"""Pass 32: Larmgatan 22 and 24 (OSM 92204181, 92204160), north of Storgatan.

Larmgatan 22: a pale green two-storey house: two wide segmental-arched shop windows and a round-
arched door, a plain frieze (its historic shop lettering omitted), five upper windows in beige
surrounds, a cornice with a low railing and two arched dormers. Larmgatan 24: a white house of
three storeys: shop fronts, balconies with wrought-iron railings over the middle three of seven
axes on both upper floors, pediments over the middle first-floor windows, panels under the
others, a dentilled main cornice and three attic dormers. Behind both front ranges lower courtyard
wings. Heights come from two Google Street View panoramas (April 2025) straight in front of the
houses, each registered on its house's two OSM joints; see references/block32-notes.md.
Run with Shapely on the path: KALMAR_GEO=/path/to/site-packages python3 prepare_block32.py
"""
from pathlib import Path
import json,math,os,sys
if os.environ.get('KALMAR_GEO'):sys.path.insert(0,os.environ['KALMAR_GEO'])
from shapely.geometry import Polygon,Point,box
from shapely.geometry.polygon import orient
from shapely.ops import unary_union
R=Path(__file__).resolve().parents[1]
district=json.loads((R/'source/kvarnholmen.json').read_text());B={b['id']:b for b in district['buildings']}
def ring(bid):
 r=[tuple(p) for p in B[bid]['polygons'][0]['outer']]
 return r[:-1] if r[0]==r[-1] else r
def flat(g):
 g=g.buffer(0);return [g] if g.geom_type=='Polygon' else [q for c in getattr(g,'geoms',[]) for q in flat(c)]
def parts(g):return [orient(r) for q in flat(g) for r in flat(q.buffer(-.02,join_style=2).buffer(.02,join_style=2).simplify(.02)) if r.area>1.0]
P22,P24=(Polygon(ring(b)).buffer(0) for b in ('92204181','92204160'))
# Front ranges: Larmgatan 22 is 10 m deep (to its courtyard notch at x -275.0), Larmgatan 24 about
# 12 m (its side walls rise above the neighbours that far). The rest are courtyard wings.
F22,F24=-275.0,-273.0
seeds=[('l22',P22.intersection(box(-300,0,F22,40))),('l22r',P22.difference(box(-300,0,F22,40))),
 ('l24',P24.intersection(box(-300,20,F24,60))),('l24r',P24.difference(box(-300,20,F24,60)))]
# Heights (m) above the Larmgatan facade base (camera height 2.48 m, as on the other Larmgatan
# panoramas; the bases themselves are hidden by terraces). Larmgatan 22: shop-floor cornice 3.8,
# frieze 4.0-4.5, upper windows 4.9-6.6, cornice 7.2-7.5 after allowing for its projection, a
# railing to about 7.85, dormers to about 9.45. Larmgatan 24: shop-floor cornice 3.8-4.3,
# windows 5.10-7.12 and 8.94-11.11, cornice 11.6-12.6 after allowing for its projection, attic
# dormers standing just behind the wall line with their caps at about 15.2 (on the sight line over the
# cornice). The roofs behind the cornices are not visible from the street and, like
# the wings, are estimates.
spec={'l22':dict(height=7.5,top=10.5,mesh='SM_Kvarnholmen_House_92204181'),
 'l22r':dict(height=6.0,top=7.8,mesh='SM_Kvarnholmen_House_92204181'),
 'l24':dict(height=12.6,top=15.1,mesh='SM_Kvarnholmen_House_92204160'),
 'l24r':dict(height=7.0,top=9.0,mesh='SM_Kvarnholmen_House_92204160')}
taken=Polygon();zones={}
for name,seed in seeds:
 ps=parts(seed.difference(taken));zones[name]=ps;taken=unary_union([taken]+ps)
