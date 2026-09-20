"""Larmtorget facade pass 11. Photo-informed interpretation, metre units.
References: Sinikka Halme 2022; Ross Murteknik renovation photograph.
No photogrammetry or survey-height claim. Only five named meshes are replaced.
"""
larm_names=[]
def lm_new(name):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 larm_names.append(name)
 return Mesh(name,'Storgatan/Landmarks')
def lp(x,y,u=0,o=0,z=0,a=0):return facade_point(x,y,u,o,z,a)
def lm_wall(m,x,y,L,H,holes,ma,a=0):
 # A 35 cm outer masonry layer, with genuine openings over the recessed glazing.
 # holes = (centre, bottom, width, rectangular height, round arch)
 zs=sorted(set([0,H]+[v for u,b,w,h,arc in holes for v in [b,b+h+(w/2 if arc else 0)] if 0<v<H]))
 for low,high in zip(zs,zs[1:]):
  mid=(low+high)/2;cuts=sorted((u-w/2,u+w/2) for u,b,w,h,arc in holes if b<mid<b+h+(w/2 if arc else 0))
  at=-L/2
  for left,right in cuts+[(L/2,L/2)]:
   left=max(-L/2,min(L/2,left));right=max(-L/2,min(L/2,right))
   if left>at+.001:facade_box(m,x,y,(at+left)/2,.18,mid,left-at,.35,high-low,ma,a)
   at=max(at,right)
 for u,b,w,h,arc in holes:
  if not arc:continue
  r=w/2;s=b+h
  for sign in [-1,1]:
   # Closed upper spandrels follow the semicircle rather than a rectangular cutout.
   outline=[(u,s+r),(u+sign*r,s+r),(u+sign*r,s)]
   outline += [(u+sign*r*math.cos(t*math.pi/32),s+r*math.sin(t*math.pi/32)) for t in range(1,16)]
   verts=[lp(x,y,v,o,z,a) for o in [.005,.355] for v,z in outline];n=len(outline)
   m.faces(verts,[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],ma)
def lm_window(m,x,y,b,w,h,a=0,frame=TW,arc=False,trim=TI,tracery=False,rows=2,cols=2):
 town_window(m,x,y,b+h/2,w,h,a,frame,arc,rows,cols,False)
 for u in [-w/2-.08,w/2+.08]:facade_box(m,x,y,u,.39,b+h/2,.14,.15,h+.06,trim,a)
 facade_box(m,x,y,0,.43,b-.09,w+.40,.55,.12,trim,a)
 if arc:
  for r,d in [(w/2+.015,.42),(w/2+.12,.46)]:town_arch_band(m,x,y,b+h,r,.045,a,trim,d)
 else:town_band(m,x,y,b+h+.14,w+.38,a,trim,.55)
 if tracery:
  spring=b+h;r=w/2
  # Two arched lights and a roundel, characteristic of the Frimurarhuset.
  for side in [-1,1]:
   cx,cy,_=lp(x,y,side*r*.48,.13,0,a)
   town_arch_band(m,cx,cy,spring-r*.26,r*.46,.029,a,frame,.08)
   facade_box(m,x,y,side*r*.48,.21,b+h*.53,.035,.06,h*.9,frame,a)
  pts=[lp(x,y,r*.28*math.cos(t*math.tau/40),.22,spring+r*.46+r*.28*math.sin(t*math.tau/40),a) for t in range(41)]
  town_path(m,pts,.026,frame)
def lm_panel(m,x,y,u,z,w,h,a,ma=TI):
 xx,yy,_=lp(x,y,u,.365,0,a);town_border(m,xx,yy,z,w,h,a,ma,.04,.055)
def lm_cornice(m,x,y,L,z,a,ma=TI,dentils=False):
 for zz,depth,hh in [(z-.30,.43,.16),(z-.12,.55,.17),(z+.02,.72,.12),(z+.13,.78,.10)]:facade_box(m,x,y,0,depth/2,zz,L,depth,hh,ma,a)
 if dentils:
  for k in range(round(L/.42)):
   u=-L/2+(k+.5)*L/round(L/.42);facade_box(m,x,y,u,.33,z-.48,.13,.42,.21,ma,a)
