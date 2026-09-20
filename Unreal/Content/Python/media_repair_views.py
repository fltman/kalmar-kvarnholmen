"""Repair photo cameras that lie inside another mapped building."""
import unreal as u,json,math
from pathlib import Path
R=Path(__file__).resolve().parents[3]
D=json.loads((R/'source/district17.json').read_text())['buildings']
plan=json.loads((R/'media/houses-plan.json').read_text())
ae=u.get_editor_subsystem(u.EditorActorSubsystem);world=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
actors={a.static_mesh_component.static_mesh.get_name():a for a in ae.get_all_level_actors() if isinstance(a,u.StaticMeshActor) and a.static_mesh_component.static_mesh}
heights={}
for name,d in D.items():
 o,e=actors[name].get_actor_bounds(False);heights[name]=max(d['H']+2,(o.z+e.z)/100)
def inside(p,d):
 x,y=p[:2]
 return sum((w['p'][1]>y)!=(w['q'][1]>y) and x<(w['q'][0]-w['p'][0])*(y-w['p'][1])/(w['q'][1]-w['p'][1])+w['p'][0] for w in d['walls'])%2

def blockers(p):return [n for n,d in D.items() if p[2]<heights[n]+1 and inside(p,d)]
def vec(p):return u.Vector(p[0]*100,-p[1]*100,p[2]*100)
def hit_name(p,q):
 h=u.SystemLibrary.line_trace_single(world,vec(p),vec(q),u.TraceTypeQuery.ECC_VISIBILITY,True,[],u.DrawDebugTrace.NONE,True)
 if not h:return None
 a=h.to_tuple()[9]
 return a.static_mesh_component.static_mesh.get_name() if isinstance(a,u.StaticMeshActor) and a.static_mesh_component.static_mesh else None
repairs=[]
for item in plan['items']:
 if item['category']!='house' or item.get('camera'):continue
 bad=blockers(item['location'])
 if not bad and item['index']!=26:continue
 name=item['mesh'];d=D[name];H=max(3,min(item['height_m'],d['H']*1.7+4));candidates=[]
 walls=sorted((w for w in d['walls'] if w['length']>1),key=lambda w:(bool(w['exposed']),w['frontage'],sum(b-a for a,b in w['exposed']),-w['road_distance']),reverse=True)[:4]
 for wall in walls:
  p,q=wall['p'],wall['q'];L=wall['length'];ux,uy=(q[0]-p[0])/L,(q[1]-p[1])/L;nx,ny=uy,-ux;mx,my=(p[0]+q[0])/2,(p[1]+q[1])/2
  distance=max(8,L*.62,H*1.18);target=[mx,my,H*.47]
  samples=[[mx+ux*L*f-nx*.32,my+uy*L*f-ny*.32,z*H] for f in [-.32,0,.32] for z in [.26,.72]]
  for factor in [1,.68]:
   for z in [3,H*.7,H+7,H+20,H+36]:
    for side in [0,.24,-.24]:
     loc=[mx+nx*distance*factor+ux*L*side,my+ny*distance*factor+uy*L*side,z]
     if blockers(loc):continue
     visible=sum(hit_name(loc,point)==name for point in samples)
     score=visible*30-z*.38-abs(side)*2+(5 if wall['frontage'] else 0)-(5 if factor<1 else 0)
     candidates.append((score,loc,target,visible,L))

 if not candidates:raise RuntimeError('No free camera for '+name)
 score,loc,target,visible,L=max(candidates,key=lambda c:c[0]);old=item['location'];item.update(location=loc,target=target,fov=88,view='Upphöjd vy' if loc[2]>6 else 'Gatunivå',visibility_samples=visible,facade_width=L)
 repairs.append({'index':item['index'],'title':item['title'],'old':old,'location':loc,'blockers':bad})
# The whole hotel is more useful than its sign-detail camera.
C={int(c['name'].split('_')[0]):c for c in json.loads((R/'exports/manifest.json').read_text())['cameras']}
item=next(i for i in plan['items'] if i['title']=='Frimurarehotellet');c=C[39];old=item['location'];item.update(location=c['location'],target=c['target'],fov=math.degrees(2*math.atan(18/c['lens'])),camera=c['name']);repairs.append({'index':item['index'],'title':item['title'],'old':old,'location':c['location']})
for title,loc,target,fov in [('Ångkvarnen – östra flygeln',[365,-115,18],[289,-114,13],82),('Gamla vattentornet',[-395,76,16],[-331,122,31],85)]:
 item=next(i for i in plan['items'] if i['title']==title);old=item['location'];item.update(location=loc,target=target,fov=fov,view='Upphöjd vy');repairs.append({'index':item['index'],'title':title,'old':old,'location':loc})
overrides=R/'source/media_camera_overrides.json'
if overrides.exists():
 by_id=json.loads(overrides.read_text())
 for item in plan['items']:
  if item['id'] in by_id:item.update(by_id[item['id']])
(R/'media/houses-plan.json').write_text(json.dumps(plan,indent=2,ensure_ascii=False))
(R/'media/view-repairs.json').write_text(json.dumps(repairs,indent=2,ensure_ascii=False))
print('REPAIRED_VIEWS',len(repairs))
