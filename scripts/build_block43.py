"""Pass 43: the district volume 91846978, the long block between Södra Långgatan, Proviantgatan and
Storgatan; its Södra Långgatan front (numbers 49-59), from west to east:
- the cream hotel range: a garage door and two storeys of windows under a roof terrace; a gabled
  four-storey middle with French balconies on two axes and an arcade with the entrances; a
  three-storey range beyond. The ground floor is banded render in a greyer beige, under a band.
- a range of ochre roughcast panels in cream frames (one, two, one and two windows), a stone quoin
  strip at its west end, flat roof with a terrace;
- a blue-grey four-storey house between cream pilasters with a front gable, bands between the
  storeys, medallions and a recessed entrance (number 55);
- a grey roughcast two-storey house with a pale strip, a tile roof with roof windows;
- the salmon-and-beige corner range: salmon ground floor, a cream band, beige upper storey, a front
  gable with two windows and a roundel, a recessed entrance (57), a French balcony at the corner.
The Storgatan and Proviantgatan sides and the courtyard wings stay plain (district height).

References: Google Street View April 2025 (eight panoramas chained along the street, anchored at
both ends), view only. Zones: source/block43.json; see references/block43-notes.md. Signs and the
house numbers are omitted.
"""
B43D=json.loads((R/'source/block43.json').read_text());Z=B43D['zones']
block43_names=[];B43={}
for old in [k for k in list(materials) if k.startswith('M_Block43_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Cream','TownIvory',(.90,.88,.81),.88,0),
 ('Beige','TownIvory',(.84,.81,.75),.88,0),
 ('Ochre','TownIvory',(.83,.70,.46),.95,0),
 ('Blue','TownIvory',(.72,.77,.80),.88,0),
 ('Grey','TownIvory',(.72,.71,.68),.95,0),
 ('Salmon','TownIvory',(.85,.60,.45),.88,0),
 ('Sand','TownIvory',(.93,.84,.74),.88,0),
 ('White','TownIvory',(.94,.94,.91),.82,0),
 ('Stone','TownStone',(.80,.77,.70),.86,0),
 ('Frame','TownPaintWhite',(.95,.95,.93),.55,0),
 ('DoorGrey','TownPaintBrown',(.55,.57,.58),.60,0),
 ('Garage','TownPaintBrown',(.75,.76,.76),.60,0),
 ('Tile','TownTileRed',(.62,.30,.20),.80,0),
 ('Roof','TownMetalGrey',(.22,.23,.24),.55,.30),
 ('Iron','TownMetalGrey',(.05,.05,.055),.45,.40),
 ('Dark','TownMetalGrey',(.05,.055,.06),.40,.20),
 ]:
 name='M_Block43_'+key;B43[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block43_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B43;FW=M['Frame']

def b43_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block43_names.append(name);return Mesh(name,category)
def b43_finish(m,osm):
 obj=s21_finish(m);obj['detail_pass']=43;obj['reference_notes']='references/block43-notes.md';obj['osm_way']=osm;return obj
def yf(X):return -69.94+(X-100.12)*(-71.52+69.94)/(176.97-100.12)
def street43(w):
 ox,oy=outward(w);return w['kind']=='outer' and oy<-.9 and min(w['p'][1],w['q'][1])<-69.5
def win43(m,x,y,u,b,w,h,a,trans=.72,o=.20,bars=2):
 # A white modern casement with glazing bars, in a shallow reveal, a sheet sill.
 facade_box(m,x,y,u,o-.04,b+h/2,w,.02,h,GLAZE,a)
 for q in (-w/2+.04,w/2-.04):facade_box(m,x,y,u+q,o,b+h/2,.08,.08,h,FW,a)
 for zz in (b+.04,b+h-.04,b+h*trans):facade_box(m,x,y,u,o,zz,w,.08,.07,FW,a)
 facade_box(m,x,y,u,o+.01,b+h/2,.07,.08,h,FW,a)
 for k in range(1,bars+1):facade_box(m,x,y,u,o+.01,b+h*trans*k/(bars+1),w,.04,.03,FW,a)
 facade_box(m,x,y,u,.40,b-.03,w+.12,.20,.05,M['White'],a)
def rail43(m,x,y,u,z,w,a):
 # A French balcony: a black railing in front of the opening.
 facade_box(m,x,y,u,.45,z+.02,w+.10,.10,.04,M['Iron'],a)
 for zz in (z+.95,z+.50):facade_box(m,x,y,u,.45,zz,w+.10,.06,.04,M['Iron'],a)
 n=max(4,round(w/.11))
 for k in range(n+1):facade_box(m,x,y,u-w/2-.05+k*(w+.10)/n,.45,z+.48,.02,.02,.94,M['Iron'],a)
def grooves43(m,x,y,u0,u1,z0,z1,a,ma,holes,step=.42):
 # Banded render: horizontal grooves (thin raised courses), interrupted by the openings.
 z=z0+step
 while z<z1-.05:
  at=u0
  for l,r in sorted((u-w/2-.05,u+w/2+.05) for u,b,w,h,rr in holes if b-.05<z<b+h+.05)+[(u1,u1)]:
   l=max(u0,min(u1,l));r=max(u0,min(u1,r))
   if l>at+.05:facade_box(m,x,y,(at+l)/2,.37,z,l-at,.03,.05,ma,a)
   at=max(at,r)
  z+=step
def cornice43(m,x,y,u0,u1,a,H,ma,out=.55):
 L=u1-u0;c=(u0+u1)/2
 facade_box(m,x,y,c,.40,H-.55,L,.10,.20,ma,a);facade_box(m,x,y,c,.48,H-.32,L,.26,.26,ma,a)
 facade_box(m,x,y,c,.36+out/2,H-.08,L,out,.18,ma,a)
def terrace43(m,x,y,u0,u1,a,H):
 # The roof terrace's railing, set back a little behind the cornice.
 L=u1-u0;c=(u0+u1)/2
 for zz in (H+.70,H+.35):town_rod(m,lp(x,y,u0,-.30,zz,a),lp(x,y,u1,-.30,zz,a),.018,M['Iron'],6)
 for k in range(max(1,round(L/1.6))+1):uu=u0+k*L/max(1,round(L/1.6));town_rod(m,lp(x,y,uu,-.30,H,a),lp(x,y,uu,-.30,H+.72,a),.02,M['Iron'],6)
def gablefront43(m,zone,H,apex,body,trim,roof,base=True):
 # A front gable on the street wall with a ridge roof running back to the courtyard side.
 P=Z[zone]['polygons'][0];xs=[p[0] for p in P];x0,x1=min(xs),max(xs)
 f0,f1=(x0,yf(x0)),(x1,yf(x1));b0,b1=(x0,max(p[1] for p in P if abs(p[0]-x0)<.3)),(x1,max(p[1] for p in P if abs(p[0]-x1)<.3))
 mid=lambda p,q:((p[0]+q[0])/2,(p[1]+q[1])/2)
 fm,bm=mid(f0,f1),mid(b0,b1);ov=.30
 def out(p,d):return (p[0],p[1]-d)
 for s0,s1 in ((f0,b0),(f1,b1)):
  vs=[(*out(fm,ov+.355),apex),(s0[0],s0[1]-ov-.355,H-.05),(s1[0],s1[1],H-.05),(*bm,apex)]
  m.faces(vs,[(0,1,2,3) if s0==f0 else (3,2,1,0)],roof)
 for (p,q),sgn in (((f0,f1),1),((b0,b1),-1)):
  sh=.355 if sgn>0 else 0.0
  tri=[(p[0],p[1]-sh,H),(q[0],q[1]-sh,H),((p[0]+q[0])/2,(p[1]+q[1])/2-sh,apex-.05)]
  m.faces(tri,[(0,1,2) if sgn>0 else (2,1,0)],body)
 x,y,L,a=sf_edge(f0,f1)
 for (u0,z0),(u1,z1) in (((-L/2,H),(0,apex)),((0,apex),(L/2,H))):town_rod(m,lp(x,y,u0,.45,z0,a),lp(x,y,u1,.45,z1,a),.10,trim,8)
 if base:facade_box(m,x,y,0,.48,H+.02,L,.24,.14,trim,a)
 return x,y,L,a

m=b43_new('SM_Building_91846978','Kvarnholmen/Södra Långgatan north')
UP1,UP2,UP3=(4.03,5.36),(6.68,8.04),(9.38,10.68)
for zone in Z:
 HZ=Z[zone]['height']
 wall={'s1a':M['Cream'],'s1b':M['Cream'],'s1c':M['Cream'],'s2':M['Cream'],'s3':M['Blue'],'s4':M['Grey'],'s5g':M['Sand'],'s5':M['Sand']}.get(zone,M['Beige'])
 for w in walls(zone):
  x,y,L,a=sf_edge(w['p'],w['q'])
  if not street43(w):
   if w['kind']=='outer':plain(m,w,HZ,wall,FW,M['White'],2,1.0)
   else:bz_wall(m,w['p'],w['q'],w['z0'],HZ,[],wall)
   continue
  S=lambda X:U(w,X,yf(X));u0,u1=-L/2,L/2
  if zone in ('s1a','s1b','s1c','s2'):
   ups=[];gfs=[];extra=[]
   if zone=='s1a':
    for x0,x1 in ((101.25,102.10),(102.77,103.62)):ups+=[(S((x0+x1)/2),b,x1-x0-.12,t-b,0) for b,t in (UP1,UP2)]
    gfs=[(S(102.42),.14,2.54,2.18,0)]
   elif zone=='s1b':
    for x0,x1 in ((104.68,106.04),(107.35,108.25),(109.33,110.20),(111.51,112.88)):
     ww=x1-x0-.12;ups+=[(S((x0+x1)/2),b,ww,t-b,0) for b,t in (UP1,UP2,UP3)]
    gfs=[(S(108.74),0,3.97,2.51,0)]
   elif zone=='s1c':
    for x0,x1 in ((113.96,114.85),(115.53,116.42),(118.42,119.34),(120.03,120.95),(121.64,122.50)):ups+=[(S((x0+x1)/2),b,x1-x0-.12,t-b,0) for b,t in (UP1,UP2)]
    for x0,x1 in ((111.59,112.97),(114.48,115.86),(118.16,119.56),(120.56,121.99)):
     if S(x0)>u0:gfs.append((S((x0+x1)/2),.94,x1-x0-.14,1.44,0))
   else:
    for x0,x1 in ((124.55,125.75),(126.92,128.13),(128.53,129.77),(131.47,132.63),(133.83,135.00),(135.41,136.62)):ups+=[(S((x0+x1)/2),b,x1-x0-.20,t-b,0) for b,t in (UP1,UP2)]
    for x0,x1 in ((124.43,125.84),(127.70,129.01),(131.46,132.73),(134.48,135.90)):gfs.append((S((x0+x1)/2),.61,x1-x0-.14,1.77,0))
   holes=ups+gfs
   bz_wall(m,w['p'],w['q'],0,HZ,holes,wall)
   GFM=M['Beige']
   grooves43(m,x,y,u0,u1,.30,2.98,a,GFM,holes)
   facade_box(m,x,y,0,.40,2.74,L,.08,.48,GFM,a);facade_box(m,x,y,0,.42,2.99,L,.10,.08,M['White'],a)
   facade_box(m,x,y,0,.39,.14,L,.08,.28,M['Stone'],a)
   for u,b,ww,hh,r in ups:
    surround36(m,x,y,u,b,ww,hh,a,M['White'],.10,.39);win43(m,x,y,u,b,ww,hh,a)
   if zone=='s1a':
    u,b,ww,hh,r=gfs[0];surround36(m,x,y,u,b,ww,hh,a,M['White'],.14,.39)
    facade_box(m,x,y,u,.22,b+hh/2,ww,.06,hh,M['Garage'],a)
    for k in range(1,12):facade_box(m,x,y,u,.26,b+k*hh/12,ww,.03,.02,M['Dark'],a)
   elif zone=='s1b':
    # The arcade: an open recess 1.9 m deep with the two doors at its back.
    u,b,ww,hh,r=gfs[0]
    for s in (-1,1):facade_box(m,x,y,u+s*(ww/2-.05),-.60,hh/2,.10,1.90,hh,GFM,a)
    facade_box(m,x,y,u,-.60,hh-.05,ww,1.90,.10,GFM,a)
    facade_box(m,x,y,u,-1.50,hh/2,ww,.10,hh,GFM,a)
    facade_box(m,x,y,u-1.05,-1.43,1.10,.80,.06,2.10,M['DoorGrey'],a)
    s21_glass(m,*lp(x,y,0,-1.75,0,a)[:2],u+.80,.05,.95,2.20,a,FW,1,.78,True)
    for X in (105.36,112.20):
     for b,t in (UP1,UP2,UP3):rail43(m,x,y,S(X),b,1.24,a)
   for u,b,ww,hh,r in gfs if zone in ('s1c','s2') else []:
    surround36(m,x,y,u,b,ww,hh,a,M['White'],.10,.39);win43(m,x,y,u,b,ww,hh,a,.75,.20,3)
   if zone=='s2':
    # The ochre roughcast panels in cream frames, between the storeys' window rows.
    for p0,p1 in ((123.97,126.14),(126.56,130.00),(130.75,132.98),(133.40,137.31)):
     pu=S((p0+p1)/2);pw=p1-p0;l0,l1=pu-pw/2,pu+pw/2
     for zz0,zz1 in ((3.55,3.93),(5.46,6.58),(8.14,8.45)):facade_box(m,x,y,pu,.37,(zz0+zz1)/2,pw,.03,zz1-zz0,M['Ochre'],a)
     for zb,zt in ((3.93,5.46),(6.58,8.14)):
      cuts=sorted((u-ww/2-.10,u+ww/2+.10) for u,b,ww,hh,r in ups if l0<u<l1 and zb<b+hh/2<zt);at=l0
      for c0,c1 in cuts+[(l1,l1)]:
       if c0>at+.03:facade_box(m,x,y,(at+c0)/2,.37,(zb+zt)/2,c0-at,.03,zt-zb,M['Ochre'],a)
       at=max(at,c1)
    # The quoin strip at the west end of the ochre range.
    k=0;zz=3.1
    while zz+.1<9.0:
     t=min(zz+.36,9.0);ww=.50 if k%2==0 else .36
     facade_box(m,x,y,S(123.40)+ww/2,.39,(zz+t)/2,ww,.06,t-zz,M['Stone'],a);zz+=.42;k+=1
   cornice43(m,x,y,u0,u1,a,HZ,M['White'])
   if zone!='s1b':terrace43(m,x,y,u0+.2,u1-.2,a,HZ)
   if zone=='s1a':
    # The mansard dormer at the west end.
    cx_,cy_,_=lp(x,y,S(102.45),-1.2,0,a);box(m,cx_,cy_,2.0,1.2,1.5,HZ,M['Roof'],a,M['Dark'])
    facade_box(m,x,y,S(102.45),-.58,HZ+.75,1.3,.04,.9,GLAZE,a)
  elif zone=='s3':
   holes=[]
   for X in (139.29,142.80):holes+=[(S(X),b,1.30,t-b,0) for b,t in ((4.14,5.49),(6.92,8.25),(9.64,11.12))]
   gw=(S(139.29),1.19,1.30,1.31,0);ent=(S(142.76),0,1.44,2.56,0)
   bz_wall(m,w['p'],w['q'],0,HZ,holes+[gw,ent],M['Blue'])
   for u,b,ww,hh,r in holes+[gw]:surround36(m,x,y,u,b,ww,hh,a,M['White'],.10,.39);win43(m,x,y,u,b,ww,hh,a)
   eu=ent[0]
   for s in (-1,1):facade_box(m,x,y,eu+s*.69,-.40,1.28,.06,1.50,2.56,M['Blue'],a)
   facade_box(m,x,y,eu,-.40,2.53,1.44,1.50,.06,M['Blue'],a);facade_box(m,x,y,eu,-1.10,1.28,1.44,.10,2.56,M['Blue'],a)
   s21_glass(m,*lp(x,y,0,-1.20,0,a)[:2],eu,.05,1.0,2.35,a,FW,1,.80,True)
   for p0,p1 in ((137.56,137.81),(140.41,141.00),(141.19,141.81),(144.27,144.48)):facade_box(m,x,y,S((p0+p1)/2),.40,(.6+HZ)/2,p1-p0,.09,HZ-.6,M['Cream'],a)
   for z0,z1 in ((3.33,3.42),(6.07,6.29),(8.95,9.10)):facade_box(m,x,y,0,.41,(z0+z1)/2,L,.10,z1-z0+.08,M['Cream'],a)
   facade_box(m,x,y,0,.39,.30,L,.08,.60,M['Stone'],a)
   for X in (139.29,142.80):
    k_=20;town_path(m,[lp(x,y,S(X)+.32*math.cos(math.tau*t/k_),.40,8.55+.24*math.sin(math.tau*t/k_),a) for t in range(k_+1)],.03,M['White'])
   cornice43(m,x,y,u0,u1,a,HZ,M['Cream'],.40)
   gx,gy,gL,ga=gablefront43(m,'s3',HZ,14.55,M['Blue'],M['Cream'],M['Roof'])
   k_=20;town_path(m,[lp(gx,gy,0+.28*math.cos(math.tau*t/k_),.42,13.1+.28*math.sin(math.tau*t/k_),ga) for t in range(k_+1)],.05,M['Cream'])
  elif zone=='s4':
   ups=[(S((x0+x1)/2),4.25,x1-x0-.10,1.36,0) for x0,x1 in ((145.60,146.54),(148.01,148.97),(149.65,150.60),(152.62,153.56),(155.04,155.97),(156.65,157.60))]
   gfs=[(S((x0+x1)/2),.65,x1-x0-.12,1.88,0) for x0,x1 in ((145.35,146.80),(148.65,150.02),(152.43,153.85),(155.61,157.05))]
   bz_wall(m,w['p'],w['q'],0,HZ,ups+gfs,M['Grey'])
   for u,b,ww,hh,r in ups:win43(m,x,y,u,b,ww,hh,a,.72,.30)
   for u,b,ww,hh,r in gfs:win43(m,x,y,u,b,ww,hh,a,.78,.30,0);facade_box(m,x,y,u,.33,b+hh/2,.14,.06,hh,FW,a)
   sp,sq=lp(x,y,S(153.10)-.575,0,0,a)[:2],lp(x,y,S(153.10)+.575,0,0,a)[:2]
   bz_wall(m,sp,sq,3.49,HZ-.4,[(uu-S(153.10),b,ww,hh,r) for uu,b,ww,hh,r in ups if abs(uu-S(153.10))<.6],M['Cream'],.355,.385)
   facade_box(m,x,y,0,.40,3.465,L,.08,.06,M['Cream'],a)
   facade_box(m,x,y,0,.39,.30,L,.08,.60,M['White'],a)
   cornice43(m,x,y,u0,u1,a,HZ,M['White'],.50)
  elif zone in ('s5g','s5'):
   if zone=='s5g':
    ups=[(S((x0+x1)/2),4.27,x1-x0-.12,1.33,0) for x0,x1 in ((159.72,161.17),(163.11,164.51))]
    gfs=[(S(160.45),1.10,1.31,1.31,0)]
    gab=[(S((x0+x1)/2),7.04,x1-x0-.12,1.12,0) for x0,x1 in ((159.89,161.39),(163.20,164.56))]
   else:
    ups=[(S((x0+x1)/2),4.27,x1-x0-.12,1.33,0) for x0,x1 in ((166.65,168.05),(170.50,171.90))]+[(S(174.01),3.20,.81,2.40,0)]
    gfs=[(S(171.92),1.10,1.23,1.31,0),(S(174.03),.93,.80,2.06,0)];gab=[]
    ent=(S(166.48),0,1.18,2.60,0)
   holes=ups+gfs+gab+([ent] if zone=='s5' else [])
   bz_wall(m,w['p'],w['q'],0,HZ if zone=='s5' else HZ,[h_ for h_ in holes if h_[1]+h_[3]<=HZ],M['Sand'])
   # The salmon ground floor and the cream band as coats over the wall, cut at the openings.
   coat=[h_ for h_ in holes if h_[1]<4.3]
   bz_wall(m,w['p'],w['q'],.85,3.47,coat,M['Salmon'],.355,.385)
   bz_wall(m,w['p'],w['q'],3.47,4.27,coat,M['Cream'],.355,.395)
   facade_box(m,x,y,0,.39,.425,L,.08,.85,M['White'],a)
   for u,b,ww,hh,r in ups+gfs+gab:
    if b+hh<=HZ or zone=='s5g':win43(m,x,y,u,b,ww,hh,a,.72 if hh<2 else .85)
   if zone=='s5':
    u,b,ww,hh,r=gfs[1];facade_box(m,x,y,u,.22,b+.55,ww,.06,1.1,M['Iron'],a)
    rail43(m,x,y,ups[2][0],4.27,.81,a)
    eu=ent[0]
    for s in (-1,1):facade_box(m,x,y,eu+s*.56,-.40,1.30,.06,1.50,2.60,M['Salmon'],a)
    facade_box(m,x,y,eu,-.40,2.57,1.18,1.50,.06,M['Salmon'],a)
    s21_glass(m,*lp(x,y,0,-1.10,0,a)[:2],eu,.05,.95,2.40,a,M['DoorGrey'],1,.80,True)
    facade_box(m,x,y,eu,-.35,.03,1.18,1.40,.06,M['Stone'],a)
   # The front gable rises from the wall face; the cornice turns up into its rakes, not across it.
   if zone!='s5g':cornice43(m,x,y,u0,u1,a,HZ,M['Cream'],.60)
   if zone=='s5g':
    gx,gy,gL,ga=gablefront43(m,'s5g',HZ-.05,10.4,M['Sand'],M['Cream'],M['Tile'],False)
    # The gable's windows and the roundel stand in the gable face above the eaves.
    for u,b,ww,hh,r in gab:win43(m,x,y,u,b,ww,hh,a,.72,.40)
    k_=20;town_path(m,[lp(x,y,S(162.10)+.20*math.cos(math.tau*t/k_),.42,7.70+.20*math.sin(math.tau*t/k_),a) for t in range(k_+1)],.04,M['Cream'])
for zone in ('s4','s5'):roof34(m,zone,M['Tile'],M['Grey'] if zone=='s4' else M['Sand'])
for zone in ('s1a','s1c','s2'):flatcap(m,zone,M['Roof'],.15)
gablefront43(m,'s1b',11.9,13.9,M['Cream'],M['White'],M['Roof'])
for w in walls('s1b'):
 if street43(w):
  x,y,L,a=sf_edge(w['p'],w['q'])
  k_=20;town_path(m,[lp(x,y,.25*math.cos(math.tau*t/k_),.42,12.9+.25*math.sin(math.tau*t/k_),a) for t in range(k_+1)],.04,M['White'])
for w in walls('bk'):
 if w['kind']=='outer':plain(m,w,Z['bk']['height'],M['Beige'],FW,M['White'],2,1.0)
 else:bz_wall(m,w['p'],w['q'],w['z0'],Z['bk']['height'],[],M['Beige'])
for g in Z['bk']['polygons']:
 pts=simplify([tuple(v) for v in g],.8)
 inset_roof(m,pts,Z['bk']['height'],2.2,2.3,M['Tile'],.35)
# The roof windows in the grey house's and the salmon range's tile roofs.
for X,d_ in ((150.0,1.5),(154.8,1.5),(157.0,1.5),(168.0,1.5),(172.5,1.5)):
 cx_,cy_=X,yf(X)+.355+d_+.6;zz=Z['s4']['height']+(d_+.6)*(Z['s4']['top']-Z['s4']['height'])/3.0
 box(m,cx_,cy_,1.2,.9,.10,zz-.05,M['Dark'],0)
b43_finish(m,'91846978')

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
# Chained camera positions (distance from the real facade, 0.355 m added for the model's wall face).
_C={'105':(104.34,4.81),'125':(124.58,4.55),'135':(134.58,4.48),'145':(145.07,4.51),'155':(155.54,4.30),'165':(165.56,4.14)}
def _cam(n):X,D_=_C[n];return X,yf(X)-.355-D_,2.41
block43_cameras=[
 sv_camera('257_Block43_Cal_Hotel',*_cam('105'),332,0,90),
 sv_camera('258_Block43_Cal_Hotel_Up',*_cam('105'),332,25,90),
 sv_camera('259_Block43_Cal_Ochre',*_cam('125'),332,0,90),
 sv_camera('260_Block43_Cal_Ochre_Up',*_cam('125'),332,25,90),
 sv_camera('261_Block43_Cal_Blue_Up',*_cam('135'),332,25,90),
 sv_camera('262_Block43_Cal_Blue',*_cam('145'),332,0,90),
 sv_camera('263_Block43_Cal_Grey',*_cam('155'),332,0,90),
 sv_camera('264_Block43_Cal_Grey_Up',*_cam('155'),332,25,90),
 sv_camera('265_Block43_Cal_Salmon',*_cam('165'),332,0,90),
 sv_camera('266_Block43_Cal_Salmon_Up',*_cam('165'),332,25,90),
 ('267_Block43_Aerial',(138.0,-105.0,34.0),(138.0,-66.0,5.0),28),
]
print('BLOCK43_GEOMETRY',len(block43_names))
