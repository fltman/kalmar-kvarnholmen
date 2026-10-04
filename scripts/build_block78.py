"""Pass 78: the district volume 93192377 on the south side of Norra Långgatan, the cream rendered
two-storey house of 1887:
- a granite plinth, four axes of green-framed casements over sunk panels on the ground floor and the
  green carriage gate with its lattice transom at the west end;
- a band between the storeys, five upper windows, a cornice with a roof rail, and a boarded dormer
  with a pair of windows over the middle axis.

References: Google Street View April 2025 (one panorama on Norra Långgatan, resected on the house's
east corner and its joint with the pass 77 block in two headings, which agree on the window axes
within 0.2 m), view only. Zones: source/block78.json; see references/block78-notes.md. The meter
cabinet and the lamp are omitted.
"""
B78D=json.loads((R/'source/block78.json').read_text());Z=B78D['zones']
block78_names=[];B78={}
for old in [k for k in list(materials) if k.startswith('M_Block78_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Cream','TownIvory',(.90,.87,.74),.92,0),
 ('Trim','TownIvory',(.93,.91,.82),.86,0),
 ('GreenFrame','TownPaintGreen',(.24,.34,.26),.55,0),
 ('Gate','TownPaintGreen',(.26,.40,.30),.60,0),
 ('Granite','TownStone',(.62,.56,.54),.88,0),
 ('Dormer','TownPaintBrown',(.50,.28,.22),.60,0),
 ('Roof','TownMetalGrey',(.36,.33,.32),.55,.30),
 ('Iron','TownMetalGrey',(.10,.10,.10),.45,.40),
 ('Dark','TownMetalGrey',(.05,.055,.06),.40,.20),
 ]:
 name='M_Block78_'+key;B78[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block78_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B78;CR=M['Cream'];TR=M['Trim']

def b78_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block78_names.append(name);return Mesh(name,category)
def b78_finish(m,osm):
 obj=s21_finish(m);obj['detail_pass']=78;obj['reference_notes']='references/block78-notes.md';obj['osm_way']=osm;return obj
def cas78(m,x,y,u,b,w,h,a,o=.16):
 facade_box(m,x,y,u,o-.04,b+h/2,w,.02,h,GLAZE,a)
 for q in (-w/2+.04,w/2-.04,0):facade_box(m,x,y,u+q,o,b+h/2,.08 if q else .06,.08,h,M['GreenFrame'],a)
 for zz in (b+.04,b+h-.04,b+h*.72,b+h*.36):facade_box(m,x,y,u,o+(0 if zz in (b+.04,b+h-.04) else .01),zz,w,.08 if zz in (b+.04,b+h-.04) else .05,.06 if zz in (b+.04,b+h-.04) else .04,M['GreenFrame'],a)
def yn78(X):return 61.303+(X-253.658)*(61.105-61.303)/(265.665-253.658)

m=b78_new('SM_Kvarnholmen_House_93192377','Kvarnholmen/Norra Långgatan')
H=Z['cr']['height']
for w in walls('cr'):
 x,y,L,a=sf_edge(w['p'],w['q']);ox,oy=outward(w)
 if w['kind']=='outer' and oy>.9:
  S=lambda X:U(w,X,yn78(X))
  gf=[(S(X0),1.43,1.16,1.79,0) for X0 in (264.12,261.85,259.71,257.51)]
  up=[(S(X0),4.52,ww,1.78,0) for X0,ww in ((264.11,1.12),(261.87,1.10),(259.72,1.16),(257.56,1.15),(255.36,1.18))]
  gate=(S(255.42),.52,2.15,2.63,0)
  bz_wall(m,w['p'],w['q'],0,H,gf+up+[gate],CR)
  for u,b,ww,hh,r in gf+up:
   cas78(m,x,y,u,b,ww,hh,a);surround36(m,x,y,u,b,ww,hh,a,TR,.12,.40);facade_box(m,x,y,u,.47,b-.06,ww+.30,.16,.06,TR,a)
  for u,b,ww,hh,r in gf:
   facade_box(m,x,y,u,.40,.95,ww+.20,.06,.72,TR,a);facade_box(m,x,y,u,.38,.95,ww,.06,.56,CR,a)
  u,b,ww,hh,r=gate
  for s in (-1,1):
   facade_box(m,x,y,u+s*ww/4,.10,b+(hh-.55)/2,ww/2-.02,.06,hh-.55,M['Gate'],a)
   for zz in (b+.5,b+1.3):facade_box(m,x,y,u+s*ww/4,.14,zz,ww/2-.25,.03,.6,M['Gate'],a)
  facade_box(m,x,y,u,.12,b+hh-.27,ww,.02,.46,GLAZE,a)
  for k in range(1,7):town_rod(m,lp(x,y,u-ww/2+(k-.5)*ww/6-.18,.14,b+hh-.5,a),lp(x,y,u-ww/2+(k-.5)*ww/6+.18,.14,b+hh-.04,a),.02,M['Gate'],4)
  facade_box(m,x,y,u,.16,b+hh-.55,ww,.06,.06,M['Gate'],a);surround36(m,x,y,u,b,ww,hh,a,TR,.14,.40)
  at=-L/2
  for lo,hi in ((gate[0]-gate[2]/2-.15,gate[0]+gate[2]/2+.15),(L/2+1,L/2+1)):
   if lo>at+.03:facade_box(m,x,y,(at+lo)/2,.39,.26,lo-at,.08,.52,M['Granite'],a)
   at=max(at,hi)
  for uu in (-L/2+.2,L/2-.2):facade_box(m,x,y,uu,.42,(.52+H)/2,.40,.10,H-.52,TR,a)
  facade_box(m,x,y,0,.42,3.85,L,.10,.14,TR,a);facade_box(m,x,y,0,.50,4.08,L+.04,.24,.30,TR,a)
  facade_box(m,x,y,0,.42,7.35,L,.10,.24,TR,a);facade_box(m,x,y,0,.54,7.64,L+.06,.34,.34,TR,a);facade_box(m,x,y,0,.68,7.86,L+.16,.60,.10,TR,a)
  for zr in (8.25,8.55):town_rod(m,lp(x,y,-L/2+.3,.10,zr,a),lp(x,y,L/2-.3,.10,zr,a),.02,M['Iron'],6)
  for k in range(int(L/1.5)+1):facade_box(m,x,y,-L/2+.3+k*(L-.6)/int(L/1.5),.10,8.25,.04,.04,.6,M['Iron'],a)
  # The dormer over the middle axis: a boarded front with two windows under a gable.
  u=S(259.7);d=.35;zf=H+.45
  box(m,*lp(x,y,u,-d-1.0,0,a)[:2],1.9,2.0,1.45,zf,M['Dormer'],a)
  for s in (-1,1):
   q=[lp(x,y,u+s*1.07,-d+.1,zf+1.45,a),lp(x,y,u+s*1.07,-d-2.0,zf+1.45,a),lp(x,y,u,-d-2.0,zf+2.1,a),lp(x,y,u,-d+.1,zf+2.1,a)]
   m.faces(q,[(0,1,2,3),(3,2,1,0)],M['Roof'])
  m.faces([lp(x,y,u-.95,-d,zf+1.45,a),lp(x,y,u+.95,-d,zf+1.45,a),lp(x,y,u,-d,zf+2.05,a)],[(0,1,2),(2,1,0)],M['Dormer'])
  for s in (-1,1):
   facade_box(m,x,y,u+s*.42,-d+.03,zf+.72,.7,.02,1.0,GLAZE,a)
   for q in (-.31,.31,0):facade_box(m,x,y,u+s*.42+q,-d+.07,zf+.72,.06,.05,1.0,M['GreenFrame'],a)
   for zz in (zf+.24,zf+1.2,zf+.8):facade_box(m,x,y,u+s*.42,-d+.07,zz,.68,.05,.05,M['GreenFrame'],a)
 else:
  if w['kind']=='outer':plain(m,w,H,CR,M['GreenFrame'],TR,2,.9)
  else:bz_wall(m,w['p'],w['q'],w['z0'],H,[],CR)
roof34(m,'cr',M['Roof'],CR)
box(m,257.0,57.0,.55,.7,1.1,Z['cr']['top']-.6,M['Roof'],0,M['Dark'])
b78_finish(m,'93192377')

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block78_cameras=[
 sv_camera('387_Block78_Cal_Front',262.47,68.75+.355,2.30,152,10,90),
 sv_camera('388_Block78_Cal_West',262.47,68.75+.355,2.30,202,10,90),
 ('389_Block78_Aerial',(260.0,75.0,24.0),(259.0,55.0,2.0),28),
]
print('BLOCK78_GEOMETRY',len(block78_names))
