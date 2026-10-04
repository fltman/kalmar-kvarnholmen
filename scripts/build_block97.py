"""Pass 97: six scattered pass-17 volumes on Norra Långgatan and Östra Sjögatan:
- 91970395 (Norra Långgatan 37): the beige boarded two-storey house with its gable to the street,
  three windows a floor in white surrounds, a small window in the gable, a dark plinth; the wide
  rear part is not seen (plain walls, flat roof, estimated);
- 91970343 (Östra Sjögatan 22): the yellow boarded one-and-a-half-storey gable house, three ground
  windows and two upper windows reaching into the gable, white corner boards and a dark plinth; the
  low annex at the back is not seen (estimated);
- 91885535: its street piece is the north end of the cream rendered house of pass 62, flush with
  it and with the ochre house of pass 64 (the strip in front of the recessed OSM wall is added):
  two pairs of round-headed windows over arched cellar hatches, two upper windows, the string
  course, the corbel frieze and the cornice in pass 62's measures; the long wing behind is not seen;
- 91885540 (Norra Långgatan 43): the beige rendered 1950s block, semi-basement windows and three
  floors of two-light windows on a 2.1 m rhythm, the entrance with a flat canopy, a hipped roof;
- 91926309 (Norra Långgatan 47): the cream neoclassical house: a dark stone plinth, a rusticated
  base, eight tall round-headed windows with archivolts and impost bands, a double string course,
  eight upper windows under cornice hoods, corner pilasters, a frieze and a dentil cornice, a low
  hipped roof; the rear wing is not seen;
- 91926329 (Norra Långgatan 55): the cream boarded two-storey house with pilaster strips, the
  double door, window awnings, and a red metal mansard roof with roof lights; the east part of the
  front and the east wing behind are estimated.

References: Google Street View (seven views from six panoramas, resected on house corners, on the
ochre house's corner and pass 62's storey heights), view only. Zones: source/block97.json; see
references/block97-notes.md. Signs, lamps, downpipes, the fences and the neighbours are omitted.
"""
B97D=json.loads((R/'source/block97.json').read_text());Z=B97D['zones']
block97_names=[];B97={}
for old in [k for k in list(materials) if k.startswith('M_Block97_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Beige','TownIvory',(.78,.75,.66),.82,0),('Yellow','TownIvory',(.90,.79,.50),.82,0),('White','TownPaintWhite',(.94,.94,.92),.55,0),
 ('Plinth','TownStone',(.27,.27,.28),.90,0),('Sheet','TownMetalGrey',(.34,.35,.36),.55,.30),('Dark','TownMetalGrey',(.05,.055,.06),.40,.20),
 ('Cream','TownIvory',(.90,.87,.78),.92,0),('CreamTrim','TownIvory',(.93,.91,.84),.86,0),('RedFrame','TownPaintBrown',(.45,.15,.12),.55,0),
 ('Hatch','TownPaintBrown',(.55,.18,.14),.60,0),('BrownRoof','TownMetalGrey',(.40,.20,.16),.55,.30),
 ('Render','TownIvory',(.84,.80,.71),.92,0),('RenderTrim','TownIvory',(.89,.86,.79),.88,0),('Canopy','TownMetalGrey',(.55,.56,.56),.55,.30),
 ('Neo','TownIvory',(.90,.84,.70),.90,0),('NeoTrim','TownIvory',(.93,.89,.78),.86,0),('NeoStone','TownStone',(.33,.31,.29),.92,0),
 ('NeoFrame','TownPaintWhite',(.84,.84,.80),.55,0),
 ('Board','TownIvory',(.87,.85,.75),.82,0),('BoardTrim','TownPaintWhite',(.92,.91,.85),.60,0),('GreenFrame','TownPaintGreen',(.66,.70,.60),.60,0),
 ('DoorGreen','TownPaintGreen',(.74,.78,.64),.60,0),('Foundation','TownStone',(.88,.88,.86),.88,0),('RedMetal','TownMetalGrey',(.62,.15,.13),.50,.30),
 ]:
 name='M_Block97_'+key;B97[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block97_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B97;WF=M['White']

def b97_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block97_names.append(name);return Mesh(name,category)
def drop_degenerate_faces97(obj,tol=1e-9):
 import bmesh
 bm=bmesh.new();bm.from_mesh(obj.data)
 def _thin(f):
  L=max(e.calc_length() for e in f.edges);return L>0 and 2*f.calc_area()/L<1e-4
 bad=[f for f in bm.faces if f.calc_area()<tol or len({v.index for v in f.verts})<len(f.verts) or _thin(f)]
 block97_samples[obj.name]=[tuple(round(c,2) for c in f.calc_center_median()) for f in bad[:4]]
 if bad:bmesh.ops.delete(bm,geom=bad,context='FACES_ONLY')
 bm.to_mesh(obj.data);bm.free();obj.data.update();return len(bad)
block97_dropped={};block97_samples={}
def b97_finish(m,osm):
 obj=s21_finish(m);block97_dropped[obj.name]=drop_degenerate_faces97(obj)
 obj['detail_pass']=97;obj['reference_notes']='references/block97-notes.md';obj['osm_way']=osm;return obj

# Street frames: s along the OSM front line from A to B, t outwards (towards the street); the
# facade surfaces stand at t = 0.355.
def fr97(A,B):
 L=math.dist(A,B);D=((B[0]-A[0])/L,(B[1]-A[1])/L);return dict(A=A,B=B,D=D,N=(D[1],-D[0]),L=L,ang=math.atan2(D[1],D[0]))
def P97(f,s,t=0,z=None):
 p=(f['A'][0]+f['D'][0]*s+f['N'][0]*t,f['A'][1]+f['D'][1]*s+f['N'][1]*t);return p if z is None else (*p,z)
def rect97(f,zone):
 pts=[v for g in Z[zone]['polygons'] for v in g];A,D,N=f['A'],f['D'],f['N']
 ss=[(v[0]-A[0])*D[0]+(v[1]-A[1])*D[1] for v in pts];ts=[(v[0]-A[0])*N[0]+(v[1]-A[1])*N[1] for v in pts]
 return min(ss),max(ss),min(ts),max(ts)
def prism97(m,f,outline,t0,t1,ma):
 # A closed prism with an (s, z) outline between depths t0 < t1. The frame is left-handed
 # (t to the right of s), so the windings are reversed against pass 95's prism.
 n=len(outline);vs=[P97(f,s,t,z) for t in (t0,t1) for s,z in outline]
 m.faces(vs,[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],ma)
def gable97(m,f,zone,wall,roof,trim,srange,ov=.30,eave=.40):
 # Gable to the street: the ridge runs back from the street over the zone's boxed outline; gable
 # prisms in the wall material on the street front and at the back, bargeboards, gutters.
 s0,s1,t0,t1=rect97(f,zone);s0,s1=srange
 H=Z[zone]['height'];T=Z[zone]['top'];o=.355;sL,sR=s0-o,s1+o;sm=(sL+sR)/2;sl=(T-H)/(sm-sL)
 tf,tb=t1+o+ov,t0-o-ov
 for se,sg in ((sL,-1),(sR,1)):
  e=se+sg*eave;ze=H-eave*sl
  m.faces([P97(f,e,tb,ze+.12),P97(f,sm,tb,T+.12),P97(f,sm,tf,T+.12),P97(f,e,tf,ze+.12)],[(0,1,2,3),(3,2,1,0)],roof)
  town_rod(m,P97(f,e,tb,ze+.02),P97(f,e,tf,ze+.02),.07,M['Sheet'],8)
  for tt in (tf-.02,tb+.02):town_path(m,[P97(f,e,tt,ze+.08),P97(f,sm,tt,T+.08)],.07,trim)
 g=[(sL,H),(sR,H),(sm,T-.02)]
 prism97(m,f,g,t1+.005,t1+o,wall);prism97(m,f,g,t0-o,t0-.005,wall)
 return sL,sR,sm,t1+o
def gable_boards97(m,f,sL,sR,sm,H,T,tface,holes,ma,step=.22):
 # Vertical boards on a street gable, clipped to the rakes and broken at the windows (s, b, w, h).
 n=int((sR-sL)/step)
 for k in range(1,n):
  s=sL+k*(sR-sL)/n;z1=H+(T-H)*(1-abs(s-sm)/(sm-sL))-.12;segs=[(H,z1)]
  for hs,hb,hw,hh in holes:
   if abs(s-hs)<hw/2+.12:segs=[(l0,h0) for l,h_ in segs for l0,h0 in ((l,min(h_,hb-.12)),(max(l,hb+hh+.12),h_)) if h0-l0>.05]
  for l0,h0 in segs:m.box(P97(f,s,tface+.02,(l0+h0)/2),(.035,.03,h0-l0),ma,f['ang'])
def win97(m,x,y,u,b,w,h,a,frame,trim,rows=None,bw=.12,o=.16):
 cas81(m,x,y,u,b,w,h,a,frame,o,rows or (2 if h<1.1 else 3));surround36(m,x,y,u,b,w,h,a,trim,bw,.40)
 facade_box(m,x,y,u,.47,b-.05,w+2*bw,.16,.06,trim,a)
def slabwin97(m,x,y,u,b,w,h,a,frame,trim):
 # A window reaching above the eaves, standing on the gable prism's face (0.355 out).
 facade_box(m,x,y,u,.365,b+h/2,w,.02,h,GLAZE,a);cas81(m,x,y,u,b,w,h,a,frame,.40,2 if h<1.1 else 3)
 surround36(m,x,y,u,b,w,h,a,trim,.12,.42);facade_box(m,x,y,u,.50,b-.05,w+.24,.16,.06,trim,a)
def arc97(m,x,y,u,a,spring,half,rise,o,r,ma,n=12):
 pts=[(u-half,spring)]+[(u-half*math.cos(math.pi*k/n),spring+rise*math.sin(math.pi*k/n)) for k in range(1,n)]+[(u+half,spring)]
 town_path(m,[lp(x,y,uu,o,zz,a) for uu,zz in pts],r,ma)
def archglass97(m,x,y,u,a,spring,half,rise,o,n=16):
 pts=[lp(x,y,u+half*math.cos(math.pi*k/n),o,spring+rise*math.sin(math.pi*k/n),a) for k in range(n+1)]
 m.faces(pts,[tuple(range(n+1)),tuple(range(n,-1,-1))],GLAZE)
def cas97(m,x,y,u,b,w,h,a,frame,o=.18,trans=.72):
 # Pass 62's casement (two lights and a transom), in this pass's frame colour.
 facade_box(m,x,y,u,o-.04,b+h/2,w,.02,h,GLAZE,a)
 for q in (-w/2+.04,w/2-.04,0):facade_box(m,x,y,u+q,o,b+h/2,.08 if q else .07,.08,h,frame,a)
 for zz in (b+.04,b+h-.04,b+h*trans):facade_box(m,x,y,u,o,zz,w,.08,.06,frame,a)
def front97(w,f):
 ox,oy=outward(w);return w['kind']=='outer' and ox*f['N'][0]+oy*f['N'][1]>.9
def mine97(w,f,ops):
 # Openings (kind, s, bottom, width, height[, rise]) that lie on wall w, as (kind, u, ...).
 x,y,L,a=sf_edge(w['p'],w['q']);out=[]
 for op in ops:
  u=U(w,*P97(f,op[1]))
  if abs(u)+op[3]/2<=L/2+.01:out.append((op[0],u)+tuple(op[2:]))
 return out
def rear97(m,zone,wall,frame,trim,levels,floor0=.9):
 # Unseen walls: plain casements (pass 26's courtyard fronts), or blank above a neighbour.
 H=Z[zone]['height']
 for w in walls(zone):
  if w['kind']!='outer':bz_wall(m,w['p'],w['q'],w['z0'],H,[],wall);continue
  plain(m,w,H,wall,frame,trim,levels,floor0)
def flat97(m,zone,wall,cap):
 # A flat roof with a low upstand along the outer walls (the unseen rear parts).
 H=Z[zone]['height'];T=Z[zone]['top']
 for g in Z[zone]['polygons']:m.faces([(*v,H+.02) for v in g],[tuple(range(len(g))),tuple(range(len(g)-1,-1,-1))],M['Sheet'])
 for w in walls(zone):
  x,y,L,a=sf_edge(w['p'],w['q']);facade_box(m,x,y,0,.30,(H+T)/2,L+.1,.14,T-H,wall,a);facade_box(m,x,y,0,.30,T+.02,L+.14,.20,.04,cap,a)
def mansard97(m,zone,A,B,ma,brk,inset=2.0,ov=.70):
 # A mansard over the boxed outline: a steep lower ring to the break, a low hip above.
 r,Ls,Lt=rect82(zone,A,B);H=Z[zone]['height'];T=Z[zone]['top']
 outer,inner=inset_roof(m,r,H,inset,brk-H,ma,ov)
 inset_roof(m,inner,brk,min(Ls,Lt)/2-inset-.25,T-brk,ma,.0)
 return (brk-H)/(inset+ov)

meshes={}
for zone,spec in Z.items():
 nm=spec['mesh']
 if nm not in meshes:meshes[nm]=b97_new(nm,'Kvarnholmen/Norra Långgatan' if zone in ('nf','nr','bl','nm','nw','sr','sw') else 'Kvarnholmen/Östra Sjögatan')

# ---------------------------------------------------------------- 91970395, the beige gable house
F_N=fr97((11.743,73.735),(18.612,73.652))
m=meshes[Z['nf']['mesh']];H=Z['nf']['height'];T=Z['nf']['top'];BG=M['Beige'];PZ=.44
OPS=[('win',s,1.37,.95,1.50) for s in (1.26,3.26,5.26)]+[('win',s,4.23,.95,1.53) for s in (1.30,3.26,5.24)]
for w in walls('nf'):
 if w['kind']!='outer':bz_wall(m,w['p'],w['q'],w['z0'],H,[],BG);continue
 x,y,L,a=sf_edge(w['p'],w['q'])
 if not front97(w,F_N):plain(m,w,H,BG,WF,WF,2,.9);continue
 mine=mine97(w,F_N,OPS);holes=[(u,b,ww,hh,0) for k,u,b,ww,hh in mine]
 bz_wall(m,w['p'],w['q'],0,H,holes,BG);boards82(m,x,y,L,a,PZ+.02,H-.08,holes,BG)
 for k,u,b,ww,hh in mine:win97(m,x,y,u,b,ww,hh,a,WF,WF)
 facade_box(m,x,y,0,.39,PZ/2,L+.02,.08,PZ,M['Plinth'],a)
 for uu in (-L/2+.09,L/2-.09):facade_box(m,x,y,uu,.42,(H+PZ)/2,.18,.10,H-PZ,WF,a)
sL,sR,sm,tface=gable97(m,F_N,'nf',BG,M['Sheet'],WF,(0,F_N['L']))
gable_boards97(m,F_N,sL,sR,sm,H,T,tface,[(3.26,7.0,.60,.75)],BG)
w0={'p':list(F_N['A']),'q':list(F_N['B'])};x,y,L,a=sf_edge(F_N['A'],F_N['B'])
slabwin97(m,x,y,U(w0,*P97(F_N,3.26)),7.0,.60,.75,a,WF,WF)
rear97(m,'nr',BG,WF,WF,2);flat97(m,'nr',BG,M['Sheet'])
b97_finish(m,'91970395')

# ---------------------------------------------------------------- 91970343, the yellow gable house
F_Y=fr97((48.501,90.442),(48.548,97.389))
m=meshes[Z['ym']['mesh']];H=Z['ym']['height'];T=Z['ym']['top'];YE=M['Yellow'];PZ=.57
OPS=[('win',s,1.34,1.0,1.55) for s in (1.66,3.74,5.78)]+[('slab',s,3.94,1.0,1.82) for s in (2.58,4.75)]
for w in walls('ym'):
 if w['kind']!='outer':bz_wall(m,w['p'],w['q'],w['z0'],H,[],YE);continue
 x,y,L,a=sf_edge(w['p'],w['q'])
 if not front97(w,F_Y):plain(m,w,H,YE,WF,WF,1,.9);continue
 mine=mine97(w,F_Y,OPS);low=[(u,b,ww,hh,0) for k,u,b,ww,hh in mine if k=='win']
 bz_wall(m,w['p'],w['q'],0,H,low,YE)
 boards82(m,x,y,L,a,PZ+.02,H-.08,low+[(u,b,ww,hh,0) for k,u,b,ww,hh in mine if k=='slab'],YE)
 for k,u,b,ww,hh in mine:
  if k=='slab':slabwin97(m,x,y,u,b,ww,hh,a,WF,WF)
  else:win97(m,x,y,u,b,ww,hh,a,WF,WF)
 facade_box(m,x,y,0,.39,PZ/2,L+.02,.08,PZ,M['Plinth'],a)
 for uu in (-L/2+.11,L/2-.11):facade_box(m,x,y,uu,.42,(H+PZ)/2,.22,.10,H-PZ,WF,a)
sL,sR,sm,tface=gable97(m,F_Y,'ym',YE,M['Sheet'],WF,(0,F_Y['L']),ov=.35,eave=.45)
gable_boards97(m,F_Y,sL,sR,sm,H,T,tface,[(s,3.94,1.0,1.82) for s in (2.58,4.75)],YE)
rear97(m,'ya',YE,WF,WF,1);flat97(m,'ya',YE,M['Sheet'])
b97_finish(m,'91970343')

# ---------------------------------------------------------------- 91885535, pass 62's north end
# Pass 62's measures (references/block62-notes.md), the axes from this pass's panorama.
F_C=fr97((59.73,108.64),(59.504,102.845))
m=meshes[Z['cr']['mesh']];H=Z['cr']['height'];CR=M['Cream'];TR=M['CreamTrim']
AX=(1.19,3.69)
for w in walls('cr'):
 if w['kind']!='outer':bz_wall(m,w['p'],w['q'],w['z0'],H,[],CR);continue
 x,y,L,a=sf_edge(w['p'],w['q']);S=lambda s:U(w,*P97(F_C,s))
 up=[(S(s),5.36,1.08,1.55,0) for s in AX];gf=[(S(s)+d*.52,2.02,.74,1.62,.30) for s in AX for d in (-1,1)]
 hat=[(S(s),.13,.95,.62,.15) for s in AX]
 bz_wall(m,w['p'],w['q'],0,H,up+gf+hat,CR)
 for u,b,ww,hh,r in up:
  cas97(m,x,y,u,b,ww,hh,a,M['RedFrame']);facade_box(m,x,y,u,.46,b-.06,ww+.30,.20,.08,TR,a);facade_box(m,x,y,u,.42,b+hh+.08,ww+.14,.10,.10,TR,a)
 for u,b,ww,hh,r in gf:cas97(m,x,y,u,b,ww,hh+r*.6,a,M['RedFrame'])
 for s in AX:
  u=S(s);arc97(m,x,y,u,a,3.64,1.02,.42,.41,.09,TR);facade_box(m,x,y,u,.40,2.8,.28,.08,1.6,TR,a)
 for u,b,ww,hh,r in hat:facade_box(m,x,y,u,.10,b+hh/2,ww,.06,hh+r,M['Hatch'],a);arc97(m,x,y,u,a,b+hh,ww/2+.10,r+.08,.41,.07,TR)
 facade_box(m,x,y,0,.38,.25,L,.06,.49,M['Plinth'],a)
 for k in range(1,4):facade_box(m,x,y,0,.37,.49+k*.30,L,.01,.02,TR,a)
 facade_box(m,x,y,0,.44,1.70,L,.14,.22,TR,a);facade_box(m,x,y,0,.42,4.91,L,.10,.16,TR,a)
 n=int(L/.62)
 for k in range(n):arc97(m,x,y,-L/2+(k+.5)*L/n,a,7.82,.28,.12,.40,.035,TR,6)
 facade_box(m,x,y,0,.40,7.78,L,.08,.04,TR,a)
 facade_box(m,x,y,0,.44,8.35,L,.12,.50,TR,a);facade_box(m,x,y,0,.56,8.75,L+.10,.36,.30,TR,a)
saddle82(m,'cr',F_C['A'],F_C['B'],M['BrownRoof'],CR,along=True,ov=.30)
rear97(m,'cb',CR,M['RedFrame'],TR,2);flat97(m,'cb',CR,M['Sheet'])
b97_finish(m,'91885535')

# ---------------------------------------------------------------- 91885540, the 1950s block
F_B=fr97((85.652,72.757),(121.713,72.331))
m=meshes[Z['bl']['mesh']];H=Z['bl']['height'];RD=M['Render'];RT=M['RenderTrim']
COLS=[1.23+2.1*k for k in range(17)];DOORK=5
OPS=[('base',s,.36,1.30,.72) for k,s in enumerate(COLS) if k!=DOORK]+[('win',s,b,1.35,1.50) for k,s in enumerate(COLS) for b in (2.23,5.03,7.80) if not (k==DOORK and b<3)]
OPS.append(('door',COLS[DOORK]+.25,0,1.60,2.80))
for w in walls('bl'):
 if w['kind']!='outer':bz_wall(m,w['p'],w['q'],w['z0'],H,[],RD);continue
 x,y,L,a=sf_edge(w['p'],w['q'])
 if not front97(w,F_B):plain(m,w,H,RD,WF,RT,3,2.0);continue
 mine=mine97(w,F_B,OPS)
 bz_wall(m,w['p'],w['q'],0,H,[(u,b,ww,hh,0) for k,u,b,ww,hh in mine],RD)
 for k,u,b,ww,hh in mine:
  if k=='door':
   facade_box(m,x,y,u,.05,b+hh/2,ww,.06,hh,M['Dark'],a);door83(m,x,y,u,b+.02,ww-.4,2.2,a,M['Canopy'],RT)
   facade_box(m,x,y,u,.10,2.6,ww,.04,.36,GLAZE,a);surround36(m,x,y,u,b,ww,hh,a,RT,.18,.40)
   facade_box(m,x,y,u,.355+.45,hh+.12,ww+.9,.90,.10,M['Canopy'],a);continue
  cas81(m,x,y,u,b,ww,hh,a,WF,.20,1);facade_box(m,x,y,u,.16,b+hh/2,.06,.08,hh,WF,a)
  surround36(m,x,y,u,b,ww,hh,a,RT,.10,.38);facade_box(m,x,y,u,.47,b-.04,ww+.20,.20,.05,M['Canopy'],a)
 facade_box(m,x,y,0,.38,.15,L,.05,.30,RT,a)
 facade_box(m,x,y,0,.40,H-.12,L+.05,.10,.24,RT,a)
hip82(m,'bl',F_B['A'],F_B['B'],M['Sheet'])
for s,t in ((9.0,-5.5),(27.0,-5.5)):X,Y=P97(F_B,s,t);chimney82(m,X,Y,Z['bl']['top']-.9,Z['bl']['top']+.6,M['Render'])
b97_finish(m,'91885540')

# ---------------------------------------------------------------- 91926309, the neoclassical house
F_M=fr97((131.976,61.876),(107.493,62.057))
m=meshes[Z['nm']['mesh']];H=Z['nm']['height'];NE=M['Neo'];NT=M['NeoTrim'];NF=M['NeoFrame']
BAYS=[F_M['L']/2+(k-3.5)*2.733 for k in range(8)]
AW,AB,AH,AR=1.52,2.76,2.15,.76;UW,UB,UH=1.15,7.57,1.78
for w in walls('nm'):
 if w['kind']!='outer':bz_wall(m,w['p'],w['q'],w['z0'],H,[],NE);continue
 x,y,L,a=sf_edge(w['p'],w['q'])
 if not front97(w,F_M):
  plain(m,w,H,NE,NF,NT,2,2.8);facade_box(m,x,y,0,.40,.25,L+.02,.10,.49,M['NeoStone'],a)
  facade_box(m,x,y,0,.60,11.30,L+.6,.70,.50,NT,a);continue
 us=[U(w,*P97(F_M,s)) for s in BAYS]
 holes=[(u,AB,AW,AH,AR) for u in us]+[(u,UB,UW,UH,0) for u in us]
 bz_wall(m,w['p'],w['q'],0,H,holes,NE)
 # The plinth and the rusticated base (courses as shallow grooves), the base cornice.
 facade_box(m,x,y,0,.42,.245,L+.02,.14,.49,M['NeoStone'],a)
 for k in range(1,5):facade_box(m,x,y,0,.37,.49+k*.37,L,.02,.03,NT,a)
 for k in range(5):
  for j in range(int(L/1.37)+1):
   uu=-L/2+(j+.5*(k%2))*1.37
   if -L/2+.1<uu<L/2-.1:facade_box(m,x,y,uu,.37,.49+(k+.5)*.37,.03,.02,.35,NT,a)
 facade_box(m,x,y,0,.44,2.40,L+.06,.18,.12,NT,a);facade_box(m,x,y,0,.48,2.51,L+.10,.26,.08,NT,a)
 for u in us:
  # Tall round-headed windows: glass, casement with transom, the arched light, archivolt, keystone.
  sp=AB+AH
  facade_box(m,x,y,u,.14,AB+AH/2,AW,.02,AH,GLAZE,a);archglass97(m,x,y,u,a,sp,AW/2,AR,.14)
  cas81(m,x,y,u,AB,AW,AH,a,NF,.18,3);facade_box(m,x,y,u,.18,sp+.03,AW,.08,.06,NF,a)
  arc97(m,x,y,u,a,sp,AW/2-.04,AR-.04,.18,.04,NF);facade_box(m,x,y,u,.18,sp+AR/2,.05,.06,AR,NF,a)
  arc97(m,x,y,u,a,sp,AW/2+.10,AR+.10,.42,.08,NT);facade_box(m,x,y,u,.45,sp+AR+.06,.24,.14,.30,NT,a)
  facade_box(m,x,y,u,.46,AB-.06,AW+.40,.22,.10,NT,a)
  # Upper windows under cornice hoods.
  cas81(m,x,y,u,UB,UW,UH,a,NF,.18,3);surround36(m,x,y,u,UB,UW,UH,a,NT,.12,.40)
  facade_box(m,x,y,u,.47,UB-.06,UW+.36,.20,.08,NT,a);facade_box(m,x,y,u,.40,UB+UH+.30,UW+.24,.06,.30,NT,a)
  facade_box(m,x,y,u,.52,UB+UH+.52,UW+.60,.30,.14,NT,a)
 # Impost band at the springing, broken by the arches; string courses; frieze and dentil cornice.
 edges=[-L/2]+[v for u in us for v in (u-AW/2-.14,u+AW/2+.14)]+[L/2]
 for lo,hi in zip(edges[0::2],edges[1::2]):
  if hi-lo>.05:facade_box(m,x,y,(lo+hi)/2,.42,AB+AH,hi-lo,.12,.12,NT,a)
 facade_box(m,x,y,0,.46,6.66,L+.06,.22,.14,NT,a);facade_box(m,x,y,0,.42,6.88,L+.04,.14,.10,NT,a)
 facade_box(m,x,y,0,.40,10.42,L,.10,.70,NT,a)
 facade_box(m,x,y,0,.47,10.95,L+.10,.24,.20,NT,a);facade_box(m,x,y,0,.62,11.30,L+.40,.54,.12,NT,a)
 for k in range(int(L/.26)):facade_box(m,x,y,-L/2+(k+.5)*L/int(L/.26),.58,11.17,.12,.18,.14,NT,a)
 facade_box(m,x,y,0,.80,11.58,L+.80,.90,.30,NT,a)
 for uu in (-L/2+.425,L/2-.425):
  facade_box(m,x,y,uu,.45,(2.55+10.85)/2,.85,.20,10.85-2.55,NT,a)
  for k in range(1,8):facade_box(m,x,y,uu,.56,2.55+k*(10.85-2.55)/8,.85,.02,.03,NE,a)
hip82(m,'nm',F_M['A'],F_M['B'],M['Sheet'])
rear97(m,'nw',NE,NF,NT,2,2.8)
hip82(m,'nw',(107.356,42.83),(107.278,31.958),M['Sheet'])
b97_finish(m,'91926309')

# ---------------------------------------------------------------- 91926329, the cream boarded house
F_S=fr97((162.323,73.229),(177.664,72.595))
m=meshes[Z['sr']['mesh']];H=Z['sr']['height'];BD=M['Board'];BT=M['BoardTrim'];GF=M['GreenFrame'];PZ=.55
WIN=(1.8,5.6,11.3,13.7);DOOR=8.4
OPS=[('win',s,1.41,1.05,1.45) for s in WIN]+[('win',s,3.98,1.0,1.22) for s in WIN+(DOOR,)]+[('door',DOOR,.30,1.70,2.15)]
PIL=(.15,3.6,7.5,9.3,12.5,F_S['L']-.15)
for w in walls('sr'):
 if w['kind']!='outer':bz_wall(m,w['p'],w['q'],w['z0'],H,[],BD);continue
 x,y,L,a=sf_edge(w['p'],w['q'])
 if not front97(w,F_S):plain(m,w,H,BD,GF,BT,2,.9);continue
 mine=mine97(w,F_S,OPS);holes=[(u,b,ww,hh,0) for k,u,b,ww,hh in mine]
 bz_wall(m,w['p'],w['q'],0,H,holes,BD);boards82(m,x,y,L,a,PZ+.02,H-.10,holes,BD)
 for k,u,b,ww,hh in mine:
  if k=='door':
   for sg in (-1,1):door83(m,x,y,u+sg*ww/4,b,ww/2-.04,hh,a,M['DoorGreen'],BT)
   facade_box(m,x,y,u,.46,b+hh+.15,ww+.5,.16,.14,BT,a);steps82(m,x,y,u,ww,b,a,M['Foundation']);continue
  win97(m,x,y,u,b,ww,hh,a,GF,BT,bw=.10)
  facade_box(m,x,y,u,.50,b+hh+.16,ww+.30,.10,.08,BT,a)
  if b>3 and U(w,*P97(F_S,1.8))-.1<u<U(w,*P97(F_S,5.6))+.1:awning82(m,x,y,u,b+hh+.02,ww+.3,a,WF,drop=.30,reach=.55)
 facade_box(m,x,y,0,.40,PZ/2,L+.04,.10,PZ,M['Foundation'],a);facade_box(m,x,y,0,.43,PZ+.06,L+.04,.10,.12,BT,a)
 for s in PIL:
  u=U(w,*P97(F_S,s))
  if abs(u)<=L/2:facade_box(m,x,y,max(-L/2+.15,min(L/2-.15,u)),.44,(PZ+H-.12)/2,.30,.12,H-.12-PZ,BT,a)
 facade_box(m,x,y,0,.46,H-.12,L+.1,.16,.24,BT,a)
# The steep lower slope: the gutter 0.35 m beyond the facade at 5.85 m, the break about 1 m inside
# the outline at 8.6 m (from the roof's top edge on the panorama, two parallel-line readings).
sl=mansard97(m,'sr',F_S['A'],F_S['B'],M['RedMetal'],8.60,inset=.95)
for s in (6.2,11.0):
 X,Y=P97(F_S,s,-.15);skylight82(m,X,Y,H+(.15+.70)*sl,F_S['ang'],sl)
rear97(m,'sw',BD,GF,BT,2)
mansard97(m,'sw',(170.642,81.36),(170.98,89.58),M['RedMetal'],8.60,inset=.95)
b97_finish(m,'91926329')

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block97_cameras=[
 sv_camera('476_Block97_Cal_Gable37',15.80,67.54,2.60,332,15,90),
 sv_camera('477_Block97_Cal_Yellow22',53.70,94.64,2.45,242,15,90),
 sv_camera('478_Block97_Cal_Neoclassical47',124.70,69.46,2.65,152,16,90),
 sv_camera('479_Block97_Cal_Boarded55',164.20,68.30,2.40,332,15,90),
 ('480_Block97_Aerial',(95.0,30.0,70.0),(95.0,85.0,2.0),24),
]
print('BLOCK97_GEOMETRY',len(block97_names),'dropped',block97_dropped,block97_samples)
