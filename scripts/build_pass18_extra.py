"""Measured footprint repairs, Witt rear articulation, and Barometern's observed entrance."""
# Re-run only the four established south-row house bodies with true front widths and clipped roofs.
site=json.loads((R/'source/site.json').read_text());buildings={b['id']:b for b in site['buildings']};town_names=[]
oldstone,oldglass,oldframe=STONE,GLASS,FRAME
code=(R/'scripts/build_town_details.py').read_text();start=code.index('# South row:');end=code.index('\n#',start+12);section=code[start:end]
# The next comment can be within the loop; use the exact next section boundary instead.
end=code.index('\n#',code.index(' m.finish()',start));section=code[start:end]
section=section.replace('x0,x1,y0,y1=town_bounds(p);w=x1-x0','x0,x1,y0,y1=D18["town"][bid]["front_bounds"];w=x1-x0')
section=section.replace('town_roof(m,','p18_skip_roof(m,')
section=section.replace(' m.finish()',"\n for tri in D18['town'][bid]['roof18']:m.faces(tri,[(0,1,2)],town_mats['MetalGrey'] if bid=='92412866' else TT)\n p18_finish(m)")
def p18_skip_roof(*args,**kwargs):pass
exec(compile(section,'correct_square_frontages','exec'))
pass18_names+=town_names
# Witt: preserve the photographed north/west facades and add the lower glazed south annex.
sodra=json.loads((R/'source/sodra-facades.json').read_text());SC={k:'M_Sodra_'+k for k in ['Cream','Sand','RedWood','OchreWood','DarkTile']}
m=p18_new('SM_Kvarnholmen_House_91846934');b=D18['witt']
# Extract only the existing hotel frontage helper.
tree=ast.parse((R/'scripts/build_sodra_facades.py').read_text());tree.body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='hotel_face'];exec(compile(tree,'witt_street_facade','exec'))
for part in b['parts18']:
 H=part['height'];poly=part['outer'];low=H<8
 for x,y,L,a in l14_edges(poly):
  if abs(y+119)<.01:continue
  street=x<59 or y>-82
  if street and not low:hotel_face(m,x,y,L,a);continue
  if L<1:continue
  N=max(1,round(L/(3.6 if low else 2.8)));us=[-L/2+(k+.5)*L/N for k in range(N)]
  if low:
   hs=[(u,1.10,L/N-.24,2.6,0) for u in us]+[(u,4.53,1.8,1.3,0) for u in us]
  else:hs=[(u,z,1.52,1.65,0) for u in us for z in [1.0,4.18,7.15]]
  p18_face(m,x,y,L,H,hs,SC['Cream'],a)
  for u,z,w,h,r in hs:p18_win(m,x,y,u,z,w,h,r,a,frame=BROWN,trim=TW,rows=1,cols=2 if low and z<2 else 1)
  facade_box(m,x,y,0,.40,.48,L,.22,.96,TS,a)
  p18_band(m,x,y,L+.2,H,a,TC,.40)
  if low:
   facade_box(m,x,y,0,.68,3.86,L,1.0,.14,METAL,a);facade_box(m,x,y,0,1.15,3.75,L,.10,.38,IRON,a)
   if y< -125:
    town_text(m,*lp(x,y,0,1.24,0,a)[:2],3.66,a,'FIRST HOTEL WITT',4.3,TW)
    # Landing and broad supported stairs to the glass rear entrance.
    for k in range(7):facade_box(m,x,y,0,1.0+k*.29,(7-k)*.075,3.4,.85,(7-k)*.15,TS,a)
    for sign in [-1,1]:
     for k in [0,3,6]:facade_box(m,x,y,sign*1.7,1.0+k*.29,(7-k)*.15+.47,.05,.05,.94,IRON,a)
     town_rod(m,lp(x,y,sign*1.7,.8,2.0,a),lp(x,y,sign*1.7,3.1,1.05,a),.027,IRON)
  for u in [-L/2+.12,L/2-.12]:sf_pipe(m,x,y,u,H,a)
 m.faces([(x,y,H+.04) for x,y in poly],[tuple(range(len(poly)))],METAL)
# Upper main block closes onto the lower roof at the step.
m.box((72.2,-119,8.52),(30.0,.3,3.4),SC['Cream'])
p18_finish(m)
# Barometern: cut away the generic entrance-area geometry before inserting the recessed door.
name='SM_Building_92379310';old=bpy.data.objects.get(name)
def outside_box(poly,bounds):
 remaining=poly;out=[]
 for axis,limit,sign in [(0,bounds[0],1),(0,bounds[1],-1),(1,bounds[2],1),(1,bounds[3],-1),(2,bounds[4],1),(2,bounds[5],-1)]:
  if not remaining:break
  ins=[];outs=[]
  for p,q in zip(remaining,remaining[1:]+remaining[:1]):
   dp=(p[axis]-limit)*sign;dq=(q[axis]-limit)*sign
   (ins if dp>=0 else outs).append(p)
   if (dp>=0)!=(dq>=0):
    t=dp/(dp-dq);v=tuple(p[i]+t*(q[i]-p[i]) for i in range(3));ins.append(v);outs.append(v)
  if len(outs)>=3:out.append(outs)
  remaining=ins
 return out
m=Mesh(name,'Buildings');cut=(-41.0,-38.0,-51.7,-46.3,-.20,4.35)
for f in old.data.polygons:
 poly=[tuple(old.matrix_world@old.data.vertices[i].co) for i in f.vertices];ma=old.data.materials[f.material_index].name
 # Bounding test makes the majority of the retained mesh untouched.
 hit=all(max(v[k] for v in poly)>=cut[k*2] and min(v[k] for v in poly)<=cut[k*2+1] for k in range(3))
 for pp in outside_box(poly,cut) if hit else [poly]:m.faces(pp,[tuple(range(len(pp)))],ma,f.use_smooth)
bpy.data.objects.remove(old,do_unlink=True);pass18_names.append(name)
x,y,a=-39.91,-49.0,math.pi/2
for q in [-2.15,2.15]:facade_box(m,x,y,q,.38,2.07,.46,.58,4.14,IRON,a)
facade_box(m,x,y,0,.25,3.83,4.45,.44,1.0,AS18,a)
facade_box(m,x,y,0,-.20,1.63,3.90,.10,3.20,GLAZE,a)
for q in [-1.92,-.95,.95,1.92]:facade_box(m,x,y,q,.13,1.64,.08,.14,3.22,IRON,a)
for z in [.08,3.22]:facade_box(m,x,y,0,.13,z,3.92,.14,.08,IRON,a)
for q in [-.75,.75]:town_rod(m,lp(x,y,q,.24,1.15,a),lp(x,y,q,.24,1.68,a),.023,TC)
facade_box(m,x,y,0,.40,.06,4.4,1.0,.12,AS18,a)
town_text(m,*lp(x,y,0,.52,0,a)[:2],3.61,a,'Barometern',3.45,IRON)
p18_finish(m)
