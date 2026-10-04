"""Pass 128: Kalmar slott, the chimneys (corrects pass 127's chimney list).

Pass 127 placed six tall chimneys 2 m up the courtyard slopes from a first, wrong reading of the 2017
courtyard photograph (two of them on the SW range, where the photograph shows SE_w), and kept pass
27's four outer chimneys. This pass measures the chimneys again and replaces the whole list
(source/block127.json 'chimneys' is overridden by source/block128.json 'chimneys' at build time).

Sources (see references/block128-notes.md for the readings):
- Google Street View 2014, courtyard panoramas zCIfieeXGQUNANmWu_Tg9A ("pano 1") and
  jOXzkLldNOjrveyz1T81wg ("pano 2"), and the outer pano VgKtBpunaiGwzOIYZf4djA (SE side), viewed only.
  Each pano camera was resected on the courtyard corners and the well (heading offset solved with it).
- Commons 2017 courtyard photograph (PD), camera as resected by pass 127.
- Commons 2021 vertical drone photograph (HaSe) and the 2021 oblique one, for the count and for the
  chimneys that no panorama sees (the SW outer row, the NE outer pair).
Positions are in each range's frame (s along the range, c across it, as pass 27/127: origin, u, n).
Heights are the height of the chimney above its downhill foot on the roof, as measured (top minus
visible foot); the build stands each chimney 0.8 m into the roof, as pass 127 did.
Output: source/block128.json and previews/block128-zones.json.
Run: KALMAR_GEO=<pylib with shapely> python3 scripts/prepare_block128.py
"""
from pathlib import Path
import json,math,os,sys
if os.environ.get('KALMAR_GEO'):sys.path.insert(0,os.environ['KALMAR_GEO'])
from shapely.geometry import Polygon,Point,box as sbox
from shapely import affinity
R=Path(__file__).resolve().parents[1]
C27=json.loads((R/'source/castle27.json').read_text());CA=C27['castle']
B127=json.loads((R/'source/block127.json').read_text())
RANGES={r['name']:dict(r) for r in CA['ranges']}
ZCE=B127['zce'];RR=B127['ranges']
PIECES=[(pc['key'],pc['plane'],[Polygon(rr[0],rr[1:]) for rr in pc['rings']]) for pc in B127['roof']]
def rp(r,s,c):o=r['origin'];return (o[0]+r['u'][0]*s+r['n'][0]*c,o[1]+r['u'][1]*s+r['n'][1]*c)
def rframe(r,p):o=r['origin'];dx,dy=p[0]-o[0],p[1]-o[1];return dx*r['u'][0]+dy*r['u'][1],dx*r['n'][0]+dy*r['n'][1]
def zroof(p):
 # the visible roof surface (pass 127's joined pieces) over a plan point, or None
 best=None
 for key,pl,polys in PIECES:
  if any(q.buffer(.03).contains(Point(p)) for q in polys):
   z=pl[0]*p[0]+pl[1]*p[1]+pl[2]
   if best is None or z>best[0]:best=(z,key)
 return best

