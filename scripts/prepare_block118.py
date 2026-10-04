"""Pass 118: the third Gamla stan pass on the mainland west of Kvarnholmen. Kungsgatan, Söderportsgatan,
Klostergatan and Skansgatan: 18th-19th-century boarded wooden houses (red, yellow, white, grey) under
tile roofs, the 18th-century pink rough-rendered stone house with quoins on Söderportsgatan, the
turn-of-the-century villas (the white villa with the corner tower, the pale yellow villa with the curved
Jugend gable and mansard roof, the pale yellow boarded gambrel villa with the glazed porch, the red
boarded villa with the hipped roof), the 1940s rendered apartment rows and blocks and the yellow-brick
1950s house further north on Kungsgatan. Pass 98 built them as plain volumes inside its chunk meshes
(source/block98.json, OSM, ODbL); this pass selects the outlines that lie within 25 m of one of the four
streets (the OSM street lines in references/osm-slott98.json), leaving out the houses of passes 107,
115 and 116 and every house of pass 117 (within 25 m of Västerlånggatan with the centroid at
x <= -930, or within 25 m of Gamla Kungsgatan or Paters gränd), and splits each into rectangular
zones for its roofs (the slab method of pass 116):
- each outline is framed on its longest edge and cut into slabs at its vertices; slabs with the same
  depth are merged, so an L or T outline becomes two or three rectangles;
- the largest rectangle is the main body (eaves, ridge and roof from the spec below); the others are
  wings with the same eaves (a lower ridge from their width) or, when small or narrow, one-storey
  annexes;
- two houses have explicit rectangles read on their photos: the derelict house at the corner of
  Söderportsgatan and Klostergatan (93293023: a two-storey cross part on the street bump, gambrel
  wings on both sides) and the gambrel villa (93293026: a cross gambrel over its west part, the
  east part under a gambrel along the house).
Heights in metres above the ground (pass 98 lays the ground at model z 0.30). Measured values are from
Google Street View panoramas resected on the OSM outlines; the rest is estimated from storeys, doors
and windows. See references/block118-notes.md.
"""
from pathlib import Path
import json,math,os,sys
if os.environ.get('KALMAR_GEO'):sys.path.insert(0,os.environ['KALMAR_GEO'])
from shapely.geometry import Polygon,Point,LineString
from shapely.geometry.polygon import orient
from shapely.ops import unary_union
R=Path(__file__).resolve().parents[1]
B98=json.loads((R/'source/block98.json').read_text())['buildings'];BY={b['id']:b for b in B98}
OSM=json.loads((R/'references/osm-slott98.json').read_text())
P107={'500979084'}
P115=set(json.loads((R/'source/block115.json').read_text())['ids'])
P116=set(json.loads((R/'source/block116.json').read_text())['ids'])

# ---------------------------------------------------------------- selection
MINE=('Kungsgatan','Söderportsgatan','Klostergatan','Skansgatan')
ST={}
for w in OSM.values():
 t=w.get('tags',{})
 if 'highway' in t and t.get('name') and len(w.get('points',[]))>1:ST.setdefault(t['name'],[]).append(LineString(w['points']))
SL={k:unary_union(v) for k,v in ST.items()}
VLG,GKG,PAT=SL['Västerlånggatan'],SL['Gamla Kungsgatan'],SL['Paters gränd']
def p117(g):
 # pass 117's rule: within 25 m of Västerlånggatan with the centroid at x <= -930, or within 25 m of
 # Gamla Kungsgatan or Paters gränd (corner houses on those streets are left to pass 117)
 return (g.distance(VLG)<25 and g.centroid.x<=-930) or g.distance(GKG)<25 or g.distance(PAT)<25
IDS=[]
for b in B98:
 if b['id'] in P107|P115|P116:continue
 g=Polygon(b['outer']).buffer(0)
 if any(g.distance(SL[n])<25 for n in MINE) and not p117(g):IDS.append(b['id'])

