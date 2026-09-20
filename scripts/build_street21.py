"""Reference-specific northern street row, from the April 2025 / June 2020 panoramas.
Original geometry and PBR maps. See references/street21-notes.md for uncertainty.
"""
import ast
# Reuse the authored joinery without rebuilding the six completed pass-20 houses.
code=(R/'scripts/build_street20.py').read_text();exec(compile(code[:code.index('# Kullzenska:')],'street20_joinery','exec'))
tree=ast.parse(code);tree.body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='s20_metal_window'];exec(compile(tree,'metal_joinery','exec'))
exec(compile((R/'scripts/bathhouse19_helpers.py').read_text(),'curved_reveals','exec'))
D21=json.loads((R/'source/district17.json').read_text())['buildings'];BASE21=json.loads((R/'source/street21-base.json').read_text())['meshes'];street21_names=[];S21={}
for key,texture,base,col,rough,metal in [
 ('WarmCream','TownIvory',(.68,.65,.55),(.72,.66,.47),.83,0),
 ('Rose','TownRose',(.49,.32,.25),(.64,.34,.22),.85,0),
 ('White','TownIvory',(.68,.65,.55),(.77,.76,.69),.80,0),
 ('Concrete','TownStone',(.38,.355,.31),(.52,.51,.44),.85,0),
 ('PanelRed','TownPanel',(.57,.58,.49),(.48,.13,.10),.74,0),
 ('PanelBlue','TownPanel',(.57,.58,.49),(.29,.45,.53),.74,0),
 ('PanelGreen','TownPanel',(.57,.58,.49),(.48,.58,.43),.74,0),
 ('PanelGrey','TownPanel',(.57,.58,.49),(.56,.58,.53),.72,0),
 ('DeepGreen','TownPaintGreen',(.08,.135,.10),(.095,.15,.10),.50,0),
 ('BlueAwning','TownPanel',(.57,.58,.49),(.035,.060,.15),.92,0),
 ('MetalGreen','TownMetalGrey',(.115,.15,.132),(.20,.29,.25),.55,.35),
 ('TileApron','Street21Tile',(.46,.475,.49),(.46,.475,.49),.34,.04),
 ]:
 name='M_Street21_'+key;S21[key]=name
 if name in materials:continue
 mat(name,col,rough,metal,texture);tint=[t/b for t,b in zip(col,base)];specs[name]['street16_tint']=tint
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])

def s21_new(name,cuts=None):
 old=bpy.data.objects.get(name);assert old is not None,name
 m=Mesh(name,'Kvarnholmen/Northern street facades')
 if cuts:
  b=BASE21[name]
  for indices,mi,smooth in b['faces']:
   pieces=[[tuple(b['vertices'][i]) for i in indices]]
   for cut in cuts:
    pieces=[pp for p in pieces for pp in (outside_box(p,cut) if all(max(v[k] for v in p)>=cut[k*2] and min(v[k] for v in p)<=cut[k*2+1] for k in range(3)) else [p])]
   for p in pieces:m.faces(p,[tuple(range(len(p)))],b['materials'][mi],smooth)
 bpy.data.objects.remove(old,do_unlink=True);street21_names.append(name);return m

def s21_finish(m):
 obj=m.finish();obj['detail_pass']=21;obj['massing_only']=False;obj['reference_notes']='references/street21-notes.md'
 # A small real edge catches light on plaster, frames and panel ribs.
 bevel=obj.modifiers.new('Crafted edge highlights','BEVEL');bevel.width=.003;bevel.segments=1;bevel.limit_method='ANGLE';bevel.angle_limit=.65;bevel.use_clamp_overlap=True
 bpy.context.view_layer.objects.active=obj;obj.select_set(True);bpy.ops.object.modifier_apply(modifier=bevel.name)
 # Bevel UV interpolation can vary by a few float bits across runs. Derive the
 # authored world-scale UVs from the final positions in a fixed iteration order.
 me=obj.data;uv=me.uv_layers.active.data
 for poly in me.polygons:
  coords=[me.vertices[i].co for i in poly.vertices];normal=Vector((0,0,0))
  for c,d in zip(coords,coords[1:]+coords[:1]):normal+=c.cross(d)
  axis=max(range(3),key=lambda k:abs(normal[k]));axes=[k for k in range(3) if k!=axis]
  for li in poly.loop_indices:
   c=me.vertices[me.loops[li].vertex_index].co;uv[li].uv=(c[axes[0]]/4,c[axes[1]]/4)
 return obj

