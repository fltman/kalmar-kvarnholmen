"""Pass 127: Kalmar slott, the courtyard fronts and the roofs.

Decisions (see references/block127-notes.md for the evidence):
- Courtyard eaves at z 17.01: 6.54 m above the state floor (z 10.47), the mean of Carl Möller's five
  measured sections of 1882 (Gyllene salen 6.38, Förbrända salen 6.54, Unionssalen 6.53, Rutsalen 6.61,
  Kyrkan 6.62). The same sections put the outer eaves 10.02 m above the floor (z 20.49), which agrees
  with pass 27's Street View value (z 20.27) within 0.2 m and so checks the scale and the reference.
- The outer eaves and outer roof planes stay pass 27's. The ridges come down to Möller's 15.0 m above
  the state floor (z 25.47; pass 27 had 26.27 by rule), except the south-west range, whose ridge pass 27
  measured from outside (z 24.79; Möller's Kyrkan 24.56). Each courtyard slope runs from the courtyard
  eaves up to where its range's outer plane reaches that ridge height, so the ridge moves towards the
  outer front, as in Möller's sections (ridge at 0.37-0.41 of the depth from the outer face).
- The roofs are one surface: the upper envelope of all the range slopes, computed here exactly with
  Shapely (each slope keeps only the part where it is the highest), minus the parts inside the round
  towers (cut where the roof meets the tower wall or its copper bell) and inside Kuretornet. Valleys and
  hips are shared edges of two pieces; any step between pieces is listed and closed by a vertical face.
- Window rows on the courtyard fronts (photographs 2017/2022, Möller 1882): see ROWS below.
Output: source/block127.json and previews/block127-zones.json.
Run: KALMAR_GEO=<pylib with shapely> python3 scripts/prepare_block127.py
"""
from pathlib import Path
import json,math,ast,os,sys
if os.environ.get('KALMAR_GEO'):sys.path.insert(0,os.environ['KALMAR_GEO'])
from shapely.geometry import Polygon,LineString,Point,MultiPolygon,box as sbox
from shapely.ops import unary_union
R=Path(__file__).resolve().parents[1]
C27=json.loads((R/'source/castle27.json').read_text());B125=json.loads((R/'source/block125.json').read_text());B126=json.loads((R/'source/block126.json').read_text())
HL=C27['levels_h'];CA=C27['castle']
def zh(h):return round(-1.33+h,4)
FL=B125['floor'];ZC=B126['zc'];ZE=zh(HL['eaves'])

# ---------------------------------------------------------------- Möller 1882 (PK006-00041), measured
# Scale bar: 90 fot = 1549 px on the 7856 x 11828 scan, 17.21 px/fot, 1 fot = 0.2969 m -> 57.97 px/m.
# Pixel rows (full scan) of the state floor, the courtyard eaves (wall top), the outer eaves, the ridge
# and the courtyard ground ("Gård"); columns of the outer face, the courtyard face and the ridge.
PXM=1549/90/.2969
MOLLER={
 'Gyllene salen (59)': dict(floor=9918,court=9548,outer=9335,ridge=9050,gard=10240,x_out=1430,x_court=2405,x_ridge=1800),
 'Förbrända salen (76)':dict(floor=7154,court=6775,outer=6560,ridge=6291,gard=7481,x_out=1477.5,x_court=2377.5,x_ridge=1806),
 'Unionssalen (87)':  dict(floor=7147.5,court=6768.75,outer=6562.5,ridge=6278.75,gard=7500,x_out=6360,x_court=5525,x_ridge=6046),
 'Rutsalen (63)':     dict(floor=9926,court=9543,outer=9569,ridge=9046,gard=10254,x_out=4530,x_court=3345,x_ridge=3842),
 'Kyrkan (86)':       dict(floor=9927,court=9543,outer=9362,ridge=9110,gard=10250,x_out=6253.75,x_court=5647.5,x_ridge=6006),
}
MREAD={}
for k,v in MOLLER.items():
 d=abs(v['x_out']-v['x_court'])/PXM
 MREAD[k]=dict(court_above_floor=round((v['floor']-v['court'])/PXM,2),outer_above_floor=round((v['floor']-v['outer'])/PXM,2),
  ridge_above_floor=round((v['floor']-v['ridge'])/PXM,2),floor_above_gard=round((v['gard']-v['floor'])/PXM,2),court_above_gard=round((v['gard']-v['court'])/PXM,2),
  depth=round(d,2),ridge_from_outer=round(abs(v['x_ridge']-v['x_out'])/PXM/d,2))
