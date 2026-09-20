"""Reference-based, traversable cathedral interior. Executed by build_blender.py.
Local u points towards the east altar; v points north. Dimensions are approximate
except the documented central clear height of 23 m. References in REFERENCES.md.
"""
IVORY=mat('M_Interior_Lime',(.80,.79,.73),.85)
PEW=mat('M_Pew_Grey',(.40,.43,.41),.72)
PANEL=mat('M_Pew_Inset',(.32,.35,.33),.75)
MARBLE=mat('M_Column_Dark',(.075,.065,.060),.28)
SILVER=mat('M_Organ_Pipes',(.52,.57,.59),.27,.85)
FLOOR1=mat('M_Interior_Stone_A',(.28,.27,.245),.68)
FLOOR2=mat('M_Interior_Stone_B',(.35,.32,.29),.66)
LIGHTGLASS=mat('M_Interior_Daylight',(.66,.76,.79),.35)
# Soft luminous glazing, complemented by actual lights in both Blender and UE.
materials[LIGHTGLASS].node_tree.nodes['Principled BSDF'].inputs['Emission Color'].default_value=(.65,.75,.80,1)
materials[LIGHTGLASS].node_tree.nodes['Principled BSDF'].inputs['Emission Strength'].default_value=.45
specs[LIGHTGLASS]['emission']=.45
BURGUNDY=mat('M_Altar_Cloth',(.23,.042,.033),.88)
def box(m,u,v,z,w,d,h,ma,ang=0):m.box((cx+u,cy+v,z),(w,d,h),ma,ang)
def rod(m,a,b,r,ma,n=8):
 a=Vector((cx+a[0],cy+a[1],a[2]));b=Vector((cx+b[0],cy+b[1],b[2]));direction=(b-a).normalized();seed=Vector((0,0,1)) if abs(direction.z)<.9 else Vector((1,0,0));s=direction.cross(seed).normalized()*r;t=direction.cross(s).normalized()*r
 vertices=[tuple(p+s*math.cos(i*math.tau/n)+t*math.sin(i*math.tau/n)) for p in [a,b] for i in range(n)]
 m.faces(vertices,[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],ma,True)
def curve(m,points,r,ma,n=12):
 # A single connected sweep avoids the old faceted joint beads.
 pts=[Vector(q) for q in points];verts=[]
 if len(pts)<2:return
 for j,q in enumerate(pts):
  tangent=(pts[min(j+1,len(pts)-1)]-pts[max(0,j-1)]).normalized()
  seed=Vector((0,0,1)) if abs(tangent.z)<.92 else Vector((1,0,0))
  e=tangent.cross(seed).normalized();f=tangent.cross(e).normalized()
  for k in range(n):
   xyz=q+r*(e*math.cos(k*math.tau/n)+f*math.sin(k*math.tau/n));verts.append((cx+xyz.x,cy+xyz.y,xyz.z))
 m.faces(verts,[(j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k) for j in range(len(pts)-1) for k in range(n)],ma,True)
def sphere(m,u,v,z,r,ma):m.lathe(cx+u,cy+v,z-r,[(r*math.sin(math.pi*i/12),r*(1-math.cos(math.pi*i/12))) for i in range(13)],ma,16)
def panel(m,u,v,z,w,h,faceaxis='x',ma=PEW):
 # framed recessed rect, plane normal along X by default
 dep=.085
 if faceaxis=='x':
  box(m,u,v,z,dep,w,h,ma)
  for vv in [-w/2+.055,w/2-.055]:box(m,u-.06,v+vv,z,.08,.075,h,IVORY)
  for zz in [-h/2+.05,h/2-.05]:box(m,u-.06,v,z+zz,.08,w,.075,IVORY)
 else:
  box(m,u,v,z,w,dep,h,ma)
  for uu in [-w/2+.055,w/2-.055]:box(m,u+uu,v-.06,z,.075,.08,h,IVORY)
  for zz in [-h/2+.05,h/2-.05]:box(m,u,v-.06,z+zz,w,.08,.075,IVORY)
