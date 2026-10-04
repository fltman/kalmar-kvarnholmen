"""Pass 112: a correction pass. It re-zones four meshes that earlier passes built but got wrong:
- 91846945 (pass 109, generic): the block between Larmgatan, Norra Långgatan and Västra
  Vallgatan. Split into the white restaurant at 9 Larmgatan (y 91.7-110.55, measured), the range
  on Norra Långgatan south of it (y < 91.7) in two parts at x -310.1 (the east part has its gable
  to Larmgatan; the west part is the cream house with red-brown pilasters at Västerport), the
  small rear piece west of x -310.1, and the cream house north of the restaurant (y > 110.55) with
  its front range to x -300.6 and a back part;
- 91072716 (pass 111): Gamla vattentornet, the round tower and its small annex (as pass 111);
- 92204191 (pass 105): the beige rendered house on Kaggensgatan / Strömgatan, one zone;
- 93238202 (pass 100): the pale grey cottage on Östra Vallgatan, the same three zones as pass 100,
  every height 0.5 m lower (the lead's review of pass 101's ground readings).
Heights from resected Google panoramas (see references/block112-notes.md).
Run with Shapely: KALMAR_GEO=<site-packages> python3 scripts/prepare_block112.py
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
IDS=['91846945','91072716','92204191','93238202']
MESH={i:'SM_Kvarnholmen_House_'+i for i in IDS}
for i in IDS:assert MESH[i] in d17,MESH[i]
ring=lambda i:[tuple(w['p']) for w in d17[MESH[i]]['walls']]
PG={i:Polygon(ring(i)).buffer(0) for i in IDS}
for i in IDS:assert PG[i].is_valid and PG[i].geom_type=='Polygon',i
def half(p,q,left=True):
 # The half-plane to the left (or right) of the infinite line p->q, as a large polygon.
 L=math.dist(p,q);d=((q[0]-p[0])/L,(q[1]-p[1])/L);n=(-d[1],d[0]) if left else (d[1],-d[0]);k=500
 a=(p[0]-d[0]*k,p[1]-d[1]*k);b=(p[0]+d[0]*k,p[1]+d[1]*k)
 return Polygon([a,b,(b[0]+n[0]*k,b[1]+n[1]*k),(a[0]+n[0]*k,a[1]+n[1]*k)])
# 91846945. Lines: y 91.7 (the gable foot of the south range on Larmgatan, measured), y 110.55
# (the restaurant's north end, measured), x -310.1 (the outline's inner corner), x -300.6 (the
# depth of the north house's front range, estimated).
P=PG['91846945']
S=half((-400,91.7),(0,91.7),False)            # y < 91.7
N=half((-400,110.55),(0,110.55),True)         # y > 110.55
E=half((-310.1,0),(-310.1,200),False)         # x > -310.1
south=P.intersection(S);north=P.intersection(N);mid=P.difference(S).difference(N)
se945=south.intersection(E);sw945=south.difference(E)
r945=mid.intersection(E);k945=mid.difference(E)
EN=half((-300.6,0),(-300.6,200),False)
n945=north.intersection(EN);nb945=north.difference(EN)
# 91072716: the round tower and the small annex on its east side (as pass 111).
T=PG['91072716'];t716=T.intersection(Point(-331.3,122.45).buffer(7.2,64));a716=T.difference(t716)
# 93238202: as pass 100.
P=PG['93238202'];e202=P.intersection(half((378.02,45.5),(378.41,51.99),False))
w202=P.difference(e202).intersection(half((375.56,48.6),(376.16,52.28),True));m202=P.difference(unary_union([e202,w202]))
GEO={'r945':r945,'se945':se945,'sw945':sw945,'k945':k945,'n945':n945,'nb945':nb945,'t716':t716,'a716':a716,
 'h191':PG['92204191'],'g202':e202,'g202w':w202,'g202m':m202}
# Heights (m) above the pavement: eaves 'height', ridge or roof top 'top'. est=True: not measured.
spec={
 'r945':dict(height=8.75,top=10.60,roof='hip',osm='91846945'),
 'se945':dict(height=8.75,top=13.45,roof='saddle',osm='91846945'),
 'sw945':dict(height=9.35,top=11.20,roof='hip',osm='91846945'),
 'k945':dict(height=6.50,top=6.50,roof='flat',osm='91846945',est=True),
 'n945':dict(height=5.20,top=7.60,roof='saddle',osm='91846945'),
 'nb945':dict(height=4.50,top=4.50,roof='flat',osm='91846945',est=True),
 't716':dict(height=52.50,top=54.00,roof='tower',osm='91072716'),
 'a716':dict(height=4.00,top=4.00,roof='flat',osm='91072716',est=True),
 'h191':dict(height=6.30,top=9.20,roof='hip',osm='92204191'),
 'g202':dict(height=1.50,top=3.35,roof='gable_street',osm='93238202'),
 'g202w':dict(height=1.70,top=3.70,roof='saddle',osm='93238202',est=True),
 'g202m':dict(height=1.90,top=1.90,roof='flat',osm='93238202',est=True),
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
    t_=(k+.5)/n;nb,h=neighbour_at(Point(p[0]+wx*Lw*t_+nx*.3,p[1]+wy*Lw*t_+ny*.3))
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
(R/'source/block112.json').write_text(json.dumps(data,indent=1,ensure_ascii=False))
c=data['checks'];ok=c['outside_osm_m2']<.2 and c['osm_not_zoned_m2']<.5 and c['overlap_m2']<.2
(R/'previews/block112-zones.json').write_text(json.dumps({'status':'passed' if ok else 'review_required','zones':report,'checks':c},indent=2,ensure_ascii=False))
print(json.dumps(report));print(c);print('BLOCK112_ZONES_OK' if ok else 'BLOCK112_ZONES_REVIEW')
