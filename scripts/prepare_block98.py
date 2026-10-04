"""Pass 98: the mainland between Kvarnholmen and the castle: Stadsparken (the castle park), the
Krusenstjernska garden, Kalmarsundsparken along the shore, Slottsvägen, Gamla kyrkogården and
Södra kyrkogården, the streets and the
houses of the blocks round them. Until now the castle (pass 27) and the prison patch (pass 85) stood
alone in open water.

Writes source/block98.json from the OpenStreetMap extract references/osm-slott98.json (ODbL):
- the land: the mainland face between the coastlines inside the study box, less the land the model
  already has (Kvarnholmen and the station, the castle island and its ravelin and islets, the
  prison patch);
- road and path strips by highway class, clipped to the land;
- parks and gardens, the two cemeteries with their paths, stone rows and boundary hedges;
- the buildings on that land as footprints with storeys (OSM building:levels, else 2);
- tree positions in the parks and cemeteries, on a jittered grid clear of paths and buildings.
Run with Shapely: KALMAR_GEO=<site-packages> python3 scripts/prepare_block98.py
"""
from pathlib import Path
import json,math,os,sys,random
if os.environ.get('KALMAR_GEO'):sys.path.insert(0,os.environ['KALMAR_GEO'])
from shapely.geometry import Polygon,LineString,Point,box,MultiPolygon
from shapely.geometry.polygon import orient
from shapely.ops import unary_union,polygonize
R=Path(__file__).resolve().parents[1]
O=json.loads((R/'references/osm-slott98.json').read_text())
K=json.loads((R/'source/kvarnholmen.json').read_text())
C27=json.loads((R/'source/castle27.json').read_text())
P85=json.loads((R/'source/block85.json').read_text())
def flat(g):
 g=g.buffer(0)
 if g.is_empty:return []
 return [g] if g.geom_type=='Polygon' else [q for c in getattr(g,'geoms',[]) for q in flat(c)]
def ring(g):return [[round(c,3) for c in v] for v in list(orient(g).exterior.coords)[:-1]]
def piece(g):return {'outer':ring(g),'holes':[[[round(c,3) for c in v] for v in list(h.coords)[:-1]] for h in orient(g).interiors]}
def area_poly(v):
 if 'points' in v and len(v['points'])>=4 and v['points'][0]==v['points'][-1]:return Polygon(v['points']).buffer(0)
 if 'members' in v:
  outer=[m['points'] for m in v['members'] if m['role']=='outer'];inner=[m['points'] for m in v['members'] if m['role']=='inner']
  # Members may be split ways: polygonize joins them.
  P=unary_union(list(polygonize(unary_union([LineString(p) for p in outer if len(p)>1]))))
  if inner:P=P.difference(unary_union(list(polygonize(unary_union([LineString(p) for p in inner if len(p)>1])))))
  return P.buffer(0)
 return None
# ---------------------------------------------------------------- land
BOX=box(-1650,-560,-470,320)
coast=[LineString(v['points']) for v in O.values() if v['tags'].get('natural')=='coastline' and 'points' in v]
faces=list(polygonize(unary_union([BOX.boundary]+[c.intersection(BOX) for c in coast if c.intersects(BOX)])))
land=max(faces,key=lambda f:f.area)
assert land.contains(Point(-898,42)) and land.contains(Point(-1110,-166))
have=[Polygon(g['outer']).buffer(0) for g in K['island_outline']]
have+=[Polygon(g['outer']).buffer(0) for key in ('island',) for g in C27.get(key,[])]
have.append(Polygon(C27['ravelin']['polygon']).buffer(0));have+=[Polygon(i['polygon']).buffer(0) for i in C27['islets']]
have.append(Polygon(P85['ground']['outer']).buffer(0))
land=land.difference(unary_union(have).buffer(.3))
land=max(flat(land),key=lambda g:g.area)
# ---------------------------------------------------------------- roads and paths
W={'primary':10,'secondary':9,'tertiary':8,'residential':6,'unclassified':6,'living_street':5,'service':4,'pedestrian':5,
   'footway':2.5,'path':2.2,'cycleway':2.8,'steps':2.0,'track':3.0}
SOFT={'footway','path','steps','track'}
hard=[];soft=[]
for v in O.values():
 t=v['tags'];hw=t.get('highway')
 if hw not in W or 'points' not in v or len(v['points'])<2 or t.get('area')=='yes':continue
 if t.get('bridge') or t.get('tunnel'):continue
 L=LineString(v['points'])
 if not L.intersects(land):continue
 s=L.buffer(W[hw]/2,cap_style=2,join_style=2).intersection(land)
 (soft if hw in SOFT else hard).append(s)
HARD=unary_union(hard);SOFTU=unary_union(soft).difference(HARD)
# ---------------------------------------------------------------- parks, gardens, cemeteries
greens=[];cems={}
for k,v in O.items():
 t=v['tags']
 if t.get('landuse')=='cemetery' or t.get('amenity')=='grave_yard':
  P=area_poly(v)
  if P is not None and P.intersects(land):cems[t.get('name') or ('Södra kyrkogården' if P.centroid.x<-1000 else k)]=P.intersection(land)
 elif t.get('leisure') in ('park','garden','common') or t.get('landuse') in ('grass','village_green','flowerbed') or t.get('natural') in ('grassland','scrub'):
  P=area_poly(v)
  if P is not None and P.intersects(land):greens.append((t.get('name') or '',t.get('landuse') or t.get('leisure') or t.get('natural'),P.intersection(land)))
