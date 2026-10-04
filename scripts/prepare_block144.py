"""Pass 144: Klapphuset (OSM 93199604), red walls, a narrower pier with railings, no east deck
(corrects pass 122).

The reviewer found pass 122's Klapphuset white with a too wide pier. Pass 122 read the house from the
satellite only: a grey roof, a pale weathered pier and deck, white corner boards and a white eaves
board. Four openly licensed photographs (Wikimedia Commons, 2015 and 2024) and two Google user
photospheres (April 2021, viewed only, one resected) show:
- falu red lap boarding all round, red corner boards, a black standing-seam hip roof with a dark
  fascia; the only white is the window frames;
- window pairs high under the eaves (three on the south front, four and a small window on the north,
  two on the east end), a green glazed double door in a shallow bay with its own small hip canopy;
- pale grey vertical skirting boards from the floor down to the water, no piles in sight;
- a timber pier from the door to the shore with railings on posts, about 2.2 m over the handrails at
  the house end (resected), deck about 1.9 m;
- no deck on the east end (the pale band east of the roof on the satellite is not a deck in any photo).

Writes source/block144.json. No zones (the pass re-creates one existing mesh from its OSM outline).
"""
import json,math
from pathlib import Path
R=Path(__file__).resolve().parents[1]
NAME='SM_Kvarnholmen_House_93199604'
D17=json.loads((R/'source/district17.json').read_text())['buildings'][NAME]
B122=json.loads((R/'source/block122.json').read_text())['zones']['wa']
ring=[tuple(w['p']) for w in D17['walls']]
# The OSM ring has five nodes: four corners and the entrance node on the south wall.
DOOR=(435.414,122.849)
assert any(math.dist(p,DOOR)<1e-3 for p in ring),ring
SW,SE,NE,NW=[tuple(v) for v in B122['rect']]
assert math.dist(SW,(426.559,127.332))<.01 and math.dist(SE,(442.119,119.443))<.01,B122['rect']
Ls=math.dist(SW,SE);Lt=math.dist(SE,NE)
d=((SE[0]-SW[0])/Ls,(SE[1]-SW[1])/Ls);n=(d[1],-d[0])            # along the south wall, and outward (south)
s_door=(DOOR[0]-SW[0])*d[0]+(DOOR[1]-SW[1])*d[1];off_door=(DOOR[0]-SW[0])*n[0]+(DOOR[1]-SW[1])*n[1]
assert abs(off_door)<.02,off_door

# ------------------------------------------------------------------ the photographs (measurements)
# Commons "Klapphuset, Kvarnholmen, Kalmar.jpg" (TS Eriksson 2015, CC BY-SA 4.0) seen square-on from the
# pier's shore end at 1014 px: walls 105..835 px (17.45 m, 41.9 px/m at the wall), eaves row 287,
# boarding bottom 410 (2.93 m; pass 17's 2.95 kept). Window pairs centred 190, 377, 699 px; door 520 px
# (= the OSM entrance node at 9.91 m from the SW corner, 9.92 m read); pairs 2.75 m wide, 1.05 m high,
# bottom 1.52 m; door frame 1.93 m x 2.33 m; ventilators at 291 and 659 px (+-4.4 m from the centre).
PHOTO_SOUTH=dict(px_per_m=730/Ls,pairs_px=[190,377,699],door_px=520,wall_px=[105,835])
pairs_south=[round((u-105)/PHOTO_SOUTH['px_per_m'],2) for u in PHOTO_SOUTH['pairs_px']]
assert abs((520-105)/PHOTO_SOUTH['px_per_m']-s_door)<.1
# Commons "Klapphuset Kalmar 03.jpg" square-on to the north front across the water: walls 388..778 px,
# pairs centred 428, 518, 609, 702 px from the east; a small two-light window at 762 px near the west end.
pairs_north=[round((u-388)/(390/Ls),2) for u in (428,518,609,702)];small_read=round((762-388)/(390/Ls),2)
# The small window reads 16.73 m, 0.7 m from the corner; with its frame it is kept 0.35 m clear of the corner board.
small_north=round(min(small_read,Ls-.35-.45),2)
# Commons "Klapphuset 01.jpg": the east end with two pairs, no deck; skirting to the water all round.
# Photosphere CIHM0ogKEICAgICK9Zy3Wg (2021, viewed only), resected on the SW corner (u 147.5), the OSM
# entrance node (u 343) and the SE corner (u 458.5) at heading 15, pitch 2, vfov 90: camera (426.57,
# 98.14), residuals under 0.3 deg. The handrails at the house end hit the door plane at -0.88 and
# +1.32 m along the wall from the entrance node (2.20 m over the rails, centre +0.22 m); the door
# frame at -0.69..+1.11 (1.80 m).
PIER=dict(centre_shift=0.22,over_rails=2.20,deck=1.90,rail_u=0.90,start_out=0.60,
          end_along=20.44,top=0.0,note='end: pass 122 shore point (426.8,104.3) projected on the pier axis')