# Separate architectural mesh: the outer shell is now hollow.
m=Mesh('SM_Domkyrka_Interior_Architecture','Cathedral interior')
# White plaster lining: intersect offset edges so corner joints stay closed.
def inset_corner(prev,cur,nxt,d):
 a=Vector(cur)-Vector(prev);b=Vector(nxt)-Vector(cur);a.normalize();b.normalize()
 aa=Vector(cur)+Vector((-a.y,a.x))*d;bb=Vector(cur)+Vector((-b.y,b.x))*d
 cross=a.x*b.y-a.y*b.x
 if abs(cross)<1e-7:return tuple(aa)
 delta=bb-aa;t=(delta.x*b.y-delta.y*b.x)/cross
 return tuple(aa+a*t)
inner=[inset_corner(p[(i-1)%len(p)],p[i],p[(i+1)%len(p)],.88) for i in range(len(p))]
for i,(ax,ay) in enumerate(inner):
 bx,by=inner[(i+1)%len(inner)];dx,dy=bx-ax,by-ay;ln=math.hypot(dx,dy);ang=math.atan2(dy,dx)
 if p[i][1]<26 and p[(i+1)%len(p)][1]<26:
  for l,r in [(ax,cx-1.45),(cx+1.45,bx)]:
   if r>l:m.box(((l+r)/2,(ay+by)/2,7.25),(r-l,.14,11.9),IVORY)
  m.box((cx,(ay+by)/2,9.8),(2.9,.14,6.8),IVORY)
 else:m.box(((ax+bx)/2,(ay+by)/2,7.25),(ln+.12,.14,11.9),IVORY,ang)
# Interior plaster on the upper cross shell, masking the exterior ochre.
for side in [-1,1]:
 box(m,0,side*16.97,18.0,21.8,.14,11.4,IVORY)
 box(m,side*24.67,0,18.0,.14,15.8,11.4,IVORY)
 for other in [-1,1]:
  box(m,side*10.27,other*12.85,18.0,.14,9.7,11.4,IVORY)
  box(m,side*18.0,other*7.27,18.0,14.0,.14,11.4,IVORY)
 for u in [0]:
  box(m,u,side*16.85,18.2,2.1,.10,5.7,LIGHTGLASS)
  for xx in [-.7,0,.7]:box(m,u+xx,side*16.77,18.2,.045,.09,5.7,FRAME)
  for zz in range(9):box(m,u,side*16.77,15.4+zz*.7,2.1,.09,.045,FRAME)
# Stone paving with real joints, confined to footprint with point-in-polygon.
def inside(x,y):
 hit=False
 for i,a in enumerate(p):
  b=p[(i+1)%len(p)]
  if (a[1]>y)!=(b[1]>y) and x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]:hit=not hit
 return hit
for ix in range(-32,33):
 for iy in range(-22,23):
  u=ix*.90;v=iy*.90
  if all(inside(cx+u+du,cy+v+dv) for du,dv in [(-.45,-.45),(-.45,.45),(.45,-.45),(.45,.45)]):box(m,u,v,1.315,.889,.889,.025,FLOOR1 if (ix*3+iy)%5 else FLOOR2)
# The cross barrel-vaults rise to 23 m above the floor. Their central intersection
# is a single continuous groin surface, so no intersecting opaque ceilings.
zspring=15.2;rise=9.1;hu=10.25;hv=7.65
for axis in ['nave','transept','crossing']:
 if axis=='nave':regions=[(-25,-hu,-hv,hv),(hu,25,-hv,hv)]
 elif axis=='transept':regions=[(-hu,hu,-17.0,-hv),(-hu,hu,hv,17.0)]
 else:regions=[(-hu,hu,-hv,hv)]
 for x0,x1,y0,y1 in regions:
  nx,ny=32,32;verts=[]
  for i in range(nx+1):
   u=x0+(x1-x0)*i/nx
   for j in range(ny+1):
    v=y0+(y1-y0)*j/ny
    zn=math.sqrt(max(0,1-(v/hv)**2));zt=math.sqrt(max(0,1-(u/hu)**2))
    zz=zspring+rise*(zn if axis=='nave' else zt if axis=='transept' else max(zn,zt))
    verts.append((cx+u,cy+v,zz))
  def vault_uv(q,r):
   return (r*math.asin(max(-1,min(1,q/r))) if abs(q)<=r else math.copysign(r*math.pi/2,q)+q-math.copysign(r,q))/4
  m.faces(verts,[(i*(ny+1)+j,(i+1)*(ny+1)+j,(i+1)*(ny+1)+j+1,i*(ny+1)+j+1) for i in range(nx) for j in range(ny)],IVORY,True,[(vault_uv(x-cx,hu),vault_uv(y-cy,hv)) for x,y,z in verts])
