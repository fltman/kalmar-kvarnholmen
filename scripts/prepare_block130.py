"""Pass 130: the interior of Slottskyrkan, Kalmar slott's chapel (1589-92; room 86 in Olsson's and
Möller's numbering), on the state floor of the south range (pass 27's 'SW' range).

Which range, and where along it.
- Olsson (room 86) and the state-floor plan (KLM 'Plan över praktvåningen': ... 10 Gröna salen,
  11 the round tower's chamber, 12 Slottskyrkan, 13 Sydöstra vindelstenen ...) put the chapel in the
  south range; in the model that is pass 27's 'SW' range (courtyard front facing true heading 216),
  between the west and south round towers. Pass 27 already puts the chapel's roof turret on its ridge
  (s 13.75), and pass 127 found the range's middle courtyard row crossing the state-floor slab.
- The c. 1780 plan 'Plan af Calmare Slotts Kyrka N:o 1' (Krigsarkivet 0424:058:212a, public domain)
  has its scale in alnar: 10 alnar = 636 px on the 3587 px scan (ticks 0/10/20/30 at x 735/1371/
  2009/2643), 63.6 px per aln, 107.1 px/m (1 aln = 0.5938 m). Inside the walls the chapel is
  2310 x 766 px = 21.57 x 7.15 m. Möller's section 'Profil genom Kyrkan' (1882, PK006-00041,
  57.97 px/m on the 90-fot bar, pass 127's reading) gives 7.30 m between the inner faces.
- The plan's thick wall (1.72 m, four deep splayed niches) is the outer wall; its thin wall (1.19 m,
  six small windows at a regular 3.67 m) is the courtyard wall. Möller has the same: outer wall
  1.89 m, courtyard wall 1.27 m. Facing the altar, the plan has the courtyard wall on the left. In the
  SW range, a viewer facing +s has the courtyard (-c) on the left, so the altar is at the +s end, by
  the south tower (the liturgical east end, true heading about 126). The photographs agree: facing
  the altar, the pulpit gallery stands against the left wall with windows behind it (Commons 2015,
  2017), and the door beside the altar is on the right, at the outer wall, as in the plan.
- The SW range's courtyard front runs from the west courtyard corner (s 6.07) to the south corner
  (s 27.84): 21.8 m, the chapel's inside length. The end walls are put at these corners:
  the west wall's inner face at s 6.20, the altar wall's at s 27.77.

Heights (Möller, 'Profil genom Kyrkan', read on full-resolution crops; floor = his red state-floor
line, row 9927, as in pass 127): a barrel vault of half-elliptic section, springing 3.14 m above the
floor (row 9745) and with its crown 5.43 m above it (row 9612); windows on both sides with their
sills 1.33 m and heads 4.6 m above the floor; the vault's back and the attic floor 6.9 m above it.
The chapel's floor is the state floor, z 10.47.

Window niches. The niches sit on the facade's windows as they stand in the scene the sandbox builds
with prelude 128 (pass 126/127's rows; read from SM_Kalmar_Slott's glass): courtyard state row at
s 10.27, 14.07, 17.87, 21.67, 25.47 (1.2 x 3.2 m, sill z 11.57); outer state row at s 10.94, 15.34,
22.42, 26.82 (1.15 x 3.2 m). The plan's sixth courtyard window (s 7.40) has no facade window; it is
built as a blind niche (pane against the shell), as pass 126 did with Gyllene salen's north niche.
The outer niche by the altar wall is splayed asymmetrically (inner axis at the plan's s 26.30, outer
at the facade's 26.82), as the plan draws its outer niches.

Furnishings are placed from the plan: altar (a), pulpit (b), the commander's pews with posts (c),
the priest's pew (d, now under the raised pulpit gallery), closed pews (e) and open benches (f), the
round object by d (the stone font of the photographs), the chancel step. The organ at the west end is
from the photographs (it is not in the 1780 plan).

Output: source/block130.json (frame, levels, room, niches, furnishing positions in (s, c)),
previews/block130-zones.json (the room and wall footprints in model coordinates, checks).
Run with Shapely: KALMAR_GEO=<site-packages> python3 scripts/prepare_block130.py
"""
from pathlib import Path
import json,math,os,sys
if os.environ.get('KALMAR_GEO'):sys.path.insert(0,os.environ['KALMAR_GEO'])
from shapely.geometry import Polygon,Point,LineString
from shapely.ops import unary_union
R=Path(__file__).resolve().parents[1]
C27=json.loads((R/'source/castle27.json').read_text());CA=C27['castle']
B125=json.loads((R/'source/block125.json').read_text());B126=json.loads((R/'source/block126.json').read_text())
B127=json.loads((R/'source/block127.json').read_text())
RG={r['name']:r for r in CA['ranges']}['SW']
O,U,N=RG['origin'],RG['u'],RG['n']
def W(s,c):return (O[0]+U[0]*s+N[0]*c,O[1]+U[1]*s+N[1]*c)
def F(p):dx,dy=p[0]-O[0],p[1]-O[1];return (dx*U[0]+dy*U[1],dx*N[0]+dy*N[1])

