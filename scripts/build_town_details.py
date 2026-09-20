"""Photo-informed square frontages; dimensions remain visual estimates.
Executed in the canonical Blender build and by rebuild_town.py.
"""
TOWN_IDS=['92412845','92412866','92412857','92412842','92412870','91926317','91846964','91970270','91970255','91970305','91970276']
town_mats={}
for key,c,rough,metal in [
 ('Ivory',(.68,.65,.55),.79,0),('Lime',(.57,.57,.49),.79,0),('Yellow',(.63,.43,.19),.79,0),('Rose',(.49,.32,.25),.79,0),('Stone',(.38,.355,.31),.79,0),
 ('PaintWhite',(.68,.68,.61),.48,0),('PaintBlue',(.17,.25,.29),.48,0),('PaintGreen',(.08,.135,.10),.48,0),('PaintBrown',(.19,.105,.065),.48,0),('Panel',(.57,.58,.49),.73,0),
 ('TileRed',(.33,.105,.047),.78,0),('TileDark',(.105,.070,.043),.78,0),('MetalRed',(.28,.074,.045),.55,.25),('MetalGrey',(.115,.15,.132),.59,.35),('Glass',(.045,.078,.09),.20,.2)]:
 town_mats[key]=mat('M_Town_'+key,c,rough,metal,'Town'+key)
TI,TL,TY,TS=[town_mats[k] for k in ['Ivory','Lime','Yellow','Stone']]
TW,TB,TG,TT=[town_mats[k] for k in ['PaintWhite','PaintBlue','PaintGreen','TileRed']]
town_names=[]
def town_new(name,category='Buildings'):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 town_names.append(name);return Mesh(name,category)
def town_rod(m,a,b,r,ma,n=8):
 a,b=Vector(a),Vector(b);v=(b-a).normalized();u=v.cross(Vector((0,0,1)))
 if u.length<.01:u=v.cross(Vector((0,1,0)))
 u.normalize();w=v.cross(u);verts=[tuple(p+r*(u*math.cos(i*math.tau/n)+w*math.sin(i*math.tau/n))) for p in [a,b] for i in range(n)]
 m.faces(verts,[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],ma,True)
def town_path(m,pts,r,ma):
 for a,b in zip(pts,pts[1:]):town_rod(m,a,b,r,ma)
def facade_point(x,y,u,out,z,ang):return(x+u*math.cos(ang)+out*math.sin(ang),y+u*math.sin(ang)-out*math.cos(ang),z)
def facade_box(m,x,y,u,out,z,w,d,h,ma,ang):m.box(facade_point(x,y,u,out,z,ang),(w,d,h),ma,ang)
def town_window(m,x,y,z,w,h,ang=0,frame=TW,arched=False,rows=3,cols=2,trim=True):
 def b(u,o,zz,ww,dd,hh,ma):facade_box(m,x,y,u,o,zz,ww,dd,hh,ma,ang)
 # Outer sill/architrave and dark reveal sit directly against the wall surface.
 b(0,.016,z,w+.22,.07,h+.22,TS if trim else frame)
 b(0,.06,z,w,.07,h,town_mats['Glass'])
 for u in [-w/2,w/2]:b(u,.14,z,.065,.16,h+.06,frame)
 for zz in [z-h/2,z+h/2]:b(0,.14,zz,w+.07,.16,.065,frame)
 for k in range(1,cols):b(-w/2+w*k/cols,.15,z,.055 if k*2==cols else .026,.12,h,frame)
 for k in range(1,rows):b(0,.15,z-h/2+h*k/rows,w,.12,.036,frame)
 b(0,.17,z-h/2-.09,w+.30,.40,.11,TW if trim else frame)
 if trim:b(0,.09,z+h/2+.12,w+.24,.18,.07,TW)
 if arched:
  zz=z+h/2;r=w/2
  # Correctly wound filled half-disc, behind a closed arched surround.
  arc=[facade_point(x,y,r*math.cos(t*math.pi/32),.065,zz+r*math.sin(t*math.pi/32),ang) for t in range(33)]
  m.faces(arc,[tuple(range(33))],town_mats['Glass'])
  town_path(m,[facade_point(x,y,r*math.cos(t*math.pi/32),.15,zz+r*math.sin(t*math.pi/32),ang) for t in range(33)],.055,frame)
  b(0,.15,zz+r*.42,.045,.12,r*.85,frame)
