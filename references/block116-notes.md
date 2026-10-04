# Pass 116: Gamla stan, Molinsgatan and the east part of Västerlånggatan

Pass 98 built the mainland houses as plain volumes inside three chunk meshes. Pass 116 is the first Gamla stan pass. It takes 37 of them out of the chunks. Each becomes its own mesh, `SM_Slott116_<osm id>` (category `Slottsområdet/Gamla stan`, `detail_pass` 116), with its real form:

- storeys (1, 1.5 or 2) and the eaves and ridge heights;
- the roof: saddle, hip, Swedish mansard (gambrel, with gable ends) or a shallow hip, in red tile, black tile, black sheet metal, dark or grey metal;
- the walls: vertical boarding (battens over the wall, white corner boards) or render, in the house's colour (falu red, yellow, pale yellow, white, pink, light blue, dark brown, blue-grey, grey-green, sage, cream, dark green), on a grey stone plinth;
- eaves boards, white (red on 93306350, the frame colour on the boarded houses) bargeboards on the gables;
- windows per storey (casements with surround and sill; red-brown frames on 93332250 and 93309091, ochre on 93332240), gable windows on the steeper gables, a door on the wall that faces the street (not on the three houses whose street front is seen without one), steps where the door stands on the plinth;
- dormers, chimneys and the notable features listed in the table.

## Selection

The selection is computed in `scripts/prepare_block116.py` from the OSM street lines in `references/osm-slott98.json` (ways with `highway` and `name`): Molinsgatan (w38177105) and Västerlånggatan (w37732304, w38177114, w543050232). It takes every outline in `source/block98.json['buildings']` whose polygon lies within 25 m of Molinsgatan, or within 25 m of Västerlånggatan with its centroid at x > −930, and leaves out pass 115's fourteen ids. Of pass 115's houses, 93332243 (Slottshotellet) and 93332252 (Västerlånggatan 1) would have been selected; they are excluded.

The 37 ids: 93306337, 93306339, 93306341, 93306345, 93306347, 93306350, 93306353, 93306358, 93306359, 93306360, 93309084, 93309091, 93309092, 93332235, 93332236, 93332237, 93332238, 93332239, 93332240, 93332241, 93332244, 93332245, 93332246, 93332247, 93332250, 93332251, 93332253, 93332254, 93333618, 93333625, 93333634, 93333644, 93333651, 93333661, 93333666, 387312777, 1433973300.

All lie in pass 98's chunks M (−1150..−850) and E (x ≥ −850).

## Zones

Each outline is split into rectangles for its roofs (`decompose` in the prepare script):

- An outline that fills 85 % of its box in the frame of its longest edge is one zone; its roof stands on the box.
- Otherwise the outline is cut into slabs at its vertices along the longest edge. Where the slabs share a depth of at least 3 m (and half the largest depth), that full-length strip is the main body and the rest are wing pieces (an L, a T, a bump at the back). Otherwise the slabs are merged by depth.
- The largest rectangle is the main body with the house's eaves, ridge and roof. The others are wings with the same eaves and a ridge lowered in proportion to their width, or one-storey flat-roofed annexes when under 12 m² or narrower than 2.6 m.
- Molinsgatan 6 (93332253) has explicit rectangles from its photo: the two-storey house on its 6.2 m street edge, 15.5 m deep; the cottage on its 5.45 m street edge, 9.6 m deep; the rest of the outline is the low link (2.8 m).
- Each zone's walls follow the OSM outline exactly (zone = outline ∩ rectangle); walls against a neighbouring zone start at the neighbour's eaves.
- For each zone the outer wall facing the nearest of the two streets is stored (`street_wall`) and carries the door.

`SLOTT98_DETAILED` gets the 37 ids, and `slott98_chunks115({'M','E'}, 116, block116_names)` (pass 115) re-creates `SM_Slott98_Buildings_M` and `_E` without them. The chunks are listed among this pass's meshes (39 names in all) and keep `detail_pass` 98 with `rebuilt_by_pass` 116.

## Measurement

The photos were captured for the pass (`SCR/p116`, `captures.txt` lines starting `116|`): 28 views, 728 × 419, vertical field of view 90°, pitch +10°, every ~28 m along both streets looking to both sides.

