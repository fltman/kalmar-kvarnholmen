# Pass 126: Kalmar slott, the courtyard level, the west range's windows and Kungstrappan

Pass 126 does three things, in this order:

1. It lowers the courtyard to its real level, together with everything standing on it.
2. It makes the windows of the west range and Kungsmakstornet agree with the rooms of pass 125.
3. It builds Kungstrappan (Olsson's room 55), the entrance from the courtyard up to Gyllene salen.

| Mesh | Category | Status | What changed |
|---|---|---|---|
| `SM_Castle27_Ground` | Kalmar slott/Ground | re-created, `corrects_pass=27` | courtyard cobbles at z 5.47 (was 8.17) |
| `SM_Kalmar_Slott` | Kalmar slott/Castle | re-created, `corrects_pass=27,124` | courtyard fronts from the new level; courtyard first row = state-floor row; outer front 55–56 on new axes; portal E's door open |
| `SM_Kalmar_Slott_Towers` | Kalmar slott/Castle | re-created, `corrects_pass=27,124,125` | Kungsmakstornet's main window faces Kungsmaket's west niche; Kuretornet's courtyard arch follows the new ramp; pass 125's door cut re-applied |
| `SM_Castle124_Passage` | Kalmar slott/Castle | re-created, `corrects_pass=124` | ramp 9.1 % (was 22 %) |
| `SM_Castle124_Portals` | Kalmar slott/Castle | re-created, `corrects_pass=124` | C, D, E, F at the new level; E moved to the Kungstrappan door |
| `SM_Castle124_Well` | Kalmar slott/Castle | re-created, `corrects_pass=124` | at the new level |
| `SM_Castle124_Paving` | Kalmar slott/Ground | re-created, `corrects_pass=124` | courtyard slabs at the new level; the path to E follows E |
| `SM_Castle125_GyllenSalen` | Kalmar slott/Interiör | re-created, `corrects_pass=125` | outer niches at s 6.45 and 14.25; second courtyard niche; south-east door open |
| `SM_Castle126_Kungstrappan` | Kalmar slott/Interiör | new | entry hall, dog-leg stair, förstuga 55 |

No other mesh is touched: pass 27's walls, bridge, postejer, ravelin, islets, riprap and guns, pass 124's approach, bridge and trees, and pass 125's Kungsmaket and 61a are as before.

**Method.** `build_block126.py` reads `build_block124.py` and runs it again in a private namespace (`NS126`), with single string replacements that assert their original text occurs exactly once. Pass 124 itself re-runs pass 27's code in its own namespace (`NS124`), so pass 27's code is reached through pass 124 unchanged.
- **Left out:** pass 124's material loop, which would delete and re-create `M_Block124_*` and strip the pass 124 meshes this pass does not rebuild. The materials are mapped by name instead, as pass 124 did with pass 27. Also left out: the approach and trees section, the bridge section, and the walls exec. Pass 27's ground section runs in place of the walls exec.
- **Kept:** pass 124's re-creation of missing `M_Castle27_*` materials from Trim.
- **Gyllene salen:** run from `build_block125.py`'s frame and Gyllene sections in a second private namespace, with a modified copy of `block125.json`'s window lists and two replacements.
- **Every re-created mesh** gets `detail_pass=126`, `corrects_pass`, `reference_notes` and `drop_degenerate_faces126` (with the `_thin` test).
- **Pass 125's tower cut** (`cut_tower125`) is called again on the re-created towers.

**A fix to a shared name.** Pass 125 assigns `TS` and `TC` (its tower position) at module level. The town helpers read these as their stone and copper materials: `town_window` uses `TS` for its trim. Pass 27's tower windows therefore failed in the first sandbox run, because the finish looked up a material named −6.315. `build_block126.py` restores `TS = town_mats['Stone']` and `TC = 'M_Town_Copper'` when they are not strings. **The lead may want to look at this:** any later code that calls the town helpers after pass 125 meets the same trap.

## 1. The courtyard level

### Evidence

| # | Evidence | What it gives |
|---|---|---|
| a | kalmarslott.se (tillgänglighet): 7 steps from the courtyard to the entrance and shop, then 24 steps in three flights by Drottningtrappan to the state floor | 31 risers. At 0.155–0.170 m that is 4.8–5.3 m below the state floor (z 10.47), so the courtyard is at z 5.2–5.7 (6.5–7.0 m above the water). |
| b | Pass 125's state floor: outer main-floor sill measured at z 11.57 (Street View, resected within 0.5 m); the floor is 1.1 m below it | z 10.47. Kept: no source contradicts it. |
| c | The 1930s plate of Gyllene salen looking east (`dimu-021017089031.jpg`) | The courtyard windows sit at the same height as the outer ones (glass sill about 1.1–1.3 m above the floor, glass about 3.1 m high). So the courtyard's first row is the state-floor row: sill z ≈ 11.6, head ≈ 14.8. |
| d | The courtyard photographs (Commons 2017, `castle27/kalmar-castle-internal-courtyard-2017-07-30.jpg`; -wuppertaler 2022) | Two rows on the west and north fronts: tall windows above (aspect about 2.2–2.8), smaller ones below. The north front also has a row of small square windows. The heads of the tall row are about 2–2.5 m under the courtyard eaves: about 80 px under the eaves at about 39 px/m, scaled on a 1.2 m window width. In the 2022 photograph, the pale front has an outside stone stair of about 7 steps to its door, which matches the "7 steps to the entrance". |
| e | Pass 27's courtyard measurement (courtyard panorama, reported 13.5 m off, resected to 0.83° rms) | The courtyard eaves are 12.2 m above the courtyard floor. Pass 27 then *assumed* that the courtyard eaves equal the outer eaves (16.6 m above the foot) and so put the courtyard 4.5 m above the foot (z 8.17). |
| f | Pass 124's gate passage | With z 8.17, the passage from Västra förborgen (z 3.70) needs a 22 % ramp. The accessibility page mentions no steps there. |
| g | Kungstrappan and the förstuga (Olsson 1974, read by pass 125) | They lie between Kuretornet and the courtyard front, over the gate passage. At z 8.17 the passage vault (top about z 12.4) rises 1.9 m above the state floor, so the förstuga cannot exist. |

### Decision

**The courtyard is at 6.80 m above the water: z 5.47, lowered 2.70 m.** This value fits every item above:

- **(a)** 31 risers of 0.161 m, an ordinary riser.
- **(c, d)** The state-floor row at z 11.57–14.77 is the courtyard's first row. With pass 27's own measured 12.2 m (e), the courtyard eaves stand at z 17.67, 2.9 m above the window heads. The photographs give about 2–2.5 m. So pass 27's courtyard measurement was right; only its assumption that the two eaves are equal was wrong.
- **(f)** The passage rises 1.80 m over 19.7 m. Level for 1.2 m at each end, the ramp is **9.1 %**.
- **(g)** The vault's top at the courtyard end is at z 9.68, 0.49 m under the förstuga's floor slab (z 10.17–10.47).

The photographs alone give z 3–5.5, depending on which window height and ground line one reads (the camera positions are not known). That range includes 5.47 but does not narrow it. A lower value, about z 4.5, would need 0.19 m risers.

### What moved

| Part | Before | After |
|---|---|---|
| Courtyard cobbles (pass 27, `SM_Castle27_Ground`) | z 8.17 | z 5.47 |
| Courtyard fronts (pass 27/124, `SM_Kalmar_Slott`) | from z 8.17 to the eaves | from z 5.47 to the eaves (the walls reach 2.7 m further down) |
| Courtyard first row | sill ZC+5.6 = 13.77, 1.2 × 2.4 m | sill z 11.57, 1.2 × 3.2 m (the outer main row's level and height) |
| Courtyard ground row and doors | ZC+1.35, doors at ZC | same offsets from the new ZC |
| Portals C, D, E, F; well house; courtyard slabs (pass 124) | at z 8.17 | at z 5.47 |
| Gate passage (pass 124) | 3.70 → 8.18, ramp 22 % | 3.70 → 5.48, ramp 9.1 % |
| Kuretornet's courtyard-side arch (pass 124) | sill zf(t) at the old ramp | at the new ramp |
| Portal B sill | z 3.70 | unchanged |
| Portal C sill | z 8.18 | z 5.48 |
| State floor (pass 125) | z 10.47 | unchanged |

## 2. Windows

| Window | Before | After | Source |
|---|---|---|---|
| Outer main row, front 55–56 (Kungsmakstornet to Kuretornet) | s 3.62, 8.02, 12.42 (pass 27's even 4.4 m rule) | **s 6.45 and 14.25**, also for the low and top rows above and below | Zettervall's west elevation (1883), scaled on the front between the tower and Kuretornet: s 6.4 and 14.5. The 2009 panorama of Gyllene salen (pass 125): s 6.5 and 14.0. The interior now has a niche at each. |
| Pass 27's third window (s 3.62, in the wall between Gyllene salen and 61a) | present | gone | Zettervall shows none there |
| Gyllene salen, outer niches | s 8.02 and 12.42 | s 6.45 and 14.25, near the corners. The fireplace stays midway (s 10.35). | as above |
| Courtyard row | sill z 13.77 (2.2 m above pass 125's niche glass) | sill z 11.57, aligned with the outer row and with Gyllene salen's niche glazing | 1930s plate |
| Gyllene salen, courtyard niches | one, s 15.36 | **two**, s 10.4 and 15.36 | 1930s plate: two niches with a wide pier and a blind arch between them. The north niche is at about 45 % of the wall, read on the coffer grid. |
| Kungsmakstornet main window (z 11.27–13.67) | pointed from the castle's centroid, 54° from Kungsmaket's west niche | faces Kungsmaket's west niche (+c), 1.4 m wide like the niche's leaded window | Zettervall shows the tower's main window centred on its west face. The other tower windows keep pass 27's directions. |

**Unresolved: Gyllene salen's north courtyard niche.** OpenStreetMap's courtyard outline turns its north-west corner at s 13.3, so only s 13.3–17.0 of the hall's courtyard wall faces the courtyard. Pass 27's outline, which this pass keeps, comes from OpenStreetMap. The 2021 aerial agrees roughly with it.

The 1930s plate and Olsson's plan (corner about 7 m further north, at the hall's north wall) disagree with it. Following the photograph, as the brief asks, the interior has the second niche at s 10.4. Its pane (opaque, as all pass 125 panes) stands against the north range's hollow shell, and the exterior shows no window there.

The 2017 courtyard photograph, read with pass 124's eye-placed camera with its heading corrected on the two courtyard corners, shows the upper row of the west front at about s 34.9, 29.4, (one hidden by the well) and 18.0. It shows blank wall from there to the corner. This also points to only one window on the courtyard in Gyllene salen's stretch.

Resolving this needs a measured plan, or a courtyard view with a known camera position.

## 3. Kungstrappan and the förstuga (55)

**Where.** Olsson (1974, read by pass 125) puts 55 Kungstrappan between Kuretornet and the courtyard front.
- In the model that is a strip 3.6–5.1 m wide between Kuretornet's courtyard skin and the courtyard front W1–N, from the gate passage (s 18.9–22.5) to the courtyard corner W1 (s 36.8).
- Pass 27 has a door at the middle of the front piece W1–V (s 29.0, c −15.7), and the brief and pass 125 call this portal E.
- **Pass 124 had dressed a different door** as E: the one at the middle of CI0–W1 (s 46.3, south of Kuretornet). Pass 124's notes say E's position is pass 27's door, "not measured".
- This pass moves E's dressing (pilasters, entablature, pediment) to the s 29 door. The door at s 46.3 is a plain pass 27 door again.

The stair is built in a frame along the courtyard front: *a* from W1 towards N, *b* inwards. Portal E's door is at a 7.82.

| Part | Where (a, b) | Level |
|---|---|---|
| Portal E's door, opened (pass 27's arch and jambs without the leaf, a stone threshold) | a 7.12–8.52 | z 5.47 |
| Entry hall, stone flags | a 6.59–9.22, full width | z 5.48 |
| Flight 1, 15 risers × 0.167 m, treads 0.30 m, 1.70 m wide | a 6.59 → 2.39, courtyard side (b 0–1.70) | 5.47 → 7.97 |
| Half landing | a 0.40–2.39, b 0–3.55 (beyond Kuretornet's corner) | z 7.97 |
| Flight 2, 15 risers × 0.167 m, 1.72 m wide | a 2.39 → 6.59, along Kuretornet (b 1.90 to its skin) | 7.97 → 10.47 |
| Spine wall between the flights, to the ceiling; oak handrails on both faces | b 1.70–1.90 | |
| Förstuga 55, stone flags on a 0.3 m slab, over the entry hall and the gate passage | a 6.59 → Gyllene salen's south wall | z 10.47 |
| Parapet with an oak cap over flight 1's well | a 6.47–6.59 | 1.0 m |
| Ceiling, plastered | over the whole strip | z 15.20 |
| End wall, side wall beyond Kuretornet's corner, wall under the förstuga beyond the entry hall, wall closing the hollow range north of Kuretornet's corner | | |
| Gyllene salen's south-east door (c −13.3), opened: a hole and threshold in pass 125's south wall, the leaf removed, a plain stone surround on the förstuga side; pass 125's pedimented surround stays in the hall | | |

**Stair form and what is estimated.** A dog-leg of two straight flights with a half landing fits the strip. The sources give the stair's position, not its form: Olsson's plan was read, not measured, by pass 125, and Scholander's 1851 drawing of the entrance from Kungstrappan (DigitaltMuseum 021017083367) was not fetched. Also estimated: the risers (30 × 0.167 m), the treads, the widths, the förstuga's ceiling height, and the finishes (plaster, limestone flags).

**The gate passage's vault.** It no longer intrudes. At the courtyard end its top is at z 9.68, under the förstuga's slab (z 10.17). The passage is otherwise pass 124's.

## Measurement

There were no new Street View views for this pass, and no camera was resected. The values come from text (step counts), from pass 27's and pass 125's measured levels, and from proportions read on drawings and photographs:

| Value | Source | Status |
|---|---|---|
| 31 steps from the courtyard to the state floor | kalmarslott.se, tillgänglighet (via `castle-sources/SOURCES.md`) | text |
| State floor z 10.47; outer main sill z 11.57, 3.2 m high | pass 125, pass 27 (resected within 0.5 m) | measured by earlier passes |
| Courtyard eaves 12.2 m above the courtyard | pass 27 (resected, 0.83° rms) | measured by pass 27 |
| Window heads about 2–2.5 m under the courtyard eaves | 2017 photograph, scaled on a 1.2 m window width | read on the photograph, ±0.5 m |
| Outer windows s 6.4 and 14.5 | Zettervall 1883, scaled on the front s 0–18 (155 px) | read on the drawing, ±0.5 m |
| Courtyard niche s 10.4 | 1930s plate, read on the coffer grid | estimated, ±1 m |
| Upper-row positions on the west courtyard front (s 34.9, 29.4, 18.0) | 2017 photograph with pass 124's camera, heading corrected by +5.2° on corners W1 and N (W1 at x 337 vs 352 seen, N at 889 vs 880) | estimated, ±2 m |

## Verification

- **Prepare.** `python3 scripts/prepare_block126.py` prints `BLOCK126_PREPARE_OK`. It asserts:
  - the riser of the 31 steps is 0.155–0.170 m (it is 0.161);
  - the courtyard eaves differ from the outer eaves by more than 2 m;
  - the stair's riser is 0.15–0.19 m (it is 0.167);
  - flight 2 is at least 1.5 m wide (it is 1.72);
  - the half landing is at least 1.6 m long (it is 1.99);
  - the passage vault's top (z 9.68) is under the förstuga's slab (z 10.17).
- **Sandbox runs** (prelude pass 125; `SCR/p126/build_block126_check.py`, logs `SCR/p126/log1.txt`–`log4.txt`):
  - Run 1 stopped at pass 125's `TS` trap (see Method).
  - Run 2 stopped at a camera name typo.
  - Runs 3 and 4 print `SANDBOX_DONE` without errors.
  - Every replacement asserted its original text once.
- **Repeatability.** The build runs twice on the same scene and compares vertex and face hashes: `REPEAT126 True` for all 9 meshes. On the second run, pass 125's cut is applied again to the freshly re-created towers (4 faces each time).
- **`drop_degenerate_faces126`** (with `_thin`) runs on all 9 meshes. It removed 2 faces from the ground and 2 from the towers (pass 27's own slivers) and 65 from Gyllene salen (the same bevel slivers as in pass 125). It removed none from the other meshes.
- **Export frame check** (the pass 123–125 wrapper's method: the export tail's preparation, then the exporter's frame test and a test FBX export on every mesh): 0 invalid loops, and 9 of 9 exports succeeded. The fallback frame covers 4 loops in the ground, 4,953 in the castle, 211 in the towers, 21 in the paving, 349 in Gyllene salen and none in Kungstrappan.
- **Walk checks** (ray casts every 0.2 m; obstruction rays at 0.45 m and 1.4 m; headroom ray 2.0 m):

| Route | Samples | Missing | Largest step | Obstructions | Low headroom | Height |
|---|---|---|---|---|---|---|
| Courtyard → portal E → entry hall → flight 1 → landing → flight 2 → förstuga → Gyllene salen's south-east door → Gyllene salen → 61a → passage → Kungsmaket's west niche | 330 | 0 | 0.167 (one riser) | 0 | 0 | 5.47–10.47 |
| Gate passage, portal B → portal C | 120 | 0 | 0.021 | 0 | – | 3.70–5.49 |
| Portal C → D, → E, → F along the slab paths | 35 / 42 / 187 | 0 | 0.012 | 0 | – | 5.47–5.48 |

  No hit on the stair route had a face normal more than 45° from up.
- **Comparisons** (`SCR/p126/sb4/`):
  - **`cmp_courtyard2017.jpg`.** The photograph has level verticals with its horizon low in the frame, so the render is level with a 102° field and the upper part is compared. The camera is placed by eye, 9.5 m from the well.
    - The camera is not matched well: the render looks more to the south, and shows Kuretornet's bell roof where the photograph shows Kungsmakstornet's cap. Treat this comparison as a check of arrangement, not of pixels.
    - The well, the low row and the doors now stand on the same floor, with the state-floor row about one window height above the ground row, as in the photograph.
    - The model's courtyard eaves are still pass 27's z 20.27, so the fronts show about 5.5 m of wall above the window heads, where the photograph shows about 2–2.5 m (see What remains).
  - **`cmp_west_front.jpg`.**
    - Two main windows on the stretch between Kungsmakstornet and Kuretornet, near the hall's corners, as in Zettervall.
    - The low and top rows are on the same axes.
    - The tower window faces west.
  - **`cmp_gyllene_east.jpg`.** Two courtyard niches with a pier between them, as in the 1930s plate. The south-east door is now open.
  - **`cmp_gyllene_west.jpg`.** The two outer niches stand near the corners with the fireplace midway, as in the 2009 panorama. Pass 125's render had them 4.4 m apart.
  - **`sheet_stair.jpg`.** Portal E from the courtyard, the entry hall and flight 1, the half landing and flight 2, and the förstuga towards Gyllene salen's door.
- **Pending.** The official build and the Unreal checks are pending; the lead fills in the build results.

## What remains

- **The courtyard eaves.** Pass 27 builds one eaves level (z 20.27) all round. The evidence above puts the courtyard eaves at about z 17.7, so the roofs' courtyard slopes should start about 2.6 m lower, giving asymmetric roofs. Changing pass 27's roof envelope, dormers and seams was beyond this pass.
- **Gyllene salen's north courtyard niche** (s 10.4) has no window outside, because the OpenStreetMap courtyard corner (s 13.3) and the 1930s plate disagree (see above).
- **The pass 27 door at s 46.3** is plain. It may be portal G or another door; it was not checked.
- **Kungstrappan's form** is an interpretation (see above). Scholander's 1851 drawing of the entrance from Kungstrappan and Olsson's *Ritningar* plates would settle it.
- **The courtyard first row** now has the state-floor windows on all fronts (pass 27's 3.8 m spacing). Their positions are pass 27's rule, not measured, except where the photographs were read above.
- **Not changed:** the ground row's height on the courtyard fronts (ZC+1.35, 2.0 m), the entresol row of the north front, and the outside stairs to the north range's entrance (the 7 steps).
- **Collision.** No collision test in Unreal; the walk checks are Blender ray casts only.
- **Views that would help:**
  - the west courtyard front square on from the courtyard, at about local (−873, −305), heading 300, pitch 15, to place its windows and Kungstrappan's door;
  - the north-west courtyard corner, to see whether a second window of Gyllene salen faces the courtyard.

## Sources

| Source | Licence | Used for |
|---|---|---|
| Kalmar slott, accessibility page (kalmarslott.se/infor-besoket/tillganglighet/, via SOURCES.md) | – | the step counts |
| Pass 27 (`source/castle27.json`, its notes), pass 124, pass 125 (`source/block125.json`) | project | levels, outlines, the frame, the rooms |
| Helgo Zettervall, west elevation, 4 September 1883 (`castle27/plan-for-the-reconstruction-1883-09-04.jpg`) | public domain | the outer window axes, the tower window |
| `castle27/kalmar-castle-internal-courtyard-2017-07-30.jpg` | PD | courtyard rows, the eaves gap, comparison |
| `castle27/swe-kalmar-slott-006.jpg` (-wuppertaler 2022) | CC BY-SA 4.0 | the outside stair of 7 steps, window rows |
| `castle27/schloss-kalmar-senkrecht-luftaufnahme-2021-.jpg` (HaSe 2021) | as in castle27/sources.json | the courtyard corner's position |
| `dimu-021017089031.jpg` (Olsson plate, 1930s) | Public Domain Mark | Gyllene salen's two courtyard windows and their height |
| `commons-kalmar-slott.gyllene-salen.jpg` (Baboş 2009) | CC BY 3.0 | the outer niches near the corners |
| Olsson, *Fornvännen* 1974, fig. 1 (as read by pass 125) | in copyright, read only | Kungstrappan's and the förstuga's position |

Google imagery was not used. No pixel of any photograph or drawing is used as a texture. The new materials (`M_Block126_Plaster`, `_Flag`, `_Step`, `_Oak`) are flat tints on the town textures; the re-created meshes keep their pass 27, 124 and 125 materials.

## Official build

The lead's build of pass 126 passed the Blender geometry checks and the FBX export, and two rebuilds gave identical meshes. Prevhash reports the intended changes only:
- pass 124's SM_Kalmar_Slott, SM_Kalmar_Slott_Towers, Passage, Portals, Well and Paving;
- pass 125's SM_Castle125_GyllenSalen and SM_Kalmar_Slott_Towers;
- the earlier intended corrections.

Pass 27's SM_Castle27_Ground is outside prevhash's range. The Unreal import and its checks are deferred.
