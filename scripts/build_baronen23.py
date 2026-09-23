"""Pass 23: Baronen shopping centre, the former Svea margarine factory at Ölandshamnen.
References: Google Street View April 2025 and September 2021, Kalmar läns museum 2015,
an orthophoto reprojected into the local frame. Zones: source/baronen23.json.
Heights and hidden elevations are estimates; see references/baronen23-notes.md.
Tenant names and logos are omitted; only the building's own name is lettered.
"""
import random
B23=json.loads((R/'source/baronen23.json').read_text());Z=B23['zones'];PT={k:tuple(v) for k,v in B23['points'].items()}
baronen23_names=[];B={}
def lin(c):return tuple(((v+.055)/1.055)**2.4 if v>.04045 else v/12.92 for v in c)
# Measured mean sRGB of each texture set (numpy over the 2048 px PNGs). Tints are
# linear target/linear mean, so the rendered average matches the photographed colour.
MEAN={'TownRose':(.727,.599,.535),'TownIvory':(.841,.824,.765),'TownTileDark':(.352,.288,.225),'TownPaintWhite':(.841,.841,.801),
 'TownMetalGrey':(.371,.421,.397),'TownPanel':(.776,.782,.726),'TownMetalRed':(.564,.299,.233),'TownStone':(.648,.628,.59),
 'TownPaintBlue':(.447,.535,.573),'Baronen23Profiled':(.738,.758,.758),'Baronen23Brick':(.58,.397,.317)}
