"""Pass 42: the district volume 92412873 along Östra Sjögatan, from pass 40's corner house to the
corner of the castle park: the Nordstjernan brewery (roughcast, tall arched windows, a stepped
central gable), two roughcast houses with blind panels and wall dormers, a narrow gabled house and
the yellow corner house Östra Sjögatan 1. The courtyard block behind stays a plain volume. Heights
come from Google Street View panoramas (April 2025) chained along the street; see
references/block42-notes.md.
Run with Shapely on the path: KALMAR_GEO=/path/to/site-packages python3 prepare_block42.py
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
PB=Polygon([tuple(w['p']) for w in d17['SM_Kvarnholmen_House_92412873']['walls']]).buffer(0)
# Street-front ranges on Östra Sjögatan, split at the measured joints (y, from north to south).
CUT=[-93.0,-95.0,-102.6,-106.6,-115.0,-119.1,-126.6,-142.0]
NAMES=['bn','bc','bs','h2','hc','gr','ye']
seeds=[]
for nm,y0,y1 in zip(NAMES,CUT[:-1],CUT[1:]):
 seeds.append((nm,PB.intersection(box(34.5 if nm=='ye' else 37.0,y1,48,y0))))
seeds.append(('bk',PB))
# Heights (m) above the facade base, from the level views and (for the upper storeys) the pitched
# views: the brewery's eaves 11.2 with its central gable to 17.2; house 2 (three storeys and a wall
# dormer) 10.2; the narrow gabled house 10.9; the grey house 11.8 (its shuttered attic storey in the
# wall face under the eaves); the yellow corner house 7.1.
# The courtyard block and the Wahlberg house on the park keep pass 17's height (7.65) and look.
spec={'bn':dict(height=11.2,top=11.6,mesh='SM_Kvarnholmen_House_92412873'),
 'bc':dict(height=11.2,top=13.2,mesh='SM_Kvarnholmen_House_92412873'),
 'bs':dict(height=11.2,top=13.2,mesh='SM_Kvarnholmen_House_92412873'),
 'h2':dict(height=10.2,top=13.0,mesh='SM_Kvarnholmen_House_92412873'),
 'hc':dict(height=10.9,top=13.4,mesh='SM_Kvarnholmen_House_92412873'),
 'gr':dict(height=11.8,top=13.6,mesh='SM_Kvarnholmen_House_92412873'),
 'ye':dict(height=7.1,top=10.4,mesh='SM_Kvarnholmen_House_92412873'),
 'bk':dict(height=7.65,top=10.9,mesh='SM_Kvarnholmen_House_92412873')}
taken=Polygon();zones={}
for name,seed in seeds:
 ps=parts(seed.difference(taken));zones[name]=ps;taken=unary_union([taken]+ps)
scope={'92412873'}
# The pass 40 corner house is the neighbour to the north.
b40=json.loads((R/'source/block40.json').read_text())['zones']
others=[(Polygon(p).buffer(0),z['height'],'block40:'+k) for k,z in b40.items() for p in z['polygons']]+[(Polygon([tuple(w['p']) for w in v['walls']]).buffer(0),v['H'],v['id']) for v in d17.values() if v['id'] not in scope|{'92412846'} and len(v['walls'])>=3]
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
for nm in ('bc','bs','h2','hc','gr'):out[nm]['roof']=roof_ring(nm,3.5)
out['ye']['roof']=roof_ring('ye',3.6)
covered=unary_union([p for ps in zones.values() for p in ps]);foot=PB
data={'source':'district volume 92412873 (source/district17.json), '+district['source'],'zones':out,
 'checks':{'footprint_m2':round(foot.area,1),'zoned_m2':round(covered.area,1),'outside_osm_m2':round(covered.difference(foot).area,2),'osm_not_zoned_m2':round(foot.difference(covered).area,2),
  'overlap_m2':round(sum(p.area for ps in zones.values() for p in ps)-covered.area,3)}}
(R/'source/block42.json').write_text(json.dumps(data,indent=1,ensure_ascii=False))
c=data['checks'];ok=c['outside_osm_m2']<.2 and c['osm_not_zoned_m2']<.5 and c['overlap_m2']<.2
(R/'previews/block42-zones.json').write_text(json.dumps({'status':'passed' if ok else 'review_required','zones':report,'checks':c},indent=2,ensure_ascii=False))
print(json.dumps(report));print(c);print('BLOCK42_ZONES_OK' if ok else 'BLOCK42_ZONES_REVIEW')
