"""Photo-informed exterior pass 14. Dimensions without survey evidence are estimates.
Preserves all other scene assets. Sources and limitations: references/landmarks14-notes.md.
"""
import ast
L14=json.loads((R/'source/landmarks14.json').read_text());landmark_names=[]
BROWN=town_mats['PaintBrown'];METAL=town_mats['MetalGrey'];GLAZE=town_mats['Glass'];SC={k:'M_Sodra_'+k for k in ['Cream','Sand','RedWood','OchreWood','DarkTile']}
for file in ['build_town_details.py','town_detail_helpers.py','build_larmtorget_facades.py','build_sodra_facades.py']:
 tree=ast.parse((R/'scripts'/file).read_text());tree.body=[n for n in tree.body if isinstance(n,ast.FunctionDef)];exec(compile(tree,file,'exec'))
LM={}
for k,c in [('Ashlar',(.38,.36,.29)),('BrickRed',(.38,.16,.09)),('BrickBuff',(.54,.45,.28)),('Rubble',(.3,.3,.25)),('Cream',(.70,.61,.38)),('OliveWood',(.15,.18,.06)),('SashOchre',(.37,.22,.06)),('CopperRoof',(.06,.13,.10)),('Turf',(.08,.11,.035))]:
 name='M_Landmark_'+k
 if name not in materials:mat(name,c,.62 if k=='CopperRoof' else .8,.35 if k=='CopperRoof' else 0,'Landmark'+k)
 LM[k]=name
BR,BF,RS,CR,OW,SO,CU,GR=[LM[k] for k in ['BrickRed','BrickBuff','Rubble','Cream','OliveWood','SashOchre','CopperRoof','Turf']]
AS=LM['Ashlar']
LM_BRIDGE='M_Polish_BridgeWood' if 'M_Polish_BridgeWood' in materials else WOOD
def l14_new(name,category='Kvarnholmen/Landmarks'):
 name='SM_Kvarnholmen_'+name
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 landmark_names.append(name);return Mesh(name,category)
def l14_edges(poly):
 p=list(poly)
 if sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(p,p[1:]+p[:1]))<0:p.reverse()
 return [sf_edge(a,b) for a,b in zip(p,p[1:]+p[:1])]
def l14_face(m,x,y,L,H,holes,ma,a=0,back=True):
 if back:facade_box(m,x,y,0,-.24,H/2,L,.43,H,ma,a)
 lm_wall(m,x,y,L,H,[(u,b,w,h+r,False) for u,b,w,h,r in holes],ma,a)
 for u,b,w,h,r in holes:
  if r<=0:continue
  for sign in [-1,1]:
   outline=[(u,b+h+r),(u+sign*w/2,b+h+r),(u+sign*w/2,b+h)]+[(u+sign*w/2*math.cos(t*math.pi/48),b+h+r*math.sin(t*math.pi/48)) for t in range(1,24)]
   vs=[lp(x,y,v,o,z,a) for o in [.005,.355] for v,z in outline];n=len(outline);m.faces(vs,[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],ma)
def l14_arcband(m,x,y,z,rx,rz,width,out,a,ma):
 # Continuous profiled arch ribbon; welded visual contour without overlapping cylindrical beads.
 n=24;vs=[]
 for depth,radius in [(out-.045,-width),(out+.025,-width),(out+.025,width),(out-.045,width)]:
  for i in range(n+1):
   t=i*math.pi/n;vs.append(lp(x,y,(rx+radius)*math.cos(t),depth,z+(rz+radius)*math.sin(t),a))
 fs=[]
 for j in range(4):
  for i in range(n):fs.append((j*(n+1)+i,j*(n+1)+i+1,((j+1)%4)*(n+1)+i+1,((j+1)%4)*(n+1)+i))
 fs.extend([(0,n+1,2*(n+1),3*(n+1)),(n,4*n+3,3*n+2,2*n+1)]);m.faces(vs,fs,ma)
def l14_win(m,x,y,u,b,w,h,r=0,a=0,frame=TW,trim=TI,rows=3,cols=2):
 xx,yy,_=lp(x,y,u,0,0,a)
 # Flat reveal and glass, recessed 23 cm behind the plaster/brick face.
 sf_modern(m,x,y,u,b,w,h,a,frame,trim,rows,cols)
 if r:
  # Remove the rectangular top architrave from the front: overwrite only its own added geometry.
  # sf_modern trim at spring is a transom, arched outer band provides the upper frame.
  vs=[lp(xx,yy,w/2*math.cos(t*math.pi/32),.125,b+h+r*math.sin(t*math.pi/32),a) for t in range(33)]
  m.faces(vs,[tuple(range(33))],GLAZE)
  for off,rr,ww in [(.19,0,.035),(.375,.085,.065)]:
   l14_arcband(m,xx,yy,b+h,w/2+rr,r+rr,ww,off,a,frame if off<.2 else trim)
  for k in range(1,cols):
   uu=-w/2+k*w/cols;hh=r*math.sqrt(max(0,1-(2*uu/w)**2));facade_box(m,xx,yy,uu,.19,b+h+hh/2,.035,.075,hh,frame,a)
