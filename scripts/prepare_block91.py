"""Pass 91: four generic pass-17 volumes at the east end of Storgatan, split at measured joints:
- north side (fronts facing south at y 0.3): 93192424, the red boarded house with its gable to the
  street, the grey double door under the east half of the gable (whose last 0.8 m lies in 93192442); 93192442, the green boarded gable house, the red
  door in the gateway east of it; 93192397, the yellow boarded gable house and the low yellow link
  west of it;
- south side (fronts facing north at y -11): 91928597, the cream stucco shop with the stepped
  gable; 91928575, Storgatan 65, the grey boarded two-storey house.
93192417 (the westmost north-side volume) is not in any photograph and is left as it is.
Heights from three resected Google Street View panoramas (April 2025); see
references/block91-notes.md.
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
R24,G42,Y97,S97,G75=PG('93192424'),PG('93192442'),PG('93192397'),PG('91928597'),PG('91928575')
# Joints on the north side, measured on the 68 Storgatan panorama (camera resected on the shop
# opposite): the red house's gable front runs to x 266.45 (its east 0.8 m lies in the green volume),
# the green house x 266.45-270.85, the yellow house's west corner x 273.93; the gateway between.
XB=lambda x0,x1:box(x0,-5,x1,20)
seeds=[('rh',R24),('gl',G42.intersection(XB(250,266.45))),('gh',G42.intersection(XB(266.45,270.85))),('gg',G42),
 ('yl',Y97.intersection(XB(250,273.93))),('yh',Y97),('sh',S97),('gr',G75)]
# Heights (m) above the pavement at the front. Camera height 2.4 m (the pavement line under the
# shop on the 68 panorama). Gable fronts: eaves at the foot of the bargeboards less 0.15 m, ridges
# at the bargeboard apex less 0.1 m; the red house's eaves from its apex and its measured slope. The shop's eaves at its cornice; its ridge set so the roof stays
# under the inner corners of the gable steps. 65: eaves scaled to a 2.4 m camera and checked
# on the 68 panorama; its ridge from the west gable apex and the roof seen over the eaves (see the notes).
spec={'rh':dict(height=2.9,top=5.2,mesh='SM_Kvarnholmen_House_93192424',roof='saddle_x'),
 'gl':dict(height=2.9,top=3.0,mesh='SM_Kvarnholmen_House_93192442',roof='flat'),
 'gh':dict(height=4.35,top=5.6,mesh='SM_Kvarnholmen_House_93192442',roof='saddle_x'),
 'gg':dict(height=3.2,top=3.3,mesh='SM_Kvarnholmen_House_93192442',roof='flat'),
 'yl':dict(height=3.2,top=3.3,mesh='SM_Kvarnholmen_House_93192397',roof='flat'),
 'yh':dict(height=3.6,top=5.2,mesh='SM_Kvarnholmen_House_93192397',roof='saddle_x'),
 'sh':dict(height=4.5,top=9.3,mesh='SM_Kvarnholmen_House_91928597',roof='saddle_x'),
 'gr':dict(height=6.3,top=10.6,mesh='SM_Kvarnholmen_House_91928575',roof='saddle')}
taken=Polygon();zones={}
for name,seed in seeds:
 ps=parts(seed.difference(taken));zones[name]=ps;taken=unary_union([taken]+ps)
scope={'93192424','93192442','93192397','91928597','91928575'}
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
foot=unary_union([R24,G42,Y97,S97,G75]);covered=unary_union([p for ps in zones.values() for p in ps])
data={'source':'district volumes 93192424, 93192442, 93192397, 91928597 and 91928575 (source/district17.json), '+district['source'],'zones':out,
 'checks':{'footprint_m2':round(foot.area,1),'zoned_m2':round(covered.area,1),'outside_osm_m2':round(covered.difference(foot).area,2),'osm_not_zoned_m2':round(foot.difference(covered).area,2),
  'overlap_m2':round(sum(p.area for ps in zones.values() for p in ps)-covered.area,3)}}
(R/'source/block91.json').write_text(json.dumps(data,indent=1,ensure_ascii=False))
c=data['checks'];ok=c['outside_osm_m2']<.2 and c['osm_not_zoned_m2']<.5 and c['overlap_m2']<.2
(R/'previews/block91-zones.json').write_text(json.dumps({'status':'passed' if ok else 'review_required','zones':report,'checks':c},indent=2,ensure_ascii=False))
print(json.dumps(report));print(c);print('BLOCK91_ZONES_OK' if ok else 'BLOCK91_ZONES_REVIEW')
