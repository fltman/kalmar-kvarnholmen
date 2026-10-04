# Pass 141: Kalmar slott, the north tower's height

Pass 141 settles the height of the north round tower's wall top (Kungsmakstornet, model key N): the eaves, the top of the cornice where the copper starts. Pass 27 put it at z 23.27 by eye. Pass 137 (task 3) found that two Möller sheets disagree by 1.65 m and left it unchanged. This pass adds a third source, three views with resected cameras, and raises the wall top to **z 24.28** (+1.01 m). The cap moves up with it.

| Mesh | Status | How |
|---|---|---|
| `SM_Kalmar_Slott_Towers` | re-created, `detail_pass=141`, `corrects_pass='27,124,125,126,132'` | pass 132's composition (pass 126's composition of pass 124's code, which re-runs pass 27's towers section with pass 132's caps) in a private namespace (`NSP141`), with asserted single replacements: N's `top` in pass 27's `TOWER_SPEC` (24.6 → 25.61, i.e. z 23.27 → 24.28); a flashing collar after N's cap (`collar141`); pass 132's marking replaced by this pass's. Pass 125's cut for Kungsmaket's door is applied again, as in pass 132. |

No other mesh changes (see Verification). The W, S and E towers, Kuretornet, the ranges and roofs (`SM_Kalmar_Slott`) and the interiors are not touched.

## The question

| Source | Reading | N eaves |
|---|---|---|
| Möller 1882, "Profil genom Kungsmaket" (PK006-00041), pass 137's reading | eaves 12.16 m over the state floor (z 10.47); Kungsmaket 4.38 m high (pass 125: 4.3) | **z 22.63** |
| Möller 1885, "Ritning till nytt tak å norra tornet" (PK006-00049), pass 137's reading | 13.5 fot (4.01 m) from the tower's eaves down to an adjoining bracketed cornice, taken as the range's outer eaves (z 20.27, pass 27, confirmed by Möller 1882 via pass 127) | **z 24.28** |
| Pass 27 | estimated by eye | z 23.27 |

## Third source: three views with resected cameras

### Method

- The model points come from `source/castle27.json`: the tower centres and radii (OSM), Kuretornet's rectangle (pass 27's `KRECT`), and the castle outline. The ranges' outer eaves are at z 20.27 on the outline edges (pass 27, pass 127).
- **Horizontal resection:** least squares on the columns of the tower silhouettes. Each silhouette is the bearing of the tangent to the tower's circle, so each tower gives its bearing and its distance. Kuretornet's corners or its lantern axis were added where visible.
  - Kuretornet's corners systematically miss by 10–30 px. Its model outline is 17.1 × 16.0 m against Möller's 14 m square (pass 132), so they are weighted down or used only as a third bearing.
- **Vertical:** neither the camera's height nor the pano's pitch is trusted. In each view the pitch is fitted so that the range's outer eaves, on the outline edge just beside the tower, come out at z 20.27. The tower's eaves are then read on the model's cornice cylinder (radius + 0.24 m) at two kinds of point:
  - **front:** the column of the highest point of the copper's lower edge, intersected with the cylinder;
  - **tangent:** the copper's lower edge at the tower's silhouette, at the tangent distance.
  
  This is a local, relative measurement: the tower's eaves against the range eaves 0–3 m beside it at nearly the same distance, so errors in camera height and pitch largely cancel.
- **Tools:** `SCR/p141/model.py` and `v004*.py` (the photograph), and `sv1*.py` and `sv2*.py` (the panoramas). They use the same projection as `SCR/p82/meas.py` and pass 129's `r22c.py`, with an added roll.
- **Street View** was viewed only, through the browser's own tab. Screenshots of the viewer (1014 × 764) were read for pixel coordinates. The fov in the URL is the vertical field of view, and the pitch is the 't' value minus 90. No imagery was downloaded or used as texture.

### The views

