"""Pass 82: the north side of Kom snart igen and Skeppsbron 13: four district volumes (91915626,
91915628, 91915620, 91915631) split at measured joints into eight parts: the orange-boarded house with
the round windows and its dark boarded annex, the yellow house with the blue awnings, the yellow
corner house (Kom snart igen 7 / Skeppsbron 11) with its lower west part and its north wing, and the
yellow café at Skeppsbron 13 with its south annex.
Heights from four Google Street View panoramas (April 2025); see references/block82-notes.md.
"""
from pathlib import Path
import json,math,os,sys
if os.environ.get('KALMAR_GEO'):sys.path.insert(0,os.environ['KALMAR_GEO'])
from shapely.geometry import Polygon,Point,box
from shapely.geometry.polygon import orient
from shapely.ops import unary_union
from shapely import affinity
R=Path(__file__).resolve().parents[1]
district=json.loads((R/'source/kvarnholmen.json').read_text())
d17=json.loads((R/'source/district17.json').read_text())['buildings']
def flat(g):
 g=g.buffer(0);return [g] if g.geom_type=='Polygon' else [q for c in getattr(g,'geoms',[]) for q in flat(c)]
def parts(g):return [orient(r) for q in flat(g) for r in flat(q.buffer(-.02,join_style=2).buffer(.02,join_style=2).simplify(.02)) if r.area>1.0]
PG=lambda b:Polygon([tuple(w['p']) for w in d17['SM_Kvarnholmen_House_'+b]['walls']]).buffer(0)
O26,Y28,K20,C31=PG('91915626'),PG('91915628'),PG('91915620'),PG('91915631')
def band(a,b,depth,s0=-60,s1=60):
 # The strip behind the street front a-b (local street frame: s along the front, t inwards), as a
 # polygon in model coordinates; inwards is to the left of a->b.
 L=math.dist(a,b);dx,dy=(b[0]-a[0])/L,(b[1]-a[1])/L;nx,ny=-dy,dx
 return Polygon([(a[0]+dx*s+nx*t,a[1]+dy*s+ny*t) for s,t in ((s0,0-.5),(s1,0-.5),(s1,depth),(s0,depth))])
# The orange house is one 8.2 m deep range on the street; its east wall carries the three round
# windows and measures 8.2 m. Behind it the dark boarded annex fills the rest of the outline.
FRONT_OR=((-42.584,-261.32),(-17.554,-268.274))
OR=O26.intersection(band(*FRONT_OR,8.2))
# Kom snart igen 7: the main house from the west step (x 17.55) east, 9.2 m deep (its east wall);
# the lower west part beyond the step; the north wing behind both.
FRONT_K7=((17.8,-277.0),(26.9,-279.8))
B7=K20.intersection(band(*FRONT_K7,9.2))
west=Polygon([(17.55,-300),(17.55,-240),(-20,-240),(-20,-300)])
seeds=[('or',OR),('ob',O26),('ye',Y28),('ma',B7.difference(west)),('wp',K20.intersection(band((9.462,-276.495),(17.256,-278.918),9.2)).intersection(west)),('nw',K20),
 ('ca',C31.intersection(box(20,-246.5,50,-225))),('cx',C31)]
# Heights (m) above the facade base. Eaves measured on the street fronts; ridges from the hip
# apex of the orange house (6.66 m) and the roof pitch it gives (about 42 degrees), estimated for
# the others. The café's eaves and ridge are estimates from a far, oblique view.
spec={'or':dict(height=3.0,top=6.6,mesh='SM_Kvarnholmen_House_91915626',roof='hip'),
 'ob':dict(height=3.4,top=3.6,mesh='SM_Kvarnholmen_House_91915626',roof='flat'),
 'ye':dict(height=3.0,top=6.8,mesh='SM_Kvarnholmen_House_91915628',roof='hip'),
 'ma':dict(height=3.2,top=6.9,mesh='SM_Kvarnholmen_House_91915620',roof='hip'),
 'wp':dict(height=2.9,top=5.6,mesh='SM_Kvarnholmen_House_91915620',roof='hip'),
 'nw':dict(height=2.9,top=5.4,mesh='SM_Kvarnholmen_House_91915620',roof='saddle_x'),
 'ca':dict(height=2.7,top=5.5,mesh='SM_Kvarnholmen_House_91915631',roof='saddle_y'),
 'cx':dict(height=3.0,top=3.2,mesh='SM_Kvarnholmen_House_91915631',roof='flat')}
taken=Polygon();zones={}
for name,seed in seeds:
 ps=parts(seed.difference(taken));zones[name]=ps;taken=unary_union([taken]+ps)
scope={'91915626','91915628','91915620','91915631'}
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
foot=unary_union([O26,Y28,K20,C31]);covered=unary_union([p for ps in zones.values() for p in ps])
data={'source':'district volumes 91915626, 91915628, 91915620 and 91915631 (source/district17.json), '+district['source'],'zones':out,
 'checks':{'footprint_m2':round(foot.area,1),'zoned_m2':round(covered.area,1),'outside_osm_m2':round(covered.difference(foot).area,2),'osm_not_zoned_m2':round(foot.difference(covered).area,2),
  'overlap_m2':round(sum(p.area for ps in zones.values() for p in ps)-covered.area,3)}}
(R/'source/block82.json').write_text(json.dumps(data,indent=1,ensure_ascii=False))
c=data['checks'];ok=c['outside_osm_m2']<.2 and c['osm_not_zoned_m2']<.5 and c['overlap_m2']<.2
(R/'previews/block82-zones.json').write_text(json.dumps({'status':'passed' if ok else 'review_required','zones':report,'checks':c},indent=2,ensure_ascii=False))
print(json.dumps(report));print(c);print('BLOCK82_ZONES_OK' if ok else 'BLOCK82_ZONES_REVIEW')
