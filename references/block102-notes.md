# Pass 102: the far east end of Storgatan and the corner of Östra Vallgatan

Pass 102 replaces seven generic district volumes from pass 17 at the east end of Storgatan with the houses that stand there.

North side (fronts facing south), west to east:
- **93238165 (69):** two cream rendered houses in one OSM way, split at the joint seen in the photo (x 343.6, 15.1 m from the west end).
  - West: three storeys, eaves/cornice 8.2 m, two iron balconies at the west end, a glazed door and a 2.9 m black carriage gate, a low dark hipped roof (not seen; 9.6 m est.).
  - East: two storeys on a grey plinth, eaves 5.6 m, five upper windows, four ground windows plus a glazed door and a narrow window, a cornice, a red tiled saddle roof (ridge 9.3 m est.) with three red gabled dormers (the east one wider, two windows each) and a chimney.
  - The rear parts (wing to y 20.7 and bits behind the west part) are flat at 5.6 / 6.0 m (not seen).
- **93238196:** two falu-red boarded houses with their gables to the street (west: eaves 4.5, apex 6.2; east: eaves 3.9, apex 5.6), white corner and verge boards, dark sheet roofs, chimneys. Between them a 1.85 m bay with a pale blue double gate in a white frame, flat at 3.3 m. A small flat rear part at 3.0 m (est.).
- **93238164:** the grey-green boarded two-storey house on a dark plinth, eaves 5.95 m, ridge 9.0 m (red tile saddle along the street), three upper windows under grey awnings, two ground windows, a pale panelled double door with a top light at the east end. Low flat rear wing (4.0 m, est.).
- **93238222:** the cream rendered corner house at Östra Vallgatan, eaves 7.3 m, red tiled hipped roof (ridge 10.2 m est.) with a roof light and a chimney; four window bays on each street front. It is under scaffolding in both photos; the scaffolding is omitted and the window layout is estimated.

South side (fronts facing north):
- **93199630 (67):** the ochre rendered two-storey house on a 1.05 m grey plinth, with a cream lesene (s 12.9–14.1 from the east end), cream corner lesenes, cream window surrounds, the red double door on three steps (threshold 0.55 m) with a small window beside it, a cornice at 7.8 m and a red tiled saddle roof (ridge 11.0 m est.).
- **93199675:** the garage range: five red chevron-boarded double doors (the two east ones with four top lights) between grey rendered piers under a beam, eaves 3.25 m, red tiled hipped roof (ridge 5.3 m). Its long rear part (to y −45) is flat at 3.0 m (not seen).

Östra Vallgatan:
- **93199606:** the brown brick two-storey house on a 1.2 m pale stone base, eaves 9.0 m. Tall white windows (ground 1.85–4.05, upper 5.55–7.45) with dark brown shutters folded back, a brick band at 5.0 m, a pale frieze under the deep eaves and a low hipped copper-green roof. Split into the east block (the 15 m Östra Vallgatan front, 8.4 m deep), the Storgatan block west of it to x 364.5, and a low walled part (2.6 m, est.) between x 359.55 and 364.5 behind the brick wall on Storgatan.

Mesh names (unchanged from district17): `SM_Kvarnholmen_House_93238165`, `_93238196`, `_93238164`, `_93238222`, `_93199630`, `_93199675`, `_93199606`. None had a detail_pass above 17. The panoramas are working references only. No pixel is used as a texture.

## Measurement

Five photos from four panoramas, pitch 15, vfov 90 (vertical), 700×375.

| Panorama (photo) | Heading | Reported position | Resected / used position | Camera height |
|---|---|---|---|---|
| RtTDAbxcNGvda8V1R3y6hg (69, north) | 332 | (346.96, −6.08) | (348.3, −6.5) | 2.1 m |
| RtTDAbxcNGvda8V1R3y6hg (garages, south) | 152 | (346.96, −6.08) | (348.3, −6.5) | 2.3 m |
| EIjtv1022HQStXC6-ZcpjA (75, red gables) | 332 | (367.06, −6.73) | (366.95, −9.21) | 2.28 m |
| G5VQG0vaqD784ECon7Ihsg (67, ochre) | 152 | (326.36, −6.54) | (322.63, −7.8) | 2.3 m (assumed) |
| SzfRf8LlrLVZX9EEuGhRkQ (Östra Vallgatan) | 242 | (394.01, −18.08) | (394.49, −20.04) | 2.28 m |

