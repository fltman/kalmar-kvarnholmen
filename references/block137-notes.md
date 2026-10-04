# Pass 137: Kalmar slott, Kungsköket's hearth, Gröna salen's window and other corrections

Pass 137 works through the open issues that passes 129–135 left on Kalmar slott. It uses only sources that are already in the project; nothing new was fetched and the browser was not used.

| # | Open issue (pass) | Result |
|---|---|---|
| 1 | Kungsköket's hearth is square with a four-sided hood (135, issue 8) | **rebuilt**: rounded corners, a projecting top course, a convex round hood into the arch, a round flue |
| 2 | Gröna salen's far end wall has two windows, the facade one (131, issue 3) | **added**: the second state-floor window on the SW outer front at SW s 1.55; Gröna salen's blind niche now runs through to it |
| 3 | North tower's wall top may be 1.2 m higher (132) | **not changed**: the two Möller sheets disagree by 1.65 m |
| 4 | NE's courtyard front is rusticated in 2022, smooth in 2014 (129) | **changed**: NE gets pass 127's painted rustication |

| Mesh | Category | Status | What changed |
|---|---|---|---|
| `SM_Kalmar_Slott` | Kalmar slott/Castle | re-created, `detail_pass=137`, `corrects_pass=27,124,126,127,128,129,133,135` | the SW outer front's new window (task 2); NE's courtyard front rusticated (task 4) |
| `SM_Castle124_Portals` | Kalmar slott/Castle | re-created by the composition, `detail_pass=137`, `corrects_pass=124,126,129,133,135` | no geometric change (same hash) |
| `SM_Castle124_Paving` | Kalmar slott/Ground | re-created by the composition, `detail_pass=137`, `corrects_pass=124,126,129,133,135` | no geometric change (same hash) |
| `SM_Castle135_Kungskoket` | Kalmar slott/Interiör | re-created, `detail_pass=137`, `corrects_pass=135` | the hearth and its hood (task 1); the rest is pass 135's |
| `SM_Castle135_KungskoketInventarier` | Kalmar slott/Interiör | re-created, `detail_pass=137`, `corrects_pass=135` | the trammel bars follow the hearth's new openings |
| `SM_Castle131_GronaSalen` | Kalmar slott/Interiör | re-created, `detail_pass=137`, `corrects_pass=131` | the end wall's second niche is no longer blind: it runs to the facade's glass |

`SM_Kalmar_Slott_Towers`, `SM_Castle130_Slottskyrkan`, the other rooms of passes 125, 126, 131 and 133, and pass 136's mainland houses are not touched.

