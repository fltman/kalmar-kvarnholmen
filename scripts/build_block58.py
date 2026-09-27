"""Pass 58: the district volume 91970261 on the corner of Fiskaregatan and Östra Sjögatan:
- the pale yellow boarded two-storey range to Fiskaregatan: nine axes of red-brown casements in
  white surrounds on both storeys, pilasters at the ends and between the axes, a dark plinth, a
  cornice and a tile roof with a snow rail and chimneys;
- the taller corner wing: a mansard roof whose gable stands to Fiskaregatan with two small windows,
  two axes on each storey below, corner pilasters with capitals, the Östra Sjögatan side plain.

References: Google Street View April 2025 (three panoramas on Fiskaregatan chained on shared window
edges, spaced as their GPS positions and anchored on both ends), view only. Zones:
source/block58.json; see references/block58-notes.md. The traffic signs and the street-name plate
are omitted.
"""
B58D=json.loads((R/'source/block58.json').read_text());Z=B58D['zones']
block58_names=[];B58={}
for old in [k for k in list(materials) if k.startswith('M_Block58_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Board','TownIvory',(.93,.89,.66),.80,0),
 ('White','TownIvory',(.95,.95,.93),.82,0),
 ('Plinth','TownStone',(.26,.20,.19),.90,0),
 ('RedFrame','TownPaintBrown',(.50,.17,.13),.55,0),
 ('Tile','TownTileRed',(.62,.34,.25),.80,0),
 ('Iron','TownMetalGrey',(.08,.08,.085),.45,.40),
 ('Dark','TownMetalGrey',(.05,.055,.06),.40,.20),
 ]:
 name='M_Block58_'+key;B58[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block58_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B58;WH=M['White'];BD=M['Board']

def b58_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block58_names.append(name);return Mesh(name,category)
def b58_finish(m,osm):
 obj=s21_finish(m);obj['detail_pass']=58;obj['reference_notes']='references/block58-notes.md';obj['osm_way']=osm;return obj
def yf58(X):return 134.027+(X-20.407)*(133.483-134.027)/(48.631-20.407)
def street58(w):ox,oy=outward(w);return w['kind']=='outer' and oy>.9 and max(w['p'][1],w['q'][1])>133.3
def cas58(m,x,y,u,b,w,h,a,o=.18):
 facade_box(m,x,y,u,o-.04,b+h/2,w,.02,h,GLAZE,a)
 for q in (-w/2+.04,w/2-.04,0):facade_box(m,x,y,u+q,o,b+h/2,.08 if q else .07,.08,h,M['RedFrame'],a)
 for zz in (b+.04,b+h-.04,b+h*.45):facade_box(m,x,y,u,o,zz,w,.08,.06,M['RedFrame'],a)

UP=[(22.36,1.06),(24.37,1.0),(26.49,1.04),(28.90,1.09),(31.10,1.15),(33.33,1.06),(35.82,.94),(37.91,.96),(39.87,1.01)]
GF=[(22.12,1.16),(24.28,1.07),(26.63,1.12),(29.25,1.13),(31.05,1.15),(33.04,1.18),(35.77,1.05),(38.00,1.05),(40.15,1.11)]
m=b58_new('SM_Kvarnholmen_House_91970261','Kvarnholmen/Fiskaregatan')
for zone in Z:
 HZ=Z[zone]['height']
 for w in walls(zone):
  x,y,L,a=sf_edge(w['p'],w['q'])
  if street58(w) and zone=='lr':
   S=lambda X:U(w,X,yf58(X))
   up=[(S(X0),3.71,ww,1.10,0) for X0,ww in UP];gf=[(S(X0),1.57,ww,1.05,0) for X0,ww in GF]
   bz_wall(m,w['p'],w['q'],0,HZ,up+gf,BD);boards35(m,x,y,L,a,.70,5.0,up+gf,BD,.22)
   for u,b,ww,hh,r in up+gf:surround36(m,x,y,u,b,ww,hh,a,WH,.12,.39);cas58(m,x,y,u,b,ww,hh,a)
   for X0,ww in ((20.7,.36),(27.9,.40),(34.3,.46),(41.0,.44)):facade_box(m,x,y,S(X0),.42,(.7+5.0)/2,ww,.10,4.3,WH,a)
   facade_box(m,x,y,0,.39,.35,L,.08,.70,M['Plinth'],a);facade_box(m,x,y,0,.42,.76,L,.12,.10,WH,a)
   facade_box(m,x,y,0,.42,5.05,L,.10,.22,WH,a);facade_box(m,x,y,0,.54,5.24,L+.10,.34,.16,WH,a)
   town_rod(m,lp(x,y,-L/2,.72,5.3,a),lp(x,y,L/2,.72,5.3,a),.07,WH,8)
   town_rod(m,lp(x,y,S(36.9),.50,.35,a),lp(x,y,S(36.9),.50,5.2,a),.05,WH,8)
   for zz in (5.9,6.15):town_rod(m,lp(x,y,-L/2+.2,-.5,zz,a),lp(x,y,L/2-.2,-.5,zz,a),.02,M['Iron'],6)
  elif street58(w) and zone=='wg':
   S=lambda X:U(w,X,yf58(X))
   up=[(S(46.75),3.60,.98,1.57,0),(S(42.66),3.60,1.20,1.57,0)];gf=[(S(46.76),1.37,1.10,1.14,0),(S(42.10),1.37,1.10,1.14,0)]
   bz_wall(m,w['p'],w['q'],0,HZ,up+gf,BD);boards35(m,x,y,L,a,.55,5.5,up+gf,BD,.22)
   for u,b,ww,hh,r in up+gf:surround36(m,x,y,u,b,ww,hh,a,WH,.13,.39);cas58(m,x,y,u,b,ww,hh,a)
   for X0 in (48.4,41.4):facade_box(m,x,y,S(X0),.44,(.55+5.6)/2,.40,.12,5.05,WH,a);facade_box(m,x,y,S(X0),.50,5.7,.62,.24,.22,WH,a)
   facade_box(m,x,y,0,.39,.28,L,.08,.55,M['Plinth'],a);facade_box(m,x,y,0,.42,.60,L,.12,.10,WH,a)
   # The gable windows sit in the mansard's upright street face (its roof edge without inset).
   for X0,ww in ((45.74,.88),(44.18,.97)):
    u=S(X0);facade_box(m,x,y,u,-.06,6.77,ww,.20,1.02,GLAZE,a);surround36(m,x,y,u,6.26,ww,1.02,a,WH,.11,.06);cas58(m,x,y,u,6.26,ww,1.02,a,-.14)
   vs=[(S(48.63),HZ),(S(46.83),Z['wg']['top']),(S(43.0),Z['wg']['top']),(S(41.2),HZ)]
   town_path(m,[lp(x,y,uu,.10,zz+.06,a) for uu,zz in vs],.08,WH)
  else:
   if w['kind']=='outer':plain(m,w,HZ,BD,M['RedFrame'],WH,2,.9)
   else:bz_wall(m,w['p'],w['q'],w['z0'],HZ,[],BD)
for g in Z['lr']['polygons']:
 pts=simplify([tuple(v) for v in g],.6)
 inset_roof(m,pts,Z['lr']['height'],min(3.0,.45*min(math.dist(p,q) for p,q in zip(pts,pts[1:]+pts[:1]))),Z['lr']['top']-Z['lr']['height'],M['Tile'],.40)
roof34(m,'wg',M['Tile'],BD)
inset_roof(m,[tuple(v) for v in Z['wg']['roof']['r1']],Z['wg']['top'],1.5,.9,M['Tile'],0)
for cx,cy in ((26.0,131.0),(34.0,131.0),(45.0,128.0)):box(m,cx,cy,.55,.75,1.0,(Z['lr']['top'] if cx<41 else Z['wg']['top']+.9)-.5,M['Tile'],0,M['Dark'])
b58_finish(m,'91970261')

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block58_cameras=[
 sv_camera('322_Block58_Cal_West',24.96,140.22+.355,2.03,152,15,90),
 sv_camera('323_Block58_Cal_Middle',36.70,139.72+.355,2.03,152,15,90),
 sv_camera('324_Block58_Cal_Wing',46.55,138.68+.355,2.03,152,20,90),
 ('325_Block58_Aerial',(34.0,160.0,26.0),(34.0,128.0,4.0),28),
]
print('BLOCK58_GEOMETRY',len(block58_names))
