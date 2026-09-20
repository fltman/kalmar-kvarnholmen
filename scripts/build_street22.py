"""Four individually authored northern street elevations. See street22 source notes."""
code=(R/'scripts/build_street21.py').read_text();exec(compile(code[:code.index('# South-west Kaggensgatan corner:')],'street21_joinery','exec'))
BASE21=json.loads((R/'source/street22-base.json').read_text())['meshes'];street22_names=street21_names;S22={}
for key,texture,base,col,rough,metal in [
 ('Clinker','Street22Clinker',(.43,.235,.155),(.43,.235,.155),.78,0),
 ('PaleOchre','TownIvory',(.68,.65,.55),(.66,.60,.43),.84,0),
 ('OfficeRender','TownIvory',(.68,.65,.55),(.61,.53,.37),.85,0),
 ('Aggregate','TownStone',(.38,.355,.31),(.44,.40,.30),.88,0),
 ('RoseAggregate','TownStone',(.38,.355,.31),(.50,.29,.22),.88,0),
 ('Timber','TownPaintBrown',(.19,.105,.065),(.31,.20,.105),.58,0),
 ('DarkMetal','TownMetalGrey',(.115,.15,.132),(.10,.12,.11),.44,.45),
 ('BlueCanvas','TownPanel',(.57,.58,.49),(.035,.12,.32),.90,0),
 ]:
 name='M_Street22_'+key;S22[key]=name
 if name in materials:continue
 mat(name,col,rough,metal,texture);tint=[t/b for t,b in zip(col,base)];specs[name]['street16_tint']=tint
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])

def s22_finish(m):
 obj=s21_finish(m);obj['detail_pass']=22;obj['reference_notes']='references/street22-notes.md';obj['category']='Kvarnholmen/Kaggensgatan and Larmgatan';return obj

def s22_recess(m,x,y,u,b,w,h,a,frame):
 # Actual 0.65 m entrance setback, with jambs, soffit and walkable landing.
 for side in [-1,1]:facade_box(m,x,y,u+side*(w/2-.035),-.11,b+h/2,.07,.90,h,S21['Concrete'],a)
 facade_box(m,x,y,u,-.11,b+h-.035,w,.90,.07,S21['Concrete'],a)
 facade_box(m,x,y,u,-.11,b-.03,w,.90,.06,TS,a)
 xx,yy,_=lp(x,y,u,-.67,0,a);s21_glass(m,xx,yy,0,b,w-.13,h-.07,a,frame,2,.84,True)

def s22_boxbay(m,x,y,u,b,w,h,a,frame,projection=.70):
 # A closed, supported rectangular oriel with glass returns and visible mullions.
 for z in [b-.07,b+h+.07]:facade_box(m,x,y,u,.38+projection/2,z,w+.18,projection+.22,.14,frame,a)
 for side in [-1,1]:
  facade_box(m,x,y,u+side*(w/2+.025),.39+projection,b+h/2,.055,.10,h,frame,a)
  m.faces([lp(x,y,u+side*w/2,o,z,a) for o,z in [(.36,b),(.38+projection,b),(.38+projection,b+h),(.36,b+h)]],[(0,1,2,3)],GLAZE)
 xx,yy,_=lp(x,y,u,projection+.10,0,a);s21_glass(m,xx,yy,0,b,w,h,a,frame,1,.20)

def s22_panelgrid(m,x,y,L,H,a,ma,holes,step=3.4):
 # Shallow concrete perimeter ribs around recessed aggregate fields.
 p18_face(m,x,y,L,H,holes,ma,a)
 n=max(1,round(L/step))
 for k in range(n+1):facade_box(m,x,y,-L/2+k*L/n,.405,H/2,.22,.20,H,S21['Concrete'],a)
 for z,hh in [(3.28,.25),(7.55,.22),(H-.12,.23)]:facade_box(m,x,y,0,.42,z,L,.24,hh,S21['Concrete'],a)
 for z in [H+.01,H+.15]:facade_box(m,x,y,0,.52,z,L,.38,.09,S22['DarkMetal'],a)
 for k in range(round(L/.75)):facade_box(m,x,y,-L/2+(k+.5)*L/round(L/.75),.65,H-.20,.09,.59,.23,S22['DarkMetal'],a)

