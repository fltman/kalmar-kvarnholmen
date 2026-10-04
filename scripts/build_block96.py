"""Pass 96: the east side of north Proviantgatan (fronts face west) and the south side of
Fiskaregatan east of it (fronts face north):
- 90859877: the red boarded house with its gable to Proviantgatan, darker red corner and bay
  boards, three windows in the gable and two (plus one estimated) below, a tiled saddle roof and
  a chimney;
- 90859878: the small white boarded cottage with its gable to the street and one window in a
  green frame reaching into the gable; the gateway with the green double gate between white
  posts fills the 3.5 m gap to the red house;
- 90859832: the grey rendered two-storey house on a brown base, four window columns (narrow,
  double, double, narrow) in white surrounds with brown joinery, a low black hipped roof; its
  south side is rendered white with three tall windows on each floor;
- 90859848: the ochre rendered two-storey house on the same brown base: the west wing on
  Proviantgatan with two window columns and two peaked dormers, a white gable above the grey
  house's roof; the long north range on Fiskaregatan under a tiled saddle roof, hipped at the
  corner (seen only at its east end; its windows are estimated);
- 90859847: the long white stucco house on Fiskaregatan: a rusticated ground floor with eight
  round-arched windows and the red arched double door in the middle, nine windows above, pilaster
  strips, a heavy cornice, two baroque gables over the side bays with two arched windows each,
  three red dormers and a red-brown sheet roof; the small yard annex in its south-west notch.

References: Google Street View (three panoramas on Proviantgatan at heading 62-63, one on
Fiskaregatan at heading 150, all pitch 15, resected on house corners), view only. Zones:
source/block96.json; see references/block96-notes.md. Signs, the parking sign, lamp posts, the
bushes and the electricity cabinets are omitted.
"""
B96D=json.loads((R/'source/block96.json').read_text());Z=B96D['zones']
block96_names=[];B96={}
for old in [k for k in list(materials) if k.startswith('M_Block96_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('RedBoard','TownPaintBrown',(.56,.19,.16),.80,0),('RedTrim','TownPaintBrown',(.44,.13,.11),.75,0),('WhiteBoard','TownPaintWhite',(.92,.92,.89),.70,0),
 ('WhiteFrame','TownPaintWhite',(.95,.95,.93),.55,0),('GreenFrame','TownPaintGreen',(.22,.45,.30),.60,0),('GateGreen','TownPaintGreen',(.42,.56,.44),.60,0),
 ('Grey','TownIvory',(.74,.74,.72),.90,0),('SideWhite','TownIvory',(.92,.91,.87),.90,0),('Ochre','TownIvory',(.72,.62,.44),.90,0),
 ('BrownBase','TownStone',(.42,.29,.22),.90,0),('Joinery','TownPaintBrown',(.30,.14,.11),.60,0),('DormerBrown','TownPaintBrown',(.33,.24,.19),.70,0),
 ('Stucco','TownIvory',(.91,.91,.89),.88,0),('Rustic','TownIvory',(.84,.85,.85),.90,0),('StuccoTrim','TownPaintWhite',(.96,.96,.94),.60,0),
 ('RedJoinery','TownPaintBrown',(.50,.17,.14),.60,0),('DoorRed','TownPaintBrown',(.55,.14,.14),.55,0),('DormerRed','TownPaintBrown',(.55,.20,.17),.60,0),
 ('Stone','TownStone',(.48,.48,.47),.92,0),('Plinth','TownStone',(.62,.62,.60),.90,0),('Tile','TownTileRed',(.72,.38,.26),.80,0),
 ('TileDark','TownTileRed',(.58,.30,.22),.80,0),('Sheet','TownMetalGrey',(.13,.13,.14),.50,.30),('SheetRed','TownMetalGrey',(.42,.20,.16),.55,.25),
 ('Chimney','TownTileRed',(.60,.35,.27),.85,0),('Iron','TownMetalGrey',(.08,.08,.085),.45,.40),('Dark','TownMetalGrey',(.05,.055,.06),.40,.20),
 ]:
 name='M_Block96_'+key;B96[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block96_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B96;WF=M['WhiteFrame']

def b96_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block96_names.append(name);return Mesh(name,category)
def drop_degenerate_faces96(obj,tol=1e-9):
 import bmesh
 bm=bmesh.new();bm.from_mesh(obj.data)
 def _thin(f):
  L=max(e.calc_length() for e in f.edges);return L>0 and 2*f.calc_area()/L<1e-4
 bad=[f for f in bm.faces if f.calc_area()<tol or len({v.index for v in f.verts})<len(f.verts) or _thin(f)]
 block96_samples[obj.name]=[tuple(round(c,2) for c in f.calc_center_median()) for f in bad[:4]]
 if bad:bmesh.ops.delete(bm,geom=bad,context='FACES_ONLY')
 bm.to_mesh(obj.data);bm.free();obj.data.update();return len(bad)
block96_dropped={};block96_samples={}
def b96_finish(m,osm):
 obj=s21_finish(m);block96_dropped[obj.name]=drop_degenerate_faces96(obj)
 obj['detail_pass']=96;obj['reference_notes']='references/block96-notes.md';obj['osm_way']=osm;return obj

# Frames. A frame is (origin, along, inwards): s along a street front, t inwards (left of the
# front's direction), so the OSM line is t = 0 and the facade surface t = -0.355.
FO96=.355
def frame96(a,b):
 L=math.dist(a,b);d=((b[0]-a[0])/L,(b[1]-a[1])/L);return (tuple(a),d,(-d[1],d[0]))
def P96(F,s,t,z=None):
 o,d,n=F;p=(o[0]+d[0]*s+n[0]*t,o[1]+d[1]*s+n[1]*t);return p if z is None else (*p,z)
def bb96(zone,F):
 o,d,n=F;pts=[v for g in Z[zone]['polygons'] for v in g]
 ss=[(v[0]-o[0])*d[0]+(v[1]-o[1])*d[1] for v in pts];ts=[(v[0]-o[0])*n[0]+(v[1]-o[1])*n[1] for v in pts]
 return min(ss),max(ss),min(ts),max(ts)
# The street walls (OSM line, direction with the building on the left) the roofs are boxed in.
FR96={'rd':((188.702,88.831),(188.637,83.22)),'co':((189.247,98.391),(188.778,92.378)),'gr':((188.816,119.401),(188.73,103.81)),
 'ow':((189.156,129.109),(188.816,119.401)),'on':((242.74,132.171),(199.57,132.513)),'wm':((270.17,131.711),(242.74,132.171))}
def roof96(m,F,r,c,H,T,roof,wall,along=True,ov=.40,verge=.30,ends=('gable','gable'),gable_ma=None):
 # Saddle roof over the box r=(r0,r1) along the ridge, c=(c0,c1) across it, in frame F (along:
 # the ridge runs along s; otherwise along t). Ends: 'gable' (a wall prism and a verge), 'hip'
 # (a hipped end at the roof's own slope) or 'none' (cut square at the box's end, for junctions).
 Q=(lambda a,b,z:P96(F,a,b,z)) if along else (lambda a,b,z:P96(F,b,a,z))
 r0,r1=r;c0,c1=c;o=FO96;cm=(c0+c1)/2;half=(c1-c0)/2+o;sl=(T-H)/half;ze=H-ov*sl
 ea,eb=c0-o-ov,c1+o+ov
 E=[];K=[]
 for rr,end,sg in ((r0,ends[0],-1),(r1,ends[1],1)):
  if end=='gable':E.append(rr+sg*(o+verge));K.append(rr+sg*(o+verge))
  elif end=='hip':E.append(rr+sg*(o+ov));K.append(rr+sg*(o+ov)-sg*(half+ov))
  else:E.append(rr);K.append(rr)
 for e,sg in ((ea,1),(eb,-1)):
  m.faces([Q(E[0],e,ze),Q(E[1],e,ze),Q(K[1],cm,T),Q(K[0],cm,T)],[(0,1,2,3),(3,2,1,0)],roof)
  town_rod(m,Q(E[0]+(.05 if ends[0]!='none' else 0),e,ze-.05),Q(E[1]-(.05 if ends[1]!='none' else 0),e,ze-.05),.065,M['Iron'] if roof==M['Sheet'] else WF,8)
 for i,(rr,end,sg) in enumerate(((r0,ends[0],-1),(r1,ends[1],1))):
  if end=='hip':m.faces([Q(E[i],ea,ze),Q(E[i],eb,ze),Q(K[i],cm,T)],[(0,1,2),(2,1,0)],roof)
  if end=='gable':
   f=rr+sg*o;g=[(c0-o,H),(c1+o,H),(cm,T-.02)];vs=[Q(f-sg*k,cc,zz) for k in (0,.30) for cc,zz in g]
   m.faces(vs,[(0,1,2),(5,4,3),(0,3,4,1),(1,4,5,2),(2,5,3,0)],gable_ma or wall)
 return sl,cm
def slab96(m,x,y,u,b,w,h,a,frame,trim,rows=2):
 # A window standing on a gable prism's face (0.355 out): glass, casement and surround proud.
 facade_box(m,x,y,u,.365,b+h/2,w,.02,h,GLAZE,a);cas81(m,x,y,u,b,w,h,a,frame,.40,rows)
 surround36(m,x,y,u,b,w,h,a,trim,.10,.42);facade_box(m,x,y,u,.50,b-.05,w+.24,.16,.06,trim,a)
def win96(m,x,y,u,b,w,h,a,frame,trim,rows=2,bw=.12):
 cas81(m,x,y,u,b,w,h,a,frame,.16,rows);surround36(m,x,y,u,b,w,h,a,trim,bw,.40)
 facade_box(m,x,y,u,.47,b-.05,w+.24,.16,.06,trim,a)
def arch96(m,x,y,u,b,w,h,a,frame,trim,o=.16):
 # Round-arched window (the rectangle b..b+h and a half-round head), frame and archivolt; o is
 # the frame's offset from the OSM line (0.16 in a wall opening, more on a gable's face).
 to=.40 if o<.3 else o+.03
 cas81(m,x,y,u,b,w,h,a,frame,o,2);r=w/2;k=12
 m.faces([lp(x,y,u+r*math.cos(math.pi*i/k),o-.04,b+h+r*math.sin(math.pi*i/k),a) for i in range(k+1)],[tuple(range(k+1)),tuple(range(k,-1,-1))],GLAZE)
 town_path(m,[lp(x,y,u+(r-.04)*math.cos(math.pi*i/k),o,b+h+(r-.04)*math.sin(math.pi*i/k),a) for i in range(k+1)],.04,frame)
 town_path(m,[lp(x,y,u+(r+.08)*math.cos(math.pi*i/k),to,b+h+(r+.08)*math.sin(math.pi*i/k),a) for i in range(k+1)],.07,trim)
 for s in (-1,1):facade_box(m,x,y,u+s*(r+.08),to,b+h/2,.14,.06,h,trim,a)
 facade_box(m,x,y,u,to+.07,b-.05,w+.24,.16,.06,trim,a)
def dormer96(m,x,y,u,a,H,slope,w,h,body,frame,roof,back=.8,dep=2.4):
 # A peaked dormer on a slope: box body, window, a small saddle roof across the slope with a
 # gable to the street.
 of=.355-back;zb=H+(back+.40-.355+.05)*slope-.20;zt=zb+h+.50;zr=zt+w*.45
 box(m,*lp(x,y,u,of-dep/2,0,a)[:2],w,dep,zt-zb,zb,body,a)
 facade_box(m,x,y,u,of+.01,zb+.28+h/2,w-.40,.02,h,GLAZE,a);cas81(m,x,y,u,zb+.28,w-.40,h,a,frame,of+.05,2)
 surround36(m,x,y,u,zb+.28,w-.40,h,a,frame,.06,of+.06)
 for s in (-1,1):
  m.faces([lp(x,y,u+s*(w/2+.12),of+.15,zt-.08,a),lp(x,y,u,of+.15,zr,a),lp(x,y,u,of-dep,zr,a),lp(x,y,u+s*(w/2+.12),of-dep,zt-.08,a)],[(0,1,2,3),(3,2,1,0)],roof)
 vs=[lp(x,y,u+uu,oo,zz,a) for oo in (of,of-.20) for uu,zz in ((-w/2,zt),(w/2,zt),(0,zr-.03))]
 m.faces(vs,[(0,1,2),(5,4,3),(0,3,4,1),(1,4,5,2),(2,5,3,0)],body)

# The street fronts. Openings as model points on the OSM line (X, Y) with bottom, width and
# height; kinds: win (rectangular), slab (on a gable prism), arch (round head of radius w/2),
# adoor (arched double door), sw (tall side window). Positions from the resected panoramas.
PV=lambda y,x=188.75:(x,y)
def FK(u):
 # Fiskaregatan front of 90859847, u from the front's middle, positive westwards.
 o,d,n=frame96((270.17,131.711),(242.74,132.171));L=math.dist((270.17,131.711),(242.74,132.171));return P96((o,d,n),L/2+u,0)
C47=[-11.13,-7.82,-5.48,-3.18,3.18,5.48,7.82,11.13]
OPS={'rd':[('slab',*PV(y,188.68),3.21,.95,1.00) for y in (87.68,86.03,84.38)]+[('win',*PV(87.30,188.69),1.05,.80,1.03),('win',*PV(85.55,188.68),1.05,.95,1.03),('win',*PV(84.10,188.66),1.05,.95,1.03)],
 'co':[('slab',*PV(95.40,189.0),.80,.95,1.20)],
 'gr':[(k,*PV(103.81+s,188.77),b,ww,hh) for s,ww in ((3.76,.95),(6.76,1.75),(11.1,1.75),(14.08,.95)) for k,b,hh in (('win',2.15,1.35),('win',4.95,1.40))]
  +[('sw',x,103.77,b,.70,1.65) for x in (192.2,193.4,194.6) for b in (1.65,4.05)],
 'ow':[('win',*PV(y,188.93),b,1.30,1.40) for y in (122.6,125.6) for b in (2.15,4.85)],
 'on':[],
 'wm':[('arch',*FK(u),1.22,1.35,1.08) for u in C47]+[('adoor',*FK(0),.12,1.90,2.02)]+[('win',*FK(u),4.48,1.15,1.88) for u in C47+[0]],
 'wx':[]}
STYLE={'rd':dict(wall='RedBoard',trim='RedTrim',frame='WhiteFrame',sur='WhiteFrame',plinth=(.35,'Plinth'),boards=True),
 'co':dict(wall='WhiteBoard',trim='WhiteFrame',frame='GreenFrame',sur='WhiteFrame',plinth=(.20,'Plinth'),boards=True),
 'gr':dict(wall='Grey',trim='WhiteFrame',frame='Joinery',sur='WhiteFrame',plinth=(1.30,'BrownBase'),side='SideWhite'),
 'ow':dict(wall='Ochre',trim='WhiteFrame',frame='Joinery',sur='WhiteFrame',plinth=(1.35,'BrownBase')),
 'on':dict(wall='Ochre',trim='WhiteFrame',frame='Joinery',sur='WhiteFrame',plinth=(1.35,'BrownBase')),
 'wm':dict(wall='Stucco',trim='StuccoTrim',frame='RedJoinery',sur='StuccoTrim',plinth=(.50,'Stone')),
 'wx':dict(wall='Stucco',trim='StuccoTrim',frame='RedJoinery',sur='StuccoTrim',plinth=(.30,'Stone'))}
def street96(zone,w):
 # Street walls get the measured fronts: west-facing walls on Proviantgatan (and the grey house's
 # south side, which carries measured windows), north-facing walls on Fiskaregatan.
 ox,oy=outward(w)
 if zone in ('rd','co','gr','ow'):return ox<-.9 or (zone=='gr' and oy<-.9)
 if zone=='wm':return oy>.9
 return False

meshes={}
for zone,spec in Z.items():
 nm=spec['mesh']
 if nm not in meshes:meshes[nm]=b96_new(nm,'Kvarnholmen/Proviantgatan' if zone in ('rd','co','gr') else 'Kvarnholmen/Fiskaregatan')
for zone,spec in Z.items():
 m=meshes[spec['mesh']];H=spec['height'];st=STYLE[zone];wm=M[st['wall']];tm=M[st['trim']];fm=M[st['frame']];sm=M[st['sur']];pz,pm=st['plinth']
 for w in walls(zone):
  if w['kind']!='outer':bz_wall(m,w['p'],w['q'],w['z0'],H,[],wm);continue
  x,y,L,a=sf_edge(w['p'],w['q']);ox,oy=outward(w)
  wma=M[st['side']] if ('side' in st and oy<-.9) else wm
  if not street96(zone,w):
   if st.get('boards'):
    bz_wall(m,w['p'],w['q'],0,H,[],wm);boards82(m,x,y,L,a,pz+.02,H-.08,[],wm);facade_box(m,x,y,0,.39,pz/2,L+.02,.08,pz,M[pm],a)
    for uu in (-L/2+.09,L/2-.09):facade_box(m,x,y,uu,.42,(H+pz)/2,.18,.10,H-pz,tm,a)
   else:plain(m,w,H,wma,fm,sm,1 if H<5 else 2,1.4 if pz>1 else 1.0)
   continue
  mine=[]
  for op in OPS[zone]:
   kind,X,Y,b,ww,hh=op;u=U(w,X,Y);off=abs((X-x)*math.sin(a)-(Y-y)*math.cos(a))
   if off<.7 and abs(u)+ww/2<=L/2+.01:mine.append((kind,u,b,ww,hh))
  holes=[(u,b,ww,hh,ww/2 if kind in ('arch','adoor') else 0) for kind,u,b,ww,hh in mine if kind!='slab']
  bz_wall(m,w['p'],w['q'],0,H,holes,wma)
  if st.get('boards'):boards82(m,x,y,L,a,pz+.02,H-.08,holes+[(u,b,ww,hh,0) for kind,u,b,ww,hh in mine if kind=='slab'],wm)
  for kind,u,b,ww,hh in mine:
   if kind=='slab':slab96(m,x,y,u,b,ww,hh,a,fm,sm)
   elif kind in ('win','sw'):win96(m,x,y,u,b,ww,hh,a,fm,sm,2 if hh<1.2 else 3)
   elif kind=='arch':arch96(m,x,y,u,b,ww,hh,a,fm,sm)
   else:
    # The red arched double door with its fanlight, on two steps.
    for s in (-1,1):facade_box(m,x,y,u+s*ww/4,.10,b+hh/2,ww/2-.03,.07,hh,M['DoorRed'],a)
    for s in (-1,1):
     for zz in (b+.45,b+1.30):facade_box(m,x,y,u+s*ww/4,.14,zz,ww/2-.25,.03,.55,M['DoorRed'],a)
    r=ww/2;k=12
    m.faces([lp(x,y,u+r*math.cos(math.pi*i/k),.10,b+hh+r*math.sin(math.pi*i/k),a) for i in range(k+1)],[tuple(range(k+1)),tuple(range(k,-1,-1))],GLAZE)
    for i in range(1,4):town_rod(m,lp(x,y,u,.13,b+hh,a),lp(x,y,u+r*math.cos(math.pi*i/4),.13,b+hh+r*math.sin(math.pi*i/4),a),.03,M['DoorRed'],6)
    facade_box(m,x,y,u,.13,b+hh,ww,.06,.08,M['DoorRed'],a)
    town_path(m,[lp(x,y,u+(r+.10)*math.cos(math.pi*i/k),.40,b+hh+(r+.10)*math.sin(math.pi*i/k),a) for i in range(k+1)],.09,sm)
    for k2 in range(2):facade_box(m,x,y,u,.36+.30*(2-k2)-.15,(k2+.5)*b/2,ww+.6,.30*(2-k2),b/2,M['Stone'],a)
  # Plinth (with a gap at the door), corner boards or quoins, cornice and gutter.
  at=-L/2
  for lo,hi in sorted((u-ww/2,u+ww/2) for kind,u,b,ww,hh in mine if kind=='adoor')+[(L/2,L/2)]:
   if lo>at+.03:facade_box(m,x,y,(at+lo)/2,.40,pz/2,lo-at,.10,pz,M[pm],a)
   at=max(at,hi)
  if st.get('boards'):
   for uu in (-L/2+.10,L/2-.10):facade_box(m,x,y,uu,.43,(H+pz)/2,.20,.12,H-pz,tm,a)
  elif zone in ('gr','ow','on'):
   facade_box(m,x,y,0,.47,H-.16,L+.12,.24,.32,sm,a)
  if zone=='wm':
   # Rusticated ground floor, the string course, pilaster strips and the cornice.
   for zz in [pz+.36*k for k in range(1,9)]:
    segs=[(-L/2,L/2)]
    for kind,u,b,ww,hh in mine:
     if kind in ('arch','adoor') and b-.05<zz<b+hh+ww/2+.12:segs=[(l0,h0) for l,h_ in segs for l0,h0 in ((l,min(h_,u-ww/2-.16)),(max(l,u+ww/2+.16),h_)) if h0-l0>.05]
    for l0,h0 in segs:facade_box(m,x,y,(l0+h0)/2,.37,zz,h0-l0,.04,.035,M['Rustic'],a)
   facade_box(m,x,y,0,.43,3.70,L+.12,.16,.30,sm,a);facade_box(m,x,y,0,.47,3.52,L+.12,.20,.08,sm,a)
   for uu in (-1.85,1.85,-9.40,9.40,-L/2+.30,L/2-.30):
    facade_box(m,x,y,uu,.42,(3.85+H-.50)/2,.55 if abs(uu)>13 else .45,.10,H-.50-3.85,sm,a)
   for uu in (-L/2+.30,L/2-.30):
    for k in range(9):facade_box(m,x,y,uu,.41,pz+.18+k*.36,.62 if k%2 else .48,.08,.30,sm,a)
   for kind,u,b,ww,hh in mine:
    if kind=='win':facade_box(m,x,y,u,.46,b+hh+.22,ww+.50,.18,.14,sm,a)
   facade_box(m,x,y,0,.45,H-.40,L+.14,.24,.22,sm,a);facade_box(m,x,y,0,.55,H-.17,L+.30,.40,.24,sm,a);facade_box(m,x,y,0,.62,H,L+.50,.55,.12,sm,a)

# Roofs, gables and dormers.
def gboards96(m,F,sL,sR,H,T,tface,holes,ma,step=.22):
 # Vertical boards on a street gable prism, clipped to the rakes, broken at windows (s, b, w, h).
 sm=(sL+sR)/2;n=int((sR-sL)/step);ang=math.atan2(F[1][1],F[1][0])
 for k in range(1,n):
  s=sL+k*(sR-sL)/n;z1=H+(T-H)*(1-abs(s-sm)/(sm-sL))-.12;segs=[(H,z1)]
  for hs,hb,hw,hh in holes:
   if abs(s-hs)<hw/2+.12:segs=[(l0,h0) for l,h_ in segs for l0,h0 in ((l,min(h_,hb-.12)),(max(l,hb+hh+.12),h_)) if h0-l0>.05]
  for l0,h0 in segs:m.box(P96(F,s,tface,(l0+h0)/2),(.035,.03,h0-l0),ma,ang)
def sof96(F,X,Y):o,d,n=F;return (X-o[0])*d[0]+(Y-o[1])*d[1]
# The red house: gable to the street, bargeboards, boards on the gable, a chimney.
F=frame96(*FR96['rd']);s0,s1,t0,t1=bb96('rd',F);m=meshes[Z['rd']['mesh']];Hrd,Trd=Z['rd']['height'],Z['rd']['top']
roof96(m,F,(t0,t1),(s0,s1),Hrd,Trd,M['TileDark'],M['RedBoard'],along=False,ov=.35,verge=.30)
sm_=(s0+s1)/2;sl=(Trd-Hrd)/((s1-s0)/2+FO96)
for sg in (-1,1):town_path(m,[P96(F,sm_+sg*((s1-s0)/2+FO96+.30),-FO96-.40,Hrd-.30*sl),P96(F,sm_,-FO96-.40,Trd+.10)],.08,M['RedTrim'])
gboards96(m,F,s0-FO96,s1+FO96,Hrd,Trd,-FO96-.015,[(sof96(F,X,Y),b,ww,hh) for k,X,Y,b,ww,hh in OPS['rd'] if k=='slab'],M['RedBoard'])
X,Y=P96(F,sm_,(t0+t1)/2+1.2);chimney82(m,X,Y,Trd-.6,Trd+.9,M['Chimney'])
# The cottage.
F=frame96(*FR96['co']);s0,s1,t0,t1=bb96('co',F);m=meshes[Z['co']['mesh']];Hc,Tc=Z['co']['height'],Z['co']['top']
roof96(m,F,(t0,t1),(s0,s1),Hc,Tc,M['Tile'],M['WhiteBoard'],along=False,ov=.30,verge=.25)
sm_=(s0+s1)/2;sl=(Tc-Hc)/((s1-s0)/2+FO96)
for sg in (-1,1):town_path(m,[P96(F,sm_+sg*((s1-s0)/2+FO96+.25),-FO96-.30,Hc-.25*sl),P96(F,sm_,-FO96-.30,Tc+.08)],.07,WF)
gboards96(m,F,s0-FO96,s1+FO96,Hc,Tc,-FO96-.015,[(sof96(F,X,Y),b,ww,hh) for k,X,Y,b,ww,hh in OPS['co'] if k=='slab'],M['WhiteBoard'])
X,Y=P96(F,sm_-.5,(t0+t1)/2+.3);chimney82(m,X,Y,Tc-.4,Tc+.6,M['Chimney'])
# The gateway between the cottage and the red house: white posts and beam, green double gate.
p,q=(188.778,92.378),(188.702,88.831);x,y,L,a=sf_edge(p,q)
gu=U({'p':list(p),'q':list(q)},*PV(90.75,188.74));holes=[(gu,0,2.25,2.05,0)]
bz_wall(m,p,q,0,2.30,holes,M['WhiteBoard']);boards82(m,x,y,L,a,.10,2.22,holes,M['WhiteBoard'])
gate83(m,x,y,gu,0,2.25,2.05,a,M['GateGreen'],WF);facade_box(m,x,y,0,.40,2.36,L+.2,.30,.14,WF,a)
for uu in (-L/2+.10,L/2-.12):facade_box(m,x,y,uu,.44,1.15,.24,.14,2.30,WF,a)
# The grey house: a low black hipped roof.
F=frame96(*FR96['gr']);s0,s1,t0,t1=bb96('gr',F);m=meshes[Z['gr']['mesh']];Hg,Tg=Z['gr']['height'],Z['gr']['top']
r=[P96(F,s0,t0),P96(F,s1,t0),P96(F,s1,t1),P96(F,s0,t1)]
if sum(r[i][0]*r[(i+1)%4][1]-r[(i+1)%4][0]*r[i][1] for i in range(4))<0:r=r[::-1]
inset_roof(m,r,Hg,min(s1-s0,t1-t0)/2-.30,Tg-Hg,M['Sheet'],.45)
# The ochre house: the west wing's saddle along Proviantgatan with a white gable over the grey
# roof; the north range's saddle along Fiskaregatan, hipped over the corner. The wing's ridge
# starts where it meets the range's ridge line; the range runs from 90859847's wall west to the
# Proviantgatan front.
Ho,To=Z['ow']['height'],Z['ow']['top'];Tn=Z['on']['top'];m=meshes[Z['ow']['mesh']]
Fn=frame96(*FR96['on']);ns0,ns1,nt0,nt1=bb96('on',Fn)
Fw=frame96(*FR96['ow']);ws0,ws1,wt0,wt1=bb96('ow',Fw)
ridge_y=P96(Fn,0,(nt0+nt1)/2)[1];wr0=(ridge_y-Fw[0][1])/Fw[1][1]
slw,_=roof96(m,Fw,(wr0,ws1),(wt0,wt1),Ho,To,M['Tile'],M['Ochre'],along=True,ov=.45,verge=.30,ends=('none','gable'),gable_ma=M['SideWhite'])
west_s=sof96(Fn,188.82,ridge_y)
roof96(m,Fn,(ns0,west_s),(nt0,nt1),Ho,Tn,M['Tile'],M['Ochre'],along=True,ov=.45,verge=.30,ends=('none','hip'))
x,y,L,a=sf_edge(*FR96['ow'])
for yy in (122.6,125.6):dormer96(m,x,y,U({'p':list(FR96['ow'][0]),'q':list(FR96['ow'][1])},*PV(yy,188.93)),a,Ho,slw,1.40,1.05,M['DormerBrown'],WF,M['TileDark'],back=.55)
for k in (14.0,30.0):X,Y=P96(Fn,ns0+k,(nt0+nt1)/2-.5);chimney82(m,X,Y,Tn-.6,Tn+.8,M['Chimney'])
# 90859847: the sheet roof, two baroque gables over the side bays, three red dormers.
Fm=frame96(*FR96['wm']);ms0,ms1,mt0,mt1=bb96('wm',Fm);m=meshes[Z['wm']['mesh']];Hm,Tm=Z['wm']['height'],Z['wm']['top']
slm,_=roof96(m,Fm,(ms0,ms1),(mt0,mt1),Hm,Tm,M['SheetRed'],M['Stucco'],along=True,ov=.50,verge=.35)
xg,yg,Lm,am=sf_edge(*FR96['wm'])
def cap96(v):return Hm+3.35+.85*math.sqrt(max(0,1-(v/1.30)**2))
def shoulder96(v):return Hm+2.30-1.20*math.sqrt(max(0,1-((2.05-abs(v))/.75)**2))
def bslab96(m,sc,v0,v1,f,ma):
 # One vertical strip of a baroque gable between v0 and v1 (from the gable's axis), top f(v).
 vs=[P96(Fm,sc+v,tt,zz) for tt in (-FO96-.12,.25) for v,zz in ((v0,Hm-.05),(v1,Hm-.05),(v1,f(v1)),(v0,f(v0)))]
 m.faces(vs,[(0,1,2,3),(7,6,5,4),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)],ma)
for gc in (-5.60,5.60):
 sc=Lm/2+gc
 for k in range(26):bslab96(m,sc,-1.30+k*.10,-1.30+(k+1)*.10,cap96,M['Stucco'])
 for sg in (-1,1):
  for k in range(10):
   v0,v1=sg*(1.30+k*.075),sg*(1.30+(k+1)*.075)
   bslab96(m,sc,min(v0,v1),max(v0,v1),shoulder96,M['Stucco'])
 edge=[(v,shoulder96(v)) for v in [-2.05+k*.075 for k in range(11)]]+[(-1.30,cap96(-1.30))]+[(v,cap96(v)) for v in [-1.30+k*.10 for k in range(1,26)]]+[(1.30,cap96(1.30))]+[(v,shoulder96(v)) for v in [1.30+k*.075 for k in range(11)]]
 town_path(m,[P96(Fm,sc+v,-FO96-.17,zz+.04) for v,zz in edge],.06,M['StuccoTrim'])
 for v in (-.55,.55):
  X,Y=P96(Fm,sc+v,0);uu=(X-xg)*math.cos(am)+(Y-yg)*math.sin(am)
  arch96(m,xg,yg,uu,Hm+.65,.55,.80,am,M['RedJoinery'],M['StuccoTrim'],o=.52)
 X,Y=P96(Fm,sc,.0);box(m,X,Y,.22,.22,.40,Hm+4.18,M['StuccoTrim'],am)
for dc,dw in ((-10.9,1.70),(0,1.30),(10.9,1.70)):dormer96(m,xg,yg,dc,am,Hm,slm,dw,.90,M['DormerRed'],WF,M['DormerRed'],back=.45,dep=2.6)
X,Y=P96(Fm,Lm/2-2.5,(mt0+mt1)/2);chimney82(m,X,Y,Tm-.5,Tm+.9,M['Chimney'])
m=meshes[Z['wx']['mesh']]
for g in Z['wx']['polygons']:
 m.faces([(*v,Z['wx']['top']+.01) for v in g],[tuple(range(len(g))),tuple(range(len(g)-1,-1,-1))],M['Dark'])
 m.prism(g,Z['wx']['height'],Z['wx']['top'],M['Stucco'])
for nm in meshes:b96_finish(meshes[nm],nm.split('_')[-1])

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block96_cameras=[
 sv_camera('471_Block96_Cal_Cottage',182.16,96.58,2.25,64.99,15,90),
 sv_camera('472_Block96_Cal_Grey',181.92,105.62,2.39,58.77,15,90),
 sv_camera('473_Block96_Cal_Ochre',181.54,116.77,2.29,63.4,15,90),
 sv_camera('474_Block96_Cal_Fiskare',254.6,140.1,2.24,150.86,15,90),
 ('475_Block96_Aerial',(215.0,155.0,38.0),(215.0,108.0,2.0),28),
]
print('BLOCK96_GEOMETRY',len(block96_names),'dropped',block96_dropped,block96_samples)
