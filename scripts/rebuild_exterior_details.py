"""Incremental export of the canonical exterior details, retaining the saved world."""
import bpy,bmesh,math,json,ast
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[1];cx,cy=10.1,44.4
bpy.ops.wm.open_mainfile(filepath=str(R/'source/Stortorget.blend'))
materials={m.name:m for m in bpy.data.materials}
STONE='M_Limestone';COPPER='M_Aged_Copper';GOLD='M_Gold';GREEN='M_Door_Green';IRON='M_Iron';BASE='M_Foundation';IVORY='M_Interior_Lime'
CHURCHSTONE='M_Church_Cut_Stone';CHURCHCOPPER='M_Church_Copper';CHURCHROOF='M_Church_Roof';CHURCHURN='M_Church_Urn'
p=next(b['polygon'] for b in json.loads((R/'source/site.json').read_text())['buildings'] if b['id']=='38319501')
for filename,names in [('build_blender.py',{'Mesh'}),('build_interior.py',{'box','rod','curve','sphere'}),('sculpture_helpers.py',None),('exterior_helpers.py',None)]:
 tree=ast.parse((R/'scripts'/filename).read_text());tree.body=[n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and (names is None or n.name in names)];exec(compile(tree,filename,'exec'))
name='SM_Domkyrka_Exterior_Details';bpy.data.objects.remove(bpy.data.objects[name],do_unlink=True)
s=(R/'scripts/build_church_details.py').read_text();a=s.index('# Exterior stonework');b=s.index('# True painting photo:',a);exec(compile(s[a:b],'exterior_details','exec'))
obj=bpy.data.objects[name];bpy.ops.object.select_all(action='DESELECT');obj.select_set(True);bpy.context.view_layer.objects.active=obj
bpy.ops.export_scene.fbx(filepath=str(R/'exports/meshes'/(name+'.fbx')),use_selection=True,object_types={'MESH'},axis_forward='-Y',axis_up='Z',apply_unit_scale=True,global_scale=1,bake_space_transform=False,mesh_smooth_type='FACE',add_leaf_bones=False,path_mode='AUTO')
manifest=json.loads((R/'exports/manifest.json').read_text());spec=next(s for s in manifest['assets'] if s['name']==name);spec.update(materials=[m.name for m in obj.data.materials],vertices=len(obj.data.vertices),polygons=len(obj.data.polygons))
manifest['total_vertices']=sum(s['vertices'] for s in manifest['assets']);manifest['total_polygons']=sum(s['polygons'] for s in manifest['assets'])
(R/'exports/manifest.json').write_text(json.dumps(manifest,indent=2));bpy.ops.wm.save_as_mainfile(filepath=str(R/'source/Stortorget.blend'));print('EXTERIOR_DETAILS_OK')
