"""Pass 80: the district volumes 90859833, 90859843 and 90859883 on the north side of Norra
Långgatan east of pass 76, and the missing white house between them (OSM way 90859904).
"""
_OLD_DOC="""Pass 76: the district volumes 90859889, 90859896 and 90859843 on the north side of Norra
Långgatan, opposite pass 75, split at their measured joints into five houses: the green boarded
cottage with its cross gable, the red house with white windows, the red house with green windows
and the orange door, a narrow boarded passage door, and the white gable-fronted house with its
low back annex. The two carriage gates between the green and the red houses open onto a yard: that
strip (x 198.3-202.3) is released as open ground and the gates are drawn in the build.
Heights come from two Google Street View panoramas (April 2025) on Norra Långgatan resected in pass
75; see references/block80-notes.md.
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
PG=lambda b:Polygon([tuple(w['p']) for w in d17['SM_Kvarnholmen_House_'+b]['walls']]).buffer(0)
P33,P43,P83=PG('90859833'),PG('90859843'),PG('90859883')
# The white house between them is mapped in OSM only as the untagged outer way 90859904 of a
# multipolygon, which the district import dropped: the model had an empty lot there. Its footprint
# is added from that way, and the 1.7 m strip up to 90859843 from the measured front.
P04=Polygon([(241.0,72.1),(253.4,71.7),(253.6,79.6),(241.2,79.9)])
GAP=Polygon([(253.4,71.7),(255.1,71.8),(255.2,79.6),(253.6,79.6)])
OL=P33.intersection(box(200,60,239.05,90))
WH=unary_union([P33.intersection(box(239.05,60,300,90)),P04,GAP]).intersection(box(200,60,254.5,90))
WA=unary_union([GAP,P43]).intersection(box(254.5,60,256.3,79.6))
YB=P43.intersection(box(254.5,79.6,256.3,90))
RD=P43.intersection(box(256.3,60,300,90))
CK=P83.intersection(box(262.3,60,266.3,90))
PB=unary_union([OL,WH,WA,YB,RD,CK]);RELEASED=unary_union([P33,P43,P83]).difference(PB)
seeds=[('ol',OL),('wh',WH),('wa',WA),('yb',YB),('rd',RD),('ck',CK)]
# Heights (m) above the facade base, measured from two Norra Långgatan panoramas: the olive gable
# house's eaves 4.2 and apex 5.2; the white house's eaves 4.9 under a tile roof to 7.3 (estimate);
# its east annex's eaves 4.3 and gable apex 6.2; the red gable house's eaves 4.3 and apex 6.0; the
# cottage's eaves 1.45 and apex 2.8.
spec={'ol':dict(height=4.2,top=5.2,mesh='SM_Kvarnholmen_House_90859833'),'wh':dict(height=4.9,top=7.3,mesh='SM_Kvarnholmen_House_90859904'),
 'wa':dict(height=4.3,top=6.2,mesh='SM_Kvarnholmen_House_90859904'),'rd':dict(height=4.3,top=6.0,mesh='SM_Kvarnholmen_House_90859843'),
 'ck':dict(height=1.45,top=2.8,mesh='SM_Kvarnholmen_House_90859883'),'yb':dict(height=4.3,top=5.3,mesh='SM_Kvarnholmen_House_90859904')}
taken=Polygon();zones={}
for name,seed in seeds:
 ps=parts(seed.difference(taken));zones[name]=ps;taken=unary_union([taken]+ps)
scope={'90859833','90859843','90859883'}
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
# Roofs: the gable-fronted houses have their ridges running back from the street (street and back
# edges upright); the white house's ridge runs along the street (its end edges upright).
def gable_roof(name,along):
 ring=[tuple(round(c,3) for c in v) for v in list(orient(zones[name][0].simplify(.3)).exterior.coords)[:-1]]
 fire=[(abs(q[0]-p[0])>abs(q[1]-p[1]))!=along for p,q in zip(ring,ring[1:]+ring[:1])]
 P=Polygon(ring);mnx,mny,mxx,mxy=P.bounds;half=((mxy-mny) if along else (mxx-mnx))/2-.35
 ins=[0 if f else half for f in fire];r1=inner(ring,ins)
 assert Polygon(r1).is_valid,(name,r1)
 out[name]['roof']=dict(outer=[list(v) for v in ring],r1=[list(v) for v in r1],firewall=fire,inset=half,insets=ins)
for z,al in (('ol',False),('wa',False),('rd',False),('ck',False)):gable_roof(z,al)
# The white house's roof (its outline has a notch at the back) is drawn in the build.
covered=unary_union([p for ps in zones.values() for p in ps]);foot=PB
data={'source':'district volume 90859843 (source/district17.json), '+district['source'],'zones':out,
 'checks':{'footprint_m2':round(foot.area,1),'zoned_m2':round(covered.area,1),'outside_osm_m2':round(covered.difference(foot).area,2),'osm_not_zoned_m2':round(foot.difference(covered).area,2),
  'overlap_m2':round(sum(p.area for ps in zones.values() for p in ps)-covered.area,3),'released_m2':round(RELEASED.area,1)}}
(R/'source/block80.json').write_text(json.dumps(data,indent=1,ensure_ascii=False))
c=data['checks'];ok=c['outside_osm_m2']<.2 and c['osm_not_zoned_m2']<.5 and c['overlap_m2']<.2
(R/'previews/block80-zones.json').write_text(json.dumps({'status':'passed' if ok else 'review_required','zones':report,'checks':c},indent=2,ensure_ascii=False))
print(json.dumps(report));print(c);print('BLOCK80_ZONES_OK' if ok else 'BLOCK80_ZONES_REVIEW')
