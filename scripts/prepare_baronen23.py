"""Pass 23: split the mapped Baronen footprint into the photographed building parts.
Zones follow the OSM outline; seeds come from Street View, the 2015 museum photo and
an orthophoto reprojected into the local frame. Heights are estimates, see notes.
Run with Shapely on the path: KALMAR_GEO=/path/to/site-packages python3 prepare_baronen23.py
"""
from pathlib import Path
import json,math,os,sys
if os.environ.get('KALMAR_GEO'):sys.path.insert(0,os.environ['KALMAR_GEO'])
from shapely.geometry import Polygon,LineString,Point,MultiPolygon
from shapely.geometry.polygon import orient
from shapely.ops import unary_union
R=Path(__file__).resolve().parents[1]
district=json.loads((R/'source/kvarnholmen.json').read_text())
ring=[tuple(p) for p in next(b for b in district['buildings'] if b['id']=='38033725')['polygons'][0]['outer']]
if ring[0]==ring[-1]:ring=ring[:-1]
def P(x,y):
 # Snap to the mapped vertex so the zones share the OSM coordinates exactly.
 return min(ring,key=lambda p:math.dist(p,(x,y)))
def add(a,b,s=1):return (a[0]+b[0]*s,a[1]+b[1]*s)
def unit(a,b):d=math.dist(a,b);return ((b[0]-a[0])/d,(b[1]-a[1])/d)
# The mapped ring runs clockwise, so the right-hand normal of a ring edge points inside.
def rn(u):return (u[1],-u[0])
def meet(p,u,q,v):
 det=u[0]*(-v[1])-u[1]*(-v[0]);t=((q[0]-p[0])*(-v[1])-(q[1]-p[1])*(-v[0]))/det;return add(p,u,t)
