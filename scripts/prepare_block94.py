"""Pass 94: the south side of Fiskaregatan east of Östra Sjögatan: four district volumes (91885523,
91926303, 91926337, 91926333) split into six parts: the grey rendered office with its tiled hip roof,
the white flat-roofed modernist block, the pale blue-green gable house with its low rear wing, and
the red gable house with the lower part west of and behind it.
Heights from three Google Street View panoramas (April 2025); see references/block94-notes.md.
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
OF,MO,BG,RH=PG('91885523'),PG('91926303'),PG('91926337'),PG('91926333')
def band(a,b,depth,s0=-60,s1=60):
 # The strip behind the street front a-b (s along the front from a, t inwards), as a polygon in
 # model coordinates; inwards is to the left of a->b, so the fronts run east -> west here.
 L=math.dist(a,b);dx,dy=(b[0]-a[0])/L,(b[1]-a[1])/L;nx,ny=-dy,dx
 return Polygon([(a[0]+dx*s+nx*t,a[1]+dy*s+ny*t) for s,t in ((s0,0-.5),(s1,0-.5),(s1,depth),(s0,depth))])
# The blue-green house: a gable house about 5.6 m deep on the street (its east wall, 130.39,113.94
# -> 129.28,108.58), the rest of the outline a low rear wing.
FRONT_BG=((130.39,113.94),(122.66,115.99))
# The red house: on the resected panorama its gable front is about 6.7 m wide from the outline's east
# corner; the 3.1 m west of it and the back of the outline are a lower part (estimated, unseen).
FRONT_RH=((143.51,110.8),(134.0,113.14))
seeds=[('of',OF),('mo',MO),('bg',BG.intersection(band(*FRONT_BG,5.6))),('bgr',BG),
 ('rh',RH.intersection(band(*FRONT_RH,8.3,-1,6.7))),('rx',RH)]
# Heights (m) above the facade base. Office: eaves and fascia measured, ridge estimated. Modernist:
# coping top measured. Blue-green and red houses: eaves and gable apex measured, the rear parts
# estimated.
spec={'of':dict(height=7.05,top=10.6,mesh='SM_Kvarnholmen_House_91885523',roof='hip'),
 'mo':dict(height=9.0,top=9.0,mesh='SM_Kvarnholmen_House_91926303',roof='flat'),
 'bg':dict(height=5.35,top=7.35,mesh='SM_Kvarnholmen_House_91926337',roof='saddle_across'),
 'bgr':dict(height=3.0,top=3.2,mesh='SM_Kvarnholmen_House_91926337',roof='flat'),
 'rh':dict(height=4.0,top=6.1,mesh='SM_Kvarnholmen_House_91926333',roof='saddle_across'),
 'rx':dict(height=3.2,top=3.3,mesh='SM_Kvarnholmen_House_91926333',roof='flat')}
taken=Polygon();zones={}
for name,seed in seeds:
 ps=parts(seed.difference(taken));zones[name]=ps;taken=unary_union([taken]+ps)
scope={'91885523','91926303','91926337','91926333'}
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
foot=unary_union([OF,MO,BG,RH]);covered=unary_union([p for ps in zones.values() for p in ps])
data={'source':'district volumes 91885523, 91926303, 91926337 and 91926333 (source/district17.json), '+district['source'],'zones':out,
 'checks':{'footprint_m2':round(foot.area,1),'zoned_m2':round(covered.area,1),'outside_osm_m2':round(covered.difference(foot).area,2),'osm_not_zoned_m2':round(foot.difference(covered).area,2),
  'overlap_m2':round(sum(p.area for ps in zones.values() for p in ps)-covered.area,3)}}
(R/'source/block94.json').write_text(json.dumps(data,indent=1,ensure_ascii=False))
c=data['checks'];ok=c['outside_osm_m2']<.2 and c['osm_not_zoned_m2']<.5 and c['overlap_m2']<.2
(R/'previews/block94-zones.json').write_text(json.dumps({'status':'passed' if ok else 'review_required','zones':report,'checks':c},indent=2,ensure_ascii=False))
print(json.dumps(report));print(c);print('BLOCK94_ZONES_OK' if ok else 'BLOCK94_ZONES_REVIEW')