def s21_edge(w):return sf_edge(w['p'],w['q'])
def s21_roof_reuse(m,name,H,scale=1):
 b=BASE21[name];oldH=D21[name]['H']
 for indices,mi,smooth in b['faces']:
  v=[b['vertices'][i] for i in indices]
  if min(p[2] for p in v)<oldH-.035:continue
  m.faces([(x,y,H+(z-oldH)*scale) for x,y,z in v],[tuple(range(len(v)))],b['materials'][mi],smooth)

def s21_rear(m,w,H,ma,levels=2):
 x,y,L,a=s21_edge(w)
 if not w['exposed'] or L<2:
  facade_box(m,x,y,0,.14,H/2,L,.28,H,ma,a);return
 n=max(1,round(L/3.4));us=[-L/2+(k+.5)*L/n for k in range(n)]
 hs=[(u,.95+j*(H-.4)/levels,min(1.15,L/n*.55),1.70,0) for u in us for j in range(levels)]
 p18_face(m,x,y,L,H,hs,ma,a)
 for u,b,ww,h,r in hs:s20_window(m,x,y,u,b,ww,h,a,TW,TW)
 s20_plinth(m,x,y,L,a,hs,.50)

def s21_glass(m,x,y,u,b,w,h,a,frame=TW,cols=2,trans=.8,door=False):
 # Thin joinery with sealed deep reveals, separate from classical casing.
 facade_box(m,x,y,u,.12,b+h/2,w,.045,h,GLAZE,a)
 for off in [-w/2,w/2]:facade_box(m,x,y,u+off,.265,b+h/2,.060,.27,h,frame,a)
 for k in range(1,cols):facade_box(m,x,y,u-w/2+w*k/cols,.29,b+h/2,.042,.09,h,frame,a)
 for z in [b,b+h]+([b+h*trans] if trans else []):facade_box(m,x,y,u,.28,z,w,.23,.052,frame,a)
 facade_box(m,x,y,u,.40,b-.035,w+.12,.19,.026,METAL,a)
 if door:
  for du in [-.12,.12]:town_rod(m,lp(x,y,u+du,.39,b+1.05,a),lp(x,y,u+du,.39,b+1.48,a),.017,METAL)

def s21_flat_roof(m,points,H,ma=METAL):
 m.faces([(x,y,H+.07) for x,y in points],[tuple(range(len(points)))],ma)
 for p,q in zip(points,points[1:]+points[:1]):
  x,y,L,a=sf_edge(p,q);facade_box(m,x,y,0,.07,H+.08,L,.28,.20,ma,a)

def s21_dormer(m,x,y,u,b,w,h,a,ma):
 # Box dormer: actual open front, closed side returns, sloping cover into the main roof.
 xx,yy,_=lp(x,y,u,-1.0,0,a)
 for side in [-1,1]:facade_box(m,xx,yy,side*(w/2+.055),-.43,b+h/2,.13,1.20,h+.16,ma,a)
 facade_box(m,xx,yy,0,-.95,b+h/2,w,.13,h,ma,a)
 facade_box(m,xx,yy,0,-.39,b+h+.08,w+.26,1.35,.12,ma,a)
 facade_box(m,xx,yy,0,.19,b-.05,w+.28,.33,.13,ma,a)
 s21_glass(m,xx,yy,0,b,w,h,a,ma,max(2,round(w/.6)),0)

