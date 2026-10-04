"""Pass 86: the west side of the Proviantgatan row on eastern Kvarnholmen, from south to north:
- Proviantgatan 6, a pale vertical-boarded house of one and a half storeys on a high stone plinth,
  with a recessed entrance up a stone stair, three dormers, a chimney and a tiled saddle roof;
- the small pink rendered cottage with two windows under a steep tiled saddle roof, and a lower
  range behind it;
- Proviantgatan 8, a cream rendered two-storey house: a rusticated ground floor, a storey band,
  relief diamond panels under the upper windows, dark green window frames, the green-and-red double
  door, and a tiled mansard roof with two red dormers;
- Proviantgatan 10, a red vertical-boarded two-storey house with white window surrounds under a
  low hipped dark metal roof;
- Proviantgatan 12, a narrow sage-green rendered corner house of two storeys with stone quoins, a
  storey cornice, a deep main cornice and a low hipped metal roof, and a lower rear wing.

References: Google Street View (four panoramas on Proviantgatan, all resected on house corners),
view only. Zones: source/block86.json; see references/block86-notes.md. Street signs, the lamp
post, plants, the fence between nos 10 and 12 and the meter box are omitted.
"""
B86D=json.loads((R/'source/block86.json').read_text());Z=B86D['zones']
block86_names=[];B86={}
for old in [k for k in list(materials) if k.startswith('M_Block86_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Pale','TownIvory',(.88,.83,.68),.82,0),('Cream','TownIvory',(.90,.86,.77),.88,0),('CreamLight','TownIvory',(.95,.93,.87),.85,0),
 ('Pink','TownIvory',(.86,.64,.50),.90,0),('Red','TownPaintBrown',(.55,.19,.15),.75,0),('Green','TownIvory',(.68,.74,.62),.88,0),
 ('Quoin','TownIvory',(.87,.86,.80),.88,0),('White','TownPaintWhite',(.95,.95,.93),.55,0),('FrameGreen','TownPaintGreen',(.17,.27,.22),.55,0),
 ('DoorRed','TownPaintBrown',(.55,.18,.16),.60,0),('DormerRed','TownPaintBrown',(.50,.24,.20),.65,0),('Door','TownPaintBrown',(.45,.36,.28),.60,0),
 ('Tile','TownTileRed',(.78,.42,.27),.80,0),('RoofDark','TownMetalGrey',(.24,.25,.27),.55,.30),('RoofGrey','TownMetalGrey',(.46,.47,.48),.55,.30),
 ('Plinth','TownStone',(.62,.60,.57),.90,0),('PlinthDark','TownStone',(.48,.46,.43),.90,0),('Chimney','TownTileRed',(.55,.30,.24),.85,0),
 ('Iron','TownMetalGrey',(.08,.08,.085),.45,.40),('Dark','TownMetalGrey',(.05,.055,.06),.40,.20),
 ]:
 name='M_Block86_'+key;B86[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block86_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B86;WH=M['White']

def b86_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block86_names.append(name);return Mesh(name,category)
def b86_finish(m,osm):
 obj=s21_finish(m);obj['detail_pass']=86;obj['reference_notes']='references/block86-notes.md';obj['osm_way']=osm;return obj
def P86(a,b,s):L=math.dist(a,b);return (a[0]+(b[0]-a[0])/L*s,a[1]+(b[1]-a[1])/L*s)

def mansard86(m,zone,a,b,ma,wall,ov=.35):
 # Gable-ended mansard roof over the zone boxed in the frame of its front a->b: a steep lower
 # slope on each long side up to the break (inset k, rise rk), a low saddle above it, and the
 # five-sided gable walls at the ends.
 r,Ls,Lt=rect82(zone,a,b);H=Z[zone]['height'];T=Z[zone]['top'];k,rk=Z[zone]['brk']
 p0,p1,p2,p3=r;d=((p1[0]-p0[0])/Ls,(p1[1]-p0[1])/Ls);n=((p3[0]-p0[0])/Lt,(p3[1]-p0[1])/Lt)
 P=lambda s,t,z:(p0[0]+d[0]*s+n[0]*t,p0[1]+d[1]*s+n[1]*t,z)
 sl=rk/k;zb=H+rk;e=.25
 for t0,t1 in ((0,k),(Lt,Lt-k)):
  to=t0-ov if t0==0 else t0+ov
  q=[P(-e,to,H-ov*sl),P(Ls+e,to,H-ov*sl),P(Ls+e,t1,zb),P(-e,t1,zb)]
  m.faces(q,[(0,1,2,3),(3,2,1,0)],ma)
  m.faces([P(-e,t1,zb),P(Ls+e,t1,zb),P(Ls+e,Lt/2,T),P(-e,Lt/2,T)],[(0,1,2,3),(3,2,1,0)],ma)
  town_rod(m,P(-e,to,H-ov*sl-.04),P(Ls+e,to,H-ov*sl-.04),.07,WH,8)
 for s in (0,Ls):
  m.faces([P(s,0,H),P(s,k,zb),P(s,Lt/2,T),P(s,Lt-k,zb),P(s,Lt,H)],[(0,1,2,3,4),(4,3,2,1,0)],wall)
 return sl
def window86(m,x,y,u,b,w,h,a,frame,sur,rows=3,bw=.12):
 cas81(m,x,y,u,b,w,h,a,frame,.16,rows);surround36(m,x,y,u,b,w,h,a,sur,bw,.40);facade_box(m,x,y,u,.47,b-.05,w+.3,.16,.06,sur,a)
def plinth86(m,x,y,L,a,hgt,gaps,ma,o=.39):
 at=-L/2
 for lo,hi in sorted(gaps)+[(L/2,L/2)]:
  if lo>at+.03:facade_box(m,x,y,(at+lo)/2,o,hgt/2,lo-at,.08,hgt,ma,a)
  at=max(at,hi)
def recess86(m,x,y,u,b,w,h,a,leaf,lining,depth=.6):
 # A recessed doorway: the door at the back of a lined reveal.
 facade_box(m,x,y,u,.355-depth,b+h/2,w,.06,h,leaf,a)
 for s in (-1,1):facade_box(m,x,y,u+s*(w/2-.03),.355-depth/2,b+h/2,.06,depth,h,lining,a)
 facade_box(m,x,y,u,.355-depth/2,b+h-.03,w,depth,.06,lining,a);facade_box(m,x,y,u,.355-depth/2,b+.03,w,depth,.06,lining,a)
 facade_box(m,x,y,u,.11-depth+.355,b+h*.72,w-.4,.02,h*.3,GLAZE,a)

# Street fronts: (a, b) with s measured from a; openings (kind, s, bottom, width, height).
PS_A,PS_B=(186.64,-55.69),(186.14,-70.57)
PK_A,PK_B=(186.0,-47.11),(185.91,-53.34)
CR_A,CR_B=(186.16,-34.98),(186.0,-47.11)
RD_A,RD_B=(186.31,-24.4),(186.16,-34.98)
GR_A,GR_B=(186.18,-13.18),(186.11,-19.2)
FR={'ps':dict(a=PS_A,b=PS_B,wall='Pale',frame='White',sur='White',plinth=.90,pm='PlinthDark',boards=True,
  ops=[('win',2.5,1.85,1.25,1.6),('win',4.7,1.85,1.25,1.6),('recess',7.9,1.2,1.35,2.15),('win',10.9,1.85,1.25,1.6),('win',13.2,1.85,1.25,1.6)]),
 'pk':dict(a=PK_A,b=PK_B,wall='Pink',frame='White',sur='White',plinth=.60,pm='Plinth',boards=False,
  ops=[('win',2.2,1.4,1.15,1.3),('win',4.6,1.4,1.15,1.3)]),
 'cr':dict(a=CR_A,b=CR_B,wall='Cream',frame='FrameGreen',sur='CreamLight',plinth=.35,pm='Plinth',boards=False,
  ops=[('win',s,3.95,1.25,1.5) for s in (1.35,3.4,5.55,7.9,10.4)]+[('win',s,1.2,1.25,1.65) for s in (1.35,3.4,5.55,7.9)]+[('door2',10.35,.2,1.75,2.35)]
   +[('diam',s,3.62,.5,.26) for s in (1.35,3.4,5.55,7.9,10.4)]),
 'rd':dict(a=RD_A,b=RD_B,wall='Red',frame='White',sur='White',plinth=.50,pm='Plinth',boards=True,
  ops=[('win',s,b,1.3,1.5) for s in (3.4,5.75,8.1) for b in (1.2,3.8)]+[('win',1.2,3.8,1.1,1.5),('door',1.2,.5,1.0,2.1)]),
 'gr':dict(a=GR_A,b=GR_B,wall='Green',frame='White',sur='Quoin',plinth=.63,pm='PlinthDark',boards=False,
  ops=[('win',1.7,1.65,1.0,1.45),('win',4.1,1.65,1.0,1.45),('win',1.7,4.55,1.05,1.6),('win',4.1,4.55,1.05,1.6)]),
 'pr':dict(wall='Pink',frame='White',sur='White'),'gw':dict(wall='Green',frame='White',sur='Quoin')}

meshes={}
for zone,spec in Z.items():
 nm=spec['mesh']
 if nm not in meshes:meshes[nm]=b86_new(nm,'Kvarnholmen/Proviantgatan')
for zone,spec in Z.items():
 m=meshes[spec['mesh']];H=spec['height'];f=FR[zone];wm=M[f['wall']];fm=M[f['frame']];sm=M[f['sur']]
 for w in walls(zone):
  if w['kind']!='outer':bz_wall(m,w['p'],w['q'],w['z0'],H,[],wm);continue
  x,y,L,a=sf_edge(w['p'],w['q']);ox,oy=outward(w)
  if zone=='rd' and ox>-.9:
   # The red house's other walls show no openings in the panoramas (north wall seen from no. 12).
   bz_wall(m,w['p'],w['q'],0,H,[],wm);boards82(m,x,y,L,a,.52,H-.25,[],wm)
   facade_box(m,x,y,0,.46,H-.12,L+.1,.14,.24,WH,a);plinth86(m,x,y,L,a,.5,[],M['Plinth']);continue
  if 'a' not in f or ox>-.9 or L<4:
   plain(m,w,H,wm,fm,sm,2 if H>5.5 else 1,.9 if H>5.5 else .8)
   if zone=='gr':
    for uu in (-L/2+.2,L/2-.2):facade_box(m,x,y,uu,.40,H/2,.40,.10,H,M['Quoin'],a)
    facade_box(m,x,y,0,.50,H+.10,L+.3,.35,.35,M['Quoin'],a)
   continue
  wf={'p':list(f['a']),'q':list(f['b'])}
  mine=[(k,U(w,*P86(f['a'],f['b'],s)),b,ww,hh) for k,s,b,ww,hh in f['ops']]
  holes=[(u,b,ww,hh,0) for k,u,b,ww,hh in mine if k in ('win','door','door2','recess')]
  bz_wall(m,w['p'],w['q'],0,H,holes,wm)
  if f['boards']:boards82(m,x,y,L,a,f['plinth']+.02,H-.25,holes,wm)
  for k,u,b,ww,hh in mine:
   if k=='win':window86(m,x,y,u,b,ww,hh,a,fm,sm,3 if hh>1.55 else 2,.14 if zone in('ps','rd') else .12)
   elif k=='recess':recess86(m,x,y,u,b,ww,hh,a,M['Door'],M['Pale'])
   elif k=='door':
    door83(m,x,y,u,b,ww,hh,a,M['Door'],WH);steps82(m,x,y,u,ww,b,a,M['Plinth'])
   elif k=='door2':
    # The double door: red leaves in green framing, a glazed transom above.
    gate83(m,x,y,u,b,ww,1.95,a,M['DoorRed'],M['FrameGreen'])
    facade_box(m,x,y,u,.14,b+2.0+(hh-2.0)/2,ww,.02,hh-2.05,GLAZE,a);facade_box(m,x,y,u,.18,b+2.0,ww,.08,.08,M['FrameGreen'],a)
    surround36(m,x,y,u,b,ww,hh,a,M['FrameGreen'],.10,.40)
   elif k=='diam':
    # Relief panel with a diamond under each upper window.
    facade_box(m,x,y,u,.39,b,ww*2.4,.06,hh*2.0,M['CreamLight'],a)
    town_path(m,[lp(x,y,u-ww*.9,.43,b,a),lp(x,y,u,.43,b-hh*.8,a),lp(x,y,u+ww*.9,.43,b,a),lp(x,y,u,.43,b+hh*.8,a),lp(x,y,u-ww*.9,.43,b,a)],.035,M['Cream'],)
  gaps=[(u-ww/2,u+ww/2) for k,u,b,ww,hh in mine if k in ('door2',)]
  plinth86(m,x,y,L,a,f['plinth'],gaps,M[f['pm']])
  if zone=='ps':
   # The stone stair up to the recessed entrance, with an iron rail on its north side.
   ul=U(w,*P86(PS_A,PS_B,7.9));ur=U(w,*P86(PS_A,PS_B,7.9-.8))
   for k in range(6):facade_box(m,x,y,ul,.36+.22*(6-k)/2,(k+.5)*.2,1.45,.22*(6-k),.2,M['Plinth'],a)
   town_rod(m,lp(x,y,ur,.36+.22*6,.95,a),lp(x,y,ur,.6,2.15,a),.03,M['Iron'],6)
   for oo,zz in ((.36+.22*6,0),(.6,1.2)):town_rod(m,lp(x,y,ur,oo,zz,a),lp(x,y,ur,oo,zz+.95,a),.025,M['Iron'],6)
  if zone in ('ps','rd','pk'):
   for uu in (-L/2+.09,L/2-.09):facade_box(m,x,y,uu,.42,(H+f['plinth'])/2,.20,.10,H-f['plinth'],WH,a)
   facade_box(m,x,y,0,.46,H-.12 if zone!='rd' else H-.3,L+.1,.14,.24,WH,a)
   if zone!='rd':town_rod(m,lp(x,y,-L/2,.66,H-.05,a),lp(x,y,L/2,.66,H-.05,a),.06,WH,8)
  if zone=='cr':
   # Rusticated ground floor, the storey band, corner pilasters and the cornice.
   for zz in [f['plinth']+.4*i for i in range(1,8)]:
    if zz<3.2:
     cuts=sorted((u-ww/2-.14,u+ww/2+.14) for k,u,b,ww,hh in mine if k in('win','door2') and b<zz<b+hh+.1);at=-L/2
     for lo,hi in cuts+[(L/2,L/2)]:
      if lo>at+.05:facade_box(m,x,y,(at+lo)/2,.37,zz,lo-at,.03,.03,M['CreamLight'],a)
      at=max(at,hi)
   facade_box(m,x,y,0,.42,3.25,L,.14,.18,M['CreamLight'],a)
   for uu in (-L/2+.2,L/2-.2):facade_box(m,x,y,uu,.40,H/2,.40,.08,H,M['CreamLight'],a)
   facade_box(m,x,y,0,.45,H-.15,L+.1,.20,.30,M['CreamLight'],a);facade_box(m,x,y,0,.55,H+.02,L+.2,.40,.12,M['CreamLight'],a)
  if zone=='gr':
   # Stone quoins, storey cornice with panels under the upper windows, the deep main cornice.
   for uu in (-L/2+.2,L/2-.2):
    for i in range(int((H-f['plinth'])/.42)):
     zz=f['plinth']+.21+i*.42;facade_box(m,x,y,uu+(.06 if i%2 else -.06)*(1 if uu<0 else -1),.43,zz,.48 if i%2 else .36,.12,.36,M['Quoin'],a)
   facade_box(m,x,y,0,.46,3.75,L+.2,.22,.14,M['Quoin'],a);facade_box(m,x,y,0,.42,4.5,L+.1,.14,.10,M['Quoin'],a)
   for k,u,b,ww,hh in mine:
    if b>4:facade_box(m,x,y,u,.40,4.18,ww+.2,.06,.4,M['Quoin'],a)
   facade_box(m,x,y,0,.45,H-.2,L+.2,.20,.40,M['Quoin'],a);facade_box(m,x,y,0,.62,H+.12,L+.6,.55,.22,M['Quoin'],a)
# The green house's chamfered corner: quoins and cornice continue round it (handled by plain above);
# its sign is omitted.

# Roofs.
m=meshes['SM_Kvarnholmen_House_91928565']
saddle82(m,'ps',PS_A,PS_B,M['Tile'],M['Pale'])
sl_ps=(Z['ps']['top']-Z['ps']['height'])/(rect82('ps',PS_A,PS_B)[2]/2)
x,y,L,a=sf_edge(PS_A,PS_B);wf={'p':list(PS_A),'q':list(PS_B)}
for s in (2.8,8.1,13.1):dormer82(m,x,y,U(wf,*P86(PS_A,PS_B,s)),a,Z['ps']['height'],sl_ps,1.5,1.0,M['Pale'],WH,M['Tile'],.3)
_,n=frame82(PS_A,PS_B);X,Y=P86(PS_A,PS_B,11.0);chimney82(m,X+n[0]*3.6,Y+n[1]*3.6,Z['ps']['top']-1.0,Z['ps']['top']+.75,M['Chimney'])
m=meshes['SM_Kvarnholmen_House_91928576']
saddle82(m,'pk',PK_A,PK_B,M['Tile'],M['Pink'])
_,n=frame82(PK_A,PK_B);X,Y=P86(PK_A,PK_B,5.3);chimney82(m,X+n[0]*2.3,Y+n[1]*2.3,Z['pk']['top']-.8,Z['pk']['top']+.7,M['Chimney'])
saddle82(m,'pr',PK_A,PK_B,M['Tile'],M['Pink'],along=False)
m=meshes['SM_Kvarnholmen_House_91928540']
sl_cr=mansard86(m,'cr',CR_A,CR_B,M['Tile'],M['Cream'])
x,y,L,a=sf_edge(CR_A,CR_B);wf={'p':list(CR_A),'q':list(CR_B)}
for s in (3.8,8.5):dormer82(m,x,y,U(wf,*P86(CR_A,CR_B,s)),a,Z['cr']['height'],sl_cr,1.7,.75,M['DormerRed'],WH,M['Tile'],.6)
_,n=frame82(CR_A,CR_B)
for s in (2.0,10.0):X,Y=P86(CR_A,CR_B,s);chimney82(m,X+n[0]*5.1,Y+n[1]*5.1,Z['cr']['top']-.8,Z['cr']['top']+.8,M['Chimney'])
m=meshes['SM_Kvarnholmen_House_91928545']
r,Ls,Lt=rect82('rd',RD_A,RD_B);inset_roof(m,r,Z['rd']['height'],min(Ls,Lt)/2-.30,Z['rd']['top']-Z['rd']['height'],M['RoofDark'],.45)
m=meshes['SM_Kvarnholmen_House_91928582']
g=Z['gr']['polygons'][0];inset_roof(m,[tuple(v) for v in g],Z['gr']['height']+.2,3.3,Z['gr']['top']-Z['gr']['height']-.2,M['RoofGrey'],.55)
_,n=frame82(GR_A,GR_B);X,Y=P86(GR_A,GR_B,3.0);chimney82(m,X+n[0]*5.0,Y+n[1]*5.0,Z['gr']['top']-.6,Z['gr']['top']+.9,M['Chimney'])
for gg in Z['gw']['polygons']:
 m.faces([(*v,Z['gw']['top']) for v in gg],[tuple(range(len(gg))),tuple(range(len(gg)-1,-1,-1))],M['RoofGrey'])
 for p,q in zip(gg,gg[1:]+gg[:1]):town_rod(m,(*p,Z['gw']['top']),(*q,Z['gw']['top']),.05,M['RoofGrey'],6)
for w in walls('gw'):bz_wall(m,w['p'],w['q'],Z['gw']['height'],Z['gw']['top'],[],M['Green'])
for nm in meshes:b86_finish(meshes[nm],nm.split('_')[-1])

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block86_cameras=[
 sv_camera('421_Block86_Cal_Six',181.8,-66.85,2.30,62,10,90),
 sv_camera('422_Block86_Cal_Eight',181.43,-46.99,2.30,62,10,90),
 sv_camera('423_Block86_Cal_Ten',181.7,-36.2,2.30,62,10,90),
 sv_camera('424_Block86_Cal_Twelve',181.5,-16.63,2.30,62,10,90),
 ('425_Block86_Aerial',(165.0,-40.0,30.0),(192.0,-40.0,2.0),28),
]
print('BLOCK86_GEOMETRY',len(block86_names))
