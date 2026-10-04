# Pass 105: Strömgatan, north-west Kvarnholmen

Pass 105 replaces seven generic district volumes from pass 17 on Strömgatan, and the large block behind it on Södra Kanalgatan, with detailed or re-zoned houses. Strömgatan runs west–east here. The houses on its north side (y ≈ 218) face south onto it, and the houses on its south side (y ≈ 206) face north. The task notes had the facing directions reversed.

- **92204196 (3 Strömgatan, south side):** the olive roughcast three-storey house, 24.4 m long.
  - White lesenes divide it into seven bays. They are wider at the corners.
  - A white string course runs at 3.5 m, with a stone plinth band and a white cornice at 9.7 m.
  - Six window axes with white surrounds on three floors.
  - The centre bay has an arched entrance, a glazed brown double door under a glazed arch with a white arched surround and a step, and an arched window on each upper floor.
  - The roof is a low grey sheet hipped roof (estimated).
  - The rear part (OSM y 176–195) is not seen. It is flat-roofed at 8.6 m with plain windows.
- **92204205 (north side):** the grey rendered four-storey house.
  - The ground floor is pale and granite-looking with horizontal joints. It has a passage with a black bar gate at its west end and six white windows, two of them narrow, each under a small grey canopy.
  - Two box bays (3.3 m wide, 0.6 m deep) run over the second and third floors, from 3.0 to 8.9 m. Each has four-light French windows behind glazed balustrades.
  - Two flat windows per floor stand beside the bays, and there is a fourth-floor window row.
  - A cornice at 11.6 m, a dark mansard (top 14.2 m) and two dormers over the bays.
- **92204158 (north side):** the red brick three-storey house on a dark plinth.
  - Four low ground-floor windows and a low red double gate.
  - At the east end, an arched door in a white surround and a white-framed box window.
  - Three wide windows on the second floor and four on the third, all under grey arched hoods.
  - A large three-light arched window over the door.
  - A brick cornice at 10.0 m, a steep dark mansard (top 12.8 m) and four box dormers.
- **92204154 (north side, west end):** brick upper floors with white window surrounds, white quoins and a white band over a pale rusticated ground floor (to 4.7 m). It has a hipped roof, and its rear wing is flat-roofed. Only the east end of this house is seen.
- **92204191 (north side):** the small green rendered house with an orange tile saddle roof along the street. It has generic `plain` openings.
- **92379281 (10 Strömgatan, south side):** the yellow brick house with four storeys, 29.8 m long.
  - A granite plinth, black window frames and stone sills.
  - Brick string courses at 4.1, 7.0 and 10.0 m.
  - An arched black double gate with boarded leaves and a glazed fanlight.
  - A red door at the back of a 1.0 m deep brick niche, reached by steps.
  - Eleven window axes.
  - The fourth floor, the cornice and the roof are estimated.
  - The rear wing running south is generic, with a saddle roof running across the front.
- **91285791 (Södra Kanalgatan):** not photographed. It is modelled at a generic level: a pale rendered volume at the district height of 9.75 m, plain windows on three levels, a flat roof (triangulated, because the outline is concave) and a parapet coping.

Mesh names (unchanged from district17): `SM_Kvarnholmen_House_92204154`, `_92204196`, `_92204205`, `_92204158`, `_92204191`, `_92379281`, `_91285791`. All had no detail pass above 17. The panoramas are working references only. No pixel is used as a texture.

## Measurement

Four photos from three panoramas, pitch 15, vfov 90 (vertical), 756×405. The 92204158 and 92379281 photos are upscaled half tiles. Resection used `SCR/p100/res.py` (vfov 90), on facade planes 0.355 m outside the OSM lines.

| Panorama (photo) | Heading | Reported position | Resected position | Camera height | Resection points |
|---|---|---|---|---|---|
| zkG4Pxo2MFqruJ_tt9W1Wg (92204196) | 153 | (−229.37, 215.50) | (−230.35, 213.99) | 2.25 m | 196's two street corners (exact fit) |
| zkG4Pxo2MFqruJ_tt9W1Wg (92204205) | 333 | (−229.37, 215.50) | (−230.23, 213.16) | 2.50 m | 205's joints with 154 and 158, two readings each (least squares) |
| vlPEOIuk4PimMNaGh2Bvuw (92204158) | 332 | (−213.78, 213.42) | (−214.02, 210.73) | 3.03 m | 158's joints with 205 and its east corner, two readings each |
| xFBtzu-1G2t6rPkBFQP9xg (92379281) | 153 | (−136.49, 211.77) | (−136.49, 210.30) | 2.40 m (assumed) | no corner in view, see below |

