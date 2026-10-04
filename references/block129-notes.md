# Pass 129: Kalmar slott, the courtyard's dormers, doors and portals

Pass 129 corrects details of Kalmar slott's courtyard that passes 27, 124 and 127 had placed by rule or left open:
1. the dormers on the courtyard slopes;
2. the doors at courtyard level on NE, SE_w and SE_e, and SE_e's outside stair;
3. portal D on NE: it moves to its door and stands on a 3-step stair;
4. portal C on NW: rebuilt to its measured height and form;
5. camera 690 (the 2022 well photograph): re-resected. It looks at the **east** corner.

| Mesh | Category | Status | What changed |
|---|---|---|---|
| `SM_Kalmar_Slott` | Kalmar slott/Castle | re-created, `detail_pass=129`, `corrects_pass=27,124,126,127,128` | dormers; courtyard doors on NE, SE_w, SE_e; portal D's raised arched door; SE_e's stair moved; portal D's stair; the gate passage's arch in the NW front |
| `SM_Castle124_Portals` | Kalmar slott/Castle | re-created, `detail_pass=129`, `corrects_pass=124,126` | portal D moved and rebuilt; portal C rebuilt. Portals B, E and F are unchanged |
| `SM_Castle124_Paving` | Kalmar slott/Ground | re-created, `detail_pass=129`, `corrects_pass=124,126` | the slab path to portal D now runs to the foot of its stair. Everything else is unchanged |

No other mesh changes (sandbox: `CHANGED129` lists exactly these three). The roofs, chimneys (pass 128), rows, rustication and Kungstrappan are as before.

**Method.** `build_block129.py` runs pass 128's composition again: the slice of `build_block128.py` from `def rep128` to `NS128=dict(globals())` gives `build_block127.py`'s source with pass 128's three edits. Pass 129 then makes its own single replacements on that source, each asserted to occur exactly once:
- Marking: `mark127` marks the meshes `detail_pass=129`, with `corrects_pass` `27,124,126,127,128` for the castle and `124,126` for the portals and the paving.
- `B127D['stairs']` is replaced by `source/block129.json`'s stairs.
- In pass 127's `EXTRA127`:
  - `filt127` treats portal D's raised arched door (`ARCHUP129`) as a door;
  - `raised127` skips stairs whose door is arched (portal D's);
  - `dormers127` calls `dormers129`.
- `EXTRA129` (new helpers: `doors129`, `solid129`, `dormers129`) runs in pass 27's namespace after `EXTRA127`.
- Pass 27's courtyard door rule (`doors=([...] if L>12 else [])+raised127(p,q)`) becomes `doors129(p,q,L)+raised127(p,q)`: the measured doors on the four edges this pass covers, pass 27's rule elsewhere. The raised arched door is drawn with `arch_door27`.
- Pass 127 cut pass 124's code after the castle. Pass 129's `cut129` keeps the castle and then pass 124's **portal** and **paving** sections, as pass 126 composed them. The passage and the well house are not run, so they keep their pass 126 versions. `edit_portals129` makes these edits in the portal and paving sections:
  - portal C's block (16 lines) gives way to `portal_c129`;
  - portal D's door becomes `(CI7, CI6)` at the measured `u`, on the landing; its body gives way to `portal_d129`;
  - the paving's target for D follows.
- The gate hole in pass 124's `court_front124` takes portal C's measured arch.

`drop_degenerate_faces129` (with `_thin`) runs on all three meshes; it removes 0 faces. The positions are computed in `scripts/prepare_block129.py` and written to `source/block129.json` and `previews/block129-zones.json`.

## 1. Dormers

Pass 27 put four red-fronted dormers (`roof_dormer`, arched head) at fixed fractions of SE_w, NE, NW and SW. Pass 127 kept them and moved NW's to 62 %. Each courtyard slope was checked in the panoramas: NE at pano 1 40° and 98°; SE_e and SE_w at pano 1 98°/140° and pano 2 150°; SW at pano 2 235°; NW at pano 2 235° and 300°. They were also checked in the 2017 and 2022 photographs. There are **four** dormers, and only one is red:

| Id | Range | s (range frame) | Type | Size (front) | Before | Status |
|---|---|---|---|---|---|---|
| SEe_red | SE_e, about 5 m from the SE_w/SE_e bend | 3.3, front 0.3 m above the eaves line | gabled, red-painted front with an arched window | 2.1 m wide, cheeks 2.9 m, gable 1.1 m; window 1.3 × 1.3 m plus arch | none on SE_e | measured: pano 1 (98°, 140°), pano 2 (150°), 2017 and 2022 photographs |
| NE_vent | NE | 15.2, 3.0 m up the slope | small grey louvred vent, shed top | 0.8 × 0.8 m | red dormer at s 21.2 | measured, one camera (pano 1, two views) |
| SW_shed | SW | 17.6, 1.6 m up | grey shed dormer with a dark opening | 1.2 × 1.3 m | red dormer at s 17.8, same place | measured, one camera (pano 2), 2017 photograph (right) |
| NW_shed | NW, south of Kuretornet | 46.0, 3.0 m up | long low grey shed dormer | 2.4 × 0.75 m | red dormer at s 35.2 | measured, one camera (two views, s 42.6 and 46.7) |

SE_w has no dormer; pass 27's red one there goes.

**How they were measured.**
- Each dormer's foot was read in the panorama and the ray intersected with its range's courtyard roof plane (pass 127).
- The pitch was first corrected per view so that the front's eaves on the face plane reads z 17.01. The uncorrected rays put the feet 3–6 m too far up the slopes (the panos' elevations read high; pass 128 saw the same).
- The positions along the ranges (s) hardly depend on this correction. The distances up the slope ('up') do, and they are set by eye to where the photographs show them: SE_e's red front stands on the eaves line, the grey ones 1.6–3.0 m up.
- **Sizes** are scaled on nearby windows: SE_e's red front against the state-floor window beside it (pano 2 at 150°: 60 px against 40 px for a 1.2–1.5 m window; height 135 px against 84 px for 2.5 m). The grey ones are estimated.

