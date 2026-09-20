"""Complete exposed facades on remaining mapped masses. Individual elevations are inferred.
Explicit party-wall masking and the original lower passage polygons retain circulation.
"""
F15=json.loads((R/'source/facades15.json').read_text());D15=json.loads((R/'source/kvarnholmen.json').read_text());facade15_names=[];facade15_audit={}
for b in D15['buildings']:
 bid=b['id']
 if bid not in F15['buildings']:continue
 cfg=F15['buildings'][bid];name='SM_Kvarnholmen_House_'+bid;old=bpy.data.objects.get(name)
 # Keep exactly the previous clipped roof topology, including courtyard holes.
 roofdata=[]
 if old:
  for f in old.data.polygons:
   if min(old.data.vertices[i].co.z for i in f.vertices)>=b['height']-.18:
    roofdata.append(([tuple(old.data.vertices[i].co) for i in f.vertices],old.data.materials[f.material_index].name))
  bpy.data.objects.remove(old,do_unlink=True)
 m=Mesh(name,'Kvarnholmen/Completed facades');facade15_names.append(name);seed=int(''.join(x for x in bid if x.isdigit())[-8:]);rr=random.Random(seed);H=b['height'];levels=max(1,round(b['levels']));step=H/levels;modern=cfg['style']=='modern';timber=cfg['style']=='timber'
 color={'white':'Ivory','yellow':'Yellow','red':'Rose','green':'Lime','grey':'Lime'}.get(b['tags'].get('building:colour',''),['Ivory','Ivory','Yellow','Lime','Rose'][seed%5]);wall=town_mats[color];frame=TW if seed%4 else town_mats['PaintGreen'];trim=TI if seed%3 else wall
 if timber:wall=OW if seed%2 else SC['RedWood']
 nwin=ndoor=0
 for wi,w in enumerate(cfg['walls']):
  x,y,L,a=sf_edge(w['p'],w['q']);lo,hi=w['z0'],w['z1'];holes=[]
  # All new detail stays within 15 cm of the footprint; reveal is behind the face.
  x,y,_=lp(x,y,0,-.30,0,a)
  for start,end in w['exposed']:
   margin=.42;span=end-start-2*margin
   if span<.9:continue
   bays=max(1,round(span/(3.0 if modern else 2.85)));pitch=span/bays
   for j in range(bays):
    u=-L/2+start+margin+(j+.5)*pitch;width=min(1.62 if modern else 1.22,pitch*.61)
    for level in range(levels):
     z=.64+level*step;height=min(1.75 if modern else 1.63,step-.95)
     if z<lo+.13 or z+height>hi-.19 or width<.5:continue
     door=(wi==cfg['entrance_wall'] and level==0 and j==bays//2)
     if door:z=.12;height=min(2.25,hi-.3);width=min(1.1,pitch*.62)
     holes.append((u,z,width,height,door))
  # Continuous backing preserves closed buildings; openings are 20 cm recessed.
  facade_box(m,x,y,0,-.19,(lo+hi)/2,L,.24,hi-lo,wall,a)
  cuts=sorted(set([-L/2,L/2]+[v for u,z,ww,hh,d in holes for v in [u-ww/2,u+ww/2]]))
  for l,r in zip(cuts,cuts[1:]):
   spans=[(lo,hi)];centre=(l+r)/2
   for u,z,ww,hh,door in holes:
    if abs(centre-u)<ww/2+1e-5:spans=[(p,q) for v0,v1 in spans for p,q in [(v0,min(v1,z)),(max(v0,z+hh),v1)] if q>p+.005]
   for bottom,top in spans:facade_box(m,x,y,centre,.24,(bottom+top)/2,r-l,.22,top-bottom,wall,a)
  for u,z,ww,hh,door in holes:
   if door:
    town_door(m,*lp(x,y,u,.17,0,a)[:2],z,ww,hh,a,frame,modern);ndoor+=1
   else:
    sf_modern(m,x,y,u,z,ww,hh,a,frame,trim,1 if modern else 2,2);nwin+=1
    if not modern:facade_box(m,x,y,u,.39,z+hh+.14,ww+.35,.15,.095,trim,a)
  for start,end in w['exposed']:
   length=end-start
   if length<.5:continue
   u=-L/2+(start+end)/2
   if lo<0:facade_box(m,x,y,u,.34,.17,length,.10,.34,TS,a)
   if abs(hi-H)<.1:
    facade_box(m,x,y,u,.35,H-.13,length,.21,.18,trim,a)
    if not modern:facade_box(m,x,y,u,.37,H-.30,length,.12,.085,trim,a)
    town_rod(m,lp(x,y,u-length/2,.40,H+.01,a),lp(x,y,u+length/2,.40,H+.01,a),.045,METAL,8)
   if lo<0 and abs(hi-H)<.1 and length>3.5:
    sf_pipe(m,x,y,u+length/2-.18,H,a,METAL)
   if timber and lo<0:sf_wood(m,x,y,L,H,a,wall,[(u,z,ww,hh) for u,z,ww,hh,d in holes])
 # Preserve mapped roof, and add no invented rooftop storeys.
 for verts,ma in roofdata:m.faces(verts,[tuple(range(len(verts)))],ma)
 if not roofdata:
  for tri in b['roof_triangles']:m.faces([(x,y,H+z) for x,y,z in tri],[(0,1,2)],TT)
 obj=m.finish();obj['osm_id']=bid;obj['massing_only']=False;obj['detail_pass']=15;obj['reference_status']=cfg['reference_status'];facade15_audit[name]={'windows':nwin,'doors':ndoor,'style':cfg['style'],'preserved_passage':b['has_passage'],'reference_status':cfg['reference_status']}
