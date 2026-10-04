"""Pass 131: two more state-floor interiors of Kalmar slott.
- Gröna salen: Olsson's room 87, 'Stora västra salen' (Möller 1882: 'Unionssalen'), in the west range
  (pass 27's 'NW' range) between Kuretornet and the west round tower (Olsson's IX, Rödkullatornet;
  pass 27's tower 'W'), with its far end in the corner where the south range (the chapel, pass 130)
  begins.
- Förbrända salen: Olsson's rooms 74 and 76, 'Stora östra salen', in the east range (pass 27's 'SE_e'
  range) between the two bays of the outer front (pass 27's 'bay2' = Olsson's tower VI, room 75, and
  'bay1' = tower VII, room 77).

Which range, and where along it (Olsson 1974, Fornvännen 69, fig. 1, read only, in copyright):
- The plan was registered to the model on the four round towers (Olsson II, IX, VIII, V = pass 27's
  N, W, S, E): a similarity of 11.47 px/m (the plan's own 0-100 m bar reads 11.37 px/m), residuals
  4, 9, 7 and 12 px (0.35-1.0 m). The model outline then lies on Olsson's walls all round. Pixel
  readings (on a 400 dpi rendering of p. 91, cropped) are listed in OLSSON below; only numbers are kept.
- Room 87 runs from Kuretornet's south face to tower IX. Its courtyard wall bends where the courtyard
  corner is: beyond it the room's wall is the chapel's west end wall (Olsson draws 86's end wall in
  line with 87's courtyard wall). Its far end wall is the south range's outer wall, and tower IX's
  round wall bulges into the room's outer corner. The photographs agree: looking along the room
  towards the tower (2017, 1929) the far end wall has two windows on the courtyard half, and on the
  right the tower's curved wall carries a pedimented door.
- Rooms 74 and 76 are one hall in the east range between Olsson's towers VI and VII (pass 27's bay2
  and bay1), from the stair 72 at the north to the wall by 77/82 at the courtyard corner. Registered,
  the hall's inner faces lie at SE_e s -1.5 ... 21.3 and its width is 11.1-11.4 m.

Heights and widths (Möller, 'Calmar slott. Profiler', 1882, PK006-00041, public domain; 57.97 px/m,
pass 127's reading of the 90-fot bar; floor = his red state-floor line):
- 'Profil genom Unions-salen' (87): inner faces x 5599 / 6248.5 (11.20 m), walls 1.28 m (court,
  x 5525-5599) and 1.88 m (outer, 6248.5-6357.5); ceiling beams' underside row 6770/6763 (6.55 m over
  the floor at row 7147.5), their top row 6748 (6.89 m); window niches from 0.17 m (row 7137) to
  4.10 m (row 6910) at the room face, glass 1.29-3.82 m (rows 7072/6925).
- 'Profil genom s.k. Brända salen' (76): inner faces x 1592.5 / 2294 (12.10 m), walls 1.94 m (outer,
  x 1480-1592.5) and 1.44 m (court, 2294-2377.5); ceiling beams' underside row 6792 (6.24 m over the
  floor at row 7152.5), top row 6775 (6.51 m); niches 0.35 m (row 7132.5) to 5.60 m (row 6827.5) at
  the room face, 5.35 m at the glass (row 6842); glass 1.34-3.98 m (rows 7075/6922). (In 1882 the
  hall had a loose intermediate floor on posts, 'löst, ofullständigt bjälklag'; it was removed in the
  1923 restoration, see the KMB photographs.)

The model's ranges are deeper than Möller's sections (west range 15.0 m facade to facade against
14.36 m; east range 16.7 against 15.53). The rooms keep Möller's inside widths; the excess goes into
both walls equally.

Window niches sit on the facade's windows as the saved scene has them (SM_Kalmar_Slott glass, read with
SCR/p131/dump131.py on a copy of source/Stortorget.blend after pass 129's official build).

Output: source/block131.json (frames, levels, room and wall footprints, wall pieces, niches, doors,
beams, furnishing positions), previews/block131-zones.json (footprints and checks).
Run with Shapely: KALMAR_GEO=<site-packages> python3 scripts/prepare_block131.py
"""
from pathlib import Path
import json,math,os,sys
if os.environ.get('KALMAR_GEO'):sys.path.insert(0,os.environ['KALMAR_GEO'])
from shapely.geometry import Polygon,Point,LineString,MultiPolygon,GeometryCollection
from shapely.ops import unary_union,split
R=Path(__file__).resolve().parents[1]
C27=json.loads((R/'source/castle27.json').read_text());CA=C27['castle']
B125=json.loads((R/'source/block125.json').read_text());B126=json.loads((R/'source/block126.json').read_text())
B127=json.loads((R/'source/block127.json').read_text());B130=json.loads((R/'source/block130.json').read_text())
RG={r['name']:r for r in CA['ranges']}
def Wr(name,s,c):r=RG[name];o,u,n=r['origin'],r['u'],r['n'];return (o[0]+u[0]*s+n[0]*c,o[1]+u[1]*s+n[1]*c)
def Fr(name,p):r=RG[name];o,u,n=r['origin'],r['u'],r['n'];dx,dy=p[0]-o[0],p[1]-o[1];return (dx*u[0]+dy*u[1],dx*n[0]+dy*n[1])
def rnd(p,k=4):return [round(p[0],k),round(p[1],k)]
def ring(poly):return [rnd(p) for p in list(poly.exterior.coords)[:-1]]
def isect(p1,d1,p2,d2):
 # intersection of two lines p+t*d
 den=d1[0]*d2[1]-d1[1]*d2[0];t=((p2[0]-p1[0])*d2[1]-(p2[1]-p1[1])*d2[0])/den;return (p1[0]+d1[0]*t,p1[1]+d1[1]*t)
