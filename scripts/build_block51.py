"""Pass 51: the Ölandsgatan range of the district volume 92379292, north side, from the Kaggensgatan
corner to pass 48:
- Kronan, the white stone house on the corner with its gable to the street: sandstone quoins, two
  tall ground-floor windows with cellar lights, a boarded door with a menu case, two upper windows,
  wall anchors, and in the gable a boarded hatch and a round opening under the apex;
- the low range: a blank limewashed wall with a heavy cornice, a segmental carriage arch with its
  boarded leaves open, and a door up a step;
- the old stone house: a half gable rising east to the party wall with pass 48, one window with a
  cellar hatch below, and a small window high in the gable.
The rest of the block keeps its district height.

References: Google Street View April 2025 (three panoramas chained on shared window and door edges,
anchored on the Kaggensgatan corner and pass 48's joint; two views tilted up for the gables), view
only. Zones: source/block51.json; see references/block51-notes.md. The signs, the menu board and the
street lamp are omitted.
"""
B51D=json.loads((R/'source/block51.json').read_text());Z=B51D['zones']
block51_names=[];B51={}
for old in [k for k in list(materials) if k.startswith('M_Block51_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Lime','TownIvory',(.93,.92,.88),.92,0),
 ('Quoin','TownStone',(.78,.67,.57),.86,0),
 ('Plinth','TownStone',(.56,.56,.55),.88,0),
 ('White','TownIvory',(.95,.95,.93),.84,0),
 ('GreyFrame','TownPaintWhite',(.45,.48,.50),.55,0),
 ('Boards','TownPaintBrown',(.36,.34,.31),.70,0),
 ('Hatch','TownPaintBrown',(.42,.30,.22),.75,0),
 ('Tile','TownTileRed',(.70,.38,.26),.80,0),
 ('Iron','TownMetalGrey',(.08,.08,.085),.45,.40),
 ('Dark','TownMetalGrey',(.05,.055,.06),.40,.20),
 ]:
 name='M_Block51_'+key;B51[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block51_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B51;LI=M['Lime']

def b51_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block51_names.append(name);return Mesh(name,category)
def b51_finish(m,osm):
 obj=s21_finish(m);obj['detail_pass']=51;obj['reference_notes']='references/block51-notes.md';obj['osm_way']=osm;return obj
def yf51(X):return -140.01+(X+182.631)*(-140.253+140.01)/(-152.989+182.631)
def street51(w):
 ox,oy=outward(w);return w['kind']=='outer' and oy<-.9 and min(w['p'][1],w['q'][1])<-139.9
def cas51(m,x,y,u,b,w,h,a,frame,rows=(.5,),o=.18):
 facade_box(m,x,y,u,o-.04,b+h/2,w,.02,h,GLAZE,a)
 for q in (-w/2+.04,w/2-.04):facade_box(m,x,y,u+q,o,b+h/2,.08,.08,h,frame,a)
 for zz in (b+.04,b+h-.04):facade_box(m,x,y,u,o,zz,w,.08,.07,frame,a)
 facade_box(m,x,y,u,o+.01,b+h/2,.07,.08,h,frame,a)
 for t in rows:facade_box(m,x,y,u,o+.01,b+h*t,w,.05,.04,frame,a)
 facade_box(m,x,y,u,o+.22,b-.03,w+.10,.20,.04,M['Plinth'],a)
def gable51(m,x,y,a,prof,ma,verge=None):
 # A gable above the eaves as a prism in the wall's thickness; prof is the outline (u, z).
 vs=[lp(x,y,uu,o,zz,a) for o in (.005,.355) for uu,zz in prof];nn=len(prof)
 m.faces(vs,[tuple(range(nn-1,-1,-1)),tuple(range(nn,2*nn))]+[(i,(i+1)%nn,(i+1)%nn+nn,i+nn) for i in range(nn)],ma)
 if verge:town_path(m,[lp(x,y,uu,.30,zz+.05,a) for uu,zz in verge],.06,M['Tile'])
def quoins51(m,x,y,u,a,z0,z1,side):
 # Alternating long and short sandstone blocks at a corner; side +1 runs into the wall to the east.
 k=0;z=z0
 while z<z1-.05:
  hh=min(.30,z1-z);ww=.55 if k%2==0 else .34
  facade_box(m,x,y,u+side*ww/2,.37,z+hh/2,ww,.05,hh-.02,M['Quoin'],a);z+=hh;k+=1
def plinth51(m,x,y,L,a,H,gaps):
 # The plinth band, broken at the openings that reach the ground (u, width).
 at=-L/2
 for u,w in sorted(gaps)+[(L/2+1,0)]:
  lo=max(-L/2,min(L/2,u-w/2))
  if lo>at+.03:facade_box(m,x,y,(at+lo)/2,.39,H/2,lo-at,.08,H,M['Plinth'],a)
  at=max(at,min(L/2,u+w/2))
def anchor51(m,x,y,u,z,a,cross=True):
 facade_box(m,x,y,u,.38,z,.04,.03,.55,M['Iron'],a)
 if cross:facade_box(m,x,y,u,.38,z+.08,.22,.03,.04,M['Iron'],a)

m=b51_new('SM_Kvarnholmen_House_92379292','Kvarnholmen/Ölandsgatan north')
for zone in Z:
 HZ=Z[zone]['height']
 for w in walls(zone):
  x,y,L,a=sf_edge(w['p'],w['q']);S=lambda X:U(w,X,yf51(X))
  if zone=='kr' and street51(w):
   gf=[(S(-180.24),1.74,1.18,2.58,0),(S(-174.15),1.72,1.35,2.66,0)]
   up=[(S(-180.28),6.48,1.11,1.93,0),(S(-174.62),6.58,1.26,1.95,0)]
   cel=[(S(-180.24),.43,1.10,.60,0),(S(-174.15),.43,1.10,.60,0)]
   door=(S(-177.10),0,1.29,1.99,0)
   bz_wall(m,w['p'],w['q'],0,HZ,gf+up+cel+[door],LI)
   for u,b,ww,hh,r in gf+up:surround36(m,x,y,u,b,ww,hh,a,M['White'],.12,.38);cas51(m,x,y,u,b,ww,hh,a,M['GreyFrame'],(.18,.55) if b<3 else (.5,))
   for u,b,ww,hh,r in cel:cas51(m,x,y,u,b,ww,hh,a,M['GreyFrame'],(),.24)
   u,b,ww,hh,r=door;facade_box(m,x,y,u,.10,hh/2,ww,.06,hh,M['Boards'],a)
   for k in range(-3,4):facade_box(m,x,y,u+k*ww/7,.14,hh/2,.03,.02,hh-.1,M['Dark'],a)
   facade_box(m,x,y,S(-178.6),.42,1.45,.62,.10,.95,M['Dark'],a);facade_box(m,x,y,S(-178.6),.47,1.45,.52,.02,.80,M['White'],a)
   plinth51(m,x,y,L,a,1.12,[(door[0],door[2])]+[(c[0],c[2]+.04) for c in cel])
   quoins51(m,x,y,-L/2,a,1.12,HZ,1);quoins51(m,x,y,L/2,a,1.12,HZ,-1)
   for X0 in (-181.9,-178.8,-176.0,-172.6):anchor51(m,x,y,S(X0),5.5,a)
   facade_box(m,x,y,0,.37,5.62,L-1.0,.01,.01,M['Iron'],a)
   # The gable: apex over the ridge (x -177.1) at 15.6, a boarded hatch and a round opening.
   ua=S(-177.1)
   gable51(m,x,y,a,[(-L/2,HZ),(L/2,HZ),(ua,Z['kr']['top']+.25)],LI,[(-L/2-.15,HZ-.1),(ua,Z['kr']['top']+.30),(L/2+.15,HZ-.1)])
   facade_box(m,x,y,S(-177.19),.37,11.18,1.14,.06,2.26,M['Hatch'],a);surround36(m,x,y,S(-177.19),10.05,1.14,2.26,a,M['White'],.10,.38)
   for k in range(-2,3):facade_box(m,x,y,S(-177.19)+k*.22,.41,11.18,.02,.02,2.2,M['Dark'],a)
   town_rod(m,lp(x,y,ua,.30,14.0,a),lp(x,y,ua,.40,14.0,a),.20,M['Dark'],12)
   for X0,zz in ((-181.0,10.3),(-179.0,10.3),(-175.2,10.3),(-173.2,10.3),(-178.4,12.9),(-175.9,12.9)):anchor51(m,x,y,S(X0),zz,a)
  elif zone=='lr' and street51(w):
   gate=(S(-167.66),0,2.62,2.75,.41);door=(S(-160.46),1.13,.88,1.86,0)
   bz_wall(m,w['p'],w['q'],0,HZ,[gate,door],LI)
   gu=gate[0]
   # The arch's white band, the passage through to the courtyard, the boarded leaves folded open.
   arc=[(gu-1.44,.05),(gu-1.44,2.75)]+[(gu-1.44*math.cos(math.pi*k/16),2.75+.55*math.sin(math.pi*k/16)) for k in range(1,16)]+[(gu+1.44,2.75),(gu+1.44,.05)]
   town_path(m,[lp(x,y,uu,.38,zz,a) for uu,zz in arc],.11,M['White'])
   for s in (-1,1):facade_box(m,x,y,gu+s*(1.31-.03),-2.3,1.55,.06,4.8,3.1,LI,a)
   facade_box(m,x,y,gu,-2.3,3.17,2.62,4.8,.06,LI,a)
   for s in (-1,1):
    facade_box(m,x,y,gu+s*(1.31-.12),-.75,1.40,.06,1.25,2.70,M['Boards'],a)
    for k in range(6):facade_box(m,x,y,gu+s*(1.31-.16),-.25-k*.2,1.4,.02,.02,2.6,M['Dark'],a)
   u,b,ww,hh,r=door
   facade_box(m,x,y,u,.10,b+hh/2,ww,.06,hh,M['Boards'],a)
   for k in range(1,6):facade_box(m,x,y,u,.14,b+.2+k*(hh*.45)/6,ww-.1,.02,.03,M['GreyFrame'],a)
   surround36(m,x,y,u,b,ww,hh,a,M['White'],.18,.38)
   steps36(m,x,y,u,a,1.30,1.10,b,3,.30,M['Quoin'])
   plinth51(m,x,y,L,a,1.0,[(gu,2.62+.24)])
   facade_box(m,x,y,0,.41,6.47,L,.08,.24,M['White'],a);facade_box(m,x,y,0,.46,6.85,L+.06,.20,.52,M['White'],a);facade_box(m,x,y,0,.53,7.30,L+.12,.34,.30,M['White'],a)
   town_rod(m,lp(x,y,S(-164.9),.50,.25,a),lp(x,y,S(-164.9),.50,7.2,a),.06,M['GreyFrame'],8)
   for X0 in (-170.6,-166.0,-164.2,-162.6,-161.4):anchor51(m,x,y,S(X0),3.4,a,False)
  elif zone=='eg' and street51(w):
   win=(S(-156.82),2.21,1.22,1.05,0);gw=(S(-156.79),7.58,.81,1.26,0);hatch=(S(-156.66),0,1.28,.88,0)
   bz_wall(m,w['p'],w['q'],0,HZ,[win,hatch],LI)
   surround36(m,x,y,win[0],2.21,1.22,1.05,a,M['White'],.14,.38);cas51(m,x,y,win[0],2.21,1.22,1.05,a,M['GreyFrame'],(.5,))
   u,b,ww,hh,r=hatch
   for s in (-1,1):facade_box(m,x,y,u+s*ww/4,.12,hh/2,ww/2-.02,.06,hh,M['GreyFrame'],a)
   plinth51(m,x,y,L,a,1.0,[(hatch[0],hatch[2]+.04)])
   # The half gable rises from the west eaves (7.84) to the party wall (13.3); the window high in it.
   gable51(m,x,y,a,[(-L/2,HZ),(L/2,HZ),(L/2,Z['eg']['top']),(L/2-.25,Z['eg']['top'])],LI,[(-L/2-.15,HZ-.1),(L/2-.25,Z['eg']['top']+.05)])
   facade_box(m,x,y,gw[0],.20,gw[1]+gw[3]/2,gw[2],.30,gw[3],M['Dark'],a)
   surround36(m,x,y,gw[0],gw[1],gw[2],gw[3],a,M['White'],.14,.42);cas51(m,x,y,gw[0],gw[1],gw[2],gw[3],a,M['GreyFrame'],(.5,),.40)
   facade_box(m,x,y,gw[0],.55,gw[1]-.05,gw[2]+.3,.25,.06,M['Hatch'],a)
   for X0,zz in ((-159.2,3.4),(-157.9,3.4),(-155.2,3.4),(-154.0,3.4),(-155.6,8.0),(-157.8,7.9)):anchor51(m,x,y,S(X0),zz,a,False)
  else:
   if w['kind']=='outer':plain(m,w,HZ,LI,M['GreyFrame'],M['White'],3 if zone in('bk','kr') else 2,.9)
   else:bz_wall(m,w['p'],w['q'],w['z0'],HZ,[],LI)
roof34(m,'kr',M['Tile'],LI);roof34(m,'lr',M['Tile'],LI);roof34(m,'eg',M['Tile'],LI)
for g in Z['bk']['polygons']:
 pts=simplify([tuple(v) for v in g],.8)
 inset_roof(m,pts,Z['bk']['height'],min(2.4,.45*min(math.dist(p,q) for p,q in zip(pts,pts[1:]+pts[:1]))),1.75,M['Tile'],.35)
for cx,cy,zz in ((-177.1,-131.0,Z['kr']['top']),(-155.5,-134.0,Z['eg']['top']-1.2)):box(m,cx,cy,.60,.80,1.0,zz-.4,M['Quoin'],0,M['Dark'])
b51_finish(m,'92379292')

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
_C={'A':(-161.18,5.84),'B':(-171.56,5.99),'C':(-181.23,5.68)}
def _cam(n):X,D_=_C[n];return X,yf51(X)-.355-D_,2.27
block51_cameras=[
 sv_camera('298_Block51_Cal_StoneHouse',*_cam('A'),332,5,90),
 sv_camera('299_Block51_Cal_Arch',*_cam('B'),332,5,90),
 sv_camera('300_Block51_Cal_Kronan',*_cam('C'),332,5,90),
 ('301_Block51_Aerial',(-168.0,-168.0,28.0),(-168.0,-132.0,6.0),28),
]
print('BLOCK51_GEOMETRY',len(block51_names))
