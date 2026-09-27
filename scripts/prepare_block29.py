"""Pass 29: the north side of Södra Långgatan between Larmgatan and Kaggensgatan.

The generic district volumes of the block's south half are split into the houses that stand on
them: Södra Långgatan 9 (OSM 92204156) with its rear wing and the small courtyard house 92204161;
Södra Långgatan 11 (92204198); the long ochre house (92204187 west of the downpipe joint) and the
three-storey corner house on Kaggensgatan (92204187 east of it); and the Kaggensgatan range
92204189. The corner building on Larmgatan (92204170, 92204162) is left for a later pass.
Heights come from Google Street View (April 2025) with each camera registered on the north
facades; see references/block29-notes.md.
Run with Shapely on the path: KALMAR_GEO=/path/to/site-packages python3 prepare_block29.py
"""
from pathlib import Path
import json,math,os,sys
if os.environ.get('KALMAR_GEO'):sys.path.insert(0,os.environ['KALMAR_GEO'])
from shapely.geometry import Polygon,Point,box
from shapely.geometry.polygon import orient
from shapely.ops import unary_union
R=Path(__file__).resolve().parents[1]
district=json.loads((R/'source/kvarnholmen.json').read_text());B={b['id']:b for b in district['buildings']}
def ring(bid):
 r=[tuple(p) for p in B[bid]['polygons'][0]['outer']]
 return r[:-1] if r[0]==r[-1] else r
def flat(g):
 g=g.buffer(0);return [g] if g.geom_type=='Polygon' else [q for c in getattr(g,'geoms',[]) for q in flat(c)]
def parts(g):return [orient(r) for q in flat(g) for r in flat(q.buffer(-.02,join_style=2).buffer(.02,join_style=2).simplify(.02)) if r.area>1.0]
P156,P161,P198,P187,P189=(Polygon(ring(b)).buffer(0) for b in ('92204156','92204161','92204198','92204187','92204189'))
# The long ochre house and the corner house stand 0.55 m in front of the OSM line: their west end
# shows a 0.55 m side wall beside Södra Långgatan 11 from both panoramas west of it, and only with
# that step do the window rows seen from four panoramas agree.
PROJ=.55
# Södra Långgatan 11 measures 11.2 m between its quoin strips in two panoramas (OSM 10.83), so
# the joint with the ochre house lies 0.37 m east of the OSM joint.
SPLIT=-233.45
E0,E1=(SPLIT,-67.657),(-192.92,-68.43)
front=Polygon([E0,E1,(E1[0],E1[1]-PROJ),(E0[0],E0[1]-PROJ)])
strip11=P187.intersection(box(-240,-70,SPLIT,-59.95));P198=P198.union(strip11).buffer(0);P187=P187.difference(strip11).buffer(0)
# The strip overlaps the outline by 5 cm so the union closes along the old street line.
P187x=P187.union(Polygon([(E0[0],E0[1]+.05),(E1[0],E1[1]+.05),(E1[0],E1[1]-PROJ),(E0[0],E0[1]-PROJ)])).buffer(0)
# The downpipe between the ochre house and the corner house lies 28.95 m east of the ochre house's
# west end (twelve window bays at 2.33 m and the gateway, tied to the gate seen from two panoramas).
# The panoramas suggest the corner house is 1-1.5 m narrower than OSM; its corner stays on OSM.
JOINT=-204.49
sl9=P156.intersection(box(-260,-70,-240,-60.95));sl9r=P156.difference(sl9)
sl11=P198.intersection(box(-246,-70,SPLIT+.01,-59.95));sl11r=P198.difference(sl11)
sl13=P187x.intersection(box(-240,-70,JOINT,-54.4));sl13r=P187x.intersection(box(-240,-54.4,JOINT,-30))
kg=P187x.intersection(box(JOINT,-70,-185,-50))
k189e=P189.intersection(box(-202.95,-60,-185,-30));k189r=P189.difference(k189e)
seeds=[('sl9',sl9),('sl9r',sl9r),('sl161',P161),('sl11',sl11),('sl11r',sl11r),('sl13',sl13),('sl13r',sl13r),('kg',kg),('k189e',k189e),('k189r',k189r)]
# Heights (m), each above the house's own facade base (the north pavement falls towards
# Kaggensgatan): eaves or cornice top, then the roof top.
# Södra Långgatan 9: gutter band 5.8-6.03, wall gable apex 8.09; the ridge follows the gable's
# 40 degree pitch over the 6.5 m front range. Södra Långgatan 11: cornice top 6.88, set 0.2 m lower
# for its projection; segmental gable top 8.0. Ochre house: cornice 7.25, eaves edge 7.9 after the
# projection correction. Corner house: eaves 11.75 after the same correction, three storeys.
# Kaggensgatan range: eaves about 7.3 against the corner house's windows. Roof tops, the rear
# wings and the courtyard houses are estimates.
spec={'sl9':dict(height=6.02,top=8.75,roof='tile_hip',mesh='SM_Kvarnholmen_House_92204156',gable=[6.40,4.98,8.04]),
 'sl9r':dict(height=5.4,top=7.4,roof='tile_hip',mesh='SM_Kvarnholmen_House_92204156'),
 'sl161':dict(height=5.4,top=7.4,roof='tile_hip',mesh='SM_Kvarnholmen_House_92204161'),
 'sl11':dict(height=6.68,top=9.3,roof='metal_hip',mesh='SM_Kvarnholmen_House_92204198',gable=[5.33,2.80,8.0]),
 'sl11r':dict(height=5.9,top=8.1,roof='metal_hip',mesh='SM_Kvarnholmen_House_92204198'),
 'sl13':dict(height=7.75,top=12.3,roof='metal_hip',mesh='SM_Kvarnholmen_House_92204187'),
 'sl13r':dict(height=6.4,top=8.6,roof='metal_hip',mesh='SM_Kvarnholmen_House_92204187'),
 'kg':dict(height=11.55,top=15.0,roof='tile_hip',mesh='SM_Kvarnholmen_House_92204187'),
 'k189e':dict(height=7.15,top=10.5,roof='tile_hip',mesh='SM_Kvarnholmen_House_92204189'),
 'k189r':dict(height=6.4,top=8.9,roof='tile_hip',mesh='SM_Kvarnholmen_House_92204189')}