# Plaster infill above the cornices and shallow ceilings below corner towers.
for sign in [-1,1]:
 for x0,x1 in [(-25,-hu),(hu,25)]:box(m,(x0+x1)/2,sign*7.9,14.1,x1-x0,.5,2.4,IVORY)
 for y0,y1 in [(-17.0,-hv),(hv,17.0)]:box(m,sign*10.5,(y0+y1)/2,14.1,.5,y1-y0,2.4,IVORY)
 # Tower-room ceilings are clipped to the measured footprint; rectangular
 # ceilings previously protruded through the curved external side roofs.
 for other in [-1,1]:
  rect=(sign*17.4-7.25,sign*17.4+7.25,other*12.15-4.4,other*12.15+4.4)
  for tri in tessellate_polygon([[Vector((x-cx,y-cy,0)) for x,y in p]]):
   poly=[(p[q][0]-cx,p[q][1]-cy) if isinstance(q,int) else (q.x,q.y) for q in tri]
   for axis,bound,above in [(0,rect[0],True),(0,rect[1],False),(1,rect[2],True),(1,rect[3],False)]:
    clipped=[]
    for j,a in enumerate(poly):
     b=poly[(j+1)%len(poly)];ina=(a[axis]>=bound) if above else (a[axis]<=bound);inb=(b[axis]>=bound) if above else (b[axis]<=bound)
     if ina:clipped.append(a)
     if ina!=inb:
      t=(bound-a[axis])/(b[axis]-a[axis]);clipped.append((a[0]+t*(b[0]-a[0]),a[1]+t*(b[1]-a[1])))
    poly=clipped
    if not poly:break
   if len(poly)>=3:m.faces([(cx+x,cy+y,12.57) for x,y in poly],[tuple(range(len(poly)))],IVORY)
# Broad pilasters, cornices with dentils, and Ionic scrolls.
for u in [-23,-10.6,10.6,23]:
 for v in [-7.9,7.9]:
  box(m,u,v,7.8,1.45,1.05,13.0,IVORY);box(m,u,v,1.6,1.85,1.35,.6,IVORY)
  box(m,u,v,14.4,2.05,1.5,.45,IVORY);box(m,u,v,14.85,2.25,1.7,.3,IVORY)
  # Scrolls in an XZ plane facing the nave.
  for sx in [-1,1]:
   pts=[]
   for i in range(45):
    a=i*math.tau/22;r=.37*(1-i/55)
    pts.append((u+sx*.60+r*math.cos(a),v+(.61 if v<0 else -.61),14.03+r*math.sin(a)))
   curve(m,pts,.055,IVORY)
for v in [-7.8,7.8]:
 for a,b in [(-25,-10.25),(10.25,25)]:
  for z,d,h in [(14.5,.65,.45),(14.95,.9,.22),(15.18,1.0,.12)]:box(m,(a+b)/2,v,z,b-a,d,h,IVORY)
  for i in range(int((b-a)/.38)):box(m,a+i*.38,v,14.69,.17,.83,.22,IVORY)
for u in [-10.4,10.4]:
 for a,b in [(-17.0,-7.65),(7.65,17.0)]:
  for z,w,h in [(14.5,.65,.45),(14.95,.9,.22),(15.18,1,.12)]:box(m,u,(a+b)/2,z,w,b-a,h,IVORY)
# Transverse ribs repeat along the barrel vault.
for u in [-24,-10.25,10.25,24]:
 curve(m,[(u,hv*math.cos(t*math.pi/48),zspring+rise*math.sin(t*math.pi/48)-.10) for t in range(49)],.18,IVORY)
for v in [-16.7,16.7]:curve(m,[(hu*math.cos(t*math.pi/48),v,zspring+rise*math.sin(t*math.pi/48)-.1) for t in range(49)],.18,IVORY)
# Glazing seen from within: tall, narrow mullioned windows in the apses.
for sign in [-1,1]:
 box(m,sign*24.65,0,7.30,.14,15.3,11.9,IVORY)
 for vv in [-5.7,5.7]:
  uu=sign*24.45
  for z,h in [(5.5,6.7),(11.0,2.7)]:
   box(m,uu,vv,z,.12,2.45,h,IVORY);box(m,uu-sign*.11,vv,z,.10,2.1,h-.25,LIGHTGLASS)
   for q in [-.7,0,.7]:box(m,uu-sign*.19,vv+q,z,.07,.045,h-.25,FRAME)
   for i in range(int(h/.6)):box(m,uu-sign*.19,vv,z-h/2+.25+i*.6,.07,2.12,.045,FRAME)