# Pale three-storey Kaggensgatan/Fiskaregatan corner, with a chamfered shop door.
name='SM_Kvarnholmen_House_92204184';m=s21_new(name);H=10.10;corner=(-179.025,135.276);ch=1.6
for w in D21[name]['walls']:
 p,q=list(w['p']),list(w['q']);north=p[1]>134.7 and q[1]>135;west=p[0]<-179 and q[0]<-179
 if north:q=[q[0]+ch,q[1]-.04]
 if west:p=[p[0]-.04,p[1]-ch]
 ww=dict(w,p=p,q=q);x,y,L,a=s21_edge(ww)
 if not(north or west):s21_rear(m,ww,H,S22['PaleOchre'],3);continue
 n=5;step=L/n;us=[-L/2+(k+.5)*step for k in range(n)]
 hs=[(u,b,1.28,hh,0) for u in us for b,hh in [(4.05,2.05),(7.30,1.70)]]
 hs += [(u,.35,step-.65,2.78,0) for u in us]
 p18_face(m,x,y,L,H,hs,S22['PaleOchre'],a);s20_plinth(m,x,y,L,a,hs,.36)
 for u,b,ww,hh,r in hs:
  if b>4:s20_window(m,x,y,u,b,ww,hh,a,TW,TW,.69 if b<6 else 1.0)
  else:s21_glass(m,x,y,u,b,ww,hh,a,S22['Timber'],2,.83)
 p18_band(m,x,y,L,3.57,a,TW,.22);s20_eaves(m,x,y,L,H,a,TW)
 for u in us:s21_shallow_awning(m,x,y,u,3.39,step-.45,a,S21['WarmCream'],.83)
 for u in [-L*.27,L*.27]:s21_dormer(m,x,y,u,H+.55,1.80,1.06,a,town_mats['MetalRed'])
p=(-177.425,135.236);q=(-179.065,133.676);x,y,L,a=sf_edge(p,q)
hs=[(0,.18,1.45,2.95,0),(0,4.05,1.32,2.05,0),(0,7.30,1.32,1.7,0)]
p18_face(m,x,y,L,H,hs,S22['PaleOchre'],a);s22_recess(m,x,y,0,.18,1.45,2.95,a,S22['Timber'])
for b,hh in [(4.05,2.05),(7.30,1.70)]:s20_window(m,x,y,0,b,1.32,hh,a,TW,TW,.69 if b<6 else 1.0)
p18_band(m,x,y,L,3.57,a,TW,.22);s20_eaves(m,x,y,L,H,a,TW)
# Keep roof skin only: the former square-corner gutter must not project
# across the new chamfer. Clip its roof to the same diagonal as the facade.
b=BASE21[name];oldH=D21[name]['H'];p=(-177.425,135.236);q=(-179.065,133.676)
def chamfer_distance(v):return (q[0]-p[0])*(v[1]-p[1])-(q[1]-p[1])*(v[0]-p[0])
for indices,mi,smooth in b['faces']:
 if b['materials'][mi]!=TT:continue
 vs=[(xx,yy,H+(zz-oldH)) for xx,yy,zz in [b['vertices'][i] for i in indices]]
 if min(v[2] for v in vs)<H-.035:continue
 clipped=[];crossings=[]
 for start,end in zip(vs,vs[1:]+vs[:1]):
  ds,de=chamfer_distance(start),chamfer_distance(end)
  if ds>=0:clipped.append(start)
  if (ds>=0)!=(de>=0):
   t=ds/(ds-de);hit=tuple(a+(bb-a)*t for a,bb in zip(start,end));clipped.append(hit);crossings.append(hit)
 if len(clipped)>=3:m.faces(clipped,[tuple(range(len(clipped)))],TT,smooth)
 if len(crossings)==2:
  aa,bb=crossings
  m.faces([aa,bb,(bb[0],bb[1],H),(aa[0],aa[1],H)],[(0,1,2,3)],S22['PaleOchre'])
s22_finish(m)