**Checks** (`prepare_block129.py`, asserted):
- the four footprint corners of each dormer lie on its own visible slope piece (pass 127), 5 cm inside;
- no dormer comes within 1 m of a chimney (pass 128);
- the dormers are more than 5 m apart.

**Build** (`dormers129`).
- Each body is a closed prism (`solid129`, faces turned outward) that runs back until the roof plane meets its top. The material is the roof's grey metal.
- The red dormer has a red front plate (`K['FrameRed']`), pass 27's green window (`town_window`, arched) and two hood slabs over the gable.
- The grey ones have shed roofs at 15° (0.27) with a 6 cm slab and a dark opening (`SIGN`). NE's vent has three slats.

## 2. Doors at courtyard level

Read in pano 1 at 140° (SE_w square on), pano 1 at 98°, and pano 2 at 150° and 60°. The positions are taken as fractions of each front between the corners measured in the same view, then laid on pass 27's outline.

| Edge (pass 27 order) | Before | Now | Measured |
|---|---|---|---|
| NE, CI8–CI7 | pass 27's door at the middle (7.1 m from the north corner), dressed by portal D | no door; pass 127's 7-step door stays | pano 1 at 40°: windows of the lower row and a basement window there, no door |
| NE, CI7–CI6 | pass 27's door at the middle (20.3 m from the north corner) | portal D's arched door, 1.4 m wide, springing 1.9 m, arch 0.7 m, sill on the stair's landing (z 5.959) | see section 3 |
| SE_w, CI3–CI2 | pass 27's door at the middle (9.5 m from the bend) | two small arched doors, 0.95 m wide, springing 1.72 m, semicircular, at 2.32 m and 10.07 m from the bend | pano 1 at 140°: 12.2 % and 53 % of the front between the bend and the south corner, 0.94 m wide, crown 2.18 m. Pano 2 at 150° (grazing): 18.6 % and 62 % |
| SE_e, CI4–CI3 | none | a wide arched door, 1.5 m wide, springing 1.5 m, rise 0.5 m, 2.0 m from the bend | pano 1 at 140° (1.4–1.6 m from the bend, 2.0 m wide on the face plane) and pano 2 at 150° (2.2 m from the bend) |

**Not three on SE_w.** The brief and pass 127 counted three small arched doors on SE_w. Pano 1 at 140° sees all of SE_w square on, with **two** narrow arched doors. The third arched door of the 2014 views is the wide double-leaved one just east of the bend, on SE_e. It is built as SE_e's door above.

**Windows over doors.** The rule stays pass 127's `filt127`: no window within 1.2 m beside a door or within 1.6 m above its arch. Portal D's raised door counts as a door. With pass 27's two NE middle doors gone, the lower-row windows return on NE where the panorama shows them.

