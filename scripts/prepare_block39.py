"""Pass 39: three district volumes on the south side of Södra Långgatan, east of Västra Sjögatan
(92412832, 92412859 and 92412869): the yellow wooden corner house with its long front on Västra
Sjögatan, the salmon-rendered house of Kalmar Stadsmission and the grey wooden house. Heights come
from Google Street View panoramas (April 2025), registered on the houses' joints and corners; see
references/block39-notes.md.
Run with Shapely on the path: KALMAR_GEO=/path/to/site-packages python3 prepare_block39.py
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
PY=Polygon(dring('92412832')).buffer(0);PS=Polygon(dring('92412859')).buffer(0);PG=Polygon(dring('92412869')).buffer(0)
REAR_Y=box(-18.77,-106,-13.0,-98.86)            # the yellow house's low rear part beside the courtyard
seeds=[('yl',PY.difference(REAR_Y)),('yr',PY.intersection(REAR_Y)),
 ('sa',PS.intersection(box(-14,-91.0,3.5,-80))),('sar',PS.difference(box(-14,-91.0,3.5,-80))),
 ('gr',PG)]
# Heights (m) above each house's facade base.
# The yellow corner house: two storeys of vertical boarding, the eaves cornice's top at 7.3 (the
# frieze's foot 6.9), a steep tile roof hipped round the corner (the ridge 12.3-12.6 m from panorama
# "34", taken at 12.6: a pitch of about 56 degrees). The salmon house: two storeys of
# render, the wall to 7.45 under a cornice whose top (7.70) was triangulated from two panoramas; a
# low roof behind it. The grey wooden house: two storeys, the eaves at 6.95, a sheet-metal roof
# rising at about 41 degrees (its ridge line and chimney seen over the eaves from panorama "39").
spec={'yl':dict(height=7.3,top=12.6,mesh='SM_Building_92412832'),
 'yr':dict(height=5.6,top=7.0,mesh='SM_Building_92412832'),
 'sa':dict(height=7.45,top=8.9,mesh='SM_Building_92412859'),
 'sar':dict(height=6.4,top=7.6,mesh='SM_Building_92412859'),
 'gr':dict(height=6.95,top=11.35,mesh='SM_Building_92412869')}
taken=Polygon();zones={}
for name,seed in seeds:
 ps=parts(seed.difference(taken));zones[name]=ps;taken=unary_union([taken]+ps)
scope={'92412832','92412859','92412869'}
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
out['yl']['roof']=roof_ring('yl',3.6)
out['sa']['roof']=roof_ring('sa',4.5)
out['gr']['roof']=roof_ring('gr',5.0)
covered=unary_union([p for ps in zones.values() for p in ps]);foot=unary_union([PY,PS,PG])
data={'source':'district volumes 92412832, 92412859 and 92412869 (source/district17.json), '+district['source'],'zones':out,
 'checks':{'footprint_m2':round(foot.area,1),'zoned_m2':round(covered.area,1),'outside_osm_m2':round(covered.difference(foot).area,2),'osm_not_zoned_m2':round(foot.difference(covered).area,2),
  'overlap_m2':round(sum(p.area for ps in zones.values() for p in ps)-covered.area,3)}}
(R/'source/block39.json').write_text(json.dumps(data,indent=1,ensure_ascii=False))
c=data['checks'];ok=c['outside_osm_m2']<.2 and c['osm_not_zoned_m2']<.5 and c['overlap_m2']<.2
(R/'previews/block39-zones.json').write_text(json.dumps({'status':'passed' if ok else 'review_required','zones':report,'checks':c},indent=2,ensure_ascii=False))
print(json.dumps(report));print(c);print('BLOCK39_ZONES_OK' if ok else 'BLOCK39_ZONES_REVIEW')
