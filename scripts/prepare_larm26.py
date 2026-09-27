"""Pass 26: five buildings on Larmgatan by the station. The Larmgatan 1 block (OSM 91222222)
is split into the bank of about 1910 with its mansard and clock lantern, the later office at its
south-east end and the lower south wing; Larmgatan 6, 8 and 10 (91856613, 91856599, 91856621)
and the Odd Fellows house at Larmgatan 2 (91856604) keep their mapped outlines. Seeds and
heights come from Google Street View (April 2025), measured by inverting the panorama camera.
Run with Shapely on the path: KALMAR_GEO=/path/to/site-packages python3 prepare_larm26.py
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
block=Polygon(ring('91222222')).buffer(0)
# The red bank facade on Larmgatan ends 36 m from Södra Långgatan (rounded corner at y=-115.5 in
# the 8 Larmgatan panorama); south of it the office, west of x=-313.2 the lower south wing
# (whose courtyard front is the mapped line at y=-112).
office=block.intersection(box(-313.2,-140,-290,-115.5))
south=block.intersection(box(-340,-140,-313.2,-111.8))
bank=block.difference(office).difference(south)
# The corner at Larmgatan/Södra Långgatan is cut back 2.2 m (chamfer with rusticated quarter
# rounds and the corner balcony in the photographs).
c1=(-297.31,-79.54);chamfer=Polygon([(c1[0]+.01,c1[1]+.01),(c1[0]-2.2,c1[1]+.01),(c1[0]+.01,c1[1]-2.2)])
bank=bank.difference(chamfer)
# Odd Fellows: both corners on Larmgatan are round towers (radius 2.4 m).
of=ring('91856604');RT=2.4
def rounded(poly,corners,r):
 g=Polygon(poly)
 for i in corners:
  a,b,c=poly[i-1],poly[i],poly[(i+1)%len(poly)]
  u=((a[0]-b[0])/math.dist(a,b),(a[1]-b[1])/math.dist(a,b));v=((c[0]-b[0])/math.dist(b,c),(c[1]-b[1])/math.dist(b,c))
  centre=(b[0]+(u[0]+v[0])*r,b[1]+(u[1]+v[1])*r)
  square=Polygon([b,(b[0]+u[0]*r,b[1]+u[1]*r),centre,(b[0]+v[0]*r,b[1]+v[1]*r)])
  g=g.difference(square).union(Point(centre).buffer(r,64).intersection(square.buffer(.001)))
 return g.buffer(0)
oddf=rounded(of,[0,1],RT)
seeds=[('bank',bank),('office',office),('southwing',south),('l10',Polygon(ring('91856621'))),('l8',Polygon(ring('91856599'))),
 ('l6',Polygon(ring('91856613'))),('oddfellow',oddf)]
# Heights (m) from the April 2025 panoramas, inverted through the camera (see notes): bank
# cornice top 10.8, mansard break 15.4 at a 1.7 m inset, upper roof 16.6, lantern base 16.6 /
# dome 18.8 / spire 21.4 (the distant plaza view, confirmed by the calibration render).
# Pass 28 re-measured the close fronts with the camera resected against OSM joints and the
# facade base (roof camera about 2.15 m high, not 2.5): Larmgatan 10 cornice 11.4 (was an
# estimate of 10.6), Larmgatan 8 main cornice 9.9 with a flush attic storey to 12.2 (was 11.3),
# Larmgatan 6 eaves 10.7 on Ölandsgatan (was 10.0), and the Odd Fellows house: rounded corner
# bays capped at 12.2, the central block with its lettered frieze rising to 15.3 (was 11.2).
# These are facade-plane intersections of the cornice edge; a projecting cornice seen from below
# stands in front of the facade, so the modelled cornices are set lower by their own projection
# (the calibration views of pass 28 confirm the correction): Larmgatan 10 10.75, Larmgatan 8 9.6,
# Larmgatan 6 10.5. The Odd Fellows block keeps 15.3 under a deep moulded cornice, whose
# silhouette then falls on the measured 16.3 m plane height.
spec={'bank':dict(height=10.8,band=15.4,inset=1.7,top=16.6,roof='mansard',mesh='SM_Kvarnholmen_House_91222222'),
 'office':dict(height=10.4,top=10.4,roof='flat',mesh='SM_Kvarnholmen_House_91222222'),
 'southwing':dict(height=7.0,top=10.0,roof='copper_hip',mesh='SM_Kvarnholmen_House_91222222'),
 'l10':dict(height=10.75,band=14.55,inset=1.6,top=15.05,roof='mansard',mesh='SM_Kvarnholmen_House_91856621'),
 'l8':dict(height=9.6,attic=12.2,top=14.6,roof='hip',mesh='SM_Kvarnholmen_House_91856599'),
 'l6':dict(height=10.5,attic=13.2,inset=1.4,top=15.0,roof='attic',mesh='SM_Kvarnholmen_House_91856613'),
 'oddfellow':dict(height=12.2,upper=15.3,top=15.8,tower=13.3,roof='parapet',mesh='SM_Kvarnholmen_House_91856604')}
taken=Polygon();zones={}
for name,seed in seeds:
 ps=parts(seed.intersection(seed).difference(taken));zones[name]=ps;taken=unary_union([taken]+ps)
# Neighbours outside the pass keep their current model heights.
scope={'91222222','91856621','91856599','91856613','91856604'}
others=[(Polygon(ring(b['id'])).buffer(0),b['height'],b['id']) for b in district['buildings'] if b['id'] not in scope]
# The pass 28 block next door has measured heights; use them where they exist.
b28=R/'source/block28.json'
if b28.exists():
 others=[(Polygon(ps).buffer(0),z['height'],'block28:'+name) for name,z in json.loads(b28.read_text())['zones'].items() for ps in z['polygons']]+others
def neighbour_at(pt):
 for name,ps in zones.items():
  if any(p.buffer(.001).contains(pt) for p in ps):return name,spec[name]['height']
 for g,h,bid in others:
  if g.buffer(.001).contains(pt):return 'osm:'+bid,h
 return None,0.0
out={};report={}
for name,ps in zones.items():
 # Larmgatan 8's attic storey is flush with its walls, so its walls rise to the attic.
 H=spec[name].get('attic',spec[name]['height']) if name=='l8' else spec[name]['height'];walls=[]
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
footprint=unary_union([Polygon(ring(b)).buffer(0) for b in scope])
covered=unary_union([p for ps in zones.values() for p in ps])
# Odd Fellows: above the corner bays only the central block rises, 3.0 m clear of both street
# corners (the rounded bays keep their own curved cornice and cap).
c0,c1=Polygon(of).exterior.coords[0],Polygon(of).exterior.coords[1]
upper=oddf.difference(Point(c0).buffer(3.0,cap_style=3)).difference(Point(c1).buffer(3.0,cap_style=3))
upper=max(flat(upper),key=lambda g:g.area).simplify(.02)
data={'source':'OpenStreetMap ways 91222222, 91856621, 91856599, 91856613, 91856604, '+district['source'],
 'oddfellow_upper':[list(v) for v in list(orient(upper).exterior.coords)[:-1]],
 'zones':out,'oddfellow_tower_radius':RT,
 'checks':{'footprint_m2':round(footprint.area,1),'zoned_m2':round(covered.area,1),'chamfer_m2':round(chamfer.intersection(block).area,2),
  'rounded_corners_m2':round(Polygon(of).difference(oddf).area,2),'outside_osm_m2':round(covered.difference(footprint).area,2),
  'osm_not_zoned_m2':round(footprint.difference(covered).area,2),'overlap_m2':round(sum(p.area for ps in zones.values() for p in ps)-covered.area,3)}}
(R/'source/larm26.json').write_text(json.dumps(data,indent=1,ensure_ascii=False))
ok=data['checks']['outside_osm_m2']<.5 and data['checks']['overlap_m2']<.5 and data['checks']['osm_not_zoned_m2']<data['checks']['chamfer_m2']+data['checks']['rounded_corners_m2']+.5
(R/'previews/larm26-zones.json').write_text(json.dumps({'status':'passed' if ok else 'review_required','zones':report,'checks':data['checks']},indent=2,ensure_ascii=False))
print(json.dumps(report,ensure_ascii=False));print(data['checks']);print('LARM26_ZONES_OK' if ok else 'LARM26_ZONES_REVIEW')
