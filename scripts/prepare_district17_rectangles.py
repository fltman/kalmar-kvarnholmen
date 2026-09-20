import sys,json,math
from pathlib import Path

from shapely.geometry import Polygon,LineString
R=Path(__file__).resolve().parents[1];p=R/'source/district17.json';d=json.loads(p.read_text());bs={}
for f in ['site','storgatan','kvarnholmen']:
 for b in json.loads((R/f'source/{f}.json').read_text())['buildings']:bs[b['id']]=b
for name,r in d['buildings'].items():
 b=bs[r['id']];ps=b.get('polygons',[{'outer':b.get('polygon'),'holes':b.get('holes',[])}]);poly=Polygon(ps[0]['outer'],ps[0]['holes'])
 if len(ps)!=1 or poly.interiors:continue
 rect=poly.minimum_rotated_rectangle;pts=list(rect.exterior.coords)[:4]
 if poly.area/rect.area<.965:continue
 lengths=[math.dist(pts[i],pts[(i+1)%4]) for i in range(4)];i=lengths.index(max(lengths));p0,p1=pts[i],pts[(i+1)%4];a=math.atan2(p1[1]-p0[1],p1[0]-p0[0]);c=rect.centroid
 r['roof_rectangle']=[c.x,c.y,max(lengths),min(lengths),a]
p.write_text(json.dumps(d,ensure_ascii=False,indent=2));print('RECT_ROOFS',sum('roof_rectangle'in r and r['action']=='rebuild' for r in d['buildings'].values()))
for bid in ['93238156','90859847','91926329','92379265','92412873']:
 r=d['buildings']['SM_Kvarnholmen_House_'+bid];print(bid,r['area'],r.get('roof_rectangle'),[(i,w['street'],round(w['length'],1),w['frontage']) for i,w in enumerate(r['walls']) if w['length']>10])
