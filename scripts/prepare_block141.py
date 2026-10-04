"""Pass 141: Kalmar slott, the height of the north tower (Kungsmakstornet, model key N).

Pass 27 put the north tower's wall top (the eaves, the top of the cornice where the copper starts)
at z 23.27 by eye. Pass 137 found two Möller sheets that disagree (references/block137-notes.md,
task 3):
- Möller 1882, "Profil genom Kungsmaket" (PK006-00041): the eaves 12.16 m over the state floor,
  z 22.63;
- Möller 1885, "Ritning till nytt tak å norra tornet" (PK006-00049): 13.5 fot (4.01 m) from the
  tower's eaves down to an adjoining cornice; if that is the range's outer eaves (z 20.27, pass 27,
  confirmed by Möller 1882 via pass 127) the tower's eaves are at z 24.28.

This pass adds a third source: three views with resected cameras (one openly licensed photograph,
two Google Street View panoramas, viewed only). Each measures the tower's eaves against the range's
outer eaves next to it (z 20.27) with a camera fitted locally, so the camera's height and the
pano's pitch error drop out. The readings are kept here; the decision follows the brief: if two of
the three sources agree within about 0.3 m, the tower gets that value.

Writes source/block141.json. No zones (the pass changes one existing mesh).
"""
import json,math
from pathlib import Path
R=Path(__file__).resolve().parents[1]
C27=json.loads((R/'source/castle27.json').read_text());B132=json.loads((R/'source/block132.json').read_text())
FOT=0.2969
def zh(h):return round(-1.33+h,4)
TOP27={'W':25.3,'S':25.6,'N':24.6,'E':25.3}          # build_castle27.py TOWER_SPEC 'top' (m above the water)
Z_OUTER_EAVES=C27['levels_z']['eaves']                  # 20.27, the ranges' outer eaves
assert abs(Z_OUTER_EAVES-20.27)<1e-6

# ------------------------------------------------------------------ the two Möller sheets (pass 137)
MOLLER={
 '1882':dict(sheet='PK006-00041',title='Calmar slott. Profiler, "Profil genom Kungsmaket"',z=22.63,
             how='eaves 12.16 m over the state floor (z 10.47); Kungsmaket 4.38 m high (pass 125: 4.3)'),
 '1885':dict(sheet='PK006-00049',title='Ritning till nytt tak å norra tornet',dim_fot=13.5,
             how='13.5 fot from the tower eaves down to an adjoining bracketed cornice; taken as the range outer eaves'),
}
MOLLER['1885']['z']=round(Z_OUTER_EAVES+MOLLER['1885']['dim_fot']*FOT,2)
assert abs(MOLLER['1885']['z']-24.28)<.01