**Camera notes.**
- **One panorama, two solutions:** the two headings of zkG4P give positions 0.8 m apart. A joint fit leaves about 0.5 m residuals at every corner, so each photo uses its own fit. That way each facade is scaled by its own OSM length. The cause is probably a heading offset between the two views or an error in the OSM lines.
- **The 92204205 view:** its camera height comes from the pavement line at the bottom of the frame (z = 0). The 92204196 view's height comes from the door threshold on a step (0.15 m). The two disagree by 0.25 m, which is within the error of these readings.
- **The 92204158 view:** the pavement line gives an implied camera height of 3.03 m, which is unusually high. The resected camera is 2.7 m south of the reported one. Heights in this view were therefore taken relative to the pavement line, which keeps the ratios. A vfov sweep from 80 to 110 changes the eaves only between 9.87 and 10.03 m. The same view reads 92204205's lower floors about 8% taller than its own view does, so 205's upper heights were averaged between the two views.
- **The 92379281 view:** no corner is in the frame. The camera's distance comes from the pavement line with an assumed height of 2.4 m (4.4 m to the facade plane). Its position along the street is the reported one, so positions along this front carry about ±1.5 m. Heights scale with the assumed camera height: ±0.2 m in height gives about ±8%.

**Values read on the facade planes** (m above the pavement; s along the street front):

| House | s from | Openings (s centre, width, bottom–top) | Eaves / top |
|---|---|---|---|
| 92204196 | east corner | lesenes about 0.30, 3.14, 6.45, 10.0, 14.0, 16.97, 20.15, 24.1; windows 1.6 / 4.97 / 8.35 / 15.43 / 18.8 / 22.07, about 1.3 wide, rows 0.76–2.63, 4.33–5.90, 7.00–8.59 (axes made symmetric about 12.1); arched door 12.1, 1.8, 0.15–2.92 (spring 2.21); arched windows 4.33–6.18 and 7.00–8.89; string course 3.48 | eaves 9.72 (both ends 9.43–9.77) |
| 92204205 | west joint | passage 0.35–1.75 to 2.6; ground windows 2.87 / 6.18 / 8.9 / 10.08 / 12.63 / 15.82, 1.05–2.54; band 2.79–3.03; bays 4.67–7.92 and 10.34–14.12 (read on the wall plane, so they come out wide), bay windows 3.23–5.46 and 5.86–8.0, bay lid about 8.5–9.1; flat windows 3.74 / 14.75, 3.82–5.54 and 6.71–8.67 | cornice 11.1 (scaled from the 158 view) to 12.1; mansard top estimated |
| 92204158 | west joint | low windows 6.13 / 7.43 / 9.93 / 11.13, 0.85, 0.50–1.39; red gate 1.53–4.09, 0.39–1.49; door 12.82–14.23, top 1.93; box window 14.3–17.1, 0.5–1.6; 2nd-floor windows 3.07 / 6.70 / 10.20, 2.84–3.96, hoods to 4.93; arched window 12.65–15.58, 2.87–4.97; 3rd-floor windows 3.47 / 6.73 / 9.77 / 13.4, 6.26–7.45, hoods to 8.16; dormers about 3.5 / 6.45 / 9.25 / 12.55, 10.3–12.0 or higher | cornice 9.67, eaves 9.98 |
| 92204154 | west end | rustication top 4.66; one 2nd-floor window at 13.66–14.54, 5.35–7.29; brick still visible at 10.34 | eaves not seen |
| 92204191 | west end | seen through the gap east of 158, obliquely | eaves about 6.4 (one reading) |
| 92379281 | east end | plinth top 0.52; gate 6.62–9.50, 0–2.54, crown 2.91; red door niche 18.34–19.76, top 3.0; ground windows 10.6 / 12.68 / 14.95 / 16.98, 1.1–2.96; upper axes 3.15 / 5.5 / 8.15 / 10.55 / 12.65 / 14.95 / 17.0 / 19.3 / 22.0; windows 4.23–5.94 and 7.21–8.91; bands 4.06 and 7.04 | top cut off |

## Estimated

