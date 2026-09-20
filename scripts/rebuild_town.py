"""Rebuild only the square frontages; preserve cathedral geometry and saved scene."""
import bpy,bmesh,math,json,ast,random
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(R/'source/Stortorget.blend'))
scene=bpy.context.scene;materials={m.name:m for m in bpy.data.materials};manifest=json.loads((R/'exports/manifest.json').read_text());specs=manifest['materials'];CHURCH_TEXTURES={}
tree=ast.parse((R/'scripts/build_blender.py').read_text())
for node in tree.body:
 if isinstance(node,ast.Assign) and isinstance(node.value,ast.Call) and isinstance(node.value.func,ast.Name) and node.value.func.id=='mat':
  for target in node.targets:
   if isinstance(target,ast.Name):globals()[target.id]=ast.literal_eval(node.value.args[0])
tree.body=[n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name in {'mat','Mesh','wallbox','window','hip','pediment','roundwindow'}]
exec(compile(tree,'town_production_helpers','exec'))
# Re-running the selective build keeps stable material names.
for material_block in list(bpy.data.materials):
 if material_block.name.startswith('M_Town_'):bpy.data.materials.remove(material_block)
site=json.loads((R/'source/site.json').read_text());buildings={b['id']:b for b in site['buildings']}
exec(compile((R/'scripts/build_town_details.py').read_text(),str(R/'scripts/build_town_details.py'),'exec'))
for name in town_names:
 obj=bpy.data.objects[name]
 bpy.ops.object.select_all(action='DESELECT');obj.select_set(True);bpy.context.view_layer.objects.active=obj
 bpy.ops.export_scene.fbx(filepath=str(R/'exports/meshes'/(name+'.fbx')),use_selection=True,object_types={'MESH'},axis_forward='-Y',axis_up='Z',apply_unit_scale=True,global_scale=1,bake_space_transform=False,mesh_smooth_type='FACE',add_leaf_bones=False,path_mode='AUTO')
 old=next(s for s in manifest['assets'] if s['name']==name)
 old.update(materials=[m.name for m in obj.data.materials],vertices=len(obj.data.vertices),polygons=len(obj.data.polygons))
for name,loc,target,lens in town_cameras:
 obj=bpy.data.objects.get(name)
 if obj:bpy.data.objects.remove(obj,do_unlink=True)
 bpy.ops.object.camera_add(location=loc);obj=bpy.context.object;obj.name=name;obj.rotation_euler=(Vector(target)-obj.location).to_track_quat('-Z','Y').to_euler();obj.data.lens=lens
 manifest['cameras']=[s for s in manifest['cameras'] if s['name']!=name]
 manifest['cameras'].append({'name':name,'location':loc,'target':target,'lens':lens})
manifest['total_vertices']=sum(s['vertices'] for s in manifest['assets']);manifest['total_polygons']=sum(s['polygons'] for s in manifest['assets'])
(R/'exports/manifest.json').write_text(json.dumps(manifest,indent=2));bpy.ops.wm.save_as_mainfile(filepath=str(R/'source/Stortorget.blend'))
(R/'previews/town-pass9-build.json').write_text(json.dumps({'status':'passed','updated':town_names,'vertices':manifest['total_vertices'],'polygons':manifest['total_polygons']},indent=2));print('TOWN_REBUILD_OK')