# ---------------------------------------------------------------- measured chimneys
# id: (range, placement, w along the range, d across, height above the downhill foot, status, source)
# placement: ('sc',s,c) in the range frame; ('xy',x,y) a triangulated plan point; ('zfoot',s,z) the
# point at s on the courtyard slope whose roof height is the measured foot height z.
CH=[
 # SE_w/SE_e bend: slender, about 1.7 m up the slope beside the bend. Triangulated from pano 1 (two
 # views), pano 2 and the 2017 photograph (bearing residuals 0.2-2.3 deg); foot z 18.9-19.7, top 4.2-5.0 m
 # above the foot.
 ('K','SE_w',('xy',-867.26,-328.41),1.0,.8,4.5,'measured','pano 1 (98, 135), pano 2 (150), 2017 photo'),
 # SE_w: the wide chimney with the row of flue holes, straddling the ridge at the middle of the range.
 # Triangulated from pano 1, pano 2 and the 2017 photo (residuals under 1 deg), base at the ridge,
 # visible height 4.3-4.9 m, width 1.66 m (pano 1). Seen from outside too (outer pano, ray 0.6 m off).
 ('I','SE_w',('sc',10.43,-5.40),1.65,1.1,4.4,'measured','pano 1 (135), pano 2 (150), 2017 photo, outer pano'),
 # SE_e: slender, close above the courtyard eaves, 0.8 m wide (pano 2). Triangulated from four rays
 # (residuals under 0.4 deg); the triangulated point lies 0.7 m in front of pass 127's fitted eaves
 # line, so it stands at its measured foot height (z 18.7, 1.7 m above the eaves) on the model slope.
 ('C','SE_e',('zfoot',9.71,18.7),.9,.8,4.5,'measured','pano 1 (98, 135), pano 2 (95, 150)'),
 # E corner: slender, well up the slope in the SE_e/NE corner. Triangulated from pano 1 (two views)
 # and pano 2 (residuals 0.1 deg); foot z 22.2-22.4, visible height 4.0 m.
 ('B','SE_e',('xy',-845.17,-319.36),.9,.8,4.0,'measured','pano 1 (98, 135), pano 2 (95)'),
 # NE near the east end, on the courtyard slope. Pano 1 only (two views, one camera): the ray is
 # intersected with pass 127's roof (s 4.6-4.8, c -10.9 to -12.0); height 3.7-5.6 m.
 ('A','NE',('sc',4.7,-11.5),.9,.8,4.6,'estimated','pano 1 (20, 98), ray on the roof'),
 # NW at the north courtyard corner: a short chimney about 1.9 m up the slope, seen from pano 2 on the
 # bearing of the corner's downpipe. Pass 27's north corner renders 6.7 deg off the panorama's corner
 # from the resected camera, so the chimney is placed on the model corner's bearing (s 11.5; the ray on
 # the roof alone gives s 14.5). Height 1.6-1.7 m.
 ('N1','NW',('sc',11.5,-16.1),.8,.7,1.7,'estimated','pano 2 (300, 330), ray on the roof, relative to the corner'),
 # Beyond the north corner, seen over the NE front from pano 2 only (top only), 7 deg right of the
 # corner. Its distance along the ray is not measured; it is placed 26 m out, where its height would
 # be about 5.3 m like the other courtyard stacks, and turned with the corner's 6.7 deg offset, which
 # puts it on the NE courtyard slope north of the corner.
 ('N2','NE',('sc',33.3,-14.1),1.0,.8,5.3,'estimated','pano 2 (330), top only'),
 # SW near the west courtyard corner, half way up the courtyard slope (the only chimney on the SW
 # courtyard slope in pano 2's 245 view). Pano 2, ray on the roof; the drone photo agrees (s 5.6, half
 # way up). Height 3.4 m (top just over the SW ridge).
 ('W','SW',('sc',6.58,-6.56),.9,.8,3.4,'measured','pano 2 (245), drone 2021'),
 # SW outer slope: a row of three in the upper half of the outer slope (drone 2021, interpolated
 # between the west and south courtyard corners; the 2021 oblique photo shows the same three over the
 # SW ridge with the same spacing ratio 0.77), and one beside the stepped gable near the outer eaves.
 # The 2017 photograph shows none of them over the SW ridge from the courtyard, so their tops stand
 # about 0.3 m over the ridge (2.9 m above the foot).
 ('SWo1','SW',('sc',17.5,-.8),.8,.7,2.7,'estimated','drone 2021'),
 ('SWo2','SW',('sc',21.37,-2.1),.9,.7,2.9,'estimated','drone 2021, oblique 2021'),
 ('SWo3','SW',('sc',24.82,-2.1),.9,.7,2.9,'estimated','drone 2021, oblique 2021'),
 ('SWo4','SW',('sc',29.19,-2.1),.9,.7,2.9,'estimated','drone 2021, oblique 2021'),
 # NE outer slope: a pair near the outer eaves at the middle of the range, one narrow, one wide;
 # tops just under the NE ridge (oblique 2021 from the north-east; drone 2021 s 19.7 and 23.0; the
 # oblique photo's tower spacing gives s 20.0 and 23.5).
 ('NEo1','NE',('sc',23.0,2.0),.9,.7,4.0,'estimated','drone 2021, oblique 2021'),
 ('NEo2','NE',('sc',19.7,2.0),1.4,.8,4.3,'estimated','drone 2021, oblique 2021'),
 # SE_e outer slope near the east end (outer pano ray meets the SE_e ridge at s 21.8-22.7; drone 2021
 # on the outer slope). It is not seen from the courtyard (pano 1), so it stands 2.9 m out from the
 # ridge with its top 1.1 m over it.
 ('SEo','SE_e',('sc',22.0,-3.0),.9,.7,3.0,'estimated','outer pano, drone 2021'),
]
# Not modelled: a short white stack at the west end where the SW and NW roofs meet (drone only, may be
# a vent), and a stack on the south tower's cap edge (drone only; it stands inside the tower's plan).

DORMERS=[]
for dm in B127['dormers']:
 a=dm['a'];u=(math.cos(a),math.sin(a));v=(-u[1],u[0])
 # pass 27's roof_dormer: about 0.9 m either side of the axis and 2.6 m up the slope from the eaves
 corners=[(dm['x']+u[0]*du+v[0]*dv,dm['y']+u[1]*du+v[1]*dv) for du,dv in ((-1.1,-3.2),(1.1,-3.2),(1.1,3.2),(-1.1,3.2))]
 DORMERS.append(Polygon(corners).convex_hull)
