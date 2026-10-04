"""Pass 140: the last mainland street houses, the ones no street pass claimed. They stand mostly in the far
west, in the villa and town-house quarters on Ringgatan, Torsgatan, Baldersvägen, Lillegårdsgatan and
Margaretaplan, and one apartment block on Stensövägen at the model's north edge. Pass 98 built them as
plain volumes in its chunk meshes W and M (source/block98.json, OSM, ODbL). The housing: on Ringgatan
the row of three rendered two-storey blocks over basements (white with the gable balcony, pale yellow,
ochre with the red dormers) and, across the street, the brick villa, the tall pale yellow house with the
gable on the street and the yellow hipped villa; on Lillegårdsgatan the white villa with the low hipped
roof and the glazed veranda and the yellow hipped apartment villa with balconies; on Torsgatan the white
boarded villa with the veranda, the yellow-brown brick house with the steep gable, the tall white house
with the dark mansard roof, the villa behind the trees and, at Margaretaplan, the yellow block with the
shop; on Margaretaplan the yellow block with the glazed corner bay; on Baldersvägen the pale grey boarded
villa with the steep gable, the house behind the privacy blur and the white garage; on Stensövägen the
yellow brick block with the balconies (clipped by pass 98's model box).
Selection: every pass-98 outline within 25 m of any named street (the OSM street lines in
references/osm-slott98.json) that no source/blockN.json with N < 140 claims (ids and demolished ids) and
that is not the Stagnell chapel (pass 107). Pass 138 left four of them to other streets and 93326725 as
clipped; pass 136 left two on Ringgatan. Every other unclaimed pass-98 outline lies 25 m or more from
every named street; they are listed in 'left_to_yards' for the yard job.
Clipped outline: 93326725 is cut by pass 98's model box at y 320 into two pieces (245.6 and 17.2 m²);
its street front on Stensövägen lies north of the box. It is built on both pieces in one mesh (as pass
139 built the corner-clipped 93326740), with plain walls on the box edge ('cut') and a flat roof: its
real low saddle runs on out of the box, and a pitched roof on the clipped pieces would close against the
box edge (a hipped roof tried in the first sandbox run read as a pyramid in sv2_h172).
Each outline is split into rectangular zones for its roofs with pass 116's slab method (as copied by
passes 134-139); RIDGE turns the main zone's ridge where the photos show the gable on another side.
Heights in metres above the ground (pass 98 lays the ground at model z 0.30). Measured values are read on
the OSM wall planes (SCR captures '140|'); the rest is estimated from storeys, doors and windows. See
references/block140-notes.md.
"""
from pathlib import Path
import json,math,os,sys,re
if os.environ.get('KALMAR_GEO'):sys.path.insert(0,os.environ['KALMAR_GEO'])
from shapely.geometry import Polygon,Point,LineString
from shapely.geometry.polygon import orient
from shapely.ops import unary_union
R=Path(__file__).resolve().parents[1]
B98=json.loads((R/'source/block98.json').read_text())['buildings']
# an outline clipped by pass 98's model box can come in several pieces with the same id
PIECES={}
for b in B98:PIECES.setdefault(b['id'],[]).append(b)
BY={i:v[0] for i,v in PIECES.items()}
OSM=json.loads((R/'references/osm-slott98.json').read_text())
EARLIER={'500979084'}  # pass 107
for f in sorted((R/'source').glob('block*.json')):
 m_=re.fullmatch(r'block(\d+)\.json',f.name)
 if not m_ or int(m_.group(1))>=140:continue
 d_=json.loads(f.read_text())
 if isinstance(d_,dict):EARLIER|=set(map(str,d_.get('ids',[])))|set(map(str,d_.get('demolished',[])))

# ---------------------------------------------------------------- selection
ST={}
for w in OSM.values():
 t=w.get('tags',{})
 if 'highway' in t and t.get('name') and len(w.get('points',[]))>1:ST.setdefault(t['name'],[]).append(LineString(w['points']))
SL={k:unary_union(v) for k,v in ST.items()}
def chunk_of(b):
 cx_=sum(v[0] for v in b['outer'])/len(b['outer']);return 'W' if cx_<-1150 else ('M' if cx_<-850 else 'E')
