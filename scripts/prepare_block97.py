"""Pass 97: six scattered pass-17 volumes on Norra Långgatan and Östra Sjögatan:
- 91970395 (Norra Långgatan 37): the beige boarded two-storey house with its gable to the street,
  split into the narrow street part under the gable roof and the wide rear part (not seen);
- 91970343 (Östra Sjögatan 22): the yellow boarded one-and-a-half-storey gable house, split into the
  main body and the low annex at the back (not seen);
- 91885535: its 5.8 m street piece on Östra Sjögatan is the north end of the cream rendered house
  of pass 62, which on the panorama runs flush from pass 62 to the ochre house of pass 64. The OSM
  wall there stands 3.5 m back from the common facade line, so the strip in front of it
  (x 59.5-63.0, y 102.8-108.6, 19.4 m2) is ADDED to the zone; the long wing behind is not seen;
- 91885540 (Norra Långgatan 43): the beige rendered 1950s block, a semi-basement and three floors;
- 91926309 (Norra Långgatan 47): the cream neoclassical house, split into the street block and the
  rear wing (not seen);
- 91926329 (Norra Långgatan 55): the cream boarded two-storey house with the red metal roof, split
  into the street range and the east wing behind (not seen).
Heights from seven Google Street View views (six panoramas), resected on house corners, a
neighbour's measured window axes and storey heights; see references/block97-notes.md.
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
MESH={'91970395':'SM_Building_91970395','91970343':'SM_Building_91970343','91885535':'SM_Kvarnholmen_House_91885535',
 '91885540':'SM_Kvarnholmen_House_91885540','91926309':'SM_Building_91926309','91926329':'SM_Kvarnholmen_House_91926329'}
for osm,nm in MESH.items():
 assert nm in d17 and d17[nm]['id']==osm and int(d17[nm].get('detail_pass') or 17)<=17,nm
PG={osm:Polygon([tuple(w['p']) for w in d17[nm]['walls']]).buffer(0) for osm,nm in MESH.items()}
# The strip in front of 91885535's recessed OSM wall, between the fronts of pass 62 (91885537,
# corner 59.504, 102.845) and pass 64 (91885528, corner 59.73, 108.64): the panorama shows one flat
# cream facade from the ochre corner southwards (see the notes).
# It reaches 0.3 m into the outline so that the union closes without a sliver.
ADDED=Polygon([(59.504,102.845),(63.30,102.784),(63.30,108.596),(59.73,108.64)])
# Cuts (all measured on the outlines, not on the photos):
# - 91970395: the narrow street body ends where the outline widens (y 91.15);
# - 91970343: the main body ends at the step of the outline (x 37.0);
# - 91885535: the cream street piece ends at the outline's step (x 69.24, the back of pass 62);
# - 91926309: the street block ends at the outline's step (y 42.83);
# - 91926329: the east wing is the part behind its inner corner (x 170.64, y 81.36).
seeds=[('nf',PG['91970395'].intersection(box(0,60,30,91.15))),('nr',PG['91970395'].difference(box(0,60,30,91.15))),
 ('ym',PG['91970343'].intersection(box(37.0,80,60,110))),('ya',PG['91970343'].difference(box(37.0,80,60,110))),
 ('cr',unary_union([PG['91885535'],ADDED]).intersection(box(55,90,69.24,115))),('cb',PG['91885535'].difference(box(55,90,69.24,115))),
 ('bl',PG['91885540']),
 ('nm',PG['91926309'].intersection(box(100,42.83,140,70))),('nw',PG['91926309'].difference(box(100,42.83,140,70))),
 ('sw',PG['91926329'].intersection(box(170.64,81.36,190,100))),('sr',PG['91926329'].difference(box(170.64,81.36,190,100)))]
# Heights (m) above the street at the facade: eaves (height) and ridge (top). Measured on the
# resected panoramas where the street front is seen; the unseen rear parts are estimated.
spec={'nf':dict(height=6.70,top=8.90,mesh=MESH['91970395'],roof='gable_street'),
 'nr':dict(height=6.00,top=6.30,mesh=MESH['91970395'],roof='flat'),
 'ym':dict(height=5.10,top=7.72,mesh=MESH['91970343'],roof='gable_street'),
 'ya':dict(height=3.20,top=3.45,mesh=MESH['91970343'],roof='flat'),
 'cr':dict(height=8.90,top=11.00,mesh=MESH['91885535'],roof='saddle_along'),
 'cb':dict(height=6.65,top=6.95,mesh=MESH['91885535'],roof='flat'),
 'bl':dict(height=10.35,top=12.60,mesh=MESH['91885540'],roof='hip'),
 'nm':dict(height=11.80,top=13.40,mesh=MESH['91926309'],roof='hip'),
 'nw':dict(height=11.80,top=13.40,mesh=MESH['91926309'],roof='hip'),
 'sr':dict(height=5.85,top=9.30,mesh=MESH['91926329'],roof='mansard'),
 'sw':dict(height=5.85,top=9.30,mesh=MESH['91926329'],roof='mansard')}
taken=Polygon();zones={}
for name,seed in seeds:
 ps=parts(seed.difference(taken));zones[name]=ps;taken=unary_union([taken]+ps)
scope=set(MESH)
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
foot=unary_union(list(PG.values())+[ADDED]);covered=unary_union([p for ps in zones.values() for p in ps])
data={'source':'district volumes '+', '.join(MESH)+' (source/district17.json), '+district['source'],
 'added':[[list(v) for v in list(orient(ADDED).exterior.coords)[:-1]]],
 'zones':out,
 'checks':{'footprint_m2':round(foot.area,1),'zoned_m2':round(covered.area,1),'outside_osm_m2':round(covered.difference(foot).area,2),'osm_not_zoned_m2':round(foot.difference(covered).area,2),
  'overlap_m2':round(sum(p.area for ps in zones.values() for p in ps)-covered.area,3),'added_m2':round(ADDED.difference(unary_union(list(PG.values()))).area,1)}}
(R/'source/block97.json').write_text(json.dumps(data,indent=1,ensure_ascii=False))
c=data['checks'];ok=c['outside_osm_m2']<.2 and c['osm_not_zoned_m2']<.5 and c['overlap_m2']<.2
(R/'previews/block97-zones.json').write_text(json.dumps({'status':'passed' if ok else 'review_required','zones':report,'checks':c},indent=2,ensure_ascii=False))
print(json.dumps(report));print(c);print('BLOCK97_ZONES_OK' if ok else 'BLOCK97_ZONES_REVIEW')
