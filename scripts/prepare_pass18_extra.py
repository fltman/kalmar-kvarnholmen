from pathlib import Path
import json,sys,math,subprocess

from shapely.geometry import Polygon,box,Point
from shapely import constrained_delaunay_triangles
R=Path(__file__).resolve().parents[1];D=json.loads((R/'source/pass18.json').read_text());site={b['id']:b for b in json.loads((R/'source/site.json').read_text())['buildings']}
D['town']={bid:site[bid] for bid in ['92412866','92412857','92412842','92412870']};D['barometern']=site['92379310'];D['witt']=json.loads((R/'source/sodra-facades.json').read_text())['91846934']
def parts(g):return [g] if g.geom_type=='Polygon' else [p for c in getattr(g,'geoms',[]) for p in parts(c)]
for bid,b in D['town'].items():
 p=b['polygon'];edge=max(zip(p,p[1:]+p[:1]),key=lambda ab:(ab[0][1]+ab[1][1])/2);x0,x1=sorted([edge[0][0],edge[1][0]]);y1=max(v[1] for v in p);y0=min(v[1] for v in p);depth=min(y1-y0,12.5);H={'92412866':6,'92412857':8.4,'92412842':7.6,'92412870':10}[bid];rise=2.9 if bid=='92412866' else 4.;g=Polygon(p);out=[]
 # Clipped ridged shell: no rectangular footprint extends into a neighbour's front or courtyard.
 for ylo,yhi,rr in [(y1-depth,y1,rise),(y0,y1-depth,2.3)]:
  if yhi-ylo<.1:continue
  mid=(ylo+yhi)/2
  for lo,hi in [(ylo,mid),(mid,yhi)]:
   for part in parts(g.intersection(box(-10000,lo,10000,hi))):
    for t in constrained_delaunay_triangles(part).geoms:
     if t.area>.001:out.append([(x,y,H+rr*(1-abs(y-mid)/((yhi-ylo)/2))) for x,y in list(t.exterior.coords)[:3]])
 b['front_bounds']=[x0,x1,y0,y1];b['roof18']=out
D['witt']['parts18']=[]
g=Polygon(D['witt']['polygon'])
for region,H in [(box(-10000,-119,10000,10000),10.2),(box(-10000,-10000,10000,-119),6.8)]:
 for p in parts(g.intersection(region)):D['witt']['parts18'].append({'outer':list(p.exterior.coords)[:-1],'height':H})
(R/'source/pass18.json').write_text(json.dumps(D,ensure_ascii=False,indent=2))
back=R/'source/backups/detail-pass-17'
for n in ['SM_Building_'+bid for bid in list(D['town'])+['92379310']]+['SM_Kvarnholmen_House_91846934']:
 for f in ['exports/meshes/'+n+'.fbx','Unreal/Content/Kalmar/Meshes/'+n+'.uasset']:
  p=R/f;q=back/f
  if p.exists() and not q.exists():q.parent.mkdir(parents=True,exist_ok=True);subprocess.run(['cp','-c',str(p),str(q)],check=True)
print('EXTRA_PREPARED')