def town_band(m,x,y,z,length,ang=0,ma=TW,scale=1):
 for dz,depth,height in [(-.15,.17,.12),(-.045,.28,.09),(.025,.37,.06),(.095,.43,.08)]:
  facade_box(m,x,y,0,depth*scale/2,z+dz*scale,length,depth*scale,height*scale,ma,ang)
def town_polyprofile(m,x,y,z,outline,ang,ma,depth=.25,edge=True):
 n=len(outline);v=[facade_point(x,y,u,o,z+h,ang) for o in [-depth,0] for u,h in outline]
 m.faces(v,[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],ma)
 if edge:town_path(m,[facade_point(x,y,u,.08,z+h,ang) for u,h in outline+[outline[0]]],.085,TW)
def town_pediment(m,x,y,z,w,h,ang,ma):town_polyprofile(m,x,y,z,[(-w/2,0),(w/2,0),(0,h)],ang,ma,.35)
def town_roof(m,x,y,w,d,z,h,ma,metal=False,axis='x',hipped=True):
 # Local roof x follows ridge. Face UV follows courses across the roof slope.
 ang=0 if axis=='x' else math.pi/2
 if axis=='y':w,d=d,w
 a=w/2+.32;b=d/2+.32;inset=min(b*.82,a*.45) if hipped else 0
 local=[(-a,-b,0),(a,-b,0),(a,b,0),(-a,b,0),(-a+inset,0,h),(a-inset,0,h)]
 faces=[(0,1,5,4),(1,2,5),(2,3,4,5),(3,0,4)]
 co,si=math.cos(ang),math.sin(ang)
 def p(u,v,q):return(x+u*co-v*si,y+u*si+v*co,z+q)
 for face in faces:
  vs=[p(*local[i]) for i in face];normal=(Vector(vs[1])-Vector(vs[0])).cross(Vector(vs[2])-Vector(vs[0])).normalized()
  tangent=Vector((0,0,1)).cross(normal).normalized();up=normal.cross(tangent)
  uv=[(Vector(q).dot(tangent)/4,Vector(q).dot(up)/4) for q in vs]
  m.faces(vs,[tuple(range(len(vs)))],ma,uvcoords=uv)
 # Solid gables for an unhipped roof.
 if not hipped:
  for u in [-a,a]:m.faces([p(u,-b,0),p(u,b,0),p(u,0,h)],[(0,1,2)],TI)
 town_rod(m,p(-a+inset,0,h+.04),p(a-inset,0,h+.04),.105,ma,12)
 for side in [-1,1]:
  town_rod(m,p(-a,side*b,0),p(a,side*b,0),.095,town_mats['MetalGrey'],12)
  if metal:
   for i in range(1,int(w/.63)):
    u=-a+i*.63
    # Clip standing seams where hipped roof planes meet.
    t=max(0,min(1,(a-abs(u))/max(inset,.001)))
    town_rod(m,p(u,side*b,.018),p(u,side*b*(1-t),h*t+.018),.016,ma)
 for u in ([-a+inset,a-inset] if max(w,d)>5 else []):
  m.box(p(u,0,h+.6),(.65,.78,1.4),TI)
  m.box(p(u,0,h+1.27),(.81,.93,.16),TS)
def town_drain(m,x,y,z,ang):
 def p(o,h):return facade_point(x,y,0,o,h,ang)
 town_path(m,[p(.33,z),p(.22,z-.4),p(.22,.45),p(.5,.2)],.055,town_mats['MetalGrey'])
 for zz in [.75,3.2,6.1,9.4,12.1]:
  if zz<z:facade_box(m,x,y,0,.19,zz,.19,.24,.045,IRON,ang)