OUTALL={i:unary_union([Polygon(b['outer']).buffer(0) for b in v]) for i,v in PIECES.items()}
# Three outlines a little beyond 25 m stand free and are seen from their street in this pass's photos, so
# they are street houses, not yard buildings: Saga behind the garden gate on Södra vägen (26.4 m, sa1_h1,
# sa2_h22), the brick block on Lilla Dammgatan (25.6 m, ld2_h353) and the white villa on the hill above
# Söderportsgatan (42.4 m, sp1_h312, sp2_h301). Pass 139's console had named these streets.
STREET_EXTRA=('93252863','93291989','93329952')
IDS=[];NEAREST={};YARDS={}
for i in PIECES:
 if i in EARLIER:continue
 g=OUTALL[i];ds=sorted((g.distance(SL[n]),n) for n in SL)
 if ds[0][0]<25 or i in STREET_EXTRA:IDS.append(i);NEAREST[i]=[ds[0][1],round(ds[0][0],1)]
 else:YARDS[i]=dict(nearest_street=ds[0][1],distance_m=round(ds[0][0],1),chunk=sorted({chunk_of(b) for b in PIECES[i]}),kind=BY[i]['kind'],area_m2=round(g.area,1))
CLIPPED={i:len(PIECES[i]) for i in IDS if len(PIECES[i])>1}
MINE=tuple(sorted({v[0] for v in NEAREST.values()}))

