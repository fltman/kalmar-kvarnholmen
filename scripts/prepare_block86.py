"""Pass 86: the west side of the Proviantgatan row on eastern Kvarnholmen, five district volumes from
pass 17 (91928565, 91928576, 91928540, 91928545, 91928582) from south to north:
- Proviantgatan 6, the pale boarded one-and-a-half-storey house with three dormers;
- the small pink rendered cottage: a front range on the street and a lower range behind it;
- Proviantgatan 8, the cream two-storey house with the mansard roof and two dormers;
- Proviantgatan 10, the red boarded two-storey house under a low hipped metal roof;
- Proviantgatan 12, the narrow green rendered corner house: its two-storey main block and a lower
  rear wing.
Heights from four Google Street View panoramas, resected on house corners; see
references/block86-notes.md.
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
def flat(g):
 g=g.buffer(0);return [g] if g.geom_type=='Polygon' else [q for c in getattr(g,'geoms',[]) for q in flat(c)]
def parts(g):return [orient(r) for q in flat(g) for r in flat(q.buffer(-.02,join_style=2).buffer(.02,join_style=2).simplify(.02)) if r.area>1.0]
PG=lambda b:Polygon([tuple(w['p']) for w in d17['SM_Kvarnholmen_House_'+b]['walls']]).buffer(0)
P65,P76,P40,P45,P82=PG('91928565'),PG('91928576'),PG('91928540'),PG('91928545'),PG('91928582')
def band(a,b,depth,s0=-60,s1=60):
 # The strip behind the street front a-b (s along the front, t inwards), as a polygon in model
 # coordinates; inwards is to the left of a->b.
 L=math.dist(a,b);dx,dy=(b[0]-a[0])/L,(b[1]-a[1])/L;nx,ny=-dy,dx
 return Polygon([(a[0]+dx*s+nx*t,a[1]+dy*s+ny*t) for s,t in ((s0,0-.5),(s1,0-.5),(s1,depth),(s0,depth))])
# The pink cottage: its tiled front range on the street (5.2 m deep, estimated from the ridge seen
# 2.6 m behind the front), the lower range behind it in the rest of the long outline.
FRONT_PK=((186.0,-47.11),(185.91,-53.34))
# The green corner house: its two-storey main block taken 9.9 m deep from the street (estimate),
# the rest of the L-shaped outline as a low rear wing.
FRONT_GR=((186.18,-13.18),(186.11,-19.2))
seeds=[('ps',P65),('pk',P76.intersection(band(*FRONT_PK,5.2))),('pr',P76),('cr',P40),('rd',P45),
 ('gr',P82.intersection(band(*FRONT_GR,9.9))),('gw',P82)]
# Heights (m) above the street. Eaves measured on the resected panoramas; ridges as noted.
spec={'ps':dict(height=4.05,top=8.7,mesh='SM_Kvarnholmen_House_91928565',roof='saddle_y'),
 'pk':dict(height=3.1,top=7.0,mesh='SM_Kvarnholmen_House_91928576',roof='saddle_y'),
 'pr':dict(height=2.9,top=4.6,mesh='SM_Kvarnholmen_House_91928576',roof='saddle_x'),
 'cr':dict(height=6.4,top=10.1,mesh='SM_Kvarnholmen_House_91928540',roof='mansard',brk=(1.7,2.5)),
 'rd':dict(height=6.1,top=8.2,mesh='SM_Kvarnholmen_House_91928545',roof='hip'),
 'gr':dict(height=6.75,top=8.2,mesh='SM_Kvarnholmen_House_91928582',roof='hip'),
 'gw':dict(height=3.6,top=3.8,mesh='SM_Kvarnholmen_House_91928582',roof='flat')}
taken=Polygon();zones={}
for name,seed in seeds:
 ps=parts(seed.difference(taken));zones[name]=ps;taken=unary_union([taken]+ps)
scope={'91928565','91928576','91928540','91928545','91928582'}
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
foot=unary_union([P65,P76,P40,P45,P82]);covered=unary_union([p for ps in zones.values() for p in ps])
data={'source':'district volumes 91928565, 91928576, 91928540, 91928545 and 91928582 (source/district17.json), '+district['source'],'zones':out,
 'checks':{'footprint_m2':round(foot.area,1),'zoned_m2':round(covered.area,1),'outside_osm_m2':round(covered.difference(foot).area,2),'osm_not_zoned_m2':round(foot.difference(covered).area,2),
  'overlap_m2':round(sum(p.area for ps in zones.values() for p in ps)-covered.area,3)}}
(R/'source/block86.json').write_text(json.dumps(data,indent=1,ensure_ascii=False))
c=data['checks'];ok=c['outside_osm_m2']<.2 and c['osm_not_zoned_m2']<.5 and c['overlap_m2']<.2
(R/'previews/block86-zones.json').write_text(json.dumps({'status':'passed' if ok else 'review_required','zones':report,'checks':c},indent=2,ensure_ascii=False))
print(json.dumps(report));print(c);print('BLOCK86_ZONES_OK' if ok else 'BLOCK86_ZONES_REVIEW')
