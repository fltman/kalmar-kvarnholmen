"""Pass 37: OSM way 92379313 on the south side of Södra Långgatan, east of the wooden house: the grey
office house, the yellow house number 28 and the corner house on Ölandsgatan.

The grey house: grey-brown render, three storeys; an iron gate, three shop windows, a window and the
entrance in a stone surround; a thin band; eleven axes of blue-grey casements in white surrounds on
both upper floors; a white frieze under the eaves and a dark metal roof. The yellow house: apricot
render, two storeys; a wooden garage door, shop windows in stone surrounds, a thin band, ten axes
of casements; a tile roof. The corner house: grey-brown render; three shop windows in brown
surrounds, a band, six axes of green casements in white surrounds on two floors, a tile roof hipped
toward Ölandsgatan with a dormer. The courtyard block behind is a plain lower range.

References: Google Street View April 2025 (each panorama registered on its own house's joints),
view only. Zones: source/block37.json; see references/block37-notes.md. Tenant signs, the shop
lettering and the posters in the windows are omitted.
"""
B37D=json.loads((R/'source/block37.json').read_text());Z=B37D['zones']
block37_names=[];B37={}
for old in [k for k in list(materials) if k.startswith('M_Block37_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Grey','TownIvory',(.50,.49,.46),.90,0),
 ('Apricot','TownIvory',(.93,.78,.62),.88,0),
 ('Brownish','TownIvory',(.47,.45,.41),.90,0),
 ('White','TownIvory',(.93,.93,.90),.82,0),
 ('Stone','TownStone',(.70,.66,.58),.86,0),
 ('BlueFrame','TownPaintBrown',(.30,.40,.50),.55,0),
 ('GreyFrame','TownPaintBrown',(.45,.43,.40),.55,0),
 ('GreenFrame','TownPaintBrown',(.20,.40,.22),.55,0),
 ('Wood','TownPaintBrown',(.48,.30,.18),.60,0),
 ('Tile','TownTileRed',(.58,.31,.21),.80,0),
 ('Plinth','TownStone',(.50,.49,.47),.82,0),
 ('Iron','TownMetalGrey',(.08,.08,.09),.45,.40),
 ('RoofDark','TownMetalGrey',(.28,.29,.30),.55,.30),
 ('Dark','TownMetalGrey',(.05,.055,.06),.40,.20),
 ]:
 name='M_Block37_'+key;B37[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block37_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B37;WH,ST=M['White'],M['Stone']

def b37_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block37_names.append(name);return Mesh(name,category)
def b37_finish(m,osm):
 obj=s21_finish(m);obj['detail_pass']=37;obj['reference_notes']='references/block37-notes.md';obj['osm_way']=osm;return obj
def street37(w):
 ox,oy=outward(w);return w['kind']=='outer' and oy>.9 and max(w['p'][1],w['q'][1])>-81
def olands37(w):
 ox,oy=outward(w);return w['kind']=='outer' and ox>.9 and min(w['p'][0],w['q'][0])>-42
def shop37(m,x,y,u,b,w,h,a,frame,surround,bw=.18,door_at=None):
 # Shop window: a stone surround, a wooden frame with a transom, optionally a glazed door at one end.
 surround36(m,x,y,u,b,w,h,a,surround,bw)
 facade_box(m,x,y,u,.12,b+h/2,w,.03,h,GLAZE,a)
 for q in (-w/2+.05,w/2-.05):facade_box(m,x,y,u+q,.22,b+h/2,.10,.12,h,frame,a)
 for zz in (b+.05,b+h-.05,b+h*.80):facade_box(m,x,y,u,.22,zz,w,.12,.08,frame,a)
 if door_at is not None:
  facade_box(m,x,y,u+door_at,.22,b+h*.40,.08,.12,h*.80,frame,a)
 facade_box(m,x,y,u,.44,b-.03,w+2*bw,.20,.06,surround,a)
def front37(m,zone,wall,frame,levels):
 for w in walls(zone):
  if street37(w) or olands37(w):continue
  if w['kind']!='outer':bz_wall(m,w['p'],w['q'],w['z0'],Z[zone]['height'],[],wall)
  else:plain(m,w,Z[zone]['height'],wall,frame,WH,levels,.9)
def upper37(m,x,y,S,a,axes,w,floors,frame,surround,bw=.12):
 ops=[(S(s),b,w,t-b,0) for s in axes for b,t in floors]
 return ops
def eaves37(m,x,y,L,a,H,ma,out=.45):
 facade_box(m,x,y,0,.40,H-.25,L,.10,.50,ma,a)
 facade_box(m,x,y,0,.36+out/2,H-.03,L+.10,out,.08,ma,a)
 town_rod(m,lp(x,y,-L/2,.36+out,H-.02,a),lp(x,y,L/2,.36+out,H-.02,a),.06,METAL,8)
m=b37_new('SM_Kvarnholmen_House_92379313','Kvarnholmen/Södra Långgatan south')

# ---------------------------------------------------------------- the grey house
GR=M['Grey'];HG=Z['gr']['height']
front37(m,'gr',GR,M['BlueFrame'],3)
for w in walls('gr'):
 if not street37(w):continue
 x,y,L,a=sf_edge(w['p'],w['q']);S=lambda s:L/2-s          # s from the wooden house's joint (the wall runs east to west)
 AX=[1.30,3.42,5.59,7.74,9.84,12.02,14.13,16.30,19.27,21.20,23.55]
 gf=[(S(2.83),0,2.21,3.02,0),(S(6.565),.45,3.31,2.61,0),(S(10.875),.45,3.27,2.61,0),(S(15.235),.45,3.29,2.61,0),(S(18.54),.75,1.58,2.30,0),(S(21.365),0,1.95,3.20,0)]
 up=[(S(s),b,1.23,t-b,0) for s in AX for b,t in ((4.70,6.39),(7.72,9.09))]
 bz_wall(m,w['p'],w['q'],0,HG,gf+up,GR)
 for i,(u,b,ww,hh,r) in enumerate(gf):
  if i==0:
   # The wrought-iron gate in a stone surround.
   surround36(m,x,y,u,b,ww,hh,a,ST,.18)
   facade_box(m,x,y,u,.20,hh/2,ww,.02,hh,M['Dark'],a)
   for k in range(9):town_rod(m,lp(x,y,u-ww/2+(k+.5)*ww/9,.24,.05,a),lp(x,y,u-ww/2+(k+.5)*ww/9,.24,hh-.05,a),.018,M['Iron'],6)
   for zz in (.10,1.2,hh-.10):town_rod(m,lp(x,y,u-ww/2,.24,zz,a),lp(x,y,u+ww/2,.24,zz,a),.025,M['Iron'],6)
   for sg in (-1,1):town_rod(m,lp(x,y,u+sg*ww/4-ww/8,.25,.3,a),lp(x,y,u+sg*ww/4+ww/8,.25,hh-.3,a),.018,M['Iron'],6)
  elif i==5:
   # The entrance: a glazed double door in a wide stone surround with a lintel panel.
   surround36(m,x,y,u,b,ww,hh,a,ST,.28)
   facade_box(m,x,y,u,.22,hh-.35,ww,.10,.70,ST,a)
   s21_glass(m,x,y,u,b,ww,hh-.70,a,M['Wood'],2,0,True)
  elif i==4:shop37(m,x,y,u,b,ww,hh,a,M['Wood'],ST,.16)
  else:shop37(m,x,y,u,b,ww,hh,a,M['Wood'],ST,.18,(ww/2-.55 if i==3 else None))
 for u,b,ww,hh,r in up:surround36(m,x,y,u,b,ww,hh,a,WH,.10);casement36(m,x,y,u,b,ww,hh,a,M['BlueFrame'],2,None,.20)
 plinth36(m,x,y,L,a,[(u-ww/2-.2,u+ww/2+.2) for u,b,ww,hh,r in gf if b<.45],.45,M['Plinth'])
 facade_box(m,x,y,0,.43,3.62,L,.16,.10,ST,a)
 facade_box(m,x,y,0,.39,10.06,L,.08,.48,WH,a)
 eaves37(m,x,y,L,a,HG+.05,WH,.40)
 for s in (4.32,17.40):town_rod(m,lp(x,y,S(s),.47,.30,a),lp(x,y,S(s),.47,HG,a),.05,M['GreyFrame'],8)
roof34(m,'gr',M['RoofDark'],GR)

# ---------------------------------------------------------------- the yellow house
YE=M['Apricot'];HY=Z['ye']['height']
front37(m,'ye',YE,M['GreyFrame'],2)
for w in walls('ye'):
 if not street37(w):continue
 x,y,L,a=sf_edge(w['p'],w['q']);S=lambda s:L/2-(s-25.5)
 AX=[26.93+2.49*k for k in range(10)]
 gf=[(S(28.06),0,3.62,2.68,0),(S(33.05),.35,3.72,2.33,0),(S(38.105),.35,3.85,2.33,0),(S(42.625),.35,2.83,2.33,0),(S(46.8),.35,3.2,2.33,0),(S(49.65),0,1.1,2.68,0)]
 up=[(S(s),b,1.30,t-b,0) for s in AX for b,t in ((4.06,5.52),(7.12,8.46))]
 bz_wall(m,w['p'],w['q'],0,HY,gf+up,YE)
 for i,(u,b,ww,hh,r) in enumerate(gf):
  if i==0:
   # The garage door (1951): vertical boards in a stone surround.
   surround36(m,x,y,u,b,ww,hh,a,ST,.20)
   facade_box(m,x,y,u,.20,hh/2,ww,.05,hh,M['Wood'],a)
   for k in range(1,14):facade_box(m,x,y,u-ww/2+k*ww/14,.235,hh/2,.03,.03,hh-.1,M['Dark'],a)
  elif i==5:surround36(m,x,y,u,b,ww,hh,a,ST,.16);s21_glass(m,x,y,u,b,ww,hh,a,M['Wood'],1,.80,True)
  else:shop37(m,x,y,u,b,ww,hh,a,M['Wood'],ST,.18,(ww/2-.55 if i in (1,2) else None))
 for u,b,ww,hh,r in up:casement36(m,x,y,u,b,ww,hh,a,M['GreyFrame'],3,None,.20);facade_box(m,x,y,u,.40,b-.03,ww+.10,.10,.04,METAL,a)
 plinth36(m,x,y,L,a,[(u-ww/2-.2,u+ww/2+.2) for u,b,ww,hh,r in gf if b<.35],.35,M['Plinth'])
 facade_box(m,x,y,0,.40,3.22,L,.08,.12,YE,a)
 eaves37(m,x,y,L,a,HY,YE,.35)
 town_rod(m,lp(x,y,S(30.3),.47,.30,a),lp(x,y,S(30.3),.47,HY,a),.05,M['GreyFrame'],8)
roof34(m,'ye',M['Tile'],YE)

# ---------------------------------------------------------------- the corner house
LB=M['Brownish'];HL=Z['lh']['height']
front37(m,'lh',LB,M['GreenFrame'],2)
for w in walls('lh'):
 x,y,L,a=sf_edge(w['p'],w['q'])
 if street37(w):
  S=lambda s:L/2-(s-51.2)
  AX=[52.67,54.54,56.37,58.25,60.12,61.99]
  # The shop windows reach down to about 0.05 (the pavement falls toward Ölandsgatan).
  gf=[(S(53.355),.05,3.43,2.22,0),(S(57.22),.05,3.70,2.22,0),(S(61.205),.05,3.51,2.22,0)]
  up=[(S(s),b,1.36,t-b,0) for s in AX for b,t in ((3.75,5.51),(6.72,8.26))]
  bz_wall(m,w['p'],w['q'],0,HL,gf+up,LB)
  for i,(u,b,ww,hh,r) in enumerate(gf):shop37(m,x,y,u,b,ww,hh,a,M['Wood'],M['Wood'],.20,(-ww/2+.75 if i==1 else None))
  for u,b,ww,hh,r in up:surround36(m,x,y,u,b,ww,hh,a,WH,.12);casement36(m,x,y,u,b,ww,hh,a,M['GreenFrame'],2,None,.20)
  facade_box(m,x,y,0,.42,3.07,L,.14,.20,ST,a)
  eaves37(m,x,y,L,a,HL,LB,.45)
 elif olands37(w):
  # The Ölandsgatan end of the corner house: the same two window storeys, plain.
  n=max(1,round(L/2.2));ops=[(-L/2+(k+.5)*L/n,b,1.2,t-b,0) for k in range(n) for b,t in ((3.75,5.51),(6.72,8.26))]
  bz_wall(m,w['p'],w['q'],0,HL,ops,LB)
  for u,b,ww,hh,r in ops:surround36(m,x,y,u,b,ww,hh,a,WH,.12);casement36(m,x,y,u,b,ww,hh,a,M['GreenFrame'],2,None,.20)
  plinth36(m,x,y,L,a,[],.25,M['Plinth']);eaves37(m,x,y,L,a,HL,LB,.45)
sl=roof34(m,'lh',M['Tile'],LB)
for w in walls('lh'):
 if street37(w):
  x,y,L,a=sf_edge(w['p'],w['q'])
  # The attic dormer over the middle axes (seen from the west).
  roof_dormer(m,x,y,L/2-(57.3-51.2),a,HL,sl,.9,1.1,1.0,LB,M['RoofDark'],WH,False)
  cx,cy,_=lp(x,y,L/2-(54.5-51.2),.355-4.0,0,a);box(m,cx,cy,.55,.85,12.9-11.5,11.5,M['Tile'],a,M['Dark'])

# ---------------------------------------------------------------- the courtyard block
rear35(m,'bk',M['Brownish'],M['GreyFrame'],M['RoofDark'],2)
b37_finish(m,'92379313')

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
# The cameras keep their measured distance from the modelled facade (0.355 m proud of the OSM line).
block37_cameras=[
 sv_camera('213_Block37_Cal_Grey',-93.04,-73.765,2.25,152,0),
 sv_camera('214_Block37_Cal_Grey_Roof',-93.04,-73.765,2.25,152,30),
 sv_camera('215_Block37_Cal_Yellow',-72.81,-73.715,2.25,152,0),
 sv_camera('216_Block37_Cal_Yellow_Roof',-72.81,-73.715,2.25,152,30),
 sv_camera('217_Block37_Cal_Corner',-47.26,-74.105,2.25,152,0),
 ('218_Block37_Aerial',(-60.0,-50.0,38.0),(-72.0,-90.0,6.0),28),
]
print('BLOCK37_GEOMETRY',len(block37_names))
