"""Nine individually observed west Storgatan frontages, pass 16.
Visual estimates from Joakim Nilsson's June 2020 panorama and Halme May 2022.
No business signage is used as evidence of present-day tenancy.
"""
import ast
street16_names=[];street16_audit={}
exec(compile((R/'scripts/street16_materials.py').read_text(),'street16_materials.py','exec'))
for filename in ['build_larmtorget_facades.py']:
 tree=ast.parse((R/'scripts'/filename).read_text());tree.body=[n for n in tree.body if isinstance(n,ast.FunctionDef)]
 exec(compile(tree,filename,'exec'))
GLZ=town_mats['Glass'];MET=town_mats['MetalGrey'];BR=town_mats['PaintBrown']
profiles16={
 '92204197':dict(H=7.45,bays=5,colour='Yellow',paint='PaintWhite',roof='MetalRed',rise=3.0,style='peak',floors=2),
 '92204194':dict(H=7.45,bays=5,colour='Rose',paint='PaintWhite',roof='TileRed',rise=3.0,style='arched',floors=2),
 '92204175':dict(H=8.1,bays=7,colour='Ivory',paint='PaintWhite',roof='MetalGrey',rise=2.6,style='attic',floors=2),
 '92204166':dict(H=7.5,bays=3,colour='Yellow',paint='PaintWhite',roof='Copper',rise=2.7,style='narrow',floors=2),
 '92204199':dict(H=7.8,bays=8,colour='Yellow',paint='PaintBrown',roof='TileRed',rise=4.0,style='yellow_corner',floors=2),
 '92204203':dict(H=7.9,bays=8,colour='Yellow',paint='PaintWhite',roof='TileRed',rise=2.8,style='bank',floors=2),
 '92204159':dict(H=8.1,bays=6,colour='PaintWhite',paint='PaintBrown',roof='Copper',rise=3.5,style='modern',floors=2),
 '92204163':dict(H=10.2,bays=6,colour='PaintWhite',paint='PaintBrown',roof='Copper',rise=2.6,style='modern',floors=3),
 '92204155':dict(H=6.6,bays=6,colour='Rose',paint='PaintWhite',roof='TileRed',rise=2.8,style='pink_corner',floors=2),
}

def s16_window(m,x,y,u,b,w,h,a,frame,style='cross',trim=TW,arc=False):
 xx,yy,_=lp(x,y,u,0,0,a)
 # Slim casements sit 20 cm inside the exterior masonry face.
 town_window(m,xx,yy,b+h/2,w,h,a,frame,arc,1,2,False)
 if style=='cross':facade_box(m,x,y,u,.17,b+h*.72,w,.09,.043,frame,a)
 elif style=='six':
  for t in [1/3,2/3]:facade_box(m,x,y,u,.17,b+h*t,w,.09,.028,frame,a)
 for off in [-w/2-.065,w/2+.065]:facade_box(m,x,y,u+off,.365,b+h/2,.095,.08,h+.13,trim,a)
 facade_box(m,x,y,u,.40,b-.065,w+.25,.30,.065,MET,a)
 if not arc:facade_box(m,x,y,u,.365,b+h+.07,w+.25,.11,.10,trim,a)
 else:town_arch_band(m,xx,yy,b+h,w/2+.035,.09,a,trim,.40)
 # Casement hinges and latch, not another full-sized grid.
 for zz in [b+.23,b+h-.23]:
  for off in [-w/2+.035,w/2-.035]:facade_box(m,x,y,u+off,.19,zz,.017,.022,.065,MET,a)
 facade_box(m,x,y,u+.08,.205,b+h*.42,.016,.025,.07,MET,a)

