"""Pass 85: Anstalten Kalmar on the mainland shore west of Västerport, outside the district model:
- the ground: grass on the shore patch, a bank down to the water along the coast, asphalt on
  Ravelinsgatan and the service road, gravel in the walled yard;
- the prison: three storeys of ochre render over a grey plinth under low hipped metal roofs, in its
  three ranges; the front range towards Västerport carries the central pavilion with its pediment,
  clock window and entrance; rows of chimneys;
- the walls and fences round the yards, and the Rotunda pavilion by Ravelinsgatan.

References: a user panorama on the Västerport bridge (winter) and Google Street View on Olof Palmes
gata (April 2025), view only. Data: source/block85.json; see references/block85-notes.md.
"""
B85D=json.loads((R/'source/block85.json').read_text());Z=B85D['zones']
block85_names=[];B85={}
for old in [k for k in list(materials) if k.startswith('M_Block85_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Ochre','TownIvory',(.85,.72,.45),.90,0),('White','TownPaintWhite',(.93,.92,.88),.60,0),('Plinth','TownStone',(.58,.57,.55),.90,0),
 ('Roof','TownMetalGrey',(.36,.37,.39),.55,.30),('Stone','TownStone',(.55,.52,.48),.92,0),('Coping','TownStone',(.66,.64,.60),.85,0),
 ('Fence','TownMetalGrey',(.12,.13,.13),.45,.40),('Door','TownPaintBrown',(.38,.27,.20),.60,0),('Chimney','TownTileRed',(.52,.44,.38),.85,0),
 ('Grass','TownStone',(.33,.42,.22),.95,0),('Bank','TownStone',(.40,.44,.30),.95,0),('Asphalt','TownMetalGrey',(.20,.20,.21),.90,0),('Gravel','TownStone',(.60,.57,.52),.95,0),
 ('Dark','TownMetalGrey',(.05,.055,.06),.40,.20),
 ]:
 name='M_Block85_'+key;B85[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block85_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B85
def b85_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block85_names.append(name);return Mesh(name,category)
def b85_finish(m,osm):
 obj=s21_finish(m);obj['detail_pass']=85;obj['reference_notes']='references/block85-notes.md';obj['osm_way']=osm;return obj
from mathutils import Vector
from mathutils.geometry import tessellate_polygon
def surf(m,piece,z,ma):
 # Flat polygon with holes, as upward triangles (as in pass 27).
 rings=[piece['outer']]+piece.get('holes',[]);flatv=[(x,y) for r in rings for x,y in r]
 for t in tessellate_polygon([[Vector((x,y,0)) for x,y in r] for r in rings]):
  v=[(flatv[i][0],flatv[i][1],z) for i in t]
  if (v[1][0]-v[0][0])*(v[2][1]-v[0][1])-(v[1][1]-v[0][1])*(v[2][0]-v[0][0])<0:v.reverse()
  m.faces(v,[(0,1,2)],ma)
ZG=0.30  # ground level of the shore patch (model z; Kvarnholmen's streets are at about 0)

# ---------------------------------------------------------------- ground
m=b85_new('SM_Prison85_Ground','Anstalten Kalmar/Ground')
surf(m,{'outer':B85D['ground']['outer'],'holes':[]},ZG,M['Grass'])
for g in B85D['roads']:surf(m,{'outer':g,'holes':[]},ZG+.02,M['Asphalt'])
for g in B85D['yard']:surf(m,{'outer':g,'holes':[]},ZG+.01,M['Gravel'])
# The bank: the coast drops 2.5 m out to below the water line (land lies left of the coastline).
sh=B85D['ground']['shore']
for p,q in zip(sh,sh[1:]):
 L=math.dist(p,q);nx,ny=(q[1]-p[1])/L,-(q[0]-p[0])/L
 m.faces([(*p,ZG),(*q,ZG),(q[0]+nx*2.5,q[1]+ny*2.5,-1.7),(p[0]+nx*2.5,p[1]+ny*2.5,-1.7)],[(0,1,2,3),(3,2,1,0)],M['Bank'])
b85_finish(m,'90822660')

# ---------------------------------------------------------------- the prison
m=b85_new('SM_Prison85_Anstalten','Anstalten Kalmar/Buildings')
def frame85(zone):
 a,b=Z[zone]['frame'];L=math.dist(a,b);d=((b[0]-a[0])/L,(b[1]-a[1])/L);return a,d,(-d[1],d[0])
def rect85(zone):
 a,d,n=frame85(zone);pts=[v for g in Z[zone]['polygons'] for v in g]
 ss=[(v[0]-a[0])*d[0]+(v[1]-a[1])*d[1] for v in pts];ts=[(v[0]-a[0])*n[0]+(v[1]-a[1])*n[1] for v in pts]
 P=lambda s,t:(a[0]+d[0]*s+n[0]*t,a[1]+d[1]*s+n[1]*t)
 r=[P(min(ss),min(ts)),P(max(ss),min(ts)),P(max(ss),max(ts)),P(min(ss),max(ts))]
 area=sum(r[i][0]*r[(i+1)%4][1]-r[(i+1)%4][0]*r[i][1] for i in range(4))
 return (r if area>0 else r[::-1]),max(ss)-min(ss),max(ts)-min(ts),P,(min(ss),max(ss),min(ts),max(ts))
for zone,spec in Z.items():
 H=spec['height']
 for w in walls(zone):
  if w['kind']!='outer':bz_wall(m,w['p'],w['q'],w['z0'],H,[],M['Ochre']);continue
  x,y,L,a=sf_edge(w['p'],w['q'])
  if L<2.5:bz_wall(m,w['p'],w['q'],ZG,H,[],M['Ochre']);continue
  plain(m,w,H,M['Ochre'],M['White'],M['White'],3,1.2)
  facade_box(m,x,y,0,.40,ZG+.45,L,.10,.90,M['Plinth'],a)
  facade_box(m,x,y,0,.44,H-.25,L+.1,.16,.50,M['White'],a);facade_box(m,x,y,0,.42,4.15,L,.06,.16,M['White'],a)
  for uu in (-L/2+.2,L/2-.2):facade_box(m,x,y,uu,.42,H/2,.40,.08,H,M['White'],a)
for zone in Z:
 r,Ls,Lt,P,(s0,s1,t0,t1)=rect85(zone);H=Z[zone]['height'];T=Z[zone]['top']
 inset_roof(m,r,H,min(Ls,Lt)/2-.30,T-H,M['Roof'],.55)
 # Chimneys along the ridge.
 tm=(t0+t1)/2;ang=math.atan2(P(1,0)[1]-P(0,0)[1],P(1,0)[0]-P(0,0)[0])
 for k in range(1,int((s1-s0)/6.5)):box(m,*P(s0+k*(s1-s0)/int((s1-s0)/6.5),tm),.7,.9,1.7,T-.5,M['Chimney'],ang,M['Dark'])
# The central pavilion on the front range: projecting 0.6 m at the risalit (OSM corners 20-21-0),
# rising to a pediment with a round clock window, a tall arched entrance below.
a,d,n=frame85('fr');ang=math.atan2(d[1],d[0]);cx,cy=(-440.6,137.9);W,Hp=8.2,Z['fr']['height']+.6;apex=Z['fr']['top']+2.3
box(m,cx-n[0]*.3,cy-n[1]*.3,W,1.6,Hp-ZG,ZG,M['Ochre'],ang)
X,Y=cx-n[0]*1.1,cy-n[1]*1.1
for o in (0.0,.4):
 m.faces([lp(X,Y,-W/2-.3,o,Hp,ang),lp(X,Y,W/2+.3,o,Hp,ang),lp(X,Y,0,o,apex,ang)],[(0,1,2),(2,1,0)],M['Ochre'] if o else M['White'])
for s in (-1,1):town_path(m,[lp(X,Y,s*(W/2+.35),.45,Hp-.05,ang),lp(X,Y,0,.45,apex+.08,ang)],.14,M['White'])
for s in (-1,1):
 q=[lp(X,Y,s*(W/2+.6),.75,Hp-.2,ang),lp(X,Y,0,.75,apex+.2,ang),lp(X,Y,0,-4.0,apex+.2,ang),lp(X,Y,s*(W/2+.6),-4.0,Hp-.2,ang)]
 m.faces(q,[(0,1,2,3),(3,2,1,0)],M['Roof'])
k=20;zc=(Hp+apex)/2-.2
m.faces([lp(X,Y,.55*math.cos(t*math.tau/k),.46,zc+.55*math.sin(t*math.tau/k),ang) for t in range(k)],[tuple(range(k)),tuple(range(k-1,-1,-1))],M['White'])
town_path(m,[lp(X,Y,.62*math.cos(t*math.tau/k),.48,zc+.62*math.sin(t*math.tau/k),ang) for t in range(k+1)],.06,M['Dark'])
for s in (-1,1):facade_box(m,X,Y,s*(W/2-.25),.45,(ZG+Hp)/2,.5,.12,Hp-ZG,M['White'],ang)
facade_box(m,X,Y,0,.44,ZG+.5,W,.12,1.0,M['Plinth'],ang);facade_box(m,X,Y,0,.46,Hp-.3,W+.2,.18,.5,M['White'],ang)
facade_box(m,X,Y,0,.42,ZG+1.55,2.0,.08,2.5,M['Door'],ang);p18_arch(m,X,Y,ZG+2.8,2.0,1.0,.3,.46,ang,M["White"])
for zz,hh in ((4.9,1.9),(8.0,1.9)):
 for s in (-1,0,1):facade_box(m,X,Y,s*2.3,.44,zz+hh/2,1.1,.02,hh,GLAZE,ang);surround36(m,X,Y,s*2.3,zz,1.1,hh,ang,M['White'],.12,.50)
b85_finish(m,'91053122')

# ---------------------------------------------------------------- walls, fences, the Rotunda
m=b85_new('SM_Prison85_Walls','Anstalten Kalmar/Walls')
for wid,wd in B85D['walls'].items():
 pts=wd['points'];h=wd['h']
 for p,q in zip(pts,pts[1:]):
  x,y,L,a=sf_edge(p,q);m.box(((p[0]+q[0])/2,(p[1]+q[1])/2,ZG+h/2-.2),(L+.5,.55,h+.4),M['Stone'],a)
  m.box(((p[0]+q[0])/2,(p[1]+q[1])/2,ZG+h+.25),(L+.6,.75,.14),M['Coping'],a)
for wid,pts in B85D['fences'].items():
 for p,q in zip(pts,pts[1:]):
  L=math.dist(p,q);n_=max(1,int(L/2.5))
  for k in range(n_+1):
   X,Y=p[0]+(q[0]-p[0])*k/n_,p[1]+(q[1]-p[1])*k/n_;town_rod(m,(X,Y,ZG),(X,Y,ZG+2.4),.04,M['Fence'],6)
  for zz in (ZG+.15,ZG+1.2,ZG+2.35):town_rod(m,(*p,zz),(*q,zz),.025,M['Fence'],6)
b85_finish(m,'91053134')
m=b85_new('SM_Prison85_Rotunda','Anstalten Kalmar/Buildings')
rp=B85D['rotunda']['points'];H=B85D['rotunda']['h'];T=B85D['rotunda']['top'];cx=sum(p[0] for p in rp)/len(rp);cy=sum(p[1] for p in rp)/len(rp)
for i in range(len(rp)):
 p,q=rp[i],rp[(i+1)%len(rp)];x,y,L,a=sf_edge(p,q)
 holes=[(0,.9,.55,1.2,.27)] if i%2==0 else []
 if i==0:holes=[(0,0,.9,2.1,.45)]
 bz_wall(m,p,q,ZG,ZG+H,holes,M['White'])
 for u,b,ww,hh,r in holes:facade_box(m,x,y,u,.10,ZG+b+hh/2,ww,.04,hh,M['Door'] if b==0 else GLAZE,a)
 facade_box(m,x,y,0,.42,ZG+H-.15,L+.1,.14,.3,M['White'],a)
# A deep white cornice and a low roof behind it.
for i in range(len(rp)):
 p,q=rp[i],rp[(i+1)%len(rp)];x,y,L,a=sf_edge(p,q);facade_box(m,x,y,0,.48,ZG+H+.12,L+.25,.24,.34,M['White'],a)
ring_=[(cx+(p[0]-cx)*.98,cy+(p[1]-cy)*.98) for p in rp]
for i in range(len(ring_)):
 p,q=ring_[i],ring_[(i+1)%len(ring_)];m.faces([(*p,ZG+H),(*q,ZG+H),(cx,cy,ZG+T)],[(0,1,2),(2,1,0)],M['Roof'])
b85_finish(m,'1118433612')

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block85_cameras=[sv_camera('418_Block85_Cal_Vasterport',-357.3,109.1,1.8,245,8,90),sv_camera('419_Block85_Cal_Palme',-526.0,86.7,2.4,10,10,90),
 ('420_Block85_Aerial',(-390.0,90.0,45.0),(-450.0,155.0,4.0),28)]
print('BLOCK85_GEOMETRY',len(block85_names))
