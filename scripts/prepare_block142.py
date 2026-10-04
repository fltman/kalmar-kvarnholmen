"""Pass 142: the mainland yard buildings, the last pass-98 outlines that no street pass claimed. They stand
25 m or more from every named street, in the back lots, courtyards and gardens of the mainland quarters
and in the parks: sheds, garages and garage rows, the outbuildings behind the villas, the back wings and
courtyard houses of the town blocks, the units of two terrace rows whose fronts face a footpath, the villas
on the private drive north of Kalmarsundsparken, the houses at Södra kyrkogården, the yellow former
barracks building on Gamla torget, Café Flädern's yellow boarded house, the courtyard houses behind
Unionsgatan and Smålandsgatan, and the kiosk and the toilets in Kalmarsundsparken. Pass 98 built them as
plain volumes in its chunk meshes W, M and E (source/block98.json, OSM, ODbL).
Selection: every pass-98 outline that no source/blockN.json claims (ids and demolished ids, any N other
than 142) and that is not the Stagnell chapel (pass 107). This is exactly pass 140's 'left_to_yards' list
(59 ids); the script asserts it. After this pass pass 98's chunks hold no building (see the build script
and references/block142-notes.md for how the empty chunks are kept).
Most of these buildings cannot be seen from a street. Their roof form, ridge direction and roof colour are
read from top-down Google satellite captures (SCR captures '142|', view only); heights come from the roof
pitch, the storeys, the neighbouring houses they join and, for four buildings, Street View. Everything not
listed as measured in references/block142-notes.md is estimated.
Each outline is split into rectangular zones for its roofs with pass 116's slab method (as copied by
passes 134-140). Heights in metres above the ground (pass 98 lays the ground at model z 0.30).
"""
from pathlib import Path
import json,math,os,sys,re
if os.environ.get('KALMAR_GEO'):sys.path.insert(0,os.environ['KALMAR_GEO'])
from shapely.geometry import Polygon,Point,LineString
from shapely.geometry.polygon import orient
from shapely.ops import unary_union
R=Path(__file__).resolve().parents[1]
B98ALL=json.loads((R/'source/block98.json').read_text());B98=B98ALL['buildings']
PIECES={}
for b in B98:PIECES.setdefault(b['id'],[]).append(b)
BY={i:v[0] for i,v in PIECES.items()}
OSM=json.loads((R/'references/osm-slott98.json').read_text())
CLAIMED={'500979084'}  # pass 107
for f in sorted((R/'source').glob('block*.json')):
 m_=re.fullmatch(r'block(\d+)\.json',f.name)
 if not m_ or int(m_.group(1))==142:continue
 d_=json.loads(f.read_text())
 if isinstance(d_,dict):CLAIMED|=set(map(str,d_.get('ids',[])))|set(map(str,d_.get('demolished',[])))

# ---------------------------------------------------------------- selection
IDS=sorted(i for i in PIECES if i not in CLAIMED)
YARDS140=set(json.loads((R/'source/block140.json').read_text())['left_to_yards'])
assert set(IDS)==YARDS140,(sorted(set(IDS)-YARDS140),sorted(YARDS140-set(IDS)))
ST={}
for w in OSM.values():
 t=w.get('tags',{})
 if 'highway' in t and t.get('name') and len(w.get('points',[]))>1:ST.setdefault(t['name'],[]).append(LineString(w['points']))
SL={k:unary_union(v) for k,v in ST.items()}
def chunk_of(b):
 cx_=sum(v[0] for v in b['outer'])/len(b['outer']);return 'W' if cx_<-1150 else ('M' if cx_<-850 else 'E')
OUTALL={i:unary_union([Polygon(b['outer']).buffer(0) for b in v]) for i,v in PIECES.items()}
NEAREST={}
for i in IDS:
 g=OUTALL[i];ds=sorted((g.distance(SL[n]),n) for n in SL);NEAREST[i]=[ds[0][1],round(ds[0][0],1)]

