"""Refine every remaining generic house; measured footprints, estimated unidentified elevations.
Five identified street houses have explicit photographic profiles. No random invented ornaments.
"""
D17=json.loads((R/'source/district17.json').read_text());district17_names=[];district17_audit={};district17_cameras=[]
exec(compile((R/'scripts/materials_district17.py').read_text(),'materials_district17.py','exec'))
BROWN=town_mats['PaintBrown'];METAL=town_mats['MetalGrey'];GLAZE=town_mats['Glass'];SC={k:'M_Sodra_'+k for k in ['Cream','Sand','RedWood','OchreWood','DarkTile']}
for filename in ['build_larmtorget_facades.py','build_sodra_facades.py']:
 tree=ast.parse((R/'scripts'/filename).read_text());tree.body=[n for n in tree.body if isinstance(n,ast.FunctionDef)];exec(compile(tree,filename,'exec'))
# Shape-specific visual measurements, not survey dimensions.
observed={
 '93238156':dict(style='jugend',H=10.4,levels=3,colour='Yellow',paint='RedJoinery',bays=4,street='Norra Långgatan',roof='MetalRed',ref='norra-langgatan-84-i-kalmar'),
 '90859847':dict(style='renaissance',H=7.9,levels=2,colour='Grey',paint='RedJoinery',bays=9,street='Fiskaregatan',roof='MetalRed',ref='fiskargatan-3-i-kalmar'),
 '91926329':dict(style='mansard_timber',H=6.15,levels=2,colour='SageWood',paint='PaintGreen',bays=5,street='Norra Långgatan',roof='MetalRed',ref='fastigheten-bokbindaren-10-i-korsningen-proviantgatan-norra-langgatan-i-kalmar'),
 '92379265':dict(style='timber_shop',H=6.8,levels=2,colour='OchreWood',paint='PaintGreen',bays=10,street='Fiskaregatan',roof='TileRed',ref='gesallen-23-i-korsningen-fiskargatan-kaggensgatan-i-kalmar'),
 '92412873':dict(style='wahlberg',H=7.65,levels=2,colour='Grey',paint='PaintGreen',bays=9,street='Ölandsgatan',roof='MetalRed',ref='olandsgatan-27'),
}
def d17_box(m,x,y,u,o,z,w,d,h,ma,a):
 if w>.001 and h>.001:facade_box(m,x,y,u,o,z,w,d,h,ma,a)
def d17_spans(lo,hi,holes,u,margin=0):
 spans=[(lo,hi)]
 for c,z,w,h,kind in holes:
  if abs(u-c)<=w/2+margin:
   spans=[(p,q) for l,r in spans for p,q in [(l,min(r,z-margin)),(max(l,z+h+margin),r)] if q>p+.004]
 return spans
def d17_wall(m,x,y,L,a,lo,hi,holes,wall):
 facade_box(m,x,y,0,-.19,(lo+hi)/2,L,.24,hi-lo,wall,a)
 cuts=sorted(set([-L/2,L/2]+[v for u,z,w,h,k in holes for v in [max(-L/2,u-w/2),min(L/2,u+w/2)]]))
 for l,r in zip(cuts,cuts[1:]):
  for bottom,top in d17_spans(lo,hi,holes,(l+r)/2):facade_box(m,x,y,(l+r)/2,.24,(bottom+top)/2,r-l,.22,top-bottom,wall,a)
def d17_window(m,x,y,u,z,w,h,a,frame,trim,style='cross',front=True):
 sf_modern(m,x,y,u,z,w,h,a,frame,trim,1,2 if w<2 else 3)
 if style=='cross':facade_box(m,x,y,u,.197,z+h*.73,w,.08,.045,frame,a)
 elif style=='six':
  for f in [1/3,2/3]:facade_box(m,x,y,u,.197,z+h*f,w,.08,.026,frame,a)
 # Stepped moulding and a sloping sheet-metal sill with a folded drip edge.
 if front:
  for off in [-w/2-.09,w/2+.09]:facade_box(m,x,y,u+off,.395,z+h/2,.037,.042,h+.18,trim,a)
  facade_box(m,x,y,u,.400,z+h+.105,w+.29,.10,.037,trim,a)
 vs=[lp(x,y,u+dx,o,zz,a) for dx,o,zz in [(-w/2-.14,.22,z-.015),(w/2+.14,.22,z-.015),(w/2+.14,.51,z-.055),(-w/2-.14,.51,z-.055)]]
 m.faces(vs,[(0,1,2,3)],METAL);facade_box(m,x,y,u,.51,z-.075,w+.28,.025,.045,METAL,a)
 if front:
  for side in [-1,1]:
   for zz in [z+.22,z+h-.22]:facade_box(m,x,y,u+side*(w/2-.038),.248,zz,.016,.021,.058,METAL,a)
  facade_box(m,x,y,u+.085,.254,z+h*.42,.013,.019,.065,METAL,a)
