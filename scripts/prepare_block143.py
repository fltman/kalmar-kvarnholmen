"""Pass 143: two more state-floor interiors of Kalmar slott, in the queen's apartment (Drottningvåningen)
of the north range (pass 27's 'NE' range, between the north round tower N = Olsson's II, Kungsmakstornet,
and the east round tower E = Olsson's V, Fångetornet).
- Rutsalen: Olsson's room 63 ('Chequer Hall'), Möller 1882: 'Profil genom s.k. "Rut-salen"' (No. 63).
- Drottningsalen: Olsson's room 65, east of 63, towards Drottningtrappan (66) and Norra trapptornet (IV).

Which range (Olsson 1974, Fornvännen 69, fig. 1 and text, read only, in copyright):
- Olsson's 'norra längan' runs from tower II to tower V. Pass 131's registration of the plan to the four
  round towers (11.47 px/m) maps it on pass 27's NE range (outward normal true 40). Pass 131's 'Gröna
  salen in NW' is Olsson's west range; the model's 'NW' range is Olsson's west range, its 'NE' range is
  Olsson's north range. The plan, rectified into the NE frame (SCR/p143/pz.png), reads:
  room 63 between s ~18.0 and ~27.2 (its west wall skewed, s 26.3-28.0), room 65 between s ~6.2 and ~16.9,
  the 63/65 wall s 16.9-18.1; outer faces c -5.0 (63) and -5.8 (65); courtyard faces c ~-15.0; three
  courtyard windows in each room (63: s ~19.7, 22.9, 25.9; 65: ~8.0, 11.7, 15.3).
- Olsson's text: 'Både Drottningsalen nr 65 och Rutsalen nr 63 har tre stora fönster vardera mot
  borggården'; 63 measures '11 x 10,5 m'; tower III (Vattentornet) 'ingår med hela sin södra vägg i
  Rutsalens norra vägg'; 63's east wall (to 65) is 'av normal tjocklek, i huvudvåningen 45 cm'.

Heights and widths (Möller, 'Calmar slott. Profiler', 1882, PK006-00041, public domain; the caption reads
'Profil genom s.k. "Rut-salen" (N:o 63 å planen af öfre våningen)'; the 90-fot bar reads 57.95 px/m
(0-90) / 57.70 (40-90), pass 127's 57.97 is kept; floor = his red state-floor line, row 9926; the
'Gård' annotation and the courtyard ground row 10254 are on the left, so the left wall is the courtyard
wall, as pass 127 read it):
- courtyard wall x 3345-3417 (1.24 m), hall 3417-4044 (10.82 m), spine wall 4044-4188 (2.48 m), outer
  rooms 4188-4483 (5.09 m, a later addition; their own floors), outer wall 4483-4528 (0.78 m): 20.41 m.
- the hall's ceiling: whitewashed boards ('hvitlimmad underpanel') under the joists, underside row 9562
  (6.28 m), top row 9538 (6.69 m).
- the courtyard window niche reaches the floor; glass sill row 9858 (1.17 m), glass head 9712 (3.69 m),
  niche head at the room face 9700 (3.90 m), sloping to the glass.
- opposite it a deep niche in the spine wall: head 9700 (3.90 m) at the room face, 9716 (3.62 m) at its
  back (x 4170, 2.18 m deep), with a door 1.90 m high (rows 9795-9905) through the last 0.30 m of the
  wall into the outer rooms; a rail or bench drawn inside it (rows 9800-9845) is not built.
- 'Det rika boiseriet', the panelling, to row 9750 (3.04 m). 'Parkettgolf: fullgodt skick'.
The model's range is deeper (22.5 m skin to skin at s 22) than Möller's 20.41 m; as in pass 131 the hall
keeps Möller's inside width and the excess is shared between the two outer walls, so the courtyard wall
takes half of it; the spine wall keeps Möller's 2.48 m. Behind the spine wall the model has no rooms.

Window niches sit on the facade's windows as the saved scene has them (SM_Kalmar_Slott glass, read with
SCR/p143/dump143.py on a copy of source/Stortorget.blend saved after pass 141's build).

Output: source/block143.json (frame, levels, rooms, walls, niches, doors, features, checks),
previews/block143-zones.json. Run with Shapely: KALMAR_GEO=<site-packages> python3 scripts/prepare_block143.py
"""
from pathlib import Path
import json,math,os,sys
if os.environ.get('KALMAR_GEO'):sys.path.insert(0,os.environ['KALMAR_GEO'])
from shapely.geometry import Polygon,Point,LineString
from shapely.ops import unary_union
R=Path(__file__).resolve().parents[1]
C27=json.loads((R/'source/castle27.json').read_text());CA=C27['castle']
B125=json.loads((R/'source/block125.json').read_text());B126=json.loads((R/'source/block126.json').read_text())
B127=json.loads((R/'source/block127.json').read_text());B130=json.loads((R/'source/block130.json').read_text())
B131=json.loads((R/'source/block131.json').read_text());B135=json.loads((R/'source/block135.json').read_text())
RG={r['name']:r for r in CA['ranges']}
def rnd(p,k=4):return [round(p[0],k),round(p[1],k)]
def ring(poly):return [rnd(p) for p in list(poly.exterior.coords)[:-1]]
def unit(v):L=math.hypot(*v);return (v[0]/L,v[1]/L)
def Wr(name,s,c):r=RG[name];o,u,n=r['origin'],r['u'],r['n'];return (o[0]+u[0]*s+n[0]*c,o[1]+u[1]*s+n[1]*c)
def Fr(name,p):r=RG[name];o,u,n=r['origin'],r['u'],r['n'];dx,dy=p[0]-o[0],p[1]-o[1];return (dx*u[0]+dy*u[1],dx*n[0]+dy*n[1])
FL=B127['floor'];Z0=round(FL-.30,3)