COURT_ABOVE_FLOOR=round(sum(v['court_above_floor'] for v in MREAD.values())/len(MREAD),2)
ZCE=round(FL+COURT_ABOVE_FLOOR,2)
OUTER_CHECK=round(sum(v['outer_above_floor'] for k,v in MREAD.items() if k!='Rutsalen (63)')/4,2)   # Rutsalen's outer eaves are low (pre-1885)
RIDGE_ABOVE_FLOOR=round(sum(MREAD[k]['ridge_above_floor'] for k in ('Gyllene salen (59)','Förbrända salen (76)','Unionssalen (87)','Rutsalen (63)'))/4,1)
ZRIDGE=round(FL+RIDGE_ABOVE_FLOOR,2)
assert 16.6<=ZCE<=17.4,ZCE
assert abs(FL+OUTER_CHECK-ZE)<.4,(FL+OUTER_CHECK,ZE)      # the scale and the floor reference check out on the outer eaves
assert ZCE>B125['floor']+B125['rooms']['gyllene']['h']-.2   # above Gyllene salen's ceiling plane (16.67)

# ---------------------------------------------------------------- ranges, planes and slopes
RANGES={r['name']:dict(r) for r in CA['ranges']}
RANGES['SE_w']['s1']+=6.0;RANGES['SE_e']['s0']-=6.0       # as pass 27
OV=.4;WALL=.355                                          # eaves overhang; pass 27's courtyard walls stand 0.355 m into the courtyard from the outline
def rp(r,s,c):o=r['origin'];return (o[0]+r['u'][0]*s+r['n'][0]*c,o[1]+r['u'][1]*s+r['n'][1]*c)
def rframe(r,p):o=r['origin'];dx,dy=p[0]-o[0],p[1]-o[1];return dx*r['u'][0]+dy*r['u'][1],dx*r['n'][0]+dy*r['n'][1]
def halfplane(d,bounds):
 # region where d[0] x + d[1] y + d[2] > 0, clipped to a box
 x0,y0,x1,y1=bounds;pts=[(x0,y0),(x1,y0),(x1,y1),(x0,y1)];out=[]
 f=lambda p:d[0]*p[0]+d[1]*p[1]+d[2]
 for i in range(4):
  p,q=pts[i],pts[(i+1)%4];fp,fq=f(p),f(q)
  if fp>0:out.append(p)
  if (fp>0)!=(fq>0):t=fp/(fp-fq);out.append((p[0]+(q[0]-p[0])*t,p[1]+(q[1]-p[1])*t))
 return Polygon(out) if len(out)>=3 else Polygon()