# ---------------------------------------------------------------- buildings
bld=[]
for k,v in O.items():
 t=v['tags']
 if 'building' not in t or 'points' not in v:continue
 P=area_poly(v)
 if P is None or P.is_empty or P.area<6 or not land.buffer(.5).contains(P.centroid):continue
 lv=t.get('building:levels');h=t.get('height')
 try:levels=max(1,min(8,int(float(lv))))
 except:levels=1 if P.area<60 else 2
 try:H=float(str(h).split()[0])
 except:H=None
 for g in flat(P.intersection(land)):
  if g.area>4:bld.append({'id':k[1:],'name':t.get('name',''),'kind':t.get('building'),'levels':levels,'height':H,'outer':ring(g.simplify(.05))})
BLD=unary_union([Polygon(b['outer']) for b in bld]) if bld else Polygon()
# ---------------------------------------------------------------- trees and grave rows
rng=random.Random(98)
def scatter(P,step,keep):
 x0,y0,x1,y1=P.bounds;out=[]
 for i in range(int((x1-x0)/step)+1):
  for j in range(int((y1-y0)/step)+1):
   x=x0+i*step+rng.uniform(-.35,.35)*step;y=y0+j*step+rng.uniform(-.35,.35)*step
   pt=Point(x,y)
   if P.contains(pt) and not keep.contains(pt):out.append([round(x,2),round(y,2),round(rng.uniform(.8,1.25),3)])
 return out
clear=unary_union([HARD.buffer(2.5),SOFTU.buffer(1.8),BLD.buffer(3.0)])
# Mapped trees first (OSM natural=tree nodes on the land), then the jittered fill keeps clear of them.
trees=[[v['point'][0],v['point'][1],1.0] for v in O.values() if v['tags'].get('natural')=='tree' and 'point' in v and land.contains(Point(v['point'])) and not clear.contains(Point(v['point']))]
clear=unary_union([clear]+[Point(t[0],t[1]).buffer(7) for t in trees])
for name,kind,P in greens:
 if kind in ('park','garden','common','village_green','grassland','scrub'):trees+=scatter(P,13.0,clear)
for name,P in cems.items():trees+=scatter(P,16.0,clear)
graves=[]
for name,P in cems.items():
 # Rows of stones on a grid aligned with the cemetery's longest edge, clear of paths and buildings.
 r=orient(P.minimum_rotated_rectangle) if P.area>0 else None
 cs=list(r.exterior.coords)[:-1];e=max(zip(cs,cs[1:]+cs[:1]),key=lambda pq:math.dist(*pq))
 a=math.atan2(e[1][1]-e[0][1],e[1][0]-e[0][0]);ca,sa=math.cos(a),math.sin(a)
 inner=P.buffer(-3).difference(unary_union([SOFTU.buffer(1.4),HARD.buffer(1.8),BLD.buffer(1.5)]))
 cx,cy=P.centroid.x,P.centroid.y;Rr=math.hypot(P.bounds[2]-P.bounds[0],P.bounds[3]-P.bounds[1])/2
 u=-Rr
 while u<Rr:
  w=-Rr
  while w<Rr:
   x=cx+u*ca-w*sa;y=cy+u*sa+w*ca
   if inner.contains(Point(x,y)) and rng.random()<.82:graves.append([round(x,2),round(y,2),round(math.degrees(a),1),rng.randrange(3)])
   w+=2.6
  u+=1.5
rd=lambda g:[piece(q) for q in flat(g) if q.area>.5]
data={'source':'OpenStreetMap (references/osm-slott98.json; ODbL), coastline faces inside the box x -1650..-470, y -560..320',
 'land':rd(land),'shore':[[[round(c,3) for c in p] for p in list(c.intersection(land.buffer(.6)).coords)] for c in coast if c.intersects(land.buffer(.6)) and c.intersection(land.buffer(.6)).geom_type=='LineString'],
 'roads':rd(HARD),'paths':rd(SOFTU),'greens':[{'name':n,'kind':k,'pieces':rd(P)} for n,k,P in greens],
 'cemeteries':[{'name':n,'pieces':rd(P),'edge':[ring(q) for q in flat(P) if q.area>20]} for n,P in cems.items()],
 'buildings':bld,'trees':trees,'graves':graves,
 'checks':{'land_m2':round(land.area),'roads_m2':round(HARD.area),'paths_m2':round(SOFTU.area),'cemeteries':{n:round(P.area) for n,P in cems.items()},
  'buildings':len(bld),'trees':len(trees),'graves':len(graves)}}
(R/'source/block98.json').write_text(json.dumps(data,ensure_ascii=False))
c=data['checks'];ok=c['land_m2']>100000 and len(cems)>=2 and c['buildings']>0
print(c);print('BLOCK98_PREP_OK' if ok else 'BLOCK98_PREP_REVIEW')
