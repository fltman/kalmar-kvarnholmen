"""Individual mill volumes and bathhouse, using reviewed 2023/2024 photographs."""
def mill18_face(m,x,y,L,H,a,bays,floors,profile='regular'):
 step=L/bays;us=[-L/2+(i+.5)*step for i in range(bays)];base=7.5;dh=(H-base-1.4)/(floors-2);holes=[]
 for i,u in enumerate(us):
  for k in range(floors):
   b=[.35,4.15][k] if k<2 else base+.30+(k-2)*dh
   h=2.65 if k==0 else 1.65 if k==1 else max(1.45,min(2.55,dh-.95));rad=.50 if k==0 else .28
   triple=profile=='risk' and i==bays//2 and k>=2
   pair=(profile=='silo' and k==floors-1) or (profile=='old' and k>=floors-2)
   if triple:
    holes += [(u+off,b,.61,h,.22) for off in [-.85,0,.85]]
   elif pair:holes += [(u+off,b,.88,h,.4) for off in [-.57,.57]]
   else:holes.append((u,b,min(1.75,step*.55),h,rad))
 start=len(m.f);p18_face(m,x,y,L,H,holes+[(0,base,0,.001,0)],P18['BrickRed'],a)
 if P18['BathCream'] not in m.mats:m.mats.append(P18['BathCream'])
 for fi in range(start,len(m.f)):
  if max(m.v[j][2] for j in m.f[fi])<=base+.005:m.mi[fi]=m.mats.index(P18['BathCream'])
 # Buff brick infill between red pilasters, cut around each opening.
 for u in us:
  w=step-.70;local=[(hu-u,b,ww,hh,r) for hu,b,ww,hh,r in holes if abs(hu-u)<step*.48];xx,yy,_=lp(x,y,u,.018,0,a)
  p18_face(m,xx,yy,w,H-.9,[(0,0,w,base+.05,0)]+local,P18['BrickBuff'],a)
  for sign in [-1,1]:facade_box(m,x,y,u+sign*(step-.36)/2,.39,(base+H)/2,.32,.25,H-base,P18['BrickRed'],a)
 for u,b,w,h,r in holes:p18_win(m,x,y,u,b,w,h,r,a,trim=P18['BathCream'] if b<base else P18['BrickRed'],rows=4 if h>2 else 3,cols=4 if w>1.3 else 2)
 for z in [base-.12,H-.72,H-.20]:p18_band(m,x,y,L,z,a,P18['BrickRed'])
 for k in range(round(L/.38)):
  facade_box(m,x,y,-L/2+(k+.5)*L/round(L/.38),.40,H-.98,.17,.32,.32,P18['BrickRed'],a)
 for k in range(round(L/.88)):
  facade_box(m,x,y,-L/2+(k+.5)*L/round(L/.88),.27,H+.20,.41,.60,.64,P18['BrickRed'],a)
 p18_rustic(m,x,y,L,base-.1,holes,a,P18['Ashlar'])
 facade_box(m,x,y,0,.38,.14,L,.24,.28,P18['Ashlar'],a)
 for u in [-L/2+.12,L/2-.12]:sf_pipe(m,x,y,u,H,a,TC)
 return holes
