"""Pass 26: five buildings on Larmgatan by the station. The Larmgatan 1 bank block (OSM 91222222)
with its terracotta render, granite plinth, stucco festoons, pedimented west front, curved entrance
gable on Södra Långgatan, chamfered corner, copper mansard and clock lantern; the later office and
the lower south wing of the same block; Larmgatan 10 (cream, red mansard, corner oriel), Larmgatan
8 (orange, grey-green stone trim, corbelled oriel, twin arched windows), Larmgatan 6 (red brick,
pub frontage, set-back attic) and the Odd Fellows house at Larmgatan 2 (cream Jugendstil, round
corner turrets, lettered frieze). References: Google Street View April 2025, heights measured by
inverting the panorama camera. Zones: source/larm26.json; see references/larm26-notes.md.
Tenant signs are omitted; only the building name ODD FELLOWS is lettered.
"""
import ast
L26D=json.loads((R/'source/larm26.json').read_text());Z=L26D['zones']
tree=ast.parse((R/'scripts/build_baronen23.py').read_text())
tree.body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in {'lin','ring_offset','walls','outward','bz_wall','inset_roof','roof_dormer','box','street_view_camera'}]
exec(compile(tree,'baronen23_helpers','exec'))
tree=ast.parse((R/'scripts/build_station24.py').read_text())
tree.body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in {'arch_door','text_on','poly_lathe','clock'}]
exec(compile(tree,'station24_helpers','exec'))
larm26_names=[];L26={}
MEAN={'TownIvory':(.841,.824,.765),'TownStone':(.648,.628,.59),'TownPaintBrown':(.471,.355,.281),'TownPanel':(.776,.782,.726),
 'TownMetalGrey':(.371,.421,.397),'TownPaintWhite':(.841,.841,.801),'ChurchCopperFine':(.318,.489,.432),'TownMetalRed':(.564,.299,.233),
 'TownPaintGreen':(.311,.401,.347),'Baronen23Brick':(.58,.397,.317),'TownTileRed':(.602,.352,.236),'Station24Slate':(.226,.228,.239)}
