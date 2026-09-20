"""Solid plaster Ionic capital relief, interpreted from the interior photos.
Added in front of the existing shallow scroll outlines; no structural changes.
"""
def ionic_curve(m,points,r,ma,n=12):
 # A stable transported frame: the generic sweep switched reference axes at
 # steep tangents, which twisted the spiral quads at each quarter turn.
 pts=[Vector(p) for p in points];verts=[]
 for i,p in enumerate(pts):
  tangent=(pts[min(i+1,len(pts)-1)]-pts[max(i-1,0)]).normalized()
  e=Vector((0,1,0));e=(e-tangent*e.dot(tangent)).normalized();f=tangent.cross(e)
  for k in range(n):
   q=p+r*(e*math.cos(k*math.tau/n)+f*math.sin(k*math.tau/n));verts.append((cx+q.x,cy+q.y,q.z))
 faces=[(i*n+k,i*n+(k+1)%n,(i+1)*n+(k+1)%n,(i+1)*n+k) for i in range(len(pts)-1) for k in range(n)]
 faces += [tuple(range(n-1,-1,-1)),tuple(range((len(pts)-1)*n,len(pts)*n))]
 m.faces(verts,faces,ma,True)
m=Mesh('SM_Domkyrka_Ionic_Details','Cathedral interior details')
for u in [-23,-10.6,10.6,23]:
 for v in [-7.9,7.9]:
  direction=1 if v<0 else -1;front=v+direction*.64
  box(m,u,front,14.36,1.75,.28,.12,IVORY)
  box(m,u,front+direction*.04,14.43,1.94,.32,.055,IVORY)
  # Each volute is a closed shallow carved drum with a curled face ridge.
  for s in [-1,1]:
   uu=u+s*.62;zz=14.04;verts=[];n=64
   for depth,r in [(0,.31),(.055,.39),(.12,.39),(.16,.34)]:
    for i in range(n):
     a=i*math.tau/n;verts.append((cx+uu+r*math.cos(a),cy+front+direction*depth,zz+r*math.sin(a)))
   faces=[tuple(range(n-1,-1,-1)),tuple(range(3*n,4*n))]
   faces += [(j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i) for j in range(3) for i in range(n)]
   m.faces(verts,faces,IVORY,True)
   ionic_curve(m,[(uu+.34*math.cos(i*math.tau/64),front+direction*.17,zz+.34*math.sin(i*math.tau/64)) for i in range(65)],.026,IVORY,10)
   pts=[]
   for i in range(101):
    t=i/100;a=s*(math.pi*.45+t*math.pi*4.3);r=.305*(1-t)+.026
    pts.append((uu+r*math.cos(a),front+direction*(.18+.018*t),zz+r*math.sin(a)))
   ionic_curve(m,pts,.024,IVORY,10)
  # Echinus cushion with egg-and-dart carving between the scrolls.
  box(m,u,front,13.99,.68,.20,.25,IVORY)
  for i in range(5):
   uu=u+(i-2)*.125
   ellipsoid(m,uu,front+direction*.135,14.03,.045,.035,.095,IVORY,16,12)
   pts=[(uu+.052*math.cos(a),front+direction*.16,14.03+.105*math.sin(a)) for a in [math.pi+j*math.pi/24 for j in range(25)]]
   ionic_curve(m,pts,.011,IVORY,8)
  for z,w,d,h in [(13.80,1.24,.20,.045),(13.74,1.18,.16,.06)]:box(m,u,front,z,w,d,h,IVORY)
m.finish()
