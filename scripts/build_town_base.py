# Ordinary buildings: original contours, estimated heights, modular facade details.
palette=[WHITE,PLASTER,CREAM,GREY,PINK,RED]
heights={'91846964':14.5,'91926317':8.8,'91970270':10.4,'91970255':8.4,'91970305':8.2,'91970276':8.7,'92412870':10.0,'92412842':7.6,'92412857':8.4,'92412866':6.0,'92412845':13.2}
for idx,(bid,b) in enumerate(buildings.items()):
 if bid=='38319501':continue
 p=b['polygon'];mx=sum(x for x,y in p)/len(p);my=sum(y for x,y in p)/len(p)
 if not (-122<mx<132 and -102<my<123):continue
 z=heights.get(bid,float(b['tags'].get('building:levels',2))*3.3+.5)
 ma=palette[idx%len(palette)]
 if bid=='91846964':ma=PLASTER
 if bid=='92412845':ma=CREAM
 if bid=='92412866':ma=WHITE
 if bid in ['92412842','92412857']:ma=PLASTER if bid=='92412857' else WHITE
 m=Mesh('SM_Radhuset' if bid=='92412845' else 'SM_Building_'+bid,'Landmarks' if bid=='92412845' else 'Buildings')
 m.prism(p,0,.55,BASE);m.prism(p,.55,z,ma)
 xmin,xmax=min(x for x,y in p),max(x for x,y in p);ymin,ymax=min(y for x,y in p),max(y for x,y in p)
 w=xmax-xmin;d=ymax-ymin
 # Inset perimeter roof preserves irregular OSM footprints.
 center=(sum(x for x,y in p)/len(p),sum(y for x,y in p)/len(p));n=len(p)
 inset=[(x*.70+center[0]*.30,y*.70+center[1]*.30,z+min(4.0,min(w,d)*.28)) for x,y in p]
 if bid not in ['92412845','92412857']:m.faces([(x,y,z) for x,y in p]+inset,[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]+[tuple(range(n,2*n))],COPPER if bid=='91846964' else TILE)
 area=sum(p[i][0]*p[(i+1)%n][1]-p[(i+1)%n][0]*p[i][1] for i in range(n));ccw=area>0
 for i,(x1,y1) in enumerate(p):
  x2,y2=p[(i+1)%n];dx,dy=x2-x1,y2-y1;length=math.hypot(dx,dy)
  if length<3:continue
  ang=math.atan2(dy,dx)+(0 if ccw else math.pi);normal=(math.sin(ang),-math.cos(ang));xx=(x1+x2)/2;yy=(y1+y2)/2
  for zz,th in [(.65,.18),(z-.15,.30),(3.5,.14)]:m.box((xx+normal[0]*.05,yy+normal[1]*.05,zz),(length+.15,.32,th),WHITE,ang)
  bays=max(1,round(length/3.05));floors=max(1,int(z/3.3))
  for floor in range(0 if bid in ['92412845','92412857','92412866'] and abs(dy)<.9 and yy>ymax-.9 else floors):
   for k in range(bays):
    t=(k+.5)/bays;x=x1+t*dx+normal[0]*.08;y=y1+t*dy+normal[1]*.08
    window(m,x,y,2.1+floor*3.3,min(1.25,length/bays*.48),1.8 if floor else 1.95,ang,False,WHITE,2)
  for t in [.03,.97]:
   m.box((x1+t*dx,y1+t*dy,z/2),(.35,.3,z),WHITE,ang)
 if bid=='92412845':
  # Rådhuset: low ground windows, tall main floor, small attic windows (three rows).
  x=(xmin+xmax)/2;yy=ymax+.16
  hip(m,x,(ymin+ymax)/2,w,d,z,5.2,TILE);pediment(m,x,yy,13.5,9.4,2.7,CREAM,math.pi);roundwindow(m,x,yy+.10,14.55,.56,math.pi)
  for k in range(7):
   xx=xmin+1.6+k*(w-3.2)/6
   if k!=3:window(m,xx,yy+.1,2.2,1.15,1.65,math.pi,False,STONE,2)
   window(m,xx,yy+.1,7.15,1.45,3.35,math.pi,False,STONE,3)
   window(m,xx,yy+.1,11.75,1.25,1.0,math.pi,False,STONE,2)
  m.box((x,yy+.18,2),(2.1,.25,3.7),GREEN)
  for k in range(8):
   xx=xmin+1.4+k*(w-2.8)/7
   for zz in [4.4,10.0]:m.box((xx,yy+.13,zz),(.07,.10,.9),IRON);m.box((xx,yy+.14,zz),(.42,.10,.06),IRON)
  for zz in [5.0,5.6,6.2,6.8,7.4,8.0,8.6,9.2,9.8,10.4,11.0,11.6,12.2]:m.box((x,yy+.055,zz),(w,.06,.035),STONE)
  for i in range(3):m.box((x,yy+.5+i*.28,.15*(3-i)),(3.8+i*.3,.55,.3*(3-i)),STONE)
 if bid=='92412866':
  xx=(xmin+xmax)/2;yy=ymax+.14
  pediment(m,xx,yy,6,w,2,WHITE,math.pi);roundwindow(m,xx,yy+.12,6.6,.45,math.pi)
  for k in range(5):window(m,xmin+1.1+k*(w-2.2)/4,yy,2.1,1.3,2.7,math.pi,True,WHITE,2)
  for wx in [xmin+2,xmax-2]:
   m.box((wx,yy+.07,5),(1.5,.16,1.1),GREY)
   for zz in [4.6,4.8,5,5.2,5.4]:m.box((wx,yy+.18,zz),(1.45,.05,.035),BASE)
 if bid=='92412857':
  # Second house right of the town hall, five green-framed bays on TWO floors.
  xx=(xmin+xmax)/2;yy=ymax+.16
  hip(m,xx,(ymin+ymax)/2,w,d,z,5.0,TILE)
  for k in range(5):
   wx=xmin+1.3+k*(w-2.6)/4
   window(m,wx,yy,6.15,1.3,1.65,math.pi,False,GREEN,2)
   if k!=2:window(m,wx,yy,2.3,1.3,2.0,math.pi,False,GREEN,2)
  m.box((xx,yy+.18,1.9),(1.3,.2,3.3),GREEN)
  for wx in [xmin+.5,xx-1.4,xx+1.4,xmax-.5]:m.box((wx,yy+.08,4.4),(.35,.3,7.6),WHITE)
  m.box((xx,yy,8.3),(w+.1,.35,.26),GREEN)
 # Modest chimneys.
 for xx in [xmin+w*.25,xmin+w*.76]:m.box((xx,(ymin+ymax)/2,z+3.5),(.8,.85,2.2),BASE)
 m.finish()
