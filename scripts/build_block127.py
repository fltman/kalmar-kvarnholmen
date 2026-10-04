"""Pass 127: Kalmar slott, the courtyard fronts and the roofs (corrects passes 27, 124 and 126).

- The courtyard eaves come down from pass 27's single eaves level (z 20.27) to z 17.01: 6.54 m above
  the state floor, the mean of Carl Möller's five measured sections of 1882 (Riksarkivet PK006-00041).
  The outer eaves stay z 20.27 (Möller: 20.51, within 0.25 m).
- The roofs are rebuilt asymmetric: pass 27's outer planes are kept, the ridges come down to Möller's
  z 25.47 (the south-west range keeps its measured 24.79) and move towards the outer fronts, and each
  courtyard slope runs from the courtyard eaves to its ridge. All slopes are joined as one surface (the
  upper envelope, computed by scripts/prepare_block127.py with Shapely) and cut where they meet the
  round towers' walls and copper bells and Kuretornet. Steps between pieces and the courtyard wall tops
  are closed by vertical faces.
- Pass 27's four courtyard dormers (red fronts) sit on the new slopes; the chimneys stand tall on the
  courtyard slopes as in the photographs; the chapel turret follows the south-west ridge.
- The courtyard fronts end at the new eaves, with the cornice under the overhang. New window rows:
  the west front's small row, the north front's two small rows, the south-west front's tall lower row
  (photographs 2017 and 2022, Möller 1882), on pass 126's axes; windows that would meet a door or its
  portal are left out. The NW and SW ranges carry painted rustication as shallow blocks; all courtyard
  fronts are lime-washed.
Only SM_Kalmar_Slott is re-created. Pass 124's code (which re-runs pass 27's), as pass 126 composed it,
is run again in private namespaces with single, asserted string replacements.
Sources: references/block127-notes.md.
"""
import re
from mathutils import Vector
from mathutils.geometry import tessellate_polygon
# Pass 125 leaves numbers in the shared names TS and TC, which the town helpers read as materials.
if not isinstance(TS,str):TS=town_mats['Stone']
if not isinstance(TC,str):TC='M_Town_Copper'
B127D=json.loads((R/'source/block127.json').read_text())
block127_names=[];B127={}
for old in [k for k in list(materials) if k.startswith('M_Block127_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Lime','TownPaintWhite',(.92,.89,.81),.92,0),          # lime-washed courtyard fronts (photographs 2017, 2022)
 ('Joint','TownPaintWhite',(.86,.77,.62),.92,0),         # the painted rustication's ochre joints (NW and SW ranges)
 ('Block','TownPaintWhite',(.95,.93,.87),.92,0),         # its pale blocks
 ('Band','TownStone',(.62,.62,.60),.86,0),               # the grey chain band under the state-floor windows
 ('Plinth','TownStone',(.60,.58,.54),.88,0),
 ]:
 name='M_Block127_'+key;B127[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block127_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M127=B127
ZCE127=B127D['zce']

def drop_degenerate_faces127(obj,tol=1e-9):
 # Faces with no area, a repeated corner or a width under 0.1 mm have no UV frame for the export.
 import bmesh
 bm=bmesh.new();bm.from_mesh(obj.data)
 def _thin(f):
  L=max(e.calc_length() for e in f.edges);return L>0 and 2*f.calc_area()/L<1e-4
 bad=[f for f in bm.faces if f.calc_area()<tol or len({v.index for v in f.verts})<len(f.verts) or _thin(f)]
 if bad:bmesh.ops.delete(bm,geom=bad,context='FACES_ONLY')
 bm.to_mesh(obj.data);bm.free();obj.data.update();return len(bad)
def mark127(obj,corrects,osm=''):
 obj['block127_dropped_faces']=drop_degenerate_faces127(obj);print('BLOCK127_DROPPED',obj.name,obj['block127_dropped_faces'],len(obj.data.polygons))
 obj['detail_pass']=127;obj['reference_notes']='references/block127-notes.md';obj['osm_way']=osm
 if corrects:obj['corrects_pass']=corrects
 if obj.name not in block127_names:block127_names.append(obj.name)
 return obj
def rep127(src,old,new):
 assert src.count(old)==1,('source changed',src.count(old),old[:80]);return src.replace(old,new)

# ================================================================= pass 126's composition of pass 124
SRC126=(R/'scripts/build_block126.py').read_text()
NSP127=dict(globals());NSP127['B126D']=json.loads((R/'source/block126.json').read_text())
exec(compile(SRC126[SRC126.index('def rep126(src,old,new):'):SRC126.index('NS126=dict(globals())')],'build_block126.py:composition','exec'),NSP127)
_s=NSP127['_s']
# Marking: the one mesh this pass re-creates is pass 127's.
_s=rep127(_s,"def b124_mark(obj,corrects=None,osm=''):return mark126(obj,'27,124' if corrects==27 and obj.name!='SM_Castle27_Ground' else ('27' if corrects==27 else '124'),osm)\n",
 "def b124_mark(obj,corrects=None,osm=''):return mark127(obj,'27,124,126',osm)\n")
# Only the castle section runs: not pass 27's ground (pass 126), not the towers, nothing after.
_s=rep127(_s,"exec(compile(sec124('# ================================================================= ground: island, ravelin, islets','# ================================================================= fortification walls'),'build_castle27.py:ground (pass 126 courtyard level)','exec'),NS124)",
 "pass   # pass 127: the ground is not re-created")
_s=rep127(_s,"_k=edit_towers126(_k)\nexec(compile(_k,'build_castle27.py:towers (pass 124+126 edits)','exec'),NS124)","_k=edit_towers126(_k)   # pass 127: the towers are not re-created")
_s=rep127(_s,"assert len(NS124['KH124'])==2,NS124['KH124']","assert len(NS124['KH124'])==0,NS124['KH124']")
_end="print('BLOCK124_PASS27_REBUILT',NS124['castle27_names'])\n";assert _s.count(_end)==1;_s=_s[:_s.index(_end)+len(_end)]
# The castle section gets pass 127's edits after pass 126's.
_s=rep127(_s,"exec(compile(EXTRA126,'build_block126.py:pass27_helpers','exec'),NS124);_c=edit_castle126(_c)\n",
 "exec(compile(EXTRA126,'build_block126.py:pass27_helpers','exec'),NS124);exec(compile(EXTRA127,'build_block127.py:pass27_helpers','exec'),NS124);_c=edit_castle127(edit_castle126(_c))\n")
# Courtyard fronts (pass 124's court_front124, with pass 126's state-floor row): the rows per range,
# the new eaves, the cornice under the overhang, no window over a door, the NW and SW ranges' dressing.
_s=rep127(_s,"rows=lambda L_:[(3.8,ZS126,1.2,HS126,0,'first'),(3.8,ZC+1.35,1.2,2.0,0,'ground')] if L_>6 else [(3.8,ZS126,1.2,HS126,0,'first')]",
 "rows=lambda L_,_p=p,_q=q:rows127(L_,_p,_q)")
_s=rep127(_s," if key!=(W1,V):front(m,p,q,ZC,ZE,ma,rows(L),doors,True,False);return"," if key!=(W1,V):front(m,p,q,ZC,ZCE127,ma,rows(L),doors,True,False);dress127(m,p,q,LASTH127);return")
_s=rep127(_s," holes=[hh for hh in holes if abs(hh[0]-CF124['u'])>hh[2]/2+CF124['half']+.1]\n"," holes=[hh for hh in holes if abs(hh[0]-CF124['u'])>hh[2]/2+CF124['half']+.1]\n holes=filt127(holes)\n")
_s=rep127(_s," bz_wall(m,W1,N,ZC,ZE,holes,ma)"," bz_wall(m,W1,N,ZC,ZCE127,holes,ma)")
_s=rep127(_s," lm_cornice(m,x,y,Lm+.4,ZE-.2,a,TRIM,False)"," lm_cornice(m,x,y,Lm+.4,ZCE127-.95,a,TRIM,False)\n dress127(m,W1,N,holes)")
EXTRA127='''
LASTH127=[]
def crange127(p,q,raw=False):
 # The range whose courtyard front the edge p-q is (nearest inner line).
 mx,my=(p[0]+q[0])/2,(p[1]+q[1])/2;best=None
 for nm,r in RANGES.items():
  s,c=rframe(r,(mx,my))
  if r['s0']-1<=s<=r['s1']+1 and (best is None or abs(c-r['inner'])<best[0]):best=(abs(c-r['inner']),nm)
 return best[1] if raw else ('SE' if best[1].startswith('SE') else best[1])
def rows127(L_,p,q):
 rs=B127D['rows'][crange127(p,q,True)]
 return [(sp,b,w,h,0,'r127') for sp,b,w,h in (rs if L_>6 else rs[:1])]
def filt127(holes):
 # No window over a door or its portal (1.2 m to the side, 1.6 m over the arch). Raised doors at the
 # outside stairs are marked by a rise of -0.001.
 isdoor=lambda h:h[1]<ZC+.2 or h[4]<0
 doors=[h for h in holes if isdoor(h)]
 return [h for h in holes if isdoor(h) or not any(abs(h[0]-d[0])<(h[2]+d[2])/2+1.2 and h[1]<d[1]+d[3]+max(d[4],0)+1.6 and h[1]+h[3]>d[1]-.5 for d in doors)]
def raised127(p,q):
 # Raised doors at the outside stairs on this courtyard edge (source/block127.json 'stairs').
 return [(st['u'],st['sill'],st['w'],st['h'],-.001) for st in B127D['stairs'] if math.dist(st['p'],p)<.01 and math.dist(st['q'],q)<.01]
def raised_door127(m,x,y,u,b,w,h,a):
 # A plain stone surround and a panelled leaf, the threshold flush with the stair's landing.
 facade_box(m,x,y,u,.12,b+h/2,w,.08,h,K['Door'],a)
 for s in (-1,1):facade_box(m,x,y,u+s*(w/2+.1),.40,b+h/2,.2,.1,h+.1,TRIM,a)
 facade_box(m,x,y,u,.40,b+h+.12,w+.4,.12,.24,TRIM,a)
def stairs127(m):
 # The outside stairs (Street View 2014): solid stone steps square to the front, a landing at the
 # door's sill, iron handrails on both sides.
 for st in B127D['stairs']:
  x,y,L,a=sf_edge(st['p'],st['q']);u=st['u'];n=st['risers'];W=st['width'];O=.355
  for i in range(n):
   D=st['landing']+(n-1-i)*st['tread'];top=ZC+(i+1)*st['rise']
   facade_box(m,x,y,u,O+D/2,(ZC-.1+top)/2,W,D,top-ZC+.1,K['Coping'],a)
  run=st['landing']+(n-1)*st['tread']
  for s in (-1,1):
   uu=u+s*(W/2-.06)
   town_rod(m,lp(x,y,uu,O+run+.05,ZC+st['rise']+.9,a),lp(x,y,uu,O+st['landing']-.05,st['sill']+.9,a),.022,K['Iron'],6)
   town_rod(m,lp(x,y,uu,O+st['landing']-.05,st['sill']+.9,a),lp(x,y,uu,O+.05,st['sill']+.9,a),.022,K['Iron'],6)
   for oo,zz in ((O+run+.05,ZC+st['rise']),(O+st['landing']-.05,st['sill']),(O+.05,st['sill'])):
    town_rod(m,lp(x,y,uu,oo,zz,a),lp(x,y,uu,oo,zz+.9,a),.02,K['Iron'],6)
# The painted rustication is on the NW and SW ranges (courtyard faces true 295 and 216): Street View 2014,
# panos zCIfieeXGQUNANmWu_Tg9A and jOXzkLldNOjrveyz1T81wg in the courtyard, viewed only. NE is smooth white
# with the 7-step stair; SE_w/SE_e are plain cream lime.
RUST127=('NW','SW')
def cmat127(p,q):return M127['Joint'] if crange127(p,q,True) in RUST127 else M127['Lime']
def dress127(m,p,q,holes):
 # The painted rustication (photographs 2017, 2022, Street View 2014): pale blocks 0.86 x 0.34 m in
 # running bond, 2 cm proud of the ochre-jointed wall; lime margins round the openings; a grey band
 # under the state-floor windows; flat pediments over them; a stone plinth. The blocks are single
 # faces 12 mm proud, so the finishing bevel leaves their size alone.
 if crange127(p,q,True) not in RUST127:return
 x,y,L,a=sf_edge(p,q);O=.355;zb=ZC+.45;zt=ZCE127-1.45;zband=ZS126-.55
 # the plinth stops at the doorways (portal E and the gate passage stand open)
 cuts=sorted((u-w/2-.25,u+w/2+.25) for u,b,w,h,r in holes if b<ZC+.2);at=-L/2
 for c0,c1 in cuts+[(L/2,L/2)]:
  if c0-at>.1:facade_box(m,x,y,(at+c0)/2,O+.02,ZC+.2,c0-at,.04,.5,M127['Plinth'],a)
  at=max(at,c1)
 facade_box(m,x,y,0,O+.015,zband,L,.03,.14,M127['Band'],a)
 keep=[(-L/2,-L/2+.25,ZC,zt),(L/2-.25,L/2,ZC,zt),(-L/2,L/2,zband-.2,zband+.2)]
 for u,b,w,h,r in holes:
  top=b+h+r;keep.append((u-w/2-.34,u+w/2+.34,b-.34,top+(.95 if b>ZS126-.1 else .34)))
  if b>ZC+.2:
   for du,dz,ww,hh in ((0,-.22,w+.44,.2),(0,h+.12,w+.44,.2),(-(w/2+.12),h/2-.05,.2,h+.14),(w/2+.12,h/2-.05,.2,h+.14)):
    facade_box(m,x,y,u+du,O+.008,b+dz+(hh/2 if dz<0 or dz>h else 0),ww,.016,hh,M127['Lime'],a)
   if b>ZS126-.1:tri_prism124(m,[(u-w/2-.3,top+.25),(u+w/2+.3,top+.25),(u,top+.8)],O,O+.05,x,y,a,M127['Lime'])
 k=0;z0=zb
 while z0+.36<=zt:
  u0=-L/2+.25-(.46 if k%2 else 0.0)
  while u0<L/2-.25:
   a0,a1=max(u0,-L/2+.25),min(u0+.88,L/2-.25)
   if a1-a0>.2 and not any(a0<k1 and a1>k0 and z0<z1_ and z0+.36>z0_ for k0,k1,z0_,z1_ in keep):
    fquad127(m,x,y,a0,a1,z0,z0+.36,O+.012,a,M127['Block'])
   u0+=.92
  z0+=.40;k+=1
def fquad127(m,x,y,u0,u1,z0,z1,o,a,ma):
 # A flat rectangle on a facade plane (u0..u1, z0..z1 at out o), facing out of the wall.
 v=[lp(x,y,u0,o,z0,a),lp(x,y,u1,o,z0,a),lp(x,y,u1,o,z1,a),lp(x,y,u0,o,z1,a)]
 c=lp(x,y,0,0,0,a);d=lp(x,y,1,0,0,a);e=lp(x,y,0,1,0,a);du=(d[0]-c[0],d[1]-c[1]);do=(e[0]-c[0],e[1]-c[1])
 if du[1]*do[0]-du[0]*do[1]<0:v=v[::-1]
 m.faces(v,[(0,1,2,3)],ma)
def plane127(pl,p):return pl[0]*p[0]+pl[1]*p[1]+pl[2]
def vquad127(m,p,q,zp0,zp1,zq0,zq1,o,ma):
 # A vertical face from p to q between the given heights, facing o; a triangle where one end closes.
 hp,hq=zp1-zp0,zq1-zq0
 if hp<.005 and hq<.005:return
 v=[(p[0],p[1],zp0),(q[0],q[1],zq0),(q[0],q[1],zq1),(p[0],p[1],zp1)]
 if hp<.005:v=v[:3]
 elif hq<.005:v=[v[0],v[1],v[3]]
 nx,ny=(q[1]-p[1]),-(q[0]-p[0])
 if nx*o[0]+ny*o[1]<0:v=v[::-1]
 m.faces(v,[tuple(range(len(v)))],ma)
def roof127(m):
 # The joined roof surface (prepare_block127.py): each piece flat on its plane, triangulated, with a
 # 0.12 m underside; fascias on the eaves; vertical faces where a piece stands over its neighbour.
 T=.12
 for pc in B127D['roof']:
  pl=pc['plane']
  for rr in pc['rings']:
   flat=[tuple(p) for ring in rr for p in ring]
   for t in tessellate_polygon([[Vector((x_,y_,0)) for x_,y_ in ring] for ring in rr]):
    v=[flat[i] for i in t]
    if (v[1][0]-v[0][0])*(v[2][1]-v[0][1])-(v[1][1]-v[0][1])*(v[2][0]-v[0][0])<0:v.reverse()
    m.faces([(x_,y_,plane127(pl,(x_,y_))) for x_,y_ in v],[(0,1,2)],K['Roof'])
    m.faces([(x_,y_,plane127(pl,(x_,y_))-T) for x_,y_ in v[::-1]],[(0,1,2)],SIGN)
 for e in B127D['eaves']:
  if math.dist(e['p'],e['q'])<.05:continue
  (zp_,zq_)=e['z'];vquad127(m,e['p'],e['q'],zp_-T,zp_,zq_-T,zq_,e['o'],K['Roof'])
  town_rod(m,(*e['p'],zp_-.02),(*e['q'],zq_-.02),.075,K['Roof'],6)
 for g in B127D['gables']:
  (zp_,zq_)=g['z'];vquad127(m,g['p'],g['q'],min(zp_,zq_)-1.0,zp_,min(zp_,zq_)-1.0,zq_,g['o'],K['Render'])
 for st in B127D['steps']:
  vquad127(m,st['p'],st['q'],st['z_lo'][0]-T,st['z_hi'][0],st['z_lo'][1]-T,st['z_hi'][1],st['o'],K['Render'])
 keyp={pc['key']:pc['plane'] for pc in B127D['roof']}
 for sm in B127D['seams']:
  pl=keyp[sm['piece']];town_rod(m,(*sm['a'],plane127(pl,sm['a'])+.028),(*sm['b'],plane127(pl,sm['b'])+.028),.02,K['Roof'],4)
 for rd in B127D['ridges']:
  if math.dist(rd['a'],rd['b'])>.05:town_rod(m,(*rd['a'],rd['z'][0]),(*rd['b'],rd['z'][1]),.07,K['Roof'],6)
 # The courtyard wall tops, closed up to the roof where it passes higher over the wall face.
 for f in B127D['fillers']:
  p,q=f['p'],f['q'];x,y,L,a=sf_edge(p,q);zp_,zq_=f['z']
  pts=[(-L/2,ZCE127),(L/2,ZCE127)]+([(L/2,zq_)] if zq_>ZCE127+.005 else [])+([(-L/2,zp_)] if zp_>ZCE127+.005 else [])
  if len(pts)==4:
   a_=[lp(x,y,u,.355,z,a) for u,z in pts];b_=[lp(x,y,u,.005,z,a) for u,z in pts];hexa124(m,a_,b_,cmat127(p,q))
  elif len(pts)==3:tri_prism124(m,pts,.005,.355,x,y,a,cmat127(p,q))
def chimneys127(m):
 for c in B127D['chimneys']:
  m.box((c['x'],c['y'],(c['z0']+c['z1'])/2),(c['w'],c['d'],c['z1']-c['z0']),K['Chimney'],c['ang'])
  m.box((c['x'],c['y'],c['z1']+.06),(c['w']+.16,c['d']+.16,.12),K['Coping'],c['ang'])
def dormers127(m):
 for d in B127D['dormers']:roof_dormer(m,d['x'],d['y'],0,d['a'],ZCE127,d['sli'],.9,.95,1.2,K['FrameRed'],K['Roof'],K['Frame'],True)
'''
def edit_castle127(c):
 # The roofs: pass 27's per-range gable prisms give way to the joined asymmetric surface.
 i0=c.index('ROOFS=[]\n');i1=c.index(' ROOFS.append((name,r))\n')+len(' ROOFS.append((name,r))\n');assert c.count('ROOFS=[]\n')==1 and c.count(' ROOFS.append((name,r))\n')==1
 c=c[:i0]+'roof127(m)\n'+c[i1:]
 i0=c.index('# Chimneys in salmon render');i1=c.index('# ---------------------------------------------------------------- outer fronts');assert c[i0:i1].count('\n')==5,c[i0:i1]
 c=c[:i0]+'# Chimneys in salmon render with stone caps, standing on the joined roof (pass 127).\nchimneys127(m)\n'+c[i1:]
 c=rep127(c," bz_wall(m,p,q,z0,z1,holes,ma)\n"," holes=filt127(holes) if z0==ZC else holes;bz_wall(m,p,q,z0,z1,holes,ma);LASTH127[:]=holes\n")
 c=rep127(c," if cornice:lm_cornice(m,x,y,L+.4,z1-.2,a,TRIM,dentils)"," if cornice:lm_cornice(m,x,y,L+.4,z1-(.95 if z1==ZCE127 else .2),a,TRIM,dentils)")
 c=rep127(c," ox,oy=math.sin(a),-math.cos(a);ma=K['CourtBlock'] if ox>.6 else K['Court']"," ox,oy=math.sin(a),-math.cos(a);ma=cmat127(p,q)")
 c=rep127(c," if L<2.5:bz_wall(m,p,q,ZC,ZE,[],ma);continue"," if L<2.5:bz_wall(m,p,q,ZC,ZCE127,[],ma);continue")
 c=rep127(c," doors=[(0.0,ZC,1.4,2.4,.7)] if L>12 else []"," doors=([(0.0,ZC,1.4,2.4,.7)] if L>12 else [])+raised127(p,q)")
 c=rep127(c,"  if b<z0+.2:arch_door27(m,x,y,u,b,w,h,r,a)","  if r<0:raised_door127(m,x,y,u,b,w,h,a)\n  elif b<z0+.2:arch_door27(m,x,y,u,b,w,h,r,a)")
 i0=c.index("for name,f in (('SE_w',.5),('NE',.45),('NW',.35),('SW',.55)):\n");i1=c.index("K['FrameRed'],K['Roof'],K['Frame'],True)\n",i0)+len("K['FrameRed'],K['Roof'],K['Frame'],True)\n");assert c[i0:i1].count('\n')==4
 c=c[:i0]+'dormers127(m)\nstairs127(m)\n'+c[i1:]
 c=rep127(c,"r=RANGES['SW'];half,rise,slope,mid=roof_geom(r);x,y,_=rp(r,r['s0']+(r['s1']-r['s0'])*.455,mid,0);zr=ZE+rise",
  "x,y,zr=B127D['turret']['x'],B127D['turret']['y'],B127D['turret']['z']")
 return c
NS127=dict(NSP127);NS127.update(B127D=B127D,M127=M127,ZCE127=ZCE127,mark127=mark127,edit_castle127=edit_castle127,EXTRA127=EXTRA127,rep127=rep127,block127_names=block127_names)
exec(compile(_s,'build_block124.py (pass 126+127 edits)','exec'),NS127)
assert NS127['NS124']['castle27_names']==['SM_Kalmar_Slott'],NS127['NS124']['castle27_names']
assert block127_names==['SM_Kalmar_Slott'],block127_names

# ================================================================= cameras
def sv_camera127(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
_ZC127=B127D['zc']
block127_cameras=[
 # 689: the 2017 courtyard photograph (Commons), camera resected on the south courtyard corner, the
 # SE_w/SE_e bend, the south tower's spire and the well (f 1890 px, 35 px total residual); the
 # photograph is level with its horizon at row 1115 of 1309, so the render is level with a 61.1 degree
 # field and its upper part is compared.
 sv_camera127('689_Block127_Cal_Courtyard2017',-861.1,-292.66,_ZC127+1.6,174.9,0,61.1),
 # 690: the 2022 well photograph (-wuppertaler), camera by search on the well's bearing and width
 # (f 1450 px assumed) with the copper cap at the upper left taken as Kuretornet's.
 sv_camera127('690_Block127_Cal_Well2022',-871.56,-318.72,_ZC127+1.6,346.3,12,82.9),
 sv_camera127('691_Block127_NorthFront',-866.0,-307.0,_ZC127+1.6,62.0,14,70),
 sv_camera127('692_Block127_CourtCorner_N',-866.0,-314.0,_ZC127+1.6,4.0,24,62),
 ('693_Block127_Aerial_Courtyard',(-830.0,-345.0,48.0),(-868.0,-300.0,8.0),24),
 ('694_Block127_Aerial_NW',(-930.0,-230.0,70.0),(-868.0,-300.0,16.0),24),
]
print('BLOCK127_GEOMETRY',len(block127_names))