- **Roofs:** none of the roof forms is seen except 158's mansard and dormers, and the bottom of 205's mansard in the 158 view. These values are assumed:
  - 196's low hipped roof, ridge 11.6 m;
  - 154's hipped roof, eaves 11.6 m and ridge 13.8 m, from three storeys over the 4.7 m ground floor;
  - 191's saddle roof, eaves 6.3 m and ridge 9.3 m;
  - 281's saddle roof, ridge 16.4 m over eaves 13.1 m. The eaves come from a fourth storey at the measured 3.0 m storey height.
- **Mansards:** the mansard profiles (inset and rise) are fitted by eye to the 158 view. 205's dormers are placed over its bays, and only one of them is seen.
- **92204205:** the fourth-floor window row (9.75–10.85 m) and the cornice at 11.6 m are an average of two views that disagree by about 8%.
- **Unseen walls:** the window layout of 92204154 west of the one seen window, its door and its rear wing are estimated. So are 92204191's openings, 92379281's ground-floor axes outside s 5.5–20.6, its rear wing, and all of 91285791. The rear part of 92204196 is also estimated: it is flat at 8.6 m, and 92204154's rear wing is flat at 8.6 m as well.
- **Colours** are by eye from the photos.

## Verification

- **Zones** (`previews/block105-zones.json`): 10 zones in 7 meshes, footprint 4723.7 m², zoned 4723.7 m², 0.05 m² outside OSM, 0.03 m² not zoned, overlap 0.0 m². `prepare_block105.py` prints `BLOCK105_ZONES_OK`.
- **Sandbox:** two runs, both printed `SANDBOX_DONE` without errors. The first used the pass 103 prelude, the second the pass 104 prelude. Renders were made from the four resected cameras at photo size and compared with the photos (`SCR/p105/cmp_2_v*.jpg`), plus an aerial.
  - **92204196:** corners, eaves, lesenes, string course, window columns and rows, the arched door and the arched windows line up within about 10 px. The model sits a few pixels low in frame, which suggests the camera is 0.1–0.2 m too high.
  - **92204205:** the ground windows, bays and side windows line up within a few pixels.
  - **92204158:** the window rows, hoods, the arched window, the door, the box window and the dormer positions line up. The mansard reads somewhat shorter than in the photo.
  - **92379281:** the window rows, the gate and the red door niche line up. The upper floors are cut off in the photo.
  - **Changes in the second run:** 158's mansard made steeper and its dormers brought forward and taller; 205's bay windows set to the measured French-window heights; 281's ground windows lengthened to the measured 1.1–2.96 m; the grey render and the brick lightened.
- **Degenerate faces:** `drop_degenerate_faces105`, with the `_thin` test, runs after `s21_finish` on every mesh. In the sandbox it removed 80, 0, 49, 12, 14, 49 and 9 faces from 92204196, 92204205, 92204158, 92204154, 92204191, 92379281 and 91285791. These counts are in the range earlier passes report. The removed faces were not sampled individually.
- **Pending:** the official build, its geometry checks and the Unreal checks. The lead fills in the build results.

## Limitations

- **Coverage:** each detailed house is seen in one photo, near-frontally, and no rear is seen. 92204154 and 92204191 are seen only at the frame edges of the neighbouring views.
- **Scale:** the 92379281 view has no corner, so its along-street positions and its absolute scale depend on the assumed camera height.
- **Disagreement between views:** the two views of 92204205 disagree by about 8% in height.
- **91285791:** not photographed and generic. A view would be needed to detail it.
- **Omitted:** cars, signs, the street lamp on 196, downpipes, the ventilation grilles under 205's windows, the decorative brick crosses under 281's eaves, and the fence in the gap east of 158.
- **Extra views that would help:**
  - 92379281 from further east or west on Strömgatan, to show a corner, the top floor and the roof. For example local (−150, 212), Street View heading 92 (local bearing 120), pitch 25.
  - 91285791 from Södra Kanalgatan, local (−100, 262), heading 150, pitch 15.
  - 92204154 and 92204191 head-on: local (−246, 212), heading 333, pitch 20, and (−195, 212), heading 333, pitch 15.

## Official build

The lead's build of pass 105 passed the Blender geometry checks and the FBX export, and two rebuilds gave identical meshes. Passes 28–104 are unchanged, except pass 85's prison building, which pass 103 deliberately corrected. The Unreal import and its checks are deferred.
