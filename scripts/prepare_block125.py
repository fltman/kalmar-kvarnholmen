"""Pass 125: the first interior rooms of Kalmar slott, on the state floor (praktvåningen) of the
west range: Gyllene salen (Olsson's room 59), Kungsmaket (room 62, in Kungsmakstornet, tower II)
and, between them, a plain stand-in for room 61a (Panelade salen, now part of Grå salen), through
which Kungsmaket is reached.

Where the rooms stand (Olsson, Fornvännen 1974, fig. 1, read but not copied; scale bar 4.28 px/m
in the DiVA scan): along the west range from tower II to Kuretornet the rooms are 62 (in the round
tower), 61a, 59 and then Kuretornet (56). The plan's distance from tower II's centre to
Kuretornet's north-east face is 25.7 m, pass 27's model (OpenStreetMap) has 23.5 m, so the plan's
lengths along the range are scaled by 0.92 to fit the model. Pass 27's frame for the range (the
'NW' range: s along the outer front from the north tower towards the west tower, c outwards) is
used throughout.

Levels: pass 27 measured the outer main-floor windows at 7.9-11.1 m above the castle foot. The
interior photographs show the glazing sill about 0.9 m above the floor, so the state floor is put
0.92 m below the outer sill.

Output (source/block125.json): the range frame, the rooms in (s,c), the floor, the window positions
of pass 27's fronts (outer main row, courtyard first row) as pass 27 computes them, the tower door
cut, and Gyllene salen's coffered ceiling as 2D polygons in the room's own frame (Mandelgren's plan
of 1848: four by four large coffers, elongated coffers along every rib, X-shaped node fields with a
boss at every crossing). The flat soffit between the coffers is triangulated here (Shapely).
Run with Shapely: KALMAR_GEO=<site-packages> python3 scripts/prepare_block125.py
"""
from pathlib import Path
import json,math,os,sys
if os.environ.get('KALMAR_GEO'):sys.path.insert(0,os.environ['KALMAR_GEO'])
from shapely.geometry import Polygon,Point,box
from shapely.ops import unary_union
from shapely import constrained_delaunay_triangles
R=Path(__file__).resolve().parents[1]
C27=json.loads((R/'source/castle27.json').read_text());B124=json.loads((R/'source/block124.json').read_text())
CA=C27['castle'];CO=[tuple(p) for p in CA['outer']]
# The frame follows pass 27's outer front of the west range from point 55 to 56 (the fitted range axis
# of pass 27 is 3.8 degrees off it): s along the front from the north tower, c outwards.
O=CO[55];_d=(CO[56][0]-O[0],CO[56][1]-O[1]);_L=math.hypot(*_d);U=(_d[0]/_L,_d[1]/_L);N=(U[1],-U[0])
def W(s,c):return (O[0]+U[0]*s+N[0]*c,O[1]+U[1]*s+N[1]*c)
def F(p):dx,dy=p[0]-O[0],p[1]-O[1];return (dx*U[0]+dy*U[1],dx*N[0]+dy*N[1])
def zh(h):return round(-1.33+h,4)
Z0=zh(C27['levels_h']['foot']);ZC=zh(C27['levels_h']['courtyard'])
CI=[tuple(p) for p in CA['court']]
TN=CA['towers']['N'];TS,TC=F(TN['centre']);TR=TN['radius']

# ---------------------------------------------------------------- levels
SILL_OUT=Z0+7.9;TOP_OUT=Z0+11.1            # pass 27: outer main-floor windows (Street View, measured)
FLOOR=round(SILL_OUT-1.10,3)                # interior photographs: glazing sill about one glass width (1.0-1.3) above the floor
SILL_COURT=ZC+5.6                           # pass 27: courtyard first-floor windows
H_GYLL=6.20                                 # floor to the coffer soffit (photographs scaled on the glass width; see notes)
H_KUNG=4.30                                 # floor to the ceiling soffit (panorama: panelling 2.6 m = 0.6 of the wall)

# ---------------------------------------------------------------- pass 27's window positions
def row_holes(L,spacing,w,margin=1.6):
 n=max(1,int((L-2*margin)/spacing)+1) if L>2*margin+w else 0
 return [-(n-1)*spacing/2+k*spacing for k in range(n) if abs(-(n-1)*spacing/2+k*spacing)+w/2<L/2-.4]
