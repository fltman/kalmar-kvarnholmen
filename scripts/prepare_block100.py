"""Pass 100: the north side of east Norra Långgatan, house numbers 78-84, and the grey cottage on
Östra Vallgatan (district volumes 93238210, 93238172, 93238187, 93238156 and 93238202):
- 93238210: two grey boarded gable cottages (the corner cottage at Landshövdingegatan and the
  taller gable house to the east) joined by a low middle part round a small yard;
- 93238172: the red boarded two-storey house (80) with its low rear wing;
- 93238187: the pale yellow rendered two-storey house (82) with three black dormers, and its rear
  stair tower;
- 93238156: the cream rendered three-storey house (84) with its bay and curved gable, and its
  long flat-roofed rear wing;
- 93238202: the pale grey cottage on Östra Vallgatan, gable to the street, and its unseen west
  parts.
Heights from five resected Google Street View panoramas (see references/block100-notes.md).

OSM way 93238210 is stored in district17 as one self-crossing ring: its small inner yard is
spliced into the outer ring. Here it is taken as the outer ring alone (the eight vertices that
close round the street notch); the inner yard (7 m2) is roofed over with the middle part.
Run with Shapely: KALMAR_GEO=<site-packages> python3 scripts/prepare_block100.py
"""
from pathlib import Path
import json,math,os,sys
if os.environ.get('KALMAR_GEO'):sys.path.insert(0,os.environ['KALMAR_GEO'])
from shapely.geometry import Polygon,Point
from shapely.geometry.polygon import orient
from shapely.ops import unary_union
R=Path(__file__).resolve().parents[1]
district=json.loads((R/'source/kvarnholmen.json').read_text())
d17=json.loads((R/'source/district17.json').read_text())['buildings']
def flat(g):
 g=g.buffer(0);return [g] if g.geom_type=='Polygon' else [q for c in getattr(g,'geoms',[]) for q in flat(c)]
def parts(g):return [orient(r) for q in flat(g) for r in flat(q.buffer(-.02,join_style=2).buffer(.02,join_style=2).simplify(.02)) if r.area>1.0]
IDS=['93238210','93238172','93238187','93238156','93238202']
MESH={i:'SM_Kvarnholmen_House_'+i for i in IDS}
for i in IDS:assert MESH[i] in d17,MESH[i]
ring=lambda i:[tuple(w['p']) for w in d17[MESH[i]]['walls']]
PG={i:Polygon(ring(i)).buffer(0) for i in IDS}
r210=ring('93238210');assert len(r210)==12
PG['93238210']=Polygon(r210[:8])
assert PG['93238210'].is_valid
def half(p,q,left=True):
 # The half-plane to the left (or right) of the infinite line p->q, as a large polygon.
 L=math.dist(p,q);d=((q[0]-p[0])/L,(q[1]-p[1])/L);n=(-d[1],d[0]) if left else (d[1],-d[0]);k=500
 a=(p[0]-d[0]*k,p[1]-d[1]*k);b=(p[0]+d[0]*k,p[1]+d[1]*k)
 return Polygon([a,b,(b[0]+n[0]*k,b[1]+n[1]*k),(a[0]+n[0]*k,a[1]+n[1]*k)])
# Heights (m) above the street: eaves 'height', ridge 'top'. Measured values from the resected
# panoramas; zones marked est. are not seen and are estimated (see the notes).
# roof: 'gable_street' ridge at right angles to the street front; 'saddle' ridge along it;
# 'hip'; 'flat'.
cut=lambda i,*hs:[PG[i].intersection(h) for h in hs]
P=PG['93238210']
w210=P.intersection(half((312.8,57.27),(312.92,60.37),True))
e210=P.intersection(half((315.79,57.14),(315.92,60.4),False))
m210=P.difference(unary_union([w210,e210]))
P=PG['93238172'];f172=P.intersection(half((321.28,53.83),(325.9,53.66),True));b172=P.difference(f172)
P=PG['93238187'];b187=P.intersection(Polygon([(339.0,40.0),(343.3,40.0),(343.3,51.30),(339.0,51.30)]));f187=P.difference(b187)
P=PG['93238156'];f156=P.intersection(half((349.66,49.99),(362.72,49.89),True));b156=P.difference(f156)
P=PG['93238202'];e202=P.intersection(half((378.02,45.5),(378.41,51.99),False))
w202=P.difference(e202).intersection(half((375.56,48.6),(376.16,52.28),True));m202=P.difference(unary_union([e202,w202]))
GEO={'c210w':w210,'c210e':e210,'c210m':m210,'r172':f172,'r172b':b172,'y187':f187,'y187b':b187,'k156':f156,'k156b':b156,
 'g202':e202,'g202w':w202,'g202m':m202}
spec={
 'c210w':dict(height=2.20,top=4.05,roof='gable_street',osm='93238210'),
 'c210e':dict(height=4.20,top=5.75,roof='gable_street',osm='93238210'),
 'c210m':dict(height=2.60,top=3.60,roof='saddle',osm='93238210',est=True),
 'r172':dict(height=5.00,top=7.10,roof='saddle',osm='93238172'),
 'r172b':dict(height=4.20,top=5.60,roof='saddle',osm='93238172',est=True),
 'y187':dict(height=8.75,top=11.90,roof='hip',osm='93238187'),
 'y187b':dict(height=8.20,top=8.20,roof='flat',osm='93238187',est=True),
 'k156':dict(height=11.80,top=15.00,roof='hip',osm='93238156'),
 'k156b':dict(height=10.40,top=10.40,roof='flat',osm='93238156',est=True),
 'g202':dict(height=2.00,top=3.85,roof='gable_street',osm='93238202'),
 'g202w':dict(height=2.20,top=4.20,roof='saddle',osm='93238202',est=True),
 'g202m':dict(height=2.40,top=2.40,roof='flat',osm='93238202',est=True),
}
for z in spec:spec[z]['mesh']=MESH[spec[z]['osm']]
taken=Polygon();zones={}
for name in spec:
 ps=parts(GEO[name].difference(taken));zones[name]=ps;taken=unary_union([taken]+ps)
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
data={'source':'district volumes '+', '.join(IDS)+' (source/district17.json; 93238210 as its outer ring), '+district['source'],'zones':out,
 'checks':{'footprint_m2':round(foot.area,1),'zoned_m2':round(covered.area,1),'outside_osm_m2':round(covered.difference(foot).area,2),'osm_not_zoned_m2':round(foot.difference(covered).area,2),
  'overlap_m2':round(sum(p.area for ps in zones.values() for p in ps)-covered.area,3)}}
(R/'source/block100.json').write_text(json.dumps(data,indent=1,ensure_ascii=False))
c=data['checks'];ok=c['outside_osm_m2']<.2 and c['osm_not_zoned_m2']<.5 and c['overlap_m2']<.2
(R/'previews/block100-zones.json').write_text(json.dumps({'status':'passed' if ok else 'review_required','zones':report,'checks':c},indent=2,ensure_ascii=False))
print(json.dumps(report));print(c);print('BLOCK100_ZONES_OK' if ok else 'BLOCK100_ZONES_REVIEW')
