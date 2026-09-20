"""Storgatan–Larmtorget extension. Footprints measured by OSM; heights/details estimated.
Executed with the canonical Mesh and facade helpers in scope; no church edits.
"""
extension=json.loads((R/'source/storgatan.json').read_text())
extension_names=[];extension_cameras=[]
PAVESTREET='M_Storgatan_Setts';PAVESLAB='M_Storgatan_Slabs'
if PAVESTREET not in materials:mat(PAVESTREET,(.35,.33,.28),.80,0,'StreetSetts')
if PAVESLAB not in materials:mat(PAVESLAB,(.38,.36,.31),.80,0,'StreetSlabs')
def ext_new(name,category='Storgatan/Buildings'):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 extension_names.append(name);return Mesh(name,category)
def ellipsoid(m,c,scale,ma,n=12,rings=7):
 # Closed rings avoid degenerate pole triangles.
 vs=[(c[0],c[1],c[2]-scale[2])]
 for j in range(1,rings):
  t=-math.pi/2+j*math.pi/rings
  for i in range(n):
   a=i*math.tau/n;vs.append((c[0]+scale[0]*math.cos(t)*math.cos(a),c[1]+scale[1]*math.cos(t)*math.sin(a),c[2]+scale[2]*math.sin(t)))
 top=len(vs);vs.append((c[0],c[1],c[2]+scale[2]))
 faces=[(0,1+(i+1)%n,1+i) for i in range(n)]
 for j in range(rings-2):
  faces.extend((1+j*n+i,1+j*n+(i+1)%n,1+(j+1)*n+(i+1)%n,1+(j+1)*n+i) for i in range(n))
 faces.extend((1+(rings-2)*n+i,1+(rings-2)*n+(i+1)%n,top) for i in range(n))
 m.faces(vs,faces,ma,True)
def ext_shop(m,x,y,width,ang,frame,door=False,arched=False):
 h=2.55;z=1.68
 town_window(m,x,y,z,width,h,ang,frame,arched,rows=1,cols=1,trim=False)
 # Deeper stone piers, top lights and raised commercial glazing frames.
 for u in [-width/2-.12,width/2+.12]:facade_box(m,x,y,u,.10,1.92,.20,.30,3.55,TS,ang)
 facade_box(m,x,y,0,.245,2.68,width,.085,.065,frame,ang)
 if door:
  facade_box(m,x,y,0,.16,1.30,.85,.13,2.45,frame,ang)
  facade_box(m,x,y,0,.235,1.47,.70,.03,2.00,town_mats['Glass'],ang)
  town_path(m,[facade_point(x,y,.26,.29,1.10,ang),facade_point(x,y,.26,.39,1.10,ang),facade_point(x,y,.26,.39,1.52,ang),facade_point(x,y,.26,.29,1.52,ang)],.015,IRON)
  facade_box(m,x,y,0,.30,.10,.96,.70,.16,TS,ang)
def ext_awning(m,x,y,w,z,ang,ma=AWNING):
 p=[(-w/2,.2,z),(w/2,.2,z),(w/2,1.12,z-.38),(-w/2,1.12,z-.38)]
 m.faces([facade_point(x,y,u,o,h,ang) for u,o,h in p],[(0,1,2,3)],ma)
 facade_box(m,x,y,0,1.12,z-.46,w,.045,.16,ma,ang)
 for u in [-w/2+.1,w/2-.1]:town_rod(m,facade_point(x,y,u,.18,z-.5,ang),facade_point(x,y,u,1.1,z-.4,ang),.018,IRON)
def ext_dormer(m,x,y,z,w,ang,roof):
 facade_box(m,x,y,0,-.5,z+.65,w,1.35,1.4,TI,ang)
 town_window(m,x,y,z+.65,w*.65,1.04,ang,TW,False,2,2,False)
 town_pediment(m,x,y,z+1.36,w+.16,.45,ang,TI)
 pts=[facade_point(x,y,u,o,zz,ang) for u,o,zz in [(-w/2-.1,.15,z+1.36),(w/2+.1,.15,z+1.36),(0,.15,z+1.81),(-w/2-.1,-1.25,z+1.36),(w/2+.1,-1.25,z+1.36),(0,-1.25,z+1.81)]]
 m.faces(pts,[(0,2,5,3),(2,1,4,5)],roof)
