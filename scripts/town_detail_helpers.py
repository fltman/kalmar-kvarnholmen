"""Pass 9: modelled metalwork, joinery and profiled hotel copperwork.
Photo-informed shapes, not scans. Units are metres.
"""
TC=mat('M_Town_Copper',(.082,.205,.158),.75,.15,'ChurchCopperFine')
def town_band_gap(m,x,y,z,length,ang,gap_width,ma=TW,scale=1,gap_center=0):
 # Stop the projecting plinth/cornice at the jamb instead of crossing the door leaf.
 for lo,hi in [(-length/2,gap_center-gap_width/2),(gap_center+gap_width/2,length/2)]:
  if hi>lo:
   xx,yy,_=facade_point(x,y,(lo+hi)/2,0,0,ang)
   town_band(m,xx,yy,z,hi-lo,ang,ma,scale)
def town_border(m,x,y,z,w,h,ang,ma,out=.25,th=.025):
 for u in [-w/2,w/2]:facade_box(m,x,y,u,out,z,th,.035,h,ma,ang)
 for zz in [z-h/2,z+h/2]:facade_box(m,x,y,0,out,zz,w,.035,th,ma,ang)
def town_door(m,x,y,bottom,w,h,ang,ma,glazed=False,lattice=False):
 def b(u,o,zz,ww,dd,hh,material):facade_box(m,x,y,u,o,zz,ww,dd,hh,material,ang)
 z=bottom+h/2
 b(0,.025,z,w+.30,.08,h+.16,IRON)
 b(0,.105,z,w,.12,h,ma)
 for u in [-w/2-.075,w/2+.075]:
  b(u,.17,z,.14,.26,h+.22,TS);b(u,.31,z,.035,.035,h+.16,ma)
 b(0,.17,bottom+h+.075,w+.42,.26,.15,TS)
 b(0,.29,bottom+.05,w+.20,.50,.10,TS)
 b(0,.19,z,.045,.08,h,ma)
 for side in [-1,1]:
  u=side*w*.25
  for frac,size in ([(.24,.28),(.70,.53)] if glazed else [(.18,.22),(.50,.28),(.82,.22)]):
   zz=bottom+h*frac;hh=h*size;ww=w*.37
   b(u,.172,zz,ww,.035,hh,town_mats['Glass'] if glazed and frac>.5 else ma)
   town_border(m,*facade_point(x,y,u,0,0,ang)[:2],zz,ww,hh,ang,ma,.235,.043)
   town_border(m,*facade_point(x,y,u,0,0,ang)[:2],zz,ww-.085,hh-.085,ang,ma,.203,.017)
   if glazed and lattice and frac>.5:
    # Clipped diamond grille confined to the upper glazed panel.
    hw=ww/2-.07;hh2=hh/2-.07
    for slope in [-1,1]:
     for k in range(-10,11):
      intercept=k*.18;pts=[]
      for px in [-hw,hw]:
       py=slope*px+intercept
       if -hh2<=py<=hh2:pts.append((px,py))
      for py in [-hh2,hh2]:
       px=(py-intercept)/slope
       if -hw<px<hw:pts.append((px,py))
      if len(pts)==2:town_rod(m,facade_point(x,y,u+pts[0][0],.228,zz+pts[0][1],ang),facade_point(x,y,u+pts[1][0],.228,zz+pts[1][1],ang),.009,IRON)
  hu=side*.10;hz=bottom+h*.49
  b(hu,.245,hz,.085,.035,.23,IRON)
  town_path(m,[facade_point(x,y,hu,.26,hz-.08,ang),facade_point(x,y,hu,.35,hz-.08,ang),facade_point(x,y,hu,.35,hz+.08,ang),facade_point(x,y,hu,.26,hz+.08,ang)],.014,GOLD)
  for zz in [bottom+.33,bottom+h-.33]:b(side*(w/2-.04),.235,zz,.034,.047,.15,IRON)
def town_cross_window(m,x,y,z,w,h,ang,frame):
 # Narrow upper lights and tall lower casements, unlike the old equal grid.
 town_window(m,x,y,z,w,h,ang,frame,False,rows=1,cols=2)
 trans=z+h*.20
 facade_box(m,x,y,0,.19,trans,w,.13,.12,TW,ang)
 # Join the upright to the transom; overlapping coplanar faces flicker in close views.
 for low,high in [(z-h/2,trans-.06),(trans+.06,z+h/2)]:
  facade_box(m,x,y,0,.215,(low+high)/2,.045,.08,high-low,frame,ang)
 town_border(m,x,y,z,w-.14,h-.14,ang,frame,.20,.027)
 # Small wedge-shaped lintel stones from the facade photograph.
 for k in [-1,0,1]:
  u=k*w*.36
  town_polyprofile(m,*facade_point(x,y,u,.12,0,ang)[:2],z+h/2+.1,[(-.12,0),(.12,0),(.16,.27),(-.16,.27)],ang,TS,.12,False)
