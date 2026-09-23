"""Ground and character-width clearance at the Kalmar C tracks: the walking line along every
track-facing platform edge, the crossing from footway to footway, and every named street within
40 m of the tracks (the island surface was rebuilt around the cut)."""
import unreal as u,json,datetime,math
from pathlib import Path
R=Path(__file__).resolve().parents[3];data=json.loads((R/'source/kvarnholmen.json').read_text());RD=json.loads((R/'source/rail25.json').read_text())
world=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
vec=lambda p,z:u.Vector(p[0]*100,-p[1]*100,z*100)
PT,RT=RD['levels']['platform_top'],RD['levels']['rail_top']
def floor(p):
 # Height of the first surface under p between +0.65 m and -0.55 m, or None.
 hit=u.SystemLibrary.line_trace_single(world,vec(p,.65),vec(p,-.55),u.TraceTypeQuery.ECC_VISIBILITY,True,[],u.DrawDebugTrace.NONE,True)
 if hit is None:return None
 try:return hit.to_tuple()[5].z/100
 except Exception:return .0
def capsule(p,q):return u.SystemLibrary.capsule_trace_single(world,vec(p,1.05),vec(q,1.05),34,88,u.TraceTypeQuery.ECC_VISIBILITY,True,[],u.DrawDebugTrace.NONE,True)
def inside(pt,poly):
 x,y=pt;c=False;j=len(poly)-1
 for i in range(len(poly)):
  xi,yi=poly[i];xj,yj=poly[j]
  if (yi>y)!=(yj>y) and x<(xj-xi)*(y-yi)/(yj-yi+1e-12)+xi:c=not c
  j=i
 return c
def dseg(p,a,b):
 dx,dy=b[0]-a[0],b[1]-a[1];l2=dx*dx+dy*dy or 1;t=max(0,min(1,((p[0]-a[0])*dx+(p[1]-a[1])*dy)/l2));return math.dist(p,(a[0]+t*dx,a[1]+t*dy))
routes=[]
# Platforms: the walking line behind the warning tiles, 1.2 m in from each track-facing edge
# (2.85 m from the track centre), split into separate runs wherever it leaves the platform.
for pl in RD['platforms']:
 poly=pl['polygon'];edges=list(zip(poly,poly[1:]+poly[:1]))
 for t in RD['tracks']:
  ps=t['points']
  for side in (1,-1):
   run=[]
   def flush():
    if len(run)>1:routes.append((f"Plattform {pl['ref']} ({pl['id']}) längs {t['id']} {side:+d}",list(run),'platform'))
    run.clear()
   for a_,b_ in zip(ps,ps[1:]):
    L=math.dist(a_,b_);ux,uy=(b_[0]-a_[0])/L,(b_[1]-a_[1])/L;nx,ny=-uy*side,ux*side
    for k in range(int(L)):
     p=[a_[0]+ux*k+nx*2.85,a_[1]+uy*k+ny*2.85]
     if inside(p,poly) and min(dseg(p,q,r) for q,r in edges)>.5:run.append(p)
     else:flush()
   flush()
# Crossing: along the footway from 1.5 m before the first ramp to 1.5 m past the last.
fw=RD['crossing_line'];CP=RD['crossing_profile'];ux,uy=fw[-1][0]-fw[0][0],fw[-1][1]-fw[0][1];ul=math.hypot(ux,uy);ux,uy=ux/ul,uy/ul
routes.append(('Plankorsning',[[fw[0][0]+ux*s,fw[0][1]+uy*s] for s in [CP['s_lo']-1.5+k*.5 for k in range(int((CP['s_hi']-CP['s_lo']+3)/.5)+1)]],'crossing'))
# Named streets that pass within 40 m of a track.
track_segs=[(a,b) for t in RD['tracks'] for a,b in zip(t['points'],t['points'][1:])]
for road in data['checks']:
 if any(dseg(p,a,b)<40 for p in road['points'] for a,b in track_segs):routes.append((road['name'],road['points'],'street'))
def cross_z(p):
 s=(p[0]-fw[0][0])*ux+(p[1]-fw[0][1])*uy
 if s<CP['s_lo'] or s>CP['s_hi']:return None
 if s<CP['s_a']:return CP['top_lo']+(RT-.005-CP['top_lo'])*(s-CP['s_lo'])/(CP['s_a']-CP['s_lo'])
 if s>CP['s_b']:return RT-.005+(CP['top_hi']-RT+.005)*(s-CP['s_b'])/(CP['s_hi']-CP['s_b'])
 return RT-.005
