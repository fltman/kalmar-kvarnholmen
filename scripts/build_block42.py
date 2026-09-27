"""Pass 42: the district volume 92412873 along Östra Sjögatan, between pass 40's corner house and the
castle park, and its courtyard block with the Wahlberg house on the park.

From north to south on Östra Sjögatan:
- the Nordstjernan brewery (roughcast between stone quoin strips): a central bay of two tall white
  frames, each with a segmental-headed window below, a recessed panel and a round-arched window
  above, small third-storey windows, and a steep gable with a triple window to about 17 m; a south
  bay with one great round-arched window over a panel and small attic lights;
- house 2 (roughcast): three axes on three storeys in flat white surrounds, a wall dormer of three
  lights under a small pediment;
- a narrow roughcast house between stone strips: two axes, windows on the ground floor and two
  upper rows, a gable with a round window;
- the grey house (roughcast, "8"): two windows and a recessed entrance on the ground floor, blind
  panels (large and small) where the second-storey windows would be, one row of windows, a gable
  of three shuttered openings;
- the yellow corner house, Östra Sjögatan 1: two storeys in yellow render with cream surrounds, a
  double string course, four windows and the panelled double door on Östra Sjögatan, three axes
  to the park, a tile roof with a round-headed dormer.
The courtyard block and the Wahlberg house on the park keep pass 17's height and estimated look
(nine axes of cross windows, the door, the curved central attic with its balcony).

References: Google Street View April 2025 (five panoramas chained along Östra Sjögatan), view only.
Zones: source/block42.json; see references/block42-notes.md. Signs and lettering are omitted.
"""
B42D=json.loads((R/'source/block42.json').read_text());Z=B42D['zones']
block42_names=[];B42={}
for old in [k for k in list(materials) if k.startswith('M_Block42_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Rough','TownIvory',(.58,.53,.47),.95,0),
 ('White','TownIvory',(.93,.92,.88),.85,0),
 ('Strip','TownStone',(.78,.75,.68),.88,0),
 ('Panel','TownIvory',(.80,.78,.73),.88,0),
 ('Frame','TownPaintBrown',(.42,.12,.10),.55,0),
 ('Board','TownPaintBrown',(.30,.18,.13),.65,0),
 ('Granite','TownStone',(.33,.33,.34),.82,0),
 ('Plinth','TownStone',(.42,.43,.44),.82,0),
 ('Yellow','TownIvory',(.87,.72,.46),.88,0),
 ('Cream','TownIvory',(.90,.84,.66),.85,0),
 ('Door','TownPaintBrown',(.40,.12,.10),.55,0),
 ('Tile','TownTileRed',(.60,.30,.20),.80,0),
 ('Roof','TownMetalGrey',(.26,.27,.28),.55,.30),
 ('Pale','TownIvory',(.80,.79,.75),.88,0),
 ('Green','TownPaintBrown',(.25,.38,.28),.55,0),
 ('RoofRed','TownMetalRed',(.45,.18,.14),.60,.10),
 ('Iron','TownMetalGrey',(.05,.05,.055),.45,.40),
 ('Dark','TownMetalGrey',(.05,.055,.06),.40,.20),
 ]:
 name='M_Block42_'+key;B42[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block42_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B42;RO,WHT,FR=M['Rough'],M['White'],M['Frame']

def b42_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block42_names.append(name);return Mesh(name,category)
def b42_finish(m,osm):
 obj=s21_finish(m);obj['detail_pass']=42;obj['reference_notes']='references/block42-notes.md';obj['osm_way']=osm;return obj
def xf(Y):return 47.065+(Y+93.634)*(46.148-47.065)/(-140.978+93.634)
def kind42(w):
 ox,oy=outward(w)
 if w['kind']!='outer':return None
 if ox>.9 and min(w['p'][0],w['q'][0])>45.9:return 'ostra'
 if oy<-.9 and max(w['p'][0],w['q'][0])<23 and min(w['p'][1],w['q'][1])<-141:return 'wahl'
 if oy<-.9 and min(w['p'][0],w['q'][0])>34 and min(w['p'][1],w['q'][1])<-140.5:return 'park'
 return None
def casement42(m,x,y,u,b,w,h,a,frame=None,bars=3,trans=.70,o=.20):
 frame=frame or FR
 facade_box(m,x,y,u,o-.04,b+h/2,w,.02,h,GLAZE,a)
 for q in (-w/2+.04,w/2-.04):facade_box(m,x,y,u+q,o,b+h/2,.08,.08,h,frame,a)
 for zz in (b+.04,b+h-.04)+((b+h*trans,) if trans else ()):facade_box(m,x,y,u,o,zz,w,.08,.07,frame,a)
 facade_box(m,x,y,u,o+.01,b+h/2,.07,.08,h,frame,a)
 for k in range(1,bars):facade_box(m,x,y,u,o+.01,b+h*(trans or 1)*k/bars,w,.05,.03,frame,a)
 facade_box(m,x,y,u,.40,b-.03,w+.12,.20,.05,M['Dark'],a)
def arched42(m,x,y,u,b,w,spring,a,rise=None,frame=None):
 # Window with a round (rise None) or segmental head: rectangular hole to the crown, closed
 # spandrel prisms, glass on the head, a frame, glazing bars.
 frame=frame or FR;r=w/2 if rise is None else rise;crown=spring+r
 spandrels(m,x,y,u,b,w,spring-b,r,a,RO)
 R_=(w*w/4+r*r)/(2*r);t0=math.asin(min(1,w/2/R_));zc=crown-R_;k=14
 arc=[(u+R_*math.sin(t0*(2*i/k-1)),zc+R_*math.cos(t0*(2*i/k-1))) for i in range(k+1)]
 facade_box(m,x,y,u,.16,(b+spring)/2,w,.02,spring-b,GLAZE,a)
 m.faces([lp(x,y,uu,.16,zz,a) for uu,zz in [(u+w/2,spring)]+arc[::-1]+[(u-w/2,spring)]],[tuple(range(k+3))],GLAZE)
 town_path(m,[lp(x,y,uu,.20,zz-.04,a) for uu,zz in arc],.045,frame)
 for q in (-w/2+.04,0,w/2-.04):facade_box(m,x,y,u+q,.20,(b+spring)/2,.08,.08,spring-b,frame,a)
 for zz in (b+.04,spring):facade_box(m,x,y,u,.20,zz,w,.08,.07,frame,a)
 n=max(2,round((spring-b)/.42))
 for j in range(1,n):facade_box(m,x,y,u,.21,b+j*(spring-b)/n,w,.05,.03,frame,a)
 facade_box(m,x,y,u,.40,b-.03,w+.14,.22,.05,M['Dark'],a)
 return crown
def surround42(m,x,y,u,b,w,h,a,ma=None,bw=.17,o=.39):surround36(m,x,y,u,b,w,h,a,ma or WHT,bw,o)
def strip42(m,x,y,u0,u1,z0,z1,a,course=.62):
 # Stone quoin strip: alternating long and short blocks, flush-ish on the roughcast.
 k=0;z=z0;w=abs(u1-u0);c=(u0+u1)/2
 while z+.1<z1:
  top=min(z+course-.06,z1);ww=w if k%2==0 else w*.72
  facade_box(m,x,y,c,.38,(z+top)/2,ww,.05,top-z,M['Strip'],a);z+=course;k+=1
def anchor42(m,x,y,u,z,a):
 ma=M['Iron'];town_rod(m,lp(x,y,u,.40,z-.40,a),lp(x,y,u,.40,z+.25,a),.024,ma,6)
 for sg in (-1,1):
  town_path(m,[lp(x,y,u+sg*(.02+.12*math.sin(math.pi*t/8)),.41,z+.18-.18*t/8,a) for t in range(9)],.018,ma)
  town_path(m,[lp(x,y,u+sg*(.08+.05*math.cos(math.tau*t/10)),.41,z+.0+.05*math.sin(math.tau*t/10),a) for t in range(11)],.015,ma)
def eaves42(m,x,y,L,a,H,ma,out=.45):
 facade_box(m,x,y,0,.40,H-.22,L,.10,.34,ma,a)
 facade_box(m,x,y,0,.36+out/2,H-.04,L+.10,out,.10,ma,a)
 town_rod(m,lp(x,y,-L/2,.36+out,H-.03,a),lp(x,y,L/2,.36+out,H-.03,a),.06,METAL,8)
def flatcap(m,zone,ma,rise=.3):
 for g in Z[zone]['polygons']:
  pts=simplify([tuple(v) for v in g],.3);H=Z[zone]['height']
  inset_roof(m,pts,H,min(1.2,.3*min(math.dist(p,q) for p,q in zip(pts,pts[1:]+pts[:1]))),rise,ma,.05)
def gable42(m,x,y,uc,base,w,apex,a,body,trim,depth=2.6,roof=None):
 # A steep street gable standing in the wall face, its body running back into the roof.
 tri=[(uc-w/2,base),(uc+w/2,base),(uc,apex)]
 vs=[lp(x,y,uu,o,zz,a) for o in (-depth,.355) for uu,zz in tri]
 m.faces(vs,[(2,1,0),(3,4,5),(0,1,4,3),(1,2,5,4),(2,0,3,5)],body)
 for (u0,z0),(u1,z1) in ((tri[0],tri[2]),(tri[2],tri[1])):town_rod(m,lp(x,y,u0,.42,z0,a),lp(x,y,u1,.42,z1,a),.09,trim,8)
 if roof:
  for s in (-1,1):
   q=[lp(x,y,uc+s*(w/2+.12),.50,base-.06,a),lp(x,y,uc,.50,apex+.10,a),lp(x,y,uc,-depth,apex+.10,a),lp(x,y,uc+s*(w/2+.12),-depth,base-.06,a)]
   m.faces(q,[(0,1,2,3) if s<0 else (3,2,1,0)],roof)

m=b42_new('SM_Kvarnholmen_House_92412873','Kvarnholmen/Östra Sjögatan')
for zone in Z:
 HZ=Z[zone]['height']
 for w in walls(zone):
  k=kind42(w);x,y,L,a=sf_edge(w['p'],w['q'])
  if k=='ostra':
   S=lambda Y:U(w,xf(Y),Y)
   wall=M['Yellow'] if zone=='ye' else RO
   if zone=='bn':
    bz_wall(m,w['p'],w['q'],0,HZ,[],RO);strip42(m,x,y,S(-94.80),S(-95.0),.9,HZ-.3,a)
    facade_box(m,x,y,0,.40,.45,L,.10,.90,M['Granite'],a);eaves42(m,x,y,L,a,HZ,WHT)
   elif zone=='bc':
    AX=[(-101.06,-99.68),(-97.70,-96.28)]
    holes=[]
    for y0,y1 in AX:
     u=S((y0+y1)/2);ww=abs(y1-y0)
     holes+=[(u,1.22,ww,1.73+.23,0),(u,4.82,ww,1.59+ww/2,0),(u,8.30,.90,1.20,0)]
    holes+=[(S(-98.85),10.95,.60,1.55,0)]
    bz_wall(m,w['p'],w['q'],0,HZ,holes,RO)
    for y0,y1 in AX:
     u=S((y0+y1)/2);ww=abs(y1-y0)
     arched42(m,x,y,u,1.22,ww,2.95,a,.23)
     arched42(m,x,y,u,4.82,ww,6.41,a)
     facade_box(m,x,y,u,.30,(3.32+4.54)/2,ww,.05,1.22,RO,a)
     # The tall white frame round both windows and the panel, round-headed.
     for s in (-1,1):facade_box(m,x,y,u+s*(ww/2+.13),.40,(.9+6.41)/2,.26,.10,6.41-.9,WHT,a)
     p18_arch(m,*lp(x,y,u,0,0,a)[:2],6.41,ww+.02,ww/2+.02,.24,.40,a,WHT,20)
     for zz in (3.26,4.62):facade_box(m,x,y,u,.40,zz,ww+.02,.10,.16,WHT,a)
     facade_box(m,x,y,u,.42,1.05,ww+.62,.14,.30,WHT,a)
     surround42(m,x,y,u,8.30,.90,1.20,a);casement42(m,x,y,u,8.30,.90,1.20,a,None,2,None)
     facade_box(m,x,y,u,.20,.45,ww,.06,.80,M['Board'],a)
    gu=S(-98.85)
    surround42(m,x,y,gu,10.95,.60,1.55,a);casement42(m,x,y,gu,10.95,.60,1.55,a,None,3,None)
    for s in (-1,1):
     facade_box(m,x,y,gu+s*.75,.20+.2,11.45,.36,.10,1.0,WHT,a);facade_box(m,x,y,gu+s*.75,.18,11.45,.28,.02,.92,GLAZE,a)
    strip42(m,x,y,S(-102.41),S(-102.60),.9,HZ-.3,a);strip42(m,x,y,S(-95.0),S(-95.23),.9,HZ-.3,a)
    facade_box(m,x,y,0,.40,.45,L,.10,.90,M['Granite'],a)
    for Y in (-102.0,-98.85,-95.6):anchor42(m,x,y,S(Y),7.55,a)
    eaves42(m,x,y,L,a,HZ,WHT)
    gable42(m,x,y,S(-98.85),HZ-.05,abs(S(-95.1)-S(-102.5)),17.2,a,RO,WHT,2.8,M['Roof'])
    facade_box(m,x,y,S(-98.85),.20,17.35,.70,.70,.40,WHT,a)
   elif zone=='bs':
    u=S(-104.58);ww=2.28
    bz_wall(m,w['p'],w['q'],0,HZ,[(u,1.94,ww,3.42+ww/2,0)]+[(S(Y),10.30,.42,.60,0) for Y in (-105.4,-104.58,-103.76)],RO)
    arched42(m,x,y,u,1.94,ww,5.36,a)
    for q in (-.38,.38):facade_box(m,x,y,u+q,.21,3.65,.06,.06,3.4,FR,a)
    for s in (-1,1):facade_box(m,x,y,u+s*(ww/2+.20),.40,(.9+5.36)/2,.40,.10,5.36-.9,WHT,a)
    p18_arch(m,*lp(x,y,u,0,0,a)[:2],5.36,ww+.04,ww/2+.02,.38,.40,a,WHT,24)
    facade_box(m,x,y,u,.40,1.52,ww+.80,.10,.64,WHT,a);facade_box(m,x,y,u,.44,1.20,ww+.90,.20,.10,WHT,a)
    facade_box(m,x,y,u,.44,1.86,ww+.40,.20,.08,M['Dark'],a)
    for Y in (-105.4,-104.58,-103.76):
     surround42(m,x,y,S(Y),10.30,.42,.60,a,WHT,.10);casement42(m,x,y,S(Y),10.30,.42,.60,a,None,2,None)
    facade_box(m,x,y,0,.40,.45,L,.10,.90,M['Granite'],a)
    for Y in (-106.35,-103.0):anchor42(m,x,y,S(Y),7.55,a)
    eaves42(m,x,y,L,a,HZ,WHT)
   elif zone=='h2':
    AX=[(-113.50,-112.45),(-111.21,-110.11),(-108.84,-107.78)]
    rows=[(1.85,3.02),(4.79,5.84),(7.25,8.30)]
    holes=[(S((y0+y1)/2),b,abs(y1-y0),t-b,0) for y0,y1 in AX for b,t in rows]
    bz_wall(m,w['p'],w['q'],0,HZ,holes,RO)
    for u,b,ww,hh,r in holes:surround42(m,x,y,u,b,ww,hh,a);casement42(m,x,y,u,b,ww,hh,a)
    strip42(m,x,y,S(-114.69),S(-115.0),.8,HZ-.3,a)
    facade_box(m,x,y,0,.40,.40,L,.10,.80,M['Plinth'],a)
    for Y in (-114.3,-111.85,-109.5,-107.1):anchor42(m,x,y,S(Y),6.7,a)
    for Yp in (-106.75,-114.55):town_rod(m,lp(x,y,S(Yp),.50,.25,a),lp(x,y,S(Yp),.50,HZ,a),.055,M['Dark'],8)
    eaves42(m,x,y,L,a,HZ,WHT)
    # The wall dormer: three lights under a small pediment, in the wall face over the eaves.
    du=S(-110.65);dw=abs(S(-108.66)-S(-112.63))
    ops=[(S(Y),10.40,.95,.80,0) for Y in (-111.86,-110.66,-109.44)]
    bz_wall(m,lp(x,y,du-dw/2,0,0,a)[:2],lp(x,y,du+dw/2,0,0,a)[:2],HZ-.3,11.55,[(uu-du,b,ww,hh,r) for uu,b,ww,hh,r in ops],RO)
    for uu,b,ww,hh,r in ops:surround42(m,x,y,uu,b,ww,hh,a,WHT,.10);casement42(m,x,y,uu,b,ww,hh,a,None,2,None)
    facade_box(m,x,y,du,.44,11.62,dw+.20,.20,.14,WHT,a)
    pediment35(m,x,y,du,11.68,dw*.55,12.83,a,RO,WHT,.40,.50,.18)
    facade_box(m,x,y,du,-1.2,(HZ+11.55)/2,dw,2.4,11.55-HZ+.3,RO,a)
    for s in (-1,1):
     q=[lp(x,y,du+s*(dw/2+.1),.30,11.62,a),lp(x,y,du,.30,12.6,a),lp(x,y,du,-2.4,12.6,a),lp(x,y,du+s*(dw/2+.1),-2.4,11.62,a)]
     m.faces(q,[(0,1,2,3) if s<0 else (3,2,1,0)],M['Roof'])
   elif zone=='hc':
    AX=[(-118.30,-117.40),(-116.62,-115.72)]
    rows=[(1.56,2.95),(6.20,7.25),(9.27,10.16)]
    holes=[(S((y0+y1)/2),b,abs(y1-y0),t-b,0) for y0,y1 in AX for b,t in rows]
    bz_wall(m,w['p'],w['q'],0,HZ,holes,RO)
    for u,b,ww,hh,r in holes:surround42(m,x,y,u,b,ww,hh,a);casement42(m,x,y,u,b,ww,hh,a)
    strip42(m,x,y,S(-115.0),S(-115.18),.8,HZ-.3,a);strip42(m,x,y,S(-118.83),S(-119.1),.8,HZ-.3,a)
    facade_box(m,x,y,0,.40,.40,L,.10,.80,M['Plinth'],a)
    eaves42(m,x,y,L,a,HZ,WHT)
    gu=S(-117.05);gw=abs(S(-119.0)-S(-115.1))
    gable42(m,x,y,gu,HZ-.05,gw,14.6,a,RO,WHT,2.6,M['Roof'])
    k_=20;town_path(m,[lp(x,y,gu+.36*math.cos(math.tau*t/k_),.42,12.55+.36*math.sin(math.tau*t/k_),a) for t in range(k_+1)],.06,WHT)
    m.faces([lp(x,y,gu+.30*math.cos(math.tau*t/k_),.38,12.55+.30*math.sin(math.tau*t/k_),a) for t in range(k_)],[tuple(range(k_))],GLAZE)
    town_rod(m,lp(x,y,S(-119.46),.50,.25,a),lp(x,y,S(-119.46),.50,HZ,a),.055,M['Dark'],8)
   elif zone=='gr':
    AX=[(-125.72,-124.72),(-123.93,-122.97)]
    ent=(S(-121.80),0,1.20,2.60,0)
    holes=[(S((y0+y1)/2),1.50,abs(y1-y0),1.35,0) for y0,y1 in AX]+[ent]
    ups=[(S((y0+y1)/2),6.02,abs(y1-y0),1.30,0) for y0,y1 in AX]+[(S(-121.80),6.02,.95,1.30,0)]
    att=[(S(Y),10.45,.70,1.10,0) for Y in (-125.22,-123.45,-121.80)]
    bz_wall(m,w['p'],w['q'],0,HZ,holes+ups+att,RO)
    for u,b,ww,hh,r in holes[:2]+ups:surround42(m,x,y,u,b,ww,hh,a,WHT,.17);casement42(m,x,y,u,b,ww,hh,a)
    # The recessed entrance: white reveals, steps inside, the red door at the back.
    eu=ent[0]
    for s in (-1,1):facade_box(m,x,y,eu+s*.57,-.10,1.30,.06,.95,2.60,WHT,a)
    facade_box(m,x,y,eu,-.10,2.57,1.20,.95,.06,WHT,a)
    facade_box(m,x,y,eu,-.55,1.62,.85,.06,2.0,M['Door'],a)
    for j in range(3):facade_box(m,x,y,eu,-.55+.45-(j+.5)*.30+.15,.10+j*.20,1.10,.30,.20+j*.20,M['Step'] if 'Step' in M else M['Plinth'],a)
    surround42(m,x,y,eu,0,1.20,2.60,a,WHT,.20)
    for j in range(3):facade_box(m,x,y,eu,.355+(3-j)*.17,.085*(j+1),1.35,(3-j)*.34,.17*(j+1),M['Plinth'],a)
    for u in [hh[0] for hh in holes[:2]]+[eu]:
     facade_box(m,x,y,u,.38,4.13,1.30,.05,1.28,M['Panel'],a);facade_box(m,x,y,u,.38,5.28,1.30,.05,.36,M['Panel'],a)
     facade_box(m,x,y,u,.38,8.40,1.30,.05,.40,M['Panel'],a)
    strip42(m,x,y,S(-126.42),S(-126.6),.8,HZ-.3,a)
    facade_box(m,x,y,0,.40,.40,L,.10,.80,M['Plinth'],a)
    eaves42(m,x,y,L,a,HZ,WHT)
    # The shuttered attic storey in the wall face under the eaves, and a small gable over the middle.
    ops=[(S(Y),10.45,.70,1.10,0) for Y in (-125.22,-123.45,-121.80)]
    for uu,b,ww,hh,r in ops:
     surround42(m,x,y,uu,b,ww,hh,a,WHT,.10);facade_box(m,x,y,uu,.40,b+hh/2,ww,.04,hh,M['Door'],a)
     for j in range(1,8):facade_box(m,x,y,uu,.43,b+j*hh/8,ww,.03,.03,M['Dark'],a)
    gu=S(-123.45);gw=1.9
    bz_wall(m,lp(x,y,gu-gw/2,0,0,a)[:2],lp(x,y,gu+gw/2,0,0,a)[:2],HZ-.3,12.35,[],RO)
    facade_box(m,x,y,gu,.44,12.42,gw+.2,.20,.14,WHT,a)
    pediment35(m,x,y,gu,12.48,gw+.1,13.45,a,RO,WHT,.40,.50,.16)
    facade_box(m,x,y,gu,-1.2,(HZ+12.35)/2,gw,2.4,12.35-HZ+.3,RO,a)
   elif zone=='ye':
    YW=[(-139.09,-138.08),(-136.51,-135.43),(-134.27,-133.22),(-131.39,-130.35)]
    door=(S(-128.53),.67,1.14,2.43,0)
    gh=[(S((y0+y1)/2),1.36,abs(y1-y0),1.69,0) for y0,y1 in YW]
    uh=[(S((y0+y1)/2),4.55,abs(y1-y0),1.45,0) for y0,y1 in YW]+[(S(-128.53),4.55,1.05,1.45,0)]
    bz_wall(m,w['p'],w['q'],0,HZ,gh+uh+[door],M['Yellow'])
    for u,b,ww,hh,r in gh+uh:surround42(m,x,y,u,b,ww,hh,a,M['Cream'],.12);casement42(m,x,y,u,b,ww,hh,a,M['Door'],3,None)
    du,db,dw,dh,_=door
    surround42(m,x,y,du,db,dw,dh,a,M['Cream'],.18)
    leaves39(m,x,y,du,db,dw,dh,a,M['Door'],M['Door'],.22,3) if 'leaves39' in globals() else facade_box(m,x,y,du,.22,db+dh/2,dw,.06,dh,M['Door'],a)
    for j in range(2):facade_box(m,x,y,du,.355+(2-j)*.20,.17+j*.25,dw+.60,(2-j)*.40,.34+j*.16,M['Plinth'],a)
    plinth36(m,x,y,L,a,[(du-dw/2-.30,du+dw/2+.30)],.65,M['Plinth'])
    facade_box(m,x,y,0,.42,3.58,L,.12,.36,M['Cream'],a);facade_box(m,x,y,0,.42,4.29,L,.12,.16,M['Cream'],a)
    for Y in (-126.75,-140.85):facade_box(m,x,y,S(Y),.40,3.6,.36,.08,7.0,M['Cream'],a)
    eaves42(m,x,y,L,a,HZ,M['Cream'],.40)
   continue
  if k=='park':
   # The yellow house's end to the castle park: three axes (estimated from an oblique view).
   ops=[(uu,1.36,1.05,1.69,0) for uu in (-L/2+2.9,0,L/2-2.9)]+[(uu,4.55,1.05,1.45,0) for uu in (-L/2+2.9,0,L/2-2.9)]
   bz_wall(m,w['p'],w['q'],0,HZ,ops,M['Yellow'])
   for u,b,ww,hh,r in ops:surround42(m,x,y,u,b,ww,hh,a,M['Cream'],.12);casement42(m,x,y,u,b,ww,hh,a,M['Door'],3,None)
   plinth36(m,x,y,L,a,[],.65,M['Plinth'])
   facade_box(m,x,y,0,.42,3.58,L,.12,.36,M['Cream'],a);facade_box(m,x,y,0,.42,4.29,L,.12,.16,M['Cream'],a)
   eaves42(m,x,y,L,a,HZ,M['Cream'],.40)
   continue
  if k=='wahl':
   # The Wahlberg house (pass 17's estimate, kept): nine axes of green cross windows on two
   # storeys, the door at the seventh axis, rusticated courses, a band, a curved central attic with
   # a window and a balcony in front of it.
   n=9;pitch=(L-.92)/n;ups=[];gfs=[]
   for j in range(n):
    u=-L/2+.46+(j+.5)*pitch
    ups.append((u,4.545,1.36,1.92,0))
    gfs.append((u,.12,2.1,2.94,0) if j==6 else (u,.72,1.36,1.92,0))
   bz_wall(m,w['p'],w['q'],0,HZ,ups+gfs,M['Pale'])
   for i,(u,b,ww,hh,r) in enumerate(gfs+ups):
    if b<.2:
     facade_box(m,x,y,u,.18,b+hh/2,ww,.06,hh,M['Green'],a);facade_box(m,x,y,u,.22,b+hh/2,.05,.05,hh,M['Dark'],a)
     facade_box(m,x,y,u,.45,.08,ww+.3,.4,.16,M['Plinth'],a)
    else:surround42(m,x,y,u,b,ww,hh,a,WHT,.12);casement42(m,x,y,u,b,ww,hh,a,M['Green'],2,.66)
   for zz in [.48+i*.30 for i in range(11)]:facade_box(m,x,y,0,.37,zz,L,.03,.02,M['Pale'],a)
   facade_box(m,x,y,0,.41,HZ/2-.10,L,.14,.15,WHT,a)
   plinth36(m,x,y,L,a,[(gfs[6][0]-1.15,gfs[6][0]+1.15)],.48,M['Plinth'])
   eaves42(m,x,y,L,a,HZ,WHT,.40)
   width=4.3;prof=[(-width/2,0),(width/2,0),(width/2,1.60),(1.16,1.60)]+[(1.16*math.cos(i*math.pi/24),1.60+.9*math.sin(i*math.pi/24)) for i in range(25)]+[(-width/2,1.60)]
   vs=[lp(x,y,uu,o,HZ+zz,a) for o in (-.30,.36) for uu,zz in prof];nn=len(prof)
   m.faces(vs,[tuple(range(nn-1,-1,-1)),tuple(range(nn,2*nn))]+[(i,(i+1)%nn,(i+1)%nn+nn,i+nn) for i in range(nn)],M['Pale'])
   town_path(m,[lp(x,y,uu,.40,HZ+zz,a) for uu,zz in prof[2:]],.05,WHT)
   casement42(m,x,y,0,HZ+.25,1.05,1.25,a,M['Green'],2,None,.42)
   facade_box(m,x,y,0,.82,HZ+.04,4.9,1.0,.20,M['Plinth'],a)
   for j in range(25):facade_box(m,x,y,-2.35+j*4.7/24,1.29,HZ+.62,.025,.035,1.04,M['Green'],a)
   for zz in (HZ+.22,HZ+1.14):facade_box(m,x,y,0,1.29,zz,4.80,.07,.06,M['Green'],a)
   continue
  if w['kind']=='outer':plain(m,w,HZ,M['Pale'] if zone=='bk' else RO,FR,WHT,2 if zone in ('bk','ye') else 3,.9)
  else:bz_wall(m,w['p'],w['q'],w['z0'],HZ,[],M['Pale'] if zone=='bk' else (M['Yellow'] if zone=='ye' else RO))
for zone in ('bc','bs','h2','hc','gr'):roof34(m,zone,M['Roof'],RO)
sl=roof34(m,'ye',M['Tile'],M['Yellow'])
flatcap(m,'bn',M['Roof'])
flatcap(m,'bk',M['RoofRed'],.35)
# The yellow house's round-headed dormer on Östra Sjögatan.
for w in walls('ye'):
 if kind42(w)=='ostra':
  x,y,L,a=sf_edge(w['p'],w['q']);roof_dormer(m,x,y,U(w,xf(-133.35),-133.35),a,7.1,sl,.55,.95,.80,M['Tile'],M['Tile'],WHT,True)
b42_finish(m,'92412873')

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
# Chained camera positions (distance from the real facade, 0.355 m added for the model's wall face).
_C={'A':(-100.72,3.39),'B':(-110.30,3.27),'C':(-120.49,3.52),'D':(-130.09,3.84),'E':(-141.88,4.60)}
def _cam(n):Y,D_=_C[n];return xf(Y)+.355+D_,Y,2.32
block42_cameras=[
 sv_camera('248_Block42_Cal_Brewery',*_cam('A'),242,0,90),
 sv_camera('249_Block42_Cal_Brewery_Up',*_cam('A'),242,35,90),
 sv_camera('250_Block42_Cal_House2',*_cam('B'),242,0,90),
 sv_camera('251_Block42_Cal_House2_Up',*_cam('B'),242,35,90),
 sv_camera('252_Block42_Cal_Grey',*_cam('C'),242,0,90),
 sv_camera('253_Block42_Cal_Grey_Up',*_cam('C'),242,35,90),
 sv_camera('254_Block42_Cal_Yellow',*_cam('D'),242,0,90),
 sv_camera('255_Block42_Cal_Yellow_Up',*_cam('D'),242,35,90),
 ('256_Block42_Aerial',(75.0,-118.0,34.0),(38.0,-118.0,4.0),28),
]
print('BLOCK42_GEOMETRY',len(block42_names))