def l14_gable(m,x,y,w,d,H,rise,ma,roof,a=0):
 # Single coherent roof shell, solid gables and verge boards; local +out is the front.
 pts=[lp(x,y,u,o,z,a) for u,o,z in [(-w/2-.20,.48,H),(w/2+.20,.48,H),(0,.48,H+rise),(-w/2-.20,-d-.20,H),(w/2+.20,-d-.20,H),(0,-d-.20,H+rise)]]
 for f in [(0,2,5,3),(2,1,4,5)]:m.faces([pts[i] for i in f],[(0,1,2,3)],roof)
 for o in [.36,-d]:
  if ma==SC['RedWood'] and o>0:
   zc=H+rise*(1-.46/(w/2))
   for poly in [[(-w/2,H),(-.46,H),(-.46,zc)],[(.46,H),(w/2,H),(.46,zc)],[(-.46,H),(.46,H),(.46,H+.22),(-.46,H+.22)],[(-.46,H+1.17),(.46,H+1.17),(.46,zc),(0,H+rise),(-.46,zc)]]:
    m.faces([lp(x,y,u,o,zz,a) for u,zz in poly],[tuple(range(len(poly)))],ma)
  else:m.faces([lp(x,y,-w/2,o,H,a),lp(x,y,w/2,o,H,a),lp(x,y,0,o,H+rise,a)],[(0,1,2)],ma)
  for sign in [-1,1]:sf_beam(m,lp(x,y,sign*(w/2+.17),o+.05,H,a),lp(x,y,0,o+.05,H+rise+.08,a),.17,.12,TW,a)
 town_rod(m,lp(x,y,0,.49,H+rise+.04,a),lp(x,y,0,-d-.2,H+rise+.04,a),.11,roof,12)
def l14_hip(m,cx,cy,w,d,z,rise,ma,a=0,hipin=None):
 # Oriented hipped roof; optional inset supports mansard lower slopes.
 i=min(w/2,d/2)*.85 if hipin is None else hipin
 local=[(-w/2,-d/2,z),(w/2,-d/2,z),(w/2,d/2,z),(-w/2,d/2,z),(-w/2+i,-d/2+i,z+rise),(w/2-i,-d/2+i,z+rise),(w/2-i,d/2-i,z+rise),(-w/2+i,d/2-i,z+rise)]
 pts=[(cx+u*math.cos(a)-v*math.sin(a),cy+u*math.sin(a)+v*math.cos(a),zz) for u,v,zz in local]
 m.faces(pts,[(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)],ma)
 # Physically modelled standing seams run up the metal slopes.
 if ma==CU:
  for side in [-1,1]:
   for k in range(max(1,int(w/.7))):
    u=-w/2+(k+.5)*w/max(1,int(w/.7));t=min(1,(w/2-abs(u))/max(i,.01));p=(u,side*d/2,z+.02);q=(u,side*(d/2-i*t),z+rise*t+.02)
    town_rod(m,(cx+p[0]*math.cos(a)-p[1]*math.sin(a),cy+p[0]*math.sin(a)+p[1]*math.cos(a),p[2]),(cx+q[0]*math.cos(a)-q[1]*math.sin(a),cy+q[0]*math.sin(a)+q[1]*math.cos(a),q[2]),.014,ma)
def l14_lantern(m,x,y,z,r=1,h=3):
 m.cylinder(x,y,z,r*1.25,.28,CU,8)
 m.cylinder(x,y,z+.28,r,h,CU,8)
 for j in range(8):
  aa=j*math.tau/8;fx,fy=x+math.sin(aa)*r*.94,y-math.cos(aa)*r*.94
  facade_box(m,fx,fy,0,.03,z+.5+h*.5,r*.65,.06,h*.75,GLAZE,aa)
  for u in [-r*.37,r*.37]:facade_box(m,fx,fy,u,.10,z+.5+h*.5,.08,.1,h*.9,CU,aa)
 m.lathe(x,y,z+h+.3,[(r*1.38,0),(r*.90,.32),(r*.45,.65),(.07,1.18)],CU,8)
 m.lathe(x,y,z+h+1.5,[(.08,0),(.16,.15),(.1,.34),(.035,.6),(.012,1.0)],METAL,16)
