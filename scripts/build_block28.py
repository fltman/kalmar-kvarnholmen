"""Pass 28: the block between Larmgatan, Södra Långgatan, Kaggensgatan and Ölandsgatan.

Södra Långgatan 8: orange render with white lesenes, eleven bays in three sections, the middle
five under a pediment, an arched door in the east section and a carved double door in the west.
Södra Långgatan 10: the yellow range of 1881, two houses joined by a rusticated quoin strip:
the gate house with Corinthian pilasters, window crowns, a dentil cornice and a pedimented
risalit over the rusticated carriage gate, and the corner house with the chamfered corner and
its segmental attic. Kaggensgatan 5: green render, a rusticated ground floor with voussoirs over
segmental shop windows, two doors with oculi, the central carriage gateway and a wide red
dormer. Ölandsgatan: the rough-cast merchant house with its loft hatches and hoisting beam, the
lower house with the red carriage gate, and the three-storey corner house with grey quoins and
dormers. References: Google Street View April 2025 (resected), two contributed photospheres on
Kaggensgatan (2020, 2025), all view only. Zones: source/block28.json; see
references/block28-notes.md. Tenant signs and lettering are omitted.
"""
B28D=json.loads((R/'source/block28.json').read_text());Z=B28D['zones']
block28_names=[];B28={}
for old in [k for k in list(materials) if k.startswith('M_Block28_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Orange','TownIvory',(.74,.44,.27),.86,0),
 ('White','TownIvory',(.93,.92,.89),.82,0),
 ('Frame','TownPaintBrown',(.22,.15,.11),.55,0),
 ('Plinth','TownStone',(.56,.55,.52),.82,0),
 ('MetalRoof','TownMetalGrey',(.33,.35,.36),.55,.30),
 ('Yellow','TownIvory',(.87,.73,.43),.86,0),
 ('YellowTrim','TownIvory',(.85,.82,.73),.82,0),
 ('Rustic','TownIvory',(.84,.70,.42),.88,0),
 ('GateStone','TownStone',(.73,.72,.68),.84,0),
 ('Granite','TownStone',(.44,.43,.42),.78,0),
 ('Green','TownIvory',(.58,.64,.51),.86,0),
 ('GreenBase','TownIvory',(.52,.58,.46),.88,0),
 ('RedDormer','TownMetalRed',(.62,.20,.16),.55,.20),
 ('Tile','TownTileRed',(.55,.30,.21),.80,0),
 ('TileDark','TownTileRed',(.42,.26,.21),.82,0),
 ('RoughCast','TownIvory',(.90,.89,.86),.95,0),
 ('WhiteRender','TownIvory',(.92,.91,.89),.84,0),
 ('Quoin','TownStone',(.62,.62,.60),.84,0),
 ('RedFrame','TownPaintBrown',(.55,.21,.16),.55,0),
 ('RedGate','TownPaintBrown',(.62,.25,.19),.60,0),
 ('Oak','TownPaintBrown',(.50,.33,.18),.58,0),
 ('Timber','TownPaintBrown',(.30,.21,.14),.70,0),
 ('Awning','TownPanel',(.94,.94,.92),.90,0),
 ('AwningRed','TownPanel',(.38,.15,.15),.90,0),
 ('Dark','TownMetalGrey',(.05,.055,.06),.40,.20),
 ]:
 name='M_Block28_'+key;B28[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block28_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B28

def b28_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block28_names.append(name);return Mesh(name,category)
def b28_finish(m,osm):
 obj=s21_finish(m);obj['detail_pass']=28;obj['reference_notes']='references/block28-notes.md';obj['osm_way']=osm;return obj
def uat(w,X,Y):
 # Position along the wall (the facade frame's u) of a world point.
 x,y,L,a=sf_edge(w['p'],w['q']);return (X-x)*math.cos(a)+(Y-y)*math.sin(a)
def front(w,test):
 ox,oy=outward(w);x,y,L,a=sf_edge(w['p'],w['q']);return w['kind']=='outer' and test(ox,oy,x,y)
def strip(m,x,y,u0,u1,z0,z1,a,ma,o=.355,d=.06):
 if u1-u0>.01 and z1-z0>.01:facade_box(m,x,y,(u0+u1)/2,o+d/2,(z0+z1)/2,u1-u0,d,z1-z0,ma,a)
def plinth(m,x,y,L,a,holes,H,ma):
 # Base course clipped at the door and gate openings.
 cuts=sorted((u-w/2-.02,u+w/2+.02) for u,b,w,h,*_ in holes if b<H);at=-L/2
 for l,r in cuts+[(L/2,L/2)]:
  if l>at:facade_box(m,x,y,(at+l)/2,.385,H/2,l-at,.11,H,ma,a)
  at=max(at,r)
def rustic(m,x,y,u0,u1,z0,z1,a,ma,holes,course=.38):
 # Banded ground floor: raised courses with narrow joints, interrupted by the openings.
 z=z0
 while z+.1<z1:
  top=min(z+course-.05,z1);mid=(z+top)/2;at=u0
  for l,r in sorted((u-w/2-.10,u+w/2+.10) for u,b,w,h,rr in holes if b-.05<mid<b+h+rr+.05)+[(u1,u1)]:
   l=max(u0,min(u1,l));r=max(u0,min(u1,r))
   if l>at+.05:strip(m,x,y,at,l,z,top,a,ma,.355,.045)
   at=max(at,r)
  z+=course
def quoins(m,x,y,u,z0,z1,a,ma,side=1,course=.42,long=1.0,short=.62):
 # Alternating long and short blocks up a building edge; side points into the facade.
 k=0;z=z0
 while z+.1<z1:
  top=min(z+course-.05,z1);w=long if k%2==0 else short
  facade_box(m,x,y,u+side*w/2,.385,(z+top)/2,w,.07,top-z,ma,a);z+=course;k+=1
def pilaster(m,x,y,u,z0,z1,w,a,ma,cap=None,base=True):
 facade_box(m,x,y,u,.40,(z0+z1)/2,w,.09,z1-z0,ma,a)
 if base:facade_box(m,x,y,u,.42,z0+.10,w+.12,.13,.20,ma,a)
 if cap:
  # Corinthian capital read as a bell with two leaf tiers and corner volutes under the abacus.
  zc=z1;facade_box(m,x,y,u,.43,zc+.12,w+.02,.12,.24,cap,a);facade_box(m,x,y,u,.45,zc+.36,w+.14,.14,.22,cap,a)
  facade_box(m,x,y,u,.46,zc+.58,w+.26,.16,.12,cap,a)
  for s in (-1,1):town_rod(m,lp(x,y,u+s*(w/2+.04),.52,zc+.40,a),lp(x,y,u+s*(w/2+.10),.52,zc+.52,a),.045,cap,6)
def crown(m,x,y,u,z,w,a,ma,rise=.26):
 # Small triangular window crown on a ledge (the upper windows of Södra Långgatan 10).
 facade_box(m,x,y,u,.44,z+.05,w+.24,.14,.10,ma,a)
 tri=[(u-w/2-.10,z+.10),(u+w/2+.10,z+.10),(u,z+.10+rise)]
 vs=[lp(x,y,uu,o,zz,a) for o in (.36,.50) for uu,zz in tri]
 m.faces(vs,[(2,1,0),(3,4,5),(0,1,4,3),(1,2,5,4),(2,0,3,5)],ma)
def gable_front(m,x,y,u,z,w,rise,a,ma,trim,o0=.02,o1=.40,light=True):
 # Pediment: tympanum, raking and base cornices, optional oval light.
 tri=[(u-w/2,z),(u+w/2,z),(u,z+rise)]
 vs=[lp(x,y,uu,o,zz,a) for o in (o0,o1) for uu,zz in tri]
 m.faces(vs,[(2,1,0),(3,4,5),(0,1,4,3),(1,2,5,4),(2,0,3,5)],ma)
 for (u0,z0),(u1,z1) in ((tri[0],tri[2]),(tri[2],tri[1])):town_rod(m,lp(x,y,u0,o1+.10,z0+.06,a),lp(x,y,u1,o1+.10,z1+.06,a),.12,trim,8)
 facade_box(m,x,y,u,o1+.05,z+.05,w,.16,.12,trim,a)
 if light:
  k=24;cz=z+rise*.42
  m.faces([lp(x,y,u+.36*math.cos(t*math.tau/k),o1+.01,cz+.26*math.sin(t*math.tau/k),a) for t in range(k)],[tuple(range(k))],GLAZE)
  town_path(m,[lp(x,y,u+.44*math.cos(t*math.tau/k),o1+.05,cz+.34*math.sin(t*math.tau/k),a) for t in range(k+1)],.05,trim)
def oculus(m,x,y,u,z,r,a,frame,trim):
 k=24;m.faces([lp(x,y,u+r*math.cos(t*math.tau/k),.30,z+r*math.sin(t*math.tau/k),a) for t in range(k)],[tuple(range(k))],GLAZE)
 town_path(m,[lp(x,y,u+(r+.02)*math.cos(t*math.tau/k),.36,z+(r+.02)*math.sin(t*math.tau/k),a) for t in range(k+1)],.045,frame)
 town_path(m,[lp(x,y,u+(r+.14)*math.cos(t*math.tau/k),.42,z+(r+.14)*math.sin(t*math.tau/k),a) for t in range(k+1)],.07,trim)
 for t in range(4):ang=t*math.pi/2;town_rod(m,lp(x,y,u,.34,z,a),lp(x,y,u+r*math.cos(ang),.34,z+r*math.sin(ang),a),.02,frame,6)
def voussoirs(m,x,y,u,b,w,h,r,a,ma,n=9,depth=.50):
 # Radiating joints of a rusticated arch: wedge blocks round the head of the opening, each a
 # prism whose ring runs counter-clockwise as seen from the street.
 for k in range(n):
  t0=math.pi*k/n+.025;t1=math.pi*(k+1)/n-.025
  ring=[(u+(w/2+depth)*math.cos(t0),b+h+(r+depth)*math.sin(t0)),(u+(w/2+depth)*math.cos(t1),b+h+(r+depth)*math.sin(t1)),
   (u+(w/2+.03)*math.cos(t1),b+h+(r+.03)*math.sin(t1)),(u+(w/2+.03)*math.cos(t0),b+h+(r+.03)*math.sin(t0))]
  vs=[lp(x,y,uu,o,zz,a) for o in (.355,.44) for uu,zz in ring]
  m.faces(vs,[(3,2,1,0),(4,5,6,7)]+[(i,(i+1)%4,(i+1)%4+4,i+4) for i in range(4)],ma)
def awning(m,x,y,u,z,w,a,ma,depth=.95):s21_shallow_awning(m,x,y,u,z,w,a,ma,depth)
def roof_gable_behind(m,x,y,u,zb,w,rise,a,ma,depth):
 # Cross gable running back from a pediment into the main roof.
 pts=[(u-w/2-.15,zb),(u,zb+rise),(u+w/2+.15,zb)]
 for (u0,z0),(u1,z1) in zip(pts,pts[1:]):
  m.faces([lp(x,y,u0,.55,z0,a),lp(x,y,u1,.55,z1,a),lp(x,y,u1,-depth,z1,a),lp(x,y,u0,-depth,z0,a)],[(0,1,2,3)],ma)
def chimney(m,cx,cy,z,h,ma,cap):box(m,cx,cy,.62,.95,h,z,ma,0,cap)
# Roof insets follow the narrowest range of each zone (not its shortest edge, which on the
# irregular outlines would give a steep mansard band round a large flat top).
INSET={'sl8':2.4,'sl10w':4.4,'sl10c':4.4,'k5':4.4,'court':2.8,'o5w':3.4,'o5m':4.4,'k3':4.4}
def hip(zone,ma,ov=.45,top=None):
 pts=simplify(poly(zone),.8);H=Z[zone]['height'];ins=INSET[zone];rs=Z[zone]['top']-H
 inset_roof(m,pts,H,ins,rs,ma,ov,top);return rs/(ins+ov)

# ---------------------------------------------------------------- Södra Långgatan 8
OR,WH,FR,PLI=M['Orange'],M['White'],M['Frame'],M['Plinth']
H8=Z['sl8']['height'];PED=Z['sl8']['pediment']
m=b28_new('SM_Kvarnholmen_House_91856615','Kvarnholmen/Södra Långgatan block')
UPX=[-237.15,-239.10,-241.04,-243.40,-245.41,-247.41,-249.41,-251.39,-253.70,-255.76,-257.72]
for w in walls('sl8'):
 x,y,L,a=sf_edge(w['p'],w['q'])
 if not front(w,lambda ox,oy,mx,my:oy>.9 and my>-80):plain(m,w,H8,OR,FR,WH,2,1.0);continue
 us=[uat(w,X,-78.8) for X in UPX];ud_e=uat(w,-238.1,-78.8);ud_w=uat(w,-256.7,-78.8)
 holes=[(ud_e,.10,2.10,2.05,1.0),(ud_w,.10,2.05,2.25,1.0)]
 for i,u in enumerate(us):
  holes.append((u,4.92,1.10,1.74,0))
  # The east door spans the ground floor under windows 1-2, the carved west door 10-11.
  if i not in (0,1,9,10):holes.append((u,.82,1.12,2.47,0))
 bz_wall(m,w['p'],w['q'],0,H8,holes,OR)
 for u,b,ww,hh,r in holes:
  if r>0:arch_door(m,x,y,u,b,ww,hh,r,a,M['Oak']);town_path(m,[lp(x,y,u+(ww/2+.16)*math.cos(t*math.pi/16),.40,b+hh+(r+.16)*math.sin(t*math.pi/16),a) for t in range(17)],.09,PLI)
  elif b<1:s21_glass(m,x,y,u,b,ww,hh,a,FR,1,.74,False)
  else:s20_window(m,x,y,u,b,ww,hh,a,FR,OR)
 plinth(m,x,y,L,a,holes,.67,PLI)
 # White lesenes: full height at the ends and the section joints, ground floor between bays.
 for X0,X1 in ((-235.22,-236.0),(-241.63,-242.73),(-252.05,-252.88),(-258.6,-259.36)):
  u0,u1=sorted((uat(w,X0,-78.8),uat(w,X1,-78.8)));strip(m,x,y,max(u0,-L/2),min(u1,L/2),.67,7.35,a,WH,.355,.07)
 for i in range(len(us)-1):
  if i in (0,2,7,9):continue
  um=(us[i]+us[i+1])/2;strip(m,x,y,um-.22,um+.22,.67,3.81,a,WH,.355,.06)
 strip(m,x,y,-L/2,L/2,3.81,4.10,a,WH,.355,.14);p18_band(m,x,y,L+.2,4.05,a,WH,.22)
 strip(m,x,y,-L/2,L/2,7.30,H8-.20,a,WH,.355,.10);lm_cornice(m,x,y,L+.5,H8-.14,a,WH,False)
 # Pediment over the middle five bays with a stucco cartouche and two rosettes.
 pu0,pu1=sorted((uat(w,PED[0],-78.8),uat(w,PED[1],-78.8)));pw=pu1-pu0;pc=(pu0+pu1)/2
 gable_front(m,x,y,pc,H8+.08,pw,PED[2]-H8-.08,a,OR,WH,.02,.40,False)
 facade_box(m,x,y,pc,.46,H8+1.45,.70,.10,.62,WH,a);town_path(m,[lp(x,y,pc+.36*math.cos(t*math.tau/20),.50,H8+1.45+.34*math.sin(t*math.tau/20),a) for t in range(21)],.05,WH)
 for s in (-1,1):
  kk=12;m.faces([lp(x,y,pc+s*(pw/2-1.6)+.18*math.cos(t*math.tau/kk),.44,H8+.55+.18*math.sin(t*math.tau/kk),a) for t in range(kk)],[tuple(range(kk))],WH)
 roof_gable_behind(m,x,y,pc,H8+.08,pw,PED[2]-H8-.08,a,M['MetalRoof'],3.2)
hip('sl8',M['MetalRoof'])
for cx,cy in ((-240.0,-84.5),(-250.5,-84.5),(-241.5,-100.0)):chimney(m,cx,cy,10.2,1.2,OR,M['Dark'])
b28_finish(m,'91856615')

# ---------------------------------------------------------------- Södra Långgatan 10
YE,YT,RU,GS,GRN=M['Yellow'],M['YellowTrim'],M['Rustic'],M['GateStone'],M['Granite']
H10=Z['sl10w']['height'];RIS=Z['sl10w']['risalit'];QX=B28D['quoin_x']
def yellow_upper(m,w,x,y,L,a,pil,wins,z0=3.92):
 # Upper floor: pilasters with capitals, crowned windows, entablature and dentil cornice.
 holes=[(u,4.52,.96,2.05,0) for u in wins]
 for u in pil:pilaster(m,x,y,u,z0,7.05,.52,a,YT,YT)
 return holes
def yellow_top(m,x,y,L,a):
 strip(m,x,y,-L/2,L/2,7.66,7.86,a,YT,.355,.12);strip(m,x,y,-L/2,L/2,7.86,H10-.55,a,YE,.355,.02)
 lm_cornice(m,x,y,L+.5,H10-.18,a,YT,True)
def yellow_ground(m,x,y,L,a,holes,u0=None,u1=None):
 u0=-L/2 if u0 is None else u0;u1=L/2 if u1 is None else u1
 facade_box(m,x,y,(u0+u1)/2,.39,.20,u1-u0,.10,.40,GRN,a)
 rustic(m,x,y,u0,u1,.40,3.66,a,RU,holes)
 strip(m,x,y,u0,u1,3.66,3.92,a,YT,.355,.16);p18_band(m,x,y,u1-u0+.2,3.86,a,YT,.20)
def arch_row(m,x,y,a,centres,w=3.0,b=.25,h=1.25,r=1.5):
 return [(u,b,w,h,r) for u in centres]
m=b28_new('SM_Kvarnholmen_House_91856624','Kvarnholmen/Södra Långgatan block')
PX_W=[-232.77,-230.96,-229.08,-227.23,-225.38,-223.47,-221.54]
PX_E=[-215.76,-213.88,-212.00,-210.20,-208.32,-206.49,-204.61]
for w in walls('sl10w'):
 x,y,L,a=sf_edge(w['p'],w['q'])
 if not front(w,lambda ox,oy,mx,my:oy>.9 and my>-80):plain(m,w,H10,YE,FR,YT,2,1.1);continue
 Y0=-78.95;pw_=[uat(w,X,Y0) for X in PX_W];pe_=[uat(w,X,Y0) for X in PX_E]
 wins=[(p0+p1)/2 for p0,p1 in zip(pw_,pw_[1:])]+[(p0+p1)/2 for p0,p1 in zip(pe_,pe_[1:])]
 ru0,ru1=sorted((uat(w,RIS[0],Y0),uat(w,RIS[1],Y0)));rc=(ru0+ru1)/2
 upper=yellow_upper(m,w,x,y,L,a,[p for p in pw_+pe_ if not(ru0-.1<p<ru1+.1)],wins)
 # Round-arched shop windows span two bays each, centred on every second pilaster.
 arches=arch_row(m,x,y,a,[uat(w,X,Y0) for X in (-230.96,-227.23,-223.47,-213.88,-210.20,-206.49)],3.05)
 holes=upper+arches
 # The main wall is opened behind the risalit's window and gate as well.
 bz_wall(m,w['p'],w['q'],0,H10,[h for h in holes if not(ru0<h[0]<ru1)]+[(rc,4.55,1.10,2.0,0),(rc,.12,2.60,1.45,1.20)],YE)
 for u,b,ww,hh,r in holes:
  if ru0<u<ru1:continue
  if r>0:p18_win(m,x,y,u,b,ww,hh,r,a,FR,YT,3,3)
  else:s20_window(m,x,y,u,b,ww,hh,a,M['White'],YT);crown(m,x,y,u,b+hh+.16,ww,a,YT)
 for u,b,ww,hh,r in upper:facade_box(m,x,y,u,.44,b-.10,ww+.34,.16,.12,YT,a)
 yellow_ground(m,x,y,L,a,[h for h in holes if h[1]<3.6 and not(ru0<h[0]<ru1)])
 # Quoin strips: the west end at Södra Långgatan 8 and the joint with the corner house.
 uq_w=uat(w,-235.0,Y0);uq_e=uat(w,QX,Y0)
 quoins(m,x,y,uq_w,.40,H10-.60,a,YT,1 if uq_w<0 else -1)
 quoins(m,x,y,uq_e,.40,H10-.60,a,YT,1 if uq_e<0 else -1)
 yellow_top(m,x,y,L,a)
 # Risalit, 0.25 m proud: paired pilasters, the crowned central window over a panel, the
 # rusticated carriage gate (piers dated 1881, not lettered) and the pediment with modillions.
 rw=ru1-ru0;rhole=[(0,4.55,1.10,2.0,0),(0,.12,2.60,1.45,1.20)]   # in the risalit wall's own frame
 bz_wall(m,lp(x,y,ru0,0,0,a)[:2],lp(x,y,ru1,0,0,a)[:2],.40,H10,rhole,YE,.36,.61)
 for s in (-1,1):facade_box(m,x,y,rc+s*rw/2,.485,(.40+H10)/2,.02,.25,H10-.40,YE,a)
 s20_window(m,*lp(x,y,rc,.25,0,a)[:2],0,4.55,1.10,2.0,a,M['White'],YT);crown(m,*lp(x,y,rc,.25,0,a)[:2],0,6.71,1.10,a,YT,.34)
 facade_box(m,x,y,rc,.70,4.28,1.50,.12,.62,YT,a)
 for s in (-1,1):
  for k in (0,1):pilaster(m,*lp(x,y,rc+s*(rw/2-.35-k*.62),.25,0,a)[:2],0,3.92,7.05,.50,a,YT,YT)
 arch_door(m,*lp(x,y,rc,.25,0,a)[:2],0,.12,2.60,1.45,1.20,a,M['Oak'])
 gw=3.9;facade_box(m,x,y,rc,.70,.20,gw,.12,.40,GRN,a)
 for s in (-1,1):
  for k in range(8):facade_box(m,x,y,rc+s*(1.30+.32),.70,.55+k*.38,.64 if k%2 else .50,.10,.33,GS,a)
 voussoirs(m,*lp(x,y,rc,.25,0,a)[:2],0,.12,2.60,1.45,1.20,a,GS,9,.46)
 facade_box(m,x,y,rc,.72,3.72,gw+.2,.14,.26,GS,a)
 gable_front(m,*lp(x,y,rc,.25,0,a)[:2],0,H10+.05,rw+.30,RIS[2]-H10-.05,a,YE,YT,.02,.40,False)
 for k in range(9):
  t=(k+.5)/9;uu=rc-(rw+.3)/2+t*(rw+.3);zz=H10+.05+(RIS[2]-H10-.05)*(1-abs(2*t-1))
  facade_box(m,*lp(x,y,uu,.25,0,a)[:2],0,.55,zz-.10,.12,.16,.14,YT,a)
 roof_gable_behind(m,x,y,rc,H10+.05,rw+.3,RIS[2]-H10-.05,a,M['MetalRoof'],2.6)
hip('sl10w',M['MetalRoof'])
for cx in (-230.0,-222.0,-210.0):chimney(m,cx,-85.0,11.0,1.3,YE,M['Dark'])
# Corner house: four bays on Södra Långgatan, the chamfer, then Kaggensgatan.
PX_C=[-203.13,-201.26,-199.34,-197.40,-195.50]
for w in walls('sl10c'):
 x,y,L,a=sf_edge(w['p'],w['q'])
 if front(w,lambda ox,oy,mx,my:oy>.9 and my>-80):
  pc_=[uat(w,X,-79.4) for X in PX_C];wins=[(p0+p1)/2 for p0,p1 in zip(pc_,pc_[1:])]
  upper=yellow_upper(m,w,x,y,L,a,pc_,wins)
  arches=arch_row(m,x,y,a,[uat(w,X,-79.4) for X in (-202.2,-198.4)],3.0)
  holes=upper+arches;bz_wall(m,w['p'],w['q'],0,H10,holes,YE)
  for u,b,ww,hh,r in holes:
   if r>0:p18_win(m,x,y,u,b,ww,hh,r,a,FR,YT,3,3)
   else:s20_window(m,x,y,u,b,ww,hh,a,M['White'],YT);crown(m,x,y,u,b+hh+.16,ww,a,YT);facade_box(m,x,y,u,.44,b-.10,ww+.34,.16,.12,YT,a)
  yellow_ground(m,x,y,L,a,[h for h in holes if h[1]<3.6]);yellow_top(m,x,y,L,a)
 elif front(w,lambda ox,oy,mx,my:ox>.5 and oy>.5):
  # Chamfer: rusticated piers, the shop door, the tall window between pilasters, the attic.
  holes=[(0,.10,1.70,2.75,0),(0,4.40,1.10,2.30,0)]
  bz_wall(m,w['p'],w['q'],0,H10,holes,YE)
  s21_glass(m,x,y,0,.10,1.70,2.75,a,M['Dark'],2,.78,True);s20_window(m,x,y,0,4.40,1.10,2.30,a,M['White'],YT)
  facade_box(m,x,y,0,.44,4.12,1.60,.14,.46,YT,a);crown(m,x,y,0,6.86,1.10,a,YT,.30)
  for s in (-1,1):
   for k in range(9):facade_box(m,x,y,s*(L/2-.42),.40,.55+k*.38,.84 if k%2 else .70,.10,.33,YT,a)
   pilaster(m,x,y,s*(L/2-.55),3.92,7.05,.48,a,YT,YT)
  facade_box(m,x,y,0,.39,.20,L,.10,.40,GRN,a);strip(m,x,y,-L/2,L/2,3.66,3.92,a,YT,.355,.16)
  yellow_top(m,x,y,L,a)
  # Segmental attic above the cornice with its round light.
  AT=Z['sl10c']['attic'];aw=L+.2;k=16;crest=[(aw/2*math.cos(math.pi*i/k),H10+1.05+(AT-H10-1.05)*math.sin(math.pi*i/k)) for i in range(k+1)]
  outline=[(-aw/2,H10-.05),(aw/2,H10-.05)]+crest
  n=len(outline);vs=[lp(x,y,uu,o,zz,a) for o in (.02,.42) for uu,zz in outline]
  m.faces(vs,[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],YE)
  town_path(m,[lp(x,y,uu,.50,zz+.07,a) for uu,zz in crest],.11,YT)
  for s in (-1,1):facade_box(m,x,y,s*(aw/2-.18),.46,H10+.50,.36,.10,1.0,YT,a)
  oculus(m,*lp(x,y,0,.12,0,a)[:2],0,H10+1.30,.46,a,M['White'],YT)
 elif front(w,lambda ox,oy,mx,my:ox>.9 and mx>-194):
  n=10;us=[-L/2+.9+(k+.5)*(L-1.8)/n for k in range(n)];pk=[-L/2+.9+k*(L-1.8)/n for k in range(n+1)]
  upper=yellow_upper(m,w,x,y,L,a,pk,us)
  arches=arch_row(m,x,y,a,[pk[k] for k in (1,3,5,7,9)],2.9)
  holes=upper+arches;bz_wall(m,w['p'],w['q'],0,H10,holes,YE)
  for u,b,ww,hh,r in holes:
   if r>0:p18_win(m,x,y,u,b,ww,hh,r,a,FR,YT,3,3)
   else:s20_window(m,x,y,u,b,ww,hh,a,M['White'],YT);crown(m,x,y,u,b+hh+.16,ww,a,YT);facade_box(m,x,y,u,.44,b-.10,ww+.34,.16,.12,YT,a)
  yellow_ground(m,x,y,L,a,[h for h in holes if h[1]<3.6])
  yellow_top(m,x,y,L,a)
 else:plain(m,w,H10,YE,FR,YT,2,1.1)
hip('sl10c',M['MetalRoof'])
chimney(m,-198.0,-92.0,11.0,1.3,YE,M['Dark'])
# Courtyard behind the gate house and the lower south-west wing: two storeys, flat roofs.
for w in walls('sl10yard'):plain(m,w,Z['sl10yard']['height'],YE,FR,YT,2,.9)
s21_flat_roof(m,simplify(poly('sl10yard'),.8),Z['sl10yard']['height'],M['MetalRoof'])
b28_finish(m,'91856624')

# ---------------------------------------------------------------- Kaggensgatan 5
GE,GB=M['Green'],M['GreenBase'];HK=Z['k5']['height']
m=b28_new('SM_Kvarnholmen_House_91856594','Kvarnholmen/Södra Långgatan block')
for w in walls('k5'):
 x,y,L,a=sf_edge(w['p'],w['q'])
 if not front(w,lambda ox,oy,mx,my:ox>.9 and mx>-194.5):plain(m,w,HK,GE,M['White'],M['White'],2,.9);continue
 # North to south: quoins, window, door with oculus, window, gateway, window, door with
 # oculus, window, window.
 un=uat(w,-192.9,-103.86);us_=-1 if un>0 else 1;span=L-.9;n=9;bw=span/n
 cen=[un+us_*(.9+(k+.5)*bw) for k in range(n)];kinds=['win','door','win','gate','win','door','win','win','win']
 holes=[]
 for u,kd in zip(cen,kinds):
  if kd=='win':holes.append((u,.55,2.0,1.90,.36))
  elif kd=='door':holes.append((u,.20,1.10,2.35,0))
  else:holes.append((u,.05,2.90,2.40,1.20))
  holes.append((u,4.60,1.05,1.98,0))
 bz_wall(m,w['p'],w['q'],0,HK,holes,GE)
 for (u,b,ww,hh,r),kd in zip([h for h in holes if h[1]<4],kinds):
  if kd=='win':p18_win(m,x,y,u,b,ww,hh,r,a,M['Frame'],GB,2,3)
  elif kd=='door':
   s20_door(m,x,y,u,b,ww,hh,a,M['Oak'])
   oculus(m,x,y,u,3.10,.36,a,M['Frame'],M['White'])
  else:
   arch_door(m,x,y,u,b,ww,hh,r,a,M['Dark'])
   for k in range(11):uu=u-ww/2+.15+k*(ww-.3)/10;town_rod(m,lp(x,y,uu,.42,b,a),lp(x,y,uu,.42,b+hh+r*math.sqrt(max(0,1-(2*(uu-u)/ww)**2))-.05,a),.018,IRON,6)
  if kd!='door':voussoirs(m,x,y,u,b,ww,hh,r,a,GB,11 if kd=='gate' else 9,.45)
 for u,b,ww,hh,r in holes:
  if b>4:s20_window(m,x,y,u,b,ww,hh,a,M['Frame'],M['White']);facade_box(m,x,y,u,.44,b+hh+.16,ww+.32,.14,.12,M['White'],a);facade_box(m,x,y,u,.44,b-.10,ww+.30,.16,.12,M['White'],a)
 for i,(kd,u) in enumerate(zip(kinds,cen)):
  if kd=='win' and i>=4:awning(m,x,y,u,2.95,2.2,a,M['AwningRed'],1.0)
 facade_box(m,x,y,0,.39,.18,L,.10,.36,M['Plinth'],a)
 rustic(m,x,y,-L/2,L/2,.36,3.85,a,GB,[h for h in holes if h[1]<4])
 strip(m,x,y,-L/2,L/2,3.85,4.05,a,M['White'],.355,.14)
 quoins(m,x,y,un,.40,HK-.30,a,M['White'],us_)
 lm_cornice(m,x,y,L+.5,HK-.16,a,M['White'],False)
sk=hip('k5',M['Tile'])
# Wide red dormer with four lights over the northern shop.
for w in walls('k5'):
 if front(w,lambda ox,oy,mx,my:ox>.9 and mx>-194.5):
  x,y,L,a=sf_edge(w['p'],w['q']);ud=uat(w,-192.9,-108.9);zf=HK+.9*sk
  facade_box(m,*lp(x,y,ud,-.90,0,a)[:2],0,-1.2,zf+.85,4.2,2.6,1.7,M['RedDormer'],a)
  for k in range(4):town_window(m,*lp(x,y,ud-1.5+k,-.76,0,a)[:2],zf+.85,.72,1.05,a,M['White'],False,2,2,False)
  facade_box(m,*lp(x,y,ud,-.90,0,a)[:2],0,-1.2,zf+1.78,4.5,2.9,.14,M['Tile'],a)
for g in Z['k5yard']['polygons']:
 inset_roof(m,simplify([tuple(v) for v in g],.8),Z['k5yard']['height'],2.4,Z['k5yard']['top']-Z['k5yard']['height'],M['Tile'],.40)
for w in walls('k5yard'):plain(m,w,Z['k5yard']['height'],GE,M['White'],M['White'],2,.9)
b28_finish(m,'91856594')

# ---------------------------------------------------------------- Courtyard house
m=b28_new('SM_Kvarnholmen_House_91856619','Kvarnholmen/Södra Långgatan block')
for w in walls('court'):plain(m,w,Z['court']['height'],M['RoughCast'],M['Frame'],M['White'],2,.9)
hip('court',M['MetalRoof'])
b28_finish(m,'91856619')

# ---------------------------------------------------------------- Ölandsgatan
RC,RF=M['RoughCast'],M['RedFrame']
m=b28_new('SM_Kvarnholmen_House_91856622','Kvarnholmen/Södra Långgatan block')
OL=lambda ox,oy,mx,my:oy<-.9 and my<-137
# Merchant house: shop windows under white awnings, loft hatches and the hoisting beam.
HW=Z['o5w']['height']
for w in walls('o5w'):
 x,y,L,a=sf_edge(w['p'],w['q'])
 if not front(w,OL):plain(m,w,HW,RC,RF,RC,2,1.0,False);continue
 Y0=-139.0;U=lambda X:uat(w,X,Y0)
 shops=[U(X) for X in (-244.6,-239.4,-237.2,-232.0,-229.9)]
 holes=[(u,.45,1.35,1.65,0) for u in shops]+[(U(-234.2),.20,1.0,2.30,0),(U(-242.0),.20,1.10,2.30,0)]
 holes+=[(U(-244.4),4.00,1.10,1.70,0),(U(-239.4),4.00,1.10,1.70,0),(U(-234.0),3.40,1.00,1.30,.50)]
 hatches=[U(X) for X in (-238.5,-234.4,-230.1)];holes+=[(u,6.62,.36,.36,0) for u in hatches]
 bz_wall(m,w['p'],w['q'],0,HW,holes,RC)
 for u,b,ww,hh,r in holes:
  if ww<.5:facade_box(m,x,y,u,.20,b+hh/2,ww,.10,hh,M['Timber'],a);continue
  # Awnings clear the pavement by 2 m at their front bar.
  if b<1 and hh<2:s21_glass(m,x,y,u,b,ww,hh,a,RF,2,.72,False);awning(m,x,y,u,2.62,ww+.35,a,M['Awning'],.70)
  elif b<1:s20_door(m,x,y,u,b,ww,hh,a,M['Oak'])
  elif r>0:p18_win(m,x,y,u,b,ww,hh,r,a,RF,RC,3,2)
  else:s20_window(m,x,y,u,b,ww,hh,a,RF,RC,.66,True)
 facade_box(m,x,y,0,.39,.22,L,.08,.44,RC,a)
 # Hoisting beam with its pulley block, iron wall anchors, eaves board and gutter.
 ub=U(-233.9);facade_box(m,x,y,ub,.95,7.55,.22,1.25,.26,M['Timber'],a);facade_box(m,x,y,ub,1.45,7.28,.16,.16,.30,M['Dark'],a)
 for X in (-237.8,-235.3,-232.4,-229.6):facade_box(m,x,y,U(X),.40,6.25,.05,.05,.55,IRON,a)
 facade_box(m,x,y,0,.45,HW-.10,L+.3,.22,.20,M['Timber'],a);town_rod(m,lp(x,y,-L/2-.1,.62,HW-.22,a),lp(x,y,L/2+.1,.62,HW-.22,a),.07,METAL,8)
hip('o5w',M['TileDark'],.40)
# House with the carriage gate: red arched gate, four upper windows, blank loft wall.
HM=Z['o5m']['height']
for w in walls('o5m'):
 x,y,L,a=sf_edge(w['p'],w['q'])
 if not front(w,OL):plain(m,w,HM,RC,RF,RC,2,1.0,False);continue
 Y0=-139.1;U=lambda X:uat(w,X,Y0)
 holes=[(U(-226.3),.05,2.20,2.00,1.10),(U(-214.1),.25,1.00,1.65,0)]+[(U(X),2.70,1.10,1.90,0) for X in (-223.5,-220.5,-218.4,-214.1)]
 bz_wall(m,w['p'],w['q'],0,HM,holes,RC)
 for u,b,ww,hh,r in holes:
  if r>0:arch_door(m,x,y,u,b,ww,hh,r,a,M['RedGate']);town_path(m,[lp(x,y,u+(ww/2+.14)*math.cos(t*math.pi/16),.40,b+hh+(r+.14)*math.sin(t*math.pi/16),a) for t in range(17)],.08,M['White'])
  else:s20_window(m,x,y,u,b,ww,hh,a,RF,RC,.66,True)
 ug=U(-226.3)
 for s in (-1,1):facade_box(m,x,y,ug+s*1.75,.40,2.45,.06,.06,.50,IRON,a)
 facade_box(m,x,y,0,.39,.20,L,.08,.40,RC,a)
 facade_box(m,x,y,0,.45,HM-.10,L+.3,.22,.20,M['Timber'],a);town_rod(m,lp(x,y,-L/2-.1,.62,HM-.22,a),lp(x,y,L/2+.1,.62,HM-.22,a),.07,METAL,8)
sm=hip('o5m',M['Tile'],.40)
for cx in (-223.0,-216.0):chimney(m,cx,-134.0,11.2,1.4,RC,M['Dark'])
# Corner house: smooth white render, grey quoins, three storeys and tiled dormers.
HC=Z['k3']['height']
for w in walls('k3'):
 x,y,L,a=sf_edge(w['p'],w['q'])
 if front(w,OL):
  Y0=-139.3;U=lambda X:uat(w,X,Y0);bays=[U(X) for X in (-209.9,-207.0,-204.1,-201.2,-198.3,-195.4)];door=bays[4]
 elif front(w,lambda ox,oy,mx,my:ox>.9 and mx>-195):
  U=lambda Y:uat(w,-193.7,Y);bays=[U(Y) for Y in (-137.0,-134.0,-131.0)];door=None
 else:plain(m,w,HC,M['WhiteRender'],RF,M['WhiteRender'],3,.9);continue
 holes=[]
 for u in bays:
  holes.append((u,.10,1.10,2.25,0) if u==door else (u,.30,1.10,1.62,0))
  holes+=[(u,2.84,1.15,1.90,0),(u,6.65,1.15,1.84,0)]
 bz_wall(m,w['p'],w['q'],0,HC,holes,M['WhiteRender'])
 for u,b,ww,hh,r in holes:
  if b<.2:s20_door(m,x,y,u,b,ww,hh,a,M['Oak'])
  else:s20_window(m,x,y,u,b,ww,hh,a,RF,M['WhiteRender'],.66,True)
 facade_box(m,x,y,0,.39,.20,L,.08,.40,M['Quoin'],a)
 for X,Y in ((-211.7,-139.3),(-193.84,-139.56)):
  uq=uat(w,X,Y)
  if abs(uq)<=L/2+.05:quoins(m,x,y,uq,.40,HC-.35,a,M['Quoin'],1 if uq<0 else -1,.40,.80,.50)
 lm_cornice(m,x,y,L+.5,HC-.16,a,M['WhiteRender'],False)
sc=hip('k3',M['Tile'],.40)
for w in walls('k3'):
 x,y,L,a=sf_edge(w['p'],w['q'])
 if front(w,OL):
  for X in (-210.3,-206.8):roof_dormer(m,x,y,uat(w,X,-139.3),a,HC,sc,.60,.80,1.0,M['WhiteRender'],M['Tile'],RF,False)
 elif front(w,lambda ox,oy,mx,my:ox>.9 and mx>-195):
  roof_dormer(m,x,y,uat(w,-193.7,-134.0),a,HC,sc,.60,.80,1.0,M['WhiteRender'],M['Tile'],RF,False)
chimney(m,-203.0,-133.8,13.2,1.3,M['WhiteRender'],M['Dark'])
b28_finish(m,'91856622')

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 # A resected Street View camera: model position and height, the panorama's heading and pitch.
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
# The model's wall slabs stand 0.355 m proud of the OSM line, so each resected camera keeps its
# measured distance from the modelled facade surface, not from the OSM line.
SLAB=.355
block28_cameras=[
 sv_camera('151_Block28_Cal_SL8',-246.04,-73.17+SLAB,2.21,152,20),
 sv_camera('152_Block28_SL10_Risalit',-214.71,-73.18+SLAB,1.85,152,22),
 sv_camera('153_Block28_Corner',-185.24,-73.5,2.1,194,20),
 sv_camera('154_Block28_Kaggensgatan',-186.8,-76.0,1.8,208,6,80),
 sv_camera('155_Block28_K5',-187.6,-114.0,1.7,242,12,80),
 sv_camera('156_Block28_Olands_W',-234.9,-144.49-SLAB,2.15,332,32),
 sv_camera('157_Block28_Cal_Olands_E',-216.06,-139.2-SLAB-5.68,2.15,332,32),
 ('158_Block28_Aerial',(-168.0,-168.0,46.0),(-224.0,-108.0,4.0),26),
 sv_camera('159_Block28_OddFellows',-287.51-SLAB-6.20,-160.9,2.15,62,32),
 sv_camera('160_Block28_Larm8',-286.3-SLAB-5.98,-108.82,2.10,62,28),
 sv_camera('161_Block28_Cal_Larm10',-255.65,-78.68+SLAB+5.75,2.0,152,22),
]
print('BLOCK28_GEOMETRY',len(block28_names))