P0,P1,P2,P3=P(-104.165,-309.343),P(-152.887,-356.556),P(-155.812,-355.227),P(-178.333,-364.903)
P4,P5,P6,P7=P(-221.399,-360.581),P(-251.648,-344.589),P(-269.279,-327.241),P(-289.117,-307.004)
P8,P9,P10,P11=P(-272.384,-290.284),P(-279.572,-282.628),P(-258.166,-262.629),P(-201.927,-272.068)
P12,P13,P14,P15=P(-203.244,-275.91),P(-198.108,-277.464),P(-198.474,-284.619),P(-192.447,-285.198)
P20,P21,P22,P23=P(-179.671,-279.922),P(-180.321,-284.449),P(-182.497,-286.592),P(-177.642,-296.256)
P24,P25,P26,P27,P28=P(-163.607,-298.148),P(-152.576,-327.986),P(-146.167,-322.934),P(-152.093,-314.502),P(-147.339,-308.147)
P29,P30,P31,P32,P33,P34=P(-133.348,-324.516),P(-119.812,-311.273),P(-135.847,-294.768),P(-177.18,-291.628),P(-175.915,-279.637),P(-130.116,-283.302)
footprint=orient(Polygon(ring).buffer(0))
# The 4 m slot between the entrance octagon and the brick gable is glazed in every
# photograph and roofed in the orthophoto; it is filled as a documented addition.
channel=Polygon([P20,P33,P32,P23,P22,P21]).buffer(0)
# Entrance octagon: a square with 3.1 m chamfers, flat face to the plaza (Street View, orthophoto).
# Its regular outline replaces the irregular mapped facets (< 1 m difference).
cx,cy,ha,hb,ch=-186.4,-281.2,6.8,6.6,3.1
octagon=[(cx+ha,cy+hb-ch),(cx+ha-ch,cy+hb),(cx-ha+ch,cy+hb),(cx-ha,cy+hb-ch),(cx-ha,cy-hb+ch),(cx-ha+ch,cy-hb),(cx+ha-ch,cy-hb),(cx+ha,cy-hb+ch)]
# Mansard L: north wing 13.4 m deep behind Skeppsbrogatan, west wing ends in the harbour gable P9-P8.
# The Street View calibration shows the house running on to the mapped step P11-P12-P13-P14;
# only the narrow glass link P14-P15 remains between it and the octagon.
east_wall=unit(P11,P12);P11i=add(P11,east_wall,13.4);Km=meet(P11i,unit(P11,P10),P8,unit(P9,P10));K2=meet(P11i,unit(P11,P10),P14,(0.0,-1.0))
mansard=[P8,Km,K2,P14,P13,P12,P11,P10,P9]
westlink=[P14,P15,(cx-ha+ch,cy-hb),(-196.0,-290.2),K2]
# Brick factory: an L of two 12 m wings; the NE return stops 22 m along the Skeppsbron gable.
ne=unit(P34,P0);J1=add(P34,ne,22.0);J2=meet(J1,rn(ne),P31,unit(P31,P30))
brick=[P33,P34,J1,J2,P31,P32]
# Packhuset: cream NE block plus the 9.4 m harbour wing along the marina quay. Three storeys
# under the red dormers: the April 2025 view puts its upper windows level with the brick top floor.
P1i=add(P1,rn(unit(P0,P1)),9.4)
hotel=[J1,P0,P1,P2,P1i,P29,P30,J2]
# Inner courtyard wing: 10 m wide, 44 m long, parallel to the mapped courtyard face P24-P25.
d=unit(P24,P25);P24w=add(P24,rn(d),10.0);inner=[P24w,P24,add(P24,d,44.0),add(P24w,d,44.0)]
annex=[P25,P26,P27,P28,P29,add(P24,d,44.0)]
plant=[(-161.0,-336.0),(-146.0,-336.0),(-151.0,-360.0),(-168.0,-362.0)]
# Gym box: 7 m deep in front of the south mansard wing, over the loading bay and ramp portal.
u76=unit(P7,P6);in87=rn(unit(P7,P8));in67=rn(unit(P6,P7))
S1=add(P7,u76,7.0);S2=P6;gym=[P7,S1,add(S1,unit(P7,P8),math.dist(P7,P8)),P8]
# South mansard wing: the same salmon facade reaches the quay from 7 m past P7 to the corner P6
# (bearings -1.2 to 11.3 degrees from Stuvaregatan, April 2025).
mansard_s=[S1,S2,add(S2,in67,26.0),add(S1,in67,26.0)]
# Mister York glass pavilion in front of the west wing, just north of P9: it spans bearings
# 103-126 degrees from the September 2021 Ölandskajen panorama. Outside the mapped outline.
u109=unit(P10,P9);out109=rn(unit(P10,P9));A0=add(P9,u109,-12.0);A1=P9;pavilion=[A0,A1,add(A1,out109,8.0),add(A0,out109,8.0)]
# The red cinema wall reaches the quay up to bearing 18 degrees: 8.5 m past P6.
G3=add(P6,unit(P6,P5),8.5)
site=unary_union([footprint,channel,Polygon(octagon),Polygon(pavilion)]).buffer(.01,join_style=2).buffer(-.01,join_style=2)
# Parking deck: 9.5 m band inside the quay facades, on the roof of the single-storey shop row.
# Two doors per 4.6 m storey height in the April 2025 harbour view fix the deck level.
quay=LineString([G3,P5,P4,P3,P2])
deckband=quay.buffer(9.5,single_sided=True).union(quay.buffer(-9.5,single_sided=True)).intersection(site)
# Tall pale box behind the deck: its 37 m face spans 18-48 degrees from Stuvaregatan (April 2025).
# The right edge sits at 44.5 degrees, so the face is 32.4 m, not 37 m.
FL,FR=(-259.5,-322.5),(-233.58,-341.94);box_n=(0.6,0.8)
tallbox=[add(FL,box_n,-3),add(FR,box_n,-3),add(FR,box_n,24),add(FL,box_n,24)]
southblock=[(-231.0,-315.5),(-158.0,-315.5),(-158.0,-362.0),(-231.0,-362.0)]
# Biostaden (OSM cinema node at -252.8,-290.0): the tall red block seen left of the pale box
# from Stuvaregatan, casting the long shadow on the mansard roof in the orthophoto.
cinema=[P6,G3,FL,add(FL,box_n,24),add(S2,in67,26.0)]
seeds=[('tower',octagon),('mansard',mansard),('mansard_s',mansard_s),('pavilion',pavilion),('westlink',westlink),('channel',[P20,P33,P32,P23,P22,P21]),('brick',brick),('hotel',hotel),('inner',inner),('annex',annex),('plant',plant),('gym',gym),('deck',None),('tallbox',tallbox),('cinema',cinema),('southblock',southblock)]
spec={
 'tower':dict(height=11.3,top=12.7,roof='octagon',mesh='SM_Baronen23_Entrance'),
 'mansard':dict(height=12.0,top=15.1,roof='mansard',mesh='SM_Kvarnholmen_House_38033725'),
 'mansard_s':dict(height=12.0,top=15.1,roof='mansard',mesh='SM_Kvarnholmen_House_38033725'),
 'pavilion':dict(height=7.6,roof='glass',mesh='SM_Baronen23_Harbour'),
 'westlink':dict(height=11.0,roof='flat',mesh='SM_Baronen23_Entrance'),
 'channel':dict(height=7.6,roof='flat',mesh='SM_Baronen23_Entrance'),
 'brick':dict(height=10.4,top=13.6,roof='bent_gable',mesh='SM_Baronen23_Factory'),
 'hotel':dict(height=8.8,top=12.6,roof='bent_hip',mesh='SM_Baronen23_Packhuset'),
 'inner':dict(height=9.3,top=13.4,roof='gable',mesh='SM_Baronen23_Packhuset'),
 'annex':dict(height=6.0,top=8.6,roof='hip',mesh='SM_Baronen23_Packhuset'),
 'plant':dict(height=6.2,roof='flat',mesh='SM_Baronen23_Halls'),
 'gym':dict(height=8.8,roof='flat',mesh='SM_Baronen23_Harbour'),
 'deck':dict(height=4.6,roof='deck',mesh='SM_Baronen23_Harbour'),
 'tallbox':dict(height=16.5,roof='flat',mesh='SM_Baronen23_Halls'),
 'cinema':dict(height=16.4,roof='flat',mesh='SM_Baronen23_Halls'),
 'southblock':dict(height=9.8,roof='flat',mesh='SM_Baronen23_Halls'),
 'mall':dict(height=9.4,roof='flat',mesh='SM_Baronen23_Halls')}
