"""Replace the complete pending house inventory; preserve other world assets."""
import unreal as u,json,ast,math,traceback,time
from pathlib import Path
ROOT=R=Path(__file__).resolve().parents[3];BASE='/Game/Kalmar'
MAN=json.loads((R/'exports/manifest.json').read_text())
assets=u.AssetToolsHelpers.get_asset_tools();library=u.EditorAssetLibrary
actors=u.get_editor_subsystem(u.EditorActorSubsystem);level=u.get_editor_subsystem(u.LevelEditorSubsystem);smes=u.get_editor_subsystem(u.StaticMeshEditorSubsystem)
tree=ast.parse((R/'Unreal/Content/Python/build_stortorget.py').read_text());tree.body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in {'import_task','vec','look'}];exec(compile(tree,'district17_import_helpers','exec'))
names=json.loads((R/'previews/district17-build.json').read_text())['changed']
names=globals().get('district17_import_only',names)
report_file=globals().get('district17_import_report','district17-import.json')
report={'status':'importing','time':time.time(),'meshes':[]}
previous=R/'previews'/report_file
if previous.exists():
 old_report=json.loads(previous.read_text());done={q['name'] for q in old_report.get('meshes',[]) if q.get('materials_assigned') and q.get('nanite') and q.get('bounds_finite')}
 report['meshes']=[q for q in old_report.get('meshes',[]) if q['name'] in done and q['name'] in names]
else:done=set()
try:
 existing={a.get_actor_label():a for a in actors.get_all_level_actors()}
 for spec in MAN['assets']:
  name=spec['name']
  if name not in names or name in done:continue
  u.log('DISTRICT17_IMPORT '+name)
  opt=u.FbxImportUI();opt.import_mesh=True;opt.import_as_skeletal=False;opt.import_materials=False;opt.import_textures=False;opt.mesh_type_to_import=u.FBXImportType.FBXIT_STATIC_MESH;opt.automated_import_should_detect_type=False
  data=opt.static_mesh_import_data;data.combine_meshes=True;data.auto_generate_collision=False;data.generate_lightmap_u_vs=False;data.convert_scene=True;data.convert_scene_unit=True;data.force_front_x_axis=False;data.normal_import_method=u.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS_AND_TANGENTS
  mesh=import_task(R/'exports'/spec['file'],BASE+'/Meshes',name,opt)
  if not isinstance(mesh,u.StaticMesh):raise RuntimeError('Missing imported mesh '+name)
  slots=list(mesh.static_materials);slots_changed=False
  for i,slot in enumerate(slots):
   mat_name=str(slot.get_editor_property('imported_material_slot_name'))
   mat_name=spec.get('material_overrides',{}).get(mat_name,mat_name)
   ma=u.load_asset(BASE+'/Materials/'+mat_name)
   if not ma:raise RuntimeError('Missing material '+mat_name)
   if slot.get_editor_property('material_interface')!=ma:slot.set_editor_property('material_interface',ma);slots_changed=True
  if slots_changed:mesh.set_editor_property('static_materials',slots)
  body=mesh.get_editor_property('body_setup');body.set_editor_property('collision_trace_flag',u.CollisionTraceFlag.CTF_USE_COMPLEX_AS_SIMPLE);body.set_editor_property('double_sided_geometry',True)
  build=smes.get_lod_build_settings(mesh,0)
  changed_build=False
  for k,v in {'recompute_normals':False,'recompute_tangents':False,'remove_degenerates':True,'use_full_precision_u_vs':True,'max_lumen_mesh_cards':32,'generate_distance_field_as_if_two_sided':True}.items():
   if build.get_editor_property(k)!=v:build.set_editor_property(k,v);changed_build=True
  if changed_build:smes.set_lod_build_settings(mesh,0,build)
  n=smes.get_nanite_settings(mesh);needs_nanite=not n.enabled or not n.explicit_tangents or n.fallback_relative_error!=0 or n.generate_fallback!=type(n.generate_fallback).ENABLED
  n.enabled=True;n.explicit_tangents=True;n.generate_fallback=type(n.generate_fallback).ENABLED;n.fallback_target=type(n.fallback_target).RELATIVE_ERROR;n.fallback_relative_error=0
  if needs_nanite:smes.set_nanite_settings(mesh,n,True)
  library.save_loaded_asset(mesh)
  actor=existing.get(name.removeprefix('SM_'))
  if not actor:raise RuntimeError('Expected existing actor '+name)
  actor.static_mesh_component.set_static_mesh(mesh)
  bb=mesh.get_bounding_box()
  report['meshes'].append({'name':name,'nanite':bool(n.enabled),'materials_assigned':all(mesh.get_material(i) for i in range(len(mesh.static_materials))),'bounds_finite':all(math.isfinite(getattr(v,k)) for v in [bb.min,bb.max] for k in ['x','y','z'])})
  (R/'previews'/report_file).write_text(json.dumps(report,indent=2))
 for s in MAN['cameras']:
  if not s['name'].startswith(('71_','72_','73_','74_','75_','76_','77_')):continue
  cam=existing.get(s['name']) or actors.spawn_actor_from_class(u.CameraActor,vec(s['location']),look(s['location'],s['target']))
  cam.set_actor_label(s['name']);cam.set_folder_path('Review cameras');cam.set_actor_location(vec(s['location']),False,False);cam.set_actor_rotation(look(s['location'],s['target']),False);cam.camera_component.set_field_of_view(math.degrees(2*math.atan(36/(2*s['lens']))))
 level.save_current_level()
 assert len(report['meshes'])==len(names)
 assert all(v['nanite'] and v['materials_assigned'] and v['bounds_finite'] for v in report['meshes'])
 report['status']='passed'
except Exception:
 report['status']='failed';report['error']=traceback.format_exc();raise
finally:(R/'previews'/report_file).write_text(json.dumps(report,indent=2))
u.log('DISTRICT17_IMPORT_DONE')
