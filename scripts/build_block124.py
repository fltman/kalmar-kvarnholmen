"""Pass 124: the approach to Kalmar slott and its courtyard, corrections of pass 27 (castle) and
pass 98 (mainland). One walk from Kungsgatan and Stadsparken over the footbridge, across the ravelin,
over the timber bridge and the drawbridge, through portal A and the vaulted passage under the
rampart, across Västra förborgen, through portal B, the gate passage and portal C into the courtyard.

Re-created pass 27 meshes (same names and categories; pass 27's own code from build_castle27.py is
run verbatim in a private namespace, NS124, with these edits only):
- SM_Castle27_Walls: the ashlar block of portal A narrowed to 3.9 m with a 2.4 m opening and the
  1568 tablet as a framed recessed panel with a simple relief; the passage under the rampart with
  rubble walls, a whitewashed vault and a slab path between cobbles;
- SM_Kalmar_Slott: the octagonal well house removed (rebuilt below), and the courtyard front of the
  west range opened for the gate passage (portal C);
- SM_Kalmar_Slott_Towers: Kuretornet opened for portal B on its north-west face and for the passage
  on its courtyard side; pass 27's blind gate on the north-east face removed;
- SM_Castle27_Bridge: rebuilt (new code) from the photographs: bents every 2.3 m with pale pile
  collars, a pile pier under the hinge of the drawbridge, the leaf, the gallows frame with struts and
  two lifting beams with chains, and the footbridge with a gap in its rail for the stair.
Re-created pass 98 mesh: SM_Slott98_Trees, pass 98's code verbatim with each tree standing on the
lifted park.
New meshes: SM_Castle124_Approach (the lifted park round the footbridge, the city wall, the wooden
stair, the abutment's plinth), SM_Castle124_Passage (the gate passage), SM_Castle124_Portals (portals
B and C, the courtyard portals D, E and F), SM_Castle124_Well (the hexagonal well house of 1578),
SM_Castle124_Paving (slab paths in the courtyard and setts in Västra förborgen).
Sources: OpenStreetMap; Wikimedia Commons and DigitaltMuseum photographs; Olsson, Fornvännen 1957;
see references/block124-notes.md.
"""
import ast,re
from mathutils import Vector
from mathutils.geometry import tessellate_polygon
B124D=json.loads((R/'source/block124.json').read_text());C124=json.loads((R/'source/castle27.json').read_text())
block124_names=[];B124={}
for old in [k for k in list(materials) if k.startswith('M_Block124_')]:bpy.data.materials.remove(materials.pop(old))
for key,texture,target,rough,metal in [
 ('Lime','TownPaintWhite',(.88,.87,.83),.92,0),('Slab','TownStone',(.60,.60,.58),.85,0),('Ashlar','TownStone',(.76,.71,.64),.86,0),
 ('Tablet','TownStone',(.70,.69,.65),.84,0),('Wall','TownStone',(.52,.51,.48),.90,0),('Wood','TownPaintBrown',(.50,.43,.34),.85,0),
 ('WoodDark','TownPaintBrown',(.24,.20,.16),.88,0),('Collar','TownStone',(.74,.73,.70),.85,0),('Iron','TownMetalGrey',(.07,.07,.075),.45,.50),
 ]:
 name='M_Block124_'+key;B124[key]=name;col=lin(target);tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
 mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block124_target_srgb']=list(target)
 ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
 for node in nodes:
  if node.bl_idname=='ShaderNodeTexImage' and node.image:
   twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
   if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
M124=B124
# Pass 27's materials are reused where the new parts continue its surfaces (cut stone, rubble, cobbles).
K124={k:'M_Castle27_'+k for k in ('Trim','KureStone','Revet','Rubble','Cobbles','Coping','Gate','Timber','TimberDark','Iron','Dark','Roof','WellStone','LowWall','Door','Frame','Court','CourtBlock')}
# A pass-27 material that lost its last user (M_Castle27_Gate, after this pass) is dropped when the
# blend is saved; recreate any such material from Trim so later rebuilds from the saved blend run.
# No mesh uses it any more, so geometry and hashes are unaffected.
for _v in [v for v in K124.values() if v not in materials]:
 _g=bpy.data.materials.get(materials['M_Castle27_Trim'] if isinstance(materials['M_Castle27_Trim'],str) else materials['M_Castle27_Trim'].name).copy();_g.name=_v
 materials[_v]=_g if not isinstance(materials['M_Castle27_Trim'],str) else _g.name
 specs.setdefault(_v,dict(specs.get('M_Castle27_Trim',{})))
assert all(v in materials for v in K124.values()),[v for v in K124.values() if v not in materials]

def b124_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 block124_names.append(name);return Mesh(name,category)
def drop_degenerate_faces124(obj,tol=1e-9):
 # Faces with no area, a repeated corner or a width under 0.1 mm have no UV frame for the export.
 import bmesh
 bm=bmesh.new();bm.from_mesh(obj.data)
 def _thin(f):
  L=max(e.calc_length() for e in f.edges);return L>0 and 2*f.calc_area()/L<1e-4
 bad=[f for f in bm.faces if f.calc_area()<tol or len({v.index for v in f.verts})<len(f.verts) or _thin(f)]
 if bad:bmesh.ops.delete(bm,geom=bad,context='FACES_ONLY')
 bm.to_mesh(obj.data);bm.free();obj.data.update();return len(bad)
def b124_mark(obj,corrects=None,osm=''):
 obj['block124_dropped_faces']=drop_degenerate_faces124(obj);print('BLOCK124_DROPPED',obj.name,obj['block124_dropped_faces'],len(obj.data.polygons))
 obj['detail_pass']=124;obj['reference_notes']='references/block124-notes.md';obj['osm_way']=osm
 if corrects:obj['corrects_pass']=corrects
 return obj
def b124_finish(m,corrects=None,osm=''):return b124_mark(s21_finish(m),corrects,osm)

# ---------------------------------------------------------------- shared levels and frames
def zh124(h):return round(-1.33+h,4)
HL124=C124['levels_h'];CA124=C124['castle']
Z0_124=zh124(HL124['foot']);ZC124=zh124(HL124['courtyard']);ZR124=zh124(HL124['rampart']);ZRV124=zh124(HL124['ravelin']);ZD124=zh124(HL124['deck']);ZW124=zh124(0.0)
def hexa124(m,a,b,ma):
 # Closed six-faced solid from two quads a (front) and b (back), corners in matching order.
 m.faces(list(a)+list(b),[(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)],ma)
def beam124(m,a,b,w,h,ma):
 # Square timber from point a to point b (w across, h up).
 a,b=Vector(a),Vector(b);d=(b-a).normalized();s=d.cross(Vector((0,0,1)))
 if s.length<.01:s=d.cross(Vector((0,1,0)))
 s.normalize();u=s.cross(d).normalized()
 q=lambda p:[tuple(p+s*sx*w/2+u*sz*h/2) for sx,sz in ((-1,-1),(1,-1),(1,1),(-1,1))]
 hexa124(m,q(a),q(b),ma)
def tri_prism124(m,pts,o0,o1,x,y,a,ma):
 # A flat triangle (u,z) in a facade frame, extruded from out o0 to o1.
 v=[lp(x,y,u,o,z,a) for o in (o0,o1) for u,z in pts];m.faces(v,[(0,1,2),(5,4,3),(0,3,4,1),(1,4,5,2),(2,5,3,0)],ma)
def fan_prism124(m,c,pts,o0,o1,x,y,a,ma):
 # A curved flat shape built as a triangle fan round c (u,z) and extruded: no large n-gon.
 n=len(pts);v=[lp(x,y,u,o,z,a) for o in (o0,o1) for u,z in [c]+pts];k=n+1
 f=[(0,i+1,i+2) for i in range(n-1)]+[(k,k+i+2,k+i+1) for i in range(n-1)]
 f+=[(i+1,k+i+1,k+i+2,i+2) for i in range(n-1)]+[(0,k,k+1,1),(n,k+n,k,0)]
 m.faces(v,f,ma)

