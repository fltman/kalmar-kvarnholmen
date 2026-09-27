"""Pass 36: OSM way 92379286 on the south side of Södra Långgatan, which holds two houses: the long
cream house next to the palace (with the barber's shop, the arched gate and the curved gable) and
the stone corner house on Kaggensgatan with the portal dated 1659. The joint between them, a
downpipe beside the corner house's quoins, is measured 28.2 m from the palace joint. Each house is
split into a front range on the street and lower ranges behind it. Heights come from Google Street
View panoramas (April 2025) on the camera track of pass 35; see references/block36-notes.md.
Run with Shapely on the path: KALMAR_GEO=/path/to/site-packages python3 prepare_block36.py
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
P=Polygon(ring('92379286')).buffer(0)
# The joint between the two houses on the street front (s 28.2 m from the palace joint), carried
# straight back to the corner house's rear wall.
F0,F1=(-139.797,-79.661),(-181.708,-79.268)
L=math.dist(F0,F1);ux,uy=(F1[0]-F0[0])/L,(F1[1]-F0[1])/L
JF=(F0[0]+ux*28.2,F0[1]+uy*28.2)
WEST=Polygon([(JF[0],-70),(-200,-70),(-200,-100),(JF[0],-100)])
EAST=P.difference(WEST).buffer(0);CORNER=P.intersection(WEST).buffer(0)
# The cream house's front range reaches the courtyard wall (y -86.6 to -86.9); its west end
# (x -160.4 to the joint) and the wing behind its east part are lower rear ranges.
FRONT=Polygon([(-139.0,-78.0),(JF[0],-78.0),(JF[0],-86.62),(-160.449,-86.575),(-147.175,-86.896),(-139.0,-86.90)])
seeds=[('cr',EAST.intersection(FRONT)),('crr',EAST.difference(FRONT)),('kh',CORNER)]
# Heights (m) above the facade base. The cream house: upper windows 4.64-6.29, the band under the
# eaves 6.35-6.78 on the facade plane, the gutter 0.45 m out, so the eaves at 6.52; the ridge 10.75
# from the sky line in the pitched view, over the middle of the 7.2 m deep front range. The corner
# house: band 5.09-5.35, upper windows 5.87-8.23, the cornice 8.75-9.4 (corrected for its
# projection); its roof is not seen from the street and is estimated.
spec={'cr':dict(height=6.52,top=10.75,mesh='SM_Kvarnholmen_House_92379286'),
 'crr':dict(height=5.6,top=8.2,mesh='SM_Kvarnholmen_House_92379286'),
 'kh':dict(height=9.35,top=13.0,mesh='SM_Kvarnholmen_House_92379286')}
taken=Polygon();zones={}
for name,seed in seeds:
 ps=parts(seed.difference(taken));zones[name]=ps;taken=unary_union([taken]+ps)
scope={'92379286'}
others=[(Polygon(ring(b['id'])).buffer(0),b['height'],b['id']) for b in district['buildings'] if b['id'] not in scope|{'92379296'}]
b35=json.loads((R/'source/block35.json').read_text())['zones']
others+=[(Polygon(p).buffer(0),z['height'],'block35:'+k) for k,z in b35.items() for p in z['polygons']]
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
# The cream house's front range: a saddle roof with fire walls at the palace and at the corner
# house; the corner house: a hipped roof over its whole block (street, Kaggensgatan and the rear),
# with a fire wall to the cream house.
fronts={'cr':([F0,JF,(JF[0],-86.62),(-139.797+(-140.16+139.797)*(86.9-79.661)/(103.718-79.661),-86.90)],[False,True,False,True],3.6),
 'kh':([JF,F1,(-181.78,-91.469),(JF[0],-91.864)],[False,False,False,True],6.0)}
for name,(fr,fw,inset) in fronts.items():
 fr=[(round(p[0],3),round(p[1],3)) for p in fr]
 r1=inner(fr,[0 if f else inset for f in fw])
 g=Polygon(r1);ok=Polygon(fr).exterior.is_ccw and g.is_valid and Polygon(fr).buffer(.01).contains(g)
 if name=='kh':
  # A hip roof collapses to a ridge: the inset ring is degenerate, so keep the ridge line only.
  ok=Polygon(fr).exterior.is_ccw
 assert ok,name
 out[name]['roof']=dict(outer=[list(v) for v in fr],r1=[list(v) for v in r1],firewall=fw,inset=inset)
out['cr']['joint']=[round(JF[0],3),round(JF[1],3)]
covered=unary_union([p for ps in zones.values() for p in ps])
data={'source':'OpenStreetMap way 92379286, '+district['source'],'zones':out,
 'checks':{'footprint_m2':round(P.area,1),'zoned_m2':round(covered.area,1),'outside_osm_m2':round(covered.difference(P).area,2),'osm_not_zoned_m2':round(P.difference(covered).area,2),
  'overlap_m2':round(sum(p.area for ps in zones.values() for p in ps)-covered.area,3)}}
(R/'source/block36.json').write_text(json.dumps(data,indent=1,ensure_ascii=False))
c=data['checks'];ok=c['outside_osm_m2']<.2 and c['osm_not_zoned_m2']<.5 and c['overlap_m2']<.2
(R/'previews/block36-zones.json').write_text(json.dumps({'status':'passed' if ok else 'review_required','zones':report,'checks':c},indent=2,ensure_ascii=False))
print(json.dumps(report));print(c);print('BLOCK36_ZONES_OK' if ok else 'BLOCK36_ZONES_REVIEW')
