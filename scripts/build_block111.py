"""Pass 111: the last street-facing generic pass-17 volumes scattered round the island.
- 91926352 (50 Storgatan, SM_Building_91926352): the 1940s grey-beige rendered block: the
  four-storey range on a dark slate plinth with five window axes in white surrounds, beige roller
  blinds, a cornice and a flat roof; the three-storey wing set back to the east, the same render,
  basement windows in the plinth;
- 91926324: the light-grey 1.5-storey house: four green-framed windows on a grey plinth, a red tile
  saddle roof with a red dormer, two pairs of roof lights and a chimney;
- 91926325: the green board gate, the low grey one-storey wing with one window in a white surround
  and white corner strips under a low red roof, the white two-storey part behind it (estimated
  beyond its front), the white yard wall with an iron gate;
- 91846953 (1 Proviantgatan): sage-green render on a dark plinth, white corner and pilaster strips,
  a white string course and cornice, five window axes in white surrounds with panels under the
  sills, a green double door, the central pediment with a lunette and a low red hipped roof; the
  wing to the south-west plain (not seen);
- 91846937 (30 Ölandsgatan): the small yellow boarded house: horizontal boards, white corner boards,
  two board-clad garage doors, the red door up two steps in a white pedimented surround, a red
  tile hip roof;
- 91931337 (Stationsgatan): the grill kiosk: red posts, white panels, glazing on the street faces,
  green awnings, a dark sign band round the top and a low dark roof;
- 149000060 (Ölandskajen): the white corrugated shed: the east part flat-roofed, the west part
  lower with its roofline sweeping up to the west end, window strips, two blue round logos;
- 91072716: Gamla vattentornet at Larmtorget: a tapering red brick shaft with stone bands and small
  round windows, a stone corbel table, the brick crown with arched windows, a crenellated parapet
  with stone coping and a low roof cap; the small annex on the east side (estimated).

References: eight Google Street View panoramas (resected where two or more known corners were
visible), view only. Zones: source/block111.json; see references/block111-notes.md. Cars, signs'
lettering, lamps, antennas and pipes are omitted.
"""
B111D=json.loads((R/'source/block111.json').read_text());Z=B111D['zones']
block111_names=[];B111={}
for old in [k for k in list(materials) if k.startswith('M_Block111_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('White','TownPaintWhite',(.93,.93,.91),.60,0),('Dark','TownMetalGrey',(.07,.07,.075),.45,.40),('Sheet','TownMetalGrey',(.36,.37,.38),.55,.25),
 ('Tile','TownTileRed',(.76,.39,.25),.80,0),('Iron','TownMetalGrey',(.08,.08,.085),.45,.40),
 ('Render52','TownIvory',(.64,.61,.56),.92,0),('Slate','TownStone',(.20,.21,.22),.80,0),('Blind','TownIvory',(.55,.49,.41),.85,0),
 ('LightGrey','TownIvory',(.80,.79,.75),.90,0),('Plinth','TownStone',(.60,.60,.58),.90,0),('Green','TownPaintGreen',(.42,.52,.30),.60,0),
 ('DormerRed','TownPaintBrown',(.68,.27,.19),.60,0),('Chimney','TownTileRed',(.60,.30,.24),.85,0),
 ('Wing','TownIvory',(.80,.80,.77),.90,0),('GateGreen','TownPaintGreen',(.58,.70,.57),.65,0),('WallWhite','TownPaintWhite',(.89,.88,.84),.70,0),
 ('Sage','TownIvory',(.57,.62,.54),.90,0),('Trim53','TownPaintWhite',(.90,.90,.87),.65,0),('Plinth53','TownStone',(.40,.40,.40),.90,0),
 ('Frame53','TownPaintGreen',(.16,.28,.19),.60,0),('Tile53','TownTileRed',(.62,.32,.24),.80,0),
 ('Yellow','TownIvory',(.88,.76,.45),.85,0),('RedDoor','TownPaintBrown',(.60,.18,.15),.60,0),('Groove','TownIvory',(.70,.59,.33),.85,0),
 ('KioskRed','TownPaintBrown',(.62,.25,.22),.60,0),('Panel','TownPaintWhite',(.90,.88,.84),.70,0),('Awning','TownPaintGreen',(.20,.42,.35),.70,0),
 ('Navy','TownPaintWhite',(.12,.14,.20),.55,0),('RoofDark','TownMetalGrey',(.24,.25,.26),.60,.20),
 ('Shed','TownPaintWhite',(.90,.90,.89),.60,0),('Rib','TownPaintWhite',(.82,.82,.81),.60,0),('Logo','TownPaintWhite',(.30,.60,.85),.60,0),
 ('Brick','TownTileRed',(.55,.27,.20),.90,0),('Stone','TownStone',(.70,.66,.58),.90,0),('Cap','TownMetalGrey',(.30,.31,.32),.55,.30),
 ]:
 name='M_Block111_'+key;B111[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block111_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B111;WH=M['White']

def b111_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block111_names.append(name);return Mesh(name,category)
def drop_degenerate_faces111(obj,tol=1e-9):
 import bmesh
 bm=bmesh.new();bm.from_mesh(obj.data)
 def _thin(f):
  L=max(e.calc_length() for e in f.edges);return L>0 and 2*f.calc_area()/L<1e-4
 bad=[f for f in bm.faces if f.calc_area()<tol or len({v.index for v in f.verts})<len(f.verts) or _thin(f)]
 if bad:bmesh.ops.delete(bm,geom=bad,context='FACES_ONLY')
 bm.to_mesh(obj.data);bm.free();obj.data.update();return len(bad)
block111_dropped={}
def b111_finish(m,osm):
 obj=s21_finish(m);block111_dropped[obj.name]=drop_degenerate_faces111(obj)
 obj['detail_pass']=111;obj['reference_notes']='references/block111-notes.md';obj['osm_way']=osm;return obj

def pt111(a,b,s):
 # The point s metres from a towards b.
 L=math.dist(a,b);return (a[0]+(b[0]-a[0])*s/L,a[1]+(b[1]-a[1])*s/L)
def fronts111(m,zone,test,wall,frame,trim,levels,floor0=1.0):
 # Party and upper walls in the wall material, other outer walls plain; returns the street fronts.
 H=Z[zone]['height'];out=[]
 for w in walls(zone):
  if w['kind']!='outer':bz_wall(m,w['p'],w['q'],w['z0'],H,[],wall);continue
  ox,oy=outward(w)
  if test(ox,oy):out.append(w);continue
  plain(m,w,H,wall,frame,trim,levels,floor0)
 return out
def flatroof111(m,zone,ma,trim,coping=.24,z=None):
 # Flat roof (triangulated, the outlines can be concave) and a parapet coping on the outer walls.
 from mathutils import Vector
 from mathutils.geometry import tessellate_polygon
 H=Z[zone]['height'] if z is None else z
 for g in Z[zone]['polygons']:
  vs=[(*v,H+.02) for v in g];tris=tessellate_polygon([[Vector(v) for v in vs]])
  m.faces(vs,[tuple(t) for t in tris]+[tuple(reversed(t)) for t in tris],ma)
 if trim:
  for w in walls(zone,'outer'):
   x,y,L,a=sf_edge(w['p'],w['q']);facade_box(m,x,y,0,.38,H+coping/2,L+.06,.12,coping,trim,a)
def prism111(m,x,y,u,outline,o0,o1,ma,a):
 # A closed prism of a convex face outline [(du,z)] between the offsets o0 and o1.
 n=len(outline);vs=[lp(x,y,u+du,o,zz,a) for o in (o0,o1) for du,zz in outline]
 m.faces(vs,[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],ma)
def win111(m,x,y,u,b,w,h,a,frame,sur,rows=2,bw=.14,sill=None):
 cas81(m,x,y,u,b,w,h,a,frame,.16,rows)
 if sur:surround36(m,x,y,u,b,w,h,a,sur,bw,.40)
 if sill:facade_box(m,x,y,u,.47,b-.05,w+.30,.16,.07,sill,a)
FRONT111=lambda dx,dy:(lambda ox,oy:ox*dx+oy*dy>.9)
def front_wall111(zone,dx,dy):return [w for w in walls(zone,'outer') if outward(w)[0]*dx+outward(w)[1]*dy>.9]

# ---- 91926352 (50 Storgatan): the four-storey range, s from the west corner along the front.
# Measured from the resected panorama (camera 117.07, -6.55, h 2.55): plinth 2.10, window rows at
# 2.30/5.30/8.35/11.40 (1.65 high), cornice 13.6-14.5; five axes at a 2.9 m pitch round s 6.88.
m=b111_new(Z['m352']['mesh'],'Kvarnholmen/Storgatan');RE=M['Render52'];SL=M['Slate']
A2,B2=(111.40,1.353),(125.154,1.254)
BLIND111=[[0,1,1,0,1],[1,0,1,1,1],[0,1,0,1,0],[1,0,1,1,1]]
def block52(w,H,axes,rows,plinth,cor,seen=True):
 x,y,L,a=sf_edge(w['p'],w['q'])
 holes=[(u,b,1.25,1.65,0) for u in axes for b in rows]
 bh=[(u,.55,.90,.60,0) for u in axes] if not seen else []
 bz_wall(m,w['p'],w['q'],0,H,holes+bh,RE)
 for j,b in enumerate(rows):
  for k,u in enumerate(axes):
   win111(m,x,y,u,b,1.25,1.65,a,WH,WH,2,.13,None)
   if BLIND111[j%4][k%5]:facade_box(m,x,y,u,.135,b+1.65-.55,1.18,.02,1.05,M['Blind'],a)
 for u,b,ww,hh,r in bh:cas81(m,x,y,u,b,ww,hh,a,WH,.16,1);facade_box(m,x,y,u,.44,b+hh/2,ww+.05,.03,hh+.05,M['Iron'],a)
 facade_box(m,x,y,0,.42,plinth/2,L+.04,.14,plinth,SL,a)
 facade_box(m,x,y,0,.42,cor-.40,L+.04,.14,.30,RE,a);facade_box(m,x,y,0,.55,H-.12,L+.30,.40,.24,M['Plinth'],a)
for w in fronts111(m,'m352',FRONT111(0,-1),RE,WH,RE,4,2.3):
 S=lambda s:U(w,*pt111(A2,B2,s))
 block52(w,14.5,[S(6.88+k*2.9) for k in (-2,-1,0,1,2)],(2.30,5.30,8.35,11.40),2.10,14.0)
flatroof111(m,'m352',M['Sheet'],None)
# The wing, set back 2.4 m: three rows over the plinth with basement windows (9 axes, 2.35 m).
for w in fronts111(m,'w352',FRONT111(0,-1),RE,WH,RE,3,2.4):
 x,y,L,a=sf_edge(w['p'],w['q'])
 block52(w,11.0,[-L/2+1.30+k*2.35 for k in range(9)],(2.40,5.30,8.20),2.00,10.6,False)
flatroof111(m,'w352',M['Sheet'],None)
b111_finish(m,'91926352')

# ---- 91926324: the light-grey 1.5-storey house, s from the west corner (146.385, 1.326).
# Eaves 4.3, ridge 9.4 (resected camera 146.08, -7.10); windows 1.95-3.70; plinth to 0.90.
m=b111_new(Z['h324']['mesh'],'Kvarnholmen/Storgatan');LG=M['LightGrey'];GR=M['Green']
A4,B4=(146.385,1.326),(156.805,1.107);H=Z['h324']['height'];T=Z['h324']['top']
for w in fronts111(m,'h324',FRONT111(0,-1),LG,WH,LG,1,1.6):
 x,y,L,a=sf_edge(w['p'],w['q']);S=lambda s:U(w,*pt111(A4,B4,s))
 ax=[S(s) for s in (2.00,4.15,6.55,8.55)]
 bz_wall(m,w['p'],w['q'],0,H,[(u,1.95,1.20,1.75,0) for u in ax]+[(S(1.0),.30,.55,.35,0),(S(9.6),.30,.55,.35,0)],LG)
 for u in ax:
  cas81(m,x,y,u,1.95,1.20,1.75,a,GR,.16,3);surround36(m,x,y,u,1.95,1.20,1.75,a,GR,.07,.38)
  facade_box(m,x,y,u,.46,1.90,1.40,.18,.06,M['Sheet'],a)
 for s in (1.0,9.6):facade_box(m,x,y,S(s),.30,.475,.55,.04,.35,M['Plinth'],a)
 facade_box(m,x,y,0,.40,.45,L+.02,.10,.90,M['Plinth'],a)
 facade_box(m,x,y,0,.42,H-.12,L+.04,.16,.24,WH,a)
 town_rod(m,lp(x,y,-L/2+.15,.50,.20,a),lp(x,y,-L/2+.15,.50,H,a),.05,M['Sheet'],8)
 town_rod(m,lp(x,y,L/2-.15,.50,.20,a),lp(x,y,L/2-.15,.50,H,a),.05,M['Sheet'],8)
 FW4=(x,y,L,a,S)
r4=saddle82(m,'h324',A4,B4,M['Tile'],LG)
x,y,L,a,S=FW4;half4=4.54;sl4=(T-H)/half4
# The red dormer over the middle window, two pairs of roof lights, the chimney.
dormer82(m,x,y,S(4.35),a,H,sl4,1.60,1.05,M['DormerRed'],GR,M['DormerRed'],1.4)
for s in (1.05,1.95,5.85,6.75):
 d=2.2;X,Y,_=lp(x,y,S(s),.355-d,0,a);skylight82(m,X,Y,H+(d-.355)*sl4,a,sl4)
X,Y,_=lp(x,y,S(1.75),.355-5.6,0,a);chimney82(m,X,Y,8.0,11.0,M['Chimney'])
b111_finish(m,'91926324')

# ---- 91926325: gate, wing, the two-storey part behind and the yard (resected camera 158.01,
# -7.58). s from the west corner (156.805, 1.107) along the street.
m=b111_new(Z['gw325']['mesh'],'Kvarnholmen/Storgatan');WG=M['Wing'];WW=M['WallWhite']
A5,B5=(156.805,1.107),(166.302,0.916)
for w in front_wall111('gw325',0,-1):
 x,y,L,a=sf_edge(w['p'],w['q']);S=lambda s:U(w,*pt111(A5,B5,s))
 bz_wall(m,w['p'],w['q'],0,3.0,[(S(1.22),0,1.74,2.72,0)],WW)
 for k in (-1,1):
  facade_box(m,x,y,S(1.22)+k*.435,.14,1.36,.85,.06,2.72,M['GateGreen'],a)
  for j in range(1,5):facade_box(m,x,y,S(1.22)+k*.435-.425+j*.17,.18,1.36,.025,.02,2.72,M['Green'],a)
 surround36(m,x,y,S(1.22),0,1.74,2.72,a,WW,.10,.40);facade_box(m,x,y,0,.45,2.95,L+.06,.20,.10,M['Sheet'],a)
for w in fronts111(m,'lw325',FRONT111(0,-1),WG,WH,WG,1,1.3):
 x,y,L,a=sf_edge(w['p'],w['q']);S=lambda s:U(w,*pt111(A5,B5,s))
 u=S(4.25);bz_wall(m,w['p'],w['q'],0,3.2,[(u,1.50,1.05,1.30,0)],WG)
 win111(m,x,y,u,1.50,1.05,1.30,a,WH,WH,2,.15,WH)
 for s in (-L/2+.12,L/2-.12):facade_box(m,x,y,s,.42,1.6,.24,.12,3.2,WW,a)
 facade_box(m,x,y,0,.40,.22,L+.02,.10,.45,M['Plinth'],a)
saddle82(m,'lw325',(159.0,1.063),(163.1,0.98),M['Tile'],WG,True,.25)
for w in walls('bk325'):
 if w['kind']!='outer':
  x,y,L,a=sf_edge(w['p'],w['q']);holes=[]
  if outward(w)[1]<-.9 and w['z0']>3.1:holes=[(0,4.55,.95,1.15,0)]
  bz_wall(m,w['p'],w['q'],w['z0'],6.4,holes,WW)
  for h_ in holes:win111(m,x,y,h_[0],h_[1],h_[2],h_[3],a,WH,None,2)
 else:plain(m,w,6.4,WW,WH,WW,2,.9)
saddle82(m,'bk325',(156.878,4.5),(163.1,4.5),M['Tile'],WW,True,.30)
X,Y=158.6,8.2;chimney82(m,X,Y,7.3,8.9,M['Chimney'])
# The yard: the white wall on the street with the iron gate, the back wall; open inside.
for w in walls('yd325','outer'):
 x,y,L,a=sf_edge(w['p'],w['q'])
 if outward(w)[1]<-.9:
  S=lambda s:U(w,*pt111(A5,B5,s));g=S(8.85)
  bz_wall(m,w['p'],w['q'],0,2.0,[(g,0,1.15,2.0,0)],WW)
  for k in range(10):facade_box(m,x,y,g-.53+k*.118,.20,1.0,.025,.025,1.9,M['Iron'],a)
  for zz in (.15,1.0,1.85):facade_box(m,x,y,g,.20,zz,1.15,.03,.04,M['Iron'],a)
  for s in (-1,1):facade_box(m,x,y,g+s*.70,.30,1.1,.26,.40,2.2,WW,a)
 else:bz_wall(m,w['p'],w['q'],0,2.0,[],WW)
 facade_box(m,x,y,0,.30,2.04,L+.04,.42,.08,M['Plinth'],a)
b111_finish(m,'91926325')

# ---- 91846953 (1 Proviantgatan), s from the south corner (175.007, -112.191) along the east
# front. Resected camera (182.81, -109.60, h 2.5): plinth 0.95, ground windows 1.80-3.55, string
# course 3.9-4.5, upper windows 4.95-6.90, cornice 7.6-8.4, pediment apex 10.7 over s 4.3-12.9.
m=b111_new(Z['f953']['mesh'],'Kvarnholmen/Proviantgatan');SG=M['Sage'];TR=M['Trim53'];FR=M['Frame53']
A3,B3=(175.007,-112.191),(175.629,-95.018);H=Z['f953']['height']
for w in fronts111(m,'f953',FRONT111(1,0),SG,FR,TR,2,1.8):
 x,y,L,a=sf_edge(w['p'],w['q']);S=lambda s:U(w,*pt111(A3,B3,s))
 axes=[2.1,4.4,7.15,10.05,12.8];door=15.1
 lo=[(S(s),1.80,1.05,1.75,0) for s in axes];up=[(S(s),4.95,1.05,1.95,0) for s in axes+[door]]
 dh=(S(door),.95,1.30,2.60,0)
 bz_wall(m,w['p'],w['q'],0,H,lo+up+[dh],SG)
 for u,b,ww,hh,r in lo+up:
  win111(m,x,y,u,b,ww,hh,a,FR,TR,3,.16,TR)
  facade_box(m,x,y,u,.40,b-.42,ww+.32,.05,.62,TR,a);facade_box(m,x,y,u,.36,b-.42,ww-.10,.04,.40,SG,a)
 u=dh[0];door83(m,x,y,u,.95,1.30,2.60,a,FR,TR,glass=True);facade_box(m,x,y,u,.14,2.25,.04,.05,2.60,M['Dark'],a)
 facade_box(m,x,y,u,.44,3.72,1.80,.18,.14,TR,a)
 for k in range(2):facade_box(m,x,y,u,.55+.15*k,.24+k*.32,1.70,.30,.32,M['Plinth53'],a)
 for s,ww in ((.30,.60),(5.70,.60),(11.50,.60),(L-.30,.60)):
  facade_box(m,x,y,S(s) if .5<s<L-.5 else (s-L/2),.42,(.95+7.6)/2,ww,.14,7.6-.95,TR,a)
  for zz in (1.4,2.0,2.6,3.2):facade_box(m,x,y,S(s) if .5<s<L-.5 else (s-L/2),.50,zz,ww+.02,.03,.04,SG,a)
 facade_box(m,x,y,0,.40,.47,L+.02,.10,.95,M['Plinth53'],a)
 facade_box(m,x,y,0,.44,4.20,L+.06,.18,.60,TR,a);facade_box(m,x,y,0,.52,4.50,L+.10,.20,.10,TR,a)
 facade_box(m,x,y,0,.44,8.00,L+.06,.18,.80,TR,a);facade_box(m,x,y,0,.58,8.36,L+.30,.40,.12,TR,a)
 # The pediment: tympanum, raking cornices, the lunette.
 pc=S(8.6);pw=8.6;pz=8.42;pr=10.7-pz
 prism111(m,x,y,pc,[(-pw/2,pz),(pw/2,pz),(0,pz+pr)],.02,.38,SG,a)
 for s_ in (-1,1):town_path(m,[lp(x,y,pc+s_*(pw/2+.15),.52,pz+.02,a),lp(x,y,pc,.52,pz+pr+.14,a)],.12,TR)
 k=16;r=.68;zc=pz+.32
 m.faces([lp(x,y,pc+r*math.cos(t*math.pi/k),.40,zc+r*math.sin(t*math.pi/k),a) for t in range(k+1)],[tuple(range(k+1)),tuple(range(k,-1,-1))],GLAZE)
 town_path(m,[lp(x,y,pc+(r+.06)*math.cos(t*math.pi/k),.44,zc+(r+.06)*math.sin(t*math.pi/k),a) for t in range(k+1)],.07,TR)
 for t in (1,2,3):town_rod(m,lp(x,y,pc,.43,zc,a),lp(x,y,pc+r*math.cos(t*math.pi/4),.43,zc+r*math.sin(t*math.pi/4),a),.03,TR,6)
 facade_box(m,x,y,pc,.43,zc,2*r+.1,.04,.06,TR,a)
hip82(m,'f953',A3,B3,M['Tile53'])
fronts111(m,'w953',lambda *_:False,SG,FR,TR,2,1.8)
hip82(m,'w953',(149.714,-119.256),(169.386,-116.162),M['Tile53'])
b111_finish(m,'91846953')

# ---- 91846937 (30 Ölandsgatan), s from the west corner (129.215, -143.544). Resected camera
# (130.49, -154.68, h 2.58): eaves 4.2, garage panels 0-2.2, door 0.60-2.85, pediment top 3.8.
m=b111_new(Z['y937']['mesh'],'Kvarnholmen/Ölandsgatan');YE=M['Yellow'];RD=M['RedDoor']
A7,B7=(129.215,-143.544),(137.174,-143.731);H=Z['y937']['height']
def boards111(m,x,y,L,a,z0,z1,ma,step=.20,o=.37):
 for k in range(1,int((z1-z0)/step)):facade_box(m,x,y,0,o,z0+k*step,L-.70,.03,.03,ma,a)
for w in walls('y937','outer'):
 x,y,L,a=sf_edge(w['p'],w['q'])
 if outward(w)[1]<-.9:
  S=lambda s:U(w,*pt111(A7,B7,s));dc=S(3.98)
  bz_wall(m,w['p'],w['q'],0,H,[(dc,.60,.95,2.25,0)],YE)
  boards111(m,x,y,L,a,2.25,H-.15,M['Groove'])
  for c,s0,s1 in ((0,.40,2.87),(1,5.10,7.60)):
   u=S((s0+s1)/2);ww=s1-s0
   facade_box(m,x,y,u,.40,1.10,ww,.04,2.20,YE,a)
   for k in range(1,11):facade_box(m,x,y,u,.43,k*.20,ww-.06,.025,.025,M['Groove'],a)
   for s_ in (-1,1):facade_box(m,x,y,u+s_*ww/2,.44,1.12,.07,.06,2.24,M['Groove'],a)
   facade_box(m,x,y,u,.44,2.22,ww+.07,.06,.06,M['Groove'],a);facade_box(m,x,y,u,.46,.25,.30,.04,.10,M['Dark'],a)
  door83(m,x,y,dc,.60,.95,2.25,a,RD,WH,glass=False);facade_box(m,x,y,dc,.17,1.85,.55,.03,.40,M['Groove'],a)
  for s_ in (-1,1):facade_box(m,x,y,dc+s_*.90,.42,(.60+3.30)/2,.42,.12,3.30-.60,WH,a)
  facade_box(m,x,y,dc,.44,3.30,2.25,.16,.14,WH,a)
  prism111(m,x,y,dc,[(-1.18,3.37),(1.18,3.37),(0,3.82)],.40,.56,WH,a)
  for k in range(3):facade_box(m,x,y,dc,.55+.30*(2-k)/2,.10+k*.20,1.50,.30*(3-k),.20,M['Plinth'],a)
 else:
  bz_wall(m,w['p'],w['q'],0,H,[],YE);boards111(m,x,y,L,a,.30,H-.15,M['Groove'])
 for s_ in (-L/2+.17,L/2-.17):facade_box(m,x,y,s_,.42,H/2,.34,.14,H,WH,a)
 facade_box(m,x,y,0,.44,H-.12,L+.06,.18,.24,WH,a);facade_box(m,x,y,0,.38,.15,L+.02,.08,.30,M['Plinth'],a)
hip82(m,'y937',A7,B7,M['Tile'])
b111_finish(m,'91846937')

# ---- 91931337: the grill kiosk (resected camera -369.5, -132.9; base hidden, h 2.5 assumed).
# Roof edge 3.4, sign band 3.4-4.25 on the street faces, glazing 1.0-2.6, a low dark roof.
m=b111_new(Z['k337']['mesh'],'Kvarnholmen/Stationsgatan');KR=M['KioskRed'];PN=M['Panel']
H=Z['k337']['height']
for w in walls('k337','outer'):
 x,y,L,a=sf_edge(w['p'],w['q']);ox,oy=outward(w);street=ox<-.9 or oy<-.9
 bz_wall(m,w['p'],w['q'],0,1.0,[],PN)
 n=max(1,round(L/1.55));bays=[(-L/2+(k+.5)*L/n,L/n-.22) for k in range(n)]
 if street and L>3:
  bz_wall(m,w['p'],w['q'],1.0,2.65,[(u,1.0,ww,1.65,0) for u,ww in bays],PN)
  for u,ww in bays:
   facade_box(m,x,y,u,.18,1.825,ww,.02,1.65,GLAZE,a)
   facade_box(m,x,y,u,.22,1.03,ww,.06,.06,KR,a);facade_box(m,x,y,u,.22,2.62,ww,.06,.06,KR,a)
  awning82(m,x,y,0,2.68,L-.30,a,M['Awning'],.32,.55)
 else:
  bz_wall(m,w['p'],w['q'],1.0,2.65,[],PN)
 bz_wall(m,w['p'],w['q'],2.65,H,[],PN)
 for k in range(n+1):facade_box(m,x,y,max(-L/2+.08,min(L/2-.08,-L/2+k*L/n)),.42,H/2,.16,.14,H,KR,a)
 for zz in (.95,):facade_box(m,x,y,0,.42,zz,L+.02,.12,.08,KR,a)
 facade_box(m,x,y,0,.47,H-.10,L+.12,.24,.20,KR,a)
 if street and L>3:
  facade_box(m,x,y,0,.62,H+.42,L+.20,.10,.85,M['Navy'],a);facade_box(m,x,y,0,.64,H+.86,L+.24,.14,.05,KR,a)
flatroof111(m,'k337',M['RoofDark'],None)
kr=[(-361.48,-125.48),(-354.50,-125.62),(-354.42,-117.94),(-361.33,-117.80)]
inset_roof(m,kr,H,2.0,Z['k337']['top']-H,M['RoofDark'],.35)
b111_finish(m,'91931337')

# ---- 149000060: the shed. The east part (s 0-17.4 from the east end) eaves 3.0 under a low
# saddle; the west part 2.6 with its roofline sweeping up to 3.6 at the west end (camera from
# the ground line, h 2.5, at -417.75, -256.60; upscaled half tile).
m=b111_new(Z['e060']['mesh'],'Kvarnholmen/Ölandskajen');SH=M['Shed'];RB=M['Rib']
EE,WE=(-404.553,-265.874),(-435.0,-270.693)
def ribs111(m,x,y,L,a,ztop,o=.37,step=.30):
 n=max(2,int(L/step))
 for k in range(1,n):
  u=-L/2+k*L/n;zt=ztop(u) if callable(ztop) else ztop
  facade_box(m,x,y,u,o,zt/2,.04,.03,zt-.06,RB,a)
def logo111(m,x,y,u,zc,r,a):
 k=24;m.faces([lp(x,y,u+r*math.cos(t*math.tau/k),.375,zc+r*math.sin(t*math.tau/k),a) for t in range(k)],[tuple(range(k)),tuple(range(k-1,-1,-1))],M['Logo'])
for w in fronts111(m,'e060',lambda ox,oy:True,SH,WH,SH,1,1.0):
 x,y,L,a=sf_edge(w['p'],w['q']);ox,oy=outward(w);north=oy>.9
 holes=[(U(w,*pt111(EE,WE,14.75)),1.55,5.0,.75,0)] if north else []
 bz_wall(m,w['p'],w['q'],0,3.0,holes,SH);ribs111(m,x,y,L,a,3.0)
 for u,b,ww,hh,r in holes:
  facade_box(m,x,y,u,.18,b+hh/2,ww,.02,hh,GLAZE,a)
  for k in range(5):facade_box(m,x,y,u-ww/2+k*ww/4,.22,b+hh/2,.06,.06,hh,M['Sheet'],a)
 if north:
  logo111(m,x,y,U(w,*pt111(EE,WE,4.6)),1.55,.70,a)
  u=U(w,*pt111(EE,WE,2.4));facade_box(m,x,y,u,.20,1.0,.95,.04,2.0,M['Sheet'],a)
 facade_box(m,x,y,0,.42,2.95,L+.06,.14,.10,SH,a)
saddle82(m,'e060',(-420.702,-275.125),(-403.525,-272.412),SH,SH,True,.20)
# The west part: walls and roof follow zt(s), s from the joint towards the west end.
J0,J1=(-421.736,-268.594),(-420.702,-275.125);LW=math.dist(J0,WE)
tw=((WE[0]-J0[0])/LW,(WE[1]-J0[1])/LW)
zt111=lambda s:2.6+1.0*max(0,(s-6.0)/(LW-6.0))**2
for w in walls('w060','outer'):
 x,y,L,a=sf_edge(w['p'],w['q']);ox,oy=outward(w)
 sp=(w['p'][0]-J0[0])*tw[0]+(w['p'][1]-J0[1])*tw[1];sq=(w['q'][0]-J0[0])*tw[0]+(w['q'][1]-J0[1])*tw[1]
 if abs(sq-sp)<1.0:
  # The west end wall.
  zz=zt111(LW);bz_wall(m,w['p'],w['q'],0,zz,[],SH);ribs111(m,x,y,L,a,zz);continue
 n=24;sgn=1 if sq>sp else -1
 zs=lambda u:zt111(sp+sgn*(u+L/2))
 for k in range(n):
  u0=-L/2+k*L/n;u1=-L/2+(k+1)*L/n
  prism111(m,x,y,0,[(u0,0),(u1,0),(u1,zs(u1)),(u0,zs(u0))],.005,.355,SH,a)
 ribs111(m,x,y,L,a,zs)
 if oy>.9:
  s0=U(w,*pt111(EE,WE,17.6));s1=U(w,*pt111(EE,WE,23.4));uc=(s0+s1)/2;ww=abs(s1-s0)
  facade_box(m,x,y,uc,.39,2.20,ww,.02,.45,GLAZE,a)
  for k in range(7):facade_box(m,x,y,uc-ww/2+k*ww/6,.41,2.20,.05,.03,.45,M['Sheet'],a)
  logo111(m,x,y,U(w,*pt111(EE,WE,21.3)),1.45,.62,a)
# The roof over the west part: strips across the depth, 0.20 m eaves at the sides.
nw=(-tw[1],tw[0]) if (-tw[1])*(J1[0]-J0[0])+tw[0]*(J1[1]-J0[1])>0 else (tw[1],-tw[0])
dw=abs((J1[0]-J0[0])*nw[0]+(J1[1]-J0[1])*nw[1])
P060=lambda s,t:(J0[0]+tw[0]*s+nw[0]*t,J0[1]+tw[1]*s+nw[1]*t)
ss=[LW*k/24 for k in range(25)]+[LW+.20]
for s0,s1 in zip(ss,ss[1:]):
 q=[(*P060(s0,-.20),zt111(min(s0,LW))),(*P060(s1,-.20),zt111(min(s1,LW))),(*P060(s1,dw+.20),zt111(min(s1,LW))),(*P060(s0,dw+.20),zt111(min(s0,LW)))]
 m.faces(q,[(0,1,2,3),(3,2,1,0)],SH)
b111_finish(m,'149000060')

# ---- 91072716: Gamla vattentornet. Heights scaled from one panorama at 48 m (nominal position,
# not resectable): corbel table 40.0-41.8, parapet top 54.5 (+-4 m); radius 6.8 at the base from
# the outline, the crown 5.95 (its silhouette in the photo).
m=b111_new(Z['t716']['mesh'],'Kvarnholmen/Larmtorget');BK=M['Brick'];STN=M['Stone']
TX,TY=-331.30,122.45;TOPZ=Z['t716']['top'];CR=Z['t716']['height']
# The tower's total height is 65 m (Swedish Wikipedia, 'Gamla vattentornet i Kalmar'); the photo
# could not settle it (52-63 m). The shaft is lengthened by D111 so its highest point (the merlons) is at 65.0 and
# the crown keeps the proportions read from the photo.
D111=65.0-max(TOPZ,CR+1.40);ST111=40.0+D111
rz111=lambda z:6.80-1.30*min(z,ST111)/ST111
m.lathe(TX,TY,0,[(rz111(z),z) for z in (0,10,20,30,40.0,ST111)],BK,48)
for z,h in ((0,.80),(9.0,.30),(19.5,.30),(30.0,.30),(40.5,.30)):
 r0=rz111(z);m.lathe(TX,TY,z,[(r0-.10,0),(r0+.08,0),(r0+.08,h),(r0-.10,h)],STN,48)
# Small round windows in eight vertical rows.
for j in range(8):
 th=j*math.tau/8+math.pi/16;ang=th+math.pi/2
 for z in (6.5,11.0,15.5,20.0,24.5,29.0,33.5,37.5,42.0,46.5)[:8+int(D111//4.5)]:
  r0=rz111(z);x,y=TX+(r0-.37)*math.cos(th),TY+(r0-.37)*math.sin(th);k=16
  m.faces([lp(x,y,.32*math.cos(t*math.tau/k),.385,z+.32*math.sin(t*math.tau/k),ang) for t in range(k)],[tuple(range(k))],GLAZE)
  ring=[lp(x,y,rr*math.cos(t*math.tau/k),.39,z+rr*math.sin(t*math.tau/k),ang) for rr in (.32,.46) for t in range(k)]
  m.faces(ring,[(t,(t+1)%k,k+(t+1)%k,k+t) for t in range(k)],STN)
# The door facing the annex (east), in a stone surround.
th=math.radians(-25);x,y=TX+(6.80-.355)*math.cos(th),TY+(6.80-.355)*math.sin(th);ang=th+math.pi/2
facade_box(m,x,y,0,.40,1.35,1.30,.10,2.70,M['Dark'],ang);surround36(m,x,y,0,0,1.30,2.70,ang,STN,.20,.42)
# The corbel table: a stone ring flaring out, corbels under it, small arches between.
nv111=len(m.v)
m.lathe(TX,TY,39.7,[(5.45,0),(5.60,0),(5.60,.40),(5.97,1.60),(6.05,2.10),(5.80,2.10)],STN,48)
for j in range(32):
 th=j*math.tau/32;ang=th+math.pi/2
 for k,(zz,dd,hh) in enumerate(((40.15,.18,.40),(40.55,.32,.40),(40.95,.46,.40))):
  x,y=TX+(5.50+dd/2)*math.cos(th),TY+(5.50+dd/2)*math.sin(th);box(m,x,y,.30,dd,hh,zz,STN,ang)
# The brick crown, arched windows, stone band, crenellated parapet, coping and roof cap.
m.lathe(TX,TY,41.80,[(5.95,0),(5.95,CR-41.80)],BK,48)
for j in range(8):
 th=j*math.tau/8;ang=th+math.pi/2;x,y=TX+(5.95-.355)*math.cos(th),TY+(5.95-.355)*math.sin(th)
 facade_box(m,x,y,0,.37,45.10,.75,.04,2.20,GLAZE,ang)
 pts=[(.375*math.cos(t*math.pi/8),46.20+.375*math.sin(t*math.pi/8)) for t in range(9)]
 m.faces([lp(x,y,du,.37,zz,ang) for du,zz in pts],[tuple(range(9))],GLAZE)
 town_path(m,[lp(x,y,.47,.42,44.0,ang),lp(x,y,.47,.42,46.20,ang)]+[lp(x,y,.47*math.cos(t*math.pi/8),.42,46.20+.47*math.sin(t*math.pi/8),ang) for t in range(1,8)]+[lp(x,y,-.47,.42,46.20,ang),lp(x,y,-.47,.42,44.0,ang)],.06,STN)
 facade_box(m,x,y,0,.44,43.97,1.10,.14,.08,STN,ang)
for z,h in ((48.6,.30),(CR-.25,.25)):m.lathe(TX,TY,z,[(5.85,0),(6.06,0),(6.06,h),(5.85,h)],STN,48)
m.lathe(TX,TY,CR,[(5.95,0),(5.95,.75),(5.55,.75),(5.55,0)],BK,48)
for j in range(24):
 th=(j+.5)*math.tau/24;ang=th+math.pi/2;x,y=TX+5.75*math.cos(th),TY+5.75*math.sin(th)
 box(m,x,y,.78,.40,TOPZ-.08-(CR+.75),CR+.75,BK,ang);box(m,x,y,.90,.50,.08,TOPZ-.08,STN,ang)
m.lathe(TX,TY,CR+.10,[(5.56,0),(4.0,.50),(.25,1.30),(0,1.30)],M['Cap'],48)
# Lift the crown by D111 onto the lengthened shaft.
m.v[nv111:]=[(x,y,z+D111) for x,y,z in m.v[nv111:]]
# The annex on the east side: a brick porch with a door and a flat roof (estimated, not seen).
for w in walls('a716','outer'):
 x,y,L,a=sf_edge(w['p'],w['q']);ox,oy=outward(w)
 door=ox>.8 and L>2.5
 bz_wall(m,w['p'],w['q'],0,Z['a716']['height'],[(0,0,1.10,2.30,0)] if door else [],BK)
 if door:door83(m,x,y,0,0,1.10,2.30,a,M['Dark'],STN,glass=True)
 facade_box(m,x,y,0,.42,Z['a716']['height']-.15,L+.06,.16,.30,STN,a)
flatroof111(m,'a716',M['Cap'],None)
b111_finish(m,'91072716')

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block111_cameras=[
 sv_camera('554_Block111_Cal_Storgatan52',117.07,-6.55,2.55,332,15,90),
 sv_camera('555_Block111_Cal_Storgatan43',158.01,-7.58,2.72,332,15,90),
 sv_camera('556_Block111_Cal_Proviant1',182.81,-109.60,2.50,242,15,90),
 sv_camera('557_Block111_Cal_Vattentornet',-288.03,101.90,2.50,250,20,90),
 ('558_Block111_Aerial',(150.0,-60.0,60.0),(145.0,5.0,4.0),24),
]
print('BLOCK111_GEOMETRY',len(block111_names),'dropped',block111_dropped)