def s21_oriel(m,x,y,u,b,w,h,a,cream=TW,roof=None):
 roof=roof or S21['MetalGreen'];front=.93
 # A shallow trapezoid bay with glazed side returns and a panelled apron.
 outline=[(-w*.60,.34),(-w*.50,front),(w*.50,front),(w*.60,.34)]
 p=[lp(x,y,u+uu,o,0,a)[:2] for uu,o in outline]
 m.prism(p,b-.52,b,cream);m.prism(p,b+h,b+h+.16,cream)
 for k in range(1,5):facade_box(m,x,y,u,front+.035,b-.51+k*.095,w,.04,.022,cream,a)
 for i in range(3):
  p0,p1=p[i],p[i+1];xx,yy,L,aa=sf_edge(p0,p1)
  # Mapped edge direction already points the joinery outside the bay.
  xx,yy,_=lp(xx,yy,0,-.12,0,aa)
  s21_glass(m,xx,yy,0,b+.08,L-.10,h-.15,aa,cream,2 if i==1 else 1,.67)
 for sign in [-1,1]:facade_box(m,x,y,u+sign*(w/2+.075),front+.12,b+h/2,.13,.20,h+.14,cream,a)
 for dz,depth,hh in [(h+.19,1.21,.08),(h+.27,1.30,.07)]:facade_box(m,x,y,u,.59,b+dz,w+.35,depth,hh,cream,a)
 # Small shaped crest, restrained to the photographed bay silhouette.
 town_polyprofile(m,*lp(x,y,u,1.22,0,a)[:2],b+h+.32,[(-w*.52,0),(-w*.31,.05),(0,.32),(w*.31,.05),(w*.52,0)],a,cream,.16,False)
 m.faces([lp(x,y,u+uu,o,b+h+.40+(.20 if o<.5 else 0),a) for uu,o in outline],[(0,1,2,3)],roof)

def s21_shallow_awning(m,x,y,u,z,w,a,ma,depth=1.0):
 # Taut fabric canopy with a fixed wall cassette, front bar and two support arms.
 vs=[lp(x,y,u+du,o,h,a) for du,o,h in [(-w/2,.4,z),(w/2,.4,z),(w/2,depth,z-.46),(-w/2,depth,z-.46)]]
 m.faces(vs,[(0,1,2,3)],ma)
 facade_box(m,x,y,u,.42,z+.025,w+.08,.14,.12,METAL,a)
 facade_box(m,x,y,u,depth,z-.52,w,.035,.13,ma,a)
 for du in [-w*.43,w*.43]:town_rod(m,lp(x,y,u+du,.37,z-.64,a),lp(x,y,u+du,depth-.04,z-.43,a),.013,METAL)

# South-west Kaggensgatan corner: the long cream TWO-storey house, not three floors.
name='SM_Kvarnholmen_House_92204207';m=s21_new(name);H=7.35
for w in D21[name]['walls']:
 x,y,L,a=s21_edge(w);north=y>63;east=x>-192.2 and L>15
 if not (north or east):s21_rear(m,w,H,S21['WarmCream'],2);continue
 n=10 if north else 7;us=[-L/2+(k+.5)*L/n for k in range(n)];hs=[(u,4.23,1.23,2.04,0) for u in us]
 gate=6.55 if north else None
 if north:ground=[(-11.35,.55,2.8,2.68,0),(-7.75,.55,3.0,2.68,0),(-4.05,.55,3.1,2.68,0),(-.35,.55,3.1,2.68,0),(3.0,.55,2.2,2.68,0),(6.55,.20,2.05,3.04,0),(10.55,.55,2.35,2.68,0),(12.8,.25,1.17,2.98,0)]
 else:ground=[(u,.45,2.24,2.78,0) for u in us]
 hs+=ground;p18_face(m,x,y,L,H,hs,S21['WarmCream'],a);s20_plinth(m,x,y,L,a,hs,.50)
 for u,b,ww,hh,r in hs:
  if b>4:s20_window(m,x,y,u,b,ww,hh,a,S21['DeepGreen'],S21['WarmCream'],.72);continue
  if north and abs(u-6.55)<.1:s20_door(m,x,y,u,b,ww,hh,a,S21['DeepGreen']);continue
  s21_glass(m,x,y,u,b,ww,hh,a,S21['DeepGreen'],2,.84,ww<1.5)
 p18_band(m,x,y,L,3.70,a,TW,.30);s20_eaves(m,x,y,L,H,a,TW,True)
 if north:
  for u in [-9.5,-3.9,1.7,8.8]:s21_dormer(m,x,y,u,H+.5,2.6,1.15,a,town_mats['MetalRed'])
  s21_shallow_awning(m,x,y,-4.8,3.48,15.5,a,IRON,1.28)
 else:
  for u in [-7.8,-1.2,5.4]:s21_dormer(m,x,y,u,H+.5,2.35,1.15,a,town_mats['MetalRed'])
s21_roof_reuse(m,name,H,.65);s21_finish(m)

