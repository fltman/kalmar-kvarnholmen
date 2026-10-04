# Pass 110: Storgatan, Norra Långgatan, Södra Långgatan 25 and Västra Sjögatan 4

Pass 110 replaces ten generic district volumes from pass 17 with the houses that stand there. Street fronts are detailed; the backs, courtyards and party walls are plain. Sixteen zones in all (`source/block110.json`).

Storgatan, north side (fronts face south, y ≈ 2.6):

- **91265011 (SM_Building_91265011):** the 1960s two-storey commercial block clad in grey-beige stone slabs. Six equal bays between full-height stone piers along the 52.1 m front; recessed shopfronts, the four western ones wrapped in blue film (NS Fastigheter) and the two eastern ones glazed; a stone fascia band with slab joints; a continuous upper window ribbon with dark mullions; a stone parapet with a dark coping; flat roof. One zone.
- **91970373 (SM_Building_91970373, Viore):** the 13.1 m front range (12 m deep) is a yellow-rendered house over dark stone shopfronts, with eight white-framed windows, a dark eave and a red tile saddle roof. The large rear of the outline is plain and flat-roofed.
- **91970296 (SM_Building_91970296):** the 23.75 m front is split at x −103.4, the line of the OSM rear wing's west wall:
  - west, 12.4 m: the yellow Sakligheter house, with a dark shopfront, a dark green fascia, a nine-window ribbon and a sloped dark green eave; flat roof;
  - east, 11.3 m: the brown granite four-storey Synsam house, with two shop bays between granite piers, a dark canopy and three windows on each upper floor; flat roof;
  - the rear of the outline (beyond 12 m) is plain, flat-roofed, at the pass-17 height 10.2 m.

Storgatan, south side (fronts face north, y ≈ −8.3):

- **92379278 (SM_Building_92379278, Dillbergs Bokhandel):** a limestone-clad ground floor with the teal-framed shop window and entrance at the east end and two roller shutters at the west, a limestone band, salmon render above with paired windows in cream surrounds, cream string course and cornice; a red tile saddle roof.
- **92379304 (SM_Building_92379304):** the narrow limestone slab front: two large brown-framed ground-floor glazings round a stone pier, a glazed door, slab-jointed band, an upper window ribbon, a flat roof.

The other streets:

- **92379276 (SM_Building_92379276, 25 Södra Långgatan):** white render on a grey plinth; four blue-framed upper windows; two shop windows and a glazed blue door under three blue awnings; the blue double door; a blue-framed shop door with a window; a red tile saddle roof with two red dormers; white downpipes. The rear wings (north of y −58.5) are plain and flat-roofed. Its `detail_pass` was checked in the sandbox before replacement (it was generic; the build skips any house whose `detail_pass` is above 17).
- **92412841 (SM_Kvarnholmen_House_92412841, 4 Västra Sjögatan):** sage-green vertical boarding on a dark plinth, lighter corner boards and a storey band, white six-pane windows in white surrounds, the porch with two pilasters and an entablature over the green double door and the window beside it, steps, a steep red tile hip roof and the white lantern dormer with twin lights and a pointed roof. The whole west wall (11.9 m) faces the street; the resection fits the full outline.
- **92204180 (SM_Kvarnholmen_House_92204180, Norra Långgatan):** split along the OSM line through (−132.38, 104.41)–(−132.0, 134.34):
  - west, 18.0 m front: white render, two storeys, six window bays with cream box awnings over the upper windows and over the ground windows, the orange-framed door with a blue sign over it, a plain plinth, a flat roof;
  - east, 18.9 m front: white frame with four bays: dark horizontal louvres over the upper glazing, glazed ground bays, the orange door frame in the first bay; flat roof.
- **91264997 (SM_Building_91264997, Åhléns/Kvasten):** the 75.8 m white front: three glazed gables (glass prisms with white edge frames) over glazed two-storey bays, the recessed entrance under the eastern gable with a red sign strip, cream canopies over the two western bays, narrow windows between the gables, shopfronts in 4.4 m bays east and west of the gables, tall paired windows east of the gables, two window rows west of them; a fascia band, cornice and flat roof. The rest of the outline (west wall, north and east walls) is plain.
- **91970385 (SM_Building_91970385, Norra Långgatan, south side):** split at the OSM rear vertex x −58.67:
  - west, 8.5 m: the orange four-storey house: shopfront with copper frames and a sign, windows in pairs, the pale green glazed oriel over the first and second floors at the west end, a round window above it, flat roof;
  - east, 9.4 m: the beige three-storey house: three large shop windows between copper piers, two rows of three white-framed windows, a red tile saddle roof.

