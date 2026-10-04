"""Pass 94: the south side of Fiskaregatan east of Östra Sjögatan, four fronts facing north onto the
narrow street:
- the grey rendered office (91885523): a semi-basement, two ribbon-window storeys with dark green
  mullions, a steep tiled roof with four gabled dormers, and a recessed two-storey entrance bay with a
  ribbed dark panel and a canopy at its west end;
- the white flat-roofed modernist block (91926303): nine tall window columns with brown boarded
  spandrel panels and copper sills on two storeys over a row of semi-basement windows;
- the pale blue-green boarded gable house (91926337): two windows below and one in the gable, white
  double bargeboards, a dark plinth, and a low rear wing;
- the red boarded gable house (91926333): two pairs of windows in grey surrounds with yellow sashes,
  grey bargeboards, and the lower part west of and behind it.

References: Google Street View April 2025 (three panoramas on Fiskaregatan, resected), view only.
Zones: source/block94.json; see references/block94-notes.md. Signs, the air-conditioning unit's
pipework, lamps, downpipes and the aerial are omitted.
"""
B94D=json.loads((R/'source/block94.json').read_text());Z=B94D['zones']
block94_names=[];B94={}
for old in [k for k in list(materials) if k.startswith('M_Block94_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Grey','TownStone',(.56,.55,.52),.92,0),('GreyLight','TownStone',(.66,.65,.62),.90,0),('Mullion','TownMetalGrey',(.16,.23,.20),.50,.20),
 ('WhiteFrame','TownPaintWhite',(.93,.93,.91),.55,0),('Roof','TownTileRed',(.34,.28,.27),.80,0),('Ribbed','TownMetalGrey',(.22,.24,.23),.55,.30),
 ('White','TownIvory',(.87,.87,.85),.88,0),('Panel','TownPaintBrown',(.29,.21,.17),.70,0),('DarkFrame','TownMetalGrey',(.11,.11,.11),.45,.30),
 ('Copper','TownPaintGreen',(.38,.53,.49),.55,.20),('Coping','TownMetalGrey',(.19,.20,.21),.50,.30),('FlatRoof','TownMetalGrey',(.17,.17,.18),.80,.10),
 ('Aqua','TownPaintWhite',(.62,.82,.78),.80,0),('Sash','TownPaintGreen',(.22,.38,.22),.60,0),('Plinth','TownStone',(.34,.35,.35),.90,0),
 ('Red','TownPaintBrown',(.50,.18,.18),.80,0),('GreyTrim','TownPaintWhite',(.68,.72,.73),.60,0),('Yellow','TownIvory',(.85,.75,.45),.60,0),
 ('Barge','TownMetalGrey',(.43,.47,.46),.60,.10),('Tile','TownTileRed',(.70,.38,.27),.80,0),
 ]:
 name='M_Block94_'+key;B94[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block94_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B94

def b94_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block94_names.append(name);return Mesh(name,category)
def drop_degenerate_faces94(obj,tol=1e-9):
 # Faces with no area, a repeated corner or a sliver thinner than 0.1 mm have no UV frame, which
 # the tangent export rejects; they draw nothing, so they are removed.
 import bmesh
 bm=bmesh.new();bm.from_mesh(obj.data)
 def _thin(f):
  L=max(e.calc_length() for e in f.edges);return L>0 and 2*f.calc_area()/L<1e-4
 bad=[f for f in bm.faces if f.calc_area()<tol or len({v.index for v in f.verts})<len(f.verts) or _thin(f)]
 if bad:bmesh.ops.delete(bm,geom=bad,context='FACES_ONLY')
 bm.to_mesh(obj.data);bm.free();obj.data.update();return len(bad)
def b94_finish(m,osm):
 obj=s21_finish(m);drop_degenerate_faces94(obj);obj['detail_pass']=94;obj['reference_notes']='references/block94-notes.md';obj['osm_way']=osm;return obj

def P94(a,b,s,t=0):
 # The point s metres from a towards b, t metres to the left of a->b (inwards on these fronts).
 L=math.dist(a,b);d=((b[0]-a[0])/L,(b[1]-a[1])/L);return (a[0]+d[0]*s-d[1]*t,a[1]+d[1]*s+d[0]*t)
def front94(zone):
 # The zone's street front: its longest outer wall facing north (outward y > 0.85).
 ws=[w for w in walls(zone) if w['kind']=='outer' and outward(w)[1]>.85]
 return max(ws,key=lambda w:math.dist(w['p'],w['q'])) if ws else None
def win94(m,x,y,u,b,w,h,a,sash,trim,rows=3,bw=.11,o=.16):
 # Windows reaching into a solid gable are drawn on its face (o 0.40).
 cas81(m,x,y,u,b,w,h,a,sash,o,rows);surround36(m,x,y,u,b,w,h,a,trim,bw,.40 if o<.3 else .44)
 facade_box(m,x,y,u,.47,b-.05,w+2*bw+.06,.16,.07,trim,a);facade_box(m,x,y,u,.45,b+h+bw+.04,w+2*bw+.10,.12,.08,trim,a)
def vboards94(m,x,y,u0,u1,a,z0,top,holes,ma,step=.22):
 # Vertical boards from z0 up to top(u) (a function, for gables), broken round the holes.
 n=max(2,int((u1-u0)/step))
 for k in range(1,n):
  u=u0+k*(u1-u0)/n;segs=[(z0,top(u)-.06)]
  for hu,hb,hw,hh,hr in holes:
   if abs(u-hu)<hw/2+.12:segs=[(l0,h0) for l,h_ in segs for l0,h0 in ((l,min(h_,hb-.12)),(max(l,hb+hh+.12),h_)) if h0-l0>.05]
  for l0,h0 in segs:facade_box(m,x,y,u,.37,(l0+h0)/2,.04,.03,h0-l0,ma,a)
def gable94(m,x,y,L,a,H,T,ma):
 # A solid gable triangle over the whole wall, flush with the wall's thickness.
 prof=[(-L/2,H),(L/2,H),(0,T)];vs=[lp(x,y,uu,o,zz,a) for o in (.005,.355) for uu,zz in prof]
 m.faces(vs,[(2,1,0),(3,4,5),(0,1,4,3),(1,2,5,4),(2,0,3,5)],ma)
def saddle94(m,a,b,s0,s1,t1,H,T,ma,ov=.40,verge=.35,back=None):
 # Saddle roof with its ridge running back from the street front a->b (gable to the street), over
 # the box s0..s1 along the front and 0..t1 inwards, eaves pushed out by ov, verges by verge.
 sm=(s0+s1)/2;sl=(T-H)/((s1-s0)/2);ta,tb=-.355-verge,t1+verge
 Q=lambda s,t,z:(*P94(a,b,s,t),z)
 m.faces([Q(s0-ov,ta,H-ov*sl),Q(sm,ta,T),Q(sm,tb,T),Q(s0-ov,tb,H-ov*sl)],[(0,1,2,3),(3,2,1,0)],ma)
 m.faces([Q(sm,ta,T),Q(s1+ov,ta,H-ov*sl),Q(s1+ov,tb,H-ov*sl),Q(sm,tb,T)],[(0,1,2,3),(3,2,1,0)],ma)
 if back:m.faces([Q(s0,t1,H),Q(s1,t1,H),Q(sm,t1,T)],[(0,1,2),(2,1,0)],back)
 for s,z in ((s0-ov,H-ov*sl),(s1+ov,H-ov*sl)):town_rod(m,Q(s,ta,z-.04),Q(s,tb,z-.04),.06,M['Coping'],8)
 return sl,Q,ta
def flat94(m,zone,z,ma):
 for g in Z[zone]['polygons']:m.faces([(*v,z) for v in g],[tuple(range(len(g))),tuple(range(len(g)-1,-1,-1))],ma)
def dormer94(m,x,y,u,a,zb,w,ww,wh,depth,back,body,frame,roof):
 # A gabled dormer: its face 'back' metres behind the facade surface, the window in a white frame,
 # a steep little saddle lid with its gable to the street.
 fo=.355-back;zt=zb+.35+wh+.30
 facade_box(m,x,y,u,fo-depth/2,(zb+zt)/2,w,depth,zt-zb,body,a)
 facade_box(m,x,y,u,fo+.01,zb+.35+wh/2,ww,.02,wh,GLAZE,a);cas81(m,x,y,u,zb+.35,ww,wh,a,frame,fo+.05,2)
 e=w/2+.12;rise=.75;of,ob=fo+.18,fo-depth
 for s in (-1,1):m.faces([lp(x,y,u+s*e,of,zt-.05,a),lp(x,y,u,of,zt+rise,a),lp(x,y,u,ob,zt+rise,a),lp(x,y,u+s*e,ob,zt-.05,a)],[(0,1,2,3),(3,2,1,0)],roof)
 m.faces([lp(x,y,u-w/2,fo,zt,a),lp(x,y,u+w/2,fo,zt,a),lp(x,y,u,fo,zt+rise-.06,a)],[(0,1,2),(2,1,0)],body)

meshes={}
for zone,spec in Z.items():
 nm=spec['mesh']
 if nm not in meshes:meshes[nm]=b94_new(nm,'Kvarnholmen/Fiskaregatan')

# ---- 91885523: the grey office. Positions s are metres from the west corner (91.05, 124.08) along
# the front; heights from the resected panorama (camera 2.5 m, 3.6 m from the facade).
OA,OB=(91.053,124.075),(108.055,119.821)
REC=3.40;RDEP=1.20;RTOP=6.40
LOW=(1.55,1.66);UPP=(4.80,1.48);COLS=[3.75+.70+1.60*k for k in range(8)]
m=meshes['SM_Kvarnholmen_House_91885523'];H=Z['of']['height'];T=Z['of']['top']
fw=front94('of')
for w in walls('of'):
 if w['kind']!='outer':bz_wall(m,w['p'],w['q'],w['z0'],H,[],M['Grey']);continue
 if w is not fw:plain(m,w,H,M['Grey'],M['WhiteFrame'],M['WhiteFrame'],2,1.5);continue
 x,y,L,a=sf_edge(w['p'],w['q']);us=lambda s:U(w,*P94(OA,OB,s))
 r0,r1=us(3.65),us(16.45);uc=(r0+r1)/2;rw=abs(r1-r0)
 holes=[(uc,LOW[0],rw,LOW[1],0),(uc,UPP[0],rw,UPP[1],0),((us(0)+us(REC))/2,0,REC,RTOP,0)]
 bz_wall(m,w['p'],w['q'],0,H,holes,M['Grey'])
 # The semi-basement in a lighter, smoother render; the dark green sill band; the fascia's gutter.
 ub=(us(REC)+us(17.53))/2;Lb=17.53-REC
 facade_box(m,x,y,ub,.37,.74,Lb,.04,1.48,M['GreyLight'],a)
 for z0,hh in (LOW,UPP):
  facade_box(m,x,y,uc,.42,z0-.05,rw+.10,.14,.10,M['Mullion'],a)
  # The ribbon: dark green posts behind white-framed two-light windows.
  facade_box(m,x,y,uc,.20,z0+hh/2,rw,.04,hh,M['Mullion'],a)
  for s in COLS:cas81(m,x,y,us(s),z0+.02,1.40,hh-.04,a,M['WhiteFrame'],.30,1)
 facade_box(m,x,y,(us(0)+us(17.53))/2,.48,H+.12,L+.1,.22,.26,M['Coping'],a)
 # The recessed entrance bay at the west end: a ribbed dark panel over a window, a canopy, and a
 # glazed shop front at the ground.
 ur=(us(0)+us(REC))/2;bo=.355-RDEP
 facade_box(m,x,y,ur,bo-.05,RTOP/2,REC,.10,RTOP,M['Grey'],a)
 for s in (REC-.10,.10):facade_box(m,x,y,us(s),(bo+.355)/2,RTOP/2,.20,RDEP,RTOP,M['Grey'],a)
 facade_box(m,x,y,ur,(bo+.355)/2,RTOP+.05,REC,RDEP,.10,M['Grey'],a)
 facade_box(m,x,y,ur,bo+.02,5.35,REC-.4,.04,2.1,M['Ribbed'],a)
 for k in range(26):facade_box(m,x,y,us(.25+k*(REC-.5)/25),bo+.06,5.35,.04,.04,2.1,M['DarkFrame'],a)
 facade_box(m,x,y,ur,bo+.01,3.70,REC-.4,.02,1.1,GLAZE,a);cas81(m,x,y,ur,3.15,REC-.4,1.1,a,M['WhiteFrame'],bo+.05,1)
 box(m,*P94(OA,OB,REC-.75,bo+.20),.80,.30,.60,2.70,M['WhiteFrame'],math.atan2(OB[1]-OA[1],OB[0]-OA[0]))
 facade_box(m,x,y,ur,(bo+.40)/2,2.29,REC,RDEP+.05,.52,M['Ribbed'],a)
 facade_box(m,x,y,ur,bo+.01,1.0,REC-.4,.02,2.0,GLAZE,a);cas81(m,x,y,ur,0,REC-.4,2.0,a,M['DarkFrame'],bo+.05,1)
# The steep roof: a 52-degree slope from the eaves to a nearly flat top 2.4 m in (the top itself
# is not seen), and four gabled dormers on the street slope.
ring=[tuple(v) for v in Z['of']['polygons'][0]]
inset_roof(m,ring,H,2.4,T-H,M['Roof'],.35,top=M['Roof'])
x,y,L,a=sf_edge(fw['p'],fw['q'])
for s in (4.20,7.85,11.50,15.15):dormer94(m,x,y,U(fw,*P94(OA,OB,s)),a,7.60,2.10,1.50,1.50,2.0,.60,M['Grey'],M['WhiteFrame'],M['Roof'])

# ---- 91926303: the white modernist block. s from the west corner (108.06, 119.82); camera 2.6 m.
MA,MB=(108.055,119.821),(122.662,115.993)
MCOLS=[13.13-1.45*k for k in range(9)];CW=1.00
m=meshes['SM_Kvarnholmen_House_91926303'];H=Z['mo']['height']
fw=front94('mo')
for w in walls('mo'):
 if w['kind']!='outer':bz_wall(m,w['p'],w['q'],w['z0'],H,[],M['White']);continue
 x,y,L,a=sf_edge(w['p'],w['q'])
 if w is not fw:
  plain(m,w,H-.35,M['White'],M['DarkFrame'],M['White'],2,1.5);bz_wall(m,w['p'],w['q'],H-.35,H,[],M['White'])
  facade_box(m,x,y,0,.42,H-.17,L+.1,.16,.36,M['Coping'],a);continue
 us=lambda s:U(w,*P94(MA,MB,s))
 rows=[(1.28,2.55,4.16),(4.92,6.12,7.78)]
 holes=[(us(s),b,CW,top-b,0) for s in MCOLS for b,g,top in rows]+[(us(s),.10,CW,.50,0) for s in MCOLS]
 bz_wall(m,w['p'],w['q'],0,H,holes,M['White'])
 for s in MCOLS:
  u=us(s)
  for b,g,top in rows:
   # Brown boarded spandrel below, the glazing above, all set back in a dark frame; copper sill.
   facade_box(m,x,y,u,.22,(b+g)/2,CW-.08,.04,g-b,M['Panel'],a)
   for k in range(1,6):facade_box(m,x,y,u-CW/2+.04+k*(CW-.08)/6,.25,(b+g)/2,.025,.02,g-b-.04,M['DarkFrame'],a)
   facade_box(m,x,y,u,.22,(g+top)/2,CW-.08,.02,top-g,GLAZE,a)
   for dz,hh in ((g,.06),(top-.03,.06),((g+top)/2+.25,.05)):facade_box(m,x,y,u,.25,dz,CW-.08,.05,hh,M['DarkFrame'],a)
   for su in (-1,1):facade_box(m,x,y,u+su*(CW/2-.04),.24,(b+top)/2,.08,.08,top-b,M['DarkFrame'],a)
   facade_box(m,x,y,u,.44,b-.02,CW+.12,.20,.05,M['Copper'],a)
  facade_box(m,x,y,u,.22,.35,CW-.06,.02,.47,GLAZE,a);cas81(m,x,y,u,.11,CW-.06,.48,a,M['DarkFrame'],.25,1)
  facade_box(m,x,y,u,.42,.08,CW+.06,.14,.04,M['Copper'],a)
 facade_box(m,x,y,0,.42,H-.17,L+.1,.16,.36,M['Coping'],a)
flat94(m,'mo',H-.06,M['FlatRoof'])

# ---- 91926337: the blue-green gable house. s from the east corner (130.39, 113.94); camera 2.6 m.
GA,GB=(130.388,113.935),(122.662,115.993)
m=meshes['SM_Kvarnholmen_House_91926337']
for zone in ('bg','bgr'):
 H=Z[zone]['height'];fw=front94(zone) if zone=='bg' else None
 for w in walls(zone):
  if w['kind']!='outer':bz_wall(m,w['p'],w['q'],w['z0'],H,[],M['Aqua']);continue
  x,y,L,a=sf_edge(w['p'],w['q'])
  if w is not fw:
   bz_wall(m,w['p'],w['q'],0,H,[],M['Aqua']);vboards94(m,x,y,-L/2,L/2,a,.45,lambda u:H,[],M['Aqua'])
   facade_box(m,x,y,0,.40,.22,L,.10,.44,M['Plinth'],a);continue
  us=lambda s:U(w,*P94(GA,GB,s));T=Z['bg']['top']
  ops=[(us(5.95),1.20,1.15,1.45,'low'),(us(2.85),1.20,1.15,1.45,'low'),(us(4.04),4.20,1.05,1.70,'gable')]
  holes=[(u,b,ww,min(hh,H-.08-b),0) for u,b,ww,hh,k in ops if b<H-.3]
  bz_wall(m,w['p'],w['q'],0,H,holes,M['Aqua']);gable94(m,x,y,L,a,H,T,M['Aqua'])
  top=lambda u:H+(T-H)*(1-abs(u)/(L/2))
  vboards94(m,x,y,-L/2+.15,L/2-.15,a,.30,top,[(u,b,ww,hh,0) for u,b,ww,hh,k in ops],M['Aqua'])
  for u,b,ww,hh,k in ops:win94(m,x,y,u,b,ww,hh,a,M['Sash'],M['WhiteFrame'],2,.11,.40 if b+hh>H-.1 else .16)
  facade_box(m,x,y,0,.40,.15,L,.10,.30,M['Plinth'],a);facade_box(m,x,y,us(4.5),.44,.16,.45,.04,.14,M['DarkFrame'],a)
  for uu in (-L/2+.10,L/2-.10):facade_box(m,x,y,uu,.42,(H+.30)/2,.20,.10,H-.30,M['Aqua'],a)
 if zone=='bgr':flat94(m,'bgr',H+.02,M['FlatRoof'])
# The saddle roof, gable to the street; white double bargeboards.
H,T=Z['bg']['height'],Z['bg']['top'];sl,Q,ta=saddle94(m,GA,GB,0,7.98,5.6,H,T,M['Tile'],ov=.45,verge=.45,back=M['Aqua'])
for dz in (0,-.22):town_path(m,[Q(-.45,ta+.02,H-.45*sl+dz),Q(3.99,ta+.02,T+dz),Q(8.43,ta+.02,H-.45*sl+dz)],.09,M['WhiteFrame'])

# ---- 91926333: the red gable house. s from the east corner (143.51, 110.80); camera 2.45 m.
RA,RB=(143.508,110.803),(134.005,113.145);RW=6.70
m=meshes['SM_Kvarnholmen_House_91926333']
for zone in ('rh','rx'):
 H=Z[zone]['height'];fw=front94(zone) if zone=='rh' else None
 for w in walls(zone):
  if w['kind']!='outer':bz_wall(m,w['p'],w['q'],w['z0'],H,[],M['Red']);continue
  x,y,L,a=sf_edge(w['p'],w['q'])
  if w is not fw:
   bz_wall(m,w['p'],w['q'],0,H,[],M['Red']);vboards94(m,x,y,-L/2,L/2,a,.30,lambda u:H,[],M['Red'])
   facade_box(m,x,y,0,.40,.15,L,.10,.30,M['Plinth'],a);facade_box(m,x,y,0,.44,H-.10,L+.1,.14,.20,M['GreyTrim'],a);continue
  us=lambda s:U(w,*P94(RA,RB,s));T=Z['rh']['top']
  ops=[(us(s),b,1.20,hh) for s in (2.00,4.55) for b,hh in ((.95,1.15),(3.05,1.40))]
  holes=[(u,b,ww,min(hh,H-.08-b),0) for u,b,ww,hh in ops]
  bz_wall(m,w['p'],w['q'],0,H,holes,M['Red']);gable94(m,x,y,L,a,H,T,M['Red'])
  top=lambda u:H+(T-H)*(1-abs(u)/(L/2))
  vboards94(m,x,y,-L/2+.2,L/2-.2,a,.30,top,[(u,b,ww,hh,0) for u,b,ww,hh in ops],M['Red'],.20)
  for u,b,ww,hh in ops:win94(m,x,y,u,b,ww,hh,a,M['Yellow'],M['GreyTrim'],3,.14,.40 if b+hh>H-.1 else .16)
  facade_box(m,x,y,0,.40,.15,L,.10,.30,M['Plinth'],a)
  for uu in (-L/2+.11,L/2-.11):facade_box(m,x,y,uu,.43,(H+.30)/2,.22,.12,H-.30,M['GreyTrim'],a)
 if zone=='rx':flat94(m,'rx',H+.02,M['FlatRoof'])
H,T=Z['rh']['height'],Z['rh']['top'];sl,Q,ta=saddle94(m,RA,RB,0,RW,8.3,H,T,M['Tile'],ov=.45,verge=.45,back=M['Red'])
town_path(m,[Q(-.45,ta+.03,H-.45*sl-.10),Q(RW/2,ta+.03,T-.10),Q(RW+.45,ta+.03,H-.45*sl-.10)],.17,M['Barge'])
for nm in meshes:b94_finish(meshes[nm],nm.split('_')[-1])

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block94_cameras=[
 sv_camera('461_Block94_Cal_Office',99.92,125.94,2.50,166,15,90),
 sv_camera('462_Block94_Cal_Modernist',121.99,121.56,2.60,166,15,90),
 sv_camera('463_Block94_Cal_RedHouse',145.87,114.25,2.45,171.3,15,90),
 ('464_Block94_Aerial',(118.0,150.0,30.0),(118.0,113.0,3.0),28),
]
print('BLOCK94_GEOMETRY',len(block94_names))
