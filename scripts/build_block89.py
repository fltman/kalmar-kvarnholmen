"""Pass 89: the south side of east Storgatan, x 202-265, five houses west to east:
- Storgatan 60, the pale green rendered two-storey house: six bays, the panelled double door, the
  carriage gateway with its fanlight at the west end, a storey band, and a dark tiled hip roof with
  two roof lights;
- Storgatan 62, the yellow boarded two-storey house: white corner and middle pilasters, four
  windows a floor (the ground-floor ones under small crowns), the pediment with its lunette over
  the middle bays, a low metal saddle roof; the yellow boarded fence in the gap to 64;
- Storgatan 64, the long pale yellow rendered two-storey house on a dark plinth: eight bays, the
  brown door on steps in the middle, a storey band, a red tiled saddle roof with two red dormers,
  ochre gables (the east one with two windows and a lunette); the low yellow boarded gateway with
  the red-panelled doors in the gap east of it;
- the small green boarded house with its gable to the street, two windows a floor;
- the green boarded wall with the black double gate and the low shed roof behind.

References: Google Street View April 2025 (four panoramas on Storgatan, all resected on house
corners), view only. Zones: source/block89.json; see references/block89-notes.md. Signs, house
numbers, lamps, pipes and the cars are omitted.
"""
B89D=json.loads((R/'source/block89.json').read_text());Z=B89D['zones']
block89_names=[];B89={}
for old in [k for k in list(materials) if k.startswith('M_Block89_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Green60','TownIvory',(.68,.72,.60),.90,0),('Yellow62','TownIvory',(.92,.83,.58),.82,0),('Yellow64','TownIvory',(.93,.87,.69),.90,0),
 ('Ochre','TownIvory',(.78,.69,.52),.90,0),('GreenBoard','TownIvory',(.53,.57,.45),.82,0),('GreenWall','TownIvory',(.58,.62,.49),.82,0),
 ('Trim','TownPaintWhite',(.92,.92,.88),.55,0),('Cream','TownPaintWhite',(.90,.86,.74),.55,0),('GreyDoor','TownPaintGreen',(.44,.48,.44),.60,0),
 ('BrownDoor','TownPaintBrown',(.52,.30,.18),.55,0),('RedPanel','TownPaintBrown',(.62,.16,.15),.60,0),('Black','TownMetalGrey',(.08,.09,.09),.45,.20),
 ('Plinth','TownStone',(.64,.63,.60),.90,0),('PlinthDark','TownStone',(.33,.34,.36),.90,0),
 ('TileDark','TownTileRed',(.38,.29,.24),.80,0),('Tile','TownTileRed',(.68,.34,.25),.80,0),('DormerRed','TownPaintBrown',(.66,.20,.17),.60,0),
 ('Metal','TownMetalGrey',(.34,.33,.32),.55,.30),('RedMetal','TownMetalGrey',(.58,.30,.26),.55,.20),('Dark','TownMetalGrey',(.05,.055,.06),.40,.20),
 ('Chimney','TownTileRed',(.55,.33,.27),.85,0),
 ]:
 name='M_Block89_'+key;B89[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block89_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B89;TR=M['Trim']

def b89_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block89_names.append(name);return Mesh(name,category)
def drop_degenerate_faces(obj,tol=1e-9):
 # Faces drawn with a repeated corner (a gable or roof end closing on one point) have no area and
 # no UV frame, which the tangent export rejects; they draw nothing, so they are removed.
 import bmesh
 bm=bmesh.new();bm.from_mesh(obj.data)
 # Also slivers thinner than 0.1 mm (two corners almost on top of each other along a long edge).
 def _thin(f):
  L=max(e.calc_length() for e in f.edges);return L>0 and 2*f.calc_area()/L<1e-4
 bad=[f for f in bm.faces if f.calc_area()<tol or len({v.index for v in f.verts})<len(f.verts) or _thin(f)]
 if bad:bmesh.ops.delete(bm,geom=bad,context='FACES_ONLY')
 bm.to_mesh(obj.data);bm.free();obj.data.update();return len(bad)
def b89_finish(m,osm):
 obj=s21_finish(m);drop_degenerate_faces(obj);obj['detail_pass']=89;obj['reference_notes']='references/block89-notes.md';obj['osm_way']=osm;return obj
def P89(a,b,s):L=math.dist(a,b);return (a[0]+(b[0]-a[0])*s/L,a[1]+(b[1]-a[1])*s/L)
def gable89(m,w,H,T,ma,u0=None,u1=None):
 # A solid gable triangle on a wall, flush with the wall's thickness (offsets 0.005-0.355).
 x,y,L,a=sf_edge(w['p'],w['q']);u0=-L/2 if u0 is None else u0;u1=L/2 if u1 is None else u1
 prof=[(u0,H),(u1,H),((u0+u1)/2,T)];vs=[lp(x,y,uu,o,zz,a) for o in (.005,.355) for uu,zz in prof]
 m.faces(vs,[(2,1,0),(3,4,5),(0,1,4,3),(1,2,5,4),(2,0,3,5)],ma)
def lunette89(m,x,y,u,zb,r,a,frame,o=.36):
 # A half-round window standing on zb, with its frame and three glazing bars.
 k=12;arc=[(u+r*math.cos(math.pi*t/k),zb+r*math.sin(math.pi*t/k)) for t in range(k+1)]
 m.faces([lp(x,y,uu,o+.01,zz,a) for uu,zz in arc],[tuple(range(k+1)),tuple(range(k,-1,-1))],GLAZE)
 town_path(m,[lp(x,y,uu,o+.05,zz,a) for uu,zz in arc]+[lp(x,y,u+r,o+.05,zb,a)],.05,frame)
 for t in (3,6,9):town_path(m,[lp(x,y,u,o+.05,zb,a),lp(x,y,u+r*math.cos(math.pi*t/12),o+.05,zb+r*math.sin(math.pi*t/12),a)],.025,frame)
def win89(m,x,y,u,b,w,h,a,frame,rendered=True,crown=False):
 cas81(m,x,y,u,b,w,h,a,frame,.16,3 if h>1.2 else 2)
 surround36(m,x,y,u,b,w,h,a,TR,.12 if rendered else .10,.40)
 facade_box(m,x,y,u,.47,b-.06,w+.30,.16,.07,TR,a)
 if crown:
  # The small gabled crown over the boarded house's ground-floor windows.
  z=b+h+.14;prof=[(u-w/2-.18,z),(u+w/2+.18,z),(u,z+.28)];vs=[lp(x,y,uu,o,zz,a) for o in (.36,.46) for uu,zz in prof]
  m.faces(vs,[(2,1,0),(3,4,5),(0,1,4,3),(1,2,5,4),(2,0,3,5)],TR)
def plinth89(m,x,y,L,a,ops,h,ma):
 at=-L/2
 for lo,hi in sorted((u-ww/2,u+ww/2) for k,u,b,ww,hh in ops if k in ('door','gate') and b<h)+[(L/2,L/2)]:
  if lo>at+.03:facade_box(m,x,y,(at+lo)/2,.40,h/2,lo-at,.10,h,ma,a)
  at=max(at,hi)
def eaves89(m,x,y,L,a,H,ma,cornice=True):
 if cornice:
  facade_box(m,x,y,0,.42,H-.22,L+.05,.14,.26,ma,a);facade_box(m,x,y,0,.47,H-.06,L+.12,.24,.10,ma,a)
 else:facade_box(m,x,y,0,.46,H-.10,L+.1,.14,.20,ma,a)
 town_rod(m,lp(x,y,-L/2,.64,H-.02,a),lp(x,y,L/2,.64,H-.02,a),.06,TR,8)

# The street fronts, east corner -> west corner (OSM vertices); positions s are metres from the
# east corner, measured on the resected panoramas. Openings: (kind, s, bottom, width, height).
F60=((216.543,-10.777),(202.156,-10.591))
F62=((227.917,-10.926),(216.543,-10.777))
F64=((250.005,-10.77),(229.344,-10.504))
FGH=((259.354,-10.68),(252.973,-10.555))
FGW=((265.243,-10.793),(259.354,-10.68))
FRONT={'g60':F60,'y62':F62,'y64':F64,'gh':FGH,'gw':FGW}
OPS={'g60':[('win',s,3.93,.95,1.35) for s in (1.75,3.56,5.96,8.23,9.97,12.61)]+[('win',s,1.35,.95,1.45) for s in (1.77,3.52,8.24,10.0)]
  +[('door',5.85,.50,1.15,2.30),('gate',12.70,0,2.40,2.80)],
 'y62':[('win',s,3.85,.95,1.40) for s in (2.0,4.37,6.74,9.13)]+[('crown',s,1.05,.95,1.55) for s in (2.0,4.37,6.74,9.13)],
 'y64':[('win',s,4.48,1.0,1.75) for s in (2.21,4.45,6.87,8.79,11.14,13.79,16.35,18.92)]+[('win',s,1.25,1.0,1.75) for s in (2.34,4.5,6.83,8.86,13.79,16.41,19.01)]
  +[('door',11.10,.80,1.15,2.30)],
 'gh':[('win',s,1.0,.95,1.35) for s in (1.75,3.85)]+[('win',s,3.2,.95,1.05) for s in (1.75,3.85)],
 'gw':[('gate',4.60,0,2.50,2.40)]}
WALL={'g60':'Green60','y62':'Yellow62','y64':'Yellow64','gh':'GreenBoard','gw':'GreenWall'}
BOARDED={'y62','gh','gw'}

meshes={}
for zone,spec in Z.items():
 nm=spec['mesh']
 if nm not in meshes:meshes[nm]=b89_new(nm,'Kvarnholmen/Storgatan')
for zone,spec in Z.items():
 m=meshes[spec['mesh']];H=spec['height'];T=spec['top'];wm=M[WALL[zone]];fa,fb=FRONT[zone]
 for w in walls(zone):
  if w['kind']!='outer':bz_wall(m,w['p'],w['q'],w['z0'],H,[],wm);continue
  x,y,L,a=sf_edge(w['p'],w['q']);ox,oy=outward(w)
  if oy<.85:
   # Side and rear walls: the east gable of 64 is ochre render; the rest plain.
   side=M['Ochre'] if zone=='y64' else wm
   if zone=='gw':bz_wall(m,w['p'],w['q'],0,H,[],wm)
   else:plain(m,w,H,side,TR,TR,1 if H<5 else 2,.9)
   continue
  ops=[(k,U(w,*P89(fa,fb,s)),b,ww,hh) for k,s,b,ww,hh in OPS[zone]]
  holes=[(u,b,ww,hh,0) for k,u,b,ww,hh in ops]
  bz_wall(m,w['p'],w['q'],0,H,holes,wm)
  if zone in BOARDED:boards81(m,x,y,L,a,.45,H-.25,holes,wm)
  for k,u,b,ww,hh in ops:
   if k in ('win','crown'):win89(m,x,y,u,b,ww,hh,a,M['Cream'] if zone=='gh' else TR,zone not in BOARDED,k=='crown')
   elif k=='door':
    door83(m,x,y,u,b,ww,hh,a,M['GreyDoor'] if zone=='g60' else M['BrownDoor'],TR,zone!='g60')
    if b>.25:steps82(m,x,y,u,ww+.3,b,a,M['Plinth'])
   elif k=='gate':
    if zone=='g60':
     # The gateway: panelled leaves under a glazed fanlight.
     gate83(m,x,y,u,b,ww,hh-.55,a,M['GreyDoor'],M['GreyDoor'])
     facade_box(m,x,y,u,.17,hh-.27,ww-.1,.02,.45,GLAZE,a)
     for q in (-.6,0,.6):facade_box(m,x,y,u+q,.20,hh-.27,.05,.05,.45,M['GreyDoor'],a)
     surround36(m,x,y,u,b,ww,hh,a,TR,.14,.40)
    else:gate83(m,x,y,u,b,ww,hh,a,M['Black'],M['Black'])
  # Corners, plinths, bands, eaves.
  if zone=='g60':
   plinth89(m,x,y,L,a,ops,.45,M['Plinth'])
   facade_box(m,x,y,0,.42,3.30,L,.10,.18,TR,a)
   for k,u,b,ww,hh in ops:
    if k=='win' and b>3:facade_box(m,x,y,u,.40,b-.40,ww+.20,.06,.55,TR,a)
   for uu in (-L/2+.15,L/2-.15):facade_box(m,x,y,uu,.40,H/2,.30,.08,H,TR,a)
   eaves89(m,x,y,L,a,H,TR)
  elif zone=='y64':
   plinth89(m,x,y,L,a,ops,.90,M['PlinthDark'])
   facade_box(m,x,y,0,.42,3.80,L,.10,.20,TR,a)
   for k,u,b,ww,hh in ops:
    if k=='win':facade_box(m,x,y,u,.40,b-.35,ww+.24,.06,.45,TR,a)
   for uu in (-L/2+.15,L/2-.15):facade_box(m,x,y,uu,.40,H/2,.30,.08,H,TR,a)
   eaves89(m,x,y,L,a,H,TR)
  elif zone=='y62':
   plinth89(m,x,y,L,a,ops,.40,M['Plinth'])
   for s in (.13,3.36,7.98,L-.13):facade_box(m,x,y,U(w,*P89(fa,fb,s)),.45,H/2,.26,.10,H,TR,a)
   facade_box(m,x,y,0,.43,3.30,L,.08,.14,TR,a)
   eaves89(m,x,y,L,a,H,TR,False)
   # The pediment over the middle bays: a frontispiece gable with its lunette.
   u=U(w,*P89(fa,fb,5.67))
   frontis83(m,x,y,u,4.4,H,H+.05,7.5,a,wm,TR,M['Metal'],False)
   lunette89(m,x,y,u,H+.30,.45,a,TR)
  elif zone=='gh':
   plinth89(m,x,y,L,a,ops,.45,M['PlinthDark'])
   for uu in (-L/2+.09,L/2-.09):facade_box(m,x,y,uu,.42,H/2,.18,.10,H,M['Cream'],a)
  elif zone=='gw':
   facade_box(m,x,y,0,.44,H-.06,L+.05,.14,.12,wm,a)
   for uu in (-L/2+.08,L/2-.08):facade_box(m,x,y,uu,.42,H/2,.16,.10,H,wm,a)
# Roofs.
m=meshes['SM_Kvarnholmen_House_91928538'];r,sl60=hip82(m,'g60',F60[1],F60[0],M['TileDark'])
d,n=frame82(*F60);ang=math.atan2(d[1],d[0])
for s in (6.6,9.0):X,Y=P89(*F60,s);skylight82(m,X+n[0]*1.9,Y+n[1]*1.9,Z['g60']['height']+1.9*sl60,ang,sl60)
X,Y=P89(*F60,10.4);chimney82(m,X+n[0]*4.2,Y+n[1]*4.2,Z['g60']['top']-.5,Z['g60']['top']+.6,M['Chimney'])
m=meshes['SM_Kvarnholmen_House_91928591'];saddle82(m,'y62',F62[1],F62[0],M['Metal'],M['Yellow62'])
for w in walls('y62'):
 ox,oy=outward(w)
 if abs(ox)>.85 and math.dist(w['p'],w['q'])>5:gable89(m,w,Z['y62']['height'],Z['y62']['top'],M['Yellow62'])
# The yellow boarded fence in the 1.4 m gap between 62 and 64 (outside the OSM outlines).
x,y,L,a=sf_edge((229.344,-10.504),(227.917,-10.926));facade_box(m,x,y,0,.32,1.30,L,.08,2.60,M['Yellow62'],a);boards81(m,x,y,L,a,.10,2.50,[],M['Yellow62'])
m=meshes['SM_Kvarnholmen_House_91928561'];saddle82(m,'y64',F64[1],F64[0],M['Tile'],M['Ochre'])
H64,T64=Z['y64']['height'],Z['y64']['top'];sl64=(T64-H64)/(12.16/2)
for w in walls('y64'):
 ox,oy=outward(w)
 if abs(ox)>.85:
  gable89(m,w,H64,T64,M['Ochre']);x,y,L,a=sf_edge(w['p'],w['q'])
  if ox>0:
   # East gable: two windows a little above the eaves and a lunette under the apex.
   for uu in (-1.5,1.5):win89(m,x,y,uu,7.55,.80,1.05,a,TR)
   lunette89(m,x,y,0,10.4,.55,a,TR)
x,y,L,a=sf_edge(*F64)
for s in (5.6,15.6):
 u=U({'p':list(F64[0]),'q':list(F64[1])},*P89(*F64,s))
 dormer82(m,x,y,u,a,H64,sl64,1.35,.85,M['DormerRed'],TR,M['DormerRed'])
 # A small gable on the dormer's face.
 zt=H64+(.9+.40-.355+.05)*sl64-.15+.85+.55
 prof=[(u-.78,zt),(u+.78,zt),(u,zt+.45)];vs=[lp(x,y,uu,o,zz,a) for o in (.355-.9-.05,.355-.9-2.2) for uu,zz in prof]
 m.faces(vs,[(2,1,0),(3,4,5),(0,1,4,3),(1,2,5,4),(2,0,3,5)],M['DormerRed'])
# The low yellow boarded gateway with red-panelled doors between 64 and the green house (outside
# the OSM outlines): a front wall with a narrow tiled lean-to.
x,y,L,a=sf_edge((252.973,-10.555),(250.005,-10.77))
facade_box(m,x,y,0,.30,1.55,L,.12,3.10,M['Yellow64'],a);boards81(m,x,y,L,a,.10,2.95,[(0,.10,2.2,2.6,0)],M['Yellow64'])
for s in (-1,1):
 facade_box(m,x,y,s*.55,.40,1.40,1.05,.06,2.60,M['Cream'],a)
 for zz in (.45,1.05,1.75,2.40):
  for q in (-.24,.24):facade_box(m,x,y,s*.55+q,.44,zz,.36,.03,.45,M['RedPanel'],a)
facade_box(m,x,y,0,-.40,3.15,L,1.3,.08,M['Tile'],a)
m=meshes['SM_Kvarnholmen_House_91928583'];saddle82(m,'gh',FGH[1],FGH[0],M['Tile'],M['GreenBoard'],along=False)
for w in walls('gh'):
 ox,oy=outward(w)
 if abs(oy)>.85:
  gable89(m,w,Z['gh']['height'],Z['gh']['top'],M['GreenBoard']);x,y,L,a=sf_edge(w['p'],w['q'])
  if oy>0:
   facade_box(m,x,y,0,.40,Z['gh']['height']+.05,L,.06,.10,M['Cream'],a)
   sl=(Z['gh']['top']-Z['gh']['height'])/(L/2)
   for s in (-1,1):town_path(m,[lp(x,y,s*(L/2+.30),.62,Z['gh']['height']-.30*sl-.05,a),lp(x,y,0,.62,Z['gh']['top']+.02,a)],.07,M['Cream'])
m=meshes['SM_Kvarnholmen_House_91928590']
for g in Z['gw']['polygons']:m.faces([(*v,Z['gw']['height']+.03) for v in g],[tuple(range(len(g))),tuple(range(len(g)-1,-1,-1))],M['RedMetal'])
for nm in meshes:b89_finish(meshes[nm],nm.split('_')[-1])

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block89_cameras=[
 sv_camera('436_Block89_Cal_Sixty',208.69,-3.56,2.40,152,15,90),
 sv_camera('437_Block89_Cal_SixtyTwo',219.15,-3.10,2.40,152,15,90),
 sv_camera('438_Block89_Cal_SixtyFour',239.36,-3.71,2.40,152,15,90),
 sv_camera('439_Block89_Cal_Gate',260.10,-2.80,2.40,152,15,90),
 ('440_Block89_Aerial',(234.0,25.0,32.0),(234.0,-15.0,2.0),28),
]
print('BLOCK89_GEOMETRY',len(block89_names))
