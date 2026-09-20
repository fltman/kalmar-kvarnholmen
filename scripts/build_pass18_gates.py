"""Reference-specific city gates; all passages stay physically open."""
AS18=P18['Ashlar'];BR18=P18['BrickRed'];RS='M_Landmark_Rubble'
def gatevault(m,g,W,S,AR,H):
 x,y,a,L,D=g['x'],g['y'],g['a'],g['width'],g['depth']
 for sign in [-1,1]:facade_box(m,x,y,sign*(L+W)/4,0,H/2,(L-W)/2,D,H,RS,a)
 for k in range(48):
  ts=[k*math.pi/48,(k+1)*math.pi/48];u0,u1=[W/2*math.cos(t) for t in ts];z0,z1=[S+AR*math.sin(t) for t in ts]
  vs=[lp(x,y,u,o,z,a) for o in [-D/2,D/2] for u,z in [(u0,z0),(u1,z1),(u1,H),(u0,H)]];m.faces(vs,[(0,1,2,3),(7,6,5,4),(0,4,5,1),(3,2,6,7)],RS)
 for side in [-1,1]:
  aa=a if side==1 else a+math.pi;fx,fy,_=lp(x,y,0,side*D/2,0,a)
  p18_arch(m,fx,fy,S,W,AR,.30,.15,aa,AS18)
  for q in [-W/2-.15,W/2+.15]:facade_box(m,fx,fy,q,.15,S/2,.30,.30,S,AS18,aa)
 return x,y,a,L,D