def unit(v):L=math.hypot(*v);return (v[0]/L,v[1]/L)
def clean(coords,tol_ang=.5,tol_len=.002):
 # drop near-duplicate points, spikes and nearly straight corners (they stop the town bevel)
 pts=list(coords);changed=True
 while changed and len(pts)>3:
  changed=False
  for k in range(len(pts)):
   a,b,c=pts[k-1],pts[k],pts[(k+1)%len(pts)]
   v1=(a[0]-b[0],a[1]-b[1]);v2=(c[0]-b[0],c[1]-b[1])
   if math.hypot(*v1)<tol_len:pts.pop(k);changed=True;break
   ang=abs(math.degrees(math.atan2(v1[0]*v2[1]-v1[1]*v2[0],v1[0]*v2[0]+v1[1]*v2[1])))
   if ang<tol_ang or ang>180-tol_ang:pts.pop(k);changed=True;break
 return pts
FL=B127['floor'];Z0=round(FL-.30,3)

# ---------------------------------------------------------------- sources: Möller and Olsson
MOLLER=dict(px_per_m=57.97,
 union87=dict(floor_row=7147.5,x_court_out=5525,x_court_in=5599,x_out_in=6248.5,x_out_out=6357.5,beam_under_rows=[6770,6763],beam_top_row=6748,
  niche_floor_row=7137,niche_head_room_row=6910,niche_head_glass_row=6925,glass_rows=[7072,6925]),
 brand76=dict(floor_row=7152.5,x_out_out=1480,x_out_in=1592.5,x_court_in=2294,x_court_out=2377.5,beam_under_row=6792,beam_top_row=6775,
  niche_floor_row=7132.5,niche_head_room_row=6827.5,niche_head_glass_row=6842,glass_rows=[7075,6922]))
def mm(d,a,b):return round(abs(a-b)/MOLLER['px_per_m'],2)
for k in ('union87','brand76'):
 d=MOLLER[k];P=MOLLER['px_per_m']
 d['inside_m']=mm(d,d['x_out_in'],d['x_court_in']);d['court_wall_m']=mm(d,d['x_court_in'],d['x_court_out']);d['outer_wall_m']=mm(d,d['x_out_out'],d['x_out_in'])
 d['depth_m']=mm(d,d['x_out_out'],d['x_court_out'])
 bu=d['beam_under_rows'] if 'beam_under_rows' in d else [d['beam_under_row']]
 d['ceiling_m']=round(sum(d['floor_row']-r for r in bu)/len(bu)/P,2);d['ceiling_top_m']=round((d['floor_row']-d['beam_top_row'])/P,2)
 d['niche_m']=[round((d['floor_row']-d['niche_floor_row'])/P,2),round((d['floor_row']-d['niche_head_room_row'])/P,2),round((d['floor_row']-d['niche_head_glass_row'])/P,2)]
 d['glass_m']=[round((d['floor_row']-r)/P,2) for r in d['glass_rows']]
M87,M76=MOLLER['union87'],MOLLER['brand76']
# Olsson 1974 fig. 1 (400 dpi rendering of p. 91, crop offset 711/626 px): tower centres and readings
OLSSON=dict(px_per_m_fit=11.47,px_per_m_bar=11.37,towers_px={'N':[160,860],'W':[925,852],'S':[1050,360],'E':[330,240]},residual_px=[4.1,8.6,6.5,11.9],
 room87_se_frame=dict(east_face_s=[34.22,34.61],court_face_c=[-15.95,-16.65],outer_face_c=[-4.63,-5.56],court_windows_s=[36.98,42.93,47.67,52.08],outer_windows_s=[37.86,41.84,45.27,49.1,53.37]),
 room74_76_SE_e=dict(south_face_s=[-1.33,-1.6],north_face_s=[21.53,21.18],outer_face_c=[0.12,-2.07],court_face_c=[-11.35,-13.21],court_windows_s=[2.9,7.26,11.16,14.86],outer_windows_s=[2.8,7.24,11.62,14.86]),
 area_74_76_text_m2=440)

# ---------------------------------------------------------------- facade windows (saved scene, SCR/p131/dump.json)
FACADE=dict(read='SM_Kalmar_Slott glass (M_Town_Glass), saved scene after pass 129, SCR/p131/dump131.py',
 NW_court=[37.67,41.47,45.27,49.07,52.87],NW_court_w=1.20,NW_outer=[38.32,42.72,47.12,51.52],NW_outer_w=1.15,
 SW_outer=[3.69],SW_outer_w=1.15,
 SEe_court=[1.16,4.93,9.80,13.57,17.33],SEe_court_c=[-16.13,-15.60,-14.92,-14.40,-13.88],SEe_court_w=1.19,
 SEe_outer=[3.55,7.91,12.28],SEe_outer_c=[0.49,1.06,1.63],SEe_outer_w=1.14,
 state_z=[11.57,14.77])

# ================================================================= Gröna salen (room 87), NW range frame
CO=Polygon(CA['outer']);CI=Polygon(CA['court']);BODY=CO.difference(CI)
TW=CA['towers']['W'];TWC=tuple(TW['centre']);TWR=TW['radius']
def line_fit(pts):
 n=len(pts);ms=sum(p[0] for p in pts)/n;mc=sum(p[1] for p in pts)/n
 b=sum((p[0]-ms)*(p[1]-mc) for p in pts)/sum((p[0]-ms)**2 for p in pts);return (mc-b*ms,b)
