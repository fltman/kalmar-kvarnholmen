"""Pass 85: Anstalten Kalmar, the prison on the mainland shore west of Västerport (OSM way 91053122,
Ravelinsgatan 2), outside the district model. Writes source/block85.json:
- the ground: the shore between Ravelinsgatan and the coast opposite Västerport (OSM coastline
  90822660), closed inland along a cut line, with the roads and the prison yard;
- the prison outline split into its three ranges: the front range towards the water (south-east,
  with the central pavilion), the long cell range behind it (bearing 30 degrees) and the north range;
- the walls and fences round the yards (OSM barriers), and the Rotunda pavilion by Ravelinsgatan.
Heights from a user panorama on the Västerport bridge and Google Street View on Olof Palmes gata
(view only); see references/block85-notes.md. Run with Shapely: KALMAR_GEO=<site-packages>.
"""
from pathlib import Path
import json,math,os,sys
if os.environ.get('KALMAR_GEO'):sys.path.insert(0,os.environ['KALMAR_GEO'])
from shapely.geometry import Polygon,Point,LineString,box
from shapely.geometry.polygon import orient
from shapely.ops import unary_union
R=Path(__file__).resolve().parents[1]
OSM=json.loads((R/'references/osm-prison85.json').read_text())
def pts(wid):return [tuple(p) for p in OSM[wid]['points']]
def flat(g):
 g=g.buffer(0);return [g] if g.geom_type=='Polygon' else [q for c in getattr(g,'geoms',[]) for q in flat(c)]
def parts(g):return [orient(r) for q in flat(g) for r in flat(q.buffer(-.02,join_style=2).buffer(.02,join_style=2).simplify(.02)) if r.area>5.0]
def ring(g):return [[round(c,3) for c in v] for v in list(orient(g).exterior.coords)[:-1]]
# ---------------------------------------------------------------- ground
coast=pts('90822660')
i0=min(range(len(coast)),key=lambda i:math.dist(coast[i],(-530.6,58.3)));i1=min(range(len(coast)),key=lambda i:math.dist(coast[i],(-414.1,224.2)))
shore=coast[i0:i1+1]
# Inland the patch is cut along a line clear of the prison walls, Ravelinsgatan and the Rotunda.
ground=orient(Polygon(shore+[(-428.0,246.0),(-522.0,214.0),(-546.0,120.0),(-541.0,66.0)]).buffer(0))
assert ground.is_valid and ground.contains(Point(-445,152)) and ground.contains(Point(-521.6,95.5))
def strip(wid,width):return LineString(pts(wid)).buffer(width/2,cap_style=2,join_style=2).intersection(ground)
roads=unary_union([strip('35813670',6.0),strip('91072714',4.0)])
# ---------------------------------------------------------------- the prison
P=Polygon(pts('91053122')).buffer(0)
def band(a,b,depth):
 L=math.dist(a,b);dx,dy=(b[0]-a[0])/L,(b[1]-a[1])/L;nx,ny=-dy,dx
 return Polygon([(a[0]+dx*s+nx*t,a[1]+dy*s+ny*t) for s,t in ((-80,-.5*math.copysign(1,depth)),(80,-.5*math.copysign(1,depth)),(80,depth),(-80,depth))])
# North range: 12 m deep behind its north front (OSM 8 -> 7, west to east; inwards to the south).
NR=P.intersection(band((-423.3,192.5),(-465.8,188.8),12.0))
# Cell range: 13.1 m from its west face (OSM 13 -> 12), the measured distance to the parallel east
# face (OSM 3 -> 4).
CR=P.intersection(band((-468.6,132.7),(-449.2,166.2),-13.1)).difference(NR)
FR=P.difference(NR).difference(CR)
spec={'fr':dict(height=11.0,top=13.4,frame=((-457.7,126.5),(-428.3,146.7))),'cr':dict(height=11.0,top=13.6,frame=((-468.6,132.7),(-449.2,166.2))),
 'nr':dict(height=10.6,top=13.0,frame=((-465.8,188.8),(-423.3,192.5)))}
zones={};taken=Polygon()
for name,seed in (('nr',NR),('cr',CR),('fr',FR)):
 ps=parts(seed.difference(taken));zones[name]=ps;taken=unary_union([taken]+ps)
out={}
for name,ps in zones.items():
 walls=[]
 for poly in ps:
  cs=list(poly.exterior.coords)[:-1]
  for p,q in zip(cs,cs[1:]+cs[:1]):
   if math.dist(p,q)<.2:continue
   mid=((p[0]+q[0])/2,(p[1]+q[1])/2);Lw=math.dist(p,q);nx,ny=(q[1]-p[1])/Lw,-(q[0]-p[0])/Lw
   nb=next((n for n,g in zones.items() if n!=name and any(x.buffer(.05).contains(Point(mid[0]+nx*.3,mid[1]+ny*.3)) for x in g)),None)
   z0=0.0 if nb is None else min(spec[nb]['height'],spec[name]['height'])
   if nb is not None and z0>=spec[name]['height']-.05:continue
   walls.append({'p':[round(c,3) for c in p],'q':[round(c,3) for c in q],'z0':z0,'z1':spec[name]['height'],'kind':'outer' if nb is None else 'upper','neighbour':nb})
 out[name]=dict(spec[name],polygons=[ring(p) for p in ps],walls=walls)
# The yard: inside the walls and fences, outside the building.
yard=Polygon(pts('91053134')[:-1]+pts('91053143')[1:]+[(-428.3,146.7),(-424.5,153.4),(-423.6,180.0),(-423.3,192.5)]).buffer(0).difference(P)
data={'source':'OpenStreetMap (references/osm-prison85.json; ODbL)','ground':{'outer':ring(ground),'shore':[list(p) for p in shore]},
 'roads':[ring(g) for g in flat(roads) if g.area>1],'yard':[ring(g) for g in flat(yard.intersection(ground)) if g.area>1],'zones':out,
 'walls':{'91053134':dict(points=[list(p) for p in pts('91053134')],h=4.5),'91053143':dict(points=[list(p) for p in pts('91053143')],h=3.0),
  '91931334':dict(points=[list(p) for p in pts('91931334')],h=3.0)},
 'fences':{k:[list(p) for p in pts(k)] for k in ('91053120','91053127')},
 'rotunda':dict(points=[list(p) for p in pts('1118433612')[:-1]],h=3.4,top=3.85),
 'checks':{'ground_m2':round(ground.area,1),'prison_m2':round(P.area,1),'zoned_m2':round(unary_union([g for ps in zones.values() for g in ps]).area,1),
  'prison_outside_ground_m2':round(P.difference(ground).area,2),'walls_outside_ground':[k for k in ('91053134','91053143','91931334') if not ground.buffer(.5).contains(LineString(pts(k)))]}}
(R/'source/block85.json').write_text(json.dumps(data,indent=1,ensure_ascii=False))
c=data['checks'];ok=abs(c['zoned_m2']-c['prison_m2'])<6 and c['prison_outside_ground_m2']<.1 and not c['walls_outside_ground']
print({k:(round(sum(Polygon(p).area for p in v['polygons']),1),len(v['walls'])) for k,v in out.items()});print(c);print('BLOCK85_PREP_OK' if ok else 'BLOCK85_PREP_REVIEW')