def town_bounds(p):return min(x for x,y in p),max(x for x,y in p),min(y for x,y in p),max(y for x,y in p)
def town_shell(m,p,z,ma):m.prism(p,0,.5,TS);m.prism(p,.5,z,ma)
def town_edges(m,p,z,frame=TW,floors=2,ma=TI,skip=None):
 area=sum(p[i][0]*p[(i+1)%len(p)][1]-p[(i+1)%len(p)][0]*p[i][1] for i in range(len(p)))
 for i,(x1,y1) in enumerate(p):
  x2,y2=p[(i+1)%len(p)];dx,dy=x2-x1,y2-y1;ln=math.hypot(dx,dy)
  if ln<3:continue
  ang=math.atan2(dy,dx)+(0 if area>0 else math.pi);xx,yy=(x1+x2)/2,(y1+y2)/2
  town_band(m,xx,yy,z-.04,ln+.1,ang)
  if skip and skip(xx,yy):continue
  town_band(m,xx,yy,.6,ln,ang,TS,.6)
  bays=max(1,round(ln/3.0))
  for floor in range(floors):
   zz=2.0+floor*(z-1.8)/floors
   for k in range(bays):
    t=(k+.5)/bays;town_window(m,x1+t*dx,y1+t*dy,zz,min(1.3,ln/bays*.51),1.85,ang,frame)
  for t in [.025,.975]:town_drain(m,x1+t*dx,y1+t*dy,z,ang)

exec(compile((R/'scripts/town_detail_helpers.py').read_text(),str(R/'scripts/town_detail_helpers.py'),'exec'))

# Rådhuset: eleven bays and blue-grey joinery, as in the municipality's recent photographs.
p=buildings['92412845']['polygon'];x0,x1,y0,y1=town_bounds(p);xc=(x0+x1)/2;w=x1-x0;z=13.2
m=town_new('SM_Radhuset','Landmarks');town_shell(m,p,z,TI);town_edges(m,p,z,TB,3,skip=lambda x,y:y>y1-.5)
town_roof(m,xc,y1-6.0,w,12.0,z,5.2,town_mats['TileDark'])
town_roof(m,x1-2.9,(y0+y1-12)/2,5.8,y1-12-y0,z,1.5,town_mats['TileDark'],axis='y')
yy=y1+.025;ang=math.pi
town_pediment(m,xc,yy+.14,z,10.4,2.9,ang,TI)
for k in range(11):
 xx=x0+1.3+k*(w-2.6)/10
 if k!=5:town_window(m,xx,yy,2.25,1.28,1.75,ang,TB,rows=3,cols=4)
 town_window(m,xx,yy,7.1,1.3,3.3,ang,TB,rows=6,cols=4)
 town_window(m,xx,yy,11.83,1.28,.96,ang,TB,rows=2,cols=4)
for zz in [4.05,4.6,9.0,10.75,13.03]:town_band(m,xc,yy,zz,w,ang,TW,.65)
# Restrained shallow rustication across the central five bays.
for zz in [4.8+i*.42 for i in range(20)]:
 if 5.4<zz<8.9:continue
 facade_box(m,xc,yy,0,.04,zz,w*.49,.06,.022,TS,ang)
for k in range(12):
 xx=x0+.65+k*(w-1.3)/11
 for zz in [4.35,10.0]:
  town_rod(m,(xx,yy+.12,zz-.4),(xx,yy+.12,zz+.4),.024,IRON)
  town_rod(m,(xx-.16,yy+.12,zz+.06),(xx+.16,yy+.12,zz+.06),.022,IRON)
  for sign in [-1,1]:
   pts=[(xx+sign*(.07+.075*math.sin(t*math.pi*1.6)),yy+.13,zz+.14+.12*math.cos(t*math.pi*1.6)) for t in [j/12 for j in range(13)]];town_path(m,pts,.014,IRON)
