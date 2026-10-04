"""Pass 132: Kalmar slott, the tower caps (corrects passes 27, 124, 125 and 126 on SM_Kalmar_Slott_Towers).

Carl Möller drew new roofs for the five towers in May-September 1885 (Riksarkivet PK006-00048..52,
public domain): an elevation, a plan and a section each, dimensioned in fot (0.2969 m). This pass
builds the caps from those sheets (scripts/prepare_block132.py reads them into source/block132.json):
- Kuretornet ("Vattentornet" on the sheet): the square bell roof with Möller's profile, a lucarne
  with columns, an arched head and a fan on each face, an aedicule on each corner (pedestal, column,
  entablature, box, ball finial), the octagonal plinth, the open octagonal lantern with paired corner
  columns and arched openings, the entablature, the octagonal dome, the neck, the bulb, the ball, the
  candelabra and the crown.
- The four round towers: polygonal bells (N 12, S 16, W 10, E 16 sides, from the plans) with copper
  ribs on the corners and, on W, S and E, the scalloped valance under the eaves; closed polygonal
  drums with corner pilasters; then N: neck and onion, ball, fleur and vane; S: ogee dome, small
  lantern with spikes, fleur and vane; W: neck, torus, tall pear bulb, disc, ball, crown ring and vane;
  E: neck, cushion, bulb, disc, ball, fleur and vane. The photographs (2017, 2019, 2020, 2022) show the
  same caps today (see the notes).
- Vertical sizes are Möller's, in metres. Horizontally the bells are scaled so that the drawn wall
  meets the model's wall (OSM radius); the scale runs linearly to Möller's own scale at the bell's top,
  so everything above the bell has Möller's dimensions. The walls and wall tops are not changed.
- Where pass 127's range roofs run into a bell (they were cut 0.15 m inside pass 27's bell), the new
  bell is kept out to pass 27's bell less 0.05 m under the roof (a ray up from the point meets the
  roof), so no gap opens between a roof and a cap.

The mesh is re-created the way pass 126 and 127 did: pass 126's composition of pass 124's code (which
re-runs pass 27's) is run in a private namespace with single, asserted string replacements, here
only the towers section, with the cap loop and Kuretornet's roof replaced. Pass 125's cut for
Kungsmaket's door passage is applied again afterwards.
Sources: references/block132-notes.md.
"""
import re,ast
from mathutils import Vector
from mathutils.bvhtree import BVHTree
# Pass 125 leaves numbers in the shared names TS and TC, which the town helpers read as materials.
if not isinstance(TS,str):TS=town_mats['Stone']
if not isinstance(TC,str):TC='M_Town_Copper'
B132D=json.loads((R/'source/block132.json').read_text())
block132_names=[];FOT132=B132D['fot']

def drop_degenerate_faces132(obj,tol=1e-9):
 # Faces with no area, a repeated corner or a width under 0.1 mm have no UV frame for the export.
 import bmesh
 bm=bmesh.new();bm.from_mesh(obj.data)
 def _thin(f):
  L=max(e.calc_length() for e in f.edges);return L>0 and 2*f.calc_area()/L<1e-4
 bad=[f for f in bm.faces if f.calc_area()<tol or len({v.index for v in f.verts})<len(f.verts) or _thin(f)]
 if bad:bmesh.ops.delete(bm,geom=bad,context='FACES_ONLY')
 bm.to_mesh(obj.data);bm.free();obj.data.update();return len(bad)
def mark132(obj):
 obj['block132_dropped_faces']=drop_degenerate_faces132(obj);print('BLOCK132_DROPPED',obj.name,obj['block132_dropped_faces'],len(obj.data.polygons))
 obj['detail_pass']=132;obj['reference_notes']='references/block132-notes.md'
 obj['osm_way']=','.join(t['osm_way'] for t in json.loads((R/'source/castle27.json').read_text())['castle']['towers'].values())
 obj['corrects_pass']='27,124,125,126'
 if obj.name not in block132_names:block132_names.append(obj.name)
 return obj
def rep132(src,old,new):
 assert src.count(old)==1,('source changed',src.count(old),old[:80]);return src.replace(old,new)

