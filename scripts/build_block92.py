"""Pass 92: the west side of Landshövdingegatan from Storgatan northwards, five district volumes:
- 93192387, the olive-green boarded corner house: five windows above and four below on Storgatan,
  the white carved double door at the west end, white corner boards, a red tiled saddle roof with
  two chimneys, the east gable on Landshövdingegatan with two windows a floor and a pair in the
  attic; behind it the low strip with the side door on steps and a small window; at its west end
  the pale green boarded gate under a yellow boarded panel;
- 93192432, the ochre rendered three-storey house: white corner pilasters, a dark brown plinth, the
  dark red gateway door, three windows below and four above in dark brown frames, and the street
  gable in gambrel form with two attic windows;
- 93192395, the stucco house: brown-pink ground floor on a grey plinth with two arched windows,
  two cellar lights and the arched gateway (white archivolt, lanterns omitted), a band, the
  beige-pink upper floors with three windows each in white surrounds, two wall anchors;
- 93192444, the red boarded house with its gable to the street, two windows a floor in ochre
  frames, and south of it, in the gap between the outlines, the carved double gate under the
  continued roof slope; its lower back wing;
- 93192382, the pink boarded two-storey house: light pink pilaster boards, three windows below and
  four above, the grey-green double door with its transom and panel at the north end, a dark
  plinth with a cellar hatch, a red tiled saddle roof with a chimney; its low back wing.

References: Google Street View April 2025 (four panoramas, resected on house corners), view only.
Zones: source/block92.json; see references/block92-notes.md. Signs, lamps, the street lantern,
plants, pipes and house numbers are omitted.
"""
B92D=json.loads((R/'source/block92.json').read_text());Z=B92D['zones']
block92_names=[];B92={}
for old in [k for k in list(materials) if k.startswith('M_Block92_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Olive','TownIvory',(.74,.68,.47),.82,0),('GatePale','TownIvory',(.80,.78,.58),.82,0),('Yellow','TownIvory',(.90,.75,.44),.82,0),
 ('Ochre','TownIvory',(.86,.64,.38),.92,0),('StuccoLow','TownIvory',(.68,.46,.39),.92,0),('StuccoUp','TownIvory',(.70,.58,.47),.92,0),
 ('Red','TownIvory',(.55,.19,.16),.82,0),('Pink','TownIvory',(.82,.60,.57),.82,0),('PinkTrim','TownPaintWhite',(.88,.76,.73),.60,0),
 ('Trim','TownPaintWhite',(.93,.93,.90),.55,0),('Cream','TownPaintWhite',(.92,.90,.82),.55,0),('Brown','TownPaintBrown',(.24,.14,.11),.55,0),
 ('DoorRed','TownPaintBrown',(.32,.12,.12),.55,0),('GateWood','TownPaintBrown',(.72,.46,.24),.60,0),('Frame92','TownPaintBrown',(.82,.62,.30),.60,0),
 ('GreyGreen','TownPaintGreen',(.58,.66,.64),.60,0),
 ('PlinthGrey','TownStone',(.58,.58,.55),.90,0),('PlinthDark','TownStone',(.24,.20,.21),.90,0),('PlinthBrown','TownStone',(.22,.13,.11),.90,0),
 ('PlinthBlue','TownStone',(.42,.44,.47),.90,0),('Passage','TownIvory',(.86,.85,.80),.90,0),
 ('Tile','TownTileRed',(.72,.40,.28),.80,0),('Brick','TownTileRed',(.62,.30,.22),.85,0),
 ('Dark','TownMetalGrey',(.06,.06,.065),.40,.20),('Iron','TownMetalGrey',(.10,.10,.11),.45,.40),
 ]:
 name='M_Block92_'+key;B92[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block92_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B92;TR=M['Trim']

def b92_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block92_names.append(name);return Mesh(name,category)
def drop_degenerate_faces92(obj,tol=1e-9):
 # The FBX export (tangent frames) fails on zero-area faces, faces with a repeated corner and thin
 # slivers.
 import bmesh
 bm=bmesh.new();bm.from_mesh(obj.data)
 def _thin(f):
  L=max(e.calc_length() for e in f.edges);return L>0 and 2*f.calc_area()/L<1e-4
 bad=[f for f in bm.faces if f.calc_area()<tol or len({v.index for v in f.verts})<len(f.verts) or _thin(f)]
 if bad:bmesh.ops.delete(bm,geom=bad,context='FACES_ONLY')
 bm.to_mesh(obj.data);bm.free();obj.data.update();return len(bad)
def b92_finish(m,osm):
 obj=s21_finish(m);n=drop_degenerate_faces92(obj)
 if n:print('BLOCK92_DROPPED_DEGENERATE',m.name,n)
 obj['detail_pass']=92;obj['reference_notes']='references/block92-notes.md';obj['osm_way']=osm;return obj
def P92(a,b,s):L=math.dist(a,b);return (a[0]+(b[0]-a[0])*s/L,a[1]+(b[1]-a[1])*s/L)
def gable92(m,w,prof,ma,o0=.005,o1=.355):
 # A solid gable on a wall: prof is a convex, counter-clockwise outline (u, z) in the wall's frame.
 x,y,L,a=sf_edge(w['p'],w['q']);n=len(prof);vs=[lp(x,y,uu,o,zz,a) for o in (o0,o1) for uu,zz in prof]
 m.faces(vs,[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,n+(i+1)%n,n+i) for i in range(n)],ma)
