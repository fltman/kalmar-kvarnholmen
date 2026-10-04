# Pass 113: the last generic pass-17 volumes near a street (Ölandskajen, Skeppsbron, the north shore, Stationsgatan and eight yard sheds)

Pass 113 replaces twelve scattered generic district volumes from pass 17. All twelve have no `detail_pass` (that is, 17) in `source/district17.json`, and `prepare_block113.py` asserts this. The build's `b113_new` also checks the object in the blend: it skips any mesh whose `detail_pass` is above 17 and not 113, and prints `BLOCK113_SKIP`. In the sandbox nothing was skipped. Pass 112's meshes (91846945, 91072716, 92204191, 93238202) are not in this pass.

## Photographed buildings

- **90977144 (Ölandskajen): the long white magasin.** The district had it at 9.75 m (three levels). It is a one-storey warehouse:
  - the outline is split where the west wall steps out 4.2 m (y −221.9) and where the narrow north end with the slanting east side begins (y −193.3); zones `ms`, `mn` and `mt`;
  - white walls with eaves at 4.8 m, on a concrete loading platform 1.2 m high and 2.4 m deep along the whole west front, with a black three-rail railing at its edge;
  - on the west front, bays of 3.95 m between dark timber eaves brackets (from s 7.6, s measured from the north corner of the west wall at (−502.64, −181.30)); in each bay a dark loading door (2.0 × 2.15 m, standing on the platform) with a glazed upper part, or every third bay a window. The oval sign over the second bay of the north range is a plain white board;
  - a grey standing-seam saddle roof along the length with 0.9 m eaves: ridge 8.4 m over the north range and 9.3 m over the wider south range (same pitch, about 23°); dark roof lights on the west slopes;
  - the north end `mt`: a hipped roof over its slanting east side, flat-topped at 6.5 m (form not seen);
  - the quay (east) side and the end walls: alternating loading doors and windows, no platform (not seen).
- **91915629 (Skeppsbron): the low light-grey hall.** **Correction to the task notes:** the dark grey modern two-storey box with the white window band in the photo is *not* this outline. Its bearings (46–70° from the camera) and its size in the image put it about 24 m from the camera at about (62, −272), where there is no OSM outline at all. 91915629's projected outline (west front at image x 327–424) lands on the low light-grey building behind the cars. It is modelled as:
  - zone `sl`: light-grey ribbed sheet walls to 5.0 m, a white fascia band 4.2–5.0 m, a band of five ground-floor windows (1.0–2.6 m) and a grey roller door on the west front, a flat roof;
  - zone `sd`: the north 5.5 m in dark grey sheet to 4.5 m (the dark lower part at the left of the hall in the photo, image x 324–352), a door on the west.
  - The unmapped dark box is not modelled (it has no outline to replace). The pass-82 houses at Kom snart igen (91915620, 91915631) are about 45 m west and are not touched.
- **91846927 (north shore, Östra Sjögatan): the red boarded pavilion.** The outline is an arrow shape pointing east; the photo shows its north-east front (tip at the left).
  - Falu-red walls with vertical battens, white base panels to 0.55 m and white corner boards, wall top 3.0 m;
  - on the north-east front, from the tip: a white panel door (s 2.55) and a white glazed double door (s 3.95), then a bank of five windows in dark red frames (0.55–2.40 m); windows on the other faces;
  - dark posts 1.4 m out carrying the deep eaves (1.6 m) of a grey metal hipped roof, top 5.8 m. The roof is built over a four-corner hull of the outline (the 2.8 m south-west corner edge is dropped so the inset does not invert); the outline's small west corner sits under the eaves.
- **1049819215 (Stationsgatan): the glazed pavilion at the bus station.** Glazing in dark frames (mullions every 1.25 m) on a dark kerb, a dark fascia 2.55–3.0 m and a dark flat roof at 3.0 m, a glazed door on the east face, and the round blue P sign (centre 4.6 m) on a post at the north-east corner. The whole outline is modelled as the pavilion (see Limitations).

