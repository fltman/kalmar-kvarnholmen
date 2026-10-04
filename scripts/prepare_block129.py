"""Pass 129: Kalmar slott, the courtyard's dormers, doors and portals (corrects passes 27, 124, 127).

Measured on the 2014 Street View courtyard panoramas (viewed only, no pixel used or saved) from the
cameras pass 128 resected (pano 1 zCIfieeXGQUNANmWu_Tg9A at (-885.06, -306.46), heading offset -1.34;
pano 2 jOXzkLldNOjrveyz1T81wg at (-860.06, -308.67), heading offset -2.65), and checked on the 2017
and 2022 courtyard photographs. See references/block129-notes.md for the readings.

- Dormers: pass 27/127 had four red-fronted dormers (SE_w, NE, NW, SW). The panoramas show one
  red-fronted gabled dormer, on SE_e beside the SE_w/SE_e bend, and three small grey ones: a louvred
  vent on NE, a shed dormer on SW (where pass 27's red one stood) and a long low shed dormer on NW
  south of Kuretornet. SE_w has none.
- Doors: NE has no door at courtyard level (pass 27's two middle doors go); the aedicule portal D
  stands 6.1-6.9 m from the east corner on a 3-step stair. SE_w has two small arched doors (pass 27's
  one middle door goes), SE_e a wide arched door 2 m from the bend. SE_e's 9-step stair stands at
  about 58 % of the front from the east corner (pass 127: 2.5 m from it).
- Portal C (NW, the gate passage's courtyard portal): two storeys of paired columns 4.95 m wide and
  6.69 m high (top z 12.16), the relief panel in the upper storey, a flat cornice; its arch 2.6 m
  wide and 3.25 m high.
- Camera 690 (the 2022 well photograph) resected anew: it looks at the EAST corner (NE left with
  portal D, SE_e right with its stair and the red dormer, the east tower's cap at the upper left).
Output: source/block129.json and previews/block129-zones.json.
Run: KALMAR_GEO=<pylib with shapely> python3 scripts/prepare_block129.py
"""
from pathlib import Path
import json,math,os,sys
if os.environ.get('KALMAR_GEO'):sys.path.insert(0,os.environ['KALMAR_GEO'])
from shapely.geometry import Polygon,Point
R=Path(__file__).resolve().parents[1]
C27=json.loads((R/'source/castle27.json').read_text());CA=C27['castle']
B126=json.loads((R/'source/block126.json').read_text());B127=json.loads((R/'source/block127.json').read_text());B128=json.loads((R/'source/block128.json').read_text())
ZC=B126['zc'];ZCE=B127['zce']
CI=[tuple(p) for p in CA['court']]
RANGES={r['name']:dict(r) for r in CA['ranges']}
PIECE={pc['key']:(pc['plane'],[Polygon(rr[0],rr[1:]) for rr in pc['rings']]) for pc in B127['roof']}
def rp(r,s,c):o=r['origin'];return (o[0]+r['u'][0]*s+r['n'][0]*c,o[1]+r['u'][1]*s+r['n'][1]*c)
def zpl(pl,p):return pl[0]*p[0]+pl[1]*p[1]+pl[2]

# ---------------------------------------------------------------- dormers
# (id, range, s along the range frame, metres up the courtyard slope from the eaves line to the front,
#  kind, front width, front height to the cheek top, gable rise, window w/h, source, status)
DORM=[('SEe_red','SE_e',3.3,.3,'gable',2.1,2.9,1.1,(1.3,1.3),'pano 1 (98, 140), pano 2 (150), 2017 and 2022 photographs','measured'),
      ('NE_vent','NE',15.2,3.0,'shed',.8,.8,0,(.5,.5),'pano 1 (40, 98)','measured (one camera)'),
      ('SW_shed','SW',17.6,1.6,'shed',1.2,1.3,0,(.7,.6),'pano 2 (235), 2017 photograph','measured (one camera)'),
      ('NW_shed','NW',46.0,3.0,'shed',2.4,.75,0,(1.8,.4),'pano 2 (235, 300)','measured (one camera, +-2 m along)')]
