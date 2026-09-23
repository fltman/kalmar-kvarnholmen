# Kalmar slott on Slottsholmen — pass 27

Research date: 2026-09-23.

The pass adds Kalmar slott and its island, about 300 m west of the station and outside the earlier model boundary. It covers:
- the castle, with its four ranges round the courtyard, the well house of 1578, the square gate tower Kuretornet, four round corner towers with copper caps, the chapel's roof turret and three stepped gables
- the dry moat and the earth ramparts with guns
- the curtain walls and the four low round postejer (gun towers)
- the north-west lower wall with its berm, the gate and tunnel, and the gate building in the dry moat
- the timber bridge with its drawbridge
- the ravelin with the castellan's house (Kastellanvillan)
- three islets in Slottsfjärden.

The mainland (Stadsparken, Kalmarsundsparken) is not modelled, as elsewhere in the model, which only has islands. The bridge from the ravelin to the park therefore ends at an abutment. Photographs and panoramas are working references only. No pixel is used as a texture, and nothing was extracted from Google.

## Sources

- **OpenStreetMap** (`references/castle27/osm-castle27.osm`, Overpass extract of 2026-09-23, ODbL) provides:
  - the island's coastline and the castle outline with its courtyard (relation 1331955)
  - the four corner towers and Kuretornet (`building:part`)
  - the four postejer, the curtain walls and the north-west lower wall
  - the dry moat's counterscarp and the walled gate building (1084130856, "height 5 m")
  - the tunnel (`tunnel=yes`, 90614014), the building passage, the gates and entrances
  - the bridges, the ravelin walls, the castellan's house, the islets and every footway.
- **Google Street View**, official imagery of September 2014, viewed in the browser. The positions were checked by resection against known points:

| Panorama | Position | Resection | Used for |
|---|---|---|---|
| South-west rampart | 56.6575075 N, 16.354454 E | within 0.5 m, 0.11° rms | castle foot, eaves, window rows, tower walls and caps, south postej, water, dry-moat coping |
| Bridge by the gate | 56.6583943 N, 16.3542411 E | 1.5 m off, 0.59° rms | Kuretornet, north-west range roof, gate and revetment, water below the deck |
| Courtyard | reported 56.6580167 N, 16.3554965 E | 13.5 m off, 0.83° rms | courtyard eaves above the courtyard floor |

- **Wikimedia Commons photographs.** They are stored in `references/castle27/` with authors, dates and licences in `sources.json`. The main ones are:
  - aerials by HaSe, 2021, one of them vertical
  - a drone view from the south-east by Iamstockton, 2019
  - views from the north-west, the entrance and the courtyard by -wuppertaler, 2022, including a photograph of the Statens fastighetsverk board that names the parts
  - an aerial by L.G.foto, 2006, and one by Kateryna Baiduzha, 2020
  - views from the east (Kiwijo2000, 2012), the south-west (Hstad, 2009) and the south-east (Moonbarker, 2013).
- **Helgo Zettervall's west elevation**, "Förslag till återställande af Calmar slott", dated 4 September 1883 (Commons, public domain).
- **Background texts.** Swedish and English Wikipedia, and the Statens fastighetsverk board: four round corner towers of 1535, Johan III's ranges and Renaissance caps, the chapel of 1589–92, the postejer finished in the early 1600s, and the silhouette restored by Zettervall in 1885–91.

## Levels and measurement

Heights were measured by inverting the Street View camera, as in passes 24 and 26. The viewing ray of a pixel is intersected with the vertical plane of the feature, a cylinder round a tower axis, or the horizontal distance to an axis. Results are given in metres above the water of the moat and Slottsfjärden. The model's water plane is at z = −1.33.

