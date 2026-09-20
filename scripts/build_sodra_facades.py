"""Pass 13: five photo-informed Södra Långgatan frontage objects.
Footprints are mapped; heights and obscured details remain estimates.
"""
import ast
sodra=json.loads((R/'source/sodra-facades.json').read_text());sodra_names=[]
# Reuse the established recessed masonry and joinery functions, not the old buildings.
for filename in ['build_town_details.py','town_detail_helpers.py','build_larmtorget_facades.py']:
 tree=ast.parse((R/'scripts'/filename).read_text());tree.body=[n for n in tree.body if isinstance(n,ast.FunctionDef)]
 exec(compile(tree,filename,'exec'))
SC={}
for key,col in [('Cream',(.6,.5,.3)),('Sand',(.5,.4,.3)),('RedWood',(.3,.05,.04)),('OchreWood',(.4,.2,.1)),('DarkTile',(.1,.06,.03))]:
 name='M_Sodra_'+key
 if name not in materials:mat(name,col,.8,0,'Sodra'+key)
 SC[key]=name
BROWN=town_mats['PaintBrown'];METAL=town_mats['MetalGrey'];GLAZE=town_mats['Glass'];REDWOOD=SC['RedWood']
def sf_new(bid):
 name=('SM_Building_' if bid=='91846951' else 'SM_Kvarnholmen_House_')+bid
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 sodra_names.append(name);return Mesh(name,'Kvarnholmen/Sodra Langgatan facades')
def sf_edge(p,q):
 return((p[0]+q[0])/2,(p[1]+q[1])/2,math.dist(p,q),math.atan2(q[1]-p[1],q[0]-p[0]))
def sf_roof_z(b,p):return b['height']+b['rise']*max(0,1-abs(p[0 if b['axis']=='x' else 1]-b['centre'])/b['half'])
def sf_shell(m,b,ma,fronts):
 poly=b['polygon'];H=b['height'];clockwise=sum(p[0]*q[1]-q[0]*p[1] for p,q in zip(poly,poly[1:]+poly[:1]))<0
 for i,(p,q) in enumerate(zip(poly,poly[1:]+poly[:1])):
  if clockwise:p,q=q,p
  x,y,L,a=sf_edge(p,q)
  if i in fronts:fronts[i](m,x,y,L,a)
  else:
   facade_box(m,x,y,0,-.12,H/2,L,.24,H,ma,a)
   facade_box(m,x,y,0,.025,.25,L,.09,.5,TS,a)
  # Fill gables exactly to the clipped roof profile.
  axis=0 if b['axis']=='x' else 1;cuts=[0,1]
  for coordinate in [b['centre']-b['half'],b['centre'],b['centre']+b['half']]:
   if abs(q[axis]-p[axis])>.001:
    t=(coordinate-p[axis])/(q[axis]-p[axis])
    if 0<t<1:cuts.append(t)
  cuts.sort()
  for t1,t2 in zip(cuts,cuts[1:]):
   v=[(p[0]+(q[0]-p[0])*t,p[1]+(q[1]-p[1])*t) for t in [t1,t2]];z1,z2=[sf_roof_z(b,vv) for vv in v]
   if max(z1,z2)>H+.001:
    offset=.355 if i in fronts else 0;v=[(vx+math.sin(a)*offset,vy-math.cos(a)*offset) for vx,vy in v]
    vs=[(*v[0],H),(*v[1],H),(*v[1],z2),(*v[0],z1)];vs=[vv for j,vv in enumerate(vs) if vv!=vs[j-1]]
    if len(vs)>2:m.faces(vs,[tuple(range(len(vs)))],ma)
    if offset:m.faces([(*v[0],z1),(*v[1],z2),(v[1][0]-math.sin(a)*offset,v[1][1]+math.cos(a)*offset,z2),(v[0][0]-math.sin(a)*offset,v[0][1]+math.cos(a)*offset,z1)],[(0,1,2,3)],ma)
 for tri in b['roof']:
  vs=[tuple(p) for p in tri]
  if (Vector(vs[1])-Vector(vs[0])).cross(Vector(vs[2])-Vector(vs[0])).z<0:vs.reverse()
  m.faces(vs,[(0,1,2)],METAL if b['rise']==0 else (SC['DarkTile'] if b is sodra['91846952'] else TT))
