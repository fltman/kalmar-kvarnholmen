"""Pass 60: the Fiskaregatan range of the district volume 91856608, from the passage by pass 59 to
the Västra Sjögatan corner:
- the grey roughcast house (number 36) with its gambrel gable to the street: the arched door in a
  sandstone surround, two windows beside it, a band, four windows upstairs and four in the gable,
  white edge boards along the gable, a granite plinth;
- the beige two-storey house: six axes of white casements in flat surrounds on both storeys, a
  band, a granite plinth, a tile roof with three dark-red dormers and a snow rail, and at the
  Västra Sjögatan corner the apothecary's bay with an arched portal in a stone surround.
The Västra Sjögatan and Norra Långgatan ranges keep the district height.

References: Google Street View April 2025 (three panoramas on Fiskaregatan chained on shared window
edges, spaced as their GPS positions and anchored on the Västra Sjögatan corner), view only. Zones:
source/block60.json; see references/block60-notes.md. The apothecary's sign and posters are omitted.
"""
B60D=json.loads((R/'source/block60.json').read_text());Z=B60D['zones']
block60_names=[];B60={}
for old in [k for k in list(materials) if k.startswith('M_Block60_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Grey','TownIvory',(.64,.64,.62),.92,0),
 ('Beige','TownIvory',(.78,.74,.64),.92,0),
 ('White','TownIvory',(.95,.95,.93),.82,0),
 ('Granite','TownStone',(.55,.40,.34),.86,0),
 ('Sandstone','TownStone',(.62,.44,.36),.86,0),
 ('WhiteFrame','TownPaintWhite',(.94,.94,.92),.55,0),
 ('DoorOlive','TownPaintBrown',(.76,.72,.52),.60,0),
 ('DormerRed','TownPaintBrown',(.45,.14,.12),.60,0),
 ('Tile','TownTileRed',(.55,.30,.23),.80,0),
 ('Roof','TownMetalGrey',(.26,.27,.28),.55,.30),
 ('Iron','TownMetalGrey',(.08,.08,.085),.45,.40),
 ('Dark','TownMetalGrey',(.05,.055,.06),.40,.20),
 ]:
 name='M_Block60_'+key;B60[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block60_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B60;WH=M['White']

def b60_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block60_names.append(name);return Mesh(name,category)
def b60_finish(m,osm):
 obj=s21_finish(m);obj['detail_pass']=60;obj['reference_notes']='references/block60-notes.md';obj['osm_way']=osm;return obj
def yf60(X):return 134.573+(X+26.148)*(134.566-134.573)/(0.768+26.148)
def street60(w):ox,oy=outward(w);return w['kind']=='outer' and oy>.9 and max(w['p'][1],w['q'][1])>134.4
def cas60(m,x,y,u,b,w,h,a,o=.18,t=.62):
 facade_box(m,x,y,u,o-.04,b+h/2,w,.02,h,GLAZE,a)
 for q in (-w/2+.04,w/2-.04,0):facade_box(m,x,y,u+q,o,b+h/2,.08 if q else .07,.08,h,M['WhiteFrame'],a)
 for zz in (b+.04,b+h-.04,b+h*t):facade_box(m,x,y,u,o,zz,w,.08,.06,M['WhiteFrame'],a)
 facade_box(m,x,y,u,.44,b-.05,w+.20,.18,.06,WH,a)
def gmap(X):
 # The grey house measures 0.60 to -8.0 m; its OSM front runs 0.77 to -8.0: a 2 % stretch.
 return -8.0+(X+8.0)*(0.77+8.0)/(0.60+8.0)

AXB=[-9.70,-11.74,-14.06,-16.18,-18.52,-20.64]
m=b60_new('SM_Building_91856608','Kvarnholmen/Fiskaregatan')
for zone in Z:
 HZ=Z[zone]['height'];wall={'gr':M['Grey'],'bg':M['Beige']}.get(zone,M['Beige'])
 for w in walls(zone):
  x,y,L,a=sf_edge(w['p'],w['q']);S=lambda X:U(w,X,yf60(X))
  if zone=='gr' and street60(w):
   door=(S(gmap(-0.67)),.20,1.35,2.50,.30)
   gf=[(S(gmap(X0)),1.20,1.10,1.52,0) for X0 in (-3.44,-5.94)]
   up=[(S(gmap(X0)),5.00,1.12,1.50,0) for X0 in (0.0,-2.38,-4.39,-6.74)]
   gb=[(S(gmap(X0)),7.95,1.02,1.28,0) for X0 in (-0.20,-2.40,-4.40,-6.50)]
   bz_wall(m,w['p'],w['q'],0,HZ,[door]+gf+up,wall)
   for u,b,ww,hh,r in gf+up:surround36(m,x,y,u,b,ww,hh,a,WH,.14,.39);cas60(m,x,y,u,b,ww,hh,a)
   u,b,ww,hh,r=door
   for s in (-1,1):facade_box(m,x,y,u+s*ww/4,.10,b+hh/2,ww/2-.02,.06,hh,M['DoorOlive'],a)
   facade_box(m,x,y,u,.12,b+hh+r*.5,ww,.02,r,GLAZE,a)
   for s in (-1,1):facade_box(m,x,y,u+s*(ww/2+.13),.44,(b+hh+r)/2,.26,.12,b+hh+r,M['Sandstone'],a)
   arc=[(u-ww/2-.13,b+hh)]+[(u-(ww/2+.13)*math.cos(math.pi*k/14),b+hh+(r+.13)*math.sin(math.pi*k/14)) for k in range(1,14)]+[(u+ww/2+.13,b+hh)]
   town_path(m,[lp(x,y,uu,.45,zz,a) for uu,zz in arc],.12,M['Sandstone'],)
   facade_box(m,x,y,0,.39,.29,L,.08,.58,M['Granite'],a)
   facade_box(m,x,y,0,.42,3.80,L,.10,.28,WH,a)
   for X0 in (0.62,-7.85):facade_box(m,x,y,S(X0),.42,(.58+8.15)/2,.30,.10,7.57,WH,a)
   # The gambrel gable in the wall plane: side eaves 8.15, the break 10.75, the apex 12.4.
   ue,uw=S(0.768),S(-8.0);ube,ubw=S(gmap(-0.20)),S(gmap(-6.90));ua=S(gmap(-3.64))
   prof=[(ue,HZ),(uw,HZ),(ubw,Z['gr']['top']),(ua,12.40),(ube,Z['gr']['top'])]
   pr=sorted(prof[:2],key=lambda p:p[0])
   vs=[lp(x,y,uu,o,zz,a) for o in (.005,.355) for uu,zz in prof];nn=len(prof)
   m.faces(vs,[tuple(range(nn-1,-1,-1)),tuple(range(nn,2*nn))]+[(i,(i+1)%nn,(i+1)%nn+nn,i+nn) for i in range(nn)],wall)
   town_path(m,[lp(x,y,uu,.42,zz+.06,a) for uu,zz in [(ue+(.25 if ue<uw else -.25),HZ-.2),(ube,Z['gr']['top']),(ua,12.40),(ubw,Z['gr']['top']),(uw+(-.25 if ue<uw else .25),HZ-.2)]],.10,WH)
   for u,b,ww,hh,r in gb:
    facade_box(m,x,y,u,.30,b+hh/2,ww,.30,hh,M['Dark'],a);surround36(m,x,y,u,b,ww,hh,a,WH,.14,.44);cas60(m,x,y,u,b,ww,hh,a,.40)
  elif zone=='bg' and street60(w):
   up=[(S(X0),5.05,1.20,1.55,0) for X0 in AXB];gf=[(S(X0),1.08,1.22,1.74,0) for X0 in AXB]
   cup=(S(-23.74),5.05,1.10,1.55,0);portal=(S(-23.84),.44,1.60,2.20,.60)
   bz_wall(m,w['p'],w['q'],0,HZ,up+gf+[cup,portal],wall)
   for u,b,ww,hh,r in up+gf+[cup]:surround36(m,x,y,u,b,ww,hh,a,WH,.15,.39);cas60(m,x,y,u,b,ww,hh,a)
   u,b,ww,hh,r=portal
   facade_box(m,x,y,u,.10,b+(hh+r)/2,ww,.04,hh+r,GLAZE,a)
   for s in (-1,1):facade_box(m,x,y,u+s*(ww/2+.15),.44,(b+hh+r)/2,.30,.12,b+hh+r,M['Granite'],a)
   arc=[(u-ww/2-.15,b+hh)]+[(u-(ww/2+.15)*math.cos(math.pi*k/14),b+hh+(r+.15)*math.sin(math.pi*k/14)) for k in range(1,14)]+[(u+ww/2+.15,b+hh)]
   town_path(m,[lp(x,y,uu,.45,zz,a) for uu,zz in arc],.13,M['Granite'])
   # The corner bay: granite pilasters and a lintel band over the portal.
   for X0 in (-22.33,-25.98):facade_box(m,x,y,S(X0),.46,(.48+3.9)/2,.36,.14,3.42,M['Granite'],a)
   facade_box(m,x,y,(S(-22.15)+S(-26.15))/2,.46,3.75,abs(S(-22.15)-S(-26.15)),.14,.30,M['Granite'],a)
   for X0 in (-8.2,-22.1,-26.0):facade_box(m,x,y,S(X0),.42,(3.9+7.3)/2,.34,.10,3.4,WH,a)
   facade_box(m,x,y,0,.39,.24,L,.08,.48,M['Granite'],a)
   facade_box(m,x,y,0,.42,3.87,L,.10,.28,WH,a)
   facade_box(m,x,y,0,.42,7.25,L,.10,.22,WH,a);facade_box(m,x,y,0,.54,7.44,L+.10,.34,.16,WH,a)
   town_rod(m,lp(x,y,-L/2,.72,7.5,a),lp(x,y,L/2,.72,7.5,a),.07,WH,8)
   sl=(Z['bg']['top']-HZ)/3.0
   for X0 in (-10.84,-15.0,-19.46):roof_dormer(m,x,y,S(X0),a,HZ+.4*sl,sl,.30,.95,.90,M['DormerRed'],M['DormerRed'],M['WhiteFrame'],False)
   for zz in (8.1,8.35):town_rod(m,lp(x,y,-L/2+.2,-.6,zz,a),lp(x,y,L/2-.2,-.6,zz,a),.02,M['Iron'],6)
  else:
   if w['kind']=='outer':plain(m,w,HZ,wall,M['WhiteFrame'],WH,2,.9)
   else:bz_wall(m,w['p'],w['q'],w['z0'],HZ,[],wall)
roof34(m,'gr',M['Roof'],M['Grey'])
r1=[tuple(v) for v in Z['gr']['roof']['r1']]
inset_roof(m,r1,Z['gr']['top'],2.9,1.65,M['Roof'],0)
for zone,rise,ins in (('bg',2.35,3.0),('rs',1.9,2.5)):
 for g in Z[zone]['polygons']:
  pts=simplify([tuple(v) for v in g],.8)
  inset_roof(m,pts,Z[zone]['height'],min(ins,.45*min(math.dist(p,q) for p,q in zip(pts,pts[1:]+pts[:1]))),rise,M['Tile'],.40)
for cx,cy,zz in ((-3.6,129.5,12.4),(-13.0,130.5,Z['bg']['top']),(-20.0,130.5,Z['bg']['top'])):box(m,cx,cy,.60,.80,1.0,zz-.6,M['Tile'],0,M['Dark'])
b60_finish(m,'91856608')

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block60_cameras=[
 sv_camera('329_Block60_Cal_Grey',-5.00,141.94+.355,2.57,152,20,90),
 sv_camera('330_Block60_Cal_Beige',-15.14,141.93+.355,2.57,152,20,90),
 sv_camera('331_Block60_Cal_Corner',-25.31,141.58+.355,2.57,152,20,90),
 ('332_Block60_Aerial',(-12.0,160.0,28.0),(-12.0,128.0,4.0),28),
]
print('BLOCK60_GEOMETRY',len(block60_names))
