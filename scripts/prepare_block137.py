"""Pass 137: Kalmar slott, corrections from the project's own sources (no new source fetched).

1. Kungsköket's great hearth (pass 135). The 1969 photographs (DigitaltMuseum 021017090086, -090089,
   -090090; PDM) show the brick stack with rounded corners (the near corner in 090086 and 090089 is a
   curved face, not an arris), arched openings on the faces (two on the long faces, 090090; one on the
   short faces, 090089), a projecting course at the stack's top and a rounded, tapering hood rising
   into the cross wall's arch (090089: a curved outline; 090090: a trapezoid with rounded shoulders).
   Pass 135 built a square stack and a four-sided hood. Same footprint, same heights; new form:
   - plan: a rounded rectangle, corner radius 0.70 m (walls 0.50 m, so the corners are quarter rings);
   - openings: long faces two arches 0.80 m wide with a 0.50 m middle pier, short faces one 1.10 m arch;
   - a projecting top course (0.06 m, 0.10 m high);
   - the hood: a loft from the stack's rounded rectangle to a circle of 0.55 m radius under the arch's
     crown, bulging (convex) as in 090089; the flue a round shaft into the cross wall over the crown.
2. Gröna salen's second end-wall window (pass 131's blind niche at SW s 1.55). The photograph
   castle27/kalmar-slott-9-kalmar.jpg (Commons, Hstad 2009, CC BY-SA 3.0) shows the SW range's outer front from the west, from the
   west tower to the south tower: next to the west tower stand two state-floor windows about one window
   width apart, then a long pier, then the chapel's windows. The camera was resected on six points
   (postejer W and S, towers W, S and N, Kuretornet; 1-1.5 px residuals): the two windows read at
   SW s 0.08 and 2.46 (widths 1.13 and 1.16 m), 2.38 m apart; the west tower's silhouette at -0.86.
   The model's single window is at 3.69 (pass 27's rule), so the measured spacing puts the second at
   1.31. The niche in Gröna salen cannot move nearer the tower's lining than 1.55 (pass 131's 0.25 m
   clearance), so the facade window goes on the niche's axis, s 1.55 (0.24 m from the spacing reading),
   and pass 131's prepare is re-run with the niche no longer blind.
3. The north tower's wall top (pass 132's open issue). Not raised: the two sources disagree. Möller 1882
   ('Profil genom Kungsmaket', PK006-00041) puts the tower's eaves 12.16 m over the state floor (z 22.63,
   0.64 m BELOW pass 27's 23.27); Kungsmaket's height on the same section (4.33 m) agrees with pass 125's
   4.3 m, so the reading is sound. Möller 1885 (PK006-00049) puts an adjoining bracketed cornice 13.5 fot
   (4.01 m) under the tower's eaves; with the range's outer eaves (z 20.27) that gives z 24.28, with the
   1882 eaves z 18.62, which is no eaves in the model. The two readings are 1.65 m apart.
4. NE's courtyard front in 2022 (pass 129's open issue): the 2022 photograph castle27/swe-kalmar-slott-006
   shows NE (portal D, the 7-step stair's front) with the painted rustication, the margins round the
   windows and the chain band, as NW and SW. Current state wins: RUST127 gains 'NE', and NE's last
   straight edge by the east corner (CI5-CI6, which pass 127's nearest-range test gives to SE_e) is added.
Output: source/block137.json, previews/block137-zones.json.
Run with Shapely: KALMAR_GEO=<site-packages> python3 scripts/prepare_block137.py
"""
from pathlib import Path
import json,math,os,sys,io,contextlib
if os.environ.get('KALMAR_GEO'):sys.path.insert(0,os.environ['KALMAR_GEO'])
from shapely.geometry import Polygon,Point,LineString
from shapely.ops import unary_union
R=Path(__file__).resolve().parents[1]
C27=json.loads((R/'source/castle27.json').read_text());CA=C27['castle']
B131=json.loads((R/'source/block131.json').read_text());B135=json.loads((R/'source/block135.json').read_text())
RG={r['name']:r for r in CA['ranges']}
def Wr(name,s,c):r=RG[name];o,u,n=r['origin'],r['u'],r['n'];return (o[0]+u[0]*s+n[0]*c,o[1]+u[1]*s+n[1]*c)
def Fr(name,p):r=RG[name];o,u,n=r['origin'],r['u'],r['n'];dx,dy=p[0]-o[0],p[1]-o[1];return (dx*u[0]+dy*u[1],dx*n[0]+dy*n[1])
def rnd(p,k=4):return [round(p[0],k),round(p[1],k)]
checks={}