# ---------------------------------------------------------------- the buildings
# wall: wall colour key; boards: vertical boarding; st: storeys; height/top: eaves and ridge above the
# ground; f0: the ground floor's height above the ground; roof: saddle, hip, mono (a shed roof falling to
# the door side) or flat; ridge: 'short' turns the ridge onto the short axis of the main zone; rm: roof
# material; frm: the flat roof's material; sat: the satellite capture and what it shows; seen: Street View
# (None = not seen); conf: confidence of the reading (high / medium / low); extras: features drawn in the
# build; parts: [x, y, overrides] gives the zone that contains the point its own height, ridge and roof.
GAR=dict(boards=True,st=1,height=2.5,top=3.6,roof='saddle',rm='Tile',fr='Frame',wall='GreyBoard',extras=['garage_door'])   # passes 136/138's garage
SHED=dict(boards=True,st=1,height=2.3,top=3.0,roof='mono',rm='RoofGrey',fr='Frame',wall='GreyBoard',extras=[])
ROW40=dict(boards=False,st=2,f0=1.0,height=7.0,top=9.4,roof='saddle',ridge='short',rm='Tile',fr='Frame',extras=['chimney'])   # pass 134's 1940s terrace row
H={
 # ---- W: Stora Dammgatan, the rose garden and the 1940s terrace rows (sat_s1, sat_s21)
 '1453534570':dict(boards=True,st=1,height=2.6,top=4.4,roof='saddle',rm='TileBrown',fr='Frame',wall='RedBoard',extras=[],
  name='long boarded shed against the wall of the rose garden (Kalmar rosenträdgård)',sat='sat_s1: saddle along the long axis, the south slope pale brown, the north slope in shadow',conf='medium'),
 '93238186':dict(SHED,wall='RedBoard',rm='RoofDark',name='small garden shed east of the rose garden',sat='sat_s1: a small dark roof, partly under trees',conf='low'),
 '93238220':dict(ROW40,wall='Cream',name='section of the 1940s terrace row (13E/13F) behind Ståthållaregatan, joining pass 134\'s 93238253',
  sat='sat_s21: the red tile roofs of the stepped row, a chimney on each section',conf='medium (heights as pass 134\'s neighbour)'),
 '93238284':dict(ROW40,wall='Red',name='section of the 1940s terrace row (13F) behind Ståthållaregatan',sat='sat_s21: red tile roof of the row\'s south-west end',conf='medium (heights as the row)'),
 '93238239':dict(boards=False,st=1.5,f0=.4,height=3.8,top=6.6,roof='saddle',rm='Tile',fr='Frame',wall='Cream',extras=['chimney'],
  name='north-east end section of the terrace row 13G/13H on the footpath north of Stora Dammgatan, joining pass 119\'s 93238263',
  sat='sat_s21: red tile roof continuous with the row, two dark roof windows',conf='medium (heights as pass 119\'s neighbour, which may be low)'),
 '93238221':dict(boards=True,st=1.5,f0=.6,height=4.2,top=8.4,roof='saddle',rm='Tile',fr='Frame',wall='YellowBoard',extras=['dormers','chimney'],nd=2,
  name='one-and-a-half-storey house in the garden south of the rose garden (no. 24)',sat='sat_s1: red tile saddle along the long axis with dormers on both slopes',conf='medium'),
 # ---- W: behind Västerlånggatan (sat_s2)
 '93238283':dict(boards=False,st=2,f0=.5,height=5.8,top=8.6,roof='hip',rm='TileBrown',fr='Frame',wall='Cream',extras=['chimney'],
  name='two-storey house in the garden west of Västerlånggatan 28 (near the drive)',sat='sat_s2: brown tile hipped roof with a light terrace in the middle',conf='low'),
 '93238290':dict(boards=True,st=1,height=2.6,top=3.8,roof='saddle',rm='RoofGrey',fr='Frame',wall='RedBoard',extras=['garage_door'],
  name='long boarded garage beside it',sat='sat_s2: long grey roof, partly under trees',conf='low'),
 '93329957':dict(boards=False,st=1.5,f0=.6,height=4.2,top=8.4,roof='hip',rm='Tile',fr='Frame',wall='WhiteRender',extras=['chimney'],
  name='villa with the cross-gabled red tile roof and the round bay, Västerlånggatan 28, in its large garden',sat='sat_s2: red tile roof with several hipped and gabled parts and a rounded bay',conf='medium'),
 # ---- W: the blocks between Ståthållaregatan, Johan III:s gata and Sankta Britas gata (sat_s3)
 '93291962':dict(boards=False,st=2,f0=.5,height=5.8,top=7.8,roof='saddle',rm='Tile',fr='Frame',wall='White',extras=['chimney'],
  name='terrace house 1E behind Sankta Britas gata',sat='sat_s3: red tile roof with a chimney, one of the row 1A-1F',conf='medium (heights as pass 119\'s 93292003)'),
 '93291967':dict(boards=False,st=2,f0=.5,height=5.8,top=7.8,roof='saddle',rm='Tile',fr='Frame',wall='White',extras=['chimney'],
  name='terrace house 1F, joining pass 119\'s white house 93292003',sat='sat_s3: red tile roof with a chimney',conf='medium (heights as pass 119\'s 93292003)'),
 '93292008':dict(boards=False,st=2,f0=.5,height=5.8,top=7.8,roof='saddle',rm='Tile',fr='Frame',wall='White',extras=['chimney'],
  name='north section of the same row',sat='sat_s3: red tile roof with a chimney, level with 1E',conf='medium'),
 '93329938':dict(boards=False,st=1,f0=.4,height=3.0,top=5.6,roof='hip',rm='Tile',fr='Frame',wall='WhiteRender',extras=['chimney'],
  name='L-shaped one-storey house with the red tile hipped roof',sat='sat_s3: L-shaped hipped roof, red tile',conf='high (roof); medium (height)'),
 '93329953':dict(boards=False,st=2,f0=.6,height=5.8,top=9.2,roof='hip',rm='Tile',fr='Frame',wall='PaleYellowRender',extras=['chimney'],
  name='two-storey villa with the red tile hipped roof (no. 6)',sat='sat_s3: square red tile hipped roof with cross gables',conf='medium'),
 '93329965':dict(boards=False,st=1.5,f0=.5,height=4.0,top=7.6,roof='hip',rm='Tile',fr='Frame',wall='Yellow',extras=['chimney'],
  name='one-and-a-half-storey house with a wing, Wollinska Stiftelsen',sat='sat_s3: red tile hipped roof with a short wing',conf='medium'),
 '93329980':dict(boards=False,st=1,height=3.2,top=3.45,roof='flat',rm='RoofGrey',frm='RoofGrey',fr='Frame',wall='GreyWhite',extras=[],
  name='flat-roofed outbuilding',sat='sat_s3: light grey flat roof',conf='high (roof); medium (height)'),
 '93329987':dict(boards=True,st=1,height=2.5,top=3.8,roof='saddle',rm='Tile',fr='Frame',wall='RedBoard',extras=[],
  name='small red tile outbuilding',sat='sat_s3: small red tile saddle',conf='medium'),
 '93330000':dict(boards=False,st=1.5,f0=.5,height=4.0,top=8.0,roof='saddle',rm='Tile',fr='Frame',wall='Cream',extras=['dormers','chimney'],nd=2,
  name='one-and-a-half-storey house with dormers behind Ståthållaregatan',sat='sat_s3: red tile saddle with dormers, a dark annex on the north-west side',conf='medium'),
 '93330001':dict(boards=False,st=1,f0=.4,height=3.0,top=5.4,roof='hip',rm='RoofGrey',fr='Frame',wall='WhiteRender',extras=[],
  name='small one-storey house with the grey hipped roof (no. 1)',sat='sat_s3: grey sheet hipped roof',conf='medium'),
 # ---- W: Sankt Eriks gata, the garages in the back lots (sat_s4)
 '93358502':dict(GAR,roof='mono',height=2.5,top=3.0,rm='RoofGrey',name='garage in the back lot of Sankt Eriks gata',sat='sat_s4: grey roof, low',conf='medium'),
 '93358543':dict(GAR,roof='mono',height=2.5,top=3.0,rm='RoofGrey',name='garage with the pale ribbed sheet roof',sat='sat_s4: pale grey ribbed roof',conf='medium'),
 '93358547':dict(GAR,roof='mono',height=2.5,top=3.0,rm='RoofGrey',name='garage beside it',sat='sat_s4: grey roof',conf='medium'),
 # ---- W: Sankt Eriks gata / Gustaf Vasagatan block (sat_s11)
 '93329937':dict(boards=False,st=1.5,f0=.4,height=3.8,top=6.6,roof='saddle',rm='Tile',fr='Frame',wall='Cream',extras=['chimney'],
  name='small house in the block\'s back lot with a red tile roof and a flat-roofed part',sat='sat_s11: red tile saddle on the north-west part, a brown-grey low roof on the rest',conf='low'),
 # ---- W: Folkungagatan, Drottning Margaretas väg, Stensövägen, Torsgatan, Baldersvägen (sat_s5, s6, s23, s24)
 '93361181':dict(GAR,height=2.6,top=4.0,rm='RoofGrey',name='L-shaped garage building behind the Folkungagatan rows (north side clipped by the model box)',sat='sat_s6: grey sheet saddle',conf='medium'),
 '93487550':dict(boards=False,st=1.5,f0=.5,height=4.0,top=8.0,roof='hip',rm='Tile',fr='Frame',wall='WhiteRender',extras=['chimney'],
  name='villa with the cross-hipped red tile roof (no. 2) behind Torsgatan',sat='sat_s23: red tile cross-hipped roof',conf='medium'),
 '93487564':dict(boards=False,st=1.5,f0=.4,height=3.6,top=6.8,roof='saddle',rm='Tile',fr='Frame',wall='Cream',extras=['chimney'],
  name='house behind Torsgatan with a red tile saddle and flat-roofed additions',sat='sat_s5: red tile saddle on the west part, grey and pale flat roofs on the rest',conf='low'),
 '93505688':dict(GAR,height=2.5,top=3.8,name='red-roofed garage behind Ringgatan',sat='sat_s24: red tile saddle',conf='medium'),
 '93505695':dict(GAR,height=2.5,top=3.8,name='garage row behind Drottning Margaretas väg',sat='sat_s24: red tile saddle on the south-west part, grey flat roof on the rest',conf='medium'),
 # ---- W: the villas on the drive north of Kalmarsundsparken and Stensviksvägen (sat_s7, s8, s9)
 '93460175':dict(boards=False,st=1.5,f0=.6,height=4.0,top=8.2,roof='saddle',rm='Tile',fr='Frame',wall='WhiteRender',extras=['gable_mid','chimney'],gable_w=3.6,gable_top=7.8,
  name='white rendered villa with the red tile roof and the central gable, 3 Kalmarsundsparken',sat='sat_s7: red tile roof, the north slope in shadow, the gable on the south slope',seen='ks1_h346',conf='high'),
 '93460156':dict(boards=False,st=1.5,f0=.6,height=4.2,top=8.4,roof='saddle',rm='Tile',fr='Frame',wall='Cream',extras=['chimney'],
  name='villa with the red tile roof and the white gable (FL-Net)',sat='sat_s7: red tile roof',seen='ks1_h346 (right, far)',conf='medium'),
 '93460172':dict(boards=False,st=2,f0=.6,height=5.6,top=8.6,roof='hip',rm='Tile',fr='Frame',wall='WhiteRender',extras=['chimney'],
  name='two-storey villa with the hipped roof and the low front part',sat='sat_s7: roof mostly in shadow, the south slope and the front part red tile',conf='low'),
 '93460187':dict(boards=False,st=2,f0=.6,height=5.6,top=9.0,roof='hip',rm='Tile',fr='Frame',wall='Cream',extras=['dormers','chimney'],nd=1,
  name='two-storey villa with the cross-hipped red tile roof (no. 7)',sat='sat_s7: red tile cross-hipped roof',conf='medium'),
 '93460203':dict(GAR,roof='mono',height=2.5,top=3.0,rm='RoofGrey',name='garage north of the villas',sat='sat_s7: grey roof',conf='medium'),
 '93460209':dict(GAR,height=2.5,top=3.8,name='garage beside the villa',sat='sat_s7: red tile roof',conf='medium'),
 '93460194':dict(boards=False,st=1.5,f0=.6,height=4.2,top=8.0,roof='hip',rm='Tile',fr='Frame',wall='PaleYellowRender',extras=['dormers','chimney'],nd=1,
  name='villa with the red tile hipped roof and dormers (15A; west end clipped by the model box)',sat='sat_s8: red-brown tile hipped roof with dormers',conf='medium'),
 '93460204':dict(boards=False,st=2,f0=.6,height=5.6,top=9.0,roof='hip',rm='Tile',fr='Frame',wall='WhiteRender',extras=['dormers','chimney'],nd=1,
  name='two-storey villa with the cross-hipped red tile roof (no. 9)',sat='sat_s8: red tile cross-hipped roof with dormers',conf='medium'),
 '93460214':dict(GAR,height=2.6,top=4.4,rm='TileBrown',wall='RedBoard',name='boarded garage with the brown roof off Gustaf Vasagatan',sat='sat_s9: brown saddle along the long axis',conf='medium'),
 # ---- W: Kalmarsundsparken (sat_s10)
 '874145313':dict(SHED,wall='White',height=2.6,top=3.1,name='the ice cream kiosk (Kalmar Glasskiosk)',sat='sat_s10: small grey roof',conf='medium'),
 '874145314':dict(boards=True,st=1,height=2.6,top=3.6,roof='saddle',rm='TileDark',fr='Frame',wall='RedBoard',extras=[],
  name='the public toilets in the park',sat='sat_s10: dark brown low saddle, a pale strip on the north edge',conf='medium'),
 # ---- M: Gamla torget, the former barracks (sat_s13, sat_s20; Street View gt1, gk1)
 '91970346':dict(boards=False,st=3,f0=.6,height=12.4,top=15.4,roof='saddle',rm='RoofDark',fr='Frame',wall='Yellow',extras=['dormers','chimneys2'],nd=6,
  parts=[[-887.5,-24.0,dict(height=12.4,top=14.0,roof='hip')]],
  name='yellow rendered three-storey former barracks on Gamla torget: the long wing with the dark roof and dormers, the south block with a low roof and iron balconies',
  sat='sat_s20: dark roof with dormers on the long wing, the south block\'s low roof',seen='gt1_h330 (resected), gk1_h150',conf='high (form); measured eaves'),
 # ---- M: Västerlånggatan / Kungsgatan (sat_s12, s22)
 '93292689':dict(GAR,height=3.0,top=4.6,rm='RoofGrey',wall='GreyBoard',name='long garage and store building behind Kungsgatan 5',sat='sat_s12: long grey roof',conf='medium'),
 '93292706':dict(SHED,name='small shed in the back lot west of it',sat='sat_s12: pale roof, small',conf='low'),
 '93292702':dict(SHED,wall='White',name='small shed in the garden east of Västerlånggatan',sat='sat_s22: small pale roof under trees',conf='low'),
 '93306352':dict(boards=True,st=1.5,f0=.4,height=4.0,top=7.0,roof='saddle',rm='TileBrown',fr='Frame',wall='YellowBoard',extras=['chimney'],
  name='back wing behind Västerlånggatan 13A',sat='sat_s22: L-shaped, brown saddle, a darker low part',conf='low'),
 # ---- M: Södra kyrkogården (sat_s14)
 '93293012':dict(boards=False,st=1.5,f0=.5,height=4.0,top=7.8,roof='hip',rm='TileBrown',fr='Frame',wall='WhiteRender',extras=['chimney'],
  name='house at Södra kyrkogården (no. 3)',sat='sat_s14: brown tile hipped roof',conf='medium'),
 '93293025':dict(boards=False,st=1,f0=.3,height=3.2,top=6.2,roof='saddle',rm='Tile',fr='Frame',wall='WhiteRender',extras=['garage_door'],
  name='long service building at Södra kyrkogården',sat='sat_s14: long red tile saddle along the long axis',conf='medium'),
 '93293041':dict(SHED,name='small shed at the cemetery yard, under the trees',sat='sat_s14: mostly hidden by trees',conf='low'),
 # ---- M: Frejagatan / Vegagatan / Kungsgatan courtyards (sat_s15, s16)
 '93325645':dict(GAR,height=3.0,top=4.4,rm='RoofDark',wall='GreyBoard',name='long garage and store building in the courtyard behind Frejagatan',sat='sat_s15: long dark grey roof',conf='medium'),
 '93325656':dict(boards=False,st=2,f0=.4,height=5.8,top=8.4,roof='saddle',rm='TileBrown',fr='Frame',wall='Cream',extras=['chimney'],
  name='courtyard building behind Vegagatan (its pass-98 roof used to overhang pass 139\'s 93325650)',sat='sat_s15: brown saddle on the north-east part, a grey flat part to the south-west',conf='low'),
 '93326718':dict(boards=False,st=1.5,f0=.4,height=4.2,top=7.8,roof='saddle',rm='TileBrown',fr='Frame',wall='Cream',extras=['chimney'],
  name='back house 20C behind Kungsgatan',sat='sat_s16: brown-red tile saddle along the long axis',conf='medium'),
 # ---- E: Molinsgatan (sat_s18)
 '93306356':dict(boards=False,st=1.5,f0=.4,height=3.6,top=6.4,roof='saddle',rm='Tile',fr='Frame',wall='Cream',extras=[],
  name='back house behind Molinsgatan',sat='sat_s18: red tile saddle, half in the shadow of the block',conf='low'),
 # ---- E: Järnvägsgatan / Bremergatan / Västerlånggatan (sat_s17; Street View vl1)
 '93333638':dict(boards=True,st=1.5,f0=.5,height=4.8,top=9.0,roof='saddle',rm='Tile',fr='Frame',wall='YellowBoard',extras=['chimney'],
  name='Café Flädern: yellow boarded one-and-a-half-storey house with a red tile roof and its wings',sat='sat_s17: red tile roofs, the main roof along the long axis with hipped wings',seen='vl1_h340 (over the garden)',conf='high (roof, colour); medium (height)'),
 '93333623':dict(boards=False,st=1,height=3.4,top=3.65,roof='flat',rm='RoofGrey',frm='LightBrick',fr='Frame',wall='WhiteRender',extras=[],
  name='flat-roofed annex beside Café Flädern',sat='sat_s17: pale tan flat roof',conf='medium'),
 '93333658':dict(boards=False,st=2,f0=.5,height=6.0,top=9.4,roof='saddle',rm='Tile',fr='Frame',wall='Yellow',extras=['chimney'],
  name='yellow rendered two-storey house with the red tile roof behind Järnvägsgatan',sat='sat_s17: red tile cross-gabled roof, the yellow walls seen beside it',conf='medium'),
 '93333627':dict(boards=False,st=2,f0=.4,height=5.8,top=8.6,roof='saddle',rm='RoofDark',fr='Frame',wall='GreyWhite',extras=['chimney'],
  name='house 1B with the dark roof behind Bremergatan',sat='sat_s17: dark grey roof',conf='low'),
 '93333660':dict(GAR,height=2.6,top=4.0,rm='RoofDark',name='long garage with the dark roof behind Bremergatan',sat='sat_s17: long dark grey saddle',conf='medium'),
 # ---- E: the courtyard behind Unionsgatan and Smålandsgatan (sat_s19)
 '93453481':dict(boards=False,st=2,f0=.6,height=7.5,top=11.5,roof='hip',rm='TileBrown',fr='Frame',wall='Cream',extras=['chimneys2'],
  name='courtyard house 4C with the brown tile hipped roof',sat='sat_s19: brown tile hipped roof with chimneys, a pale flat terrace roof on the east part',conf='medium (roof); low (height)'),
 '93453490':dict(boards=False,st=2,f0=.6,height=7.5,top=11.5,roof='hip',rm='TileBrown',fr='Frame',wall='Cream',extras=['chimneys2'],
  name='courtyard house with the brown tile cross-hipped roof',sat='sat_s19: brown tile cross-hipped roof',conf='medium (roof); low (height)'),
 '93453516':dict(boards=False,st=2,f0=.6,height=7.5,top=11.5,roof='hip',rm='TileBrown',fr='Frame',wall='Cream',extras=['chimney'],
  name='courtyard house 4D with the brown tile hipped roof (north edge on the model box)',sat='sat_s19: brown tile hipped roof, joined to the Smålandsgatan block',conf='medium (roof); low (height)'),
}
for v in H.values():
 v.setdefault('extras',[]);v.setdefault('seen',None);v.setdefault('f0',0.0)
 # no garage carries both garage_door and no_door (pass 136's fix)
 assert not ('garage_door' in v['extras'] and 'no_door' in v['extras'])
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
# Outlines with many small jogs (bays, porches, the barracks' steps): the rectangles are found on the
# outline simplified by this many metres; the walls still follow the OSM outline.
COARSE={'93329957':1.2,'91970346':1.5,'93333638':1.0}
# pass 98's model box: x >= -1650 and y <= 320; walls on its edges are cut walls (no windows or doors)
def on_box_edge(a,b):return (abs(a[0]+1650)<.05 and abs(b[0]+1650)<.05) or (abs(a[1]-320)<.05 and abs(b[1]-320)<.05)
zones={}
for osm in IDS:
 spec=H[osm]
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
  if k==0:z=dict(height=spec['height'],top=spec['top'],roof=spec['roof'],role='main')
  elif area<12 or w<2.6:
   hh=spec['height'] if spec['st']>=3 else min(spec['height'],3.1)
   z=dict(height=hh,top=hh+.25,roof='flat',role='annex')
  else:
   c0=list(rs[0][1].exterior.coords)[:-1];mw=min(math.dist(c0[i],c0[(i+1)%4]) for i in range(4))
   rf=spec['roof'] if spec['roof'] not in ('flat','mono') else ('flat' if spec['roof']=='flat' else 'saddle')
   if rf=='flat':z=dict(height=spec['height'],top=spec['top'],roof='flat',role='wing')
   else:z=dict(height=spec['height'],top=spec['height']+(spec['top']-spec['height'])*min(1,w/mw),roof=rf,role='wing')
  # a part of the building with its own height and roof (91970346's south block)
  for px_,py_,ov in spec.get('parts',[]):
   if Polygon(cs).contains(Point(px_,py_)):z.update(ov);z['part']=True
  zones[f'{osm}_{k}']=(osm,ps,dict(z,rect=[list(v) for v in cs]))
 rem=OUT[osm].difference(taken)
 for bit in flat(rem):
  if bit.area<.01:continue
  mine=[k for k in zones if zones[k][0]==osm]
  k=max(mine,key=lambda k:Polygon(zones[k][2]['rect']).buffer(.3).intersection(bit).area)
  o_,ps_,sp_=zones[k];zones[k]=(o_,[orient(r) for q in flat(unary_union(ps_+[bit])) for r in flat(q.simplify(.02)) if r.area>.05],sp_)
