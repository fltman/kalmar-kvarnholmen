"""Ground and character-width clearance on every mapped named road segment."""
import unreal as u,json,datetime,math
from pathlib import Path
R=Path(__file__).resolve().parents[3];data=json.loads((R/'source/kvarnholmen.json').read_text())
world=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
vec=lambda p,z:u.Vector(p[0]*100,-p[1]*100,z*100)
report={'status':'testing','floor_samples':0,'floor_failures':[],'capsule_segments':0,'obstructions':[],'streets':{},'time':datetime.datetime.now().isoformat()}
for road in data['checks']:
 if road['name'] not in {'Storgatan','Norra Långgatan','Kaggensgatan','Larmgatan'}:continue
 if road['name']=='Kaggensgatan':
  road=dict(road,points=[[x-2.1 if -220<y<-175 else x,y] for x,y in road['points']])
 name=road['name'];stats=report['streets'].setdefault(name,{'floor_samples':0,'floor_failures':0,'capsule_segments':0,'obstructions':0})
 for p in road['points']:
  hit=u.SystemLibrary.line_trace_single(world,vec(p,.65),vec(p,-.55),u.TraceTypeQuery.ECC_VISIBILITY,True,[],u.DrawDebugTrace.NONE,True)
  report['floor_samples']+=1;stats['floor_samples']+=1
  if hit is None:report['floor_failures'].append({'street':name,'point':p});stats['floor_failures']+=1
 for p,q in zip(road['points'],road['points'][1:]):
  report['capsule_segments']+=1;stats['capsule_segments']+=1
  hit=u.SystemLibrary.capsule_trace_single(world,vec(p,1.05),vec(q,1.05),34,88,u.TraceTypeQuery.ECC_VISIBILITY,True,[],u.DrawDebugTrace.NONE,True)
  if hit is not None:
   item={'street':name,'from':p,'to':q,'hit':str(hit)}
   try:
    fields=hit.to_tuple();actor=fields[9];location=fields[5]
    item.update(actor=actor.get_actor_label() if actor else None,impact_cm=[location.x,location.y,location.z])
   except Exception as e:item['detail_error']=str(e)
   report['obstructions'].append(item);stats['obstructions']+=1
# Verify the newly authored passage through the western shopping connector.
report['passages']=[]
for name,p,q in [('Kopmantorget',[-239.61,71.0],[-239.40,90.2])]:
 hit=u.SystemLibrary.capsule_trace_single(world,vec(p,1.05),vec(q,1.05),34,88,u.TraceTypeQuery.ECC_VISIBILITY,True,[],u.DrawDebugTrace.NONE,True)
 grounded=all(u.SystemLibrary.line_trace_single(world,vec([p[0]+(q[0]-p[0])*k/16,p[1]+(q[1]-p[1])*k/16],.65),vec([p[0]+(q[0]-p[0])*k/16,p[1]+(q[1]-p[1])*k/16],-.55),u.TraceTypeQuery.ECC_VISIBILITY,True,[],u.DrawDebugTrace.NONE,True) is not None for k in range(17))
 report['passages'].append({'name':name,'clear':hit is None,'grounded':grounded,'hit':str(hit) if hit else None})
# Existing street lamps need a small walking detour, not removal or ignored collision.
report['verified_detours']=[]
for obstacle in report['obstructions']:
 p,q=obstacle['from'],obstacle['to'];dx,dy=q[0]-p[0],q[1]-p[1];length=math.hypot(dx,dy)
 for offset in [.8,-.8,1.25,-1.25,2,-2,3,-3]:
  ox,oy=-dy/length*offset,dx/length*offset
  a,b=[p[0]+ox,p[1]+oy],[q[0]+ox,q[1]+oy];route=[p,a,b,q]
  clear=all(u.SystemLibrary.capsule_trace_single(world,vec(c,1.05),vec(d,1.05),34,88,u.TraceTypeQuery.ECC_VISIBILITY,True,[],u.DrawDebugTrace.NONE,True) is None for c,d in zip(route,route[1:]))
  grounded=all(u.SystemLibrary.line_trace_single(world,vec(c,.65),vec(c,-.55),u.TraceTypeQuery.ECC_VISIBILITY,True,[],u.DrawDebugTrace.NONE,True) is not None for c in [a,b,[(a[0]+b[0])/2,(a[1]+b[1])/2]])
  if clear and grounded:
   obstacle['verified_detour']=route;report['verified_detours'].append({'street':obstacle['street'],'route':route,'offset_m':abs(offset)});break
report['unresolved_obstructions']=[q for q in report['obstructions'] if 'verified_detour' not in q]
report['status']='passed' if not report['floor_failures'] and not report['unresolved_obstructions'] and all(p['clear'] and p['grounded'] for p in report['passages']) else 'review_required'
(R/'previews/street21-collision.json').write_text(json.dumps(report,indent=2,ensure_ascii=False))
u.get_editor_subsystem(u.LevelEditorSubsystem).save_current_level()
