"""Pass 62: the district volume 91885537 on Östra Sjögatan, north of pass 61, a cream rendered
two-storey house:
- a rusticated cellar storey on a dark plinth with arched hatches, a sill band;
- five pairs of round-headed windows under segmental hoods on the ground floor and the arched door
  (22) at the north end;
- a string course, single upper windows with sills, an arched corbel frieze under the cornice, and
  a raised attic band with bracketed eaves over the middle.

References: Google Street View April 2025 (two panoramas on Östra Sjögatan anchored on the joint
with pass 61 and chained on three shared window edges), view only. Zones: source/block62.json; see
references/block62-notes.md.
"""
B62D=json.loads((R/'source/block62.json').read_text());Z=B62D['zones']
block62_names=[];B62={}
for old in [k for k in list(materials) if k.startswith('M_Block62_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Cream','TownIvory',(.90,.87,.78),.92,0),
 ('Trim','TownIvory',(.93,.91,.84),.86,0),
 ('Plinth','TownStone',(.20,.20,.20),.88,0),
 ('RedFrame','TownPaintBrown',(.45,.15,.12),.55,0),
 ('Hatch','TownPaintBrown',(.55,.18,.14),.60,0),
 ('Roof','TownMetalGrey',(.40,.20,.16),.55,.30),
 ('Dark','TownMetalGrey',(.05,.055,.06),.40,.20),
 ]:
 name='M_Block62_'+key;B62[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block62_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B62;CR=M['Cream'];TR=M['Trim']

def b62_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block62_names.append(name);return Mesh(name,category)
def b62_finish(m,osm):
 obj=s21_finish(m);obj['detail_pass']=62;obj['reference_notes']='references/block62-notes.md';obj['osm_way']=osm;return obj
def xw62(Y):return 59.2+(Y-84.011)*(59.504-59.2)/(102.845-84.011)
def cas62(m,x,y,u,b,w,h,a,o=.18):
 facade_box(m,x,y,u,o-.04,b+h/2,w,.02,h,GLAZE,a)
 for q in (-w/2+.04,w/2-.04,0):facade_box(m,x,y,u+q,o,b+h/2,.08 if q else .07,.08,h,M['RedFrame'],a)
 for zz in (b+.04,b+h-.04,b+h*.72):facade_box(m,x,y,u,o,zz,w,.08,.06,M['RedFrame'],a)
def arc62(m,x,y,u,a,spring,half,rise,o,r,ma,n=12):
 pts=[(u-half,spring)]+[(u-half*math.cos(math.pi*k/n),spring+rise*math.sin(math.pi*k/n)) for k in range(1,n)]+[(u+half,spring)]
 town_path(m,[lp(x,y,uu,o,zz,a) for uu,zz in pts],r,ma)

UPY=[101.5,98.98,96.59,94.05,91.46,88.87,86.24]
PAIRS=[96.52,94.02,91.46,88.92,86.31]
m=b62_new('SM_Kvarnholmen_House_91885537','Kvarnholmen/Östra Sjögatan')
H=Z['ow']['height']
for w in walls('ow'):
 x,y,L,a=sf_edge(w['p'],w['q']);ox,oy=outward(w)
 if w['kind']=='outer' and ox<-.9 and min(w['p'][0],w['q'][0])<60:
  S=lambda Y:U(w,xw62(Y),Y)
  up=[(S(Y0),5.36,1.08,1.55,0) for Y0 in UPY]
  gf=[(S(Y0+s*.52),2.02,.74,1.62,.30) for Y0 in PAIRS for s in (-1,1)]+[(S(101.5),2.02,1.30,1.62,.30)]
  door=(S(98.3),1.20,1.10,2.45,.40)
  hat=[(S(Y0),.13,.95,.62,.15) for Y0 in PAIRS+[101.5]]
  bz_wall(m,w['p'],w['q'],0,H,up+gf+[door]+hat,CR)
  for u,b,ww,hh,r in up:
   cas62(m,x,y,u,b,ww,hh,a);facade_box(m,x,y,u,.46,b-.06,ww+.30,.20,.08,TR,a);facade_box(m,x,y,u,.42,b+hh+.08,ww+.14,.10,.10,TR,a)
  for u,b,ww,hh,r in gf:cas62(m,x,y,u,b,ww,hh+r*.6,a)
  for Y0 in PAIRS+[101.5]:
   u=S(Y0);arc62(m,x,y,u,a,3.64,1.02,.42,.41,.09,TR)
   facade_box(m,x,y,u,.40,2.8,.28,.08,1.6,TR,a)
  u,b,ww,hh,r=door
  facade_box(m,x,y,u,.10,b+hh/2,ww,.06,hh,M['RedFrame'],a);steps36(m,x,y,u,a,1.6,1.4,b,3,.30,M['Plinth'])
  arc62(m,x,y,u,a,b+hh,ww/2+.12,r+.1,.41,.09,TR)
  for u,b,ww,hh,r in hat:facade_box(m,x,y,u,.10,b+hh/2,ww,.06,hh+r,M['Hatch'],a);arc62(m,x,y,u,a,b+hh,ww/2+.10,r+.08,.41,.07,TR)
  # The cellar storey: rusticated render on a dark plinth, the sill band over it.
  facade_box(m,x,y,0,.38,.25,L,.06,.49,M['Plinth'],a)
  for k in range(1,4):facade_box(m,x,y,0,.37,.49+k*.30,L,.01,.02,M['Trim'],a)
  facade_box(m,x,y,0,.44,1.70,L,.14,.22,TR,a)
  facade_box(m,x,y,0,.42,4.91,L,.10,.16,TR,a)
  n=int(L/.62)
  for k in range(n):arc62(m,x,y,-L/2+(k+.5)*L/n,a,7.82,.28,.12,.40,.035,TR,6)
  facade_box(m,x,y,0,.40,7.78,L,.08,.04,TR,a)
  facade_box(m,x,y,0,.44,8.35,L,.12,.50,TR,a);facade_box(m,x,y,0,.56,8.75,L+.10,.36,.30,TR,a)
  # The raised attic band over the middle, with bracketed eaves.
  ua,ub=S(99.7),S(88.8);lo,hi=min(ua,ub),max(ua,ub)
  facade_box(m,x,y,(lo+hi)/2,.18,9.3,hi-lo,.35,.80,CR,a)
  facade_box(m,x,y,(lo+hi)/2,.55,9.78,hi-lo+.4,.60,.10,M['Roof'],a)
  for k in range(int((hi-lo)/.75)+1):facade_box(m,x,y,lo+k*.75,.42,9.62,.10,.30,.16,M['Dark'],a)
 else:
  if w['kind']=='outer':plain(m,w,H,CR,M['RedFrame'],TR,2,.9)
  else:bz_wall(m,w['p'],w['q'],w['z0'],H,[],CR)
roof34(m,'ow',M['Roof'],CR)
for cy in (88.0,95.0):box(m,65.0,cy,.55,.75,1.0,Z['ow']['top']-.5,M['Roof'],0,M['Dark'])
b62_finish(m,'91885537')

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block62_cameras=[
 sv_camera('336_Block62_Cal_South',52.33-.355,83.64,2.30,62,20,90),
 sv_camera('337_Block62_Cal_North',52.61-.355,91.68,2.30,62,20,90),
 ('338_Block62_Aerial',(40.0,93.0,24.0),(66.0,93.0,4.0),28),
]
print('BLOCK62_GEOMETRY',len(block62_names))