Q122=(426.8,104.3);end_along=(Q122[0]-DOOR[0])*n[0]+(Q122[1]-DOOR[1])*n[1]
assert abs(end_along-PIER['end_along'])<.05,end_along

WALLS={
 # name: (p, q, openings [kind, s from p, width])
 'south':(SW,SE,[['pair',s,2.75] for s in pairs_south]+[['door',round(s_door+.0,3),1.80]]),
 'east':(SE,NE,[['pair',round(Lt/2-2.0,2),2.75],['pair',round(Lt/2+2.0,2),2.75]]),
 'north':(NE,NW,[['pair',s,2.75] for s in pairs_north]+[['small',small_north,0.90]]),
 'west':(NW,SW,[['pair',round(Lt/2-2.0,2),2.75],['pair',round(Lt/2+2.0,2),2.75]]),
}
OUT=dict(mesh=NAME,osm='93199604',corrects_pass=122,
 outline=[list(p) for p in ring],rect=[list(SW),list(SE),list(NE),list(NW)],door_node=list(DOOR),
 lengths=dict(long=round(Ls,3),short=round(Lt,3)),
 heights=dict(floor=0.0,eaves=2.95,ridge=4.20,water=-1.33,skirt_bottom=-1.45,window_bottom=1.52,window_h=1.05,door_h=2.25),
 roof=dict(kind='hip',overhang=0.80,ridge_inset=round(Lt/2-.15,3),ventilators=[-4.36,4.36]),
 bay=dict(s=round(s_door,3),width=2.50,depth=0.25,canopy_width=3.40,canopy_out=1.45,canopy_eaves=2.82,canopy_top=3.55),
 walls={k:dict(p=list(p),q=list(q),openings=o) for k,(p,q,o) in WALLS.items()},
 pier=dict(PIER,axis_origin=[DOOR[0]+d[0]*PIER['centre_shift'],DOOR[1]+d[1]*PIER['centre_shift']],axis_dir=list(n),along=list(d)),
 materials={'Falu':['TownIvory',[.48,.15,.11]],'Frame':['TownPaintWhite',[.93,.93,.90]],'DoorGreen':['TownPaintGreen',[.25,.46,.31]],
            'Roof':['TownMetalGrey',[.13,.13,.14]],'Vent':['TownMetalGrey',[.17,.17,.18]],'Skirt':['TownPaintWhite',[.55,.55,.53]],
            'Timber':['TownPaintWhite',[.50,.47,.43]],'TimberDark':['TownPaintBrown',[.28,.25,.22]]},
 measured=dict(pairs_south=pairs_south,pairs_north=pairs_north,small_north=small_north,small_north_read=small_read,pier_over_rails=2.20,door_frame=1.80,
               camera_shore=[426.57,98.14],pier_length_from_wall=round(PIER['end_along']-.355,2)))
# checks: openings inside their walls and clear of each other
for k,w in OUT['walls'].items():
 L=math.dist(w['p'],w['q']);sp=sorted((s-wd/2,s+wd/2) for _,s,wd in w['openings'])
 assert all(a>.3 and b<L-.3 for a,b in sp),(k,sp,L)
 assert all(b1+.3<a2 for (a1,b1),(a2,b2) in zip(sp,sp[1:])),(k,sp)
assert abs(OUT['bay']['s']-s_door)<1e-3 and OUT['bay']['width']>OUT['walls']['south']['openings'][-1][2]
(R/'source/block144.json').write_text(json.dumps(OUT,indent=1,ensure_ascii=False))
print('BLOCK144_PREPARED OK',NAME,'south pairs',pairs_south,'north pairs',pairs_north,'small',small_north,'door s',round(s_door,2),'pier',PIER['deck'],'deck,',PIER['over_rails'],'over rails, length',round(PIER['end_along']-PIER['start_out'],2))