| Level | m above water | Basis |
|---|---|---|
| Low berm on the south-west, south-east and north-east | 1.5 | photographs |
| Postej walls | 1.2 to 13.4 | south postej: foot −11.6, top −0.1 below the rampart camera |
| Curtain top on the south-west, south-east and north-east | 6.8 | photographs (about 0.45 of the postej height) |
| North-west berm, gate threshold, bridge deck, dry-moat floor | 5.0 | castle foot −8.6 under the rampart camera, which is 13.5 m above the water; bridge camera 2.2–2.6 m above its deck with the water 7.9 m below |
| Rampart top | 11.4 | rampart camera less a trekker height of about 2 m; dry-moat coping −2.5 to −3.0 |
| Courtyard | 9.5 | outer eaves 16.6 m above the foot, courtyard eaves 12.2 m above the courtyard floor |
| Eaves | 21.6 | 16.6–16.9 m above the foot (Zettervall: 15.6) |
| Ridges | 26.1–27.6 | south-west range 21.2 m above the foot, north-west range 20–22 m; deeper ranges have flatter roofs |
| Corner tower walls | 24.6–25.6 | west 20.3 and south 20.6 m above the foot; north from the bridge |
| Corner tower finials | 40.2–44.2 | west 39.2 and south 37.6 m above the foot |
| Kuretornet cornice | 32.0 | 27.1–27.3 m above the foot from the bridge, tied to the west tower (Zettervall: 27.0) |
| Kuretornet crown | 59.0 | about 54 m above the foot (Zettervall: 53.9) |

The outer fronts carry these rows of openings, measured above the castle foot:
- doors at the foot
- small windows at 4.85–6.06 m
- tall main-floor windows with small panes at 7.9–11.1 m
- small windows under brick segmental arches at 13.9–14.7 m, below a dentilled cornice.

The courtyard fronts have two rows of windows and doors with stone portals. Zettervall's drawing agrees with the measurements within about 1 m. It was used for the proportions of the caps.

## Geometry and interpretation

`scripts/prepare_castle27.py` (Shapely) writes `source/castle27.json`. `scripts/build_castle27.py` builds ten meshes from it.

- **Island.**
  - The rampart top is the area between the curtains and the counterscarp.
  - On the south-west, south-east and north-east a curtain about 5 m high carries a grassed slope 6 m wide up to the rampart. It narrows to 2.2 m towards the postejer, where the rampart walk runs close to the edge.
  - The north-west side has the lower wall with its brick-arched casemate openings, the berm walkway at the gate level, and a battered revetment with a cordon up to the rampart.
  - The outer 2.2 m of every berm slopes to the water under boulder riprap.
  - The dry moat is the area inside the counterscarp. The gravel paths follow the OSM footways.
- **Entrance.** It follows OSM:
  - The bridge leads to the gate in an ashlar block with a coat-of-arms tablet (the relief is not modelled).
  - A vaulted tunnel runs along its mapped line under the rampart to the counterscarp.
  - From there a walk leads past the walled gate building, whose vaulted passage carries the dry-moat walk through it, to the castle gate in the foot of Kuretornet.
  - A second door in the counterscarp, near the foot of the steps up the rampart, is shown closed. The steps and the cobbled ramp up the rampart are not modelled.
- **Castle.**
  - Each range is a gable roof over a rectangle fitted to the outline. The roofs are joined as their upper envelope, which gives hips and valleys; the outer corners lie inside the towers.
  - Roofs are dark sheet metal with standing seams every 0.62 m, and the chimneys are rendered in salmon.
  - Two bays on the south-east front and the middle of the north-east front carry stepped gables with white trim, obelisk finials and an oval light.
  - The chapel's small roof turret sits at 45 % along the south-west range, where Street View shows its spire.
  - Dormers with red-painted fronts sit on the courtyard slopes.
- **Towers.**
  - Each round tower has a stone cornice, a row of small square openings and a few windows.
  - Each cap is ribbed copper and follows the photographs:
    - west: a tall bell, a neck and an onion
    - south and east: a bell and an open octagonal lantern
    - north: a lower bell, a drum and an onion.
  - Kuretornet has rubble-stone walls with six small openings on each face under a corbelled cornice, and the pointed window and a small window towards the north-west.
  - Its square copper bell roof has steep sides, shoulders, four dormers and corner pinnacles, under an open octagonal lantern, a spire with two balls and a gilded crown.