# ---------------------------------------------------------------- the houses
# wall: wall colour key; boards: vertical boarding; st: storeys; height/top: eaves and ridge above the
# ground; f0: the ground floor's height above the ground (a raised floor over a basement); roof: saddle,
# hip, low, gambrel or flat; ridge: 'street' (ridge parallel to the street wall) or 'across' (the gable
# on the street); door_street: the street the door faces where it is not the nearest one; rm: roof
# material; fr: window frame colour; seen: the photo the values are read from (None = not seen;
# estimated); measured: what was measured; extras: features drawn in the build; nd: the number of
# dormers on the street slope where it differs from the rule; balcony_near/balcony_z: the gable end (the
# one nearest the point) and the height of a gable balcony; bay_near: the corner of the glazed bay.
V1=dict(boards=True,st=1.5,f0=.6,roof='saddle',rm='Tile',fr='Frame')        # a boarded villa of one and a half storeys
VR=dict(boards=False,st=1.5,f0=.6,roof='saddle',rm='Tile',fr='Frame')       # a rendered villa of one and a half storeys
RW=dict(boards=False,st=2,f0=1.0,height=6.8,top=9.4,roof='saddle',rm='Tile',fr='Frame')   # the Ringgatan row over basements
H={
 # ---- Ringgatan, the north-west side: the row of three blocks over basements (south-west to north-east)
 '93566356':dict(RW,name='white rendered two-storey block over a basement with a red tile roof, the attic and the balcony on the south-west gable',wall='WhiteRender',
  seen='rg1_h296 (close), rg2_h22',measured='as 93566385 (the eaves run on in rg1_h296)',extras=['end_balcony','chimney'],balcony_near=[-1636.0,265.05],balcony_z=6.75),
 '93566367':dict(RW,name='pale yellow rendered two-storey block over a basement with a red tile roof',wall='PaleYellowRender',
  seen='rg1_h296 (right), rg2_h22, rg3_h239 (far)',measured='as 93566385',extras=['chimney']),
 '93566385':dict(RW,name='ochre rendered two-storey block over a basement with a red tile roof and two red wall dormers',wall='OchreYellow',
  seen='rg3_h239 (close), rg2_h22',measured='base at z 0.46 and the eaves 7.1 at the east corner on the south-east front (rg3_h239, pano position, camera 2.5 assumed), so 6.6 above the base; 6.8 used with the street sloping',
  extras=['dormers_wall','chimney'],nd=2,dormer_mat='DormerRed'),
 # ---- Ringgatan, the south-east side (south-west to north-east)
 '93505709':dict(VR,name='red brick one-and-a-half-storey villa with a red tile roof and the balcony in the west gable',wall='RedBrick',height=4.0,top=8.2,
  seen='rg6_h82',extras=['chimney','gable_balcony'],door_street='Ringgatan'),
 '93505730':dict(VR,name='pale yellow rendered two-and-a-half-storey house with white corner boards, the gable on Ringgatan and a dark roof',wall='PaleYellowRender',st=2,f0=.5,height=7.8,top=11.0,rm='RoofDark',ridge='across',
  seen='rg5_h103 (resected), rg2_h22 (right)',measured='camera resected on the gable\'s two corners (vertices 0 and 1) to (-1628.37, 256.59); the base reads 0.59 behind the hedge, the eaves 8.74 at the west corner and the gable apex 11.48 in the middle of the gable (camera 2.5 assumed); eaves 7.8 and the ridge 11.0 above the ground',extras=['corners','chimney']),
 '93505770':dict(VR,name='pale yellow rendered two-storey villa with a red tile hipped roof and a red chimney behind the shrubs',wall='PaleYellowRender',st=2,f0=.5,height=5.8,top=9.0,roof='hip',
  seen='rg4_h108 (behind the shrubs), rg6_h82 (far left)',extras=['chimney']),
 # ---- Lillegårdsgatan (north side)
 '93505686':dict(VR,name='white rendered two-storey villa with a low red tile hipped roof, the glazed veranda and balconies (only its east part lies inside the model box)',wall='WhiteRender',st=2,f0=.4,height=6.0,top=7.8,roof='hip',
  seen='lg1_h341, lg3_h67 (west front, outside the box)',extras=['chimney']),
 '93505704':dict(VR,name='yellow rendered two-storey apartment villa over a basement with a red tile hipped roof and the corner balconies',wall='Yellow',st=2,f0=.8,height=6.6,top=9.6,roof='hip',
  seen='lg2_h7, lg1_h341 (right)',extras=['entrance_balcony','chimney']),
 # ---- Torsgatan (north-west side, south-west to north-east), then the corner at Margaretaplan
 '93487572':dict(V1,name='white boarded one-and-a-half-storey villa with a red tile roof, the white wall dormer, two chimneys and the glazed veranda',wall='White',height=4.0,top=8.0,ridge='street',
  seen='ts1_h263 (close), ts7_h345',extras=['dormers_wall','chimneys2'],nd=1,dormer_mat='White'),
 '93487589':dict(VR,name='light rendered one-and-a-half-storey villa with a dark tile roof behind the trees',wall='PaleCream',height=4.0,top=7.8,rm='TileDark',
  seen='ts2_h310 (behind the trees)',extras=['chimney']),
 '93487584':dict(VR,name='yellow-brown brick two-storey house with the steep red tile roof and the gable on Torsgatan',wall='YellowBrick',st=2,f0=.8,height=5.0,top=11.0,
  seen='ts3_h309 (resected), ts4_h294',measured='camera resected on the street gable\'s two corners (vertices 1 and 0) to (-1564.83, 97.28); the base reads 0.52, the eaves 4.6 at the east corner and the apex 11.47 (camera 2.5 assumed); the west eave reads 8.3 where the roof runs on over the bay; eaves 5.0 and ridge 11.0 above the ground',ridge='across',extras=['chimney']),
 '93487582':dict(VR,name='tall white rendered two-and-a-half-storey house with the dark sheet mansard roof and a dormer',wall='WhiteRender',st=2,f0=.4,height=5.8,top=9.8,roof='gambrel',rm='RoofDark',
  seen='ts4_h294 (behind the brick house)',extras=['dormers','chimney'],nd=1),
 '93487556':dict(name='yellow rendered two-storey block with an attic, a red tile roof, the balcony and the shop on the ground floor at Margaretaplan',wall='Yellow',boards=False,st=2,f0=.3,height=8.4,top=12.6,roof='saddle',rm='Tile',fr='Frame',
  seen='ts6_h255 (resected), ts5_h344',measured='camera resected on the Torsgatan gable\'s two corners (vertices 5 and 0) to (-1504.81, 121.66); the base reads 0.23, the eaves 8.96-8.98 at both corners and the gable apex 13.07 (camera 2.5 assumed); with the Google camera the eaves read 7.9; eaves 8.4 and ridge 12.6 used',
  door_street='Margaretaplan',extras=['dormers','chimney','end_balcony','shop'],nd=2,balcony_near=[-1531.1,116.7],balcony_z=3.6),
 # ---- Margaretaplan
 '93358537':dict(name='yellow rendered two-storey block with a red tile hipped roof, dormers, a red chimney and the white glazed corner bay',wall='Yellow',boards=False,st=2,f0=.5,height=7.8,top=11.0,roof='hip',rm='Tile',fr='Frame',
  seen='mp1_h100 (resected)',measured='camera resected on the front\'s corners (vertices 2 and 3, the second under the bay, less certain) to (-1504.46, 151.09); the base reads 0.07 and the eaves 7.83 at the west corner (camera 2.5 assumed); eaves 7.8 above the ground',
  extras=['dormers','chimney','corner_bay'],nd=1,bay_near=[-1484.86,137.29]),
 # ---- Baldersvägen
 '93487591':dict(V1,name='pale grey boarded one-and-a-half-storey villa with the steep red tile roof, the gable on Baldersvägen and a side dormer',wall='PaleGrey',height=4.6,top=9.4,
  seen='bv1_h44 (resected)',measured='camera resected on the street gable\'s two corners (vertices 0 and 3) to (-1634.19, 41.98); the eaves read 5.2 and 4.3 at the two corners and the apex 9.7 (camera 2.5 assumed, the base behind the bushes); 4.6 and 9.4 used',ridge='across',extras=['chimney']),
 '93487569':dict(VR,name='house south of Baldersvägen hidden by Google\'s privacy blur (form estimated)',wall='WhiteRender',height=4.0,top=7.8,seen='bv2_h184 (blurred)',extras=['chimney']),
 '93487574':dict(boards=True,st=1,height=2.5,top=3.8,roof='saddle',rm='TileDark',fr='Frame',name='white boarded garage with a gable roof (clipped by the model box at its west end)',wall='White',
  seen='bv3_h147 (behind)',extras=['garage_door']),
 # ---- the three free-standing houses a little beyond 25 m (STREET_EXTRA)
 '93252863':dict(name='beige rendered two-storey house with a red tile roof and its low west wing at the end of the garden behind the gate on Södra vägen (Saga; clipped by the model box at its north side)',wall='Cream',boards=False,st=2,f0=.4,height=5.6,top=8.8,roof='saddle',rm='Tile',fr='Frame',
  seen='sa1_h1 (through the gate), sa2_h22 (the low west part)',door_street='Södra vägen',extras=['chimney']),
 '93291989':dict(name='yellow brick three-storey block with balconies and a red tile roof behind the trees on Lilla Dammgatan',wall='YellowBrick',boards=False,st=3,f0=.8,height=9.6,top=11.6,roof='saddle',rm='Tile',fr='Frame',
  seen='ld2_h353 (between the trees, June 2011), ld1_h10',extras=['balconies','chimneys2']),
 '93329952':dict(name='white rendered two-and-a-half-storey villa with the corner pavilions and a low dark hipped roof on the hill above Söderportsgatan',wall='WhiteRender',boards=False,st=2,f0=1.0,height=7.4,top=10.0,roof='hip',rm='RoofDark',fr='Frame',
  seen='sp2_h301, sp1_h312 (from the street below the hill)',extras=['corners','chimneys2']),
 # ---- Stensövägen at the north edge of the model
 '93326725':dict(name='yellow brick three-storey apartment block over a basement with balconies and a low roof (only its rear part lies inside the model box)',wall='YellowBrick',boards=False,st=3,f0=1.0,height=10.4,top=10.65,roof='flat',rm='RoofDark',fr='Frame',
  seen='sv2_h172',extras=['no_door']),
}
for v in H.values():v.setdefault('extras',[])
# No outline is a cleared site in the photos; every house stands. 93487569 is hidden by the blur.
DEMOLISHED=set()
IDS=[i for i in IDS if i not in DEMOLISHED]
assert set(H)==set(IDS),(sorted(set(IDS)-set(H)),sorted(set(H)-set(IDS)))
def flat(g):
 g=g.buffer(0);return [g] if g.geom_type=='Polygon' else [q for c in getattr(g,'geoms',[]) for q in flat(c)]
