"""Procedural carved forms for detail pass 2. Shapes interpreted from photos,
not scanned sculpture. Local front points toward -X, Y is left/right.
"""
def ellipsoid(m,u,v,z,rx,ry,rz,ma,n=24,rings=16):
 verts=[]
 for j in range(rings+1):
  t=math.pi*j/rings
  for i in range(n):
   a=i*math.tau/n;verts.append((cx+u+rx*math.sin(t)*math.cos(a),cy+v+ry*math.sin(t)*math.sin(a),z+rz*math.cos(t)))
 m.faces(verts,[(j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i) for j in range(rings) for i in range(n)],ma,True)
def leaf(m,u,v,z,w,h,ma=GOLD,axis='x',direction=1):
 # Cupped acanthus leaf: scalloped margin, curved tip, central keel, fine veins.
 verts=[];rows,cols=16,8
 for i in range(rows+1):
  t=i/rows;span=w*math.sin(math.pi*t)**.72*(.84+.16*math.cos(t*math.pi*10))
  for j in range(cols+1):
   q=-1+2*j/cols;depth=(.14*w*(1-q*q)+.30*w*t**4)*math.sin(math.pi*t*.85)
   depth+=.025*w*math.cos(t*math.pi*12+abs(q)*5)*(abs(q)**.6)
   xyz=(cx+u+direction*depth,cy+v+q*span/2,z+t*h) if axis=='x' else (cx+u+q*span/2,cy+v+direction*depth,z+t*h)
   verts.append(xyz)
 m.faces(verts,[(i*(cols+1)+j,i*(cols+1)+j+1,(i+1)*(cols+1)+j+1,(i+1)*(cols+1)+j) for i in range(rows) for j in range(cols)],ma,True)
 # Central vein is shallow enough to read as carving rather than a separate rod.
 pts=[]
 for i in range(15):
  t=i/16;d=(.14*w+.30*w*t**4)*math.sin(math.pi*t*.85)+.008
  pts.append((u+direction*d,v,z+t*h) if axis=='x' else (u,v+direction*d,z+t*h))
 curve(m,pts,max(.003,w*.025),ma)
def rosette(m,u,v,z,r,ma=GOLD,axis='x'):
 # Lenticular petals with a small raised heart.
 for k in range(8):
  a=k*math.tau/8
  if axis=='x':ellipsoid(m,u,v+r*.52*math.cos(a),z+r*.52*math.sin(a),r*.11,r*.27,r*.27,ma,12,8)
  else:ellipsoid(m,u+r*.52*math.cos(a),v,z+r*.52*math.sin(a),r*.27,r*.11,r*.27,ma,12,8)
 sphere(m,u,v,z,r*.19,ma)
def turn_vertices(m,start,u,v,yaw):
 c,s=math.cos(yaw),math.sin(yaw)
 for i in range(start,len(m.v)):
  x,y,z=m.v[i];xx=x-cx-u;yy=y-cy-v;m.v[i]=(cx+u+xx*c-yy*s,cy+v+xx*s+yy*c,z)
def limb(m,a,b,r0,r1,ma,n=16):
 a,b=Vector(a),Vector(b);d=(b-a).normalized();seed=Vector((0,0,1)) if abs(d.z)<.9 else Vector((0,1,0));s=d.cross(seed).normalized();t=d.cross(s)
 vs=[];steps=8
 for j in range(steps+1):
  q=j/steps;r=(r0*(1-q)+r1*q)*(1+.08*math.sin(math.pi*q));p=a.lerp(b,q)
  for k in range(n):
   pos=p+r*(s*math.cos(k*math.tau/n)+t*math.sin(k*math.tau/n));vs.append((cx+pos.x,cy+pos.y,pos.z))
 m.faces(vs,[(j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k) for j in range(steps) for k in range(n)]+[tuple(range(n-1,-1,-1)),tuple(range(steps*n,(steps+1)*n))],ma,True)