# Main Ångkvarnen: lower museum wing, high silo, older gabled western wing.
for bid,H,floors in [('91285823',24.3,6),('91285828',33.2,8),('91285833',23.6,6)]:
 m=p18_new('SM_Kvarnholmen_House_'+bid);b=D18['buildings'][bid];poly=b['polygons'][0]['outer']
 if bid=='91285828':poly=[(233.32,-144.2),(258.78,-144.2),(258.83,-98.79),(233.38,-98.76)]
 for x,y,L,a in l14_edges(poly):
  if L<2:continue
  front=y< -142;N=5 if front and bid=='91285828' else 7 if front and bid=='91285833' else 9 if front else max(2,round(L/4.4))
  mill18_face(m,x,y,L,H,a,N,floors,'silo' if bid=='91285828' else 'old' if bid=='91285823' else 'regular')
 m.faces([(x,y,H-.35) for x,y in poly],[tuple(range(len(poly)))],METAL)
 if bid=='91285828':
  for x in [233.6,258.4]:
   for y in [-143.9,-99.1]:
    m.box((x,y,H+.5),(.72,.72,1.5),P18['BrickRed']);m.lathe(x,y,H+1.3,[(.12,0),(.26,.25),(.12,.53),(.02,1.05)],TC,12)
  # Glass gallery: raised slab, narrow mullions, opaque low parapet and clear columns.
  m.box((246.04,-151.9,4.0),(25.5,15.4,.32),P18['Ashlar']);m.box((246.04,-151.9,8.9),(25.7,15.6,.25),TC)
  for x,y,L,a in [(246.04,-159.82,25.5,0),(258.82,-152,15.5,math.pi/2),(233.28,-152,15.5,-math.pi/2)]:
   facade_box(m,x,y,0,0,6.15,L,.09,3.7,GLAZE,a);facade_box(m,x,y,0,.10,4.55,L,.13,.65,P18['Ashlar'],a)
   for k in range(round(L/1.1)+1):facade_box(m,x,y,-L/2+k*L/round(L/1.1),.14,6.65,.055,.15,4.45,TW,a)
   for k in range(round(L/5)+1):facade_box(m,x,y,-L/2+k*L/round(L/5),.1,4.4,.28,.46,8.8,P18['BrickRed'],a)
   for z in [4.0,4.85,7.85,8.8]:facade_box(m,x,y,0,.20,z,L,.18,.09,TW,a)
  town_text(m,246,-160.12,3.55,0,'KALMARSALEN',5.8,TI)
 elif bid=='91285833':
  town_text(m,284,-144.7,5.4,0,'KALMAR LÄNS MUSEUM',9.5,P18['BrickRed']);m.box((264.4,-145.1,3.6),(4.3,1.5,.12),TC)
 elif bid=='91285823':
  # Correct the formerly over-tall 59 m tower; dimensions still inferred from the silhouette.
  tx,ty=192.8,-91.0;m.box((tx,ty,31.2),(8.4,10.0,23.0),P18['BrickRed'])
  for aa,LL,dd in [(0,8.4,5),(math.pi/2,10,4.2),(math.pi,8.4,5),(-math.pi/2,10,4.2)]:
   fx,fy,_=lp(tx,ty,0,dd,0,aa)
   for uu in [-LL*.23,LL*.23]:
    facade_box(m,fx,fy,uu,.04,32.1,LL*.32,.08,18,P18['BrickBuff'],aa);p18_win(m,fx,fy,uu,36.6,1.1,2.4,.45,aa)
   for z in [40.9,42.7]:p18_band(m,fx,fy,LL+.3,z,aa,P18['BrickRed'])
   for k in range(round(LL/.9)):facade_box(m,fx,fy,-LL/2+(k+.5)*LL/round(LL/.9),.22,43.12,.42,.50,.68,TI,aa)
  l14_gable(m,186.25,-134.5,19.2,47.0,24.3,4.1,P18['BrickRed'],TC,-math.pi/2)
  # Pale classical office at west, separate from the industrial upper gable.
  gx,gy,LL,aa=186.13,-134.0,20.0,-math.pi/2;hs=[(u,z,1.3,1.9,.4 if z<2 else 0) for u in [-7.5,-3.75,0,3.75,7.5] for z in [.7,4.5,7.6]]
  p18_face(m,gx,gy,LL,10.3,hs,TL,aa)
  for h in hs:p18_win(m,gx,gy,*h,aa,frame=TW,trim=TL)
  for z in [3.75,7,10.3]:p18_band(m,gx,gy,LL,z,aa,TL)
 p18_finish(m)