# ---------------------------------------------------------------- pass 27's bells, for the roof joint
# Pass 127 cut the range roofs 0.15 m inside these bells (prepare_block127.py, Rz).
_t27=ast.parse((R/'scripts/build_castle27.py').read_text())
TSPEC132=next(eval(compile(ast.Expression(n.value),'TOWER_SPEC','eval'),{'__builtins__':{},'dict':dict}) for n in _t27.body if isinstance(n,ast.Assign) and getattr(n.targets[0],'id','')=='TOWER_SPEC')
def rold132(key,z):
 T=B132D['towers'][key];r=T['radius'];z1=round(-1.33+TSPEC132[key]['top'],4)
 if z<=z1:return r
 prof=[((r+v[0]),v[1]) if v[0]!='a' else (v[1],v[2]) for v in TSPEC132[key]['cap'][0][1]]
 for (r0,h0),(r1,h1) in zip(prof,prof[1:]):
  if h0<=z-z1<=h1:return r0+(r1-r0)*(z-z1-h0)/(h1-h0)
 return prof[-1][0]
def _roof_tree132():
 import bmesh
 o=bpy.data.objects['SM_Kalmar_Slott'];bm=bmesh.new();bm.from_mesh(o.data);bm.transform(o.matrix_world)
 t=BVHTree.FromBMesh(bm);bm.free();return t
ROOF132=_roof_tree132()
def under_roof132(x,y,z):
 loc,_,_,_=ROOF132.ray_cast(Vector((x,y,z)),Vector((0,0,1)),20.0);return loc is not None

