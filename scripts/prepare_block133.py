"""Pass 133: Kalmar slott, Kyrkportalen (portal F) at its true place and the way up to Slottskyrkan.

Portal F (Kyrkportalen, 1568; Olsson, Fornvännen 1957, p. 138 and fig. 10) is "the eastern" of the
south range's two courtyard portals: two fluted Doric columns on each side of the round-arched door,
an entablature with triglyphs and plain metopes, four herms (male and female) on Ionic capitals
carrying a second entablature, a cartouche with Johan III's crowned initials and 1568 between the
herms, and on top a segmental tablet with the arms held by two lions. Pass 124 put it at the middle
of the SW courtyard front (s 17.9); pass 129 found it 3-3.5 m from the south corner.

Readings (no pixel of any panorama or photograph is used or kept):
- Street View 2014, pano 2 (jOXzkLldNOjrveyz1T81wg, pass 128's resected camera), URL 207h 40y 95t,
  viewed on a 1400 x 806 screen: SW is seen almost square on (the rays meet the front at 76-80 deg).
- Street View 2014, pano 1 (zCIfieeXGQUNANmWu_Tg9A), URL 162h 60y 95t: a grazing view (26-35 deg).
- Commons 2017 courtyard photograph (PD), pass 127's resected camera 689 (f 1890 px, heading 174.9).
Each reading is a ray intersected with the SW courtyard face; positions are taken from the south
corner measured in the same view.

Route to the chapel. The state-floor plan of Kalmar läns museum ('Kalmar slott, plan över
praktvåningen', KLMF.Slott003-57, viewed) numbers '13. Sydöstra vindelstenen' as a narrow stair hall
immediately beyond the chapel's altar wall (12), running across the range from the courtyard side to
the outer wall, with its treads drawn on the courtyard half and a door into the chapel by the altar at
the outer side; the c. 1780 chapel plan (Krigsarkivet 0424:058:212a) has that door (pass 130's altar
door, c -2.00) and the west door, and no door in the courtyard wall. Olsson's 1574 plan (Fv 69, 1974,
fig. 1; in copyright, read only) shows a passage in the cross wall at the same place. Kyrkportalen
stands 2.4-3.5 m from the south corner, i.e. at the courtyard foot of that stair. The ground-floor
link from the portal to the stair is not drawn in any open source: it is built as the simplest
plausible one, a vestibule and a flight along the courtyard wall under the chancel into the stair hall,
a half landing and a second flight across the range (as the museum plan draws the treads) to a landing
at the altar door, at the chancel's level (z 10.75).

Output: source/block133.json, previews/block133-zones.json.
Run with Shapely: KALMAR_GEO=<site-packages> python3 scripts/prepare_block133.py
"""
from pathlib import Path
import json,math,os,sys
if os.environ.get('KALMAR_GEO'):sys.path.insert(0,os.environ['KALMAR_GEO'])
from shapely.geometry import Polygon,Point,box
from shapely.ops import unary_union
R=Path(__file__).resolve().parents[1]
C27=json.loads((R/'source/castle27.json').read_text());CA=C27['castle']
B125=json.loads((R/'source/block125.json').read_text());B126=json.loads((R/'source/block126.json').read_text())
B127=json.loads((R/'source/block127.json').read_text());B129=json.loads((R/'source/block129.json').read_text())
B130=json.loads((R/'source/block130.json').read_text());B131=json.loads((R/'source/block131.json').read_text())
RG={r['name']:r for r in CA['ranges']}['SW'];O,U,N=RG['origin'],RG['u'],RG['n']
def W(s,c):return (O[0]+U[0]*s+N[0]*c,O[1]+U[1]*s+N[1]*c)
def F(p):dx,dy=p[0]-O[0],p[1]-O[1];return (dx*U[0]+dy*U[1],dx*N[0]+dy*N[1])
def rnd(p,k=4):return [round(v,k) for v in p]
def ring(poly):
 # The outer ring, counter-clockwise, without near-collinear points or slivers (the town bevel stops
 # on the whole mesh at one bad vertex; pass 131).
 g=poly.simplify(.002,preserve_topology=True)
 g=Polygon(g.exterior.coords) if g.exterior.is_ccw else Polygon(list(g.exterior.coords)[::-1])
 return [rnd(p) for p in list(g.exterior.coords)[:-1]]
