# Pass 117: Gamla stan, west Västerlånggatan, Gamla Kungsgatan and Paters gränd

Pass 98 built the mainland houses as plain volumes inside three chunk meshes. Pass 117 is the second Gamla stan pass after pass 116. It takes out 40 houses, each now its own mesh `SM_Slott117_<osm id>` (category `Slottsområdet/Gamla stan`, `detail_pass` 117). They stand on pass 98's ground height (model z 0.30), and all heights below are metres above that ground.

**Selection.** The pass takes every building in `source/block98.json['buildings']` that meets one of these conditions:

- within 25 m of Västerlånggatan with its centroid at x ≤ −930;
- within 25 m of Gamla Kungsgatan;
- within 25 m of Paters gränd.

The street lines are the OSM ways in `references/osm-slott98.json`. The selection leaves out:

- pass 115's fourteen ids;
- the Stagnell chapel 500979084 (pass 107);
- pass 116's houses (within 25 m of Molinsgatan, or within 25 m of Västerlånggatan with centroid x > −930).

The 40 ids are listed in the table below and in `source/block117.json['ids']`.

**Chunk.** All 40 centroids lie between x −1150 and −850. The pass adds its ids to `SLOTT98_DETAILED`, which keeps the ids of every earlier pass in the chain, including pass 116's when the chain runs it first. It then calls pass 115's `slott98_chunks115({'M'}, 117, block117_names)`. `SM_Slott98_Buildings_M` is re-created by pass 98's code without these houses, keeps `detail_pass` 98 and gets `rebuilt_by_pass` 117. Chunks W and E are not touched.

**Zones** (`scripts/prepare_block117.py`). The zones use pass 116's slab method, copied into the script:

- Each outline is framed on its longest edge and cut into rectangles.
- The largest rectangle is the main body; the others are wings or one-storey annexes.
- The walls run on the real outline. A wall against a neighbour starts at the neighbour's eaves: the spec eaves for houses of this pass, pass 98's height for the rest.
- Each house has a spec: wall colour, boarded or rendered, storeys, eaves, ridge, roof kind and material, and the ridge direction relative to its street wall (`par` or `perp`).
- The street wall is the outer wall that faces the nearest of the three streets. Two overrides apply:
  - Västerlånggatan 25 (93292707) and 93292657 are forced to Västerlånggatan.
  - The two stone houses 93292700 and 93292694 have their front fixed to their south-west outline edge (`FRONT117` in the build). This is the facade seen in k02_h14 and k01_h30.

**Build** (`scripts/build_block117.py`).

- **Boarded houses:** vertical boards (pass 81's `boards81`), corner boards, an eaves board, a stone plinth and white cased windows (pass 81's `cas81`) by storey and bay.
- **Rendered houses:** a cornice and frame surrounds instead of boards.
- **Roofs:**
  - saddle: pass 115's `saddle115`, with bargeboards;
  - hip: `inset_roof`;
  - gambrel: a new `gambrel117` with a steep lower slope, a break and five-sided gable walls;
  - mansard: a hipped two-stage roof, as in pass 115.
- **Gable windows** sit on the gable slab, 0.24 m proud, because that slab has no hole.
- **Other features:**
  - dormers: pass 82's `dormer82`;
  - street gables: pass 83's `frontis83`;
  - chimneys, skylights, shutters and lunettes;
  - the curved central gable of Gamla Kungsgatan 10;
  - rustication and cellar windows;
  - the pediment and pilasters of 93292700;
  - the balcony of 93292670.
- **Doors:** one per house, on the street wall unless the photo shows none there. The houses with a door on the back are 93292674, 93292684, 93292699, 93292707, 93292700 and 93292671.
- **Materials** are `M_Block117_*`, with the setup loop of pass 82/115 (flat colour targets on the town textures).
- `drop_degenerate_faces117` (with the `_thin` test) runs right after `s21_finish` on every mesh, including the re-created chunk.

## The houses

"Photo" is the capture the form and colour are read from. Values are eaves / ridge (or break, top) in metres above the ground. An "est." in the photo column means the house is not seen, and its form is a plausible Gamla stan form with the colour taken from its neighbours.

