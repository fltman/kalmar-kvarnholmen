import xml.etree.ElementTree as E, math,json
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
r=E.parse(ROOT/'references/osm-map.osm').getroot()
lat0,lon0=56.66412,16.36560
angle=math.radians(28.2); c,s=math.cos(angle),math.sin(angle)
def project(lat,lon):
 e=(lon-lon0)*111320*math.cos(math.radians(lat0)); n=(lat-lat0)*111320
 return [round(e*c+n*s,3),round(-e*s+n*c,3)]
nodes={n.attrib['id']:project(float(n.attrib['lat']),float(n.attrib['lon'])) for n in r.findall('node')}
b=[]; ways=[]
for w in r.findall('way'):
 t={a.attrib['k']:a.attrib['v'] for a in w.findall('tag')}; p=[nodes[n.attrib['ref']] for n in w.findall('nd')]
 if 'building' in t: b.append({'id':w.attrib['id'],'tags':t,'polygon':p[:-1] if p[0]==p[-1] else p})
 elif t.get('highway'): ways.append({'id':w.attrib['id'],'tags':t,'points':p})
json.dump({'origin':[lat0,lon0],'rotation_degrees':28.2,'buildings':b,'roads':ways},open(ROOT/'source/site.json','w'),indent=2,ensure_ascii=False)
im=Image.new('RGB',(1600,1500),'#e7e7df'); d=ImageDraw.Draw(im)
def xy(p):return (800+p[0]*5,800-p[1]*5)
for w in ways:
 d.line([xy(p) for p in w['points']],fill='#ffffff',width=12)
for a in b:
 p=a['polygon']; center=[sum(v[i] for v in p)/len(p) for i in [0,1]]
 d.polygon([xy(v) for v in p],fill='#e9bc76' if a['id']=='38319501' else '#c0c7c6',outline='#304050',width=2)
 d.text(xy(center),a['id'],fill='black',anchor='mm')
 print(a['id'],[round(min(v[i] for v in p),1) for i in [0,1]],[round(max(v[i] for v in p),1) for i in [0,1]])
d.ellipse((794,794,806,806),fill='red'); im.save(ROOT/'references/footprints.png')
