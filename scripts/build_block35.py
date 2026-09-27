"""Pass 35: two houses on the south side of Södra Långgatan, opposite pass 34 (OSM 92379316 and
92379296).

The wooden house (number 22 by its door): ochre vertical boarding with white corner boards and two
white pilaster boards; a ground floor of four shop windows, a glazed door, a red double door and a
second glazed door in white casings, a narrow boarded panel with a vent, a grey awning box over the
first three openings and a white band; four upper windows with red casements in white surrounds
under drip caps; a white frieze and moulded cornice; a red tile roof with two wall dormers
(round-headed windows in red fronts under segmental hoods) and a chimney on the ridge.

The palace: a rusticated ground floor with flat arches over its openings, the stone portal with a
pediment and a relief in the tympanum (its lettering omitted), a narrow window, five shop windows,
a glazed shop door and a wooden door; a band; two storeys of white casements in yellow render
between rusticated quoins; a three-axis centre framed by two Ionic pilasters under an entablature
broken forward and a pediment with an oculus and garlands (triangulated from two panoramas); the
cornice; three small roof dormers over each wing; a dark metal roof.

References: Google Street View April 2025 (registered on one camera track), view only. Zones:
source/block35.json; see references/block35-notes.md. Tenant signs and lettering are omitted.
"""
B35D=json.loads((R/'source/block35.json').read_text());Z=B35D['zones']
block35_names=[];B35={}
for old in [k for k in list(materials) if k.startswith('M_Block35_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Ochre','TownPaintBrown',(.80,.55,.28),.70,0),
 ('White','TownIvory',(.94,.94,.91),.82,0),
 ('RedSash','TownPaintBrown',(.55,.17,.13),.55,0),
 ('RedDoor','TownPaintBrown',(.62,.14,.12),.55,0),
 ('DormerRed','TownMetalRed',(.47,.15,.12),.60,.10),
 ('Tile','TownTileRed',(.58,.31,.21),.80,0),
 ('Plinth','TownStone',(.46,.46,.45),.80,0),
 ('Awning','TownPanel',(.52,.52,.51),.85,0),
 ('Yellow','TownIvory',(.90,.72,.40),.88,0),
 ('Stone','TownStone',(.81,.75,.63),.86,0),
 ('Grey','TownStone',(.62,.60,.56),.82,0),
 ('Render','TownIvory',(.75,.73,.68),.88,0),
 ('FrameRed','TownPaintBrown',(.44,.20,.15),.55,0),
 ('Oak','TownPaintBrown',(.56,.41,.26),.60,0),
 ('RoofDark','TownMetalGrey',(.28,.29,.30),.55,.30),
 ('Dark','TownMetalGrey',(.05,.055,.06),.40,.20),
 ]:
 name='M_Block35_'+key;B35[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block35_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B35;WH,PL=M['White'],M['Plinth']

def snap35(holes):
 # Openings whose tops agree to within a millimetre get bit-identical tops, so that bz_wall does
 # not cut a zero-height row between two nearly equal levels.
 tops=[];out=[]
 for u,b,w,h,r in holes:
  t=b+h;t0=next((v for v in tops if abs(v-t)<1e-3),None)
  if t0 is None:tops.append(t);out.append((u,b,w,h,r));continue
  h2=t0-b
  while b+h2!=t0:h2=math.nextafter(h2,math.inf if b+h2<t0 else -math.inf)
  out.append((u,b,w,h2,r))
 return out
def b35_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block35_names.append(name);return Mesh(name,category)
def b35_finish(m,osm):
 obj=s21_finish(m);obj['detail_pass']=35;obj['reference_notes']='references/block35-notes.md';obj['osm_way']=osm;return obj
def street35(w):
 ox,oy=outward(w);return w['kind']=='outer' and oy>.9 and max(w['p'][1],w['q'][1])>-81
def front35(m,zone,wall,frame,levels):
 for w in walls(zone):
  if w['kind']!='outer':bz_wall(m,w['p'],w['q'],w['z0'],Z[zone]['height'],[],wall)
  elif not street35(w):plain(m,w,Z[zone]['height'],wall,frame,WH,levels,.9)
def rear35(m,zone,wall,frame,roof,levels):
 for w in walls(zone):
  if w['kind']=='outer':plain(m,w,Z[zone]['height'],wall,frame,WH,levels,.9)
  else:bz_wall(m,w['p'],w['q'],w['z0'],Z[zone]['height'],[],wall)
 for g in Z[zone]['polygons']:
  pts=simplify([tuple(v) for v in g],.8)
  inset_roof(m,pts,Z[zone]['height'],min(2.4,.45*min(math.dist(p,q) for p,q in zip(pts,pts[1:]+pts[:1]))),Z[zone]['top']-Z[zone]['height'],roof,.35)
def ridge35(m,zone,ma):
 # Ridge cap along the middle of the front range's ridge band.
 r1=Z[zone]['roof']['r1'];T=Z[zone]['top']
 p=((r1[0][0]+r1[3][0])/2,(r1[0][1]+r1[3][1])/2);q=((r1[1][0]+r1[2][0])/2,(r1[1][1]+r1[2][1])/2)
 town_rod(m,(*p,T+.06),(*q,T+.06),.11,ma,8)
 return p,q
def boards35(m,x,y,L,a,z0,z1,holes,ma,step=.19):
 # Vertical board cladding: battens on the boarded wall, stopped at the openings' casings.
 n=int(L/step)
 for k in range(1,n):
  u=-L/2+k*L/n;segs=[(z0,z1)]
  for hu,hb,hw,hh,hr in holes:
   if abs(u-hu)<hw/2+.17:segs=[(lo,hi) for l,h_ in segs for lo,hi in ((l,min(h_,hb-.16)),(max(l,hb+hh+.20),h_)) if hi-lo>.05]
  for lo,hi in segs:facade_box(m,x,y,u,.37,(lo+hi)/2,.035,.03,hi-lo,ma,a)
def win35d(m,x,y,u,b,w,spring,crown,a,frame):
 # The wall dormers' round-headed windows: white frame, mullion and a transom at the springing, a
 # thin sill; (x,y) is the dormer's front plane.
 r=crown-spring;h=spring-b;k=16
 contour=[(-w/2,b),(w/2,b)]+[(w/2*math.cos(t*math.pi/k),spring+r*math.sin(t*math.pi/k)) for t in range(k+1)]
 m.faces([lp(x,y,uu,-.10,zz,a) for uu,zz in contour],[tuple(range(len(contour)))],GLAZE)
 for q in (-w/2+.035,w/2-.035):facade_box(m,x,y,u+q,-.05,b+h/2,.07,.08,h,frame,a)
 facade_box(m,x,y,u,-.05,b+.035,w,.08,.07,frame,a);facade_box(m,x,y,u,-.05,spring,w,.08,.06,frame,a)
 facade_box(m,x,y,u,-.05,(b+spring)/2+r/2,.06,.08,h+r-.02,frame,a)
 p18_arch(m,*lp(x,y,u,0,0,a)[:2],spring,w,r,.07,-.05,a,frame,16)
 facade_box(m,x,y,u,.03,b-.02,w+.10,.10,.04,frame,a)
def wdormer35(m,x,y,u,a,of,zf,slope,w,sill,spring,crown,top,body,hood,frame):
 # Wall dormer on the steep lower roof slope (the two on the wooden house, triangulated): a
 # round-headed window in a red front, red cheeks and a segmental hood. The front stands at of
 # (outward of the OSM line), where the roof is at zf; the body runs back until the roof reaches
 # the hood. The front has a rectangular opening up to the springing; above it the front is built
 # in strips that stop at the arch (an arched hole's spandrels would triangulate into slivers).
 xx,yy,_=lp(x,y,u,of,0,a);W=w+.36;zh=spring+.30
 depth=(top-zf)/slope+.30
 p0=lp(xx,yy,-W/2,0,0,a)[:2];p1=lp(xx,yy,W/2,0,0,a)[:2]
 bz_wall(m,p0,p1,zf-.30,spring,[(0,sill,w,spring-sill,0)],body,-.12,0)
 win35d(m,xx,yy,0,sill,w,spring,crown,a,frame)
 k=14;half=W/2+.05;rise=top-zh;R_=(half*half+rise*rise)/(2*rise);zo=top-R_;t0=math.asin(half/R_)
 prof=[(R_*math.sin(-t0+2*t0*i/k),zo+R_*math.cos(-t0+2*t0*i/k)) for i in range(k+1)]
 for (u0,z0),(u1,z1) in zip(prof,prof[1:]):
  m.faces([lp(xx,yy,u0,.02,z0,a),lp(xx,yy,u1,.02,z1,a),lp(xx,yy,u1,-depth,z1,a),lp(xx,yy,u0,-depth,z0,a)],[(0,1,2,3)],hood)
 hw=w/2+.07;rr=crown-spring+.07;n_=16
 def hood_in(uu):return zo+math.sqrt(max(0,R_*R_-uu*uu))-.05
 def arch_out(uu):return spring+rr*math.sqrt(max(0,1-(uu/hw)**2)) if abs(uu)<hw else spring
 for i in range(n_):
  ua,ub=-W/2+W*i/n_,-W/2+W*(i+1)/n_
  za,zb_=arch_out(ua),arch_out(ub);ta,tb=hood_in(ua),hood_in(ub)
  if ta>za+.01 and tb>zb_+.01:m.faces([lp(xx,yy,ua,-.02,za,a),lp(xx,yy,ub,-.02,zb_,a),lp(xx,yy,ub,-.02,tb,a),lp(xx,yy,ua,-.02,ta,a)],[(0,1,2,3)],body)
 for sg in (-1,1):facade_box(m,xx,yy,sg*(W/2-.05),-depth/2,(zf-.30+zh)/2,.10,depth,zh-zf+.30,body,a)
def roof35w(m,zone,prof,ma,gable):
 # A broken roof across the front range: profile (o, z) pairs from the eaves to the courtyard wall,
 # o outward of the street edge; each band spans the two party walls. Gables fill both party walls
 # from the zone height up to the roof, including the small triangle under the eaves overhang.
 fr=Z[zone]['roof']['outer'];H=Z[zone]['height'];p,q=fr[0],fr[1]
 L=math.dist(p,q);ux,uy=(q[0]-p[0])/L,(q[1]-p[1])/L;nx,ny=uy,-ux      # outward (street side)
 def meet(o,wa,wb):
  # The street edge offset by o, cut by the party wall line wa-wb.
  ax,ay=p[0]+nx*o,p[1]+ny*o;dx,dy=wb[0]-wa[0],wb[1]-wa[1];den=ux*dy-uy*dx
  t=((wa[0]-ax)*dy-(wa[1]-ay)*dx)/den;return (ax+ux*t,ay+uy*t)
 E=lambda o:meet(o,fr[0],fr[3]);Wp=lambda o:meet(o,fr[1],fr[2])
 for (oa,za),(ob,zb) in zip(prof,prof[1:]):
  m.faces([(*E(oa),za),(*Wp(oa),za),(*Wp(ob),zb),(*E(ob),zb)],[(0,1,2,3)],ma)
 (o0,z0),(o1,z1)=prof[0],prof[1];zw=z0+(z1-z0)*o0/(o0-o1)             # the roof over the street edge
 cx=sum(v[0] for v in fr)/4;cy=sum(v[1] for v in fr)/4
 for side in (E,Wp):
  ring=[(0,H),(0,zw)]+[(o,z) for o,z in prof[1:]]+[(prof[-1][0],H)]
  for poly in (ring,[(o0,z0),(0,zw),(0,H)]):
   vs=[(*side(o),z) for o,z in poly]
   # Newell normal of the ring as listed (right-hand rule)
   nxx=sum((vs[i-1][1]-vs[i][1])*(vs[i-1][2]+vs[i][2]) for i in range(len(vs)))
   nyy=sum((vs[i-1][2]-vs[i][2])*(vs[i-1][0]+vs[i][0]) for i in range(len(vs)))
   sx,sy=side(-5.0);out=(sx-cx)*nxx+(sy-cy)*nyy
   m.faces(vs,[tuple(range(len(vs))) if out>0 else tuple(reversed(range(len(vs))))],gable)
 return E,Wp
def win35p(m,x,y,u,b,w,h,a,frame):
 # The palace's casements in the render without a casing, set 0.13 m into the wall (the oblique
 # views show a narrow reveal): dark glass, white frame, mullion, transom and glazing bars, a thin
 # white sill.
 facade_box(m,x,y,u,.17,b+h/2,w,.02,h,GLAZE,a)
 for q in (-w/2+.04,w/2-.04):facade_box(m,x,y,u+q,.22,b+h/2,.08,.08,h,frame,a)
 for zz in (b+.04,b+h-.04):facade_box(m,x,y,u,.22,zz,w,.08,.08,frame,a)
 facade_box(m,x,y,u,.23,b+h*.66,w,.06,.06,frame,a);facade_box(m,x,y,u,.23,b+h*.33,w,.05,.03,frame,a)
 facade_box(m,x,y,u,.23,b+h/2,.06,.06,h,frame,a)
 facade_box(m,x,y,u,.33,b-.02,w+.04,.24,.025,frame,a)
def win35w(m,x,y,u,b,w,h,a,sash,trim):
 # The wooden house's windows: red casements (two lights of three panes) in a flat white surround
 # 0.12 m wide under a thin drip cap, whose top is 0.13 m above the opening.
 facade_box(m,x,y,u,.24,b+h/2,w,.02,h,GLAZE,a)
 for q in (-w/2+.035,w/2-.035):facade_box(m,x,y,u+q,.30,b+h/2,.07,.08,h,sash,a)
 for zz in (b+.035,b+h-.035):facade_box(m,x,y,u,.30,zz,w,.08,.07,sash,a)
 facade_box(m,x,y,u,.30,b+h/2,.08,.08,h,sash,a)
 for k in (1,2):facade_box(m,x,y,u,.30,b+h*k/3,w,.05,.03,sash,a)
 for sg in (-1,1):facade_box(m,x,y,u+sg*(w/2+.06),.37,b+h/2,.12,.04,h+.26,trim,a)
 facade_box(m,x,y,u,.37,b+h+.04,w+.24,.04,.08,trim,a);facade_box(m,x,y,u,.37,b-.065,w+.24,.04,.13,trim,a)
 facade_box(m,x,y,u,.40,b+h+.105,w+.36,.10,.05,trim,a);facade_box(m,x,y,u,.40,b-.03,w+.20,.10,.03,trim,a)
def door35(m,x,y,u,b,w,h,a,ma,casing):
 # s20_door with the casing in the wall's own material (the palace's doors stand in stone).
 facade_box(m,x,y,u,.14,b+h/2,w,.15,h,ma,a)
 for side in [-1,1]:
  facade_box(m,x,y,u+side*(w/2+.055),.39,b+h/2,.16,.20,h+.14,casing,a)
  for z in [b+.5,b+1.2,b+2.0]:
   if z+.27<b+h:town_border(m,*lp(x,y,u+side*w*.24,0,0,a)[:2],z,w*.38,.52,a,ma,.26,.035)
 for q in [0,-w/2,w/2]:facade_box(m,x,y,u+q,.245,b+h/2,.055,.09,h,ma,a)
 facade_box(m,x,y,u,.43,b+h+.065,w+.28,.25,.14,casing,a)
 for s in [-1,1]:town_rod(m,lp(x,y,u+s*.075,.29,b+1.1,a),lp(x,y,u+s*.075,.29,b+1.38,a),.016,METAL)
 facade_box(m,x,y,u,.51,b-.045,w+.35,.8,.10,TS,a)
def flat_arch35(m,x,y,u,z0,z1,w,a,ma,n=7,spread=22):
 # Flat arch of radiating voussoirs over an opening (the palace's rusticated ground floor).
 zc=z0-(w/2)/math.tan(math.radians(spread))
 for i in range(n):
  e=[(u-w/2+w*(i+t)/n,z0) for t in (.03,.97)]
  top=[(u+(uu-u)*(z1-zc)/(z0-zc),z1) for uu,_ in e]
  ring=[e[0],e[1],top[1],top[0]]
  vs=[lp(x,y,uu,o,zz,a) for o in (.355,.405) for uu,zz in ring]
  m.faces(vs,[(3,2,1,0),(4,5,6,7)]+[(j,(j+1)%4,(j+1)%4+4,j+4) for j in range(4)],ma)
def pediment35(m,x,y,uc,zb,w,apex,a,body,trim,ot=.55,oc=1.0,band=.32):
 # Pediment triangulated from two panoramas: the tympanum 0.2 m proud of the wall, the raking
 # and base cornices 0.65 m proud, the raking cornice's top at the apex.
 rise=apex-band-zb
 tri=[(uc-w/2+.35,zb+band),(uc+w/2-.35,zb+band),(uc,zb+band+rise*(1-.35/(w/2)))]
 vs=[lp(x,y,uu,o,zz,a) for o in (.36,ot) for uu,zz in tri]
 m.faces(vs,[(2,1,0),(3,4,5),(0,1,4,3),(1,2,5,4),(2,0,3,5)],body)
 for sg in (-1,1):
  # Raking cornice: foot, its top, the apex, the apex's underside; counter-clockwise (as seen from
  # the street) on the west side, clockwise on the east side.
  ring=[(uc+sg*w/2,zb),(uc+sg*w/2,zb+band),(uc,apex),(uc,apex-band)]
  vv=[lp(x,y,uu,o,zz,a) for o in (.36,oc) for uu,zz in ring]
  f=[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
  if sg<0:f=[tuple(reversed(t)) for t in f]
  m.faces(vv,f,trim)
 facade_box(m,x,y,uc,(.36+oc)/2,zb+band/2,w-.20,oc-.36,band,trim,a)
def ionic35(m,x,y,u,z,w,a,ma,o=.53):
 # Ionic capital: echinus, abacus and a volute either side.
 facade_box(m,x,y,u,o-.03,z+.08,w+.06,.22,.16,ma,a);facade_box(m,x,y,u,o,z+.30,w+.20,.26,.10,ma,a)
 for sg in (-1,1):
  kk=14;cx_=u+sg*(w/2+.02)
  town_path(m,[lp(x,y,cx_+.11*math.cos(t*math.tau/kk),o+.06,z+.13+.11*math.sin(t*math.tau/kk),a) for t in range(kk+1)],.035,ma)
  facade_box(m,x,y,cx_,o+.03,z+.13,.10,.12,.10,ma,a)

# ---------------------------------------------------------------- the wooden house
OC,RS=M['Ochre'],M['RedSash'];H22=Z['w22']['height']
m=b35_new('SM_Kvarnholmen_House_92379316','Kvarnholmen/Södra Långgatan south')
front35(m,'w22',OC,RS,2)
for w in walls('w22'):
 if not street35(w):continue
 x,y,L,a=sf_edge(w['p'],w['q']);S=lambda s:-L/2+s             # s from the east joint
 # Openings, measured from panorama "22" (registered on the house's east joint and the camera track).
 gf=[(S(1.665),.64,1.33,1.62,0),(S(2.975),0,.83,2.26,0),(S(4.26),.55,1.24,1.71,0),(S(6.295),0,1.27,2.26,0),
     (S(8.20),.55,1.26,1.71,0),(S(9.75),.30,.82,1.96,0),(S(11.13),.54,1.30,1.72,0)];gf=snap35(gf)
 up=[(S(s),3.51,1.12,1.54,0) for s in (2.03,4.03,7.25,10.58)]
 bz_wall(m,w['p'],w['q'],0,H22,gf+up,OC)
 for i,(u,b,ww,hh,r) in enumerate(gf):
  if i==3:s20_door(m,x,y,u,b,ww,hh,a,M['RedDoor']);continue
  if b<.35:s21_glass(m,x,y,u,b,ww,hh,a,M['RedDoor'],1,.78,True)
  else:s21_glass(m,x,y,u,b,ww,hh,a,WH,1 if ww<1.3 else 2,0,False)
  for sg in (-1,1):facade_box(m,x,y,u+sg*(ww/2+.06),.40,b+hh/2,.12,.08,hh+.10,WH,a)
  facade_box(m,x,y,u,.40,b+hh+.05,ww+.24,.08,.10,WH,a)
 # The boarded panel between the double door and the third shop window, with a vent.
 facade_box(m,x,y,S(7.26),.39,1.30,.36,.05,1.80,OC,a);facade_box(m,x,y,S(7.26),.42,2.05,.24,.04,.16,M['Dark'],a)
 for u,b,ww,hh,r in up:
  win35w(m,x,y,u,b,ww,hh,a,RS,WH)
 boards35(m,x,y,L,a,.40,2.28,gf+[(S(7.26),.40,.36,1.80,0)],OC);boards35(m,x,y,L,a,2.48,5.38,up,OC)
 # Corner boards, the two pilaster boards, the band, the frieze and the moulded cornice.
 for s0,s1 in ((0,.45),(9.01,9.24),(5.34,5.62),(11.92,12.32)):facade_box(m,x,y,S((s0+s1)/2),.375,(.40+5.38)/2,s1-s0,.04,4.98,WH,a)
 facade_box(m,x,y,0,.42,2.33,L,.12,.14,WH,a);facade_box(m,x,y,0,.47,2.415,L+.04,.18,.03,WH,a)
 facade_box(m,x,y,S(2.90),.58,2.30,4.10,.30,.19,M['Awning'],a)
 # Frieze 5.38-5.59; the cornice steps out to 0.45 m with its gutter's top at 5.78 (6.08 on the
 # facade plane, corrected for the projection; the eaves at 5.85).
 facade_box(m,x,y,0,.40,5.485,L,.08,.21,WH,a)
 facade_box(m,x,y,0,.46,5.63,L+.04,.18,.08,WH,a);facade_box(m,x,y,0,.53,5.69,L+.06,.32,.06,WH,a);facade_box(m,x,y,0,.60,5.75,L+.08,.46,.06,WH,a)
 town_rod(m,lp(x,y,-L/2,.86,5.73,a),lp(x,y,L/2,.86,5.73,a),.05,METAL,8)
 plinth34(m,x,y,L,a,[(u-ww/2-.02,u+ww/2+.02) for u,b,ww,hh,r in gf if b<.35],.40)
# The broken roof, o outward of the street edge (the modelled wall face is at 0.355): the eaves at
# 0.65 above the cornice, a steep kick to the dormer fronts, 53° to the break measured on the west
# fire wall (1.7 m behind the facade, 8.8 m), then 38° to the ridge (11.33 m from the sky line in the
# level view) and down to the courtyard wall.
PROF=[(.65,5.92),(.30,6.64),(-1.345,8.80),(-4.60,11.33),(-9.95,7.40)]
E_,W_=roof35w(m,'w22',PROF,M['Tile'],OC)
ridge=[(*E_(-4.60),11.39),(*W_(-4.60),11.39)];town_rod(m,ridge[0],ridge[1],.11,M['Tile'],8)
for w in walls('w22'):
 if street35(w):
  x,y,L,a=sf_edge(w['p'],w['q']);S=lambda s:-L/2+s
  # Wall dormers on the steep kick: fronts 0.055 behind the wall face, sills 6.64 on the tiles,
  # round heads with the frames' tops at 7.91, the hoods' tops 8.11 and 7.99 (triangulated).
  for s,top in ((3.20,8.11),(9.18,7.99)):wdormer35(m,x,y,S(s),a,.30,6.62,1.31,1.00,6.64,7.34,7.84,top,M['DormerRed'],M['DormerRed'],WH)
  cx,cy,_=lp(x,y,S(6.2),-4.60,0,a);box(m,cx,cy,.55,.85,11.60-10.90,10.90,M['Render'],a,M['Dark'])
rear35(m,'w22r',OC,RS,M['Tile'],2)
b35_finish(m,'92379316')

# ---------------------------------------------------------------- the palace
YE,ST,GR=M['Yellow'],M['Stone'],M['Grey'];HP=Z['pal']['height']
m=b35_new('SM_Kvarnholmen_House_92379296','Kvarnholmen/Södra Långgatan south')
front35(m,'pal',M['Render'],WH,3)
for w in walls('pal'):
 if not street35(w):continue
 x,y,L,a=sf_edge(w['p'],w['q']);S=lambda s:-L/2+s             # s from the measured east joint
 # Window axes: the east wing from two-panorama triangulation, the centre and the west wing from
 # panorama "21" in front of them (checked against "18").
 AX=[2.02,4.48,6.96,9.55,11.59,13.56,16.25,18.43,20.57]
 gf=[(S(2.25),0,2.20,3.32,0),(S(4.91),.61,.64,2.60,0),(S(6.85),.86,1.25,2.44,0),(S(9.15),.86,1.20,2.44,0),(S(11.70),0,1.55,3.30,0),
     (S(13.95),.86,1.24,2.44,0),(S(16.11),.86,1.35,2.44,0),(S(18.29),.86,1.20,2.44,0),(S(20.53),0,1.03,3.32,0)];gf=snap35(gf)
 up=[(S(s),b,1.22,h,0) for s in AX for b,h in ((5.31,1.67),(8.60,1.47))]
 # The ground floor's openings stand in deep reveals (about 0.45 m, from the oblique views): the
 # wall there is 0.55 m thick and the joinery is set 0.20 m further back than in the upper storeys.
 bz_wall(m,w['p'],w['q'],0,4.25,gf,ST,-.20,.355);bz_wall(m,w['p'],w['q'],4.25,HP,up,YE)
 gx,gy,_=lp(x,y,0,-.20,0,a)
 # Rusticated ground floor: channelled courses stopped at the openings, flat arches over them.
 rustic(m,x,y,-L/2,L/2,.75,4.25,a,ST,[(u,b,ww,4.25-b,0) for u,b,ww,hh,r in gf[1:]]+[(S(2.25),0,4.70,4.25,0)],.42)
 for u,b,ww,hh,r in gf[1:]:flat_arch35(m,x,y,u,b+hh,4.25,ww,a,ST,7 if ww>1 else 5)
 for i,(u,b,ww,hh,r) in enumerate(gf):
  if i in (0,8):door35(m,gx,gy,u,b,ww,hh,a,M['Oak'],M['Oak'])
  elif b==0:s21_glass(m,gx,gy,u,b,ww,hh,a,M['FrameRed'],1,.78,True)
  else:s21_glass(m,gx,gy,u,b,ww,hh,a,M['FrameRed'],1 if ww<1 else 2,.78,False)
 plinth34(m,x,y,L,a,[(u-ww/2-.02,u+ww/2+.02) for u,b,ww,hh,r in gf if b<.75],.75)
 facade_box(m,x,y,0,.40,4.345,L,.10,.19,GR,a);p18_band(m,x,y,L+.1,4.38,a,GR,.24)
 # The portal: piers 0.55 m wide and 0.2 m proud with consoles, the frieze (its lettering omitted),
 # a cornice and the pediment to 5.31, 0.3-0.45 m proud (triangulated), with a relief in the tympanum.
 pc=S(2.25);pw=4.56
 for sg in (-1,1):
  uu=pc+sg*1.375
  facade_box(m,x,y,uu,.455,1.66,.55,.20,3.32,GR,a)
  for zz in (.9,1.8,2.7):facade_box(m,x,y,uu,.565,zz,.57,.02,.04,M['Stone'],a)
  facade_box(m,x,y,uu,.57,3.72,.34,.30,.52,GR,a)
  town_path(m,[lp(x,y,uu+.10*math.cos(t*math.tau/14),.73,3.52+.10*math.sin(t*math.tau/14),a) for t in range(15)],.035,GR)
 facade_box(m,x,y,pc,.48,3.83,pw-.30,.26,.74,GR,a);facade_box(m,x,y,pc,.56,4.27,pw,.42,.14,GR,a)
 ptri=[(pc-pw/2,4.34),(pc+pw/2,4.34),(pc,5.31)]
 vs=[lp(x,y,uu,o,zz,a) for o in (.40,.72) for uu,zz in ptri]
 m.faces(vs,[(2,1,0),(3,4,5),(0,1,4,3),(1,2,5,4),(2,0,3,5)],GR)
 for (u0,z0),(u1,z1) in ((ptri[0],ptri[2]),(ptri[2],ptri[1])):town_rod(m,lp(x,y,u0,.78,z0+.05,a),lp(x,y,u1,.78,z1+.05,a),.07,GR,8)
 for k in range(9):
  t=k/8;uu=pc+(t-.5)*2.4;zz=4.52+.26*math.sin(math.pi*t)
  xx,yy,_=lp(x,y,uu,.74,0,a);m.lathe(xx,yy,zz-.07,[(.02,0),(.07,.04),(.08,.08),(.05,.13),(.02,.15)],GR,8)
 # Upper storeys: white casements in the yellow render.
 for u,b,ww,hh,r in up:win35p(m,x,y,u,b,ww,hh,a,WH)
 quoins(m,x,y,-L/2+.01,4.50,10.35,a,GR,1,.42,.85,.50);quoins(m,x,y,L/2-.01,4.50,10.35,a,GR,-1,.42,.85,.50)
 # Ionic pilasters framing the centre.
 for s in (8.28,14.86):
  facade_box(m,x,y,S(s),.44,7.315,.70,.18,5.67,GR,a);facade_box(m,x,y,S(s),.47,4.60,.82,.24,.24,GR,a)
  ionic35(m,x,y,S(s),10.15,.70,a,GR)
 # Entablature and cornice (architrave from 10.51, top 11.6, corona 0.45 m out, all corrected for
 # their projection); broken forward 0.2 m over the centre.
 facade_box(m,x,y,0,.39,10.605,L,.07,.19,GR,a);facade_box(m,x,y,0,.375,10.85,L,.04,.30,GR,a)
 facade_box(m,x,y,0,.47,11.06,L+.10,.24,.16,GR,a);facade_box(m,x,y,0,.58,11.33,L+.30,.46,.30,GR,a);facade_box(m,x,y,0,.60,11.55,L+.34,.50,.10,GR,a)
 rc=S(11.57)
 facade_box(m,x,y,rc,.56,10.755,7.72,.40,.49,GR,a);facade_box(m,x,y,rc,.78,11.33,7.92,.50,.30,GR,a);facade_box(m,x,y,rc,.80,11.55,8.00,.54,.10,GR,a)
 # The pediment: feet 7.74 and 15.50, the apex 13.68 (the raking cornice's top), 0.65 m proud; an
 # oculus at 12.49 between two garlands.
 pediment35(m,x,y,rc,11.60,7.76,13.68,a,YE,GR)
 kk=24;m.faces([lp(x,y,rc+.30*math.cos(t*math.tau/kk),.56,12.49+.30*math.sin(t*math.tau/kk),a) for t in range(kk)],[tuple(range(kk))],GLAZE)
 town_path(m,[lp(x,y,rc+.36*math.cos(t*math.tau/kk),.60,12.49+.36*math.sin(t*math.tau/kk),a) for t in range(kk+1)],.06,GR)
 for sg in (-1,1):town_path(m,[lp(x,y,rc+sg*(.45+.9*t),.60,12.55-.22*math.sin(math.pi*t)-.10*t,a) for t in [k/10 for k in range(11)]],.06,GR)
 gable_behind(m,x,y,rc,11.62,7.76,13.68-.32-11.62,a,M['RoofDark'],3.0)
 # Small flat-topped roof dormers over each wing, 0.6 m behind the wall face with their tops at
 # 13.8: the west ones where "21" places them, the east ones on the window axes (the oblique view
 # from "22" agrees); only their tops show above the cornice.
 for s in (2.02,4.48,6.96,16.27,18.70,21.00):
  xx,yy,_=lp(x,y,S(s),.355-.60,0,a)
  facade_box(m,xx,yy,0,-.55,12.66,1.55,1.10,2.12,M['Render'],a)
  facade_box(m,xx,yy,0,.01,13.22,1.10,.04,.42,M['Dark'],a)
  facade_box(m,xx,yy,0,-.53,13.76,1.63,1.18,.08,M['RoofDark'],a)
sl=roof34(m,'pal',M['RoofDark'],M['Render'])
rear35(m,'palr',YE,WH,M['RoofDark'],3)
b35_finish(m,'92379296')

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
# The cameras keep their measured distance from the modelled facade (0.355 m proud of the OSM line):
# the registered track at y -73.56 moves 0.355 m north.
block35_cameras=[
 sv_camera('197_Block35_Cal_Wood',-113.22,-73.205,2.24,152,0),
 sv_camera('198_Block35_Cal_Wood_Roof',-113.22,-73.205,2.24,152,28),
 sv_camera('199_Block35_Cal_Palace',-133.42,-73.205,2.30,152,0),
 sv_camera('200_Block35_Cal_Palace_Roof',-133.42,-73.205,2.30,152,32),
 sv_camera('201_Block35_Cal_Palace_East',-113.22,-73.205,2.24,205,0),
 sv_camera('202_Block35_Cal_Palace_Pediment',-113.22,-73.205,2.24,212,25),
 sv_camera('203_Block35_Cal_Palace_Oblique',-133.42,-73.205,2.30,107,0),
 ('204_Block35_Aerial',(-112.0,-52.0,34.0),(-124.0,-86.0,6.0),28),
]
print('BLOCK35_GEOMETRY',len(block35_names))