| OSM id | Identity | Photo | Values (eaves / ridge) | Roof |
|---|---|---|---|---|
| 93292658 | beige rendered villa with a street gable | w01_h106 (37 m, far) | 4.8 / 8.8 est. | red tile saddle, two chimneys |
| 93292678 | yellow rendered 1½-storey villa, gable to the street, shutters, red dormers | w01_h106, w02_h108 | 4.0 / 8.6 est. | red tile saddle across the street |
| 93292704 | red boarded 1½-storey house with the street gable (frontispiece) | w02_h108 | 3.6 / 7.4 est. | red tile saddle, chimney |
| 93292681 | small red outbuilding | est. | 2.5 / 4.0 | tile saddle |
| 93292660 | pale yellow boarded two-storey house, white trim, glazed door | w03_h119 | 5.4 / 7.9 est.; windows 0.9 and 3.3 | tile saddle, chimney |
| 93292686 | red boarded cottage | w03_h119 | 2.8 / 5.0 est. | tile saddle, gable to the street |
| 93292708 | red boarded cottage | w04_h119 | 2.8 / 4.9 est. | tile saddle, chimney |
| 93292684 | narrow pale yellow boarded gable house, two low storeys | w04_h119 | **4.0 / 5.7** measured | tile saddle, gable to the street, gable window |
| 93292674 | tall red boarded gable house, black corner boards, storey bands and window surrounds | w04_h119, w05_h123 | **7.0 / 10.2** measured | tile saddle, gable to the street, attic window, red dormers on the long sides |
| 93292657 | red boarded house behind 93292674 | est. | 4.0 / 7.4 | tile saddle |
| 93292707 | Västerlånggatan 25, long red boarded corner house, tall windows and knee-wall windows | w05_h123 | **4.2 / 6.9** measured | red tile hip, chimney |
| 93292675 | white boarded garage with black doors | w06_h126 | 2.6 / 3.1 est. | low grey metal saddle |
| 93292665 | grey boarded 1½-storey house under a big red tile roof | w06_h126, w07_h134 | 3.4 / 7.8 (eaves about 3.2 read on the Google camera) | tile saddle, gable east, two skylights, two chimneys |
| 93292699 | long red boarded house with green shutters | w07_h134, w08_h121 | 3.2 / break 5.0 / 6.2 (Google camera, see below) | red tile gambrel, chimney |
| 93292693 | pale yellow boarded house under a gambrel roof, gable to the street | w08_h121, v09_h121 (pass 116) | 3.6 / break 6.0 / 7.6 est. | tile gambrel, dormer, chimney, gable windows |
| 93306348 | pale yellow boarded cottage (behind) | v09_h121, partly | 3.0 / 5.4 est. | tile saddle |
| 93306357 | sage-green boarded two-storey gable house with the lunette | v09_h121 (pass 116) | 5.6 / 8.6 est. | grey metal saddle, gable to the street |
| 93306344 | white boarded house under a gambrel roof | v09_h121 (pass 116) | 3.2 / 5.4 / 6.6 est. | tile gambrel |
| 149905962 | red boarded outbuilding by the field | w01_h286, w02_h288 (far) | 2.6 / 4.6 est. | tile saddle |
| 93309098 | white rendered house, red tile hip, dormer | w08_h301, v09_h301 (pass 116) | 4.2 / 8.6 est. | tile hip, dormer, chimney |
| 93292705 | Gamla Kungsgatan 9, olive-green boarded house, white frames | k01_h210 | 3.8 / 6.6 est. | tile saddle |
| 93292703 | yellow rendered two-storey house | k01_h210, k02_h194 | 6.0 / 8.8 est. | tile saddle |
| 93292694 | Gamla Kungsgatan 10, ochre rendered, rusticated ground floor, string course, wooden double door, cellar windows, curved central gable | k01_h30, k02_h14 | **7.2 / break 9.6 / 10.6**; string course 4.4 measured; break and top est. | slate mansard, slate dormers |
| 93292700 | salmon rendered two-storey house, pilasters, pediment with lunette in the middle, cellar windows | k02_h14 | **8.0 / 11.6**; pediment apex 9.9 measured | red tile hip, red dormers, chimney |
| 93292676, 93292698 | ochre rendered two-storey houses at the end of Paters gränd | k02_h194 (far) | 6.0 / 9.4 est. | tile hip |
| 93292670 | light brick 1½-storey house, balcony on the gable to Paters gränd | k02_h194 | 4.0 / 7.6 est. | tile saddle |
| 93292661 | yellow boarded house | est. | 3.8 / 7.0 | tile saddle |
| 93292662 | small red outbuilding | est. | 2.5 / 4.0 | tile saddle |
| 93292663 | red boarded house | est. | 3.8 / 7.0 | tile saddle |
| 93292664 | white boarded cottage | est. | 3.0 / 5.4 | tile saddle |
| 93292659 | pale yellow boarded cottage | est. | 3.0 / 5.4 | tile saddle |
| 93292668 | yellow boarded cottage | est. | 3.0 / 5.2 | tile saddle |
| 93292697 | white boarded cottage with shutters and a brick chimney | k04_h9 | 2.9 / 5.2 est. | tile saddle |
| 93292671 | red boarded low house, east end of Gamla Kungsgatan | k04_h9 | 2.7 / 4.8 est. | tile saddle |
| 93292687 | grey boarded cottage | est. | 3.0 / 5.4 | tile saddle |
| 93292692 | small white shed with a dark roof | k03_h189, edge | 2.3 / 3.4 est. | grey saddle |
| 93292669 | white boarded cottage behind the hedge | k03_h189, edge | 3.0 / 5.0 est. | grey saddle |
| 93292695 | small yellow outbuilding | est. | 2.5 / 4.0 | tile saddle |
| 93292691 | red boarded cottage | est. | 2.9 / 5.0 | tile saddle |