town_door(m,xc,yy,.51,1.44,3.09,ang,town_mats['PaintBrown'])
for j in range(3):m.box((xc,yy+.35+j*.3,.085*(3-j)),(2.9+j*.28,.65,.17*(3-j)),TS)
# Three stone plaques with interpreted medallions; no invented lettering.
for k in [-1,0,1]:
 xx=xc+k*w*.365;facade_box(m,xx,yy,0,.14,10.1,1.0,.22,1.17,TS,ang)
 facade_box(m,xx,yy,0,.26,10.1,.78,.04,1.0,TB if k==0 else IRON,ang)
 town_path(m,[(xx+.35*math.cos(t*math.tau/40),yy+.3,10.1+.43*math.sin(t*math.tau/40)) for t in range(41)],.026,GOLD)
 if k==0:
  for sign in [-1,1]:town_path(m,[(xx+sign*(.12+.15*math.cos(.3+t*5.6/32)),yy+.34,10.07+.26*math.sin(.3+t*5.6/32)) for t in range(33)],.022,GOLD)
  for dx in [-.075,.075]:town_rod(m,(xx+dx,yy+.34,9.9),(xx-dx,yy+.34,10.26),.016,GOLD)
  crown=[(-.27,10.53),(-.32,10.72),(-.14,10.61),(0,10.80),(.14,10.61),(.32,10.72),(.27,10.53),(-.27,10.53)]
  town_path(m,[(xx+dx,yy+.34,zz) for dx,zz in crown],.029,GOLD)
 elif k==-1:
  town_rod(m,(xx,yy+.34,9.84),(xx,yy+.34,10.36),.02,GOLD)
  town_rod(m,(xx-.23,yy+.34,10.26),(xx+.23,yy+.34,10.26),.024,GOLD)
  for sign in [-1,1]:
   town_rod(m,(xx+sign*.21,yy+.34,10.26),(xx+sign*.21,yy+.34,9.99),.009,GOLD)
   town_path(m,[(xx+sign*.21+.10*math.cos(t*math.pi/16),yy+.34,10.0-.06*math.sin(t*math.pi/16)) for t in range(17)],.018,GOLD)
 else:
  town_polyprofile(m,xx,yy+.33,9.88,[(-.23,0),(.23,0),(.18,.15),(.07,.23),(.11,.38),(.05,.46),(-.07,.46),(-.12,.38),(-.07,.23),(-.18,.15)],ang,GOLD,.025,False)
oldstone,oldglass,oldframe=STONE,GLASS,FRAME;STONE,TEMP=TW,None;GLASS,FRAME=town_mats['Glass'],TB
roundwindow(m,xc,yy+.30,14.30,.44,ang);STONE,GLASS,FRAME=oldstone,oldglass,oldframe
for xx in [x0+.1,x1-.1]:town_drain(m,xx,yy,z,ang)
m.finish()

