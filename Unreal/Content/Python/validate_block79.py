"""Ground and character-width clearance round the pass-79 green areas: the named streets past the
parks and the southern rampart, and the mapped park paths, must stay walkable past the new trees,
hedge, grass slope and the corrected southern wall."""
import unreal as u,json,datetime,math,xml.etree.ElementTree as E
from pathlib import Path
R=Path(__file__).resolve().parents[3];data=json.loads((R/'source/kvarnholmen.json').read_text());G=json.loads((R/'source/block79.json').read_text())
world=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
vec=lambda p,z:u.Vector(p[0]*100,-p[1]*100,z*100)
MESHES=('Kvarnholmen_Green79_Lawns','Kvarnholmen_Trees79','Kvarnholmen_Hedge79','Kvarnholmen_Ringmur_Sodra','Kvarnholmen_Green79_Glacis')
def floor(p):return u.SystemLibrary.line_trace_single(world,vec(p,4.0),vec(p,-.55),u.TraceTypeQuery.ECC_VISIBILITY,True,[],u.DrawDebugTrace.NONE,True) is not None
# The ground probe ignores the gate portals, whose vaults would otherwise read as ground in the tunnels.
PORTS=[a for a in u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors() if a.get_actor_label().startswith('Kvarnholmen_Port_')]
def ground(p):
 h=u.SystemLibrary.line_trace_single(world,vec(p,4.0),vec(p,-.55),u.TraceTypeQuery.ECC_VISIBILITY,True,PORTS,u.DrawDebugTrace.NONE,True)
 if h is None:return 0.0
 try:return h.to_tuple()[4].z/100
 except Exception:return 0.0
def capsule(p,q):
 # The capsule rides the local ground (the parks and rampart slopes are not flat).
 zp,zq=ground(p),ground(q)
 return u.SystemLibrary.capsule_trace_single(world,vec(p,zp+1.05),vec(q,zq+1.05),34,88,u.TraceTypeQuery.ECC_VISIBILITY,True,[],u.DrawDebugTrace.NONE,True)
def dseg(p,a,b):
 dx,dy=b[0]-a[0],b[1]-a[1];l2=dx*dx+dy*dy or 1;t=max(0,min(1,((p[0]-a[0])*dx+(p[1]-a[1])*dy)/l2));return math.dist(p,(a[0]+t*dx,a[1]+t*dy))
# Everything this pass added, as segments: tree trunks, the hedge, the slope edges, the kept walls.
segs=[((t['x'],t['y']),(t['x']+.01,t['y'])) for t in G['trees']+G['limes']]+[(a,b) for r in G['hedge']+G['sodra_walls'] for a,b in zip(r,r[1:])]+[(a,b) for g in G['glacis'] for a,b in zip(g['points'],g['points'][1:])]
routes=[]
for road in data['checks']:
 dense=[road['points'][0]]
 for p,q in zip(road['points'],road['points'][1:]):
  n=max(1,int(math.dist(p,q)/3));dense+=[[p[0]+(q[0]-p[0])*k/n,p[1]+(q[1]-p[1])*k/n] for k in range(1,n+1)]
 run=[]
 for p in dense+[None]:
  if p is not None and min(dseg(p,a,b) for a,b in segs)<=25:run.append(p);continue
  if len(run)>1:routes.append((f"{road['name']} ({road['id']})",run,'street'))
  run=[]
# The mapped footways and paths through the parks.
A=math.radians(28.2)
def xy(lat,lon):
 e=(lon-16.3656)*111320*math.cos(math.radians(56.66412));n=(lat-56.66412)*111320;return(e*math.cos(A)+n*math.sin(A),-e*math.sin(A)+n*math.cos(A))
root=E.parse(R/'references/osm-kvarnholmen-full.osm').getroot();nodes={n.get('id'):xy(float(n.get('lat')),float(n.get('lon'))) for n in root.findall('node')}
LAND=data['land'][0]['outer']
def on_land(p):
 # Paths that run off the modelled island (over water at its edge) are left out.
 x,y=p;c=False
 for (x1,y1),(x2,y2) in zip(LAND,LAND[1:]+LAND[:1]):
  if (y1>y)!=(y2>y) and x<x1+(y-y1)*(x2-x1)/(y2-y1):c=not c
 return c
for w in root.findall('way'):
 t={x.get('k'):x.get('v') for x in w.findall('tag')}
 if t.get('highway') not in ('footway','path','track'):continue
 pts=[list(nodes[n.get('ref')]) for n in w.findall('nd') if n.get('ref') in nodes and on_land(nodes[n.get('ref')])]
 near=[p for p in pts if min(math.dist(p,(tt['x'],tt['y'])) for tt in G['trees']+G['limes'])<=15]
 if len(pts)>1 and near:routes.append((f"path {w.get('id')}",pts,'path'))
report={'status':'testing','floor_samples':0,'floor_failures':[],'capsule_segments':0,'obstructions':[],'routes':{},'time':datetime.datetime.now().isoformat()}
for name,points,kind in routes:
 stats=report['routes'].setdefault(name,{'kind':kind,'floor_samples':0,'floor_failures':0,'capsule_segments':0,'obstructions':0})
 dense=[points[0]]
 for p,q in zip(points,points[1:]):
  n=max(1,int(math.dist(p,q)/(2 if kind=='path' else 3)));dense+=[[p[0]+(q[0]-p[0])*k/n,p[1]+(q[1]-p[1])*k/n] for k in range(1,n+1)]
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
# Obstructions by earlier assets (the pass 14 gate portals on Kaggensgatan and at Kavaljersporten)
# are reported but are not this pass's to fix; the pass fails only on its own meshes.
report['preexisting_obstructions']=[q for q in report['unresolved_obstructions'] if not str(q.get('actor','')).startswith(MESHES)]
report['pass_obstructions']=[q for q in report['unresolved_obstructions'] if str(q.get('actor','')).startswith(MESHES)]
report['status']='passed' if not report['floor_failures'] and not report['pass_obstructions'] else 'review_required'
(R/'previews/block79-collision.json').write_text(json.dumps(report,indent=2,ensure_ascii=False))
u.get_editor_subsystem(u.LevelEditorSubsystem).save_current_level()