def edge_s(p,q,us):
 (s0,c0),(s1,c1)=F(p),F(q);L=math.dist(p,q)
 return [round((s0+s1)/2+(s1-s0)/L*u,3) for u in us],round((c0+c1)/2,3)
OUTER=edge_s(CO[55],CO[56],row_holes(math.dist(CO[55],CO[56]),4.4,1.15))        # the outer front 55-56
COURT=edge_s(CI[9],CI[8],row_holes(math.dist(CI[9],CI[8]),3.8,1.2))             # courtyard piece V-N

# ---------------------------------------------------------------- rooms (s along the range, c outwards)
# Kuretornet's north-east face runs from s 18.2 (outer) to 17.4 (c -11); its 0.35 m skin is outside
# the outline, so the room's south wall stops at s 16.95. The gate passage (pass 124) lies at s 17.7
# and beyond.
ROOMS={
 'gyllene':dict(s0=4.60,s1=17.00,c0=-15.00,c1=-2.10,h=H_GYLL),
 'forrum':dict(s0=0.30,s1=3.20,c0=-11.50,c1=-0.50,h=4.50),
 'kungsmak':dict(s0=round(TS-3.0,3),s1=round(TS+3.0,3),c0=round(TC-2.8,3),c1=round(TC+2.8,3),h=H_KUNG),
}
# Walls (s or c ranges): Gyllene salen's north wall (shared with 61a), its south wall against
# Kuretornet (whose 0.35 m skin reaches s 17.75), the courtyard wall and its window layer, which stop
# 0.03 m short of pass 27's courtyard front where it comes closest (s 17.7).
WALL={'gyllene':dict(n=(3.20,4.60),s=(17.00,17.70),o=(-.28,-.05),e=(-16.35,-16.70))}
# Openings. Gyllene salen: the two outer windows that fall in the room (pass 27's positions), the
# courtyard window that falls in it, the door to 61a in the north wall, three closed doors.
gw_out=[s for s in OUTER[0] if ROOMS['gyllene']['s0']+1.0<s<ROOMS['gyllene']['s1']-1.0]
gw_court=[s for s in COURT[0] if ROOMS['gyllene']['s0']+1.0<s<ROOMS['gyllene']['s1']-1.0]
DOORS={'gyllene_forrum':dict(c=-10.0,w=1.1,h=2.35),'forrum_kungsmak':dict(c=-1.2,w=1.0,h=2.25)}
# Kungsmaket's door passage crosses pass 27's closed tower cylinder (radius 6.35) here; the build cuts
# this box out of the cylinder's skin. It lies inside the range, under its roof, out of sight.
cy_s=TS+math.sqrt(TR**2-(DOORS['forrum_kungsmak']['c']-TC)**2)
CUT=dict(s0=round(cy_s-.6,3),s1=round(cy_s+.6,3),c0=-1.75,c1=-.65,z0=round(FLOOR-.05,3),z1=round(FLOOR+DOORS['forrum_kungsmak']['h']+.05,3))

# ---------------------------------------------------------------- Gyllene salen's coffered ceiling
# Room frame: x along s from the room's centre, y along c. Four by four large coffers (octagons:
# squares with chamfered corners), an elongated hexagonal coffer along every rib between two nodes,
# a flat X-shaped field at every node. Band half-width h, node tip t, a flat rim at the walls.
g=ROOMS['gyllene'];LX=g['s1']-g['s0'];LY=g['c1']-g['c0'];HB=.45;TT=.25;RIM=.10
px=(LX-2*(HB+RIM))/4;py=(LY-2*(HB+RIM))/4
xs=[-LX/2+RIM+HB+k*px for k in range(5)];ys=[-LY/2+RIM+HB+k*py for k in range(5)]
octs=[];hexs=[];nodes=[]
for i in range(4):
 for j in range(4):
  x0,y0,x1,y1=xs[i],ys[j],xs[i+1],ys[j+1]
  octs.append([(x0+TT+HB,y0+HB),(x1-TT-HB,y0+HB),(x1-HB,y0+TT+HB),(x1-HB,y1-TT-HB),(x1-TT-HB,y1-HB),(x0+TT+HB,y1-HB),(x0+HB,y1-TT-HB),(x0+HB,y0+TT+HB)])