# ---------------------------------------------------------------- sources: scales and readings
PLAN=dict(scan=[3587,2558],aln_ticks_x={'0':735,'10':1371,'20':2009,'30':2643},px_per_aln=63.6,aln_m=.5938)
PLAN['px_per_m']=round(PLAN['px_per_aln']/PLAN['aln_m'],2)            # 107.11
PXM=PLAN['px_per_m']
# Plan rows/columns (full-resolution scan): inner faces of the walls, outer faces, openings.
PX=dict(x_altar_in=578,x_altar_out=478,x_west_in=2888,x_west_out=3025,y_out_in=697,y_out_out=513,y_court_in=1463,y_court_out=1590)
PLAN['inside_m']=[round((PX['x_west_in']-PX['x_altar_in'])/PXM,2),round((PX['y_court_in']-PX['y_out_in'])/PXM,2)]
PLAN['walls_m']=dict(outer=round((PX['y_out_in']-PX['y_out_out'])/PXM,2),court=round((PX['y_court_out']-PX['y_court_in'])/PXM,2),
 altar=round((PX['x_altar_in']-PX['x_altar_out'])/PXM,2),west=round((PX['x_west_out']-PX['x_west_in'])/PXM,2))
# Window openings: (inner-face centre x, inner width px, outer width px); the plan's courtyard windows at
# rows 1475/1530, its outer niches at rows 690/525 (grey-run detection on the scan).
PLAN_COURT=[(784.5,121,97),(1174,118,102),(1570.5,115,91),(1955.5,119,101),(2352.5,117,94),(2760.5,129,97)]
PLAN_OUT=[(739.5,193,125),(1391,190,127),(2020.5,195,150),(2431.5,191,133)]
MOLLER=dict(px_per_m=57.97,floor_row=9927,spring_row=9745,crown_row=9612,attic_row=9527,x_court_in=5721,x_out_in=6144,
 x_court_out=5647.5,x_out_out=6253.75,court_sill_row=9850,court_head_row=9660,out_sill_row=9852,out_head_row=9662,niche_head_inner_row=9690)
def mz(row):return round((MOLLER['floor_row']-row)/MOLLER['px_per_m'],2)
MOLLER.update(inside_m=round((MOLLER['x_out_in']-MOLLER['x_court_in'])/MOLLER['px_per_m'],2),court_wall_m=round((MOLLER['x_court_in']-MOLLER['x_court_out'])/MOLLER['px_per_m'],2),
 out_wall_m=round((MOLLER['x_out_out']-MOLLER['x_out_in'])/MOLLER['px_per_m'],2),spring_m=mz(MOLLER['spring_row']),crown_m=mz(MOLLER['crown_row']),attic_m=mz(MOLLER['attic_row']),
 court_window_m=[mz(MOLLER['court_sill_row']),mz(MOLLER['court_head_row'])],out_window_m=[mz(MOLLER['out_sill_row']),mz(MOLLER['out_head_row'])],niche_head_inner_m=mz(MOLLER['niche_head_inner_row']))

# ---------------------------------------------------------------- room in the SW range frame
FL=B127['floor']                       # 10.47, the state floor (pass 125); Möller's chapel floor is on it
SLAB=.30
S_W,S_A=6.20,6.20+PLAN['inside_m'][0]  # west wall's and altar wall's inner faces
C_OI,C_CI=-1.25,-1.25-PLAN['inside_m'][1]   # outer and courtyard inner faces
C_OO,C_CO=-0.10,-9.25                  # the walls' outer faces, inside pass 27's outline (outer front c -0.07..0.36, courtyard front -9.27..-9.37)
T_W,T_A=1.28,0.93                      # end walls (plan)
SPRING=round(FL+MOLLER['spring_m'],3);CROWN=round(FL+MOLLER['crown_m'],3)
ZTOP=16.60                             # top of the walls and the vault's fill: under the courtyard roof (eaves z 17.01 at the courtyard face)
A_V=round((C_OI-C_CI)/2,4);B_V=round(CROWN-SPRING,4);CC=round((C_OI+C_CI)/2,4)
def sx(x):return round(S_A-(x-PX['x_altar_in'])/PXM,3)   # plan column -> s
def cy(y):return round(C_OI-(y-PX['y_out_in'])/PXM,3)     # plan row -> c