CI=[tuple(p) for p in CA['court']];CO=[tuple(p) for p in CA['outer']]
COURT=Polygon(CI);OUTLINE=Polygon(CO)
# The courtyard vertices on each range's courtyard front (pass 27's outline, see the notes).
CV={'SW':[0,1,2],'SE_w':[2,3],'SE_e':[3,4,5],'NE':[5,6,7,8],'NW':[8,9,10,0]}
SL={};BB=OUTLINE.buffer(12).bounds
for name,r in RANGES.items():
 half=(r['outer']-r['inner'])/2;rise=min(.93*half,6.0);slo=rise/half          # pass 27's outer plane
 zr=ZE+rise if name=='SW' else ZRIDGE
 cr=r['outer']-(zr-ZE)/slo                                                   # where the outer plane reaches the ridge
 # The courtyard eaves line: fitted through the range's courtyard vertices (least squares), moved to
 # the wall face of the vertex that stands furthest into the courtyard, so that no courtyard wall
 # rises through the roof; where the wall stands further back a filler closes the wall top to the roof.
 pts=[CI[i] for i in CV[name]];mx=sum(p[0] for p in pts)/len(pts);my=sum(p[1] for p in pts)/len(pts)
 sxx=sum((p[0]-mx)**2 for p in pts);syy=sum((p[1]-my)**2 for p in pts);sxy=sum((p[0]-mx)*(p[1]-my) for p in pts)
 th=.5*math.atan2(2*sxy,sxx-syy);e=(math.cos(th),math.sin(th));m=(-e[1],e[0])
 if m[0]*r['n'][0]+m[1]*r['n'][1]<0:m=(-m[0],-m[1])                         # m points from the courtyard towards the outer front
 d0=min(p[0]*m[0]+p[1]*m[1] for p in pts)-WALL
 smid=(r['s0']+r['s1'])/2;X=rp(r,smid,cr);sli=(zr-ZCE)/(X[0]*m[0]+X[1]*m[1]-d0)
 r.update(slo=slo,sli=sli,zr=zr,cr=cr,pass27_ridge=ZE+rise,m=m,d0=d0,skew=round(math.degrees(math.acos(min(1,m[0]*r['n'][0]+m[1]*r['n'][1]))),2),
  vertex_offsets=[round(p[0]*m[0]+p[1]*m[1]-WALL-d0,3) for p in pts])
 n=r['n'];o=r['origin']
 pin=(sli*m[0],sli*m[1],ZCE-sli*d0)                                          # z = A x + B y + C
 pout=(-slo*n[0],-slo*n[1],ZE+slo*(r['outer']+o[0]*n[0]+o[1]*n[1]))
 rect=Polygon([rp(r,r['s0'],r['inner']-6),rp(r,r['s1'],r['inner']-6),rp(r,r['s1'],r['outer']+OV),rp(r,r['s0'],r['outer']+OV)])
 lower_in=halfplane(tuple(pout[i]-pin[i] for i in range(3)),BB)              # where the courtyard plane is the lower one
 eave=halfplane((m[0],m[1],-(d0-OV)),BB)                                     # not beyond the eaves line
 Pin=rect.intersection(lower_in).intersection(eave);Pout=rect.difference(lower_in)
 SL[name+'_in']=dict(range=name,side='in',plane=pin,P=Pin,grad=m)
 SL[name+'_out']=dict(range=name,side='out',plane=pout,P=Pout,grad=(-n[0],-n[1]))
def zp(pl,p):return pl[0]*p[0]+pl[1]*p[1]+pl[2]
# Courtyard side: the roof overhangs the wall faces by 0.4 m, no more; courtyard slopes do not run out
# past the outer fronts (pass 27's north-east slope did, beside Kungsmakstornet).
BAND=COURT.buffer(-(WALL+OV),join_style=2)
for k,v in SL.items():
 v['P']=v['P'].difference(BAND)
 if v['side']=='in':v['P']=v['P'].intersection(OUTLINE.buffer(OV+.05,join_style=2))
ALL=unary_union([v['P'] for v in SL.values()])
keys=list(SL)
for k in keys:
 V=SL[k]['P']
 for j in keys:
  if j==k:continue
  Pj=SL[j]['P']
  if not V.intersects(Pj):continue
  a,b,c=[SL[j]['plane'][i]-SL[k]['plane'][i] for i in range(3)]
  if abs(a)<1e-9 and abs(b)<1e-9:
   if c>1e-6 or (abs(c)<=1e-6 and j<k):V=V.difference(Pj)
   continue
  V=V.difference(Pj.intersection(halfplane((a,b,c-1e-7),BB)))
 SL[k]['V0']=V
# Towers: the roof stops 0.15 m inside the tower wall below the wall top, and inside the copper bell
# above it (the bell profiles of pass 27, build_castle27.py TOWER_SPEC).
src=(R/'scripts/build_castle27.py').read_text();_t=ast.parse(src)
TSPEC=next(eval(compile(ast.Expression(n.value),'TOWER_SPEC','eval'),{'__builtins__':{},'dict':dict}) for n in _t.body if isinstance(n,ast.Assign) and getattr(n.targets[0],'id','')=='TOWER_SPEC')
def Rz(key,z):
 T=CA['towers'][key];r=T['radius'];z1=zh(TSPEC[key]['top'])
 if z<=z1:return r
 prof=[((r+v[0]),v[1]) if v[0]!='a' else (v[1],v[2]) for v in TSPEC[key]['cap'][0][1]]
 for (r0,h0),(r1,h1) in zip(prof,prof[1:]):
  if h0<=z-z1<=h1:return r0+(r1-r0)*(z-z1-h0)/(h1-h0)
 return prof[-1][0]
def tower_cut(key,pl):
 cx,cy=CA['towers'][key]['centre'];pts=[]
 for k in range(144):
  t=k*math.tau/144;d=(math.cos(t),math.sin(t));lo,hi=0.0,CA['towers'][key]['radius']+2
  g=lambda rho:rho-(Rz(key,zp(pl,(cx+d[0]*rho,cy+d[1]*rho)))-.15)
  for _ in range(40):
   mid=(lo+hi)/2
   if g(mid)<0:lo=mid
   else:hi=mid
  pts.append((cx+d[0]*lo,cy+d[1]*lo))
 return Polygon(pts)
