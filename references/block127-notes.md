# Pass 127: Kalmar slott, the courtyard fronts and the roofs

Pass 127 corrects the castle's courtyard side. Pass 27 used one eaves level (z 20.27) all round, so the courtyard fronts rose about 3 m too high and the roofs had no visible courtyard slope. The pass does five things:

1. It lowers the courtyard eaves to z 17.01, measured on Carl Möller's sections of 1882.
2. It rebuilds all the range roofs as one asymmetric surface. The outer eaves and outer planes stay; the ridges come down and move outwards.
3. It puts pass 27's dormers on the new slopes and makes the courtyard chimneys tall.
4. It adds the missing courtyard window rows.
5. It gives the NW and SW ranges their painted rustication and lime-washes all the courtyard fronts. The agent first built it on the north range; the lead moved it after checking Street View, and the window rows were then measured again on the 2014 panoramas (see "Lead's correction" and section 4).

| Mesh | Category | Status | What changed |
|---|---|---|---|
| `SM_Kalmar_Slott` | Kalmar slott/Castle | re-created, `detail_pass=127`, `corrects_pass=27,124,126` | roofs, chimneys, dormers, chapel turret height source, courtyard fronts (height, cornice, rows, colour, rustication) |

No other mesh is touched. Pass 27's ground, walls, towers, bridge and the rest, pass 124's passage, portals, well and paving, pass 125's rooms and pass 126's Kungstrappan are as before. The well and the portals stand in front of the re-created fronts as before.

**Method.** `build_block127.py` takes the composition that `build_block126.py` makes of `build_block124.py`: the slice from `def rep126` to `NS126=dict(globals())` is run in a private namespace. That gives pass 124's code with pass 126's edits, and through it pass 27's code. The pass then makes its own single replacements, each asserted to occur exactly once:
- Only the castle section runs. Pass 27's ground, the towers and everything after the castle (passage, portals, well, paving) are not run again, so those meshes keep their pass 126 versions.
- `b124_mark` marks the re-created mesh as pass 127's. `drop_degenerate_faces127` with the `_thin` test runs on it.
- In pass 27's castle section:
  - the per-range roof prisms and their seams give way to `roof127`;
  - the chimney block gives way to `chimneys127`, and the dormer loop to `dormers127`;
  - the chapel turret takes its position and height from `source/block127.json`;
  - the courtyard walls end at z 17.01, the courtyard cornice moves under the overhang, and the courtyard materials change.
- In pass 124's `court_front124`, the rows come from `rows127`, the walls end at the new eaves, and windows that meet a door are left out. The NW and SW ranges get `dress127` (`RUST127`), including the west range's merged front W1–N with portals C and E.

