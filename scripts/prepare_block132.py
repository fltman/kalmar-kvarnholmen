"""Pass 132: Kalmar slott, the tower caps after Carl Möller's roof drawings of 1885 (Riksarkivet
PK006-00048...00052, public domain) and the photographs.

Writes source/block132.json (the measured cap profiles, in fot and in metres, per model tower) and
previews/block132-zones.json (one zone per cap: eaves level, tip level, checks).

Reading the sheets. Every sheet carries a scale bar in fot (0.2969 m) and written dimensions. The
written vertical chains were read on full-resolution crops and give 52.2-53.0 px per fot (bar:
52.2 px/fot on the Vattentornet sheet), so every sheet is read at 52.5 px/fot unless its own chain
says otherwise (noted per tower). Heights are measured from the eaves line (the top of the cornice,
where the copper starts), half-widths from the cap's axis. The bell silhouettes were traced
automatically (the right-hand outline, darkest non-red pixel per row, every 25 px) and cleaned by
hand where a dimension line or a pinnacle stood in the way; the rest (plinths, drums, necks, bulbs,
balls, finials) were read off the crops point by point. Precision is about +-0.2 fot (6 cm).

Which tower is which (model keys of source/castle27.json):
- "Vattentornet" (PK006-00048) is the square tower with the four lucarnes, the corner aedicules,
  the open octagonal lantern and the crown: pass 27's Kuretornet (the square gate tower, KRECT).
  It is the only square tower of the castle; its total height on the sheet (91 fot = 27.0 m from the
  eaves to the cross) puts the crown at 59.0 m above the water, which is what pass 27 measured on
  Kuretornet from Street View (59.0). The museum's state-floor plan also calls this tower
  "Vattentornet" (see references/castle-sources/SOURCES.md on the conflicting tower names).
- "Norra / Södra / Västra / Östra tornet" are the model's N, S, W and E round towers. Evidence: the
  shapes in the photographs (the 2019 drone view from the east-north-east shows, left to right, S:
  bell + drum + ogee dome, E: bell + drum + cushion + bulb, W: bell + drum + tall pear bulb + ball,
  Kuretornet, N: low wide bell + drum + onion); the courtyard photographs, whose cameras pass 127/129
  resected independently (2017: the south tower; 2022: the east tower), show the Södra and Östra
  sheets' caps; and the wall diameters on the sheets rank as the model's do (S 41.2 > N 39.7 > W 37.7
  fot; the model's E is the one exception, see the notes).
"""
import json,math
from pathlib import Path
R=Path(__file__).resolve().parents[1]
FOT=0.2969
C27=json.loads((R/'source/castle27.json').read_text());TW=C27['castle']['towers'];HL=C27['levels_h']
def zh(h):return round(-1.33+h,4)
# pass 27's wall tops (build_castle27.py TOWER_SPEC 'top', m above the water); kept unchanged.
TOP27={'W':25.3,'S':25.6,'N':24.6,'E':25.3}

