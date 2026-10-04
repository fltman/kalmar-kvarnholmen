"""Pass 92: five generic pass-17 volumes on the west side of Landshövdingegatan, north of Storgatan,
split at measured joints:
- 93192387, the olive-green boarded corner house (Storgatan front, east gable on Landshövdingegatan),
  the pale green gate section at its west end and the low strip behind its main roof;
- 93192432, the ochre rendered three-storey house with the street gable in gambrel form;
- 93192395, the pink and brown stucco house with the arched gateway;
- 93192444, the red boarded house with its gable to the street (the carved gate south of it stands in
  the gap between the outlines and is built with this mesh) and its lower back wing;
- 93192382, the pink boarded two-storey house with the grey double door, and its low back wing.
Heights from four resected Google Street View panoramas (April 2025); see
references/block92-notes.md.
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
IDS=['93192387','93192432','93192395','93192444','93192382']
for i in IDS:
 b=d17['SM_Kvarnholmen_House_'+i];assert (b.get('detail_pass') or 17)<=17,(i,b.get('detail_pass'))
PG=lambda b:Polygon([tuple(w['p']) for w in d17['SM_Kvarnholmen_House_'+b]['walls']]).buffer(0)
C87,O32,S95,R44,P82=[PG(i) for i in IDS]
# Joints. 93192387: the gate section west of x 282.74 (pass 91's reading on the 63 Storgatan
# panorama, confirmed on the 65 panorama); the main roof ends at y 7.5, where the corner board and
# the foot of the east bargeboard stand on the 9 Landshövdingegatan panorama. 93192444: the street
# gable is the part east of x 283.0 (the outline's step); the narrower west part is a back wing.
# 93192382: the part west of x 287.36 (beside the outline's notch) is a back wing.
XB=lambda x0,x1,y0=-5,y1=60:box(x0,y0,x1,y1)
seeds=[('gt',C87.intersection(XB(270,282.74))),('og',C87.intersection(XB(282.74,300,-5,7.5))),('or',C87),
 ('oc',O32),('pk',S95),('rf',R44.intersection(XB(283.0,300))),('rb',R44),('pb',P82.intersection(XB(287.36,300))),('pw',P82)]
# Heights (m) above the pavement, read on the facade plane 0.355 m in front of the outline.
spec={'gt':dict(height=3.6,top=3.7,mesh='SM_Kvarnholmen_House_93192387',roof='flat'),
 'og':dict(height=5.35,top=8.2,mesh='SM_Kvarnholmen_House_93192387',roof='saddle'),
 'or':dict(height=5.0,top=5.3,mesh='SM_Kvarnholmen_House_93192387',roof='lean'),
 'oc':dict(height=6.1,top=8.45,brk=8.3,mesh='SM_Kvarnholmen_House_93192432',roof='gambrel_x'),
 'pk':dict(height=11.4,top=15.6,mesh='SM_Kvarnholmen_House_93192395',roof='saddle'),
 'rf':dict(height=5.4,top=7.0,mesh='SM_Kvarnholmen_House_93192444',roof='saddle_x'),
 'rb':dict(height=3.6,top=5.0,mesh='SM_Kvarnholmen_House_93192444',roof='saddle_x'),
 'pb':dict(height=6.2,top=10.7,mesh='SM_Kvarnholmen_House_93192382',roof='saddle'),
 'pw':dict(height=3.2,top=3.6,mesh='SM_Kvarnholmen_House_93192382',roof='lean')}
taken=Polygon();zones={}
for name,seed in seeds:
 ps=parts(seed.difference(taken));zones[name]=ps;taken=unary_union([taken]+ps)
assert all(zones[k] for k in zones),{k:len(v) for k,v in zones.items()}
scope=set(IDS)
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
foot=unary_union([C87,O32,S95,R44,P82]);covered=unary_union([p for ps in zones.values() for p in ps])
data={'source':'district volumes '+', '.join(IDS)+' (source/district17.json), '+district['source'],'zones':out,
 'checks':{'footprint_m2':round(foot.area,1),'zoned_m2':round(covered.area,1),'outside_osm_m2':round(covered.difference(foot).area,2),'osm_not_zoned_m2':round(foot.difference(covered).area,2),
  'overlap_m2':round(sum(p.area for ps in zones.values() for p in ps)-covered.area,3)}}
(R/'source/block92.json').write_text(json.dumps(data,indent=1,ensure_ascii=False))
c=data['checks'];ok=c['outside_osm_m2']<.2 and c['osm_not_zoned_m2']<.5 and c['overlap_m2']<.2
(R/'previews/block92-zones.json').write_text(json.dumps({'status':'passed' if ok else 'review_required','zones':report,'checks':c},indent=2,ensure_ascii=False))
print(json.dumps(report));print(c);print('BLOCK92_ZONES_OK' if ok else 'BLOCK92_ZONES_REVIEW')
