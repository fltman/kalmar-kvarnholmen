import unreal as u,json,traceback,time
from pathlib import Path
R=Path(__file__).resolve().parents[3]
u.EditorPythonScripting.set_keep_python_script_alive(True)
ae=u.get_editor_subsystem(u.EditorActorSubsystem);ue=u.get_editor_subsystem(u.UnrealEditorSubsystem);level=u.get_editor_subsystem(u.LevelEditorSubsystem)
world=ue.get_editor_world();allactors=ae.get_all_level_actors()
report={'mesh_count':sum(isinstance(a,u.StaticMeshActor) for a in allactors),'status':'running'}
for a in allactors:
 if isinstance(a,u.SkyLight):a.light_component.set_intensity(3);a.light_component.recapture_sky()
 if isinstance(a,u.DirectionalLight):
  a.set_actor_rotation(u.Rotator(pitch=-38,yaw=135,roll=0),False);a.light_component.set_intensity(4)
  report['sun_direction']=str(a.get_actor_forward_vector())
# A soft non-shadowing fill keeps the POC readable on this Mac without baked GI.
fill=next((a for a in allactors if a.get_actor_label()=='Soft sky fill'),None)
if not fill:fill=ae.spawn_actor_from_class(u.DirectionalLight,u.Vector(0,0,5000),u.Rotator(pitch=-60,yaw=-45,roll=0));fill.set_actor_label('Soft sky fill')
fill.light_component.set_mobility(u.ComponentMobility.MOVABLE);fill.light_component.set_intensity(.65);fill.light_component.set_editor_property('cast_shadows',False)
loc=u.Vector(-2200,2400,200);target=u.Vector(1000,-4200,1200);rot=u.MathLibrary.find_look_at_rotation(loc,target);ue.set_level_viewport_camera_info(loc,rot)
for name,start,end in [('ground',u.Vector(0,0,300),u.Vector(0,0,-300)),('wall',u.Vector(1000,0,300),u.Vector(1000,-4500,300))]:
 hit=u.SystemLibrary.line_trace_single(world,start,end,u.TraceTypeQuery.TRACE_TYPE_QUERY1,False,[],u.DrawDebugTrace.NONE,True)
 report[name]=str(hit)
 report[name+'_hit']=hit is not None
level.save_current_level()
# Save an actual Unreal viewport render, then exercise the playable character.
start_time=time.monotonic();stage=0;move_start=None;first=None
camera=next(a for a in allactors if a.get_actor_label()=='01_Stortorget')
def write(): (R/'previews/unreal-runtime-validation.json').write_text(json.dumps(report,indent=2))
def tick(delta):
 global stage,move_start,first,handle
 try:
  elapsed=time.monotonic()-start_time
  if stage==0 and elapsed>8:
   u.AutomationLibrary.take_high_res_screenshot(1600,1000,str(R/'previews/04_Unreal_Stortorget.png'),camera=camera,delay=1)
   stage=1
  elif stage==1 and elapsed>14:
   level.editor_request_begin_play();stage=2
  elif stage==2:
   gw=ue.get_game_world()
   if gw:
    pawn=u.GameplayStatics.get_player_pawn(gw,0)
    if pawn:
     move_start=time.monotonic();first=pawn.get_actor_location();report['pawn_class']=pawn.get_class().get_name();report['start_position']=[first.x,first.y,first.z];stage=3
  elif stage==3:
   gw=ue.get_game_world();pawn=u.GameplayStatics.get_player_pawn(gw,0)
   if time.monotonic()-move_start<2.0:
    pawn.add_movement_input(u.Vector(0,-1,0),1.0,False)
   else:
    last=pawn.get_actor_location();distance=math.sqrt((last.x-first.x)**2+(last.y-first.y)**2)
    report['end_position']=[last.x,last.y,last.z];report['walk_distance_cm']=distance;report['walk_passed']=distance>200 and 70<last.z<160
    level.editor_request_end_play();stage=4
  elif stage==4 and elapsed>20:
   report['status']='passed' if report.get('walk_passed') and report['ground_hit'] and report['wall_hit'] else 'failed'
   write();u.unregister_slate_post_tick_callback(handle);u.EditorPythonScripting.set_keep_python_script_alive(False)
  if elapsed>60:
   report['status']='timeout';write();u.unregister_slate_post_tick_callback(handle);u.EditorPythonScripting.set_keep_python_script_alive(False)
 except Exception:
  report['status']='failed';report['error']=traceback.format_exc();write();u.unregister_slate_post_tick_callback(handle);u.EditorPythonScripting.set_keep_python_script_alive(False)
import math
handle=u.register_slate_post_tick_callback(tick)
write()
