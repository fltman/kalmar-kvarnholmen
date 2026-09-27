"""Pass 68: the district volume 91926340 on the south side of Norra Långgatan, a white roughcast
single-storey cottage:
- the green door with its glazed upper panels in a white surround at the east end, and three white
  casements;
- a dark plinth and a white fascia under the eaves;
- a steep mansard roof of dark weathered tile with three white dormers, and a rendered chimney with
  a black cowl.
The yard and side walls keep a plain rhythm.

References: Google Street View April 2025 (one panorama on Norra Långgatan, resected on both
corners of the cottage), view only. Zones: source/block68.json; see references/block68-notes.md.
The aerials, the traffic signs and the street lamp are omitted.
"""
B68D=json.loads((R/'source/block68.json').read_text());Z=B68D['zones']
block68_names=[];B68={}
for old in [k for k in list(materials) if k.startswith('M_Block68_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('White','TownIvory',(.93,.93,.91),.92,0),
 ('WhiteFrame','TownPaintWhite',(.95,.95,.93),.55,0),
 ('Plinth','TownStone',(.30,.30,.31),.88,0),
 ('Door','TownPaintBrown',(.42,.52,.36),.55,0),
 ('Roof','TownTileRed',(.24,.21,.19),.90,0),
 ('Chimney','TownIvory',(.55,.43,.33),.90,0),
 ('Dark','TownMetalGrey',(.05,.055,.06),.40,.20),
 ]:
 name='M_Block68_'+key;B68[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block68_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B68;WH=M['White']

def b68_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block68_names.append(name);return Mesh(name,category)
def b68_finish(m,osm):
 obj=s21_finish(m);obj['detail_pass']=68;obj['reference_notes']='references/block68-notes.md';obj['osm_way']=osm;return obj
def yn68(X):return 61.126+(X-169.654)*(61.339-61.126)/(159.433-169.654)
def cas68(m,x,y,u,b,w,h,a,o=.16):
 facade_box(m,x,y,u,o-.04,b+h/2,w,.02,h,GLAZE,a)
 for q in (-w/2+.04,w/2-.04,0):facade_box(m,x,y,u+q,o,b+h/2,.08 if q else .06,.08,h,M['WhiteFrame'],a)
 for zz in (b+.04,b+h-.04,b+h/3,b+2*h/3):facade_box(m,x,y,u,o+(0 if zz in (b+.04,b+h-.04) else .01),zz,w,.08 if zz in (b+.04,b+h-.04) else .05,.06 if zz in (b+.04,b+h-.04) else .04,M['WhiteFrame'],a)

m=b68_new('SM_Kvarnholmen_House_91926340','Kvarnholmen/Norra Långgatan')
H=Z['cz']['height']
for w in walls('cz'):
 x,y,L,a=sf_edge(w['p'],w['q']);ox,oy=outward(w)
 if w['kind']=='outer' and oy>.9:
  S=lambda X:U(w,X,yn68(X))
  win=[(S(X0),1.39,ww,1.17,0) for X0,ww in ((166.08,.97),(164.45,.96),(161.47,1.01))]
  door=(S(168.04),.45,1.0,2.01,0)
  bz_wall(m,w['p'],w['q'],0,H,win+[door],WH)
  for u,b,ww,hh,r in win:
   cas68(m,x,y,u,b,ww,hh,a);surround36(m,x,y,u,b,ww,hh,a,M['WhiteFrame'],.09,.39)
   facade_box(m,x,y,u,.45,b-.05,ww+.22,.14,.05,M['WhiteFrame'],a)
  u,b,ww,hh,r=door
  for s in (-1,1):
   facade_box(m,x,y,u+s*ww/4,.10,b+hh/2,ww/2-.02,.06,hh,M['Door'],a)
   facade_box(m,x,y,u+s*ww/4,.14,b+hh*.72,ww/2-.20,.02,hh*.34,GLAZE,a)
   facade_box(m,x,y,u+s*ww/4,.15,b+hh*.28,ww/2-.20,.03,hh*.34,M['Door'],a)
  surround36(m,x,y,u,b,ww,hh,a,M['WhiteFrame'],.12,.39)
  facade_box(m,x,y,u,.50,b-.08,ww+.50,.40,.16,M['Plinth'],a)
  facade_box(m,x,y,0,.39,.22,L,.08,.45,M['Plinth'],a)
  facade_box(m,x,y,0,.42,H-.06,L,.10,.14,M['WhiteFrame'],a);facade_box(m,x,y,0,.62,H+.02,L+.1,.55,.06,M['WhiteFrame'],a)
  sl=(Z['cz']['top']-H)/2.2
  for X0,ww in ((167.55,1.0),(164.38,.80),(161.15,1.0)):roof_dormer(m,x,y,S(X0),a,H,sl,.60,ww,1.0,WH,M['Roof'],M['WhiteFrame'],False)
 else:
  if w['kind']=='outer':plain(m,w,H,WH,M['WhiteFrame'],WH,1,.9)
  else:bz_wall(m,w['p'],w['q'],w['z0'],H,[],WH)
roof34(m,'cz',M['Roof'],WH)
inset_roof(m,[tuple(v) for v in Z['cz']['roof']['r1']],Z['cz']['top'],1.8,.6,M['Roof'],0)
box(m,163.4,59.0,.75,.60,2.0,Z['cz']['top']-.4,M['Chimney'],0,M['Dark'])
town_rod(m,(163.4,59.0,Z['cz']['top']+1.6),(163.4,59.0,Z['cz']['top']+2.1),.14,M['Dark'],10)
b68_finish(m,'91926340')

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block68_cameras=[
 sv_camera('355_Block68_Cal_Front',165.2,67.94+.355,2.15,152,10,90),
 ('356_Block68_Aerial',(164.0,80.0,20.0),(164.0,57.0,2.0),28),
]
print('BLOCK68_GEOMETRY',len(block68_names))