# Kuretornet's fitted rectangle, exactly as pass 27 computes it (build_castle27.py, towers section).
_kp=[tuple(p) for p in CA124['kure']];_ek=max(zip(_kp,_kp[1:]+_kp[:1]),key=lambda e:math.dist(*e));_ka=math.atan2(_ek[1][1]-_ek[0][1],_ek[1][0]-_ek[0][0])
_ku=(math.cos(_ka),math.sin(_ka));_kv=(-_ku[1],_ku[0]);_cx=sum(p[0] for p in _kp)/len(_kp);_cy=sum(p[1] for p in _kp)/len(_kp)
_us=[(p[0]-_cx)*_ku[0]+(p[1]-_cy)*_ku[1] for p in _kp];_vs=[(p[0]-_cx)*_kv[0]+(p[1]-_cy)*_kv[1] for p in _kp]
_cx,_cy=_cx+_ku[0]*(max(_us)+min(_us))/2+_kv[0]*(max(_vs)+min(_vs))/2,_cy+_ku[1]*(max(_us)+min(_us))/2+_kv[1]*(max(_vs)+min(_vs))/2
_hu,_hv=(max(_us)-min(_us))/2,(max(_vs)-min(_vs))/2
KRECT124=[(_cx+_ku[0]*a_*_hu+_kv[0]*b_*_hv,_cy+_ku[1]*a_*_hu+_kv[1]*b_*_hv) for a_,b_ in ((-1,-1),(1,-1),(1,1),(-1,1))]
KNW124=(KRECT124[0],KRECT124[1])            # the north-west face, outward to the outer bailey
def line_hit124(P,d,a,b):
 # Parameter t where P+d*t crosses the line a-b.
 ex,ey=b[0]-a[0],b[1]-a[1];den=d[0]*ey-d[1]*ex;return ((a[0]-P[0])*ey-(a[1]-P[1])*ex)/den
# The gate passage (OSM way 90613986) runs 1.5 m inside Kuretornet's north-east face. It is moved
# 0.9 m south-west so that portal B (4.4 m wide) stands clear of the gate building at the north
# corner, as in the 1957 photograph of Västra förborgen.
_ps=B124D['gate']['passage'];_S,_E=tuple(_ps[0]),tuple(_ps[-1]);_L=math.dist(_S,_E);D124=((_E[0]-_S[0])/_L,(_E[1]-_S[1])/_L)
_perp=(-D124[1],D124[0]) if (-D124[1])*_ku[0]+D124[0]*_ku[1]>0 else (D124[1],-D124[0])   # towards the south-west face
_P=(_S[0]+_perp[0]*.9,_S[1]+_perp[1]*.9)
CI124=[tuple(p) for p in CA124['court']];W1_124,V124,N124=CI124[10],CI124[9],CI124[8]
_t0=line_hit124(_P,D124,*KNW124);A0_124=(_P[0]+D124[0]*_t0,_P[1]+D124[1]*_t0)
T1_124=line_hit124(A0_124,D124,W1_124,N124);A1_124=(A0_124[0]+D124[0]*T1_124,A0_124[1]+D124[1]*T1_124)
FLAT124=1.2
def zf124(t):
 # Floor of the gate passage: level at portal B and at portal C, an even cobbled ramp between.
 if t<=FLAT124:return Z0_124+.03
 if t>=T1_124-FLAT124:return ZC124+.012
 return Z0_124+.03+(ZC124+.012-Z0_124-.03)*(t-FLAT124)/(T1_124-2*FLAT124)
def pt124(t,c=0.0):return (A0_124[0]+D124[0]*t-_perp[0]*c,A0_124[1]+D124[1]*t-_perp[1]*c)
_xn,_yn,_Ln,_an=sf_edge(*KNW124);UB124=(A0_124[0]-_xn)*math.cos(_an)+(A0_124[1]-_yn)*math.sin(_an)
_xc,_yc,_Lc,_ac=sf_edge(W1_124,N124);UC124=(A1_124[0]-_xc)*math.cos(_ac)+(A1_124[1]-_yc)*math.sin(_ac)
print('BLOCK124_PASSAGE A0',[round(v,2) for v in A0_124],'A1',[round(v,2) for v in A1_124],'length',round(T1_124,2),'rise',round(ZC124-Z0_124,2),'uB',round(UB124,2),'uC',round(UC124,2))

# ================================================================= pass 27's own code, re-run with edits
SRC27=(R/'scripts/build_castle27.py').read_text()
NS124=dict(globals())
exec(compile(SRC27[SRC27.index('import ast,random'):SRC27.index('castle27_names=[];K={}')],'build_castle27.py:header','exec'),NS124)
_keys=re.findall(r"^ \('(\w+)','\w+',\(",SRC27[SRC27.index('for key,texture,target,rough,metal in ['):SRC27.index("SIGN=K['Dark']")],re.M)
NS124.update(castle27_names=[],K={k:'M_Castle27_'+k for k in _keys},KH124=[])
exec(compile("SIGN=K['Dark'];TRIM=K['Trim'];GL=GLAZE\nrng=random.Random(27)\n",'build_castle27.py:setup','exec'),NS124)
_t=ast.parse(SRC27);_t.body=[n for n in _t.body if isinstance(n,ast.FunctionDef)]
exec(compile(_t,'build_castle27.py:functions','exec'),NS124)
exec(compile("Z0=zh(HL['foot']);ZC=zh(HL['courtyard']);ZE=zh(HL['eaves']);ZR=zh(HL['rampart']);ZW=zh(0.0)\n",'build_castle27.py:levels','exec'),NS124)
def sec124(a,b):return SRC27[SRC27.index(a):SRC27.index(b)]
def rep124(src,old,new):
 assert src.count(old)==1,('pass 27 source changed',old[:70]);return src.replace(old,new)