# Tripp-trapp-trull: green low timber, cream two-storey, red tall timber, gables to Fiskaregatan.
for bid,H,rise,ma,levels,bays in [('92204204',2.90,2.05,OW,1,1),('92204192',5.75,2.05,CR,2,2),('92204165',6.45,2.40,SC['RedWood'],2,2)]:
 b=L14['buildings'][bid];x0,y0,x1,y1=b['bounds'];front=min(l14_edges(b['polygon']),key=lambda e:abs(e[1]-y0));x,y,L,a=front;m=l14_new('House_'+bid)
 for ex,ey,LL,aa in l14_edges(b['polygon']):
  isfront=abs(ey-y)<.6;iswest=abs(ex-x0)<.5;holes=[]
  if isfront:
   us=[0] if bays==1 else [-L*.23,L*.23]
   for k in range(levels):
    for ui,u in enumerate(us):
     if bid=='92204192' and k==0 and ui==0:holes.append((u,.13,1.1,2.23,0))
     else:holes.append((u,.72+k*(2.78 if levels==2 else 0),1.24 if bays==2 else 1.58,1.65 if levels==2 else 1.56,0))
  elif iswest and bid=='92204204':holes=[(u,.74,1.1,1.52,0) for u in [-LL*.29,0,LL*.29]]
  l14_face(m,ex,ey,LL,H,holes,ma,aa)
  facade_box(m,ex,ey,0,.33,.20,LL,.18,.4,RS,aa)
  if ma!=CR:sf_wood(m,ex,ey,LL,H,aa,ma,holes)
  for u,z,w,h,r in holes:
   if z==.13:
    town_door(m,*lp(ex,ey,u,.16,0,aa)[:2],z,w,h,aa,OW)
    for zz in [.07,.14]:facade_box(m,ex,ey,u,.68,zz,1.35,.7,.14,RS,aa)
   else:l14_win(m,ex,ey,u,z,w,h,0,aa,SO,TW,3,2)
  for u in [-LL/2+.065,LL/2-.065]:facade_box(m,ex,ey,u,.38,H/2,.15,.1,H,TW if ma!=OW else ma,aa)
  if isfront:
   sf_pipe(m,ex,ey,LL/2-.08,H,aa,TW)
   if ma==CR:facade_box(m,ex,ey,0,.39,3.03,LL,.13,.18,TW,aa)
 depth=y1-y0;l14_gable(m,x,y,L,depth,H,rise,ma,TT,a)
 if ma!=CR:
  for i in range(int(L/.16)+1):
   u=-L/2+i*L/int(L/.16);h=rise*max(0,1-abs(2*u/L))
   if h>.03:
    spans=[(H,H+h)]
    if ma==SC['RedWood'] and abs(u)<.48:spans=[(H,H+.22),(H+1.17,H+h)]
    for lo,hi in spans:
     if hi>lo:facade_box(m,x,y,u,.39,(lo+hi)/2,.025,.04,hi-lo,ma,a)
 if bid=='92204165':l14_win(m,x,y,0,H+.3,.69,.76,0,a,SO,TW,2,1)
 if ma==CR:
  for sign in [-1,1]:
   for k in range(1,9):
    u=sign*(L/2)*(k/10);z=H+rise*(1-abs(2*u/L))-.19;m.lathe(*lp(x,y,u,.41,z,a)[:2],z,[(.035,0),(.08,.05),(.045,.16)],TW,8)
 cx,cy=x,y+depth*.6;m.box((cx,cy,H+rise+.47),(.6,.65,1.14),TI);m.box((cx,cy,H+rise+1.04),(.78,.84,.14),RS)
 # Curved chimney rain hood, not a pointed spike.
 for sign in [-1,1]:town_path(m,[(cx+sign*(.29*(1-t)),cy,H+rise+1.13+.5*math.sin(t*math.pi/2)) for t in [k/12 for k in range(13)]],.07,RS)
 m.finish()
# Varmbadhuset: articulated plaster shell, triplet top lights, portal and copper turrets.
b=L14['buildings']['91846928'];m=l14_new('House_91846928');H=11.7
for x,y,L,a in l14_edges(b['polygon']):
 if L<8:
  l14_face(m,x,y,L,H,[],CR,a);continue
 west=x<396.1;south=y<-95;north=y>-64;N=5 if south else max(3,round(L/4.2));us=[-L/2+(k+.5)*L/N for k in range(N)];holes=[]
 for u in us:
  holes.extend([(u,.60,.85,1.1,.16),(u,3.30,1.05,1.35,.25)])
  if south:
   for off in [-.72,0,.72]:holes.append((u+off,8.95,.55,1.36,.25))
  else:holes.append((u,9.17,.83,1.08,0))
 if west:
  holes=[h for h in holes if not(abs(h[0]+L*.22)<2.1 and h[1]<5)];holes.append((-L*.22,.13,2.05,2.75,.65))
 l14_face(m,x,y,L,H,holes,CR,a)
 for u,z,w,h,r in holes:l14_win(m,x,y,u,z,w,h,r,a,CU,AS if z<2 else CR,3,2)
 for z in [2.45,5.07,8.40]:facade_box(m,x,y,0,.37,z,L,.14,.13,AS,a)
 facade_box(m,x,y,0,.37,.21,L,.20,.42,AS,a);lm_cornice(m,x,y,L,H,a,CR,True)
 if south:
  for i in range(N+1):
   u=-L/2+i*L/N;facade_box(m,x,y,u,.43,6.7,.35,.28,9.75,CR,a)
   for zz in [2.6,5.2]:facade_box(m,x,y,u,.51,zz,.48,.40,.32,AS,a)
 if west:
  u=-L*.22;px,py,_=lp(x,y,u,.35,0,a)
  for side in [-1,1]:facade_box(m,px,py,side*1.36,.26,1.87,.50,.65,3.75,AS,a)
  l14_arcband(m,px,py,2.88,1.32,.8,.22,.30,a,AS)
  town_band(m,px,py,4.0,3.8,a,AS,1.2)
  town_polyprofile(m,px,py,4.05,[(-1.9,0),(1.9,0),(1.5,.5),(.65,.7),(.65,1.8),(.35,2.1),(-.35,2.1),(-.65,1.8),(-.65,.7),(-1.5,.5)],a,AS,.38,False)
  lm_panel(m,px,py,0,5.17,.83,1.60,a,AS)
  # Low-relief draped figure, deliberately interpreted rather than claimed scanned sculpture.
  fx,fy,_=lp(px,py,0,.15,0,a);m.lathe(fx,fy,4.50,[(.20,0),(.13,.60),(.21,.92),(.13,1.03)],AS,12);m.lathe(fx,fy,5.56,[(.07,0),(.12,.10),(.07,.22)],AS,12)
  for sign in [-1,1]:town_path(m,[lp(px,py,sign*.17,.20,5.43,a),lp(px,py,sign*.31,.23,5.15,a),lp(px,py,sign*.14,.25,5.04,a)],.06,AS)
  # Projecting oriel near the centre, connected back to the wall.
  ox,oy,_=lp(x,y,L*.17,.2,0,a);facade_box(m,ox,oy,0,.53,4.3,2.1,1.1,2.40,CR,a)
  for uu in [-.48,.48]:l14_win(m,*lp(ox,oy,0,1.10,0,a)[:2],uu,3.48,.77,1.52,0,a,CU,CR,3,2)
  l14_hip(m,*lp(ox,oy,0,.62,0,a)[:2],2.5,1.4,5.55,.85,CU,a)
 for u in [-L/2+.16,L/2-.16]:sf_pipe(m,x,y,u,H,a,TW)
