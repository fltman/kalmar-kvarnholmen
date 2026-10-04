"""Pass 96: the east side of north Proviantgatan (fronts face west) and the south side of
Fiskaregatan east of it (fronts face north): five district volumes split into seven parts:
- 90859877: the red boarded house with its gable to Proviantgatan;
- 90859878: the small white boarded gable cottage (the gateway with the green gate lies in the
  3.5 m gap between the two outlines and is drawn in the build);
- 90859832: the grey rendered two-storey house on a brown base, low hipped roof;
- 90859848: the ochre rendered two-storey house, split at x 199.57 into its west wing on
  Proviantgatan (saddle roof along the street, two dormers) and its long north range on
  Fiskaregatan (saddle roof along that street, not photographed except its east end);
- 90859847: the long white stucco two-storey house on Fiskaregatan (11 m main body) and the small
  yard annex in the notch at its south-west corner.
Heights from four Google Street View panoramas (three on Proviantgatan, one on Fiskaregatan),
resected on house corners; see references/block96-notes.md.
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
R77,C78,G32,O48,W47=PG('90859877'),PG('90859878'),PG('90859832'),PG('90859848'),PG('90859847')
def band(a,b,depth,s0=-80,s1=80):
 # The strip behind the street front a-b (inwards is to the left of a->b), depth metres deep.
 L=math.dist(a,b);dx,dy=(b[0]-a[0])/L,(b[1]-a[1])/L;nx,ny=-dy,dx
 return Polygon([(a[0]+dx*s+nx*t,a[1]+dy*s+ny*t) for s,t in ((s0,-.5),(s1,-.5),(s1,depth),(s0,depth))])
# 90859848: the west wing is the part west of x 199.57 (the outline's own step); the north range
# is the rest. 90859847: the main body is the 10.95 m deep strip behind the Fiskaregatan front; the
# notch at its south-west corner is a low yard annex.
WING=O48.intersection(box(150,100,199.57,140))
FISK_A,FISK_B=(270.17,131.71),(242.74,132.17)
MAIN47=W47.intersection(band(FISK_A,FISK_B,10.95))
seeds=[('rd',R77),('co',C78),('gr',G32),('ow',WING),('on',O48),('wm',MAIN47),('wx',W47)]
# Heights (m) above the street at the facade. Eaves measured on the resected panoramas; ridges
# measured where a gable faces the street (red house, cottage) and estimated for the others.
spec={'rd':dict(height=3.90,top=6.20,mesh='SM_Kvarnholmen_House_90859877',roof='gable_street'),
 'co':dict(height=1.90,top=3.55,mesh='SM_Kvarnholmen_House_90859878',roof='gable_street'),
 'gr':dict(height=6.85,top=8.30,mesh='SM_Kvarnholmen_House_90859832',roof='hip'),
 'ow':dict(height=7.00,top=11.80,mesh='SM_Kvarnholmen_House_90859848',roof='saddle_along'),
 'on':dict(height=7.00,top=11.65,mesh='SM_Kvarnholmen_House_90859848',roof='saddle_along'),
 'wm':dict(height=7.85,top=11.20,mesh='SM_Kvarnholmen_House_90859847',roof='saddle_along'),
 'wx':dict(height=4.00,top=4.20,mesh='SM_Kvarnholmen_House_90859847',roof='flat')}
taken=Polygon();zones={}
for name,seed in seeds:
 ps=parts(seed.difference(taken));zones[name]=ps;taken=unary_union([taken]+ps)
scope={'90859877','90859878','90859832','90859848','90859847'}
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
foot=unary_union([R77,C78,G32,O48,W47]);covered=unary_union([p for ps in zones.values() for p in ps])
data={'source':'district volumes 90859877, 90859878, 90859832, 90859848 and 90859847 (source/district17.json), '+district['source'],
 'frames':{'proviant':{'origin':[188.73,103.81],'along':[0,1],'note':'Proviantgatan fronts, s northwards along x about 188.8, inwards +x'},
  'fiskare':{'origin':list(FISK_A),'along':[round((FISK_B[0]-FISK_A[0])/math.dist(FISK_A,FISK_B),5),round((FISK_B[1]-FISK_A[1])/math.dist(FISK_A,FISK_B),5)],'note':'Fiskaregatan front of 90859847, s westwards, inwards -y'}},
 'zones':out,
 'checks':{'footprint_m2':round(foot.area,1),'zoned_m2':round(covered.area,1),'outside_osm_m2':round(covered.difference(foot).area,2),'osm_not_zoned_m2':round(foot.difference(covered).area,2),
  'overlap_m2':round(sum(p.area for ps in zones.values() for p in ps)-covered.area,3)}}
(R/'source/block96.json').write_text(json.dumps(data,indent=1,ensure_ascii=False))
c=data['checks'];ok=c['outside_osm_m2']<.2 and c['osm_not_zoned_m2']<.5 and c['overlap_m2']<.2
(R/'previews/block96-zones.json').write_text(json.dumps({'status':'passed' if ok else 'review_required','zones':report,'checks':c},indent=2,ensure_ascii=False))
print(json.dumps(report));print(c);print('BLOCK96_ZONES_OK' if ok else 'BLOCK96_ZONES_REVIEW')
