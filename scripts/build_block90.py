"""Pass 90: the north side of east Storgatan between Proviantgatan and the brick corner house:
- 93192351: the red boarded cottage on a grey plinth: three white-framed casements, white corner
  boards, a hipped red tile roof with a break below the top, an arched red dormer and two
  chimneys; a low rear part behind;
- 93192354: the two-storey boarded pair, mirror-symmetric about its middle joint: the grey west
  half with vertical boards and the white east half with horizontal boards, each with three
  casements below, a large three-light window and a smaller one above, a storey band, a gabled
  dormer on each half and a snow guard along the eaves;
- 93192423: the cream boarded two-storey house with brown frames, a central olive double door on a
  step, four casements below, five above (with panels under the glass), a storey band, two gabled
  dormers and a brick chimney; the rear wing behind;
- 93192353: the ochre rendered house with its gable on the street: white bargeboards and corner
  pilasters, two casements on each floor;
- 93192374: the low boarded link with the white carriage gate, and the three-storey brick and
  stucco house from the 1890s: a granite plinth, a rusticated stucco ground floor with an arched
  red door and four arched windows, a stucco band, brick upper floors with stucco surrounds and
  heads, a cornice under the arched top-floor windows, the main cornice, quoins at the west corner.

References: Google Street View April 2025 (four panoramas on Storgatan, resected on house joints and
window rows), view only. Zones: source/block90.json; see references/block90-notes.md. Lamps, signs,
the parking meter, the cabinet, the satellite dish and downpipes are omitted.
"""
B90D=json.loads((R/'source/block90.json').read_text());Z=B90D['zones']
block90_names=[];B90={}
for old in [k for k in list(materials) if k.startswith('M_Block90_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Falu','TownIvory',(.55,.20,.15),.82,0),('GreyBoard','TownIvory',(.68,.72,.76),.80,0),('WhiteBoard','TownIvory',(.87,.87,.85),.80,0),
 ('Cream','TownIvory',(.92,.87,.68),.80,0),('Ochre','TownIvory',(.92,.74,.53),.88,0),('YellowBoard','TownIvory',(.85,.71,.45),.80,0),
 ('Brick','TownTileRed',(.60,.30,.24),.88,0),('PaleRender','TownIvory',(.86,.83,.74),.88,0),('Stucco','TownIvory',(.88,.77,.55),.88,0),
 ('WhiteFrame','TownPaintWhite',(.95,.95,.93),.55,0),('GreyTrim','TownPaintWhite',(.83,.83,.81),.60,0),('Teak','TownPaintBrown',(.58,.36,.18),.60,0),
 ('RedFrame','TownPaintBrown',(.62,.17,.13),.60,0),('Olive','TownPaintGreen',(.47,.49,.38),.60,0),('DormerRed','TownPaintBrown',(.55,.25,.18),.60,0),
 ('PlinthGreen','TownStone',(.38,.40,.35),.85,0),('Stone','TownStone',(.73,.71,.68),.90,0),('Granite','TownStone',(.55,.50,.48),.88,0),
 ('Tile','TownTileRed',(.78,.40,.26),.80,0),('Roof','TownMetalGrey',(.30,.31,.33),.55,.30),('Chimney','TownTileRed',(.62,.34,.26),.85,0),
 ('Iron','TownMetalGrey',(.08,.08,.085),.45,.40),('Dark','TownMetalGrey',(.05,.055,.06),.40,.20),
 ]:
 name='M_Block90_'+key;B90[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block90_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M=B90;WF=M['WhiteFrame']

def b90_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block90_names.append(name);return Mesh(name,category)
def drop_degenerate_faces90(obj,tol=1e-9):
 # The FBX export with tangent frames fails on zero-area faces or faces with a repeated corner.
 import bmesh
 bm=bmesh.new();bm.from_mesh(obj.data)
 # Also slivers thinner than 0.1 mm (two corners almost on top of each other along a long edge).
 def _thin(f):
  L=max(e.calc_length() for e in f.edges);return L>0 and 2*f.calc_area()/L<1e-4
 bad=[f for f in bm.faces if f.calc_area()<tol or len({v.index for v in f.verts})<len(f.verts) or _thin(f)]
 if bad:bmesh.ops.delete(bm,geom=bad,context='FACES_ONLY')
 bm.to_mesh(obj.data);bm.free();obj.data.update();return len(bad)
def b90_finish(m,osm):
 obj=s21_finish(m);obj['block90_dropped_faces']=drop_degenerate_faces90(obj);print('BLOCK90_DROPPED',obj.name,obj['block90_dropped_faces']);obj['detail_pass']=90;obj['reference_notes']='references/block90-notes.md';obj['osm_way']=osm;return obj
FR90={k:tuple(map(tuple,v)) for k,v in B90D['fronts'].items()}
def U90(F,X):
 # Position along the front wall F (from its middle) of the front point at model x X.
 (ax,ay),(bx,by)=F;t=(X-ax)/(bx-ax);return U({'p':[ax,ay],'q':[bx,by]},X,ay+t*(by-ay))
def Uw90(w,X):
 # Position along wall w (from its middle) of the point on its line at model x X.
 (px,py),(qx,qy)=w['p'],w['q'];t=(X-px)/(qx-px);return U(w,X,py+t*(qy-py))
def hboards90(m,x,y,L,a,z0,z1,holes,ma,step=.19):
 # Horizontal weatherboarding: thin laps, cut round the openings.
 n=int((z1-z0)/step)
 for k in range(1,n):
  z=z0+k*(z1-z0)/n;segs=[(-L/2,L/2)]
  for hu,hb,hw,hh,hr in holes:
   if hb-.14<z<hb+hh+hr+.16:segs=[(l0,h0) for l,h_ in segs for l0,h0 in ((l,min(h_,hu-hw/2-.15)),(max(l,hu+hw/2+.15),h_)) if h0-l0>.05]
  for l0,h0 in segs:facade_box(m,x,y,(l0+h0)/2,.37,z,h0-l0,.03,.035,ma,a)
def win90(m,x,y,u,b,w,h,a,frame,sur,rows=3):
 cas81(m,x,y,u,b,w,h,a,frame,.16,rows);surround36(m,x,y,u,b,w,h,a,sur,.10,.40);facade_box(m,x,y,u,.47,b-.05,w+.24,.16,.06,sur,a)
def big90(m,x,y,u,b,w,h,a,frame,sur):
 # The large three-light window with a transom.
 facade_box(m,x,y,u,.12,b+h/2,w,.02,h,GLAZE,a)
 for k in range(4):facade_box(m,x,y,u-w/2+.04+k*(w-.08)/3,.16,b+h/2,.07,.08,h,frame,a)
 for zz in (b+.04,b+h*.72,b+h-.04):facade_box(m,x,y,u,.16,zz,w,.08,.07,frame,a)
 surround36(m,x,y,u,b,w,h,a,sur,.12,.40);facade_box(m,x,y,u,.47,b-.05,w+.28,.16,.06,sur,a);facade_box(m,x,y,u,.44,b+h+.18,w+.34,.14,.12,sur,a)
def arch90(m,x,y,u,b,w,h,r,a,frame,sur,bars=True):
 # A round-headed opening: glass, a frame round the arch, a mullion and a transom at the spring.
 k=12;arc=[(u+w/2*math.cos(math.pi*i/k),b+h+r*math.sin(math.pi*i/k)) for i in range(k+1)]
 facade_box(m,x,y,u,.14,b+h/2,w,.02,h,GLAZE,a)
 m.faces([lp(x,y,uu,.14,zz,a) for uu,zz in arc],[tuple(range(k+1)),tuple(range(k,-1,-1))],GLAZE)
 town_path(m,[lp(x,y,uu,.18,zz,a) for uu,zz in arc],.05,frame)
 for s in (-1,1):facade_box(m,x,y,u+s*(w/2-.04),.18,b+h/2,.08,.08,h,frame,a)
 facade_box(m,x,y,u,.18,b+.04,w,.08,.08,frame,a)
 if bars:
  facade_box(m,x,y,u,.18,b+h,w,.08,.07,frame,a);facade_box(m,x,y,u,.18,b+(h+r)/2,.07,.08,h+r,frame,a)
 if sur:town_path(m,[lp(x,y,u+(w/2+.12)*math.cos(math.pi*i/k),.42,b+h+(r+.12)*math.sin(math.pi*i/k),a) for i in range(k+1)],.10,sur)
def gable90(m,x,y,u,w,z,rise,a,ma,o0=.005,o1=.355):
 # A gable triangle in the facade plane (between o0 and o1), base w at height z.
 prof=[(u-w/2,z),(u+w/2,z),(u,z+rise)];vs=[lp(x,y,uu,o,zz,a) for o in (o0,o1) for uu,zz in prof]
 m.faces(vs,[(2,1,0),(3,4,5),(0,1,4,3),(1,2,5,4),(2,0,3,5)],ma)
def gdormer90(m,x,y,u,a,H,slope,w,h,body,face,frame,roof,back=1.0,rise=.75):
 # A gabled dormer standing on the slope: box, front gable with bargeboards, saddle lid, window.
 zb=H+(back+.40-.355+.05)*slope-.15;zt=zb+h+.50;dep=2.4;o=.355-back
 box(m,*lp(x,y,u,o-dep/2,0,a)[:2],w,dep,zt-zb,zb,body,a)
 facade_box(m,x,y,u,o+.01,(zb+zt)/2,w-.02,.02,zt-zb,face,a)
 m.faces([lp(x,y,u-w/2,o+.01,zt,a),lp(x,y,u+w/2,o+.01,zt,a),lp(x,y,u,o+.01,zt+rise,a)],[(0,1,2),(2,1,0)],face)
 for s in (-1,1):
  e=w/2+.18;m.faces([lp(x,y,u+s*e,o+.2,zt-.12,a),lp(x,y,u,o+.2,zt+rise+.05,a),lp(x,y,u,o-dep,zt+rise+.05,a),lp(x,y,u+s*e,o-dep,zt-.12,a)],[(0,1,2,3),(3,2,1,0)],roof)
  town_path(m,[lp(x,y,u+s*e,o+.17,zt-.14,a),lp(x,y,u,o+.17,zt+rise+.02,a)],.05,WF)
 facade_box(m,x,y,u,o+.02,zb+.30+h/2,w-.6,.02,h,GLAZE,a);cas81(m,x,y,u,zb+.30,w-.6,h,a,frame,o+.06,2)
def adormer90(m,x,y,u,a,H,slope,w,h,body,frame,roof,back=1.0):
 # A dormer under a segmental (arched) roof, with a round-headed window.
 zb=H+(back+.40-.355+.05)*slope-.15;zt=zb+h+.40;dep=2.2;o=.355-back
 box(m,*lp(x,y,u,o-dep/2,0,a)[:2],w,dep,zt-zb,zb,body,a)
 k=8;r=w/2+.12;pts=[(r*math.cos(math.pi*i/k),.35*w*math.sin(math.pi*i/k)) for i in range(k+1)]
 for (u0,z0),(u1,z1) in zip(pts,pts[1:]):
  m.faces([lp(x,y,u+u0,o+.15,zt+z0,a),lp(x,y,u+u1,o+.15,zt+z1,a),lp(x,y,u+u1,o-dep,zt+z1,a),lp(x,y,u+u0,o-dep,zt+z0,a)],[(0,1,2,3),(3,2,1,0)],roof)
 m.faces([lp(x,y,u+pu,o+.005,zt+pz,a) for pu,pz in pts],[tuple(range(k+1)),tuple(range(k,-1,-1))],body)
 arch90(m,x,y,u,zb+.30,w-.5,h-.2,.25,a,frame,None,False)
def flat90(m,zone,ma,lift=.02):
 z=Z[zone]['height']+lift
 for g in Z[zone]['polygons']:m.faces([(*v,z) for v in g],[tuple(range(len(g))),tuple(range(len(g)-1,-1,-1))],ma)
def snow90(m,x,y,L,a,z,back=.9):
 # The snow guard: two rails on posts a little up the slope.
 for zz in (z+.18,z+.32):town_rod(m,lp(x,y,-L/2,.355-back,zz,a),lp(x,y,L/2,.355-back,zz,a),.02,M['Dark'],6)
 for k in range(int(L/1.2)+1):town_rod(m,lp(x,y,-L/2+k*L/int(L/1.2),.355-back,z,a),lp(x,y,-L/2+k*L/int(L/1.2),.355-back,z+.34,a),.02,M['Dark'],6)

# The fronts. Openings: (kind, x on the front, bottom, width, height, extra); kinds: win (casement,
# extra = rows), big (three lights and a transom), panel (casement over a panel, extra = panel
# height), door, gate, arch (round head, extra = rise), adoor (round-headed door). Positions and
# heights from the resected panoramas; see the notes for the estimates.
PAIR90=lambda X0,sg:[('win',X0+sg*k,1.22,1.35,1.50,3) for k in (1.45,3.25,5.75)]
F90={'cf':dict(front='51',wall='Falu',frame='WhiteFrame',sur='WhiteFrame',trim='WhiteFrame',plinth=.30,pm='Stone',boards='v',
  ops=[('win',X,1.0,1.40,1.50,2) for X in (189.6,191.8,194.1)])}
F90['pg']=dict(front='54',wall='GreyBoard',frame='WhiteFrame',sur='GreyTrim',trim='GreyTrim',plinth=.50,pm='Stone',boards='v',band=(2.90,.16),
  ops=PAIR90(208.45,-1)+[('big',206.0,3.55,2.30,2.10,0),('win',202.45,3.75,1.50,1.70,3)])
F90['pw']=dict(F90['pg'],wall='WhiteBoard',boards='h',ops=PAIR90(208.45,1)+[('big',210.9,3.55,2.30,2.10,0),('win',214.45,3.75,1.50,1.70,3)])
F90['kf']=dict(front='23',wall='Cream',frame='Teak',sur='GreyTrim',trim='GreyTrim',plinth=.35,pm='PlinthGreen',boards='v',band=(2.78,.25),
  ops=[('win',X,1.10,1.20,1.50,3) for X in (218.4,220.25,225.3,227.2)]+[('panel',X,3.10,1.20,1.90,.58) for X in (218.4,220.3,225.3,227.2)]+
  [('panel',222.8,3.10,1.40,1.90,.58),('door',222.8,.37,1.55,2.25,'Olive')])
F90['og']=dict(front='53',wall='Ochre',frame='WhiteFrame',sur='WhiteFrame',trim='WhiteFrame',plinth=.30,pm='Stone',boards=None,
  ops=[('win',X,.65,1.20,1.30,3) for X in (230.65,233.15)]+[('win',X,2.95,1.20,1.30,3) for X in (230.65,233.15)])
F90['lk']=dict(front='74',wall='YellowBoard',frame='WhiteFrame',sur='WhiteFrame',trim='WhiteFrame',plinth=.15,pm='Stone',boards='v',
  ops=[('gate',236.48,.05,2.25,2.35,0)])
BAYS=[246.05+3.1*k for k in (-2,-1,0,1,2)]
F90['bk']=dict(front='74',wall='Brick',frame='RedFrame',sur='Stucco',trim='Stucco',plinth=.63,pm='Granite',boards=None,
  ops=[('adoor',BAYS[0],.05,2.30,2.60,1.10)]+[('arch',X,1.66,1.50,1.45,.60) for X in BAYS[1:]]+[('win',X,5.62,1.40,2.05,3) for X in BAYS]+[('arch',X,9.65,1.10,1.25,.55) for X in BAYS])
STREET90={'cf','pg','pw','kf','og','lk','bk'}

meshes={}
for zone,spec in Z.items():
 nm=spec['mesh']
 if nm not in meshes:meshes[nm]=b90_new(nm,'Kvarnholmen/Storgatan')
for zone,spec in Z.items():
 m=meshes[spec['mesh']];H=spec['height'];f=F90.get(zone)
 wm=M[f['wall']] if f else M[{'cr':'Falu','kr':'Cream','br':'Brick'}[zone]]
 for w in walls(zone):
  if w['kind']!='outer':bz_wall(m,w['p'],w['q'],w['z0'],H,[],wm);continue
  x,y,L,a=sf_edge(w['p'],w['q']);ox,oy=outward(w)
  if not f or oy>-.9 or zone not in STREET90:
   plain(m,w,H,M['PaleRender'] if zone in ('pg','pw') and abs(ox)>.9 else wm,WF if zone!='kr' else M['Teak'],M['GreyTrim'],2 if H>5 else 1,.9 if H>5 else .8);continue
  Fr=FR90[f['front']]
  mine=[(k,Uw90(w,X),b,ww,hh,ex) for k,X,b,ww,hh,ex in f['ops']]
  mine=[o for o in mine if abs(o[1])+o[3]/2<=L/2+.01]
  if zone=='bk':
   # Stucco below the band, brick above; arched heads cut as round-topped holes.
   hz=lambda lo,hi:[(u,b,ww,hh,(ex if k in ('arch','adoor') else 0)) for k,u,b,ww,hh,ex in mine if lo<=b<hi]
   bz_wall(m,w['p'],w['q'],0,5.52,hz(0,5.5),M['Stucco']);bz_wall(m,w['p'],w['q'],5.52,H,hz(5.5,20),wm)
   holes=hz(0,20)
  else:
   holes=[(u,b,ww,hh,0) for k,u,b,ww,hh,ex in mine];bz_wall(m,w['p'],w['q'],0,H,holes,wm)
  top=H-(.95 if zone=='kf' else .20)
  if f['boards']=='v':boards82(m,x,y,L,a,f['plinth']+.02,top,holes,wm)
  elif f['boards']=='h':hboards90(m,x,y,L,a,f['plinth']+.02,top,holes,wm)
  fm,sm=M[f['frame']],M[f['sur']]
  for k,u,b,ww,hh,ex in mine:
   if k=='win':
    if zone=='bk':
     cas81(m,x,y,u,b,ww,hh,a,fm,.16,ex);surround36(m,x,y,u,b,ww,hh,a,sm,.16,.42)
     facade_box(m,x,y,u,.50,b-.10,ww+.5,.24,.14,sm,a);facade_box(m,x,y,u,.52,b+hh+.30,ww+.7,.30,.16,sm,a);facade_box(m,x,y,u,.46,b+hh+.15,ww+.4,.18,.20,sm,a)
    else:win90(m,x,y,u,b,ww,hh,a,fm,sm,ex)
   elif k=='big':big90(m,x,y,u,b,ww,hh,a,fm,sm)
   elif k=='panel':
    # Casement over a painted panel (the cream house's upper windows).
    facade_box(m,x,y,u,.16,b+ex/2,ww-.06,.06,ex,M['WhiteBoard'],a);win90(m,x,y,u,b+ex,ww,hh-ex,a,fm,sm,3)
    facade_box(m,x,y,u,.18,b+ex,ww,.08,.07,fm,a)
   elif k=='door':
    door83(m,x,y,u,b,ww,hh,a,M[ex],M[ex],False);surround36(m,x,y,u,b,ww,hh,a,sm,.12,.40);steps82(m,x,y,u,ww,b,a,M['Stone'])
    facade_box(m,x,y,u,.44,b+hh+.20,ww+.4,.14,.16,sm,a)
   elif k=='gate':gate83(m,x,y,u,b,ww,hh,a,WF,WF)
   elif k=='arch':arch90(m,x,y,u,b,ww,hh,ex,a,fm,sm)
   elif k=='adoor':
    # The red double door: panelled leaves with grilled lights, a fanlight in the arch.
    for s2 in (-1,1):
     facade_box(m,x,y,u+s2*ww/4,.12,b+hh/2,ww/2-.04,.07,hh,fm,a)
     facade_box(m,x,y,u+s2*ww/4,.16,b+hh*.66,ww/2-.40,.02,hh*.45,M['Dark'],a)
    arch90(m,x,y,u,b+hh-.01,ww,.01,ex,a,fm,sm,False)
    k2=12;m.faces([lp(x,y,u+ww/2*math.cos(math.pi*i/k2),.14,b+hh+ex*math.sin(math.pi*i/k2),a) for i in range(k2+1)],[tuple(range(k2+1)),tuple(range(k2,-1,-1))],GLAZE)
  # Plinth (with gaps at the doors and the gate), corner boards, the storey band, eaves.
  at=-L/2
  for lo,hi in sorted((u-ww/2,u+ww/2) for k,u,b,ww,hh,ex in mine if b<f['plinth'])+[(L/2,L/2)]:
   if lo>at+.03:facade_box(m,x,y,(at+lo)/2,.39,f['plinth']/2,lo-at,.08 if zone!='bk' else .14,f['plinth'],M[f['pm']],a)
   at=max(at,hi)
  if zone=='bk':
   # Rustication grooves on the ground floor, the band, the cornices, the quoins.
   for zz in [.63+k*.46 for k in range(1,9)]:
    at=-L/2
    for lo,hi in sorted((u-ww/2-.25,u+ww/2+.25) for k,u,b,ww,hh,ex in mine if b<zz<b+hh+ex)+[(L/2,L/2)]:
     if lo>at+.03:facade_box(m,x,y,(at+lo)/2,.37,zz,lo-at,.04,.035,M['Granite'],a)
     at=max(at,hi)
   facade_box(m,x,y,0,.46,4.95,L+.1,.22,1.12,M['Stucco'],a);facade_box(m,x,y,0,.56,5.45,L+.2,.30,.14,M['Stucco'],a)
   facade_box(m,x,y,0,.52,9.18,L+.1,.34,.36,M['Stucco'],a);facade_box(m,x,y,0,.60,9.42,L+.2,.44,.12,M['Stucco'],a)
   for X in BAYS:facade_box(m,x,y,Uw90(w,X),.47,7.05,.24,.20,1.0,M['Stucco'],a)
   for X in BAYS[:-1]:facade_box(m,x,y,Uw90(w,X+1.55),.44,11.35,.55,.16,3.5,M['Stucco'],a)
   facade_box(m,x,y,0,.62,H-.30,L+.3,.55,.60,M['Stucco'],a);facade_box(m,x,y,0,.80,H-.04,L+.5,.80,.10,M['Stucco'],a)
   for k in range(int(L/.55)):facade_box(m,x,y,-L/2+.3+k*L/int(L/.55),.62,H-.66,.12,.40,.14,M['Stucco'],a)
   for k,zz in enumerate([5.5+j*.55 for j in range(14)]):
    if zz+.5<H-.6:facade_box(m,x,y,-L/2+(.40 if k%2 else .55),.44,zz+.25,.80 if k%2 else 1.1,.14,.48,M['Stucco'],a)
   continue
  if f['boards'] or zone=='og':
   for uu in (-L/2+.12,L/2-.12):facade_box(m,x,y,uu,.42,(H+f['plinth'])/2,.24 if zone!='og' else .36,.10,H-f['plinth'],M[f['trim']],a)
  if 'band' in f:
   zb,hb=f['band'];facade_box(m,x,y,0,.43,zb+hb/2,L,.12,hb,M[f['trim']],a)
  if zone=='kf':
   # The frieze under the eaves: a broad board and a moulding.
   facade_box(m,x,y,0,.40,H-.48,L,.07,.85,wm,a);facade_box(m,x,y,0,.44,H-.92,L,.06,.08,M['GreyTrim'],a)
  if zone in ('lk',):
   facade_box(m,x,y,0,.42,H-.12,L+.1,.14,.24,WF,a);town_rod(m,lp(x,y,-L/2,.66,H-.05,a),lp(x,y,L/2,.66,H-.05,a),.06,WF,8)
  elif zone!='og':
   facade_box(m,x,y,0,.46,H-.12,L+.1,.14,.24,WF if zone=='cf' else M['GreyTrim'],a);town_rod(m,lp(x,y,-L/2,.70,H-.02,a),lp(x,y,L/2,.70,H-.02,a),.07,M['GreyTrim'] if zone!='cf' else WF,8)

# Roofs and roof furniture.
# The cottage: a hipped roof with a break: a steep lower ring, then a flatter top.
m=meshes['SM_Kvarnholmen_House_93192351'];F51=FR90['51']
r,Ls,Lt=rect82('cf',*F51);H=Z['cf']['height'];T=Z['cf']['top']
outer,inner=inset_roof(m,r,H,1.9,2.55,M['Tile'],.40)
inset_roof(m,inner,H+2.55,min(Ls,Lt)/2-1.9-.25,T-H-2.55,M['Tile'],0.0)
sl_cf=2.55/(1.9+.40);x,y,L,a=sf_edge(*F51)
adormer90(m,x,y,U90(F51,193.4),a,H,sl_cf,1.35,1.05,M['DormerRed'],WF,M['Tile'],.8)
d,n=frame82(*F51)
for X,t,z0,z1 in ((196.2,1.6,H+1.0,H+2.4),(191.2,4.6,T-.4,T+.6)):
 P=(X+n[0]*t,F51[0][1]+n[1]*t);box(m,P[0],P[1],.55,.55,z1-z0,z0,M['Ochre' if X>195 else 'Chimney'],0,M['Dark'])
flat90(m,'cr',M['Dark'])
# The boarded pair: one saddle roof along the street, a gabled dormer on each half, snow guards.
m=meshes['SM_Kvarnholmen_House_93192354'];F54=FR90['54']
for zone in ('pg','pw'):saddle82(m,zone,*F54,M['Roof'],M['GreyBoard' if zone=='pg' else 'WhiteBoard'],along=True,ov=.40)
r,Ls,Lt=rect82('pg',*F54);H=Z['pg']['height'];sl_p=(Z['pg']['top']-H)/(Lt/2);x,y,L,a=sf_edge(*F54)
for X in (202.4,214.5):gdormer90(m,x,y,U90(F54,X),a,H,sl_p,2.0,1.0,M['DormerRed'],M['WhiteBoard'],WF,M['Roof'])
snow90(m,x,y,L,a,H+.75*sl_p)
# The cream house: saddle roof, two gabled dormers, the chimney, snow guard; flat rear wing.
m=meshes['SM_Kvarnholmen_House_93192423'];F23=FR90['23']
saddle82(m,'kf',*F23,M['Roof'],M['Cream'],along=True,ov=.40)
r,Ls,Lt=rect82('kf',*F23);H=Z['kf']['height'];sl_k=(Z['kf']['top']-H)/(Lt/2);x,y,L,a=sf_edge(*F23)
for X in (218.35,223.3):gdormer90(m,x,y,U90(F23,X),a,H,sl_k,2.1,1.0,M['DormerRed'],M['Cream'],M['Teak'],M['Roof'])
box(m,221.9,3.4,.60,.60,Z['kf']['top']+.7-(H+2.4*sl_k),H+2.4*sl_k,M['Chimney'],0,M['Dark'])
snow90(m,x,y,L,a,H+.75*sl_k)
flat90(m,'kr',M['Roof'])
# The ochre house: a saddle roof with its gable on the street, white bargeboards on the front gable.
m=meshes['SM_Kvarnholmen_House_93192353'];F53=FR90['53']
saddle82(m,'og',*F53,M['Tile'],M['Ochre'],along=False,ov=.35)
H,T=Z['og']['height'],Z['og']['top'];x,y,L,a=sf_edge(*F53)
gable90(m,x,y,0,L,H,T-H,a,M['Ochre'])
for s2 in (-1,1):
 town_path(m,[lp(x,y,s2*(L/2+.35),.50,H-.25,a),lp(x,y,0,.50,T+.10,a)],.09,WF)
 facade_box(m,x,y,s2*(L/2-.6),.45,H-.05,1.2,.18,.18,WF,a)
facade_box(m,x,y,0,.40,H+.10,L-2.0,.10,.12,WF,a)
# The link: a flat roof. The brick house: a low saddle roof behind the cornice; flat rear parts.
m=meshes['SM_Kvarnholmen_House_93192374'];F74=FR90['74']
flat90(m,'lk',M['Roof']);flat90(m,'br',M['Roof'])
saddle82(m,'bk',(238.5,.4),(253.6,.3),M['Roof'],M['Brick'],along=True,ov=.20)
for nm in meshes:b90_finish(meshes[nm],nm.split('_')[-1])

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block90_cameras=[
 sv_camera('441_Block90_Cal_Cottage',190.93,-5.01,2.40,332,15,90),
 sv_camera('442_Block90_Cal_Pair',208.55,-4.12,2.40,332,15,90),
 sv_camera('443_Block90_Cal_Cream',218.73,-4.48,2.40,332,15,90),
 sv_camera('444_Block90_Cal_Brick',240.43,-4.80,2.40,332,20,90),
 ('445_Block90_Aerial',(222.0,-34.0,24.0),(222.0,6.0,4.0),24),
]
print('BLOCK90_GEOMETRY',len(block90_names))