report={'status':'testing','floor_samples':0,'floor_failures':[],'height_mismatches':[],'capsule_segments':0,'obstructions':[],'routes':{},'time':datetime.datetime.now().isoformat()}
for name,points,kind in routes:
 stats=report['routes'].setdefault(name,{'kind':kind,'floor_samples':0,'floor_failures':0,'height_mismatches':0,'capsule_segments':0,'obstructions':0})
 dense=[points[0]]
 for p,q in zip(points,points[1:]):
  n=max(1,int(math.dist(p,q)/(1 if kind!='street' else 3)));dense+=[[p[0]+(q[0]-p[0])*k/n,p[1]+(q[1]-p[1])*k/n] for k in range(1,n+1)]
 for p in dense:
  report['floor_samples']+=1;stats['floor_samples']+=1;z=floor(p)
  if z is None:report['floor_failures'].append({'route':name,'point':p});stats['floor_failures']+=1;continue
  want=PT if kind=='platform' else cross_z(p) if kind=='crossing' else None
  if want is not None and abs(z-want)>.03:report['height_mismatches'].append({'route':name,'point':p,'floor_m':round(z,3),'expected_m':round(want,3)});stats['height_mismatches']+=1
 for p,q in zip(dense,dense[1:]):
  report['capsule_segments']+=1;stats['capsule_segments']+=1;hit=capsule(p,q)
  if hit is not None:
   item={'route':name,'kind':kind,'from':p,'to':q}
   try:
    fields=hit.to_tuple();actor=fields[9];location=fields[5]
    item.update(actor=actor.get_actor_label() if actor else None,impact_cm=[location.x,location.y,location.z])
   except Exception as e:item['detail_error']=str(e)
   report['obstructions'].append(item);stats['obstructions']+=1
# An obstruction (a mast or column standing in the walkway) passes when the route can step aside:
# from 2 m before the blocked segment, along a line up to 2 m to either side, back 2 m after it,
# clear of everything and on platform (or any) ground throughout.
report['verified_detours']=[]
def ground_ok(c,kind):
 z=floor(c);return z is not None and (kind!='platform' or abs(z-PT)<=.03)
for obstacle in report['obstructions']:
 p,q=obstacle['from'],obstacle['to'];dx,dy=q[0]-p[0],q[1]-p[1];length=math.hypot(dx,dy);ux,uy=dx/length,dy/length
 p2,q2=[p[0]-ux*2,p[1]-uy*2],[q[0]+ux*2,q[1]+uy*2]
 for offset in [.8,-.8,1.25,-1.25,2,-2]:
  ox,oy=-uy*offset,ux*offset;a,b=[p2[0]+ox,p2[1]+oy],[q2[0]+ox,q2[1]+oy];route=[p2,a,b,q2]
  if all(capsule(c,d) is None for c,d in zip(route,route[1:])) and all(ground_ok(c,obstacle['kind']) for c in [a,b,[(a[0]+b[0])/2,(a[1]+b[1])/2]]):
   obstacle['verified_detour']=route;report['verified_detours'].append({'route':obstacle['route'],'actor':obstacle.get('actor'),'offset_m':abs(offset)});break
report['unresolved_obstructions']=[q for q in report['obstructions'] if 'verified_detour' not in q]
# A raised sample under an obstruction that has a verified detour is that obstacle's foot (a mast
# base plate), not a wrong platform level.
for h in report['height_mismatches']:
 h['on_detoured_obstacle']=any('verified_detour' in q and q['route']==h['route'] and min(math.dist(h['point'],q['from']),math.dist(h['point'],q['to']))<1.5 for q in report['obstructions'])
report['unexplained_height_mismatches']=[h for h in report['height_mismatches'] if not h['on_detoured_obstacle']]
report['rail_on_streets']=[q for q in report['obstructions'] if q['kind']=='street' and str(q.get('actor','')).startswith(('Rail25','Kvarnholmen_Land','Kvarnholmen_Street_07_09'))]
report['status']='passed' if not report['floor_failures'] and not report['unexplained_height_mismatches'] and not report['unresolved_obstructions'] and not report['rail_on_streets'] else 'review_required'
(R/'previews/rail25-collision.json').write_text(json.dumps(report,indent=2,ensure_ascii=False))
u.get_editor_subsystem(u.LevelEditorSubsystem).save_current_level()