# ---------------------------------------------------------------- the cap builders (run inside NS124)
EXTRA132=r'''
F132=B132D['fot']
def ring132(cx,cy,z,a,n,sub,rot):
 # A polygon of n sides with apothem a and a corner at angle rot; each side split in sub parts.
 R_=a/math.cos(math.pi/n);pts=[]
 for j in range(n):
  t0_=rot+j*math.tau/n;t1_=t0_+math.tau/n
  p0=(cx+R_*math.cos(t0_),cy+R_*math.sin(t0_));p1=(cx+R_*math.cos(t1_),cy+R_*math.sin(t1_))
  for s in range(sub):f=s/sub;pts.append((p0[0]+(p1[0]-p0[0])*f,p0[1]+(p1[1]-p0[1])*f,z))
 return pts
def skin132(m,rings,ma,bottom=False,top=True,smooth=False):
 # Rings (counter-clockwise, equal length, or a single point for a tip) joined by quads; tips and
 # caps are triangle fans, so there is no large n-gon and no collapsed quad at a tip.
 rr=[]
 for rg in rings:
  if rr and len(rg)==len(rr[-1]) and all(math.dist(p,q)<1e-6 for p,q in zip(rg,rr[-1])):continue
  rr.append(rg)
 V=[];idx=[]
 for rg in rr:idx.append(list(range(len(V),len(V)+len(rg))));V.extend(rg)
 Fc=[]
 for A,B in zip(idx,idx[1:]):
  if len(A)==1 and len(B)==1:continue
  if len(A)==1:N=len(B);Fc+=[(A[0],B[(i+1)%N],B[i]) for i in range(N)]
  elif len(B)==1:N=len(A);Fc+=[(A[i],A[(i+1)%N],B[0]) for i in range(N)]
  else:N=len(A);Fc+=[(A[i],A[(i+1)%N],B[(i+1)%N],B[i]) for i in range(N)]
 for k,sel in ((0,bottom),(-1,top)):
  rg=rr[k]
  if not sel or len(rg)==1:continue
  c=(sum(p[0] for p in rg)/len(rg),sum(p[1] for p in rg)/len(rg),rg[0][2]);ci=len(V);V.append(c);A=idx[k];N=len(A)
  Fc+=[(ci,A[(i+1)%N],A[i]) for i in range(N)] if k==0 else [(A[i],A[(i+1)%N],ci) for i in range(N)]
 m.faces(V,Fc,ma,smooth);return [[V[i] for i in A] for A in idx]
def lathe132(m,cx,cy,z0,prof,ma,n,rot,sub=1,bottom=False,top=True,smooth=False):
 # prof: (h, apothem) in metres above z0; apothem 0 is a tip.
 rings=[[(cx,cy,z0+h)] if a<1e-4 else ring132(cx,cy,z0+h,a,n,sub,rot) for h,a in prof]
 return skin132(m,rings,ma,bottom,top,smooth)
def sphere132(m,cx,cy,zc,r,ma,n=16):
 prof=[(-r,0)]+[(r*math.sin(math.radians(a)),r*math.cos(math.radians(a))) for a in range(-75,90,15)]+[(r,0)]
 lathe132(m,cx,cy,zc,[(h,a) for h,a in prof],ma,n,0,smooth=True)
def frame132(fx,fy,th):
 n_=(math.cos(th),math.sin(th));t_=(-n_[1],n_[0])
 return lambda u,o,z:(fx+u*t_[0]+o*n_[0],fy+u*t_[1]+o*n_[1],z)
def fbox132(m,P,th,u0,u1,o0,o1,z0,z1_,ma):
 # A box in a face frame (u along the face, o outwards).
 m.box(P((u0+u1)/2,(o0+o1)/2,(z0+z1_)/2),(u1-u0,o1-o0,z1_-z0),ma,th+math.pi/2)
def fanprism132(m,P,pts,o0,o1,ma):
 # A flat shape (u,z) built as a triangle fan round its centroid and extruded from o0 to o1.
 n=len(pts);cu=sum(p[0] for p in pts)/n;cz=sum(p[1] for p in pts)/n
 V=[P(u,o,z) for o in (o0,o1) for u,z in [(cu,cz)]+list(pts)];k=n+1
 f=[(0,1+(i+1)%n,1+i) for i in range(n)]+[(k,k+1+i,k+1+(i+1)%n) for i in range(n)]
 f+=[(1+i,1+(i+1)%n,k+1+(i+1)%n,k+1+i) for i in range(n)]
 m.faces(V,f,ma)
def archpanel132(m,P,hw,zi,zt,rr,o0,o1,ma,K_=12):
 # The wall over a round-headed opening: the rectangle |u|<=hw, zi<=z<=zt less the half disc of
 # radius rr round (0,zi); quads between the arc and the rectangle, a soffit along the arc.
 fc=math.atan2(zt-zi,hw);phis=sorted(set([math.pi*k/K_ for k in range(K_+1)]+[fc,math.pi-fc]))
 def rect(p):
  c,s=math.cos(p),math.sin(p);ts=[]
  if abs(c)>1e-9:ts.append(hw/abs(c))
  if s>1e-9:ts.append((zt-zi)/s)
  t=min(ts);return (t*c,zi+t*s)
 arc=[(rr*math.cos(p),zi+rr*math.sin(p)) for p in phis];out=[rect(p) for p in phis];N=len(phis)
 V=[P(u,o,z) for o in (o1,o0) for u,z in arc+out]
 f=[]
 for s,b in ((0,0),(1,2*N)):
  for i in range(N-1):
   q=(b+i,b+N+i,b+N+i+1,b+i+1);f.append(q if s==0 else q[::-1])
 for i in range(N-1):f.append((i+1,2*N+i+1,2*N+i,i))                    # soffit
 for i in range(N-1):f.append((N+i,2*N+N+i,2*N+N+i+1,N+i+1))           # top and sides
 m.faces(V,f,ma)
def fleur132(m,cx,cy,z,a,ma,s=1.0):
 # The wrought-iron fleur: two curled leaves and a bud in each of two planes.
 for k in range(2):
  P=frame132(cx,cy,a+k*math.pi/2)
  for sg in (-1,1):
   leaf=[(sg*.04*s,0),(sg*.22*s,.10*s),(sg*.40*s,.26*s),(sg*.44*s,.38*s),(sg*.34*s,.34*s),(sg*.20*s,.22*s),(sg*.04*s,.16*s)]
   fanprism132(m,P,[(u,z+zz) for u,zz in leaf],-.012,.012,ma)
  fanprism132(m,P,[(0,z-.05*s),(.07*s,z+.15*s),(0,z+.42*s),(-.07*s,z+.15*s)],-.015,.015,ma)
def vane132(m,cx,cy,z,a,ma,L=1.45,H=.30):
 # The weather vane: a swallow-tailed plate on the rod, a bar with scrolled ends above it.
 P=frame132(cx,cy,a)
 fanprism132(m,P,[(.06,z-H/2),(L,z-H/2),(L-.22,z),(L,z+H/2),(.06,z+H/2)],-.01,.01,ma)
 town_rod(m,P(-.30,0,z+H/2+.07),P(L+.05,0,z+H/2+.07),.018,ma,6)
 for u_ in (-.30,L+.05):lathe132(m,*P(u_,0,0)[:2],z+H/2+.02,[(0,0),(.05,.06),(.10,0)],ma,8,0)

def bulge132(key,cx,cy,pts,z):
 # Under a range roof the bell is kept out to pass 27's bell less 0.05 m (the roof was cut 0.15 m
 # inside it), so the roof's cut edge stays covered.
 ro=rold132(key,z)-.05;out=[]
 for x,y,zz in pts:
  d=math.hypot(x-cx,y-cy)
  if d<ro:
   ux,uy=(x-cx)/d,(y-cy)/d;q=(cx+ux*ro,cy+uy*ro)
   # tested 0.2 m lower and half a vertex step to each side, so the face from the last bulged ring
   # to the next one up, and between neighbouring vertices, stays outside the roof's cut edge
   tt=math.atan2(uy,ux);ok=False
   for dt in (0,-.035,.035):
    if under_roof132(cx+ro*math.cos(tt+dt),cy+ro*math.sin(tt+dt),zz-.2):ok=True;break
   if ok:x,y=q;BULGED132.append(key)
  out.append((x,y,zz))
 return out
BULGED132=[]

def caps132(m,key,cx,cy,r,z1,t0):
 T=B132D['towers'][key];F=F132;nb=T['n_bell'];nu=T['n_up'];hb=T['bell_top'];k0=T['k_eaves']
 kk=lambda h:k0+(F-k0)*min(1,max(0,h/hb))
 rotb=t0-math.pi/nb;rotu=t0-math.pi/nu;sub=8;CU=K['Copper'];CD=K['CopperDark']
 # The soffit from inside the wall top to the bell's eaves.
 base=ring132(cx,cy,z1,T['bell'][0][1]*k0,nb,sub,rotb)
 inner=[(cx+(r-.06)*(p[0]-cx)/math.hypot(p[0]-cx,p[1]-cy),cy+(r-.06)*(p[1]-cy)/math.hypot(p[0]-cx,p[1]-cy),z1) for p in base]
 skin132(m,[inner,base],SIGN,top=False)
 # The bell: Möller's outline, polygonal, ribs on the corners.
 rings=[]
 for h,half in T['bell']:
  z=z1+h*F;rg=ring132(cx,cy,z,half*kk(h),nb,sub,rotb)
  if z<z1+3.2:rg=bulge132(key,cx,cy,rg,z)
  rings.append(rg)
 rings=skin132(m,rings,CU)
 for j in range(nb):
  pts=[]
  for rg in rings[1:]:
   x,y,z=rg[j*sub];d=math.hypot(x-cx,y-cy);pts.append((cx+(x-cx)*(d+.03)/d,cy+(y-cy)*(d+.03)/d,z))
  town_path(m,pts,.035,CU)
 # The scalloped valance under the eaves (W, S, E): cusps on the corners, arcs between.
 if T['valance']>0:
  zt=z1-T['cornice']*F;D=T['valance']*F;av=r+.27
  for j in range(nb):
   c0=ring132(cx,cy,0,av,nb,1,rotb)[j];c1=ring132(cx,cy,0,av,nb,1,rotb)[(j+1)%nb]
   if True:
    us=[i/10 for i in range(11)]
    def pt(u,dd,z):
     x=c0[0]+(c1[0]-c0[0])*u;y=c0[1]+(c1[1]-c0[1])*u;d=math.hypot(x-cx,y-cy);return (cx+(x-cx)*(d-dd)/d,cy+(y-cy)*(d-dd)/d,z)
    zb=lambda u:zt-D+D*.78*math.sin(math.pi*u)
    V=[pt(u,0,zt) for u in us]+[pt(u,0,zb(u)) for u in us]+[pt(u,.04,zt) for u in us]+[pt(u,.04,zb(u)) for u in us];N=11
    f=[(i,i+1,N+i+1,N+i) for i in range(N-1)]+[(2*N+i,3*N+i,3*N+i+1,2*N+i+1) for i in range(N-1)]
    f+=[(N+i,N+i+1,3*N+i+1,3*N+i) for i in range(N-1)]+[(i,2*N+i,2*N+i+1,i+1) for i in range(N-1)]
    m.faces(V,f,CU)
 # Drum, necks and bulbs: one faceted lathe from the bell's top.
 for part in T['parts']:
  kind,n,data=part
  if kind=='poly':
   prof=[(h*F,a*F) for h,a in data];lathe132(m,cx,cy,z1,prof,CU,n,rotu,bottom=True)
   PROF132[key]=prof
  elif kind=='pilasters':
   h0,h1=data;body=min(a for h,a in PROF132[key] if h0*F-1e-6<=h<=h1*F+1e-6)
   for j in range(n):
    t=rotu+j*math.tau/n;Rc=body/math.cos(math.pi/n)
    m.box((cx+(Rc+.02)*math.cos(t),cy+(Rc+.02)*math.sin(t),z1+(h0+h1)/2*F),(.16,.30,(h1-h0)*F),CU,t)
  elif kind=='ball':hc,rb=data;sphere132(m,cx,cy,z1+hc*F,rb*F,CD)
  elif kind=='rod':h0,h1,rd=data;m.cylinder(cx,cy,z1+h0*F,rd*F,(h1-h0)*F,CD,8)
  elif kind=='fleur':fleur132(m,cx,cy,z1+data*F,t0,CD)
  elif kind=='vane':vane132(m,cx,cy,z1+data*F,t0+math.pi/2,CD)
  elif kind=='tip':
   rodtop=max(p[2][1] for p in T['parts'] if p[0]=='rod');lathe132(m,cx,cy,z1+rodtop*F,[(0,.07),(.06,.07),(data*F-rodtop*F,0)],CD,8,0,bottom=True)
  elif kind=='spikes':
   hs,hl=data
   for j in range(4):
    t=t0+j*math.pi/2;m.box((cx+hl*F/2*math.cos(t),cy+hl*F/2*math.sin(t),z1+hs*F),(hl*F,.05,.05),CD,t)
  elif kind=='crownring':
   h0,h1,hl=data;a=hl*F
   ring=[ring132(cx,cy,z1+h*F,aa,12,1,t0) for h,aa in ((h0,a),(h1,a),(h1,a-.05),(h0,a-.05))]
   skin132(m,ring+[ring[0]],CD,top=False)
   for j in range(12):
    t=t0+j*math.tau/12;x,y=cx+a*math.cos(t),cy+a*math.sin(t)
    lathe132(m,x,y,z1+h1*F,[(0,.035),(.14,0)],CD,4,t,bottom=True)
PROF132={}

def kure132(m,KRECT,kcx,kcy,ku,kv,hu,hv,ka,ZK):
 KD=B132D['kure'];F=F132;CU=K['Copper'];CD=K['CopperDark'];GO=K['Gold']
 EU,EV=hu+.62,hv+.62;hb=KD['bell'][-1][0];e0=KD['bell'][0][1]
 su=lambda h:EU/e0+(F-EU/e0)*min(1,h/hb);sv=lambda h:EV/e0+(F-EV/e0)*min(1,h/hb)
 def W(a,b):return (kcx+ku[0]*a+kv[0]*b,kcy+ku[1]*a+kv[1]*b)
 def sq(h,half,sub=4):
  au,av=half*su(h),half*sv(h);cs=[(-au,-av),(au,-av),(au,av),(-au,av)];pts=[]
  for i in range(4):
   (a0,b0),(a1,b1)=cs[i],cs[(i+1)%4]
   for s in range(sub):f=s/sub;pts.append((*W(a0+(a1-a0)*f,b0+(b1-b0)*f),ZK+h*F))
  return pts
 # Soffit from the wall top to the eaves, then the bell with ribs on the hips.
 inner=[];sub=4
 for i in range(4):
  p,q=KRECT[i],KRECT[(i+1)%4]
  for s in range(sub):f=s/sub;inner.append((p[0]+(q[0]-p[0])*f,p[1]+(q[1]-p[1])*f,ZK))
 skin132(m,[inner,sq(0,e0)],SIGN,top=False)
 rings=skin132(m,[sq(h,half) for h,half in KD['bell']],CU)
 for i in range(4):
  pts=[]
  for rg in rings[1:]:
   x,y,z=rg[i*sub];d=math.hypot(x-kcx,y-kcy);pts.append((kcx+(x-kcx)*(d+.03)/d,kcy+(y-kcy)*(d+.03)/d,z))
  town_path(m,pts,.04,CU)
 # Lucarnes, one on each face, standing on the eaves: base, volutes, columns, the opening, the
 # entablature, an arched head with a fan, a finial.
 DM=KD['dormer']
 for side in range(4):
  ax=[(1,0),(0,1),(-1,0),(0,-1)][side];th=math.atan2(ku[1]*ax[0]+kv[1]*ax[1],ku[0]*ax[0]+kv[0]*ax[1])
  dist=DM['front']*(su(2.0) if ax[0] else sv(2.0));fx,fy=W(ax[0]*dist,ax[1]*dist);P=frame132(fx,fy,th)
  ch,vh,op=DM['col_half']*F,DM['volute_half']*F,DM['opening']*F/2;zb0,zb1=ZK+DM['base'][0]*F,ZK+DM['base'][1]*F
  zc1=ZK+DM['col_top']*F;ze0,ze1=ZK+DM['entab'][0]*F,ZK+DM['entab'][1]*F;ar=DM['arch_r']*F;back=-2.2
  fbox132(m,P,th,-ch-.10,ch+.10,back,.22,zb0,zb1,CU)                               # base
  fbox132(m,P,th,-ch,ch,back,0,zb1,ze0,CU)                                          # body
  fbox132(m,P,th,-op,op,0,.02,ZK+DM['open_bottom']*F,zc1-.25,SIGN)                  # the opening
  kk_=10;fanprism132(m,P,[(op*math.cos(i*math.pi/kk_),zc1-.25+op*math.sin(i*math.pi/kk_)) for i in range(kk_+1)],0,.02,SIGN)
  for s in (-1,1):
   for uu in (s*(ch-.12),s*(ch-.40)):
    town_rod(m,P(uu,.14,zb1),P(uu,.14,ze0),.085,CD,8)
    fbox132(m,P,th,uu-.13,uu+.13,0,.28,zb1,zb1+.10,CD);fbox132(m,P,th,uu-.13,uu+.13,0,.28,ze0-.10,ze0,CD)
   q=[(s*ch,zb1),(s*vh,zb1)]+[(s*(ch+(vh-ch)*math.cos(i*math.pi/16)),zb1+(vh-ch)*math.sin(i*math.pi/16)) for i in range(1,8)]+[(s*ch,zb1+(vh-ch))]
   fanprism132(m,P,q,-.4,.10,CU)                                                    # volute
  fbox132(m,P,th,-ch-.12,ch+.12,back,.32,ze0,ze1,CD)                                # entablature
  kk_=14;fanprism132(m,P,[(ar*math.cos(i*math.pi/kk_),ze1+ar*math.sin(i*math.pi/kk_)) for i in range(kk_+1)],back,.20,CU)   # arched head
  fanprism132(m,P,[(.72*ar*math.cos(i*math.pi/kk_),ze1+.05+.72*ar*math.sin(i*math.pi/kk_)) for i in range(kk_+1)],.20,.24,CD) # fan
  for i in range(1,7):
   a_=i*math.pi/7;town_rod(m,P(.12*ar*math.cos(a_),.25,ze1+.05+.12*ar*math.sin(a_)),P(.70*ar*math.cos(a_),.25,ze1+.05+.70*ar*math.sin(a_)),.03,CU,6)
  zf0=ze1+ar;xf,yf,_=P(0,0,0);lathe132(m,xf,yf,zf0,[(0,.12),(.12,.12),(.22,.16),(.40,.16),(.50,.05),(ZK+DM['finial']*F-zf0,0)],CD,8,0,bottom=True)
 # The corner aedicules: pedestal, column, entablature joined to the bell, box, ball and spike.
 AE=KD['aedicule'];ins=AE['inset']*F
 for a_,b_ in ((-1,-1),(1,-1),(1,1),(-1,1)):
  x,y=W(a_*(hu-ins),b_*(hv-ins));dg=math.atan2(y-kcy,x-kcx)
  h0,h1,w=AE['pedestal'];m.box((x,y,ZK+(h0+h1)/2*F),(w*F,w*F,(h1-h0)*F),CU,ka)
  h0,h1,cr,cc=AE['column'];m.cylinder(x,y,ZK+h0*F,cr*F,(h1-h0)*F,CD,12)
  m.box((x,y,ZK+h0*F+.05),(2*cc*F,2*cc*F,.10),CU,ka);m.box((x,y,ZK+h1*F-.05),(2*cc*F,2*cc*F,.10),CU,ka)
  h0,h1,w=AE['entab'];m.box((x,y,ZK+(h0+h1)/2*F),(w*F,w*F,(h1-h0)*F),CU,ka)
  # the entablature runs back into the bell along the diagonal
  zc_=ZK+(h0+h1)/2*F;hm=(h0+h1)/2
  half=next(hh for h,hh in reversed(KD['bell']) if h<=hm);inner_=math.hypot(half*su(hm),half*sv(hm))-.4;dd=math.hypot(x-kcx,y-kcy)
  L_=max(.1,dd-inner_);m.box((x-math.cos(dg)*L_/2,y-math.sin(dg)*L_/2,zc_),(L_,w*F*.7,(h1-h0)*F*.8),CU,dg)
  h0,h1,w=AE['box'];m.box((x,y,ZK+(h0+h1)/2*F),(w*F,w*F,(h1-h0)*F),CU,ka)
  h0,h1,rb=AE['finial'];sphere132(m,x,y,ZK+(h0+1.2)*F,rb*F,CD,12)
  lathe132(m,x,y,ZK+h0*F,[(0,.10),(.12,.10),(.12,.05)],CD,8,0,bottom=True)
  lathe132(m,x,y,ZK+(h0+1.6)*F,[(0,.13),((h1-h0-1.6)*F,0)],CD,8,0,bottom=True)
 # Plinth, open lantern, entablature, dome, neck, bulb.
 rot8=ka-math.pi/8
 lathe132(m,kcx,kcy,ZK,[(h*F,a*F) for h,a in KD['plinth']],CU,8,rot8)
 LT=KD['lantern'];A=LT['apothem']*F;zs=ZK+LT['h0']*F;zl1=ZK+LT['h1']*F;sill=LT['sill']*F
 lathe132(m,kcx,kcy,zs,[(0,A+.08),(sill,A+.08)],CU,8,rot8,bottom=True)
 hwf=A*math.tan(math.pi/8);ow=LT['opening']*F/2;zi=ZK+LT['impost']*F
 for j in range(8):
  th=ka+j*math.pi/4;P=frame132(kcx+A*math.cos(th),kcy+A*math.sin(th),th)
  for s in (-1,1):fbox132(m,P,th,min(s*hwf,s*ow),max(s*hwf,s*ow),-.30,0,zs+sill,zi,CU)
  archpanel132(m,P,hwf,zi,zl1,ow,-.30,0,CU)
  for s in (-1,1):fbox132(m,P,th,min(s*ow,s*(ow+.10)),max(s*ow,s*(ow+.10)),-.02,.06,zi-.12,zi,CD)   # imposts
  # paired columns at the corners, one each side of the corner on this face
  for s in (-1,1):
   uu=s*(hwf-.20);x0,y0,_=P(uu,.16,0)
   m.cylinder(x0,y0,zs+sill+.10,LT['col_r']*F,zl1-zs-sill-.30,CD,10)
   m.box((x0,y0,zs+sill+.05),(2*LT['col_cap']*F,2*LT['col_cap']*F,.10),CU,th+math.pi/2);m.box((x0,y0,zl1-.10),(2*LT['col_cap']*F,2*LT['col_cap']*F,.20),CU,th+math.pi/2)
 up=lathe132(m,kcx,kcy,ZK,[(h*F,a*F) for h,a in KD['upper']],CU,8,rot8,bottom=True)
 for j in range(8):
  pts=[]
  for rg in up:
   x,y,z=rg[j];d=math.hypot(x-kcx,y-kcy)
   if ZK+44.5*F-1e-6<=z<=ZK+54.3*F+1e-6:pts.append((kcx+(x-kcx)*(d+.03)/d,kcy+(y-kcy)*(d+.03)/d,z))
  if len(pts)>1:town_path(m,pts,.035,CU)
 # Ball, band, neck, rod, plate, candelabra and crown.
 hc,rb=KD['ball'];sphere132(m,kcx,kcy,ZK+hc*F,rb*F,CD,16)
 h0,h1,ab=KD['band'];lathe132(m,kcx,kcy,ZK,[(h0*F,ab*F),(h1*F,ab*F)],CU,16,0,bottom=True)
 lathe132(m,kcx,kcy,ZK,[(h*F,a*F) for h,a in KD['neck']],CD,12,0,bottom=True)
 h0,h1,rd=KD['rod'];m.cylinder(kcx,kcy,ZK+h0*F,rd*F,(h1-h0)*F,CD,8)
 hp,ap=KD['plate'];lathe132(m,kcx,kcy,ZK,[(hp*F,ap*F),(hp*F+.10,ap*F)],CD,12,0,bottom=True)
 ha,aa=KD['arms']
 for s in (-1,1):
  x1,y1=W(s*aa*F,0);x_,y_=W(s*aa*F*.45,0)
  town_path(m,[(kcx,kcy,ZK+(ha-2.2)*F),(x_,y_,ZK+(ha-1.9)*F),(x1,y1,ZK+(ha-.6)*F),(x1,y1,ZK+ha*F)],.03,CD)
 for s in (-1,0,1):
  x1,y1=W(s*aa*F,0);lathe132(m,x1,y1,ZK+ha*F,[(0,.06),(.05,.12),(.18,.16),(.18,.12)],GO,8,0,bottom=True,top=True)
 c0,c1,cr=KD['crown'];zc=ZK+c0*F
 lathe132(m,kcx,kcy,zc,[(0,cr*F*.8),(.10,cr*F),(.30,cr*F),(.36,cr*F*.85)],GO,14,0,bottom=True)
 for k in range(5):
  t=k*math.tau/5;town_path(m,[(kcx+cr*F*.85*math.cos(t),kcy+cr*F*.85*math.sin(t),zc+.34),(kcx+cr*F*.7*math.cos(t),kcy+cr*F*.7*math.sin(t),zc+.62),(kcx+.05*math.cos(t),kcy+.05*math.sin(t),zc+.78)],.035,GO)
 sphere132(m,kcx,kcy,zc+.84,.09,GO,10)
 town_rod(m,(kcx,kcy,zc+.90),(kcx,kcy,ZK+c1*F),.025,GO,6)
 x_,y_=W(.11,0);x2,y2=W(-.11,0);town_rod(m,(x2,y2,ZK+c1*F-.12),(x_,y_,ZK+c1*F-.12),.025,GO,6)
'''