# North-east Kaggensgatan corner: rose plaster, white projecting bays and chamfered entry.
name='SM_Kvarnholmen_House_92204178';m=s21_new(name);H=8.1;walls=D21[name]['walls']
corner=(-179.977,75.788);ch=1.6
for w in walls:
 p,q=list(w['p']),list(w['q']);west=p[0]<-179 and q[0]<-179;south=p[1]<76 and q[1]<76
 if west:q=[q[0]+.017,q[1]+ch]
 if south:p=[p[0]+ch,p[1]-.045]
 ww=dict(w,p=p,q=q);x,y,L,a=s21_edge(ww)
 if not(west or south):s21_rear(m,ww,H,S21['Rose'],2);continue
 n=4 if west else 8;us=[-L/2+(k+.5)*L/n for k in range(n)];oriels={1} if west else {2,6}
 hs=[(u,4.55,1.25,2.28,0) for k,u in enumerate(us) if k not in oriels]
 hs += [(u,4.55,1.70,2.28,0) for k,u in enumerate(us) if k in oriels]
 hs += [(u,.78,1.9,2.52,.18) for u in us]
 p18_face(m,x,y,L,H,hs,S21['Rose'],a);s20_plinth(m,x,y,L,a,hs,.76)
 for k,u in enumerate(us):
  if k in oriels:s21_oriel(m,x,y,u,4.48,1.80,2.28,a)
  else:s20_window(m,x,y,u,4.55,1.25,2.28,a,TW,TW,.68)
  b19_win(m,x,y,u,.78,1.9,2.52,.18,a,BROWN,S21['Rose'],1,2)
  s20_awning(m,x,y,u,3.50,2.05,a,S20['CreamWood'])
 p18_band(m,x,y,L,4.02,a,TW,.29);s20_eaves(m,x,y,L,H,a,TW,True)
# Recessed diagonal corner door with a bay over its landing.
p=(-179.960,77.388);q=(-178.377,75.743);x,y,L,a=sf_edge(p,q)
hs=[(0,.49,1.20,2.95,.22),(0,4.55,1.46,2.28,0)]
p18_face(m,x,y,L,H,hs,S21['Rose'],a);b19_win(m,x,y,0,.49,1.20,2.95,.22,a,BROWN,TW,1,2)
for k in range(3):facade_box(m,x,y,0,.55+k*.26,(3-k)*.075,1.64,.82,(3-k)*.15,TS,a)
s21_oriel(m,x,y,0,4.48,1.55,2.28,a)
for u in [-L/2+.10,L/2-.10]:facade_box(m,x,y,u,.41,2.24,.20,.19,4.45,TW,a)
s20_eaves(m,x,y,L,H,a,TW);s21_roof_reuse(m,name,H,.60);s21_finish(m)