def lm_rail(m,x,y,L,z,a,out=1.05,ma=IRON):
 for zz in [z+.12,z+.55,z+.96]:town_rod(m,lp(x,y,-L/2,out,zz,a),lp(x,y,L/2,out,zz,a),.019,ma)
 for k in range(round(L/.65)+1):
  u=-L/2+k*L/round(L/.65);town_rod(m,lp(x,y,u,out,z,a),lp(x,y,u,out,z+1.02,a),.024,ma)
def lm_dormer(m,x,y,z,w,a,roof):
 # Body terminates behind the glass, with a sheet-metal hood matching its roof.
 facade_box(m,x,y,0,-.70,z+.65,w,1.35,1.4,roof,a)
 town_window(m,x,y,z+.65,w*.65,1.04,a,TW,False,2,2,False)
 town_pediment(m,x,y,z+1.36,w+.16,.30,a,roof)
 pts=[lp(x,y,u,o,zz,a) for u,o,zz in [(-w/2-.1,.15,z+1.36),(w/2+.1,.15,z+1.36),(0,.15,z+1.66),(-w/2-.1,-1.4,z+1.36),(w/2+.1,-1.4,z+1.36),(0,-1.4,z+1.66)]]
 m.faces(pts,[(0,2,5,3),(2,1,4,5)],roof)
def lm_front(m,x,y,L,H,holes,ma,a=0):
 # Flat backing terminates behind the recessed glass; avoids the old OSM-wall overlaps.
 facade_box(m,x,y,0,-.22,H/2,L,.43,H,ma,a);lm_wall(m,x,y,L,H,holes,ma,a)

# Theatre: five ground/middle axes and paired upper windows, low side wings.
m=lm_new('SM_Storgatan_Kalmar_Teater');x,y,a=-344.45,17.05,math.pi/2
b=next(q for q in extension['buildings'] if q['id']=='91265009');town_shell(m,b['polygon'],7.7,TW)
m.box((-362.6,y,9.50),(35.3,24.4,5.0),TW)
# Central block body stays behind the architectural front.
holes=[]
for u in [-9,-4.5,0,4.5,9]:
 holes += [(u,.56 if abs(u)<8 else .92,1.90,2.18 if abs(u)<8 else 1.90,True),(u,4.95,1.78,2.10,True)]
for u in [-9.55,-8.05,-5.05,-3.55,-.75,.75,3.55,5.05,8.05,9.55]:holes.append((u,9.40,.86,1.48,True))
lm_front(m,x,y,24.4,12.0,holes,TW,a)
for u,bottom,w,h,arc in holes:
 xx,yy,_=lp(x,y,u,0,0,a)
 if bottom==.56:
  town_door(m,xx,yy,bottom,w,h,a,town_mats['PaintBrown']);lm_window(m,xx,yy,bottom,w,h,a,town_mats['PaintBrown'],True,TW,False,1,2)
  # Door leaves are in front of the glazing, below the fanlight.
  town_door(m,*lp(xx,yy,0,.17,0,a)[:2],bottom,w-.12,h-.07,a,town_mats['PaintBrown'])
 else:lm_window(m,xx,yy,bottom,w,h,a,town_mats['PaintBrown'],arc,TW,False,2,2 if w>1 else 1)
for z in [4.12,8.67,12.08]:lm_cornice(m,x,y,24.8,z,a,TW,z==8.67)
for u in [-11.85,-6.75,-2.25,2.25,6.75,11.85]:
 for z,h in [(2.35,3.5),(6.46,3.85)]:
  facade_box(m,x,y,u,.43,z,.42,.23,h,TW,a)
  for zz in [z-h/2,z+h/2]:facade_box(m,x,y,u,.47,zz,.65,.35,.18,TW,a)
