import bpy,bmesh,math,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(R/'source/polish15-working.blend'))
w=json.loads((R/'source/polish15-working.json').read_text());manifest=w['manifest'];extension_names=w['names'];extension_cameras=w['cameras']
exec(compile((R/'scripts/district_tangent_export.py').read_text(),'district_tangent_export.py','exec'))
audit={}
for name in extension_names:
 print('EXPORT15',name,flush=True)
 obj=bpy.data.objects[name];me=obj.data
 if obj.get('category')=='Kvarnholmen/Completed facades':
  # Give the stone plinth a real projection instead of coplanar plaster/stone faces.
  groups={}
  for face in me.polygons:
   if me.materials[face.material_index].name!='M_Town_Stone':continue
   ids=list(face.vertices)
   if min(me.vertices[i].co.z for i in ids)<-.001 or max(me.vertices[i].co.z for i in ids)>.345:continue
   # Each plinth was emitted as one independent eight-vertex box.
   for existing in list(groups):
    if groups[existing][0].intersection(ids):
     groups[existing][0].update(ids)
     if abs(face.normal.z)<.1 and face.area>groups[existing][2]:groups[existing]=(groups[existing][0],face.normal.copy(),face.area)
     break
   else:groups[min(ids)]=(set(ids),face.normal.copy(),face.area if abs(face.normal.z)<.1 else 0)
  for ids,n,area in groups.values():
   if area<=0:continue
   centre=sum((me.vertices[i].co for i in ids),Vector())/len(ids)
   for i in ids:
    v=me.vertices[i];v.co+=n*(.02 if (v.co-centre).dot(n)>0 else -.02)
  me.update()
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.triangulate(bm,faces=list(bm.faces));bad=[f for f in bm.faces if f.calc_area()<1e-7]
 if bad:bmesh.ops.delete(bm,geom=bad,context='FACES')
 bm.to_mesh(me);bm.free();me.update();me.calc_loop_triangles();uv=me.uv_layers.active.data
 # Align tile courses to ridge and slope instead of a world-axis projection.
 for poly in me.polygons:
  if me.materials[poly.material_index].name=='M_Town_TileRed' and poly.normal.z>.2 and abs(poly.normal.z)<.999:
   n=poly.normal;uaxis=Vector((n.y,-n.x,0)).normalized();vaxis=n.cross(uaxis).normalized()
   for li in poly.loop_indices:
    co=me.vertices[me.loops[li].vertex_index].co;uv[li].uv=(co.dot(uaxis)/4,co.dot(vaxis)/4)
 # Dominant-plane projection repairs occasional triangulated Boolean UV slivers.
 repaired=set()
 for tri in me.loop_triangles:
  a,b,c=[uv[i].uv for i in tri.loops];d=b-a;e=c-a
  if abs(d.x*e.y-d.y*e.x)<1e-12:repaired.add(tri.polygon_index)
 for pi in repaired:
  poly=me.polygons[pi];axis=max(range(3),key=lambda i:abs(poly.normal[i]));axes=[i for i in range(3) if i!=axis]
  for li in poly.loop_indices:
   co=me.vertices[me.loops[li].vertex_index].co;uv[li].uv=(co[axes[0]]/4,co[axes[1]]/4)
 me.calc_loop_triangles();zeros=0
 for tri in me.loop_triangles:
  a,b,c=[uv[i].uv for i in tri.loops];d=b-a;e=c-a
  if abs(d.x*e.y-d.y*e.x)<1e-12:zeros+=1
 me.calc_tangents(uvmap=me.uv_layers.active.name)
 zero_tangents=sum(loop.tangent.length<1e-4 for loop in me.loops)
 audit[name]={'mikk_zero_loops_before_export_repair':zero_tangents,'vertices':len(me.vertices),'polygons':len(me.polygons),'reprojected_polygons':len(repaired),'zero_uv_triangles':zeros}
 bpy.ops.object.select_all(action='DESELECT');obj.select_set(True);bpy.context.view_layer.objects.active=obj
 audit[name]['export_frame_repairs']=export_district_fbx(obj,R/'exports/meshes'/(name+'.fbx'))
 manifest['assets']=[a for a in manifest['assets'] if a['name']!=name]
 manifest['assets'].append({'name':name,'file':'meshes/'+name+'.fbx','category':obj['category'],'materials':[m.name for m in me.materials],'vertices':len(me.vertices),'polygons':len(me.polygons)})
for name,loc,target,lens in extension_cameras:
 obj=bpy.data.objects.get(name)
 if obj:bpy.data.objects.remove(obj,do_unlink=True)
 bpy.ops.object.camera_add(location=loc);obj=bpy.context.object;obj.name=name;obj.rotation_euler=(Vector(target)-obj.location).to_track_quat('-Z','Y').to_euler();obj.data.lens=lens
 manifest['cameras']=[s for s in manifest['cameras'] if s['name']!=name];manifest['cameras'].append({'name':name,'location':loc,'target':target,'lens':lens})
manifest['total_vertices']=sum(s['vertices'] for s in manifest['assets']);manifest['total_polygons']=sum(s['polygons'] for s in manifest['assets'])
(R/'exports/manifest.json').write_text(json.dumps(manifest,indent=2));bpy.ops.wm.save_as_mainfile(filepath=str(R/'source/Stortorget.blend'))
(R/'previews/polish15-build.json').write_text(json.dumps({'status':'passed' if not any(x['zero_uv_triangles'] for x in audit.values()) else 'uv_review_required','assets':audit,'changed':extension_names,'cameras':[c[0] for c in extension_cameras]},indent=2));print('POLISH15_BUILD_OK')
