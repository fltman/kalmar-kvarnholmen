"""Pass 38: two ways on the north side of Södra Långgatan, opposite pass 37 (the district volumes
92379256 and 92379310): the yellow two-storey house number 27 with the tattoo studio and the drug
store, and the Barometern newspaper building (1950s-60s) with its four fronts: a glass and slate
curtain wall with a mosaic pier and the garage, a salmon-rendered office front with pale vertical
bands, a tiled bay with the entrance, and a yellow corner at Ölandsgatan with an open arcade.
Heights come from Google Street View panoramas (April 2025) registered in pass 37; see
references/block38-notes.md.
Run with Shapely on the path: KALMAR_GEO=/path/to/site-packages python3 prepare_block38.py
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
def dring(bid):return [tuple(w['p']) for w in d17['SM_Building_'+bid]['walls']]
def flat(g):
 g=g.buffer(0);return [g] if g.geom_type=='Polygon' else [q for c in getattr(g,'geoms',[]) for q in flat(c)]
def parts(g):return [orient(r) for q in flat(g) for r in flat(q.buffer(-.02,join_style=2).buffer(.02,join_style=2).simplify(.02)) if r.area>1.0]
P27=Polygon(dring('92379256')).buffer(0);PB=Polygon(dring('92379310')).buffer(0)
seeds=[('n27',P27.intersection(box(-110,-68.95,-92.9,-58.59))),('n27r',P27.difference(box(-110,-68.95,-92.9,-58.59))),
 ('bar',PB.intersection(box(-95,-69.3,-39,-44.7))),('barr',PB.difference(box(-95,-69.3,-39,-44.7)))]
# Heights (m) above the facade base. Number 27: shop fronts to 3.0-3.15, a band at 3.87, windows
# 4.28-5.99 under cornice heads to 6.72, the eaves 7.7 (7.40-8.15 on the facade plane, corrected for
# the cornice's projection). The Barometern building: a stone-clad ground floor to 3.3-3.5, two
# window storeys (4.5-6.1 and 7.6-9.1), a flat roof behind a parapet at 10.2-10.6.
spec={'n27':dict(height=7.7,top=10.2,mesh='SM_Building_92379256'),
 'n27r':dict(height=6.2,top=8.0,mesh='SM_Building_92379256'),
 'bar':dict(height=10.6,top=10.6,mesh='SM_Building_92379310'),
 'barr':dict(height=7.4,top=7.4,mesh='SM_Building_92379310')}
taken=Polygon();zones={}
for name,seed in seeds:
 ps=parts(seed.difference(taken));zones[name]=ps;taken=unary_union([taken]+ps)
scope={'92379256','92379310'}
others=[(Polygon([tuple(w['p']) for w in v['walls']]).buffer(0),v['H'],v['id']) for v in d17.values() if v['id'] not in scope and len(v['walls'])>=3]
b34=json.loads((R/'source/block34.json').read_text())['zones']
others=[(Polygon(p).buffer(0),z['height'],'block34:'+k) for k,z in b34.items() for p in z['polygons']]+others
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
def inner(ring,insets):
 lines=[]
 for (p,q),d in zip(zip(ring,ring[1:]+ring[:1]),insets):
  Lr=math.dist(p,q);ax,ay=(q[0]-p[0])/Lr,(q[1]-p[1])/Lr;nx,ny=-ay,ax
  lines.append(((p[0]+nx*d,p[1]+ny*d),(ax,ay)))
 pts=[]
 for i in range(len(ring)):
  (p1,d1),(p2,d2)=lines[i-1],lines[i];det=d1[0]*(-d2[1])-d1[1]*(-d2[0])
  t=((p2[0]-p1[0])*(-d2[1])-(p2[1]-p1[1])*(-d2[0]))/det;pts.append((round(p1[0]+d1[0]*t,3),round(p1[1]+d1[1]*t,3)))
 return pts
# Number 27's front range: slopes to the street and the courtyard, fire walls at both party walls.
fr=[(-104.978,-68.85),(-92.999,-68.919),(-92.95,-58.59),(-104.945,-58.59)]      # street, east, courtyard, west
r1=inner(fr,[4.4,0,4.4,0])
assert Polygon(fr).exterior.is_ccw and Polygon(r1).is_valid
out['n27']['roof']=dict(outer=[list(v) for v in fr],r1=[list(v) for v in r1],firewall=[False,True,False,True],inset=4.4)
covered=unary_union([p for ps in zones.values() for p in ps]);foot=unary_union([P27,PB])
data={'source':'district volumes 92379256 and 92379310 (source/district17.json), '+district['source'],'zones':out,
 'checks':{'footprint_m2':round(foot.area,1),'zoned_m2':round(covered.area,1),'outside_osm_m2':round(covered.difference(foot).area,2),'osm_not_zoned_m2':round(foot.difference(covered).area,2),
  'overlap_m2':round(sum(p.area for ps in zones.values() for p in ps)-covered.area,3)}}
(R/'source/block38.json').write_text(json.dumps(data,indent=1,ensure_ascii=False))
c=data['checks'];ok=c['outside_osm_m2']<.2 and c['osm_not_zoned_m2']<.5 and c['overlap_m2']<.2
(R/'previews/block38-zones.json').write_text(json.dumps({'status':'passed' if ok else 'review_required','zones':report,'checks':c},indent=2,ensure_ascii=False))
print(json.dumps(report));print(c);print('BLOCK38_ZONES_OK' if ok else 'BLOCK38_ZONES_REVIEW')
