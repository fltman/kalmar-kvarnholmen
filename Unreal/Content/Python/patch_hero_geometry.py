import unreal as u,json
from pathlib import Path
R=Path(__file__).resolve().parents[3]
assets=u.AssetToolsHelpers.get_asset_tools();library=u.EditorAssetLibrary
for name in ['SM_Domkyrka_Altar_Carving']:
 opt=u.FbxImportUI();opt.import_mesh=True;opt.import_as_skeletal=False;opt.import_materials=False;opt.import_textures=False;opt.mesh_type_to_import=u.FBXImportType.FBXIT_STATIC_MESH;opt.automated_import_should_detect_type=False
 data=opt.static_mesh_import_data;data.combine_meshes=True;data.auto_generate_collision=False;data.generate_lightmap_u_vs=False;data.convert_scene=True;data.convert_scene_unit=True;data.force_front_x_axis=False;data.normal_import_method=u.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS
 t=u.AssetImportTask();t.filename=str(R/'exports/meshes'/(name+'.fbx'));t.destination_path='/Game/Kalmar/Meshes';t.destination_name=name;t.automated=True;t.replace_existing=True;t.save=True;t.options=opt;assets.import_asset_tasks([t])
 if not t.imported_object_paths:raise RuntimeError('Sculpture import produced no assets; review the import log')
 mesh=u.load_asset('/Game/Kalmar/Meshes/'+name)
 if not mesh or mesh.get_name()!=name:raise RuntimeError('Sculpture path resolved to an unexpected resource')
 for i,slot in enumerate(mesh.get_editor_property('static_materials')):
  mat=u.load_asset('/Game/Kalmar/Materials/'+str(slot.get_editor_property('imported_material_slot_name')))
  if mat and mesh.get_material(i)!=mat:mesh.set_material(i,mat)
 body=mesh.get_editor_property('body_setup');body.set_editor_property('collision_trace_flag',u.CollisionTraceFlag.CTF_USE_COMPLEX_AS_SIMPLE);body.set_editor_property('double_sided_geometry',True);library.save_loaded_asset(mesh)
 smes=u.get_editor_subsystem(u.StaticMeshEditorSubsystem)
 build=smes.get_lod_build_settings(mesh,0)
 changes={'remove_degenerates':True,'max_lumen_mesh_cards':32,'generate_distance_field_as_if_two_sided':True}
 if any(build.get_editor_property(k)!=v for k,v in changes.items()):
  for k,v in changes.items():build.set_editor_property(k,v)
  smes.set_lod_build_settings(mesh,0,build)
 nanite=smes.get_nanite_settings(mesh)
 changes={'enabled':True,'generate_fallback':type(nanite.get_editor_property('generate_fallback')).ENABLED,'fallback_relative_error':0.0}
 if any(nanite.get_editor_property(k)!=v for k,v in changes.items()):
  for k,v in changes.items():nanite.set_editor_property(k,v)
  smes.set_nanite_settings(mesh,nanite,True)
 library.save_loaded_asset(mesh)
 for a in u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors():
  if a.get_actor_label()==name.replace('SM_',''):a.static_mesh_component.set_static_mesh(mesh)
world=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
for a in u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors():
 if isinstance(a,u.DirectionalLight):a.light_component.set_editor_property('forward_shading_priority',0 if 'fill' in a.get_actor_label() else 1)
u.get_editor_subsystem(u.LevelEditorSubsystem).save_current_level()


P=R/'Unreal/Content/Python'
exec(compile((P/'start_hero_review.py').read_text(),str(P/'start_hero_review.py'),'exec'))