# South row: fire station, green-framed neighbour, and two further street houses.
for bid in ['92412866','92412857','92412842','92412870']:
 p=buildings[bid]['polygon'];x0,x1,y0,y1=town_bounds(p);w=x1-x0;xc=(x0+x1)/2;yy=y1+.025;ang=math.pi
 z={'92412866':6.0,'92412857':8.4,'92412842':7.6,'92412870':10.0}[bid];ma=TI if bid in ['92412866','92412842'] else TY
 m=town_new('SM_Building_'+bid);town_shell(m,p,z,ma);town_edges(m,p,z,TG if bid=='92412857' else TW,2,skip=lambda x,y:y>y1-.6)
 # Use a proper ridge instead of the former flat-topped inset roof.
 depth=min(y1-y0,12.5)
 town_roof(m,xc,y1-depth/2,w,depth,z,2.9 if bid=='92412866' else 4.0,town_mats['MetalGrey'] if bid=='92412866' else TT,metal=bid=='92412866',axis='x')
 if y1-y0>depth+.5:town_roof(m,xc,(y0+y1-depth)/2,w,y1-depth-y0,z,2.3,TT,axis='y')
 if bid=='92412866':
  town_pediment(m,xc,yy+.12,6,w,2,ang,TI)
  for k in range(5):town_window(m,x0+1.2+k*(w-2.4)/4,yy,1.9,1.30,2.30,ang,TG,True,3)
  STONE,GLASS,FRAME=TW,town_mats['Glass'],TB;roundwindow(m,xc,yy+.16,5.05,.46,ang);STONE,GLASS,FRAME=oldstone,oldglass,oldframe
  for xx in [x0+2,x1-2]:facade_box(m,xx,yy,0,.08,5.0,1.4,.16,.85,TS,ang)
 else:
  bays=5 if bid!='92412870' else 6
  for k in range(bays):
   xx=x0+1.15+k*(w-2.3)/(bays-1)
   for zz in [2.2,z-2.1]:
    if k==bays//2 and zz==2.2:continue
    town_window(m,xx,yy,zz,1.3,2.2 if bid=='92412842' else 1.8,ang,TG if bid=='92412857' else (town_mats['PaintBrown'] if bid=='92412842' else TW),rows=4 if bid=='92412842' else 3,cols=4 if bid=='92412842' else 2)
  town_door(m,xc,yy,.34,1.40,3.11,ang,town_mats['PaintBrown'] if bid=='92412842' else TG,bid=='92412842',bid=='92412842')
  for j in range(2):facade_box(m,xc,yy,0,.34+j*.28,.085*(2-j),1.95+j*.25,.65,.17*(2-j),TS,ang)
  town_band(m,xc,yy,4.35,w,ang)
  if bid=='92412842':
   town_pediment(m,xc,yy+.10,z+.1,5.0,1.35,ang,TI)
   STONE,GLASS,FRAME=TW,town_mats['Glass'],TB;roundwindow(m,xc,yy+.20,z+.65,.40,ang);STONE,GLASS,FRAME=oldstone,oldglass,oldframe
   town_pediment(m,xc,yy+.18,3.7,2.0,.48,ang,TW)
   # Raised timber strips and recessed painted panels visible in the 2024 reference.
   for k in range(26):facade_box(m,x0+.25+k*(w-.5)/25,yy,0,.035,4.1,.035,.055,6.9,TW,ang)
   for xx in [x0+.2,xc-1.15,xc+1.15,x1-.2]:facade_box(m,xx,yy,0,.10,4.1,.22,.16,6.9,TW,ang)
 town_band(m,xc,yy,z,w+.2,ang)
 for xx in [x0+.08,x1-.08]:town_drain(m,xx,yy,z,ang)
 m.finish()

# Nelsonska: plaster-imitating vertical timber, blue-grey sashes, seven bays.
p=buildings['91926317']['polygon'];x0,x1,y0,y1=town_bounds(p);z=8.8;m=town_new('SM_Building_91926317');town_shell(m,p,z,town_mats['Panel'])
town_edges(m,p,z,TB,2,skip=lambda x,y:x<x0+.8)
ang=-math.pi/2;yc=(y0+y1)/2;length=y1-y0
town_roof(m,x0+6.0,yc,12.0,length,z,4.2,TT,axis='y',hipped=False)
town_roof(m,(x0+12+x1)/2,yc,x1-x0-12,length,z,2.4,TT,axis='x')
for k in range(7):
 yy=y0+1.45+k*(length-2.9)/6
 for zz in [2.4,6.5]:
  if k==3 and zz==2.4:continue
  town_window(m,x0-.025,yy,zz,1.3,2.1,ang,TB,rows=3)
town_band_gap(m,x0-.02,yc,.6,length,ang,1.65,TW)
for zz in [4.3,4.55,8.7]:town_band(m,x0-.02,yc,zz,length,ang,TW)
for k in range(8):facade_box(m,x0-.02,y0+.25+k*(length-.5)/7,0,.08,4.45,.23,.16,8.4,TW,ang)
town_door(m,x0,yc,.68,1.30,2.77,ang,TW)
for j in range(4):m.box((x0-.35-j*.28,yc,.085*(4-j)),(.65,2.4+j*.1,.17*(4-j)),TS)
for yy in [y0+.1,y1-.1]:town_drain(m,x0,yy,z,ang)
m.finish()