OUTF=line_fit([Fr('NW',CA['outer'][60]),Fr('NW',CA['outer'][0])])    # outer outline (Kuretornet to the west tower)
CRTF=line_fit([Fr('NW',CA['court'][10]),Fr('NW',CA['court'][0])])    # courtyard outline (W1 to the courtyard corner)
def co_(s):return OUTF[0]+OUTF[1]*s
def cc_(s):return CRTF[0]+CRTF[1]*s
SKIN_O,SKIN_C=.36,.355               # pass 27's skins: outward of the outer outline, courtyard-ward of the courtyard outline
SMID=45.0
DEPTH87=round((co_(SMID)+SKIN_O)-(cc_(SMID)-SKIN_C),3)
EX87=round((DEPTH87-M87['depth_m'])/2,3)
TO87=round(M87['outer_wall_m']+EX87,3);TC87=round(M87['court_wall_m']+EX87,3)
def coi(s):return co_(s)+SKIN_O-TO87     # outer room face
def cci(s):return cc_(s)-SKIN_C+TC87     # courtyard room face
def cob(s):return co_(s)-.10             # backs: 0.10 m inside pass 27's outline
def ccb(s):return cc_(s)+.10
S_E,S_EB=36.08,35.70                     # east wall (lining against Kuretornet and the stair hall)
SW_L,SW_LB=4.60,4.90                     # lining in front of the chapel's west wall (pass 130: SW s 4.92-6.20)
SW_CE=B130['room']['c_co']               # the chapel's courtyard-side edge, SW c -9.25
C_END,C_ENDB=-1.60,-0.10                 # the south range's outer wall (SW frame): room face, back
R_ARC,R_ARCB=round(TWR+.36+.225,3),round(TWR+.36+.025,3)   # tower W: room face and back of the lining round it
U_NW=RG['NW']['u'];N_NW=RG['NW']['n'];U_SW=RG['SW']['u'];N_SW=RG['SW']['n']
def nwline(f,s):return Wr('NW',s,f(s))
def nwdir(f):a=Wr('NW',0,f(0));b=Wr('NW',100,f(100));return unit((b[0]-a[0],b[1]-a[1]))
def circ_line(p,d,r,far=True):
 # intersection of the line p+t*d (d unit) with the circle round TWC; the root on the +d side if far
 fx,fy=p[0]-TWC[0],p[1]-TWC[1];b=fx*d[0]+fy*d[1];c=fx*fx+fy*fy-r*r;disc=b*b-c
 t=-b+math.sqrt(disc) if far else -b-math.sqrt(disc);return (p[0]+d[0]*t,p[1]+d[1]*t)
# room corners
A=Wr('NW',S_E,coi(S_E));B=Wr('NW',S_E,cci(S_E))
C=isect(Wr('NW',40,cci(40)),nwdir(cci),Wr('SW',SW_L,SW_CE),tuple(N_SW))
D=Wr('SW',SW_L,C_END)
E=circ_line(D,tuple(-x for x in U_SW),R_ARC,far=False)
F=circ_line(Wr('NW',40,coi(40)),nwdir(coi),R_ARC,far=False)
def arc(p,q,r,k=None):
 a0=math.atan2(p[1]-TWC[1],p[0]-TWC[0]);a1=math.atan2(q[1]-TWC[1],q[0]-TWC[0])
 while a1-a0>math.pi:a1-=2*math.pi
 while a0-a1>math.pi:a1+=2*math.pi
 k=k or max(2,int(abs(a1-a0)/math.radians(3))+1)
 return [(TWC[0]+r*math.cos(a0+(a1-a0)*i/k),TWC[1]+r*math.sin(a0+(a1-a0)*i/k)) for i in range(k+1)]
ARC_ROOM=arc(E,F,R_ARC)
LC=Wr('SW',SW_L,SW_CE)                   # where the lining's face meets the chapel's courtyard edge
ROOM87=Polygon([A,B,C,LC,D]+ARC_ROOM[:-1]+[F])
assert ROOM87.is_valid,ROOM87
# envelope (the walls' backs)
E1=Wr('NW',S_EB,cob(S_EB));E2=Wr('NW',S_EB,ccb(S_EB))
E3=isect(Wr('NW',40,ccb(40)),nwdir(ccb),Wr('SW',SW_LB,SW_CE),tuple(U_SW))
E4=Wr('SW',SW_LB,SW_CE);E5=Wr('SW',SW_LB,C_ENDB)
E6=circ_line(E5,tuple(-x for x in U_SW),R_ARCB,far=False)
E7=circ_line(Wr('NW',40,cob(40)),nwdir(cob),R_ARCB,far=False)
ARC_BACK=arc(E6,E7,R_ARCB)
ENV87=Polygon([E1,E2,E3,E4,E5]+ARC_BACK[:-1]+[E7])
assert ENV87.is_valid and ENV87.contains(ROOM87)
WALL87=ENV87.difference(ROOM87)
# split the wall ring into named pieces at the room's corners
def ext(p,q,e=.02):d=unit((q[0]-p[0],q[1]-p[1]));return LineString([(p[0]-d[0]*e,p[1]-d[1]*e),(q[0]+d[0]*e,q[1]+d[1]*e)])
CUTS=[ext(A,E1),ext(B,E2),ext(C,E4),ext(D,E5),ext(E,E6),ext(F,E7)]
from shapely.ops import polygonize
pieces=[g for g in polygonize(unary_union([LineString(list(ENV87.exterior.coords)),LineString(list(ROOM87.exterior.coords))]+CUTS)) if g.area>1e-6 and WALL87.contains(g.representative_point())]
assert abs(sum(g.area for g in pieces)-WALL87.area)<1e-4,(sum(g.area for g in pieces),WALL87.area)
FACES87=dict(east=LineString([A,B]),court=LineString([B,C]),lining=LineString([C,LC,D]),end=LineString([D,E]),arc=LineString(ARC_ROOM),outer=LineString([F,A]))
PIECES87={}
for pc in pieces:
 best=max(FACES87,key=lambda k:pc.buffer(.01).intersection(FACES87[k]).length)
 assert best not in PIECES87,(best,pc.area)
 PIECES87[best]=pc