def tri92(w,H,T):x,y,L,a=sf_edge(w['p'],w['q']);return [(-L/2,H),(L/2,H),(0,T)]
def barge92(m,w,prof,ma,o=.62,r=.08):
 x,y,L,a=sf_edge(w['p'],w['q']);top=prof[1:]+prof[:1]
 town_path(m,[lp(x,y,uu,o,zz+.03,a) for uu,zz in prof[1:]+prof[:1]],r,ma)
def win92(m,x,y,u,b,w,h,a,frame,sash=None,face=False,sur=True):
 o=.40 if face else .16
 cas81(m,x,y,u,b,w,h,a,sash or frame,o,3 if h>1.2 else 2)
 if sur:surround36(m,x,y,u,b,w,h,a,frame,.10,.42 if face else .40)
 facade_box(m,x,y,u,.47,b-.05,w+.26,.16,.06,frame,a)
def front92(m,w,H,ops,wm,boarded=True,plinth=.30,pm=None,z0=0):
 # A street front: the wall with its openings cut, vertical boards, the plinth with gaps at low
 # doors. ops: (kind, X, Y, bottom, w, h) with (X, Y) the opening's centre on the facade line.
 p,q=w['p'],w['q'];x,y,L,a=sf_edge(p,q);mine=[]
 for k,X,Y,b,ww,hh in ops:
  u=U(w,X,Y);off=abs((X-x)*math.sin(a)-(Y-y)*math.cos(a))
  if off<.8 and abs(u)<=L/2:mine.append((k,u,b,ww,hh))
 holes=[(u,b,ww,min(hh,H-b),0) for k,u,b,ww,hh in mine if b<H-.2 and b+hh<=H+.01]
 bz_wall(m,p,q,z0,H,holes,wm)
 if boarded:boards81(m,x,y,L,a,plinth+.05,H-.12,holes,wm)
 if plinth>0:
  at=-L/2
  for lo,hi in sorted((u-ww/2,u+ww/2) for u,b,ww,hh,r in holes if b<plinth)+[(L/2,L/2)]:
   if lo>at+.03:facade_box(m,x,y,(at+lo)/2,.40,plinth/2,lo-at,.10,plinth,pm or M['PlinthGrey'],a)
   at=max(at,hi)
 return x,y,L,a,mine
def corners92(m,x,y,L,a,z0,z1,ma,bw=.18):
 for uu in (-L/2+bw/2,L/2-bw/2):facade_box(m,x,y,uu,.42,(z0+z1)/2,bw,.10,z1-z0,ma,a)
def eaves92(m,x,y,L,a,H,ma,gutter=True):
 facade_box(m,x,y,0,.44,H-.10,L+.08,.14,.20,ma,a)
 if gutter:town_rod(m,lp(x,y,-L/2,.66,H-.04,a),lp(x,y,L/2,.66,H-.04,a),.06,M['Dark'],8)
def chimney92(m,X,Y,z0,z1,ma,w=.55):box(m,X,Y,w,w,z1-z0,z0,ma,0,M['Dark'])
def flat92(m,zone,z,ma):
 for g in Z[zone]['polygons']:m.faces([(*v,z) for v in g],[tuple(range(len(g))),tuple(range(len(g)-1,-1,-1))],ma)