others=[(Polygon(b['outer']).buffer(0),max(2.6,min(b['height'] or (b['levels']*3.0+.5),28.0)),b['id']) for b in B98 if b['id'] not in IDS]
# the neighbours' heights where a later pass built them (their own eaves, not pass 98's volume)
NB_H={}
for f in sorted((R/'source').glob('block*.json')):
 m_=re.fullmatch(r'block(\d+)\.json',f.name)
 if not m_ or int(m_.group(1))==142:continue
 d_=json.loads(f.read_text())
 if isinstance(d_,dict):
  for z_ in (d_.get('zones') or {}).values():
   if isinstance(z_,dict) and 'osm' in z_ and z_.get('height') and z_.get('role')=='main':NB_H.setdefault(str(z_['osm']),z_['height'])
def neighbour_at(osm,pt):
 for name,(o,ps,spec) in zones.items():
  if o==osm and any(p.buffer(.001).contains(pt) for p in ps):return name,spec['height']
 for name,(o,ps,spec) in zones.items():
  if o!=osm and any(p.buffer(.001).contains(pt) for p in ps):return o,spec['height']
 for g,h,bid in others:
  if g.buffer(.001).contains(pt):return bid,NB_H.get(bid,h-.30)
 return None,0.0
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
 # the door wall: the outer wall nearest a named street that faces it (within 60 m), else the longest
 # outer wall (the buildings in the parks and the cemetery lie further than 60 m from any street)
 faces={}
 for w in walls:
  if w['kind']!='outer' or math.dist(w['p'],w['q'])<1.5:continue
  mid=Point((w['p'][0]+w['q'][0])/2,(w['p'][1]+w['q'][1])/2);L_=math.dist(w['p'],w['q'])
  nx,ny=(w['q'][1]-w['p'][1])/L_,-(w['q'][0]-w['p'][0])/L_
  for nm in SL:
   ln=SL[nm];sp=ln.interpolate(ln.project(mid));dd=mid.distance(sp)
   if dd<.01 or dd>60 or ((sp.x-mid.x)*nx+(sp.y-mid.y)*ny)/dd<.5:continue
   if nm not in faces or dd<faces[nm][0]:faces[nm]=(dd,[w['p'],w['q']])
 best=min(((v[0],k,v[1]) for k,v in faces.items()),default=None)
 if best is None:
  ow=[w for w in walls if w['kind']=='outer' and math.dist(w['p'],w['q'])>=1.5]
  if ow:w_=max(ow,key=lambda w:math.dist(w['p'],w['q']));best=(None,None,[w_['p'],w_['q']])
 spec=dict(spec,street=best[1] if best else None,street_wall=best[2] if best else None,street_m=round(best[0],1) if best and best[0] is not None else None)
 out[name]=dict(spec,osm=osm,mesh='SM_Slott142_'+osm,wall=hs['wall'],boards=hs['boards'],
  polygons=[[list(v) for v in list(p.exterior.coords)[:-1]] for p in ps],walls=walls)
 report[name]={'osm':osm,'role':spec['role'],'roof':spec['roof'],'height':spec['height'],'area_m2':round(sum(p.area for p in ps),1),'walls':len(walls),'outer_m':round(sum(math.dist(w['p'],w['q']) for w in walls if w['kind']=='outer'),1),'door_wall_street':spec['street']}

