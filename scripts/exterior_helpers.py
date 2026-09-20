"""Cathedral exterior construction from the south elevation and photo references.
Dimension estimates preserve the existing traversable shell and church interior.
"""
CHURCHSTONE=mat('M_Church_Cut_Stone',(.43,.415,.365),.68,texture='ChurchCutStone')
CHURCHFRAME=mat('M_Church_Window_Frame',(.26,.285,.235),.43,texture='ChurchWindowPaint')
CHURCHGLASS=mat('M_Church_Window_Glass',(.08,.12,.135),.17,.10,texture='ChurchWindowGlass')
CHURCHSHUTTER=mat('M_Church_Lantern_Shutter',(.035,.055,.048),.64)

CHURCHCOPPER=mat('M_Church_Copper',(.082,.205,.158),.75,.15,texture='ChurchCopperFine')
CHURCHROOF=mat('M_Church_Roof',(.052,.062,.054),.68,.20,texture='ChurchRoofFine')
CHURCHPIER=mat('M_Church_Pier_Stone',(.405,.371,.305),.72,texture='ChurchPierStone')
CHURCHURN=mat('M_Church_Urn',(.052,.062,.054),.64,.30,texture='ChurchRoofFine')

def ext_tube(m,points,r,ma,n=8):
 pts=[Vector(p) for p in points];verts=[];previous=None
 for i,p in enumerate(pts):
  tangent=(pts[min(i+1,len(pts)-1)]-pts[max(0,i-1)]).normalized()
  if previous is None:
   seed=Vector((0,1,0)) if abs(tangent.y)<.95 else Vector((1,0,0))
  else:seed=previous
  e=(seed-tangent*seed.dot(tangent)).normalized();previous=e;f=tangent.cross(e)
  for k in range(n):verts.append(tuple(p+r*(e*math.cos(k*math.tau/n)+f*math.sin(k*math.tau/n))))
 faces=[(i*n+k,i*n+(k+1)%n,(i+1)*n+(k+1)%n,(i+1)*n+k) for i in range(len(pts)-1) for k in range(n)]
 faces += [tuple(range(n-1,-1,-1)),tuple(range((len(pts)-1)*n,len(pts)*n))]
 m.faces(verts,faces,ma,True)