def lean92(m,zone,a,b,lo,hi,ma,ov=.30):
 # A mono-pitch roof over the zone's box in the frame of front a->b: height hi along the side at
 # t=min (the a->b side), lo at the far side.
 r,Ls,Lt=rect82(zone,a,b);d,n=frame82(a,b);p0,p1,p2,p3=r
 sh=lambda p,s,t:(p[0]+d[0]*s+n[0]*t,p[1]+d[1]*s+n[1]*t)
 k=(hi-lo)/Lt
 vs=[(*sh(p0,-ov,-ov),hi+ov*k),(*sh(p1,ov,-ov),hi+ov*k),(*sh(p2,ov,ov),lo-ov*k),(*sh(p3,-ov,ov),lo-ov*k)]
 m.faces(vs,[(0,1,2,3),(3,2,1,0)],ma)
def gambrel92(m,zone,a,b,ma,wall,bk,ov=.25,verge=.15):
 # Gambrel roof with its ridge across the front a->b: walls to 'height', a steep lower slope to
 # 'brk' bk metres in from each side wall, a shallow upper slope to 'top'. Gable outlines are
 # returned in each end wall's frame by gprof92.
 r,Ls,Lt=rect82(zone,a,b);d,n=frame82(a,b);p0=r[0];H=Z[zone]['height'];T=Z[zone]['top'];Bz=Z[zone]['brk']
 k1=(Bz-H)/bk
 prof=[(-ov,H-ov*k1),(bk,Bz),(Ls/2,T),(Ls-bk,Bz),(Ls+ov,H-ov*k1)]
 P=lambda s,t,z:(p0[0]+d[0]*s+n[0]*t,p0[1]+d[1]*s+n[1]*t,z)
 for (s0,z0),(s1,z1) in zip(prof,prof[1:]):
  vs=[P(s0,-verge,z0),P(s1,-verge,z1),P(s1,Lt+verge,z1),P(s0,Lt+verge,z0)]
  m.faces(vs,[(0,1,2,3),(3,2,1,0)],ma)
 return Ls,Lt
def gprof92(w,H,Bz,T,bk):
 x,y,L,a=sf_edge(w['p'],w['q']);return [(-L/2,H),(L/2,H),(L/2-bk,Bz),(0,T),(-L/2+bk,Bz)]

meshes={}
for zone,spec in Z.items():
 nm=spec['mesh']
 if nm not in meshes:meshes[nm]=b92_new(nm,'Kvarnholmen/Landshövdingegatan')

# ---- 93192387: the olive corner house. Storgatan front x 282.74-294.91 (65 Storgatan panorama,
# camera 289.64,-5.44, 2.44 m); east gable y 0.07-7.5 (9 Landshövdingegatan panorama).
m=meshes['SM_Kvarnholmen_House_93192387'];H=Z['og']['height'];T=Z['og']['top']
OS=[('dbl',284.6,0,.34,1.30,2.04)]+[('win',X,0,1.25,1.12,1.35) for X in (286.35,288.7,291.15,293.05)]+[('win',X,0,3.40,1.12,1.45) for X in (284.5,286.35,288.65,291.15,293.0)]
OE=[('win',295.0,y_,1.25,1.0,1.35) for y_ in (2.0,5.6)]+[('win',295.0,y_,3.40,1.0,1.40) for y_ in (2.0,5.6)]+[('att',295.0,y_,6.25,.62,.95) for y_ in (3.25,4.35)]
for w in walls('og'):
 ox,oy=outward(w);x,y,L,a=sf_edge(w['p'],w['q'])
 if w['kind']!='outer':
  bz_wall(m,w['p'],w['q'],w['z0'],H,[],M['Olive'])
  if ox<-.85:gable92(m,w,tri92(w,H,T),M['Olive']);barge92(m,w,tri92(w,H,T),TR,o=.50)
  continue
 if oy<-.85:
  x,y,L,a,mine=front92(m,w,H,OS,M['Olive'],plinth=.45)
  for k,u,b,ww,hh in mine:
   if k=='win':win92(m,x,y,u,b,ww,hh,a,TR,M['Olive'])
   else:
    # The carved double door: white leaves with grilles above, fluted pilasters and a cornice.
    gate83(m,x,y,u,b,ww,hh,a,M['Cream'],TR)
    for s in (-1,1):
     facade_box(m,x,y,u+s*ww/4,.20,b+hh*.70,ww/2-.22,.02,hh*.38,M['Dark'],a)
     facade_box(m,x,y,u+s*(ww/2+.16),.46,b+hh/2+.05,.22,.12,hh+.1,TR,a)
    facade_box(m,x,y,u,.50,b+hh+.20,ww+.60,.16,.30,TR,a);facade_box(m,x,y,u,.56,b+hh+.40,ww+.75,.24,.08,TR,a)
    steps82(m,x,y,u,ww+.3,b,a,M['PlinthGrey'])
  corners92(m,x,y,L,a,0,H,TR,.20);eaves92(m,x,y,L,a,H,TR)
 elif ox>.85:
  x,y,L,a,mine=front92(m,w,H,[o for o in OE if o[0]!='att'],M['Olive'],plinth=.45)
  for k,u,b,ww,hh in mine:win92(m,x,y,u,b,ww,hh,a,TR,M['Olive'])
  for k,X,Y,b,ww,hh in OE:
   if k=='att':win92(m,x,y,U(w,X,Y),b,ww,hh,a,TR,M['Olive'],face=True)
  gable92(m,w,tri92(w,H,T),M['Olive']);barge92(m,w,tri92(w,H,T),TR)
  corners92(m,x,y,L,a,0,H,TR,.20)
 else:plain(m,w,H,M['Olive'],TR,TR,2,.9)