def sf_beam(m,p,q,width,depth,ma,a):
 p,q=Vector(p),Vector(q);v=(q-p).normalized();out=Vector((math.sin(a),-math.cos(a),0));side=v.cross(out).normalized()*width/2;out*=depth/2
 vs=[tuple(point+ss*side+oo*out) for point in [p,q] for ss,oo in [(-1,-1),(1,-1),(1,1),(-1,1)]]
 m.faces(vs,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],ma)
def sf_pipe(m,x,y,u,H,a,ma=METAL):
 town_path(m,[lp(x,y,u,.32,.18,a),lp(x,y,u,.32,H-.6,a),lp(x,y,u,.52,H-.22,a)],.055,ma)
 for z in [.6,H*.5,H-.8]:facade_box(m,x,y,u,.33,z,.18,.13,.06,ma,a)
def sf_sill(m,x,y,L,H,a):
 town_rod(m,lp(x,y,-L/2,.24,H,a),lp(x,y,L/2,.24,H,a),.09,METAL,12)
def sf_window(m,x,y,u,b,w,h,a,frame=TW,trim=TI,rows=2,cols=2):
 xx,yy,_=lp(x,y,u,0,0,a);lm_window(m,xx,yy,b,w,h,a,frame,False,trim,False,rows,cols)
def sf_modern(m,x,y,u,b,w,h,a,frame=TW,trim=TW,rows=1,cols=1,panel=0):
 # Flush modern reveal; no classical projecting lintel or oversized cornice.
 H=h+panel;xx,yy,_=lp(x,y,u,0,0,a)
 facade_box(m,xx,yy,0,.075,b+H/2,w+.02,.06,H,BROWN if panel else frame,a)
 facade_box(m,xx,yy,0,.125,b+h/2,w-.09,.045,h-.08,GLAZE,a)
 for off in [-w/2,w/2]:facade_box(m,xx,yy,off,.19,b+H/2,.055,.1,H,frame,a)
 for z in [b,b+h,b+H]:facade_box(m,xx,yy,0,.19,z,w,.1,.055,frame,a)
 for k in range(1,cols):facade_box(m,xx,yy,-w/2+w*k/cols,.19,b+h/2,.042,.10,h,frame,a)
 for k in range(1,rows):facade_box(m,xx,yy,0,.19,b+h*k/rows,w,.10,.028,frame,a)
 for off in [-w/2-.07,w/2+.07]:facade_box(m,xx,yy,off,.365,b+H/2,.10,.055,H+.15,trim,a)
 for z in [b-.075,b+H+.075]:facade_box(m,xx,yy,0,.365,z,w+.24,.055,.10,trim,a)
 facade_box(m,xx,yy,0,.39,b-.07,w+.25,.20,.045,METAL,a)
 if panel:
  for k in range(round(w/.13)):
   off=-w/2+.08+k*.13;facade_box(m,xx,yy,off,.17,b+h+panel/2,.025,.04,panel-.05,frame,a)
def sf_wood(m,x,y,L,H,a,ma,holes):
 # Narrow battens stop at windows and doors instead of crossing glass.
 for i in range(round(L/.16)+1):
  u=-L/2+i*L/round(L/.16);spans=[(.25,H)]
  for c,b,w,h,*_ in holes:
   if abs(u-c)<w/2+.06:
    spans=[(l,r) for lo,hi in spans for l,r in [(lo,min(hi,b-.05)),(max(lo,b+h+.05),hi)] if r>l+.01]
  for lo,hi in spans:facade_box(m,x,y,u,.37,(lo+hi)/2,.024,.034,hi-lo,ma,a)