# ================================================================= 1. the hearth
K=B135['kitchen'];A=K['arch'];H0=K['hearth']
def W(s,c):return Wr('SE_w',s,c)
SH,CH=H0['s'],H0['c']
H=dict(H0)
H.update(r=.70,arches_sn=[[-1.05,-.25],[.25,1.05]],arch_ew=[-.55,.55],ledge=.06,ledge_h=.10,
 hood_r=.55,hood_rings=7,hood_bulge=1.5,flue_r=.40)
for k in ('hood_hs','hood_hc'):H.pop(k)
H['hood_z0']=round(H['top']+H['ledge_h'],3)
def rrect(s0,s1,c0,c1,r,k=6):
 # A rounded rectangle in the frame (s,c), counter-clockwise from the +s,-c corner's start; k points per quarter.
 pts=[];cs=((s1-r,c0+r,-90),(s1-r,c1-r,0),(s0+r,c1-r,90),(s0+r,c0+r,180))
 for cs_,cc_,a0 in cs:
  for i in range(k+1):a=math.radians(a0+90*i/k);pts.append((cs_+r*math.cos(a),cc_+r*math.sin(a)))
 return pts
def arch_z(c):x=c-CH;return A['zo']+math.sqrt(max(0,A['R']**2-x*x))
# The hood's rings (frame points): from the stack's rounded rectangle (half-extents hs, hc, radius r)
# to a circle of hood_r; each point keeps its polar angle about the axis; a convex profile (blend t^1.5).
base=rrect(SH-H['hs'],SH+H['hs'],CH-H['hc'],CH+H['hc'],H['r'])
def hood_ring(t):
 b=t**H['hood_bulge'];z=H['hood_z0']+(H['hood_top']-H['hood_z0'])*t;out=[]
 for s,c in base:
  a=math.atan2(c-CH,s-SH);ps,pc=SH+H['hood_r']*math.cos(a),CH+H['hood_r']*math.sin(a)
  out.append((s+(ps-s)*b,c+(pc-c)*b))
 return z,out
RINGS=[hood_ring(i/(H['hood_rings']-1)) for i in range(H['hood_rings'])]
H['hood']=[[round(z,3),[[round(s,4),round(c,4)] for s,c in pts]] for z,pts in RINGS]
HK=checks['hearth']={}
HK['arches_in_flat_sn']=max(abs(a) for p in H['arches_sn'] for a in p)+.05<=H['hc']-H['r']
HK['arches_in_flat_ew']=max(abs(a) for a in H['arch_ew'])+.05<=H['hs']-H['r']
HK['arch_widths']=[round(p[1]-p[0],2) for p in H['arches_sn']]+[round(H['arch_ew'][1]-H['arch_ew'][0],2)]
HK['middle_pier']=round(H['arches_sn'][1][0]-H['arches_sn'][0][1],2)
# under the cross wall's arch: every hood point within the wall's thickness (plus 0.10) stays 0.05 under the intrados
under=[(round(arch_z(c)-z,3),round(s,2),round(c,2),z) for z,pts in RINGS for s,c in pts if A['s0']-.10<=s<=A['s1']+.10]
HK['hood_min_clearance_under_arch_m']=min(u[0] for u in under)
HK['hood_all_points_clearance_m']=round(min(arch_z(c)-z for z,pts in RINGS for s,c in pts),3)
HK['flue_in_wall']=A['s0']+.05<=SH-H['flue_r'] and SH+H['flue_r']<=A['s1']-.05
HK['flue_top']=round(A['crown']+.10,3)
SE=lambda pts:Polygon([W(s,c) for s,c in pts])
PL=SE(rrect(SH-H['hs']-H['plinth'],SH+H['hs']+H['plinth'],CH-H['hc']-H['plinth'],CH+H['hc']+H['plinth'],H['r']+H['plinth']))
OLDP=SE([(SH-H['hs']-H['plinth'],CH-H['hc']-H['plinth']),(SH+H['hs']+H['plinth'],CH-H['hc']-H['plinth']),(SH+H['hs']+H['plinth'],CH+H['hc']+H['plinth']),(SH-H['hs']-H['plinth'],CH+H['hc']+H['plinth'])])
HK['plinth_inside_pass135_footprint']=PL.difference(OLDP.buffer(1e-6)).area<1e-6
HK['in_arch_opening']=A['c0']<CH-H['hc']-H['plinth'] and CH+H['hc']+H['plinth']<A['c1']
HK['route_clear_of_hearth']=not any(PL.contains(Point(W(s,c))) for s,c in K['route'])
HK['route_min_dist_to_plinth_m']=round(min(PL.exterior.distance(Point(W(s,c))) for s,c in K['route']),2)
assert HK['arches_in_flat_sn'] and HK['arches_in_flat_ew'] and HK['hood_min_clearance_under_arch_m']>.05 and HK['hood_all_points_clearance_m']>.05,HK
assert HK['flue_in_wall'] and HK['plinth_inside_pass135_footprint'] and HK['in_arch_opening'] and HK['route_clear_of_hearth'],HK

