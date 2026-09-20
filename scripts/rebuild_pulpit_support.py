import bpy,bmesh,math,json,ast
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[1];cx,cy=10.1,44.4
bpy.ops.wm.open_mainfile(filepath=str(R/'source/Stortorget.blend'))
materials={m.name:m for m in bpy.data.materials};MARBLE='M_Column_Dark';IVORY='M_Interior_Lime';GREEN='M_Door_Green';IRON='M_Iron';GOLD='M_Gold'
for filename,names in [('build_blender.py',{'Mesh'}),('build_interior.py',{'box','rod'})]:
 tree=ast.parse((R/'scripts'/filename).read_text());tree.body=[n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name in names];exec(compile(tree,filename,'exec'))
name='SM_Domkyrka_Pulpit_Support';bpy.data.objects.remove(bpy.data.objects[name],do_unlink=True)
s=(R/'scripts/build_interior.py').read_text();a=s.index('# Continuous physical load path:');b=s.index('# Area lights',a);exec(compile(s[a:b],'pulpit_support','exec'))
obj=bpy.data.objects[name];bpy.ops.object.select_all(action='DESELECT');obj.select_set(True);bpy.context.view_layer.objects.active=obj
bpy.ops.export_scene.fbx(filepath=str(R/'exports/meshes'/(name+'.fbx')),use_selection=True,object_types={'MESH'},axis_forward='-Y',axis_up='Z',apply_unit_scale=True,global_scale=1,bake_space_transform=False,mesh_smooth_type='FACE',add_leaf_bones=False,path_mode='AUTO')
manifest=json.loads((R/'exports/manifest.json').read_text());spec=next(s for s in manifest['assets'] if s['name']==name);spec.update(materials=[m.name for m in obj.data.materials],vertices=len(obj.data.vertices),polygons=len(obj.data.polygons))
# A wider review camera shows floor, bowl, pier and canopy together.
cam=bpy.data.objects['16_Predikstol_Infästning'];loc=(10,45,3.2);target=(19.2,52.3,7);lens=23
cam.location=loc;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=lens
next(c for c in manifest['cameras'] if c['name']==cam.name).update(location=loc,target=target,lens=lens)
manifest['total_vertices']=sum(s['vertices'] for s in manifest['assets']);manifest['total_polygons']=sum(s['polygons'] for s in manifest['assets'])
(R/'exports/manifest.json').write_text(json.dumps(manifest,indent=2));bpy.ops.wm.save_as_mainfile(filepath=str(R/'source/Stortorget.blend'))
print('PULPIT_SUPPORT_OK')