**Resection** (points on the facade planes 0.355 m outside the OSM lines; `SCR/p100/res.py`, vfov 90):
- **75 Storgatan:** three-point least-squares on the joints 355.6 (cream/red), 366.03 (red/grey-green) and 376.36 (grey-green/scaffold). Residuals up to 14 px; the middle joint is seen 0.8 m further east than OSM puts it. The OSM joints were kept and the red houses' features scaled to their 10.43 m front (×0.93). Camera height 2.28 m from the base row at two places.
- **69 Storgatan:** the north and south views of the same panorama look in opposite directions, so a two-bearing solve (corner 355.6 north, garage east end 354.79 south) gives (348.30, −6.50) but is poorly conditioned. Base rows give camera heights 1.9 m (north) and 2.8 m (south) at that position; no single position and pitch reconciles both, so heights on each side are taken relative to that side's own base row. The garage front reads 15.5 m wide at y −6.5 against 14.4 m in OSM; a camera at about y −7.2 would fit the width and give 2.4 m doors. Values below are the mean of the two camera positions tried ((348.3, −6.5) and (347.9, −7.1)); spread about ±0.3 m on heights.
- **67 Storgatan:** the house is close and only its west corner is in frame, so x comes from the bearing of the west corner (317.58) and y was chosen so that the red double door leaf reads 2.2 m (y −7.8, 3.85 m from the facade). This is a scale assumption, not a resection. Window heights high in the frame read large (upper windows 2.6 m) and are reduced to 1.9 m.
- **Östra Vallgatan:** two-point fit on the brick house's south and north corners (OSM 386.73/−27.06 and 386.68/−12.06), exact, no redundancy. Camera height 2.28 m from the stone base row. The resected facade width matches the photo to within 5 px at both ends of the render.

**Values read on the facade planes** (m above the local base row):

| House | Openings | Eaves / ridge |
|---|---|---|
| 93238165 east (69) | upper windows 3.3–4.65 (two cameras: 3.13–4.41 and 3.45–4.87), ground 1.10–2.35, about 1.2 wide; dormer windows 5.8–6.75; dormer widths 2.6 / 2.4 / 3.4 | eaves 5.3–5.9 (5.6 used); dormer peaks 7.25–8.0 |
| 93238165 west | top windows 6.0–7.3, middle 3.2–4.6; gate top 2.3–2.6 | cornice 7.9–8.7 (8.2 used) |
| 93238196 west gable house | ground windows 0.92–2.39; upper windows 3.38–4.65 (at the gable foot) | gable feet 4.53–4.55, apex 6.15 |
| 93238196 gate | gate 1.9 m wide (scaled 1.85), top 2.19 | — |
| 93238196 east gable house | ground window 0.75–2.31, upper 3.03–4.62 (in the gable) | gable feet 3.91–3.92, apex 5.59 |
| 93238164 grey-green | upper windows 3.36–4.83, ground 1.02–2.39, about 1.4 wide; door 0.31–2.60 | eaves 5.95; ridge 9.25 (silhouette projected 3.6 m back), 9.0 used |
| 93238222 corner | upper windows 3.23–5.53, ground from 0.31 under the scaffold boards | eaves 7.4–7.5 (75 view), 6.9–7.5 (Vallgatan view) |
| 93199630 ochre | door 0.51–2.69; plinth top 1.04; ground windows 1.2–2.8; small window 1.5–2.6 | cornice 8.1 (7.8 used) |
| 93199675 garages | doors to 2.7–3.0 (camera-dependent; 2.45 used) | beam top 3.26; roof silhouette 4.0 on the facade plane, 5.9 if it is the ridge 5.8 m back (5.3 used) |
| 93199606 brick | stone base top 1.21; ground windows 1.84–4.08, upper 5.47–7.41, about 1.3 wide; band 5.0; frieze to 8.5 | eaves 8.96, roof edge 9.37 |

