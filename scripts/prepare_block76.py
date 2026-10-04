"""Pass 76: the district volumes 90859889, 90859896 and 90859844 on the north side of Norra
Långgatan, opposite pass 75, split at their measured joints into five houses: the green boarded
cottage with its cross gable, the red house with white windows, the red house with green windows
and the orange door, a narrow boarded passage door, and the white gable-fronted house with its
low back annex. The two carriage gates between the green and the red houses open onto a yard: that
strip (x 198.3-202.3) is released as open ground and the gates are drawn in the build.
Heights come from two Google Street View panoramas (April 2025) on Norra Långgatan resected in pass
75; see references/block76-notes.md.
"""
from pathlib import Path
import json,math,os,sys
if os.environ.get('KALMAR_GEO'):sys.path.insert(0,os.environ['KALMAR_GEO'])
from shapely.geometry import Polygon,Point,box
from shapely.geometry.polygon import orient
from shapely.ops import unary_union
R=Path(__file__).resolve().parents[1]
district=json.loads((R/'source/kvarnholmen.json').read_text())
d17=json.loads((R/'source/district17.json').read_text())['buildings']
def dring(bid):return [tuple(w['p']) for w in d17['SM_Building_'+bid]['walls']]
def flat(g):
 g=g.buffer(0);return [g] if g.geom_type=='Polygon' else [q for c in getattr(g,'geoms',[]) for q in flat(c)]
def parts(g):return [orient(r) for q in flat(g) for r in flat(q.buffer(-.02,join_style=2).buffer(.02,join_style=2).simplify(.02)) if r.area>1.0]
PG=lambda b:Polygon([tuple(w['p']) for w in d17['SM_Kvarnholmen_House_'+b]['walls']]).buffer(0)
P89,P96,P44=PG('90859889'),PG('90859896'),PG('90859844')
ALL=unary_union([P89,P96,P44])
GR=P89.intersection(box(180,60,198.3,90));RW=P96.intersection(box(202.3,60,209.7,90))
RE=unary_union([P96,P44]).intersection(box(209.7,60,221.82,90))
PS=P44.intersection(box(221.82,60,222.45,78.4));WW=P44.intersection(box(222.45,60,229.5,78.4))
BK=P44.difference(unary_union([RE,PS,WW]))
PB=unary_union([GR,RW,RE,PS,WW,BK]);RELEASED=ALL.difference(PB)
seeds=[('gr',GR),('rw',RW),('re',RE),('ps',PS),('ww',WW),('bk',BK)]
# Heights (m) above the facade base, measured (the north side lies about 0.3 m below the resected
# base row): the green cottage's eaves 3.4, its cross gable to 4.8 and main ridge 5.0 (estimate);
# both red houses' eaves 4.1 and ridges 6.0 (estimate); the passage door 2.4; the white house's
# walls to 2.8 (its gable is drawn in the build: eaves 3.9 west and 2.8 east, apex 5.8); the back
# annex 2.8 under a roof to 4.0 (estimate).
spec={'gr':dict(height=3.4,top=5.0,mesh='SM_Kvarnholmen_House_90859889'),'rw':dict(height=4.1,top=6.0,mesh='SM_Kvarnholmen_House_90859896'),
 're':dict(height=4.1,top=6.0,mesh='SM_Kvarnholmen_House_90859896'),'ps':dict(height=2.4,top=2.6,mesh='SM_Kvarnholmen_House_90859844'),
 'ww':dict(height=2.8,top=5.8,mesh='SM_Kvarnholmen_House_90859844'),'bk':dict(height=2.8,top=4.0,mesh='SM_Kvarnholmen_House_90859844')}
taken=Polygon();zones={}
for name,seed in seeds:
 ps=parts(seed.difference(taken));zones[name]=ps;taken=unary_union([taken]+ps)
scope={'90859889','90859896','90859844'}
others=[(Polygon([tuple(w['p']) for w in v['walls']]).buffer(0),v['H'],v['id']) for v in d17.values() if v['id'] not in scope and len(v['walls'])>=3]
def neighbour_at(pt):
 for name,ps in zones.items():
  if any(p.buffer(.001).contains(pt) for p in ps):return name,spec[name]['height']
 for g,h,bid in others:
  if g.buffer(.001).contains(pt):return bid,h
 return None,0.0
