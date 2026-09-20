"""Cathedral detail pass, photo-led and intentionally labelled approximate.
Uses museum plan + interior/exterior photographs listed in REFERENCES.md.
No invented writing or invented historical painting: the altarpiece uses a
credited CC BY-SA photograph with a UV selection of the painted canvas.
"""
import shutil
PULPIT=mat('M_Pulpit_Painted_Wood',(.027,.071,.067),.48,texture='ChurchDoor')
exec(compile((R/'scripts/sculpture_helpers.py').read_text(),str(R/'scripts/sculpture_helpers.py'),'exec'))
# Exterior stonework and correctly shaped flaming urn finials.
interior_stone=STONE;STONE=CHURCHSTONE
interior_copper=COPPER;COPPER=CHURCHCOPPER
m=Mesh('SM_Domkyrka_Exterior_Details','Cathedral exterior details')
for u in [-14.4,14.4]:
 for v in [-13.1,13.1]:
  m.lathe(cx+u,cy+v,29.6,[(.16,0),(.36,.14),(.36,.24),(.21,.31),(.24,.55),(.42,.78),(.46,.96),(.32,1.13),(.24,1.20),(.35,1.28),(.35,1.35)],CHURCHURN,32)
  for k in range(5):
   a=k*math.tau/5
   # Curving individual flame tongues make a lobed urn silhouette.
   for j in range(9):
    t=j/8;r=.18*(1-t);zz=30.94+t*(.76 if k else 1.05)
    sphere(m,u+math.cos(a)*(.18*(1-t)+.11*math.sin(t*math.pi)),v+math.sin(a)*.18*(1-t),zz,max(.017,r),GOLD)
# Portal columns, entablature, volutes, voussoirs and open-leaf hardware.
for sign in [-1,1]:
 v=-18.86 if sign<0 else 18.65
 for u in [-2.25,2.25]:
  m.lathe(cx+u,cy+v,1.35,[(.46,0),(.46,.25),(.35,.33),(.31,.46),(.29,4.48),(.38,4.60),(.46,4.80)],STONE,24)
  box(m,u,v,6.26,1.0,.9,.24,STONE)
  for offset in [-.32,.32]:
   pts=[(cx+u+offset+.18*math.cos(t*math.tau/64),cy+v+sign*.40,6.03+.18*math.sin(t*math.tau/64)) for t in range(64)]
   m.faces(pts,[tuple(range(64))],STONE)
   ext_tube(m,pts+[pts[0]],.035,STONE,10)
   ext_tube(m,[(cx+u+offset+.155*(1-t)*math.cos(t*math.tau*1.25),cy+v+sign*.43,6.03+.155*(1-t)*math.sin(t*math.tau*1.25)) for t in [i/64 for i in range(65)]],.017,STONE,8)
 for z,w,d,h in [(6.45,5.55,.95,.22),(6.66,5.75,1.05,.18),(6.83,6.0,1.15,.13)]:box(m,0,v,z,w,d,h,STONE)
 for u in [i*.27 for i in range(-10,11)]:box(m,u,v+sign*.49,6.55,.12,.13,.17,STONE)
 # The portal has a flat profiled cornice; its south cartouche is added below.
 for k in range(17):
  a=k*math.pi/16
  rod(m,(1.29*math.cos(a),v+sign*.13,9.4+1.29*math.sin(a)),(1.44*math.cos(a),v+sign*.13,9.4+1.44*math.sin(a)),.025,BASE)
 if sign<0:
  # Door leaves lie along Y; panels/hinges remain outside the clear passage.
  for s in [-1,1]:
   for zz in [2.15,3.60,5.05]:
    box(m,s*1.28,-17.73,zz,.08,.91,1.13,GREEN)
    for vv in [-18.15,-17.31]:box(m,s*1.23,vv,zz,.06,.055,1.13,GREEN)
    for zedge in [zz-.54,zz+.54]:box(m,s*1.23,-17.73,zedge,.06,.91,.055,GREEN)
    for vv in [-18.25,-17.2]:box(m,s*1.25,vv,zz,.08,.08,.08,IRON)
   rod(m,(s*1.25,-17.25,3.38),(s*1.25,-17.25,3.70),.035,GOLD)
   for zz in [1.6,3.8,5.9]:box(m,s*1.32,-18.3,zz,.15,.28,.09,IRON)
 # Solid carved scroll shoulders: masonry backing touches the upper facade.
 for side in [-1,1]:
  def wp(u,depth,z):return (cx+side*u,cy+sign*depth,z)
  outline=[(10.62,13.3),(12.92,13.3),(12.92,14.7)]
  outline += [(11.68+1.17*math.cos(t),14.72+1.17*math.sin(t)) for t in [i*math.pi/40 for i in range(21)]]
  outline += [(11.30,16.30),(10.62,18.70)]
  n=len(outline);verts=[wp(u,d,z) for d in [17.45,17.84] for u,z in outline]
  m.faces(verts,[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],STONE)
  pts=[]
  for j in range(100):
   t=j/99;a=t*math.tau*1.18;rr=1.08*(1-.83*t)
   pts.append(wp(11.68+rr*math.cos(a),17.88,14.72+rr*math.sin(a)))
  ext_tube(m,pts,.055,STONE,10)
  ext_tube(m,[wp(10.69+1.40*(1-t)**2,17.88,15.06+3.61*t) for t in [j/48 for j in range(49)]],.075,STONE,10)
