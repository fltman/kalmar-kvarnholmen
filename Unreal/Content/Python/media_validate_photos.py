"""Check camera body clearance; visual QA remains necessary for occlusion."""
import unreal as u,json
from pathlib import Path
R=Path(__file__).resolve().parents[3];world=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world();plan=json.loads((R/'media/houses-plan.json').read_text());blocked=[]
for item in plan['items']:
 p=item['location'];a=u.Vector(p[0]*100,-p[1]*100,p[2]*100);b=a+u.Vector(0,0,1)
 h=u.SystemLibrary.sphere_trace_single(world,a,b,30,u.TraceTypeQuery.ECC_VISIBILITY,True,[],u.DrawDebugTrace.NONE,True)
 if h:
  actor=h.to_tuple()[9];blocked.append({'index':item['index'],'title':item['title'],'actor':actor.get_actor_label() if actor else None})
(R/'media/photo-clearance.json').write_text(json.dumps({'checks':len(plan['items']),'blocked':blocked},indent=2,ensure_ascii=False))