def SB(s0,s1,c0,c1):return Polygon([W(s0,c0),W(s1,c0),W(s1,c1),W(s0,c1)])
ZC=B127['zc'];FL=B130['levels']['floor'];ZCH=round(FL+B130['chancel']['risers']*B130['chancel']['rise'],3)
CI=[tuple(p) for p in CA['court']]
S_CORNER=F(CI[2])[0];S_WCORNER=F(CI[0])[0]          # the south and west courtyard corners on SW (27.84, 6.07)
C_LINE=-9.371                                         # the SW courtyard line by the south corner

# ---------------------------------------------------------------- readings
def hit(cam,bear,c0):
 # A horizontal ray from cam at model bearing 'bear', intersected with the face c = c0 of the SW range.
 d=(math.sin(math.radians(bear)),math.cos(math.radians(bear)));s0,cc=F(cam)
 ds=d[0]*U[0]+d[1]*U[1];dc=d[0]*N[0]+d[1]*N[1];t=(c0-cc)/dc;return s0+ds*t,t
FACE=C_LINE-.355                                      # the portal stands on pass 27's wall face
def reading(cam,head_true,W_,H_,vfov,xs):
 f=(H_/2)/math.tan(math.radians(vfov/2));out={}
 for k,x in xs.items():
  b=head_true+28.2+math.degrees(math.atan((x-W_/2)/f));s,t=hit(cam,b,C_LINE if k=='corner' else FACE);out[k]=dict(px=x,bearing=round(b,2),s=round(s,2),dist=round(t,1))
 return out
P2=reading((-860.06,-308.67),207-2.65,1400,806,40,dict(corner=582,left=590,right=733,door_l=640,door_r=686,window=656.5))
P1=reading((-885.06,-306.46),162-1.34,1400,806,60,dict(corner=595,left=618,right=703,door_l=645,door_r=672))
PH=reading((-861.1,-292.66),174.9,1920,1309,2*math.degrees(math.atan(1309/2/1890)),dict(corner=1197.7,left=1225,right=1413,tablet_l=1278.3,tablet_r=1363.3,window=1307))
def summary(r):
 c=r['corner']['s'];door=(r['door_l']['s']+r['door_r']['s'])/2 if 'door_l' in r else (r['left']['s']+r['right']['s'])/2
 return dict(corner_s=c,axis_from_corner=round(c-door,2),width=round(abs(r['left']['s']-r['right']['s']),2),edge_from_corner=round(c-r['left']['s'],2))
READ=dict(pano2=dict(view='URL 207h 40y 95t, 1400x806, rays 76-80 deg to the front',rays=P2,**summary(P2)),
 pano1=dict(view='URL 162h 60y 95t, 1400x806, grazing 26-35 deg',rays=P1,**summary(P1)),
 photo2017=dict(view='Commons 2017, camera 689 (f 1890 px), rays 57-62 deg',rays=PH,**summary(PH)))
READ['photo2017']['axis_from_corner']=round(PH['corner']['s']-(PH['left']['s']+PH['right']['s'])/2,2)
# Heights on pano 2 (pitch +5, f 1107 px, 33.2 m to the face, camera ZC+1.9), scaled per front between
# the courtyard (row 576 -> 5.12) and the courtyard eaves (row 172 -> 17.39, true 17.01), as pass 129.
def zrow(y):return ZC+1.9+33.2*math.tan(math.radians(5)+math.atan((403-y)/1107.2))
_z0,_z1=zrow(576),zrow(172);_k=(B127['zce']-ZC)/(_z1-_z0)
ROWS=dict(pedestal_top=555,column_top=490,lower_entablature_top=472.5,upper_cornice_bottom=425,upper_cornice_top=419,tablet_top=400,door_crown=499,door_springing=523.5,window_bottom=399,window_top=375)
HEIGHTS={k:round((zrow(y)-_z0)*_k,2) for k,y in ROWS.items()}
WIDTHS=dict(portal=round((733-591)*33.2/1107.2*_k,2),door=round((685-636)*33.2/1107.2*_k,2),window=round((673-637)*33.2/1107.2*_k,2))