def d17_arch_window(m,x,y,u,z,w,h,a,frame,trim,wall):
 r=w/2;spring=z+h-r;xx,yy,_=lp(x,y,u,0,0,a)
 town_window(m,xx,yy,z+(h-r)/2,w,h-r,a,frame,True,1,2,False)
 for side in [-1,1]:
  outline=[(side*r,spring+r),(0,spring+r)]+[(side*r*math.cos(t*math.pi/40),spring+r*math.sin(t*math.pi/40)) for t in range(20,-1,-1)]
  # Fill the rectangular opening outside the semicircular head.
  vs=[lp(xx,yy,v,o,zz,a) for o in [.13,.35] for v,zz in outline];n=len(outline)
  m.faces(vs,[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],wall)
 town_arch_band(m,xx,yy,spring,r,.105,a,trim,.40)
 for side in [-1,1]:facade_box(m,xx,yy,side*(r+.07),.38,z+(h-r)/2,.10,.08,h-r,trim,a)
 facade_box(m,xx,yy,0,.41,z-.065,w+.30,.27,.065,METAL,a)

def d17_band(m,x,y,L,a,z,holes,ma,depth=.07,height=.07):
 cuts=sorted(set([-L/2,L/2]+[v for u,b,w,h,k in holes if b-height/2<z<b+h+height/2 for v in [max(-L/2,u-w/2-.025),min(L/2,u+w/2+.025)]]))
 for l,r in zip(cuts,cuts[1:]):
  if not any(b-height/2<z<b+h+height/2 and abs((l+r)/2-u)<w/2+.025 for u,b,w,h,k in holes):facade_box(m,x,y,(l+r)/2,.355+depth/2,z,r-l,depth,height,ma,a)
def d17_gutter(m,x,y,u,L,H,a):
 vs=[];n=8
 for end in [-L/2,L/2]:
  for i in range(n+1):
   t=math.pi+i*math.pi/n;vs.append(lp(x,y,u+end,.42+.075*math.cos(t),H+.03+.075*math.sin(t),a))
 m.faces(vs,[(j,j+1,n+j+2,n+j+1) for j in range(n)],METAL,True)
 for p in [-L/2,L/2]:town_rod(m,lp(x,y,u+p,.345,H+.03,a),lp(x,y,u+p,.495,H+.03,a),.012,METAL)
 for j in range(max(1,round(L/1.2))):
  at=u-L/2+(j+.5)*L/max(1,round(L/1.2));facade_box(m,x,y,at,.38,H-.06,.035,.13,.04,METAL,a)
def d17_roof(m,record,oldroof,obs,primary):
 H=record['H'];roof=town_mats.get(record['roof'],TT);simple=record.get('roof_rectangle')
 if obs and record.get('authored_roof_faces'):
  for vs in record['authored_roof_faces']:
   normal=(Vector(vs[1])-Vector(vs[0])).cross(Vector(vs[2])-Vector(vs[0]))
   ma=D17MAT.get(record['colour'],D17MAT['Ivory']) if abs(normal.z)<normal.length*.05 else roof
   m.faces(vs,[tuple(range(len(vs)))],ma)
  for P,Q in record.get('authored_roof_seams',[]):town_rod(m,P,Q,.012,roof,6)
  return 'photo-informed ridge/mansard clipped to mapped courtyard'
 if simple and record['roof']!='flat' and record['style']!='service':
  x,y,L,W,a=simple;rise=min(3.7,W*.48);h=rise
  # A closed coherent ridge replaces triangulated mound roofs on rectangular footprints only.
  cuts=[(-W/2,0),(0,h),(W/2,0)]
  if obs and obs['style']=='mansard_timber':cuts=[(-W/2,0),(-W*.29,h*.72),(0,h),(W*.29,h*.72),(W/2,0)]
  for (v,z),(vv,zz) in zip(cuts,cuts[1:]):
   m.faces([lp(x,y,u,-v,H+z,a) for u in [-L/2,L/2]]+[lp(x,y,u,-vv,H+zz,a) for u in [L/2,-L/2]],[(0,1,2,3)],roof)
  for u in [-L/2,L/2]:m.faces([lp(x,y,u,-v,H+z,a) for v,z in cuts],[tuple(range(len(cuts)))],D17MAT.get(record['colour'],D17MAT['Ivory']))
  town_rod(m,lp(x,y,-L/2,0,H+h+.025,a),lp(x,y,L/2,0,H+h+.025,a),.065,roof)
  if L>8:
   xx,yy,_=lp(x,y,-L*.22,0,0,a);m.box((xx,yy,H+h+.45),(.55,.65,.92),D17MAT.get(record['colour'],D17MAT['Ivory']),a);m.box((xx,yy,H+h+.94),(.70,.8,.12),METAL,a)
  if roof in [town_mats['MetalRed'],METAL]:
   for i in range(1,int(L/.65)):
    u=-L/2+i*.65
    for (v,z),(vv,zz) in zip(cuts,cuts[1:]):town_rod(m,lp(x,y,u,-v,H+z+.025,a),lp(x,y,u,-vv,H+zz+.025,a),.012,roof,6)
  return 'coherent ridge following rectangular footprint'
 for verts,ma in oldroof:m.faces(verts,[tuple(range(len(verts)))],ma)
 return 'preserved clipped courtyard roof'