| View | Camera (resected) | Range eaves used (z 20.27) | N eaves: front | N eaves: tangents | W eaves |
|---|---|---|---|---|---|
| **Photo 2022**, `castle27/swe-kalmar-slott-004.jpg` (-wuppertaler, 2022-06-07, CC BY-SA 4.0, 1920 × 1440), from the north shore of the moat | (−898.9, −176.3), z 2.0, heading 140.3, pitch 9.2, f 1444 px (vfov 52.97) | NW outer eaves right of N, rows 681–681.5 at columns 667–700 | 24.6–24.8 | 25.0–25.2 | 24.1–24.5 front, 24.9–25.2 tangent |
| **SV 2014, bridge**: pano `iMd5WI6ugBpN7x-8vlt6pA` (Sep 2014), on the castle bridge; views 40y/92h/104t, 55y/103h/102t and 40y/122h/104t | pano (−913.60, −233.36); resected (−915.14, −231.90), z 5.5–6.5; heading as given; local pitch +1.5 to +2.9° | NW outer eaves right of N, row 441.7 at columns 560–610 (40y view) | hidden by the drawbridge's beam | 24.5–24.8 (40y); 25.3–25.4 in the low-resolution 55y view | 25.1–25.4 tangent |
| **SV 2014, NE rampart**: pano `81wq-3oJLh_ApLhniDADzg` (Sep 2014), on the north-east terreplein, about 30 m from the tower; view 45y/222h/110t | pano (−826.94, −253.84); resected (−823.7, −252.8) with N's radius 6.35 (OSM), or (−826.1, −253.0) with 5.9 (Möller); z 11.8–12.8; heading −2.7°, pitch −2.5 to −4.4° | NE outer eaves on outline edge 45→46, rows 414–418 at columns 200–400 | 24.0–24.45 | 23.1–24.3 | not seen |

The camera alternatives behind the ranges:

- **Photo 2022.** The bearings alone fit any focal length from about 950 to 1444 px, sliding the camera along its line of sight (y −210 to −176).
  - Only f 1444 px makes the cornice's curvature consistent: at f 950–1000 the front point reads 1.3 m lower than the silhouettes, at f 1444 px within 0.3–0.4 m. f 1444 px is also what pass 129's f 1925 px (portrait, same photographer and camera) becomes at this image's scale.
  - With f 950–1000 the front gives 23.9–24.7.
  - The roll is not determined by the eaves near N. The ranges above are for roll −1° to +2°. The range eaves beside W imply a roll of about +1.5° if they too are at 20.27.
- **SV bridge.** Heading as in the URL. The camera height changes the result by less than 0.1 m, and the pano position (pano or resected) by about 0.1 m.
- **SV rampart.** The close range makes this view sensitive to the camera position and to N's radius. The radius changes the result by 0.4 m. The pitch offset the fit needs (−2.5 to −4.4°) is larger than Street View's usual error, so this view carries the least weight.

**Preferred readings** (mean of the front range, or of the tangent range where the front is hidden): photo 24.70, bridge 24.65, rampart 24.23. Their mean is **z 24.53** (median 24.65, spread 0.48 m). In terms of the range eaves beside the tower, the views put the tower's eaves **4.0–4.4 m higher**; Möller 1885 says 4.01 m.

The earlier Street View captures of passes 82–140 do not show the north tower; none were reused.

## Decision

| Pair | Difference |
|---|---|
| Möller 1885 – views (mean) | **0.25 m** |
| Möller 1882 – Möller 1885 | 1.65 m |
| Möller 1882 – views (mean) | 1.90 m |

Möller 1885 and the views agree within 0.3 m. Möller 1882 is 1.65–1.9 m below both, and below pass 27 too. Its tower line may be a different line from the one the copper starts at today, for example the pre-1885 roof's eaves; the section is internally consistent for Kungsmaket's room, which is why pass 137 trusted it.

The wall top is set to Möller 1885's written dimension on the model's range eaves: **z 24.28**. The views' mean (24.53) is not used as the value because their scatter (0.48 m) is larger than the difference. Möller's own 1882 range eaves (20.51) would give 24.52, which the views would fit equally well.

### What moves

