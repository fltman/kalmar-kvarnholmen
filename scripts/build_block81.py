"""Pass 81: the east end of Norra Långgatan, x 268-296, both sides; small boarded houses:
- south: the yellow gable cottage, a red-brown double gate (72), the green cottage with its gable, the
  grey-green gable house with a lunette window and its gateway, and the orange corner cottage;
- north: a boarded wall with a green door (73), the grey-green cottage, a red house, the white gable
  house, the small white house, the small red house with the pilastered door (77) and the big red
  corner house with dark corner boards.
Each front is drawn from its measured openings; the gate strips are released as open ground and
their gates drawn in the street plane.

References: Google Street View April 2025 (two panoramas on Norra Långgatan, each resected on a corner
and both base rows, with the vertical field of view checked), view only. Zones: source/block81.json;
see references/block81-notes.md. Signs, lamps, the parking meter and the number plates are omitted.
"""
B81D=json.loads((R/'source/block81.json').read_text());Z=B81D['zones']
block81_names=[];B81={}
for old in [k for k in list(materials) if k.startswith('M_Block81_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Yellow','TownIvory',(.86,.66,.28),.82,0),('Orange','TownIvory',(.88,.56,.24),.82,0),
 ('Green','TownIvory',(.62,.70,.58),.82,0),('GreyGreen','TownIvory',(.66,.72,.66),.82,0),
 ('Red','TownIvory',(.62,.20,.16),.82,0),('White','TownIvory',(.94,.94,.91),.82,0),
 ('WhiteFrame','TownPaintWhite',(.95,.95,.93),.55,0),('DarkBoard','TownPaintBrown',(.14,.12,.11),.70,0),
 ('RedBrown','TownPaintBrown',(.50,.22,.18),.60,0),('GreenDoor','TownPaintGreen',(.25,.50,.40),.60,0),
 ('GreyGreenDoor','TownPaintGreen',(.42,.48,.44),.60,0),('WeatheredWood','TownPaintBrown',(.55,.50,.42),.80,0),
 ('Plinth','TownStone',(.55,.55,.53),.90,0),('Tile','TownTileRed',(.62,.33,.24),.80,0),('TileDark','TownTileRed',(.40,.24,.20),.80,0),
 ('WindowBox','TownPaintBrown',(.30,.24,.18),.70,0),('Iron','TownMetalGrey',(.08,.08,.085),.45,.40),('Dark','TownMetalGrey',(.05,.055,.06),.40,.20),
 ]:
 name='M_Block81_'+key;B81[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block81_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B81;WF=M['WhiteFrame']

def b81_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block81_names.append(name);return Mesh(name,category)
def b81_finish(m,osm):
 obj=s21_finish(m);obj['detail_pass']=81;obj['reference_notes']='references/block81-notes.md';obj['osm_way']=osm;return obj
def cas81(m,x,y,u,b,w,h,a,frame,o=.16,rows=3):
 facade_box(m,x,y,u,o-.04,b+h/2,w,.02,h,GLAZE,a)
 for q in (-w/2+.04,w/2-.04,0):facade_box(m,x,y,u+q,o,b+h/2,.08 if q else .05,.08,h,frame,a)
 for k in range(rows+1):facade_box(m,x,y,u,o,b+.04+k*(h-.08)/rows,w,.08 if k in (0,rows) else .05,.06 if k in (0,rows) else .04,frame,a)
def boards81(m,x,y,L,a,z0,z1,holes,ma,step=.21):
 n=int(L/step)
 for k in range(1,n):
  u=-L/2+k*L/n;segs=[(z0,z1)]
  for hu,hb,hw,hh,hr in holes:
   if abs(u-hu)<hw/2+.15:segs=[(l0,h0) for l,h_ in segs for l0,h0 in ((l,min(h_,hb-.14)),(max(l,hb+hh+.16),h_)) if h0-l0>.05]
  for l0,h0 in segs:facade_box(m,x,y,u,.37,(l0+h0)/2,.035,.03,h0-l0,ma,a)

# The fronts: wall and trim colours, windows (x, bottom, width, height), doors (x, bottom, width,
# height, material), the gable window, window boxes. From the two panoramas.
F={'yl':dict(wall='Yellow',trim='WhiteFrame',wins=[(270.85,.92,1.38,1.65)]),
 'gc':dict(wall='Green',trim='WhiteFrame',wins=[(279.0,.92,1.49,1.30)],boxes=True),
 'gg':dict(wall='GreyGreen',trim='WhiteFrame',wins=[(287.0,1.21,1.33,1.32),(285.2,1.21,1.10,1.32),(287.0,3.0,1.1,1.1),(285.2,3.0,1.0,1.1)],gwin=(285.97,4.75,.6,.55),boxes=True),
 'gs':dict(wall='GreyGreen',trim='WhiteFrame',doors=[(290.13,.15,1.83,2.41,'GreyGreenDoor')]),
 'or':dict(wall='Orange',trim='WhiteFrame',wins=[(294.49,.88,1.18,1.39),(292.95,.88,1.10,1.39)],gwin=(293.71,2.95,1.2,1.40),boxes=True),
 'ck':dict(wall='GreyGreen',trim='WhiteFrame',wins=[(274.75,1.08,1.07,1.18)],boxes=True),
 'rd':dict(wall='Red',trim='WhiteFrame',wins=[(278.2,.95,1.0,1.2)]),
 'wb':dict(wall='White',trim='WhiteFrame',wins=[(281.2,.9,1.0,1.2),(283.0,.9,1.0,1.2),(281.2,2.55,1.0,1.1),(283.0,2.55,1.0,1.1)],boxes=True),
 'ws':dict(wall='White',trim='WhiteFrame',wins=[(286.36,1.0,.92,1.2)],doors=[(284.75,.1,.72,1.9,'GreenDoor')]),
 'sr':dict(wall='Red',trim='RedBrown',wins=[(288.6,1.0,.8,1.0)],doors=[(290.55,.15,.76,2.0,'DarkBoard')],pilasters=(289.89,291.09)),
 'br':dict(wall='Red',trim='WhiteFrame',wins=[(294.72,.65,1.0,1.22),(294.72,2.49,1.0,1.23)],corner='DarkBoard')}
SOUTH=('yl','gc','gg','gs','or')
def yface(zone,X):
 return 60.9+(X-268)*(60.2-60.9)/28 if zone in SOUTH else 71.9+(X-270)*(71.0-71.9)/27

meshes={}
for zone,spec in Z.items():
 nm=spec['mesh']
 if nm not in meshes:meshes[nm]=b81_new(nm,'Kvarnholmen/Norra Långgatan')
for zone,spec in Z.items():
 m=meshes[spec['mesh']];H=spec['height'];T=spec['top'];f=F[zone];wm=M[f['wall']];tm=M[f['trim']]
 for w in walls(zone):
  x,y,L,a=sf_edge(w['p'],w['q']);ox,oy=outward(w)
  front=w['kind']=='outer' and ((zone in SOUTH and oy>.9 and min(w['p'][1],w['q'][1])>59.5) or (zone not in SOUTH and oy<-.9 and max(w['p'][1],w['q'][1])<72.5))
  if not front:
   if w['kind']=='outer':plain(m,w,H,wm,WF,M['WhiteFrame'],1 if H<3.5 else 2,.6)
   else:bz_wall(m,w['p'],w['q'],w['z0'],H,[],wm)
   continue
  S=lambda X:U(w,X,yface(zone,X))
  # Openings only on the segment they lie on: a short slanted step would otherwise carry the house's
  # windows along its own extended line, out in the street.
  on=lambda u,ww:abs(u)+ww/2<=L/2+.01
  wins=[(S(X0),b,ww,hh,0) for X0,b,ww,hh in f.get('wins',[]) if on(S(X0),ww)]
  dl=[(d,(S(d[0]),d[1],d[2],d[3],0)) for d in f.get('doors',[]) if on(S(d[0]),d[2])];doors=[o for _,o in dl]
  bz_wall(m,w['p'],w['q'],0,H,wins+doors,wm);boards81(m,x,y,L,a,.3,H-.05,wins+doors,wm)
  for u,b,ww,hh,r in wins:
   cas81(m,x,y,u,b,ww,hh,a,WF if f['trim']=='WhiteFrame' else tm);surround36(m,x,y,u,b,ww,hh,a,tm,.10,.40);facade_box(m,x,y,u,.47,b-.06,ww+.26,.16,.06,tm,a)
   if f.get('boxes') and b<2:facade_box(m,x,y,u,.54,b-.24,ww*.8,.20,.20,M['WindowBox'],a)
  for (X0,_,_,_,dm),(u,b,ww,hh,r) in dl:
   for s in (-1,1):facade_box(m,x,y,u+s*ww/4,.10,b+hh/2,ww/2-.02,.06,hh,M[dm],a)
   surround36(m,x,y,u,b,ww,hh,a,tm,.12,.40)
  if 'pilasters' in f and all(on(S(X0),.3) for X0 in f['pilasters']):
   for X0 in f['pilasters']:facade_box(m,x,y,S(X0),.46,1.15,.22,.14,2.3,M['Yellow'],a)
   facade_box(m,x,y,(S(f['pilasters'][0])+S(f['pilasters'][1]))/2,.48,2.42,abs(S(f['pilasters'][1])-S(f['pilasters'][0]))+.3,.2,.2,tm,a)
  corner=M[f.get('corner','WhiteFrame')]
  for uu in (-L/2+.1,L/2-.1):facade_box(m,x,y,uu,.42,H/2,.22,.10,H,corner,a)
  facade_box(m,x,y,0,.39,.15,L,.08,.30,M['Plinth'],a)
  # One gable per house: on the longest street segment, its apex over the house's middle.
  fronts=[ww for ww in walls(zone) if ww['kind']=='outer' and ((zone in SOUTH and outward(ww)[1]>.9) or (zone not in SOUTH and outward(ww)[1]<-.9))]
  longest=max(fronts,key=lambda ww:math.dist(ww['p'],ww['q']))
  xs=[v[0] for g in spec['polygons'] for v in g]
  if spec['rooftype']=='gable' and w is longest:
   uc=S((min(xs)+max(xs))/2)
   ua,ub=S(min(xs)),S(max(xs));ua,ub=min(ua,ub),max(ua,ub)
   prof=[(ua,H),(ub,H),(uc,T)];vs=[lp(x,y,uu,o,zz,a) for o in (.005,.355) for uu,zz in prof]
   m.faces(vs,[(2,1,0),(3,4,5),(0,1,4,3),(1,2,5,4),(2,0,3,5)],wm)
   for ue in (ua-.3,ub+.3):town_path(m,[lp(x,y,ue,.46,H-.2,a),lp(x,y,uc,.46,T+.12,a)],.09,corner)
   if 'gwin' in f:
    X0,b,ww,hh=f['gwin'];u=S(X0)
    if b+hh<T-.3:facade_box(m,x,y,u,.37,b+hh/2,ww,.02,hh,GLAZE,a);cas81(m,x,y,u,b,ww,hh,a,WF,.40,2);surround36(m,x,y,u,b,ww,hh,a,tm,.10,.44)
  else:
   facade_box(m,x,y,0,.46,H-.06,L+.1,.16,.12,tm,a)
 if isinstance(spec.get('roof'),dict):roof34(m,zone,M['TileDark'] if zone in ('ck','gc') else M['Tile'],wm)
 else:
  # Irregular outlines: a saddle over the outline's bounding rectangle, gable triangles at its ends.
  xs=[v[0] for g in spec['polygons'] for v in g];ys=[v[1] for g in spec['polygons'] for v in g]
  x0,x1,y0,y1=min(xs),max(xs),min(ys),max(ys);ov=.3
  if spec['rooftype']=='gable':
   xm=(x0+x1)/2;sl=(T-H)/((x1-x0)/2)
   for xe in (x0-ov,x1+ov):
    pts=[(xe,y0-ov,H-ov*sl),(xm,y0-ov,T),(xm,y1+ov,T),(xe,y1+ov,H-ov*sl)]
    (a0,b0,c0),(a1,b1,c1),(a2,b2,c2)=pts[:3];nz=(a1-a0)*(b2-b0)-(b1-b0)*(a2-a0)
    m.faces(pts,[(0,1,2,3) if nz>0 else (3,2,1,0)],M['Tile'])
   for yy in (y0,y1):m.faces([(x0,yy,H),(x1,yy,H),(xm,yy,T)],[(0,1,2),(2,1,0)],wm)
  else:
   ym=(y0+y1)/2;sl=(T-H)/((y1-y0)/2)
   for ye in (y0-ov,y1+ov):
    pts=[(x0-ov,ye,H-ov*sl),(x1+ov,ye,H-ov*sl),(x1+ov,ym,T),(x0-ov,ym,T)]
    (a0,b0,c0),(a1,b1,c1),(a2,b2,c2)=pts[:3];nz=(a1-a0)*(b2-b0)-(b1-b0)*(a2-a0)
    m.faces(pts,[(0,1,2,3) if nz>0 else (3,2,1,0)],M['Tile'])
   for xx in (x0,x1):m.faces([(xx,y0,H),(xx,y1,H),(xx,ym,T)],[(0,1,2),(2,1,0)],wm)
# Gates and walls in the street plane over the released strips.
def gate81(m,p,q,Xs,hh,dm,wallm,top):
 x,y,L,a=sf_edge(p,q);S=lambda X:U({'p':p,'q':q},X,(p[1]+q[1])/2)
 for (X0,X1) in Xs:
  u=(S(X0)+S(X1))/2;ww=abs(S(X1)-S(X0))
  for s in (-1,1):
   facade_box(m,x,y,u+s*ww/4,.10,hh/2,ww/2-.02,.06,hh,dm,a)
   for k in range(1,10):facade_box(m,x,y,u+s*ww/4,.14,k*hh/10,ww/2-.06,.02,.02,M['Dark'],a)
 if wallm:
  at=-L/2
  for lo,hi in sorted([(min(S(X0),S(X1)),max(S(X0),S(X1))) for X0,X1 in Xs])+[(L/2,L/2)]:
   if lo>at+.03:facade_box(m,x,y,(at+lo)/2,.30,top/2,lo-at,.05,top,wallm,a)
   at=max(at,hi)
  for X0,X1 in Xs:facade_box(m,x,y,(S(X0)+S(X1))/2,.30,(hh+top)/2,abs(S(X1)-S(X0)),.05,top-hh,wallm,a)
 for uu in (-L/2+.08,L/2-.08):facade_box(m,x,y,uu,.30,(top+.1)/2,.16,.16,top+.1,M['WhiteFrame'],a)
 facade_box(m,x,y,0,.30,top+.08,L+.1,.30,.12,M['WhiteFrame'],a)
m=meshes['SM_Kvarnholmen_House_93192416'];gate81(m,(273.3,60.95),(276.06,60.9),[(273.64,276.06)],2.16,M['RedBrown'],None,2.2)
m.prism([(273.3,60.9),(276.06,60.85),(276.06,56.5),(273.3,56.5)],2.25,2.4,M['Tile'])
m=meshes['SM_Kvarnholmen_House_93192447'];gate81(m,(267.0,61.0),(268.6,61.0),[(267.0,268.3)],1.8,M['WeatheredWood'],None,1.85)
m=meshes['SM_Kvarnholmen_House_90859897'];gate81(m,(270.3,71.95),(272.35,71.9),[(270.54,271.83)],2.16,M['GreenDoor'],M['White'],2.25)
for nm in meshes:b81_finish(meshes[nm],nm.split('_')[-1])

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block81_cameras=[
 sv_camera('401_Block81_Cal_South',273.61,68.0,2.30,152,10,90),
 sv_camera('402_Block81_Cal_North',273.61,68.0,2.30,332,10,90),
 sv_camera('403_Block81_Cal_Corner',294.64,67.2,2.16,152,10,90),
 sv_camera('404_Block81_Cal_Red',294.64,67.2,2.16,332,10,90),
 sv_camera('405_Block81_Cal_West',294.64,67.2,2.16,282,10,90),
 ('406_Block81_Aerial',(282.0,48.0,26.0),(282.0,66.0,2.0),28),
]
print('BLOCK81_GEOMETRY',len(block81_names))
