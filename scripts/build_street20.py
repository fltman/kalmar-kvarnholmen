"""Six reference-specific street houses; dimensions estimated, mapped rear wings retained.
Research photographs are references only. No photographic pixels enter materials.
"""
import ast
street20_names=[]
street20_base=json.loads((R/'source/street20-base.json').read_text())['meshes']
for filename in ['build_town_details.py','town_detail_helpers.py','build_larmtorget_facades.py','build_sodra_facades.py','build_pass18_extra.py']:
 tree=ast.parse((R/'scripts'/filename).read_text())
 tree.body=[n for n in tree.body if isinstance(n,ast.FunctionDef)]
 exec(compile(tree,filename,'exec'))
exec(compile((R/'scripts/pass18_helpers.py').read_text(),'pass18_helpers.py','exec'))
S20={}
for key,texture,base,col,rough in [
 ('CreamWood','TownPanel',(.57,.58,.49),(.64,.625,.51),.74),
 ('HoneyWood','TownPanel',(.57,.58,.49),(.64,.49,.30),.74),
 ('Orange','TownIvory',(.68,.65,.55),(.59,.22,.055),.82),
 ('Ochre','TownYellow',(.63,.43,.19),(.69,.49,.22),.85),
 ('Pale','TownIvory',(.68,.65,.55),(.72,.70,.62),.82),
 ('RedFrame','TownPaintBrown',(.19,.105,.065),(.24,.065,.035),.53),
 ('GreyFrame','TownPaintBlue',(.17,.25,.29),(.15,.20,.19),.48),
 ('Burgundy','TownPanel',(.57,.58,.49),(.23,.018,.028),.90),
 ('DarkPlinth','TownStone',(.38,.355,.31),(.19,.20,.19),.85),
 ('Limestone','Portal19Stone',(.49,.475,.425),(.52,.48,.37),.81),
 ]:
 name='M_Street20_'+key;S20[key]=name
 if name in materials:continue
 mat(name,col,rough,0,texture);tint=[t/b for t,b in zip(col,base)]
 specs[name]['street16_tint']=tint
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;p=nodes.get('Principled BSDF');src=p.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1)
 links.new(src,mix.inputs[1]);links.new(mix.outputs[0],p.inputs['Base Color'])
 if texture=='Portal19Stone':
  specs[name]['uv_scale']=4
  for n in nodes:
   if n.bl_idname=='ShaderNodeVectorMath' and n.operation=='SCALE':n.inputs[3].default_value=4

def s20_start(name,cuts):
 old=bpy.data.objects.get(name);m=Mesh(name,'Kvarnholmen/Reference street facades')
 assert old is not None,name
 base=street20_base[name]
 for indices,material_index,smooth in base['faces']:
  pieces=[[tuple(base['vertices'][i]) for i in indices]]
  for cut in cuts:
   pieces=[pp for p in pieces for pp in (outside_box(p,cut) if all(max(v[k] for v in p)>=cut[k*2] and min(v[k] for v in p)<=cut[k*2+1] for k in range(3)) else [p])]
  for p in pieces:m.faces(p,[tuple(range(len(p)))],base['materials'][material_index],smooth)
 bpy.data.objects.remove(old,do_unlink=True);street20_names.append(name);return m

def s20_finish(m):
 obj=m.finish();obj['detail_pass']=20;obj['massing_only']=False;obj['reference_notes']='references/street20-notes.md'
 return obj

def s20_spans(lo,hi,u,holes,pad=.09):
 spans=[(lo,hi)]
 for c,b,w,h,*_ in holes:
  if abs(u-c)<w/2+pad:
   spans=[(l,r) for aa,bb in spans for l,r in [(aa,min(bb,b-pad)),(max(aa,b+h+pad),bb)] if r-l>.005]
 return spans

def s20_panel(m,x,y,L,H,a,ma,holes,lo=.7):
 n=max(1,round(L/.19))
 for i in range(n+1):
  u=-L/2+i*L/n
  for b,t in s20_spans(lo,H-.12,u,holes):facade_box(m,x,y,u,.372,(b+t)/2,.033,.038,t-b,ma,a)

