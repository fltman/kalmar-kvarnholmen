"""Reference-informed shaped gables and broad, continuous coping stones."""
def b19_arch(m,x,y,z,w,r,thick,out,depth,a,ma):
 n=64;profile=[(0,out-depth/2),(0,out+depth/2),(thick,out+depth/2),(thick,out-depth/2)]
 verts=[lp(x,y,(w/2+dr)*math.cos(math.pi*i/n),o,z+(r+dr)*math.sin(math.pi*i/n),a) for i in range(n+1) for dr,o in profile]
 m.faces(verts,[(i*4+j,i*4+(j+1)%4,(i+1)*4+(j+1)%4,(i+1)*4+j) for i in range(n) for j in range(4)]+[(3,2,1,0),(n*4,n*4+1,n*4+2,n*4+3)],ma)

def b19_win(m,x,y,u,b,w,h,r=0,a=0,frame=None,trim=None,rows=3,cols=2):
 if not r:return p18_win(m,x,y,u,b,w,h,r,a,frame,trim,rows,cols)
 frame=frame or P18['GreenJoinery'];trim=trim or P18['BathCream'];xx,yy,_=lp(x,y,u,0,0,a)
 contour=[(-w/2,b),(w/2,b)]+[(w/2*math.cos(k*math.pi/64),b+h+r*math.sin(k*math.pi/64)) for k in range(65)]
 m.faces([lp(xx,yy,q,.105,z,a) for q,z in contour],[tuple(range(len(contour)))],GLAZE)
 for sign in [-1,1]:
  facade_box(m,xx,yy,sign*(w/2-.025),.24,b+h/2,.10,.30,h,frame,a)
  facade_box(m,xx,yy,sign*(w/2+.065),.39,b+h/2,.13,.16,h+.05,trim,a)
 facade_box(m,xx,yy,0,.24,b,w,.30,.06,frame,a)
 b19_arch(m,xx,yy,b+h,w-.10,r-.05,.10,.24,.30,a,frame)
 b19_arch(m,xx,yy,b+h,w+.12,r+.06,.14,.39,.16,a,trim)
 for k in range(1,cols):
  q=-w/2+w*k/cols;top=b+h+r*math.sqrt(max(0,1-(2*q/w)**2))-.025
  facade_box(m,xx,yy,q,.25,(b+top)/2,.028,.08,top-b,frame,a)
 for k in range(1,rows):facade_box(m,xx,yy,0,.25,b+h*k/rows,w,.08,.027,frame,a)
 facade_box(m,xx,yy,0,.46,b-.07,w+.3,.46,.075,trim,a)

def b19_gable(m,gx,gy,gw,gr,base,wb,ww,wh,wr,a,render,stone):
 # Each half runs from the peak's rounded nose to the projecting shoulder.
 points=[]
 def bezier(p0,p1,p2,p3,n):
  for i in range(n):
   t=i/n;s=1-t
   points.append(tuple(s**3*p0[k]+3*s*s*t*p1[k]+3*s*t*t*p2[k]+t**3*p3[k] for k in range(2)))
 bezier((0,1),(.065,1),(.11,.97),(.16,.89),16)
 bezier((.16,.89),(.30,.70),(.49,.44),(.67,.19),24)
 bezier((.67,.19),(.72,.12),(.77,.11),(.89,.11),12)
 bezier((.89,.11),(.95,.10),(.95,.025),(1,0),10)
 points.append((1,0))
 points=[(-u,z) for u,z in reversed(points[1:])]+points
 pts=[(u*gw/2,base+z*gr) for u,z in points]
 # Include aperture jambs as exact split positions, avoiding missing slivers.
 for edge in [-ww/2,ww/2]:
  for j in range(len(pts)-1):
   p,q=pts[j:j+2]
   if p[0]<edge<q[0]:
    pts.insert(j+1,(edge,p[1]+(q[1]-p[1])*(edge-p[0])/(q[0]-p[0])));break
 for (u0,z0),(u1,z1) in zip(pts,pts[1:]):
  if (u0+u1)/2 < -ww/2 or (u0+u1)/2 > ww/2:lo0=lo1=base
  else:
   lo0=max(base,wb+wh+wr*math.sqrt(max(0,1-(2*u0/ww)**2)))
   lo1=max(base,wb+wh+wr*math.sqrt(max(0,1-(2*u1/ww)**2)))
  if min(z0-lo0,z1-lo1)>0:
   vs=[lp(gx,gy,u,o,z,a) for o in [.20,.385] for u,z in [(u0,lo0),(u1,lo1),(u1,z1),(u0,z0)]]
   m.faces(vs,[(0,3,2,1),(4,5,6,7),(3,7,6,2)],render)
 # Broad bevelled coping strip with a single continuous surface, no round beads.
 section=[(-.04,.22),(-.04,.44),(0,.50),(.16,.50),(.21,.43),(.21,.16)]
 n=len(section)
 verts=[lp(gx,gy,u,o,z+dz,a) for u,z in pts for dz,o in section]
 faces=[(j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i) for j in range(len(pts)-1) for i in range(n)]
 faces += [tuple(range(n-1,-1,-1)),tuple(range((len(pts)-1)*n,len(pts)*n))]
 m.faces(verts,faces,stone)