def d17_ornament(m,x,y,L,a,H,obs,wall,frame,holes):
 style=obs['style']
 if style in ['renaissance','jugend','wahlberg']:
  # Mortar/rustication courses stop at every opening.
  for zz in [.48+i*.30 for i in range(11)]:d17_band(m,x,y,L,a,zz,holes,wall,.023,.018)
  d17_band(m,x,y,L,a,H/obs['levels']-.10,holes,TW,.14,.15)
  if style=='renaissance':
   upper=sorted(u for u,b,w,h,k in holes if b>H*.4)
   pilasters=[-L/2+.16,L/2-.16]+[(upper[i]+upper[i+1])/2 for i in [1,len(upper)-3] if 0<=i<len(upper)-1]
   for u in pilasters:facade_box(m,x,y,u,.395,H*.72,.23,.11,H*.49,TW,a)
  # Curved central attic with solid cheeks and rear; no floating triangular outlines.
  width=4.3 if style!='jugend' else 4.1;top=2.5
  outline=[(-width/2,0),(width/2,0),(width/2,1.60),(1.16,1.60)]+[(1.16*math.cos(i*math.pi/24),1.60+.9*math.sin(i*math.pi/24)) for i in range(25)]+[(-width/2,1.60)]
  xx,yy,_=lp(x,y,0,-.10,0,a);town_polyprofile(m,xx,yy,H,outline,a,wall,.28,False)
  # Windows sit in front of the separate attic backing with a raised trim.
  for u in ([-.70,.70] if style=='renaissance' else [0]):d17_window(m,x,y,u,H+.25,1.05,1.25,a,frame,TW,'cross',True)
  for dz in [0,.13]:facade_box(m,x,y,0,.46,H+dz,width+.24,.24,.11,TW,a)
  pts=[lp(x,y,v,-.065,H+z+.01,a) for v,z in outline[2:]];town_path(m,pts,.045,TW)
 if style=='wahlberg':
  # Balcony structurally tied to the facade; uprights seated into its stone slab.
  facade_box(m,x,y,0,.82,H+.04,4.9,1.0,.20,TS,a)
  for u in [-2.17,2.17]:
   town_rod(m,lp(x,y,u,.36,H-.62,a),lp(x,y,u,1.29,H-.02,a),.05,METAL)
  for j in range(25):facade_box(m,x,y,-2.35+j*4.7/24,1.29,H+.62,.025,.035,1.04,frame,a)
  for z in [H+.22,H+1.14]:facade_box(m,x,y,0,1.29,z,4.80,.07,.06,frame,a)
 if style=='jugend':
  # Faceted approximation of the photographed curved oriel, supported above the ground floor.
  pts=[(-2.05,.38),(-1.18,1.15),(1.18,1.15),(2.05,.38)]
  for (u,o),(v,p) in zip(pts,pts[1:]):
   P=lp(x,y,u,o,0,a);Q=lp(x,y,v,p,0,a);xx,yy,ln,aa=sf_edge(P[:2],Q[:2]);hh=[(0,3.9,ln*.55,1.95,'window'),(0,7.25,ln*.55,1.95,'window')]
   d17_wall(m,xx,yy,ln+.32,aa,3.35,H,hh,wall)
   for uu,b,w,h,k in hh:d17_window(m,xx,yy,uu,b,w,h,aa,frame,wall,'cross')
  outer=[(-2.32,.64),(-1.22,1.56),(1.22,1.56),(2.32,.64)]
  v=[lp(x,y,u,o,0,a)[:2] for u,o in outer];m.prism(v,3.25,3.36,wall)
  roof=town_mats['MetalRed'];vs=[lp(x,y,u,o,H+.12,a) for u,o in outer]+[lp(x,y,0,.15,H+.6,a)];m.faces(vs,[(0,1,4),(1,2,4),(2,3,4)],roof)
  for P,Q in zip(outer,outer[1:]):
   town_rod(m,lp(x,y,P[0],P[1],H+.06,a),lp(x,y,Q[0],Q[1],H+.06,a),.08,roof,8)

