"""Pass 102: the far east end of Storgatan (district volumes 93238165, 93238196, 93238164, 93238222,
93199630, 93199675 and 93199606):
- north side, fronts facing south:
  - 93238165 (69): the cream rendered three-storey house with balconies and a carriage gate (west)
    and the cream rendered two-storey house with three red gabled dormers (east), split at the
    joint seen in the photo; the unseen rear parts low and flat;
  - 93238196: two small red boarded gable houses with a blue gate between them, and a low rear part;
  - 93238164: the grey-green boarded two-storey house under a red tiled saddle roof, low rear wing;
  - 93238222: the cream rendered corner house at Östra Vallgatan (under scaffolding in the photos);
- south side, fronts facing north:
  - 93199630 (67): the ochre rendered two-storey house with a lesene and a red door;
  - 93199675: the low garage range with five red doors under a tiled hipped roof, and its long
    unseen rear part;
- 93199606: the brown brick two-storey house on a stone base with shutters and a low hipped copper
  roof, its east front on Östra Vallgatan; split into the east block (15 m front), the Storgatan
  block (its west face seen at about x 364.5 from the garage panorama) and a low walled part west
  of it behind the brick wall on Storgatan.
Heights from four resected Google Street View panoramas (see references/block102-notes.md).
Run with Shapely: KALMAR_GEO=<site-packages> python3 scripts/prepare_block102.py
"""
from pathlib import Path
import json,math,os,sys
if os.environ.get('KALMAR_GEO'):sys.path.insert(0,os.environ['KALMAR_GEO'])
from shapely.geometry import Polygon,Point,box as sbox
from shapely.geometry.polygon import orient
from shapely.ops import unary_union
R=Path(__file__).resolve().parents[1]
district=json.loads((R/'source/kvarnholmen.json').read_text())
d17=json.loads((R/'source/district17.json').read_text())['buildings']
def flat(g):
 g=g.buffer(0);return [g] if g.geom_type=='Polygon' else [q for c in getattr(g,'geoms',[]) for q in flat(c)]
def parts(g):return [orient(r) for q in flat(g) for r in flat(q.buffer(-.02,join_style=2).buffer(.02,join_style=2).simplify(.02)) if r.area>1.0]
IDS=['93238165','93238196','93238164','93238222','93199630','93199675','93199606']
MESH={i:'SM_Kvarnholmen_House_'+i for i in IDS}
for i in IDS:
 assert MESH[i] in d17,MESH[i]
 assert (d17[MESH[i]].get('detail_pass') or 17)<=17,MESH[i]