# ================================================================= 2. Gröna salen's end-wall window
SRC131=(R/'scripts/prepare_block131.py').read_text()
def rep137(src,old,new,n=1):
 assert src.count(old)==n,('source changed',src.count(old),old[:80]);return src.replace(old,new)
_W1="(R/'source/block131.json').write_text(json.dumps(OUT,indent=1,ensure_ascii=False))\n"
_W2="(R/'previews/block131-zones.json').write_text(json.dumps(dict(**{'pass':131},rooms=zones,checks=checks),indent=1,ensure_ascii=False))\n"
def run131(src):
 src=rep137(rep137(src,_W1,''),_W2,'')
 ns={'__file__':str(R/'scripts/prepare_block131.py'),'__name__':'prepare_block131_rerun'}
 with contextlib.redirect_stdout(io.StringIO()) as buf:exec(compile(src,'prepare_block131.py (pass 137)','exec'),ns)
 assert 'BLOCK131_PREPARE_OK' in buf.getvalue()
 return json.loads(json.dumps(ns['OUT'],ensure_ascii=False))
# (a) pass 131's prepare, unchanged, reproduces source/block131.json exactly (the re-run is faithful)
G0=run131(SRC131);checks['gron_rerun_identical']=G0==B131
assert checks['gron_rerun_identical']
# (b) the same with the niche at SW s 1.55 no longer blind: it runs through to the facade's glass
G1=run131(rep137(SRC131,"NI87.append(niche_sw(1.55,FACADE['SW_outer_w'],blind=True))","NI87.append(niche_sw(1.55,FACADE['SW_outer_w']))"))
GR=G1['gron']
GK=checks['gron']={}
GK['changed_keys']=sorted(k for k in GR if GR[k]!=B131['gron'][k])
GK['forb_unchanged']=G1['forb']==B131['forb']
GK['niches_end']=[(n['s_out'],n['blind'],n['depth']) for n in GR['niches'] if n['wall']=='end']
assert set(GK['changed_keys'])<={'niches','wallbands'} and GK['forb_unchanged'],GK
assert [n['blind'] for n in GR['niches'] if n['wall']=='end']==[False,False],GK
# The facade window on pass 27's SW outer edge CO7 -> CO8 (s 0 -> 7.37), main row (pass 27's OUT_ROWS[0]).
CO=[tuple(p) for p in CA['outer']]
p,q=CO[7],CO[8];L=math.dist(p,q);mid=((p[0]+q[0])/2,(p[1]+q[1])/2);d=((q[0]-p[0])/L,(q[1]-p[1])/L)
S_WIN=1.55
_niche=[n for n in GR['niches'] if n['wall']=='end' and abs(n['s_out']-S_WIN)<1e-6][0]
_bm=_niche['back_mid']
U_WIN=round((_bm[0]-mid[0])*d[0]+(_bm[1]-mid[1])*d[1],3)
ZH=lambda h:round(-1.33+h,4)
Z0=ZH(C27['levels_h']['foot'])
WIN=[U_WIN,round(Z0+7.9,4),1.15,3.2,0]
GK['edge']=[7,8];GK['edge_len']=round(L,3);GK['u']=U_WIN;GK['window_sill_head']=[WIN[1],round(WIN[1]+WIN[3],3)]
GK['s_of_window']=round(Fr('SW',(mid[0]+d[0]*U_WIN,mid[1]+d[1]*U_WIN))[0],3)
GK['in_edge']=abs(U_WIN)+WIN[2]/2<L/2-.4
GK['pier_to_pass27_window_m']=round(abs(U_WIN)-WIN[2],3)        # pass 27's window is at u 0 (s 3.69)
GK['photo']=dict(file='references/castle27/kalmar-slott-9-kalmar.jpg',size=[1280,857],
 resection=dict(points={'postej W':[312],'postej S':[1138],'tower W':[448],'tower S':[772],'Kuretornet':[362],'tower N':[262]},
  camera=[-1107.3,-354.2],bearing=82.8,f_px=1649,vfov=29.14,residual_px=1.5),
 windows_px=[[493.7,502.5],[512.0,521.0]],windows_s=[[-.47,.66],[1.88,3.04]],window_axes_s=[.08,2.46],tower_W_edge_s=-.86,tower_S_edge_s=30.3,
 spacing_m=2.38,second_window_from_pass27_spacing_s=round(3.687-2.38,2))