- **Moved with z1:** pass 27's wall cylinder now runs to z 24.28. The cornice (r + 0.24, z1 − 0.55 to z1), the corbel row (r + 0.12, z1 − 0.95 to z1 − 0.55) and the 26 small openings (z1 − 1.35) move up 1.01 m. So does pass 132's whole cap: soffit, bell, ribs, drum, pilasters, neck, onion, ball, rod, fleur, vane and tip. N's tip rises from z 42.4 to 43.4 m above the water.
- **Unchanged:** the windows (pass 27's offsets from the base, pass 126's turned main window), Kungsmaket's door cut (pass 125), and W, S, E and Kuretornet.
- **The collar (`collar141`).** Pass 127 cut the range roofs 0.15 m inside pass 27's bell (`prepare_block127.py`, `Rz`).
  - Between the old wall top (z 23.27) and about 0.5 m above it, that bell is wider than the wall, so where a roof's cut edge lies in this band it stops up to 0.30 m short of the raised wall, an open slot under the corbel row.
  - `CUTV141` lists the vertices of `SM_Kalmar_Slott` round N with z 23.22–23.87 and 0–0.45 m outside the wall (56 vertices). They are binned every 2.5° of azimuth, with one bin added on each side.
  - In each such bin the collar adds a solid band of tower render. It runs from 0.30 m under the lowest edge vertex up to z 23.87, out to pass 27's bell less 0.05 m (r + 0.40 below z 23.27), and back into the wall to r − 0.30.
  - This gives two runs of 6 bins (15°), where the NW and NE roofs meet the tower. The roofs' cut edges end 0.10 m inside the collar, as they end inside the bells elsewhere.
  - Pass 132's `bulge132` now uses a freshly built tree of the present roofs (`under_roof141`). It bulges the same 21 vertex positions on N as before.

## Verification

- **Prepare.** `prepare_block141.py` prints `BLOCK141_PREPARE_OK`. It asserts that Möller 1885 is 24.28 on the range eaves, that Möller 1885 and the views' mean agree within 0.30 m, that Möller 1882 is over 1.0 m from both, and that the new value lies in 24.0–24.6.
- **Sandbox:** see below (`SCR/p141/build_block141_check.py`, logs `SCR/p141/log_r*.txt`).

Sandbox runs: three runs with `SCR/p141/build_block141_check.py` through `SCR/sandbox.py` (logs `SCR/p141/log_r1.txt`–`log_r3.txt`). The check renders the views, builds twice, runs the checks and renders again.
- **r1:** prelude 139, first collar.
- **r2:** prelude 140, adds the slot test; the slot test showed that r1's collar (driven by roof heights cast from above) covered only 6 cut-edge vertices more than no collar at all.
- **r3:** prelude 140, the final files, with the collar driven by the cut-edge vertices. All numbers below are r3's, and `SANDBOX_DONE prelude 140` was printed.

**Change set and repeatability:**
- `CHANGED141 ['SM_Kalmar_Slott_Towers']`; no other mesh in the scene changes.
- `REPEAT141 True`; the second run changes nothing.