Photos are working references only. No pixel is used as a texture.

## Measurement

Ten photos were used: four Google Street View panoramas and six contributor 360 photos.

| Photo | Building | Camera position used | Camera height | Status |
|---|---|---|---|---|
| bh6gO-wUQ20pN_SDsbjUVQ, heading 332 | 92379276 | (−108.28, −75.81) | 2.6 m | resected on the two house corners on the facade plane y −69.16 |
| uyi1gDDwXxA_2x1aTf3BEA, heading 62 | 92412841 | (−36.47, −113.74) | 2.4 m | resected on the two house corners on the facade plane x −29.35 |
| 6xqkrw3KZK3FLyZd36LxJg, heading 332 (upscaled half tile) | 92204180 | (−135.09, 69.41), Google's position | 2.2 m | not resected (one corner visible); checked by the joint |
| aOa5Gq5FMPYdLuYbug3C2w, heading 332 (upscaled half tile) | 91264997 | (−72.64, 67.37), Google's position | 2.4 m assumed | not resected (no corner visible) |
| CIABIhCEfCs4707CFpAlzU (two views) | 91265011, 92379278 | – | – | contributor photo, style only |
| CIHM0ogKEICAgICz8YaL2A | 92379304 | – | – | contributor photo, style only |
| CIABIhAxqK8hiRyxrUvLfG | 91970373 | – | – | contributor photo, style only |
| CIHM0ogKEICAgIDy3dezPQ | 91970296 | – | – | contributor photo, style only |
| CIHM0ogKEICAgIDy3dezSQ (upscaled half tile) | 91970385 | – | – | contributor photo, style only |

All values are in metres above the pavement; "s" is the distance along the front from the named corner.

**92379276 (s from the west corner).** The resected camera lies 3.3 m south and 0.8 m west of Google's position. The door reads 2.40 m (0.05–2.45), which gives the camera height 2.6 m. Measured: eaves 7.45–7.6; upper windows 4.3–6.1 (1.4 wide, centres about s 3.75, 6.95, 10.35); shop windows s 0.2–2.3 and 3.8–6.5; the glazed door s 2.6–3.6; the double door s 7.24–8.62; the east shop door s 9.16–11.64 to 2.45; awnings 2.05–2.95. The left window reads 1.84 m wide against 1.40 for the others, and no heading correction makes all four equal; I put it at s 1.05 with the common width (±0.4 m). Dormers at s 2.9 and 9.2 are placed by eye (they stand behind the facade plane).

**92412841 (s from the north corner).** The resected camera lies 1.5 m west and 1.3 m south of Google's position. The door is 2.03 m on steps; camera height 2.4 m from it. Measured: plinth top 0.6; door s 10.07–11.33, 0.73–2.76; ground windows 1.6–3.2 at s 1.14, 3.28, 7.48, 9.48; upper windows 4.5–6.3 at s 1.99, 4.44, 8.20 and a small one 5.06–6.44 at s 10.75; porch entablature 3.6–3.85; eaves 6.85. The roof crest in the photo reads higher than any plausible hip over the 10.6 m deep outline (it would need a ridge near 14 m); the model uses a steep hip to 12.6 m (about 47°), which still sits lower in the comparison than the photo.

**92204180.** At Google's position the door reads 2.30 m tall (camera height 2.2 m). The joint between the two parts reads at x −132.7; the OSM rear line extended meets the front at x −132.75. Measured: parapet 7.45 (west), about 7.85 (east); upper windows 3.7–5.9, about 1.9 wide at a 2.85 m pitch; ground windows 0.45–2.85; door 2.30. The window run is fitted to end at the joint (the pano's own readings put the last window 0.3 m over it).

**91264997.** No corner is visible, so the scale rests on Google's position (±3 m) and an assumed 2.4 m camera height; the pavement at the facade is hidden by steps and planters. Read: three glazed gables 5.2–5.3 wide, centres about s 27.3, 34.5 and 42.4; gable base about 9.1, apex about 12.3; entrance about s 39.9–44.9, to 4.6; sign band about 4.8–5.8; tall upper windows in the east part about 6.1–9.2.