NS124.update(PA124={'A0':A0_124,'d':D124,'T':T1_124,'zf':zf124},CF124={'W1':W1_124,'V':V124,'N':N124,'u':UC124,'half':2.6},UB124=UB124)
# Pass 124's replacements, run inside NS124 so that they see pass 27's helpers and constants.
exec(compile('''
def portal_a124(m,a,b,x,y,Lg,ang,ug,ZB,F):
 # Portal A (photographs 2014-2024): an upright ashlar block 3.9 m wide, a round arch of voussoirs
 # 2.4 m wide and 3.55 m high, and Roland Mackle's arms tablet of 1568 under the rampart's edge.
 AS=M124['Ashlar'];T=M124['Tablet']
 bz_wall(m,a,b,ZB-.3,ZR+.05,[(ug,ZB,2.4,2.35,1.2)],AS,-1.8,F)
 facade_box(m,x,y,ug,F-.1,ZR+.13,Lg+.3,.5,.16,K['Coping'],ang)
 p18_arch(m,*lp(x,y,ug,0,0,ang)[:2],ZB+2.35,2.4,1.2,.42,F+.03,ang,AS)
 for s in (-1,1):facade_box(m,x,y,ug+s*1.43,F+.04,ZB+2.30,.48,.08,.14,AS,ang)
 # The tablet: a sill, a frame round a recessed field, a triglyph frieze and a cornice.
 facade_box(m,x,y,ug,F+.07,ZB+3.86,3.3,.14,.12,T,ang)
 facade_box(m,x,y,ug,F+.01,ZB+4.91,2.8,.02,1.98,T,ang)
 for s in (-1,1):facade_box(m,x,y,ug+s*1.49,F+.05,ZB+4.91,.18,.10,1.98,T,ang)
 facade_box(m,x,y,ug,F+.06,ZB+6.12,3.3,.12,.28,T,ang)
 for k in range(9):facade_box(m,x,y,ug-1.5+k*.375,F+.14,ZB+6.12,.09,.04,.24,T,ang)
 facade_box(m,x,y,ug,F+.11,ZB+6.33,3.5,.22,.14,T,ang)
 # Relief as simple blocks: the crowned shield of the Three Crowns between two lions.
 facade_box(m,x,y,ug,F+.06,ZB+4.86,.64,.10,.80,T,ang);facade_box(m,x,y,ug,F+.05,ZB+5.40,.54,.08,.26,T,ang)
 for s in (-1,1):
  facade_box(m,x,y,ug+s*.86,F+.04,ZB+4.66,.52,.07,.96,T,ang);facade_box(m,x,y,ug+s*.66,F+.04,ZB+5.32,.30,.07,.30,T,ang)
  facade_box(m,x,y,ug+s*.95,F+.035,ZB+4.12,.42,.05,.12,T,ang)
def tunnel124(m,TL,tn):
 # The vaulted passage under the rampart (Commons photograph 2017): rubble walls, a whitewashed
 # barrel vault, a path of stone slabs between strips of cobbles. 3.0 m wide, 3.8 m high.
 hw,zw,r,t=1.5,Z0+2.3,1.5,.3
 inner=[(-hw,Z0-.06),(-hw,zw)]+[(-hw*math.cos(k*math.pi/12),zw+r*math.sin(k*math.pi/12)) for k in range(1,12)]+[(hw,zw),(hw,Z0-.06)]
 def outer(c,z):
  if z<=zw+1e-6:return (c+(t if c>0 else -t),z)
  k=(r+t)/r;return (c*k,zw+(z-zw)*k)
 sec=lambda p_,n_,c,z:(p_[0]+n_[0]*c,p_[1]+n_[1]*c,z)
 for (p0,n0),(p1,n1) in zip(zip(TL,tn),list(zip(TL,tn))[1:]):
  for k in range(len(inner)-1):
   (c0,z0),(c1,z1)=inner[k],inner[k+1];o0,o1=outer(c0,z0),outer(c1,z1)
   ma=M124['Lime'] if (z0>zw+1e-6 or z1>zw+1e-6) else K['Revet']
   hexa124(m,[sec(p0,n0,c0,z0),sec(p0,n0,c1,z1),sec(p0,n0,*o1),sec(p0,n0,*o0)],[sec(p1,n1,c0,z0),sec(p1,n1,c1,z1),sec(p1,n1,*o1),sec(p1,n1,*o0)],ma)
  for c0,c1,top,ma in ((-hw,-.6,Z0+.012,K['Cobbles']),(-.6,.6,Z0+.018,M124['Slab']),(.6,hw,Z0+.012,K['Cobbles'])):
   hexa124(m,[sec(p0,n0,c0,Z0-.1),sec(p0,n0,c1,Z0-.1),sec(p0,n0,c1,top),sec(p0,n0,c0,top)],[sec(p1,n1,c0,Z0-.1),sec(p1,n1,c1,Z0-.1),sec(p1,n1,c1,top),sec(p1,n1,c0,top)],ma)
 # Threshold slabs through portal A's block, from the tunnel to the block's face.
 p0,p1=TL[0],TL[1];L_=math.dist(p0,p1);d_=((p1[0]-p0[0])/L_,(p1[1]-p0[1])/L_);n_=tn[0];e=(p0[0]-d_[0]*(F124+.02),p0[1]-d_[1]*(F124+.02))
 hexa124(m,[sec(e,n_,-1.2,Z0-.1),sec(e,n_,1.2,Z0-.1),sec(e,n_,1.2,Z0+.012),sec(e,n_,-1.2,Z0+.012)],[sec(p0,n_,-1.2,Z0-.1),sec(p0,n_,1.2,Z0-.1),sec(p0,n_,1.2,Z0+.012),sec(p0,n_,-1.2,Z0+.012)],M124['Slab'])
def court_front124(m,p,q,ma,L,doors):
 # The courtyard fronts as pass 27 builds them, except the west range's front from the corner by
 # Kuretornet: its two collinear pieces are built as one wall with the gate passage's opening
 # (portal C), and the windows behind the portal are left out.
 rows=lambda L_:[(3.8,ZC+5.6,1.2,2.4,0,'first'),(3.8,ZC+1.35,1.2,2.0,0,'ground')] if L_>6 else [(3.8,ZC+5.6,1.2,2.4,0,'first')]
 key=(tuple(p),tuple(q));W1,V,N=CF124['W1'],CF124['V'],CF124['N']
 if key==(V,N):return
 if key!=(W1,V):front(m,p,q,ZC,ZE,ma,rows(L),doors,True,False);return
 x,y,Lm,a=sf_edge(W1,N);holes=[]
 for s0,s1 in ((W1,V),(V,N)):
  Ls=math.dist(s0,s1);c=math.dist(W1,((s0[0]+s1[0])/2,(s0[1]+s1[1])/2))-Lm/2
  hs=[(0.0,ZC,1.4,2.4,.7)] if Ls>12 else []
  for spacing,b,w,h,r,kind in rows(Ls):hs+=row_holes(Ls,spacing,b,w,h,r)
  holes+=[(u+c,b,w,h,r) for u,b,w,h,r in hs]
 holes=[hh for hh in holes if abs(hh[0]-CF124['u'])>hh[2]/2+CF124['half']+.1]
 gate=(CF124['u'],ZC,2.8,2.4,1.4);holes.append(gate)
 bz_wall(m,W1,N,ZC,ZE,holes,ma)
 for u,b,w,h,r in holes:
  if (u,b,w,h,r)==gate:continue
  if b<ZC+.2:arch_door27(m,x,y,u,b,w,h,r,a)
  elif r>0:p18_win(m,x,y,u,b,w,h,r,a,K['Frame'],K['Brick'],2,2)
  else:s20_window(m,x,y,u,b,w,h,a,K['Frame'],TRIM,.62)
 lm_cornice(m,x,y,Lm+.4,ZE-.2,a,TRIM,False)
def kure_holes124(x,y,L,a,nw):
 # Openings in Kuretornet's walls where the gate passage crosses them: portal B on the north-west
 # face, the passage's arch on the courtyard side. The walls are pass 27's 0.35 m skins.
 ca,sa=math.cos(a),math.sin(a);A0=PA124['A0'];d=PA124['d']
 od=d[0]*sa-d[1]*ca
 if abs(od)<.3:return []
 t=-((A0[0]-x)*sa-(A0[1]-y)*ca)/od;P=(A0[0]+d[0]*t,A0[1]+d[1]*t);u=(P[0]-x)*ca+(P[1]-y)*sa
 if abs(u)>L/2-1.0 or t<-1 or t>PA124['T']+1:return []
 h_=(u,Z0,2.4,2.6,1.2) if nw else (u,PA124['zf'](t)-.05,3.1,2.45,1.55)
 KH124.append(h_);return [h_]
''','build_block124.py:pass27_edits','exec'),NS124)

# Portal A and the passage under the rampart: pass 27's walls section.
_cur=[c for c in C124['curtains'] if c['side']=='NW'][0];F124=_cur['batter']*(ZR124+.05-Z0_124)+.25
NS124.update(F124=F124,W124=1.95)
_w=sec124('# ================================================================= fortification walls','# ================================================================= the four postejer')
_w=rep124(_w,'key=lambda d:math.dist(at(d),gate_o));w=3.3','key=lambda d:math.dist(at(d),gate_o));w=W124')
_i0=_w.index('   # Ashlar gate block');_i1=_w.index("K['KureStone'],ang)\n",_i0)+len("K['KureStone'],ang)\n");assert _w[_i0:_i1].count('\n')==7
_w=_w[:_i0]+'   portal_a124(m,a,b,x,y,Lg,ang,ug,ZB,F)\n'+_w[_i1:]
_i0=_w.index('prof=[(-1.6,Z0-.02)');_i1=_w.index("K['Cobbles'])\n",_i0)+len("K['Cobbles'])\n");assert _w[_i0:_i1].count('\n')==5
_w=_w[:_i0]+'tunnel124(m,TL,tn)\n'+_w[_i1:]
_w=rep124(_w,'((tex,3.2,3.1,1.6),(gate_i,1.6,2.4,.8))','((tex,3.0,2.3,1.5),(gate_i,1.6,2.4,.8))')
exec(compile(_w,'build_castle27.py:walls (pass 124 edits)','exec'),NS124)
# The castle: well house removed, the courtyard front opened for portal C.
_c=sec124('# ================================================================= the castle','# ================================================================= towers, Kuretornet')
_i0=_c.index('# ---------------------------------------------------------------- the well house of 1578');_i1=_c.rindex('c27_finish(m)')
_c=_c[:_i0]+_c[_i1:]
_c=rep124(_c," front(m,p,q,ZC,ZE,ma,[(3.8,ZC+5.6,1.2,2.4,0,'first'),(3.8,ZC+1.35,1.2,2.0,0,'ground')] if L>6 else [(3.8,ZC+5.6,1.2,2.4,0,'first')],doors,True,False)"," court_front124(m,p,q,ma,L,doors)")
exec(compile(_c,'build_castle27.py:castle (pass 124 edits)','exec'),NS124)
# Kuretornet: portal B and the passage's arch instead of the blind gate on the north-east face.
_k=sec124('# ================================================================= towers, Kuretornet','# ================================================================= timber bridges')
_k=rep124(_k,' if gate_face:holes.append((max(-L/2+1.6,min(L/2-1.6,ud)),Z0,2.2,3.0,1.1))',' holes+=kure_holes124(x,y,L,a,nw)')
_k=rep124(_k,' for u,b,w,h,r in holes:\n  if b<Z0+.2:facade_box(m,x,y,u,-1.2,',' for u,b,w,h,r in [h_ for h_ in holes if h_ not in KH124]:\n  if b<Z0+.2:facade_box(m,x,y,u,-1.2,')
exec(compile(_k,'build_castle27.py:towers (pass 124 edits)','exec'),NS124)
assert len(NS124['KH124'])==2,NS124['KH124']
for _n in NS124['castle27_names']:
 block124_names.append(_n);b124_mark(bpy.data.objects[_n],27)
print('BLOCK124_PASS27_REBUILT',NS124['castle27_names'])

