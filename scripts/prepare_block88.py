"""Pass 88: five generic pass-17 volumes in the south-west of Kvarnholmen, split into eleven parts:
- Ölandsgatan 7 (92379283): the pale green boarded house with the arched carriage gate;
- Södra Vallgatan 15 (92379259): the white boarded house with the entrance bay, and its rear wing;
- 91856598 on Södra Vallgatan: the small brown boarded building (west 4.85 m) and the yellow boarded
  house east of it (the rest of the outline);
- 91856586 on Södra Vallgatan: the white functionalist house, as its taller west part with the bay
  and the round window, its lower east part with the roof terrace, and the rear;
- 91856600 on Larmgatan: the green boarded pavilion, the glazed café and the white-framed
  conservatory at its south end.
Heights from Google Street View panoramas (April 2025); see references/block88-notes.md.
"""
from pathlib import Path
import json,math,os,sys
if os.environ.get('KALMAR_GEO'):sys.path.insert(0,os.environ['KALMAR_GEO'])
from shapely.geometry import Polygon,Point
from shapely.geometry.polygon import orient
from shapely.ops import unary_union
R=Path(__file__).resolve().parents[1]
district=json.loads((R/'source/kvarnholmen.json').read_text())
d17=json.loads((R/'source/district17.json').read_text())['buildings']
def flat(g):
 g=g.buffer(0);return [g] if g.geom_type=='Polygon' else [q for c in getattr(g,'geoms',[]) for q in flat(c)]
def parts(g):return [orient(r) for q in flat(g) for r in flat(q.buffer(-.02,join_style=2).buffer(.02,join_style=2).simplify(.02)) if r.area>1.0]
PG=lambda b:Polygon([tuple(w['p']) for w in d17['SM_Kvarnholmen_House_'+b]['walls']]).buffer(0)
OL,SV,BY,WF,PV=PG('92379283'),PG('92379259'),PG('91856598'),PG('91856586'),PG('91856600')
def band(a,b,depth,s0=-60,s1=60):
 # The strip behind the street front a-b between s0 and s1 along it (inwards: left of a->b).
 L=math.dist(a,b);dx,dy=(b[0]-a[0])/L,(b[1]-a[1])/L;nx,ny=-dy,dx
 return Polygon([(a[0]+dx*s+nx*t,a[1]+dy*s+ny*t) for s,t in ((s0,-.5),(s1,-.5),(s1,depth),(s0,depth))])
# Street fronts (OSM vertices), west to east, or north to south on Larmgatan.
F15=((-156.11,-172.16),(-143.93,-172.03))
FBY=((-254.69,-171.87),(-239.78,-172.07))
FWF=((-268.18,-171.68),(-254.69,-171.87))
FPV=((-283.75,-195.06),(-284.16,-214.36))
seeds=[('ol',OL),
 # Södra Vallgatan 15: the main range is the full width of the front, 9.35 m deep (to the step in
 # the outline); the narrow rear wing beyond.
 ('sv',SV.intersection(band(*F15,9.35,-5,12.19))),('sw',SV),
 # 91856598: the brown building is the west 4.85 m of the front (measured edge), the yellow house
 # the rest.
 ('br',BY.intersection(band(*FBY,30,-5,4.85))),('yl',BY),
 # 91856586: the taller west part with the bay ends 6.4 m along the front (measured), the lower east
 # part runs to the end; both 10 m deep (estimated), the rear behind.
 ('wt',WF.intersection(band(*FWF,10,-5,6.4))),('wr',WF.intersection(band(*FWF,10,6.4,30))),('wb',WF),
 # Larmgatan: the green pavilion is the north 6.8 m of the west front, the conservatory the south
 # 4.3 m (from s 15.0), the glazed café between.
 ('pg',PV.intersection(band(*FPV,30,-5,6.8))),('pv',PV.intersection(band(*FPV,30,15.0,30))),('pc',PV)]
# Heights (m) above the facade base: eaves measured on the resected panoramas; ridges, the west
# part of 91856586 and the rear parts estimated (see the notes).
spec={'ol':dict(height=6.2,top=12.2,mesh='SM_Kvarnholmen_House_92379283',roof='saddle'),
 'sv':dict(height=6.45,top=9.6,mesh='SM_Kvarnholmen_House_92379259',roof='saddle'),
 'sw':dict(height=6.0,top=6.2,mesh='SM_Kvarnholmen_House_92379259',roof='flat'),
 'br':dict(height=4.7,top=4.85,mesh='SM_Kvarnholmen_House_91856598',roof='flat'),
 'yl':dict(height=6.2,top=9.0,mesh='SM_Kvarnholmen_House_91856598',roof='hip'),
 'wt':dict(height=10.8,top=11.0,mesh='SM_Kvarnholmen_House_91856586',roof='flat'),
 'wr':dict(height=7.05,top=7.25,mesh='SM_Kvarnholmen_House_91856586',roof='flat'),
 'wb':dict(height=7.05,top=7.25,mesh='SM_Kvarnholmen_House_91856586',roof='flat'),
 'pg':dict(height=3.0,top=4.4,mesh='SM_Kvarnholmen_House_91856600',roof='hip'),
 'pc':dict(height=3.2,top=3.35,mesh='SM_Kvarnholmen_House_91856600',roof='flat'),
 'pv':dict(height=2.9,top=3.05,mesh='SM_Kvarnholmen_House_91856600',roof='flat')}
taken=Polygon();zones={}
for name,seed in seeds:
 ps=parts(seed.difference(taken));zones[name]=ps;taken=unary_union([taken]+ps)
scope={'92379283','92379259','91856598','91856586','91856600'}
others=[(Polygon([tuple(w['p']) for w in v['walls']]).buffer(0),v['H'],v['id']) for v in d17.values() if v['id'] not in scope and len(v['walls'])>=3]
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
foot=unary_union([OL,SV,BY,WF,PV]);covered=unary_union([p for ps in zones.values() for p in ps])
data={'source':'district volumes 92379283, 92379259, 91856598, 91856586 and 91856600 (source/district17.json), '+district['source'],
 'fronts':{'ol':[[-117.34,-140.61],[-106.09,-140.45]],'sv':F15,'by':FBY,'wf':FWF,'pv':FPV},'zones':out,
 'checks':{'footprint_m2':round(foot.area,1),'zoned_m2':round(covered.area,1),'outside_osm_m2':round(covered.difference(foot).area,2),'osm_not_zoned_m2':round(foot.difference(covered).area,2),
  'overlap_m2':round(sum(p.area for ps in zones.values() for p in ps)-covered.area,3)}}
(R/'source/block88.json').write_text(json.dumps(data,indent=1,ensure_ascii=False))
c=data['checks'];ok=c['outside_osm_m2']<.2 and c['osm_not_zoned_m2']<.5 and c['overlap_m2']<.2 and all(zones[k] for k in spec)
(R/'previews/block88-zones.json').write_text(json.dumps({'status':'passed' if ok else 'review_required','zones':report,'checks':c},indent=2,ensure_ascii=False))
print(json.dumps(report));print(c);print('BLOCK88_ZONES_OK' if ok else 'BLOCK88_ZONES_REVIEW')