saddle82(m,'og',(282.74,0.254),(294.914,0.075),M['Tile'],M['Olive'],along=True,ov=.40)
chimney92(m,285.4,2.9,T-1.2,9.1,M['Brick'],.60);chimney92(m,291.8,3.1,T-1.0,8.9,M['PlinthBlue'],.55)
# The low strip behind (y 7.5-9.7): the side door on steps and a small window on the street.
H2=Z['or']['height']
for w in walls('or'):
 ox,oy=outward(w)
 if w['kind']!='outer':bz_wall(m,w['p'],w['q'],w['z0'],H2,[],M['Olive']);continue
 if ox>.85:
  x,y,L,a,mine=front92(m,w,H2,[('door',295.05,8.84,.55,1.10,2.05),('win',295.05,8.55,4.30,.45,.55)],M['Olive'],plinth=.45)
  for k,u,b,ww,hh in mine:
   if k=='win':win92(m,x,y,u,b,ww,hh,a,TR,M['Olive'])
   else:door83(m,x,y,u,b,ww,hh,a,M['Brown'],TR);steps82(m,x,y,u,ww+.5,b,a,M['PlinthGrey'])
  corners92(m,x,y,L,a,0,H2,TR,.16);eaves92(m,x,y,L,a,H2,TR,False)
 else:plain(m,w,H2,M['Olive'],TR,TR,1,.9)
lean92(m,'or',(282.74,7.5),(295.02,7.5),H2,Z['or']['top'],M['Tile'])
# The gate section west of the house (x 280.19-282.74): pale green boarded gate leaves to 2.1 m,
# a grey beam, a yellow boarded panel above to 3.6 m; flat roof behind.
H3=Z['gt']['height']
for w in walls('gt'):
 ox,oy=outward(w)
 if oy<-.85:
  x,y,L,a=sf_edge(w['p'],w['q']);u=U(w,281.4,0.27)
  bz_wall(m,w['p'],w['q'],0,H3,[(u,0,2.2,2.1,0)],M['Yellow'])
  boards81(m,x,y,L,a,2.45,H3-.1,[],M['Yellow'])
  for s in (-1,1):facade_box(m,x,y,u+s*.55,.14,1.05,1.08,.08,2.1,M['GatePale'],a)
  boards81(m,x,y,2.2,a,.05,2.05,[],M['GatePale'])
  facade_box(m,x,y,u,.40,2.24,L,.12,.28,M['PlinthGrey'],a);facade_box(m,x,y,0,.42,H3-.06,L,.12,.12,M['Yellow'],a)
 else:bz_wall(m,w['p'],w['q'],0,H3,[],M['Yellow'])
flat92(m,'gt',H3+.02,M['Dark'])
b92_finish(m,'93192387')