taken=Polygon();zones={}
for name,seed in seeds:
 ps=parts(seed.difference(taken));zones[name]=ps;taken=unary_union([taken]+ps)
scope={'92204156','92204161','92204198','92204187','92204189'}
# Neighbours: the pass 26/28 zones are across the street; the rest keep their district heights.
others=[(Polygon(ring(b['id'])).buffer(0),b['height'],b['id']) for b in district['buildings'] if b['id'] not in scope]
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
   ux,uy=(q[0]-p[0])/Lw,(q[1]-p[1])/Lw;nx,ny=uy,-ux;n=max(1,int(Lw/.2));runs=[]
   for k in range(n):
    t=(k+.5)/n;nb,h=neighbour_at(Point(p[0]+ux*Lw*t+nx*.3,p[1]+uy*Lw*t+ny*.3))
    if runs and runs[-1][0]==nb:runs[-1][3]=(k+1)/n
    else:runs.append([nb,h,k/n,(k+1)/n])
   for nb,h,t0,t1 in runs:
    z0=0.0 if nb is None else h
    if z0>=H-.05:continue
    a=(round(p[0]+ux*Lw*t0,3),round(p[1]+uy*Lw*t0,3));b=(round(p[0]+ux*Lw*t1,3),round(p[1]+uy*Lw*t1,3))
    if math.dist(a,b)<.2:continue
    walls.append({'p':list(a),'q':list(b),'z0':z0,'z1':H,'kind':'outer' if nb is None else 'upper','neighbour':nb})
 out[name]=dict(spec[name],polygons=[[list(v) for v in list(p.exterior.coords)[:-1]] for p in ps],walls=walls)
 report[name]={'area_m2':round(sum(p.area for p in ps),1),'polygons':len(ps),'walls':len(walls),'outer_m':round(sum(math.dist(w['p'],w['q']) for w in walls if w['kind']=='outer'),1)}
footprint=unary_union([P156,P161,P198,P187,P189])   # P198 and P187 as re-split above
covered=unary_union([p for ps in zones.values() for p in ps])
data={'source':'OpenStreetMap ways 92204156, 92204161, 92204198, 92204187, 92204189, '+district['source'],
 'zones':out,'joint_x':JOINT,'projection':PROJ,
 'checks':{'footprint_m2':round(footprint.area,1),'zoned_m2':round(covered.area,1),'outside_osm_m2':round(covered.difference(footprint).area,2),
  'osm_not_zoned_m2':round(footprint.difference(covered).area,2),'overlap_m2':round(sum(p.area for ps in zones.values() for p in ps)-covered.area,3),
  'projection_m2':round(front.area,2)}}
(R/'source/block29.json').write_text(json.dumps(data,indent=1,ensure_ascii=False))
c=data['checks']
ok=abs(c['outside_osm_m2']-c['projection_m2'])<.5 and c['overlap_m2']<.5 and c['osm_not_zoned_m2']<.5
(R/'previews/block29-zones.json').write_text(json.dumps({'status':'passed' if ok else 'review_required','zones':report,'checks':c},indent=2,ensure_ascii=False))
print(json.dumps(report,ensure_ascii=False));print(c);print('BLOCK29_ZONES_OK' if ok else 'BLOCK29_ZONES_REVIEW')