`TS` and `TC` are restored before any town helper runs (pass 125's trap, as in pass 126).

The roof geometry is computed in `scripts/prepare_block127.py` with Shapely and written to `source/block127.json`. The build only lifts the plan polygons onto their planes.

## 1. The courtyard eaves

### Möller 1882: the measured value

**Source.** Riksarkivet PK006-00041, "Calmar slott. Profiler", "Uppmätt och ritadt af Carl Möller, Calmar Jan. 1882" (public domain). The scan is 7856 × 11828 px.
- **Scale.** 90 fot = 1549 px on the scale bar, 17.21 px per fot. With 1 fot = 0.2969 m, that is **57.97 px/m**.
- **Method.** Each section was read on full-resolution crops with a pixel grid. The rows read are the state floor (the floor line under the hall, Möller's red line), the wall tops on both sides, the ridge and the ground. The columns read are the outer face, the courtyard face and the ridge.
- **Which side is the courtyard.** The courtyard side is labelled "Gård", the outer side "Jordlinie".

| Section | Courtyard eaves above floor | Outer eaves above floor | Ridge above floor | Floor above courtyard ground | Courtyard eaves above ground | Depth | Ridge from outer face |
|---|---|---|---|---|---|---|---|
| Gyllene salen (59) | 6.38 | 10.06 | 14.97 | 5.55 | 11.94 | 16.8 m | 0.38 |
| Förbrända salen (76) | 6.54 | 10.25 | 14.89 | 5.64 | 12.18 | 15.5 m | 0.36 |
| Unionssalen (87) | 6.53 | 10.09 | 14.99 | 6.08 | 12.61 | 14.4 m | 0.38 |
| Rutsalen (63) | 6.61 | 6.16 (low) | 15.18 | 5.66 | 12.27 | 20.4 m | 0.58 |
| Kyrkan (86) | 6.62 | 9.75 | 14.09 | 5.57 | 12.20 | 10.5 m | 0.41 |
| **Mean** | **6.54** | **10.04** (without Rutsalen) | **15.0** (the four halls) | 5.70 | 12.24 | | |

**Reading error.** The rows are read to about ±5 px, which is ±0.1 m. The sections are drawn, not photographed, and Möller's floors may differ by a few decimetres between the ranges.

**Decision: courtyard eaves at z 17.01.** That is the state floor (z 10.47, pass 125) plus 6.54 m.

**Check on the outer side.** The same sections put the outer eaves at z 10.47 + 10.04 = 20.51. Pass 27 measured z 20.27 from outside with resected Street View cameras. They agree within 0.24 m, which confirms both the scale bar reading and the floor as the reference.

**Möller predates Zettervall.** Möller surveyed before Zettervall's restoration of 1885–91. The outer eaves have not moved since, so the walls probably have not either; Zettervall's work was mainly the tower caps and gables. Rutsalen's low outer eaves (6.16) are kept out of the outer mean.

### What the other evidence says

| # | Evidence | Courtyard eaves | Status |
|---|---|---|---|
| a | Möller 1882, relative to the state floor (above) | z 16.85–17.09, mean **17.01** | measured on a survey drawing |
| b | Möller 1882, relative to the courtyard ground, with pass 126's courtyard (z 5.47) | z 17.2–18.1, mean 17.71 | measured; depends on pass 126's courtyard level |
| c | Pass 27's courtyard panorama (12.2 m above the courtyard floor) with z 5.47 | z 17.67 | measured by pass 27 (resected 13.5 m, 0.83° rms) |
| d | 2017 photograph, right front (SW, see section 4), scaled on the state-floor window (3.2 m = 185 px) | about 1.0 m over the window heads: z 15.8 | read on the photograph, ±0.7 m |
| e | 2017 photograph, middle front (SE_w), at 50–60 px/m | 1.8–2.2 m over the window heads: z 16.6–17.0 | read on the photograph, ±0.7 m |
| f | 2017 photograph, camera height 1.6 m at the horizon (row 1115, from the standing people) | 10.9–11.4 m above the courtyard: z 16.4–16.9 | estimated |
| g | 2022 photograph, the door at the outside stair (2.2 m door = 195 px) | at least 10.8 m above the courtyard (the upward tilt is not corrected): z ≥ 16.3 | estimated |
| h | Gyllene salen (pass 125): ceiling plane z 16.67, walls to z 17.27, 1.3–1.6 m inside the courtyard face | the courtyard roof must clear z 17.27 there | geometric |

**Where the evidence disagrees.**
- (a) and (b) differ by 0.7 m. The reason is pass 126's floor-to-courtyard height of 5.00 m, against Möller's 5.55–6.08 (mean 5.70). Relative to the rooms, which are fixed by pass 125's measured sill, (a) is the right reference.
- The photographs (d–g) all put the eaves at or below (a). The expected z 17.7 is (b)/(c).
- (h) does not conflict with z 17.01. The roof rises inwards, so over Gyllene salen's courtyard wall it stands at z 18.1–18.3. The sandbox confirms that every vertex of the hall lies under the roof.

**Also read on the Gyllene section.**
- **State-floor window.** The courtyard window has its sill 1.09 m above the floor (z 11.56, the same as pass 126's 11.57) and its head 3.76 m above it (z 14.23). Pass 126 uses 14.77.
- **Lower window.** The courtyard window below it runs z 7.5–9.4.
- **Hall height.** Möller draws the hall 5.4 m high to the plafond. Pass 125 uses 6.2.

None of these is changed here; see What remains.

## 2. The roofs

### Rule

For each range, the build keeps pass 27's outer plane: the outer eaves at z 20.27 on the range's outer line, with pass 27's pitch `rise/half`. On top of that:
- **Ridges.** The ridge comes down to Möller's 15.0 m above the floor, z 25.47. Pass 27's z 26.27 came from its rule `rise=min(0.93·half, 6)`. The south-west range keeps pass 27's z 24.80, which pass 27 measured from outside (Möller's Kyrkan: 24.56).
- **Ridge position.** The ridge lies where the outer plane reaches that height. That puts it at 0.43 of the depth from the outer face (Möller: 0.36–0.41), and at the middle for the south-west range.
- **Courtyard slope.** It runs from the courtyard eaves line at z 17.01 up to the ridge.
- **Courtyard eaves line.** It is not the range rectangle's inner edge. It is a least-squares line through that range's courtyard vertices (pass 27's outline), moved to the wall face (0.355 m into the courtyard) of the vertex that stands furthest out.
  - So no courtyard wall rises through the roof.
  - Where a wall stands further back, a filler closes the wall top up to 3 cm under the roof surface (up to 0.42 m high, at the corners).
  - Pass 27's outline deviates from its range rectangles by up to 2.9 m (the south-east range's courtyard front runs 8° off its axis). Pass 27's roofs therefore overhung some courtyard walls by over 3 m. The fitted line removes that.

| Range | Depth | Courtyard pitch before (= outer) | Courtyard pitch now | Outer pitch | Ridge before | Ridge now | Ridge from outer face |
|---|---|---|---|---|---|---|---|
| NW (west, Gyllene salen) | 18.0 | 33.7° | 39.7° (Möller Gyllene 39.5°) | 33.7° | 26.27 | 25.47 | 0.43 |
| NE (north) | 21.7 | 28.9° | 33.8° | 28.9° | 26.27 | 25.47 | 0.43 |
| SE_w | 14.8 | 39.0° | 45.6° | 39.0° | 26.27 | 25.47 | 0.43 |
| SE_e | 18.4 | 33.1° | 44.7° | 33.1° | 26.27 | 25.47 | 0.43 |
| SW (chapel) | 9.7 | 42.9° | 56.4° (Möller Kyrkan about 50°) | 42.9° | 24.80 | 24.80 | 0.50 |

### Construction (`prepare_block127.py`)

- **Slopes.** Each range has two slope pieces. Each is a plan polygon and a plane z = Ax + By + C:
  - the courtyard piece is bounded by the eaves line minus the 0.4 m overhang, the ridge (where it is the lower plane), and the range's ends;
  - the outer piece is bounded by the ridge, the outer line plus 0.4 m (pass 27's overhang), and the ends.
  
  The courtyard pieces are clipped to the outer outline plus 0.45 m. Before this, the north range's courtyard slope ran out past the west range's outer front beside Kungsmakstornet. All pieces are clipped so that they overhang the courtyard walls' faces by 0.4 m and no more.
- **Envelope.** Each piece keeps only the part where it is the highest of all the pieces that cover the point: the exact upper envelope, by half-plane differences. Valleys and hips are then shared edges of two pieces. The SE_w/SE_e overlap of pass 27 (±6 m) is kept.
- **Towers.** Each piece is cut where it enters a round tower: 0.15 m inside the tower wall below the wall top, and inside the copper bell above it. The bell is pass 27's profile, read from `TOWER_SPEC` in `build_castle27.py`, and solved per direction for the height of that piece's plane. Pass 27's roofs ran on through the towers and out through the bells.
- **Kuretornet.** Pieces are cut 0.15 m inside its fitted rectangle.
- **Checks** (asserted):
  - the overlap between pieces is 0.00002 m²;
  - the gap between the pieces plus the tower cuts and the plan area is 0.0 m²;
  - 3015 m² of roof is visible, and 479 m² lies inside the towers and Kuretornet.
- **Edges.**
  - 36 shared edges, of which 7 are ridges.
  - 23 eaves segments, each with a fascia and an eaves rod.
  - 331 edges at the towers.
  - 14 steps: places where one piece stands over its neighbour, closed by vertical faces in the outer render colour. Ten are under 0.3 m (at courtyard corners where two eaves lines meet). The large ones are gable ends of pass 27's rectangles:
    - SE_e over SE_w at the bend of the south-east range, 10.0 m long, up to 3.1 m high;
    - NE over SE_e by the east tower, 5.5 m, up to 3.3 m;
    - NW over NE and NW over SW by the north and west towers, 0.8–2.7 m.
  - No free gable edges remain.
- **Seams.** 681 standing seams, every 0.62 m down each piece's slope, clipped to the piece.

### Build (`roof127`)

- **Faces.** Each piece is triangulated (`tessellate_polygon`) on its plane, with a 0.12 m underside in the dark material.
- **Edges.** Fascias and eaves rods on the eaves, ridge rods on the shared ridge edges, and seams on the surface.
- **Closures.** Vertical faces close the steps, and fillers close the courtyard wall tops.
- **Courtyard cornice.** Pass 27's dentil-less cornice now sits at z 16.06 (eaves −0.95), under the overhang. At eaves −0.2 it would have stood out through the overhang.

## 3. Dormers, chimneys, turret

- **Dormers.** Pass 27's four courtyard dormers (red-painted fronts, `roof_dormer`) now stand on the fitted eaves line at z 17.01, with each courtyard slope's pitch.
  - The west range's dormer moves from 35 % to 62 % along the range. At 35 % it stood 5 m from the north courtyard corner and was buried in the north range's slope (seen in sandbox run 2).
  - The prepare script checks nine points of each dormer's footprint on its own slope.
- **Chimneys.** All are in salmon render with stone caps, standing on the joined roof, with their tops 1.6 m over their range's ridge (pass 27).
  - Six stand 2 m up the courtyard slopes, where the photographs show tall chimneys near the courtyard eaves: SW 40 % and 58 % (the second 1.3 × 0.9 m; placed from the 2017 photograph before the lead's identification, which puts those two chimneys on SE_w, see What remains), NW 50 % (2022 photograph), NE 26 % and 80 %, SE_w 45 %.
  - Pass 27 had these at mid − 1.3 to 2.2 m, with tops at ridge + 1.6.
  - The four outer-side chimneys keep pass 27's positions.
  - The positions along the ranges are approximate.
- **Chapel turret.** It stays on the south-west ridge, which did not move (z 24.80).

## 4. Courtyard fronts

- **Height.** The fronts end at z 17.01 (were 20.27), and the cornice sits under the overhang.
- **Which front is which.** The lead settled this on the 2014 Street View panoramas: NW and SW are rusticated, NE is smooth white, SE_w and SE_e are plain cream lime. The first version of this pass had read the 2017 photograph as looking at the north corner; with that identification its rows and rustication went on the wrong ranges. Re-read with the lead's identification, the 2017 photograph looks south from near the north corner:
  - the middle front is SE_w;
  - the far-left part beyond the jog is SE_e (the SE_w/SE_e bend, CI3);
  - the right front is SW, with Kyrkportalen (portal F) by the corner;
  - the cap is the south tower's.
  
  The 2022 photograph looks at the north corner: NW on the left (rusticated, with Kuretornet's cap above), NE on the right (white, with the 7-step stair).
- **Rows.** Measured on the panoramas (Measurement below). Every row keeps pass 27/126's 3.8 m spacing, centred on each front piece, so all rows stay on pass 126's axes. Pass 126's state-floor row (sill z 11.57, 1.2 × 3.2 m) is shared and kept on every front; where the panoramas disagree, it is flagged below, not moved.

| Front | Rows before (pass 126) | Rows now | Measured (panoramas 2014) |
|---|---|---|---|
| NW (rusticated) | state; ground ZC+1.35 (6.82–8.82) | state; small row sill 8.6, 1.05 × 1.2 m (head 9.8) | west part: rows 12.0–14.4 and 8.6–9.8, arched cellar windows and doors at the ground. The centre (Kungstrappan, Kuretornet behind) is irregular: windows at 15.0–16.4, 13.3–15.1, 12.2–14.7, 10.7–12.3, 10.3–11.2, 9.4–10.8 and 6.5–7.8. North part: 12.2–14.7 and 7.9–10.0. The relief portal with the arcade (portal C) reaches about z 12.2 |
| SW (rusticated) | state; ground 6.82–8.82 | state; middle row sill 9.9, 0.9 × 1.2 m; lower row sill 6.77, 0.9 × 1.26 m | upper 12.26–15.43 (1.08 × 3.17); middle 9.91–11.10 (0.9 × 1.2); lower 6.77–8.03 (0.9 × 1.26) |
| NE (smooth white) | state; ground 6.82–8.82 | state; lower row sill 7.42, 1.3 × 2.2 m; basement windows sill 5.71, 0.8 × 0.65 m | upper 12.31–14.55 (1.34 × 2.24); lower 7.42–9.63 (1.30 × 2.21); basement 5.71–6.36 (0.78 wide); the door up 7 steps, sill 6.89, head 8.79 |
| SE_w (cream) | state; ground 6.82–8.82 | state; small row sill 9.95, 1.25 × 1.15 m; lower small row sill 6.3, 1.25 × 1.2 m | upper 12.9–15.9 (1.5 × 3.0); small 10.0–11.1; lower small 6.3–7.5; three small arched doors. The 2017 photograph agrees: scaled on its upper row, the small row is at 10.0–11.2 |
| SE_e (cream) | state; ground 6.82–8.82 | state; middle row sill 7.75, 1.3 × 2.3 m | upper 11.7–14.2 (2.5 tall); middle 7.7–10.0 (2.3 tall). The 2017 photograph's far-left part has two tall rows; the 9-step stair is at the north end |

**The state-floor row against the panoramas.** Scaled between the courtyard and the eaves:
- **Upper-row sills.** The panoramas put them at 12.3 (NE), 12.3 (SW), 12.9 (SE_w), 11.7 (SE_e) and about 12.0–12.5 (NW). Pass 126 has 11.57.
- **Heights.** The NE upper windows are only 2.24 m high (pass 126: 3.2), SE_e's 2.5. SW's and SE_w's (3.0–3.2) agree.
- **What this means.** Möller's Gyllene section has the courtyard sill at 11.56, which supports pass 126 in the west range. The other ranges may have higher floors, or the courtyard may lie lower: with Möller's floor-to-courtyard height the readings come down by about 0.3–0.4 m.
- **Not moved.** The row is shared and aligned with Gyllene salen's niches (pass 126).

**Rows across the state-floor slab.** Two rows clearly cross the slab level (z 10.17–10.47):
- SW's middle row (9.9–11.1). SW is the chapel range, where Möller's Kyrkan section shows other floor levels.
- SE_w's small row (9.95–11.1), also in the 2017 photograph.

There are no pass 125/126 rooms behind either; the windows show pass 27's glazing, closed behind (blind glass). The prepare script allows them only for SW and SE_w and asserts all other lower rows stay under the slab.

**Spacing.** The measured window axes are irregular, 2.5–4.6 m (NE about 3.0–3.5, SW 2.5–3.6, SE about 3.2–3.5). They are kept at 3.8 so that the lower rows stay under pass 126's state-floor windows.

**Rooms behind the new rows.**
- On the west front, the small row (8.6–9.8) lies below Gyllene salen's floor (slab from 10.17), where the range has no rooms; it is blind glass.
- In Kungstrappan's front (W1–V), it looks into the stair hall over flight 1 and its landing (z 7.97), under the förstuga's slab.
- The walk check through the stair passes unchanged.

**Windows over doors.** Windows within 1.2 m beside a door or below 1.6 m over its arch are left out, on the courtyard fronts only, now also beside the raised doors at the stairs. This also removes pass 27's ground-row windows that overlapped doors at the middle of the long fronts; the hole lists had overlapping holes there before.

**Outside stairs and raised doors (new; `stairs127`).** Both stairs are solid stone steps square to the front, with a landing at the door's sill and iron handrails on both sides. Each door is a plain stone surround with a leaf (`raised_door127`), cut into the wall as a hole that the window rule treats as a door.
- **NE.** The door 11.0 m from the north courtyard corner (pano 1: about 11 m), up 7 risers of 0.20 m (pano: 7 steps, 1.29 m at 38 px/m) to a sill at z 6.87. The door is 1.0 × 1.9 m, the stair 1.5 m wide with a 0.9 m landing.
- **SE_e.** The door 2.5 m from the east courtyard corner, up 9 risers of 0.167 m (1.50 m) to a sill at z 6.97. The door is 1.0 × 2.0 m, the stair 2.0 m wide with a 1.2 m landing.
- **Positions.** The positions along the fronts are estimated (±1.5 m): read at grazing angles, and the outline's corners are pass 27's.

**Not done.**
- The NE aedicule portal with its 3-step stair is in the panorama about 22.8 m from the north corner. In the model, pass 124's portal D (banded Doric, "Drottningtrappan") dresses pass 27's door 7.1 m from the corner at courtyard level. Moving or raising it means changing pass 124's portal mesh, which this pass does not touch.
- SE_w's three small arched doors are still pass 27's single door per long piece.

**Rustication.** The NW and SW courtyard fronts (`RUST127=('NW','SW')`, the lead's change) carry:
- an ochre-jointed wall (`M_Block127_Joint`, sRGB 0.86/0.77/0.62);
- pale blocks 0.88 × 0.36 m in running bond (`M_Block127_Block`, 0.95/0.93/0.87), as single faces 12 mm proud. Thin boxes were tried in run 1; the finishing bevel shrank them;
- lime margins round the openings;
- flat triangular pediments over the state-floor windows;
- a grey band under them;
- a stone plinth that stops at the doorways.

The west range's merged front W1–N (pass 124's `court_front124`, with portals C and E) is dressed too. In run 4 the plinth crossed portal E's open doorway, and the walk check found it: a 0.45 m step and 2 obstructions. It is now cut at every door. All of these are flat colours on town textures. Pass 27's `CourtBlock` ashlar texture is gone.

**Colour.** NE, SE_w and SE_e are `M_Block127_Lime` (0.92/0.89/0.81), lighter than pass 27's `Court` (0.87/0.83/0.73). The panoramas show NE brighter white than SE; one lime tone is used for both.

## Measurement

| Source | Camera / reading | Used for |
|---|---|---|
| Möller 1882, PK006-00041 | scale bar 57.97 px/m; five sections read on full-resolution crops (table above) | courtyard eaves, ridge height and position, pitches; check of the outer eaves |
| Street View 2014, pano `zCIfieeXGQUNANmWu_Tg9A` (south corner area), viewed only | NE square on: true heading 40, 40y. On the front, ground at row 493 and wall top at row 54 give 38.0 px/m with the courtyard at z 5.47 and the eaves at 17.01. SE_e and SE_w: heading 97, 60y; SE_e at column 800: 27.7 px/m; SE_w at column 1180: 32.9 px/m | NE, SE_w, SE_e rows; NE door and 7-step stair; SE_e 9-step stair |
| Street View 2014, pano `jOXzkLldNOjrveyz1T81wg` (NE/E side), viewed only | SW square on: heading 216, 50y, 27.7 px/m. NW: heading 295, 90y, 23.3 px/m | SW and NW rows; portals |
| Commons 2017, `castle27/kalmar-castle-internal-courtyard-2017-07-30.jpg` | resected anew with the lead's identification: camera (−861.1, −292.66), heading 174.9, f 1890 px, level, horizon at row 1115. It uses the south courtyard corner (x 1210), the SE_w/SE_e bend (x 495), the south tower's spire (x 1160) and the well (x 990, base 360 px), with a total residual of 35 px | SE_w and SE_e rows (check), eaves checks (d–f), comparison 689 |
| -wuppertaler 2022, `castle27/swe-kalmar-slott-006.jpg` | camera by search: well bearing and width (f 1450 px assumed), the cap at the upper left taken as Kuretornet's: (−871.56, −318.72), heading 346.3, pitch 12 | NW/NE arrangement, the 7-step stair, eaves check (g); comparison 690 |
| HaSe 2021, vertical aerial | not resected | roof arrangement; comparison |

**Reading error.**
- The panorama readings depend on the eaves line and the ground line read on each front, and on the pano's own projection (level view, verticals vertical). They are ±0.3–0.5 m, worse on the irregular NW front.
- The scale assumes the courtyard at z 5.47 and the eaves at 17.01. With Möller's lower courtyard the readings move down 0.3–0.4 m.
- No pixel of the panoramas was used, and none was saved.

The first 2017 resection (north corner, north tower) had a 10 px fit, but it predicted a visible Kuretornet where the photograph has sky. With the south corner it fits within 35 px, and Kuretornet falls outside the frame.

## Verification

- **Prepare.** `KALMAR_GEO=<pylib> python3 scripts/prepare_block127.py` prints `BLOCK127_PREPARE_OK`. It asserts:
  - the courtyard eaves are in 16.6–17.4;
  - Möller's outer eaves agree with pass 27's within 0.4 m;
  - the courtyard eaves are above Gyllene salen's ceiling plane;
  - the overlap is under 0.01 m², and so is the gap;
  - no courtyard wall rises through the roof;
  - every dormer stands on its own slope;
  - no chimney stands in a tower;
  - every lower window row stays under the state-floor slab, except SW and SE_w;
  - each stair fits on its front piece.
- **Sandbox runs** (prelude pass 126; `SCR/p127/build_block127_check.py`; logs `SCR/p127/log1.txt`–`log5.txt`). All five print `SANDBOX_DONE` without errors.
  - Run 2: rustication as flat faces, wider aerial.
  - Run 3: the west range's dormer moved, the 2022 camera.
  - Run 4: the lead's identification, the measured rows, the stairs. The walk check failed here on the plinth across portal E.
  - Run 5: the plinth cut at the doors; all checks pass.
- **Repeatability (run 5).** The build runs twice on the same scene: `REPEAT127 True` (SM_Kalmar_Slott, vertex and face hash).
- **`drop_degenerate_faces127`** (with `_thin`) removes 2 faces of 314,211.
- **Export frame check (run 5).** It uses pass 126's wrapper: the export tail's preparation, the exporter's frame test, and a test FBX export. Result: 0 invalid loops, 1 of 1 exports succeeded, and the fallback frame covers 5,659 loops (pass 126: 4,953).
- **Walk checks (run 5).** These are pass 126's routes, re-run with ray casts every 0.2 m, obstruction rays at 0.45 and 1.4 m, and a headroom ray of 2.0 m. All pass, with the same numbers as pass 126:

| Route | Samples | Missing | Largest step | Obstructions | Low headroom | Height |
|---|---|---|---|---|---|---|
| Courtyard → portal E → Kungstrappan → förstuga → Gyllene salen → 61a → Kungsmaket's west niche | 330 | 0 | 0.167 | 0 | 0 | 5.47–10.47 |
| Gate passage, portal B → portal C | 120 | 0 | 0.021 | 0 | – | 3.70–5.49 |
| Portal C → D / E / F | 35 / 42 / 187 | 0 | 0.012 | 0 | – | 5.47–5.48 |

- **Roof clearance.** An upward ray was cast from every vertex above z 15.5 of the pass 125/126 rooms. All 54,748 such vertices of Gyllene salen (up to z 17.27) meet the castle roof above them. Kungstrappan, Kungsmaket and Förrum have none above z 15.5.
- **Comparisons** (`SCR/p127/sb5/`):
  - **`cmp_courtyard2017.jpg`.**
    - The south tower's cap now stands where the photograph has it.
    - SE_w (middle) has its tall upper row, the small row and the lower small row.
    - SE_e beyond the bend has two tall rows, as the photograph's far left.
    - SW on the right is rusticated, with portal F by the corner.
    - The courtyard slopes, the chimneys and the red dormer are visible.
  - **`cmp_well2022.jpg`.** NW rusticated on the left with Kuretornet above, NE white on the right, as in the photograph.
  - **`cmp_aerial.jpg`.** The roof arrangement from above.
  - **`sheet_views.jpg`.** The NE door and 7-step stair beside portal D, the SE_e raised door and stair, SW square on (as pano 2 at 216), and NW square on with portals C and E and Kuretornet behind (as pano 2 at 295).
- **Official build:** done by the lead on 2026-10-03; see "Official build".

## What remains

- **The state-floor row.** The panoramas put its sills 0.7–1.3 m higher than pass 126 on NE, SW and SE_w, and NE's upper windows are only 2.24 m tall (pass 126: 3.2). It is shared and kept; see section 4.
- **The courtyard level.** Möller puts the state floor 5.55–6.08 m above the courtyard ground (mean 5.70). Pass 126 has 5.00 (courtyard z 5.47). By Möller, the courtyard would be about 0.7 m lower (z ≈ 4.8). Not changed here.
- **Pass 126/125 against Möller.** The state-floor window head is 14.23 in Möller, 14.77 in pass 126. Gyllene salen's height is 5.4 m in Möller, 6.2 m in pass 125. Not changed.
- **Portals.**
  - The NE aedicule with its 3-step stair should stand about 22.8 m from the north corner. Pass 124's portal D is at 7.1 m at courtyard level, and that is pass 124's mesh.
  - The NW relief portal reaches about z 12.2 in the panorama, higher than pass 124's portal C.
- **NW's irregular windows** (centre, by Kungstrappan) are simplified to the state row and one small row.
- **Window spacing** is kept at 3.8 m (measured 2.5–4.6 m, irregular).
- **Gable steps.** The large steps between the ranges (SE_e/SE_w, NE/SE_e, NW/NE) come from pass 27's range rectangles. They are now closed, but they are not checked against photographs; real roofs probably meet in valleys there.
- **Chimneys.** These keep this pass's first placement (SW, NW, NE, SE_w courtyard slopes). The photographs show the tall chimneys of the 2017 view on the SE range, where only one is placed.
- **Not modelled:** SE_w's three small arched doors, the snow guards and ladders, the chain pattern of the band, the scrollwork in the pediments, the chimney pots.
- **Collision.** No Unreal test; the walk checks are Blender ray casts only.

## Sources

| Source | Licence | Used for |
|---|---|---|
| Carl Möller, "Calmar slott. Profiler", January 1882, Riksarkivet PK006-00041 (`castle-sources/riksarkivet/`) | public domain | eaves, ridges, pitches, ridge position, window heights |
| Pass 27 (`source/castle27.json`, its notes and `TOWER_SPEC`), pass 124, pass 125 (`source/block125.json`), pass 126 (`source/block126.json`) | project | outline, ranges, levels, tower caps, rooms, rows |
| `castle27/kalmar-castle-internal-courtyard-2017-07-30.jpg` (Commons 2017) | PD | rows, rustication, dormers, chimneys, eaves checks |
| `castle27/swe-kalmar-slott-006.jpg` (-wuppertaler 2022) | CC BY-SA 4.0 | rows, outside stair, rustication question |
| Google Street View 2014, courtyard panoramas `zCIfieeXGQUNANmWu_Tg9A` and `jOXzkLldNOjrveyz1T81wg` | viewed only | which front is which (the lead), rows, stairs, portals |
| `castle27/schloss-kalmar-senkrecht-luftaufnahme-2021-.jpg` (HaSe 2021) | as in castle27/sources.json | roof arrangement |
| A. Mayer, Commission scientifique du Nord, "Cour du château de Kalmar" (1840s) | public domain | three rows and outside stairs on the courtyard fronts (pre-restoration) |
| Olsson, *Fornvännen* 1974 (as read by pass 125), kalmarslott.se accessibility page | read only | room numbering, the 7 steps |

Google imagery was only viewed (the two panoramas above, for the rows and the identification). No pixel of any photograph or drawing is used as a texture. The new materials (`M_Block127_Lime`, `_Joint`, `_Block`, `_Band`, `_Plinth`) are flat tints on TownPaintWhite and TownStone. The rest of the mesh keeps pass 27's materials.

## Lead's correction: the rustication is on NW and SW

The lead checked two 2014 Google Street View panoramas in the courtyard, viewed only (no pixels used):
- `zCIfieeXGQUNANmWu_Tg9A` at 56.6578188, 16.3553971
- `jOXzkLldNOjrveyz1T81wg` at 56.6579135, 16.3556968

Both pano positions are several metres off. The fronts were therefore identified by the headings at which each is seen square-on. Pass 27's ranges face (true): NE 40, SE_e 118, SE_w 140, SW 216, NW 295. The local heading is the true heading + 28.2.
- **NW:** painted rustication (pale blocks, ochre joints). The big relief portal with an arcade is at its north end.
- **SW:** painted rustication. Its aedicule portal is near the south end, and the gate passage's arch is at the corner.
- **NE:** smooth bright white. It has the door with the 7-step outside stair and an aedicule portal.
- **SE_w and SE_e:** plain cream lime. They have a 9-step outside stair at the north end, small arched doors, the red-fronted dormer and the chimneys.

The agent had built the rustication on NE. A first quick correction by the lead put it on SW and SE_w, because the lead converted headings with the wrong sign; that correction was withdrawn before any build. `build_block127.py` now has:
- `crange127(p,q,raw=True)`
- `RUST127=('NW','SW')`

**Window rows.** The rows had been assigned through the same wrong reading. The agent measured them again on both panoramas, each front square on, and re-read the 2017 and 2022 photographs with this identification. It also added the NE and SE_e outside stairs with their raised doors; see section 4.

## Official build

The lead built pass 127 officially on 2026-10-03, with `RUST127=('NW','SW')` and the re-measured rows.
- **Checks:** the geometry check passed on the second rebuild (True), the FBX audit passed (exit 0), and the two rebuilds gave identical meshes.
- **Prevhash:** it reports only intended changes:
  - pass 126's `SM_Kalmar_Slott`, which this pass re-creates;
  - pass 124's and 125's castle meshes, as in pass 126;
  - the earlier mainland corrections.
- **Dry renders:** cameras 689–694 rendered.
- **Unreal:** the import is deferred.