# ---------------------------------------------------------------- sources
MOLLER=dict(px_per_m=57.97,bar_check_px_per_m=[57.95,57.70],caption='Profil genom s.k. "Rut-salen" (N:o 63 å planen af öfre våningen)',
 floor_row=9926,x_court_out=3345,x_court_in=3417,x_spine_in=4044,x_spine_out=4188,x_outer_in=4483,x_outer_out=4528,
 ceiling_under_row=9562,ceiling_top_row=9538,glass_sill_row=9858,glass_head_row=9712,niche_head_room_row=9700,
 spine_niche_head_rows=[9700,9716],spine_niche_back_x=4170,spine_door_rows=[9795,9905],panel_top_row=9750,ground_court_row=10254)
P=MOLLER['px_per_m'];M=MOLLER
def hm(r):return round((M['floor_row']-r)/P,2)
def wm(a,b):return round(abs(a-b)/P,2)
MREAD=dict(court_wall=wm(M['x_court_out'],M['x_court_in']),hall=wm(M['x_court_in'],M['x_spine_in']),spine_wall=wm(M['x_spine_in'],M['x_spine_out']),
 outer_rooms=wm(M['x_spine_out'],M['x_outer_in']),outer_wall=wm(M['x_outer_in'],M['x_outer_out']),depth=wm(M['x_court_out'],M['x_outer_out']),
 ceiling=hm(M['ceiling_under_row']),ceiling_top=hm(M['ceiling_top_row']),glass=[hm(M['glass_sill_row']),hm(M['glass_head_row'])],niche_head_room=hm(M['niche_head_room_row']),
 spine_niche_head=[hm(r) for r in M['spine_niche_head_rows']],spine_niche_depth=wm(M['x_spine_in'],M['spine_niche_back_x']),spine_door_h=round((M['spine_door_rows'][1]-M['spine_door_rows'][0])/P,2),
 panel=hm(M['panel_top_row']),floor_above_court_ground=round((M['ground_court_row']-M['floor_row'])/P,2))
