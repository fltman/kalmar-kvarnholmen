"""Pass 30: the corner building Larmgatan 14 / Södra Långgatan (OSM 92204170).

Three storeys under a copper and tile mansard: a pink ground floor with stone-framed openings and a
granite plinth, ochre upper floors, bracketed eaves, a canted corner carrying the corner oriel,
two further oriels, and two tall curved gable bays, one on Södra Långgatan and one at the north end
of the Larmgatan front. The east and north walls above the neighbours are fire walls.
Heights come from Google Street View (April 2025), each camera registered on the building's two
fronts; see references/block30-notes.md. Heights refer to the Södra Långgatan facade base; the
Larmgatan pavement lies 0.17 m lower.
Run with Shapely on the path: KALMAR_GEO=/path/to/site-packages python3 prepare_block30.py
"""
from pathlib import Path
import json,math,os,sys
if os.environ.get('KALMAR_GEO'):sys.path.insert(0,os.environ['KALMAR_GEO'])
from shapely.geometry import Polygon,Point
from shapely.geometry.polygon import orient
from shapely.ops import unary_union
R=Path(__file__).resolve().parents[1]
district=json.loads((R/'source/kvarnholmen.json').read_text());B={b['id']:b for b in district['buildings']}
def ring(bid):
 r=[tuple(p) for p in B[bid]['polygons'][0]['outer']]
 return r[:-1] if r[0]==r[-1] else r
P=Polygon(ring('92204170')).buffer(0)
# The corner is canted with 1.7 m legs: the Södra Långgatan front ends 1.57 m from the OSM corner
# (seen along the street from the east), the canted face measures 2.4-2.7 m against its own shop
# window in a magnified view from the south-west, and the Larmgatan front then ends 22.3 m from the
# joint with Larmgatan 16.
CN=(-285.58,-67.12);LEG=1.7
chamfer=Polygon([(CN[0]-.01,CN[1]-.01),(CN[0]-.01,CN[1]+LEG),(CN[0]+LEG,CN[1]-.01)])
main=orient(P.difference(chamfer).buffer(-.02,join_style=2).buffer(.02,join_style=2).simplify(.02))
# Heights (m) above the Södra Långgatan facade base. Measured: band 5.25-5.47 (5.36 on both fronts
# once the Larmgatan base is allowed for), first-floor windows 5.45-7.75, second floor 9.2-11.45,
# eaves (wall line) 12.4-13.0, the east fire wall's roof profile rising from 12.7 at the front to
# 19.2 4.7 m in and about 20 further back, both gable tops 19.1-19.3 with finials to 20.3.
spec=dict(height=12.8,copper_top=15.6,top=19.8,mesh='SM_Kvarnholmen_House_92204170',
 band=[5.25,5.47],plinth=.55,floors=[[5.45,7.75],[9.2,11.45]],
 # Gable bays: the Södra Långgatan bay between its two downpipes, the north bay on Larmgatan
 # between the joint with Larmgatan 16 and its downpipe.
 gable_sodra=dict(x=[-268.44,-263.38],shoulder=15.3,top=19.2,finial=20.3,oval=[13.2,15.2]),
 gable_north=dict(s=[0.0,4.75],shoulder=15.0,top=19.3,finial=20.25,window=[13.25,14.1]))
district_h={b['id']:b['height'] for b in district['buildings']}
b29=json.loads((R/'source/block29.json').read_text())['zones']
others=[(Polygon(ps).buffer(0),z['height'],'block29:'+n) for n,z in b29.items() for ps in z['polygons']]
others+=[(Polygon(ring(b['id'])).buffer(0),b['height'],b['id']) for b in district['buildings'] if b['id'] not in {'92204170','92204156','92204161','92204198','92204187','92204189'}]
def neighbour_at(pt):
 for g,h,bid in others:
  if g.buffer(.001).contains(pt):return bid,h
 return None,0.0
