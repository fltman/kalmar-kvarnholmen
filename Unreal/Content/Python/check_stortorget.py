import unreal as u,json,math
from pathlib import Path
R=Path(__file__).resolve().parents[3]
ae=u.get_editor_subsystem(u.EditorActorSubsystem);ue=u.get_editor_subsystem(u.UnrealEditorSubsystem)
world=ue.get_editor_world();actors=ae.get_all_level_actors()
report={'actor_count':len(actors),'mesh_count':sum(isinstance(a,u.StaticMeshActor) for a in actors),'trace_doc':u.SystemLibrary.line_trace_single.__doc__}
for a in actors:
 if isinstance(a,u.SkyLight):a.light_component.set_intensity(3.0);a.light_component.recapture_sky()
# Facing cathedral from south, +X to the right, -Y toward the cathedral.
loc=u.Vector(-2200,2400,200);target=u.Vector(1000,-4200,1200)
rot=u.MathLibrary.find_look_at_rotation(loc,target)
ue.set_level_viewport_camera_info(loc,rot)
report['camera']={'location':str(loc),'rotation':str(rot)}
for name,start,end in [('square_ground',u.Vector(0,0,300),u.Vector(0,0,-300)),('cathedral_wall',u.Vector(1000,0,300),u.Vector(1000,-4500,300))]:
 result=u.SystemLibrary.line_trace_single(world,start,end,u.TraceTypeQuery.TRACE_TYPE_QUERY1,False,[],u.DrawDebugTrace.NONE,True)
 report[name]=str(result)
u.get_editor_subsystem(u.LevelEditorSubsystem).save_current_level()
(R/'previews/unreal-validation.json').write_text(json.dumps(report,indent=2))
u.log('STORTORGET_VALIDATED '+str(report))