# Riskvarnen: distinct eight-storey sea front and lower five-storey rear wings.
m=p18_new('SM_Kvarnholmen_House_91846944');b=D18['buildings']['91846944'];x0,y0,x1,y1=b['bounds'];cut=y0+17.4;H=31.0;low=18.9
for x,y,L,a in l14_edges([(x0,y0),(x1,y0),(x1,cut),(x0,cut)]):
 mill18_face(m,x,y,L,H,a,13 if abs(math.sin(a))<.5 else 5,8,'risk' if y<y0+1 else 'regular')
m.box(((x0+x1)/2,(y0+cut)/2,H-.35),(x1-x0,cut-y0,.2),METAL)
for x,y,L,a in l14_edges([(x0,cut),(x1,cut),(x1,y1),(x0,y1)]):
 if abs(y-cut)<.2:continue
 mill18_face(m,x,y,L,low,a,max(3,round(L/4.2)),5)
m.box(((x0+x1)/2,(cut+y1)/2,low-.32),(x1-x0,y1-cut,.2),METAL)
xc=(x0+x1)/2
for tx in [x0+1.5,xc,x1-1.5]:
 # Turret/riser strip above the crown, linked to the pilasters underneath.
 facade_box(m,tx,y0,0,.20,H+.83,3.05,.80,2.55,P18['BrickRed'],0)
 p18_band(m,tx,y0,3.55,H+2.05,0,P18['BrickRed'])
 for q in [-1.45,1.45]:
  facade_box(m,tx,y0,q,.22,H+2.40,.55,.65,.9,P18['BrickRed'],0)
  m.lathe(tx+q,y0-.22,H+2.9,[(.09,0),(.21,.20),(.11,.42),(.015,.95)],TC,12)
# Central portal and pierced balcony from the observed south facade.
p18_win(m,xc,y0,0,.22,2.2,3.0,.65,0,trim=P18['BathCream']);m.box((xc,y0-.86,4.22),(4.0,1.55,.25),P18['BathCream'])
for xx in [xc-1.65,xc+1.65]:
 sf_beam(m,(xx,y0-.3,3.1),(xx,y0-1.5,4.15),.25,.25,P18['Ashlar'],0)
