"""Pass 81: the east end of Norra Långgatan, both sides from x 268 to 296: nine district volumes
(93192447, 93192416, 93192390, 93192433 on the south side; 90859897, 90859890, 90859875, 90859864,
90859880 on the north side) split at measured joints into eleven small houses; gate strips released.
Heights from two Google Street View panoramas (April 2025); see references/block81-notes.md.
"""
_OLD="""Pass 80: the district volumes 90859833, 90859843 and 90859883 on the north side of Norra
Långgatan east of pass 76, and the missing white house between them (OSM way 90859904).
"""
_OLD_DOC="""Pass 76: the district volumes 90859889, 90859896 and 90859843 on the north side of Norra
Långgatan, opposite pass 75, split at their measured joints into five houses: the green boarded
cottage with its cross gable, the red house with white windows, the red house with green windows
and the orange door, a narrow boarded passage door, and the white gable-fronted house with its
low back annex. The two carriage gates between the green and the red houses open onto a yard: that
strip (x 198.3-202.3) is released as open ground and the gates are drawn in the build.
Heights come from two Google Street View panoramas (April 2025) on Norra Långgatan resected in pass
75; see references/block81-notes.md.
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
S47,S16,S90,S33=PG('93192447'),PG('93192416'),PG('93192390'),PG('93192433')
N97,N90,N75,N64,N80=PG('90859897'),PG('90859890'),PG('90859875'),PG('90859864'),PG('90859880')
# The 1.4 m between 93192390 and 93192433 is covered by the green house's roof over its gateway.
SGAP=Polygon([(288.1,60.7),(289.5,60.4),(289.5,52.6),(288.0,51.3)])
SOUTH=unary_union([S47,S16,S90,S33,SGAP]);NORTH=unary_union([N97,N90,N75,N64,N80])
cut=lambda P,a,b:P.intersection(box(a,40,b,100))
# Zones split at the joints measured from the two panoramas (x along the street).
seeds=[('yl',cut(S47,268.6,273.3)),('gc',cut(S16,276.06,281.6)),('gg',cut(SOUTH,281.6,288.72)),('gs',cut(SOUTH,288.72,291.1)),('or',cut(SOUTH,291.1,300)),
 ('ck',cut(N97,272.35,276.84)),('rd',cut(NORTH,276.84,279.67)),('wb',cut(NORTH,279.67,284.56)),('ws',cut(NORTH,284.56,287.6)),('sr',cut(NORTH,287.6,292.55)),('br',cut(NORTH,292.55,300))]
PB=unary_union([g for n,g in seeds]);RELEASED=unary_union([SOUTH,NORTH]).difference(PB)
# Heights (m) above the facade base: the eaves measured; gable apexes measured where the gable faces
# the street, ridges along the street estimated.
spec={'yl':dict(height=3.04,top=4.22,mesh='SM_Kvarnholmen_House_93192447',rooftype='gable'),
 'gc':dict(height=1.92,top=3.39,mesh='SM_Kvarnholmen_House_93192416',rooftype='gable'),
 'gg':dict(height=4.2,top=6.38,mesh='SM_Kvarnholmen_House_93192390',rooftype='gable'),
 'gs':dict(height=4.16,top=5.4,mesh='SM_Kvarnholmen_House_93192390',rooftype='along'),
 'or':dict(height=3.67,top=5.43,mesh='SM_Kvarnholmen_House_93192433',rooftype='gable'),
 'ck':dict(height=1.78,top=3.22,mesh='SM_Kvarnholmen_House_90859897',rooftype='gable'),
 'rd':dict(height=2.9,top=4.2,mesh='SM_Kvarnholmen_House_90859890',rooftype='along'),
 'wb':dict(height=4.37,top=5.62,mesh='SM_Kvarnholmen_House_90859890',rooftype='gable'),
 'ws':dict(height=2.93,top=4.0,mesh='SM_Kvarnholmen_House_90859875',rooftype='along'),
 'sr':dict(height=2.7,top=3.9,mesh='SM_Kvarnholmen_House_90859864',rooftype='along'),
 'br':dict(height=3.8,top=5.52,mesh='SM_Kvarnholmen_House_90859880',rooftype='gable')}
taken=Polygon();zones={}
for name,seed in seeds:
 ps=parts(seed.difference(taken));zones[name]=ps;taken=unary_union([taken]+ps)
scope={'93192447','93192416','93192390','93192433','90859897','90859890','90859875','90859864','90859880'}
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
 for tol in (.3,.6,1.0,1.5,2.5):
  ring=[tuple(round(c,3) for c in v) for v in list(orient(zones[name][0].simplify(tol)).exterior.coords)[:-1]]
  if len(ring)==4:break
 fire=[(abs(q[0]-p[0])>abs(q[1]-p[1]))!=along for p,q in zip(ring,ring[1:]+ring[:1])]
 P=Polygon(ring);mnx,mny,mxx,mxy=P.bounds;half=((mxy-mny) if along else (mxx-mnx))/2-.35
 ins=[0 if f else half for f in fire];r1=inner(ring,ins)
 if not (Polygon(r1).is_valid and len(ring)==4):return  # irregular outlines get a hipped roof in the build
 out[name]['roof']=dict(outer=[list(v) for v in ring],r1=[list(v) for v in r1],firewall=fire,inset=half,insets=ins)
for z in spec:gable_roof(z,spec[z]['rooftype']=='along')
covered=unary_union([p for ps in zones.values() for p in ps]);foot=PB
data={'source':'district volume 90859843 (source/district17.json), '+district['source'],'zones':out,
 'checks':{'footprint_m2':round(foot.area,1),'zoned_m2':round(covered.area,1),'outside_osm_m2':round(covered.difference(foot).area,2),'osm_not_zoned_m2':round(foot.difference(covered).area,2),
  'overlap_m2':round(sum(p.area for ps in zones.values() for p in ps)-covered.area,3),'released_m2':round(RELEASED.area,1)}}
(R/'source/block81.json').write_text(json.dumps(data,indent=1,ensure_ascii=False))
c=data['checks'];ok=c['outside_osm_m2']<.2 and c['osm_not_zoned_m2']<.5 and c['overlap_m2']<.2
(R/'previews/block81-zones.json').write_text(json.dumps({'status':'passed' if ok else 'review_required','zones':report,'checks':c},indent=2,ensure_ascii=False))
print(json.dumps(report));print(c);print('BLOCK81_ZONES_OK' if ok else 'BLOCK81_ZONES_REVIEW')
