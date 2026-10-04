"""Pass 129: Kalmar slott, the courtyard's dormers, doors and portals (corrects passes 27, 124, 126, 127, 128).

Measured on the 2014 Street View courtyard panoramas (viewed only) from pass 128's resected cameras,
and on the 2017 and 2022 courtyard photographs (scripts/prepare_block129.py, source/block129.json):
- Dormers: one red-fronted gabled dormer on SE_e beside the SE_w/SE_e bend, and three small grey ones
  (a louvred vent on NE, shed dormers on SW and NW); pass 27/127's four red dormers go.
- Doors at courtyard level: none on NE except the two raised ones (pass 27's middle doors go); portal
  D's arched door raised on a 3-step stair 6.9 m from the east corner; SE_w's two small arched doors;
  SE_e's wide arched door by the bend; SE_e's 9-step stair moved to its measured place.
- SM_Castle124_Portals: portal D (banded columns, a segmental cap) moves to its door and stands on the
  stair's landing; portal C is rebuilt to its measured two storeys (6.69 m, top z 12.16, flat cornice,
  the relief panel between the upper pairs), and the gate passage's arch in the front to 2.6 x 3.25 m.
- SM_Castle124_Paving: the slab path to portal D follows it to the foot of its stair.
Method: pass 128's composition (build_block127.py with pass 128's three edits) runs again in a private
namespace with this pass's single, asserted replacements; pass 127's cut after the castle now keeps
pass 124's portal and paving sections (as pass 126 composed them), and skips the passage and the well.
Re-created: SM_Kalmar_Slott, SM_Castle124_Portals, SM_Castle124_Paving.
Sources: references/block129-notes.md.
"""
B129D=json.loads((R/'source/block129.json').read_text());B128D=json.loads((R/'source/block128.json').read_text())
def rep129(src,old,new):
 assert src.count(old)==1,('source changed',src.count(old),old[:80]);return src.replace(old,new)
def drop_degenerate_faces129(obj,tol=1e-9):
 # Faces with no area, a repeated corner or a width under 0.1 mm have no UV frame for the export.
 import bmesh
 bm=bmesh.new();bm.from_mesh(obj.data)
 def _thin(f):
  L=max(e.calc_length() for e in f.edges);return L>0 and 2*f.calc_area()/L<1e-4
 bad=[f for f in bm.faces if f.calc_area()<tol or len({v.index for v in f.verts})<len(f.verts) or _thin(f)]
 if bad:bmesh.ops.delete(bm,geom=bad,context='FACES_ONLY')
 bm.to_mesh(obj.data);bm.free();obj.data.update();return len(bad)

# ================================================================= pass 128's composition of pass 127
_SRC128=(R/'scripts/build_block128.py').read_text()
NSC129=dict(globals())
exec(compile(_SRC128[_SRC128.index('def rep128(src,old,new):'):_SRC128.index('NS128=dict(globals())')],'build_block128.py:composition','exec'),NSC129)
SRC129=NSC129['SRC128']
# Marking: the re-created meshes are pass 129's.
SRC129=rep129(SRC129," obj['detail_pass']=128;obj['reference_notes']='references/block128-notes.md';obj['osm_way']=osm\n",
 " obj['detail_pass']=129;obj['reference_notes']='references/block129-notes.md';obj['osm_way']=osm\n")
SRC129=rep129(SRC129,"return mark127(obj,'27,124,126,127',osm)","return mark127(obj,'27,124,126,127,128' if obj.name=='SM_Kalmar_Slott' else '124,126',osm)")
# The outside stairs: pass 127's NE stair, SE_e's moved, portal D's new one.
SRC129=rep129(SRC129,"B127D['chimneys']=B128D['chimneys']   # pass 128\n","B127D['chimneys']=B128D['chimneys']   # pass 128\nB127D['stairs']=B129D['stairs']   # pass 129\n")
# Pass 27's helpers as pass 127 edits them: portal D's raised arched door counts as a door, the stair
# door of portal D is not a plain raised door, and the dormers are this pass's.
SRC129=rep129(SRC129," isdoor=lambda h:h[1]<ZC+.2 or h[4]<0\n"," isdoor=lambda h:h[1]<ZC+.2 or h[4]<0 or tuple(h) in ARCHUP129\n")
SRC129=rep129(SRC129,"for st in B127D['stairs'] if math.dist(st['p'],p)<.01","for st in B127D['stairs'] if st.get('door','plain')=='plain' and math.dist(st['p'],p)<.01")
SRC129=rep129(SRC129,"def dormers127(m):\n for d in B127D['dormers']:roof_dormer(m,d['x'],d['y'],0,d['a'],ZCE127,d['sli'],.9,.95,1.2,K['FrameRed'],K['Roof'],K['Frame'],True)\n",
 "def dormers127(m):dormers129(m)\n")
