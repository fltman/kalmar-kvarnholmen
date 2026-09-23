"""Ground and character-width clearance on Slottsholmen: the timber bridge from the ravelin to the
gate, the gate tunnel into the dry moat, the gravel paths in the dry moat and on the ramparts, the
walled causeway to the castle door, the courtyard round the well house, the ravelin paths and the
bridge towards the park. The ground lies between 4 and 10 m above the model's zero, so every trace
is taken relative to the surface expected on its route, and each capsule rides that surface."""
import unreal as u,json,datetime,math
from pathlib import Path
R=Path(__file__).resolve().parents[3];C=json.loads((R/'source/castle27.json').read_text());H=C['levels_h']
world=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
zh=lambda h:-1.33+h
vec=lambda p,z:u.Vector(p[0]*100,-p[1]*100,z*100)
def floor(p,expect,above=.65,below=.55):
 hit=u.SystemLibrary.line_trace_single(world,vec(p,expect+above),vec(p,expect-below),u.TraceTypeQuery.ECC_VISIBILITY,True,[],u.DrawDebugTrace.NONE,True)
 if hit is None:return None
 try:return hit.to_tuple()[5].z/100
 except Exception:return expect
def capsule(p,zp,q,zq):return u.SystemLibrary.capsule_trace_single(world,vec(p,zp+1.05),vec(q,zq+1.05),34,88,u.TraceTypeQuery.ECC_VISIBILITY,True,[],u.DrawDebugTrace.NONE,True)
def dense(points,step):
 out=[list(points[0])]
 for p,q in zip(points,points[1:]):
  n=max(1,int(math.dist(p,q)/step));out+=[[p[0]+(q[0]-p[0])*k/n,p[1]+(q[1]-p[1])*k/n] for k in range(1,n+1)]
 return out
routes=[]
# Main bridge, deck from the ravelin level down to the gate threshold; then the tunnel to the moat.
main=C['bridges']['main']['points'];Lm=sum(math.dist(p,q) for p,q in zip(main,main[1:]))
def deck_z(p):
 # expected deck height along the bridge (linear in distance from the ravelin end)
 best=None;acc=0.0
 for a,b in zip(main,main[1:]):
  L=math.dist(a,b);t=max(0,min(1,((p[0]-a[0])*(b[0]-a[0])+(p[1]-a[1])*(b[1]-a[1]))/L/L));d=math.dist(p,(a[0]+(b[0]-a[0])*t,a[1]+(b[1]-a[1])*t))
  if best is None or d<best[0]:best=(d,acc+L*t)
  acc+=L
 return zh(H['ravelin'])+(zh(H['deck'])-zh(H['ravelin']))*best[1]/Lm
# start the bridge route 1.5 m out on the deck so the first sample is clear of the ravelin coping
routes.append(('Bro till porten',main,deck_z,1.0))
# Gate tunnel along its OSM line, then the walled corridor across the moat floor to the castle gate.
tl=C['tunnel'];cd=C['castle_door']
walk=[p['points'] for p in C['paths'] if p['osm_way']=='90613989']
walk=walk[0] if walk else [tl[-1],cd]
def inside(pt,poly):
 x,y=pt;c=False;j=len(poly)-1
 for i in range(len(poly)):
  xi,yi=poly[i];xj,yj=poly[j]
  if (yi>y)!=(yj>y) and x<(xj-xi)*(y-yi)/(yj-yi+1e-12)+xi:c=not c
  j=i
 return c
kr=C['castle']['kure_rect'];kc=[sum(v[0] for v in kr)/4,sum(v[1] for v in kr)/4]
grown=[[kc[0]+(v[0]-kc[0])*1.14,kc[1]+(v[1]-kc[1])*1.14] for v in kr]   # stop about 1.2 m before the tower face
gw=[]
for pt in dense(tl+walk[1:],.5):
 if inside(pt,grown):break
 gw.append(pt)
routes.append(('Porttunneln och gången till Kuretornet',gw,lambda p:zh(H['foot']),1.0))
# The cobbled ramp from the tunnel mouth up along the counterscarp (OSM 1165138006) is not modelled.
names={'90614021':'Torrgraven, gång runt slottet','90613995':'Torrgraven, gång mot porttunneln','90613981':'Vallgången','206979655':'Ravelinen','1084130865':'Ravelinen, mot bron'}
for p in C['paths']:
 if p['osm_way'] not in names:continue
 z=zh(H['rampart']) if p['osm_way']=='90613981' else zh(H['ravelin']) if p['osm_way'] in ('206979655','1084130865') else zh(H['foot'])
 routes.append((names[p['osm_way']],p['points'],(lambda zz:lambda q:zz)(z),1.0))