# ---------------------------------------------------------------- facade windows (prelude 128 scene)
FACADE=dict(read='SM_Kalmar_Slott glass faces, sandbox with prelude 128 (SCR/p130/dump.json)',
 court_state=[10.27,14.07,17.87,21.67,25.47],court_state_w=1.2,court_mid=[10.27,14.07,21.67,25.47],court_mid_z=[9.9,11.1],
 out_state=[3.69,10.94,15.34,22.42,26.82],out_state_w=1.15,state_z=[11.57,14.77],court_door=[17.17,18.57,5.47,7.87])
plan_court=[sx(x) for x,_,_ in PLAN_COURT];plan_out=[sx(x) for x,_,_ in PLAN_OUT]
NICHES=[]
for s in FACADE['court_state']:
 p=min(plan_court,key=lambda q:abs(q-s))
 NICHES.append(dict(side='court',u_in=s,u_out=s,r_in=.725,r_out=.65,zb=FACADE['state_z'][0],zs_in=13.85,h_in=.725,zs_out=FACADE['state_z'][1],h_out=.30,
  lun_L=1.25,lun_R=1.75,facade=s,plan=p,blind=False))
NICHES.append(dict(side='court',u_in=7.55,u_out=7.55,r_in=.725,r_out=.65,zb=FACADE['state_z'][0],zs_in=13.85,h_in=.725,zs_out=FACADE['state_z'][1],h_out=.30,
 lun_L=1.25,lun_R=1.75,facade=None,plan=plan_court[-1],blind=True))
for s in FACADE['out_state'][1:]:
 p=min(plan_out,key=lambda q:abs(q-s));ui=p if abs(s-S_A)<1.5 else s
 NICHES.append(dict(side='out',u_in=round(ui,3),u_out=s,r_in=.90,r_out=.65,zb=FACADE['state_z'][0],zs_in=13.75,h_in=.90,zs_out=FACADE['state_z'][1],h_out=.30,
  lun_L=1.45,lun_R=1.75,facade=s,plan=p,blind=False))
NICHES.sort(key=lambda n:(n['side'],n['u_in']))

# ---------------------------------------------------------------- doors, chancel, furnishings (plan -> s, c)
DOORS=dict(west=dict(c=cy(1019),w=1.10,h=2.40,plan_rows=[960,1078]),altar=dict(c=-2.00,w=.90,h=2.20,plan_rows=[765,835]))
CHANCEL=dict(s=sx(982),risers=2,rise=.14)
ALTAR=dict(s0=round(S_A-.80,3),s1=S_A,c0=cy(965),c1=cy(1215),h=1.00)
RAIL=dict(c_mid=round((cy(840)+cy(1335))/2,3),half=round((cy(840)-cy(1335))/2,3),depth=round(S_A-sx(870),3),h=.95,platform=.14)
FONT=dict(s=sx(900),c=cy(1300))
PULPIT=dict(s0=sx(1015),s1=S_A,c0=cy(1340),c1=C_CI,deck=1.40,parapet=1.10)
CPEWS=[dict(s0=sx(1150),s1=sx(1030),c0=C_OI,c1=cy(935),posts=[[sx(1030),cy(745)],[sx(1150),cy(745)],[sx(1030),cy(935)],[sx(1150),cy(935)]]),
 dict(s0=sx(1150),s1=sx(1030),c0=cy(1240),c1=C_CI,posts=[[sx(1030),cy(1250)],[sx(1150),cy(1250)],[sx(1030),cy(1445)],[sx(1150),cy(1445)]])]
