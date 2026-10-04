"""Pass 139: the mainland street houses around Järnvägsgatan and Tullslätten and their small side
streets (Odengatan, Frejagatan, Tullbron, Unionsgatan and the Järnvägsgatan end of Södra vägen). Pass 98
built these houses as plain volumes inside its chunk meshes M and E (source/block98.json, OSM, ODbL).
The housing: on Järnvägsgatan the long yellow 1920s block over a basement with the brown tile mansard
roof, round-topped dormers, pilasters and stone portals (no. 3), the dark brown boarded villa with the
steep tile roof and dormers (no. 9), the tall white rendered house with the black mansard roof and the
yellow house behind the hedge (no. 7); Frasses, the grey boarded kiosk with the roof lantern on Södra
vägen; on Odengatan the dark brown boarded gambrel villa (no. 1), the pale pink house with the wall gable
(no. 7) and the cream Jugend apartment block with iron balconies; on Frejagatan the white Jugend corner
block with the red tile roof, the cream 1910s block with the curved gable and the grey sheet roof, the
brown rendered block (no. 5) and the yellow brick block (no. 8); at Tullbron the yellow house with the
dark mansard roof; at Tullslätten the red brick Tullbroskolan with its stepped gables and the white
flat-roofed school building; on Unionsgatan the red boarded gymnasium with the clerestory.
Selection: every pass-98 outline within 25 m of one of the pass's streets (the OSM street lines in
references/osm-slott98.json) whose nearest named street is one of them, leaving out every id claimed in
source/block*.json of passes below 139 (pass 138 included) and the Stagnell chapel (pass 107). Outlines
within 25 m that are nearer another street are listed in 'left_to_other_streets'. Pass 98's mainland
chunks are W (x < -1150), M and E; these houses lie in M and E, pass 138's in W.
Each outline is split into rectangular zones for its roofs with pass 116's slab method (as copied by
passes 134 and 136); 93333631 has an explicit split (the higher main part and the lower east section).
Heights in metres above the ground (pass 98 lays the ground at model z 0.30). Measured values are read
on the OSM wall planes from the Google pano positions with an assumed 2.5 m camera (SCR captures
'139|'); the rest is estimated from storeys, doors and windows. See references/block139-notes.md.
"""
from pathlib import Path
import json,math,os,sys,re
if os.environ.get('KALMAR_GEO'):sys.path.insert(0,os.environ['KALMAR_GEO'])
from shapely.geometry import Polygon,Point,LineString
from shapely.geometry.polygon import orient
from shapely.ops import unary_union
R=Path(__file__).resolve().parents[1]
B98=json.loads((R/'source/block98.json').read_text())['buildings'];BY={b['id']:b for b in B98}
OSM=json.loads((R/'references/osm-slott98.json').read_text())
EARLIER={'500979084'}  # pass 107
for f in sorted((R/'source').glob('block*.json')):
 m_=re.fullmatch(r'block(\d+)\.json',f.name)
 if not m_ or int(m_.group(1))>=139:continue
 d_=json.loads(f.read_text())
 if isinstance(d_,dict):EARLIER|=set(map(str,d_.get('ids',[])))|set(map(str,d_.get('demolished',[])))

