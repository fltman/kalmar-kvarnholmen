"""Pass 44: the district volume 92412862 at Västra Sjögatan and Ölandsgatan, south of pass 39.

- The stone corner house (17th century), white roughcast between fluted pilasters, on a grey
  plinth. On Ölandsgatan five axes: tall casements in flat surrounds on both storeys, the sandstone
  portal with its round-arched opening, pilasters, an entablature and a crest with finials over the
  third axis; basement grilles; a moulded cornice; a tile roof with two eyebrow dormers and two
  chimneys; a stepped gable to the east. To Västra Sjögatan three axes under a curved baroque gable
  with three small windows and a blind panel, a bronze relief between the ground-floor windows.
- The white roughcast house 2 Västra Sjögatan: a plain ground floor with a small window, the
  panelled door in a stone surround on three steps and three windows; a band; four upper windows in
  a smooth upper storey; the cornice and a tile roof.
- The yellow wooden house on Ölandsgatan: vertical boarding between white corner boards and
  pilasters, two windows with white shutters and the red door; a tile roof hipped all round with a
  segmental dormer.
- The grey board gate between them, and the courtyard wings (plain, estimated).

References: Google Street View April 2025 (four panoramas, chained per street), view only. Zones:
source/block44.json; see references/block44-notes.md. The relief's subject, the street signs and the
portal's inscription are omitted.
"""
B44D=json.loads((R/'source/block44.json').read_text());Z=B44D['zones']
block44_names=[];B44={}
for old in [k for k in list(materials) if k.startswith('M_Block44_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Rough','TownIvory',(.88,.86,.82),.95,0),
 ('White','TownIvory',(.94,.94,.91),.82,0),
 ('Smooth','TownIvory',(.92,.91,.88),.88,0),
 ('Sandstone','TownStone',(.66,.52,.40),.86,0),
 ('Plinth','TownStone',(.60,.60,.58),.84,0),
 ('Frame','TownPaintBrown',(.12,.12,.12),.55,0),
 ('Door','TownPaintBrown',(.40,.33,.24),.60,0),
 ('Yellow','TownPaintBrown',(.92,.80,.54),.70,0),
 ('RedDoor','TownPaintBrown',(.70,.20,.16),.55,0),
 ('GreyBoard','TownPaintBrown',(.62,.64,.66),.70,0),
 ('Tile','TownTileRed',(.64,.32,.22),.80,0),
 ('Bronze','TownMetalGrey',(.20,.22,.18),.45,.60),
 ('Iron','TownMetalGrey',(.05,.05,.055),.45,.40),
 ('Dark','TownMetalGrey',(.05,.055,.06),.40,.20),
 ]:
 name='M_Block44_'+key;B44[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block44_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B44;RO,WH=M['Rough'],M['White']

def b44_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block44_names.append(name);return Mesh(name,category)
def b44_finish(m,osm):
 obj=s21_finish(m);obj['detail_pass']=44;obj['reference_notes']='references/block44-notes.md';obj['osm_way']=osm;return obj
def kind44(w):
 ox,oy=outward(w)
 if w['kind']!='outer':return None
 if oy<-.9 and min(w['p'][1],w['q'][1])<-140.5:return 'olands'
 if ox<-.9 and min(w['p'][0],w['q'][0])<-28.5:return 'vsj'
 if ox>.9 and abs(w['p'][0]+12.65)<.2:return 'east'
 return None
def cas44(m,x,y,u,b,w,h,a,frame=None,trans=.72,o=.16):
 # Dark casement: two leaves, a transom, glazing bars (the corner house's windows).
 frame=frame or M['Frame']
 facade_box(m,x,y,u,o-.04,b+h/2,w,.02,h,GLAZE,a)
 for q in (-w/2+.04,w/2-.04):facade_box(m,x,y,u+q,o,b+h/2,.08,.08,h,frame,a)
 for zz in (b+.04,b+h-.04,b+h*trans):facade_box(m,x,y,u,o,zz,w,.08,.07,frame,a)
 facade_box(m,x,y,u,o+.01,b+h/2,.07,.08,h,frame,a)
 facade_box(m,x,y,u,o+.01,b+h*trans/2,w,.05,.03,frame,a)
 facade_box(m,x,y,u,.40,b-.03,w+.10,.20,.04,M['Dark'],a)
def pil44(m,x,y,u,w,z0,z1,a):
 # A fluted pilaster: a flat shaft with four flutes, a base and a small capital.
 facade_box(m,x,y,u,.42,(z0+z1)/2,w,.12,z1-z0,WH,a)
 for k in range(4):facade_box(m,x,y,u-w/2+(k+.5)*w/4,.49,(z0+z1)/2,.04,.02,z1-z0-.4,M['Smooth'],a)
 facade_box(m,x,y,u,.46,z0+.20,w+.10,.20,.40,WH,a);facade_box(m,x,y,u,.47,z1-.10,w+.12,.22,.20,WH,a)
def cornice44(m,x,y,L,a,H,ma=None,ext=0):
 ma=ma or WH;facade_box(m,x,y,0,.42,H-.62,L+ext,.14,.16,ma,a);facade_box(m,x,y,0,.50,H-.40,L+ext,.30,.28,ma,a)
 facade_box(m,x,y,0,.60,H-.12,L+ext,.50,.24,ma,a)
def gable_wall44(m,p,q,base,apex,holes,ma,steps=0,curved=False):
 # The gable wall above the cornice: a pentagon prism from base to the apex along the wall line, with
 # a stepped or curved (baroque) outline approximated by shoulders.
 x,y,L,a=sf_edge(p,q)
 if curved:
  # Baroque outline: straight shoulders, then concave curves drawing in to a narrow top section
  # (about a sixth of the width) under a small segmental cap.
  H_=apex-base;half=[(-L/2,base),(-L/2,base+.45)]
  for i in range(1,11):
   t=i/10;hw=L/2*(1-.80*t**.8);half.append((-hw,base+.45+(H_*.86-.45)*t+.18*math.sin(t*math.pi*3)))
  top=half[-1]
  cap=[(top[0]*math.cos(math.pi/2*j/6),top[1]+(apex-top[1])*math.sin(math.pi/2*j/6)) for j in range(1,7)]
  prof=half+cap[:-1]+[(0,apex)]+[(-uu,zz) for uu,zz in reversed(cap[:-1])]+[(-uu,zz) for uu,zz in reversed(half)]
 else:
  n=max(1,steps);half=[(-L/2,base)]
  for k in range(n):
   u=-L/2+(L/2-.5)*k/n;zt=base+(apex-base)*(k+1)/(n+1)
   half+=[(u,zt),(-L/2+(L/2-.5)*(k+1)/n,zt)]
  prof=half+[(-.5,apex),(.5,apex)]+[(-uu,zz) for uu,zz in reversed(half)]
 vs=[lp(x,y,uu,o,zz,a) for o in (.005,.355) for uu,zz in prof];nn=len(prof)
 m.faces(vs,[tuple(range(nn-1,-1,-1)),tuple(range(nn,2*nn))]+[(i,(i+1)%nn,(i+1)%nn+nn,i+nn) for i in range(nn)],ma)
 town_path(m,[lp(x,y,uu,.40,zz+.06,a) for uu,zz in prof[1:-1]],.07,WH)
 for u,b,w,h,r in holes:
  facade_box(m,x,y,u,.38,b+h/2,w+.20,.04,h+.20,WH,a);cas44(m,x,y,u,b,w,h,a,None,.99,.42)

m=b44_new('SM_Kvarnholmen_House_92412862','Kvarnholmen/Ölandsgatan')
CH=Z['ch']['height']
for zone in Z:
 HZ=Z[zone]['height']
 for w in walls(zone):
  k=kind44(w);x,y,L,a=sf_edge(w['p'],w['q'])
  if zone=='ch' and k=='olands':
   S=lambda X:U(w,X,-141.1)
   AX=[(-27.74,-26.10),(-24.82,-23.17),(-18.84,-17.00),(-15.94,-14.42)]
   gf=[(S((x0+x1)/2),1.90,abs(x1-x0)-.24,2.18,0) for x0,x1 in AX]
   up=[(S((x0+x1)/2),6.12,abs(x1-x0)-.24,2.14,0) for x0,x1 in AX]+[(S(-21.15),6.12,1.40,2.14,0)]
   pu=S(-21.15);portal=(pu,0,1.47,3.00,.73)
   base_g=[(S((x0+x1)/2),.12,.55,.30,0) for x0,x1 in AX]
   bz_wall(m,w['p'],w['q'],0,HZ,gf+up+[(pu,0,1.47,3.73,0)]+base_g,RO)
   for u,b,ww,hh,r in gf+up:surround36(m,x,y,u,b,ww,hh,a,WH,.12,.39);cas44(m,x,y,u,b,ww,hh,a)
   for u,b,ww,hh,r in base_g:
    facade_box(m,x,y,u,.20,b+hh/2,ww,.04,hh,M['Dark'],a)
    for j in range(4):facade_box(m,x,y,u-ww/2+(j+.5)*ww/4,.30,b+hh/2,.02,.02,hh,M['Iron'],a)
   # The sandstone portal: pilasters on pedestals, an arched opening with steps inside, the
   # entablature and a crest (the date panel) with three finials and two obelisks.
   spandrels(m,x,y,pu,0,1.47,3.00,.73,a,RO)
   p18_arch(m,*lp(x,y,pu,0,0,a)[:2],3.0,1.47,.73,.20,.42,a,M['Sandstone'],20)
   for s in (-1,1):
    facade_box(m,x,y,pu+s*1.02,.48,1.9,.40,.26,3.8,M['Sandstone'],a)
    facade_box(m,x,y,pu+s*1.02,.52,.45,.52,.34,.90,M['Sandstone'],a)
   facade_box(m,x,y,pu,.52,3.92,2.75,.34,.26,M['Sandstone'],a);facade_box(m,x,y,pu,.56,4.10,2.95,.42,.12,M['Sandstone'],a)
   facade_box(m,x,y,pu,.44,4.70,1.30,.12,1.00,M['Sandstone'],a);facade_box(m,x,y,pu,.48,4.70,1.00,.06,.70,M['Bronze'],a)
   for s in (-1,1):
    town_rod(m,lp(x,y,pu+s*1.05,.50,4.16,a),lp(x,y,pu+s*1.05,.50,5.2,a),.07,M['Sandstone'],8)
    town_rod(m,lp(x,y,pu+s*.55,.48,5.2,a),lp(x,y,pu+s*.55,.48,5.55,a),.08,M['Sandstone'],8)
   town_rod(m,lp(x,y,pu,.48,5.2,a),lp(x,y,pu,.48,5.8,a),.10,M['Sandstone'],8)
   facade_box(m,x,y,pu,-.40,1.5,1.47,1.40,.06,M['Plinth'],a)
   for j in range(4):facade_box(m,x,y,pu,-.10-j*.28,.09+j*.18,1.40,.28,.18+j*.18,M['Plinth'],a)
   facade_box(m,x,y,pu,-1.40,1.9,1.47,.06,3.4,M['Door'],a)
   pil44(m,x,y,S(-28.95),.70,.52,CH-.62,a)
   plinth36(m,x,y,L,a,[(pu-.9,pu+.9)],.52,M['Plinth'])
   cornice44(m,x,y,L,a,CH,WH,.30)
   facade_box(m,x,y,S(-12.9),.40,(0.52+CH)/2,.40,.10,CH-.52,M['Plinth'],a)
  elif zone=='ch' and k=='vsj':
   S=lambda Y:U(w,-29.2,Y)
   AX=[(-130.18,-131.88),(-133.93,-135.54),(-137.53,-139.36)]
   gf=[(S((y0+y1)/2),2.10,abs(y1-y0)-.24,2.10,0) for y0,y1 in AX]
   up=[(S((y0+y1)/2),6.28,abs(y1-y0)-.24,2.14,0) for y0,y1 in AX]
   base_g=[(S((y0+y1)/2),.12,.55,.30,0) for y0,y1 in AX]
   bz_wall(m,w['p'],w['q'],0,HZ,gf+up+base_g,RO)
   for u,b,ww,hh,r in gf+up:surround36(m,x,y,u,b,ww,hh,a,WH,.12,.39);cas44(m,x,y,u,b,ww,hh,a)
   for u,b,ww,hh,r in base_g:facade_box(m,x,y,u,.20,b+hh/2,ww,.04,hh,M['Dark'],a)
   ru=S(-132.7);facade_box(m,x,y,ru,.40,1.8,.45,.08,.62,WH,a);facade_box(m,x,y,ru,.46,1.85,.30,.06,.40,M['Bronze'],a)
   for Y0 in (-129.2,-140.55):pil44(m,x,y,S(Y0),.65,.52,CH-.62,a)
   plinth36(m,x,y,L,a,[],.52,M['Plinth'])
   cornice44(m,x,y,L,a,CH,WH,.30)
   # The curved baroque gable: three small windows, a blind panel under the top.
   gh=[(S(Y),10.20,1.00,1.10,0) for Y in (-132.9,-134.6,-136.3)]
   gable_wall44(m,w['p'],w['q'],CH-.05,17.9,gh,RO,0,True)
   facade_box(m,x,y,S(-134.6),.38,13.95,.95,.04,1.60,WH,a)
  elif zone=='ch' and k=='east':
   bz_wall(m,w['p'],w['q'],0,HZ,[(0,6.12,1.10,1.8,0),(0,2.0,1.10,1.9,0)],RO)
   x,y,L,a=sf_edge(w['p'],w['q'])
   for b,hh in ((6.12,1.8),(2.0,1.9)):surround36(m,x,y,0,b,1.10,hh,a,WH,.12,.39);cas44(m,x,y,0,b,1.10,hh,a)
   plinth36(m,x,y,L,a,[],.52,M['Plinth']);cornice44(m,x,y,L,a,CH)
   gable_wall44(m,w['p'],w['q'],CH-.05,17.9,[(0,11.2,.66,.90,0)],RO,4,False)
  elif zone=='wh' and k=='vsj':
   S=lambda Y:U(w,-29.05,Y)
   small=(S(-117.80),2.40,.54,.98,0)
   door=(S(-119.47),.36,1.28,3.60,0)
   gf=[(S((y0+y1)/2),2.10,abs(y1-y0)-.24,2.00,0) for y0,y1 in ((-121.71,-123.34),(-123.94,-125.54),(-126.31,-128.03))]
   up=[(S((y0+y1)/2),6.00,abs(y1-y0)-.24,2.10,0) for y0,y1 in ((-117.62,-119.23),(-120.2,-121.89),(-123.83,-125.53),(-126.21,-128.0))]
   bz_wall(m,w['p'],w['q'],0,HZ,gf+up+[small,door],RO)
   bz_wall(m,w['p'],w['q'],5.0,HZ-.3,up,M['Smooth'],.355,.375)
   for u,b,ww,hh,r in gf+up+[small]:surround36(m,x,y,u,b,ww,hh,a,WH,.12,.39);cas44(m,x,y,u,b,ww,hh,a)
   du,db,dw,dh,_=door
   surround36(m,x,y,du,db,dw,dh,a,WH,.16,.39)
   facade_box(m,x,y,du,.16,db+1.4,dw,.06,2.8,M['Door'],a)
   for j in range(3):
    for s in (-1,1):facade_box(m,x,y,du+s*dw/4,.20,db+.4+j*.8,dw/2-.2,.03,.6,M['Door'],a)
   cas44(m,x,y,du,db+2.85,dw,.75,a,M['Door'],.99,.16)
   for j in range(3):facade_box(m,x,y,du,.355+(3-j)*.15,.06*(j+1),dw+.5,(3-j)*.30,.12*(j+1),M['Plinth'],a)
   facade_box(m,x,y,0,.42,5.0,L,.10,.12,WH,a)
   plinth36(m,x,y,L,a,[(du-dw/2-.2,du+dw/2+.2)],.60,M['Plinth'])
   cornice44(m,x,y,L,a,HZ,WH)
  elif zone=='yh' and k=='olands':
   S=lambda X:U(w,X,-141.4)
   wins=[(S(-7.40),1.30,.95,1.50,0),(S(0.55),1.30,.95,1.50,0)]
   door=(S(-2.45),.55,.72,2.30,0)
   bz_wall(m,w['p'],w['q'],0,HZ,wins+[door],M['Yellow'])
   boards35(m,x,y,L,a,.55,HZ-.35,wins+[door],M['Yellow'])
   for u,b,ww,hh,r in wins:
    surround36(m,x,y,u,b,ww,hh,a,WH,.10,.39);cas44(m,x,y,u,b,ww,hh,a,WH,.72,.20)
    for s in (-1,1):facade_box(m,x,y,u+s*(ww/2+.36),.40,b+hh/2,.60,.05,hh+.10,WH,a)
   du,db,dw,dh,_=door
   surround36(m,x,y,du,db,dw,dh,a,WH,.10,.39);facade_box(m,x,y,du,.20,db+(dh-.4)/2,dw,.06,dh-.4,M['RedDoor'],a)
   for j in range(8):facade_box(m,x,y,du,.24,db+.1+j*(dh-.5)/8,dw,.02,.02,M['Dark'],a)
   cas44(m,x,y,du,db+dh-.38,dw,.34,a,WH,.99,.20)
   for u0 in (-8.9,-5.4,-4.15,.0,2.2):facade_box(m,x,y,S(u0),.42,(.55+HZ)/2,.18,.08,HZ-.55,WH if abs(u0)>2 or u0==0 else M['Yellow'],a)
   facade_box(m,x,y,0,.40,.28,L,.08,.55,M['Plinth'],a)
   eaves37(m,x,y,L,a,HZ,WH,.45)
  else:
   if w['kind']=='outer':plain(m,w,HZ,M['Yellow'] if zone=='yh' else RO,M['Frame'],WH,1 if zone=='yh' else 2,.9)
   else:bz_wall(m,w['p'],w['q'],w['z0'],HZ,[],M['Yellow'] if zone=='yh' else RO)
sl=roof34(m,'ch',M['Tile'],RO)
roof34(m,'wh',M['Tile'],RO)
sy=roof34(m,'yh',M['Tile'],M['Yellow'])
for g in Z['bk']['polygons']:
 pts=simplify([tuple(v) for v in g],.8)
 inset_roof(m,pts,Z['bk']['height'],2.0,2.4,M['Tile'],.35)
# Dormers and chimneys on the corner house; the yellow house's dormer.
for w in walls('ch'):
 if kind44(w)=='olands':
  x,y,L,a=sf_edge(w['p'],w['q'])
  for X in (-23.6,-20.5):roof_dormer(m,x,y,U(w,X,-141.1),a,CH,sl,1.2,.70,.45,M['Tile'],M['Tile'],M['Frame'],True)
for cx,cy in ((-28.3,-133.2),(-21.6,-133.2)):box(m,cx,cy,.70,.90,1.4,17.0,RO,0,M['Dark'])
for w in walls('yh'):
 if kind44(w)=='olands':
  x,y,L,a=sf_edge(w['p'],w['q']);roof_dormer(m,x,y,U(w,-3.45,-141.4),a,Z['yh']['height'],sy,.5,.80,.70,M['RedDoor'],M['Tile'],WH,True)
box(m,-5.2,-137.0,.55,.55,1.0,6.6,M['Dark'],0,M['Dark'])
# The grey board gate between the corner house and the yellow house.
gp,gq=(-12.66,-141.3),(-9.0,-141.3);gx,gy,gL,ga=sf_edge(gp,gq)
facade_box(m,gx,gy,0,0,1.6,gL,.08,3.2,M['GreyBoard'],ga)
for j in range(1,18):facade_box(m,gx,gy,-gL/2+j*gL/18,.05,1.6,.02,.02,3.1,M['Dark'],ga)
facade_box(m,gx,gy,0,.05,3.25,gL+.2,.14,.12,M['GreyBoard'],ga)
b44_finish(m,'92412862')

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
# Chained camera positions (distances from the real facades; 0.355 m added for the model's walls).
block44_cameras=[
 sv_camera('268_Block44_Cal_Olands',-27.99,-141.1-.355-7.70,2.36,332,5,90),
 sv_camera('269_Block44_Cal_Olands_Up',-27.99,-141.1-.355-7.70,2.36,332,30,90),
 sv_camera('270_Block44_Cal_Yellow',-7.81,-141.1-.355-9.20,2.51,332,5,90),
 sv_camera('271_Block44_Cal_White',-29.15-.355-6.43,-123.81,2.51,62,5,90),
 sv_camera('272_Block44_Cal_Gable',-29.15-.355-6.36,-138.35,2.51,62,5,90),
 sv_camera('273_Block44_Cal_Gable_Up',-29.15-.355-6.36,-138.35,2.51,62,30,90),
 ('274_Block44_Aerial',(-45.0,-160.0,30.0),(-15.0,-130.0,5.0),28),
]
print('BLOCK44_GEOMETRY',len(block44_names))
