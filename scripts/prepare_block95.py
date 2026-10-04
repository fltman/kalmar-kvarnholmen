"""Pass 95: the south side of Fiskaregatan, east part (fronts face north): four district volumes
(91926308, 91926299, 91926297, 91926357) split at measured joints into four parts and two open
gateways: the boarded gate wall with the green gate (west 3.4 m of 91926308, released), the pale
one-storey gable cottage (across the joint of 91926308 and 91926299), a narrow link east of it
(91926299, not seen), the pale grey two-storey gable house with the lunette (west part of
91926297), the gateway with the rendered pier and the green gate (east 3.04 m of 91926297, released
as open ground; gate and walls are drawn in the build), and the red two-storey house with the white
pilasters (91926357).
Heights from three Google Street View panoramas (two on this block, one from pass 94 further west),
resected on house corners; see references/block95-notes.md.
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
PG=lambda b:Polygon([tuple(w['p']) for w in d17['SM_Kvarnholmen_House_'+b]['walls']]).buffer(0)
S08,S99,S97,S57=PG('91926308'),PG('91926299'),PG('91926297'),PG('91926357')
# Street frame: origin at the shared front corner of 91926297 and 91926357, s eastwards along the
# fronts, t northwards (towards the street); the facades stand 0.355 m out at t = 0.355.
C=(165.91,105.19);D=(0.9693,-0.2459);N=(0.2459,0.9693)
def band95(s0,s1):
 # Everything between s = s0 and s = s1 in the street frame.
 P=lambda s,t:(C[0]+D[0]*s+N[0]*t,C[1]+D[1]*s+N[1]*t)
 return Polygon([P(s0,-30),P(s1,-30),P(s1,30),P(s0,30)])
# Joints measured on the panoramas (s in the street frame):
# - the green gate and the white door in a boarded wall fill the west 3.4 m of 91926308 (s -23.09
#   to -19.65); a yard lies behind, so that strip is released and the wall drawn in the build;
# - the cottage runs from s -19.65 to -14.87 across the joint between 91926308 and 91926299;
# - a narrow link (not seen) fills 91926299 east of the cottage, to the grey house's west wall;
# - the grey house's east corner is at s -3.04; east of it to the red house the gateway (s -3.04
#   to 0) opens onto a yard and is released.
GATEW=S08.intersection(band95(-40,-19.65));GATEE=S97.intersection(band95(-3.04,10))
COT=unary_union([S08,S99]).intersection(band95(-19.65,-14.87))
RELEASED=unary_union([GATEW,GATEE])
seeds=[('co',COT),('ln',S99.difference(COT)),('gr',S97.difference(GATEE)),('rd',S57)]
# Heights (m) above the street at the facade. Eaves measured on the resected panoramas; ridges
# measured where the gable faces the street (cottage, grey house), estimated for the others.
spec={'co':dict(height=2.41,top=3.90,mesh='SM_Kvarnholmen_House_91926308',roof='gable_street'),
 'ln':dict(height=2.50,top=3.30,mesh='SM_Kvarnholmen_House_91926299',roof='saddle_along'),
 'gr':dict(height=5.10,top=7.60,mesh='SM_Kvarnholmen_House_91926297',roof='gable_street'),
 'rd':dict(height=5.75,top=8.30,mesh='SM_Kvarnholmen_House_91926357',roof='saddle_along')}
taken=Polygon();zones={}
for name,seed in seeds:
 ps=parts(seed.difference(taken));zones[name]=ps;taken=unary_union([taken]+ps)
scope={'91926308','91926299','91926297','91926357'}
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
foot=unary_union([S08,S99,S97,S57]).difference(RELEASED);covered=unary_union([p for ps in zones.values() for p in ps])
data={'source':'district volumes 91926308, 91926299, 91926297 and 91926357 (source/district17.json), '+district['source'],
 'frame':{'origin':list(C),'along':list(D),'inwards':[-N[0],-N[1]]},'released':[[list(v) for v in list(orient(p).exterior.coords)[:-1]] for p in flat(RELEASED) if p.area>.5],
 'zones':out,
 'checks':{'footprint_m2':round(foot.area,1),'zoned_m2':round(covered.area,1),'outside_osm_m2':round(covered.difference(foot).area,2),'osm_not_zoned_m2':round(foot.difference(covered).area,2),
  'overlap_m2':round(sum(p.area for ps in zones.values() for p in ps)-covered.area,3),'released_m2':round(RELEASED.area,1)}}
(R/'source/block95.json').write_text(json.dumps(data,indent=1,ensure_ascii=False))
c=data['checks'];ok=c['outside_osm_m2']<.2 and c['osm_not_zoned_m2']<.5 and c['overlap_m2']<.2
(R/'previews/block95-zones.json').write_text(json.dumps({'status':'passed' if ok else 'review_required','zones':report,'checks':c},indent=2,ensure_ascii=False))
print(json.dumps(report));print(c);print('BLOCK95_ZONES_OK' if ok else 'BLOCK95_ZONES_REVIEW')
