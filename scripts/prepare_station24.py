"""Pass 24: split the two mapped station footprints (OSM 90965009, 90965025) into the
photographed parts: the 1874 range, the 1910 block, its round corner tower and the lower
south wing. Seeds come from Street View (April 2025), Commons photographs and an orthophoto.
Run with Shapely on the path: KALMAR_GEO=/path/to/site-packages python3 prepare_station24.py
"""
from pathlib import Path
import json,math,os,sys
if os.environ.get('KALMAR_GEO'):sys.path.insert(0,os.environ['KALMAR_GEO'])
from shapely.geometry import Polygon,Point
from shapely.geometry.polygon import orient
from shapely.ops import unary_union
R=Path(__file__).resolve().parents[1]
district=json.loads((R/'source/kvarnholmen.json').read_text())
def ring(bid):
 r=[tuple(p) for p in next(b for b in district['buildings'] if b['id']==bid)['polygons'][0]['outer']]
 return r[:-1] if r[0]==r[-1] else r
old,new=ring('90965009'),ring('90965025')
# Frame of the 1910 street front: origin at its north corner, 'along' towards the tower,
# 'depth' towards the tracks. Every seed below is written in this frame.
O=new[2];U=(new[3][0]-O[0],new[3][1]-O[1]);L=math.hypot(*U);U=(U[0]/L,U[1]/L)
# The depth axis is the normal of the street front that points at the track front (vertex 15).
N=(-U[1],U[0]) if (-U[1])*(new[15][0]-O[0])+U[0]*(new[15][1]-O[1])>0 else (U[1],-U[0])
def xy(a,d):return (round(O[0]+U[0]*a+N[0]*d,3),round(O[1]+U[1]*a+N[1]*d,3))
def ad(p):r=(p[0]-O[0],p[1]-O[1]);return (r[0]*U[0]+r[1]*U[1],r[0]*N[0]+r[1]*N[1])
# Corner tower: least-squares circle through the mapped bulge (vertices 4-9).
pts=[ad(p) for p in new[4:10]]
A=[[2*a,2*d,1] for a,d in pts];bb=[a*a+d*d for a,d in pts]
# Normal equations of the Kasa fit, solved by Cramer's rule.
M=[[sum(A[k][i]*A[k][j] for k in range(len(A))) for j in range(3)] for i in range(3)];v=[sum(A[k][i]*bb[k] for k in range(len(A))) for i in range(3)]
def det3(m):return m[0][0]*(m[1][1]*m[2][2]-m[1][2]*m[2][1])-m[0][1]*(m[1][0]*m[2][2]-m[1][2]*m[2][0])+m[0][2]*(m[1][0]*m[2][1]-m[1][1]*m[2][0])
D=det3(M);sol=[det3([[v[r] if c==i else M[r][c] for c in range(3)] for r in range(3)])/D for i in range(3)]
ca,cd=sol[0],sol[1];rad=math.sqrt(sol[2]+ca*ca+cd*cd)
tower=[xy(ca+rad*math.cos(k*math.tau/32),cd+rad*math.sin(k*math.tau/32)) for k in range(32)]
# 1874 range: the four mapped corners; the 0.3 m notch at its north corner is dropped. Two
# independent April 2025 panoramas (5 Stationsgatan, headings 190/205 and 240) both place the
# north-west gable 1.4-1.7 m beyond the mapped one, so it is moved out by 1.6 m.
EXT=1.6
def beyond(p,frm,d):v=(p[0]-frm[0],p[1]-frm[1]);l=math.hypot(*v);return (round(p[0]+v[0]/l*d,3),round(p[1]+v[1]/l*d,3))
range1874=[old[0],beyond(old[2],old[0],EXT),beyond(old[7],old[8],EXT),old[8]]
site=unary_union([Polygon(old),Polygon(new),Polygon(tower),Polygon(range1874)]).buffer(.01,join_style=2).buffer(-.01,join_style=2)
# 1910 block: the street front up to the tower, the track front to the mapped jog at 18.47 m.
e15=ad(new[15]);main=[new[2],xy(e15[0],0.0),new[15],new[16],new[17],new[0],new[1]]
# South wing: everything east of the block's track corner, outside the tower.
wing=[xy(e15[0],0.0),xy(26.0,0.0),xy(26.0,18.0),xy(e15[0],18.0)]
seeds=[('tower',tower),('main',main),('range1874',range1874),('wing',wing)]
# Heights from the April 2025 Street View front, inverted through the pano camera (see notes):
# 1910 cornice 13.0 m (its 0.78 m projection taken into account), clock 15.3 m, roof break 16.1 m
# at a 1.6 m inset, lantern base 20.9 m, lantern body top 22.3 m, tower body 9.4 m, slate drum 11.5 m. The 1874 eave (9.3 m) and the south wing are estimated from the same view.
spec={'range1874':dict(height=9.3,top=12.7,roof='copper_hip',mesh='SM_Kvarnholmen_House_90965009'),
 'main':dict(height=13.0,band=16.1,inset=1.6,top=20.9,roof='pyramid',mesh='SM_Kvarnholmen_House_90965025'),
 'tower':dict(height=11.5,body=9.4,top=19.5,roof='bell',mesh='SM_Kvarnholmen_House_90965025'),
 'wing':dict(height=10.2,top=12.8,roof='hip',mesh='SM_Kvarnholmen_House_90965025')}
