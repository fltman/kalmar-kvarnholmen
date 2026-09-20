"""Drive the actual player pawn from the existing square to Larmtorget in PIE."""
import unreal as u,time,json,traceback
from pathlib import Path
R=Path(__file__).resolve().parents[3]
ae=u.get_editor_subsystem(u.EditorActorSubsystem);ue=u.get_editor_subsystem(u.UnrealEditorSubsystem);level=u.get_editor_subsystem(u.LevelEditorSubsystem)
start_actor=next(a for a in ae.get_all_level_actors() if isinstance(a,u.PlayerStart))
old_location=start_actor.get_actor_location();old_rotation=start_actor.get_actor_rotation()
start_actor.set_actor_location(u.Vector(-3600,280,110),False,False);start_actor.set_actor_rotation(u.Rotator(0,180,0),False)
report={'status':'running','scope':'Actual PIE character movement from Stortorget along Storgatan to Larmtorget, no teleports during the traversal. Original PlayerStart restored afterward.','samples':[]}
begin=time.monotonic();stage=0;last_sample=0;last_progress=0;best_x=-3600
def write():(R/'previews/storgatan-pie-walk.json').write_text(json.dumps(report,indent=2))
def finish():
 start_actor.set_actor_location(old_location,False,False);start_actor.set_actor_rotation(old_rotation,False)
 level.save_current_level();write();u.unregister_slate_post_tick_callback(walk_handle)
def walk_tick(delta):
 global stage,last_sample,last_progress,best_x,end_time
 try:
  now=time.monotonic()
  if stage==0 and now-begin>2:level.editor_request_begin_play();stage=1
  elif stage==1:
   game=ue.get_game_world()
   if game and u.GameplayStatics.get_player_pawn(game,0):last_progress=now;stage=2
  elif stage==2:
   pawn=u.GameplayStatics.get_player_pawn(ue.get_game_world(),0);pos=pawn.get_actor_location()
   pawn.add_movement_input(u.Vector(-1,0,0),1,False)
   if pos.x<best_x-50:best_x=pos.x;last_progress=now
   if now-last_sample>3:
    report['samples'].append([round(pos.x,1),round(pos.y,1),round(pos.z,1)]);last_sample=now;write()
   if pos.x<=-30500 or pos.z< -100 or now-last_progress>15:
    report['end_cm']=[pos.x,pos.y,pos.z];report['status']='passed' if pos.x<=-30500 and 50<pos.z<180 else 'failed'
    level.editor_request_end_play();end_time=now;stage=3
  elif stage==3 and now-end_time>3:stage=4;finish()
  if now-begin>180 and stage<3:
   report['status']='timeout';level.editor_request_end_play();end_time=now;stage=3
 except Exception:
  report['status']='failed';report['error']=traceback.format_exc();stage=4;level.editor_request_end_play();finish()
walk_handle=u.register_slate_post_tick_callback(walk_tick);write()
