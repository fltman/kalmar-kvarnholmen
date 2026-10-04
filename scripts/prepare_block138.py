"""Pass 138: the mainland street houses along Stensövägen, Stensviksvägen, Långviksvägen and
Sturevägen, west and south-west of Drottning Margaretas väg. Pass 98 built these houses as plain
volumes inside its chunk mesh W (source/block98.json, OSM, ODbL). The housing: on Stensövägen, near
Ståthållaregatan, the rendered two-storey town houses (the beige corner house with the shop, the pink
house with two chimneys, the white corner house with the dark red dormer), the pale yellow and white
blocks over basements with dormers; further west the villas behind the hedges (the grey-white villa with
the dark mansard roof and the black balcony, the white boarded house, the beige villa with the hipped
roof). The villa quarter between Sturevägen, Långviksvägen and Stensviksvägen: boarded and rendered
villas of the 1900s-1930s in white, yellow, olive green, salmon and grey-blue, with cross gables over
porches with balconies, mansard roofs, the white villa with the octagonal tower and the white house
with the tower-like top storey; the cream block with the dark red wall dormers on Långviksvägen; on
Stensviksvägen the grey 1930s block with the pedimented door, the yellow boarded houses, the two new
white houses at the east end and the garages and sheds behind.
Selection: every pass-98 outline whose nearest named street (the OSM street lines in
references/osm-slott98.json) is one of the four, leaving out the ids already claimed in any
source/block*.json (passes 107, 115-119, 134, 136 and the rest). Passes 134 and 136 took only the
outlines within 25 m of their streets; here the back-lot houses beyond 25 m whose nearest street is
still one of the four are taken too (listed in 'beyond_25m'), because they stand in the same closed
blocks and no other street reaches them. Outlines within 25 m that are nearer another street are left to
those streets ('left_to_other_streets'). 93326725 on Stensövägen at Vegagatan is clipped by pass 98's
model box at y 320 (two small pieces of a block that stands mostly outside the model); it stays in the
chunk ('left_clipped').
Each outline is split into rectangular zones for its roofs with pass 116's slab method (as copied by
passes 134 and 136).
Heights in metres above the ground (pass 98 lays the ground at model z 0.30). Measured values are from
Google Street View panoramas captured for this pass (SCR captures '138|'), resected on the OSM outlines
where noted; the rest is estimated from storeys, doors and windows. See references/block138-notes.md.
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
# every id claimed by an earlier pass: the chapel of pass 107 and every source/block*.json's ids and
# demolished ids (this pass's own file excluded)
EARLIER={'500979084'}
for f in sorted((R/'source').glob('block*.json')):
 if f.name=='block138.json':continue
 d=json.loads(f.read_text())
 if isinstance(d,dict):EARLIER|=set(map(str,d.get('ids',[])))|set(map(str,d.get('demolished',[])))

# ---------------------------------------------------------------- selection
MINE=('Stensövägen','Stensviksvägen','Långviksvägen','Sturevägen')
ST={}
for w in OSM.values():
 t=w.get('tags',{})
 if 'highway' in t and t.get('name') and len(w.get('points',[]))>1:ST.setdefault(t['name'],[]).append(LineString(w['points']))
SL={k:unary_union(v) for k,v in ST.items()}
def nearest_street(g):return min(SL,key=lambda k:g.distance(SL[k]))
CLIPPED=sorted({b['id'] for b in B98 if sum(1 for c in B98 if c['id']==b['id'])>1 and b['id'] not in EARLIER})
IDS=[];NEAR={};BEYOND={}
for b in B98:
 if b['id'] in EARLIER or b['id'] in CLIPPED:continue
 g=Polygon(b['outer']).buffer(0);ns=nearest_street(g);dmin=min(g.distance(SL[n]) for n in MINE)
 if ns in MINE:
  IDS.append(b['id'])
  if dmin>=25:BEYOND[b['id']]=[ns,round(dmin,1)]
 elif dmin<25:NEAR[b['id']]=ns

# ---------------------------------------------------------------- the houses
# wall: wall colour key; boards: vertical boarding; st: storeys; height/top: eaves and ridge above the
# ground; f0: the ground floor's height above the ground (a raised floor over a basement); roof: saddle,
# hip, gambrel, mhip (hipped mansard) or flat; ridge: 'street' (ridge parallel to the street wall),
# 'across' (at right angles to it, the gable on the street) or the default (along the long side of the
# main rectangle); rm: roof material; fr: window frame colour; seen: the photo the values are read from
# (None = not seen; estimated); measured: what was measured; extras: features drawn in the build;
# gable_w/gable_top: width and apex (above the ground) of a central gable on the street front
# ('gable_mid'); nd: the number of dormers on the street slope where it differs from the rule.
V1=dict(boards=True,st=1.5,f0=.6,roof='saddle',rm='Tile',fr='Frame')        # a boarded villa of one and a half storeys
VR=dict(boards=False,st=1.5,f0=.6,roof='saddle',rm='Tile',fr='Frame')       # a rendered villa of one and a half storeys
SH=dict(boards=True,st=1,height=2.4,top=3.6,roof='saddle',rm='Tile',fr='Frame',extras=['no_door'])   # a shed
GA=dict(boards=True,st=1,height=2.5,top=3.6,roof='saddle',rm='Tile',fr='Frame',extras=['garage_door'])  # a garage
H={
 # ---- Stensövägen, the east end near Ståthållaregatan (south-east side, north-east to south-west)
 '93329947':dict(name='white rendered two-storey corner house with a red tile roof and the dark red boarded wall dormer',wall='WhiteRender',boards=False,st=2,f0=.5,height=6.6,top=10.0,roof='saddle',rm='Tile',fr='Frame',
  seen='so03_h140 (left)',extras=['dormers_wall','chimney'],nd=1,dormer_mat='DormerRed'),
 '93329999':dict(name='pink rendered two-storey house with a red-brown tile roof (the east part of the pink house)',wall='Pink',boards=False,st=2,f0=.3,height=5.5,top=8.6,roof='saddle',ridge='street',rm='TileBrown',fr='Frame',
  seen='so02_h130 (right edge)',measured='as 93329962 (the same facade continues)',extras=['chimney']),
 '93329962':dict(name='pink rendered two-storey corner house with a red-brown tile roof, two chimneys and the café door',wall='Pink',boards=False,st=2,f0=.3,height=5.5,top=8.6,roof='saddle',ridge='street',rm='TileBrown',fr='Frame',
  seen='so02_h130 (resected)',measured='base at z 0.4, eaves 5.3 at the corner and 5.95 along the front, i.e. about 5.5 above the ground (camera resected on the side wall\'s two corners to (-1411.1, 228.7))',extras=['chimneys2']),
 '93329960':dict(name='beige rendered two-storey corner house with a red tile roof, dormers, a balcony and the shop door',wall='GreyBeige',boards=False,st=2,f0=.4,height=6.4,top=9.8,roof='saddle',ridge='street',rm='Tile',fr='Frame',
  seen='so01_h150 (close), so08_h105 (left)',extras=['dormers','chimney']),
 '93329969':dict(name='light rendered two-storey house behind the street row (seen only far)',wall='PaleCream',boards=False,st=2,f0=.3,height=5.8,top=8.8,roof='saddle',rm='Tile',fr='Frame',seen='so03_h140 (far, centre)'),
 # ---- Stensövägen, north-west side near Ståthållaregatan
 '93361249':dict(name='pale yellow rendered two-storey block over a basement with a red tile roof and three broad dormers',wall='PaleYellowRender',boards=False,st=2,f0=.8,height=7.4,top=10.8,roof='saddle',ridge='street',rm='Tile',fr='Frame',
  seen='so04_h304 (resected)',measured='base at z 0.32, eaves 7.7 above model zero, i.e. 7.4 above the ground (camera resected on the front corners to (-1393.4, 239.0))',extras=['dormers_wall','chimney'],nd=3,dormer_mat='PaleYellowRender'),
 '94560067':dict(name='white rendered two-storey block over a basement with a red tile roof and the central gabled wall dormer',wall='WhiteRender',boards=False,st=2,f0=.8,height=7.2,top=10.6,roof='saddle',ridge='street',rm='Tile',fr='Frame',
  seen='so05_h310 (resected)',measured='base at z 0.27, eaves 7.5 and the dormer top 9.6 on the front plane (camera resected on the front corners to (-1285.7, 276.4)); eaves 7.2 above the ground',extras=['gdormers'],nd=1,dormer_mat='Weathered'),
 # ---- Stensövägen, the south-west part (villas behind the hedges, north-west side, then south-east side)
 '93505743':dict(V1,name='white boarded one-and-a-half-storey house with a red tile roof behind the trees',wall='White',height=4.0,top=8.0,seen='so06_h333, so10_h20 (right)',extras=['chimney']),
 '93505722':dict(VR,name='grey-white rendered one-and-a-half-storey villa with a dark tile mansard roof and the black balcony',wall='GreyWhite',height=3.6,top=7.8,roof='gambrel',rm='RoofDark',
  seen='so10_h20 (centre), so06_h333 (left)',extras=['chimney','gable_balcony']),
 '93505764':dict(VR,name='grey-white rendered wing of the mansard villa with a dark roof',wall='GreyWhite',st=1,height=3.0,top=5.4,rm='RoofDark',seen='so10_h20 (behind)',extras=['no_door']),
 '93505682':dict(VR,name='cream rendered one-and-a-half-storey villa with a dark roof and a chimney (not seen clearly)',wall='Cream',height=3.8,top=7.8,rm='RoofDark',seen=None,extras=['chimney']),
 '93487559':dict(VR,name='beige rendered one-storey villa with a dark tile hipped roof and a chimney',wall='GreyBeige',st=1,f0=.6,height=3.1,top=6.2,roof='hip',rm='RoofDark',seen='so07_h137 (centre)',extras=['chimney']),
 '93487562':dict(VR,name='cream rendered one-and-a-half-storey house with a red tile roof and the cross gable',wall='PaleCream',height=4.0,top=8.0,seen='so07_h137 (right)',extras=['gable_mid','chimney'],gable_w=4.0,gable_top=7.4),
 '93487555':dict(SH,name='small outbuilding behind the cream house',wall='WhiteRender',boards=False,seen='so07_h137 (right edge, behind)'),
 # ---- Sturevägen (east side, north to south)
 '93460233':dict(VR,name='white rendered one-and-a-half-storey villa with a dark tile roof behind the trees',wall='WhiteRender',height=3.8,top=7.6,rm='RoofDark',seen='su03_h120 (centre)',extras=['chimney']),
 '93461693':dict(SH,name='small outbuilding behind the villa',wall='WhiteRender',boards=False,rm='RoofDark',seen='su01_h100 (behind)'),
 '93460152':dict(VR,name='low white rendered one-storey villa with the dark brown boarded gable and a dark tile roof',wall='WhiteRender',st=1,f0=.4,height=2.9,top=5.8,rm='RoofDark',ridge='across',seen='su01_h100 (left)',extras=['chimney','gable_boards']),
 '93460179':dict(V1,name='white boarded one-storey house with a dark tile roof behind the birch',wall='White',st=1,f0=.5,height=3.0,top=5.8,rm='RoofDark',seen='su04_h60 (right), su01_h100 (right)',extras=['chimney']),
 '93460211':dict(GA,name='garage behind the white house',wall='GreyBoard',rm='RoofDark',seen='su01_h100 (behind the hedge)'),
 '93460230':dict(SH,name='small shed behind the white house',wall='GreyBoard',rm='RoofDark',seen='su01_h100 (behind the hedge)'),
 '93460238':dict(V1,name='salmon boarded one-and-a-half-storey house with a red tile roof and the round gable window',wall='SalmonBoard',height=4.2,top=8.4,seen='su02_h90 (left), lv04_h145 (right)',extras=['chimney','oculus_end']),
 '93460174':dict(SH,name='small shed between the villas',wall='GreyBoard',seen='su02_h90 (behind)'),
 '93460232':dict(V1,name='grey-blue boarded one-and-a-half-storey villa with a red tile roof, the cross gable with the balcony over the glazed veranda',wall='BlueGreyBoard',height=4.2,top=8.6,
  seen='su02_h90 (right), su05_h60 (centre)',extras=['gable_mid','balcony','chimney'],gable_w=4.6,gable_top=8.0),
 '93460197':dict(GA,name='grey boarded garage with the green door',wall='GreyBoard',rm='RoofDark',seen='su05_h60 (right)'),
 # ---- Långviksvägen, north side (east to west)
 '93460177':dict(V1,name='white boarded one-and-a-half-storey villa with a red tile roof and the cross gable on the street',wall='White',height=4.0,top=8.2,seen='lv01_h335 (centre)',extras=['gable_mid','chimney'],gable_w=4.4,gable_top=7.6),
 '93460160':dict(VR,name='low white rendered house with a dark roof',wall='WhiteRender',st=1,f0=.3,height=2.8,top=5.0,rm='RoofDark',seen='lv01_h335 (right)'),
 '93460229':dict(GA,name='garage behind the low white house',wall='White',rm='RoofDark',seen='lv01_h335 (right, behind)'),
 '93460196':dict(name='cream rendered two-storey block with a red tile roof, three dark red wall dormers and the balcony on the gable',wall='Cream',boards=False,st=2,f0=.6,height=6.6,top=10.0,roof='saddle',ridge='street',rm='Tile',fr='Frame',
  seen='lv02_h330 (resected)',measured='eaves 6.4 above model zero on the corner (camera resected on the side wall\'s two corners to (-1538.3, -9.5)); the base is behind the shrubs (read at 1.5, not used)',extras=['dormers_wall','chimney'],nd=3),
 '93460195':dict(VR,name='white rendered one-and-a-half-storey house with the gable on the street and a lower beige wing with the entrance',wall='WhiteRender',height=4.2,top=8.4,ridge='across',seen='lv03_h325 (close)',extras=['chimney']),
 # ---- Långviksvägen, south side (east to west) and the back lots
 '93460185':dict(name='white rendered two-and-a-half-storey villa with the tower-like top storey and the roof terrace',wall='WhiteRender',boards=False,st=2,f0=.6,height=6.0,top=8.6,roof='hip',rm='Tile',fr='Frame',
  seen='lv01_h155 (centre)',extras=['tower','chimney']),
 '93460217':dict(VR,name='white rendered one-and-a-half-storey house with a red tile roof (seen only far)',wall='WhiteRender',height=4.0,top=7.8,seen='lv01_h155 (far left)'),
 '93460169':dict(VR,name='white rendered one-and-a-half-storey house behind the tower villa (seen only in part)',wall='WhiteRender',height=4.0,top=7.8,seen='lv01_h155 (behind)'),
 '93460183':dict(V1,name='olive-green boarded one-and-a-half-storey villa with a red tile roof and the decorated gable on the street',wall='OliveBoard',height=4.0,top=8.4,ridge='across',seen='lv02_h150 (left)',extras=['chimney']),
 '93460161':dict(V1,name='white boarded villa with the octagonal tower, the cross gable, the balcony and the glazed porch',wall='White',height=4.6,top=9.0,seen='lv02_h150 (right), lv03_h145 (left)',
  extras=['gable_mid','spire','chimney'],gable_w=4.6,gable_top=8.6),
 '93460226':dict(SH,name='small outbuilding behind the tower villa',wall='White',seen='lv03_h145 (behind)'),
 '93460167':dict(SH,name='small shed behind the tower villa',wall='White',seen='lv03_h145 (behind)'),
 '93460201':dict(SH,name='small shed in the garden',wall='GreyBoard',seen='lv03_h145 (behind)'),
 '93460162':dict(VR,name='white rendered one-and-a-half-storey house in the back lot (not seen)',wall='WhiteRender',height=4.0,top=7.8,seen=None),
 '93460207':dict(SH,name='small shed behind the hedge',wall='GreyBoard',seen='lv03_h145 (right, behind the hedge)'),
 '93460176':dict(V1,name='yellow boarded one-and-a-half-storey villa with a red tile mansard roof and the central cross gable with the balcony over the porch',wall='YellowBoard',height=3.6,top=8.4,roof='gambrel',ridge='street',
  seen='lv04_h145 (resected)',measured='eaves 3.9 above the ground on the front plane, the roof top at 7.3 on the front plane and the cross gable\'s apex at 8.0 (camera resected on the front corners to (-1589.8, -18.9)); the base is behind the fence',
  extras=['gable_mid','balcony','chimneys2'],gable_w=3.6,gable_top=8.0),
 # ---- Stensviksvägen, north side (west to east)
 '93460157':dict(VR,name='white rendered one-and-a-half-storey villa with a dark tile roof, the balcony on the street gable and a dormer',wall='WhiteRender',height=4.2,top=8.4,rm='RoofDark',ridge='across',seen='sv03_h324 (close)',extras=['gable_balcony','chimney']),
 '93460166':dict(VR,name='white rendered one-and-a-half-storey villa with a red tile roof and the dark red wall dormer',wall='WhiteRender',height=4.0,top=8.0,seen='sv01_h338 (left)',extras=['dormers_wall','chimney'],nd=1,dormer_mat='DormerRed'),
 '93460184':dict(VR,name='small white rendered house in the back lot (not seen)',wall='WhiteRender',st=1,height=3.0,top=5.4,seen=None),
 '93460189':dict(GA,name='small garage in the back lot (not seen; the white garage with the green sheet roof on sv02_h338 stands nearer the street and has no OSM outline)',wall='GreyBoard',seen=None),
 '93460200':dict(V1,name='yellow boarded one-and-a-half-storey house with a red tile roof and two gabled dormers',wall='YellowBoard',height=3.8,top=7.8,seen='sv02_h338 (left), sv01_h338 (right)',extras=['dormers2','chimney']),
 '93460199':dict(VR,name='cream rendered one-and-a-half-storey house in the back lot (seen only far)',wall='Cream',height=4.0,top=7.8,seen='sv01_h338 (far right)'),
 '93460164':dict(name='white rendered two-storey villa with a red tile hipped roof, dormers and the balcony over the door',wall='WhiteRender',boards=False,st=2,f0=.6,height=6.0,top=9.4,roof='hip',rm='Tile',fr='Frame',
  seen='sv02_h338 (centre)',extras=['dormers','entrance_balcony','chimney'],nd=2),
 '93477842':dict(name='new white rendered two-storey house with a low red tile roof and solar panels',wall='WhiteRender',boards=False,st=2,height=5.8,top=7.4,roof='saddle',rm='Tile',fr='FrameDark',seen='sv04_h330 (left)',extras=['chimney']),
 '93477789':dict(name='new white rendered two-storey house with the set-back glazed top storey',wall='WhiteRender',boards=False,st=2,height=5.8,top=6.1,roof='flat',rm='RoofDark',fr='FrameDark',seen='sv04_h330 (right)',extras=['glass_top']),
 # ---- Stensviksvägen, south side (east to west)
 '93460165':dict(name='white rendered two-storey block behind the trees',wall='WhiteRender',boards=False,st=2,f0=.4,height=6.2,top=9.4,roof='saddle',rm='Tile',fr='Frame',seen='sv08_h140 (left)'),
 '93460158':dict(name='beige-brown brick two-storey block behind the trees',wall='BrownBrick',boards=False,st=2,f0=.4,height=6.2,top=9.2,roof='saddle',rm='Tile',fr='Frame',seen='sv08_h140 (right)',extras=['chimney']),
 '93460235':dict(SH,name='small shed behind the brick block',wall='GreyBoard',seen='sv08_h140 (behind)'),
 '93460222':dict(name='white rendered two-storey block with a low red tile roof and the garage doors',wall='WhiteRender',boards=False,st=2,height=5.8,top=7.6,roof='saddle',rm='Tile',fr='Frame',seen='sv04_h146 (left)',extras=['chimney']),
 '93460180':dict(VR,name='yellow rendered one-and-a-half-storey house with a red tile roof and dormers',wall='Yellow',height=4.6,top=8.8,seen='sv04_h146 (right), sv05_h150 (left)',extras=['dormers','chimney']),
 '93460155':dict(SH,name='small shed in the back lot (not seen)',wall='GreyBoard',seen=None),
 '93460208':dict(SH,name='white shed with the red door',wall='WhiteRender',boards=False,seen='sv05_h150 (left)',extras=[]),
 '93460234':dict(name='light grey rendered two-storey 1930s block over a basement with a red tile hipped roof, the central wall dormer, the pedimented double door and red-brown window frames',wall='GreyWhite',boards=False,st=2,f0=1.0,height=7.6,top=11.0,roof='hip',rm='TileBrown',fr='FrameRed',
  seen='sv05_h150 (resected)',measured='eaves 7.9 above model zero, i.e. 7.6 above the ground, the wall dormer\'s top 10.4 on the front plane (camera resected on the front corners to (-1512.5, -164.0)); the base is behind the fence',extras=['dormers','door_mid','pediment','chimney'],nd=1),
 '93460163':dict(V1,name='yellow boarded two-storey house with a red tile roof, the broad gable and white trim',wall='YellowBoard',st=2,f0=.4,height=5.6,top=9.2,ridge='across',seen='sv06_h151 (left)',extras=['chimney']),
 '93460181':dict(GA,name='garage beside the yellow house',wall='YellowBoard',seen='sv06_h151 (centre)'),
 '93460237':dict(VR,name='light rendered one-and-a-half-storey house in the back lot (seen only far)',wall='PaleCream',height=4.0,top=7.8,seen='sv06_h151, sv07_h153 (behind the trees)'),
 '93460224':dict(V1,name='yellow boarded one-and-a-half-storey villa with a red tile roof and the central cross gable with the balcony over the porch',wall='YellowBoard',height=4.0,top=8.6,seen='sv07_h153 (centre)',
  extras=['gable_mid','balcony','chimney'],gable_w=4.2,gable_top=8.0),
}
for v in H.values():v.setdefault('extras',[])
# No outline is a cleared site in the photos that show it; the two new houses at the east end of
# Stensviksvägen (93477842, 93477789) stand on their OSM outlines. Several are not seen (see the notes).
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
# the streets a door may face: the pass's four, and the side streets of the corner and back-lot houses
DOORST=MINE+('Torsgatan','Baldersvägen','Margaretaplan','Gustaf Vasagatan','Drottning Margaretas väg','Johan III:s gata','Ståthållaregatan','Kalmarsundsparken')
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
 out[name]=dict(spec,osm=osm,mesh='SM_Slott138_'+osm,wall=spec.get('wall',hs['wall']),boards=spec.get('boards',hs['boards']),brick=False,
  polygons=[[list(v) for v in list(p.exterior.coords)[:-1]] for p in ps],walls=walls)
 report[name]={'osm':osm,'role':spec['role'],'roof':spec['roof'],'area_m2':round(sum(p.area for p in ps),1),'walls':len(walls),'outer_m':round(sum(math.dist(w['p'],w['q']) for w in walls if w['kind']=='outer'),1),'street':spec['street']}
foot=unary_union(list(OUT.values()));covered=unary_union([p for o,ps,s in zones.values() for p in ps])
houses={i:{k:v for k,v in H[i].items()} for i in IDS}
near_other={k:v for k,v in NEAR.items()}
clipped={i:'clipped by pass 98\'s model box at y 320 (two pieces, mostly outside the model); left in the chunk' for i in CLIPPED}
data={'demolished':sorted(DEMOLISHED),'source':'pass 98 outlines (source/block98.json, from references/osm-slott98.json, OpenStreetMap, ODbL)','ground_z':0.30,'ids':IDS,'left_to_other_streets':near_other,'left_clipped':clipped,'beyond_25m':BEYOND,'houses':houses,'zones':out,
 'checks':{'buildings':len(IDS),'footprint_m2':round(foot.area,1),'zoned_m2':round(covered.area,1),'outside_osm_m2':round(covered.difference(foot).area,2),'osm_not_zoned_m2':round(foot.difference(covered).area,2),
  'overlap_m2':round(sum(p.area for o,ps,s in zones.values() for p in ps)-covered.area,3),
  'outlines_overlapping_m2':round(sum(OUT[a].intersection(OUT[b]).area for i,a in enumerate(IDS) for b in IDS[i+1:]),3),
  'zones_per_building':{i:sum(1 for o,ps,s in zones.values() if o==i and ps) for i in IDS}}}
(R/'source/block138.json').write_text(json.dumps(data,indent=1,ensure_ascii=False))
# pass 134's limits (outside OSM < 0.3 m², not zoned < 0.5 m², overlap within the outlines' own overlap + 0.2 m²)
c=data['checks'];ok=c['outside_osm_m2']<.3 and c['osm_not_zoned_m2']<.5 and c['overlap_m2']<.2+c['outlines_overlapping_m2'] and all(c['zones_per_building'].values())
(R/'previews/block138-zones.json').write_text(json.dumps({'status':'passed' if ok else 'review_required','zones':report,'checks':c},indent=2,ensure_ascii=False))
for k,v in report.items():print(k,v)
print(c);print('BLOCK138_ZONES_OK' if ok else 'BLOCK138_ZONES_REVIEW')