# Low modular shopping block: coloured infill, stone piers and two connector bays.
name='SM_Kvarnholmen_House_92204173';m=s21_new(name,[(-256,-190,73.2,88.1,-1,40),(-204.0,-189.4,74,94.1,-1,40),(-241.10,-237.92,87.7,89.0,-1,3.30)])
H=7.30
# Slightly rotated frontage follows its mapped street edge.
p=(-255.303,75.820);q=(-191.504,75.198);x,y,L,a=sf_edge(p,q)
segments=[(-L/2,-L/2+14,'PanelBlue',5),(-L/2+14,-L/2+17.5,'connector',1),(-L/2+17.5,-L/2+32.5,'PanelGreen',5),(-L/2+32.5,-L/2+36,'connector',1),(-L/2+36,L/2,'PanelRed',9)]
for lo,hi,key,n in segments:
 xx,yy,_=lp(x,y,(lo+hi)/2,0,0,a);ll=hi-lo
 if key=='connector':
  # The western connector is the open Kopmantorget passage through the street wing.
  passage=lo<0
  holes=[(0,.12,ll-.45,3.14,0)] if passage else [(0,.25,ll-.45,3.0,0)]
  holes += [(0,4.28,ll-.40,2.0,0)]
  p18_face(m,xx,yy,ll,H-.33,holes,S21['PanelGrey'],a)
  s21_glass(m,xx,yy,0,4.28,ll-.40,2.0,a,TW,3,0)
  if not passage:s21_glass(m,xx,yy,0,.25,ll-.45,3,a,S20['GreyFrame'],2,.88,True)
  else:
   for side in [-1,1]:facade_box(m,xx,yy,side*(ll/2-.14),-5.95,1.65,.28,12.2,3.3,S21['Concrete'],a)
   facade_box(m,xx,yy,0,-5.9,3.34,ll,12.5,.15,S21['Concrete'],a)
   facade_box(m,xx,yy,0,-5.9,.06,ll-.25,12.5,.12,TS,a)
   town_text(m,*lp(xx,yy,0,.45,0,a)[:2],3.65,a,'KÖPMANTORGET',ll-.35,BROWN)
  facade_box(m,xx,yy,0,.39,6.63,ll,.10,.72,S21['PanelGrey'],a)
  for z in [6.35,6.49,6.63,6.77,6.91]:facade_box(m,xx,yy,0,.45,z,ll,.022,.022,TW,a)
  continue
 step=ll/n
 for k in range(n):
  u=-ll/2+(k+.5)*step;blank=key=='PanelRed' and k in [0,4,5];large=key=='PanelRed' and k>=7
  ww=step-.34 if large else 1.43;bh=2.45 if large else 1.45;bb=4.38 if large else 4.78
  hs=[(u,.46,step-.34,2.60,0)]+([] if blank else [(u,bb,ww,bh,0)])
  bx,by,_=lp(xx,yy,u,0,0,a)
  local=[(c-u,b,w,h,r) for c,b,w,h,r in hs]
  p18_face(m,bx,by,step,H,local,S21[key],a)
  s20_panel(m,bx,by,step-.14,H-.37,a,S21[key],local,4.06)
  s21_glass(m,bx,by,0,.46,step-.34,2.60,a,S20['GreyFrame'],1,.88,k in [0,n-1])
  if not blank:s21_glass(m,bx,by,0,bb,ww,bh,a,S20['GreyFrame'],2,0)
  for side in [-1,1]:facade_box(m,bx,by,side*(step/2-.05),.405,H/2,.18,.18,H,S21['Concrete'],a)
  facade_box(m,bx,by,0,.40,.24,step,.15,.48,S21['Concrete'],a)
  facade_box(m,bx,by,0,.40,3.75,step,.15,.62,S21['Concrete'],a)
  if key!='PanelBlue':s21_shallow_awning(m,bx,by,0,3.40,step-.12,a,TG if key=='PanelGreen' else S20['Burgundy'],1.27)
 # Broad roof fascia and separately modelled projecting rafter tails.
 facade_box(m,xx,yy,0,.41,H-.04,ll,.58,.23,S21['Concrete'],a)
 for k in range(max(1,round(ll/1.1))):facade_box(m,xx,yy,-ll/2+(k+.5)*ll/round(ll/1.1),.70,H+.06,.09,.81,.20,TW,a)
# Shallow tiled street roof, split at connector strips. Back edge terminates at courtyard wall.
for lo,hi,key,n in segments:
 xx,yy,_=lp(x,y,(lo+hi)/2,0,0,a);ll=hi-lo
 if key=='connector':
  facade_box(m,xx,yy,0,-5.7,H-.24,ll,12.2,.15,METAL,a);continue
 vs=[lp(xx,yy,u,o,z,a) for u,o,z in [(-ll/2,.42,H+.17),(ll/2,.42,H+.17),(ll/2,-5.8,H+1.72),(-ll/2,-5.8,H+1.72),(-ll/2,-12.2,H+.17),(ll/2,-12.2,H+.17)]]
 m.faces(vs,[(0,1,2,3),(3,2,5,4)],TT)
# Close the street-wing rear face except the true western passage.
for lo,hi,key,n in segments:
 if key=='connector' and lo<0:continue
 xx,yy,_=lp(x,y,(lo+hi)/2,-12.2,0,a);p18_face(m,xx,yy,hi-lo,H,[],S21['Concrete'],a+math.pi)
# Kaggensgatan return: two fully glazed corner bays followed by red infill windows.
x,y,L,a=-191.415,84.5,18.55,math.pi/2
for k in range(6):
 u=-L/2+(k+.5)*L/6;xx,yy,_=lp(x,y,u,0,0,a);ww=L/6;large=k<2
 hs=[(0,.46,ww-.34,2.60,0),(0,4.38 if large else 4.78,ww-.34 if large else 1.43,2.45 if large else 1.45,0)]
 p18_face(m,xx,yy,ww,H,hs,S21['PanelRed'],a);s20_panel(m,xx,yy,ww-.15,H-.3,a,S21['PanelRed'],hs,4.05)
 for u,b,w,h,r in hs:s21_glass(m,xx,yy,u,b,w,h,a,S20['GreyFrame'],2 if b>4 else 1,0 if b>4 else .88)
 for sign in [-1,1]:facade_box(m,xx,yy,sign*(ww/2-.05),.405,H/2,.18,.18,H,S21['Concrete'],a)
 for z,h in [(.24,.48),(3.75,.62),(H-.04,.23)]:facade_box(m,xx,yy,0,.42,z,ww,.30,h,S21['Concrete'],a)