for xx in [xc-1.85,xc+1.85]:m.box((xx,y0-.85,4.8),(.22,1.45,1.1),P18['BathCream'])
for q in [-1.7,-1.1,-.55,0,.55,1.1,1.7]:facade_box(m,xc,y0,q,1.55,4.83,.20,.22,.84,P18['BathCream'],0)
facade_box(m,xc,y0,0,1.55,5.33,4.05,.34,.16,P18['BathCream'],0)
p18_finish(m)
exec(compile((R/'scripts/bathhouse19_helpers.py').read_text(),'bathhouse19_helpers.py','exec'))
# Varmbadhuset: pale render, three west gables, paired windows and a recessed iron-gated portal.
m=p18_new('SM_Kvarnholmen_House_91846928');b=D18['buildings']['91846928'];H=10.9;CR18=P18['BathCream'];JOIN=P18['GreenJoinery'];AS18='M_Portal19_Stone'
for x,y,L,a in l14_edges(b['polygons'][0]['outer']):
 if L<5:p18_face(m,x,y,L,H,[],CR18,a);continue
 west=x<396;south=y< -95;N=5 if south else max(3,round(L/2.8));us=[-L/2+(k+.5)*L/N for k in range(N)];holes=[]
 for u in us:
  holes.extend([(u,.45,.76,.97,.13),(u,3.48,.94,1.50,.20)])
  if south:
   for off in [-.65,0,.65]:holes.append((u+off,8.25,.46,1.17,.23))
  else:holes.append((u,8.32,.77,1.13,.12))
 if west:
  portal=-L*.08;oriel=L*.19
  holes=[h for h in holes if not (abs(h[0]-portal)<1.5 and h[1]<5.3) and not(abs(h[0]-oriel)<1.3 and 3<h[1]<6)]
  holes.append((portal,.08,2.25,3.10,.75))
  for gu,gw in [(-L*.34,3.45),(0,4.15),(L*.34,4.8)]:
   holes=[h for h in holes if not(h[1]>8 and abs(h[0]-gu)<1.5)]
   holes.append((gu,8.20,1.90 if gw>4 else 1.1,2.0 if gw>4 else 2.3,.72 if gw>4 else .30))
 p18_face(m,x,y,L,H,holes,CR18,a)
 for u,bb,w,hh,r in holes:
  if west and abs(u-portal)<.01 and bb<.1:continue
  b19_win(m,x,y,u,bb,w,hh,r,a,frame=JOIN,trim=CR18,rows=4,cols=3 if w>.7 else 2)
 for z in [1.66,3.18,5.23,7.91]:
  gap=1.58 if z<4 else .80
  spans=[(-L/2,portal-gap),(portal+gap,L/2)] if west and z<7 else [(-L/2,L/2)]
  for lo,hi in spans:
   bx,by,_=lp(x,y,(lo+hi)/2,0,0,a);p18_band(m,bx,by,hi-lo,z,a,AS18,.20)
 spans=[(-L/2,portal-1.50),(portal+1.50,L/2)] if west else [(-L/2,L/2)]
 for lo,hi in spans:facade_box(m,x,y,(lo+hi)/2,.37,.25,hi-lo,.14,.50,AS18,a)
 p18_band(m,x,y,L+.18,H,a,CR18,.4)
 town_rod(m,lp(x,y,-L/2,.53,H+.04,a),lp(x,y,L/2,.53,H+.04,a),.07,TC,12)
 if south:
  for i in range(N+1):
   u=-L/2+i*L/N;facade_box(m,x,y,u,.40,6.7,.33,.26,8.5,CR18,a)
   for z in [2.0,5.5]:
    vs=[lp(x,y,u+du,o,zz,a) for du,o,zz in [(-.24,.25,z),(.24,.25,z),(.24,.85,z-.50),(-.24,.85,z-.50),(-.24,.25,z-.6),(.24,.25,z-.6)]];m.faces(vs,[(0,1,2,3),(3,2,5,4),(0,4,5,1)],AS18)
 if west:
  px,py,_=lp(x,y,portal,0,0,a)
  # Inner dark vestibule is behind the metal gate; no window fitted in the doorway.
  facade_box(m,px,py,0,-.65,1.8,2.25,.07,3.5,IRON,a)
  for q in [-1.30,1.30]:facade_box(m,px,py,q,.44,1.85,.42,.60,3.7,AS18,a)
  p18_arch(m,px,py,3.18,2.27,.76,.39,.42,a,AS18)
  for q in [-1.0+i*.20 for i in range(11)]:facade_box(m,px,py,q,.12,1.70,.027,.03,3.0+.18*(1-abs(q)),JOIN,a)
  for z in [.23,1.40,2.7]:facade_box(m,px,py,0,.12,z,2.1,.05,.04,JOIN,a)
  for sign in [-1,1]:sf_beam(m,lp(px,py,sign*1.0,.12,.4,a),lp(px,py,-sign*1.0,.12,2.7,a),.032,.032,JOIN,a)
  for i in range(3):facade_box(m,px,py,0,.64+i*.2,.075*(3-i),2.5,.9,.15*(3-i),AS18,a)
  p18_band(m,px,py,3.5,4.48,a,AS18,.68)
  facade_box(m,px,py,0,.60,4.21,3.22,.30,.30,AS18,a)
  town_text(m,*lp(px,py,0,.77,0,a)[:2],4.20,a,'BADHUS',1.85,'M_Portal19_Engraving')
  # Carved niche, pilasters and draped figure; explicit stylised relief, not scanned artwork.
  for q in [-.56,.56]:facade_box(m,px,py,q,.42,5.70,.20,.32,2.15,AS18,a)
  p18_arch(m,px,py,6.68,1.12,.55,.14,.43,a,AS18)
  facade_box(m,px,py,0,.26,5.8,.98,.1,1.85,TS,a)
  facade_box(m,px,py,0,.45,4.74,.77,.45,.24,AS18,a)
  fx,fy,_=lp(px,py,0,.52,0,a);m.lathe(fx,fy,4.85,[(.28,0),(.19,.65),(.22,1.2),(.15,1.50),(.09,1.63)],AS18,16);m.lathe(fx,fy,6.50,[(.09,0),(.17,.15),(.11,.30),(.06,.36)],AS18,16)
  for sign in [-1,1]:
   town_path(m,[lp(px,py,sign*.19,.53,6.27,a),lp(px,py,sign*.29,.64,6.0,a),lp(px,py,0,.69,6.15,a)],.075,AS18)
   town_scroll(m,*lp(px,py,sign*.95,.44,0,a)[:2],4.94,a,sign,.70,.09,AS18)
  ox,oy,_=lp(x,y,oriel,.02,0,a)
  facade_box(m,ox,oy,0,.65,4.18,2.0,1.3,2.50,CR18,a)
  for q in [-.48,.48]:b19_win(m,*lp(ox,oy,0,1.33,0,a)[:2],q,3.55,.70,1.69,0,a,frame=JOIN,trim=CR18,rows=4,cols=2)
  l14_hip(m,*lp(ox,oy,0,.72,0,a)[:2],2.3,1.6,5.45,.85,TC,a)
  # Supported taper below the oriel.
  town_polyprofile(m,ox,oy,2.50,[(-.25,0),(.25,0),(.9,.64),(.9,.9),(-.9,.9),(-.9,.64)],a,CR18,1.0,False)
  # Gable faces split around arched upper windows, and mouldings on the face.
  for gu,gw,gr in [(-L*.34,3.45,2.2),(0,4.15,2.9),(L*.34,4.8,3.35)]:
   gx,gy,_=lp(x,y,gu,0,0,a);base=H-.75;wb=8.20;ww=1.90 if gw>4 else 1.1;wh=2.0 if gw>4 else 2.3;wr=.72 if gw>4 else .30
   b19_gable(m,gx,gy,gw,gr,base,wb,ww,wh,wr,a,CR18,AS18)
   # Joinery already exists in the facade aperture above; do not duplicate it.
 for q in [-L/2+.12,L/2-.12]:sf_pipe(m,x,y,q,H,a,TW)
