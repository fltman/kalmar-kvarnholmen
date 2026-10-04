"""Pass 120: correction of the fire station site at Larmgatan / Södra Kanalgatan,
SM_Kvarnholmen_House_91846968, first built by landmarks pass 14 (build_landmarks14.py, line 183 on).
The mesh is re-created with two parts:
- the old 1905 station in the east half: pass 14's code for the long front, the side and rear
  facades, the roofs, the dormers, the west bay and the hose tower, copied verbatim below
  (OLD14_CODE120) and run in pass 14's own helper environment (NS120), so it comes out the same;
- the modern western part, rebuilt from three Street View panoramas instead of pass 14's cream
  three-row box at 10 m:
  - the limestone-clad five-storey block on Larmgatan: a tall shop-front ground floor, three storeys
    of large windows over brown panels, the top floor set back from the courtyard face with a glass
    rail on the terrace, flat roofs; it reaches about 8 m north of the OSM north-west corner;
  - the white rendered wing between it and the old station: two full storeys, a third in a dark
    mansard with wall dormers, a gutter line, a flat top;
  - the one-storey glazed pavilion in front of the white wing, in line with the stone block's north
    face: glass walls with mullions, a grey fascia, a roof terrace with a glass rail.
References: Google Street View (view only). Zones: source/block120.json; see
references/block120-notes.md.
"""
B120D=json.loads((R/'source/block120.json').read_text());Z120=B120D['zones']
block120_names=[];B120={}
for old in [k for k in list(materials) if k.startswith('M_Block120_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Lime','TownStone',(.75,.72,.65),.88,0),('LimeShade','TownStone',(.62,.60,.55),.90,0),('Panel','TownPaintBrown',(.43,.29,.20),.70,0),
 ('FrameDark','TownMetalGrey',(.17,.17,.18),.50,.30),('White','TownPaintWhite',(.93,.93,.91),.80,0),('RoofDark','TownMetalGrey',(.25,.26,.28),.60,.25),
 ('Fascia','TownMetalGrey',(.52,.53,.54),.55,.25),('Rail','TownMetalGrey',(.64,.65,.66),.45,.40),('Plinth','TownStone',(.44,.44,.43),.90,0),
 ('Flat','TownMetalGrey',(.33,.33,.34),.70,.15),
 ]:
 name='M_Block120_'+key;B120[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block120_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
GL120=town_mats['Glass']
def b120_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block120_names.append(name);return Mesh(name,category)
def drop_degenerate_faces120(obj,tol=1e-9):
 # Faces with no area, a repeated corner or a width under 0.1 mm have no UV frame for the export.
 import bmesh
 bm=bmesh.new();bm.from_mesh(obj.data)
 def _thin(f):
  L=max(e.calc_length() for e in f.edges);return L>0 and 2*f.calc_area()/L<1e-4
 bad=[f for f in bm.faces if f.calc_area()<tol or len({v.index for v in f.verts})<len(f.verts) or _thin(f)]
 if bad:bmesh.ops.delete(bm,geom=bad,context='FACES_ONLY')
 bm.to_mesh(obj.data);bm.free();obj.data.update();return len(bad)
def b120_finish(m,osm):
 obj=s21_finish(m);obj['block120_dropped_faces']=drop_degenerate_faces120(obj);print('BLOCK120_DROPPED',m.name,obj['block120_dropped_faces'],len(obj.data.polygons))
 obj['detail_pass']=120;obj['corrects_pass']=14;obj['reference_notes']='references/block120-notes.md';obj['osm_way']=osm;return obj

# ---------------------------------------------------------------- pass 14's environment
# Pass 14's own setup (its lines up to the material table) and every function it defines, run in a
# private namespace so that its helper versions (facade_box, lm_cornice, town_polyprofile ...) do not
# replace the ones later passes use.
NS120=dict(globals())
_t120=ast.parse((R/'scripts/build_landmarks14.py').read_text())
_t120.body=[n for n in _t120.body if n.lineno<=16 or isinstance(n,ast.FunctionDef)]
exec(compile(_t120,'build_landmarks14.py','exec'),NS120)

# Pass 14's old 1905 station, verbatim (build_landmarks14.py lines 183-235). Changes: the mesh is
# created by b120_new instead of l14_new, the modern wing (lines 184-194) is left out, and the final
# m.finish() is done by b120_finish after the modern part.
OLD14_CODE120='''
poly=L14['buildings']['91846968']['polygon'];fa=math.atan2(7.013,-42.22);fx,fy=(-232.567-190.347)/2,(280.42+273.407)/2;FL=math.hypot(42.22,7.013)
# Old long front, seven tall arched former vehicle doors, eastern regular bay.
spacing=FL/9;us=[-FL/2+(i+.5)*spacing for i in range(9)];holes=[]
for i,u in enumerate(us):
 holes.append((u,.15 if i>=2 else .85,2.55 if i>=2 else 1.1,2.7 if i>=2 else 1.65,1.25 if i>=2 else 0))
 holes.append((u,5.30,1.25,2.1 if i<7 else 4.5,0))
holes=[h for h in holes if not(h[1]>5 and h[0]>FL/2-10.6)]+[(FL/2-5.3+du,5.30,1.25,4.5,0) for du in [-3.3,0,3.3]]
l14_face(m,fx,fy,FL,10.50,holes,CR,fa)
for u,z,w,h,r in holes:l14_win(m,fx,fy,u,z,w,h,r,fa,SC['RedWood'] if z<.2 else TW,CR,3 if z<5 else 6,3 if z<.2 else 2)
for i,u in enumerate(us):
 if i>=2:
  for off in [-.9,0,.9]:facade_box(m,fx,fy,u+off,.22,.61,.75,.10,.92,SC['RedWood'],fa)
for z in [4.65,10.45]:lm_cornice(m,fx,fy,FL,z,fa,CR)
# Horizontal rustication avoids openings and sits as fine recessed-shadow courses.
for k in range(1,25):
 zz=k*.42
 spans=[(-FL/2,FL/2)]
 for u,b,w,h,r in holes:
  if b-.03<zz<b+h+r+.03:spans=[(l,rr) for lo,hi in spans for l,rr in [(lo,min(hi,u-w/2-.1)),(max(lo,u+w/2+.1),hi)] if rr>l+.04]
 for lo,hi in spans:facade_box(m,fx,fy,(lo+hi)/2,.361,zz,hi-lo,.012,.016,TS,fa)
# Side/rear facade retains lower service rooms and stair tower.
for x,y,L,a in l14_edges([(-232.567,280.42),(-190.347,273.407),(-190.38,259.505),(-202.368,261.499),(-204.359,255.417),(-226.912,259.792)]):
 if y>270:continue
 n=max(1,round(L/4));hs=[(-L/2+(i+.5)*L/n,z,1.2,1.85,0) for i in range(n) for z in [1.0,5.2]];l14_face(m,x,y,L,10.5,hs,CR,a)
 for u,z,w,h,r in hs:l14_win(m,x,y,u,z,w,h,r,a,TW,CR,4,2)
cx,cy,_=lp(fx,fy,0,-7,0,fa);l14_hip(m,cx,cy,FL+1,15.2,10.60,3.35,CU,fa,2.25)
l14_hip(m,cx,cy,FL-3.5,10.7,14.0,.55,CU,fa,1)
for u in us[:7]:
 dx,dy,_=lp(fx,fy,u,.83,0,fa);lm_dormer(m,dx,dy,11.0,1.65,fa,CU)
# Raised western gymnasium bay and its decorated tall-window front.
u=FL/2-5.3;wx,wy,_=lp(fx,fy,u,-.12,0,fa)
for du in [-4.7,4.7]:facade_box(m,wx,wy,du,.48,7.6,.34,.35,5.5,CR,fa)
for du in [-3.3,0,3.3]:lm_panel(m,wx,wy,du,5.02,2.6,.52,fa,RS)
lm_cornice(m,wx,wy,10.6,10.7,fa,CR);cx2,cy2,_=lp(wx,wy,0,-6.4,0,fa);l14_hip(m,cx2,cy2,10.6,13.6,10.9,4.1,CU,fa,2.2)
town_polyprofile(m,*lp(wx,wy,0,.5,0,fa)[:2],10.85,[(-2.1,0),(2.1,0),(1.65,1.4),(.9,1.8),(-.9,1.8),(-1.65,1.4)],fa,CR,.3,False);lm_panel(m,wx,wy,0,11.72,2.65,.9,fa,RS)
# Slang tower on the courtyard side, square masonry base with octagonal lantern.
tx,ty,_=lp(fx,fy,FL/2-7,-14.7,0,fa);m.box((tx,ty,10.2),(4.5,4.5,20.4),CR,fa)
for aa in [fa+j*math.pi/2 for j in range(4)]:
 xx,yy,_=lp(tx,ty,0,2.27,0,aa)
 for z in [4,10.7,16.5]:l14_win(m,*lp(xx,yy,0,.35,0,aa)[:2],0,z,.78,2.40,0,aa,TW,CR,6,2)
 lm_cornice(m,xx,yy,4.8,20.4,aa,CR)
l14_lantern(m,tx,ty,20.62,1.20,3.2)
'''

# ---------------------------------------------------------------- the modern part
def win120(m,x,y,a,u,b,w,h,frame,panel=None,ph=0,mull=1,out=.20):
 # Glass recessed in the opening, an optional coloured panel in its bottom ph metres, frame bars.
 if panel and ph>0:facade_box(m,x,y,u,out+.01,b+ph/2,w-.02,.06,ph,panel,a)
 gb=b+ph;gh=h-ph
 facade_box(m,x,y,u,out,gb+gh/2,w-.02,.04,gh,GL120,a)
 for s in (-1,1):facade_box(m,x,y,u+s*(w/2-.035),out+.03,b+h/2,.07,.08,h,frame,a)
 facade_box(m,x,y,u,out+.03,b+h-.035,w-.14,.08,.07,frame,a);facade_box(m,x,y,u,out+.03,gb+.035,w-.14,.08,.07,frame,a)
 for k in range(1,mull+1):facade_box(m,x,y,u-w/2+k*w/(mull+1),out+.03,gb+gh/2,.06,.08,gh-.14,frame,a)
def rail120(m,p,q,z,out=.18,h=1.05):
 # Frameless glass balustrade with a steel top rail.
 x,y,L,a=sf_edge(p,q)
 if L<.3:return
 facade_box(m,x,y,0,out,z+h/2-.03,L-.04,.025,h-.06,GL120,a);facade_box(m,x,y,0,out,z+h-.015,L,.06,.05,B120['Rail'],a)
def stone_wall120(m,w):
 # Limestone: tall shop windows, then large windows over brown panels on every storey.
 p,q,z0,z1,kind=w['p'],w['q'],w['z0'],w['z1'],w['kind'];x,y,L,a=sf_edge(p,q)
 if kind=='party' or L<.05:return
 top=kind in ('outer','setback') and z0>=13
 levels=[(13.5,2.8)] if top else [(0.0,4.4),(4.4,3.0),(7.4,3.0),(10.4,3.1)]
 holes=[];wins=[]
 if L>2.2:
  n=max(1,round(L/3.3));step=L/n
  for i in range(n):
   u=-L/2+(i+.5)*step
   for f,fh in levels:
    if f<z0-.01 or f+fh>z1+.01:continue
    if top and kind=='setback':hl=(u,f+.05,min(2.4,step-.7),2.35,0);wins.append(hl+(None,0,2))
    elif top:hl=(u,f+.35,min(2.0,step-.9),2.05,0);wins.append(hl+(None,0,1))
    elif f==0:hl=(u,.30,min(2.7,step-.7),3.55,0);wins.append(hl+(None,0,2))
    else:hl=(u,f+.30,min(2.1,step-.9),2.25,0);wins.append(hl+(B120['Panel'],.62,1))
    holes.append(hl[:5])
 bz_wall(m,p,q,z0,z1,holes,B120['Lime'])
 for u,b,ww,hh,r,pan,ph,mu in wins:win120(m,x,y,a,u,b,ww,hh,B120['FrameDark'],pan,ph,mu)
 facade_box(m,x,y,0,.17,z1+.04,L+.02,.40,.08,B120['LimeShade'],a)
 if z0<.01:facade_box(m,x,y,0,.40,.12,L,.10,.24,B120['Plinth'],a)
def white_wall120(m,w,eaves):
 # White render: ground and first-floor windows, the third storey's windows rising into dormers.
 p,q,z0,z1,kind=w['p'],w['q'],w['z0'],w['z1'],w['kind'];x,y,L,a=sf_edge(p,q)
 if kind=='party' or L<.05:return
 if kind=='party_old':bz_wall(m,p,q,z0,z1,[],B120['White']);return
 holes=[];wins=[];dorm=[]
 if L>2.6:
  n=max(1,round(L/3.6));step=L/n
  for i in range(n):
   u=-L/2+(i+.5)*step
   for b,ww,hh in [(.75,1.5,2.35),(5.25,1.3,2.25)]:
    if b>=z0-.01:holes.append((u,b,ww,hh,0));wins.append((u,b,ww,hh))
   holes.append((u,eaves-1.0,1.2,1.0,0));dorm.append(u)
 bz_wall(m,p,q,z0,z1,holes,B120['White'])
 for u,b,ww,hh in wins:win120(m,x,y,a,u,b,ww,hh,B120['White'],mull=1)
 for u in dorm:
  # Wall dormer: the window runs from 1.0 m under the eaves to 1.25 m above them.
  du=1.9;zt=eaves+1.6
  hx,hy=lp(x,y,u,0,0,a)[:2]
  bz_wall(m,lp(x,y,u-du/2,0,0,a)[:2],lp(x,y,u+du/2,0,0,a)[:2],eaves,zt,[(0,eaves,1.2,1.25,0)],B120['White'])
  win120(m,x,y,a,u,eaves-1.0,1.2,2.25,B120['White'],mull=1)
  for s in (-1,1):facade_box(m,hx,hy,s*(du/2-.06),-.22,(eaves+zt)/2,.12,1.15,zt-eaves,B120['White'],a)
  # Hipped hood: eaves 10 cm proud of the front, the ridge running back into the mansard.
  e=du/2+.12
  vs=[lp(hx,hy,uu,oo,zz,a) for uu,oo,zz in [(-e,.47,zt),(e,.47,zt),(e,-.85,zt),(-e,-.85,zt),(0,-.05,zt+.55),(0,-.85,zt+.55)]]
  m.faces(vs,[(0,1,4),(1,2,5,4),(3,0,4,5),(2,3,5),(3,2,1,0)],B120['RoofDark'])
 facade_box(m,x,y,0,.43,eaves-.07,L+.1,.20,.16,B120['RoofDark'],a)
 if z0<.01:facade_box(m,x,y,0,.40,.12,L,.10,.24,B120['Plinth'],a)
def pavilion_wall120(m,w):
 # Floor-to-fascia glass with dark mullions every 1.5 m, a grey fascia on top.
 p,q,z0,z1,kind=w['p'],w['q'],w['z0'],w['z1'],w['kind'];x,y,L,a=sf_edge(p,q)
 if kind!='outer' or L<.05:return
 n=max(1,round(L/1.5))
 facade_box(m,x,y,0,.20,.05,L,.40,.10,B120['Plinth'],a)
 facade_box(m,x,y,0,.18,(z1-.6+.10)/2,L,.04,z1-.6-.10,GL120,a)
 for k in range(n+1):facade_box(m,x,y,-L/2+k*L/n,.22,(z1-.6)/2,.09 if 0<k<n else .22,.12 if 0<k<n else .40,z1-.6,B120['FrameDark'],a)
 for zz in (1.05,3.2):facade_box(m,x,y,0,.22,zz,L,.10,.06,B120['FrameDark'],a)
 facade_box(m,x,y,0,.21,z1-.30,L+.40,.42,.60,B120['Fascia'],a)
 rail120(m,p,q,z1,out=.10)
def flat_roof120(m,ring,tris,z,ma):
 m.faces([(v[0],v[1],z) for v in ring],[tuple(t) for t in tris],ma)

m=b120_new('SM_Kvarnholmen_House_91846968','Kvarnholmen/Landmarks')
NS120['m']=m
exec(compile(OLD14_CODE120,'build_landmarks14.py (pass 14 old station, verbatim)','exec'),NS120)
block120_old_part_verts=len(m.v)      # pass 14's old part is m.v[:block120_old_part_verts]
zs=Z120['stone'];zt=Z120['stone_top'];zp=Z120['pavilion'];zw=Z120['white']
for w in zs['walls']:stone_wall120(m,w)
flat_roof120(m,zs['roof_ring'],zs['roof_tris'],zs['height']-.02,B120['Flat'])
# The terrace rail along the courtyard edge, where the top floor stands back.
for w in zs['walls']:
 if w['neighbour'] in ('white','pavilion') or (w['kind']=='outer' and min(w['p'][0],w['q'][0])>-263.71 and w['p'][1]>285):rail120(m,w['p'],w['q'],zs['height']+.08,out=.20)
for w in zt['walls']:stone_wall120(m,w)
flat_roof120(m,zt['roof_ring'],zt['roof_tris'],zt['height']-.02,B120['Flat'])
for w in zp['walls']:pavilion_wall120(m,w)
flat_roof120(m,zp['roof_ring'],zp['roof_tris'],zp['height'],B120['Flat'])
for w in zw['walls']:white_wall120(m,w,zw['height'])
# Mansard: the slope from the gutter line 0.40 m outside the walls to the inset flat top.
ow120=zw['outer_eave'];iw120=zw['inner'];n120=len(ow120)
for i in range(n120):
 j=(i+1)%n120;m.faces([(*ow120[i],zw['height']),(*ow120[j],zw['height']),(*iw120[j],zw['top']),(*iw120[i],zw['top'])],[(0,1,2,3)],B120['RoofDark'])
flat_roof120(m,iw120,zw['roof_tris'],zw['top'],B120['Flat'])
b120_finish(m,'91846968')

def sv_camera(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block120_cameras=[
 sv_camera('646_Block120_Cal_LarmgatanCorner',-272.4,301.5,2.45,152,12),
 sv_camera('647_Block120_Cal_KanalWhiteWing',-242.6,318.71,1.94,162.2,15),
 sv_camera('648_Block120_Cal_PavilionFromDrum',-277.02,292.22,2.0,25,15),
 ('649_Block120_Aerial',(-215.0,330.0,55.0),(-252.0,268.0,6.0),24)]
print('BLOCK120_GEOMETRY',len(block120_names))