m.finish()
# Reference-based painted joinery, shared with detail iteration builds.
exec(compile((R/'scripts/build_joinery.py').read_text(),str(R/'scripts/build_joinery.py'),'exec'))
# Galleries on the north/south cross arms and organ gallery at the west.
m=Mesh('SM_Domkyrka_Galleries_Organ','Cathedral interior')
def column(u,v,base,height,r=.36):
 m.lathe(cx+u,cy+v,base,[(r*1.5,0),(r*1.5,.22),(r*1.15,.33),(r,.55),(r*.86,height-.42),(r*1.36,height-.25),(r*1.5,height)],MARBLE,20)
 box(m,u,v,base+height-.15,r*3.2,r*3.2,.3,GOLD)
 box(m,u,v,base+.12,r*3.5,r*3.5,.24,PEW)
for sign in [-1,1]:
 box(m,0,sign*14.35,6.7,18.0,6.1,.48,IVORY)
 for u in [-7.5,-4.5,-1.5,1.5,4.5,7.5]:column(u,sign*11.45,1.33,5.15)
 # Balcony face with repeated balusters.
 for z,h in [(6.65,.30),(7.03,.16),(8.00,.14)]:box(m,0,sign*11.25,z,18.2,.3,h,IVORY)
 for i in range(48):
  u=-8.6+i*.365;box(m,u,sign*11.25,7.51,.105,.2,.89,PEW)
 for u in [-8,-4,0,4,8]:box(m,u,sign*11.24,7.5,.30,.3,1,IVORY)
 box(m,0,sign*11.12,8.10,18.2,.07,.06,GOLD)
# Elliptical projecting west gallery, visible in the west-facing photograph.
def gallery_front(v):return -19.5+2.8*math.sqrt(max(0,1-(v/7.55)**2))
outline=[(-25.5,-7.55)]+[(gallery_front(-7.55+15.1*i/96),-7.55+15.1*i/96) for i in range(97)]+[(-25.5,7.55)]
m.prism([(cx+u,cy+v) for u,v in outline],6.45,6.95,IVORY)
for v in [-6,-3,3,6]:column(gallery_front(v)-.38,v,1.33,5.12)
for z,h,depth,ma in [(6.54,.30,.36,IVORY),(6.78,.12,.43,IVORY),(6.96,.09,.32,GOLD),(7.15,.14,.27,IVORY),(8.05,.16,.32,IVORY),(8.17,.055,.33,GOLD)]:
 verts=[]
 for i in range(97):
  v=-7.55+15.1*i/96;u=gallery_front(v)
  verts.extend([(cx+u+off,cy+v,z+zz) for off,zz in [(-depth/2,-h/2),(depth/2,-h/2),(depth/2,h/2),(-depth/2,h/2)]])
 m.faces(verts,[(i*4+j,i*4+(j+1)%4,(i+1)*4+(j+1)%4,(i+1)*4+j) for i in range(96) for j in range(4)],ma,True)
for i in range(47):
 v=-7.25+i*14.5/46;u=gallery_front(v)
 m.lathe(cx+u,cy+v,7.16,[(.063,0),(.063,.08),(.040,.12),(.033,.25),(.066,.38),(.068,.47),(.040,.56),(.033,.68),(.062,.76)],IVORY,16)
for v in [-7.2,-4.8,-2.4,0,2.4,4.8,7.2]:
 box(m,gallery_front(v),v,7.60,.27,.28,.97,IVORY)
 box(m,gallery_front(v)+.15,v,7.60,.045,.19,.68,GOLD)
 box(m,gallery_front(v)+.18,v,7.60,.045,.12,.58,PEW)
for i in range(85):
 v=-7.4+i*14.8/84;box(m,gallery_front(v)+.11,v,6.60,.21,.075,.12,GOLD)
