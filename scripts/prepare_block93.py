"""Pass 93: the east side of Landshövdingegatan between the cross street at y -12..0 and y 51 (fronts
face west). Six generic pass-17 volumes are split into zones:
- 93199599 (3 Landshövdingegatan): the yellow rendered three-storey corner house with the chamfered
  corner, one zone over its outline;
- 93238178 (7 Landshövdingegatan): the taupe rendered two-storey corner house, one zone;
- 93238200: the light grey boarded house with the garage door, and a low annex on its back bump;
- 93238168: the green-grey boarded house with the red garage door, and a low annex on its back bump;
- 93238182: the red boarded house: the gable wing to the street, the low south piece beside it,
  and the low outbuildings along the yard behind;
- 93238147: the brown boarded house with the gambrel gable to the street, and the low yard
  buildings behind it.
Heights from four Google Street View panoramas (heading 62); see references/block93-notes.md.
"""
from pathlib import Path
import json,math,os,sys
if os.environ.get('KALMAR_GEO'):sys.path.insert(0,os.environ['KALMAR_GEO'])
from shapely.geometry import Polygon,Point,box
from shapely.geometry.polygon import orient
from shapely.ops import unary_union
R=Path(__file__).resolve().parents[1]
district=json.loads((R/'source/kvarnholmen.json').read_text())
d17=json.loads((R/'source/district17.json').read_text())['buildings']
def flat(g):
 g=g.buffer(0);return [g] if g.geom_type=='Polygon' else [q for c in getattr(g,'geoms',[]) for q in flat(c)]
def parts(g):return [orient(r) for q in flat(g) for r in flat(q.buffer(-.02,join_style=2).buffer(.02,join_style=2).simplify(.02)) if r.area>1.0]
IDS=['93199599','93238178','93238200','93238168','93238182','93238147']
PG={i:Polygon([tuple(w['p']) for w in d17['SM_Kvarnholmen_House_'+i]['walls']]).buffer(0) for i in IDS}
MS=lambda i:'SM_Kvarnholmen_House_'+i
# Zone seeds, in order (each takes what is left of its house). Cuts follow the outlines: the main
# houses stand on the street; bumps and yard ranges behind them are low annexes.
seeds=[('yl',PG['93199599']),
 ('ta',PG['93238178']),
 ('lg',PG['93238200'].intersection(box(300,0,316.7,30))),('lgb',PG['93238200']),
 ('gg',PG['93238168'].intersection(box(300,0,316.9,40))),('ggb',PG['93238168']),
 ('rs',PG['93238182'].intersection(box(300,30,312,35.45))),('rg',PG['93238182'].intersection(box(300,35.45,317.4,45))),('rw',PG['93238182']),
 ('bg',PG['93238147'].intersection(box(300,42,315.8,52))),('bw',PG['93238147'])]
# Heights (m) above the facade base: eaves or wall top (height) and ridge (top). Measured on the
# resected panoramas where the notes say so; the yard annexes are estimates.
spec={'yl':dict(height=10.8,top=13.4,mesh=MS('93199599'),roof='inset'),
 'ta':dict(height=7.3,top=8.5,mesh=MS('93238178'),roof='inset'),
 'lg':dict(height=6.25,top=8.65,mesh=MS('93238200'),roof='saddle_s'),
 'lgb':dict(height=3.0,top=3.2,mesh=MS('93238200'),roof='flat'),
 'gg':dict(height=6.2,top=7.8,mesh=MS('93238168'),roof='saddle_s'),
 'ggb':dict(height=3.0,top=3.2,mesh=MS('93238168'),roof='flat'),
 'rs':dict(height=4.8,top=5.9,mesh=MS('93238182'),roof='saddle_s'),
 'rg':dict(height=4.5,top=6.6,mesh=MS('93238182'),roof='saddle_t'),
 'rw':dict(height=3.0,top=3.2,mesh=MS('93238182'),roof='flat'),
 'bg':dict(height=3.1,top=7.4,mesh=MS('93238147'),roof='gambrel'),
 'bw':dict(height=3.0,top=3.2,mesh=MS('93238147'),roof='flat')}
taken=Polygon();zones={}
for name,seed in seeds:
 ps=parts(seed.difference(taken));zones[name]=ps;taken=unary_union([taken]+ps)
others=[(Polygon([tuple(w['p']) for w in v['walls']]).buffer(0),v['H'],v['id']) for v in d17.values() if v['id'] not in IDS and len(v['walls'])>=3]
def neighbour_at(pt):
 for name,ps in zones.items():
  if any(p.buffer(.001).contains(pt) for p in ps):return name,spec[name]['height']
 for g,h,bid in others:
  if g.buffer(.001).contains(pt):return bid,h
 return None,0.0
out={};report={}
for name,ps in zones.items():
 H=spec[name]['height'];walls=[]
 for poly in ps:
  cs=list(poly.exterior.coords)[:-1]
  for p,q in zip(cs,cs[1:]+cs[:1]):
   Lw=math.dist(p,q)
   if Lw<.05:continue
   wx,wy=(q[0]-p[0])/Lw,(q[1]-p[1])/Lw;nx,ny=wy,-wx;n=max(1,int(Lw/.2));runs=[]
   for k in range(n):
    t=(k+.5)/n;nb,h=neighbour_at(Point(p[0]+wx*Lw*t+nx*.3,p[1]+wy*Lw*t+ny*.3))
    if runs and runs[-1][0]==nb:runs[-1][3]=(k+1)/n
    else:runs.append([nb,h,k/n,(k+1)/n])
   for nb,h,t0,t1 in runs:
    z0=0.0 if nb is None else h
    if z0>=H-.05:continue
    a=(round(p[0]+wx*Lw*t0,3),round(p[1]+wy*Lw*t0,3));b=(round(p[0]+wx*Lw*t1,3),round(p[1]+wy*Lw*t1,3))
    if math.dist(a,b)<.2:continue
    walls.append({'p':list(a),'q':list(b),'z0':z0,'z1':H,'kind':'outer' if nb is None else 'upper','neighbour':nb})
 out[name]=dict(spec[name],polygons=[[list(v) for v in list(p.exterior.coords)[:-1]] for p in ps],walls=walls)
 report[name]={'area_m2':round(sum(p.area for p in ps),1),'polygons':len(ps),'walls':len(walls),'outer_m':round(sum(math.dist(w['p'],w['q']) for w in walls if w['kind']=='outer'),1)}
foot=unary_union(list(PG.values()));covered=unary_union([p for ps in zones.values() for p in ps])
data={'source':'district volumes '+', '.join(IDS)+' (source/district17.json), '+district['source'],'zones':out,
 'checks':{'footprint_m2':round(foot.area,1),'zoned_m2':round(covered.area,1),'outside_osm_m2':round(covered.difference(foot).area,2),'osm_not_zoned_m2':round(foot.difference(covered).area,2),
  'overlap_m2':round(sum(p.area for ps in zones.values() for p in ps)-covered.area,3)}}
(R/'source/block93.json').write_text(json.dumps(data,indent=1,ensure_ascii=False))
c=data['checks'];ok=c['outside_osm_m2']<.2 and c['osm_not_zoned_m2']<.5 and c['overlap_m2']<.2 and all(zones[k] for k in zones)
(R/'previews/block93-zones.json').write_text(json.dumps({'status':'passed' if ok else 'review_required','zones':report,'checks':c},indent=2,ensure_ascii=False))
print(json.dumps(report));print(c);print('BLOCK93_ZONES_OK' if ok else 'BLOCK93_ZONES_REVIEW')