SRC129=rep129(SRC129,";exec(compile(EXTRA127,'build_block127.py:pass27_helpers','exec'),NS124);",";exec(compile(EXTRA127,'build_block127.py:pass27_helpers','exec'),NS124);exec(compile(EXTRA129,'build_block129.py:pass27_helpers','exec'),NS124);")
# The courtyard doors per edge, and the raised arched door drawn as a door.
SRC129=rep129(SRC129,'" doors=([(0.0,ZC,1.4,2.4,.7)] if L>12 else [])+raised127(p,q)"','" doors=doors129(p,q,L)+raised127(p,q)"')
SRC129=rep129(SRC129,'"  if r<0:raised_door127(m,x,y,u,b,w,h,a)\\n  elif b<z0+.2:arch_door27(m,x,y,u,b,w,h,r,a)"',
 '"  if (u,b,w,h,r) in ARCHUP129:arch_door27(m,x,y,u,b,w,h,r,a)\\n  elif r<0:raised_door127(m,x,y,u,b,w,h,a)\\n  elif b<z0+.2:arch_door27(m,x,y,u,b,w,h,r,a)"')
# Pass 127 stopped after the castle; this pass also runs pass 124's portals and paving (not the
# passage, not the well), with the gate passage's arch in the front at portal C's measured size.
SRC129=rep129(SRC129,"_end=\"print('BLOCK124_PASS27_REBUILT',NS124['castle27_names'])\\n\";assert _s.count(_end)==1;_s=_s[:_s.index(_end)+len(_end)]\n",
 "_end=\"print('BLOCK124_PASS27_REBUILT',NS124['castle27_names'])\\n\";assert _s.count(_end)==1;_s=cut129(_s,_end)\n"
 "_s=rep127(_s,\"gate=(CF124['u'],ZC,2.8,2.4,1.4)\",\"gate=(CF124['u'],ZC,PC129['open_w'],PC129['open_h'],PC129['open_r'])\")\n")
SRC129=rep129(SRC129,"assert block127_names==['SM_Kalmar_Slott'],block127_names","assert block127_names==['SM_Kalmar_Slott','SM_Castle124_Portals','SM_Castle124_Paving'],block127_names")

