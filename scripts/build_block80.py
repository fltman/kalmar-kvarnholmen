"""Pass 80: the north side of Norra Långgatan east of pass 76:
- a red boarded wall with a brown double gate and a stained-glass window between the pass 76 white
  house and the olive house;
- the olive boarded gable house (90859833) with red-brown trim;
- the long white two-storey boarded house with a tile roof and a red dormer, missing from the model
  until now (OSM way 90859904), and its grey-white gabled annex with the garage door;
- the red boarded gable house (90859843) with white trim and window boxes;
- the small white cottage with blue trim (90859883), with a blue boarded fence and a red gate beside
  it (the strips beside the cottage are released as open ground).

References: Google Street View April 2025 (the pass 77 and pass 78 panoramas on Norra Långgatan,
looking north; their base rows put these fronts about 0.8 m behind the district outline, and the
fronts are kept on the outline), view only. Zones: source/block80.json; see
references/block80-notes.md. The window boxes' flowers, the lamp and the number plates are omitted.
"""
B80D=json.loads((R/'source/block80.json').read_text());Z=B80D['zones']
block80_names=[];B80={}
for old in [k for k in list(materials) if k.startswith('M_Block80_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Olive','TownIvory',(.52,.46,.26),.85,0),
 ('OliveTrim','TownPaintBrown',(.45,.20,.16),.60,0),
 ('White','TownIvory',(.93,.92,.88),.82,0),
 ('GreyWhite','TownIvory',(.84,.84,.80),.84,0),
 ('WhiteFrame','TownPaintWhite',(.95,.95,.93),.55,0),
 ('Red','TownIvory',(.62,.20,.16),.82,0),
 ('RedWall','TownIvory',(.66,.36,.32),.85,0),
 ('BrownGate','TownPaintBrown',(.32,.25,.20),.60,0),
 ('BrownDoor','TownPaintBrown',(.52,.24,.18),.60,0),
 ('Blue','TownPaintWhite',(.18,.28,.42),.55,0),
 ('Plinth','TownStone',(.62,.62,.60),.90,0),
 ('Tile','TownTileRed',(.62,.32,.24),.80,0),
 ('RedDormer','TownPaintBrown',(.55,.20,.16),.60,0),
 ('Glass','TownPaintWhite',(.30,.45,.40),.30,0),
 ('WindowBox','TownPaintBrown',(.36,.28,.20),.70,0),
 ('Dark','TownMetalGrey',(.05,.055,.06),.40,.20),
 ]:
 name='M_Block80_'+key;B80[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block80_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B80;WF=M['WhiteFrame']

def b80_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block80_names.append(name);return Mesh(name,category)
def b80_finish(m,osm):
 obj=s21_finish(m);obj['detail_pass']=80;obj['reference_notes']='references/block80-notes.md';obj['osm_way']=osm;return obj
def cas80(m,x,y,u,b,w,h,a,frame,o=.16,rows=3):
 facade_box(m,x,y,u,o-.04,b+h/2,w,.02,h,GLAZE,a)
 for q in (-w/2+.04,w/2-.04,0):facade_box(m,x,y,u+q,o,b+h/2,.08 if q else .05,.08,h,frame,a)
 for k in range(rows+1):facade_box(m,x,y,u,o,b+.04+k*(h-.08)/rows,w,.08 if k in (0,rows) else .05,.06 if k in (0,rows) else .04,frame,a)
def boards80(m,x,y,L,a,z0,z1,holes,ma,step=.22,lo=None,hi=None):
 lo=-L/2 if lo is None else lo;hi=L/2 if hi is None else hi;n=int((hi-lo)/step)
 for k in range(1,n):
  u=lo+k*(hi-lo)/n;segs=[(z0,z1(u) if callable(z1) else z1)]
  for hu,hb,hw,hh,hr in holes:
   if abs(u-hu)<hw/2+.15:segs=[(l0,h0) for l,h_ in segs for l0,h0 in ((l,min(h_,hb-.14)),(max(l,hb+hh+.16),h_)) if h0-l0>.05]
  for l0,h0 in segs:facade_box(m,x,y,u,.37,(l0+h0)/2,.035,.03,h0-l0,ma,a)
def gable80(m,x,y,a,ua,ub,uc,H,T,ma,o0=.005,o1=.355):
 # The gable triangle over the eaves, in the wall plane.
 prof=[(ua,H),(ub,H),(uc,T)]
 vs=[lp(x,y,uu,o,zz,a) for o in (o0,o1) for uu,zz in prof];nn=3
 m.faces(vs,[(2,1,0),(3,4,5),(0,1,4,3),(1,2,5,4),(2,0,3,5)],ma)
def window80(m,x,y,wins,a,frame,surround,o=.16):
 for u,b,ww,hh,r in wins:
  cas80(m,x,y,u,b,ww,hh,a,frame,o);surround36(m,x,y,u,b,ww,hh,a,surround,.10,.40 if o<.3 else .44)
  facade_box(m,x,y,u,.47 if o<.3 else .5,b-.06,ww+.26,.16,.06,surround,a)
def yf80(X):return 72.25+(X-234.5)*(71.68-72.25)/(266.3-234.5)

meshes={nm:b80_new(nm,'Kvarnholmen/Norra Långgatan') for nm in ('SM_Kvarnholmen_House_90859833','SM_Kvarnholmen_House_90859904','SM_Kvarnholmen_House_90859843','SM_Kvarnholmen_House_90859883')}
WALLM={'ol':M['Olive'],'wh':M['White'],'wa':M['GreyWhite'],'yb':M['GreyWhite'],'rd':M['Red'],'ck':M['White']}
for zone in ('ol','wh','wa','yb','rd','ck'):
 m=meshes[Z[zone]['mesh']];H=Z[zone]['height'];T=Z[zone]['top'];wm=WALLM[zone]
 for w in walls(zone):
  x,y,L,a=sf_edge(w['p'],w['q']);ox,oy=outward(w)
  front=w['kind']=='outer' and oy<-.9 and max(w['p'][1],w['q'][1])<72.5
  if not front:
   if w['kind']=='outer':plain(m,w,H,wm,WF,M['WhiteFrame'],1 if zone=='ck' else 2,.6)
   else:bz_wall(m,w['p'],w['q'],w['z0'],H,[],wm)
   continue
  S=lambda X:U(w,X,yf80(X))
  if zone=='ol':
   wins=[(S(X0),b,1.05,h,0) for X0 in (235.1,236.97) for b,h in ((.73,1.05),(2.66,1.14))]
   bz_wall(m,w['p'],w['q'],0,H,wins,wm);boards80(m,x,y,L,a,.30,H-.05,wins,wm)
   window80(m,x,y,wins,a,WF,M['OliveTrim'])
   gable80(m,x,y,a,-L/2-.1,L/2+.1,S(236.2),H,T+.02,wm)
   for uu in (-L/2+.1,L/2-.1):facade_box(m,x,y,uu,.42,H/2,.20,.10,H,M['OliveTrim'],a)
   facade_box(m,x,y,0,.42,H-.05,L+.1,.10,.12,M['OliveTrim'],a)
   for s in (-1,1):town_path(m,[lp(x,y,s*(L/2+.3),.46,H-.18,a),lp(x,y,S(236.2),.46,T+.12,a)],.08,M['OliveTrim'])
   facade_box(m,x,y,0,.39,.15,L,.08,.30,M['Plinth'],a)
  elif zone=='wh':
   AX=[241.63,243.97,246.62,251.21,252.86]
   gf=[(S(X0),.90,1.10,1.40,0) for X0 in AX];up=[(S(X0),2.90,1.10,1.30,0) for X0 in AX+[249.5]]
   door=(S(249.5),.45,1.10,2.15,0)
   bz_wall(m,w['p'],w['q'],0,H,gf+up+[door],wm);boards80(m,x,y,L,a,.45,H-.1,gf+up+[door],wm)
   window80(m,x,y,gf+up,a,M['OliveTrim'],WF)
   u,b,ww,hh,r=door
   facade_box(m,x,y,u,.10,b+hh/2,ww,.06,hh,M['BrownDoor'],a);surround36(m,x,y,u,b,ww,hh,a,WF,.12,.40)
   facade_box(m,x,y,u,.46,b+hh+.2,ww+.4,.16,.12,WF,a);steps36(m,x,y,u,a,1.5,1.3,b,2,.30,M['Plinth'])
   for uu in (-L/2+.1,S(248.2),L/2-.1):facade_box(m,x,y,uu,.42,(.45+H)/2,.20,.10,H-.45,WF,a)
   facade_box(m,x,y,0,.39,.22,L,.08,.45,M['Plinth'],a)
   facade_box(m,x,y,0,.42,H-.12,L,.10,.24,WF,a);facade_box(m,x,y,0,.56,H+.04,L+.10,.36,.12,WF,a)
  elif zone=='wa':
   gar=(S(255.35),.02,1.45,2.30,0)
   bz_wall(m,w['p'],w['q'],0,H,[gar],wm);boards80(m,x,y,L,a,.3,H-.05,[gar],wm)
   u,b,ww,hh,r=gar
   facade_box(m,x,y,u,.10,b+hh/2,ww,.06,hh,M['GreyWhite'],a)
   for k in range(1,9):facade_box(m,x,y,u,.14,b+k*hh/9,ww-.06,.02,.02,M['Plinth'],a)
   surround36(m,x,y,u,b,ww,hh,a,WF,.10,.40);facade_box(m,x,y,u,.46,b+hh+.3,L+.2,.16,.30,WF,a)
   gable80(m,x,y,a,-L/2-.05,L/2+.05,0,H,T,wm)
   for s in (-1,1):town_path(m,[lp(x,y,s*(L/2+.2),.46,H-.12,a),lp(x,y,0,.46,T+.1,a)],.07,WF)
  elif zone=='rd':
   wins=[(S(X0),b,1.20,h,0) for X0 in (257.95,259.55) for b,h in ((.82,1.18),(2.87,1.25))]
   gw=(S(258.9),4.45,.72,.85,0)
   bz_wall(m,w['p'],w['q'],0,H,wins,wm);boards80(m,x,y,L,a,.45,H-.05,wins,wm)
   window80(m,x,y,wins,a,WF,WF)
   for u,b,ww,hh,r in wins:
    if b<2:facade_box(m,x,y,u,.62,b-.22,ww,.28,.24,M['WindowBox'],a)
   gable80(m,x,y,a,-L/2-.1,L/2+.1,S(258.65),H,T+.02,wm)
   u,b,ww,hh,r=gw;facade_box(m,x,y,u,.37,b+hh/2,ww,.02,hh,GLAZE,a);cas80(m,x,y,u,b,ww,hh,a,WF,.40,2);surround36(m,x,y,u,b,ww,hh,a,WF,.10,.44)
   for uu in (-L/2+.1,L/2-.1):facade_box(m,x,y,uu,.42,H/2,.22,.10,H,WF,a)
   for s in (-1,1):town_path(m,[lp(x,y,s*(L/2+.3),.46,H-.2,a),lp(x,y,S(258.65),.46,T+.14,a)],.10,WF)
   facade_box(m,x,y,0,.39,.22,L,.08,.45,M['Plinth'],a)
  elif zone=='ck':
   win=(S(264.28),.49,1.22,1.35,0)
   bz_wall(m,w['p'],w['q'],0,H,[win],wm);boards80(m,x,y,L,a,.2,H-.05,[win],wm,.20)
   gable80(m,x,y,a,-L/2-.05,L/2+.05,S(264.3),H,T,wm)
   u,b,ww,hh,r=win;facade_box(m,x,y,u,.2,b+hh/2,ww,.02,hh,GLAZE,a);cas80(m,x,y,u,b,ww,hh,a,WF,.40,2);surround36(m,x,y,u,b,ww,hh,a,M['Blue'],.10,.44)
   for uu in (-L/2+.1,L/2-.1):facade_box(m,x,y,uu,.42,H/2,.20,.10,H,M['Blue'],a)
   for s in (-1,1):town_path(m,[lp(x,y,s*(L/2+.3),.48,H-.2,a),lp(x,y,S(264.3),.48,T+.1,a)],.10,M['Blue'])
   facade_box(m,x,y,0,.39,.10,L,.08,.20,M['Plinth'],a)
 if 'roof' in Z[zone]:roof34(m,zone,M['Tile'],wm)
# The white house's roof: a saddle along the street over its main block, and a low roof over the
# notch behind the olive house and over the annex's back part.
m=meshes['SM_Kvarnholmen_House_90859904']
yF,yB,Hw,Tw=72.0,79.8,Z['wh']['height'],Z['wh']['top'];ym=(yF+yB)/2;sw=(Tw-Hw)/((yB-yF)/2)
for ya in (yF-.35,yB+.35):
 za=Hw-.35*sw;pts=[(239.05,ya,za),(254.5,ya,za),(254.5,ym,Tw),(239.05,ym,Tw)]
 (x0,y0,z0),(x1,y1,z1),(x2,y2,z2)=pts[:3];nz=(x1-x0)*(y2-y0)-(y1-y0)*(x2-x0)
 m.faces(pts,[(0,1,2,3) if nz>0 else (3,2,1,0)],M['Tile'])
for xx in (239.05,254.5):m.faces([(xx,yF,Hw),(xx,yB,Hw),(xx,ym,Tw)],[(0,1,2),(2,1,0)],M['White'])
m.prism([(239.05,79.9),(241.28,79.9),(241.28,82.1),(239.05,82.16)],Hw,Hw+.3,M['Dark'])
m.prism([(255.17,79.6),(256.3,79.6),(256.3,84.39),(255.23,84.4)],Z['yb']['height'],Z['yb']['height']+.3,M['Dark'])
x,y,L,a=sf_edge((241.0,72.1),(253.4,71.7))
roof_dormer(m,x,y,U({'p':(241.0,72.1),'q':(253.4,71.7)},249.5,71.8),a,Hw,sw,.6,1.0,1.2,M['RedDormer'],M['RedDormer'],WF,False)
box(m,246.0,76.0,.55,.7,1.0,Tw-.5,M['Tile'],0,M['Dark'])
# The red boarded wall with the gate and the stained-glass window, from the pass 76 house to the olive house.
m=meshes['SM_Kvarnholmen_House_90859833'];gp,gq=(229.5,72.3),(234.46,72.25);x,y,L,a=sf_edge(gp,gq)
S=lambda X:U({'p':gp,'q':gq},X,72.28)
gate=(S(231.3),.02,1.74,2.05,0);gl=(S(232.6),.72,.66,1.15,0)
bz_wall(m,gp,gq,0,2.22,[gate,gl],M['RedWall']);boards80(m,x,y,L,a,.1,2.15,[gate,gl],M['RedWall'],.24)
u,b,ww,hh,r=gate
for s in (-1,1):
 facade_box(m,x,y,u+s*ww/4,.10,b+hh/2,ww/2-.02,.06,hh,M['BrownGate'],a)
 for k in range(1,12):facade_box(m,x,y,u+s*ww/4,.14,b+k*hh/12,ww/2-.06,.02,.02,M['Dark'],a)
u,b,ww,hh,r=gl;facade_box(m,x,y,u,.2,b+hh/2,ww,.02,hh,M['Glass'],a)
for k in range(1,5):facade_box(m,x,y,u-ww/2+k*ww/5,.24,b+hh/2,.02,.02,hh,M['Dark'],a)
for k in range(1,8):facade_box(m,x,y,u,.24,b+k*hh/8,ww,.02,.02,M['Dark'],a)
surround36(m,x,y,u,b,ww,hh,a,M['RedWall'],.08,.40)
facade_box(m,x,y,0,.25,2.28,L+.1,.60,.12,M['Dark'],a)
# The blue boarded fence and the red gate beside the cottage.
m=meshes['SM_Kvarnholmen_House_90859883']
for p,q,hh,ma in (((261.0,71.75),(262.3,71.73),1.9,M['Blue']),((266.3,71.68),(267.05,71.67),1.6,M['Red'])):
 x,y,L,a=sf_edge(p,q);facade_box(m,x,y,0,.30,hh/2,L,.06,hh,ma,a)
 for k in range(1,int(L/.16)):facade_box(m,x,y,-L/2+k*L/int(L/.16),.34,hh/2,.03,.03,hh,M['Dark'],a)
for nm,osm in (('SM_Kvarnholmen_House_90859833','90859833'),('SM_Kvarnholmen_House_90859904','90859904'),('SM_Kvarnholmen_House_90859843','90859843'),('SM_Kvarnholmen_House_90859883','90859883')):b80_finish(meshes[nm],osm)

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block80_cameras=[
 sv_camera('396_Block80_Cal_Gate',230.44,68.6-.355,1.95,332,10,90),
 sv_camera('397_Block80_Cal_Olive',230.44,68.6-.355,1.95,22,10,90),
 sv_camera('398_Block80_Cal_Red',262.47,67.95-.355,1.95,332,10,90),
 sv_camera('399_Block80_Cal_White',262.47,67.95-.355,1.95,282,10,90),
 ('400_Block80_Aerial',(250.0,58.0,24.0),(250.0,78.0,2.0),28),
]
print('BLOCK80_GEOMETRY',len(block80_names))
