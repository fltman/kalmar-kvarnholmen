"""Pass 135: Kalmar slott, portal G on the south range's courtyard front, and Kungsköket (room 43).

Portal G ('sydvästra portalen', Olsson, Fornvännen 1957: the south range's western courtyard portal,
fluted Doric columns, masks in the metopes, framing the walled-up south gate passage).
- Kalmar läns museum, 'Sydvästra portalen på Kalmar slott', 1960 (DigitaltMuseum 021017057393, PDM):
  seen nearly square on from the courtyard, with the west courtyard corner (its downpipe) at the right.
  Read on a 924 x 927 scan (no pixel is used): the front's vanishing point from the cornice and the
  pedestal bases (x 2343), the two column axes (x 245, 535), the frame's edges (185, 575), the arch
  opening at the face (273, 495), the window over the cornice (348-450) and the corner downpipe (765).
  A projective fit along the front (x = 2343 + A/(t - t*), t in column spacings) gives every position
  in column spacings; one column spacing is 2.80 m (the window over the portal on the model's 0.9-1.0 m
  middle row, and Street View 2014 pano 2's 3.7 m portal width as read by pass 133).
- Place: on the model's SW window column at s 10.27 (the photograph's window over the cornice stands
  on the portal's axis, as at Kyrkportalen). That is 4.20 m from the model's west courtyard corner
  (photograph 4.36 m from the corner downpipe); pass 133's grazing pano reading was s 8.6-9.2.

Kungsköket (Olsson's ground-floor room 43, 'bottenvåningen, östra längan').
- Which range: the museum's state-floor plan has '16. Salen över Kungsköket' beside '17. Förbrända
  salen' (pass 131, SE_e between the bays), on the far side of it from the south tower (15); the 1969
  captions name the room's west wall the courtyard side with two exits to the courtyard ('den nordliga
  utgången', 'den sydliga utgången', the southern one in the wall's middle part), the east wall 'the
  sea side', a stair in the north wall. Pass 27's SE_w range (between the south tower and bay1, Olsson's
  tower VII) has exactly two small arched courtyard doors (pass 129: 2.32 and 10.07 m from the bend), the
  southern one at the middle of the front. Olsson's compass is turned about 40 degrees from true (his
  south range is the model's SW), so SE_w's courtyard wall is his west wall. The kitchen is SE_w's
  ground floor; the hall over it (room 82/'16') is SE_w's upper floor, south of Förbrända salen.
- Heights: the 1969 photographs of the west wall (021017090101, -103) show two window rows, low
  windows and high windows just under the ceiling, and a few steps up into the exits. The model's
  SE_w courtyard front has exactly two lower rows (pass 127, measured on Street View 2014): sills 6.30
  (1.25 x 1.20) and 9.95 (1.25 x 1.15). Read as fractions of the floor-to-ceiling height on the far
  wall (090101: sills 0.18 / 0.74; 090103: 0.15 / 0.70), the floor is at z 5.1-5.3 and the ceiling at
  z 11.6-11.9. Pass 127 also measured SE_w's upper row 1.3 m higher than the other ranges (sill 12.9).
  Built: floor z 5.10 (three risers of 0.127 down from the courtyard), joists' underside z 11.18,
  board ceiling z 11.43-11.55 (under the facade's state-floor row, sill 11.57). This is above the
  state-floor slab of the other ranges (z 10.17); SE_w has no upper room in the model.
- The room (photographs 021017090083-090103, 1969, PDM; S. Lindegren's sketches 021017083364/-365):
  whitewashed rubble and brick walls, a board ceiling on dense joists, cobbles; a great hearth: a
  square brick stack with arched openings on its faces and a tapering hood, standing under the wide
  arch of a cross wall ('mellanväggens valv'); a smaller arched fireplace with a hood in the south
  wall's west part; deep window niches; a drain ('trumma') along the north wall; a stair in the north
  wall. Positions along the room are estimated from the photographs; the window niches follow the
  facade's glass as the saved scene has it (SCR/p135/dump135.py).

Output: source/block135.json, previews/block135-zones.json.
Run with Shapely: KALMAR_GEO=<site-packages> python3 scripts/prepare_block135.py
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
RG={r['name']:r for r in CA['ranges']}
def Wr(name,s,c):r=RG[name];o,u,n=r['origin'],r['u'],r['n'];return (o[0]+u[0]*s+n[0]*c,o[1]+u[1]*s+n[1]*c)
def Fr(name,p):r=RG[name];o,u,n=r['origin'],r['u'],r['n'];dx,dy=p[0]-o[0],p[1]-o[1];return (dx*u[0]+dy*u[1],dx*n[0]+dy*n[1])
def W(s,c):return Wr('SE_w',s,c)
def F(p):return Fr('SE_w',p)
def rnd(p,k=4):return [round(p[0],k),round(p[1],k)]
def clean(coords,tol_ang=.5,tol_len=.002):
 # Drop near-duplicate points, spikes and nearly straight corners (one bad vertex stops the town bevel; pass 131).
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
def ring(poly):
 g=poly.simplify(.001,preserve_topology=True)
 g=Polygon(g.exterior.coords) if g.exterior.is_ccw else Polygon(list(g.exterior.coords)[::-1])
 return [rnd(p) for p in clean(list(g.exterior.coords)[:-1])]
def rings(g):
 # Every polygon of a (multi)polygon, as clean counter-clockwise rings; holes are not allowed.
 out=[]
 for q in ([g] if g.geom_type=='Polygon' else list(getattr(g,'geoms',[]))):
  if q.geom_type!='Polygon' or q.area<1e-4:continue
  assert not list(q.interiors),('hole in a wall band',q.area)
  out.append(ring(q))
 return out
ZC=B127['zc'];FL=B127['floor'];CI=[tuple(p) for p in CA['court']]
CO=Polygon(CA['outer']);CP=Polygon(CA['court']);BODY=CO.difference(CP)

# ================================================================= Kungsköket, in pass 27's SE_w frame (s along, c outwards)
P2,P3=F(CI[2]),F(CI[3])                                   # the courtyard line CI2 -> CI3
OUT0=F(tuple(CA['outer'][22]));OUT1=F(tuple(CA['outer'][23]))  # the outer line: SE_w's corner by the south tower -> bay1's corner
assert abs(OUT0[0])<1e-3 and abs(OUT1[0]-18.047)<.01,(OUT0,OUT1)
def cl(s):return P2[1]+(P3[1]-P2[1])*(s-P2[0])/(P3[0]-P2[0])      # courtyard line (the skin's back) at s
def ol(s):return OUT0[1]+(OUT1[1]-OUT0[1])*(s-OUT0[0])/(OUT1[0]-OUT0[0])  # outer line (the skin's back) at s
T_CW,T_OW=2.00,2.30              # courtyard and outer walls (Möller's ground floor under Brända salen: 1.4-1.9 m plus the model's deeper range)
S_SB,S_S,S_N,S_NB=0.60,1.80,18.40,19.60   # south wall back / face, north wall face / back
RISE=round((ZC+.012-5.10)/3,4);ZF=round(ZC+.012-3*RISE,3) # floor three risers below the threshold (z 5.10)
ZB=round(ZF-.30,3);Z_JU=11.18;Z_BU=11.43;Z_TOP=11.55     # base, joists' underside, boards, wall tops
def cface(s):return cl(s)+T_CW
def oface(s):return ol(s)-T_OW
def Q(pts):return Polygon([W(s,c) for s,c in pts])
def band(s0,s1,f0,f1):
 # A quad between two lines given as functions of s (or constants), from s0 to s1.
 g0=f0 if callable(f0) else (lambda s,v=f0:v);g1=f1 if callable(f1) else (lambda s,v=f1:v)
 return Q([(s0,g0(s0)),(s1,g0(s1)),(s1,g1(s1)),(s0,g1(s0))])
ROOM=band(S_S,S_N,cface,oface)
TOWERS=unary_union([Point(t['centre']).buffer(t['radius']+.36,128) for t in CA['towers'].values()])
B133=json.loads((R/'source/block133.json').read_text())
def SWp(s,c):f=B133['frame'];return (f['origin'][0]+f['u'][0]*s+f['n'][0]*c,f['origin'][1]+f['u'][1]*s+f['n'][1]*c)
ENV133=unary_union([Polygon(B133['env13']),Polygon(B133['hall'])])
ENV130=Polygon([SWp(B130['room']['s_w']-B130['room']['t_w'],B130['room']['c_co']),SWp(B133['stair']['s_room0'],B130['room']['c_co']),SWp(B133['stair']['s_room0'],B130['room']['c_oo']),SWp(B130['room']['s_w']-B130['room']['t_w'],B130['room']['c_oo'])])
BAYS=unary_union([Polygon(b['polygon']) for b in CA['bays']])
# The corner by the south courtyard corner belongs to pass 133's stair hall and pass 130's chapel (above
# z 10.17); the kitchen's walls stop 0.05 m short of them, and of the towers and bay1.
ENV=band(S_SB,S_NB,lambda s:cl(s)+.0,lambda s:ol(s)-.0).difference(unary_union([TOWERS,BAYS,ENV133.buffer(.05,join_style=2),ENV130.buffer(.05,join_style=2)]))
ENV=max(getattr(ENV,'geoms',[ENV]),key=lambda q:q.area)
PIECES=dict(court=band(S_SB,S_NB,lambda s:cl(s)+.02,cface),outer=band(S_SB,S_NB,oface,lambda s:ol(s)-.02),
 south=band(S_SB,S_S,cface,oface),north=band(S_N,S_NB,cface,oface))
PIECES={k:v.intersection(ENV) for k,v in PIECES.items()}
for k,v in PIECES.items():assert v.geom_type=='Polygon',(k,v.geom_type)

# ---------------------------------------------------------------- openings
# The two courtyard exits (pass 129's arched doors on CI3-CI2), drawn open in the facade by this pass.
def edge_pt(i,j,u):
 p,q=CI[i],CI[j];L=math.dist(p,q);m=((p[0]+q[0])/2,(p[1]+q[1])/2);return (m[0]+(q[0]-p[0])/L*u,m[1]+(q[1]-p[1])/L*u)
EXITS=[]
for d in B129['doors']['3,2']:
 s,c=F(edge_pt(3,2,d[0]));EXITS.append(dict(name='north' if s>12 else 'south',hole=d,s=round(s,3),w=d[2],crown=round(d[1]+d[3]+d[4],3)))
EXITS.sort(key=lambda e:e['s'])
NW_DOOR=1.35;Z_DOORHEAD=8.00
# Window niches on the facade's glass (SM_Kalmar_Slott, read from the saved scene: SCR/p135/dump.json).
WIN_COURT=[(2.45,6.30,7.50),(6.25,6.30,7.50),(13.84,6.30,7.50),(2.45,9.95,11.10),(6.25,9.95,11.10),(10.05,9.95,11.10),(13.84,9.95,11.10),(17.64,9.95,11.10)]
WIN_OUT=[(4.02,8.52,9.72),(9.02,8.52,9.72),(14.01,8.52,9.72)]
WCW,WOW=1.25,0.62
CUTS=[]   # (wall piece, footprint, z0, z1, kind)
NICHES=[]
for s,z0,z1 in WIN_COURT:
 hb,hf=WCW/2+.05,WCW/2+.35
 g=Q([(s-hb,cl(s-hb)+.0),(s+hb,cl(s+hb)+.0),(s+hf,cface(s+hf)+.03),(s-hf,cface(s-hf)+.03)])
 CUTS.append(('court',g,round(z0-.02,3),round(min(z1+.10,Z_JU-.03),3),'window'));NICHES.append(dict(wall='court',s=s,w=WCW,sill=z0,head=z1,niche=[round(z0-.02,3),round(min(z1+.10,Z_JU-.03),3)]))
for s,z0,z1 in WIN_OUT:
 hb,hf=WOW/2+.05,WOW/2+.40
 g=Q([(s-hb,ol(s-hb)-.0),(s+hb,ol(s+hb)-.0),(s+hf,oface(s+hf)-.03),(s-hf,oface(s-hf)-.03)])
 CUTS.append(('outer',g,round(z0-.02,3),round(z1+.15,3),'window'));NICHES.append(dict(wall='outer',s=s,w=WOW,sill=z0,head=z1,niche=[round(z0-.02,3),round(z1+.15,3)]))
for e in EXITS:
 s=e['s'];g=Q([(s-NW_DOOR/2,cl(s-NW_DOOR/2)-.0),(s+NW_DOOR/2,cl(s+NW_DOOR/2)-.0),(s+NW_DOOR/2,cface(s+NW_DOOR/2)+.03),(s-NW_DOOR/2,cface(s-NW_DOOR/2)+.03)])
 CUTS.append(('court',g,ZF,Z_DOORHEAD,'door'))
# The stair in the north wall (Selling 1969: 'Spisen, östra väggen (från trappan i Norra muren)'), by the east corner.
STAIR=dict(c0=round(oface(S_N)-1.70,3),c1=round(oface(S_N)-.60,3),n=4,rise=.18,tread=.25,door_s=19.40)
CUTS.append(('north',band(S_N-.03,STAIR['door_s'],STAIR['c0'],STAIR['c1']),ZF,round(ZF+STAIR['n']*STAIR['rise']+2.20,3),'stair'))

# ---------------------------------------------------------------- the cross wall, the great hearth, the small fireplace
SA=11.95;TA=1.00                 # the cross wall's middle and thickness (between the window columns 10.05 and 13.84)
CA0=round(cface(SA)+1.20,3);CA1=round(oface(SA)-1.20,3)   # the arch opening, 1.2 m piers
ARCH=dict(s0=round(SA-TA/2,3),s1=round(SA+TA/2,3),c0=CA0,c1=CA1,spring=round(ZF+1.80,3),crown=round(ZF+4.60,3),cw0=round(cface(SA)-.30,3),cw1=round(oface(SA)+.30,3))
_hw=(CA1-CA0)/2;_rise=ARCH['crown']-ARCH['spring'];ARCH['R']=round((_hw*_hw+_rise*_rise)/(2*_rise),4);ARCH['zo']=round(ARCH['crown']-ARCH['R'],4)
CH=round((CA0+CA1)/2,3)
HEARTH=dict(s=SA,c=CH,hs=1.50,hc=1.80,t=.50,top=round(ZF+2.60,3),plinth=.30,zp=round(ZF+.12,3),
 arches_sn=[[-1.35,-.25],[.25,1.35]],arch_ew=[-.60,.60],spring=round(ZF+1.25,3),spring_ew=round(ZF+1.20,3),
 hood_top=round(ARCH['crown']-.16,3),hood_hs=.50,hood_hc=.75,bed=round(ZF+.40,3))
FIRE=dict(c=round(cface(S_S)+2.00,3),hc=1.40,d=1.00,top=round(ZF+2.40,3),open=[-.80,.80],spring=round(ZF+1.00,3),flue_hc=.60,flue_d=.40)
DRAIN=dict(s0=round(S_N-.50,3),s1=S_N,c0=round(cface(S_N)+.30,3),c1=round(STAIR['c0']-.30,3),z=round(ZF-.12,3))
JOISTS=[round(S_S+.45+k*.90,3) for k in range(int((S_N-S_S-.6)/.90)+1) if S_S+.45+k*.90<S_N-.3]

# ---------------------------------------------------------------- the wall pieces in horizontal bands
zs=sorted({ZB,Z_TOP}|{c[2] for c in CUTS}|{c[3] for c in CUTS})
BANDS=[]
for z0,z1 in zip(zs,zs[1:]):
 for name,g in PIECES.items():
  cut=[c[1] for c in CUTS if c[0]==name and c[2]<=z0+1e-6 and c[3]>=z1-1e-6]
  rest=g.difference(unary_union(cut)) if cut else g
  for r_ in rings(rest):BANDS.append(dict(piece=name,z0=z0,z1=z1,ring=r_))
# Door niches: landing and two treads down to the floor (along c from the skin's back).
STEPS=[]
for e in EXITS:
 s=e['s'];h=NW_DOOR/2
 def seg(a,b,s=s,h=h):return Q([(s-h+.02,cl(s-h)+a),(s+h-.02,cl(s+h)+a),(s+h-.02,cl(s+h)+b),(s-h+.02,cl(s-h)+b)])
 STEPS.append(dict(door=e['name'],top=round(ZC+.012,3),ring=ring(seg(-.03,.90))))
 STEPS.append(dict(door=e['name'],top=round(ZF+2*RISE,3),ring=ring(seg(.90,1.20))))
 STEPS.append(dict(door=e['name'],top=round(ZF+RISE,3),ring=ring(seg(1.20,1.50))))
 STEPS.append(dict(door=e['name'],top=ZF,ring=ring(seg(1.50,T_CW+.05))))
FLOOR=ROOM.difference(band(DRAIN['s0'],DRAIN['s1'],DRAIN['c0'],DRAIN['c1']))

# ---------------------------------------------------------------- the walk route (frame points)
ROUTE=[]
# From the gate passage's courtyard end: west of the well house (pass 124), then to the south exit.
WELL=F(tuple(CA['well']));ROUTE.append((round(WELL[0]-6.0,3),round(WELL[1],3)))
for e in [x for x in EXITS if x['name']=='south']:ROUTE+=[(e['s'],round(cl(e['s'])-3.0,3)),(e['s'],round(cl(e['s'])-1.6,3)),(e['s'],round(cl(e['s'])+.3,3)),(e['s'],round(cface(e['s'])+.8,3))]
ROUTE+=[(6.0,-7.0),(4.5,-5.2),(9.0,-3.6),(SA,-3.75),(15.5,-4.2),(15.6,-9.6),(SA,round((CA0+CH-HEARTH['hc']-HEARTH['plinth'])/2,3)),(9.0,-9.9)]
for e in [x for x in EXITS if x['name']=='north']:ROUTE+=[(16.2,-9.8),(e['s'],round(cface(e['s'])+.8,3)),(e['s'],round(cl(e['s'])+.3,3)),(e['s'],round(cl(e['s'])-1.6,3))]

# ================================================================= portal G on the SW courtyard front (CI2 -> CI1)
def WS(s,c):return Wr('SW',s,c)
def FS(p):return Fr('SW',p)
S_C2,S_C1,S_C0=FS(CI[2])[0],FS(CI[1])[0],FS(CI[0])[0]
S_MID=(S_C2+S_C1)/2;L21=math.dist(CI[2],CI[1])
# The 1960 photograph, positions along the front in column spacings t (left column 0, right column 1;
# the photograph's left is towards the south corner, +s): x = 2343 + A/(t - t*), A = -13080, t* = -6.234.
def tph(x):return -6.234+(-13080)/(x-2343)
PH=dict(frame=[tph(185),tph(575)],cols=[tph(245),tph(535)],opening=[tph(273),tph(495)],window=[tph(348),tph(450)],corner=tph(765),right_window=[tph(590),tph(695)])
UNIT=2.80                        # one column spacing in metres
G_S=10.27                        # the model's SW window column (lower and middle rows)
U_G=round(S_MID-G_S,3)
G=dict(s=G_S,u=U_G,unit=UNIT,width=round((PH['frame'][1]-PH['frame'][0])*UNIT,2),col_u=1.40,col_r=.17,
 plinth=.20,ped=[.20,1.05],ped_cap=[1.05,1.17],ped_w=.80,col=[1.17,3.53],arch_t=[3.53,3.73],frieze=[3.73,4.11],cornice=[4.11,4.40],top=4.40,
 open_w=2.10,open_h=2.00,open_r=1.05,recess=.30,infill=.30,triglyphs=9)
G['corner_from_axis_photo']=round((PH['corner']-.5)*UNIT,2);G['corner_from_axis_model']=round(G_S-S_C0,2)
DOOR_G=[U_G,ZC,G['open_w'],G['open_h'],G['open_r']]
G_LINE=FS(edge_pt(2,1,U_G))[1]

# ================================================================= checks
checks=dict(kitchen={},portal_g={})
K=checks['kitchen']
K['floor_z']=ZF;K['rise']=RISE;K['room_area_m2']=round(ROOM.area,2)
K['room_width_south_north']=[round(oface(S_S)-cface(S_S),2),round(oface(S_N)-cface(S_N),2)];K['room_length']=round(S_N-S_S,2)
K['ceiling']=[Z_JU,Z_BU,Z_TOP];K['state_row_sill_over_ceiling_top']=round(B126['court_row']['sill']-Z_TOP,3)
K['exits_s']=[(e['name'],e['s'],e['crown']) for e in EXITS]
K['env_outside_body_m2']=round(ENV.difference(BODY).area,4);K['env_in_court_m2']=round(ENV.intersection(CP).area,4)
for k,t in CA['towers'].items():K[f'env_in_tower_{k}_m2']=round(ENV.intersection(Point(t['centre']).buffer(t['radius']+.36,128)).area,4)
for k,b in enumerate(CA['bays']):K[f'env_in_{b["name"]}_m2']=round(ENV.intersection(Polygon(b['polygon'])).area,4)
FORB=Polygon(B131['forb']['env']);GRON=Polygon(B131['gron']['env'])
def w125(s,c):f=B125['frame'];return (f['origin'][0]+f['u'][0]*s+f['n'][0]*c,f['origin'][1]+f['u'][1]*s+f['n'][1]*c)
R125=unary_union([Polygon([w125(r['s0'],r['c0']),w125(r['s1'],r['c0']),w125(r['s1'],r['c1']),w125(r['s0'],r['c1'])]) for r in B125['rooms'].values()])
st=B126['stair'];E_,IN_=st['E'],st['IN'];W1=st['W1']
def w126(a,b):return (W1[0]+E_[0]*a+IN_[0]*b,W1[1]+E_[1]*a+IN_[1]*b)
R126=Polygon([w126(st['a_end']-1,-1),w126(30,-1),w126(30,8),w126(st['a_end']-1,8)])
for nm,g in (('pass125',R125),('pass126',R126),('pass131_grona',GRON),('pass131_forbranda',FORB),('pass133_stair',ENV133),('pass130_chapel',ENV130)):
 K[f'env_vs_{nm}_m2']=round(ENV.intersection(g).area,4);K[f'dist_{nm}_m']=round(ENV.distance(g),2)
# Every niche and door in its own wall piece, clear of the others and of the cross wall, the hearth and the fireplace.
ARCHP=band(ARCH['s0'],ARCH['s1'],ARCH['cw0'],ARCH['cw1'])
HEARTHP=band(SA-HEARTH['hs']-HEARTH['plinth'],SA+HEARTH['hs']+HEARTH['plinth'],CH-HEARTH['hc']-HEARTH['plinth'],CH+HEARTH['hc']+HEARTH['plinth'])
FIREP=band(S_S,S_S+FIRE['d'],FIRE['c']-FIRE['hc'],FIRE['c']+FIRE['hc'])
opens=[(c[0],c[1],c[2],c[3]) for c in CUTS]
bad=[]
for i,(p1,g1,a1,b1) in enumerate(opens):
 if g1.difference(PIECES[p1].buffer(.06)).area>.01:bad.append(('outside_piece',i,round(g1.difference(PIECES[p1]).area,3)))
 for j,(p2,g2,a2,b2) in enumerate(opens[:i]):
  if a1<b2 and a2<b1 and g1.buffer(.15).intersects(g2):bad.append(('openings_meet',i,j))
 if g1.intersects(ARCHP):bad.append(('opening_in_cross_wall',i))
 if g1.intersects(FIREP.buffer(.2)):bad.append(('opening_at_fireplace',i))
K['bad']=bad
K['hearth_in_arch']=CA0<CH-HEARTH['hc']-HEARTH['plinth'] and CH+HEARTH['hc']+HEARTH['plinth']<CA1
def arch_z(c):x=c-CH;return ARCH['zo']+math.sqrt(max(0,ARCH['R']**2-x*x))
K['hood_under_arch']=all(arch_z(CH+sg*hc)>z+.05 for sg in (-1,1) for hc,z in ((HEARTH['hc'],HEARTH['top']),(HEARTH['hood_hc'],HEARTH['hood_top'])))
K['passages_by_hearth_m']=[round((CH-HEARTH['hc']-HEARTH['plinth'])-CA0,2),round(CA1-(CH+HEARTH['hc']+HEARTH['plinth']),2)]
K['headroom_east_passage_m']=round(arch_z(-3.75)-ZF,2)
K['room_in_env']=ROOM.difference(ENV).area<1e-6
K['joists']=len(JOISTS)
K['steps_rise']=RISE;K['niche_count']=len(NICHES)
K['route_in_room_or_niches']=all(ROOM.buffer(.01).contains(Point(W(s,c))) or any(Polygon(st_['ring']).buffer(.02).contains(Point(W(s,c))) for st_ in STEPS) or not ENV.contains(Point(W(s,c))) for s,c in ROUTE)
PIERS=ARCHP.difference(band(ARCH['s0']-.1,ARCH['s1']+.1,CA0,CA1))
K['route_clear_of_piers']=not any(PIERS.buffer(.3).contains(Point(W(s,c))) for s,c in ROUTE)
K['route_clear_of_hearth_and_drain']=not any(HEARTHP.contains(Point(W(s,c))) or band(DRAIN['s0'],DRAIN['s1'],DRAIN['c0'],DRAIN['c1']).contains(Point(W(s,c))) for s,c in ROUTE)
Gc=checks['portal_g'];Gc.update(photo_t={k:([round(x,3) for x in v] if isinstance(v,list) else round(v,3)) for k,v in PH.items()})
Gc['width_m']=G['width'];Gc['opening_m']=round((PH['opening'][1]-PH['opening'][0])*UNIT,2);Gc['window_m']=round((PH['window'][1]-PH['window'][0])*UNIT,2)
Gc['axis_from_corner_photo_m']=G['corner_from_axis_photo'];Gc['axis_from_corner_model_m']=G['corner_from_axis_model']
Gc['portal_edges_s']=[round(G_S-G['width']/2,2),round(G_S+G['width']/2,2)];Gc['edge_s']=[round(S_C1,3),round(S_C2,3)]
Gc['door_in_edge']=abs(U_G)+G['open_w']/2<L21/2-.3
Gc['portal_on_front']=G_S-G['width']/2>S_C0+.2
Gc['clear_of_kyrkportalen_m']=round((B133['portal']['s']-B133['portal']['width']/2)-(G_S+G['width']/2),2)
Gc['window_over_top_m']=round(9.90-(ZC+G['top']),3)
# The recess behind the arch (portal G's blind infill) inside the SW range's body, clear of the other rooms.
REC=Polygon([WS(G_S-G['open_w']/2-.30,G_LINE-.02),WS(G_S+G['open_w']/2+.30,G_LINE-.02),WS(G_S+G['open_w']/2+.30,G_LINE+G['recess']+G['infill']),WS(G_S-G['open_w']/2-.30,G_LINE+G['recess']+G['infill'])])
Gc['recess_outside_body_m2']=round(REC.difference(CO).area,4);Gc['recess_vs_grona_m2']=round(REC.intersection(GRON).area,4)
Gc['recess_vs_pass133_m2']=round(REC.intersection(ENV133).area,4)
assert not bad,bad
assert K['env_outside_body_m2']<.01 and K['env_in_court_m2']<.01,K
assert all(K[f'env_in_tower_{k}_m2']<.01 for k in CA['towers']) and all(K[f'env_in_{b["name"]}_m2']<.01 for b in CA['bays']),K
assert all(K[k]==0 for k in K if k.startswith('env_vs_')),K
assert K['hearth_in_arch'] and K['hood_under_arch'] and min(K['passages_by_hearth_m'])>1.2 and K['headroom_east_passage_m']>2.2,K
assert K['room_in_env'] and K['route_in_room_or_niches'] and K['route_clear_of_hearth_and_drain'] and K['route_clear_of_piers'],K
assert K['state_row_sill_over_ceiling_top']>0,K
assert len(EXITS)==2 and EXITS[0]['name']=='south' and EXITS[1]['name']=='north'
assert Gc['door_in_edge'] and Gc['portal_on_front'] and Gc['clear_of_kyrkportalen_m']>3 and 0<Gc['window_over_top_m']<.1,Gc
assert Gc['recess_outside_body_m2']<.001 and Gc['recess_vs_grona_m2']==0 and Gc['recess_vs_pass133_m2']==0,Gc

OUT=dict(source='pass 135: DigitaltMuseum (Kalmar läns museum) 021017057393 (1960) and 021017090083-090103, 083364-365 (1969), PDM, viewed; Olsson 1957 (read only); museum state-floor plan (viewed); passes 27, 127, 129, 131, 133. See references/block135-notes.md',
 frame=dict(range='SE_w',origin=RG['SE_w']['origin'],u=RG['SE_w']['u'],n=RG['SE_w']['n']),zc=ZC,
 kitchen=dict(zf=ZF,zb=ZB,rise=RISE,z_ju=Z_JU,z_bu=Z_BU,z_top=Z_TOP,s=[S_SB,S_S,S_N,S_NB],t_cw=T_CW,t_ow=T_OW,
  cl=[list(P2),list(P3)],ol=[list(OUT0),list(OUT1)],room=ring(ROOM),env=ring(ENV),floor=ring(FLOOR),pieces={k:ring(v) for k,v in PIECES.items()},
  bands=BANDS,steps=STEPS,exits=EXITS,door_niche_w=NW_DOOR,door_head=Z_DOORHEAD,niches=NICHES,
  stair=STAIR,arch=ARCH,hearth=HEARTH,fire=FIRE,drain=DRAIN,joists=JOISTS,route=ROUTE),
 portal_g=dict(G,door=DOOR_G,edge=[2,1],line_c=round(G_LINE,4),photo=PH,sw=dict(origin=RG['SW']['origin'],u=RG['SW']['u'],n=RG['SW']['n'])),
 open_doors=[list(e['hole']) for e in EXITS]+[DOOR_G],
 checks=checks)
(R/'source/block135.json').write_text(json.dumps(OUT,indent=1,ensure_ascii=False))
(R/'previews/block135-zones.json').write_text(json.dumps({'pass':135,'zones':dict(kitchen_room=ring(ROOM),kitchen_envelope=ring(ENV),cross_wall=ring(ARCHP),hearth=ring(HEARTHP),fireplace=ring(FIREP),
 portal_g=ring(Polygon([WS(G_S-G['width']/2,G_LINE-1.0),WS(G_S+G['width']/2,G_LINE-1.0),WS(G_S+G['width']/2,G_LINE),WS(G_S-G['width']/2,G_LINE)])),portal_g_recess=ring(REC)),'checks':checks},indent=1,ensure_ascii=False))
print(json.dumps(checks,indent=0,ensure_ascii=False)[:5000])
print('BLOCK135_PREPARE_OK','kitchen',round(ROOM.area,1),'m2 floor',ZF,'bands',len(BANDS),'niches',len(NICHES),'portal G s',G_S,'u',U_G,'width',G['width'])