# ================================================================= the lifted park at the footbridge (pass 98)
AP124=B124D['approach'];LAND124=tuple(AP124['landing']);ZG124=AP124['zg']
LIFT124=(AP124['z_top']-.015)-(ZG124+.025+.006)        # Kungsgatan's sett meets the deck 15 mm below it
DOM124=[tuple(v) for v in AP124['domain']['outer']];DOMH124=[[tuple(v) for v in h] for h in AP124['domain']['holes']]
def inside124(p,poly):
 x,y=p;c=False;j=len(poly)-1
 for i in range(len(poly)):
  xi,yi=poly[i];xj,yj=poly[j]
  if (yi>y)!=(yj>y) and x<(xj-xi)*(y-yi)/(yj-yi+1e-12)+xi:c=not c
  j=i
 return c
def lift124(x,y,check=False):
 # Smooth rise of the park round the landing: flat within r_flat, a half-cosine to nothing at
 # r_flat+r_fall (the steepest grade is 1:8, the mean 1:13).
 d=math.dist((x,y),LAND124)
 if d>=AP124['r_flat']+AP124['r_fall']:return 0.0
 if check and (not inside124((x,y),DOM124) or any(inside124((x,y),h) for h in DOMH124)):return 0.0
 s=1.0 if d<=AP124['r_flat'] else .5*(1+math.cos(math.pi*(d-AP124['r_flat'])/AP124['r_fall']))
 return LIFT124*s
m=b124_new('SM_Castle124_Approach','Slottsområdet/Ground')
for layer in AP124['layers']:
 ma=B98[layer['mat']];off=ZG124+layer['offset']+.006
 for piece in layer['pieces']:
  rings=[piece['outer']]+piece['holes'];flatv=[(x,y) for r in rings for x,y in r]
  for t in tessellate_polygon([[Vector((x,y,0)) for x,y in r] for r in rings]):
   v=[(flatv[i][0],flatv[i][1],off+lift124(*flatv[i])) for i in t]
   if (v[1][0]-v[0][0])*(v[2][1]-v[0][1])-(v[1][1]-v[0][1])*(v[2][0]-v[0][0])<0:v.reverse()
   m.faces(v,[(0,1,2)],ma)
# The city wall (OSM 1084130858) retaining the park along the ditch, a quay wall at the water:
# rubble with a stone coping flush with the lawn, split every 1.5 m to follow the rise.
for e in AP124['edges']:
 p,q=e['p'],e['q'];L=math.dist(p,q);n=max(1,math.ceil(L/1.5));nx,ny=(q[1]-p[1])/L,-(q[0]-p[0])/L
 zb=-.1 if e['side']!='water' else -1.9
 for k in range(n):
  a=(p[0]+(q[0]-p[0])*k/n,p[1]+(q[1]-p[1])*k/n);b=(p[0]+(q[0]-p[0])*(k+1)/n,p[1]+(q[1]-p[1])*(k+1)/n)
  za,zb_=ZG124+.006+lift124(*a),ZG124+.006+lift124(*b)
  if max(za,zb_)<ZG124+.03:continue
  o=lambda P,d_:(P[0]+nx*d_,P[1]+ny*d_)
  hexa124(m,[(*a,zb),(*o(a,.35),zb),(*o(a,.35),za-.02),(*a,za-.02)],[(*b,zb),(*o(b,.35),zb),(*o(b,.35),zb_-.02),(*b,zb_-.02)],M124['Wall'])
  hexa124(m,[(*o(a,-.05),za-.02),(*o(a,.42),za-.02),(*o(a,.42),za+.01),(*o(a,-.05),za+.01)],[(*o(b,-.05),zb_-.02),(*o(b,.42),zb_-.02),(*o(b,.42),zb_+.01),(*o(b,-.05),zb_+.01)],K124['Coping'])
# The bridge's park abutment (pass 27) stood 0.35 m clear of the ditch; a plinth now carries it.
RVB124=[tuple(v) for v in C124['bridges']['ravelin']['points']];_ab=RVB124[0];_aa=math.atan2(RVB124[1][1]-_ab[1],RVB124[1][0]-_ab[0])
m.box((_ab[0],_ab[1],(ZG124-.1+ZRV124-.2-3.42+.01)/2),(3.6,3.6,ZRV124-.2-3.42+.01-(ZG124-.1)),K124['LowWall'],_aa)
# The wooden stair (OSM 93293022: 30 steps, handrail) from the ditch path up along the wall to the
# abutment's top beside the bridge deck.
_wa,_wb=[tuple(v) for v in AP124['wall_osm'][6:8]];_wl=math.dist(_wa,_wb);UW124=((_wb[0]-_wa[0])/_wl,(_wb[1]-_wa[1])/_wl);SW124=(UW124[1],-UW124[0])
_bd=((RVB124[1][0]-_ab[0]),(RVB124[1][1]-_ab[1]));_bl=math.hypot(*_bd);_bd=(_bd[0]/_bl,_bd[1]/_bl);_bn=(_bd[1],-_bd[0])   # +c is the west side
_sc=(LAND124[0]+SW124[0]*1.15,LAND124[1]+SW124[1]*1.15)
_te=line_hit124(_sc,(-UW124[0],-UW124[1]),(_ab[0]+_bn[0]*1.8,_ab[1]+_bn[1]*1.8),(_ab[0]+_bn[0]*1.8+_bd[0],_ab[1]+_bn[1]*1.8+_bd[1]))
ST_END124=(_sc[0]-UW124[0]*_te,_sc[1]-UW124[1]*_te);ST_RUN124=12.6;NSTEP124=30
ST_START124=(ST_END124[0]-UW124[0]*ST_RUN124,ST_END124[1]-UW124[1]*ST_RUN124)
ST_Z0_124=ZG124+.025;ST_Z1_124=ZRV124-.2-.02;RISE124=(ST_Z1_124-ST_Z0_124)/NSTEP124;TREAD124=ST_RUN124/NSTEP124
_sa=math.atan2(UW124[1],UW124[0]);SWID124=1.5
for i in range(1,NSTEP124+1):
 c=(ST_START124[0]+UW124[0]*(i-.5)*TREAD124,ST_START124[1]+UW124[1]*(i-.5)*TREAD124);z=ST_Z0_124+i*RISE124
 m.box((c[0],c[1],z-.03),(TREAD124+.02,SWID124,.06),M124['Wood'],_sa)
for s in (-1,1):
 sp=lambda P,z:(P[0]+SW124[0]*s*(SWID124/2+.04),P[1]+SW124[1]*s*(SWID124/2+.04),z)
 beam124(m,sp(ST_START124,ST_Z0_124-.05),sp(ST_END124,ST_Z1_124-.09),.08,.26,M124['WoodDark'])
 hs=1.1 if s>0 else .95
 for k in range(10):
  f=k/9;P=(ST_START124[0]+UW124[0]*ST_RUN124*f,ST_START124[1]+UW124[1]*ST_RUN124*f);z=ST_Z0_124+(ST_Z1_124-ST_Z0_124)*f
  if s>0:m.box((P[0]+SW124[0]*(SWID124/2+.1),P[1]+SW124[1]*(SWID124/2+.1),z+hs/2),(.1,.1,hs),M124['Wood'],_sa)
 town_rod(m,sp(ST_START124,ST_Z0_124+hs),sp(ST_END124,ST_Z1_124+hs),.035,M124['Wood'],6)
# Short posts carry the stair's middle on the ditch floor.
for f in (.35,.7):
 P=(ST_START124[0]+UW124[0]*ST_RUN124*f,ST_START124[1]+UW124[1]*ST_RUN124*f);z=ST_Z0_124+(ST_Z1_124-ST_Z0_124)*f
 for s in (-1,1):m.box((P[0]+SW124[0]*s*.6,P[1]+SW124[1]*s*.6,(ZG124+z-.1)/2),(.14,.14,z-.1-ZG124),M124['WoodDark'],_sa)
b124_finish(m,None,'1084130858')

# Pass 98's trees, verbatim (build_block98.py), each standing on the lifted park.
m=b124_new('SM_Slott98_Trees','Slottsområdet/Vegetation')
for i,(x,y,s) in enumerate(B98D['trees']):
 rng124=random.Random(98000+i);h=rng124.uniform(9.5,13.5)*s;r=rng124.uniform(3.4,4.8)*s;trunk=h*.40;z0=ZG+lift124(x,y,True)
 m.lathe(x,y,z0,[(.24,0),(.20,.4),(.16,trunk*.6),(.13,trunk)],B98['Bark'],8)
 cz=z0+trunk+(h-trunk)*.52
 blob79(m,(x,y,cz),(r*.85,r*.85,(h-trunk)*.46),B98['Leaf'],10,6)
 for k in range(3):
  a=rng124.uniform(0,math.tau);d=rng124.uniform(.35,.65)*r;rr=r*rng124.uniform(.38,.55)
  blob79(m,(x+math.cos(a)*d,y+math.sin(a)*d,cz+rng124.uniform(-.2,.35)*(h-trunk)*.5),(rr,rr,rr*.8),B98['LeafLight'] if k%2 else B98['Leaf'],8,5)
