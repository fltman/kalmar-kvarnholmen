# Pass 114: correction of the round drum at 50 Larmgatan (886305409)

Pass 114 rebuilds one mesh, `SM_Kvarnholmen_House_886305409`, the round glass and panel office drum at 50 Larmgatan in front of the fire station. Pass 109 built it first, and this pass corrects it. The object is re-created unconditionally under the same name and category (`Kvarnholmen/Larmgatan`). It carries `detail_pass = 114` and `corrects_pass = 109`. No other mesh is touched.

What the pass builds (zone `d886`, `source/block114.json`):

- **Plan:** a regular 66-facet polygon on the circle fitted to the OSM ring. The centre is (−255.55, 302.39) and the radius 8.81 m. The 19 OSM vertices lie on that circle within 5 mm, so the ring is a mapped circle. One facet is one panel column, about 0.84 m wide. The panel plane stands on the OSM line (apothem 8.80 m).
- **Facade rows, bottom-up:** ten panel rows, giving three storeys of about 3.1 m, a short glass row under the top band, and the opaque top band.

  | Row | Height (m) | Kind |
  |---|---|---|
  | 1 | 0–0.73 | short mixed row |
  | 2 | 0.73–2.30 | tall glass |
  | 3 | 2.30–3.08 | opaque |
  | 4 | 3.08–3.83 | short |
  | 5 | 3.83–5.52 | tall glass |
  | 6 | 5.52–6.16 | opaque |
  | 7 | 6.16–6.85 | short |
  | 8 | 6.85–8.52 | tall glass |
  | 9 | 8.52–9.27 | short glass |
  | 10 | 9.27–10.08 | opaque top band |

  The coping runs to 10.2 m.
- **Chequer:** glass, dark grey and silver panels. The pattern is deterministic: the tall rows are mostly glass, the short rows are mixed, and the opaque rows alternate light and dark.
- **Frame:**
  - silver transoms at every row line;
  - a dark ledge on top of each tall glass row (at 2.30, 5.52 and 8.52 m);
  - a dark base strip;
  - the coping;
  - thin radial fins at all 66 panel joints, 0.30 m deep and 0.05 m thick, running the full height.
- **Entrance:** on the Larmgatan side (south-west, polar angle −158°). It is a light grey door leaf to 2.05 m under a dark transom to 2.30 m.
- **Roof and core:** a flat roof at 9.96 m inside the coping, and a dark core wall behind the panels that shows in the mullion gaps.

Panoramas are working references only. No pixel is used as a texture; all materials are flat tints on the town textures (`M_Block114_*`, plus the shared glass).

## What pass 109 got wrong, and what changed

| Pass 109 | Pass 114 |
|---|---|
| 19 flat facets (one per OSM vertex), each split into two very wide panels | 66 facets of about 0.84 m, one per panel column, so the drum reads as round |
| Four bands of 1.8–2.55 m tall panels; storeys and mullions far too tall | Ten measured rows: three storeys, each a short row, a tall glass row and an opaque spandrel, then a short glass row and the top band |
| Fins only at the 19 facet corners, set on the facet normal and protruding 0.5 m, which made them splay in a close view | 66 thin radial fins, 0.30 m deep, at every panel joint |
| Floor bands at 2.3, 5.1 and 8.1 m; top at 9.6 m | Row lines as in the table above; coping at 10.2 m |
| No entrance | Entrance on the Larmgatan side |
| Comparison camera at (−268.75, 308.41), 13.3 m from the centre. That is too close, and it made the drum look squat and too wide | Re-resected at (−269.11, 308.38), 14.8 m from the centre (see below) |

**The height.** The squat look in pass 109's comparison came mainly from that camera. Its resection was too close, so the render's drum was about 10 % too wide against the photo. The measured height changes only a little, from 9.6 to 10.2 m. **The photos do not support a drum much taller than about 10 m on the OSM circle:**
- the drum's height-to-radius ratio is fixed by angles alone, at about 1.04–1.07 from both panoramas;
- the OSM district height for this way is 9.75 m, which suggests three levels.

There are three storeys, not four. The "fourth glass storey" is the 0.75 m short glass row under the top band. See the scale caveat under Limitations.

## Measurement

Two Google Street View panoramas were used. The vertical field of view is 90°, and the bearing is the heading + 28.2°. The views are `SCR/p114/886305409_h25_p15.jpg` (700×375, compared after scaling to 756×405), `886305409_h86_p15.jpg` (756×405) and `886305409_h330_p12.jpg` (756×405, the same pano as h25).

**Resection.** Each camera was solved on the drum's two silhouette tangents, with the fin-tip radius taken as 9.10 m:
- the mean of the two tangent bearings gives the bearing to the centre;
- the half-angle between them gives the distance;
- the readings were taken on two image rows and averaged.

The camera height comes from the drum's base line at the front generator, on the panel plane at 8.80 m.

| Panorama | View | Google position (local) | Resected position | Distance to centre | Height |
|---|---|---|---|---|---|
| HsWLWKRmyL92sdlcqTcrww | 21 Larmgatan, h 25 / 330 | (−278.55, 290.29) | (−277.02, 292.22) | 23.76 m | 1.82 m |
| qzjtLjyN1xtmtmwQmPg9cg | 50 Larmgatan, h 86 | (−268.84, 309.19) | (−269.11, 308.38) | 14.82 m | 1.93 m |

