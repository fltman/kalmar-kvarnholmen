"""Pass 28: the block between Larmgatan, Södra Långgatan, Kaggensgatan and Ölandsgatan.

The five remaining generic district volumes of the block are split into the houses that stand on
them: Södra Långgatan 8 (OSM 91856615); the yellow 1881 range of Södra Långgatan 10 (91856624),
whose rusticated quoin strip divides the gate house with its risalit from the corner house on
Kaggensgatan; Kaggensgatan 5 (91856594) with its street range and courtyard wings; the
courtyard house 91856619; and on Ölandsgatan (91856622) the rough-cast merchant house, the
lower house with the carriage gate and the three-storey corner house on Kaggensgatan.
Heights come from Google Street View (April 2025) with each camera resected against OSM joints
and the facade base; see references/block28-notes.md.
Run with Shapely on the path: KALMAR_GEO=/path/to/site-packages python3 prepare_block28.py
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
P15,P24,P94,P19,P22=(Polygon(ring(b)).buffer(0) for b in ('91856615','91856624','91856594','91856619','91856622'))
# Södra Långgatan 10: the quoin strip between the gate house and the corner house stands at
# x = -204.0 (it measures -203.6 .. -204.3 once the panoramas are resected). The gate house keeps
# a 12 m street range; behind it lie the glazed courtyard and the lower south-west wing.
QUOIN=-204.0
sl10c=P24.intersection(box(QUOIN,-140,-150,-60))
# The corner on Kaggensgatan is cut back 2.4 m on both streets (rusticated piers, shop door,
# tall window and the segmental attic with its oculus).
CH=2.4;cn=(-192.39,-79.46);chamfer=Polygon([(cn[0]+.01,cn[1]+.01),(cn[0]-CH,cn[1]+.01),(cn[0]+.01,cn[1]-CH)])
sl10c=sl10c.difference(chamfer);P24=P24.difference(chamfer)
sl10w=P24.intersection(box(-260,-91.0,QUOIN,-60))
sl10yard=P24.difference(sl10c).difference(sl10w)
# Kaggensgatan 5: the street range is 11.6 m deep; the two courtyard wings run west from it.
k5=P94.intersection(box(-204.6,-140,-150,-60));k5yard=P94.difference(k5)
# Ölandsgatan: joints at x = -227.8 (downpipe west of the carriage gate) and -212.0 (downpipe
# west of the corner house's quoins), both on the resected panoramas.
o5w=P22.intersection(box(-260,-150,-227.8,-100));o5m=P22.intersection(box(-227.8,-150,-212.0,-100));k3=P22.intersection(box(-212.0,-150,-150,-100))
seeds=[('sl8',P15),('sl10w',sl10w),('sl10c',sl10c),('sl10yard',sl10yard),('k5',k5),('k5yard',k5yard),('court',P19),('o5w',o5w),('o5m',o5m),('k3',k3)]
# Heights (m): cornice or eaves top, then the roof top. Measured on the facade plane: Södra
# Långgatan 8 cornice 8.2, pediment apex 10.9; Södra Långgatan 10 cornice 9.3, risalit pediment
# 10.6. A cornice's top edge seen from below lies in front of the facade, so the plane
# intersection overstates it; the calibration views (151, 152) put the modelled cornices 16-22 px
# high, and they are set 0.35-0.5 m lower: 7.8 and 10.5, 8.85 and 10.1. Corner attic about 2.5 m
# above the cornice; Kaggensgatan 5 eaves 7.8 (against the yellow neighbour's windows and
# cornice); Ölandsgatan eaves 8.6, 8.1 and 10.4. The same cornice correction lowers the corner
# house (deep moulded cornice) to 9.8 and Kaggensgatan 5 to 7.45; the rough-cast eaves boards
# barely project and match the calibration view unchanged. Roof tops, the courtyard wings and the courtyard
# house are estimates.
spec={'sl8':dict(height=7.8,top=10.6,roof='metal_hip',mesh='SM_Kvarnholmen_House_91856615',pediment=[-242.40,-252.71,10.5]),
 'sl10w':dict(height=8.85,top=11.65,roof='metal_hip',mesh='SM_Kvarnholmen_House_91856624',risalit=[-215.8,-221.2,10.1]),
 'sl10c':dict(height=8.85,top=11.65,attic=11.35,roof='metal_hip',mesh='SM_Kvarnholmen_House_91856624'),
 'sl10yard':dict(height=7.0,top=7.0,roof='flat',mesh='SM_Kvarnholmen_House_91856624'),
 'k5':dict(height=7.45,top=11.45,roof='tile_hip',mesh='SM_Kvarnholmen_House_91856594'),
 'k5yard':dict(height=6.4,top=8.2,roof='tile_hip',mesh='SM_Kvarnholmen_House_91856594'),
 'court':dict(height=6.4,top=8.6,roof='metal_hip',mesh='SM_Kvarnholmen_House_91856619'),
 'o5w':dict(height=8.6,top=13.2,roof='tile_hip',mesh='SM_Kvarnholmen_House_91856622'),
 'o5m':dict(height=8.1,top=12.4,roof='tile_hip',mesh='SM_Kvarnholmen_House_91856622'),
 'k3':dict(height=9.8,top=14.0,roof='tile_hip',mesh='SM_Kvarnholmen_House_91856622')}
taken=Polygon();zones={}
for name,seed in seeds:
 ps=parts(seed.difference(taken));zones[name]=ps;taken=unary_union([taken]+ps)
scope={'91856615','91856624','91856594','91856619','91856622'}
# Neighbours: the pass 26 houses keep their re-measured heights, the rest their district heights.
l26=json.loads((R/'source/larm26.json').read_text())['zones']
l26_ids={'91222222','91856621','91856599','91856613','91856604'}
others=[(Polygon(ps).buffer(0),z['height'],'larm26:'+name) for name,z in l26.items() for ps in z['polygons']]
others+=[(Polygon(ring(b['id'])).buffer(0),b['height'],b['id']) for b in district['buildings'] if b['id'] not in scope|l26_ids]
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
footprint=unary_union([P15,P24.union(chamfer),P94,P19,P22])
covered=unary_union([p for ps in zones.values() for p in ps])
data={'source':'OpenStreetMap ways 91856615, 91856624, 91856594, 91856619, 91856622, '+district['source'],
 'zones':out,'quoin_x':QUOIN,'chamfer':CH,
 'checks':{'footprint_m2':round(footprint.area,1),'zoned_m2':round(covered.area,1),'outside_osm_m2':round(covered.difference(footprint).area,2),
  'osm_not_zoned_m2':round(footprint.difference(covered).area,2),'overlap_m2':round(sum(p.area for ps in zones.values() for p in ps)-covered.area,3)}}
data['checks']['chamfer_m2']=round(chamfer.area,2)
(R/'source/block28.json').write_text(json.dumps(data,indent=1,ensure_ascii=False))
ok=data['checks']['outside_osm_m2']<.5 and data['checks']['overlap_m2']<.5 and data['checks']['osm_not_zoned_m2']<data['checks']['chamfer_m2']+1.0
(R/'previews/block28-zones.json').write_text(json.dumps({'status':'passed' if ok else 'review_required','zones':report,'checks':data['checks']},indent=2,ensure_ascii=False))
print(json.dumps(report,ensure_ascii=False));print(data['checks']);print('BLOCK28_ZONES_OK' if ok else 'BLOCK28_ZONES_REVIEW')