# Continuous pitched roof volumes at the two mapped widths.
l14_hip(m,405.3,-85.25,20.1,22.5,H,4.1,TT);l14_hip(m,400.75,-68.65,10.8,12.9,H,2.8,TT)
for tx,ty in [(397.1,-94.5),(413.4,-94.0)]:
 m.box((tx,ty,10.45),(3.15,3.15,2.3),CR18)
 for aa in [0,math.pi/2,math.pi,3*math.pi/2]:
  xx,yy,_=lp(tx,ty,0,1.59,0,aa);b19_win(m,xx,yy,0,10.0,.86,1.03,.40,aa,frame=JOIN,trim=CR18,rows=3,cols=3)
 # Curved copper cap rather than a straight pyramid.
 town_square_loft(m,tx,ty,11.65,[(1.80,0),(1.71,.12),(1.39,.36),(1.02,.79),(.59,1.43),(.27,2.05),(.09,2.52),(.04,2.70)],TC)
 m.lathe(tx,ty,14.35,[(.07,0),(.16,.12),(.07,.28),(.01,.45)],TC,12)
l14_lantern(m,400.6,-69.1,13.2,.67,1.65)
for yy in [-88,-74]:
 l14_hip(m,398.7,yy,1.5,1.0,12.20,.45,TC,math.pi/2);b19_win(m,398.2,yy,0,11.70,.70,.57,.18,-math.pi/2,frame=JOIN,trim=TC,rows=1,cols=2)
p18_finish(m)