# ---- 93192432: the ochre rendered house (9 Landshövdingegatan panorama, camera 300.18,14.28,
# 2.3 m). Street front y 9.69-19.29, gambrel gable to the street.
m=meshes['SM_Kvarnholmen_House_93192432'];zs=Z['oc'];H=zs['height'];T=zs['top'];BZ=zs['brk'];BK=1.1
OO=[('gate',295.1,11.39,.05,1.55,2.50)]+[('win',295.1,y_,1.20,1.02,1.36) for y_ in (13.22,15.58,17.67)]+[('win',295.1,y_,3.70,1.0,1.62) for y_ in (11.39,13.23,15.55,17.6)]+[('att',295.1,y_,6.72,1.0,1.03) for y_ in (13.22,15.6)]
for w in walls('oc'):
 ox,oy=outward(w);x,y,L,a=sf_edge(w['p'],w['q'])
 if w['kind']!='outer':bz_wall(m,w['p'],w['q'],w['z0'],H,[],M['Ochre']);continue
 if ox>.85:
  x,y,L,a,mine=front92(m,w,H,[o for o in OO if o[0]!='att'],M['Ochre'],boarded=False,plinth=.62,pm=M['PlinthBrown'])
  for k,u,b,ww,hh in mine:
   if k=='win':win92(m,x,y,u,b,ww,hh,a,M['Brown'],sur=False)
   else:
    gate83(m,x,y,u,b,ww,hh,a,M['DoorRed'],M['Brown']);facade_box(m,x,y,u,.42,b+hh+.08,ww+.25,.10,.16,M['Brown'],a)
  for k,X,Y,b,ww,hh in OO:
   if k=='att':win92(m,x,y,U(w,X,Y),b,ww,hh,a,M['Brown'],face=True,sur=False)
  prof=gprof92(w,H,BZ,T,BK);gable92(m,w,prof,M['Ochre']);barge92(m,w,prof,M['Brown'],o=.45,r=.07)
  # White corner pilasters on dark brown bases.
  for s in (-1,1):
   facade_box(m,x,y,s*(L/2-.32),.45,(.62+H)/2,.60,.14,H-.62,TR,a);facade_box(m,x,y,s*(L/2-.32),.45,.31,.68,.16,.62,M['PlinthBrown'],a)
   facade_box(m,x,y,s*(L/2-.32),.50,H-.12,.74,.20,.24,TR,a)
 else:
  plain(m,w,H,M['Ochre'],TR,TR,2,.9)
# The back gable over the whole west wall (its north part stands above the neighbour's 6.65 m).
gw={'p':[285.61,19.43],'q':[285.458,9.835]};gable92(m,gw,gprof92(gw,H,BZ,T,BK),M['Ochre'])
gambrel92(m,'oc',(295.051,9.69),(295.199,19.287),M['Tile'],M['Ochre'],BK)
chimney92(m,290.2,16.9,BZ-.5,T+.9,M['PlinthBlue'],.55)
b92_finish(m,'93192432')

# ---- 93192395: the stucco house (12 Landshövdingegatan panorama, camera 300.48,25.23, 2.4 m).
# Street front y 19.29-29.49.
m=meshes['SM_Kvarnholmen_House_93192395'];H=Z['pk']['height'];T=Z['pk']['top']
SPR,ARW,ARR=2.45,2.60,1.15
OP=[('arch',295.3,21.1,0,ARW,SPR+ARR+.25)]+[('win',295.3,y_,1.65,1.10,2.0) for y_ in (24.7,28.15)]+[('cel',295.3,y_,.08,.78,.62) for y_ in (24.7,28.15)]+\
 [('win',295.3,y_,z_,1.12,1.90) for y_ in (21.0,24.7,28.2) for z_ in (4.85,8.0)]
