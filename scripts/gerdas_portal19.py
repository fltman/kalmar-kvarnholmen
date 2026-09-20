"""Continuous carved profiles and inset timber joinery for Castenska garden.

Shapes are estimated from the referenced exterior photographs, not measured
sculpture. Keep this helper local to Gerdas; shared facade modules are unchanged.
Executed by build_pass18_gerdas.py with its mesh and facade coordinate frame.
"""
stone = 'M_Portal19_Stone'

def g19_ring(u,z,rx,rz,out,r,ma):
 # One joined sweep prevents the bead-like joints of individual capped rods.
 verts=[];n=128;sides=10
 for i in range(n):
  t=math.tau*i/n
  for j in range(sides):
   q=math.tau*j/sides
   verts.append(lp(x,y,u+(rx+r*math.cos(q))*math.cos(t),out+r*math.sin(q),z+(rz+r*math.cos(q))*math.sin(t),a))
 faces=[(i*sides+j,i*sides+(j+1)%sides,((i+1)%n)*sides+(j+1)%sides,((i+1)%n)*sides+j) for i in range(n) for j in range(sides)]
 m.faces(verts,faces,ma,True)

def g19_arch(u,z,rx,rz,profile,ma):
 # Connected cross sections: radial offset and facade depth, with real reveals.
 n=64;s=len(profile)
 verts=[lp(x,y,u+(rx+dr)*math.cos(math.pi*i/n),out,z+(rz+dr)*math.sin(math.pi*i/n),a) for i in range(n+1) for dr,out in profile]
 faces=[(i*s+j,i*s+(j+1)%s,(i+1)*s+(j+1)%s,(i+1)*s+j) for i in range(n) for j in range(s)]
 faces += [tuple(range(s-1,-1,-1)),tuple(range(n*s,(n+1)*s))]
 m.faces(verts,faces,ma,True)

def g19_sphere(u,out,z,sx,sy,sz,ma):
 n=32;steps=20
 verts=[lp(x,y,u+sx*math.sin(math.pi*j/steps)*math.cos(math.tau*i/n),out+sy*math.sin(math.pi*j/steps)*math.sin(math.tau*i/n),z+sz*math.cos(math.pi*j/steps),a) for j in range(steps+1) for i in range(n)]
 m.faces(verts,[(j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i) for j in range(steps) for i in range(n)],ma,True)

def g19_loft(u,profile,ma):
 # Chamfered rectangular section, smoothly sampled along the carved profile.
 section=[(-1,-.06),(-.86,0),(.86,0),(1,-.06),(1,-.22),(-1,-.22)]
 n=len(section)
 verts=[lp(x,y,u+s*width/2,depth+o,z,a) for z,width,depth in profile for s,o in section]
 faces=[(j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i) for j in range(len(profile)-1) for i in range(n)]
 faces += [tuple(range(n-1,-1,-1)),tuple(range((len(profile)-1)*n,len(profile)*n))]
 m.faces(verts,faces,ma,True)

def g19_glazing(u,b,w,h,r,door=False):
 # Glass sits behind a deep timber reveal; the lining closes the entire arch.
 spring=b+h
 contour=[(-w/2,b),(w/2,b)]+[(w/2*math.cos(k*math.pi/64),spring+r*math.sin(k*math.pi/64)) for k in range(65)]
 m.faces([lp(x,y,u+q,.065,z,a) for q,z in contour],[tuple(range(len(contour)))],GLAZE)
 profile=[(-.075,.07),(-.075,.35),(-.045,.39),(.008,.39),(.025,.35),(.025,.07)]
 g19_arch(u,spring,w/2,r,profile,WOOD)
 for sign in [-1,1]:
  facade_box(m,x,y,u+sign*(w/2-.025),.225,b+h/2,.10,.32,h,WOOD,a)
 facade_box(m,x,y,u,.23,b,w,.32,.09,WOOD,a)
 if not door:
  facade_box(m,x,y,u,.39,b-.09,w+.25,.50,.12,stone,a)
  return
 # A glazed single timber leaf, lower raised panels and a separate fanlight.
 for side in [-1,1]:facade_box(m,x,y,side*.68,.145,1.65,.115,.12,2.54,WOOD,a)
 for zz,hh in [(.44,.15),(1.06,.13),(2.76,.18)]:facade_box(m,x,y,0,.145,zz,1.34,.12,hh,WOOD,a)
 for u in [-.325,.325]:
  facade_box(m,x,y,u,.11,.76,.52,.06,.43,WOOD,a)
  town_border(m,*lp(x,y,u,0,0,a)[:2],.76,.53,.44,a,WOOD,.18,.035)
 facade_box(m,x,y,0,.15,.76,.07,.13,.57,WOOD,a)
 facade_box(m,x,y,0,.19,2.82,1.44,.19,.09,WOOD,a)
 for zz in [.77,2.36]:
  facade_box(m,x,y,-.66,.22,zz,.035,.055,.17,IRON,a)
 facade_box(m,x,y,.59,.225,1.40,.075,.025,.23,IRON,a)
 town_path(m,[lp(x,y,.59,.25,1.32,a),lp(x,y,.59,.32,1.32,a),lp(x,y,.59,.32,1.48,a),lp(x,y,.59,.25,1.48,a)],.012,GOLD)
 # Fine perimeter of the glazed leaf keeps the glass visibly recessed.
 town_border(m,x,y,1.88,1.12,1.49,a,WOOD,.205,.028)