PC129=B129D['portal_c'];PD129=dict(B129D['portal_d'])
_std=[s for s in B129D['stairs'] if s.get('door')=='arch'][0];PD129['run']=_std['landing']+(_std['risers']-1)*_std['tread']
EXTRA129='''
ARCHUP129=[tuple(h) for h in B129D['archup']]
def doors129(p,q,L):
 # Pass 129's doors on the courtyard edges it measured; pass 27's rule (a middle door on edges over
 # 12 m) on the others.
 for k,hs in B129D['doors'].items():
  i,j=map(int,k.split(','))
  if math.dist(CI[i],p)<.01 and math.dist(CI[j],q)<.01:return [tuple(h) for h in hs]
 return [(0.0,ZC,1.4,2.4,.7)] if L>12 else []
def solid129(m,front,back,ma):
 # A closed prism between two matching convex rings, every face turned outwards.
 n=len(front);v=[tuple(p) for p in front]+[tuple(p) for p in back];c=[sum(p[i] for p in v)/len(v) for i in range(3)]
 out=[]
 for f in [tuple(range(n)),tuple(range(n,2*n))]+[(i,(i+1)%n,n+(i+1)%n,n+i) for i in range(n)]:
  pts=[v[i] for i in f];nx=ny=nz=0.0
  for a_,b_ in zip(pts,pts[1:]+pts[:1]):nx+=(a_[1]-b_[1])*(a_[2]+b_[2]);ny+=(a_[2]-b_[2])*(a_[0]+b_[0]);nz+=(a_[0]-b_[0])*(a_[1]+b_[1])
  fc=[sum(p[i] for p in pts)/len(pts) for i in range(3)]
  if nx*(fc[0]-c[0])+ny*(fc[1]-c[1])+nz*(fc[2]-c[2])<0:f=f[::-1]
  out.append(f)
 m.faces(v,out,ma)
def dormers129(m):
 # The courtyard dormers (Street View 2014, photographs 2017 and 2022): the red-fronted gabled dormer
 # on SE_e, the grey shed dormers on SW and NW and the louvred vent on NE. Each front stands on its
 # slope 'up' metres above the eaves line; the body runs back into the roof.
 for d in B129D['dormers']:
  F=(d['x'],d['y']);mv=d['m'];ev=(-mv[1],mv[0]);zf=d['z'];W=d['w'];hf=d['hf'];L=d['depth'];ang=math.atan2(-mv[0],mv[1])
  P=lambda a_,b_,z_:(F[0]+ev[0]*a_+mv[0]*b_,F[1]+ev[1]*a_+mv[1]*b_,z_)
  if d['kind']=='gable':
   gh=d['gh'];ring=[(-W/2,zf-.3),(W/2,zf-.3),(W/2,zf+hf),(0,zf+hf+gh),(-W/2,zf+hf)]
   solid129(m,[P(a_,0,z_) for a_,z_ in ring],[P(a_,L,z_) for a_,z_ in ring],K['Roof'])
   # the hood: a slab over each gable edge, 0.15 m proud of the front and the cheeks
   for s_ in (-1,1):
    a0,a1=s_*(W/2+.15),0.0;z0,z1=zf+hf-.15*gh/(W/2),zf+hf+gh+.06
    q=[P(a0,-.15,z0),P(a1,-.15,z1),P(a1,L,z1),P(a0,L,z0)];solid129(m,q,[(x_,y_,z_+.08) for x_,y_,z_ in q],K['Roof'])
   # the red-painted front with its arched window
   inset=[(-W/2+.06,zf+.02),(W/2-.06,zf+.02),(W/2-.06,zf+hf-.02),(0,zf+hf+gh-.12),(-W/2+.06,zf+hf-.02)]
   solid129(m,[P(a_,-.04,z_) for a_,z_ in inset],[P(a_,0,z_) for a_,z_ in inset],K['FrameRed'])
   ww,wh=d['win'];X,Y,_=P(0,-.04,0)
   town_window(m,X,Y,zf+.5+wh/2,ww,wh,ang,K['Frame'],True,2,2,False)
  else:
   sh=d['shed'];prof=[(0,zf-.3),(0,zf+hf),(L,zf+hf+sh*L),(L,zf+d['sli']*L-.3)]
   solid129(m,[P(-W/2,b_,z_) for b_,z_ in prof],[P(W/2,b_,z_) for b_,z_ in prof],K['Roof'])
   q=[P(-W/2-.08,-.1,zf+hf-.02),P(W/2+.08,-.1,zf+hf-.02),P(W/2+.08,L,zf+hf+sh*(L+.1)-.02),P(-W/2-.08,L,zf+hf+sh*(L+.1)-.02)]
   solid129(m,q,[(x_,y_,z_+.06) for x_,y_,z_ in q],K['Roof'])
   ww,wh=d['win'];zw=zf+hf/2+.05
   facade_box(m,F[0],F[1],0,.015,zw,ww,.03,wh,SIGN,ang)
   if d['id']=='NE_vent':
    for k in range(3):facade_box(m,F[0],F[1],0,.05,zw-wh/2+wh*(k+.5)/3,ww+.04,.04,.05,K['Roof'],ang)
'''
def cut129(_s,_end):
 # Pass 124's code after the castle (as pass 126 composed it): the portals and the paving run again
 # with this pass's edits; the passage and the well house are not re-created.
 i_p=_s.index('# ================================================================= portals B, C, D, E and F')
 i_w=_s.index('# ================================================================= the well house of 1578, hexagonal')
 i_v=_s.index('# ================================================================= paving')
 return _s[:_s.index(_end)+len(_end)]+edit_portals129(_s[i_p:i_w]+"WX124,WY124=CA124['well']\n"+_s[i_v:])