# ---------------------------------------------------------------- the emptied chunks
# Every building of pass 98's chunks W, M and E is now detailed, so pass 98's code would draw no
# geometry for them. A mesh with no faces cannot be exported (the export tail's calc_tangents needs a UV
# map with loops, and the official build stops) and a missing chunk object would break every earlier
# pass's name list in the rebuild chain. So each chunk keeps one marker: a 0.4 x 0.4 m horizontal quad,
# 0.10 m under the ground (model z 0.20, the ground is 0.30), on open land at least 5 m from any building
# outline. It cannot be seen and draws no building.
STUBS={'W':(-1380.0,-330.0),'M':(-950.0,40.0),'E':(-700.0,40.0)}
landp=unary_union([Polygon(l['outer']).buffer(0) for l in B98ALL['land']])
allp=unary_union([Polygon(b['outer']).buffer(0) for b in B98])
stub_check={k:{'on_land':bool(landp.contains(Point(p))),'clear_of_buildings_m':round(allp.distance(Point(p)),1),'in_model_box':p[0]>=-1650 and p[1]<=320} for k,p in STUBS.items()}
assert all(v['on_land'] and v['clear_of_buildings_m']>=5 and v['in_model_box'] for v in stub_check.values()),stub_check
LEFT={k:sorted(b['id'] for b in B98 if chunk_of(b)==k and b['id'] not in CLAIMED|set(IDS)) for k in 'WME'}

