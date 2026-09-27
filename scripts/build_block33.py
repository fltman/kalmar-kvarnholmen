"""Pass 33: Södra Långgatan 16 (OSM 92379302), the corner house east of Kaggensgatan.

White render over a stone plinth. The ground floor: an open arcade behind the square corner pier on
both streets, shop windows between plain piers, round vents over the second shop, and the arched
carriage gate with a wrought-iron gate in the risalit. Above a moulded band a console frieze under
the first-floor windows; window heads on consoles, segmental pediments over the middle window of
each wing; small heads over the second-floor windows; a frieze and a dentilled cornice; rusticated
quoins at the corner and the east end. The risalit (0.3 m proud, quoin strips): paired pilasters
with capitals round the first-floor window, an entablature, a medallion in a segmental frame, the
second-floor window and a pediment above the cornice. References: Google Street View April 2025
(registered on the corner and the east joint), view only. Zones: source/block33.json; see
references/block33-notes.md. Tenant signs and awnings are omitted.
"""
B33D=json.loads((R/'source/block33.json').read_text());Z=B33D['zones'];Z33=Z['sl16']
block33_names=[];B33={}
for old in [k for k in list(materials) if k.startswith('M_Block33_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('White','TownIvory',(.90,.89,.85),.88,0),
 ('Trim','TownIvory',(.94,.93,.90),.82,0),
 ('Frame','TownPaintBrown',(.55,.24,.20),.55,0),
 ('Plinth','TownStone',(.70,.68,.64),.84,0),
 ('RoofDark','TownMetalGrey',(.26,.27,.28),.55,.30),
 ('Iron','TownMetalGrey',(.08,.08,.09),.45,.30),
 ('Oak','TownPaintBrown',(.44,.28,.16),.58,0),
 ('Shade','TownStone',(.60,.59,.56),.86,0),
 ]:
 name='M_Block33_'+key;B33[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block33_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B33;WH,TR,FR,PL=M['White'],M['Trim'],M['Frame'],M['Plinth']
H=Z33['height'];BD=Z33['band'];FL=Z33['floors'];RS=Z33['risalit'];ARC=Z33['arcade']

def b33_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block33_names.append(name);return Mesh(name,category)
def b33_finish(m,osm):
 obj=s21_finish(m);obj['detail_pass']=33;obj['reference_notes']='references/block33-notes.md';obj['osm_way']=osm;return obj
def front33(w):
 ox,oy=outward(w)
 if w['kind']!='outer':return None
 if oy<-.9:return 'sodra'
 if ox<-.9:return 'kagg'
 return None
def up_window(m,x,y,u,b,w,h,a,head='cornice'):
 # Casement in a moulded surround; heads: a cornice on two consoles, a segmental pediment, or a
 # small moulded head (second floor).
 s20_window(m,x,y,u,b,w,h,a,FR,WH,.68,False)
 for s in (-1,1):facade_box(m,x,y,u+s*(w/2+.08),.39,b+h/2,.16,.07,h+.16,TR,a)
 facade_box(m,x,y,u,.40,b+h+.08,w+.32,.07,.16,TR,a)
 facade_box(m,x,y,u,.46,b-.06,w+.40,.20,.10,TR,a)
 for s in (-1,1):facade_box(m,x,y,u+s*(w/2+.10),.44,b-.22,.12,.14,.22,TR,a)
 if head in ('cornice','segment'):
  # Frieze with a festoon between two consoles and a central keystone over the window (7.35-7.92),
  # the moulded ledge (7.92-8.24) and on the middle axes a segmental pediment to 8.51.
  for s in (-1,1):facade_box(m,x,y,u+s*(w/2+.20),.43,b+h+.33,.14,.16,.46,TR,a)
  facade_box(m,x,y,u,.42,b+h+.30,.22,.12,.44,TR,a)
  town_path(m,[lp(x,y,u+(w/2)*(2*k/8-1),.42,b+h+.44-.14*math.sin(math.pi*k/8),a) for k in range(9)],.035,TR)
  facade_box(m,x,y,u,.44,b+h+.63,w+.50,.18,.12,TR,a);facade_box(m,x,y,u,.49,b+h+.79,w+.70,.28,.20,TR,a)
  if head=='segment':
   k=12;r=(w+.7)/2;rise=.27
   R_=(r*r+rise*rise)/(2*rise);t0=math.asin(r/R_);zc=b+h+.89+rise-R_
   arc=[(u+R_*math.sin(-t0+2*t0*i/k),zc+R_*math.cos(-t0+2*t0*i/k)) for i in range(k+1)]
   outline=[(u-r,b+h+.89),(u+r,b+h+.89)]+arc[::-1][1:-1];n=len(outline)   # the arc's ends are the base corners
   vs=[lp(x,y,uu,o,zz,a) for o in (.36,.56) for uu,zz in outline]
   m.faces(vs,[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],TR)
 else:
  facade_box(m,x,y,u,.44,b+h+.26,w+.40,.16,.10,TR,a);facade_box(m,x,y,u,.42,b+h+.42,.34,.08,.22,TR,a)
def cornice33(m,x,y,L,a,ztop,o0=0.0):
 # The main cornice, triangulated: dentils 11.65-11.79 (0.03-0.29 m out), a bed moulding, the
 # corona 0.8 m out and its cymatium with the top at 11.91. o0 shifts it with a wall standing proud.
 n=round(L/.30)
 for k in range(n):facade_box(m,x,y,-L/2+(k+.5)*L/n,o0+.51,ztop-.19,.13,.26,.14,TR,a)
 facade_box(m,x,y,0,o0+.355+.05,ztop-.19,L,.10,.14,TR,a)
 facade_box(m,x,y,0,o0+.355+.23,ztop-.25,L+.10,.46,.06,TR,a)
 facade_box(m,x,y,0,o0+.355+.40,ztop-.12,L+.30,.80,.16,TR,a)
 facade_box(m,x,y,0,o0+.355+.425,ztop-.02,L+.34,.85,.04,TR,a)
def quoin_strip(m,x,y,u,z0,z1,a,side):
 quoins(m,x,y,u,z0,z1,a,TR,side,.46,.95,.60)
def plinth33(m,x,y,L,a,gaps):
 at=-L/2
 for l,r in sorted(gaps)+[(L/2,L/2)]:
  if l>at+.02:facade_box(m,x,y,(at+l)/2,.40,.30,l-at,.10,.60,PL,a)
  at=max(at,r)
def storeys33(m,x,y,L,a,S,wins,peds,segs_at=()):
 # Band, console frieze, the two window storeys, the frieze and the dentilled cornice.
 for s_ in wins:
  u=S(s_);up_window(m,x,y,u,FL[0][0],1.07,FL[0][1]-FL[0][0],a,'segment' if s_ in peds else 'cornice')
  up_window(m,x,y,u,FL[1][0],1.07,FL[1][1]-FL[1][0],a,'small')
  # Console frieze panel under the first-floor window.
  facade_box(m,x,y,u,.38,5.05,1.25,.06,.60,TR,a)
  for sg in (-1,1):facade_box(m,x,y,u+sg*.85,.41,5.10,.16,.12,.70,TR,a)
 facade_box(m,x,y,0,.39,(BD[0]+BD[1])/2,L,.10,BD[1]-BD[0],TR,a);p18_band(m,x,y,L+.2,BD[1]-.08,a,TR,.30)
 cornice33(m,x,y,L+.4,a,H+.01)

m=b33_new('SM_Kvarnholmen_House_92379302','Kvarnholmen/Södra Långgatan north')
for w in walls('sl16'):
 x,y,L,a=sf_edge(w['p'],w['q']);fr=front33(w)
 if fr is None:
  bz_wall(m,w['p'],w['q'],w['z0'],H,[],WH);continue
 if fr=='sodra':
  S=lambda s:-L/2+s                                  # s from the corner (the wall runs west to east)
  ru0,ru1=S(RS['s'][0]),S(RS['s'][1]);rc=(ru0+ru1)/2
  gf=[(S((ARC[0]+ARC[1])/2),0,ARC[1]-ARC[0],4.10,0),(S(5.32),.67,3.52,2.53,0),(S(10.31),.67,3.51,2.53,0),
      (S(19.79),.67,3.19,2.57,0),(S(22.91),.67,1.37,2.57,0),(S(24.90),0,.94,3.28,0),(S(27.0),.67,1.90,2.57,0)]
  up=[(S(s_),b,1.07,t-b,0) for s_ in Z33['sodra_windows'] for b,t in FL]
  bz_wall(m,w['p'],w['q'],0,H,gf+up+[(rc,0,ru1-ru0,H,0)],WH)
  for u,b,ww,hh,r in gf:
   if b==0 and ww>1.2:continue                        # the arcade opening
   if b==0:s20_door(m,x,y,u,b,ww,hh,a,M['Oak'])
   else:s21_glass(m,x,y,u,b,ww,hh,a,FR,max(1,round(ww/1.3)),.80,False)
  # Round vents over the second shop window.
  for k in range(4):
   uu=S(9.25+k*.72);kk=16
   m.faces([lp(x,y,uu+.19*math.cos(t*math.tau/kk),.32,3.90+.19*math.sin(t*math.tau/kk),a) for t in range(kk)],[tuple(range(kk))],M['Iron'])
   town_path(m,[lp(x,y,uu+.22*math.cos(t*math.tau/kk),.38,3.90+.22*math.sin(t*math.tau/kk),a) for t in range(kk+1)],.03,TR)
  plinth33(m,x,y,L,a,[(u-ww/2-.02,u+ww/2+.02) for u,b,ww,hh,r in gf if b<.6]+[(ru0,ru1)])
  storeys33(m,x,y,L,a,S,Z33['sodra_windows'],Z33['sodra_pediments'])
  quoin_strip(m,x,y,-L/2+.01,.6,H-.40,a,1);quoin_strip(m,x,y,L/2-.01,.6,H-.40,a,-1)
  # Risalit, 0.3 m proud: quoin strips, the gate, paired pilasters, the medallion and the pediment.
  pr=RS['proud'];rw=ru1-ru0;g0,g1=S(RS['gate'][0]),S(RS['gate'][1]);gc=(g0+g1)/2;gw=g1-g0
  p0=lp(x,y,ru0,pr,0,a)[:2];p1=lp(x,y,ru1,pr,0,a)[:2]
  RW=RS['windows'];rholes=[(gc-rc,0,gw,3.78-gw/2,gw/2),(0,RW[0][0],1.10,RW[0][1]-RW[0][0],0),(0,RW[1][0],1.10,RW[1][1]-RW[1][0],0)]
  bz_wall(m,p0,p1,0,H,[(u,b,ww,hh+r,0) for u,b,ww,hh,r in rholes],WH,.005,.355)
  for sg in (-1,1):facade_box(m,x,y,rc+sg*rw/2,(.005+.355+pr)/2,H/2,.02,pr+.35,H,WH,a)
  rx,ry,_=lp(x,y,rc,pr,0,a)
  spandrels(m,rx,ry,gc-rc,0,gw,3.78-gw/2,gw/2,a,WH)
  # The gate: an iron grille under a fanlight in an arched stone surround with a keystone.
  # The gate stands shallow in its opening (no deep reveal shows in the oblique views).
  facade_box(m,rx,ry,gc-rc,.12,1.55,gw,.06,3.10,M['Iron'],a)
  for k in range(15):
   uu=gc-rc-gw/2+.08+k*(gw-.16)/14;hh_=3.78-gw/2+gw/2*math.sqrt(max(0,1-(2*(uu-(gc-rc))/gw)**2))-.06
   town_rod(m,lp(rx,ry,uu,.20,.05,a),lp(rx,ry,uu,.20,hh_,a),.016,M['Iron'],6)
  # Moulded surround 0.40 m wide (0.37-0.50 m in the frontal view): flat jambs and a flat arch band
  # with an edge moulding, the keystone and a console either side at the springing.
  zs=3.78-gw/2
  for sg in (-1,1):facade_box(m,rx,ry,gc-rc+sg*(gw/2+.25),.40,zs/2,.40,.08,zs,TR,a)
  # The arch band is narrower than the jambs: its crown reaches 4.1 (the frontal view).
  p18_arch(m,rx,ry,zs,gw+.10,gw/2+.05,.28,.40,a,TR,20)
  town_path(m,[lp(rx,ry,gc-rc+(gw/2+.34)*math.cos(math.pi*t/20),.46,zs+(gw/2+.34)*math.sin(math.pi*t/20),a) for t in range(21)],.04,TR)
  facade_box(m,rx,ry,gc-rc,.48,zs+gw/2+.17,.34,.12,.30,TR,a)
  for sg in (-1,1):facade_box(m,rx,ry,gc-rc+sg*(gw/2+.25),.46,zs+.10,.50,.14,.20,TR,a)
  facade_box(m,rx,ry,0,.39,.30,rw,.10,.60,PL,a)
  for sg in (-1,1):quoin_strip(m,rx,ry,sg*(rw/2-.01),.6,H-.40,a,-sg)
  # First floor: the window between paired pilasters with capitals, the entablature broken by the
  # medallion, the segmental frame over it, the second-floor window.
  RW=RS['windows'];EN=RS['entablature'];MZ=RS['medallion']
  s20_window(m,rx,ry,0,RW[0][0],1.10,RW[0][1]-RW[0][0],a,FR,WH,.68,False)
  for sg in (-1,1):
   for k in (0,1):pilaster(m,rx,ry,sg*(.95+k*.38),4.75,RS['capitals_top']-.64,.30,a,TR,TR)
  for sg in (-1,1):
   uc_=sg*1.03;facade_box(m,rx,ry,uc_,.42,EN[0]+.10,1.05,.14,.20,TR,a);facade_box(m,rx,ry,uc_,.47,(EN[0]+.20+EN[1])/2,1.15,.26,EN[1]-EN[0]-.20,TR,a)
  k=16;crest=[(1.05*math.cos(math.pi*i/k),EN[1]+(RS['frame_top']-EN[1])*math.sin(math.pi*i/k)) for i in range(k+1)]
  town_path(m,[lp(rx,ry,uu,.44,zz,a) for uu,zz in crest],.08,TR)
  kk=20;m.faces([lp(rx,ry,.36*math.cos(t*math.tau/kk),.40,MZ+.36*math.sin(t*math.tau/kk),a) for t in range(kk)],[tuple(range(kk))],TR)
  town_path(m,[lp(rx,ry,.40*math.cos(t*math.tau/kk),.44,MZ+.40*math.sin(t*math.tau/kk),a) for t in range(kk+1)],.04,TR)
  for t in range(8):ang=t*math.pi/4;town_rod(m,lp(rx,ry,.08*math.cos(ang),.43,MZ+.08*math.sin(ang),a),lp(rx,ry,.30*math.cos(ang),.43,MZ+.30*math.sin(ang),a),.03,TR,6)
  s20_window(m,rx,ry,0,RW[1][0],1.10,RW[1][1]-RW[1][0],a,FR,WH,.68,False);facade_box(m,rx,ry,0,.46,RW[1][0]-.06,1.50,.20,.10,TR,a)
  facade_box(m,rx,ry,0,.44,RW[1][1]+.28,1.50,.16,.12,TR,a)
  facade_box(m,rx,ry,0,.39,(BD[0]+BD[1])/2,rw,.10,BD[1]-BD[0],TR,a);p18_band(m,rx,ry,rw+.2,BD[1]-.08,a,TR,.30)
  cornice33(m,rx,ry,rw+.5,a,H+.01)
  # The pediment stands on the corona, 0.8 m out; the apex (the raking moulding's top) at 12.99.
  pw=RS['pediment_width'];zb=H+.02;rise=RS['apex']-.18-zb
  gable_front(m,rx,ry,0,zb,pw,rise,a,WH,TR,.46,.84,False)
  gable_behind(m,rx,ry,0,zb,pw,rise,a,M['RoofDark'],3.0)
 else:
  S=lambda s:L/2-s                                   # s from the corner (the wall runs north to south)
  gf=[(S((ARC[0]+ARC[1])/2),0,ARC[1]-ARC[0],4.10,0),(S(4.60),.67,2.60,2.53,0),(S(8.00),.67,2.60,2.53,0),(S(11.10),0,1.10,3.10,0),
      (S(14.20),.67,2.80,2.53,0),(S(18.00),.67,2.80,2.53,0),(S(21.60),.67,2.40,2.53,0)]
  up=[(S(s_),b,1.07,t-b,0) for s_ in Z33['kagg_windows'] for b,t in FL]
  bz_wall(m,w['p'],w['q'],0,H,gf+up,WH)
  for u,b,ww,hh,r in gf:
   if b==0 and ww>1.2:continue
   if b==0:s20_door(m,x,y,u,b,ww,hh,a,M['Oak'])
   else:s21_glass(m,x,y,u,b,ww,hh,a,FR,max(1,round(ww/1.3)),.80,False)
  plinth33(m,x,y,L,a,[(u-ww/2-.02,u+ww/2+.02) for u,b,ww,hh,r in gf if b<.6])
  storeys33(m,x,y,L,a,S,Z33['kagg_windows'],Z33['kagg_pediments'])
  quoin_strip(m,x,y,L/2-.01,.6,H-.40,a,-1)
  ud=S(Z33['kagg_downpipe']);town_rod(m,lp(x,y,ud,.46,.30,a),lp(x,y,ud,.46,H-.30,a),.055,M['Shade'],8)
# The arcade behind the corner pier (1.2 m square): open 1.2-2.69 m from the corner on both streets,
# 1.5 m deep, with the pier's inner faces, the end and back walls and a ceiling at the band.
cx,cy=-181.42,-68.38;a0,a1,dep=ARC
sx,sy=.99998,-.0061;kx,ky=.0048,1.0          # unit vectors along Södra Långgatan (east) and Kaggensgatan (north)
def P2(s,t):return (cx+sx*s+kx*t,cy+sy*s+ky*t)
for (s0,t0),(s1,t1) in (((a1,0),(a1,dep)),((a1,dep),(dep,dep)),((dep,dep),(dep,a1)),((dep,a1),(0,a1)),((0,a0),(a0,a0)),((a0,a0),(a0,0))):
 bz_wall(m,P2(s0,t0),P2(s1,t1),0,4.10,[],WH,-.10,.10)
ring_=[P2(a0,0),P2(a1,0),P2(a1,dep),P2(dep,dep),P2(dep,a1),P2(0,a1),P2(0,a0),P2(a0,a0)]
m.faces([(*p,4.10) for p in ring_],[tuple(range(len(ring_)))],WH)
m.faces([(*p,.02) for p in reversed(ring_)],[tuple(range(len(ring_)))],PL)
sl=roof32(m,'sl16',M['RoofDark'],WH)
b33_finish(m,'92379302')

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
# The cameras keep their measured distance from the modelled facade (0.355 m proud of the OSM line).
block33_cameras=[
 sv_camera('184_Block33_Cal_West',-174.91,-73.96,2.34,332,0),
 sv_camera('185_Block33_Cal_West_Roof',-174.91,-73.96,2.34,332,32),
 sv_camera('186_Block33_Cal_East',-164.24,-74.10,2.34,332,0),
 sv_camera('187_Block33_Cal_East_Roof',-164.24,-74.10,2.34,332,32),
 sv_camera('188_Block33_Corner',-185.24,-73.5,2.10,20,10),
 ('189_Block33_Aerial',(-150.0,-100.0,40.0),(-168.0,-58.0,6.0),28),
]
print('BLOCK33_GEOMETRY',len(block33_names))
