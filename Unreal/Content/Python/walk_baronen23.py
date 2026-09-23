"""Actual PIE traversal from the Baronen entrance plaza round Packhuset and along the whole quay."""
import unreal as u,time,json,traceback,math
from pathlib import Path
R=Path(__file__).resolve().parents[3];route=json.loads((R/'source/baronen23-walk.json').read_text())
ae=u.get_editor_subsystem(u.EditorActorSubsystem);ue=u.get_editor_subsystem(u.UnrealEditorSubsystem);level=u.get_editor_subsystem(u.LevelEditorSubsystem)
start_actor=next(a for a in ae.get_all_level_actors() if isinstance(a,u.PlayerStart));old_loc=start_actor.get_actor_location();old_rot=start_actor.get_actor_rotation()
points=[u.Vector(p[0]*100,-p[1]*100,110) for p in route['points']];start_actor.set_actor_location(points[0],False,False)
first=points[1]-points[0];start_actor.set_actor_rotation(u.Rotator(0,math.degrees(math.atan2(first.y,first.x)),0),False)
report={'status':'running','route_length_m':route['length_m'],'scope':'Actual PIE character movement; no teleport during the route; original PlayerStart restored.','samples':[]};stage=0;index=1;begin=time.monotonic();last_sample=0;last_progress=begin;best=float('inf')
def write():(R/'previews/baronen23-pie-walk.json').write_text(json.dumps(report,indent=2))
def finish():
 start_actor.set_actor_location(old_loc,False,False);start_actor.set_actor_rotation(old_rot,False);level.save_current_level();write();u.unregister_slate_post_tick_callback(walk_handle)
def tick(dt):
 global stage,index,last_sample,last_progress,best,end_time
 try:
  now=time.monotonic()
  if stage==0 and now-begin>2:level.editor_request_begin_play();stage=1
  elif stage==1:
   game=ue.get_game_world()
   if game and u.GameplayStatics.get_player_pawn(game,0):last_progress=now;stage=2
  elif stage==2:
   pawn=u.GameplayStatics.get_player_pawn(ue.get_game_world(),0);pos=pawn.get_actor_location();goal=points[index];dx,dy=goal.x-pos.x,goal.y-pos.y;distance=math.hypot(dx,dy)
   if distance<95:
    index+=1;best=float('inf');last_progress=now
    if index>=len(points):report['status']='passed';report['end_cm']=[pos.x,pos.y,pos.z];level.editor_request_end_play();end_time=now;stage=3
   else:
    pawn.add_movement_input(u.Vector(dx/distance,dy/distance,0),1,False)
    if distance<best-35:best=distance;last_progress=now
   if now-last_sample>2:report['samples'].append({'point_cm':[round(pos.x,1),round(pos.y,1),round(pos.z,1)],'target':index});last_sample=now;write()
   if stage==2 and (pos.z< -100 or now-last_progress>18):
    report['status']='failed';report['end_cm']=[pos.x,pos.y,pos.z];report['target']=index;level.editor_request_end_play();end_time=now;stage=3
  elif stage==3 and now-end_time>3:stage=4;finish()
  if now-begin>240 and stage<3:report['status']='timeout';level.editor_request_end_play();end_time=now;stage=3
 except Exception:
  report['status']='failed';report['error']=traceback.format_exc();stage=4;level.editor_request_end_play();finish()
walk_handle=u.register_slate_post_tick_callback(tick);write()