# Per-building profile, informed by the June 2020 street panoramas and 2022 square views.
# (eaves, storeys, facade material, window paint, roof, front bays, character)
profiles={
 '91970290':(10.7,3,'Rose','PaintBlue','TileRed',7,'modern'),
 '91970296':(10.2,3,'Lime','PaintWhite','TileRed',6,'modern'),
 '91970373':(9.0,2,'Ivory','PaintBrown','MetalGrey',4,'modern'),
 '91265011':(8.2,2,'Ivory','PaintBrown','MetalGrey',14,'modern'),
 '92379255':(10.2,3,'Yellow','PaintWhite','TileRed',12,'classic'),
 '92379254':(7.2,2,'Yellow','PaintWhite','TileRed',3,'classic'),
 '92379269':(7.4,2,'Ivory','PaintGreen','TileRed',3,'classic'),
 '92379288':(8.0,2,'Lime','PaintWhite','TileRed',3,'classic'),
 '92379312':(9.5,3,'Ivory','PaintWhite','TileRed',3,'ornate'),
 '92379304':(7.8,2,'Rose','PaintBrown','TileDark',2,'classic'),
 '92379278':(7.6,2,'Yellow','PaintWhite','TileRed',5,'classic'),
 '92379295':(13.3,3,'Yellow','PaintWhite','TileRed',7,'bank'),
 '92204203':(7.9,2,'Yellow','PaintWhite','TileRed',8,'modern'),
 '92204159':(9.3,2,'Ivory','PaintGreen','MetalGrey',6,'modern'),
 '92204163':(10.8,3,'Ivory','PaintWhite','MetalGrey',5,'modern'),
 '92204155':(7.0,2,'Rose','PaintWhite','TileRed',5,'corner'),
 '92204197':(7.7,2,'Yellow','PaintWhite','TileRed',4,'classic'),
 '92204194':(7.4,2,'Ivory','PaintGreen','TileRed',4,'ornate'),
 '92204175':(8.0,2,'Ivory','PaintBrown','TileDark',7,'ornate'),
 '92204166':(7.2,2,'Yellow','PaintBrown','TileRed',3,'classic'),
 '92204199':(8.2,2,'Yellow','PaintBrown','TileRed',7,'corner'),
 '91846938':(8.8,2,'Ivory','PaintGreen','TileRed',8,'classic'),
 '91846980':(8.2,2,'Yellow','PaintBrown','TileRed',4,'classic'),
 '91264999':(12.4,3,'Yellow','PaintBrown','MetalGrey',10,'ornate'),
}
def ext_front(m,x,y,length,z,floors,bays,ang,frame,kind,roof):
 spacing=length/bays
 for k in range(bays):
  u=(k+.5)*spacing-length/2;xx,yy,_=facade_point(x,y,u,0,0,ang)
  ext_shop(m,xx,yy,min(spacing*.80,3.35),ang,frame,door=k in {1,bays//2},arched=kind=='bank')
  for f in range(1,floors):
   zz=4.9+(f-1)*(z-4.4)/max(1,floors-1)
   hh=min(2.05,(z-4.4)/max(1,floors-1)-.5)
   if kind=='modern':town_window(m,xx,yy,zz,min(1.6,spacing*.59),hh,ang,frame,False,1,2)
   else:town_window(m,xx,yy,zz,min(1.35,spacing*.52),hh,ang,frame,False,3,2)
   if kind in ['ornate','bank'] and f==1:town_pediment(m,xx,yy,zz+hh/2+.2,1.75,.35,ang,TW)
  if kind in ['classic','corner','ornate'] and k%3==1:ext_awning(m,xx,yy,spacing*.90,3.15,ang)
 town_band(m,x,y,3.85,length,ang,TW,.75);town_band(m,x,y,z-.10,length+.12,ang,TW,.85)
 # Window frames rise cleanly from the low plinth; no band crosses the doors.
 for end in [-length/2+.30,length/2-.30]:
  facade_box(m,x,y,end,.09,(z+3.9)/2,.25,.22,z-3.9,TW,ang)
 for u in [-length/2+.22,length/2-.22]:town_drain(m,*facade_point(x,y,u,.12,0,ang)[:2],z,ang)
 if kind!='modern' and length>10:
  for u in [-length*.27,length*.27]:
   xx,yy,_=facade_point(x,y,u,-1.65,0,ang);ext_dormer(m,xx,yy,z+.7,1.3,ang,roof)
 if kind=='bank':
  town_pediment(m,x,y,z,7.4,3.2,ang,TY)
  for u in [-length/2+.50,length/2-.50]:
   xx,yy,_=facade_point(x,y,u,0,0,ang);town_pediment(m,xx,yy,z,2.8,2.2,ang,TY)
for b in extension['buildings']:
 bid=b['id'];p=b['polygon'];x0,x1,y0,y1=b['bounds'];cx,cy=(x0+x1)/2,(y0+y1)/2
 if bid in ['91265009','91265021']:continue
 name='SM_Building_'+bid
 z,floors,key,paint,roofkey,bays,kind=profiles.get(bid,(7.1,2,'Ivory','PaintWhite','TileRed',4,'classic'))
 ma=town_mats[key];frame=town_mats[paint];roof=town_mats[roofkey]
 m=ext_new(name);town_shell(m,p,z,ma)
 # A shallow rear roof follows the footprint, with a separate street-facing ridge.
 m.prism(p,z,z+.14,roof)
 area=sum(p[i][0]*p[(i+1)%len(p)][1]-p[(i+1)%len(p)][0]*p[i][1] for i in range(len(p)))
 fronts=[]
 for i,(ax,ay) in enumerate(p):
  bx,by=p[(i+1)%len(p)];dx,dy=bx-ax,by-ay;ln=math.hypot(dx,dy)
  if ln<4:continue
  xx,yy=(ax+bx)/2,(ay+by)/2;ang=math.atan2(dy,dx)+(0 if area>0 else math.pi)
  street=b['role']=='street' and abs(dy)<1.0 and -12<yy<6
  square=b['role']=='square' and ((abs(dy)<1 and (abs(yy-28)<2 or abs(yy+30)<2)) or (abs(dx)<1 and xx> -298))
  corner=bid in ['92204155','92204199'] and abs(dx)<1 and xx< -284
  if street or square or corner:
   n=max(2,round(bays*ln/max(x1-x0,1))) if abs(dx)>abs(dy) else max(3,round(ln/3.1))
   ext_front(m,xx,yy,ln,z,floors,n,ang,frame,kind,roof);fronts.append((xx,yy,ln,ang))
  elif abs(dy)<1 and (abs(yy-y0)<.5 or abs(yy-y1)<.5):
   for f in range(floors):
    for k in range(max(1,round(ln/3.2))):
     t=(k+.5)/max(1,round(ln/3.2));town_window(m,ax+t*dx,ay+t*dy,2+f*3.1,1.1,1.65,ang,frame,False,2,2)
 if fronts:
  xx,yy,ln,ang=max(fronts,key=lambda f:f[2]);depth=min(12,y1-y0) if abs(math.cos(ang))>.7 else min(12,x1-x0)
  rx,ry,_=facade_point(xx,yy,0,-depth/2,0,ang)
  if kind=='modern':
   town_roof(m,rx,ry,ln,depth,z,1.3,roof,True,hipped=True)
   if bid=='91970290':town_pediment(m,xx,yy,z,8,2.4,ang,ma)
  else:town_roof(m,rx,ry,ln,depth,z,min(4.4,depth*.35),roof,'Metal' in roofkey,hipped=kind=='corner')
 obj=m.finish()
 # Keep mapped courtyards open instead of filling the inner multipolygon rings.
 for j,hole in enumerate(b.get('holes',[])):
  cutter=Mesh('Temporary_courtyard','Temporary');cutter.prism(hole,-1,z+10,TS);cut=cutter.finish()
  mod=obj.modifiers.new('Mapped courtyard','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cut
  bpy.context.view_layer.objects.active=obj;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cut,do_unlink=True)
# Kalmar theatre: low side wings, central three-level frontage and raised parapet.
b=next(b for b in extension['buildings'] if b['id']=='91265009');p=b['polygon'];m=ext_new('SM_Storgatan_Kalmar_Teater','Storgatan/Landmarks');town_shell(m,p,8.4,TW);m.prism(p,8.4,8.58,town_mats['MetalGrey'])
tx,ty=-344.50,17.05;ang=math.pi/2
m.box((-344.90,ty,6.20),(.90,24.4,12.4),TW)
m.box((-361,ty,10.3),(31.7,23.4,4.5),TW)
for zz in [.62,3.55,8.15,11.7,12.35]:town_band(m,tx,ty,zz,24.4,ang,TW,.85)
for k in range(7):
 u=(k-3)*3.0;xx,yy,_=facade_point(tx,ty,u,0,0,ang)
 if k in [2,3,4]:
  town_door(m,xx,yy,.56,1.25,2.55,ang,town_mats['PaintBrown']);town_arch_band(m,xx,yy,3.11,.67,.14,ang,TW,.32)
 else:town_window(m,xx,yy,1.94,1.30,2.15,ang,town_mats['PaintBrown'],True,2,2)
 town_window(m,xx,yy,5.56,1.18,2.16,ang,town_mats['PaintBrown'],True,2,2)
 town_window(m,xx,yy,9.66,.86,1.36,ang,town_mats['PaintBrown'],True,1,1)
 for zz in [3.62,7.6]:facade_box(m,tx,ty,u,.18,zz,.22,.40,.40,TW,ang)
for u in [-11.5,11.5]:facade_box(m,tx,ty,u,.14,6.6,.45,.5,11.8,TW,ang)
town_polyprofile(m,tx,ty,12.4,[(-12,0),(12,0),(12,.65),(2.8,1.9),(2.8,2.4),(-2.8,2.4),(-2.8,1.9),(-12,.65)],ang,TW,.50)
roundwindow(m,tx+.14,ty,13.74,.61,ang)
town_text(m,tx+.45,ty,3.78,ang,'KALMAR TEATER',5.5,IRON)
for i in range(4):facade_box(m,tx,ty,0,.45+i*.35,.07*(4-i),10+i*.45,.70,.14*(4-i),TS,ang)
for side in [-1,1]:
 town_path(m,[facade_point(tx,ty,side*3.3,1.45,.85,ang),facade_point(tx,ty,side*3.3,.35,1.18,ang)],.026,IRON)
for yy in [7,27]:town_rod(m,(tx-.8,yy,13.4),(tx-.8,yy,17),.032,IRON)
# Windowed southern side elevation.
for xx in [-350,-354,-358,-362,-366,-370,-374,-378]:
 for zz in [2.0,5.55]:town_window(m,xx,4.6,zz,1.2,1.8,0,town_mats['PaintBrown'],zz==2,2,2)
town_band(m,-363.5,4.6,8.3,36,0,TW)
m.finish()
# Frimurarehotellet: ochre facade, arcaded windows, two raised corner towers.
b=next(b for b in extension['buildings'] if b['id']=='91265021');p=b['polygon'];m=ext_new('SM_Storgatan_Frimurarehotellet','Storgatan/Landmarks');town_shell(m,p,13.4,TY);m.prism(p,13.4,13.55,town_mats['TileDark'])
fx,fy=-345.50,-33.55;ang=math.pi/2
m.box((-345.90,fy,6.7),(.90,52.6,13.4),TY)
for zz in [3.95,7.0,12.75,13.35]:town_band(m,fx,fy,zz,52.6,ang,TI,.85)
for low,high in [(-26.3,-18),(-16,-1),(1,16),(18,26.3)]:
 xx,yy,_=facade_point(fx,fy,(low+high)/2,0,0,ang);town_band(m,xx,yy,.75,high-low,ang,TI,.85)
for k in range(15):
 u=(k-7)*3.4;xx,yy,_=facade_point(fx,fy,u,0,0,ang)
 town_window(m,xx,yy,2.00,1.45,2.1,ang,town_mats['PaintGreen'],True,2,2)
 town_window(m,xx,yy,9.55,1.45,2.9,ang,town_mats['PaintGreen'],True,2,2)
 for pair in [-.40,.40]:town_window(m,*facade_point(xx,yy,pair,0,0,ang)[:2],5.25,.52,1.45,ang,town_mats['PaintGreen'],True,1,1)
 facade_box(m,xx,yy,0,.2,5.25,.11,.15,1.75,TI,ang)
 if k in [2,7,12]:
  town_door(m,xx,yy,.18,1.6,2.8,ang,town_mats['PaintBrown'])
  facade_box(m,xx,yy,0,.49,.09,2.15,.95,.18,TS,ang)
for yy in [-10.3,-56.6]:
 m.box((-348.2,yy,15.4),(5.4,5.3,5.5),TY)
 town_band(m,fx+.25,yy,18.05,5.7,ang,TI)
 for u in [-2.65,2.65]:
  xx,y,_=facade_point(fx+.25,yy,u,0,0,ang);m.box((xx,y,18.2),(.65,.65,1.55),TI);m.lathe(xx,y,19,[(.23,0),(.18,.16),(.04,.62)],IRON,12)
 for u in [-1.6,0,1.6]:town_window(m,*facade_point(fx+.30,yy,u,0,0,ang)[:2],16.1,.94,2.35,ang,town_mats['PaintGreen'],True,1,1)
town_roof(m,-356,-33.5,19,51,13.4,1.35,town_mats['TileDark'],axis='y')
for xx in [-350,-354,-358,-362,-366]:
 for zz,hh in [(2,2.1),(5.25,1.45),(9.55,2.9)]:town_window(m,xx,-7.1,zz,1.25,hh,math.pi,town_mats['PaintGreen'],True,2,2)
for k in range(98):
 xx,yy,_=facade_point(fx,fy,-25.9+k*.535,.16,0,ang);town_arch_band(m,xx,yy,12.25,.15,.035,ang,TI,.16)
town_polyprofile(m,fx,fy,13.4,[(-2.7,0),(2.7,0),(2.7,.7),(1.7,.7),(1.7,1.4),(.55,1.4),(.55,2),(-.55,2),(-.55,1.4),(-1.7,1.4),(-1.7,.7),(-2.7,.7)],ang,TY,.4)
roundwindow(m,fx+.18,fy,14.27,.52,ang,True)
m.finish()
exec(compile((R/'scripts/build_larmtorget_facades.py').read_text(),str(R/'scripts/build_larmtorget_facades.py'),'exec'))
exec(compile((R/'scripts/build_street16.py').read_text(),str(R/'scripts/build_street16.py'),'exec'))

# Join the old square to the new corridor, removing the old placeholder strip beneath it.
m=ext_new('SM_Streets','Ground')
for x in [-33,53]:m.box((x,10,-.072),(10,245,.16),GRANITE)
for y in [-4,68,-75]:m.box(((48.5 if y==-4 else 0),y,-.071),((173 if y==-4 else 270),9,.16),GRANITE)
for x in [-38,58]:
 if x==-38:
  for lo,hi in [(-54.5,-10),(5,70.5)]:m.box((x,(lo+hi)/2,.01),(1.2,hi-lo,.22),PATH)
 else:m.box((x,8,.01),(1.2,125,.22),PATH)
for y in [-32,73]:m.box((7,y,.01),(91,1.2,.22),PATH)
m.finish()
m=ext_new('SM_Storgatan_Ground','Storgatan/Ground');m.box((-267.5,-2,-.38),(245,180,.6),GROUND);m.finish()
m=ext_new('SM_Storgatan_Paving','Storgatan/Ground')
route=next(w['points'] for w in extension['roads'] if w['id']=='35772928')
for (ax,ay),(bx,by) in zip(route,route[1:]):
 ln=math.hypot(bx-ax,by-ay);an=math.atan2(by-ay,bx-ax);cx,cy=(ax+bx)/2,(ay+by)/2
 m.box((cx,cy,-.054),(ln+.035,11.55,.13),PAVESTREET,an)
 for off in [-4.52,4.52]:m.box((cx-off*math.sin(an),cy+off*math.cos(an),.018),(ln+.035,2.0,.085),PAVESLAB,an)
 for off in [-3.43,3.43]:m.box((cx-off*math.sin(an),cy+off*math.cos(an),.014),(ln+.035,.17,.062),PATH,an)
 for off in [-3.2,3.2]:m.box((cx-off*math.sin(an),cy+off*math.cos(an),.015),(ln+.035,.09,.06),IRON,an)
for x in [-186.5,-290.4]:m.box((x,-3,-.059),(11.2,137,.13),PAVESTREET)
square=next(w['points'] for w in extension['roads'] if w['id']=='35772926')
m.prism(square[:-1],-.08,.007,PAVESTREET)
for y in [-1,-25,22]:m.box((-317,y,.013),(49,.55,.06),PATH)
for x in [-299,-335]:m.box((x,-1,.013),(.55,52,.06),PATH)
m.finish()
# Planters, pruned street trees and benches. Keep a generous continuous walking lane.
m=ext_new('SM_Storgatan_Furniture','Storgatan/Props');leaves=ext_new('SM_Storgatan_Trees','Storgatan/Vegetation')
for index,x in enumerate([-77,-99,-122,-148,-173,-203,-225,-251,-273]):
 y=.05
 m.box((x,y,.57),(1.05,1.05,1.10),town_mats['MetalGrey']);m.box((x,y,1.12),(.96,.96,.06),BASE)
 m.cylinder(x,y,1.08,.085,2.9,WOOD,12)
 rng=random.Random(800+index)
 for j in range(900):
  theta=rng.random()*math.tau;zz=rng.uniform(-1,1);rr=math.sqrt(1-zz*zz)*rng.uniform(.5,1)
  pos=(x+rr*math.cos(theta),y+rr*math.sin(theta),3.43+zz*.87)
  start=len(leaves.v);size=rng.uniform(.09,.16)
  ellipsoid(leaves,pos,(size,size*.60,.028),LEAF,6,4)
  a,b=rng.uniform(0,math.tau),rng.uniform(-1.2,1.2)
  for vi in range(start,len(leaves.v)):
   px,py,pz=leaves.v[vi];px-=pos[0];py-=pos[1];pz-=pos[2]
   xx,zz=px*math.cos(b)+pz*math.sin(b),-px*math.sin(b)+pz*math.cos(b)
   leaves.v[vi]=(pos[0]+xx*math.cos(a)-py*math.sin(a),pos[1]+xx*math.sin(a)+py*math.cos(a),pos[2]+zz)
 for u in [-1.8,1.8]:
  m.box((x+u,y,.30),(.09,.63,.60),IRON)
 for q in range(5):m.box((x,y-.24+q*.115,.55),(3.85,.085,.07),WOOD)
 for q in range(3):m.box((x,y+.34,.82+q*.14),(3.85,.07,.10),WOOD)
 for u in [-1.84,1.84]:town_rod(m,(x+u,y+.34,.3),(x+u,y+.34,1.18),.025,IRON)
for x in [-55,-110,-166,-210,-267]:
 y=-7.1
 m.cylinder(x,y,0,.065,3.95,IRON,12);town_path(m,[(x,y,3.7),(x,y+.75,4.15),(x,y+1.7,4.10)],.04,IRON)
 m.box((x,y+1.65,4.07),(.50,.40,.10),town_mats['MetalGrey'])
for x,y in [(-293,-5.1),(-293,3),(-337,-5),(-337,4)]:m.lathe(x,y,0,[(.15,0),(.13,.15),(.095,.85),(.16,.91),(.12,1.02)],IRON,12)
for x in [-233,-218,-274]:
 for y in [-5.7,-4.7]:
  m.cylinder(x,y,.06,.035,.7,IRON,8);m.cylinder(x,y,.76,.38,.045,WOOD,16)
  for xx in [-.55,.55]:
   m.box((x+xx,y,.43),(.37,.38,.05),WOOD)
   for dx in [-.15,.15]:
    for dy in [-.15,.15]:town_rod(m,(x+xx+dx,y+dy,.06),(x+xx+dx,y+dy,.43),.018,IRON)
m.finish();leaves.finish()
# Vasabrunnen: mapped position, basin and an explicitly simplified sculpture study.
m=ext_new('SM_Storgatan_Vasabrunnen_Study','Storgatan/Landmarks');vx,vy=-316.1,-13.1
m.lathe(vx,vy,0,[(6.1,0),(6.1,.25),(5.85,.33),(5.55,.28),(5.5,.14)],TS,64)
m.cylinder(vx,vy,.15,5.48,.025,town_mats['Glass'],64)
m.box((vx,vy,.4),(4.1,4.1,.5),TS);m.box((vx,vy,.70),(3.2,3.2,.20),TC)
m.lathe(vx,vy,.8,[(2.25,0),(2.20,.75),(2.55,.90),(2.6,1.02),(2.3,1.10)],TC,8)
m.lathe(vx,vy,1.85,[(.7,0),(.68,.18),(.48,.32),(.43,2.1),(.68,2.22)],TC,12)
ellipsoid(m,(vx,vy,4.7),(.33,.24,.58),TC)
ellipsoid(m,(vx+.1,vy,5.46),(.23,.22,.28),TC)
for points in [[(0,0,4.3),(-.3,.05,3.7),(-.55,.12,3.6)],[(.12,0,4.3),(.38,0,3.7),(.70,.13,3.55)],[(-.2,0,4.95),(-.55,0,5.35),(-.38,0,5.7)],[(.2,0,4.95),(.65,0,5.2),(1.15,0,5.45)]]:
 town_path(m,[(vx+x,vy+y,z) for x,y,z in points],.10,TC)
town_rod(m,(vx+.6,vy,5.85),(vx+1.85,vy,4.9),.055,TC)
m.finish()
extension_cameras=[
 ('34_Storgatan_Entré',(-37,-2.8,1.75),(-125,-2.4,3.3),29),
 ('35_Storgatan_Östra',(-84,-2.8,1.75),(-175,-2.2,3.8),29),
 ('36_Storgatan_Kaggensgatan',(-182,-2,1.75),(-270,-1.4,3.4),29),
 ('37_Larmtorget_Storgatan',(-303,-1,1.8),(-235,-1.6,4),31),
 ('38_Larmtorget_Teatern',(-302,-9,1.8),(-347,15,6.0),29),
 ('39_Larmtorget_Frimurare',(-308,4,2.0),(-350,-30,9.0),30),
 ('40_Storgatan_Översikt',(-205,-124,120),(-188,3,0),34),
]
extension_cameras.extend(larm_cameras)
extension_cameras.extend(street16_cameras)
# Reproject any Boolean-created UV slivers in the full build as well as the incremental one.
for name in extension_names:
 me=bpy.data.objects[name].data;me.calc_loop_triangles();uv=me.uv_layers.active.data;bad=set()
 for tri in me.loop_triangles:
  a,b,c=[uv[i].uv for i in tri.loops];d=b-a;e=c-a
  if abs(d.x*e.y-d.y*e.x)<1e-12:bad.add(tri.polygon_index)
 for pi in bad:
  poly=me.polygons[pi];dominant=max(range(3),key=lambda i:abs(poly.normal[i]));axes=[i for i in range(3) if i!=dominant]
  for li in poly.loop_indices:
   co=me.vertices[me.loops[li].vertex_index].co;uv[li].uv=(co[axes[0]]/4,co[axes[1]]/4)