kp=[tuple(p) for p in CA['kure']];ek=max(zip(kp,kp[1:]+kp[:1]),key=lambda e:math.dist(*e));ka=math.atan2(ek[1][1]-ek[0][1],ek[1][0]-ek[0][0])
ku=(math.cos(ka),math.sin(ka));kv=(-ku[1],ku[0]);kcx=sum(p[0] for p in kp)/len(kp);kcy=sum(p[1] for p in kp)/len(kp)
us=[(p[0]-kcx)*ku[0]+(p[1]-kcy)*ku[1] for p in kp];vs=[(p[0]-kcx)*kv[0]+(p[1]-kcy)*kv[1] for p in kp]
kcx,kcy=kcx+ku[0]*(max(us)+min(us))/2+kv[0]*(max(vs)+min(vs))/2,kcy+ku[1]*(max(us)+min(us))/2+kv[1]*(max(vs)+min(vs))/2
hu,hv=(max(us)-min(us))/2,(max(vs)-min(vs))/2
KCUT=Polygon([(kcx+ku[0]*a_*(hu-.15)+kv[0]*b_*(hv-.15),kcy+ku[1]*a_*(hu-.15)+kv[1]*b_*(hv-.15)) for a_,b_ in ((-1,-1),(1,-1),(1,1),(-1,1))])
CUTS={}
for k in keys:
 cut=KCUT
 for tk in CA['towers']:cut=cut.union(tower_cut(tk,SL[k]['plane']))
 CUTS[k]=cut;V=SL[k]['V0'].difference(cut)
 V=V.buffer(0)
 # drop crumbs under 1 cm2 left by the cuts
 if isinstance(V,MultiPolygon):V=MultiPolygon([g for g in V.geoms if g.area>1e-4])
 SL[k]['V']=V

# ---------------------------------------------------------------- checks: no gaps, no overlaps
vis=[SL[k]['V'] for k in keys]
ov=sum(vis[i].intersection(vis[j]).area for i in range(len(vis)) for j in range(i+1,len(vis)))
cut_all=unary_union([SL[k]['V0'].intersection(CUTS[k]) for k in keys])
cover=unary_union(vis).union(cut_all)
gap=ALL.difference(cover).area
area_sum=sum(v.area for v in vis)
assert ov<.01,('overlap',ov)
assert gap<.01,('gap',gap)
# Edges between pieces: classify every boundary segment of every piece.
def rings(g):
 gs=[g] if isinstance(g,Polygon) else list(g.geoms)
 return [(list(p.exterior.coords),[list(h.coords) for h in p.interiors]) for p in gs if not p.is_empty]
def z_env(p):
 best=None
 for k in keys:
  if SL[k]['P'].buffer(1e-6).contains(Point(p)):
   z=zp(SL[k]['plane'],p);best=z if best is None or z>best else best
 return best
TOWERS=[(tuple(t['centre']),t['radius']) for t in CA['towers'].values()]
def near_tower(p):
 return any(math.dist(p,c)<r+2.5 for c,r in TOWERS) or KCUT.buffer(.6).contains(Point(p))
steps=[];gables=[];eaves=[];ridges=[];seam_ok=0;tower_edges=0
for k in keys:
 pl=SL[k]['plane'];r=RANGES[SL[k]['range']]
 for ext,holes in rings(SL[k]['V']):
  for ring in [ext]+holes:
   for p,q in zip(ring,ring[1:]):
    L=math.dist(p,q)
    if L<1e-4:continue
    m=((p[0]+q[0])/2,(p[1]+q[1])/2);nx,ny=(q[1]-p[1])/L,-(q[0]-p[0])/L
    a=(m[0]+nx*.02,m[1]+ny*.02);b=(m[0]-nx*.02,m[1]-ny*.02)
    out=a if not SL[k]['V'].contains(Point(a)) else b
    other=[j for j in keys if j!=k and SL[j]['V'].contains(Point(out))]
    zpq=[zp(pl,v) for v in (p,q)]
    if other:
     j=other[0];dz=[zp(pl,v)-zp(SL[j]['plane'],v) for v in (p,q)]
     if max(abs(d) for d in dz)<.005:
      seam_ok+=1
      if SL[j]['range']==SL[k]['range'] and SL[k]['side']=='in':ridges.append(dict(range=SL[k]['range'],a=list(p),b=list(q),z=zpq))
     elif min(dz)>-.005:steps.append(dict(p=p,q=q,z_hi=zpq,z_lo=[zp(SL[j]['plane'],v) for v in (p,q)],piece=k,under=j,o=[out[0]-m[0],out[1]-m[1]]))
    elif near_tower(m):tower_edges+=1
    elif abs(zpq[0]-zpq[1])<=.08*L+.03:eaves.append(dict(p=p,q=q,z=zpq,piece=k,o=[out[0]-m[0],out[1]-m[1]]))
    else:gables.append(dict(p=p,q=q,z=zpq,piece=k,o=[out[0]-m[0],out[1]-m[1]]))