def s20_window(m,x,y,u,b,w,h,a,frame=TW,trim=TW,cross=.66,small=False):
 # Closed reveal, deep glazing, stepped timber casing; no floating plane window.
 p18_win(m,x,y,u,b,w,h,0,a,frame,trim,1,2)
 facade_box(m,x,y,u,.24,b+h*cross,w,.10,.060 if not small else .033,frame,a)
 if small:facade_box(m,x,y,u,.24,b+h*.33,w,.08,.028,frame,a)
 for side in [-1,1]:
  for z in [b+.23,b+h-.23]:facade_box(m,x,y,u+side*(w/2-.025),.283,z,.035,.045,.13,IRON,a)
 for side in [-1,1]:facade_box(m,x,y,u+side*.055,.285,b+h*.49,.025,.028,.105,METAL,a)
 # Folded metal weather sill, with small raised end returns.
 facade_box(m,x,y,u,.53,b-.037,w+.18,.24,.025,METAL,a)
 for side in [-1,1]:facade_box(m,x,y,u+side*(w/2+.07),.51,b-.007,.024,.21,.055,METAL,a)

def s20_plinth(m,x,y,L,a,holes,H=.7):
 # Clip the base and bottom moulding at actual door openings.
 cuts=sorted((u-w/2-.02,u+w/2+.02) for u,b,w,h,*_ in holes if b<H)
 at=-L/2
 for l,r in cuts+[(L/2,L/2)]:
  if l>at:facade_box(m,x,y,(at+l)/2,.385,H/2,l-at,.11,H,S20['DarkPlinth'],a)
  at=max(at,r)

def s20_eaves(m,x,y,L,H,a,ma=TW,dentils=False):
 for z,d,h in [(H-.19,.48,.13),(H-.07,.58,.09),(H+.025,.67,.10)]:facade_box(m,x,y,0,d/2+.08,z,L,d,h,ma,a)
 if dentils:
  for k in range(round(L/.17)):facade_box(m,x,y,-L/2+(k+.5)*L/round(L/.17),.45,H-.27,.085,.16,.12,ma,a)
 town_rod(m,lp(x,y,-L/2,.62,H+.02,a),lp(x,y,L/2,.62,H+.02,a),.075,METAL,12)
 for u in [-L/2+.14,L/2-.14]:sf_pipe(m,x,y,u,H,a,TW if ma==TW else METAL)

def s20_roof(m,x0,x1,y0,y1,H,rise,axis='x',ma=None,open_north=False):
 ma=ma or TT;cx=(x0+x1)/2;cy=(y0+y1)/2
 if axis=='x':
  faces=[[(x0,y0,H),(x1,y0,H),(x1,cy,H+rise),(x0,cy,H+rise)],[(x0,cy,H+rise),(x1,cy,H+rise),(x1,y1,H),(x0,y1,H)]]
  ends=[[(x,y0,H),(x,y1,H),(x,cy,H+rise)] for x in [x0,x1]];ridge=[(x0,cy,H+rise),(x1,cy,H+rise)]
 else:
  faces=[[(x0,y0,H),(cx,y0,H+rise),(cx,y1,H+rise),(x0,y1,H)],[(cx,y0,H+rise),(x1,y0,H),(x1,y1,H),(cx,y1,H+rise)]]
  ends=[[(x0,y,H),(x1,y,H),(cx,y,H+rise)] for y in [y0,y1]];ridge=[(cx,y0,H+rise),(cx,y1,H+rise)]
 for p in faces:m.faces(p,[(0,1,2,3)],ma)
 for p in (ends[:-1] if open_north else ends):m.faces(p,[(0,1,2)],S20['Pale'])
 town_rod(m,*ridge,.08,ma,12)

def s20_round(m,x,y,u,z,r,a,frame=TW,out=.38):
 n=64;vs=[lp(x,y,u+r*math.cos(k*math.tau/n),out-.015,z+r*math.sin(k*math.tau/n),a) for k in range(n)]
 m.faces(vs,[tuple(range(n))],GLAZE)
 # Continuous ring, rather than capped rods around the circumference.
 verts=[lp(x,y,u+(r+dr)*math.cos(k*math.tau/n),o,z+(r+dr)*math.sin(k*math.tau/n),a) for k in range(n) for dr,o in [(0,out-.025),(0,out+.05),(.065,out+.05),(.065,out-.025)]]
 m.faces(verts,[(k*4+j,k*4+(j+1)%4,((k+1)%n)*4+(j+1)%4,((k+1)%n)*4+j) for k in range(n) for j in range(4)],frame,True)
 facade_box(m,x,y,u,out+.025,z,.04,.06,2*r,frame,a)

