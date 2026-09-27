"""Pass 46: the district volumes 92379258 and 92379298 on the south side of Ölandsgatan, west of
pass 45:
- the salmon two-storey house (number 20): segmental-arched ground-floor windows in white surrounds
  with keystones, the panelled black double door with a transom and the shop door and window under
  arches, four (six) upper casements in white eared surrounds, a roundel, a dark plinth and a white
  cornice;
- the tall roughcast courtyard wall with its arched carriage gate (boarded doors), a barred arched
  window and a plinth;
- the small grey roughcast house with a white corner strip and two axes of red casements in white
  surrounds;
- the cream house: a rusticated yellow ground floor with two arched windows, an arched gateway with
  boarded doors in a stone surround, shop windows, a stone quoin strip; a white band; a cream upper
  storey of casements in surrounds with small roundels between them; a white cornice.
The Södra Vallgatan sides and the courtyard ranges stay plain (district heights).

References: Google Street View April 2025 (four panoramas chained along the street), view only.
Zones: source/block46.json; see references/block46-notes.md. Signs and house numbers are omitted.
"""
B46D=json.loads((R/'source/block46.json').read_text());Z=B46D['zones']
block46_names=[];B46={}
for old in [k for k in list(materials) if k.startswith('M_Block46_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Salmon','TownIvory',(.86,.64,.52),.88,0),
 ('Rough','TownIvory',(.60,.55,.49),.95,0),
 ('GreyRough','TownIvory',(.70,.67,.62),.95,0),
 ('Cream','TownIvory',(.92,.90,.84),.88,0),
 ('Yellow','TownIvory',(.90,.83,.62),.88,0),
 ('White','TownIvory',(.95,.95,.92),.82,0),
 ('Stone','TownStone',(.76,.74,.68),.86,0),
 ('Plinth','TownStone',(.36,.34,.33),.84,0),
 ('BlackFrame','TownPaintBrown',(.10,.10,.10),.55,0),
 ('RedFrame','TownPaintBrown',(.50,.18,.13),.55,0),
 ('BrownFrame','TownPaintBrown',(.42,.28,.18),.55,0),
 ('Door','TownPaintBrown',(.08,.08,.08),.55,0),
 ('Oak','TownPaintBrown',(.42,.36,.24),.60,0),
 ('Tile','TownTileRed',(.58,.30,.22),.80,0),
 ('Roof','TownMetalGrey',(.40,.41,.42),.55,.30),
 ('Iron','TownMetalGrey',(.05,.05,.055),.45,.40),
 ('Dark','TownMetalGrey',(.05,.055,.06),.40,.20),
 ]:
 name='M_Block46_'+key;B46[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block46_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B46;WH=M['White']

def b46_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block46_names.append(name);return Mesh(name,category)
def b46_finish(m,osm):
 obj=s21_finish(m);obj['detail_pass']=46;obj['reference_notes']='references/block46-notes.md';obj['osm_way']=osm;return obj
def xf46(X):return -151.463+(X+90.599)*(-151.63+151.463)/(-142.798+90.599)
def street46(w):
 ox,oy=outward(w);return w['kind']=='outer' and oy>.9 and max(w['p'][1],w['q'][1])>-152.2
def cas46(m,x,y,u,b,w,h,a,frame,trans=.72,o=.18,bars=1):
 facade_box(m,x,y,u,o-.04,b+h/2,w,.02,h,GLAZE,a)
 for q in (-w/2+.04,w/2-.04):facade_box(m,x,y,u+q,o,b+h/2,.08,.08,h,frame,a)
 for zz in (b+.04,b+h-.04,b+h*trans):facade_box(m,x,y,u,o,zz,w,.08,.07,frame,a)
 facade_box(m,x,y,u,o+.01,b+h/2,.07,.08,h,frame,a)
 for k in range(1,bars+1):facade_box(m,x,y,u,o+.01,b+h*trans*k/(bars+1),w,.04,.03,frame,a)
 facade_box(m,x,y,u,.40,b-.03,w+.10,.20,.04,M['Dark'],a)
def seg46(m,x,y,u,b,w,h,r,a,frame,wall,trim,kw=.14):
 # Segmental-arched opening: rectangular hole to the crown, closed spandrels, glass on the head,
 # a white arched surround with a keystone.
 spandrels(m,x,y,u,b,w,h,r,a,wall)
 cas46(m,x,y,u,b,w,h,a,frame,.99)
 R_=(w*w/4+r*r)/(2*r);t0=math.asin(w/2/R_);zc=b+h+r-R_;k=10
 arc=[(u+R_*math.sin(t0*(2*i/k-1)),zc+R_*math.cos(t0*(2*i/k-1))) for i in range(k+1)]
 m.faces([lp(x,y,uu,.14,zz,a) for uu,zz in [(u+w/2,b+h)]+arc[::-1]+[(u-w/2,b+h)]],[tuple(range(k+3))],GLAZE)
 town_path(m,[lp(x,y,uu,.18,zz-.04,a) for uu,zz in arc],.04,frame)
 R2=R_+kw;t2=math.asin((w/2+kw)/R2)
 town_path(m,[lp(x,y,u+R2*math.sin(t2*(2*i/k-1)),.39,zc+R2*math.cos(t2*(2*i/k-1))-.03,a) for i in range(k+1)],.07,trim)
 for s in (-1,1):facade_box(m,x,y,u+s*(w/2+kw/2),.39,b+h/2,kw,.07,h,trim,a)
 facade_box(m,x,y,u,.40,b+h+r+.05,.22,.10,.26,trim,a)
 facade_box(m,x,y,u,.40,b-.06,w+2*kw+.08,.10,.10,trim,a)
def eared46(m,x,y,u,b,w,h,a,trim,bw=.13):
 # A flat surround with "ears" at the top corners (the salmon house's upper windows).
 surround36(m,x,y,u,b,w,h,a,trim,bw,.39)
 for s in (-1,1):facade_box(m,x,y,u+s*(w/2+bw+.06),.39,b+h+bw/2-.05,.12,.07,.22,trim,a)
 facade_box(m,x,y,u,.42,b-bw-.03,w+2*bw+.12,.14,.06,trim,a)
def cornice46(m,x,y,L,a,H,ma,out=.42):
 facade_box(m,x,y,0,.40,H-.35,L,.10,.26,ma,a);facade_box(m,x,y,0,.36+out/2,H-.10,L+.10,out,.20,ma,a)

meshes={'SM_Kvarnholmen_House_92379258':b46_new('SM_Kvarnholmen_House_92379258','Kvarnholmen/Ölandsgatan south'),
 'SM_Kvarnholmen_House_92379298':b46_new('SM_Kvarnholmen_House_92379298','Kvarnholmen/Ölandsgatan south')}
for zone in Z:
 m=meshes[Z[zone]['mesh']];HZ=Z[zone]['height']
 wall={'sal':M['Salmon'],'sal2':M['Salmon'],'gr':M['GreyRough'],'cr':M['Cream']}.get(zone,M['Cream'])
 for w in walls(zone):
  x,y,L,a=sf_edge(w['p'],w['q']);S=lambda X:U(w,X,xf46(X))
  if zone=='sal' and street46(w) or zone=='sal2' and street46(w):
   if zone=='sal':
    gw=[(X0,X1) for X0,X1 in ((-91.6,-92.84),(-93.9,-95.14),(-96.58,-97.82),(-98.76,-100.14))]
    uw=[(-91.9,-93.2),(-94.3,-95.6),(-96.84,-98.19),(-99.02,-100.43),(-102.05,-103.36)]
    gf=[(S((a0+b0)/2),1.09,abs(b0-a0)-.28,1.55,0) for a0,b0 in gw]
    up=[(S((a0+b0)/2),3.95,abs(b0-a0)-.26,1.26,0) for a0,b0 in uw]
    door=(S(-102.6),.34,1.85,2.24,0)
    bz_wall(m,w['p'],w['q'],0,HZ,gf+up+[(door[0],.34,1.85,2.51,0)],wall)
    for u,b,ww,hh,r in gf:seg46(m,x,y,u,b,ww,hh-.27,.27,a,M['BlackFrame'],wall,WH)
    for u,b,ww,hh,r in up:eared46(m,x,y,u,b,ww,hh,a,WH);cas46(m,x,y,u,b,ww,hh,a,M['BlackFrame'],.66)
    du=door[0];spandrels(m,x,y,du,.34,1.85,2.24,.27,a,wall)
    facade_box(m,x,y,du,.20,.34+1.25,1.85,.06,2.5,M['Door'],a)
    for s in (-1,1):
     for zz in (.8,1.4):facade_box(m,x,y,du+s*.45,.24,zz,.5,.03,.35,WH,a)
     facade_box(m,x,y,du+s*.45,.18,2.1,.55,.02,.9,GLAZE,a)
    for s in (-1,1):facade_box(m,x,y,du+s*(.925+.10),.39,1.47,.20,.07,2.26,WH,a)
    p18_arch(m,*lp(x,y,du,0,0,a)[:2],2.58,1.85,.27,.20,.40,a,WH,16)
    k_=16;town_path(m,[lp(x,y,du+.14*math.cos(math.tau*t/k_),.42,3.17+.14*math.sin(math.tau*t/k_),a) for t in range(k_+1)],.03,WH)
    plinth36(m,x,y,L,a,[(du-1.0,du+1.0)],.73,M['Plinth'])
    for j in range(2):facade_box(m,x,y,du,.355+(2-j)*.15,.085*(j+1),1.9,(2-j)*.30,.17*(j+1),M['Plinth'],a)
   else:
    # sal2: the shop door and window under one arch.
    su=S(-105.1);bz_wall(m,w['p'],w['q'],0,HZ,[(su,.60,2.1,1.98,0),(S(-105.2),3.95,1.1,1.26,0)],wall)
    spandrels(m,x,y,su,.60,2.1,1.98,.30,a,wall);p18_arch(m,*lp(x,y,su,0,0,a)[:2],2.58,2.1,.30,.20,.40,a,WH,16)
    for s in (-1,1):facade_box(m,x,y,su+s*1.15,.39,1.58,.20,.07,2.0,WH,a)
    s21_glass(m,x,y,su-.55,.60,.9,1.95,a,M['Door'],1,.80,True);cas46(m,x,y,su+.45,.75,1.0,1.8,a,WH,.99)
    eared46(m,x,y,S(-105.2),3.95,1.1,1.26,a,WH);cas46(m,x,y,S(-105.2),3.95,1.1,1.26,a,M['BlackFrame'],.66)
    plinth36(m,x,y,L,a,[(su-1.15,su+1.15)],.73,M['Plinth'])
   cornice46(m,x,y,L,a,HZ,WH)
   town_rod(m,lp(x,y,S(-106.35) if zone=='sal2' else -L/2+.2,.48,.25,a),lp(x,y,S(-106.35) if zone=='sal2' else -L/2+.2,.48,HZ,a),.05,M['Stone'],8)
  elif zone=='gr' and street46(w):
   ops=[(S((a0+b0)/2),b,abs(b0-a0)-.24,t-b,0) for a0,b0 in ((-125.08,-126.37),(-127.06,-128.33)) for b,t in ((1.34,2.70),(3.70,5.07))]
   bz_wall(m,w['p'],w['q'],0,HZ,ops,wall)
   for u,b,ww,hh,r in ops:surround36(m,x,y,u,b,ww,hh,a,WH,.12,.39);cas46(m,x,y,u,b,ww,hh,a,M['RedFrame'],.70)
   facade_box(m,x,y,S(-124.25),.40,(0.8+HZ)/2,.42,.08,HZ-.8,WH,a)
   plinth36(m,x,y,L,a,[],.8,M['Plinth'])
   cornice46(m,x,y,L,a,HZ,WH,.30)
   town_rod(m,lp(x,y,S(-129.0),.48,.25,a),lp(x,y,S(-129.0),.48,HZ,a),.05,M['Dark'],8)
  elif zone=='cr' and street46(w):
   AXU=[(-130.04,-131.0),(-132.22,-133.16),(-134.12,-135.09),(-136.05,-137.02),(-138.23,-139.2),(-140.4,-141.35)]
   up=[(S((a0+b0)/2),3.79,abs(b0-a0),1.80,0) for a0,b0 in AXU]
   gw=[(S(-130.52),1.22,.98,1.18,0),(S(-132.6),1.22,.98,1.18,0)]
   gate=(S(-134.70),.31,1.63,2.0,.28)
   shops=[(S(-138.1),.70,2.0,1.77,0),(S(-141.3),.70,1.7,1.77,0)]
   bz_wall(m,w['p'],w['q'],0,HZ,up+[(u,b,ww,hh+.28,0) for u,b,ww,hh,r in gw]+[(gate[0],.31,1.63,2.28,0)]+shops,wall)
   bz_wall(m,w['p'],w['q'],.55,2.9,[(u,b,ww,hh+.28,0) for u,b,ww,hh,r in gw]+[(gate[0],.31,1.63,2.28,0)]+shops,M['Yellow'],.355,.385)
   grooves=[.9+.3*i for i in range(7)]
   for zz in grooves:
    at=-L/2
    for l_,r_ in sorted((u-ww/2-.08,u+ww/2+.08) for u,b,ww,hh,rr in gw+shops+[(gate[0],.31,1.63,2.28,0)] if b-.05<zz<b+hh+.4)+[(L/2,L/2)]:
     l_=max(-L/2,min(L/2,l_))
     if l_>at+.05:facade_box(m,x,y,(at+l_)/2,.39,zz,l_-at,.02,.03,M['Stone'],a)
     at=max(at,r_)
   for u,b,ww,hh,r in gw:seg46(m,x,y,u,b,ww,hh,.28,a,M['BrownFrame'],M['Yellow'],M['Yellow'],.10)
   gu=gate[0];spandrels(m,x,y,gu,.31,1.63,2.0,.28,a,M['Yellow'])
   facade_box(m,x,y,gu,.22,.31+1.14,1.63,.06,2.28,M['Oak'],a);facade_box(m,x,y,gu,.26,1.45,.04,.04,2.2,M['Dark'],a)
   for s in (-1,1):
    for j in range(6):facade_box(m,x,y,gu+s*(.82+.13),.40,.45+j*.36,.26 if j%2 else .36,.10,.30,M['Stone'],a)
   p18_arch(m,*lp(x,y,gu,0,0,a)[:2],2.31,1.63,.28,.24,.41,a,M['Stone'],16)
   for u,b,ww,hh,r in shops:surround36(m,x,y,u,b,ww,hh,a,M['Stone'],.10,.39);cas46(m,x,y,u,b,ww,hh,a,WH,.99,.18,0)
   facade_box(m,x,y,0,.42,3.05,L,.12,.30,WH,a);facade_box(m,x,y,0,.40,3.42,L,.10,.44,WH,a)
   for u,b,ww,hh,r in up:surround36(m,x,y,u,b,ww,hh,a,WH,.14,.39);cas46(m,x,y,u,b,ww,hh,a,M['BrownFrame'],.70)
   for j in range(len(AXU)-1):
    uu=S((AXU[j][1]+AXU[j+1][0])/2);k_=12
    town_path(m,[lp(x,y,uu+.08*math.cos(math.tau*t/k_),.40,6.2+.08*math.sin(math.tau*t/k_),a) for t in range(k_+1)],.03,M['Dark'])
   k=0;z=.55
   while z+.1<2.9:
    top=min(z+.34,2.9);ln=.55 if k%2==0 else .38
    facade_box(m,x,y,S(-129.84)-ln/2 if S(-129.84)>0 else S(-129.84)+ln/2,.40,(z+top)/2,ln,.08,top-z,M['Stone'],a);z+=.40;k+=1
   plinth36(m,x,y,L,a,[(gu-.9,gu+.9)],.55,M['Stone'])
   cornice46(m,x,y,L,a,HZ,WH,.45)
  else:
   if w['kind']=='outer':plain(m,w,HZ,wall,M['BrownFrame'],WH,2,.9)
   else:bz_wall(m,w['p'],w['q'],w['z0'],HZ,[],wall)
m58,m98=meshes['SM_Kvarnholmen_House_92379258'],meshes['SM_Kvarnholmen_House_92379298']
roof34(m58,'sal',M['Tile'],M['Salmon']);roof34(m58,'gr',M['Roof'],M['GreyRough']);roof34(m98,'cr',M['Tile'],M['Cream'])
for zone,mm,ma in (('sal2',m58,M['Tile']),('bk58',m58,M['Tile']),('bk98',m98,M['Tile'])):
 for g in Z[zone]['polygons']:
  pts=simplify([tuple(v) for v in g],.6)
  if len(pts)<3:continue
  inset_roof(mm,pts,Z[zone]['height'],min(2.0,.45*min(math.dist(p,q) for p,q in zip(pts,pts[1:]+pts[:1]))),.3 if zone=='sal2' else 2.0,ma,.30)
# The courtyard wall on the street line between the salmon house and the grey house.
W0,W1=(-106.73,-151.30),(-124.05,-151.384);wx,wy,wL,wa=sf_edge(W0,W1)
arch=(U({'p':list(W0),'q':list(W1)},-109.85,-151.33),.0,1.55,2.10,.55);grille=(U({'p':list(W0),'q':list(W1)},-114.64,-151.35),.19,1.30,1.60,.44)
bz_wall(m58,W0,W1,0,6.0,[(arch[0],0,1.55,2.65,0),(grille[0],.19,1.30,2.04,0)],M['Rough'],-.25,.355)
for u,b,ww,hh,r in (arch,grille):spandrels(m58,wx,wy,u,b,ww,hh,r,wa,M['Rough'])
facade_box(m58,wx,wy,arch[0],-.15,1.3,1.55,.06,2.6,M['Dark'],wa)
for j in range(12):facade_box(m58,wx,wy,grille[0]-.6+j*1.2/11,.25,1.2,.03,.03,2.0,M['Iron'],wa)
facade_box(m58,wx,wy,0,.39,.37,wL,.08,.75,M['Plinth'],wa)
facade_box(m58,wx,wy,0,.05,6.05,wL,.62,.12,M['Roof'],wa)
for cx,cy in ((-97.0,-156.0),(-139.0,-155.0)):box(m58 if cx>-130 else m98,cx,cy,.55,.80,1.2,(Z['sal']['top'] if cx>-130 else Z['cr']['top'])-.5,M['Dark'],0,M['Dark'])
b46_finish(m58,'92379258');b46_finish(m98,'92379298')

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
_C={'A':(-103.66,4.42),'B':(-112.63,4.53),'C':(-121.93,4.83),'D':(-130.56,5.06)}
def _cam(n):X,D_=_C[n];return X,xf46(X)+.355+D_,2.09
block46_cameras=[
 sv_camera('280_Block46_Cal_Salmon',*_cam('A'),152,5,90),
 sv_camera('281_Block46_Cal_Wall',*_cam('B'),152,5,90),
 sv_camera('282_Block46_Cal_Grey',*_cam('C'),152,5,90),
 sv_camera('283_Block46_Cal_Cream',*_cam('D'),152,5,90),
 ('284_Block46_Aerial',(-115.0,-128.0,30.0),(-115.0,-160.0,4.0),28),
]
print('BLOCK46_GEOMETRY',len(block46_names))