for u in [-4.65,-2.32,2.32,4.65]:g19_glazing(u,.64,1.48,2.52,.74)
g19_glazing(0,.34,1.58,2.62,.79,True)

# Wave-cut pilasters: continuous surfaces, foot plinths, moulded capitals.
for sign in [-1,1]:
 u=sign*1.08
 profile=[(.48+2.57*k/224,.36+.018*math.cos(math.tau*7*k/224),.48+.048*math.cos(math.tau*7*k/224)) for k in range(225)]
 g19_loft(u,profile,stone)
 g19_loft(u,[(.28,.53,.54),(.43,.53,.54),(.48,.41,.49),(.53,.38,.49)],stone)
 g19_loft(u,[(3.03,.39,.49),(3.10,.48,.54),(3.17,.51,.57),(3.24,.61,.59),(3.34,.64,.59),(3.38,.55,.56)],stone)
 # Neck and pedestal touch both the capital and the finial.
 g19_loft(u,[(3.37,.34,.49),(3.44,.24,.49),(3.55,.105,.49),(3.58,.105,.49)],stone)
 g19_sphere(u,.43,3.80,.245,.235,.245,stone)
 # Low relief acanthus curls on the arch shoulder.
 town_scroll(m,*lp(x,y,sign*.91,.21,0,a)[:2],4.08,a,sign,.50,.39,stone)

g19_arch(0,2.96,.79,.79,[(0,.16),(0,.42),(.025,.48),(.25,.48),(.28,.41),(.28,.16)],stone)
# Oval sits above the keystone instead of intersecting the arch or lettering.
cart_z=4.65;cart_rx=1.01;cart_rz=.57
verts=[lp(x,y,cart_rx*math.cos(t*math.tau/128),.455,cart_z+cart_rz*math.sin(t*math.tau/128),a) for t in range(128)]
m.faces(verts,[tuple(range(128))],stone)
g19_ring(0,cart_z,1.045,.605,.47,.045,stone)
g19_ring(0,cart_z,.97,.535,.48,.012,stone)
for txt,z,w in [('CHRISTIAN CERSTEN',4.85,1.68),('ANNA HERMANSDOTTER',4.64,1.82),('ANNO 1667',4.42,1.19)]:town_text(m,*lp(x,y,0,.47,0,a)[:2],z,a,txt,w,stone)
assert 4.42-.11 > 2.96+.79+.28  # lowest lettering clear of stone arch
g19_loft(0,[(5.22,.46,.47),(5.25,.52,.49),(5.30,.37,.47),(5.42,.36,.47),(5.46,.61,.55),(5.55,.63,.56),(5.58,.45,.51),(5.68,.13,.48)],stone)
g19_sphere(0,.43,5.90,.24,.23,.24,stone)

# Small stylised carved mask on the keystone, modelled relief, not a decal.
town_polyprofile(m,*lp(x,y,0,.47,0,a)[:2],3.90,[(-.13,-.09),(.13,-.09),(.18,.24),(-.18,.24)],a,stone,.13,False)
g19_sphere(0,.49,3.98,.12,.057,.14,stone)
for sign in [-1,1]:
 g19_sphere(sign*.062,.55,4.02,.046,.029,.023,stone)
 g19_sphere(sign*.065,.55,3.945,.050,.024,.038,stone)
 town_path(m,[lp(x,y,sign*.005,.57,3.96,a),lp(x,y,sign*.042,.57,3.93,a),lp(x,y,sign*.088,.55,3.94,a)],.014,stone)
g19_sphere(0,.57,3.99,.025,.040,.056,stone)
town_rod(m,lp(x,y,-.045,.553,3.903,a),lp(x,y,.045,.553,3.903,a),.009,stone)
for k in range(2):facade_box(m,x,y,0,.60+k*.31,(2-k)*.085,2.04,.72,(2-k)*.17,stone,a)