MOLLER['read_m']=MREAD
OLSSON=dict(read='Fornvännen 69 (1974) fig. 1, pass 131 registration (SCR/p131/reg.json), rectified into the NE frame (SCR/p143/pz.png); ±1 m',
 room63_NE=dict(s=[18.0,27.2],west_wall_skew_s=[26.3,28.0],outer_face_c=-5.0,court_face_c=-15.0,court_windows_s=[19.7,22.9,25.9]),
 room65_NE=dict(s=[6.2,16.9],outer_face_c=-5.8,court_face_c=-15.0,court_windows_s=[8.0,11.7,15.3],outer_windows_s=[8.2,13.9]),
 wall_63_65_NE_s=[16.9,18.1],text=dict(room63_m=[11,10.5],wall_63_65_m=.45,court_windows_each=3))
# facade windows read from the saved scene (SCR/p143/dump.json, M_Town_Glass, NE frame s, c)
FACADE=dict(read='SM_Kalmar_Slott glass, saved scene after pass 141, SCR/p143/dump143.py',
 NE_court=[(0.64,-18.606),(5.94,-18.645),(9.74,-18.675),(13.54,-18.705),(19.15,-18.748),(22.95,-18.777),(26.75,-18.806)],w=1.20,state_z=[11.57,14.77],
 NE_outer_state=[1.82,6.17,10.53,14.88,19.24,23.60],note='the outer front state row lights the space behind the spine wall (no rooms built)')

# ---------------------------------------------------------------- frame: along NE's courtyard outline
CI=[tuple(p) for p in CA['court']];CO=[tuple(p) for p in CA['outer']]
p6,p8=CI[6],CI[8];U=unit((p8[0]-p6[0],p8[1]-p6[1]));NN=(U[1],-U[0])
if NN[0]*RG['NE']['n'][0]+NN[1]*RG['NE']['n'][1]<0:NN=(-NN[0],-NN[1])
O=tuple(RG['NE']['origin'])
def WF(a,b):return (O[0]+U[0]*a+NN[0]*b,O[1]+U[1]*a+NN[1]*b)
def FF(p):dx,dy=p[0]-O[0],p[1]-O[1];return (dx*U[0]+dy*U[1],dx*NN[0]+dy*NN[1])
BC_OUT=round(sum(FF(CI[i])[1] for i in (6,7,8))/3,4)          # courtyard outline (b const)
BC_DEV=round(max(abs(FF(CI[i])[1]-BC_OUT) for i in (6,7,8)),4)
def outer_b(a):
 # pass 27's outer outline (points 39-42) in this frame, at a
 pts=[FF(CO[i]) for i in (39,40,41,42)]
 for (a0,b0),(a1,b1) in zip(pts,pts[1:]):
  if a0<=a<=a1:return b0+(b1-b0)*(a-a0)/(a1-a0)
 return None
SKIN_O,SKIN_C=.36,.355
AMID=22.0
DEPTH=round(outer_b(AMID)+SKIN_O-(BC_OUT-SKIN_C),3)
EX=round((DEPTH-MREAD['depth'])/2,3)
TC=round(MREAD['court_wall']+EX,3)                    # courtyard wall, skin face to room face
BCB=round(BC_OUT+.10,3)                               # courtyard back (0.10 m inside pass 27's outline)
BCI=round(BC_OUT-SKIN_C+TC,3)                         # courtyard room face
BOI=round(BCI+MREAD['hall'],3)                        # spine wall's room face (Möller's inside width)
BOB=round(BOI+MREAD['spine_wall'],3)                  # spine wall's back
# along the range
T_PART=OLSSON['text']['wall_63_65_m']
def a_of(s,c=-11.0):return FF(Wr('NE',s,c))[0]
NI_C=[]
for s,c in FACADE['NE_court']:
 a=FF(Wr('NE',s,c))[0];bg=FF(Wr('NE',s,c))[1];NI_C.append(dict(s=s,a=round(a,3),b_glass=round(bg,3)))