# Rusticated ground-floor piers, clipped to the arched openings.
for i in range(1,10):
 zz=i*.40
 for lo,hi in [(-12.2,-10.2),(-7.8,-5.65),(-3.35,-1.15),(1.15,3.35),(5.65,7.8),(10.2,12.2)]:facade_box(m,x,y,(lo+hi)/2,.361,zz,hi-lo,.025,.018,TI,a)
outline=[(-12.2,0),(12.2,0),(12.2,1.25),(2.75,2.15),(2.75,2.65),(-2.75,2.65),(-2.75,2.15),(-12.2,1.25)]
town_polyprofile(m,*lp(x,y,0,.36,0,a)[:2],12.25,outline,a,TW,.55)
for u in [-7.2,7.2]:lm_panel(m,x,y,u,13.10,8.0,.62,a,TW)
lm_panel(m,x,y,0,13.62,4.35,1.63,a,TW);# Dark circular vent, without the invented cross-shaped sash.
for rr,out,ma in [(.69,.50,TI),(.58,.53,IRON)]:
 m.faces([lp(x,y,rr*math.cos(t*math.tau/48),out,13.68+rr*math.sin(t*math.tau/48),a) for t in range(48)],[tuple(range(48))],ma)
for dz in [-.4,-.2,0,.2,.4]:
 half=math.sqrt(.57**2-dz**2);town_rod(m,lp(x,y,-half,.55,13.68+dz,a),lp(x,y,half,.55,13.68+dz,a),.012,town_mats['PaintBrown'])
# Interpreted gilded lyre ornament, modelled separately from the parapet silhouette.
for sign in [-1,1]:
 pts=[lp(x,y,sign*(.48+.22*math.sin(t*math.pi)),.35,14.94+t*1.05,a) for t in [j/24 for j in range(25)]];town_path(m,pts,.065,GOLD)
 town_scroll(m,*lp(x,y,sign*.52,.34,0,a)[:2],14.97,a,sign,.9,.08,GOLD)
for zz in [14.99,15.99]:town_rod(m,lp(x,y,-.53,.35,zz,a),lp(x,y,.53,.35,zz,a),.05,GOLD)
for u in [-.25,0,.25]:town_rod(m,lp(x,y,u,.35,15.02,a),lp(x,y,u,.35,15.94,a),.012,GOLD)
town_text(m,*lp(x,y,0,.80,0,a)[:2],4.48,a,'KALMAR TEATER',5.0,IRON)
for i in range(4):facade_box(m,x,y,0,.65+i*.35,.07*(4-i),12+i*.35,.70,.14*(4-i),TS,a)
for u in [-6,-2.25,2.25,6]:
 town_path(m,[lp(x,y,u,.50,1.4,a),lp(x,y,u,1.70,.95,a)],.026,IRON)
 for o,zz in [(.5,1.4),(1.7,.95)]:town_rod(m,lp(x,y,u,o,.20,a),lp(x,y,u,o,zz,a),.025,IRON)
# South wing has rectangular main windows, small attic lights and arched ground windows.
wx,wy=-362.9,4.55;L=35.7;hs=[]
for u in [-15,-11.25,-7.5,-3.75,0,3.75,7.5,11.25,15]:hs.extend([(u,.8,1.3,1.65,True),(u,4.05,1.4,2.0,False),(u,6.95,.85,.40,False)])
lm_front(m,wx,wy,L,7.8,hs,TW)
for u,b,w,h,ar in hs:lm_window(m,wx+u,wy,b,w,h,0,town_mats['PaintBrown'],ar,TW,False,2,2)
for z in [3.35,6.55,7.90]:lm_cornice(m,wx,wy,L+.3,z,0,TW)
town_roof(m,-362.5,10,35.5,10,7.9,1.4,town_mats['MetalGrey'],True)
m.finish()

