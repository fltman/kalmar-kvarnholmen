"""Ground and character-width clearance around the pass-26 houses on Larmgatan: walking lines 1.2 m
and 2.0 m outside every street front of the bank block, Larmgatan 10, 8, 6 and the Odd Fellows
house (entrance steps, plinths, oriels and turrets included), and every named street within 40 m
of the five buildings."""
import unreal as u,json,datetime,math
from pathlib import Path
R=Path(__file__).resolve().parents[3];data=json.loads((R/'source/kvarnholmen.json').read_text());Z=json.loads((R/'source/larm26.json').read_text())['zones']
world=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
vec=lambda p,z:u.Vector(p[0]*100,-p[1]*100,z*100)
MESHES=('Kvarnholmen_House_91222222','Kvarnholmen_House_91856621','Kvarnholmen_House_91856599','Kvarnholmen_House_91856613','Kvarnholmen_House_91856604')
def floor(p):return u.SystemLibrary.line_trace_single(world,vec(p,.65),vec(p,-.55),u.TraceTypeQuery.ECC_VISIBILITY,True,[],u.DrawDebugTrace.NONE,True) is not None
def capsule(p,q):return u.SystemLibrary.capsule_trace_single(world,vec(p,1.05),vec(q,1.05),34,88,u.TraceTypeQuery.ECC_VISIBILITY,True,[],u.DrawDebugTrace.NONE,True)
def dseg(p,a,b):
 dx,dy=b[0]-a[0],b[1]-a[1];l2=dx*dx+dy*dy or 1;t=max(0,min(1,((p[0]-a[0])*dx+(p[1]-a[1])*dy)/l2));return math.dist(p,(a[0]+t*dx,a[1]+t*dy))
def normal(w):
 L=math.dist(w['p'],w['q']);return (w['q'][1]-w['p'][1])/L,-(w['q'][0]-w['p'][0])/L
# Street fronts per zone (outward normal, wall midpoint); the rest face courtyards.
FRONT={'bank':lambda nx,ny,mx,my:(ny>.9 and my>-81) or (nx>.9 and mx>-299.5) or (nx<-.9 and mx<-336) or (nx>.5 and ny>.5),
 'office':lambda nx,ny,mx,my:True,'southwing':lambda nx,ny,mx,my:nx<-.9 or ny<-.9,
 'l10':lambda nx,ny,mx,my:ny>.9 or nx<-.9,'l8':lambda nx,ny,mx,my:nx<-.9,'l6':lambda nx,ny,mx,my:nx<-.9 or ny<-.9,
 'oddfellow':lambda nx,ny,mx,my:True}
def chains(zone):
 # Consecutive street-front walls (ring order, shared end points) joined into runs.
 ws=[w for w in Z[zone]['walls'] if w['kind']=='outer'];keep=[FRONT[zone](*normal(w),(w['p'][0]+w['q'][0])/2,(w['p'][1]+w['q'][1])/2) for w in ws]
 runs=[];cur=[]
 for w,k in zip(ws,keep):
  if k and cur and math.dist(cur[-1]['q'],w['p'])<.01:cur.append(w)
  else:
   if cur:runs.append(cur)
   cur=[w] if k else []
 if cur:runs.append(cur)
 if len(runs)>1 and math.dist(runs[-1][-1]['q'],runs[0][0]['p'])<.01 and keep[0] and keep[-1]:runs[0]=runs.pop()+runs[0]
 return runs
def offset(run,o):
 # Offset polyline with mitred joints. Free ends meet a neighbouring house or, in a re-entrant
 # corner, another zone of the same block, so they are pulled back o+0.3 m: the walking line of
 # the adjoining wall starts there.
 trim=o+.3
 ns=[normal(w) for w in run];pts=[[run[0]['p'][0]+ns[0][0]*o,run[0]['p'][1]+ns[0][1]*o]]
 for w,(n1,n2) in zip(run[1:],zip(ns,ns[1:])):
  c=1+n1[0]*n2[0]+n1[1]*n2[1];pts.append([w['p'][0]+o*(n1[0]+n2[0])/c,w['p'][1]+o*(n1[1]+n2[1])/c])
 pts.append([run[-1]['q'][0]+ns[-1][0]*o,run[-1]['q'][1]+ns[-1][1]*o])
 for end in (0,-1):
  a,b=(pts[0],pts[1]) if end==0 else (pts[-1],pts[-2]);L=math.dist(a,b)
  if L>trim+.3:
   t=trim/L;a[0]+=(b[0]-a[0])*t;a[1]+=(b[1]-a[1])*t
 return pts