foot=unary_union(list(OUT.values()));covered=unary_union([p for o,ps,s in zones.values() for p in ps])
houses={i:dict(H[i],nearest_street=NEAREST[i][0],nearest_street_m=NEAREST[i][1],chunks=sorted({chunk_of(b) for b in PIECES[i]}),area_m2=round(OUT[i].area,1)) for i in IDS}
clipped={i:'touches pass 98\'s model box (x -1650 or y 320); built on the clipped outline with plain walls on the box edge' for i in IDS
 if any(any(abs(v[0]+1650)<.01 or abs(v[1]-320)<.01 for v in b['outer']) for b in PIECES[i])}
data={'demolished':[],'source':'pass 98 outlines (source/block98.json, from references/osm-slott98.json, OpenStreetMap, ODbL)','ground_z':0.30,'ids':IDS,
 'nearest_streets':NEAREST,'clipped':clipped,'chunk_stubs':STUBS,'left_in_chunks':LEFT,'houses':houses,'zones':out,
 'checks':{'buildings':len(IDS),'by_chunk':{k:sum(1 for i in IDS if chunk_of(BY[i])==k) for k in 'WME'},'footprint_m2':round(foot.area,1),'zoned_m2':round(covered.area,1),
  'outside_osm_m2':round(covered.difference(foot).area,2),'osm_not_zoned_m2':round(foot.difference(covered).area,2),
  'overlap_m2':round(sum(p.area for o,ps,s in zones.values() for p in ps)-covered.area,3),
  'outlines_overlapping_m2':round(sum(OUT[a].intersection(OUT[b]).area for i,a in enumerate(IDS) for b in IDS[i+1:]),3),
  'zones_per_building':{i:sum(1 for o,ps,s in zones.values() if o==i and ps) for i in IDS},
  'cut_walls':sum(1 for z in out.values() for w in z['walls'] if w['kind']=='cut'),'left_in_chunks':{k:len(v) for k,v in LEFT.items()},'stubs':stub_check}}
(R/'source/block142.json').write_text(json.dumps(data,indent=1,ensure_ascii=False))
# pass 134's limits (outside OSM < 0.3 m², not zoned < 0.5 m², overlap within the outlines' own overlap + 0.2 m²)
c=data['checks'];ok=c['outside_osm_m2']<.3 and c['osm_not_zoned_m2']<.5 and c['overlap_m2']<.2+c['outlines_overlapping_m2'] and all(c['zones_per_building'].values()) and not any(LEFT.values())
(R/'previews/block142-zones.json').write_text(json.dumps({'status':'passed' if ok else 'review_required','zones':report,'checks':c},indent=2,ensure_ascii=False))
for k,v in report.items():print(k,v)
print(c);print('BLOCK142_ZONES_OK' if ok else 'BLOCK142_ZONES_REVIEW')
