"""Run inside UE 5.8: Tools > Execute Python Script, or via Build Unreal.command.
Imports only assets owned by this proof of concept, then constructs its generated map.
"""
import unreal as u
import json, math, traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
MAN=json.loads((ROOT/'exports/manifest.json').read_text())
BASE='/Game/Kalmar';MAP=BASE+'/Maps/Stortorget'
assets=u.AssetToolsHelpers.get_asset_tools();library=u.EditorAssetLibrary
actors=u.get_editor_subsystem(u.EditorActorSubsystem)
level=u.get_editor_subsystem(u.LevelEditorSubsystem)
report={'status':'building','meshes':[],'warnings':[]}
def log(s):u.log('STORTORGET: '+str(s))
def setp(obj,name,value):obj.set_editor_property(name,value)
def import_task(filename,dest,name=None,options=None):
 t=u.AssetImportTask();t.filename=str(filename);t.destination_path=dest;t.automated=True;t.replace_existing=True;t.save=True
 if name:t.destination_name=name
 if options:t.options=options
 assets.import_asset_tasks([t])
 paths=t.imported_object_paths
 if not paths:raise RuntimeError('Import produced no asset: '+str(filename))
 return u.load_asset(paths[0])
def scalar(m,value,prop,x=-250,y=0):
 n=u.MaterialEditingLibrary.create_material_expression(m,u.MaterialExpressionConstant,x,y);n.r=value
 u.MaterialEditingLibrary.connect_material_property(n,'',prop)
def material(name,spec):
 path=BASE+'/Materials';m=u.load_asset(path+'/'+name)
 if not m:m=assets.create_asset(name,path,u.Material,u.MaterialFactoryNew())
 u.MaterialEditingLibrary.delete_all_material_expressions(m)
 color=u.MaterialEditingLibrary.create_material_expression(m,u.MaterialExpressionConstant3Vector,-450,0)
 color.constant=u.LinearColor(*spec['color'],1)
 u.MaterialEditingLibrary.connect_material_property(color,'',u.MaterialProperty.MP_BASE_COLOR)
 scalar(m,spec['roughness'],u.MaterialProperty.MP_ROUGHNESS,-250,150)
 scalar(m,spec['metallic'],u.MaterialProperty.MP_METALLIC,-250,260)
 if spec.get('emission'):u.MaterialEditingLibrary.connect_material_property(color,'',u.MaterialProperty.MP_EMISSIVE_COLOR)
 if spec['texture']:
  for suffix,prop in [('BaseColor',u.MaterialProperty.MP_BASE_COLOR),('Normal',u.MaterialProperty.MP_NORMAL),('Roughness',u.MaterialProperty.MP_ROUGHNESS)]:
   name_tex='T_'+spec['texture']+'_'+suffix
   tex=import_task(ROOT/'exports/textures'/(name_tex+'.png'),BASE+'/Textures',name_tex)
   if suffix=='Normal':setp(tex,'compression_settings',u.TextureCompressionSettings.TC_NORMALMAP);setp(tex,'srgb',False);setp(tex,'flip_green_channel',True)
   elif suffix=='Roughness':setp(tex,'srgb',False)
   library.save_loaded_asset(tex)
   n=u.MaterialEditingLibrary.create_material_expression(m,u.MaterialExpressionTextureSample,-600,420)
   n.texture=tex
   uv=u.MaterialEditingLibrary.create_material_expression(m,u.MaterialExpressionTextureCoordinate,-850,420)
   uv.u_tiling=spec.get('uv_scale',1);uv.v_tiling=spec.get('uv_scale',1)
   u.MaterialEditingLibrary.connect_material_expressions(uv,'',n,'UVs')
   n.sampler_type=u.MaterialSamplerType.SAMPLERTYPE_NORMAL if suffix=='Normal' else (u.MaterialSamplerType.SAMPLERTYPE_LINEAR_COLOR if suffix=='Roughness' else u.MaterialSamplerType.SAMPLERTYPE_COLOR)
   u.MaterialEditingLibrary.connect_material_property(n,'RGB' if suffix!='Roughness' else 'R',prop)
 if spec.get('street16_tint'):
  source=u.MaterialEditingLibrary.get_material_property_input_node(m,u.MaterialProperty.MP_BASE_COLOR)
  tint=u.MaterialEditingLibrary.create_material_expression(m,u.MaterialExpressionConstant3Vector,-450,-180);tint.constant=u.LinearColor(*spec['street16_tint'],1)
  mult=u.MaterialEditingLibrary.create_material_expression(m,u.MaterialExpressionMultiply,-200,-100)
  assert u.MaterialEditingLibrary.connect_material_expressions(source,'RGB',mult,'A')
  assert u.MaterialEditingLibrary.connect_material_expressions(tint,'',mult,'B')
  assert u.MaterialEditingLibrary.connect_material_property(mult,'',u.MaterialProperty.MP_BASE_COLOR)
 if spec.get('photo'):
  tex=import_task(ROOT/'exports/textures'/spec['photo'],BASE+'/Textures','T_AltarpiecePhoto')
  n=u.MaterialEditingLibrary.create_material_expression(m,u.MaterialExpressionTextureSample,-600,-250);n.texture=tex
  u.MaterialEditingLibrary.connect_material_property(n,'RGB',u.MaterialProperty.MP_BASE_COLOR)
 if spec.get('polish15'):
  import runpy
  runpy.run_path(str(ROOT/'Unreal/Content/Python/polish15_material_graph.py'))['enhance'](m,spec,ROOT,import_task)
 u.MaterialEditingLibrary.recompile_material(m);library.save_loaded_asset(m)
 return m
