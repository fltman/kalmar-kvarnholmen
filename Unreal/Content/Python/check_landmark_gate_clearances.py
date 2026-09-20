import unreal as u,json,math
from pathlib import Path
R=Path(__file__).resolve().parents[3];D=json.loads((R/'source/landmarks14.json').read_text());world=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world();result=[]
def vec(x,y,z):return u.Vector(100*x,-100*y,100*z)
for g in D['gates']:
 for offset in [-.85,0,.85]:
  x=g['x']+math.cos(g['a'])*offset;y=g['y']+math.sin(g['a'])*offset;d=g['depth']/2+2
  p=vec(x+math.sin(g['a'])*d,y-math.cos(g['a'])*d,1.05);q=vec(x-math.sin(g['a'])*d,y+math.cos(g['a'])*d,1.05)
  hit=u.SystemLibrary.capsule_trace_single(world,p,q,34,88,u.TraceTypeQuery.ECC_VISIBILITY,True,[],u.DrawDebugTrace.NONE,True)
  floor=u.SystemLibrary.line_trace_single(world,vec(x,y,.65),vec(x,y,-.55),u.TraceTypeQuery.ECC_VISIBILITY,True,[],u.DrawDebugTrace.NONE,True)
  result.append({'gate':g['name'],'offset':offset,'capsule_clear':hit is None,'floor_present':floor is not None})
(R/'previews/landmarks14-gates.json').write_text(json.dumps({'status':'passed' if all(c['capsule_clear'] and c['floor_present'] for c in result) else 'review_required','checks':result},indent=2))