def parts(g):return [orient(r) for q in flat(g) for r in flat(q.buffer(-.02,join_style=2).buffer(.02,join_style=2).simplify(.02)) if r.area>.5]
def frame_of(poly):
 cs=list(poly.exterior.coords)[:-1];a,b=max(zip(cs,cs[1:]+cs[:1]),key=lambda pq:math.dist(*pq))
 L=math.dist(a,b);d=((b[0]-a[0])/L,(b[1]-a[1])/L);return a,d,(-d[1],d[0])
def decompose(poly):
 # pass 116's slab decomposition in the frame of the longest edge: rectangles (s0,s1,t0,t1)
 o,d,n=frame_of(poly);cs=list(poly.simplify(.15).exterior.coords)[:-1]
 st=[((v[0]-o[0])*d[0]+(v[1]-o[1])*d[1],(v[0]-o[0])*n[0]+(v[1]-o[1])*n[1]) for v in cs]
 P=lambda s,t:(o[0]+d[0]*s+n[0]*t,o[1]+d[1]*s+n[1]*t)
 S0,S1,T0,T1=min(s for s,t in st),max(s for s,t in st),min(t for s,t in st),max(t for s,t in st)
 if poly.area>.85*(S1-S0)*(T1-T0):
  return [(dict(s0=S0,s1=S1,t0=T0,t1=T1),Polygon([P(S0,T0),P(S1,T0),P(S1,T1),P(S0,T1)]))]
 ss=sorted(s for s,t in st);cuts=[ss[0]]
 for s in ss[1:]:
  if s-cuts[-1]>1.0:cuts.append(s)
 cuts[-1]=ss[-1]
 if len(cuts)<2:cuts=[ss[0],ss[-1]]
 tlo,thi=min(t for s,t in st)-1,max(t for s,t in st)+1;slabs=[]
 for s0,s1 in zip(cuts,cuts[1:]):
  e=min(.15,(s1-s0)/4);piece=poly.intersection(Polygon([P(s0+e,tlo),P(s1-e,tlo),P(s1-e,thi),P(s0+e,thi)]))
  if piece.area<.2:continue
  ts=[(v[0]-o[0])*n[0]+(v[1]-o[1])*n[1] for g in flat(piece) for v in g.exterior.coords]
  slabs.append([s0,s1,min(ts),max(ts)])
 c0,c1=max(sl[2] for sl in slabs),min(sl[3] for sl in slabs);dmax=max(sl[3]-sl[2] for sl in slabs)
 if len(slabs)>1 and c1-c0>=3.0 and c1-c0>=.5*dmax:
  pcs=[]
  for s0,s1,t0,t1 in slabs:
   for a_,b_ in ((t0,c0),(c1,t1)):
    if b_-a_>.6:pcs.append([s0,s1,a_,b_])
  wings=[]
  for pc in pcs:
   if wings and abs(wings[-1][1]-pc[0])<.01 and abs(wings[-1][2]-pc[2])<.6 and abs(wings[-1][3]-pc[3])<.6:wings[-1][1]=pc[1]
   else:wings.append(pc)
  out=[[slabs[0][0],slabs[-1][1],c0,c1]]+[w_ for w_ in wings if w_[1]-w_[0]>=1.2]
  return [(dict(s0=s0,s1=s1,t0=t0,t1=t1),Polygon([P(s0,t0),P(s1,t0),P(s1,t1),P(s0,t1)])) for s0,s1,t0,t1 in out]
 out=[]
 for sl in slabs:
  if out and abs(out[-1][2]-sl[2])<.6 and abs(out[-1][3]-sl[3])<.6:out[-1][1]=sl[1];out[-1][2]=min(out[-1][2],sl[2]);out[-1][3]=max(out[-1][3],sl[3])
  else:out.append(sl)
 i=0
 while len(out)>1 and i<len(out):
  if out[i][1]-out[i][0]<1.2:
   j=i-1 if i>0 else i+1;out[j]=[min(out[j][0],out[i][0]),max(out[j][1],out[i][1]),min(out[j][2],out[i][2]),max(out[j][3],out[i][3])];out.pop(i);i=0
  else:i+=1
 return [(dict(s0=s0,s1=s1,t0=t0,t1=t1),Polygon([P(s0,t0),P(s1,t0),P(s1,t1),P(s0,t1)])) for s0,s1,t0,t1 in out]


