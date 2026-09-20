"""Selective surrounding-house import; preserve the hand-reviewed lighting and other assets."""
import unreal as u,json,math,ast,traceback
from pathlib import Path
ROOT=R=Path(__file__).resolve().parents[3]
MAN=json.loads((R/'exports/manifest.json').read_text());BASE='/Game/Kalmar'
assets=u.AssetToolsHelpers.get_asset_tools();library=u.EditorAssetLibrary
actors=u.get_editor_subsystem(u.EditorActorSubsystem);level=u.get_editor_subsystem(u.LevelEditorSubsystem)
smes=u.get_editor_subsystem(u.StaticMeshEditorSubsystem)
# Reuse the production import/material helpers without rebuilding the level.
tree=ast.parse((R/'Unreal/Content/Python/build_stortorget.py').read_text())
tree.body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in {'setp','import_task','scalar','material','vec','look'}]
exec(compile(tree,'production_material_helpers','exec'))
report={'status':'importing','meshes':[],'materials':{},'checks':{}}
ionic_only=False
try:
 for name in ['M_Kvarnholmen_Asphalt','M_Kvarnholmen_Water']:
  mat_asset=u.load_asset(BASE+'/Materials/'+name) if ionic_only else material(name,MAN['materials'][name])
  mat_asset.set_editor_property('two_sided',True)
  mat_asset.set_editor_property('used_with_nanite',True)
  u.MaterialEditingLibrary.recompile_material(mat_asset);library.save_loaded_asset(mat_asset)
  if MAN['materials'][name].get('texture'):
   node=u.MaterialEditingLibrary.get_material_property_input_node(mat_asset,u.MaterialProperty.MP_NORMAL)
   rough=u.MaterialEditingLibrary.get_material_property_input_node(mat_asset,u.MaterialProperty.MP_ROUGHNESS)
   tex=node.texture if isinstance(node,u.MaterialExpressionTextureSample) else None
   report['materials'][name]={'normal_connected':tex is not None,'roughness_connected':isinstance(rough,u.MaterialExpressionTextureSample),'normal_texture':tex.get_name() if tex else None,'normal_srgb':tex.get_editor_property('srgb') if tex else None,'flip_green':tex.get_editor_property('flip_green_channel') if tex else None,'compression':str(tex.get_editor_property('compression_settings')) if tex else None}
 prefixes=('SM_Kvarnholmen_',)
 selected=[s for s in MAN['assets'] if s['name'].startswith(prefixes)]
 expected={s['name'] for s in selected}
 for a in list(actors.get_all_level_actors()):
  if isinstance(a,u.StaticMeshActor):
   mesh=a.static_mesh_component.static_mesh
   if mesh and mesh.get_name().startswith(prefixes) and mesh.get_name() not in expected:actors.destroy_actor(a)
 existing={a.get_actor_label():a for a in actors.get_all_level_actors()}
 for spec in selected:
  name=spec['name'];opt=u.FbxImportUI();opt.import_mesh=True;opt.import_as_skeletal=False;opt.import_materials=False;opt.import_textures=False
  opt.mesh_type_to_import=u.FBXImportType.FBXIT_STATIC_MESH;opt.automated_import_should_detect_type=False
  data=opt.static_mesh_import_data;data.build_nanite=not name.startswith('SM_Kvarnholmen_');data.combine_meshes=True;data.auto_generate_collision=False;data.generate_lightmap_u_vs=False;data.convert_scene=True;data.convert_scene_unit=True;data.force_front_x_axis=False;data.normal_import_method=u.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS_AND_TANGENTS
  mesh=import_task(R/'exports'/spec['file'],BASE+'/Meshes',name,opt)
  if not isinstance(mesh,u.StaticMesh):raise RuntimeError('Wrong asset type: '+name)
  for i,slot in enumerate(mesh.get_editor_property('static_materials')):
   mat_name=str(slot.get_editor_property('imported_material_slot_name'));ma=u.load_asset(BASE+'/Materials/'+mat_name)
   if not ma:raise RuntimeError('Missing material: '+mat_name)
   if mesh.get_material(i)!=ma:mesh.set_material(i,ma)
  body=mesh.get_editor_property('body_setup');body.set_editor_property('collision_trace_flag',u.CollisionTraceFlag.CTF_USE_COMPLEX_AS_SIMPLE);body.set_editor_property('double_sided_geometry',True)
  build=smes.get_lod_build_settings(mesh,0)
  changes={'recompute_tangents':False,'use_mikk_t_space':True,'remove_degenerates':True,'use_full_precision_u_vs':True,'max_lumen_mesh_cards':32,'generate_distance_field_as_if_two_sided':True}
  if any(build.get_editor_property(k)!=v for k,v in changes.items()):
   for k,v in changes.items():build.set_editor_property(k,v)
   smes.set_lod_build_settings(mesh,0,build)
  nanite=smes.get_nanite_settings(mesh)
  desired_nanite=not name.startswith('SM_Kvarnholmen_')
  if nanite.enabled!=desired_nanite:nanite.enabled=desired_nanite;smes.set_nanite_settings(mesh,nanite,True)
  if name=='SM_Domkyrka_Altar_Carving':
   nanite=smes.get_nanite_settings(mesh);nanite.generate_fallback=type(nanite.generate_fallback).ENABLED;nanite.fallback_relative_error=0.0;smes.set_nanite_settings(mesh,nanite,True)
  library.save_loaded_asset(mesh)
  label=name.replace('SM_','');actor=existing.get(label)
  if actor:actor.static_mesh_component.set_static_mesh(mesh)
  else:
   actor=actors.spawn_actor_from_object(mesh,u.Vector(),u.Rotator());actor.set_actor_label(label);actor.set_folder_path(spec['category']);actor.static_mesh_component.set_mobility(u.ComponentMobility.STATIC)
  if name=='SM_Kvarnholmen_Water':actor.static_mesh_component.set_collision_enabled(u.CollisionEnabled.NO_COLLISION)
  bounds=mesh.get_bounding_box();finite=all(math.isfinite(getattr(v,k)) for v in [bounds.min,bounds.max] for k in ['x','y','z'])
  report['meshes'].append({'name':name,'vertices':spec['vertices'],'polygons':spec['polygons'],'bounds_finite':finite,'nanite':bool(smes.get_nanite_settings(mesh).enabled),'expected_nanite':desired_nanite,'materials_assigned':all(mesh.get_material(i) is not None for i in range(len(mesh.static_materials)))})
  (R/'previews/kvarnholmen-refine-import.json').write_text(json.dumps(report,indent=2))
 for spec in MAN['cameras']:
  if not spec['name'].startswith(('46_','47_','48_','49_','50_','51_','52_','53_')):continue
  cam=existing.get(spec['name']) or actors.spawn_actor_from_class(u.CameraActor,vec(spec['location']),look(spec['location'],spec['target']))
  cam.set_actor_location(vec(spec['location']),False,False);cam.set_actor_rotation(look(spec['location'],spec['target']),False)
  cam.set_actor_label(spec['name']);cam.set_folder_path('Review cameras');cam.camera_component.set_field_of_view(math.degrees(2*math.atan(36/(2*spec['lens']))))
 world=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
 for name,start,end,expect in [('doorway',(1010,-2200,300),(1010,-3100,300),False),('aisle',(-800,-4440,280),(2100,-4440,280),False),('floor',(1010,-4440,300),(1010,-4440,0),True)]:
  hit=u.SystemLibrary.line_trace_single(world,u.Vector(*start),u.Vector(*end),u.TraceTypeQuery.ECC_VISIBILITY,True,[],u.DrawDebugTrace.NONE,True)
  report['checks'][name]=(hit is not None)==expect
 # Verify all board mount locations against the actual structural piers.
 ignore=[a for a in actors.get_all_level_actors() if isinstance(a,u.StaticMeshActor) and a.static_mesh_component.static_mesh and not a.static_mesh_component.static_mesh.get_name().startswith('SM_Domkyrka_Interior_Architecture')]
 report['mount_checks']=[]
 for uu in [-23,-10.6,23]:
  for side in [-1,1]:
   start=vec((10.1+uu,44.4+side*7.20,6.1));end=vec((10.1+uu,44.4+side*7.5,6.1))
   hit=u.SystemLibrary.line_trace_single(world,start,end,u.TraceTypeQuery.ECC_VISIBILITY,True,ignore,u.DrawDebugTrace.NONE,True)
   report['mount_checks'].append({'u':uu,'side':side,'pier_present':hit is not None})
 report['checks']['hymn_board_backing']=all(q['pier_present'] for q in report['mount_checks'])
 hit=u.SystemLibrary.line_trace_single(world,vec((19.80,52.3,6.4)),vec((20.1,52.3,6.4)),u.TraceTypeQuery.ECC_VISIBILITY,True,ignore,u.DrawDebugTrace.NONE,True)
 report['checks']['pulpit_pier_backing']=hit is not None
 report['checks']['mesh_integrity']=bool(report['meshes']) and all(m['bounds_finite'] and m['nanite']==m['expected_nanite'] and m['materials_assigned'] for m in report['meshes'])
 report['checks']['normal_materials']=all(m['normal_connected'] and m['roughness_connected'] and not m['normal_srgb'] and m['flip_green'] and 'NORMALMAP' in m['compression'] for m in report['materials'].values())
 level.save_current_level()
 library.save_directory(BASE+'/Materials',only_if_is_dirty=True,recursive=True)
 report['status']='passed' if all(report['checks'].values()) else 'failed'
 (R/'previews/kvarnholmen-refine-import.json').write_text(json.dumps(report,indent=2))
 if report['status']!='passed':raise RuntimeError('Exterior/fixture verification failed')

except Exception:
 report['status']='failed';report['error']=traceback.format_exc();(R/'previews/kvarnholmen-refine-import.json').write_text(json.dumps(report,indent=2));raise


import runpy
runpy.run_path(str(R/'Unreal/Content/Python/check_kvarnholmen.py'))
