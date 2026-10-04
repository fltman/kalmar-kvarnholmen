"""Pass 110: ten generic pass-17 volumes on Storgatan, Norra Långgatan, Södra Långgatan and Västra
Sjögatan. Street fronts detailed, backs plain.
- 91265011 (Storgatan, north side): the 1960s two-storey commercial block in grey-beige stone
  slabs: six bays between full-height piers, recessed shopfronts (four wrapped in blue film), a
  stone fascia band, a continuous upper window ribbon with dark mullions, a stone parapet;
- 91970373 (Viore): yellow render over dark stone shopfronts, eight white-framed windows, a dark
  eave and a red tile saddle roof; the rear unseen and plain;
- 91970296: the yellow Sakligheter house (dark shopfront, dark green fascia, a nine-window ribbon,
  a dark green eave) and the brown granite four-storey Synsam house (shop bays between piers, a dark
  canopy, three windows a storey); the large rear unseen and plain;
- 92379278 (Dillbergs Bokhandel, Storgatan south side): limestone ground floor with the teal shop
  window and entrance and two roller shutters, salmon render above with paired windows in cream
  surrounds, a red tile roof;
- 92379304: limestone slab front, large brown-framed ground glazing, upper window ribbon;
- 92379276 (25 Södra Långgatan): white render, four blue-framed windows, blue doors, three blue
  awnings, a red tile saddle roof with two red dormers; the rear wings plain;
- 92412841 (4 Västra Sjögatan): sage-green vertical boarding on a dark plinth, white six-pane
  windows, the porch with its entablature and the green double door, a steep red tile hip roof with
  the white lantern dormer;
- 92204180 (Norra Långgatan): the white two-storey west part with six window bays, cream awnings
  and the orange-framed door; the east part with dark louvre bands over glazed ground bays;
- 91264997 (Åhléns/Kvasten): the white three-storey front with three glazed gables over glazed
  two-storey bays, the recessed entrance under the east gable, shopfronts; the unseen west end of
  the front and all other walls plain;
- 91970385: the orange four-storey house with a glazed oriel and a round window, and the beige
  three-storey house beside it (contributor photo only).

References: four Google Street View panoramas (92379276 and 92412841 resected on the house
corners; 92204180 and 91264997 at the panorama position, checked against the OSM joint) and six
contributor 360 photos (position and heading unreliable: style, storeys and openings only, scaled
from door and storey heights), view only. Zones: source/block110.json; see
references/block110-notes.md. Signs' lettering, lamps, planters and cars are omitted.
"""
B110D=json.loads((R/'source/block110.json').read_text());Z=B110D['zones']
block110_names=[];B110={};block110_skipped=[]
for old in [k for k in list(materials) if k.startswith('M_Block110_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('White','TownPaintWhite',(.92,.92,.89),.60,0),('Frame','TownPaintWhite',(.95,.95,.93),.55,0),
 ('Slab','TownStone',(.70,.67,.61),.90,0),('Pier','TownStone',(.63,.61,.57),.90,0),('Groove','TownStone',(.50,.48,.44),.90,0),
 ('NSBlue','TownPaintWhite',(.10,.17,.40),.55,0),('Dark','TownMetalGrey',(.07,.07,.075),.45,.40),('Alu','TownMetalGrey',(.30,.30,.31),.45,.40),
 ('Sheet','TownMetalGrey',(.36,.37,.38),.55,.25),('Tile','TownTileRed',(.72,.36,.24),.80,0),
 ('Salmon','TownIvory',(.71,.43,.37),.90,0),('Cream','TownIvory',(.88,.84,.74),.85,0),('Lime','TownStone',(.80,.77,.69),.90,0),
 ('Teal','TownPaintGreen',(.08,.45,.38),.55,0),('Shutter','TownMetalGrey',(.62,.63,.64),.50,.30),
 ('Yellow','TownIvory',(.86,.78,.47),.85,0),('SakYellow','TownIvory',(.88,.79,.32),.85,0),('DarkStone','TownStone',(.17,.17,.18),.70,0),
 ('DarkGreen','TownPaintGreen',(.14,.22,.18),.60,0),('Granite','TownStone',(.52,.42,.35),.80,0),('Brown','TownPaintBrown',(.40,.27,.20),.60,0),
 ('Beige','TownIvory',(.80,.74,.60),.90,0),('Render','TownPaintWhite',(.90,.90,.88),.70,0),('Blue','TownPaintWhite',(.17,.29,.52),.55,0),
 ('Awning','TownPaintWhite',(.14,.24,.52),.70,0),('DormerRed','TownPaintBrown',(.55,.22,.17),.60,0),('Plinth','TownStone',(.62,.61,.58),.90,0),
 ('Sage','TownPaintGreen',(.62,.67,.57),.75,0),('SageBoard','TownPaintGreen',(.55,.61,.51),.75,0),('Corner','TownPaintGreen',(.76,.80,.72),.70,0),
 ('DoorGreen','TownPaintGreen',(.33,.38,.30),.60,0),('DarkPlinth','TownStone',(.24,.24,.24),.90,0),
 ('Orange','TownPaintBrown',(.80,.45,.20),.60,0),('Louvre','TownMetalGrey',(.16,.16,.17),.55,.30),('CreamAwn','TownPaintWhite',(.93,.92,.87),.70,0),
 ('OrangeRender','TownIvory',(.87,.42,.20),.90,0),('BeigeR','TownIvory',(.80,.71,.53),.90,0),('Copper','TownPaintBrown',(.62,.36,.20),.60,0),
 ('Oriel','TownPaintGreen',(.55,.66,.62),.50,0),('RedSign','TownPaintBrown',(.70,.12,.10),.60,0),
 ]:
 name='M_Block110_'+key;B110[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block110_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B110;WH=M['White'];FR=M['Frame']

def b110_ok(name):
 # Only generic volumes are replaced: a house detailed by another pass is left alone (this pass's
 # own earlier output is rebuilt, so repeated builds give the same result).
 old=bpy.data.objects.get(name);dp=old.get('detail_pass',17) if old else 17
 if dp and dp>17 and dp!=110:block110_skipped.append((name,dp));return False
 return True
def b110_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block110_names.append(name);return Mesh(name,category)
def drop_degenerate_faces110(obj,tol=1e-9):
 import bmesh
 bm=bmesh.new();bm.from_mesh(obj.data)
 def _thin(f):
  L=max(e.calc_length() for e in f.edges);return L>0 and 2*f.calc_area()/L<1e-4
 bad=[f for f in bm.faces if f.calc_area()<tol or len({v.index for v in f.verts})<len(f.verts) or _thin(f)]
 if bad:bmesh.ops.delete(bm,geom=bad,context='FACES_ONLY')
 bm.to_mesh(obj.data);bm.free();obj.data.update();return len(bad)
block110_dropped={}
def b110_finish(m,osm):
 obj=s21_finish(m);block110_dropped[obj.name]=drop_degenerate_faces110(obj)
 obj['detail_pass']=110;obj['reference_notes']='references/block110-notes.md';obj['osm_way']=osm;return obj

def pt110(a,b,s):
 L=math.dist(a,b);return (a[0]+(b[0]-a[0])*s/L,a[1]+(b[1]-a[1])*s/L)
FRONT110=lambda dx,dy:(lambda ox,oy:ox*dx+oy*dy>.9)
def fronts110(m,zone,test,wall,frame,trim,levels,floor0=1.0):
 # Party and upper walls in the wall material, other outer walls plain; returns the street fronts.
 H=Z[zone]['height'];out=[]
 for w in walls(zone):
  if w['kind']!='outer':bz_wall(m,w['p'],w['q'],w['z0'],H,[],wall);continue
  if test(*outward(w)):out.append(w);continue
  plain(m,w,H,wall,frame,trim,levels,floor0)
 return out
def flatroof110(m,zone,ma,trim,coping=.24):
 from mathutils import Vector
 from mathutils.geometry import tessellate_polygon
 H=Z[zone]['height']
 for g in Z[zone]['polygons']:
  vs=[(*v,H+.02) for v in g];tris=tessellate_polygon([[Vector(v) for v in vs]])
  m.faces(vs,[tuple(t) for t in tris]+[tuple(reversed(t)) for t in tris],ma)
 for w in walls(zone,'outer'):
  x,y,L,a=sf_edge(w['p'],w['q']);facade_box(m,x,y,0,.38,H+coping/2,L+.06,.12,coping,trim,a)
def glass110(m,x,y,u,b,w,h,a,frame,n=1,o=.14,rails=()):
 # A glazed opening: glass, a frame round it, n lights, optional transoms at the heights rails.
 facade_box(m,x,y,u,o-.04,b+h/2,w,.02,h,GLAZE,a)
 for zz in (b+.04,b+h-.04)+tuple(rails):facade_box(m,x,y,u,o,zz,w,.07,.07,frame,a)
 for k in range(n+1):facade_box(m,x,y,max(-w/2+.04,min(w/2-.04,-w/2+k*w/n))+u,o,b+h/2,.07,.07,h,frame,a)
def win110(m,x,y,u,b,w,h,a,frame,sur=None,rows=2,bw=.14,sill=None):
 cas81(m,x,y,u,b,w,h,a,frame,.16,rows)
 if sur:surround36(m,x,y,u,b,w,h,a,sur,bw,.40)
 if sill:facade_box(m,x,y,u,.47,b-.05,w+.24,.16,.07,sill,a)
def prism110(m,x,y,u,outline,o0,o1,ma,a):
 n=len(outline);vs=[lp(x,y,u+du,o,zz,a) for o in (o0,o1) for du,zz in outline]
 m.faces(vs,[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],ma)
def joints110(m,x,y,L,a,z0,z1,step,ma,rows=()):
 # Slab joints: vertical grooves every step metres between z0 and z1, and horizontal ones.
 n=max(1,round(L/step))
 for k in range(1,n):facade_box(m,x,y,-L/2+k*L/n,.365,(z0+z1)/2,.03,.02,z1-z0,ma,a)
 for zz in rows:facade_box(m,x,y,0,.365,zz,L,.02,.03,ma,a)

# ---- 91265011: the stone-clad commercial block. Six equal bays (contributor photo, style only;
# the bay count and the heights are estimated from the photo's proportions).
if b110_ok(Z['g011']['mesh']):
 m=b110_new(Z['g011']['mesh'],'Storgatan/Buildings');ST=M['Slab']
 A,B=(-181.39,2.98),(-129.26,2.59);H=Z['g011']['height']
 for w in fronts110(m,'g011',FRONT110(0,-1),ST,M['Alu'],ST,2,1.0):
  x,y,L,a=sf_edge(w['p'],w['q']);S=lambda s,w=w:U(w,*pt110(A,B,s))
  n=6;bw=L/n
  shops=[(S((k+.5)*bw),0,bw-.70,3.40) for k in range(n)]
  ribs=[(S((k+.5)*bw),5.00,bw-.70,1.55) for k in range(n)]
  bz_wall(m,w['p'],w['q'],0,H,[(u,b,ww,hh,0) for u,b,ww,hh in shops+ribs],ST)
  for k,(u,b,ww,hh) in enumerate(shops):
   # Recessed shopfronts: four wrapped in blue film with a door each, two glazed.
   if k<4:
    facade_box(m,x,y,u,.04,b+hh/2,ww,.02,hh,M['NSBlue'],a)
    for zz in (b+.05,b+hh-.05):facade_box(m,x,y,u,.08,zz,ww,.06,.08,M['Alu'],a)
    for j in range(1,3):facade_box(m,x,y,u-ww/2+j*ww/3,.08,b+hh/2,.06,.06,hh,M['Alu'],a)
   else:
    glass110(m,x,y,u,b,ww,hh,a,M['Dark'],3,.08,(2.40,))
    facade_box(m,x,y,u+ww/2-1.0,.05,1.15,1.0,.03,2.30,M['Dark'],a)
  for u,b,ww,hh in ribs:glass110(m,x,y,u,b,ww,hh,a,M['Dark'],max(2,round(ww/1.25)),.20)
  # Full-height piers between the bays, the slab joints, the parapet's dark coping.
  for k in range(n+1):
   s=k*bw;pw=.70 if 0<k<n else .45;s=min(max(s,pw/2),L-pw/2)
   facade_box(m,x,y,S(s),.46,(H-.25)/2,pw,.22,H-.25,M['Pier'],a)
  joints110(m,x,y,L,a,3.40,5.00,1.30,M['Groove'],(4.20,))
  joints110(m,x,y,L,a,6.55,H,1.30,M['Groove'],(7.35,))
  facade_box(m,x,y,0,.42,H+.06,L+.06,.18,.14,M['Dark'],a)
 flatroof110(m,'g011',M['Sheet'],M['Dark'],.12)
 b110_finish(m,'91265011')

# ---- 91970373 (Viore): yellow render over dark stone shopfronts (contributor photo, style only).
if b110_ok(Z['v373']['mesh']):
 m=b110_new(Z['v373']['mesh'],'Storgatan/Buildings');YE=M['Yellow'];DS=M['DarkStone']
 A,B=(-129.26,2.59),(-116.13,2.61);H=Z['v373']['height']
 for w in fronts110(m,'v373',FRONT110(0,-1),YE,FR,YE,2,1.0):
  x,y,L,a=sf_edge(w['p'],w['q']);S=lambda s,w=w:U(w,*pt110(A,B,s))
  shops=[(S(2.10),.15,3.00,2.85),(S(5.20),0,1.60,2.70),(S(9.95),.30,5.30,2.70)]
  ups=[(S(.90+k*1.62),4.90,.95,1.35) for k in range(8)]
  bz_wall(m,w['p'],w['q'],0,3.80,[(u,b,ww,hh,0) for u,b,ww,hh in shops],DS)
  bz_wall(m,w['p'],w['q'],3.80,H,[(u,b,ww,hh,0) for u,b,ww,hh in ups],YE)
  for u,b,ww,hh in shops:glass110(m,x,y,u,b,ww,hh,a,M['Dark'],max(1,round(ww/1.6)),.12)
  # The big east window carries a black sign panel inside the glass.
  facade_box(m,x,y,S(10.5),.06,1.80,3.80,.02,2.20,M['Dark'],a)
  for s in (2.10,5.20,9.95):facade_box(m,x,y,S(s),.42,3.32,1.30,.08,.36,M['Cream'],a)
  for u,b,ww,hh in ups:win110(m,x,y,u,b,ww,hh,a,FR,None,1,.12,FR)
  facade_box(m,x,y,0,.42,3.86,L+.02,.14,.14,DS,a)
  facade_box(m,x,y,0,.55,H-.10,L+.10,.40,.24,M['Brown'],a)
 saddle82(m,'v373',(-129.263,2.592),(-116.132,2.612),M['Tile'],YE)
 for w in fronts110(m,'r373',lambda *_:False,M['Beige'],FR,FR,2,1.0):pass
 flatroof110(m,'r373',M['Sheet'],M['Beige'])
 b110_finish(m,'91970373')

# ---- 91970296: Sakligheter (west) and Synsam (east), split at the rear wing's line (estimated
# joint; contributor photo, style only).
if b110_ok(Z['s296']['mesh']):
 m=b110_new(Z['s296']['mesh'],'Storgatan/Buildings');SY=M['SakYellow'];DG=M['DarkGreen']
 A,B=(-116.13,2.61),(-103.70,2.61);H=Z['s296']['height']
 for w in fronts110(m,'s296',FRONT110(0,-1),SY,FR,SY,2,1.0):
  x,y,L,a=sf_edge(w['p'],w['q']);S=lambda s,w=w:U(w,*pt110(A,B,s))
  shops=[(S(2.10),.10,1.20,2.80),(S(4.70),.35,3.40,2.75),(S(8.70),.35,3.90,2.75)]
  ups=[(S(1.40+k*1.18),5.20,.95,1.15) for k in range(9)]
  bz_wall(m,w['p'],w['q'],0,3.50,[(u,b,ww,hh,0) for u,b,ww,hh in shops],M['Dark'])
  bz_wall(m,w['p'],w['q'],3.50,H,[(u,b,ww,hh,0) for u,b,ww,hh in ups],SY)
  for u,b,ww,hh in shops:glass110(m,x,y,u,b,ww,hh,a,M['Dark'],max(1,round(ww/1.8)),.12)
  for s in (.85,11.55):facade_box(m,x,y,S(s),.42,1.70,.80,.10,3.40,M['Dark'],a)
  facade_box(m,x,y,0,.50,3.80,L+.02,.30,.60,DG,a);facade_box(m,x,y,S(6.4),.66,3.80,3.60,.02,.30,M['Cream'],a)
  for u,b,ww,hh in ups:win110(m,x,y,u,b,ww,hh,a,FR,None,1,.12,None)
  facade_box(m,x,y,0,.42,5.12,L,.12,.08,FR,a)
  # The dark green eave: a sloped fascia over the ribbon.
  vs=[lp(x,y,-L/2-.05,.36,H-.35,a),lp(x,y,L/2+.05,.36,H-.35,a),lp(x,y,L/2+.05,.95,H+.05,a),lp(x,y,-L/2-.05,.95,H+.05,a)]
  m.faces(vs,[(0,1,2,3),(3,2,1,0)],DG)
 flatroof110(m,'s296',M['Sheet'],DG,.10)
 GR=M['Granite'];A,B=(-103.70,2.61),(-92.38,2.61);H=Z['y296']['height']
 for w in fronts110(m,'y296',FRONT110(0,-1),GR,M['Dark'],GR,4,1.0):
  x,y,L,a=sf_edge(w['p'],w['q']);S=lambda s,w=w:U(w,*pt110(A,B,s))
  shops=[(S(3.10),.20,4.40,3.20),(S(8.20),.20,4.40,3.20)]
  ups=[(S(s),b,2.60,1.60) for s in (1.95,5.66,9.37) for b in (4.80,7.80,10.80)]
  bz_wall(m,w['p'],w['q'],0,H,[(u,b,ww,hh,0) for u,b,ww,hh in shops+ups],GR)
  for u,b,ww,hh in shops:glass110(m,x,y,u,b,ww,hh,a,M['Dark'],3,.12,(2.50,))
  facade_box(m,x,y,S(4.2),.10,1.30,1.10,.03,2.20,M['Dark'],a)
  for u,b,ww,hh in ups:glass110(m,x,y,u,b,ww,hh,a,M['Dark'],2,.16)
  facade_box(m,x,y,0,.80,3.65,L-.20,.90,.18,M['Dark'],a)
  joints110(m,x,y,L,a,3.80,H,1.10,M['Brown'],(4.40,6.40,7.40,9.40,10.40,12.40))
  facade_box(m,x,y,0,.42,H+.06,L+.06,.18,.14,M['Dark'],a)
 flatroof110(m,'y296',M['Sheet'],M['Dark'],.10)
 fronts110(m,'r296',lambda *_:False,M['Beige'],FR,FR,3,1.0);flatroof110(m,'r296',M['Sheet'],M['Beige'])
 b110_finish(m,'91970296')

# ---- 92379278 (Dillbergs Bokhandel): s from the west corner. Contributor photo, style only;
# the photo shows the ground floor and the first floor; the second floor is estimated.
if b110_ok(Z['d278']['mesh']):
 m=b110_new(Z['d278']['mesh'],'Storgatan/Buildings');SA=M['Salmon'];CR=M['Cream'];LI=M['Lime']
 A,B=(-151.94,-8.29),(-134.38,-8.40);H=Z['d278']['height']
 for w in fronts110(m,'d278',FRONT110(0,1),SA,FR,CR,3,1.0):
  x,y,L,a=sf_edge(w['p'],w['q']);S=lambda s,w=w:U(w,*pt110(A,B,s))
  shop=(S(15.16),.35,3.80,3.05);ent=(S(11.06),0,3.20,3.40);shut=[(S(3.05),.15,3.40,3.20),(S(6.85),.15,3.40,3.20)]
  ups=[(S(c+d),b,1.15,1.55) for c in (2.95,8.78,14.61) for d in (-.85,.85) for b in (5.30,8.00)]
  bz_wall(m,w['p'],w['q'],0,4.40,[(u,b,ww,hh,0) for u,b,ww,hh in [shop,ent]+shut],LI)
  bz_wall(m,w['p'],w['q'],4.40,H,[(u,b,ww,hh,0) for u,b,ww,hh in ups],SA)
  u,b,ww,hh=shop;glass110(m,x,y,u,b,ww,hh,a,M['Teal'],1,.14,(2.55,))
  u,b,ww,hh=ent;glass110(m,x,y,u,b,ww,hh,a,M['Teal'],3,.16,(2.55,))
  facade_box(m,x,y,u,.10,1.25,1.05,.03,2.50,M['Teal'],a);facade_box(m,x,y,u,.13,1.25,.85,.02,2.35,GLAZE,a)
  for u,b,ww,hh in shut:
   facade_box(m,x,y,u,.10,b+hh/2,ww,.03,hh,M['Shutter'],a)
   for k in range(1,int(hh/.12)):facade_box(m,x,y,u,.12,b+k*.12,ww,.01,.015,M['Alu'],a)
  facade_box(m,x,y,S(4.95),.20,1.75,.10,.10,3.20,M['Dark'],a)
  joints110(m,x,y,L,a,3.45,4.40,1.20,M['Groove'],(3.45,))
  for u,b,ww,hh in ups:win110(m,x,y,u,b,ww,hh,a,FR,CR,2,.16,CR)
  facade_box(m,x,y,0,.46,4.47,L+.04,.22,.16,CR,a)
  facade_box(m,x,y,0,.44,H-.25,L+.04,.18,.30,CR,a);facade_box(m,x,y,0,.56,H-.06,L+.16,.40,.14,CR,a)
  for s in (.20,L-.20):facade_box(m,x,y,S(s),.43,(4.40+H)/2,.40,.16,H-4.40,CR,a)
 saddle82(m,'d278',(-134.377,-8.396),(-151.937,-8.29),M['Tile'],SA)
 b110_finish(m,'92379278')

# ---- 92379304: limestone slab front (contributor photo, close: style and openings; heights
# scaled from the door, 2.3 m).
if b110_ok(Z['l304']['mesh']):
 m=b110_new(Z['l304']['mesh'],'Storgatan/Buildings');LI=M['Lime']
 A,B=(-134.38,-8.40),(-128.89,-8.44);H=Z['l304']['height']
 for w in fronts110(m,'l304',FRONT110(0,1),LI,M['Brown'],LI,2,1.0):
  x,y,L,a=sf_edge(w['p'],w['q']);S=lambda s,w=w:U(w,*pt110(A,B,s))
  gl=[(S(1.42),.15,2.25,3.05),(S(4.12),.05,2.15,3.15)];rib=(S(L/2),5.40,L-.50,1.80)
  bz_wall(m,w['p'],w['q'],0,H,[(u,b,ww,hh,0) for u,b,ww,hh in gl+[rib]],LI)
  for u,b,ww,hh in gl:glass110(m,x,y,u,b,ww,hh,a,M['Brown'],1,.12,(2.45,))
  facade_box(m,x,y,S(4.60),.16,1.20,.95,.04,2.30,M['Brown'],a);facade_box(m,x,y,S(4.60),.19,1.25,.80,.02,2.10,GLAZE,a)
  u,b,ww,hh=rib;glass110(m,x,y,u,b,ww,hh,a,M['Dark'],4,.18)
  joints110(m,x,y,L,a,3.25,5.40,.90,M['Groove'],(3.95,4.70))
  facade_box(m,x,y,S(2.80),.42,1.60,.50,.14,3.20,LI,a)
  facade_box(m,x,y,0,.42,H+.05,L+.04,.16,.12,M['Alu'],a)
 flatroof110(m,'l304',M['Sheet'],M['Alu'],.10)
 b110_finish(m,'92379304')

# ---- 92379276 (25 Södra Långgatan): s from the west corner. Resected panorama: camera
# (-108.28, -75.81), 2.6 m; the openings and heights measured on the facade plane.
if b110_ok(Z['w276']['mesh']):
 m=b110_new(Z['w276']['mesh'],'Kvarnholmen/Södra Långgatan');RE=M['Render'];BL=M['Blue']
 A,B=(-117.06,-68.77),(-104.98,-68.85);H=Z['w276']['height'];T=Z['w276']['top']
 for w in fronts110(m,'w276',FRONT110(0,-1),RE,FR,RE,2,1.0):
  x,y,L,a=sf_edge(w['p'],w['q']);S=lambda s,w=w:U(w,*pt110(A,B,s))
  ups=[(S(s),4.35,1.40,1.75) for s in (1.05,3.75,6.95,10.35)]
  shops=[(S(1.23),.45,2.00,2.45),(S(5.14),.45,2.50,2.45)]
  doors=[(S(3.12),.35,.95,2.15),(S(7.93),.10,1.38,2.35)];sd=(S(10.40),.10,2.40,2.35)
  bz_wall(m,w['p'],w['q'],0,H,[(u,b,ww,hh,0) for u,b,ww,hh in ups+shops+doors+[sd]],RE)
  for u,b,ww,hh in ups:win110(m,x,y,u,b,ww,hh,a,BL,None,2,.12,RE)
  for u,b,ww,hh in shops:glass110(m,x,y,u,b,ww,hh,a,BL,2,.14)
  u,b,ww,hh=doors[0];door83(m,x,y,u,b,ww,hh,a,BL,RE,glass=True)
  u,b,ww,hh=doors[1]
  for k in (-1,1):facade_box(m,x,y,u+k*ww/4,.12,b+hh/2,ww/2-.03,.07,hh,BL,a)
  facade_box(m,x,y,u,.17,b+hh*.70,ww-.20,.03,.04,M['Dark'],a)
  u,b,ww,hh=sd;glass110(m,x,y,u-.45,b,1.40,hh,a,BL,1,.14,(.60,));door83(m,x,y,u+.75,b,.90,hh,a,BL,RE,glass=True)
  for s,ww in ((1.36,2.70),(3.38,1.35),(5.47,2.80)):awning82(m,x,y,S(s),2.75,ww,a,M['Awning'],.85,.80)
  for k in range(2):facade_box(m,x,y,S(7.93),.55+.15*k,.06+.08*k,1.80,.30,.08,M['Plinth'],a)
  facade_box(m,x,y,0,.40,.18,L+.02,.10,.36,M['Plinth'],a)
  facade_box(m,x,y,0,.44,H-.15,L+.04,.18,.30,RE,a)
  for s in (.12,L-.12):town_rod(m,lp(x,y,S(s),.50,.30,a),lp(x,y,S(s),.50,H,a),.05,RE,8)
 saddle82(m,'w276',(-117.064,-68.773),(-104.978,-68.85),M['Tile'],RE)
 sl=(T-H)/(10.30/2);fw=[w for w in walls('w276','outer') if outward(w)[1]<-.9][0];x,y,L,a=sf_edge(fw['p'],fw['q'])
 for s in (2.90,9.20):
  u=U(fw,*pt110(A,B,s));dormer82(m,x,y,u,a,H,sl,1.35,1.00,M['DormerRed'],FR,M['DormerRed'],.90)
 fronts110(m,'b276',lambda *_:False,RE,FR,RE,2,1.0);flatroof110(m,'b276',M['Sheet'],RE)
 b110_finish(m,'92379276')

# ---- 92412841 (4 Västra Sjögatan): s from the north corner. Resected panorama: camera
# (-36.47, -113.74), 2.4 m (from the door, 2.03 m on its steps).
if b110_ok(Z['g841']['mesh']):
 m=b110_new(Z['g841']['mesh'],'Kvarnholmen/Västra Sjögatan');SG=M['Sage']
 A,B=(-29.014,-104.806),(-28.982,-116.748);H=Z['g841']['height']
 for w in fronts110(m,'g841',FRONT110(-1,0),SG,FR,M['Corner'],2,.9):
  x,y,L,a=sf_edge(w['p'],w['q']);S=lambda s,w=w:U(w,*pt110(A,B,s))
  ups=[(S(1.99),4.50,1.40,1.75),(S(4.44),4.50,1.40,1.75),(S(8.20),4.50,1.25,1.75),(S(10.75),5.06,.95,1.30)]
  gnd=[(S(1.14),1.60,1.45,1.60),(S(3.28),1.60,1.45,1.60),(S(7.48),1.60,1.40,1.60),(S(9.48),1.60,.85,1.60)]
  door=(S(10.70),.73,1.26,2.03)
  holes=[(u,b,ww,hh,0) for u,b,ww,hh in ups+gnd+[door]]
  bz_wall(m,w['p'],w['q'],0,H,holes,SG);boards81(m,x,y,L,a,.62,H-.15,holes,M['SageBoard'])
  for u,b,ww,hh in ups+gnd:win110(m,x,y,u,b,ww,hh,a,FR,FR,3,.12,FR)
  u,b,ww,hh=door;door83(m,x,y,u,b,ww,hh,a,M['DoorGreen'],FR,glass=False)
  steps82(m,x,y,u,ww+.2,b,a,M['Plinth'])
  # The porch: pilasters and an entablature over the door and the window beside it.
  for s in (8.95,11.80):facade_box(m,x,y,S(s),.48,2.15,.26,.26,3.10,FR,a)
  facade_box(m,x,y,S(10.37),.62,3.75,3.15,.55,.30,FR,a);facade_box(m,x,y,S(10.37),.66,3.95,3.30,.62,.10,M['Corner'],a)
  for s in (.12,6.05,8.85,11.82):facade_box(m,x,y,S(s),.42,(.62+H)/2,.22,.10,H-.62,M['Corner'],a)
  facade_box(m,x,y,0,.42,4.10,L,.10,.14,M['Corner'],a)
  facade_box(m,x,y,0,.40,.31,L+.02,.12,.62,M['DarkPlinth'],a)
  facade_box(m,x,y,0,.48,H-.10,L+.10,.20,.22,FR,a)
 r,sl=hip82(m,'g841',(-29.014,-104.806),(-28.982,-116.748),M['Tile'])
 # The lantern dormer: a white body standing on the front slope, a steep gable roof, twin lights.
 fw=[w for w in walls('g841','outer') if outward(w)[0]<-.9][0];x,y,L,a=sf_edge(fw['p'],fw['q']);u=U(fw,*pt110(A,B,3.70))
 back=1.80;zb=H+(back+.40-.355+.05)*sl-.15;zt=zb+2.30;dep=2.4
 box(m,*lp(x,y,u,.355-back-dep/2,0,a)[:2],1.70,dep,zt-zb,zb,WH,a)
 prism110(m,x,y,u,[(-.98,zt),(.98,zt),(0,zt+1.20)],.355-back-dep,.355-back+.12,WH,a)
 for k in (-1,1):cas81(m,x,y,u+k*.38,zt-1.45,.58,1.05,a,FR,.355-back+.04,2)
 town_rod(m,lp(x,y,u,.355-back-.8,zt+1.1,a),lp(x,y,u,.355-back-.8,zt+2.0,a),.03,M['Dark'],6)
 b110_finish(m,'92412841')

# ---- 92204180 (Norra Långgatan): s from the west corner. Panorama at its own position
# (-135.09, 69.41), 2.2 m; it puts the joint at x -132.7, on the OSM line used as the split.
if b110_ok(Z['w180']['mesh']):
 m=b110_new(Z['w180']['mesh'],'Kvarnholmen/Norra Långgatan');RE=M['Render']
 A,B=(-150.726,74.971),(-132.754,74.932);H=Z['w180']['height']
 for w in fronts110(m,'w180',FRONT110(0,-1),RE,FR,RE,2,1.0):
  x,y,L,a=sf_edge(w['p'],w['q']);S=lambda s,w=w:U(w,*pt110(A,B,s))
  cs=[2.65+k*2.85 for k in range(6)]
  ups=[(S(c),3.70,1.80,2.15) for c in cs];gnd=[(S(c),.45,1.80,2.40) for c in cs[:5]];door=(S(cs[5]),0,1.85,2.30)
  bz_wall(m,w['p'],w['q'],0,H,[(u,b,ww,hh,0) for u,b,ww,hh in ups+gnd+[door]],RE)
  for u,b,ww,hh in ups:
   glass110(m,x,y,u,b,ww,hh,a,M['Dark'],2,.16,(b+1.45,));awning82(m,x,y,u,5.70,ww+.10,a,M['CreamAwn'],.65,.55)
  for u,b,ww,hh in gnd:
   glass110(m,x,y,u,b,ww,hh,a,M['Dark'],2,.16);facade_box(m,x,y,u,.55,2.70,ww+.10,.40,.32,M['CreamAwn'],a)
  u,b,ww,hh=door
  for k in (-1,1):facade_box(m,x,y,u+k*(ww/2-.14),.14,hh/2,.28,.12,hh,M['Orange'],a)
  facade_box(m,x,y,u,.14,hh-.12,ww,.12,.24,M['Orange'],a);facade_box(m,x,y,u,.12,1.05,ww-.56,.03,2.10,GLAZE,a)
  facade_box(m,x,y,u,.10,1.05,.55,.04,2.10,M['Dark'],a)
  facade_box(m,x,y,u,.45,2.62,ww,.06,.36,M['Blue'],a)
  facade_box(m,x,y,0,.40,.22,L+.02,.10,.45,M['Plinth'],a)
  facade_box(m,x,y,0,.42,H+.05,L+.06,.18,.16,M['Sheet'],a)
 flatroof110(m,'w180',M['Sheet'],M['Sheet'],.10)
 A,B=(-132.754,74.932),(-113.902,74.892);H=Z['l180']['height']
 for w in fronts110(m,'l180',FRONT110(0,-1),RE,FR,RE,2,1.0):
  x,y,L,a=sf_edge(w['p'],w['q']);S=lambda s,w=w:U(w,*pt110(A,B,s))
  bays=[(1.50+k*4.46+1.73,3.46) for k in range(4)]
  lou=[(S(c),3.80,ww,2.30) for c,ww in bays];gl=[(S(c),.30,ww,2.70) for c,ww in bays]
  bz_wall(m,w['p'],w['q'],0,H,[(u,b,ww,hh,0) for u,b,ww,hh in lou+gl],RE)
  for u,b,ww,hh in lou:
   facade_box(m,x,y,u,.06,b+hh/2,ww,.02,hh,GLAZE,a)
   for k in range(int(hh/.16)):facade_box(m,x,y,u,.22,b+.08+k*.16,ww,.22,.05,M['Louvre'],a)
  for k,(u,b,ww,hh) in enumerate(gl):
   glass110(m,x,y,u,b,ww,hh,a,M['Dark'],2,.10)
   if k==0:
    for d in (-1,1):facade_box(m,x,y,u+d*.95,.16,1.40,.30,.12,2.70,M['Orange'],a)
    facade_box(m,x,y,u,.16,2.62,2.20,.12,.25,M['Orange'],a)
  facade_box(m,x,y,0,.40,.15,L+.02,.10,.30,M['Plinth'],a)
  facade_box(m,x,y,0,.42,H+.05,L+.06,.18,.16,M['Sheet'],a)
 flatroof110(m,'l180',M['Sheet'],M['Sheet'],.10)
 b110_finish(m,'92204180')

# ---- 91264997 (Åhléns/Kvasten): s from the west corner. Panorama at its own position
# (-72.64, 67.37), 2.4 m assumed; positions along the front carry about +-3 m.
if b110_ok(Z['a997']['mesh']):
 m=b110_new(Z['a997']['mesh'],'Kvarnholmen/Norra Långgatan');RE=M['Render']
 A,B=(-113.902,74.892),(-38.138,73.93);H=Z['a997']['height']
 for w in fronts110(m,'a997',FRONT110(0,-1),RE,FR,RE,3,1.0):
  x,y,L,a=sf_edge(w['p'],w['q']);S=lambda s,w=w:U(w,*pt110(A,B,s))
  gab=[27.30,34.50,42.40];GW=5.30;ent=42.40
  holes=[];shops=[];wins=[]
  # Ground shopfronts in 4.4 m bays west and east of the gables, under the two west gables.
  for c in [2.4+k*4.4 for k in range(5)]+[48.6+k*4.4 for k in range(6)]+gab[:2]:
   ww=3.70 if c not in gab else GW-.40;shops.append((S(c),.30,ww,4.20))
  # Upper floors: two rows in the west part (not seen, estimated), tall paired windows east.
  for c in [2.4+k*2.2 for k in range(10)]:
   for b in (5.60,7.50):wins.append((S(c),b,1.30,1.40))
  for c in [48.6+k*4.4 for k in range(6)]:
   for d in (-.75,.75):wins.append((S(c+d),5.90,1.15,2.85))
  for c in (30.90,38.45):wins.append((S(c),5.70,.95,2.90))
  bays=[(S(c),5.00,GW-.30,3.85) for c in gab]
  e=(S(ent),0,GW-.40,4.60)
  bz_wall(m,w['p'],w['q'],0,H,[(u,b,ww,hh,0) for u,b,ww,hh in shops+wins+bays+[e]],RE)
  for u,b,ww,hh in shops:glass110(m,x,y,u,b,ww,hh,a,FR,max(2,round(ww/1.3)),.12,(3.20,))
  for u,b,ww,hh in wins:glass110(m,x,y,u,b,ww,hh,a,FR,1,.16,((b+2.10,) if hh>2 else ()))
  for u,b,ww,hh in bays:glass110(m,x,y,u,b,ww,hh,a,FR,4,.30,(b+2.05,))
  # The recessed entrance: inner glazed wall with doors, soffit; the fascia over it.
  u,b,ww,hh=e
  glass110(m,x,y,u,b,ww,hh-.20,a,M['Teal'],4,-1.40,(2.40,))
  for k in (-1,1):facade_box(m,x,y,u+k*(ww/2+.02),-.55,hh/2,.04,1.80,hh,RE,a)
  facade_box(m,x,y,u,-.55,hh-.02,ww,1.80,.04,RE,a)
  for c in gab:
   u=S(c)
   # Glazed gable: a glass prism over the cornice, white frame on its edge, a canopy.
   tri=[(-GW/2,H-.10),(GW/2,H-.10),(0,H+3.10)]
   prism110(m,x,y,u,tri,-2.60,.40,GLAZE,a)
   for (u0,z0),(u1,z1) in ((tri[0],tri[2]),(tri[2],tri[1]),(tri[0],tri[1])):
    town_rod(m,lp(x,y,u+u0,.44,z0,a),lp(x,y,u+u1,.44,z1,a),.07,FR,6)
   town_rod(m,lp(x,y,u,.44,H-.10,a),lp(x,y,u,.44,H+3.10,a),.04,FR,6)
   for d in (-GW/4,GW/4):town_rod(m,lp(x,y,u+d,.44,H-.10,a),lp(x,y,u+d,.44,H+1.55,a),.04,FR,6)
   if c!=ent:awning82(m,x,y,u,8.20,GW-.20,a,M['CreamAwn'],.55,.70)
   facade_box(m,x,y,u,.48,4.75,GW+.10,.16,.50,FR,a)
  facade_box(m,x,y,S(ent),.58,4.75,2.40,.04,.30,M['RedSign'],a)
  facade_box(m,x,y,0,.42,4.75,L+.02,.12,.50,RE,a)
  facade_box(m,x,y,0,.46,H-.20,L+.04,.22,.30,RE,a);facade_box(m,x,y,0,.50,H+.05,L+.06,.30,.10,M['Sheet'],a)
 flatroof110(m,'a997',M['Sheet'],M['Sheet'],.10)
 b110_finish(m,'91264997')

# ---- 91970385: orange (west) and beige (east) houses, s from the east corner of each front.
# Contributor photo only (style, storeys and openings; scaled from the storey heights).
if b110_ok(Z['o385']['mesh']):
 m=b110_new(Z['o385']['mesh'],'Kvarnholmen/Norra Långgatan');OR=M['OrangeRender']
 A,B=(-58.67,62.657),(-67.142,62.792);H=Z['o385']['height']
 for w in fronts110(m,'o385',FRONT110(0,1),OR,FR,OR,4,1.0):
  x,y,L,a=sf_edge(w['p'],w['q']);S=lambda s,w=w:U(w,*pt110(A,B,s))
  shop=[(S(2.00),.40,3.20,2.60),(S(6.70),.20,2.80,2.80)];door=(S(4.45),0,1.10,2.60)
  ups=[(S(s),b,ww,1.40) for s,ww in ((1.00,.60),(1.85,.60),(3.00,.80),(4.05,.60)) for b in (4.50,7.30,10.10)]
  ups+=[(S(5.55),b,1.40,1.40) for b in (4.50,7.30,10.10)]
  bz_wall(m,w['p'],w['q'],0,3.70,[(u,b,ww,hh,0) for u,b,ww,hh in shop+[door]],M['Beige'])
  bz_wall(m,w['p'],w['q'],3.70,H,[(u,b,ww,hh,0) for u,b,ww,hh in ups],OR)
  for u,b,ww,hh in shop:glass110(m,x,y,u,b,ww,hh,a,M['Copper'],2,.14)
  u,b,ww,hh=door;door83(m,x,y,u,b,ww,hh,a,M['Copper'],M['Beige'],glass=True)
  facade_box(m,x,y,S(2.00),.48,3.25,3.20,.12,.42,FR,a);facade_box(m,x,y,S(2.00),.55,3.25,2.40,.02,.20,M['RedSign'],a)
  for u,b,ww,hh in ups:win110(m,x,y,u,b,ww,hh,a,FR,None,1,.12,FR)
  # The glazed oriel at the west end over the first and second floors; the round window above.
  oc=S(7.35);facade_box(m,x,y,oc,.80,7.00,1.90,.90,5.60,M['Oriel'],a)
  facade_box(m,x,y,oc,1.26,7.00,1.70,.02,5.20,GLAZE,a)
  for zz in (4.25,6.95,9.75):facade_box(m,x,y,oc,1.28,zz,1.92,.06,.12,FR,a)
  for d in (-.9,0,.9):facade_box(m,x,y,oc+d,1.28,7.00,.06,.06,5.60,FR,a)
  for k in (-1,1):facade_box(m,x,y,oc+k*.96,.80,7.00,.02,.70,5.20,GLAZE,a)
  porthole82(m,x,y,oc,11.05,.45,a,FR)
  facade_box(m,x,y,0,.44,3.75,L+.02,.16,.14,FR,a)
  facade_box(m,x,y,0,.46,H-.15,L+.04,.22,.30,OR,a)
 flatroof110(m,'o385',M['Sheet'],OR,.12)
 BE=M['BeigeR'];A,B=(-49.248,62.507),(-58.67,62.657);H=Z['b385']['height']
 for w in fronts110(m,'b385',FRONT110(0,1),BE,FR,BE,3,1.0):
  x,y,L,a=sf_edge(w['p'],w['q']);S=lambda s,w=w:U(w,*pt110(A,B,s))
  shop=[(S(c),.50,2.60,2.80) for c in (1.80,4.70,7.60)]
  ups=[(S(c),b,1.15,1.50) for c in (1.70,4.70,7.70) for b in (4.60,7.30)]
  bz_wall(m,w['p'],w['q'],0,H,[(u,b,ww,hh,0) for u,b,ww,hh in shop+ups],BE)
  for u,b,ww,hh in shop:glass110(m,x,y,u,b,ww,hh,a,M['Dark'],2,.14)
  for s in (.20,3.25,6.15,9.20):facade_box(m,x,y,S(s),.45,1.85,.40,.16,3.70,M['Copper'],a)
  facade_box(m,x,y,0,.46,3.55,L+.04,.18,.30,M['Copper'],a)
  for u,b,ww,hh in ups:win110(m,x,y,u,b,ww,hh,a,FR,FR,2,.12,FR)
  facade_box(m,x,y,0,.46,H-.15,L+.04,.22,.30,BE,a)
 saddle82(m,'b385',(-49.248,62.507),(-58.67,62.657),M['Tile'],BE)
 b110_finish(m,'91970385')

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block110_cameras=[
 sv_camera('545_Block110_Cal_SodraLanggatan25',-108.28,-75.81,2.60,332,15,90),
 sv_camera('546_Block110_Cal_VastraSjogatan4',-36.47,-113.74,2.40,62,15,90),
 sv_camera('547_Block110_Cal_NorraLanggatan24',-135.09,69.41,2.20,332,15,90),
 sv_camera('548_Block110_Cal_Ahlens',-72.64,67.37,2.40,332,15,90),
 ('549_Block110_Aerial',(-60.0,-60.0,110.0),(-100.0,20.0,4.0),20),
]
print('BLOCK110_GEOMETRY',len(block110_names),'dropped',block110_dropped,'skipped',block110_skipped)