# Roof is split at the mapped L-shaped return.
l14_hip(m,405.3,-85.25,19.6,22.5,H,4.65,TT)
l14_hip(m,400.75,-68.65,10.4,12.6,H,3.0,TT)
for gy in [-92.2,-67.5]:
 gx=395.64;aa=-math.pi/2;w=5.4
 outline=[(-w/2,0),(w/2,0),(w/2,1.1),(2,1.4),(1.25,2.4),(.45,3.55),(0,3.85),(-.45,3.55),(-1.25,2.4),(-2,1.4),(-w/2,1.1)]
 town_polyprofile(m,gx,gy,10.9,outline,aa,CR,.43,False)
 l14_win(m,*lp(gx,gy,0,.45,0,aa)[:2],0,11.1,2.25,1.18,.85,aa,CU,CR,3,4)
 for sign in [-1,1]:town_path(m,[lp(gx,gy,sign*u,.11,10.9+z,aa) for u,z in [(2.7,1.1),(2,1.4),(1.25,2.4),(.45,3.55),(0,3.85)]],.13,AS)
for tx,ty in [(413,-93.6),(397.2,-93.8)]:
 m.box((tx,ty,11.45),(3.6,3.6,3.4),CR);l14_hip(m,tx,ty,4.2,4.2,13.2,2.1,CU,hipin=2.02)
 for aa in [0,math.pi/2,math.pi,3*math.pi/2]:
  fx,fy,_=lp(tx,ty,0,1.82,0,aa);l14_win(m,fx,fy,0,11.7,.82,.74,.41,aa,CU,CR,2,2)
l14_lantern(m,400.6,-69.1,14.25,.67,2.0);m.finish()
# Fire station: 1905 section occupies east half of the mapped combined footprint.
m=l14_new('House_91846968');poly=L14['buildings']['91846968']['polygon'];fa=math.atan2(7.013,-42.22);fx,fy=(-232.567-190.347)/2,(280.42+273.407)/2;FL=math.hypot(42.22,7.013)
# Modern western wing footprint separated at the old/new facade junction.
modern=[(-273.94,277.619),(-267.079,277.818),(-266.184,279.89),(-232.567,280.42),(-226.912,259.792),(-226.105,251.187),(-253.53,247.59),(-282.848,247.672),(-282.832,255.457),(-281.189,255.725),(-281.664,259.757)]
for x,y,L,a in l14_edges(modern):
 n=max(1,round(L/3.7));us=[-L/2+(i+.5)*L/n for i in range(n)];holes=[(u,z,1.65,1.90,0) for u in us for z in [.7,4.1,7.25]];l14_face(m,x,y,L,10.0,holes,CR,a)
 for u,z,w,h,r in holes:l14_win(m,x,y,u,z,w,h,0,a,METAL,TW,1,2)
 facade_box(m,x,y,0,.15,10.13,L,.55,.25,METAL,a)
 for u in us:
  if y>273:
   facade_box(m,x,y,u,.95,6.82,2.7,1.45,.18,TI,a);lm_rail(m,*lp(x,y,u,0,0,a)[:2],2.7,6.9,a,1.60)
# Modern wing roof, footprint triangulated by Blender (plan is concave but simple).
m.faces([(x,y,10.25) for x,y in modern],[tuple(range(len(modern)))],METAL)
# Old long front, seven tall arched former vehicle doors, eastern regular bay.
spacing=FL/9;us=[-FL/2+(i+.5)*spacing for i in range(9)];holes=[]
for i,u in enumerate(us):
 holes.append((u,.15 if i>=2 else .85,2.55 if i>=2 else 1.1,2.7 if i>=2 else 1.65,1.25 if i>=2 else 0))
 holes.append((u,5.30,1.25,2.1 if i<7 else 4.5,0))
