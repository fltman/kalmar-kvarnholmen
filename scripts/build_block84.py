"""Pass 84: Skeppsbron 30, the low rendered building west of the warehouse row: pale ochre walls with
white corner pilasters, a dark hipped tile roof with three chimneys over the main body and the
south-west wing, and the gabled porch on the north-east side with its fretwork gable.

References: Google Street View April 2025 (one panorama on Skeppsbron at about 35 m), view only.
Zones: source/block84.json; see references/block84-notes.md. Heights and openings are estimates.
"""
B84D=json.loads((R/'source/block84.json').read_text());Z=B84D['zones']
block84_names=[];B84={}
for old in [k for k in list(materials) if k.startswith('M_Block84_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Ochre','TownIvory',(.86,.79,.62),.90,0),('White','TownPaintWhite',(.94,.94,.92),.55,0),('Tile','TownTileRed',(.30,.29,.29),.80,0),
 ('Door','TownPaintBrown',(.42,.30,.22),.60,0),('Chimney','TownTileRed',(.45,.40,.37),.85,0),('Dark','TownMetalGrey',(.05,.055,.06),.40,.20),
 ]:
 name='M_Block84_'+key;B84[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block84_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B84
old=bpy.data.objects.get('SM_Kvarnholmen_House_91915619')
if old:bpy.data.objects.remove(old,do_unlink=True)
m=Mesh('SM_Kvarnholmen_House_91915619','Kvarnholmen/Skeppsbron');block84_names.append('SM_Kvarnholmen_House_91915619')
TA,TB=(-83.1,-314.1),(-92.0,-304.7)
for zone,spec in Z.items():
 H=spec['height']
 for w in walls(zone):
  if w['kind']!='outer':bz_wall(m,w['p'],w['q'],w['z0'],H,[],M['Ochre']);continue
  x,y,L,a=sf_edge(w['p'],w['q'])
  if zone=='tp' and L>5:
   # The porch front: a double door with a fanlight, flanking windows.
   ops=[(0,0,1.4,2.3,0),(-2.0,1.0,.8,1.2,0),(2.0,1.0,.8,1.2,0)]
   bz_wall(m,w['p'],w['q'],0,H,ops,M['Ochre'])
   for u,b,ww,hh,r in ops:
    if b==0:
     for s in (-1,1):facade_box(m,x,y,u+s*ww/4,.12,hh/2,ww/2-.03,.07,hh,M['Door'],a)
    else:cas81(m,x,y,u,b,ww,hh,a,M['White'],.16,2)
    surround36(m,x,y,u,b,ww,hh,a,M['White'],.12,.40)
  else:plain(m,w,H,M['Ochre'],M['White'],M['White'],1,.6)
  for uu in (-L/2+.15,L/2-.15):facade_box(m,x,y,uu,.42,H/2,.30,.10,H,M['White'],a)
  facade_box(m,x,y,0,.44,H-.15,L+.1,.14,.30,M['White'],a);facade_box(m,x,y,0,.40,.25,L,.08,.50,M['White'],a)
# Hipped roofs over the main body and the wing, boxed in the frame of the north-east front.
def rect84(zone):
 L=math.dist(TA,TB);d=((TB[0]-TA[0])/L,(TB[1]-TA[1])/L);n=(-d[1],d[0]);pts=[v for g in Z[zone]['polygons'] for v in g]
 ss=[(v[0]-TA[0])*d[0]+(v[1]-TA[1])*d[1] for v in pts];ts=[(v[0]-TA[0])*n[0]+(v[1]-TA[1])*n[1] for v in pts]
 P=lambda s,t:(TA[0]+d[0]*s+n[0]*t,TA[1]+d[1]*s+n[1]*t)
 r=[P(min(ss),min(ts)),P(max(ss),min(ts)),P(max(ss),max(ts)),P(min(ss),max(ts))]
 area=sum(r[i][0]*r[(i+1)%4][1]-r[(i+1)%4][0]*r[i][1] for i in range(4))
 return (r if area>0 else r[::-1]),max(ss)-min(ss),max(ts)-min(ts),P,(min(ss),max(ss),min(ts),max(ts))
for zone in ('tm','tw'):
 r,Ls,Lt,P,bb=rect84(zone);H=Z[zone]['height'];T=Z[zone]['top'];inset_roof(m,r,H,min(Ls,Lt)/2-.30,T-H,M['Tile'],.45)
r,Ls,Lt,P,(s0,s1,t0,t1)=rect84('tm');tm=(t0+t1)/2
for s in (s0+.25*(s1-s0),s0+.5*(s1-s0),s0+.75*(s1-s0)):box(m,*P(s,tm),.6,.6,1.6,Z['tm']['top']-.6,M['Chimney'],math.atan2(TB[1]-TA[1],TB[0]-TA[0]),M['Dark'])
# The porch: a gable towards Skeppsbron with fretwork in its triangle, a saddle roof back to the
# main slope.
r,Ls,Lt,P,(s0,s1,t0,t1)=rect84('tp');H=Z['tp']['height'];T=Z['tp']['top'];sm=(s0+s1)/2;half=(s1-s0)/2;sl=(T-H)/half
for s in (s0-.35,s1+.35):
 zz=H-.35*sl
 m.faces([(*P(s,t0-.35),zz),(*P(sm,t0-.35),T),(*P(sm,t1+3.0),T),(*P(s,t1+3.0),zz)],[(0,1,2,3),(3,2,1,0)],M['Tile'])
m.faces([(*P(s0,t0),H),(*P(s1,t0),H),(*P(sm,t0),T)],[(0,1,2),(2,1,0)],M['Ochre'])
for s in (s0-.3,s1+.3):town_path(m,[(*P(s,t0-.38),H-.30*sl-.05),(*P(sm,t0-.38),T-.02)],.08,M['White'])
for k in range(-3,4):
 tx=sm+k*half/4.5;zt=T-abs(tx-sm)*sl-.15
 if zt>H+.2:town_path(m,[(*P(sm,t0-.08),H+.25),(*P(tx,t0-.08),zt)],.03,M['White'])
obj=s21_finish(m);obj['detail_pass']=84;obj['reference_notes']='references/block84-notes.md';obj['osm_way']='91915619'

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block84_cameras=[sv_camera('416_Block84_Cal_Porch',-60.0,-282.0,2.40,178,5,50),('417_Block84_Aerial',(-60.0,-300.0,26.0),(-87.0,-318.0,2.0),28)]
print('BLOCK84_GEOMETRY',len(block84_names))