def s20_door(m,x,y,u,b,w,h,a,ma=TG):
 facade_box(m,x,y,u,.14,b+h/2,w,.15,h,ma,a)
 for side in [-1,1]:
  facade_box(m,x,y,u+side*(w/2+.055),.39,b+h/2,.16,.20,h+.14,TW,a)
  for z in [b+.5,b+1.2,b+2.0]:
   if z+.27<b+h:town_border(m,*lp(x,y,u+side*w*.24,0,0,a)[:2],z,w*.38,.52,a,ma,.26,.035)
 for q in [0,-w/2,w/2]:facade_box(m,x,y,u+q,.245,b+h/2,.055,.09,h,ma,a)
 facade_box(m,x,y,u,.43,b+h+.065,w+.28,.25,.14,TW,a)
 for s in [-1,1]:town_rod(m,lp(x,y,u+s*.075,.29,b+1.1,a),lp(x,y,u+s*.075,.29,b+1.38,a),.016,METAL)
 facade_box(m,x,y,u,.51,b-.045,w+.35,.8,.10,TS,a)

def s20_awning(m,x,y,u,z,w,a,ma):
 profile=[(.41,z+.10),(.68,z+.06),(1.20,z-.12),(1.52,z-.55),(1.52,z-.75)]
 verts=[lp(x,y,u+s*w/2,o,h,a) for s in [-1,1] for o,h in profile];N=len(profile)
 m.faces(verts,[(i,i+1,N+i+1,N+i) for i in range(N-1)]+[tuple(range(N-1,-1,-1)),tuple(range(N,2*N))],ma)
 for side in [-1,1]:town_rod(m,lp(x,y,u+side*w*.42,.37,z-.64,a),lp(x,y,u+side*w*.42,1.45,z-.51,a),.016,METAL)
 facade_box(m,x,y,u,.42,z+.09,w+.1,.15,.12,METAL,a)

# Kullzenska: three-window timber gable + four-window cafe face, lower courtyard wing.
name='SM_Kvarnholmen_House_91970263'
m=s20_start(name,[(-183,-170.5,51.5,65,-1,40),(-171.1,-151.2,58.6,65,-1,40)])
x0,x1,y0,y1=-180.89,-171.02,52.0,63.75;H=8.05
for x,y,L,a,us,cafe in [((x0+x1)/2,y1,x1-x0,math.pi,[-3.12,0,3.12],False),(x0,(y0+y1)/2,y1-y0,-math.pi/2,[-4.32,-1.55,1.35,4.15],True)]:
 holes=[(u,4.53,1.44,2.43,0) for u in us]
 lows=[(u,1.20,1.44,1.90,0) for u in us] if not cafe else [(u,.94,2.08,2.36,0) for u in [-4.32,-1.55,4.15]]+[(1.35,.36,1.13,3.0,0)]
 holes+=lows;p18_face(m,x,y,L,H,holes,S20['CreamWood'],a);s20_panel(m,x,y,L,H,a,S20['CreamWood'],holes,.8);s20_plinth(m,x,y,L,a,holes,.81)
 for u,b,w,h,_ in holes:
  if cafe and b<1 and w<1.2:s20_door(m,x,y,u,b,w,h,a,S20['RedFrame']);continue
  s20_window(m,x,y,u,b,w,h,a,S20['RedFrame'],S20['CreamWood'],.66,not cafe and b<2)
  if cafe and b<2:s20_awning(m,x,y,u,3.5,w+.15,a,S20['Burgundy'])
 for u in [-L/2+.12,L/2-.12]:facade_box(m,x,y,u,.41,4.4,.27,.19,7.25,S20['CreamWood'],a)
 s20_eaves(m,x,y,L+.07,H,a,S20['CreamWood'],True)
 if cafe:
  for u in [.51,2.14]:town_lantern(m,*lp(x,y,u,.55,0,a)[:2],3.05,a)
