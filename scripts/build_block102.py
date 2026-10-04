"""Pass 102: the far east end of Storgatan and the corner of Östra Vallgatan:
- 93238165 (69): the cream rendered three-storey house (west) with iron balconies, a glazed door
  and a black carriage gate, under a low dark hipped roof; the cream rendered two-storey house
  (east) on a grey plinth with five upper and six ground-floor openings (a glazed door among them),
  a cornice and a red tiled saddle roof with three red gabled dormers (the east one wider);
- 93238196: two small falu-red boarded houses with their gables to the street, white corner and
  verge boards and white windows, a blue double gate in a white frame between them;
- 93238164: the grey-green boarded two-storey house on a dark plinth, three upper windows under
  grey awnings, two ground-floor windows and a pale panelled door, under a red tiled saddle roof;
- 93238222: the cream rendered corner house at Östra Vallgatan under a red tiled hipped roof with
  a roof light and a chimney (under scaffolding in the photos; scaffolding omitted);
- 93199630 (67): the ochre rendered two-storey house on a grey plinth with a cream lesene, cream
  window surrounds, the red double door on steps and a small window beside it;
- 93199675: the garage range: five red chevron-boarded doors (the two east ones glazed at the top)
  between grey rendered piers under a red tiled hipped roof; its long rear part low and flat;
- 93199606: the brown brick two-storey house on a pale stone base, tall white windows with dark
  brown shutters, a brick band and a pale frieze under the dark hipped roof with deep eaves.

References: Google Street View (four panoramas on Storgatan and Östra Vallgatan, resected on house
corners), view only. Zones: source/block102.json; see references/block102-notes.md. Cars, lamps,
drainpipes, signs, the scaffolding and the electricity cabinet are omitted.
"""
B102D=json.loads((R/'source/block102.json').read_text());Z=B102D['zones']
block102_names=[];B102={}
for old in [k for k in list(materials) if k.startswith('M_Block102_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Cream','TownIvory',(.88,.85,.76),.85,0),('Cream3','TownIvory',(.86,.83,.74),.85,0),('Trim','TownPaintWhite',(.93,.92,.88),.60,0),
 ('White','TownPaintWhite',(.95,.95,.93),.55,0),('Plinth','TownStone',(.62,.62,.60),.90,0),('PlinthDark','TownStone',(.36,.36,.36),.90,0),
 ('Tile','TownTileRed',(.80,.38,.24),.80,0),('DormerRed','TownPaintBrown',(.66,.22,.18),.60,0),('Red','TownPaintBrown',(.66,.17,.14),.80,0),
 ('Blue','TownPaintWhite',(.55,.66,.80),.60,0),('GreyGreen','TownPaintWhite',(.62,.65,.60),.80,0),('Awning','TownPaintWhite',(.72,.72,.70),.70,0),
 ('Ochre','TownIvory',(.82,.66,.33),.85,0),('Lesene','TownIvory',(.90,.87,.78),.85,0),('DoorRed','TownPaintBrown',(.55,.20,.17),.60,0),
 ('Concrete','TownStone',(.58,.56,.52),.90,0),('GarageRed','TownPaintBrown',(.75,.25,.25),.70,0),
 ('Brick','TownTileRed',(.52,.34,.25),.90,0),('Copper','TownPaintGreen',(.45,.62,.54),.60,0),('BrickBand','TownTileRed',(.38,.24,.18),.90,0),('Stone','TownStone',(.80,.78,.72),.90,0),
 ('Frieze','TownIvory',(.78,.70,.55),.85,0),('Shutter','TownPaintBrown',(.22,.15,.12),.70,0),('RoofDark','TownMetalGrey',(.20,.19,.19),.60,.20),
 ('Roof','TownMetalGrey',(.30,.30,.31),.60,.20),('Sheet','TownMetalGrey',(.12,.12,.13),.50,.30),('Chimney','TownTileRed',(.60,.34,.27),.85,0),
 ('Dark','TownMetalGrey',(.06,.06,.065),.45,.40),('Iron','TownMetalGrey',(.08,.08,.085),.45,.40),
 ]:
 name='M_Block102_'+key;B102[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block102_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B102;WF=M['White']

def b102_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block102_names.append(name);return Mesh(name,category)
def drop_degenerate_faces102(obj,tol=1e-9):
 import bmesh
 bm=bmesh.new();bm.from_mesh(obj.data)
 def _thin(f):
  L=max(e.calc_length() for e in f.edges);return L>0 and 2*f.calc_area()/L<1e-4
 bad=[f for f in bm.faces if f.calc_area()<tol or len({v.index for v in f.verts})<len(f.verts) or _thin(f)]
 if bad:bmesh.ops.delete(bm,geom=bad,context='FACES_ONLY')
 bm.to_mesh(obj.data);bm.free();obj.data.update();return len(bad)
block102_dropped={};block102_samples={}
def b102_finish(m,osm):
 obj=s21_finish(m)
 import bmesh
 bm=bmesh.new();bm.from_mesh(obj.data)
 block102_samples[obj.name]=[tuple(round(c,2) for c in f.calc_center_median())+(round(f.calc_area(),6),len(f.verts)) for f in bm.faces if f.calc_area()<1e-9 or (max(e.calc_length() for e in f.edges)>0 and 2*f.calc_area()/max(e.calc_length() for e in f.edges)<1e-4)][:6]
 bm.free();block102_dropped[obj.name]=drop_degenerate_faces102(obj)
 obj['detail_pass']=102;obj['reference_notes']='references/block102-notes.md';obj['osm_way']=osm;return obj

def pt102(a,b,s):
 # The point s metres from a towards b.
 L=math.dist(a,b);return (a[0]+(b[0]-a[0])*s/L,a[1]+(b[1]-a[1])*s/L)
# Street frames for the gable fronts (as pass 100): s along the OSM front from A to B, t outwards
# (to the right of A->B); the facade surfaces stand at t = 0.355.
def fr102(A,B):
 L=math.dist(A,B);D=((B[0]-A[0])/L,(B[1]-A[1])/L);return dict(A=A,B=B,D=D,N=(D[1],-D[0]),L=L,ang=math.atan2(D[1],D[0]))
def P102(f,s,t=0,z=None):
 p=(f['A'][0]+f['D'][0]*s+f['N'][0]*t,f['A'][1]+f['D'][1]*s+f['N'][1]*t);return p if z is None else (*p,z)
def rect102(f,zone):
 pts=[v for g in Z[zone]['polygons'] for v in g];A,D,N=f['A'],f['D'],f['N']
 ss=[(v[0]-A[0])*D[0]+(v[1]-A[1])*D[1] for v in pts];ts=[(v[0]-A[0])*N[0]+(v[1]-A[1])*N[1] for v in pts]
 return min(ss),max(ss),min(ts),max(ts)
def prism102(m,f,outline,t0,t1,ma):
 n=len(outline);vs=[P102(f,s,t,z) for t in (t0,t1) for s,z in outline]
 m.faces(vs,[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],ma)
def gable102(m,f,zone,wall,roof,trim,ov=.30,eave=.30):
 # Saddle roof with its ridge running back from the street over the boxed outline; gable prisms in
 # the wall material at the street front and the back, verge boards, gutters.
 s0,s1,t0,t1=rect102(f,zone)
 H=Z[zone]['height'];T=Z[zone]['top'];o=.355;sL,sR=s0-o,s1+o;sm=(sL+sR)/2;sl=(T-H)/(sm-sL)
 tf,tb=t1+o+ov,t0-o-ov
 for se,sg in ((sL,-1),(sR,1)):
  e=se+sg*eave;ze=H-eave*sl
  m.faces([P102(f,e,tb,ze+.12),P102(f,sm,tb,T+.12),P102(f,sm,tf,T+.12),P102(f,e,tf,ze+.12)],[(0,1,2,3),(3,2,1,0)],roof)
  town_rod(m,P102(f,e,tb,ze+.02),P102(f,e,tf,ze+.02),.07,M['Sheet'],8)
  for tt in (tf-.03,tb+.03):town_path(m,[P102(f,e,tt,ze+.06),P102(f,sm,tt,T+.06)],.08,trim)
 g=[(sL,H),(sR,H),(sm,T-.02)]
 prism102(m,f,g,t1+.005,t1+o,wall);prism102(m,f,g,t0-o,t0-.005,wall)
 return sL,sR,sm,t1+o
def gable_boards102(m,f,sL,sR,sm,H,T,tface,ma,step=.22,holes=()):
 # Vertical boards on the street gable, clipped to the rakes and broken round windows (s,b,w,h).
 n=int((sR-sL)/step)
 for k in range(1,n):
  s=sL+k*(sR-sL)/n;z1=H+(T-H)*(1-abs(s-sm)/(sm-sL))-.14;z0=H
  for hs,hb,hw,hh in holes:
   if abs(s-hs)<hw/2+.12 and hb+hh+.12>z0:z0=hb+hh+.12
  if z1-z0>.06:m.box(P102(f,s,tface+.02,(z0+z1)/2),(.035,.03,z1-z0),ma,f['ang'])
def win102(m,x,y,u,b,w,h,a,frame,sur,rows=2,bw=.10,o=.16):
 # Casement in its frame, a flat surround and a sill.
 cas81(m,x,y,u,b,w,h,a,frame,o,rows)
 if sur:surround36(m,x,y,u,b,w,h,a,sur,bw,.40);facade_box(m,x,y,u,.47,b-.05,w+.24,.16,.06,sur,a)
def flush102(m,x,y,u,b,w,h,a,frame,rows=2):
 # A window laid on a solid face (gable prisms): glass, frame and surround in front of it.
 facade_box(m,x,y,u,.37,b+h/2,w,.02,h,GLAZE,a);cas81(m,x,y,u,b,w,h,a,frame,.41,rows);surround36(m,x,y,u,b,w,h,a,frame,.08,.42)
def fronts102(m,zone,test,wall,frame,trim,levels,floor0=1.0):
 # Party and upper walls in the wall material, unseen outer walls plain; returns the street fronts.
 H=Z[zone]['height'];out=[]
 for w in walls(zone):
  if w['kind']!='outer':bz_wall(m,w['p'],w['q'],w['z0'],H,[],wall);continue
  ox,oy=outward(w);x,y,L,a=sf_edge(w['p'],w['q'])
  if test(ox,oy,x,y):out.append(w);continue
  plain(m,w,H,wall,frame,trim,levels,floor0)
 return out
def flatroof102(m,zone,ma,trim):
 H=Z[zone]['height']
 for g in Z[zone]['polygons']:m.faces([(*v,H+.02) for v in g],[tuple(range(len(g))),tuple(range(len(g)-1,-1,-1))],ma)
 for w in walls(zone,'outer'):
  x,y,L,a=sf_edge(w['p'],w['q']);facade_box(m,x,y,0,.38,H+.12,L+.06,.12,.24,trim,a)
def dormer102(m,x,y,u,a,H,w,wins,body,roof,frame,back=-.25,dep=2.9,zt=1.55,zp=2.40,wb=.30,wh=1.05):
 # A gabled dormer: its face 'back' metres inside the OSM line (negative: in front of it), side eaves zt and ridge zp above
 # the main eaves, a small saddle roof running back into the main roof, white verge boards.
 of=-back;z0=H-.20;zt=H+zt;zp=H+zp
 box(m,*lp(x,y,u,of-dep/2,0,a)[:2],w,dep,zt-z0,z0,body,a)
 tri=[(u-w/2,zt),(u+w/2,zt),(u,zp-.03)];vs=[lp(x,y,uu,o,zz,a) for o in (of,of-dep) for uu,zz in tri]
 m.faces(vs,[(2,1,0),(3,4,5),(0,1,4,3),(1,2,5,4),(2,0,3,5)],body)
 k=(zp-zt)/(w/2)
 for sg in (-1,1):
  e=w/2+.15
  m.faces([lp(x,y,u+sg*e,of+.15,zt-.15*k+.08,a),lp(x,y,u,of+.15,zp+.08,a),lp(x,y,u,of-dep,zp+.08,a),lp(x,y,u+sg*e,of-dep,zt-.15*k+.08,a)],[(0,1,2,3),(3,2,1,0)],roof)
  town_path(m,[lp(x,y,u+sg*e,of+.13,zt-.15*k+.04,a),lp(x,y,u,of+.13,zp+.04,a)],.07,frame)
 for du,ww in wins:
  facade_box(m,x,y,u+du,of+.01,H+wb+wh/2,ww,.02,wh,GLAZE,a);cas81(m,x,y,u+du,H+wb,ww,wh,a,frame,of+.05,2)
 facade_box(m,x,y,u,of+.04,H+wb-.06,w-.10,.08,.06,frame,a)
def corners102(m,x,y,L,a,z0,z1,ma,bw=.16):
 for uu in (-L/2+bw/2,L/2-bw/2):facade_box(m,x,y,uu,.42,(z0+z1)/2,bw,.10,z1-z0,ma,a)
NS=lambda ox,oy,x,y:oy<-.9 and y<1.5          # north side of Storgatan, fronts facing south
SS=lambda ox,oy,x,y:oy>.9 and y>-13.0         # south side, fronts facing north

# ---- 93238165 (69): the three-storey west part and the two-storey east part with dormers.
m=b102_new(Z['t165']['mesh'],'Kvarnholmen/Storgatan');CR=M['Cream'];C3=M['Cream3'];TR=M['Trim']
A65,B65=(328.51,-0.33),(355.6,-0.43)
H=Z['t165']['height']
for w in fronts102(m,'t165',NS,C3,WF,TR,3):
 x,y,L,a=sf_edge(w['p'],w['q']);S=lambda s:U(w,*pt102(A65,B65,s))
 ops=[(S(s),b,1.15,1.40) for s in (1.6,4.6,7.6,10.2,13.0) for b in (3.30,5.95)]+[(S(s),1.05,1.15,1.40) for s in (1.6,4.6,7.6)]
 gu,du=S(12.55),S(10.0)
 holes=[(u,b,ww,hh,0) for u,b,ww,hh in ops]+[(gu,0,2.90,2.55,0),(du,.15,1.05,2.30,0)]
 bz_wall(m,w['p'],w['q'],0,H,holes,C3)
 for u,b,ww,hh in ops:win102(m,x,y,u,b,ww,hh,a,WF,TR,2)
 # The carriage gate: two black leaves with a lattice of diagonal battens; the glazed door.
 gate83(m,x,y,gu,0,2.90,2.55,a,M['Iron'],M['Dark'])
 door83(m,x,y,du,.15,1.05,2.30,a,WF,TR,glass=True);facade_box(m,x,y,du,.10,.15+2.30*.45,.75,.02,1.2,GLAZE,a)
 # Iron balconies on the two upper floors at the west end.
 for b in (3.30,5.95):
  bu=S(6.1);facade_box(m,x,y,bu,.95,b-.12,3.60,1.20,.10,M['Iron'],a)
  for ou,od,ww in ((0,1.53,3.60),(-1.78,.95,.04),(1.78,.95,.04)):
   facade_box(m,x,y,bu+ou,od,b+.45,ww if ww>1 else .04,1.20 if ww<1 else .04,.04,M['Iron'],a);facade_box(m,x,y,bu+ou,od,b+.95,ww if ww>1 else .04,1.20 if ww<1 else .04,.05,M['Iron'],a)
  for k in range(19):facade_box(m,x,y,bu-1.75+k*3.5/18,1.53,b+.45,.025,.025,1.0,M['Iron'],a)
 facade_box(m,x,y,0,.40,.30,L+.02,.10,.60,M['Plinth'],a)
 facade_box(m,x,y,0,.46,H-.18,L+.10,.22,.36,TR,a)
fronts102(m,'t165b',lambda *_:False,C3,WF,TR,2);flatroof102(m,'t165b',M['Roof'],C3)
hip82(m,'t165',A65,(343.6,-0.39),M['Roof'])
H=Z['c165']['height']
for w in fronts102(m,'c165',NS,CR,WF,TR,2):
 x,y,L,a=sf_edge(w['p'],w['q']);S=lambda s:U(w,*pt102(A65,B65,s))
 ops=[(S(s),3.30,1.20,1.35) for s in (16.1,18.4,20.75,23.95,25.75)]+[(S(s),1.10,1.20,1.25) for s in (16.1,18.4,20.75,23.05)]+[(S(25.45),1.10,1.05,1.25)]
 du=S(24.25);holes=[(u,b,ww,hh,0) for u,b,ww,hh in ops]+[(du,.10,.85,2.25,0)]
 bz_wall(m,w['p'],w['q'],0,H,holes,CR)
 for u,b,ww,hh in ops:win102(m,x,y,u,b,ww,hh,a,WF,TR,2,bw=.08)
 door83(m,x,y,du,.10,.85,2.25,a,WF,TR,glass=True);facade_box(m,x,y,du,.10,1.0,.60,.02,1.4,GLAZE,a)
 facade_box(m,x,y,0,.40,.30,L+.02,.10,.60,M['Plinth'],a)
 corners102(m,x,y,L,a,.60,H-.3,CR,.40)
 facade_box(m,x,y,0,.46,H-.18,L+.10,.22,.36,TR,a);town_rod(m,lp(x,y,-L/2,.70,H+.02,a),lp(x,y,L/2,.70,H+.02,a),.07,M['Sheet'],8)
saddle82(m,'c165',(343.6,-0.39),B65,M['Tile'],CR,along=True)
fw=[w for w in walls('c165','outer') if NS(*outward(w),*sf_edge(w['p'],w['q'])[:2])][0];x,y,L,a=sf_edge(fw['p'],fw['q'])
for s,ww,wins in ((17.5,2.6,[(-.55,.95),(.55,.95)]),(20.4,2.4,[(-.50,.90),(.50,.90)]),(24.0,3.4,[(-.75,1.25),(.75,1.25)])):
 dormer102(m,x,y,U(fw,*pt102(A65,B65,s)),a,H,ww,wins,M['DormerRed'],M['Tile'],WF)
fronts102(m,'c165b',lambda *_:False,CR,WF,TR,2);flatroof102(m,'c165b',M['Roof'],CR)
X,Y=pt102(A65,B65,19.0);chimney82(m,X,Y+5.6,Z['c165']['top']-.6,Z['c165']['top']+.7,M['Chimney'])
b102_finish(m,'93238165')

# ---- 93238196: the two red gable houses and the blue gate (s from the west end of each front).
m=b102_new(Z['r196a']['mesh'],'Kvarnholmen/Storgatan');RE=M['Red']
for zone,A,B,ups,downs in (('r196a',(355.6,-0.43),(359.85,-0.42),[(1.30,3.30,.95,1.10),(2.95,3.30,.95,1.10)],[(1.30,1.00,1.00,1.30),(2.95,1.00,1.00,1.30)]),
                            ('r196b',(361.7,-0.41),(366.03,-0.40),[(2.17,3.05,1.00,1.25)],[(2.17,.90,1.05,1.35)])):
 H=Z[zone]['height'];T=Z[zone]['top'];F=fr102(A,B)
 for w in fronts102(m,zone,NS,RE,WF,WF,1,.9):
  x,y,L,a=sf_edge(w['p'],w['q']);S=lambda s:U(w,*pt102(A,B,s))
  holes=[(S(s),b,ww,hh,0) for s,b,ww,hh in downs+[o for o in ups if o[1]+o[3]<H-.1]]
  bz_wall(m,w['p'],w['q'],0,H,holes,RE);boards82(m,x,y,L,a,.32,H-.08,[(S(s),b,ww,hh,0) for s,b,ww,hh in downs+ups],RE)
  for s,b,ww,hh in downs:win102(m,x,y,S(s),b,ww,hh,a,WF,WF,2)
  facade_box(m,x,y,0,.39,.16,L+.02,.08,.32,M['PlinthDark'],a)
  corners102(m,x,y,L,a,.32,H,WF)
  facade_box(m,x,y,0,.44,H-.08,L+.1,.12,.16,WF,a)
 sL,sR,sm,tface=gable102(m,F,zone,RE,M['RoofDark'],WF)
 gable_boards102(m,F,sL,sR,sm,H,T,tface,RE,holes=ups)
 fw=[w for w in walls(zone,'outer') if NS(*outward(w),*sf_edge(w['p'],w['q'])[:2])][0];x,y,L,a=sf_edge(fw['p'],fw['q'])
 for s,b,ww,hh in ups:
  if b+hh<H-.1:win102(m,x,y,U(fw,*pt102(A,B,s)),b,ww,hh,a,WF,WF,2)
  else:flush102(m,x,y,U(fw,*pt102(A,B,s)),b,ww,hh,a,WF,2)
 s0,s1,t0,t1=rect102(F,zone);X,Y=P102(F,(s0+s1)/2,t1-4.0);chimney82(m,X,Y,T-.6,T+.6,M['Dark'])
# The gate bay: a red boarded wall with the blue double gate in a white frame, flat behind.
H=Z['r196g']['height']
for w in fronts102(m,'r196g',NS,RE,WF,WF,1):
 x,y,L,a=sf_edge(w['p'],w['q']);holes=[(0,0,1.55,2.20,0)]
 bz_wall(m,w['p'],w['q'],0,H,holes,RE);boards82(m,x,y,L,a,.3,H-.08,holes,RE)
 for s in (-1,1):
  facade_box(m,x,y,s*.39,.14,1.10,.76,.07,2.20,M['Blue'],a)
  for k in range(1,6):facade_box(m,x,y,s*.39-.38+k*.127,.19,1.10,.03,.02,2.10,M['Blue'],a)
 surround36(m,x,y,0,0,1.55,2.20,a,WF,.12,.42);facade_box(m,x,y,0,.46,2.38,1.90,.18,.10,WF,a)
flatroof102(m,'r196g',M['RoofDark'],RE)
fronts102(m,'r196c',lambda *_:False,RE,WF,WF,1);flatroof102(m,'r196c',M['RoofDark'],RE)
b102_finish(m,'93238196')

# ---- 93238164: the grey-green boarded house (e from the east end of the front).
m=b102_new(Z['g164']['mesh'],'Kvarnholmen/Storgatan');GG=M['GreyGreen']
A64,B64=(366.03,-0.40),(376.36,-0.80);H=Z['g164']['height']
for w in fronts102(m,'g164',NS,GG,WF,WF,2):
 x,y,L,a=sf_edge(w['p'],w['q']);S=lambda e:U(w,*pt102(B64,A64,e))
 ups=[(S(e),3.35,1.35,1.45) for e in (7.0,3.3,1.15)];downs=[(S(e),1.00,1.35,1.40) for e in (7.0,3.3)]
 du=S(1.05);holes=[(u,b,ww,hh,0) for u,b,ww,hh in ups+downs]+[(du,.30,1.15,2.30,0)]
 bz_wall(m,w['p'],w['q'],0,H,holes,GG);boards82(m,x,y,L,a,.50,H-.08,holes,GG)
 for u,b,ww,hh in ups+downs:win102(m,x,y,u,b,ww,hh,a,WF,WF,2,bw=.09)
 for u,b,ww,hh in ups:awning82(m,x,y,u,b+hh-.05,ww+.10,a,M['Awning'],.60,.55)
 # The pale panelled double door with a top light, on a step.
 door83(m,x,y,du,.30,1.15,2.00,a,M['Trim'],WF,glass=False);facade_box(m,x,y,du,.10,2.45,1.0,.02,.25,GLAZE,a)
 surround36(m,x,y,du,.30,1.15,2.30,a,WF,.14,.42);steps82(m,x,y,du,1.15,.30,a,M['Plinth'])
 facade_box(m,x,y,0,.40,.25,L+.02,.10,.50,M['PlinthDark'],a)
 corners102(m,x,y,L,a,.50,H,WF,.20)
 facade_box(m,x,y,0,.44,H-.10,L+.1,.12,.20,WF,a);town_rod(m,lp(x,y,-L/2,.70,H+.02,a),lp(x,y,L/2,.70,H+.02,a),.07,M['Sheet'],8)
saddle82(m,'g164',A64,B64,M['Tile'],GG,along=True)
X,Y=pt102(A64,B64,.8);chimney82(m,X,Y+3.6,Z['g164']['top']-.6,Z['g164']['top']+.6,M['Chimney'])
fronts102(m,'g164b',lambda *_:False,GG,WF,WF,1);flatroof102(m,'g164b',M['RoofDark'],GG)
b102_finish(m,'93238164')

# ---- 93238222: the cream corner house (south front on Storgatan, east front on Östra Vallgatan).
m=b102_new(Z['k222']['mesh'],'Kvarnholmen/Storgatan');H=Z['k222']['height']
for w in fronts102(m,'k222',lambda ox,oy,x,y:(oy<-.9 and y<1.5) or (ox>.9 and x>386),CR,WF,TR,2):
 x,y,L,a=sf_edge(w['p'],w['q']);n=4;us=[-L/2+(k+.5)*L/n for k in range(n)]
 ops=[(u,3.45,1.20,2.00) for u in us]+[(u,1.00,1.20,1.60) for u in us]
 holes=[(u,b,ww,hh,0) for u,b,ww,hh in ops]
 bz_wall(m,w['p'],w['q'],0,H,holes,CR)
 for u,b,ww,hh in ops:win102(m,x,y,u,b,ww,hh,a,WF,TR,3)
 facade_box(m,x,y,0,.40,.35,L+.02,.10,.70,M['Plinth'],a)
 facade_box(m,x,y,0,.42,2.95,L+.04,.14,.18,TR,a)
 corners102(m,x,y,L,a,.70,H-.3,CR,.45)
 facade_box(m,x,y,0,.46,H-.20,L+.10,.24,.40,TR,a)
r,sl=hip82(m,'k222',(376.36,-0.8),(387.06,-0.69),M['Tile'])
skylight82(m,381.0,1.65,H+2.8*sl,0.0,sl)
chimney82(m,382.5,4.4,Z['k222']['top']-.7,Z['k222']['top']+.7,M['Chimney'])
b102_finish(m,'93238222')

# ---- 93199630 (67): the ochre house (s from the east end of the front).
m=b102_new(Z['o630']['mesh'],'Kvarnholmen/Storgatan');OC=M['Ochre'];LE=M['Lesene']
A30,B30=(337.5,-11.98),(317.58,-12.01);H=Z['o630']['height']
for w in fronts102(m,'o630',SS,OC,WF,LE,2):
 x,y,L,a=sf_edge(w['p'],w['q']);S=lambda s:U(w,*pt102(A30,B30,s))
 ups=[(S(s),4.70,1.40,1.90) for s in (2.0,5.2,8.2,11.0,16.0,18.5)]
 downs=[(S(s),1.20,1.45,1.60) for s in (2.0,5.2,8.6,16.0,18.5)]+[(S(12.4),1.55,.80,1.05)]
 du=S(11.0);holes=[(u,b,ww,hh,0) for u,b,ww,hh in ups+downs]+[(du,.55,1.45,2.20,0)]
 bz_wall(m,w['p'],w['q'],0,H,holes,OC)
 for u,b,ww,hh in ups+downs:win102(m,x,y,u,b,ww,hh,a,WF,LE,3 if hh>1.2 else 2,bw=.14)
 door83(m,x,y,du,.55,1.45,2.20,a,M['DoorRed'],LE,glass=False)
 for s_ in (-1,1):facade_box(m,x,y,du+s_*.36,.20,.55+1.55,.42,.02,.55,GLAZE,a)
 steps82(m,x,y,du,1.45,.55,a,M['Plinth'])
 facade_box(m,x,y,0,.42,.52,L+.04,.14,1.05,M['Plinth'],a)
 # The lesene and the corner lesenes, the cornice band.
 facade_box(m,x,y,S(13.5),.44,(1.05+H)/2,1.20,.18,H-1.05,LE,a)
 for uu in (-L/2+.30,L/2-.30):facade_box(m,x,y,uu,.44,(1.05+H)/2,.60,.16,H-1.05,LE,a)
 facade_box(m,x,y,0,.48,H-.25,L+.12,.26,.50,LE,a);town_rod(m,lp(x,y,-L/2,.75,H+.02,a),lp(x,y,L/2,.75,H+.02,a),.07,M['Sheet'],8)
saddle82(m,'o630',B30,A30,M['Tile'],OC,along=True)
chimney82(m,327.0,-17.5,Z['o630']['top']-.8,Z['o630']['top']+.6,M['Chimney'])
b102_finish(m,'93199630')

# ---- 93199675: the garage range (s from the east end of the front).
m=b102_new(Z['p675']['mesh'],'Kvarnholmen/Storgatan');CO=M['Concrete'];GR=M['GarageRed']
A75,B75=(354.79,-12.40),(340.40,-12.19);H=Z['p675']['height']
for w in fronts102(m,'p675',SS,CO,WF,CO,1):
 x,y,L,a=sf_edge(w['p'],w['q']);S=lambda s:U(w,*pt102(A75,B75,s))
 pw=.45;dw=(L-6*pw)/5;dh=2.45;cs=[pw+dw/2+k*(dw+pw) for k in range(5)]
 holes=[(S(c),.12,dw,dh,0) for c in cs]
 bz_wall(m,w['p'],w['q'],0,H,holes,CO)
 for k,c in enumerate(cs):
  u=S(c)
  # Two leaves of chevron boarding: the boards drawn as diagonal battens in each leaf.
  facade_box(m,x,y,u,.10,.12+dh/2,dw,.06,dh,GR,a);facade_box(m,x,y,u,.15,.12+dh/2,.04,.03,dh,M['DoorRed'],a)
  for s_ in (-1,1):
   for j in range(6):
    zc=.12+.25+j*.38;h_=.30
    m.faces([lp(x,y,u+s_*.08,.135,zc,a),lp(x,y,u+s_*(dw/2-.08),.135,zc+h_,a),lp(x,y,u+s_*(dw/2-.08),.135,zc+h_+.06,a),lp(x,y,u+s_*.08,.135,zc+.06,a)],[(0,1,2,3),(3,2,1,0)],M['DoorRed'])
  if k<2:
   for q in range(4):facade_box(m,x,y,u-dw/2+(q+.5)*dw/4,.14,.12+dh-.55,dw/4-.20,.02,.42,GLAZE,a)
 # Piers standing proud of the doors, and the beam over them.
 for k in range(6):facade_box(m,x,y,S(pw/2+k*(dw+pw)),.48,(.12+dh)/2,pw,.26,.12+dh,CO,a)
 facade_box(m,x,y,0,.48,(.12+dh+H)/2,L+.04,.26,H-.12-dh,CO,a)
 facade_box(m,x,y,0,.80,.05,L+.6,.90,.10,CO,a)
hip82(m,'p675',A75,B75,M['Tile'])
fronts102(m,'p675b',lambda *_:False,CO,WF,CO,1);flatroof102(m,'p675b',M['RoofDark'],CO)
b102_finish(m,'93199675')

# ---- 93199606: the brick house; the east front on Östra Vallgatan measured, the Storgatan and west
# fronts given the same windows (seen only obliquely behind the garage range).
m=b102_new(Z['b606e']['mesh'],'Kvarnholmen/Östra Vallgatan');BR=M['Brick'];SH=M['Shutter']
def brick102(m,w,H,cols):
 x,y,L,a=sf_edge(w['p'],w['q'])
 ops=[(u,b,ww,hh) for u in cols for b,ww,hh in ((1.85,1.30,2.20),(5.55,1.25,1.90))]
 holes=[(u,b,ww,hh,0) for u,b,ww,hh in ops]
 bz_wall(m,w['p'],w['q'],0,H,holes,BR)
 for u,b,ww,hh in ops:
  cas81(m,x,y,u,b,ww,hh,a,WF,.18,3);surround36(m,x,y,u,b,ww,hh,a,WF,.08,.40)
  facade_box(m,x,y,u,.46,b-.05,ww+.20,.18,.08,M['Stone'],a)
  for s_ in (-1,1):facade_box(m,x,y,u+s_*(ww/2+.36),.44,b+hh/2,.60,.05,hh+.05,SH,a)
 facade_box(m,x,y,0,.43,.60,L+.06,.16,1.20,M['Stone'],a)
 for k in range(int(L/.9)):facade_box(m,x,y,-L/2+(k+.5)*L/int(L/.9),.515,.60,.02,.01,1.15,M['Plinth'],a)
 facade_box(m,x,y,0,.515,.60,L+.06,.01,.03,M['Plinth'],a)
 facade_box(m,x,y,0,.40,4.98,L+.02,.10,.22,M['BrickBand'],a)
 facade_box(m,x,y,0,.40,H-.35,L+.02,.10,.55,M['Frieze'],a)
 facade_box(m,x,y,0,.44,H-.04,L+.10,.16,.10,M['Frieze'],a)
 for uu in (-L/2+.15,L/2-.15):facade_box(m,x,y,uu,.42,(1.2+H-.6)/2,.30,.10,H-1.8,BR,a)
for zone in ('b606e','b606w'):
 H=Z[zone]['height']
 for w in walls(zone):
  if w['kind']!='outer' and w['z0']>3:bz_wall(m,w['p'],w['q'],w['z0'],H,[],BR);continue
  L=math.dist(w['p'],w['q']);n=max(1,round(L/3.75));brick102(m,w,H,[-L/2+(k+.5)*L/n for k in range(n)])
 rr,sl=hip82(m,zone,*((( 386.73,-27.06),(386.68,-12.06)) if zone=='b606e' else ((364.5,-12.11),(378.3,-12.08))),M['Copper'])
# The deep eaves: a dark soffit board ringing both blocks at the eaves.
for zone in ('b606e','b606w'):
 for w in walls(zone,'outer'):
  x,y,L,a=sf_edge(w['p'],w['q']);facade_box(m,x,y,0,.62,Z[zone]['height']+.02,L+.9,.70,.06,M['RoofDark'],a)
# The low walled part west of the house: brick walls with a coping, a flat roof.
for w in walls('b606y'):
 x,y,L,a=sf_edge(w['p'],w['q']);bz_wall(m,w['p'],w['q'],w['z0'],Z['b606y']['height'],[],BR)
 if w['kind']=='outer':facade_box(m,x,y,0,.40,Z['b606y']['height']-.06,L+.04,.16,.12,M['Stone'],a)
flatroof102(m,'b606y',M['RoofDark'],BR)
chimney82(m,382.5,-19.0,Z['b606e']['top']-.6,Z['b606e']['top']+.8,M['Chimney'])
b102_finish(m,'93199606')

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block102_cameras=[
 sv_camera('499_Block102_Cal_Dormers',348.30,-6.50,2.10,332,15,90),
 sv_camera('500_Block102_Cal_RedGables',366.95,-9.21,2.28,332,15,90),
 sv_camera('501_Block102_Cal_Ochre',322.63,-7.80,2.30,152,15,90),
  sv_camera('502_Block102_Cal_Brick',394.49,-20.04,2.28,242,15,90),
 ('503_Block102_Aerial',(356.0,-48.0,34.0),(356.0,-8.0,2.0),28),
]
print('BLOCK102_GEOMETRY',len(block102_names),'dropped',block102_dropped,block102_samples)