OUT={i:OUTALL[i] for i in IDS}
V=lambda i,k:tuple(BY[i]['outer'][k])
def box_in(poly,a,b):
 # The rectangle that boxes 'poly' in the frame of the direction a->b, first edge along a->b
 # (counter-clockwise), so a roof built on it has its ridge along a->b.
 L=math.dist(a,b);d=((b[0]-a[0])/L,(b[1]-a[1])/L);n=(-d[1],d[0])
 cs=[v for g in flat(poly) for v in g.exterior.coords]
 ss=[(v[0]-a[0])*d[0]+(v[1]-a[1])*d[1] for v in cs];ts=[(v[0]-a[0])*n[0]+(v[1]-a[1])*n[1] for v in cs]
 P=lambda s,t:(a[0]+d[0]*s+n[0]*t,a[1]+d[1]*s+n[1]*t)
 return Polygon([P(min(ss),min(ts)),P(max(ss),min(ts)),P(max(ss),max(ts)),P(min(ss),max(ts))])
def strip(a,b,s0,s1,poly):
 L=math.dist(a,b);d=((b[0]-a[0])/L,(b[1]-a[1])/L);n=(-d[1],d[0])
 cs=[v for g in flat(poly) for v in g.exterior.coords];ts=[(v[0]-a[0])*n[0]+(v[1]-a[1])*n[1] for v in cs]
 P=lambda s,t:(a[0]+d[0]*s+n[0]*t,a[1]+d[1]*s+n[1]*t)
 return Polygon([P(s0,min(ts)-.5),P(s1,min(ts)-.5),P(s1,max(ts)+.5),P(s0,max(ts)+.5)])