for g in D18['gates']:
 m=p18_new('SM_Kvarnholmen_Port_'+g['name'],'Kvarnholmen/Fortifications');x,y,a,L,D=g['x'],g['y'],g['a'],g['width'],g['depth']
 if g['name']=='Jordbroporten':
  # The 1931 gate is square-headed, with two main passages and two small lateral passages.
  H=6.25;holes=[(-2.10,0,3.30,4.72),(2.10,0,3.30,4.72),(-6.0,0,1.30,2.30),(6.0,0,1.30,2.30)]
  bounds=sorted(set([-L/2,L/2]+[u+q*w/2 for u,b,w,h in holes for q in [-1,1]]))
  for lo,hi in zip(bounds,bounds[1:]):
   mid=(lo+hi)/2;h=max([hh for u,b,w,hh in holes if abs(mid-u)<w/2]+[0]);facade_box(m,x,y,mid,0,(h+H)/2,hi-lo,D,H-h,AS18,a)
  for side in [-1,1]:
   aa=a if side==1 else a+math.pi;fx,fy,_=lp(x,y,0,side*D/2,0,a)
   p18_band(m,fx,fy,L+.25,H,aa,AS18,.40)
   p18_rustic(m,fx,fy,L,H,[(u,b,w,h,0) for u,b,w,h in holes],aa,TI)
   for u in [-6.0,6.0]:
    # Circular medallion/recess with a shallow stone annulus.
    town_path(m,[lp(fx,fy,u+.47*math.cos(k*math.tau/48),.22,4.82+.47*math.sin(k*math.tau/48),aa) for k in range(49)],.027,AS18)
   town_text(m,*lp(fx,fy,0,.27,0,aa)[:2],3.65,aa,'1931',.66,AS18)
   town_text(m,*lp(fx,fy,0,.28,0,aa)[:2],4.17,aa,'GV',.50,AS18)
  m.box((x,y,H+.03),(L,D,.12),AS18,a)
 elif g['name']=='Kavaljersporten':
  W,S,AR,H=3.9,3.05,1.60,5.15;gatevault(m,g,W,S,AR,H)
  fx,fy,_=lp(x,y,0,D/2,0,a)
  for sign in [-1,1]:
   u=sign*(W/2+.57);facade_box(m,fx,fy,u,.22,2.53,.78,.65,5.05,AS18,a)
   for z,w,h in [(.20,1.08,.35),(.47,.91,.12),(4.85,1.12,.26),(5.10,1.25,.16)]:facade_box(m,fx,fy,u,.36,z,w,.81,h,AS18,a)
   town_scroll(m,*lp(fx,fy,sign*(W/2+1.6),.28,0,a)[:2],5.45,a,sign,.92,.12,AS18)
  facade_box(m,fx,fy,0,.30,5.91,W+2.1,.85,1.42,AS18,a)
  for z in [5.24,5.46,6.47,6.69]:p18_band(m,fx,fy,W+2.6,z,a,AS18,.85)
  for u in [-2.35,-1.4,1.4,2.35]:
   for d in [-.12,0,.12]:facade_box(m,fx,fy,u+d,.77,5.92,.05,.13,.78,AS18,a)
   facade_box(m,fx,fy,u,.74,6.50,.42,.44,.30,AS18,a)
  # Supported carved crest, crown and acanthus around the XI monogram.
  town_polyprofile(m,*lp(fx,fy,0,.81,0,a)[:2],5.49,[(-.39,.86),(.39,.86),(.31,.21),(0,0),(-.31,.21)],a,AS18,.10,False)
  town_text(m,*lp(fx,fy,0,.93,0,a)[:2],5.87,a,'XI',.35,AS18)
  for sign in [-1,1]:
   for j in range(6):town_path(m,[lp(fx,fy,sign*(.28+t*.7),.86,5.56+j*.11+math.sin(t*math.pi)*.18,a) for t in [k/12 for k in range(13)]],.036,AS18)
  facade_box(m,x,y,0,0,H+.03,L,D,.1,P18['Grass'],a)
 else:
  W,S,AR,H=3.65,2.62,1.82,8.6;gatevault(m,g,W,S,AR,H)
  # Dressed harbour facade, a distinct plain masonry city facade.
  aa=a+math.pi;fx,fy,_=lp(x,y,0,-D/2,0,a)
  hs=[(0,0,W,S,AR),(-1.4,6.23,1.0,.85,.22),(1.4,6.23,1.0,.85,.22)]
  p18_face(m,fx,fy,L,H,hs,AS18,aa)
  for u,b,w,h,r in hs[1:]:p18_win(m,fx,fy,u,b,w,h,r,aa,frame=IRON,trim=AS18,rows=1,cols=1)
  p18_arch(m,fx,fy,S,W,AR,.28,.39,aa,AS18)
  for z in [4.85,5.90,8.30,8.60]:p18_band(m,fx,fy,L+.25,z,aa,AS18,.4)
  facade_box(m,fx,fy,0,.40,5.34,2.45,.15,.63,TS,aa)
  for q in [-L*.42,-2.6,2.6,L*.42]:
   for z in [1.30,3.7,5.32]:facade_box(m,fx,fy,q,.40,z,.11,.06,.13,IRON,aa)
  town_polyprofile(m,fx,fy,H,[(-2.2,0),(2.2,0),(2.2,.22),(.8,.22),(.8,.56),(-.8,.56),(-.8,.22),(-2.2,.22)],aa,AS18,.42,False)
  # Inner gate has brick upper courses, rough stone below, no copied ornate exterior.
  ix,iy,_=lp(x,y,0,D/2+.02,0,a);p18_face(m,ix,iy,L,H,[(0,0,W,S,AR)],BR18,a)
  for sign in [-1,1]:facade_box(m,ix,iy,sign*(L+W)/4,.2,2.1,(L-W)/2,.40,4.2,RS,a)
  p18_arch(m,ix,iy,S,W,AR,.24,.42,a,AS18)
  # Bridge keeps the existing footprint, now with piles and diagonal supports.
  bridge='M_Polish_BridgeWood'
  for k in range(94):facade_box(m,x,y,0,-D/2-(k+.5)*30/94,.095,3.35,30/94-.015,.07,bridge,a)
  for side in [-1,1]:
   for k in range(16):
    oo=-D/2-2*k;facade_box(m,x,y,side*1.60,oo,-.04,.15,.17,2.50,bridge,a)
    if k<15:sf_beam(m,lp(x,y,side*1.60,oo,-.70,a),lp(x,y,side*1.60,oo-2,1.1,a),.09,.11,bridge,a+math.pi/2)
   for z in [.5,1.18]:sf_beam(m,lp(x,y,side*1.60,-D/2,z,a),lp(x,y,side*1.60,-D/2-30,z,a),.10,.12,bridge,a+math.pi/2)
  facade_box(m,x,y,0,0,H+.02,L,D,.12,AS18,a)
 p18_finish(m)