# Back party wall and courtyard side close the replaced corner block.
for x,y,L,a in [((x0+x1)/2,y0,x1-x0,0),(x1,(y0+y1)/2,y1-y0,math.pi/2)]:
 hs=[(u,z,1.05,1.5,0) for u in [-2.8,0,2.8] for z in [1.25,4.65]] if a else []
 p18_face(m,x,y,L,H,hs,S20['CreamWood'],a)
 for u,b,w,h,_ in hs:s20_window(m,x,y,u,b,w,h,a,S20['RedFrame'],S20['CreamWood'])
s20_roof(m,x0-.16,x1+.05,y0,y1+.25,H,4.05,'y',open_north=True)
m.box((x0-.18,y1+.18,4.43),(.37,.37,7.25),S20['CreamWood'])
x,y,a=(x0+x1)/2,y1+.02,math.pi;L=x1-x0
# Solid timber gable in front of its roof end, with battens clipped to roof slope.
# Cut the attic aperture through both gable surfaces, rather than projecting it onto timber.
gv=[lp(x,y,u,o,z,a) for o in [.005,.355] for u,z in [(-L/2,H),(L/2,H),(0,H+4.05)]]
for face in [(0,2,1),(3,4,5),(0,1,4,3),(1,2,5,4),(2,0,3,5)]:
 for poly in outside_box([gv[i] for i in face],(x-.53,x+.53,y-.2,y+.6,8.62,10.22)):m.faces(poly,[tuple(range(len(poly)))],S20['CreamWood'])
for u in [-.53,.53]:facade_box(m,x,y,u,.18,9.42,.06,.35,1.60,S20['RedFrame'],a)
for i in range(1,round(L/.19)):
 u=-L/2+i*L/round(L/.19);top=H+4.05*(1-abs(u)/(L/2))
 for b,t in s20_spans(H,top,u,[(0,8.62,1.06,1.60,0)]):facade_box(m,x,y,u,.425,(b+t)/2,.033,.038,t-b,S20['CreamWood'],a)
# The attic backing must be ahead of the gable; reveal depth remains visible.
s20_window(m,x,y,0,8.62,1.06,1.6,a,S20['RedFrame'],S20['CreamWood'],.5,True)
for u,z in [(0,10.78),(-2.52,8.87),(2.52,8.87)]:s20_round(m,x,y,u,z,.25,a,S20['CreamWood'],.48)
for side in [-1,1]:sf_beam(m,lp(x,y,side*L/2,.49,H,a),lp(x,y,0,.49,H+4.07,a),.16,.18,S20['CreamWood'],a)
m.box((-175.7,55.4,11.85),(.75,.85,1.65),P18['BrickRed']);m.box((-175.7,55.4,12.7),(.90,.99,.12),METAL)
# Lower north wing; gate and small-paned red casements, courtyard kept open.
x0w,x1w=-171.02,-151.84;x,y=(x0w+x1w)/2,63.55;L=x1w-x0w;H=6.85;a=math.pi
us=[-7.3,-3.65,0,3.65,7.3];holes=[(u,4.03,1.15,1.85,0) for u in us]+[(u,1.05,1.15,1.75,0) for u in us if u!=0]+[(0,.20,1.85,2.37,.925)]
p18_face(m,x,y,L,H,holes,S20['CreamWood'],a);s20_panel(m,x,y,L,H,a,S20['CreamWood'],[(u,b,w,h+r,0) for u,b,w,h,r in holes]);s20_plinth(m,x,y,L,a,holes)
for u,b,w,h,r in holes:
 if r:
  s20_door(m,x,y,u,b,w,h,a,S20['CreamWood']);p18_arch(m,*lp(x,y,u,0,0,a)[:2],b+h,w,r,.13,.43,a,S20['CreamWood']);continue
 s20_window(m,x,y,u,b,w,h,a,S20['RedFrame'],S20['CreamWood'],.67,True)
s20_eaves(m,x,y,L,H,a,S20['CreamWood']);s20_roof(m,x0w,x1w,59.03,63.8,H,2.3)
p18_face(m,x,59.03,L,H,[],S20['CreamWood'],0)
s20_finish(m)

