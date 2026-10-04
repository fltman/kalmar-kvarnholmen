"""Pass 100: the north side of east Norra Långgatan (78-84) and the grey cottage on Östra Vallgatan:
- 93238210: the grey boarded corner cottage at Landshövdingegatan (gable to the street, one window
  with white shutters and a flower box), the taller grey gable house to the east (a window with
  shutters and an attic window in the gable), the low middle part behind a boarded screen with a
  green door across the street notch;
- 93238172 (80): the falu-red boarded two-storey house on a dark plinth, ochre window frames and
  door on steps, under a red tiled saddle roof, with a low rear wing;
- 93238187 (82): the pale yellow rendered two-storey house on a high dark plinth with cellar
  windows, a string course and cornice, five ground-floor windows, a green door on steps and a
  green carriage gate with a fanlight, seven upper windows, a black hipped roof with three black
  box dormers (the middle one wide) and a chimney; a flat-roofed stair tower behind;
- 93238156 (84): the cream rendered three-storey house with dark red window frames, the red
  double door, a three-sided bay over the two upper floors under a curved gable with its own
  window, two red-brown dormers and a dark hipped roof; the long rear wing flat-roofed;
- 93238202: the pale grey boarded cottage on Östra Vallgatan with its gable to the street, and its
  unseen west parts.

References: Google Street View (five panoramas on Norra Långgatan and Östra Vallgatan, resected on
house corners), view only. Zones: source/block100.json; see references/block100-notes.md. Signs,
the fences in front of 93238210, lamps, pipes, cars and planting are omitted.
"""
B100D=json.loads((R/'source/block100.json').read_text());Z=B100D['zones']
block100_names=[];B100={}
for old in [k for k in list(materials) if k.startswith('M_Block100_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Yellow','TownIvory',(.88,.78,.55),.85,0),('Trim','TownPaintWhite',(.90,.88,.80),.60,0),('Green','TownPaintGreen',(.33,.55,.51),.60,0),
 ('Plinth','TownStone',(.32,.32,.33),.90,0),('Black','TownMetalGrey',(.12,.12,.13),.55,.25),('Cream','TownIvory',(.90,.86,.74),.85,0),
 ('WinRed','TownPaintBrown',(.48,.13,.11),.60,0),('DoorRed','TownPaintBrown',(.50,.15,.15),.60,0),('Stone','TownStone',(.55,.55,.54),.90,0),
 ('Roof','TownMetalGrey',(.24,.24,.25),.60,.20),('DormerRed','TownPaintBrown',(.55,.25,.20),.60,0),('Red','TownPaintBrown',(.50,.14,.13),.80,0),
 ('Ochre','TownPaintWhite',(.80,.66,.42),.60,0),('DoorOchre','TownPaintBrown',(.82,.62,.32),.60,0),('Tile','TownTileRed',(.78,.42,.27),.80,0),
 ('Grey','TownPaintWhite',(.47,.50,.53),.80,0),('PaleGrey','TownPaintWhite',(.80,.81,.78),.80,0),('White','TownPaintWhite',(.94,.94,.92),.55,0),
 ('Sheet','TownMetalGrey',(.12,.12,.13),.50,.30),('Chimney','TownTileRed',(.55,.32,.26),.85,0),('Dark','TownMetalGrey',(.06,.06,.065),.45,.40),
 ('Flowers','TownPaintGreen',(.30,.45,.25),.80,0),
 ]:
 name='M_Block100_'+key;B100[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block100_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B100;WF=M['White']

def b100_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block100_names.append(name);return Mesh(name,category)
def drop_degenerate_faces100(obj,tol=1e-9):
 import bmesh
 bm=bmesh.new();bm.from_mesh(obj.data)
 def _thin(f):
  L=max(e.calc_length() for e in f.edges);return L>0 and 2*f.calc_area()/L<1e-4
 bad=[f for f in bm.faces if f.calc_area()<tol or len({v.index for v in f.verts})<len(f.verts) or _thin(f)]
 if bad:bmesh.ops.delete(bm,geom=bad,context='FACES_ONLY')
 bm.to_mesh(obj.data);bm.free();obj.data.update();return len(bad)
block100_dropped={}
block100_samples={}
def b100_finish(m,osm):
 obj=s21_finish(m)
 import bmesh
 bm=bmesh.new();bm.from_mesh(obj.data)
 block100_samples[obj.name]=[tuple(round(c,2) for c in f.calc_center_median())+(round(f.calc_area(),6),len(f.verts)) for f in bm.faces if f.calc_area()<1e-9 or (max(e.calc_length() for e in f.edges)>0 and 2*f.calc_area()/max(e.calc_length() for e in f.edges)<1e-4)][:5]
 bm.free();block100_dropped[obj.name]=drop_degenerate_faces100(obj)
 obj['detail_pass']=100;obj['reference_notes']='references/block100-notes.md';obj['osm_way']=osm;return obj

def pt100(a,b,s):
 # The point s metres from a towards b.
 L=math.dist(a,b);return (a[0]+(b[0]-a[0])*s/L,a[1]+(b[1]-a[1])*s/L)
# Street frames for the gable fronts (as pass 99): s along the OSM front from A to B, t outwards
# (to the right of A->B); the facade surfaces stand at t = 0.355.
def fr100(A,B):
 L=math.dist(A,B);D=((B[0]-A[0])/L,(B[1]-A[1])/L);return dict(A=A,B=B,D=D,N=(D[1],-D[0]),L=L,ang=math.atan2(D[1],D[0]))
def P100(f,s,t=0,z=None):
 p=(f['A'][0]+f['D'][0]*s+f['N'][0]*t,f['A'][1]+f['D'][1]*s+f['N'][1]*t);return p if z is None else (*p,z)
def rect100(f,zone):
 pts=[v for g in Z[zone]['polygons'] for v in g];A,D,N=f['A'],f['D'],f['N']
 ss=[(v[0]-A[0])*D[0]+(v[1]-A[1])*D[1] for v in pts];ts=[(v[0]-A[0])*N[0]+(v[1]-A[1])*N[1] for v in pts]
 return min(ss),max(ss),min(ts),max(ts)
def prism100(m,f,outline,t0,t1,ma):
 n=len(outline);vs=[P100(f,s,t,z) for t in (t0,t1) for s,z in outline]
 m.faces(vs,[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],ma)
def gable100(m,f,zone,wall,roof,trim,ov=.30,eave=.35):
 # Saddle roof with its ridge running back from the street over the boxed outline; gable prisms in
 # the wall material at the street front and at the back, verge boards, gutters.
 s0,s1,t0,t1=rect100(f,zone)
 H=Z[zone]['height'];T=Z[zone]['top'];o=.355;sL,sR=s0-o,s1+o;sm=(sL+sR)/2;sl=(T-H)/(sm-sL)
 tf,tb=t1+o+ov,t0-o-ov
 for se,sg in ((sL,-1),(sR,1)):
  e=se+sg*eave;ze=H-eave*sl
  m.faces([P100(f,e,tb,ze+.12),P100(f,sm,tb,T+.12),P100(f,sm,tf,T+.12),P100(f,e,tf,ze+.12)],[(0,1,2,3),(3,2,1,0)],roof)
  town_rod(m,P100(f,e,tb,ze+.02),P100(f,e,tf,ze+.02),.07,M['Sheet'],8)
  for tt in (tf-.03,tb+.03):town_path(m,[P100(f,e,tt,ze+.06),P100(f,sm,tt,T+.06)],.08,trim)
 g=[(sL,H),(sR,H),(sm,T-.02)]
 prism100(m,f,g,t1+.005,t1+o,wall);prism100(m,f,g,t0-o,t0-.005,wall)
 return sL,sR,sm,t1+o,sl
def gable_boards100(m,f,sL,sR,sm,H,T,tface,ma,step=.22):
 # Vertical boards on the street gable, clipped to the rakes.
 n=int((sR-sL)/step)
 for k in range(1,n):
  s=sL+k*(sR-sL)/n;z1=H+(T-H)*(1-abs(s-sm)/(sm-sL))-.14
  if z1-H>.06:m.box(P100(f,s,tface+.02,(H+z1)/2),(.035,.03,z1-H),ma,f['ang'])
def win100(m,x,y,u,b,w,h,a,frame,sur,rows=3,o=.16,bw=.10):
 # Casement in its frame, a flat surround and a sill.
 cas81(m,x,y,u,b,w,h,a,frame,o,rows)
 if sur:surround36(m,x,y,u,b,w,h,a,sur,bw,.40);facade_box(m,x,y,u,.47,b-.05,w+.24,.16,.06,sur,a)
def flush100(m,x,y,u,b,w,h,a,frame,rows=2):
 # A window laid on a solid face (gable prisms): glass, frame and surround in front of it.
 facade_box(m,x,y,u,.37,b+h/2,w,.02,h,GLAZE,a);cas81(m,x,y,u,b,w,h,a,frame,.41,rows);surround36(m,x,y,u,b,w,h,a,frame,.08,.42)
def shutters100(m,x,y,u,b,w,h,a,ma,fl=None):
 # White shutters folded back beside the window, and a flower box under it.
 for s in (-1,1):facade_box(m,x,y,u+s*(w/2+.30),.44,b+h/2,.50,.05,h+.10,ma,a)
 if fl:facade_box(m,x,y,u,.58,b-.12,w+.10,.30,.20,ma,a);facade_box(m,x,y,u,.58,b+.02,w,.24,.12,fl,a)
def dormer100(m,x,y,u,a,H,slope,w,h,body,roof,frame,wins,back=.9,dep=2.2):
 # A box dormer standing on the slope, its face 'back' metres behind the facade surface, a flat
 # lid, and one or more windows (offset along the face, width).
 zb=H+(back+.40-.355+.05)*slope-.15;zt=zb+h+.55
 box(m,*lp(x,y,u,.355-back-dep/2,0,a)[:2],w,dep,zt-zb,zb,body,a)
 box(m,*lp(x,y,u,.355-back-dep/2+.10,0,a)[:2],w+.25,dep+.2,.12,zt,roof,a)
 for du,ww in wins:
  facade_box(m,x,y,u+du,.355-back+.01,zb+.30+h/2,ww,.02,h,GLAZE,a);cas81(m,x,y,u+du,zb+.30,ww,h,a,frame,.355-back+.05,2)
def fronts100(m,zone,test,wall,frame,trim,levels,floor0=1.0):
 # Party and upper walls in the wall material, unseen outer walls plain; returns the street fronts.
 H=Z[zone]['height'];out=[]
 for w in walls(zone):
  if w['kind']!='outer':bz_wall(m,w['p'],w['q'],w['z0'],H,[],wall);continue
  ox,oy=outward(w);x,y,L,a=sf_edge(w['p'],w['q'])
  if test(ox,oy,x,y):out.append(w);continue
  plain(m,w,H,wall,frame,trim,levels,floor0)
 return out
def flatroof100(m,zone,ma,trim):
 H=Z[zone]['height']
 for g in Z[zone]['polygons']:m.faces([(*v,H+.02) for v in g],[tuple(range(len(g))),tuple(range(len(g)-1,-1,-1))],ma)
 for w in walls(zone,'outer'):
  x,y,L,a=sf_edge(w['p'],w['q']);facade_box(m,x,y,0,.38,H+.12,L+.06,.12,.24,trim,a)
NL=lambda ox,oy,x,y:oy>.9 and y>59.0

# ---- 93238210: the grey cottages (positions s in metres from the west end of each OSM front).
m=b100_new(Z['c210w']['mesh'],'Kvarnholmen/Norra Långgatan');GR=M['Grey']
for zone,A,B,ops in (('c210w',(312.92,60.371),(307.694,60.585),[('win',2.55,1.44,1.15,1.10)]),
                     ('c210e',(319.874,60.244),(315.92,60.396),[('win',1.10,1.34,1.15,1.20),('attic',1.17,3.39,1.10,1.15)])):
 H=Z[zone]['height'];T=Z[zone]['top'];F=fr100(A,B)
 for w in fronts100(m,zone,NL,GR,WF,WF,1,.9):
  x,y,L,a=sf_edge(w['p'],w['q']);S=lambda s:U(w,*pt100(B,A,s))
  holes=[(S(s),b,ww,hh,0) for k,s,b,ww,hh in ops if k=='win']
  bz_wall(m,w['p'],w['q'],0,H,holes,GR);boards82(m,x,y,L,a,.57,H-.08,holes,GR)
  for k,s,b,ww,hh in ops:
   if k=='win':win100(m,x,y,S(s),b,ww,hh,a,WF,WF,2);shutters100(m,x,y,S(s),b,ww,hh,a,WF,M['Flowers'])
   else:flush100(m,x,y,S(s),b,ww,hh,a,WF,2)
  facade_box(m,x,y,0,.39,.28,L+.02,.08,.56,M['Stone'],a)
  for uu in (-L/2+.08,L/2-.08):facade_box(m,x,y,uu,.42,(H+.56)/2,.16,.10,H-.56,WF,a)
 sL,sR,sm,tface,sl=gable100(m,F,zone,GR,M['Tile'],WF)
 gable_boards100(m,F,sL,sR,sm,H,T,tface,GR)
 s0,s1,t0,t1=rect100(F,zone);X,Y=P100(F,(s0+s1)/2,(t0+t1)/2-1.0);chimney82(m,X,Y,T-.6,T+.65,M['Chimney'])
# The middle part behind the street notch, and the boarded screen across the notch with its green
# door and a lean-to roof back to the middle part.
fronts100(m,'c210m',lambda *_:False,GR,WF,WF,1);saddle82(m,'c210m',(312.53,50.32),(315.51,50.2),M['Tile'],GR,along=True)
sw={'p':[315.92,60.396],'q':[312.92,60.371]};x,y,L,a=sf_edge(sw['p'],sw['q']);ud=U(sw,314.72,60.38)
bz_wall(m,sw['p'],sw['q'],0,2.15,[(ud,.12,.95,1.85,0)],GR);boards82(m,x,y,L,a,.40,2.07,[(ud,.12,.95,1.85,0)],GR)
facade_box(m,x,y,ud,.14,.12+1.85/2,.95,.06,1.85,M['Green'],a);surround36(m,x,y,ud,.12,.95,1.85,a,WF,.08,.40)
m.faces([(315.95,60.95,2.22),(312.89,60.95,2.22),(312.83,57.20,2.55),(315.82,57.10,2.55)],[(0,1,2,3),(3,2,1,0)],M['Tile'])
facade_box(m,x,y,0,.46,2.10,L+.1,.10,.18,WF,a)
b100_finish(m,'93238210')

# ---- 93238172 (80): the red house.
m=b100_new(Z['r172']['mesh'],'Kvarnholmen/Norra Långgatan');RE=M['Red'];OC=M['Ochre']
W72,E72=(321.511,60.604),(330.441,60.313);H=Z['r172']['height']
for w in fronts100(m,'r172',NL,RE,OC,OC,2):
 x,y,L,a=sf_edge(w['p'],w['q']);S=lambda s:U(w,*pt100(W72,E72,s))
 ops=[(S(s),1.67,1.05,1.06,2) for s in (1.14,5.27,7.17)]+[(S(s),3.69,.92,.91,2) for s in (1.81,5.16,7.16)]
 du=S(2.81);holes=[(u,b,ww,hh,0) for u,b,ww,hh,n in ops]+[(du,.74,1.06,1.86,0)]
 bz_wall(m,w['p'],w['q'],0,H,holes,RE);boards82(m,x,y,L,a,.85,H-.08,holes,RE)
 for u,b,ww,hh,n in ops:win100(m,x,y,u,b,ww,hh,a,OC,OC,n,bw=.09)
 door83(m,x,y,du,.74,1.06,1.86,a,M['DoorOchre'],OC,glass=False);steps82(m,x,y,du,1.06,.74,a,M['Stone'])
 facade_box(m,x,y,0,.39,.42,L+.02,.08,.84,M['Plinth'],a)
 for uu in (-L/2+.08,L/2-.08):facade_box(m,x,y,uu,.42,(H+.84)/2,.16,.10,H-.84,RE,a)
 facade_box(m,x,y,0,.46,H-.10,L+.1,.14,.20,RE,a);town_rod(m,lp(x,y,-L/2,.66,H-.05,a),lp(x,y,L/2,.66,H-.05,a),.06,M['Sheet'],8)
saddle82(m,'r172',W72,E72,M['Tile'],RE,along=True)
fronts100(m,'r172b',lambda *_:False,RE,OC,OC,1);saddle82(m,'r172b',(325.78,50.09),(330.16,49.94),M['Tile'],RE,along=True)
X,Y=pt100(W72,E72,6.2);chimney82(m,X,Y-3.4,Z['r172']['top']-.6,Z['r172']['top']+.75,M['Chimney'])
b100_finish(m,'93238172')

# ---- 93238187 (82): the yellow rendered house.
m=b100_new(Z['y187']['mesh'],'Kvarnholmen/Norra Långgatan');YE=M['Yellow'];TR=M['Trim'];GN=M['Green']
W82,E82=(330.441,60.313),(349.869,59.988);H=Z['y187']['height']
for w in fronts100(m,'y187',NL,YE,TR,TR,2):
 x,y,L,a=sf_edge(w['p'],w['q']);S=lambda s:U(w,*pt100(W82,E82,s))
 ops=[(S(s),1.96,1.30,1.95) for s in (3.46,5.80,12.24,15.10,17.68)]+[(S(s),5.17,1.30,2.06) for s in (1.30,3.40,5.80,9.05,12.24,14.85,17.40)]
 gu,du=S(1.30),S(9.10)
 holes=[(u,b,ww,hh,0) for u,b,ww,hh in ops]+[(gu,0,2.30,3.85,0),(du,0,1.11,3.71,0)]
 bz_wall(m,w['p'],w['q'],0,H,holes,YE)
 for u,b,ww,hh in ops:win100(m,x,y,u,b,ww,hh,a,TR,TR,3,bw=.12)
 # The carriage gate: two leaves, a transom and a glazed fanlight.
 for s in (-1,1):
  facade_box(m,x,y,gu+s*.575,.12,1.60,1.12,.07,3.20,GN,a)
  for zz in (.45,1.6,2.75):facade_box(m,x,y,gu+s*.575,.17,zz,.90,.03,.06,GN,a)
 facade_box(m,x,y,gu,.10,3.52,2.20,.02,.64,GLAZE,a);facade_box(m,x,y,gu,.16,3.22,2.30,.08,.08,GN,a)
 for k in range(1,4):facade_box(m,x,y,gu-1.15+k*.575,.16,3.52,.05,.05,.64,GN,a)
 surround36(m,x,y,gu,0,2.30,3.85,a,TR,.12,.40)
 # The door stands in a niche with its steps inside it, the lowest step just proud of the wall.
 door83(m,x,y,du,1.44,1.11,2.27,a,GN,TR,glass=True)
 for k in range(8):o1=.85-k*.14;facade_box(m,x,y,du,(o1-.30)/2,(k+.5)*.18,1.11,o1+.30,.18,M['Stone'],a)
 # Plinth (broken at the gate) with cellar windows, string course, cornice.
 lo,hi=sorted((gu-1.27,gu+1.27))
 for u0,u1 in ((-L/2,lo),(hi,L/2)):
  if u1-u0>.05:facade_box(m,x,y,(u0+u1)/2,.40,.50,u1-u0,.10,1.00,M['Plinth'],a)
 for s in (3.46,5.80,12.24,15.10,17.68):facade_box(m,x,y,S(s),.46,.52,.60,.02,.32,M['Dark'],a)
 facade_box(m,x,y,0,.42,4.62,L+.04,.14,.24,TR,a);facade_box(m,x,y,0,.40,4.93,L+.02,.08,.38,YE,a)
 facade_box(m,x,y,0,.46,8.40,L+.12,.22,.40,TR,a);facade_box(m,x,y,0,.52,8.68,L+.20,.34,.14,TR,a)
fronts100(m,'y187b',lambda *_:False,YE,TR,TR,2);flatroof100(m,'y187b',M['Black'],YE)
r,sl82=hip82(m,'y187',W82,E82,M['Black'])
fw=[w for w in walls('y187','outer') if outward(w)[1]>.9][0];x,y,L,a=sf_edge(fw['p'],fw['q'])
for s,ww,wins in ((2.3,3.0,[(-.55,.95),(.55,.95)]),(9.4,5.4,[(-1.5,1.05),(1.5,1.05)]),(16.7,3.0,[(-.55,.95),(.55,.95)])):
 dormer100(m,x,y,U(fw,*pt100(W82,E82,s)),a,H,sl82,ww,1.15,M['Black'],M['Black'],TR,wins,back=.9)
X,Y=pt100(W82,E82,4.0);chimney82(m,X,Y-4.6,Z['y187']['top']-.9,Z['y187']['top']+.6,M['Chimney'])
b100_finish(m,'93238187')

# ---- 93238156 (84): the cream rendered three-storey house.
m=b100_new(Z['k156']['mesh'],'Kvarnholmen/Norra Långgatan');CR=M['Cream'];WR=M['WinRed']
W84,E84=(349.869,59.988),(363.575,59.889);H=Z['k156']['height']
for w in fronts100(m,'k156',NL,CR,WR,TR,3):
 x,y,L,a=sf_edge(w['p'],w['q']);S=lambda s:U(w,*pt100(W84,E84,s))
 ops=[(S(s),1.30,1.55,1.76) for s in (2.20,5.35,8.17)]+[(S(s),b,ww,1.68) for s,ww in ((2.32,1.50),(11.30,1.38)) for b in (4.88,8.08)]
 du=S(12.02);holes=[(u,b,ww,hh,0) for u,b,ww,hh in ops]+[(du,.05,1.90,3.00,0)]
 bz_wall(m,w['p'],w['q'],0,H,holes,CR)
 for u,b,ww,hh in ops:win100(m,x,y,u,b,ww,hh,a,WR,None,3);facade_box(m,x,y,u,.45,b-.05,ww+.20,.14,.06,CR,a)
 # The double door with its fanlight, in a raised surround.
 door83(m,x,y,du,.05,1.90,2.62,a,M['DoorRed'],M['DoorRed'],glass=False)
 facade_box(m,x,y,du,.10,2.85,1.80,.02,.36,GLAZE,a)
 for k in range(1,4):facade_box(m,x,y,du-.9+k*.45,.15,2.85,.05,.05,.36,M['DoorRed'],a)
 surround36(m,x,y,du,.05,1.90,3.00,a,CR,.14,.44)
 # The bay over the upper floors: three faces on a corbel, its windows, a lid.
 bu=S(6.69);bp=[(-1.75,.355),(-.95,1.05),(.95,1.05),(1.75,.355)];z0,z1=3.25,10.45
 vs=[lp(x,y,bu+pu,po,z,a) for z in (z0,z1) for pu,po in bp]
 m.faces(vs,[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],CR)
 cv=[lp(x,y,bu+pu*.55,.355+(po-.355)*.55,z0-.55,a) for pu,po in bp]+[lp(x,y,bu+pu,po,z0,a) for pu,po in bp]
 m.faces(cv,[(3,2,1,0),(0,1,5,4),(1,2,6,5),(2,3,7,6)],CR)
 lid=[lp(x,y,bu+pu*1.06,.355+(po-.355)*1.12,z1,a) for pu,po in bp]+[lp(x,y,bu+pu*1.06,.355+(po-.355)*1.12,z1+.18,a) for pu,po in bp]
 m.faces(lid,[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6)],M['Roof'])
 for b in (4.88,8.08):
  cas81(m,x,y,bu,b,1.10,1.68,a,WR,1.10,3)
  for (u0,o0),(u1,o1) in ((bp[0],bp[1]),(bp[2],bp[3])):
   # Glass on each chamfer, 2 cm out along its outward normal.
   cu,co=(u0+u1)/2,(o0+o1)/2;du_,do_=(u1-u0),(o1-o0);ln=math.hypot(du_,do_);nu,no=-do_/ln,du_/ln
   qu=[(cu-du_/ln*.33+nu*.02,co-do_/ln*.33+no*.02),(cu+du_/ln*.33+nu*.02,co+do_/ln*.33+no*.02)]
   q=[lp(x,y,bu+qu[0][0],qu[0][1],b,a),lp(x,y,bu+qu[1][0],qu[1][1],b,a),lp(x,y,bu+qu[1][0],qu[1][1],b+1.68,a),lp(x,y,bu+qu[0][0],qu[0][1],b+1.68,a)]
   m.faces(q,[(0,1,2,3),(3,2,1,0)],GLAZE)
   fu,fo=[(qu[k][0]+nu*.02,qu[k][1]+no*.02) for k in (0,1)],None
   town_path(m,[lp(x,y,bu+fu[k][0],fu[k][1],zz,a) for k,zz in ((0,b),(1,b),(1,b+1.68),(0,b+1.68),(0,b))],.04,WR)
 # Plinth, string course over the ground floor, cornice.
 facade_box(m,x,y,0,.40,.25,L+.02,.10,.50,M['Stone'],a)
 facade_box(m,x,y,0,.42,3.98,L+.04,.14,.20,TR,a)
 facade_box(m,x,y,0,.46,H-.35,L+.10,.20,.50,CR,a);facade_box(m,x,y,0,.52,H-.06,L+.20,.32,.12,TR,a)
 # The curved gable over the bay, with its window and a short saddle running back into the roof.
 gp=[(-2.2,H),(2.2,H),(2.2,H+.65),(1.75,H+1.45),(1.0,H+2.15),(0,H+2.56),(-1.0,H+2.15),(-1.75,H+1.45),(-2.2,H+.65)]
 vs=[lp(x,y,bu+gu_,o,gz,a) for o in (.005,.42) for gu_,gz in gp];n=len(gp)
 m.faces(vs,[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],CR)
 town_path(m,[lp(x,y,bu+gu_,.46,gz+.05,a) for gu_,gz in gp[1:]+gp[:1]][1:],.07,TR)
 flush100(m,x,y,bu,H+.15,1.15,1.05,a,WR,2)
 for s in (-1,1):
  m.faces([lp(x,y,bu+s*2.3,.20,H+.60,a),lp(x,y,bu,.20,H+2.45,a),lp(x,y,bu,-3.3,H+2.45,a),lp(x,y,bu+s*2.3,-3.3,H+.60,a)],[(0,1,2,3),(3,2,1,0)],M['Roof'])
 m.faces([lp(x,y,bu-2.3,-3.3,H+.60,a),lp(x,y,bu+2.3,-3.3,H+.60,a),lp(x,y,bu,-3.3,H+2.45,a)],[(0,1,2),(2,1,0)],CR)