SHED=.27                     # the shed dormers' roofs, about 15 degrees
dormers=[];zones={}
for did,rn,s,up,kind,W,hf,gh,(ww,wh),src,status in DORM:
 pl,polys=PIECE[rn+'_in'];sli=math.hypot(pl[0],pl[1]);m=(pl[0]/sli,pl[1]/sli)      # uphill, horizontal
 r=RANGES[rn];P0=rp(r,s,r['inner']);k=(ZCE-zpl(pl,P0))/sli;E=(P0[0]+m[0]*k,P0[1]+m[1]*k)   # on the eaves line
 e=(-m[1],m[0]);F=(E[0]+m[0]*up,E[1]+m[1]*up);zf=ZCE+sli*up                      # front foot on the roof
 top=hf+gh;L=(top+.3)/sli if kind=='gable' else hf/(sli-SHED)                     # how far back the body runs
 foot=[(F[0]+e[0]*a+m[0]*b,F[1]+e[1]*a+m[1]*b) for a in (-W/2,W/2) for b in (0,L)]
 inside=[any(q.buffer(-.05).contains(Point(p)) for q in polys) for p in foot]
 assert all(inside),('dormer not on its own slope',did,inside)
 for c in B128['chimneys']:
  assert min(math.dist((c['x'],c['y']),p) for p in foot+[F])>1.0,('dormer meets a chimney',did,c['id'])
 dormers.append(dict(id=did,range=rn,s=s,up=up,kind=kind,x=round(F[0],4),y=round(F[1],4),z=round(zf,4),m=[round(v,6) for v in m],sli=round(sli,6),
  w=W,hf=hf,gh=gh,win=[ww,wh],depth=round(L,3),shed=SHED,source=src,status=status))
 zones[did]=dict(range=rn,s=s,up=up,kind=kind,front_foot_z=round(zf,2),top_z=round(zf+top,2))
for i in range(len(dormers)):
 for j in range(i+1,len(dormers)):assert math.dist((dormers[i]['x'],dormers[i]['y']),(dormers[j]['x'],dormers[j]['y']))>5

# ---------------------------------------------------------------- doors at courtyard level
# Per courtyard edge (CI indices in the order pass 27 builds the fronts: p -> q, u from the edge's
# middle, increasing towards q): (u, sill z, width, height to the springing, arch rise).
def edge(i,j):return math.dist(CI[i],CI[j])
RISE_D=3*.163                # portal D's three steps (pano 2: 3 risers, 0.49 m)
UD=round(edge(7,6)/2-.955,3)  # portal D: as close to the east corner as the edge allows (6.9 m from it; measured 6.0-6.2 / fraction 0.80)
DOORS={
 '8,7':[],                                                         # NE north part: pass 27's middle door goes (pano 1: windows there)
 '7,6':[[UD,round(ZC+RISE_D,3),1.4,1.9,.7]],                       # portal D's arched door, raised on its stair
 '3,2':[[round(-edge(3,2)/2+2.32,3),ZC,.95,1.72,.475],[round(-edge(3,2)/2+10.07,3),ZC,.95,1.72,.475]],   # SE_w's two small arched doors (12 % and 53 %)
 '4,3':[[round(edge(4,3)/2-2.0,3),ZC,1.5,1.5,.5]],                 # SE_e's wide arched door, 2.0 m from the bend
}
ARCHUP=[tuple(h) for h in DOORS['7,6']]
for k,hs in DOORS.items():
 i,j=map(int,k.split(','));L=edge(i,j)
 for u,b,w,h,r_ in hs:assert abs(u)+w/2+.25<=L/2+1e-6,(k,u,w,L)
# ---------------------------------------------------------------- outside stairs
# NE's 7-step stair is pass 127's. SE_e's 9-step stair moves to its measured place (pano 1: 54 %,
# pano 2: 58 % of the front from the east corner; set at 59.6 %, the nearest place that keeps the stair on
# one edge). Portal D's stair: 3 risers of 0.163 m, a landing for the portal's pedestals.
st_ne=dict(B127['stairs'][0]);assert st_ne['edge']==[8,7]
st_se=dict(B127['stairs'][1]);assert st_se['edge']==[5,4]
L43=edge(4,3);st_se.update(edge=[4,3],u=round(-L43/2+1.0+.3,3))
st_d=dict(edge=[7,6],u=UD,risers=3,rise=.163,tread=.32,width=3.0,landing=.75,w=1.4,h=1.9,door='arch')
STAIRS=[st_ne,st_se,st_d]
for st in STAIRS:
 L_=edge(*st['edge'])
 if st.get('door')=='arch':assert L_/2-st['u']+edge(6,5)>st['width']/2+1.0,st      # NE is straight through CI6 (edges 7-6 and 6-5 collinear)
 else:assert abs(st['u'])+st['width']/2+.3<L_/2+.2,st
 st.update(p=list(CI[st['edge'][0]]),q=list(CI[st['edge'][1]]),sill=round(ZC+st['risers']*st['rise'],3))
