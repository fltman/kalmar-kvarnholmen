import unreal as u,time,json
from pathlib import Path
R=Path(__file__).resolve().parents[3]
u.EditorPythonScripting.set_keep_python_script_alive(True)
ae=u.get_editor_subsystem(u.EditorActorSubsystem);ue=u.get_editor_subsystem(u.UnrealEditorSubsystem);level=u.get_editor_subsystem(u.LevelEditorSubsystem)
actors=ae.get_all_level_actors();world=ue.get_editor_world();report=[]
for a in actors:
 label=a.get_actor_label()
 if isinstance(a,u.DirectionalLight):
  fill='fill' in label
  a.set_actor_rotation(u.Rotator(pitch=-60 if fill else -38,yaw=135 if fill else -45,roll=0),False)
  a.light_component.set_intensity(.65 if fill else 4.0)
  a.light_component.set_editor_property('atmosphere_sun_light',not fill)
  report.append({'label':label,'rotation':str(a.get_actor_rotation()),'direction':str(a.get_actor_forward_vector())})
 if isinstance(a,u.PointLight):
  a.light_component.set_intensity(80 if 'ambient' in label else 35)
  report.append({'label':label,'units':str(a.light_component.get_editor_property('intensity_units')),'intensity':a.light_component.intensity})
 if isinstance(a,u.SkyLight):a.light_component.recapture_sky()
for cmd in ['r.ScreenPercentage 100','r.AntiAliasingMethod 2','r.SkyAtmosphere 1','ShowFlag.Atmosphere 1','ShowFlag.Lighting 1']:
 u.SystemLibrary.execute_console_command(world,cmd)
level.save_current_level()
(R/'previews/unreal-lighting-report.json').write_text(json.dumps(report,indent=2))
queue=[('07_Stadshotellet','08_Unreal_Stadshotellet.png'),('05_Interiör_Altare','09_Unreal_Interior.png'),('06_Interiör_Orgel','10_Unreal_Organ.png'),('01_Stortorget','04_Unreal_Stortorget.png')]
start=time.monotonic();index=0;state=0;stamp=None
# A small local review queue permits adjusting the same editor without relaunch.
def view(name):
 cam=next(a for a in actors if a.get_actor_label()==name)
 ae.clear_actor_selection_set()
 for key in level.get_viewport_config_keys():
  level.set_level_viewport_camera_info(cam.get_actor_location(),cam.get_actor_rotation(),key)
  level.set_level_viewport_fov(cam.camera_component.field_of_view,key)
  level.editor_set_game_view(True,key)
 level.editor_invalidate_viewports()
def tick(dt):
 global start,index,state,stamp,queue,handle
 request=R/'previews/review-request.json'
 if request.exists() and request.stat().st_mtime!=stamp:
  stamp=request.stat().st_mtime;data=json.loads(request.read_text())
  if 'ambient' in data:
   for a in actors:
    if isinstance(a,u.PointLight):a.light_component.set_intensity(data['ambient'] if 'ambient' in a.get_actor_label() else data.get('window',data['ambient']/2))
   level.save_current_level()
  if 'shots' in data:queue=data['shots'];index=0;state=0;start=time.monotonic()
  if data.get('finish'):
   level.save_current_level();u.unregister_slate_post_tick_callback(handle);return
 if index<len(queue) and time.monotonic()-start>5:
  name,filename=queue[index]
  if state==0:view(name);start=time.monotonic();state=1
  else:
   u.SystemLibrary.execute_console_command(world,'HighResShot 1600x1000 filename="'+str(R/'previews'/filename)+'"')
   index+=1;state=0;start=time.monotonic()
handle=u.register_slate_post_tick_callback(tick)