def church_window(m,x,y,z,w,h,angle=0,arched=False,trim=None,grids=2,arch_rise=None):
 trim=trim or CHURCHSTONE;c,s=math.cos(angle),math.sin(angle)
 def pos(u,depth,zz):return (x+u*c+depth*s,y+u*s-depth*c,zz)
 def block(u,depth,zz,ww,dd,hh,ma):m.box(pos(u,depth,zz),(ww,dd,hh),ma,angle)
 bottom=z-h/2;top=z+h/2;rise=(w*.15 if arch_rise is None else arch_rise) if arched else 0
 # Glass sits behind a stepped frame; the wall shell remains unchanged.
 block(0,.09,z,w,.08,h,CHURCHGLASS)
 for offset,width,depth in [(.16,.11,.20),(.045,.055,.245)]:
  for u in [-w/2-offset,w/2+offset]:block(u,depth,z,.12 if offset>.1 else .065,.12,h+.22,trim)
  block(0,depth,bottom-offset,w+offset*2+.12,.16,width,trim)
 if arched:
  # Segmental, not semicircular: the high central window has a shallow head.
  vs=[pos(-w/2,.14,top),pos(w/2,.14,top)]+[pos(w/2*math.cos(i*math.pi/48),.14,top+rise*math.sin(i*math.pi/48)) for i in range(1,48)]
  m.faces(vs,[tuple(range(len(vs)))],CHURCHGLASS)
  for offset,radius in [(.18,.075),(.065,.028)]:
   ext_tube(m,[pos((w/2+offset)*math.cos(i*math.pi/64),.26,top+(rise+offset)*math.sin(i*math.pi/64)) for i in range(65)],radius,trim,10)
  block(0,.25,top+rise+.35,w+.75,.40,.12,trim)
  block(0,.22,top+rise+.46,w+.87,.44,.075,trim)
  # Keystone is a shallow trapezoid aligned with the arched surround.
  verts=[pos(u,d,zz) for d in [.26,.40] for u,zz in [(-.15,top+rise-.04),(.15,top+rise-.04),(.23,top+rise+.30),(-.23,top+rise+.30)]]
  m.faces(verts,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],trim)
 else:
  for off,ww,hh in [(0,w+.40,.13),(.095,w+.48,.06)]:block(0,.23,top+.08+off,ww,.25,hh,trim)
 # Outer sash and fine small-pane divisions, with stronger structural crossbars.
 for u in [-w/2+.025,w/2-.025]:block(u,.22,z,.062,.072,h,CHURCHFRAME)
 for zz in [bottom+.026,top-.026]:block(0,.22,zz,w,.072,.060,CHURCHFRAME)
 cols=6 if w>=1.55 else 4;rows=max(3,round(h/.40))
 for i in range(1,cols):
  u=-w/2+w*i/cols;extra=rise*math.sqrt(max(0,1-(u/(w/2))**2))
  block(u,.235,z+extra/2,.059 if i==cols//2 else .020,.061,h+extra,CHURCHFRAME)
 for j in range(1,rows):block(0,.234,bottom+h*j/rows,w,.055,.020,CHURCHFRAME)
 if h>3:
  for t in [.35,.70]:block(0,.253,bottom+h*t,w,.087,.067,CHURCHFRAME)
 # Sloped projecting sill and a lower drip edge.
 block(0,.28,bottom-.17,w+.46,.38,.12,trim)
 block(0,.32,bottom-.235,w+.51,.42,.045,trim)

def church_roundwindow(m,x,y,z,r,angle=0,clock=False):
 c,s=math.cos(angle),math.sin(angle)
 def p(u,depth,zz):return(x+u*c+depth*s,y+u*s-depth*c,z+zz)
 n=64
 for rr,d,ma in [(r+.12,.08,CHURCHSTONE),(r,.14,CHURCHSHUTTER if clock else CHURCHGLASS)]:
  m.faces([p(rr*math.cos(i*math.tau/n),d,rr*math.sin(i*math.tau/n)) for i in range(n)],[tuple(range(n))],ma)
 for rr,rad in [(r+.11,.062),(r+.015,.022)]:ext_tube(m,[p(rr*math.cos(i*math.tau/n),.20,rr*math.sin(i*math.tau/n)) for i in range(n+1)],rad,CHURCHSTONE,10)
 if clock:
  for i in range(12):
   a=i*math.tau/12
   for delta in [-.022,.022]:ext_tube(m,[p(rr*math.sin(a+delta),.225,rr*math.cos(a+delta)) for rr in [r*.75,r*.89]],r*.010,GOLD,6)
  ext_tube(m,[p(0,.24,0),p(r*.05,.24,r*.65)],r*.020,GOLD,8)
  ext_tube(m,[p(0,.25,0),p(r*.46,.25,-r*.18)],r*.028,GOLD,8)
 else:
  for i in range(12):
   a=i*math.tau/12
   ext_tube(m,[p(rr*math.cos(a),.21,rr*math.sin(a)) for rr in [r*.25,r*.96]],.018,CHURCHFRAME,6)
  for rr in [r*.26,r*.67]:ext_tube(m,[p(rr*math.cos(i*math.tau/n),.21,rr*math.sin(i*math.tau/n)) for i in range(n+1)],.024,CHURCHFRAME,8)

def copper_lantern(m,x,y):
 # Chamfered square lantern and an ogee cap. Eight planar faces preserve the
 # octagonal silhouette instead of the previous circular umbrella-like skirt.
 footprint=[(-1,-.42),(-.42,-1),(.42,-1),(1,-.42),(1,.42),(.42,1),(-.42,1),(-1,.42)]
 profile=[(3.58,22.90),(3.60,23.03),(3.22,23.17),(2.47,23.52),(2.40,23.62),(2.40,25.57),(2.58,25.62),(2.62,25.73)]
 # Smooth ogee meridian; ring outline stays eight-sided.
 for i in range(1,33):
  t=i/32;radius=.47+2.15*(1-t)**1.1+.17*math.sin(t*math.tau)
  profile.append((radius,25.73+2.69*t))
 profile += [(.48,28.56),(.55,28.64),(.55,28.77),(.36,28.88),(.34,29.40),(.46,29.51),(.44,29.62)]
 verts=[(x+r*u,y+r*v,z) for r,z in profile for u,v in footprint]
 faces=[tuple(range(7,-1,-1))]+[(j*8+k,j*8+(k+1)%8,(j+1)*8+(k+1)%8,(j+1)*8+k) for j in range(len(profile)-1) for k in range(8)]+[tuple(range((len(profile)-1)*8,len(profile)*8))]
 m.faces(verts,faces,COPPER,True)
 # Standing seams follow the modeled cap and skirt.
 for u,v in footprint:
  for indices in [range(0,5),range(7,len(profile))]:
   ext_tube(m,[(x+(profile[j][0]+.018)*u,y+(profile[j][0]+.018)*v,profile[j][1]+.01) for j in indices],.024,COPPER,6)
 # Oval louvres on the four principal faces, copper rims and horizontal slats.
 for a in [0,math.pi/2,math.pi,math.pi*1.5]:
  nx,ny=math.sin(a),-math.cos(a);tx,ty=math.cos(a),math.sin(a)
  def pp(u,zz,depth=.018):return (x+nx*(2.4+depth)+tx*u,y+ny*(2.4+depth)+ty*u,24.61+zz)
  m.faces([pp(.47*math.cos(i*math.tau/64),.76*math.sin(i*math.tau/64)) for i in range(64)],[tuple(range(64))],CHURCHSHUTTER)
  for j in range(-6,7):
   zz=j*.10;ww=.44*math.sqrt(max(0,1-(zz/.72)**2))
   ext_tube(m,[pp(-ww,zz,.032),pp(ww,zz,.032)],.025,CHURCHSHUTTER,6)
  for radius in [1,1.13]:ext_tube(m,[pp(.47*radius*math.cos(i*math.tau/64),.76*radius*math.sin(i*math.tau/64),.055) for i in range(65)],.030,COPPER,8)

def roof_seams(m):
 for sign in [-1,1]:
  for k in range(1,30):
   yy=k*.60;extent=11.35*min(1,yy/8.3)
   for side in [-1,1]:ext_tube(m,[(cx+side*extent*t,cy+sign*yy,27.8-4*extent*t/11.35+.025) for t in [0,1]],.018,DARKROOF,6)
  for k in range(1,43):
   xx=k*.60;extent=8.3*min(1,xx/11.35)
   for side in [-1,1]:ext_tube(m,[(cx+sign*xx,cy+side*extent*t,27.8-4*extent*t/8.3+.025) for t in [0,1]],.018,DARKROOF,6)

def facade_finial(m,x,y,z,scale=1):
 # Profiled dark urn with a small gilt flame, on a stepped stone pedestal.
 for dz,w,h in [(0,.84,.16),(.23,.62,.32),(.43,.91,.12)]:
  m.box((x,y,z+dz*scale),(w*scale,w*scale,h*scale),CHURCHSTONE)
 profile=[(.23,.49),(.23,.55),(.15,.61),(.18,.67),(.31,.83),(.32,1.03),(.22,1.24),(.14,1.32),(.13,1.59),(.20,1.66),(.20,1.75)]
 m.lathe(x,y,z,[(r*scale,h*scale) for r,h in profile],CHURCHURN,32)
 for j in [-1,0,1]:
  for k in range(12):
   t=k/11;rr=(.065*(1-t)+.008)*scale
   m.cylinder(x+j*.066*scale*(1-t),y+.03*scale*math.sin(t*4),z+(1.75+t*(.35 if j else .48))*scale,rr,.05*scale,GOLD,8,r2=rr*.8)

def curved_roof_seams(m):
 # True longitudinal seams follow each sampled curved side roof.
 for sx in [-1,1]:
  for sy in [-1,1]:
   for k in range(24):
    x=cx+sx*(11.25+k*.60);outer=footprint_y_at(x)[0 if sy<0 else 1]
    points=[]
    for j in range(49):
     t=.01+.98*j/48;y=(cy+sy*8)*(1-t)+outer*t
     points.append((x,y,13.35+9.95*(1-t)**.60+.025))
    ext_tube(m,points,.014,DARKROOF,6)

def facade_band(m,x,y,z,length,angle=0):
 # A closed cyma profile, extruded continuously along the facade.
 c,s=math.cos(angle),math.sin(angle)
 profile=[(.20,-.18),(.45,-.18),(.45,-.13),(.52,-.13)]
 profile += [(.52+.16*(.5-.5*math.cos(t*math.pi)),-.13+.24*t) for t in [j/12 for j in range(1,13)]]
 profile += [(.78,.11),(.78,.17),(.81,.17),(.81,.23),(.20,.23)]
 n=len(profile);verts=[(x+u*c+d*s,y+u*s-d*c,z+h) for u in [-length/2,length/2] for d,h in profile]
 m.faces(verts,[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],CHURCHSTONE)

def exterior_ionic(m,x,y,z,angle=0):
 c,s=math.cos(angle),math.sin(angle)
 def p(u,depth,h):return(x+u*c+depth*s,y+u*s-depth*c,z+h)
 m.box(p(0,.36,.18),(1.18,.40,.10),CHURCHSTONE,angle)
 m.box(p(0,.35,-.07),(.91,.28,.14),CHURCHSTONE,angle)
 for side in [-1,1]:
  centre=side*.44;n=48
  verts=[p(centre+.19*math.cos(i*math.tau/n),dep,.19*math.sin(i*math.tau/n)) for dep in [.27,.49] for i in range(n)]
  m.faces(verts,[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],CHURCHSTONE)
  ext_tube(m,[p(centre+.166*(1-t)*math.cos(side*t*math.tau*1.3),.51,.166*(1-t)*math.sin(side*t*math.tau*1.3)) for t in [i/64 for i in range(65)]],.018,CHURCHSTONE,8)
 for i in range(-2,3):
  ext_tube(m,[p(i*.12+.039*math.cos(t),.47,.09*math.sin(t)) for t in [j*math.tau/32 for j in range(33)]],.016,CHURCHSTONE,8)