PORT129='''
def ent129(m,x,y,u,z0,z1,w,a,ma,d):
 # Architrave, frieze and cornice in the proportions 0.35 / 0.35 / 0.30; d is the projection.
 h=z1-z0;fb124(m,x,y,u,d,z0,z0+.35*h,w,ma,a);fb124(m,x,y,u,d-.06,z0+.35*h,z0+.7*h,w-.1,ma,a);fb124(m,x,y,u,d+.15,z0+.7*h,z1,w+.25,ma,a)
def portal_c129(m):
 # Portal C (pano 2 at 300 degrees, Street View 2014; Olsson 1957): two storeys of paired fluted
 # columns, 4.95 m wide and 6.69 m high; pedestals, the lower order, an entablature, the upper order
 # with the relief panel between the pairs, a flat cornice. The arch 2.6 m wide, its crown 3.25 m.
 x,y,L,a=sf_edge(W1_124,N124);u=UC124;zc=ZC124;P=PC129;p0,p1=P['pairs']
 for s in (-1,1):
  um=u+s*(p0+p1)/2;wp=p1-p0+.5
  fb124(m,x,y,um,.62,zc,zc+P['ped']-.1,wp,TR124,a);fb124(m,x,y,um,.68,zc+P['ped']-.1,zc+P['ped'],wp+.08,TR124,a)
  fb124(m,x,y,um,.5,zc+P['base2'][0],zc+P['base2'][1],wp,TR124,a)
  for du in (p0,p1):
   column124(m,x,y,u+s*du,O124+.33,zc+P['col1'][0],P['col1'][1]-P['col1'][0],P['r1'],a,TR124)
   column124(m,x,y,u+s*du,O124+.27,zc+P['col2'][0],P['col2'][1]-P['col2'][0],P['r2'],a,TR124,12)
 ent129(m,x,y,u,zc+P['ent1'][0],zc+P['ent1'][1],P['width'],a,TR124,.62)
 pw=2*(p0-P['r2']-.12)
 fb124(m,x,y,u,.2,zc+P['panel'][0],zc+P['panel'][1],pw,TR124,a)
 fb124(m,x,y,u,.08,zc+P['panel'][0]+.18,zc+P['panel'][1]-.18,pw-.36,M124['Tablet'],a,O124+.2)
 fb124(m,x,y,u,.06,zc+P['panel'][0]+.5,zc+P['panel'][1]-.45,.9,M124['Tablet'],a,O124+.28)
 ent129(m,x,y,u,zc+P['ent2'][0],zc+P['ent2'][1],P['width'],a,TR124,.5)
 for s in (-1,1):fb124(m,x,y,u+s*(P['open_w']/2+.15),.2,zc,zc+P['open_h'],.3,TR124,a)
 p18_arch(m,*lp(x,y,u,0,0,a)[:2],zc+P['open_h'],P['open_w'],P['open_r'],.22,O124+.04,a,TR124)
def portal_d129(m,x,y,u,z,a):
 # Portal D, Drottningtrappan (panos 1 and 2, Street View 2014): banded Doric columns on pedestals,
 # an entablature and a segmental cap, 2.66 m wide and 4.13 m high on its stair's landing.
 P=PD129
 for s in (-1,1):
  uu=u+s*P['cols']
  fb124(m,x,y,uu,.55,z+P['ped'][0],z+P['ped'][1],.5,TR124,a)
  column124(m,x,y,uu,O124+.28,z+P['col'][0],P['col'][1]-P['col'][0],.16,a,TR124)
  for k in range(int((P['col'][1]-P['col'][0]-.3)/.36)):fb124(m,x,y,uu,.5,z+P['col'][0]+.2+k*.36,z+P['col'][0]+.36+k*.36,.44,TR124,a,O124+.03)
 ent129(m,x,y,u,z+P['ent'][0],z+P['ent'][1],P['width'],a,TR124,.55)
 c0,c1=P['cap'];cw=P['cap_w']/2;zb=z+c0+.12;hh=c1-c0-.12;Rr=(cw*cw+hh*hh)/(2*hh);th=math.asin(cw/Rr);zo=zb+hh-Rr
 fb124(m,x,y,u,.42,z+c0,zb,P['cap_w']+.1,TR124,a)
 fan_prism124(m,(u,zb),[(u+Rr*math.sin(th-2*th*k/10),zo+Rr*math.cos(th-2*th*k/10)) for k in range(11)],O124,O124+.4,x,y,a,TR124)
'''
def edit_portals129(t):
 # Portal C is rebuilt; portal D moves to its door on CI7-CI6 and stands on the landing.
 i0=t.index("# Portal C, the west courtyard portal");i1=t.index("p18_arch(m,*lp(x,y,u,0,0,a)[:2],zc+2.4,2.8,1.4,.3,O124+.04,a,TR124)\n")+len("p18_arch(m,*lp(x,y,u,0,0,a)[:2],zc+2.4,2.8,1.4,.3,O124+.04,a,TR124)\n")
 assert t.count("# Portal C, the west courtyard portal")==1 and t[i0:i1].count('\n')==16,t[i0:i1].count('\n')
 t=t[:i0]+PORT129+'portal_c129(m)   # pass 129\n'+t[i1:]
 t=rep129(t,"_doors={'D':(N124,CI124[7]),","_doors={'D':(CI124[7],CI124[6]),")
 t=rep129(t," x,y,L,a=sf_edge(p,q);u=0.0;z=ZC124\n"," x,y,L,a=sf_edge(p,q);u,z=(PD129['u'],ZC124+PD129['rise']) if key=='D' else (0.0,ZC124)\n")
 i0=t.index(" if key=='D':\n");i1=t.index(" elif key=='E':\n");assert t[i0:i1].count('\n')==6,t[i0:i1]
 t=t[:i0]+" if key=='D':portal_d129(m,x,y,u,z,a)\n"+t[i1:]
 t=rep129(t,"for key,(p,q) in _doors.items():x,y,L,a=sf_edge(p,q);_targets.append(lp(x,y,0,.355+.9,0,a)[:2])",
  "for key,(p,q) in _doors.items():x,y,L,a=sf_edge(p,q);_targets.append(lp(x,y,PD129['u'] if key=='D' else 0,.355+(PD129['run']+.6 if key=='D' else .9),0,a)[:2])")
 return t