# Corner closes the meeting of both structural frames.
m.box((-191.32,75.04,H/2),(.39,.40,H),S21['Concrete'])
s20_roof(m,-204.0,-191.12,87.7,94.1,H+.10,1.6,'y')
s21_finish(m)

# Modern white corner: broad unsprossed windows, stone shop piers and roof terrace.
name='SM_Kvarnholmen_House_92204200';m=s21_new(name);H=10.55
for w in D21[name]['walls']:
 x,y,L,a=s21_edge(w);south=y<77;west=x<-284
 if not(south or west):s21_rear(m,w,H,S21['White'],3);continue
 n=7 if south else 5;step=L/n;us=[-L/2+(k+.5)*step for k in range(n)]
 hs=[(u,b,step*.68,1.82,0) for u in us for b in [4.23,7.38]]+[(u,.3,step-.55,2.95,0) for u in us]
 p18_face(m,x,y,L,H,hs,S21['White'],a)
 for u,b,ww,hh,r in hs:s21_glass(m,x,y,u,b,ww,hh,a,BROWN,2 if b>4 else 1,0,b<1 and abs(u)<step)
 # Ground-floor stone slabs have recessed joints and wrap the corner.
 for k in range(n+1):
  u=-L/2+k*step
  for j in range(5):facade_box(m,x,y,u,.395,.40+j*.62,.46,.10,.60,S21['Concrete'],a)
 facade_box(m,x,y,0,.395,3.56,L,.12,.55,S21['Concrete'],a)
 facade_box(m,x,y,0,.43,H-.12,L,.27,.25,S21['White'],a)
 sf_pipe(m,x,y,L/2-.18,H,a,METAL)
 if west:
  for k in [1,3]:
   u=us[k];ww=step*.68
   for b in [4.23,7.38]:
    facade_box(m,x,y,u,.76,b-.17,ww+.40,1.08,.28,S21['White'],a)
    facade_box(m,x,y,u,.76,b+1.96,ww+.40,1.08,.26,S21['White'],a)
    for sign in [-1,1]:facade_box(m,x,y,u+sign*(ww/2+.10),.78,b+.91,.20,1.10,1.82,S21['White'],a)
    xx,yy,_=lp(x,y,u,1.0,0,a);s21_glass(m,xx,yy,0,b,ww,1.82,a,BROWN,2,0)
points=[w['p'] for w in D21[name]['walls']];s21_flat_roof(m,points,H)
for w in D21[name]['walls']:
 x,y,L,a=s21_edge(w)
 for z in [H+.20,H+1.03]:facade_box(m,x,y,0,-.28,z,L,.045,.045,IRON,a)
 for k in range(round(L/.15)+1):facade_box(m,x,y,-L/2+k*L/round(L/.15),-.28,H+.60,.018,.018,.83,IRON,a)
s21_finish(m)

# Classical three-storey corner opposite Areskogska, with a rusticated shop base.
name='SM_Kvarnholmen_House_92204190';m=s21_new(name);H=11.15
for w in D21[name]['walls']:
 x,y,L,a=s21_edge(w);north=y>64.3;west=x<-284.5 and L>15
 if not(north or west):s21_rear(m,w,H,S21['White'],3);continue
 n=3 if north else 6;step=L/n;us=[-L/2+(k+.5)*step for k in range(n)]
 hs=[(u,b,1.40,hh,0) for u in us for b,hh in [(4.56,2.10),(7.87,1.94)]]+[(u,.80,2.06,2.75,0) for u in us]
 p18_face(m,x,y,L,H,hs,S21['White'],a);s20_plinth(m,x,y,L,a,hs,.80)
 for u,b,ww,hh,r in hs:
  if b>4:s20_window(m,x,y,u,b,ww,hh,a,BROWN,S21['White'],.68)
  else:s21_glass(m,x,y,u,b,ww,hh,a,BROWN,2,.82)
 # Real shallow horizontal joints clipped at shop openings.
 for j in range(9):
  z=.92+j*.34;spans=[(-L/2,L/2)]
  for c,b,ww,hh,r in hs:
   if b<z<b+hh:spans=[(l,r) for lo,hi in spans for l,r in [(lo,min(hi,c-ww/2)),(max(lo,c+ww/2),hi)] if r-l>.01]
  for lo,hi in spans:facade_box(m,x,y,(lo+hi)/2,.366,z,hi-lo,.026,.025,S21['Concrete'],a)
 for z in [4.02,7.23]:p18_band(m,x,y,L,z,a,TW,.25)
 s20_eaves(m,x,y,L,H,a,TW,True)
 if north:
  for u in us:s21_shallow_awning(m,x,y,u,3.83,2.30,a,S21['BlueAwning'],1.27)
 else:s21_shallow_awning(m,x,y,0,3.83,L-.6,a,S21['BlueAwning'],1.27)