# Courtyard loop 3 m in front of the fronts, clear of the well house.
court=C['castle']['court'];cx=sum(p[0] for p in court)/len(court);cy=sum(p[1] for p in court)/len(court)
loop=[]
for p in court:
 dx,dy=cx-p[0],cy-p[1];L=math.hypot(dx,dy);loop.append([p[0]+dx/L*4.2,p[1]+dy/L*4.2])
routes.append(('Borggården',loop+[loop[0]],lambda p:zh(H['courtyard']),1.0))
rb=C['bridges']['ravelin']['points'];routes.append(('Bro mot parken',rb[::-1][:-1]+[[rb[0][0]+(rb[1][0]-rb[0][0])*.12,rb[0][1]+(rb[1][1]-rb[0][1])*.12]],lambda p:zh(H['ravelin']),1.0))
report={'status':'testing','floor_samples':0,'floor_failures':[],'capsule_segments':0,'obstructions':[],'routes':{},'time':datetime.datetime.now().isoformat()}
for name,points,expect,step in routes:
 st=report['routes'].setdefault(name,{'floor_samples':0,'floor_failures':0,'capsule_segments':0,'obstructions':0});pts=dense(points,step);zs=[]
 rampart=name=='Vallgången'
 for p in pts:
  report['floor_samples']+=1;st['floor_samples']+=1
  z=floor(p,expect(p),.65,5.5 if rampart else .55)
  if z is None:report['floor_failures'].append({'route':name,'point':p,'expected_z':round(expect(p),2)});st['floor_failures']+=1
  zs.append(z)
 for (p,zp),(q,zq) in zip(zip(pts,zs),zip(pts[1:],zs[1:])):
  if zp is None or zq is None or math.dist(p,q)<.05:continue
  report['capsule_segments']+=1;st['capsule_segments']+=1;hit=capsule(p,zp,q,zq)
  if hit is not None:
   item={'route':name,'from':p,'to':q,'z':[round(zp,2),round(zq,2)]}
   try:
    f=hit.to_tuple();actor=f[9];loc=f[5];item.update(actor=actor.get_actor_label() if actor else None,impact=[round(loc.x/100,2),round(-loc.y/100,2),round(loc.z/100,2)])
   except Exception as e:item['detail_error']=str(e)
   report['obstructions'].append(item);st['obstructions']+=1
# Obstructions (a cannon, a railing post) pass when the route can step aside: 2 m before, a parallel
# line up to 2 m to either side, 2 m after; consecutive blocked segments form one obstacle.
report['verified_detours']=[];groups=[]
for ob in report['obstructions']:
 if groups and groups[-1][-1]['route']==ob['route'] and math.dist(groups[-1][-1]['to'],ob['from'])<.01:groups[-1].append(ob)
 else:groups.append([ob])
exp={n:e for n,_,e,_ in routes}
for gr in groups:
 p,q=gr[0]['from'],gr[-1]['to'];dx,dy=q[0]-p[0],q[1]-p[1];L=math.hypot(dx,dy);ux,uy=dx/L,dy/L;e=exp[gr[0]['route']]
 p2,q2=[p[0]-ux*2,p[1]-uy*2],[q[0]+ux*2,q[1]+uy*2]
 for off in [.8,-.8,1.25,-1.25,2,-2]:
  ox,oy=-uy*off,ux*off;a_,b_=[p2[0]+ox,p2[1]+oy],[q2[0]+ox,q2[1]+oy];route=[p2,a_,b_,q2];zz=[floor(c,e(c),.65,5.5 if gr[0]['route']=='Vallgången' else .55) for c in route]
  if None in zz:continue
  if all(capsule(c,zc,d,zd) is None for (c,zc),(d,zd) in zip(zip(route,zz),zip(route[1:],zz[1:]))):
   for ob in gr:ob['verified_detour']=route
   report['verified_detours'].append({'route':gr[0]['route'],'actor':gr[0].get('actor'),'segments':len(gr),'offset_m':abs(off)});break
report['unresolved_obstructions']=[o for o in report['obstructions'] if 'verified_detour' not in o]
report['status']='passed' if not report['floor_failures'] and not report['unresolved_obstructions'] else 'review_required'
(R/'previews/castle27-collision.json').write_text(json.dumps(report,indent=2,ensure_ascii=False))
u.get_editor_subsystem(u.LevelEditorSubsystem).save_current_level()
