"""Pass 106: the north side of Södra Långgatan from 60 Södra Långgatan to Sjöfartsmuseet, and both
sides of the south end of Landshövdingegatan. Eight generic pass-17 volumes are split into zones:
- 91928568 (60 Södra Långgatan): the brick-and-stucco two-storey house: the street range and the
  lower back wing;
- 91928594 (the corner of Landshövdingegatan): the ochre roughcast two-storey house and its small
  back bump;
- 93199647: the grey boarded shed with the garage door (the Sjöfartsmuseum sign), one zone;
- 93199649 (Sjöfartsmuseet): the grey stucco neo-renaissance house: the main body and the narrow
  strip at the back;
- 91928552: the yard behind the grey board wall with the red carved gate on Landshövdingegatan,
  and the low courtyard ranges further west (not seen from the street; estimated);
- 91928587: the red boarded gambrel house on Landshövdingegatan, one zone;
- 93199672: the long taupe stucco three-storey house: the main range and the stair bumps behind;
- 93199626: the pink stucco corner house with quoins, one zone.
Heights from seven Google Street View panoramas (view only); see references/block106-notes.md.
Run with Shapely: KALMAR_GEO=<site-packages> python3 scripts/prepare_block106.py
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
IDS=['91928568','91928594','93199647','93199649','91928552','91928587','93199672','93199626']
PG={i:Polygon([tuple(w['p']) for w in d17['SM_Kvarnholmen_House_'+i]['walls']]).buffer(0) for i in IDS}
MS=lambda i:'SM_Kvarnholmen_House_'+i
# Zone seeds, in order (each takes what is left of its house). Cuts follow the outlines' own
# vertices: the street ranges first, then what is left behind them.
BKW=Polygon([(268.68,-62.54),(268.78,-57.31),(275.42,-57.44),(276.27,-57.46),(276.17,-62.47)])
OCB=Polygon([(278.98,-61.60),(279.07,-58.27),(283.0,-58.35),(282.93,-61.56)])
TPB=unary_union([Polygon([(315.75,-48.54),(318.23,-48.34),(320.82,-45.65),(320.69,-42.16),(318.22,-39.69),(316.16,-39.63)]),box(315.77,-58.1,319,-56.82)])
seeds=[('bk',PG['91928568'].difference(BKW)),('bkw',PG['91928568']),
 ('oc',PG['91928594'].difference(OCB)),('ocb',PG['91928594']),
 ('gw',PG['93199647']),
 ('mu',PG['93199649'].intersection(box(355,-75,390,-60.07))),('mub',PG['93199649']),
 ('yd',PG['91928552'].intersection(box(283.0,-63,296,-49))),('yw',PG['91928552'].intersection(box(230,-50,264.55,-41))),('ym',PG['91928552']),
 ('rd',PG['91928587']),
 ('tp',PG['93199672'].difference(TPB)),('tpb',PG['93199672']),
 ('pk',PG['93199626'])]
# Heights (m) above the street: eaves, cornice or wall top (height) and ridge (top); for the
# gambrel also the knee. Measured on the resected panoramas where the notes say so; the yard
# ranges, back wings and all ridges are estimates.
spec={'bk':dict(height=10.0,top=11.6,mesh=MS('91928568'),roof='hip'),
 'bkw':dict(height=7.0,top=7.3,mesh=MS('91928568'),roof='flat'),
 'oc':dict(height=7.9,top=11.3,mesh=MS('91928594'),roof='saddle'),
 'ocb':dict(height=3.0,top=3.2,mesh=MS('91928594'),roof='flat'),
 'gw':dict(height=3.3,top=3.5,mesh=MS('93199647'),roof='flat'),
 'mu':dict(height=10.3,top=11.9,mesh=MS('93199649'),roof='hip'),
 'mub':dict(height=10.3,top=10.5,mesh=MS('93199649'),roof='flat'),
 'yd':dict(height=2.8,top=3.0,mesh=MS('91928552'),roof='flat'),
 'yw':dict(height=6.0,top=6.2,mesh=MS('91928552'),roof='flat'),
 'ym':dict(height=6.0,top=6.2,mesh=MS('91928552'),roof='flat'),
 'rd':dict(height=3.9,top=8.0,knee=6.3,mesh=MS('91928587'),roof='gambrel'),
 'tp':dict(height=11.6,top=13.6,mesh=MS('93199672'),roof='hip'),
 'tpb':dict(height=11.6,top=11.8,mesh=MS('93199672'),roof='flat'),
 'pk':dict(height=15.8,top=18.0,mesh=MS('93199626'),roof='hip')}
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
(R/'source/block106.json').write_text(json.dumps(data,indent=1,ensure_ascii=False))
c=data['checks'];ok=c['outside_osm_m2']<.2 and c['osm_not_zoned_m2']<.5 and c['overlap_m2']<.2 and all(zones[k] for k in zones)
(R/'previews/block106-zones.json').write_text(json.dumps({'status':'passed' if ok else 'review_required','zones':report,'checks':c},indent=2,ensure_ascii=False))
print(json.dumps(report));print(c);print({i:round(PG[i].difference(covered).area,2) for i in IDS});print('BLOCK106_ZONES_OK' if ok else 'BLOCK106_ZONES_REVIEW')
