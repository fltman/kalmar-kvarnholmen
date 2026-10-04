"""Pass 108: Kaggensgatan, five generic pass-17 volumes.
- 92204167 (west side, north of Storgatan): the brown brick shop house (Klintheims Skor) over the
  southern 16.3 m of the front: glazed shopfronts between brick piers, a white fascia sign, two
  rows of nine dark-framed windows, a flat roof with a low dark roof box; the northern 8.5 m (a
  lighter facade only glimpsed at the photo's edge) a plain beige rendered house, estimated;
- 92379295 (SM_Building_92379295, the Storgatan corner, east side): salmon render on a grey stone
  base, the photographed stretch of the Kaggensgatan front with two arched shop windows round a
  door in a cream surround, cream pilasters and a red arched gate; the rest of the front and the
  Storgatan front plain in the same materials; cream window surrounds above; a red tile mansard;
- 92379291 (38 Kaggensgatan): cream render on a grey plinth, nine first-floor windows in white
  surrounds, the red arched carriage gate, the red door, white awnings over the ground-floor
  windows, red-brown string course and cornice lines, two curved gables with paired arched windows,
  a red brick mansard with arched dormers between and beside them; the Strömgatan wing plain;
- 92204171: the white four-storey frame house: slab edges and side columns in white, glazed
  balustrades, the dark recessed wall behind, garage doors and the red band on the ground floor;
  the garage storey north of it; the rear part plain and low (not seen);
- 92379305 (40c Kaggensgatan): the 1960s office: 1.2 m window module between projecting
  concrete fins, dark spandrels, shopfronts between piers every four modules, blue awning strips
  over the shopfronts and the top windows, a metal fascia and a flat roof; the Strömgatan front
  given the same treatment (not seen).

References: two Google Street View panoramas on Kaggensgatan (resected) and two contributor
360 photos (position and heading unreliable; style, openings and storeys only, scaled from door
and storey heights), view only. Zones: source/block108.json; see references/block108-notes.md.
Cars, signs' lettering, lamps and pipes are omitted.
"""
B108D=json.loads((R/'source/block108.json').read_text());Z=B108D['zones']
block108_names=[];B108={}
for old in [k for k in list(materials) if k.startswith('M_Block108_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('White','TownPaintWhite',(.92,.92,.89),.60,0),('Brick','TownTileRed',(.42,.27,.21),.90,0),('Pier','TownStone',(.55,.42,.29),.85,0),
 ('Frame','TownMetalGrey',(.20,.17,.15),.50,.30),('Dark','TownMetalGrey',(.07,.07,.075),.45,.40),('Beige','TownIvory',(.80,.74,.60),.90,0),
 ('Tile','TownTileRed',(.62,.30,.22),.80,0),('Sheet','TownMetalGrey',(.36,.37,.38),.55,.25),
 ('Salmon','TownIvory',(.82,.53,.40),.90,0),('Cream','TownIvory',(.90,.84,.68),.85,0),('Stone','TownStone',(.55,.54,.51),.90,0),
 ('RedGate','TownPaintBrown',(.62,.20,.15),.60,0),('Navy','TownPaintWhite',(.13,.14,.26),.55,0),
 ('Cream38','TownIvory',(.87,.80,.63),.90,0),('Line','TownPaintBrown',(.58,.27,.18),.70,0),('RedBrick','TownTileRed',(.62,.31,.24),.90,0),
 ('Plinth','TownStone',(.64,.63,.60),.90,0),('Groove','TownIvory',(.74,.68,.53),.90,0),('RedDoor','TownPaintBrown',(.55,.17,.12),.60,0),
 ('Awning','TownPaintWhite',(.90,.90,.88),.70,0),
 ('WhiteR','TownPaintWhite',(.90,.90,.88),.70,0),('Wall','TownMetalGrey',(.16,.16,.17),.60,.15),('Garage','TownMetalGrey',(.08,.08,.085),.50,.30),
 ('RedBand','TownPaintBrown',(.62,.20,.15),.60,0),('Grey','TownIvory',(.66,.65,.62),.90,0),
 ('Conc','TownStone',(.71,.68,.63),.90,0),('Span','TownStone',(.44,.41,.38),.90,0),('Blue','TownPaintWhite',(.13,.24,.62),.60,0),
 ('Fascia','TownMetalGrey',(.62,.63,.64),.50,.30),('Alu','TownMetalGrey',(.30,.30,.31),.45,.40),
 ]:
 name='M_Block108_'+key;B108[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block108_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B108;WH=M['White']

def b108_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block108_names.append(name);return Mesh(name,category)
def drop_degenerate_faces108(obj,tol=1e-9):
 import bmesh
 bm=bmesh.new();bm.from_mesh(obj.data)
 def _thin(f):
  L=max(e.calc_length() for e in f.edges);return L>0 and 2*f.calc_area()/L<1e-4
 bad=[f for f in bm.faces if f.calc_area()<tol or len({v.index for v in f.verts})<len(f.verts) or _thin(f)]
 if bad:bmesh.ops.delete(bm,geom=bad,context='FACES_ONLY')
 bm.to_mesh(obj.data);bm.free();obj.data.update();return len(bad)
block108_dropped={}
def b108_finish(m,osm):
 obj=s21_finish(m);block108_dropped[obj.name]=drop_degenerate_faces108(obj)
 obj['detail_pass']=108;obj['reference_notes']='references/block108-notes.md';obj['osm_way']=osm;return obj

def pt108(a,b,s):
 # The point s metres from a towards b.
 L=math.dist(a,b);return (a[0]+(b[0]-a[0])*s/L,a[1]+(b[1]-a[1])*s/L)
def fronts108(m,zone,test,wall,frame,trim,levels,floor0=1.0):
 # Party and upper walls in the wall material, other outer walls plain; returns the street fronts.
 H=Z[zone]['height'];out=[]
 for w in walls(zone):
  if w['kind']!='outer':bz_wall(m,w['p'],w['q'],w['z0'],H,[],wall);continue
  ox,oy=outward(w)
  if test(ox,oy):out.append(w);continue
  plain(m,w,H,wall,frame,trim,levels,floor0)
 return out
def flatroof108(m,zone,ma,trim,coping=.24):
 # Flat roof (triangulated, the outlines can be concave) and a parapet coping on the outer walls.
 from mathutils import Vector
 from mathutils.geometry import tessellate_polygon
 H=Z[zone]['height']
 for g in Z[zone]['polygons']:
  vs=[(*v,H+.02) for v in g];tris=tessellate_polygon([[Vector(v) for v in vs]])
  m.faces(vs,[tuple(t) for t in tris]+[tuple(reversed(t)) for t in tris],ma)
 for w in walls(zone,'outer'):
  x,y,L,a=sf_edge(w['p'],w['q']);facade_box(m,x,y,0,.38,H+coping/2,L+.06,.12,coping,trim,a)
def mansard108(m,zone,A,B,ma,inset,top=None):
 r,Ls,Lt=rect82(zone,A,B);H=Z[zone]['height'];T=Z[zone]['top']
 inset_roof(m,r,H,inset,T-H,ma,.30,top)
def arc108(w,z,r,k=12):
 # Elliptic head: from the right spring over to the left (the shape of bz_wall's arched holes).
 return [(w/2*math.cos(t*math.pi/k),z+r*math.sin(t*math.pi/k)) for t in range(k+1)]
def archglass108(m,x,y,u,b,w,h,r,a,frame,o=.16,lights=1,sur=None,bw=.14):
 # Glass to the crown of an arched opening, a frame round it, mullions, optional flat surround.
 pts=[(-w/2,b),(w/2,b)]+arc108(w,b+h,r)
 m.faces([lp(x,y,u+du,o-.04,zz,a) for du,zz in pts],[tuple(range(len(pts))),tuple(range(len(pts)-1,-1,-1))],GLAZE)
 town_path(m,[lp(x,y,u+du,o,zz,a) for du,zz in pts+pts[:1]],.04,frame)
 for k in range(1,lights):facade_box(m,x,y,u-w/2+k*w/lights,o,b+h/2,.05,.06,h,frame,a)
 if sur:
  town_path(m,[lp(x,y,u+du*(1+2*bw/w),.40,b+h+(zz-b-h)*(1+bw/r),a) for du,zz in arc108(w,b+h,r)],.08,sur)
  for s in (-1,1):facade_box(m,x,y,u+s*(w/2+bw/2),.39,b+h/2,bw,.08,h,sur,a)
def win108(m,x,y,u,b,w,h,a,frame,sur,rows=2,bw=.14,sill=None):
 cas81(m,x,y,u,b,w,h,a,frame,.16,rows)
 if sur:surround36(m,x,y,u,b,w,h,a,sur,bw,.40)
 if sill:facade_box(m,x,y,u,.47,b-.05,w+.30,.16,.07,sill,a)
def prism108(m,x,y,u,outline,o0,o1,ma,a):
 # A closed prism of a convex face outline [(du,z)] between the offsets o0 and o1.
 n=len(outline);vs=[lp(x,y,u+du,o,zz,a) for o in (o0,o1) for du,zz in outline]
 m.faces(vs,[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],ma)
FRONT108=lambda dx,dy:(lambda ox,oy:ox*dx+oy*dy>.9)

# ---- 92204167: brown brick shop house, s from the south joint (y 14.55) along the east front.
# Scaled from the contributor photo by the 11 m front of the yellow neighbour 92204203 and the
# storey heights (3.05 m); positions carry about +-0.8 m.
m=b108_new(Z['b167']['mesh'],'Kvarnholmen/Kaggensgatan');BR=M['Brick'];FR=M['Frame']
A7,B7=(-192.33,14.55),(-192.16,30.90);H=Z['b167']['height']
for w in fronts108(m,'b167',FRONT108(1,0),BR,FR,BR,3,1.0):
 x,y,L,a=sf_edge(w['p'],w['q']);S=lambda s:U(w,*pt108(A7,B7,s))
 piers=[(.25,.50),(5.40,.55),(11.60,.55),(16.05,.50)]
 shops=[(S((p0+w0/2+p1-w1/2)/2),.25,(p1-w1/2)-(p0+w0/2),3.70) for (p0,w0),(p1,w1) in zip(piers,piers[1:])]
 ups=[(S(1.20+k*1.75),b,1.20,1.55) for k in range(9) for b in (6.00,9.15)]
 bz_wall(m,w['p'],w['q'],0,H,[(u,b,ww,hh,0) for u,b,ww,hh in shops+ups],BR)
 for s,ww in piers:facade_box(m,x,y,S(s),.42,2.05,ww,.14,4.10,M['Pier'],a)
 for u,b,ww,hh in shops:
  facade_box(m,x,y,u,.16,b+hh/2,ww,.02,hh,GLAZE,a)
  for zz in (b+.04,b+hh-.04,b+hh-.75):facade_box(m,x,y,u,.20,zz,ww,.08,.07,M['Dark'],a)
  for k in range(1,max(2,round(ww/1.6))):facade_box(m,x,y,u-ww/2+k*ww/max(2,round(ww/1.6)),.20,b+hh/2,.06,.08,hh,M['Dark'],a)
 # The glazed entrance doors in the middle shop, the white fascia sign over it.
 du=S(8.50);facade_box(m,x,y,du,.10,1.25,2.10,.04,2.30,M['Dark'],a);facade_box(m,x,y,du,.14,1.25,1.90,.02,2.15,GLAZE,a)
 facade_box(m,x,y,S(8.50),.47,4.45,7.70,.12,.70,WH,a);facade_box(m,x,y,S(8.50),.54,4.45,7.20,.02,.38,M['Dark'],a)
 facade_box(m,x,y,0,.40,4.02,L+.02,.10,.14,M['Pier'],a)
 for u,b,ww,hh in ups:
  cas81(m,x,y,u,b,ww,hh,a,FR,.16,1);facade_box(m,x,y,u,.44,b-.05,ww+.10,.14,.07,M['Sheet'],a)
 facade_box(m,x,y,0,.42,H-.10,L+.06,.16,.20,M['Sheet'],a)
flatroof108(m,'b167',M['Sheet'],M['Sheet'],.10)
fw=[w for w in walls('b167','outer') if outward(w)[0]>.9][0];x,y,L,a=sf_edge(fw['p'],fw['q'])
bx,by,_=lp(x,y,U(fw,*pt108(A7,B7,8.2)),-3.4,0,a);box(m,bx,by,6.5,4.0,1.10,H,M['Dark'],a)
# The northern part: not seen beyond the photo's edge; plain beige render, hipped tile roof.
fronts108(m,'n167',lambda *_:False,M['Beige'],WH,WH,3,1.0)
hip82(m,'n167',(-192.16,30.90),(-192.08,39.39),M['Tile'])
b108_finish(m,'92204167')

# ---- 92379295: salmon render, s from the north corner along the west front. The contributor
# photo is scaled from the door (2.3 m) and placed at its nominal position (door at s 20.6);
# its position along the front is not known (+-5 m).
m=b108_new(Z['s295']['mesh'],'Kvarnholmen/Kaggensgatan');SA=M['Salmon'];CR=M['Cream'];ST=M['Stone']
A5,B5=(-181.09,-8.12),(-181.30,-44.19);H=Z['s295']['height']
def salmon108(w,seen):
 x,y,L,a=sf_edge(w['p'],w['q'])
 if seen:S=lambda s:U(w,*pt108(A5,B5,s))
 else:S=lambda s:s-L/2
 n=max(2,round((L-5.0)/2.95));ax=[2.85+k*2.95 for k in range(n) if 2.85+k*2.95<L-2.0] if seen else [L/2+(k-(n-1)/2)*2.95 for k in range(n)]
 ups=[(S(s),b,1.30,2.10,0) for s in ax for b in (5.70,9.30)]
 arch=[(S(17.80),.55,2.70,2.25,.95),(S(23.30),.55,2.70,2.25,.95)] if seen else []
 door=[(S(20.55),.15,1.00,2.30,0)] if seen else []
 gate=[(S(26.90),0,2.60,2.75,.80)] if seen else []
 gnd=[(S(s),.90,1.40,2.20,0) for s in ax if not seen or not 15.4<s<28.6]
 bz_wall(m,w['p'],w['q'],0,H,ups+arch+door+gate+gnd,SA)
 for u,b,ww,hh,r in ups:win108(m,x,y,u,b,ww,hh,a,WH,CR,2,.16,CR)
 for u,b,ww,hh,r in gnd:win108(m,x,y,u,b,ww,hh,a,WH,CR,2,.14,None)
 for u,b,ww,hh,r in arch:
  # Arched shop windows: glass to the crown, a navy fascia band in the head, a cream surround.
  archglass108(m,x,y,u,b,ww,hh,r,a,M['Navy'],.16,1,CR,.20)
  facade_box(m,x,y,u,.20,b+hh-.10,ww-.04,.06,.30,M['Navy'],a);facade_box(m,x,y,u,.20,b+.12,ww-.04,.06,.24,M['Navy'],a)
 for u,b,ww,hh,r in door:
  door83(m,x,y,u,b,ww,hh,a,M['Frame'],CR,glass=True);facade_box(m,x,y,u,.40,b+hh+.25,ww+.50,.08,.20,CR,a)
 for u,b,ww,hh,r in gate:
  pts=[(-ww/2,0),(ww/2,0)]+arc108(ww,hh,r)
  m.faces([lp(x,y,u+du,.10,zz,a) for du,zz in pts],[tuple(range(len(pts))),tuple(range(len(pts)-1,-1,-1))],M['RedGate'])
  for k in (-1,1):facade_box(m,x,y,u+k*ww/4,.13,1.20,.02,.03,2.10,M['Dark'],a)
  town_path(m,[lp(x,y,u+du*1.12,.40,zz+(zz-hh)*.25,a) for du,zz in arc108(ww,hh,r)],.10,CR)
 # Pilasters (the seen pair and the corners), stone base, string course, cornice.
 for s,ww in ([(16.00,.70),(25.10,.65)] if seen else [])+[(.35,.70),(L-.35,.70)]:
  facade_box(m,x,y,S(s) if seen or s>1 and s<L-1 else s-L/2,.42,(H-.40)/2,ww,.14,H-.40,CR,a)
 facade_box(m,x,y,0,.40,.22,L+.02,.10,.45,ST,a)
 facade_box(m,x,y,0,.42,4.80,L+.04,.14,.30,CR,a)
 facade_box(m,x,y,0,.42,H-.30,L+.04,.14,.30,CR,a);facade_box(m,x,y,0,.52,H-.08,L+.20,.34,.16,CR,a)
for w in fronts108(m,'s295',lambda ox,oy:ox<-.9 or oy>.9,SA,WH,CR,3,.9):
 salmon108(w,outward(w)[0]<-.9)
mansard108(m,'s295',A5,B5,M['Tile'],3.0)
b108_finish(m,'92379295')

# ---- 92379291 (38 Kaggensgatan): cream render, s from the north corner along the west front.
m=b108_new(Z['c291']['mesh'],'Kvarnholmen/Kaggensgatan');C8=M['Cream38'];LN=M['Line'];RB=M['RedBrick']
A1,B1=(-179.105,205.94),(-179.32,175.84);H=Z['c291']['height']
for w in fronts108(m,'c291',FRONT108(-1,0),C8,WH,WH,2,.9):
 x,y,L,a=sf_edge(w['p'],w['q']);S=lambda s:U(w,*pt108(A1,B1,s))
 ups=[(S(s),4.54,1.25,2.07) for s in (2.15,4.80,7.74,10.87,13.84,17.75,21.62,24.96,28.34)]
 gw=[(S(s),.80,ww,2.45) for s,ww in ((1.60,1.30),(5.05,1.50),(8.07,1.30),(11.00,1.20),(14.05,1.25),(21.47,1.50),(24.55,1.60),(27.82,1.60))]
 du,gu=S(12.85),S(17.77)
 holes=[(u,b,ww,hh,0) for u,b,ww,hh in ups+gw]+[(du,.35,.95,2.25,0),(gu,0,2.95,2.72,.55)]
 bz_wall(m,w['p'],w['q'],0,H,holes,C8)
 for u,b,ww,hh in ups:win108(m,x,y,u,b,ww,hh,a,WH,WH,2,.17,WH)
 for u,b,ww,hh in gw:
  win108(m,x,y,u,b,ww,hh,a,WH,None,2);facade_box(m,x,y,u,.45,b-.05,ww+.16,.14,.06,WH,a)
  awning82(m,x,y,u,b+hh+.02,ww+.20,a,M['Awning'],.32,.55)
 # The red door up three steps, the red arched carriage gate with a glazed fanlight.
 door83(m,x,y,du,.35,.95,2.25,a,M['RedDoor'],WH,glass=True)
 for k in range(2):facade_box(m,x,y,du,.55+.15*k,.09+k*.13,1.30,.30,.13,M['Plinth'],a)
 pts=[(-1.475,2.25),(1.475,2.25)]+arc108(2.95,2.72,.55)
 m.faces([lp(x,y,gu+dd,.10,zz,a) for dd,zz in pts],[tuple(range(len(pts))),tuple(range(len(pts)-1,-1,-1))],GLAZE)
 for k in (-1,1):facade_box(m,x,y,gu+k*.735,.12,1.12,1.42,.06,2.25,M['RedGate'],a)
 facade_box(m,x,y,gu,.16,1.12,.04,.04,2.25,M['Dark'],a);facade_box(m,x,y,gu,.14,2.26,2.95,.05,.06,M['RedGate'],a)
 town_path(m,[lp(x,y,gu+dd,.14,zz,a) for dd,zz in arc108(2.95,2.72,.55)],.05,M['RedGate'])
 # Plinth, ground-floor grooves, the string course with its red line, cornice with its red line.
 facade_box(m,x,y,0,.40,.30,L+.02,.10,.60,M['Plinth'],a)
 for zz in (1.20,1.80,2.40,3.00,3.55):facade_box(m,x,y,0,.36,zz,L,.02,.035,M['Groove'],a)
 facade_box(m,x,y,0,.42,3.98,L+.04,.14,.24,C8,a);facade_box(m,x,y,0,.50,4.08,L+.06,.02,.05,LN,a)
 facade_box(m,x,y,0,.42,H-.22,L+.04,.14,.30,C8,a);facade_box(m,x,y,0,.52,H-.04,L+.12,.30,.10,C8,a);facade_box(m,x,y,0,.68,H-.11,L+.12,.02,.05,LN,a)
 for s in (.10,15.20,L-.10):town_rod(m,lp(x,y,S(s),.50,.20,a),lp(x,y,S(s),.50,H,a),.05,LN,8)
 # The two curved gables standing on the cornice, paired arched windows in them.
 for s0,s1,top,pairs in ((3.70,12.10,11.10,(5.10,7.90,10.80)),(16.10,23.80,11.45,(17.70,21.40))):
  gu0=S((s0+s1)/2);W=s1-s0;sh=10.35;k=8
  rim=[(W/2-(W/2-W/5)*(1-math.cos(t*math.pi/2/k)),sh+(top-sh)*math.sin(t*math.pi/2/k)) for t in range(k+1)]
  outline=[(-W/2,H),(W/2,H)]+rim+[(-du_,zz) for du_,zz in reversed(rim)]
  prism108(m,x,y,gu0,outline,-.45,.355,C8,a)
  town_path(m,[lp(x,y,gu0+du_,.40,zz+.06,a) for du_,zz in [(W/2+.05,sh-.05)]+rim+[(-d,z) for d,z in reversed(rim)]+[(-W/2-.05,sh-.05)]],.08,C8)
  for s in pairs:
   for k2 in (-1,1):archglass108(m,x,y,S(s)+k2*.37,8.25,.55,1.22,.28,a,WH,.41,1)
 # Arched dormers in the red brick mansard: north end, between the gables, south end.
 for s in (2.27,13.86,24.60,28.00):
  bu=S(s);bx,by,_=lp(x,y,bu,-.40,0,a);box(m,bx,by,1.45,1.40,2.15,H,RB,a)
  archglass108(m,x,y,bu,8.35,.85,1.05,.42,a,WH,.36,1)
  town_path(m,[lp(x,y,bu+dd*1.30,.32,zz+(zz-9.40)*.4,a) for dd,zz in arc108(.85,9.40,.42)],.07,RB)
mansard108(m,'c291',A1,B1,RB,1.50,M['Sheet'])
# The Strömgatan wing: not seen; plain cream render with the same mansard.
fronts108(m,'w291',lambda *_:False,C8,WH,WH,2,.9)
mansard108(m,'w291',(-168.77,197.47),(-153.59,197.36),RB,1.50,M['Sheet'])
b108_finish(m,'92379291')

# ---- 92204171: white frame house, s from the south corner along the east front.
m=b108_new(Z['w171']['mesh'],'Kvarnholmen/Kaggensgatan');WR=M['WhiteR'];WL=M['Wall']
A4,B4=(-190.71,236.26),(-190.66,245.66);H=Z['w171']['height']
for w in fronts108(m,'w171',FRONT108(1,0),WR,WH,WH,4,.9):
 x,y,L,a=sf_edge(w['p'],w['q'])
 # Ground floor set back 0.3 m: dark wall, garage doors, the red band; recessed wall above.
 bz_wall(m,w['p'],w['q'],0,3.10,[],WL,-.30,.05)
 for s,ww in ((1.55,2.00),(4.40,2.30),(7.45,2.60)):facade_box(m,x,y,s-L/2,.07,.85,ww,.04,1.70,M['Garage'],a)
 facade_box(m,x,y,0,.08,1.88,L-.70,.04,.40,M['RedBand'],a)
 bz_wall(m,w['p'],w['q'],3.10,H-.30,[],WL,-1.35,-1.00)
 for zb in (3.10,5.90,8.60):
  zh=(5.90 if zb==3.10 else 8.60 if zb==5.90 else 11.30)-zb-.30
  for s,ww in ((2.00,2.40),(4.70,2.20),(7.40,2.40)):
   facade_box(m,x,y,s-L/2,-.98,zb+.15+zh/2,ww,.02,zh-.25,GLAZE,a)
   for k in (-1,0,1):facade_box(m,x,y,s-L/2+k*ww/2,-.96,zb+.15+zh/2,.06,.06,zh-.25,M['Garage'],a)
 for zb in (11.30,):facade_box(m,x,y,0,-.98,zb+.75,L-1.0,.02,1.0,GLAZE,a)
 # Slab edges, the glazed balustrades, the white side columns and the roof frame.
 for zs in (3.10,5.90,8.60,11.30):
  facade_box(m,x,y,0,(.355-1.35)/2,zs-.15,L-.70,1.70,.30,WR,a)
  facade_box(m,x,y,0,.30,zs+.55,L-.80,.02,.95,GLAZE,a);facade_box(m,x,y,0,.30,zs+1.04,L-.80,.05,.05,M['Alu'],a)
 facade_box(m,x,y,0,(.355-1.35)/2,H-.15,L-.10,1.70,.30,WR,a)
 for u in (-L/2+.48,L/2-.40):facade_box(m,x,y,u,(.355-1.35)/2,H/2,.35 if u<0 else .35,1.70,H,WR,a)
flatroof108(m,'w171',M['Sheet'],WR,.10)
# The garage storey on to the north corner, and the unseen rear part.
for w in fronts108(m,'g171',FRONT108(1,0),WR,WH,WH,1,.9):
 x,y,L,a=sf_edge(w['p'],w['q']);bz_wall(m,w['p'],w['q'],0,3.10,[(0,0,L-.60,2.30,0)],WR)
 facade_box(m,x,y,0,.10,1.15,L-.60,.04,2.30,M['Garage'],a);facade_box(m,x,y,0,.12,1.88,L-.60,.04,.40,M['RedBand'],a)
flatroof108(m,'g171',M['Sheet'],WR,.10)
fronts108(m,'r171',lambda *_:False,M['Grey'],WH,WH,2,.9);flatroof108(m,'r171',M['Sheet'],M['Grey'])
b108_finish(m,'92204171')

# ---- 92379305 (40c): the office. Module 1.2 m, piers every four modules (measured 4.8 m).
m=b108_new(Z['o305']['mesh'],'Kvarnholmen/Kaggensgatan');CO=M['Conc'];SP=M['Span'];BL=M['Blue']
H=Z['o305']['height']
def office108(w,door_s=None):
 x,y,L,a=sf_edge(w['p'],w['q']);n=max(4,round(L/1.2));md=L/n;s0=-L/2
 fins=[s0+k*md for k in range(n+1)];piers=fins[::4]
 if piers[-1]<L/2-.5:piers.append(L/2)
 rows=((4.05,1.45),(7.00,1.40))
 wins=[(s0+(k+.5)*md,b,md-.30,h) for k in range(n) for b,h in rows]
 bz_wall(m,w['p'],w['q'],3.25,H,[(u,b,ww,hh,0) for u,b,ww,hh in wins],CO)
 for u,b,ww,hh in wins:
  facade_box(m,x,y,u,.18,b+hh/2,ww,.02,hh,GLAZE,a)
  for zz in (b+.03,b+hh-.03):facade_box(m,x,y,u,.22,zz,ww,.06,.06,M['Alu'],a)
  for k in (-1,1):facade_box(m,x,y,u+k*(ww/2-.03),.22,b+hh/2,.06,.06,hh,M['Alu'],a)
  facade_box(m,x,y,u,.37,b-.43 if b<5 else b-.64,md-.30,.03,.75 if b<5 else 1.15,SP,a)
 for u in fins:facade_box(m,x,y,max(-L/2+.14,min(L/2-.14,u)),.48,(3.25+8.80)/2,.28,.25,8.80-3.25,CO,a)
 # Blue awning boxes over the top windows, the metal fascia over them.
 facade_box(m,x,y,0,.62,8.68,L+.02,.30,.24,BL,a);facade_box(m,x,y,0,.42,9.25,L+.06,.18,.90,M['Fascia'],a)
 # Ground floor: shopfronts between piers, dark fascia, blue awning strip.
 bays=[((p0+p1)/2,p1-p0-.55) for p0,p1 in zip(piers,piers[1:])]
 bz_wall(m,w['p'],w['q'],0,3.25,[(u,.35,ww,2.25,0) for u,ww in bays],CO)
 for u,ww in bays:
  facade_box(m,x,y,u,.12,1.475,ww,.02,2.25,GLAZE,a)
  for zz in (.38,2.57):facade_box(m,x,y,u,.16,zz,ww,.06,.06,M['Alu'],a)
  for k in range(1,max(2,round(ww/2.2))):facade_box(m,x,y,u-ww/2+k*ww/max(2,round(ww/2.2)),.16,1.475,.06,.06,2.25,M['Alu'],a)
 if door_s is not None:
  facade_box(m,x,y,door_s-L/2,.18,1.20,1.10,.04,2.25,M['Alu'],a);facade_box(m,x,y,door_s-L/2,.21,1.20,.95,.02,2.10,GLAZE,a)
 for u in piers:facade_box(m,x,y,max(-L/2+.28,min(L/2-.28,u)),.42,1.62,.55,.16,3.25,CO,a)
 facade_box(m,x,y,0,.40,2.82,L+.02,.12,.40,M['Alu'],a);facade_box(m,x,y,0,.62,3.12,L+.04,.45,.22,BL,a)
for w in fronts108(m,'o305',lambda ox,oy:ox<-.9 or oy<-.9,CO,M['Alu'],CO,3,1.0):
 office108(w,27.60 if outward(w)[0]<-.9 else None)
flatroof108(m,'o305',M['Sheet'],M['Fascia'],.12)
b108_finish(m,'92379305')

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block108_cameras=[
 sv_camera('532_Block108_Cal_Cream38',-187.10,190.47,2.40,64,15,90),
 sv_camera('533_Block108_Cal_Office40c',-184.60,236.50,2.40,61,15,90),
 sv_camera('534_Block108_Cal_White40',-184.60,236.50,2.40,241,15,90),
 sv_camera('535_Block108_Cal_Brick',-184.30,17.30,1.55,243,15,90),
 ('536_Block108_Aerial',(-105.0,110.0,95.0),(-185.0,110.0,4.0),20),
]
print('BLOCK108_GEOMETRY',len(block108_names),'dropped',block108_dropped)