# ---------------------------------------------------------------- the houses
# wall: wall colour key; boards: vertical boarding; brick: brick coursing; st: storeys (1, 1.5, 2, 3);
# height/top: eaves and ridge above the ground; f0: the ground floor's height above the ground (a
# raised floor over a basement); roof: saddle, hip, gambrel, mhip (hipped mansard), low (shallow hip
# on any outline) or flat; ridge: 'long' (along the main rectangle's long side) or 'short'; rm: roof
# material; fr: window frame colour; seen: the photo the values are read from (None = not seen;
# estimated); measured: what was measured. extras: per-house features drawn in the build.
H={
 # Söderportsgatan, south side (east to west), and the corner with Klostergatan
 '93293023':dict(name='derelict white-grey boarded house at the corner of Söderportsgatan and Klostergatan: two-storey cross part with a low gable on both streets, gambrel wings on both sides, boarded-up windows, green door with a carved surround',
  wall='WhiteGrey',boards=True,st=2,height=5.4,top=7.1,roof='saddle',rm='Tile',fr='Frame',seen='sp01_h145, kg01_h213, kl01_h304',
  measured='cross part wall top 5.1-6.3 (drawn 5.4) and gable apex 6.9; wing eaves 3.2, gambrel break 5.4, top 6.7; upper windows 3.6-5.1 (resected, camera 1.97)',
  rest=dict(height=3.2,top=6.7,roof='gambrel',st=1),extras=['boarded_up','door_green']),
 '93293034':dict(name='yellow boarded cottage with a red tile roof',wall='Yellow',boards=True,st=1.5,height=3.6,top=6.6,roof='saddle',rm='Tile',fr='Frame',seen='sp01_h145, kl01_h304',extras=['chimney']),
 '93293020':dict(name='row of garages',wall='Brown',boards=True,st=1,height=2.5,top=2.9,roof='saddle',rm='RoofDark',fr='Frame',seen='sp01_h145 (far), kl03_h304 (far)',extras=['garages','no_door']),
 '93293021':dict(name='red-brick villa with a hipped tile roof',wall='Brick',boards=False,brick=True,st=2,height=6.0,top=9.6,roof='hip',rm='Tile',fr='Frame',seen='kg01_h213 (60 m), kl03_h304 (46 m)',extras=['chimney']),
 '93293038':dict(name='18th-century pink rough-rendered stone house with light quoins, a stone door surround, a hipped tile roof with two dormers',
  wall='PinkRender',boards=False,st=2,height=6.2,top=11.0,roof='hip',rm='Tile',fr='Frame',seen='sp03_h151, sp04_h142',
  measured='eaves 6.1-6.3, ridge 11.5 (read on the ridge line), door 0-3.0, windows 1.17-2.89 and 4.06-5.57 (resected, camera 2.1)',
  rows=[(1.15,1.7,1.0),(4.05,1.5,1.0)],door_h=2.9,extras=['quoins','door_stone','dormers2','chimney']),
 '93293013':dict(name='small red boarded outbuilding with a hipped tile roof',wall='Red',boards=True,st=1,height=2.6,top=4.6,roof='hip',rm='Tile',fr='Frame',seen='kl03_h304'),
 '93293026':dict(name='pale yellow boarded villa on a raised grey plinth with a cross gambrel gable and the glazed porch',
  wall='PaleYellow',boards=True,st=2,height=5.6,top=10.8,roof='gambrel',rm='TileBrown',fr='Frame',f0=1.8,seen='sp04_h142, kl03_h304 (far)',
  measured='plinth 1.8, eaves 5.8, gambrel break 9.3, apex 11.6, ground-floor windows 3.1-4.9, gable windows 6.5-8.3, porch top 5.7 (Google camera, height 2.84 from the base)',
  rest=dict(height=5.6,top=9.6,roof='gambrel'),extras=['porch_glazed','chimney']),
 '93293015':dict(name='garage',wall='Grey',boards=True,st=1,height=2.5,top=3.1,roof='saddle',rm='RoofDark',fr='Frame',seen=None,extras=['garages','no_door']),
 '93293011':dict(name='shed',wall='Red',boards=True,st=1,height=2.4,top=3.6,roof='saddle',rm='Tile',fr='Frame',seen=None),
 '93293029':dict(name='red boarded one-and-a-half-storey house with dormers and white trim at the corner of Skansgatan',wall='Red',boards=True,st=1.5,height=4.0,top=8.0,roof='saddle',rm='Tile',fr='Frame',seen='sp06_h131, sp05_h316 (edge)',extras=['dormers','chimney']),
 # Söderportsgatan, north side (east to west)
 '93292701':dict(name='small pale yellow boarded house behind the fence',wall='PaleYellow',boards=True,st=1,height=3.0,top=5.2,roof='saddle',rm='Tile',fr='Frame',seen='kg02_h213 (hedge), sp01_h325 (far)'),
 '93292672':dict(name='pale yellow rendered villa with a hipped mansard roof in red-brown tile, dormers and the white curved Jugend gable towards Söderportsgatan',
  wall='PaleYellowRender',boards=False,st=2,height=5.2,top=10.6,roof='mhip',rm='TileBrown',fr='Frame',seen='kg02_h213, kg03_h213, sp01_h325',
  measured='mansard foot 5.0-5.3, break about 9.2, ridge seen at 9.6-9.9 on the wall plane (Google camera, height 2.2-2.5 assumed)',extras=['jugend','dormers','chimneys2']),
 '93292679':dict(name='white rendered villa with the corner tower (pyramid roof), the cross gable and the balcony, red tile hipped roof',
  wall='White',boards=False,st=2,height=6.6,top=9.8,roof='hip',rm='Tile',fr='Frame',seen='sp03_h331, sp04_h322 (edge)',
  measured='tower eaves 8.2, tower apex 10.5, cross-gable eaves 4.6 and apex 8.3, middle eaves 6.8, balcony 4.6 (resected; the base is behind the hedge, so the readings are taken up by 1.2 m to a 2.3 m camera)',
  extras=['tower','gable_left','balcony','chimney']),
 '93292667':dict(name='red boarded two-storey villa with white trim, a hipped tile roof, a dormer and two chimneys',wall='Red',boards=True,st=2,height=5.5,top=9.6,roof='hip',rm='Tile',fr='Frame',seen='sp04_h322, sp03_h331, sp05_h316',
  measured='eaves 5.2-5.9 (camera height 2.2-2.6 assumed; the base is behind the hedge), ridge about 9.6 (carried back to the ridge line)',extras=['dormer1','chimneys2']),
 # Klostergatan and Skansgatan (south-west end; far or no views)
 '93293019':dict(name='white boarded one-and-a-half-storey house',wall='White',boards=True,st=1.5,height=3.8,top=7.0,roof='saddle',rm='Tile',fr='Frame',seen='kl03_h304 (far, trees)'),
 '93293018':dict(name='pale yellow boarded two-storey house',wall='PaleYellow',boards=True,st=2,height=5.4,top=8.4,roof='saddle',rm='Tile',fr='Frame',seen='kl03_h304 (far)'),
 '93293042':dict(name='yard shed',wall='Red',boards=True,st=1,height=2.4,top=3.8,roof='saddle',rm='Tile',fr='Frame',seen=None),
 '93293035':dict(name='red boarded one-and-a-half-storey house',wall='Red',boards=True,st=1.5,height=3.8,top=6.8,roof='saddle',rm='Tile',fr='Frame',seen=None),
 '93293040':dict(name='yellow boarded one-and-a-half-storey house',wall='Yellow',boards=True,st=1.5,height=3.8,top=6.8,roof='saddle',rm='Tile',fr='Frame',seen=None),
 '93293027':dict(name='small grey boarded cottage',wall='Grey',boards=True,st=1,height=2.8,top=4.8,roof='saddle',rm='Tile',fr='Frame',seen=None),
 # Kungsgatan north of Västerlånggatan, west side
 '93238265':dict(name='garden shed behind the red board fence',wall='Red',boards=True,st=1,height=2.3,top=3.4,roof='saddle',rm='Tile',fr='Frame',seen='kg06_h212 (hidden by the fence)',extras=['no_door']),
 '93238237':dict(name='Kungsgatan 13A: pale green rendered section of the 1940s apartment row, entrance with the balcony above',wall='PaleGreen',boards=False,st=2,height=7.0,top=8.6,roof='low',rm='Tile',fr='Frame',f0=1.2,seen='kg07_h212',
  measured='eaves 6.1 on the facade plane with a camera height of 1.39 from the base, taken up to a 2.3 m camera: about 7.0; door 0.4-2.6; basement windows to 1.2 (resected)',extras=['entrance_balcony']),
 '93238276':dict(name='yellow rendered section of the 1940s row with the white curved window hoods',wall='YellowRender',boards=False,st=2,height=8.0,top=9.6,roof='low',rm='Tile',fr='Frame',f0=1.2,seen='kg07_h212',
  measured='cornice 8.0 on the facade plane (camera 1.39 from the base): about 1.5 m above the green sections in the photo',extras=['hoods']),
 '93238230':dict(name='pale green rendered section of the 1940s row',wall='PaleGreen',boards=False,st=2,height=7.0,top=8.6,roof='low',rm='Tile',fr='Frame',f0=1.2,seen='kg07_h212 (far)'),
 '93238258':dict(name='yellow rendered section of the 1940s row',wall='YellowRender',boards=False,st=2,height=8.0,top=9.6,roof='low',rm='Tile',fr='Frame',f0=1.2,seen='kg07_h212 (far), kg08_h200 (far)',extras=['hoods']),
 '93238271':dict(name='white rendered two-storey 1940s block at the corner of Ståthållaregatan, red tile roof and chimneys',wall='WhiteRender',boards=False,st=2,height=6.0,top=9.0,roof='saddle',rm='Tile',fr='Frame',seen='kg08_h200',extras=['chimneys2']),
 '93238289':dict(name='white rendered two-storey 1940s block',wall='WhiteRender',boards=False,st=2,height=6.0,top=9.0,roof='saddle',ridge='short',rm='Tile',fr='Frame',seen='kg08_h200'),
 '93238238':dict(name='white rendered two-storey 1940s block',wall='WhiteRender',boards=False,st=2,height=6.0,top=9.0,roof='saddle',rm='Tile',fr='Frame',seen='kg08_h200 (far)',extras=['chimneys2']),
 '93326721':dict(name='yellow rendered three-storey block with a red tile hipped roof',wall='YellowRender',boards=False,st=3,height=9.3,top=12.4,roof='hip',rm='Tile',fr='Frame',f0=.6,seen='kg08_h200, kg09_h201 (edge)'),
 '93326735':dict(name='yellow-brick 1950s houses (a pair) with red tile roofs, roof lights and the garage',wall='YellowBrick',boards=False,brick=True,st=2,height=5.6,top=8.4,roof='saddle',rm='Tile',fr='Frame',seen='kg09_h201',
  measured='eaves 5.8, ridge seen at 7.3 on the front plane (Google camera, height 2.9 from the base)',extras=['garage_door','skylights']),
 # Kungsgatan north of Västerlånggatan, east side
 '93291960':dict(name='garden outbuilding',wall='Red',boards=True,st=1,height=2.5,top=3.8,roof='saddle',rm='Tile',fr='Frame',seen=None),
 '93291990':dict(name='garden outbuilding',wall='Red',boards=True,st=1,height=2.5,top=3.8,roof='saddle',rm='Tile',fr='Frame',seen=None),
 '93291994':dict(name='garden outbuilding',wall='Grey',boards=True,st=1,height=2.5,top=4.0,roof='saddle',rm='Tile',fr='Frame',seen=None),
 '93291986':dict(name='garden shed',wall='Red',boards=True,st=1,height=2.3,top=3.3,roof='saddle',rm='Tile',fr='Frame',seen=None),
 '93291980':dict(name='garden shed',wall='Grey',boards=True,st=1,height=2.3,top=3.3,roof='saddle',rm='RoofDark',fr='Frame',seen=None),
 '93291997':dict(name='garden shed',wall='Red',boards=True,st=1,height=2.3,top=3.3,roof='saddle',rm='Tile',fr='Frame',seen=None),
 '93291987':dict(name='garden outbuilding',wall='Yellow',boards=True,st=1,height=2.6,top=4.2,roof='saddle',rm='Tile',fr='Frame',seen=None),
 '93291974':dict(name='salmon rendered three-storey 1940s apartment block with balconies',wall='Salmon',boards=False,st=3,height=10.4,top=12.6,roof='hip',rm='Tile',fr='Frame',f0=1.0,seen='kg08_h20',
  measured='storeys read by eye: three rows of windows over a basement',extras=['balconies','chimneys2']),
 '93326709':dict(name='salmon rendered three-storey 1940s apartment block with balconies and attic dormers',wall='Salmon',boards=False,st=3,height=10.4,top=14.0,roof='saddle',rm='TileBrown',fr='Frame',f0=1.0,seen='kg08_h20',
  measured='storeys read by eye: three rows of windows over a basement, dormers in the roof',extras=['balconies','dormers']),
 '93326746':dict(name='salmon rendered three-storey 1940s apartment block (Kungsgatan and Stensögatan corner)',wall='Salmon',boards=False,st=3,height=10.4,top=13.6,roof='saddle',rm='TileBrown',fr='Frame',f0=1.0,seen=None),
}
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