# ---------------------------------------------------------------- portal F and its door
# The courtyard edge p=CI2 -> q=CI1 (pass 27's order); u runs from its middle towards CI1 (towards -s).
P_,Q_=CI[2],CI[1];S_MID=(F(P_)[0]+F(Q_)[0])/2;L_EDGE=math.dist(P_,Q_)
# The portal's axis is put on the window column above it: in pano 2 and in the 2017 photograph the
# state-floor window and the small window over the tablet stand on the portal's axis. That column is
# pass 126's row at u -7.60 (s 25.47; the chapel's niche, pass 130), 2.37 m from the south corner:
# within the readings (pano 2 2.6, photograph 3.5, pass 129 3-3.5).
U_F=-7.60;S_F=round(S_MID-U_F,3)
# Heights from pano 2 (above): pedestals 0.58, columns to 2.40, lower entablature to 2.89, the herm
# storey to 4.23, the upper cornice to 4.40, the segmental tablet to 4.94; the door 1.38 m wide,
# springing 1.46, crown 2.14. Width 4.0 (pano 2) to 4.9 (2017 photograph): 4.2.
H_=HEIGHTS
PORTAL=dict(u=U_F,s=S_F,width=4.20,ped=H_['pedestal_top'],col=[H_['pedestal_top'],H_['column_top']],col_r=.14,col_u=[.95,1.80],
 ent1=[H_['column_top'],H_['lower_entablature_top']],herm=[H_['lower_entablature_top'],H_['upper_cornice_bottom']],herm_u=[.95,1.80],
 panel=[H_['lower_entablature_top']+.12,H_['upper_cornice_bottom']-.12],panel_w=1.30,ent2=[H_['upper_cornice_bottom'],H_['upper_cornice_top']],
 cap=[H_['upper_cornice_top'],H_['tablet_top']],cap_w=1.90,open_w=1.40,open_h=H_['door_springing'],open_r=.70)
DOOR=[U_F,ZC,PORTAL['open_w'],PORTAL['open_h'],PORTAL['open_r']]
# The middle-row window over the portal (pass 127's SW row: sill 9.9, 1.2 m) sits on the portal's top,
# as in pano 2 and the 2017 photograph: sill 0.05 m over the tablet, head unchanged (z 11.10).
MIDWIN=dict(u=U_F,b0=9.9,b=round(ZC+PORTAL['cap'][1]+.05,3),head=11.1)

# ---------------------------------------------------------------- the stair (Sydöstra vindelstenen) and its approach
RISERS=30;RISE=round((ZCH-ZC)/RISERS,4);TREAD=.26;N1=14;N2=RISERS-N1
Z_L1=round(ZC+N1*RISE,4)
C_HALL=-9.33                    # the ground-floor hall's courtyard edge: the back of pass 27's courtyard skin (the line runs c -9.28 to -9.37)
C_CW=-9.25                       # the courtyard side of the stair lane (pass 27's courtyard skin's back is c -9.37)
C_L1=-7.45                       # flight 1's inner edge (a spine wall beyond)
S_V0,S_V1=24.20,26.50            # the vestibule inside the portal (the door at s 24.77-26.17)
S_R1=[round(S_V1+k*TREAD,4) for k in range(N1)]          # risers of flight 1 along +s
S_L1=S_R1[-1]                                             # flight 1's top riser = the half landing's edge (29.88)
S_ROOM0=B130['room']['s_a']+B130['room']['t_a']          # the altar wall's back, s 28.70: the stair hall starts here
S_ROOM1=31.25                    # the stair hall's far side (up to the tower's lining)
C_OI=-1.25;C_OB=B130['room']['c_oo']                     # the outer wall's inner face and back, as in the chapel
C_R2=[round(C_L1+k*TREAD,4) for k in range(N2)]          # risers of flight 2 along +c
C_L2=C_R2[-1]                                             # the top landing's edge (c -3.55)
ZCEIL_LOW=10.0                   # the plastered ceiling under the chapel's floor slab (z 10.17)
ZCEIL=14.20                      # the stair hall's ceiling
ZB=ZC-.30
TS=CA['towers']['S'];TSC=tuple(TS['centre']);TSR=TS['radius']
TOWER_SKIN=Point(TSC).buffer(TSR+.36,128)                 # pass 27's tower with its skin
TOWER_LINE=Point(TSC).buffer(TSR+.36+.20,128)             # plus the stair hall's lining
ENV13=SB(S_ROOM0,S_ROOM1+.20,C_CW-.30,C_OB).difference(TOWER_SKIN)
ROOM13=SB(S_ROOM0,S_ROOM1,C_CW,C_OI).difference(TOWER_LINE)
WALL13=ENV13.difference(ROOM13)
HALL=unary_union([SB(S_V0-.20,S_ROOM0,C_HALL,C_L1+.20),SB(27.90,S_ROOM0,C_CW-.25,C_HALL)])   # the ground-floor hall under the chancel, with the wall piece by the south corner (envelope)
ENV=unary_union([ENV13,HALL])
def clip(p):
 g=p.intersection(ROOM13);return g if g.geom_type=='Polygon' else max(g.geoms,key=lambda q:q.area)