# Frimurarhotellet: arcades, true recessed openings, paired mezzanine lights,
# upper window tracery, facade panels and four-sided corner towers.
m=lm_new('SM_Storgatan_Frimurarehotellet');x,y,a=-345.45,-33.55,math.pi/2
b=next(q for q in extension['buildings'] if q['id']=='91265021');town_shell(m,b['polygon'],13.2,TY)
def frim_face(x,y,L,a,bays):
 spacing=L/bays;holes=[]
 for k in range(bays):
  u=(k+.5)*spacing-L/2
  door=bays==15 and k in [2,7,12]
  holes.extend([(u,.18 if door else .55,1.55,2.47 if door else 2.10,True),(u,8.0,1.60,2.75,True)])
  for off in [-.43,.43]:holes.append((u+off,4.5,.60,1.40,True))
 lm_front(m,x,y,L,13.4,holes,TY,a)
 for u,b,w,h,ar in holes:lm_window(m,*lp(x,y,u,0,0,a)[:2],b,w,h,a,TG,True,TY,b==8.0,1 if b==4.5 else 2,1 if b==4.5 else 2)
 for k in range(bays):
  u=(k+.5)*spacing-L/2;xx,yy,_=lp(x,y,u,0,0,a)
  facade_box(m,x,y,u,.40,5.23,.13,.20,1.63,TI,a)
  for zz in [4.48,5.95]:facade_box(m,x,y,u,.43,zz,.24,.26,.12,TI,a)
  lm_panel(m,x,y,u+spacing/2,5.27,spacing-1.9,1.6,a,TY) if k<bays-1 else None
  for off in [-.55,-.28,0,.28,.55]:lm_panel(m,x,y,u+off,7.70,.19,.27,a,TI)
  for i in range(1,9):
   zz=i*.43
   if k<bays-1:facade_box(m,x,y,u+spacing/2,.361,zz,spacing-1.85,.025,.022,TS,a)
 for z in [3.86,6.68,12.75,13.40]:lm_cornice(m,x,y,L+.2,z,a,TY,z==12.75)
 # Corbel arcade below the main cornice; connected stems make it read as masonry.
 for k in range(round(L/.40)):
  u=-L/2+(k+.5)*L/round(L/.40);xx,yy,_=lp(x,y,u,.27,0,a)
  town_arch_band(m,xx,yy,12.13,.145,.065,a,TY,.17)
  facade_box(m,x,y,u-.18,.40,12.0,.07,.18,.27,TY,a)
 facade_box(m,x,y,0,.02,13.79,L,.46,.72,TY,a)
 for k in range(round(L/.62)):
  u=-L/2+(k+.5)*L/round(L/.62);lm_panel(m,x,y,u,13.77,.45,.48,a,TY)
 town_band(m,x,y,14.18,L+.12,a,TY,.85)
frim_face(x,y,52.6,a,15)
frim_face(-359.0,-6.85,27.0,math.pi,8)
# Three front entrances; broken low plinths keep thresholds unobstructed.
for u in [-17.533,0,17.533]:
 xx,yy,_=lp(x,y,u,.17,0,a);town_door(m,xx,yy,.18,1.55,2.45,a,TG,True);facade_box(m,x,y,u,.60,.09,2.0,1.1,.18,TS,a)
 for sign in [-1,1]:
  facade_box(m,x,y,u+sign*1.06,.53,1.95,.24,.38,3.55,TI,a)
  town_scroll(m,*lp(x,y,u+sign*1.03,.43,0,a)[:2],3.63,a,sign,.60,.08,TI)
 town_band(m,*lp(x,y,u,0,0,a)[:2],3.73,2.65,a,TI)
