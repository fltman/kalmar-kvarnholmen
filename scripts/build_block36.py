"""Pass 36: OSM way 92379286 on the south side of Södra Långgatan: the long cream house next to the
palace and the stone corner house on Kaggensgatan with the portal dated 1659.

The cream house: cream render over a grey plinth; a modern shop front, an arched gate with boarded
leaves, a tall window, a shop front of two windows and a door, and three tall windows with high
sills; eleven upper windows in light surrounds (two of them blind); a band under the eaves; a red
tile roof with three chimneys and small vents; a curved gable with a round-headed window over the
east end, with a copper roof behind it.

The corner house: cream render with quoins; on both streets tall shop windows under transom
windows, a grey band with iron wall anchors, tall upper windows with brown casements in stone
surrounds, a frieze and a cornice; on Södra Långgatan the sandstone portal with its steps, the
door under an arch, the entablature and a broken pediment with the date cartouche. Its roof is not
seen from the street and is estimated as a hipped roof.

References: Google Street View April 2025 (the camera track of pass 35), view only. Zones:
source/block36.json; see references/block36-notes.md. Tenant signs and lettering are omitted.
"""
B36D=json.loads((R/'source/block36.json').read_text());Z=B36D['zones']
block36_names=[];B36={}
for old in [k for k in list(materials) if k.startswith('M_Block36_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Cream','TownIvory',(.89,.82,.66),.90,0),
 ('Render','TownIvory',(.91,.88,.79),.88,0),
 ('Surround','TownIvory',(.80,.79,.74),.86,0),
 ('White','TownIvory',(.93,.93,.90),.82,0),
 ('Brown','TownPaintBrown',(.42,.28,.17),.55,0),
 ('Sandstone','TownStone',(.64,.47,.40),.88,0),
 ('Stone','TownStone',(.74,.71,.65),.86,0),
 ('Tile','TownTileRed',(.58,.31,.21),.80,0),
 ('Copper','TownMetalRed',(.52,.27,.20),.55,.30),
 ('Plinth','TownStone',(.55,.55,.53),.82,0),
 ('Gate','TownIvory',(.86,.86,.83),.80,0),
 ('Shopfront','TownMetalGrey',(.36,.37,.38),.45,.40),
 ('Oak','TownPaintBrown',(.38,.26,.16),.60,0),
 ('RoofDark','TownMetalGrey',(.28,.29,.30),.55,.30),
 ('Dark','TownMetalGrey',(.05,.055,.06),.40,.20),
 ('PartyWall','TownIvory',(.75,.73,.68),.88,0),
 ]:
 name='M_Block36_'+key;B36[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block36_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B36;WH,SU=M['White'],M['Surround']

def b36_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block36_names.append(name);return Mesh(name,category)
def b36_finish(m,osm):
 obj=s21_finish(m);obj['detail_pass']=36;obj['reference_notes']='references/block36-notes.md';obj['osm_way']=osm;return obj
def kind36(w):
 ox,oy=outward(w)
 if w['kind']!='outer':return None
 if oy>.9 and max(w['p'][1],w['q'][1])>-80.5:return 'sodra'
 if ox<-.9 and min(w['p'][0],w['q'][0])<-181:return 'kagg'
 return None
def plinth36(m,x,y,L,a,gaps,H,ma):
 at=-L/2
 for l,r in sorted(gaps)+[(L/2,L/2)]:
  if l>at+.02:facade_box(m,x,y,(at+l)/2,.40,H/2,l-at,.10,H,ma,a)
  at=max(at,r)
def surround36(m,x,y,u,b,w,h,a,ma,bw=.12,o=.38):
 # Flat plaster surround round an opening (w, h: the opening; bw: the band's width).
 for s in (-1,1):facade_box(m,x,y,u+s*(w/2+bw/2),o,b+h/2,bw,.06,h+2*bw,ma,a)
 for zz in (b-bw/2,b+h+bw/2):facade_box(m,x,y,u,o,zz,w+2*bw,.06,bw,ma,a)
def casement36(m,x,y,u,b,w,h,a,frame,panes=3,trans=None,o=.20):
 # Casement with a mullion and glazing bars, set o behind the wall face (+0.355).
 facade_box(m,x,y,u,o-.04,b+h/2,w,.02,h,GLAZE,a)
 for q in (-w/2+.04,w/2-.04):facade_box(m,x,y,u+q,o,b+h/2,.08,.08,h,frame,a)
 for zz in (b+.04,b+h-.04):facade_box(m,x,y,u,o,zz,w,.08,.08,frame,a)
 facade_box(m,x,y,u,o+.01,b+h/2,.07,.07,h,frame,a)
 if trans:facade_box(m,x,y,u,o+.01,b+h*trans,w,.07,.06,frame,a)
 for k in range(1,panes):facade_box(m,x,y,u,o+.01,b+h*k/panes,w,.05,.03,frame,a)
 facade_box(m,x,y,u,o+.12,b-.02,w+.06,.26,.03,METAL,a)
def anchor36(m,x,y,u,z,a,ma):
 # Iron wall anchor: a vertical bar with a scroll either side at the band (fleur-de-lis).
 town_rod(m,lp(x,y,u,.42,z-.55,a),lp(x,y,u,.42,z+.55,a),.025,ma,6)
 for sg in (-1,1):
  town_path(m,[lp(x,y,u+sg*(.02+.11*math.sin(math.pi*t/8)),.43,z+.10-.20*t/8,a) for t in range(9)],.018,ma)
  town_path(m,[lp(x,y,u+sg*(.06+.05*math.cos(math.tau*t/10)),.43,z-.10+.05*math.sin(math.tau*t/10),a) for t in range(11)],.015,ma)
def steps36(m,x,y,u,a,w0,w1,top,n,d,ma):
 # Stone steps up to a door n treads, flaring from w1 at the door to w0 at the street.
 for k in range(n):
  zt=top*(k+1)/n;dep=d*(n-k)/n;ww=w1+(w0-w1)*(n-1-k)/(n-1)
  facade_box(m,x,y,u,.355+dep/2,zt/2,ww,dep,zt,ma,a)

# ---------------------------------------------------------------- the cream house
CRM=M['Cream'];HC=Z['cr']['height']
m=b36_new('SM_Kvarnholmen_House_92379286','Kvarnholmen/Södra Långgatan south')
for w in walls('cr'):
 k=kind36(w)
 if k is None:
  if w['kind']=='outer':plain(m,w,HC,CRM,M['Brown'],SU,2,.9)
  else:bz_wall(m,w['p'],w['q'],w['z0'],HC,[],CRM)
  continue
 x,y,L,a=sf_edge(w['p'],w['q']);S=lambda s:-L/2+s                  # s from the palace joint
 # Openings, from panoramas "18" and "17" (s: opening edges inside the surrounds).
 # The gate's segmental head: a rectangular hole up to the crown and closed spandrel prisms (an
 # arched hole's own spandrels triangulate into slivers at the crown).
 gate=(S(8.93),0,2.32,2.71,.37)
 gf=[(S(4.56),.45,3.29,2.56,0),(gate[0],0,2.32,2.71+.37,0),(S(12.555),.69,1.25,2.68,0),(S(17.265),.72,5.19,2.65,0),
     (S(21.17),.83,1.28,2.63,0),(S(24.0),1.31,1.21,2.25,0),(S(26.65),1.31,1.22,2.25,0)]
 UP=[2.89,5.015,7.23,9.74,12.565,15.365,17.255,19.285,21.23,24.015,26.66]
 BLIND=(17.255,21.23)
 up=[(S(s),4.76,1.19,1.41,0) for s in UP if s not in BLIND]
 bz_wall(m,w['p'],w['q'],0,HC,gf+up,CRM)
 # The barber's shop front: a grey aluminium frame, the window and a door with a transom.
 u0,b0,w0,h0,_=gf[0]
 facade_box(m,x,y,u0,.12,b0+h0/2,w0,.03,h0,GLAZE,a)
 for q in (-w0/2,w0/2,S(5.21)-u0,S(6.17)-u0):facade_box(m,x,y,u0+q,.24,b0+h0/2,.07,.18,h0,M['Shopfront'],a)
 for zz in (b0,b0+h0,2.26):facade_box(m,x,y,u0+(S(5.72)-u0 if zz==2.26 else 0),.24,zz,(.96 if zz==2.26 else w0),.18,.06,M['Shopfront'],a)
 facade_box(m,x,y,u0,.38,b0/2,w0,.06,b0,M['Plinth'],a)
 # The arched gate: boarded leaves with a diamond pattern and a wicket, a plain surround.
 gu,gb,gw,gh,gr=gate
 spandrels(m,x,y,gu,gb,gw,gh,gr,a,CRM)
 # The leaves stand nearly flush (no deep reveal shows in the panoramas).
 facade_box(m,x,y,gu,.30,gh/2,gw,.06,gh,M['Gate'],a)
 for zz in (.35,.85,1.35,1.85,2.35):
  for k in range(7):
   uu=gu-gw/2+(k+.5)*gw/7
   town_path(m,[lp(x,y,uu-.16,.34,zz,a),lp(x,y,uu,.34,zz+.22,a),lp(x,y,uu+.16,.34,zz,a),lp(x,y,uu,.34,zz-.22,a),lp(x,y,uu-.16,.34,zz,a)],.012,SU)
 facade_box(m,x,y,gu,.35,gh/2,.05,.05,gh,SU,a)
 facade_box(m,x,y,gu+.58,.28,1.00,.78,.05,1.80,M['Dark'],a)
 p18_arch(m,*lp(x,y,gu,0,0,a)[:2],gh,gw,gr,.26,.40,a,SU,20)
 facade_box(m,x,y,gu-gw/2-.30,.40,1.35,.60,.08,2.70,SU,a);facade_box(m,x,y,gu+gw/2+.08,.40,1.35,.16,.08,2.70,SU,a)
 # The windows and the second shop front, in plaster surrounds.
 for u,b,ww,hh,r in gf[2:]:
  surround36(m,x,y,u,b,ww,hh,a,SU,.12)
  if ww>3:
   facade_box(m,x,y,u,.12,b+hh/2,ww,.03,hh,GLAZE,a)
   for q in (-ww/2,S(16.70)-u,S(17.76)-u,ww/2):facade_box(m,x,y,u+q,.24,b+hh/2,.08,.18,hh,WH,a)
   for zz in (b,b+hh):facade_box(m,x,y,u,.24,zz,ww,.18,.07,WH,a)
   facade_box(m,x,y,S(17.23),.24,2.30,1.06,.18,.06,WH,a);facade_box(m,x,y,S(17.23),.14,(b+2.30)/2,.96,.05,2.30-b,WH,a)
  else:casement36(m,x,y,u,b,ww,hh,a,WH,4,.80)
 for u,b,ww,hh,r in up:surround36(m,x,y,u,b,ww,hh,a,SU,.12);casement36(m,x,y,u,b,ww,hh,a,WH,3)
 for s in BLIND:facade_box(m,x,y,S(s),.38,5.50,1.43,.05,1.66,M['Render'],a)
 plinth36(m,x,y,L,a,[(u-ww/2-.14,u+ww/2+.14) for u,b,ww,hh,r in gf if b<.62],.62,M['Plinth'])
 # (the gate's hole in gf is rectangular; its jambs and arch band are drawn above)
 # The band under the eaves, the eaves board and the gutter (its edge 0.45 m out).
 facade_box(m,x,y,0,.40,6.40,L,.10,.24,SU,a);facade_box(m,x,y,0,.52,6.49,L+.06,.30,.08,SU,a)
 town_rod(m,lp(x,y,-L/2,.80,6.52,a),lp(x,y,L/2,.80,6.52,a),.06,METAL,8)
 town_rod(m,lp(x,y,S(10.34),.48,.30,a),lp(x,y,S(10.34),.48,6.45,a),.05,M['Dark'],8)
# The neighbours' party walls above the two houses. The palace (pass 35) and the generic volume
# 92379292 behind were built against this way's old district height (9.75 m): the palace's west
# wall starts at 9.75, and 92379292 has no wall on its shared edges. The strips between the new,
# lower roofs and those walls are filled here, on the neighbours' side of each party line (the
# palace's on the same side as its pass 35 wall).
PW=M['PartyWall']
bz_wall(m,(-139.797,-79.661),(-139.99,-92.56),5.6,9.75,[],PW)
bz_wall(m,(-139.99,-92.56),(-140.16,-103.718),5.6,8.8,[],PW)
bz_wall(m,(-152.042,-92.788),(-152.276,-103.386),5.6,9.75,[],PW)
bz_wall(m,(-181.78,-91.469),(-168.914,-91.838),9.30,9.75,[],PW)
sl=roof34(m,'cr',M['Tile'],CRM)
for w in walls('cr'):
 if kind36(w)!='sodra':continue
 x,y,L,a=sf_edge(w['p'],w['q']);S=lambda s:-L/2+s
 # The curved gable over the east end (triangulated: apex 11.27, 0.19 m behind the facade), with a
 # round-headed window, scrolls at the shoulders and a cap; a copper roof runs back behind it.
 gc=S(3.82);o=.355-.08
 prof=[(2.25,HC),(2.18,6.85),(1.95,7.15),(1.70,7.40),(1.52,7.70),(1.44,8.05),(1.36,8.35),(1.18,8.52),(1.00,8.60),(.97,8.64),(.95,10.30),(.80,10.55),(.62,10.70)]
 full=[(-u,z) for u,z in prof]+[(u,z) for u,z in reversed(prof)]
 for (ua,za),(ub,zb) in zip(full,full[1:]):
  if abs(ub-ua)<1e-6:continue
  m.faces([lp(x,y,gc+ua,o,HC-.30,a),lp(x,y,gc+ub,o,HC-.30,a),lp(x,y,gc+ub,o,zb,a),lp(x,y,gc+ua,o,za,a)],[(0,1,2,3)],CRM)
  m.faces([lp(x,y,gc+ub,o-.30,HC-.30,a),lp(x,y,gc+ua,o-.30,HC-.30,a),lp(x,y,gc+ua,o-.30,za,a),lp(x,y,gc+ub,o-.30,zb,a)],[(0,1,2,3)],CRM)
  m.faces([lp(x,y,gc+ua,o,za,a),lp(x,y,gc+ub,o,zb,a),lp(x,y,gc+ub,o-.30,zb,a),lp(x,y,gc+ua,o-.30,za,a)],[(0,1,2,3)],SU)
 for sg in (-1,1):
  m.faces([lp(x,y,gc+sg*2.25,o,HC-.30,a),lp(x,y,gc+sg*2.25,o-.30,HC-.30,a),lp(x,y,gc+sg*2.25,o-.30,HC,a),lp(x,y,gc+sg*2.25,o,HC,a)][::(1 if sg>0 else -1)],[(0,1,2,3)],CRM)
  kk=14;cx_=gc+sg*1.18
  m.faces([lp(x,y,cx_+.16*math.cos(t*math.tau/kk),o+.04,8.40+.16*math.sin(t*math.tau/kk),a) for t in range(kk)],[tuple(range(kk))],SU)
 # The cap: a small gable roof over the top.
 cap=[(-1.05,10.70),(1.05,10.70),(0,11.27)];vs=[lp(x,y,gc+uu,oo,zz,a) for oo in (o+.08,o-.40) for uu,zz in cap]
 m.faces(vs,[(0,1,2),(5,4,3),(0,3,4,1),(1,4,5,2),(2,5,3,0)],SU)
 # The round-headed window (7.53-9.47), flush in the gable.
 wu,wb,ww,wt=gc,7.53,.80,9.47;r_=ww/2;k_=16
 contour=[(-ww/2,wb),(ww/2,wb)]+[(ww/2*math.cos(t*math.pi/k_),wt-r_+r_*math.sin(t*math.pi/k_)) for t in range(k_+1)]
 m.faces([lp(x,y,wu+uu,o+.01,zz,a) for uu,zz in contour],[tuple(range(len(contour)))],GLAZE)
 town_path(m,[lp(x,y,wu+uu,o+.03,zz,a) for uu,zz in contour+[contour[0]]],.03,WH)
 facade_box(m,x,y,wu,o+.03,(wb+wt-r_)/2,.05,.05,wt-r_-wb,WH,a);facade_box(m,x,y,wu,o+.03,wt-r_,ww,.05,.05,WH,a)
 town_path(m,[lp(x,y,wu+(ww/2+.10)*math.cos(t*math.pi/k_),o+.06,wt-r_+(r_+.10)*math.sin(t*math.pi/k_),a) for t in range(k_+1)],.05,SU)
 facade_box(m,x,y,wu,o+.10,wb-.05,ww+.24,.20,.08,SU,a)
 # The copper roof behind the gable, back to the main ridge.
 cz=10.55;dep=3.2
 for sg in (-1,1):
  m.faces([lp(x,y,gc,o-.30,cz,a),lp(x,y,gc+sg*1.0,o-.30,8.6,a),lp(x,y,gc+sg*1.0,o-.30-dep,8.6,a),lp(x,y,gc,o-.30-dep,cz,a)][::sg],[(0,1,2,3)],M['Copper'])
  # The cheek under each copper slope, down to the main roof (which reaches 8.6 about 1.8 m in).
  o_end=-(8.6-HC)/sl
  tri=[lp(x,y,gc+sg*1.0,o-.30,HC+(.30-o)*sl-.05,a),lp(x,y,gc+sg*1.0,o-.30,8.6,a),lp(x,y,gc+sg*1.0,o_end,8.6,a)]
  m.faces(tri if sg<0 else tri[::-1],[(0,1,2)],M['Copper'])
 # Chimneys on the ridge and small vents on the street slope.
 for s,top in ((6.8,11.40),(13.7,11.70),(27.6,11.60)):
  cx,cy,_=lp(x,y,S(s),.355-3.6,0,a);box(m,cx,cy,.55,.80,top-10.2,10.2,M['Tile'],a,M['Dark'])
 for s in (15.3,18.2,21.0):
  cx,cy,_=lp(x,y,S(s),.355-1.4,0,a);box(m,cx,cy,.18,.18,.55,HC+1.4*sl-.10,M['Dark'],a,M['Dark'])

# ---------------------------------------------------------------- the corner house
RN,ST=M['Render'],M['Stone'];HK=Z['kh']['height']
def kh_storeys(m,w,x,y,L,a,S,axes,tr_axes,ground,portal=None):
 # Band, anchors, the upper windows in stone surrounds, transom windows over the ground floor on
 # tr_axes, the frieze and the cornice (8.75-9.40 with the gutter on top).
 up=[(S(s),6.02,1.14,2.07,0) for s in axes]
 tr=[(S(s),3.44,1.14,.55,0) for s in tr_axes]
 gf=[(S(s),b,ww,hh,0) for s,b,ww,hh in ground]
 holes=up+tr+gf+([portal] if portal else [])
 bz_wall(m,w['p'],w['q'],0,HK,holes,RN)
 for u,b,ww,hh,r in up:surround36(m,x,y,u,b,ww,hh,a,ST,.15);casement36(m,x,y,u,b,ww,hh,a,M['Brown'],3,.70,.18)
 for u,b,ww,hh,r in tr:surround36(m,x,y,u,b,ww,hh,a,ST,.15);casement36(m,x,y,u,b,ww,hh,a,M['Brown'],1,None,.18)
 for u,b,ww,hh,r in gf:
  surround36(m,x,y,u,b,ww,hh,a,ST,.15)
  if b<.3:s20_door(m,x,y,u,b,ww,hh,a,M['Oak'])
  else:
   facade_box(m,x,y,u,.12,b+hh/2,ww,.03,hh,GLAZE,a)
   for q in (-ww/2+.04,ww/2-.04):facade_box(m,x,y,u+q,.22,b+hh/2,.08,.10,hh,M['Brown'],a)
   for zz in (b+.04,b+hh-.04):facade_box(m,x,y,u,.22,zz,ww,.10,.08,M['Brown'],a)
 facade_box(m,x,y,0,.40,5.22,L,.10,.26,ST,a)
 for k in range(len(axes)+1):
  if k==0:uu=S(axes[0])-1.25
  elif k==len(axes):uu=S(axes[-1])+1.25
  else:uu=(S(axes[k-1])+S(axes[k]))/2
  if -L/2+.3<uu<L/2-.3:anchor36(m,x,y,uu,5.22,a,M['Dark'])
 facade_box(m,x,y,0,.38,8.60,L,.06,.30,RN,a)
 facade_box(m,x,y,0,.43,8.80,L+.04,.16,.10,ST,a);facade_box(m,x,y,0,.51,8.95,L+.10,.32,.20,ST,a);facade_box(m,x,y,0,.58,9.20,L+.16,.46,.30,ST,a)
 town_rod(m,lp(x,y,-L/2,.82,9.34,a),lp(x,y,L/2,.82,9.34,a),.055,M['Dark'],8)
 plinth36(m,x,y,L,a,[(u-ww/2-.15,u+ww/2+.15) for u,b,ww,hh,r in gf if b<.68]+([(portal[0]-portal[2]/2-.60,portal[0]+portal[2]/2+.60)] if portal else []),.68,M['Plinth'])
m_=m
for w in walls('kh'):
 k=kind36(w);m=m_
 if k is None:
  if w['kind']=='outer':plain(m,w,HK,RN,M['Brown'],ST,2,.9)
  else:bz_wall(m,w['p'],w['q'],w['z0'],HK,[],RN)
  continue
 x,y,L,a=sf_edge(w['p'],w['q'])
 if k=='sodra':
  S=lambda s:-L/2+s                                                  # s from the joint
  axes=[1.895,4.155,6.67,9.335,11.885]
  ground=[(1.895,.78,1.14,2.29),(4.155,.78,1.14,2.29),(9.335,.78,1.14,2.29),(11.895,.78,1.14,2.29)]
  # The portal's arched door: a rectangular hole up to the crown and closed spandrel prisms.
  pu=S(6.705);portal=(pu,1.44,1.33,2.10+.57,0)
  kh_storeys(m,w,x,y,L,a,S,axes,[axes[0],axes[1],axes[3],axes[4]],ground,portal)
  for sg in (-1,1):quoins(m,x,y,sg*(L/2-.01),.68,8.55,a,ST,-sg,.42,.50,.30)
  # The sandstone portal: rusticated piers either side of the arched door, the entablature, a
  # broken segmental pediment with scrolls and the date cartouche (its inscription omitted).
  SS=M['Sandstone']
  spandrels(m,x,y,pu,1.44,1.33,2.10,.57,a,RN)
  facade_box(m,x,y,pu,.16,1.44+1.05,1.33,.08,2.10,M['Oak'],a)
  for sg in (-1,1):
   for zz,hh in ((1.44+.55,.70),(1.44+1.45,.80)):facade_box(m,x,y,pu+sg*.33,.21,zz,.48,.03,hh,M['Brown'],a)
  facade_box(m,x,y,pu,.22,1.44+1.05,.04,.04,2.10,M['Dark'],a)
  facade_box(m,x,y,pu,.14,2.10+1.44+.28,1.33,.05,.56,GLAZE,a)
  for sg in (-1,1):
   uu=pu+sg*(1.33/2+.30)
   facade_box(m,x,y,uu,.52,2.45,.60,.34,4.90,SS,a)
   for zz in (1.1,1.75,2.40,3.05,3.70):facade_box(m,x,y,uu,.70,zz,.62,.02,.04,M['Stone'],a)
   facade_box(m,x,y,uu,.62,4.12,.68,.34,.16,SS,a)
  p18_arch(m,*lp(x,y,pu,0,0,a)[:2],3.54,1.33+.10,.62,.26,.50,a,SS,20)
  facade_box(m,x,y,pu,.60,4.50,2.56,.36,.30,SS,a);facade_box(m,x,y,pu,.66,4.72,2.70,.46,.14,SS,a)
  for sg in (-1,1):
   town_path(m,[lp(x,y,pu+sg*(1.28-.50*t/10),.62,4.80+.34*math.sin(math.pi*t/10)+.18*t/10,a) for t in range(11)],.08,SS)
   kk=12;cx_=pu+sg*.85
   m.faces([lp(x,y,cx_+.12*math.cos(t*math.tau/kk),.70,5.02+.12*math.sin(t*math.tau/kk),a) for t in range(kk)],[tuple(range(kk))],SS)
  facade_box(m,x,y,pu,.62,5.20,.62,.24,.80,SS,a)
  xx,yy,_=lp(x,y,pu,.74,0,a);m.lathe(xx,yy,5.58,[(.06,0),(.20,.04),(.24,.10),(.14,.16),(.02,.18)],SS,12)
  steps36(m,x,y,pu,a,3.0,2.0,1.44,7,1.75,M['Stone'])
 else:
  S=lambda s:-L/2+s                                                  # s from the corner (north)
  axes=[2.15,4.30,6.42,8.52,10.60]
  ground=[(2.95,.78,3.0,2.29),(6.42,.25,1.0,2.30),(9.45,.78,2.9,2.29)]
  kh_storeys(m,w,x,y,L,a,S,axes,axes,ground)
  quoins(m,x,y,-L/2+.01,.68,8.55,a,ST,1,.42,.65,.35)
  steps36(m,x,y,S(6.42),a,1.6,1.2,.25,2,.50,M['Stone'])
sl=roof34(m,'kh',M['Tile'],RN)
for w in walls('kh'):
 if kind36(w)=='sodra':
  x,y,L,a=sf_edge(w['p'],w['q']);cx,cy,_=lp(x,y,-L/2+6.8,.355-1.0,0,a)
  box(m,cx,cy,.60,.90,11.9-9.6,9.6,RN,a,M['Dark'])
rear35(m,'crr',CRM,M['Brown'],M['Tile'],2)
b36_finish(m,'92379286')

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
# The cameras keep their measured distance from the modelled facade (0.355 m proud of the OSM line).
block36_cameras=[
 sv_camera('205_Block36_Cal_Cream',-153.92,-73.205,2.25,152,0),
 sv_camera('206_Block36_Cal_Cream_Roof',-153.92,-73.205,2.25,152,28),
 sv_camera('207_Block36_Cal_Cream_East',-153.92,-73.205,2.25,120,0),
 sv_camera('208_Block36_Cal_Cream_West',-164.43,-72.955,2.25,152,0),
 sv_camera('209_Block36_Cal_Corner',-175.10,-72.775,2.34,152,0),
 sv_camera('210_Block36_Cal_Corner_Roof',-175.10,-72.775,2.34,152,28),
 sv_camera('211_Block36_Cal_Corner_Kagg',-185.90,-72.585,2.30,150,0),
 ('212_Block36_Aerial',(-150.0,-52.0,34.0),(-162.0,-86.0,6.0),28),
]
print('BLOCK36_GEOMETRY',len(block36_names))
