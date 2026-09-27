"""Pass 41: the district volume 92412838 on the north side of Södra Långgatan between the garage yard
and Östra Sjögatan (numbers 39-43): a white-rendered two-storey range in two builds, the eastern
of 1888 (segmental ground-floor windows, a rusticated arched portal, a baroque central gable with a
cartouche) and the western of 1940 (garages, doors in stone surrounds, a wide window, a lunette
gable). Heights come from Google Street View panoramas (April 2025) registered on the building's
two ends and shared window edges; see references/block41-notes.md.
Run with Shapely on the path: KALMAR_GEO=/path/to/site-packages python3 prepare_block41.py
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
PN=Polygon(dring('92412838')).buffer(0)
FRONT=box(-10,-75,50,-61.3)
seeds=[('fr',PN.intersection(FRONT)),('ew',PN.intersection(box(41.5,-61.3,50,-40))),('rw',PN.difference(FRONT).difference(box(41.5,-61.3,50,-40)))]
# Heights (m) above the facade base: the string course 4.5-4.62, the upper windows 5.25-7.55, the
# cornice from 8.0 (its top 9.0-9.2 on the facade plane, 8.75 at its projection), the front range's
# roof to a ridge at about 12. The east wing on Östra Sjögatan carries the same cornice; the
# courtyard wing's height is the district's.
spec={'fr':dict(height=8.75,top=12.0,mesh='SM_Building_92412838'),
 'ew':dict(height=8.75,top=11.3,mesh='SM_Building_92412838'),
 'rw':dict(height=7.1,top=9.0,mesh='SM_Building_92412838')}
taken=Polygon();zones={}
for name,seed in seeds:
 ps=parts(seed.difference(taken));zones[name]=ps;taken=unary_union([taken]+ps)
scope={'92412838'}
# The pass 39 zones are neighbours (the grey house to the west).
b39=json.loads((R/'source/block39.json').read_text())['zones']
others=[(Polygon(p).buffer(0),z['height'],'block39:'+k) for k,z in b39.items() for p in z['polygons']]+[(Polygon([tuple(w['p']) for w in v['walls']]).buffer(0),v['H'],v['id']) for v in d17.values() if v['id'] not in scope|{'92412832','92412859','92412869'} and len(v['walls'])>=3]
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
def roof_ring(name,inset):
 # Counter-clockwise outline of the zone, merged at near-collinear vertices; inset 0 on the edges
 # that lie on a party wall (a fire wall rises there), the given inset on the free edges.
 poly=orient(zones[name][0].simplify(.12));ring=[tuple(round(c,3) for c in v) for v in list(poly.exterior.coords)[:-1]]
 fire=[]
 for p,q in zip(ring,ring[1:]+ring[:1]):
  Lr=math.dist(p,q);wx,wy=(q[0]-p[0])/Lr,(q[1]-p[1])/Lr;nx,ny=wy,-wx
  nb,_=neighbour_at(Point((p[0]+q[0])/2+nx*.3,(p[1]+q[1])/2+ny*.3))
  fire.append(nb is not None)
 r1=inner(ring,[0 if f else inset for f in fire])
 assert Polygon(ring).exterior.is_ccw and Polygon(r1).is_valid and Polygon(r1).area>.5,(name,r1)
 return dict(outer=[list(v) for v in ring],r1=[list(v) for v in r1],firewall=fire,inset=inset)
out['fr']['roof']=roof_ring('fr',4.0)
# The western end is a gable wall over the garage yard (seen from panorama "37"), not a hip.
# The rear edge rises over the lower courtyard wing: a hip slope there, not a fire wall.
fr=out['fr']['roof'];n_=len(fr['outer']);mid=lambda k:((fr['outer'][k][0]+fr['outer'][(k+1)%n_][0])/2,(fr['outer'][k][1]+fr['outer'][(k+1)%n_][1])/2)
fr['firewall']=[mid(k)[0]<0 for k in range(n_)];fr['r1']=[list(v) for v in inner([tuple(v) for v in fr['outer']],[0 if f else 4.0 for f in fr['firewall']])]
out['ew']['roof']=roof_ring('ew',2.6)
covered=unary_union([p for ps in zones.values() for p in ps]);foot=PN
data={'source':'district volume 92412838 (source/district17.json), '+district['source'],'zones':out,
 'checks':{'footprint_m2':round(foot.area,1),'zoned_m2':round(covered.area,1),'outside_osm_m2':round(covered.difference(foot).area,2),'osm_not_zoned_m2':round(foot.difference(covered).area,2),
  'overlap_m2':round(sum(p.area for ps in zones.values() for p in ps)-covered.area,3)}}
(R/'source/block41.json').write_text(json.dumps(data,indent=1,ensure_ascii=False))
c=data['checks'];ok=c['outside_osm_m2']<.2 and c['osm_not_zoned_m2']<.5 and c['overlap_m2']<.2
(R/'previews/block41-zones.json').write_text(json.dumps({'status':'passed' if ok else 'review_required','zones':report,'checks':c},indent=2,ensure_ascii=False))
print(json.dumps(report));print(c);print('BLOCK41_ZONES_OK' if ok else 'BLOCK41_ZONES_REVIEW')