for cy in [-9.75,-56.5]:
 cx=-348.0;m.box((cx,cy,15.55),(5.5,5.5,5.1),TY)
 for a2 in [0,math.pi/2,math.pi,math.pi*1.5]:
  fx,fy,_=lp(cx,cy,0,2.77,0,a2);hs=[(u,14.95,1.03,2.15,True) for u in [-1.55,0,1.55]]
  facade_box(m,fx,fy,0,-.22,16.4,5.55,.43,3.7,TY,a2)
  lm_wall(m,fx,fy,5.55,18.25,[(0,0,5.55,14.55,False)]+hs,TY,a2)
  for u,b,w,h,ar in hs:lm_window(m,*lp(fx,fy,u,0,0,a2)[:2],b,w,h,a2,TG,True,TY,False,1,1)
  for u in [-2.48,2.48]:facade_box(m,fx,fy,u,.43,16.17,.30,.22,3.70,TY,a2)
  for z in [14.55,18.13]:lm_cornice(m,fx,fy,5.85,z,a2,TY)
  facade_box(m,fx,fy,0,.05,18.59,5.65,.40,.70,TY,a2)
  for u in [-1.95,-1.3,-.65,0,.65,1.3,1.95]:lm_panel(m,fx,fy,u,18.57,.47,.47,a2,TY)
  town_band(m,fx,fy,19.01,5.95,a2,TY)
 for dx in [-2.8,2.8]:
  for dy in [-2.8,2.8]:
   m.box((cx+dx,cy+dy,18.65),(.58,.58,1.30),TY);m.box((cx+dx,cy+dy,19.33),(.76,.76,.16),TI)
   m.lathe(cx+dx,cy+dy,19.41,[(.13,0),(.17,.14),(.10,.28),(.045,.45),(.006,.69)],IRON,16)
town_roof(m,-359.0,-33.55,25.5,52,13.40,2.25,town_mats['MetalGrey'],True,axis='y')
for u in [-17.5,-10.5,10.5,17.5]:
 xx,yy,_=lp(x,y,u,-2.3,0,a);lm_dormer(m,xx,yy,14.2,1.65,a,town_mats['MetalGrey'])
outline=[(-3.2,0),(3.2,0),(3.2,.6),(2.1,.6),(2.1,1.25),(1.1,1.25),(1.1,1.9),(.4,1.9),(.4,2.45),(-.4,2.45),(-.4,1.9),(-1.1,1.9),(-1.1,1.25),(-2.1,1.25),(-2.1,.6),(-3.2,.6)]
town_polyprofile(m,*lp(x,y,0,.5,0,a)[:2],14.1,outline,a,TY,.6);roundwindow(m,*lp(x,y,0,.65,0,a)[:2],15.10,.59,a,True)
m.finish()

# North-west frontage: Kalmarhem functionalism and the white arched palazzo
# share a mapped OSM footprint, but are not the same architectural facade.
m=lm_new('SM_Building_91846938');b=next(q for q in extension['buildings'] if q['id']=='91846938');town_shell(m,b['polygon'],7.4,TI)
x,y=-330.3,27.85;L=13.6
m.box((x,35,5.325),(13.6,14.0,10.65),TI)
holes=[(u,b,2.1,2.0,False) for u in [-4.8,-1.6,1.6,4.8] for b in [4.1,7.45]]
holes += [(u,.25,2.65,3.0,False) for u in [-4.8,-1.6,1.6,4.8]]
lm_front(m,x,y,L,10.65,holes,TI)
for u,b,w,h,ar in holes:lm_window(m,x+u,y,b,w,h,0,TG,False,TI,False,1,2)
# Set-back roof storey and thin wraparound balconies.
m.box((x+1,35.7,11.48),(11.6,12.2,2.1),TI)
for u in [-3.9,-.6,2.7,5.0]:town_window(m,x+u,y+1.6,11.65,1.8,1.5,0,TG,False,1,2,False)
for z in [3.65,7.05]:
 facade_box(m,x,y,0,1.0,z,L+1.0,2.4,.17,TS,0);lm_rail(m,x,y,L+.6,z+.1,0,2.13,TG)
 facade_box(m,x-L/2,y+4,0,.90,z,8.0,2.2,.17,TS,-math.pi/2);lm_rail(m,x-L/2,y+4,8,z+.1,-math.pi/2,1.9,TG)