# ------------------------------------------------------------------ the four round towers (fot)
# bell: (h, half) from the eaves; n_bell: sides of the bell (plan); n_up: sides of drum and bulbs.
# parts: (kind, n or None, [(h, half), ...]) on top of the bell; kinds: 'poly' (faceted, n sides),
# 'round' (smooth), 'ball' (centre h, radius), 'rod' (h0, h1, radius), 'fleur' (h), 'vane' (h),
# 'tip' (h), 'pilasters' (h0, h1), 'spikes' (h, half) and 'crownring' (h0, h1, half).
ROUND={
 'N':dict(sheet='PK006-00049_1885_Moller_tak-Norra-tornet.jpg',moller='Norra tornet',drawn='July 1885',ppf=52.5,
  wall_half=19.85,eaves_half=21.15,valance=0.0,cornice=1.20,n_bell=12,n_up=10,total_written=60.50,
  bell=[(0,21.43),(.48,19.49),(.95,18.78),(1.43,18.29),(1.9,17.85),(2.86,17.24),(3.81,16.80),(4.76,16.46),(5.71,16.19),(6.67,15.92),
        (7.62,15.70),(8.57,15.45),(9.52,15.20),(10.48,14.95),(11.43,14.63),(12.38,14.29),(13.33,13.92),(14.29,13.43),(15.24,12.80),
        (16.19,11.98),(16.67,11.35),(17.14,10.70),(17.62,9.62),(17.85,8.6),(18.0,7.6)],
  parts=[('poly',10,[(18.0,7.3),(18.3,7.3),(18.3,7.0),(18.8,6.0),(19.4,5.3),(20.2,4.95),(20.75,4.85),(21.2,4.6),(21.3,4.1),(23.9,4.1),
                     (23.9,4.25),(24.2,4.25),(24.2,4.1),(27.5,4.1),(27.6,4.5),(28.0,5.05),(28.25,5.05),(28.25,4.6),(28.6,3.6),(29.3,2.8),
                     (30.5,2.3),(32.4,2.17),(32.75,2.17),(32.75,2.95),(33.0,2.95),(33.1,1.8),(33.6,3.2),(34.3,3.85),(35.5,3.95),(37.0,3.3),
                     (38.5,2.0),(39.6,1.2),(40.3,1.12),(40.6,1.76),(40.9,1.76),(41.0,.8),(41.8,.8)]),
         ('pilasters',10,(21.3,27.5)),('ball',None,(43.9,1.55)),('rod',None,(41.8,59.6,.22)),('fleur',None,51.4),('vane',None,56.8),('tip',None,60.0)]),
 'S':dict(sheet='PK006-00050_1885_Moller_tak-Sodra-tornet.jpg',moller='Södra tornet',drawn='August 1885',ppf=52.5,
  wall_half=20.6,eaves_half=22.15,valance=1.80,cornice=1.20,n_bell=16,n_up=8,total_written=57.90,
  bell=[(0,22.23),(.48,20.44),(.95,19.41),(1.43,18.67),(1.9,18.08),(2.86,17.16),(3.81,16.51),(4.76,16.04),(5.71,15.60),(6.67,15.22),
        (7.62,14.90),(8.57,14.57),(9.52,14.27),(10.48,13.96),(11.43,13.66),(12.38,13.33),(13.33,12.93),(14.29,12.40),(15.24,11.66),
        (16.19,10.84),(16.67,10.27),(17.14,9.33),(17.45,8.3),(17.68,7.6)],
  parts=[('poly',8,[(17.68,7.3),(19.45,7.3),(19.45,7.0),(23.7,7.0),(23.7,7.15),(24.2,7.15),(24.2,7.0),(25.4,7.0),(25.4,7.2),(25.9,7.6),(26.4,8.1),
                    (26.6,8.1),(26.6,8.0),(27.0,7.2),(27.4,6.4),(27.93,5.95),(29.1,5.5),(30.9,5.05),(33.86,3.97),(35.3,2.7),(36.0,2.0),(36.25,1.6),
                    (36.25,2.1),(36.85,2.1),(36.85,.75),(40.4,.75),(40.4,1.33),(40.9,1.33),(40.9,.6),(42.4,.6),(42.4,1.5),(42.9,1.8),(43.3,1.6),(43.6,1.0),(44.6,.5)]),
         ('pilasters',8,(19.45,25.4)),('spikes',None,(42.9,2.3)),('rod',None,(44.6,57.6,.2)),('fleur',None,49.65),('vane',None,55.1),('tip',None,58.1)]),
 'W':dict(sheet='PK006-00051_1885_Moller_tak-Vastra-tornet.jpg',moller='Västra tornet',drawn='August 1885',ppf=52.6,
  wall_half=18.85,eaves_half=21.1,valance=2.60,cornice=1.20,n_bell=10,n_up=12,total_written=65.20,
  bell=[(0,20.13),(.48,19.01),(.95,18.27),(1.43,17.79),(1.9,17.40),(2.85,16.69),(3.80,16.18),(4.75,15.78),(5.70,15.36),(6.65,15.08),
        (7.60,14.85),(8.56,14.62),(9.51,14.41),(10.46,14.14),(11.41,13.92),(12.36,13.71),(13.31,13.35),(14.26,13.04),(15.21,12.59),
        (16.16,12.00),(17.11,11.25),(18.06,10.10),(18.8,8.5),(19.1,7.5)],
  parts=[('poly',12,[(19.1,7.15),(20.95,7.15),(20.95,6.85),(25.6,6.85),(25.6,7.1),(26.6,7.5),(27.3,7.5),(27.3,7.0),(27.6,5.6),(28.7,4.9),(31.0,3.06),
                     (31.4,3.0),(31.4,3.6),(32.2,3.6),(32.2,3.3),(32.9,3.3),(33.3,4.2),(34.1,4.5),(35.4,4.34),(37.3,3.86),(38.2,3.2),(39.0,2.8),
                     (40.5,2.0),(41.5,1.4),(42.0,1.4),(42.3,1.85),(42.7,1.85),(42.7,.9),(45.4,.9),(45.4,2.7),(45.9,2.7),(45.9,.9),(46.4,.9)]),
         ('pilasters',12,(20.95,25.6)),('ball',None,(49.5,1.75)),('rod',None,(46.4,63.5,.2)),('crownring',None,(53.4,54.2,2.07)),('vane',None,61.6),('tip',None,65.0)]),
 'E':dict(sheet='PK006-00052_1885_Moller_tak-Ostra-tornet.jpg',moller='Östra tornet',drawn='September 1885',ppf=52.2,
  wall_half=20.05,eaves_half=21.65,valance=1.80,cornice=1.20,n_bell=16,n_up=8,total_written=67.30,
  bell=[(0,21.46),(.48,20.11),(.96,19.14),(1.44,18.28),(1.92,17.76),(2.87,16.92),(3.83,16.30),(4.79,15.73),(5.75,15.33),(6.70,14.96),
        (7.66,14.64),(8.62,14.37),(9.58,14.10),(10.54,13.79),(11.49,13.51),(12.45,13.22),(13.41,13.01),(14.37,12.70),(15.33,12.24),
        (16.28,11.72),(17.24,11.09),(18.2,9.8),(18.7,8.5),(19.16,7.6)],
  # photo 2022 (camera 716): above the drum's cornice a straight octagonal block of Möller's 7.70 fot
  # carries the cushion; the sheet's concave 6.20 fot neck is not there today (photograph wins).
  parts=[('poly',8,[(19.16,7.35),(20.6,7.35),(20.6,7.0),(27.3,7.0),(27.4,7.6),(27.9,8.2),(28.1,8.2),(28.1,3.85),(33.5,3.85),(33.5,2.75),(34.3,2.75),(34.3,3.05),(35.0,4.4),(36.1,5.15),(37.0,4.4),(37.9,2.4),(38.2,2.08),
                    (38.2,1.95),(38.5,1.95),(39.2,2.9),(40.7,3.28),(43.2,2.36),(45.1,1.1),(46.8,1.05),(48.0,1.05),(48.0,2.83),(48.4,2.83),(48.4,.7),(50.0,.7)]),
         ('pilasters',8,(20.6,27.3)),('ball',None,(51.8,1.55)),('rod',None,(50.0,67.0,.2)),('fleur',None,59.2),('vane',None,64.6),('tip',None,67.9)]),
}