NS129=dict(globals());NS129.update(B129D=B129D,EXTRA129=EXTRA129,PORT129=PORT129,PC129=PC129,PD129=PD129,cut129=cut129,edit_portals129=edit_portals129,rep129=rep129)
exec(compile(SRC129,'build_block127.py (pass 128+129 edits)','exec'),NS129)
block129_names=['SM_Kalmar_Slott','SM_Castle124_Portals','SM_Castle124_Paving']
assert NS129['block127_names']==block129_names,NS129['block127_names']
for _n in block129_names:
 _o=bpy.data.objects[_n];_o['block129_dropped_faces']=drop_degenerate_faces129(_o)
 assert _o['detail_pass']==129,(_n,_o['detail_pass'])
 print('BLOCK129_MESH',_n,_o['corrects_pass'],'dropped',_o['block129_dropped_faces'],len(_o.data.polygons))
bpy.data.objects['SM_Kalmar_Slott']['block129_dormers']=len(B129D['dormers'])

# ================================================================= cameras
def sv_camera129(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
_ZC129=B129D['zc'];_c690=B129D['camera690']
block129_cameras=[
 # 690 (re-created): the 2022 well photograph (-wuppertaler), resected anew. It looks at the east corner:
 # NE with portal D on the left, SE_e with its stair and the red dormer on the right, the east tower's
 # cap at the upper left (pass 127 took it for the north corner). Portrait, f 1925 px.
 sv_camera129('690_Block127_Cal_Well2022',_c690['x'],_c690['y'],_ZC129+_c690['h'],_c690['heading'],_c690['pitch'],_c690['vfov']),
 # 700-703: Street View 2014 courtyard views at pass 128's resected pano cameras (heading offset applied):
 # pano 1 (zCIfieeXGQUNANmWu_Tg9A) at NE square on (URL 40h, 92t, 60y) and at SE_w (140h, 98t, 60y);
 # pano 2 (jOXzkLldNOjrveyz1T81wg) at portal C on NW (300h, 108t, 75y) and at SE_e (150h, 100t, 75y).
 sv_camera129('700_Block129_Cal_Pano1_NE',-885.06,-306.46,_ZC129+2.1,38.66,2,60),
 sv_camera129('701_Block129_Cal_Pano1_SEw',-885.06,-306.46,_ZC129+2.1,138.66,8,60),
 sv_camera129('702_Block129_Cal_Pano2_PortalC',-860.06,-308.67,_ZC129+1.9,297.35,18,75),
 sv_camera129('703_Block129_Cal_Pano2_SEe',-860.06,-308.67,_ZC129+1.9,147.35,10,75),
 ('704_Block129_Aerial_Dormers',(-815.0,-372.0,62.0),(-868.0,-308.0,14.0),26),
]
print('BLOCK129_GEOMETRY',len(block129_names))