**Mesh:**
- 241,304 faces (pass 132: 241,030), 127,011 vertices.
- `drop_degenerate_faces141` removes 0 faces. Pass 125's door cut removes 4 faces again (2 dropped).
- Materials unchanged (pass 27's set plus glass, paint and stone).

**Heights** (vertices within 1 m of each axis; cornice ring at r + 0.20–0.26):

| Tower | Top, before → after | Cornice top, before → after |
|---|---|---|
| N | 41.08 → 42.09 | 23.55 → 24.28 (the old cornice top includes the corbel; the wall top was 23.27) |
| S, W, E | unchanged (41.52, 43.25, 44.12) | unchanged |

The tops are the rod's tip in model z (water −1.33), so 42.09 is 43.4 m above the water.

**Export frame check** (pass 132's wrapper: the export tail's preparation, the exporter's frame test, a test FBX export):
- 0 invalid loops;
- the export succeeded;
- the exporter's fallback covers 215 loops (pass 132: 214).

**Roof joints:**
- `JOINT141`: pass 132's test, with the ray now started 1.5 m outside pass 27's bell so that it cannot start inside the new copper. It must meet the towers mesh before the roof's cut edge.
  - N: 0 gaps in 43 azimuths under a roof (roof z 24.21–25.57).
  - S: 1 of 2; W: 0 of 11; E: 1 of 22. These are pass 132's two known ridge-apex azimuths (z 25.33 and 25.47); those towers are unchanged.
  - This test only finds the topmost roof surface at each azimuth, so it does not see the band between the old and the new wall top. The slot test does.
- `SLOT141`: every `SM_Kalmar_Slott` vertex between the old and the new wall top and 0–0.45 m outside N's wall (58 vertices). An outward horizontal ray from each must meet the towers mesh within 0.35 m.
  - **With the collar: 44 covered.** Of the 14 left:
    - 2 at z 23.27, 0.025 m outside the wall, lie 0.38 m inside the collar's face, beyond the test ray's 0.35 m. They are covered.
    - 12 at z 24.08–24.12, 0.38–0.42 m outside the wall, are not cut-edge vertices: at that height pass 127's cut lies inside the wall. They are roof pieces standing under the new bell's eaves (the bell's base is r + 0.50 at z 24.28) and were outside the old bell too.
  - **Calibration:** the same test on a build without the collar (run at the end of r3) gives 10 covered and 48 uncovered. The test catches the slots, and the collar closes 34 of them.
- `CLASH141` (castle vertices more than 0.25 m inside a bell, N measured from the new eaves): 0 for every tower. On N, 202 castle vertices are in the bell's zone, at most 0.19 m deep (the roofs' cut edges).
- `WALLBAND141`: 119 castle vertices lie within r + 0.45 between the old and the new wall top: 61 inside the wall (hidden, as the roofs run into the wall below) and 58 just outside it (the cut edges above).

**Kungsmaket (pass 125):**
- `INSIDE_N141`: `SM_Castle125_Kungsmaket` has 23,742 vertices inside N's cylinder, at z 10.17–15.27, 9.01 m under the new wall top.
- `TOWERS_IN_N_ROOM141`: no vertex of the towers mesh inside the tower's room space (more than 1.6 m inside the wall, z 10–20).

**Walk checks** (pass 126/131's, verbatim from pass 137's wrapper):

| Route | Samples | Missing | Largest step | Obstructions | Low headroom | Height |
|---|---|---|---|---|---|---|
| Pass 126: courtyard → portal E → Kungstrappan → Gyllene salen → Kungsmaket | 330 | 0 | 0.167 | 0 | 0 | 5.47–10.47 |
| Gate passage B → C | 120 | 0 | 0.021 | 0 | – | 3.70–5.49 |
| Portal C → D / E / F | 35 / 42 / 187 | 0 | 0.012 | 0 | – | 5.47–5.48 |

`ROOFCLEAR131`: all interior vertices above z 15.5 stand under the castle roof (0 not under).

**Comparisons** (`SCR/p141/`, photograph or pano | before | after; renders from r3; Workbench, no shadows):

- **`cmp_sv_rampart.jpg`** (the NE rampart pano, camera 787). The clearest view. In the pano the tower's copper starts well above the NE range's ridge line. Before, the cornice stood at the ridge; after, it stands above it, as in the pano. The render's camera is about 1 m off: the range's front falls further left than in the pano.
- **`cmp_photo2022.jpg`** and **`cmp_photo2022_zoom.jpg`** (camera 785). After, the tower's eaves stand above the NW range's ridge by about as much as in the photograph; before, they were level with it.
  - The match is approximate: in the render the castle stands lower behind the rampart and is shifted left.
  - The model's bastion and rampart hide more of the castle than in the photograph. The camera height of 2 m is assumed, and the camera's distance depends on the focal length.
- **`cmp_sv_bridge92.jpg`, `cmp_sv_bridge103.jpg`, `cmp_sv_bridge122.jpg`** (camera 786): the bridge views; the drawbridge's beam covers the tower's front in the pano as in the render.
- **`cmp_jointNW.jpg`, `cmp_jointNE.jpg`, `cmp_jointNE_zoom.jpg`** (camera 788 and a view from the NE): the roofs against the raised wall. In the zoom the collar shows as a small render-coloured lip where the NE roof's slope meets the tower under the cornice; there is no open slot.
- Other views: `cmp_aerial.jpg`, `cmp_photo2022b.jpg` (the photograph's f 994 px camera).


The official build is done (see "Official build"); the Unreal checks are pending.

## Cameras

| Camera | Where | Compared with |
|---|---|---|
| `785_Block141_Cal_Photo2022_NorthTower` | (−898.89, −176.26), z 2.0, heading 140.3, pitch 9.2, vfov 52.97 | `castle27/swe-kalmar-slott-004.jpg`, resected |
| `786_Block141_Cal_SV2014_Bridge` | (−915.14, −231.90), z 6.0, heading 92, pitch 15.9, vfov 40 | Street View pano `iMd5WI6ugBpN7x-8vlt6pA`, 40y/92h/104t, resected (pitch locally fitted) |
| `787_Block141_Cal_SV2014_Rampart` | (−823.68, −252.79), z 12.3, heading 219.3, pitch 16.5, vfov 45 | Street View pano `81wq-3oJLh_ApLhniDADzg`, 45y/222h/110t, resected |
| `788_Block141_NorthTower_Joint` | (−872, −238), z 23, heading 129, pitch −8, vfov 40 | the roof joints at N from the north-west |
| `789_Block141_Aerial_NorthTower` | (−800, −200, 70) towards (−855.8, −262, 22), 35 mm | – |

## Limitations and open issues

1. **The views are not precise.** The individual readings run from 23.1 to 25.8 depending on the camera alternative and the point read; the preferred readings scatter by 0.48 m. They settle the question between the two Möller sheets (both 1882 and pass 27 are clearly too low), but not the value to better than about ±0.3 m.
2. **What would settle it better:** a photograph from a known position with the tower and the NW range square on (from the moat's north shore at about (−880, −185), heading 145, a long lens), or a measured elevation of the NW front. The 1882 section's tower line should also be re-read: if it is the old roof's eaves rather than today's copper line, the conflict disappears.
3. **W reads high in all three views** (24.1–25.4 against pass 27's 23.97), but the readings depend strongly on the roll in the photograph and disagree with each other. W was not changed. S and E were not seen side-on in any usable view, so they were not measured.
4. **N's radius.** OSM gives 6.35 m; Möller's sheet gives a wall of 39.7 fot (11.79 m, radius 5.89 m) at the eaves, and the tower is faceted (12 sides on Möller's plan, visible in all three views). The body is pass 27's round cylinder.
5. **The collar** is a modelling fix for a joint that pass 127's roof cut makes. A re-cut of the roofs against the new wall would be cleaner but would change `SM_Kalmar_Slott`, which this pass leaves alone.

## Sources

| Source | Licence | Used for |
|---|---|---|
| -wuppertaler 2022, `castle27/swe-kalmar-slott-004.jpg` | CC BY-SA 4.0 | the north tower against the NW range; camera 785 |
| Google Street View, panos `iMd5WI6ugBpN7x-8vlt6pA` and `81wq-3oJLh_ApLhniDADzg` (Sep 2014) | viewed only | the north tower against the NW and NE range eaves; cameras 786, 787 |
| C. Möller, "Calmar slott. Profiler", 1882 (PK006-00041), as read by pass 137 | public domain | the 1882 reading |
| C. Möller, "Ritning till nytt tak å norra tornet", 1885 (PK006-00049), as read by pass 137 | public domain | the 13.5 fot dimension; the new wall top |
| Passes 27, 127, 132 (`castle27.json`, `block132.json`, `prepare_block127.py`) | project | outline, towers, roof cut, caps |

No pixel of any photograph, panorama or drawing is used as a texture. No new material is added.

## Official build

The lead built pass 141 officially on 2026-10-04.
- **Checks:** the geometry check passed on the second rebuild (True), the FBX audit passed (exit 0), and the two rebuilds gave identical meshes.
- **Prevhash:** only intended changes. Pass 132's `SM_Kalmar_Slott_Towers` changed, and pass 140's 24 meshes are identical. The rest are known earlier corrections.
- **Dry renders:** cameras 785–789, 5 of 5.
