"""Persistent visual QA without resetting production lighting."""
import unreal as u,time,json,math,statistics,traceback
from pathlib import Path
R=Path(__file__).resolve().parents[3]
u.EditorPythonScripting.set_keep_python_script_alive(True)
ae=u.get_editor_subsystem(u.EditorActorSubsystem);ue=u.get_editor_subsystem(u.UnrealEditorSubsystem);level=u.get_editor_subsystem(u.LevelEditorSubsystem)
actors=ae.get_all_level_actors();world=ue.get_editor_world()
performance_settings=u.get_default_object(u.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'))
throttle_property='bThrottleCPUWhenNotForeground'
original_throttle=performance_settings.get_editor_property(throttle_property)
performance_settings.set_editor_property(throttle_property,False)
# Preserve the editor's realtime state. Unconditionally toggling it during
# startup triggers a missing-override ensure in UE 5.8. Native CSV checks below
# reject performance captures that do not contain actual scene rendering.
for cmd in ['r.AntiAliasingMethod 4','ShowFlag.Atmosphere 1','ShowFlag.Lighting 1']:
 u.SystemLibrary.execute_console_command(world,cmd)
smes=u.get_editor_subsystem(u.StaticMeshEditorSubsystem)
mesh_report=[]
for a in actors:
 if isinstance(a,u.StaticMeshActor):
  mesh=a.static_mesh_component.static_mesh
  if mesh and mesh.get_name().startswith(('SM_Domkyrka','SM_Kalmar_Domkyrka')):
   mesh_report.append({'name':mesh.get_name(),'nanite':bool(smes.get_nanite_settings(mesh).get_editor_property('enabled')),'lumen_cards':smes.get_lod_build_settings(mesh,0).get_editor_property('max_lumen_mesh_cards')})
vars={k:u.SystemLibrary.get_console_variable_int_value(k) for k in ['r.DynamicGlobalIlluminationMethod','r.ReflectionMethod','r.GenerateMeshDistanceFields','r.Nanite','r.Shadow.Virtual.Enable','r.AntiAliasingMethod']}
(R/'previews/hero-render-validation.json').write_text(json.dumps({'cvars':vars,'church_meshes':mesh_report,'nanite_meshes':sum(m['nanite'] for m in mesh_report),'status':'passed' if vars['r.DynamicGlobalIlluminationMethod']==1 and vars['r.ReflectionMethod']==1 and vars['r.GenerateMeshDistanceFields']==1 and all(m['nanite'] for m in mesh_report) else 'failed'},indent=2))
queue=[];index=0;state=0;start=time.monotonic();stamp=None;perf=None;samples=[]
def view(name):
 cam=next(a for a in actors if a.get_actor_label()==name);ae.clear_actor_selection_set()
 for key in level.get_viewport_config_keys():
  level.set_level_viewport_camera_info(cam.get_actor_location(),cam.get_actor_rotation(),key);level.set_level_viewport_fov(cam.camera_component.field_of_view,key);level.editor_set_game_view(True,key)
 level.editor_invalidate_viewports()
def tick(dt):
 global queue,index,state,start,stamp,handle,perf,samples,actors,world
 try:
  request=R/'previews/hero-review-request.json'
  if request.exists() and request.stat().st_mtime!=stamp:
   stamp=request.stat().st_mtime;d=json.loads(request.read_text())
   if d.get('relight'):
    exec(compile((R/'Unreal/Content/Python/configure_hero_scene.py').read_text(),str(R/'Unreal/Content/Python/configure_hero_scene.py'),'exec'),globals());actors=ae.get_all_level_actors()
   if 'bias' in d:
    for a in actors:
     if isinstance(a,u.PostProcessVolume):s=a.settings;s.auto_exposure_bias=d['bias'];a.settings=s
   if 'screen' in d:u.SystemLibrary.execute_console_command(world,'r.ScreenPercentage '+str(d['screen']))
   if 'window_lumens' in d:
    for a in actors:
     if isinstance(a,u.RectLight):a.light_component.set_intensity(d['window_lumens'])
   if 'view' in d:view(d['view'])
   if d.get('execute'):
    folder=R/'Unreal/Content/Python';path=(folder/d['execute']).resolve()
    if path.parent!=folder.resolve():raise ValueError('Review script must belong to this project')
    try:
     exec(compile(path.read_text(),str(path),'exec'),{'__file__':str(path)})
     error_path=R/'previews/hero-review-command-error.txt'
     if error_path.exists():error_path.unlink()
    except Exception:
     (R/'previews/hero-review-command-error.txt').write_text(traceback.format_exc())
     queue=[];index=0
     return
    actors=ae.get_all_level_actors();world=ue.get_editor_world()
   if d.get('surface_repair'):
    path=R/'Unreal/Content/Python/repair_exterior_uv.py'
    exec(compile(path.read_text(),str(path),'exec'),{'__file__':str(path)})
   if d.get('fixture_validation'):
    path=R/'Unreal/Content/Python/validate_fixtures.py'
    exec(compile(path.read_text(),str(path),'exec'),{'__file__':str(path)})
   if d.get('walk_test'):
    walk_script=R/'Unreal/Content/Python/validate_joinery_walk.py'
    exec(compile(walk_script.read_text(),str(walk_script),'exec'),{'__file__':str(walk_script)})
   if d.get('performance'):
    perf=time.monotonic();samples=[];u.SystemLibrary.execute_console_command(world,'csvprofile start')
   if 'shots' in d:queue=d['shots'];index=0;state=0;start=time.monotonic()
   if d.get('finish'):
    level.save_current_level();performance_settings.set_editor_property(throttle_property,original_throttle);u.unregister_slate_post_tick_callback(handle)
    if d.get('quit'):u.SystemLibrary.quit_editor()
    return
   level.save_current_level()
  if perf:
   elapsed=time.monotonic()-perf
   if elapsed>8:samples.append({'dt_ms':dt*1000,'engine_frame_ms':0})
   if elapsed>30:
    u.SystemLibrary.execute_console_command(world,'csvprofile stop')
    vals=[x['dt_ms'] for x in samples if x['dt_ms']>0];eng=[x['engine_frame_ms'] for x in samples if x['engine_frame_ms']>0]
    (R/'previews/hero-editor-performance.json').write_text(json.dumps({'context':'Editor viewport, stationary camera, background CPU throttle temporarily disabled; not a packaged gameplay benchmark','samples':len(vals),'slate_frame_median_ms':statistics.median(vals) if vals else None,'slate_frame_p95_ms':sorted(vals)[int(.95*(len(vals)-1))] if vals else None,'engine_frame_median_ms':statistics.median(eng) if eng else None},indent=2));perf=None
  if index<len(queue) and time.monotonic()-start>12:
   name,filename=queue[index]
   if state==0:view(name);state=1;start=time.monotonic()
   else:
    u.SystemLibrary.execute_console_command(world,'HighResShot 1600x1000 filename="'+str(R/'previews'/filename)+'"');index+=1;state=0;start=time.monotonic()
 except Exception:
  (R/'previews/hero-review-error.txt').write_text(traceback.format_exc())
  performance_settings.set_editor_property(throttle_property,original_throttle)
  u.unregister_slate_post_tick_callback(handle)
handle=u.register_slate_post_tick_callback(tick)
initial={'view':'05_Interiör_Altare'} if '-HeroIdle' in u.SystemLibrary.get_command_line() else ({'view':'05_Interiör_Altare','performance':True} if '-HeroPerformance' in u.SystemLibrary.get_command_line() else {'shots':[['05_Interiör_Altare','23_Hero_Interior.png'],['10_Orgel_Läktare','24_Hero_Organ.png'],['12_Altarskulptur','25_Hero_Sculpture.png'],['13_Predikstol','26_Hero_Pulpit.png'],['04_Domkyrkan','27_Hero_Exterior.png']]})
(R/'previews/hero-review-request.json').write_text(json.dumps(initial))