holes=[h for h in holes if not(h[1]>5 and h[0]>FL/2-10.6)]+[(FL/2-5.3+du,5.30,1.25,4.5,0) for du in [-3.3,0,3.3]]
l14_face(m,fx,fy,FL,10.50,holes,CR,fa)
for u,z,w,h,r in holes:l14_win(m,fx,fy,u,z,w,h,r,fa,SC['RedWood'] if z<.2 else TW,CR,3 if z<5 else 6,3 if z<.2 else 2)
for i,u in enumerate(us):
 if i>=2:
  for off in [-.9,0,.9]:facade_box(m,fx,fy,u+off,.22,.61,.75,.10,.92,SC['RedWood'],fa)
for z in [4.65,10.45]:lm_cornice(m,fx,fy,FL,z,fa,CR)
# Horizontal rustication avoids openings and sits as fine recessed-shadow courses.
for k in range(1,25):
 zz=k*.42
 spans=[(-FL/2,FL/2)]
 for u,b,w,h,r in holes:
  if b-.03<zz<b+h+r+.03:spans=[(l,rr) for lo,hi in spans for l,rr in [(lo,min(hi,u-w/2-.1)),(max(lo,u+w/2+.1),hi)] if rr>l+.04]
 for lo,hi in spans:facade_box(m,fx,fy,(lo+hi)/2,.361,zz,hi-lo,.012,.016,TS,fa)
# Side/rear facade retains lower service rooms and stair tower.
for x,y,L,a in l14_edges([(-232.567,280.42),(-190.347,273.407),(-190.38,259.505),(-202.368,261.499),(-204.359,255.417),(-226.912,259.792)]):
 if y>270:continue
 n=max(1,round(L/4));hs=[(-L/2+(i+.5)*L/n,z,1.2,1.85,0) for i in range(n) for z in [1.0,5.2]];l14_face(m,x,y,L,10.5,hs,CR,a)
 for u,z,w,h,r in hs:l14_win(m,x,y,u,z,w,h,r,a,TW,CR,4,2)
cx,cy,_=lp(fx,fy,0,-7,0,fa);l14_hip(m,cx,cy,FL+1,15.2,10.60,3.35,CU,fa,2.25)
l14_hip(m,cx,cy,FL-3.5,10.7,14.0,.55,CU,fa,1)
for u in us[:7]:
 dx,dy,_=lp(fx,fy,u,.83,0,fa);lm_dormer(m,dx,dy,11.0,1.65,fa,CU)
# Raised western gymnasium bay and its decorated tall-window front.
u=FL/2-5.3;wx,wy,_=lp(fx,fy,u,-.12,0,fa)
for du in [-4.7,4.7]:facade_box(m,wx,wy,du,.48,7.6,.34,.35,5.5,CR,fa)
for du in [-3.3,0,3.3]:lm_panel(m,wx,wy,du,5.02,2.6,.52,fa,RS)
lm_cornice(m,wx,wy,10.6,10.7,fa,CR);cx2,cy2,_=lp(wx,wy,0,-6.4,0,fa);l14_hip(m,cx2,cy2,10.6,13.6,10.9,4.1,CU,fa,2.2)
town_polyprofile(m,*lp(wx,wy,0,.5,0,fa)[:2],10.85,[(-2.1,0),(2.1,0),(1.65,1.4),(.9,1.8),(-.9,1.8),(-1.65,1.4)],fa,CR,.3,False);lm_panel(m,wx,wy,0,11.72,2.65,.9,fa,RS)
# Slang tower on the courtyard side, square masonry base with octagonal lantern.
tx,ty,_=lp(fx,fy,FL/2-7,-14.7,0,fa);m.box((tx,ty,10.2),(4.5,4.5,20.4),CR,fa)
for aa in [fa+j*math.pi/2 for j in range(4)]:
 xx,yy,_=lp(tx,ty,0,2.27,0,aa)
 for z in [4,10.7,16.5]:l14_win(m,*lp(xx,yy,0,.35,0,aa)[:2],0,z,.78,2.40,0,aa,TW,CR,6,2)
 lm_cornice(m,xx,yy,4.8,20.4,aa,CR)