# Copper eaves channels/downpipes with discrete fastening collars.
for s in [-1,1]:
 for u in [-10.25,10.25]:
  v=s*18.7
  curve(m,[(u,v,12.8),(u+.27,v,12.45),(u+.27,v,1.2),(u+.44,v+s*.12,.85)],.063,COPPER)
  for z in [2,5,8,11]:m.lathe(cx+u+.27,cy+v,z,[(.078,0),(.078,.08)],IRON,12)
 for a,b in [(-10,10)]:rod(m,(a,s*18.67,13.13),(b,s*18.67,13.13),.085,COPPER)
# Additional cornice profiles and block-joint end returns across the main fronts.
for s in [-1,1]:
 for z,w,h in [(11.49,22.3,.09),(12.02,22.8,.1),(12.83,23.0,.12)]:box(m,0,s*18.55,z,w,.8,h,STONE)
 # Pilaster joints now come from the shallow aligned masonry normal map.
exec(compile((R/'scripts/build_exterior_stonework.py').read_text(),str(R/'scripts/build_exterior_stonework.py'),'exec'))
m.finish()
STONE=interior_stone;COPPER=interior_copper
# Public edition: neutral canvas, pending a compatible openly licensed painting.
PHOTO=mat('M_Altarpiece_Photo',(.23,.17,.10),.88)
m=Mesh('SM_Domkyrka_Altarpiece_Canvas','Cathedral interior details')
# Existing frame: 4.3 m wide, straight sides to z9.35, semicircular head.
outline=[(-2.04,3.46),(2.04,3.46),(2.04,9.35)]+[(2.04*math.cos(i*math.pi/48),9.35+2.04*math.sin(i*math.pi/48)) for i in range(1,49)]
m.faces([(cx+25.01,cy+v,z) for v,z in outline],[tuple(range(len(outline)))],PHOTO)
m.v=[(x-2.5,y,z) for x,y,z in m.v]
obj=m.finish();me=obj.data
for loop in me.loops:
 co=me.vertices[loop.vertex_index].co
 # Source canvas occupies approximately x=465..788,y=756..1355.
 me.uv_layers.active.data[loop.index].uv=((626.5-(co.y-cy)/2.04*161.5)/1263,1-(1355-(co.z-3.46)/7.93*599)/1552)
# Altar carving, leaf capitals, broken cornice, angel cloud and sculptural figures.
m=Mesh('SM_Domkyrka_Altar_Carving','Cathedral interior details')
for v in [-2.7,2.7]:
 capital(m,24.6,v,10.35,.45,.84,IVORY)
 for z,r in [(3.25,.48),(10.65,.48),(11.45,.73)]:m.lathe(cx+24.6,cy+v,z,[(r,0),(r,.09)],IVORY,32)
# Smaller leaves follow both sides of the arched gold frame.
for s in [-1,1]:
 for j in range(18):leaf(m,24.99,s*2.20,3.55+j*.31,.22,.34,GOLD,'x',-1)
 for offset in [0,.13]:
  curve(m,[(24.94-offset,2.19*math.cos(i*math.pi/64),9.35+2.19*math.sin(i*math.pi/64)) for i in range(65)],.065,GOLD)
 # Swept white cornice, visually separate from the painting frame.
 for zz,rad in [(13.5,.16),(13.72,.10)]:
  curve(m,[(24.4,s*(1.15+2.3*t),zz-1.0*t) for t in [i/28 for i in range(29)]],rad,IVORY)
 for j in range(11):leaf(m,24.25,s*(1.3+j*.20),13.77-j*.086,.20,.40,IVORY,'x',-1)
