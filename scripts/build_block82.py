"""Pass 82: the north side of Kom snart igen and Skeppsbron 13, low boarded houses under tiled roofs:
- the orange-boarded house (Kom snart igen 1) on a grey plinth, with three round windows in its east
  wall, three dormers and a dark boarded annex behind;
- the yellow house (Kom snart igen 5) with three windows under blue awnings, two roof lights and a
  chimney;
- the yellow corner house (Kom snart igen 7 / Skeppsbron 11) with its doors on steps, two red
  dormers and a roof light, the lower west part with a green awning, and the north wing under a
  saddle roof;
- the yellow café at Skeppsbron 13 under a dark saddle roof, with its flat-roofed south annex.

References: Google Street View April 2025 (four panoramas on Kom snart igen and Skeppsbron, the two
on Kom snart igen resected on house corners), view only. Zones: source/block82.json; see
references/block82-notes.md. Signs, awning lettering, heat pumps and meter boxes are omitted.
"""
B82D=json.loads((R/'source/block82.json').read_text());Z=B82D['zones']
block82_names=[];B82={}
for old in [k for k in list(materials) if k.startswith('M_Block82_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Orange','TownIvory',(.80,.47,.31),.82,0),('Yellow','TownIvory',(.92,.78,.47),.82,0),('CafeYellow','TownIvory',(.90,.73,.38),.82,0),
 ('DarkBoard','TownPaintBrown',(.28,.20,.15),.75,0),('WhiteFrame','TownPaintWhite',(.95,.95,.93),.55,0),('Corner','TownPaintWhite',(.86,.86,.84),.60,0),
 ('DormerRed','TownPaintBrown',(.62,.24,.19),.60,0),('Awning','TownPaintWhite',(.13,.30,.70),.70,0),('AwningGreen','TownPaintWhite',(.30,.48,.42),.70,0),
 ('Plinth','TownStone',(.70,.69,.66),.90,0),('Tile','TownTileRed',(.78,.42,.27),.80,0),('TileDark','TownTileRed',(.32,.24,.20),.80,0),
 ('Chimney','TownTileRed',(.62,.36,.28),.85,0),('Iron','TownMetalGrey',(.08,.08,.085),.45,.40),('Dark','TownMetalGrey',(.05,.055,.06),.40,.20),
 ]:
 name='M_Block82_'+key;B82[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block82_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B82;WF=M['WhiteFrame']

def b82_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block82_names.append(name);return Mesh(name,category)
def b82_finish(m,osm):
 obj=s21_finish(m);obj['detail_pass']=82;obj['reference_notes']='references/block82-notes.md';obj['osm_way']=osm;return obj

def frame82(a,b):
 # Street frame of a front a->b: unit along, unit inwards (left of a->b).
 L=math.dist(a,b);d=((b[0]-a[0])/L,(b[1]-a[1])/L);return d,(-d[1],d[0])
def rect82(zone,a,b):
 # The zone's outline boxed in the frame of its street front: a counter-clockwise rectangle.
 d,n=frame82(a,b);pts=[v for g in Z[zone]['polygons'] for v in g]
 ss=[(v[0]-a[0])*d[0]+(v[1]-a[1])*d[1] for v in pts];ts=[(v[0]-a[0])*n[0]+(v[1]-a[1])*n[1] for v in pts]
 P=lambda s,t:(a[0]+d[0]*s+n[0]*t,a[1]+d[1]*s+n[1]*t)
 r=[P(min(ss),min(ts)),P(max(ss),min(ts)),P(max(ss),max(ts)),P(min(ss),max(ts))]
 area=sum(r[i][0]*r[(i+1)%4][1]-r[(i+1)%4][0]*r[i][1] for i in range(4))
 return (r if area>0 else r[::-1]),max(ss)-min(ss),max(ts)-min(ts)
def hip82(m,zone,a,b,ma):
 r,Ls,Lt=rect82(zone,a,b);H=Z[zone]['height'];T=Z[zone]['top']
 inset_roof(m,r,H,min(Ls,Lt)/2-.30,T-H,ma,.40)
 # Slope of the hip planes: they rise from the eave ring 0.40 m outside the walls.
 return r,(T-H)/(min(Ls,Lt)/2-.30+.40)
def saddle82(m,zone,a,b,ma,wall,along=True,ov=.35):
 # Saddle roof over the boxed outline, ridge along the front (along=True) or across it, gable
 # triangles in the wall material at the ends.
 r,Ls,Lt=rect82(zone,a,b);H=Z[zone]['height'];T=Z[zone]['top']
 if not along:r=r[1:]+r[:1]
 p0,p1,p2,p3=r;mid=lambda u,v:((u[0]+v[0])/2,(u[1]+v[1])/2)
 e0,e1=mid(p0,p3),mid(p1,p2);half=math.dist(p0,p3)/2;sl=(T-H)/half
 ex=lambda p,q,k:(p[0]+(p[0]-q[0])/math.dist(p,q)*k,p[1]+(p[1]-q[1])/math.dist(p,q)*k)
 # Eaves pushed out by the overhang, ends by the verge.
 L=math.dist(p0,p1);dx,dy=(p1[0]-p0[0])/L,(p1[1]-p0[1])/L
 sh=lambda p,s:(p[0]+dx*s,p[1]+dy*s)
 q0,q1,q2,q3=sh(ex(p0,p3,ov),-ov),sh(ex(p1,p2,ov),ov),sh(ex(p2,p1,ov),ov),sh(ex(p3,p0,ov),-ov);f0,f1=sh(e0,-ov),sh(e1,ov)
 for quad in ([q0,q1,f1,f0],[f1,q2,q3,f0]):
  zs=[H-ov*sl,H-ov*sl,T,T] if quad[0] is q0 else [T,H-ov*sl,H-ov*sl,T]
  m.faces([(*v,z) for v,z in zip(quad,zs)],[(0,1,2,3),(3,2,1,0)],ma)
 for u,v,c in ((p0,p3,e0),(p1,p2,e1)):m.faces([(*u,H),(*v,H),(*c,T)],[(0,1,2),(2,1,0)],wall)
 return r
def boards82(m,x,y,L,a,z0,z1,holes,ma,step=.22):
 n=max(2,int(L/step))
 for k in range(1,n):
  u=-L/2+k*L/n;segs=[(z0,z1)]
  for hu,hb,hw,hh,hr in holes:
   if abs(u-hu)<hw/2+.12:segs=[(l0,h0) for l,h_ in segs for l0,h0 in ((l,min(h_,hb-.12)),(max(l,hb+hh+.12),h_)) if h0-l0>.05]
  for l0,h0 in segs:facade_box(m,x,y,u,.37,(l0+h0)/2,.035,.03,h0-l0,ma,a)
def porthole82(m,x,y,u,zc,r,a,frame):
 k=20;ring=[lp(x,y,u+r*math.cos(t*math.tau/k),.385,zc+r*math.sin(t*math.tau/k),a) for t in range(k)]
 m.faces(ring,[tuple(range(k)),tuple(range(k-1,-1,-1))],GLAZE)
 town_path(m,[lp(x,y,u+(r+.05)*math.cos(t*math.tau/k),.41,zc+(r+.05)*math.sin(t*math.tau/k),a) for t in range(k+1)],.05,frame)
def awning82(m,x,y,u,top,w,a,ma,drop=.55,reach=.75):
 hi,lo=top+.20,top+.20-drop;vs=[lp(x,y,u-w/2,.42,hi,a),lp(x,y,u+w/2,.42,hi,a),lp(x,y,u+w/2,.42+reach,lo,a),lp(x,y,u-w/2,.42+reach,lo,a)]
 m.faces(vs,[(0,1,2,3),(3,2,1,0)],ma)
 for s in (-1,1):m.faces([lp(x,y,u+s*w/2,.42,hi,a),lp(x,y,u+s*w/2,.42+reach,lo,a),lp(x,y,u+s*w/2,.42,lo,a)],[(0,1,2),(2,1,0)],ma)
 facade_box(m,x,y,u,.42+reach,lo-.08,w,.02,.16,ma,a)
def dormer82(m,x,y,u,a,H,slope,w,h,body,frame,roof,back=.9):
 # A box dormer standing on the slope: its face 'back' metres behind the facade surface, a low
 # tiled lid, the window in a white frame.
 zb=H+(back+.40-.355+.05)*slope-.15;zt=zb+h+.55;dep=2.2
 box(m,*lp(x,y,u,.355-back-dep/2,0,a)[:2],w,dep,zt-zb,zb,body,a)
 box(m,*lp(x,y,u,.355-back-dep/2+.10,0,a)[:2],w+.25,dep+.2,.12,zt,roof,a)
 facade_box(m,x,y,u,.355-back+.01,zb+.30+h/2,w-.36,.02,h,GLAZE,a)
 cas81(m,x,y,u,zb+.30,w-.36,h,a,frame,.355-back+.05,3)
def steps82(m,x,y,u,w,top,a,ma):
 n=max(1,round(top/.18))
 for k in range(n):facade_box(m,x,y,u,.36+.32*(n-k)-.16+.0,(k+.5)*top/n,w+.5,.32*(n-k),top/n,ma,a)
def chimney82(m,X,Y,z0,z1,ma):box(m,X,Y,.55,.55,z1-z0,z0,ma,0,M['Dark'])
def skylight82(m,X,Y,z,ang,slope):
 # A flat roof light lying in the slope (ang: the slope's downhill bearing as a facade angle).
 k=math.atan(slope);w,l=.75,.95;c,s=math.cos(ang),math.sin(ang)
 pts=[]
 for du,dl in ((-w/2,-l/2),(w/2,-l/2),(w/2,l/2),(-w/2,l/2)):
  ox=du*c-(dl*math.cos(k))*s;oy=du*s+(dl*math.cos(k))*c;pts.append((X+ox,Y+oy,z+.06+dl*math.sin(k)))
 m.faces(pts,[(0,1,2,3),(3,2,1,0)],GLAZE)

# The fronts. Openings are given as model points on the facade line (x, y), with their bottom,
# width and height; kinds: win, door (with steps when the bottom is raised), port (round, centre
# height and radius). Positions from the resected panoramas; see the notes for the estimates.
def P82(a,b,s):d,_=frame82(a,b);return (a[0]+d[0]*s,a[1]+d[1]*s)
OA,OB=(-17.554,-268.274),(-42.584,-261.32);OE=(-15.023,-260.486)
YA,YB=(-9.713,-270.558),(5.017,-274.415)
KA,KB=(17.8,-277.0),(26.9,-279.8);KE=(34.5,-280.4)
WA,WB=(9.462,-276.495),(17.256,-278.918)
F={'or':dict(wall='Orange',trim='Corner',plinth=.55,ops=[('door',*P82(OA,OB,5.1),.10,1.0,2.05),('win',*P82(OA,OB,7.1),1.0,.9,1.1),('win',*P82(OA,OB,10.1),1.0,.9,1.1),
   ('win',*P82(OA,OB,15.1),1.0,.9,1.1),('win',*P82(OA,OB,21.2),1.0,.9,1.1)]+[('port',*P82(OA,OE,s),1.8,.33,0) for s in (1.52,4.03,6.5)]),
 'ob':dict(wall='DarkBoard',trim='DarkBoard',plinth=.30,ops=[]),
 'ye':dict(wall='Yellow',trim='WhiteFrame',plinth=.30,awning='Awning',ops=[('win',*P82(YA,YB,s),.90,1.5,1.4) for s in (3.9,7.4,11.1)]),
 'ma':dict(wall='Yellow',trim='WhiteFrame',plinth=.35,ops=[('door',*P82(KA,KB,.50),.50,.85,2.0),('win',*P82(KA,KB,1.96),1.50,1.9,1.3),('door',*P82(KA,KB,5.03),.60,.97,2.0),
   ('win',*P82(KA,KB,7.15),1.50,1.9,1.3),('win',*P82(KB,KE,3.6),1.50,1.2,1.3)]),
 'wp':dict(wall='Yellow',trim='WhiteFrame',plinth=.35,awning='AwningGreen',ops=[('win',*P82(WA,WB,5.6),1.20,1.0,1.2)]),
 'nw':dict(wall='Yellow',trim='WhiteFrame',plinth=.30,ops=[]),
 'ca':dict(wall='CafeYellow',trim='WhiteFrame',plinth=.30,ops=[('win',38.68,-235.7,.90,1.2,1.2),('door',36.0,-239.3,.15,1.1,2.1),('win',37.6,-244.0,.90,1.2,1.2)]),
 'cx':dict(wall='CafeYellow',trim='WhiteFrame',plinth=.30,ops=[('win',36.95,-249.6,.95,1.3,1.1)])}
STREET={'or':lambda ox,oy:oy<-.9,'ob':lambda ox,oy:False,'ye':lambda ox,oy:oy<-.9,'ma':lambda ox,oy:oy<-.9,'wp':lambda ox,oy:oy<-.9,
 'nw':lambda ox,oy:False,'ca':lambda ox,oy:ox>.9,'cx':lambda ox,oy:ox>.9}

meshes={}
for zone,spec in Z.items():
 nm=spec['mesh']
 if nm not in meshes:meshes[nm]=b82_new(nm,'Kvarnholmen/Kom snart igen')
for zone,spec in Z.items():
 m=meshes[spec['mesh']];H=spec['height'];f=F[zone];wm=M[f['wall']];tm=M[f['trim']]
 for w in walls(zone):
  if w['kind']!='outer':bz_wall(m,w['p'],w['q'],w['z0'],H,[],wm);continue
  x,y,L,a=sf_edge(w['p'],w['q']);ox,oy=outward(w)
  # Openings that lie on this wall: within 0.6 m of its line and inside its length.
  mine=[]
  for kind,X,Y,b,ww,hh in f['ops']:
   u=U(w,X,Y);off=abs((X-x)*math.sin(a)-(Y-y)*math.cos(a))
   wd=2*ww if kind=='port' else ww
   if off<.6 and abs(u)+wd/2<=L/2+.01:mine.append((kind,u,b,ww,hh))
  if not mine and not STREET[zone](ox,oy):
   plain(m,w,H,wm,WF,tm,1,.6);continue
  holes=[(u,b,ww,hh,0) for kind,u,b,ww,hh in mine if kind!='port']
  bz_wall(m,w['p'],w['q'],0,H,holes,wm)
  boards82(m,x,y,L,a,f['plinth']+.02,H-.08,holes+[(u,b-ww,2*ww,2*ww,0) for kind,u,b,ww,hh in mine if kind=='port'],wm)
  for kind,u,b,ww,hh in mine:
   if kind=='port':porthole82(m,x,y,u,b,ww,a,tm);continue
   if kind=='win':
    cas81(m,x,y,u,b,ww,hh,a,WF,.16,3 if hh>1.0 else 2);surround36(m,x,y,u,b,ww,hh,a,WF,.10,.40);facade_box(m,x,y,u,.47,b-.05,ww+.24,.16,.06,WF,a)
    if 'awning' in f:awning82(m,x,y,u,b+hh,ww+.2,a,M[f['awning']])
   else:
    facade_box(m,x,y,u,.12,b+hh/2,ww,.06,hh,WF,a)
    for zz in (b+hh*.62,b+hh*.30):facade_box(m,x,y,u,.17,zz,ww-.24,.03,hh*.22,WF,a)
    facade_box(m,x,y,u,.10,b+hh*.80,ww-.30,.02,hh*.25,GLAZE,a);surround36(m,x,y,u,b,ww,hh,a,WF,.10,.40)
    if b>.25:steps82(m,x,y,u,ww,b,a,M['Plinth'])
  # Corner boards, the plinth (with gaps at the low doors), the eaves board and gutter.
  for uu in (-L/2+.09,L/2-.09):facade_box(m,x,y,uu,.42,(H+f['plinth'])/2,.20,.10,H-f['plinth'],tm,a)
  at=-L/2
  for lo,hi in sorted((u-ww/2,u+ww/2) for kind,u,b,ww,hh in mine if kind=='door' and b<f['plinth'])+[(L/2,L/2)]:
   if lo>at+.03:facade_box(m,x,y,(at+lo)/2,.39,f['plinth']/2,lo-at,.08,f['plinth'],M['Plinth'],a)
   at=max(at,hi)
  if spec['roof']!='flat':
   facade_box(m,x,y,0,.46,H-.10,L+.1,.14,.20,WF if zone!='ob' else wm,a);town_rod(m,lp(x,y,-L/2,.66,H-.05,a),lp(x,y,L/2,.66,H-.05,a),.06,WF,8)
  else:
   facade_box(m,x,y,0,.42,H+(spec['top']-H)/2,L+.1,.14,spec['top']-H,tm if zone=='cx' else wm,a)
# Roofs.
m=meshes['SM_Kvarnholmen_House_91915626'];r,sl_or=hip82(m,'or',OB,OA,M['Tile'])
r_ob,_,_=rect82('ob',OB,OA)
for g in Z['ob']['polygons']:m.faces([(*v,Z['ob']['height']+.02) for v in g],[tuple(range(len(g))),tuple(range(len(g)-1,-1,-1))],M['Dark'])
x,y,L,a=sf_edge(OB,OA)
for s in (3.0,6.0,9.0):dormer82(m,x,y,U({'p':list(OB),'q':list(OA)},*P82(OA,OB,s)),a,Z['or']['height'],sl_or,1.3,.95,M['DormerRed'],WF,M['Tile'])
m=meshes['SM_Kvarnholmen_House_91915628'];r,sl_ye=hip82(m,'ye',YA,YB,M['Tile'])
d,n=frame82(YA,YB);ang=math.atan2(d[1],d[0])
X,Y=P82(YA,YB,9.4);chimney82(m,X+n[0]*3.6,Y+n[1]*3.6,Z['ye']['top']-.8,Z['ye']['top']+.75,M['Chimney'])
for s in (4.6,9.6):
 X,Y=P82(YA,YB,s);X,Y=X+n[0]*1.6,Y+n[1]*1.6;skylight82(m,X,Y,Z['ye']['height']+2.0*sl_ye,ang,sl_ye)
m=meshes['SM_Kvarnholmen_House_91915620'];r,sl_ma=hip82(m,'ma',KA,KE,M['Tile'])
x,y,L,a=sf_edge(KA,KE)
for X0,ww in ((20.2,1.7),(24.4,1.7)):dormer82(m,x,y,U({'p':list(KA),'q':list(KE)},*P82(KA,KE,(X0-17.8)/.979)),a,Z['ma']['height'],sl_ma,ww,1.15,M['DormerRed'],WF,M['Tile'])
d,n=frame82(KA,KE);ang=math.atan2(d[1],d[0]);X,Y=P82(KA,KE,3.6);skylight82(m,X+n[0]*2.2,Y+n[1]*2.2,Z['ma']['height']+2.6*sl_ma,ang,sl_ma)
for s,t in ((1.2,5.2),(9.0,5.0)):
 X,Y=P82(KA,KE,s);chimney82(m,X+n[0]*t,Y+n[1]*t,Z['ma']['top']-.6,Z['ma']['top']+.85,M['Chimney'])
hip82(m,'wp',WA,WB,M['Tile']);X,Y=P82(WA,WB,4.0);d,n=frame82(WA,WB);chimney82(m,X+n[0]*4.4,Y+n[1]*4.4,Z['wp']['top']-.5,Z['wp']['top']+.8,M['Chimney'])
saddle82(m,'nw',(14.76,-259.378),(26.4,-263.0),M['Tile'],M['Yellow'])
m=meshes['SM_Kvarnholmen_House_91915631']
saddle82(m,'ca',(28.575,-252.462),(30.783,-233.132),M['TileDark'],M['CafeYellow'],along=True)
chimney82(m,33.4,-238.0,Z['ca']['top']-.5,Z['ca']['top']+.7,M['Chimney'])
for g in Z['cx']['polygons']:m.faces([(*v,Z['cx']['height']+.02) for v in g],[tuple(range(len(g))),tuple(range(len(g)-1,-1,-1))],M['Dark'])
for nm in meshes:b82_finish(meshes[nm],nm.split('_')[-1])

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block82_cameras=[
 sv_camera('407_Block82_Cal_Orange',-9.84,-274.6,2.20,282,10,90),
 sv_camera('408_Block82_Cal_Yellow',-9.84,-274.6,2.20,62,10,90),
 sv_camera('409_Block82_Cal_Seven',19.32,-281.51,2.40,2,10,90),
 sv_camera('410_Block82_Cal_East',19.32,-281.51,2.40,62,10,90),
 ('411_Block82_Aerial',(5.0,-300.0,30.0),(5.0,-262.0,2.0),28),
]
print('BLOCK82_GEOMETRY',len(block82_names))