OUT={i:Polygon(BY[i]['outer']).buffer(0) for i in IDS}
V=lambda i,k:tuple(BY[i]['outer'][k])
def box_in(poly,a,b):
 # The rectangle that boxes 'poly' in the frame of the direction a->b, first edge along a->b
 # (counter-clockwise), so a saddle or gambrel built on it has its ridge along a->b.
 L=math.dist(a,b);d=((b[0]-a[0])/L,(b[1]-a[1])/L);n=(-d[1],d[0])
 cs=[v for g in flat(poly) for v in g.exterior.coords]
 ss=[(v[0]-a[0])*d[0]+(v[1]-a[1])*d[1] for v in cs];ts=[(v[0]-a[0])*n[0]+(v[1]-a[1])*n[1] for v in cs]
 P=lambda s,t:(a[0]+d[0]*s+n[0]*t,a[1]+d[1]*s+n[1]*t)
 return Polygon([P(min(ss),min(ts)),P(max(ss),min(ts)),P(max(ss),max(ts)),P(min(ss),max(ts))])
def strip(a,b,s0,s1,poly):
 # The part of the box of 'poly' (frame a->b) between s0 and s1 along a->b.
 L=math.dist(a,b);d=((b[0]-a[0])/L,(b[1]-a[1])/L);n=(-d[1],d[0])
 cs=[v for g in flat(poly) for v in g.exterior.coords];ts=[(v[0]-a[0])*n[0]+(v[1]-a[1])*n[1] for v in cs]
 P=lambda s,t:(a[0]+d[0]*s+n[0]*t,a[1]+d[1]*s+n[1]*t)
 return Polygon([P(s0,min(ts)),P(s1,min(ts)),P(s1,max(ts)),P(s0,max(ts))])
