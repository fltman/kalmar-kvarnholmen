"""Pass 50: the district volume 92379264 on the south side of Ölandsgatan, east of pass 49: house
number 14, a white roughcast two-storey house:
- an arched gateway with open iron gates and a white passage through to the courtyard;
- two shop windows, and a round-headed door at each end (a grey roller shutter, a grey panelled door);
- three white casements in flat surrounds upstairs;
- a grey plinth, a small cornice, and a tile roof with two dormers at the eaves (red and white) and
  two chimneys.

References: Google Street View April 2025 (two panoramas chained on nine shared edges and anchored on
the joint measured in pass 49), view only. Zones: source/block50.json; see
references/block50-notes.md. The signs, the hanging signs, the number plate and the pavement boards
are omitted.
"""
B50D=json.loads((R/'source/block50.json').read_text());Z=B50D['zones']
block50_names=[];B50={}
for old in [k for k in list(materials) if k.startswith('M_Block50_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('White','TownIvory',(.95,.95,.93),.88,0),
 ('Plinth','TownStone',(.52,.52,.51),.86,0),
 ('Grey','TownPaintWhite',(.62,.63,.63),.60,0),
 ('WhiteFrame','TownPaintWhite',(.94,.94,.92),.55,0),
 ('RedBoard','TownPaintBrown',(.55,.16,.12),.65,0),
 ('Tile','TownTileRed',(.52,.30,.24),.80,0),
 ('Brick','TownTileRed',(.62,.28,.22),.85,0),
 ('Iron','TownMetalGrey',(.08,.08,.085),.45,.40),
 ('Dark','TownMetalGrey',(.05,.055,.06),.40,.20),
 ]:
 name='M_Block50_'+key;B50[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block50_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B50;WH=M['White']

def b50_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block50_names.append(name);return Mesh(name,category)
def b50_finish(m,osm):
 obj=s21_finish(m);obj['detail_pass']=50;obj['reference_notes']='references/block50-notes.md';obj['osm_way']=osm;return obj
def yf50(X):return -151.63+(X+142.798)*(-151.077+151.63)/(-156.926+142.798)
def street50(w):
 ox,oy=outward(w);return w['kind']=='outer' and oy>.9 and max(w['p'][1],w['q'][1])>-151.7
def cas50(m,x,y,u,b,w,h,a,frame,trans=.66,o=.18):
 facade_box(m,x,y,u,o-.04,b+h/2,w,.02,h,GLAZE,a)
 for q in (-w/2+.04,w/2-.04):facade_box(m,x,y,u+q,o,b+h/2,.08,.08,h,frame,a)
 for zz in (b+.04,b+h-.04,b+h*trans):facade_box(m,x,y,u,o,zz,w,.08,.07,frame,a)
 facade_box(m,x,y,u,o+.01,b+h/2,.07,.08,h,frame,a)
 for zz in (b+h*.33,):facade_box(m,x,y,u,o+.01,zz,w,.04,.03,frame,a)
 facade_box(m,x,y,u,o+.22,b-.03,w+.10,.20,.04,M['Dark'],a)

m=b50_new('SM_Kvarnholmen_House_92379264','Kvarnholmen/Ölandsgatan south')
HZ=Z['wh']['height']
for w in walls('wh'):
 x,y,L,a=sf_edge(w['p'],w['q']);S=lambda X:U(w,X,yf50(X))
 if not street50(w):
  if w['kind']=='outer':plain(m,w,HZ,WH,M['WhiteFrame'],WH,2,.9)
  else:bz_wall(m,w['p'],w['q'],w['z0'],HZ,[],WH)
  continue
 # Openings (x from the panoramas): the doors and the gateway are round-headed.
 d1=(S(-144.0),.53,1.00,1.72,.49);d2=(S(-155.42),.53,.98,1.40,.49)
 gate=(S(-150.2),0,2.31,2.45,.53)
 shops=[(S(-146.765),.94,1.77,1.48,0),(S(-153.27),.88,1.96,1.54,0)]
 up=[(S(X0),4.19,ww,1.40,0) for X0,ww in ((-146.565,1.19),(-150.62,1.12),(-154.165,1.13))]
 bz_wall(m,w['p'],w['q'],0,HZ,[d1,d2,gate]+shops+up,WH)
 for u,b,ww,hh,r in up:surround36(m,x,y,u,b,ww,hh,a,WH,.10,.39);cas50(m,x,y,u,b,ww,hh,a,M['WhiteFrame'])
 for u,b,ww,hh,r in shops:surround36(m,x,y,u,b,ww,hh,a,WH,.08,.39);shopfront38(m,x,y,u,b,ww,hh,a,M['WhiteFrame'],1)
 # The doors: a grey roller shutter in the east one, a grey panelled door in the west one, each on a
 # step; arched white reveals.
 for (u,b,ww,hh,r),kind in ((d1,'shutter'),(d2,'door')):
  facade_box(m,x,y,u,.05,b+(hh+r)/2,ww,.06,hh+r,M['Grey'],a)
  if kind=='shutter':
   for k in range(1,16):facade_box(m,x,y,u,.09,b+k*(hh+r)/16,ww,.02,.02,M['Dark'],a)
  else:
   for zz in (b+.35,b+1.05):facade_box(m,x,y,u,.09,zz,ww-.24,.02,.5,M['WhiteFrame'],a)
  facade_box(m,x,y,u,.50,b/2,ww+.40,.30,b,M['Plinth'],a)
 # The gateway: white reveals and ceiling through to the courtyard, the iron gates folded open.
 gu=gate[0]
 for s in (-1,1):facade_box(m,x,y,gu+s*(1.155-.03),-2.8,1.3,.06,6.3,2.6,WH,a)
 facade_box(m,x,y,gu,-2.8,2.98,2.31,6.3,.06,WH,a)
 for s in (-1,1):
  for k in range(9):facade_box(m,x,y,gu+s*1.08,-.15-k*1.1/8,1.2,.03,.025,2.4,M['Iron'],a)
  for zz in (.1,1.1,2.3):facade_box(m,x,y,gu+s*1.08,-.70,zz,.03,1.12,.05,M['Iron'],a)
 plinth=[(-L/2,d1[0]-.70),(d1[0]+.70,gate[0]-1.155),(gate[0]+1.155,d2[0]-.69),(d2[0]+.69,L/2)]
 for lo,hi in plinth:
  lo,hi=max(-L/2,min(lo,hi)),min(L/2,max(lo,hi))
  if hi-lo>.05:facade_box(m,x,y,(lo+hi)/2,.39,.325,hi-lo,.08,.65,M['Plinth'],a)
 facade_box(m,x,y,0,.42,6.20,L,.10,.18,WH,a);facade_box(m,x,y,0,.54,6.34,L+.10,.34,.12,WH,a)
 town_rod(m,lp(x,y,-L/2,.66,6.28,a),lp(x,y,L/2,.66,6.28,a),.06,M['Iron'],8)
 for X0 in (-143.0,-156.7):town_rod(m,lp(x,y,S(X0),.48,.25,a),lp(x,y,S(X0),.48,HZ,a),.05,M['Grey'],8)
sl=roof34(m,'wh',M['Tile'],WH)
for w in walls('wh'):
 if street50(w):
  x,y,L,a=sf_edge(w['p'],w['q'])
  for X0,body in ((-146.15,M['RedBoard']),(-153.13,WH)):
   roof_dormer(m,x,y,U(w,X0,yf50(X0)),a,HZ,sl,.3,1.05,.72,body,M['Tile'] if body==WH else M['RedBoard'],M['WhiteFrame'],False)
for cx,cy,ma in ((-146.0,-152.6,M['Brick']),(-150.3,-154.3,M['Plinth'])):box(m,cx,cy,.55,.75,1.1,Z['wh']['top']-.3,ma,0,M['Dark'])
b50_finish(m,'92379264')

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
_C={'W':(-151.55,5.79),'E':(-141.58,5.70)}
def _cam(n):X,D_=_C[n];return X,yf50(X)+.355+D_,2.40
block50_cameras=[
 sv_camera('295_Block50_Cal_House14',*_cam('W'),152,5,90),
 sv_camera('296_Block50_Cal_East',*_cam('E'),152,5,90),
 ('297_Block50_Aerial',(-150.0,-128.0,26.0),(-150.0,-160.0,4.0),28),
]
print('BLOCK50_GEOMETRY',len(block50_names))
