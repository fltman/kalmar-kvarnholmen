"""PIE regression check after changing pew collision geometry; no lighting edits."""
import unreal as u,time,json,traceback
from pathlib import Path
R=Path(__file__).resolve().parents[3]
ae=u.get_editor_subsystem(u.EditorActorSubsystem);ue=u.get_editor_subsystem(u.UnrealEditorSubsystem);level=u.get_editor_subsystem(u.LevelEditorSubsystem)
start_actor=next(a for a in ae.get_all_level_actors() if isinstance(a,u.PlayerStart))
old_location=start_actor.get_actor_location();old_rotation=start_actor.get_actor_rotation()
start_actor.set_actor_location(u.Vector(1010,-2170,110),False,False);start_actor.set_actor_rotation(u.Rotator(0,-90,0),False)
report={'status':'running','scope':'Actual character movement in PIE through the south entrance and along the centre aisle; aisle start repositioned between the two checks'}
begin=time.monotonic();stage=0;walk_start=0
def write(): (R/'previews/joinery-pie-walk.json').write_text(json.dumps(report,indent=2))
def finish():
 start_actor.set_actor_location(old_location,False,False);start_actor.set_actor_rotation(old_rotation,False)
 level.save_current_level();write();u.unregister_slate_post_tick_callback(walk_handle)
def walk_tick(delta):
 global stage,walk_start
 try:
  if stage==0 and time.monotonic()-begin>3:level.editor_request_begin_play();stage=1
  elif stage==1:
   game=ue.get_game_world()
   if game and u.GameplayStatics.get_player_pawn(game,0):walk_start=time.monotonic();stage=2
  elif stage in (2,3):
   pawn=u.GameplayStatics.get_player_pawn(ue.get_game_world(),0)
   seconds=4.5 if stage==2 else 3.0
   if time.monotonic()-walk_start<seconds:pawn.add_movement_input(u.Vector(0,-1,0) if stage==2 else u.Vector(1,0,0),1,False)
   else:
    pos=pawn.get_actor_location()
    if stage==2:
     report['entrance_end_cm']=[pos.x,pos.y,pos.z];report['entered_from_square']=pos.y<-3100 and 200<pos.z<260
     pawn.set_actor_location(u.Vector(-800,-4440,240),False,True);walk_start=time.monotonic();stage=3
    else:
     report['aisle_end_cm']=[pos.x,pos.y,pos.z];report['walked_aisle']=pos.x>0 and 200<pos.z<260
     level.editor_request_end_play();walk_start=time.monotonic();stage=4
  elif stage==4 and time.monotonic()-walk_start>3:
   report['status']='passed' if report.get('entered_from_square') and report.get('walked_aisle') else 'failed';stage=5;finish()
  if time.monotonic()-begin>70 and stage<5:
   level.editor_request_end_play();report['status']='timeout';stage=5;finish()
 except Exception:
  report['status']='failed';report['error']=traceback.format_exc();stage=5
  level.editor_request_end_play();finish()
walk_handle=u.register_slate_post_tick_callback(walk_tick)
write()