# Kaggensgatan 30: eight flat modern office bays and recessed shop entries.
# Rear wings and the short Fiskaregatan elevation stay outside this researched face.
name='SM_Kvarnholmen_House_92204157';m=s21_new(name,[(-181,-170.5,91.6,114.95,-1,40)]);H=9.8
x,y,L,a=sf_edge((-179.542,114.724),(-179.801,91.975));step=L/8;us=[-L/2+(k+.5)*step for k in range(8)]
hs=[(u,b,1.58,1.67,0) for u in us for b in [4.14,7.20]]
ground=[(-L/2+1.14,.28,1.55,2.70,0),(-L/2+3.55,.46,2.78,2.48,0),(-L/2+6.57,.46,2.78,2.48,0),(-L/2+9.10,.28,1.43,2.70,0),(-L/2+11.52,.46,2.85,2.48,0),(-L/2+14.58,.46,2.85,2.48,0),(-L/2+17.00,.28,1.43,2.70,0),(-L/2+19.53,.46,2.78,2.48,0),(-L/2+21.94,.28,1.20,2.70,0)]
hs+=ground;p18_face(m,x,y,L,H,hs,S22['OfficeRender'],a);s20_plinth(m,x,y,L,a,hs,.46)
for u,b,w,h,r in hs:
 if b<1 and w<1.7:s22_recess(m,x,y,u,b,w,h,a,S20['GreyFrame'])
 else:s21_glass(m,x,y,u,b,w,h,a,S22['DarkMetal'] if b>4 else S20['GreyFrame'],1 if b>4 else 2,.18 if b>4 else 0)
for k in range(9):facade_box(m,x,y,-L/2+k*step,.39,6.48,.10,.10,6.33,S21['WarmCream'],a)
for j,u in enumerate(us):
 for b in [4.14,7.20]:
  z=b+1.80;ma=S22['BlueCanvas'] if b<6 and j in [0,2,3,5] else S22['DarkMetal']
  facade_box(m,x,y,u,.47,z,1.78,.20,.11,ma,a)
  for side in [-1,1]:town_rod(m,lp(x,y,u+side*.78,.42,z-.17,a),lp(x,y,u+side*.78,.65,z-.48,a),.012,METAL)
facade_box(m,x,y,0,.42,3.34,L,.19,.55,S22['DarkMetal'],a)
facade_box(m,x,y,0,.46,H,L,.47,.19,S22['DarkMetal'],a)
for u in [-L/2+.13,L/2-.13]:sf_pipe(m,x,y,u,H,a,S21['White'])
points=[(-179.801,91.975),(-173.672,91.897),(-173.630,95.095),(-170.51,95.05),(-170.51,114.5),(-179.542,114.724)];s21_flat_roof(m,points,H,S22['DarkMetal']);s22_finish(m)

# Larmgatan 32: brick apron panels, white frame, timber triples and copper box bays.
name='SM_Kvarnholmen_House_92204172';m=s21_new(name);H=10.65
for w in D21[name]['walls']:
 x,y,L,a=s21_edge(w);west=x<-284; north=y>135.8
 if not(west or north):s21_rear(m,w,H,S21['White'],3);continue
 n=8 if west else 5;step=L/n;hs=[]
 for k in range(n):
  centre=-L/2+(k+.5)*step
  for b in [4.32,7.62]:
   for du in [-1.32,0,1.32]:hs.append((centre+du,b,1.11,1.63,0))
  hs.extend([(centre-.60,.43,step-1.78,2.58,0),(centre+step/2-.67,.19,1.10,2.82,0)])
 p18_face(m,x,y,L,H,hs,S21['White'],a);s20_plinth(m,x,y,L,a,hs,.43)
 for k in range(n):
  u=-L/2+(k+.5)*step
  for z,hh in [(3.73,1.03),(6.78,1.22),(9.86,.70)]:facade_box(m,x,y,u,.405,z,step-.30,.13,hh,S22['Clinker'],a)
  for edge in [-1,1]:facade_box(m,x,y,u+edge*(step/2-.09),.43,6.85,.18,.16,7.45,S21['White'],a)
  for b in [4.32,7.62]:
   for du in [-1.32,0,1.32]:
    if west and b>7 and k in [2,4,6] and du==0:s22_boxbay(m,x,y,u,b,1.11,1.63,a,S22['DarkMetal'],.62)
    else:s21_glass(m,x,y,u+du,b,1.11,1.63,a,S22['Timber'],1,.17)
   for du in [-.66,.66]:
    for j in [-1,0,1]:facade_box(m,x,y,u+du+j*.046,.42,b+.815,.025,.10,1.70,S22['Timber'],a)
  s21_glass(m,x,y,u-.60,.43,step-1.78,2.58,a,S22['Timber'],1,0)
  s22_recess(m,x,y,u+step/2-.67,.19,1.10,2.82,a,S22['Timber'])
  facade_box(m,x,y,u,.46,3.27,step-.10,.22,.47,S21['WarmCream'],a)
  if k%3==1:s21_shallow_awning(m,x,y,u,6.14,step-.50,a,S22['BlueCanvas'],.78)
  if west and k in [1,3,5,7]:s21_dormer(m,x,y,u,H+.45,1.13,1.15,a,S22['DarkMetal'])
 facade_box(m,x,y,0,.49,H-.02,L,.52,.29,S22['DarkMetal'],a)
 for u in [-L/2+.12,L/2-.12]:sf_pipe(m,x,y,u,H,a,METAL)
