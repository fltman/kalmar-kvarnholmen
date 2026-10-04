"""Pass 77: the district volumes 93192402 and 93192406 on the south side of Norra Långgatan, east of
pass 75:
- the red boarded cottage with its gable to the street: grey weathered corner and barge boards,
  two yellow-framed windows in grey surrounds below and one in the gable;
- the yellow rendered apartment block: a grey plinth with cellar windows, a raised ground floor,
  white-framed windows, the recessed entrance with the stair window over it, recessed loggias with
  white balcony fronts at both ends, a cornice and a tile roof;
- the iron gate between the cottage and the pass 75 range.

References: Google Street View April 2025 (one panorama on Norra Långgatan, resected on both corners
of the cottage, in two headings), view only. Zones: source/block77.json; see
references/block77-notes.md. The meter cabinet and the lamp are omitted.
"""
B77D=json.loads((R/'source/block77.json').read_text());Z=B77D['zones']
block77_names=[];B77={}
for old in [k for k in list(materials) if k.startswith('M_Block77_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Red','TownIvory',(.62,.20,.16),.82,0),
 ('Weathered','TownIvory',(.52,.50,.47),.90,0),
 ('Yellow','TownIvory',(.86,.72,.45),.94,0),
 ('White','TownIvory',(.95,.95,.93),.84,0),
 ('WhiteFrame','TownPaintWhite',(.95,.95,.93),.55,0),
 ('YellowFrame','TownPaintBrown',(.86,.66,.32),.55,0),
 ('GreySurround','TownIvory',(.78,.80,.82),.85,0),
 ('Plinth','TownIvory',(.60,.60,.58),.92,0),
 ('Tile','TownTileRed',(.55,.30,.24),.80,0),
 ('Iron','TownMetalGrey',(.08,.08,.085),.45,.40),
 ('Dark','TownMetalGrey',(.05,.055,.06),.40,.20),
 ]:
 name='M_Block77_'+key;B77[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block77_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B77;WH=M['White']

def b77_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block77_names.append(name);return Mesh(name,category)
def b77_finish(m,osm):
 obj=s21_finish(m);obj['detail_pass']=77;obj['reference_notes']='references/block77-notes.md';obj['osm_way']=osm;return obj
def cas77(m,x,y,u,b,w,h,a,frame,o=.16,rows=3,mull=True):
 facade_box(m,x,y,u,o-.04,b+h/2,w,.02,h,GLAZE,a)
 for q in ((-w/2+.04,w/2-.04,0) if mull else (-w/2+.04,w/2-.04)):facade_box(m,x,y,u+q,o,b+h/2,.08 if q else .05,.08,h,frame,a)
 for k in range(rows+1):facade_box(m,x,y,u,o,b+.04+k*(h-.08)/rows,w,.08 if k in (0,rows) else .05,.06 if k in (0,rows) else .04,frame,a)
def yn77(X):return 61.711+(X-229.082)*(61.303-61.711)/(253.658-229.082)

meshes={'ck':b77_new('SM_Kvarnholmen_House_93192402','Kvarnholmen/Norra Långgatan'),'ap':b77_new('SM_Kvarnholmen_House_93192406','Kvarnholmen/Norra Långgatan')}
for zone in ('ck','ap'):
 m=meshes[zone];H=Z[zone]['height']
 for w in walls(zone):
  x,y,L,a=sf_edge(w['p'],w['q']);ox,oy=outward(w)
  front=w['kind']=='outer' and oy>.9 and min(w['p'][1],w['q'][1])>61
  if zone=='ck' and front:
   S=lambda X:U(w,X,61.75)
   gf=[(S(X0),1.28,ww,1.09,0) for X0,ww in ((227.24,1.17),(225.71,1.24))];up=[(S(226.53),3.53,1.19,1.30,0)]
   bz_wall(m,w['p'],w['q'],0,H,gf,M['Red'])
   n=int(L/.22)
   for k in range(1,n):
    u=-L/2+k*L/n;segs=[(.2,H-.05)]
    for hu,hb,hw,hh,hr in gf:
     if abs(u-hu)<hw/2+.15:segs=[(l0,h0) for l,h_ in segs for l0,h0 in ((l,min(h_,hb-.14)),(max(l,hb+hh+.16),h_)) if h0-l0>.05]
    for l0,h0 in segs:facade_box(m,x,y,u,.37,(l0+h0)/2,.035,.03,h0-l0,M['Red'],a)
   for u,b,ww,hh,r in gf:cas77(m,x,y,u,b,ww,hh,a,M['YellowFrame']);surround36(m,x,y,u,b,ww,hh,a,M['GreySurround'],.10,.40)
   for uu in (-L/2+.12,L/2-.12):facade_box(m,x,y,uu,.42,H/2,.24,.12,H,M['Weathered'],a)
   # The gable in the wall plane, with its window in front of it.
   prof=[(-L/2,H),(L/2,H),(S(226.37),Z['ck']['top'])]
   vs=[lp(x,y,uu,o,zz,a) for o in (.005,.355) for uu,zz in prof];nn=len(prof)
   m.faces(vs,[tuple(range(nn-1,-1,-1)),tuple(range(nn,2*nn))]+[(i,(i+1)%nn,(i+1)%nn+nn,i+nn) for i in range(nn)],M['Red'])
   for u,b,ww,hh,r in up:
    facade_box(m,x,y,u,.37,b+hh/2,ww,.02,hh,GLAZE,a);cas77(m,x,y,u,b,ww,hh,a,M['YellowFrame'],.40);surround36(m,x,y,u,b,ww,hh,a,M['GreySurround'],.10,.44)
   for s in (-1,1):town_path(m,[lp(x,y,s*(L/2+.3),.50,H-.2,a),lp(x,y,S(226.37),.50,Z['ck']['top']+.12,a)],.09,M['Weathered'])
  elif zone=='ap' and front:
   S=lambda X:U(w,X,yn77(X))
   gf=[(S(X0),2.16,ww,1.66,0) for X0,ww in ((236.0,1.50),(238.55,1.52),(246.9,1.50))]
   up=[(S(X0),5.05,ww,1.64,0) for X0,ww in ((236.0,1.47),(238.55,1.52),(242.34,1.49),(246.9,1.50))]
   cel=[(S(X0),.35,.90,.40,0) for X0 in (236.0,238.55,246.9)]
   door=(S(242.1),.42,1.80,3.26,0)
   logs=[(S(X0),.0,3.85,H-.6,0) for X0 in (231.53,250.67)]
   bz_wall(m,w['p'],w['q'],0,H,gf+up+cel+[door]+logs,M['Yellow'])
   for u,b,ww,hh,r in gf+up:cas77(m,x,y,u,b,ww,hh,a,M['WhiteFrame'],.16,1);surround36(m,x,y,u,b,ww,hh,a,M['GreySurround'],.10,.40);facade_box(m,x,y,u,.46,b-.05,ww+.24,.14,.05,M['Plinth'],a)
   for u,b,ww,hh,r in cel:facade_box(m,x,y,u,.44,b+hh/2,ww,.02,hh,M['Dark'],a);surround36(m,x,y,u,b,ww,hh,a,WH,.05,.44)
   # The recessed entrance: its back wall and a glazed door 1.3 m in.
   u,b,ww,hh,r=door
   facade_box(m,x,y,u,-.95,b+hh/2,ww,.06,hh,M['Yellow'],a);facade_box(m,x,y,u,-.90,b+1.1,1.1,.04,2.1,GLAZE,a);facade_box(m,x,y,u,-.88,b+1.1,1.2,.05,.06,M['WhiteFrame'],a)
   for s in (-1,1):facade_box(m,x,y,u+s*ww/2,-.3,b+hh/2,.06,1.3,hh,M['Yellow'],a)
   facade_box(m,x,y,u,-.3,b+hh,ww,1.3,.06,M['Yellow'],a);steps36(m,x,y,u,a,ww+.2,ww,b,2,.40,M['Plinth'])
   # The loggias: back walls with wide windows 1.2 m in, floor slabs and white balcony fronts.
   for u,b,ww,hh,r in logs:
    facade_box(m,x,y,u,-.85,H/2,ww,.06,H,M['Yellow'],a)
    for s in (-1,1):facade_box(m,x,y,u+s*ww/2,-.25,H/2,.06,1.2,H,M['Yellow'],a)
    for zb,wb in ((2.49,1.12),(5.04,1.08)):
     facade_box(m,x,y,u,-.80,zb+wb/2,2.3,.02,wb,GLAZE,a);cas77(m,x,y,u,zb,2.3,wb,a,M['WhiteFrame'],-.78,1)
    for zs in (.9,3.95):facade_box(m,x,y,u,-.25,zs,ww,1.2,.14,M['Plinth'],a)
    for z0,z1 in ((.92,2.13),(3.94,5.14)):facade_box(m,x,y,u,.40,(z0+z1)/2,ww-.1,.08,z1-z0,WH,a)
    facade_box(m,x,y,u,-.25,H-.62,ww,1.2,.12,M['Yellow'],a)
    facade_box(m,x,y,u,.19,.42,ww,.34,.84,M['Plinth'],a)
    for zr in (2.45,5.46):town_rod(m,lp(x,y,u-ww/2+.05,.40,zr,a),lp(x,y,u+ww/2-.05,.40,zr,a),.025,WH,6)
   at=-L/2
   for lo,hi in sorted([(l[0]-l[2]/2,l[0]+l[2]/2) for l in logs]+[(door[0]-door[2]/2,door[0]+door[2]/2)])+[(L/2+1,L/2+1)]:
    if lo>at+.03:facade_box(m,x,y,(at+lo)/2,.39,.50,lo-at,.08,1.0,M['Plinth'],a)
    at=max(at,hi)
   facade_box(m,x,y,0,.42,7.55,L,.10,.22,WH,a);facade_box(m,x,y,0,.54,7.76,L+.06,.34,.14,WH,a)
  else:
   if w['kind']=='outer':plain(m,w,H,M['Red'] if zone=='ck' else M['Yellow'],M['WhiteFrame'],WH,1 if zone=='ck' else 2,.9)
   else:bz_wall(m,w['p'],w['q'],w['z0'],H,[],M['Red'] if zone=='ck' else M['Yellow'])
 roof34(m,zone,M['Tile'],M['Red'] if zone=='ck' else M['Yellow'])
for cx in (234.0,241.4,249.0):box(meshes['ap'],cx,56.0,.9,.7,.6,Z['ap']['top']-.55,M['Tile'],0,M['Dark'])
# The iron gate between the cottage and the pass 75 range.
m=meshes['ck'];gp,gq=(222.74,61.15),(224.27,61.79);x,y,L,a=sf_edge((222.74,61.2),(224.27,61.2))
for k in range(int(L/.12)+1):facade_box(m,x,y,-L/2+k*L/int(L/.12),.20,1.0,.03,.03,2.0,M['Iron'],a)
for zz in (.1,1.0,1.95):facade_box(m,x,y,0,.20,zz,L,.05,.05,M['Iron'],a)
b77_finish(meshes['ck'],'93192402');b77_finish(meshes['ap'],'93192406')

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block77_cameras=[
 sv_camera('384_Block77_Cal_Cottage',230.44,69.38+.355,2.30,152,10,90),
 sv_camera('385_Block77_Cal_Block',230.44,69.38+.355,2.30,112,10,90),
 ('386_Block77_Aerial',(240.0,74.0,26.0),(240.0,54.0,2.0),28),
]
print('BLOCK77_GEOMETRY',len(block77_names))