for z in [10.65,12.6]:facade_box(m,x+(.8 if z>11 else 0),y+(1.5 if z>11 else 0),0,.1,z,L-(1.6 if z>11 else 0),.7,.18,TC,0)
# Palazzo next door: three storeys, upper double arches, central triple lights.
x,y=-316.69,27.84;L=13.65;hs=[]
for u in [-5,-1.7,1.7,5]:
 hs += [(u,.35,2.25,2.9,False),(u,4.5,1.45,2.2,False)]
 for off in [-.36,.36]:hs.append((u+off,8.20,.58,1.23,True))
lm_front(m,x,y,L,10.45,hs,TW)
m.box((x,32.8,8.75),(L,10,3.5),TW)
# Backing above was placed inward; ensure its front is behind all glass.
for u,b,w,h,ar in hs:lm_window(m,x+u,y,b,w,h,0,TW,ar,TW,False,2,1 if ar else 2)
for u in [-6.6,-.2,6.6]:facade_box(m,x,y,u,.44,7.4,.30,.20,6.0,TW,0)
for z in [3.8,7.37,10.50]:lm_cornice(m,x,y,L+.15,z,0,TW)
for k in range(29):town_arch_band(m,x-L/2+.25+k*.47,y+.0,10.03,.17,.055,0,TW,.46)
town_roof(m,x,32.9,L,10,10.60,.65,TC,True)
m.box((x,34.4,11.7),(4.1,3.0,1.9),TW);town_band(m,x,32.87,12.65,4.4,0,TC)
for u in [-1.35,-.45,.45,1.35]:
 town_arch_band(m,x+u,32.84,12.02,.27,.05,0,TW,.1)
 for off in [-.3,.3]:facade_box(m,x+u,32.84,off,.08,11.70,.045,.12,.65,TW,0)
for u in [-5,-1.7,1.7,5]:ext_awning(m,x+u,y,3.1,3.55,0,AWNING)
m.finish()

# Low white eastern part of the northern row (Krögers).
m=lm_new('SM_Building_91846980');b=next(q for q in extension['buildings'] if q['id']=='91846980');town_shell(m,b['polygon'],7.45,TW)
x,y=-302.73,27.78;L=14.25;hs=[]
for u in [-5.45,-1.8,1.8,5.45]:hs.extend([(u,.35,2.75,2.9,False),(u,4.45,1.60,2.05,False)])
lm_front(m,x,y,L,7.50,hs,TW)
for u,b,w,h,ar in hs:lm_window(m,x+u,y,b,w,h,0,TW,False,TW,False,2,2)
for z in [3.72,7.50]:lm_cornice(m,x,y,L+.15,z,0,TW)
town_roof(m,x,34.8,L,13.9,7.65,3.0,TT)
for u in [-5.35,-1.78,1.78,5.35]:ext_awning(m,x+u,y,3.5,3.55,0,AWNING)
# Visible east return toward Larmgatan.
for yy in [31,34.6,38.2]:town_cross_window(m,-295.47,yy,5.55,1.4,2.05,math.pi/2,TW)
town_band(m,-295.45,35.2,7.45,14.2,math.pi/2,TW)
m.finish()

# Ludvigshuset: white Jugend frontage, curved centre gable and oxidised copper roof.
m=lm_new('SM_Building_91264999');b=next(q for q in extension['buildings'] if q['id']=='91264999');town_shell(m,b['polygon'],13.5,TW)
def ludvig_face(x,y,L,a,bays):
 hs=[];step=L/bays
 for k in range(bays):
  u=(k+.5)*step-L/2;hs += [(u,.38,1.80,2.50,True),(u,5.00,1.45,2.35,False),(u,9.30,1.40,2.25,False)]
 lm_front(m,x,y,L,13.5,hs,TW,a)
 for u,b,w,h,ar in hs:lm_window(m,*lp(x,y,u,0,0,a)[:2],b,w,h,a,town_mats['PaintBrown'],ar,TW,False,1 if ar else 3,2)
 for k in range(bays):
  u=(k+.5)*step-L/2
  # Under-window plaster aprons with gently sloping sides, not classical pediments.
  for z in [4.55,8.87]:
   xx,yy,_=lp(x,y,u,.39,0,a);town_polyprofile(m,xx,yy,z,[(-.84,0),(.84,0),(.67,.34),(-.67,.34)],a,TW,.08,False)
  facade_box(m,x,y,u,.43,12.88,.22,.40,.47,TW,a)
 for z in [3.85,13.50]:lm_cornice(m,x,y,L+.2,z,a,TW)
 for u in [-L/2+.18,L/2-.18]:town_drain(m,*lp(x,y,u,.45,0,a)[:2],13.6,a)
 return step
