import unreal as u,json
from pathlib import Path
R=Path(__file__).resolve().parents[3];world=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world();ae=u.get_editor_subsystem(u.EditorActorSubsystem);allactors=list(ae.get_all_level_actors());names=set(json.loads((R/'previews/landmarks14-build.json').read_text())['changed']);bad=json.loads((R/'previews/landmarks14-collision.json').read_text())['unresolved_obstructions'];out=[]
for o in bad:
 p,q=o['from'],o['to'];hits=[]
 for actor in allactors:
  if not isinstance(actor,u.StaticMeshActor):continue
  mesh=actor.static_mesh_component.static_mesh
  if not mesh or mesh.get_name() not in names:continue
  ignore=[a for a in allactors if a!=actor]
  hit=u.SystemLibrary.capsule_trace_single(world,u.Vector(p[0]*100,-p[1]*100,105),u.Vector(q[0]*100,-q[1]*100,105),34,88,u.TraceTypeQuery.ECC_VISIBILITY,True,ignore,u.DrawDebugTrace.NONE,True)
  if hit is not None:hits.append(actor.get_actor_label())
 out.append({'obstruction':o,'actors':hits})
(R/'previews/landmarks14-diagnose.json').write_text(json.dumps(out,indent=2))
