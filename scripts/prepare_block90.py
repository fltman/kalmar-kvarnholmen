"""Pass 90: the north side of east Storgatan between Proviantgatan and the brick corner house: five
generic pass-17 volumes (93192351, 93192354, 93192423, 93192353, 93192374) split into ten parts:
- 93192351: the red boarded cottage (front range 7.2 m deep under a hipped tile roof) and the low
  rear part behind it;
- 93192354: the boarded pair, split at its measured middle joint into the grey west half (vertical
  boards) and the white east half (horizontal boards);
- 93192423: the cream boarded two-storey front range (6.3 m deep) and the rear wing;
- 93192353: the ochre rendered house with its gable on the street (the whole outline);
- 93192374: the boarded gate link at the west end (the first 3.4 m of the front, 6 m deep), the
  three-storey brick and stucco house (from x 238.5, 10.4 m deep) and the rear parts behind.
Heights from Google Street View panoramas (April 2025); see references/block90-notes.md.
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
IDS=('93192351','93192354','93192423','93192353','93192374')
PG=lambda b:Polygon([tuple(w['p']) for w in d17['SM_Kvarnholmen_House_'+b]['walls']]).buffer(0)
C51,P54,C23,O53,B74=[PG(i) for i in IDS]
# Street fronts (OSM vertices, west to east). The model x axis runs along Storgatan here, so the
# zones are cut with axis-aligned boxes.
FRONTS={'51':((188.3,0.5),(197.7,0.7)),'54':((200.0,0.5),(216.9,0.5)),'23':((216.9,0.5),(228.7,0.4)),
 '53':((228.7,0.4),(235.1,0.4)),'74':((235.1,0.4),(253.6,0.3))}
# Measured joints: the pair 93192354 meets at x 208.45 (the middle of its front, confirmed by the
# mirror-symmetric window rows); the brick house starts at x 238.5, the link west of it is 6 m deep
# (estimated). The cottage's front range is 7.2 m deep and the brick range 10.4 m (the step in the
# OSM outline); both estimated from the roof forms.
seeds=[('cf',C51.intersection(box(180,-1,200,7.7))),('cr',C51),
 ('pg',P54.intersection(box(195,-1,208.45,12))),('pw',P54),
 ('kf',C23.intersection(box(215,-1,230,6.75))),('kr',C23),
 ('og',O53),
 ('lk',B74.intersection(box(234,-1,238.5,6.0))),('bk',B74.intersection(box(238.5,-1,256,10.4))),('br',B74)]
# Heights (m) above the facade base. Eaves measured on the resected panoramas (camera 2.4 m);
# ridges and the rear parts estimated (see the notes).
M_={'c':'SM_Kvarnholmen_House_93192351','p':'SM_Kvarnholmen_House_93192354','k':'SM_Kvarnholmen_House_93192423',
 'o':'SM_Kvarnholmen_House_93192353','l':'SM_Kvarnholmen_House_93192374','b':'SM_Kvarnholmen_House_93192374'}
spec={'cf':dict(height=2.95,top=6.9,roof='hip'),'cr':dict(height=3.0,top=3.15,roof='flat'),
 'pg':dict(height=6.75,top=9.9,roof='saddle'),'pw':dict(height=6.75,top=9.9,roof='saddle'),
 'kf':dict(height=6.25,top=8.9,roof='saddle'),'kr':dict(height=6.0,top=6.2,roof='flat'),
 'og':dict(height=3.95,top=6.05,roof='gable'),
 'lk':dict(height=3.6,top=3.75,roof='flat'),'bk':dict(height=13.2,top=15.2,roof='saddle'),'br':dict(height=6.5,top=6.7,roof='flat')}
for k in spec:spec[k]['mesh']=M_[k[0]]
taken=Polygon();zones={}
for name,seed in seeds:
 ps=parts(seed.difference(taken));zones[name]=ps;taken=unary_union([taken]+ps)
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
foot=unary_union([C51,P54,C23,O53,B74]);covered=unary_union([p for ps in zones.values() for p in ps])
data={'source':'district volumes '+', '.join(IDS)+' (source/district17.json), '+district['source'],'fronts':FRONTS,'zones':out,
 'checks':{'footprint_m2':round(foot.area,1),'zoned_m2':round(covered.area,1),'outside_osm_m2':round(covered.difference(foot).area,2),'osm_not_zoned_m2':round(foot.difference(covered).area,2),
  'overlap_m2':round(sum(p.area for ps in zones.values() for p in ps)-covered.area,3)}}
(R/'source/block90.json').write_text(json.dumps(data,indent=1,ensure_ascii=False))
c=data['checks'];ok=c['outside_osm_m2']<.2 and c['osm_not_zoned_m2']<.5 and c['overlap_m2']<.2 and all(zones[k] for k in zones)
(R/'previews/block90-zones.json').write_text(json.dumps({'status':'passed' if ok else 'review_required','zones':report,'checks':c},indent=2,ensure_ascii=False))
print(json.dumps(report));print(c);print('BLOCK90_ZONES_OK' if ok else 'BLOCK90_ZONES_REVIEW')
