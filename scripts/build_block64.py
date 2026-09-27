"""Pass 64: the district volume 91885528 on the corner of Östra Sjögatan and Fiskaregatan, an ochre
roughcast two-storey house:
- to Östra Sjögatan six axes of green-framed casements in white surrounds (the upper ones under
  small green hoods), a pale green plinth with barred cellar windows, the eaves, and a tile roof with
  four red dormers;
- the long Fiskaregatan side (seen only at the corner) keeps the same rhythm.

References: Google Street View April 2025 (two panoramas on Östra Sjögatan, each anchored on one end
of the house), view only. Zones: source/block64.json; see references/block64-notes.md. The shop
sign and the street lamp are omitted.
"""
B64D=json.loads((R/'source/block64.json').read_text());Z=B64D['zones']
block64_names=[];B64={}
for old in [k for k in list(materials) if k.startswith('M_Block64_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Ochre','TownIvory',(.66,.54,.38),.95,0),
 ('White','TownIvory',(.95,.95,.93),.82,0),
 ('Plinth','TownIvory',(.74,.80,.70),.90,0),
 ('GreenFrame','TownPaintBrown',(.42,.46,.30),.55,0),
 ('RedDormer','TownPaintBrown',(.50,.15,.12),.60,0),
 ('Tile','TownTileRed',(.58,.32,.24),.80,0),
 ('Dark','TownMetalGrey',(.05,.055,.06),.40,.20),
 ]:
 name='M_Block64_'+key;B64[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block64_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B64;WH=M['White'];OC=M['Ochre']

def b64_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block64_names.append(name);return Mesh(name,category)
def b64_finish(m,osm):
 obj=s21_finish(m);obj['detail_pass']=64;obj['reference_notes']='references/block64-notes.md';obj['osm_way']=osm;return obj
def xw64(Y):return 59.729+(Y-108.636)*(60.313-59.729)/(129.985-108.636)
def cas64(m,x,y,u,b,w,h,a,o=.18):
 facade_box(m,x,y,u,o-.04,b+h/2,w,.02,h,GLAZE,a)
 for q in (-w/2+.04,w/2-.04,0):facade_box(m,x,y,u+q,o,b+h/2,.08 if q else .07,.08,h,M['GreenFrame'],a)
 for zz in (b+.04,b+h-.04):facade_box(m,x,y,u,o,zz,w,.08,.07,M['GreenFrame'],a)
 facade_box(m,x,y,u,.44,b-.05,w+.10,.18,.06,M['Dark'],a)
def front64(m,w,axes,a_hoods=True):
 x,y,L,a=sf_edge(w['p'],w['q'])
 return x,y,L,a

AX=[127.97,124.49,121.4,118.04,114.63,111.17]
m=b64_new('SM_Kvarnholmen_House_91885528','Kvarnholmen/Östra Sjögatan')
H=Z['br']['height']
for w in walls('br'):
 x,y,L,a=sf_edge(w['p'],w['q']);ox,oy=outward(w)
 if w['kind']=='outer' and ox<-.9 and min(w['p'][0],w['q'][0])<60.5:
  S=lambda Y:U(w,xw64(Y),Y)
  up=[(S(Y0),5.04,1.10,1.81,0) for Y0 in AX];gf=[(S(Y0),1.73,1.28,1.95,0) for Y0 in AX]
  grl=[(S(Y0),.28,.95,.45,0) for Y0 in (121.0,117.7,110.9,127.6)]
  bz_wall(m,w['p'],w['q'],0,H,up+gf+grl,OC)
  for u,b,ww,hh,r in up+gf:surround36(m,x,y,u,b,ww,hh,a,WH,.10,.39);cas64(m,x,y,u,b,ww,hh,a)
  for u,b,ww,hh,r in up:facade_box(m,x,y,u,.50,b+hh+.08,ww+.20,.30,.06,M['GreenFrame'],a)
  for u,b,ww,hh,r in grl:
   facade_box(m,x,y,u,.46,b+hh/2,ww,.02,hh,M['Dark'],a)
   for k in range(1,7):facade_box(m,x,y,u-ww/2+k*ww/7,.48,b+hh/2,.025,.03,hh,M['GreenFrame'],a)
   facade_box(m,x,y,u,.48,b+hh+.03,ww+.08,.04,.05,M['GreenFrame'],a)
  facade_box(m,x,y,0,.40,.42,L,.10,.84,M['Plinth'],a)
  facade_box(m,x,y,0,.42,7.10,L,.10,.26,WH,a);facade_box(m,x,y,0,.54,7.34,L+.10,.36,.14,WH,a)
  sl=(Z['br']['top']-H)/3.5
  for Y0 in (124.49,121.4,118.04,114.63):roof_dormer(m,x,y,S(Y0),a,H+.4*sl,sl,.30,1.00,.95,M['RedDormer'],M['RedDormer'],WH,False)
 elif w['kind']=='outer' and oy>.9 and L>5:
  # The Fiskaregatan side (seen only at the corner): the same storeys and rhythm.
  n=max(1,int(L/3.4));up=[(-L/2+(k+.5)*L/n,5.04,1.10,1.81,0) for k in range(n)];gf=[(-L/2+(k+.5)*L/n,1.73,1.28,1.95,0) for k in range(n)]
  bz_wall(m,w['p'],w['q'],0,H,up+gf,OC)
  for u,b,ww,hh,r in up+gf:surround36(m,x,y,u,b,ww,hh,a,WH,.10,.39);cas64(m,x,y,u,b,ww,hh,a)
  facade_box(m,x,y,0,.40,.42,L,.10,.84,M['Plinth'],a);facade_box(m,x,y,0,.42,7.10,L,.10,.26,WH,a)
 else:
  if w['kind']=='outer':plain(m,w,H,OC,M['GreenFrame'],WH,2,.9)
  else:bz_wall(m,w['p'],w['q'],w['z0'],H,[],OC)
for g in Z['br']['polygons']:
 pts=simplify([tuple(v) for v in g],.8)
 inset_roof(m,pts,H,min(3.5,.45*min(math.dist(p,q) for p,q in zip(pts,pts[1:]+pts[:1]))),Z['br']['top']-H,M['Tile'],.40)
for cx,cy in ((64.0,119.0),(78.0,121.0)):box(m,cx,cy,.55,.75,1.0,Z['br']['top']-.7,M['Tile'],0,M['Dark'])
b64_finish(m,'91885528')

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block64_cameras=[
 sv_camera('342_Block64_Cal_South',52.18-.355,116.01+.25,2.60,62,20,90),
 sv_camera('343_Block64_Cal_Corner',53.76-.355,128.98-.25,2.60,62,20,90),
 ('344_Block64_Aerial',(48.0,118.0,26.0),(72.0,118.0,4.0),28),
]
print('BLOCK64_GEOMETRY',len(block64_names))