for old in [k for k in list(materials) if k.startswith('M_Larm26_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('BankRender','TownIvory',(.71,.45,.30),.86,0),
 ('BankTrim','TownIvory',(.77,.53,.36),.82,0),
 ('Stucco','TownIvory',(.80,.78,.72),.80,0),
 ('Granite','TownStone',(.55,.53,.50),.80,0),
 ('Copper','ChurchCopperFine',(.45,.60,.52),.58,.30),
 ('BankFrame','TownPaintBrown',(.47,.22,.15),.55,0),
 ('Door','TownPaintBrown',(.30,.18,.11),.55,0),
 ('OfficeRender','TownIvory',(.76,.60,.40),.86,0),
 ('WingRender','TownIvory',(.80,.67,.45),.86,0),
 ('CreamRender','TownIvory',(.87,.84,.75),.86,0),
 ('CreamTrim','TownIvory',(.92,.90,.84),.82,0),
 ('RedMetal','TownMetalRed',(.56,.22,.17),.50,.35),
 ('OrangeRender','TownIvory',(.84,.56,.34),.86,0),
 ('GreyTrim','TownStone',(.61,.63,.56),.82,0),
 ('DarkStone','TownStone',(.30,.30,.29),.78,0),
 ('Brick','Baronen23Brick',(.58,.30,.22),.86,0),
 ('BrickTrim','TownStone',(.70,.68,.63),.84,0),
 ('RoofTile','TownTileRed',(.52,.26,.18),.80,0),
 ('Slate','Station24Slate',(.20,.21,.22),.62,.05),
 ('OddRender','TownIvory',(.90,.88,.80),.86,0),
 ('OddGreen','TownPaintGreen',(.08,.22,.15),.50,0),
 ('Gold','TownPaintWhite',(.75,.58,.24),.35,.60),
 ('Roundel','TownPaintWhite',(.62,.12,.10),.45,0),
 ('Awning','TownPanel',(.06,.06,.06),.90,0),
 ('Dial','TownPaintWhite',(.93,.93,.91),.35,0),
 ('Dark','TownMetalGrey',(.05,.055,.06),.40,.20),
 ]:
 name='M_Larm26_'+key;L26[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['larm26_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
COPPER=L26['Copper'];SIGN=L26['Dark'];ST={'Door':L26['Door'],'Clock':L26['Dial']};TRIM=L26['BankTrim']

def l26_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 larm26_names.append(name);return Mesh(name,category)
def l26_finish(m,osm):
 obj=s21_finish(m);obj['detail_pass']=26;obj['reference_notes']='references/larm26-notes.md';obj['osm_way']=osm;return obj
def poly(zone):return [tuple(p) for p in Z[zone]['polygons'][0]]
def simplify(pts,minlen=1.2):
 # Drop vertices that bound very short edges, for roof offsets over the zone outline.
 out=list(pts);changed=True
 while changed and len(out)>4:
  changed=False
  for i in range(len(out)):
   if math.dist(out[i],out[(i+1)%len(out)])<minlen:out.pop((i+1)%len(out));changed=True;break
 return out
def side_of(w,rules):
 # rules: list of (name, outward test, midpoint test); first match wins, else 'court'.
 ox,oy=outward(w);mx,my=(w['p'][0]+w['q'][0])/2,(w['p'][1]+w['q'][1])/2
 for name,test in rules:
  if test(ox,oy,mx,my):return name
 return 'court'
def window(m,x,y,u,b,w,h,a,frame,trim,kind='plain',ma=None):
 # Casement with a stepped architrave; heads: plain, cornice (hood mould) or eared surround.
 s20_window(m,x,y,u,b,w,h,a,frame,trim,.72)
 if kind=='cornice':
  facade_box(m,x,y,u,.42,b+h+.24,w+.30,.12,.20,trim,a);facade_box(m,x,y,u,.47,b+h+.40,w+.50,.24,.09,trim,a)
  for s in (-1,1):facade_box(m,x,y,u+s*(w/2+.15),.44,b+h+.20,.10,.16,.32,trim,a)
 elif kind=='eared':
  for s in (-1,1):
   facade_box(m,x,y,u+s*(w/2+.13),.42,b+h/2,.14,.12,h+.30,trim,a)
   facade_box(m,x,y,u+s*(w/2+.20),.43,b+h+.02,.26,.13,.22,trim,a)
  facade_box(m,x,y,u,.42,b+h+.16,w+.40,.12,.16,trim,a)
 facade_box(m,x,y,u,.40,b-.28,w+.14,.08,.24,trim,a)
def festoon(m,x,y,u,z,w,a,ma):
 # Stucco garland: a sagging swag between two bows, a centre drop and hanging ribbons.
 town_path(m,[lp(x,y,u+w/2*(2*k/8-1),.42,z-.20*math.sin(math.pi*k/8),a) for k in range(9)],.065,ma)
 for s in (-1,1):
  facade_box(m,x,y,u+s*w/2,.42,z+.02,.16,.10,.14,ma,a)
  town_rod(m,lp(x,y,u+s*w/2,.42,z-.04,a),lp(x,y,u+s*(w/2+.06),.42,z-.40,a),.03,ma,6)
 facade_box(m,x,y,u,.43,z-.26,.14,.10,.16,ma,a)
def plain(m,w,H,ma,frame,trim,levels,floor0=1.0,plinth=True):
 # Courtyard and party-wall fronts: simple casements, as on the photographed rear elevations.
 x,y,L,a=sf_edge(w['p'],w['q']);z0=w['z0']
 if L<1.0 or H-z0<1.0:
  bz_wall(m,w['p'],w['q'],z0,H,[],ma);return
 n=max(1,round(L/3.2));holes=[]
 for k in range(n):
  u=-L/2+(k+.5)*L/n
  for j in range(levels):
   b=floor0+j*(H-floor0)/levels
   if b>z0+.3 and b+1.6<H-.3:holes.append((u,b,min(1.15,L/n*.55),1.60,0))
 bz_wall(m,w['p'],w['q'],z0,H,holes,ma)
 for u,b,ww,hh,r in holes:s20_window(m,x,y,u,b,ww,hh,a,frame,trim)
 if plinth and z0<.1:s20_plinth(m,x,y,L,a,holes,.45)
def pediment(m,x,y,u,z,w,rise,a,ma,trim):
 # Triangular gable: solid tympanum, raking and base cornices, oval light.
 tri=[(u-w/2,z),(u+w/2,z),(u,z+rise)]
 vs=[lp(x,y,uu,o,zz,a) for o in (.02,.40) for uu,zz in tri]
 m.faces(vs,[(2,1,0),(3,4,5),(0,1,4,3),(1,2,5,4),(2,0,3,5)],ma)
 for (u0,z0),(u1,z1) in ((tri[0],tri[2]),(tri[2],tri[1])):town_rod(m,lp(x,y,u0,.50,z0+.05,a),lp(x,y,u1,.50,z1+.05,a),.11,trim,8)
 k=24;cz=z+rise*.40
 m.faces([lp(x,y,u+.42*math.cos(t*math.tau/k),.41,cz+.30*math.sin(t*math.tau/k),a) for t in range(k)],[tuple(range(k))],GLAZE)
 town_path(m,[lp(x,y,u+.50*math.cos(t*math.tau/k),.45,cz+.38*math.sin(t*math.tau/k),a) for t in range(k+1)],.06,trim)
def curved_gable(m,x,y,u,z,w,h,rise,a,ma,trim,stucco):
 # Tall entrance gable with a segmental crown, cartouche and oval light (Södra Långgatan).
 k=16;crown=[(u-w/2+w*i/k,z+h+rise*math.sin(math.pi*i/k)) for i in range(k+1)]
 outline=[(u-w/2,z),(u+w/2,z)]+crown[::-1]
 n=len(outline);vs=[lp(x,y,uu,o,zz,a) for o in (.02,.40) for uu,zz in outline]
 m.faces(vs,[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],ma)
 town_path(m,[lp(x,y,uu,.50,zz+.06,a) for uu,zz in crown],.10,trim)
 for s in (-1,1):facade_box(m,x,y,u+s*(w/2-.20),.45,z+h/2,.40,.10,h,trim,a)
 kk=24;cz=z+h*.55
 m.faces([lp(x,y,u+.48*math.cos(t*math.tau/kk),.41,cz+.36*math.sin(t*math.tau/kk),a) for t in range(kk)],[tuple(range(kk))],GLAZE)
 town_path(m,[lp(x,y,u+.57*math.cos(t*math.tau/kk),.46,cz+.45*math.sin(t*math.tau/kk),a) for t in range(kk+1)],.07,stucco)
 facade_box(m,x,y,u,.45,z+h+rise*.55,1.0,.12,.55,stucco,a)
 for s in (-1,1):town_rod(m,lp(x,y,u+s*.5,.46,z+h+rise*.55,a),lp(x,y,u+s*1.1,.46,z+h+rise*.15,a),.06,stucco,6)
def balcony(m,x,y,u,z,w,a,rail=None):
 # Stone slab on two consoles with a wrought-iron railing.
 rail=rail or IRON;facade_box(m,x,y,u,.36+.35,z,w,.70,.14,TS,a)
 for s in (-1,1):facade_box(m,x,y,u+s*(w/2-.20),.36+.25,z-.28,.16,.50,.42,TS,a)
 lm_rail(m,x,y,w,z+.07,a,1.0,rail)

# ---------------------------------------------------------------- Larmgatan 1: the bank
BR,BT,STU,GR,FR=L26['BankRender'],L26['BankTrim'],L26['Stucco'],L26['Granite'],L26['BankFrame']
BH=Z['bank']['height'];PL=1.17;WU=-1.3
BANK_RULES=[('north',lambda ox,oy,mx,my:oy>.9 and my>-81),('east',lambda ox,oy,mx,my:ox>.9 and mx>-299.5),
 ('west',lambda ox,oy,mx,my:ox<-.9 and mx<-336),('chamfer',lambda ox,oy,mx,my:ox>.5 and oy>.5)]
def bank_face(m,w):
 p,q,z0=w['p'],w['q'],w['z0'];x,y,L,a=sf_edge(p,q);sd=side_of(w,BANK_RULES)
 if w['kind']=='upper' or sd=='court':plain(m,w,BH,BR,FR,BT,3,1.2);return
 holes=[];extras=[]
 if sd=='east':
  n=9;st=L/n;us=[-L/2+(k+.5)*st for k in range(n)]
  for u in us:holes+=[(u,2.10,1.35,2.20,0),(u,6.00,1.25,1.75,0)]
 elif sd=='west':
  us=[WU+d for d in (-9.0,-5.1,0.0,5.1,9.0)]
  for u in us:holes+=[(u,2.10,1.35,2.15,0),(u,6.25,1.30,2.05,0)]
 elif sd=='north':
  n=10;st=L/n;us=[-L/2+(k+.5)*st for k in range(n)];door=3
  for i,u in enumerate(us):
   holes.append((u,.30,1.70,2.95,.85) if i==door else (u,1.35,2.00,2.55,1.0))
   holes.append((u,6.25,1.30,1.95,0))
 elif sd=='chamfer':
  us=[0.0];holes+=[(0.0,2.10,1.00,2.15,0),(0.0,6.00,1.00,2.20,0)]
 bz_wall(m,p,q,z0,BH,holes,BR)
 for u,b,ww,hh,r in holes:
  if b<.5:arch_door(m,x,y,u,b,ww,hh,r,a,L26['Door'])
  elif r>0:
   p18_win(m,x,y,u,b,ww,hh,r,a,FR,BT,3,2);facade_box(m,x,y,u,.46,b+hh+r+.10,.30,.14,.36,STU,a)
  elif sd=='west' and abs(u-WU)<.1:continue
  elif b<5:window(m,x,y,u,b,ww,hh,a,FR,BT,'eared')
  else:window(m,x,y,u,b,ww,hh,a,FR,BT,'cornice' if sd!='east' else 'plain')
 # Granite plinth, floor band, festoons (above the upper windows on Larmgatan, below them on the
 # other fronts), frieze and cornice.
 s20_plinth(m,x,y,L,a,holes,PL)
 facade_box(m,x,y,0,.40,PL+.05,L+.10,.12,.10,GR,a)
 p18_band(m,x,y,L+.6,5.25,a,BT,.30)
 for u,b,ww,hh,r in holes:
  if b>5:
   if sd=='east':festoon(m,x,y,u,9.45,ww+.55,a,STU)
   elif not(sd=='west' and abs(u-WU)<.1):festoon(m,x,y,u,b-.55,ww+.35,a,STU)
 if sd=='east':
  for k in range(n+1):
   u=max(-L/2+.35,min(L/2-.35,-L/2+k*L/n))
   facade_box(m,x,y,u,.405,(PL+9.75)/2,.70,.10,9.75-PL,BT,a)
 elif sd=='north':
  for k in (0,2,5,8,10):
   u=max(-L/2+.40,min(L/2-.40,-L/2+k*L/n));facade_box(m,x,y,u,.41,(PL+9.75)/2,.80,.12,9.75-PL,BT,a)
  # Entrance: steps, portal surround and the curved gable above the cornice.
  ud=us[door];facade_box(m,x,y,ud,.95,.12,3.0,1.2,.24,GR,a);facade_box(m,x,y,ud,.75,.30,2.6,.8,.12,GR,a)
  for s in (-1,1):facade_box(m,x,y,ud+s*1.25,.46,2.2,.45,.14,4.4,BT,a)
  facade_box(m,x,y,ud,.47,4.55,3.0,.16,.40,BT,a)
  curved_gable(m,x,y,ud,BH-.10,4.6,2.1,1.0,a,BR,BT,STU)
 elif sd=='west':
  # Pedimented centre risalit, 5.2 m wide and 0.35 m proud, with the balcony door.
  rh=[(0,2.10,1.35,2.15,0),(0,6.25,1.30,2.05,0)]
  bz_wall(m,lp(x,y,WU-2.6,0,0,a)[:2],lp(x,y,WU+2.6,0,0,a)[:2],PL,BH,rh,BR,.36,.71)
  for s in (-1,1):facade_box(m,x,y,WU+s*2.6,.53,(PL+BH)/2,.02,.35,BH-PL,BR,a);facade_box(m,x,y,WU+s*2.6,.77,(PL+9.75)/2,.40,.12,9.75-PL,BT,a)
  window(m,*lp(x,y,WU,.355,0,a)[:2],0,2.10,1.35,2.15,a,FR,BT,'eared');window(m,*lp(x,y,WU,.355,0,a)[:2],0,6.25,1.30,2.05,a,FR,BT,'cornice')
  balcony(m,*lp(x,y,WU,.35,0,a)[:2],0,6.10,2.2,a)
  pediment(m,*lp(x,y,WU,.35,0,a)[:2],0,BH-.05,6.0,1.9,a,BR,BT)
  for s in (-1,1):facade_box(m,x,y,s*(L/2-.45),.41,(PL+9.75)/2,.90,.12,9.75-PL,BT,a)
 elif sd=='chamfer':
  # Rusticated quarter rounds read as horizontal banding; the corner balcony on its console.
  for k in range(int((9.6-PL)/.45)):
   z=PL+.225+k*.45
   for s in (-1,1):facade_box(m,x,y,s*(L/2-.30),.38,z,.62,.06,.30,BT,a)
  balcony(m,x,y,0,5.90,1.6,a);facade_box(m,x,y,0,.44,9.25,.60,.16,.55,STU,a)
 facade_box(m,x,y,0,.40,9.85,L+.25,.08,.26,BT,a)
 lm_cornice(m,x,y,L+.9,BH-.18,a,BT,sd in ('north','west','east'))
def bank_roof(m):
 pts=simplify(poly('bank'));H=Z['bank']['height'];band=Z['bank']['band'];top=Z['bank']['top'];ins=Z['bank']['inset']
 outer,inner=inset_roof(m,pts,H,ins,band-H,COPPER,.45)
 inset_roof(m,inner,band,2.4,top-band,COPPER,.10)
 slope=(band-H)/(ins+.45)
 # Round-headed copper dormers over the upper windows of the three street fronts.
 for w in walls('bank','outer'):
  x,y,L,a=sf_edge(w['p'],w['q']);sd=side_of(w,BANK_RULES)
  if sd=='west':us=[WU+d for d in (-9.0,-5.1,5.1,9.0)]
  elif sd=='north':n=10;us=[-L/2+(k+.5)*L/n for k in range(n) if k not in (3,)][::2]
  elif sd=='east':n=9;us=[-L/2+(k+.5)*L/n for k in range(0,n,2)]
  else:continue
  for u in us:roof_dormer(m,x,y,u,a,H,slope,.55,.90,1.05,COPPER,COPPER,TW,True)
 # Clock lantern near the north-west corner: octagonal copper drum with four dials, an onion
 # dome, a ball and the spire (base 16.6, dome 18.8, spire 21.4 m in the plaza panorama).
 wx=min(p[0] for p in pts);ny=max(p[1] for p in pts);cx,cy=wx+7.0,ny-6.0;zb=top;r=1.05;rot=math.pi/8
 poly_lathe(m,cx,cy,zb-.20,[(r+.25,0),(r+.25,.35),(r,.35),(r,1.55),(r+.15,1.55),(r+.18,1.70)],COPPER,8,rot)
 for k in range(4):
  t=k*math.pi/2;ang=t+math.pi/2;rr=r*math.cos(math.pi/8);px,py=cx+rr*math.cos(t),cy+rr*math.sin(t)
  clock(m,px,py,0,zb+.85,ang,.36,.04)
 poly_lathe(m,cx,cy,zb+1.50,[(r+.10,0),(r*.95,.30),(r*.62,.95),(r*.30,1.35),(r*.22,1.55)],COPPER,16,0,True)
 m.lathe(cx,cy,zb+3.02,[(.20,0),(.30,.18),(.30,.32),(.12,.48),(.07,.52),(.05,2.0),(.02,2.08)],COPPER,12)
 facade_box(m,cx,cy,.28,0,zb+4.30,.50,.02,.26,COPPER,0)

m=l26_new('SM_Kvarnholmen_House_91222222','Kvarnholmen/Larmgatan')
for w in walls('bank'):bank_face(m,w)
bank_roof(m)
# Later office at the south end of Larmgatan: yellow-brown render, three floors, flat roof.
OR=L26['OfficeRender'];OH=Z['office']['height']
for w in walls('office'):
 x,y,L,a=sf_edge(w['p'],w['q'])
 if w['kind']=='upper' or L<3:plain(m,w,OH,OR,TW,OR,3,1.0);continue
 n=max(1,round(L/2.5));st=L/n;holes=[(-L/2+(k+.5)*st,b,1.40,1.55,0) for k in range(n) for b in (1.10,4.50,7.80)]
 ox,oy=outward(w);east=ox>.9
 if east:holes=[h for h in holes if not(h[1]<2 and abs(h[0]-(-L/2+1.5*st))<.1)]+[(-L/2+1.5*st,.05,1.8,2.6,0)]
 bz_wall(m,w['p'],w['q'],0,OH,holes,OR)
 for u,b,ww,hh,r in holes:
  if b<.5:s21_glass(m,x,y,u,b,ww,hh,a,L26['Dark'],2,.78,True)
  else:s20_window(m,x,y,u,b,ww,hh,a,TW,OR)
 s20_plinth(m,x,y,L,a,holes,.45)
 if east:
  u=-L/2+1.5*st;facade_box(m,x,y,u,1.1,2.95,3.0,1.6,.18,L26['Dark'],a)
  for s in (-1,1):town_rod(m,lp(x,y,u+s*1.3,1.85,2.95,a),lp(x,y,u+s*1.3,.40,3.9,a),.02,METAL,6)
 facade_box(m,x,y,0,.40,OH+.12,L+.10,.12,.24,L26['Granite'],a)
s21_flat_roof(m,simplify(poly('office'),.8),OH,METAL)
# Lower south wing on the station square: ochre render, copper hip.
WR=L26['WingRender'];WH=Z['southwing']['height']
for w in walls('southwing'):
 x,y,L,a=sf_edge(w['p'],w['q']);n=max(1,round(L/2.7));holes=[(-L/2+(k+.5)*L/n,b,1.15,1.60,0) for k in range(n) for b in (1.10,4.40)]
 bz_wall(m,w['p'],w['q'],w['z0'],WH,holes,WR)
 for u,b,ww,hh,r in holes:window(m,x,y,u,b,ww,hh,a,TW,L26['CreamTrim'],'plain')
 s20_plinth(m,x,y,L,a,holes,.50);lm_cornice(m,x,y,L+.9,WH-.18,a,L26['CreamTrim'])
sw=simplify(poly('southwing'));d=min(math.dist(sw[i],sw[(i+1)%len(sw)]) for i in range(len(sw)))
inset_roof(m,sw,WH,d/2-.30,Z['southwing']['top']-WH,COPPER,.45)
cx=sum(p[0] for p in sw)/len(sw);cy=sum(p[1] for p in sw)/len(sw);box(m,cx+3.0,cy,.7,.7,2.0,Z['southwing']['top']-1.2,WR,0,COPPER)
l26_finish(m,'91222222')

# ---------------------------------------------------------------- Larmgatan 10
CR,CT,RM=L26['CreamRender'],L26['CreamTrim'],L26['RedMetal'];H10=Z['l10']['height']
L10_RULES=[('north',lambda ox,oy,mx,my:oy>.9 and my>-80),('west',lambda ox,oy,mx,my:ox<-.9 and mx<-285)]
m=l26_new('SM_Kvarnholmen_House_91856621','Kvarnholmen/Larmgatan')
for w in walls('l10'):
 x,y,L,a=sf_edge(w['p'],w['q']);sd=side_of(w,L10_RULES)
 if w['kind']=='upper' or sd=='court':plain(m,w,H10,CR,TW,CT,3,1.2);continue
 n=max(1,round(L/3.0));st=L/n;us=[-L/2+(k+.5)*st for k in range(n)];holes=[]
 for i,u in enumerate(us):
  holes.append((u,.10,2.0,2.85,0) if i%2==0 else (u,.10,1.10,2.45,0))
  holes+=[(u,4.60,1.25,1.95,0),(u,7.80,1.20,1.85,0)]
 bz_wall(m,w['p'],w['q'],0,H10,holes,CR)
 for u,b,ww,hh,r in holes:
  if b<.5:s21_glass(m,x,y,u,b,ww,hh,a,L26['Dark'] if ww>1.5 else TW,3 if ww>1.5 else 1,.80,ww<1.5)
  else:window(m,x,y,u,b,ww,hh,a,TW,CT,'cornice' if b<6 else 'plain')
 s20_plinth(m,x,y,L,a,holes,.40)
 facade_box(m,x,y,0,.40,3.55,L+.12,.12,.60,CT,a);p18_band(m,x,y,L+.6,4.25,a,CT,.30)
 if sd=='north':
  for u in us[::2]:s21_shallow_awning(m,x,y,u,3.20,2.2,a,L26['Roundel'],1.0)
 lm_cornice(m,x,y,L+.9,H10-.18,a,CT,True)
# Round oriel over the Larmgatan / Södra Långgatan corner, second floor.
p10=poly('l10');corner=max(p10,key=lambda p:p[1]-p[0]*.02)
corner=min((p for p in p10 if p[1]>-80),key=lambda p:p[0])
m.cylinder(corner[0],corner[1],7.2,1.05,2.9,CR,24);m.cylinder(corner[0],corner[1],6.9,.75,.30,CT,24);m.cylinder(corner[0],corner[1],10.1,1.20,.18,CT,24)
for t in range(5):
 th=math.radians(90+45+(t-2)*30);px,py=corner[0]+1.05*math.cos(th),corner[1]+1.05*math.sin(th)
 facade_box(m,px,py,0,.02,8.65,.55,.05,1.45,GLAZE,th-math.pi/2);town_border(m,px,py,8.65,.55,1.45,th-math.pi/2,TW,.05,.04)
p10s=simplify(p10);outer,inner=inset_roof(m,p10s,H10,Z['l10']['inset'],Z['l10']['band']-H10,RM,.45)
inset_roof(m,inner,Z['l10']['band'],2.0,Z['l10']['top']-Z['l10']['band'],RM,.10)
s10=(Z['l10']['band']-H10)/(Z['l10']['inset']+.45)
for w in walls('l10','outer'):
 x,y,L,a=sf_edge(w['p'],w['q'])
 if side_of(w,L10_RULES)=='court':continue
 n=max(1,round(L/3.0))
 for k in range(n):roof_dormer(m,x,y,-L/2+(k+.5)*L/n,a,H10,s10,.55,.85,1.05,CR,town_mats['MetalRed'],TW,False)
l26_finish(m,'91856621')

# ---------------------------------------------------------------- Larmgatan 8
OGR,GT,DS=L26['OrangeRender'],L26['GreyTrim'],L26['DarkStone'];H8=Z['l8']['height']
m=l26_new('SM_Kvarnholmen_House_91856599','Kvarnholmen/Larmgatan')
for w in walls('l8'):
 x,y,L,a=sf_edge(w['p'],w['q']);ox,oy=outward(w)
 if not(w['kind']=='outer' and ox<-.9 and L>8):plain(m,w,H8,OGR,TW,GT,3,1.2);continue
 # Street front: dark stone shop floor, oriel on the centre axis, two axes either side.
 axes=[-4.35,-2.35,2.35,4.35];holes=[(-3.35,.55,2.9,2.55,0),(3.35,.55,2.9,2.55,0),(0,.20,1.55,2.75,0)]
 for u in axes:holes+=[(u,4.80,1.20,1.80,0)]
 bz_wall(m,w['p'],w['q'],4.20,H8,[h for h in holes if h[1]>4],OGR)
 bz_wall(m,w['p'],w['q'],0,4.20,[h for h in holes if h[1]<4],DS)
 for u,b,ww,hh,r in holes:
  if b<4:s21_glass(m,x,y,u,b,ww,hh,a,L26['Door'] if b<.4 else L26['Dark'],2 if b<.4 else 3,.82,b<.4)
  else:window(m,x,y,u,b,ww,hh,a,L26['Door'],GT,'cornice')
 for u in (-3.35,3.35):s21_shallow_awning(m,x,y,u,3.35,3.0,a,L26['CreamTrim'],.9)
 facade_box(m,x,y,0,.42,3.95,L+.10,.16,.50,DS,a)
 p18_band(m,x,y,L+.4,4.45,a,GT,.34);p18_band(m,x,y,L+.4,7.45,a,GT,.34)
 # Second floor: twin round-headed windows under one grey surround.
 for u in axes:
  for s in (-.34,.34):p18_win(m,x,y,u+s,8.30,.56,1.05,.28,a,L26['Door'],GT,2,1)
  facade_box(m,x,y,u,.44,9.85,1.55,.12,.18,GT,a)
 for k in range(round(L/.55)):facade_box(m,x,y,-L/2+(k+.5)*L/round(L/.55),.47,H8-.62,.14,.22,.20,GT,a)
 lm_cornice(m,x,y,L+.6,H8-.18,a,GT,False)
 # Corbelled oriel on the centre axis, first and second floor, with the attic gable above.
 ow=2.10;front=.95;out=[(-ow*.62,.36),(-ow*.50,front),(ow*.50,front),(ow*.62,.36)];pp=[lp(x,y,uu,o,0,a)[:2] for uu,o in out]
 m.prism(pp,4.05,4.35,GT);m.prism(pp,7.35,7.55,GT);m.prism(pp,10.35,10.60,GT)
 for zc,hh in ((3.70,.35),(3.35,.35)):facade_box(m,x,y,0,.62,zc,ow*.8-(3.70-zc)*1.2,.55,hh,GT,a)
 for i in range(3):
  p0,p1=pp[i],pp[i+1];xx,yy,LL,aa=sf_edge(p0,p1)
  for b,hh in ((4.55,2.45),(7.75,2.25)):
   facade_box(m,xx,yy,0,-.02,b+hh/2,LL,.10,hh,OGR if i!=1 else OGR,aa)
   facade_box(m,xx,yy,0,.04,b+hh/2,LL*.62,.04,hh*.82,GLAZE,aa);town_border(m,xx,yy,b+hh/2,LL*.62,hh*.82,aa,GT,.06,.06)
 for s in (-1,1):facade_box(m,x,y,s*(ow/2+.06),front+.06,7.4,.12,.16,6.3,GT,a)
 gw=2.3;outline=[(-gw/2,H8-.1),(gw/2,H8-.1),(gw/2,H8+.9)]+[(gw/2*math.cos(t*math.pi/12),H8+.9+.75*math.sin(t*math.pi/12)) for t in range(1,13)]
 nn=len(outline);vs=[lp(x,y,uu,o,zz,a) for o in (.02,.62) for uu,zz in outline]
 m.faces(vs,[tuple(range(nn-1,-1,-1)),tuple(range(nn,2*nn))]+[(i,(i+1)%nn,(i+1)%nn+nn,i+nn) for i in range(nn)],OGR)
 p18_win(m,*lp(x,y,0,.30,0,a)[:2],0,H8+.25,.95,.85,.45,a,L26['Door'],GT,2,2)
 town_path(m,[lp(x,y,gw/2*math.cos(t*math.pi/12),.70,H8+.95+.75*math.sin(t*math.pi/12),a) for t in range(13)],.07,GT)
 for u in (-3.35,3.35):roof_dormer(m,x,y,u,a,H8,(Z['l8']['top']-H8)/4.0,.45,.80,.95,GT,L26['Slate'],TW,True)
p8=simplify(poly('l8'));inset_roof(m,p8,H8,min(4.2,min(math.dist(p8[i],p8[(i+1)%len(p8)]) for i in range(len(p8)))/2-.2),Z['l8']['top']-H8,L26['Slate'],.40)
l26_finish(m,'91856599')

# ---------------------------------------------------------------- Larmgatan 6
BK,BKT=L26['Brick'],L26['BrickTrim'];H6=Z['l6']['height'];A6=Z['l6']['attic'];I6=Z['l6']['inset']
L6_RULES=[('west',lambda ox,oy,mx,my:ox<-.9 and mx<-285),('south',lambda ox,oy,mx,my:oy<-.9 and my<-137)]
m=l26_new('SM_Kvarnholmen_House_91856613','Kvarnholmen/Larmgatan')
for w in walls('l6'):
 x,y,L,a=sf_edge(w['p'],w['q']);sd=side_of(w,L6_RULES)
 if w['kind']=='upper' or sd=='court':plain(m,w,H6,BK,L26['Dark'],BKT,3,1.1);continue
 n=max(1,round(L/2.6));st=L/n;us=[-L/2+(k+.5)*st for k in range(n)];holes=[]
 for i,u in enumerate(us):
  holes.append((u,.10,st-.55,3.10,0) if (sd=='west' or i%3!=1) else (u,.10,1.2,2.4,0))
  holes+=[(u,4.60,1.45,1.40,0),(u,7.05,1.45,1.60,0)]
 bz_wall(m,w['p'],w['q'],0,H6,holes,BK)
 for u,b,ww,hh,r in holes:
  if b<.5:s21_glass(m,x,y,u,b,ww,hh,a,L26['Dark'],max(1,round(ww/1.0)),.78,ww<1.5)
  else:s20_window(m,x,y,u,b,ww,hh,a,L26['Dark'],BK)
 for u,b,ww,hh,r in holes:
  if b>6 and (us.index(u)%2==0):lm_rail(m,x,y,ww+.2,b,a,.55,IRON)
 facade_box(m,x,y,0,.40,3.75,L+.10,.12,.50,L26['Dark'],a)
 facade_box(m,x,y,0,.40,6.70,L+.10,.14,.46,BKT,a)
 facade_box(m,x,y,0,.40,H6+.10,L+.20,.16,.20,BKT,a);lm_rail(m,x,y,L,H6+.15,a,.30,IRON)
 if sd=='west':
  for u in us:s21_shallow_awning(m,x,y,u,3.40,st-.3,a,L26['Awning'],1.4)
s21_flat_roof(m,simplify(poly('l6'),.8),H6,METAL)
# Set-back attic storey with a shallow tiled roof; terraces behind the street railings.
att=ring_offset(simplify(poly('l6')),-I6)
for p0,p1 in zip(att,att[1:]+att[:1]):
 x,y,L,a=sf_edge(p0,p1);n=max(1,round(L/3.2));holes=[(-L/2+(k+.5)*L/n,H6+.35,1.40,1.85,0) for k in range(n)]
 bz_wall(m,p0,p1,H6,A6,holes,BKT)
 for u,b,ww,hh,r in holes:s21_glass(m,x,y,u,b,ww,hh,a,L26['Dark'],2,.80,True)
inset_roof(m,att,A6,4.0,Z['l6']['top']-A6,L26['RoofTile'],.35)
l26_finish(m,'91856613')

# ---------------------------------------------------------------- Larmgatan 2: Odd Fellows
TRIM=L26['CreamTrim'];ODR,ODG=L26['OddRender'],L26['OddGreen'];HO=Z['oddfellow']['height'];RT=L26D['oddfellow_tower_radius']
of=[tuple(p) for p in next(b for b in json.loads((R/'source/kvarnholmen.json').read_text())['buildings'] if b['id']=='91856604')['polygons'][0]['outer']]
def tower_centre(i):
 a_,b_,c_=of[i-1],of[i],of[(i+1)%len(of)]
 u=((a_[0]-b_[0])/math.dist(a_,b_),(a_[1]-b_[1])/math.dist(a_,b_));v=((c_[0]-b_[0])/math.dist(b_,c_),(c_[1]-b_[1])/math.dist(b_,c_))
 return (b_[0]+(u[0]+v[0])*RT,b_[1]+(u[1]+v[1])*RT),(-(u[0]+v[0])/math.sqrt(2),-(u[1]+v[1])/math.sqrt(2))
towers=[tower_centre(0),tower_centre(1)]
m=l26_new('SM_Kvarnholmen_House_91856604','Kvarnholmen/Larmgatan')
for w in walls('oddfellow'):
 x,y,L,a=sf_edge(w['p'],w['q']);ox,oy=outward(w)
 if L<1.0:bz_wall(m,w['p'],w['q'],w['z0'],HO,[],ODR);continue
 if w['kind']=='upper':plain(m,w,HO,ODR,ODG,L26['CreamTrim'],3,1.2);continue
 street=ox<-.9
 n=max(1,round(L/2.3));st=L/n;us=[-L/2+(k+.5)*st for k in range(n)];holes=[]
 for i,u in enumerate(us):
  if street and i==2:holes.append((u,.25,1.70,2.60,.85))
  elif street:holes.append((u,.55,1.80,2.40,.90))
  else:holes.append((u,1.10,1.25,2.00,0))
  holes+=[(u,4.90,1.40,2.05,0),(u,7.75,1.40,1.85,0)]
 bz_wall(m,w['p'],w['q'],0,HO,holes,ODR)
 for u,b,ww,hh,r in holes:
  if b<.4:arch_door(m,x,y,u,b,ww,hh,r,a,L26['Door'])
  elif r>0:
   p18_win(m,x,y,u,b,ww,hh,r,a,ODG,L26['CreamTrim'],3,3)
   s21_shallow_awning(m,x,y,u,b+hh+r+.05,ww+.3,a,L26['Awning'],.8)
  else:window(m,x,y,u,b,ww,hh,a,ODG,L26['CreamTrim'],'plain')
 s20_plinth(m,x,y,L,a,holes,.60)
 p18_band(m,x,y,L+.4,4.35,a,L26['CreamTrim'],.30);p18_band(m,x,y,L+.4,7.25,a,L26['CreamTrim'],.26)
 if street:balcony(m,x,y,us[1],4.80,2.4,a,ODG)
 # Frieze band with the lettered name between red roundels, then the parapet coping.
 facade_box(m,x,y,0,.40,10.15,L+.10,.08,.95,L26['CreamTrim'],a)
 if street:
  text_on(m,x,y,0,10.12,a,'ODD FELLOWS',min(6.5,L*.45),L26['Gold'],.45)
  for s in (-1,1):
   for k,uu in enumerate((3.9,4.4)):
    kk=16;px,py,_=lp(x,y,s*uu,.46,0,a);m.faces([facade_point(px,py,.13*math.cos(t*math.tau/kk),0,10.12+.13*math.sin(t*math.tau/kk),a) for t in range(kk)],[tuple(range(kk))],L26['Roundel'])
 facade_box(m,x,y,0,.46,HO+.05,L+.30,.30,.14,L26['CreamTrim'],a)
for (cx,cy),(dx,dy) in towers:
 # Round corner turrets: windows on the diagonal, the drum above the parapet, copper cap.
 for b,hh in ((4.90,2.05),(7.75,1.85)):
  px,py=cx+dx*RT,cy+dy*RT;ang=math.atan2(dy,dx)+math.pi/2
  town_window(m,px,py,b+hh/2,1.0,hh,ang,ODG,False,3,2,False);facade_box(m,px,py,0,.14,b-.10,1.2,.30,.10,L26['CreamTrim'],ang)
 m.cylinder(cx,cy,HO-.02,RT-.05,2.30,ODR,32);m.cylinder(cx,cy,HO+2.25,RT+.10,.14,L26['CreamTrim'],32)
 for k in range(6):
  t=k*math.tau/6;px,py=cx+(RT-.05)*math.cos(t),cy+(RT-.05)*math.sin(t);town_window(m,px,py,HO+1.1,.60,.95,t+math.pi/2,ODG,True,2,2,False)
 m.lathe(cx,cy,HO+2.36,[(RT+.12,0),(RT*.95,.22),(RT*.70,.62),(RT*.40,.98),(.25,1.18),(.10,1.26)],COPPER,24)
 m.lathe(cx,cy,HO+3.60,[(.06,0),(.12,.10),(.12,.24),(.03,.34),(.025,.95),(.01,1.0)],COPPER,12)
po=simplify(poly('oddfellow'),1.0);inset_roof(m,po,HO-.35,3.2,Z['oddfellow']['top']-HO+.35,COPPER,-.05)
l26_finish(m,'91856604')

larm26_cameras=[
 street_view_camera('137_Larm_Bank_Plaza',56.6619035,16.3608527,82,5.87),
 street_view_camera('138_Larm_Bank_North',56.6622659,16.3617759,250,10),
 street_view_camera('139_Larm_Street_North',56.6620328,16.3622273,25,12,90),
 street_view_camera('140_Larm_L8',56.6620328,16.3622273,62,15,90),
 street_view_camera('141_Larm_OddFellow',56.6614318,16.3623679,38,5),
 ('142_Larm_Aerial',(-250.0,-190.0,48.0),(-305.0,-115.0,6.0),26),
 street_view_camera('143_Larm_Cal_Plaza',56.6619035,16.3608527,82,5.87,match='height'),
]
print('LARM26_GEOMETRY',len(larm26_names))