## Measurement

The photos were captured for the pass: `SCR/p117`, the `captures.txt` lines starting `117|`. Pass 116's v09_h121 and v09_h301 were used for the east end. The images are 728 × 419 with a 90° vertical field.

**Identities.** For each view, the pass-98 outlines were projected from the pano position: their bearing ranges, distances and an outline overlay (`SCR/p117/w/ov_*.png`, `vis.py`, `plan_*.png`).

- 93292694 and 93292700 share a wall (vertex (−1020.8, 44.1)). The "cream mansard house with the curved gable" of k02_h14 is the long south-west front of 93292694 seen obliquely. The same front, seen close, is the ochre "no. 10" of k01_h30. The pass therefore models one house with the curved gable as a central gable over the door.
- k04_h9: the pano sits on the outline of 93292671. From the street layout, the white cottage is taken as 93292697 and the red low house, with the street sign on its east end, as 93292671. This is not resected.
- k03_h189: the yellow house with the veranda is 93292701, which is not in this pass.

**Resection.** Corners were resected from the OSM outline vertices with base rows (`SCR/p100/res.py` with vfov 90). The camera height was read from the base rows. Heights were read on the wall plane with `hit.py`. Ridges were read on a plane moved in by half the depth.

| View | Google position (x, y) | Resected (x, y), height | Used for | Readings |
|---|---|---|---|---|
| w04_h119 (AVPT4UiX…) | (−1075.9, 56.3) | (−1076.85, 55.19), 2.3–2.5 m (four corners, residual up to 23 px); a second solution on 93292674's corners alone gives (−1078.1, 55.4) and reads 1 m higher | 93292674, 93292684 | 93292674 eaves 6.8–7.4, apex 9.6–10.4, windows 1.1–2.8, 4.1–5.7, gable window 6.8–8.3; 93292684 eaves 4.0, apex 5.6–5.7, windows 0.7–1.5 and 2.6–3.6 |
| w05_h123 (YfKlWimL…) | (−1051.1, 70.8) | (−1051.96, 69.91), 2.56 m (two corners) | 93292707 | eaves 4.2–4.5, ridge 6.9, chimney top 7.4, windows 0.6–2.2 and 3.2–3.9 |
| k02_h14 (5lm5eOTh…) | (−1020.6, 33.4) | (−1021.62, 31.52), 2.2 m (two corners) | 93292700, 93292694 | 93292700 cornice 7.9–8.3, pediment apex 9.9, middle 5.2 m between s 4.3 and 9.5 of 15.5, windows 1.8–3.6 and 4.7–6.9, plinth 0.7, dormer top 10.7; 93292694 string course 4.4, eaves 7.3, curved gable top 10.3 |
| w07_h134 (Qbatg-EI…) | (−994.7, 95.7) | not resected (Google camera, height 2.4) | 93292699, 93292665 | 93292699 eaves 3.0, gambrel break 5.2, ridge 6.3; the base reads −0.3 to −0.65, so the values are uncertain by about ±0.4; 93292665 eaves about 3.2 |

All other values are estimated from storeys, doors and windows against the measured houses. The wall and roof colours were read by eye and set as flat targets.