def s16_shop(m,x,y,u,b,w,h,a,frame,door=False,arc=False):
 xx,yy,_=lp(x,y,u,0,0,a)
 town_window(m,xx,yy,b+h/2,w,h,a,frame,arc,1,1,False)
 for off in [-w/2-.07,w/2+.07]:facade_box(m,x,y,u+off,.36,b+h/2,.11,.10,h+.1,TS,a)
 facade_box(m,x,y,u,.38,b-.06,w+.25,.22,.08,TS,a)
 if door:
  town_door(m,*lp(x,y,u,.03,0,a)[:2],.10,min(w,1.1),h-.02,a,frame,True)
 else:
  facade_box(m,x,y,u,.17,b+h*.84,w,.07,.045,frame,a)
  # Thin inward returns establish the window recess, leaving clear glazing.
  for side in [-1,1]:facade_box(m,x,y,u+side*(w/2-.015),.24,b+h/2,.028,.22,h,frame,a)
 if arc:town_arch_band(m,xx,yy,b+h,w/2+.035,.09,a,TW,.40)

def s16_dormer(m,x,y,z,w,a,roof,curved=False):
 # Recessed face with solid cheeks; the roof ends behind the window, never across it.
 h=1.45
 facade_box(m,x,y,0,-.85,z+h/2,w,1.7,h,roof,a)
 hs=[(0,z+.14,w*.67,h-.27,False)]
 lm_wall(m,x,y,w,z+h,[(0,0,w,z,False)]+hs,roof,a)
 s16_window(m,x,y,0,z+.14,w*.67,h-.27,a,TW,'cross',roof)
 if curved:
  outline=[(-w/2,0),(w/2,0)]+[(w/2*math.cos(t*math.pi/20),.22*math.sin(t*math.pi/20)) for t in range(21)]
  town_polyprofile(m,*lp(x,y,0,.40,0,a)[:2],z+h,outline,a,roof,1.9,False)
  pts=[lp(x,y,w*.54*math.cos(t*math.pi/24),.43,z+h+.25*math.sin(t*math.pi/24),a) for t in range(25)]
  town_path(m,pts,.035,roof)
 else:
  facade_box(m,x,y,0,-.60,z+h+.04,w+.18,2.1,.12,roof,a)

