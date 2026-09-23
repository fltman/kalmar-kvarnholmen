"""Ground and character-width clearance around Kalmar C: Stationsgatan, the plaza front and the
platform under the canopy (between the wall and the columns)."""
import unreal as u,json,datetime,math
from pathlib import Path
R=Path(__file__).resolve().parents[3];data=json.loads((R/'source/kvarnholmen.json').read_text());S=json.loads((R/'source/station24.json').read_text())
world=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
vec=lambda p,z:u.Vector(p[0]*100,-p[1]*100,z*100)
def floor(p):return u.SystemLibrary.line_trace_single(world,vec(p,.65),vec(p,-.55),u.TraceTypeQuery.ECC_VISIBILITY,True,[],u.DrawDebugTrace.NONE,True) is not None
def capsule(p,q):return u.SystemLibrary.capsule_trace_single(world,vec(p,1.05),vec(q,1.05),34,88,u.TraceTypeQuery.ECC_VISIBILITY,True,[],u.DrawDebugTrace.NONE,True)
FO,FU,FN=S['frame']['origin'],S['frame']['along'],S['frame']['depth']
A,B,C,D=S['range1874']['corners']
def along(p,q,o,before=1.5,after=0.0):
 # Line parallel to the wall p-q, o metres outside it (right-hand side of p->q is outside),
 # from 'before' metres ahead of p to 'after' metres short of q.
 L=math.dist(p,q);ux,uy=(q[0]-p[0])/L,(q[1]-p[1])/L;nx,ny=uy,-ux
 return [[p[0]+nx*o-ux*before,p[1]+ny*o-uy*before],[q[0]+nx*o-ux*after,q[1]+ny*o-uy*after]]
ring=[x for x in data['buildings'] if x['id']=='90965025'][0]['polygons'][0]['outer']
report={'status':'testing','floor_samples':0,'floor_failures':[],'capsule_segments':0,'obstructions':[],'streets':{},'time':datetime.datetime.now().isoformat()}
routes=[(road['name'],road['points']) for road in data['checks'] if road['name'] in {'Stationsgatan'}]
# Platform along the 1874 range, 1.3 m and 2.0 m from the wall: clear of the door steps, inside the columns.
# The 1910 block projects 1.5 m towards the tracks, so each front gets its own line.
for o in (1.3,2.0):
 routes.append((f'Plattform 1874 {o} m',along(C,D,o,1.5,1.0)))
 routes.append((f'Plattform 1910 {o} m',along(ring[17],ring[15],o,-0.5,-4.0)))
# Plaza front of the 1874 range and the 1910 block, 3 m out.
routes.append(('Framsida 1874',along(A,B,3.0)[::-1]))
routes.append(('Framsida 1910',[[FO[0]-FN[0]*3.0,FO[1]-FN[1]*3.0],[FO[0]+FU[0]*15.5-FN[0]*3.0,FO[1]+FU[1]*15.5-FN[1]*3.0]]))
for name,points in routes:
 stats=report['streets'].setdefault(name,{'floor_samples':0,'floor_failures':0,'capsule_segments':0,'obstructions':0})
 dense=[points[0]]
 for p,q in zip(points,points[1:]):
  n=max(1,int(math.dist(p,q)/3));dense+=[[p[0]+(q[0]-p[0])*k/n,p[1]+(q[1]-p[1])*k/n] for k in range(1,n+1)]
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
report['verified_detours']=[]
for obstacle in report['obstructions']:
 p,q=obstacle['from'],obstacle['to'];dx,dy=q[0]-p[0],q[1]-p[1];length=math.hypot(dx,dy)
 for offset in [.8,-.8,1.25,-1.25,2,-2,3,-3]:
  ox,oy=-dy/length*offset,dx/length*offset;a,b=[p[0]+ox,p[1]+oy],[q[0]+ox,q[1]+oy];route=[p,a,b,q]
  if all(capsule(c,d) is None for c,d in zip(route,route[1:])) and all(floor(c) for c in [a,b,[(a[0]+b[0])/2,(a[1]+b[1])/2]]):
   obstacle['verified_detour']=route;report['verified_detours'].append({'street':obstacle['street'],'route':route,'offset_m':abs(offset)});break
report['unresolved_obstructions']=[q for q in report['obstructions'] if 'verified_detour' not in q]
report['station_obstructions']=[q for q in report['obstructions'] if str(q.get('actor','')).startswith(('Kvarnholmen_House_90965009','Kvarnholmen_House_90965025','Station24'))]
report['status']='passed' if not report['floor_failures'] and not report['unresolved_obstructions'] and not report['station_obstructions'] else 'review_required'
(R/'previews/station24-collision.json').write_text(json.dumps(report,indent=2,ensure_ascii=False))
u.get_editor_subsystem(u.LevelEditorSubsystem).save_current_level()