l14_lantern(m,tx,ty,20.62,1.20,3.2);m.finish()
# Ångkvarnen complex. Recessed buff fields between red brick pilasters and cornices.
def l14_millface(m,x,y,L,H,a,N,floors,base=True):
 spacing=L/N;us=[-L/2+(i+.5)*spacing for i in range(N)];step=(H-8)/max(1,floors-2);hs=[]
 for u in us:
  hs.extend([(u,.55,1.60,2.0,.68),(u,4.45,1.55,1.63,.47)])
  for k in range(floors-2):hs.append((u,8.4+k*step,1.48,max(1.4,step*.55),.30))
 l14_face(m,x,y,L,H,hs,BF,a)
 for u,z,w,h,r in hs:l14_win(m,x,y,u,z,w,h,r,a,CU,BR if z>7 else CR,3,3)
 # Lower two-storey plaster is built around the openings, not pasted across windows.
 l14_face(m,*lp(x,y,0,.01,0,a)[:2],L,7.95,[q for q in hs if q[1]<7],CR,a,False)
 for k in range(N+1):
  u=-L/2+k*spacing;facade_box(m,x,y,u,.51,(H+8)/2,.54,.36,H-8,BR,a)
 for z in [7.85,H-4.2,H]:lm_cornice(m,x,y,L,z,a,BR,True)
 for k in range(max(1,round(L/.62))):
  u=-L/2+(k+.5)*L/max(1,round(L/.62));facade_box(m,x,y,u,.31,H+.37,.33,.48,.66,BR,a)
 facade_box(m,x,y,0,.3,.24,L,.18,.48,RS,a)
 for u in [-L/2+.35,L/2-.35]:sf_pipe(m,x,y,u,H,a,CU)
for bid,H,floors in [('91285823',23.5,6),('91285828',34.0,8),('91285833',28.5,7)]:
 m=l14_new('House_'+bid);poly=L14['buildings'][bid]['polygon']
 # Kalmarsalen projects south as a glazed raised foyer; main tall block starts at y=-144.2.
 if bid=='91285828':poly=[(233.32,-144.2),(258.78,-144.2),(258.83,-98.79),(233.38,-98.76)]
 for x,y,L,a in l14_edges(poly):
  if L<3:continue
  N=max(2,round(L/4.3));l14_millface(m,x,y,L,H,a,N,floors)
 # Flat/low roof behind parapets; no generic red pitched cap.
 m.faces([(x,y,H-.18) for x,y in poly],[tuple(range(len(poly)))],METAL)
 if bid=='91285828':
  for x in [233.6,258.4]:
   for y in [-143.9,-99.1]:
    m.box((x,y,H+.65),(.9,.9,1.65),BR);m.box((x,y,H+1.5),(1.15,1.15,.18),TI);m.lathe(x,y,H+1.65,[(.12,0),(.25,.22),(.13,.53),(.025,.95)],CU,16)
  # Modern foyer on five structural columns, physically connected to the main entrance.
  m.box((246.04,-151.9,4.23),(25.5,15.4,.36),RS);m.box((246.04,-151.9,10.6),(25.7,15.6,.35),CU)
  for x,y,L,a in [(246.04,-159.82,25.5,0),(258.82,-152.0,15.5,math.pi/2),(233.28,-152.0,15.5,-math.pi/2)]:
   for k in range(max(2,round(L/4.8))+1):
    u=-L/2+k*L/max(2,round(L/4.8));facade_box(m,x,y,u,.04,5.3,.28,.44,10.6,BR,a)
   facade_box(m,x,y,0,-.05,7.0,L,.12,5.2,GLAZE,a)
   for z in [4.6,5.0,9.5,10.15]:facade_box(m,x,y,0,.15,z,L,.15,.1,TW,a)
   for k in range(max(1,round(L/1.1))):facade_box(m,x,y,-L/2+(k+.5)*L/max(1,round(L/1.1)),.14,7.3,.055,.14,5.1,TW,a)
  town_text(m,246,-160.12,3.5,0,'KALMARSALEN',7.3,TI)
 elif bid=='91285833':
  town_text(m,277,-144.7,5.65,0,'KALMAR LÄNS MUSEUM',14,BR)
  for dx in [-8,0,8]:
   town_lantern(m,277+dx,-144.8,3.2,0)
  # Centre entrance canopy and stone landing.
  m.box((276.9,-145.6,.14),(4.4,2.0,.28),RS);m.box((276.9,-145.5,3.65),(4.7,2.2,.16),CU)
 elif bid=='91285823':
  # The tall industrial tower sits in the western wing, maintaining the harbour silhouette.
  tx,ty=192.8,-91.0;m.box((tx,ty,28.8),(10.5,13.2,57.6),BR)
  for aa,L in [(0,10.5),(math.pi/2,13.2),(math.pi,10.5),(-math.pi/2,13.2)]:
   fx,fy,_=lp(tx,ty,0,6.6 if abs(math.cos(aa))>.5 else 5.25,0,aa)
   for u in [-L*.23,L*.23]:
    facade_box(m,fx,fy,u,.37,37.5,L*.29,.13,31.0,BF,aa)
    l14_win(m,*lp(fx,fy,0,.45,0,aa)[:2],u,49.0,1.4,3.6,.55,aa,CU,BR,4,2)
   for z in [54.6,57.7]:lm_cornice(m,fx,fy,L+.35,z,aa,BR,True)
   for k in range(round(L/1.1)):
    facade_box(m,fx,fy,-L/2+(k+.5)*L/round(L/1.1),.25,58.38,.55,.58,.9,TI,aa)
  for dx in [-5.1,5.1]:
   for dy in [-6.45,6.45]:
    m.box((tx+dx,ty+dy,58.55),(1.15,1.15,2.0),BR);m.lathe(tx+dx,ty+dy,59.55,[(.16,0),(.3,.28),(.12,.70),(.025,1.6)],CU,16)
  # Pale green lower western entrance wing below the industrial red brick gable.
  gx,gy=186.18,-133.8;aa=-math.pi/2;LL=20.5;hs=[(u,z,1.35,2.1,.65 if z<2 else 0) for u in [-7.8,-3.9,0,3.9,7.8] for z in [.7,5.15,8.50]]
  l14_face(m,gx,gy,LL,11.8,hs,TL,aa)
  for u,z,w,h,r in hs:l14_win(m,gx,gy,u,z,w,h,r,aa,TW,TL,3,2)
  for z in [4.65,8.10,11.75]:lm_cornice(m,gx,gy,LL,z,aa,TL,True)
  l14_gable(m,186.20,-134.5,19.4,47.1,23.5,5.1,BR,CU,-math.pi/2)
  # Filled brick pediment, centred on the southern wing instead of a floating outline.
  town_polyprofile(m,186.05,-134.5,23.3,[(-9.6,0),(9.6,0),(0,5.1)],aa,BR,.3,False)
  for uu,zz in [(-3.6,24.1),(0,26.0),(3.6,24.1)]:l14_win(m,185.69,-134.5,uu,zz,.95,1.0,.3,aa,CU,BF,2,2)
 m.finish()