for name,original in D17['buildings'].items():
 if original['action']!='rebuild' or (globals().get('district17_only') and name not in district17_only):continue
 record=dict(original);bid=record['id'];obs=observed.get(bid);old=bpy.data.objects.get(name)
 if not old:raise RuntimeError('Missing original '+name)
 oldH=observed[bid]['H'] if old.get('detail_pass')==17 and bid in observed else record['H'];oldroof=[]
 for p in old.data.polygons:
  if min(old.data.vertices[i].co.z for i in p.vertices)>=oldH-.035:oldroof.append(([tuple(old.data.vertices[i].co) for i in p.vertices],old.data.materials[p.material_index].name))
 if obs:
  record.update(obs);delta=record['H']-oldH;oldroof=[([(x,y,z+delta) for x,y,z in vs],ma) for vs,ma in oldroof]
 bpy.data.objects.remove(old,do_unlink=True)
 m=Mesh(name,record['category']);H=record['H'];levels=record['levels'];modern=record['style'] in ['modern','service'];timber=record['style'] in ['timber','mansard_timber','timber_shop'];service=record['style']=='service';step=H/levels
 wall=D17MAT.get(record['colour'],town_mats.get(record['colour'],D17MAT['Ivory']));frame=D17MAT.get(record['paint'],town_mats.get(record['paint'],TW));trim=wall if modern else TW
 if timber and not obs:wall=SC['RedWood'] if 'M_Sodra_RedWood' in materials else town_mats['Panel'];trim=TW
 count={'windows':0,'doors':0,'frontages':0,'rear_segments':0,'roof':'','reference_status':record['reference_status'],'street':record['street']};primary=None
 if obs:
  possible=[(i,w) for i,w in enumerate(record['walls']) if w['street']==obs['street'] and w['frontage'] and w['z0']<0 and w['exposed']]
  if possible:primary=max(possible,key=lambda it:it[1]['length'])[0]
 for wi,w in enumerate(record['walls']):
  x,y,L,a=sf_edge(w['p'],w['q']);lo=w['z0'];hi=H if abs(w['z1']-original['H'])<.1 else w['z1'];holes=[];front=w['frontage'];isprimary=wi==primary
  # Exposed wall is only 5 cm outside the mapped outline; joints are behind this face.
  x,y,_=lp(x,y,0,-.30,0,a)
  for start,end in w['exposed']:
   margin=.46;span=end-start-2*margin
   if span<.78:continue
   pitch_target=3.05 if front else 3.50
   bays=obs['bays'] if isprimary else max(1,round(span/pitch_target));pitch=span/bays
   for j in range(bays):
    u=-L/2+start+margin+(j+.5)*pitch
    for level in range(levels):
     z=.72+level*step;h=min(1.92 if front else 1.57,step-1.13);ww=min(1.36 if front else 1.13,pitch*.54);kind='window'
     commercial=front and record['street'] in ['Storgatan','Kaggensgatan','Larmgatan'] and levels>=2 and not service
     if record['style']=='timber_shop':commercial=front
     if commercial and level==0:z=.28;h=min(2.75,step-.56);ww=min(2.8,pitch*.78);kind='shop'
     if service:h=.6;z=min(1.8,H-1);ww=min(.8,pitch*.45)
     if wi==record['entrance_wall'] and not isprimary and level==0 and j==bays//2:
      z=.12;h=min(2.55 if commercial else 2.28,step-.35);ww=min(1.18,pitch*.65);kind='door'
      if service:ww=min(2.5,pitch*.82);h=min(2.35,H-.3);kind='service_door'
     if isprimary:
      if record['style']=='renaissance' and level==0:kind='arch_window';z=.70;h=2.30
      if level==0 and j==(6 if record['style']=='wahlberg' else (0 if record['style']=='jugend' else bays//2)):
       z=.12;h=min(2.94,step-.35);ww=min(2.1,pitch*.86);kind='door'
      if record['style']=='jugend' and level>0 and j in [1,2]:continue
     if z<lo+.12 or z+h>hi-.25 or ww<.4 or h<.35:continue
     holes.append((u,z,ww,h,kind))
  d17_wall(m,x,y,L,a,lo,hi,holes,wall)
  for u,z,ww,h,kind in holes:
   if kind.endswith('door'):
    town_door(m,*lp(x,y,u,.095,0,a)[:2],z,ww,h,a,frame,kind=='door' and front and record['street'] in ['Storgatan','Kaggensgatan']);count['doors']+=1
    # Stone threshold is seated at ground level, no floating steps.
    facade_box(m,x,y,u,.40,.13,ww+.24,.35,.16,TS,a)
    if front:
     facade_box(m,x,y,u+ww/2+.19,.44,1.15,.085,.036,.19,METAL,a)
   elif kind=='arch_window':
    d17_arch_window(m,x,y,u,z,ww,h,a,frame,trim,wall);count['windows']+=1
   else:
    style='plain' if modern or kind=='shop' or not front else ('six' if timber else 'cross')
    d17_window(m,x,y,u,z,ww,h,a,frame,trim,style,front);count['windows']+=1
  if timber and lo<0:
   for start,end in w['exposed']:
    for j in range(max(1,round((end-start)/.18))):
     u=-L/2+start+(j+.5)*(end-start)/max(1,round((end-start)/.18))
     for p,q in d17_spans(.30,H-.15,holes,u,.095):facade_box(m,x,y,u,.371,(p+q)/2,.025,.032,q-p,wall,a)
  for start,end in w['exposed']:
   length=end-start;u=-L/2+(start+end)/2
   if length<.5:continue
   if front:count['frontages']+=1
   else:count['rear_segments']+=1
   if lo<0:
    # Cut the plinth at entrances instead of putting stone across a door.
    cuts=sorted(set([start,end]+[max(start,min(end,c+L/2+s*ww/2)) for c,z,ww,h,k in holes if k.endswith('door') for s in [-1,1]]))
    for l,r in zip(cuts,cuts[1:]):
     at=-L/2+(l+r)/2
     if not any(abs(at-c)<ww/2 for c,z,ww,h,k in holes if k.endswith('door')):facade_box(m,x,y,at,.36,.24,r-l,.095,.48,TS,a)
   if hi==H:
    facade_box(m,x,y,u,.37,H-.11,length,.19,.14,trim,a)
    if not modern:facade_box(m,x,y,u,.39,H-.24,length,.12,.065,trim,a)
    d17_gutter(m,x,y,u,length,H,a)
   if lo<0 and hi==H and length>3.4:
    pos=u+length/2-.17
    if all(abs(pos-c)>ww/2+.12 for c,z,ww,h,k in holes):sf_pipe(m,x,y,pos,H,a,METAL)
  if isprimary:
   d17_ornament(m,x,y,L,a,H,obs,wall,frame,holes)
   xx,yy,_=lp(x,y,0,15,0,a);target=lp(x,y,0,0,H*.52,a);label=f"{71+list(observed).index(bid)}_District_{bid}";district17_cameras.append((label,(xx,yy,2.3),target,26))
 count['roof']=d17_roof(m,record,oldroof,obs,primary)
 if obs:count['reference_status']='photographed facade; estimated dimensions and hidden elevations';count['reference']='https://www.kalmarkusten.se/platser/'+obs['ref']+'/'
 obj=m.finish();obj['osm_id']=bid;obj['detail_pass']=17;obj['eaves_height']=H;obj['massing_only']=False;obj['reference_status']=count['reference_status'];district17_names.append(name);district17_audit[name]=count
 print('HOUSE17',len(district17_names),name,count['windows'],flush=True)
if 'SM_Kvarnholmen_House_91072716' in district17_names:
 exec(compile((R/'scripts/build_water_tower17.py').read_text(),'build_water_tower17.py','exec'))
if 'SM_Kvarnholmen_House_93199604' in district17_names:
 exec(compile((R/'scripts/build_klapphuset17.py').read_text(),'build_klapphuset17.py','exec'))
if (R/'source/district17-camera-overrides.json').exists():
 overrides=json.loads((R/'source/district17-camera-overrides.json').read_text());byname={v['name']:v for v in overrides.values()}
 district17_cameras=[(c[0],byname[c[0]]['location'],byname[c[0]]['target'],byname[c[0]]['lens']) if c[0] in byname else c for c in district17_cameras]
(R/'previews/district17-facades.json').write_text(json.dumps(district17_audit,ensure_ascii=False,indent=2))