for w in walls('pk'):
 ox,oy=outward(w);x,y,L,a=sf_edge(w['p'],w['q'])
 if w['kind']!='outer':bz_wall(m,w['p'],w['q'],w['z0'],H,[],M['StuccoUp']);continue
 if ox>.85:
  p,q=w['p'],w['q'];mine=[(k,U(w,X,Y),b,ww,hh) for k,X,Y,b,ww,hh in OP]
  holes=[(u,b,ww,hh,0) for k,u,b,ww,hh in mine]
  # Two-tone render: brown-pink to the band at 4.4 m, beige-pink above.
  bz_wall(m,p,q,0,4.42,[hh for hh in holes if hh[1]<4.42],M['StuccoLow'])
  bz_wall(m,p,q,4.42,H,[hh for hh in holes if hh[1]>=4.42],M['StuccoUp'])
  at=-L/2
  for u,b,ww,hh,r in sorted(hh for hh in holes if hh[1]<.1)+[(L/2+ .0,0,0,0,0)]:
   lo=u-ww/2
   if lo>at+.03:facade_box(m,x,y,(at+lo)/2,.40,.36,lo-at,.10,.72,M['PlinthBlue'],a)
   at=max(at,u+ww/2)
  facade_box(m,x,y,0,.42,4.42,L,.10,.14,M['StuccoUp'],a)
  for k,u,b,ww,hh in mine:
   if k=='win':
    win92(m,x,y,u,b,ww,hh,a,TR)
    if b<4:
     # Round-headed surround over the ground-floor windows.
     town_path(m,[lp(x,y,u+(ww/2+.08)*math.cos(math.pi*i/12),.42,b+hh+.02+.32*math.sin(math.pi*i/12),a) for i in range(13)],.07,TR)
    else:facade_box(m,x,y,u,.44,b+hh+.20,ww+.30,.10,.14,TR,a)
   elif k=='cel':
    facade_box(m,x,y,u,.12,b+hh/2,ww,.04,hh,M['PlinthBlue'],a);facade_box(m,x,y,u,.18,b+hh/2,ww-.12,.02,hh-.12,GLAZE,a)
    for s in (-1,1):facade_box(m,x,y,u,.18,b+hh/2+s*hh/6,ww-.12,.03,.03,M['Iron'],a)
   else:
    # The arched gateway: the arch fill above the springing, a white archivolt and jambs, the
    # passage (white walls and vault) and the yard gate seen at its far end.
    top=b+hh;k_=16
    arc=[(u+ww/2*math.cos(math.pi*i/k_),SPR+ARR*math.sin(math.pi*i/k_)) for i in range(k_+1)][::-1]
    for (u0,z0),(u1,z1) in zip(arc,arc[1:]):
     for o,rev in ((.355,False),(.005,True)):
      f=[lp(x,y,u0,o,z0,a),lp(x,y,u1,o,z1,a),lp(x,y,u1,o,top,a),lp(x,y,u0,o,top,a)]
      m.faces(f,[(3,2,1,0) if rev else (0,1,2,3)],M['StuccoLow'])
    town_path(m,[lp(x,y,uu,.40,zz,a) for uu,zz in [(u-ww/2-.08,0)]+[(u+(ww/2+.08)*math.cos(math.pi*i/k_),SPR+(ARR+.08)*math.sin(math.pi*i/k_)) for i in range(k_,-1,-1)]+[(u+ww/2+.08,0)]],.10,TR)
    for s in (-1,1):facade_box(m,x,y,u+s*(ww/2+.05),-2.4,(SPR+ARR)/2,.10,5.5,SPR+ARR,M['Passage'],a)
    facade_box(m,x,y,u,-2.4,SPR+ARR+.05,ww+.2,5.5,.10,M['Passage'],a)
    facade_box(m,x,y,u,-5.2,1.1,ww,.06,2.2,M['GatePale'],a);facade_box(m,x,y,u,-5.2,.4,ww,.07,.8,M['PlinthDark'],a)
    facade_box(m,x,y,u,-2.4,.01,ww,5.5,.02,M['PlinthGrey'],a)
  # Wall anchors between the upper windows, and the cornice.
  for yy in (22.85,26.45):
   uu=U(w,295.3,yy);facade_box(m,x,y,uu,.40,7.4,.06,.05,.50,M['Iron'],a);facade_box(m,x,y,uu,.40,7.45,.32,.05,.06,M['Iron'],a)
  facade_box(m,x,y,0,.47,H-.15,L+.1,.24,.30,TR,a);town_rod(m,lp(x,y,-L/2,.70,H-.02,a),lp(x,y,L/2,.70,H-.02,a),.07,M['Dark'],8)
 else:plain(m,w,H,M['StuccoUp'],TR,TR,3,.9)
saddle82(m,'pk',(295.199,19.287),(295.345,29.49),M['Tile'],M['StuccoUp'],along=True,ov=.40)
chimney92(m,290.4,29.0,T-1.5,T+1.6,M['StuccoUp'],.80)
b92_finish(m,'93192395')

