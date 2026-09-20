from pathlib import Path
import json,sys

from shapely.geometry import Polygon,box
from shapely import constrained_delaunay_triangles
R=Path(__file__).resolve().parents[1];d=json.loads((R/'source/kvarnholmen.json').read_text());site=json.loads((R/'source/site.json').read_text());out={}
for bid,H,axis,centre,half,rise in [('91846934',10.2,'y',-85,6,0),('91846979',9.5,'y',-87,6.2,2.5),('91846996',5.65,'x',158.355,2.879,1.5),('91846952',3.05,'y',-85.3,3.45,3.0),('91846951',6.25,'y',-63.5,5.75,3.4)]:
 b=next((b for b in d['buildings'] if b['id']==bid),None)
 poly=b['polygons'][0]['outer'] if b else next(b['polygon'] for b in site['buildings'] if b['id']==bid)
 g=Polygon(poly);lo,hi=(g.bounds[0],g.bounds[2]) if axis=='x' else (g.bounds[1],g.bounds[3]);cuts=sorted(set([lo,hi]+[p for p in [centre-half,centre,centre+half] if lo<p<hi]));roof=[]
 for low,high in zip(cuts,cuts[1:]):
  cell=box(low,-1000,high,1000) if axis=='x' else box(-1000,low,1000,high);q=g.intersection(cell)
  parts=[q] if q.geom_type=='Polygon' else list(getattr(q,'geoms',[]))
  for part in parts:
   if part.area<1e-5:continue
   for t in constrained_delaunay_triangles(part).geoms:
    roof.append([[x,y,H+rise*max(0,1-abs((x if axis=='x' else y)-centre)/half)] for x,y in list(t.exterior.coords)[:3]])
 out[bid]={'polygon':poly,'height':H,'roof':roof,'axis':axis,'centre':centre,'half':half,'rise':rise}
(R/'source/sodra-facades.json').write_text(json.dumps(out,indent=2))
