"""Pass 30: the corner building Larmgatan 14 / Södra Långgatan (OSM 92204170).

A pink ground floor with stone-framed openings on a granite plinth under a moulded band; ochre
upper floors with red-brown casements; bracketed eaves with a red-brown soffit and a copper edge;
a copper and tile mansard; a canted corner with the corner oriel on a corbel carved with the arms
of Kalmar; a second oriel with the arms over the entrance on Larmgatan and a third on Södra
Långgatan, each with a hood between its floors and a copper bell cap; two tall curved gable bays
(salmon on Södra Långgatan with an oval light, brown at the north end of Larmgatan) rising to
finials at about 20 m; fire walls above the neighbours to the east and north.
References: Google Street View April 2025 (cameras registered on the two fronts), view only.
Zones: source/block30.json; see references/block30-notes.md. Tenant signs are omitted.
"""
B30D=json.loads((R/'source/block30.json').read_text());Z=B30D['zones'];Z30=Z['main']
block30_names=[];B30={}
for old in [k for k in list(materials) if k.startswith('M_Block30_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Pink','TownIvory',(.80,.58,.52),.90,0),
 ('Ochre','TownIvory',(.86,.71,.52),.90,0),
 ('Salmon','TownIvory',(.80,.58,.46),.90,0),
 ('BayBrown','TownIvory',(.62,.46,.37),.92,0),
 ('Band','TownIvory',(.66,.47,.40),.84,0),
 ('Stone','TownStone',(.74,.69,.62),.84,0),
 ('Granite','TownStone',(.58,.52,.50),.80,0),
 ('RedBrown','TownPaintBrown',(.42,.16,.13),.55,0),
 ('Oriel','TownPaintBrown',(.46,.27,.22),.60,0),
 ('Relief','TownIvory',(.88,.86,.80),.80,0),
 ('Soffit','TownPaintBrown',(.55,.27,.18),.60,0),
 ('SoffitDark','TownMetalGrey',(.10,.09,.09),.60,.10),
 ('Copper','ChurchCopperFine',(.40,.58,.50),.55,.35),
 ('Tile','TownTileRed',(.32,.25,.22),.82,0),
 ('Oak','TownPaintBrown',(.44,.28,.16),.58,0),
 ('Dark','TownMetalGrey',(.05,.055,.06),.40,.20),
 ]:
 name='M_Block30_'+key;B30[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block30_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B30;PK,OC,SA,BB,BD,ST,GRA,RB,OR,RL=(M[k] for k in ('Pink','Ochre','Salmon','BayBrown','Band','Stone','Granite','RedBrown','Oriel','Relief'))
H=Z30['height'];CT=Z30['copper_top'];TOP=Z30['top'];BAND=Z30['band'];FL=Z30['floors']
GS=Z30['gable_sodra'];GN=Z30['gable_north']

def b30_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block30_names.append(name);return Mesh(name,category)
def b30_finish(m,osm):
 obj=s21_finish(m);obj['detail_pass']=30;obj['reference_notes']='references/block30-notes.md';obj['osm_way']=osm;return obj
def kind30(w):
 ox,oy=outward(w)
 if w['kind']!='outer':return 'party'
 if oy<-.9 and min(w['p'][1],w['q'][1])<-66:return 'sodra'
 if ox<-.9 and min(w['p'][0],w['q'][0])<-285:return 'larm'
 if ox<-.5 and oy<-.5:return 'canted'
 return 'court'
def sframe(m,x,y,u,b,w,h,a,sill=True):
 # Stone surround of a ground-floor opening: jambs, lintel and a sill block.
 for s in (-1,1):facade_box(m,x,y,u+s*(w/2+.10),.39,b+h/2,.20,.08,h+.20,ST,a)
 facade_box(m,x,y,u,.40,b+h+.12,w+.44,.10,.24,ST,a)
 if sill:facade_box(m,x,y,u,.44,b-.08,w+.44,.18,.16,ST,a)
def upper_window(m,x,y,u,b,w,h,a,wall):
 s20_window(m,x,y,u,b,w,h,a,RB,wall,.70,False)
 # Small panes: two more glazing bars across each casement.
 for k in (1,2):facade_box(m,x,y,u,.235,b+h*.70*k/3,w,.05,.03,RB,a)
 facade_box(m,x,y,u,.44,b-.06,w+.16,.16,.06,wall,a)
def eaves(m,x,y,u0,u1,a):
 # Bracketed eaves: a red-brown soffit 0.8 m deep with dark panels between the rafter ends,
 # a fascia and the copper roof edge.
 L=u1-u0;uc=(u0+u1)/2
 if L<.3:return
 facade_box(m,x,y,uc,.355+.40,H+.10,L,.80,.08,M['SoffitDark'],a)
 n=max(1,round(L/.62))
 for k in range(n+1):
  u=u0+k*L/n;facade_box(m,x,y,u,.355+.40,H-.02,.12,.80,.18,M['Soffit'],a)
 facade_box(m,x,y,uc,.355+.82,H+.02,L,.08,.26,M['Soffit'],a)
 facade_box(m,x,y,uc,.355+.86,H+.22,L+.02,.14,.14,M['Copper'],a)
def gable30(m,x,y,u,w,shoulder,top,finial,a,ma):
 # Curved gable: straight sides to the shoulders, an S-curve in to a small segmental cap, a vase
 # finial; the gable body runs back into the mansard with its own curved roof.
 w2=w/2;c=.55;capz=top-.35;k=12;zb=H-.30
 left=[(-w2,zb),(-w2,shoulder)]+[(-w2+(w2-c)*(3*t*t-2*t*t*t),shoulder+(capz-shoulder)*t) for t in [i/k for i in range(1,k+1)]]
 cap=[(-c*math.cos(math.pi*i/8),capz+.35*math.sin(math.pi*i/8)) for i in range(1,8)]
 half=left+cap;out=(half+[(-uu,zz) for uu,zz in reversed(left)])[::-1]   # counter-clockwise from the street
 n=len(out)
 vs=[lp(x,y,u+uu,o,zz,a) for o in (-4.6,.40) for uu,zz in out]
 m.faces(vs,[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],ma)
 # Moulded coping along the curve and a small cornice at the shoulders.
 town_path(m,[lp(x,y,u+uu,.48,zz+.06,a) for uu,zz in out[1:-1]],.08,ma)
 for s in (-1,1):facade_box(m,x,y,u+s*(w2-.05),.50,shoulder,.40,.20,.16,ma,a)
 cx,cy,_=lp(x,y,u,.30,0,a);m.lathe(cx,cy,top,[(.22,0),(.26,.14),(.16,.34),(.20,.50),(.10,.75),(.04,finial-top)],ma,10)
def oval30(m,x,y,u,zc,rw,rh,a,frame,trim):
 kk=24;m.faces([lp(x,y,u+rw*math.cos(t*math.tau/kk),.42,zc+rh*math.sin(t*math.tau/kk),a) for t in range(kk)],[tuple(range(kk))],GLAZE)
 town_path(m,[lp(x,y,u+(rw+.04)*math.cos(t*math.tau/kk),.46,zc+(rh+.04)*math.sin(t*math.tau/kk),a) for t in range(kk+1)],.04,frame)
 town_path(m,[lp(x,y,u+(rw+.16)*math.cos(t*math.tau/kk),.50,zc+(rh+.16)*math.sin(t*math.tau/kk),a) for t in range(kk+1)],.07,trim)
 facade_box(m,x,y,u,.46,zc,2*rw,.05,.04,frame,a);facade_box(m,x,y,u,.46,zc,.04,.05,2*rh,frame,a)
def oriel30(m,x,y,u,a,W0=2.9,Wf=1.6,P=.75,z0=3.75,arms=True,cap='bell'):
 # Canted oriel through the first and second floors on a carved corbel.
 base=.36;out=[(-W0/2,base),(-Wf/2,base+P),(Wf/2,base+P),(W0/2,base)]
 pp=[lp(x,y,u+uu,o,0,a)[:2] for uu,o in out]
 # Corbel: stepped consoles, a moulded slab and the carved apron under the first-floor lights.
 for s in (-1,0,1):
  for kk,(zc,dd) in enumerate(((z0+.18,.30),(z0+.52,.55),(z0+.86,.80))):facade_box(m,x,y,u+s*Wf*.38,base+dd/2,zc,.22,dd,.36,OR,a)
 m.prism(pp,z0+1.02,z0+1.18,OR);m.prism(pp,z0+1.18,5.40,OR)
 xx,yy,LL,aa=sf_edge(pp[1],pp[2])
 facade_box(m,xx,yy,0,.03,(z0+1.18+5.40)/2,LL*.82,.04,5.40-z0-1.30,RL,aa)
 if arms:
  # A crowned shield in a wreath (the arms of Kalmar), read as a raised shield and two leaf rods.
  facade_box(m,xx,yy,0,.08,(z0+1.18+5.40)/2,.42,.06,.52,RL,aa);facade_box(m,xx,yy,0,.10,(z0+1.18+5.40)/2+.34,.30,.06,.14,RL,aa)
  for s in (-1,1):town_rod(m,lp(xx,yy,s*.26,.07,z0+1.35,aa),lp(xx,yy,s*.50,.07,z0+1.95,aa),.05,RL,6)
 else:facade_box(m,xx,yy,0,.08,(z0+1.18+5.40)/2,.50,.06,.40,RL,aa)
 m.prism(pp,5.40,5.55,OR)
 # Body with casements on every facet; a panel zone with the hood between the floors.
 for i in range(3):
  p0,p1=pp[i],pp[i+1];xx,yy,LL,aa=sf_edge(p0,p1)
  for b,hh in ((5.62,2.05),(9.30,2.00)):
   facade_box(m,xx,yy,0,-.02,b+hh/2,LL,.10,hh,OR,aa)
   gw=LL-.22 if i==1 else LL-.16
   facade_box(m,xx,yy,0,.04,b+hh/2,gw,.04,hh-.14,GLAZE,aa);town_border(m,xx,yy,b+hh/2,gw,hh-.14,aa,RB,.06,.06)
   if i==1:facade_box(m,xx,yy,0,.07,b+hh/2,.05,.05,hh-.14,RB,aa)
   for kk in (1,2):facade_box(m,xx,yy,0,.07,b+(hh-.14)*kk/3+.07,gw,.04,.03,RB,aa)
  facade_box(m,xx,yy,0,-.02,8.49,LL,.10,1.62,OR,aa)
  facade_box(m,xx,yy,0,.05,8.49,LL*.70,.04,.90,RL,aa)
  facade_box(m,xx,yy,0,-.02,11.95,LL,.10,.70,OR,aa)
 xx,yy,LL,aa=sf_edge(pp[1],pp[2])
 tri=[(-LL/2-.10,8.05),(LL/2+.10,8.05),(0,8.95)];vs=[lp(xx,yy,uu,o,zz,aa) for o in (.02,.26) for uu,zz in tri]
 m.faces(vs,[(2,1,0),(3,4,5),(0,1,4,3),(1,2,5,4),(2,0,3,5)],OR)
 m.prism(pp,12.30,12.50,OR);m.prism([lp(x,y,u+uu*1.06,o+.05,0,a)[:2] for uu,o in out],12.50,12.66,M['Copper'])
 cx_,cy_=sum(q[0] for q in pp)/4,sum(q[1] for q in pp)/4
 # Copper caps: a bell over the side oriels (top 14.4 on Larmgatan), a dome over the corner oriel
 # (top 15.1-15.8 from two panoramas).
 if cap=='bell':
  m.lathe(cx_,cy_,12.66,[(.95,0),(.88,.35),(.62,.85),(.40,1.25),(.30,1.55),(.10,1.74)],M['Copper'],4)
  m.lathe(cx_,cy_,14.38,[(.05,0),(.10,.10),(.03,.20),(.02,.60)],M['Copper'],8)
 else:
  m.lathe(cx_,cy_,12.66,[(1.25,0),(1.20,.45),(1.00,1.15),(.68,1.75),(.34,2.15),(.12,2.36)],M['Copper'],8)
  m.lathe(cx_,cy_,15.00,[(.06,0),(.12,.12),(.04,.24),(.025,.80)],M['Copper'],8)

m=b30_new('SM_Kvarnholmen_House_92204170','Kvarnholmen/Södra Långgatan north')
# Openings (facade u from each wall's midpoint).
SL_GF=[(-282.33,'w'),(-279.20,'w'),(-276.10,'w'),(-272.99,'w'),(-269.93,'d'),(-265.89,'w'),(-261.22,'w'),(-258.43,'w')]
SL_UP=[-282.33,-279.20,-270.50,-266.84,-264.97,-261.31,-258.59]
LG_GF=[(1.15,'bw'),(3.55,'bw'),(6.90,'g'),(9.59,'w'),(12.56,'d'),(15.52,'w'),(20.26,'w')]
LG_UP=[1.15,3.55,6.60,9.72,15.53,20.15]
DL=.17   # Larmgatan pavement below the Södra Långgatan datum
for w in walls('main'):
 x,y,L,a=sf_edge(w['p'],w['q']);kd=kind30(w)
 if kd=='party':bz_wall(m,w['p'],w['q'],w['z0'],H,[],OC);continue
 if kd=='court':plain(m,w,H,OC,RB,OC,3,1.0);continue
 if kd=='sodra':
  U=lambda X:uat(w,X,-67.3);gu0,gu1=sorted((U(GS['x'][0]),U(GS['x'][1])))
  gf=[];holes=[]
  for X,t in SL_GF:
   u=U(X)
   gf.append((u,.55,1.53,3.05,0) if t=='d' else (u,1.30,1.60,2.30,0))
  up=[(U(X),b,1.15,t-b,0) for X in SL_UP for b,t in FL]
  oc=U(-274.55)
 elif kd=='larm':
  U=lambda s:-L/2+s;gu0,gu1=U(GN['s'][0]),U(GN['s'][1])
  gf=[]
  for s,t in LG_GF:
   u=U(s)
   if t=='bw':gf.append((u,.90,1.05,2.20,0))
   elif t=='g':gf.append((u,0,1.45,3.30,0))
   elif t=='d':gf.append((u,0,1.70,3.62,0))
   else:gf.append((u,.84,1.72,2.67,0))
  up=[(U(s),b,1.15,t-b,0) for s in LG_UP for b,t in FL]
  oc=U(12.76)
 else:
  gf=[(0,.70,1.40,2.90,0)];up=[];gu0=gu1=None;oc=0
 holes=gf+up
 # Walls: the pink ground floor to the band; the upper floors ochre, the gable bays salmon or brown.
 bz_wall(m,w['p'],w['q'],0,BAND[0],[h for h in holes if h[1]<BAND[0]],PK)
 if gu0 is not None:
  segs=[(-L/2,gu0,OC),(gu0,gu1,SA if kd=='sodra' else BB),(gu1,L/2,OC)]
 else:segs=[(-L/2,L/2,OC)]
 for s0,s1,ma in segs:
  if s1-s0<.05:continue
  p0=lp(x,y,s0,0,0,a)[:2];p1=lp(x,y,s1,0,0,a)[:2];xs,ys,Ls,as_=sf_edge(p0,p1)
  hs=[(h[0]-(s0+s1)/2,h[1],h[2],h[3],h[4]) for h in holes if h[1]>=BAND[0] and s0<h[0]<s1]
  bz_wall(m,p0,p1,BAND[0],H,hs,ma)
  if kd=='larm' and ma==BB:bz_wall(m,p0,p1,0,BAND[0],[(h[0]-(s0+s1)/2,h[1],h[2],h[3],h[4]) for h in gf if s0<h[0]<s1],BB,.36,.40)
 # Ground floor joinery and stone frames.
 for u,b,ww,hh,r in gf:
  if kd=='larm' and b==0 and ww<1.5:
   # Carriage gate with an iron grille; a wide stone surround with the pier to its north.
   facade_box(m,x,y,u,.10,hh/2,ww,.06,hh,M['Dark'],a)
   for k in range(9):uu=u-ww/2+.1+k*(ww-.2)/8;town_rod(m,lp(x,y,uu,.22,.05,a),lp(x,y,uu,.22,hh-.08,a),.016,IRON,6)
   facade_box(m,x,y,u-ww/2-.72,.40,(hh+.52)/2,1.24,.10,hh+.52,ST,a);facade_box(m,x,y,u+ww/2+.10,.40,(hh+.52)/2,.20,.10,hh+.52,ST,a)
   facade_box(m,x,y,u-.31,.41,hh+.33,ww+1.66,.12,.40,ST,a)
  elif b<.7 and hh>2.9:
   s21_glass(m,x,y,u,b,ww,hh,a,M['Oak'],2,.74,True);sframe(m,x,y,u,b,ww,hh,a,False)
   if b>.2:facade_box(m,x,y,u,.62,b/2,ww+.6,.55,b,GRA,a)
  else:
   s21_glass(m,x,y,u,b,ww,hh,a,M['Oak'],1 if ww<1.2 else 2,.80,False);sframe(m,x,y,u,b,ww,hh,a,True)
 for u,b,ww,hh,r in up:
  if kd=='sodra' and abs(u-oc)<1.6:continue
  upper_window(m,x,y,u,b,ww,hh,a,SA if gu0 is not None and gu0<u<gu1 and kd=='sodra' else (BB if gu0 is not None and gu0<u<gu1 else OC))
 # Plinth, band, the shop-floor cornice line and the eaves.
 cuts=[(u-ww/2-.05,u+ww/2+.05) for u,b,ww,hh,r in gf if b<Z30['plinth']];at=-L/2
 for l,r_ in sorted(cuts)+[(L/2,L/2)]:
  if l>at+.02:facade_box(m,x,y,(at+l)/2,.40,Z30['plinth']/2,l-at,.10,Z30['plinth'],GRA,a)
  at=max(at,r_)
 p18_band(m,x,y,L+.3,(BAND[0]+BAND[1])/2,a,BD,.30)
 # The eaves stop at the gable bays; on the canted corner the corner oriel's dome takes their place.
 if gu0 is not None:
  eaves(m,x,y,-L/2-.4,gu0,a);eaves(m,x,y,gu1,L/2+.4,a)
 elif kd!='canted':eaves(m,x,y,-L/2-.4,L/2+.4,a)
 # Oriels and gables.
 if kd=='sodra':
  oriel30(m,x,y,oc,a,arms=False)
  gable30(m,x,y,(gu0+gu1)/2,gu1-gu0,GS['shoulder'],GS['top'],GS['finial'],a,SA)
  oval30(m,x,y,(gu0+gu1)/2,(GS['oval'][0]+GS['oval'][1])/2,.62,.95,a,RB,SA)
 elif kd=='larm':
  oriel30(m,x,y,oc,a,arms=True)
  gable30(m,x,y,(gu0+gu1)/2,gu1-gu0,GN['shoulder'],GN['top'],GN['finial'],a,BB)
  upper_window(m,x,y,(gu0+gu1)/2,GN['window'][0],.90,GN['window'][1]-GN['window'][0],a,BB)
 else:
  # Canted corner: the corner oriel over the shop window.
  # Its front is nearly as wide as the canted face, with short returns (magnified south-west view).
  oriel30(m,x,y,0,a,W0=L,Wf=L-.20,P=.80,z0=3.70,arms=True,cap='dome')
# Mansard: copper to the break, tile above, a flat tile top; the fire-wall faces are rendered.
RF=Z30['roof'];outer,r1,r2,fw=RF['outer'],RF['r1'],RF['r2'],RF['firewall']
def stage(ra,rb,z0,z1,ma):
 n=len(ra)
 for i in range(n):
  j=(i+1)%n;quad=[(*ra[i],z0),(*ra[j],z0),(*rb[j],z1),(*rb[i],z1)]
  if math.dist(rb[i],rb[j])<1e-3:m.faces(quad[:3],[(0,1,2)],OC if fw[i] else ma)
  else:m.faces(quad,[(0,1,2,3)],OC if fw[i] else ma)
stage(outer,r1,H,CT,M['Copper']);stage(r1,r2,CT,TOP,M['Tile'])
top=[p for i,p in enumerate(r2) if i==0 or math.dist(p,r2[i-1])>1e-3]
m.faces([(*p,TOP) for p in top],[tuple(range(len(top)))],M['Tile'])
m.faces([(*p,H-.02) for p in outer],[tuple(range(len(outer)-1,-1,-1))],M['SoffitDark'])
# Dormers on the copper slope and the chimney at the east fire wall.
slope=(CT-H)/1.6
for w in walls('main'):
 x,y,L,a=sf_edge(w['p'],w['q']);kd=kind30(w)
 if kd=='larm':
  for s in (9.72,15.53):roof_dormer(m,x,y,-L/2+s,a,H,slope,.55,.80,.90,M['Copper'],M['Copper'],RB,False)
 elif kd=='sodra':
  for X in (-279.20,-261.31):roof_dormer(m,x,y,uat(w,X,-67.3),a,H,slope,.55,.80,.90,M['Copper'],M['Copper'],RB,False)
box(m,-256.95,-62.75,.70,1.00,TOP+1.25-H,H,OC,0,M['Dark'])
b30_finish(m,'92204170')

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
# Cameras keep their measured distance from the modelled facade (0.355 m proud of the OSM line).
block30_cameras=[
 sv_camera('169_Block30_Cal_Sodra',-266.76,-73.22,2.32,332,32),
 sv_camera('170_Block30_Cal_Larmgatan',-291.03,-57.77,2.50,62,32),
 sv_camera('171_Block30_Corner',-305.96,-73.35,2.30,42,10,40),
 sv_camera('172_Block30_Firewall',-245.43,-73.46,2.37,288,13),
 sv_camera('173_Block30_West',-266.76,-73.22,2.32,285,22),
 ('174_Block30_Aerial',(-318.0,-100.0,40.0),(-272.0,-56.0,8.0),26),
 sv_camera('175_Block30_North_Gable',-291.03,-57.77,2.50,22,18),
]
print('BLOCK30_GEOMETRY',len(block30_names))
