"""Pass 88: five houses in the south-west of Kvarnholmen, on Ölandsgatan, Södra Vallgatan and
Larmgatan:
- Ölandsgatan 7 (92379283): a pale green boarded two-storey house on a stone plinth, with white
  corner boards and a central lesene, an arched carriage gate in a white portal, seven casements, a
  red tile saddle roof with a central dormer and a flue pipe;
- Södra Vallgatan 15 (92379259): a white boarded two-storey house on a high stone plinth, with a
  central entrance bay between two broad lesenes (steps up to a recessed double door, a balcony door
  with a French balcony above), eight casements, a saddle roof with an arched dormer and two brick
  chimneys, and a low rear wing;
- 91856598: the small brown boarded building (a carriage door under a band window, a green door) and
  the yellow boarded house east of it, under a hipped tile roof with a red gabled dormer;
- 91856586: the white functionalist house: a granite-clad ground floor with shop windows and a blue
  door with a round light, red-framed windows, a projecting bay and a round window on the taller west
  part, a set-back top floor and a glazed roof-terrace railing on the east part, a grey awning;
- 91856600 on Larmgatan: the low green boarded pavilion under a dark hipped roof (door, round window,
  small window, chimney stack), the glazed café under a dark fascia, and the white-framed
  conservatory at its south end.

References: Google Street View April 2025 (five panoramas, four of them resected on OSM corners),
view only. Zones: source/block88.json; see references/block88-notes.md. Signs, lettering, the
house number, lamps, bicycles, the café furniture and its terrace railing are omitted.
"""
B88D=json.loads((R/'source/block88.json').read_text());Z=B88D['zones']
block88_names=[];B88={}
for old in [k for k in list(materials) if k.startswith('M_Block88_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('PaleGreen','TownIvory',(.70,.77,.63),.80,0),('White','TownIvory',(.91,.91,.89),.80,0),('Yellow','TownIvory',(.91,.80,.52),.80,0),
 ('Render','TownIvory',(.93,.93,.91),.88,0),('BrownBoard','TownPaintBrown',(.36,.29,.22),.78,0),('PavGreen','TownPaintGreen',(.18,.36,.30),.70,0),
 ('WhiteFrame','TownPaintWhite',(.95,.95,.93),.55,0),('GreyGreen','TownPaintGreen',(.43,.47,.40),.60,0),('RedFrame','TownPaintBrown',(.66,.33,.24),.60,0),
 ('GreenDoor','TownPaintGreen',(.20,.42,.30),.60,0),('Olive','TownPaintBrown',(.42,.40,.30),.65,0),('BlueDoor','TownPaintWhite',(.36,.52,.74),.60,0),
 ('Ochre','TownPaintWhite',(.82,.62,.30),.60,0),('Teak','TownPaintBrown',(.55,.33,.20),.60,0),
 ('Stone','TownStone',(.70,.67,.63),.90,0),('Granite','TownStone',(.62,.60,.57),.88,0),
 ('Tile','TownTileRed',(.76,.38,.25),.80,0),('TileDark','TownTileRed',(.25,.24,.24),.80,0),('Brick','TownTileRed',(.58,.36,.30),.85,0),
 ('Metal','TownMetalGrey',(.55,.56,.57),.45,.40),('Awning','TownPaintWhite',(.70,.71,.72),.75,0),('Iron','TownMetalGrey',(.08,.08,.085),.45,.40),
 ('Dark','TownMetalGrey',(.05,.055,.06),.40,.20),
 ]:
 name='M_Block88_'+key;B88[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block88_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B88

def b88_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block88_names.append(name);return Mesh(name,category)
def b88_finish(m,osm):
 obj=s21_finish(m);obj['detail_pass']=88;obj['reference_notes']='references/block88-notes.md';obj['osm_way']=osm;return obj
def front88(a,b):
 # Unit along the front a->b, and its point at s metres.
 L=math.dist(a,b);d=((b[0]-a[0])/L,(b[1]-a[1])/L);return d,(lambda s:(a[0]+d[0]*s,a[1]+d[1]*s))
def on88(w,a,b):
 # Is the wall on the front line a-b? Returns the s of its middle along the front, or None.
 d,_=front88(a,b);n=(-d[1],d[0])
 off=[abs((p[0]-a[0])*n[0]+(p[1]-a[1])*n[1]) for p in (w['p'],w['q'])]
 if max(off)>.3:return None
 return sum((p[0]-a[0])*d[0]+(p[1]-a[1])*d[1] for p in (w['p'],w['q']))/2
def gdormer88(m,x,y,u,a,H,slope,w,h,body,frame,roof,back=.9,rise=.8):
 # A dormer with a gabled (front) roof: dormer82's box with a saddle lid and a front gable.
 zb=H+(back+.40-.355+.05)*slope-.15;zt=zb+h+.55;dep=2.4;o=.355-back
 box(m,*lp(x,y,u,o-dep/2,0,a)[:2],w,dep,zt-zb,zb,body,a)
 m.faces([lp(x,y,u-w/2,o,zt,a),lp(x,y,u+w/2,o,zt,a),lp(x,y,u,o,zt+rise,a)],[(0,1,2),(2,1,0)],body)
 for s in (-1,1):
  e=w/2+.18;m.faces([lp(x,y,u+s*e,o+.2,zt-.12,a),lp(x,y,u,o+.2,zt+rise+.05,a),lp(x,y,u,o-dep,zt+rise+.05,a),lp(x,y,u+s*e,o-dep,zt-.12,a)],[(0,1,2,3),(3,2,1,0)],roof)
 facade_box(m,x,y,u,o+.01,zb+.30+h/2,w-.4,.02,h,GLAZE,a);cas81(m,x,y,u,zb+.30,w-.4,h,a,frame,o+.05,2)
def adormer88(m,x,y,u,a,H,slope,w,h,body,frame,roof,back=.9):
 # A dormer under a segmental (arched) roof: the box, then a curved lid of strips.
 zb=H+(back+.40-.355+.05)*slope-.15;zt=zb+h+.45;dep=2.2;o=.355-back
 box(m,*lp(x,y,u,o-dep/2,0,a)[:2],w,dep,zt-zb,zb,body,a)
 k=8;r=w/2+.12;pts=[(r*math.cos(math.pi*i/k),.35*w*math.sin(math.pi*i/k)) for i in range(k+1)]
 for (u0,z0),(u1,z1) in zip(pts,pts[1:]):
  m.faces([lp(x,y,u+u0,o+.15,zt+z0,a),lp(x,y,u+u1,o+.15,zt+z1,a),lp(x,y,u+u1,o-dep,zt+z1,a),lp(x,y,u+u0,o-dep,zt+z0,a)],[(0,1,2,3),(3,2,1,0)],roof)
 m.faces([lp(x,y,u+pu,o+.005,zt+pz,a) for pu,pz in pts],[tuple(range(k+1)),tuple(range(k,-1,-1))],body)
 facade_box(m,x,y,u,o+.01,zb+.30+h/2,w-.4,.02,h,GLAZE,a);cas81(m,x,y,u,zb+.30,w-.4,h,a,frame,o+.05,2)
def flat88(m,zone,ma,lift=.02):
 z=Z[zone]['height']+lift
 for g in Z[zone]['polygons']:m.faces([(*v,z) for v in g],[tuple(range(len(g))),tuple(range(len(g)-1,-1,-1))],ma)
def mullions88(m,x,y,u,b,w,h,a,frame,n,trans=None,o=.20,bar=.07):
 # Glazing in a frame grid: n bays, an optional transom height.
 facade_box(m,x,y,u,o-.04,b+h/2,w,.02,h,GLAZE,a)
 for k in range(n+1):facade_box(m,x,y,u-w/2+k*w/n,o,b+h/2,bar,.08,h,frame,a)
 for zz in [b+.04,b+h-.04]+([trans] if trans else []):facade_box(m,x,y,u,o,zz,w,.08,bar,frame,a)

# The fronts. Openings: (kind, s along the front from its first point, bottom, width, height[, extra]).
# Kinds: win (casement, extra = rows), door (extra = leaf material), gate, shop (extra = bays), port
# (round: s, centre height, radius). From the resected panoramas; see the notes for the estimates.
FR=B88D['fronts'];FOL,F15,FBY,FWF,FPV=[tuple(map(tuple,FR[k])) for k in ('ol','sv','by','wf','pv')]
F={'ol':dict(front=FOL,wall='PaleGreen',frame='WhiteFrame',trim='WhiteFrame',plinth=.50,pm='Stone',boards=True,surr=True,
  ops=[('gate',1.9,.05,2.0,2.85,0)]+[('win',s,4.25,1.0,1.55,3) for s in (2.3,4.4,7.4,9.7)]+[('win',s,1.95,1.0,1.40,3) for s in (4.3,7.4,9.7)]),
 'sv':dict(front=F15,wall='White',frame='GreyGreen',trim='WhiteFrame',plinth=.95,pm='Stone',boards=True,surr=True,
  ops=[('win',s,1.95,1.25,1.30,2) for s in (1.5,3.4,8.8,10.7)]+[('win',s,4.50,1.05,1.30,2) for s in (1.6,3.5,8.7,10.6)]+[('bdoor',6.15,3.75,1.15,2.05,0),('recess',6.15,.95,1.30,2.15,0)]),
 'br':dict(front=FBY,wall='BrownBoard',frame='GreenDoor',trim='BrownBoard',plinth=.10,pm='Stone',boards=True,surr=False,
  ops=[('gate',1.95,.05,1.8,2.0,0),('shop',1.95,2.30,2.3,.85,5),('gdoor',3.98,.05,.90,3.05,0)]),
 'yl':dict(front=FBY,wall='Yellow',frame='WhiteFrame',trim='WhiteFrame',plinth=.45,pm='Stone',boards=True,surr=True,
  ops=[('win',s,3.75,1.10,1.30,3) for s in (6.05,8.45,11.35,13.75)]+[('win',s,.95,1.10,1.30,3) for s in (6.05,8.45,11.35,13.75)]),
 'wt':dict(front=FWF,wall='Render',frame='RedFrame',trim='Render',plinth=0,pm='Granite',boards=False,surr=False,
  ops=[('shop',1.8,.45,2.9,2.65,4),('door',4.45,.05,1.15,3.05,'BlueDoor'),('win',1.4,4.7,1.4,1.7,2)]),
 'wr':dict(front=FWF,wall='Render',frame='RedFrame',trim='Render',plinth=0,pm='Granite',boards=False,surr=False,
  ops=[('shop',7.65,.45,2.4,2.65,2),('shop',10.9,.05,2.9,3.05,3)]+[('win',s,4.65,1.35,1.75,2) for s in (7.6,9.95,12.6)]),
 'pg':dict(front=FPV,wall='PavGreen',frame='WhiteFrame',trim='WhiteFrame',plinth=.15,pm='Granite',boards=True,surr=True,
  ops=[('win',1.85,1.6,.9,1.0,2),('door',3.9,.05,.95,2.25,'Ochre')]),
 'pc':dict(front=FPV,wall='PavGreen',frame='Dark',trim='Dark',plinth=0,pm='Granite',boards=False,surr=False,ops=[]),
 'pv':dict(front=FPV,wall='WhiteFrame',frame='WhiteFrame',trim='WhiteFrame',plinth=0,pm='Granite',boards=False,surr=False,ops=[])}
F['wb']=dict(F['wr'],ops=[]);F['sw']=dict(F['sv'],ops=[])
PORT={'wt':[(1.6,8.6,.50)],'pg':[(5.6,2.1,.62)]}

meshes={}
for zone,spec in Z.items():
 nm=spec['mesh']
 if nm not in meshes:meshes[nm]=b88_new(nm,'Kvarnholmen/Södra Vallgatan' if '9185660' not in nm else 'Kvarnholmen/Larmgatan')
for zone,spec in Z.items():
 m=meshes[spec['mesh']];H=spec['height'];f=F[zone];wm=M[f['wall']];fm=M[f['frame']];tm=M[f['trim']]
 for w in walls(zone):
  if w['kind']!='outer':bz_wall(m,w['p'],w['q'],w['z0'],H,[],wm);continue
  x,y,L,a=sf_edge(w['p'],w['q']);sm=on88(w,*f['front'])
  if zone in ('pc','pv'):
   # The café: glass between dark posts under a dark fascia; the conservatory: white frames with a
   # transom, a white fascia.
   top=H-.35;bz_wall(m,w['p'],w['q'],0,H,[(0,.30,L-.2,top-.30,0)],wm if zone=='pc' else M['WhiteFrame'])
   n=max(1,round(L/(2.0 if zone=='pc' else 1.1)))
   mullions88(m,x,y,0,.30,L-.2,top-.30,a,fm,n,None if zone=='pc' else 2.15,.25,.09 if zone=='pc' else .07)
   facade_box(m,x,y,0,.45,H-.17,L+.1,.20,.36,M['Dark'] if zone=='pc' else M['WhiteFrame'],a)
   facade_box(m,x,y,0,.40,.15,L,.10,.30,M['Granite'],a);continue
  if sm is None or not f['ops']:
   if zone in ('wt','wr','wb'):plain(m,w,H,wm,fm,M['WhiteFrame'],2,.9)
   else:plain(m,w,H,wm,M['WhiteFrame'],tm,2 if H>5 else 1,.9 if H>5 else .8)
   continue
  mine=[(o[0],o[1]-sm,*o[2:]) for o in f['ops'] if abs(o[1]-sm)+o[3]/2<=L/2+.01]
  holes=[(u,b,ww,hh,0) for k,u,b,ww,hh,*_ in mine]
  bz_wall(m,w['p'],w['q'],0,H,holes,wm)
  ports=[(s-sm,zc,r) for s,zc,r in PORT.get(zone,[]) if abs(s-sm)<L/2]
  if f['boards']:boards82(m,x,y,L,a,f['plinth']+.02,H-.10,holes+[(u,zc-r,2*r,2*r,0) for u,zc,r in ports],wm)
  for u,zc,r in ports:porthole82(m,x,y,u,zc,r,a,fm if zone!='pg' else M['WhiteFrame'])
  for k,u,b,ww,hh,ex in mine:
   if k=='win':
    cas81(m,x,y,u,b,ww,hh,a,fm,.16,ex);facade_box(m,x,y,u,.47,b-.05,ww+.24,.16,.06,M['WhiteFrame'] if f['surr'] else fm,a)
    if f['surr']:surround36(m,x,y,u,b,ww,hh,a,M['WhiteFrame'],.10,.40)
   elif k=='shop':
    mullions88(m,x,y,u,b,ww,hh,a,fm if zone!='wr' or u+sm<9 else M['Dark'],ex,b+hh*.72 if zone in ('wt','wr') else None)
    if zone=='wr' and u+sm>9:facade_box(m,x,y,u,-1.2,b+hh/2,ww,.05,hh,M['Dark'],a)
   elif k=='gate':gate83(m,x,y,u,b,ww,hh,a,M['Olive'] if zone=='ol' else M['BrownBoard'],M['WhiteFrame'] if zone=='ol' else fm)
   elif k=='gdoor':
    # The green door: a panelled leaf under a tall glazed light.
    facade_box(m,x,y,u,.12,b+1.15,ww,.07,2.3,M['GreenDoor'],a);mullions88(m,x,y,u,b+2.35,ww,hh-2.35,a,M['GreenDoor'],2,None,.16)
    surround36(m,x,y,u,b,ww,hh,a,M['GreenDoor'],.10,.40)
   elif k=='recess':
    # The entrance recess: reveals 1.0 m deep, the double door at its back, steps up to it.
    for s in (-1,1):facade_box(m,x,y,u+s*(ww/2+.02),-.32,b+hh/2,.04,1.36,hh,M['WhiteFrame'],a)
    facade_box(m,x,y,u,-.32,b+hh+.02,ww,1.36,.04,M['WhiteFrame'],a);facade_box(m,x,y,u,-1.02,b+hh/2,ww,.04,hh,M['WhiteFrame'],a)
    facade_box(m,x,y,u,-.96,b+(hh-.1)/2,ww-.35,.06,hh-.1,M['GreyGreen'],a)
    for s in (-1,1):facade_box(m,x,y,u+s*(ww-.35)/4,-.92,b+(hh-.1)*.72,(ww-.35)/2-.16,.02,(hh-.1)*.32,GLAZE,a)
    for j in range(5):
     o1=.36+.3*(4-j);facade_box(m,x,y,u,(o1-1.0)/2,(j+1)*b/10,ww+.3,o1+1.0,(j+1)*b/5,M['Stone'],a)
   elif k=='bdoor':
    cas81(m,x,y,u,b,ww,hh,a,fm,.16,3);surround36(m,x,y,u,b,ww,hh,a,M['WhiteFrame'],.10,.40)
    # The French balcony: a bowed iron basket in front of the balcony door.
    facade_box(m,x,y,u,.50,b+.02,ww+.3,.25,.05,M['Iron'],a)
    for j in range(9):facade_box(m,x,y,u-ww/2-.1+j*(ww+.2)/8,.62,b+.45,.03,.03,.9,M['Iron'],a)
    town_rod(m,lp(x,y,u-ww/2-.1,.62,b+.9,a),lp(x,y,u+ww/2+.1,.62,b+.9,a),.025,M['Iron'],6)
   else:
    door83(m,x,y,u,b,ww,min(hh,2.45),a,M[ex],fm if zone!='pg' else M['WhiteFrame'],zone=='pg')
    if hh>2.6:facade_box(m,x,y,u,.13,b+2.45+(hh-2.45)/2,ww,.05,hh-2.45,M['Teak'],a)
    if zone=='wt':porthole82(m,x,y,u,1.75,.20,a,M['WhiteFrame'])
  # Plinth (with gaps at the low doors and gates), corner boards, eaves board.
  if f['plinth']>.05:
   at=-L/2
   for lo,hi in sorted((u-ww/2,u+ww/2) for k,u,b,ww,hh,ex in mine if b<f['plinth'])+[(L/2,L/2)]:
    if lo>at+.03:facade_box(m,x,y,(at+lo)/2,.39,f['plinth']/2,lo-at,.08,f['plinth'],M[f['pm']],a)
    at=max(at,hi)
  if f['boards']:
   for uu in (-L/2+.10,L/2-.10):facade_box(m,x,y,uu,.42,(H+f['plinth'])/2,.22,.10,H-f['plinth'],tm,a)
  if Z[zone]['roof']!='flat':
   facade_box(m,x,y,0,.46,H-.12,L+.1,.14,.24,M['WhiteFrame'],a);town_rod(m,lp(x,y,-L/2,.66,H-.05,a),lp(x,y,L/2,.66,H-.05,a),.06,M['Metal'],8)
  else:
   facade_box(m,x,y,0,.42,H+(Z[zone]['top']-H)/2-.05,L+.1,.14,Z[zone]['top']-H+.1,M['Metal'] if zone=='br' else wm,a)
  # The granite-clad ground floor of the functionalist house: cladding, pilasters, the fascia band.
  if zone in ('wt','wr'):
   holes2=[(u,b,ww,hh) for k,u,b,ww,hh,ex in mine if b<3]
   at=-L/2
   for lo,hi in sorted((u-ww/2-.05,u+ww/2+.05) for u,b,ww,hh in holes2)+[(L/2,L/2)]:
    if lo>at+.03:facade_box(m,x,y,(at+lo)/2,.43,1.6,lo-at,.16,3.2,M['Granite'],a)
    at=max(at,hi)
   for u,b,ww,hh in holes2:
    if b>.2:facade_box(m,x,y,u,.43,b/2,ww+.1,.16,b,M['Granite'],a)
    if b+hh<3.15:facade_box(m,x,y,u,.43,(b+hh+3.2)/2,ww+.1,.16,3.2-b-hh,M['Granite'],a)
   facade_box(m,x,y,0,.47,3.35,L,.22,.30,M['Granite'],a)
   if zone=='wr':awning82(m,x,y,11.55-sm,3.25,3.7,a,M['Awning'],.75,1.6)

# Roofs and roof furniture.
def P88(a,b,s,t=0):d,P=front88(a,b);n=(-d[1],d[0]);p=P(s);return (p[0]+n[0]*t,p[1]+n[1]*t)
# Ölandsgatan 7: saddle roof along the street, the arched dormer, the flue pipe.
m=meshes['SM_Kvarnholmen_House_92379283']
saddle82(m,'ol',*FOL,M['Tile'],M['PaleGreen'],along=True,ov=.40)
r,Ls,Lt=rect82('ol',*FOL);sl_ol=(Z['ol']['top']-Z['ol']['height'])/(Lt/2)
x,y,L,a=sf_edge(*FOL);adormer88(m,x,y,U({'p':list(FOL[0]),'q':list(FOL[1])},*P88(*FOL,5.8)),a,Z['ol']['height'],sl_ol,1.5,1.0,M['WhiteFrame'],M['WhiteFrame'],M['Metal'])
X,Y=P88(*FOL,5.9,2.6);town_rod(m,(X,Y,Z['ol']['height']+2.2*sl_ol),(X,Y,Z['ol']['top']+1.3),.10,M['Iron'],8)
facade_box(m,x,y,U({'p':list(FOL[0]),'q':list(FOL[1])},*P88(*FOL,5.66)),.42,(Z['ol']['height']+.5)/2,.24,.10,Z['ol']['height']-.5,M['WhiteFrame'],a)
# The gate portal: white pilasters, a cornice over it, the arch drawn on the leaves.
ug=U({'p':list(FOL[0]),'q':list(FOL[1])},*P88(*FOL,1.9))
for s in (-1,1):facade_box(m,x,y,ug+s*1.2,.45,1.9,.30,.14,3.8,M['WhiteFrame'],a)
facade_box(m,x,y,ug,.50,3.95,2.9,.30,.22,M['WhiteFrame'],a)
k=12;town_path(m,[lp(x,y,ug+1.0*math.cos(math.pi*i/k),.30,1.85+1.0*math.sin(math.pi*i/k),a) for i in range(k+1)],.07,M['WhiteFrame'])
for s in (-1,1):facade_box(m,x,y,ug+s*.80,.24,2.62,.40,.10,.46,M['WhiteFrame'],a)
# Södra Vallgatan 15: the entrance bay's lesenes, the saddle roof, the arched dormer and the chimneys.
m=meshes['SM_Kvarnholmen_House_92379259']
x,y,L,a=sf_edge(*F15);Uf=lambda s:U({'p':list(F15[0]),'q':list(F15[1])},*P88(*F15,s))
for s0,s1 in ((4.6,5.45),(6.85,7.65)):facade_box(m,x,y,Uf((s0+s1)/2),.48,(Z['sv']['height']+.95)/2,s1-s0,.26,Z['sv']['height']-.95,M['WhiteFrame'],a)
saddle82(m,'sv',*F15,M['Tile'],M['White'],along=True,ov=.40)
r,Ls,Lt=rect82('sv',*F15);sl_sv=(Z['sv']['top']-Z['sv']['height'])/(Lt/2)
adormer88(m,x,y,Uf(6.15),a,Z['sv']['height'],sl_sv,1.4,.95,M['WhiteFrame'],M['GreyGreen'],M['Tile'])
for s in (2.9,9.1):
 X,Y=P88(*F15,s,1.4);box(m,X,Y,1.1,.55,2.9,7.0,M['Brick'],math.atan2(F15[1][1]-F15[0][1],F15[1][0]-F15[0][0]),M['WhiteFrame'])
flat88(m,'sw',M['Metal'])
# 91856598: the brown building's flat roof, the yellow house's hipped roof and its gabled dormer.
m=meshes['SM_Kvarnholmen_House_91856598']
flat88(m,'br',M['Metal'])
r,sl_yl=hip82(m,'yl',*FBY,M['Tile'])
x,y,L,a=sf_edge(*FBY);gdormer88(m,x,y,U({'p':list(FBY[0]),'q':list(FBY[1])},*P88(*FBY,10.9)),a,Z['yl']['height'],sl_yl,2.0,1.0,M['RedFrame'],M['WhiteFrame'],M['RedFrame'])
# 91856586: flat roofs; the bay on the west part; the set-back top floor and the terrace railing on
# the east part.
m=meshes['SM_Kvarnholmen_House_91856586']
for zone in ('wt','wr','wb'):flat88(m,zone,M['Dark'])
x,y,L,a=sf_edge(*FWF);Uw=lambda s:U({'p':list(FWF[0]),'q':list(FWF[1])},*P88(*FWF,s))
# The bay, 0.8 m out from the wall: its faces measured on the wall plane and brought forward to its
# own plane (heights and widths scaled about the camera).
ub=Uw(4.6);bw=2.95;bo=.80
facade_box(m,x,y,ub,.355+bo/2,(3.3+4.82)/2,bw,bo,1.52,M['Render'],a)
facade_box(m,x,y,ub,.355+bo/2,(6.6+8.0)/2,bw,bo,1.4,M['Render'],a)
facade_box(m,x,y,ub,.355+bo/2,9.95,bw,bo,.3,M['Render'],a)
for z0,z1 in ((4.82,6.6),(8.0,9.8)):
 for s in (-1,1):facade_box(m,x,y,ub+s*(bw/2-.06),.355+bo/2,(z0+z1)/2,.12,bo,z1-z0,M['Render'],a)
 mullions88(m,x,y,ub,z0,bw-.2,z1-z0,a,M['RedFrame'],4,None,.355+bo-.08)
uh=Uw(8.7);dep=6.0;sb=.6
box(m,*lp(x,y,uh,.355-sb-dep/2,0,a)[:2],4.6,dep,2.4,Z['wr']['height'],M['Render'],a)
mullions88(m,x,y,uh,8.25,4.2,1.0,a,M['RedFrame'],5,None,.355-sb+.04)
box(m,*lp(x,y,uh,.355-sb-dep/2+.3,0,a)[:2],5.0,dep+.6,.18,Z['wr']['height']+2.4,M['Render'],a)
ut=Uw(12.25)
facade_box(m,x,y,ut,.30,Z['wr']['height']+.6,2.5,.02,1.1,GLAZE,a)
for zz in (Z['wr']['height']+.08,Z['wr']['height']+.6,Z['wr']['height']+1.18):facade_box(m,x,y,ut,.30,zz,2.5,.06,.05,M['Metal'],a)
for j in range(4):facade_box(m,x,y,ut-1.25+j*2.5/3,.30,Z['wr']['height']+.6,.05,.06,1.2,M['Metal'],a)
# The Larmgatan pavilion: the hipped roof and the chimney stack; flat roofs on the café and the
# conservatory.
m=meshes['SM_Kvarnholmen_House_91856600']
r,sl_pg=hip82(m,'pg',*FPV,M['TileDark'])
X,Y=P88(*FPV,2.6,3.0);chimney82(m,X,Y,Z['pg']['top']-.6,Z['pg']['top']+1.0,M['Dark'])
flat88(m,'pc',M['Dark']);flat88(m,'pv',M['Metal'])
for nm in meshes:b88_finish(meshes[nm],nm.split('_')[-1])

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block88_cameras=[
 sv_camera('431_Block88_Cal_Olandsgatan7',-110.79,-146.93,2.20,333,15,90),
 sv_camera('432_Block88_Cal_SodraVallgatan15',-149.33,-175.77,2.30,332,15,90),
 sv_camera('433_Block88_Cal_BrownYellow',-253.0,-176.21,2.30,332,20,90),
 sv_camera('434_Block88_Cal_Pavilion',-293.36,-204.07,2.30,62,15,90),
 ('435_Block88_Aerial',(-200.0,-215.0,45.0),(-190.0,-160.0,2.0),24),
]
print('BLOCK88_GEOMETRY',len(block88_names))