# North-east municipal building and west-side row: fine joinery, cornices and drainage.
for bid in ['91846964','91970270','91970255','91970305','91970276']:
 p=buildings[bid]['polygon'];x0,x1,y0,y1=town_bounds(p);z={'91846964':12.6,'91970270':10.4,'91970255':8.4,'91970305':8.2,'91970276':8.7}[bid]
 ma={'91846964':TY,'91970270':TI,'91970255':TL,'91970305':town_mats['Rose'],'91970276':TY}[bid]
 m=town_new('SM_Building_'+bid);town_shell(m,p,z,ma);floors=3 if bid in ['91846964','91970270'] else 2
 town_edges(m,p,z,TB if bid=='91846964' else TW,floors,skip=(lambda x,y:x<x0+1) if bid=='91846964' else None)
 town_roof(m,(x0+x1)/2,(y0+y1)/2,x1-x0,y1-y0,z,3.4,town_mats['MetalGrey'] if bid=='91846964' else TT,metal=bid=='91846964',axis='y' if y1-y0>x1-x0 else 'x')
 # Exterior facing the square gets continuous moulded string courses.
 xx=x0 if bid=='91846964' else x1;ang=-math.pi/2 if bid=='91846964' else math.pi/2
 for zz in [3.7,z-.4]:town_band(m,xx,(y0+y1)/2,zz,y1-y0,ang)
 if bid=='91846964':
  for yy in [y0+2.6+i*(y1-y0-5.2)/10 for i in range(11)]:
   for zz in [2.0,6.0,10.0]:town_window(m,xx-.025,yy,zz,1.3,2.0,ang,TB,zz==2.0,rows=3)
   town_pediment(m,xx-.10,yy,7.2,1.8,.53,ang,TI)
 m.finish()

# Stadshotell: solid shaped gables, red standing-seam roof, square tower at north end.
import xml.etree.ElementTree as ET
r=ET.parse(R/'references/osm-map.osm').getroot();nd={n.get('id'):(float(n.get('lat')),float(n.get('lon'))) for n in r.findall('node')}
aa=math.radians(28.2)
def town_proj(lat,lon):
 e=(lon-site['origin'][1])*111320*math.cos(math.radians(site['origin'][0]));n=(lat-site['origin'][0])*111320
 return(e*math.cos(aa)+n*math.sin(aa),-e*math.sin(aa)+n*math.cos(aa))
w=next(w for w in r.findall('way') if w.get('id')=='91846976');pp=[town_proj(*nd[n.get('ref')]) for n in w.findall('nd')][:-1]
x0,x1,y0,y1=town_bounds(pp);xx=x0-.03;yc=(y0+y1)/2;length=y1-y0;ang=-math.pi/2;z=13.3
m=town_new('SM_Calmar_Stadshotell','Landmarks');town_shell(m,pp,z,TI);town_edges(m,pp,z,town_mats['PaintBrown'],3,skip=lambda x,y:x<x0+2)
town_roof(m,x0+6.1,yc,12.2,length,z,4.4,town_mats['MetalRed'],True,axis='y')
town_roof(m,(x0+12.2+x1)/2,yc,x1-x0-12.2,length,z,2.5,town_mats['MetalRed'],True,axis='x')
ys=[y0+1.65+i*(length-3.3)/8 for i in range(9)]
for i,yy in enumerate(ys):
 for zz in [2.05,6.45,10.2]:
  if zz==2.05:
   if i!=4:town_window(m,xx,yy,zz,1.35,2.15,ang,town_mats['PaintBrown'],True,rows=1)
  else:town_cross_window(m,xx,yy,zz,1.35,2.15,ang,town_mats['PaintBrown'])
 if i not in [0,4,8]:
  # Curved canvas hood; thin closed edge, not an opaque box.
  vs=[]
  for u in [-.85,.85]:
   for j in range(13):
    t=j*math.pi/2/12;vs.append(facade_point(xx,yy,u,.12+.85*math.sin(t),3.72+.64*math.cos(t),ang))
  m.faces(vs,[(j,j+1,14+j,13+j) for j in range(12)],AWNING)
  town_rod(m,facade_point(xx,yy,-.85,.97,3.72,ang),facade_point(xx,yy,.85,.97,3.72,ang),.027,IRON)