def flat(g):
 g=g.buffer(0);return [g] if g.geom_type=='Polygon' else [q for c in getattr(g,'geoms',[]) for q in flat(c)]
def parts(g):return [orient(r) for q in flat(g) for r in flat(q.buffer(-.02,join_style=2).buffer(.02,join_style=2).simplify(.02)) if r.area>1.0]
taken=Polygon();zones={}
for name,seed in seeds:
 ps=parts(Polygon(seed).buffer(0).intersection(site).difference(taken));zones[name]=ps;taken=unary_union([taken]+ps)
def zone_at(pt):
 for name,ps in zones.items():
  if any(p.buffer(.001).contains(pt) for p in ps):return name
 return None
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
    t=(k+.5)/n;nb=zone_at(Point(p[0]+ux*Lw*t+nx*.3,p[1]+uy*Lw*t+ny*.3))
    if runs and runs[-1][0]==nb:runs[-1][2]=(k+1)/n
    else:runs.append([nb,k/n,(k+1)/n])
   for nb,t0,t1 in runs:
    z0=0.0 if nb is None else spec[nb]['height']
    if z0>=H-.05:continue
    a=(round(p[0]+ux*Lw*t0,3),round(p[1]+uy*Lw*t0,3));b=(round(p[0]+ux*Lw*t1,3),round(p[1]+uy*Lw*t1,3))
    if math.dist(a,b)<.2:continue
    walls.append({'p':list(a),'q':list(b),'z0':z0,'z1':H,'kind':'outer' if nb is None else 'upper','neighbour':nb})
 out[name]=dict(spec[name],polygons=[[list(v) for v in list(p.exterior.coords)[:-1]] for p in ps],walls=walls)
 report[name]={'area_m2':round(sum(p.area for p in ps),1),'polygons':len(ps),'walls':len(walls)}
covered=unary_union([p for ps in zones.values() for p in ps])
footprint=unary_union([Polygon(old),Polygon(new)])
data={'source':'OpenStreetMap ways 90965009 and 90965025 (Kalmar C), '+district['source'],
 'frame':{'origin':list(O),'along':list(U),'depth':list(N)},
 'tower':{'centre':list(xy(ca,cd)),'radius':round(rad,3),'centre_frame':[round(ca,3),round(cd,3)]},
 'range1874':{'corners':[list(p) for p in range1874]},
 'main_frame':{'along':round(e15[0],3),'depth':round(e15[1],3)},
 'zones':out,
 'checks':{'footprint_m2':round(footprint.area,1),'zoned_m2':round(covered.area,1),'tower_outside_osm_m2':round(Polygon(tower).difference(footprint).area,1),'range_extension_outside_osm_m2':round(Polygon(range1874).difference(footprint).area,1),
  'osm_not_zoned_m2':round(footprint.difference(covered).area,2),'overlap_m2':round(sum(p.area for ps in zones.values() for p in ps)-covered.area,3)}}
(R/'source/station24.json').write_text(json.dumps(data,indent=1,ensure_ascii=False))
ok=data['checks']['osm_not_zoned_m2']<1 and data['checks']['overlap_m2']<.5
(R/'previews/station24-zones.json').write_text(json.dumps({'status':'passed' if ok else 'review_required','zones':report,'checks':data['checks'],'tower':data['tower']},indent=2,ensure_ascii=False))
print(json.dumps(report,ensure_ascii=False));print(data['checks'],data['tower']);print('STATION24_ZONES_OK')