# ---------------------------------------------------------------- seams
seams=[]
for k in keys:
 g=SL[k]['grad'];t=(-g[1],g[0]);V=SL[k]['V'].buffer(-.04)
 if V.is_empty:continue
 cs=[p for e,hs in rings(SL[k]['V']) for p in e]
 tv=[p[0]*t[0]+p[1]*t[1] for p in cs];gv=[p[0]*g[0]+p[1]*g[1] for p in cs]
 off=min(tv)+.31
 while off<max(tv):
  a=(t[0]*off+g[0]*(min(gv)-1),t[1]*off+g[1]*(min(gv)-1));b=(t[0]*off+g[0]*(max(gv)+1),t[1]*off+g[1]*(max(gv)+1))
  x=LineString([a,b]).intersection(V)
  for piece in ([x] if isinstance(x,LineString) else list(getattr(x,'geoms',[]))):
   if isinstance(piece,LineString) and piece.length>.25:seams.append(dict(piece=k,a=list(piece.coords[0]),b=list(piece.coords[-1])))
  off+=.62

# ---------------------------------------------------------------- courtyard wall tops
# Each courtyard wall (pass 27's edges, in its clockwise order) stands to ZCE; where the roof passes
# higher over the wall face, a filler closes the wall top up to 3 cm under the roof surface.
VB=[(k,SL[k]['V'].buffer(.03)) for k in keys]
def z_top(pt):
 zs=[zp(SL[k]['plane'],pt) for k,v in VB if v.contains(Point(pt))];return max(zs) if zs else None
CW=CI[::-1];fillers=[]
for i in range(len(CW)):
 p,q=CW[i],CW[(i+1)%len(CW)];L=math.dist(p,q);nx,ny=(q[1]-p[1])/L,-(q[0]-p[0])/L
 if not COURT.contains(Point((p[0]+q[0])/2+nx*.5,(p[1]+q[1])/2+ny*.5)):nx,ny=-nx,-ny
 zz=[]
 for v in (p,q):
  f=(v[0]+nx*WALL,v[1]+ny*WALL);inner=((p[0]+q[0])/2-v[0],(p[1]+q[1])/2-v[1]);il=math.hypot(*inner)
  f=(f[0]+inner[0]/il*.02,f[1]+inner[1]/il*.02);zz.append(z_top(f))
 assert all(z is not None for z in zz),('no roof over the courtyard wall',i)
 assert min(zz)>ZCE-.005,('courtyard wall rises through the roof',i,zz)
 fillers.append(dict(p=list(p),q=list(q),z=[round(z-.03,4) for z in zz]))
# ---------------------------------------------------------------- chimneys and dormers
# Chimneys: (range, fraction along s, side, metres from that eaves line, width, depth). Courtyard-side
# chimneys stand about 2 m up the courtyard slope, tall, as in the 2017 and 2022 photographs; the
# outer-side ones keep pass 27's positions. Tops 1.6 m over the ridge (pass 27).
CH=[('SW',.40,'in',2.0,1.0,.72),('SW',.58,'in',2.0,1.3,.9),('NW',.22,'out',7.4,1.0,.72),('NW',.50,'in',2.0,1.1,.8),('NW',.74,'out',7.2,1.0,.72),
    ('NE',.26,'in',2.0,1.0,.72),('NE',.52,'out',8.3,1.0,.72),('NE',.80,'in',2.0,1.0,.72),('SE_w',.45,'in',2.0,1.0,.72),('SE_e',.55,'out',7.4,1.0,.72)]
