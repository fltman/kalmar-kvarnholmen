"""Full-width character clearance and ground continuity from Stortorget to Larmtorget."""
import unreal as u,json,datetime,math
from pathlib import Path
R=Path(__file__).resolve().parents[3]
world=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
def vec(p):return u.Vector(p[0]*100,-p[1]*100,p[2]*100)
floors=[]
for x in range(-36,-307,-5):
 hit=u.SystemLibrary.line_trace_single(world,vec((x,-2.8,1)),vec((x,-2.8,-1)),u.TraceTypeQuery.ECC_VISIBILITY,True,[],u.DrawDebugTrace.NONE,True)
 floors.append({'x':x,'ground_present':hit is not None})
obstruction=u.SystemLibrary.capsule_trace_single(world,vec((-36,-2.8,1.0)),vec((-305,-2.8,1.0)),34,88,u.TraceTypeQuery.ECC_VISIBILITY,True,[],u.DrawDebugTrace.NONE,True)
checks={'ground_continuous':all(f['ground_present'] for f in floors),'character_capsule_clear':obstruction is None}
report={'status':'passed' if all(checks.values()) else 'failed','time':datetime.datetime.now().isoformat(),'checks':checks,'scope':'All scene collision included, including street furniture. 34cm radius / 88cm half-height capsule along the 269m route; ground rays every 5m.','ground_samples':floors,'obstruction':str(obstruction) if obstruction else None}
(R/'previews/storgatan-collision.json').write_text(json.dumps(report,indent=2));u.get_editor_subsystem(u.LevelEditorSubsystem).save_current_level()