**Contributor photos.** Position and heading are not reliable. They give style, materials, storey counts and openings. Scale comes from the doors (2.3–2.4 m) and from storey heights (about 3 m). On Dillbergs, the green door frames give the photographer about 3.2 m from the facade at 1.5 m: ground floor to 4.4 m, first-floor windows 5.3–6.7 m.

| Part | Measured | Estimated |
|---|---|---|
| 92379276 front | eaves, windows, doors, awnings (above) | left window position; dormers; ridge 10.6; rear wings (6.6, flat) |
| 92412841 | openings, plinth, porch, eaves (above) | roof height 12.6 (photo reads higher); lantern size and position |
| 92204180 | joint, parapets, window and door heights, pitch | window run west of the photo's edge; east part bays beyond the photo; all rear walls |
| 91264997 | gable widths and heights, entrance, sign band (pano position, ±3 m along) | cornice 9.3; the west part of the front (not seen); all other walls |
| Storgatan fronts and 91970385 | – | all heights and positions: 91265011 8.2 (pass-17 value), Viore eaves 7.4 / ridge 9.9, Sakligheter 7.6, Synsam 13.4, Dillbergs eaves 10.0 / ridge 12.4 (second floor not seen), 92379304 7.8, orange 12.6, beige 9.8 / ridge 12.0; the 12 m depth of the Storgatan front ranges; the joints in 91970296 (rear wing line) and 91970385 (rear vertex) |

## Verification

- The zones cover the ten outlines: 12 165.6 m² in all, 0.2 m² not zoned, 0.06 m² outside OSM, and no overlap (`previews/block110-zones.json`, BLOCK110_ZONES_OK).
- The sandbox build (prelude: the committed chain to pass 109) ran without errors and printed BLOCK110_GEOMETRY 10 and SANDBOX_DONE. `drop_degenerate_faces110` (with the thin-sliver test) runs on every mesh after `s21_finish`.
- Renders from the resected and nominal cameras were compared with all ten photos:
  - The first comparison found the Åhléns cornice too high above the glazed bays (10.1, now 9.3, with the gable apexes raised to 12.4) and the lantern dormer on Västra Sjögatan too low (moved up the slope and raised); the oriel on the orange house was too dark and is now pale green with frames. In the second comparison the Åhléns gable bases and apexes fall within about 10 px of the photo and the Södra Långgatan 25 eaves, windows, doors and dormers line up; the Västra Sjögatan 4 roof and lantern still sit lower than in the photo (see Measurement).
  - Two sandbox iterations were run.
  - The contributor-photo views can only be compared for style and storeys, since their camera positions are guesses.
- The official build, the FBX export and the Unreal checks are pending; the lead fills in the build results.

## Limitations

- **Contributor photos:** six of the ten houses rest on them. Their dimensions are estimates from door and storey heights; positions of openings along the fronts are approximate (±1 m or more).
- **Joints:** the splits of 91970296 and 91970385 follow OSM vertices that agree with the photos' house order, but they are not measured. Which of Sakligheter and Viore is which rests on the photos' neighbours (the stone block beside Viore).
- **Dillbergs:** only the ground and first floors are seen; the second floor and the roof are estimated.
- **Västra Sjögatan 4:** the roof stays lower than the photo shows (see Measurement).
- **Åhléns:** the front's west 24 m and the east end beyond the photo repeat estimated patterns.
- **Backs:** all walls not facing the photographed streets carry generic windows; the large rear parts are flat-roofed boxes.
- **Omitted:** sign lettering, logos, lamps, planters, benches, flags, cars and the pedestrians.
- **Extra views that would help:** Storgatan from the street (the pedestrian street has no Google car imagery; a frontal view of 92379278 at about (−143, −1), heading 152, pitch 25, to see the second floor and roof); Västra Sjögatan 4 from further away for the roof (about (−40, −111), heading 62, pitch 20).

## Official build

The first official build failed the repeatability audit. `b110_ok` skipped any object with a detail_pass above 17, so the second rebuild, run on the saved blend, found its own meshes marked 110 and skipped all ten (and the recreated M_Block110 materials left their slots empty). The lead changed the guard to skip only other passes (`dp>17 and dp!=110`) and rebuilt. The build then passed the Blender geometry checks and the FBX export, and two rebuilds gave identical meshes. Passes 28–109 are unchanged except the earlier intended changes (pass 85's prison building, corrected by pass 103, and pass 98's three meshes re-created by pass 107). The Unreal import and its checks are deferred.
