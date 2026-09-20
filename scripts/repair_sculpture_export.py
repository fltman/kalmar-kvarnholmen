import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
exec(compile((R/'scripts/clean_sculpture_mesh.py').read_text(),str(R/'scripts/clean_sculpture_mesh.py'),'exec'))
ob=bpy.data.objects['SM_Domkyrka_Altar_Carving']
report=clean_sculpture_mesh(ob.data)
bpy.ops.object.select_all(action='DESELECT');ob.select_set(True);bpy.context.view_layer.objects.active=ob
bpy.ops.export_scene.fbx(filepath=str(R/'exports/meshes'/f'{ob.name}.fbx'),use_selection=True,object_types={'MESH'},axis_forward='-Y',axis_up='Z',apply_unit_scale=True,global_scale=1,bake_space_transform=False,mesh_smooth_type='FACE',add_leaf_bones=False,path_mode='AUTO')
m=json.loads((R/'exports/manifest.json').read_text())
for a in m['assets']:
 if a['name']==ob.name:a.update(vertices=len(ob.data.vertices),polygons=len(ob.data.polygons))
m['total_vertices']=sum(a['vertices'] for a in m['assets']);m['total_polygons']=sum(a['polygons'] for a in m['assets'])
(R/'exports/manifest.json').write_text(json.dumps(m,indent=2))
(R/'previews/hero-sculpture-cleanup.json').write_text(json.dumps(report,indent=2))
bpy.ops.wm.save_as_mainfile(filepath=str(R/'source/Stortorget.blend'))
print('SCULPTURE_CLEANED',report)
