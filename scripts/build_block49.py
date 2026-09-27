"""Pass 49: the district volume 92379272 on the south side of Ölandsgatan, from the white house to the
Kaggensgatan corner:
- the cream roughcast house: a long, nearly blank front with one white casement over a segmental-
  arched gateway (an iron gate, a boarded passage), a grey plinth, a cornice and a tile roof with one
  white dormer;
- the ochre wooden corner house: vertical boarding between corner and middle pilasters, three shop
  windows, three brown casements in white surrounds, a cornice band, and a boarded mansard storey with
  three windows, hipped at both ends under a shallow sheet roof.
The courtyard ranges and the Kaggensgatan side stay plain.

References: Google Street View April 2025 (three panoramas chained on shared window and pilaster
edges, anchored on the Kaggensgatan corner), view only. Zones: source/block49.json; see
references/block49-notes.md. The signs, the letter boxes and the pavement boards are omitted.
"""
B49D=json.loads((R/'source/block49.json').read_text());Z=B49D['zones']
block49_names=[];B49={}
for old in [k for k in list(materials) if k.startswith('M_Block49_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Cream','TownIvory',(.92,.89,.80),.90,0),
 ('Ochre','TownIvory',(.84,.63,.32),.80,0),
 ('White','TownIvory',(.95,.95,.92),.82,0),
 ('Plinth','TownStone',(.40,.40,.39),.86,0),
 ('Wood','TownPaintBrown',(.72,.52,.30),.70,0),
 ('BrownFrame','TownPaintBrown',(.46,.29,.19),.55,0),
 ('WhiteFrame','TownPaintWhite',(.94,.94,.92),.55,0),
 ('Tile','TownTileRed',(.64,.34,.25),.80,0),
 ('Roof','TownMetalGrey',(.32,.33,.34),.55,.30),
 ('Iron','TownMetalGrey',(.08,.08,.085),.45,.40),
 ('Dark','TownMetalGrey',(.05,.055,.06),.40,.20),
 ]:
 name='M_Block49_'+key;B49[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block49_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B49;WH=M['White']

def b49_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block49_names.append(name);return Mesh(name,category)
def b49_finish(m,osm):
 obj=s21_finish(m);obj['detail_pass']=49;obj['reference_notes']='references/block49-notes.md';obj['osm_way']=osm;return obj
def yf49(X):return -151.077+(X+156.926)*(-150.39+151.077)/(-181.977+156.926)
def street49(w):
 ox,oy=outward(w);return w['kind']=='outer' and oy>.9 and max(w['p'][1],w['q'][1])>-151.2
def cas49(m,x,y,u,b,w,h,a,frame,trans=.66,o=.18):
 facade_box(m,x,y,u,o-.04,b+h/2,w,.02,h,GLAZE,a)
 for q in (-w/2+.04,w/2-.04):facade_box(m,x,y,u+q,o,b+h/2,.08,.08,h,frame,a)
 for zz in (b+.04,b+h-.04,b+h*trans):facade_box(m,x,y,u,o,zz,w,.08,.07,frame,a)
 facade_box(m,x,y,u,o+.01,b+h/2,.07,.08,h,frame,a)
 for zz in (b+h*.33,b+h*.5):facade_box(m,x,y,u,o+.01,zz,w,.04,.03,frame,a)
 facade_box(m,x,y,u,o+.22,b-.03,w+.10,.20,.04,M['Dark'],a)

m=b49_new('SM_Kvarnholmen_House_92379272','Kvarnholmen/Ölandsgatan south')
for zone in Z:
 HZ=Z[zone]['height'];wall={'cr':M['Cream'],'yw':M['Ochre']}.get(zone,M['Cream'])
 for w in walls(zone):
  x,y,L,a=sf_edge(w['p'],w['q']);S=lambda X:U(w,X,yf49(X))
  if zone=='cr' and street49(w):
   gate=(S(-167.07),0,2.75,1.82,.76);win=(S(-166.8),4.34,1.50,1.22,0)
   bz_wall(m,w['p'],w['q'],0,HZ,[gate,win],wall)
   surround36(m,x,y,win[0],4.34,1.50,1.22,a,WH,.12,.39);cas49(m,x,y,win[0],4.34,1.50,1.22,a,M['WhiteFrame'])
   # The gateway: boarded reveals and ceiling through to the courtyard, the iron gate just inside.
   gu=gate[0]
   for s in (-1,1):facade_box(m,x,y,gu+s*(1.375-.03),-2.5,1.3,.06,5.7,2.6,M['Wood'],a)
   facade_box(m,x,y,gu,-2.5,2.61,2.75,5.7,.06,M['Wood'],a)
   for k in range(24):facade_box(m,x,y,gu-1.32+k*2.64/23,-.25,1.25,.025,.025,2.5,M['Iron'],a)
   for zz in (.08,1.2,2.45):facade_box(m,x,y,gu,-.25,zz,2.7,.04,.05,M['Iron'],a)
   for lo,hi in ((-L/2,gu-1.375),(gu+1.375,L/2)):facade_box(m,x,y,(lo+hi)/2,.39,.465,hi-lo,.08,.93,M['Plinth'],a)
   facade_box(m,x,y,0,.42,6.62,L,.10,.24,WH,a);facade_box(m,x,y,0,.56,6.90,L+.10,.40,.18,WH,a)
   town_rod(m,lp(x,y,-L/2+.93,.62,6.84,a),lp(x,y,L/2,.62,6.84,a),.06,M['Iron'],8)
   for X0 in (-157.15,-170.45):town_rod(m,lp(x,y,S(X0),.48,.25,a),lp(x,y,S(X0),.48,HZ,a),.05,M['Iron'],8)
  elif zone=='yw' and street49(w):
   GF=[(-172.56,1.54),(-175.405,1.63),(-179.525,1.65)];UP=[(-172.55,1.16),(-175.33,1.18),(-179.34,1.20)]
   gf=[(S(X0),1.22,ww,2.03,0) for X0,ww in GF];up=[(S(X0),4.20,ww,1.82,0) for X0,ww in UP]
   bz_wall(m,w['p'],w['q'],0,HZ,gf+up,wall)
   boards35(m,x,y,L,a,1.0,6.35,gf+up,wall)
   for u,b,ww,hh,r in gf:surround36(m,x,y,u,b,ww,hh,a,WH,.12,.39);shopfront38(m,x,y,u,b,ww,hh,a,M['BrownFrame'],1)
   for u,b,ww,hh,r in up:
    surround36(m,x,y,u,b,ww,hh,a,WH,.12,.39);cas49(m,x,y,u,b,ww,hh,a,M['BrownFrame'])
    facade_box(m,x,y,u,.46,b+hh+.20,ww+.40,.14,.08,WH,a)
   for X0,ww in ((-170.80,.32),(-177.05,.60),(-181.82,.32)):facade_box(m,x,y,S(X0),.42,(1.0+6.35)/2,ww,.10,5.35,wall,a)
   facade_box(m,x,y,0,.39,.50,L,.08,1.0,M['Plinth'],a)
   facade_box(m,x,y,0,.44,6.45,L,.14,.22,wall,a);facade_box(m,x,y,0,.52,6.62,L+.08,.30,.12,WH,a)
   town_rod(m,lp(x,y,S(-181.75),.55,.25,a),lp(x,y,S(-181.75),.55,HZ,a),.05,M['Iron'],8)
  else:
   if w['kind']=='outer':plain(m,w,HZ,wall,M['BrownFrame'] if zone=='yw' else M['WhiteFrame'],WH,2,.9)
   else:bz_wall(m,w['p'],w['q'],w['z0'],HZ,[],wall)
sl=roof34(m,'cr',M['Tile'],M['Cream'])
roof34(m,'yw',M['Ochre'],M['Ochre'])
# The shallow upper roof over the mansard's top ring.
r1=[tuple(v) for v in Z['yw']['roof']['r1']]
inset_roof(m,r1,Z['yw']['top'],2.4,.75,M['Roof'],0)
for g in Z['bk']['polygons']:
 pts=simplify([tuple(v) for v in g],.6)
 inset_roof(m,pts,Z['bk']['height'],min(2.0,.45*min(math.dist(p,q) for p,q in zip(pts,pts[1:]+pts[:1]))),1.8,M['Tile'],.30)
for w in walls('cr'):
 if street49(w):
  x,y,L,a=sf_edge(w['p'],w['q'])
  roof_dormer(m,x,y,U(w,-166.9,yf49(-166.9)),a,Z['cr']['height'],sl,.6,1.15,1.1,WH,M['Roof'],M['WhiteFrame'],False)
for w in walls('yw'):
 if street49(w):
  # The mansard storey's windows, set into the boarded steep slope.
  x,y,L,a=sf_edge(w['p'],w['q']);k=.35/(Z['yw']['top']-Z['yw']['height'])
  for X0 in (-173.2,-176.28,-179.43):
   u=U(w,X0,yf49(X0));o=.355-k*(8.16-Z['yw']['height'])
   surround36(m,x,y,u,7.54,1.21,1.24,a,WH,.12,o+.03);cas49(m,x,y,u,7.54,1.21,1.24,a,M['BrownFrame'],.66,o-.18)
for cx,cy in ((-163.0,-154.0),(-176.0,-155.0)):box(m,cx,cy,.55,.75,1.1,(Z['cr']['top'] if cx>-170.6 else Z['yw']['top']+.75)-.4,M['Tile'],0,M['Dark'])
b49_finish(m,'92379272')

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
_C={'A':(-161.21,5.64),'B':(-171.21,5.55),'C':(-180.43,5.33)}
def _cam(n):X,D_=_C[n];return X,yf49(X)+.355+D_,2.39
block49_cameras=[
 sv_camera('291_Block49_Cal_Gate',*_cam('A'),152,5,90),
 sv_camera('292_Block49_Cal_Joint',*_cam('B'),152,5,90),
 sv_camera('293_Block49_Cal_Corner',*_cam('C'),152,5,90),
 ('294_Block49_Aerial',(-170.0,-128.0,26.0),(-170.0,-160.0,4.0),28),
]
print('BLOCK49_GEOMETRY',len(block49_names))
