"""Repair only collapsed UV triangles introduced by bevel interpolation."""
import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parents[1];bpy.ops.wm.open_mainfile(filepath=str(R/'source/Stortorget.blend'))
repaired=[]
for obj in list(bpy.data.objects):
 if not obj.name.startswith('SM_Kalmar_Domkyrka'):continue
 me=obj.data;me.calc_loop_triangles();uv=me.uv_layers.active.data;bad=set()
 for t in me.loop_triangles:
  a,b,c=[uv[i].uv for i in t.loops];d=b-a;e=c-a
  if abs(d.x*e.y-d.y*e.x)<1e-12:bad.add(t.polygon_index)
 if not bad:continue
 for pi in bad:
  p=me.polygons[pi];dominant=max(range(3),key=lambda i:abs(p.normal[i]));axes=[i for i in range(3) if i!=dominant]
  for li in p.loop_indices:
   co=me.vertices[me.loops[li].vertex_index].co;uv[li].uv=(co[axes[0]]/4,co[axes[1]]/4)
 bpy.ops.object.select_all(action='DESELECT');obj.select_set(True);bpy.context.view_layer.objects.active=obj
 bpy.ops.export_scene.fbx(filepath=str(R/'exports/meshes'/(obj.name+'.fbx')),use_selection=True,object_types={'MESH'},axis_forward='-Y',axis_up='Z',apply_unit_scale=True,global_scale=1,bake_space_transform=False,mesh_smooth_type='FACE',add_leaf_bones=False,path_mode='AUTO')
 repaired.append({'name':obj.name,'faces':len(bad)})
(R/'previews/exterior-uv-repaired.json').write_text(json.dumps(repaired,indent=2));bpy.ops.wm.save_as_mainfile(filepath=str(R/'source/Stortorget.blend'));print('UV_REPAIRED',repaired)
