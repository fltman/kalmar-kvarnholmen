"""District road network and explicit building massing, pass 12.
Geometry follows mapped footprints; unknown heights/roof profiles are estimates.
Existing detailed town/church objects remain untouched.
"""
district=json.loads((R/'source/kvarnholmen.json').read_text());district_names=[]
ASPHALT='M_Kvarnholmen_Asphalt';WATER='M_Kvarnholmen_Water'
if ASPHALT not in materials:mat(ASPHALT,(.06,.065,.07),.90,0,'DistrictAsphalt')
if WATER not in materials:mat(WATER,(.025,.10,.13),.34,.15,'DistrictWater')
def district_new(name,category):
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 district_names.append(name);return Mesh(name,category)
def district_surface(m,triangles,z,ma):
 # Independent top triangles share spatially consistent UV coordinates.
 for t in triangles:
  v=[(x,y,z) for x,y in t]
  cross=(Vector(v[1])-Vector(v[0])).cross(Vector(v[2])-Vector(v[0]))
  if cross.z<0:v.reverse()
  m.faces(v,[(0,1,2)],ma)
def district_walls(m,polys,bottom,top,ma):
 for p in polys:
  for ring in [p['outer']]+p['holes']:
   for (ax,ay),(bx,by) in zip(ring,ring[1:]+ring[:1]):
    m.faces([(ax,ay,bottom),(bx,by,bottom),(bx,by,top),(ax,ay,top)],[(0,1,2,3)],ma)
# Replace only the placeholder portions of the original streets.
# Preserve the reviewed paving and curbs inside Stortorget.
m=district_new('SM_Streets','Ground')
for x in [-33,53]:m.box((x,20,.008-.08),(10,106,.16),GRANITE)
m.box((10.5,-4,-.071),(97,9,.16),GRANITE)
m.box((9.5,68,-.071),(99,9,.16),GRANITE)
for low,high in [(-33,-10),(5,70.5)]:m.box((-38,(low+high)/2,.01),(1.2,high-low,.22),PATH)
m.box((58,18.75,.01),(1.2,103.5,.22),PATH)
for y in [-32,73]:m.box((7,y,.01),(91,1.2,.22),PATH)
m.finish()
# Keep the exact authored Storgatan and Larmtorget paving, remove the two
# temporary full-length cross-street rectangles now supplied by the network.
m=district_new('SM_Storgatan_Paving','Storgatan/Ground');ext=json.loads((R/'source/storgatan.json').read_text())
route=next(w['points'] for w in ext['roads'] if w['id']=='35772928')
for (ax,ay),(bx,by) in zip(route,route[1:]):
 ln=math.hypot(bx-ax,by-ay);an=math.atan2(by-ay,bx-ax);cx,cy=(ax+bx)/2,(ay+by)/2
 m.box((cx,cy,-.054),(ln+.035,11.55,.13),'M_Storgatan_Setts',an)
 for off in [-4.52,4.52]:m.box((cx-off*math.sin(an),cy+off*math.cos(an),.018),(ln+.035,2.0,.085),'M_Storgatan_Slabs',an)
 for off in [-3.43,3.43]:m.box((cx-off*math.sin(an),cy+off*math.cos(an),.014),(ln+.035,.17,.062),PATH,an)
 for off in [-3.2,3.2]:m.box((cx-off*math.sin(an),cy+off*math.cos(an),.015),(ln+.035,.09,.06),IRON,an)
