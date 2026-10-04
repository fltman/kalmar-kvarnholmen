# Pass 118: Gamla stan, Kungsgatan, Söderportsgatan, Klostergatan and Skansgatan

Pass 98 built the mainland houses as plain volumes inside three chunk meshes. Pass 118 is the third Gamla stan pass. It takes 40 of them out of the chunks. Each becomes its own mesh, `SM_Slott118_<osm id>` (category `Slottsområdet/Gamla stan`, `detail_pass` 118), with its real form:

- storeys (1, 1.5, 2 or 3, some over a raised basement) and the eaves and ridge heights;
- the roof: saddle, hip, Swedish mansard (gambrel, with gable ends), hipped mansard, or a shallow hip, in red tile, red-brown tile or dark metal;
- the walls: vertical boarding (battens, white corner boards), render or brick, in the house's colour (falu red, yellow, pale yellow, white, white-grey, grey, pink, pale green, ochre yellow, salmon, yellow brick, red brick), on a grey stone plinth;
- white eaves boards and bargeboards, windows per storey (casement, surround, sill), small basement windows under raised ground floors, a door on the wall that faces the street (steps where the door stands above the ground), gable windows on the steeper gables;
- dormers, chimneys and the notable features listed in the table.

## Selection

The selection is computed in `scripts/prepare_block118.py` from the OSM street lines in `references/osm-slott98.json` (ways with `highway` and `name`): Kungsgatan (all seven ways), Söderportsgatan (w37732307, w959684368), Klostergatan (w37732306) and Skansgatan (w37732305). It takes every outline in `source/block98.json['buildings']` that lies within 25 m of one of them and leaves out:

- the houses of passes 107, 115 and 116 (read from `source/block115.json` and `source/block116.json`; only 91970274, the Söderport pavilion of pass 115, would have been selected);
- every house in pass 117's area by its rule: within 25 m of Västerlånggatan with the centroid at x ≤ −930, or within 25 m of Gamla Kungsgatan or Paters gränd. This drops 16 outlines near Kungsgatan and Söderportsgatan, among them every house at a corner with Västerlånggatan or Gamla Kungsgatan, and the beige villa with the lunette and balcony on sp05_h316 (93292658, pass 117). The selection shares no id with the current `source/block117.json` (40 ids).

The 40 ids: 93238230, 93238237, 93238238, 93238258, 93238265, 93238271, 93238276, 93238289, 93291960, 93291974, 93291980, 93291986, 93291987, 93291990, 93291994, 93291997, 93292667, 93292672, 93292679, 93292701, 93293011, 93293013, 93293015, 93293018, 93293019, 93293020, 93293021, 93293023, 93293026, 93293027, 93293029, 93293034, 93293035, 93293038, 93293040, 93293042, 93326709, 93326721, 93326735, 93326746.

They lie in pass 98's chunks M (−1150..−850) and W (x < −1150). `SLOTT98_DETAILED` gets the 40 ids, and `slott98_chunks115({'M','W'}, 118, block118_names)` (pass 115) re-creates `SM_Slott98_Buildings_M` and `_W` without them. The chunks are listed among this pass's meshes (42 names in all) and keep `detail_pass` 98 with `rebuilt_by_pass` 118. Because the set accumulates, the chunks re-created here also stay without the houses of passes 107, 115, 116 and (in the official chain) 117. The first sandbox run's prelude was `rebuild_block116` (pass 117's houses still in the chunks); the second ran on `rebuild_block117`.

## Zones

Pass 116's slab method (`decompose`) splits each outline into rectangles for its roofs. The largest is the main body; the others are wings (same eaves, a ridge lowered by width) or flat-roofed annexes when under 12 m² or narrower than 2.6 m. On the three-storey blocks the annexes keep the full height, because the notches there are stair bays and not sheds. Two houses have explicit rectangles read on their photos:

- **93293023**, the derelict corner house. The two-storey cross part stands on the 7.2 m bump of the street front (vertices 3–4) and runs through to Klostergatan, with its ridge across the house, so it shows a low gable to both streets. The rest of the outline forms two gambrel wings with their ridges along the house (axis 7→0).
- **93293026**, the gambrel villa. A cross gambrel with its ridge running north–south covers the west part (7.5 m of the 14.4 m street front). The east part's gambrel runs along the house.

