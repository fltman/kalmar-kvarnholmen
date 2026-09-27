"""Pass 47: the district volumes 92379306 and 92379253 on the north side of Ölandsgatan, opposite
pass 46:
- the cream two-storey house (92379306): a banded ground floor on a salmon plinth with five brown
  casements in plain surrounds, a band, five upper casements, the eaves and a tile roof with two
  dormers;
- the narrow white wooden house (number 13, in 92379253): vertical boarding, a white garage door, one
  upper window, a sheet roof;
- the white stone house (in 92379253): four axes of white casements in flat surrounds with aprons on
  both storeys, a band with a frieze, a grey plinth with cellar lights, the eaves and a sheet roof
  with a roof terrace railing.
The rear wing stays plain.

References: Google Street View April 2025 (two panoramas chained on shared edges and the joint with
pass 46's houses opposite), view only. Zones: source/block47.json; see references/block47-notes.md.
"""
B47D=json.loads((R/'source/block47.json').read_text());Z=B47D['zones']
block47_names=[];B47={}
for old in [k for k in list(materials) if k.startswith('M_Block47_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Cream','TownIvory',(.93,.88,.76),.88,0),
 ('Salmon','TownIvory',(.80,.62,.52),.88,0),
 ('White','TownIvory',(.95,.95,.93),.82,0),
 ('Board','TownPaintBrown',(.93,.93,.91),.70,0),
 ('Plinth','TownStone',(.60,.60,.58),.84,0),
 ('BrownFrame','TownPaintBrown',(.48,.34,.24),.55,0),
 ('WhiteFrame','TownPaintWhite',(.95,.95,.93),.55,0),
 ('Tile','TownTileRed',(.72,.40,.28),.80,0),
 ('Roof','TownMetalGrey',(.35,.36,.37),.55,.30),
 ('Iron','TownMetalGrey',(.20,.20,.21),.45,.40),
 ('Dark','TownMetalGrey',(.05,.055,.06),.40,.20),
 ]:
 name='M_Block47_'+key;B47[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block47_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B47;WH=M['White']

def b47_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block47_names.append(name);return Mesh(name,category)
def b47_finish(m,osm):
 obj=s21_finish(m);obj['detail_pass']=47;obj['reference_notes']='references/block47-notes.md';obj['osm_way']=osm;return obj
def yf47(X):return -140.385+(X+129.258)*(-140.61+140.385)/(-117.342+129.258)
def street47(w):
 ox,oy=outward(w);return w['kind']=='outer' and oy<-.9 and min(w['p'][1],w['q'][1])<-140
def cas47(m,x,y,u,b,w,h,a,frame,trans=.66,o=.18):
 facade_box(m,x,y,u,o-.04,b+h/2,w,.02,h,GLAZE,a)
 for q in (-w/2+.04,w/2-.04):facade_box(m,x,y,u+q,o,b+h/2,.08,.08,h,frame,a)
 for zz in (b+.04,b+h-.04,b+h*trans):facade_box(m,x,y,u,o,zz,w,.08,.07,frame,a)
 facade_box(m,x,y,u,o+.01,b+h/2,.07,.08,h,frame,a)
 facade_box(m,x,y,u,.40,b-.03,w+.10,.20,.04,M['Dark'],a)
def eaves47(m,x,y,L,a,H,ma,out=.42):
 facade_box(m,x,y,0,.40,H-.25,L,.10,.34,ma,a);facade_box(m,x,y,0,.36+out/2,H-.05,L+.10,out,.12,ma,a)
 town_rod(m,lp(x,y,-L/2,.36+out,H-.04,a),lp(x,y,L/2,.36+out,H-.04,a),.06,M['Iron'],8)

meshes={'SM_Kvarnholmen_House_92379306':b47_new('SM_Kvarnholmen_House_92379306','Kvarnholmen/Ölandsgatan north'),
 'SM_Kvarnholmen_House_92379253':b47_new('SM_Kvarnholmen_House_92379253','Kvarnholmen/Ölandsgatan north')}
for zone in Z:
 m=meshes[Z[zone]['mesh']];HZ=Z[zone]['height']
 wall={'cr':M['Cream'],'nw':M['Board'],'st':WH}.get(zone,WH)
 for w in walls(zone):
  x,y,L,a=sf_edge(w['p'],w['q']);S=lambda X:U(w,X,yf47(X))
  if zone=='cr' and street47(w):
   GW=[(-139.06,-137.92),(-137.0,-135.9),(-135.14,-134.07),(-133.31,-132.19),(-131.15,-130.06)]
   UW=[(-138.84,-137.67),(-136.75,-135.65),(-134.98,-133.94),(-133.2,-132.19),(-131.15,-130.13)]
   gf=[(S((a0+b0)/2),1.24,abs(b0-a0)-.20,1.65,0) for a0,b0 in GW]
   up=[(S((a0+b0)/2),4.01,abs(b0-a0)-.20,1.59,0) for a0,b0 in UW]
   bz_wall(m,w['p'],w['q'],0,HZ,gf+up,wall)
   for u,b,ww,hh,r in gf+up:surround36(m,x,y,u,b,ww,hh,a,M['Cream'],.10,.385);cas47(m,x,y,u,b,ww,hh,a,M['BrownFrame'])
   for k in range(6):
    zz=1.0+k*.40;at=-L/2
    for l_,r_ in sorted((u-ww/2-.12,u+ww/2+.12) for u,b,ww,hh,rr in gf if b-.05<zz<b+hh+.05)+[(L/2,L/2)]:
     l_=max(-L/2,min(L/2,l_))
     if l_>at+.05:facade_box(m,x,y,(at+l_)/2,.37,zz,l_-at,.03,.04,M['White'],a)
     at=max(at,r_)
   facade_box(m,x,y,0,.40,3.48,L,.10,.14,M['Cream'],a)
   facade_box(m,x,y,0,.40,.41,L,.10,.82,M['Salmon'],a)
   for X0 in (-140.5,-129.4):facade_box(m,x,y,S(X0),.40,(0.82+HZ)/2,.30,.08,HZ-.82,M['Cream'],a)
   eaves47(m,x,y,L,a,HZ,M['Cream'])
  elif zone=='nw' and street47(w):
   gar=(S(-127.98),.20,1.84,2.75,0);win=(S(-127.82),4.16,1.09,1.63,0)
   bz_wall(m,w['p'],w['q'],0,HZ,[gar,win],wall)
   boards35(m,x,y,L,a,.6,HZ-.4,[gar,win],WH)
   surround36(m,x,y,gar[0],.20,1.84,2.75,a,WH,.12,.39);facade_box(m,x,y,gar[0],.20,1.575,1.84,.06,2.75,M['Board'],a)
   for k in range(1,12):facade_box(m,x,y,gar[0],.24,.20+k*2.75/12,1.84,.02,.02,M['Dark'],a)
   surround36(m,x,y,win[0],4.16,1.09,1.63,a,WH,.12,.39);cas47(m,x,y,win[0],4.16,1.09,1.63,a,M['WhiteFrame'])
   facade_box(m,x,y,0,.40,.30,L,.08,.60,M['Plinth'],a)
   eaves47(m,x,y,L,a,HZ,WH)
  elif zone=='st' and street47(w):
   AX=[(-125.86,-124.81),(-124.37,-123.3),(-122.57,-121.52),(-120.79,-119.7)]
   gf=[(S((a0+b0)/2),1.71,abs(b0-a0)-.20,1.38,0) for a0,b0 in AX]
   up=[(S((a0+b0)/2),4.17,abs(b0-a0)-.20,1.71,0) for a0,b0 in AX]
   bz_wall(m,w['p'],w['q'],0,HZ,gf+up,wall)
   for u,b,ww,hh,r in gf+up:
    surround36(m,x,y,u,b,ww,hh,a,WH,.12,.39);cas47(m,x,y,u,b,ww,hh,a,M['WhiteFrame'],.99)
    facade_box(m,x,y,u,.40,b-.40,ww+.28,.06,.50,WH,a)
   facade_box(m,x,y,0,.42,3.75,L,.10,.12,WH,a);facade_box(m,x,y,0,.42,3.52,L,.08,.08,WH,a)
   for X0 in (-126.5,-118.2):facade_box(m,x,y,S(X0),.40,(1.0+HZ)/2,.36,.08,HZ-1.0,WH,a)
   facade_box(m,x,y,0,.39,.49,L,.08,.98,M['Plinth'],a)
   for u,b,ww,hh,r in gf:facade_box(m,x,y,u,.44,.55,.55,.04,.40,M['Dark'],a)
   eaves47(m,x,y,L,a,HZ,WH)
   town_rod(m,lp(x,y,S(-126.9),.50,.25,a),lp(x,y,S(-126.9),.50,HZ,a),.05,M['Iron'],8)
  else:
   if w['kind']=='outer':plain(m,w,HZ,wall,M['BrownFrame'] if zone=='cr' else M['WhiteFrame'],WH,2,.9)
   else:bz_wall(m,w['p'],w['q'],w['z0'],HZ,[],wall)
m06,m53=meshes['SM_Kvarnholmen_House_92379306'],meshes['SM_Kvarnholmen_House_92379253']
sl=roof34(m06,'cr',M['Tile'],M['Cream'])
roof34(m53,'st',M['Roof'],WH);roof34(m53,'nw',M['Roof'],M['Board'])
for g in Z['bk']['polygons']:
 pts=simplify([tuple(v) for v in g],.6)
 inset_roof(m53,pts,Z['bk']['height'],min(1.5,.45*min(math.dist(p,q) for p,q in zip(pts,pts[1:]+pts[:1]))),1.4,M['Roof'],.30)
for w in walls('cr'):
 if street47(w):
  x,y,L,a=sf_edge(w['p'],w['q'])
  for X in (-134.5,-131.7):roof_dormer(m06,x,y,U(w,X,yf47(X)),a,Z['cr']['height'],sl,.7,.85,.75,M['Salmon'],M['Tile'],WH,False)
for w in walls('st'):
 if street47(w):
  x,y,L,a=sf_edge(w['p'],w['q'])
  for zz in (Z['st']['height']+.45,Z['st']['height']+.8):town_rod(m53,lp(x,y,-L/2,-.3,zz,a),lp(x,y,L/2,-.3,zz,a),.02,M['Iron'],6)
for cx,cy in ((-135.5,-134.8),(-123.0,-135.0),(-120.5,-135.0)):box(m06 if cx<-129.2 else m53,cx,cy,.55,.75,1.1,(Z['cr']['top'] if cx<-129.2 else Z['st']['top'])-.4,M['Tile'],0,M['Dark'])
b47_finish(m06,'92379306');b47_finish(m53,'92379253')

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
_C={'C':(-122.22,5.79),'D':(-131.35,5.37)}
def _cam(n):X,D_=_C[n];return X,yf47(X)-.355-D_,2.10
block47_cameras=[
 sv_camera('285_Block47_Cal_Stone',*_cam('C'),332,5,90),
 sv_camera('286_Block47_Cal_Cream',*_cam('D'),332,5,90),
 ('287_Block47_Aerial',(-128.0,-170.0,28.0),(-128.0,-136.0,4.0),28),
]
print('BLOCK47_GEOMETRY',len(block47_names))