for x in [-186.5,-290.4]:m.box((x,-2.5,-.059),(11.2,15,.13),'M_Storgatan_Setts')
square=next(w['points'] for w in ext['roads'] if w['id']=='35772926');m.prism(square[:-1],-.08,.007,'M_Storgatan_Setts')
for y in [-1,-25,22]:m.box((-317,y,.013),(49,.55,.06),PATH)
for x in [-299,-335]:m.box((x,-1,.013),(.55,52,.06),PATH)
m.finish()
# Coastline-ground and a low water plane establish the extent of the district.
m=district_new('SM_Kvarnholmen_Land','Kvarnholmen/Ground');district_surface(m,district['land_triangles'],-.115,GROUND)
district_walls(m,district['island_outline'],-1.25,-.115,TS);m.finish()
m=district_new('SM_Kvarnholmen_Water','Kvarnholmen/Water');m.box((-50,-30,-1.36),(10000,10000,.06),WATER);m.finish()
levels={'asphalt':(.013,ASPHALT),'stone':(.013,'M_Storgatan_Setts'),'path':(.015,'M_Storgatan_Slabs'),'sidewalk':(.105,'M_Storgatan_Slabs'),'curb':(.12,TS)}
for chunk in district['surface_chunks']:
 m=district_new('SM_Kvarnholmen_Street_'+chunk['id'],'Kvarnholmen/Streets')
 for key,triangles in chunk['layers'].items():
  z,ma=levels[key];district_surface(m,triangles,z,ma)
  if key in chunk.get('edges',{}):district_walls(m,chunk['edges'][key],.008,z,ma)
 m.finish()
# Each footprint stays a separate named mesh for the later facade passes.
# Roof heightfields are clipped to all outer/inner rings, keeping courtyards open.
for b in district['buildings']:
 bid=b['id'];t=b['tags'];m=district_new('SM_Kvarnholmen_House_'+bid,'Kvarnholmen/Building massing')
 key={'white':'Ivory','yellow':'Yellow','red':'Rose','green':'Lime','grey':'Lime'}.get(t.get('building:colour',''),['Ivory','Ivory','Yellow','Lime','Rose'][int(''.join(c for c in bid if c.isdigit())[-6:])%5]);wall=town_mats[key]
 if t.get('building:material')=='brick':wall=town_mats['Rose']
 roof=town_mats['MetalGrey'] if b['roof']=='flat' else town_mats['TileRed']
 if t.get('roof:material') in ['copper','metal','sheet_metal','zinc']:roof=TC if t.get('roof:material')=='copper' else town_mats['MetalGrey']
 h=b['height'];base=b['base_polygons'] if b['has_passage'] else b['polygons']
 if t.get('building')=='roof':
  x0,y0,x1,y1=b['bounds'];h=3.0
  for x in [x0+.2,x1-.2]:
   for y in [y0+.2,y1-.2]:m.box((x,y,h/2),(.14,.14,h),IRON)
 else:
  district_walls(m,base,-.10,.45,TS);district_walls(m,base,.45,min(3.4,h),wall)
  if h>3.4:district_walls(m,b['polygons'],3.4,h,wall)
 if b['roof']=='flat' or t.get('building')=='roof':district_surface(m,b['triangles'],h+.025,roof)
 else:
  for tri in b['roof_triangles']:
   vs=[(x,y,h+z) for x,y,z in tri]
   if (Vector(vs[1])-Vector(vs[0])).cross(Vector(vs[2])-Vector(vs[0])).z<0:vs.reverse()
   m.faces(vs,[(0,1,2)],roof)
 # A narrow coping follows the actual outline; no bounding-box roofs across courtyards.
 for p in b['polygons']:
  for ring in [p['outer']]+p['holes']:
   for (ax,ay),(bx,by) in zip(ring,ring[1:]+ring[:1]):
    ln=math.hypot(bx-ax,by-ay)
    if ln>.02:m.box(((ax+bx)/2,(ay+by)/2,h-.06),(ln,.15,.13),TI,math.atan2(by-ay,bx-ax))
 obj=m.finish();obj['osm_id']=bid;obj['massing_only']=True;obj['height_source']='OSM height' if t.get('height') else ('OSM storeys' if t.get('building:levels') else 'estimated')
# Clear, named viewpoints for reviewing the expanded streets.
district_cameras=[
 ('46_Kvarnholmen_Hela',(-690,-800,680),(-70,0,0),36),
 ('47_Sodra_Langgatan',(-184,-74,1.8),(120,-74,5.0),28),
 ('48_Norra_Langgatan',(-180,69,1.8),(130,69,4.6),28),
 ('49_Fiskaregatan',(-178,141,1.8),(180,141,4.6),28),
 ('50_Ostra_Kvarnholmen',(255,105,2.0),(254,-130,4.5),28),
 ('51_Sodra_Kanalgatan',(-130,292,3.0),(170,247,6.0),29),
 ('52_Skeppsbron',(70,-227,3.0),(296,-135,6.0),29),
 ('53_Kvarnholmen_Fagelvy',(470,-490,390),(-90,35,0),38),
]

