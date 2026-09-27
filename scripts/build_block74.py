"""Pass 74: the district volume 93192350 on the east side of Proviantgatan:
- the beige rendered three-storey house: a grey plinth with cellar windows, a grooved grey ground
  floor under a band, three axes of wide white-framed casements in white surrounds on every storey,
  a cornice, and a tile roof with white box dormers;
- the southern part of the narrow white three-storey house with the red panelled door and wide
  upper windows, which continues into the next volume.

References: Google Street View April 2025 (two panoramas on Proviantgatan whose views meet at about
95 degrees; the three vertical joints they share triangulate on one line about 0.8 m in front of the
district outline, and the front is kept on the outline), view only. Zones: source/block74.json; see
references/block74-notes.md. The street lamp is omitted.
"""
B74D=json.loads((R/'source/block74.json').read_text());Z=B74D['zones']
block74_names=[];B74={}
for old in [k for k in list(materials) if k.startswith('M_Block74_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Beige','TownIvory',(.80,.76,.70),.94,0),
 ('Band','TownIvory',(.72,.70,.66),.94,0),
 ('Groove','TownIvory',(.60,.58,.55),.95,0),
 ('White','TownIvory',(.94,.94,.92),.84,0),
 ('WhiteFrame','TownPaintWhite',(.95,.95,.93),.55,0),
 ('Plinth','TownIvory',(.36,.36,.37),.94,0),
 ('RedDoor','TownPaintBrown',(.62,.16,.14),.60,0),
 ('Tile','TownTileRed',(.46,.30,.26),.80,0),
 ('Dark','TownMetalGrey',(.05,.055,.06),.40,.20),
 ]:
 name='M_Block74_'+key;B74[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block74_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B74;WH=M['White'];BG=M['Beige']

def b74_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block74_names.append(name);return Mesh(name,category)
def b74_finish(m,osm):
 obj=s21_finish(m);obj['detail_pass']=74;obj['reference_notes']='references/block74-notes.md';obj['osm_way']=osm;return obj
def xw74(Y):return 188.981+(Y-25.412)*(188.968-188.981)/(36.534-25.412)
def cas74(m,x,y,u,b,w,h,a,o=.16,lights=2):
 facade_box(m,x,y,u,o-.04,b+h/2,w,.02,h,GLAZE,a)
 for k in range(lights+1):
  q=-w/2+.04+k*(w-.08)/lights;facade_box(m,x,y,u+q,o,b+h/2,.08 if k in (0,lights) else .06,.08,h,M['WhiteFrame'],a)
 for zz in (b+.04,b+h-.04,b+h*.72):facade_box(m,x,y,u,o,zz,w,.08,.06,M['WhiteFrame'],a)

m=b74_new('SM_Kvarnholmen_House_93192350','Kvarnholmen/Proviantgatan')
for zone in ('bg','wh'):
 H=Z[zone]['height']
 for w in walls(zone):
  x,y,L,a=sf_edge(w['p'],w['q']);ox,oy=outward(w)
  if w['kind']=='outer' and ox<-.9 and zone=='bg':
   S=lambda Y:U(w,xw74(Y),Y)
   rows=[(1.97,1.64),(4.75,1.89),(7.35,1.90)]
   wins=[(S(Y0),b,1.45,h,0) for Y0 in (27.04,29.83,32.52) for b,h in rows]
   cel=[(S(Y0),.40,.95,.50,0) for Y0 in (27.04,29.83,32.52)]
   bz_wall(m,w['p'],w['q'],0,H,wins+cel,BG)
   for u,b,ww,hh,r in wins:
    cas74(m,x,y,u,b,ww,hh,a);surround36(m,x,y,u,b,ww,hh,a,WH,.10,.39)
    facade_box(m,x,y,u,.46,b-.06,ww+.26,.16,.06,WH,a)
   for u,b,ww,hh,r in cel:
    facade_box(m,x,y,u,.44,b+hh/2,ww,.02,hh,M['Dark'],a);surround36(m,x,y,u,b,ww,hh,a,M['WhiteFrame'],.06,.44)
   # The grooved grey ground floor under its band, broken round the windows.
   at=-L/2
   for uu,ww in sorted([(u,ww+.20) for u,b,ww,hh,r in wins if b<3])+[(L/2+1,0)]:
    lo=min(L/2,uu-ww/2)
    if lo>at+.03:facade_box(m,x,y,(at+lo)/2,.37,(1.46+4.22)/2,lo-at,.02,4.22-1.46,M['Band'],a)
    at=max(at,uu+ww/2)
   for u,b,ww,hh,r in wins:
    if b<3:
     for zz,hz in ((1.46+(b-.1-1.46)/2,b-.1-1.46),(b+hh+.1+(4.22-b-hh-.1)/2,4.22-b-hh-.1)):facade_box(m,x,y,u,.37,zz,ww+.20,.02,hz,M['Band'],a)
   for k in range(1,9):
    zz=1.46+k*.30;at=-L/2
    for uu,ww in sorted([(u,ww+.24) for u,b,ww,hh,r in wins if b<3 and b-.1<zz<b+hh+.1]):
     if uu-ww/2>at+.05:facade_box(m,x,y,(at+uu-ww/2)/2,.39,zz,uu-ww/2-at,.03,.025,M['Groove'],a)
     at=uu+ww/2
    if L/2>at+.05:facade_box(m,x,y,(at+L/2)/2,.39,zz,L/2-at,.03,.025,M['Groove'],a)
   facade_box(m,x,y,0,.39,.73,L,.08,1.46,M['Plinth'],a)
   facade_box(m,x,y,0,.44,4.33,L,.14,.22,M['Band'],a)
   facade_box(m,x,y,0,.42,11.25,L,.10,.24,WH,a);facade_box(m,x,y,0,.54,11.6,L+.06,.32,.46,WH,a);facade_box(m,x,y,0,.68,11.9,L+.16,.58,.14,WH,a)
   sl=(Z['bg']['top']-H)/3.0
   for Y0 in (26.2,28.4,30.6,32.8):
    u=S(Y0);d=.6;zf=H+d*sl
    box(m,*lp(x,y,u,-d-1.2,0,a)[:2],1.3,2.4,1.7,zf-.3,WH,a,M['Dark'])
    facade_box(m,x,y,u,-d+.02,zf+.62,.95,.04,1.0,GLAZE,a)
    for q in (-.44,.44,0):facade_box(m,x,y,u+q,-d+.06,zf+.62,.08 if q else .06,.06,1.0,M['WhiteFrame'],a)
  elif w['kind']=='outer' and ox<-.9 and zone=='wh':
   S=lambda Y:U(w,xw74(Y),Y)
   door=(S(35.41),.35,1.25,2.75,0)
   ups=[(S(35.25),b,1.9,1.75,0) for b in (4.6,7.4)]
   bz_wall(m,w['p'],w['q'],0,H,[door]+ups,WH)
   u,b,ww,hh,r=door
   for s in (-1,1):
    facade_box(m,x,y,u+s*ww/4,.10,b+(hh-.5)/2,ww/2-.02,.06,hh-.5,M['RedDoor'],a)
    for zz in (b+.5,b+1.4):facade_box(m,x,y,u+s*ww/4,.14,zz,ww/2-.22,.03,.7,M['RedDoor'],a)
   facade_box(m,x,y,u,.12,b+hh-.25,ww,.02,.45,GLAZE,a);facade_box(m,x,y,u,.16,b+hh-.5,ww,.06,.06,M['RedDoor'],a)
   surround36(m,x,y,u,b,ww,hh,a,WH,.10,.39)
   for u,b,ww,hh,r in ups:cas74(m,x,y,u,b,ww,hh,a,.16,3);surround36(m,x,y,u,b,ww,hh,a,WH,.10,.39)
   facade_box(m,x,y,0,.39,.30,L,.08,.60,M['Plinth'],a)
   facade_box(m,x,y,0,.42,H-.15,L,.10,.30,WH,a);facade_box(m,x,y,0,.56,H+.05,L+.06,.36,.14,WH,a)
  else:
   if w['kind']=='outer':plain(m,w,H,BG if zone=='bg' else WH,M['WhiteFrame'],WH,3,.9)
   else:bz_wall(m,w['p'],w['q'],w['z0'],H,[],BG if zone=='bg' else WH)
 for g in Z[zone]['polygons']:
  pts=simplify([tuple(v) for v in g],.8)
  inset_roof(m,pts,Z[zone]['height'],min(3.0,.45*min(math.dist(p,q) for p,q in zip(pts,pts[1:]+pts[:1]))),Z[zone]['top']-Z[zone]['height'],M['Tile'],.30)
b74_finish(m,'93192350')

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block74_cameras=[
 sv_camera('371_Block74_Cal_FromSouth',180.98-.355,24.44,2.50,20,10,90),
 sv_camera('372_Block74_Cal_FromNorth',181.51-.355,44.84,2.30,115,10,90),
 ('373_Block74_Aerial',(176.0,31.0,26.0),(196.0,31.0,4.0),28),
]
print('BLOCK74_GEOMETRY',len(block74_names))