def edit_towers132(k):
 # The cap loop of the round towers and Kuretornet's roof are replaced; the walls stay.
 i0=k.index(" for part in spec['cap']:\n");e=" m.box((cx+.28,cy,z+.9*Ht),(.56,.02,.3),K['Gold'],t0)\n";i1=k.index(e)+len(e)
 assert k.count(" for part in spec['cap']:\n")==1 and k.count(e)==1
 k=k[:i0]+" caps132(m,key,cx,cy,r,z1,t0)\n"+k[i1:]
 s0="# Square bell roof in copper:";s1="c27_finish(m)"
 assert k.count(s0)==1 and k.count(s1)==1
 return k[:k.index(s0)]+"kure132(m,KRECT,kcx,kcy,ku,kv,hu,hv,ka,ZK)\n"+k[k.index(s1):]

# ================================================================= pass 126's composition of pass 124
SRC126_132=(R/'scripts/build_block126.py').read_text()
NSP132=dict(globals());NSP132['B126D']=json.loads((R/'source/block126.json').read_text())
exec(compile(SRC126_132[SRC126_132.index('def rep126(src,old,new):'):SRC126_132.index('NS126=dict(globals())')],'build_block126.py:composition','exec'),NSP132)
_s=NSP132['_s']
# Marking is done below, after pass 125's cut.
_s=rep132(_s,"def b124_mark(obj,corrects=None,osm=''):return mark126(obj,'27,124' if corrects==27 and obj.name!='SM_Castle27_Ground' else ('27' if corrects==27 else '124'),osm)\n",
 "def b124_mark(obj,corrects=None,osm=''):return obj\n")