s21_roof_reuse(m,name,H,.65);s21_finish(m)

# Cream modern strip with grey ceramic window aprons and four narrow casements.
name='SM_Kvarnholmen_House_92204168';m=s21_new(name);H=10.45
for w in D21[name]['walls']:
 x,y,L,a=s21_edge(w)
 if y<64:s21_rear(m,w,H,S21['WarmCream'],3);continue
 n=6;step=L/n;us=[-L/2+(k+.5)*step for k in range(n)]
 hs=[(u,b,3.03,1.64,0) for u in us for b in [4.84,8.01]]+[(u,.4,step-.48,2.82,0) for u in us]
 p18_face(m,x,y,L,H,hs,S21['WarmCream'],a);s20_plinth(m,x,y,L,a,hs,.38)
 for u,b,ww,hh,r in hs:
  s21_glass(m,x,y,u,b,ww,hh,a,TW if b>4 else S20['GreyFrame'],4 if b>4 else 2,0,b<1 and abs(u)<step)
  if b>4:
   facade_box(m,x,y,u,.39,b-.42,ww,.075,.77,S21['TileApron'],a)
   for side in [-1,1]:facade_box(m,x,y,u+side*(ww/2+.035),.42,b-.4,.043,.07,.82,METAL,a)
 # Slim band and fascia, deliberately without classical cornices.
 facade_box(m,x,y,0,.40,3.57,L,.16,.48,S20['GreyFrame'],a)
 facade_box(m,x,y,0,.45,H-.08,L,.42,.18,S21['White'],a)
 for u in [-L/2+.16,L/2-.16]:sf_pipe(m,x,y,u,H,a,METAL)
points=[w['p'] for w in D21[name]['walls']];s21_flat_roof(m,points,H,S21['MetalGreen']);s21_finish(m)

# North entrance of Gallerian only. Keep the previously authored Storgatan entrance.
name='SM_Building_92204159';m=s21_new(name,[(-244.15,-219.92,54.0,65.2,-1,40)])
p=(-220.270,63.882);q=(-243.740,64.113);x,y,L,a=sf_edge(p,q);H=8.65
# Circular light sits in its own square recess; annular plaster closes its corners.
circle_u=7.2;circle_z=6.03;radius=1.19
hs=[(u,4.44,2.75,2.63,0) for u in [-8.9,-4.9,-.9,3.1]]
hs += [(circle_u,circle_z-radius,2*radius,2*radius,0)]
hs += [(u,.27,3.65,3.15,0) for u in [-8.9,-4.45,0,4.45,8.9]]
p18_face(m,x,y,L,H,hs,S20['Limestone'],a)
for u,b,ww,hh,r in hs:
 if abs(u-circle_u)<.01 and b>4:continue
 s21_glass(m,x,y,u,b,ww,hh,a,S21['MetalGreen'],2,0,b<1 and u>=0)
for k in range(64):
 t0=k*math.tau/64;t1=(k+1)*math.tau/64
 ps=[]
 for t,rr in [(t0,radius),(t1,radius),(t1,radius/max(abs(math.cos(t1)),abs(math.sin(t1)))),(t0,radius/max(abs(math.cos(t0)),abs(math.sin(t0))))]:ps.append(lp(x,y,circle_u+rr*math.cos(t),.36,circle_z+rr*math.sin(t),a))
 m.faces(ps,[(0,1,2,3)],S20['Limestone'])
