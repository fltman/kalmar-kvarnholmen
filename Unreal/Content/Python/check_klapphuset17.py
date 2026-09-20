import unreal as u,json,math
from pathlib import Path
R=Path(__file__).resolve().parents[3];s=json.loads((R/'source/klapphuset17-shore.json').read_text());world=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world();p=s['door'];q=s['shore'];length=math.dist(p,q)
# Stop outside the closed door: no interior access is claimed in this pass.
points=[[p[0]+(q[0]-p[0])*t,p[1]+(q[1]-p[1])*t] for t in [(.9+i*(length-.9)/30)/length for i in range(31)]]
vec=lambda p,z:u.Vector(p[0]*100,-p[1]*100,z*100)
floors=[u.SystemLibrary.line_trace_single(world,vec(p,.60),vec(p,-.1),u.TraceTypeQuery.ECC_VISIBILITY,True,[],u.DrawDebugTrace.NONE,True) is not None for p in points]
obstacles=[i for i,(p,q) in enumerate(zip(points,points[1:])) if u.SystemLibrary.capsule_trace_single(world,vec(p,1.15),vec(q,1.15),34,88,u.TraceTypeQuery.ECC_VISIBILITY,True,[],u.DrawDebugTrace.NONE,True) is not None]
(R/'previews/district17-klapp-access.json').write_text(json.dumps({'status':'passed' if all(floors) and not obstacles else 'review_required','grounded':sum(floors),'samples':len(floors),'capsule_segments':30,'obstacles':obstacles,'length_m':length},indent=2))