# Areskogska: small traditional openings, coach gate, pilasters, a broken hipped roof.
name='SM_Building_91846946';H=7.45
m=s20_start(name,[(-296.20,-293.8,41.8,65,-1,40),(-310,-294.5,63.60,65,-1,40),(-311,-294,41,66,7.05,40)])
for x,y,L,a,us,east in [(-295.70,53.285,21.63,math.pi/2,[-9,-6.45,-3.9,-1.35,1.2,3.75,6.3,8.85],True),(-302.63,64.115,13.79,math.pi,[-5.3,-2.65,0,2.65,5.3],False)]:
 holes=[(u,4.33,1.26,2.18,0) for u in us]
 for u in us:
  if east and u==-3.9:holes.append((u,.15,2.12,3.12,0))
  elif east and u==3.75:holes.append((u,.25,1.22,2.93,0))
  else:holes.append((u,1.13,1.25,1.83,0))
 p18_face(m,x,y,L,H,holes,S20['HoneyWood'],a);s20_panel(m,x,y,L,H,a,S20['HoneyWood'],holes,.77);s20_plinth(m,x,y,L,a,holes,.75)
 for u,b,w,h,r in holes:
  if b<.5:s20_door(m,x,y,u,b,w,h,a,TG if w>2 else TW);continue
  s20_window(m,x,y,u,b,w,h,a,TW,TW,.67,b<2)
  if b<2:
   facade_box(m,x,y,u,.42,3.30,w+.3,.12,.47,TW,a)
   p18_band(m,*lp(x,y,u,0,0,a)[:2],w+.5,3.56,a,TW,.24)
 for u in [-L/2+.10,L/2-.10]+([-5.16,2.48] if east else [1.34]):
  facade_box(m,x,y,u,.41,4.08,.30,.20,6.66,TW,a)
  facade_box(m,x,y,u,.45,.87,.42,.28,.28,TW,a)
 s20_eaves(m,x,y,L+.08,H,a,TW)
 if east:
  town_pediment(m,*lp(x,y,3.75,.51,0,a)[:2],3.43,1.73,.39,a,TW)
  s20_awning(m,x,y,-.12,3.57,4.86,a,TG)
m.box((-295.53,64.285,4.10),(.39,.39,6.69),TW)
m.box((-295.52,64.29,7.37),(.53,.53,.30),TW)
# Fill the rear height extension; existing mapped rear openings are preserved below 7.05.
for x,y,L,a in [(-309.57,53.27,21.55,-math.pi/2),(-302.64,42.46,13.9,0)]:facade_box(m,x,y,0,.13,7.25,L,.25,.40,S20['HoneyWood'],a)
# Concentric rectangular hips produce the photographed broken pitch.
cx,cy=-302.66,53.29;ww,dd=14.15,21.9
rings=[[(cx+s*ww/2,cy+t*dd/2,H+.12) for s,t in [(-1,-1),(1,-1),(1,1),(-1,1)]],[(cx+s*(ww/2-2.9),cy+t*(dd/2-2.9),H+3.17) for s,t in [(-1,-1),(1,-1),(1,1),(-1,1)]],[(cx-.07,cy-3.9,H+4.05),(cx+.07,cy-3.9,H+4.05),(cx+.07,cy+3.9,H+4.05),(cx-.07,cy+3.9,H+4.05)]]
for low,high in zip(rings,rings[1:]):
 for i in range(4):j=(i+1)%4;m.faces([low[i],low[j],high[j],high[i]],[(0,1,2,3)],TT)
# Flush roof lights follow the steep lower roof plane, rather than unsupported dormers.
for x,y,L,a,us in [(-295.585,53.29,21.9,math.pi/2,[-7.2,-2.5,2.5,7.2]),(-302.66,64.24,14.15,math.pi,[-4.4,0,4.4])]:
 for u in us:
  verts=[lp(x,y,u+du,-v,H+.14+v*3.05/2.9,a) for du,v in [(-.62,.56),(.62,.56),(.62,2.09),(-.62,2.09)]]
  m.faces(verts,[(0,1,2,3)],GLAZE)
  for p,q in zip(verts,verts[1:]+verts[:1]):town_rod(m,p,q,.042,METAL)
  # Roof seal and flashing at the uphill end.
  town_rod(m,verts[2],verts[3],.068,METAL)
for yy in [47.4,58.9]:m.box((cx,yy,H+4.2),(.64,.72,1.10),METAL)
s20_finish(m)

