"""Facade cornices and the south portal, interpreted from contemporary photos.
Executed inside the exterior details mesh. No conjectural inscription is added.
"""
for sign in [-1,1]:
 angle=0 if sign<0 else math.pi;y=25.85 if sign<0 else 62.9
 for z,w in [(11.89,22.6),(13.12,23.15)]:facade_band(m,cx,y,z,w,angle)
 upper=cy+sign*17.55
 for z in [23.20,23.64]:facade_band(m,cx,upper,z,23.25,angle)
 for u in [-10.3,-4,4,10.3]:
  exterior_ionic(m,cx+u,upper,22.98,angle)
  for z,w,h in [(13.74,.98,.08),(13.87,.84,.12),(22.68,.89,.08)]:
   box(m,u,sign*17.55,z,w,.74,h,STONE)
 for u in [-14.4,14.4]:
  tower_y=cy+sign*16.4
  for z in [22.36,22.76]:facade_band(m,cx+u,tower_y,z,7.18,angle)
  for dx in [-3,3]:exterior_ionic(m,cx+u+dx,tower_y,22.12,angle)
 for u in [-11.65,11.65]:facade_finial(m,cx+u,cy+sign*17.58,18.54,.69)
 for u in [-10.5,-6,6,10.5]:
  # Torus/scotia-like steps at the foot of the stone piers.
  for z,w,d,h in [(1.57,1.21,.83,.11),(1.70,1.09,.77,.07),(2.02,.89,.64,.06),(11.50,1.02,.71,.09),(11.62,1.13,.81,.08)]:box(m,u,y-cy,z,w,d,h,STONE)

# Continuous fine coping and drip courses around the measured lower perimeter.
for i,(ax,ay) in enumerate(p):
 bx,by=p[(i+1)%len(p)];length=math.hypot(bx-ax,by-ay)
 if length<.4:continue
 facade_band(m,(ax+bx)/2,(ay+by)/2,12.97,length,math.atan2(by-ay,bx-ax))

v=-18.86
# Portal cornice: layered projecting flat slab with an ogee underside.
facade_band(m,cx,cy+v,6.79,6.08)
for u in [-2.25,2.25]:
 for k in range(12):
  start=len(m.v);a=k*math.tau/12
  leaf(m,u+.34,v,5.80,.17,.30,STONE,'x',1)
  turn_vertices(m,start,u,v,a)
 for z,rad in [(1.57,.45),(1.68,.37),(5.79,.35),(6.13,.43)]:
  m.lathe(cx+u,cy+v,z,[(rad,0),(rad,.047)],STONE,32)

def portal_relief(outline,depth,thickness,ma):
 n=len(outline);verts=[(cx+x,cy+v-d,z) for d in [depth,depth+thickness] for x,z in outline]
 m.faces(verts,[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],ma)

# A filled shaped panel over the lintel. The inscription cannot be resolved
# from the selected images, so its field remains plain instead of fabricated text.
outline=[(-1.54,5.74),(-1.54,6.27),(-1.13,6.27),(-1.02,6.40),(1.02,6.40),(1.13,6.27),(1.54,6.27),(1.54,5.74),(1.13,5.74),(1.02,5.63),(-1.02,5.63),(-1.13,5.74)]
portal_relief(outline,.38,.11,STONE)
ext_tube(m,[(cx+x,cy+v-.515,z) for x,z in outline+[outline[0]]],.027,STONE,8)
for side in [-1,1]:
 for j in range(3):leaf(m,side*(1.59+j*.12),v-.49,5.87,.14,.24,STONE,'y',-1)

# Low stone pedestal, dark cartouche, modeled mirrored C / XI cipher and crown.
# Svenska kyrkan identifies Karl XI's cipher here; the carving is approximate.
portal_relief([(-1.42,6.98),(-1.06,7.10),(-.77,7.48),(.77,7.48),(1.06,7.10),(1.42,6.98)],.12,.37,STONE)
for z,w in [(6.97,2.85),(7.10,2.36),(7.46,1.70)]:box(m,0,v-.33,z,w,.46,.065,STONE)
outline=[(-.64,7.48),(-.63,7.75),(-.45,7.90),(.45,7.90),(.63,7.75),(.64,7.48)]
portal_relief(outline,.26,.19,CHURCHURN)
for side in [-1,1]:
 points=[]
 for i in range(65):
  t=.25+1.50*i/64;a=math.pi*t
  points.append((cx+side*(.09+.125*math.cos(a)),cy+v-.485,7.67+.145*math.sin(a)))
 ext_tube(m,points,.018,GOLD,8)
for a,b in [((-.063,7.58),(.042,7.77)),((-.063,7.77),(.042,7.58)),((.097,7.58),(.097,7.77))]:
 ext_tube(m,[(cx+x,cy+v-.495,z) for x,z in [a,b]],.012,GOLD,8)
for off in [-.16,0,.16]:
 ext_tube(m,[(cx+off*(1-t),cy+v-.40,7.93+.17*math.sin(t*math.pi/2)) for t in [i/20 for i in range(21)]],.023,GOLD,8)
box(m,0,v-.40,7.93,.42,.10,.055,GOLD)
ext_tube(m,[(cx,cy+v-.40,8.08),(cx,cy+v-.40,8.21)],.016,GOLD,8)
ext_tube(m,[(cx-.045,cy+v-.40,8.16),(cx+.045,cy+v-.40,8.16)],.014,GOLD,8)