b124_finish(m,98)

# ================================================================= the timber bridges and the drawbridge (pass 27)
def along124(pts,s):
 acc=0.0
 for p,q in zip(pts,pts[1:]):
  L=math.dist(p,q)
  if s<=acc+L+1e-9:t=(s-acc)/L;return (p[0]+(q[0]-p[0])*t,p[1]+(q[1]-p[1])*t),((q[0]-p[0])/L,(q[1]-p[1])/L)
  acc+=L
 p,q=pts[-2],pts[-1];L=math.dist(p,q);return q,((q[0]-p[0])/L,(q[1]-p[1])/L)
def deck124(m,pts,s0,s1,zf,w,step=3.0):
 n=max(1,math.ceil((s1-s0)/step))
 for k in range(n):
  a=s0+(s1-s0)*k/n;b=s0+(s1-s0)*(k+1)/n;pa,_=along124(pts,a);pb,_=along124(pts,b)
  NS124['plank_deck'](m,pa,pb,zf(a),zf(b),w,K124['Timber'])
  _,u=along124(pts,(a+b)/2);nx,ny=u[1],-u[0]
  for c in (-w/2+.35,0,w/2-.35):town_rod(m,(pa[0]+nx*c,pa[1]+ny*c,zf(a)-.28),(pb[0]+nx*c,pb[1]+ny*c,zf(b)-.28),.14,K124['TimberDark'],6)
def bent124(m,pts,s,zf,w,collar,pile_c):
 p,u=along124(pts,s);nx,ny=u[1],-u[0];ang=math.atan2(u[1],u[0]);z=zf(s)
 for c in pile_c:
  m.box((p[0]+nx*c,p[1]+ny*c,(zh124(-2.2)+z-.45)/2),(.26,.26,z-.45-zh124(-2.2)),K124['TimberDark'],ang)
  if collar:m.cylinder(p[0]+nx*c,p[1]+ny*c,ZW124-.15,.21,.62,M124['Collar'],12)
 m.box((p[0],p[1],z-.52),(.3,w+.3,.24),K124['TimberDark'],ang)
def rails124(m,pts,s0,s1,zf,w,skip=()):
 for side in (-1,1):
  c=side*(w/2-.06);n=max(1,round((s1-s0)/1.6));runs=[(s0,s1)]
  for side_,a,b in skip:
   if side_==side:runs=[r_ for lo,hi in runs for r_ in ((lo,min(hi,a)),(max(lo,b),hi)) if r_[1]-r_[0]>.3]
  for lo,hi in runs:
   k=max(1,round((hi-lo)/1.6))
   for i in range(k+1):
    s=lo+(hi-lo)*i/k;p,u=along124(pts,s);m.box((p[0]+u[1]*c,p[1]-u[0]*c,zf(s)+.55),(.12,.12,1.1),K124['Timber'],math.atan2(u[1],u[0]))
   for hz,rw,rh in ((1.08,.10,.14),(.55,.07,.10)):
    k2=max(1,math.ceil((hi-lo)/4.0))
    for j in range(k2):
     a=lo+(hi-lo)*j/k2;b=lo+(hi-lo)*(j+1)/k2;pa,ua=along124(pts,a);pb,ub=along124(pts,b)
     beam124(m,(pa[0]+ua[1]*c,pa[1]-ua[0]*c,zf(a)+hz+rh/2),(pb[0]+ub[1]*c,pb[1]-ub[0]*c,zf(b)+hz+rh/2),rw,rh,K124['Timber'])
m=b124_new('SM_Castle27_Bridge','Kalmar slott/Bridges')
MAIN124=[tuple(v) for v in C124['bridges']['main']['points']];WB124=C124['bridges']['main']['width']
# The deck now ends at the face of portal A's block (pass 27 ran it into the arch); the threshold
# slabs through the block belong to the walls.
_go=tuple(C124['gate']['outer']);LEAF124=4.2
def main_end124():
 # Arc length where the deck meets the block's face: F along the outward normal of the NW
 # revetment at the gate (pass 27's frame), measured back along the deck.
 cur=_cur;pts=[tuple(p) for p in cur['runs'][0]];L=[0.0]
 for p,q in zip(pts,pts[1:]):L.append(L[-1]+math.dist(p,q))
 def at(d):
  for k in range(len(pts)-1):
   if L[k]<=d<=L[k+1]:t=(d-L[k])/(L[k+1]-L[k]);return (pts[k][0]+(pts[k+1][0]-pts[k][0])*t,pts[k][1]+(pts[k+1][1]-pts[k][1])*t)
  return pts[-1]
 dg=min(range(int(L[-1])),key=lambda d:math.dist(at(d),_go));a,b=at(dg-1.95),at(dg+1.95);ang=math.atan2(b[1]-a[1],b[0]-a[0]);on=(math.sin(ang),-math.cos(ang))
 face=(_go[0]+on[0]*F124,_go[1]+on[1]*F124);fa=(face[0]+math.cos(ang),face[1]+math.sin(ang))
 acc=0.0
 for p,q in zip(MAIN124,MAIN124[1:]):
  L_=math.dist(p,q);u=((q[0]-p[0])/L_,(q[1]-p[1])/L_);t=line_hit124(p,u,face,fa)
  if -1e-6<=t<=L_+1e-6:return acc+t
  acc+=L_
 raise RuntimeError('deck does not reach the gate face')
SEND124=main_end124();SLEAF124=SEND124-LEAF124
zmain124=lambda s:ZRV124+(ZD124-ZRV124)*min(1.0,s/SEND124)
deck124(m,MAIN124,0.0,SLEAF124-.03,zmain124,WB124)
deck124(m,MAIN124,SLEAF124,SEND124,zmain124,WB124-.1,step=LEAF124)
_k=0
while _k*2.3<SLEAF124-1.2:bent124(m,MAIN124,_k*2.3,zmain124,WB124,True,(-WB124/2+.3,WB124/2-.3));_k+=1
# The pier under the leaf's hinge: a cluster of piles with a heavy cap (photograph from the rampart, 2017).
_p,_u=along124(MAIN124,SLEAF124);_n=(_u[1],-_u[0]);_ang=math.atan2(_u[1],_u[0]);_z=zmain124(SLEAF124)
for ds in (-.45,.05):
 for c in (-1.35,-.45,.45,1.35):
  P=(_p[0]+_u[0]*ds+_n[0]*c,_p[1]+_u[1]*ds+_n[1]*c);m.box((P[0],P[1],(zh124(-2.2)+_z-.5)/2),(.3,.3,_z-.5-zh124(-2.2)),K124['TimberDark'],_ang)
  m.cylinder(P[0],P[1],ZW124-.15,.23,.62,M124['Collar'],12)