ring=lambda i:[tuple(w['p']) for w in d17[MESH[i]]['walls']]
PG={i:Polygon(ring(i)).buffer(0) for i in IDS}
for i in IDS:assert PG[i].is_valid and PG[i].geom_type=='Polygon',i
# Cuts as axis boxes in the local frame (the street fronts here run within 1.3 degrees of x).
X=lambda x0,x1,y0=-80,y1=80:sbox(x0,y0,x1,y1)
GEO={}
P=PG['93238165']
GEO['t165']=P.intersection(X(300,343.6,-5,8.0))      # three-storey part, west of the seen joint
GEO['t165b']=P.intersection(X(300,343.6,8.0,40))     # its rear bits (not seen)
GEO['c165']=P.intersection(X(343.6,400,-5,8.3))      # two-storey with dormers
GEO['c165b']=P.intersection(X(343.6,400,8.3,40))     # rear wing (not seen)
P=PG['93238196']
GEO['r196a']=P.intersection(X(300,359.85,-5,9.3))    # west red gable house
GEO['r196g']=P.intersection(X(359.85,361.7,-5,9.3))  # the blue gate and the yard behind it
GEO['r196b']=P.intersection(X(361.7,400))            # east red gable house
GEO['r196c']=P.difference(unary_union([GEO['r196a'],GEO['r196g'],GEO['r196b']]))
P=PG['93238164']
GEO['g164']=P.intersection(X(300,400,-5,6.38))
GEO['g164b']=P.difference(GEO['g164'])
GEO['k222']=PG['93238222']
GEO['o630']=PG['93199630']
P=PG['93199675']
GEO['p675']=P.intersection(X(300,400,-23.9,0))
GEO['p675b']=P.difference(GEO['p675'])
P=PG['93199606']
GEO['b606e']=P.intersection(X(378.3,400))
GEO['b606w']=P.intersection(X(364.5,378.3))         # west face seen at about x 364.5 (garage pano)
GEO['b606y']=P.difference(unary_union([GEO['b606e'],GEO['b606w']]))  # walled yard / outbuilding
# Heights (m) above the street: eaves 'height', ridge 'top'. est = not seen, estimated.
# roof: 'gable_street' ridge at right angles to the street front; 'saddle' ridge along it; 'hip';
# 'flat'.
spec={
 't165':dict(height=8.20,top=9.60,roof='hip',osm='93238165'),
 't165b':dict(height=6.00,top=6.00,roof='flat',osm='93238165',est=True),
 'c165':dict(height=5.60,top=9.30,roof='saddle',osm='93238165'),
 'c165b':dict(height=5.60,top=5.60,roof='flat',osm='93238165',est=True),
 'r196a':dict(height=4.50,top=6.20,roof='gable_street',osm='93238196'),
 'r196g':dict(height=3.30,top=3.30,roof='flat',osm='93238196'),
 'r196b':dict(height=3.90,top=5.60,roof='gable_street',osm='93238196'),
 'r196c':dict(height=3.00,top=3.00,roof='flat',osm='93238196',est=True),
 'g164':dict(height=5.95,top=9.00,roof='saddle',osm='93238164'),
 'g164b':dict(height=4.00,top=4.00,roof='flat',osm='93238164',est=True),
 'k222':dict(height=7.30,top=10.20,roof='hip',osm='93238222'),
 'o630':dict(height=7.80,top=11.00,roof='saddle',osm='93199630'),
 'p675':dict(height=3.25,top=5.30,roof='hip',osm='93199675'),
 'p675b':dict(height=3.00,top=3.00,roof='flat',osm='93199675',est=True),
 'b606e':dict(height=9.00,top=10.60,roof='hip',osm='93199606'),
 'b606w':dict(height=9.00,top=10.80,roof='hip',osm='93199606'),
 'b606y':dict(height=2.60,top=2.60,roof='flat',osm='93199606',est=True),
}
for z in spec:spec[z]['mesh']=MESH[spec[z]['osm']]
taken=Polygon();zones={}
for name in spec:
 ps=parts(GEO[name].difference(taken));zones[name]=ps;taken=unary_union([taken]+ps)
 assert ps,name
scope=set(IDS)
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
foot=unary_union(list(PG.values()));covered=unary_union([p for ps in zones.values() for p in ps])
data={'source':'district volumes '+', '.join(IDS)+' (source/district17.json), '+district['source'],'zones':out,
 'checks':{'footprint_m2':round(foot.area,1),'zoned_m2':round(covered.area,1),'outside_osm_m2':round(covered.difference(foot).area,2),'osm_not_zoned_m2':round(foot.difference(covered).area,2),
  'overlap_m2':round(sum(p.area for ps in zones.values() for p in ps)-covered.area,3)}}
(R/'source/block102.json').write_text(json.dumps(data,indent=1,ensure_ascii=False))
c=data['checks'];ok=c['outside_osm_m2']<.2 and c['osm_not_zoned_m2']<.5 and c['overlap_m2']<.2
(R/'previews/block102-zones.json').write_text(json.dumps({'status':'passed' if ok else 'review_required','zones':report,'checks':c},indent=2,ensure_ascii=False))
print(json.dumps(report));print(c);print('BLOCK102_ZONES_OK' if ok else 'BLOCK102_ZONES_REVIEW')
