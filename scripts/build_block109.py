"""Pass 109: generic pass-17 volumes in the north-west of Kvarnholmen:
- 92204179 (38 Larmgatan): a small falu-red boarded outbuilding with a flat-topped street wall to
  Larmgatan on a low stone plinth, its low saddle roof hidden behind the wall top (estimated);
- 92204177 (40 Larmgatan): a 1950s three-storey office block in cream render with red-brown brick
  bands between continuous dark window ribbons, shop windows under a long canvas awning, a thin
  dark roof slab and a brick lift house on the flat roof; the two-storey wing to the south with
  the navy 'Ludvig & Co' fascia over its glazed door and shop windows, an ochre brick band under
  the upper window ribbon, and a flat roof;
- 92204174 (1 Strömgatan): an ochre rendered two-storey street range on a grey plinth: shop
  windows under navy fascias, two (and an unseen third) white door surrounds with pediments,
  boarded-up windows, a cornice and a dark sheet saddle roof with small gabled red dormers; the
  cream three-storey west end with round-headed top windows and a low hipped roof; flat-roofed
  back ranges (not seen);
- 886305409 (50 Larmgatan): the round office drum, 19 facets of glass and light and dark grey
  panels in a chequer, vertical fins, floor bands, a parapet and a flat roof;
- 91846958 (4 Norra Långgatan): a cream rendered three-storey corner house on a tall grey plinth,
  green window frames, the green door with a glazed top light, the chamfered corner, a dark
  hipped roof; its south wing flat-roofed (not seen);
- 91846925: a grey boarded two-storey house with white corner boards and pilasters, red window
  frames, a dark plinth and a saddle roof; the white rendered gateway with the red gate between it
  and the corner house;
- 91846945: the block between Norra Långgatan, Larmgatan and Västra Vallgatan, generic: plain
  rendered three-storey walls with simple windows and a flat roof (no usable photo).

References: Google Street View (six panoramas, resected on house corners and the drum's
silhouette), view only. Zones: source/block109.json; see references/block109-notes.md. Signs,
lamps, flags, pipes other than the one downpipe on 1 Strömgatan, cars and planting are omitted.
"""
B109D=json.loads((R/'source/block109.json').read_text());Z=B109D['zones']
block109_names=[];B109={}
for old in [k for k in list(materials) if k.startswith('M_Block109_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Red','TownPaintBrown',(.55,.15,.12),.80,0),('Stone','TownStone',(.52,.52,.50),.90,0),('Tile','TownTileRed',(.70,.36,.25),.80,0),
 ('Cream','TownIvory',(.86,.83,.74),.85,0),('Brick','TownTileRed',(.50,.26,.19),.88,0),('WinDark','TownMetalGrey',(.14,.13,.12),.50,.20),
 ('Canvas','TownPaintWhite',(.84,.82,.76),.80,0),('BrickYel','TownIvory',(.72,.60,.38),.90,0),('Navy','TownPaintWhite',(.12,.17,.32),.55,0),
 ('Ochre','TownIvory',(.80,.68,.45),.92,0),('Cream3','TownIvory',(.86,.80,.62),.90,0),('Trim','TownPaintWhite',(.90,.89,.85),.65,0),
 ('Plinth','TownStone',(.45,.46,.46),.90,0),('DoorGrey','TownPaintWhite',(.72,.72,.68),.60,0),('DormerRed','TownPaintBrown',(.50,.18,.15),.65,0),
 ('BoardUp','TownPaintBrown',(.55,.50,.44),.85,0),
 ('PanelLight','TownMetalGrey',(.70,.72,.73),.45,.30),('PanelDark','TownMetalGrey',(.36,.38,.40),.45,.30),('Fin','TownMetalGrey',(.60,.62,.64),.45,.35),
 ('Cream958','TownIvory',(.88,.86,.79),.85,0),('Green','TownPaintGreen',(.30,.45,.30),.60,0),('DoorGreen','TownPaintGreen',(.36,.53,.38),.60,0),
 ('Plinth958','TownStone',(.50,.50,.49),.90,0),
 ('GreyBoard','TownPaintWhite',(.62,.63,.60),.80,0),('WinRed','TownPaintBrown',(.45,.12,.10),.60,0),('White','TownPaintWhite',(.93,.93,.91),.55,0),
 ('DarkPlinth','TownStone',(.30,.30,.30),.90,0),('GateRed','TownPaintBrown',(.55,.16,.13),.60,0),('Gateway','TownIvory',(.89,.88,.84),.85,0),
 ('MutedTile','TownTileRed',(.55,.36,.29),.85,0),
 ('Render945','TownIvory',(.84,.78,.64),.90,0),
 ('Sheet','TownMetalGrey',(.22,.22,.23),.55,.30),('Flat','TownMetalGrey',(.30,.30,.31),.70,.20),('Chimney','TownTileRed',(.55,.33,.27),.85,0),
 ('Dark','TownMetalGrey',(.06,.06,.065),.45,.40),
 ]:
 name='M_Block109_'+key;B109[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block109_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
# chimney82 and the pass-82/83 helpers read the globals M and Z.
M=B109

def b109_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block109_names.append(name);return Mesh(name,category)
def drop_degenerate_faces109(obj,tol=1e-9):
 import bmesh
 bm=bmesh.new();bm.from_mesh(obj.data)
 def _thin(f):
  L=max(e.calc_length() for e in f.edges);return L>0 and 2*f.calc_area()/L<1e-4
 bad=[f for f in bm.faces if f.calc_area()<tol or len({v.index for v in f.verts})<len(f.verts) or _thin(f)]
 block109_samples[obj.name]=[tuple(round(c,2) for c in f.calc_center_median()) for f in bad[:4]]
 if bad:bmesh.ops.delete(bm,geom=bad,context='FACES_ONLY')
 bm.to_mesh(obj.data);bm.free();obj.data.update();return len(bad)
block109_dropped={};block109_samples={}
def b109_finish(m,osm):
 obj=s21_finish(m);block109_dropped[obj.name]=drop_degenerate_faces109(obj)
 obj['detail_pass']=109;obj['reference_notes']='references/block109-notes.md';obj['osm_way']=osm;return obj

def pt109(a,b,s,t=0.0):
 # The point s metres from a towards b, and t metres to the right of a->b (outwards on a front).
 L=math.dist(a,b);d=((b[0]-a[0])/L,(b[1]-a[1])/L);return (a[0]+d[0]*s+d[1]*t,a[1]+d[1]*s-d[0]*t)
def on109(A,B):
 # Test: an outer wall lies on the street front A->B (same direction, within 0.6 m of the line).
 L=math.dist(A,B);d=((B[0]-A[0])/L,(B[1]-A[1])/L)
 def t(w):
  x,y,Lw,a=sf_edge(w['p'],w['q'])
  return math.cos(a)*d[0]+math.sin(a)*d[1]>.99 and abs((x-A[0])*d[1]-(y-A[1])*d[0])<.6
 return t
def fronts109(m,zone,test,wall,frame,trim,levels,floor0=1.0,ma_upper=None):
 # Party and upper walls in the wall material, unseen outer walls plain; returns the street fronts.
 H=Z[zone]['height'];out=[]
 for w in walls(zone):
  if w['kind']!='outer':bz_wall(m,w['p'],w['q'],w['z0'],H,[],ma_upper or wall);continue
  if test(w):out.append(w);continue
  plain(m,w,H,wall,frame,trim,levels,floor0)
 return out
def flatroof109(m,zone,ma,trim,lip=.24,o=.38):
 H=Z[zone]['height']
 for g in Z[zone]['polygons']:m.faces([(*v,H+.02) for v in g],[tuple(range(len(g))),tuple(range(len(g)-1,-1,-1))],ma)
 for w in walls(zone,'outer'):
  x,y,L,a=sf_edge(w['p'],w['q']);facade_box(m,x,y,0,o,H+lip/2,L+.06,.12,lip,trim,a)
def win109(m,x,y,u,b,w,h,a,frame,sur=None,rows=3,o=.16,bw=.10,sill=None):
 # Casement in its frame, an optional flat surround and a sill.
 cas81(m,x,y,u,b,w,h,a,frame,o,rows)
 if sur:surround36(m,x,y,u,b,w,h,a,sur,bw,.40)
 facade_box(m,x,y,u,.47,b-.05,w+.20,.16,.06,sill or sur or frame,a)
def ribbon109(m,x,y,u0,u1,b,h,a,n,frame,o=.24):
 # A continuous window band: glass behind n equal panes, mullions and rails in the frame colour.
 w=u1-u0;facade_box(m,x,y,(u0+u1)/2,o-.04,b+h/2,w,.02,h,GLAZE,a)
 for k in range(n+1):facade_box(m,x,y,u0+k*w/n,o,b+h/2,.10 if k in (0,n) else .07,.08,h,frame,a)
 for zz in (b+.04,b+h-.04):facade_box(m,x,y,(u0+u1)/2,o,zz,w,.08,.08,frame,a)
def pediment109(m,x,y,u,z,w,rise,a,ma):
 # Triangular pediment over a door: a solid prism standing on the wall, a raking cornice.
 tri=[(u-w/2,z),(u+w/2,z),(u,z+rise)];vs=[lp(x,y,uu,o,zz,a) for o in (.355,.62) for uu,zz in tri]
 m.faces(vs,[(2,1,0),(3,4,5),(0,1,4,3),(1,2,5,4),(2,0,3,5)],ma)
 for (u0,z0),(u1,z1) in ((tri[0],tri[2]),(tri[2],tri[1])):town_rod(m,lp(x,y,u0,.66,z0+.04,a),lp(x,y,u1,.66,z1+.04,a),.06,ma,6)
def gdormer109(m,X,Y,ang,zb,w,h,dep,rise,body,roof,frame):
 # A small gabled dormer: a box body (front face at X,Y facing along ang's outward normal), a
 # gable prism over it and a saddle lid running back into the roof, a two-pane window.
 x,y=X,Y;box(m,*lp(x,y,0,-dep/2,0,ang)[:2],w,dep,h,zb,body,ang)
 g=[(-w/2-.08,zb+h),(w/2+.08,zb+h),(0,zb+h+rise)]
 vs=[lp(x,y,uu,o,zz,ang) for o in (.10,-dep) for uu,zz in g]
 m.faces(vs,[(2,1,0),(3,4,5),(1,2,5,4),(2,0,3,5),(0,1,4,3)],body)
 for s in (-1,1):m.faces([lp(x,y,s*(w/2+.15),.14,zb+h-.06,ang),lp(x,y,0,.14,zb+h+rise+.04,ang),lp(x,y,0,-dep,zb+h+rise+.04,ang),lp(x,y,s*(w/2+.15),-dep,zb+h-.06,ang)],[(0,1,2,3),(3,2,1,0)],roof)
 facade_box(m,x,y,0,.02,zb+.2+(h-.35)/2,w-.30,.02,h-.35,GLAZE,ang);cas81(m,x,y,0,zb+.2,w-.30,h-.35,ang,frame,.06,2)

# ---- 92204179 (38 Larmgatan): the red boarded outbuilding.
m=b109_new(Z['r179']['mesh'],'Kvarnholmen/Larmgatan');RE=M['Red']
A,B=(-283.53,165.46),(-283.61,159.47);H=Z['r179']['height']
for w in walls('r179'):
 x,y,L,a=sf_edge(w['p'],w['q']);z0=w['z0']
 bz_wall(m,w['p'],w['q'],z0,H,[],RE);boards82(m,x,y,L,a,max(z0,.25),H-.08,[],RE)
 if w['kind']=='outer':
  facade_box(m,x,y,0,.39,.12,L+.02,.08,.24,M['Stone'],a);facade_box(m,x,y,0,.44,H-.05,L+.12,.16,.10,RE,a)
  for uu in (-L/2+.07,L/2-.07):facade_box(m,x,y,uu,.42,H/2,.14,.08,H,RE,a)
saddle82(m,'r179',A,B,M['Tile'],RE,along=True)
b109_finish(m,'92204179')

# ---- 92204177 (40 Larmgatan): the office block and its wing (s from the north corner).
A7,J7,B7=(-283.06,206.4),(-283.08,194.8),(-283.12,176.66)
m=b109_new(Z['o177']['mesh'],'Kvarnholmen/Larmgatan');CR=M['Cream'];BR=M['Brick'];WD=M['WinDark']
H=Z['o177']['height']
def office109(w,street):
 x,y,L,a=sf_edge(w['p'],w['q'])
 if L<3.0:bz_wall(m,w['p'],w['q'],0,H,[],CR);return
 u0,u1=-L/2+(1.2 if street else 1.0),L/2-(.6 if street else 1.0)
 gh=[(u,.45,ww,2.35,0) for u,ww in street] if street else [((u0+u1)/2,1.0,u1-u0,1.6,0)]
 holes=gh+[((u0+u1)/2,4.55,u1-u0,1.35,0),((u0+u1)/2,7.50,u1-u0,1.30,0)]
 bz_wall(m,w['p'],w['q'],0,H,holes,CR)
 n=max(2,round((u1-u0)/1.38))
 ribbon109(m,x,y,u0,u1,4.55,1.35,a,n,WD);ribbon109(m,x,y,u0,u1,7.50,1.30,a,n,WD)
 for u,b,ww,hh,r in gh:ribbon109(m,x,y,u-ww/2,u+ww/2,b,hh,a,2 if street else n,WD,.20)
 # Brick bands in the window bays, laid proud of the render; plinth; roof slab edge.
 for z0,z1 in ((3.26,4.55),(5.90,7.50)):facade_box(m,x,y,(u0+u1)/2,.38,(z0+z1)/2,u1-u0,.06,z1-z0,BR,a)
 facade_box(m,x,y,0,.39,.22,L+.02,.08,.45,M['Stone'],a)
 facade_box(m,x,y,0,.62,H+.06,L+.90,.60,.14,M['Sheet'],a)
 return x,y,L,a
for w in walls('o177'):
 if w['kind']!='outer':bz_wall(m,w['p'],w['q'],w['z0'],H,[],CR);continue
 if on109(A7,J7)(w):
  S=lambda s:U(w,*pt109(A7,J7,s));shops=[(S((s0+s1)/2),s1-s0) for s0,s1 in ((2.0,4.6),(5.0,7.8),(8.2,10.7))]
  x,y,L,a=office109(w,shops)
  # The corner pier ground floor and the long canvas awning over the shop windows.
  awning82(m,x,y,S(5.8),2.75,10.2,a,M['Canvas'],.50,1.40)
 else:office109(w,None)
flatroof109(m,'o177',M['Flat'],M['Sheet'],.14,.60)
# The brick lift house on the roof, set back from the Larmgatan front.
X,Y=pt109(A7,J7,6.2,-1.7);box(m,X,Y,3.0,3.8,2.5,H,BR,0,M['Sheet'])
fw=[w for w in walls('o177','outer') if on109(A7,J7)(w)][0];x,y,L,a=sf_edge(fw['p'],fw['q'])
for s in (5.0,7.4):
 X,Y=pt109(A7,J7,s,-.19);facade_box(m,X,Y,0,0,H+1.45,.9,.02,.60,GLAZE,a)
m2=m
# The wing: s from the joint with the office block.
m=m2;HW=Z['w177']['height']
for w in fronts109(m,'w177',on109(J7,B7),CR,WD,CR,2,1.0):
 x,y,L,a=sf_edge(w['p'],w['q']);S=lambda s:U(w,*pt109(J7,B7,s))
 shops=[(.3,3.0,0,2.75),(4.2,6.9,.45,2.30),(9.7,12.8,.45,2.30),(13.4,17.4,.45,2.30)]
 holes=[(S((s0+s1)/2),b,s1-s0,hh,0) for s0,s1,b,hh in shops]+[(S(1.43),4.47,2.12,1.38,0),(S(10.6),4.55,13.9,1.35,0)]
 bz_wall(m,w['p'],w['q'],0,HW,holes,CR)
 ribbon109(m,x,y,S(.37),S(2.49),4.47,1.38,a,2,WD);ribbon109(m,x,y,S(3.65),S(17.55),4.55,1.35,a,11,WD)
 for s0,s1,b,hh in shops:ribbon109(m,x,y,S(s0),S(s1),b,hh,a,2 if s1-s0<3.5 else 3,WD,.20)
 # Glazed door in the first bay, the navy fascia, the ochre brick band, plinth, roof slab edge.
 facade_box(m,x,y,S(1.65),.20,1.25,.08,.06,2.5,WD,a)
 facade_box(m,x,y,(S(.2)+S(8.6))/2,.55,3.10,abs(S(8.6)-S(.2)),.40,.65,M['Navy'],a)
 facade_box(m,x,y,(S(3.0)+S(18.15))/2,.38,3.98,abs(S(18.15)-S(3.0)),.06,1.13,M['BrickYel'],a)
 facade_box(m,x,y,S(3.0),.42,HW/2,.30,.14,HW,CR,a)
 facade_box(m,x,y,0,.39,.22,L+.02,.08,.45,M['Stone'],a)
 facade_box(m,x,y,0,.62,HW+.06,L+.90,.60,.14,M['Sheet'],a)
flatroof109(m,'w177',M['Flat'],M['Sheet'],.14,.60)
b109_finish(m,'92204177')

# ---- 92204174 (1 Strömgatan): s from the west corner on Larmgatan.
A4,B4=(-282.93,218.51),(-253.72,218.48)
m=b109_new(Z['sf174']['mesh'],'Kvarnholmen/Strömgatan');OC=M['Ochre'];C3=M['Cream3'];TR=M['Trim']
# The west end: three storeys, round-headed top windows (the left one on Larmgatan estimated).
H=Z['sw174']['height']
for w in fronts109(m,'sw174',on109(A4,B4),C3,TR,TR,3,1.0,OC):
 x,y,L,a=sf_edge(w['p'],w['q']);S=lambda s:U(w,*pt109(A4,B4,s))
 ups=[(S(s),4.45,1.10,1.76,0) for s in (1.0,3.07,5.26)];tops=[(S(s),8.40,1.0,1.05,.45) for s in (1.0,2.92,5.13)]
 shops=[(S(2.1),.80,2.4,2.5,0),(S(5.63),.80,2.66,2.5,0)]
 bz_wall(m,w['p'],w['q'],0,H,ups+tops+shops,C3)
 for u,b,ww,hh,r in ups:win109(m,x,y,u,b,ww,hh,a,TR,None,3,sill=TR)
 for u,b,ww,hh,r in tops:p18_win(m,x,y,u,b,ww,hh,r,a,TR,TR,2,2)
 for u,b,ww,hh,r in shops:ribbon109(m,x,y,u-ww/2,u+ww/2,b,hh,a,1,M['Navy'],.20);facade_box(m,x,y,u,.45,3.45,ww+.2,.14,.25,M['Navy'],a)
 facade_box(m,x,y,0,.40,.27,L+.02,.10,.55,M['Plinth'],a);facade_box(m,x,y,0,.48,7.95,L+.06,.24,.50,TR,a)
 facade_box(m,x,y,0,.52,H-.15,L+.10,.30,.30,TR,a)
 for k in range(int((H-.6)/.45)):facade_box(m,x,y,-L/2+.30 if k%2==0 else -L/2+.22,.40,.6+(k+.5)*.45,.60 if k%2==0 else .44,.08,.40,TR,a)
hip82(m,'sw174',A4,B4,M['Sheet'])
# The street range.
H=Z['sf174']['height']
DOORS=[(10.28,1.48,.30,2.68),(14.77,1.84,.25,2.74),(23.6,1.60,.30,2.68)]
SHOPS=[(7.11,9.30),(11.51,13.48),(25.2,27.9)];BOARD=[(16.43,17.72),(19.19,21.29)]
UPS=[7.94,10.14,12.6,14.64,17.34,20.1,22.48,25.0,27.4]
for w in fronts109(m,'sf174',on109(A4,B4),OC,TR,TR,2,1.0):
 x,y,L,a=sf_edge(w['p'],w['q']);S=lambda s:U(w,*pt109(A4,B4,s))
 holes=[(S(s),b,ww,hh,0) for s,ww,b,hh in DOORS]+[(S((s0+s1)/2),.80,s1-s0,2.50,0) for s0,s1 in SHOPS+BOARD]+[(S(s),4.45,1.15,1.76,0) for s in UPS]
 holes=[h for h in holes if abs(h[0])+h[2]/2<=L/2+.01]
 bz_wall(m,w['p'],w['q'],0,H,holes,OC)
 for s in UPS:win109(m,x,y,S(s),4.45,1.15,1.76,a,TR,None,3,sill=TR)
 for s0,s1 in SHOPS:
  u=S((s0+s1)/2);ribbon109(m,x,y,u-(s1-s0)/2,u+(s1-s0)/2,.80,2.50,a,2,M['Navy'],.20);facade_box(m,x,y,u,.45,3.42,s1-s0+.20,.14,.20,M['Navy'],a)
 for s0,s1 in BOARD:
  u=S((s0+s1)/2);facade_box(m,x,y,u,.26,2.05,s1-s0,.04,2.50,M['BoardUp'],a);surround36(m,x,y,u,.80,s1-s0,2.50,a,M['BoardUp'],.06,.38)
 for s,ww,b,hh in DOORS:
  # Panelled double doors with a top light, flat white pilasters, an entablature and a pediment.
  u=S(s);door83(m,x,y,u,b,ww,hh-.45,a,M['DoorGrey'],TR,glass=False)
  facade_box(m,x,y,u,.12,b+hh-.22,ww,.02,.36,GLAZE,a);facade_box(m,x,y,u,.18,b+hh-.45,ww,.06,.06,TR,a)
  for sg in (-1,1):facade_box(m,x,y,u+sg*(ww/2+.17),.42,(b+hh+.05)/2,.30,.14,b+hh+.05,TR,a)
  facade_box(m,x,y,u,.46,b+hh+.30,ww+.80,.22,.50,TR,a);pediment109(m,x,y,u,b+hh+.58,ww+.95,.66,a,TR)
  facade_box(m,x,y,u,.36+.35,.10,ww+.5,.70,.20,M['Plinth'],a)
 # Plinth (broken at the doors), the cornice, the downpipe at the west end's joint.
 at=-L/2
 for lo,hi in sorted((S(s)-ww/2-.05,S(s)+ww/2+.05) for s,ww,b,hh in DOORS)+[(L/2,L/2)]:
  lo=max(-L/2,min(L/2,lo))
  if lo>at+.05:facade_box(m,x,y,(at+lo)/2,.40,.27,lo-at,.10,.55,M['Plinth'],a)
  at=max(at,min(L/2,hi))
 facade_box(m,x,y,0,.48,7.95,L+.06,.24,.50,TR,a);facade_box(m,x,y,0,.58,H-.10,L+.20,.40,.22,TR,a)
 town_rod(m,lp(x,y,S(6.68),.50,.25,a),lp(x,y,S(6.68),.50,8.0,a),.06,TR,8)
r,Ls,Lt=rect82('sf174',(-276.2,218.5),B4);saddle82(m,'sf174',(-276.2,218.5),B4,M['Sheet'],OC,along=True)
sl=(Z['sf174']['top']-H)/(Lt/2)
for s in (12.6,18.55):
 X,Y=pt109(A4,B4,s,.355-1.0);gdormer109(m,X,Y,math.atan2(B4[1]-A4[1],B4[0]-A4[0]),H+1.0*sl+.15,1.40,1.45,2.2,.65,M['DormerRed'],M['DormerRed'],TR)
X,Y=pt109(A4,B4,21.0,-6.0);chimney82(m,X,Y,Z['sf174']['top']-.6,Z['sf174']['top']+.8,M['Chimney'])
# The party wall up to the east neighbour's wall foot (pass 105 builds its wall from 9.75).
bz_wall(m,(-253.59,229.0),(-253.72,218.48),H,9.75,[],OC)
# The back ranges (not seen): plain two-storey render under a flat roof.
fronts109(m,'sb174',lambda w:False,OC,TR,TR,2,1.0);flatroof109(m,'sb174',M['Sheet'],TR)
b109_finish(m,'92204174')

# ---- 886305409 (50 Larmgatan): the round drum.
m=b109_new(Z['d886']['mesh'],'Kvarnholmen/Larmgatan');H=Z['d886']['height']
BANDS=[(.40,1.80),(2.45,2.50),(5.30,2.55),(8.25,.85)]
for i,w in enumerate(walls('d886','outer')):
 x,y,L,a=sf_edge(w['p'],w['q']);holes=[]
 for k,(b,hh) in enumerate(BANDS):
  for j,u in enumerate((-L/4,L/4)):holes.append((u,b,L/2-.30,hh,0))
 bz_wall(m,w['p'],w['q'],0,H,holes,M['PanelLight'])
 for k,(b,hh) in enumerate(BANDS):
  for j,u in enumerate((-L/4,L/4)):
   if (i+j+k)%2==0 or k==3:
    facade_box(m,x,y,u,.24,b+hh/2,L/2-.30,.02,hh,GLAZE,a)
    for zz in (b+.04,b+hh-.04)+((b+hh*.62,) if hh>2 else ()):facade_box(m,x,y,u,.29,zz,L/2-.30,.06,.06,M['Fin'],a)
   else:facade_box(m,x,y,u,.30,b+hh/2,L/2-.30,.04,hh,M['PanelDark'] if (i+k)%2 else M['PanelLight'],a)
 facade_box(m,x,y,-L/2,.50,H/2,.10,.30,H,M['Fin'],a)
 for zz in (.20,2.32,5.17,8.13):facade_box(m,x,y,0,.40,zz,L+.06,.12,.22,M['Fin'],a)
 facade_box(m,x,y,0,.42,H-.12,L+.08,.16,.24,M['PanelDark'],a)
flatroof109(m,'d886',M['Flat'],M['Fin'],.18,.42)
b109_finish(m,'886305409')

# ---- 91846958 (4 Norra Långgatan): s from the east corner of the street front.
A8,B8,C8=(-323.13,64.4),(-330.7,64.96),(-334.36,61.73)
m=b109_new(Z['c958']['mesh'],'Storgatan/Buildings');CM=M['Cream958'];GN=M['Green']
H=Z['c958']['height'];ROWS=[(2.10,1.50),(5.00,1.70),(8.00,1.60)]
def plinth958(x,y,L,a,cut=()):
 at=-L/2
 for lo,hi in sorted(cut)+[(L/2,L/2)]:
  if lo>at+.05:facade_box(m,x,y,(at+lo)/2,.40,.55,lo-at,.10,1.10,M['Plinth958'],a)
  at=max(at,hi)
for w in fronts109(m,'c958',lambda w:on109(A8,B8)(w) or on109(B8,C8)(w),CM,GN,CM,3,2.1):
 x,y,L,a=sf_edge(w['p'],w['q'])
 if on109(A8,B8)(w):
  S=lambda s:U(w,*pt109(A8,B8,s));cols=[1.31,3.64,5.69];du=S(5.62)
  holes=[(S(s),b,1.08,hh,0) for s in cols for k,(b,hh) in enumerate(ROWS) if not (k==0 and s==5.69)]+[(du,.15,1.02,3.40,0)]
  bz_wall(m,w['p'],w['q'],0,H,holes,CM)
  for u,b,ww,hh,r in holes[:-1]:win109(m,x,y,u,b,ww,hh,a,GN,None,2,sill=GN)
  # The green boarded door with a glazed top light.
  facade_box(m,x,y,du,.14,1.20,1.02,.07,2.10,M['DoorGreen'],a)
  for k in range(8):facade_box(m,x,y,du,.19,.30+k*.26,.96,.02,.03,GN,a)
  facade_box(m,x,y,du,.12,2.90,.90,.02,1.15,GLAZE,a);cas81(m,x,y,du,2.32,1.02,1.20,a,GN,.17,1)
  plinth958(x,y,L,a,[(du-.56,du+.56)])
 else:
  S=lambda s:U(w,*pt109(B8,C8,s));holes=[(S(s),b,1.0,hh,0) for s in (1.25,3.65) for b,hh in ROWS]
  bz_wall(m,w['p'],w['q'],0,H,holes,CM)
  for u,b,ww,hh,r in holes:win109(m,x,y,u,b,ww,hh,a,GN,None,2,sill=GN)
  plinth958(x,y,L,a)
 facade_box(m,x,y,0,.48,H-.18,L+.10,.26,.36,CM,a)
for w in walls('c958','outer'):
 if not (on109(A8,B8)(w) or on109(B8,C8)(w)):x,y,L,a=sf_edge(w['p'],w['q']);facade_box(m,x,y,0,.48,H-.18,L+.10,.26,.36,CM,a)
# Hipped roof over the outline with the chamfer, a short flat top.
ring=[(-323.13,64.4),(-330.7,64.96),(-334.36,61.73),(-336.45,52.48),(-336.52,50.9),(-323.51,50.92)]
if sum(p[0]*q[1]-q[0]*p[1] for p,q in zip(ring,ring[1:]+ring[:1]))<0:ring=ring[::-1]
inset_roof(m,ring,H,4.6,Z['c958']['top']-H,M['Sheet'],.40)
X,Y=(-327.0,57.0);chimney82(m,X,Y,Z['c958']['top']-.8,Z['c958']['top']+.6,M['Chimney'])
fronts109(m,'w958',lambda w:False,CM,GN,CM,3,2.1);flatroof109(m,'w958',M['Sheet'],CM)
b109_finish(m,'91846958')

# ---- 91846925: the grey boarded house (s from its east corner) and the gateway to the west.
A5,B5=(-309.52,64.13),(-320.0,64.18)
m=b109_new(Z['g925']['mesh'],'Storgatan/Buildings');GB=M['GreyBoard'];WR=M['WinRed'];WH=M['White']
H=Z['g925']['height'];COLS=[2.36,4.41,7.02,9.37]
for w in fronts109(m,'g925',on109(A5,B5),GB,WR,WH,2,1.0):
 x,y,L,a=sf_edge(w['p'],w['q']);S=lambda s:U(w,*pt109(A5,B5,s))
 holes=[(S(s),b,1.00,hh,0) for s in COLS for b,hh in ((1.60,1.35),(4.02,1.50))]
 bz_wall(m,w['p'],w['q'],0,H,holes,GB);boards82(m,x,y,L,a,.90,H-.45,holes,GB)
 for u,b,ww,hh,r in holes:win109(m,x,y,u,b,ww,hh,a,WR,WH,2,bw=.12)
 facade_box(m,x,y,0,.39,.33,L+.02,.08,.65,M['DarkPlinth'],a);facade_box(m,x,y,0,.43,.78,L+.04,.10,.22,WH,a)
 facade_box(m,x,y,0,.43,3.30,L+.04,.10,.22,WH,a);facade_box(m,x,y,0,.43,H-.22,L+.04,.10,.44,WH,a)
 for s in (.10,3.40,5.72,8.20,10.38):facade_box(m,x,y,S(s),.44,(H+.65)/2,.26,.10,H-.65,WH,a)
for w in walls('g925','outer'):
 if not on109(A5,B5)(w):
  x,y,L,a=sf_edge(w['p'],w['q']);boards82(m,x,y,L,a,.90,H-.30,[],GB)
saddle82(m,'g925',A5,B5,M['MutedTile'],GB,along=True)
X,Y=pt109(A5,B5,3.4,-4.5);chimney82(m,X,Y,Z['g925']['top']-.6,Z['g925']['top']+.7,M['Chimney'])
# The gateway: white rendered posts and lintel across the 3.1 m gap, the red gate leaf on the west
# half, the east half open to the yard.
gw={'p':[-320.0,64.18],'q':[-323.13,64.40]};x,y,L,a=sf_edge(gw['p'],gw['q']);GW=M['Gateway']
for u in (-L/2+.55,L/2-.55):facade_box(m,x,y,u,.20,1.40,.36,.30,2.80,GW,a)
facade_box(m,x,y,0,.20,2.68,L-.74,.30,.30,GW,a);facade_box(m,x,y,0,.24,2.88,L-.60,.40,.10,GW,a)
gu=U(gw,-322.35,64.35);facade_box(m,x,y,gu,.18,1.27,1.25,.06,2.50,M['GateRed'],a)
for zz in (.40,1.30,2.20):facade_box(m,x,y,gu,.22,zz,1.10,.03,.08,M['GateRed'],a)
b109_finish(m,'91846925')

# ---- 91846945: generic (no usable photo).
m=b109_new(Z['b945']['mesh'],'Kvarnholmen/Västra Vallgatan');RN=M['Render945'];H=Z['b945']['height']
fronts109(m,'b945',lambda w:False,RN,WH,WH,3,1.0)
for w in walls('b945','outer'):
 x,y,L,a=sf_edge(w['p'],w['q']);facade_box(m,x,y,0,.46,H-.20,L+.10,.22,.40,WH,a)
flatroof109(m,'b945',M['Sheet'],RN)
b109_finish(m,'91846945')

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block109_cameras=[
 sv_camera('538_Block109_Cal_Office',-290.85,193.81,2.30,61,15,90),
 sv_camera('539_Block109_Cal_Stromgatan',-270.82,213.17,2.30,333,15,90),
 sv_camera('540_Block109_Cal_Corner',-330.52,69.57,2.05,152,15,90),
 sv_camera('541_Block109_Cal_Drum',-268.75,308.41,2.00,86,15,90),
 ('542_Block109_Aerial',(-345.0,160.0,70.0),(-290.0,170.0,4.0),28),
]
print('BLOCK109_GEOMETRY',len(block109_names),'dropped',block109_dropped,block109_samples)
