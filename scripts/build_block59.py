"""Pass 59: the district volume 91970317 on Fiskaregatan, west of pass 58, a green-boarded
two-storey wooden house:
- vertical boarding with white pilasters at the corners and between the parts;
- six white casements upstairs (a narrow one at the east end), four below, and the black boarded
  gateway at the east end under a white hood with a panel;
- a black plinth with three cellar windows, a white cornice, and a tile roof with a snow rail and
  three boarded dormers.

References: Google Street View April 2025 (two panoramas on Fiskaregatan anchored on both ends and
spaced as their GPS positions), view only. Zones: source/block59.json; see
references/block59-notes.md. The parking sign and the wall lamp are omitted.
"""
B59D=json.loads((R/'source/block59.json').read_text());Z=B59D['zones']
block59_names=[];B59={}
for old in [k for k in list(materials) if k.startswith('M_Block59_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Board','TownIvory',(.52,.66,.46),.80,0),
 ('White','TownIvory',(.95,.95,.93),.82,0),
 ('Plinth','TownMetalGrey',(.10,.10,.10),.90,0),
 ('WhiteFrame','TownPaintWhite',(.94,.94,.92),.55,0),
 ('Gate','TownPaintBrown',(.10,.10,.10),.60,0),
 ('Tile','TownTileRed',(.60,.32,.24),.80,0),
 ('Iron','TownMetalGrey',(.08,.08,.085),.45,.40),
 ('Dark','TownMetalGrey',(.05,.055,.06),.40,.20),
 ]:
 name='M_Block59_'+key;B59[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block59_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B59;WH=M['White'];BD=M['Board']

def b59_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block59_names.append(name);return Mesh(name,category)
def b59_finish(m,osm):
 obj=s21_finish(m);obj['detail_pass']=59;obj['reference_notes']='references/block59-notes.md';obj['osm_way']=osm;return obj
def yf59(X):return 134.536+(X-5.937)*(134.027-134.536)/(20.407-5.937)
def street59(w):ox,oy=outward(w);return w['kind']=='outer' and oy>.9 and max(w['p'][1],w['q'][1])>133.9
def cas59(m,x,y,u,b,w,h,a,o=.18):
 facade_box(m,x,y,u,o-.04,b+h/2,w,.02,h,GLAZE,a)
 for q in (-w/2+.04,w/2-.04,0):facade_box(m,x,y,u+q,o,b+h/2,.08 if q else .07,.08,h,M['WhiteFrame'],a)
 for zz in (b+.04,b+h-.04,b+h*.6):facade_box(m,x,y,u,o,zz,w,.08,.06,M['WhiteFrame'],a)

UP=[(19.80,.90),(17.45,1.20),(14.88,1.10),(12.95,1.20),(9.60,1.30),(7.50,1.30)]
GF=[(14.98,1.25),(12.74,1.35),(9.60,1.30),(7.50,1.30)]
m=b59_new('SM_Kvarnholmen_House_91970317','Kvarnholmen/Fiskaregatan')
H=Z['gn']['height']
for w in walls('gn'):
 x,y,L,a=sf_edge(w['p'],w['q'])
 if street59(w):
  S=lambda X:U(w,X,yf59(X))
  up=[(S(X0),4.38,ww,1.47,0) for X0,ww in UP];gf=[(S(X0),1.93,ww,1.64,0) for X0,ww in GF]
  gate=(S(18.60),0,2.30,2.57,0)
  bz_wall(m,w['p'],w['q'],0,H,up+gf+[gate],BD);boards35(m,x,y,L,a,1.1,6.0,up+gf+[gate],BD,.22)
  for u,b,ww,hh,r in up+gf:surround36(m,x,y,u,b,ww,hh,a,WH,.12,.39);cas59(m,x,y,u,b,ww,hh,a)
  u,b,ww,hh,r=gate
  for s in (-1,1):
   facade_box(m,x,y,u+s*ww/4,.10,hh/2,ww/2-.02,.06,hh,M['Gate'],a)
   for k in range(1,12):facade_box(m,x,y,u+s*ww/4,.14,k*hh/12,ww/2-.06,.02,.02,M['Dark'],a)
  surround36(m,x,y,u,0,ww,hh,a,WH,.10,.39)
  facade_box(m,x,y,u,.46,2.95,ww+.40,.12,.64,WH,a);facade_box(m,x,y,u,.53,2.95,ww-.10,.02,.36,BD,a);facade_box(m,x,y,u,.52,3.31,ww+.52,.22,.08,WH,a)
  for X0,ww in ((20.25,.30),(15.76,.30),(10.95,.46),(6.10,.34)):facade_box(m,x,y,S(X0),.42,(1.1+6.1)/2,ww,.10,5.0,WH,a)
  at=-L/2
  for uu,ww2 in ((gate[0],gate[2]+.2),(L/2+2,0)):
   lo=max(-L/2,min(L/2,uu-ww2/2))
   if lo>at+.03:facade_box(m,x,y,(at+lo)/2,.39,.55,lo-at,.08,1.1,M['Plinth'],a)
   at=max(at,min(L/2,uu+ww2/2))
  for X0 in (14.4,12.3,8.2):facade_box(m,x,y,S(X0),.44,.55,.62,.04,.52,M['Dark'],a)
  facade_box(m,x,y,0,.42,1.14,L,.12,.08,WH,a)
  facade_box(m,x,y,0,.42,6.05,L,.10,.22,WH,a);facade_box(m,x,y,0,.54,6.24,L+.10,.34,.16,WH,a)
  town_rod(m,lp(x,y,-L/2,.72,6.3,a),lp(x,y,L/2,.72,6.3,a),.07,WH,8)
  sl=(Z['gn']['top']-H)/3.0
  # (the roof's 0.4 m overhang lifts its surface at the wall line; the dormers start from there)
  for X0 in (17.2,13.9,10.3):roof_dormer(m,x,y,S(X0),a,H+.4*sl,sl,.30,1.00,.95,BD,M['Tile'],M['WhiteFrame'],False)
  for zz in (6.9,7.15):town_rod(m,lp(x,y,-L/2+.2,-.5,zz,a),lp(x,y,L/2-.2,-.5,zz,a),.02,M['Iron'],6)
 else:
  if w['kind']=='outer':plain(m,w,H,BD,M['WhiteFrame'],WH,2,.9)
  else:bz_wall(m,w['p'],w['q'],w['z0'],H,[],BD)
for g in Z['gn']['polygons']:
 pts=simplify([tuple(v) for v in g],.8)
 inset_roof(m,pts,H,min(3.0,.45*min(math.dist(p,q) for p,q in zip(pts,pts[1:]+pts[:1]))),Z['gn']['top']-H,M['Tile'],.40)
box(m,8.0,131.5,.55,.75,1.0,Z['gn']['top']-.6,M['Tile'],0,M['Dark'])
b59_finish(m,'91970317')

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block59_cameras=[
 sv_camera('326_Block59_Cal_Gate',14.60,141.27+.355,2.27,152,20,90),
 sv_camera('327_Block59_Cal_West',4.33,141.51+.355,2.27,152,20,90),
 ('328_Block59_Aerial',(13.0,160.0,24.0),(13.0,128.0,4.0),28),
]
print('BLOCK59_GEOMETRY',len(block59_names))
