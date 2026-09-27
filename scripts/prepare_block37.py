"""Pass 37: OSM way 92379313 on the south side of Södra Långgatan, east of the wooden house of pass
35, which holds three houses: the grey three-storey office house (with the iron gate and the stone
door surround), the yellow two-storey house number 28 (with the garage door dated 1951) and the
corner house on Ölandsgatan with the toy shop. Their joints are measured 25.5 m and 51.2 m from the
wooden house. Each gets a front range on Södra Långgatan; the large courtyard block behind stays a
plain lower range. Heights come from Google Street View panoramas (April 2025), each registered on
its own house's two joints; see references/block37-notes.md.
Run with Shapely on the path: KALMAR_GEO=/path/to/site-packages python3 prepare_block37.py
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
P=Polygon(ring('92379313')).buffer(0)
F0,F1=(-105.127,-79.872),(-41.648,-80.664)
L=math.dist(F0,F1);ux,uy=(F1[0]-F0[0])/L,(F1[1]-F0[1])/L
def at(s):return (F0[0]+ux*s,F0[1]+uy*s)
J1,J2=at(25.5),at(51.2)
# Strips across the front range between the joints (perpendicular to the street), 13.2 m deep.
def strip(sa,sb,depth=13.3):
 a,b=at(sa),at(sb);nx,ny=uy,-ux   # into the block (south)
 return Polygon([a,b,(b[0]+nx*depth,b[1]+ny*depth),(a[0]+nx*depth,a[1]+ny*depth)])
FRONT=strip(-2,66)
seeds=[('gr',P.intersection(strip(-2,25.5))),('ye',P.intersection(strip(25.5,51.2))),('lh',P.intersection(strip(51.2,66))),('bk',P.difference(FRONT))]
# Heights (m) above the facade base. The grey house: shop fronts to 3.1, band 3.53-3.72, windows
# 4.60-6.49 and 7.62-9.19, a frieze 9.82-10.4 under the eaves (10.3, corrected for its projection).
# The yellow house: shop fronts and the garage to 2.68, windows 4.06-5.52 and 7.12-8.46, eaves 9.2.
# The corner house: shop fronts to 2.27, a band 2.97-3.17, windows 3.63-5.63 and 6.61-8.37, eaves
# about 9.4 and an attic storey with a dormer. The roofs above the eaves and the courtyard block are
# estimates.
spec={'gr':dict(height=10.3,top=12.8,mesh='SM_Kvarnholmen_House_92379313'),
 'ye':dict(height=9.2,top=12.3,mesh='SM_Kvarnholmen_House_92379313'),
 'lh':dict(height=9.4,top=12.5,mesh='SM_Kvarnholmen_House_92379313'),
 'bk':dict(height=7.0,top=9.0,mesh='SM_Kvarnholmen_House_92379313')}
taken=Polygon();zones={}
for name,seed in seeds:
 ps=parts(seed.difference(taken));zones[name]=ps;taken=unary_union([taken]+ps)
scope={'92379313'}
others=[(Polygon(ring(b['id'])).buffer(0),b['height'],b['id']) for b in district['buildings'] if b['id'] not in scope|{'92379316'}]
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
# Front-range roofs: slopes to the street and the courtyard, fire walls at the party walls (the
# corner house's east end is hipped toward Ölandsgatan).
def front_ring(sa,sb,depth=13.0):
 a,b=at(sa),at(sb);nx,ny=uy,-ux
 return [b,a,(a[0]+nx*depth,a[1]+ny*depth),(b[0]+nx*depth,b[1]+ny*depth)]      # counter-clockwise
# edges: street, west party wall, courtyard, east party wall (the corner house's east end is hipped)
fronts={'gr':(front_ring(0,25.5),[False,True,False,True],5.0),'ye':(front_ring(25.5,51.2),[False,True,False,True],5.0),'lh':(front_ring(51.2,63.5),[False,True,False,False],5.0)}
for name,(fr,fw,inset) in fronts.items():
 fr=[(round(p[0],3),round(p[1],3)) for p in fr]
 r1=inner(fr,[0 if f else inset for f in fw])
 assert Polygon(fr).exterior.is_ccw and Polygon(r1).is_valid,name
 out[name]['roof']=dict(outer=[list(v) for v in fr],r1=[list(v) for v in r1],firewall=fw,inset=inset)
out['gr']['joints']=[[round(v,3) for v in J1],[round(v,3) for v in J2]]
covered=unary_union([p for ps in zones.values() for p in ps])
data={'source':'OpenStreetMap way 92379313, '+district['source'],'zones':out,
 'checks':{'footprint_m2':round(P.area,1),'zoned_m2':round(covered.area,1),'outside_osm_m2':round(covered.difference(P).area,2),'osm_not_zoned_m2':round(P.difference(covered).area,2),
  'overlap_m2':round(sum(p.area for ps in zones.values() for p in ps)-covered.area,3)}}
(R/'source/block37.json').write_text(json.dumps(data,indent=1,ensure_ascii=False))
c=data['checks'];ok=c['outside_osm_m2']<.2 and c['osm_not_zoned_m2']<.5 and c['overlap_m2']<.2
(R/'previews/block37-zones.json').write_text(json.dumps({'status':'passed' if ok else 'review_required','zones':report,'checks':c},indent=2,ensure_ascii=False))
print(json.dumps(report));print(c);print('BLOCK37_ZONES_OK' if ok else 'BLOCK37_ZONES_REVIEW')
