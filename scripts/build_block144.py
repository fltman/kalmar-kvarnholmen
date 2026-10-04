"""Pass 144: Klapphuset (OSM 93199604) re-created red, with a narrower pier with railings and no east
deck (corrects pass 122 on SM_Kvarnholmen_House_93199604).

Pass 122 built Klapphuset from the satellite: falu red walls, but a mid-grey metal roof (RoofGrey),
a pale weathered pier 2.2 m wide and a 1.6 m deck on the east end (Timber, a grey-beige on
TownPaintWhite), white corner boards and a white eaves board. Seen from the bastion or from above,
the grey roof, the pale pier and deck and the white trim make up most of the house, and it reads
white. Openly licensed photographs (Wikimedia Commons 2015, 2024) and two Google user photospheres
(2021, viewed only, one resected) show the house as built:
- falu red lap boarding all round with red corner boards; white only on the window frames;
- a black standing-seam hip roof (low pitch, dark fascia) with two dark ventilators;
- window pairs high under the eaves: three on the south front, four and a small window on the north
  front, two on each end (the west end is assumed like the east);
- the green glazed double door in a shallow bay with its own small hip canopy;
- pale grey vertical skirting boards from the floor to the water;
- a timber pier from the door to the shore: deck 1.9 m, railings on posts outside the deck,
  2.2 m over the handrails (resected at the house end), on piles; no deck on the east end.

This is a clean dedicated rebuild of the one house: pass 122's code builds all its houses in shared
loops, so re-running it for one zone would need many replacements. Nothing of pass 122 is re-run;
the mesh is removed and re-created here from source/block144.json (scripts/prepare_block144.py) with
this pass's own materials (M_Block144_*), so it does not depend on pass 122's materials.
Sources: references/block144-notes.md.
"""
import json,math
B144D=json.loads((R/'source/block144.json').read_text())
block144_names=[];M144={}
def _mats144():
 for old in [k for k in list(materials) if k.startswith('M_Block144_')]:bpy.data.materials.remove(materials.pop(old))
 for key,(texture,target) in B144D['materials'].items():
  rough,metal={'Roof':(.55,.30),'Vent':(.60,.25),'Frame':(.55,0),'DoorGreen':(.60,0)}.get(key,(.88,0))
  name='M_Block144_'+key;M144[key]=name;col=lin(tuple(target));tint=[round(c/m,4) for c,m in zip(col,lin(MEAN[texture]))]
  mat(name,col,rough,metal,texture);specs[name]['street16_tint']=tint;specs[name]['block144_target_srgb']=list(target)
  ma=materials[name];nodes=ma.node_tree.nodes;links=ma.node_tree.links;bsdf=nodes.get('Principled BSDF');src=bsdf.inputs['Base Color'].links[0].from_socket
  mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);links.new(src,mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
  for node in nodes:
   if node.bl_idname=='ShaderNodeTexImage' and node.image:
    twin=next((im for im in bpy.data.images if im!=node.image and im.filepath==node.image.filepath),None)
    if twin:loaded=node.image;node.image=twin;bpy.data.images.remove(loaded)
_mats144()
RED144,WHITE144,GREEN144,ROOF144=M144['Falu'],M144['Frame'],M144['DoorGreen'],M144['Roof']

def b144_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 if name not in block144_names:block144_names.append(name)
 return Mesh(name,category)
def drop_degenerate_faces144(obj,tol=1e-9):
 # Faces with no area, a repeated corner or a width under 0.1 mm have no UV frame for the export.
 import bmesh
 bm=bmesh.new();bm.from_mesh(obj.data)
 def _thin(f):
  L=max(e.calc_length() for e in f.edges);return L>0 and 2*f.calc_area()/L<1e-4
 bad=[f for f in bm.faces if f.calc_area()<tol or len({v.index for v in f.verts})<len(f.verts) or _thin(f)]
 if bad:bmesh.ops.delete(bm,geom=bad,context='FACES_ONLY')
 bm.to_mesh(obj.data);bm.free();obj.data.update();return len(bad)
def b144_finish(m):
 obj=s21_finish(m);obj['block144_dropped_faces']=drop_degenerate_faces144(obj);print('BLOCK144_DROPPED',m.name,obj['block144_dropped_faces'],len(obj.data.polygons))
 obj['detail_pass']=144;obj['corrects_pass']=122;obj['reference_notes']='references/block144-notes.md';obj['osm_way']=B144D['osm']
 obj['block144_pier_deck']=B144D['pier']['deck'];obj['block144_pier_over_rails']=B144D['pier']['over_rails'];return obj

# ---------------------------------------------------------------- helpers (wall frame: u along p->q from the middle, out from the OSM line)
def laps144(m,x,y,L,a,z0,z1,holes,ma,o=.37,step=.15,ext=0.0):
 # horizontal lap boarding: one shadow strip per board, broken at the openings (holes: u,b,w,h,r)
 for k in range(1,int((z1-z0)/step)):
  zz=z0+k*step;segs=[(-L/2+.05,L/2-.05+ext)]
  for hu,hb,hw,hh,hr in holes:
   if hb-.16<zz<hb+hh+.16:segs=[(l0,h0) for l,h_ in segs for l0,h0 in ((l,min(h_,hu-hw/2-.14)),(max(l,hu+hw/2+.14),h_)) if h0-l0>.05]
  for l0,h0 in segs:facade_box(m,x,y,(l0+h0)/2,o,zz,h0-l0,.03,.03,ma,a)
def light144(m,x,y,u,b,w,h,a,cols,rows):
 # one casement: glass set back, white frame, glazing bars
 facade_box(m,x,y,u,.20,b+h/2,w,.02,h,GLAZE,a)
 for q in (-w/2+.03,w/2-.03):facade_box(m,x,y,u+q,.24,b+h/2,.06,.06,h,WHITE144,a)
 for zz in (b+.03,b+h-.03):facade_box(m,x,y,u,.24,zz,w,.06,.06,WHITE144,a)
 for c in range(1,cols):facade_box(m,x,y,u-w/2+c*w/cols,.24,b+h/2,.03,.04,h-.06,WHITE144,a)
 for r in range(1,rows):facade_box(m,x,y,u,.24,b+r*h/rows,w-.06,.04,.03,WHITE144,a)
def window144(m,x,y,u,b,w,h,a,n):
 # n casements side by side in one white surround, with a post between them and a sill
 post=.10;lw=(w-(n-1)*post)/n
 for i in range(n):light144(m,x,y,u-w/2+lw/2+i*(lw+post),b,lw,h,a,3 if lw>1.0 else 2,2)
 for i in range(1,n):facade_box(m,x,y,u-w/2+i*(lw+post)-post/2,.24,b+h/2,post,.10,h,WHITE144,a)
 surround36(m,x,y,u,b,w,h,a,WHITE144,.09,.38)
 facade_box(m,x,y,u,.43,b-.05,w+.22,.14,.05,WHITE144,a)
H144=B144D['heights']['eaves'];FL144=B144D['heights']['floor'];SK144=B144D['heights']['skirt_bottom']
WB144=B144D['heights']['window_bottom'];WH144=B144D['heights']['window_h']

def _build144():
 # ---------------------------------------------------------------- the house
 m=b144_new(B144D['mesh'],'Kvarnholmen/Courtyards')
 for key in ('south','east','north','west'):
  w=B144D['walls'][key];p,q=tuple(w['p']),tuple(w['q']);x,y,L,a=sf_edge(p,q)
  holes=[];wins=[]
  for kind,s,wd in w['openings']:
   u=s-L/2
   if kind=='door':continue                      # the door stands in the bay in front of the wall
   hb=WB144;hh=WH144;holes.append((u,hb,wd,hh,0));wins.append((u,hb,wd,hh,2 if kind=='pair' else 1))
  bz_wall(m,p,q,FL144,H144,holes,RED144)
  laps144(m,x,y,L,a,FL144+.02,H144-.05,holes,RED144,ext=.36)
  for u,hb,wd,hh,n in wins:window144(m,x,y,u,hb,wd,hh,a,n)
  # the corner square at q (walls stand outside the outline), red corner boards on both faces
  facade_box(m,x,y,L/2+.18,.18,(FL144+H144)/2,.36,.35,H144-FL144,RED144,a)
  facade_box(m,x,y,L/2+.29,.39,(FL144+H144)/2,.14,.05,H144-FL144,RED144,a)
  facade_box(m,x,y,-L/2+.07,.39,(FL144+H144)/2,.14,.05,H144-FL144,RED144,a)
  # the skirting: pale grey vertical boards from the floor down into the water, round the corner square
  facade_box(m,x,y,.18,.18,(SK144+FL144)/2,L+.36,.35,FL144-SK144,M144['Skirt'],a)
  nb=int((L+.36)/.12)
  for k in range(1,nb):facade_box(m,x,y,-L/2+k*(L+.36)/nb,.365,(SK144+FL144)/2-.02,.03,.03,FL144-SK144-.08,M144['Skirt'],a)
  facade_box(m,x,y,.18,.38,FL144-.03,L+.40,.07,.08,RED144,a)        # drip board between boarding and skirting

 # the entrance bay on the south front, with the green glazed double door, and its little hip canopy
 Bb=B144D['bay'];sw=B144D['walls']['south'];p,q=tuple(sw['p']),tuple(sw['q']);x,y,L,a=sf_edge(p,q);ub=Bb['s']-L/2
 d144=((q[0]-p[0])/L,(q[1]-p[1])/L);bp=(p[0]+d144[0]*(Bb['s']-Bb['width']/2),p[1]+d144[1]*(Bb['s']-Bb['width']/2));bq=(p[0]+d144[0]*(Bb['s']+Bb['width']/2),p[1]+d144[1]*(Bb['s']+Bb['width']/2))
 bx,by,bL,_=sf_edge(bp,bq);o1=.355+Bb['depth'];DW,DH=1.80,B144D['heights']['door_h']
 bz_wall(m,bp,bq,FL144,Bb['canopy_eaves']-.02,[(0,FL144,DW,DH,0)],RED144,.355,o1)
 laps144(m,bx,by,bL,a,FL144+.02,Bb['canopy_eaves']-.06,[(0,FL144,DW,DH,0)],RED144,o=o1+.015)
 for s_ in (-1,1):
  facade_box(m,bx,by,s_*(bL/2-.07),o1+.03,(FL144+Bb['canopy_eaves'])/2,.14,.05,Bb['canopy_eaves']-FL144,RED144,a)
  facade_box(m,bx,by,s_*(DW/2+.05),o1+.03,DH/2,.10,.06,DH+.10,GREEN144,a)           # green door frame
 facade_box(m,bx,by,0,o1+.03,DH+.05,DW+.20,.06,.10,GREEN144,a)
 facade_box(m,bx,by,0,o1-.06,DH/2,DW,.06,DH,GREEN144,a)                              # the two leaves
 facade_box(m,bx,by,0,o1-.02,DH/2,.04,.04,DH,GREEN144,a)
 for s_ in (-1,1):
  cu=s_*DW/4;gw=DW/2-.24;gb=DH*.48;gh=DH*.44
  facade_box(m,bx,by,cu,o1-.025,gb+gh/2,gw,.02,gh,GLAZE,a)
  for c in range(1,2):facade_box(m,bx,by,cu,o1-.01,gb+gh/2,.03,.03,gh,GREEN144,a)
  for r in range(1,4):facade_box(m,bx,by,cu,o1-.01,gb+r*gh/4,gw,.03,.03,GREEN144,a)
  facade_box(m,bx,by,cu,o1-.01,DH*.22,gw,.03,DH*.30,GREEN144,a)                   # lower panel
 # canopy: front eaves at canopy_out from the outline, back ridge poking out of the main roof
 cw=Bb['canopy_width']/2;co_=Bb['canopy_out'];ce=Bb['canopy_eaves'];ct=Bb['canopy_top']
 # the main roof's height over the outline (t=0): eaves 3.10 at the overhang, rising to the ridge
 Bh_=math.dist(*[tuple(v) for v in B144D['rect'][1:3]])/2;ov_=B144D['roof']['overhang'];zm=3.10+ov_*(B144D['heights']['ridge']+.05-3.10)/(Bh_+ov_-.15)
 F0,F1=lp(bx,by,-cw,co_,ce,a),lp(bx,by,cw,co_,ce,a);K0,K1=lp(bx,by,-.6,0,ct,a),lp(bx,by,.6,0,ct,a);S0,S1=lp(bx,by,-cw,0,zm,a),lp(bx,by,cw,0,zm,a)
 m.faces([K0,K1,lp(bx,by,.6,0,zm-.05,a),lp(bx,by,-.6,0,zm-.05,a)],[(0,1,2,3),(3,2,1,0)],ROOF144)
 m.faces([F0,F1,K1,K0],[(0,1,2,3),(3,2,1,0)],ROOF144)
 m.faces([F0,K0,S0],[(0,1,2),(2,1,0)],ROOF144);m.faces([F1,S1,K1],[(0,1,2),(2,1,0)],ROOF144)
 facade_box(m,bx,by,0,co_,ce-.08,2*cw,.05,.16,ROOF144,a)
 m.faces([lp(bx,by,-cw,co_,ce-.16,a),lp(bx,by,cw,co_,ce-.16,a),lp(bx,by,cw,o1,ce-.16,a),lp(bx,by,-cw,o1,ce-.16,a)],[(0,1,2,3),(3,2,1,0)],ROOF144)

 # ---------------------------------------------------------------- the hip roof: black standing seam, dark fascia and soffit
 Rf=B144D['roof'];SW_,SE_,NE_,NW_=[tuple(v) for v in B144D['rect']]
 cx=sum(v[0] for v in B144D['rect'])/4;cy=sum(v[1] for v in B144D['rect'])/4
 A_=math.dist(SW_,SE_)/2;Bh=math.dist(SE_,NE_)/2;dd=((SE_[0]-SW_[0])/(2*A_),(SE_[1]-SW_[1])/(2*A_));nn=(dd[1],-dd[0])
 def P144(s,t,z):return (cx+dd[0]*s+nn[0]*t,cy+dd[1]*s+nn[1]*t,z)
 ov=Rf['overhang'];ZE=3.10;ZF=2.93;ZR=B144D['heights']['ridge']+.05;ri=.15
 outer=[P144(-(A_+ov),Bh+ov,ZE),P144(A_+ov,Bh+ov,ZE),P144(A_+ov,-(Bh+ov),ZE),P144(-(A_+ov),-(Bh+ov),ZE)]
 inner=[P144(-(A_-Bh+ri),ri,ZR),P144(A_-Bh+ri,ri,ZR),P144(A_-Bh+ri,-ri,ZR),P144(-(A_-Bh+ri),-ri,ZR)]
 fasc=[(v[0],v[1],ZF) for v in outer];wallf=[P144(sg*(A_+.355),tg*(Bh+.355),ZF) for sg,tg in ((-1,1),(1,1),(1,-1),(-1,-1))]
 # The roof is one closed solid (the slopes and flat top over a base at the eaves), and the fascia and
 # soffit one closed ring, so Mesh.finish's normal recalculation turns every face outward.
 m.faces(outer+inner,[(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7),(3,2,1,0)],ROOF144)
 wtop=[(v[0],v[1],ZE-.01) for v in wallf]
 ring=[(v[0],v[1],ZE-.01) for v in outer]+fasc+wallf+wtop;rf=[]
 for i in range(4):
  j=(i+1)%4;rf+=[(i,j,4+j,4+i),(4+i,4+j,8+j,8+i),(8+i,8+j,12+j,12+i),(12+i,12+j,j,i)]
 m.faces(ring,rf,ROOF144)
 for i in range(4):
  j=(i+1)%4;town_rod(m,outer[i],outer[j],.035,ROOF144,6)
 # standing seams on the four slopes, about 0.55 m apart, from the eaves to the ridge or hip line
 sl=(ZR-ZE)/(Bh+ov-ri)
 for side in (1,-1):
  k=int(2*(A_+ov)/.55)
  for i in range(1,k):
   s=-(A_+ov)+i*2*(A_+ov)/k
   t1=max(ri,min(Bh+ov,abs(s)-(A_-Bh))) if abs(s)>A_-Bh+ri else ri
   if Bh+ov-t1<.25:continue
   a0=P144(s,side*(Bh+ov),ZE+.02);a1=P144(s,side*t1,ZE+(Bh+ov-t1)*sl+.02);town_rod(m,a0,a1,.018,ROOF144,4)
 # ventilators on the ridge
 ang=math.atan2(dd[1],dd[0])
 for s in Rf['ventilators']:
  X,Y,_=P144(s,0,0);m.box((X,Y,ZR+.23),(.80,.62,.46),M144['Vent'],ang);m.box((X,Y,ZR+.50),(1.02,.82,.08),ROOF144,ang)
  m.faces([P144(s-.51,-.41,ZR+.54),P144(s+.51,-.41,ZR+.54),P144(s+.51,.41,ZR+.54),P144(s-.51,.41,ZR+.54),P144(s,0,ZR+.80)],[(0,1,4),(1,2,4),(2,3,4),(3,0,4)],ROOF144)
  for zz in (ZR+.12,ZR+.24,ZR+.36):
   for o in (-1,1):m.box((X+nn[0]*o*.315,Y+nn[1]*o*.315,zz),(.70,.02,.04),ROOF144,ang)

 # ---------------------------------------------------------------- the pier: deck, stringers, piles, railings on posts
 Pr=B144D['pier'];O=Pr['axis_origin'];N_=Pr['axis_dir'];W_=Pr['deck'];RU=Pr['over_rails']/2-.07
 P0=(O[0]+N_[0]*Pr['start_out'],O[1]+N_[1]*Pr['start_out']);P1=(O[0]+N_[0]*Pr['end_along'],O[1]+N_[1]*Pr['end_along'])
 x,y,L,a=sf_edge(P0,P1);tim=M144['Timber'];dark=M144['TimberDark'];T0=Pr['top']
 facade_box(m,x,y,0,0,T0-.06,L,W_,.12,tim,a)
 for k in range(1,int(L/.16)):facade_box(m,x,y,-L/2+k*L/int(L/.16),0,T0+.002,.02,W_-.02,.01,dark,a)
 for side in (-1,1):
  facade_box(m,x,y,0,side*(W_/2-.10),T0-.23,L,.14,.22,dark,a)
  n=max(2,round(L/2.5))
  for k in range(n+1):
   u=-L/2+.15+k*(L-.3)/n;town_rod(m,lp(x,y,u,side*(W_/2-.10),-2.3,a),lp(x,y,u,side*(W_/2-.10),T0-.33,a),.11,dark,8)
  # posts fixed to the deck edge, a handrail board on top and a knee rail
  n=max(2,round(L/1.65))
  for k in range(n+1):
   u=-L/2+.05+k*(L-.1)/n;facade_box(m,x,y,u,side*(W_/2+.05),T0+.48,.09,.09,1.08,tim,a)
  facade_box(m,x,y,0,side*RU,T0+1.045,L,.14,.05,tim,a)
  facade_box(m,x,y,0,side*(W_/2+.115),T0+.50,L,.04,.10,tim,a)
 b144_finish(m)
_build144()

def sv_camera144(name,x,y,h,heading,pitch,vfov=90,match='height'):
 b=math.radians(heading+28.2);t=(x+30*math.sin(b),y+30*math.cos(b),h+30*math.tan(math.radians(pitch)))
 lens=(9.667 if match=='width' else 11.25)/math.tan(math.radians(vfov/2))
 return (name,(round(x,2),round(y,2),round(h,2)),tuple(round(v,2) for v in t),round(lens,2))
block144_cameras=[
 sv_camera144('805_Block144_Cal_ShorePano',426.57,98.14,1.70,15.0,2.0,90),
 sv_camera144('806_Block144_Cal_NorthWater',448.0,182.0,2.0,164.0,0.0,18),
 ('807_Block144_Aerial',(470.0,90.0,30.0),(436.2,127.1,1.0),35)]
print('BLOCK144_GEOMETRY',len(block144_names))
