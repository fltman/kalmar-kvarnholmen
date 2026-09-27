"""Pass 45: the district volumes 92379262 and 92379314 on the south side of Ölandsgatan between
Västra Sjögatan and the Frösunda house: the yellow two-storey house (a baroque-classical stone
house, five axes), the one-storey entrance link with a relief, the long beige house of 1909 with
two curved front gables and three dormers, and the plain beige two-storey house (Frösunda). The
Södra Vallgatan side and the courtyard wings stay plain. Heights come from Google Street View
panoramas (April 2025) chained along the street; see references/block45-notes.md.
Run with Shapely on the path: KALMAR_GEO=/path/to/site-packages python3 prepare_block45.py
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
P62=Polygon([tuple(w['p']) for w in d17['SM_Kvarnholmen_House_92379262']['walls']]).buffer(0)
P14=Polygon([tuple(w['p']) for w in d17['SM_Kvarnholmen_House_92379314']['walls']]).buffer(0)
PB=P62.union(P14)
# Street ranges on Ölandsgatan, split at the measured joints (x): the yellow house to -53.3 (and
# its east end on Västra Sjögatan), the link to -56.2, the 1909 house to -77.24, the Frösunda house
# on to -90.9. Depths: 11 m (the yellow house to the courtyard), 7 m (link), 9 m, 11 m.
seeds=[('yl',P62.intersection(box(-53.3,-164.45,-40,-151))),('ln',P62.intersection(box(-56.2,-159,-53.3,-151))),
 ('h9',P62.intersection(box(-77.24,-158.7,-56.2,-151))),('fr',PB.intersection(box(-91.5,-163,-77.24,-151))),
 ('bk62',P62),('bk14',P14)]
# Heights (m) above the facade base: the yellow house's eaves 7.3; the link's parapet 4.4 with a
# glazed storey set back to 5.4; the 1909 house's eaves 4.8, its front gables to 8.3; the Frösunda
# house's eaves 6.8; the courtyard ranges keep the district heights.
spec={'yl':dict(height=7.3,top=10.3),'ln':dict(height=4.4,top=5.6),'h9':dict(height=4.8,top=8.3),'fr':dict(height=6.8,top=9.6),
 'bk62':dict(height=7.3,top=9.5),'bk14':dict(height=6.65,top=8.8)}
for k_,v in spec.items():v['mesh']='SM_Kvarnholmen_House_92379262' if k_ in ('yl','ln','h9','bk62') else 'SM_Kvarnholmen_House_92379314'
taken=Polygon();zones={}
for name,seed in seeds:
 ps=parts(seed.difference(taken));zones[name]=ps;taken=unary_union([taken]+ps)
scope={'92379262','92379314'}
b39=json.loads((R/'source/block39.json').read_text())['zones']
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
out['yl']['roof']=roof_ring('yl',4.0)
r=roof_ring('h9',3.3);ring=[tuple(v) for v in r['outer']]
out['h9']['roof']=r
out['fr']['roof']=roof_ring('fr',4.0)
covered=unary_union([p for ps in zones.values() for p in ps]);foot=PB
data={'source':'district volumes 92379262 and 92379314 (source/district17.json), '+district['source'],'zones':out,
 'checks':{'footprint_m2':round(foot.area,1),'zoned_m2':round(covered.area,1),'outside_osm_m2':round(covered.difference(foot).area,2),'osm_not_zoned_m2':round(foot.difference(covered).area,2),
  'overlap_m2':round(sum(p.area for ps in zones.values() for p in ps)-covered.area,3)}}
(R/'source/block45.json').write_text(json.dumps(data,indent=1,ensure_ascii=False))
c=data['checks'];ok=c['outside_osm_m2']<.2 and c['osm_not_zoned_m2']<.5 and c['overlap_m2']<.2
(R/'previews/block45-zones.json').write_text(json.dumps({'status':'passed' if ok else 'review_required','zones':report,'checks':c},indent=2,ensure_ascii=False))
print(json.dumps(report));print(c);print('BLOCK45_ZONES_OK' if ok else 'BLOCK45_ZONES_REVIEW')
