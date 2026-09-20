"""Actual Unreal collision and PIE walking checks; capture real editor views."""
import unreal as u,time,json,traceback,math
from pathlib import Path
R=Path(__file__).resolve().parents[3]
u.EditorPythonScripting.set_keep_python_script_alive(True)
ae=u.get_editor_subsystem(u.EditorActorSubsystem);ue=u.get_editor_subsystem(u.UnrealEditorSubsystem);level=u.get_editor_subsystem(u.LevelEditorSubsystem)
world=ue.get_editor_world();actors=ae.get_all_level_actors()
organ_cam=next(a for a in actors if a.get_actor_label()=='06_Interiör_Orgel')
organ_loc=u.Vector(2000,-4440,310);organ_cam.set_actor_location(organ_loc,False,False);organ_cam.set_actor_rotation(u.MathLibrary.find_look_at_rotation(organ_loc,u.Vector(-1200,-4440,1000)),False)
report={'status':'running','mesh_count':sum(isinstance(a,u.StaticMeshActor) for a in actors)}
def vec(x,y,z):return u.Vector(x*100,-y*100,z*100)
def trace(a,b):return u.SystemLibrary.line_trace_single(world,vec(*a),vec(*b),u.TraceTypeQuery.TRACE_TYPE_QUERY1,True,[],u.DrawDebugTrace.NONE,True)
report['doorway_clear']=trace((10.1,22,3),(10.1,31,3)) is None
report['central_aisle_clear']=trace((-8,44.4,2.8),(21,44.4,2.8)) is None
report['floor_hit']=trace((10.1,44.4,3),(10.1,44.4,0)) is not None
report['vault_hit']=trace((10.1,44.4,2),(10.1,44.4,26)) is not None
report['two_sided_materials']=all(u.load_asset(p).get_editor_property('two_sided') for p in u.EditorAssetLibrary.list_assets('/Game/Kalmar/Materials',recursive=True,include_folder=False))
start=time.monotonic();stage=0;walk_time=0
# Begin immediately outside the steps, then walk through the actual open portal.
playerstart=next(a for a in actors if isinstance(a,u.PlayerStart));oldloc=playerstart.get_actor_location();oldrot=playerstart.get_actor_rotation()
playerstart.set_actor_location(vec(10.1,21.7,1.1),False,False);playerstart.set_actor_rotation(u.Rotator(0,-90,0),False)
shots=[('07_Stadshotellet','08_Unreal_Stadshotellet.png'),('05_Interiör_Altare','09_Unreal_Interior.png'),('06_Interiör_Orgel','10_Unreal_Organ.png')]
def write(): (R/'previews/unreal-interior-validation.json').write_text(json.dumps(report,indent=2))
def camera(name):return next(a for a in actors if a.get_actor_label()==name)
def shot(name,filename):
 cam=camera(name);ue.set_level_viewport_camera_info(cam.get_actor_location(),cam.get_actor_rotation())
 # HighResShot directly targets the editor viewport, also when the window is unfocused.
 u.SystemLibrary.execute_console_command(world,'HighResShot 1600x1000 filename="'+str(R/'previews'/filename)+'"')
def finish():
 playerstart.set_actor_location(oldloc,False,False);playerstart.set_actor_rotation(oldrot,False)
 level.save_current_level();write();u.unregister_slate_post_tick_callback(handle)
 # Auto-exit this validation instance so the user can open a fresh editor.
 u.EditorPythonScripting.set_keep_python_script_alive(False)
def tick(delta):
 global stage,walk_time,handle
 try:
  elapsed=time.monotonic()-start
  if stage==0 and elapsed>7:level.editor_request_begin_play();stage=1
  elif stage==1:
   gw=ue.get_game_world()
   if gw and u.GameplayStatics.get_player_pawn(gw,0):walk_time=time.monotonic();stage=2
  elif stage==2:
   gw=ue.get_game_world();pawn=u.GameplayStatics.get_player_pawn(gw,0)
   if time.monotonic()-walk_time<4.5:pawn.add_movement_input(u.Vector(0,-1,0),1,False)
   else:
    pos=pawn.get_actor_location();report['entrance_end_cm']=[pos.x,pos.y,pos.z];report['entered_from_square']=pos.y<-3100 and 200<pos.z<260
    pawn.set_actor_location(vec(-8,44.4,2.4),False,True);walk_time=time.monotonic();stage=3
  elif stage==3:
   gw=ue.get_game_world();pawn=u.GameplayStatics.get_player_pawn(gw,0)
   if time.monotonic()-walk_time<3:pawn.add_movement_input(u.Vector(1,0,0),1,False)
   else:
    pos=pawn.get_actor_location();report['aisle_end_cm']=[pos.x,pos.y,pos.z];report['walked_aisle']=pos.x>0 and 200<pos.z<260
    level.editor_request_end_play();stage=4;walk_time=time.monotonic()
  elif stage>=4 and stage<=6 and time.monotonic()-walk_time>4:
   name,filename=shots[stage-4];shot(name,filename);walk_time=time.monotonic();stage+=1
  elif stage==7 and time.monotonic()-walk_time>5:
   report['status']='passed' if all(report.get(k) for k in ['doorway_clear','central_aisle_clear','floor_hit','vault_hit','two_sided_materials','entered_from_square','walked_aisle']) else 'failed';finish();stage=8
  if elapsed>90 and stage<8:report['status']='timeout';finish();stage=8
 except Exception:
  report['status']='failed';report['error']=traceback.format_exc();finish();stage=8
handle=u.register_slate_post_tick_callback(tick)
write()