fd=Polygon(CI).buffer(-.355,join_style=2)
def from_corner(i,j,u,corner):
 # distance along the edge's line from CI[corner] to the point u on edge i->j
 p,q=CI[i],CI[j];L=edge(i,j);t=.5+u/L;P=(p[0]+(q[0]-p[0])*t,p[1]+(q[1]-p[1])*t);return round(math.dist(P,CI[corner]),2)
# ---------------------------------------------------------------- portal C (relief portal, NW)
# Pano 2 at 300 degrees, 75y, 108t, scaled between the courtyard (z 5.47) and the eaves (17.01) on the
# front (x 1.064): total 6.69 m high, 4.95 m wide; lower order on pedestals 1.02 m, entablature
# 3.44-4.19, the upper order 4.30-6.15 with the relief panel 4.30-5.71, the top cornice 6.15-6.69;
# the arch 2.6 m wide with its crown at 3.22-3.25 m.
PC=dict(width=4.95,ped=1.02,col1=(1.02,3.44),ent1=(3.44,4.19),base2=(4.19,4.30),col2=(4.30,6.15),panel=(4.30,5.71),ent2=(6.15,6.69),
 pairs=(1.68,2.18),r1=.16,r2=.13,open_w=2.6,open_h=1.95,open_r=1.3)
# ---------------------------------------------------------------- portal D (aedicule, NE)
# Pano 1 at 40 degrees (60y, 92t) and pano 2 at 60 degrees (75y, 95t), scaled 0.954 between the
# courtyard and the eaves: 2.66 m wide, 4.62 m high from the courtyard, the stair 0.49 m, the door
# 1.49 m wide with its arch crown 2.61 m above the landing; banded columns, a segmental cap.
PD=dict(edge=[7,6],u=UD,rise=round(RISE_D,3),width=2.66,cols=1.05,ped=(0,.35),col=(.35,2.95),ent=(2.95,3.6),cap=(3.6,4.13),cap_w=1.7,
 from_east_corner=from_corner(7,6,UD,5),from_north_corner=from_corner(7,6,UD,8))
# ---------------------------------------------------------------- camera 690 (2022 well photograph)
# Resected on portal D, the well, SE_e's stair door and the red dormer (bearings, f 1925 px for the
# phone's 26 mm lens on the 1920 px short side): (-878.55, -309.10), heading 81.5; residuals 0.1-3.4
# degrees. Pitch 12.4 from the well's foot (9.1 m away at the 4.6 m base width). The cap at the upper left
# is the east tower's (it projects 43 px from where the photograph has it).
CAM690=dict(x=-878.55,y=-309.10,h=1.6,heading=81.5,pitch=12.4,vfov=round(2*math.degrees(math.atan(1280/1925)),2))

out=dict(source='pass 129: Street View 2014 courtyard panoramas (viewed only), 2017/2022 photographs; see references/block129-notes.md',
 zc=ZC,zce=ZCE,dormers=dormers,doors=DOORS,archup=ARCHUP,stairs=STAIRS,portal_c=PC,portal_d=PD,camera690=CAM690,
 checks=dict(dormers=len(dormers),doors={k:len(v) for k,v in DOORS.items()},stairs=len(STAIRS),
  portal_d_from_east_corner=PD['from_east_corner'],portal_d_from_north_corner=PD['from_north_corner'],
  sew_doors_from_bend=[from_corner(3,2,h[0],3) for h in DOORS['3,2']],see_door_from_bend=from_corner(4,3,DOORS['4,3'][0][0],3),
  see_stair_from_east_corner=from_corner(4,3,st_se['u'],5)))
(R/'source/block129.json').write_text(json.dumps(out,indent=1,ensure_ascii=False))
(R/'previews/block129-zones.json').write_text(json.dumps(dict(dormers=zones,doors=DOORS,stairs=[dict(edge=s['edge'],u=s['u'],risers=s['risers']) for s in STAIRS],checks=out['checks']),indent=1))
print(json.dumps(out['checks']))
print('BLOCK129_PREPARE_OK')