# City wall meshes are grouped geographically; stone faces have batter and a capped crest.
def l14_wallsegment(m,p,q,H,W,ma=RS):
 x,y,L,a=sf_edge(p,q);inset=min(.48,H*.11)
 vs=[lp(x,y,u,o,z,a) for u,o,z in [(-L/2,-W/2,-.22),(L/2,-W/2,-.22),(L/2,W/2,-.22),(-L/2,W/2,-.22),(-L/2,-W/2+inset,H),(L/2,-W/2+inset,H),(L/2,W/2-inset,H),(-L/2,W/2-inset,H)]]
 m.faces(vs,[(0,3,2,1),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)],ma)
 # Broken stone coping courses, varied lengths, actually touch the wall.
 n=max(1,round(L/.95))
 for k in range(n):facade_box(m,x,y,-L/2+(k+.5)*L/n,0,H+.075,L/n-.025,max(.35,W-2*inset+.07),.15,RS,a)
for group in sorted(set(w['name'] for w in L14['walls'])):
 m=l14_new('Ringmur_'+group,'Kvarnholmen/Fortifications')
 for w in L14['walls']:
  if w['name']!=group:continue
  for p,q in zip(w['points'],w['points'][1:]):l14_wallsegment(m,p,q,w['height'],w['width'])
  for x,y in w['points'][1:-1]:m.cylinder(x,y,-.23,w['width']/2,w['height']+.25,RS,12,max(.18,w['width']/2-min(.48,w['height']*.11)))
 m.finish()
for group in sorted(set(w['name'] for w in L14['ramparts'])):
 m=l14_new('Vall_'+group,'Kvarnholmen/Fortifications')
 for g in L14['ramparts']:
  if g['name']!=group:continue
  z=g['height']
  for t in g['triangles']:m.faces([(x,y,z) for x,y in t],[(0,1,2)],GR)
  for poly in [g['outer']]+g['holes']:
   for p,q in zip(poly,poly[1:]+poly[:1]):m.faces([(*p,-.1),(*q,-.1),(*q,z),(*p,z)],[(0,1,2,3)],RS)
 m.finish()