# Symmetric organ facade: three towers and two lower fields of metal pipes.
for v,w,top in [(-4.8,2.6,13.2),(-2.8,1.35,15.1),(0,3.4,16.8),(2.8,1.35,15.1),(4.8,2.6,13.2)]:
 box(m,-23.15,v,(7.8+top)/2,1.1,w,top-7.8,IVORY)
 box(m,-22.52,v,(8.4+top-.35)/2,.10,w-.3,top-8.75,MARBLE)
 for edge in [-1,1]:box(m,-22.38,v+edge*w*.46,(8.0+top)/2,.28,.17,top-8,GOLD)
 for z in [8.1,top]:box(m,-22.3,v,z,.36,w+.25,.22,GOLD)
 count=max(5,int(w/.18))
 for i in range(count):
  vv=v-w*.38+i*w*.76/(count-1);hh=top-8.65-.6*abs(i-(count-1)/2)/max(1,count/2)
  m.cylinder(cx-22.15,cy+vv,8.5,.065,hh,SILVER,10)
  box(m,-22.04,vv,8.85,.055,.10,.25,MARBLE)
# Radiating half-round pipe crown over the central organ bay.
for i in range(15):
 a=math.pi*i/14
 rod(m,(-22.1,0,16.9),(-22.1,2.0*math.cos(a),16.9+2.0*math.sin(a)),.07,SILVER)
curve(m,[(-22.18,2.15*math.cos(i*math.pi/36),16.9+2.15*math.sin(i*math.pi/36)) for i in range(37)],.17,IVORY)
sphere(m,-22.15,0,19.35,.25,GOLD)
m.finish()
# East altar and baroque reredos base; detailed carving and a credited
# photographic painting are added in build_church_details.py.
m=Mesh('SM_Domkyrka_Altar_Pulpit','Cathedral interior')
for i in range(3):box(m,19.5+i*.12,0,1.39+i*.12,13.3-i*.24,15.0-i*.28,.12,FLOOR2)
box(m,25.0,0,2.15,1.65,7.0,1.0,MARBLE)
box(m,24.8,0,2.8,1.8,7.4,.32,IVORY)
box(m,25.6,0,7.2,.48,5.25,8.5,MARBLE)
for v in [-2.7,2.7]:
 m.lathe(cx+24.6,cy+v,2.95,[(.63,0),(.63,.28),(.43,.4),(.40,7.55)],MARBLE,32)
 m.lathe(cx+24.6,cy+v,10.45,[(.41,0),(.43,.14),(.52,.54),(.62,.82),(.64,.92)],IVORY,32)
 box(m,24.6,v,11.46,1.4,1.4,.20,IVORY)
 box(m,24.6,v,11.88,1.31,1.31,.65,MARBLE)
 for z,w,h in [(11.62,1.47,.15),(12.25,1.50,.18),(12.45,1.7,.16)]:box(m,24.6,v,z,w,w,h,IVORY)
for v in [-2.15,2.15]:box(m,25.18,v,6.3,.20,.20,6.0,GOLD)
for z in [3.35]:box(m,25.18,0,z,.20,4.5,.20,GOLD)
curve(m,[(25.18,2.15*math.cos(t*math.pi/40),9.35+2.15*math.sin(t*math.pi/40)) for t in range(41)],.13,GOLD)
# All geometry so far in this mesh is the east reredos/platform.
m.v=[(x-2.5,y,z) for x,y,z in m.v]
# Modern freestanding gilded central altar, red stone slab.
m.lathe(cx+13.6,cy,1.7,[(1.15,0),(1.12,.18),(.85,.75),(1.15,1.15)],GOLD,32)
box(m,13.6,0,2.92,1.9,2.8,.18,RED)
box(m,13.6,0,3.6,.08,.08,1.2,GOLD);box(m,13.6,0,3.9,.09,.65,.08,GOLD)
# Carved dark and gold pulpit north of nave.
pulpit_start=len(m.v)
m.lathe(cx+8.1,cy+6.3,3.0,[(.2,0),(.3,.5),(1.0,1.1),(1.28,1.5),(1.28,3.0),(1.4,3.15)],GREEN,8)
for z in [4.5,5.9,6.15]:m.lathe(cx+8.1,cy+6.3,z,[(1.4,0),(1.4,.11)],GOLD,8)
for i in range(8):
 a=i*math.tau/8;box(m,8.1+1.27*math.cos(a),6.3+1.27*math.sin(a),5.2,.09,.09,1.2,GOLD)