# Only the towers section runs: not pass 27's ground (pass 126), not the castle (pass 127), nothing after.
_s=rep132(_s,"exec(compile(sec124('# ================================================================= ground: island, ravelin, islets','# ================================================================= fortification walls'),'build_castle27.py:ground (pass 126 courtyard level)','exec'),NS124)",
 "pass   # pass 132: the ground is not re-created")
_s=rep132(_s,"exec(compile(_c,'build_castle27.py:castle (pass 124+126 edits)','exec'),NS124)",
 "exec(compile(_c[_c.index('CO=[tuple(p)'):_c.index('RANGES={')],'build_castle27.py:castle outline only (pass 132)','exec'),NS124)   # pass 132: the castle is not re-created")
_s=rep132(_s,"_k=edit_towers126(_k)\nexec(compile(_k,'build_castle27.py:towers (pass 124+126 edits)','exec'),NS124)",
 "_k=edit_towers132(edit_towers126(_k))\nexec(compile(EXTRA132,'build_block132.py:caps','exec'),NS124)\nexec(compile(_k,'build_castle27.py:towers (pass 124+126+132 edits)','exec'),NS124)")
_end="print('BLOCK124_PASS27_REBUILT',NS124['castle27_names'])\n";assert _s.count(_end)==1;_s=_s[:_s.index(_end)+len(_end)]
exec(compile(_s,'build_block126.py composition (pass 132 edits)','exec'),NSP132)
assert NSP132['NS124']['castle27_names']==['SM_Kalmar_Slott_Towers'],NSP132['NS124']['castle27_names']
print('BLOCK132_BULGED',{k_:NSP132['NS124']['BULGED132'].count(k_) for k_ in 'NSWE'})
# Pass 125's door passage into Kungsmaket crosses the re-created tower skin again.
cut_tower125();mark132(bpy.data.objects['SM_Kalmar_Slott_Towers'])

# ================================================================= cameras
def sv_camera132(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
_ZC132=json.loads((R/'source/block126.json').read_text())['zc']
block132_cameras=[
 # 715: the 2017 courtyard photograph (Commons, PD), pass 127's resection; the south tower's cap.
 sv_camera132('715_Block132_Cal_SouthCap2017',-861.1,-292.66,_ZC132+1.6,174.9,0,68.21),
 # 716: the 2022 well photograph (-wuppertaler), pass 129's resection; the east tower's cap.
 sv_camera132('716_Block132_Cal_EastCap2022',-878.55,-309.10,_ZC132+1.6,81.5,12.4,67.24),
 # 717: from the east-north-east over the water, as the 2019 drone view (placed by eye).
 sv_camera132('717_Block132_Drone2019',-550.0,-380.0,70.0,255.0,-7.0,14.0),
 # 718: Kuretornet's cap from the outer bailey.
 sv_camera132('718_Block132_Kuretornet',-925.0,-245.0,15.0,103.0,26.0,50.0),
 ('719_Block132_Aerial_Caps',(-780.0,-400.0,95.0),(-871.0,-303.0,30.0),30),
]
print('BLOCK132_GEOMETRY',len(block132_names))
