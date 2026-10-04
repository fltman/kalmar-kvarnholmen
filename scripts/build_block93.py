"""Pass 93: the east side of Landshövdingegatan from the cross street north to the brown gambrel
house (fronts face west):
- 93199599 (3 Landshövdingegatan): a yellow rendered three-storey corner house with a rusticated
  ground floor, light quoins, a chamfered corner, a red entrance door on steps and a hipped sheet
  roof;
- 93238178 (7 Landshövdingegatan): a taupe rendered two-storey corner house with white window
  surrounds, a storey band, a deep cornice and a low sheet roof;
- 93238200: a light grey boarded two-storey house with a brown garage door, a brown door and a
  basement window;
- 93238168: a green-grey boarded two-storey house with a burgundy garage door and door;
- 93238182: a falu-red boarded house: a gable wing to the street with blue-grey trim, a lower piece
  south of it, low yard ranges behind, and the white gate in its own red wall in the gap to the
  south;
- 93238147: a brown boarded house with a gambrel gable to the street on a dark plinth, window boxes,
  low yard ranges behind, and the burgundy gate in the dark boarded gap wall to the south.

References: Google Street View (four panoramas on Landshövdingegatan, heading 62, resected on house
corners), view only. Zones: source/block93.json; see references/block93-notes.md.
"""
B93D=json.loads((R/'source/block93.json').read_text());Z=B93D['zones']
block93_names=[];B93={}
for old in [k for k in list(materials) if k.startswith('M_Block93_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Yellow','TownIvory',(.86,.75,.50),.88,0),('YellowBase','TownIvory',(.82,.70,.45),.90,0),('Quoin','TownStone',(.89,.87,.81),.85,0),
 ('Taupe','TownIvory',(.56,.51,.47),.90,0),('TaupeTrim','TownPaintWhite',(.86,.85,.82),.70,0),('Granite','TownStone',(.36,.33,.32),.90,0),
 ('LightGrey','TownPaintWhite',(.79,.80,.79),.75,0),('GreenGrey','TownPaintGreen',(.53,.57,.51),.75,0),('FaluRed','TownPaintBrown',(.52,.15,.11),.80,0),
 ('BlueGrey','TownPaintWhite',(.68,.73,.76),.65,0),('Brown','TownPaintBrown',(.41,.35,.32),.80,0),('PaleFrame','TownPaintWhite',(.84,.86,.83),.60,0),
 ('WhiteFrame','TownPaintWhite',(.94,.94,.92),.55,0),('Plinth','TownStone',(.63,.63,.61),.90,0),('DarkPlinth','TownStone',(.30,.30,.30),.90,0),
 ('Burgundy','TownPaintBrown',(.47,.10,.16),.60,0),('WoodBrown','TownPaintBrown',(.55,.30,.17),.65,0),('GarageBrown','TownPaintBrown',(.42,.24,.15),.65,0),
 ('RedDoor','TownPaintBrown',(.55,.16,.12),.60,0),('GateWhite','TownPaintWhite',(.86,.86,.83),.60,0),('BoxGreen','TownPaintGreen',(.30,.38,.24),.80,0),
 ('Sheet','TownMetalGrey',(.40,.41,.42),.55,.30),('SheetRed','TownMetalGrey',(.46,.23,.18),.55,.25),('SheetDark','TownMetalGrey',(.17,.17,.18),.55,.30),
 ('Tile','TownTileRed',(.62,.33,.24),.80,0),('TileDark','TownTileRed',(.38,.27,.23),.85,0),('Chimney','TownTileRed',(.58,.34,.27),.85,0),
 ('Iron','TownMetalGrey',(.08,.08,.085),.45,.40),('Dark','TownMetalGrey',(.05,.055,.06),.40,.20),
 ]:
 name='M_Block93_'+key;B93[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block93_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B93;WF=M['WhiteFrame']

def b93_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block93_names.append(name);return Mesh(name,category)
def drop_degenerate_faces93(obj,tol=1e-9):
 import bmesh
 bm=bmesh.new();bm.from_mesh(obj.data)
 def _thin(f):
  L=max(e.calc_length() for e in f.edges);return L>0 and 2*f.calc_area()/L<1e-4
 bad=[f for f in bm.faces if f.calc_area()<tol or len({v.index for v in f.verts})<len(f.verts) or _thin(f)]
 block93_samples[obj.name]=[tuple(round(c,2) for c in f.calc_center_median()) for f in bad[:4]]
 if bad:bmesh.ops.delete(bm,geom=bad,context='FACES_ONLY')
 bm.to_mesh(obj.data);bm.free();obj.data.update();return len(bad)
block93_dropped={};block93_samples={}
def b93_finish(m,osm):
 obj=s21_finish(m);block93_dropped[obj.name]=drop_degenerate_faces93(obj)
 obj['detail_pass']=93;obj['reference_notes']='references/block93-notes.md';obj['osm_way']=osm;return obj

# Street frames: a front from its north end to its south end; s along it, t inwards (east).
def frame93(F):a,b=F;L=math.dist(a,b);d=((b[0]-a[0])/L,(b[1]-a[1])/L);return d,(-d[1],d[0])
def P93(F,s,t=0,z=None):
 d,n=frame93(F);p=(F[0][0]+d[0]*s+n[0]*t,F[0][1]+d[1]*s+n[1]*t);return p if z is None else (*p,z)
def rect93(zone,F):
 d,n=frame93(F);pts=[v for g in Z[zone]['polygons'] for v in g]
 ss=[(v[0]-F[0][0])*d[0]+(v[1]-F[0][1])*d[1] for v in pts];ts=[(v[0]-F[0][0])*n[0]+(v[1]-F[0][1])*n[1] for v in pts]
 return min(ss),max(ss),min(ts),max(ts)
def at93(F,Y):
 # The point of a front line at model y = Y.
 (ax,ay),(bx,by)=F;k=(Y-ay)/(by-ay);return (ax+k*(bx-ax),Y)
def prism93(m,F,outline,t0,t1,ma):
 # A closed prism with an (s, z) outline in a street frame, between depths t0 and t1 (gables).
 n=len(outline);vs=[P93(F,s,t,z) for t in (t0,t1) for s,z in outline]
 m.faces(vs,[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],ma)
def saddle_s93(m,F,s0,s1,t0,t1,H,T,ma,wall,ov=.45,verge=.25,gutter=None):
 # Ridge along the street over the box s0..s1, t0..t1; eaves from the wall faces (0.355 outside
 # the outline) pushed out by the overhang; closed gable prisms at both ends.
 o=.355;tm=(t0+t1)/2;half=tm-t0+o;sl=(T-H)/half
 for ta,sg in ((t0-o,-1),(t1+o,1)):
  e=ta+sg*ov;ze=H-ov*sl
  m.faces([P93(F,s0-o-verge,e,ze),P93(F,s1+o+verge,e,ze),P93(F,s1+o+verge,tm,T),P93(F,s0-o-verge,tm,T)],[(0,1,2,3),(3,2,1,0)],ma)
  town_rod(m,P93(F,s0-o-verge,e,ze-.05),P93(F,s1+o+verge,e,ze-.05),.07,gutter or M['Sheet'],8)
 for s,sg in ((s0-o,1),(s1+o,-1)):
  m.faces([P93(F,s,t0-o,H),P93(F,s,t1+o,H),P93(F,s,tm,T-.02),P93(F,s+sg*.3,t0-o,H),P93(F,s+sg*.3,t1+o,H),P93(F,s+sg*.3,tm,T-.02)],
   [(2,1,0),(3,4,5),(0,1,4,3),(1,2,5,4),(2,0,3,5)],wall)
 return sl
def roof_across93(m,F,prof,t0,t1,ma,trim,ov=.30):
 # A roof whose ridge runs inwards from the street (gable or gambrel to the street): 'prof' is the
 # (s, z) profile across the front, from eave to eave; it runs from t0 to t1 with verges 'ov'.
 for (p0,z0),(p1,z1) in zip(prof,prof[1:]):
  m.faces([P93(F,p0,t0-ov,z0+.12),P93(F,p1,t0-ov,z1+.12),P93(F,p1,t1+ov,z1+.12),P93(F,p0,t1+ov,z0+.12)],[(0,1,2,3),(3,2,1,0)],ma)
  town_path(m,[P93(F,p0,t0-ov-.02,z0+.10),P93(F,p1,t0-ov-.02,z1+.10)],.07,trim)
 for e in (0,-1):town_rod(m,P93(F,prof[e][0],t0-ov,prof[e][1]+.05),P93(F,prof[e][0],t1+ov,prof[e][1]+.05),.07,M['Sheet'],8)
def grooves93(m,x,y,L,a,z0,z1,holes,step=.30,ma=None):
 # Horizontal rustication grooves on the rendered ground floor, broken at the openings.
 z=z0+step
 while z<z1-.05:
  cuts=sorted((hu-hw/2-.12,hu+hw/2+.12) for hu,hb,hw,hh,hr in holes if hb-.1<z<hb+hh+hr+.1);at=-L/2
  for lo,hi in cuts+[(L/2,L/2)]:
   lo=max(-L/2,min(L/2,lo))
   if lo>at+.05:facade_box(m,x,y,(at+lo)/2,.37,z,lo-at,.03,.035,ma or M['Dark'],a)
   at=max(at,min(L/2,hi))
  z+=step
def quoins93(m,x,y,u,side,a,z0,z1,ma):
 # Alternating long and short quoin blocks at a corner (side -1: the block runs to +u).
 z=z0;k=0
 while z<z1-.2:
  w=.62 if k%2==0 else .40;facade_box(m,x,y,u+side*w/2,.40,z+.16,w,.10,.30,ma,a);z+=.36;k+=1
def win93(m,x,y,u,b,w,h,a,frame,trim,o=.16,rows=None,bw=.12):
 cas81(m,x,y,u,b,w,h,a,frame,o,rows or (2 if h<1.0 else 3));surround36(m,x,y,u,b,w,h,a,trim,bw,.40)
 facade_box(m,x,y,u,.47,b-.05,w+.24,.16,.06,trim,a)
def slabwin93(m,x,y,u,b,w,h,a,frame,trim):
 # A window on a gable prism (its face 0.355 out): glass, casement and surround stand proud.
 facade_box(m,x,y,u,.365,b+h/2,w,.02,h,GLAZE,a);cas81(m,x,y,u,b,w,h,a,frame,.40,3 if h>1.0 else 2)
 surround36(m,x,y,u,b,w,h,a,trim,.12,.42);facade_box(m,x,y,u,.50,b-.05,w+.24,.16,.06,trim,a)
def leaf93(m,x,y,u,b,w,h,a,leaf,frame,kind):
 if kind=='garage' or kind=='gate':gate83(m,x,y,u,b,w,h,a,leaf,frame)
 else:door83(m,x,y,u,b,w,h,a,leaf,frame,glass=False)
def pent93(m,p,q,z,depth,ma,ov=.30,drop=.35):
 # A small lean-to roof over a gap wall from p to q (west faces): from z at the wall face down
 # 'drop' over 'depth' inwards.
 x,y,L,a=sf_edge(p,q)
 c=[lp(x,y,-L/2,.355+ov,z+.05,a),lp(x,y,L/2,.355+ov,z+.05,a),lp(x,y,L/2,-depth,z-drop,a),lp(x,y,-L/2,-depth,z-drop,a)]
 m.faces(c,[(0,1,2,3),(3,2,1,0)],ma)

# The fronts (north end -> south end) and the openings, as (kind, model y, bottom, width,
# height). kinds: win, door, garage, gate, base (low basement window). Positions from the
# resected panoramas; see the notes for which are measured and which are estimates.
FR={'yl':((305.51,-14.17),(305.56,-27.69)),'ta':((306.72,9.81),(306.88,-0.01)),'lg':((306.76,19.82),(306.72,9.81)),
 'gg':((306.86,30.33),(306.76,19.82)),'rg':((307.06,40.57),(306.94,35.45)),'rs':((306.94,35.45),(306.88,32.7)),'bg':((307.29,50.53),(307.1,42.65))}
YL_COLS=[-25.91,-23.63,-21.31,-18.97,-16.69];YL_LEV=[(1.20,1.30,1.65),(4.30,1.30,1.75),(7.35,1.25,1.60)]
TA_COLS=[1.35,3.89,6.27,8.19];TA_LEV=[(1.40,1.20,1.70),(3.85,1.20,1.80)]
OPS={'yl':[('door',-25.91,.45,1.15,2.00)]+[('win',Y,b,w,h) for Y in YL_COLS[1:] for b,w,h in YL_LEV[:1]]+[('win',Y,b,w,h) for Y in YL_COLS for b,w,h in YL_LEV[1:]],
 'ta':[('win',Y,b,w,h) for Y in TA_COLS for b,w,h in TA_LEV],
 'lg':[('garage',11.21,0,2.30,2.00),('door',14.41,.15,1.00,2.10),('win',17.91,1.40,1.30,1.30),('base',17.91,.30,1.15,.45)]+[('win',Y,4.05,1.30,1.40) for Y in (11.11,14.41,17.81)],
 'gg':[('win',28.15,1.65,1.50,1.40),('door',24.73,.10,1.20,2.10),('garage',21.53,0,2.80,2.15)]+[('win',Y,4.20,1.50,1.50) for Y in (28.16,24.72,21.21)],
 'rg':[('win',Y,b,1.20,h) for Y in (38.42,36.87) for b,h in ((1.30,1.40),(3.45,1.35))],
 'rs':[('win',34.20,1.30,1.20,1.30),('win',34.20,3.30,1.10,1.20)],
 'bg':[('win',Y,1.25,1.35,1.30) for Y in (47.88,45.03)]+[('win',Y,3.85,1.30,1.40) for Y in (47.83,45.08)]}
STYLE={'yl':dict(wall='Yellow',trim='Quoin',frame='WhiteFrame',plinth=(.35,'Granite'),render=True,leaf='RedDoor'),
 'ta':dict(wall='Taupe',trim='TaupeTrim',frame='WhiteFrame',plinth=(.50,'Plinth'),render=True),
 'lg':dict(wall='LightGrey',trim='WhiteFrame',frame='WhiteFrame',plinth=(.30,'Plinth'),leaf='WoodBrown',garage='GarageBrown'),
 'lgb':dict(wall='LightGrey',trim='WhiteFrame',frame='WhiteFrame',plinth=(.30,'Plinth')),
 'gg':dict(wall='GreenGrey',trim='WhiteFrame',frame='WhiteFrame',plinth=(.25,'Plinth'),leaf='Burgundy',garage='Burgundy'),
 'ggb':dict(wall='GreenGrey',trim='WhiteFrame',frame='WhiteFrame',plinth=(.25,'Plinth')),
 'rs':dict(wall='FaluRed',trim='BlueGrey',frame='BlueGrey',plinth=(.30,'Plinth')),
 'rg':dict(wall='FaluRed',trim='BlueGrey',frame='BlueGrey',plinth=(.30,'Plinth'),gable=True),
 'rw':dict(wall='FaluRed',trim='BlueGrey',frame='BlueGrey',plinth=(.30,'Plinth')),
 'bg':dict(wall='Brown',trim='PaleFrame',frame='PaleFrame',plinth=(.55,'DarkPlinth'),gable=True,boxes=True),
 'bw':dict(wall='Brown',trim='PaleFrame',frame='PaleFrame',plinth=(.40,'DarkPlinth'))}
def rhythm93(zone,w,L):
 # Side fronts on the cross street (estimated: the panoramas only graze them): window columns
 # at the street front's spacing, all storeys.
 ox,oy=outward(w)
 if zone=='yl' and oy>.5:
  n=max(1,round(L/2.35));return [('win',-L/2+(k+.5)*L/n,b,ww,hh) for k in range(n) for b,ww,hh in YL_LEV]
 if zone=='ta' and oy<-.9:
  n=max(1,round(L/2.5));return [('win',-L/2+(k+.5)*L/n,b,ww,hh) for k in range(n) for b,ww,hh in TA_LEV]
 return None

meshes={}
for zone,spec in Z.items():
 nm=spec['mesh']
 if nm not in meshes:meshes[nm]=b93_new(nm,'Kvarnholmen/Landshovdingegatan')
for zone,spec in Z.items():
 m=meshes[spec['mesh']];H=spec['height'];st=STYLE[zone];wm=M[st['wall']];tm=M[st['trim']];fm=M[st['frame']];pz,pm=st['plinth']
 ren=st.get('render',False)
 for w in walls(zone):
  if w['kind']!='outer':bz_wall(m,w['p'],w['q'],w['z0'],H,[],wm);continue
  x,y,L,a=sf_edge(w['p'],w['q']);ox,oy=outward(w)
  mine=[]
  if zone in FR:
   for kind,Y,b,ww,hh in OPS.get(zone,[]):
    X,Y2=at93(FR[zone],Y);u=U(w,X,Y2);off=abs((X-x)*math.sin(a)-(Y2-y)*math.cos(a))
    if off<.6 and abs(u)+ww/2<=L/2+.01:mine.append((kind,u,b,ww,hh))
  street=bool(mine)
  if not mine:
   r=rhythm93(zone,w,L)
   if r:mine=r;street=True
  if not street:
   if L<1.5:bz_wall(m,w['p'],w['q'],0,H,[],wm);continue
   plain(m,w,H,wm,fm,tm,1 if H<4 else 2,.9);continue
  lowh=[(u,b,ww,hh,0) for kind,u,b,ww,hh in mine if b+hh<=H-.05]
  bz_wall(m,w['p'],w['q'],0,H,lowh,wm)
  if ren:
   # Rendered fronts: plinth, storey band, cornice; the yellow house has a rusticated ground
   # floor and quoins.
   facade_box(m,x,y,0,.40,pz/2,L+.02,.10,pz,M[pm],a)
   if zone=='yl':
    grooves93(m,x,y,L,a,pz,3.90,lowh,.30,M['YellowBase'])
    facade_box(m,x,y,0,.44,4.07,L+.02,.18,.32,M['Yellow'],a)
    facade_box(m,x,y,0,.42,9.70,L+.02,.14,.30,M['Quoin'],a);facade_box(m,x,y,0,.56,10.45,L+.20,.42,.70,M['Quoin'],a)
    for uu,sg in ((-L/2,-1),(L/2,1)):
     if L<4 or sg==1:quoins93(m,x,y,uu,-sg,a,pz,9.5,M['Quoin'])
   else:
    facade_box(m,x,y,0,.43,3.65,L+.02,.16,.22,tm,a);facade_box(m,x,y,0,.40,6.65,L+.02,.10,.40,tm,a)
    facade_box(m,x,y,0,.58,7.05,L+.25,.46,.50,tm,a)
   for kind,u,b,ww,hh in mine:
    if kind=='door':
     door83(m,x,y,u,b,ww,hh,a,M[st.get('leaf','RedDoor')],fm,glass=True);facade_box(m,x,y,u,.18,b/2,ww+.10,.40,b,M['Granite'],a)
     facade_box(m,x,y,u,.13,b+hh+.22,ww,.02,.34,GLAZE,a);surround36(m,x,y,u,b,ww,hh+.42,a,M['Quoin'],.14,.40)
    else:win93(m,x,y,u,b,ww,hh,a,fm,tm,bw=.14)
   continue
  # Boarded fronts.
  slabw=[(u,b,ww,hh,0) for kind,u,b,ww,hh in mine if b+hh>H-.05]
  boards82(m,x,y,L,a,pz+.02,H-.08,lowh,wm)
  for kind,u,b,ww,hh in mine:
   if b+hh>H-.05:slabwin93(m,x,y,u,b,ww,hh,a,fm,tm);continue
   if kind=='win':
    win93(m,x,y,u,b,ww,hh,a,fm,tm)
    if st.get('boxes'):facade_box(m,x,y,u,.62,b-.22,ww+.10,.22,.18,M['BoxGreen'],a)
   elif kind=='base':facade_box(m,x,y,u,.20,b+hh/2,ww,.02,hh,GLAZE,a);surround36(m,x,y,u,b,ww,hh,a,fm,.10,.40)
   elif kind=='garage':leaf93(m,x,y,u,b,ww,hh,a,M[st.get('garage','GarageBrown')],fm,'garage')
   else:
    leaf93(m,x,y,u,b,ww,hh,a,M[st.get('leaf','WoodBrown')],fm,'door')
    if zone=='lg':facade_box(m,x,y,u,.62,b+hh+.20,ww+.6,.55,.08,fm,a)
  for uu in (-L/2+.09,L/2-.09):facade_box(m,x,y,uu,.42,(H+pz)/2,.18,.10,H-pz,tm,a)
  at=-L/2
  for lo,hi in sorted((u-ww/2,u+ww/2) for kind,u,b,ww,hh in mine if kind in ('door','garage') and b<pz)+[(L/2,L/2)]:
   if lo>at+.03:facade_box(m,x,y,(at+lo)/2,.39,pz/2,lo-at,.08,pz,M[pm],a)
   at=max(at,hi)
  if not st.get('gable') and spec['roof']!='flat':facade_box(m,x,y,0,.46,H-.10,L+.1,.14,.20,tm,a)

# Roofs.
Fy=FR['yl'];m=meshes[Z['yl']['mesh']]
inset_roof(m,[tuple(v) for v in Z['yl']['polygons'][0]],Z['yl']['height'],3.0,Z['yl']['top']-Z['yl']['height'],M['SheetRed'],.45)
for s,t in ((3.0,7.0),(9.5,6.5)):X,Y=P93(Fy,s,t);chimney82(m,X,Y,Z['yl']['top']-.5,Z['yl']['top']+.9,M['Chimney'])
m=meshes[Z['ta']['mesh']];inset_roof(m,[tuple(v) for v in Z['ta']['polygons'][0]],Z['ta']['height'],1.8,Z['ta']['top']-Z['ta']['height'],M['Sheet'],.30)
box(m,*P93(FR['ta'],4.5,4.0),.9,.9,.5,Z['ta']['top']-.3,M['Sheet'],0,M['SheetDark'])
for zone,ma,chims in (('lg','Tile',[(5.0,6.0)]),('gg','SheetDark',[(3.0,4.8),(7.0,4.6)]),('rs','Tile',[])):
 F=FR[zone];m=meshes[Z[zone]['mesh']];s0,s1,t0,t1=rect93(zone,F)
 saddle_s93(m,F,s0,s1,t0,t1,Z[zone]['height'],Z[zone]['top'],M[ma],M[STYLE[zone]['wall']],gutter=M['Sheet'] if zone!='rs' else M['BlueGrey'])
 for s,t in chims:X,Y=P93(F,s,t);chimney82(m,X,Y,Z[zone]['top']-.6,Z[zone]['top']+.8,M['Chimney'])
# The red gable wing: ridge running in from the street, a closed gable prism at each end.
F=FR['rg'];m=meshes[Z['rg']['mesh']];s0,s1,t0,t1=rect93('rg',F);H=Z['rg']['height'];T=Z['rg']['top'];o=.355;sm=(s0+s1)/2
roof_across93(m,F,[(s0-o-.30,H-.30),(s0-o,H),(sm,T),(s1+o,H),(s1+o+.30,H-.30)],t0-o,t1+o,M['Tile'],M['BlueGrey'])
for tt,sg in ((t0-o,1),(t1+o,-1)):prism93(m,F,[(s0-o,H),(s1+o,H),(sm,T-.05)],tt+(.005 if sg>0 else 0),tt+sg*.35,M['FaluRed'])
X,Y=P93(F,sm,(t0+t1)/2+2.5);chimney82(m,X,Y,T-.6,T+.7,M['Chimney'])
# The brown gambrel house: profile across the front (wall face to wall face), the ridge running
# back from the street; gable prisms front and rear carry the attic windows.
F=FR['bg'];m=meshes[Z['bg']['mesh']];s0,s1,t0,t1=rect93('bg',F);H=Z['bg']['height'];T=Z['bg']['top'];KN,KW=5.35,.95
sL,sR=s0-o,s1+o;sm=(sL+sR)/2
roof_across93(m,F,[(sL-.25,H-.50),(sL,H),(sL+KW,KN),(sm,T),(sR-KW,KN),(sR,H),(sR+.25,H-.50)],t0-o,t1+o,M['TileDark'],M['PaleFrame'])
g=[(sL,H),(sR,H),(sR-KW,KN),(sm,T-.05),(sL+KW,KN)]
for tt,sg in ((t0-o,1),(t1+o,-1)):prism93(m,F,g,tt+(.005 if sg>0 else 0),tt+sg*.35,M['Brown'])
# Boards on the street gable, clipped to the profile.
def gz93(s):
 if s<=sL+KW:return H+(KN-H)*(s-sL)/KW
 if s<=sm:return KN+(T-KN)*(s-sL-KW)/(sm-sL-KW)
 if s<=sR-KW:return KN+(T-KN)*(sR-KW-s)/(sR-KW-sm)
 return H+(KN-H)*(sR-s)/KW
x,y,L,a=sf_edge(*F);n=int((sR-sL)/.22)
for k in range(1,n):
 s=sL+k*(sR-sL)/n;z1=gz93(s)-.10;segs=[(H,z1)]
 for Y in (47.83,45.08):
  X2,Y2=at93(F,Y);sc=(math.dist(F[0],(X2,Y2)))
  if abs(s-sc)<.65+.12:segs=[(l0,h0) for l,h_ in segs for l0,h0 in ((l,min(h_,3.85-.12)),(max(l,3.85+1.40+.12),h_)) if h0-l0>.05]
 for l0,h0 in segs:
  if h0-l0>.05:m.box(P93(F,s,t0-o-.02,(l0+h0)/2),(.035,.03,h0-l0),M['Brown'],a)
# The low yard ranges and bumps: flat dark roofs.
for zone in ('lgb','ggb','rw','bw'):
 m=meshes[Z[zone]['mesh']]
 for gpoly in Z[zone]['polygons']:m.faces([(*v,Z[zone]['height']+.02) for v in gpoly],[tuple(range(len(gpoly))),tuple(range(len(gpoly)-1,-1,-1))],M['SheetDark'])
# The gap walls with their gates (outside the OSM outlines, as on the panoramas): the white gate
# between the green-grey and the red house, the burgundy gate between the red and the brown.
for (p,q),mesh,wall,leaf,frame,ztop,gw,gh in ((((306.88,32.7),(306.86,30.33)),'93238182','FaluRed','GateWhite','BlueGrey',3.40,2.00,2.60),
                                            (((307.1,42.65),(307.06,40.57)),'93238147','Brown','Burgundy','PaleFrame',3.90,1.90,2.20)):
 m=meshes['SM_Kvarnholmen_House_'+mesh];x,y,L,a=sf_edge(p,q)
 bz_wall(m,p,q,0,ztop,[(0,.05,gw,gh,0)],M[wall]);gate83(m,x,y,0,.05,gw,gh,a,M[leaf],M[frame])
 facade_box(m,x,y,0,.40,.05+gh+.12,gw+.40,.10,.20,M[frame],a)
 for uu in (-L/2+.08,L/2-.08):facade_box(m,x,y,uu,.42,ztop/2,.16,.10,ztop,M[frame],a)
 pent93(m,p,q,ztop,2.0,M['SheetDark'])
for nm in meshes:b93_finish(meshes[nm],nm.split('_')[-1])

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block93_cameras=[
 sv_camera('456_Block93_Cal_Taupe',300.09,3.50,2.43,62,15,90),
 sv_camera('457_Block93_Cal_GreenGrey',299.22,25.18,2.60,62,15,90),
 sv_camera('458_Block93_Cal_Gambrel',300.30,46.27,2.30,62,15,90),
 sv_camera('459_Block93_Cal_Yellow',300.00,-26.70,2.11,62,15,90),
 ('460_Block93_Aerial',(285.0,12.0,40.0),(312.0,12.0,2.0),28),
]
print('BLOCK93_GEOMETRY',len(block93_names),'dropped',block93_dropped,block93_samples)