r,sl84=hip82(m,'k156',W84,E84,M['Roof'])
fw=[w for w in walls('k156','outer') if outward(w)[1]>.9 and sf_edge(w['p'],w['q'])[2]>5][0];x,y,L,a=sf_edge(fw['p'],fw['q'])
for s in (1.30,11.20):dormer100(m,x,y,U(fw,*pt100(W84,E84,s)),a,H,sl84,1.60,.95,M['DormerRed'],M['Roof'],WR,[(0,1.0)],back=.35,dep=1.8)
fronts100(m,'k156b',lambda *_:False,CR,WR,TR,3);flatroof100(m,'k156b',M['Roof'],CR)
b100_finish(m,'93238156')

# ---- 93238202: the pale grey cottage on Östra Vallgatan (s from the south end of the front).
m=b100_new(Z['g202']['mesh'],'Kvarnholmen/Östra Vallgatan');PG=M['PaleGrey']
A2,B2=(387.278,44.83),(387.899,50.687);H=Z['g202']['height'];T=Z['g202']['top'];F=fr100(A2,B2)
for w in fronts100(m,'g202',lambda ox,oy,x,y:ox>.9 and x>386.5,PG,WF,WF,1):
 x,y,L,a=sf_edge(w['p'],w['q']);S=lambda s:U(w,*pt100(A2,B2,s))
 holes=[(S(1.60),1.15,1.00,.95,0)]
 bz_wall(m,w['p'],w['q'],0,H,holes,PG);boards82(m,x,y,L,a,.42,H-.08,holes,PG)
 win100(m,x,y,S(1.60),1.15,1.00,.95,a,WF,WF,2)
 facade_box(m,x,y,0,.39,.20,L+.02,.08,.40,M['Stone'],a)
 for uu in (-L/2+.08,L/2-.08):facade_box(m,x,y,uu,.42,(H+.40)/2,.16,.10,H-.40,WF,a)