- Tangent bearings: h25, 42.0–87.5° (row v 200) and 42.2–86.9° (v 230); h86, 75.6–152.3° (v 200) and 76.3–151.1° (v 300).
- The h330 view, from the same camera, was not used in the solve. The render puts the drum's left silhouette within about 2 px of the photo.

**Row lines.** These were read at the front generator in both views and scaled by each camera's front distance (6.02 m for h86, 14.96 m for h25). Values are listed as h86 / h25 in metres:

| Row line | h86 | h25 |
|---|---|---|
| Top of the ground glass (ledge) | 2.27 | 2.32 |
| Opaque spandrel top | 3.07 | 3.10 |
| Short row top | 3.79 | 3.88 |
| Second ledge | 5.52 | 5.53 |
| Spandrel top | 6.16 | — |
| Short row top | 6.87 | 6.83 |
| Third ledge | 8.48 | 8.56 |
| Short glass row top | 9.32 | 9.22 |
| Front top of the coping | 10.56 | 9.90 |

The model uses the averages. The top is taken as 10.2 m; the close view's 10.56 m is sensitive to small errors in its 6 m front distance.

**Other measurements:**
- **Panel columns:** about 27–30 px apart at the front in the close view, which is 0.80–0.85 m. That gives about 66–68 around, and 66 is used.
- **Entrance:** in the h25 view, a light grey door-width panel at u 375–389 under a dark transom. It hits the drum at a polar angle of −158° and is about 1 m wide. The leaf reads 1.9–2.0 m tall, and the model uses 2.05 m.
- **Pitch check:** the vertical vanishing point from the window column of the stone block (h86) agrees with 15°. In h25, a lamp post and a sign pole give 13.6° ± 1°, but poles can lean. 15° is used.

## Estimated

- The chequer, which is a regular deterministic pattern, not a cell-by-cell copy. The share of glass, dark and silver panels per row type was matched by eye.
- The panel count (66) to within about ±2.
- The fin depth (0.30 m) and thickness, and the ledge and coping projections.
- The roof (not visible): flat, with no plant or rooftop structures.
- The faces not seen (east and north-east), which repeat the pattern.

## Verification

- `prepare_block114.py` prints `BLOCK114_ZONES_OK`.
  - Footprint (OSM ring) 239.6 m², zoned 243.5 m², OSM not zoned 0.01 m², overlap 0.
  - Outside OSM 3.92 m². This is expected: the 19-vertex ring is inscribed in the circle, so its straight chords cut off slivers of the round building. The check bounds it below 6 m².
  - OSM vertex residuals from the fitted circle: −5 to +4 mm.
- Sandbox: two runs (`SCR/p114/sb1`, `sb2`) on the pass 111 prelude. Both ended in `SANDBOX_DONE` without errors and printed `BLOCK114_GEOMETRY 1`.
- `drop_degenerate_faces114`, with the `_thin` test, ran after `s21_finish` and dropped 0 faces.
- The aerial render (`SCR/p114/sb2/aer.png`) shows the flat roof closed inside the coping.
- Side-by-side comparisons at the photo size with the resected cameras (`SCR/p114/cmp_2_v25.jpg`, `cmp_2_v86.jpg`, `cmp_2_v330.jpg`):
  - the silhouette, base and top line up in all three views to within a few pixels (h86: photo 205–550 / top 32 / base 333; render 203–543 / 32 / 330);
  - the row rhythm, ledges, fins and top band match.
  - The visible differences are the glass colour (the shared glass renders darker than the sky-reflecting real glass), the exact chequer, lamps, signs and cars.
- **Pending:** the official build, the FBX export and the Unreal checks. The lead fills in the build results.

## Limitations

- **The scale.** The drum stands on the OSM circle (r 8.81). On that circle, both cameras come out at 1.8–1.9 m, which is below the usual 2.0–2.2 m. Some independent cues in the h25 view suggest a camera at 2.2–2.5 m:
  - a pedestrian;
  - parked cars;
  - the h86 bollards;
  - the door leaf, which reads only 1.9–2.0 m.

  If those cues are right, the whole drum is 10–15 % larger than OSM (radius about 10.0–10.4 m, height about 11 m). The views cannot settle this, because everything on the drum scales together. OSM was kept, as the brief requires. An orthophoto or cadastral diameter would settle it; a 17.6 m diameter would confirm this pass.
- The neighbour on the fire-station side is `SM_Kvarnholmen_House_91846968` (landmarks pass 14, "modern western wing"). It looks clearly wrong:
  - In both photos it is a stone-clad block of four storeys plus a set-back top floor with balconies, with large windows over brown panels and a low glazed pavilion jutting north towards the drum.
  - In the model it is a cream three-row generic wing at 10 m.
  - In the h25 view the real stone block and pavilion stand much closer to the camera than the OSM north face at y ≈ 280. The pavilion corner reads about 8 m north of it, at roughly (−262, 288). The model shows nothing there.

  This was not changed; it needs its own pass.
- Signs, the lamp post and the bollards are omitted.

## Official build

The lead's build of pass 114 passed the Blender geometry checks and the FBX export, and two rebuilds gave identical meshes. Besides the earlier intended corrections, prevhash reports pass 109's drum (886305409) as changed; that is this pass's correction. The Unreal import and its checks are deferred.

The neighbour SM_Kvarnholmen_House_91846968 (the fire station's modern western wing, built by landmarks pass 14) was seen to be clearly wrong in this pass's photos. It is queued for its own correction pass.
