"""Castenska garden: five-axis stepped gable and carved 1667 portal, photo-informed."""
name='SM_Building_92379312';old=bpy.data.objects.get(name);m=Mesh(name,'Storgatan/Landmarks')
# Preserve mapped rear wings; replace complete street block, not an overlay on generic windows.
cut=(-130,-115,-16.70,-7.0,-1,40)
for f in old.data.polygons:
 poly=[tuple(old.matrix_world@old.data.vertices[i].co) for i in f.vertices];ma=old.data.materials[f.material_index].name
 for pp in outside_box(poly,cut):m.faces(pp,[tuple(range(len(pp)))],ma,f.use_smooth)
bpy.data.objects.remove(old,do_unlink=True);pass18_names.append(name)
x,y,L,H,a=-122.8085,-8.4665,12.155,9.65,math.pi
cream='M_District17_Ivory';red='M_District17_RedJoinery';stone=TS
us=[-4.65,-2.32,0,2.32,4.65]
holes=[(u,.64,1.48,2.52,.74) for u in us if u!=0]+[(0,.34,1.58,2.62,.79)]+[(u,6.24,1.38,2.62,0) for u in us]
p18_face(m,x,y,L,H,holes,cream,a)
for u,b,w,h,r in holes:
 if r:continue  # Curved ground-floor joinery is built by gerdas_portal19.
 p18_win(m,x,y,u,b,w,h,r,a,frame=BROWN if b<1 else red,trim=stone,rows=1 if b<1 else 4,cols=1 if b<1 else 2)
# Roof falls behind a solid stepped gable; rear wings remain in their surveyed footprint.
back=-16.67
for sx in [-1,1]:
 m.faces([(x+sx*L/2,y-.35,H-.2),(x,y-.35,17.0),(x,back,17.0),(x+sx*L/2,back,H-.2)],[(0,1,2,3)],TT)
 facade_box(m,x+sx*L/2,(y+back)/2,0,0,H/2,.18,abs(back-y),H,cream,0)
# Continuous rectangular bands create the stepped silhouette without overlapping neighbouring roofs.
levels=[(12.155,9.65,11.05),(10.20,11.05,12.46),(8.20,12.46,13.88),(6.24,13.88,15.30),(4.28,15.30,16.72),(2.36,16.72,18.15),(.95,18.15,18.78)]
for tier,(width,z0,z1) in enumerate(levels):
 hs=[]
 if z0<12.46:hs=[(0,9.99,1.25,2.28,0)]
 # Clip holes to each stepped layer; the lower gable casement spans the first two tiers.
 facade_box(m,x,y,0,.12,(z0+z1)/2,width,.44,z1-z0,cream,a) if not hs else None
 if hs:
  for lo,hi in [(-width/2,-.625),(.625,width/2)]:facade_box(m,x,y,(lo+hi)/2,.12,(z0+z1)/2,hi-lo,.44,z1-z0,cream,a)
  if z0<9.99:facade_box(m,x,y,0,.12,(z0+9.99)/2,1.25,.44,9.99-z0,cream,a)
  if z1>12.27:facade_box(m,x,y,0,.12,(12.27+z1)/2,1.25,.44,z1-12.27,cream,a)
 nextwidth=levels[tier+1][0] if tier+1<len(levels) else 0
 for lo,hi in [(-width/2-.06,-nextwidth/2),(nextwidth/2,width/2+.06)]:
  if hi>lo:facade_box(m,x,y,(lo+hi)/2,.18,z1+.035,hi-lo,.58,.07,METAL,a)
p18_win(m,x,y,0,9.99,1.25,2.28,0,a,frame=red,trim=stone,rows=4,cols=2)
xx,yy,_=lp(x,y,0,.18,0,a);m.lathe(xx,yy,18.80,[(.24*math.sin(t*math.pi/16),.24*(1-math.cos(t*math.pi/16))) for t in range(17)],stone,24)
# Three circular loft vents: recessed dark discs and sandstone rim.
def ring(u,z,rx,rz,ma,out=.43,r=.045):
 town_path(m,[lp(x,y,u+rx*math.cos(t*math.tau/64),out,z+rz*math.sin(t*math.tau/64),a) for t in range(65)],r,ma)
for u,z in [(-2.17,10.73),(2.17,10.73),(0,14.00)]:
 vs=[lp(x,y,u+.23*math.cos(t*math.tau/40),.352,z+.29*math.sin(t*math.tau/40),a) for t in range(40)];m.faces(vs,[tuple(range(40))],IRON);ring(u,z,.27,.33,stone,.395,.06)
# Forged fleur-de-lys wall anchors in photographed staggered rows.
for z,row in [(4.72,[-5.5,-3.4,-1.2,1.2,3.4,5.5]),(8.95,[-5.5,-3.4,-1.2,1.2,3.4,5.5]),(12.55,[-3.2,-1.05,1.05,3.2]),(14.95,[-1.8,1.8]),(16.85,[0])]:
 for u in row:
  town_rod(m,lp(x,y,u,.40,z-.32,a),lp(x,y,u,.40,z+.37,a),.024,IRON)
  for sign in [-1,1]:
   town_path(m,[lp(x,y,u+sign*(.055+.13*math.cos(t*math.pi*1.7/20)),.42,z+.07+.13*math.sin(t*math.pi*1.7/20),a) for t in range(21)],.019,IRON)
# Continuous sculpted portal, timber door and sealed arched reveals.
exec(compile((R/'scripts/gerdas_portal19.py').read_text(),'gerdas_portal19.py','exec'))
# Shop glazing displays: sparse warm timber shelves and tins behind each arch.
for u in [-4.65,-2.32,2.32,4.65]:
 for z in [.94,1.40]:
  facade_box(m,x,y,u,.17,z,1.25,.12,.045,BROWN,a)
  for j in range(5):facade_box(m,x,y,u+(j-2)*.21,.19,z+.16,.14,.09,.27,GOLD if j%2 else TG,a)
# Distinctive circular hanging Gerda sign with an attached iron bracket.
u=5.53
town_path(m,[lp(x,y,u,.35,4.19,a),lp(x,y,u,1.2,4.19,a),lp(x,y,u,1.2,3.66,a)],.025,IRON)
# Two-sided disc perpendicular to facade.
xx,yy,_=lp(x,y,u,1.05,0,a)
for side in [-1,1]:
 aa=a+side*math.pi/2
 vv=[facade_point(xx,yy,.44*math.cos(t*math.tau/48),side*.025,3.48+.44*math.sin(t*math.tau/48),aa) for t in range(48)];m.faces(vv,[tuple(range(48))],GOLD)
 town_text(m,xx,yy,3.50,aa,'Gerda',.71,red)
# Copper downpipes anchored to the wall.
for u in [-L/2+.10,L/2-.10]:
 sf_pipe(m,x,y,u,H,a)
obj=p18_finish(m);obj['detail_pass']=19;obj['reference_notes']='references/portal19-notes.md'