routes=[]
for zone in Z:
 for i,run in enumerate(chains(zone)):
  if sum(math.dist(w['p'],w['q']) for w in run)<2.5:continue
  for o in (1.2,2.0):routes.append((f'{zone} front {i+1} {o} m',offset(run,o),'front'))
segs=[(w['p'],w['q']) for z in Z.values() for w in z['walls']]
for road in data['checks']:
 if road['name'] not in {'Larmgatan','Södra Långgatan','Ölandsgatan','Stationsgatan'}:continue
 dense=[road['points'][0]]
 for p,q in zip(road['points'],road['points'][1:]):
  n=max(1,int(math.dist(p,q)/3));dense+=[[p[0]+(q[0]-p[0])*k/n,p[1]+(q[1]-p[1])*k/n] for k in range(1,n+1)]
 run=[]
 for p in dense+[None]:
  if p is not None and min(dseg(p,a,b) for a,b in segs)<=40:run.append(p);continue
  if len(run)>1:routes.append((f"{road['name']} ({road['id']})",run,'street'))
  run=[]
report={'status':'testing','floor_samples':0,'floor_failures':[],'capsule_segments':0,'obstructions':[],'routes':{},'time':datetime.datetime.now().isoformat()}
for name,points,kind in routes:
 stats=report['routes'].setdefault(name,{'kind':kind,'floor_samples':0,'floor_failures':0,'capsule_segments':0,'obstructions':0})
 dense=[points[0]]
 for p,q in zip(points,points[1:]):
  n=max(1,int(math.dist(p,q)/(1 if kind=='front' else 3)));dense+=[[p[0]+(q[0]-p[0])*k/n,p[1]+(q[1]-p[1])*k/n] for k in range(1,n+1)]
 for p in dense:
  report['floor_samples']+=1;stats['floor_samples']+=1
  if not floor(p):report['floor_failures'].append({'route':name,'point':p});stats['floor_failures']+=1
 for p,q in zip(dense,dense[1:]):
  if math.dist(p,q)<.05:continue
  report['capsule_segments']+=1;stats['capsule_segments']+=1;hit=capsule(p,q)
  if hit is not None:
   item={'route':name,'kind':kind,'from':p,'to':q}
   try:
    fields=hit.to_tuple();actor=fields[9];location=fields[5]
    item.update(actor=actor.get_actor_label() if actor else None,impact_cm=[location.x,location.y,location.z])
   except Exception as e:item['detail_error']=str(e)
   report['obstructions'].append(item);stats['obstructions']+=1
# An obstruction (steps, a lamp or a tree in the footway) passes when the route can step aside:
# from 2 m before the blocked stretch, along a line up to 2 m to either side, back 2 m after it,
# clear of everything and on ground throughout. Consecutive blocked segments of one route are one
# obstacle (the bank's entrance steps span several).
report['verified_detours']=[];groups=[]
for obstacle in report['obstructions']:
 if groups and groups[-1][-1]['route']==obstacle['route'] and math.dist(groups[-1][-1]['to'],obstacle['from'])<.01:groups[-1].append(obstacle)
 else:groups.append([obstacle])
for group in groups:
 p,q=group[0]['from'],group[-1]['to'];dx,dy=q[0]-p[0],q[1]-p[1];length=math.hypot(dx,dy);ux,uy=dx/length,dy/length
 p2,q2=[p[0]-ux*2,p[1]-uy*2],[q[0]+ux*2,q[1]+uy*2]
 for off in [.8,-.8,1.25,-1.25,2,-2]:
  ox,oy=-uy*off,ux*off;a,b=[p2[0]+ox,p2[1]+oy],[q2[0]+ox,q2[1]+oy];route=[p2,a,b,q2]
  if all(capsule(c,d) is None for c,d in zip(route,route[1:])) and all(floor(c) for c in [a,b,[(a[0]+b[0])/2,(a[1]+b[1])/2]]):
   for obstacle in group:obstacle['verified_detour']=route
   report['verified_detours'].append({'route':group[0]['route'],'actor':group[0].get('actor'),'segments':len(group),'length_m':round(length,2),'offset_m':abs(off)});break
report['unresolved_obstructions']=[q for q in report['obstructions'] if 'verified_detour' not in q]
report['house_obstructions']=[q for q in report['obstructions'] if str(q.get('actor','')).startswith(MESHES)]
report['houses_on_streets']=[q for q in report['house_obstructions'] if q['kind']=='street']
report['status']='passed' if not report['floor_failures'] and not report['unresolved_obstructions'] and not report['houses_on_streets'] else 'review_required'
(R/'previews/larm26-collision.json').write_text(json.dumps(report,indent=2,ensure_ascii=False))
u.get_editor_subsystem(u.LevelEditorSubsystem).save_current_level()
