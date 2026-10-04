"""Pass 136 (started as a parked street pass 'pass 124' and renumbered): the mainland south-west of
Ståthållaregatan around Drottning Margaretas väg, Sankt Eriks gata, Johan III:s gata and Sankta Britas
gata. Pass 98 built these houses as plain volumes inside its chunk meshes (source/block98.json, OSM,
ODbL). The housing: on Drottning Margaretas väg the two rows of the 1920s-30s, the southern row of rendered
two-and-a-half-storey houses over basements in white, grey, cream and yellow-green with gables,
dormers and a curved gable with a round window, and the northern row of rendered two-storey blocks in red,
cream and white with dormers; the villas west and south of the avenue (boarded and rendered, saddle,
mansard and hipped roofs). On Sankt Eriks gata the pink, orange and white rendered town houses, the
pink 1910s house with the pedimented centre bay, the dark boarded house with the white oriel, the pink
and green villas and the light brick house; on Johan III:s gata the white boarded block with the
boarded roof storey, the white rendered house with the central gable, the 1990s terrace and the low
white houses; on Sankta Britas gata the yellow 18th-century-style house with the mansard roof and the
low houses and sheds behind the fences.
Selection: every pass-98 outline within 25 m of one of the four streets (the OSM street lines in
references/osm-slott98.json) whose nearest named street is one of them, leaving out the houses of
passes 107, 115-119 and 134. Outlines nearer another street (Stensövägen, Margaretaplan, Ringgatan)
are left to the passes of those streets.
Each outline is split into rectangular zones for its roofs with pass 116's slab method (as copied by
pass 134).
Heights in metres above the ground (pass 98 lays the ground at model z 0.30). Measured values are from
Google Street View panoramas (resected on the OSM outlines where noted, or read on the wall plane from
the pano position with an assumed 2.5 m camera); the rest is estimated from storeys, doors and
windows. See references/block136-notes.md.
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
EARLIER={'500979084'}  # pass 107
for n in (115,116,117,118,119,134):EARLIER|=set(json.loads((R/f'source/block{n}.json').read_text())['ids'])

# ---------------------------------------------------------------- selection
MINE=('Drottning Margaretas väg','Sankt Eriks gata','Johan III:s gata','Sankta Britas gata')
ST={}
for w in OSM.values():
 t=w.get('tags',{})
 if 'highway' in t and t.get('name') and len(w.get('points',[]))>1:ST.setdefault(t['name'],[]).append(LineString(w['points']))
SL={k:unary_union(v) for k,v in ST.items()}
def nearest_street(g):return min(SL,key=lambda k:g.distance(SL[k]))
IDS=[];NEAR={}
for b in B98:
 if b['id'] in EARLIER:continue
 g=Polygon(b['outer']).buffer(0)
 if any(g.distance(SL[n])<25 for n in MINE):
  ns=nearest_street(g)
  if ns in MINE:IDS.append(b['id'])
  else:NEAR[b['id']]=ns

# ---------------------------------------------------------------- the houses
# wall: wall colour key; boards: vertical boarding; st: storeys; height/top: eaves and ridge above the
# ground; f0: the ground floor's height above the ground (a raised floor over a basement); roof: saddle,
# hip, gambrel, mhip (hipped mansard) or flat; ridge: 'street' (ridge parallel to the street wall), 'across' (at right angles to it, the gable on the street) or
# the default (along the long side of the main rectangle); rm: roof material; fr: window frame colour;
# seen: the photo the values are read from (None = not seen; estimated); measured: what was measured;
# extras: features drawn in the build; gable_w/gable_top: width and apex (above the ground) of a
# central gable on the street front ('gable_mid').
DMS=dict(boards=False,st=2,f0=1.0,height=8.1,top=12.0,roof='saddle',ridge='street',rm='Tile',fr='Frame')   # the southern row, Drottning Margaretas väg (north-east side)
DMN=dict(boards=False,st=2,f0=.9,height=7.2,top=10.6,roof='saddle',ridge='street',rm='Tile',fr='Frame')    # the northern row, Drottning Margaretas väg (north-east side)
H={
 # ---- Drottning Margaretas väg, the southern row on the north-east side (fronts on the avenue, south-east to north-west)
 '93358522':dict(DMS,name='cream-white rendered south end of the southern row, with the gable on the avenue',wall='PaleCream',height=7.5,top=11.1,
  seen='dm01_h24 (resected)',measured='eaves 7.5 and gable apex 9.4 on the front plane (camera resected on four section joints to (-1427.6, 33.5), 2.5 m assumed; the base is behind the fence)',
  extras=['gable_mid','chimney'],gable_w=5.0,gable_top=9.4),
 '93358514':dict(DMS,name='white rendered section of the southern row with the curved central gable and its round window',wall='WhiteRender',height=7.5,top=11.1,
  seen='dm01_h24 (resected)',measured='eaves 7.5 and gable apex 9.4 on the front plane (same camera)',extras=['gable_mid','oculus','chimney'],gable_w=4.6,gable_top=9.6),
 '93358534':dict(DMS,name='white rendered section of the southern row with dormers',wall='WhiteRender',height=6.9,top=10.6,
  seen='dm01_h24 (behind the tree)',measured='eaves 6.9 on the front plane (same camera)',extras=['dormers']),
 '93358521':dict(DMS,name='white rendered section of the southern row with dormers',wall='WhiteRender',height=6.9,top=10.6,seen='dm01_h24',extras=['dormers','chimney']),
 '93358510':dict(DMS,name='white rendered section of the southern row with the broad dark brown wall dormer and round roof lights',wall='WhiteRender',height=6.9,top=10.6,
  seen='dm01_h24 (left edge)',extras=['dormers_wall','chimney']),
 '93358549':dict(DMS,name='yellow rendered one-and-a-half-storey section of the southern row, lower, with a red tile roof, dormers and the porch roof',wall='Yellow',st=1.5,f0=.6,height=5.0,top=9.0,
  seen='dm02_h24 (behind the tree)',measured='eaves seen at 4.4 on the front plane (the wall stands back, so higher; 5.0 used)',extras=['dormers','canopy']),
 '93358516':dict(DMS,name='yellow-green rendered section of the southern row with the broad gable on the avenue',wall='Sage',height=8.45,top=12.6,
  seen='dm02_h24 (resected)',measured='base at z 0.49 with the camera at 2.5 (so the camera is about 2.0 above the ground), eaves 8.45 and gable apex 12.3 above the ground',
  extras=['gable_mid','chimney'],gable_w=7.0,gable_top=12.3),
 '93358528':dict(DMS,name='grey rendered section of the southern row with the central gable over the white bay window and dormers',wall='GreyWhite',height=8.1,top=12.0,
  seen='dm02_h24 (resected)',measured='eaves 8.1 and gable apex 12.3 above the ground (same camera, base visible)',extras=['gable_mid','oriel','dormers','chimney'],gable_w=3.6,gable_top=12.3),
 '93358531':dict(DMS,name='grey rendered north end of the southern row with dormers and the arched gateway',wall='GreyWhite',height=8.1,top=12.0,
  seen='dm02_h24 (resected)',measured='eaves 8.1 above the ground (same camera)',extras=['dormers','arch_door','chimney']),
 # ---- Drottning Margaretas väg, the northern row on the north-east side (fronts on the avenue, south to north)
 '93361162':dict(DMN,name='white rendered two-storey block over a basement at the south end of the northern row, with the broad dark wall dormers and the side balconies',wall='WhiteRender',
  seen='dm03_h39',measured='eaves 7.2 above the base (camera 2.5 assumed, pano position)',extras=['dormers_wall','chimney']),
 '93361185':dict(DMN,name='cream rendered two-storey block over a basement (not seen; as its neighbours)',wall='Cream',seen=None,extras=['dormers']),
 '93361177':dict(DMN,name='cream rendered two-storey block over a basement (not seen; as its neighbours)',wall='PaleCream',seen=None,extras=['dormers','chimney']),
 '93361214':dict(DMN,name='white rendered two-storey block over a basement (not seen; as its neighbours)',wall='WhiteRender',seen=None,extras=['dormers']),
 '93361247':dict(DMN,name='white rendered two-storey block with the dark metal-clad roof storey (a modern roof extension)',wall='WhiteRender',roof='mhip',rm='RoofDark',top=10.4,
  seen='dm05_h51 (right edge)',extras=[]),
 '93361242':dict(DMN,name='light yellow rendered two-storey block over a basement with red dormers',wall='PaleYellowRender',seen='dm05_h51',extras=['dormers']),
 '93361235':dict(DMN,name='cream rendered two-storey block over a basement with the dark red wall dormers',wall='Cream',seen='dm05_h51',
  measured='eaves 7.2 above the base (camera resected on 93361172\'s two front corners)',extras=['dormers_wall','chimney']),
 '93361172':dict(DMN,name='red rendered two-storey block over a basement with the balcony over the door and a small dormer, at the north end of the northern row',wall='Red',height=7.1,top=10.4,
  seen='dm05_h51 (resected)',measured='base at z 0.37, eaves 7.1 above it (camera resected on the two front corners to (-1568.3, 302.7))',extras=['entrance_balcony','dormers','chimney']),
 # ---- Drottning Margaretas väg, the south-west side and the villas
 '93566374':dict(name='beige-yellow rendered two-storey block over a basement with a red-brown tile roof',wall='PaleYellowRender',boards=False,st=2,f0=.9,height=6.6,top=9.2,roof='saddle',rm='TileBrown',fr='Frame',
  seen='dm05_h231 (right)',extras=['chimney']),
 '93505718':dict(name='white rendered one-and-a-half-storey villa with a red tile roof, the cross gable with the balcony and the glazed veranda',wall='WhiteRender',boards=False,st=1.5,f0=.6,height=4.0,top=8.4,
  roof='saddle',rm='Tile',fr='Frame',seen='dm04_h219',extras=['gable_mid','balcony','chimney'],gable_w=4.4,gable_top=7.6),
 '93460219':dict(name='yellow boarded one-and-a-half-storey villa with a red tile hipped mansard roof and two dormers',wall='YellowBoard',boards=True,st=1.5,f0=.5,height=3.8,top=8.6,roof='mhip',rm='Tile',fr='Frame',
  seen='dm01_h204',extras=['dormers2','chimney']),
 '93460240':dict(name='red boarded two-storey house with a red tile roof and white trim',wall='RedBoard',boards=True,st=2,height=5.6,top=9.0,roof='saddle',rm='Tile',fr='Frame',seen='dm01_h204 (right edge)',extras=['chimney']),
 '93460227':dict(name='yellow boarded villa with a brown tile roof, the cross gable over the glazed veranda with the balcony',wall='YellowBoard',boards=True,st=1.5,f0=.6,height=4.6,top=9.0,roof='saddle',rm='TileBrown',fr='Frame',
  seen='dm02_h204',extras=['gable_mid','balcony','chimney'],gable_w=5.2,gable_top=8.4),
 '93460193':dict(name='white garage with a dark roof behind the villa',wall='WhiteRender',boards=False,st=1,height=2.6,top=4.0,roof='saddle',rm='RoofDark',fr='Frame',seen='dm02_h204 (centre, far)',extras=['garage_door']),
 '93460178':dict(name='cream rendered two-storey villa with a red tile roof and two chimneys',wall='Cream',boards=False,st=2,height=5.4,top=8.8,roof='saddle',rm='Tile',fr='Frame',seen='dm02_h204 (right)',extras=['chimneys2']),
 # ---- Johan III:s gata
 '93329997':dict(name='white rendered two-storey house over a basement with a red tile hipped roof and the central gable',wall='WhiteRender',boards=False,st=2,f0=1.3,height=8.4,top=11.6,roof='hip',rm='Tile',fr='Frame',
  seen='j302_h340 (resected)',measured='eaves 8.4 and central gable apex 11.6 (on the front plane; 11.2 used, the gable is lower than the ridge in the comparison) above the estimated ground (camera resected on the two front corners to (-1406.7, 161.0); the base is behind the hedge)',
  extras=['gable_mid','chimney'],gable_w=5.0,gable_top=11.2),
 '93329986':dict(name='low white rendered house with a red tile roof',wall='WhiteRender',boards=False,st=1,height=3.0,top=5.4,roof='saddle',rm='Tile',fr='Frame',seen='j302_h340 (right)'),
 '149905963':dict(name='white rendered one-and-a-half-storey house with a red tile roof (seen only far)',wall='WhiteRender',boards=False,st=1.5,height=4.0,top=7.4,roof='saddle',rm='Tile',fr='Frame',seen='j302_h340 (far right)'),
 '93329955':dict(name='long low white house with a red tile roof behind the white garden wall',wall='WhiteRender',boards=False,st=1,height=3.0,top=5.4,roof='saddle',rm='Tile',fr='Frame',seen='j301_h341'),
 '93329954':dict(name='low white house with a red tile roof at the garden wall',wall='WhiteRender',boards=False,st=1,height=2.8,top=5.0,roof='saddle',rm='Tile',fr='Frame',seen='j301_h341',extras=['no_door']),
 '93329936':dict(name='cream rendered two-storey 1990s terrace with red tile roofs and gabled dormers',wall='Cream',boards=False,st=2,height=5.6,top=8.8,roof='saddle',rm='Tile',fr='Frame',seen='j301_h341 (right)',extras=['dormers2']),
 '93329963':dict(name='cream rendered two-storey 1990s terrace house with a red tile roof (the east end of the terrace)',wall='Cream',boards=False,st=2,height=5.6,top=8.8,roof='saddle',rm='Tile',fr='Frame',seen='j301_h341 (far right)'),
 '93329984':dict(name='white boarded two-storey block over a basement with the brown boarded roof storey and a low dark roof',wall='White',boards=True,st=2,f0=1.2,height=8.2,top=9.4,roof='saddle',rm='RoofDark',fr='Frame',
  seen='j301_h161 (close, scaffolding)',measured='read at 9.7 from the pano position (not resected, 8 m away); 8.2 used from the storeys',extras=['attic']),
 '93358517':dict(name='white rendered one-and-a-half-storey house with a red tile roof (not seen)',wall='WhiteRender',boards=False,st=1.5,height=4.2,top=7.8,roof='saddle',rm='Tile',fr='Frame',seen=None),
 '93358519':dict(name='white rendered two-storey house with a red tile hipped roof',wall='WhiteRender',boards=False,st=2,height=6.2,top=9.4,roof='hip',rm='Tile',fr='Frame',seen='dm03_h39 (far)',extras=['chimney']),
 '93358524':dict(name='cream rendered two-and-a-half-storey house with a red tile roof and dark red dormers',wall='PaleYellowRender',boards=False,st=2,f0=.6,height=6.8,top=10.6,roof='saddle',rm='Tile',fr='Frame',
  seen='se01_h231 (right)',extras=['dormers']),
 # ---- Sankt Eriks gata, west side (fronts on the street, north to south)
 '93358535':dict(name='white rendered two-storey 1940s block over a basement with balconies on the gable',wall='WhiteRender',boards=False,st=2,f0=.9,height=6.6,top=9.6,roof='saddle',ridge='street',rm='RoofGrey',fr='Frame',seen='se01_h231 (close)'),
 '93358513':dict(name='cream rendered two-storey town house (not seen)',wall='Cream',boards=False,st=2,f0=.6,height=7.0,top=10.2,roof='saddle',ridge='street',rm='Tile',fr='Frame',seen=None),
 '93358507':dict(name='orange rendered two-storey town house',wall='OrangeRender',boards=False,st=2,f0=.6,height=7.6,top=10.8,roof='saddle',ridge='street',rm='Tile',fr='Frame',
  seen='se02_h231 (right edge)',measured='eaves 7.5 above the base (camera 2.5 assumed, pano position)',extras=['chimney']),
 '93358523':dict(name='pink rendered two-storey 1910s house with the pedimented centre bay, white pilasters and the round window over the door',wall='Pink',boards=False,st=2,f0=.6,height=7.2,top=10.3,roof='saddle',ridge='street',rm='Tile',fr='Frame',
  seen='se02_h231 (resected)',measured='eaves 7.15 and pediment apex 9.6 above the base (camera resected on the two front corners to (-1358.5, 61.3))',extras=['gable_mid','door_mid','oculus_door','chimney'],gable_w=3.6,gable_top=9.6),
 '93358536':dict(name='dark boarded two-storey house with the white oriel on the upper floor',wall='Charcoal',boards=True,st=2,height=7.3,top=10.4,roof='saddle',ridge='street',rm='RoofDark',fr='Frame',
  seen='se02_h231 (left)',measured='eaves 7.3 above the base (camera 2.5 assumed, pano position)',extras=['oriel','chimney'],oriel_near='93358523'),
 '93358511':dict(name='small garage (not seen)',wall='GreyBoard',boards=True,st=1,height=2.5,top=3.6,roof='saddle',rm='Tile',fr='Frame',seen=None,extras=['garage_door']),
 '93358540':dict(name='small garage (not seen)',wall='GreyBoard',boards=True,st=1,height=2.5,top=3.6,roof='saddle',rm='Tile',fr='Frame',seen=None,extras=['garage_door']),
 '93358515':dict(name='red-brown boarded two-storey house with a red tile roof at the south end',wall='RedBoard',boards=True,st=2,height=5.6,top=9.0,roof='saddle',rm='Tile',fr='Frame',seen='dm01_h24 (far right)',extras=['chimney']),
 # ---- Sankt Eriks gata, east side
 '93329949':dict(name='light brick one-and-a-half-storey house with a black tile mansard roof (gable on the street) and solar panels',wall='LightBrick',boards=False,st=1.5,f0=.4,height=3.4,top=8.0,roof='gambrel',ridge='across',rm='RoofDark',fr='Frame',
  seen='se01_h51 (close)'),
 '93329985':dict(name='small outbuilding behind the brick house',wall='WhiteRender',boards=False,st=1,height=2.5,top=3.8,roof='saddle',rm='RoofDark',fr='Frame',seen='se01_h51 (behind)',extras=['no_door']),
 '93329935':dict(name='pink rendered two-and-a-half-storey house with a red tile roof and gabled dormers',wall='Pink',boards=False,st=2,f0=.6,height=6.5,top=10.2,roof='saddle',rm='Tile',fr='Frame',
  seen='se02_h51 (left)',measured='eaves about 6.5 (a grazing view from the pano position; estimated)',extras=['dormers2','chimney']),
 '93329968':dict(name='small shed between the villas',wall='GreyBoard',boards=True,st=1,height=2.4,top=3.6,roof='saddle',rm='Tile',fr='Frame',seen='se02_h51 (behind the hedge)',extras=['no_door']),
 '93329973':dict(name='sage-green boarded one-and-a-half-storey villa with a red tile roof, the glazed gable bay and the round window',wall='SageBoard',boards=True,st=1.5,f0=.5,height=4.2,top=8.8,roof='saddle',rm='Tile',fr='Frame',
  seen='se02_h51 (right)',extras=['gable_mid','oculus','chimney'],gable_w=4.0,gable_top=8.0),
 # ---- Sankta Britas gata
 '93329941':dict(name='yellow rendered one-and-a-half-storey house in 18th-century style with a brown tile mansard roof, the curved gable and dormers, behind the green door gateway',wall='Yellow',boards=False,st=1.5,f0=.5,height=5.5,top=10.0,
  roof='gambrel',rm='TileBrown',fr='Frame',seen='sb01_h235 (close)',measured='base at -0.25, eaves 5.5 above it, gable apex about 10.6 (camera 2.5 assumed, pano position)',extras=['dormers','chimneys2']),
 '93329959':dict(name='low ochre house with a red sheet roof behind the picket fence',wall='Ochre',boards=False,st=1,height=2.8,top=4.6,roof='saddle',rm='RoofRed',fr='Frame',seen='sb01_h235 (behind the fence)'),
 '93329996':dict(name='red boarded shed',wall='RedBoard',boards=True,st=1,height=2.4,top=3.6,roof='saddle',rm='Tile',fr='Frame',seen='sb01_h235 (left, far)',extras=['no_door']),
 '93329994':dict(name='red boarded one-and-a-half-storey house with white corner boards and a red tile roof',wall='RedBoard',boards=True,st=1.5,height=4.4,top=8.0,roof='saddle',rm='Tile',fr='Frame',seen='sb01_h235 (left edge)',extras=['chimney']),
 '93329942':dict(name='yellow rendered two-storey house with a red tile roof (not seen)',wall='Yellow',boards=False,st=2,height=5.8,top=9.2,roof='saddle',rm='Tile',fr='Frame',seen=None,extras=['chimney']),
}
# No outline in the selection is a cleared site or demolished in the 2025 imagery as far as the photos show
# (several are not seen at all; see the notes).
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

OUT={i:Polygon(BY[i]['outer']).buffer(0) for i in IDS}
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
SPLIT={}
zones={}
for osm in IDS:
 spec=H[osm]
 if osm in SPLIT:
  a_,b_,s_=SPLIT[osm]
  west=OUT[osm].intersection(strip(a_,b_,-1,s_,OUT[osm]))
  rs=[('main',orient(box_in(west,a_,b_)))]
  for bit in flat(OUT[osm].difference(rs[0][1])):
   if bit.area>3:rs.append(('rest',orient(box_in(bit,a_,b_))))
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
  if fr=='main':z=dict(height=spec['height'],top=spec['top'],roof=spec['roof'],role='main',ridge_fixed=True)
  elif fr=='rest':z=dict(spec['rest'],role='wing',ridge_fixed=True)
  elif k==0:z=dict(height=spec['height'],top=spec['top'],roof=spec['roof'],role='main')
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
  # the remainder joins the nearest zone; unlike pass 118 its slivers are kept down to 0.05 m²
  o_,ps_,sp_=zones[k];zones[k]=(o_,[orient(r) for q in flat(unary_union(ps_+[bit])) for r in flat(q.simplify(.02)) if r.area>.05],sp_)
others=[(Polygon(b['outer']).buffer(0),max(2.6,min(b['height'] or (b['levels']*3.0+.5),28.0)),b['id']) for b in B98 if b['id'] not in IDS]
def neighbour_at(osm,pt):
 for name,(o,ps,spec) in zones.items():
  if o==osm and any(p.buffer(.001).contains(pt) for p in ps):return name,spec['height']
 for g,h,bid in others:
  if g.buffer(.001).contains(pt):return bid,h-.30
 return None,0.0
# the streets a door may face: the pass's four, and the side streets of the corner houses
DOORST=MINE+('Stensövägen','Margaretaplan','Ringgatan','Torsgatan','Långviksvägen','Ståthållaregatan','Gustaf Vasagatan')
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
 out[name]=dict(spec,osm=osm,mesh='SM_Slott136_'+osm,wall=spec.get('wall',hs['wall']),boards=spec.get('boards',hs['boards']),brick=False,
  polygons=[[list(v) for v in list(p.exterior.coords)[:-1]] for p in ps],walls=walls)
 report[name]={'osm':osm,'role':spec['role'],'roof':spec['roof'],'area_m2':round(sum(p.area for p in ps),1),'walls':len(walls),'outer_m':round(sum(math.dist(w['p'],w['q']) for w in walls if w['kind']=='outer'),1),'street':spec['street']}
foot=unary_union(list(OUT.values()));covered=unary_union([p for o,ps,s in zones.values() for p in ps])
houses={i:{k:v for k,v in H[i].items()} for i in IDS}
near_other={k:v for k,v in NEAR.items()}
data={'demolished':sorted(DEMOLISHED),'source':'pass 98 outlines (source/block98.json, from references/osm-slott98.json, OpenStreetMap, ODbL)','ground_z':0.30,'ids':IDS,'left_to_other_streets':near_other,'houses':houses,'zones':out,
 'checks':{'buildings':len(IDS),'footprint_m2':round(foot.area,1),'zoned_m2':round(covered.area,1),'outside_osm_m2':round(covered.difference(foot).area,2),'osm_not_zoned_m2':round(foot.difference(covered).area,2),
  'overlap_m2':round(sum(p.area for o,ps,s in zones.values() for p in ps)-covered.area,3),
  'outlines_overlapping_m2':round(sum(OUT[a].intersection(OUT[b]).area for i,a in enumerate(IDS) for b in IDS[i+1:]),3),
  'zones_per_building':{i:sum(1 for o,ps,s in zones.values() if o==i and ps) for i in IDS}}}
(R/'source/block136.json').write_text(json.dumps(data,indent=1,ensure_ascii=False))
# pass 134's limits (outside OSM < 0.3 m², not zoned < 0.5 m², overlap within the outlines' own overlap + 0.2 m²)
c=data['checks'];ok=c['outside_osm_m2']<.3 and c['osm_not_zoned_m2']<.5 and c['overlap_m2']<.2+c['outlines_overlapping_m2'] and all(c['zones_per_building'].values())
(R/'previews/block136-zones.json').write_text(json.dumps({'status':'passed' if ok else 'review_required','zones':report,'checks':c},indent=2,ensure_ascii=False))
for k,v in report.items():print(k,v)
print(c);print('BLOCK136_ZONES_OK' if ok else 'BLOCK136_ZONES_REVIEW')