for j in range(5):
 for i in range(4):
  x0,x1,y=xs[i],xs[i+1],ys[j];hexs.append([(x0+TT,y),(x0+TT+HB,y-HB),(x1-TT-HB,y-HB),(x1-TT,y),(x1-TT-HB,y+HB),(x0+TT+HB,y+HB)])
for i in range(5):
 for j in range(4):
  y0,y1,x=ys[j],ys[j+1],xs[i];hexs.append([(x,y0+TT),(x+HB,y0+TT+HB),(x+HB,y1-TT-HB),(x,y1-TT),(x-HB,y1-TT-HB),(x-HB,y0+TT+HB)])
nodes=[(x,y) for x in xs for y in ys]
# Each coffer stands 0.10 m inside its tile, so a flat cream strip 0.2 m wide runs between neighbours
# (ceiling photograph 2017).
MG=.10
def inset(poly,d):
 n=len(poly);area=sum(poly[i][0]*poly[(i+1)%n][1]-poly[(i+1)%n][0]*poly[i][1] for i in range(n));sg=1 if area>0 else -1;out=[]
 for i in range(n):
  a,b,c=poly[i-1],poly[i],poly[(i+1)%n]
  e1=((b[0]-a[0]),(b[1]-a[1]));l1=math.hypot(*e1);e1=(e1[0]/l1,e1[1]/l1);e2=((c[0]-b[0]),(c[1]-b[1]));l2=math.hypot(*e2);e2=(e2[0]/l2,e2[1]/l2)
  n1=(-e1[1]*sg,e1[0]*sg);n2=(-e2[1]*sg,e2[0]*sg);p1=(a[0]+n1[0]*d,a[1]+n1[1]*d);p2=(b[0]+n2[0]*d,b[1]+n2[1]*d)
  den=e1[0]*e2[1]-e1[1]*e2[0];t=((p2[0]-p1[0])*e2[1]-(p2[1]-p1[1])*e2[0])/den;out.append((round(p1[0]+e1[0]*t,4),round(p1[1]+e1[1]*t,4)))
 return out
octs=[inset(p,MG) for p in octs];hexs=[inset(p,MG) for p in hexs]
ceil=box(-LX/2,-LY/2,LX/2,LY/2);cof=unary_union([Polygon(p) for p in octs+hexs])
flat=ceil.difference(cof)
tris=[]
for t in constrained_delaunay_triangles(flat).geoms:
 c=list(t.exterior.coords)[:3]
 if Polygon(c).area>1e-5:tris.append([[round(v,4) for v in q] for q in c])
flat_area=sum(Polygon(t).area for t in tris)

# ---------------------------------------------------------------- checks
checks={}
outer=Polygon(CO);kure=Polygon(CA['kure']).buffer(.36);court=Polygon(CI);tower=Point(CA['towers']['N']['centre']).buffer(TR,64)
def rpoly(r):return Polygon([W(r['s0'],r['c0']),W(r['s1'],r['c0']),W(r['s1'],r['c1']),W(r['s0'],r['c1'])])
zones={}
for k,r in ROOMS.items():
 P=rpoly(r);zones[k]=[list(map(lambda v:round(v,3),p)) for p in P.exterior.coords][:-1]
 checks[k+'_inside_castle']=round(P.difference(outer).area,4)
 checks[k+'_in_kure']=round(P.intersection(kure).area,4)
 checks[k+'_in_court']=round(P.intersection(court).area,4)
 checks[k+'_m2']=round(P.area,2)
