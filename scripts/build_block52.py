"""Pass 52: the district volumes 91856606 and 91856592 on the south side of Ölandsgatan, west of
Kaggensgatan:
- the cream corner house (91856606): to Ölandsgatan three tall shop windows and a glazed door under
  four red-framed casements, white corner pilasters with capitals at the eaves, and a steep gable
  with two small windows under a hipped top; its long Kaggensgatan side keeps a plain rhythm (seen
  only obliquely);
- the grey-white house with green windows (91856592): shop windows, a green door, casements in flat
  surrounds, a pilaster strip, a cornice and a tile roof with two roof lights.

References: Google Street View April 2025 (two panoramas, each anchored on the houses' corners and
joints; one view tilted up for the corner house's gable; an oblique view from the Kaggensgatan
crossing), view only. Zones: source/block52.json; see references/block52-notes.md. The shop signs,
the posters and the parking sign are omitted.
"""
B52D=json.loads((R/'source/block52.json').read_text());Z=B52D['zones']
block52_names=[];B52={}
for old in [k for k in list(materials) if k.startswith('M_Block52_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Cream','TownIvory',(.95,.86,.70),.88,0),
 ('GreyWhite','TownIvory',(.86,.85,.80),.90,0),
 ('White','TownIvory',(.95,.95,.93),.84,0),
 ('Plinth','TownStone',(.52,.52,.51),.88,0),
 ('RedFrame','TownPaintBrown',(.60,.18,.14),.55,0),
 ('GreenFrame','TownPaintBrown',(.33,.47,.30),.55,0),
 ('GreenDoor','TownPaintWhite',(.56,.66,.58),.60,0),
 ('Tile','TownTileRed',(.68,.36,.25),.80,0),
 ('Iron','TownMetalGrey',(.08,.08,.085),.45,.40),
 ('Dark','TownMetalGrey',(.05,.055,.06),.40,.20),
 ]:
 name='M_Block52_'+key;B52[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block52_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B52;WH=M['White']

def b52_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block52_names.append(name);return Mesh(name,category)
def b52_finish(m,osm):
 obj=s21_finish(m);obj['detail_pass']=52;obj['reference_notes']='references/block52-notes.md';obj['osm_way']=osm;return obj
def yf52(X):return -151.297+(X+194.937)*(-150.917+151.297)/(-223.797+194.937)
def street52(w):
 ox,oy=outward(w);return w['kind']=='outer' and oy>.9 and max(w['p'][1],w['q'][1])>-151.4
def cas52(m,x,y,u,b,w,h,a,frame,rows=(.62,),o=.18):
 facade_box(m,x,y,u,o-.04,b+h/2,w,.02,h,GLAZE,a)
 for q in (-w/2+.04,w/2-.04):facade_box(m,x,y,u+q,o,b+h/2,.08,.08,h,frame,a)
 for zz in (b+.04,b+h-.04):facade_box(m,x,y,u,o,zz,w,.08,.07,frame,a)
 facade_box(m,x,y,u,o+.01,b+h/2,.07,.08,h,frame,a)
 for t in rows:facade_box(m,x,y,u,o+.01,b+h*t,w,.05,.05,frame,a)
 facade_box(m,x,y,u,o+.22,b-.03,w+.10,.20,.04,M['Plinth'],a)
def plinth52(m,x,y,L,a,H,gaps,ma):
 at=-L/2
 for u,w in sorted(gaps)+[(L/2+1,0)]:
  lo=max(-L/2,min(L/2,u-w/2))
  if lo>at+.03:facade_box(m,x,y,(at+lo)/2,.39,H/2,lo-at,.08,H,ma,a)
  at=max(at,min(L/2,u+w/2))

meshes={Z[z]['mesh']:b52_new(Z[z]['mesh'],'Kvarnholmen/Ölandsgatan south') for z in Z}
for zone in Z:
 m=meshes[Z[zone]['mesh']];HZ=Z[zone]['height'];wall=M['Cream'] if zone=='ch' else M['GreyWhite']
 for w in walls(zone):
  x,y,L,a=sf_edge(w['p'],w['q']);S=lambda X:U(w,X,yf52(X))
  if zone=='ch' and street52(w):
   shops=[(S(-195.97),.75,1.60,3.39,0),(S(-198.60),.75,1.61,3.39,0),(S(-201.31),.75,1.52,3.39,0)]
   door=(S(-204.09),.20,1.33,3.94,0)
   up=[(S(X0),6.37,ww,2.0,0) for X0,ww in ((-196.0,1.51),(-198.68,1.52),(-201.36,1.42),(-204.09,1.42))]
   bz_wall(m,w['p'],w['q'],0,HZ,shops+[door]+up,wall)
   for u,b,ww,hh,r in shops+[door]:
    surround36(m,x,y,u,b,ww,hh,a,M['GreyWhite'],.16,.38)
    facade_box(m,x,y,u,.14,b+hh/2,ww,.02,hh,GLAZE,a)
    for q in (-ww/2+.05,ww/2-.05):facade_box(m,x,y,u+q,.20,b+hh/2,.10,.10,hh,M['RedFrame'],a)
    for zz in (b+.05,b+hh-.05,b+hh*.78):facade_box(m,x,y,u,.20,zz,ww,.10,.10,M['RedFrame'],a)
   facade_box(m,x,y,door[0],.20,door[1]+door[3]*.52,door[2],.10,.10,M['RedFrame'],a)
   for u,b,ww,hh,r in up:surround36(m,x,y,u,b,ww,hh,a,M['GreyWhite'],.14,.38);cas52(m,x,y,u,b,ww,hh,a,M['RedFrame'],(.70,))
   plinth52(m,x,y,L,a,.45,[(door[0],door[2]+.32)],M['Plinth'])
   # White corner pilasters with capitals at the eaves.
   for u0,ww in ((S(-195.19),.50),(S(-205.86),.76)):
    facade_box(m,x,y,u0,.42,(.45+10.0)/2,ww,.10,9.55,WH,a);facade_box(m,x,y,u0,.48,10.12,ww+.24,.22,.26,WH,a)
   for X0 in (-199.2,-201.7,-203.4):facade_box(m,x,y,S(X0),.38,5.3,.04,.03,.5,M['Iron'],a)
   # The steep street gable (the roof ring's edge without inset) carries two small windows.
   for X0 in (-199.2,-201.7):
    u=S(X0);facade_box(m,x,y,u,-.06,11.05,1.10,.20,1.30,GLAZE,a);surround36(m,x,y,u,10.40,1.10,1.30,a,M['GreyWhite'],.10,.06)
    cas52(m,x,y,u,10.40,1.10,1.30,a,M['RedFrame'],(.62,),-.14)
  elif zone=='gh' and street52(w):
   shops=[(S(X0),.56,ww,2.02,0) for X0,ww in ((-208.23,1.57),(-210.66,1.71),(-214.2,1.30),(-217.53,1.68),(-221.66,1.69))]
   door=(S(-219.55),.11,1.49-.3,2.37,0)
   up=[(S(X0),3.64,ww,1.50,0) for X0,ww in ((-208.85,1.37),(-211.8,1.40),(-214.9,1.35),(-217.93,1.32),(-221.55,1.24))]
   bz_wall(m,w['p'],w['q'],0,HZ,shops+[door]+up,wall)
   for u,b,ww,hh,r in shops:surround36(m,x,y,u,b,ww,hh,a,M['GreyWhite'],.10,.38);shopfront38(m,x,y,u,b,ww,hh,a,M['GreenFrame'],1)
   for u,b,ww,hh,r in up:surround36(m,x,y,u,b,ww,hh,a,M['GreyWhite'],.12,.39);cas52(m,x,y,u,b,ww,hh,a,M['GreenFrame'],(.5,))
   u,b,ww,hh,r=door;facade_box(m,x,y,u,.10,b+hh/2,ww,.06,hh,M['GreenDoor'],a);facade_box(m,x,y,u+.1,.13,b+hh*.72,ww*.45,.02,hh*.3,GLAZE,a)
   for zz in (b+.5,b+1.1):facade_box(m,x,y,u-.25,.14,zz,ww*.35,.02,.45,M['GreenFrame'],a)
   surround36(m,x,y,u,b,ww,hh,a,M['GreyWhite'],.12,.38)
   plinth52(m,x,y,L,a,.35,[(door[0],door[2]+.24)],M['Plinth'])
   facade_box(m,x,y,S(-215.93),.40,(.35+HZ)/2,.36,.08,HZ-.35,M['GreyWhite'],a)
   facade_box(m,x,y,0,.42,HZ-.25,L,.10,.22,WH,a);facade_box(m,x,y,0,.52,HZ-.06,L+.10,.30,.16,WH,a)
   town_rod(m,lp(x,y,-L/2,.66,HZ-.02,a),lp(x,y,L/2,.66,HZ-.02,a),.06,M['Dark'],8)
   town_rod(m,lp(x,y,S(-206.6),.50,.25,a),lp(x,y,S(-206.6),.50,HZ,a),.05,M['Dark'],8)
  else:
   if w['kind']=='outer':plain(m,w,HZ,wall,M['RedFrame'] if zone=='ch' else M['GreenFrame'],WH,2,.9)
   else:bz_wall(m,w['p'],w['q'],w['z0'],HZ,[],wall)
mc,mg=meshes['SM_Kvarnholmen_House_91856606'],meshes['SM_Kvarnholmen_House_91856592']
roof34(mc,'ch',M['Tile'],M['Cream'])
inset_roof(mc,[tuple(v) for v in Z['ch']['roof']['r1']],Z['ch']['top'],2.4,2.5,M['Tile'],0)
for g in Z['gh']['polygons']:
 pts=simplify([tuple(v) for v in g],.6)
 inset_roof(mg,pts,Z['gh']['height'],min(3.0,.45*min(math.dist(p,q) for p,q in zip(pts,pts[1:]+pts[:1]))),Z['gh']['top']-Z['gh']['height'],M['Tile'],.35)
for w in walls('gh'):
 if street52(w):
  x,y,L,a=sf_edge(w['p'],w['q'])
  for X0 in (-219.47,-220.68):
   u=U(w,X0,yf52(X0));facade_box(mg,x,y,u,-1.2,Z['gh']['height']+1.15,.62,.06,.90,GLAZE,a);facade_box(mg,x,y,u,-1.18,Z['gh']['height']+1.15,.72,.04,1.0,M['Dark'],a)
for cx,cy,mm,zz in ((-200.0,-160.0,mc,Z['ch']['top']+2.5),(-214.0,-153.8,mg,Z['gh']['top'])):box(mm,cx,cy,.60,.80,1.0,zz-.4,M['Tile'],0,M['Dark'])
b52_finish(mc,'91856606');b52_finish(mg,'91856592')

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
_C={'A':(-203.45,5.65),'B':(-223.56,6.37)}
def _cam(n):X,D_=_C[n];return X,yf52(X)+.355+D_,2.64
block52_cameras=[
 sv_camera('302_Block52_Cal_Corner',*_cam('A'),152,5,90),
 sv_camera('303_Block52_Cal_Green',*_cam('B'),152,5,90),
 ('304_Block52_Aerial',(-209.0,-128.0,26.0),(-209.0,-160.0,4.0),28),
]
print('BLOCK52_GEOMETRY',len(block52_names))