## Unphotographed buildings

Each was checked against every capture in `SCR/captures.txt` (all passes) for a pano within 70 m whose field of view contains the building. Only 92204195 came up, in `p109/92204179_h61_p15.jpg` (pass 109): it stands behind pass 109's red outbuilding 92204179 and a green board fence and is not visible. A red tile roof shows above that outbuilding's wall top, but a ray through it reads 5.3–7.5 m on planes through 92204195, which is too high for a 63 m² shed, and it cannot be tied to this outline. So all eight are modelled plainly at estimated heights, with materials from their detailed neighbours: one door on the side facing the street or yard, small windows in white frames on the other long walls, white corner boards, a plinth strip.

| Mesh | Where | Modelled as | Eaves / top (m) |
|---|---|---|---|
| 149000062 | Ölandskajen, beside pass 111's shed 149000060 | white corrugated sheet with ribs and a low white saddle roof, as the pass-111 shed | 2.8 / 3.3 |
| 90859836, 90859884, 90859852 | the yard south of pass 96's Fiskaregatan houses (three identical 6.7 × 10.9 m outlines) | red boarded yard outbuildings, red tile saddle roofs along the long side, door in the north gable | 3.2 / 5.8 |
| 93238185 | Norra Långgatan, behind pass 80's houses | grey-white boarded shed, flat felt roof with white fascia | 2.8 |
| 93192417 | Storgatan, against pass 90's 93192374 (shared wall skipped) | yellow rendered annex, red tile saddle roof, as pass 91's low rendered neighbours | 2.9 / 4.7 |
| 92204195 | Larmgatan, behind pass 109's 92204179 | red boarded outbuilding, flat dark roof with white fascia (as 92204179's flat wall top) | 3.0 |
| 1549543685 | Östra Vallgatan, in the park | small red boarded shed, dark sheet saddle roof | 2.4 / 3.4 |

## Measurement

The tools are the project's standard ones: `SCR/p82/hit.py` and `meas.py` at 756 × 405 with vfov 90, and an overlay script (`SCR/p113/ov113.py`) that projects every district outline within range. The facade plane is the OSM line offset 0.355 m outward. Positions are local (x, y).

| Photo (pano id) | Google position | Camera used (x, y, h) | Method | Measured |
|---|---|---|---|---|
| 90977144_h110 (yYQbHKjB…) | (−528.65, −194.57) | (−528.65, −194.57, 2.3) nominal | Not resected: the only corners in view are the far south end (projects at x 454–464, seen at about 450) and the step at y −222 (projected 368–386, the roof change seen at about 330). Readings on the west wall plane, then scaled ×1.1, between 1.0 (raw) and 1.18 (door height 2.3 m). The camera stands on the raised road; the lot reads 1.9 m below it raw. | Platform 1.2 (1.1–1.4); doors on the platform 1.95 raw (2.0–2.3); eaves 4.8 (4.4–5.2); north ridge 8.4 (7.7–9.1); bracket spacing 3.9 raw at s 7.6, 11.6, 15.5, 19.3, 23.4; doors at s 9.6, 17.4, 21.3; sign at s 13.4 |
| 91915629_h57 (HXVDwp9M…) | (41.52, −284.07) | nominal, h 2.5 | Not resected; the projected outline corners fall within about 2 px of the hall's ends (x 327 and 424), at 46 m. The base is hidden by cars. | Fascia top 4.7–4.8 raw, fascia bottom about 3.4; ground about −0.4 raw → top 5.0; dark north part top 4.3 raw (4.5), extends about 5.5 m along the west front |
| ksi_h332 (same pano) | | | Used only to identify buildings: the cottage at left is pass 82's 91915620; the dark box at the right edge has no outline. | |
| 91846927_h152 (8RaqVg67…) | (87.46, 185.61) | (88.9, 185.9, 2.4) | Least-squares on the wall's base line and the tip corner (image x 530); residuals about 1 m, so the camera is good to about ±1 m. | Wall top 2.9; eaves fascia 3.2; glazed door 0.15–2.53; panel door s 2.0–2.9; posts about 1–2 m out (inconsistent readings) |
| 1049819215_h250 (6ROp9NdxZj…) | (−479.73, −1.91) | nominal, h 2.5 | Not resected; about 30–45 m away. | Roof top 2.75–3.1; fascia about 0.4–0.5; P sign centre about 4.5 |

