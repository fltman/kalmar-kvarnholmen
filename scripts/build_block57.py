"""Pass 57: the district volume 91970300 on the corner of Norra Långgatan and Östra Sjögatan, a
grey-boarded two-storey wooden house:
- to Norra Långgatan twelve upper casements in white surrounds with toothed sill boards, a string
  course, ground-floor casements over boarded panels in white frames, the red glazed double door
  (number 39) up three steps, a dark boarded gateway at the west end, a rendered plinth with cellar
  vents, a cornice and a tile roof with chimneys;
- the Östra Sjögatan end keeps a plain two-storey rhythm (seen obliquely).

References: Google Street View April 2025 (three panoramas chained on shared window edges, spaced
as their GPS positions and anchored on the Östra Sjögatan corner), view only. Zones:
source/block57.json; see references/block57-notes.md. The bicycle stands and the utility box are
omitted.
"""
B57D=json.loads((R/'source/block57.json').read_text());Z=B57D['zones']
block57_names=[];B57={}
for old in [k for k in list(materials) if k.startswith('M_Block57_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Board','TownIvory',(.80,.80,.76),.80,0),
 ('White','TownIvory',(.95,.95,.93),.82,0),
 ('Plinth','TownStone',(.74,.73,.70),.90,0),
 ('Frame','TownPaintBrown',(.22,.26,.28),.55,0),
 ('RedDoor','TownPaintBrown',(.60,.18,.14),.55,0),
 ('Gate','TownPaintBrown',(.18,.20,.21),.60,0),
 ('Tile','TownTileRed',(.62,.32,.23),.80,0),
 ('Dark','TownMetalGrey',(.05,.055,.06),.40,.20),
 ]:
 name='M_Block57_'+key;B57[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block57_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B57;WH=M['White']

def b57_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block57_names.append(name);return Mesh(name,category)
def b57_finish(m,osm):
 obj=s21_finish(m);obj['detail_pass']=57;obj['reference_notes']='references/block57-notes.md';obj['osm_way']=osm;return obj
def yf57(X):return 73.652+(X-18.612)*(73.369-73.652)/(48.281-18.612)
def street57(w):ox,oy=outward(w);return w['kind']=='outer' and oy<-.9 and min(w['p'][1],w['q'][1])<73.8
def cas57(m,x,y,u,b,w,h,a,o=.18):
 facade_box(m,x,y,u,o-.04,b+h/2,w,.02,h,GLAZE,a)
 for q in (-w/2+.04,w/2-.04,0):facade_box(m,x,y,u+q,o,b+h/2,.08 if q else .07,.08,h,M['Frame'],a)
 for zz in (b+.04,b+h-.04):facade_box(m,x,y,u,o,zz,w,.08,.07,M['Frame'],a)
 for zz in (b+h/3,b+2*h/3):facade_box(m,x,y,u,o+.01,zz,w,.05,.04,M['Frame'],a)

UP=[(21.33,1.21),(24.37,.98),(27.10,1.06),(28.98,1.17),(30.58,1.06),(32.33,1.15),(35.07,.97),(37.80,1.10),(40.10,1.24),(42.12,1.15),(44.81,1.12),(46.75,.95)]
GF=[(24.15,1.21),(27.32,1.18),(29.48,1.39),(31.87,1.32),(38.17,1.22),(40.25,1.41),(42.10,1.16),(44.80,1.04),(46.72,.96)]
m=b57_new('SM_Building_91970300','Kvarnholmen/Norra Långgatan')
H=Z['gb']['height']
for w in walls('gb'):
 x,y,L,a=sf_edge(w['p'],w['q'])
 if street57(w):
  S=lambda X:U(w,X,yf57(X))
  up=[(S(X0),3.80,ww,1.50,0) for X0,ww in UP];gf=[(S(X0),1.23,ww,1.42,0) for X0,ww in GF]
  door=(S(35.05),.84,1.35,1.73,0);gate=(S(21.22),0,1.15,2.80,0)
  bz_wall(m,w['p'],w['q'],0,H,up+gf+[door,gate],M['Board'])
  boards35(m,x,y,L,a,.66,5.6,up+gf+[door,gate],M['Board'],.22)
  for u,b,ww,hh,r in up:
   surround36(m,x,y,u,b,ww,hh,a,WH,.12,.39);cas57(m,x,y,u,b,ww,hh,a)
   for k in range(int((ww+.2)/.08)):facade_box(m,x,y,u-(ww+.2)/2+.04+k*.08,.46,b-.13,.05,.08,.06,WH,a)
   facade_box(m,x,y,u,.44,b+hh+.20,ww+.40,.12,.08,WH,a)
  for u,b,ww,hh,r in gf:
   surround36(m,x,y,u,.72,ww,hh+b-.72,a,WH,.14,.39);cas57(m,x,y,u,b,ww,hh,a)
   facade_box(m,x,y,u,.30,(.72+b)/2,ww,.06,b-.72,WH,a);facade_box(m,x,y,u,.36,(.72+b)/2,ww-.3,.02,b-.9,M['Board'],a)
  u,b,ww,hh,r=door
  for s in (-1,1):
   facade_box(m,x,y,u+s*ww/4,.10,b+hh/2,ww/2-.02,.06,hh,M['RedDoor'],a)
   facade_box(m,x,y,u+s*ww/4,.14,b+hh*.6,ww/2-.2,.02,hh*.6,GLAZE,a)
  surround36(m,x,y,u,b,ww,hh,a,WH,.16,.39);steps36(m,x,y,u,a,1.9,1.6,b,3,.30,M['Plinth'])
  u,b,ww,hh,r=gate
  for s in (-1,1):facade_box(m,x,y,u+s*ww/4,.10,hh/2,ww/2-.02,.06,hh,M['Gate'],a)
  surround36(m,x,y,u,b,ww,hh,a,WH,.14,.39)
  at=-L/2
  for uu,ww2 in sorted([(door[0],door[2]+.4),(gate[0],gate[2]+.3)])+[(L/2+2,0)]:
   lo=max(-L/2,min(L/2,uu-ww2/2))
   if lo>at+.03:facade_box(m,x,y,(at+lo)/2,.39,.33,lo-at,.08,.66,M['Plinth'],a)
   at=max(at,min(L/2,uu+ww2/2))
  for X0 in (23.9,31.8,38.3,45.9):facade_box(m,x,y,S(X0),.44,.30,.42,.04,.20,M['Dark'],a)
  facade_box(m,x,y,0,.42,.70,L,.10,.08,WH,a)
  facade_box(m,x,y,0,.42,3.05,L,.10,.22,WH,a);facade_box(m,x,y,0,.50,3.28,L+.04,.24,.12,WH,a)
  facade_box(m,x,y,0,.42,5.85,L,.10,.30,WH,a);facade_box(m,x,y,0,.54,6.25,L+.10,.34,.40,WH,a);facade_box(m,x,y,0,.64,6.48,L+.20,.52,.08,WH,a)
  for X0,ww2 in ((18.8,.32),(48.1,.32)):facade_box(m,x,y,S(X0),.42,(.66+5.7)/2,ww2,.10,5.04,WH,a)
  town_rod(m,lp(x,y,S(47.9),.55,.4,a),lp(x,y,S(47.9),.55,6.4,a),.05,WH,8)
 else:
  if w['kind']=='outer':plain(m,w,H,M['Board'],M['Frame'],WH,2,.9)
  else:bz_wall(m,w['p'],w['q'],w['z0'],H,[],M['Board'])
for g in Z['gb']['polygons']:
 pts=simplify([tuple(v) for v in g],.6)
 inset_roof(m,pts,H,min(3.5,.45*min(math.dist(p,q) for p,q in zip(pts,pts[1:]+pts[:1]))),Z['gb']['top']-H,M['Tile'],.40)
for cx in (23.5,33.0,41.0):box(m,cx,77.0,.55,.75,1.0,Z['gb']['top']-.6,M['Tile'],0,M['Dark'])
b57_finish(m,'91970300')

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block57_cameras=[
 sv_camera('318_Block57_Cal_West',25.76,68.98-.355,2.13,332,15,90),
 sv_camera('319_Block57_Cal_Door',35.75,68.27-.355,2.13,332,15,90),
 sv_camera('320_Block57_Cal_Corner',49.19,65.87-.355,2.13,322,15,90),
 ('321_Block57_Aerial',(33.0,50.0,26.0),(33.0,80.0,4.0),28),
]
print('BLOCK57_GEOMETRY',len(block57_names))