def flat(g):
 g=g.buffer(0)
 return [g] if g.geom_type=='Polygon' else [q for c in getattr(g,'geoms',[]) for q in flat(c)]
def parts(g):
 # Opening removes slivers thinner than 4 cm; it can split a zone, so flatten again.
 return [orient(r) for q in flat(g) for r in flat(q.buffer(-.02,join_style=2).buffer(.02,join_style=2).simplify(.03)) if r.area>1.5]
taken=Polygon();zones={}
for name,seed in seeds:
 g=deckband if seed is None else Polygon(seed).buffer(0).intersection(site)
 g=g.difference(taken);ps=parts(g)
 zones[name]=ps;taken=unary_union([taken]+ps)
zones['mall']=parts(site.difference(taken))
def coords(p):return [[round(x,3),round(y,3)] for x,y in list(p.exterior.coords)[:-1]]
def zone_at(pt):
 for name,ps in zones.items():
  if any(p.buffer(.001).contains(pt) for p in ps):return name
 return None
report={};out={}
for name,ps in zones.items():
 H=spec[name]['height'];walls=[]
 for poly in ps:
  cs=list(poly.exterior.coords)[:-1]
  for p,q in zip(cs,cs[1:]+cs[:1]):
   L=math.dist(p,q)
   if L<.05:continue
   ux,uy=(q[0]-p[0])/L,(q[1]-p[1])/L;nx,ny=uy,-ux
   n=max(1,int(L/.25));runs=[]
   for k in range(n):
    t=(k+.5)/n;pt=Point(p[0]+ux*L*t+nx*.3,p[1]+uy*L*t+ny*.3);nb=zone_at(pt)
    if runs and runs[-1][0]==nb:runs[-1][2]=(k+1)/n
    else:runs.append([nb,k/n,(k+1)/n])
   for nb,t0,t1 in runs:
    z0=0.0 if nb is None else spec[nb]['height']
    if z0>=H-.05:continue
    a=(round(p[0]+ux*L*t0,3),round(p[1]+uy*L*t0,3));b=(round(p[0]+ux*L*t1,3),round(p[1]+uy*L*t1,3))
    if math.dist(a,b)<.2:continue
    walls.append({'p':list(a),'q':list(b),'z0':z0,'z1':H,'kind':'outer' if nb is None else 'upper','neighbour':nb,'outside_osm':not footprint.buffer(.05).contains(Point((a[0]+b[0])/2-nx*.2,(a[1]+b[1])/2-ny*.2))})
 out[name]=dict(spec[name],polygons=[coords(p) for p in ps],walls=walls)
 report[name]={'area_m2':round(sum(p.area for p in ps),1),'polygons':len(ps),'walls':len(walls),'outer_m':round(sum(math.dist(w['p'],w['q']) for w in walls if w['kind']=='outer'),1)}