# ---- 93192444: the red boarded house (gable to the street, y 32.65-39.11) and the carved gate in
# the gap south of it (y 29.49-32.65, outside the OSM outlines), whose wall top follows the house's
# south roof slope down to 3.9 m.
m=meshes['SM_Kvarnholmen_House_93192444'];H=Z['rf']['height'];T=Z['rf']['top']
OR=[('win',295.0,y_,1.85,.95,1.40) for y_ in (34.9,36.9)]+[('up',295.0,y_,4.10,.95,1.35) for y_ in (34.9,36.9)]
for w in walls('rf'):
 ox,oy=outward(w);x,y,L,a=sf_edge(w['p'],w['q'])
 if w['kind']!='outer':bz_wall(m,w['p'],w['q'],w['z0'],H,[],M['Red']);continue
 if ox>.85:
  x,y,L,a,mine=front92(m,w,H,[o for o in OR if o[0]=='win'],M['Red'],plinth=.30)
  for k,u,b,ww,hh in mine:win92(m,x,y,u,b,ww,hh,a,M['Frame92'],sur=True)
  for k,X,Y,b,ww,hh in OR:
   if k=='up':win92(m,x,y,U(w,X,Y),b,ww,hh,a,M['Frame92'],face=True)
  gable92(m,w,tri92(w,H,T),M['Red']);barge92(m,w,tri92(w,H,T),M['Red'],o=.55,r=.09)
  corners92(m,x,y,L,a,0,H,M['Red'],.16)
 else:
  if math.dist(w['p'],w['q'])<1.0:bz_wall(m,w['p'],w['q'],0,H,[],M['Red'])
  else:plain(m,w,H,M['Red'],M['Frame92'],M['Red'],1,.9)
gw={'p':[283.0,39.369],'q':[283.0,32.645]};gable92(m,gw,tri92(gw,H,T),M['Red'])
saddle82(m,'rf',(294.927,32.645),(295.075,39.108),M['Tile'],M['Red'],along=False,ov=.35)
chimney92(m,290.0,36.2,T-.6,T+.9,M['Brick'],.55)
H4=Z['rb']['height']
for w in walls('rb'):plain(m,w,H4,M['Red'],M['Frame92'],M['Red'],1,.9)
saddle82(m,'rb',(283.0,32.914),(283.0,36.971),M['Tile'],M['Red'],along=False,ov=.30)
# The gate: red boarded wall, the carved double gate (orange-brown leaves with raised panels and
# lozenges) under a red lintel panel, the sloping wall top and the roof slope over the passage.
GP,GQ=(295.345,29.49),(294.927,32.645);gw={'p':list(GP),'q':list(GQ)};x,y,L,a=sf_edge(GP,GQ);u=U(gw,295.15,30.95)
k_=(H-3.9)/L
bz_wall(m,GP,GQ,0,3.9,[(u,0,2.75,2.75,0)],M['Red']);boards81(m,x,y,L,a,2.85,3.85,[],M['Red'])
gable92(m,gw,[(-L/2,3.9),(L/2,3.9),(L/2,H)],M['Red'])
gate83(m,x,y,u,0,2.75,2.15,a,M['GateWood'],M['DoorRed'])
facade_box(m,x,y,u,.16,2.45,2.75,.07,.60,M['DoorRed'],a);facade_box(m,x,y,u,.20,2.45,2.2,.03,.38,M['GateWood'],a)
for du in (-.92,0,.92):
 diamond83(m,x,y,u+du,1.78,.17,a,M['DoorRed'])
 for zz in (.95,.42):facade_box(m,x,y,u+du,.18,zz,.62,.04,.36,M['DoorRed'],a)
facade_box(m,x,y,u,.42,2.80,3.05,.12,.12,M['DoorRed'],a)
for s in (-1,1):facade_box(m,x,y,u+s*1.47,.40,1.40,.16,.10,2.80,M['DoorRed'],a)
D_=frame82(GP,GQ)[1];ov=.35
EL=lambda s,t,z:(GP[0]+(GQ[0]-GP[0])*s/L+D_[0]*t,GP[1]+(GQ[1]-GP[1])*s/L+D_[1]*t,z)
m.faces([EL(-.05,-ov,3.9-ov*0),EL(L,-ov,H),EL(L,2.4,H),EL(-.05,2.4,3.9)],[(0,1,2,3),(3,2,1,0)],M['Tile'])
b92_finish(m,'93192444')