s20_round(m,x,y,circle_u,circle_z,radius,a,S21['MetalGreen'],.38)
facade_box(m,x,y,circle_u,.43,circle_z,2*radius,.06,.04,S21['MetalGreen'],a)
# Stone panel joints stop at openings and stay subordinate to the entrance.
for u in [-L/2+.10,-6.9,-2.9,1.1,5.1,L/2-.1]:facade_box(m,x,y,u,.38,4.12,.025,.035,8.17,S21['Concrete'],a)
facade_box(m,x,y,0,.41,3.88,L,.12,.46,S20['Limestone'],a)
facade_box(m,x,y,0,.40,H-.06,L,.40,.22,S20['Limestone'],a)
# Broad supported glazing canopy. Glass is an original material, never photo texture.
can_u=4.4;can_w=13.5
verts=[lp(x,y,can_u+u,o,z,a) for u,o,z in [(-can_w/2,.45,3.69),(can_w/2,.45,3.69),(can_w/2,2.25,3.48),(-can_w/2,2.25,3.48)]]
m.faces(verts,[(0,1,2,3)],GLAZE)
for o,z in [(.45,3.69),(2.25,3.48)]:facade_box(m,x,y,can_u,o,z,can_w,.085,.10,S21['MetalGreen'],a)
for u in [can_u-can_w/2,can_u,can_u+can_w/2]:
 town_rod(m,lp(x,y,u,2.12,.12,a),lp(x,y,u,2.12,3.5,a),.044,S21['MetalGreen'])
 town_rod(m,lp(x,y,u,.43,3.65,a),lp(x,y,u,2.25,3.45,a),.042,S21['MetalGreen'])
 town_rod(m,lp(x,y,u,.4,4.18,a),lp(x,y,u,1.60,3.53,a),.020,S21['MetalGreen'])
town_text(m,*lp(x,y,4.4,.52,0,a)[:2],4.10,a,'GALLERIAN',6.8,S21['MetalGreen'])
# Front roof terminates exactly at party lines and the retained rear section.
s20_roof(m,-243.74,-220.27,54.01,63.96,H,2.15,'x',S21['MetalGreen'])
for xx in [-243.72,-220.29]:facade_box(m,xx,59.0,0,0,H/2,.10,9.98,H,S20['Limestone'],0)
# Broad angular roof lights with closed cheeks and faceted metal caps.
for u in [-5.3,5.2]:
 xx,yy,_=lp(x,y,u,-1.25,0,a);ww=3.55;b=H+.20;hh=1.30
 s21_glass(m,xx,yy,0,b,ww,hh,a,S21['MetalGreen'],3,0)
 for sign in [-1,1]:facade_box(m,xx,yy,sign*(ww/2+.05),-.53,b+hh/2,.12,1.55,hh,S21['MetalGreen'],a)
 for sign in [-1,1]:
  vs=[lp(xx,yy,du,o,z,a) for du,o,z in [(0,.39,b+hh+.47),(sign*(ww/2+.17),.39,b+hh+.05),(sign*(ww/2+.17),-1.27,b+hh+.05),(0,-1.27,b+hh+.47)]]
  m.faces(vs,[(0,1,2,3)],S21['MetalGreen'])
 m.faces([lp(xx,yy,du,.33,z,a) for du,z in [(-ww/2,b+hh),(ww/2,b+hh),(0,b+hh+.44)]],[(0,1,2)],S21['MetalGreen'])
s21_finish(m)

street21_cameras=[
 ('98_CreamCorner21',(-186.3,69.2,2.1),(-208,61.8,4.2),22),
 ('99_RoseCorner21',(-188.8,67.0,2.1),(-176,79.0,4.8),18),
 ('100_PanelShops21',(-239.0,66.4,2.0),(-227,76.0,4.0),17),
 ('101_WhiteCorner21',(-291.6,66.4,2.0),(-274,80.0,5.4),19),
 ('102_ClassicalCorner21',(-291.2,71.2,2.0),(-276,59.0,5.5),23),
 ('103_CeramicFront21',(-258.2,74.4,2.1),(-258,64.2,5.5),12),
 ('104_GallerianNorth21',(-233.3,73.7,2.0),(-232,64.0,5.0),13),
 ('105_NorraStreet21',(-286.2,69.5,1.85),(-219,68.8,3.4),29),
]
