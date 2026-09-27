"""Pass 44: the district volume 92412862 at Västra Sjögatan and Ölandsgatan, south of pass 39: the
17th-century stone corner house (roughcast, pilasters, a sandstone portal on Ölandsgatan, a curved
baroque gable to Västra Sjögatan and a stepped gable to the east, a tile roof with two dormers), the
white roughcast house 2 Västra Sjögatan, the yellow wooden house on Ölandsgatan with its dormer, and
the plain courtyard wings. Heights come from Google Street View panoramas (April 2025), chained per
street and anchored on the corners and joints; see references/block44-notes.md.
Run with Shapely on the path: KALMAR_GEO=/path/to/site-packages python3 prepare_block44.py
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
PB=Polygon([tuple(w['p']) for w in d17['SM_Kvarnholmen_House_92412862']['walls']]).buffer(0)
seeds=[('ch',PB.intersection(box(-30,-142,-12.6,-128.55))),('wh',PB.intersection(box(-30,-128.55,-22.0,-116.0))),
 ('yh',PB.intersection(box(-9.1,-142,3,-134.4))),('bk',PB)]
# Heights (m) above the facade base: the corner house's cornice 9.5 and its ridge 17.9 (the gables'
# apex, triangulated from the pitched views); the white house's eaves 9.0; the yellow wooden house's
# eaves 4.6 under a hipped roof; the courtyard wings keep the district height.
spec={'ch':dict(height=9.5,top=17.9),'wh':dict(height=9.0,top=12.8),'yh':dict(height=4.6,top=7.4),'bk':dict(height=7.0,top=9.6)}
for v in spec.values():v['mesh']='SM_Kvarnholmen_House_92412862'
taken=Polygon();zones={}
for name,seed in seeds:
 ps=parts(seed.difference(taken));zones[name]=ps;taken=unary_union([taken]+ps)
scope={'92412862'}
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
# The corner house: gables on its short (north-south) ends, so its roof ring is inset only on the long
# sides (nearly to the ridge); the white house hips to the street; the yellow house is hipped.
r=roof_ring('ch',6.2);ring=[tuple(v) for v in r['outer']]
fire=[abs(q[0]-p[0])<abs(q[1]-p[1]) for p,q in zip(ring,ring[1:]+ring[:1])]
r['firewall']=fire;r['r1']=[list(v) for v in inner(ring,[0 if f else 6.2 for f in fire])];r['inset']=6.2;out['ch']['roof']=r
r=roof_ring('wh',3.4);ring=[tuple(v) for v in r['outer']]
fire=[abs(q[0]-p[0])>abs(q[1]-p[1]) for p,q in zip(ring,ring[1:]+ring[:1])]
r['firewall']=fire;r['r1']=[list(v) for v in inner(ring,[0 if f else 3.4 for f in fire])];r['inset']=3.4;out['wh']['roof']=r
out['yh']['roof']=roof_ring('yh',3.1)
covered=unary_union([p for ps in zones.values() for p in ps]);foot=PB
data={'source':'district volume 92412862 (source/district17.json), '+district['source'],'zones':out,
 'checks':{'footprint_m2':round(foot.area,1),'zoned_m2':round(covered.area,1),'outside_osm_m2':round(covered.difference(foot).area,2),'osm_not_zoned_m2':round(foot.difference(covered).area,2),
  'overlap_m2':round(sum(p.area for ps in zones.values() for p in ps)-covered.area,3)}}
(R/'source/block44.json').write_text(json.dumps(data,indent=1,ensure_ascii=False))
c=data['checks'];ok=c['outside_osm_m2']<.2 and c['osm_not_zoned_m2']<.5 and c['overlap_m2']<.2
(R/'previews/block44-zones.json').write_text(json.dumps({'status':'passed' if ok else 'review_required','zones':report,'checks':c},indent=2,ensure_ascii=False))
print(json.dumps(report));print(c);print('BLOCK44_ZONES_OK' if ok else 'BLOCK44_ZONES_REVIEW')
