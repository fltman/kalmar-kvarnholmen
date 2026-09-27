"""Pass 41: the district volume 92412838 on the north side of Södra Långgatan, from the garage yard to
Östra Sjögatan (numbers 39-43).

A white-rendered two-storey range in two builds on one grey plinth, under one string course and one
moulded cornice and a copper-green sheet roof:
- the western build (dated 1940 on the wall): two garages with boarded doors under glazed
  transoms, two doors in stone surrounds with recessed panels over them, rectangular windows in
  flat surrounds, one wide window of twelve lights, a lunette gable with a scrolled outline;
- the eastern build (dated 1888), from a quoin strip: segmental-headed ground-floor windows in
  surrounds, a rusticated round-arched portal with voussoirs and a keystone over a glazed double
  door on three steps (number 43), a baroque central gable with a cartouche, scroll volutes and a
  segmental-headed window;
- sixteen upper windows (two leaves, a transom) in flat surrounds with aprons down to the string;
- iron wall anchors on the piers, black downpipes, quoins at both ends.
The Östra Sjögatan end repeats the eastern build's storeys (five axes, estimated positions).

References: Google Street View April 2025 (five panoramas along the street, chained on the
building's two ends and shared window edges; one on Östra Sjögatan), view only. Zones:
source/block41.json; see references/block41-notes.md. The house numbers, the dates, the hanging
sign and the notices are omitted.
"""
B41D=json.loads((R/'source/block41.json').read_text());Z=B41D['zones']
block41_names=[];B41={}
for old in [k for k in list(materials) if k.startswith('M_Block41_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('White','TownIvory',(.92,.91,.88),.90,0),
 ('Trim','TownIvory',(.88,.87,.83),.85,0),
 ('Frame','TownPaintBrown',(.35,.22,.17),.55,0),
 ('Stone','TownStone',(.70,.67,.60),.86,0),
 ('Door','TownPaintBrown',(.55,.34,.18),.60,0),
 ('GarageWood','TownPaintBrown',(.45,.30,.20),.70,0),
 ('BrownDoor','TownPaintBrown',(.38,.22,.18),.60,0),
 ('Plinth','TownStone',(.56,.58,.58),.82,0),
 ('Step','TownStone',(.62,.60,.56),.84,0),
 ('Roof','TownMetalGrey',(.36,.47,.40),.55,.25),
 ('Iron','TownMetalGrey',(.05,.05,.055),.45,.40),
 ('Dark','TownMetalGrey',(.05,.055,.06),.40,.20),
 ]:
 name='M_Block41_'+key;B41[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block41_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B41;W41,T41=M['White'],M['Trim']

def b41_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block41_names.append(name);return Mesh(name,category)
def b41_finish(m,osm):
 obj=s21_finish(m);obj['detail_pass']=41;obj['reference_notes']='references/block41-notes.md';obj['osm_way']=osm;return obj
def kind41(w):
 ox,oy=outward(w)
 if w['kind']!='outer':return None
 if oy<-.9 and min(w['p'][1],w['q'][1])<-69:return 'sodra'
 if ox>.9 and min(w['p'][0],w['q'][0])>46.9:return 'ostra'
 if ox<-.9 and max(w['p'][0],w['q'][0])<-2.8 and min(w['p'][1],w['q'][1])<-63:return 'gable'
 return None
def casement41(m,x,y,u,b,w,h,a,trans=.72,o=.18):
 # Brown casement in a reveal: two leaves, a transom, glazing bars, a metal sill.
 facade_box(m,x,y,u,o-.04,b+h/2,w,.02,h,GLAZE,a)
 for q in (-w/2+.04,w/2-.04):facade_box(m,x,y,u+q,o,b+h/2,.08,.08,h,M['Frame'],a)
 for zz in (b+.04,b+h-.04,b+h*trans):facade_box(m,x,y,u,o,zz,w,.08,.07,M['Frame'],a)
 facade_box(m,x,y,u,o+.01,b+h/2,.07,.08,h,M['Frame'],a)
 facade_box(m,x,y,u,o+.01,b+h*trans/2,w,.05,.03,M['Frame'],a)
 facade_box(m,x,y,u,.36,b-.03,w+.10,.28,.05,M['Frame'],a)
def seg41(m,x,y,u,b,w,h,r,a):
 # Segmental-headed ground-floor window: a rectangular hole to the crown (closed spandrels), glass
 # and a frame to the springing, a transom, the head on the true segment; a flat surround.
 spandrels(m,x,y,u,b,w,h,r,a,W41)
 casement41(m,x,y,u,b,w,h,a,.70)
 R_=(w*w/4+r*r)/(2*r);t0=math.asin(w/2/R_);zc=b+h+r-R_;k=10
 arc=[(u+R_*math.sin(t0*(2*i/k-1)),zc+R_*math.cos(t0*(2*i/k-1))) for i in range(k+1)]
 m.faces([lp(x,y,uu,.14,zz,a) for uu,zz in [(u+w/2,b+h)]+arc[::-1]+[(u-w/2,b+h)]],[tuple(range(k+3))],GLAZE)
 town_path(m,[lp(x,y,uu,.18,zz-.04,a) for uu,zz in arc],.04,M['Frame'])
 R2=R_+.20;t2=math.asin((w/2+.20)/R2)
 town_path(m,[lp(x,y,u+R2*math.sin(t2*(2*i/k-1)),.39,zc+R2*math.cos(t2*(2*i/k-1))-.02,a) for i in range(k+1)],.07,T41)
 for s in (-1,1):facade_box(m,x,y,u+s*(w/2+.10),.39,b+h/2,.20,.07,h,T41,a)
 facade_box(m,x,y,u,.39,b-.10,w+.40,.07,.20,T41,a)
def rect41(m,x,y,u,b,w,h,a,bw=.19):
 surround36(m,x,y,u,b,w,h,a,T41,bw,.39);casement41(m,x,y,u,b,w,h,a,.72)
def up41(m,x,y,u,a,b=5.25,h=2.30,w=1.10):
 # Upper window: casement, a flat surround and an apron down to the string course.
 surround36(m,x,y,u,b,w,h,a,T41,.14,.39);casement41(m,x,y,u,b,w,h,a,.72)
 facade_box(m,x,y,u,.385,(4.66+b-.14)/2,w+.28,.05,b-.14-4.66,T41,a)
def anchor41(m,x,y,u,z,a):
 ma=M['Iron'];town_rod(m,lp(x,y,u,.40,z-.40,a),lp(x,y,u,.40,z+.24,a),.022,ma,6)
 for sg in (-1,1):
  town_path(m,[lp(x,y,u+sg*(.02+.10*math.sin(math.pi*t/8)),.41,z+.16-.16*t/8,a) for t in range(9)],.017,ma)
  town_path(m,[lp(x,y,u+sg*(.07+.045*math.cos(math.tau*t/10)),.41,z+.0+.045*math.sin(math.tau*t/10),a) for t in range(11)],.014,ma)
def cornice41(m,x,y,L,a,gaps=()):
 # String 4.50-4.62; the eaves: a frieze band, a bed moulding and the corona 0.45 m out of the
 # wall, its front edge at 8.75 (the eaves line's elevation angle in the pitched views; the level
 # views' plane readings of 9.0-9.2 agree at this projection). The corona stops at gaps (u0, u1),
 # where a gable comes down onto the bed moulding.
 facade_box(m,x,y,0,.41,4.56,L,.12,.12,T41,a);facade_box(m,x,y,0,.44,4.625,L+.02,.16,.03,T41,a)
 facade_box(m,x,y,0,.38,7.92,L,.06,.18,T41,a);facade_box(m,x,y,0,.44,8.08,L,.17,.14,T41,a)
 facade_box(m,x,y,0,.51,8.28,L+.04,.31,.26,T41,a)
 at=-L/2-.05
 for g0,g1 in sorted(gaps)+[(L/2+.05,L/2+.05)]:
  if g0-at>.05:
   c=(at+g0)/2;l=g0-at
   facade_box(m,x,y,c,.58,8.57,l,.45,.32,T41,a)
   facade_box(m,x,y,c,.61,8.76,l,.51,.05,M['Roof'],a)
  at=max(at,g1)
def quoins41(m,x,y,u,side,a,z0=.75,z1=7.85,course=.40):
 k=0;z=z0
 while z+.1<z1:
  top=min(z+course-.06,z1);ln=.62 if k%2==0 else .40
  facade_box(m,x,y,u+side*ln/2,.38,(z+top)/2,ln,.05,top-z,T41,a);z+=course;k+=1
def scroll_gable(m,x,y,uc,base,W,crown,a,shoulder=None,o1=.40):
 # A gable in the wall face with a scrolled segmental top: the body between the two volutes is a
 # closed prism under an arc; the volutes are rods curling out at the foot.
 k=16;hw=W/2;sh=shoulder if shoulder is not None else base+.35
 prof=[(uc-hw,base),(uc-hw,sh)]+[(uc-hw*math.cos(math.pi*i/k),sh+(crown-sh)*math.sin(math.pi*i/k)) for i in range(1,k)]+[(uc+hw,sh),(uc+hw,base)]
 vs=[lp(x,y,uu,o,zz,a) for o in (.005,o1) for uu,zz in prof];n=len(prof)
 m.faces(vs,[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],W41)
 town_path(m,[lp(x,y,uu,o1+.04,zz+.05,a) for uu,zz in prof[1:-1]],.07,T41)
 return prof
def volute(m,x,y,u,z,side,a,r=.32):
 pts=[lp(x,y,u+side*(r*(1-t/20)*math.cos(math.pi*1.6*t/20)),.30,z+r*(1-t/20)*math.sin(math.pi*1.6*t/20)+.02,a) for t in range(21)]
 town_path(m,pts,.08,T41)
 facade_box(m,x,y,u+side*.05,.20,z+.10,r*2,.40,.20,W41,a)

m=b41_new('SM_Building_92412838','Kvarnholmen/Södra Långgatan north')
H41=Z['fr']['height']
UPX=[-0.75,2.58,6.02,9.49,12.72,15.90,19.11,22.32,25.62,28.43,31.26,34.07,36.96,39.82,42.92,45.50]
for zone in ('fr','ew'):
 for w in walls(zone):
  k=kind41(w);HZ=Z[zone]['height']
  if k is None:
   if w['kind']=='outer':plain(m,w,HZ,W41,M['Frame'],T41,2,1.1)
   else:bz_wall(m,w['p'],w['q'],w['z0'],HZ,[],W41)
   continue
  x,y,L,a=sf_edge(w['p'],w['q'])
  if k=='sodra':
   S=lambda X:U(w,X,-70.1)
   # The ground floor, x from the chained panoramas (outer edges of the openings).
   gar=[(-1.95,.35),(1.45,3.84)]
   rect=[(8.92,10.12),(21.85,22.84)]
   wide=(15.37,19.59)
   doors=[(5.29,6.61),(12.31,13.16)]
   segs=[(25.08,26.16),(27.95,28.92),(30.75,31.78),(39.22,40.18),(42.30,43.25),(44.95,46.05)]
   portal=(34.45,36.36)
   holes=[(S((a0+b0)/2),.30,b0-a0,3.28,0) for a0,b0 in gar]+[(S((a0+b0)/2),1.45,b0-a0,2.13,0) for a0,b0 in rect]
   holes+=[(S(sum(wide)/2),1.50,wide[1]-wide[0],2.09,0)]+[(S((a0+b0)/2),.30,b0-a0,2.22,0) for a0,b0 in doors]
   holes+=[(S((a0+b0)/2),1.58,b0-a0,1.62+.18,0) for a0,b0 in segs]
   pu=S(sum(portal)/2);pw=portal[1]-portal[0];holes+=[(pu,.75,pw,2.68,0)]
   holes+=[(S(X),5.25,1.10,2.30,0) for X in UPX]
   bz_wall(m,w['p'],w['q'],0,HZ,holes,W41)
   # Garages: boarded doors, a glazed transom row over them, a flat surround.
   for a0,b0 in gar:
    u=S((a0+b0)/2);ww=b0-a0
    surround36(m,x,y,u,.30,ww,3.28,a,T41,.18,.39)
    facade_box(m,x,y,u,.22,(.30+2.56)/2,ww,.06,2.26,M['GarageWood'],a)
    for j in range(1,12):facade_box(m,x,y,u-ww/2+j*ww/12,.25,1.43,.03,.03,2.2,M['Dark'],a)
    facade_box(m,x,y,u,.25,1.43,.06,.05,2.26,M['Dark'],a)
    facade_box(m,x,y,u,.16,3.10,ww,.02,.92,GLAZE,a)
    for j in range(5):facade_box(m,x,y,u-ww/2+j*ww/4,.22,3.10,.07,.08,.92,M['Frame'],a)
    for zz in (2.62,3.54):facade_box(m,x,y,u,.22,zz,ww,.08,.07,M['Frame'],a)
   # The two doors of 1940: stone surrounds, a recessed panel over each (the anchors hang there).
   for a0,b0 in doors:
    u=S((a0+b0)/2);ww=b0-a0
    for s in (-1,1):facade_box(m,x,y,u+s*(ww/2+.12),.42,(.30+2.64)/2,.24,.14,2.34,M['Stone'],a)
    facade_box(m,x,y,u,.44,2.63,ww+.60,.18,.14,M['Stone'],a)
    facade_box(m,x,y,u,.18,1.41,ww,.06,2.22,M['BrownDoor'],a)
    facade_box(m,x,y,u,.15,2.12,ww-.20,.02,.55,GLAZE,a)
    facade_box(m,x,y,u,.38,3.27,ww+.40,.05,1.05,T41,a);facade_box(m,x,y,u,.34,3.27,ww+.20,.04,.85,W41,a)
    facade_box(m,x,y,u,.355+.225,.15,ww+.50,.45,.30,M['Step'],a)
   for a0,b0 in rect:rect41(m,x,y,S((a0+b0)/2),1.45,b0-a0,2.13,a)
   # The wide window of twelve lights with iron bars behind the glass.
   u=S(sum(wide)/2);ww=wide[1]-wide[0]
   surround36(m,x,y,u,1.50,ww,2.09,a,T41,.20,.39)
   facade_box(m,x,y,u,.14,2.545,ww,.02,2.09,GLAZE,a)
   for j in range(7):facade_box(m,x,y,u-ww/2+.04+j*(ww-.08)/6,.18,2.545,.08,.08,2.09,M['Frame'],a)
   for zz in (1.54,2.66,3.55):facade_box(m,x,y,u,.18,zz,ww,.08,.08,M['Frame'],a)
   for j in range(24):town_rod(m,lp(x,y,u-ww/2+(j+.5)*ww/24,.10,1.55,a),lp(x,y,u-ww/2+(j+.5)*ww/24,.10,3.55,a),.012,M['Iron'],4)
   facade_box(m,x,y,u,.36,1.47,ww+.10,.28,.05,M['Frame'],a)
   for a0,b0 in segs:seg41(m,x,y,S((a0+b0)/2),1.58,b0-a0,1.62,.18,a)
   # The rusticated portal: blocks up the jambs, voussoirs and a keystone, the glazed double door.
   R_=pw/2;sp=.75+2.68-R_
   for j in range(6):
    zb=.75+j*(sp-.75)/6;zt=zb+(sp-.75)/6-.05;ext=.55 if j%2==0 else .40
    for s in (-1,1):facade_box(m,x,y,pu+s*(pw/2+ext/2),.46,(zb+zt)/2,ext,.22,zt-zb,M['Stone'],a)
   for j in range(9):
    t0=math.pi*j/9+.02;t1=math.pi*(j+1)/9-.02;rr=.62 if j==4 else .48
    ring=[(pu+R_*math.cos(t0),sp+R_*math.sin(t0)),(pu+R_*math.cos(t1),sp+R_*math.sin(t1)),(pu+(R_+rr)*math.cos(t1),sp+(R_+rr)*math.sin(t1)),(pu+(R_+rr)*math.cos(t0),sp+(R_+rr)*math.sin(t0))]
    vs=[lp(x,y,uu,o,zz,a) for o in (.355,.60) for uu,zz in ring]
    m.faces(vs,[(3,2,1,0),(4,5,6,7)]+[(i,(i+1)%4,(i+1)%4+4,i+4) for i in range(4)],M['Stone'])
   facade_box(m,x,y,pu,.20,.75+(sp-.75)/2,pw,.06,sp-.75,M['Door'],a)
   facade_box(m,x,y,pu,.16,.75+1.9,pw-.3,.02,1.2,GLAZE,a)
   k_=16;m.faces([lp(x,y,pu+R_*math.cos(math.pi*i/k_),.14,sp+R_*math.sin(math.pi*i/k_),a) for i in range(k_+1)],[tuple(range(k_+1))[::-1]],GLAZE)
   for q in (-pw/2+.06,0,pw/2-.06):facade_box(m,x,y,pu+q,.22,.75+(sp-.75)/2,.10,.08,sp-.75,M['Door'],a)
   facade_box(m,x,y,pu,.22,sp,pw,.08,.10,M['Door'],a)
   steps36(m,x,y,pu,a,2.30,2.00,.75,3,1.05,M['Step'])
   # Upper windows, the string, the cornice, quoins, the quoin strip of 1888, anchors, downpipes.
   for X in UPX:up41(m,x,y,S(X),a)
   cornice41(m,x,y,L,a,[(S(17.79)-1.62,S(17.79)+1.62)])
   plinth36(m,x,y,L,a,[(S(a0)-.25,S(b0)+.25) for a0,b0 in gar+doors]+[(pu-pw/2-.7,pu+pw/2+.7)],.75,M['Plinth'])
   quoins41(m,x,y,S(-2.996),1,a);quoins41(m,x,y,S(47.11),-1,a)
   k2=0;z=.75
   while z+.1<4.45:
    top=min(z+.34,4.45);facade_box(m,x,y,S(24.13),.39,(z+top)/2,.53,.07,top-z,T41,a);z+=.40
   for z0 in (4.7,):
    for s0,s1 in ((23.87,24.40),):facade_box(m,x,y,S((s0+s1)/2),.39,(z0+7.85)/2,.53,.07,7.85-z0,T41,a)
   for X in (-2.11,4.02,10.26,14.29,20.69,26.95,29.79,32.63,38.35,41.26):anchor41(m,x,y,S(X),4.15,a)
   for X in (-2.57,10.92,23.35,29.60,41.45):town_rod(m,lp(x,y,S(X),.50,.25,a),lp(x,y,S(X),.50,8.70,a),.055,M['Dark'],8)
  elif k=='ostra':
   S=lambda Y:U(w,47.3,Y)
   SIDE=[-66.74,-63.79,-60.72,-57.68,-54.70]
   ys=[Y for Y in SIDE if abs(S(Y))<L/2-.8]
   holes=[(S(Y),1.58,1.00,1.80,0) for Y in ys]+[(S(Y),5.25,1.00,2.30,0) for Y in ys]
   bz_wall(m,w['p'],w['q'],0,HZ,holes,W41)
   for Y in ys:seg41(m,x,y,S(Y),1.58,1.00,1.62,.18,a);up41(m,x,y,S(Y),a,5.25,2.30,1.00)
   cornice41(m,x,y,L,a);plinth36(m,x,y,L,a,[],.75,M['Plinth'])
   if zone=='fr':quoins41(m,x,y,S(-70.54),1,a)
   for Y in (-65.2,-62.2,-56.2):
    if abs(S(Y))<L/2-.3:anchor41(m,x,y,S(Y),4.15,a)
  else:
   # The western gable wall over the garage yard: plain render, the plinth, the quoins.
   bz_wall(m,w['p'],w['q'],0,HZ,[],W41);plinth36(m,x,y,L,a,[],.75,M['Plinth'])
   cornice41(m,x,y,L,a)
sl=roof34(m,'fr',M['Roof'],W41)
sl2=roof34(m,'ew',M['Roof'],W41)
rear35(m,'rw',W41,M['Frame'],M['Roof'],2)
# The two gables on the street front, triangulated from panoramas "40" and "43" (central gable) and
# "40" and "41" (lunette gable), in the chained cameras' frame.
for w in walls('fr'):
 if kind41(w)!='sodra':continue
 x,y,L,a=sf_edge(w['p'],w['q']);S=lambda X:U(w,X,-70.1)
 # The baroque central gable (1888): body 33.51-37.43 in the wall face, rising behind the cornice;
 # its window 9.60-10.45 (segmental head), set 0.13 m back; its moulded ledge 10.62-10.78, 0.5 m
 # out; the scrolled top 10.78-11.78, 0.3 m out, with the cartouche; volutes at the foot.
 gu=S(35.47);gb=8.70;GL=10.62
 bz_wall(m,lp(x,y,gu-1.96,0,0,a)[:2],lp(x,y,gu+1.96,0,0,a)[:2],gb,GL,[(0,9.60,1.62,.85,0)],W41)
 spandrels(m,x,y,gu,9.60,1.62,.70,.15,a,W41);casement41(m,x,y,gu,9.60,1.62,.85,a,.72,.05)
 for s_ in (-1,1):
  facade_box(m,x,y,gu+s_*1.72,.43,(gb+GL)/2,.44,.15,GL-gb,T41,a)
  volute(m,x,y,gu+s_*2.25,9.30,s_,a,.36)
 facade_box(m,x,y,gu,.52,GL+.04,4.30,.33,.08,T41,a);facade_box(m,x,y,gu,.60,GL+.12,4.40,.49,.08,T41,a)
 scroll_gable(m,x,y,gu,GL+.16,4.10,11.78,a,GL+.16,.65)
 for dz,wdt in ((11.0,1.1),(11.28,.7)):facade_box(m,x,y,gu,.72,dz,wdt,.14,.26,M['Stone'],a)
 town_path(m,[lp(x,y,gu+.24*math.cos(math.tau*t/12),.80,11.50+.14*math.sin(math.tau*t/12),a) for t in range(13)],.05,M['Stone'])
 facade_box(m,x,y,gu,-1.3,(gb+GL)/2,3.92,2.6,GL-gb,W41,a)
 for s_ in (-1,1):
  vs=[lp(x,y,gu+s_*2.1,.30,GL+.2,a),lp(x,y,gu,.30,11.70,a),lp(x,y,gu,-2.6,11.70,a),lp(x,y,gu+s_*2.1,-2.6,GL+.2,a)]
  m.faces(vs,[(0,1,2,3) if s_<0 else (3,2,1,0)],M['Roof'])
 # The lunette gable (1940): its face 0.3 m out of the wall, on the cornice (which stops under it);
 # the base 8.45, the lunette 8.46-8.80 (1.34 wide), the scrolled top to 10.2; volutes at the foot.
 lu=S(17.79);lb=8.45;o1=.655
 scroll_gable(m,x,y,lu,lb,3.30,10.20,a,9.00,o1)
 R_=(1.34**2/4+.34**2)/(2*.34);t0=math.asin(.67/R_);zc=8.80-R_;k_=12
 arc=[(lu+R_*math.sin(t0*(2*i/k_-1)),zc+R_*math.cos(t0*(2*i/k_-1))) for i in range(k_+1)]
 m.faces([lp(x,y,uu,o1+.01,zz,a) for uu,zz in [(lu+.67,8.46)]+arc[::-1]+[(lu-.67,8.46)]],[tuple(range(k_+3))],GLAZE)
 town_path(m,[lp(x,y,uu,o1+.03,zz,a) for uu,zz in arc]+[lp(x,y,lu-.67,o1+.03,8.46,a)],.04,M['Frame'])
 R2=R_+.22;t2=math.asin(.89/R2)
 town_path(m,[lp(x,y,lu+R2*math.sin(t2*(2*i/k_-1)),o1+.06,zc+R2*math.cos(t2*(2*i/k_-1)),a) for i in range(k_+1)],.07,T41)
 facade_box(m,x,y,lu,o1+.04,8.47,1.60,.10,.06,T41,a)
 for s_ in (-1,1):volute(m,x,y,lu+s_*1.95,8.55,s_,a,.30)
 facade_box(m,x,y,lu,-1.3,(lb+10.3)/2,3.30,2.6,10.3-lb,W41,a)
 for s_ in (-1,1):
  vs=[lp(x,y,lu+s_*1.75,.30,9.10,a),lp(x,y,lu,.30,10.10,a),lp(x,y,lu,-2.6,10.10,a),lp(x,y,lu+s_*1.75,-2.6,9.10,a)]
  m.faces(vs,[(0,1,2,3) if s_<0 else (3,2,1,0)],M['Roof'])
b41_finish(m,'92412838')

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
# The cameras stand at their chained distance from the facade, measured from the model's wall face.
def fyN(X):return -69.73+(X+3.0)*(-70.54+69.73)/(47.11+3.0)
_C={'G':(35.11,5.11,2.52),'F':(25.40,4.79,2.54),'H':(15.42,4.60,2.50),'C':(5.09,4.36,2.49),'B':(-5.22,4.30,2.46)}
def _cam(n):X,D_,h=_C[n];return X,fyN(X)-.355-D_,h
block41_cameras=[
 sv_camera('241_Block41_Cal_Portal',*_cam('G'),332,0,90),
 sv_camera('242_Block41_Cal_Portal_Roof',*_cam('G'),332,20,90),
 sv_camera('243_Block41_Cal_1888',*_cam('F'),332,0,90),
 sv_camera('244_Block41_Cal_1940',*_cam('H'),332,0,90),
 sv_camera('245_Block41_Cal_1940_Roof',*_cam('H'),332,20,90),
 sv_camera('246_Block41_Cal_Garages',*_cam('C'),332,0,90),
 ('247_Block41_Aerial',(20.0,-95.0,30.0),(22.0,-62.0,6.0),28),
]
print('BLOCK41_GEOMETRY',len(block41_names))