# South Storgatan: three separate street blocks, original rear wings retained.
for bid,x0,x1,y,kind,H in [('92379254',-92.72,-81.34,-8.66,'ochre',7.30),('92379269',-104.48,-92.84,-8.59,'awning',7.65),('92379288',-116.77,-104.61,-8.52,'pale',7.90)]:
 name='SM_Building_'+bid;back=-17.10;m=s20_start(name,[(x0-.18,x1+.18,back,y+2,-1,45)])
 x=(x0+x1)/2;L=x1-x0;a=math.pi;wall=S20['Ochre'] if kind=='ochre' else S20['Pale'];frame=TW if kind=='ochre' else S20['RedFrame'];n=4 if kind=='ochre' else 5
 us=[-L/2+(i+.5)*L/n for i in range(n)];holes=[(u,4.32,1.27 if n==4 else 1.10,1.95,0) for u in us]
 shops=[(-L*.31,.36,2.70,2.60,0),(0,.24,1.28,2.77,0),(L*.31,.36,2.70,2.60,0)]
 holes+=shops;p18_face(m,x,y,L,H,holes,wall,a);s20_plinth(m,x,y,L,a,holes,.40)
 for u,b,w,h,r in holes:
  if b>4:s20_window(m,x,y,u,b,w,h,a,frame,TW,.61);continue
  if w<1.5:s20_door(m,x,y,u,b,w,h,a,BROWN);continue
  s20_window(m,x,y,u,b,w,h,a,frame,TW,.82)
  if kind=='awning':s20_awning(m,x,y,u,3.19,w+.22,a,TG)
 # Individual entrance lintels and restrained plaster bands.
 p18_band(m,x,y,L,3.83,a,TW,.25);s20_eaves(m,x,y,L,H,a,TW)
 for xx in [x0,x1]:facade_box(m,xx,(y+back)/2,0,0,H/2,.14,y-back,H,wall,0)
 s20_roof(m,x0,x1,back,y+.34,H,2.80)
 # A solid pediment on #24, not an empty triangular frame.
 if kind=='awning':
  town_pediment(m,*lp(x,y,0,.43,0,a)[:2],H-.06,3.25,1.62,a,wall);s20_round(m,x,y,0,H+.58,.33,a,TW,.57)
 # Metal hood dormers are integrated into the sloped roof and have closed cheeks.
 for u in ([-3.42,0,3.42] if kind=='ochre' else [-3.85,3.85]):
  xx,yy,_=lp(x,y,u,-1.18,0,a);z=H+.83;w=1.25;h=1.12
  facade_box(m,xx,yy,0,-.31,z+.40,w+.20,.9,1.65,wall,a)
  # Place the window ahead of dormer backing; hood projects and seals the head.
  wx,wy,_=lp(xx,yy,0,.34,0,a);s20_window(m,wx,wy,0,z-.1,w,h,a,frame,TW,.55)
  outline=[(-w/2-.17,0)]+[(.80*math.cos(math.pi-k*math.pi/32),.45*math.sin(k*math.pi/32)) for k in range(33)]+[(w/2+.17,0)]
  town_polyprofile(m,*lp(xx,yy,0,.60,0,a)[:2],z+h+.10,outline,a,town_mats['MetalRed'],1.25,False)
 s20_finish(m)

def s20_metal_window(m,x,y,u,b,w,h,a,cross=0):
 facade_box(m,x,y,u,.14,b+h/2,w,.045,h,GLAZE,a)
 for off in [-w/2,0,w/2]:facade_box(m,x,y,u+off,.265,b+h/2,.052,.24,h,S20['GreyFrame'],a)
 for z in [b,b+h]+([b+h*cross] if cross else []):facade_box(m,x,y,u,.265,z,w,.24,.052,S20['GreyFrame'],a)
 # Thin folded perimeter and flashing, no classical timber casing or applied hinges.
 for off in [-w/2-.025,w/2+.025]:facade_box(m,x,y,u+off,.367,b+h/2,.075,.045,h+.09,S20['GreyFrame'],a)
 facade_box(m,x,y,u,.40,b-.033,w+.12,.18,.027,METAL,a)

# Kappahl frontage: two orange bays, projecting glass oriels and circular upper lights.
name='SM_Building_91970290';x0,x1,y,back=-92.25,-68.52,2.64,11.1;L=x1-x0;x=(x0+x1)/2;H=11.35;a=0
m=s20_start(name,[(x0-.20,x1+.20,y-2.2,back,-1,40)])
holes=[]
for centre in [-L/4,L/4]:
 for du in [-4.08,4.08]:
  holes.extend([(centre+du,4.35,1.15,2.55,0),(centre+du,7.82,1.15,2.55,0)])
 for du in [-2.22,2.22]:holes.append((centre+du,7.99,1.27,1.89,0))
 holes.append((centre,4.3,2.33,2.52,0))
 for du in [-3.88,0,3.88]:holes.append((centre+du,.28,3.27,2.82,0))
