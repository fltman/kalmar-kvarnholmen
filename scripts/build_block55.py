"""Pass 55: the district volume 92379255 on the corner of Storgatan and Västra Sjögatan, a
limestone-clad three-storey commercial building:
- to Västra Sjögatan seven axes of white casements set flush in the slab cladding on two storeys, a
  dark fascia at the flat roof, and at street level a garage door, a shopfront, the entrance (13) in a
  carved stone surround, a wide shop window and an open arcade under the corner with a square pier;
- the long Storgatan side (pedestrian, not in Street View) repeats the same rhythm as an estimate.

References: Google Street View April 2025 (two panoramas on Västra Sjögatan chained on shared window
edges and anchored on the joint with the wooden house to the south; a view towards the corner),
view only. Zones: source/block55.json; see references/block55-notes.md. The signs, the awnings and
the reliefs' motifs are omitted.
"""
B55D=json.loads((R/'source/block55.json').read_text());Z=B55D['zones']
block55_names=[];B55={}
for old in [k for k in list(materials) if k.startswith('M_Block55_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Slab','TownStone',(.80,.78,.72),.80,0),
 ('Joint','TownStone',(.62,.60,.56),.85,0),
 ('Granite','TownStone',(.55,.54,.52),.84,0),
 ('WhiteFrame','TownPaintWhite',(.94,.94,.92),.55,0),
 ('ShopFrame','TownMetalGrey',(.12,.12,.12),.45,.30),
 ('Garage','TownPaintBrown',(.26,.20,.16),.60,0),
 ('Fascia','TownMetalGrey',(.16,.17,.17),.50,.40),
 ('Dark','TownMetalGrey',(.05,.055,.06),.40,.20),
 ]:
 name='M_Block55_'+key;B55[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block55_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B55;SL=M['Slab']

def b55_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block55_names.append(name);return Mesh(name,category)
def b55_finish(m,osm):
 obj=s21_finish(m);obj['detail_pass']=55;obj['reference_notes']='references/block55-notes.md';obj['osm_way']=osm;return obj
def xe55(Y):return -39.512+(Y+26.813)*(-39.406+39.512)/(-8.971+26.813)
def yn55(X):return -8.712+(X+81.208)*(-8.971+8.712)/(-39.406+81.208)
def east55(w):ox,oy=outward(w);return w['kind']=='outer' and ox>.9 and max(w['p'][0],w['q'][0])>-40
def north55(w):ox,oy=outward(w);return w['kind']=='outer' and oy>.9 and max(w['p'][1],w['q'][1])>-9.2
def cas55(m,x,y,u,b,w,h,a,o=.30):
 # Flush white casements: two leaves with a narrow transom.
 facade_box(m,x,y,u,o-.05,b+h/2,w,.02,h,GLAZE,a)
 for q in (-w/2+.04,w/2-.04,0):facade_box(m,x,y,u+q,o,b+h/2,.08 if q else .07,.06,h,M['WhiteFrame'],a)
 for zz in (b+.04,b+h-.04):facade_box(m,x,y,u,o,zz,w,.06,.07,M['WhiteFrame'],a)
 facade_box(m,x,y,u,.40,b-.03,w+.06,.10,.05,M['Joint'],a)
def slabs55(m,x,y,L,a,z0,z1,holes):
 # Slab joints of the cladding: courses of 0.62 m, stopped at the openings.
 z=z0+.62
 while z<z1-.1:
  at=-L/2
  for u,b,ww,hh,r in sorted([h for h in holes if h[1]-.05<z<h[1]+h[3]+.05])+[(L/2+2,0,0,0,0)]:
   lo=max(-L/2,min(L/2,u-ww/2-.05))
   if lo>at+.1:facade_box(m,x,y,(at+lo)/2,.362,z,lo-at,.01,.015,M['Joint'],a)
   at=max(at,min(L/2,u+ww/2+.05))
  z+=.62
def shop55(m,x,y,u,b,w,h,a,cols=2):
 facade_box(m,x,y,u,.12,b+h/2,w,.03,h,GLAZE,a)
 for k in range(cols+1):facade_box(m,x,y,u-w/2+k*w/cols,.18,b+h/2,.07,.08,h,M['ShopFrame'],a)
 for zz in (b+.04,b+h-.04):facade_box(m,x,y,u,.18,zz,w,.08,.07,M['ShopFrame'],a)

AX=[-25.65,-23.2,-20.7,-18.17,-15.55,-12.9,-10.3]
m=b55_new('SM_Building_92379255','Kvarnholmen/Storgatan')
H=Z['sb']['height']
for w in walls('sb'):
 x,y,L,a=sf_edge(w['p'],w['q'])
 if east55(w):
  S=lambda Y:U(w,xe55(Y),Y)
  up=[(S(Y0),5.19,1.40,1.93,0) for Y0 in AX]+[(S(Y0),8.52,1.34,1.92,0) for Y0 in AX]
  gar=(S(-25.07),.0,2.55,3.24,0);sushi=(S(-21.4),.0,2.63,2.63,0);door=(S(-18.05),.0,1.29,3.20,0);shopw=(S(-14.08),.44,4.55,2.09,0)
  arc=(S(-10.12),0,2.40,3.30,0)
  holes=up+[gar,sushi,door,shopw,arc]
  bz_wall(m,w['p'],w['q'],0,H,holes,SL)
  for u,b,ww,hh,r in up:cas55(m,x,y,u,b,ww,hh,a)
  slabs55(m,x,y,L,a,0,H-.5,holes)
  u,b,ww,hh,r=gar;facade_box(m,x,y,u,.08,hh/2,ww,.06,hh,M['Garage'],a)
  for k in range(1,14):facade_box(m,x,y,u,.12,k*hh/14,ww,.02,.02,M['Dark'],a)
  u,b,ww,hh,r=sushi;shop55(m,x,y,u,b,ww,hh,a,2)
  u,b,ww,hh,r=door;facade_box(m,x,y,u,-.9,b+hh/2,ww,.06,hh,M['ShopFrame'],a);facade_box(m,x,y,u,-.86,b+hh*.55,ww-.3,.02,hh*.7,GLAZE,a)
  for s in (-1,1):facade_box(m,x,y,u+s*(ww/2-.03),-.45,hh/2,.06,.9,hh,SL,a)
  facade_box(m,x,y,u,-.45,hh-.03,ww,.9,.06,SL,a)
  # The carved stone surround of the entrance: two broad jambs and a lintel, proud of the slabs.
  # (1.14 m wide on the south side, 0.55 m on the north side, measured)
  uS,uN=S(-19.27),S(-17.135)
  facade_box(m,x,y,uS,.44,1.62,1.14,.16,3.24,SL,a);facade_box(m,x,y,uN,.44,1.62,.55,.16,3.24,SL,a)
  facade_box(m,x,y,(uS+uN)/2,.44,3.45,abs(uN-uS)+(1.14+.55)/2,.16,.42,SL,a)
  u,b,ww,hh,r=shopw;shop55(m,x,y,u,b,ww,hh,a,3);facade_box(m,x,y,u,.40,.22,ww,.10,.44,M['Granite'],a)
  facade_box(m,x,y,0,.42,3.45,L,.12,.34,SL,a)
  facade_box(m,x,y,0,.40,.22,L,.08,.44,M['Granite'],a)
  facade_box(m,x,y,0,.46,H-.18,L+.1,.24,.36,M['Fascia'],a)
  town_rod(m,lp(x,y,S(-26.6),.52,.25,a),lp(x,y,S(-26.6),.52,H-.2,a),.05,M['Dark'],8)
 elif north55(w):
  S=lambda X:U(w,X,yn55(X))
  # Storgatan (no Street View): the same rhythm, shopfronts on the ground floor, the arcade's first
  # bay at the corner.
  n=int((-41.8+80.8)/2.6);xs=[-41.8-2.6*(k+.5)+.1 for k in range(n)]
  xs=[X0 for X0 in xs if X0<-43.2]
  up=[(S(X0),5.19,1.40,1.93,0) for X0 in xs]+[(S(X0),8.52,1.34,1.92,0) for X0 in xs]
  shops=[(S(-47.0-5.3*k),.44,4.2,2.09,0) for k in range(7)]
  arc=(S(-40.6),0,2.40,3.30,0)
  holes=up+shops+[arc]
  bz_wall(m,w['p'],w['q'],0,H,holes,SL)
  for u,b,ww,hh,r in up:cas55(m,x,y,u,b,ww,hh,a)
  for u,b,ww,hh,r in shops:shop55(m,x,y,u,b,ww,hh,a,3)
  slabs55(m,x,y,L,a,0,H-.5,holes)
  facade_box(m,x,y,0,.42,3.45,L,.12,.34,SL,a);facade_box(m,x,y,0,.40,.22,L,.08,.44,M['Granite'],a)
  facade_box(m,x,y,0,.46,H-.18,L+.1,.24,.36,M['Fascia'],a)
 else:
  if w['kind']=='outer':plain(m,w,H,SL,M['WhiteFrame'],SL,3,.9)
  else:bz_wall(m,w['p'],w['q'],w['z0'],H,[],SL)
# The corner arcade: a recess 2.4 m deep under the first floor, with a square pier at the corner.
cx,cy=xe55(-8.97),yn55(-39.4)
for (X0,Y0),(X1,Y1) in (((cx-2.75,cy-.2),(cx-2.75,cy-2.5)),((cx-.2,cy-2.55),(cx-2.75,cy-2.55))):
 xx,yy,LL,aa=sf_edge((X0,Y0),(X1,Y1));facade_box(m,xx,yy,0,0,1.65,LL,.10,3.30,SL,aa)
box(m,cx+.05,cy+.05,.55,.55,3.30,0,SL,0,SL)
box(m,cx-1.2,cy-1.2,2.9,2.9,.08,3.26,SL,0,SL)
for g in Z['sb']['polygons']:
 pts=simplify([tuple(v) for v in g],.5)
 inset_roof(m,pts,H,min(1.5,.45*min(math.dist(p,q) for p,q in zip(pts,pts[1:]+pts[:1]))),Z['sb']['top']-H,M['Fascia'],.15)
b55_finish(m,'92379255')

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
_C={'A':(-17.04,5.89),'S':(-27.60,5.80)}
def _cam(n):Y,D_=_C[n];return xe55(Y)+.355+D_,Y,2.38
block55_cameras=[
 sv_camera('312_Block55_Cal_Entrance',*_cam('A'),242,20,90),
 sv_camera('313_Block55_Cal_South',*_cam('S'),242,20,90),
 ('314_Block55_Aerial',(-30.0,5.0,30.0),(-58.0,-20.0,4.0),28),
]
print('BLOCK55_GEOMETRY',len(block55_names))