- **Identities.** All OSM outlines within 70 m were projected into every view from the Google positions (`SCR/p116/ov116.py`, overlays `ov_*.png`; plan `plan.png`). Every house in the table was matched this way, by bearing ranges and distance.
- **Resection.** Where two outline corners are clear, the camera was found by a grid search within 8 m of the Google position that fits their bearings (`SCR/p116/m116.py`, `grid_resect`), with the street side as a tie-break; heights were then read on the plane of the named wall (`hit`). With two corners the fit is exact, so the residual says nothing; a third corner (the cottage's on m03) missed by 12°, which is an OSM or identification error, so that camera is the least-shift solution.

| Panorama (view) | Google position (x, y) | Camera used (x, y), height | How | Used for |
|---|---|---|---|---|
| rVLziobSL4A34v5b4dSVhA (m03_h16) | (−792.6, 70.3) | (−795.0, 68.5), 2.32 | two gable corners of 93332253 (the Google position is 1.6 m from the wall, which the view contradicts) | Molinsgatan 6 |
| 4IgCsnTHNV-kM3oVdi3dlA (m04_h16) | (−807.7, 84.4) | (−813.9, 85.2), 2.67 | two gable corners of 93332235; a 6.2 m shift, mostly along the street | 93332235 |
| 7_rqmQqy2mIdY8aUUjLfsA (v08_h329) | (−911.6, 119.9) | (−911.6, 117.9), 1.48 from the hedge line, taken as 2.3 | two front corners of 93309084 | Västerlånggatan 14 |
| Tu7Q8I5BOB4eRe5imZJWpA (m02_h196, m02_h16) | (−771.0, 49.5) | Google, 2.0 from the base row | the corner of 93306345 projects on the photo's corner (u 365) | 93306345, 387312777, 93332240 |
| al-YkiwWIhlP3qV8D2YRIQ (v07_h329) | (−881.1, 121.3) | Google, assumed 2.2 | the right front corner of 93309091 projects at u 375 against 370 in the photo | Västerlånggatan 12 |
| all other views | Google | Google, 2.2 | identification and storeys only | the rest |

### Houses

Heights are metres above the ground (model z 0.30). "Measured" means read with the cameras above; everything else is estimated from storeys, doors and windows (one storey ≈ 3.0–3.4 m to the eaves, two storeys ≈ 5.4–5.8 m) and roof pitch by eye.

| OSM id | Identity | Photo | Storeys | Eaves / ridge | Roof | Walls | Measured or estimated |
|---|---|---|---|---|---|---|---|
| 93332253 | Molinsgatan 6: red boarded two-storey house with its gable on the street; the red cottage beside it (gable on the street, 3.0 / 5.2); the low link with the entrance | m03_h16 | 2 | 5.8 / 7.9 | red tile saddle | falu red boards | measured: eaves 5.76–5.85, apex 7.88, windows 0.95–2.3 and 3.9–5.2, wall width s −0.2..6.5 against 6.2 m; the cottage and link estimated |
| 93332235 | pale yellow one-storey gable house with carved bargeboards (no. 11 gate beside it) | m04_h16 | 1 | 3.4 / 5.4 | red tile saddle, carved bargeboards | pale yellow boards | measured: eaves 3.37–3.47, apex 5.42, plinth 0.7 |
| 93332250 | white boarded gable house with red window frames, gable to Molinsgatan | m05_h8, v05_h150, v04_h157 | 2 + attic | 5.4 / 8.8 | red tile saddle | white boards | estimated (storeys and gable windows by eye) |
| 93332244 | long white range with dormers | m05_h8 (roof), v04_h157 | 1.5 | 4.0 / 7.6 | red tile saddle, dormers | white boards | estimated |
| 93332251 | small shed with a tile roof | m05_h8 | 1 | 2.4 / 3.9 | red tile saddle | white boards | estimated |
| 93332238, 93332239 | red houses behind 93332235 | m04_h16 (roofs only) | 1.5 | 3.8 / 6.4 | red tile saddle | falu red boards | estimated |
| 93332247 | red rendered house with dormers in the courtyard (four zones) | m02_h16, v02_h178 (far) | 1.5 | 4.4 / 8.0 | red tile saddle, dormers | red render | estimated |
| 93332246, 93332241, 1433973300 | house and two yard sheds inside the block | not seen | 1.5 / 1 / 1 | 3.8 / 6.4; 2.4 / 3.6 | red tile saddle | falu red boards | estimated (plain Gamla stan form) |
| 93332240 | sage rendered house with a dormer and balcony on the courtyard side | m02_h16 | 2 | 6.0 / 9.4 | slate-grey saddle | sage render, ochre frames | eaves about 6, scaled from a reading with an unresected camera (camera height came out 1.26, scaled to 2.2) |
| 387312777 | dark green corrugated store | m01_h196, m02_h196 | 1 | 3.9 / 4.4 | dark low saddle | dark green ribs | measured: top 4.1–4.6 (Google camera, height 2.5 from the base) |
| 93306345 | grey-green rendered 1940s block, raised ground floor, two glazed stair bays, chimneys | m02_h196, m03_h196 | 2 + basement | 8.2 / 10.0 | dark low hip | grey-green render, 1.2 m plinth | measured: eaves 8.39–8.43, chimney top 10.4, ground-floor sills 2.1, door 2.45 (Google camera, height 2.0) |
| 93306337 | dark boarded house | m03_h196 (edge) | 1.5 | 4.0 / 6.6 | dark saddle | dark brown boards | estimated |
| 93306339 | dark brown boarded two-storey gable house at the corner of the two streets | v06_h149 | 2 | 5.4 / 8.0 | grey saddle | dark brown boards | estimated (two rows of windows) |
| 93306347 | red boarded house with white trim and the ornamented chimney | v05_h150, v06_h149 | 2 | 5.2 / 8.0 | red tile saddle | falu red boards | estimated |
| 93306358 | red boarded two-storey house with white trim | v06_h149 (far) | 2 | 5.4 / 8.2 | red tile saddle | falu red boards | estimated |
| 93306341 | dark blue-grey house with a mansard roof | v05_h150, v06_h149 (far) | 1.5 | 3.6 / 7.0 | red tile mansard | blue-grey boards | estimated |
| 93333661 | cream rendered two-storey house with deep eaves (four zones) | v10_h15, v01_h344 | 2 | 6.4 / 8.6 | red tile shallow hips, 0.9 m eaves | cream render | estimated |
| 93333644 | pink boarded villa with the carved glazed veranda at its south-west corner and a red chimney | v02_h358, v01_h344 | 1.5 | 4.0 / 7.4 | red tile saddle (gables east and west), carved bargeboards | pink boards | estimated; veranda 3.2 × 2.2 × 3.1 m |
| 93333651 | light blue house with its gable on the street | v03_h355 | 1.5 | 4.0 / 7.6 | red tile saddle | light blue boards | estimated |
| 93333666 | Västerlånggatan 6: yellow cottage with the red garage door | v03_h355 | 1 | 3.0 / 4.9 | red tile saddle | yellow boards | estimated |
| 93333625 | house behind 93333618 | not seen | 2 | 5.4 / 8.4 | red tile saddle | ochre boards | estimated (plain Gamla stan form) |
| 93333618 | white boarded two-storey house | v04_h337 | 2 | 5.6 / 8.4 | red tile saddle | white boards | estimated |
| 93333634 | white rendered corner villa, the yellow boarded porch at its east end | v06_h329, v05_h330 | 2 | 6.0 / 9.4 | red tile hips | white render | estimated |
| 93309091 | Västerlånggatan 12: white rendered one-storey house, black sheet-metal hip, two chimneys, wooden double door, red-brown frames | v07_h329 | 1 | 3.5 / 5.6 | black metal hip | white render | measured: eaves 3.46, door top 2.24, ridge about 5.6 (from 4.26 read on the wall plane, carried back 4 m to the ridge line) |
| 93309084 | Västerlånggatan 14: red boarded two-storey villa with the central gable, porch roof over the door, two chimneys | v08_h329 | 2 | 5.7 / 9.0 | red tile saddle, frontispiece | falu red boards | measured: eaves 4.93–4.96 and gable apex 8.63 above the hedge line; the camera height came out 1.48, so the base is hidden by the hedge and the readings are taken up by 0.8 m (camera 2.3); frontispiece s 5.6–8.4 (2.8 m) on a 14.1 m front; the ridge is estimated |
| 93309092 | house under renovation, wrapped in plastic | v07_h329 (edge) | 1.5 | 3.6 / 6.4 | dark saddle | grey boards | estimated; v06_h329 shows the street end of the outline as an open yard behind a red fence, so the outline may be larger than the house |
| 93306360 | white boarded two-storey house | v07_h149 | 2 | 5.6 / 8.4 | red tile saddle | white boards | estimated |
| 93306359 | house behind the trees | not seen (v07_h149 is all trees) | 2 | 5.4 / 8.2 | red tile saddle | pale yellow boards | estimated (plain Gamla stan form) |
| 93306350 | yellow one-storey house, black tile roof, red eaves board, red dormer | v08_h149 | 1 | 3.3 / 6.4 | black tile saddle, one dormer | yellow boards | estimated |
| 93306353 | white cottage with a mansard roof | v09_h121 | 1 | 2.8 / 5.6 | red tile mansard | white boards | estimated |
| 93332237 | yellow boarded two-storey house | v02_h178 | 2 | 5.6 / 8.5 | red tile saddle | yellow boards | estimated |
| 93332254 | Västerlånggatan 5: yellow one-storey house, white panelled door, chimney | v03_h175 | 1 | 3.4 / 6.0 | red tile saddle | yellow boards | estimated |
| 93332236 | white boarded outbuilding with a mansard roof and a window in its gable on the street | v04_h157 | 1.5 | 2.6 / 5.8 | red tile mansard | white boards | estimated |
| 93332245 | yellow boarded two-storey house | v04_h157 | 2 | 5.5 / 8.2 | red tile saddle | yellow boards | estimated |

Colours are read by eye from the photos and set as flat targets on the town textures.

## Estimated

- Every value marked estimated above, including all roofs' pitches except the two measured gables.
- The ridge direction of the houses seen only from the side; the default is along the long side of the main rectangle, and 93333644, 93333651 and 93332253 were set from their photos.
- Window counts: regular bays (2.7 m on two-storey houses, 2.9 m on one-storey ones, 1.9 m on Västerlånggatan 12). Only the measured fronts were checked against the photos.
- Doors: one per house, on the street wall; the position along the wall is a rule (a third of the way along walls over 6 m).
- Chimney places, dormer counts (one per 6 m of slope) and the veranda, porch and stair-bay sizes.
- The seven houses not seen in any photo, and 93309092.

## Verification

- **Zones** (`previews/block116-zones.json`): 63 zones cover the 37 outlines, 4004.4 m².
  - 0.07 m² lies outside OSM and 0.36 m² of OSM is not zoned (slivers at the cuts).
  - The overlap is 0.074 m² (the OSM outlines themselves overlap by 0.007 m²).
  - Status: passed.
- **Sandbox** (prelude `rebuild_block115`), four runs:
  - The first stopped on a wrong call (`diamond83` in the veranda frieze); fixed.
  - The second and later runs printed `BLOCK116_GEOMETRY 39` and `SANDBOX_DONE`.
  - Degenerate faces dropped per house mesh: 0–69, 705 in all (mostly the rods of bargeboards and railings).
  - The chunks re-created by this pass have 609,728 (E) and 1,887,328 (M) vertices, against 1,021,625 and 1,988,224 before.
- **Repeatability**, run in the sandbox through a wrapper that executes the build twice in one session (`SCR/p116/build_block116_twice.py`): both runs give the same 39 meshes with the same vertex counts (2,957,080 in all in the last run), 37 `SM_Slott116_` objects and three `SM_Slott98_Buildings_` chunks.
- **Comparison** with the photos (side by side in `SCR/p116/sb2/cmp_*.png` and `sb4/cmp_*.png`), rendered at the photo size from the cameras above:
  - Molinsgatan 6: the two-storey gable, its windows and the cottage's gable beside it match in place and size.
  - 93332235: gable, carved bargeboard and wall height match; the 6 m camera shift makes this the weakest resection.
  - Västerlånggatan 14: the form, central gable, chimneys and windows match; the model reads slightly smaller (the camera height is uncertain).
  - Västerlånggatan 12: the white walls, black hip and two chimneys match; the door is out of the render's frame because the house sits a little further right than in the photo (camera offset).
  - 93306350: the long front, red eaves board, black roof and dormer match; the photo's dormer has an arched window, the model's is rectangular.
  - 93306339: form and storeys match; the dark brown renders greyer than the photo under the studio light.
  - 93332236 and 93333651: the gables face the street as in the photos (after the second run's fix).
  - 93306345: the length, raised ground floor and stair bay read correctly; the roof is barely visible in either image.
  - 93333644: the veranda first rendered as a solid box; the last run makes it glazed (see `sb4/cmp_v02n.png`).
  - Several Google positions stand too close to the houses (m05, v05_h150, v02_h358), so those renders are cut by the house itself; they were used for identification only.
- **Pending:** the official build, its two-rebuild repeatability check and the export, which only the official build covers, and the Unreal checks. The lead fills in the build results.

## Limitations

- Only six houses have measured heights; the rest are estimated from storeys. Roof pitches are mostly estimated.
- The houses are boxes on the OSM outline with rectangular roofs; small notches in an outline are covered by the roof.
- Window and door positions are regular bays, not the real ones, except where noted.
- 93309092: the outline and the photos disagree (open yard at its street end, a wrapped house at its north side).
- No fences, gates or gateways are modelled, though the photos show many (the white double gate beside 93332235, the blue gate beside 93306339, the white gateway by 93332237).
- The arched dormer window of 93306350, the lattice windows of 93333644 and the carved porch of 93333634 are simplified.
- Extra views that would help, given as location (x, y), Street View heading and pitch:
  - the courtyard houses 93332246/93332247 from (−760, 85), heading 330, pitch 10;
  - 93306359 behind the trees from (−895, 95), heading 30, pitch 10;
  - 93333661 and 93333644 from Västerlånggatan's east end (−715, 102), heading 300, pitch 10.

## Official build

The lead's build of pass 116 passed the Blender geometry checks and the FBX export, and two rebuilds gave identical meshes. Prevhash reports the mainland chunks SM_Slott98_Buildings_E and _M (pass 98, 107 and 115 versions) as changed. That is intended, because they are re-created without this pass's 37 houses. The other changes are the earlier intended corrections. The Unreal import and its checks are deferred.