m.box((_p[0]-_u[0]*.2,_p[1]-_u[1]*.2,_z-.45),(.9,WB124+.9,.32),K124['TimberDark'],_ang)
rails124(m,MAIN124,0.0,SLEAF124-.05,zmain124,WB124)
rails124(m,MAIN124,SLEAF124+.3,SEND124-.2,zmain124,WB124-.1)
# The gallows over the hinge (photographs of 1934 and of the 1930s-40s, and 2014-2024): two posts
# beside the deck, a head beam higher than the rampart's edge, struts down to the deck on both sides,
# and two lifting beams over the head that rest on the block above the arms tablet and project past
# the frame, with chains from their outer ends to the deck.
_zt=_z+6.9
for side in (-1,1):
 c=side*(WB124/2+.18);P=(_p[0]+_n[0]*c,_p[1]+_n[1]*c)
 m.box((P[0],P[1],(_z-.6+_zt)/2),(.3,.3,_zt-_z+.6),K124['TimberDark'],_ang)
 for ds in (-1.7,1.7):beam124(m,(P[0],P[1],_z+3.3),(P[0]+_u[0]*ds,P[1]+_u[1]*ds,_z+.05),.14,.14,K124['TimberDark'])
 inner=(_p[0]+_u[0]*(LEAF124+.35)+_n[0]*c,_p[1]+_u[1]*(LEAF124+.35)+_n[1]*c,ZR124+.36)
 piv=_zt+.46;k=(piv-inner[2])/(LEAF124+.35);outer=(_p[0]-_u[0]*1.2+_n[0]*c,_p[1]-_u[1]*1.2+_n[1]*c,piv+k*1.2)
 beam124(m,outer,inner,.26,.32,K124['TimberDark'])
 cs=side*(WB124/2-.12);foot=(_p[0]-_u[0]*1.05+_n[0]*cs,_p[1]-_u[1]*1.05+_n[1]*cs,zmain124(SLEAF124-1.05)+.12)
 town_rod(m,(outer[0]+_u[0]*.15,outer[1]+_u[1]*.15,outer[2]-.16),foot,.03,M124['Iron'],6)
 ci=(inner[0]-_u[0]*.25,inner[1]-_u[1]*.25,inner[2]-.16);cb=(ci[0],ci[1],ZD124+2.5)
 town_rod(m,ci,cb,.025,M124['Iron'],6)
 for j in range(8):
  t0,t1=j*math.tau/8,(j+1)*math.tau/8;rr=.11
  town_rod(m,(cb[0]+_u[0]*rr*math.sin(t0),cb[1]+_u[1]*rr*math.sin(t0),cb[2]-rr+rr*math.cos(t0)),(cb[0]+_u[0]*rr*math.sin(t1),cb[1]+_u[1]*rr*math.sin(t1),cb[2]-rr+rr*math.cos(t1)),.018,M124['Iron'],6)
 Pk=(P[0]-_n[0]*side*.9,P[1]-_n[1]*side*.9);beam124(m,(P[0],P[1],_zt-1.1),(Pk[0],Pk[1],_zt-.02),.13,.13,K124['TimberDark'])   # knee brace
beam124(m,(_p[0]-_n[0]*(WB124/2+.45),_p[1]-_n[1]*(WB124/2+.45),_zt+.15),(_p[0]+_n[0]*(WB124/2+.45),_p[1]+_n[1]*(WB124/2+.45),_zt+.15),.32,.3,K124['TimberDark'])
# The footbridge from the park to the ravelin (OSM 91222140), as pass 27 built it, with the west rail
# open where the stair arrives.
_lr=sum(math.dist(p,q) for p,q in zip(RVB124,RVB124[1:]));zrv124=lambda s:ZRV124-.2+.2*s/_lr;WR124=C124['bridges']['ravelin']['width']
deck124(m,RVB124,0.0,_lr,zrv124,WR124)
_k=0
while _k*2.3<=_lr+.01:bent124(m,RVB124,min(_k*2.3,_lr-.15),zrv124,WR124,False,(-WR124/2+.3,WR124/2-.3));_k+=1
rails124(m,RVB124,.05,_lr-.05,zrv124,WR124,skip=((1,0.0,2.9),))
b124_finish(m,27,'24455363')

# ================================================================= the gate passage (Kuretornet and the west range)
m=b124_new('SM_Castle124_Passage','Kalmar slott/Castle')
HW124,ZWALL124,RV124,TH124=1.5,2.4,1.5,.3
_prof=[(-HW124,-.08),(-HW124,ZWALL124)]+[(-HW124*math.cos(k*math.pi/12),ZWALL124+RV124*math.sin(k*math.pi/12)) for k in range(1,12)]+[(HW124,ZWALL124),(HW124,-.08)]
def _out124(c,z):
 if z<=ZWALL124+1e-6:return (c+(TH124 if c>0 else -TH124),z)
 k=(RV124+TH124)/RV124;return (c*k,ZWALL124+(z-ZWALL124)*k)
_ts=sorted(set([0.0,FLAT124,T1_124-FLAT124,T1_124]+[k*1.0 for k in range(1,int(T1_124))]))
def _sp124(t,c,z):P=pt124(t,c);return (P[0],P[1],zf124(t)+z)
for t0,t1 in zip(_ts,_ts[1:]):
 for k in range(len(_prof)-1):
  (c0,z0),(c1,z1)=_prof[k],_prof[k+1];o0,o1=_out124(c0,z0),_out124(c1,z1)
  ma=M124['Lime']
  hexa124(m,[_sp124(t0,c0,z0),_sp124(t0,c1,z1),_sp124(t0,*o1),_sp124(t0,*o0)],[_sp124(t1,c0,z0),_sp124(t1,c1,z1),_sp124(t1,*o1),_sp124(t1,*o0)],ma)
 # a stone plinth band 0.6 m high along both walls
 for c in (-HW124,HW124):
  s=1 if c>0 else -1
  hexa124(m,[_sp124(t0,c-s*.04,-.05),_sp124(t0,c,-.05),_sp124(t0,c,.6),_sp124(t0,c-s*.04,.6)],[_sp124(t1,c-s*.04,-.05),_sp124(t1,c,-.05),_sp124(t1,c,.6),_sp124(t1,c-s*.04,.6)],K124['KureStone'])
 for c0,c1,dz,ma in ((-HW124,-.6,0,K124['Cobbles']),(-.6,.6,.006,M124['Slab']),(.6,HW124,0,K124['Cobbles'])):
  hexa124(m,[_sp124(t0,c0,-.12),_sp124(t0,c1,-.12),_sp124(t0,c1,dz),_sp124(t0,c0,dz)],[_sp124(t1,c0,-.12),_sp124(t1,c1,-.12),_sp124(t1,c1,dz),_sp124(t1,c0,dz)],ma)
# Thresholds through the two walls and out under the portals.
for t0,t1,z in ((-1.25,0.0,Z0_124+.03),(T1_124,T1_124+1.35,ZC124+.012)):
 hexa124(m,[(*pt124(t0,-1.3),z-.12),(*pt124(t0,1.3),z-.12),(*pt124(t0,1.3),z),(*pt124(t0,-1.3),z)],[(*pt124(t1,-1.3),z-.12),(*pt124(t1,1.3),z-.12),(*pt124(t1,1.3),z),(*pt124(t1,-1.3),z)],M124['Slab'])
# Iron lanterns hang from the vault (photograph of portal A, 2014), one at each end.
for t in (2.0,T1_124-2.0):
 P=pt124(t);z=zf124(t)+ZWALL124+RV124
 town_rod(m,(P[0],P[1],z-.02),(P[0],P[1],z-.55),.012,M124['Iron'],6);m.box((P[0],P[1],z-.72),(.26,.26,.34),M124['Iron'],math.atan2(D124[1],D124[0]))
b124_finish(m,None,'90613986')

# ================================================================= portals B, C, D, E and F
m=b124_new('SM_Castle124_Portals','Kalmar slott/Castle')
TR124=K124['Trim'];O124=.355                       # pass 27's walls: outer face 0.355 out from the line
def fb124(m,x,y,u,d,z0,z1,w,ma,a,o=O124):facade_box(m,x,y,u,o+d/2,(z0+z1)/2,w,d,z1-z0,ma,a)   # box standing on the wall face
def column124(m,x,y,u,o,z0,h,r,a,ma,fl=16):
 X,Y,_=lp(x,y,u,o,0,a)
 poly_lathe(m,X,Y,z0,[(r+.06,0),(r+.06,.1),(r,.16),(r*.98,h*.4),(r*.86,h-.2),(r*.9,h-.14),(r+.07,h-.08),(r+.07,h)],ma,fl,a)
def entab124(m,x,y,u,z,w,a,ma,triglyphs=0,metopes=False,d=.6):
 # Architrave, frieze (triglyph blocks, square metope plates) and cornice on the wall face: 0.98 m.
 fb124(m,x,y,u,d,z,z+.34,w,ma,a);fb124(m,x,y,u,d-.06,z+.34,z+.78,w-.1,ma,a)
 for k in range(triglyphs):
  uu=u-w/2+.3+k*(w-.6)/max(1,triglyphs-1);fb124(m,x,y,uu,d-.03,z+.36,z+.76,.2,ma,a,O124+.03)
  if metopes and k<triglyphs-1:um=uu+(w-.6)/max(1,triglyphs-1)/2;fb124(m,x,y,um,.03,z+.45,z+.67,.22,ma,a,O124+d-.06)
 fb124(m,x,y,u,d+.2,z+.78,z+.98,w+.3,ma,a)
# Portal B on Kuretornet's north-west face (1957 photograph of Västra förborgen and the postcard
# from the passage under the rampart): fluted Doric columns on tall plain pedestals, a triglyph frieze
# with metopes, a small lean-to roof of sheet metal, and a round arch 2.4 m wide.
x,y,L,a=sf_edge(*KNW124);u=UB124;zb=Z0_124
for s in (-1,1):
 uu=u+s*1.75
 fb124(m,x,y,uu,.84,zb,zb+.2,.86,TR124,a);fb124(m,x,y,uu,.8,zb+.2,zb+1.5,.72,TR124,a);fb124(m,x,y,uu,.84,zb+1.5,zb+1.62,.84,TR124,a)
 column124(m,x,y,uu,O124+.42,zb+1.62,3.3,.23,a,TR124)
 fb124(m,x,y,uu,.66,zb+4.92,zb+5.02,.66,TR124,a,O124+.09)