# Rebuilt every run so colour corrections reach the materials; shared images are reused.
for old in [k for k in list(materials) if k.startswith('M_Baronen23_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('RedRender','TownRose',(.62,.31,.24),.86,0),
 ('WhiteTrim','TownIvory',(.88,.855,.80),.80,0),
 ('Terracotta','TownIvory',(.64,.33,.26),.86,0),
 ('Cream','TownIvory',(.78,.71,.56),.88,0),
 ('Aluminium','TownPaintWhite',(.71,.72,.73),.34,.55),
 ('DarkRoof','TownMetalGrey',(.19,.20,.22),.46,.42),
 ('SlateTile','TownTileDark',(.27,.275,.285),.80,0),
 ('PanelTan','TownPanel',(.74,.58,.40),.72,0),
 ('PanelLight','TownPanel',(.80,.79,.75),.62,0),
 ('Profiled','Baronen23Profiled',(.738,.758,.758),.42,.45),
 ('Grille','TownMetalRed',(.47,.14,.12),.58,.25),
 ('Galvanized','TownPaintWhite',(.60,.62,.62),.42,.78),
 ('Felt','TownStone',(.30,.30,.31),.93,0),
 ('Canvas','TownPanel',(.84,.83,.80),.90,0),
 ('Blue','TownPaintBlue',(.08,.24,.62),.40,0),
 ('Brick','Baronen23Brick',(.58,.397,.317),.82,0),
 ('BrickArch','Baronen23Brick',(.53,.36,.29),.84,0),
 ]:
 name='M_Baronen23_'+key;B[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['baronen23_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
BRICK,BRICKDARK,CONC,ASPH,PAINT,SIGN,PLINTH=B['Brick'],B['BrickArch'],S21['Concrete'],'M_Kvarnholmen_Asphalt',P18['ParkingPaint'],S22['DarkMetal'],S20['DarkPlinth']
ALU=B['Aluminium']

def bz_new(name):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 baronen23_names.append(name);return Mesh(name,'Kvarnholmen/Baronen')
def bz_finish(m):
 obj=s21_finish(m);obj['detail_pass']=23;obj['reference_notes']='references/baronen23-notes.md';obj['osm_way']='38033725';return obj
def ring_offset(poly,d):
 # Mitred offset of a counter-clockwise ring; positive d grows the ring outward.
 n=len(poly);out=[]
 for i in range(n):
  a,b,c=poly[i-1],poly[i],poly[(i+1)%n]
  u1=((b[0]-a[0]),(b[1]-a[1]));l1=math.hypot(*u1);u1=(u1[0]/l1,u1[1]/l1)
  u2=((c[0]-b[0]),(c[1]-b[1]));l2=math.hypot(*u2);u2=(u2[0]/l2,u2[1]/l2)
  n1=(u1[1],-u1[0]);n2=(u2[1],-u2[0]);bis=(n1[0]+n2[0],n1[1]+n2[1]);k=1+n1[0]*n2[0]+n1[1]*n2[1]
  if k<.05:out.append((b[0]+n1[0]*d,b[1]+n1[1]*d));continue
  out.append((b[0]+bis[0]*d/k,b[1]+bis[1]*d/k))
 return out
def walls(zone,kind=None):return [w for w in Z[zone]['walls'] if kind is None or w['kind']==kind]
def outward(w):x,y,L,a=sf_edge(w['p'],w['q']);return (math.sin(a),-math.cos(a))

def bz_wall(m,p,q,z0,z1,holes,ma,o0=.005,o1=.355):
 # p18_face, generalised to walls that start above a lower roof. holes=(u,bottom,w,h,rise)
 x,y,L,a=sf_edge(p,q)
 zs=sorted(set([z0,z1]+[v for u,b,w,h,r in holes for v in (b,b+h+r) if z0<v<z1]))
 for low,high in zip(zs,zs[1:]):
  mid=(low+high)/2;cuts=sorted((u-w/2,u+w/2) for u,b,w,h,r in holes if b<mid<b+h+r);at=-L/2
  for left,right in cuts+[(L/2,L/2)]:
   left=max(-L/2,min(L/2,left));right=max(-L/2,min(L/2,right))
   if left>at+.001:facade_box(m,x,y,(at+left)/2,(o0+o1)/2,mid,left-at,o1-o0,high-low,ma,a)
   at=max(at,right)
 for u,b,w,h,r in holes:
  if r<=0:continue
  # One closed spandrel prism per side, as in lm_wall. Open 24-strip infill has zero-height
  # strips at the crown, and the bevel's overlap clamp then collapses every edge in the mesh.
  for sign in (-1,1):
   outline=[(u,b+h+r),(u+sign*w/2,b+h+r),(u+sign*w/2,b+h)]+[(u+sign*w/2*math.cos(t*math.pi/32),b+h+r*math.sin(t*math.pi/32)) for t in range(1,16)]
   verts=[lp(x,y,uu,o,zz,a) for o in (o0,o1) for uu,zz in outline];n=len(outline)
   m.faces(verts,[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],ma)
def bz_sill(m,x,y,u,b,w,a):
 facade_box(m,x,y,u,.48,b-.04,w+.16,.26,.035,METAL,a)
 for side in [-1,1]:facade_box(m,x,y,u+side*(w/2+.06),.46,b-.01,.025,.22,.06,METAL,a)
def bz_rail(m,x,y,L,z,a,out=.25,h=1.05,ma=None,bars=.13):
 # Galvanised deck railing: posts, top and knee rails and closely spaced balusters.
 ma=ma or B['Galvanized'];n=max(1,round(L/1.8))
 for k in range(n+1):facade_box(m,x,y,-L/2+k*L/n,out,z+h/2,.05,.05,h,ma,a)
 for zz,r in [(z+h,.032),(z+h*.52,.018),(z+.10,.018)]:town_rod(m,lp(x,y,-L/2,out,zz,a),lp(x,y,L/2,out,zz,a),r,ma)
 for k in range(1,round(L/bars)):
  u=-L/2+k*L/round(L/bars);town_rod(m,lp(x,y,u,out,z+.10,a),lp(x,y,u,out,z+h,a),.009,ma,6)

# ---------------------------------------------------------------- facades
def mansard_face(m,w):
 # Salmon render, white lesenes, round-arched windows; continuous canopy over the shops.
 p,q,z0,H=w['p'],w['q'],w['z0'],w['z1'];x,y,L,a=sf_edge(p,q);ox,oy=outward(w)
 # Walls above the mall's own roofs stay plain; above the pavilion or gym they keep windows.
 plain=w['kind']=='upper' and w['neighbour'] in ('mall','cinema','tallbox','southblock','westlink','channel','tower')
 n=max(1,round(L/3.8));step=L/n;us=[-L/2+(k+.5)*step for k in range(n)];holes=[]
 if L>2.4 and not plain:
  for u in us:
   for b,ww,hh,r in [(5.55,1.25,1.55,.62),(8.75,1.10,1.30,.55)]:
    if b>z0+.4:holes.append((u,b,ww,hh,r))
  if z0<.5:
   for k,u in enumerate(us):holes.append((u,0,1.36,2.55,.68) if (k%4==1 if oy>.5 else k==n-1) else (u,.55,2.05,2.25,1.02))
 bz_wall(m,p,q,z0,H,holes,B['RedRender'])
 for u,b,ww,hh,r in holes:
  if b<.1:
   facade_box(m,x,y,u,.14,b+(hh+r)/2,ww,.12,hh+r,SIGN,a)
   for du in [-.34,.34]:facade_box(m,x,y,u+du,.24,b+hh/2+.1,.62,.06,hh-.25,GLAZE,a)
   p18_arch(m,*lp(x,y,u,0,0,a)[:2],b+hh,ww+.16,r+.08,.16,.40,a,B['WhiteTrim'])
  elif b<1:p18_win(m,x,y,u,b,ww,hh,r,a,SIGN,B['WhiteTrim'],1,3)
  else:p18_win(m,x,y,u,b,ww,hh,r,a,TW,B['WhiteTrim'],3,2)
 zb=max(z0,.45);zt=H-.55
 if not plain:
  for k in range(0,n+1,3):
   u=-L/2+k*step;wl=.85 if k in (0,n) else .62;u=max(-L/2+wl/2,min(L/2-wl/2,u))
   facade_box(m,x,y,u,.40,(zb+zt)/2,wl,.10,zt-zb,B['WhiteTrim'],a)
  if z0<.5:
   s20_plinth(m,x,y,L,a,holes,.45)
   p18_band(m,x,y,L,4.98,a,B['WhiteTrim'],.30)
  if z0<.5 and oy>.5:
   # Lean-to canopy: black sheet roof, white fascia and slim columns at the lesenes.
   vs=[lp(x,y,-L/2,.40,4.46,a),lp(x,y,L/2,.40,4.46,a),lp(x,y,L/2,2.0,4.12,a),lp(x,y,-L/2,2.0,4.12,a)]
   m.faces(vs,[(0,1,2,3)],B['DarkRoof']);m.faces([(v[0],v[1],v[2]-.10) for v in vs],[(3,2,1,0)],SIGN)
   facade_box(m,x,y,0,2.0,3.98,L,.07,.28,B['WhiteTrim'],a)
   for k in range(0,n+1,3):
    u=max(-L/2+.3,min(L/2-.3,-L/2+k*step));town_rod(m,lp(x,y,u,1.9,.0,a),lp(x,y,u,1.9,3.86,a),.075,B['WhiteTrim'],12)
  elif z0<5:p18_band(m,x,y,L,max(z0+.1,4.98),a,B['WhiteTrim'],.30)
  facade_box(m,x,y,0,.43,8.45,L,.16,.10,B['WhiteTrim'],a)
 lm_cornice(m,x,y,L,H-.2,a,B['WhiteTrim'])

def roof_dormer(m,x,y,u,a,H,slope,d,w,h,body,hood,frame=None,arched=False):
 # Front plane d metres inside the wall line (+o outward). The body runs back until the
 # main roof reaches its top, so the cheeks emerge from the slope at the right angle.
 frame=frame or TW;zf=H+d*slope;xx,yy,_=lp(x,y,u,-d,0,a);zc=zf+.25+h/2;zs=zf+.25+h
 if arched:t0,c=0.0,w/2+.2
 elif hood==town_mats['MetalRed']:t0,c=math.radians(35),w/2+.26
 else:t0,c=None,w/2+.26
 # Hood profile across the dormer: round head, shallow barrel or a small gable.
 if t0 is None:prof=[(-c,zs+.16),(0,zs+.58),(c,zs+.16)]
 else:
  r=c/math.cos(t0);zo=zs+.16-r*math.sin(t0)
  prof=[(r*math.cos(t),zo+r*math.sin(t)) for t in [math.pi-t0-(math.pi-2*t0)*k/12 for k in range(13)]]
 zt=max(v for _,v in prof);depth=(zt-zf)/slope+.25
 facade_box(m,xx,yy,0,-depth/2,(zf-.2+zs+.16)/2,w+.32,depth,zs+.36-zf,body,a)
 town_window(m,xx,yy,zc,w,h,a,frame,arched,2,2,False)
 facade_box(m,xx,yy,0,.12,zf+.10,w+.40,.34,.08,body,a)
 for (u0,z0),(u1,z1) in zip(prof,prof[1:]):
  m.faces([lp(xx,yy,u0,.24,z0,a),lp(xx,yy,u1,.24,z1,a),lp(xx,yy,u1,-depth,z1,a),lp(xx,yy,u0,-depth,z0,a)],[(0,1,2,3)],hood)
 m.faces([lp(xx,yy,uu,.02,zz,a) for uu,zz in prof],[tuple(range(len(prof)))],body)

def brick_face(m,w,doors=()):
 # 1880s factory brick: lesenes every second bay, arched corbel frieze, dog-tooth band.
 p,q,z0,H=w['p'],w['q'],w['z0'],w['z1'];x,y,L,a=sf_edge(p,q)
 n=max(1,round(L/3.5));step=L/n;us=[-L/2+(k+.5)*step for k in range(n)];holes=[]
 if w['kind']=='outer' and L>2.8:
  for k,u in enumerate(us):
   for b,hh,r in [(1.0,1.60,.22),(4.3,1.60,.22),(7.2,1.45,.2)]:
    if b<1.5 and k in doors:holes.append((u,0,1.45,2.55,.3))
    elif b>z0+.3:holes.append((u,b,1.15,hh,r))
 bz_wall(m,p,q,z0,H,holes,BRICK)
 for u,b,ww,hh,r in holes:
  if b<.1:
   s21_glass(m,x,y,u,b,ww,hh,a,TW,2,.72,True);p18_arch(m,*lp(x,y,u,0,0,a)[:2],b+hh,ww+.18,r+.1,.14,.40,a,BRICKDARK)
   facade_box(m,x,y,u,.26,b+hh+r/2,ww,.06,r,GLAZE,a)
  else:p18_win(m,x,y,u,b,ww,hh,r,a,TW,BRICKDARK,2,2);bz_sill(m,x,y,u,b,ww,a)
 if z0<.6:
  facade_box(m,x,y,0,.40,.25,L,.10,.5,PLINTH,a) if not any(b<.1 for u,b,*_ in holes) else s20_plinth(m,x,y,L,a,holes,.5)
 zb=max(z0,.5);zt=H-1.15
 for k in range(0,n+1,2):
  u=max(-L/2+.26,min(L/2-.26,-L/2+k*step));facade_box(m,x,y,u,.39,(zb+zt)/2,.52,.07,zt-zb,BRICK,a)
 if z0<3.2:
  # Dog-tooth course between ground and first floor, a corbelled row above it.
  facade_box(m,x,y,0,.38,3.30,L,.05,.10,BRICK,a);facade_box(m,x,y,0,.40,3.62,L,.09,.10,BRICK,a)
  for k in range(round(L/.27)):
   u=-L/2+(k+.5)*L/round(L/.27)
   if not any(abs(u-hu)<hw/2+.05 and hb<3.62<hb+hh+hr for hu,hb,hw,hh,hr in holes):facade_box(m,x,y,u,.39,3.46,.12,.08,.12,BRICK,a)
 # Arched corbel frieze between the lesenes, then a stepped brick cornice.
 for k in range(0,n,2):
  u0=-L/2+k*step+.3;u1=min(L/2-.3,-L/2+(k+2)*step-.3);cnt=max(1,round((u1-u0)/.46))
  for j in range(cnt):
   uc=u0+(j+.5)*(u1-u0)/cnt;xx,yy,_=lp(x,y,uc,0,0,a);p18_arch(m,xx,yy,H-.98,(u1-u0)/cnt-.08,.19,.07,.40,a,BRICK,8)
   facade_box(m,x,y,uc+(u1-u0)/cnt/2,.40,H-1.1,.07,.07,.24,BRICK,a)
 for zz,d in [(H-.66,.08),(H-.46,.14),(H-.26,.20),(H-.08,.26)]:facade_box(m,x,y,0,.355+d/2,zz,L+2*d,d,.18,BRICK,a)

def cream_face(m,w,entrance=None,floors=(.95,3.95,6.95),H0=None):
 p,q,z0,H=w['p'],w['q'],w['z0'],w['z1'];x,y,L,a=sf_edge(p,q)
 n=max(1,round(L/3.2));step=L/n;us=[-L/2+(k+.5)*step for k in range(n)];holes=[]
 if L>2.2:
  for k,u in enumerate(us):
   if entrance is not None and k==entrance:holes.append((u,0,1.9,2.55,0));continue
   for b in floors:
    if b>z0+.3 and b+1.4<H-.3:holes.append((u,b,1.12,1.38,0))
 bz_wall(m,p,q,z0,H,holes,B['Cream'])
 for u,b,ww,hh,r in holes:
  if b<.1:
   s21_glass(m,x,y,u,b,ww,hh,a,ALU,2,.78,True)
   # Home-hotel style entrance box: white metal frame projecting from the render.
   facade_box(m,x,y,u,1.25,2.95,ww+.95,1.9,.42,B['WhiteTrim'],a)
   for side in [-1,1]:facade_box(m,x,y,u+side*(ww/2+.42),1.25,1.37,.11,1.9,2.75,B['WhiteTrim'],a)
  else:sf_modern(m,x,y,u,b,ww,hh,a,TW,B['WhiteTrim'],1,2)
 if z0<.5:s20_plinth(m,x,y,L,a,holes,.42)
 for k in range(0,n+1,3):
  u=max(-L/2+.25,min(L/2-.25,-L/2+k*step));facade_box(m,x,y,u,.385,(max(z0,.42)+H-.1)/2,.48,.06,H-.1-max(z0,.42),B['Cream'],a)
 # Red-painted eaves board and gutter, as on the Packhuset entrance photograph.
 facade_box(m,x,y,0,.62,H-.06,L+.5,.55,.14,B['WhiteTrim'],a);facade_box(m,x,y,0,.90,H-.02,L+.5,.07,.22,town_mats['MetalRed'],a)
 town_rod(m,lp(x,y,-L/2-.2,.98,H+.06,a),lp(x,y,L/2+.2,.98,H+.06,a),.07,town_mats['MetalRed'],10)

def curtain(m,p,q,z0,z1,rails,col=1.3,spandrels=(),frame=None,glass=None,door=False):
 # Stick-built aluminium curtain wall; opaque bands for floor slabs and signs.
 frame=frame or ALU;glass=glass or GLAZE;x,y,L,a=sf_edge(p,q)
 facade_box(m,x,y,0,.08,(z0+z1)/2,L,.05,z1-z0,glass,a)
 n=max(1,round(L/col))
 for k in range(n+1):facade_box(m,x,y,-L/2+k*L/n,.17,(z0+z1)/2,.16 if k in (0,n) else .075,.18,z1-z0,frame,a)
 for z in [z0+.05]+[r for r in rails if z0<r<z1]+[z1-.04]:facade_box(m,x,y,0,.17,z,L,.16,.075,frame,a)
 for s0,s1,ma in spandrels:
  s0=max(s0,z0);s1=min(s1,z1)
  if s1>s0:facade_box(m,x,y,0,.135,(s0+s1)/2,L,.07,s1-s0,ma,a)
 if door and z0<.1:
  for du in [-.62,.62]:facade_box(m,x,y,du,.23,1.14,.05,.10,2.28,frame,a)
  facade_box(m,x,y,0,.23,2.30,2.5,.10,.08,frame,a)
  for du in [-.1,.1]:town_rod(m,lp(x,y,du,.28,.85,a),lp(x,y,du,.28,1.45,a),.016,METAL)
 return n

def tower_face(m,w,front=False):
 p,q,z0=w['p'],w['q'],w['z0'];top=Z['tower']['height'];x,y,L,a=sf_edge(p,q)
 n=curtain(m,p,q,z0,top,[2.95,4.8,5.5,7.95,10.2],1.3,[(4.8,5.5,B['WhiteTrim'])],door=front);step=L/n
 # Clerestory of small square panes and the tubular X-bracing behind the tall lights.
 for k in range(n):
  u=-L/2+(k+.5)*step
  if z0<10.2:facade_box(m,x,y,u,.16,10.75,.045,.12,1.1,ALU,a)
  for zb,zt in [(5.5,7.95),(7.95,10.2),(2.95,4.8)]:
   if zb<z0-.01:continue
   u0,u1=-L/2+k*step+.08,-L/2+(k+1)*step-.08
   if zb<3:
    town_rod(m,lp(x,y,u0,.125,zb+.05,a),lp(x,y,(u0+u1)/2,.125,zt-.05,a),.028,ALU);town_rod(m,lp(x,y,(u0+u1)/2,.125,zt-.05,a),lp(x,y,u1,.125,zb+.05,a),.028,ALU)
   else:
    town_rod(m,lp(x,y,u0,.125,zb+.06,a),lp(x,y,u1,.125,zt-.06,a),.032,ALU);town_rod(m,lp(x,y,u1,.125,zb+.06,a),lp(x,y,u0,.125,zt-.06,a),.032,ALU)
 if z0<10.2:facade_box(m,x,y,0,.16,10.75,L,.12,.04,ALU,a)
 if front:
  xx,yy,_=lp(x,y,0,.30,0,a);town_text(m,xx,yy,8.95,a,'BARONEN',min(4.9,L*.66),B['Blue'])

def retail_face(m,w,rng):
 # Quay shop row under the parking deck: terracotta render, shop windows, awnings, parapet.
 p,q,z0,H=w['p'],w['q'],w['z0'],w['z1'];x,y,L,a=sf_edge(p,q);mid=((p[0]+q[0])/2,(p[1]+q[1])/2)
 bryggan=mid[0]>-182 and mid[1]<-352
 holes=[];units=max(1,round(L/7.0));uw=L/units
 for k in range(units):
  c=-L/2+(k+.5)*uw
  if bryggan:holes.append((c,.30,uw-.9,2.95,0));continue
  kind=rng.random()
  if kind<.55:holes.append((c-.6,.32,min(4.2,uw-2.2),2.95,0));holes.append((c+uw/2-1.05,0,1.0,2.25,0))
  elif kind<.8:holes.append((c,0,1.0,2.25,0));holes.append((c-1.9,2.15,.85,.85,0));holes.append((c+1.9,2.15,.85,.85,0))
  else:holes.append((c,.32,min(5.8,uw-.8),2.95,0))
 bz_wall(m,p,q,z0,H,holes,B['Terracotta'])
 for u,b,ww,hh,r in holes:
  if b<.1:s21_glass(m,x,y,u,b,ww,hh,a,SIGN,1,.0,True)
  elif hh<1:sf_modern(m,x,y,u,b,ww,hh,a,SIGN,SIGN,1,1)
  else:
   s21_glass(m,x,y,u,b,ww,hh,a,ALU if bryggan else SIGN,max(2,round(ww/1.4)),.0 if bryggan else .82)
   if not bryggan and rng.random()<.55:s21_shallow_awning(m,x,y,u,3.78,ww+.3,a,B['Canvas'],1.25)
 s20_plinth(m,x,y,L,a,holes,.30)
 if bryggan:
  # Restaurant Bryggan: white profiled cladding with portholes above the glazing.
  facade_box(m,x,y,0,.40,3.92,L,.10,1.35,B['Profiled'],a)
  for k in range(max(1,round(L/2.4))):s20_round(m,x,y,-L/2+(k+.5)*L/max(1,round(L/2.4)),3.92,.24,a,ALU,.46)
 facade_box(m,x,y,0,.40,H+.45,L,.12,.9,CONC,a);facade_box(m,x,y,0,.30,H+.93,L+.2,.62,.08,CONC,a)
 bz_rail(m,x,y,L,H+.97,a,.26,1.10)

def gym_face(m,w):
 p,q,z0,H=w['p'],w['q'],w['z0'],w['z1'];x,y,L,a=sf_edge(p,q);ox,oy=outward(w)
 west=ox<-.5 and oy>0 and w['kind']=='outer'
 if w['kind']=='upper':
  bz_wall(m,p,q,z0,H,[],B['Profiled']);facade_box(m,x,y,0,.40,H-.25,L,.10,.5,ALU,a);return
 if west:
  # Service bays: red square-mesh screens, a dark loading bay and the garage ramp portal.
  holes=[(-L/2+5.2,0,5.0,3.8,0),(L/2-4.4,0,3.6,2.45,0)]
  bz_wall(m,p,q,4.2,H,[(0,5.1,L-1.4,2.6,0)],B['Profiled'])
  bz_wall(m,p,q,0,4.2,holes,B['Grille'],.005,.12)
  for u,b,ww,hh,r in holes:
   facade_box(m,x,y,u,-2.8,b+hh/2,ww,.2,hh,SIGN,a)
   for side in [-1,1]:facade_box(m,x,y,u+side*ww/2,-1.4,b+hh/2,.2,2.8,hh,CONC,a)
   facade_box(m,x,y,u,-1.4,b+hh+.1,ww,2.8,.2,CONC,a)
  for u0,u1 in [(-L/2+.2,-L/2+2.6),(-L/2+7.8,L/2-6.4),(L/2-2.5,L/2-.2)]:
   facade_box(m,x,y,(u0+u1)/2,.20,2.0,u1-u0,.03,4.0,B['Grille'],a)
   for k in range(int((u1-u0)/.11)):facade_box(m,x,y,u0+(k+.5)*.11,.25,2.0,.022,.06,4.0,B['Grille'],a)
   for k in range(int(4.0/.11)):facade_box(m,x,y,(u0+u1)/2,.27,.05+k*.11,u1-u0,.05,.022,B['Grille'],a)
  for u in [-L/2+2.7,-L/2+7.7,L/2-6.3,L/2-2.5]:facade_box(m,x,y,u,.30,2.1,.26,.30,4.2,SIGN,a)
  s21_glass(m,x,y,0,5.1,L-1.4,2.6,a,ALU,max(2,round((L-1.4)/1.5)),0)
  facade_box(m,x,y,0,.42,4.28,L,.16,.16,ALU,a);facade_box(m,x,y,0,.42,H-.28,L,.14,.56,ALU,a)
  return
 # Harbour end of the gym: two storeys of red render with large square windows and a stair.
 holes=[(-L/4,0,1.0,2.25,0),(L/4,1.1,1.4,1.3,0)]+[(u,5.0,2.3,2.0,0) for u in ((-L/4,L/4) if L<10 else (-L/2+3.0,0,L/2-3.0))]
 bz_wall(m,p,q,z0,H,holes,B['RedRender'])
 for u,b,ww,hh,r in holes:
  if b<.1:s20_door(m,x,y,u,b,ww,hh,a,SIGN)
  else:sf_modern(m,x,y,u,b,ww,hh,a,SIGN,B['WhiteTrim'],1,2)
 s20_plinth(m,x,y,L,a,holes,.35);facade_box(m,x,y,0,.42,H-.2,L,.2,.4,B['WhiteTrim'],a)

def panel_face(m,w,ma,frame,fascia):
 # Tall cinema box: pale framed fields under a light fascia; the south block: dark fascia.
 p,q,z0,H=w['p'],w['q'],w['z0'],w['z1'];x,y,L,a=sf_edge(p,q)
 bz_wall(m,p,q,z0,H,[],ma)
 facade_box(m,x,y,0,.40,H-fascia/2,L+.1,.10,fascia,frame,a)
 if L>6 and ma==B['PanelTan']:
  nf=max(1,round(L/12.5))
  for k in range(nf+1):u=max(-L/2+.3,min(L/2-.3,-L/2+k*L/nf));facade_box(m,x,y,u,.39,(z0+H-fascia)/2,.55,.08,H-fascia-z0,frame,a)
  facade_box(m,x,y,0,.39,z0+.3,L,.08,.6,frame,a)
  if nf>=3:
   # The middle field is quartered in the April 2025 harbour view.
   c=-L/2+1.5*L/nf;hz=(z0+H-fascia)/2
   facade_box(m,x,y,c,.385,hz,.22,.07,H-fascia-z0-.6,frame,a);facade_box(m,x,y,c,.385,hz,L/nf-.5,.07,.22,frame,a)

def surface_door(m,x,y,u,b,w,h,a):
 facade_box(m,x,y,u,.385,b+h/2,w,.06,h,SIGN,a)
 for side in (-1,1):facade_box(m,x,y,u+side*(w/2+.05),.40,b+h/2,.10,.10,h+.1,ALU,a)
 facade_box(m,x,y,u,.40,b+h+.05,w+.2,.10,.10,ALU,a);town_rod(m,lp(x,y,u+w*.3,.45,b+1.0,a),lp(x,y,u+w*.3,.45,b+1.2,a),.018,METAL)
def plain_face(m,w,ma,windows=0):
 p,q,z0,H=w['p'],w['q'],w['z0'],w['z1'];x,y,L,a=sf_edge(p,q);holes=[]
 if windows and L>4:
  for k in range(min(windows,round(L/4))):holes.append((-L/2+(k+.5)*L/min(windows,round(L/4)),max(z0+.9,1.0),1.1,1.3,0))
 bz_wall(m,p,q,z0,H,holes,ma)
 for u,b,ww,hh,r in holes:sf_modern(m,x,y,u,b,ww,hh,a,ALU,ma,1,2)
 facade_box(m,x,y,0,.30,H+.12,L+.2,.50,.24,CONC if ma!=CONC else B['PanelLight'],a)

# ------------------------------------------------------------------ roofs
def inset_roof(m,poly,H,inset,rise,ma,ov=.45,top=None,drop=None):
 # Outer ring over the cornice, a steep or hipped slope, then a flat top.
 outer=ring_offset(poly,ov);inner=ring_offset(poly,-inset);n=len(poly);z0=H if drop is None else H-drop
 for i in range(n):
  j=(i+1)%n;m.faces([(*outer[i],z0),(*outer[j],z0),(*inner[j],H+rise),(*inner[i],H+rise)],[(0,1,2,3)],ma)
 m.faces([(*v,H+rise) for v in inner],[tuple(range(n))],top or ma)
 m.faces([(*v,z0-.12) for v in outer],[tuple(range(n-1,-1,-1))],SIGN)
 for i in range(n):
  j=(i+1)%n;town_rod(m,(*outer[i],z0-.02),(*outer[j],z0-.02),.06,ma,8)
 return outer,inner

def strip_roof(m,outer,inner,H,rise,ma,ov=.45,hip_start=False,hip_end=False,gable_ma=None):
 # Bent gable/hip roof over a strip given by its two eave polylines (mitred corners).
 n=len(outer)
 def mid(a,b):return ((a[0]+b[0])/2,(a[1]+b[1])/2)
 def dirn(a,b):d=math.dist(a,b);return ((b[0]-a[0])/d,(b[1]-a[1])/d)
 def meet2(p,u,q,v):
  det=u[0]*(-v[1])-u[1]*(-v[0])
  if abs(det)<1e-9:return q
  t=((q[0]-p[0])*(-v[1])-(q[1]-p[1])*(-v[0]))/det;return (p[0]+u[0]*t,p[1]+u[1]*t)
 def extend(line,end,s):
  a,b=(line[0],line[1]) if end==0 else (line[-1],line[-2]);d=math.dist(a,b);return (a[0]+(a[0]-b[0])/d*s,a[1]+(a[1]-b[1])/d*s)
 # Each wing's ridge is its own mid-line; bends sit where neighbouring mid-lines meet.
 R=[mid(outer[0],inner[0])]
 for i in range(1,n-1):R.append(meet2(mid(outer[i-1],inner[i-1]),dirn(outer[i-1],outer[i]),mid(outer[i+1],inner[i+1]),dirn(outer[i+1],outer[i])))
 R.append(mid(outer[-1],inner[-1]))
 half=[math.dist(outer[i],inner[i])/2 for i in (0,n-1)]
 def off(line,other):
  # Mitred offset of an eave polyline away from the opposite eave by the overhang.
  res=[]
  for i in range(n):
   ns=[]
   for j in (i-1,i):
    if 0<=j<n-1:
     u=dirn(line[j],line[j+1]);nn=(u[1],-u[0]);ref=other[j]
     if (ref[0]-line[j][0])*nn[0]+(ref[1]-line[j][1])*nn[1]>0:nn=(-nn[0],-nn[1])
     ns.append(nn)
   if len(ns)==1:res.append((line[i][0]+ns[0][0]*ov,line[i][1]+ns[0][1]*ov));continue
   bis=(ns[0][0]+ns[1][0],ns[0][1]+ns[1][1]);k=1+ns[0][0]*ns[1][0]+ns[0][1]*ns[1][1]
   res.append((line[i][0]+bis[0]*ov/k,line[i][1]+bis[1]*ov/k))
  return res
 O=off(outer,inner);I=off(inner,outer);ze=H-ov*rise/min(half);zr=H+rise
 # Verges run past gable walls; hipped ends pull the ridge in by half the span.
 if hip_start:R[0]=extend(R,0,-half[0])
 else:O[0]=extend(O,0,ov);I[0]=extend(I,0,ov);R[0]=extend(R,0,ov)
 if hip_end:R[-1]=extend(R,1,-half[-1])
 else:O[-1]=extend(O,1,ov);I[-1]=extend(I,1,ov);R[-1]=extend(R,1,ov)
 for i in range(len(O)-1):
  m.faces([(*O[i],ze),(*O[i+1],ze),(*R[i+1],zr),(*R[i],zr)],[(0,1,2,3)],ma)
  m.faces([(*I[i+1],ze),(*I[i],ze),(*R[i],zr),(*R[i+1],zr)],[(0,1,2,3)],ma)
 for k,(e_o,e_i,r) in enumerate([(O[0],I[0],R[0]),(O[-1],I[-1],R[-1])]):
  hip=hip_start if k==0 else hip_end
  if hip:m.faces([(*e_o,ze),(*r,zr),(*e_i,ze)] if k==0 else [(*e_i,ze),(*r,zr),(*e_o,ze)],[(0,1,2)],ma)
  else:
   # Gable triangle sits in the wall plane, not at the verge.
   wo,wi=(outer[0],inner[0]) if k==0 else (outer[-1],inner[-1]);wr=((wo[0]+wi[0])/2,(wo[1]+wi[1])/2)
   m.faces([(*wo,H),(*wi,H),(*wr,zr)] if k==0 else [(*wi,H),(*wo,H),(*wr,zr)],[(0,1,2)],gable_ma or ma)
 for line in (O,I):
  for i in range(len(line)-1):town_rod(m,(*line[i],ze-.05),(*line[i+1],ze-.05),.07,METAL,8)
 for i in range(len(R)-1):town_rod(m,(*R[i],zr+.04),(*R[i+1],zr+.04),.09,ma,8)
 return O,I,R,ze,zr

def octagon_roof(m):
 poly=[tuple(p) for p in B23['octagon']['polygon']];cx,cy=B23['octagon']['centre'];glass_top=Z['tower']['height']
 band=ring_offset(poly,.20);edge=ring_offset(poly,1.35);n=len(poly)
 for i in range(n):
  j=(i+1)%n;x,y,L,a=sf_edge(poly[i],poly[j]);facade_box(m,x,y,0,.17,glass_top+.33,L+.3,.22,.66,SIGN,a)
 z1,z2=glass_top+.66,glass_top+1.22
 m.faces([(*v,z1) for v in edge],[tuple(range(n-1,-1,-1))],SIGN)
 for i in range(n):
  j=(i+1)%n
  m.faces([(*edge[i],z1),(*edge[j],z1),(*edge[j],z2),(*edge[i],z2)],[(0,1,2,3)],SIGN)
  m.faces([(*edge[i],z2),(*edge[j],z2),(cx,cy,glass_top+2.7)],[(0,1,2)],B['DarkRoof'])
  town_rod(m,(*edge[i],z2+.02),(cx,cy,glass_top+2.72),.05,B['DarkRoof'],8)
 m.cylinder(cx,cy,glass_top+2.6,.35,.35,B['DarkRoof'],12)

def dome(m):
 cx,cy=B23['dome']['centre'];r=B23['dome']['radius'];z=Z['mall']['height']+.07
 m.cylinder(cx,cy,z,r+.25,.55,CONC,24)
 prof=[(r,0)]+[(r*math.cos(t*math.pi/2/8),2.1*math.sin(t*math.pi/2/8)) for t in range(1,8)]+[(.2,2.1)]
 m.lathe(cx,cy,z+.55,prof,GLAZE,32)
 for k in range(16):
  t=k*math.tau/16;pts=[(cx+(rr+.03)*math.cos(t),cy+(rr+.03)*math.sin(t),z+.55+h+.02) for rr,h in prof]
  town_path(m,pts,.045,ALU)
 town_path(m,[(cx+(r+.03)*math.cos(k*math.tau/32),cy+(r+.03)*math.sin(k*math.tau/32),z+.58) for k in range(33)],.05,ALU)

def box(m,cx,cy,w,d,h,z,ma,ang=0,lid=None):
 m.box((cx,cy,z+h/2),(w,d,h),ma,ang)
 if lid:m.box((cx,cy,z+h+.04),(w+.12,d+.12,.08),lid,ang)

# ---------------------------------------------------------------- build
rng=random.Random(2309)
# Mansard house (Coop): north wing on Skeppsbrogatan and the west wing to the harbour gable.
m=bz_new('SM_Kvarnholmen_House_38033725');H=Z['mansard']['height'];MR=Z['mansard']['top']-H;ms=MR/1.45
for zone in ('mansard','mansard_s'):
 for w in walls(zone):mansard_face(m,w)
 for poly in Z[zone]['polygons']:inset_roof(m,[tuple(p) for p in poly],H,1.0,MR,B['DarkRoof'],.45,B['DarkRoof'])
for w in walls('mansard','outer')+walls('mansard_s','outer'):
 x,y,L,a=sf_edge(w['p'],w['q']);n=max(1,round(L/3.8));step=L/n
 if L<6:continue
 for k in range(n):
  if k%2==0 or n<3:roof_dormer(m,x,y,-L/2+(k+.5)*step,a,H+.45*ms,ms,.02,.9,.95,B['DarkRoof'],B['DarkRoof'],TW,True)
for cxy in [(-236.0,-272.0),(-214.0,-276.5),(-267.0,-281.5)]:
 box(m,*cxy,.9,.7,1.5,H+MR-.05,B['WhiteTrim'],0,B['DarkRoof'])
bz_finish(m)

# Entrance octagon, the three-storey glass link and the glazed slot to the brick gable.
m=bz_new('SM_Baronen23_Entrance')
front_mid=(B23['octagon']['centre'][0],B23['octagon']['centre'][1]+B23['octagon']['half'][1])
for w in walls('tower'):
 mid=((w['p'][0]+w['q'][0])/2,(w['p'][1]+w['q'][1])/2);tower_face(m,w,front=math.dist(mid,front_mid)<1.0 and w['kind']=='outer')
octagon_roof(m)
for w in walls('westlink'):
 if w['kind']=='outer':curtain(m,w['p'],w['q'],w['z0'],w['z1'],[4.5,5.3,8.2,8.6],1.3,[(4.5,5.3,SIGN),(8.2,8.6,ALU),(10.55,11.0,ALU)],door=math.dist(w['p'],w['q'])>5)
 else:plain_face(m,w,ALU)
s21_flat_roof(m,[tuple(p) for p in Z['westlink']['polygons'][0]],Z['westlink']['height'],B['Felt'])
for w in walls('channel'):
 if outward(w)[1]>.5:curtain(m,w['p'],w['q'],0,w['z1'],[3.8,4.4],1.25,[(3.8,4.4,SIGN),(7.15,7.6,ALU)],door=True)
 else:plain_face(m,w,CONC,1)
s21_flat_roof(m,[tuple(p) for p in Z['channel']['polygons'][0]],Z['channel']['height'],B['Felt'])
bz_finish(m)

# Brick factory, the L-shaped 1880s wing along Skeppsbrogatan and the Skeppsbron gable.
m=bz_new('SM_Baronen23_Factory')
for w in walls('brick'):
 L=math.dist(w['p'],w['q']);brick_face(m,w,doors=(1,6,11) if L>40 else ((2,) if L>18 else ()))
S=B23['strips']['brick'];Hb=Z['brick']['height'];rise=Z['brick']['top']-Hb
O,I,Rr,ze,zr=strip_roof(m,[tuple(p) for p in S['eave_outer']],[tuple(p) for p in S['eave_inner']],Hb,rise,B['SlateTile'],.45,gable_ma=BRICK)
bs=rise/(math.dist(S['eave_outer'][0],S['eave_inner'][0])/2)
for i in range(len(S['eave_outer'])-1):
 p,q=S['eave_outer'][i],S['eave_outer'][i+1];x,y,L,a=sf_edge(q,p)
 for u in [v for v in [-L/2+4.0+j*7.0 for j in range(20)] if v<L/2-3.5]:roof_dormer(m,x,y,u,a,Hb,bs,.9,1.05,1.05,B['DarkRoof'],B['SlateTile'])
for cxy in [(-160.0,-286.0),(-126.0,-292.5)]:box(m,*cxy,.8,.8,2.4,zr-1.4,BRICK,0,CONC)
bz_finish(m)

# Home Hotel Packhuset (cream, red tiles), the inner courtyard wing and the annex.
m=bz_new('SM_Baronen23_Packhuset')
ne_face=[w for w in walls('hotel','outer') if outward(w)[0]>.5 and outward(w)[1]>.5]
entrance_wall=min(ne_face,key=lambda w:math.dist(((w['p'][0]+w['q'][0])/2,(w['p'][1]+w['q'][1])/2),PT['J1'])) if ne_face else None
for w in walls('hotel'):
 L=math.dist(w['p'],w['q']);ent=None
 if w is entrance_wall:ent=max(0,round(L/3.2)-1)
 cream_face(m,w,ent)
S=B23['strips']['hotel'];Hh=Z['hotel']['height'];rise=Z['hotel']['top']-Hh
O,I,Rr,ze,zr=strip_roof(m,[tuple(p) for p in S['eave_outer']],[tuple(p) for p in S['eave_inner']],Hh,rise,TT,.45,hip_end=True,gable_ma=B['Cream'])
for i in range(len(S['eave_outer'])-1):
 p,q=S['eave_outer'][i],S['eave_outer'][i+1];x,y,L,a=sf_edge(q,p);hs=rise/(math.dist(S['eave_outer'][i],S['eave_inner'][i])/2 if i==0 else math.dist(S['eave_outer'][-1],S['eave_inner'][-1])/2)
 for u in [v for v in [-L/2+3.5+j*6.4 for j in range(20)] if v<L/2-3.5]:roof_dormer(m,x,y,u,a,Hh,hs,.8,1.0,.95,town_mats['MetalRed'],town_mats['MetalRed'])
for w in walls('inner'):cream_face(m,w)
S=B23['strips']['inner'];Hi=Z['inner']['height']
strip_roof(m,[tuple(p) for p in S['eave_outer']],[tuple(p) for p in S['eave_inner']],Hi,Z['inner']['top']-Hi,TT,.45,gable_ma=B['Cream'])
for w in walls('annex'):cream_face(m,w,floors=(.95,3.6))

inset_roof(m,[tuple(p) for p in Z['annex']['polygons'][0]],Z['annex']['height'],2.4,Z['annex']['top']-Z['annex']['height'],TT,.40)
bz_finish(m)

# Mall halls: central street under the glazed dome, the tall pale box and the south block.
m=bz_new('SM_Baronen23_Halls')
for w in walls('mall'):plain_face(m,w,CONC,2 if w['kind']=='outer' else 0)
for poly in Z['mall']['polygons']:s21_flat_roof(m,[tuple(p) for p in poly],Z['mall']['height'],B['Felt'])
dome(m)
for w in walls('tallbox'):panel_face(m,w,B['PanelTan'],B['PanelLight'],2.1)
s21_flat_roof(m,[tuple(p) for p in Z['tallbox']['polygons'][0]],Z['tallbox']['height'],B['Felt'])
# Biostaden: the tall red auditorium block behind the deck, with silver ducts on its south face.
for w in walls('cinema'):
 plain_face(m,w,B['RedRender'])
 x,y,L,a=sf_edge(w['p'],w['q'])
 if w['kind']=='outer' and L>3:surface_door(m,x,y,0,0,1.3,2.4,a)
 if outward(w)[1]<-.3 and L>6:
  for k,z in enumerate((w['z1']-7.5,w['z1']-6.6)):town_rod(m,lp(x,y,-L/2+1.0,.75+.5*k,z,a),lp(x,y,L/2-1.0,.75+.5*k,z,a),.28-.06*k,ALU,16)
for poly in Z['cinema']['polygons']:s21_flat_roof(m,[tuple(p) for p in poly],Z['cinema']['height'],SIGN)
box(m,-253.5,-305.0,3.4,2.2,1.6,Z['cinema']['height']+.07,SIGN,math.atan2(.6,.8),B['Galvanized'])
for w in walls('southblock'):
 panel_face(m,w,CONC,SIGN,1.35)
 if w['neighbour']=='deck' and math.dist(w['p'],w['q'])>12:
  x,y,L,a=sf_edge(w['p'],w['q'])
  for u in (-L/4,L/4):surface_door(m,x,y,u,Z['deck']['height'],1.2,2.2,a)
s21_flat_roof(m,[tuple(p) for p in Z['southblock']['polygons'][0]],Z['southblock']['height'],B['Felt'])
for w in walls('plant'):plain_face(m,w,CONC)
s21_flat_roof(m,[tuple(p) for p in Z['plant']['polygons'][0]],Z['plant']['height'],B['Felt'])
# Roof plant read from the orthophoto: fan housings and ducts, positions approximate.
for cx_,cy_,w_,d_,h_,zone in [(-200.0,-298.0,2.2,1.6,1.3,'mall'),(-199.5,-312.0,3.6,2.2,1.6,'mall'),(-180.0,-314.0,4.4,2.0,1.4,'mall'),(-220.0,-300.0,2.6,2.0,1.2,'mall'),(-236.0,-322.0,3.0,2.4,1.5,'tallbox'),(-205.0,-333.0,3.2,2.2,1.4,'southblock'),(-183.0,-343.0,2.4,1.8,1.1,'southblock'),(-156.0,-346.0,3.4,2.4,1.5,'plant'),(-152.0,-352.0,2.0,1.6,1.1,'plant')]:
 box(m,cx_,cy_,w_,d_,h_,Z[zone]['height']+.07,B['PanelLight'],0,B['Galvanized'])
bz_finish(m)

# Harbour side: the single-storey quay shops, the parking deck on their roof, the gym box.
m=bz_new('SM_Baronen23_Harbour')
for w in walls('deck'):
 if w['kind']=='outer':retail_face(m,w,rng)
deck=[tuple(p) for p in Z['deck']['polygons'][0]];Hd=Z['deck']['height']
m.faces([(x,y,Hd+.02) for x,y in deck],[tuple(range(len(deck)))],ASPH)
for w in walls('deck','outer'):
 x,y,L,a=sf_edge(w['p'],w['q'])
 if L<6:continue
 # Perpendicular bays along the parapet, lamp posts every fourth bay.
 nb=int((L-1.0)/2.5)
 for k in range(nb+1):
  u=-L/2+.5+k*2.5;facade_box(m,x,y,u,-3.0,Hd+.035,.10,4.8,.012,PAINT,a)
  if k%6==3:
   pole=lp(x,y,u,-.5,Hd,a);town_rod(m,pole,(pole[0],pole[1],Hd+4.2),.055,B['Galvanized'],10)
   head=lp(x,y,u,-.95,Hd+4.2,a);town_rod(m,(pole[0],pole[1],Hd+4.2),head,.035,B['Galvanized'],8);m.cylinder(head[0],head[1],Hd+4.05,.28,.14,B['Galvanized'],16)
# Stair and lift house plus the glazed Bryggan pavilion, both visible on the orthophoto.
box(m,-229.5,-353.0,7.2,4.6,3.1,Hd,CONC,math.radians(-18),B['Felt'])
xx,yy,_=(-229.5,-353.0,0);facade_box(m,xx,yy,0,2.35,Hd+1.1,1.2,.08,2.2,SIGN,math.radians(-18)+math.pi)
box(m,-189.4,-360.2,8.6,5.0,.25,Hd+3.0,B['PanelLight'],math.radians(-6))
for sx in (-1,1):
 for sy in (-1,1):box(m,-189.4+sx*4.1*math.cos(math.radians(-6))-sy*2.3*math.sin(math.radians(-6)),-360.2+sx*4.1*math.sin(math.radians(-6))+sy*2.3*math.cos(math.radians(-6)),.12,.12,3.0,Hd,ALU,math.radians(-6))
box(m,-189.4,-360.2,8.3,4.7,2.9,Hd+.05,GLAZE,math.radians(-6))
for w in walls('gym'):gym_face(m,w)
# Mister York pavilion: two glazed storeys, dark fascia between them, a ribbed glass roof.
for w in walls('pavilion'):
 if w['kind']=='outer':curtain(m,w['p'],w['q'],0,w['z1'],[3.3,3.9],1.5,[(3.3,3.9,SIGN),(7.2,7.6,ALU)],door=math.dist(w['p'],w['q'])>9)
poly=[tuple(p) for p in Z['pavilion']['polygons'][0]];Hp=Z['pavilion']['height']
m.faces([(x,y,Hp+.05) for x,y in poly],[tuple(range(len(poly)))],GLAZE)
for pq in zip(poly,poly[1:]+poly[:1]):
 x,y,L,a=sf_edge(*pq);facade_box(m,x,y,0,.10,Hp+.10,L+.2,.25,.20,ALU,a)
c0,c1=poly[0],poly[1];c3=poly[-1]
for k in range(1,9):
 t=k/9;town_rod(m,(c0[0]+(c1[0]-c0[0])*t,c0[1]+(c1[1]-c0[1])*t,Hp+.12),(c3[0]+(poly[2][0]-c3[0])*t,c3[1]+(poly[2][1]-c3[1])*t,Hp+.12),.04,ALU,6)
s21_flat_roof(m,[tuple(p) for p in Z['gym']['polygons'][0]],Z['gym']['height'],B['Felt'])
bz_finish(m)

def street_view_camera(name,lat,lon,heading,pitch,vfov=50,h=2.5,match='width'):
 # Matches a Google Street View view for side-by-side calibration (same position and heading).
 e=(lon-16.3656)*111320*math.cos(math.radians(56.66412));nn=(lat-56.66412)*111320;ar=math.radians(28.2)
 x=e*math.cos(ar)+nn*math.sin(ar);y=-e*math.sin(ar)+nn*math.cos(ar);b=math.radians(heading+28.2)
 t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 # 'width' keeps the 1512 x 812 panorama's horizontal view; 'height' matches its vertical
 # field of view in the 1600 x 1000 review shot, for pixel comparisons of heights.
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),h),tuple(round(v,2) for v in t),round(lens,2))
baronen23_cameras=[
 street_view_camera('112_Baronen_Entrance',56.6614368,16.3647238,150,5),
 street_view_camera('113_Baronen_Mansard',56.6612328,16.3639655,150,6),
 street_view_camera('114_Baronen_Factory',56.6615401,16.3659835,172,5),
 street_view_camera('115_Baronen_Packhuset',56.6614705,16.3662017,200,6),
 street_view_camera('116_Baronen_Harbour',56.6598206,16.364559,5,4),
 street_view_camera('117_Baronen_Gym',56.6607394,16.3631684,122,3),
 ('118_Baronen_Aerial',(-70.0,-430.0,78.0),(-195.0,-312.0,4.0),24),
 ('119_Baronen_Deck',(-203.0,-357.5,6.3),(-250.0,-338.0,9.0),20),
 street_view_camera('120_Baronen_Cal_Entrance',56.6614368,16.3647238,150,5,match='height'),
 street_view_camera('121_Baronen_Cal_Packhuset',56.6614705,16.3662017,200,6,match='height'),
 street_view_camera('122_Baronen_Cal_Harbour',56.6598206,16.364559,5,4,match='height'),
]
print('BARONEN23_GEOMETRY',len(baronen23_names))