# The main zone's ridge, where the photos show the gable on a side the slab method does not give:
# 93487556's gable faces Torsgatan (south-east, the wall from vertex 5 to vertex 0) in ts6_h255, so its ridge
# runs parallel to the Margaretaplan front (vertex 0 to vertex 1).
RIDGE={'93487556':(V('93487556',0),V('93487556',1))}
# 93566385 is an L: the block along Ringgatan (the front from vertex 2 to vertex 3, 24.5 m, 11.5 m deep to
# vertex 0) and a back wing at its north-east end. The slab method cut a flat strip off the street front;
# here the main zone is the band within 11.5 m of the front, boxed with its ridge along the street (one
# roof in rg3_h239), and the rest is decomposed as usual.
MAINBAND={'93566385':(V('93566385',2),V('93566385',3),11.5)}
# Saga's (93252863) south front has ten small jogs of 1-2.5 m (porches and bays); the slab method made a flat
# annex of each. The rectangles are found on the outline simplified by 1.5 m; the walls still follow the
# OSM outline and the jogs join the nearest zone.
COARSE={'93252863':1.5}
def band(a,b,t1,poly):
 L=math.dist(a,b);d=((b[0]-a[0])/L,(b[1]-a[1])/L);n=(-d[1],d[0])
 cs=[v for g in flat(poly) for v in g.exterior.coords];ss=[(v[0]-a[0])*d[0]+(v[1]-a[1])*d[1] for v in cs]
 tt=[(v[0]-a[0])*n[0]+(v[1]-a[1])*n[1] for v in cs];sg=1 if max(tt)>-min(tt) else -1
 P=lambda s,t:(a[0]+d[0]*s+n[0]*t*sg,a[1]+d[1]*s+n[1]*t*sg)
 return Polygon([P(min(ss)-.5,-.5),P(max(ss)+.5,-.5),P(max(ss)+.5,t1),P(min(ss)-.5,t1)])