## Estimated

- Every value marked "est." in the table, and every house marked "est." in the photo column. These have a plausible Gamla stan form: boarded, one to one-and-a-half storeys, a tile saddle roof, and a colour taken from their neighbours.
- Ridge directions of the unseen houses: along the street, or along the long side.
- Window counts on sides not seen: bays at about 2.8 m. Gable windows: one or two by gable size.
- Dormer, chimney and skylight positions, except where the photos show their number.
- The mansard break and top of 93292694, and the hip of 93292700 (only its front is seen).
- Door positions on unseen sides.

## Verification

- **Zones** (`previews/block117-zones.json`): status passed.
  - There are 46 zones (40 main, 5 wings, 1 annex) for 40 outlines, 3795.0 m² in all.
  - 0.0 m² lies outside OSM and 0.08 m² of OSM is not zoned.
  - The overlap is 0.001 m², equal to the overlap of the OSM outlines themselves.
- **Sandbox** (prelude rebuild_block115), four runs:
  1. The first run printed `BLOCK117_GEOMETRY 41` (40 houses + chunk M) and `SANDBOX_DONE`. The comparison showed two problems: gable windows hidden inside the gable slab, and features of the main bodies placed on the wrong side because a stale centre variable was used.
  2. Fixed the gable-window offset, the stone-house fronts and the doors.
  3. Fixed the centre variable. A projecting box over the middle of 93292700 hid its windows, so it was replaced by pilaster strips.
  4. The last run, in a wrapper (`SCR/p117/build_block117_twice.py`), runs the build twice in one session and compares every named mesh (vertex count, face count, coordinate checksum, detail_pass). The result is in the "Repeat run" line below.
- **Dropped degenerate faces** (final run): 0–40 per house, 741 in all. Which parts the dropped faces come from was not inspected.
- **Comparison images** are side by side, photo over render, at the photo size: `SCR/p117/sb4/cmp_*.png` (earlier runs in `sb1`–`sb3`).
  - **w04_h119:** the red gable house with its black bands, two windows per floor and the attic window, and the narrow yellow gable house beside it, match in eaves, apex and window rows. The red cottage to the right matches.
  - **w05_h123:** Västerlånggatan 25 matches in length, eaves, the hip ends and both window rows.
  - **v09_h121:** the sage gable house with its lunette and the white gambrel house match. 93292693 reads as the gambrel house in w08_h121. In v09_h121 its roof looks hipped from that angle; it stays a gambrel, which follows w08.
  - **k02_h14:** the salmon house has the pilasters, the pediment with the lunette, the dormers and the cellar windows. The camera stands about 2 m off (the yellow 93292703 fills the left edge), so the comparison view is shifted to (−1019.5, 30.5).
  - **k01_h30:** the rusticated ground floor, string course and double door are right. The OSM outline puts the wall about 2 m from the pano, against about 3 m in the photo, so the view is moved back 1.5 m.
  - **w01_h106, w08_h121:** the villa's street gable and the gambrel house's gable profile match in form. The w01 camera is not resected.
- The official build and the Unreal checks are pending; the lead fills in the build results.

Repeat run (final sandbox): `BLOCK117_REPEAT 41 41 differ []`. All 41 meshes (40 houses and chunk M) are identical between the two runs. Chunk M after the build has 1,487,715 vertices.

## Limitations

- Many of the houses behind the street fronts are not seen and are estimated.
- 93292699's gambrel (w07) reads as a nearly plain saddle from the street, because the lower slope is short.
- The k04_h9 and k01 views stand on or very close to the OSM outlines, so the outlines there are probably 1–3 m off the real walls. The houses keep the OSM outlines.
- Pass 116 runs in parallel. A house at the x −930 boundary belongs to this pass by the rule; 93306344, 93306348 and 93306357 (centroids −936.7 to −943.3) are this pass's.
- The curved gable of 93292694 is a symmetric S-curve with two windows and a round window. The real gable has more ornament.

## Official build

The lead's build of pass 117 passed the Blender geometry checks and the FBX export, and two rebuilds gave identical meshes. Prevhash reports the mainland chunk SM_Slott98_Buildings_M (in its pass 98, 107, 115 and 116 versions) as changed. That is intended, because the chunk is re-created without this pass's 40 houses. The other changes are the earlier intended corrections. The Unreal import and its checks are deferred.