town_band_gap(m,xx,yc,.55,length,ang,2.15,TW)
for zz in [4.48,4.78,13.18]:town_band(m,xx,yc,zz,length,ang,TW)
# Flemish-inspired stepped/curved silhouette, based on the front photograph.
gable=[(-2.5,0),(2.5,0),(2.5,2.1),(2.15,2.25),(1.7,2.62),(1.6,3.35),(1.1,3.4),(.85,4.0),(.65,4.28),(.3,4.47),(-.3,4.47),(-.65,4.28),(-.85,4.0),(-1.1,3.4),(-1.6,3.35),(-1.7,2.62),(-2.15,2.25),(-2.5,2.1)]
for yy in [y0+4.3,y1-3.6]:
 town_polyprofile(m,xx-.09,yy,z,gable,ang,TI,.45)
 town_window(m,xx-.11,yy,14.65,1.1,1.85,ang,town_mats['PaintBrown'],True,3)
for yy in [y0+9,y0+14,y0+19]:
 m.box((x0+1.0,yy,14.3),(1.8,1.8,2.0),town_mats['MetalRed'])
 town_window(m,x0+.04,yy,14.45,.82,1.42,ang,TW)
 town_pediment(m,x0+.02,yy,15.32,1.85,.67,ang,town_mats['MetalRed'])
# Tall square tower belongs toward the northern part of the square-facing frontage.
tx,ty=x0+1.7,y1-9.0
hotel_tower(m,tx,ty)
# Small rounded corner oriel and copper cap at the street corner.
ox,oy=x0-.65,y1-1.25
m.lathe(ox,oy,7.1,[(.25,0),(.85,.35),(1.1,.8),(1.1,4.7),(1.20,4.9),(1.20,5.15),(.8,5.65),(.42,5.9)],TI,24)
m.lathe(ox,oy,13,[(1.2,0),(1.24,.10),(1.18,.3),(1.0,.55),(.65,.72),(.35,.82),(.27,.96),(.26,1.13),(.40,1.25),(.42,1.48),(.26,1.72),(.06,1.85)],TC,48)
town_window(m,ox-1.1,oy,10.1,.75,2.15,ang,town_mats['PaintBrown'])
for yy in [ys[1],ys[5],ys[7]]:
 facade_box(m,xx,yy,0,.42,9.24,1.65,.82,.12,TS,ang)
 for h in [9.4,10.05]:town_rod(m,facade_point(xx,yy,-.8,.88,h,ang),facade_point(xx,yy,.8,.88,h,ang),.026,IRON)
 for i in range(9):town_rod(m,facade_point(xx,yy,-.78+i*.195,.88,9.3,ang),facade_point(xx,yy,-.78+i*.195,.88,10.1,ang),.017,IRON)
# Ornamental stone portal, fanlight, closed glazed double doors and metalwork.
hotel_portal(m,xx,ys[4],ang)
for yy in [y0+.15,y1-.15]:town_drain(m,xx,yy,z,ang)
m.finish()

town_cameras=[('32_Radhusport',(32,-25,1.9),(35.2,-34.2,2.4),43),('33_Nelsonska_Port',(50,10.7,1.7),(58.55,10.8,2.0),38),('28_Hotellportal',(49,-21,1.9),(58.02,-24.77,2.7),38),('29_Hotelltorn',(39,-4,23.8),(59.7,-17.5,21.0),50),('30_Radmannen_Port',(-7,-23,1.9),(-9.1,-33.5,2.7),40),('31_Hotell_Snickeri',(47,-21,8.5),(58,-21.1,9.8),48),('23_Radhus_Fasad',(27,-2,2.4),(35,-38,8.2),36),('24_Sodra_Husraden',(-7,1,2.8),(7,-39,6.8),28),('25_Stadshotell',(18,-12,3.0),(60,-24,12.0),32),('26_Nelsonska',(24,17,2.4),(62,11,6),34),('27_Vastra_Husraden',(0,15,3),(-42,29,6),29)]
print('TOWN_DETAIL_MESHES',town_names)