# Explicit rectangles (read on the photos). Each is (rectangle, ridge direction a->b); the first is
# the main body; the rest of the outline gets the spec's 'rest' values with its ridge along 'axis'.
#  93293023, read on sp01_h145: the two-storey cross part stands on the 7.2 m street bump (vertices
#   3-4) and runs through to the back (kl01_h304 shows its gable on Klostergatan too); its ridge runs
#   across the house. The wings on both sides are under gambrels along the house (axis 7->0).
#  93293026, read on sp04_h142: the cross gambrel gable faces the street over the west 7.5 m (s 6.9
#   to 14.4 along the north wall 0->1); its ridge runs north-south. The east part's gambrel runs
#   along the house.
_a,_b=V('93293023',3),V('93293023',4)
_r23=box_in(OUT['93293023'].intersection(strip(_a,_b,0,math.dist(_a,_b),OUT['93293023'])),_a,_b)
_a26,_b26=V('93293026',0),V('93293026',1)
_r26=strip(_a26,_b26,6.9,math.dist(_a26,_b26)+.5,OUT['93293026'])
RECTS={'93293023':dict(main=(_r23,('across',_a,_b)),axis=(V('93293023',7),V('93293023',0))),
 '93293026':dict(main=(_r26,('across',_a26,_b26)),axis=(_a26,_b26))}