chimneys=[]
for name,f,side,d,w,dep in CH:
 r=RANGES[name];s=r['s0']+(r['s1']-r['s0'])*f;c=r['inner']+d if side=='in' else r['outer']-d
 x,y=rp(r,s,c);ang=math.atan2(r['u'][1],r['u'][0])
 corners=[(x+dx*math.cos(ang)-dy*math.sin(ang),y+dx*math.sin(ang)+dy*math.cos(ang)) for dx in (-w/2,w/2) for dy in (-dep/2,dep/2)]
 zs=[z_env(p) for p in corners];assert all(z is not None for z in zs),name
 assert not near_tower((x,y)),('chimney in a tower',name,f)
 own=SL[name+'_'+side]['V'].contains(Point(x,y))
 chimneys.append(dict(range=name,f=f,side=side,x=x,y=y,w=w,d=dep,ang=ang,z0=min(zs)-.8,z1=RANGES[name]['zr']+1.6,on_own_slope=own))
# Pass 27's courtyard dormers; the west range's moves from 35 % to 62 % along the range, because at
# 35 % it stood within 5 m of the north courtyard corner, under the north range's slope.
DORM=[('SE_w',.5),('NE',.45),('NW',.62),('SW',.55)]
dormers=[]
for name,f in DORM:
 r=RANGES[name];s=r['s0']+(r['s1']-r['s0'])*f;m=r['m'];P0=rp(r,s,r['inner'])
 k_=r['d0']-(P0[0]*m[0]+P0[1]*m[1]);E=(P0[0]+m[0]*k_,P0[1]+m[1]*k_)        # on the eaves line (roof at ZCE)
 dv=(m[1],-m[0]) if m[1]*-r['u'][0]-m[0]*-r['u'][1]>0 else (-m[1],m[0])      # along the line, close to -u as pass 27
 for du in (-1.0,0,1.0):
  for up in (.6,1.5,2.6):
   probe=(E[0]+m[0]*up+dv[0]*du,E[1]+m[1]*up+dv[1]*du)
   assert SL[name+'_in']['V'].contains(Point(probe)),('dormer not on its own slope',name,du,up)
 dormers.append(dict(range=name,f=f,x=E[0],y=E[1],a=math.atan2(dv[1],dv[0]),sli=r['sli']))
# The chapel's roof turret on the south-west ridge (pass 27 at 45.5 % along the range).
rSW=RANGES['SW'];tx,ty=rp(rSW,rSW['s0']+(rSW['s1']-rSW['s0'])*.455,rSW['cr'])

# ---------------------------------------------------------------- courtyard window rows
# (spacing, sill z, width, height), read on the 2014 Street View courtyard panoramas (viewed only;
# zCIfieeXGQUNANmWu_Tg9A, jOXzkLldNOjrveyz1T81wg), each front square on, scaled between the courtyard
# (z 5.47) and the courtyard eaves (z 17.01) on the front itself; see the notes for the readings.
# The ranges as the lead settled them: NW and SW rusticated, NE smooth white, SE_w/SE_e cream lime.
# The state-floor row (pass 126) is shared and kept; where the panoramas put the upper row elsewhere
# the notes say so. Spacing stays 3.8 m on pass 126's axes (measured 3.0-3.6 m, irregular).
STATE=[3.8,B126['court_row']['sill'],B126['court_row']['w'],B126['court_row']['h']]
ROWS={'NW':[STATE,[3.8,8.6,1.05,1.2]],                                   # small row 8.6-9.8 (west part); centre irregular
      'NE':[STATE,[3.8,7.42,1.3,2.2],[3.8,5.71,.8,.65]],                  # full lower row 7.42-9.63; basement windows
      'SW':[STATE,[3.8,9.9,.9,1.2],[3.8,6.77,.9,1.26]],                   # small middle row 9.9-11.1; lower row 6.8-8.0
      'SE_w':[STATE,[3.8,9.95,1.25,1.15],[3.8,6.3,1.25,1.2]],             # small rows 9.95-11.1 and 6.3-7.5 (also 2017)
      'SE_e':[STATE,[3.8,7.75,1.3,2.3]]}                                  # middle row 7.75-10.05
