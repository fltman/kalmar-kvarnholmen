"""Pass 61: the district volume 91885539 on the corner of Norra Långgatan and Östra Sjögatan, the pale
yellow two-storey house (Norra Långgatan 41):
- to Norra Långgatan seven axes of red-brown casements in white surrounds (the ground windows over
  roughcast panels), white pilasters at the corners and flanking the middle axis, the carved double
  door (41) with its glazed transom up a step, a sill band between the storeys, a grey plinth, a
  cornice, and a red sheet-metal gambrel roof with an ornate dormer;
- to Östra Sjögatan the gambrel gable: four ground windows, two pairs of windows upstairs and three
  small windows in the gable.

References: Google Street View April 2025 (a close panorama facing the door and an overview from the
Östra Sjögatan crossing, resected on three corners), view only. Zones: source/block61.json; see
references/block61-notes.md. The traffic signs and the street-name plates are omitted.
"""
B61D=json.loads((R/'source/block61.json').read_text());Z=B61D['zones']
block61_names=[];B61={}
for old in [k for k in list(materials) if k.startswith('M_Block61_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Yellow','TownIvory',(.94,.88,.66),.88,0),
 ('White','TownIvory',(.96,.96,.94),.82,0),
 ('Panel','TownIvory',(.88,.82,.62),.95,0),
 ('Plinth','TownStone',(.62,.62,.60),.88,0),
 ('RedFrame','TownPaintBrown',(.50,.17,.12),.55,0),
 ('Door','TownPaintBrown',(.42,.16,.10),.55,0),
 ('RoofRed','TownMetalGrey',(.55,.16,.12),.45,.40),
 ('Dark','TownMetalGrey',(.05,.055,.06),.40,.20),
 ]:
 name='M_Block61_'+key;B61[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block61_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B61;WH=M['White'];YL=M['Yellow']

def b61_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block61_names.append(name);return Mesh(name,category)
def b61_finish(m,osm):
 obj=s21_finish(m);obj['detail_pass']=61;obj['reference_notes']='references/block61-notes.md';obj['osm_way']=osm;return obj
def ys61(X):return 72.805+(X-58.897)*(72.283-72.805)/(81.99-58.897)
def xw61(Y):return 58.897+(Y-72.805)*(59.2-58.897)/(84.011-72.805)
def cas61(m,x,y,u,b,w,h,a,o=.18):
 facade_box(m,x,y,u,o-.04,b+h/2,w,.02,h,GLAZE,a)
 for q in (-w/2+.04,w/2-.04,0):facade_box(m,x,y,u+q,o,b+h/2,.08 if q else .07,.08,h,M['RedFrame'],a)
 for zz in (b+.04,b+h-.04,b+h*.66):facade_box(m,x,y,u,o,zz,w,.08,.06,M['RedFrame'],a)
 facade_box(m,x,y,u,.44,b-.05,w+.18,.18,.06,WH,a)

SAX=[60.5,63.9,67.0,70.5,76.4,80.5];DOOR=73.2
m=b61_new('SM_Kvarnholmen_House_91885539','Kvarnholmen/Norra Långgatan')
H=Z['ny']['height']
for w in walls('ny'):
 x,y,L,a=sf_edge(w['p'],w['q']);ox,oy=outward(w)
 if w['kind']=='outer' and oy<-.9:
  S=lambda X:U(w,X,ys61(X))
  gf=[(S(X0),1.35,1.24,1.50,0) for X0 in SAX];up=[(S(X0),4.20,1.30,1.70,0) for X0 in SAX+[DOOR]]
  door=(S(DOOR),.60,1.64,2.62,0)
  bz_wall(m,w['p'],w['q'],0,H,gf+up+[door],YL)
  for u,b,ww,hh,r in gf:
   surround36(m,x,y,u,.62,ww,hh+b-.62,a,WH,.14,.39);cas61(m,x,y,u,b,ww,hh,a)
   facade_box(m,x,y,u,.36,(.62+b)/2,ww,.06,b-.62,M['Panel'],a)
  for u,b,ww,hh,r in up:surround36(m,x,y,u,b,ww,hh,a,WH,.14,.39);cas61(m,x,y,u,b,ww,hh,a)
  u,b,ww,hh,r=door
  for s in (-1,1):
   facade_box(m,x,y,u+s*ww/4,.10,b+(hh-.55)/2,ww/2-.02,.06,hh-.55,M['Door'],a)
   for zz in (b+.45,b+1.35):facade_box(m,x,y,u+s*ww/4,.14,zz,ww/2-.25,.03,.7,M['Door'],a)
  facade_box(m,x,y,u,.12,b+hh-.27,ww,.02,.5,GLAZE,a);facade_box(m,x,y,u,.16,b+hh-.56,ww,.06,.06,M['Door'],a)
  surround36(m,x,y,u,b,ww,hh,a,WH,.16,.39);steps36(m,x,y,u,a,2.0,1.8,b,2,.30,M['Plinth'])
  for X0,ww in ((59.25,.62),(69.3,.55),(71.6,.50),(81.7,.56)):
   facade_box(m,x,y,S(X0),.44,(.6+6.2)/2,ww,.12,5.6,WH,a);facade_box(m,x,y,S(X0),.50,6.28,ww+.2,.22,.18,WH,a)
  at=-L/2
  for uu,w2 in ((door[0],door[2]+.3),(L/2+2,0)):
   lo=max(-L/2,min(L/2,uu-w2/2))
   if lo>at+.03:facade_box(m,x,y,(at+lo)/2,.39,.30,lo-at,.08,.60,M['Plinth'],a)
   at=max(at,min(L/2,uu+w2/2))
  facade_box(m,x,y,0,.42,3.88,L,.10,.24,WH,a)
  facade_box(m,x,y,0,.42,6.35,L,.10,.30,WH,a);facade_box(m,x,y,0,.52,6.72,L+.10,.30,.44,WH,a);facade_box(m,x,y,0,.64,7.02,L+.20,.52,.16,WH,a)
  sl=(Z['ny']['top']-H)/1.3
  roof_dormer(m,x,y,S(69.0),a,H+.4*sl,sl,.35,1.0,1.1,M['RoofRed'],M['RoofRed'],M['RedFrame'],True)
 elif w['kind']=='outer' and ox<-.9:
  S=lambda Y:U(w,xw61(Y),Y)
  gf=[(S(Y0),1.35,1.10,1.60,0) for Y0 in (82.4,80.4,77.3,75.1)]
  up=[(S(Y0),4.30,.95,2.40,0) for Y0 in (82.0,80.8,76.9,75.5)]
  at=[(S(Y0),7.70,ww,1.30,0) for Y0,ww in ((81.45,.62),(78.9,1.05),(76.2,.62))]
  bz_wall(m,w['p'],w['q'],0,H,gf+up,YL)
  for u,b,ww,hh,r in gf+up:surround36(m,x,y,u,b,ww,hh,a,WH,.13,.39);cas61(m,x,y,u,b,ww,hh,a)
  for u,b,ww,hh,r in gf:facade_box(m,x,y,u,.36,(.62+b)/2,ww,.06,b-.62,M['Panel'],a)
  facade_box(m,x,y,0,.39,.30,L,.08,.60,M['Plinth'],a);facade_box(m,x,y,0,.42,3.88,L,.10,.24,WH,a)
  for Y0 in (72.95,83.85):facade_box(m,x,y,S(Y0),.44,(.6+7.0)/2,.56,.12,6.4,WH,a)
  facade_box(m,x,y,0,.42,6.9,L,.10,.26,WH,a)
  # The upper part of the gambrel gable (break 9.6, apex 10.8) in the wall plane, with its windows.
  top=Z['ny']['top'];ua=S(78.4);ub1,ub2=S(74.1),S(82.7)
  prof=[(S(72.805),H),(S(84.011),H),(ub2,top),(ua,10.8),(ub1,top)]
  vs=[lp(x,y,uu,o,zz,a) for o in (.005,.355) for uu,zz in prof];nn=len(prof)
  m.faces(vs,[tuple(range(nn-1,-1,-1)),tuple(range(nn,2*nn))]+[(i,(i+1)%nn,(i+1)%nn+nn,i+nn) for i in range(nn)],YL)
  town_path(m,[lp(x,y,uu,.42,zz+.06,a) for uu,zz in [(S(72.7),H-.1),(ub1,top),(ua,10.8),(ub2,top),(S(84.1),H-.1)]],.10,WH)
  for u,b,ww,hh,r in at:
   facade_box(m,x,y,u,.30,b+hh/2,ww,.30,hh,M['Dark'],a);surround36(m,x,y,u,b,ww,hh,a,WH,.12,.44);cas61(m,x,y,u,b,ww,hh,a,.40)
 else:
  if w['kind']=='outer':plain(m,w,H,YL,M['RedFrame'],WH,2,.9)
  else:bz_wall(m,w['p'],w['q'],w['z0'],H,[],YL)
roof34(m,'ny',M['RoofRed'],YL)
inset_roof(m,[tuple(v) for v in Z['ny']['roof']['r1']],Z['ny']['top'],2.4,1.2,M['RoofRed'],0)
for cx,cy in ((64.0,78.0),(72.5,79.0),(77.0,78.0)):box(m,cx,cy,.55,.75,1.0,10.4,M['RoofRed'],0,M['Dark'])
b61_finish(m,'91885539')

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block61_cameras=[
 sv_camera('333_Block61_Cal_Door',70.41,ys61(70.41)-.355-4.13,2.13,332,15,90),
 sv_camera('334_Block61_Cal_Corner',48.03,64.17,2.13,24.34,15,90),
 ('335_Block61_Aerial',(70.0,55.0,26.0),(70.0,80.0,4.0),28),
]
print('BLOCK61_GEOMETRY',len(block61_names))