sL,sR,sm,tface,sl=gable100(m,F,'g202',PG,M['Tile'],WF);gable_boards100(m,F,sL,sR,sm,H,T,tface,PG)
s0,s1,t0,t1=rect100(F,'g202');X,Y=P100(F,(s0+s1)/2,t1-2.5);chimney82(m,X,Y,T-.6,T+.9,M['Chimney'])
fronts100(m,'g202w',lambda *_:False,PG,WF,WF,1);saddle82(m,'g202w',(369.359,44.94),(374.608,43.843),M['Tile'],PG,along=False)
fronts100(m,'g202m',lambda *_:False,PG,WF,WF,1);flatroof100(m,'g202m',M['Dark'],PG)
b100_finish(m,'93238202')

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block100_cameras=[
 sv_camera('489_Block100_Cal_Red',326.33,67.76,2.37,152,15,90),
 sv_camera('490_Block100_Cal_Yellow',340.06,67.91,2.41,154,15,90),
 sv_camera('491_Block100_Cal_Cream',362.18,67.41,2.23,152,15,90),
 sv_camera('492_Block100_Cal_Vallgatan',395.01,42.20,2.54,222,15,90),
 ('493_Block100_Aerial',(345.0,92.0,34.0),(345.0,52.0,2.0),28),
]
print('BLOCK100_GEOMETRY',len(block100_names),'dropped',block100_dropped,block100_samples)