# ------------------------------------------------------------------ Vattentornet = Kuretornet (fot)
KURE=dict(sheet='PK006-00048_1885_Moller_tak-Vattentornet.jpg',moller='Vattentornet',drawn='May 1885',ppf=52.6,
 wall_half=23.5,eaves_half=24.45,total_written=88.0,
 # the bell's outline in the face elevation (the face's half-width), from the eaves
 bell=[(0,24.45),(.6,23.3),(1.24,22.4),(2.3,21.1),(3.4,20.2),(4.8,19.55),(6.2,19.1),(8.0,18.7),(9.9,18.4),(11.8,18.2),(13.6,18.0),(15.0,17.8),
       (16.4,17.6),(17.8,17.2),(19.2,16.7),(20.1,16.3),(21.0,15.8),(21.8,15.2),(22.5,14.5),(23.0,14.0),(23.3,13.7),(23.5,13.2)],
 # octagonal parts above the bell (faces square to the tower), (h, half = apothem)
 plinth=[(23.5,12.5),(23.92,12.4),(24.6,11.2),(25.55,10.1),(26.2,9.3),(26.87,8.74),(27.5,8.9),(28.06,9.5),(28.65,10.25),(29.24,9.5),(29.6,8.83),(30.5,8.83)],
 lantern=dict(h0=30.5,h1=41.0,apothem=8.25,face=6.85,sill=.7,opening=3.0,impost=37.2,col_r=.55,col_cap=.68),
 upper=[(41.0,8.3),(42.2,8.3),(42.4,8.7),(43.8,9.2),(44.2,9.8),(44.5,9.79),(45.18,8.56),(46.1,7.6),(47.6,6.94),(49.5,6.56),(51.4,5.89),
        (52.9,4.75),(53.85,3.6),(54.3,2.28),(54.8,2.28),(54.8,1.6),(55.6,1.6),(56.0,3.18),(56.9,3.18),(57.0,1.95),(58.75,1.95),(59.25,3.0),
        (59.65,3.2),(60.75,3.15),(62.75,2.47),(64.75,1.5),(66.75,.9),(68.25,.9),(68.25,1.25),(68.75,1.25),(69.35,1.0),(69.8,2.1),(70.0,2.1),
        (70.0,1.0),(71.0,1.0),(71.0,1.4),(71.5,1.4),(71.5,.8)],
 ball=(75.0,2.375),band=(74.75,75.25,2.5),neck=[(77.4,.9),(78.6,.9),(78.6,1.5),(79.0,1.5),(79.0,.35)],
 rod=(79.0,87.8,.35),plate=(82.8,1.7),arms=(85.6,3.0),crown=(87.8,90.9,1.57),
 # four lucarnes, one on each face (front plane at half 21.0 from the axis)
 dormer=dict(front=21.0,base=(.5,2.15),volute_half=6.2,col_half=3.8,opening=3.7,col_top=10.6,entab=(10.6,12.8),arch_r=3.9,finial=21.8,open_bottom=2.6),
 # the corner aedicules (centre 22.97 fot from the axis on each face, i.e. on the wall's corner)
 aedicule=dict(inset=.55,pedestal=(0,2.5,1.6),column=(2.5,10.75,.55,.68),entab=(10.75,12.85,2.0),box=(12.85,16.85,1.6),finial=(16.85,22.05,.6)))

