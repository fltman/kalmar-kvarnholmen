"""Solid curved reveals, small joinery and modular industrial masonry."""
def p18_new(name,category='Kvarnholmen/Reference corrections'):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 pass18_names.append(name);return Mesh(name,category)
def p18_face(m,x,y,L,H,holes,ma,a=0):
 # Genuine rectangular cuts, then solid curved spandrels. No rectangular top rail across an arch.
 lm_wall(m,x,y,L,H,[(u,b,w,h+r,False) for u,b,w,h,r in holes],ma,a)
 for u,b,w,h,r in holes:
  if r<=0:continue
  for k in range(24):
   t0=k*math.pi/24;t1=(k+1)*math.pi/24
   u0,u1=u+w/2*math.cos(t0),u+w/2*math.cos(t1);z0,z1=b+h+r*math.sin(t0),b+h+r*math.sin(t1)
   vs=[lp(x,y,uu,o,zz,a) for o in [.005,.355] for uu,zz in [(u0,z0),(u1,z1),(u1,b+h+r),(u0,b+h+r)]]
   m.faces(vs,[(0,1,2,3),(7,6,5,4),(0,4,5,1)],ma)
def p18_arch(m,x,y,z,w,r,thick,out,a,ma,n=24):
 for k in range(n):
  t0=k*math.pi/n;t1=(k+1)*math.pi/n
  vs=[lp(x,y,(w/2+dr)*math.cos(t),o,z+(r+dr)*math.sin(t),a) for o in [out-.04,out+.04] for dr,t in [(0,t0),(0,t1),(thick,t1),(thick,t0)]]
  m.faces(vs,[(0,1,2,3),(7,6,5,4),(0,4,5,1),(3,2,6,7),(1,5,6,2),(0,3,7,4)],ma)
def p18_win(m,x,y,u,b,w,h,r=0,a=0,frame=None,trim=None,rows=3,cols=2):
 frame=frame or P18['GreenJoinery'];trim=trim or P18['BrickRed'];xx,yy,_=lp(x,y,u,0,0,a)
 # Black recess and glass follow the actual arched boundary.
 contour=[(-w/2,b),(w/2,b)]+[(w/2*math.cos(k*math.pi/24),b+h+r*math.sin(k*math.pi/24)) for k in range(25)]
 m.faces([lp(xx,yy,q,.105,z,a) for q,z in contour],[tuple(range(len(contour)))],GLAZE)
 for q in [-w/2,w/2]:
  facade_box(m,xx,yy,q,.205,b+h/2,.055,.12,h,frame,a)
  facade_box(m,xx,yy,q+(.065 if q>0 else -.065),.39,b+h/2,.13,.16,h+.05,trim,a)
 facade_box(m,xx,yy,0,.20,b,w,.13,.06,frame,a)
 if r>0:p18_arch(m,xx,yy,b+h,w,r,.055,.205,a,frame);p18_arch(m,xx,yy,b+h,w+.12,r+.06,.14,.39,a,trim)
 else:
  facade_box(m,xx,yy,0,.205,b+h,w,.12,.055,frame,a);facade_box(m,xx,yy,0,.39,b+h+.07,w+.25,.16,.14,trim,a)
 for k in range(1,cols):
  q=-w/2+w*k/cols;top=b+h+(r*math.sqrt(max(0,1-(2*q/w)**2)) if r else 0);facade_box(m,xx,yy,q,.22,(b+top)/2,.028,.08,top-b,frame,a)
 for k in range(1,rows):facade_box(m,xx,yy,0,.22,b+h*k/rows,w,.08,.027,frame,a)
 facade_box(m,xx,yy,0,.46,b-.07,w+.3,.46,.075,trim,a)
def p18_band(m,x,y,L,z,a,ma,depth=.49):
 for zz,dd,hh in [(z-.08,depth-.05,.10),(z,depth,.075),(z+.07,depth+.06,.065)]:facade_box(m,x,y,0,dd/2+.17,zz,L,dd,hh,ma,a)
def p18_rustic(m,x,y,L,H,holes,a,ma):
 for k in range(1,int(H/.42)):
  z=k*.42;spans=[(-L/2,L/2)]
  for u,b,w,h,r in holes:
   if b-.12<z<b+h+r+.15:spans=[(lo,hi) for l,rr in spans for lo,hi in [(l,min(rr,u-w/2-.16)),(max(l,u+w/2+.16),rr)] if hi-lo>.02]
  for lo,hi in spans:facade_box(m,x,y,(lo+hi)/2,.362,z,hi-lo,.014,.014,ma,a)
def p18_finish(m):
 obj=m.finish();obj['detail_pass']=18;obj['reference_notes']='references/pass18-notes.md';return obj