# Stadshotell outer footprint is an OSM multipolygon; front sits east of the square.
import xml.etree.ElementTree as ET
r=ET.parse(R/'references/osm-map.osm').getroot();nd={n.get('id'):(float(n.get('lat')),float(n.get('lon'))) for n in r.findall('node')}
a=math.radians(28.2)
def proj(lat,lon):
 e=(lon-site['origin'][1])*111320*math.cos(math.radians(site['origin'][0]));n=(lat-site['origin'][0])*111320
 return(e*math.cos(a)+n*math.sin(a),-e*math.sin(a)+n*math.cos(a))
w=next(w for w in r.findall('way') if w.get('id')=='91846976');pp=[proj(*nd[n.get('ref')]) for n in w.findall('nd')][:-1]
hotel=Mesh('SM_Calmar_Stadshotell','Landmarks');hotel.prism(pp,0,.6,BASE);hotel.prism(pp,.6,13.3,CREAM)
xmin=min(x for x,y in pp);xmax=max(x for x,y in pp);ymin=min(y for x,y in pp);ymax=max(y for x,y in pp)
hip(hotel,(xmin+xmax)/2,(ymin+ymax)/2,xmax-xmin,ymax-ymin,13.3,4.0,RED)
# West facade is the landmark frontage, height and ornament derived visually.
for y in [ymin+(ymax-ymin)*(i+.5)/9 for i in range(9)]:
 for z in [2.3,6.2,9.8]:window(hotel,xmin-.1,y,z,1.35,2.15,-math.pi/2,arched=z==2.3,trim=WHITE,grids=2)
for z in [.7,4.4,12.9]:hotel.box((xmin-.1,(ymin+ymax)/2,z),(.35,ymax-ymin+.5,.28),WHITE)
for y in [ymin+3,(ymin+ymax)/2,ymax-3]:
 pediment(hotel,xmin-.25,y,13.2,6,4.4,CREAM,-math.pi/2)
 hotel.box((xmin-.1,y,9),(.4,.65,8),WHITE)
# Prominent corner turret and upper lantern.
tx,ty=xmin+1.5,ymin+2.0
hotel.lathe(tx,ty,0,[(2.35,0),(2.35,13.3),(1.7,13.6),(1.7,17.2),(1.35,17.8),(.95,19.0)],CREAM,8)
hotel.lathe(tx,ty,19,[(1.65,0),(1.5,.4),(.65,1.2),(.65,2.1),(1.0,2.4),(.7,3.5),(.1,5.2)],COPPER,8)
for z in [5.5,9.2,15.4]:window(hotel,tx-2.3,ty,z,1.0,1.7,-math.pi/2,True,STONE,2)
for y in [ymin+6,ymin+10,ymin+14,ymin+18]:hotel.box((xmin-.65,y,3.45),(1.3,2.25,.2),AWNING)
hotel.finish()
