"""Pass 35: two houses on the south side of Södra Långgatan, opposite pass 34 (OSM 92379316 and
92379296): the wooden house with number 22 by its door and the yellow palace with the Systembolaget
portal. Each is split into a front range on the street and lower ranges behind it. Heights come
from Google Street View panoramas (April 2025), registered on a common camera track (see
references/block35-notes.md): the palace's west joint and the wooden house's east joint agree with
OSM, but the joint between the two houses stands 0.83 m west of the OSM vertex, so the zones are
split at the measured joint.
Run with Shapely on the path: KALMAR_GEO=/path/to/site-packages python3 prepare_block35.py
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
P316,P296=(Polygon(ring(b)).buffer(0) for b in ('92379316','92379296'))
# The measured joint (the downpipe between the wooden house's corner board and the palace's
# quoins) is 0.83 m west of the shared OSM vertex (-116.616, -80.003). The party wall is moved
# parallel to itself, as far back as the palace's front range (y -92.54).
JX=-117.45
def on(p,q,x):return (x,p[1]+(q[1]-p[1])*(x-p[0])/(q[0]-p[0]))
JF=on((-105.127,-79.872),(-116.616,-80.003),JX)                 # the joint on the wooden front line
dx=JX-(-116.616);JB=(-116.808+dx,-92.544)
strip=Polygon([(-116.616,-80.003),JF,JB,(-116.808,-92.544)])
WOOD=unary_union([P316,strip]).buffer(0);PAL=P296.difference(strip).buffer(0)
FRONTW=box(-120,-89.90,-100,-79);FRONTP=box(-142,-92.56,-117,-79)
seeds=[('w22',WOOD.intersection(FRONTW)),('w22r',WOOD.difference(FRONTW)),('pal',PAL.intersection(FRONTP)),('palr',PAL.difference(FRONTP))]
# Heights (m) above each house's facade base. The wooden house: band 2.28-2.48, windows 3.38-5.18,
# frieze 5.38-5.59; the cornice's gutter edge reads 6.08 on the facade plane but stands 0.45 m out,
# so the eaves are at 5.85; the ridge 11.1 from the sight line over the eaves (the front range is
# 10 m deep). The palace: ground floor to the band at 4.17-4.50, windows 5.31-6.98 and
# 8.60-10.07, the cornice top 11.6 (corrected for its projection); the ridge 15.7 from the east
# fire wall seen above the wooden house. The rear ranges are estimates.
spec={'w22':dict(height=5.85,top=11.1,mesh='SM_Kvarnholmen_House_92379316'),
 'w22r':dict(height=5.0,top=7.0,mesh='SM_Kvarnholmen_House_92379316'),
 'pal':dict(height=11.6,top=15.7,mesh='SM_Kvarnholmen_House_92379296'),
 'palr':dict(height=8.8,top=11.0,mesh='SM_Kvarnholmen_House_92379296')}
taken=Polygon();zones={}
for name,seed in seeds:
 ps=parts(seed.difference(taken));zones[name]=ps;taken=unary_union([taken]+ps)
scope={'92379316','92379296'}
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
# Front-range roofs: slopes to the street and the courtyard, fire walls at the party walls.
def inner(ring,insets):
 lines=[]
 for (p,q),d in zip(zip(ring,ring[1:]+ring[:1]),insets):
  L=math.dist(p,q);ux,uy=(q[0]-p[0])/L,(q[1]-p[1])/L;nx,ny=-uy,ux
  lines.append(((p[0]+nx*d,p[1]+ny*d),(ux,uy)))
 pts=[]
 for i in range(len(ring)):
  (p1,d1),(p2,d2)=lines[i-1],lines[i];det=d1[0]*(-d2[1])-d1[1]*(-d2[0])
  t=((p2[0]-p1[0])*(-d2[1])-(p2[1]-p1[1])*(-d2[0]))/det;pts.append((round(p1[0]+d1[0]*t,3),round(p1[1]+d1[1]*t,3)))
 return pts
jr=lambda y:(JX+(JB[0]-JX)*(y-JF[1])/(JB[1]-JF[1]),y)           # the moved party wall at depth y
fronts={'w22':([(-105.127,-79.872),JF,jr(-89.90),(-105.184,-89.896)],4.9),
 'pal':([JF,(-139.797,-79.661),(-139.797+(-140.16+139.797)*(92.45-79.661)/(103.718-79.661),-92.45),JB],6.2)}
for name,(fr,inset) in fronts.items():
 fr=[(round(p[0],3),round(p[1],3)) for p in fr]
 fw=[False,True,False,True]            # street side, west party wall, courtyard side, east party wall (CCW)
 r1=inner(fr,[0 if f else inset for f in fw])
 g=Polygon(r1);assert Polygon(fr).exterior.is_ccw and g.is_valid and g.area<Polygon(fr).area and Polygon(fr).buffer(.01).contains(g),name
 out[name]['roof']=dict(outer=[list(v) for v in fr],r1=[list(v) for v in r1],firewall=fw,inset=inset)
out['w22']['joint']=[round(JF[0],3),round(JF[1],3)]
covered=unary_union([p for ps in zones.values() for p in ps]);foot=unary_union([P316,P296])
data={'source':'OpenStreetMap ways 92379316, 92379296, '+district['source'],'zones':out,
 'checks':{'footprint_m2':round(foot.area,1),'zoned_m2':round(covered.area,1),'outside_osm_m2':round(covered.difference(foot).area,2),'osm_not_zoned_m2':round(foot.difference(covered).area,2),
  'overlap_m2':round(sum(p.area for ps in zones.values() for p in ps)-covered.area,3),'joint_moved_m':round(math.dist(JF,(-116.616,-80.003)),2),'strip_m2':round(strip.area,2)}}
(R/'source/block35.json').write_text(json.dumps(data,indent=1,ensure_ascii=False))
c=data['checks'];ok=c['outside_osm_m2']<.2 and c['osm_not_zoned_m2']<.5 and c['overlap_m2']<.2
(R/'previews/block35-zones.json').write_text(json.dumps({'status':'passed' if ok else 'review_required','zones':report,'checks':c},indent=2,ensure_ascii=False))
print(json.dumps(report));print(c);print('BLOCK35_ZONES_OK' if ok else 'BLOCK35_ZONES_REVIEW')
