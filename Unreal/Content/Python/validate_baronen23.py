"""Ground and character-width clearance around Baronen: named streets, the quay path, the entrance."""
import unreal as u,json,datetime,math
from pathlib import Path
R=Path(__file__).resolve().parents[3];data=json.loads((R/'source/kvarnholmen.json').read_text())
world=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
vec=lambda p,z:u.Vector(p[0]*100,-p[1]*100,z*100)
def floor(p):return u.SystemLibrary.line_trace_single(world,vec(p,.65),vec(p,-.55),u.TraceTypeQuery.ECC_VISIBILITY,True,[],u.DrawDebugTrace.NONE,True) is not None
def capsule(p,q):return u.SystemLibrary.capsule_trace_single(world,vec(p,1.05),vec(q,1.05),34,88,u.TraceTypeQuery.ECC_VISIBILITY,True,[],u.DrawDebugTrace.NONE,True)
report={'status':'testing','floor_samples':0,'floor_failures':[],'capsule_segments':0,'obstructions':[],'streets':{},'time':datetime.datetime.now().isoformat()}
# Same Jordbroporten offset as validate_street22: the mapped centreline meets the gate pier.
routes=[(road['name'],[[x-2.1 if road['name']=='Kaggensgatan' and -220<y<-175 else x,y] for x,y in road['points']]) for road in data['checks'] if road['name'] in {'Skeppsbrogatan','Skeppsbron','Kaggensgatan','Ölandskajen'}]
# OSM footway 129011579 along the quay, 2.5-7 m outside the harbour facades (unnamed, not in the district checks).
routes.append(('Kajpromenaden',[[-306.33,-292.8],[-289.5,-310.02],[-254.18,-345.53],[-245.82,-352.58],[-234.6,-359.01],[-223.28,-363.41],[-207.76,-367.99],[-179.18,-372.33],[-152.41,-360.25],[-133.55,-342.43],[-128.17,-341.78],[-121.17,-335.67],[-120.24,-328.72],[-93.1,-301.37]]))
# Kaggensgatan's paved walk through the car park, continued to 0.6 m in front of the octagon's doors.
routes.append(('Entre',[[-188.066,-256.613],[-187.32,-265.49],[-186.6,-273.6]]))
for name,points in routes:
 stats=report['streets'].setdefault(name,{'floor_samples':0,'floor_failures':0,'capsule_segments':0,'obstructions':0})
 dense=[points[0]]
 for p,q in zip(points,points[1:]):
  n=max(1,int(math.dist(p,q)/4));dense+= [[p[0]+(q[0]-p[0])*k/n,p[1]+(q[1]-p[1])*k/n] for k in range(1,n+1)]
 for p in dense:
  report['floor_samples']+=1;stats['floor_samples']+=1
  if not floor(p):report['floor_failures'].append({'street':name,'point':p});stats['floor_failures']+=1
 for p,q in zip(dense,dense[1:]):
  report['capsule_segments']+=1;stats['capsule_segments']+=1;hit=capsule(p,q)
  if hit is not None:
   item={'street':name,'from':p,'to':q,'hit':str(hit)}
   try:
    fields=hit.to_tuple();actor=fields[9];location=fields[5]
    item.update(actor=actor.get_actor_label() if actor else None,impact_cm=[location.x,location.y,location.z])
   except Exception as e:item['detail_error']=str(e)
   report['obstructions'].append(item);stats['obstructions']+=1
# Existing lamp posts and bollards need a small walking detour, not removal.
report['verified_detours']=[]
for obstacle in report['obstructions']:
 p,q=obstacle['from'],obstacle['to'];dx,dy=q[0]-p[0],q[1]-p[1];length=math.hypot(dx,dy)
 for offset in [.8,-.8,1.25,-1.25,2,-2,3,-3]:
  ox,oy=-dy/length*offset,dx/length*offset;a,b=[p[0]+ox,p[1]+oy],[q[0]+ox,q[1]+oy];route=[p,a,b,q]
  if all(capsule(c,d) is None for c,d in zip(route,route[1:])) and all(floor(c) for c in [a,b,[(a[0]+b[0])/2,(a[1]+b[1])/2]]):
   obstacle['verified_detour']=route;report['verified_detours'].append({'street':obstacle['street'],'route':route,'offset_m':abs(offset)});break
report['unresolved_obstructions']=[q for q in report['obstructions'] if 'verified_detour' not in q]
report['baronen_obstructions']=[q for q in report['obstructions'] if str(q.get('actor','')).startswith(('Baronen23','Kvarnholmen_House_38033725'))]
# The parking deck must carry a person where the stair houses stand (floor trace from above).
report['deck_floor']=all(u.SystemLibrary.line_trace_single(world,vec(p,6.2),vec(p,4.0),u.TraceTypeQuery.ECC_VISIBILITY,True,[],u.DrawDebugTrace.NONE,True) is not None for p in [[-215.0,-356.5],[-240.0,-348.0],[-176.0,-360.5]])
report['status']='passed' if not report['floor_failures'] and not report['unresolved_obstructions'] and not report['baronen_obstructions'] and report['deck_floor'] else 'review_required'
(R/'previews/baronen23-collision.json').write_text(json.dumps(report,indent=2,ensure_ascii=False))
u.get_editor_subsystem(u.LevelEditorSubsystem).save_current_level()
