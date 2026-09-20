"""Trace structural backing, floor contact and walking clearances after placement repair."""
import unreal as u,json,datetime
from pathlib import Path
R=Path(__file__).resolve().parents[3];ae=u.get_editor_subsystem(u.EditorActorSubsystem);world=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
all_actors=ae.get_all_level_actors()
ignore=[a for a in all_actors if isinstance(a,u.StaticMeshActor) and a.static_mesh_component.static_mesh and not a.static_mesh_component.static_mesh.get_name().startswith('SM_Domkyrka_Interior_Architecture')]
def vec(p):return u.Vector(p[0]*100,-p[1]*100,p[2]*100)
def hit(a,b,ignored):return u.SystemLibrary.line_trace_single(world,vec(a),vec(b),u.TraceTypeQuery.ECC_VISIBILITY,True,ignored,u.DrawDebugTrace.NONE,True) is not None
checks={}
for uu in [-23,-10.6,23]:
 for side in [-1,1]:checks[f'hymn_board_{uu}_{side}']=hit((10.1+uu,44.4+side*7.2,6.1),(10.1+uu,44.4+side*7.5,6.1),ignore)
for z in [4.28,6.4,9.3]:checks['pulpit_pier_'+str(z)]=hit((19.80,52.3,z),(20.1,52.3,z),ignore)
# Test the four bearing areas: the exact centre lies over an 11 mm grout joint.
for dx in [-.2,.2]:
 for dy in [-.2,.2]:checks[f'pulpit_floor_{dx}_{dy}']=hit((18.65+dx,52.3+dy,1.4),(18.65+dx,52.3+dy,1.25),ignore)
for name,a,b,expected in [('entrance',(10.1,22,3),(10.1,31,3),False),('aisle',(-8,44.4,2.8),(21,44.4,2.8),False),('floor',(10.1,44.4,3),(10.1,44.4,0),True)]:checks[name]=hit(a,b,[])==expected
report={'status':'passed' if all(checks.values()) else 'failed','time':datetime.datetime.now().isoformat(),'checks':checks}
(R/'previews/fixture-final-validation.json').write_text(json.dumps(report,indent=2))
u.get_editor_subsystem(u.LevelEditorSubsystem).save_current_level()
