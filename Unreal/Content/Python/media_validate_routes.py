import unreal as u,json
from pathlib import Path
R=Path(__file__).resolve().parents[3];world=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world();routes=json.loads((R/'media/routes.json').read_text());report={}
def vec(p):return u.Vector(p[0]*100,-p[1]*100,p[2]*100)
for name in ['street','church']:
 frames=routes[name]['frames'];blocked=[];checks=0
 for i in range(0,len(frames)-1,6):
  a=vec(frames[i]['location']);b=vec(frames[min(i+6,len(frames)-1)]['location']);h=u.SystemLibrary.sphere_trace_single(world,a,b,22,u.TraceTypeQuery.ECC_VISIBILITY,True,[],u.DrawDebugTrace.NONE,True);checks+=1
  if h:
   actor=h.to_tuple()[9];blocked.append({'frame':i,'position':frames[i]['location'],'actor':actor.get_actor_label() if actor else None})
 report[name]={'checks':checks,'blocked':blocked,'status':'passed' if not blocked else 'needs_adjustment'}
(R/'media/routes-validation.json').write_text(json.dumps(report,indent=2))