def figure(m,u,v,z,h,ma=GOLD,pose='rest',yaw=0):
 start=len(m.v);n=72 if h>1.5 else 36;rows=64 if h>1.5 else 32
 # Contrapposto and layered hanging cloth, with folds changing through the waist.
 verts=[]
 for j in range(rows+1):
  t=j/rows;zz=.035+.755*t
  profile=[(0,.178),(.24,.161),(.48,.102),(.67,.078),(.87,.110),(1,.098)]
  for (a,ra),(b,rb) in zip(profile,profile[1:]):
   if a<=t<=b:ry=h*(ra+(rb-ra)*(t-a)/(b-a));break
  rx=h*(.074+.033*(1-t)+.015*math.exp(-((t-.8)/.14)**2))
  sway=h*(.038*math.sin(math.pi*t)-.024*(1-t))
  for k in range(n):
   a=k*math.tau/n
   hanging=(.014*math.sin(9*a+2.7*t+1.6*math.sin(6*t))+.006*math.cos(15*a-3*t))*(1-.60*t)
   mantle=.022*math.sin(14*t+3*a+2*math.sin(a))*(max(0,-math.cos(a))**3)
   fold=h*(hanging+mantle);hem=.009*h*math.sin(5*a)*(1-t)**5
   verts.append((cx+u+(rx+fold)*math.cos(a)-.012*h*math.sin(math.pi*t),cy+v+sway+(ry+fold)*math.sin(a),z+h*zz+hem+h*.025*t**8*(1-abs(math.sin(a))**.65)))
 m.faces(verts,[(j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k) for j in range(rows) for k in range(n)]+[tuple(range(n-1,-1,-1)),tuple(range(rows*n,(rows+1)*n))],ma,True)
 ellipsoid(m,u-.008*h,v-.006*h,z+.818*h,.035*h,.036*h,.038*h,ma,24,16)
 head_start=len(m.v)
 # Continuous sculpted head. Eyes, cheeks, nose and mouth deform one surface.
 verts=[];nr=48 if h>1.5 else 24;nc=64 if h>1.5 else 32
 def g(y,z0,yy,zz,sy,sz):return math.exp(-((y-yy)/sy)**2-((z0-zz)/sz)**2)
 for j in range(nr+1):
  t=math.pi*j/nr;zz=.878+.106*math.cos(t)
  jaw=.79+.21*min(1,max(0,(zz-.786)/.09))
  for k in range(nc):
   a=k*math.tau/nc;yy=.068*math.sin(t)*math.sin(a)*jaw
   xx=-.018+.076*math.sin(t)*math.cos(a);front=max(0,-math.cos(a))**10
   depth=-.024*g(yy,zz,0,.875,.014,.030)-.008*g(yy,zz,0,.85,.032,.014)
   depth+=.007*g(yy,zz,0,.843,.036,.0035)
   for sign in [-1,1]:
    depth+=.013*g(yy,zz,sign*.029,.897,.018,.011)
    depth-=.011*g(yy,zz,sign*.030,.914,.024,.008)
    depth-=.011*g(yy,zz,sign*.044,.872,.020,.018)
   xx+=front*depth
   # Slight head inclination as in carved standing figures.
   yy+=.006*(zz-.878)/.106
   verts.append((cx+u+xx*h,cy+v+yy*h,z+zz*h))
 m.faces(verts,[(j*nc+k,j*nc+(k+1)%nc,(j+1)*nc+(k+1)%nc,(j+1)*nc+k) for j in range(nr) for k in range(nc)],ma,True)
 for sign in [-1,1]:
  ellipsoid(m,u-.014*h,v+sign*.064*h,z+.873*h,.014*h,.013*h,.027*h,ma,16,12)
  # Eyes seated in the modeled socket, with fine upper lids.
  ellipsoid(m,u-.082*h,v+(sign*.029+.004)*h,z+.897*h,.008*h,.013*h,.0055*h,ma,16,12)
  curve(m,[(u-.089*h,v+(sign*.029+.004+.014*math.cos(t))*h,z+(.897+.005*math.sin(t))*h) for t in [i*math.pi/16 for i in range(17)]],.0018*h,ma,8)
 # Curled hair is kept on the crown, sides and back, leaving the face open.
 for k in range(19):
  a=k*math.tau/19
  for row in range(2 if h>1 else 1):
   if math.cos(a)<-.4 and row>0:continue
   points=[]
   for i in range(21):
    t=i/20;aa=a+.09*math.sin(t*math.pi*2)
    zz=.983-(.047 if math.cos(a)<-.4 else .135)*t-row*.036
    rr=.076*math.sqrt(max(.015,1-((zz-.878)/.106)**2))+.003+.002*math.sin(t*math.pi*4)
    points.append((u+(-.007+rr*math.cos(aa))*h,v+(rr*math.sin(aa)+.013)*h,z+zz*h))
   curve(m,points,.0055*h,ma,10)
 # Bring the head to classical human proportions (about one seventh of height).
 for i in range(head_start,len(m.v)):
  xx,yy,zz=m.v[i];m.v[i]=(cx+u+(xx-cx-u)*.86,cy+v+(yy-cy-v)*.84,z+h*.91+(zz-z-h*.878)*.69)
 for sign in [-1,1]:
  shoulder=(u-.008*h,v+sign*.108*h,z+.765*h)
  if pose=='chalice' and sign<0:elbow=(u-.067*h,v-.225*h,z+.562*h);wrist=(u-.17*h,v-.28*h,z+.67*h)
  elif pose=='raised' and sign<0:elbow=(u-.045*h,v-.24*h,z+.76*h);wrist=(u-.08*h,v-.22*h,z+.91*h)
  elif pose=='wide':elbow=(u-.07*h,v+sign*.26*h,z+.72*h);wrist=(u-.09*h,v+sign*.37*h,z+.77*h)
  else:elbow=(u-.08*h,v+sign*.215*h,z+.55*h);wrist=(u-.17*h,v+sign*.17*h,z+.60*h)
  ellipsoid(m,*shoulder,.045*h,.045*h,.043*h,ma,24,16)
  limb(m,shoulder,elbow,.043*h,.028*h,ma,20);ellipsoid(m,*elbow,.033*h,.032*h,.034*h,ma,16,12)
  limb(m,elbow,wrist,.033*h,.021*h,ma,20)
  ellipsoid(m,wrist[0],wrist[1],wrist[2]+.020*h,.022*h,.027*h,.040*h,ma,20,12)
  for finger in range(4):
   yy=wrist[1]+(finger-1.5)*.012*h
   curve(m,[(wrist[0]-.008*h-.018*h*math.sin(t*math.pi*.8),yy,wrist[2]+(.040+.035*t)*h) for t in [i/12 for i in range(13)]],.005*h,ma,10)
  curve(m,[(wrist[0]-.01*h-t*.027*h,wrist[1]+sign*.025*h,wrist[2]+(.02+.018*math.sin(t*math.pi))*h) for t in [i/12 for i in range(13)]],.007*h,ma,10)
  ellipsoid(m,u-.065*h,v+sign*.078*h,z+.029*h,.080*h,.035*h,.028*h,ma,24,12)
 # A folded drape from one shoulder to the opposite hip; volume and curled hem.
 verts=[]
 for i in range(45):
  t=i/44
  for j in range(17):
   q=j/16;yy=(-.099+.197*t)*h
   zz=(.768-.275*t-.15*q+.028*math.sin(math.pi*t))*h
   xx=(-.112*math.sqrt(max(.12,1-(yy/(.12*h))**2))-.024-.008*math.cos(q*math.pi*4)) * h
   verts.append((cx+u+xx,cy+v+yy,z+zz))
 faces=[(i*17+j,i*17+j+1,(i+1)*17+j+1,(i+1)*17+j) for i in range(44) for j in range(16)]
 # A closed drape volume survives voxel union without torn, needle-like edges.
 offset=len(verts);verts += [(x+.10*h,y,zz) for x,y,zz in verts]
 faces += [tuple(offset+k for k in reversed(f)) for f in list(faces)]
 boundary=list(range(17))+[i*17+16 for i in range(1,45)]+list(range(44*17+15,44*17-1,-1))+[i*17 for i in range(43,0,-1)]
 faces += [(a,b,b+offset,a+offset) for a,b in zip(boundary,boundary[1:]+boundary[:1])]
 m.faces(verts,faces,ma,True)
 if h>1.5:
  # Fuse overlapping sculptural masses; retain small folds through a 5-6 mm voxel.
  end=len(m.v);firstface=next(i for i,f in enumerate(m.f) if min(f)>=start)
  data=bpy.data.meshes.new('SculptUnion');data.from_pydata(m.v[start:end],[],[tuple(k-start for k in f) for f in m.f[firstface:]]);data.update()
  ob=bpy.data.objects.new('SculptUnion',data);bpy.context.collection.objects.link(ob)
  bpy.ops.object.select_all(action='DESELECT');ob.select_set(True);bpy.context.view_layer.objects.active=ob
  mod=ob.modifiers.new('Unify carved masses','REMESH');mod.mode='VOXEL';mod.voxel_size=h*.0028;mod.use_smooth_shade=True
  bpy.ops.object.modifier_apply(modifier=mod.name)
  mod=ob.modifiers.new('Relax sculpt surface','SMOOTH');mod.factor=.35;mod.iterations=3;bpy.ops.object.modifier_apply(modifier=mod.name)
  mod=ob.modifiers.new('Keep hero silhouette','DECIMATE');mod.ratio=.65;bpy.ops.object.modifier_apply(modifier=mod.name)
  vv=[tuple(q.co) for q in ob.data.vertices];ff=[tuple(q.vertices) for q in ob.data.polygons]
  del m.v[start:];del m.f[firstface:];del m.mi[firstface:];del m.sm[firstface:];del m.fuv[firstface:]
  m.faces(vv,ff,ma,True);bpy.data.objects.remove(ob,do_unlink=True)
 turn_vertices(m,start,u,v,yaw)