GK['offset_from_photo_spacing_m']=round(S_WIN-GK['photo']['second_window_from_pass27_spacing_s'],2)
assert GK['in_edge'] and GK['pier_to_pass27_window_m']>.8 and abs(GK['s_of_window']-S_WIN)<.03,GK

# ================================================================= 3. the north tower's wall top (not changed)
NT=checks['north_tower']=dict(
 moller1882=dict(sheet='PK006-00041, Profil genom Kungsmaket',px_per_m=57.97,state_floor_row=4270.7,eaves_row=3565.7,
  room_cornice_row=4017,eaves_over_floor_m=round((4270.7-3565.7)/57.97,2),eaves_z=round(10.47+(4270.7-3565.7)/57.97,2),
  kungsmaket_height_m=round((4270.7-4017)/57.97,2),pass125_kungsmaket_height_m=4.3),
 moller1885=dict(sheet='PK006-00049, Norra tornet',written='13.5 fot from the eaves down to an adjoining bracketed cornice',fot_m=.2969,
  drop_m=round(13.5*.2969,2),if_range_outer_eaves=round(20.27+13.5*.2969,2),if_1882_eaves_the_cornice_is_at=round(10.47+(4270.7-3565.7)/57.97-13.5*.2969,2)),
 pass27_wall_top=23.27)
NT['disagreement_m']=round(NT['moller1885']['if_range_outer_eaves']-NT['moller1882']['eaves_z'],2)
NT['decision']='not raised: the 1882 section (validated by Kungsmaket\'s height) and the 1885 sheet\'s cornice (if it is the range\'s eaves) disagree by %.2f m'%NT['disagreement_m']
assert abs(NT['moller1882']['kungsmaket_height_m']-4.3)<.15 and NT['disagreement_m']>1.0

# ================================================================= 4. NE rustication (2022)
checks['ne_rust']=dict(photo='references/castle27/swe-kalmar-slott-006.jpg (-wuppertaler 2022, CC BY-SA 4.0), camera 690 (pass 129)',
 seen='NE left of the well: painted block rustication, lime margins round the windows, the chain band under the state-floor windows, as on NW and SW; SE_e right of the well: plain cream lime (faint traces only)',
 street_view_2014='NE smooth white (pass 127/129)',rust=['NW','SW','NE'],
 extra_edge=dict(ci=[5,6],length_m=round(math.dist(CA['court'][5],CA['court'][6]),2),why='collinear with NE (pass 129); pass 127 classes it SE_e by the nearest range line, so it is added by name'))

OUT=dict(source='pass 137: DigitaltMuseum 021017090086/-089/-090 (1969, PDM); Commons kalmar-slott-9-kalmar.jpg and swe-kalmar-slott-006.jpg; Möller 1882 (PK006-00041) and 1885 (PK006-00049); passes 27, 127, 129, 131, 132, 135. See references/block137-notes.md',
 hearth=H,gron=GR,facade_window=dict(edge=[7,8],hole=WIN,s=S_WIN),rust=['NW','SW','NE'],checks=checks)
(R/'source/block137.json').write_text(json.dumps(OUT,indent=1,ensure_ascii=False))
_wb=Polygon([Wr('SW',S_WIN-.575,-.10),Wr('SW',S_WIN+.575,-.10),Wr('SW',S_WIN+.575,.40),Wr('SW',S_WIN-.575,.40)])
(R/'previews/block137-zones.json').write_text(json.dumps({'pass':137,'zones':dict(
 hearth_plinth=[rnd(p) for p in list(PL.exterior.coords)[:-1]],
 hood_top=[rnd(W(s,c)) for s,c in RINGS[-1][1]],
 facade_window_sw=[rnd(p) for p in list(_wb.exterior.coords)[:-1]],
 grona_end_niche=_niche['foot']),'checks':checks},indent=1,ensure_ascii=False))
print(json.dumps(checks,ensure_ascii=False)[:3000])
print('BLOCK137_PREPARE_OK','hearth r',H['r'],'hood clearance',HK['hood_min_clearance_under_arch_m'],'gron changed',GK['changed_keys'],'window u',U_WIN,'s',GK['s_of_window'],'north tower',NT['decision'])