RUT_W=[n for n in NI_C if 18<n['s']<28];DRO_W=[n for n in NI_C if 5<n['s']<15]
assert len(RUT_W)==3 and len(DRO_W)==3,(RUT_W,DRO_W)
LEN63=OLSSON['text']['room63_m'][1]                   # 10.5 m along the range (Olsson's text); across = Möller's 10.82
A63_MID=round(RUT_W[1]['a'],3)                        # on the middle courtyard window
A63=[round(A63_MID-LEN63/2,3),round(A63_MID+LEN63/2,3)]
APART=[round(A63[0]-T_PART,3),A63[0]]
A65_E=round(DRO_W[0]['a']+.36-.75-.25,3)               # the first window's niche (skewed, see below) keeps a 0.25 m pier
A65=[A65_E,APART[0]]
T_E65,T_W63=1.0,1.2                                   # end walls (estimated; plan: 1.2 m)
ENV65=[A65[0]-T_E65,APART[0]];ENV63=[APART[0],A63[1]+T_W63]
LV=dict(floor=FL,z0=Z0,sill=FACADE['state_z'][0],glass_top=FACADE['state_z'][1],board_under=round(FL+MREAD['ceiling'],3),ztop=round(FL+MREAD['ceiling_top'],3),
 panel_top=round(FL+MREAD['panel'],3),door_head=round(FL+2.40,3))
LV['cornice']=round(LV['board_under']-.20,3)
# roof: pass 127's pieces (plane z = Ax+By+C; the joined roof is the upper envelope); underside 0.12 m
ROOF=[(Polygon(rr[0]),pc['plane']) for pc in B127['roof'] for rr in pc['rings']]
def roof_under(p):
 zs=[pl[0]*p[0]+pl[1]*p[1]+pl[2] for poly,pl in ROOF if poly.buffer(.05).contains(Point(p))]
 return (max(zs)-.12) if zs else None
def court_back_top(a):return round(min(LV['ztop'],roof_under(WF(a,BCB))-.10),3)
CBT=[(round(a,2),court_back_top(a)) for a in [ENV65[0]+k*(ENV63[1]-ENV65[0])/40 for k in range(41)]]

# ---------------------------------------------------------------- niches
NICHES=[]
def niche(room,wall,a_in,r_in,a_out,r_out,kind,zb,head,depth=None,door=None,bench=None,b_glass=None):
 return dict(room=room,wall=wall,u_in=round(a_in,3),r_in=round(r_in,3),u_out=round(a_out,3),r_out=round(r_out,3),kind=kind,zb=round(zb,3),head=head,depth=depth,door=door,bench=bench,b_glass=b_glass)
# Rutsalen: three courtyard niches to the floor, flat heads (Möller), each on its facade window; the head is
# raised to clear the facade's glass (z 14.77; Möller's glass head is 3.69 m, the facade's 4.30 m)
for n in RUT_W:
 NICHES.append(niche('rut','court',n['a'],.825,n['a'],FACADE['w']/2+.05,'rect',FL,dict(z_in=round(FL+4.50,3),z_out=round(FACADE['state_z'][1]+.05,3)),b_glass=n['b_glass']))
# Drottningsalen: three round-arched courtyard niches (photographs 1922/1933: arched, the soffit painted
# with coffers), floor one step up; the first is skewed (room face 0.36 m west of its facade window)
for k,n in enumerate(DRO_W):
 a_in=n['a']+(.36 if k==0 else 0);r_in=.75 if k==0 else .825
 NICHES.append(niche('dro','court',a_in,r_in,n['a'],FACADE['w']/2+.05,'arch',FL+.15,dict(zs_in=round(FACADE['state_z'][1]-.17,3),zs_out=round(FACADE['state_z'][1]-.17,3)),b_glass=n['b_glass']))
# spine-wall niches (Möller's section; the 1933 photograph): blind at the back or with a closed door into the
# (unbuilt) outer rooms
SD=MREAD['spine_niche_depth']
NICHES.append(niche('rut','spine',A63_MID,.90,A63_MID,.90,'rect',FL,dict(z_in=round(FL+MREAD['spine_niche_head'][0],3),z_out=round(FL+MREAD['spine_niche_head'][1],3)),depth=SD,
 door=dict(w=1.0,h=MREAD['spine_door_h'])))
