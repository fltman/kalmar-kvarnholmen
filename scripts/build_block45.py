"""Pass 45: the district volumes 92379262 and 92379314 on the south side of Ölandsgatan, from Västra
Sjögatan westwards:
- the yellow two-storey house: five axes of white-framed casements of many panes in flat surrounds
  on both storeys, a blank panel between the storeys over the middle axis, a grey plinth, a moulded
  cornice and a tile roof hipped to the street; three axes on its east end to Västra Sjögatan;
- the one-storey entrance link: a relief panel over the green double door in a stone surround on
  two steps, a flat cornice, a glazed storey set back above;
- the beige house of 1909: a long one-storey range with six windows in pale surrounds, a curved
  front gable at each end over two windows (the western with an arched window of many panes), three
  dormers in the tile roof between them, the date on the wall;
- the plain beige two-storey house (Frösunda): three large windows on each storey, three small
  windows on each storey, the glazed entrance under a sign board, a tile roof.
The Södra Vallgatan side and the courtyard wings stay plain (district heights).

References: Google Street View April 2025 (four panoramas chained along the street, anchored on the
Västra Sjögatan corner), view only. Zones: source/block45.json; see references/block45-notes.md.
The date figures, the relief's subject, the signs and the lettering are omitted.
"""
B45D=json.loads((R/'source/block45.json').read_text());Z=B45D['zones']
block45_names=[];B45={}
for old in [k for k in list(materials) if k.startswith('M_Block45_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Yellow','TownIvory',(.93,.80,.45),.88,0),
 ('Beige','TownIvory',(.86,.81,.70),.90,0),
 ('Cream','TownIvory',(.88,.85,.77),.90,0),
 ('White','TownIvory',(.94,.94,.91),.82,0),
 ('Stone','TownStone',(.78,.74,.66),.86,0),
 ('Frame','TownPaintWhite',(.93,.93,.91),.55,0),
 ('GreyFrame','TownPaintBrown',(.55,.58,.58),.55,0),
 ('Green','TownPaintBrown',(.20,.28,.24),.55,0),
 ('Brown','TownPaintBrown',(.35,.22,.16),.60,0),
 ('Plinth','TownStone',(.52,.52,.51),.82,0),
 ('Tile','TownTileRed',(.58,.28,.20),.80,0),
 ('Iron','TownMetalGrey',(.05,.05,.055),.45,.40),
 ('Dark','TownMetalGrey',(.05,.055,.06),.40,.20),
 ]:
 name='M_Block45_'+key;B45[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block45_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B45;WH=M['White']

def b45_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block45_names.append(name);return Mesh(name,category)
def b45_finish(m,osm):
 obj=s21_finish(m);obj['detail_pass']=45;obj['reference_notes']='references/block45-notes.md';obj['osm_way']=osm;return obj
def kind45(w):
 ox,oy=outward(w)
 if w['kind']!='outer':return None
 if oy>.9 and max(w['p'][1],w['q'][1])>-152.2:return 'olands'
 if ox>.9 and min(w['p'][0],w['q'][0])>-41:return 'vsj'
 return None
def xf45(X):return -151.977+(X+40.688)*(-151.463+151.977)/(-90.599+40.688)
def pane45(m,x,y,u,b,w,h,a,frame=None,cols=4,rows=4,o=.18):
 # A white casement of small panes (two leaves, glazing bars in a grid).
 frame=frame or M['Frame']
 facade_box(m,x,y,u,o-.04,b+h/2,w,.02,h,GLAZE,a)
 for q in (-w/2+.04,w/2-.04,0):facade_box(m,x,y,u+q,o,b+h/2,.08,.08,h,frame,a)
 for zz in (b+.04,b+h-.04):facade_box(m,x,y,u,o,zz,w,.08,.08,frame,a)
 for j in range(1,rows):facade_box(m,x,y,u,o+.01,b+j*h/rows,w,.04,.03,frame,a)
 for j in range(1,cols):
  if j*2!=cols:facade_box(m,x,y,u-w/2+j*w/cols,o+.01,b+h/2,.03,.04,h,frame,a)
 facade_box(m,x,y,u,.40,b-.03,w+.12,.20,.05,M['Dark'],a)
def cornice45(m,x,y,L,a,H,ma,out=.45):
 facade_box(m,x,y,0,.40,H-.35,L,.10,.30,ma,a);facade_box(m,x,y,0,.36+out/2,H-.10,L+.10,out,.20,ma,a)
def curved_gable45(m,x,y,uc,base,W,apex,a,body,trim):
 # A curved (Jugend) front gable in the wall face: shoulders, concave sides, a short flat top.
 half=[(-W/2,base),(-W/2,base+.35)]
 for i in range(1,9):t=i/8;half.append((-W/2*(1-.78*t**1.3),base+.35+(apex-base-.55)*t))
 prof=half+[(-W/2*.2,apex),(W/2*.2,apex)]+[(-uu,zz) for uu,zz in reversed(half)]
 prof=[(uc+uu,zz) for uu,zz in prof]
 vs=[lp(x,y,uu,o,zz,a) for o in (.005,.355) for uu,zz in prof];nn=len(prof)
 m.faces(vs,[tuple(range(nn-1,-1,-1)),tuple(range(nn,2*nn))]+[(i,(i+1)%nn,(i+1)%nn+nn,i+nn) for i in range(nn)],body)
 town_path(m,[lp(x,y,uu,.40,zz+.05,a) for uu,zz in prof[1:-1]],.06,trim)
 # The gable's roof runs back 2.4 m; a back triangle closes it.
 tri=[lp(x,y,uc-W/2,-2.4,base+.2,a),lp(x,y,uc+W/2,-2.4,base+.2,a),lp(x,y,uc,-2.4,apex-.1,a)]
 m.faces(tri,[(2,1,0)],body)
 for s in (-1,1):
  sd=[lp(x,y,uc+s*W/2,.005,base,a),lp(x,y,uc+s*W/2,-2.4,base+.2,a),lp(x,y,uc+s*W/2,.005,base+.35,a)]
  m.faces(sd,[(0,1,2) if s>0 else (2,1,0)],body)
 for s in (-1,1):
  q=[lp(x,y,uc+s*W/2,.2,base+.2,a),lp(x,y,uc,.2,apex-.1,a),lp(x,y,uc,-2.4,apex-.1,a),lp(x,y,uc+s*W/2,-2.4,base+.2,a)]
  m.faces(q,[(0,1,2,3) if s<0 else (3,2,1,0)],M['Tile'])

meshes={'SM_Kvarnholmen_House_92379262':b45_new('SM_Kvarnholmen_House_92379262','Kvarnholmen/Ölandsgatan south'),
 'SM_Kvarnholmen_House_92379314':b45_new('SM_Kvarnholmen_House_92379314','Kvarnholmen/Ölandsgatan south')}
for zone in Z:
 m=meshes[Z[zone]['mesh']];HZ=Z[zone]['height']
 wall={'yl':M['Yellow'],'ln':M['Yellow'],'h9':M['Beige'],'fr':M['Cream']}.get(zone,M['Cream'])
 for w in walls(zone):
  k=kind45(w);x,y,L,a=sf_edge(w['p'],w['q'])
  if zone=='yl' and k=='olands':
   S=lambda X:U(w,X,xf45(X))
   AX=[(-41.54,-43.05),(-43.81,-45.36),(-46.29,-47.75),(-48.64,-50.11),(-50.92,-52.42)]
   gf=[(S((x0+x1)/2),1.43,abs(x1-x0)-.24,1.56,0) for x0,x1 in AX]
   up=[(S((x0+x1)/2),4.73,abs(x1-x0)-.24,1.45,0) for x0,x1 in AX]
   bz_wall(m,w['p'],w['q'],0,HZ,gf+up,wall)
   for u,b,ww,hh,r in gf+up:surround36(m,x,y,u,b,ww,hh,a,WH,.12,.39);pane45(m,x,y,u,b,ww,hh,a,None,4,4)
   facade_box(m,x,y,S(-47.02),.38,3.85,1.30,.04,.75,M['Cream'],a)
   plinth36(m,x,y,L,a,[],.55,M['Plinth'])
   cornice45(m,x,y,L,a,HZ,WH,.50)
  elif zone=='yl' and k=='vsj':
   n=3;ops=[(-L/2+(j+.5)*L/n,b,1.15,hh,0) for j in range(n) for b,hh in ((1.43,1.56),(4.73,1.45))]
   bz_wall(m,w['p'],w['q'],0,HZ,ops,wall)
   for u,b,ww,hh,r in ops:surround36(m,x,y,u,b,ww,hh,a,WH,.12,.39);pane45(m,x,y,u,b,ww,hh,a,None,4,4)
   plinth36(m,x,y,L,a,[],.55,M['Plinth']);cornice45(m,x,y,L,a,HZ,WH,.50)
  elif zone=='ln' and k=='olands':
   S=lambda X:U(w,X,xf45(X));du=S(-54.42)
   bz_wall(m,w['p'],w['q'],0,HZ,[(du,.28,1.00,2.62,0)],wall)
   for s in (-1,1):facade_box(m,x,y,du+s*.62,.42,1.60,.24,.14,2.70,M['Stone'],a)
   facade_box(m,x,y,du,.44,3.00,1.50,.16,.16,M['Stone'],a)
   facade_box(m,x,y,du,.42,3.55,1.40,.10,.85,M['Cream'],a)
   for j in range(5):town_path(m,[lp(x,y,du-.45+j*.22,.48,3.40+.18*math.sin(j),a),lp(x,y,du-.35+j*.22,.48,3.70,a)],.04,M['Cream'])
   facade_box(m,x,y,du,.20,1.59,1.00,.06,2.62,M['Green'],a);facade_box(m,x,y,du,.24,1.59,.04,.05,2.62,M['Dark'],a)
   for s in (-1,1):facade_box(m,x,y,du+s*.25,.18,2.25,.28,.02,.9,GLAZE,a)
   for j in range(2):facade_box(m,x,y,du,.355+(2-j)*.20,.07*(j+1),1.60,(2-j)*.40,.14*(j+1),M['Stone'],a)
   plinth36(m,x,y,L,a,[(du-.8,du+.8)],.45,M['Plinth'])
   cornice45(m,x,y,L,a,HZ,M['Cream'],.40)
   # The glazed storey set back 0.8 m above the link.
   x2,y2,_=lp(x,y,0,-.8,0,a);facade_box(m,x2,y2,0,.2,HZ+.5,L-.2,.1,1.0,M['Cream'],a)
   for j in range(3):pane45(m,x2,y2,-L/2+.5+j*(L-1)/2.0,HZ+.12,.70,.70,a,None,2,2,.25)
  elif zone=='h9' and k=='olands':
   S=lambda X:U(w,X,xf45(X))
   AX=[(-56.79,-58.29),(-58.74,-60.24),(-61.59,-63.09),(-64.27,-65.73),(-66.92,-68.39),(-69.57,-71.06),(-72.18,-73.67),(-74.81,-76.44)]
   gf=[(S((x0+x1)/2),1.28,abs(x1-x0)-.26,1.84,0) for x0,x1 in AX]
   bz_wall(m,w['p'],w['q'],0,HZ,gf,wall)
   for u,b,ww,hh,r in gf:surround36(m,x,y,u,b,ww,hh,a,M['Cream'],.13,.39);pane45(m,x,y,u,b,ww,hh,a,M['GreyFrame'],4,5)
   plinth36(m,x,y,L,a,[],.45,M['Plinth'])
   cornice45(m,x,y,L,a,HZ,M['Cream'],.40)
   for X in (-61.5,-67.0,-72.3):town_rod(m,lp(x,y,S(X),.48,.25,a),lp(x,y,S(X),.48,HZ,a),.05,WH,8)
   # The two curved front gables: east (x -56.3/-60.8, two windows) and west (x -70.55/-75.29,
   # an arched window of many panes).
   ge=S(-58.55);curved_gable45(m,x,y,ge,HZ-.1,abs(S(-60.82)-S(-56.3)),8.1,a,wall,M['Cream'])
   for q in (-.62,.62):pane45(m,x,y,ge+q,5.62,.70,1.15,a,M['GreyFrame'],2,3,.40)
   gw=S(-72.95);curved_gable45(m,x,y,gw,HZ-.1,abs(S(-75.29)-S(-70.55)),8.3,a,wall,M['Cream'])
   pane45(m,x,y,gw,5.12,1.45,1.05,a,M['GreyFrame'],4,3,.40)
   k_=14;cz=6.17;m.faces([lp(x,y,gw+.725*math.cos(math.pi*i/k_),.36,cz+.40*math.sin(math.pi*i/k_),a) for i in range(k_+1)],[tuple(range(k_+1))],GLAZE)
   town_path(m,[lp(x,y,gw+.80*math.cos(math.pi*i/k_),.42,cz+.46*math.sin(math.pi*i/k_),a) for i in range(k_+1)],.05,M['Cream'])
  elif zone=='fr' and k=='olands':
   S=lambda X:U(w,X,xf45(X))
   big=[(-77.92,-79.50),(-79.87,-81.46),(-81.81,-83.41)];small=[(-83.93,-84.78),(-84.96,-85.78),(-85.99,-86.81)]
   gf=[(S((x0+x1)/2),1.31,abs(x1-x0)-.20,1.22,0) for x0,x1 in big]+[(S((x0+x1)/2),1.40,abs(x1-x0)-.18,.70,0) for x0,x1 in small]
   up=[(S((x0+x1)/2),4.50,abs(x1-x0)-.22,1.05,0) for x0,x1 in ((-77.99,-79.41),(-79.98,-81.37),(-81.83,-83.30))]+[(S((x0+x1)/2),4.86,abs(x1-x0)-.18,.60,0) for x0,x1 in ((-86.45,-87.17),(-87.45,-88.24),(-88.46,-89.25))]
   door=(S(-87.70),0,1.25,2.50,0)
   bz_wall(m,w['p'],w['q'],0,HZ,gf+up+[door],wall)
   for u,b,ww,hh,r in gf+up:surround36(m,x,y,u,b,ww,hh,a,WH,.10,.39);pane45(m,x,y,u,b,ww,hh,a,M['Brown'],1,1)
   du,db,dw,dh,_=door;s21_glass(m,x,y,du,db,dw,dh,a,M['Brown'],1,.80,True)
   facade_box(m,x,y,du,.46,2.85,1.40,.12,.50,M['White'],a)
   plinth36(m,x,y,L,a,[(du-.7,du+.7)],.35,M['Plinth'])
   cornice45(m,x,y,L,a,HZ,M['Cream'],.40)
  else:
   if w['kind']=='outer':plain(m,w,HZ,wall,M['Brown'],WH,1 if HZ<5 else 2,.9)
   else:bz_wall(m,w['p'],w['q'],w['z0'],HZ,[],wall)
m62,m14=meshes['SM_Kvarnholmen_House_92379262'],meshes['SM_Kvarnholmen_House_92379314']
roof34(m62,'yl',M['Tile'],M['Yellow'])
sl9=roof34(m62,'h9',M['Tile'],M['Beige'])
roof34(m14,'fr',M['Tile'],M['Cream'])
for zone,mm,ma in (('ln',m62,M['Tile']),('bk62',m62,M['Tile']),('bk14',m14,M['Tile'])):
 for g in Z[zone]['polygons']:
  pts=simplify([tuple(v) for v in g],.8)
  inset_roof(mm,pts,Z[zone]['height']+(1.2 if zone=='ln' else 0),min(2.0,.45*min(math.dist(p,q) for p,q in zip(pts,pts[1:]+pts[:1]))),1.0 if zone=='ln' else 2.2,ma,.30)
for w in walls('h9'):
 if kind45(w)=='olands':
  x,y,L,a=sf_edge(w['p'],w['q'])
  for X in (-62.4,-64.9,-67.4):roof_dormer(m62,x,y,U(w,X,xf45(X)),a,Z['h9']['height'],sl9,.6,.95,.55,M['Stone'],M['Tile'],WH,False)
for cx,cy in ((-49.0,-158.0),(-63.5,-157.0),(-84.0,-158.0)):box(m62 if cx>-77 else m14,cx,cy,.60,.85,1.2,(Z['yl']['top'] if cx>-53 else Z['h9']['top'] if cx>-77 else Z['fr']['top'])-.4,M['Brown'],0,M['Dark'])
b45_finish(m62,'92379262');b45_finish(m14,'92379314')

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
# Chained camera positions (distance from the real facade; 0.355 m added for the model's wall).
_C={'A':(-48.54,4.84,2.36),'E':(-58.69,5.21,2.24),'B':(-69.13,5.11,2.36),'C':(-79.56,5.16,2.36)}
def _cam(n):X,D_,h=_C[n];return X,xf45(X)+.355+D_,h
block45_cameras=[
 sv_camera('275_Block45_Cal_Yellow',*_cam('A'),152,5,90),
 sv_camera('276_Block45_Cal_Link',*_cam('E'),152,10,90),
 sv_camera('277_Block45_Cal_1909',*_cam('B'),152,5,90),
 sv_camera('278_Block45_Cal_Frosunda',*_cam('C'),152,5,90),
 ('279_Block45_Aerial',(-65.0,-128.0,30.0),(-65.0,-160.0,4.0),28),
]
print('BLOCK45_GEOMETRY',len(block45_names))