def town_arch_band(m,x,y,z,r,width,ang,ma,out=.23):
 vs=[]
 for o in [out-.15,out]:
  for rr in [r,r+width]:
   for j in range(49):vs.append(facade_point(x,y,rr*math.cos(j*math.pi/48),o,z+rr*math.sin(j*math.pi/48),ang))
 faces=[]
 for j in range(48):
  faces += [(j,j+1,49+j+1,49+j),(98+j,147+j,148+j,99+j),(j,98+j,99+j,j+1),(49+j,50+j,148+j,147+j)]
 faces += [(0,49,147,98),(48,146,195,97)]
 m.faces(vs,faces,ma)
def town_scroll(m,x,y,z,ang,sign=1,scale=1,out=.36,ma=TS):
 pts=[]
 for j in range(73):
  t=j/72*math.pi*3.5;r=scale*(.28-.23*j/72)
  pts.append(facade_point(x,y,sign*r*math.cos(t),out,z+r*math.sin(t),ang))
 town_path(m,pts,.042*scale,ma)
def town_leaf(m,x,y,z,ang,sign=1,scale=1):
 p=[(-.04,0),(-.16,.16),(-.10,.25),(-.20,.36),(-.13,.48),(0,.65),(.13,.48),(.20,.36),(.10,.25),(.16,.16),(.04,0)]
 town_polyprofile(m,x,y,z,[(sign*u*scale,h*scale) for u,h in p],ang,TS,.055,False)
 town_path(m,[facade_point(x,y,0,.055,z+h*scale,ang) for h in [0,.18,.36,.61]],.012,TS)
def town_square_loft(m,x,y,z,profile,ma):
 # Hermite interpolation smooths the roof's vertical profile while retaining its rim steps.
 dense=[]
 for i in range(len(profile)-1):
  r0,h0=profile[i];r1,h1=profile[i+1];prev=profile[max(0,i-1)];nxt=profile[min(len(profile)-1,i+2)]
  d0=(r1-prev[0])/(h1-prev[1]);d1=(nxt[0]-r0)/(nxt[1]-h0)
  for j in range(6):
   t=j/6;rad=(2*t**3-3*t*t+1)*r0+(t**3-2*t*t+t)*(h1-h0)*d0+(-2*t**3+3*t*t)*r1+(t**3-t*t)*(h1-h0)*d1
   dense.append((rad,h0+t*(h1-h0)))
 profile=dense+[profile[-1]]
 # An eight-sided square with clipped corners; 32 perimeter samples smooth the swept roof.
 shape=[(-1,-.78),(-.78,-1),(.78,-1),(1,-.78),(1,.78),(.78,1),(-.78,1),(-1,.78)]
 ring=[]
 for i,(u,v) in enumerate(shape):
  q=shape[(i+1)%8]
  for j in range(4):ring.append((u+(q[0]-u)*j/4,v+(q[1]-v)*j/4))
 n=len(ring);verts=[(x+u*r,y+v*r,z+h) for r,h in profile for u,v in ring]
 faces=[tuple(range(n-1,-1,-1))]
 for j in range(len(profile)-1):
  faces += [(j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i) for i in range(n)]
 faces.append(tuple(range((len(profile)-1)*n,len(profile)*n)))
 m.faces(verts,faces,ma,True)
 for i in range(0,n,4):
  u,v=ring[i];town_path(m,[(x+u*(r+.012),y+v*(r+.012),z+h+.01) for r,h in profile],.012,ma)
def town_lantern(m,x,y,z,ang):
 # Closed facade lantern with a bracket and four solid corner bars.
 p=lambda u,o,h:facade_point(x,y,u,o,h,ang)
 town_path(m,[p(0,.05,z+.25),p(0,.45,z+.45),p(0,.65,z+.35)],.025,IRON)
 facade_box(m,x,y,0,.63,z,.25,.26,.42,town_mats['Glass'],ang)
 for u in [-.15,.15]:
  for o in [.48,.78]:town_rod(m,p(u,o,z-.22),p(u,o,z+.23),.016,IRON)
 for dz in [-.24,.25]:facade_box(m,x,y,0,.63,z+dz,.34,.34,.05,IRON,ang)
 town_polyprofile(m,*p(0,.79,0)[:2],z+.28,[(-.2,0),(.2,0),(0,.20)],ang,IRON,.32,False)
def town_text(m,x,y,z,ang,text,width,ma):
 curve=bpy.data.curves.new('Temporary facade lettering','FONT');curve.body=text;curve.align_x='CENTER';curve.align_y='CENTER';curve.size=1;curve.extrude=.004;curve.resolution_u=4
 obj=bpy.data.objects.new('Temporary facade lettering',curve);bpy.context.collection.objects.link(obj)
 bpy.context.view_layer.objects.active=obj;obj.select_set(True);bpy.context.view_layer.update()
 scale=width/max(obj.dimensions.x,.01)
 deps=bpy.context.evaluated_depsgraph_get();me=bpy.data.meshes.new_from_object(obj.evaluated_get(deps))
 verts=[facade_point(x,y,v.co.x*scale,.02+v.co.z*scale,z+v.co.y*scale,ang) for v in me.vertices]
 m.faces(verts,[tuple(p.vertices) for p in me.polygons],ma)
 bpy.data.objects.remove(obj,do_unlink=True);bpy.data.meshes.remove(me);bpy.data.curves.remove(curve)