# Rows the panoramas clearly show across the state floor's slab (z 10.17-10.47): no rooms of pass
# 125/126 lie behind them (SW: the chapel range; SE_w, also in the 2017 photograph).
OVER_SLAB={'SW','SE_w'}
for k,rows in ROWS.items():
 for sp,b,w,h in rows[1:]:assert b+h<FL-.3 or k in OVER_SLAB,(k,b,h)
assert all(r[1]+r[3]<ZCE-1.0 for rs in ROWS.values() for r in rs)
# Raised doors with outside stairs (panoramas): NE, the door 11.0 m from the north courtyard corner up 7
# steps; SE_e, the door 2.5 m from the east corner up 9 steps. Edge = courtyard vertices (clockwise as
# the fronts are built), u from the edge's middle.
STAIRS=[dict(edge=[8,7],u=round(11.0-math.dist(CI[8],CI[7])/2,3),risers=7,rise=.2,tread=.30,width=1.5,landing=.9,w=1.0,h=1.9),
        dict(edge=[5,4],u=round(-math.dist(CI[5],CI[4])/2+2.5,3),risers=9,rise=.167,tread=.32,width=2.0,landing=1.2,w=1.0,h=2.0)]
for st in STAIRS:
 L_=math.dist(CI[st['edge'][0]],CI[st['edge'][1]]);assert abs(st['u'])+st['width']/2+.3<L_/2,st
 st.update(p=list(CI[st['edge'][0]]),q=list(CI[st['edge'][1]]),sill=round(ZC+st['risers']*st['rise'],3))

out=dict(source='pass 127: Möller 1882 sections (PK006-00041), pass 27/125/126 levels, photographs 2017/2022; see references/block127-notes.md',
 zc=ZC,zce=ZCE,ze=ZE,floor=FL,zridge=ZRIDGE,moller=MREAD,moller_px_per_m=round(PXM,3),court_above_floor=COURT_ABOVE_FLOOR,outer_check=OUTER_CHECK,
 ranges={k:dict(sli=round(r['sli'],5),slo=round(r['slo'],5),zr=round(r['zr'],4),cr=round(r['cr'],4),pass27_ridge=round(r['pass27_ridge'],3),
   pitch_in=round(math.degrees(math.atan(r['sli'])),1),pitch_out=round(math.degrees(math.atan(r['slo'])),1),ridge_from_outer=round((r['outer']-r['cr'])/(r['outer']-r['inner']),3)) for k,r in RANGES.items()},
 roof=[dict(key=k,range=SL[k]['range'],side=SL[k]['side'],plane=list(SL[k]['plane']),rings=[[[list(map(float,p)) for p in e[:-1]]]+[[list(map(float,p)) for p in h[:-1]] for h in hs] for e,hs in rings(SL[k]['V'])]) for k in keys],
 steps=steps,gables=gables,fillers=fillers,eaves=eaves,seams=seams,ridges=ridges,chimneys=chimneys,dormers=dormers,turret=dict(x=tx,y=ty,z=rSW['zr']),rows=ROWS,stairs=STAIRS,over_slab=sorted(OVER_SLAB),
 checks=dict(overlap_m2=round(ov,5),gap_m2=round(gap,5),visible_m2=round(area_sum,2),plan_m2=round(ALL.area,2),cut_m2=round(cut_all.area,2),
  shared_edges=seam_ok,steps=len(steps),step_max=round(max([max(abs(a-b) for a,b in zip(s_['z_hi'],s_['z_lo'])) for s_ in steps],default=0),3),
  gables=len(gables),gable_len=round(sum(math.dist(g['p'],g['q']) for g in gables),2),tower_edges=tower_edges,eave_segments=len(eaves),filler_max=round(max(max(f['z'])+.03-ZCE for f in fillers),3),seams=len(seams),ridges=len(ridges)))
(R/'source/block127.json').write_text(json.dumps(out,indent=1))
zones={k:dict(range=SL[k]['range'],side=SL[k]['side'],visible_m2=round(SL[k]['V'].area,2),slope_m2=round(SL[k]['P'].area,2)) for k in keys}
(R/'previews/block127-zones.json').write_text(json.dumps(dict(pieces=zones,checks=out['checks'],ranges=out['ranges']),indent=1))
print(json.dumps(out['checks']));print(json.dumps(out['ranges'],ensure_ascii=False));print(json.dumps(MREAD,ensure_ascii=False))
print('ZCE',ZCE,'ZRIDGE',ZRIDGE,'outer check',round(FL+OUTER_CHECK,2))
print('BLOCK127_PREPARE_OK')
