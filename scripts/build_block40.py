"""Pass 40: the district volume 92412846 on the south side of Södra Långgatan at the corner of Östra
Sjögatan (numbers 41-43).

A white-rendered two-storey stone house: on Södra Långgatan ten window axes of blue-grey casements
(two leaves of three panes, the top panes under a transom) set in plain reveals, a sandstone portal
with a transom light over a diamond-panelled door on three stone steps, a grey plinth, black
downpipes, iron wall anchors between the storeys and under the cornice, quoins at the street
corner; a moulded brown-grey cornice; a low black sheet-metal roof, hipped towards Östra Sjögatan,
with two white chimneys. On Östra Sjögatan four upper and three lower windows and a small white
cabinet house at the corner.

References: Google Street View April 2025 (four panoramas, three of them in one bundle adjustment),
view only. Zones: source/block40.json; see references/block40-notes.md. The street signs and the
notices in the windows are omitted.
"""
B40D=json.loads((R/'source/block40.json').read_text());Z=B40D['zones']
block40_names=[];B40={}
for old in [k for k in list(materials) if k.startswith('M_Block40_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('White','TownIvory',(.92,.91,.87),.90,0),
 ('Frame','TownPaintBrown',(.45,.57,.62),.55,0),
 ('Cornice','TownStone',(.55,.49,.42),.86,0),
 ('Sandstone','TownStone',(.58,.44,.34),.86,0),
 ('Door','TownPaintBrown',(.42,.30,.20),.60,0),
 ('Plinth','TownStone',(.52,.53,.52),.82,0),
 ('Quoin','TownStone',(.68,.63,.57),.86,0),
 ('Step','TownStone',(.62,.60,.56),.84,0),
 ('Roof','TownMetalGrey',(.12,.12,.13),.50,.30),
 ('Iron','TownMetalGrey',(.05,.05,.055),.45,.40),
 ('Dark','TownMetalGrey',(.05,.055,.06),.40,.20),
 ]:
 name='M_Block40_'+key;B40[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block40_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B40;W40=M['White']

def b40_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block40_names.append(name);return Mesh(name,category)
def b40_finish(m,osm):
 obj=s21_finish(m);obj['detail_pass']=40;obj['reference_notes']='references/block40-notes.md';obj['osm_way']=osm;return obj
def kind40(w):
 ox,oy=outward(w)
 if w['kind']!='outer':return None
 if oy>.9 and max(w['p'][1],w['q'][1])>-81.5:return 'sodra'
 if ox>.9 and min(w['p'][0],w['q'][0])>46.5:return 'ostra'
 return None
def win40(m,x,y,u,b,w,h,a):
 # Blue-grey casement in a plain reveal 0.15 m deep: two leaves, a transom at two thirds, glazing
 # bars (three panes a leaf), a thin sheet sill.
 o=.21
 facade_box(m,x,y,u,o-.04,b+h/2,w,.02,h,GLAZE,a)
 for q in (-w/2+.045,w/2-.045):facade_box(m,x,y,u+q,o,b+h/2,.09,.08,h,M['Frame'],a)
 for zz in (b+.045,b+h-.045,b+h*.70):facade_box(m,x,y,u,o,zz,w,.08,.08,M['Frame'],a)
 facade_box(m,x,y,u,o+.01,b+h/2,.08,.08,h,M['Frame'],a)
 facade_box(m,x,y,u,o+.01,b+h*.35,w,.05,.03,M['Frame'],a)
 facade_box(m,x,y,u,.38,b-.02,w+.08,.20,.03,M['Iron'],a)
def anchor40(m,x,y,u,z,a):
 # A fleur-de-lis wall anchor: a vertical bar with scrolls either side near its top.
 ma=M['Iron'];town_rod(m,lp(x,y,u,.40,z-.35,a),lp(x,y,u,.40,z+.22,a),.022,ma,6)
 for sg in (-1,1):
  town_path(m,[lp(x,y,u+sg*(.02+.10*math.sin(math.pi*t/8)),.41,z+.14-.16*t/8,a) for t in range(9)],.017,ma)
  town_path(m,[lp(x,y,u+sg*(.07+.045*math.cos(math.tau*t/10)),.41,z-.02+.045*math.sin(math.tau*t/10),a) for t in range(11)],.014,ma)
def cornice40(m,x,y,L,a,H):
 # The moulded cornice: a cavetto, a fascia, a bed moulding and the corona 0.40 m out of the wall,
 # its top at 9.12 (the plane reading 9.50 corrected for the projection); the roof's black edge above.
 C=M['Cornice']
 facade_box(m,x,y,0,.40,8.76,L,.09,.12,C,a)
 facade_box(m,x,y,0,.46,8.88,L+.04,.21,.12,C,a)
 facade_box(m,x,y,0,.54,9.00,L+.08,.37,.12,C,a)
 facade_box(m,x,y,0,.57,9.10,L+.12,.43,.06,C,a)
 facade_box(m,x,y,0,.60,9.16,L+.14,.49,.05,M['Roof'],a)
 town_rod(m,lp(x,y,-L/2,.80,9.28,a),lp(x,y,L/2,.80,9.28,a),.018,M['Iron'],6)
GB,GT=1.47,3.60;UB,UT=5.52,7.62                   # window frames' outer edges

m=b40_new('SM_Building_92412846','Kvarnholmen/Södra Långgatan south')
H40=Z['wh']['height']
for w in walls('wh'):
 k=kind40(w)
 if k is None:
  if w['kind']=='outer':plain(m,w,H40,W40,M['Frame'],W40,2,1.2)
  else:bz_wall(m,w['p'],w['q'],w['z0'],H40,[],W40)
  continue
 x,y,L,a=sf_edge(w['p'],w['q'])
 if k=='sodra':
  S=lambda X:U(w,X,-81.1)
  # Axis edges from the bundle adjustment of panoramas "40", "41" and "43" (x, west to east).
  AX=[(15.99,17.32),(18.39,19.73),(20.81,22.20),(23.91,25.30),(27.43,28.83),(29.94,31.39),(32.82,34.23),(38.56,39.98),(41.55,42.97),(44.43,45.86)]
  gw=[(S((p0+p1)/2),GB,abs(p0-p1),GT-GB,0) for p0,p1 in AX]
  uw=[(S((p0+p1)/2),UB,abs(p0-p1),UT-UB,0) for p0,p1 in AX]
  door=(S(36.42),.59,1.25,3.00,0)
  bz_wall(m,w['p'],w['q'],0,H40,gw+uw+[door],W40)
  for u,b,ww,hh,r in gw+uw:win40(m,x,y,u,b,ww,hh,a)
  # The sandstone portal: jambs with a base block, a lintel; the transom light, the diamond door.
  du,db,dw,dh,_=door
  for s in (-1,1):
   facade_box(m,x,y,du+s*(dw/2+.155),.43,(db+dh+.22)/2,.31,.15,dh+.22,M['Sandstone'],a)
   facade_box(m,x,y,du+s*(dw/2+.17),.45,db+.25,.36,.19,.50,M['Sandstone'],a)
  facade_box(m,x,y,du,.44,db+dh+.11,dw+.62,.17,.22,M['Sandstone'],a)
  facade_box(m,x,y,du,.15,db+2.25+(dh-2.25)/2,dw,.02,dh-2.25,GLAZE,a)
  for q in (-dw/6,dw/6):facade_box(m,x,y,du+q,.20,db+2.25+(dh-2.25)/2,.06,.06,dh-2.25,M['Door'],a)
  facade_box(m,x,y,du,.20,db+2.25,dw,.08,.10,M['Door'],a)
  facade_box(m,x,y,du,.18,db+1.10,dw,.06,2.20,M['Door'],a)
  # The diamond panelling: two families of diagonal battens, clipped to the leaf.
  for i in range(-4,5):
   for s in (-1,1):
    pts=[]
    for t in [k/20 for k in range(21)]:
     zz=db+1.10+s*(i*.36+(t-.5)*(dw-.1)*.9)
     if db+.08<zz<db+2.18:pts.append(lp(x,y,du-dw/2+.05+t*(dw-.1),.22,zz,a))
    if len(pts)>=2:town_path(m,[pts[0],pts[-1]],.016,M['Dark'])
  steps36(m,x,y,du,a,2.05,1.90,db,3,.95,M['Step'])
  plinth36(m,x,y,L,a,[(du-dw/2-.35,du+dw/2+.35)],.58,M['Plinth'])
  facade_box(m,x,y,0,.42,.585,L,.10,.03,M['Plinth'],a)
    # Wall anchors on every pier (the portal counts as an axis), in both rows.
  AXD=sorted(AX+[(35.46,37.36)])
  piers=[(AXD[i][1]+AXD[i+1][0])/2 for i in range(len(AXD)-1)]
  for X in piers:anchor40(m,x,y,S(X),4.55,a);anchor40(m,x,y,S(X),8.30,a)
  for X in (15.07,26.10,37.95):town_rod(m,lp(x,y,S(X),.49,.25,a),lp(x,y,S(X),.49,9.05,a),.055,M['Dark'],8)
  for zz in range(10):
   z0=.58+zz*.82
   if z0+.7>8.7:break
   ln=.95 if zz%2==0 else .60
   facade_box(m,x,y,S(47.232)+ln/2,.38,z0+.36,ln,.06,.72,M['Quoin'],a)
  cornice40(m,x,y,L,a,H40)
 else:
  S=lambda Y:U(w,47.15,Y)
  # Östra Sjögatan: four upper axes and three lower windows (from panorama "3 Östra Sjögatan",
  # registered on the corner and the joint with the brewery building; the positions are estimates).
  UP=[-84.00,-86.70,-89.37,-92.00];GF=[-86.55,-89.34,-92.23]
  uw=[(S(Y),UB,1.40,UT-UB,0) for Y in UP];gw=[(S(Y),GB,1.40,GT-GB,0) for Y in GF]
  bz_wall(m,w['p'],w['q'],0,H40,uw+gw,W40)
  for u,b,ww,hh,r in uw+gw:win40(m,x,y,u,b,ww,hh,a)
  plinth36(m,x,y,L,a,[],.58,M['Plinth'])
  for Y in (-85.35,-88.03,-90.68):anchor40(m,x,y,S(Y),4.55,a);anchor40(m,x,y,S(Y),8.30,a)
  for zz in range(10):
   z0=.58+zz*.82
   if z0+.7>8.7:break
   ln=.60 if zz%2==0 else .95
   facade_box(m,x,y,S(-81.308)-ln/2,.38,z0+.36,ln,.06,.72,M['Quoin'],a)
  cornice40(m,x,y,L,a,H40)
  # The white cabinet house at the corner, with its black pent roof and a grey door.
  cu=S(-82.75);cx,cy,_=lp(x,y,cu,.355+.50,0,a)
  box(m,cx,cy,1.05,.95,2.15,0,W40,a)
  vs=[lp(x,y,cu-.60,.30,2.30,a),lp(x,y,cu+.60,.30,2.30,a),lp(x,y,cu+.60,1.42,2.12,a),lp(x,y,cu-.60,1.42,2.12,a)]
  m.faces(vs,[(0,1,2,3)],M['Roof']);m.faces([(v[0],v[1],v[2]-.05) for v in vs],[(3,2,1,0)],M['Roof'])
  facade_box(m,x,y,cu+.20,1.34,1.0,.45,.02,1.75,M['Plinth'],a)
# The street corner: the two fronts' slabs stand 0.355 m out of their OSM lines; a corner post in
# the quoin stone fills the notch.
box(m,47.42,-81.12,.41,.41,8.70,0,M['Quoin'],0)
sl=roof34(m,'wh',M['Roof'],W40)
for cx,cy in ((30.0,-83.3),(35.4,-83.3)):box(m,cx,cy,.80,.70,2.7,10.4,W40,0,M['Dark'])
b40_finish(m,'92412846')

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
# Bundle-adjusted camera positions, shifted 0.355 m outward like the modelled walls.
block40_cameras=[
 sv_camera('235_Block40_Cal_West',14.761,-74.353+.355,2.50,152,0,75),       # its height not measured (no base in view): 2.50 assumed
 sv_camera('236_Block40_Cal_Middle',24.896,-74.479+.355,2.52,152,0,75),
 sv_camera('237_Block40_Cal_Middle_Roof',24.896,-74.479+.355,2.52,152,25,75),
 sv_camera('238_Block40_Cal_Portal',35.11,-74.795+.355,2.51,152,0,75),
 sv_camera('239_Block40_Cal_Corner',35.11,-74.795+.355,2.51,112,5,75),
 ('240_Block40_Aerial',(28.0,-55.0,34.0),(32.0,-90.0,5.0),28),
]
print('BLOCK40_GEOMETRY',len(block40_names))