p18_face(m,x,y,L,H,holes,S20['Orange'],a)
# Stone cladding has real narrow panel joints, cut around ground-floor glazing.
for z0,z1 in [(.08,.75),(.77,1.43),(1.45,2.13),(2.15,2.82),(2.84,3.5),(3.52,4.05)]:
 for k in range(round(L/1.27)):
  u=-L/2+(k+.5)*L/round(L/1.27);w=L/round(L/1.27)-.018
  # Clip at shop openings instead of covering them with a second facade skin.
  spans=[(u-w/2,u+w/2)]
  for c,b,hw,hh,r in holes:
   if b<(z0+z1)/2<b+hh:spans=[(l,rr) for lo,hi in spans for l,rr in [(lo,min(hi,c-hw/2)),(max(lo,c+hw/2),hi)] if rr-l>.02]
  for lo,hi in spans:facade_box(m,x,y,(lo+hi)/2,.39,(z0+z1)/2,hi-lo,.10,z1-z0,S20['Limestone'],a)
for u,b,w,h,r in holes:
 if b>4 and w>2:continue
 s20_metal_window(m,x,y,u,b,w,h,a,.87 if b<1 else (.18 if h>2.4 else 0))
 if b<1 and abs(abs(u)-L/4)<.1:
  for v in [-.11,.11]:town_rod(m,lp(x,y,u+v,.39,1.1,a),lp(x,y,u+v,.39,1.64,a),.018,METAL)
for centre in [-L/4,L/4]:
 # Box oriel, with visible glazed side returns and supported metal apron.
 facade_box(m,x,y,centre,.94,4.27,2.56,1.5,.22,S20['GreyFrame'],a)
 facade_box(m,x,y,centre,.94,6.97,2.67,1.58,.14,S20['GreyFrame'],a)
 for edge in [-1,1]:
  xx,yy,_=lp(x,y,centre+edge*1.22,.82,0,a)
  facade_box(m,x,y,centre+edge*1.22,.84,5.63,.065,1.22,2.48,S20['GreyFrame'],a)
  m.faces([lp(x,y,centre+edge*1.23,o,z,a) for o,z in [(.40,4.43),(1.57,4.43),(1.57,6.86),(.40,6.86)]],[(0,1,2,3)],GLAZE)
 xx,yy,_=lp(x,y,centre,1.32,0,a);s20_metal_window(m,xx,yy,0,4.44,2.33,2.38,a,.12)
 s20_round(m,x,y,centre,9.26,.62,a,S20['GreyFrame'],.42)
# Full-height pale piers divide the two photographic bays.
for u in [-L/2+.10,0,L/2-.10]:facade_box(m,x,y,u,.41,H/2,.23,.17,H,S20['Limestone'],a)
facade_box(m,x,y,0,.38,H,L,.62,.17,S20['Limestone'],a)
facade_box(m,x,y,0,.65,H+.07,L,.11,.10,METAL,a)
for xx in [x0,x1]:facade_box(m,xx,(y+back)/2,0,0,H/2,.15,back-y,H,S20['Orange'],0)
s20_roof(m,x0,x1,y-.34,back,H,1.25,ma=METAL)
s20_finish(m)

street20_cameras=[
 ('91_Storgatan_South20',(-76.0,-1.7,2.2),(-100,-8.6,4.8),23),
 ('92_Storgatan_Orange20',(-79,-6.1,2.3),(-80.3,2.64,6.0),12),
 ('93_Kullzenska20',(-192,74.5,2.2),(-174.0,59.8,5.9),24),
 ('94_Areskogska20',(-285.7,72.6,2.2),(-298.5,59.5,4.8),23),
 ('95_Norra_Langgatan20',(-191,68.1,1.8),(-158,64,3.5),29),
 ('96_Larmgatan20',(-290.6,39,1.85),(-295.6,57,4.3),23),
 ('97_Kaggensgatan20',(-185.1,46,1.85),(-180.9,60,4.2),23),
]