def wing(m,u,v,z,w,h,ma=IVORY,side=1):
 # Layered flight feathers, each with tapered tip and a curved shaft.
 for row in range(2):
  count=9 if row==0 else 7
  for k in range(count):
   t=k/(count-1);length=h*(.62+.35*t)*(1-.32*row)
   a=(.25+t*.9)*side
   root=(u,v+side*w*.08*row,z+.10*h*row)
   pts=[(root[0]-.10*w*math.sin(q*math.pi),root[1]+side*w*(.15+.85*t)*q,root[2]+length*q-.16*h*q*q) for q in [j/14 for j in range(15)]]
   # tapered feather tube with smooth continuous silhouette
   for j in range(len(pts)-1):limb(m,pts[j],pts[j+1],w*.038*(1-j/15),max(.004,w*.038*(1-(j+1)/15)),ma,8)
def capital(m,u,v,z,r,h,ma):
 # Two staggered acanthus crowns, each leaf facing radially outward.
 for row in range(2):
  for k in range(12):
   a=(k+row*.5)*math.tau/12;start=len(m.v)
   leaf(m,u+r,v,z+row*h*.38,r*.55,h*.76,ma,'x',1)
   turn_vertices(m,start,u,v,a)
 for k in range(8):
  a=k*math.tau/8;start=len(m.v)
  curve(m,[(u+r*.94,v+r*.33*(1-i/55)*math.cos(i*math.tau/30),z+h*.83+r*.33*(1-i/55)*math.sin(i*math.tau/30)) for i in range(45)],r*.06,ma)
  turn_vertices(m,start,u,v,a)
