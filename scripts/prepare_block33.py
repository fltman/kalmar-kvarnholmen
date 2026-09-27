"""Pass 33: Södra Långgatan 16 (OSM 92379302), the corner house east of Kaggensgatan.

A white palace-like house of three storeys on the corner of Södra Långgatan and Kaggensgatan: an
open arcade behind the corner pier, shop windows, a projecting risalit with the arched carriage
gate, paired pilasters, a medallion and a pediment, window heads with segmental pediments over the
middle windows of each wing, a console frieze and a dentilled cornice. Heights come from two Google
Street View panoramas (April 2025) registered on the house's corner and east joint; see
references/block33-notes.md. Run with Shapely on the path: KALMAR_GEO=... python3 prepare_block33.py
"""
from pathlib import Path
import json,math,os,sys
if os.environ.get('KALMAR_GEO'):sys.path.insert(0,os.environ['KALMAR_GEO'])
from shapely.geometry import Polygon,Point
from shapely.geometry.polygon import orient
R=Path(__file__).resolve().parents[1]
district=json.loads((R/'source/kvarnholmen.json').read_text());B={b['id']:b for b in district['buildings']}
def ring(bid):
 r=[tuple(p) for p in B[bid]['polygons'][0]['outer']]
 return r[:-1] if r[0]==r[-1] else r
P=orient(Polygon(ring('92379302')).buffer(0))
# Heights (m) above the Södra Långgatan facade base. Flat features straight from the facade plane:
# band 4.40-4.70, first-floor windows 5.50-7.35, second floor 9.25-11.03. Projecting parts are
# triangulated from both panoramas or corrected for their projection: the main cornice's top stands
# at 11.91, 0.8 m out (13.6 on the facade plane); the risalit pediment's apex at 12.99, 0.81 m out
# (rays 0.03 m apart); the risalit face only about 0.1 m proud (medallion, frame). The roof behind the
# cornice is not visible from the street and is an estimate.
spec=dict(height=11.9,top=15.0,mesh='SM_Kvarnholmen_House_92379302',band=[4.40,4.70],floors=[[5.50,7.35],[9.25,11.03]],
 risalit=dict(s=[12.8,17.7],proud=.10,gate=[14.04,16.28],apex=12.99,pediment_width=5.2,windows=[[5.43,7.22],[9.17,10.90]],
  entablature=[7.61,8.09],medallion=8.10,frame_top=8.60,capitals_top=7.28),
 sodra_windows=[2.79,4.92,7.02,9.11,11.26,18.73,20.73,22.85,24.93,27.0],sodra_pediments=[7.02,22.85],
 kagg_windows=[1.30,3.27,5.18,7.17,9.14,11.7,13.7,15.7,17.7,19.7,21.7],kagg_pediments=[5.18],kagg_downpipe=10.31,
 arcade=[1.20,2.69,1.5])
sg=json.loads((R/'source/storgatan.json').read_text())['buildings'];d17=json.loads((R/'source/district17.json').read_text())['buildings']
others=[(Polygon(ring(b['id'])).buffer(0),b['height'],b['id']) for b in district['buildings'] if b['id']!='92379302']
others+=[(Polygon(b['polygon']).buffer(0),d17.get('SM_Building_'+b['id'],{}).get('H',8.0),'storgatan:'+b['id']) for b in sg if b.get('polygon')]
def neighbour_at(pt):
 for g,h,bid in others:
  if g.buffer(.001).contains(pt):return bid,h
 return None,0.0
H=spec['height'];walls=[];cs=list(P.exterior.coords)[:-1]
for p,q in zip(cs,cs[1:]+cs[:1]):
 Lw=math.dist(p,q);ux,uy=(q[0]-p[0])/Lw,(q[1]-p[1])/Lw;nx,ny=uy,-ux;n=max(1,int(Lw/.2));runs=[]
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
# Roof: slopes to the two streets over a 5 m inset, fire walls to the east and north neighbours.
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
def street_edge(p,q):
 mx,my=(p[0]+q[0])/2,(p[1]+q[1])/2
 return my<-66 or mx<-181
fw=[not street_edge(p,q) for p,q in zip(cs,cs[1:]+cs[:1])]
r1=inner(cs,[0 if f else 5.0 for f in fw])
g=Polygon(r1);assert g.is_valid and g.area<P.area and P.buffer(.01).contains(g)
zone=dict(spec,polygons=[[list(v) for v in cs]],walls=walls,roof=dict(outer=[list(v) for v in cs],r1=[list(v) for v in r1],firewall=fw,inset=5.0))
data={'source':'OpenStreetMap way 92379302, '+district['source'],'zones':{'sl16':zone},
 'checks':{'footprint_m2':round(P.area,1),'zoned_m2':round(P.area,1),'outside_osm_m2':0.0,'osm_not_zoned_m2':0.0,'roof_top_m2':round(g.area,1)}}
(R/'source/block33.json').write_text(json.dumps(data,indent=1,ensure_ascii=False))
report={'sl16':{'area_m2':round(P.area,1),'walls':len(walls),'outer_m':round(sum(math.dist(w['p'],w['q']) for w in walls if w['kind']=='outer'),1)}}
(R/'previews/block33-zones.json').write_text(json.dumps({'status':'passed','zones':report,'checks':data['checks']},indent=2,ensure_ascii=False))
print(report,data['checks'],fw);print('BLOCK33_ZONES_OK')