# Modern corner hotel: two upper floors, brown window spandrels, stone piers,
# and a continuous metal canopy. The old generic pitched roof is replaced.
m=sf_new('91846934');b=sodra['91846934']
def hotel_face(m,x,y,L,a):
 bays=max(3,round(L/2.75));centres=[-L/2+(k+.5)*L/bays for k in range(bays)]
 holes=[(0,0,L,3.45,False)]+[(u,z,1.52,2.12,False) for u in centres for z in [4.18,7.15]]
 lm_front(m,x,y,L,10.2,holes,SC['Cream'],a)
 for u in centres:
  for z in [4.18,7.15]:
   sf_modern(m,x,y,u,z,1.52,1.65,a,BROWN,TW,1,1,.47)
  # Ground-storey timber cladding and glazing set behind supporting piers.
  facade_box(m,x,y,u,-.13,1.72,L/bays-.08,.16,2.95,BROWN,a)
  sf_modern(m,x,y,u,1.45,1.9,1.25,a,BROWN,BROWN,1,2)
  facade_box(m,x,y,u,-.04,.45,L/bays,.20,.90,TS,a)
 for k in range(0,bays+1,2):
  u=-L/2+k*L/bays;facade_box(m,x,y,u,.42,1.7,.30,.54,3.4,TS,a)
  for z in [.3,.7,1.1,1.5,1.9,2.3,2.7,3.1]:facade_box(m,x,y,u,.697,z,.30,.012,.013,TI,a)
 facade_box(m,x,y,0,.85,3.43,L+.2,1.8,.23,METAL,a)
 facade_box(m,x,y,0,1.77,3.48,L+.2,.045,.31,TI,a)
 for k in range(round(L/.26)):
  facade_box(m,x,y,-L/2+(k+.5)*.26,.85,3.305,.025,1.7,.018,IRON,a)
 facade_box(m,x,y,0,.05,10.31,L+.18,.43,.22,METAL,a)
 sf_pipe(m,x,y,L/2-.45,10.2,a)
 # Glazed entrance under the canopy.
 town_door(m,*lp(x,y,centres[len(centres)//2],.12,0,a)[:2],.14,1.65,2.62,a,BROWN,True)
sf_shell(m,b,SC['Cream'],{0:hotel_face,1:hotel_face});m.finish()
# White modern neighbouring frontage, grouped windows, an east garage and roof dormers.
m=sf_new('91846979');b=sodra['91846979']
def white_face(m,x,y,L,a):
 centres=[-L/2+(k+.5)*L/6 for k in range(6)];holes=[]
 for k,u in enumerate(centres):
  for z in [.8,3.9,6.9]:
   if k==0 and z==.8:holes.append((u,.18,2.85,2.9,False));continue
   for off in [-1.18,0,1.18]:holes.append((u+off,z,1.04,1.35,False))
 lm_front(m,x,y,L,9.5,holes,TW,a)
 for u,z,w,h,_ in holes:
  if w>2:town_door(m,*lp(x,y,u,.16,0,a)[:2],z,w,h,a,BROWN)
  else:sf_modern(m,x,y,u,z,w,h,a,TW,TW,1,1)
 # Split the plinth at the garage opening.
 town_band_gap(m,x,y,.42,L,a,3.1,METAL,1,gap_center=centres[0])
 for u in [v+L/12 for v in centres[:-1]]:
  for z in [2.8,5.8]:facade_box(m,x,y,u,.38,z,.38,.055,.55,TW,a)
 sf_sill(m,x,y,L,9.55,a)
 for u in [centres[0]+.8,centres[2],centres[4]]:
  xx,yy,_=lp(x,y,u,-1.2,0,a)
  facade_box(m,xx,yy,0,-.8,10.94,4.1,1.6,1.48,METAL,a)
  hs=[(off,10.35,1.14,1.13,False) for off in [-1.3,0,1.3]]
  lm_wall(m,xx,yy,4.1,11.75,[(0,0,4.1,10.25,False)]+hs,METAL,a)
  for off,z,w,h,_ in hs:sf_modern(m,xx,yy,off,z,w,h,a,TW,METAL,1,1)
  facade_box(m,xx,yy,0,-.65,11.81,4.35,2,.14,METAL,a)
 for u in [-L/2+.15,L/2-.15]:sf_pipe(m,x,y,u,9.5,a)
sf_shell(m,b,TW,{0:white_face});m.finish()
# Narrow red wooden gable house, not a generic three-storey block.
m=sf_new('91846996');b=sodra['91846996']
def red_face(m,x,y,L,a):
 hs=[(u,z,1.22,1.30,False) for u in [-1.43,1.43] for z in [.85,3.46]]
 lm_front(m,x,y,L,5.65,hs,REDWOOD,a);sf_wood(m,x,y,L,5.65,a,REDWOOD,hs)
 for u,z,w,h,_ in hs:
  sf_modern(m,x,y,u,z,w,h,a,TW,TW,3,2)
  if z<1:facade_box(m,x,y,u,.50,z-.18,1.32,.40,.18,BROWN,a)
 for u in [-L/2+.06,L/2-.06]:facade_box(m,x,y,u,.37,2.85,.14,.1,5.7,TW,a)
 for k in range(round(L/.16)+1):
  u=-L/2+k*L/round(L/.16);height=1.5*max(0,1-abs(u)/(L/2))
  if height>.03:facade_box(m,x,y,u,.375,5.65+height/2,.024,.035,height,REDWOOD,a)
 for side in [-1,1]:
  a1=lp(x,y,side*L/2,.38,5.65,a);a2=lp(x,y,0,.38,7.15,a)
  sf_beam(m,a1,a2,.20,.10,TW,a)
 sf_pipe(m,x,y,L/2-.17,5.7,a,TW)
sf_shell(m,b,REDWOOD,{4:red_face})
# The low gate closes the actual gap to the neighbouring frontage, with clear street space.
gx,gy,L,a=sf_edge((155.476,-81.61),(150.901,-80.95));hs=[(.72,.13,1.60,2.12,False)]
lm_front(m,gx,gy,L,2.65,hs,REDWOOD,a);sf_wood(m,gx,gy,L,2.65,a,REDWOOD,hs)
town_door(m,*lp(gx,gy,.72,.15,0,a)[:2],.13,1.60,2.12,a,SC['OchreWood'])
facade_box(m,gx,gy,0,.23,2.70,L+.1,.28,.14,TW,a);m.finish()
# Low half-timbered neighbour with steep tile roof and an actual roof dormer.
m=sf_new('91846952');b=sodra['91846952']
def timber_face(m,x,y,L,a):
 centres=[-L/2+1.35+k*(L-2.7)/5 for k in range(6)];hs=[(u,.75,1.20,1.58,False) for u in centres];hs[3]=(centres[3],.10,1.16,2.30,False)
 lm_front(m,x,y,L,3.05,hs,TW,a)
 for i,(u,z,w,h,_) in enumerate(hs):
  if i==3:town_door(m,*lp(x,y,u,.13,0,a)[:2],z,w,h,a,BROWN)
  else:sf_window(m,x,y,u,z,w,h,a,TW,BROWN,3,2)
 for z in [.30,2.50,2.94]:facade_box(m,x,y,0,.39,z,L,.13,.16,BROWN,a)
 for k in range(7):
  u=-L/2+k*L/6;facade_box(m,x,y,u,.39,1.62,.15,.13,2.85,BROWN,a)
  if k<6:
   for z0,z1 in [(.4,.72),(2.61,2.83)]:
    sf_beam(m,lp(x,y,u+.18,.41,z0,a),lp(x,y,u+L/6-.18,.41,z1,a),.11,.12,BROWN,a)
 sf_sill(m,x,y,L,3.08,a)
 xx,yy,_=lp(x,y,1.3,-1.15,0,a);lm_dormer(m,xx,yy,4.18,2.0,a,SC['DarkTile'])
 for u in [-L/2+.1,L/2-.1]:sf_pipe(m,x,y,u,3.05,a)
sf_shell(m,b,TW,{0:timber_face});m.finish()
# Northern corner frontage: three distinct material/roof characters in one mapped object.
m=sf_new('91846951');b=sodra['91846951']
def north_front(m,x,y,L,a):
 at=-L/2
 for width,ma,mode in [(21,SC['Sand'],'plaster'),(9,SC['OchreWood'],'wood'),(L-30,TL,'lime')]:
  centre=at+width/2;xx,yy,_=lp(x,y,centre,0,0,a);bays=5 if mode=='plaster' else 3;us=[-width/2+(k+.5)*width/bays for k in range(bays)]
  hs=[(u,z,1.20 if z>3 else 2.08,1.58 if z>3 else 2.00,False) for u in us for z in [.48,3.90]]
  hs[2]= (us[1],.16,1.28,2.48,False)
  lm_front(m,xx,yy,width,6.25,hs,ma,a)
  for u,z,w,h,_ in hs:
   if z==.16:town_door(m,*lp(xx,yy,u,.10,0,a)[:2],z,w,h,a,TW,True)
   else:sf_window(m,xx,yy,u,z,w,h,a,TW,TW,3 if z>3 else 1,2 if z>3 else 1)
  if mode=='wood':sf_wood(m,xx,yy,width,6.25,a,ma,hs)
  else:
   for u in [-width/2+.14,width/2-.14]:facade_box(m,xx,yy,u,.42,3.28,.26,.18,5.92,TW,a)
  lm_cornice(m,xx,yy,width,6.30,a,TW)
  facade_box(m,xx,yy,0,.22,.23,width,.15,.46,SC['RedWood'],a)
  for u in [-width/2+.2,width/2-.2]:sf_pipe(m,xx,yy,u,6.30,a,TW)
  at+=width
 # A small green entrance awning on the eastern part, seen in the reference.
 facade_box(m,x,y,L/2-7,.80,2.72,2.7,1.35,.14,TG,a)
def north_west(m,x,y,L,a):
 # Only the street-facing 11.5 m front wing receives the old gable facade.
 hs=[(u,z,1.22,1.6,False) for u in [L/2-2.0,L/2-5.7,L/2-9.4] for z in [.5,3.9]]
 lm_front(m,x,y,L,6.25,hs,SC['Sand'],a)
 for u,z,w,h,_ in hs:sf_modern(m,x,y,u,z,w,h,a,TW,TW,3,2)
 lm_cornice(m,x,y,L,6.30,a,TW)
sf_shell(m,b,SC['Sand'],{0:north_west,1:north_front})
# Roof-profile trims on the western street gable follow the filled geometry.
p,q=b['polygon'][0:2];x,y,L,a=sf_edge(p,q);front_centre=sf_edge((57.563,-69.239),(57.755,-57.745))
for pa,pb in [((57.563,-69.239,6.3),(57.66,-63.5,9.65)),((57.66,-63.5,9.65),(57.755,-57.745,6.3))]:town_rod(m,pa,pb,.10,TW,8)
town_window(m,57.66,-63.5,7.66,1.05,1.2,-math.pi/2,TW,False,2,2,True)
# Chimneys meet the roof, with caps and flashing.
for x,y in [(65,-63.5),(88,-63.5),(96,-61.8)]:
 z=sf_roof_z(b,(x,y));m.box((x,y,z+.65),(.65,.75,1.3),SC['Sand']);m.box((x,y,z+1.30),(.82,.92,.14),METAL)
m.finish()
# Small edge bevels catch light without changing the footprint or closing openings.
for name in sodra_names:
 obj=bpy.data.objects[name];obj['facade_pass']=13;obj['massing_only']=False;obj['reference_notes']='references/sodra-facades-reference-notes.json'
 # All new faces retain physically scaled projected UV for the existing PBR maps.
 me=obj.data;bm=bmesh.new();bm.from_mesh(me);bmesh.ops.triangulate(bm,faces=list(bm.faces));bad=[f for f in bm.faces if f.calc_area()<1e-9];bmesh.ops.delete(bm,geom=bad,context='FACES') if bad else None;bm.to_mesh(me);bm.free();me.update()
sodra_cameras=[('54_Sodra_Hotellhorn',(48,-68,2.3),(73,-91,5.0),28),('55_Sodra_Fasadstrak',(112,-73.8,2.0),(173,-81.2,4.4),30),('56_Sodra_Trahus',(158,-72.0,2.1),(162,-83,3.4),27),('57_Sodra_NorraHornet',(51,-76,2.8),(75,-63.5,5.0),29),('58_Sodra_Oversikt',(112,-152,73),(116,-71,2),34)]