scope={'92204181','92204160'}
others=[(Polygon(ring(b['id'])).buffer(0),b['height'],b['id']) for b in district['buildings'] if b['id'] not in scope]
sg=json.loads((R/'source/storgatan.json').read_text())['buildings'];d17=json.loads((R/'source/district17.json').read_text())['buildings']
others+=[(Polygon(b['polygon']).buffer(0),d17.get('SM_Building_'+b['id'],{}).get('H',8.0),'storgatan:'+b['id']) for b in sg if b.get('polygon')]
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
   ux,uy=(q[0]-p[0])/Lw,(q[1]-p[1])/Lw;nx,ny=uy,-ux;n=max(1,int(Lw/.2));runs=[]
   for k in range(n):
    t=(k+.5)/n;nb,h=neighbour_at(Point(p[0]+ux*Lw*t+nx*.3,p[1]+uy*Lw*t+ny*.3))
    if runs and runs[-1][0]==nb:runs[-1][3]=(k+1)/n
    else:runs.append([nb,h,k/n,(k+1)/n])
   for nb,h,t0,t1 in runs:
    z0=0.0 if nb is None else h
    if z0>=H-.05:continue
    a=(round(p[0]+ux*Lw*t0,3),round(p[1]+uy*Lw*t0,3));b=(round(p[0]+ux*Lw*t1,3),round(p[1]+uy*Lw*t1,3))
    if math.dist(a,b)<.2:continue
    walls.append({'p':list(a),'q':list(b),'z0':z0,'z1':H,'kind':'outer' if nb is None else 'upper','neighbour':nb})
 out[name]=dict(spec[name],polygons=[[list(v) for v in list(p.exterior.coords)[:-1]] for p in ps],walls=walls)
 report[name]={'area_m2':round(sum(p.area for p in ps),1),'polygons':len(ps),'walls':len(walls),'outer_m':round(sum(math.dist(w['p'],w['q']) for w in walls if w['kind']=='outer'),1)}
# Roofs of the two front ranges: slopes to the street and the courtyard, gable (fire) walls at the
# party walls. Rings from the ranges' four corners.
def inner(ring,insets):
 lines=[]
 for (p,q),d in zip(zip(ring,ring[1:]+ring[:1]),insets):
  L=math.dist(p,q);ux,uy=(q[0]-p[0])/L,(q[1]-p[1])/L;nx,ny=-uy,ux
  lines.append(((p[0]+nx*d,p[1]+ny*d),(ux,uy)))
 pts=[]
 for i in range(len(ring)):
  (p1,d1),(p2,d2)=lines[i-1],lines[i];det=d1[0]*(-d2[1])-d1[1]*(-d2[0])
  t=((p2[0]-p1[0])*(-d2[1])-(p2[1]-p1[1])*(-d2[0]))/det;pts.append((round(p1[0]+d1[0]*t,3),round(p1[1]+d1[1]*t,3)))
 return pts
roofs={'l22':([(-285.12,16.65),(F22,16.56),(F22,28.82),(-285.01,28.91)],4.5),'l24':([(-285.01,28.91),(F24,28.80),(F24,44.50),(-284.86,44.61)],5.0)}
for name,(fr,ins) in roofs.items():
 fw=[True,False,True,False]            # south side, courtyard side, north side, street side (CCW)
 r1=inner(fr,[0 if f else ins for f in fw])
 g=Polygon(r1);assert g.is_valid and g.area<Polygon(fr).area and Polygon(fr).buffer(.01).contains(g),name
 out[name]['roof']=dict(outer=[list(v) for v in fr],r1=[list(v) for v in r1],firewall=fw,inset=ins)
covered=unary_union([p for ps in zones.values() for p in ps]);foot=P22.union(P24)
data={'source':'OpenStreetMap ways 92204181, 92204160, '+district['source'],'zones':out,
 'checks':{'footprint_m2':round(foot.area,1),'zoned_m2':round(covered.area,1),'outside_osm_m2':round(covered.difference(foot).area,2),'osm_not_zoned_m2':round(foot.difference(covered).area,2),
  'overlap_m2':round(sum(p.area for ps in zones.values() for p in ps)-covered.area,3)}}
(R/'source/block32.json').write_text(json.dumps(data,indent=1,ensure_ascii=False))
c=data['checks'];ok=c['outside_osm_m2']<.2 and c['osm_not_zoned_m2']<.5 and c['overlap_m2']<.2
(R/'previews/block32-zones.json').write_text(json.dumps({'status':'passed' if ok else 'review_required','zones':report,'checks':c},indent=2,ensure_ascii=False))
print(json.dumps(report));print(c);print('BLOCK32_ZONES_OK' if ok else 'BLOCK32_ZONES_REVIEW')
