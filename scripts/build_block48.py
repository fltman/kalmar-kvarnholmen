"""Pass 48: the district volume 92379261 on the north side of Ölandsgatan, west of pass 47: a pale
yellow two-storey house with three ground-floor and four upper casements (brown frames in white
surrounds), a gateway passage with an iron gate set back, a buff plinth, a cornice and a dark sheet
roof with a dormer and a railing.

References: Google Street View April 2025 (two panoramas, chained on four shared window edges and the
gateway, anchored on both joints), view only. Zones: source/block48.json; see
references/block48-notes.md. The company sign and the parking signs are omitted.
"""
B48D=json.loads((R/'source/block48.json').read_text());Z=B48D['zones']
block48_names=[];B48={}
for old in [k for k in list(materials) if k.startswith('M_Block48_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Yellow','TownIvory',(.93,.88,.66),.88,0),
 ('White','TownIvory',(.95,.95,.92),.82,0),
 ('Plinth','TownStone',(.72,.56,.46),.84,0),
 ('BrownFrame','TownPaintBrown',(.50,.33,.22),.55,0),
 ('Roof','TownMetalGrey',(.20,.21,.22),.55,.30),
 ('Iron','TownMetalGrey',(.08,.08,.085),.45,.40),
 ('Dark','TownMetalGrey',(.05,.055,.06),.40,.20),
 ]:
 name='M_Block48_'+key;B48[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block48_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B48;WH=M['White']

def b48_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block48_names.append(name);return Mesh(name,category)
def b48_finish(m,osm):
 obj=s21_finish(m);obj['detail_pass']=48;obj['reference_notes']='references/block48-notes.md';obj['osm_way']=osm;return obj
def yf48(X):return -140.253+(X+152.989)*(-140.143+140.253)/(-141.511+152.989)
def cas48(m,x,y,u,b,w,h,a,o=.18):
 facade_box(m,x,y,u,o-.04,b+h/2,w,.02,h,GLAZE,a)
 for q in (-w/2+.04,w/2-.04):facade_box(m,x,y,u+q,o,b+h/2,.08,.08,h,M['BrownFrame'],a)
 for zz in (b+.04,b+h-.04,b+h*.66):facade_box(m,x,y,u,o,zz,w,.08,.07,M['BrownFrame'],a)
 facade_box(m,x,y,u,o+.01,b+h/2,.07,.08,h,M['BrownFrame'],a)
 facade_box(m,x,y,u,o+.01,b+h*.33,w,.04,.03,M['BrownFrame'],a)
 facade_box(m,x,y,u,.40,b-.03,w+.10,.20,.04,M['Dark'],a)

m=b48_new('SM_Kvarnholmen_House_92379261','Kvarnholmen/Ölandsgatan north')
H=Z['yh']['height']
for w in walls('yh'):
 x,y,L,a=sf_edge(w['p'],w['q']);ox,oy=outward(w)
 if not(oy<-.9 and w['kind']=='outer'):
  if w['kind']=='outer':plain(m,w,H,M['Yellow'],M['BrownFrame'],WH,2,.9)
  else:bz_wall(m,w['p'],w['q'],w['z0'],H,[],M['Yellow'])
  continue
 S=lambda X:U(w,X,yf48(X))
 UP=[(-151.66,-150.39),(-149.31,-148.03),(-146.95,-145.73),(-144.65,-143.3)]
 GF=[(-151.66,-150.32),(-149.18,-147.84),(-146.76,-145.41)]
 up=[(S((a0+b0)/2),4.55,abs(b0-a0)-.24,1.66,0) for a0,b0 in UP]
 gf=[(S((a0+b0)/2),1.69,abs(b0-a0)-.24,1.49,0) for a0,b0 in GF]
 gate=(S(-143.22),0,2.86,3.19,0)
 bz_wall(m,w['p'],w['q'],0,H,up+gf+[gate],M['Yellow'])
 for u,b,ww,hh,r in up+gf:surround36(m,x,y,u,b,ww,hh,a,WH,.12,.39);cas48(m,x,y,u,b,ww,hh,a)
 # The gateway passage: white reveals and ceiling, the lintel beam, the iron gate just inside the front.
 gu=gate[0]
 for s in (-1,1):facade_box(m,x,y,gu+s*(1.43-.03),-2.0,1.6,.06,4.7,3.19,WH,a)
 facade_box(m,x,y,gu,-2.0,3.16,2.86,4.7,.06,WH,a)
 facade_box(m,x,y,gu,.40,3.40,3.10,.10,.40,WH,a)
 for k in range(22):facade_box(m,x,y,gu-1.35+k*2.7/21,-.30,.95,.025,.025,1.8,M['Iron'],a)
 for zz in (.1,1.0,1.85):facade_box(m,x,y,gu,-.30,zz,2.8,.04,.05,M['Iron'],a)
 facade_box(m,x,y,0,.39,.30,L,.08,.59,M['Plinth'],a)
 facade_box(m,x,y,0,.42,H-.30,L,.10,.26,WH,a);facade_box(m,x,y,0,.58,H-.10,L+.10,.45,.16,WH,a)
 town_rod(m,lp(x,y,S(-152.7),.48,.25,a),lp(x,y,S(-152.7),.48,H,a),.05,M['Plinth'],8)
 town_rod(m,lp(x,y,S(-141.7),.48,.25,a),lp(x,y,S(-141.7),.48,H,a),.05,M['Plinth'],8)
sl=roof34(m,'yh',M['Roof'],M['Yellow'])
for w in walls('yh'):
 ox,oy=outward(w)
 if oy<-.9 and w['kind']=='outer':
  x,y,L,a=sf_edge(w['p'],w['q'])
  roof_dormer(m,x,y,U(w,-147.4,yf48(-147.4)),a,H,sl,.4,.80,.65,M['Roof'],M['Roof'],WH,False)
  for zz in (H+.45,H+.8):town_rod(m,lp(x,y,-L/2,-.3,zz,a),lp(x,y,L/2,-.3,zz,a),.02,M['Iron'],6)
b48_finish(m,'92379261')

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
_C={'E':(-142.22,5.50),'W':(-151.55,5.35)}
def _cam(n):X,D_=_C[n];return X,yf48(X)-.355-D_,2.11
block48_cameras=[
 sv_camera('288_Block48_Cal_West',*_cam('W'),332,5,90),
 sv_camera('289_Block48_Cal_Gate',*_cam('E'),332,5,90),
 ('290_Block48_Aerial',(-147.0,-168.0,26.0),(-147.0,-136.0,4.0),28),
]
print('BLOCK48_GEOMETRY',len(block48_names))