H=spec['height'];walls=[]
cs=list(main.exterior.coords)[:-1]
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
# Mansard rings: a steep copper lower slope (12.8 -> 15.6) and a tile upper slope (-> 19.8) with
# a flat top. The fire walls (the east side and the north ends above the neighbours) take no
# inset, so the roof rises straight from them, as the east fire wall shows over Södra Långgatan 9.
def merge(ring):
 out=list(ring);changed=True
 while changed:
  changed=False
  for i in range(len(out)):
   a,b,c=out[i-1],out[i],out[(i+1)%len(out)]
   u=(b[0]-a[0],b[1]-a[1]);v=(c[0]-b[0],c[1]-b[1])
   if abs(u[0]*v[1]-u[1]*v[0])<.035*math.hypot(*u)*math.hypot(*v):out.pop(i);changed=True;break
 return out
def firewall(p,q):
 mx,my=(p[0]+q[0])/2,(p[1]+q[1])/2
 return mx>-257.2 or (my>-43.9 and abs(q[1]-p[1])<1.0)
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
outer=merge(cs);fw=[firewall(p,q) for p,q in zip(outer,outer[1:]+outer[:1])]
r1=inner(outer,[0 if f else 1.6 for f in fw])
# At the upper slope's 4.4 m inset the 2.4 m canted face vanishes: the two fronts' slopes meet in a
# hip, so the canted edge is collapsed and its two ring points share the hip's apex.
ch=min(range(len(outer)),key=lambda i:abs(math.dist(outer[i],outer[(i+1)%len(outer)])-2.4))
n=len(r1);a0,a1=r1[(ch-1)%n],r1[ch];b0,b1=r1[(ch+1)%n],r1[(ch+2)%n]
da=(a1[0]-a0[0],a1[1]-a0[1]);db=(b1[0]-b0[0],b1[1]-b0[1]);det=da[0]*(-db[1])-da[1]*(-db[0])
t=((b0[0]-a0[0])*(-db[1])-(b0[1]-a0[1])*(-db[0]))/det;X=(a0[0]+da[0]*t,a0[1]+da[1]*t)
order=[(ch+1+k)%n for k in range(n)]           # starts at the canted edge's far end
r1b=[X]+[r1[i] for i in order[1:-1]];fwb=[fw[i] for i in order[:-1]]
r2b=inner(r1b,[0 if f else 2.8 for f in fwb])
r2=[None]*n;r2[order[0]]=r2b[0];r2[ch]=r2b[0]
for k,i in enumerate(order[1:-1]):r2[i]=r2b[k+1]
for name,r in (('r1',r1),('r2',r2b)):
 g=Polygon(r)
 assert g.is_valid and g.area<Polygon(outer).area and Polygon(outer).buffer(.01).contains(g),name
roof=dict(canted_edge=ch,outer=[list(v) for v in outer],r1=[list(v) for v in r1],r2=[list(v) for v in r2],firewall=fw,
 areas=[round(Polygon(outer).area,1),round(Polygon(r1).area,1),round(Polygon(r2b).area,1)])
zone=dict(spec,polygons=[[list(v) for v in cs]],walls=walls,roof=roof)
data={'source':'OpenStreetMap way 92204170, '+district['source'],'zones':{'main':zone},'chamfer':{'corner':list(CN),'leg':LEG},
 'checks':{'footprint_m2':round(P.area,1),'zoned_m2':round(main.area,1),'chamfer_m2':round(chamfer.intersection(P).area,2),
  'outside_osm_m2':round(main.difference(P).area,2),'osm_not_zoned_m2':round(P.difference(main).area,2)}}
(R/'source/block30.json').write_text(json.dumps(data,indent=1,ensure_ascii=False))
c=data['checks'];ok=c['outside_osm_m2']<.2 and abs(c['osm_not_zoned_m2']-c['chamfer_m2'])<.3
report={'main':{'area_m2':c['zoned_m2'],'walls':len(walls),'outer_m':round(sum(math.dist(w['p'],w['q']) for w in walls if w['kind']=='outer'),1),
 'upper_m':round(sum(math.dist(w['p'],w['q']) for w in walls if w['kind']=='upper'),1)}}
(R/'previews/block30-zones.json').write_text(json.dumps({'status':'passed' if ok else 'review_required','zones':report,'checks':c},indent=2,ensure_ascii=False))
print(report);print(c);print('BLOCK30_ZONES_OK' if ok else 'BLOCK30_ZONES_REVIEW')