STEPS=[]
for k in range(1,N1):                                    # flight 1 treads 1..13 (under the chancel, then into the hall)
 g=SB(S_R1[k-1],S_R1[k],C_CW,C_L1);STEPS.append(dict(flight=1,k=k,top=round(ZC+k*RISE,4),ring=ring(g)))
LAND1=SB(S_L1,S_ROOM1,C_CW,C_L1).intersection(ROOM13)
for k in range(1,N2):                                    # flight 2 treads 1..15 (across the range)
 g=clip(SB(S_L1,S_ROOM1,C_R2[k-1],C_R2[k]));STEPS.append(dict(flight=2,k=k,top=round(Z_L1+k*RISE,4),ring=ring(g)))
LAND2=clip(SB(S_ROOM0,S_ROOM1,C_L2,C_OI))
SPINE13=SB(S_ROOM0,S_L1,C_L1,C_L2)                        # full-height spine between the flights' wells
DOOR_A=B130['doors']['altar']

# ---------------------------------------------------------------- checks
CO=Polygon(CA['outer']);CP=Polygon(CA['court']);BODY=CO.difference(CP)
checks=dict(readings={k:{kk:v for kk,v in r.items() if kk!='rays'} for k,r in READ.items()},heights=HEIGHTS,widths=WIDTHS)
checks['portal_s']=S_F;checks['portal_axis_from_corner']=round(S_CORNER-S_F,2)
checks['portal_edges_s']=[round(S_F-PORTAL['width']/2,2),round(S_F+PORTAL['width']/2,2)]
checks['portal_clear_of_corner_m']=round(S_CORNER-(S_F+PORTAL['width']/2),2)
checks['door_in_edge']=abs(U_F)+PORTAL['open_w']/2<L_EDGE/2-.3
checks['rise']=RISE;checks['tread']=TREAD;checks['blondel_2R_plus_T']=round(2*RISE+TREAD,3)
checks['flight1_top_s']=S_L1;checks['landing1_z']=Z_L1;checks['landing2_z']=ZCH;checks['landing2_c']=C_L2
# headroom under the chancel: the highest tread under the chapel's slab (s < 28.70)
under=[st['top'] for st in STEPS if st['flight']==1 and S_R1[st['k']-1]<S_ROOM0]
checks['headroom_under_chapel_min_m']=round(ZCEIL_LOW-max(under),2)
checks['env_outside_body_m2']=round(ENV.difference(BODY).area,4)
checks['env_in_court_m2']=round(ENV.intersection(CP).area,4)
for k,t in CA['towers'].items():checks[f'env_in_tower_{k}_m2']=round(ENV.intersection(Point(t['centre']).buffer(t['radius']+.36,128)).area,4)
def w125(s,c):f=B125['frame'];return (f['origin'][0]+f['u'][0]*s+f['n'][0]*c,f['origin'][1]+f['u'][1]*s+f['n'][1]*c)
R125=unary_union([Polygon([w125(r['s0'],r['c0']),w125(r['s1'],r['c0']),w125(r['s1'],r['c1']),w125(r['s0'],r['c1'])]).buffer(2.2) for r in B125['rooms'].values()])
st=B126['stair'];E_,IN_=st['E'],st['IN'];W1=st['W1']
def w126(a,b):return (W1[0]+E_[0]*a+IN_[0]*b,W1[1]+E_[1]*a+IN_[1]*b)
R126=Polygon([w126(st['a_end']-1,-1),w126(30,-1),w126(30,8),w126(st['a_end']-1,8)])
ENV130=SB(B130['room']['s_w']-B130['room']['t_w'],S_ROOM0,B130['room']['c_co'],B130['room']['c_oo'])
for nm,g in (('pass125',R125),('pass126',R126),('pass131_grona',Polygon(B131['gron']['env'])),('pass131_forbranda',Polygon(B131['forb']['env']))):
 checks[f'env_vs_{nm}_m2']=round(ENV.intersection(g).area,4);checks[f'dist_{nm}_m']=round(ENV.distance(g),2)