# Portals are true open tunnels with radial vault surfaces; no invisible wall across the route.
for g in L14['gates']:
 m=l14_new('Port_'+g['name'],'Kvarnholmen/Fortifications');x,y,a=g['x'],g['y'],g['a'];L,H,D,W,S,AR=g['width'],g['height'],g['depth'],g['w'],g['spring'],g['rise']
 gate_ma=AS if g['name']=='Vasterport' else RS
 for sign in [-1,1]:facade_box(m,x,y,sign*(L+W)/4,0,H/2,(L-W)/2,D,H,gate_ma,a)
 for k in range(48):
  t0=k*math.pi/48;t1=(k+1)*math.pi/48;u0,u1=W/2*math.cos(t0),W/2*math.cos(t1);z0,z1=S+AR*math.sin(t0),S+AR*math.sin(t1)
  vs=[lp(x,y,u,o,z,a) for o in [-D/2,D/2] for u,z in [(u0,z0),(u1,z1),(u1,H),(u0,H)]]
  m.faces(vs,[(0,1,2,3),(7,6,5,4),(0,4,5,1),(3,2,6,7)],gate_ma)
 for side in [-1,1]:
  aa=a if side==1 else a+math.pi;fx,fy,_=lp(x,y,0,side*D/2,0,a)
  # Pale dressed arch stones outside rough rubble masonry.
  for k in range(24):
   t0=k*math.pi/24+.009;t1=(k+1)*math.pi/24-.009
   vs=[lp(fx,fy,r*math.cos(t),.11,S+rr*math.sin(t),aa) for r,rr,t in [(W/2,AR,t0),(W/2,AR,t1),(W/2+.36,AR+.36,t1),(W/2+.36,AR+.36,t0)]];m.faces(vs,[(0,1,2,3)],TI)
  for sign in [-1,1]:
   for k in range(round(S/.35)):facade_box(m,fx,fy,sign*(W/2+.18),.09,(k+.5)*S/round(S/.35),.36,.18,S/round(S/.35)-.018,TI,aa)
  if g['name']=='Vasterport':
   for zz in [S+AR+.22,6.35,H]:lm_cornice(m,fx,fy,L+.25,zz,aa,AS)
   lm_panel(m,fx,fy,0,5.65,2.85,.92,aa,AS)
   for u in [-1.5,1.5]:l14_win(m,*lp(fx,fy,0,.36,0,aa)[:2],u,6.85,1.28,1.1,.20,aa,IRON,AS,1,1)
   for u in [-L*.42,-2.9,2.9,L*.42]:
    for zz in [1.45,3.9,5.83]:facade_box(m,fx,fy,u,.38,zz,.16,.025,.17,IRON,aa)
   town_polyprofile(m,*lp(fx,fy,0,.1,0,aa)[:2],H+.12,[(-2.8,0),(2.8,0),(2.8,.48),(1.2,.48),(1.2,.77),(-1.2,.77),(-1.2,.48),(-2.8,.48)],aa,AS,.4,False)
   for u in [-2.55,2.55]:facade_box(m,fx,fy,u,.14,H+.62,1.3,.6,.25,AS,aa)
  elif g['name']=='Kavaljersporten':
   facade_box(m,fx,fy,0,0,H+.05,L,.40,.14,AS,aa)
   for sign in [-1,1]:
    u=sign*(W/2+.5)
    for zz,ww,hh in [(.18,1.05,.36),(2.65,.67,4.60),(4.90,1.12,.38)]:facade_box(m,fx,fy,u,.25,zz,ww,.60,hh,AS,aa)
    town_scroll(m,*lp(fx,fy,sign*(W/2+1.9),.25,0,aa)[:2],H+.18,aa,sign,1.0,.11,AS)
   facade_box(m,fx,fy,0,.20,H+.25,W+2.0,.70,1.0,AS,aa)
   lm_cornice(m,fx,fy,W+2.65,H+.80,aa,AS,True)
   for u in [-W*.42,-W*.23,W*.23,W*.42]:
    for du in [-.10,0,.10]:facade_box(m,fx,fy,u+du,.60,H+.24,.045,.10,.70,AS,aa)
   # Shallow heraldic shield and surrounding acanthus, supported on the frieze.
   town_polyprofile(m,*lp(fx,fy,0,.61,0,aa)[:2],H-.15,[(-.43,.85),(.43,.85),(.35,.15),(0,0),(-.35,.15)],aa,AS,.10,False)
   for sign in [-1,1]:town_scroll(m,*lp(fx,fy,sign*.56,.63,0,aa)[:2],H+.24,aa,sign,.42,.07,AS)
  else:facade_box(m,fx,fy,0,0,H+.05,L,.40,.14,AS,aa)
 if g['name']=='Vasterport':
  # Timber bridge rails and narrow planks, aligned with the mapped approach.
  for side in [-1,1]:
   for k in range(16):
    oo=-D/2-2*k;facade_box(m,x,y,side*1.74,oo,.62,.14,.14,1.2,LM_BRIDGE,a)
   for zz in [.40,.80,1.21]:sf_beam(m,lp(x,y,side*1.74,-D/2,zz,a),lp(x,y,side*1.74,-D/2-30,zz,a),.095,.105,LM_BRIDGE,a+math.pi/2)
  for k in range(94):facade_box(m,x,y,0,-D/2-(k+.5)*30/94,.095,3.35,30/94-.015,.07,LM_BRIDGE,a)
 # Turf roof and parapet are supported by the vault mass.
 facade_box(m,x,y,0,0,H+.03,L,D,.10,GR,a)
 m.finish()
# Consolidate triangles and remove float32 geometric slivers before tangent export.
for name in landmark_names:
 obj=bpy.data.objects[name];obj['detail_pass']=14;obj['massing_only']=False;obj['reference_notes']='references/landmarks14-notes.md';me=obj.data;bm=bmesh.new();bm.from_mesh(me);bmesh.ops.triangulate(bm,faces=list(bm.faces));bad=[f for f in bm.faces if f.calc_area()<1e-9]
 if bad:bmesh.ops.delete(bm,geom=bad,context='FACES')
 bm.to_mesh(me);bm.free();me.update()
landmark_cameras=[('59_TrippTrappTrull',(-296,136,2.3),(-275,150,3.4),29),('60_Varmbadhuset',(379,-91,3.2),(400,-79,7),25),('61_Brandstationen',(-220,315,3.0),(-213,267,10),30),('62_Angkvarnen',(285,-206,3.2),(242,-123,23),25),('63_Angkvarnen_Ostra',(325,-111,3.0),(281,-110,15),24),('64_Ringmur_Sodra',(-140,-240,2.1),(-88,-209,3.1),28),('65_Vasterport',(-380,109,2),(-343,89,5),30),('66_Regeringen',(460,-130,3),(425,-73,2.6),30),('67_Holmporten',(428,-4,2),(412,20,1),30),('68_Kavaljersporten',(51,-192,2),(51,-160,3),30)]
