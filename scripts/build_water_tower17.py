"""Gamla vattentornet: photo-informed brick shaft, stone corbels and crenellated crown.
Height: museum/OSM 65m; detailed dimensions and hidden elevations remain estimates.
"""
name='SM_Kvarnholmen_House_91072716'
old=bpy.data.objects.get(name)
if old:bpy.data.objects.remove(old,do_unlink=True)
m=Mesh(name,'Kvarnholmen/Completed facades');cx,cy=-331.32,122.45;BR='M_Landmark_BrickRed';AS='M_Landmark_Ashlar';FR=town_mats['PaintGreen'];count=0
# Forty-eight facets keep the round silhouette; sixteen vertical strips of narrow openings.
for level in range(15):
 z0=level*4.05;z1=(level+1)*4.05
 radius=6.55-(min(z0,43.0)/43.0)*.78 if z0<44.55 else 6.45
 for j in range(48):
  t=j*math.tau/48;tt=(j+1)*math.tau/48;P=(cx+radius*math.cos(t),cy+radius*math.sin(t));Q=(cx+radius*math.cos(tt),cy+radius*math.sin(tt));x,y,L,a=sf_edge(P,Q);x,y,_=lp(x,y,0,-.35,0,a);holes=[]
  if j%3==1 and level not in [10,14]:holes=[(0,z0+.74,.43,2.35,'window')]
  if j==37 and level==0:holes=[(0,.13,.76,2.72,'door')]
  d17_wall(m,x,y,L,a,z0,z1,holes,BR)
  for u,z,w,h,k in holes:
   if k=='door':town_door(m,x,y,z,w,h,a,FR)
   else:
    sf_modern(m,x,y,0,z,w,h,a,FR,BR,1,1);count+=1
    facade_box(m,x,y,0,.388,z-.11,w+.15,.07,.14,AS,a)
  # Slender continuous vertical brick ribs articulate the shaft.
  if j%3==0 and level>1:facade_box(m,x,y,-L/2+.04,.40,(z0+z1)/2,.10,.14,z1-z0,BR,a)
# Stone string courses and the wide reservoir support ring, seated against the shaft.
for z,r,h in [(1.0,6.59,.23),(7.85,6.48,.28),(24.1,6.20,.22),(32.20,6.05,.22),(40.30,5.88,.22),(44.48,6.40,.35),(47.90,6.53,.21),(53.75,6.53,.30),(60.55,6.59,.32)]:
 m.lathe(cx,cy,z,[(r-.13,0),(r,0),(r,h),(r-.13,h)],AS,96)
for j in range(32):
 t=j*math.tau/32;x,y=cx+5.77*math.cos(t),cy+5.77*math.sin(t);a=t+math.pi/2
 outline=[(-.22,0),(.22,0),(.25,.38),(.31,.84),(.38,1.22),(.33,1.49),(-.33,1.49),(-.38,1.22),(-.31,.84),(-.25,.38)]
 xx,yy,_=lp(x,y,0,.55,0,a);town_polyprofile(m,xx,yy,43.1,outline,a,AS,.62,False)
# Weatherproof roof inside the parapet; crenellations and stone coping above it.
m.cylinder(cx,cy,60.85,6.42,.15,METAL,96)
for j in range(48):
 t=j*math.tau/48;x,y=cx+6.45*math.cos(t),cy+6.45*math.sin(t);a=t+math.pi/2
 facade_box(m,x,y,0,0,61.22,.85,.27,.60,BR,a)
 if j%2==0:
  facade_box(m,x,y,0,0,61.94,.29,.40,1.02,BR,a);facade_box(m,x,y,0,0,62.48,.40,.50,.13,AS,a)
  town_polyprofile(m,x,y,62.54,[(-.2,0),(.2,0),(0,.25)],a,AS,.28,False)
 else:facade_box(m,x,y,0,0,61.53,.82,.39,.12,AS,a)
for j in range(6):
 t=j*math.tau/6;x,y=cx+4.9*math.cos(t),cy+4.9*math.sin(t);town_rod(m,(x,y,60.95),(x,y,65),.035,TW,8)
obj=m.finish();obj['osm_id']='91072716';obj['detail_pass']=17;obj['eaves_height']=60.85;obj['massing_only']=False;obj['reference_status']='photographed water tower; height museum/OSM, details visually estimated'
district17_audit[name]={'windows':count,'doors':1,'frontages':16,'rear_segments':0,'roof':'sealed circular roof and stone/brick crown','reference_status':obj['reference_status'],'street':'Västra Vallgatan','reference':'https://www.kalmarkusten.se/platser/kalmar-gamla-vattentorn/'}
district17_cameras.append(('76_Gamla_Vattentornet',(cx-43,cy-33,3),(cx,cy,33),24))