entab124(m,x,y,u,zb+5.02,4.4,a,TR124,7,True,.85)
_zr=zb+6.45;_zf=zb+6.03
m.faces([lp(x,y,u-2.45,O124,_zr+.04,a),lp(x,y,u+2.45,O124,_zr+.04,a),lp(x,y,u+2.45,O124+1.1,_zf+.04,a),lp(x,y,u-2.45,O124+1.1,_zf+.04,a),
 lp(x,y,u-2.45,O124,_zr,a),lp(x,y,u+2.45,O124,_zr,a),lp(x,y,u+2.45,O124+1.1,_zf,a),lp(x,y,u-2.45,O124+1.1,_zf,a)],[(0,1,2,3),(7,6,5,4),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)],K124['Roof'])
p18_arch(m,*lp(x,y,u,0,0,a)[:2],zb+2.6,2.4,1.2,.32,O124+.04,a,TR124)
for s in (-1,1):fb124(m,x,y,u+s*1.36,.12,zb+2.48,zb+2.62,.36,TR124,a)
# Portal C, the west courtyard portal (Olsson 1957; Mayer's lithograph about 1840): two storeys,
# paired fluted columns below and above, the arms tablet with Johan III's crowned initials between.
x,y,L,a=sf_edge(W1_124,N124);u=UC124;zc=ZC124
for s in (-1,1):
 for du in (1.75,2.35):
  uu=u+s*du;fb124(m,x,y,uu,.62,zc,zc+1.0,.5,TR124,a);fb124(m,x,y,uu,.66,zc+1.0,zc+1.08,.58,TR124,a)
  column124(m,x,y,uu,O124+.33,zc+1.08,3.0,.17,a,TR124)
entab124(m,x,y,u,zc+4.08,5.3,a,TR124,9,False,.66)
fb124(m,x,y,u,.5,zc+5.06,zc+5.26,3.6,TR124,a)
for s in (-1,1):
 for du in (1.05,1.55):column124(m,x,y,u+s*du,O124+.25,zc+5.26,1.7,.12,a,TR124,12)
fb124(m,x,y,u,.16,zc+5.4,zc+6.7,1.5,TR124,a);fb124(m,x,y,u,.06,zc+5.7,zc+6.4,.9,M124['Tablet'],a,O124+.16)
fb124(m,x,y,u,.08,zc+6.44,zc+6.66,.5,TR124,a,O124+.16)
entab124(m,x,y,u,zc+6.96,3.8,a,TR124,0,False,.5)
tri_prism124(m,[(u-1.9,zc+7.94),(u+1.9,zc+7.94),(u,zc+8.4)],O124,O124+.45,x,y,a,TR124)
p18_arch(m,*lp(x,y,u,0,0,a)[:2],zc+2.4,2.8,1.4,.3,O124+.04,a,TR124)
# The courtyard portals D, E and F dress three of pass 27's doors (Olsson 1957: D Drottningtrappan
# with banded Doric columns, E Kungstrappan, F Kyrkportalen of 1568 with herms). Pass 27's doors are
# 1.4 m wide with their arched trims to 3.44 m.
_doors={'D':(N124,CI124[7]),'E':(CI124[0],W1_124),'F':(CI124[2],CI124[1])}
for key,(p,q) in _doors.items():
 assert math.dist(p,q)>12
 x,y,L,a=sf_edge(p,q);u=0.0;z=ZC124
 if key=='D':
  for s in (-1,1):
   uu=u+s*1.28;fb124(m,x,y,uu,.6,z,z+.3,.66,TR124,a)
   column124(m,x,y,uu,O124+.3,z+.3,3.18,.19,a,TR124)
   for k in range(7):fb124(m,x,y,uu,.55,z+.53+k*.4,z+.71+k*.4,.5,TR124,a,O124+.025)
  entab124(m,x,y,u,z+3.48,3.3,a,TR124,5,False)
 elif key=='E':
  for s in (-1,1):
   uu=u+s*1.18;fb124(m,x,y,uu,.24,z,z+.24,.42,TR124,a);fb124(m,x,y,uu,.2,z+.24,z+3.45,.32,TR124,a)
  entab124(m,x,y,u,z+3.45,2.9,a,TR124,0,False,.32)
  tri_prism124(m,[(u-1.6,z+4.43),(u+1.6,z+4.43),(u,z+5.05)],O124,O124+.3,x,y,a,TR124)
 else:
  for s in (-1,1):
   uu=u+s*1.2
   v=[lp(x,y,uu+su*wd/2,oo,zz,a) for oo in (O124,O124+.22) for su,wd,zz in ((-1,.24,z+.3),(1,.24,z+.3),(1,.4,z+2.75),(-1,.4,z+2.75))]
   hexa124(m,v[:4],v[4:],TR124)
   fb124(m,x,y,uu,.3,z,z+.3,.46,TR124,a);fb124(m,x,y,uu,.26,z+2.75,z+3.17,.3,TR124,a);fb124(m,x,y,uu,.3,z+3.17,z+3.31,.5,TR124,a)
  entab124(m,x,y,u,z+3.31,3.0,a,TR124,0,False,.32)
  tri_prism124(m,[(u-1.7,z+4.29),(u+1.7,z+4.29),(u,z+4.75)],O124,O124+.3,x,y,a,TR124)
  fb124(m,x,y,u,.08,z+4.38,z+4.62,.5,M124['Tablet'],a,O124+.3)
b124_finish(m)

# ================================================================= the well house of 1578, hexagonal
# Olsson (Fornvännen 1957): a domed shaft about 1.5 m across inside a parapet with six pedestals,
# Doric columns carrying a hexagonal entablature, six low pediments, six curved brackets up to a
# moulded slab, a lantern of six herms under a dome with six round-topped gables, and a cast-iron
# dolphin on its nose. The photographs (2022, about 1900) show a square pier inside each round
# column, so each corner has one round column and one square shaft. Heights from the 1890s
# photograph, scaled on the man standing beside it (about 7.1 m to the dolphin's tail).
m=b124_new('SM_Castle124_Well','Kalmar slott/Castle')
WX124,WY124=CA124['well'];WS124=K124['WellStone'];Zw=ZC124
_fa=math.atan2(A1_124[1]-WY124,A1_124[0]-WX124)            # one face turned to portal C
CORN124=[_fa+math.pi/6+k*math.pi/3 for k in range(6)]
def wpt124(r,t):return (WX124+r*math.cos(t),WY124+r*math.sin(t))
def hexring124(m,z0,z1,Rc,rin,ma,sub=3):
 # A hexagonal ring (corner radius Rc) round a round hole (radius rin), as closed wedges.
 for k in range(6):
  t0=CORN124[k];t1=t0+math.pi/3;c0,c1=wpt124(Rc,t0),wpt124(Rc,t1)
  for j in range(sub):
   f0,f1=j/sub,(j+1)/sub;o0=(c0[0]+(c1[0]-c0[0])*f0,c0[1]+(c1[1]-c0[1])*f0);o1=(c0[0]+(c1[0]-c0[0])*f1,c0[1]+(c1[1]-c0[1])*f1)
   if rin>0:
    i0,i1=wpt124(rin,t0+(t1-t0)*f0),wpt124(rin,t0+(t1-t0)*f1)
    hexa124(m,[(*i0,z0),(*o0,z0),(*o1,z0),(*i1,z0)],[(*i0,z1),(*o0,z1),(*o1,z1),(*i1,z1)],ma)
   else:m.faces([(WX124,WY124,z0),(*o0,z0),(*o1,z0),(WX124,WY124,z1),(*o0,z1),(*o1,z1)],[(0,2,1),(3,4,5),(0,1,4,3),(1,2,5,4),(2,0,3,5)],ma)
