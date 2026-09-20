"""Check that the changed frontages leave the public walking strips unobstructed."""
import unreal as u,json,datetime
from pathlib import Path
R=Path(__file__).resolve().parents[3]
ae=u.get_editor_subsystem(u.EditorActorSubsystem);world=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
selected=set(json.loads((R/'previews/town-pass9-scope.json').read_text())['changed'])
# Only the altered houses are tested here, not furniture intentionally on the square.
ignore=[a for a in ae.get_all_level_actors() if not isinstance(a,u.StaticMeshActor) or not a.static_mesh_component.static_mesh or a.static_mesh_component.static_mesh.get_name() not in selected]
def vec(p):return u.Vector(p[0]*100,-p[1]*100,p[2]*100)
checks={}
for name,a,b in [('south_walk',(-27,-29,1.6),(48,-29,1.6)),('west_walk',(-34,-27,1.6),(-34,64,1.6)),('east_walk',(53,-32,1.6),(53,63,1.6))]:
 hit=u.SystemLibrary.line_trace_single(world,vec(a),vec(b),u.TraceTypeQuery.ECC_VISIBILITY,True,ignore,u.DrawDebugTrace.NONE,True)
 checks[name]=hit is None
report={'status':'passed' if all(checks.values()) else 'failed','time':datetime.datetime.now().isoformat(),'scope':'Visibility collision rays at pedestrian height against the modified buildings; furniture excluded','checks':checks}
(R/'previews/town-pass9-walkways.json').write_text(json.dumps(report,indent=2));u.get_editor_subsystem(u.LevelEditorSubsystem).save_current_level()
