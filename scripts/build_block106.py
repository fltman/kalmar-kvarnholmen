"""Pass 106: the north side of Södra Långgatan from 60 Södra Långgatan to Sjöfartsmuseet, and the
south end of Landshövdingegatan:
- 91928568 (60 Södra Långgatan): a two-storey house with a rusticated cream ground floor on a dark
  plinth, an upper floor of red brick banded with cream stucco, segment-headed windows in red
  frames, a centre bay between pilasters with a round-headed window, a bracketed cornice, a low
  sheet roof with round-topped dormers and a brick aedicule over the centre; a lower back wing;
- 91928594 (the corner of Landshövdingegatan): an ochre roughcast two-storey house on a grey plinth,
  red window frames in light surrounds, the dark red door up steps in a stone surround, a saddle
  roof with a round-topped dormer and the gable with attic windows to Landshövdingegatan;
- 93199647: the grey boarded shed with the olive garage door and the blue Sjöfartsmuseum sign;
- 93199649 (Sjöfartsmuseet): a grey stucco neo-renaissance two-storey house: rusticated ground
  floor over a stone plinth, the entrance up steps, balustrade panels under round-headed upper
  windows between pilasters, frieze and deep bracketed cornice, a low hipped roof;
- 91928552: the light grey board wall with the red carved gate on Landshövdingegatan, the yard
  behind it under a flat roof and a tiled lean-to, and the courtyard ranges further west (not seen;
  plain ochre render, flat roofs);
- 91928587: a falu-red boarded house with a gambrel roof along Landshövdingegatan (seen only from
  the yard to the south; its street front is an estimate);
- 93199672: the long taupe stucco three-storey house: white window surrounds, a granite base, a
  thin cornice and a low hipped roof;
- 93199626: the pink stucco four-storey corner house with cream quoins, a tall stone base with
  basement windows, cream window surrounds and a low hipped roof.

References: Google Street View (seven panoramas, resected on house corners), view only. Zones:
source/block106.json; see references/block106-notes.md.
"""
B106D=json.loads((R/'source/block106.json').read_text());Z=B106D['zones']
block106_names=[];B106={}
for old in [k for k in list(materials) if k.startswith('M_Block106_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Brick','TownTileRed',(.50,.22,.17),.85,0),('Ashlar','TownStone',(.80,.75,.62),.88,0),('Band','TownIvory',(.86,.81,.68),.85,0),
 ('BkPlinth','TownStone',(.26,.25,.24),.90,0),('RedFrame','TownPaintBrown',(.45,.14,.11),.60,0),('DoorRed','TownPaintBrown',(.38,.10,.09),.60,0),
 ('Ochre','TownIvory',(.78,.66,.42),.92,0),('OcPlinth','TownStone',(.66,.66,.64),.90,0),('OcTrim','TownPaintWhite',(.86,.84,.78),.70,0),
 ('GreyBoard','TownPaintWhite',(.58,.58,.52),.80,0),('Olive','TownPaintGreen',(.30,.30,.24),.65,0),('Granite','TownStone',(.52,.44,.41),.90,0),
 ('SignBlue','TownPaintWhite',(.22,.45,.75),.50,0),
 ('MuStucco','TownIvory',(.74,.72,.65),.88,0),('MuTrim','TownPaintWhite',(.84,.83,.78),.75,0),('MuFrame','TownMetalGrey',(.24,.25,.23),.55,.10),
 ('MuDoor','TownPaintBrown',(.30,.25,.20),.60,0),('MuPlinth','TownStone',(.62,.61,.58),.90,0),
 ('YdBoard','TownPaintWhite',(.68,.68,.62),.80,0),('GateRed','TownPaintBrown',(.50,.13,.12),.60,0),('Lattice','TownPaintWhite',(.86,.84,.76),.60,0),
 ('YardRender','TownIvory',(.80,.70,.48),.92,0),('FaluRed','TownPaintBrown',(.56,.14,.12),.80,0),('WhiteFrame','TownPaintWhite',(.94,.94,.92),.55,0),
 ('Taupe','TownIvory',(.55,.52,.46),.92,0),('TpTrim','TownPaintWhite',(.88,.87,.83),.70,0),('DarkGranite','TownStone',(.33,.30,.29),.90,0),
 ('Pink','TownIvory',(.62,.45,.41),.92,0),('Quoin','TownIvory',(.86,.82,.70),.85,0),('PkBase','TownStone',(.60,.59,.56),.90,0),
 ('Sheet','TownMetalGrey',(.36,.37,.38),.55,.30),('SheetDark','TownMetalGrey',(.20,.20,.21),.55,.30),('SheetRed','TownMetalGrey',(.48,.20,.15),.55,.25),
 ('Tile','TownTileRed',(.66,.30,.21),.80,0),('Chimney','TownTileRed',(.55,.33,.27),.85,0),('Dark','TownMetalGrey',(.05,.055,.06),.40,.20),
 ]:
 name='M_Block106_'+key;B106[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block106_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M106=B106

def b106_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block106_names.append(name);return Mesh(name,category)
def drop_degenerate_faces106(obj,tol=1e-9):
 import bmesh
 bm=bmesh.new();bm.from_mesh(obj.data)
 def _thin(f):
  L=max(e.calc_length() for e in f.edges);return L>0 and 2*f.calc_area()/L<1e-4
 bad=[f for f in bm.faces if f.calc_area()<tol or len({v.index for v in f.verts})<len(f.verts) or _thin(f)]
 block106_samples[obj.name]=[tuple(round(c,2) for c in f.calc_center_median()) for f in bad[:4]]
 if bad:bmesh.ops.delete(bm,geom=bad,context='FACES_ONLY')
 bm.to_mesh(obj.data);bm.free();obj.data.update();return len(bad)
block106_dropped={};block106_samples={}
def b106_finish(m,osm):
 obj=s21_finish(m);block106_dropped[obj.name]=drop_degenerate_faces106(obj)
 obj['detail_pass']=106;obj['reference_notes']='references/block106-notes.md';obj['osm_way']=osm;return obj

# Street frames: a front from a to b, its outward side on the right of a->b; s along it from a,
# t inwards.
def frame106(F):a,b=F;L=math.dist(a,b);d=((b[0]-a[0])/L,(b[1]-a[1])/L);return d,(-d[1],d[0])
def P106(F,s,t=0,z=None):
 d,n=frame106(F);p=(F[0][0]+d[0]*s+n[0]*t,F[0][1]+d[1]*s+n[1]*t);return p if z is None else (*p,z)
def rect106(zone,F):
 d,n=frame106(F);pts=[v for g in Z[zone]['polygons'] for v in g]
 ss=[(v[0]-F[0][0])*d[0]+(v[1]-F[0][1])*d[1] for v in pts];ts=[(v[0]-F[0][0])*n[0]+(v[1]-F[0][1])*n[1] for v in pts]
 return min(ss),max(ss),min(ts),max(ts)
def ring106(F,s0,s1,t0,t1):
 # Counter-clockwise ring of the boxed outline (for inset_roof).
 r=[P106(F,s0,t0),P106(F,s1,t0),P106(F,s1,t1),P106(F,s0,t1)]
 area=sum(r[i][0]*r[(i+1)%4][1]-r[(i+1)%4][0]*r[i][1] for i in range(4));return r if area>0 else r[::-1]
def prism106(m,F,outline,t0,t1,ma):
 # A closed prism with an (s, z) outline in a street frame, between depths t0 and t1.
 n=len(outline);vs=[P106(F,s,t,z) for t in (t0,t1) for s,z in outline]
 m.faces(vs,[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],ma)
def hstrip106(m,x,y,L,a,z,h,holes,o,d,ma,gap=.10):
 # A horizontal band broken at the openings it crosses.
 cuts=sorted((hu-hw/2-gap,hu+hw/2+gap) for hu,hb,hw,hh,hr in holes if hb-.05<z<hb+hh+hr+.05);at=-L/2
 for lo,hi in cuts+[(L/2,L/2)]:
  lo=max(-L/2,min(L/2,lo))
  if lo>at+.05:facade_box(m,x,y,(at+lo)/2,o,z,lo-at,d,h,ma,a)
  at=max(at,min(L/2,hi))
def quoins106(m,x,y,u,side,a,z0,z1,ma,long=.70,short=.45,course=.40):
 z=z0;k=0
 while z<z1-.2:
  w=long if k%2==0 else short;facade_box(m,x,y,u+side*w/2,.40,z+course*.42,w,.10,course*.84,ma,a);z+=course;k+=1
def steps106(m,x,y,u,w,top,a,ma,reach=.70):
 # Short stone steps: most of the rise sits inside the door recess, only 'reach' projects.
 n=max(2,round(top/.18))
 for k in range(n):
  d=reach*(n-k)/n+.10;facade_box(m,x,y,u,.355+d/2-.05,(k+.5)*top/n,w+.30,d,top/n,ma,a)
def win106(m,x,y,u,b,w,h,a,frame,trim,bw=.12,rows=None):
 cas81(m,x,y,u,b,w,h,a,frame,.16,rows or (2 if h<1.0 else 3));surround36(m,x,y,u,b,w,h,a,trim,bw,.40)
 facade_box(m,x,y,u,.47,b-.05,w+.24,.16,.06,trim,a)
def roundtop106(m,F,s,t_front,depth,zb,w,h,body,roof,frame):
 # A round-topped dormer: a box body with a half-round top, extruded back from its front face
 # (t_front inwards of the street line), with a glazed front.
 r=w/2;prof=[(s-r,zb),(s+r,zb)]+[(s+r*math.cos(k*math.pi/12),zb+h+r*math.sin(k*math.pi/12)) for k in range(13)]
 prism106(m,F,prof,t_front,t_front+depth,body)
 town_path(m,[P106(F,s+(r+.04)*math.cos(k*math.pi/12),t_front-.04,zb+h+(r+.04)*math.sin(k*math.pi/12)) for k in range(13)],.06,roof)
 gl=[(s-r+.18,zb+.15),(s+r-.18,zb+.15)]+[(s+(r-.18)*math.cos(k*math.pi/12),zb+h+(r-.18)*math.sin(k*math.pi/12)) for k in range(13)]
 m.faces([P106(F,ss,t_front-.02,zz) for ss,zz in gl],[tuple(range(len(gl)))],GLAZE)
 town_rod(m,P106(F,s,t_front-.04,zb+.15),P106(F,s,t_front-.04,zb+h+r-.18),.035,frame,6)

# ---------------------------------------------------------------- the fronts and their openings
# kinds: win, arch (round-headed; r = rise), door, garage, gate, base (basement window).
# Positions: s along the front from its first point (m), bottom, width, height (and rise).
F_BK=((263.85,-72.13),(278.78,-72.43));F_OC=((278.78,-72.43),(294.04,-72.73));F_OCE=((294.04,-72.73),(294.25,-61.78))
F_GW=((351.29,-72.35),(359.52,-72.54));F_MU=((359.52,-72.54),(383.09,-73.31));F_MUW=((359.77,-60.07),(359.61,-68.14))
F_YD=((294.25,-61.78),(294.5,-49.83));F_RD=((294.48,-48.02),(294.8,-34.98))
F_TP=((305.56,-27.69),(305.45,-57.98));F_PKW=((305.45,-57.98),(305.42,-72.04));F_PKS=((305.42,-72.04),(329.78,-72.09));F_PKE=((329.78,-72.09),(329.81,-58.03))
BK_COLS=[1.8,4.2,9.8,12.2]
OC_COLS=[3.4,5.7,11.5,13.8];OC_UP=[3.4,5.7,8.7,11.5,13.8]
MU_COLS=[2.6+2.7*k for k in range(8)]
TP_COLS=[28.82-2.384*k for k in range(12)];TP_LEV=[(1.86,1.30,2.05),(5.16,1.30,1.90),(8.72,1.30,1.75)]
PK_LEV=[(2.0,1.30,1.90),(5.6,1.30,1.90),(9.25,1.30,1.85),(12.8,1.25,1.80)]
def cols106(F,n0,step,n,levels):return [('win',n0+k*step,b,w,h) for k in range(n) for b,w,h in levels]
FRONTS={
 'bk':[(F_BK,[('win',s,1.45,1.15,2.30) for s in BK_COLS]+[('door',6.8,.90,1.25,2.60)]+[('seg',s,5.70,1.10,1.95,.25) for s in BK_COLS]+[('arch',7.07,5.70,1.15,1.65,.55)])],
 'oc':[(F_OC,[('win',s,1.85,1.15,1.35) for s in OC_COLS]+[('door',8.85,1.22,1.05,2.14),('base',5.0,.20,.75,.40)]+[('win',s,4.50,1.15,1.95) for s in OC_UP]),
       (F_OCE,[('win',s,b,1.15,h) for s in (2.3,5.6,8.9) for b,h in ((1.85,1.35),(4.50,1.95))])],
 'gw':[(F_GW,[('garage',1.5,0,2.20,2.20)])],
 'mu':[(F_MU,[('win' if k!=3 else 'door',s,1.95 if k!=3 else 1.30,1.35 if k!=3 else 1.55,2.05 if k!=3 else 2.50) for k,s in enumerate(MU_COLS)]+
             [('arch',s,5.60,1.25,1.35,.62) for s in MU_COLS]+[('base',s,.30,.70,.45) for k,s in enumerate(MU_COLS) if k!=3]),
       (F_MUW,[('win',s,b,1.2,h) for s in (2.0,5.0) for b,h in ((1.95,2.0),(5.6,1.9))])],
 'yd':[(F_YD,[('gate',6.3,.05,2.70,2.70)])],
 'rd':[(F_RD,[('win',s,1.0,1.10,1.25) for s in (2.6,10.4)]+[('door',6.5,.15,1.00,2.05)])],
 'tp':[(F_TP,[('win',s,b,w,h) for s in TP_COLS for b,w,h in TP_LEV])],
 'pk':[(F_PKW,cols106(F_PKW,2.2,2.52,5,PK_LEV)+[('base',2.2+2.52*k,.35,.85,.55) for k in (0,2,4)]),
       (F_PKS,cols106(F_PKS,2.0,2.5,9,PK_LEV)+[('base',2.0+2.5*k,.35,.85,.55) for k in (1,3,5,7)]),
       (F_PKE,cols106(F_PKE,2.2,2.52,5,PK_LEV))],
}
STYLE={'bk':dict(wall='Ashlar',frame='RedFrame',trim='Band',kind='brick'),'bkw':dict(wall='Band',frame='RedFrame',trim='Band',kind='plain'),
 'oc':dict(wall='Ochre',frame='RedFrame',trim='OcTrim',kind='ochre'),'ocb':dict(wall='Ochre',frame='RedFrame',trim='OcTrim',kind='plain'),
 'gw':dict(wall='GreyBoard',frame='GreyBoard',trim='GreyBoard',kind='boards'),
 'mu':dict(wall='MuStucco',frame='MuFrame',trim='MuTrim',kind='museum'),'mub':dict(wall='MuStucco',frame='MuFrame',trim='MuTrim',kind='plain'),
 'yd':dict(wall='YdBoard',frame='YdBoard',trim='YdBoard',kind='boards'),'yw':dict(wall='YardRender',frame='WhiteFrame',trim='OcTrim',kind='plain'),
 'ym':dict(wall='YardRender',frame='WhiteFrame',trim='OcTrim',kind='plain'),'rd':dict(wall='FaluRed',frame='WhiteFrame',trim='WhiteFrame',kind='redboards'),
 'tp':dict(wall='Taupe',frame='WhiteFrame',trim='TpTrim',kind='taupe'),'tpb':dict(wall='Taupe',frame='WhiteFrame',trim='TpTrim',kind='plain'),
 'pk':dict(wall='Pink',frame='WhiteFrame',trim='Quoin',kind='pink')}
def ops106(zone,w):
 x,y,L,a=sf_edge(w['p'],w['q']);ox,oy=outward(w);out=[];hit=False
 for F,ops in FRONTS.get(zone,[]):
  d,n=frame106(F)
  # The wall belongs to this front when it runs the same way along the same line.
  if (math.cos(a)*d[0]+math.sin(a)*d[1])<.99:continue
  if abs((x-F[0][0])*n[0]+(y-F[0][1])*n[1])>.6:continue
  hit=True
  for kind,s,b,ww,hh,*r in ops:
   X,Y=P106(F,s);u=U(w,X,Y)
   if abs(u)+ww/2<=L/2+.01:out.append((kind,u,b,ww,hh,r[0] if r else 0))
 return hit,out

meshes={}
for zone,spec in Z.items():
 nm=spec['mesh']
 if nm not in meshes:meshes[nm]=b106_new(nm,'Kvarnholmen/Sodra Langgatan north')
for zone,spec in Z.items():
 m=meshes[spec['mesh']];H=spec['height'];st=STYLE[zone];wm=M106[st['wall']];tm=M106[st['trim']];fm=M106[st['frame']];kind=st['kind']
 for w in walls(zone):
  if w['kind']!='outer':bz_wall(m,w['p'],w['q'],w['z0'],H,[],wm if kind!='brick' else M106['Brick']);continue
  x,y,L,a=sf_edge(w['p'],w['q']);front,mine=ops106(zone,w)
  if not front:
   if L<1.5 or kind=='boards':
    bz_wall(m,w['p'],w['q'],0,H,[],wm)
    if kind=='boards':boards82(m,x,y,L,a,.3,H-.08,[],wm)
    continue
   if kind=='redboards':bz_wall(m,w['p'],w['q'],0,H,[],wm);boards82(m,x,y,L,a,.35,H-.08,[],wm);continue
   plain(m,w,H,M106['Brick'] if kind=='brick' else wm,fm,tm,1 if H<4 else (2 if H<9 else (3 if H<13 else 4)),.9 if H<13 else 2.0);continue
  holes=[(u,b,ww,hh,r) for k,u,b,ww,hh,r in mine]
  if kind=='brick':
   # Ground floor: rusticated ashlar render to the storey band; upper floor brick.
   gh=[hh for hh in holes if hh[1]<5.0];uh=[hh for hh in holes if hh[1]>=5.0]
   bz_wall(m,w['p'],w['q'],0,5.0,gh,wm);bz_wall(m,w['p'],w['q'],5.0,H,uh,M106['Brick'])
   facade_box(m,x,y,0,.40,.30,L+.02,.10,.60,M106['BkPlinth'],a)
   z=.95
   while z<4.9:hstrip106(m,x,y,L,a,z,.035,gh,.37,.03,M106['BkPlinth']);z+=.42
   facade_box(m,x,y,0,.45,5.30,L+.04,.20,.60,M106['Band'],a)
   for z in (6.05,6.55,7.05,7.55,8.05,8.55,9.05):hstrip106(m,x,y,L,a,z,.20,uh,.38,.06,M106['Band'],.05)
   facade_box(m,x,y,0,.42,9.25,L+.04,.14,.30,M106['Band'],a);facade_box(m,x,y,0,.62,9.75,L+.30,.55,.50,M106['Band'],a)
   for k in range(int(L/.9)+1):facade_box(m,x,y,-L/2+.3+k*(L-.6)/int(L/.9),.55,9.42,.16,.35,.30,M106['Band'],a)
   # The centre bay: pilasters each side of the round-headed window.
   X,Y=P106(F_BK,7.07);uc=U(w,X,Y)
   for s_ in (-1.50,1.50):facade_box(m,x,y,uc+s_,.46,7.35,.42,.18,3.9,M106['Band'],a);facade_box(m,x,y,uc+s_,.50,9.05,.55,.24,.30,M106['Band'],a)
   for k_,u,b,ww,hh,r in mine:
    if k_=='door':
     door83(m,x,y,u,b,ww,hh,a,M106['DoorRed'],fm,glass=False);steps106(m,x,y,u,ww,b,a,M106['BkPlinth'],.65)
     surround36(m,x,y,u,b,ww,hh,a,M106['Band'],.18,.42)
    elif k_=='arch':p18_win(m,x,y,u,b,ww,hh,r,a,fm,M106['Band'],3,2)
    elif k_=='seg':p18_win(m,x,y,u,b,ww,hh,r,a,fm,M106['Band'],3,2);facade_box(m,x,y,u,.50,b+hh+r+.12,ww+.45,.20,.18,M106['Band'],a)
    else:win106(m,x,y,u,b,ww,hh,a,fm,M106['Band'],.14)
   continue
  bz_wall(m,w['p'],w['q'],0,H,[(u,b,ww,hh,r) for u,b,ww,hh,r in holes if b+hh+r<=H-.05],wm)
  if kind=='ochre':
   facade_box(m,x,y,0,.40,.35,L+.02,.10,.70,M106['OcPlinth'],a);facade_box(m,x,y,0,.48,H-.18,L+.10,.24,.36,tm,a)
   for uu in (-L/2+.18,L/2-.18):facade_box(m,x,y,uu,.42,H/2,.36,.10,H,tm,a)
   for k_,u,b,ww,hh,r in mine:
    if k_=='door':
     door83(m,x,y,u,b,ww,hh,a,M106['DoorRed'],fm,glass=False);surround36(m,x,y,u,b,ww,hh,a,M106['OcPlinth'],.22,.42)
     steps106(m,x,y,u,ww+.2,b,a,M106['OcPlinth'],.90)
    elif k_=='base':facade_box(m,x,y,u,.47,b+hh/2,ww,.02,hh,M106['Dark'],a);surround36(m,x,y,u,b,ww,hh,a,M106['OcTrim'],.08,.48)
    else:win106(m,x,y,u,b,ww,hh,a,fm,tm,.14)
  elif kind=='boards':
   lowh=[(u,b,ww,hh,r) for k_,u,b,ww,hh,r in mine]
   boards82(m,x,y,L,a,.36,H-.08,lowh,wm);facade_box(m,x,y,0,.40,.18,L+.02,.10,.36,M106['Granite'],a)
   facade_box(m,x,y,0,.42,H-.06,L+.06,.14,.12,wm,a)
   for k_,u,b,ww,hh,r in mine:
    if k_=='garage':gate83(m,x,y,u,b,ww,hh,a,M106['Olive'],M106['Olive'])
    else:
     gate83(m,x,y,u,b,ww,hh,a,M106['GateRed'],M106['GateRed'])
     # Carved lattice panels in the upper part of the gate leaves.
     for q in (-.85,-.30,.30,.85):facade_box(m,x,y,u+q,.21,b+hh-.70,.22,.03,.90,M106['Lattice'],a)
     facade_box(m,x,y,u,.42,b+hh+.15,ww+.40,.16,.30,M106['GateRed'],a)
   if zone=='gw':
    X,Y=P106(F_GW,6.3);u=U(w,X,Y);facade_box(m,x,y,u,.42,2.0,1.7,.04,.28,M106['SignBlue'],a)
  elif kind=='museum':
   facade_box(m,x,y,0,.42,.50,L+.04,.14,1.0,M106['MuPlinth'],a)
   for z in (1.15,1.45):hstrip106(m,x,y,L,a,z,.06,holes,.43,.04,M106['MuTrim'])
   z=2.0
   while z<4.3:hstrip106(m,x,y,L,a,z,.04,holes,.38,.04,M106['MuFrame'],.05);z+=.34
   facade_box(m,x,y,0,.46,4.50,L+.06,.22,.24,M106['MuTrim'],a);facade_box(m,x,y,0,.44,4.85,L+.04,.16,.30,M106['MuStucco'],a)
   facade_box(m,x,y,0,.50,8.70,L+.06,.26,.40,M106['MuTrim'],a);facade_box(m,x,y,0,.46,9.15,L+.04,.18,.50,M106['MuStucco'],a)
   facade_box(m,x,y,0,.95,9.95,L+1.1,1.00,.36,M106['MuTrim'],a);facade_box(m,x,y,0,.75,9.65,L+.6,.70,.24,M106['MuTrim'],a)
   for k in range(int(L/.7)+1):facade_box(m,x,y,-L/2+.3+k*(L-.6)/max(1,int(L/.7)),.70,9.40,.14,.55,.26,M106['MuTrim'],a)
   ups=[hh for hh in mine if hh[0]=='arch']
   if ups:
    # Pilasters between the round-headed windows, with balustrade panels below each window.
    us=sorted(u for k_,u,b,ww,hh,r in ups);step=(us[-1]-us[0])/max(1,len(us)-1) if len(us)>1 else 2.7
    for pu in [us[0]-step/2]+[u+step/2 for u in us]:
     if abs(pu)<L/2-.2:facade_box(m,x,y,pu,.46,6.80,.40,.20,3.6,M106['MuTrim'],a);facade_box(m,x,y,pu,.50,8.45,.55,.24,.30,M106['MuTrim'],a)
    for pu in [L/2-.25,-L/2+.25]:facade_box(m,x,y,pu,.46,6.80,.50,.20,3.6,M106['MuTrim'],a)
    for k_,u,b,ww,hh,r in ups:
     facade_box(m,x,y,u,.50,5.05,ww+.5,.24,.10,M106['MuTrim'],a);facade_box(m,x,y,u,.50,5.50,ww+.5,.24,.10,M106['MuTrim'],a)
     for q in range(7):town_rod(m,lp(x,y,u-ww/2+q*(ww)/6,.47,5.10,a),lp(x,y,u-ww/2+q*(ww)/6,.47,5.45,a),.035,M106['MuTrim'],6)
   for k_,u,b,ww,hh,r in mine:
    if k_=='arch':p18_win(m,x,y,u,b,ww,hh,r,a,fm,M106['MuTrim'],3,2)
    elif k_=='door':
     door83(m,x,y,u,b,ww,hh,a,M106['MuDoor'],fm,glass=True);steps106(m,x,y,u,ww+.6,b,a,M106['MuPlinth'],1.40)
     surround36(m,x,y,u,b,ww,hh,a,M106['MuTrim'],.25,.44);facade_box(m,x,y,u,.60,b+hh+.55,ww+1.0,.40,.25,M106['MuTrim'],a)
    elif k_=='base':facade_box(m,x,y,u,.51,b+hh/2,ww,.02,hh,M106['Dark'],a);surround36(m,x,y,u,b,ww,hh,a,M106['MuTrim'],.08,.53)
    else:win106(m,x,y,u,b,ww,hh,a,fm,M106['MuTrim'],.16,3)
  elif kind=='redboards':
   lowh=[(u,b,ww,hh,r) for k_,u,b,ww,hh,r in mine];boards82(m,x,y,L,a,.40,H-.08,lowh,wm)
   facade_box(m,x,y,0,.40,.20,L+.02,.10,.40,M106['OcPlinth'],a)
   for uu in (-L/2+.09,L/2-.09):facade_box(m,x,y,uu,.42,H/2,.18,.10,H,tm,a)
   for k_,u,b,ww,hh,r in mine:
    if k_=='door':door83(m,x,y,u,b,ww,hh,a,M106['GateRed'],tm,glass=False)
    else:win106(m,x,y,u,b,ww,hh,a,tm,tm)
  elif kind=='taupe':
   facade_box(m,x,y,0,.40,.26,L+.02,.10,.52,M106['DarkGranite'],a);facade_box(m,x,y,0,.42,.66,L+.02,.12,.28,M106['TpTrim'],a)
   facade_box(m,x,y,0,.48,H-.20,L+.10,.26,.40,M106['TpTrim'],a)
   for k_,u,b,ww,hh,r in mine:win106(m,x,y,u,b,ww,hh,a,fm,tm,.16)
  elif kind=='pink':
   lowb=[(u,b,ww,hh,r) for k_,u,b,ww,hh,r in mine if k_=='base']
   at=-L/2
   for lo,hi in sorted((u-ww/2-.05,u+ww/2+.05) for u,b,ww,hh,r in lowb)+[(L/2,L/2)]:
    if lo>at+.05:facade_box(m,x,y,(at+lo)/2,.42,.70,lo-at,.14,1.40,M106['PkBase'],a)
    at=max(at,hi)
   for u,b,ww,hh,r in lowb:facade_box(m,x,y,u,.42,b+hh+(1.40-b-hh)/2,ww+.1,.14,1.40-b-hh,M106['PkBase'],a);facade_box(m,x,y,u,.30,b+hh/2,ww,.02,hh,M106['Dark'],a)
   facade_box(m,x,y,0,.46,1.45,L+.06,.18,.12,M106['Quoin'],a)
   facade_box(m,x,y,0,.62,H-.25,L+.30,.50,.50,M106['Quoin'],a);facade_box(m,x,y,0,.46,H-.70,L+.06,.18,.20,M106['Quoin'],a)
   for uu,sg in ((-L/2,1),(L/2,-1)):quoins106(m,x,y,uu,sg,a,1.5,H-.8,M106['Quoin'])
   for k_,u,b,ww,hh,r in mine:
    if k_!='base':win106(m,x,y,u,b,ww,hh,a,fm,M106['Quoin'],.16)

# ---------------------------------------------------------------- roofs
def hip106(zone,F,rise,ma,ov=.40,chims=()):
 m=meshes[Z[zone]['mesh']];s0,s1,t0,t1=rect106(zone,F);H=Z[zone]['height'];r=ring106(F,s0,s1,t0,t1)
 inset_roof(m,r,H,min(s1-s0,t1-t0)/2-.30,rise,M106[ma],ov)
 for s,t in chims:X,Y=P106(F,s,t);chimney82(m,X,Y,H+rise-.6,H+rise+.9,M106['Chimney'])
 return m,s0,s1,t0,t1,rise/(min(s1-s0,t1-t0)/2-.30+ov)
# 91928568: low hip, two round-topped dormers and the brick aedicule over the centre bay.
m,s0,s1,t0,t1,sl=hip106('bk',F_BK,Z['bk']['top']-Z['bk']['height'],'SheetDark',chims=((3.5,6.0),(11.0,6.0)))
H=Z['bk']['height']
for s in (3.0,11.2):roundtop106(m,F_BK,s,.9,1.6,H+(.9+.40)*sl-.15,1.15,.55,M106['SheetDark'],M106['SheetDark'],M106['RedFrame'])
roundtop106(m,F_BK,7.07,-.25,1.8,H-.05,2.3,1.25,M106['Brick'],M106['Band'],M106['RedFrame'])
m=meshes[Z['bkw']['mesh']]
for g in Z['bkw']['polygons']:m.faces([(*v,Z['bkw']['height']+.02) for v in g],[tuple(range(len(g))),tuple(range(len(g)-1,-1,-1))],M106['SheetDark'])
# 91928594: saddle along the street, gables to the west (on the brick house's party wall) and
# to Landshövdingegatan (attic windows), a round-topped dormer over the door.
F=F_OC;m=meshes[Z['oc']['mesh']];s0,s1,t0,t1=rect106('oc',F);H=Z['oc']['height'];T=Z['oc']['top'];o=.355;tm_=(t0+t1)/2;half=tm_-t0+o;sl=(T-H)/half;ov=.40
for ta,sg in ((t0-o,-1),(t1+o,1)):
 e=ta+sg*ov;ze=H-ov*sl
 m.faces([P106(F,s0-o-.25,e,ze),P106(F,s1+o+.30,e,ze),P106(F,s1+o+.30,tm_,T),P106(F,s0-o-.25,tm_,T)],[(0,1,2,3),(3,2,1,0)],M106['SheetDark'])
 town_rod(m,P106(F,s0-o-.25,e,ze-.05),P106(F,s1+o+.30,e,ze-.05),.07,M106['Sheet'],8)
for s,sg in ((s0-o,1),(s1+o,-1)):
 # Gable prisms (in the frame's (t, z) plane, extruded along s).
 pts=[(t0-o,H),(t1+o,H),(tm_,T-.02)];vs=[P106(F,ss,t,z) for ss in (s,s+sg*.30) for t,z in pts]
 m.faces(vs,[(2,1,0),(3,4,5),(0,1,4,3),(1,2,5,4),(2,0,3,5)],M106['Ochre'])
x,y,L,a=sf_edge(*F_OCE)
for uu in (-1.1,1.1):
 X,Y=P106(F,s1+o+.30,t0+(t1-t0)/2+uu);u=U({'p':list(F_OCE[0]),'q':list(F_OCE[1])},X,Y)
 facade_box(m,x,y,u,.47,H+.35+.55,.70,.02,1.10,GLAZE,a);cas81(m,x,y,u,H+.35,.70,1.10,a,M106['RedFrame'],.50,2);surround36(m,x,y,u,H+.35,.70,1.10,a,M106['OcTrim'],.10,.53)
roundtop106(m,F,8.85,1.4,1.5,H+(1.4+o+ov)*sl-.15,1.05,.60,M106['SheetRed'],M106['SheetRed'],M106['WhiteFrame'])
X,Y=P106(F,4.0,tm_+.6);chimney82(m,X,Y,T-.6,T+.7,M106['Chimney'])
m=meshes[Z['ocb']['mesh']]
for g in Z['ocb']['polygons']:m.faces([(*v,Z['ocb']['height']+.02) for v in g],[tuple(range(len(g))),tuple(range(len(g)-1,-1,-1))],M106['SheetDark'])
# 93199647: flat roof behind the board wall.
m=meshes[Z['gw']['mesh']]
for g in Z['gw']['polygons']:m.faces([(*v,Z['gw']['height']+.04) for v in g],[tuple(range(len(g))),tuple(range(len(g)-1,-1,-1))],M106['SheetDark'])
# Sjöfartsmuseet: low hip over the boxed main body, flat strip behind.
hip106('mu',F_MU,Z['mu']['top']-Z['mu']['height'],'Sheet',.45,chims=((4.0,5.5),(19.5,5.5)))
m=meshes[Z['mub']['mesh']]
for g in Z['mub']['polygons']:m.faces([(*v,Z['mub']['height']+.04) for v in g],[tuple(range(len(g))),tuple(range(len(g)-1,-1,-1))],M106['Sheet'])
# 91928552: the yard under a flat roof, a tiled lean-to along its north side; flat roofs on the
# courtyard ranges with a parapet band.
m=meshes[Z['yd']['mesh']]
for zone in ('yd','yw','ym'):
 for g in Z[zone]['polygons']:m.faces([(*v,Z[zone]['height']+.02) for v in g],[tuple(range(len(g))),tuple(range(len(g)-1,-1,-1))],M106['SheetDark'])
for zone in ('yw','ym'):
 for w in walls(zone,'outer'):
  x,y,L,a=sf_edge(w['p'],w['q'])
  if L>.5:facade_box(m,x,y,0,.40,Z[zone]['height']+.10,L+.1,.14,.30,M106['OcTrim'],a)
F=F_YD;yz=Z['yd']['height']
m.faces([P106(F,6.5,-.10,yz+.55),P106(F,12.2,-.10,yz+.55),P106(F,12.2,6.0,yz+.10),P106(F,6.5,6.0,yz+.10)],[(0,1,2,3),(3,2,1,0)],M106['Tile'])
# 91928587: gambrel along the street; the profile across the depth, gable prisms at both ends
# with windows in the south one.
F=F_RD;m=meshes[Z['rd']['mesh']];s0,s1,t0,t1=rect106('rd',F);H=Z['rd']['height'];T=Z['rd']['top'];KN=Z['rd']['knee'];o=.355;KW=1.0
tL,tR=t0-o,t1+o;tmid=(tL+tR)/2
prof=[(tL-.30,H-.35),(tL,H),(tL+KW,KN),(tmid,T),(tR-KW,KN),(tR,H),(tR+.30,H-.35)]
for (p0,z0),(p1,z1) in zip(prof,prof[1:]):
 m.faces([P106(F,s0-o-.30,p0,z0+.12),P106(F,s1+o+.30,p0,z0+.12),P106(F,s1+o+.30,p1,z1+.12),P106(F,s0-o-.30,p1,z1+.12)],[(0,1,2,3),(3,2,1,0)],M106['Tile'])
for e in (0,-1):town_rod(m,P106(F,s0-o-.30,prof[e][0],prof[e][1]+.05),P106(F,s1+o+.30,prof[e][0],prof[e][1]+.05),.07,M106['Sheet'],8)
g=[(tL,H),(tR,H),(tR-KW,KN),(tmid,T-.05),(tL+KW,KN)]
for s,sg in ((s0-o,1),(s1+o,-1)):
 vs=[P106(F,ss,t,z) for ss in (s,s+sg*.30) for t,z in g];n=len(g)
 m.faces(vs,[tuple(range(n)),tuple(range(2*n-1,n-1,-1))]+[(i,i+n,(i+1)%n+n,(i+1)%n) for i in range(n)],M106['FaluRed'])
# Gable windows on the south end (seen from the yard) and dormers on the street slope.
x,y,L,a=sf_edge(P106(F,s0-o,tR),P106(F,s0-o,tL))
for uu,b in ((-1.4,4.3),(1.4,4.3),(0,6.4)):
 facade_box(m,x,y,uu,.02,b+.55,.75,.02,1.1,GLAZE,a);cas81(m,x,y,uu,b,.75,1.1,a,M106['WhiteFrame'],.05,2);surround36(m,x,y,uu,b,.75,1.1,a,M106['WhiteFrame'],.10,.06)
for s in (3.5,9.5):
 X,Y=P106(F,s,tL+.55);x_,y_,L_,a_=sf_edge(*F)
 box(m,X,Y,1.3,1.2,1.3,H+.45,M106['FaluRed'],a_,M106['Tile']);facade_box(m,X,Y,0,.62,H+1.1,.80,.02,.90,GLAZE,a_);cas81(m,X,Y,0,H+.65,.80,.90,a_,M106['WhiteFrame'],.64,2)
X,Y=P106(F,(s0+s1)/2+2,tmid);chimney82(m,X,Y,T-.6,T+.7,M106['Chimney'])
# 93199672 and 93199626: low hips in dark sheet; the stair bumps under flat roofs.
hip106('tp',F_TP,Z['tp']['top']-Z['tp']['height'],'SheetDark',.45,chims=((8.0,5.5),(20.0,5.5)))
m=meshes[Z['tpb']['mesh']]
for g in Z['tpb']['polygons']:m.faces([(*v,Z['tpb']['height']+.04) for v in g],[tuple(range(len(g))),tuple(range(len(g)-1,-1,-1))],M106['SheetDark'])
hip106('pk',F_PKS,Z['pk']['top']-Z['pk']['height'],'SheetDark',.55,chims=((6.0,6.0),(18.0,6.0)))
for nm in meshes:b106_finish(meshes[nm],nm.split('_')[-1])

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block106_cameras=[
 sv_camera('506_Block106_Cal_Brick',265.37,-78.29,2.30,332,20,90),
 sv_camera('507_Block106_Cal_Museum',374.47,-79.93,2.40,331,20,90),
 sv_camera('508_Block106_Cal_Taupe',298.76,-47.51,2.30,62,15,90),
 sv_camera('509_Block106_Cal_Ochre',291.05,-79.32,2.30,332,20,90),
 ('510_Block106_Aerial',(325.0,-15.0,45.0),(325.0,-62.0,4.0),28),
]
print('BLOCK106_GEOMETRY',len(block106_names),'dropped',block106_dropped,block106_samples)