- **Postejer.** Three are round, battered drums of rubble stone with three rows of openings, some barred. They have low cone roofs of light sheet metal with seams. The north postej follows its D-shaped OSM outline and has a square stair tower on the moat side.
- **Courtyard.** It is paved with cobbles. The painted rustication is on the south-west range's courtyard front. The well house has an octagonal base, eight columns, four pediments, a lantern and a finial.
- **Bridge.** A timber trestle on pairs of piles every 2.7 m, with plank decking, posts and two rails. The drawbridge frame (two posts, a head beam, braces and two lifting arms with chains) stands 5.8 m from the gate.
- **Ravelin.** Stone walls from the water, grass and gravel paths, and a raised grass parapet on the outer faces, opened where the park bridge lands. The castellan's house has one storey of cream render and a mansard roof: red shingles below, tiles above, with dormers and a brick chimney.
- **Guns.** Twelve guns stand on timber carriages on the south-west and north-west ramparts, at positions spaced from the aerials.

Signs and interpretation boards are omitted, and nothing is lettered.

## Materials

The 36 new `M_Castle27_*` materials tint existing texture sets towards colours read from the photographs. Each tint is computed against the texture's measured mean colour in linear space.

A first version used a running-bond ashlar texture on the revetment, curtains and courtyard front. Its alternating block tones read as diagonal stripes. The revetment and lower wall now use a natural rubble texture, the curtains coursed rubble, and the gate and courtyard rustication large ashlar blocks.

The first grass texture repeated as visible diagonal waves, so the lawns now use the turf texture tinted green. No new texture sets were needed.

## Verification

All reports in `previews/castle27-delivery.json` passed:
- **Zoning.**
- **Build:** 626,715 triangles in ten meshes, with no zero-area or zero-UV triangles.
- **FBX vectors:** no zero or non-finite normals, tangents or binormals.
- **Repeatability:** identical geometry, UV and material hashes on a second rebuild.
- **Materials:** all 36 materials have normal and roughness maps.
- **Import and render:** Nanite import and render buffers pass.

The castle lies about 900 m from the model's origin, where 32-bit coordinates resolve only about 0.06 mm. Thin slivers from the arch spandrels and the bevelled window parts therefore get undefined normals, and the first export could not derive a tangent frame for them. Faces under 20 mm² and thinner than 1:100 are now removed when each mesh is finished. They are not visible.

The collision test (`Unreal/Content/Python/validate_castle27.py`) takes 843 floor samples and 834 character-sized capsule sweeps. Each follows the surface of its route:
- the bridge from the ravelin to the gate
- the tunnel and the walk to Kuretornet's gate
- the rampart walk
- two dry-moat walks
- the courtyard loop
- two ravelin paths
- the bridge to the park.

The first runs found faults in the model itself. Each was fixed and the test run again:
- The ravelin parapet stood across the landing of the park bridge.
- The walled landing at the south tower had been built as a solid block and closed the dry moat.
- The corner wall in the east lacked its mapped gate.
- The gate building blocked the dry-moat walk, which passes through it.
- The rampart walk ran onto the grassed slope near the postejer.

The only remaining obstruction is a step of about 0.3 m where the park bridge lands on the ravelin. It has a verified detour 0.8 m to the side.

The review shots match the Street View calibration views within a few pixels at the same vertical field of view (`144_Castle_Cal_Rampart`, `145_Castle_Cal_Bridge`, `146_Castle_Cal_Courtyard`). This holds for the tower walls, eaves and finials, and for Kuretornet's cornice and crown.

## Limitations

- The mainland is not modelled, including the park and the moat's outer bank.
- The north tower's height, the east tower's cap, the courtyard levels and the depths of the ranges' roofs are estimates.
- The cannon positions are interpreted.
- Not modelled: the steps and cobbled ramp from the tunnel mouth up to the rampart, the interior of the gate passage through the castle, the sculpted portals and coat of arms, the interiors, flags, signs and reeds.
- No performance measurement was made.

## Licences

Mapped geometry: © OpenStreetMap contributors, ODbL. The Commons photographs keep their licences (see `sources.json`) and are not redistributed with the public edition. Street View imagery was only viewed. Authored geometry follows the project licence (CC BY 4.0, code MIT).
