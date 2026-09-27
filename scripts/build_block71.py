"""Pass 71: the district volume 91926323 on the west side of Proviantgatan, a yellow boarded
two-storey house with its gable to the street:
- vertical board-and-batten cladding between white corner boards, with two white boards dividing the
  front into three bays;
- three dark-framed casements on each storey in white surrounds, and one in the gable;
- a stone plinth under a white sill board, and white barge boards;
- a tile saddle roof running back from the street.
The gap to the pass 70 house is closed at the street by white boarding; above it the infill
house's south wall, drawn by pass 70 only above the district height, is completed here.

References: Google Street View April 2025 (one panorama on Proviantgatan resected on the south corner
and the base row), view only. Zones: source/block71.json; see references/block71-notes.md.
"""
B71D=json.loads((R/'source/block71.json').read_text());Z=B71D['zones']
block71_names=[];B71={}
for old in [k for k in list(materials) if k.startswith('M_Block71_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Yellow','TownIvory',(.93,.86,.64),.80,0),
 ('White','TownIvory',(.95,.95,.93),.82,0),
 ('Frame','TownPaintBrown',(.30,.34,.32),.55,0),
 ('Plinth','TownStone',(.64,.60,.54),.90,0),
 ('Render','TownIvory',(.90,.87,.84),.92,0),
 ('Tile','TownTileRed',(.60,.31,.24),.80,0),
 ('Dark','TownMetalGrey',(.05,.055,.06),.40,.20),
 ]:
 name='M_Block71_'+key;B71[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block71_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B71;WH=M['White'];YL=M['Yellow']

def b71_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block71_names.append(name);return Mesh(name,category)
def b71_finish(m,osm):
 obj=s21_finish(m);obj['detail_pass']=71;obj['reference_notes']='references/block71-notes.md';obj['osm_way']=osm;return obj
def xe71(Y):return 176.821+(Y-16.547)*(177.048-176.821)/(24.41-16.547)
def cas71(m,x,y,u,b,w,h,a,o=.18):
 facade_box(m,x,y,u,o-.04,b+h/2,w,.02,h,GLAZE,a)
 for q in (-w/2+.04,w/2-.04,0):facade_box(m,x,y,u+q,o,b+h/2,.08 if q else .06,.08,h,M['Frame'],a)
 for zz in (b+.04,b+h-.04,b+h/3,b+2*h/3):facade_box(m,x,y,u,o+(0 if zz in (b+.04,b+h-.04) else .01),zz,w,.08 if zz in (b+.04,b+h-.04) else .05,.06 if zz in (b+.04,b+h-.04) else .04,M['Frame'],a)

m=b71_new('SM_Kvarnholmen_House_91926323','Kvarnholmen/Proviantgatan')
H=Z['gh']['height'];T=Z['gh']['top']
for w in walls('gh'):
 x,y,L,a=sf_edge(w['p'],w['q']);ox,oy=outward(w)
 if w['kind']=='outer' and ox>.9:
  S=lambda Y:U(w,xe71(Y),Y)
  gf=[(S(Y0),1.44,ww,1.27,0) for Y0,ww in ((18.36,1.20),(20.58,1.08),(22.77,1.03))]
  up=[(S(Y0),3.75,ww,1.28,0) for Y0,ww in ((18.28,1.20),(20.57,1.08),(22.79,1.03))]
  bz_wall(m,w['p'],w['q'],0,H,gf+up,YL)
  # The gable over the eaves, in the wall plane, with its window.
  ua=S(20.62);gw=(ua,5.57,.96,1.24,0)
  prof=[(-L/2,H),(L/2,H),(S(20.64),T)]
  vs=[lp(x,y,uu,o,zz,a) for o in (.005,.355) for uu,zz in prof];nn=len(prof)
  m.faces(vs,[tuple(range(nn-1,-1,-1)),tuple(range(nn,2*nn))]+[(i,(i+1)%nn,(i+1)%nn+nn,i+nn) for i in range(nn)],YL)
  facade_box(m,x,y,ua,.36,5.57+.62,.96,.02,1.24,M['Dark'],a)
  # Board-and-batten cladding, stopped at the casings.
  n=int(L/.20)
  for k in range(1,n):
   u=-L/2+k*L/n;segs=[(.70,H-.1)]
   for hu,hb,hw,hh,hr in gf+up:
    if abs(u-hu)<hw/2+.17:segs=[(l0,h0) for l,h_ in segs for l0,h0 in ((l,min(h_,hb-.16)),(max(l,hb+hh+.18),h_)) if h0-l0>.05]
   for l0,h0 in segs:facade_box(m,x,y,u,.37,(l0+h0)/2,.035,.03,h0-l0,YL,a)
  for u,b,ww,hh,r in gf+up+[gw]:
   o=.18 if b<5 else .40
   cas71(m,x,y,u,b,ww,hh,a,o);surround36(m,x,y,u,b,ww,hh,a,WH,.12,.39 if b<5 else .44)
   facade_box(m,x,y,u,.47 if b<5 else .50,b-.07,ww+.34,.16,.06,WH,a)
  for uu,ww in ((-L/2+.10,.22),(L/2-.10,.22),(S(19.55),.16),(S(21.72),.16)):facade_box(m,x,y,uu,.42,(.68+H)/2,ww,.10,H-.68,WH,a)
  facade_box(m,x,y,0,.39,.28,L,.08,.55,M['Plinth'],a);facade_box(m,x,y,0,.46,.62,L+.04,.20,.12,WH,a)
  for s in (-1,1):town_path(m,[lp(x,y,s*(L/2+.25),.46,H-.12,a),lp(x,y,S(20.64),.46,T+.14,a)],.07,WH)
  # The gap to the pass 70 house: white boarding at the street, a shadowed recess above.
  ug0,ug1=S(24.41),S(25.04);gc=(ug0+ug1)/2;gwid=abs(ug1-ug0)
  facade_box(m,x,y,gc,.10,1.25,gwid,.04,2.5,WH,a)
  for k in range(1,4):facade_box(m,x,y,gc-gwid/2+k*gwid/4,.14,1.25,.03,.03,2.5,M['Frame'],a)
  facade_box(m,x,y,gc,-.30,4.4,gwid,.04,3.8,M['Dark'],a)
 else:
  if w['kind']=='outer':plain(m,w,H,YL,M['Frame'],WH,2,.9)
  else:bz_wall(m,w['p'],w['q'],w['z0'],H,[],YL)
roof34(m,'gh',M['Tile'],YL)
box(m,169.0,20.6,.55,.75,1.2,T-.6,M['Tile'],0,M['Dark'])
# The pass 70 house's south wall below its district height, over the released strip.
bz_wall(m,(165.449,25.373),(177.066,25.043),0,6.65,[],M['Render'])
b71_finish(m,'91926323')

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block71_cameras=[
 sv_camera('363_Block71_Cal_Gable',181.24+.355,24.09,2.30,222,10,90),
 ('364_Block71_Aerial',(192.0,20.0,22.0),(170.0,20.0,3.0),28),
]
print('BLOCK71_GEOMETRY',len(block71_names))