zones={}
for osm in IDS:
 spec=H[osm]
 if osm in RECTS:
  rr=RECTS[osm];mr,(how,a_,b_)=rr['main']
  # the main rectangle with its first edge across a->b (so the ridge runs across)
  L_=math.dist(a_,b_);d_=((b_[0]-a_[0])/L_,(b_[1]-a_[1])/L_);n_=(-d_[1],d_[0])
  mrect=box_in(mr,(0,0),n_)
  rs=[('main',orient(mrect))]
  rest=OUT[osm].difference(mrect)
  for bit in flat(rest):
   if bit.area>3:rs.append(('rest',orient(box_in(bit,*rr['axis']))))
 else:
  rs=[(None,r) for f,r in sorted(decompose(OUT[osm]),key=lambda r:-r[1].area)]
 taken=Polygon()
 for k,(fr,rect) in enumerate(rs):
  ps=parts(OUT[osm].intersection(rect).difference(taken))
  if not ps:continue
  taken=unary_union([taken]+ps)
  cs=list(rect.exterior.coords)[:-1]
  if Polygon(cs).exterior.is_ccw is False:cs=cs[::-1]
  ed=[math.dist(cs[i],cs[(i+1)%4]) for i in range(4)];w=min(ed);area=sum(p.area for p in ps)
  if fr=='main':
   # the first edge of the stored rectangle is the ridge direction (fixed)
   z=dict(height=spec['height'],top=spec['top'],roof='saddle' if osm=='93293023' else spec['roof'],role='main',ridge_fixed=True)
  elif fr=='rest':
   z=dict(spec['rest'],role='wing',ridge_fixed=True)
  elif k==0:z=dict(height=spec['height'],top=spec['top'],roof=spec['roof'],role='main')
  elif area<12 or w<2.6:
   # a one-storey flat-roofed annex; on the three-storey blocks the notches of the outline keep the
   # full height (stair towers and bays, not sheds)
   hh=spec['height'] if spec['st']>=3 else min(spec['height'],3.1)
   z=dict(height=hh,top=hh+.25,roof='flat',role='annex')
  else:
   c0=list(rs[0][1].exterior.coords)[:-1];mw=min(math.dist(c0[i],c0[(i+1)%4]) for i in range(4))
   rf=spec['roof'] if spec['roof'] not in ('mhip',) else 'hip'
   z=dict(height=spec['height'],top=spec['height']+(spec['top']-spec['height'])*min(1,w/mw),roof=rf,role='wing')
  zones[f'{osm}_{k}']=(osm,ps,dict(z,rect=[list(v) for v in cs]))
 rem=OUT[osm].difference(taken)
 for bit in flat(rem):
  if bit.area<.01:continue
  mine=[k for k in zones if zones[k][0]==osm]
  k=max(mine,key=lambda k:Polygon(zones[k][2]['rect']).buffer(.3).intersection(bit).area)
  o_,ps_,sp_=zones[k];zones[k]=(o_,parts(unary_union(ps_+[bit])),sp_)