# Place street review cameras on mapped centre-lines rather than nominal grid lines.
review_streets={'47_':'Södra Långgatan','48_':'Norra Långgatan','49_':'Fiskaregatan','50_':'Östra Vallgatan','51_':'Södra Kanalgatan','52_':'Skeppsbron'}
for index,(label,loc,target,lens) in enumerate(district_cameras):
 key=label[:3]
 if key not in review_streets:continue
 road=next(q for q in district['roads'] if q['id']=='35771894') if key=='49_' else max([q for q in district['roads'] if q['name']==review_streets[key]],key=lambda q:q['length'])
 points=road['points'];segments=[math.dist(p,q) for p,q in zip(points,points[1:])];total=sum(segments)
 def along(frac):
  remaining=frac*total
  for p,q,ln in zip(points,points[1:],segments):
   if remaining<=ln:return(p[0]+(q[0]-p[0])*remaining/ln,p[1]+(q[1]-p[1])*remaining/ln)
   remaining-=ln
  return points[-1]
 start=along(.12);end=along(.80);district_cameras[index]=(label,(*start,1.85),(*end,3.5),lens)

# Remove sub-millimetre clipping slivers after Blender's float32 conversion.
for name in district_names:
 if name.startswith('SM_Kvarnholmen_Street_') or name=='SM_Kvarnholmen_Land':
  me=bpy.data.objects[name].data;bm=bmesh.new();bm.from_mesh(me)
  bad=[f for f in bm.faces if f.calc_area()<1e-7]
  if bad:bmesh.ops.delete(bm,geom=bad,context='FACES')
  bm.to_mesh(me);bm.free();me.update()

# Preserve the photo-reviewed street facades in future district rebuilds.
if (R/'source/sodra-facades.json').exists():
 exec(compile((R/'scripts/build_sodra_facades.py').read_text(),str(R/'scripts/build_sodra_facades.py'),'exec'))
 district_names=list(dict.fromkeys(district_names+sodra_names));district_cameras+=sodra_cameras

# Restore pass-15 scan recipes before creating the landmark and district facades.
if (R/'source/polish15-material-specs.json').exists():
 specs.update(json.loads((R/'source/polish15-material-specs.json').read_text()))
 exec(compile((R/'scripts/apply_polish15_blender.py').read_text(),'apply_polish15_blender.py','exec'))
 exec(compile((R/'scripts/polish15_geometry_helpers.py').read_text(),'polish15_geometry_helpers.py','exec'))

# Preserve the landmark and surviving-fortification pass in future district builds.
if (R/'source/landmarks14.json').exists():
 exec(compile((R/'scripts/build_landmarks14.py').read_text(),str(R/'scripts/build_landmarks14.py'),'exec'))
 district_names=list(dict.fromkeys(district_names+landmark_names));district_cameras+=landmark_cameras

# Keep completed background facades on future district rebuilds.
if (R/'source/facades15.json').exists():
 exec(compile((R/'scripts/build_facades15.py').read_text(),'build_facades15.py','exec'))
 district_names=list(dict.fromkeys(district_names+facade15_names))

# Full coverage pass also upgrades the older square/corridor background objects.
if (R/'source/district17.json').exists():
 exec(compile((R/'scripts/build_district17.py').read_text(),'build_district17.py','exec'))
 district_names=list(dict.fromkeys(district_names+district17_names));district_cameras+=district17_cameras

# Reference-specific pass 18 overrides retain bespoke facades and land use on full rebuilds.
if (R/'source/pass18.json').exists():
 exec(compile((R/'scripts/build_pass18.py').read_text(),'build_pass18.py','exec'))
 district_names=list(dict.fromkeys(district_names+pass18_names));district_cameras+=pass18_cameras

# Preserve the reference-specific Storgatan and northern street corners.
exec(compile((R/'scripts/build_street20.py').read_text(),'build_street20.py','exec'))
district_names=list(dict.fromkeys(district_names+street20_names));district_cameras+=street20_cameras