A65_MID=round((A65[0]+A65[1])/2,3)
NICHES.append(niche('dro','spine',round(DRO_W[2]['a']+.35,3),1.00,round(DRO_W[2]['a']+.35,3),1.00,'arch',FL,dict(zs_in=round(FL+2.90,3),zs_out=round(FL+2.90,3)),depth=SD,door=dict(w=1.0,h=2.00)))
NICHES.append(niche('dro','spine',round(DRO_W[0]['a']+2.25,3),.75,round(DRO_W[0]['a']+2.25,3),.75,'arch',FL,dict(zs_in=round(FL+2.55,3),zs_out=round(FL+2.55,3)),depth=1.60,bench=dict(h=.50,d=.55)))
FIRE=dict(a=round((NICHES[-1]['u_in']+NICHES[-2]['u_in'])/2,3),w=1.70,open_w=1.10,open_h=1.35,proj=.42,recess=.55)
# doors (end walls): b positions across the room
BMID=round((BCI+BOI)/2,3)
DOORS=[dict(name='rut_dro',wall='partition',a0=APART[0],a1=APART[1],b=round(BMID+.30,3),w=1.25,h=2.40,leaf=False),
 dict(name='dro_east',wall='east65',a0=ENV65[0],a1=A65[0],b=round(BOI-2.60,3),w=1.10,h=2.30,leaf=True),
 dict(name='rut_west',wall='west63',a0=A63[1],a1=ENV63[1],b=round(BMID+.60,3),w=1.10,h=2.30,leaf=True)]

# ---------------------------------------------------------------- footprints and checks
ROOM65=Polygon([WF(A65[0],BCI),WF(A65[1],BCI),WF(A65[1],BOI),WF(A65[0],BOI)])
ROOM63=Polygon([WF(A63[0],BCI),WF(A63[1],BCI),WF(A63[1],BOI),WF(A63[0],BOI)])
EP65=Polygon([WF(ENV65[0],BCB),WF(ENV65[1],BCB),WF(ENV65[1],BOB),WF(ENV65[0],BOB)])
EP63=Polygon([WF(ENV63[0],BCB),WF(ENV63[1],BCB),WF(ENV63[1],BOB),WF(ENV63[0],BOB)])
COP=Polygon(CO);CIP=Polygon(CI);BODY=COP.difference(CIP)
checks={}
for nm,env in (('rut',EP63),('dro',EP65)):
 checks[f'{nm}_outside_body_m2']=round(env.difference(BODY).area,4);checks[f'{nm}_in_court_m2']=round(env.intersection(CIP).area,4)
 for k,t in CA['towers'].items():checks[f'{nm}_in_tower_{k}_m2']=round(env.intersection(Point(t['centre']).buffer(t['radius']+.36,128)).area,4)
 checks[f'{nm}_in_kure_m2']=round(env.intersection(Polygon(CA['kure_rect']).buffer(.36)).area,4)
 for bn,bay in ((b['name'],Polygon(b['polygon'])) for b in CA['bays']):checks[f'{nm}_in_{bn}_m2']=round(env.intersection(bay.buffer(.36)).area,4)
def w125(s,c):f=B125['frame'];return (f['origin'][0]+f['u'][0]*s+f['n'][0]*c,f['origin'][1]+f['u'][1]*s+f['n'][1]*c)
R125={k:Polygon([w125(r['s0'],r['c0']),w125(r['s1'],r['c0']),w125(r['s1'],r['c1']),w125(r['s0'],r['c1'])]) for k,r in B125['rooms'].items()}
# pass 125's walls stand outside its room rectangles; its Gyllene salen mesh reaches NE s 31.03 (saved scene,
# SCR/p143/dump.json) - the check uses the rooms plus 1.6 m, the thickest of its walls towards this range
R125U=unary_union([p.buffer(1.6,join_style=2) for p in R125.values()])
st=B126['stair'];E_,IN_,W1=st['E'],st['IN'],st['W1']
def w126(a,b):return (W1[0]+E_[0]*a+IN_[0]*b,W1[1]+E_[1]*a+IN_[1]*b)
# pass 126's stair and förstuga end by a 9.2 (a_hall); the strip is checked to a 20 (pass 131's proxy runs to a 30,
# which reaches past the courtyard corner into this range's west end, where pass 126 has no geometry)
R126=Polygon([w126(st['a_end'],-1),w126(20,-1),w126(20,8),w126(st['a_end'],8)])
E131=Polygon(B131['forb']['env']);E87=Polygon(B131['gron']['env'])
for nm,env in (('rut',EP63),('dro',EP65)):
 checks[f'{nm}_vs_pass125_m2']=round(env.intersection(R125U).area,4);checks[f'{nm}_dist_pass125_rooms_m']=round(env.distance(unary_union(list(R125.values()))),2)
 checks[f'{nm}_vs_pass126_m2']=round(env.intersection(R126).area,4)
 checks[f'{nm}_vs_pass131_m2']=round(env.intersection(E131).area+env.intersection(E87).area,4)