# Roof follows the footprint; corner attic is a broad, glazed raised dormer.
BASE21[name]['materials']=[S22['DarkMetal'] if q==TT else q for q in BASE21[name]['materials']]
s21_roof_reuse(m,name,H,.55)
x,y,L,a=sf_edge((-284.074,136.201),(-284.458,96.531));s21_dormer(m,x,y,-L/2+2.95,H+.12,4.1,2.15,a,S21['White'])
s22_finish(m)

# Shopping block's north-east corner. Preserve pass-21 low coloured southern wing.
name='SM_Kvarnholmen_House_92204173';m=s21_new(name,[(-209.2,-189.8,119.6,136.9,-1,40),(-221.8,-209.1,124.1,136.9,-1,40)]);H=11.2
# Exact mapped street edges: five Kaggensgatan bays, four grey and three rose Fiskaregatan bays.
for p,q,n,ma,is_east in [
 ((-191.078,119.6),(-190.917,135.286),5,S22['Aggregate'],True),
 ((-190.917,135.286),(-207.45,135.449),4,S22['Aggregate'],False),
 ((-207.45,135.449),(-221.8,135.590),4,S22['RoseAggregate'],False),
]:
 x,y,L,a=sf_edge(p,q);step=L/n;hs=[]
 for k in range(n):
  u=-L/2+(k+.5)*step;hs.extend([(u,.30,step-.40,2.76,0),(u,8.19,1.55,1.92,0)])
  if (is_east and k>=n-2) or (not is_east and ma==S22['Aggregate'] and k<2):hs.append((u,3.79,step-.42,3.10,0))
 s22_panelgrid(m,x,y,L,H,a,ma,hs,step)
 for u,b,w,h,r in hs:
  if b<1:s21_glass(m,x,y,u,b,w,h,a,S22['DarkMetal'],2,0,abs(u)<step)
  elif b>7:s21_glass(m,x,y,u,b,w,h,a,S22['DarkMetal'],2,0)
  else:s22_boxbay(m,x,y,u,b,w,h,a,S21['Concrete'],.52)
 # Deep sill and lintel outline each recessed, often blind, central panel.
 for k in range(n):
  u=-L/2+(k+.5)*step
  for z in [3.72,7.05]:facade_box(m,x,y,u,.42,z,step-.22,.19,.13,S21['Concrete'],a)
 # Low opaque store sign band, without guessing present-day tenants.
 facade_box(m,x,y,0,.48,3.38,L,.12,.22,S22['DarkMetal'],a)
for points in [[(-209.19,119.61),(-191.078,119.61),(-190.917,135.286),(-209.19,135.466)],[(-221.79,124.11),(-209.20,124.11),(-209.20,135.468),(-221.79,135.590)]]:s21_flat_roof(m,points,H,S22['DarkMetal'])
# Rear closure at the two scoped transitions, never a wall across either street.
for p,q in [((-209.19,135.46),(-209.19,119.61)),((-221.79,124.11),(-221.79,135.59))]:
 x,y,L,a=sf_edge(p,q);p18_face(m,x,y,L,H,[],S21['Concrete'],a)
s22_finish(m)

street22_cameras=[
 ('106_KaggensCorner22',(-186.4,144.0,2.1),(-174,131.8,5.3),20),
 ('107_KaggensOffice22',(-189.7,104.7,2.0),(-179.7,103.1,4.9),14),
 ('108_LarmBrick22',(-292.8,106.0,2.0),(-284.3,118.5,5.9),18),
 ('109_LarmCorner22',(-290.6,145.0,2.0),(-279,133.3,6.3),20),
 ('110_ShoppingCorner22',(-183.4,143.9,2.0),(-196.6,130.9,5.8),19),
 ('111_KaggensNorth22',(-185.1,98.0,1.85),(-183.7,133.6,4.2),26),
]
