"""Pass 34: the three low houses on Södra Långgatan east of number 16 (OSM 92379287, 92379267,
92379282): the white house with the Blanc shop (house number 18 over its door), the yellow house
number 21 and the cream house with its long shop front. Each is split into a two-storey front range
on the street and lower ranges behind it. Heights come from Google Street View panoramas (April
2025), each registered on the house's own OSM joints; the third house is seen only obliquely, from
both sides. See references/block34-notes.md.
Run with Shapely on the path: KALMAR_GEO=/path/to/site-packages python3 prepare_block34.py
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
P18,P21,P23=(Polygon(ring(b)).buffer(0) for b in ('92379287','92379267','92379282'))
# The front ranges are about 10 m deep (the courtyard notches of 92379267 and 92379282 lie at
# y -58.6 and -57.3); everything behind them is a lower rear range.
FRONT=box(-160,-70,-110,-58.6)
seeds=[('b18',P18.intersection(FRONT)),('b18r',P18.difference(FRONT)),('y21',P21.intersection(FRONT)),('y21r',P21.difference(FRONT)),('c23',P23.intersection(FRONT)),('c23r',P23.difference(FRONT))]
# Heights (m) above each house's facade base, flat features from the facade plane, the eaves
# corrected for their small projection. The Blanc house: band 3.06-3.28, windows 3.88-5.36, eaves
# board 5.63-6.08, gutter 6.31 on the plane (6.08, the calibration view). The yellow house: band 2.88-3.19, windows
# 3.61-4.79, eaves board 5.44-5.71, gutter 6.16 on the plane (5.9). The cream house (two oblique
# views): windows 3.5-5.5, eaves 6.2-6.4 on the plane (6.15). Roof tops and the rear ranges are
# estimates.
spec={'b18':dict(height=6.08,top=9.5,mesh='SM_Kvarnholmen_House_92379287'),
 'b18r':dict(height=5.2,top=7.4,mesh='SM_Kvarnholmen_House_92379287'),
 'y21':dict(height=5.9,top=9.3,mesh='SM_Kvarnholmen_House_92379267'),
 'y21r':dict(height=5.0,top=7.0,mesh='SM_Kvarnholmen_House_92379267'),
 'c23':dict(height=6.15,top=9.4,mesh='SM_Kvarnholmen_House_92379282'),
 'c23r':dict(height=5.2,top=7.2,mesh='SM_Kvarnholmen_House_92379282')}
taken=Polygon();zones={}
for name,seed in seeds:
 ps=parts(seed.difference(taken));zones[name]=ps;taken=unary_union([taken]+ps)
scope={'92379287','92379267','92379282'}
b33=json.loads((R/'source/block33.json').read_text())['zones']['sl16']
others=[(Polygon(b33['polygons'][0]).buffer(0),b33['height'],'block33:sl16')]
others+=[(Polygon(ring(b['id'])).buffer(0),b['height'],b['id']) for b in district['buildings'] if b['id'] not in scope|{'92379302'}]
sg=json.loads((R/'source/storgatan.json').read_text())['buildings'];d17=json.loads((R/'source/district17.json').read_text())['buildings']
others+=[(Polygon(b['polygon']).buffer(0),d17.get('SM_Building_'+b['id'],{}).get('H',8.0),'storgatan:'+b['id']) for b in sg if b.get('polygon')]
# The authored neighbour to the east (SM_Building_92379276, height 7.1) is kept from district17.
w276=d17['SM_Building_92379276']['walls'];ring276=[tuple(w['p']) for w in w276]
if len(ring276)>=3:others.append((Polygon(ring276).buffer(0),d17['SM_Building_92379276'].get('H',7.1),'district17:92379276'))
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
# Front-range roofs: slopes to the street and the courtyard, fire walls at the party walls.
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
fronts={'b18':[(-152.28,-68.56),(-140.20,-68.63),(-140.20,-58.6),(-152.22,-58.6)],
 'y21':[(-140.20,-68.63),(-129.03,-68.47),(-129.03,-58.6),(-140.20,-58.6)],
 'c23':[(-129.03,-68.47),(-117.06,-68.77),(-117.06,-58.6),(-129.03,-58.6)]}
for name,fr in fronts.items():
 fw=[False,True,False,True]            # street side, east party wall, courtyard side, west party wall (CCW)
 r1=inner(fr,[0 if f else 4.9 for f in fw])
 g=Polygon(r1);assert g.is_valid and g.area<Polygon(fr).area and Polygon(fr).buffer(.01).contains(g),name
 out[name]['roof']=dict(outer=[list(v) for v in fr],r1=[list(v) for v in r1],firewall=fw,inset=4.9)
covered=unary_union([p for ps in zones.values() for p in ps]);foot=unary_union([P18,P21,P23])
data={'source':'OpenStreetMap ways 92379287, 92379267, 92379282, '+district['source'],'zones':out,
 'checks':{'footprint_m2':round(foot.area,1),'zoned_m2':round(covered.area,1),'outside_osm_m2':round(covered.difference(foot).area,2),'osm_not_zoned_m2':round(foot.difference(covered).area,2),
  'overlap_m2':round(sum(p.area for ps in zones.values() for p in ps)-covered.area,3)}}
(R/'source/block34.json').write_text(json.dumps(data,indent=1,ensure_ascii=False))
c=data['checks'];ok=c['outside_osm_m2']<.2 and c['osm_not_zoned_m2']<.5 and c['overlap_m2']<.2
(R/'previews/block34-zones.json').write_text(json.dumps({'status':'passed' if ok else 'review_required','zones':report,'checks':c},indent=2,ensure_ascii=False))
print(json.dumps(report));print(c);print('BLOCK34_ZONES_OK' if ok else 'BLOCK34_ZONES_REVIEW')
