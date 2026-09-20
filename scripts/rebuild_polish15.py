"""Incremental corridor build: preserve all existing authored objects outside its scope."""
import bpy,bmesh,math,json,ast,random
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(R/'source/Stortorget.blend'))
scene=bpy.context.scene;materials={m.name:m for m in bpy.data.materials}
manifest=json.loads((R/'exports/manifest.json').read_text());specs=manifest['materials'];CHURCH_TEXTURES={}
tree=ast.parse((R/'scripts/build_blender.py').read_text())
for n in tree.body:
 if isinstance(n,ast.Assign) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Name) and n.value.func.id=='mat':
  for target in n.targets:
   if isinstance(target,ast.Name):globals()[target.id]=ast.literal_eval(n.value.args[0])
tree.body=[n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name in {'mat','Mesh','wallbox','window','hip','pediment','roundwindow'}]
exec(compile(tree,'production_core','exec'))
town_mats={name.removeprefix('M_Town_'):name for name in materials if name.startswith('M_Town_') and '.' not in name}
TI,TL,TY,TS=[town_mats[k] for k in ['Ivory','Lime','Yellow','Stone']]
TW,TB,TG,TT,TC=[town_mats[k] for k in ['PaintWhite','PaintBlue','PaintGreen','TileRed','Copper']]
for filename in ['build_town_details.py','town_detail_helpers.py']:
 tree=ast.parse((R/'scripts'/filename).read_text());tree.body=[n for n in tree.body if isinstance(n,ast.FunctionDef)]
 exec(compile(tree,filename,'exec'))
exec(compile((R/'scripts/apply_polish15_blender.py').read_text(),'apply_polish15_blender.py','exec'))
exec(compile((R/'scripts/polish15_geometry_helpers.py').read_text(),'polish15_geometry_helpers.py','exec'))
exec(compile((R/'scripts/build_landmarks14.py').read_text(),str(R/'scripts/build_landmarks14.py'),'exec'))
exec(compile((R/'scripts/build_facades15.py').read_text(),'build_facades15.py','exec'))
extension_names=landmark_names+facade15_names;extension_cameras=landmark_cameras
(R/'previews/facades15-coverage.json').write_text(json.dumps({'status':'passed','buildings':facade15_audit,'count':len(facade15_audit),'windows':sum(v['windows'] for v in facade15_audit.values()),'doors':sum(v['doors'] for v in facade15_audit.values())},indent=2))
bpy.ops.wm.save_as_mainfile(filepath=str(R/'source/polish15-working.blend'))
(R/'source/polish15-working.json').write_text(json.dumps({'names':extension_names,'cameras':extension_cameras,'manifest':manifest}))
exec(compile((R/'scripts/district_tangent_export.py').read_text(),'district_tangent_export.py','exec'))
audit={}
for name in extension_names:
 print('EXPORT15',name,flush=True)
 obj=bpy.data.objects[name];me=obj.data;bm=bmesh.new();bm.from_mesh(me);bmesh.ops.triangulate(bm,faces=list(bm.faces));bad=[f for f in bm.faces if f.calc_area()<1e-7]
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
