"""Pass 67: the district volume 91885524 on Norra Långgatan (number 51), a yellow boarded two-storey
house:
- vertical board-and-batten cladding between six white pilasters with bases and capitals;
- white-framed casements in white surrounds, a narrow pair in the east bay;
- the green double door up three stone steps under a white hood;
- a grey plinth with glass-block cellar windows under a white ledge;
- a white profiled cornice, and a red tile saddle roof with an arched red dormer.
The fenced gap to number 49 is drawn as a shadowed recess behind a white fence.

References: Google Street View April 2025 (a close panorama facing the house, resected on both
measured corners, and the pass 66 panorama at number 50 looking along the street), view only.
Zones: source/block67.json; see references/block67-notes.md. The window awnings, the lamp and the
shop sign are omitted.
"""
B67D=json.loads((R/'source/block67.json').read_text());Z=B67D['zones']
block67_names=[];B67={}
for old in [k for k in list(materials) if k.startswith('M_Block67_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Yellow','TownIvory',(.93,.82,.58),.80,0),
 ('White','TownIvory',(.96,.96,.94),.82,0),
 ('WhiteFrame','TownPaintWhite',(.95,.95,.93),.55,0),
 ('Plinth','TownIvory',(.55,.57,.60),.90,0),
 ('Door','TownPaintBrown',(.27,.32,.27),.55,0),
 ('RedDormer','TownPaintBrown',(.55,.18,.14),.60,0),
 ('Tile','TownTileRed',(.62,.30,.22),.80,0),
 ('Step','TownStone',(.80,.80,.78),.85,0),
 ('Dark','TownMetalGrey',(.05,.055,.06),.40,.20),
 ]:
 name='M_Block67_'+key;B67[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block67_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B67;WH=M['White'];YL=M['Yellow']

def b67_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block67_names.append(name);return Mesh(name,category)
def b67_finish(m,osm):
 obj=s21_finish(m);obj['detail_pass']=67;obj['reference_notes']='references/block67-notes.md';obj['osm_way']=osm;return obj
def ys67(X):return 72.403+(X-134.275)*(71.859-72.403)/(149.9-134.275)
def cas67(m,x,y,u,b,w,h,a,o=.18):
 facade_box(m,x,y,u,o-.04,b+h/2,w,.02,h,GLAZE,a)
 for q in (-w/2+.04,w/2-.04,0):facade_box(m,x,y,u+q,o,b+h/2,.08 if q else .07,.08,h,M['WhiteFrame'],a)
 for zz in (b+.04,b+h-.04,b+h/3,b+2*h/3):facade_box(m,x,y,u,o+(0 if zz in (b+.04,b+h-.04) else .01),zz,w,.08 if zz in (b+.04,b+h-.04) else .05,.06 if zz in (b+.04,b+h-.04) else .04,M['WhiteFrame'],a)

PIL=[(135.1,.60),(139.07,.56),(141.75,.60),(144.38,.56),(146.85,.60),(149.6,.60)]
WIN=[(137.1,1.35),(140.45,1.30),(143.1,1.30),(148.2,.80)]
DOOR=145.45;UP=WIN[:3]+[(145.7,1.35),WIN[3]]
m=b67_new('SM_Kvarnholmen_House_91885524','Kvarnholmen/Norra Långgatan')
H=Z['yh']['height']
for w in walls('yh'):
 x,y,L,a=sf_edge(w['p'],w['q']);ox,oy=outward(w)
 if w['kind']=='outer' and oy<-.9:
  S=lambda X:U(w,X,ys67(X))
  gf=[(S(X0),1.71,ww,1.69,0) for X0,ww in WIN];up=[(S(X0),4.49,ww,1.79,0) for X0,ww in UP]
  door=(S(DOOR),1.0,1.05,2.15,0)
  cel=[(S(X0),.30,.85,.40,0) for X0,ww in WIN]
  bz_wall(m,w['p'],w['q'],0,H,gf+up+[door]+cel,YL)
  lo_u=S(134.8)
  # The board-and-batten cladding east of the gap, stopped at the casings.
  n=int((L/2-lo_u)/.20)
  for k in range(1,n):
   u=lo_u+k*(L/2-lo_u)/n;segs=[(1.12,6.5)]
   for hu,hb,hw,hh,hr in gf+up+[door]:
    if abs(u-hu)<hw/2+.17:segs=[(l0,h0) for l,h_ in segs for l0,h0 in ((l,min(h_,hb-.16)),(max(l,hb+hh+.20),h_)) if h0-l0>.05]
   for l0,h0 in segs:facade_box(m,x,y,u,.37,(l0+h0)/2,.035,.03,h0-l0,YL,a)
  for u,b,ww,hh,r in gf+up:
   surround36(m,x,y,u,b,ww,hh,a,WH,.12,.39);cas67(m,x,y,u,b,ww,hh,a)
   facade_box(m,x,y,u,.46,b-.08,ww+.32,.16,.06,WH,a)
  for u,b,ww,hh,r in up:facade_box(m,x,y,u,.46,b+hh+.20,ww+.34,.14,.07,WH,a)
  u,b,ww,hh,r=door
  for s in (-1,1):
   facade_box(m,x,y,u+s*ww/4,.10,b+(hh-.45)/2,ww/2-.02,.06,hh-.45,M['Door'],a)
   for zz in (b+.45,b+1.20):facade_box(m,x,y,u+s*ww/4,.14,zz,ww/2-.22,.03,.55,M['Door'],a)
  facade_box(m,x,y,u,.12,b+hh-.22,ww,.02,.40,GLAZE,a);facade_box(m,x,y,u,.16,b+hh-.44,ww,.06,.05,M['Door'],a)
  for s in (-1,1):facade_box(m,x,y,u+s*(ww/2+.12),.44,b+hh/2,.22,.12,hh,WH,a)
  facade_box(m,x,y,u,.46,b+hh+.22,ww+.60,.14,.44,WH,a);facade_box(m,x,y,u,.56,b+hh+.50,ww+.80,.34,.12,WH,a)
  steps36(m,x,y,u,a,1.9,1.5,b,3,.32,M['Step'])
  for u,b,ww,hh,r in cel:
   facade_box(m,x,y,u,.44,b+hh/2,ww,.02,hh,M['Dark'],a)
   for k in range(1,4):facade_box(m,x,y,u-ww/2+k*ww/4,.46,b+hh/2,.03,.03,hh,M['WhiteFrame'],a)
   facade_box(m,x,y,u,.46,b+hh/2,ww,.03,.03,M['WhiteFrame'],a)
  # The pilasters: bases on the plinth ledge, plain shafts, capitals under the cornice.
  for X0,ww in PIL:
   uu=S(X0);facade_box(m,x,y,uu,.46,3.8,ww,.16,5.0,WH,a)
   facade_box(m,x,y,uu,.50,1.45,ww+.14,.24,.66,WH,a);facade_box(m,x,y,uu,.52,6.35,ww+.18,.28,.20,WH,a)
  # The plinth and its ledge, stopped at the steps.
  dl,dh=door[0]-1.0,door[0]+1.0
  for lo,hi in ((lo_u,dl),(dh,L/2)):facade_box(m,x,y,(lo+hi)/2,.39,.50,hi-lo,.08,1.0,M['Plinth'],a);facade_box(m,x,y,(lo+hi)/2,.50,1.06,hi-lo,.30,.12,WH,a)
  # The gap to number 49: a shadowed recess behind a white fence.
  gw=lo_u+L/2;gu=-L/2+gw/2
  facade_box(m,x,y,gu,.37,H/2,gw,.02,H,M['Dark'],a)
  for k in range(4):facade_box(m,x,y,-L/2+(k+.5)*gw/4,.50,.80,.08,.03,1.60,WH,a)
  for zz in (.35,1.30):facade_box(m,x,y,gu,.48,zz,gw,.03,.08,WH,a)
  # The cornice and the eaves.
  facade_box(m,x,y,S(135.1)/2+S(149.9)/2,.42,6.55,S(149.9)-S(135.1)+.6,.12,.20,WH,a)
  facade_box(m,x,y,S(135.1)/2+S(149.9)/2,.56,6.78,S(149.9)-S(135.1)+.7,.40,.26,WH,a)
  facade_box(m,x,y,S(135.1)/2+S(149.9)/2,.72,6.96,S(149.9)-S(135.1)+.8,.70,.10,WH,a)
  sl=(Z['yh']['top']-H)/4.9
  roof_dormer(m,x,y,S(143.1),a,H+.4*sl,sl,.35,1.0,.95,M['RedDormer'],M['RedDormer'],M['WhiteFrame'],True)
 else:
  if w['kind']=='outer':plain(m,w,H,YL,M['WhiteFrame'],WH,2,.9)
  else:bz_wall(m,w['p'],w['q'],w['z0'],H,[],YL)
roof34(m,'yh',M['Tile'],YL)
for cx in (139.5,145.0):box(m,cx,79.5,.55,.75,1.0,Z['yh']['top']-.9,M['Tile'],0,M['Dark'])
b67_finish(m,'91885524')

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block67_cameras=[
 sv_camera('352_Block67_Cal_Front',142.63,68.17-.355,2.55,332,15,90),
 sv_camera('353_Block67_Cal_Along',132.05,68.51-.355,2.57,22,10,90),
 ('354_Block67_Aerial',(142.0,55.0,24.0),(142.0,78.0,4.0),28),
]
print('BLOCK67_GEOMETRY',len(block67_names))
