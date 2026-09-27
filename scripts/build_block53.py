"""Pass 53: the district volumes 91856590 and 91856614 on the south side of Ölandsgatan, west of pass
52:
- Ölandsgatan 8 (91856590): three storeys; a sandstone-clad ground floor with four shop windows and
  a portal (wooden double doors under a panel with the number), a band, two storeys of white
  casements in flat surrounds, rusticated quoins at both ends, a cornice, a low sheet roof and a
  lantern with two windows set back on it;
- the pale yellow wooden house (91856614): vertical boarding between six pilasters, five upper and
  four ground-floor casements, a panelled double door up two steps in the middle, a cornice, a tile
  roof and a slate-hung dormer.

References: Google Street View April 2025 (two panoramas chained on nine shared edges and spaced as
their GPS positions; one view tilted up for the cornice and the lantern), view only. Zones:
source/block53.json; see references/block53-notes.md. The shop signs and the letter boards are
omitted.
"""
B53D=json.loads((R/'source/block53.json').read_text());Z=B53D['zones']
block53_names=[];B53={}
for old in [k for k in list(materials) if k.startswith('M_Block53_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Plaster','TownIvory',(.93,.91,.86),.88,0),
 ('Sandstone','TownStone',(.80,.74,.62),.86,0),
 ('Board','TownIvory',(.90,.86,.68),.78,0),
 ('White','TownIvory',(.95,.95,.93),.84,0),
 ('Plinth','TownStone',(.55,.53,.50),.88,0),
 ('WhiteFrame','TownPaintWhite',(.92,.92,.90),.55,0),
 ('GreyFrame','TownPaintWhite',(.70,.70,.66),.55,0),
 ('Oak','TownPaintBrown',(.62,.44,.26),.60,0),
 ('Tile','TownTileRed',(.52,.30,.24),.80,0),
 ('Roof','TownMetalGrey',(.22,.23,.24),.55,.30),
 ('Iron','TownMetalGrey',(.08,.08,.085),.45,.40),
 ('Dark','TownMetalGrey',(.05,.055,.06),.40,.20),
 ]:
 name='M_Block53_'+key;B53[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block53_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B53;WH=M['White']

def b53_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block53_names.append(name);return Mesh(name,category)
def b53_finish(m,osm):
 obj=s21_finish(m);obj['detail_pass']=53;obj['reference_notes']='references/block53-notes.md';obj['osm_way']=osm;return obj
def yf53(X):return -150.917+(X+223.797)*(-150.564+150.917)/(-249.826+223.797)
def street53(w):
 ox,oy=outward(w);return w['kind']=='outer' and oy>.9 and max(w['p'][1],w['q'][1])>-150.8
def cas53(m,x,y,u,b,w,h,a,frame,rows=(.62,),o=.18):
 facade_box(m,x,y,u,o-.04,b+h/2,w,.02,h,GLAZE,a)
 for q in (-w/2+.04,w/2-.04):facade_box(m,x,y,u+q,o,b+h/2,.08,.08,h,frame,a)
 for zz in (b+.04,b+h-.04):facade_box(m,x,y,u,o,zz,w,.08,.07,frame,a)
 facade_box(m,x,y,u,o+.01,b+h/2,.07,.08,h,frame,a)
 for t in rows:facade_box(m,x,y,u,o+.01,b+h*t,w,.05,.05,frame,a)
 facade_box(m,x,y,u,o+.22,b-.03,w+.10,.20,.04,M['Plinth'],a)
def quoins53(m,x,y,u,a,z0,z1,side):
 k=0;z=z0
 while z<z1-.05:
  hh=min(.34,z1-z);ww=.66 if k%2==0 else .44
  facade_box(m,x,y,u+side*ww/2,.37,z+hh/2,ww,.05,hh-.03,M['Sandstone'],a);z+=hh;k+=1
def mid(a0,b0):return (a0+b0)/2,abs(b0-a0)

meshes={Z[z]['mesh']:b53_new(Z[z]['mesh'],'Kvarnholmen/Ölandsgatan south') for z in Z}
for zone in Z:
 m=meshes[Z[zone]['mesh']];HZ=Z[zone]['height'];wall=M['Plaster'] if zone=='o8' else M['Board']
 for w in walls(zone):
  x,y,L,a=sf_edge(w['p'],w['q']);S=lambda X:U(w,X,yf53(X))
  if zone=='o8' and street53(w):
   shops=[(S(c),.46,ww-.20,2.53,0) for c,ww in (mid(-225.12,-227.86),mid(-228.7,-231.41),mid(-235.97,-238.66))]
   door=(S(-233.80),.06,2.54,2.93,0)
   up1=[(S(c),4.49,ww-.16,1.69,0) for c,ww in (mid(-226.23,-227.71),mid(-229.59,-231.09),mid(-233.02,-234.5),mid(-236.45,-237.94))]
   up2=[(S(c),7.77,ww-.16,1.57,0) for c,ww in (mid(-226.57,-227.96),mid(-229.94,-231.22),mid(-233.12,-234.54),mid(-236.45,-237.88))]
   cel=[(u,.08,ww,.30,0) for u,b,ww,hh,r in shops]
   bz_wall(m,w['p'],w['q'],0,HZ,shops+[door]+up1+up2+cel,M['Plaster'])
   # The sandstone ground floor: a cladding coat cut at the openings, piers, the band over it.
   bz_wall(m,w['p'],w['q'],0,3.83,shops+[door]+cel,M['Sandstone'],.355,.40)
   facade_box(m,x,y,0,.43,3.90,L,.10,.14,M['Sandstone'],a)
   for u,b,ww,hh,r in shops:
    facade_box(m,x,y,u,.14,b+hh/2,ww,.02,hh,GLAZE,a)
    for q in (-ww/2+.04,ww/2-.04):facade_box(m,x,y,u+q,.20,b+hh/2,.08,.08,hh,M['WhiteFrame'],a)
    for zz in (b+.04,b+hh-.04):facade_box(m,x,y,u,.20,zz,ww,.08,.08,M['WhiteFrame'],a)
    facade_box(m,x,y,u,.20,.23,ww,.10,.30,M['Dark'],a)
   u,b,ww,hh,r=door
   for s in (-1,1):facade_box(m,x,y,u+s*(ww/2+.12),.46,(b+hh+.9)/2,.24,.10,hh+.9-b,M['Sandstone'],a)
   facade_box(m,x,y,u,.46,3.50,ww+.48,.10,.60,M['Sandstone'],a);facade_box(m,x,y,u,.52,3.50,ww-.2,.02,.36,M['Plaster'],a)
   facade_box(m,x,y,u,-.35,b+hh/2,1.30,.08,hh,M['Oak'],a)
   for s in (-1,1):facade_box(m,x,y,u+s*.95,-.2,b+hh/2,.50,.08,hh,M['Oak'],a)
   for s in (-.33,.33):facade_box(m,x,y,u+s,-.30,b+hh*.62,.46,.02,hh*.36,GLAZE,a)
   facade_box(m,x,y,u,-.30,b+hh-.22,1.2,.02,.30,GLAZE,a)
   steps36(m,x,y,u,a,ww,ww-.1,b+.12,2,.25,M['Sandstone'])
   for u,b,ww,hh,r in up1+up2:surround36(m,x,y,u,b,ww,hh,a,M['GreyFrame'],.12,.38);cas53(m,x,y,u,b,ww,hh,a,M['WhiteFrame'],(.64,))
   quoins53(m,x,y,-L/2,a,3.97,HZ-.8,1);quoins53(m,x,y,L/2,a,3.97,HZ-.8,-1)
   facade_box(m,x,y,0,.42,10.60,L,.10,.26,M['WhiteFrame'],a);facade_box(m,x,y,0,.54,10.98,L+.10,.34,.50,M['WhiteFrame'],a)
   town_rod(m,lp(x,y,-L/2,.72,11.25,a),lp(x,y,L/2,.72,11.25,a),.07,M['Dark'],8)
   for X0 in (-224.6,-239.1):town_rod(m,lp(x,y,S(X0),.50,.25,a),lp(x,y,S(X0),.50,HZ,a),.05,M['Dark'],8)
  elif zone=='wd' and street53(w):
   ups=[(S(c),3.27,ww-.12,1.06,0) for c,ww in (mid(-240.78,-241.68),mid(-242.4,-243.4),mid(-244.27,-245.22),mid(-246.06,-247.1),mid(-247.75,-248.83))]
   gfs=[(S(c),1.25,ww-.12,1.01,0) for c,ww in (mid(-240.64,-241.68),mid(-242.31,-243.4),mid(-246.08,-247.16),mid(-247.88,-248.94))]
   door=(S(-244.70),.88,1.03,1.48,0)
   bz_wall(m,w['p'],w['q'],0,HZ,ups+gfs+[door],M['Board'])
   boards35(m,x,y,L,a,.51,5.15,ups+gfs+[door],M['Board'])
   for u,b,ww,hh,r in ups+gfs:
    surround36(m,x,y,u,b,ww,hh,a,M['WhiteFrame'],.10,.39);cas53(m,x,y,u,b,ww,hh,a,M['GreyFrame'],(.5,))
    facade_box(m,x,y,u,.44,b+hh+.18,ww+.30,.14,.08,M['WhiteFrame'],a)
   u,b,ww,hh,r=door
   for s in (-1,1):
    facade_box(m,x,y,u+s*ww/4,.10,b+hh/2,ww/2-.02,.06,hh,M['GreyFrame'],a)
    facade_box(m,x,y,u+s*ww/4,.14,b+hh*.72,ww/2-.2,.02,hh*.34,GLAZE,a)
   surround36(m,x,y,u,b,ww,hh,a,M['WhiteFrame'],.10,.39);facade_box(m,x,y,u,.44,2.60,ww+.3,.10,.18,M['WhiteFrame'],a)
   steps36(m,x,y,u,a,1.5,1.3,b,3,.30,M['Plinth'])
   for c,ww in (mid(-239.84,-240.25),mid(-241.79,-242.18),mid(-243.78,-244.16),mid(-245.44,-245.66),mid(-247.33,-247.6),mid(-249.33,-249.83)):
    facade_box(m,x,y,S(c),.42,(.51+5.21)/2,max(ww,.26),.08,4.70,M['WhiteFrame'],a)
   facade_box(m,x,y,0,.39,.26,L,.08,.51,M['Plinth'],a)
   facade_box(m,x,y,0,.42,5.32,L,.10,.22,M['WhiteFrame'],a);facade_box(m,x,y,0,.54,5.56,L+.10,.34,.20,M['WhiteFrame'],a)
   town_rod(m,lp(x,y,-L/2,.72,5.63,a),lp(x,y,L/2,.72,5.63,a),.07,M['Dark'],8)
  else:
   if w['kind']=='outer':plain(m,w,HZ,wall,M['WhiteFrame'],WH,3 if zone=='o8' else 2,.9)
   else:bz_wall(m,w['p'],w['q'],w['z0'],HZ,[],wall)
mo,mw=meshes['SM_Kvarnholmen_House_91856590'],meshes['SM_Kvarnholmen_House_91856614']
for zone,mm,ma in (('o8',mo,M['Roof']),('wd',mw,M['Tile'])):
 for g in Z[zone]['polygons']:
  pts=simplify([tuple(v) for v in g],.6)
  inset_roof(mm,pts,Z[zone]['height'],min(3.0 if zone=='wd' else 2.0,.45*min(math.dist(p,q) for p,q in zip(pts,pts[1:]+pts[:1]))),Z[zone]['top']-Z[zone]['height'],ma,.35)
for w in walls('o8'):
 if street53(w):
  x,y,L,a=sf_edge(w['p'],w['q']);u=U(w,-228.2,yf53(-228.2))
  # The lantern: a boarded box set back 1.6 m on the low roof, with two windows to the street.
  facade_box(mo,x,y,u,-3.0,Z['o8']['height']+.85,5.8,2.8,1.7,M['Plaster'],a)
  facade_box(mo,x,y,u,-3.0,Z['o8']['height']+1.76,6.0,3.0,.12,M['Roof'],a)
  for X0 in (-227.2,-229.46):cas53(mo,x,y,U(w,X0,yf53(X0)),Z['o8']['height']+.35,1.08,.95,a,M['WhiteFrame'],(.5,),-1.42)
for w in walls('wd'):
 if street53(w):
  x,y,L,a=sf_edge(w['p'],w['q']);sl=(Z['wd']['top']-Z['wd']['height'])/3.0
  roof_dormer(mw,x,y,U(w,-244.91,yf53(-244.91)),a,Z['wd']['height'],sl,.35,.92,.95,M['Roof'],M['Roof'],M['WhiteFrame'],False)
for cx,cy,mm,zz in ((-232.0,-156.0,mo,Z['o8']['top']),(-244.0,-155.5,mw,Z['wd']['top'])):box(mm,cx,cy,.60,.80,1.0,zz-.4,M['Tile'],0,M['Dark'])
b53_finish(mo,'91856590');b53_finish(mw,'91856614')

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
# The cameras in the model's frame: Ölandsgatan 8 in the frame spaced by the panoramas' GPS positions
# (mapped onto its OSM joints); the wooden house in the frame anchored on its own OSM corners.
_C={'A':(-234.98,6.47,2.38),'W':(-244.49,4.80,1.86)}
def _cam(n):X,D_,hh=_C[n];return X,yf53(X)+.355+D_,hh
block53_cameras=[
 sv_camera('305_Block53_Cal_Number8',*_cam('A'),152,5,90),
 sv_camera('306_Block53_Cal_Wooden',*_cam('W'),152,5,90),
 ('307_Block53_Aerial',(-237.0,-128.0,26.0),(-237.0,-160.0,4.0),28),
]
print('BLOCK53_GEOMETRY',len(block53_names))