m.lathe(WX124,WY124,Zw-.05,[(2.3,0),(2.3,.19),(2.0,.19),(2.0,.33)],WS124,32)
m.cylinder(WX124,WY124,Zw-.9,.75,1.5,K124['Dark'],24)
hexring124(m,Zw+.28,Zw+.42,1.47,.76,WS124);hexring124(m,Zw+.42,Zw+1.12,1.36,.76,WS124);hexring124(m,Zw+1.12,Zw+1.24,1.44,.76,WS124)
for t in CORN124:
 P=wpt124(1.3,t)
 m.box((P[0],P[1],Zw+.37),(.66,.62,.18),WS124,t);m.box((P[0],P[1],Zw+.85),(.54,.5,.78),WS124,t);m.box((P[0],P[1],Zw+1.30),(.64,.6,.12),WS124,t)
 M_=wpt124(1.58,t);m.box((M_[0],M_[1],Zw+.88),(.06,.26,.32),WS124,t)          # lion and goat masks
 poly_lathe(m,*wpt124(1.38,t),Zw+1.36,[(.17,0),(.17,.08),(.13,.12),(.125,1.0),(.115,1.62),(.15,1.68),(.15,1.74),(.19,1.74),(.19,1.8)],WS124,12)
 Q_=wpt124(1.06,t);m.box((Q_[0],Q_[1],Zw+2.26),(.22,.22,1.8),WS124,t)
 tm=t+math.pi/6;F_=wpt124(1.19,tm)                                             # cartouche on each face
 m.box((F_[0],F_[1],Zw+.8),(.05,.7,.46),WS124,tm);m.box((F_[0]+.03*math.cos(tm),F_[1]+.03*math.sin(tm),Zw+.8),(.05,.3,.34),WS124,tm)
hexring124(m,Zw+3.16,Zw+3.36,1.52,.85,WS124);hexring124(m,Zw+3.36,Zw+3.60,1.46,.85,WS124);hexring124(m,Zw+3.60,Zw+3.74,1.66,.85,WS124)
hexring124(m,Zw+3.74,Zw+3.80,1.5,0,WS124)
for t in CORN124:
 tm=t+math.pi/6;c0,c1=wpt124(1.47,t),wpt124(1.47,t+math.pi/3)
 for f in (.25,.5,.75):m.box((c0[0]+(c1[0]-c0[0])*f,c0[1]+(c1[1]-c0[1])*f,Zw+3.48),(.06,.12,.22),WS124,tm)   # triglyphs
 xm,ym=wpt124(1.36,tm)
 tri_prism124(m,[(-.81,Zw+3.74),(.81,Zw+3.74),(0,Zw+4.16)],-.08,.06,xm,ym,tm-math.pi/2,WS124)       # a low pediment, flush with the cornice
 pts=[(*wpt124(1.3-.62*math.sin(f*math.pi/2),t),Zw+3.80+.87*(1-math.cos(f*math.pi/2))) for f in (0,.25,.5,.75,1.0)]
 town_path(m,pts,.08,WS124)                                                      # a curved bracket up to the slab
poly_lathe(m,WX124,WY124,Zw+3.80,[(.5,0),(.5,.87)],WS124,6,CORN124[0])
poly_lathe(m,WX124,WY124,Zw+4.67,[(.82,0),(.88,.08),(.92,.16),(.78,.18)],WS124,6,CORN124[0])
# The lantern: six herms, a cornice, a dome with six round-topped gables, the dolphin.
hexring124(m,Zw+4.85,Zw+5.15,.72,.42,WS124)
for t in CORN124:
 P=wpt124(.58,t)
 v=[(P[0]+math.cos(t+math.pi/2)*su*wd/2+math.cos(t)*so*.08,P[1]+math.sin(t+math.pi/2)*su*wd/2+math.sin(t)*so*.08,zz) for so in (-1,1) for su,wd,zz in ((-1,.12,Zw+5.15),(1,.12,Zw+5.15),(1,.18,Zw+6.01),(-1,.18,Zw+6.01))]
 hexa124(m,v[:4],v[4:],WS124)
 m.box((P[0],P[1],Zw+6.11),(.2,.2,.2),WS124,t)
hexring124(m,Zw+6.21,Zw+6.35,.74,.3,WS124);hexring124(m,Zw+6.35,Zw+6.43,.80,0,WS124)
poly_lathe(m,WX124,WY124,Zw+6.43,[(.70,0),(.66,.12),(.55,.27),(.38,.39),(.2,.46),(.06,.5)],WS124,6,CORN124[0])
for t in CORN124:
 tm=t+math.pi/6;xm,ym=wpt124(.6,tm)
 fan_prism124(m,(0,Zw+6.43),[(.22*math.cos(k*math.pi/10),Zw+6.43+.22*math.sin(k*math.pi/10)) for k in range(11)],-.03,.03,xm,ym,tm-math.pi/2,WS124)
_dp=[(*wpt124(px,_fa),Zw+pz) for px,pz in ((0,6.91),(.05,7.07),(.07,7.22),(.03,7.33),(-.06,7.39))]
for (p0,p1),r in zip(zip(_dp,_dp[1:]),(.045,.075,.065,.045)):town_rod(m,p0,p1,r,M124['Iron'],8)
for s in (-1,1):town_rod(m,_dp[-1],(_dp[-1][0]-.12*math.cos(_fa)+s*.1*math.sin(_fa),_dp[-1][1]-.12*math.sin(_fa)-s*.1*math.cos(_fa),Zw+7.45),.03,M124['Iron'],6)
b124_finish(m)

# ================================================================= paving
m=b124_new('SM_Castle124_Paving','Kalmar slott/Ground')
SL124=M124['Slab']
def slab124(m,p,q,w,z,ma,depth=.1):
 L=math.dist(p,q);ux,uy=(q[0]-p[0])/L,(q[1]-p[1])/L;nx,ny=uy*w/2,-ux*w/2
 hexa124(m,[(p[0]-nx,p[1]-ny,z-depth),(p[0]+nx,p[1]+ny,z-depth),(p[0]+nx,p[1]+ny,z),(p[0]-nx,p[1]-ny,z)],[(q[0]-nx,q[1]-ny,z-depth),(q[0]+nx,q[1]+ny,z-depth),(q[0]+nx,q[1]+ny,z),(q[0]-nx,q[1]-ny,z)],ma)
# The courtyard (photographs 2017-2022, Mayer about 1840): cobbles with an apron of flat slabs round the
# well and slab paths to the portals.
for k in range(32):
 t0,t1=k*math.tau/32,(k+1)*math.tau/32
 r0,r1=2.3,3.1;P=lambda r,t:(WX124+r*math.cos(t),WY124+r*math.sin(t))
 hexa124(m,[(*P(r0,t0),ZC124-.1),(*P(r1,t0),ZC124-.1),(*P(r1,t1),ZC124-.1),(*P(r0,t1),ZC124-.1)],[(*P(r0,t0),ZC124+.012),(*P(r1,t0),ZC124+.012),(*P(r1,t1),ZC124+.012),(*P(r0,t1),ZC124+.012)],SL124)
_targets=[pt124(T1_124+1.35)]
for key,(p,q) in _doors.items():x,y,L,a=sf_edge(p,q);_targets.append(lp(x,y,0,.355+.9,0,a)[:2])
for P in _targets:
 d=math.dist(P,(WX124,WY124));u=((P[0]-WX124)/d,(P[1]-WY124)/d)
 slab124(m,(WX124+u[0]*3.05,WY124+u[1]*3.05),P,1.2,ZC124+.012,SL124)
# Västra förborgen: setts along the OSM footway from the passage under the rampart to portal B,
# with a slab path down the middle as in the passage itself.
_bp=[tuple(C124['tunnel'][-1]),tuple(B124D['route']['bailey'][1]),pt124(-1.25)]
for (p,q),dz in zip(zip(_bp,_bp[1:]),(0,.001)):
 slab124(m,p,q,3.0,Z0_124+.035+dz,K124['Cobbles']);slab124(m,p,q,1.2,Z0_124+.045+dz,SL124)
b124_finish(m)

def sv_camera124(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
def _cam_on_main124(s,dh):
 p,u=along124(MAIN124,s);return p[0],p[1],zmain124(s)+dh,math.degrees(math.atan2(u[0],u[1]))-28.2
block124_cameras=[
 # Photograph matches (Commons): the bridge towards the gate (ThomasLendt 2018), the drawbridge
 # (Steinkatz 2024), portal A from the leaf (Oregran 2014), the well house (-wuppertaler 2022).
 sv_camera124('666_Block124_Cal_Bridge',-925.36,-226.54,zmain124(4.0)+1.6,100.0,5,62),
 sv_camera124('667_Block124_Cal_Drawbridge',*_cam_on_main124(SEND124-10.0,1.7),12,48),
 sv_camera124('668_Block124_Cal_PortalA',*_cam_on_main124(SEND124-4.5,1.6),30,72),
 sv_camera124('669_Block124_Cal_Well',-869.33,-319.28,ZC124+1.6,327.6,12,72),
 ('670_Block124_Aerial_Approach',(-990.0,-120.0,70.0),(-905.0,-245.0,6.0),24),
]
print('BLOCK124_GEOMETRY',len(block124_names))
