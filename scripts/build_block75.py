"""Pass 75: the district volume 93192446 on the corner of Proviantgatan and Norra Långgatan, four
houses split at their measured joints:
- the last metre of the narrow white house with the red door (pass 74);
- number 20, a cream three-storey house on Proviantgatan: a rusticated ground floor over a granite
  plinth with vents, the red door with its fanlight in a dark stone surround up four steps, a band,
  five axes of dark green casements in white surrounds, hoods over the first floor, a cornice and a
  dark mansard;
- number 22, the light ochre corner house: two storeys with white corner strips, white-framed
  windows on both fronts, the red door (22) in a stone surround on Proviantgatan, and a hipped roof
  with a dormer;
- the dark ochre roughcast range on Norra Långgatan: dark-framed windows (two small ones in the
  middle), a blue-grey plinth, a white cornice, and six large red boarded dormers on a dark roof.

References: Google Street View April 2025 (the pass 70 panorama facing number 20, and two panoramas
on Norra Långgatan resected on the corner, the range's east end and the base row; the east one
predicts the corner house's joint within 3 px), view only. Zones: source/block75.json; see
references/block75-notes.md. The signs, lamps and letterbox are omitted.
"""
B75D=json.loads((R/'source/block75.json').read_text());Z=B75D['zones']
block75_names=[];B75={}
for old in [k for k in list(materials) if k.startswith('M_Block75_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Cream','TownIvory',(.90,.86,.76),.92,0),
 ('CreamGF','TownIvory',(.88,.85,.77),.92,0),
 ('Groove','TownIvory',(.70,.67,.60),.95,0),
 ('White','TownIvory',(.95,.95,.93),.84,0),
 ('WhiteWall','TownIvory',(.93,.93,.91),.92,0),
 ('Granite','TownStone',(.50,.38,.32),.88,0),
 ('StoneSurround','TownStone',(.45,.33,.27),.88,0),
 ('GreenFrame','TownPaintGreen',(.20,.28,.22),.55,0),
 ('RedDoor','TownPaintBrown',(.60,.16,.12),.60,0),
 ('Ochre22','TownIvory',(.90,.73,.47),.92,0),
 ('OchreRange','TownIvory',(.82,.62,.28),.96,0),
 ('BluePlinth','TownIvory',(.45,.50,.60),.92,0),
 ('GreyPlinth','TownIvory',(.78,.79,.80),.92,0),
 ('DarkFrame','TownPaintBrown',(.14,.12,.11),.55,0),
 ('RedDormer','TownPaintBrown',(.58,.20,.16),.60,0),
 ('Mansard','TownMetalGrey',(.16,.17,.19),.55,.25),
 ('Slate','TownMetalGrey',(.30,.32,.34),.55,.25),
 ('Tile','TownTileRed',(.55,.30,.24),.80,0),
 ('Dark','TownMetalGrey',(.05,.055,.06),.40,.20),
 ]:
 name='M_Block75_'+key;B75[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block75_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B75;WH=M['White']

def b75_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block75_names.append(name);return Mesh(name,category)
def b75_finish(m,osm):
 obj=s21_finish(m);obj['detail_pass']=75;obj['reference_notes']='references/block75-notes.md';obj['osm_way']=osm;return obj
def cas75(m,x,y,u,b,w,h,a,frame,o=.16,transom=.70):
 facade_box(m,x,y,u,o-.04,b+h/2,w,.02,h,GLAZE,a)
 for q in (-w/2+.04,w/2-.04,0):facade_box(m,x,y,u+q,o,b+h/2,.08 if q else .06,.08,h,frame,a)
 for zz in (b+.04,b+h-.04,b+h*transom):facade_box(m,x,y,u,o,zz,w,.08,.06,frame,a)
def grooves75(m,x,y,L,a,z0,z1,step,holes,ma,o=.37):
 # Rustication: horizontal grooves broken round the openings.
 k=1
 while z0+k*step<z1-.05:
  zz=z0+k*step;at=-L/2;k+=1
  for uu,ww in sorted([(u,ww+.26) for u,b,ww,hh,r in holes if b-.1<zz<b+hh+.1]):
   if uu-ww/2>at+.05:facade_box(m,x,y,(at+uu-ww/2)/2,o,zz,uu-ww/2-at,.03,.025,ma,a)
   at=max(at,uu+ww/2)
  if L/2>at+.05:facade_box(m,x,y,(at+L/2)/2,o,zz,L/2-at,.03,.025,ma,a)
def plinth75(m,x,y,L,a,h,ma,gaps=()):
 at=-L/2
 for uu,ww in sorted(gaps)+[(L/2+2,0)]:
  lo=max(-L/2,min(L/2,uu-ww/2))
  if lo>at+.03:facade_box(m,x,y,(at+lo)/2,.39,h/2,lo-at,.08,h,ma,a)
  at=max(at,min(L/2,uu+ww/2))
def door75(m,x,y,u,b,ww,hh,a,surround,steps):
 for s in (-1,1):
  facade_box(m,x,y,u+s*ww/4,.10,b+(hh-.55)/2,ww/2-.02,.06,hh-.55,M['RedDoor'],a)
  facade_box(m,x,y,u+s*ww/4,.14,b+(hh-.55)*.68,ww/2-.20,.02,(hh-.55)*.45,GLAZE,a)
 facade_box(m,x,y,u,.12,b+hh-.27,ww,.02,.46,GLAZE,a);facade_box(m,x,y,u,.16,b+hh-.55,ww,.06,.06,M['RedDoor'],a)
 for s in (-1,1):facade_box(m,x,y,u+s*(ww/2+.16),.44,(b+hh+.2)/2,.30,.14,b+hh+.2,surround,a)
 facade_box(m,x,y,u,.46,b+hh+.16,ww+.62,.16,.32,surround,a)
 if steps:steps36(m,x,y,u,a,ww+.9,ww+.4,b,steps,.30,M['Granite'])

def dormer75(m,x,y,u,a,H,bw,bh,ww,wh,depth=1.7,rise=.95):
 # A boarded wall dormer on the range: its front in the wall plane, a short body back into the low
 # roof, a gabled roof and a white-framed window.
 facade_box(m,x,y,u,.355-depth/2,H+bh/2,bw,depth,bh,M['RedDormer'],a)
 for s in (-1,1):
  q=[lp(x,y,u+s*(bw/2+.12),o,H+bh-.02,a) for o in (.45,.355-depth)]+[lp(x,y,u,o,H+bh+rise,a) for o in (.355-depth,.45)]
  m.faces(q,[(0,1,2,3) if s<0 else (3,2,1,0)],M['RedDormer'])
 tri=[lp(x,y,u-bw/2,.36,H+bh,a),lp(x,y,u+bw/2,.36,H+bh,a),lp(x,y,u,.36,H+bh+rise-.05,a)]
 m.faces(tri,[(0,1,2)],M['RedDormer'])
 b=H+.35;facade_box(m,x,y,u,.33,b+wh/2,ww,.02,wh,GLAZE,a)
 for q in (-ww/2+.04,ww/2-.04,0):facade_box(m,x,y,u+q,.38,b+wh/2,.08 if q else .06,.06,wh,WH,a)
 for zz in (b+.04,b+wh-.04):facade_box(m,x,y,u,.38,zz,ww,.06,.07,WH,a)

m=b75_new('SM_Kvarnholmen_House_93192446','Kvarnholmen/Proviantgatan')
def xw75(Y):return 188.918+(Y-61.129)*(188.968-188.918)/(36.534-61.129)
for zone in ('wh','n20','n22','rg'):
 H=Z[zone]['height']
 for w in walls(zone):
  x,y,L,a=sf_edge(w['p'],w['q']);ox,oy=outward(w)
  street=w['kind']=='outer' and ((ox<-.9 and zone in ('wh','n20','n22')) or (oy>.9 and zone in ('n22','rg')))
  if not street:
   if w['kind']=='outer':plain(m,w,H,M[{'wh':'WhiteWall','n20':'Cream','n22':'Ochre22','rg':'OchreRange'}[zone]],M['DarkFrame'],WH,3 if zone=='n20' else 2,.9)
   else:bz_wall(m,w['p'],w['q'],w['z0'],H,[],M[{'wh':'WhiteWall','n20':'Cream','n22':'Ochre22','rg':'OchreRange'}[zone]])
   continue
  if zone=='wh':
   bz_wall(m,w['p'],w['q'],0,H,[],M['WhiteWall'])
   facade_box(m,x,y,0,.39,.30,L,.08,.60,M['GreyPlinth'],a)
   facade_box(m,x,y,0,.42,H-.15,L,.10,.30,WH,a);facade_box(m,x,y,0,.56,H+.05,L+.06,.36,.14,WH,a)
  elif zone=='n20':
   S=lambda Y:U(w,xw75(Y),Y)
   AX=[48.23,45.8,40.84,38.4]
   gf=[(S(Y0),1.97,1.25,1.89,0) for Y0 in AX];mid=[(S(Y0),5.45,1.28,1.97,0) for Y0 in AX+[43.3]];top=[(S(Y0),9.01,1.30,1.80,0) for Y0 in AX+[43.3]]
   door=(S(43.47),1.37,1.10,2.34,0)
   bz_wall(m,w['p'],w['q'],0,H,gf+mid+top+[door],M['Cream'])
   grooves75(m,x,y,L,a,.92,4.75,.30,gf+[(door[0],door[1],door[2]+.6,door[3]+.4,0)],M['Groove'],.39)
   for u,b,ww,hh,r in gf+mid+top:
    cas75(m,x,y,u,b,ww,hh,a,M['GreenFrame'],.18)
    if b>3:surround36(m,x,y,u,b,ww,hh,a,WH,.12,.40)
    facade_box(m,x,y,u,.47,b-.06,ww+.30,.16,.06,WH,a)
   for u,b,ww,hh,r in mid:facade_box(m,x,y,u,.46,b+hh+.28,ww+.36,.18,.10,WH,a);facade_box(m,x,y,u,.44,b+hh+.18,ww+.24,.10,.10,WH,a)
   door75(m,x,y,*door[:4],a,M['StoneSurround'],4)
   plinth75(m,x,y,L,a,.92,M['Granite'],[(door[0],2.2)])
   for u,b,ww,hh,r in gf:facade_box(m,x,y,u,.44,.45,.45,.04,.30,M['WhiteWall'],a);facade_box(m,x,y,u,.46,.45,.28,.04,.16,M['Dark'],a)
   facade_box(m,x,y,0,.42,4.85,L,.10,.20,M['Dark'],a);facade_box(m,x,y,0,.50,5.08,L+.04,.26,.26,WH,a)
   facade_box(m,x,y,0,.42,12.35,L,.10,.30,WH,a);facade_box(m,x,y,0,.56,12.68,L+.06,.36,.40,WH,a);facade_box(m,x,y,0,.70,12.92,L+.16,.62,.10,WH,a)
   for Y0 in (48.23,45.8,43.3,40.84,38.4):
    u=S(Y0);d=.55;zf=H+.55
    box(m,*lp(x,y,u,-d-.6,0,a)[:2],1.2,1.2,1.35,zf,M['Mansard'],a,M['Mansard'])
    facade_box(m,x,y,u,-d+.02,zf+.68,.90,.04,.95,GLAZE,a)
    for q in (-.42,.42,0):facade_box(m,x,y,u+q,-d+.06,zf+.68,.08 if q else .06,.06,.95,WH,a)
  elif zone=='n22' and ox<-.9:
   S=lambda Y:U(w,xw75(Y),Y)
   gf=[(S(Y0),1.47,1.25,1.81,0) for Y0 in (54.07,56.96,59.28)];up=[(S(Y0),4.47,1.28,2.0,0) for Y0 in (51.47,54.13,57.05,59.46)]
   door=(S(50.95),1.03,1.0,2.43,0)
   bz_wall(m,w['p'],w['q'],0,H,gf+up+[door],M['Ochre22'])
   for u,b,ww,hh,r in gf+up:cas75(m,x,y,u,b,ww,hh,a,WH,.16,.66);surround36(m,x,y,u,b,ww,hh,a,WH,.12,.40);facade_box(m,x,y,u,.47,b-.06,ww+.30,.16,.06,WH,a)
   door75(m,x,y,*door[:4],a,M['StoneSurround'],3)
   plinth75(m,x,y,L,a,.58,M['GreyPlinth'],[(door[0],2.0)])
   facade_box(m,x,y,-L/2+.18,.42,(.58+H)/2,.36,.10,H-.58,WH,a)
   facade_box(m,x,y,0,.42,H-.15,L,.10,.30,WH,a);facade_box(m,x,y,0,.56,H+.05,L+.06,.36,.14,WH,a)
  elif zone=='n22':
   S=lambda X:U(w,X,61.13)
   gf=[(S(X0),1.32,1.30,1.92,0) for X0 in (191.4,195.77)];up=[(S(X0),4.38,1.30,2.07,0) for X0 in (191.4,195.77)]
   bz_wall(m,w['p'],w['q'],0,H,gf+up,M['Ochre22'])
   for u,b,ww,hh,r in gf+up:cas75(m,x,y,u,b,ww,hh,a,WH,.16,.66);surround36(m,x,y,u,b,ww,hh,a,WH,.12,.40);facade_box(m,x,y,u,.47,b-.06,ww+.30,.16,.06,WH,a)
   facade_box(m,x,y,0,.39,.29,L,.08,.58,M['GreyPlinth'],a)
   for uu in (-L/2+.18,L/2-.18):facade_box(m,x,y,uu,.42,(.58+H)/2,.36,.10,H-.58,WH,a)
   facade_box(m,x,y,0,.42,H-.15,L,.10,.30,WH,a);facade_box(m,x,y,0,.56,H+.05,L+.06,.36,.14,WH,a)
   sl=(Z['n22']['top']-H)/3.0
   roof_dormer(m,x,y,S(193.66),a,H,sl,.6,1.0,1.1,M['Slate'],M['Slate'],WH,False)
  elif zone=='rg':
   S=lambda X:U(w,X,61.14)
   AX=[(220.27,1.40),(217.36,1.36),(214.9,1.40),(211.3,1.42),(208.35,1.42),(206.1,.80),(203.43,1.43),(200.33,1.40)]
   gf=[(S(X0),.93 if ww>1 else 1.30,ww,1.57 if ww>1 else .80,0) for X0,ww in AX]
   up=[(S(X0),3.65 if ww>1 else 4.05,ww,1.60 if ww>1 else .80,0) for X0,ww in AX]
   bz_wall(m,w['p'],w['q'],0,H,gf+up,M['OchreRange'])
   for u,b,ww,hh,r in gf+up:cas75(m,x,y,u,b,ww,hh,a,M['DarkFrame'],.16,.99 if ww<1 else .70);surround36(m,x,y,u,b,ww,hh,a,WH,.10,.40)
   facade_box(m,x,y,0,.39,.15,L,.08,.30,M['BluePlinth'],a)
   facade_box(m,x,y,0,.42,H-.2,L,.10,.26,WH,a);facade_box(m,x,y,0,.56,H+.02,L+.06,.36,.20,WH,a)
   sl=(Z['rg']['top']-H)/3.5
   for X0 in (217.4,214.9,211.8,208.95,203.45,200.2):dormer75(m,x,y,S(X0),a,H,1.85,1.9,1.35,1.05)
 for g in Z[zone]['polygons']:
  pts=simplify([tuple(v) for v in g],.6)
  if zone=='n20':
   inset_roof(m,pts,H,1.1,Z[zone]['top']-H,M['Mansard'],.30)
  else:
   inset_roof(m,pts,H,min(3.2,.45*min(math.dist(p,q) for p,q in zip(pts,pts[1:]+pts[:1]))),Z[zone]['top']-H,{'wh':M['Tile'],'n22':M['Slate'],'rg':M['Slate']}[zone],.35)
box(m,193.0,55.0,.55,.75,1.0,Z['n22']['top']-.6,M['Slate'],0,M['Dark'])
box(m,210.0,55.0,.55,.75,1.0,Z['rg']['top']-.6,M['Tile'],0,M['Dark'])
b75_finish(m,'93192446')

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block75_cameras=[
 sv_camera('374_Block75_Cal_Twenty',181.51-.355,44.84,2.30,62,10,90),
 sv_camera('375_Block75_Cal_Corner',201.67,68.51+.355,2.30,152,10,90),
 sv_camera('376_Block75_Cal_Range',221.59,68.39+.355,2.30,202,10,90),
 ('377_Block75_Aerial',(205.0,78.0,30.0),(200.0,52.0,3.0),28),
]
print('BLOCK75_GEOMETRY',len(block75_names))