CLOSED=[1157,1256,1373,1476,1596,1700,1808,1928,2029,2143,2244]     # partitions of the closed pews (c, e)
OPEN=[2244,2350,2464,2578,2689,2786,2868]                            # partitions of the open benches (f)
PEWS=dict(top_c=[cy(708),cy(963)],bottom_c=[cy(1191),C_CI],closed=[sx(x) for x in CLOSED],open=[sx(x) for x in OPEN])
ORGAN=dict(s=S_W,c0=round(DOORS['west']['c']+DOORS['west']['w']/2+.25,3),c1=round(C_OI-.12,3),h=3.60,d=.85)
CHANDELIERS=[11.0,17.0,23.0]
RINGS=[8.85,12.75,16.65,20.55,24.45]      # crown medallions, between the courtyard bays
SUN=dict(s=23.57,dc=.45,z=round(SPRING+1.10,3),r=.62)      # on the pier between the courtyard lunettes over the pulpit's west end (photographs)

# ---------------------------------------------------------------- checks
CO=Polygon(CA['outer']);CI=Polygon(CA['court']);BODY=CO.difference(CI)
def poly(s0,s1,c0,c1):return Polygon([W(s0,c0),W(s1,c0),W(s1,c1),W(s0,c1)])
ROOM=poly(S_W,S_A,C_CI,C_OI);ENV=poly(S_W-T_W,S_A+T_A,C_CO,C_OO)
checks={}
checks['inside_m']=PLAN['inside_m'];checks['moller_inside_m']=MOLLER['inside_m']
checks['envelope_outside_body_m2']=round(ENV.difference(BODY).area,4)
checks['envelope_in_court_m2']=round(ENV.intersection(CI).area,4)
for k,t in CA['towers'].items():checks[f'envelope_in_tower_{k}_m2']=round(ENV.intersection(Point(t['centre']).buffer(t['radius']+.36,64)).area,4)
checks['envelope_in_kure_m2']=round(ENV.intersection(Polygon(CA['kure_rect']).buffer(.36)).area,4)
# pass 125's rooms and pass 126's stair (their frames), as footprints
def w125(s,c):f=B125['frame'];return (f['origin'][0]+f['u'][0]*s+f['n'][0]*c,f['origin'][1]+f['u'][1]*s+f['n'][1]*c)
R125=unary_union([Polygon([w125(r['s0'],r['c0']),w125(r['s1'],r['c0']),w125(r['s1'],r['c1']),w125(r['s0'],r['c1'])]).buffer(2.2) for r in B125['rooms'].values()])
checks['envelope_vs_pass125_rooms_plus_walls_m2']=round(ENV.intersection(R125).area,4);checks['distance_to_pass125_m']=round(ENV.distance(R125),2)
st=B126['stair'];E,IN=st['E'],st['IN'];W1=st['W1']
def w126(a,b):return (W1[0]+E[0]*a+IN[0]*b,W1[1]+E[1]*a+IN[1]*b)
R126=Polygon([w126(st['a_end']-1,-1),w126(30,-1),w126(30,8),w126(st['a_end']-1,8)])
checks['envelope_vs_pass126_m2']=round(ENV.intersection(R126).area,4);checks['distance_to_pass126_m']=round(ENV.distance(R126),2)
# the courtyard corners bound the chapel's courtyard wall
cs=[F(p) for p in CA['court']];corner_w=min((p for p in cs if abs(p[1]+9.3)<.2),key=lambda p:p[0]);corner_s=max((p for p in cs if abs(p[1]+9.35)<.2),key=lambda p:p[0])
checks['court_corners_s']=[round(corner_w[0],2),round(corner_s[0],2)]
outline=[F(p) for p in CA['outer'][7:11]];checks['outer_front_c']=[round(p[1],3) for p in outline]
# niches: inside the room's length, lunettes clear of each other and of the end walls; the niche arch
# stays under its lunette at the wall face (so the vault's fill never covers a niche mouth)
def lun(n,x):return SPRING+n['lun_R']*math.sqrt(max(0,1-(x/n['lun_L'])**2))
bad=[]
for n in NICHES:
 if not(S_W+.05<n['u_in']-n['lun_L'] and n['u_in']+n['lun_L']<S_A-.01):bad.append(('lunette_end',n['side'],n['u_in']))
 for k in range(21):
  x=-n['r_in']+2*n['r_in']*k/20;arch=n['zs_in']+n['h_in']*math.sqrt(max(0,1-(x/n['r_in'])**2))
  if arch>lun(n,x)-.08:bad.append(('arch_over_lunette',n['side'],n['u_in'],round(x,2)))
 if n['zs_out']+n['h_out']>ZTOP-.3 or n['zs_in']+n['h_in']>ZTOP-.3:bad.append(('head',n['u_in']))
