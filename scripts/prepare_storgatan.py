"""Project OSM corridor data without changing the established Stortorget source."""
import xml.etree.ElementTree as E, math, json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
r=E.parse(R/'references/osm-storgatan-larmtorget.osm').getroot()
lat0,lon0=56.66412,16.3656;a=math.radians(28.2)
def project(lat,lon):
 e=(lon-lon0)*111320*math.cos(math.radians(lat0));n=(lat-lat0)*111320
 return [round(e*math.cos(a)+n*math.sin(a),3),round(-e*math.sin(a)+n*math.cos(a),3)]
def tags(e):return {v.get('k'):v.get('v') for v in e.findall('tag')}
nodes={n.get('id'):project(float(n.get('lat')),float(n.get('lon'))) for n in r.findall('node')}
ways={w.get('id'):w for w in r.findall('way')}
def points(w):return [nodes[n.get('ref')] for n in w.findall('nd')]
def ring(w):
 p=points(w);return p[:-1] if p[0]==p[-1] else p
buildings={w.get('id'):{'id':w.get('id'),'tags':tags(w),'polygon':ring(w),'holes':[]} for w in ways.values() if tags(w).get('building')}
for rel in r.findall('relation'):
 if not tags(rel).get('building'):continue
 outer=[m.get('ref') for m in rel.findall('member') if m.get('role')=='outer' and m.get('ref') in ways]
 holes=[ring(ways[m.get('ref')]) for m in rel.findall('member') if m.get('role')=='inner' and m.get('ref') in ways]
 for bid in outer:buildings[bid]={'id':bid,'relation':rel.get('id'),'tags':tags(rel),'polygon':ring(ways[bid]),'holes':holes}
selected=[]
preserve={'91970270','91970255','91970305','91970276'}
for b in buildings.values():
 p=b['polygon'];x0,x1=min(v[0] for v in p),max(v[0] for v in p);y0,y1=min(v[1] for v in p),max(v[1] for v in p)
 street=(-288<x0 and x1< -38 and y0<6 and y1> -12)
 square=(-385<x0 and x1< -294 and y0<66 and y1> -68)
 if (street or square) and b['id'] not in preserve:
  b['bounds']=[x0,x1,y0,y1];b['role']='square' if square else 'street';selected.append(b)
roads=[{'id':w.get('id'),'tags':tags(w),'points':points(w)} for w in ways.values() if tags(w).get('highway')]
result={'origin':[lat0,lon0],'rotation_degrees':28.2,'source':'OpenStreetMap contributors, downloaded 2026-09-19','buildings':selected,'roads':roads,'preserved_stortorget_buildings':sorted(preserve)}
(R/'source/storgatan.json').write_text(json.dumps(result,indent=2,ensure_ascii=False))
print('Selected',len(selected),'buildings')
for b in selected:print(b['id'],b['bounds'],b['tags'].get('name',''),len(b['holes']))
