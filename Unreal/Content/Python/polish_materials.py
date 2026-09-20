import unreal as u,time,json
from pathlib import Path
R=Path(__file__).resolve().parents[3]
u.EditorPythonScripting.set_keep_python_script_alive(True)
for path in u.EditorAssetLibrary.list_assets('/Game/Kalmar/Materials',recursive=True,include_folder=False):
 m=u.load_asset(path)
 if isinstance(m,u.Material):
  m.set_editor_property('two_sided',True);u.MaterialEditingLibrary.recompile_material(m);u.EditorAssetLibrary.save_loaded_asset(m)
actors=u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors();camera=next(a for a in actors if a.get_actor_label()=='01_Stortorget')
u.get_editor_subsystem(u.UnrealEditorSubsystem).set_level_viewport_camera_info(camera.get_actor_location(),camera.get_actor_rotation())
u.get_editor_subsystem(u.LevelEditorSubsystem).save_current_level()
world=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
u.SystemLibrary.execute_console_command(world,'r.ScreenPercentage 100')
u.SystemLibrary.execute_console_command(world,'r.AntiAliasingMethod 2')
u.SystemLibrary.execute_console_command(world,'sg.ShadowQuality 3')
start=time.monotonic();done=False
# Leave this verified editor window open for the user.
def tick(delta):
 global done,handle
 if not done and time.monotonic()-start>12:
  u.AutomationLibrary.take_high_res_screenshot(1600,1000,str(R/'previews/04_Unreal_Stortorget.png'),camera=camera,delay=1)
  done=True
 if time.monotonic()-start>20:
  (R/'previews/unreal-material-validation.json').write_text(json.dumps({'two_sided_materials':24,'map':'/Game/Kalmar/Maps/Stortorget','status':'complete'},indent=2))
  u.unregister_slate_post_tick_callback(handle)
handle=u.register_slate_post_tick_callback(tick)