covered=unary_union([p for ps in zones.values() for p in ps])
data={'source':'OpenStreetMap way 38033725 (Baronens köpcentrum), '+district['source'],'footprint':coords(footprint),'channel':coords(orient(channel)),
 'octagon':{'centre':[cx,cy],'half':[ha,hb],'chamfer':ch,'polygon':[list(p) for p in octagon]},
 'strips':{
  'brick':{'eave_outer':[list(P33),list(P34),list(J1)],'eave_inner':[list(P32),list(P31),list(J2)]},
  'hotel':{'eave_outer':[list(J1),list(P0),list(P1)],'eave_inner':[list(J2),list(P30),list(P1i)]},
  'inner':{'eave_outer':[list(P24),list(add(P24,d,44.0))],'eave_inner':[list(P24w),list(add(P24w,d,44.0))]}},
 'points':{k:list(v) for k,v in dict(P0=P0,P1=P1,P2=P2,P3=P3,P4=P4,P5=P5,P6=P6,P7=P7,P8=P8,P9=P9,P10=P10,P11=P11,P12=P12,P13=P13,P14=P14,P15=P15,P20=P20,P21=P21,P22=P22,P23=P23,P24=P24,P25=P25,P31=P31,P32=P32,P33=P33,P34=P34,J1=J1,J2=J2,P1i=P1i,P11i=P11i,Km=Km,K2=K2,S1=S1,S2=S2,A0=A0,A1=A1,FL=FL,FR=FR).items()},
 'dome':{'centre':[-187.6,-300.4],'radius':4.2},
 'zones':out,
 'checks':{'footprint_m2':round(footprint.area,1),'channel_m2':round(channel.difference(footprint).area,1),'octagon_outside_osm_m2':round(Polygon(octagon).difference(footprint).area,1),'pavilion_outside_osm_m2':round(Polygon(pavilion).difference(footprint).area,1),'zoned_m2':round(covered.area,1),'uncovered_m2':round(site.difference(covered).area,2),'overlap_m2':round(sum(p.area for ps in zones.values() for p in ps)-covered.area,2)}}
(R/'source/baronen23.json').write_text(json.dumps(data,indent=1,ensure_ascii=False))
(R/'previews/baronen23-zones.json').write_text(json.dumps({'status':'passed' if data['checks']['uncovered_m2']<2 and data['checks']['overlap_m2']<1 else 'review_required','zones':report,'checks':data['checks']},indent=2,ensure_ascii=False))
print(json.dumps(report,indent=1,ensure_ascii=False));print(data['checks']);print('BARONEN23_ZONES_OK')