def hotel_portal(m,x,y,ang):
 town_door(m,x,y,.24,1.60,2.81,ang,town_mats['PaintBrown'],True)
 # Fanlight and closed profiled stone arch.
 arc=[facade_point(x,y,.8*math.cos(j*math.pi/32),.07,3.05+.8*math.sin(j*math.pi/32),ang) for j in range(33)]
 m.faces(arc,[tuple(range(33))],town_mats['Glass'])
 for r in [.84,1.00,1.08]:town_arch_band(m,x,y,3.05,r,.055,ang,TS,.30)
 for j in [1,2,3]:
  a=j*math.pi/4;town_rod(m,facade_point(x,y,0,.19,3.05,ang),facade_point(x,y,.78*math.cos(a),.19,3.05+.78*math.sin(a),ang),.017,town_mats['PaintBrown'])
 for sign in [-1,1]:
  u=sign*1.12
  for zz,ww,hh,out in [(.35,.45,.3,.30),(1.88,.28,2.75,.24),(3.2,.44,.20,.30)]:facade_box(m,x,y,u,out,zz,ww,.42,hh,TS,ang)
  town_scroll(m,*facade_point(x,y,sign*1.26,0,0,ang)[:2],3.73,ang,sign,.85,.38)
  for du,dz in [(1.25,3.06),(.93,3.55),(1.50,3.82)]:town_leaf(m,*facade_point(x,y,sign*du,.37,0,ang)[:2],dz,ang,sign,.63)
  town_lantern(m,*facade_point(x,y,sign*1.70,0,0,ang)[:2],2.9,ang)
 town_polyprofile(m,x,y,3.83,[(-.26,0),(.26,0),(.31,.35),(0,.51),(-.31,.35)],ang,TS,.28)
 town_band(m,x,y,4.52,3.35,ang,TS,1.1)
 town_text(m,*facade_point(x,y,0,.30,0,ang)[:2],4.29,ang,'CALMAR STADSHOTELL',2.6,IRON)
 facade_box(m,x,y,0,.60,.12,2.6,1.1,.24,TS,ang)
def hotel_tower(m,tx,ty):
 ang=-math.pi/2
 m.box((tx,ty,15.0),(3.6,3.7,7.0),TI)
 for side in range(4):
  a=side*math.pi/2;fx,fy=tx+1.81*math.sin(a),ty-1.86*math.cos(a)
  for zz in [17.8,18.45]:town_band(m,fx,fy,zz,3.85,a,TS,.85)
  for u in [-.43,.43]:town_window(m,*facade_point(fx,fy,u,0,0,a)[:2],17.0,.43,1.05,a,town_mats['PaintBrown'],True,2,1,False)
  outline=[(-1.8,0),(1.8,0),(1.8,.40),(1.15,.48),(.77,.78),(.54,1.42),(.40,1.65),(0,1.78),(-.40,1.65),(-.54,1.42),(-.77,.78),(-1.15,.48),(-1.8,.40)]
  town_polyprofile(m,fx,fy,18.5,outline,a,TI,.32)
  town_window(m,fx,fy,19.05,.40,.83,a,town_mats['PaintBrown'],False,2,1,False)
 town_window(m,tx-1.84,ty,14.3,1.05,1.8,ang,town_mats['PaintBrown'],True)
 town_pediment(m,tx-1.85,ty,15.86,1.65,.56,ang,TI)
 # Windowed copper lantern, gently curved square dome and upper finial.
 m.box((tx,ty,20.25),(2.65,2.65,1.2),TC)
 for side in range(4):
  a=side*math.pi/2;fx,fy=tx+1.33*math.sin(a),ty-1.33*math.cos(a)
  town_window(m,fx,fy,20.28,1.60,.72,a,TC,False,2,3,False)
 for zz in [19.68,20.86]:m.box((tx,ty,zz),(3.03,3.03,.17),TC)
 profile=[(1.72,0),(1.75,.15),(1.69,.28),(1.60,.52),(1.48,.75),(1.25,1.02),(.98,1.23),(.78,1.42),(.64,1.65),(.62,1.91)]
 town_square_loft(m,tx,ty,20.91,profile,TC)
 m.box((tx,ty,23.13),(1.28,1.28,.65),TC)
 for side in range(4):
  a=side*math.pi/2;fx,fy=tx+.65*math.sin(a),ty-.65*math.cos(a)
  town_path(m,[facade_point(fx,fy,.20*math.cos(j*math.tau/32),.025,23.13+.20*math.sin(j*math.tau/32),a) for j in range(33)],.025,TC)
 town_square_loft(m,tx,ty,23.49,[(.77,0),(.79,.12),(.65,.29),(.47,.55),(.38,.75),(.34,.97),(.10,1.12)],TC)
 m.lathe(tx,ty,24.61,[(.10,0),(.20,.08),(.21,.20),(.14,.30),(.055,.35)],TC,24)
 town_rod(m,(tx,ty,24.95),(tx,ty,27.1),.022,IRON)