checks['rut_vs_dro_m2']=round(EP63.intersection(EP65).area,4)
checks['rut_room_m']=[round(A63[1]-A63[0],2),round(BOI-BCI,2)];checks['dro_room_m']=[round(A65[1]-A65[0],2),round(BOI-BCI,2)]
checks['rut_room_m2']=round(ROOM63.area,2);checks['dro_room_m2']=round(ROOM65.area,2)
checks['walls_m']=dict(court=TC,court_from_back=round(BCI-BCB,3),spine=MREAD['spine_wall'],depth_model=DEPTH,depth_moller=MREAD['depth'],excess_each=EX)
checks['frame_deg_off_NE']=round(math.degrees(math.acos(U[0]*RG['NE']['u'][0]+U[1]*RG['NE']['u'][1])),3);checks['court_outline_dev_m']=BC_DEV
checks['faces_NE']=dict(court=round(Fr('NE',WF(20,BCI))[1],2),spine=round(Fr('NE',WF(20,BOI))[1],2),spine_back=round(Fr('NE',WF(20,BOB))[1],2),
 dro_e=round(Fr('NE',WF(A65[0],-11))[0],2),part=[round(Fr('NE',WF(APART[0],-11))[0],2),round(Fr('NE',WF(APART[1],-11))[0],2)],rut_w=round(Fr('NE',WF(A63[1],-11))[0],2),
 env=[round(Fr('NE',WF(ENV65[0],-11))[0],2),round(Fr('NE',WF(ENV63[1],-11))[0],2)])
checks['vs_olsson']=dict(court_face=[checks['faces_NE']['court'],OLSSON['room63_NE']['court_face_c']],spine_face=[checks['faces_NE']['spine'],OLSSON['room63_NE']['outer_face_c'],OLSSON['room65_NE']['outer_face_c']],
 rut_s=[checks['faces_NE']['part'][1],checks['faces_NE']['rut_w'],OLSSON['room63_NE']['s']],dro_s=[checks['faces_NE']['dro_e'],checks['faces_NE']['part'][0],OLSSON['room65_NE']['s']])
# niches: within their room's wall length, clear of the end walls and of each other
bad=[]
for rm,(a0,a1) in (('rut',A63),('dro',A65)):
 for wall in ('court','spine'):
  ns=sorted((n for n in NICHES if n['room']==rm and n['wall']==wall),key=lambda n:n['u_in'])
  for n in ns:
   if n['u_in']-n['r_in']<a0+.25-1e-6 or n['u_in']+n['r_in']>a1-.25+1e-6:bad.append(('niche_end',rm,wall,n['u_in']))
   if n['u_out']-n['r_out']<(ENV65[0] if rm=='dro' else ENV63[0])+.3:bad.append(('niche_env',rm,n['u_out']))
  for p,q in zip(ns,ns[1:]):
   if p['u_in']+p['r_in']>q['u_in']-q['r_in']-.45:bad.append(('niches_close',rm,wall,p['u_in'],q['u_in']))
f=FIRE
for n in NICHES:
 if n['room']=='dro' and n['wall']=='spine' and abs(n['u_in']-f['a'])<n['r_in']+f['w']/2+.15:bad.append(('fire_niche',n['u_in']))