# Connected entablature over the relief, with individual dentils.
for z,rad in [(12.65,.12),(12.9,.16),(13.09,.08)]:
 curve(m,[(24.63,-2.5+5*t,z+.23*math.sin(math.pi*t)) for t in [j/64 for j in range(65)]],rad,IVORY)
for j in range(23):
 v=-2.45+j*4.9/22
 box(m,24.59,v,12.43+.23*math.cos(v/2.5*math.pi/2),.35,.11,.18,IVORY)
for v in [-2.7,2.7]:
 for j in range(5):box(m,23.87,v+(j-2)*.28,12.32,.16,.11,.20,IVORY)
# Upper relief field, bounded by the painting arch and the broken cornice.
outline=[(-2.22,9.35)]+[(2.22*math.cos(math.pi-i*math.pi/48),9.35+2.22*math.sin(math.pi-i*math.pi/48)) for i in range(1,49)]+[(2.22,12.87),(-2.22,12.87)]
m.faces([(cx+25.06,cy+v,z) for v,z in outline],[tuple(range(len(outline)))],GOLD)
figure(m,24.93,0,11.72,1.1,GOLD,'wide')
for sign in [-1,1]:
 figure(m,24.83,sign*1.6,10.62,.95,GOLD,'raised')
 wing(m,24.95,sign*1.6,11.22,.55,.64,GOLD,sign)
 # Seated angels at the ends of the broken pediment, with feathered wings.
 figure(m,24.18,sign*2.5,13.10,1.08,IVORY,'raised')
 wing(m,24.43,sign*2.43,13.67,.9,.94,IVORY,sign)
# Radiating bundles of gilded rays around a filled medallion.
zc=15.45
for j in range(44):
 a=j*math.tau/44;outer=2.50+.28*math.sin(j*2.6)
 for shift in [-.015,0,.015]:
  aa=a+shift
  rod(m,(24.96,1.05*math.cos(aa),zc+1.05*math.sin(aa)),(24.96,outer*math.cos(aa),zc+outer*math.sin(aa)),.024 if shift else .043,GOLD)
m.faces([(cx+24.90,cy+.76*math.cos(i*math.tau/64),zc+.76*math.sin(i*math.tau/64)) for i in range(64)],[tuple(range(64))],GOLD)
for j in range(12):
 a=j*math.tau/12;v=1.13*math.cos(a);z=zc+1.13*math.sin(a)
 # Gold scrolling cloud supports, replacing the conspicuous white bead ring.
 curve(m,[(24.72,v+.27*(1-i/70)*math.cos(i*math.tau/28),z+.27*(1-i/70)*math.sin(i*math.tau/28)) for i in range(55)],.085,GOLD)
 if j%2==0:
  figure(m,24.56,v,z-.20,.48,IVORY,'wide')
  for sign in [-1,1]:wing(m,24.62,v+sign*.05,z+.13,.24,.28,IVORY,sign)
