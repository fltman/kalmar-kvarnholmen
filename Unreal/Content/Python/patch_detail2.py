import unreal as u,json
from pathlib import Path
R=Path(__file__).resolve().parents[3]
assets=u.AssetToolsHelpers.get_asset_tools();library=u.EditorAssetLibrary
for name in ['SM_Domkyrka_Altar_Carving']:
 opt=u.FbxImportUI();opt.import_mesh=True;opt.import_as_skeletal=False;opt.import_materials=False;opt.import_textures=False;opt.mesh_type_to_import=u.FBXImportType.FBXIT_STATIC_MESH;opt.automated_import_should_detect_type=False
 data=opt.static_mesh_import_data;data.combine_meshes=True;data.auto_generate_collision=False;data.generate_lightmap_u_vs=False;data.convert_scene=True;data.convert_scene_unit=True;data.force_front_x_axis=False;data.normal_import_method=u.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS
 t=u.AssetImportTask();t.filename=str(R/'exports/meshes'/(name+'.fbx'));t.destination_path='/Game/Kalmar/Meshes';t.destination_name=name;t.automated=True;t.replace_existing=True;t.save=True;t.options=opt;assets.import_asset_tasks([t])
 mesh=u.load_asset('/Game/Kalmar/Meshes/'+name)
 for i,slot in enumerate(mesh.get_editor_property('static_materials')):
  mat=u.load_asset('/Game/Kalmar/Materials/'+str(slot.get_editor_property('imported_material_slot_name')))
  if mat:mesh.set_material(i,mat)
 body=mesh.get_editor_property('body_setup');body.set_editor_property('collision_trace_flag',u.CollisionTraceFlag.CTF_USE_COMPLEX_AS_SIMPLE);body.set_editor_property('double_sided_geometry',True);library.save_loaded_asset(mesh)
world=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
for a in u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors():
 if isinstance(a,u.DirectionalLight):a.light_component.set_editor_property('forward_shading_priority',0 if 'fill' in a.get_actor_label() else 1)
u.get_editor_subsystem(u.LevelEditorSubsystem).save_current_level()

# Synchronise saved review cameras with the Blender manifest.
import math
actors=u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors()
manifest=json.loads((R/'exports/manifest.json').read_text())
for spec in manifest['cameras']:
 cam=next(a for a in actors if a.get_actor_label()==spec['name'])
 loc=u.Vector(spec['location'][0]*100,-spec['location'][1]*100,spec['location'][2]*100)
 target=u.Vector(spec['target'][0]*100,-spec['target'][1]*100,spec['target'][2]*100)
 cam.set_actor_location(loc,False,False);cam.set_actor_rotation(u.MathLibrary.find_look_at_rotation(loc,target),False)
 cam.camera_component.set_field_of_view(math.degrees(2*math.atan(36/(2*spec['lens']))))
u.get_editor_subsystem(u.LevelEditorSubsystem).save_current_level()
checks={}
for name,start,end,expect in [('doorway',(1010,-2200,300),(1010,-3100,300),False),('aisle',(-800,-4440,280),(2100,-4440,280),False),('floor',(1010,-4440,300),(1010,-4440,0),True)]:
 hit=u.SystemLibrary.line_trace_single(world,u.Vector(*start),u.Vector(*end),u.TraceTypeQuery.TRACE_TYPE_QUERY1,True,[],u.DrawDebugTrace.NONE,True)
 checks[name]=(hit is not None)==expect
checks['status']='passed' if all(checks.values()) else 'failed'
(R/'previews/unreal-final-collision-check.json').write_text(json.dumps(checks,indent=2))
exec(compile((R/'Unreal/Content/Python/review_detail2.py').read_text(),str(R/'Unreal/Content/Python/review_detail2.py'),'exec'))