assert set(PIECES87)==set(FACES87),set(PIECES87)
# niches: footprints through the walls (room-face span and back span), from the facade windows
def niche_nw(side,s_out,w_glass,s_in=None,r_in=.825,blind=False):
 s_in=s_out if s_in is None else s_in
 if side=='court':fi,fb=cci,ccb
 else:fi,fb=coi,cob
 r_out=w_glass/2+.05
 pi0,pi1=Wr('NW',s_in-r_in,fi(s_in-r_in)),Wr('NW',s_in+r_in,fi(s_in+r_in))
 nrm=unit((N_NW[0]*(-1 if side=='court' else 1),N_NW[1]*(-1 if side=='court' else 1)))
 if blind:
  dep=(abs(fb(s_in)-fi(s_in)))-.15;po0,po1=(pi0[0]+nrm[0]*dep,pi0[1]+nrm[1]*dep),(pi1[0]+nrm[0]*dep,pi1[1]+nrm[1]*dep);back=dep
 else:
  po0,po1=Wr('NW',s_out-r_out,fb(s_out-r_out)),Wr('NW',s_out+r_out,fb(s_out+r_out));back=abs(fb(s_out)-fi(s_out))
  po0,po1=(po0[0]+nrm[0]*.05,po0[1]+nrm[1]*.05),(po1[0]+nrm[0]*.05,po1[1]+nrm[1]*.05)
 return dict(room='gron',wall=side,frame='NW',s_in=round(s_in,3),s_out=round(s_out,3),r_in=r_in,r_out=round(r_out,3),blind=blind,
  foot=[rnd(pi0),rnd(pi1),rnd(po1),rnd(po0)],t=rnd(unit((pi1[0]-pi0[0],pi1[1]-pi0[1])),5),nrm=rnd(nrm,5),
  face_mid=rnd(((pi0[0]+pi1[0])/2,(pi0[1]+pi1[1])/2)),back_mid=rnd(Wr('NW',s_out,fb(s_out)) if not blind else ((po0[0]+po1[0])/2,(po0[1]+po1[1])/2)),depth=round(back,3))
def niche_sw(s_out,w_glass,r_in=.62,blind=False):
 r_out=w_glass/2+.05;nrm=tuple(N_SW)
 pi0,pi1=Wr('SW',s_out+r_in,C_END),Wr('SW',s_out-r_in,C_END)
 if blind:
  dep=C_ENDB-C_END-.15;po0,po1=Wr('SW',s_out+r_in,C_END+dep),Wr('SW',s_out-r_in,C_END+dep)
 else:
  dep=C_ENDB-C_END;po0,po1=Wr('SW',s_out+r_out,C_ENDB+.05),Wr('SW',s_out-r_out,C_ENDB+.05)
 return dict(room='gron',wall='end',frame='SW',s_in=s_out,s_out=s_out,r_in=r_in,r_out=round(r_out,3),blind=blind,foot=[rnd(pi0),rnd(pi1),rnd(po1),rnd(po0)],
  t=rnd(unit((pi1[0]-pi0[0],pi1[1]-pi0[1])),5),nrm=rnd(nrm,5),face_mid=rnd(Wr('SW',s_out,C_END)),back_mid=rnd(Wr('SW',s_out,C_END+dep)),depth=round(dep,3))
NI87=[]
for s in FACADE['NW_court']:
 if s>52:NI87.append(niche_nw('court',s,FACADE['NW_court_w'],s_in=52.38,r_in=.75))   # skewed: its room face stops short of the bend at C
 else:NI87.append(niche_nw('court',s,FACADE['NW_court_w']))
for s in FACADE['NW_outer']:NI87.append(niche_nw('out',s,FACADE['NW_outer_w']))
NI87.append(niche_sw(FACADE['SW_outer'][0],FACADE['SW_outer_w']))
NI87.append(niche_sw(1.55,FACADE['SW_outer_w'],blind=True))      # the second window of the photographs (pier between them about one window wide): no facade window there
LV87=dict(floor=FL,z0=Z0,niche_floor=round(FL+M87['niche_m'][0],3),sill=FACADE['state_z'][0],glass_top=FACADE['state_z'][1],niche_head=14.95,
 door_head=round(FL+2.40,3),beam_under=round(FL+M87['ceiling_m'],3),board_under=round(FL+M87['ceiling_m']+.30,3),ztop=round(FL+M87['ceiling_m']+.38,3))
# doors: east (to the stair hall and Kuretornet; closed), chapel (pass 130's west door, opposite), tower (closed)
def door_rect(p,t,nrm,w,d0,d1):
 return [rnd((p[0]+t[0]*a+nrm[0]*d,p[1]+t[1]*a+nrm[1]*d)) for a,d in ((-w/2,d0),(w/2,d0),(w/2,d1),(-w/2,d1))]
DOORS87=[]
pe=Wr('NW',S_E,-12.30);DOORS87.append(dict(name='east',wall='east',p=rnd(pe),t=rnd(tuple(N_NW),5),nrm=rnd(tuple(-x for x in U_NW),5),w=1.05,h=2.40,depth=round(S_E-S_EB,3),leaf=True,
 foot=door_rect(pe,tuple(N_NW),tuple(-x for x in U_NW),1.05,-.02,S_E-S_EB+.05)))
pc_=Wr('SW',SW_L,B130['doors']['west']['c']);DOORS87.append(dict(name='chapel',wall='lining',p=rnd(pc_),t=rnd(tuple(N_SW),5),nrm=rnd(tuple(U_SW),5),w=B130['doors']['west']['w'],h=B130['doors']['west']['h'],
 depth=round(SW_LB-SW_L,3),leaf=False,foot=door_rect(pc_,tuple(N_SW),tuple(U_SW),B130['doors']['west']['w'],-.02,SW_LB-SW_L+.05)))
