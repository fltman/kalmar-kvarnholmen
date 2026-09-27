"""Pass 56: the district volume 92379307 on Västra Sjögatan, south of pass 55: the green-boarded
two-storey wooden house:
- vertical boarding between six white pilasters on a grey rendered plinth;
- five axes of green casements (six lights) in white surrounds on both storeys, the middle ground
  axis a panelled white door under a pedimented porch hood up five steps;
- a frieze and a dentil cornice, and a tile roof with a snow rail and two chimneys.

References: Google Street View April 2025 (two panoramas on Västra Sjögatan chained on shared window
edges and anchored on both corners), view only. Zones: source/block56.json; see
references/block56-notes.md. The signs and the seasonal decorations are omitted.
"""
B56D=json.loads((R/'source/block56.json').read_text());Z=B56D['zones']
block56_names=[];B56={}
for old in [k for k in list(materials) if k.startswith('M_Block56_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Board','TownIvory',(.62,.64,.45),.80,0),
 ('White','TownIvory',(.95,.95,.93),.82,0),
 ('Plinth','TownStone',(.82,.81,.78),.90,0),
 ('Sill','TownMetalGrey',(.18,.19,.19),.60,.20),
 ('GreenFrame','TownPaintBrown',(.18,.34,.22),.55,0),
 ('Tile','TownTileRed',(.55,.30,.22),.80,0),
 ('Iron','TownMetalGrey',(.08,.08,.085),.45,.40),
 ('Dark','TownMetalGrey',(.05,.055,.06),.40,.20),
 ]:
 name='M_Block56_'+key;B56[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block56_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B56;WH=M['White']

def b56_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block56_names.append(name);return Mesh(name,category)
def b56_finish(m,osm):
 obj=s21_finish(m);obj['detail_pass']=56;obj['reference_notes']='references/block56-notes.md';obj['osm_way']=osm;return obj
def xe56(Y):return -39.608+(Y+42.475)*(-39.512+39.608)/(-26.813+42.475)
def east56(w):ox,oy=outward(w);return w['kind']=='outer' and ox>.9 and max(w['p'][0],w['q'][0])>-40
def cas56(m,x,y,u,b,w,h,a,o=.18):
 facade_box(m,x,y,u,o-.04,b+h/2,w,.02,h,GLAZE,a)
 for q in (-w/2+.04,w/2-.04,0):facade_box(m,x,y,u+q,o,b+h/2,.08 if q else .07,.08,h,M['GreenFrame'],a)
 for zz in (b+.04,b+h-.04,b+h/3,b+2*h/3):facade_box(m,x,y,u,o+(0 if zz in (b+.04,b+h-.04) else .01),zz,w,.08 if zz in (b+.04,b+h-.04) else .05,.06 if zz in (b+.04,b+h-.04) else .04,M['GreenFrame'],a)
 facade_box(m,x,y,u,.44,b-.05,w+.24,.18,.06,WH,a)

UPX=[-41.12,-38.08,-34.72,-31.78,-28.77]
m=b56_new('SM_Building_92379307','Kvarnholmen/Västra Sjögatan')
H=Z['gw']['height']
for w in walls('gw'):
 x,y,L,a=sf_edge(w['p'],w['q'])
 if east56(w):
  S=lambda Y:U(w,xe56(Y),Y)
  up=[(S(Y0),5.41,1.26,1.94,0) for Y0 in UPX]
  gf=[(S(Y0),2.06,1.30,1.84,0) for Y0 in UPX if Y0!=-34.72]
  door=(S(-34.58),1.49,1.17,2.18,0)
  bz_wall(m,w['p'],w['q'],0,H,up+gf+[door],M['Board'])
  boards35(m,x,y,L,a,1.04,7.45,up+gf+[door],M['Board'])
  for u,b,ww,hh,r in up+gf:surround36(m,x,y,u,b,ww,hh,a,WH,.14,.39);cas56(m,x,y,u,b,ww,hh,a)
  u,b,ww,hh,r=door
  facade_box(m,x,y,u,.10,b+hh/2,ww,.06,hh,WH,a)
  for zz in (b+.35,b+1.0):facade_box(m,x,y,u,.14,zz,ww-.25,.02,.5,WH,a)
  facade_box(m,x,y,u,.13,b+hh*.78,ww-.4,.02,.5,GLAZE,a)
  # The porch: two white pilasters, the pedimented hood, five steps.
  for s in (-1,1):facade_box(m,x,y,u+s*(ww/2+.20),.50,(b+4.05)/2,.26,.26,4.05-b,WH,a)
  facade_box(m,x,y,u,.62,4.12,ww+.90,.50,.14,WH,a)
  prof=[(u-ww/2-.45,4.19),(u+ww/2+.45,4.19),(u,4.55)]
  vs=[lp(x,y,uu,o,zz,a) for o in (.40,.86) for uu,zz in prof];m.faces(vs,[(2,1,0),(3,4,5),(0,1,4,3),(1,2,5,4),(2,0,3,5)],M['Sill'])
  steps36(m,x,y,u,a,2.2,1.9,1.40,5,.30,M['Plinth'])
  for Y0,ww in ((-42.2,.30),(-39.81,.56),(-36.4,.49),(-33.37,.49),(-30.58,.62),(-27.07,.49)):
   facade_box(m,x,y,S(Y0),.42,(1.04+7.5)/2,ww,.10,6.46,WH,a)
  facade_box(m,x,y,0,.39,.44,L,.10,.87,M['Plinth'],a);facade_box(m,x,y,0,.44,.95,L,.14,.16,M['Sill'],a)
  facade_box(m,x,y,0,.42,7.62,L,.10,.28,WH,a)
  for k in range(int(L/.22)):facade_box(m,x,y,-L/2+.11+k*.22,.50,8.02,.10,.08,.10,WH,a)
  facade_box(m,x,y,0,.54,8.24,L+.1,.30,.26,WH,a);facade_box(m,x,y,0,.62,8.42,L+.2,.46,.12,WH,a)
  town_rod(m,lp(x,y,-L/2,.80,8.5,a),lp(x,y,L/2,.80,8.5,a),.07,M['Sill'],8)
  town_rod(m,lp(x,y,S(-42.3),.52,.9,a),lp(x,y,S(-42.3),.52,8.4,a),.05,M['Sill'],8)
  for zz in (9.05,9.3):town_rod(m,lp(x,y,-L/2+.2,-.4,zz,a),lp(x,y,L/2-.2,-.4,zz,a),.02,M['Iron'],6)
 else:
  if w['kind']=='outer':plain(m,w,H,M['Board'],M['GreenFrame'],WH,2,.9)
  else:bz_wall(m,w['p'],w['q'],w['z0'],H,[],M['Board'])
for g in Z['gw']['polygons']:
 pts=simplify([tuple(v) for v in g],.6)
 inset_roof(m,pts,H,min(3.5,.45*min(math.dist(p,q) for p,q in zip(pts,pts[1:]+pts[:1]))),Z['gw']['top']-H,M['Tile'],.40)
for cy in (-38.0,-31.0):box(m,-42.2,cy,.55,.75,1.0,Z['gw']['top']-.8,M['Tile'],0,M['Dark'])
b56_finish(m,'92379307')

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
_C={'G':(-37.97,6.14),'S':(-27.54,6.15)}
def _cam(n):Y,D_=_C[n];return xe56(Y)+.355+D_,Y,2.40
block56_cameras=[
 sv_camera('315_Block56_Cal_Porch',*_cam('G'),242,20,90),
 sv_camera('316_Block56_Cal_North',*_cam('S'),242,20,90),
 ('317_Block56_Aerial',(-22.0,-35.0,24.0),(-50.0,-35.0,4.0),28),
]
print('BLOCK56_GEOMETRY',len(block56_names))