## Estimated

- **90977144:** the scale (±10 %), the south range's ridge (its raw skyline reading gives 11 m, inconsistent with the north range, so the north range's pitch is used), the north end's roof form, the quay side and both ends, the door/window pattern beyond the measured bays, the roof-light positions.
- **91915629:** everything except the west front's heights and the dark part's extent; the window band and roller door positions are approximate (behind cars).
- **91846927:** the ridge height (top 5.8 m is taken from the roof's appearance, about 28°), the faces other than the north-east one, post positions.
- **1049819215:** the footprint use (see Limitations), door position, the P sign's post.
- **The eight unphotographed sheds:** everything.
- **All:** colours are judged by eye from the photos.

## Verification

- `KALMAR_GEO=SCR/pylib python3 scripts/prepare_block113.py` prints `BLOCK113_ZONES_OK`: footprint 2762.3 m², zoned 2762.3 m², outside OSM 0.01 m², OSM not zoned 0.0 m², overlap 0.0 m².
- The sandbox (prelude: rebuild chain 111) ran twice and printed `SANDBOX_DONE` with no errors and `BLOCK113_GEOMETRY 12`, nothing skipped.
- `drop_degenerate_faces113`, with the `_thin` test, runs on every mesh right after `s21_finish`. Faces dropped: 90977144 360, 91915629 4, 91846927 0, 1049819215 35, 149000062 14, each red outbuilding 14, 93238185 3, 93192417 14, 92204195 7, 1549543685 14. These are zero-area or sliver faces from the edge bevel at abutting boxes (the magasin has hundreds of small door, bracket and railing parts); they were not inspected one by one. The aerial renders show no holes in the walls or roofs.
- Renders at the photos' size were compared side by side (`SCR/p113/cmp2_c*.jpg`; aerials in `SCR/p113/aer1.jpg`):
  - **Magasin:** the length, the far end, the eaves line and the platform line up; the render's roof reads a little darker than the silvery real roof.
  - **Skeppsbron hall:** its ends and height line up with the low light-grey building.
  - **Pavilion:** the tip, the posts and the eaves are in about the right place; the real roof rises more steeply in the photo (it reaches the image top at the right), so 5.8 m may still be low.
  - **Bus station pavilion:** the modelled pavilion spans image x 330–407; the real one spans about 354–408 (see Limitations).
- The official build, the export check and the Unreal checks are pending; the lead fills in the build results.

## Limitations

- **The bus station pavilion** in the photo looks narrower than its outline: it covers only the right two-thirds of where the outline projects. Either the camera is about 3 m off or the outline also covers open ground west of the pavilion. A closer view would settle it, e.g. from about (−500, −12), heading 300, pitch 5.
- **The magasin** is measured from one unresected photo; a view from the quay (east) side, e.g. from about (−470, −230), heading 242, pitch 10, would give the roof's ridge and the quay front.
- **The unmapped dark grey two-storey box** at about (62, −272) on Skeppsbron is a real building with no OSM outline and is missing from the model.
- **Omitted:** cars, bicycles, containers, signs' lettering, lamps and the masts on Skeppsbron.

## Official build

The lead's build of pass 113 passed the Blender geometry checks and the FBX export, and two rebuilds gave identical meshes. Passes 28–112 are unchanged except the earlier intended corrections (passes 85, 98, 100, 105, 109 and 111, made by passes 103, 107 and 112). The Unreal import and its checks are deferred.