ludvig_face(-316.2,-29.80,39.55,math.pi,11)
ludvig_face(-336.48,-48.40,37.0,-math.pi/2,10)
ludvig_face(-296.07,-48.65,36.5,math.pi/2,10)
town_roof(m,-316.25,-48.4,39.5,37.0,13.6,4.25,TC,True)
# Raised flowing central gable facing the square.
x,y,a=-316.2,-29.80,math.pi
outline=[(-4.6,0),(4.6,0),(4.35,.8),(3.9,.85),(3.45,.48),(2.95,.5),(2.55,.95),(2.12,1.63),(1.55,2.10),(.8,2.40),(0,2.5),(-.8,2.40),(-1.55,2.1),(-2.12,1.63),(-2.55,.95),(-2.95,.5),(-3.45,.48),(-3.9,.85),(-4.35,.8)]
town_polyprofile(m,*lp(x,y,0,.45,0,a)[:2],13.6,outline,a,TW,.65,False)
town_path(m,[lp(x,y,u,.52,13.6+z,a) for u,z in outline[2:]+[outline[0]]],.09,TC)
town_window(m,*lp(x,y,0,.51,0,a)[:2],14.8,.66,1.05,a,town_mats['PaintBrown'],False,2,1,False)
for u in [-3.85,3.85]:town_scroll(m,*lp(x,y,u,.55,0,a)[:2],14.30,a,1,.65,.03,TS)
for u in [-15.7,-12.6,-9.5,9.5,12.6,15.7]:
 xx,yy,_=lp(x,y,u,-2.1,0,a);lm_dormer(m,xx,yy,14.0,1.65,a,TC)
# Corner roof turrets have brown sheet-metal hoods rather than generic chimneys.
for xx in [-333.7,-298.7]:
 cy=-32.4;m.cylinder(xx,cy,13.6,2.10,1.4,town_mats['MetalGrey'],32)
 for aa in [0,math.pi/2,math.pi,math.pi*1.5]:town_window(m,*lp(xx,cy,0,2.12,0,aa)[:2],14.30,.85,.65,aa,TW,False,1,1,False)
 m.lathe(xx,cy,14.95,[(2.18,0),(2.15,.23),(1.83,.42),(1.64,.65),(1.59,.88),(1.25,1.15),(.84,1.45),(.75,1.65),(.20,1.85)],town_mats['MetalGrey'],40)
for u in [-14,-7,7,14]:ext_awning(m,*lp(x,y,u,0,0,a)[:2],6.7,3.65,a,AWNING)
m.finish()

larm_cameras=[
 ('41_Larmtorget_Norra',(-311,-6,2.0),(-320,28,6.0),27),
 ('42_Larmtorget_Ludvig',(-308,19,2.1),(-317,-31,7.5),30),
 ('43_Larmtorget_Frimurare_Detalj',(-325,-3,2.0),(-348,-13,10.5),31),
 ('45_Larmtorget_Ludvig_Tak',(-282,7,20),(-317,-44,8),33),
 ('44_Larmtorget_Teater_Fasad',(-312,15,2.0),(-345,17,7.3),26),
]

# Explicit, stable triangulation also permits exporting verified Mikk tangents.
for name in larm_names:
 me=bpy.data.objects[name].data
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.triangulate(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();me.update()