**SE_e's stair moved.** Pass 127 put SE_e's 9-step stair 2.5 m from the east corner. Both panoramas put its door near the middle of the front:
- pano 1 at 98°: 54 % from the east corner;
- pano 2 at 150°: 58 %.

The 2022 photograph agrees: the stair is well right of the east corner, with the red dormer further right again. The stair now stands on edge CI4–CI3 at u −3.645, 12.66 m from the east corner (59.6 %). That is the nearest place where the 2.0 m stair stays on one edge; CI4 sits in the middle of the straight front, so the stair cannot straddle it. The stair's shape is pass 127's.

## 3. Portal D on NE

**Verified.** Pano 1 at 40° (NE square on) shows the NE front with these features from the north corner: the 7-step door, a grey vent dormer above, then the aedicule portal with banded columns on a 3-step stair (Olsson's D, Drottningtrappan), and then the east corner.

| Reading | Pano 1, 40°/60y/92t | Pano 2, 60°/75y/95t | Used |
|---|---|---|---|
| North corner on the NE face plane | 0.53 | – | |
| Portal axis | 23.83 | 24.97 | |
| East corner | 29.81 | 31.19 | |
| Portal from the east corner | 5.98 | 6.22 | |
| Portal as a fraction of the front | 0.796 | – | |
| Placed | | | 6.9 m from the east corner, 25.46 m from the north corner (CI points) |

**Where it goes.** Pass 27's outline makes NE 32.4 m long. The panoramas see 29.3 m between the corner downpipes, so pass 27's north corner is about 2 m off (pass 128 found the same; it is not moved here). Measured from the east corner, which pano 2 sees from 9 m away, the portal is 6.0–6.2 m from it; as a fraction of the front, 25.8 m from pass 27's north corner. Pass 27's NE line has three collinear edges (CI8–CI7–CI6–CI5). The door is put on CI7–CI6 as near CI6 as the edge allows (u 5.17, door edge 0.25 m from the end), 6.9 m from the east corner. The portal's pedestals pass over CI6 onto the collinear edge beyond. The two-camera triangulation was unstable (the rays are nearly parallel) and is not used.

**Sizes.** Scaled 0.954 between the courtyard (z 5.47) and the eaves (17.01) on the front:
- total height 4.62 m from the courtyard;
- 3 steps, 0.49 m (risers 0.163 m);
- width 2.66 m;
- the door 1.49 m wide, its crown 2.61 m above the landing;
- the top is a segmental cap over an entablature.

**Portal D now** (`portal_d129`), on its landing:
- pedestals 0–0.35;
- banded Doric columns (pass 124's `column124` with band blocks every 0.36 m) at ±1.05 m to 2.95;
- an entablature 2.95–3.60 (2.66 m wide);
- a segmental cap 1.7 m wide to 4.13 (a triangle fan, `fan_prism124`).

Its stair is a `stairs127` stair: 3 risers of 0.163, treads 0.32, a 0.75 m landing for the pedestals, 3.0 m wide, iron handrails as on the other stairs. Pass 124's D (3.3 m wide, at courtyard level) is gone.

**Walk check.** A new route runs from the gate passage's courtyard end to the foot of D's stair and up onto the landing; see Verification.

## 4. Portal C on NW

**Measured.** Pano 2 at 300°/75y/108t, about 14 m from the front. Scaled 1.064 between the courtyard and the eaves on the front; the courtyard reads z 5.47 exactly.

| Part | Height above the courtyard (m) |
|---|---|
| Pedestal tops | 1.02 |
| Lower entablature | 3.44 (estimated from the arch) – 4.19 |
| Arch crown (intrados / extrados) | 3.22 / 3.47 |
| Relief panel | 4.30 – 5.71 |
| Upper capitals | 6.15 |
| Top of the cornice | **6.69 (z 12.16)** |

- **Width:** 4.95 m overall; the arch opening 2.6 m.
- **Form.** Both storeys are the full width, each with paired columns on each side. The upper storey's relief panel spans between the pairs, and the top is a **flat cornice**. There is no pediment.

**Against pass 124.** Pass 124's portal C had its lower entablature at +4.08, a narrower upper storey and a pediment to **+8.40 (z 13.87)**: 1.7 m **higher** than the panorama, not lower. The brief said "higher than pass 124's portal C"; the measurement says pass 124's was too high and too narrow above.

**Portal C now** (`portal_c129`):
- pedestals 0–1.02 under each pair;
- the lower pairs at u ±1.68 and ±2.18 (r 0.16) to 3.44;
- the entablature 3.44–4.19 (4.95 m wide);
- a base 4.19–4.30;
- the upper pairs (r 0.13) 4.30–6.15;
- the relief panel 2.86 m wide (a frame, the tablet and a raised field);
- the top entablature 6.15–6.69 with a flat cornice;
- jambs and an arch ring (`p18_arch`) on a 2.6 m opening springing at 1.95 m (crown 3.25 m).

**The opening.** The opening in the NW front (pass 124's `gate=(u, ZC, 2.8, 2.4, 1.4)`, crown 3.8 m) becomes 2.6 × 1.95 + 1.3 m (crown 3.25 m), inside the passage's own 3.0 m × 3.9 m section. The passage mesh itself is not changed. The gate walk check passes with the same numbers.

## 5. Camera 690 (the 2022 well photograph)

**Identification.** The photograph looks at the **east corner**: neither the north corner (pass 127) nor the south corner (pass 128).
- **Right front: SE_e.** It has the 9-step stair with the grey door, the small window over the door, the lamp left of it, the large lower window and the basement window right of it, and the red-fronted dormer above. That is the same arrangement as pano 1 at 98° and pano 2 at 150°.
- **Left front: NE.** It has portal D with its banded surround, the segmental cap and the steps. The lower-row and middle windows right of the portal match pano 1 at 40°.
- **The cap** at the upper left is the east tower's: it projects at x 397 against 440 in the 1500-px display.
- **The corner** between the fronts is hidden by the well.

**Resection.** Plan bearings of portal D, the well, SE_e's stair door (at its measured place) and the red dormer's front, with f 1925 px. That is a phone's 26 mm lens on the 1920 px short side; the focal length cannot be found from the bearings alone.
- **Result:** camera (−878.55, −309.10), true heading 81.5. Residuals: portal D −1.2°, the well −0.1°, the stair door 3.4°, the dormer −2.1°.
- **Pitch:** 12.4°, from the well's foot (9.1 m away at the 4.6 m base width).
- **Height:** ZC + 1.6.
- **Vertical field:** 67.24°.
- In the sandbox render (`cmp_well2022.jpg`), portal D, the cap, SE_e's stair and the red dormer fall within 10–30 px (of 667) of the photograph.

Camera 690 is re-created in `block129_cameras` under its old name `690_Block127_Cal_Well2022`. The export tail removes the old object first, so the transform is replaced.

**What the photograph shows that the model gets wrong** (not changed here unless stated):
- **NE is rusticated in 2022.** In 2014 (Street View) NE was smooth white. The 2022 photograph shows NE with the same painted rustication as NW and SW, including the band, so it was repainted after 2014. The model keeps the 2014 white (pass 127).
- Before this pass, portal D, SE_e's stair and the red dormer were all in the wrong places (fixed).
- **SE_e's stair** is a wide stair with flared sides and a stone side wall. The model's is 2.0 m wide and straight-sided.
- **The east tower's cap** is a tall lantern with an onion and a spire on the copper bell. Pass 27's is a dome with a small lantern.
- **The well house** looks taller and slimmer in the photograph than pass 124's. The vertical extents also do not fit this camera: the render's tops sit about 10 % of the frame lower than the photograph's, while the ground lines agree. A free fit of the camera with heights did not converge, so this is reported, not resolved.

## Measurement

| Source | Camera / reading | Used for |
|---|---|---|
| Street View 2014, pano 1 `zCIfieeXGQUNANmWu_Tg9A`, viewed only | pass 128's resection: (−885.06, −306.46), heading offset −1.34°, height ZC + 2.1. Views 40°/60y/92t, 98°/75y/105t, 140°/60y/98t. Screen 1400 × 806, the y value taken as the vertical field | NE (portal D, doors, vent dormer), SE_e (stair, red dormer, door), SE_w (doors) |
| Street View 2014, pano 2 `jOXzkLldNOjrveyz1T81wg`, viewed only | (−860.06, −308.67), heading offset −2.65°, height ZC + 1.9. Views 60°/75y/95t, 150°/75y/100t, 235°/75y/105t, 300°/75y/108t | portal D (from 9 m), SE_e, SW and NW dormers, portal C |
| Commons 2017 courtyard photograph (PD) | pass 127's camera (689) | red dormer on SE_e, SW shed dormer, the SE_e door by the bend; comparison |
| -wuppertaler 2022, `swe-kalmar-slott-006.jpg` (CC BY-SA 4.0) | re-resected (section 5) | identification, camera 690 |

**Reading error.**
- Positions along the fronts: ±0.5 m from the close views, ±1 m at grazing angles (SE_w in pano 2 differs by 6–9 % of the front from pano 1, which is used).
- Heights are scaled per front between the courtyard and the eaves: ±0.2 m.
- Dormers along the ranges: ±1 m (NW ±2 m). Up the slopes: estimated.
- Pass 27's outline is off by 1.5–2.5 m at the corners, so a position taken as a fraction of the front and one taken from a single corner can differ by up to 1 m. The notes say which was used.
- No pixel of the panoramas was used or saved. They were viewed in a browser tab and read on screen.

## The courtyard corners (not moved; noted for later)

Each reading is in the same view, on the model's face plane.
- **NE.** Pano 1 at 40° sees 29.3 m between the north and east corner downpipes; the model's face is 31.6 m. Pano 2 puts the east corner within 0.4 m of the model's, so the north corner is about 2 m off.
- **SE_e.** Pano 2 at 150° sees 21.9 m from the east corner to the bend (model 20.9); the bend lies about 1.0–1.3 m further west than pass 27's CI3. Pano 1 at 140° agrees within 0.3 m.
- **SE_w.** Pano 1 at 140° sees 16.5 m from the bend to the south corner (model 18.7); the south corner agrees within 0.1 m, so the bend is the vertex that is off (by 2 m along SE_w).
- **Kyrkportalen (portal F)** stands about 3–3.5 m from the south corner (pano 1 at 140°, pano 2 at 235°), not at the middle of CI2–CI1 (about 10 m), where pass 124 puts it. It is not moved here; the brief keeps F as is.

## Verification

- **Prepare.** `KALMAR_GEO=<pylib> python3 scripts/prepare_block129.py` prints `BLOCK129_PREPARE_OK`. It asserts:
  - each dormer's footprint on its own slope piece;
  - the dormers clear of the chimneys and of each other;
  - every door inside its edge;
  - each stair on its edge (portal D's on the straight NE line through CI6).
- **Sandbox** (prelude pass 128; `SCR/p129/build_block129_check.py`; logs `SCR/p129/log1.txt` and `log2.txt`). Both runs print `SANDBOX_DONE` without errors. Run 1 also rendered every view before the build (`before_*.png`). Run 2 moved the end of portal D's walk route onto the landing (run 1's route ended on the second step). The geometry is the same in both runs.
- **Change set.** `CHANGED129 ['SM_Castle124_Paving', 'SM_Castle124_Portals', 'SM_Kalmar_Slott']`. No other mesh in the scene changes.
- **Repeatability.** The build runs twice on the same scene: `REPEAT129 True`, and the second run changes nothing.
- **Polygons.** `SM_Kalmar_Slott` 311,152 (pass 128: 314,651); `SM_Castle124_Portals` 5,765; `SM_Castle124_Paving` 1,040. `drop_degenerate_faces129` removes 0 faces from each.
- **Export frame check** (pass 128's wrapper: the export tail's preparation, the exporter's frame test, a test FBX export of each mesh):
  - 0 invalid loops;
  - 3 of 3 exports succeeded;
  - fallback frames: `SM_Kalmar_Slott` 5,656 loops (pass 128: 5,664), Portals 0, Paving 16.
- **Walk checks** (pass 126's routes; ray casts every 0.2 m, obstruction rays at 0.45 and 1.4 m, a headroom ray of 2.0 m on the main route):

| Route | Samples | Missing | Largest step | Obstructions | Height |
|---|---|---|---|---|---|
| Courtyard → portal E → Kungstrappan → förstuga → Gyllene salen → 61a → Kungsmaket (low headroom 0) | 330 | 0 | 0.167 | 0 | 5.47–10.47 |
| Gate passage, portal B → portal C | 120 | 0 | 0.021 | 0 | 3.70–5.49 |
| Portal C → portal D's stair → its landing (new, run 2) | 124 | 0 | 0.163 | 0 | 5.47–5.96 |
| Portal C → E / F | 42 / 187 | 0 | 0.012 | 0 | 5.47–5.48 |

  The numbers for the pass 126 routes are the same as passes 127 and 128. Pass 126's old route to portal D at courtyard level is replaced by the new one.
- **Roof clearance.** All 54,748 vertices of Gyllene salen above z 15.5 (up to z 17.27) meet the castle roof above them. Kungstrappan, Kungsmaket and Förrum have none above z 15.5.
- **Comparisons** (`SCR/p129/sb1/`, before | after):
  - **`cmp_well2022.jpg`** (photograph | before | after). After: portal D at x 157 (photograph 150 of 667), the east tower's cap 197 (195), SE_e's stair 507 (≈520), the red dormer 597 (625).
  - **`cmp_courtyard2017.jpg`.** The red dormer on SE_e at the upper left and the SW shed dormer at the right are where the photograph has them. SE_w's door and SE_e's door by the bend are in place. Kyrkportalen still stands further from the corner than in the photograph (see above).
  - **`ba_p1ne.jpg`** (pano 1, 40°). The 7-step door, portal D and the east corner render at x 784 / 1120 / 1267 against 818 / 1097 / 1240 in the panorama. The vent dormer is at 854 (857).
  - **`ba_p2nw.jpg`** (pano 2, 300°). Portal C renders at x 777–952 with its top at row 416, against 732–885 and 432 in the panorama. The whole view sits about 45 px right; that is the camera and the outline.
  - **`ba_p2se.jpg`** (pano 2, 150°). Stair door 700 (730), red dormer 784 (840; the same distance from the bend as in the panorama), the SE_e door 903 (933), the SE_w doors 1008 / 1204 (1052 / 1197).
  - **`ba_p1sew.jpg`** (pano 1, 140°). The SE_e door 238 (258), SE_w's doors 375 / 605 (430 / 632; both 53–60 px from the bend as in the panorama), the south corner 854 (860).
  - **`ba_air.jpg`** and **`ba_top.jpg`**: the dormers from above.
  - The panorama views were compared on screen with the live panoramas; no panorama pixel is in these files.
- **Official build:** done by the lead on 2026-10-03; see "Official build". **Unreal:** pending.

## Limitations

- The dormers' distances up the slopes and the grey dormers' sizes are estimated. NE's, SW's and NW's dormers are each seen from one camera.
- Portal D stands 0.8 m nearer the north corner than its measured distance from the east corner, because the door must stay on one edge of pass 27's outline. Portals C and D are simplified: no relief, no scrollwork, no herms or masks, and the cap is plain.
- SE_e's stair keeps pass 127's straight 2.0 m form; the real one is wider and flared.
- NE's 2022 rustication is not modelled (the model follows the 2014 panoramas).
- Kyrkportalen (portal F) is about 6–7 m too far from the south corner (pass 124); not moved, as the brief asked.
- The 2022 camera fits in plan, but not in height; see section 5.
- Pass 27's courtyard corners are not moved (see above).

## Sources

| Source | Licence | Used for |
|---|---|---|
| Google Street View 2014, courtyard panoramas `zCIfieeXGQUNANmWu_Tg9A` and `jOXzkLldNOjrveyz1T81wg` | viewed only | dormers, doors, stairs, portals C and D |
| `castle27/kalmar-castle-internal-courtyard-2017-07-30.jpg` (Commons 2017) | PD | dormers, the SE_e door, comparison |
| `castle27/swe-kalmar-slott-006.jpg` (-wuppertaler 2022) | CC BY-SA 4.0 | camera 690, identification, comparison |
| Olsson, *Fornvännen* 1957 (as read by pass 124) | read only | portal names (D Drottningtrappan, banded columns) |
| Passes 27, 124, 126, 127, 128 (`source/castle27.json`, `block126.json`, `block127.json`, `block128.json`) | project | outline, roof planes, stairs, chimneys |

No new material is added. The dormers use pass 27's roof, red-frame, frame and dark materials, and the portals use pass 124's trim and tablet.

## Official build

The lead built pass 129 officially on 2026-10-03.
- **Geometry and export:** the geometry check passed on the second rebuild (True), the FBX audit passed (exit 0), and the two rebuilds gave identical meshes.
- **Prevhash:** only intended changes. Pass 128's `SM_Kalmar_Slott` and pass 126's `SM_Kalmar_Slott`, `SM_Castle124_Portals` and `SM_Castle124_Paving` are re-created here. The other entries are the known earlier corrections.
- **Dry renders:** 6 of 6, including the re-created camera 690.
