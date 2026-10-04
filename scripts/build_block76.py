"""Pass 76: the district volumes 90859889, 90859896 and 90859844 on the north side of Norra
Långgatan, opposite pass 75:
- the green boarded cottage: red-framed windows in white surrounds, white corner boards, a cross
  gable towards the street and a tile roof;
- the two carriage gates (57 and 59), blue and grey with chevron boarding between white posts, in
  front of a yard;
- the red boarded house with white windows, white corner boards and a chimney with a red cowl;
- the red boarded house with green-framed windows, the orange chevron door (61) up a stone step,
  and two brick chimneys;
- a narrow red boarded passage door;
- the white roughcast house with its off-centre gable to the street, red windows and red barge
  boards, and a low annex behind.

References: Google Street View April 2025 (the two pass 75 panoramas on Norra Långgatan, resected
there, looking across the street), view only. Zones: source/block76.json; see
references/block76-notes.md. The traffic sign and the lamps are omitted.
"""
B76D=json.loads((R/'source/block76.json').read_text());Z=B76D['zones']
block76_names=[];B76={}
for old in [k for k in list(materials) if k.startswith('M_Block76_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Green','TownIvory',(.66,.80,.56),.80,0),
 ('Red','TownIvory',(.62,.22,.17),.82,0),
 ('White','TownIvory',(.95,.95,.93),.82,0),
 ('WhiteWall','TownIvory',(.93,.93,.91),.94,0),
 ('RedFrame','TownPaintBrown',(.62,.20,.16),.55,0),
 ('GreenFrame','TownPaintGreen',(.42,.48,.32),.55,0),
 ('Orange','TownPaintBrown',(.90,.58,.22),.55,0),
 ('Blue','TownPaintWhite',(.33,.55,.80),.60,0),
 ('GreyGate','TownPaintWhite',(.72,.70,.68),.60,0),
 ('Plinth','TownStone',(.55,.55,.55),.90,0),
 ('Stone','TownStone',(.70,.69,.66),.88,0),
 ('Tile','TownTileRed',(.64,.33,.24),.80,0),
 ('Brick','TownTileRed',(.62,.30,.22),.85,0),
 ('Dark','TownMetalGrey',(.05,.055,.06),.40,.20),
 ]:
 name='M_Block76_'+key;B76[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block76_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B76;WH=M['White']

def b76_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block76_names.append(name);return Mesh(name,category)
def b76_finish(m,osm):
 obj=s21_finish(m);obj['detail_pass']=76;obj['reference_notes']='references/block76-notes.md';obj['osm_way']=osm;return obj
def cas76(m,x,y,u,b,w,h,a,frame,o=.16,rows=3):
 facade_box(m,x,y,u,o-.04,b+h/2,w,.02,h,GLAZE,a)
 for q in (-w/2+.04,w/2-.04,0):facade_box(m,x,y,u+q,o,b+h/2,.08 if q else .05,.08,h,frame,a)
 for k in range(rows+1):facade_box(m,x,y,u,o,b+.04+k*(h-.08)/rows,w,.08 if k in (0,rows) else .05,.06 if k in (0,rows) else .04,frame,a)
def win76(m,x,y,wins,a,frame,surround):
 for u,b,ww,hh,r in wins:
  cas76(m,x,y,u,b,ww,hh,a,frame);surround36(m,x,y,u,b,ww,hh,a,surround,.11,.40)
  facade_box(m,x,y,u,.47,b-.06,ww+.30,.16,.06,surround,a)
def battens76(m,x,y,L,a,z0,z1,holes,ma,step=.22):
 n=int(L/step)
 for k in range(1,n):
  u=-L/2+k*L/n;segs=[(z0,z1)]
  for hu,hb,hw,hh,hr in holes:
   if abs(u-hu)<hw/2+.15:segs=[(l0,h0) for l,h_ in segs for l0,h0 in ((l,min(h_,hb-.14)),(max(l,hb+hh+.16),h_)) if h0-l0>.05]
  for l0,h0 in segs:facade_box(m,x,y,u,.37,(l0+h0)/2,.035,.03,h0-l0,ma,a)
def quad76(m,pts,ma,up=True):
 # A single roof or wall face; wound so that its normal points up (or towards the street).
 (x0,y0,z0),(x1,y1,z1),(x2,y2,z2)=pts[:3]
 nz=(x1-x0)*(y2-y0)-(y1-y0)*(x2-x0)
 m.faces(pts,[tuple(range(len(pts))) if (nz>0)==up else tuple(range(len(pts)-1,-1,-1))],ma)
def saddle76(m,x0,x1,yf,yb,H,top,ma,wall,ov=.35,gable_ends=True):
 # A saddle roof with its ridge along the street, gable triangles at both ends.
 ym=(yf+yb)/2;s=(top-H)/((yb-yf)/2)
 for ya,yr in ((yf-ov,ym),(yb+ov,ym)):
  za=H-ov*s
  pts=[(x0-.2,ya,za),(x1+.2,ya,za),(x1+.2,ym,top),(x0-.2,ym,top)]
  quad76(m,pts,ma)
 if gable_ends:
  for xx in (x0,x1):
   tri=[(xx,yf,H),(xx,yb,H),(xx,ym,top)];m.faces(tri,[(0,1,2),(2,1,0)],wall)
def gable76(m,x,y,u,a,H,gw,rise,depth,wall,roof,ov=.30):
 # A cross gable standing on the street front: the gable triangle in the wall plane and two roof
 # planes running back into the main roof.
 tri=[lp(x,y,u-gw/2,.355,H,a),lp(x,y,u+gw/2,.355,H,a),lp(x,y,u,.355,H+rise,a)]
 m.faces(tri,[(0,1,2),(2,1,0)],wall)
 for s in (-1,1):
  q=[lp(x,y,u+s*(gw/2+ov),.355+ov,H-ov*rise/(gw/2),a),lp(x,y,u,.355+ov,H+rise,a),lp(x,y,u,.355-depth,H+rise,a),lp(x,y,u+s*(gw/2+ov),.355-depth,H-ov*rise/(gw/2),a)]
  m.faces(q,[(0,1,2,3),(3,2,1,0)],roof)
 town_path(m,[lp(x,y,u-gw/2-.2,.45,H-.1,a),lp(x,y,u,.45,H+rise+.08,a),lp(x,y,u+gw/2+.2,.45,H-.1,a)],.07,WH)
def chimney76(m,cx,cy,z0,h,ma,cowl=None):
 box(m,cx,cy,.55,.60,h,z0,ma,0,M['Dark'])
 if cowl:town_rod(m,(cx,cy,z0+h+.05),(cx,cy,z0+h+.75),.13,cowl,10)

meshes={nm:b76_new(nm,'Kvarnholmen/Norra Långgatan') for nm in ('SM_Kvarnholmen_House_90859889','SM_Kvarnholmen_House_90859896','SM_Kvarnholmen_House_90859844')}
def yf76(X):return 72.548+(X-188.517)*(71.945-72.548)/(229.5-188.517)
for zone in ('gr','rw','re','ps','ww','bk'):
 m=meshes[Z[zone]['mesh']];H=Z[zone]['height']
 wallm={'gr':M['Green'],'rw':M['Red'],'re':M['Red'],'ps':M['Red'],'ww':M['WhiteWall'],'bk':M['WhiteWall']}[zone]
 for w in walls(zone):
  x,y,L,a=sf_edge(w['p'],w['q']);ox,oy=outward(w)
  front=w['kind']=='outer' and oy<-.9 and max(w['p'][1],w['q'][1])<72.7
  if not front:
   if w['kind']=='outer':plain(m,w,H,wallm,M['RedFrame'] if zone in ('ww','bk','rw') else M['GreenFrame'],WH,1,.6)
   else:bz_wall(m,w['p'],w['q'],w['z0'],H,[],wallm)
   continue
  S=lambda X:U(w,X,yf76(X))
  if zone=='gr':
   gf=[(S(X0),.50,ww,1.30,0) for X0,ww in ((192.66,1.08),(195.67,1.12),(197.39,1.14))]
   up=[(S(X0),2.42,ww,.82,0) for X0,ww in ((195.64,.88),(197.36,.91))]+[(S(192.66),2.50,1.0,.95,0)]
   bz_wall(m,w['p'],w['q'],0,H,gf+up,wallm);battens76(m,x,y,L,a,.30,H-.05,gf+up,wallm)
   win76(m,x,y,gf+up,a,M['RedFrame'],WH)
   for X0 in (188.6,194.3,197.0):facade_box(m,x,y,S(X0),.42,(.3+H)/2,.20,.10,H-.3,WH,a)
   facade_box(m,x,y,0,.39,.15,L,.08,.30,M['Plinth'],a);facade_box(m,x,y,0,.44,H-.08,L+.1,.14,.16,WH,a)
   gable76(m,x,y,S(192.3),a,H,4.0,1.45,2.2,wallm,M['Tile'])
  elif zone in ('rw','re'):
   if zone=='rw':
    gf=[(S(X0),.86,1.30,1.28,0) for X0 in (204.35,207.45)];up=[(S(X0),2.94,1.26,.94,0) for X0 in (204.35,207.45)];door=None;fr=WH
   else:
    gf=[(S(X0),.86,1.22,1.28,0) for X0 in (210.9,212.25,213.76,215.9,217.38)]
    up=[(S(X0),2.94,1.08,.94,0) for X0 in (210.9,212.15,213.8,215.93,217.47,219.96)];door=(S(219.85),.35,1.30,1.60,0);fr=M['GreenFrame']
   bz_wall(m,w['p'],w['q'],0,H,gf+up+([door] if door else []),wallm);battens76(m,x,y,L,a,.30,H-.05,gf+up+([door] if door else []),wallm)
   win76(m,x,y,gf+up,a,fr,fr)
   if door:
    u,b,ww,hh,r=door
    for s in (-1,1):
     facade_box(m,x,y,u+s*ww/4,.10,b+hh/2,ww/2-.02,.06,hh,M['Orange'],a)
     facade_box(m,x,y,u+s*ww/4,.14,b+hh*.78,.22,.03,.22,M['Dark'],a)
    surround36(m,x,y,u,b,ww,hh,a,fr,.14,.40);steps36(m,x,y,u,a,1.8,1.6,b,2,.40,M['Stone'])
   for uu in (-L/2+.1,L/2-.1):facade_box(m,x,y,uu,.42,(.3+H)/2,.20,.10,H-.3,WH if zone=='rw' else M['Red'],a)
   facade_box(m,x,y,0,.39,.15,L,.08,.30,M['Dark'],a);facade_box(m,x,y,0,.44,H-.08,L+.1,.14,.16,M['Red'],a)
  elif zone=='ps':
   bz_wall(m,w['p'],w['q'],0,H,[],wallm)
   facade_box(m,x,y,0,.40,1.1,L-.1,.06,2.0,M['Red'],a)
   for k in range(1,4):facade_box(m,x,y,-L/2+k*L/4,.44,1.1,.03,.03,2.0,M['Dark'],a)
  elif zone=='ww':
   gf=[(S(X0),1.11,ww,1.08,0) for X0,ww in ((223.93,.94),(225.41,.96),(228.12,1.02))]
   up=[(S(X0),3.02,ww,1.12,0) for X0,ww in ((223.87,.91),(225.36,.94))]
   bz_wall(m,w['p'],w['q'],0,H,gf,wallm)
   win76(m,x,y,gf,a,M['RedFrame'],M['RedFrame'])
   # The upper windows sit in the gable slab (drawn with the roof): glass and frames in front of it.
   for u,b,ww,hh,r in up:
    facade_box(m,x,y,u,.37,b+hh/2,ww,.02,hh,GLAZE,a);cas76(m,x,y,u,b,ww,hh,a,M['RedFrame'],.40)
    surround36(m,x,y,u,b,ww,hh,a,M['RedFrame'],.11,.44);facade_box(m,x,y,u,.50,b-.06,ww+.30,.16,.06,M['RedFrame'],a)
   facade_box(m,x,y,0,.39,.14,L,.08,.28,M['Plinth'],a)
  elif zone=='bk':
   bz_wall(m,w['p'],w['q'],0,H,[],wallm);facade_box(m,x,y,0,.39,.14,L,.08,.28,M['Plinth'],a)
 # Roofs.
 if zone=='gr':
  saddle76(m,188.5,197.12,72.5,76.9,H,Z[zone]['top'],M['Tile'],wallm)
  rest=[g for g in Z[zone]['polygons']]
  inset_roof(m,[(196.24,76.86),(196.27,79.84),(198.3,79.81),(198.3,83.11),(188.64,83.22),(188.6,76.9)],H,1.6,.9,M['Tile'],.30)
  chimney76(m,193.0,74.7,H+.9,1.1,M['WhiteWall'])
 elif zone=='rw':
  saddle76(m,202.3,209.7,72.3,78.2,H,Z[zone]['top'],M['Tile'],wallm)
  chimney76(m,204.9,75.2,Z[zone]['top']-.4,.9,WH,M['RedFrame'])
 elif zone=='re':
  saddle76(m,209.7,221.82,72.15,78.1,H,Z[zone]['top'],M['Tile'],wallm)
  box(m,221.56,79.5,.5,2.9,.2,H,M['Dark'])
  for cx in (214.1,218.3):chimney76(m,cx,75.1,Z[zone]['top']-.4,.9,M['Brick'],M['RedFrame'])
 elif zone=='ps':
  box(m,222.13,75.2,.75,6.6,.12,H,M['Dark'])
 elif zone=='ww':
  # The off-centre gable: eaves 3.93 on the west side and 2.82 on the east, apex 5.76 at x 224.74.
  ax,az=224.74,5.76
  for yy,out in ((72.0,-.35),(78.4,.35)):
   prof=[(222.45,2.8),(229.5,2.8),(229.5,2.82),(ax,az),(222.45,3.93)]
   vs=[(xx,yy+o,zz) for o in (0,out) for xx,zz in prof];nn=len(prof)
   m.faces(vs,[tuple(range(nn-1,-1,-1)),tuple(range(nn,2*nn))]+[(i,(i+1)%nn,(i+1)%nn+nn,i+nn) for i in range(nn)],wallm)
  bz_wall(m,(222.45,78.4),(222.45,72.044),2.8,3.93,[],wallm)
  sW=(az-3.93)/(ax-222.45);sE=(az-2.82)/(229.5-ax)
  quad76(m,[(222.15,71.6,3.93-.3*sW),(ax,71.6,az),(ax,78.8,az),(222.15,78.8,3.93-.3*sW)],M['Tile'])
  quad76(m,[(ax,71.6,az),(229.8,71.6,2.82-.3*sE),(229.8,78.8,2.82-.3*sE),(ax,78.8,az)],M['Tile'])
  for yy in (71.58,78.82):town_path(m,[(222.15,yy,3.93-.3*sW),(ax,yy,az+.05),(229.8,yy,2.82-.3*sE)],.08,M['RedFrame'])
  chimney76(m,225.6,77.0,az-.9,1.2,M['Brick'])
 elif zone=='bk':
  for g in Z[zone]['polygons']:
   pts=simplify([tuple(v) for v in g],.3)
   inset_roof(m,pts,H,min(1.5,.45*min(math.dist(p,q) for p,q in zip(pts,pts[1:]+pts[:1]))),Z[zone]['top']-H,M['Tile'],.25)
# The two carriage gates in the released strip between the green and the red houses.
m=meshes['SM_Kvarnholmen_House_90859896'];gp,gq=(198.3,72.42),(202.3,72.34);x,y,L,a=sf_edge(gp,gq)
S=lambda X:U({'p':gp,'q':gq},X,72.38)
for X0,ww in ((198.37,.16),(200.29,.28),(202.2,.2)):facade_box(m,x,y,S(X0),.20,1.15,ww,.22,2.3,WH,a)
facade_box(m,x,y,0,.20,2.26,L,.26,.10,WH,a)
for X0,X1,ma in ((198.45,200.15,M['Blue']),(200.43,202.1,M['GreyGate'])):
 c=S((X0+X1)/2);ww=abs(S(X1)-S(X0))
 facade_box(m,x,y,c,.12,1.06,ww,.06,2.1,ma,a);facade_box(m,x,y,c,.16,1.06,.03,.03,2.1,M['Dark'],a)
 for k in range(1,7):facade_box(m,x,y,c,.16,k*.30,ww,.02,.02,M['Dark'],a)
for nm,osm in (('SM_Kvarnholmen_House_90859889','90859889'),('SM_Kvarnholmen_House_90859896','90859896'),('SM_Kvarnholmen_House_90859844','90859844')):b76_finish(meshes[nm],osm)

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block76_cameras=[
 sv_camera('378_Block76_Cal_Gates',201.67,68.51-.355,1.95,332,10,90),
 sv_camera('379_Block76_Cal_Green',201.67,68.51-.355,1.95,282,10,90),
 sv_camera('380_Block76_Cal_RedWest',201.67,68.51-.355,1.95,22,10,90),
 sv_camera('381_Block76_Cal_RedEast',221.59,68.39-.355,1.97,282,10,90),
 sv_camera('382_Block76_Cal_White',221.59,68.39-.355,1.97,12,10,90),
 ('383_Block76_Aerial',(210.0,58.0,24.0),(210.0,78.0,2.0),28),
]
print('BLOCK76_GEOMETRY',len(block76_names))