# pass 98's model box: x >= -1650 and y <= 320; walls on its edges are cut walls (no windows or doors)
def on_box_edge(a,b):return (abs(a[0]+1650)<.05 and abs(b[0]+1650)<.05) or (abs(a[1]-320)<.05 and abs(b[1]-320)<.05)
zones={}
for osm in IDS:
 spec=H[osm]
 # each piece of a clipped outline is decomposed on its own
 if osm in MAINBAND:
  a_,b_,t_=MAINBAND[osm];main=OUT[osm].intersection(band(a_,b_,t_,OUT[osm]))
  rs=[('main',orient(box_in(main,a_,b_)))]
  rs+=sorted([(None,r) for bit in flat(OUT[osm].difference(main)) if bit.area>3 for f,r in decompose(orient(bit))],key=lambda r:-r[1].area)
 else:
  rs=[(None,r) for piece in flat(OUT[osm]) for f,r in decompose(orient(piece.simplify(COARSE.get(osm,0))))]
  rs.sort(key=lambda r:-r[1].area)
 taken=Polygon()
 for k,(fr,rect) in enumerate(rs):
  ps=parts(OUT[osm].intersection(rect).difference(taken))
  if not ps:continue
  taken=unary_union([taken]+ps)
  cs=list(rect.exterior.coords)[:-1]
  if Polygon(cs).exterior.is_ccw is False:cs=cs[::-1]
  ed=[math.dist(cs[i],cs[(i+1)%4]) for i in range(4)];w=min(ed);area=sum(p.area for p in ps)
  if fr=='main':z=dict(height=spec['height'],top=spec['top'],roof=spec['roof'],role='main',ridge_fixed=True)
  elif k==0:
   z=dict(height=spec['height'],top=spec['top'],roof=spec['roof'],role='main')
   if osm in RIDGE:
    # turn the rectangle so that its first edge runs along the given direction
    a_,b_=RIDGE[osm];d_=(b_[0]-a_[0],b_[1]-a_[1])
    def par(i):
     e=(cs[(i+1)%4][0]-cs[i][0],cs[(i+1)%4][1]-cs[i][1]);return abs(e[0]*d_[0]+e[1]*d_[1])/(math.hypot(*e)*math.hypot(*d_))
    j=max(range(4),key=par);cs=cs[j:]+cs[:j];z['ridge_fixed']=True
  elif area<12 or w<2.6:
   # a flat-roofed annex; on blocks of three storeys or more the notches keep the full height
   hh=spec['height'] if spec['st']>=3 else min(spec['height'],3.1)
   z=dict(height=hh,top=hh+.25,roof='flat',role='annex')
  else:
   c0=list(rs[0][1].exterior.coords)[:-1];mw=min(math.dist(c0[i],c0[(i+1)%4]) for i in range(4))
   rf=spec['roof'] if spec['roof'] not in ('mhip','flat') else 'hip'
   if spec['roof']=='flat':z=dict(height=spec['height'],top=spec['top'],roof='flat',role='wing')
   else:z=dict(height=spec['height'],top=spec['height']+(spec['top']-spec['height'])*min(1,w/mw),roof=rf,role='wing')
  zones[f'{osm}_{k}']=(osm,ps,dict(z,rect=[list(v) for v in cs]))
 rem=OUT[osm].difference(taken)
 for bit in flat(rem):
  if bit.area<.01:continue
  mine=[k for k in zones if zones[k][0]==osm]
  k=max(mine,key=lambda k:Polygon(zones[k][2]['rect']).buffer(.3).intersection(bit).area)
  # the remainder joins the nearest zone; its slivers are kept down to 0.05 m²
  o_,ps_,sp_=zones[k];zones[k]=(o_,[orient(r) for q in flat(unary_union(ps_+[bit])) for r in flat(q.simplify(.02)) if r.area>.05],sp_)
others=[(Polygon(b['outer']).buffer(0),max(2.6,min(b['height'] or (b['levels']*3.0+.5),28.0)),b['id']) for b in B98 if b['id'] not in IDS]
def neighbour_at(osm,pt):
 for name,(o,ps,spec) in zones.items():
  if o==osm and any(p.buffer(.001).contains(pt) for p in ps):return name,spec['height']
 for g,h,bid in others:
  if g.buffer(.001).contains(pt):return bid,h-.30
 return None,0.0
# the streets a door may face: the houses' nearest streets and the side streets of the corner houses
DOORST=MINE+tuple(n for n in ('Drottning Margaretas väg','Sturevägen','Rosenstigen','Vegagatan') if n not in MINE)
out={};report={}
for name,(osm,ps,spec) in zones.items():
 Hh=spec['height'];walls=[]
 for poly in ps:
  cs=list(poly.exterior.coords)[:-1]
  for p,q in zip(cs,cs[1:]+cs[:1]):
   Lw=math.dist(p,q)
   if Lw<.05:continue
   wx,wy=(q[0]-p[0])/Lw,(q[1]-p[1])/Lw;nx,ny=wy,-wx;n=max(1,int(Lw/.2));runs=[]
   for k in range(n):
    t=(k+.5)/n;nb,h=neighbour_at(osm,Point(p[0]+wx*Lw*t+nx*.3,p[1]+wy*Lw*t+ny*.3))
    if runs and runs[-1][0]==nb:runs[-1][3]=(k+1)/n
    else:runs.append([nb,h,k/n,(k+1)/n])
   for nb,h,t0,t1 in runs:
    z0=0.0 if nb is None else h
    if z0>=Hh-.05:continue
    a=(round(p[0]+wx*Lw*t0,3),round(p[1]+wy*Lw*t0,3));b=(round(p[0]+wx*Lw*t1,3),round(p[1]+wy*Lw*t1,3))
    if math.dist(a,b)<.2:continue
    kind='upper' if nb is not None else ('cut' if on_box_edge(a,b) else 'outer')
    walls.append({'p':list(a),'q':list(b),'z0':z0,'z1':Hh,'kind':kind,'neighbour':nb})
 hs=H[osm]
 # per street: the outer wall nearest it that faces it (outward normal towards it)
 faces={}
 for w in walls:
  if w['kind']!='outer' or math.dist(w['p'],w['q'])<1.5:continue
  mid=Point((w['p'][0]+w['q'][0])/2,(w['p'][1]+w['q'][1])/2);L_=math.dist(w['p'],w['q'])
  nx,ny=(w['q'][1]-w['p'][1])/L_,-(w['q'][0]-w['p'][0])/L_
  for nm in DOORST:
   ln=SL[nm];sp=ln.interpolate(ln.project(mid));dd=mid.distance(sp)
   if dd<.01 or dd>60 or ((sp.x-mid.x)*nx+(sp.y-mid.y)*ny)/dd<.5:continue
   if nm not in faces or dd<faces[nm][0]:faces[nm]=(dd,[w['p'],w['q']])
 best=min(((v[0],k,v[1]) for k,v in faces.items()),default=None)
 # the door street named per house, else the house's nearest street where a wall faces it
 want=hs.get('door_street',NEAREST[osm][0])
 if want in faces:best=(faces[want][0],want,faces[want][1])
 spec=dict(spec,street=best[1] if best else None,street_wall=best[2] if best else None,street_m=round(best[0],1) if best else None,
  street_walls={k:v[1] for k,v in faces.items()})
 out[name]=dict(spec,osm=osm,mesh='SM_Slott140_'+osm,wall=spec.get('wall',hs['wall']),boards=spec.get('boards',hs['boards']),brick=False,
  polygons=[[list(v) for v in list(p.exterior.coords)[:-1]] for p in ps],walls=walls)
 report[name]={'osm':osm,'role':spec['role'],'roof':spec['roof'],'area_m2':round(sum(p.area for p in ps),1),'walls':len(walls),'outer_m':round(sum(math.dist(w['p'],w['q']) for w in walls if w['kind']=='outer'),1),'street':spec['street']}

