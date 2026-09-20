"""Painted pew joinery interpreted from interior-east.jpg.
Metres; closed panels and mouldings, with millimetre-scale painted ornament.
The motifs are modeled interpretations, not exact tracings of the originals.
Executed in the build_blender namespace.
"""
PEWTRIM=mat('M_Pew_Trim',(.45,.47,.435),.40,texture='ChurchPewTrim')
PEWPAINT=mat('M_Pew_Ornament',(.022,.029,.026),.48)

def pew_rail(m,u,v,z,length):
 # Extruded handrail with a rounded crown and a small lower quirk.
 profile=[(-.10,-.045),(.10,-.045)]
 profile += [(.10*math.cos(i*math.pi/16),.005+.048*math.sin(i*math.pi/16)) for i in range(17)]
 profile += [(-.10,-.045)]
 profile=profile[:-1];n=len(profile)
 verts=[(cx+u+x,cy+v+y,z+zz) for x in [-length/2,length/2] for y,zz in profile]
 m.faces(verts,[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],PEWTRIM,True)
 box(m,u,v,z-.065,length,.15,.030,PEWTRIM)

def pew_frame(m,u,v,z,sign,width,height):
 # Raised-and-fielded panel: three nested mouldings, stepped corner returns.
 def outline(w,h,step):
  a,b=w/2,h/2;s=step
  return [(-a+s,-b),(a-s,-b),(a-s,-b+s),(a,-b+s),(a,b-s),(a-s,b-s),(a-s,b),(-a+s,b),(-a+s,b-s),(-a,b-s),(-a,-b+s),(-a+s,-b+s)]
 for w,h,thick,depth,ma in [(width,height,.027,.014,PEWTRIM),(width-.065,height-.065,.006,.029,GOLD),(width-.086,height-.086,.012,.022,PEWTRIM)]:
  outer=outline(w,h,.056);inner=outline(w-2*thick,h-2*thick,.049)
  verts=[(cx+u+x,cy+v+sign*d,z+zz) for d in [0,depth] for ring in [outer,inner] for x,zz in ring]
  n=len(outer);faces=[]
  for i in range(n):
   j=(i+1)%n
   faces.extend([(i,j,j+2*n,i+2*n),(i+n,i+3*n,j+3*n,j+n),(i+2*n,j+2*n,j+3*n,i+3*n),(i,i+n,j+n,j)])
  m.faces(verts,faces,ma)

def pew_scroll(m,u,v,z,sign):
 # Small dark painted scrollwork laid just proud of the stile, not metal rods.
 # A flat ribbon cross-section keeps the motif close to the painted surface.
 def ribbon(points,width=.009):
  verts=[]
  for i,(x,zz) in enumerate(points):
   a=Vector(points[max(0,i-1)]);b=Vector(points[min(len(points)-1,i+1)])
   tangent=(b-a).normalized();side=Vector((-tangent.y,tangent.x))*width/2
   for d in [0,.0025]:
    for q in [-1,1]:verts.append((cx+u+x+q*side.x,cy+v+sign*d,z+zz+q*side.y))
  faces=[]
  for i in range(len(points)-1):
   a=i*4;b=(i+1)*4
   faces.extend([(a,b,b+1,a+1),(a+2,a+3,b+3,b+2),(a,a+2,b+2,b),(a+1,b+1,b+3,a+3)])
  end=len(verts)-4
  faces.extend([(0,1,3,2),(end,end+2,end+3,end+1)])
  m.faces(verts,faces,PEWPAINT)
 for s in [-1,1]:
  for flip in [-1,1]:
   pts=[]
   for i in range(29):
    t=i/28;a=t*math.pi*2.25;r=.040*(1-.78*t)
    pts.append((s*(.017+r*math.sin(a)),flip*(.095+r*math.cos(a))))
   ribbon(pts)
  ribbon([(s*(.018+.021*math.sin(t*math.pi)),.19*(t-.5)) for t in [i/20 for i in range(21)]],.011)
 ribbon([(0,-.18),(0,.18)],.009)

def pew_unit(m,u,v,length,yaw=0):
 start=len(m.v)
 # Seat and gently raked back. Separate lower support and book ledge.
 box(m,u+.045,v,1.84,.47,length-.10,.095,PEW)
 verts=[(cx+u+x,cy+v+y,z) for y in [-length/2,length/2] for x,z in [(-.31,1.81),(-.18,1.81),(-.29,2.51),(-.41,2.51)]]
 m.faces(verts,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],PEW)
 # Back top follows the same restrained grey joinery, without plaster texture.
 box(m,u-.35,v,2.53,.21,length+.04,.08,PEWTRIM)
 box(m,u-.42,v,2.15,.16,length-.12,.042,PEWTRIM)
 for vv in [-length*.38,length*.38]:
  box(m,u,v+vv,1.57,.115,.115,.48,PEW)
  box(m,u+.02,v+vv,1.39,.50,.14,.07,PEWTRIM)
 for side in [-1,1]:
  end=v+side*(length/2+.02)
  # Solid door face with an inset field, frame, stiles and skirting.
  box(m,u,end,1.935,1.12,.11,1.19,PEW)
  box(m,u,end+side*.060,1.98,.70,.015,.85,PANEL)
  face=end+side*.071
  pew_frame(m,u,face,1.98,side,.71,.89)
  for offset in [-.465,.465]:
   box(m,u+offset,end+side*.008,1.965,.10,.13,1.12,PEWTRIM)
   pew_scroll(m,u+offset,end+side*.077,2.00,side)
  box(m,u,end,1.405,1.15,.15,.095,PEWTRIM)
  box(m,u,end,1.47,1.145,.14,.025,PEWTRIM)
  pew_rail(m,u,end,2.565,1.17)
  # Compact brass latch and two leaf hinges, kept subordinate to painted decor.
  box(m,u+.35,face+side*.018,2.24,.024,.008,.065,GOLD)
  rod(m,(u+.35,face+side*.027,2.22),(u+.35,face+side*.027,2.25),.009,GOLD,8)
  for zz in [1.63,2.32]:
   box(m,u-.36,face+side*.014,zz,.037,.012,.052,IRON)
   rod(m,(u-.365,face+side*.027,zz-.031),(u-.365,face+side*.027,zz+.031),.008,IRON,8)
 if yaw:
  c,s=math.cos(yaw),math.sin(yaw)
  for i in range(start,len(m.v)):
   x,y,z=m.v[i];x-=cx+u;y-=cy+v;m.v[i]=(cx+u+x*c-y*s,cy+v+x*s+y*c,z)

m=Mesh('SM_Domkyrka_Pews','Cathedral interior')
for u in [-18+i*1.17 for i in range(25)]:
 if -2.0<u<2.5:continue
 for sign in [-1,1]:pew_unit(m,u,sign*3.6,4.70)
for sign in [-1,1]:
 for side in [-1,1]:
  for j in range(5):pew_unit(m,side*4.4,sign*(9.0+j*1.2),4.9,-sign*math.pi/2)
m.finish()
