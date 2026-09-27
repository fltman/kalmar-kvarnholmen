"""Pass 72: the district volume 91926300 on the corner of Proviantgatan and Storgatan, a grey
roughcast two-storey house:
- four axes of white-framed six-pane casements in wide white surrounds on each storey;
- a broad white corner pilaster on the Storgatan corner and a white corner board at the north end;
- a grey rendered plinth with cellar vents, a plain cornice and a low hipped sheet-metal roof.
The Storgatan, yard and party walls keep a plain two-storey rhythm.

References: Google Street View April 2025 (one panorama on Proviantgatan, resected on both corners
of the front in two headings), view only. Zones: source/block72.json; see
references/block72-notes.md. The street-name plate, the lamp and the traffic sign are omitted.
"""
B72D=json.loads((R/'source/block72.json').read_text());Z=B72D['zones']
block72_names=[];B72={}
for old in [k for k in list(materials) if k.startswith('M_Block72_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Grey','TownIvory',(.70,.66,.62),.96,0),
 ('White','TownIvory',(.93,.93,.91),.84,0),
 ('WhiteFrame','TownPaintWhite',(.95,.95,.93),.55,0),
 ('Plinth','TownIvory',(.48,.48,.46),.94,0),
 ('Roof','TownMetalGrey',(.40,.40,.41),.55,.30),
 ('Dark','TownMetalGrey',(.05,.055,.06),.40,.20),
 ]:
 name='M_Block72_'+key;B72[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block72_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B72;WH=M['White'];GR=M['Grey']

def b72_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block72_names.append(name);return Mesh(name,category)
def b72_finish(m,osm):
 obj=s21_finish(m);obj['detail_pass']=72;obj['reference_notes']='references/block72-notes.md';obj['osm_way']=osm;return obj
def xe72(Y):return 176.69+(Y-.702)*(176.943-176.69)/(13.071-.702)
def cas72(m,x,y,u,b,w,h,a,o=.16):
 facade_box(m,x,y,u,o-.04,b+h/2,w,.02,h,GLAZE,a)
 for q in (-w/2+.04,w/2-.04,0):facade_box(m,x,y,u+q,o,b+h/2,.08 if q else .05,.08,h,M['WhiteFrame'],a)
 for zz in (b+.04,b+h-.04):facade_box(m,x,y,u,o,zz,w,.08,.07,M['WhiteFrame'],a)
 for zz in (b+h/3,b+2*h/3):facade_box(m,x,y,u,o+.01,zz,w,.05,.04,M['WhiteFrame'],a)

AX=[(2.9,1.13,1.20),(5.32,1.14,1.22),(8.13,1.12,1.25),(11.04,1.06,1.11)]
m=b72_new('SM_Kvarnholmen_House_91926300','Kvarnholmen/Proviantgatan')
H=Z['gr']['height']
for w in walls('gr'):
 x,y,L,a=sf_edge(w['p'],w['q']);ox,oy=outward(w)
 if w['kind']=='outer' and ox>.9:
  S=lambda Y:U(w,xe72(Y),Y)
  up=[(S(Y0),4.64,wu,1.49,0) for Y0,wu,wg in AX];gf=[(S(Y0),1.59,wg,1.52,0) for Y0,wu,wg in AX]
  cel=[(S(Y0),.18,.45,.30,0) for Y0,wu,wg in AX]
  bz_wall(m,w['p'],w['q'],0,H,up+gf+cel,GR)
  for u,b,ww,hh,r in up+gf:
   cas72(m,x,y,u,b,ww,hh,a);surround36(m,x,y,u,b,ww,hh,a,WH,.16,.39)
   facade_box(m,x,y,u,.47,b-.10,ww+.40,.14,.05,M['Dark'],a)
  for u,b,ww,hh,r in cel:
   facade_box(m,x,y,u,.44,b+hh/2,ww,.02,hh,M['Dark'],a)
   for k in range(1,5):facade_box(m,x,y,u,.46,b+k*hh/5,ww,.03,.02,M['Plinth'],a)
  facade_box(m,x,y,0,.39,.30,L,.08,.60,M['Plinth'],a)
  facade_box(m,x,y,S(1.1),.42,(.6+7.6)/2,.80,.10,7.0,WH,a);facade_box(m,x,y,S(12.97),.42,(.6+7.6)/2,.20,.08,7.0,WH,a)
  facade_box(m,x,y,0,.42,7.62,L,.10,.26,WH,a);facade_box(m,x,y,0,.54,7.86,L+.10,.34,.18,WH,a)
 else:
  if w['kind']=='outer':plain(m,w,H,GR,M['WhiteFrame'],WH,2,.9)
  else:bz_wall(m,w['p'],w['q'],w['z0'],H,[],GR)
roof34(m,'gr',M['Roof'],GR)
box(m,170.0,7.0,.55,.75,1.0,Z['gr']['top']-.5,M['Roof'],0,M['Dark'])
b72_finish(m,'91926300')

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block72_cameras=[
 sv_camera('365_Block72_Cal_South',181.36+.355,4.49,2.51,242,10,90),
 sv_camera('366_Block72_Cal_North',181.36+.355,4.49,2.51,290,10,90),
 ('367_Block72_Aerial',(192.0,7.0,24.0),(170.0,7.0,3.0),28),
]
print('BLOCK72_GEOMETRY',len(block72_names))
