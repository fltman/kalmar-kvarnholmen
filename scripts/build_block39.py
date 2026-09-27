"""Pass 39: three district volumes on the south side of Södra Långgatan, between Västra Sjögatan and
the white house 92412846.

The yellow wooden corner house (92412832, "34" by its door): pale yellow vertical boarding between
white pilasters, two storeys, a frieze and eaves cornice, a steep tile roof hipped round the corner.
On Södra Långgatan: two window axes, a frontispiece with an arched door in a white surround, a
window above it and an attic storey under a pediment with an oculus, then a shop window with a
glazed door and two windows over them; a gable dormer either side of the frontispiece. On Västra
Sjögatan: four shop windows, an arched carriage gate, a door and a shop window under one transom,
seven windows above, a flush attic storey and four gable dormers.
The salmon house (92412859, Kalmar Stadsmission): a rusticated ground floor with four windows, the
glazed door and a recessed gateway in grey-green surrounds on a panelled plinth; a band with the
sill band over it; six brown casements with top lights; a thin string and a deep cornice (its
front top edge triangulated from two panoramas); a low metal roof behind it.
The grey wooden house (92412869, "39"): grey-blue vertical boarding on a dark plinth, four windows
and a panelled double gate under a dentil cornice on the ground floor, five windows above, all in
white surrounds under head boards; a white frieze and eaves; a sheet-metal roof with a chimney.

References: Google Street View April 2025 (five panoramas, registered on joints, corners and a
bundle of shared features), view only. Zones: source/block39.json; see references/block39-notes.md.
The shop lettering, the stencilled name on the salmon house and the signs are omitted.
"""
B39D=json.loads((R/'source/block39.json').read_text());Z=B39D['zones']
block39_names=[];B39={}
for old in [k for k in list(materials) if k.startswith('M_Block39_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Yellow','TownPaintBrown',(.92,.80,.58),.70,0),
 ('GreyBoard','TownPaintBrown',(.66,.70,.74),.70,0),
 ('Salmon','TownIvory',(.86,.50,.38),.88,0),
 ('Sage','TownIvory',(.62,.64,.57),.85,0),
 ('White','TownIvory',(.94,.94,.91),.82,0),
 ('BrownFrame','TownPaintBrown',(.36,.17,.12),.55,0),
 ('GreenDoor','TownPaintBrown',(.26,.35,.30),.55,0),
 ('GreyDoor','TownPaintBrown',(.60,.62,.62),.60,0),
 ('BrownDoor','TownPaintBrown',(.32,.16,.12),.55,0),
 ('Plinth','TownStone',(.52,.53,.52),.82,0),
 ('DarkPlinth','TownStone',(.30,.30,.31),.82,0),
 ('Stone','TownStone',(.62,.60,.56),.84,0),
 ('Tile','TownTileRed',(.62,.30,.20),.80,0),
 ('RoofDark','TownMetalGrey',(.30,.31,.32),.55,.30),
 ('RoofRed','TownMetalRed',(.40,.18,.14),.60,.10),
 ('Brick','TownTileRed',(.55,.25,.18),.85,0),
 ('Dark','TownMetalGrey',(.05,.055,.06),.40,.20),
 ]:
 name='M_Block39_'+key;B39[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block39_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B39;WH=M['White']

def b39_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block39_names.append(name);return Mesh(name,category)
def b39_finish(m,osm):
 obj=s21_finish(m);obj['detail_pass']=39;obj['reference_notes']='references/block39-notes.md';obj['osm_way']=osm;return obj
def kind39(w):
 ox,oy=outward(w)
 if w['kind']!='outer':return None
 if oy>.9 and max(w['p'][1],w['q'][1])>-81.5:return 'sodra'
 if ox<-.9 and min(w['p'][0],w['q'][0])<-28.5:return 'vsj'
 return None
def U(w,X,Y):
 # Position along a wall (its u axis, from the wall's middle) of the world point (X, Y).
 x,y,L,a=sf_edge(w['p'],w['q']);return (X-x)*math.cos(a)+(Y-y)*math.sin(a)
def others39(m,zone,wall,frame,levels):
 for w in walls(zone):
  if kind39(w):continue
  if w['kind']!='outer':bz_wall(m,w['p'],w['q'],w['z0'],Z[zone]['height'],[],wall)
  else:plain(m,w,Z[zone]['height'],wall,frame,WH,levels,.9)
def head39(m,x,y,u,top,w,a,ma,board=.24,cap=.12):
 # A head board over a surround with a moulded cap (the wooden houses' window heads).
 facade_box(m,x,y,u,.40,top+board/2,w,.08,board,ma,a)
 facade_box(m,x,y,u,.45,top+board+cap/2,w+.14,.18,cap,ma,a)
def pil39(m,x,y,u0,u1,z0,z1,a,ma):
 # A flat board pilaster with a plain base and a small capital under the frieze.
 u=(u0+u1)/2;w=abs(u1-u0)
 facade_box(m,x,y,u,.41,(z0+z1)/2,w,.11,z1-z0,ma,a)
 facade_box(m,x,y,u,.43,z0+.12,w+.06,.15,.24,ma,a);facade_box(m,x,y,u,.44,z1-.08,w+.08,.17,.16,ma,a)
def shopwin39(m,x,y,u,b,w,h,a,frame,cols=2,trans=None):
 # Shop window in a white casing: glass, frame, mullions and an optional transom.
 facade_box(m,x,y,u,.16,b+h/2,w,.03,h,GLAZE,a)
 for k in range(cols+1):facade_box(m,x,y,u-w/2+k*w/cols,.24,b+h/2,.07,.10,h,frame,a)
 for zz in (b+.035,b+h-.035)+((b+h*trans,) if trans else ()):facade_box(m,x,y,u,.24,zz,w,.10,.07,frame,a)
def casing39(m,x,y,u,b,w,h,a,ma,bw=.10,sill=True):
 surround36(m,x,y,u,b,w,h,a,ma,bw,.39)
 if sill:facade_box(m,x,y,u,.45,b-bw-.02,w+2*bw+.10,.16,.05,ma,a)
def leaves39(m,x,y,u,b,w,h,a,ma,trim,o=.26,rows=2):
 # A panelled double door or gate: two leaves, raised panels, a meeting stile.
 facade_box(m,x,y,u,o,b+h/2,w,.06,h,ma,a)
 for s in (-1,1):
  for k in range(rows):
   z0=b+.15+k*(h-.30)/rows;z1=b+.15+(k+1)*(h-.30)/rows-.12
   facade_box(m,x,y,u+s*w/4,o+.04,(z0+z1)/2,w/2-.28,.03,z1-z0,trim,a)
 facade_box(m,x,y,u,o+.04,b+h/2,.05,.04,h,trim,a)

# ---------------------------------------------------------------- the grey wooden house
m=b39_new('SM_Building_92412869','Kvarnholmen/Södra Långgatan south')
GB=M['GreyBoard'];HG=Z['gr']['height']
others39(m,'gr',GB,WH,2)
for w in walls('gr'):
 if kind39(w)!='sodra':continue
 x,y,L,a=sf_edge(w['p'],w['q']);S=lambda X:U(w,X,-80.88)
 # Openings from panorama "39" (x of the white surrounds' outer edges; surrounds 0.12 wide).
 GW=[(13.88,12.49),(11.74,10.36),(9.56,8.21),(7.48,6.08)]
 UW=[(13.83,12.52),(11.70,10.39),(9.54,8.21),(7.47,6.10),(5.29,3.93)]
 gf=[(S((p0+p1)/2),1.77,abs(p0-p1)-.24,1.55,0) for p0,p1 in GW]
 gate=(S(4.51),0,2.04,3.25,0)
 up=[(S((p0+p1)/2),4.53,abs(p0-p1)-.24,1.56,0) for p0,p1 in UW]
 holes=gf+[gate]+up
 bz_wall(m,w['p'],w['q'],0,HG,holes,GB)
 boards35(m,x,y,L,a,.75,6.50,holes,GB)
 for u,b,ww,hh,r in gf+up:
  casing39(m,x,y,u,b,ww,hh,a,WH,.12);casement36(m,x,y,u,b,ww,hh,a,WH,3,None,.20)
  head39(m,x,y,u,b+hh+.12,ww+.24,a,WH,.24 if b<2 else .27)
 # The gate: white pilasters, a lintel board, a dentil course and a cornice; grey panelled leaves.
 gu,gb,gw,gh,gr=gate
 for s0,s1 in ((5.77,5.53),(3.49,3.31)):pil39(m,x,y,S(s0),S(s1),0,gh,a,WH)
 facade_box(m,x,y,gu,.41,3.415,S(3.19)-S(5.80),.11,.33,WH,a)
 n=18
 for k in range(n):facade_box(m,x,y,S(5.72)+(k+.5)*(S(3.27)-S(5.72))/n,.50,3.63,.07,.08,.08,WH,a)
 facade_box(m,x,y,gu,.50,3.76,S(3.19)-S(5.80)+.10,.24,.16,WH,a)
 leaves39(m,x,y,gu,0,gw,gh,a,M['GreyDoor'],M['GreyDoor'],.24,2)
 plinth36(m,x,y,L,a,[(gu-gw/2-.25,gu+gw/2+.25)],.75,M['DarkPlinth'])
 # Corner boards, the frieze and the eaves; the white downpipe at the salmon house.
 for s0,s1 in ((15.05,14.82),(2.89,3.10)):facade_box(m,x,y,(S(s0)+S(s1))/2,.40,(.75+6.50)/2,abs(S(s1)-S(s0)),.10,5.75,WH,a)
 facade_box(m,x,y,0,.39,6.52,L,.08,.10,WH,a)
 eaves37(m,x,y,L,a,HG,WH,.40)
 town_rod(m,lp(x,y,S(3.02),.50,.25,a),lp(x,y,S(3.02),.50,HG,a),.05,WH,8)
sl=roof34(m,'gr',M['RoofDark'],GB)
box(m,10.2,-85.6,.55,.80,1.9,10.6,M['Brick'],0,M['Dark'])
b39_finish(m,'92412869')

# ---------------------------------------------------------------- the salmon house
m=b39_new('SM_Building_92412859','Kvarnholmen/Södra Långgatan south')
SA,SG=M['Salmon'],M['Sage'];HS=Z['sa']['height']
others39(m,'sa',SA,M['BrownFrame'],2)
for w in walls('sa'):
 if kind39(w)!='sodra':continue
 x,y,L,a=sf_edge(w['p'],w['q']);S=lambda X:U(w,X,-80.88)
 # Openings from panorama "37" (x of the grey-green surrounds' outer edges, 0.12 wide).
 UP=[(1.946,.595),(-.724,-2.11),(-2.691,-4.112),(-5.503,-6.928),(-8.192,-9.621),(-11.019,-12.485)]
 GF=[(1.996,.601),(-.667,-2.086),(-5.484,-6.935),(-8.174,-9.635)]
 up=[(S((p0+p1)/2),4.62,abs(p0-p1)-.24,1.78,0) for p0,p1 in UP]
 gf=[(S((p0+p1)/2),1.30,abs(p0-p1)-.24,1.80,0) for p0,p1 in GF]
 door=(S(-3.51),0,1.32,3.03,0);portal=(S(-11.73),0,2.28,3.02,0)
 holes=gf+[door,portal]+up
 bz_wall(m,w['p'],w['q'],0,HS,holes,SA)
 # The rusticated ground floor: courses 0.30 m from the plinth to the band.
 rustic(m,x,y,-L/2,L/2,1.18,3.74,a,SA,holes,.30)
 for u,b,ww,hh,r in up+gf:surround36(m,x,y,u,b,ww,hh,a,SG,.12,.39);casement36(m,x,y,u,b,ww,hh,a,M['BrownFrame'],2,.70,.20)
 # The glazed door (a transom over two leaves) and the gateway with its doors set back 0.8 m.
 du,db,dw,dh,_=door;surround36(m,x,y,du,db,dw,dh,a,SG,.15,.39)
 s21_glass(m,x,y,du,db,dw,dh,a,M['BrownDoor'],2,.78,True)
 pu,pb,pw,ph,_=portal;surround36(m,x,y,pu,pb,pw,ph,a,SG,.15,.39)
 for s in (-1,1):facade_box(m,x,y,pu+s*(pw/2-.03),-.22,ph/2,.06,1.15,ph,M['Plinth'],a)
 facade_box(m,x,y,pu,-.22,ph-.03,pw,1.15,.06,M['Plinth'],a)
 leaves39(m,x,y,pu,0,pw-.10,ph-.08,a,M['BrownDoor'],M['BrownDoor'],-.80,3)
 # The panelled plinth, the bands and the sill band, the string and the cornice.
 plinth36(m,x,y,L,a,[(du-dw/2-.18,du+dw/2+.18),(pu-pw/2-.18,pu+pw/2+.18)],1.18,M['Plinth'])
 for k in range(19):
  uu=-L/2+(k+.5)*L/19
  if all(abs(uu-u0)>w0/2+.25 for u0,b0,w0,h0,r0 in (door,portal)):facade_box(m,x,y,uu,.46,.60,.05,.03,.95,SG,a)
 facade_box(m,x,y,0,.46,1.16,L,.12,.05,SG,a)
 facade_box(m,x,y,0,.40,3.78,L,.09,.08,SG,a)
 facade_box(m,x,y,0,.43,4.23,L,.16,.28,SG,a);facade_box(m,x,y,0,.41,4.47,L,.11,.22,SG,a)
 facade_box(m,x,y,0,.40,7.125,L,.09,.13,SG,a)
 # Cornice: bed moulding, fascia and corona; the corona's front top edge 0.83 m out of the OSM
 # line at 7.70 m (triangulated from panoramas "37" and "39").
 facade_box(m,x,y,0,.53,7.37,L,.35,.16,SG,a);facade_box(m,x,y,0,.66,7.515,L+.04,.60,.13,SG,a)
 facade_box(m,x,y,0,.77,7.64,L+.08,.83,.12,SG,a)
 for s in (2.72,-13.20):town_rod(m,lp(x,y,S(s),.50,.25,a),lp(x,y,S(s),.50,7.30,a),.05,M['BrownFrame'],8)
sl=roof34(m,'sa',M['RoofRed'],SA)
rear35(m,'sar',SA,M['BrownFrame'],M['RoofRed'],2)
b39_finish(m,'92412859')

# ---------------------------------------------------------------- the yellow corner house
m=b39_new('SM_Building_92412832','Kvarnholmen/Södra Långgatan south')
YE=M['Yellow'];HY=Z['yl']['height']
others39(m,'yl',YE,WH,2)
UPB,UPT=4.37,6.21                                    # upper openings (surrounds 4.25-6.33)
for w in walls('yl'):
 k=kind39(w)
 if k is None:continue
 x,y,L,a=sf_edge(w['p'],w['q'])
 if k=='sodra':
  S=lambda X:U(w,X,-80.85)
  PIL=[(-13.33,-13.75),(-16.67,-17.08),(-20.25,-20.70),(-22.08,-22.67),(-28.44,-28.90)]
  UW=[(-14.55,-15.94),(-18.00,-19.40),(-20.82,-21.96),(-23.53,-24.98),(-26.02,-27.48)]
  up=[(S((p0+p1)/2),UPB,abs(p0-p1)-.24,UPT-UPB,0) for p0,p1 in UW]
  gw=[(S((p0+p1)/2),1.17,abs(p0-p1)-.24,1.86,0) for p0,p1 in UW[:2]]
  # The frontispiece's arched door: a rectangular hole to the crown and closed spandrel prisms.
  door=(S(-21.39),.50,.90,2.05,.45)
  shop=(S(-24.93),.98,2.42,2.24,0);sdoor=(S(-26.85),.55,.90,2.67,0)
  holes=gw+[(door[0],door[1],door[2],door[3]+door[4],0),shop,sdoor]+up
  bz_wall(m,w['p'],w['q'],0,HY,holes,YE)
  boards35(m,x,y,L,a,.92,6.75,holes+[(S((p0+p1)/2),.9,abs(p0-p1),5.9,0) for p0,p1 in PIL],YE)
  for u,b,ww,hh,r in up+gw:
   casing39(m,x,y,u,b,ww,hh,a,WH,.12);casement36(m,x,y,u,b,ww,hh,a,WH,2,.72,.20)
   facade_box(m,x,y,u,.46,b+hh+.16,ww+.40,.18,.08,WH,a)
  du,db,dwid,dh,dr=door
  spandrels(m,x,y,du,db,dwid,dh,dr,a,YE)
  p18_arch(m,*lp(x,y,du,0,0,a)[:2],db+dh,dwid+.02,dr+.01,.20,.40,a,WH,20)
  for s in (-1,1):facade_box(m,x,y,du+s*(dwid/2+.10),.40,(db+dh)/2,.20,.10,dh,WH,a)
  facade_box(m,x,y,du,.20,db+(dh+dr)/2,dwid,.04,dh+dr,M['GreenDoor'],a)
  facade_box(m,x,y,du,.25,db+dh,dwid,.06,.06,WH,a);facade_box(m,x,y,du,.25,db+dh/2,.05,.06,dh,M['Dark'],a)
  steps36(m,x,y,du,a,1.35,1.05,db,3,.90,M['Stone'])
  # The shop front: one white casing round the window and the glazed door with its transom.
  su,sb,sw,sh,_=shop;tu,tb,tw,th,_=sdoor
  shopwin39(m,x,y,su,sb,sw,sh,a,WH,2)
  s21_glass(m,x,y,tu,tb,tw,2.12,a,M['GreenDoor'],1,.75,True);shopwin39(m,x,y,tu,tb+2.12,tw,th-2.12,a,WH,1)
  for s0,s1 in ((-23.49,-23.61),(-26.19,-26.35),(-27.39,-27.51)):facade_box(m,x,y,(S(s0)+S(s1))/2,.40,(.92+3.35)/2,abs(S(s1)-S(s0)),.08,2.43,WH,a)
  facade_box(m,x,y,(S(-23.49)+S(-27.51))/2,.40,3.41,abs(S(-27.51)-S(-23.49)),.08,.14,WH,a)
  facade_box(m,x,y,(S(-23.49)+S(-27.51))/2,.46,3.50,abs(S(-27.51)-S(-23.49))+.10,.18,.07,WH,a)
  steps36(m,x,y,tu,a,1.20,1.00,tb,2,.70,M['Stone'])
  for p0,p1 in PIL:pil39(m,x,y,S(p0),S(p1),.80,6.75,a,WH)
  plinth36(m,x,y,L,a,[(du-.75,du+.75),(tu-.50,tu+.50)],.80,M['Plinth'])
  facade_box(m,x,y,0,.43,.86,L,.14,.12,YE,a)
  facade_box(m,x,y,0,.39,6.85,L,.08,.20,WH,a)
  eaves37(m,x,y,L,a,HY,WH,.45)
  # The frontispiece's short attic storey (its window sits on the main cornice) and the pediment
  # with the oculus, triangulated from panoramas "34" and "35" with the review cameras (so in the
  # model's frame): the window's top 8.55, the base cornice's top 8.6, the apex 10.82, all at the wall
  # face (the pediment is not broken forward).
  ZA=8.40
  au=(S(-20.25)+S(-22.67))/2;ax,ay,_=lp(x,y,au,0,0,a);aw=abs(S(-22.67)-S(-20.25))
  bz_wall(m,lp(ax,ay,-aw/2,0,0,a)[:2],lp(ax,ay,aw/2,0,0,a)[:2],HY-.3,ZA,[(0,7.45,.90,1.0,0)],YE)
  casing39(m,ax,ay,0,7.45,.90,1.0,a,WH,.08,False);casement36(m,ax,ay,0,7.45,.90,1.0,a,WH,2,None,.20)
  for s_ in (-1,1):facade_box(m,ax,ay,s_*(aw/2-.20),.41,(HY+ZA)/2,.40,.11,ZA-HY,WH,a)
  facade_box(m,ax,ay,0,-1.30,(HY+ZA)/2,aw,2.6,ZA-HY+.4,YE,a)
  facade_box(m,x,y,au,.45,ZA+.05,aw+.30,.20,.12,WH,a)
  pediment35(m,x,y,au,ZA,aw+.30,10.82,a,YE,WH,.40,.50,.22)
  k_=24;cz=9.50
  m.faces([lp(x,y,au+.19*math.cos(t*math.tau/k_),.42,cz+.19*math.sin(t*math.tau/k_),a) for t in range(k_)],[tuple(range(k_))],GLAZE)
  town_path(m,[lp(x,y,au+.25*math.cos(t*math.tau/k_),.44,cz+.25*math.sin(t*math.tau/k_),a) for t in range(k_+1)],.05,WH)
  # The pediment's roof: a small gable running back into the main roof.
  for s in (-1,1):
   vs=[lp(x,y,au+s*(aw/2+.15),.30,ZA+.20,a),lp(x,y,au,.30,10.70,a),lp(x,y,au,-2.6,10.70,a),lp(x,y,au+s*(aw/2+.15),-2.6,ZA+.20,a)]
   m.faces(vs,[(0,1,2,3) if s<0 else (3,2,1,0)],M['Tile'])
 else:
  S=lambda Y:U(w,-28.95,Y)
  PIL=[(-80.79,-81.25),(-87.45,-87.95),(-92.12,-92.54),(-95.85,-96.30),(-98.72,-99.22),(-104.30,-104.80)]
  UW=[(-82.62,-84.07),(-84.98,-86.42),(-89.27,-90.74),(-93.49,-94.90),(-96.80,-98.34),(-99.96,-101.42),(-102.17,-103.69)]
  up=[(S((p0+p1)/2),UPB,abs(p0-p1)-.24,UPT-UPB,0) for p0,p1 in UW]
  SH=[(-82.17,-84.19),(-84.51,-86.47),(-88.92,-90.92),(-93.40,-95.13)]
  shops=[(S((p0+p1)/2),1.05,abs(p0-p1)-.20,2.15,0) for p0,p1 in SH]
  gate=(S(-97.51),0,2.42,2.67,.45)
  wdoor=(S(-100.49),.55,.76,2.45,0);wwin=(S(-102.34),1.00,2.14,2.00,0)
  holes=shops+[(gate[0],0,gate[2],gate[3]+gate[4],0),wdoor,wwin]+up
  bz_wall(m,w['p'],w['q'],0,HY,holes,YE)
  boards35(m,x,y,L,a,.92,6.75,holes+[(S((p0+p1)/2),.9,abs(p0-p1),5.9,0) for p0,p1 in PIL],YE)
  for u,b,ww,hh,r in up:
   casing39(m,x,y,u,b,ww,hh,a,WH,.12);casement36(m,x,y,u,b,ww,hh,a,WH,2,.72,.20)
   facade_box(m,x,y,u,.46,b+hh+.16,ww+.40,.18,.08,WH,a)
  for u,b,ww,hh,r in shops:casing39(m,x,y,u,b,ww,hh,a,WH,.10);shopwin39(m,x,y,u,b,ww,hh,a,WH,1)
  # The carriage gate: diagonal boarding in two leaves under a segmental head, a white surround.
  gu,gb,gwid,gh,gr=gate
  spandrels(m,x,y,gu,gb,gwid,gh,gr,a,YE)
  facade_box(m,x,y,gu,.28,(gh+gr)/2,gwid,.06,gh+gr,M['GreenDoor'],a)
  for s in (-1,1):
   for j in range(9):
    z_=.25+j*.30;u0_=gu+s*.06;u1_=gu+s*(gwid/2-.06)
    if z_+(gwid/2)*.9<gh:town_rod(m,lp(x,y,u0_,.32,z_,a),lp(x,y,u1_,.32,z_+(gwid/2-.12)*.9,a),.012,M['Dark'],4)
  facade_box(m,x,y,gu,.33,(gh+gr)/2,.05,.04,gh+gr,M['Dark'],a)
  p18_arch(m,*lp(x,y,gu,0,0,a)[:2],gh,gwid+.04,gr+.02,.24,.40,a,WH,20)
  for s in (-1,1):facade_box(m,x,y,gu+s*(gwid/2+.12),.40,gh/2,.24,.10,gh,WH,a)
  facade_box(m,x,y,gu,.41,3.30,gwid+.70,.11,.18,WH,a)
  # The door and the shop window under one transom, in one white casing.
  wu,wb,wwid,wh_,_=wdoor;vu,vb,vw,vh,_=wwin
  s21_glass(m,x,y,wu,wb,wwid,2.02,a,M['GreenDoor'],1,.70,True);shopwin39(m,x,y,wu,wb+2.02,wwid,wh_-2.02,a,WH,1)
  shopwin39(m,x,y,vu,vb,vw,vh-.43,a,WH,1);shopwin39(m,x,y,vu,vb+vh-.43,vw,.43,a,WH,4)
  for s0,s1 in ((-99.96,-100.08),(-100.90,-101.24),(-103.44,-103.63)):facade_box(m,x,y,(S(s0)+S(s1))/2,.40,(.92+3.05)/2,abs(S(s1)-S(s0)),.08,2.13,WH,a)
  facade_box(m,x,y,(S(-99.96)+S(-103.63))/2,.40,3.05,abs(S(-103.63)-S(-99.96)),.08,.12,WH,a)
  steps36(m,x,y,wu,a,1.10,.90,wb,2,.60,M['Stone'])
  for p0,p1 in PIL:pil39(m,x,y,S(p0),S(p1),.80,6.75,a,WH)
  plinth36(m,x,y,L,a,[(gu-gwid/2-.30,gu+gwid/2+.30),(wu-.45,wu+.45)],.80,M['Plinth'])
  facade_box(m,x,y,0,.43,.86,L,.14,.12,YE,a)
  facade_box(m,x,y,0,.39,6.85,L,.08,.20,WH,a)
  eaves37(m,x,y,L,a,HY,WH,.45)
  # The flush attic storey on Västra Sjögatan (its window read straight on; its top and pediment
  # taken from the Södra Långgatan frontispiece).
  ZA=8.40
  au=S(-92.27);ax,ay,_=lp(x,y,au,0,0,a);aw=abs(S(-94.04)-S(-90.50))
  bz_wall(m,lp(ax,ay,-aw/2,0,0,a)[:2],lp(ax,ay,aw/2,0,0,a)[:2],HY-.3,ZA,[(0,7.42,1.05,.83,0)],YE)
  casing39(m,ax,ay,0,7.42,1.05,.83,a,WH,.06,False);casement36(m,ax,ay,0,7.42,1.05,.83,a,WH,2,None,.20)
  for s_ in (-1,1):facade_box(m,ax,ay,s_*(aw/2-.18),.41,(HY+ZA)/2,.36,.11,ZA-HY,WH,a)
  facade_box(m,ax,ay,0,-1.30,(HY+ZA)/2,aw,2.6,ZA-HY+.4,YE,a)
  facade_box(m,ax,ay,0,.45,ZA+.05,aw+.30,.20,.12,WH,a)
  pediment35(m,ax,ay,0,ZA,aw+.30,10.60,a,YE,WH,.40,.50,.22)
  for s_ in (-1,1):
   vs=[lp(ax,ay,s_*(aw/2+.15),.30,ZA+.20,a),lp(ax,ay,0,.30,10.48,a),lp(ax,ay,0,-2.6,10.48,a),lp(ax,ay,s_*(aw/2+.15),-2.6,ZA+.20,a)]
   m.faces(vs,[(0,1,2,3) if s_<0 else (3,2,1,0)],M['Tile'])
# The corner post: the two fronts' wall slabs stand 0.355 m out of their OSM lines, which leaves an
# open notch at the street corner; the corner pilaster wraps it.
box(m,-29.105,-80.64,.53,.51,5.95,.80,WH,0);box(m,-29.105,-80.64,.53,.51,.80,0,M['Plinth'],0)
box(m,-29.13,-80.62,.62,.58,.55,6.75,WH,0)
sl=roof34(m,'yl',M['Tile'],YE)
# Gable dormers: two on Södra Långgatan (the western one triangulated: its front in the wall face, the
# window 7.88-8.60, the apex 9.48), four on Västra Sjögatan over the window axes. roof_dormer takes its
# front's height from the roof line, so it is given the height at which the window's sill is right.
for w in walls('yl'):
 k=kind39(w)
 if k is None:continue
 x,y,L,a=sf_edge(w['p'],w['q'])
 at=[U(w,X,-80.85) for X in (-15.20,-26.70)] if k=='sodra' else [U(w,-28.95,Y) for Y in (-85.70,-88.60,-97.57,-100.69)]
 for u in at:roof_dormer(m,x,y,u,a,7.63+.355*sl,sl,-.355,.90,.85,YE,M['Tile'],WH,False)
for cx,cy in ((-24.6,-84.5),(-23.9,-95.2)):box(m,cx,cy,.60,.90,1.2,Z['yl']['top']-.3,M['Brick'],0,M['Dark'])
rear35(m,'yr',YE,WH,M['Tile'],2)
b39_finish(m,'92412832')

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
# The cameras keep their measured distance from the modelled facades (0.355 m proud of the OSM line).
block39_cameras=[
 sv_camera('225_Block39_Cal_Yellow',-16.058,-74.15+.355,2.39,152,0,75),
 sv_camera('226_Block39_Cal_Yellow_Roof',-16.058,-74.15+.355,2.39,175,22,75),
 sv_camera('227_Block39_Cal_Corner',-26.884,-74.892+.355,2.50,140,0,75),
 sv_camera('228_Block39_Cal_Corner_Roof',-26.884,-74.892+.355,2.50,140,25,75),
 sv_camera('229_Block39_Cal_Vsj',-35.392-.355,-93.396,2.46,62,5,75),
 sv_camera('230_Block39_Cal_Salmon',-5.27,-73.786+.355,2.30,152,0,75),
 sv_camera('231_Block39_Cal_Salmon_Roof',-5.27,-73.786+.355,2.30,152,25,75),
 sv_camera('232_Block39_Cal_Grey',4.94,-73.79+.355,2.35,133,0,75),
 sv_camera('233_Block39_Cal_Grey_Roof',4.94,-73.79+.355,2.35,133,20,75),
 ('234_Block39_Aerial',(-12.0,-52.0,36.0),(-8.0,-92.0,4.0),28),
]
print('BLOCK39_GEOMETRY',len(block39_names))