# ---- 93192382: the pink boarded house (16 Landshövdingegatan panorama, camera 300.82,46.92,
# 2.43 m). Street front y 39.11-49.25.
m=meshes['SM_Kvarnholmen_House_93192382'];H=Z['pb']['height'];T=Z['pb']['top']
OB=[('win',295.2,y_,1.66,1.05,1.45) for y_ in (40.9,42.43,45.43)]+[('win',295.2,y_,4.31,1.05,1.40) for y_ in (40.95,42.46,45.4,47.57)]+\
 [('dbl',295.2,48.3,0,1.62,2.30),('hatch',295.2,45.45,.02,.65,.70)]
for w in walls('pb'):
 ox,oy=outward(w);x,y,L,a=sf_edge(w['p'],w['q'])
 if w['kind']!='outer':bz_wall(m,w['p'],w['q'],w['z0'],H,[],M['Pink']);continue
 if ox>.85:
  x,y,L,a,mine=front92(m,w,H,[o for o in OB if o[0]!='hatch'],M['Pink'],plinth=.76,pm=M['PlinthDark'])
  for k,u,b,ww,hh in mine:
   if k=='win':win92(m,x,y,u,b,ww,hh,a,M['PinkTrim'],M['Cream'])
   else:
    gate83(m,x,y,u,b,ww,hh,a,M['GreyGreen'],M['Cream'])
    for s in (-1,1):
     for zz,hz in ((.55,.75),(1.55,.95)):facade_box(m,x,y,u+s*ww/4,.17,zz,ww/2-.34,.03,hz,M['Cream'],a)
    facade_box(m,x,y,u,.36,b+hh+.13,ww,.04,.22,GLAZE,a);facade_box(m,x,y,u,.40,b+hh+.27,ww+.1,.08,.06,M['Cream'],a)
    facade_box(m,x,y,u,.40,b+hh+.62,ww+.1,.10,.62,M['PinkTrim'],a);facade_box(m,x,y,u,.46,b+hh+1.0,ww+.3,.16,.12,M['Cream'],a)
    for s in (-1,1):facade_box(m,x,y,u+s*(ww/2+.10),.42,(b+hh+1.0)/2,.18,.10,b+hh+1.0,M['Cream'],a)
  for k,X,Y,b,ww,hh in OB:
   if k=='hatch':facade_box(m,x,y,U(w,X,Y),.46,b+hh/2,ww,.06,hh,M['Brown'],a)
  # Pilaster boards: the corners and two between the bays.
  for yy in (41.66,43.55):facade_box(m,x,y,U(w,295.2,yy),.44,(.76+H)/2,.22,.10,H-.76,M['PinkTrim'],a)
  corners92(m,x,y,L,a,.76,H,M['PinkTrim'],.22)
  facade_box(m,x,y,0,.44,.80,L,.12,.08,M['PinkTrim'],a);eaves92(m,x,y,L,a,H,M['PinkTrim'])
 else:plain(m,w,H,M['Pink'],M['PinkTrim'],M['PinkTrim'],2,.9)
saddle82(m,'pb',(295.075,39.108),(295.292,49.249),M['Tile'],M['Pink'],along=True,ov=.45)
chimney92(m,291.6,43.5,T-.8,12.0,M['Brick'],.60)
H5=Z['pw']['height']
for w in walls('pw'):plain(m,w,H5,M['Pink'],M['PinkTrim'],M['PinkTrim'],1,.9)
lean92(m,'pw',(287.36,39.28),(287.36,45.778),H5,Z['pw']['top'],M['Tile'])
b92_finish(m,'93192382')

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block92_cameras=[
 sv_camera('451_Block92_Cal_Corner',289.64,-5.44,2.44,332,15,90),
 sv_camera('452_Block92_Cal_Ochre',300.18,14.28,2.30,242,15,90),
 sv_camera('453_Block92_Cal_Stucco',300.48,25.23,2.40,242,15,90),
 sv_camera('454_Block92_Cal_Pink',300.82,46.92,2.43,242,15,90),
 ('455_Block92_Aerial',(318.0,24.0,30.0),(289.0,24.0,4.0),28),
]
print('BLOCK92_GEOMETRY',len(block92_names))