## Estimated

- All ridges except the gable apexes of 93238196 and the silhouette readings for 93238164 and the garages. Roof forms of 93238165 west (low hip), 93238222 (hip), 93199630 (saddle along the street) and the brick house (low hip; the copper colour is from the garage view) are inferred.
- All rear parts marked est. in `source/block102.json`, and every unseen wall (party and rear walls are plain).
- The west 9 m of 93238165 west (out of frame): window columns at s 1.6/4.6/7.6 continue the seen rhythm; the balconies are placed at s 4.3–7.9.
- 93238222's window layout (four even bays per front) and its door-less ground floor.
- The east 7.8 m of 93199630 (out of frame): ground and upper windows at s 2.0 and 5.2 continue the pattern.
- The brick house's Storgatan and west fronts: same window rhythm (3.75 m bays) as the measured east front. Its west face at x 364.5 is from the eave line of one oblique view (the garage photo): with the OSM line at 359.55 the eave would land 30–40 px too far right and too high. The low walled part west of it is a guess.
- Gable dormer sizes on 69: widths from the photo, depth and the 0.25 m projection in front of the OSM line chosen so the peaks match the photo.

## Verification

- `KALMAR_GEO=SCR/pylib python3 scripts/prepare_block102.py` prints `BLOCK102_ZONES_OK`: footprint 1643.9 m², zoned 1643.8 m², outside OSM 0.0 m², OSM not zoned 0.13 m², overlap 0.0 m².
- Sandbox (prelude rebuild_block101): the build runs and prints `BLOCK102_GEOMETRY 7`; `drop_degenerate_faces102` (with the `_thin` test) runs on every object after `s21_finish`. In sandbox run 1 it dropped 94 / 30 / 52 / 4 / 14 / 244 / 0 faces on 93238165 / 93238196 / 93238164 / 93238222 / 93199630 / 93199675 / 93199606; which faces those are has not been inspected yet (run 2's sample print did not flush before the run was stopped). Run 2 rendered the 69, 75 and 67 views and was then stopped; run 3 (garages, Östra Vallgatan, aerial) was still running when this was written.
- Renders at 700×375 from the cameras above were compared side by side with each photo (`SCR/p102/cmp_*`): eaves, dormers, gable feet, plinths, door and window rows and colours line up within a few pixels on the near facades; see Limitations for the misfits.
- The official build, the FBX export check and the Unreal checks are pending; the lead fills in the build results.

## Limitations

- The 69 panorama's two views disagree on the camera position by about 0.6 m across the street; heights there carry ±0.3 m. In the 69 north render the two-storey front spans u 205–575 against 185–625 in the photo (camera a little far).
- The joint between 93238196 and 93238164 is seen about 0.8 m east of the OSM joint; OSM was kept, so the grey-green house's west 0.9 m is blank boarding and the red houses are squeezed by 7%.
- The 67 camera is scaled on the door, not resected; its west corner falls about 50 px short in the render.
- 93238222 is modelled from scaffolded views; window sizes and the ground floor are approximate.
- The brick house's west extent (x 364.5) rests on one oblique view; a view from Storgatan looking south at about (362, −6), heading 152, pitch 15 would settle it, and would show the house's Storgatan front.
- Drainpipes, lamps, the electricity cabinet, the scaffolding, the diamond vents in the garage doors and the glazed balcony on the brick house's west face are omitted.

## Official build

The lead's build of pass 102 passed the Blender geometry checks and the FBX export, two rebuilds gave identical meshes, and passes 28–101 are unchanged. The final sandbox run (run 3, prelude pass 101) rendered the garage, Östra Vallgatan, ochre and aerial views without errors. The Unreal import and its checks are deferred.