am=ARC_ROOM[len(ARC_ROOM)//2];rn=unit((TWC[0]-am[0],TWC[1]-am[1]));tn=(-rn[1],rn[0])
DOORS87.append(dict(name='tower',wall='arc',p=rnd(am),t=rnd(tn,5),nrm=rnd(rn,5),w=1.05,h=2.30,depth=round(R_ARC-R_ARCB,3),leaf=True,foot=door_rect(am,tn,rn,1.05,-.02,R_ARC-R_ARCB+.05)))
# ceiling beams across the hall: along NW n, fanning by up to 10.6 deg towards the chapel's direction
# at the far end (photographs 2017: the beams follow the bend)
def ang(v):return math.atan2(v[1],v[0])
a_nw=ang(N_NW);a_sw=ang(tuple(-x for x in U_SW))     # the chapel's end wall runs along SW n; beams across it run along -SW u
d_ang=(a_sw-a_nw+math.pi)%(2*math.pi)-math.pi
BEAMS87=[];s=S_E+.55
while s<64:
 f=min(1,max(0,(s-50.5)/7.0));th=a_nw+d_ang*f;dv=(math.cos(th),math.sin(th))
 mid=Wr('NW',s,(cci(s)+coi(s))/2)
 L=LineString([(mid[0]-dv[0]*30,mid[1]-dv[1]*30),(mid[0]+dv[0]*30,mid[1]+dv[1]*30)]).intersection(ROOM87)
 segs=[L] if L.geom_type=='LineString' else list(getattr(L,'geoms',[]))
 for g in segs:
  if g.length>.6:BEAMS87.append([rnd(g.coords[0]),rnd(g.coords[-1])])
 s+=.95
# board floor strips along NW u
BOARDS87=[];k=0;cmin=min(Fr('NW',p)[1] for p in ROOM87.exterior.coords);cmax=max(Fr('NW',p)[1] for p in ROOM87.exterior.coords)
c=cmin
while c<cmax:
 strip=Polygon([Wr('NW',30,c),Wr('NW',70,c),Wr('NW',70,c+.30),Wr('NW',30,c+.30)]).intersection(ROOM87)
 for g in ([strip] if strip.geom_type=='Polygon' else list(getattr(strip,'geoms',[]))):
  if g.geom_type=='Polygon' and g.area>.005:
   co=clean(list(g.simplify(0.0005).exterior.coords)[:-1])
   if len(co)>=3 and Polygon(co).area>.005:BOARDS87.append(dict(k=k%2,ring=[rnd(p) for p in co]))
 c+=.30;k+=1
# the walls in horizontal bands: each wall piece minus the niches and doors open in that band; the
# top band's vertices carry their own top (the courtyard roof comes lower than the ceiling's top over
# the courtyard wall's back: pass 127's roof pieces, underside 0.12 m, minus 0.10 m)
for d in DOORS87:d['h']=LV87['door_head']-FL
def cutfoot(n):
 # the niche's footprint, run 0.03 m into the room so that the cut leaves no sliver along the face
 f=[Point(*p) for p in n['foot']];nr=n['nrm'];e=.03
 return Polygon([(f[0].x-nr[0]*e,f[0].y-nr[1]*e),(f[1].x-nr[0]*e,f[1].y-nr[1]*e),(f[2].x,f[2].y),(f[3].x,f[3].y)])
NICHE_U=unary_union([cutfoot(n) for n in NI87]);DOOR_U=unary_union([Polygon(d['foot']) for d in DOORS87])
BANDS87=[(Z0,FL,False,False),(FL,LV87['niche_floor'],True,False),(LV87['niche_floor'],LV87['door_head'],True,True),(LV87['door_head'],LV87['niche_head'],False,True),(LV87['niche_head'],LV87['ztop'],False,False)]
ROOFP=[(Polygon(rr[0]),pc['plane']) for pc in B127['roof'] for rr in pc['rings']]
def roof_under0(p):
 zs=[pl[0]*p[0]+pl[1]*p[1]+pl[2] for poly,pl in ROOFP if poly.buffer(.05).contains(Point(p))]
 return (max(zs)-.12) if zs else None
def dens(coords,step=.5):
 out=[]
 for p,q in zip(coords,coords[1:]+coords[:1]):
  n=max(1,int(math.ceil(math.hypot(q[0]-p[0],q[1]-p[1])/step)))
  out+=[(p[0]+(q[0]-p[0])*i/n,p[1]+(q[1]-p[1])*i/n) for i in range(n)]
 return out
def tag_edges(coords):
 tags=[]
 for p,q in zip(coords,coords[1:]+coords[:1]):
  m_=LineString([p,q]).interpolate(.5,normalized=True)
  if NICHE_U.boundary.distance(m_)<2e-3:tags.append('r')
  elif DOOR_U.boundary.distance(m_)<2e-3:tags.append('d')
  else:tags.append('w')
 return tags
WALLBANDS87=[];CLIPPED87=0
for name,pc in PIECES87.items():
 for z0,z1,cut_d,cut_n in BANDS87:
  g=pc
  if cut_d:g=g.difference(DOOR_U)
  if cut_n:g=g.difference(NICHE_U)
  for q in ([g] if g.geom_type=='Polygon' else list(g.geoms)):
   if q.geom_type!='Polygon' or q.area<1e-5:continue
   assert len(q.interiors)==0,(name,z0)
   co=clean(list(q.simplify(1e-5).exterior.coords)[:-1])
   if len(co)<3 or Polygon(co).area<1e-4:continue
   # (no densifying: collinear points make zero-area cap triangles, which stop the town bevel)
   zt=[]
   for pt in co:
    ru=roof_under0(pt) if z1==LV87['ztop'] else None
    zz=z1 if ru is None else min(z1,round(ru-.10,3))
    if zz<z1:CLIPPED87+=1
    zt.append(round(zz,3))
   WALLBANDS87.append(dict(piece=name,z0=z0,z1=z1,ring=[rnd(pt) for pt in co],zt=zt,tags=tag_edges(co)))
# furnishings and wall features (positions)
FEAT87=dict(fireplace=dict(wall='east',p=rnd(Wr('NW',S_E,-5.95)),w=1.50,proj=.45),
 escutcheons=[dict(wall='east',p=rnd(Wr('NW',S_E,c_)),zc=FL+4.55) for c_ in (-7.6,-10.5,-13.4)]
  +[dict(wall='out',p=rnd(Wr('NW',s_,coi(s_))),zc=FL+4.45) for s_ in (40.52,44.92,36.80)]
  +[dict(wall='court',p=rnd(Wr('NW',s_,cci(s_))),zc=FL+4.45) for s_ in (39.57,43.37,47.17)],
 crucifix=dict(wall='out',p=rnd(Wr('NW',49.32,coi(49.32))),zc=FL+3.55),
 crucifix_end=dict(wall='end',p=rnd(Wr('SW',2.62,C_END)),t=rnd(tuple(-x for x in U_SW),5),nrm=rnd(tuple(N_SW),5),zc=FL+3.45,scale=.78))

# ================================================================= Förbrända salen (rooms 74, 76), SE_e
# Own frame: u along the courtyard outline (pass 27's points 3-4-5 are collinear; 7.9 deg off the
# range's fitted axis), n outwards; origin at pass 27's outline point 26 (bay1's corner).
p3,p5=CA['court'][3],CA['court'][5];UF=unit((p5[0]-p3[0],p5[1]-p3[1]));NF=(UF[1],-UF[0])
if NF[0]*RG['SE_e']['n'][0]+NF[1]*RG['SE_e']['n'][1]<0:NF=(-NF[0],-NF[1])
OF=tuple(CA['outer'][26])
def WF(a,b):return (OF[0]+UF[0]*a+NF[0]*b,OF[1]+UF[1]*a+NF[1]*b)
def FF(p):dx,dy=p[0]-OF[0],p[1]-OF[1];return (dx*UF[0]+dy*UF[1],dx*NF[0]+dy*NF[1])
BC_OUT=sum(FF(CA['court'][i])[1] for i in (3,4,5))/3          # courtyard outline (b const)
o26,o27=FF(CA['outer'][26]),FF(CA['outer'][27]);KO=(o27[1]-o26[1])/(o27[0]-o26[0])   # outer outline: b = o26 + KO a
def bo_(a):return o26[1]+KO*(a-o26[0])
AMID=10.0
DEPTH76=round((bo_(AMID)+SKIN_O)-(BC_OUT-SKIN_C),3);EX76=round((DEPTH76-M76['depth_m'])/2,3)
TO76=round(M76['outer_wall_m']+EX76,3);TC76=round(M76['court_wall_m']+EX76,3)
BCI=round(BC_OUT-SKIN_C+TC76,3)               # courtyard room face
BOI=round(BCI+M76['inside_m'],3)              # outer room face (Möller's inside width)
BCB=round(BC_OUT+.10,3)                       # courtyard back
def bob(a):return bo_(a)-.10                  # outer back
# ends from the registered plan (SE_e s -1.5 and 21.3), converted to this frame on the hall's axis
def a_of_SEe(s):return FF(Wr('SE_e',s,-6.0))[0]
A_PLAN=[round(a_of_SEe(-1.45),3),round(a_of_SEe(21.30),3)]
A_N=A_PLAN[1];T_END=1.20
# The south face: the facade's first courtyard window (SE_e s 1.16) stands 1.2 m from the courtyard
# corner, so the plan's face (a -2.26) is moved 0.21 m south to leave a 0.45 m pier beside its niche.
A_S=None
LV76=dict(floor=FL,z0=Z0,niche_floor=round(FL+M76['niche_m'][0],3),sill=FACADE['state_z'][0],glass_top=FACADE['state_z'][1],
 crown_room=round(FL+M76['niche_m'][1],3),crown_glass=round(FL+M76['niche_m'][2],3),beam_under=round(FL+M76['ceiling_m']-.05,3),door_head=round(FL+2.30,3))
LV76['board_under']=round(LV76['beam_under']+.18,3);LV76['ztop']=round(LV76['board_under']+.06,3)
NI76=[]
def niche_f(side,s_seE,cg,w_glass):
 a=FF(Wr('SE_e',s_seE,cg))[0]          # the facade window's centre (SE_e s, c) projected on this frame's axis
 r_in=.95;r_out=round(w_glass/2+.05,3)
 return dict(room='forb',wall=side,u_in=round(a,3),u_out=round(a,3),r_in=r_in,r_out=r_out,zb=LV76['niche_floor'],zs_in=round(LV76['crown_room']-r_in,3),h_in=r_in,
  zs_out=round(LV76['crown_glass']-r_out,3),h_out=r_out,sill=LV76['sill'],facade_SEe=s_seE)
for s,c in zip(FACADE['SEe_court'],FACADE['SEe_court_c']):NI76.append(niche_f('court',s,c,FACADE['SEe_court_w']))
for s,c in zip(FACADE['SEe_outer'],FACADE['SEe_outer_c']):NI76.append(niche_f('out',s,c,FACADE['SEe_outer_w']))
A_S=round(min(n['u_in']-n['r_in'] for n in NI76)-.45,3)
ROOM76=Polygon([WF(A_S,BCI),WF(A_N,BCI),WF(A_N,BOI),WF(A_S,BOI)])
ENV76=Polygon([WF(A_S-T_END,BCB),WF(A_N+T_END,BCB),WF(A_N+T_END,bob(A_N+T_END)),WF(A_S-T_END,bob(A_S-T_END))])
DOORS76=[dict(name='south',wall='south',b=round(BCI+1.65,3),w=1.10,h=2.30),dict(name='north',wall='north',b=round(BCI+1.45,3),w=1.10,h=2.30)]
fp_a=round((NI76[5]['u_in']+NI76[6]['u_in'])/2,3)   # between the outer niches at 3.55 and 7.91 (SE_e s)
FEAT76=dict(hood=dict(wall='out',a=fp_a,w=1.70,proj=.70),fireplace_north=dict(wall='north',b=round((BCI+BOI)/2+.8,3),w=1.60),
 beams=[round(A_S+1.25+k*(A_N-A_S-2.5)/8,3) for k in range(9)])

# ================================================================= checks
checks={}
for nm,env in (('gron',ENV87),('forb',ENV76)):
 checks[f'{nm}_outside_body_m2']=round(env.difference(BODY).area,4);checks[f'{nm}_in_court_m2']=round(env.intersection(CI).area,4)
 for k,t in CA['towers'].items():checks[f'{nm}_in_tower_{k}_m2']=round(env.intersection(Point(t['centre']).buffer(t['radius']+.36,128)).area,4)
 checks[f'{nm}_in_kure_m2']=round(env.intersection(Polygon(CA['kure_rect']).buffer(.36)).area,4)
 checks[f'{nm}_in_kure_poly_m2']=round(env.intersection(Polygon(CA['kure']).buffer(.36)).area,4)
def w125(s,c):f=B125['frame'];return (f['origin'][0]+f['u'][0]*s+f['n'][0]*c,f['origin'][1]+f['u'][1]*s+f['n'][1]*c)
R125=unary_union([Polygon([w125(r['s0'],r['c0']),w125(r['s1'],r['c0']),w125(r['s1'],r['c1']),w125(r['s0'],r['c1'])]).buffer(2.2) for r in B125['rooms'].values()])
st=B126['stair'];E_,IN_=st['E'],st['IN'];W1=st['W1']
def w126(a,b):return (W1[0]+E_[0]*a+IN_[0]*b,W1[1]+E_[1]*a+IN_[1]*b)
R126=Polygon([w126(st['a_end'],-1),w126(30,-1),w126(30,8),w126(st['a_end'],8)])      # pass 126's stair strip from its end wall (a 0.4)
def p130(s,c):return Wr('SW',s,c)
ENV130=Polygon([p130(B130['room']['s_w']-B130['room']['t_w'],B130['room']['c_co']),p130(B130['room']['s_a']+B130['room']['t_a'],B130['room']['c_co']),
 p130(B130['room']['s_a']+B130['room']['t_a'],B130['room']['c_oo']),p130(B130['room']['s_w']-B130['room']['t_w'],B130['room']['c_oo'])])
for nm,env in (('gron',ENV87),('forb',ENV76)):
 checks[f'{nm}_vs_pass125_m2']=round(env.intersection(R125).area,4);checks[f'{nm}_dist_pass125_m']=round(env.distance(R125),2)
 checks[f'{nm}_vs_pass126_m2']=round(env.intersection(R126).area,4);checks[f'{nm}_dist_pass126_m']=round(env.distance(R126),2)
 checks[f'{nm}_vs_pass130_m2']=round(env.intersection(ENV130).area,4);checks[f'{nm}_dist_pass130_m']=round(env.distance(ENV130),3)
checks['gron_vs_forb_m2']=round(ENV87.intersection(ENV76).area,4)
checks['gron_room_m2']=round(ROOM87.area,2);checks['forb_room_m2']=round(ROOM76.area,2)
checks['gron_widths_m']=[round(coi(s)-cci(s),2) for s in (36,45,53)];checks['forb_width_m']=round(BOI-BCI,2)
checks['gron_walls_m']=dict(outer=TO87,court=TC87,depth_model=DEPTH87,depth_moller=M87['depth_m'])
checks['forb_walls_m']=dict(outer_at_mid=round(bo_(AMID)+SKIN_O-BOI,3),court=TC76,depth_model=DEPTH76,depth_moller=M76['depth_m'])
checks['gron_corners']={k:rnd(Fr('NW',v),3) for k,v in dict(A=A,B=B,C=C,LC=LC,D=D,E=E,F=F).items()}
checks['gron_end_SW']={k:rnd(Fr('SW',v),3) for k,v in dict(C=C,LC=LC,D=D,E=E).items()}
checks['forb_plan_a']=A_PLAN;checks['forb_ends_a']=[A_S,A_N];checks['forb_ends_SEe']=[rnd(Fr('SE_e',WF(A_S,(BCI+BOI)/2)),3),rnd(Fr('SE_e',WF(A_N,(BCI+BOI)/2)),3)]
checks['forb_frame_deg_off_SEe']=round(math.degrees(math.acos(UF[0]*RG['SE_e']['u'][0]+UF[1]*RG['SE_e']['u'][1])),2)
checks['forb_outer_skew_deg']=round(math.degrees(math.atan(KO)),2)
checks['pieces87']={k:round(v.area,3) for k,v in PIECES87.items()}
checks['beams87']=len(BEAMS87);checks['wallbands87']=len(WALLBANDS87);checks['tops_clipped87']=CLIPPED87;checks['min_wall_top87']=min(min(b['zt']) for b in WALLBANDS87 if b['z1']==LV87['ztop']);checks['boards87']=len(BOARDS87)
# niches inside their wall pieces, clear of each other and of the corners
bad=[]
for n in NI87:
 fp=Polygon(n['foot']);pc=PIECES87[n['wall'] if n['wall']!='out' else 'outer']
 if fp.intersection(ROOM87).area>1e-4:bad.append(('niche_in_room',n['wall'],n['s_out']))
 others=[v for k,v in PIECES87.items() if k!=(n['wall'] if n['wall']!='out' else 'outer')]
 for o in others:
  if fp.intersection(o).area>1e-4:bad.append(('niche_in_other_piece',n['wall'],n['s_out']))
 if fp.intersection(pc).area<.5*fp.area:bad.append(('niche_outside_piece',n['wall'],n['s_out']))
for i,a in enumerate(NI87):
 for b in NI87[i+1:]:
  if Polygon(a['foot']).buffer(.25).intersects(Polygon(b['foot'])):bad.append(('niches_close',a['wall'],a['s_out'],b['wall'],b['s_out']))
for d in DOORS87:
 fp=Polygon(d['foot'])
 for n in NI87:
  if fp.buffer(.2).intersects(Polygon(n['foot'])):bad.append(('door_niche',d['name'],n['s_out']))
for side in ('court','out'):
 ns=sorted((n for n in NI76 if n['wall']==side),key=lambda n:n['u_in'])
 if ns[0]['u_in']-ns[0]['r_in']<A_S+.4 or ns[-1]['u_in']+ns[-1]['r_in']>A_N-.4:bad.append(('forb_niche_end',side))
 for a,b in zip(ns,ns[1:]):
  if a['u_in']+a['r_in']>b['u_in']-b['r_in']-.6:bad.append(('forb_niches_close',side,a['u_in'],b['u_in']))
fpn=FEAT76['hood']
for n in NI76:
 if n['wall']=='out' and abs(n['u_in']-fpn['a'])<n['r_in']+fpn['w']/2+.15:bad.append(('hood_niche',n['u_in']))
checks['problems']=bad
checks['niches87']=[(n['wall'],n['s_in'],n['s_out'],n['blind']) for n in NI87];checks['niches76']=[(n['wall'],n['u_in'],n['facade_SEe']) for n in NI76]
checks['olsson_plan_vs_facade']=dict(gron_court=list(zip(OLSSON['room87_se_frame']['court_windows_s'],FACADE['NW_court'][:4])),gron_outer_plan=OLSSON['room87_se_frame']['outer_windows_s'],gron_outer_facade=FACADE['NW_outer'])
# roof: pass 127's pieces (plane z = Ax+By+C; the joined roof is the upper envelope); underside 0.12 m
ROOF=[(Polygon(rr[0]),pc['plane']) for pc in B127['roof'] for rr in pc['rings']]
def roof_under(p):
 zs=[pl[0]*p[0]+pl[1]*p[1]+pl[2] for poly,pl in ROOF if poly.buffer(.05).contains(Point(p))]
 return (max(zs)-.12) if zs else None
def roof_min(poly):
 pts=list(poly.exterior.coords)
 dense=[];
 for p,q in zip(pts,pts[1:]):
  n=max(1,int(math.hypot(q[0]-p[0],q[1]-p[1])/.5))
  dense+=[(p[0]+(q[0]-p[0])*i/n,p[1]+(q[1]-p[1])*i/n) for i in range(n)]
 zs=[roof_under(p) for p in dense];zs=[z for z in zs if z is not None]
 return round(min(zs),3) if zs else None
checks['gron_roof_under_min_over_env']=roof_min(ENV87);checks['forb_roof_under_min_over_env']=roof_min(ENV76)
checks['gron_roof_under_min_over_room']=roof_min(ROOM87);checks['forb_roof_under_min_over_room']=roof_min(ROOM76)
# wall tops follow the roof where it comes lower than the ceiling's top (the courtyard backs)
assert all(checks[k]<.01 for k in checks if k.endswith('_m2') and ('outside_body' in k or 'in_court' in k or 'in_tower' in k or 'in_kure' in k or '_vs_' in k)),{k:v for k,v in checks.items() if k.endswith('_m2')}
assert not bad,bad
assert abs(checks['forb_width_m']-M76['inside_m'])<.05 and 10.9<min(checks['gron_widths_m']) and max(checks['gron_widths_m'])<11.6
assert checks['gron_roof_under_min_over_room']>LV87['ztop']+.3 and checks['forb_roof_under_min_over_room']>LV76['ztop']+.3,checks
assert ENV76.difference(BODY).area<.01 and ENV87.difference(BODY).area<.01

OUT=dict(source='pass 131: Möller 1882 (PK006-00041), Olsson 1974 fig. 1 (registered, read only), photographs (Commons, KMB/DigitaltMuseum); see references/block131-notes.md',
 moller=MOLLER,olsson=OLSSON,facade=FACADE,
 gron=dict(frame=dict(range='NW',origin=RG['NW']['origin'],u=U_NW,n=N_NW),sw=dict(origin=RG['SW']['origin'],u=U_SW,n=N_SW),levels=LV87,
  walls=dict(outer=TO87,court=TC87,s_e=S_E,s_eb=S_EB,sw_l=SW_L,sw_lb=SW_LB,c_end=C_END,c_endb=C_ENDB,r_arc=R_ARC,r_arcb=R_ARCB,tower=list(TWC)),
  room=[rnd(p) for p in clean(list(ROOM87.exterior.coords)[:-1])],env=ring(ENV87),pieces={k:ring(v) for k,v in PIECES87.items()},corners={k:rnd(v) for k,v in dict(A=A,B=B,C=C,LC=LC,D=D,E=E,F=F).items()},
  arc_room=[rnd(p) for p in ARC_ROOM],wallbands=WALLBANDS87,niches=NI87,doors=DOORS87,beams=BEAMS87,boards=BOARDS87,feat=FEAT87),
 forb=dict(frame=dict(origin=list(OF),u=list(UF),n=list(NF)),levels=LV76,room=dict(a_s=A_S,a_n=A_N,t_end=T_END,bci=BCI,boi=BOI,bcb=BCB,bo=[round(o26[0],4),round(o26[1],4),round(KO,6)]),
  walls=dict(outer_mid=checks['forb_walls_m']['outer_at_mid'],court=TC76),niches=NI76,doors=DOORS76,feat=FEAT76,env=ring(ENV76)),
 checks=checks)
(R/'source/block131.json').write_text(json.dumps(OUT,indent=1,ensure_ascii=False))
zones=dict(gron=dict(room=ring(ROOM87),envelope=ring(ENV87)),forb=dict(room=ring(ROOM76),envelope=ring(ENV76)))
(R/'previews/block131-zones.json').write_text(json.dumps(dict(**{'pass':131},rooms=zones,checks=checks),indent=1,ensure_ascii=False))
print(json.dumps({k:v for k,v in checks.items() if not k.startswith('niches') and k!='olsson_plan_vs_facade'},ensure_ascii=False))
print('BLOCK131_PREPARE_OK','gron',checks['gron_room_m2'],'m2',checks['gron_widths_m'],'forb',checks['forb_room_m2'],'m2',checks['forb_width_m'],'niches',len(NI87),len(NI76))