**Method** (the cross-pass pattern):
- `build_block137.py` takes `build_block135.py` from `def rep135` to `furnish135(*kitchen135())`. That slice re-runs pass 135's composition (which re-runs pass 133's composition of passes 124–129 and 133) and pass 135's kitchen. It runs in a private namespace (`NSP137`) with pass 135's materials mapped by name.
- Its replacements, each asserted to occur the expected number of times:
  - the marking (`detail_pass=137`, the `corrects_pass` lists, the asserts and print labels, the kitchen's `corrects_pass='135'`);
  - `SRC133=EDITSRC135(SRC133)` becomes `SRC133=EDITSRC137(EDITSRC135(SRC133))`. `EDITSRC137` makes three single replacements on the composed source: `EXTRA137` runs in pass 27's namespace after `EXTRA135`; `RUST127=('NW','SW')` becomes `('NW','SW','NE')`; and `edit_castle127` gets one more replacement on pass 27's own outer-front rule (`doors=[…] if (i,j)==longest else []` gains `+OUTWIN137.get((i,j),[])`);
  - the kitchen's hearth data come from `source/block137.json`, and the hearth's block (from `H=K135['hearth']` to the old flue box) is replaced by a call to `hearth137`.
- Gröna salen: `build_block131.py` from `def b131_new` to the furnishings runs again in its own namespace (`NSG137`), with pass 131's materials mapped by name and `B131D['gron']` taken from `source/block137.json`. The marking line is the only replacement.
- `scripts/prepare_block137.py` re-runs `prepare_block131.py` in a private namespace with its two file writes removed. Unchanged, the re-run reproduces `source/block131.json` exactly (asserted). With the one replacement `niche_sw(1.55,…,blind=True)` → `niche_sw(1.55,…)`, only `gron.niches` and `gron.wallbands` change (asserted); Förbrända salen's data are identical.
- Every re-created mesh then gets `drop_degenerate_faces137` and this pass's marking (`finish137`).

## 1. Kungsköket's hearth

### Sources

The 1969 photographs of Dagmar Selling (Kalmar läns museum, DigitaltMuseum, PDM), already in `castle-sources/` (pass 135):
- **021017090089, "Spisens norra del"**: the stack under the cross wall's wide arch, seen from the north part's outer side. The near corner is a curved face, not an arris. There is a projecting course at the stack's top. The hood above it has a curved outline and rises into the arch.
- **021017090090, "Spisens södra sida"**: the long south face with **two** round-headed openings and a middle pier of about the openings' width, iron trammel bars across both. Above it the hood is a trapezoid with rounded shoulders, brick in its lower part and plastered above.
- **021017090086, "Spisen, östra väggen"**: the stack's near corner is again rounded, with the top course and a rounded hood above it.
- **021017083364/083365** (sketches): the arrangement only (openings on two faces, the stack under the arch).

### What changed (`hearth137`)

The stack keeps pass 135's footprint (3.0 × 3.6 m, s 11.95 / c −6.697 in the SE_w frame), wall thickness (0.50 m), plinth, heights (base z 5.22, top z 7.70) and hood top (z 9.54). Only the form changes:

| Part | Pass 135 | Pass 137 | Source |
|---|---|---|---|
| Plan | square corners | rounded rectangle, corner radius **0.70 m**; the corners are quarter rings (outer 0.70, inner 0.20) | 090086, 090089 (curved corner) |
| Long faces | two openings 1.10 m wide, middle pier 0.50 | two openings **0.80 m** wide, middle pier 0.50 (they must stay on the straight part, |c| ≤ 1.10) | 090090 |
| Short faces | one opening 1.20 m | one opening **1.10 m** (on the straight part, |s| ≤ 0.80) | 090089 |
| Fire bed, soot ceiling | rectangles | rounded rectangles (radius 0.20) inside the walls | – |
| Top course | none | 0.06 m proud, 0.10 m high, whitewashed | 090086, 090089 |
| Hood | a four-sided frustum to 1.0 × 1.5 m | a loft of 7 rings from the stack's rounded outline to a **circle of r 0.55 m**, each point keeping its polar angle; the profile is convex (blend t^1.5); the lower two bands brick, the rest whitewashed | 090089 (curved outline), 090090 (brick below, plaster above) |
| Flue | a box into the cross wall | a round shaft, r 0.40 m, from the hood's top to 0.10 m over the arch's crown (z 9.80) | – |

Checks in `prepare_block137.py` (asserted):
- the openings lie on the straight parts with 0.05 m to spare;
- every hood point within the cross wall's thickness (±0.10 m) stays under the arch's intrados with at least **0.128 m** (the same minimum over all points);
- the flue lies inside the wall's thickness (s 11.55–12.35 in a wall of 11.45–12.45);
- the rounded plinth lies inside pass 135's square one, inside the arch's opening, and pass 135's kitchen route stays 0.83 m clear of it.

The furnishings are re-created unchanged in code; the trammel bars and pot hooks follow the new openings because they read the hearth's data.

### Estimated

The corner radius, the opening widths, the hood's profile and the top course are read by eye from the photographs; none of the 1969 cameras is known. The photographs show a north face (090089) whose openings are not symmetric about its middle; the model keeps pass 135's symmetric layout.

## 2. Gröna salen's second end-wall window

### Source and resection

`references/castle27/kalmar-slott-9-kalmar.jpg` (Commons, "Kalmar Slott 9, Kalmar", Hstad 2009, CC BY-SA 3.0, 1280 × 857) shows the castle from the meadow west of the castle: postej W in front on the left, the SW range's outer front between the west and south towers, Kuretornet and the north tower behind on the left, postej S on the right. Cannons stand on the rampart in front of the front, as along the model's SW rampart. The camera was resected by least squares on six bearings (pixel columns of the axes): postej W (312), postej S (1138), tower W (448), tower S (772), Kuretornet (362) and tower N (262).

| Result | Value |
|---|---|
| Camera | (−1107.3, −354.2), bearing 82.8 (Street View heading 54.6) |
| Focal length | 1649 px (vfov 29.14) |
| Residuals | −0.6, −1.1, 1.5, 1.5, −0.1, −1.0 px |

Columns on the front were then intersected with the SW outer face (pass 27's CO7→CO8 line):

| Feature | Columns (px) | SW s (m) |
|---|---|---|
| West tower's silhouette | 490.6 | −0.86 |
| First window | 493.7–502.5 | −0.47 to 0.66 (axis 0.08, width 1.13) |
| Second window | 512.0–521.0 | 1.88 to 3.04 (axis 2.46, width 1.16) |
| Next windows (chapel) | 579, 608 | 10.6, 14.5 |
| South tower's silhouette | 723.8 | 30.3 (model ~30.5) |

The two windows by the west tower are 2.38 m apart, with a pier of about one window's width between them, as pass 131 read inside (the 2017 and 1929 photographs). One small arched attic window stands over the second one only, as in the model.

### Placement

- The model's single window (pass 27's rule) is at s 3.69, about 1.2 m east of the photograph's second window (the model's west tower and outline are also about 0.7 m off there).
- From the model's window the measured spacing puts the second at **s 1.31**.
- Gröna salen's niche for it cannot come nearer the west tower's lining than s 1.55 (pass 131's 0.25 m clearance; at 1.31 the niche's room face would be 0.09 m from the lining). The window is therefore put on the niche's axis, **s 1.55** (0.24 m from the spacing reading). The pier between the two windows is 0.99 m (photograph 1.22 m).
- In pass 27's frame of edge CO7→CO8 (7.374 m long) this is u −2.136; the window is a main-row window like the others (1.15 × 3.20 m, sill z 11.57, head 14.77), drawn by pass 27's own `front()`.