def s16_front(m,x,y,L,a,pr,side=False):
 H=pr['H'];style=pr['style'];ma=town_mats[pr['colour']];frame=town_mats[pr['paint']]
 n=(4 if style=='yellow_corner' else 4) if side else pr['bays']
 spacing=L/n;centres=[-L/2+(k+.5)*spacing for k in range(n)]
 ismodern=style=='modern';ww=min(1.52 if ismodern else 1.38,spacing*.54)
 upper=[]
 for floor in range(1,pr['floors']):
  bottom=4.35 if pr['floors']==2 else 4.05+(floor-1)*2.8
  hh=1.62 if style in ['bank','pink_corner'] else (1.85 if pr['floors']==2 else 1.75)
  for u in centres:upper.append((u,bottom,ww,hh,False))
 # Different commercial bay widths and separate historic entrance position.
 shops=[];door_index=0 if style in ['peak','attic'] else n//2
 for k,u in enumerate(centres):
  ar=style=='arched';w=min(spacing*.78,3.15)
  if style=='bank':w=min(1.85,spacing*.66)
  door=k==door_index
  if style=='peak' and door:w=1.52
  if style=='bank' and door:w=1.75
  b=.10 if door else (.53 if style in ['peak','bank'] else .29)
  h=(2.9-b) if ar else 2.96-b
  shops.append((u,b,w,h,ar,door))
 holes=upper+[s[:5] for s in shops]
 lm_front(m,x,y,L,H,holes,ma,a)
 for u,b,w,h,arc in upper:
  winstyle='plain' if style in ['pink_corner','bank','modern'] else 'cross'
  s16_window(m,x,y,u,b,w,h,a,frame,winstyle,ma if ismodern else TW)
  if style=='yellow_corner':
   facade_box(m,x,y,u,.362,b-.39,w+.37,.035,.38,TW,a)
   facade_box(m,x,y,u,.386,b-.39,w+.10,.025,.22,ma,a)
  if style=='attic':
   # Framed X reliefs below each window and a shallow raised lintel.
   xx,yy,_=lp(x,y,u,.37,0,a);town_border(m,xx,yy,b-.37,w+.15,.44,a,TW,.04,.032)
   for sg in [-1,1]:town_rod(m,lp(x,y,u-w*.42,.42,b-.53 if sg==1 else b-.21,a),lp(x,y,u+w*.42,.42,b-.21 if sg==1 else b-.53,a),.018,TW)
 for k,(u,b,w,h,arc,door) in enumerate(shops):
  if door and style in ['peak','arched','bank']:
   town_door(m,*lp(x,y,u,.055,0,a)[:2],.10,w,h,a,BR if style!='bank' else IRON,style=='bank')
   if style=='arched':
    xx,yy,_=lp(x,y,u,.4,0,a);town_arch_band(m,xx,yy,b+h,w/2+.04,.13,a,TW,.08)
    for sg in [-1,1]:town_scroll(m,*lp(x,y,u+sg*(w/2+.22),.37,0,a)[:2],3.18,a,sg,.52,.08,TW)
  else:s16_shop(m,x,y,u,b,w,h,a,BR if style in ['yellow_corner','pink_corner'] else frame,door,arc)
  if style=='peak' and not door:
   # Basement ventilators are visible below the retail glazing.
   facade_box(m,x,y,u,.367,.245,w*.48,.045,.25,MET,a)
   for du in [-w*.17,0,w*.17]:facade_box(m,x,y,u+du,.40,.245,.032,.045,.25,TW,a)
  if style=='bank' and door:
   # Staggered stone portal blocks, clearly visible in the June 2020 panorama.
   for side2 in [-1,1]:
    for row in range(8):
     for col in range(3):
      du=side2*(w/2+.12+col*.18)
      facade_box(m,x,y,u+du,.405+(row+col)%2*.025,.23+row*.355,.16,.14,.33,TS if col==0 else TI,a)
   for k2 in range(13):facade_box(m,x,y,u-1.32+k2*.22,.43,3.18,.15,.17,.31,TI,a)
  # Low masonry is split at every door to keep thresholds uncluttered.
 for lo,hi in zip([-L/2]+[s[0]+s[2]/2 for s in shops],[s[0]-s[2]/2 for s in shops]+[L/2]):
  if hi>lo:facade_box(m,x,y,(lo+hi)/2,.369,.25,hi-lo,.07,.50,TS,a)
 if style=='pink_corner':
  facade_box(m,x,y,0,.45,3.27,L,.20,.38,IRON,a)
  ext_awning(m,x,y,L-.35,3.28,a,IRON)
 elif style in ['yellow_corner','modern']:
  for s in shops:ext_awning(m,*lp(x,y,s[0],0,0,a)[:2],s[2]+.2,3.23,a,MET if style=='yellow_corner' else AWNING)
 else:
  facade_box(m,x,y,0,.382,4.17 if style=='arched' else 3.45,L,.12,.13,ma if style=='bank' else TI,a)
 # More restrained, building-specific cornice sizes than the shared old profile.
 lm_cornice(m,x,y,L+.1,H-.08,a,ma if ismodern else TW,style=='attic')
 if style=='bank':
  for u in [centres[0]-spacing/2+.12,centres[n//2]+spacing/2,centres[-1]+spacing/2-.12]:facade_box(m,x,y,u,.386,H/2,.19,.09,H-.4,TI,a)
  facade_box(m,x,y,0,.39,4.0,L,.10,.12,TI,a)
 if style=='yellow_corner':
  for u in [-L/2+.15,L/2-.15]:facade_box(m,x,y,u,.39,(H+3.5)/2,.25,.10,H-3.5,TW,a)
 for u in [-L/2+.12,L/2-.12]:town_drain(m,*lp(x,y,u,.15,0,a)[:2],H,a)
 street16_audit.setdefault(current_bid,{'fronts':0,'windows':0,'shops':0,'doors':0})
 q=street16_audit[current_bid];q['fronts']+=1;q['windows']+=len(upper);q['shops']+=len(shops);q['doors']+=sum(s[-1] for s in shops)
 return centres

for current_bid,pr in profiles16.items():
 b=next(b for b in extension['buildings'] if b['id']==current_bid);p=b['polygon'];H=pr['H'];ma=town_mats[pr['colour']];roof=town_mats[pr['roof']]
 name='SM_Building_'+current_bid;old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 m=Mesh(name,'Storgatan/Buildings');street16_names.append(name)
 clockwise=sum(v[0]*w[1]-w[0]*v[1] for v,w in zip(p,p[1:]+p[:1]))<0
 main=[]
 for v,w in zip(p,p[1:]+p[:1]):
  if clockwise:v,w=w,v
  dx,dy=w[0]-v[0],w[1]-v[1];L=math.hypot(dx,dy);a=math.atan2(dy,dx);x,y=(v[0]+w[0])/2,(v[1]+w[1])/2
  front=abs(dy)<1 and -12<y<6 and L>3
  side=pr['style'] in ['yellow_corner','pink_corner'] and abs(dx)<1 and x< -284 and L>3
  if front or side:
   s16_front(m,x,y,L,a,pr,side)
   if front:main.append((x,y,L,a))
  else:
   facade_box(m,x,y,0,-.15,H/2,L,.30,H,ma,a)
   facade_box(m,x,y,0,.02,.25,L,.06,.50,TS,a)
   # Rear-facing windows remain simple; party walls receive no arbitrary detail.
   if abs(dy)<1 and (abs(y-b['bounds'][2])<.5 or abs(y-b['bounds'][3])<.5):
    for k in range(max(1,round(L/3.3))):
     xx=v[0]+(k+.5)/max(1,round(L/3.3))*dx;yy=v[1]+(k+.5)/max(1,round(L/3.3))*dy
     for floor in range(pr['floors']):town_window(m,xx,yy,2+floor*2.9,1.1,1.5,a,TW,False,2,2)
 # The same OSM footprint and courtyard holes are retained.
 m.prism(p,H,H+.08,roof)
 x,y,L,a=max(main,key=lambda q:q[2]);depth=min(12,b['bounds'][3]-b['bounds'][2]);rx,ry,_=lp(x,y,0,-depth/2,0,a)
 roof_face_start=len(m.f)
 town_roof(m,rx,ry,L,depth,H,pr['rise'],roof,pr['roof'] in ['MetalGrey','MetalRed','Copper'],hipped=pr['style'] not in ['yellow_corner','peak','arched','attic'])
 if pr['style']=='yellow_corner':
  # The square-facing gable is ochre, not the helper's generic ivory.
  for i in range(roof_face_start,len(m.f)):
   if m.mats[m.mi[i]]==TI and len(m.f[i])==3:
    if ma not in m.mats:m.mats.append(ma)
    m.mi[i]=m.mats.index(ma)
 if pr['style']!='pink_corner':
  positions=[-L*.30,L*.30] if pr['style'] not in ['modern','bank'] else [-L*.27,L*.27]
  for u in positions:
   xx,yy,_=lp(x,y,u,-1.8,0,a)
   s16_dormer(m,xx,yy,H+.62,2.8 if pr['style']=='modern' else 1.42,a,roof,pr['style'] in ['peak','yellow_corner','attic'])
 if pr['style']=='attic':
  xx,yy,_=lp(x,y,0,-1.8,0,a);w=L*.43;z=H+.55
  facade_box(m,xx,yy,0,-1,z+.8,w,2,1.6,ma,a)
  for u in [-w*.31,0,w*.31]:s16_window(m,xx,yy,u,z+.2,w*.22,1.20,a,frame=TW,style='plain',trim=TW)
  lm_cornice(m,xx,yy,w+.12,z+1.65,a,TW)
 obj=m.finish()
 for idx,material_slot in enumerate(obj.data.materials):
  if material_slot.name in street16_material_map:obj.data.materials[idx]=materials[street16_material_map[material_slot.name]]
 for j,hole in enumerate(b.get('holes',[])):
  cutm=Mesh('Temporary16_courtyard','Temporary');cutm.prism(hole,-1,H+10,TS);cut=cutm.finish()
  bpy.context.view_layer.objects.active=obj;mod=obj.modifiers.new('Mapped courtyard','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cut;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cut,do_unlink=True)
 street16_audit[current_bid]['style']=pr['style']
 print('STREET16_BUILT',name,flush=True)

street16_cameras=[('69_Storgatan_Portal',(-199,-2.8,1.75),(-204,5,4.1),27),('70_Storgatan_Sodra',(-197,-1.6,1.75),(-216,-8,4.2),27)]