# Central white dove, carved flight feathers rather than simple rods.
ellipsoid(m,24.56,0,zc,.10,.11,.23,IVORY)
ellipsoid(m,24.50,0,zc+.23,.07,.075,.09,IVORY)
for sign in [-1,1]:wing(m,24.62,sign*.06,zc+.06,.57,.41,IVORY,sign)
for v in [-4.4,4.4]:
 # Marble plinth and white profiled cap physically support each statue.
 box(m,24.20,v,2.40,1.18,1.18,1.46,MARBLE)
 for z,w,h in [(1.73,1.35,.16),(3.12,1.28,.12),(3.24,1.43,.12),(3.33,1.48,.06)]:box(m,24.20,v,z,w,w,h,IVORY)
 figure(m,24.20,v,3.35,2.32,GOLD,'chalice' if v>0 else 'rest')
 if v>0:
  # Chalice and staff visible in the left figure's silhouette.
  m.lathe(cx+23.806,cy+v-.65,4.94,[(.12,0),(.035,.07),(.035,.26),(.13,.31),(.19,.45),(.19,.48)],GOLD,24)
  rod(m,(23.80,v+.40,3.65),(23.80,v+.40,6.2),.023,GOLD)
  rod(m,(23.80,v+.14,5.91),(23.80,v+.66,5.91),.023,GOLD)
 else:
  # Nåden carries cornucopia, shield and flame (Svenska kyrkan).
  points=[];verts=[];steps=32;n=40
  for i in range(steps+1):
   t=i/steps;xx=24.42-.62*t*t;yy=v-.40-.18*(1-t)**2;zz=3.65+.90*t
   points.append(Vector((xx,yy,zz)))
  for i,pt in enumerate(points):
   t=i/steps;d=(points[min(i+1,steps)]-points[max(0,i-1)]).normalized();e=d.cross(Vector((0,1,0))).normalized();f=d.cross(e)
   r=.025+.33*t**1.5
   for k in range(n):
    aa=k*math.tau/n;rr=r*(1+.026*math.cos(12*aa))
    q=pt+rr*(e*math.cos(aa)+f*math.sin(aa));verts.append((cx+q.x,cy+q.y,q.z))
  m.faces(verts,[(i*n+k,i*n+(k+1)%n,(i+1)*n+(k+1)%n,(i+1)*n+k) for i in range(steps) for k in range(n)],GOLD,True)
  # Open mouth, rolled lip, and a shadowed inner bowl.
  pt=points[-1];d=(points[-1]-points[-2]).normalized();e=d.cross(Vector((0,1,0))).normalized();f=d.cross(e)
  curve(m,[tuple(pt+.355*(e*math.cos(i*math.tau/64)+f*math.sin(i*math.tau/64))) for i in range(65)],.033,GOLD)
  m.faces([(cx+q.x,cy+q.y,q.z) for q in [pt-d*.13+.29*(e*math.cos(i*math.tau/40)+f*math.sin(i*math.tau/40)) for i in range(40)]],[tuple(range(40))],MARBLE)
  for j in range(5):
   q=pt-d*.04+e*((j%3)-1)*.15+f*((j//3)-.5)*.16
   ellipsoid(m,q.x,q.y,q.z,.09,.085,.08,GOLD,20,12)
  ellipsoid(m,23.91,v+.34,4.03,.085,.39,.54,GOLD)
  curve(m,[(23.80,v+.34+.35*math.cos(i*math.tau/64),4.03+.49*math.sin(i*math.tau/64)) for i in range(65)],.025,GOLD)
  # Pentecost flame above the head, with a curved, tapering silhouette.
  for side in [-1,0,1]:
   curve(m,[(24.18-.05*math.sin(t*math.pi),v+side*.08*(1-t)+.08*math.sin(t*4),5.62+t*(.39 if side else .57)) for t in [j/20 for j in range(21)]],.035,GOLD)
 for j in range(7):leaf(m,24.0,v+(j-3)*.12,2.95,.15,.27,GOLD,'x',-1)
# Altar sarcophagus relief and carved moulded rails.
for j in range(13):rosette(m,24.11,-2.9+j*.48,2.18,.12,IVORY)
for z in [1.78,2.51]:box(m,24.08,0,z,.07,6.35,.06,GOLD)
m.v=[(x-2.5,y,z) for x,y,z in m.v]
# Pulpit eight framed blue-green panels, gold leaves, under-bowl fluting and canopy.
pulpit_detail_start=len(m.v)
for k in range(8):
 a=(k+.5)*math.tau/8;uu=8.1+1.24*math.cos(a);vv=6.3+1.24*math.sin(a)
 box(m,uu,vv,5.23,.07,.86,1.02,PULPIT,a)
 # Panel bosses on the outward side, not a generic blank cylinder.
 sphere(m,8.1+1.31*math.cos(a),6.3+1.31*math.sin(a),5.23,.12,GOLD)
 figure(m,8.1+1.30*math.cos(a),6.3+1.30*math.sin(a),4.84,.66,GOLD,yaw=a+math.pi)
 for j in range(3):
  aa=a+(j-1)*.11
  curve(m,[(8.1+( .35+.83*t)*math.cos(aa),6.3+(.35+.83*t)*math.sin(aa),3.53+.96*t) for t in [q/16 for q in range(17)]],.035,GOLD)
 for j in range(3):
  aa=a+(j-1)*.18
  rod(m,(8.1+.12*math.cos(aa),6.3+.12*math.sin(aa),9.38),(8.1+1.46*math.cos(aa),6.3+1.46*math.sin(aa),9.38),.025,GOLD)
 figure(m,8.1+1.32*math.cos(a),6.3+1.32*math.sin(a),9.60,.70,GOLD,pose="raised",yaw=a+math.pi)
# Carved scroll frames surround each pulpit panel, with small leafed pilasters.
for k in range(8):
 a=(k+.5)*math.tau/8;start=len(m.v)
 for side in [-1,1]:
  for j in range(3):leaf(m,9.45,6.3+side*.34,4.72+j*.31,.11,.28,GOLD,'x',1)
  curve(m,[(9.46,6.3+side*.20+.105*math.cos(t),5.71+.105*math.sin(t)) for t in [i*math.tau/32 for i in range(42)]],.024,GOLD)
 for zz in [4.64,5.82]:rod(m,(9.44,5.9,zz),(9.44,6.7,zz),.035,GOLD,12)
 turn_vertices(m,start,8.1,6.3,a)
 for j in range(5):
  aa=a+(j-2)*.105
  leaf(m,8.1+1.6*math.cos(aa),6.3+1.6*math.sin(aa),9.50,.105,.21,GOLD,'x',1)
figure(m,8.1,6.3,11.47,1.04,GOLD,'raised')
rod(m,(8.02,6.04,11.9),(8.02,6.04,13.0),.013,GOLD)
m.faces([(cx+8.02,cy+6.04,12.68),(cx+8.05,cy+6.49,12.73),(cx+8.04,cy+6.46,12.96),(cx+8.02,cy+6.04,12.94)],[(0,1,2,3)],IVORY)
figure(m,8.1,6.3,1.45,1.86,GOLD)
m.v[pulpit_detail_start:]=[(x+.45,y+1.60,z) for x,y,z in m.v[pulpit_detail_start:]]
m.finish()
# Interior plaster carving, gallery tracery and organ ornaments.
m=Mesh('SM_Domkyrka_Interior_Carving','Cathedral interior details')
for u in [-23,-10.6,10.6,23]:
 for v in [-7.9,7.9]:
  front=v+(.65 if v<0 else -.65)
  for j in range(7):leaf(m,u+(j-3)*.16,front,13.28,.17,.52,IVORY,'y',1 if v<0 else -1)
  curve(m,[(u+.66*math.cos(t*math.pi/32),front,13.56-.4*math.sin(t*math.pi/32)) for t in range(33)],.05,IVORY)
  rosette(m,u,front,13.24,.13,IVORY,'y')
# Curved openwork in each gallery bay.
for s in [-1,1]:
 for j in range(23):
  u=-8.4+j*.73
  curve(m,[(u+.30*math.cos(t*math.tau/40),s*11.10,7.54+.30*math.sin(t*math.tau/40)) for t in range(41)],.043,IVORY)
 for u in [-7.5,-4.5,-1.5,1.5,4.5,7.5]:
  capital(m,u,s*11.45,5.84,.4,.60,GOLD)
# West balcony ornaments follow its curved front; keep the openings real.
for v in [-6,-3,3,6]:
 u=gallery_front(v)-.38
 capital(m,u,v,5.84,.4,.60,GOLD)
for j in range(13):
 v=-6.6+j*1.1;u=gallery_front(v)+.23
 rosette(m,u,v,6.79,.075,GOLD)
# Organ facade: leaf scrolls, pipe toes, mouths, crest and a visible console.
for v,w,top in [(-4.8,2.6,13.2),(-2.8,1.35,15.1),(0,3.4,16.8),(2.8,1.35,15.1),(4.8,2.6,13.2)]:
 for s in [-1,1]:
  for j in range(8):leaf(m,-22.15,v+s*w*.43,9+j*(top-9)/8,.18,.39,GOLD,'x',1)
  pts=[]
  for i in range(50):
   a=i*math.tau/25;r=.44*(1-i/65);pts.append((-22.04,v+s*w*.41+r*math.cos(a),top+.34+r*math.sin(a)))
  curve(m,pts,.065,GOLD)
 rosette(m,-22.08,v,top+.3,.24,GOLD)
 count=max(5,int(w/.18))
 for i in range(count):
  vv=v-w*.38+i*w*.76/(count-1)
  m.lathe(cx-22.15,cy+vv,8.22,[(.022,0),(.025,.07),(.063,.28)],SILVER,12)
  box(m,-22.075,vv,8.86,.028,.077,.015,SILVER)
box(m,-21.20,0,7.67,.8,1.9,1.35,PEW)
for row in range(3):
 for key in range(51):
  v=-.82+key*.032
  box(m,-20.73+row*.065,v,7.59+row*.115,.26,.029,.025,IVORY)
  if key%7 in [0,1,3,4,5]:box(m,-20.81+row*.065,v+.014,7.62+row*.115,.14,.015,.032,IRON)
for s in [-1,1]:
 for j in range(12):sphere(m,-20.78,s*(.94+.055*(j%3)),7.48+.09*(j//3),.024,IVORY)
box(m,-20.28,0,7.36,.45,1.3,.11,WOOD)
for v in [-.5,.5]:box(m,-20.28,v,7.13,.09,.09,.43,WOOD)
m.finish()

# Modern blue baptismal font and choir organ, photographed in Koret_010.
BLUEFONT=mat('M_Font_Cobalt',(.015,.033,.18),.19,.50)
BOWL=mat('M_Font_Bowl',(.45,.63,.68),.12,.35)
m=Mesh('SM_Domkyrka_Choir_Furnishings','Cathedral interior details')
# Approximate pierced blue metal stem: individual irregular slots remain open.
u,v=12.9,-5.8
for k in range(8):
 a=k*math.tau/8
 rod(m,(u+.24*math.cos(a),v+.24*math.sin(a),1.34),(u+.24*math.cos(a),v+.24*math.sin(a),2.46),.021,BLUEFONT)
 for j in range(23):
  z=1.36+j*.047;aa=a+.025*math.sin(j*3+k)
  pts=[(u+.25*math.cos(aa+t*.52),v+.25*math.sin(aa+t*.52),z+.010*math.sin(t*math.pi*3+j)) for t in [i/8 for i in range(9)]]
  curve(m,pts,.012 if j>3 else .023,BLUEFONT)
m.lathe(cx+u,cy+v,2.35,[(.18,0),(.23,.06),(.34,.15),(.46,.20),(.48,.22),(.465,.235),(.43,.215),(.31,.15),(.20,.07)],BOWL,64)
# Small north-side choir organ: pale case, gold trim, two high outer pipe towers.
u,v=17.6,6.65
for du,w,top in [(-1.10,.75,6.4),(0,1.25,5.1),(1.10,.75,6.8)]:
 box(m,u+du,v,(2.0+top)/2,w,.72,top-2.0,IVORY)
 box(m,u+du,v-.43,(3.2+top)/2,w-.12,.05,top-3.2,MARBLE)
 for z in [2.1,3.18,top]:box(m,u+du,v-.44,z,w+.1,.12,.09,GOLD)
 for side in [-1,1]:box(m,u+du+side*w*.48,v-.45,(3.2+top)/2,.05,.13,top-3.2,GOLD)
 for j in range(7):
  xx=u+du-w*.36+j*w*.72/6;hh=top-3.40-.34*abs(j-3)/3
  m.cylinder(cx+xx,cy+v-.50,3.33,.044,hh,SILVER,12)
  box(m,xx,v-.547,3.55,.049,.016,.055,IRON)
 for j in range(4):leaf(m,u+du+(j-1.5)*w*.19,v-.52,top-.50,.14,.39,GOLD,'y',-1)
 rosette(m,u+du,v-.48,top+.20,.17,GOLD,'y')
box(m,u,v-.59,2.47,1.03,.26,.08,IVORY)
for j in range(39):box(m,u-.47+j*.024,v-.66,2.53,.021,.20,.018,IVORY)
for j in range(15):box(m,u-.49+j*.07,v-.54,1.45,.036,.62,.032,WOOD)
# Communion rail, candle stands and modest movable choir seating.
for side in [-1,1]:
 pts=[(16.1+2.7*math.sin(t*math.pi/2),side*(1.9+4.4*t),2.55) for t in [i/36 for i in range(37)]]
 curve(m,pts,.032,GOLD)
 for j in range(7):
  t=j/6;xx=16.1+2.7*math.sin(t*math.pi/2);yy=side*(1.9+4.4*t)
  rod(m,(xx,yy,1.66),(xx,yy,2.55),.025,GOLD)
for vv in [-1.1,1.1]:
 m.lathe(cx+13.6,cy+vv,3.03,[(.10,0),(.05,.08),(.028,.42),(.07,.45)],GOLD,20)
 m.cylinder(cx+13.6,cy+vv,3.48,.035,.25,IVORY,16)
for j in range(5):
 for side in [-1,1]:
  uu=20+j*.65;vv=side*5.0
  box(m,uu,vv,2.05,.49,.49,.09,WOOD)
  box(m,uu,vv+side*.23,2.38,.49,.075,.65,WOOD)
  box(m,uu,vv,2.115,.43,.43,.04,BURGUNDY)
  for dx in [-.18,.18]:
   for dy in [-.18,.18]:box(m,uu+dx,vv+dy,1.81,.045,.045,.50,WOOD)
m.finish()

exec(compile((R/'scripts/build_ionic_details.py').read_text(),str(R/'scripts/build_ionic_details.py'),'exec'))