for d in DOORS:
 if not(BCI+.4<d['b']-d['w']/2 and d['b']+d['w']/2<BOI-.4):bad.append(('door_end',d['name']))
checks['problems']=bad
checks['niche_axes_vs_glass']=[(n['room'],n['wall'],n['u_out'],n['b_glass']) for n in NICHES if n['wall']=='court']
checks['glass_to_niche_back_m']=[round(BCB+.05-n['b_glass'],3) for n in NICHES if n['wall']=='court']
checks['court_back_top_min']=min(z for a,z in CBT);checks['court_back_top_clipped']=sum(1 for a,z in CBT if z<LV['ztop'])
def roof_min(poly):
 pts=list(poly.exterior.coords);dense=[]
 for p,q in zip(pts,pts[1:]):
  n=max(1,int(math.hypot(q[0]-p[0],q[1]-p[1])/.5));dense+=[(p[0]+(q[0]-p[0])*i/n,p[1]+(q[1]-p[1])*i/n) for i in range(n)]
 zs=[roof_under(p) for p in dense];zs=[z for z in zs if z is not None];return round(min(zs),3) if zs else None
for nm,room,env in (('rut',ROOM63,EP63),('dro',ROOM65,EP65)):
 checks[f'{nm}_roof_under_min_over_room']=roof_min(room);checks[f'{nm}_roof_under_min_over_env']=roof_min(env)
# the niche heads stay under the ceiling, the arched crowns under the frieze (0.80 m) in Drottningsalen
for n in NICHES:
 top=n['head']['z_in'] if n['kind']=='rect' else n['head']['zs_in']+n['r_in']
 if top>LV['board_under']-.85:bad.append(('niche_high',n['room'],n['u_in'],top))
assert all(checks[k]<.01 for k in checks if k.endswith('_m2') and any(t in k for t in ('outside_body','in_court','in_tower','in_kure','in_bay','_vs_'))),{k:v for k,v in checks.items() if k.endswith('_m2')}
assert not bad,bad
assert abs(checks['rut_room_m'][1]-MREAD['hall'])<.01 and abs(checks['rut_room_m'][0]-10.5)<.01
assert checks['rut_roof_under_min_over_room']>LV['ztop']+.3 and checks['dro_roof_under_min_over_room']>LV['ztop']+.3,checks
assert checks['court_back_top_min']>LV['board_under']+.05,checks['court_back_top_min']
assert all(.10<g<.30 for g in checks['glass_to_niche_back_m']),checks['glass_to_niche_back_m']
assert BC_DEV<.03,BC_DEV
assert 19<MREAD['depth']<22

OUT=dict(source='pass 143: Möller 1882 (PK006-00041, "Rut-salen"), Olsson 1974 fig. 1 and text (registered, read only), photographs (DigitaltMuseum/KLM PDM, Commons KMB); see references/block143-notes.md',
 moller=MOLLER,olsson=OLSSON,facade=FACADE,frame=dict(origin=list(O),u=list(U),n=list(NN)),levels=LV,
 walls=dict(bcb=BCB,bci=BCI,boi=BOI,bob=BOB,court=TC),rut=dict(a=A63,env=ENV63,part=APART,t_w=T_W63),dro=dict(a=A65,env=ENV65,t_e=T_E65),
 court_back_top=CBT,niches=NICHES,doors=DOORS,fire=FIRE,bmid=BMID,checks=checks)
(R/'source/block143.json').write_text(json.dumps(OUT,indent=1,ensure_ascii=False))
zones=dict(rut=dict(room=ring(ROOM63),envelope=ring(EP63)),dro=dict(room=ring(ROOM65),envelope=ring(EP65)))
(R/'previews/block143-zones.json').write_text(json.dumps(dict(**{'pass':143},rooms=zones,checks=checks),indent=1,ensure_ascii=False))
print(json.dumps(checks,ensure_ascii=False))
print('BLOCK143_PREPARE_OK','rut',checks['rut_room_m'],checks['rut_room_m2'],'m2','dro',checks['dro_room_m'],checks['dro_room_m2'],'m2','niches',len(NICHES))
