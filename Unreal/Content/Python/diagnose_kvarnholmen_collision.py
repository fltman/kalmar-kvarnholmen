import unreal as u,json
from pathlib import Path
R=Path(__file__).resolve().parents[3];ae=u.get_editor_subsystem(u.EditorActorSubsystem);world=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world();actors=[a for a in ae.get_all_level_actors() if isinstance(a,u.StaticMeshActor)]
report=json.loads((R/'previews/kvarnholmen-collision.json').read_text());out=[]
for item in report['obstructions']:
 p,q=item['from'],item['to'];hits=[]
 for actor in actors:
  c,e=actor.get_actor_bounds(False)
  if c.x+e.x<min(p[0],q[0])*100-100 or c.x-e.x>max(p[0],q[0])*100+100 or c.y+e.y<min(-p[1],-q[1])*100-100 or c.y-e.y>max(-p[1],-q[1])*100+100:continue
  ignore=[a for a in actors if a!=actor]
  hit=u.SystemLibrary.capsule_trace_single(world,u.Vector(p[0]*100,-p[1]*100,105),u.Vector(q[0]*100,-q[1]*100,105),34,88,u.TraceTypeQuery.ECC_VISIBILITY,True,ignore,u.DrawDebugTrace.NONE,True)
  if hit is not None:hits.append(actor.get_actor_label())
 out.append(dict(street=item['street'],actors=hits))
(R/'previews/kvarnholmen-obstacle-diagnosis.json').write_text(json.dumps(out,indent=2))
