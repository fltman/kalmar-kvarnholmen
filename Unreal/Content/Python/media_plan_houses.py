"""One collision-aware view per mapped building, plus grouped named landmarks."""
import unreal as u,json,math,collections
from pathlib import Path
R=Path(__file__).resolve().parents[3];D=json.loads((R/'source/district17.json').read_text())['buildings'];M=json.loads((R/'exports/manifest.json').read_text());K=json.loads((R/'source/kvarnholmen.json').read_text());C={int(c['name'].split('_')[0]):c for c in M['cameras']};tags={b['id']:b['tags'] for b in K['buildings']}
ae=u.get_editor_subsystem(u.EditorActorSubsystem);world=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world();actors={a.static_mesh_component.static_mesh.get_name():a for a in ae.get_all_level_actors() if isinstance(a,u.StaticMeshActor) and a.static_mesh_component.static_mesh}
def vec(p):return u.Vector(p[0]*100,-p[1]*100,p[2]*100)
def hit_name(p,q):
 h=u.SystemLibrary.line_trace_single(world,vec(p),vec(q),u.TraceTypeQuery.ECC_VISIBILITY,True,[],u.DrawDebugTrace.NONE,True)
 if not h:return None
 a=h.to_tuple()[9]
 return a.static_mesh_component.static_mesh.get_name() if isinstance(a,u.StaticMeshActor) and a.static_mesh_component.static_mesh else str(a)
manual={
 'SM_Building_92379312':(89,'Gerdas / Castenska gården'),
 'SM_Kvarnholmen_House_91846928':(80,'Gamla varmbadhuset'),
 'SM_Kvarnholmen_House_91846968':(61,'Gamla brandstationen'),
 'SM_Kvarnholmen_House_91846944':(78,'Riskvarnen'),
 'SM_Kvarnholmen_House_91285828':(62,'Ångkvarnen – silodelen'),
 'SM_Kvarnholmen_House_91285833':(63,'Ångkvarnen – östra flygeln'),
 'SM_Kvarnholmen_House_91072716':(76,'Gamla vattentornet'),
 'SM_Kvarnholmen_House_93199604':(77,'Klapphuset'),
 'SM_Kvarnholmen_House_91846934':(85,'Hotell Witt – baksidan'),
 'SM_Kvarnholmen_House_91970263':(93,'Kullzénska huset'),
 'SM_Building_91846946':(94,'Areskogska huset'),
 'SM_Building_91970290':(92,'Storgatan – orange fasaden'),
 'SM_Kvarnholmen_House_92204207':(98,'Norra Långgatan – gräddfärgade hörnet'),
 'SM_Kvarnholmen_House_92204178':(99,'Norra Långgatan – rosa hörnet'),
 'SM_Kvarnholmen_House_92204173':(110,'Butikskvarteret – nordöstra hörnet'),
 'SM_Kvarnholmen_House_92204200':(101,'Larmgatan – vita hörnet'),
 'SM_Kvarnholmen_House_92204190':(102,'Norra Långgatan – klassiska vita huset'),
 'SM_Kvarnholmen_House_92204168':(103,'Norra Långgatan – keramiska fält'),
 'SM_Building_92204159':(104,'Gallerian – norra entrén'),
 'SM_Kvarnholmen_House_92204184':(106,'Kaggensgatan / Fiskaregatan – ljusa hörnet'),
 'SM_Kvarnholmen_House_92204157':(107,'Kaggensgatan 30'),
 'SM_Kvarnholmen_House_92204172':(108,'Larmgatan – tegelfasaden'),
}
items=[]
for name,d in D.items():
 assert name in actors,name
 a=actors[name];origin,extent=a.get_actor_bounds(False);height=max(d['H'],(origin.z+extent.z)/100);street=d['street'] or 'Övriga hus';title=tags.get(d['id'],{}).get('name') or (street+' · '+d['id']);item={'id':d['id'],'mesh':name,'street':street,'title':title,'category':'house','height_m':height,'reference_status':d.get('reference_status','')}
 if name in manual:
  ci,title=manual[name];c=C[ci];item.update(title=title,location=c['location'],target=c['target'],fov=math.degrees(2*math.atan(18/c['lens'])),view='Sparad fasadkamera',camera=c['name'])
 else:
  walls=sorted((w for w in d['walls'] if w['length']>1),key=lambda w:(bool(w['exposed']),w['frontage'],sum(b-a for a,b in w['exposed']),-w['road_distance']),reverse=True)[:3];candidates=[]
  for wall in walls:
   p,q=wall['p'],wall['q'];L=wall['length'];ux,uy=(q[0]-p[0])/L,(q[1]-p[1])/L;nx,ny=uy,-ux;mx,my=(p[0]+q[0])/2,(p[1]+q[1])/2
   H=max(3,min(height,d['H']*1.7+4));distance=max(8,L*.62,H*1.18)
   target=[mx,my,H*.47]
   samples=[[mx+ux*L*f-nx*.32,my+uy*L*f-ny*.32,z*H] for f in [-.32,0,.32] for z in [.26,.72]]
   for z in [2.5,H*.65,H+6,H+18]:
    for side in [0,.24,-.24]:
     loc=[mx+nx*distance+ux*L*side,my+ny*distance+uy*L*side,z]
     visible=sum(hit_name(loc,point)==name for point in samples)
     score=visible*30-z*.55-abs(side)*2+(5 if wall['frontage'] else 0)
     candidates.append((score,loc,target,visible,L,wall['street']))
  score,loc,target,visible,L,wallstreet=max(candidates,key=lambda c:c[0]);item.update(location=loc,target=target,fov=88,view='Upphöjd vy' if loc[2]>6 else 'Gatunivå',visibility_samples=visible,facade_width=L)
 items.append(item)
for name,ci,title in [('SM_Radhuset',23,'Rådhuset'),('SM_Calmar_Stadshotell',25,'Calmar Stadshotell'),('SM_Kalmar_Domkyrka_Part00',4,'Kalmar domkyrka'),('SM_Storgatan_Kalmar_Teater',44,'Kalmar teater'),('SM_Storgatan_Frimurarehotellet',43,'Frimurarehotellet')]:
 assert name in actors,name
 c=C[ci];items.append({'id':name,'mesh':name,'street':'Stortorget' if ci in [23,25,4] else 'Larmtorget','title':title,'category':'landmark','location':c['location'],'target':c['target'],'fov':math.degrees(2*math.atan(18/c['lens'])),'view':'Sparad fasadkamera','camera':c['name']})
items.sort(key=lambda d:(d['street'],d['title']))
for i,item in enumerate(items):item['index']=i;item['image']=f'hus/{i:04d}.jpg'
report={'count':len(items),'mapped_buildings':len(D),'items':items,'low_visibility':[d['id'] for d in items if d.get('visibility_samples',6)<4]}
(R/'media/houses-plan.json').write_text(json.dumps(report,indent=2,ensure_ascii=False));print('HOUSES_PLANNED',len(items),len(report['low_visibility']))
