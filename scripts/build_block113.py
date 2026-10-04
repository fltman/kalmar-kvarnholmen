"""Pass 113: the last generic pass-17 volumes near a street, scattered round the island.
- 90977144 (Ölandskajen): the long white one-storey magasin on a concrete loading platform with a
  black railing; loading doors and windows in 3.95 m bays between dark eaves brackets, a grey
  standing-seam saddle roof with roof lights, a hipped north end;
- 91915629 (Skeppsbron): the low light-grey flat-roofed hall with a white fascia band and a band of
  ground-floor glazing, its dark grey north end;
- 91846927 (north shore): the red boarded pavilion with white corner boards and base panels, white
  glazed doors, windows in red frames, dark posts carrying the deep eaves of a grey metal hipped
  roof;
- 1049819215 (Stationsgatan): the glazed pavilion in dark frames under a dark flat roof, the
  round blue P sign on a post;
- the unphotographed sheds 149000062 (white corrugated, as the pass-111 shed beside it), 90859836,
  90859884, 90859852 (red boarded yard outbuildings, tile saddle roofs), 93238185 (grey-white
  boarded, flat roof), 93192417 (yellow rendered annex, tile saddle roof), 92204195 (red boarded,
  flat roof, as the pass-109 outbuilding in front of it) and 1549543685 (small red boarded shed).

References: four Google Street View panoramas (one resected on the pavilion), view only. Zones:
source/block113.json; see references/block113-notes.md. Cars, signs' lettering, bicycles, lamps
and the containers on the quays are omitted.
"""
B113D=json.loads((R/'source/block113.json').read_text());Z=B113D['zones']
block113_names=[];B113={}
for old in [k for k in list(materials) if k.startswith('M_Block113_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('White','TownPaintWhite',(.93,.93,.91),.60,0),('Dark','TownMetalGrey',(.07,.07,.075),.45,.40),('Iron','TownMetalGrey',(.08,.08,.085),.45,.40),
 ('MagWall','TownPaintWhite',(.88,.87,.83),.75,0),('MagRoof','TownMetalGrey',(.60,.62,.64),.45,.35),('RoofLight','TownMetalGrey',(.22,.26,.32),.25,.50),
 ('Concrete','TownStone',(.62,.62,.60),.90,0),('Bracket','TownPaintBrown',(.17,.14,.12),.70,0),('MagDoor','TownPaintBrown',(.22,.20,.18),.65,0),
 ('HallGrey','TownPaintWhite',(.76,.77,.77),.60,.10),('Fascia','TownPaintWhite',(.92,.92,.91),.55,.10),('HallDark','TownMetalGrey',(.20,.22,.24),.55,.25),
 ('RoofFelt','TownMetalGrey',(.18,.18,.19),.85,0),
 ('Falu','TownPaintBrown',(.55,.17,.13),.80,0),('FaluDark','TownPaintBrown',(.42,.13,.10),.80,0),('Post','TownPaintBrown',(.14,.12,.11),.70,0),
 ('PavRoof','TownMetalGrey',(.40,.41,.42),.50,.35),('Frame','TownMetalGrey',(.10,.11,.12),.45,.40),
 ('Blue','TownPaintWhite',(.25,.36,.75),.55,0),
 ('Shed','TownPaintWhite',(.90,.90,.89),.60,0),('Rib','TownPaintWhite',(.82,.82,.81),.60,0),
 ('Tile','TownTileRed',(.74,.38,.25),.80,0),('Sheet','TownMetalGrey',(.24,.25,.26),.60,.20),
 ('GreyWhite','TownPaintWhite',(.84,.84,.81),.75,0),('Batten','TownPaintWhite',(.76,.76,.73),.75,0),
 ('Yellow','TownIvory',(.88,.79,.56),.90,0),('Plinth','TownStone',(.55,.55,.53),.90,0),
 ]:
 name='M_Block113_'+key;B113[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block113_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B113;WH=M['White']

block113_skipped=[]
def b113_new(name,category):
 old=bpy.data.objects.get(name)
 if old:
  dp=old.get('detail_pass') or 17
  # Never replace a mesh another later pass has detailed (a repeat build of this pass is fine).
  if dp>17 and dp!=113:block113_skipped.append((name,dp));print('BLOCK113_SKIP',name,dp);return None
  bpy.data.objects.remove(old,do_unlink=True)
 block113_names.append(name);return Mesh(name,category)
def drop_degenerate_faces113(obj,tol=1e-9):
 import bmesh
 bm=bmesh.new();bm.from_mesh(obj.data)
 def _thin(f):
  L=max(e.calc_length() for e in f.edges);return L>0 and 2*f.calc_area()/L<1e-4
 bad=[f for f in bm.faces if f.calc_area()<tol or len({v.index for v in f.verts})<len(f.verts) or _thin(f)]
 if bad:bmesh.ops.delete(bm,geom=bad,context='FACES_ONLY')
 bm.to_mesh(obj.data);bm.free();obj.data.update();return len(bad)
block113_dropped={}
def b113_finish(m,osm):
 obj=s21_finish(m);block113_dropped[obj.name]=drop_degenerate_faces113(obj)
 obj['detail_pass']=113;obj['reference_notes']='references/block113-notes.md';obj['osm_way']=osm;return obj

def pt113(a,b,s):
 # The point s metres from a towards b.
 L=math.dist(a,b);return (a[0]+(b[0]-a[0])*s/L,a[1]+(b[1]-a[1])*s/L)
def proj113(a,b,P):
 # Distance along a->b of the point P's foot.
 L=math.dist(a,b);return ((P[0]-a[0])*(b[0]-a[0])+(P[1]-a[1])*(b[1]-a[1]))/L
def long113(zone):
 # The longest edge of the zone's outline, as (p, q).
 g=Z[zone]['polygons'][0];es=[(g[i],g[(i+1)%len(g)]) for i in range(len(g))]
 return max(es,key=lambda e:math.dist(*e))
def flatroof113(m,zone,ma,trim,coping=.24,ov=.38):
 # Flat roof (triangulated, the outlines can be concave) and a coping on the outer walls.
 from mathutils import Vector
 from mathutils.geometry import tessellate_polygon
 H=Z[zone]['height']
 for g in Z[zone]['polygons']:
  vs=[(*v,H+.02) for v in g];tris=tessellate_polygon([[Vector(v) for v in vs]])
  m.faces(vs,[tuple(t) for t in tris]+[tuple(reversed(t)) for t in tris],ma)
 if trim:
  for w in walls(zone,'outer'):
   x,y,L,a=sf_edge(w['p'],w['q']);facade_box(m,x,y,0,ov,H+coping/2-.04,L+.06,.12,coping,trim,a)
def ribs113(m,x,y,L,a,z0,z1,ma,o=.37,step=.30):
 n=max(2,int(L/step))
 for k in range(1,n):facade_box(m,x,y,-L/2+k*L/n,o,(z0+z1)/2,.04,.03,z1-z0-.06,ma,a)
def win113(m,x,y,u,b,w,h,a,frame,trim=None,rows=2):
 cas81(m,x,y,u,b,w,h,a,frame,.16,rows)
 if trim:surround36(m,x,y,u,b,w,h,a,trim,.09,.39)

# ---- 90977144: the magasin. West front measured from the panorama on Järnvägsgatan (camera
# -528.65, -194.57, nominal; scale checked on the loading doors): platform 1.2, doors 1.2-3.35,
# eaves 4.8, ridge 8.4 over the north range; brackets every 3.95 m from s 7.6 (s from the north
# corner of the west wall, (-502.64, -181.30)).
m=b113_new(Z['ms']['mesh'],'Kvarnholmen/Ölandskajen')
if m:
 MW=M['MagWall'];WA=(-502.64,-181.30);WB=(-501.79,-221.86)
 H=Z['mn']['height'];BAY=3.95;S0=7.60
 def mag113(zone):
  for w in walls(zone):
   x,y,L,a=sf_edge(w['p'],w['q']);ox,oy=outward(w)
   if w['kind']!='outer':bz_wall(m,w['p'],w['q'],w['z0'],H,[],MW);continue
   west=ox<-.9 and L>3
   if west:
    # s of the wall ends on the global bay line (the south range is 4.2 m further west).
    sp=proj113(WA,WB,w['p']);sq=proj113(WA,WB,w['q']);sgn=1 if sq>sp else -1
    us=lambda s:sgn*(s-sp)-L/2
    ks=[k for k in range(-2,20) if min(sp,sq)+.9<S0+BAY*(k+.5)<max(sp,sq)-.9]
    holes=[];ops=[]
    for k in ks:
     u=us(S0+BAY*(k+.5))
     if k%3==1:holes.append((u,2.00,1.40,1.20,0));ops.append(('w',u))
     else:holes.append((u,1.20,2.00,2.15,0));ops.append(('d',u))
    bz_wall(m,w['p'],w['q'],0,H,holes,MW)
    for kind,u in ops:
     if kind=='w':win113(m,x,y,u,2.00,1.40,1.20,a,WH,None,2);facade_box(m,x,y,u,.44,1.97,1.60,.14,.06,M['Concrete'],a)
     else:
      facade_box(m,x,y,u,.15,1.20+2.15/2,2.00,.06,2.15,M['MagDoor'],a);facade_box(m,x,y,u,.18,2.70,1.70,.02,.90,GLAZE,a)
      facade_box(m,x,y,u,.16,1.70,.06,.04,1.0,M['Bracket'],a);surround36(m,x,y,u,1.20,2.00,2.15,a,M['Bracket'],.08,.39)
    # The eaves brackets at the bay lines.
    for k in range(-2,20):
     s=S0+BAY*k
     if not min(sp,sq)+.3<s<max(sp,sq)-.3:continue
     u=us(s);facade_box(m,x,y,u,.42,H-.75,.14,.12,1.30,M['Bracket'],a)
     town_rod(m,lp(x,y,u,.42,H-1.40,a),lp(x,y,u,.95,H-.50,a),.06,M['Bracket'],6)
    # The oval sign over the second bay of the north range.
    s=S0+BAY*1.5
    if min(sp,sq)<s<max(sp,sq):facade_box(m,x,y,us(s),.40,3.85,1.50,.04,.55,WH,a)
    # The loading platform along the front, its railing at the outer edge.
    facade_box(m,x,y,0,.355+1.20,.60,L,2.40,1.20,M['Concrete'],a)
    n=max(1,round(L/2.0))
    for j in range(n+1):facade_box(m,x,y,-L/2+.05+j*(L-.10)/n,2.45,1.20+.55,.05,.05,1.10,M['Iron'],a)
    for zz in (1.25,1.75,2.30):town_rod(m,lp(x,y,-L/2+.05,2.45,zz,a),lp(x,y,L/2-.05,2.45,zz,a),.025,M['Iron'],6)
   else:
    # The quay and end walls (not seen): loading doors in the same bays, no platform.
    n=max(1,int(L/BAY));holes=[]
    for j in range(n):
     u=-L/2+(j+.5)*L/n
     if L<6 or j%2==0:holes.append((u,0,2.00,2.60,0))
     else:holes.append((u,1.40,1.40,1.20,0))
    bz_wall(m,w['p'],w['q'],0,H,holes,MW)
    for u,b,ww,hh,r in holes:
     if b==0:facade_box(m,x,y,u,.15,hh/2,ww,.06,hh,M['MagDoor'],a);surround36(m,x,y,u,0,ww,hh,a,M['Bracket'],.08,.39)
     else:win113(m,x,y,u,b,ww,hh,a,WH,None,2)
   facade_box(m,x,y,0,.40,.20,L+.02,.10,.40,M['Concrete'],a)
   facade_box(m,x,y,0,.42,H-.10,L+.04,.14,.20,MW,a)
 for zone in ('ms','mn','mt'):mag113(zone)
 # Saddle roofs along the length, the eaves 0.9 m out; roof lights on the west slopes.
 def lights113(zone,A,B,ss,t0=1.6,t1=3.2,ln=3.6):
  d,n=frame82(A,B);H_=Z[zone]['height'];T_=Z[zone]['top'];r,Ls,Lt=rect82(zone,A,B);sl=(T_-H_)/(Lt/2)
  tmin=min((v[0]-A[0])*n[0]+(v[1]-A[1])*n[1] for g in Z[zone]['polygons'] for v in g)
  for s in ss:
   q=[(A[0]+d[0]*ss_+n[0]*(tmin+tt),A[1]+d[1]*ss_+n[1]*(tmin+tt),H_+tt*sl+.05) for ss_,tt in ((s-ln/2,t0),(s+ln/2,t0),(s+ln/2,t1),(s-ln/2,t1))]
   m.faces(q,[(0,1,2,3),(3,2,1,0)],M['RoofLight'])
 SA,SB=(-505.96,-222.0),(-505.2,-262.56)
 saddle82(m,'mn',WA,WB,M['MagRoof'],MW,True,.90)
 lights113('mn',WA,WB,(15.5,23.0))
 saddle82(m,'ms',SA,SB,M['MagRoof'],MW,True,.90)
 lights113('ms',SA,SB,(4.5,12.0,19.5,27.0,34.5))
 # The north end: hipped over its slanting east side (form estimated, not seen).
 tip=[(-502.39,-193.30),(-487.39,-193.24),(-491.56,-176.51),(-500.90,-176.65),(-502.64,-181.30)]
 inset_roof(m,tip,Z['mt']['height'],4.0,Z['mt']['top']-Z['mt']['height'],M['MagRoof'],.90)
 b113_finish(m,'90977144')

# ---- 91915629 (Skeppsbron): the low hall, measured on its west front from 10 Kom snart igen
# (camera 41.52, -284.07, nominal): fascia 4.2-5.0, glazing 1.0-2.6; the dark north end 4.5.
m=b113_new(Z['sl']['mesh'],'Kvarnholmen/Skeppsbron')
if m:
 for zone,wall,H in (('sd',M['HallDark'],4.5),('sl',M['HallGrey'],5.0)):
  for w in walls(zone):
   x,y,L,a=sf_edge(w['p'],w['q']);ox,oy=outward(w)
   if w['kind']!='outer':bz_wall(m,w['p'],w['q'],w['z0'],H,[],wall);continue
   holes=[]
   if zone=='sl' and ox<-.9:
    holes=[(-L/2+3.0+k*2.6,1.00,2.20,1.60,0) for k in range(5)]+[(L/2-2.6,0,3.0,3.2,0)]
   elif zone=='sl' and oy<-.9:holes=[(-3.0,1.00,2.20,1.60,0),(1.5,0,1.0,2.2,0)]
   elif zone=='sd' and ox<-.9:holes=[(0,0,1.0,2.2,0)]
   elif zone=='sd' and oy>.9:holes=[(-L/2+3+k*3.0,1.2,1.4,1.2,0) for k in range(int((L-4)/3.0))]
   elif zone=='sl' and ox>.9:holes=[(-L/2+3+k*3.5,1.2,1.4,1.2,0) for k in range(int((L-4)/3.5))]
   bz_wall(m,w['p'],w['q'],0,H,holes,wall)
   ribs113(m,x,y,L,a,.30,H-(.80 if zone=='sl' else .25),M['HallGrey'] if zone=='sl' else M['Frame'])
   for u,b,ww,hh,r in holes:
    if b>0:win113(m,x,y,u,b,ww,hh,a,M['Frame'],None,1)
    elif ww>2:
     facade_box(m,x,y,u,.15,hh/2,ww,.06,hh,M['HallGrey'],a)
     for k in range(1,12):facade_box(m,x,y,u,.19,k*hh/12,ww-.06,.02,.03,M['Frame'],a)
    else:door83(m,x,y,u,0,ww,hh,a,M['Frame'],M['Frame'],glass=True)
   if zone=='sl':facade_box(m,x,y,0,.43,H-.40,L+.06,.16,.80,M['Fascia'],a)
   else:facade_box(m,x,y,0,.42,H-.12,L+.04,.14,.24,M['Frame'],a)
   facade_box(m,x,y,0,.40,.15,L+.02,.10,.30,M['Plinth'],a)
  flatroof113(m,zone,M['RoofFelt'],None)
 b113_finish(m,'91915629')

# ---- 91846927: the red pavilion on the north shore, measured on its north-east front from the
# car park (camera resected to 88.9, 185.9, h 2.4): wall top 2.9-3.0, doors 0-2.4, eaves 3.0
# carried 1.4 m out on posts; ridge estimated.
m=b113_new(Z['pv']['mesh'],'Kvarnholmen/Östra Sjögatan')
if m:
 FA=M['Falu'];H=Z['pv']['height']
 for w in walls('pv','outer'):
  x,y,L,a=sf_edge(w['p'],w['q']);ox,oy=outward(w);holes=[];ops=[]
  if ox>.6 and oy>.6:
   # The north-east front, s from the east tip: two doors, then a bank of windows.
   T0=(82.44,176.9);us=lambda s:proj113(w['p'],w['q'],pt113(T0,(71.09,188.9),s))-L/2
   holes=[(us(2.55),0,1.05,2.25,0),(us(3.95),0,1.25,2.35,0)]+[(us(5.4+k*2.0),.55,1.75,1.85,0) for k in range(5)]
  elif L>3:
   n=max(1,int(L/2.6));holes=[(-L/2+(k+.5)*L/n,.55,1.60,1.85,0) for k in range(n)]
  bz_wall(m,w['p'],w['q'],0,H,holes,FA)
  boards82(m,x,y,L,a,.55,H-.25,holes,M['FaluDark'],.25)
  for u,b,ww,hh,r in holes:
   if b==0:door83(m,x,y,u,0,ww,hh,a,WH,WH,glass=hh>2.3)
   else:win113(m,x,y,u,b,ww,hh,a,M['FaluDark'],None,2);facade_box(m,x,y,u,.42,b-.04,ww+.10,.12,.06,WH,a)
  facade_box(m,x,y,0,.40,.27,L+.04,.08,.55,WH,a)
  for s_ in (-L/2+.08,L/2-.08):facade_box(m,x,y,s_,.40,H/2,.16,.10,H,WH,a)
  facade_box(m,x,y,0,.42,H-.12,L+.04,.12,.24,FA,a)
  # Posts under the deep eaves, 1.4 m out.
  if L>4:
   n=max(1,round(L/3.2))
   for k in range(n+1):
    u=-L/2+.3+k*(L-.6)/n;facade_box(m,x,y,u,.355+1.40,H/2,.16,.16,H,M['Post'],a)
 hull=[(66.36,161.32),(82.44,176.90),(71.09,188.90),(65.90,186.43)]
 o,i=inset_roof(m,hull,H,3.2,Z['pv']['top']-H,M['PavRoof'],1.60)
 for k in range(len(o)):town_rod(m,(*o[k],H-.10),(*o[(k+1)%len(o)],H-.10),.12,M['Post'],6)
 b113_finish(m,'91846927')

# ---- 1049819215: the glazed pavilion at the bus station (camera on Stationsgatan, nominal):
# roof top 3.0, fascia 2.55-3.0; the P sign at 4.6 on a post at the north-east corner.
m=b113_new(Z['bp']['mesh'],'Kvarnholmen/Stationsgatan')
if m:
 H=Z['bp']['height'];FR=M['Frame']
 for w in walls('bp','outer'):
  x,y,L,a=sf_edge(w['p'],w['q']);ox,oy=outward(w)
  bz_wall(m,w['p'],w['q'],0,.25,[],FR);bz_wall(m,w['p'],w['q'],2.55,H,[],FR)
  facade_box(m,x,y,0,.20,1.40,L-.10,.02,2.30,GLAZE,a)
  n=max(1,round(L/1.25))
  for k in range(n+1):facade_box(m,x,y,-L/2+.05+k*(L-.10)/n,.22,1.40,.08,.10,2.30,FR,a)
  for zz in (.30,1.05):facade_box(m,x,y,0,.22,zz,L,.08,.06,FR,a)
  facade_box(m,x,y,0,.50,H-.22,L+.60,.12,.46,FR,a)
  if ox>.6:door83(m,x,y,0,.25,1.60,2.20,a,FR,FR,glass=True)
 flatroof113(m,'bp',FR,None)
 X,Y=-505.6,4.3
 town_rod(m,(X,Y,0),(X,Y,4.15),.05,FR,8)
 ang=math.atan2(3.64+4.02,-506.22+509.41)
 k=24;r=.46;zc=4.60;ring=lambda rr,o:[lp(X,Y,rr*math.cos(t*math.tau/k),o,zc+rr*math.sin(t*math.tau/k),ang) for t in range(k)]
 m.faces(ring(r,.06),[tuple(range(k)),tuple(range(k-1,-1,-1))],M['Blue'])
 v=ring(r,.065)+ring(r+.07,.065);m.faces(v,[(t,(t+1)%k,k+(t+1)%k,k+t) for t in range(k)]+[(k+t,k+(t+1)%k,(t+1)%k,t) for t in range(k)],WH)
 for du,dz,ww,hh in ((-.10,0,.07,.50),(.02,.14,.20,.06),(.02,-.04,.20,.06),(.13,.05,.06,.18)):facade_box(m,X,Y,du,.075,zc+dz,ww,.01,hh,WH,ang)
 b113_finish(m,'1049819215')

# ---- The unphotographed sheds: plain walls, one door on the side facing the street or yard,
# windows on the other long walls, corner boards, a saddle roof along the long side or a flat
# roof with a fascia. Heights estimated from their detailed neighbours.
def shed113(m,zone,wall,trim,roofma,door=(0,-1),kind='boards',batten=None):
 H=Z[zone]['height'];outer=walls(zone,'outer')
 cand=[w for w in outer if outward(w)[0]*door[0]+outward(w)[1]*door[1]>.6] or outer
 dw=max(cand,key=lambda w:math.dist(w['p'],w['q']))
 for w in walls(zone):
  x,y,L,a=sf_edge(w['p'],w['q'])
  if w['kind']!='outer':bz_wall(m,w['p'],w['q'],w['z0'],H,[],wall);continue
  holes=[]
  if w is dw:holes.append((-L/2+min(1.4,L/3),0,.95,2.05,0))
  if L>3.6:
   n=int((L-(2.4 if w is dw else 0))/3.6)
   for k in range(n):holes.append(((L/2-1.6-k*3.6) if w is dw else (-L/2+(k+.5)*L/n),1.15,.85,.90,0))
  bz_wall(m,w['p'],w['q'],0,H,holes,wall)
  if kind=='boards':boards82(m,x,y,L,a,.30,H-.20,holes,batten or wall,.24)
  elif kind=='ribs':ribs113(m,x,y,L,a,.10,H-.10,batten or wall)
  for u,b,ww,hh,r in holes:
   if b==0:door83(m,x,y,u,0,ww,hh,a,batten or wall,trim,glass=False)
   else:win113(m,x,y,u,b,ww,hh,a,trim,trim,2)
  if kind!='ribs':
   for s_ in (-L/2+.08,L/2-.08):facade_box(m,x,y,s_,.40,H/2,.16,.10,H,trim,a)
  facade_box(m,x,y,0,.40,.15,L+.02,.08,.30,M['Plinth'],a)
 if Z[zone]['roof']=='saddle':p,q=long113(zone);saddle82(m,zone,tuple(p),tuple(q),roofma,wall,True,.30)
 else:flatroof113(m,zone,roofma,trim,.24)
for zone,cat,args in (
 ('s062','Kvarnholmen/Ölandskajen',(M['Shed'],WH,M['Shed'],(0,1),'ribs',M['Rib'])),
 ('r836','Kvarnholmen/Fiskaregatan',(M['Falu'],WH,M['Tile'],(0,1),'boards',M['FaluDark'])),
 ('r884','Kvarnholmen/Fiskaregatan',(M['Falu'],WH,M['Tile'],(0,1),'boards',M['FaluDark'])),
 ('r852','Kvarnholmen/Fiskaregatan',(M['Falu'],WH,M['Tile'],(0,1),'boards',M['FaluDark'])),
 ('w185','Kvarnholmen/Norra Långgatan',(M['GreyWhite'],WH,M['RoofFelt'],(0,-1),'boards',M['Batten'])),
 ('y417','Kvarnholmen/Storgatan',(M['Yellow'],WH,M['Tile'],(0,-1),'render',None)),
 ('r195','Kvarnholmen/Larmgatan',(M['Falu'],WH,M['RoofFelt'],(0,-1),'boards',M['FaluDark'])),
 ('s685','Kvarnholmen/Östra Vallgatan',(M['Falu'],WH,M['Sheet'],(0,-1),'boards',M['FaluDark'])),
 ):
 m=b113_new(Z[zone]['mesh'],cat)
 if m:shed113(m,zone,*args);b113_finish(m,Z[zone]['osm'])

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block113_cameras=[
 sv_camera('567_Block113_Cal_Magasin',-528.65,-194.57,2.30,110,8,90),
 sv_camera('568_Block113_Cal_Skeppsbron',41.52,-284.07,2.50,57,8,90),
 sv_camera('569_Block113_Cal_Paviljong',88.90,185.90,2.40,152,8,90),
 sv_camera('570_Block113_Cal_Busstation',-479.73,-1.91,2.50,250,8,90),
 ('571_Block113_Aerial',(-560.0,-300.0,60.0),(-494.0,-224.0,4.0),24),
]
print('BLOCK113_GEOMETRY',len(block113_names),'dropped',block113_dropped,'skipped',block113_skipped)