For each zone, the prepare script stores the outer wall that faces each nearby street (`street_walls`) and the nearest one (`street_wall`). The door goes on the nearest. For five houses on Söderportsgatan, the build uses the Söderportsgatan wall instead, because the photos show the entrance there.

## Measurement

The photos were captured for the pass (`SCR/p118`, `captures.txt` lines starting `118|`): 20 views, 728 × 419, vertical field of view 90°, pitch +10°.

- **Identities.** All OSM outlines within 70 m were projected into every view from the Google positions (overlays `SCR/p118/w/ov_*.png`, plan `w/plan.png`). Vertex labels on the photos (`w/vx.py`) gave the corners used for resection.
- **Resection.** The camera is found by a grid search within 8 m of the Google position that fits the bearings of two outline corners (pass 116's `grid_resect`, `SCR/p118/w/m118.py`). Heights are read on the plane of the named wall with `hit`. With two corners the fit is exact, so the residual says nothing about accuracy.
- Several views look over hedges and fences. There the base is hidden, so the camera height from the base row is wrong. Those readings are taken up or down to an assumed 2.2–2.6 m camera, as noted in the table.

| Panorama (view) | Google position (x, y) | Camera used (x, y), height | How | Used for |
|---|---|---|---|---|
| _y14HLmQPeWul8TdA_v3ww (sp03_h151) | (−1084.8, −55.3) | (−1086.26, −56.26), 2.10 | the two front corners of 93293038 (u 122 and 612) | the pink stone house |
| _y14HLmQPeWul8TdA_v3ww (sp03_h331) | (−1084.8, −55.3) | (−1085.86, −57.36), 1.1 from the hedge line, taken as 2.3 | the front corners of 93292679 (the west gable wall u 345, the tower's east face u 561) | the tower villa |
| mvI7dWQHpmmYVB1m8AcsUw (sp04_h322) | (−1105.2, −57.5) | (−1106.33, −58.94), assumed 2.2–2.6 | the front corners of 93292667 (u 290 and 418) | the red villa |
| mvI7dWQHpmmYVB1m8AcsUw (sp04_h142) | (−1105.2, −57.5) | Google, 2.84 from the base | one corner only (u 432, 0.9 m from Google) | the gambrel villa |
| RWIv3AcGXeED3RXEr4Me5Q (sp01_h145) | (−1021.9, −53.5) | (−1022.56, −54.7), 1.97 | the two corners of the cross part's bump (u 105 and 290) | the derelict corner house |
| 2SZ7RC-vr5ArT0MULQCzuw (kg02_h213) | (−1011.2, −23.2) | Google, assumed 2.2–2.5 | – (over the hedge) | the mansard villa |
| plmFqqRn4O1qXL7pZVgcyg (kg07_h212) | (−1120.4, 169.3) | (−1120.67, 166.8), 1.39 from the base, taken as 2.3 | the left corner of 93238237 and the right corner of 93238276 | the 1940s row |
| tOHZ-fwfPCFbaa-qKzX2TA (kg09_h201) | (−1188.6, 262.1) | Google, 2.92 from the base | – | the yellow-brick houses |
| all other views | Google | Google, 2.3 | identification, storeys and colours only | the rest |

### Houses

Heights are metres above the ground (model z 0.30). "Measured" means read with the cameras above. Everything else is estimated from storeys, doors and windows (one storey ≈ 3.0–3.4 m to the eaves, two ≈ 5.4–6.0 m, three over a basement ≈ 10.4 m), with roof pitches by eye.

| OSM id | Identity | Photo | Storeys | Eaves / ridge | Roof | Walls | Measured or estimated |
|---|---|---|---|---|---|---|---|
| 93293023 | derelict house at the Söderportsgatan/Klostergatan corner: two-storey cross part with low gables on both streets, gambrel wings on both sides, boarded-up windows, green door in a carved surround | sp01_h145, kg01_h213, kl01_h304 | 2 (cross part), 1 + attic (wings) | cross 5.4 / 7.1; wings 3.2 / 6.7 (break 5.4) | red tile saddle and gambrels | white-grey boards | measured (camera 1.97): cross-part wall top 5.1–6.3, apex 6.9, upper windows 3.6–5.1; wing eaves 3.2, break 5.4, top 6.7 |
| 93293038 | 18th-century pink rough-rendered stone house, light quoins, stone door surround, two dormers | sp03_h151, sp04_h142 | 2 | 6.2 / 11.0 | red tile hip | pink render | measured (camera 2.10): eaves 6.1–6.3, ridge 11.5 on the ridge line (drawn 11.0), door 0–3.0, windows 1.17–2.89 and 4.06–5.57 |
| 93293026 | pale yellow boarded villa on a raised grey plinth with basement windows, a cross gambrel gable on the street and the two-storey glazed porch at the north-east corner | sp04_h142 | 1 + gambrel storey | 5.6 / 10.8 (cross gambrel), 5.6 / 9.6 (east part) | red-brown tile gambrels | pale yellow boards | measured (Google camera, 2.84 from the base): plinth 1.8, eaves 5.8, break 9.3, apex 11.6 (drawn 10.8), ground-floor windows 3.1–4.9, gable windows 6.5–8.3, porch top 5.7 (drawn 5.5) |
| 93292679 | white rendered villa with the corner tower (pyramid roof), the cross gable at the west end of the front and the balcony | sp03_h331 | 2 (tower 3) | 6.6 / 9.8; tower 8.2 / 10.6 | red tile hip; brown-grey tower roof | white render | measured on the hedge line (camera came out 1.1, taken up by 1.2 to 2.3): tower eaves 8.2, tower apex 10.5, cross-gable apex 8.3, middle eaves 6.8, balcony 4.6; tower size (3.8 m) estimated |
| 93292672 | pale yellow rendered villa, hipped mansard in red-brown tile with dormers, the white curved Jugend gable with an oculus towards Söderportsgatan, two chimneys | kg02_h213, kg03_h213, sp01_h325 | 1 + mansard storey | 5.2 / 10.6 (break 8.8) | red-brown tile hipped mansard | pale yellow render | measured on the east wall plane (Google camera, assumed 2.2–2.5): mansard foot 5.0–5.3, break about 9.2, top seen at 9.6–9.9 on the wall plane (the true ridge is higher; drawn 10.6); the Jugend gable's size and crown (3.6 m above the eaves) estimated from sp01_h325 |
| 93292667 | red boarded two-storey villa, white trim, hipped roof, a dormer on the street, two chimneys | sp04_h322, sp03_h331, sp05_h316 | 2 | 5.5 / 9.6 | red tile hip | falu red boards | measured (camera assumed 2.2–2.6; base behind the hedge): eaves 5.2–5.9; ridge about 9.6 after carrying the reading back to the ridge line |
| 93293034 | yellow boarded cottage | sp01_h145, kl01_h304 | 1.5 | 3.6 / 6.6 | red tile saddle | yellow boards | estimated |
| 93293020 | row of garages | sp01_h145, kl03_h304 (far) | 1 | 2.5 / 2.9 | dark low saddle | brown boards, garage doors | estimated |
| 93293021 | red-brick villa | kg01_h213 (60 m), kl03_h304 (46 m) | 2 | 6.0 / 9.6 | red tile hip | red brick | estimated |
| 93293013 | small red boarded outbuilding | kl03_h304 | 1 | 2.6 / 4.6 | red tile hip | falu red boards | estimated |
| 93293029 | red boarded one-and-a-half-storey house with dormers at the Skansgatan corner | sp06_h131, sp05_h316 (edge) | 1.5 | 4.0 / 8.0 | red tile saddle, dormers | falu red boards | estimated |
| 93292701 | small pale yellow boarded house behind the fence | kg02_h213 (hedge), sp01_h325 (far) | 1 | 3.0 / 5.2 | red tile saddle | pale yellow boards | estimated (barely seen) |
| 93293015, 93293011 | garage and shed | not seen | 1 | 2.5 / 3.1; 2.4 / 3.6 | dark / tile saddle | grey / red boards | estimated |
| 93293018, 93293019, 93293035, 93293040 | houses at the south-west end of Klostergatan and on Skansgatan | kl03_h304 (far, partly trees) or not seen | 2 / 1.5 / 1.5 / 1.5 | 5.4 / 8.4; 3.8 / 7.0; 3.8 / 6.8; 3.8 / 6.8 | red tile saddle | pale yellow, white, red, yellow boards | estimated (plain Gamla stan form, colours from the neighbours) |
| 93293042, 93293027 | yard shed and small cottage | not seen | 1 | 2.4 / 3.8; 2.8 / 4.8 | red tile saddle | red, grey boards | estimated |
| 93238237 | Kungsgatan 13A: pale green section of the 1940s row, entrance with the balcony above | kg07_h212 | 2 over a basement | 7.0 / 8.6 | red tile, shallow | pale green render, 1.2 m grey plinth | measured (camera 1.39 from the base, taken to 2.3): eaves about 7.0, door 0.4–2.6, basement windows to 1.2 |
| 93238276 | yellow section of the row with the white curved window hoods | kg07_h212 | 2 over a basement | 8.0 / 9.6 | red tile, shallow | ochre yellow render | measured: cornice about 1.5 m above the green sections' at the joint (8.0 on the facade plane) |
| 93238230, 93238258 | the next pale green and yellow sections | kg07_h212 (far), kg08_h200 (far) | 2 over a basement | 7.0 / 8.6; 8.0 / 9.6 | red tile, shallow | pale green; ochre yellow | estimated (the alternation continued) |
| 93238271, 93238289, 93238238 | white rendered two-storey 1940s blocks at Ståthållaregatan, chimneys | kg08_h200 | 2 | 6.0 / 9.0 | red tile saddle | white render | estimated (the base readings on kg08_h200 were inconsistent: camera 1.1–1.9) |
| 93326721 | yellow rendered three-storey block | kg08_h200 | 3 | 9.3 / 12.4 | red tile hip | yellow render | estimated (three rows of windows) |
| 93326735 | yellow-brick 1950s houses (a pair) with roof lights and the garage | kg09_h201 | 2 | 5.6 / 8.4 | red tile saddle, roof lights | yellow brick | measured (Google camera, 2.92 from the base): eaves 5.8, ridge seen at 7.3 on the front plane |
| 93291974 | salmon rendered three-storey 1940s block with balconies | kg08_h20 | 3 over a basement | 10.4 / 12.6 | red tile hip | salmon render | estimated (storeys; the plane readings were unusable at that grazing angle) |
| 93326709 | salmon rendered three-storey block with balconies and attic dormers | kg08_h20 | 3 over a basement | 10.4 / 14.0 | red-brown tile saddle, dormers | salmon render | estimated |
| 93326746 | salmon three-storey block at Stensögatan | not seen | 3 | 10.4 / 13.6 | red-brown tile saddle | salmon render | estimated (plain form like 93326709) |
| 93238265 | garden shed behind the red board fence | kg06_h212 (hidden) | 1 | 2.3 / 3.4 | red tile saddle | red boards | estimated |
| 93291960, 93291980, 93291986, 93291987, 93291990, 93291994, 93291997 | garden outbuildings and sheds east of Kungsgatan | not seen | 1 | 2.3–2.6 / 3.3–4.2 | tile or dark saddle | red, grey, yellow boards | estimated |

Colours are read by eye from the photos and set as flat targets on the town textures.

## Estimated

- Every value marked estimated above, and all roof pitches except the measured ridges.
- The ridge direction of houses seen only from one side. The default runs along the long side of the main rectangle.
- Window counts and places: regular bays (2.7 m on two-storey houses, 2.9 m on one-storey and three-storey ones), except on 93293038, whose rows were measured. Only the measured fronts were compared with the photos.
- Doors: one per house, on the street wall, a third of the way along walls over 6 m (centred on 93293038 and 93293023).
- The sizes of the dormers, chimneys, the tower, the Jugend gable, the balconies, the glazed porch and the entrance balcony.
- The 17 houses seen in no photo or only far or behind trees: the sheds east of Kungsgatan, 93326746, 93293011, 93293015, 93293018, 93293019, 93293027, 93293035, 93293040 and 93293042.

## Verification

- **Zones** (`previews/block118-zones.json`): 63 zones cover the 40 outlines, 4915.1 m².
  - 0.11 m² lies outside OSM and 0.11 m² of OSM is not zoned (slivers at the cuts).
  - The overlap is 0.054 m² (the OSM outlines themselves overlap by 0.045 m²).
  - Status: passed.
- **Sandbox**, two runs:
  - The first run (prelude `rebuild_block116`, so pass 117's houses were still in the chunks) printed `BLOCK118_GEOMETRY 42` and `SANDBOX_DONE`. Degenerate faces dropped per house mesh: 0–80, 857 in all (mostly bargeboard and railing rods). The re-created chunks had 1,473,097 (M) and 3,578,998 (W) faces.
  - Pass 117 was committed between the runs, so the second run's prelude was `rebuild_block117`. It went through a wrapper that executes the build twice in one session (`SCR/p118/build_block118_twice.py`) and printed `BLOCK118_GEOMETRY 42` twice and `SANDBOX_DONE`. Degenerate faces dropped: 0–80 per house mesh, 826 in all. Chunk M, now also without pass 117's houses, had 1,016,190 faces, and W had 3,578,998.
- **Repeatability** (second run): `REPEAT118 True`. Both builds give the same 42 meshes with the same vertex counts (5,055,330 in all), 40 `SM_Slott118_` objects and three `SM_Slott98_Buildings_` chunks.
- **Comparison** with the photos (side by side in `SCR/p118/sb1/cmp_*.png` and `sb2/cmp_*.png`), rendered at the photo size from the cameras above:
  - 93293038 (sp03_h151): the front, the windows in two rows, the door with its stone surround, the quoins and the two dormers match in place and size. The model reads a little wider in the frame.
  - 93293023 (sp01_h145): the two-storey cross part with its low gable, the gambrel wings on both sides, the boarded upper windows and the green door match. The yellow cottage 93293034 stands behind on the right as in the photo. On kl01_h304 the back gable and the wings also match.
  - 93293026 (sp04_h142): the raised plinth, the cross gambrel gable on the right and the glazed porch on the left match. The model stands a little nearer (the camera is not resected).
  - 93292679 and 93292667 (sp03_h331, sp04_h322): the white villa with the tower at its east end and the cross gable at the west end, and the red hipped villa, are at the right places and heights. The tower's pyramid roof is steeper and taller in the photo.
  - 93292672 (sp01_h325): the white curved gable with the oculus over a pair of windows, the red-brown mansard and the dormer match in form. The photo shows only the upper part over the fence.
  - Kungsgatan 13A (kg07_h212): the pale green and yellow sections, the higher yellow cornice, the window hoods, the entrance balcony and the grey plinth match. The first run's gables on the street were wrong, and the second run uses a shallow roof instead.
  - kg08_h20 and kg08_h200: the salmon three-storey blocks with balconies, the white two-storey blocks and the yellow three-storey block read correctly. The first run left a full-height sliver of 93326709 without windows, which the second run fixes.
  - 6735 (kg09_h201): the two-storey yellow-brick front, the garage door and the roof lights match. The roof reads lower than in the photo.
- **Pending:** the official build, its two-rebuild repeatability check and the export, which only the official build covers, and the Unreal checks. The lead fills in the build results.

## Limitations

- About ten houses have measured heights; the rest are estimated from storeys. Several "measured" values come from views over hedges, with the camera height assumed.
- The houses are boxes on the OSM outline with rectangular roofs. Small notches in an outline are covered by the roof, and 93293034's irregular outline gives several small flat annexes.
- Window and door positions are regular bays, not the real ones, except on 93293038.
- 93293026's photo also shows a hipped roof part with a gable over the porch. It is simplified to two gambrels.
- 93292679's left cross gable is half-hipped in the photo and drawn as a plain gable. The dark-roofed garage between 93292667 and 93292679 has no OSM outline and is not modelled.
- The Jugend gable's exact curve, 93292672's stair to the garden and the patched mansard (the white tarpaulin on kg02_h213) are not modelled.
- No fences, gates or hedges are modelled, though the photos show many (white and green picket fences, the long red board fence on kg06_h212).
- Extra views that would help, given as location (x, y), Street View heading and pitch:
  - the south-west end of Klostergatan and Skansgatan (93293018, 93293019, 93293035, 93293040) from (−1095, −125), heading 300, pitch 10;
  - the sheds east of Kungsgatan from Lilla Dammgatan (−1075, 160), heading 250, pitch 5;
  - 93326746 from Kungsgatan (−1190, 290), heading 20, pitch 10;
  - 93292672's south front from Söderportsgatan without the fence, (−1034, −50), heading 340, pitch 15.

## Official build

The lead's build of pass 118 passed the Blender geometry checks and the FBX export, and two rebuilds gave identical meshes. Prevhash reports the mainland chunks SM_Slott98_Buildings_W and _M (in their earlier versions) as changed. That is intended, because they are re-created without this pass's 40 houses. The other changes are the earlier intended corrections. The Unreal import and its checks are deferred.