# ------------------------------------------------------------------ the third source: resected views
# z values: the tower's eaves read on the model's cylinder (pass 27 radius + 0.24 m cornice) with the
# camera's pitch fitted so that the adjacent range eaves sit at z 20.27. 'front' = the cornice's
# nearest point (column of the highest point of the copper's lower edge), 'tangent' = the cornice's
# top at the tower's silhouette. Ranges cover the camera alternatives listed in the notes.
VIEWS=[
 dict(id='photo2022',src='references/castle27/swe-kalmar-slott-004.jpg',what='-wuppertaler 2022-06-07, CC BY-SA 4.0, 1920 x 1440',
      cam=[-898.89,-176.26,2.0],heading=140.3,pitch=9.2,f_px=1444,
      cam_note='bearings of both silhouettes of N and W and Kuretornet\'s corners; f 1444 px is the only focal length for which the '
               'curvature of the cornice (front against silhouettes) is consistent; f 950-1000 px fits the bearings as well but not the curvature',
      eaves_rows={'range at N (667,681),(700,681.5)':20.27},
      N={'front':[24.6,24.8],'tangent':[25.0,25.2]},N_all=[23.9,25.8],W={'front':[24.1,24.5],'tangent':[24.9,25.2]}),
 dict(id='sv2014_bridge',src='Street View pano iMd5WI6ugBpN7x-8vlt6pA (Sep 2014), the castle bridge',what='screenshots 1014 x 764, viewed only',
      cam=[-915.14,-231.90,6.0],heading=92.0,pitch=14.0,f_px=1049.6,
      cam_note='pano at (-913.60,-233.36); resected on N\'s silhouettes and Kuretornet\'s face corners (heading 103, vfov 55): (-915.14,-231.90); '
               'camera height 5.5-6.5 m; local pitch +1.5..+2.9 deg from the range eaves',
      eaves_rows={'range NW by N (560..610, 441.7) in 40y/92h/104t':20.27},
      N={'tangent':[24.5,24.8]},N_all=[24.5,25.5],W={'tangent':[25.1,25.4]}),
 dict(id='sv2014_terreplein',src='Street View pano 81wq-3oJLh_ApLhniDADzg (Sep 2014), the north-east rampart',what='screenshots 1014 x 764, viewed only',
      cam=[-823.68,-252.79,12.3],heading=219.3,pitch=16.5,f_px=922.2,
      cam_note='pano at (-826.94,-253.84); resected on N\'s silhouettes and Kuretornet\'s axis with the NE outer eaves on outline edge 45-46; '
               'camera 11.8-12.8 m; N radius 6.35 (OSM) or 5.9 (Möller 1885) m',
      eaves_rows={'NE outer eaves by N (200,414),(400,418) in 45y/222h/110t':20.27},
      N={'front':[24.0,24.45],'tangent':[23.1,24.3]},N_all=[23.1,24.5],W=None),
]
best={v['id']:sum(v['N'].get('front',v['N'].get('tangent')))/2 for v in VIEWS}
THIRD=round(sum(best.values())/len(best),2)             # the mean of the three views' preferred readings
MEDIAN=round(sorted(best.values())[1],2)
spread=round(max(best.values())-min(best.values()),2)

# ------------------------------------------------------------------ decision
srcs={'Möller 1882':MOLLER['1882']['z'],'Möller 1885':MOLLER['1885']['z'],'views (mean)':THIRD}
pairs=[(a,b,round(abs(srcs[a]-srcs[b]),2)) for a in srcs for b in srcs if a<b]
agree=[p for p in pairs if p[2]<=.30]
assert any({'Möller 1885','views (mean)'}=={p[0],p[1]} for p in agree),pairs
assert all(abs(srcs['Möller 1882']-v)>1.0 for k,v in srcs.items() if k!='Möller 1882')
# The new wall top is Möller 1885's dimension on the model's range eaves: a written dimension on a
# measured drawing, confirmed by the views within their spread; the views' median is not used as
# the value because their readings scatter (0.5 m) by more than the difference (0.24 m).
Z_N=MOLLER['1885']['z'];TOP_N=round(Z_N+1.33,2)
assert abs(Z_N-THIRD)<=.30 and 24.0<Z_N<24.6

out=dict(
 source='references/block141-notes.md',
 z_outer_eaves=Z_OUTER_EAVES,
 moller=MOLLER,views=VIEWS,view_best=best,view_mean=THIRD,view_median=MEDIAN,view_spread=spread,
 pairs=pairs,agree=agree,
 towers={k:dict(top27=TOP27[k],z27=zh(TOP27[k])) for k in 'NSWE'},
 decision=dict(key='N',z_old=zh(TOP27['N']),z_new=Z_N,top_new=TOP_N,dz=round(Z_N-zh(TOP27['N']),2),
               others='W, S and E unchanged (see the notes: W reads 24.1-25.4 against 23.97, inconclusive; S and E not seen side-on)'),
 collar=dict(note='where a pass 127 roof\'s cut edge (against pass 27\'s bell) lies between the old wall top and 0.6 m above it, '
                  'outside the wall, a flashing collar in the tower render closes the slot to the raised wall',z_old=zh(TOP27['N']),h_top=.60,depth=.30,step_deg=2.5),
 checks=dict(n_views=len(VIEWS)),
)
(R/'source/block141.json').write_text(json.dumps(out,indent=1,ensure_ascii=False))
print('views',best,'mean',THIRD,'median',MEDIAN,'spread',spread)
print('pairs',pairs)
print('N wall top: z %.2f -> %.2f (TOWER_SPEC top %.2f -> %.2f)'%(zh(TOP27['N']),Z_N,TOP27['N'],TOP_N))
print('BLOCK141_PREPARE_OK')
