"""Pass 73: the district volume 93192422 on the east side of Proviantgatan, a cream rendered
three-storey house:
- a rusticated ground floor over a grey plinth with cellar windows, and a band over it;
- seven axes of white-framed casements in white surrounds on every storey, three and three either
  side of a pilaster strip rusticated on the ground floor, with strips at both ends;
- a profiled cornice, and a dark mansard with a dormer over each axis.
The yard and party walls keep a plain rhythm.

References: Google Street View April 2025 (one panorama on Proviantgatan, resected on the joint
with the house to the north and on the south corner in two headings), view only.
Zones: source/block73.json; see references/block73-notes.md. The meter cabinet is omitted.
"""
B73D=json.loads((R/'source/block73.json').read_text());Z=B73D['zones']
block73_names=[];B73={}
for old in [k for k in list(materials) if k.startswith('M_Block73_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Cream','TownIvory',(.86,.82,.72),.92,0),
 ('Groove','TownIvory',(.70,.66,.58),.95,0),
 ('White','TownIvory',(.94,.94,.91),.84,0),
 ('WhiteFrame','TownPaintWhite',(.95,.95,.93),.55,0),
 ('Plinth','TownIvory',(.52,.53,.54),.94,0),
 ('Mansard','TownMetalGrey',(.14,.15,.17),.55,.25),
 ('Dark','TownMetalGrey',(.05,.055,.06),.40,.20),
 ]:
 name='M_Block73_'+key;B73[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block73_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B73;WH=M['White'];CR=M['Cream']

def b73_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block73_names.append(name);return Mesh(name,category)
def b73_finish(m,osm):
 obj=s21_finish(m);obj['detail_pass']=73;obj['reference_notes']='references/block73-notes.md';obj['osm_way']=osm;return obj
def xw73(Y):return 188.302+(Y-11.679)*(188.981-188.302)/(25.412-11.679)
def cas73(m,x,y,u,b,w,h,a,o=.16):
 facade_box(m,x,y,u,o-.04,b+h/2,w,.02,h,GLAZE,a)
 for q in (-w/2+.04,w/2-.04,0):facade_box(m,x,y,u+q,o,b+h/2,.08 if q else .06,.08,h,M['WhiteFrame'],a)
 for zz in (b+.04,b+h-.04,b+h*.62):facade_box(m,x,y,u,o,zz,w,.08,.06,M['WhiteFrame'],a)
 for s in (-1,1):facade_box(m,x,y,u+s*w/4,o+.01,b+h*.81,.04,.05,h*.36,M['WhiteFrame'],a)

AX=[23.72,21.7,19.96,16.42,14.78,12.9];STRIPS=[(25.15,.52),(18.1,1.15),(11.95,.52)]
ROWS=[(1.87,1.69),(5.2,1.65),(8.13,1.59)]
m=b73_new('SM_Kvarnholmen_House_93192422','Kvarnholmen/Proviantgatan')
H=Z['cr']['height']
for w in walls('cr'):
 x,y,L,a=sf_edge(w['p'],w['q']);ox,oy=outward(w)
 if w['kind']=='outer' and ox<-.9:
  S=lambda Y:U(w,xw73(Y),Y)
  wins=[(S(Y0),b,1.25,h,0) for Y0 in AX for b,h in ROWS]
  cel=[(S(Y0),.30,.95,.45,0) for Y0 in AX]
  bz_wall(m,w['p'],w['q'],0,H,wins+cel,CR)
  for u,b,ww,hh,r in wins:
   cas73(m,x,y,u,b,ww,hh,a);surround36(m,x,y,u,b,ww,hh,a,WH,.10,.39)
   facade_box(m,x,y,u,.46,b-.06,ww+.28,.16,.06,WH,a)
  for u,b,ww,hh,r in cel:
   facade_box(m,x,y,u,.44,b+hh/2,ww,.02,hh,M['Dark'],a);surround36(m,x,y,u,b,ww,hh,a,M['WhiteFrame'],.06,.44)
  # The rusticated ground floor: grooves broken round the windows.
  for k in range(1,11):
   zz=.98+k*.30;at=-L/2
   for uu,ww in sorted([(u,ww+.24) for u,b,ww,hh,r in wins if b<3 and b-.1<zz<b+hh+.1]):
    if uu-ww/2>at+.05:facade_box(m,x,y,(at+uu-ww/2)/2,.37,zz,uu-ww/2-at,.03,.025,M['Groove'],a)
    at=uu+ww/2
   if L/2>at+.05:facade_box(m,x,y,(at+L/2)/2,.37,zz,L/2-at,.03,.025,M['Groove'],a)
  for Y0,ww in STRIPS:
   facade_box(m,x,y,S(Y0),.42,(4.41+10.3)/2,ww,.10,10.3-4.41,CR,a)
   facade_box(m,x,y,S(Y0),.42,(.98+4.06)/2,ww,.10,4.06-.98,CR,a)
   for k in range(1,11):facade_box(m,x,y,S(Y0),.47,.98+k*.30,ww,.02,.025,M['Groove'],a)
  facade_box(m,x,y,0,.39,.49,L,.08,.98,M['Plinth'],a)
  facade_box(m,x,y,0,.42,4.12,L,.10,.12,WH,a);facade_box(m,x,y,0,.50,4.30,L+.04,.24,.22,CR,a)
  facade_box(m,x,y,0,.42,10.4,L,.10,.20,WH,a);facade_box(m,x,y,0,.52,10.72,L+.06,.30,.44,WH,a);facade_box(m,x,y,0,.66,11.0,L+.16,.56,.12,WH,a)
  sl=(Z['cr']['top']-H)/1.0
  for Y0 in AX:
   u=S(Y0);d=.55;zf=H+.75
   box(m,*lp(x,y,u,-d-.6,0,a)[:2],1.2,1.2,1.25,zf,M['Mansard'],a,M['Mansard'])
   facade_box(m,x,y,u,-d+.02,zf+.62,.95,.04,.85,GLAZE,a)
   for q in (-.44,.44,0):facade_box(m,x,y,u+q,-d+.06,zf+.62,.08 if q else .06,.06,.85,M['WhiteFrame'],a)
   for zz in (zf+.2,zf+1.04):facade_box(m,x,y,u,-d+.06,zz,.95,.06,.07,M['WhiteFrame'],a)
 else:
  if w['kind']=='outer':plain(m,w,H,CR,M['WhiteFrame'],WH,3,.9)
  else:bz_wall(m,w['p'],w['q'],w['z0'],H,[],CR)
roof34(m,'cr',M['Mansard'],CR)
inset_roof(m,[tuple(v) for v in Z['cr']['roof']['r1']],Z['cr']['top'],2.0,.4,M['Mansard'],0)
b73_finish(m,'93192422')

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block73_cameras=[
 sv_camera('368_Block73_Cal_Front',180.98-.355,24.44,2.50,62,10,90),
 sv_camera('369_Block73_Cal_South',180.98-.355,24.44,2.50,112,10,90),
 ('370_Block73_Aerial',(176.0,18.0,26.0),(196.0,18.0,4.0),28),
]
print('BLOCK73_GEOMETRY',len(block73_names))
