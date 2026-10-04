"""Pass 87: the north side of the east end of Södra Långgatan:
- no. 63 (91928581): a pale green rendered three-storey house with stone-grey window surrounds and a
  lesene, and a two-storey west bay with a boxed cornice;
- no. 67 (91928560): a three-storey front on a grey grooved ground floor, a cream west part with an
  arched gateway and a two-storey bay up to the eaves, a pink east part with its own bay, a garage
  door and a rear wing;
- no. 69 (91928553): an ochre roughcast front with smooth lesenes, dark red frames, arched middle
  windows and a dark stone plinth, under a low hipped roof;
- 91928566: an ochre roughcast house with a gambrel gable to the street, a round gable window and
  dark red frames, with the iron gates under small canopies on both sides.

References: Google Street View 2025 (four panoramas on Södra Långgatan, two resected on house
corners), view only. Zones: source/block87.json; see references/block87-notes.md.
"""
B87D=json.loads((R/'source/block87.json').read_text());Z=B87D['zones']
block87_names=[];B87={}
for old in [k for k in list(materials) if k.startswith('M_Block87_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Green','TownIvory',(.69,.75,.64),.88,0),('Surround','TownStone',(.84,.83,.79),.85,0),('Cream','TownIvory',(.87,.84,.74),.88,0),
 ('Pink','TownIvory',(.88,.76,.74),.88,0),('GreyBase','TownStone',(.56,.56,.53),.88,0),('Groove','TownMetalGrey',(.36,.36,.35),.80,0),
 ('Ochre','TownIvory',(.78,.60,.33),.95,0),('OchreSmooth','TownIvory',(.84,.68,.40),.85,0),('StonePlinth','TownStone',(.31,.30,.29),.90,0),
 ('Plinth','TownStone',(.66,.65,.62),.90,0),('White','TownPaintWhite',(.94,.94,.92),.55,0),('Red','TownPaintBrown',(.40,.13,.11),.60,0),
 ('GarageWhite','TownPaintWhite',(.88,.88,.86),.60,0),('Sheet','TownMetalGrey',(.30,.31,.32),.55,.30),('Tile','TownTileRed',(.55,.30,.22),.80,0),
 ('CanopyGreen','TownPaintGreen',(.18,.28,.24),.60,0),('Chimney','TownTileRed',(.50,.32,.26),.85,0),('Iron','TownMetalGrey',(.07,.07,.075),.45,.40),
 ('Dark','TownMetalGrey',(.05,.055,.06),.40,.20),
 ]:
 name='M_Block87_'+key;B87[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block87_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B87

def b87_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block87_names.append(name);return Mesh(name,category)
def b87_finish(m,osm):
 obj=s21_finish(m);obj['detail_pass']=87;obj['reference_notes']='references/block87-notes.md';obj['osm_way']=osm;return obj

FR87={k:(tuple(v[0]),tuple(v[1])) for k,v in B87D['fronts'].items()}
def frame87(a,b):L=math.dist(a,b);d=((b[0]-a[0])/L,(b[1]-a[1])/L);return d,(-d[1],d[0])
def S87(F,X,Y):d,_=frame87(*F);return (X-F[0][0])*d[0]+(Y-F[0][1])*d[1]
def P87(F,s,t=0,z=None):
 d,n=frame87(*F);p=(F[0][0]+d[0]*s+n[0]*t,F[0][1]+d[1]*s+n[1]*t);return p if z is None else (*p,z)
def rect87(zone,F):
 # The zone's outline boxed in its street frame: (s0, s1, t0, t1).
 d,n=frame87(*F);pts=[v for g in Z[zone]['polygons'] for v in g]
 ss=[(v[0]-F[0][0])*d[0]+(v[1]-F[0][1])*d[1] for v in pts];ts=[(v[0]-F[0][0])*n[0]+(v[1]-F[0][1])*n[1] for v in pts]
 return min(ss),max(ss),min(ts),max(ts)
def ring87(F,s0,s1,t0,t1):
 r=[P87(F,s0,t0),P87(F,s1,t0),P87(F,s1,t1),P87(F,s0,t1)]
 area=sum(r[i][0]*r[(i+1)%4][1]-r[(i+1)%4][0]*r[i][1] for i in range(4));return r if area>0 else r[::-1]

# Openings per house, in the street frame: s along the front from its west corner (m), bottom,
# width, height; kinds: win (casement), arch (round-headed, last value the rise), gate (arched
# passage), garage, port (round, centre height, radius). From the resected panoramas; see notes.
def W87(s,b,w,h,kind='win',r=0):return (kind,s,b,w,h,r)
OPS={'581':[W87(2.05,1.55,1.4,1.5),W87(2.05,4.15,1.4,1.45)]+[W87(s,b,1.4,h) for s in (5.6,9.2,12.8) for b,h in ((1.55,1.5),(4.15,1.45),(6.5,1.3))],
 '560':[W87(1.5,0,2.3,2.3,'gate',.6),W87(4.8,1.65,1.5,1.3),W87(8.7,1.65,.95,1.3),W87(12.5,1.65,1.6,1.3),W87(16.7,1.65,1.3,1.3),W87(21.2,0,2.8,2.6,'garage')]
  +[W87(s,b,w,h) for s,w in ((1.0,1.1),(8.7,.95),(12.5,1.6),(20.6,.9)) for b,h in ((4.4,1.4),(6.95,1.35))],
 '553':[W87(s,b,w,h,k,r) for s in (2.5,6.75) for b,w,h,k,r in ((1.95,1.25,1.2,'win',0),(3.7,1.2,.75,'arch',.42),(6.65,1.0,.8,'win',0))],
 '566':[W87(s,b,1.2,h) for s in (2.0,5.3,7.9) for b,h in ((1.65,1.4),(4.3,1.45))]}
HOUSE={'gw':'581','gm':'581','cr':'560','pk':'560','rw':'560','oc':'553','ob':'553','gb':'566'}
FRONT={'581':FR87['gm'],'560':FR87['cr'],'553':FR87['oc'],'566':FR87['gb']}
# Wall bands (z0, z1, material) per zone; frames and surrounds per house.
BANDS={'gw':[(0,9,'Green')],'gm':[(0,9,'Green')],'cr':[(0,3.1,'GreyBase'),(3.1,20,'Cream')],'pk':[(0,3.1,'GreyBase'),(3.1,20,'Pink')],
 'rw':[(0,20,'Pink')],'oc':[(0,20,'Ochre')],'ob':[(0,20,'Ochre')],'gb':[(0,20,'Ochre')]}
STYLE={'581':dict(frame='White',trim='Surround',plinth=(.92,'Plinth')),'560':dict(frame='White',trim='Surround',plinth=(.60,'Plinth')),
 '553':dict(frame='Red',trim='OchreSmooth',plinth=(.75,'StonePlinth')),'566':dict(frame='Red',trim='OchreSmooth',plinth=(.80,'Plinth'))}

def win87(m,x,y,u,b,w,h,a,frame,trim,rows=None):
 cas81(m,x,y,u,b,w,h,a,M[frame],.16,rows or (2 if h<1.0 else 3));surround36(m,x,y,u,b,w,h,a,M[trim],.14,.40)
 facade_box(m,x,y,u,.47,b-.05,w+.34,.16,.06,M[trim],a)
def arch87(m,x,y,u,b,w,h,r,a,frame,trim):
 cas81(m,x,y,u,b,w,h,a,M[frame],.16,2);k=16;zc=b+h
 fan=[lp(x,y,u,.13,zc,a)]+[lp(x,y,u+w/2*math.cos(math.pi*i/k),.13,zc+r*math.sin(math.pi*i/k),a) for i in range(k+1)]
 m.faces(fan,[tuple(range(len(fan))),tuple(range(len(fan)-1,-1,-1))],GLAZE)
 town_path(m,[lp(x,y,u+(w/2-.04)*math.cos(math.pi*i/k),.16,zc+(r-.04)*math.sin(math.pi*i/k),a) for i in range(k+1)],.045,M[frame])
 town_path(m,[lp(x,y,u+(w/2+.07)*math.cos(math.pi*i/k),.40,zc+(r+.07)*math.sin(math.pi*i/k),a) for i in range(k+1)],.08,M[trim])
 for s in (-1,1):facade_box(m,x,y,u+s*(w/2+.07),.40,b+h/2,.14,.06,h,M[trim],a)
 facade_box(m,x,y,u,.47,b-.05,w+.34,.16,.06,M[trim],a)
def grooves87(m,x,y,u0,u1,a,z0,z1,holes,step=.30):
 # Horizontal rustication grooves on the grey ground floor, broken at the openings.
 z=z0+step
 while z<z1-.05:
  cuts=sorted((hu-hw/2-.15,hu+hw/2+.15) for hu,hb,hw,hh,hr in holes if hb-.1<z<hb+hh+hr+.1);at=u0
  for lo,hi in cuts+[(u1,u1)]:
   lo=max(u0,min(u1,lo))
   if lo>at+.05:facade_box(m,x,y,(at+lo)/2,.37,z,lo-at,.03,.035,M['Groove'],a)
   at=max(at,min(u1,hi))
  z+=step
def lesene87(m,F,s,w,z0,z1,ma,o=.40):
 x,y,L,a=sf_edge(*F);facade_box(m,x,y,s-L/2,o,(z0+z1)/2,w,.10,z1-z0,M[ma],a)
def slab87(m,x,y,a,outline,ma,o0=.005,o1=.355):
 # A wall prism with a polygonal outline (u, z) in a wall's frame (gables).
 n=len(outline);vs=[lp(x,y,u,o,z,a) for o in (o0,o1) for u,z in outline]
 m.faces(vs,[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],ma)
def bay87(m,F,s0,s1,dep,z0,z1,ma,frame,trim,wins,lid):
 # A box bay on the front: front and side walls with windows, a soffit and a lid.
 x,y,L,a=sf_edge(*F);u0,u1=s0-L/2,s1-L/2;o=.355
 bz_wall(m,P87(F,s0),P87(F,s1),z0,z1,[((s0+s1)/2-(s0+s1)/2,b,w,h,0) for b,w,h in wins],M[ma],o+dep-.20,o+dep)
 for b,w,h in wins:
  cas81(m,x,y,(u0+u1)/2,b,w,h,a,M[frame],o+dep-.18,3);facade_box(m,x,y,(u0+u1)/2,o+dep+.06,b-.05,w+.2,.14,.06,M[trim],a)
 for uu,sg in ((u0,1),(u1,-1)):
  facade_box(m,x,y,uu+sg*.10,o+dep/2,(z0+z1)/2,.20,dep,z1-z0,M[ma],a)
  for b,w,h in wins:facade_box(m,x,y,uu+sg*.10,o+dep/2+.05,b+h/2,.22,min(.45,dep-.3),h,GLAZE,a)
 facade_box(m,x,y,(u0+u1)/2,o+dep/2,z0+.10,u1-u0,dep,.20,M[ma],a)
 facade_box(m,x,y,(u0+u1)/2,o+dep/2+.03,z1+.06,u1-u0+.14,dep+.10,.12,M[lid],a)
 for zz in (z0+.25,):facade_box(m,x,y,(u0+u1)/2,o+dep+.03,zz,u1-u0+.04,.06,.10,M[trim],a)

meshes={}
for zone,spec in Z.items():
 nm=spec['mesh']
 if nm not in meshes:meshes[nm]=b87_new(nm,'Kvarnholmen/Sodra Langgatan')
def band_mat(zone,z):return next(M[k] for z0,z1,k in BANDS[zone] if z0<=z<z1)
for zone,spec in Z.items():
 m=meshes[spec['mesh']];H=spec['height'];hs=HOUSE[zone];F=FRONT[hs];st=STYLE[hs];wm=band_mat(zone,H-.1)
 for w in walls(zone):
  if w['kind']!='outer':bz_wall(m,w['p'],w['q'],w['z0'],H,[],wm);continue
  x,y,L,a=sf_edge(w['p'],w['q']);ox,oy=outward(w)
  if oy>-.9:
   if zone in ('gb',) and abs(ox)<.3:plain(m,w,H,wm,M['Red'],M['OchreSmooth'],2,1.6);continue
   plain(m,w,H,wm,M[st['frame']] if st['frame']!='White' else M['White'],M[st['trim']],2 if H<7 else 3,1.0);continue
  # The street front: this wall's s range on the house front, and the openings inside it.
  sa,sb=S87(F,*w['p']),S87(F,*w['q']);s0,s1=min(sa,sb),max(sa,sb);sm=(s0+s1)/2
  mine=[o for o in OPS[hs] if s0+.05<=o[1]-o[3]/2 and o[1]+o[3]/2<=s1-.05]
  holes=[(o[1]-sm,o[2],o[3],o[4],o[5] if o[0] in ('arch','gate') else 0) for o in mine if o[2]<H]
  fx,fy,FL,fa=sf_edge(*F)
  for z0,z1,k in BANDS[zone]:
   if z0<H:bz_wall(m,w['p'],w['q'],z0,min(z1,H),holes,M[k])
  if zone in ('cr','pk'):grooves87(m,fx,fy,s0-FL/2,s1-FL/2,fa,st['plinth'][0],3.0,[(o[1]-FL/2,*o[2:]) for o in mine])
  for kind,s,b,ww,hh,r in mine:
   u=s-FL/2
   if b>=H:continue
   if kind=='win':win87(m,fx,fy,u,b,ww,hh,fa,st['frame'],st['trim'])
   elif kind=='arch':arch87(m,fx,fy,u,b,ww,hh,r,fa,st['frame'],st['trim'])
   elif kind=='gate':
    # The arched gateway: a dark passage behind an iron gate.
    facade_box(m,fx,fy,u,-1.2,(hh+r)/2,ww,.05,hh+r,M['Dark'],fa)
    for sg in (-1,1):facade_box(m,fx,fy,u+sg*ww/2,-.6,(hh+r)/2,.04,1.2,hh+r,M['GreyBase'],fa)
    n=int(ww/.12)
    for k in range(n+1):
     uu=u-ww/2+.06+k*(ww-.12)/n;top=b+hh+r*math.sqrt(max(0,1-((uu-u)/(ww/2))**2))-.05
     facade_box(m,fx,fy,uu,.15,top/2,.025,.025,top,M['Iron'],fa)
    for zz in (.15,1.1,2.0):facade_box(m,fx,fy,u,.15,zz,ww,.03,.05,M['Iron'],fa)
    town_path(m,[lp(fx,fy,u+(ww/2+.06)*math.cos(math.pi*i/16),.38,b+hh+(r+.06)*math.sin(math.pi*i/16),fa) for i in range(17)],.07,M['Cream'])
   elif kind=='garage':
    facade_box(m,fx,fy,u,.12,hh/2,ww,.06,hh,M['GarageWhite'],fa)
    for k in range(1,int(ww/.35)):facade_box(m,fx,fy,u-ww/2+k*ww/int(ww/.35),.16,hh/2,.03,.03,hh-.1,M['White'],fa)
    surround36(m,fx,fy,u,b,ww,hh,fa,M['Surround'],.12,.40)
  # Plinth band (broken at the ground-level openings) and the eaves cornice.
  ph,pm=st['plinth'];at=s0
  for lo,hi in sorted((o[1]-o[3]/2,o[1]+o[3]/2) for o in mine if o[2]<.1)+[(s1,s1)]:
   if lo>at+.03:facade_box(m,fx,fy,(at+lo)/2-FL/2,.40,ph/2,lo-at,.10,ph,M[pm],fa)
   at=max(at,hi)
  if zone!='gb':
   cm=M['White'] if hs in ('581','560') else M['OchreSmooth']
   if zone=='gw':facade_box(m,fx,fy,sm-FL/2,.75,H+.40,s1-s0+.6,.80,.80,M['Surround'],fa);facade_box(m,fx,fy,sm-FL/2,1.12,H+.84,s1-s0+.7,.10,.10,M['Sheet'],fa)
   else:
    facade_box(m,fx,fy,sm-FL/2,.46,H-.18,s1-s0+.1,.22,.36,cm,fa);facade_box(m,fx,fy,sm-FL/2,.60,H-.02,s1-s0+.3,.50,.10,cm,fa)
    town_rod(m,lp(fx,fy,s0-FL/2-.1,.92,H+.02,fa),lp(fx,fy,s1-FL/2+.1,.92,H+.02,fa),.07,M['Sheet'],8)

# Lesenes, bands and bays.
m=meshes['SM_Kvarnholmen_House_91928581'];F=FRONT['581']
lesene87(m,F,3.72,.34,.92,8.8,'Surround')
m=meshes['SM_Kvarnholmen_House_91928560'];F=FRONT['560']
lesene87(m,F,6.9,.30,3.1,9.4,'Cream');lesene87(m,F,14.35,.30,3.1,9.4,'Pink')
x,y,L,a=sf_edge(*F);facade_box(m,x,y,0,.42,3.12,L,.14,.18,M['Cream'],a)
for s in (2.83,):facade_box(m,x,y,s-L/2,.40,1.45,.36,.10,2.9,M['Cream'],a)
bay87(m,F,3.15,6.15,.80,3.25,9.2,'Cream','White','Surround',[(4.55,2.2,1.45),(7.0,2.2,1.35)],'Sheet')
bay87(m,F,15.0,18.4,.80,3.20,8.9,'Pink','White','Surround',[(4.40,2.2,1.45),(6.95,2.2,1.35)],'Sheet')
m=meshes['SM_Kvarnholmen_House_91928553'];F=FRONT['553']
for s,w in ((.27,.54),(4.55,.80),(8.84,.54)):lesene87(m,F,s,w,.75,8.8,'OchreSmooth',.38)
x,y,L,a=sf_edge(*F);facade_box(m,x,y,0,.38,8.55,L,.10,.50,M['OchreSmooth'],a)

# Roofs.
def saddle87(m,F,s0,s1,t0,t1,H,T,ma,wall,ov=.55,verge=.30,ends=(True,True)):
 # Saddle roof with its ridge along the street front, over the box s0..s1, t0..t1 (outline), eaves
 # from the wall faces (0.355 outside the outline) pushed out by the overhang; gable prisms.
 o=.355;tm=(t0+t1)/2;half=tm-t0+o;sl=(T-H)/half
 for ta,sg in ((t0-o,-1),(t1+o,1)):
  e=ta+sg*ov;ze=H-ov*sl
  m.faces([P87(F,s0-o-verge,e,ze),P87(F,s1+o+verge,e,ze),P87(F,s1+o+verge,tm,T),P87(F,s0-o-verge,tm,T)],[(0,1,2,3),(3,2,1,0)],ma)
  town_rod(m,P87(F,s0-o-verge,e,ze-.04),P87(F,s1+o+verge,e,ze-.04),.07,M['Sheet'],8)
 for s,e in ((s0,ends[0]),(s1,ends[1])):
  if e:m.faces([P87(F,s-o/2,t0-o,H),P87(F,s-o/2,t1+o,H),P87(F,s-o/2,tm,T)],[(0,1,2),(2,1,0)],wall)
 return sl
F=FRONT['581'];m=meshes['SM_Kvarnholmen_House_91928581']
s0,s1,t0,t1=rect87('gw',F);saddle87(m,F,s0,s1,t0,t1,Z['gw']['height'],Z['gw']['top'],M['Sheet'],M['Green'],ov=.2,verge=.1)
s0,s1,t0,t1=rect87('gm',F);saddle87(m,F,s0,s1,t0,t1,Z['gm']['height'],Z['gm']['top'],M['Sheet'],M['Green'])
F=FRONT['560'];m=meshes['SM_Kvarnholmen_House_91928560']
a0,a1,b0,b1=rect87('cr',F);c0,c1,d0,d1=rect87('pk',F)
saddle87(m,F,a0,c1,min(b0,d0),13.5,9.4,Z['cr']['top'],M['Sheet'],M['Cream'])
# The rear wing: a low hipped roof over its outline boxed in its own frame.
RW=((234.742,-50.964),(234.618,-59.197));s0,s1,t0,t1=rect87('rw',RW)
r=ring87(RW,s0,s1,t0,t1);inset_roof(m,r,Z['rw']['height'],min(s1-s0,abs(t1-t0))/2-.30,Z['rw']['top']-Z['rw']['height'],M['Sheet'],.40)
F=FRONT['553'];m=meshes['SM_Kvarnholmen_House_91928553']
s0,s1,t0,t1=rect87('oc',F);r=ring87(F,s0,s1,t0,t1);inset_roof(m,r,Z['oc']['height'],min(s1-s0,t1-t0)/2-.30,Z['oc']['top']-Z['oc']['height'],M['Sheet'],.55)
for g in Z['ob']['polygons']:m.faces([(*v,Z['ob']['height']+.02) for v in g],[tuple(range(len(g))),tuple(range(len(g)-1,-1,-1))],M['Sheet'])
# The gambrel house: the profile across the street front (wall face to wall face), the ridge
# running back from the street; gable prisms front and rear carry the attic windows.
F=FRONT['566'];m=meshes['SM_Kvarnholmen_House_91928566']
s0,s1,t0,t1=rect87('gb',F);H=Z['gb']['height'];T=Z['gb']['top'];o=.355;KN=8.8;KW=1.0
sL,sR=s0-o,s1+o;sm=(sL+sR)/2
prof=[(sL-.25,H-.50),(sL,H),(sL+KW,KN),(sm,T),(sR-KW,KN),(sR,H),(sR+.25,H-.50)]
for (p0,z0),(p1,z1) in zip(prof,prof[1:]):
 m.faces([P87(F,p0,t0-o-.30,z0+.12),P87(F,p1,t0-o-.30,z1+.12),P87(F,p1,t1+o+.30,z1+.12),P87(F,p0,t1+o+.30,z0+.12)],[(0,1,2,3),(3,2,1,0)],M['Tile'])
 town_path(m,[P87(F,p0,t0-o-.32,z0+.10),P87(F,p1,t0-o-.32,z1+.10)],.07,M['White'])
for e in (0,-1):town_rod(m,P87(F,prof[e][0],t0-o-.3,prof[e][1]+.05),P87(F,prof[e][0],t1+o+.3,prof[e][1]+.05),.07,M['Sheet'],8)
for w in walls('gb'):
 x,y,L,a=sf_edge(w['p'],w['q']);ox,oy=outward(w)
 if abs(ox)>.3:continue
 g=[(-L/2-o,H),(L/2+o,H),(L/2+o-KW,KN),(0,T),(-L/2-o+KW,KN)];slab87(m,x,y,a,g,M['Ochre'])
x,y,L,a=sf_edge(*F)
for s in (3.1,6.6):
 u=s-L/2;b,ww,hh=7.05,1.1,1.3;facade_box(m,x,y,u,.36,b+hh/2,ww,.02,hh,GLAZE,a);cas81(m,x,y,u,b,ww,hh,a,M['Red'],.40,2)
 surround36(m,x,y,u,b,ww,hh,a,M['OchreSmooth'],.14,.40);facade_box(m,x,y,u,.47,b-.05,ww+.34,.16,.06,M['OchreSmooth'],a)
porthole82(m,x,y,4.82-L/2,9.65,.36,a,M['White'])
facade_box(m,x,y,0,.42,H-.05,L+.7,.14,.20,M['OchreSmooth'],a)
for s,t in ((3.9,5.0),(3.9,7.6)):
 X,Y=P87(F,s,t);box(m,X,Y,.55,.55,1.6,T-1.0,M['Chimney'],0,M['Dark'])
# The iron gates on both sides of the gable house, under small green canopies.
for ga,gb_,ref in (((248.652,-72.999),(252.403,-71.739),'west'),((262.037,-71.65),(263.9,-72.1),'east')):
 x,y,L,a=sf_edge(ga,gb_)
 for sg in (-1,1):facade_box(m,x,y,sg*(L/2-.08),.10,1.1,.12,.12,2.2,M['Iron'],a)
 n=int(L/.13)
 for k in range(1,n):facade_box(m,x,y,-L/2+k*L/n,.10,1.05,.025,.025,2.0,M['Iron'],a)
 for zz in (.12,1.0,2.05):facade_box(m,x,y,0,.10,zz,L,.04,.05,M['Iron'],a)
 facade_box(m,x,y,0,.40,2.75,L+.1,.75,.10,M['CanopyGreen'],a)
for nm in meshes:b87_finish(meshes[nm],nm.split('_')[-1])

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block87_cameras=[
 sv_camera('426_Block87_Cal_Green',204.1,-76.0,2.40,332,10,90),
 sv_camera('427_Block87_Cal_SixtySeven',223.6,-76.85,2.40,332,10,90),
 sv_camera('428_Block87_Cal_Ochre',245.85,-78.56,2.40,332,25,90),
 sv_camera('429_Block87_Cal_Gable',256.28,-77.67,2.40,332,25,90),
 ('430_Block87_Aerial',(232.0,-95.0,55.0),(232.0,-64.0,5.0),28),
]
print('BLOCK87_GEOMETRY',len(block87_names))