m.lathe(cx+8.1,cy+6.3,9.4,[(1.65,0),(1.65,.18),(1.15,.35),(.65,1.15),(.3,1.65),(.08,2.1)],GREEN,8)
for z,r in [(9.4,1.7),(9.75,1.2),(10.55,.7)]:m.lathe(cx+8.1,cy+6.3,z,[(r,0),(r,.09)],GOLD,8)
# Bring the complete pulpit and canopy against the west face of the NE pier.
m.v[pulpit_start:]=[(x+.45,y+1.60,z) for x,y,z in m.v[pulpit_start:]]
m.finish()
# Three branched brass chandeliers.
m=Mesh('SM_Domkyrka_Chandeliers','Cathedral interior')
for u,scale in [(-13,.72),(0,1.0),(17,.8)]:
 z=10.2
 rod(m,(u,0,z+3.1*scale),(u,0,24),.025,IRON)
 m.lathe(cx+u,cy,z,[(.12,0),(.50*scale,.4),(.56*scale,.8),(.17,1.2),(.28,1.6),(.12,2.5),(.22,3.0)],GOLD,20)
 for tier in range(3):
  radius=(1.8-tier*.32)*scale;zz=z+.7+tier*.8
  for i in range(12):
   a=i*math.tau/12+tier*.12
   pts=[]
   for j in range(13):
    t=j/12;rr=.18+(radius-.18)*t
    pts.append((u+rr*math.cos(a),rr*math.sin(a),zz-.42*math.sin(t*math.pi)+.15*t))
   curve(m,pts,.034*scale,GOLD)
   xx=u+radius*math.cos(a);yy=radius*math.sin(a)
   m.cylinder(cx+xx,cy+yy,zz+.13,.13*scale,.05,GOLD,12)
   m.cylinder(cx+xx,cy+yy,zz+.18,.047*scale,.25,IVORY,8)
   sphere(m,xx,yy,zz+.47,.055,LIGHTGLASS)
m.finish()
# Hymn boards belong to real piers, not arbitrary points across the nave.
HYMN=mat('M_Hymn_Board',(.025,.026,.022),.57,texture='ChurchDoor')
m=Mesh('SM_Domkyrka_Hymn_Boards','Cathedral interior')
for u in [-23,-10.6,23]:
 for side in [-1,1]:
  pier_v=side*7.9
  # Pier inward face is at |v|=7.375. Back overlaps it by 10 mm.
  v=side*7.31;front=v-side*.105
  box(m,u,v,6.1,1.2,.15,1.7,HYMN)
  for z in [5.2,7.0]:box(m,u,front,z,1.4,.14,.13,GOLD)
  for dx in [-.635,.635]:box(m,u+dx,front,6.1,.13,.14,1.9,GOLD)
  box(m,u,front,7.13,.08,.08,.22,GOLD)
  sphere(m,u,front,7.35,.20,GOLD)
  # Through-mounted back cleats terminate inside the plaster pier.
  for z in [5.55,6.65]:
   box(m,u,side*7.39,z,.92,.10,.08,IRON)
   for dx in [-.44,.44]:box(m,u+dx,side*7.39,z,.065,.14,.19,IRON)
m.finish()
# Continuous physical load path: floor plinth, caryatid, bowl and pier fixings.
m=Mesh('SM_Domkyrka_Pulpit_Support','Cathedral interior')
for z,w,d,h in [(1.36,.96,.96,.08),(1.42,.82,.82,.08)]:box(m,8.55,7.9,z,w,d,h,MARBLE)
# Flush plaster pier face behind the pulpit, as in the reference photograph.
box(m,9.875,7.9,6.42,.20,1.05,6.30,IVORY)
# Short shaped consoles connect bowl and canopy to that board.
for zz in [4.28,9.30]:
 box(m,9.54,7.9,zz,.74,.64,.20,GREEN)
 for vv in [7.63,8.17]:rod(m,(9.82,vv,zz-.46),(9.22,vv,zz),.048,IRON)
m.finish()
# Area lights for the Blender reference renders. UE counterparts are real lights.
for u in [-18,0,18]:
 bpy.ops.object.light_add(type='AREA',location=(cx+u,cy,13));light=bpy.context.object;light.name='Interior_Soft_'+str(u);light.data.energy=2200;light.data.shape='DISK';light.data.size=10
for u in [-23,23]:
 for v in [-5.8,5.8]:
  bpy.ops.object.light_add(type='AREA',location=(cx+u,cy+v,8));light=bpy.context.object;light.name='Interior_Window';light.data.energy=1400;light.data.size=4;light.rotation_euler=(Vector((cx,cy,4))-light.location).to_track_quat('-Z','Y').to_euler()