# The chapel's envelope is above z 10.17; only the ground-floor hall (below z 10.15) lies under it.
checks['room13_vs_chapel_m2']=round(ENV13.intersection(ENV130).area,4)
checks['hall_under_chapel_m2']=round(HALL.intersection(ENV130).area,2)
checks['landing2_reaches_altar_door']=LAND2.contains(Point(W(S_ROOM0+.05,DOOR_A['c']-DOOR_A['w']/2+.05))) and LAND2.contains(Point(W(S_ROOM0+.05,DOOR_A['c']+DOOR_A['w']/2-.05)))
checks['flight2_min_width_m']=round(min((Polygon(s['ring']).area/TREAD) for s in STEPS if s['flight']==2),2)
checks['room13_area_m2']=round(ROOM13.area,2);checks['walls13_area_m2']=round(WALL13.area,2)
bad=[]
for s in STEPS:
 if Polygon(s['ring']).area<.2:bad.append(('small_step',s['flight'],s['k']))
assert not bad,bad
assert RISE<=.18 and .58<=checks['blondel_2R_plus_T']<=.66,checks
assert checks['headroom_under_chapel_min_m']>=2.0,checks
assert checks['env_outside_body_m2']<.01 and checks['env_in_court_m2']<.01,checks
assert all(checks[f'env_in_tower_{k}_m2']<.01 for k in CA['towers']),checks
assert all(checks[k]==0 for k in checks if k.startswith('env_vs_')),checks
assert checks['room13_vs_chapel_m2']<.01 and checks['landing2_reaches_altar_door'],checks
assert checks['door_in_edge'] and checks['portal_clear_of_corner_m']>.1,checks
assert checks['flight2_min_width_m']>1.0,checks
assert abs(S_L1-(S_V1+(N1-1)*TREAD))<1e-6 and S_ROOM0<S_L1<S_ROOM1-1.0

OUT=dict(source='pass 133: Street View 2014 (viewed only), Commons 2017, Olsson 1957/1974 (read only), KLM plan över praktvåningen (viewed), Krigsarkivet 0424:058:212a; see references/block133-notes.md',
 frame=dict(origin=O,u=U,n=N,range='SW'),zc=ZC,floor=FL,zch=ZCH,readings=READ,heights=HEIGHTS,widths=WIDTHS,
 portal=PORTAL,door=DOOR,edge=[2,1],midwin=MIDWIN,
 stair=dict(risers=RISERS,rise=RISE,tread=TREAD,n1=N1,n2=N2,z_l1=Z_L1,c_cw=C_CW,c_l1=C_L1,c_line=C_LINE,s_v0=S_V0,s_v1=S_V1,s_r1=S_R1,s_l1=S_L1,
  s_room0=S_ROOM0,s_room1=S_ROOM1,c_oi=C_OI,c_ob=C_OB,c_r2=C_R2,c_l2=C_L2,zceil_low=ZCEIL_LOW,zceil=ZCEIL,zb=ZB,s_corner=round(S_CORNER,3)),
 steps=STEPS,land1=ring(LAND1),land2=ring(LAND2),spine13=ring(SPINE13),walls13=ring(WALL13),env13=ring(ENV13),room13=ring(ROOM13),hall=ring(HALL),
 checks=checks)
(R/'source/block133.json').write_text(json.dumps(OUT,indent=1,ensure_ascii=False))
(R/'previews/block133-zones.json').write_text(json.dumps({'pass':133,'zones':dict(stair_hall=ring(ROOM13),stair_hall_envelope=ring(ENV13),ground_hall=ring(HALL),
 portal_f=ring(SB(S_F-PORTAL['width']/2,S_F+PORTAL['width']/2,C_LINE-1.2,C_LINE))),'checks':checks},indent=1,ensure_ascii=False))
print(json.dumps(checks,indent=0,ensure_ascii=False)[:4000])
print('BLOCK133_PREPARE_OK','portal s',S_F,'from corner',round(S_CORNER-S_F,2),'risers',RISERS,'x',RISE,'tread',TREAD,'steps',len(STEPS))