foot=unary_union(list(OUT.values()));covered=unary_union([p for o,ps,s in zones.values() for p in ps])
houses={i:dict(H[i],nearest_street=NEAREST[i][0],nearest_street_m=NEAREST[i][1],chunks=sorted({chunk_of(b) for b in PIECES[i]})) for i in IDS}
clipped={i:'cut by pass 98\'s model box (x -1650 or y 320) into %d piece(s); built on the clipped outline with plain walls on the box edge'%n for i,n in
 sorted(dict(CLIPPED,**{i:1 for i in IDS if i not in CLIPPED and any(any(abs(v[0]+1650)<.01 or abs(v[1]-320)<.01 for v in b['outer']) for b in PIECES[i])}).items())}
data={'demolished':sorted(DEMOLISHED),'source':'pass 98 outlines (source/block98.json, from references/osm-slott98.json, OpenStreetMap, ODbL)','ground_z':0.30,'ids':IDS,
 'nearest_streets':NEAREST,'clipped':clipped,'left_to_yards':dict(sorted(YARDS.items())),'houses':houses,'zones':out,
 'checks':{'buildings':len(IDS),'footprint_m2':round(foot.area,1),'zoned_m2':round(covered.area,1),'outside_osm_m2':round(covered.difference(foot).area,2),'osm_not_zoned_m2':round(foot.difference(covered).area,2),
  'overlap_m2':round(sum(p.area for o,ps,s in zones.values() for p in ps)-covered.area,3),
  'outlines_overlapping_m2':round(sum(OUT[a].intersection(OUT[b]).area for i,a in enumerate(IDS) for b in IDS[i+1:]),3),
  'zones_per_building':{i:sum(1 for o,ps,s in zones.values() if o==i and ps) for i in IDS},
  'left_to_yards':len(YARDS),'cut_walls':sum(1 for z in out.values() for w in z['walls'] if w['kind']=='cut')}}
(R/'source/block140.json').write_text(json.dumps(data,indent=1,ensure_ascii=False))
# pass 134's limits (outside OSM < 0.3 m², not zoned < 0.5 m², overlap within the outlines' own overlap + 0.2 m²)
c=data['checks'];ok=c['outside_osm_m2']<.3 and c['osm_not_zoned_m2']<.5 and c['overlap_m2']<.2+c['outlines_overlapping_m2'] and all(c['zones_per_building'].values())
(R/'previews/block140-zones.json').write_text(json.dumps({'status':'passed' if ok else 'review_required','zones':report,'checks':c},indent=2,ensure_ascii=False))
for k,v in report.items():print(k,v)
print(c);print('BLOCK140_ZONES_OK' if ok else 'BLOCK140_ZONES_REVIEW')