out={'source':'Carl Möller, roof drawings for Kalmar slott, May-Sept 1885, Riksarkivet PK006-00048..52 (public domain); see references/block132-notes.md',
     'fot':FOT,'towers':{},'kure':None}
zones=[];checks={}
for key,T in ROUND.items():
 r=TW[key]['radius'];z1=zh(TOP27[key])
 hs=[h for h,_ in T['bell']]+[h for h,_ in T['parts'][0][2]]
 assert all(b>=a for a,b in zip(hs,hs[1:])),('heights not monotonic',key)
 k0=r/T['wall_half']                                  # horizontal scale at the eaves (model wall / drawn wall)
 a0=T['bell'][0][1]*k0
 assert a0>=r+.26,('bell base does not cover the cornice',key,a0,r)  # pass 27's cornice: r+0.24
 tip=[p for p in T['parts'] if p[0]=='tip'][0][2]
 z_tip=z1+tip*FOT
 out['towers'][key]=dict(T,radius=r,centre=TW[key]['centre'],z_eaves=z1,k_eaves=round(k0,5),bell_top=T['bell'][-1][0])
 zones.append(dict(zone=key,mesh='SM_Kalmar_Slott_Towers',moller=T['moller'],sheet=T['sheet'],z_eaves=z1,z_tip=round(z_tip,3),
   tip_above_water=round(z_tip+1.33,2),cap_height_m=round(tip*FOT,2),written_total_fot=T['total_written'],read_total_fot=tip,
   bell_base_apothem=round(a0,3),wall_radius=r,k_eaves=round(k0,4),n_bell=T['n_bell'],n_up=T['n_up']))
 checks[key]=dict(total_read_vs_written_fot=round(tip-T['total_written'],2),bell_base_over_wall_m=round(a0-r,3))
kp=[tuple(p) for p in C27['castle']['kure']];ZK=zh(32.0)
out['kure']=dict(KURE,z_eaves=ZK)
kt=KURE['crown'][1];zones.append(dict(zone='Kure',mesh='SM_Kalmar_Slott_Towers',moller='Vattentornet',sheet=KURE['sheet'],z_eaves=ZK,
  z_tip=round(ZK+kt*FOT,3),tip_above_water=round(ZK+kt*FOT+1.33,2),cap_height_m=round(kt*FOT,2),written_total_fot=KURE['total_written'],
  read_total_fot=KURE['crown'][0]))
checks['Kure']=dict(crown_top_above_water=round(ZK+kt*FOT+1.33,2),pass27_crown=59.0)
assert abs(ZK+kt*FOT+1.33-59.0)<.3
# Pass 27's Street View measurements of the finials: W 39.2 and S 37.6 m above the castle foot (5.0).
checks['W']['tip_vs_streetview_m']=round(zones[2]['tip_above_water']-(39.2+HL['foot']),2)
checks['S']['tip_vs_streetview_m']=round(zones[1]['tip_above_water']-(37.6+HL['foot']),2)
for k in ('N','S','W','E'):assert abs(checks[k]['total_read_vs_written_fot'])<1.0,(k,checks[k])
out['checks']=checks
(R/'source/block132.json').write_text(json.dumps(out,indent=1,ensure_ascii=False))
(R/'previews/block132-zones.json').write_text(json.dumps(dict(zones=zones,checks=checks),indent=1,ensure_ascii=False))
print('BLOCK132_PREPARE_OK',json.dumps(checks,ensure_ascii=False))