TOWERS=[(tuple(t['centre']),t['radius']) for t in CA['towers'].values()]
KURE=Polygon(CA['kure_rect'])

chimneys=[];rows=[]
for cid,rn,pl,w,dep,h,status,src in CH:
 r=RANGES[rn];ang=math.atan2(r['u'][1],r['u'][0])
 if pl[0]=='xy':x,y=pl[1],pl[2]
 elif pl[0]=='sc':x,y=rp(r,pl[1],pl[2])
 else:
  # zfoot: walk up the courtyard slope at s until the roof (at the downhill face) reaches z
  s,zt=pl[1],pl[2];c=r['inner']-1.0;x=y=None
  while c<RR[rn]['cr']:
   zr=zroof(rp(r,s,c-dep/2))
   if zr and zr[0]>=zt:x,y=rp(r,s,c);break
   c+=.01
  assert x is not None,(cid,'no foot height on the slope')
 s,c=rframe(r,(x,y))
 corners=[(x+dx*math.cos(ang)-dy*math.sin(ang),y+dx*math.sin(ang)+dy*math.cos(ang)) for dx in (-w/2,w/2) for dy in (-dep/2,dep/2)]
 zs=[zroof(p) for p in corners]
 assert all(z is not None for z in zs),(cid,'a corner is off the roof',zs)
 zlo=min(z[0] for z in zs);zhi=max(z[0] for z in zs)
 foot=Polygon(corners).convex_hull
 for (cx,cy),rad in TOWERS:assert math.dist((x,y),(cx,cy))>rad+.8,(cid,'in a tower')
 assert not foot.intersects(KURE),(cid,'in Kuretornet')
 for dpoly in DORMERS:assert not foot.intersects(dpoly),(cid,'meets a dormer')
 z1=zlo+h;assert z1>zhi+.8,(cid,'top not clear of the roof',z1,zhi)
 if rn=='NW':assert zlo-.8>17.35,(cid,'would reach Gyllene salen (walls to z 17.27)')
 side='in' if c<RR[rn]['cr'] else 'out'
 piece=max(zs,key=lambda z:z[0])[1]
 chimneys.append(dict(id=cid,range=rn,side=side,x=x,y=y,w=w,d=dep,ang=ang,z0=round(zlo-.8,4),z1=round(z1,4),
  s=round(s,3),c=round(c,3),foot_z=round(zlo,3),height=h,status=status,source=src,piece=piece))
 rows.append((cid,rn,side,round(s,2),round(c,2),round(r['inner'],2),round(RR[rn]['cr'],2),round(r['outer'],2),round(zlo,2),round(z1,2),round(z1-RR[rn]['zr'],2),status))
# no two chimneys overlap
for i in range(len(chimneys)):
 for j in range(i+1,len(chimneys)):
  a,b=chimneys[i],chimneys[j];assert math.dist((a['x'],a['y']),(b['x'],b['y']))>1.5,(a['id'],b['id'])

out=dict(source='pass 128: chimneys re-measured on Street View 2014 (courtyard panos zCIfieeXGQUNANmWu_Tg9A, jOXzkLldNOjrveyz1T81wg; outer pano VgKtBpunaiGwzOIYZf4djA; viewed only), the 2017 Commons photograph and the 2021 Commons drone photographs; see references/block128-notes.md',
 chimneys=chimneys,count=len(chimneys),
 checks=dict(count=len(chimneys),measured=sum(c['status']=='measured' for c in chimneys),estimated=sum(c['status']=='estimated' for c in chimneys),
  courtyard_side=sum(c['side']=='in' for c in chimneys),outer_side=sum(c['side']=='out' for c in chimneys),
  replaces_pass127=len(B127['chimneys'])))
(R/'source/block128.json').write_text(json.dumps(out,indent=1,ensure_ascii=False))
(R/'previews/block128-zones.json').write_text(json.dumps(dict(chimneys={c['id']:dict(range=c['range'],side=c['side'],s=c['s'],c=c['c'],plan=[round(c['x'],2),round(c['y'],2)],
  size=[c['w'],c['d']],foot_z=c['foot_z'],top_z=c['z1'],status=c['status']) for c in chimneys},checks=out['checks']),indent=1))
print('id    range side     s       c   (inner  ridge  outer)  foot   top  top-ridge status')
for row in rows:print('%-5s %-5s %-4s %7.2f %7.2f  (%6.2f %6.2f %6.2f) %5.2f %5.2f %6.2f  %s'%row)
print(json.dumps(out['checks']))
print('BLOCK128_PREPARE_OK')