others=[(Polygon(b['outer']).buffer(0),max(2.6,min(b['height'] or (b['levels']*3.0+.5),28.0)),b['id']) for b in B98 if b['id'] not in IDS]
def neighbour_at(osm,pt):
 for name,(o,ps,spec) in zones.items():
  if o==osm and any(p.buffer(.001).contains(pt) for p in ps):return name,spec['height']
 for g,h,bid in others:
  if g.buffer(.001).contains(pt):return bid,h-.30
 return None,0.0
# the streets a door may face: the pass's four, and the side streets of the houses at the north end
DOORST=('Kungsgatan','Söderportsgatan','Klostergatan','Skansgatan','Ståthållaregatan','Stora Dammgatan','Lilla Dammgatan')
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
    walls.append({'p':list(a),'q':list(b),'z0':z0,'z1':Hh,'kind':'outer' if nb is None else 'upper','neighbour':nb})
 hs=H[osm]
 # per street: the outer wall nearest it that faces it (outward normal towards it)
 faces={}
 for w in walls:
  if w['kind']!='outer' or math.dist(w['p'],w['q'])<1.5:continue
  mid=Point((w['p'][0]+w['q'][0])/2,(w['p'][1]+w['q'][1])/2);L_=math.dist(w['p'],w['q'])
  nx,ny=(w['q'][1]-w['p'][1])/L_,-(w['q'][0]-w['p'][0])/L_
  for nm in DOORST:
   ln=SL[nm];sp=ln.interpolate(ln.project(mid));dd=mid.distance(sp)
   if dd<.01 or dd>40 or ((sp.x-mid.x)*nx+(sp.y-mid.y)*ny)/dd<.5:continue
   if nm not in faces or dd<faces[nm][0]:faces[nm]=(dd,[w['p'],w['q']])
 best=min(((v[0],k,v[1]) for k,v in faces.items()),default=None)
 spec=dict(spec,street=best[1] if best else None,street_wall=best[2] if best else None,street_m=round(best[0],1) if best else None,
  street_walls={k:v[1] for k,v in faces.items()})
 out[name]=dict(spec,osm=osm,mesh='SM_Slott118_'+osm,wall=hs['wall'],boards=hs['boards'],brick=hs.get('brick',False),
  polygons=[[list(v) for v in list(p.exterior.coords)[:-1]] for p in ps],walls=walls)
 report[name]={'osm':osm,'role':spec['role'],'roof':spec['roof'],'area_m2':round(sum(p.area for p in ps),1),'walls':len(walls),'outer_m':round(sum(math.dist(w['p'],w['q']) for w in walls if w['kind']=='outer'),1),'street':spec['street']}
