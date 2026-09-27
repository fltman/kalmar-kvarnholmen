"""Pass 69: the district volume 91926315 on the corner of Norra Långgatan and Proviantgatan, a pale
yellow rendered two-storey corner house with a canted corner:
- a rusticated ground floor over a granite plinth with cellar windows, brown-framed casements over
  sunk panels, and the brown double door (23) up three stone steps on Proviantgatan;
- a white band between the storeys, upper windows in white surrounds that run down to the band
  over sunk panels, and a white cornice;
- a hipped sheet-metal roof with a chimney.

References: Google Street View April 2025 (a panorama at the crossing resected on the ends of the
Norra Långgatan front, and one on Proviantgatan resected on the ends of that front), view only.
Zones: source/block69.json; see references/block69-notes.md. The street-name plates, the traffic
sign, the letterbox and the street lamp are omitted.
"""
B69D=json.loads((R/'source/block69.json').read_text());Z=B69D['zones']
block69_names=[];B69={}
for old in [k for k in list(materials) if k.startswith('M_Block69_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Yellow','TownIvory',(.93,.86,.66),.92,0),
 ('Groove','TownIvory',(.78,.70,.52),.95,0),
 ('White','TownIvory',(.95,.95,.92),.84,0),
 ('Plinth','TownStone',(.58,.58,.57),.88,0),
 ('BrownFrame','TownPaintBrown',(.40,.25,.18),.55,0),
 ('Door','TownPaintBrown',(.45,.27,.18),.60,0),
 ('Step','TownStone',(.52,.50,.47),.88,0),
 ('Roof','TownMetalGrey',(.25,.26,.28),.55,.30),
 ('Chimney','TownIvory',(.62,.40,.32),.90,0),
 ('Dark','TownMetalGrey',(.05,.055,.06),.40,.20),
 ]:
 name='M_Block69_'+key;B69[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block69_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B69;WH=M['White'];YL=M['Yellow']

def b69_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block69_names.append(name);return Mesh(name,category)
def b69_finish(m,osm):
 obj=s21_finish(m);obj['detail_pass']=69;obj['reference_notes']='references/block69-notes.md';obj['osm_way']=osm;return obj
def cas69(m,x,y,u,b,w,h,a,o=.18):
 facade_box(m,x,y,u,o-.04,b+h/2,w,.02,h,GLAZE,a)
 for q in (-w/2+.04,w/2-.04,0):facade_box(m,x,y,u+q,o,b+h/2,.08 if q else .07,.08,h,M['BrownFrame'],a)
 for zz in (b+.04,b+h-.04,b+h*.68):facade_box(m,x,y,u,o,zz,w,.08,.06,M['BrownFrame'],a)

GF_B,GF_H,UP_B,UP_H=1.69,1.47,4.54,1.52
def front69(m,w,axes,door=None,cellars=()):
 # axes: (u, width) of the window pairs, one over the other; door: (u, width) under an upper window.
 x,y,L,a=sf_edge(w['p'],w['q'])
 gf=[(u,GF_B,ww,GF_H,0) for u,ww in axes];up=[(u,UP_B,ww,UP_H,0) for u,ww in axes]
 if door:up.append((door[0],UP_B,.98,UP_H,0));dr=(door[0],.93,door[1],2.22,0)
 cel=[(u,.31,.65,.34,0) for u in cellars]
 bz_wall(m,w['p'],w['q'],0,H,gf+up+cel+([dr] if door else []),YL)
 # The rusticated ground floor: grooves broken round the openings.
 for k in range(1,10):
  zz=.72+k*.30;at=-L/2
  for uu,ww in sorted([(u,ww+.30) for u,b,ww,hh,r in gf if b-.1<zz<b+hh+.1]+([(dr[0],dr[2]+.30)] if door and zz<3.2 else [])):
   if uu-ww/2>at+.05:facade_box(m,x,y,(at+uu-ww/2)/2,.37,zz,uu-ww/2-at,.03,.025,M['Groove'],a)
   at=max(at,uu+ww/2)
  if L/2>at+.05:facade_box(m,x,y,(at+L/2)/2,.37,zz,L/2-at,.03,.025,M['Groove'],a)
 for u,b,ww,hh,r in gf:
  cas69(m,x,y,u,b,ww,hh,a);facade_box(m,x,y,u,.44,b-.04,ww+.16,.16,.06,M['BrownFrame'],a)
  facade_box(m,x,y,u,.40,1.25,ww+.10,.06,.60,YL,a)
 for u,b,ww,hh,r in up:
  cas69(m,x,y,u,b,ww,hh,a);surround36(m,x,y,u,b,ww,hh,a,WH,.12,.40)
  for s in (-1,1):facade_box(m,x,y,u+s*(ww/2+.06),.40,(3.98+b)/2,.12,.06,b-3.98,WH,a)
  facade_box(m,x,y,u,.39,(4.02+b-.1)/2,ww-.10,.06,b-.1-4.02,YL,a)
 if door:
  u,b,ww,hh,r=dr
  for s in (-1,1):
   facade_box(m,x,y,u+s*ww/4,.10,b+hh/2,ww/2-.02,.06,hh,M['Door'],a)
   facade_box(m,x,y,u+s*ww/4,.14,b+hh*.70,ww/2-.22,.02,hh*.36,GLAZE,a)
   facade_box(m,x,y,u+s*ww/4,.15,b+hh*.25,ww/2-.22,.03,hh*.30,M['Door'],a)
  steps36(m,x,y,u,a,1.5,1.3,b,3,.30,M['Step'])
 for u,b,ww,hh,r in cel:
  facade_box(m,x,y,u,.44,b+hh/2,ww,.02,hh,M['Dark'],a);facade_box(m,x,y,u,.46,b+hh/2,.03,.03,hh,M['BrownFrame'],a)
  for zz in (b,b+hh):facade_box(m,x,y,u,.46,zz,ww+.06,.04,.05,M['BrownFrame'],a)
 at=-L/2
 for uu,w2 in (([(dr[0],1.4)] if door else [])+[(L/2+2,0)]):
  lo=max(-L/2,min(L/2,uu-w2/2))
  if lo>at+.03:facade_box(m,x,y,(at+lo)/2,.39,.36,lo-at,.08,.72,M['Plinth'],a)
  at=max(at,min(L/2,uu+w2/2))
 facade_box(m,x,y,0,.42,3.72,L,.10,.18,WH,a);facade_box(m,x,y,0,.48,3.90,L+.04,.22,.16,WH,a)
 facade_box(m,x,y,0,.42,6.78,L,.10,.18,WH,a);facade_box(m,x,y,0,.52,6.98,L+.06,.28,.22,WH,a);facade_box(m,x,y,0,.66,7.16,L+.14,.52,.10,WH,a)

m=b69_new('SM_Kvarnholmen_House_91926315','Kvarnholmen/Proviantgatan')
H=Z['ch']['height']
for w in walls('ch'):
 x,y,L,a=sf_edge(w['p'],w['q']);ox,oy=outward(w)
 X0,Y0=[(w['p'][i]+w['q'][i])/2 for i in (0,1)]
 if w['kind']!='outer':bz_wall(m,w['p'],w['q'],w['z0'],H,[],YL);continue
 if oy>.9 and L>5:
  front69(m,w,[(U(w,X,61.0),ww) for X,ww in ((173.8,.95),(171.15,.90))],None,[U(w,X,61.0) for X in (173.8,171.15)])
 elif ox>.9 and L>5:
  front69(m,w,[(U(w,177.3,Y),ww) for Y,ww in ((50.65,.85),(52.33,.92),(56.17,.93),(57.95,.94))],(U(w,177.3,54.29),1.14),[U(w,177.3,Y) for Y in (52.33,56.17,57.95)])
 elif ox>.3 and oy>.3 and L>1.1 and Y0>60.4:
  # The canted corner: its window pair on the face next to Norra Långgatan.
  front69(m,w,[(0,.78)])
 elif ox>.3 and oy>.3:
  front69(m,w,[])
 else:plain(m,w,H,YL,M['BrownFrame'],WH,2,.9)
for g in Z['ch']['polygons']:
 pts=simplify([tuple(v) for v in g],.8)
 inset_roof(m,pts,H,min(2.6,.45*min(math.dist(p,q) for p,q in zip(pts,pts[1:]+pts[:1]))),Z['ch']['top']-H,M['Roof'],.40)
box(m,172.0,56.0,.55,.75,1.2,Z['ch']['top']-.7,M['Chimney'],0,M['Dark'])
b69_finish(m,'91926315')

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block69_cameras=[
 sv_camera('357_Block69_Cal_Corner',175.53,68.37+.355,2.43,172,10,90),
 sv_camera('358_Block69_Cal_Proviant',181.59+.355,55.23,2.30,242,10,90),
 ('359_Block69_Aerial',(192.0,70.0,24.0),(172.0,55.0,3.0),28),
]
print('BLOCK69_GEOMETRY',len(block69_names))