# ---------------------------------------------------------------- selection
# Södra vägen is in the list for its stretch at the north end of Järnvägsgatan: the one unclaimed outline
# nearest it (Frasses, 93309088) stands at the crossing; every other Södra vägen house is claimed already.
MINE=('Järnvägsgatan','Tullslätten','Tullbron','Unionsgatan','Odengatan','Frejagatan','Södra vägen')
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
# hip, gambrel, mhip (hipped mansard) or flat; ridge: 'street' (ridge parallel to the street wall) or the
# default (along the long side of the main rectangle); rm: roof material; fr: window frame colour; seen:
# the photo the values are read from (None = not seen; estimated); measured: what was measured; extras:
# features drawn in the build; gable_w/gable_top: width and apex (above the ground) of a central gable on
# the street front ('gable_mid'); rest: the values of the second part of an explicitly split outline.
JUG=dict(boards=False,st=4,f0=1.0,height=14.2,top=17.6,roof='saddle',rm='Tile',fr='Frame')   # the 1900s-1910s apartment blocks
H={
 # ---- Järnvägsgatan (the south-west side, south-east to north-west)
 '93333646':dict(name='long yellow rendered two-storey 1920s block over a basement with the brown tile mansard roof, round-topped dormers, white pilasters and the stone door portals (Järnvägsgatan 3)',
  wall='Yellow',boards=False,st=2,f0=1.1,height=8.0,top=12.0,roof='mhip',rm='TileDark',fr='Frame',ridge='street',
  seen='jv4_h159, jv5_h236',measured='base at z 0.65, eaves 8.7 on the street front at the north-west corner, so 8.1 above the base (jv4_h159, pano position, camera 2.5 assumed)',
  extras=['dormers','pilasters','portals','chimneys2']),
 '93333654':dict(name='yellow rendered two-storey house with a red tile roof and the gable dormer, behind the hedge (Järnvägsgatan 7)',wall='Yellow',boards=False,st=2,height=7.0,top=10.6,roof='saddle',rm='Tile',fr='Frame',ridge='street',
  seen='jv3_h197 (behind the hedge)',measured='eaves read at 8.8 on the OSM front plane from the pano position (the base is hidden; not trusted, 7.0 used from the storeys)',extras=['dormers','chimney']),
 '93333649':dict(name='small dark brown boarded annex behind the villa (seen only as an overlap in jv1_h197)',wall='BrownBoard',boards=True,st=1,height=2.6,top=4.0,roof='saddle',rm='TileBrown',fr='Frame',seen=None,extras=['no_door']),
 '93333631':dict(name='dark brown boarded villa with the steep brown tile roof, dormers and two red brick chimneys; the lower east section with its own roof; the gabled entrance porch (Järnvägsgatan 9)',
  wall='BrownBoard',boards=True,st=1.5,f0=.3,height=4.7,top=10.6,roof='saddle',rm='TileDark',fr='Frame',
  seen='jv1_h197 (resected)',measured='camera resected on the two front corners to (-793.19, 231.48), 2.31 m above the ground from the base; eaves 4.6 above the ground, the ridge read at 8.9 on the front plane, carried back 4.25 m to about 10.4; the east section about 0.9 m lower (read from the pano position)',
  extras=['dormers','chimneys2','porch'],
  rest=dict(height=3.9,top=9.6,roof='saddle')),
 '93333642':dict(name='white rendered two-storey house with tall storeys, the black tile mansard roof and two dormers, behind the hedge on the stone wall',wall='WhiteRender',boards=False,st=2,f0=.9,height=8.6,top=12.2,roof='mhip',rm='RoofDark',fr='Frame',
  seen='jv2_h197',measured='eaves read at 9.1 on the OSM front plane above the street (pano position, camera 2.5 assumed; the base is behind the hedge), 8.6 used; the roof top seen at 12.0 on the front plane',extras=['dormers2','chimney']),
 # ---- Södra vägen at Järnvägsgatan
 '93309088':dict(name='Frasses: grey boarded one-storey kiosk with a low hipped roof, the raised roof lantern and the blue sign',wall='GreyBoard',boards=True,st=1,height=3.0,top=4.4,roof='hip',rm='RoofDark',fr='Frame',
  seen='sv1_h181 (June 2025)',extras=['lantern']),
 # ---- Odengatan
 '93333637':dict(name='dark brown boarded one-and-a-half-storey gambrel villa with the brown tile roof, the cross gable and the glazed veranda (Odengatan 1)',wall='BrownBoard',boards=True,st=1.5,f0=.5,height=3.6,top=8.4,roof='gambrel',rm='TileDark',fr='Frame',
  seen='od1_h124',measured='eaves 4.3 (3.4 above the base at 0.9) and the roof read at 7.0 on the front plane (pano position, camera 2.5 assumed)',extras=['chimneys2']),
 '93309101':dict(name='pale pink rendered one-and-a-half-storey house with the red tile hipped mansard roof and the wall gable on the street (Odengatan 7)',wall='Pink',boards=False,st=1.5,f0=.6,height=4.8,top=10.8,roof='mhip',rm='Tile',fr='FrameDark',
  seen='od2_h124 (resected)',measured='camera resected on the two front corners to (-947.90, 207.48), 2.3 m from the pano position; with a 2.5 m camera the base reads 0.58 (behind the fence), the eaves 5.46 and the wall gable apex 11.98, so about 4.9 and 11.4 above the base; 4.8 and 10.8 used (the pano-position reading gave 4.4 and 10.2)',
  extras=['gable_mid'],gable_w=6.2,gable_top=10.8),
 '93309089':dict(name='small white garage with a red tile roof in front of the white house',wall='WhiteRender',boards=False,st=1,height=2.5,top=4.0,roof='saddle',rm='Tile',fr='Frame',seen='od7_h188 (behind the hedge)',extras=['garage_door']),
 '93325628':dict(JUG,name='cream rendered four-storey Jugend apartment block over a grey stone basement with the iron balconies; white with red window frames at the Vegagatan end (in scaffolding in 2025)',wall='Cream',
  seen='od6_h219, od3_h346, od4_h263, od5_h21 (close, scaffolding)',extras=['balconies','chimneys2']),
 # ---- Frejagatan
 '93325650':dict(JUG,name='white rendered four-storey Jugend corner block with the red tile roof, the rounded corner bays and the iron balconies (Frejagatan 4)',wall='WhiteRender',
  seen='fj7_h26, fj1_h162, fj2_h83',measured='base at z 0.38, eaves 14.6 (14.2 above it) near the west corner (fj7_h26, pano position, camera 2.5 assumed)',extras=['balconies','chimneys2']),
 '93326740':dict(JUG,name='cream rendered four-storey 1910s apartment block with arched windows, the curved central gable over the stone portal and the grey sheet hipped roof (Frejagatan 3)',wall='Cream',
  height=14.4,top=17.2,roof='hip',rm='RoofGrey',
  seen='fj3_h302, fj7_h26',measured='base at z 0.42, eaves 14.8 (14.4 above it) and the gable apex 19.3 on the west front plane (fj7_h26, pano position, camera 2.5 assumed)',
  extras=['gable_mid','chimneys2'],gable_w=9.0,gable_top=18.6),
 '93291993':dict(name='brown-beige rendered four-storey block with the shop windows on the ground floor and a low dark roof (Frejagatan 5)',wall='Ochre',boards=False,st=4,height=12.4,top=13.8,roof='saddle',rm='RoofDark',fr='Frame',
  seen='fj4_h123 (close), fj7_h26 (right edge)',extras=['shopfront']),
 '93326744':dict(name='yellow brick three-storey block over a basement with a low roof and the two entrances (Frejagatan 8)',wall='YellowBrick',boards=False,st=3,f0=.9,height=10.0,top=11.8,roof='saddle',rm='RoofRed',fr='Frame',
  seen='fj5_h303'),
 # ---- Tullbron
 '91933165':dict(name='yellow rendered two-storey house with the dark mansard roof and dormers at Tullbron',wall='Yellow',boards=False,st=2,f0=.4,height=7.0,top=10.6,roof='mhip',rm='RoofDark',fr='Frame',
  seen='tb3_h8 (across the railway, about 50 m), tb4_h290'),
 '91933162':dict(name='yellow rendered two-storey house with a red tile roof behind the trees at Tullbron (seen only far)',wall='Yellow',boards=False,st=2,height=6.4,top=9.4,roof='hip',rm='Tile',fr='Frame',seen='tb3_h8 (far, behind the buses)'),
 # ---- Tullslätten
 '91222178':dict(name='Tullbroskolan: red brick three-storey 1880s school with the stepped gables, arched windows and brick friezes',wall='RedBrick',boards=False,st=3,f0=.6,height=11.5,top=15.5,roof='saddle',rm='RoofDark',fr='Frame',
  seen='ts1_h307, ts5_h48, ts6_h83',measured='eaves about 9-11 above the base, inconsistent between columns (grazing view, pano position not resected; the yard lies lower than the street); 11.5 used from the three tall storeys',
  extras=['stepped_gables','chimney']),
 '91222193':dict(name='white rendered flat-roofed two-storey school building behind Tullbroskolan (the school yard was a building site in 2025)',wall='WhiteRender',boards=False,st=2,height=7.2,top=7.45,roof='flat',rm='RoofDark',fr='FrameDark',seen='ts3_h11 (behind the site fence)'),
 # ---- Unionsgatan
 '93252919':dict(name='red boarded gymnasium with the big white windows, the buttresses, the pent roof over the lower hall wall, the clerestory and the tall brick chimney',wall='RedBoard',boards=True,st=1,height=9.2,top=11.4,roof='saddle',rm='RoofDark',fr='Frame',
  seen='un1_h164 (close)',measured='base at z -0.25, the pent roof at 6.4-6.5, the clerestory window tops at 8.7-9.1, the chimney top at 12.4-12.9 (pano position, camera 2.5 assumed); so the pent 6.6 and the eaves 9.2 above the base',
  extras=['hall','tall_chimney']),
}
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
# Explicit split, read on jv1_h197: 93333631's street front runs from vertex 0 (south-east) to vertex 1
# (15.3 m). The higher main part with the steep roof and the dormers covers the first 10.2 m; the lower
# east section with its own roof the rest. Both ridges run along the street.
SPLIT={'93333631':(V('93333631',0),V('93333631',1),10.2)}
# Tullbroskolan (91222178) is an H in plan: the north wing (vertices 0-3 and 10-11), the middle body and the
# south wing (vertices 4-9), cut across the frame from vertex 1 to vertex 2 at 12.14 m and 34.8 m (the
# vertices' own positions are 12.04-12.24 and 34.41-35.17). The slab method gives one box over the whole H.
CUTS={'91222178':(V('91222178',1),V('91222178',2),[-1.0,12.14,34.8,48.0])}
CUTS_LONG={'91222178':(V('91222178',0),V('91222178',1))}
# The gymnasium (93252919) is one hall under one roof (un1_h164): its 2.3 m jogs on the north front are
# small porches and steps, and the slab method's flat 3.1 m annex along that front hid the hall wall in the
# first sandbox comparison. One box, the ridge along the long side (vertex 0 to 1).
ONEBOX={'93252919':(V('93252919',0),V('93252919',1))}
zones={}
for osm in IDS:
 spec=H[osm]
 if osm in SPLIT:
  a_,b_,s_=SPLIT[osm]
  west=OUT[osm].intersection(strip(a_,b_,-1,s_,OUT[osm]))
  rs=[('main',orient(box_in(west,a_,b_)))]
  for bit in flat(OUT[osm].difference(rs[0][1])):
   if bit.area>3:rs.append(('rest',orient(box_in(bit,a_,b_))))
 elif osm in ONEBOX:
  # one box over the whole outline, ridge along a->b
  rs=[('main',orient(box_in(OUT[osm],*ONEBOX[osm])))]
 elif osm in CUTS:
  # an H-shaped plan in three parts across the frame a->b: each part boxed with its ridge along its
  # long side
  a_,b_,cuts=CUTS[osm];rs=[]
  for s0,s1 in zip(cuts,cuts[1:]):
   piece=OUT[osm].intersection(strip(a_,b_,s0,s1,OUT[osm]))
   c0=box_in(piece,a_,b_);e=list(c0.exterior.coords)
   rect=c0 if math.dist(e[0],e[1])>=math.dist(e[1],e[2]) else box_in(piece,CUTS_LONG[osm][0],CUTS_LONG[osm][1])
   rs.append(('main',orient(rect)))
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
# the streets a door may face: the pass's streets, and the side streets of the corner houses
DOORST=MINE+('Bremergatan','Vegagatan','Olof Palmes gata','Jenny Nyströms gränd','Esplanaden','Stationsgatan')
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
 out[name]=dict(spec,osm=osm,mesh='SM_Slott139_'+osm,wall=spec.get('wall',hs['wall']),boards=spec.get('boards',hs['boards']),brick=False,
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
(R/'source/block139.json').write_text(json.dumps(data,indent=1,ensure_ascii=False))
# pass 134's limits (outside OSM < 0.3 m², not zoned < 0.5 m², overlap within the outlines' own overlap + 0.2 m²)
c=data['checks'];ok=c['outside_osm_m2']<.3 and c['osm_not_zoned_m2']<.5 and c['overlap_m2']<.2+c['outlines_overlapping_m2'] and all(c['zones_per_building'].values())
(R/'previews/block139-zones.json').write_text(json.dumps({'status':'passed' if ok else 'review_required','zones':report,'checks':c},indent=2,ensure_ascii=False))
for k,v in report.items():print(k,v)
print(c);print('BLOCK139_ZONES_OK' if ok else 'BLOCK139_ZONES_REVIEW')
