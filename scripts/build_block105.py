"""Pass 105: Strömgatan in the north-west of Kvarnholmen.
- 92204196 (3 Strömgatan, south side): the olive roughcast three-storey house, white lesenes
  dividing it into seven bays, a white string course over the ground floor, white window
  surrounds, the arched centre bay with the arched entrance and two arched windows, a white
  cornice and a low grey sheet hipped roof; the rear part flat-roofed (not seen);
- 92204205 (north side): the grey rendered four-storey house on a pale granite-look ground floor
  with a passage at its west end, two box bays over the second and third floors, white windows
  with small canopies, a cornice and a dark mansard with two dormers;
- 92204158 (north side): the red brick three-storey house on a dark plinth, low ground-floor
  windows, the low red gate, the arched door and the white-framed box window at the east end,
  three and four wide windows under grey arched hoods, a large arched window over the door, a
  brick cornice and a dark mansard with four dormers;
- 92204154 (north side, west end): brick upper floors with white window surrounds over a pale
  rusticated ground floor (one window and the rustication seen; the rest estimated), hipped roof;
- 92204191 (north side): the small green rendered house with an orange tile saddle roof, generic
  openings (seen only obliquely);
- 92379281 (10 Strömgatan, south side): the yellow brick four-storey house on a granite plinth,
  black window frames, brick string courses, the arched black double gate and the recessed red
  door; the top floor and roof are cut off in the photo and estimated; the rear wing generic;
- 91285791 (Södra Kanalgatan): not photographed; a generic rendered volume with plain windows.

References: Google Street View (three panoramas on Strömgatan, resected on house corners and
joints), view only. Zones: source/block105.json; see references/block105-notes.md. Cars, signs,
lamps and pipes are omitted.
"""
B105D=json.loads((R/'source/block105.json').read_text());Z=B105D['zones']
block105_names=[];B105={}
for old in [k for k in list(materials) if k.startswith('M_Block105_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Olive','TownIvory',(.55,.52,.42),.90,0),('White','TownPaintWhite',(.92,.92,.89),.60,0),('Sheet','TownMetalGrey',(.42,.43,.44),.55,.25),
 ('Grey','TownPaintWhite',(.55,.54,.52),.85,0),('Granite','TownStone',(.66,.65,.62),.90,0),('Mansard','TownMetalGrey',(.28,.28,.30),.55,.25),
 ('Brick','TownTileRed',(.60,.36,.28),.90,0),('Hood','TownMetalGrey',(.40,.42,.45),.55,.25),('Plinth','TownStone',(.20,.20,.21),.90,0),
 ('RedGate','TownPaintBrown',(.68,.22,.15),.60,0),('Door','TownPaintBrown',(.50,.28,.20),.60,0),('Green','TownIvory',(.63,.64,.51),.90,0),
 ('Tile','TownTileRed',(.80,.42,.25),.80,0),('Yellow','TownIvory',(.71,.61,.46),.90,0),('Black','TownMetalGrey',(.09,.09,.10),.50,.30),
 ('RedDoor','TownPaintBrown',(.66,.30,.19),.60,0),('Stone','TownStone',(.62,.61,.58),.90,0),('Render','TownIvory',(.80,.76,.66),.85,0),
 ('Rust','TownStone',(.80,.78,.72),.90,0),('Dark','TownMetalGrey',(.06,.06,.065),.45,.40),
 ]:
 name='M_Block105_'+key;B105[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block105_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B105;WH=M['White']

def b105_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block105_names.append(name);return Mesh(name,category)
def drop_degenerate_faces105(obj,tol=1e-9):
 import bmesh
 bm=bmesh.new();bm.from_mesh(obj.data)
 def _thin(f):
  L=max(e.calc_length() for e in f.edges);return L>0 and 2*f.calc_area()/L<1e-4
 bad=[f for f in bm.faces if f.calc_area()<tol or len({v.index for v in f.verts})<len(f.verts) or _thin(f)]
 if bad:bmesh.ops.delete(bm,geom=bad,context='FACES_ONLY')
 bm.to_mesh(obj.data);bm.free();obj.data.update();return len(bad)
block105_dropped={}
def b105_finish(m,osm):
 obj=s21_finish(m);block105_dropped[obj.name]=drop_degenerate_faces105(obj)
 obj['detail_pass']=105;obj['reference_notes']='references/block105-notes.md';obj['osm_way']=osm;return obj

def pt105(a,b,s):
 # The point s metres from a towards b.
 L=math.dist(a,b);return (a[0]+(b[0]-a[0])*s/L,a[1]+(b[1]-a[1])*s/L)
def fronts105(m,zone,test,wall,frame,trim,levels,floor0=1.0):
 # Party and upper walls in the wall material, unseen outer walls plain; returns the street fronts.
 H=Z[zone]['height'];out=[]
 for w in walls(zone):
  if w['kind']!='outer':bz_wall(m,w['p'],w['q'],w['z0'],H,[],wall);continue
  ox,oy=outward(w);x,y,L,a=sf_edge(w['p'],w['q'])
  if test(ox,oy,x,y):out.append(w);continue
  plain(m,w,H,wall,frame,trim,levels,floor0)
 return out
def flatroof105(m,zone,ma,trim):
 # Flat roof (triangulated, the outlines can be concave) and a low parapet coping.
 from mathutils import Vector
 from mathutils.geometry import tessellate_polygon
 H=Z[zone]['height']
 for g in Z[zone]['polygons']:
  vs=[(*v,H+.02) for v in g];tris=tessellate_polygon([[Vector(v) for v in vs]])
  m.faces(vs,[tuple(t) for t in tris]+[tuple(reversed(t)) for t in tris],ma)
 for w in walls(zone,'outer'):
  x,y,L,a=sf_edge(w['p'],w['q']);facade_box(m,x,y,0,.38,H+.12,L+.06,.12,.24,trim,a)
def prism105(m,x,y,u,outline,o0,o1,ma,a):
 # A closed prism of the face outline [(du,z)] between the offsets o0 and o1 from the wall line.
 n=len(outline);vs=[lp(x,y,u+du,o,zz,a) for o in (o0,o1) for du,zz in outline]
 m.faces(vs,[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],ma)
def arc105(u,w,z,r,k=12):
 # The elliptic head used by bz_wall's arched holes: from the right spring over to the left.
 return [(w/2*math.cos(t*math.pi/k),z+r*math.sin(t*math.pi/k)) for t in range(k+1)]
def archwin105(m,x,y,u,b,w,h,r,a,frame,sur=None,lights=3,o=.16,bw=.12):
 # An arched opening: glass to the crown, frame round it, mullions, a transom at the spring.
 pts=[(-w/2,b),(w/2,b)]+arc105(u,w,b+h,r)
 m.faces([lp(x,y,u+du,o-.04,zz,a) for du,zz in pts],[tuple(range(len(pts))),tuple(range(len(pts)-1,-1,-1))],GLAZE)
 town_path(m,[lp(x,y,u+du,o,zz,a) for du,zz in pts+pts[:1]],.045,frame)
 facade_box(m,x,y,u,o,b+h,w,.06,.06,frame,a)
 for k in range(1,lights):facade_box(m,x,y,u-w/2+k*w/lights,o,b+(h+r*.8)/2,.05,.06,h+r*.8,frame,a)
 if sur:
  town_path(m,[lp(x,y,u+du*(1+2*bw/w),.40,zz+(zz-b-h)*(bw/r if zz>b+h else 0),a) for du,zz in arc105(u,w,b+h,r)],.07,sur)
  for s in (-1,1):facade_box(m,x,y,u+s*(w/2+bw/2),.39,b+h/2,bw,.07,h,sur,a)
  facade_box(m,x,y,u,.45,b-.05,w+.24,.16,.06,sur,a)
def win105(m,x,y,u,b,w,h,a,frame,sur,rows=2,bw=.12):
 cas81(m,x,y,u,b,w,h,a,frame,.16,rows)
 if sur:surround36(m,x,y,u,b,w,h,a,sur,bw,.40);facade_box(m,x,y,u,.47,b-.05,w+.24,.16,.06,sur,a)
def hood105(m,x,y,u,top,w,a,ma,rise=.55,th=.22,o0=.36,o1=.66):
 # The grey arched hood over a window: a segmental band standing out from the brick, built from
 # convex quads between its outer and inner arcs.
 k=10;ou=[(w/2*math.cos(t*math.pi/k),top+th+rise*math.sin(t*math.pi/k)) for t in range(k+1)]
 inn=[(w/2*math.cos(t*math.pi/k),top+rise*math.sin(t*math.pi/k)) for t in range(k+1)]
 for i in range(k):
  q=[ou[i],ou[i+1],inn[i+1],inn[i]];vs=[lp(x,y,u+du,o,zz,a) for o in (o0,o1) for du,zz in q]
  m.faces(vs,[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],ma)
def dormer105(m,x,y,u,a,H,w,h,body,frame,back=.7,dep=2.0):
 # A box dormer on a mansard: face 'back' metres behind the facade surface, flat lid, one window.
 zb=H+.15;zt=zb+h+.45
 box(m,*lp(x,y,u,.355-back-dep/2,0,a)[:2],w,dep,zt-zb,zb,body,a)
 box(m,*lp(x,y,u,.355-back-dep/2+.08,0,a)[:2],w+.16,dep+.16,.10,zt,body,a)
 facade_box(m,x,y,u,.355-back+.01,zb+.25+h/2,w-.30,.02,h,GLAZE,a);cas81(m,x,y,u,zb+.25,w-.30,h,a,frame,.355-back+.05,2)
def mansard105(m,zone,A,B,ma,inset=1.5):
 r,Ls,Lt=rect82(zone,A,B);H=Z[zone]['height'];T=Z[zone]['top']
 inset_roof(m,r,H,inset,T-H,ma,.30)
def cornice105(m,x,y,L,a,H,ma,d=.30):
 facade_box(m,x,y,0,.40,H-.25,L+.04,.12,.30,ma,a);facade_box(m,x,y,0,.355+d/2,H-.05,L+.20,d,.10,ma,a)
S105=lambda ox,oy:(lambda o,p,x,y:p>.9) if oy>0 else (lambda o,p,x,y:p<-.9)

# ---- 92204196 (3 Strömgatan): olive roughcast, s from the east corner along the north front.
m=b105_new(Z['f196']['mesh'],'Kvarnholmen/Strömgatan');OL=M['Olive']
A6,B6=(-221.06,205.97),(-245.45,206.24);H=Z['f196']['height'];C6=12.1
for w in fronts105(m,'f196',S105(0,1),OL,WH,WH,3,.8):
 x,y,L,a=sf_edge(w['p'],w['q']);S=lambda s:U(w,*pt105(A6,B6,s))
 axes=[C6+k*d for d in (3.6,6.95,10.3) for k in (-1,1)]
 ops=[(S(s),b,1.30,h) for s in axes for b,h in ((.76,1.87),(4.33,1.57),(7.00,1.59))]
 cu=S(C6);holes=[(u,b,ww,hh,0) for u,b,ww,hh in ops]+[(cu,.15,1.80,2.06,.70),(cu,4.33,1.55,1.40,.45),(cu,7.00,1.45,1.40,.49)]
 bz_wall(m,w['p'],w['q'],0,H,holes,OL)
 for u,b,ww,hh in ops:win105(m,x,y,u,b,ww,hh,a,WH,WH,2)
 archwin105(m,x,y,cu,4.33,1.55,1.40,.45,a,WH,WH,3);archwin105(m,x,y,cu,7.00,1.45,1.40,.49,a,WH,WH,3)
 # The entrance: a glazed brown double door under a glazed arch, a white arched surround, a step.
 pts=[(-.90,.15),(.90,.15)]+arc105(cu,1.80,2.21,.70)
 m.faces([lp(x,y,cu+du,.10,zz,a) for du,zz in pts],[tuple(range(len(pts))),tuple(range(len(pts)-1,-1,-1))],GLAZE)
 for s in (-1,1):
  facade_box(m,x,y,cu+s*.45,.14,1.18,.86,.06,2.06,M['Door'],a);facade_box(m,x,y,cu+s*.45,.18,1.40,.55,.02,1.2,GLAZE,a)
 town_path(m,[lp(x,y,cu+du,.14,zz,a) for du,zz in arc105(cu,1.80,2.21,.70)],.05,M['Door'])
 town_path(m,[lp(x,y,cu+du*1.14,.40,zz+(zz-2.21)*.17,a) for du,zz in arc105(cu,1.80,2.21,.70)],.08,WH)
 for s in (-1,1):facade_box(m,x,y,cu+s*1.02,.39,1.18,.14,.07,2.06,WH,a)
 facade_box(m,x,y,cu,.50,.075,2.3,.30,.15,M['Stone'],a)
 # Lesenes (corner ones wider), the string course broken by them, plinth band, cornice.
 for s,ww in [(C6+k*d,.48) for d in (2.0,5.25,8.5) for k in (-1,1)]+[(.30,.62),(L-.30,.62)]:
  facade_box(m,x,y,S(s),.40,(H-.30+.30)/2,ww,.10,H-.60,WH,a)
 facade_box(m,x,y,0,.39,3.48,L+.02,.08,.16,WH,a);facade_box(m,x,y,0,.39,.15,L+.02,.08,.30,M['Stone'],a)
 cornice105(m,x,y,L,a,H,WH,.35)
hip82(m,'f196',A6,B6,M['Sheet'])
fronts105(m,'b196',lambda *_:False,OL,WH,WH,2,.8);flatroof105(m,'b196',M['Sheet'],OL)
b105_finish(m,'92204196')

# ---- 92204205: grey render over a pale granite-look ground floor; s from the west joint.
m=b105_new(Z['o205']['mesh'],'Kvarnholmen/Strömgatan');GY=M['Grey'];GR=M['Granite']
A5,B5=(-238.58,218.23),(-220.55,217.77);H=Z['o205']['height']
for w in fronts105(m,'o205',S105(0,-1),GY,WH,WH,4,.9):
 x,y,L,a=sf_edge(w['p'],w['q']);S=lambda s:U(w,*pt105(A5,B5,s))
 gops=[(S(s),1.05,ww,1.49) for s,ww in ((2.87,1.45),(6.18,1.40),(8.90,.80),(10.08,.85),(12.63,1.55),(15.82,1.55))]
 uops=[(S(s),b,1.35,h) for s in (3.74,14.75) for b,h in ((3.82,1.72),(6.71,1.85))]
 tops=[(S(s),9.75,ww,1.10) for s,ww in ((3.74,1.35),(6.40,2.10),(12.00,2.10),(14.75,1.35))]
 pu=S(1.0)
 holes=[(u,b,ww,hh,0) for u,b,ww,hh in gops+uops+tops]+[(pu,0,1.50,2.60,0)]
 bz_wall(m,w['p'],w['q'],3.03,H,[hh for hh in holes if hh[1]>3],GY);bz_wall(m,w['p'],w['q'],0,3.03,[hh for hh in holes if hh[1]<3],GR)
 for u,b,ww,hh in gops+uops+tops:
  win105(m,x,y,u,b,ww,hh,a,WH,None,2);facade_box(m,x,y,u,.45,b-.04,ww+.16,.20,.05,WH,a)
  facade_box(m,x,y,u,.62,b+hh+.12,ww+.30,.55,.06,M['Hood'],a)
 # The passage: dark inside, a black bar gate.
 facade_box(m,x,y,pu,-1.0,1.30,1.50,.10,2.60,M['Dark'],a)
 for k in range(9):facade_box(m,x,y,pu-.70+k*.175,.25,1.05,.03,.03,2.10,M['Black'],a)
 for zz in (.15,1.0,2.05):facade_box(m,x,y,pu,.25,zz,1.45,.04,.05,M['Black'],a)
 # Ground floor joints and the band over it.
 for zz in (.35,1.00,1.65,2.30):facade_box(m,x,y,0,.36,zz,L,.02,.025,M['Stone'],a)
 facade_box(m,x,y,0,.42,2.91,L+.04,.14,.24,GR,a)
 # The two box bays over the second and third floors.
 for s in (6.40,12.00):
  bu=S(s);bw,dep,z0,z1=3.30,.60,3.03,8.90
  facade_box(m,x,y,bu,.355+dep/2,(z0+z1)/2,bw,dep,z1-z0,GY,a);facade_box(m,x,y,bu,.355+dep/2+.03,z1+.06,bw+.12,dep+.10,.12,M['Hood'],a)
  for b,h in ((3.25,2.25),(5.95,2.15)):
   # French windows of four lights behind a glazed balustrade.
   o=.355+dep;facade_box(m,x,y,bu,o+.01,b+h/2,2.50,.02,h,GLAZE,a);cas81(m,x,y,bu,b,2.50,h,a,WH,o+.05,2)
   for k in (-1,1):facade_box(m,x,y,bu+k*.625,o+.05,b+h/2,.06,.06,h,WH,a)
   facade_box(m,x,y,bu,o+.12,b+.50,2.50,.02,.95,GLAZE,a);facade_box(m,x,y,bu,o+.12,b+.98,2.55,.05,.05,WH,a)
   facade_box(m,x,y,bu,o+.10,b+h+.10,2.80,.40,.05,M['Hood'],a)
   surround36(m,x,y,bu,b,2.50,h,a,WH,.10,o+.02)
 cornice105(m,x,y,L,a,H,GY,.32)
mansard105(m,'o205',A5,B5,M['Mansard'],1.6)
fw=[w for w in walls('o205','outer') if outward(w)[1]<-.9][0];x,y,L,a=sf_edge(fw['p'],fw['q'])
for s in (6.40,12.00):dormer105(m,x,y,U(fw,*pt105(A5,B5,s)),a,H,1.70,1.10,M['Mansard'],WH,.75,1.6)
b105_finish(m,'92204205')

# ---- 92204158: red brick, s from the west joint.
m=b105_new(Z['r158']['mesh'],'Kvarnholmen/Strömgatan');BR=M['Brick']
A8,B8=(-220.55,217.77),(-203.74,217.97);H=Z['r158']['height']
for w in fronts105(m,'r158',S105(0,-1),BR,WH,WH,3,.8):
 x,y,L,a=sf_edge(w['p'],w['q']);S=lambda s:U(w,*pt105(A8,B8,s))
 gops=[(S(s),.55,.82,.88) for s in (6.13,7.43,9.93,11.13)]
 w2=[(S(s),2.84,2.00,1.15) for s in (3.07,6.70,10.20)];w3=[(S(s),6.26,1.85,1.20) for s in (3.47,6.73,9.77,13.40)]
 gu,du,bu,au=S(2.81),S(13.52),S(15.70),S(14.10)
 holes=[(u,b,ww,hh,0) for u,b,ww,hh in gops+w2+w3]+[(gu,.40,2.40,1.10,0),(du,0,1.20,1.75,.35),(bu,.50,2.50,1.25,0),(au,2.87,2.30,1.40,.70)]
 bz_wall(m,w['p'],w['q'],0,H,holes,BR)
 for u,b,ww,hh in gops:win105(m,x,y,u,b,ww,hh,a,WH,None,2)
 for u,b,ww,hh in w2+w3:
  cas81(m,x,y,u,b,ww,hh,a,WH,.16,2)
  for k in (-1,1):facade_box(m,x,y,u+k*ww/6,.16,b+hh/2,.05,.08,hh,WH,a)
  facade_box(m,x,y,u,.45,b-.05,ww+.20,.16,.06,M['Stone'],a);hood105(m,x,y,u,b+hh+.05,ww+.35,a,M['Hood'])
 archwin105(m,x,y,au,2.87,2.30,1.40,.70,a,WH,WH,3)
 # Low red double gate, arched door in a white surround, the white box window at the east end.
 for k in (-1,1):facade_box(m,x,y,gu+k*.60,.14,.95,1.17,.06,1.10,M['RedGate'],a)
 surround36(m,x,y,gu,.40,2.40,1.10,a,WH,.08,.40)
 pts=[(-.60,0),(.60,0)]+arc105(du,1.20,1.75,.35)
 m.faces([lp(x,y,du+dd,.12,zz,a) for dd,zz in pts],[tuple(range(len(pts))),tuple(range(len(pts)-1,-1,-1))],M['Door'])
 town_path(m,[lp(x,y,du+dd*1.15,.40,zz+(zz-1.75)*.3,a) for dd,zz in arc105(du,1.20,1.75,.35)],.08,WH)
 for k in (-1,1):facade_box(m,x,y,du+k*.69,.39,.88,.16,.07,1.75,WH,a)
 facade_box(m,x,y,bu,.12,1.12,2.50,.02,1.25,GLAZE,a);surround36(m,x,y,bu,.50,2.50,1.25,a,WH,.16,.42);facade_box(m,x,y,bu,.20,1.55,2.50,.10,.08,WH,a)
 facade_box(m,x,y,0,.40,.22,L+.02,.10,.45,M['Plinth'],a)
 facade_box(m,x,y,0,.42,H-.30,L+.04,.14,.24,BR,a);facade_box(m,x,y,0,.50,H-.10,L+.16,.30,.16,BR,a)
mansard105(m,'r158',A8,B8,M['Mansard'],.95)
fw=[w for w in walls('r158','outer') if outward(w)[1]<-.9][0];x,y,L,a=sf_edge(fw['p'],fw['q'])
for s in (3.50,6.50,9.30,12.60):dormer105(m,x,y,U(fw,*pt105(A8,B8,s)),a,H,1.35,1.30,M['Mansard'],WH,.40,1.3)
b105_finish(m,'92204158')

# ---- 92204154: brick over a pale rusticated ground floor; s from the west end (layout estimated
# from one seen window at s 13.7-14.5 and the rustication top at 4.7 m).
m=b105_new(Z['f154']['mesh'],'Kvarnholmen/Strömgatan');RU=M['Rust']
A4,B4=(-253.72,218.48),(-238.58,218.23);H=Z['f154']['height']
for w in fronts105(m,'f154',S105(0,-1),BR,WH,WH,3,.9):
 x,y,L,a=sf_edge(w['p'],w['q']);S=lambda s:U(w,*pt105(A4,B4,s))
 axes=[1.80,4.80,7.60,10.60,13.95]
 gops=[(S(s),1.10,1.25,2.40) for s in axes if s!=7.60];du=S(7.60)
 uops=[(S(s),b,1.15,1.95) for s in axes for b in (5.35,8.55)]
 holes=[(u,b,ww,hh,0) for u,b,ww,hh in gops+uops]+[(du,0,1.40,2.80,.30)]
 bz_wall(m,w['p'],w['q'],4.70,H,[hh for hh in holes if hh[1]>4],BR);bz_wall(m,w['p'],w['q'],0,4.70,[hh for hh in holes if hh[1]<4],RU)
 for u,b,ww,hh in gops:win105(m,x,y,u,b,ww,hh,a,WH,None,3)
 for u,b,ww,hh in uops:win105(m,x,y,u,b,ww,hh,a,WH,WH,3,.16)
 door83(m,x,y,du,0,1.40,2.80,a,M['Door'],WH,glass=True)
 for k in range(1,7):facade_box(m,x,y,0,.37,k*.66,L,.03,.04,M['Stone'],a)
 facade_box(m,x,y,0,.42,4.66,L+.04,.14,.18,WH,a)
 for uq in (-L/2+.25,L/2-.25):
  for k in range(int((H-5.0)/.6)):facade_box(m,x,y,uq,.40,5.0+k*.6+.25,.50 if k%2 else .36,.08,.50,WH,a)
 cornice105(m,x,y,L,a,H,WH,.35)
hip82(m,'f154',A4,B4,M['Mansard'])
fronts105(m,'b154',lambda *_:False,BR,WH,WH,2,.9);flatroof105(m,'b154',M['Mansard'],BR)
b105_finish(m,'92204154')

# ---- 92204191: the green house, generic openings, orange tile saddle along the street.
m=b105_new(Z['g191']['mesh'],'Kvarnholmen/Strömgatan')
fronts105(m,'g191',lambda *_:False,M['Green'],WH,WH,2,.8)
saddle82(m,'g191',(-199.6,217.95),(-190.79,218.03),M['Tile'],M['Green'],along=True)
b105_finish(m,'92204191')

# ---- 92379281 (10 Strömgatan): yellow brick, s from the east end of the north front. The camera's
# position along the street is the panorama's (no corner in view), so positions carry +-1.5 m.
m=b105_new(Z['y281']['mesh'],'Kvarnholmen/Strömgatan');YB=M['Yellow'];BL=M['Black']
A1,B1=(-123.78,205.50),(-153.56,205.61);H=Z['y281']['height']
for w in fronts105(m,'y281',S105(0,1),YB,BL,YB,4,.9):
 x,y,L,a=sf_edge(w['p'],w['q']);S=lambda s:U(w,*pt105(A1,B1,s))
 axes=[3.15,5.85,8.10,10.60,12.68,14.95,16.98,19.05,21.90,24.40,26.80]
 gops=[(S(s),1.10,1.25,1.86) for s in axes if s not in (8.10,19.05)]
 uops=[(S(s),b,1.20,1.70) for s in axes for b in (4.23,7.21,10.20)]
 gu,du=S(8.10),S(19.05)
 holes=[(u,b,ww,hh,0) for u,b,ww,hh in gops+uops]+[(gu,0,2.85,2.54,.37),(du,.52,1.42,2.50,0)]
 bz_wall(m,w['p'],w['q'],0,H,holes,YB)
 for u,b,ww,hh in gops+uops:
  cas81(m,x,y,u,b,ww,hh,a,BL,.18,3);facade_box(m,x,y,u,.45,b-.04,ww+.10,.14,.06,M['Stone'],a)
 # Arched black double gate with a glazed fanlight.
 pts=[(-1.425,2.10),(1.425,2.10)]+arc105(gu,2.85,2.54,.37)
 m.faces([lp(x,y,gu+dd,.08,zz,a) for dd,zz in pts],[tuple(range(len(pts))),tuple(range(len(pts)-1,-1,-1))],GLAZE)
 for k in (-1,1):
  facade_box(m,x,y,gu+k*.71,.12,1.05,1.38,.06,2.10,BL,a)
  for j in range(1,10):facade_box(m,x,y,gu+k*.71,.16,j*.21,1.30,.02,.03,M['Dark'],a)
 town_path(m,[lp(x,y,gu+dd,.14,zz,a) for dd,zz in arc105(gu,2.85,2.54,.37)],.05,BL);facade_box(m,x,y,gu,.14,2.12,2.85,.05,.06,BL,a)
 # Recessed red door: a deep brick niche with steps up to the door at its back.
 facade_box(m,x,y,du,-.60,2.02,1.42,.06,2.50,M['RedDoor'],a)
 for k in range(3):facade_box(m,x,y,du,-.10-.15*k,.52+.17*k,1.42,1.0-.30*k,.17,M['Stone'],a)
 for k in (-1,1):facade_box(m,x,y,du+k*.72,-.15,1.80,.04,.95,2.50,YB,a)
 facade_box(m,x,y,du,-.15,3.04,1.46,.95,.08,YB,a)
 facade_box(m,x,y,0,.40,.26,L+.02,.12,.52,M['Stone'],a)
 for zz in (4.06,7.04,10.02):facade_box(m,x,y,0,.40,zz,L+.02,.09,.14,YB,a)
 cornice105(m,x,y,L,a,H,YB,.35)
saddle82(m,'y281',A1,B1,M['Mansard'],YB,along=True)
fronts105(m,'w281',lambda *_:False,YB,BL,YB,4,.9);saddle82(m,'w281',A1,B1,M['Mansard'],YB,along=False)
b105_finish(m,'92379281')

# ---- 91285791: not photographed; a generic rendered volume, plain windows, flat roof.
m=b105_new(Z['k791']['mesh'],'Kvarnholmen/Södra Kanalgatan')
fronts105(m,'k791',lambda *_:False,M['Render'],WH,WH,3,.9);flatroof105(m,'k791',M['Sheet'],M['Render'])
b105_finish(m,'91285791')

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block105_cameras=[
 sv_camera('519_Block105_Cal_Olive',-230.35,213.99,2.25,153,15,90),
 sv_camera('520_Block105_Cal_Grey',-230.23,213.16,2.50,333,15,90),
 sv_camera('521_Block105_Cal_Brick',-214.02,210.73,3.03,332,15,90),
 sv_camera('522_Block105_Cal_Yellow',-136.49,210.30,2.40,153,15,90),
 ('523_Block105_Aerial',(-190.0,170.0,45.0),(-190.0,215.0,4.0),28),
]
print('BLOCK105_GEOMETRY',len(block105_names),'dropped',block105_dropped)
