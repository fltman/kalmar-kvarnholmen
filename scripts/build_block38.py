"""Pass 38: two district volumes on the north side of Södra Långgatan, opposite pass 37: number 27
(92379256) and the Barometern newspaper building (92379310).

Number 27: yellow render with white trim, two storeys; a shop window, the glazed door with steps, a
wide shop window and the drug store's front in white surrounds; a band; five windows in white
surrounds under cornice heads; the eaves cornice; a dark roof with two small dormers.

The Barometern building, three storeys over a stone-clad ground floor, flat-roofed, in four parts
from Ölandsgatan: a yellow corner with an open arcade, eight axes and a pale vertical band; a tiled
bay with the recessed entrance; a salmon office front with pale horizontal and vertical bands and
groups of narrow windows; a glass and slate curtain wall with a mosaic-tiled pier, a shop window and
the garage. The yellow corner's windows continue along Ölandsgatan.

References: Google Street View April 2025 (the pass 37 registrations), view only. Zones:
source/block38.json; see references/block38-notes.md. The newspaper's signs, the posters and the
exhibition texts in the windows, and the mosaic's figures are omitted.
"""
B38D=json.loads((R/'source/block38.json').read_text());Z=B38D['zones']
block38_names=[];B38={}
for old in [k for k in list(materials) if k.startswith('M_Block38_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Yellow27','TownIvory',(.92,.80,.54),.88,0),
 ('White','TownIvory',(.93,.93,.90),.82,0),
 ('Salmon','TownIvory',(.78,.52,.43),.90,0),
 ('Ochre','TownIvory',(.90,.77,.50),.90,0),
 ('Pale','TownIvory',(.86,.82,.72),.86,0),
 ('Cladding','TownStone',(.80,.75,.66),.84,0),
 ('Tile','TownStone',(.55,.45,.32),.70,0),
 ('Mosaic','TownPanel',(.84,.82,.76),.70,0),
 ('Slate','TownMetalGrey',(.36,.38,.40),.55,.20),
 ('Frame','TownMetalGrey',(.12,.12,.13),.45,.30),
 ('GreenDoor','TownPaintBrown',(.42,.52,.46),.55,0),
 ('Shutter','TownMetalGrey',(.62,.63,.64),.50,.40),
 ('RoofDark','TownMetalGrey',(.28,.29,.30),.55,.30),
 ('Dark','TownMetalGrey',(.05,.055,.06),.40,.20),
 ]:
 name='M_Block38_'+key;B38[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block38_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B38;WH,CL=M['White'],M['Cladding']

def b38_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block38_names.append(name);return Mesh(name,category)
def b38_finish(m,osm):
 obj=s21_finish(m);obj['detail_pass']=38;obj['reference_notes']='references/block38-notes.md';obj['osm_way']=osm;return obj
def street38(w):
 ox,oy=outward(w);return w['kind']=='outer' and oy<-.9 and min(w['p'][1],w['q'][1])<-68
def olands38(w):
 ox,oy=outward(w);return w['kind']=='outer' and ox>.9 and min(w['p'][0],w['q'][0])>-41
def others38(m,zone,wall,frame,levels):
 for w in walls(zone):
  if street38(w) or olands38(w):continue
  if w['kind']!='outer':bz_wall(m,w['p'],w['q'],w['z0'],Z[zone]['height'],[],wall)
  else:plain(m,w,Z[zone]['height'],wall,frame,WH,levels,.9)
def flat38(m,zone,ma,rise=.25):
 for g in Z[zone]['polygons']:
  pts=simplify([tuple(v) for v in g],.3)
  inset_roof(m,pts,Z[zone]['height'],1.2,rise,ma,.05)
def win38(m,x,y,u,b,w,h,a,frame=None):
 # A plain modern casement: a slim dark frame flush-ish in the render, a transom and a metal sill.
 frame=frame or WH
 facade_box(m,x,y,u,.18,b+h/2,w,.02,h,GLAZE,a)
 for q in (-w/2+.035,w/2-.035):facade_box(m,x,y,u+q,.23,b+h/2,.07,.08,h,frame,a)
 for zz in (b+.035,b+h-.035,b+h*.72):facade_box(m,x,y,u,.23,zz,w,.08,.06,frame,a)
 facade_box(m,x,y,u,.42,b-.02,w+.08,.16,.03,METAL,a)
def shopfront38(m,x,y,u,b,w,h,a,frame,cols=3):
 facade_box(m,x,y,u,.12,b+h/2,w,.03,h,GLAZE,a)
 for k in range(cols+1):facade_box(m,x,y,u-w/2+k*w/cols,.22,b+h/2,.08,.12,h,frame,a)
 for zz in (b+.04,b+h-.04,b+h*.82):facade_box(m,x,y,u,.22,zz,w,.12,.08,frame,a)

# ---------------------------------------------------------------- number 27
m=b38_new('SM_Building_92379256','Kvarnholmen/Södra Långgatan north')
Y7=M['Yellow27'];H7=Z['n27']['height']
others38(m,'n27',Y7,WH,2)
for w in walls('n27'):
 if not street38(w):continue
 x,y,L,a=sf_edge(w['p'],w['q']);S=lambda s:L/2-s                      # s from the east joint
 gf=[(S(2.06),.78,2.09,2.26,0),(S(3.53),.54,.75,2.46,0),(S(6.65),.78,3.27,2.37,0),(S(10.05),.50,2.70,2.60,0)]
 # The windows' glass 4.24-5.99 in surrounds 3.97-6.21, under cornice heads 6.65-6.94.
 up=[(S(s),4.22,1.04,1.78,0) for s in (1.57,3.62,5.64,7.66,9.70)]
 bz_wall(m,w['p'],w['q'],0,H7,gf+up,Y7)
 for i,(u,b,ww,hh,r) in enumerate(gf):
  surround36(m,x,y,u,b,ww,hh,a,WH,.15)
  if i==1:
   s20_door(m,x,y,u,b,ww,hh,a,M['GreenDoor'])
   steps36(m,x,y,u,a,1.1,.9,.54,3,.75,CL)
  else:shopfront38(m,x,y,u,b,ww,hh,a,WH,2 if ww<3 else 3)
 for u,b,ww,hh,r in up:
  surround36(m,x,y,u,b,ww,hh,a,WH,.12);casement36(m,x,y,u,b,ww,hh,a,WH,3,.70,.20)
  facade_box(m,x,y,u,.42,b+hh+.50,ww+.46,.14,.12,WH,a);facade_box(m,x,y,u,.48,b+hh+.64,ww+.56,.26,.18,WH,a)
 plinth36(m,x,y,L,a,[(u-ww/2-.17,u+ww/2+.17) for u,b,ww,hh,r in gf if b<.6],.55,CL)
 facade_box(m,x,y,0,.42,3.87,L,.12,.14,WH,a);facade_box(m,x,y,0,.47,3.96,L+.04,.20,.05,WH,a)
 eaves37(m,x,y,L,a,H7,WH,.42)
 for s0,s1 in ((0,.25),(11.73,11.98)):facade_box(m,x,y,S((s0+s1)/2),.38,(.55+H7)/2,s1-s0,.05,H7-.55,WH,a)
sl=roof34(m,'n27',M['RoofDark'],Y7)
for w in walls('n27'):
 if street38(w):
  x,y,L,a=sf_edge(w['p'],w['q'])
  for s in (3.6,8.7):
   xx,yy,_=lp(x,y,L/2-s,.355-2.4,0,a);box(m,xx,yy,1.1,1.4,1.0,H7+2.4*sl-.3,M['RoofDark'],a,M['Dark'])
rear35(m,'n27r',Y7,WH,M['RoofDark'],2)
b38_finish(m,'92379256')

# ---------------------------------------------------------------- the Barometern building
m=b38_new('SM_Building_92379310','Kvarnholmen/Södra Långgatan north')
HB=Z['bar']['height']
others38(m,'bar',M['Pale'],M['Frame'],3)
others38(m,'barr',M['Pale'],M['Frame'],2)
def yellow_axes():return [1.29,2.55,3.81,5.05,6.77,8.02,9.28,10.53]
def salmon_axes():
 ax=[]
 for b0,b1 in ((14.1,17.09),(17.38,22.45),(22.74,27.81),(28.10,33.17)):
  u=b0+.63
  while u+.42<b1-.2:ax.append(round(u,2));u+=1.27
 return ax+[34.03,35.30,36.58,37.81,39.15]
for w in walls('bar'):
 x,y,L,a=sf_edge(w['p'],w['q'])
 if street38(w):
  S=lambda s:L/2-s                                                   # s from the Ölandsgatan corner
  YA,SA=yellow_axes(),salmon_axes()
  FL=((4.61,6.11),(7.70,9.14));FC=((4.51,6.00),(7.62,8.97))
  gf=[(S(2.08),0,1.78,2.95,0),(S(4.50),.66,2.36,2.33,0),(S(7.325),.66,2.27,2.33,0),(S(10.09),.66,2.24,2.33,0),(S(13.2),0,3.59,3.30,0),
      (S(17.2),.48,3.4,2.31,0),(S(20.95),.48,3.4,2.31,0),(S(25.1),.48,3.6,2.31,0),(S(29.2),.48,2.67,2.31,0),(S(31.97),.48,1.89,2.31,0),(S(35.21),.48,3.60,2.31,0),(S(38.70),0,2.76,2.79,0),
      (S(42.9),.33,3.8,2.32,0),(S(48.40),.33,2.33,2.32,0),(S(51.10),0,2.45,2.72,0)]
  up=[(S(s),b,.84,t-b,0) for s in YA for b,t in FL]+[(S(s),b,.84,t-b,0) for s in (12.35,13.45) for b,t in FL]+[(S(s),b,.84,t-b,0) for s in SA for b,t in FC]
  # The curtain wall (40.5-45.05 and 47.24-53) is built as its own glazing in two bands.
  cw=[(S((a0+a1)/2),b,a1-a0,t-b,0) for a0,a1 in ((40.55,45.05),(47.24,53.0)) for b,t in ((4.13,6.05),(7.26,9.10))]
  holes=gf+up+cw
  bz_wall(m,w['p'],w['q'],0,3.46,[h for h in holes if h[1]<3.46],CL)
  # The upper storeys in three renders, split at the parts' edges.
  (x0,y0),(x1,y1)=w['p'],w['q'];Lw=math.dist(w['p'],w['q']);ux,uy=(x1-x0)/Lw,(y1-y0)/Lw
  def pt(s):return (x1-ux*s,y1-uy*s)                                  # s from the east end (q is east)
  for s0,s1,ma in ((0,11.5,M['Ochre']),(11.5,14.1,M['Tile']),(14.1,40.5,M['Salmon']),(40.5,53.0,M['Slate'])):
   xs,ys,Ls,aa=sf_edge(pt(s1),pt(s0))
   loc=[(h[0]-S((s0+s1)/2),h[1],h[2],h[3],0) for h in holes if h[1]>=3.46 and abs(h[0]-S((s0+s1)/2))<(s1-s0)/2]
   bz_wall(m,pt(s1),pt(s0),3.46,HB,loc,ma)
  for u,b,ww,hh,r in gf:
   if b==0 and ww<2.0:
    # The arcade at the corner: an open bay 2 m deep with a ceiling and a back wall.
    xx,yy,_=lp(x,y,u,-2.0,0,a);facade_box(m,x,y,u,.355-1.0,2.97,ww,2.0,.05,CL,a)
    facade_box(m,x,y,u,.355-2.0,1.5,ww,.1,2.95,M['Pale'],a)
   elif b==0 and ww>3.3:
    # The recessed entrance.
    facade_box(m,x,y,u,.355-1.2,1.65,ww-.2,.1,3.3,GLAZE,a);facade_box(m,x,y,u,.355-1.15,1.2,1.6,.06,2.3,M['Frame'],a)
    facade_box(m,x,y,u,.355-.6,3.28,ww,1.2,.05,CL,a)
   elif b==0 and u<S(50):
    facade_box(m,x,y,u,.18,hh/2,ww,.05,hh,M['Shutter'],a)
    for k in range(1,12):facade_box(m,x,y,u,.21,k*hh/12,ww,.02,.02,M['Frame'],a)
   elif b==0:shopfront38(m,x,y,u,b,ww,hh,a,M['Frame'],2)
   else:shopfront38(m,x,y,u,b,ww,hh,a,M['Frame'],3)
  for u,b,ww,hh,r in up:win38(m,x,y,u,b,ww,hh,a,WH)
  for u,b,ww,hh,r in cw:
   facade_box(m,x,y,u,.30,b+hh/2,ww,.03,hh,GLAZE,a)
   n=max(1,round(ww/2.3))
   for k in range(n+1):facade_box(m,x,y,u-ww/2+k*ww/n,.36,b+hh/2,.07,.10,hh,M['Frame'],a)
   for zz in (b,b+hh):facade_box(m,x,y,u,.36,zz,ww,.10,.07,M['Frame'],a)
  # Bands: the pale horizontal band between the storeys, the vertical bands, the corner piers, the
  # mosaic pier, the stone cornice of the ground floor and the parapet.
  facade_box(m,x,y,S(20.25),.38,6.60,40.5,.05,.26,M['Pale'],a)
  for s in (5.97,17.23,22.59,27.95,33.31):facade_box(m,x,y,S(s),.38,(3.46+HB)/2,.28,.05,HB-3.46,M['Pale'],a)
  for s0,s1 in ((0,.40),(11.35,11.55),(14.0,14.2),(40.4,40.6)):facade_box(m,x,y,S((s0+s1)/2),.39,(3.46+HB)/2,s1-s0,.07,HB-3.46,M['Pale'],a)
  facade_box(m,x,y,S(46.15),.42,HB/2,2.19,.14,HB,M['Mosaic'],a)
  facade_box(m,x,y,S(20.25),.43,3.40,40.5,.16,.12,CL,a)
  facade_box(m,x,y,0,.42,10.33,L,.14,.54,M['Pale'],a);facade_box(m,x,y,0,.45,HB-.02,L+.06,.20,.06,M['Frame'],a)
  plinth36(m,x,y,L,a,[(u-ww/2-.05,u+ww/2+.05) for u,b,ww,hh,r in gf if b<.35],.33,CL)
  for s in (27.69,6.0):town_rod(m,lp(x,y,S(s),.47,.30,a),lp(x,y,S(s),.47,HB-.3,a),.05,M['Frame'],8)
 elif olands38(w):
  # The yellow corner along Ölandsgatan: the same storeys, stone-clad shop windows below.
  S=lambda s:-L/2+s                                                  # s from the street corner (south)
  AX=[1.3+1.26*k for k in range(19) if 1.3+1.26*k<L-1.0]
  up=[(S(s),b,.84,t-b,0) for s in AX for b,t in ((4.61,6.11),(7.70,9.14))]
  gf=[(S(s),.66,2.3,2.33,0) for s in (5.2,8.4,11.6,14.8,18.0,21.2) if s<L-1.5]
  bz_wall(m,w['p'],w['q'],0,3.46,gf,CL);bz_wall(m,w['p'],w['q'],3.46,HB,up,M['Ochre'])
  for u,b,ww,hh,r in gf:shopfront38(m,x,y,u,b,ww,hh,a,M['Frame'],3)
  for u,b,ww,hh,r in up:win38(m,x,y,u,b,ww,hh,a,WH)
  facade_box(m,x,y,0,.38,6.70,L,.05,.24,M['Pale'],a);facade_box(m,x,y,0,.43,3.40,L,.16,.12,CL,a)
  facade_box(m,x,y,0,.42,10.33,L,.14,.54,M['Pale'],a);facade_box(m,x,y,0,.45,HB-.02,L+.06,.20,.06,M['Frame'],a)
  plinth36(m,x,y,L,a,[],.33,CL)
flat38(m,'bar',M['RoofDark'],.20);flat38(m,'barr',M['RoofDark'],.20)
b38_finish(m,'92379310')

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
# The cameras keep their measured distance from the modelled facade: the north facades stand 0.355 m
# proud of the OSM line, so the cameras move 0.355 m south.
block38_cameras=[
 sv_camera('219_Block38_Cal_No27',-93.04,-74.475,2.25,332,5),
 sv_camera('220_Block38_Cal_No27_Roof',-93.04,-74.475,2.25,332,30),
 sv_camera('221_Block38_Cal_Barometern',-72.81,-74.425,2.25,332,5),
 sv_camera('222_Block38_Cal_Barometern_Roof',-72.81,-74.425,2.25,332,30),
 sv_camera('223_Block38_Cal_Barometern_Corner',-47.26,-74.815,2.25,332,5),
 ('224_Block38_Aerial',(-60.0,-95.0,36.0),(-72.0,-55.0,6.0),28),
]
print('BLOCK38_GEOMETRY',len(block38_names))