out={};report={}
for name,ps in zones.items():
 H=spec[name]['height'];walls=[]
 for poly in ps:
  cs=list(poly.exterior.coords)[:-1]
  for p,q in zip(cs,cs[1:]+cs[:1]):
   Lw=math.dist(p,q)
   if Lw<.05:continue
   wx,wy=(q[0]-p[0])/Lw,(q[1]-p[1])/Lw;nx,ny=wy,-wx;n=max(1,int(Lw/.2));runs=[]
   for k in range(n):
    t=(k+.5)/n;nb,h=neighbour_at(Point(p[0]+wx*Lw*t+nx*.3,p[1]+wy*Lw*t+ny*.3))
    if runs and runs[-1][0]==nb:runs[-1][3]=(k+1)/n
    else:runs.append([nb,h,k/n,(k+1)/n])
   for nb,h,t0,t1 in runs:
    z0=0.0 if nb is None else h
    if z0>=H-.05:continue
    a=(round(p[0]+wx*Lw*t0,3),round(p[1]+wy*Lw*t0,3));b=(round(p[0]+wx*Lw*t1,3),round(p[1]+wy*Lw*t1,3))
    if math.dist(a,b)<.2:continue
    walls.append({'p':list(a),'q':list(b),'z0':z0,'z1':H,'kind':'outer' if nb is None else 'upper','neighbour':nb})
 out[name]=dict(spec[name],polygons=[[list(v) for v in list(p.exterior.coords)[:-1]] for p in ps],walls=walls)
 report[name]={'area_m2':round(sum(p.area for p in ps),1),'polygons':len(ps),'walls':len(walls),'outer_m':round(sum(math.dist(w['p'],w['q']) for w in walls if w['kind']=='outer'),1)}
def inner(ring,insets):
 lines=[]
 for (p,q),d in zip(zip(ring,ring[1:]+ring[:1]),insets):
  Lr=math.dist(p,q);ax,ay=(q[0]-p[0])/Lr,(q[1]-p[1])/Lr;nx,ny=-ay,ax
  lines.append(((p[0]+nx*d,p[1]+ny*d),(ax,ay)))
 pts=[]
 for i in range(len(ring)):
  (p1,d1),(p2,d2)=lines[i-1],lines[i];det=d1[0]*(-d2[1])-d1[1]*(-d2[0])
  t=((p2[0]-p1[0])*(-d2[1])-(p2[1]-p1[1])*(-d2[0]))/det;pts.append((round(p1[0]+d1[0]*t,3),round(p1[1]+d1[1]*t,3)))
 return pts
def roof_ring(name,inset):
 # Counter-clockwise outline of the zone, merged at near-collinear vertices; inset 0 on the edges
 # that lie on a party wall (a fire wall rises there), the given inset on the free edges.
 poly=orient(zones[name][0].simplify(.12));ring=[tuple(round(c,3) for c in v) for v in list(poly.exterior.coords)[:-1]]
 fire=[]
 for p,q in zip(ring,ring[1:]+ring[:1]):
  Lr=math.dist(p,q);wx,wy=(q[0]-p[0])/Lr,(q[1]-p[1])/Lr;nx,ny=wy,-wx
  nb,_=neighbour_at(Point((p[0]+q[0])/2+nx*.3,(p[1]+q[1])/2+ny*.3))
  fire.append(nb is not None)
 r1=inner(ring,[0 if f else inset for f in fire])
 assert Polygon(ring).exterior.is_ccw and Polygon(r1).is_valid and Polygon(r1).area>.5,(name,r1)
 return dict(outer=[list(v) for v in ring],r1=[list(v) for v in r1],firewall=fire,inset=inset)
# Roofs are drawn from the outlines in the build.
covered=unary_union([p for ps in zones.values() for p in ps]);foot=PB
data={'source':'district volume 90859844 (source/district17.json), '+district['source'],'zones':out,
 'checks':{'footprint_m2':round(foot.area,1),'zoned_m2':round(covered.area,1),'outside_osm_m2':round(covered.difference(foot).area,2),'osm_not_zoned_m2':round(foot.difference(covered).area,2),
  'overlap_m2':round(sum(p.area for ps in zones.values() for p in ps)-covered.area,3),'released_m2':round(RELEASED.area,1)}}
(R/'source/block76.json').write_text(json.dumps(data,indent=1,ensure_ascii=False))
c=data['checks'];ok=c['outside_osm_m2']<.2 and c['osm_not_zoned_m2']<.5 and c['overlap_m2']<.2
(R/'previews/block76-zones.json').write_text(json.dumps({'status':'passed' if ok else 'review_required','zones':report,'checks':c},indent=2,ensure_ascii=False))
print(json.dumps(report));print(c);print('BLOCK76_ZONES_OK' if ok else 'BLOCK76_ZONES_REVIEW')