for side in ('court','out'):
 ns=sorted((n for n in NICHES if n['side']==side),key=lambda n:n['u_in'])
 for a,b in zip(ns,ns[1:]):
  if a['u_in']+a['lun_L']>b['u_in']-b['lun_L']-.05:bad.append(('lunettes_touch',side,a['u_in'],b['u_in']))
  if max(a['u_in'],a['u_out'])+a['r_in']>min(b['u_in'],b['u_out'])-b['r_in']-.3:bad.append(('niches_touch',side,a['u_in'],b['u_in']))
checks['niche_problems']=bad
checks['niches']=[(n['side'],n['u_in'],n['u_out'],n['facade'],n['plan'],round((n['facade'] or n['u_in'])-n['plan'],2)) for n in NICHES]
checks['plan_court_s']=plan_court;checks['plan_out_s']=plan_out
checks['vault']=dict(spring=SPRING,crown=CROWN,a=A_V,b=B_V,cc=CC)
# the vault and walls stay under pass 127's roof: the courtyard slope over the courtyard wall's face
sl=B127['ranges']['SW'];zroof=B127['zce']+sl['sli']*(C_CO-(min(corner_w[1],corner_s[1])-.355))-.12   # roof underside (0.12 m) over the courtyard wall's face
checks['roof_over_court_wall_min_z']=round(zroof,2);checks['ztop']=ZTOP
checks['crown_below_ztop']=round(ZTOP-CROWN,2)
checks['pews_clear_of_aisle']=PEWS['top_c'][1]-PEWS['bottom_c'][0]
assert checks['envelope_outside_body_m2']<.01 and checks['envelope_in_court_m2']<.01,checks
assert all(checks[f'envelope_in_tower_{k}_m2']<.01 for k in CA['towers']) and checks['envelope_in_kure_m2']<.01,checks
assert checks['envelope_vs_pass125_rooms_plus_walls_m2']==0 and checks['envelope_vs_pass126_m2']==0,checks
assert not bad,bad
assert 7.0<PLAN['inside_m'][1]<7.4 and abs(PLAN['inside_m'][1]-MOLLER['inside_m'])<.3
assert abs(S_W-corner_w[0])<.3 and abs(S_A-corner_s[0])<.3,(S_W,S_A,corner_w,corner_s)
assert CROWN<ZTOP-.5 and ZTOP<zroof-.5
assert PEWS['top_c'][1]>PEWS['bottom_c'][0]+1.5
for n in NICHES:assert C_OI-.01<0 and n['zb']>FL+.9

OUT=dict(source='pass 130: Krigsarkivet 0424:058:212a (plan of the chapel, c. 1780), Möller 1882 (PK006-00041), Commons photographs; see references/block130-notes.md',
 frame=dict(origin=O,u=U,n=N,range='SW'),plan=PLAN,plan_px=PX,moller=MOLLER,
 levels=dict(floor=FL,slab=SLAB,spring=SPRING,crown=CROWN,a=A_V,b=B_V,cc=CC,ztop=ZTOP),
 room=dict(s_w=S_W,s_a=round(S_A,3),c_oi=C_OI,c_ci=round(C_CI,3),c_oo=C_OO,c_co=C_CO,t_w=T_W,t_a=T_A),
 facade=FACADE,niches=NICHES,doors=DOORS,chancel=CHANCEL,altar=ALTAR,rail=RAIL,font=FONT,pulpit=PULPIT,cpews=CPEWS,pews=PEWS,organ=ORGAN,
 chandeliers=CHANDELIERS,rings=RINGS,sun=SUN,checks=checks)
(R/'source/block130.json').write_text(json.dumps(OUT,indent=1,ensure_ascii=False))
zones=dict(room=[list(map(lambda v:round(v,3),p)) for p in ROOM.exterior.coords][:-1],envelope=[list(map(lambda v:round(v,3),p)) for p in ENV.exterior.coords][:-1])
(R/'previews/block130-zones.json').write_text(json.dumps(dict(**{'pass':130},rooms=zones,checks=checks),indent=1,ensure_ascii=False))
print(json.dumps(checks,indent=0,ensure_ascii=False)[:3000])
print('BLOCK130_PREPARE_OK','room',PLAN['inside_m'],'s',S_W,round(S_A,2),'niches',len(NICHES),'vault',SPRING,CROWN)