foot=unary_union(list(OUT.values()));covered=unary_union([p for o,ps,s in zones.values() for p in ps])
houses={i:{k:v for k,v in H[i].items()} for i in IDS}
data={'source':'pass 98 outlines (source/block98.json, from references/osm-slott98.json, OpenStreetMap, ODbL)','ground_z':0.30,'ids':IDS,'houses':houses,'zones':out,
 'checks':{'buildings':len(IDS),'footprint_m2':round(foot.area,1),'zoned_m2':round(covered.area,1),'outside_osm_m2':round(covered.difference(foot).area,2),'osm_not_zoned_m2':round(foot.difference(covered).area,2),
  'overlap_m2':round(sum(p.area for o,ps,s in zones.values() for p in ps)-covered.area,3),
  'outlines_overlapping_m2':round(sum(OUT[a].intersection(OUT[b]).area for i,a in enumerate(IDS) for b in IDS[i+1:]),3),
  'zones_per_building':{i:sum(1 for o,ps,s in zones.values() if o==i and ps) for i in IDS}}}
(R/'source/block118.json').write_text(json.dumps(data,indent=1,ensure_ascii=False))
c=data['checks'];ok=c['outside_osm_m2']<.2 and c['osm_not_zoned_m2']<.5 and c['overlap_m2']<.2+c['outlines_overlapping_m2'] and all(c['zones_per_building'].values())
(R/'previews/block118-zones.json').write_text(json.dumps({'status':'passed' if ok else 'review_required','zones':report,'checks':c},indent=2,ensure_ascii=False))
for k,v in report.items():print(k,v)
print(c);print('BLOCK118_ZONES_OK' if ok else 'BLOCK118_ZONES_REVIEW')
