"""Incremental geometry repair, using exactly the canonical generator helpers."""
import bpy,bmesh,math,json,ast
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[1];cx,cy=10.1,44.4
bpy.ops.wm.open_mainfile(filepath=str(R/'source/Stortorget.blend'))
materials={m.name:m for m in bpy.data.materials};IVORY='M_Interior_Lime';GOLD='M_Gold'
for filename,names in [('build_blender.py',{'Mesh'}),('build_interior.py',{'box'}),('sculpture_helpers.py',{'ellipsoid'})]:
 tree=ast.parse((R/'scripts'/filename).read_text());tree.body=[n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name in names];exec(compile(tree,filename,'exec'))
for o in list(bpy.data.objects):
 if o.name.startswith('SM_Domkyrka_Ionic_Details'):bpy.data.objects.remove(o,do_unlink=True)
for script in ['build_ionic_details.py','partition_for_lumen.py']:exec(compile((R/'scripts'/script).read_text(),str(R/'scripts'/script),'exec'))
manifest=json.loads((R/'exports/manifest.json').read_text());manifest['assets']=[s for s in manifest['assets'] if not s['name'].startswith('SM_Domkyrka_Ionic_Details')]
for obj in sorted([o for o in bpy.data.objects if o.type=='MESH' and o.name.startswith('SM_Domkyrka_Ionic_Details')],key=lambda o:o.name):
 bpy.ops.object.select_all(action='DESELECT');obj.select_set(True);bpy.context.view_layer.objects.active=obj
 bpy.ops.export_scene.fbx(filepath=str(R/'exports/meshes'/(obj.name+'.fbx')),use_selection=True,object_types={'MESH'},axis_forward='-Y',axis_up='Z',apply_unit_scale=True,global_scale=1,bake_space_transform=False,mesh_smooth_type='FACE',add_leaf_bones=False,path_mode='AUTO')
 manifest['assets'].append({'name':obj.name,'file':'meshes/'+obj.name+'.fbx','category':obj['category'],'materials':[m.name for m in obj.data.materials],'vertices':len(obj.data.vertices),'polygons':len(obj.data.polygons)})
manifest['total_vertices']=sum(x['vertices'] for x in manifest['assets']);manifest['total_polygons']=sum(x['polygons'] for x in manifest['assets'])
(R/'exports/manifest.json').write_text(json.dumps(manifest,indent=2));bpy.ops.wm.save_as_mainfile(filepath=str(R/'source/Stortorget.blend'))
print('IONIC_REPAIR_OK',len(manifest['assets']),manifest['total_vertices'],manifest['total_polygons'])
