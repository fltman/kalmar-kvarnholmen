"""Pass 70: the district volume 93238145 on the west side of Proviantgatan, a pale rendered
two-storey infill house:
- dark-framed two-light windows on both storeys, a smooth plinth under a grey drip line and a
  profiled cornice;
- the gateway at the north end with its boarded wooden gates;
- the glass stair tower with its glazed door, rising past the eaves;
- a red tile roof with white box dormers over the window axes.

References: Google Street View April 2025 (two panoramas on Proviantgatan: the north one resected on
the joint with the pass 69 corner house and its base row, the south one on the glass tower and its
base row, which puts the south end within 0.12 m of the district outline), view only.
Zones: source/block70.json; see references/block70-notes.md. The lamps and the sign are omitted.
"""
B70D=json.loads((R/'source/block70.json').read_text());Z=B70D['zones']
block70_names=[];B70={}
for old in [k for k in list(materials) if k.startswith('M_Block70_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Render','TownIvory',(.90,.87,.84),.92,0),
 ('Plinth','TownIvory',(.86,.81,.76),.94,0),
 ('White','TownIvory',(.94,.94,.92),.84,0),
 ('Frame','TownPaintBrown',(.28,.21,.18),.55,0),
 ('Gate','TownPaintBrown',(.74,.56,.30),.70,0),
 ('Tile','TownTileRed',(.60,.32,.25),.80,0),
 ('Metal','TownMetalGrey',(.55,.56,.58),.45,.40),
 ('Dark','TownMetalGrey',(.05,.055,.06),.40,.20),
 ]:
 name='M_Block70_'+key;B70[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block70_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B70;RE=M['Render'];WH=M['White']

def b70_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block70_names.append(name);return Mesh(name,category)
def b70_finish(m,osm):
 obj=s21_finish(m);obj['detail_pass']=70;obj['reference_notes']='references/block70-notes.md';obj['osm_way']=osm;return obj
def xe70(Y):return 177.066+(Y-25.043)*(177.356-177.066)/(49.481-25.043)
def cas70(m,x,y,u,b,w,h,a,o=.20):
 facade_box(m,x,y,u,o-.04,b+h/2,w,.02,h,GLAZE,a)
 for q in (-w/2+.04,w/2-.04,0):facade_box(m,x,y,u+q,o,b+h/2,.08 if q else .07,.08,h,M['Frame'],a)
 for zz in (b+.04,b+h-.04):facade_box(m,x,y,u,o,zz,w,.08,.07,M['Frame'],a)
 facade_box(m,x,y,u,.42,b-.03,w+.08,.14,.04,M['Metal'],a)

AX=[26.72,29.44,32.1,39.1,41.5,44.0];GATE=(47.45,3.45);TOWER=(34.23,37.32)
m=b70_new('SM_Kvarnholmen_House_93238145','Kvarnholmen/Proviantgatan')
H=Z['wi']['height']
for w in walls('wi'):
 x,y,L,a=sf_edge(w['p'],w['q']);ox,oy=outward(w)
 if w['kind']=='outer' and ox>.9:
  S=lambda Y:U(w,xe70(Y),Y)
  gf=[(S(Y0),1.70,1.20,1.51,0) for Y0 in AX];up=[(S(Y0),4.45,1.20,1.55,0) for Y0 in AX+[47.27]]
  gate=(S(GATE[0]),0,GATE[1],3.13,0)
  t0,t1=S(TOWER[0]),S(TOWER[1]);tl,th=min(t0,t1),max(t0,t1)
  tower=((tl+th)/2,.02,th-tl,H-.1,0)
  bz_wall(m,w['p'],w['q'],0,H,gf+up+[gate,tower],RE)
  for u,b,ww,hh,r in gf+up:cas70(m,x,y,u,b,ww,hh,a)
  u,b,ww,hh,r=gate
  facade_box(m,x,y,u,-1.2,hh/2,ww,.06,hh,M['Dark'],a)
  for s in (-1,1):
   facade_box(m,x,y,u+s*ww/4,-.60,(hh-.25)/2+.05,ww/2-.04,.05,hh-.25,M['Gate'],a)
   for k in range(1,16):facade_box(m,x,y,u+s*ww/4,-.57,.05+k*(hh-.25)/16,ww/2-.06,.02,.02,M['Frame'],a)
  # The glass stair tower: mullions and transoms over the glazing, the glazed door at its foot,
  # rising past the eaves under a flat metal roof.
  tw=th-tl;tc=(tl+th)/2
  facade_box(m,x,y,tc,.30,(H+2.6)/2,tw,.05,H+2.6,GLAZE,a)
  for k in range(4):facade_box(m,x,y,tl+k*tw/3,.34,(H+2.6)/2,.08,.08,H+2.6,M['Dark'],a)
  for zz in [.02+k*1.18 for k in range(9)]:facade_box(m,x,y,tc,.34,zz,tw,.08,.06,M['Dark'],a)
  facade_box(m,x,y,tc+tw/4,.36,1.12,.95,.10,2.2,M['Gate'],a);facade_box(m,x,y,tc+tw/4,.40,1.12,.75,.04,2.0,GLAZE,a)
  box(m,*lp(x,y,tc,-1.2,0,a)[:2],tw+.2,3.2,.25,H+2.6,M['Metal'],a)
  for uu in (tl,th):facade_box(m,x,y,uu,-1.25,H+1.3,.06,3.1,2.6,GLAZE,a)
  # The plinth under its drip line, stopped at the gateway and the tower.
  at=-L/2
  for lo,hi in sorted([(gate[0]-gate[2]/2,gate[0]+gate[2]/2),(tl,th)])+[(L/2+1,L/2+1)]:
   if lo>at+.03:facade_box(m,x,y,(at+lo)/2,.39,.41,lo-at,.08,.82,M['Plinth'],a);facade_box(m,x,y,(at+lo)/2,.45,.84,lo-at,.10,.04,M['Metal'],a)
   at=max(at,hi)
  facade_box(m,x,y,0,.42,6.92,L,.10,.16,WH,a);facade_box(m,x,y,0,.54,7.10,L+.06,.30,.22,WH,a)
  sl=(Z['wi']['top']-H)/3.4
  for Y0 in (26.72,29.44,32.1,39.1,41.5,44.0,47.27):
   u=S(Y0);d=.6;zf=H+d*sl
   box(m,*lp(x,y,u,-d-1.3,0,a)[:2],1.45,2.6,2.3,zf-.5,WH,a,M['Metal'])
   facade_box(m,x,y,u,-d+.02,zf+.95,1.05,.04,1.45,GLAZE,a);facade_box(m,x,y,u,-d+.06,zf+.95,.06,.06,1.45,M['Frame'],a)
   for s2 in (-1,1):facade_box(m,x,y,u+s2*.54,-d+.06,zf+.95,.06,.06,1.45,M['Frame'],a)
 else:
  if w['kind']=='outer':plain(m,w,H,RE,M['Frame'],WH,2,.9)
  else:bz_wall(m,w['p'],w['q'],w['z0'],H,[],RE)
roof34(m,'wi',M['Tile'],RE)
b70_finish(m,'93238145')

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block70_cameras=[
 sv_camera('360_Block70_Cal_North',181.51+.355,44.84,2.30,242,10,90),
 sv_camera('361_Block70_Cal_South',181.79+.355,23.79,2.30,272,10,90),
 ('362_Block70_Aerial',(196.0,37.0,26.0),(170.0,37.0,3.0),28),
]
print('BLOCK70_GEOMETRY',len(block70_names))