### Gröna salen

`prepare_block137.py` re-runs `prepare_block131.py` (asserted identical to `source/block131.json` unchanged) with the end niche at 1.55 no longer blind. The niche now runs to the facade's glass like the one at 3.69 (depth 1.50 m), and pass 131's own window and soffit stand in it at the glass. Only the niche list and the wall bands change; Förbrända salen's data are identical.

## 3. The north tower's wall top: not changed

| Reading | Value |
|---|---|
| Möller 1882, "Profil genom Kungsmaket" (PK006-00041), 57.97 px/m (pass 127's scale) | red state-floor line at row 4270.7; the tower's eaves (top of the cornice where the roof starts) at row 3565.7: **12.16 m over the floor, z 22.63** |
| same section, check | Kungsmaket's height (floor to the room's cornice, row 4017) 4.38 m; pass 125 has 4.3 m |
| Möller 1885, "Ritning till nytt tak å norra tornet" (PK006-00049) | a dimension "13.5 fot" from the tower's eaves down to an adjoining cornice with brackets, at the right of the elevation: **4.01 m** |
| if that cornice is the range's outer eaves (z 20.27) | tower eaves z **24.28** (1.0 m over pass 27's 23.27) |
| if the 1882 eaves are right | the cornice is at z 18.62, which is no eaves in the model |

