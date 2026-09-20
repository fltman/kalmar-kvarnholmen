"""Capture settled editor views without reopening the city for each building."""
import unreal as u,json,time,traceback
from pathlib import Path
R=Path(__file__).resolve().parents[3];ae=u.get_editor_subsystem(u.EditorActorSubsystem);ue=u.get_editor_subsystem(u.UnrealEditorSubsystem);le=u.get_editor_subsystem(u.LevelEditorSubsystem)
world=ue.get_editor_world();plan=json.loads((R/'media/houses-plan.json').read_text());items=plan['items'];folder=R/'media/houses';folder.mkdir(exist_ok=True)
settings=u.get_default_object(u.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));settings.set_editor_property('bThrottleCPUWhenNotForeground',False)
u.SystemLibrary.execute_console_command(world,'t.MaxFPS 30');u.SystemLibrary.execute_console_command(world,'r.ScreenPercentage 100')
u.EditorPythonScripting.set_keep_python_script_alive(True)
state={'index':0,'phase':'view','start':time.monotonic()};report=R/'media/houses-progress.json'
def vec(p):return u.Vector(p[0]*100,-p[1]*100,p[2]*100)
def photo_tick(dt):
 try:
  if state['index']>=len(items):
   report.write_text(json.dumps({'status':'complete','count':len(items)}));u.unregister_slate_post_tick_callback(photo_handle);return
  item=items[state['index']];path=folder/f"{item['index']:05d}.png"
  if state['phase']=='view':
   if path.exists() and path.stat().st_size>10000:state['index']+=1;return
   p=vec(item['location']);rot=u.MathLibrary.find_look_at_rotation(p,vec(item['target']));ae.clear_actor_selection_set()
   for key in le.get_viewport_config_keys():le.set_level_viewport_camera_info(p,rot,key);le.set_level_viewport_fov(item['fov'],key);le.editor_set_game_view(True,key)
   le.editor_invalidate_viewports();state.update(phase='settle',start=time.monotonic());report.write_text(json.dumps({'status':'capturing','done':state['index'],'total':len(items),'title':item['title']},ensure_ascii=False));return
  if state['phase']=='settle' and time.monotonic()-state['start']>=3.5:
   u.SystemLibrary.execute_console_command(world,'HighResShot 1600x1000 filename="'+str(path)+'"');state.update(phase='save',start=time.monotonic());return
  if state['phase']=='save':
   if time.monotonic()-state['start']>60:raise RuntimeError('Screenshot was not saved: '+str(path))
   if time.monotonic()-state['start']>1.0 and path.exists() and path.stat().st_size>10000:state['index']+=1;state['phase']='view'
 except Exception:
  report.write_text(json.dumps({'status':'error','traceback':traceback.format_exc(),'index':state['index']}));u.unregister_slate_post_tick_callback(photo_handle)
photo_handle=u.register_slate_post_tick_callback(photo_tick)