def vec(p):return u.Vector(p[0]*100,-p[1]*100,p[2]*100)
def look(loc,target):return u.MathLibrary.find_look_at_rotation(vec(loc),vec(target))
def spawn(cls,name,loc=(0,0,0),rotation=None):
 a=actors.spawn_actor_from_class(cls,vec(loc),rotation or u.Rotator(0,0,0));a.set_actor_label(name);return a
try:
 for folder in ['Meshes','Materials','Textures','Maps']:library.make_directory(BASE+'/'+folder)
 mats={name:(u.load_asset(BASE+'/Materials/'+name) if '-StortorgetSceneOnly' in u.SystemLibrary.get_command_line() else material(name,spec)) for name,spec in MAN['materials'].items()}
 for material_asset in mats.values():
  if not material_asset.get_editor_property('two_sided'):
   setp(material_asset,'two_sided',True);u.MaterialEditingLibrary.recompile_material(material_asset);library.save_loaded_asset(material_asset)
 log('Materials complete')
 meshes=[]
 for spec in MAN['assets']:
  opt=u.FbxImportUI();opt.import_mesh=True;opt.import_as_skeletal=False;opt.import_materials=False;opt.import_textures=False
  opt.mesh_type_to_import=u.FBXImportType.FBXIT_STATIC_MESH;opt.automated_import_should_detect_type=False
  data=opt.static_mesh_import_data;data.combine_meshes=True;data.auto_generate_collision=False;data.generate_lightmap_u_vs=False
  data.convert_scene=True;data.convert_scene_unit=True;data.force_front_x_axis=False
  data.normal_import_method=u.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS
  mesh=(u.load_asset(BASE+'/Meshes/'+spec['name']) if '-StortorgetSceneOnly' in u.SystemLibrary.get_command_line() else import_task(ROOT/'exports'/spec['file'],BASE+'/Meshes',spec['name'],opt))
  if not isinstance(mesh,u.StaticMesh):raise TypeError(spec['name']+' did not import as a static mesh')
  slots=mesh.get_editor_property('static_materials')
  for index,slot in enumerate(slots):
   slot_name=str(slot.get_editor_property('imported_material_slot_name'))
   slot_name=spec.get('material_overrides',{}).get(slot_name,slot_name)
   if slot_name not in mats:slot_name=str(slot.get_editor_property('material_slot_name'))
   if slot_name not in mats:
    if index>=len(spec['materials']):raise RuntimeError('Unmatched material slot')
    slot_name=spec['materials'][index]
   mesh.set_material(index,mats[slot_name])
  body=mesh.get_editor_property('body_setup')
  if body:
   setp(body,'collision_trace_flag',u.CollisionTraceFlag.CTF_USE_COMPLEX_AS_SIMPLE);setp(body,'double_sided_geometry',True)
  library.save_loaded_asset(mesh)
  if spec['name'].startswith(('SM_Domkyrka','SM_Kalmar_Domkyrka')) and '-StortorgetSceneOnly' not in u.SystemLibrary.get_command_line():
   smes=u.get_editor_subsystem(u.StaticMeshEditorSubsystem)
   build=smes.get_lod_build_settings(mesh,0)
   build.set_editor_property('max_lumen_mesh_cards',32)
   if spec['name'].startswith('SM_Kalmar_Domkyrka'):build.set_editor_property('use_full_precision_u_vs',True)
   build.set_editor_property('distance_field_resolution_scale',1.0)
   build.set_editor_property('generate_distance_field_as_if_two_sided',True)
   smes.set_lod_build_settings(mesh,0,build)
   nanite=smes.get_nanite_settings(mesh);nanite.set_editor_property('enabled',True)
   if spec['name']=='SM_Domkyrka_Altar_Carving':
    nanite.set_editor_property('generate_fallback',type(nanite.get_editor_property('generate_fallback')).ENABLED)
    nanite.set_editor_property('fallback_relative_error',0.0)
   smes.set_nanite_settings(mesh,nanite,True);library.save_loaded_asset(mesh)
  bb=mesh.get_bounding_box()
  report['meshes'].append({'name':spec['name'],'min':[bb.min.x,bb.min.y,bb.min.z],'max':[bb.max.x,bb.max.y,bb.max.z],'materials':len(slots),'collision':str(body.get_editor_property('collision_trace_flag')) if body else 'MISSING'})
  meshes.append((spec,mesh))
  (ROOT/'previews/unreal-build-report.json').write_text(json.dumps(report,indent=2))
 log(str(len(meshes))+' scene meshes imported')
 if library.does_asset_exist(MAP):
  if not level.load_level(MAP):raise RuntimeError('Could not load generated map '+MAP)
  # This map is generator-owned; preserve a backup before rebuilding.
  for existing in list(actors.get_all_level_actors()):
   if not isinstance(existing,(u.WorldSettings,u.LevelScriptActor)):actors.destroy_actor(existing)
 elif not level.new_level(MAP):raise RuntimeError('Could not create generated map '+MAP)
 for spec,mesh in meshes:
  actor=actors.spawn_actor_from_object(mesh,u.Vector(0,0,0),u.Rotator(0,0,0));actor.set_actor_label(spec['name'].replace('SM_',''))
  actor.set_folder_path('Stortorget/'+spec['category'])
  actor.static_mesh_component.set_mobility(u.ComponentMobility.STATIC)
 sun=spawn(u.DirectionalLight,'Sun — afternoon',rotation=u.Rotator(pitch=-38,yaw=-45,roll=0));sun.light_component.set_mobility(u.ComponentMobility.MOVABLE)
 sun.light_component.set_intensity(4.0);setp(sun.light_component,'atmosphere_sun_light',True)
 setp(sun.light_component,'light_source_angle',1.0);setp(sun.light_component,'forward_shading_priority',1)
 sky=spawn(u.SkyLight,'Sky light');sky.light_component.set_mobility(u.ComponentMobility.MOVABLE);setp(sky.light_component,'real_time_capture',True);sky.light_component.set_intensity(3.0)
 fill=spawn(u.DirectionalLight,'Soft sky fill',rotation=u.Rotator(pitch=-60,yaw=135,roll=0));fill.light_component.set_mobility(u.ComponentMobility.MOVABLE);fill.light_component.set_intensity(.65);setp(fill.light_component,'cast_shadows',False);setp(fill.light_component,'atmosphere_sun_light',False)
 # Broad interior light sources, independent from the exterior sunlight.
 for x in [-8,10.1,28]:
  lamp=spawn(u.PointLight,'Cathedral ambient '+str(x),(x,44.4,12))
  lamp.light_component.set_mobility(u.ComponentMobility.MOVABLE);lamp.light_component.set_intensity(80)
  setp(lamp.light_component,'attenuation_radius',2200);setp(lamp.light_component,'source_radius',200)
  setp(lamp.light_component,'cast_shadows',False);lamp.set_folder_path('Stortorget/Cathedral interior lights')
 for x in [-13,33]:
  for y in [38.6,50.2]:
   lamp=spawn(u.PointLight,'Cathedral window fill',(x,y,7.5))
   lamp.light_component.set_mobility(u.ComponentMobility.MOVABLE);lamp.light_component.set_intensity(35)
   setp(lamp.light_component,'attenuation_radius',1300);setp(lamp.light_component,'source_radius',100)
   setp(lamp.light_component,'cast_shadows',False);lamp.set_folder_path('Stortorget/Cathedral interior lights')
 spawn(u.SkyAtmosphere,'Baltic daylight sky')
 fog=spawn(u.ExponentialHeightFog,'Soft distance haze');setp(fog.get_component_by_class(u.ExponentialHeightFogComponent),'fog_density',.003)
 post=spawn(u.PostProcessVolume,'Exposure');post.unbound=True
 settings=post.settings;settings.override_auto_exposure_method=True;settings.auto_exposure_method=u.AutoExposureMethod.AEM_MANUAL
 settings.override_auto_exposure_bias=True;settings.auto_exposure_bias=0
 settings.override_auto_exposure_apply_physical_camera_exposure=True;settings.auto_exposure_apply_physical_camera_exposure=False
 post.settings=settings
 # Human-scale first person start, facing the cathedral. Official Epic template BP.
 start=spawn(u.PlayerStart,'Start — south side of square',(-12,-22,1.10),look((-12,-22,1.8),(10,40,1.8)))
 for camera in MAN['cameras']:
  a=spawn(u.CameraActor,camera['name'],camera['location'],look(camera['location'],camera['target']))
  a.camera_component.set_field_of_view(math.degrees(2*math.atan(36/(2*camera['lens']))));a.set_folder_path('Review cameras')
 # No weapons. The standard template provides WASD + mouse + jump.
 gm=u.load_class(None,'/Game/FirstPerson/Blueprints/BP_FirstPersonGameMode.BP_FirstPersonGameMode_C')
 if not gm:raise RuntimeError('First person game mode failed to load')
 world=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world();world.get_world_settings().set_editor_property('default_game_mode',gm)
 # First-person walking pace.
 char=u.load_class(None,'/Game/FirstPerson/Blueprints/BP_FirstPersonCharacter.BP_FirstPersonCharacter_C')
 if char:
  cdo=u.get_default_object(char);cdo.character_movement.max_walk_speed=350
  library.save_asset('/Game/FirstPerson/Blueprints/BP_FirstPersonCharacter')
 cam=MAN['cameras'][0];u.get_editor_subsystem(u.UnrealEditorSubsystem).set_level_viewport_camera_info(vec(cam['location']),look(cam['location'],cam['target']))
 exec(compile((ROOT/'Unreal/Content/Python/configure_hero_scene.py').read_text(),str(ROOT/'Unreal/Content/Python/configure_hero_scene.py'),'exec'))
 level.save_current_level();library.save_directory(BASE,only_if_is_dirty=False,recursive=True)
 report['actor_count']=len(actors.get_all_level_actors());report['status']='complete';report['map']=MAP
 (ROOT/'previews/unreal-build-report.json').write_text(json.dumps(report,indent=2))
 log('BUILD_COMPLETE — '+MAP)
except Exception:
 report['status']='failed';report['error']=traceback.format_exc();(ROOT/'previews/unreal-build-report.json').write_text(json.dumps(report,indent=2));u.log_error(report['error']);raise
