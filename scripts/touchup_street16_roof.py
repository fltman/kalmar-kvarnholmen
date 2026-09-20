"""Correct the square-facing ochre gable; geometry and camera evidence are retained."""
import bpy,json,ast,math,bmesh
from pathlib import Path
R=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(R/'source/Stortorget.blend'))
name='SM_Building_92204199';obj=bpy.data.objects[name];me=obj.data
target=next(i for i,m in enumerate(me.materials) if m.name=='M_Street16_Yellow');changed=0
for p in me.polygons:
 if me.materials[p.material_index].name=='M_Street16_Ivory' and abs(p.normal.x)>.95 and p.area>1 and min(me.vertices[i].co.z for i in p.vertices)>=7.79:
  p.material_index=target;changed+=1
assert changed>=2 or any(p.material_index==target and abs(p.normal.x)>.95 and p.area>1 and min(me.vertices[i].co.z for i in p.vertices)>=7.79 for p in me.polygons)
exec(compile((R/'scripts/district_tangent_export.py').read_text(),'district_tangent_export.py','exec'))
bpy.ops.object.select_all(action='DESELECT');obj.select_set(True);bpy.context.view_layer.objects.active=obj
export_district_fbx(obj,R/'exports/meshes'/(name+'.fbx'))
bpy.ops.wm.save_as_mainfile(filepath=str(R/'source/Stortorget.blend'))
(R/'previews/street16-roof-touchup.json').write_text(json.dumps({'status':'passed','name':name,'recoloured_gable_triangles':changed}))