The two sheets disagree by 1.65 m. The 1882 section is internally consistent (Kungsmaket's height agrees with pass 125), and it puts the eaves 0.64 m **below** pass 27's, not above. The 1885 sheet's cornice is drawn beside the tower's small arched windows, so it may belong to a lower building (for example Olsson's small tower XII) rather than the range. The brief asks for two agreeing sources; there are none, so `SM_Kalmar_Slott_Towers` is not re-created. Kungsmaket (pass 125) and Gröna salen (pass 131) are therefore unaffected.

## 4. NE's courtyard front: rusticated

`castle27/swe-kalmar-slott-006.jpg` (-wuppertaler 2022, CC BY-SA 4.0; pass 129's camera 690) shows NE left of the well clearly: painted blocks, lime margins round the windows, the pediments over the state-floor windows and the chain band under them, as on NW and SW. SE_e on the right is plain cream lime. The Street View panoramas of 2014 show NE smooth white, so NE was repainted between 2014 and 2022. The project models today's town, so NE now gets pass 127's dressing:
- `RUST127=('NW','SW')` becomes `('NW','SW','NE')` in the composed source;
- NE's straight courtyard line runs on over CI5–CI6 to the east corner (pass 129). Pass 127's nearest-range test gives that 5.95 m edge to SE_e, so it is added by name (`rust137`, used by `cmat127` and `dress127`).

The rows, doors, portal D and its stair are unchanged. Pass 127's block faces (`M_Block127_Block`) on `SM_Kalmar_Slott` grow from 1,516 to 2,296 (run 3; run 2, without the CI5–CI6 edge, had 2,070 and left the 6 m by the east corner white).

## Cameras

| Camera | Where | Look | Compared with |
|---|---|---|---|
| `750_Block137_Cal_Hearth1969North` | Kungsköket, SE_w s 16.6, c −3.4, floor + 1.5 | towards the hearth's centre, pitch 10, vfov 66 | 090089 ("Spisens norra del"), by eye |
| `751_Block137_Cal_Hearth1969South` | Kungsköket, SE_w s 6.6, c −6.7, floor + 1.5 | +s (north), pitch 15, vfov 64 | 090090 ("Spisens södra sida"), by eye |
| `752_Block137_Cal_SWFront_GronaWindows` | (−1107.3, −354.2), z 2.0 | Street View heading 54.6, pitch 5.1, vfov 29.14 | Commons "Kalmar Slott 9" — **resected** (6 points, ≤1.5 px) |
| `753_Block137_Cal_Well2022_NE` | pass 129's camera 690: (−878.55, −309.10), ZC + 1.6 | heading 81.5, pitch 12.4, vfov 67.24 | `swe-kalmar-slott-006.jpg` (2022) |
| `754_Block137_Aerial_Castle` | (−960, −380, 62) | towards (−878, −312, 12), 24 mm | – |

Camera 752's pitch was set from the eaves row (photograph row 432.5; the render puts the eaves at row 431). The model's park trees stand between this camera and the castle; the sandbox comparison renders it with a near clip of 110 m.

## Verification

### Prepare

`KALMAR_GEO=<pylib> python3 scripts/prepare_block137.py` prints `BLOCK137_PREPARE_OK`. It asserts the hearth checks above, that the re-run of pass 131's prepare reproduces `source/block131.json` exactly, that the unblinded re-run changes only `gron.niches` and `gron.wallbands`, the window's place on its edge (u −2.136, s 1.551, pier 0.99 m to pass 27's window), and the north-tower readings (Kungsmaket's height within 0.15 m of pass 125's, the disagreement over 1 m).

### Sandbox

Three runs with `SCR/p137/build_block137_check.py` (it renders the views before the build, builds twice, runs all checks, renders again) and `SCR/p137/sandbox137.py` (pass 135's copy, Workbench shadows off), prelude **136**. Logs: `SCR/p137/log_r1.txt`–`log_r3.txt`.
- **Run 1** built (6 meshes), then stopped in the check: the build's `_h0` overwrote the harness's hash table of the same name. All the build's private globals were then prefixed with 137.
- **Run 2** printed `SANDBOX_DONE prelude 136` with all checks passing. Its renders showed NE's last 6 m by the east corner still white (the CI5–CI6 edge; see task 4). The hearth cameras were moved to fit the photographs better.
- **Run 3** is the final run on the final files; the numbers below are run 3's.

**Change set and repeatability:**
- `CHANGED137 ['SM_Castle131_GronaSalen', 'SM_Castle135_Kungskoket', 'SM_Castle135_KungskoketInventarier', 'SM_Kalmar_Slott']`; `SM_Castle124_Portals` and `SM_Castle124_Paving` are re-created with the same hashes. No other mesh in the scene changes (`SM_Kalmar_Slott_Towers`, `SM_Castle130_Slottskyrkan`, `SM_Castle131_GronaInventarier`, `SM_Castle131_ForbrandaSalen` and pass 136's houses included).
- `REPEAT137 True`; the second run changes nothing.

**Polygons and degenerate faces:**
- `SM_Kalmar_Slott` 318,348 faces (pass 135: 313,159), Portals 10,638, Paving 1,040, Kungskoket 7,268 (pass 135: 6,134), furnishings 1,964, Gröna salen 15,728.
- `drop_degenerate_faces137` removes 0 faces from each of the six meshes (pass 131's own filter inside the Gröna section removes its usual 5 bevel slivers first).

**Export frame check** (pass 135's wrapper: the export tail's preparation, the exporter's frame test, a test FBX export of each mesh): 0 invalid loops; 6 of 6 exports succeeded. Fallback frames: `SM_Kalmar_Slott` 5,876 loops, Portals 0, Paving 15, Kungskoket 176, furnishings 3, Gröna salen 366.

**Placement and intrusion:**
- `EXTENT137`: every vertex of the kitchen meshes lies in pass 135's envelope and z 4.80–11.55 (furnishings to 6.41), and every vertex of Gröna salen in pass 131's envelope and z 10.17–17.42: 0 outside.
- `INTRUDE137`: no vertex of any other mesh inside Gröna salen's envelope. Inside the kitchen's envelope only the facade's open-arch thresholds of `SM_Kalmar_Slott` (24 vertices at z 5.47–5.48), as in pass 135 (its open issue 7).
- `WINRAY137`: horizontal rays from outside the SW front at s 1.55 (z 12.4 and 13.9) meet the new window's frame and glass (`M_Town_Glass`) 2.91 m in, then Gröna salen's own window in the niche (3.13 m). At s 1.15 and 1.95 they meet the facade glass and then the niche's panes, so the niche is open through the wall. At s 3.69 the old window gives the same sequence.
- `ROOFCLEAR`: all interior vertices above z 15.5 stand under the castle roof (12 meshes, 0 not under the roof).
- `NE_RUST137`: `M_Block127_Block` faces 1,516 → 2,296.

**Walk checks** (ray casts every 0.2 m, obstruction rays at 0.45 and 1.4 m, a 2.0 m headroom ray):

| Route | Samples | Missing | Largest step | Obstructions | Low headroom | Height |
|---|---|---|---|---|---|---|
| Pass 135: kitchen (gate passage → south exit → under the arch both sides of the hearth → north exit) | 423 | 0 | 0.128 | 0 | 0 | 5.10–5.48 |
| Pass 133: courtyard → Kyrkportalen → stair → chancel (Kyrktrappan) | 328 | 0 | 0.176 | 0 | 0 | 5.47–10.75 |
| Pass 133: Gröna salen → chapel | 46 | 0 | 0.012 | 0 | 0 | 10.47–10.48 |
| Pass 130: chapel | 117 | 0 | 0.14 | 0 | 0 | 10.46–10.75 |
| Pass 131: Gröna salen / Förbrända salen | 204 / 241 | 0 | 0.18 / 0.015 | 0 | 0 | 10.46–10.65 |
| Pass 126: courtyard → portal E → Kungstrappan → Gyllene salen → Kungsmaket | 330 | 0 | 0.167 | 0 | 0 | 5.47–10.47 |
| Gate passage B → C | 120 | 0 | 0.021 | 0 | – | 3.70–5.49 |
| Portal C → D (old) / E / F (old) | 35 / 42 / 187 | 0 | 0.012 | 0 | – | 5.47–5.48 |
| Pass 129: portal C → D's stair → landing | 125 | 0 | 0.163 | 0 | – | 5.47–5.96 |
| Pass 133: portal C → Kyrkportalen's slab path target | 206 | 0 | 0.012 | 0 | – | 5.47–5.48 |

All earlier routes give the same numbers as in pass 135.

### Comparisons (`SCR/p137/final/`; photograph | before | after)

- **`cmp_hearthN.jpg`** (090089) and **`cmp_hearthS.jpg`** (090090): the rounded stack, the top course and the convex hood rising into the arch replace the box and the four-sided hood. In 090090 the hood is taller and reaches the ceiling beams more broadly than the model's; the photographs' stack is rougher and partly whitewashed.
- **`cmp_swfront.jpg`** and **`cmp_swfront_zoom.jpg`** (Commons "Kalmar Slott 9", camera 752): the eaves and the towers fall within about 10 px of the photograph. After the change the west end has two state-floor windows close together, a long pier, then the chapel's pair, as in the photograph. The model's pair stands about 1.2 m further east than the photograph's (see Limitations), and the model's rampart hides more of the windows than the real one.
- **`cmp_swclose.jpg`**: the SW outer front from close by, before and after.
- **`cmp_well2022.jpg`** (2022, camera 753) and **`cmp_neclose.jpg`**: NE now rusticated up to the east corner, as in the photograph; SE_e stays plain.
- **`cmp_grona2017.jpg`, `cmp_gronaend.jpg`**: Gröna salen's end wall, the two windows (the left one's niche now open to the facade). Workbench without lights shows little difference inside.
- Other views: `cmp_kitchen_long.jpg`, `cmp_aerial.jpg`.

### Pending

The official build is done (see "Official build"); the Unreal checks are pending.

## Limitations and open issues

1. **The SW outer front's windows are about 1.2 m east of the photograph.** The photograph puts the end wall's windows at SW s 0.08 and 2.46; the model has 1.55 and 3.69 (pass 27's single window plus this pass's). Moving pass 27's window and both of Gröna salen's niches westwards would need the west tower's lining in the room to move (the model's tower and outline are about 0.7 m off there).
2. **The new window is 0.24 m further east than the measured spacing**, because Gröna salen's niche keeps pass 131's 0.25 m clearance to the tower's lining. The pier is 0.99 m against the photograph's 1.22 m.
3. **The north tower's wall top** is unresolved. Möller 1882 gives z 22.63 (0.64 m under pass 27's), Möller 1885's adjoining cornice gives z 24.28 if it is the range's eaves. A third source is needed: a measured elevation, or a photograph from a known camera, for example from the bridge at about local (−895, −230), heading 125, pitch 20 (pass 132's suggestion).
4. **The hearth's form is read by eye.** The 1969 cameras are not known; the corner radius (0.70 m), the openings (0.80 and 1.10 m) and the hood's profile are estimates. 090089 suggests the north face's openings are not symmetric; the model keeps them symmetric. 090090's hood reaches the beams more broadly than the model's.
5. **Camera 752's height** (2.0 m over the model's datum) is assumed; the pitch was fitted to the eaves row. The model's park trees block this view in Unreal unless the camera's near clip is raised.
6. **NE's rustication** follows pass 127's NW/SW dressing (block size, band, margins, pediments); the 2022 photograph's chain pattern in the band and the exact block layout are not modelled.
7. **Collision.** No Unreal collision test; the walk checks are Blender ray casts.

## Sources

| Source | Licence | Used for |
|---|---|---|
| Kalmar läns museum, D. Selling 1969, Kungsköket (DigitaltMuseum 021017090086, -090089, -090090; `castle-sources/`) | PDM | the hearth's form; comparisons 750, 751 |
| Kalmar läns museum, sketches 021017083364/083365 | PDM | the hearth's arrangement only |
| Commons "Kalmar Slott 9, Kalmar" (Hstad, 2009; `castle27/kalmar-slott-9-kalmar.jpg`) | CC BY-SA 3.0 | the SW outer front's west-end windows; resected camera 752 |
| Commons "Kalmar Castle Museum, Green Hall, 2017-07-30" (`castle-sources/`) | PD | Gröna salen's two end-wall windows (as read by pass 131) |
| -wuppertaler 2022, `castle27/swe-kalmar-slott-006.jpg` | CC BY-SA 4.0 | NE's rustication; camera 753 |
| C. Möller, "Calmar slott. Profiler", 1882 (PK006-00041) | public domain | the north tower's eaves and Kungsmaket's height |
| C. Möller, "Ritning till nytt tak å norra tornet", 1885 (PK006-00049) | public domain | the 13.5 fot dimension to the adjoining cornice |
| Passes 27, 127, 129, 131, 132, 135 (`castle27.json`, `block129.json`, `block131.json`, `block135.json`) | project | outline, edges, frames, niches, the kitchen |

No pixel of any photograph or drawing is used as a texture. No new material is added: the hearth uses pass 135's materials, Gröna salen pass 131's, the facade pass 27's and 127's.

## Official build

The lead built pass 137 officially on 2026-10-04.
- **Geometry and export:** the geometry check passed on the second rebuild (True), the FBX audit passed (exit 0), and the two rebuilds gave identical meshes.
- **Prevhash:** only intended changes.
  - Pass 135's `SM_Kalmar_Slott`, `SM_Castle135_Kungskoket` and `SM_Castle135_KungskoketInventarier` changed.
  - Pass 131's `SM_Castle131_GronaSalen` changed.
  - Pass 136's 54 meshes are identical.
  - The rest are known earlier corrections.
- **Dry renders:** cameras 750–754, 5 of 5.