# The whole envelope of Gyllene salen's walls must stay inside pass 27's outline (its skins lie outside
# the outer ring, inside the courtyard ring and outside Kuretornet's ring).
GW_=WALL['gyllene'];env=unary_union([Polygon([W(GW_['n'][0],GW_['e'][1]),W(GW_['s'][0],GW_['e'][1]),W(GW_['s'][0],-.05),W(GW_['n'][0],-.05)]),Polygon([W(GW_['s'][0],GW_['e'][1]),W(GW_['s'][1],GW_['e'][1]),W(GW_['s'][1],-.12),W(GW_['s'][0],-.12)])])
checks['gyllene_walls_outside_castle']=round(env.difference(outer).area,4);checks['gyllene_walls_in_court']=round(env.intersection(court).area,4)
checks['gyllene_walls_in_kure']=round(env.intersection(kure).area,4)
assert checks['gyllene_walls_outside_castle']<.001 and checks['gyllene_walls_in_court']<.001 and checks['gyllene_walls_in_kure']<.001,checks
checks['gyllene_in_tower']=round(rpoly(ROOMS['gyllene']).intersection(tower).area,4)
checks['forrum_in_tower']=round(rpoly(ROOMS['forrum']).intersection(tower).area,4)
checks['kungsmak_outside_tower']=round(rpoly(ROOMS['kungsmak']).difference(tower).area,4)
# The gate passage (pass 124): OSM line moved 0.9 m towards Kuretornet's south-west face, 3.0 m wide
# with 0.3 m walls. Its nearest edge to Gyllene salen's south wall:
ps=[F(p) for p in B124['gate']['passage']]
checks['passage_min_s_edge']=round(min(s for s,c in ps)+.9-1.8,3)
checks['gyllene_south_wall_s']=WALL['gyllene']['s'][1]
checks['ceiling_cover_m2']=round(flat_area+cof.area-ceil.area,4)
checks['ceiling_flat_triangles']=len(tris)
assert all(checks[k+'_inside_castle']<.01 and checks[k+'_in_kure']<.01 and checks[k+'_in_court']<.01 for k in ROOMS),checks
assert checks['gyllene_in_tower']<.01 and checks['forrum_in_tower']<.01 and checks['kungsmak_outside_tower']<.01,checks
assert checks['passage_min_s_edge']>checks['gyllene_south_wall_s']+.3,checks
assert abs(checks['ceiling_cover_m2'])<.02,checks
assert len(gw_out)==2 and len(gw_court)==1,(gw_out,gw_court)
# Mismatches reported, not corrected: Kungsmaket's west niche against pass 27's tower window.
t0=math.atan2(TN['centre'][1]-sum(p[1] for p in CO)/len(CO),TN['centre'][0]-sum(p[0] for p in CO)/len(CO))
tw=(math.cos(t0)*U[0]+math.sin(t0)*U[1],math.cos(t0)*N[0]+math.sin(t0)*N[1])
checks['tower_window_angle_from_west_niche_deg']=round(math.degrees(math.atan2(-tw[0],tw[1])),1)
checks['outer_windows_s']=OUTER[0];checks['court_windows_s']=COURT[0]
checks['floor_z']=FLOOR;checks['court_sill_above_floor']=round(SILL_COURT-FLOOR,3);checks['outer_sill_above_floor']=round(SILL_OUT-FLOOR,3)
data=dict(source='pass 125: Olsson 1974 fig. 1 (read only), Mandelgren 1848, photographs; pass 27 frame and windows',
 frame=dict(origin=O,u=U,n=N),floor=FLOOR,z0=Z0,zc=ZC,sill_out=SILL_OUT,top_out=TOP_OUT,sill_court=SILL_COURT,
 tower=dict(s=round(TS,3),c=round(TC,3),r=TR,t0_sc=[round(v,4) for v in tw]),rooms=ROOMS,walls=WALL,doors=DOORS,cut=CUT,
 windows=dict(gyllene_outer=gw_out,gyllene_court=gw_court,outer_row=OUTER[0],court_row=COURT[0],court_c=COURT[1]),
 ceiling=dict(lx=LX,ly=LY,xs=xs,ys=ys,band=HB,tip=TT,octs=octs,hexs=hexs,nodes=nodes,flat=tris))
(R/'source/block125.json').write_text(json.dumps(data,separators=(',',':')))
(R/'previews/block125-zones.json').write_text(json.dumps(dict(**{'pass':125},rooms=zones,checks=checks),indent=1))
print('BLOCK125_PREPARE_OK',json.dumps(checks))
