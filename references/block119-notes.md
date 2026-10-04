# Pass 119: Gamla stan, Stora and Lilla Dammgatan, Bremergatan, Smålandsgatan and Spikgatan

Pass 98 built the mainland houses as plain volumes inside three chunk meshes. Pass 119 is the fourth and last Gamla stan pass, after passes 116, 117 and 118. It takes out 22 houses, each now its own mesh `SM_Slott119_<osm id>` (category `Slottsområdet/Gamla stan`, `detail_pass` 119), standing on pass 98's ground height (model z 0.30), with its real form:

- storeys (1, 1.5, 2, 3 or 4) and the eaves and ridge heights;
- the roof: saddle, hip, Swedish mansard (gambrel, with gable ends) or a shallow hip, in red tile, dark tile, green sheet, dark or grey metal;
- the walls: vertical boarding (battens over the wall, white corner boards), render or brick in the house's colour, on a stone or granite plinth;
- eaves boards, white bargeboards on the gables;
- windows per storey (casement, surround, sill), gable windows on the steeper gables, a door on the wall that faces the street, steps where the door stands on the plinth;
- dormers, chimneys and the notable features in the table.

## Selection

The selection is computed in `scripts/prepare_block119.py` from the OSM street lines in `references/osm-slott98.json` (ways with `highway` and `name`). It takes every outline in `source/block98.json['buildings']` that lies within 25 m of Stora Dammgatan, Lilla Dammgatan, Bremergatan, Smålandsgatan or Spikgatan, and leaves out:

- the Stagnell chapel 500979084 (pass 107) and the ids of passes 115, 116 and 117 (read from `source/block115.json` … `block117.json`) and pass 118 (`source/block118.json`, when present);
- every outline that pass 118's rule takes (within 25 m of Kungsgatan, Söderportsgatan, Klostergatan or Skansgatan, unless pass 117's rule takes it). This removes the 15 houses on Stora and Lilla Dammgatan near the Kungsgatan corner (93238230, 93238237, 93238258, 93238265, 93238271, 93238276, 93238289, 93291960, 93291974, 93291980, 93291986, 93291987, 93291990, 93291994, 93291997); they all are in pass 118's ids.

Of the 48 outlines within 25 m of the five streets, 11 belong to passes 116 and 117 and 15 to pass 118, which leaves 22, not the "about 31" of the brief.

The 22 ids: 93238199, 93238223, 93238233, 93238263, 93238280, 93291981, 93292001, 93292003, 93292007, 93309086, 93309102, 93325640, 93325641, 93325643, 93325644, 93329943, 93329979, 93333624, 93333632, 93333650, 93453479, 93453484.

**Chunks.** The houses lie in all three of pass 98's chunks: eight at the west end of Stora Dammgatan in W (x < −1150), twelve in M (−1150..−850), and the two on Smålandsgatan and Spikgatan in E (x ≥ −850). The build adds the ids to `SLOTT98_DETAILED`, which keeps the ids of every earlier pass in the chain, and calls pass 115's `slott98_chunks115({'W','M','E'}, 119, block119_names)`. The three chunks are re-created by pass 98's code without these houses, keep `detail_pass` 98 and get `rebuilt_by_pass` 119. They are among this pass's meshes (25 names in all).

## Zones

Pass 116's slab method, copied into the prepare script:

- An outline that fills 85 % of its box in the frame of its longest edge is one zone; otherwise it is cut into slabs at its vertices and merged into a main body and wings, or one-storey annexes when under 12 m² or narrower than 2.6 m.
- The two annexes of the large buildings (93325640, 93325643) keep the full height under a flat roof (`annex_spec`), so they do not read as holes in the block.
- Each zone's walls follow the OSM outline exactly; walls against a neighbouring zone start at the neighbour's eaves.
- The street wall (for the door) is the outer wall that faces the nearest of the five streets within 30 m; only when none is faced, the nearest other named street (Sankta Britas gata for 93329943 and 93329979, the path "A" for two zone parts of 93453484).
- 93292003 has `gable_street`: its ridge runs across its street wall, so the gable stands on Stora Dammgatan as on sd05.

## Measurement

The photos were captured for the pass (`SCR/p119`, `captures.txt` lines starting `119|`): 12 views, 728 × 419, vertical field of view 90°, pitch +10°. Several panoramas snapped away from the requested points: sd05 lies at the west end of Stora Dammgatan (−1294.7, 142.3), sd06 at Ståthållaregatan (−1202.1, 212.9) and shows no house of this pass, and the sd02 and ld01 positions put the camera inside or against pass 118's houses.

- **Identities.** All OSM outlines within 70 m were projected into every view from the Google positions (`SCR/p119/ov119.py`, overlays `ov_*.png`; plans `plan.png`, `zB.png`, `zS.png`). Every photographed house in the table was matched this way.
- **Resection.** Where two outline corners are clear, the camera was found by a grid search within 8 m of the Google position that fits their bearings (`SCR/p119/m119.py`, `grid`); heights were then read on the plane of the named wall (`hit`). With two corners the fit is exact, so there is no residual to report.

| Panorama (view) | Google position (x, y) | Camera used (x, y), height | How | Used for |
|---|---|---|---|---|
| mBhO1yixfA4cv7cUlVSJMg (br01_h214) | (−892.5, 213.7) | Google, 1.56 above the house base | the projected street front of 93309086 (u 19–312) matches the photo (u 5–357 with the tower); the grid fit moved the camera 3.2 m into the street and gave a lower camera, so it was not used | Bremergatan 9 |
| mBhO1yixfA4cv7cUlVSJMg (br01_h34) | (−892.5, 213.7) | (−893.2, 212.2), 2.35 | two corners of 93333650's west wall | 93333650, 93333624 |
| Gyub0vxo9b30q4FMKRgCzw (br04_h213) | (−917.3, 265.3) | Google, read 2.98, taken as 2.7 | the boundary of 93325640/93325641 projects at u 221 against 245 in the photo (0.6 m along the wall) | Bremergatan 13 |
| vErj7BQDgfw9jyEIgZn9OA (sd04_h352) | (−1023.0, 134.8) | (−1023.2, 132.8), 2.34 | the two corners of 93292001's east gable | Stora Dammgatan 4 |
| 88r28WlFN9pJg1Aw6dmTIA (sd02_h339) | (−1082.1, 144.5) | Google, assumed 2.3 | none | 93291981 |
| TVbTceNVGs6htqujdqeyWw (ld01_h10) | (−1084.1, 171.3) | Google, about 2.0–2.4 from the base row | none | 93292007 |
| all other views | Google | Google, 2.3 | identification and storeys only | the rest |

### Houses

Heights are metres above the ground (model z 0.30). "Measured" means read with the cameras above; everything else is estimated from storeys, doors and windows and roof pitch by eye.

| OSM id | Identity | Photo | Storeys | Eaves / ridge | Roof | Walls | Measured or estimated |
|---|---|---|---|---|---|---|---|
| 93309086 | Bremergatan 9: white rendered Jugend villa; swept round-headed gable over the south end of the street front with three arched windows; arched dormer; square entrance tower at the north corner with cornice, two arched windows over the door and a green spire with a finial; red-brown window frames | br01_h214 | 1.5 | 4.5 / 8.2; street gable 5.0 / 9.0; tower 8.7, spire tip 14.2 | green sheet hip and cross gable | white render, 0.6 plinth | measured on the street front (Google camera, 1.56 above the house base): eaves 4.46, gable apex 9.0, tower cornice 8.7, spire base 9.8, tip 14.2, windows 1.4–3.9, dormer top 7.3. The garden stands about 0.7 m above the street behind the stone wall and fence; the model stands on the flat ground, so these heights are above the house base. The ridge 8.2 is estimated |
| 93325641 | Bremergatan 13: four-storey public building; granite plinth, cream rusticated ground floor with arched windows, cornice band, red-brick upper floors with cream pilaster strips between pairs of bays, cream window surrounds, sill bands, main cornice; green window frames | br04_h213 | 4 | 17.5 / 20.5 | dark shallow hip | brick over cream render | ground floor measured: plinth top 1.03, arched windows 2.4–4.7 (top of arch), ground-floor cornice 5.83, first-floor windows 6.6–8.8, second-floor band 10.6 above the pavement with a 2.98 m camera height; the camera height is not resected, and the values were scaled by 0.9 (to a 2.7 m camera): plinth 0.9, ground-floor cornice 5.3, band 9.5. The upper storeys, eaves and roof are estimated (three 4.1 m storeys over the ground floor) |
| 93325644 | north range of the same building along Bremergatan | not seen | 4 | 17.5 / 20.5 | dark shallow hip | as 93325641 | estimated (the same facade carried on) |
| 93325643 | courtyard wing of the same building | not seen | 3 | 11.0 / 13.0 | dark shallow hip | brick | estimated |
| 93325640 | pale yellow rendered four-storey corner range of the block, floor bands, cornice hoods over the upper windows | br01_h214 (behind the trees), br04_h213 (left edge) | 4 | 16.0 / 19.0 | red tile shallow hip | pale yellow render | estimated (storeys counted; the ground floor aligns with 93325641's) |
| 93333650 | grey-beige rendered two-storey villa, red tile hipped roof, roof window, chimney | br01_h34 | 2 | 5.2 / 10.0 | red tile hip | grey-beige render | eaves measured 5.17 (resected camera, height 2.35); ridge estimated from the roof's height in the photo (raised from 9.2 after the first sandbox run) |
| 93333624 | yellow boarded two-storey house with a mansard roof, the lunette in its gable, chimney | br01_h34 | 2 | 5.0 / 8.8 (break 7.3) | grey gambrel | yellow boards | eaves about 5.2 and break about 7.6, read obliquely with a camera that fits the neighbour; taken as 5.0 / 8.8 |
| 93309102 | yellow-brick one-and-a-half-storey house, dark tile roof, gable to the south | br03_h214 | 1.5 | 3.6 / 7.6 | dark tile saddle | yellow brick | estimated (the photo's house lies beyond the projected outline; the camera could not be resected) |
| 93333632 | house on Bremergatan's east side | not seen | 1.5 | 3.8 / 6.8 | red tile saddle | white boards | estimated (plain Gamla stan form) |
| 93292001 | Stora Dammgatan 4: red boarded two-storey house, white trim, the lunette in its east gable | sd04_h352 | 2 | 5.3 / 7.9 | red tile saddle | falu red boards | measured: eaves 5.2–5.4, apex 7.9, window sills 1.0 and 3.4, lunette sill 5.1 (resected, camera height 2.34) |
| 93291981 | long red boarded one-and-a-half-storey house with knee-wall windows, two chimneys, dark shutters | sd02_h339, ld01_h190 (edge) | 1.5 | 4.0 / 7.1 | red tile saddle | falu red boards | eaves 3.95–4.2 (Google camera, assumed 2.3); ridge estimated |
| 93292007 | yellow-brick three-storey 1950s apartment block, balconies, glazed stair bay with the entrance, chimneys, one dormer | ld01_h10, sd03_h340 (far) | 3 | 9.0 / 11.0 | dark low saddle | yellow brick | eaves 8.5–9.4 above the base row (Google camera); ridge estimated |
| 93292003 | white rendered two-storey house, gable and balcony on Stora Dammgatan | sd05_h332 (21 m) | 2 | 5.8 / 7.8 | red tile low saddle | white render | estimated |
| 93238223 | long white rendered two-storey house with a low saddle roof | sd05_h332 (35 m, its west part) | 2 | 5.8 / 7.6 | red tile saddle | white render | estimated; the photo shows an ochre part at its east end that is not modelled |
| 93238263, 93238280 | the two houses on the north side of Stora Dammgatan's west end | not seen | 1.5 | 3.8 / 6.6 | red tile saddle | red boards, yellow boards | estimated (plain Gamla stan form) |
| 93238199, 93238233 | white boarded cottage (L outline) and a small red shed | not seen | 1 | 3.0 / 5.2; 2.4 / 3.8 | red tile saddle | white, red boards | estimated |
| 93329943, 93329979 | pale yellow boarded house and red outbuilding at the west end | not seen | 1.5 / 1 | 3.8 / 6.8; 2.8 / 4.6 | red tile saddle | pale yellow, red boards | estimated |
| 93453479 | Smålandsgatan: beige rendered three-storey 1940s apartment block, balconies, chimneys | not seen | 3 | 9.6 / 12.6 | red tile saddle | beige render | estimated (60 × 13.6 m outline; a plausible 1940s block) |
| 93453484 | Spikgatan: small white boarded house | not seen | 1.5 | 3.6 / 6.4 | red tile saddle | white boards | estimated |

Colours are read by eye from the photos and set as flat targets on the town textures.

## Estimated

- Every value marked estimated above, and all ridge heights except 93292001's.
- The ridge direction of the houses not seen; the default is along the long side of the main rectangle.
- Window counts: regular bays (2.7 m on two-storey houses, 2.9 m on one-storey ones, 3.0 m on the public building, 2.3 m on the villa's front). The upper-floor windows of 93325641 and the arched ground-floor windows were checked against br04_h213 only for their heights and approximate spacing.
- Doors: one per house, on the street wall; the position along the wall is a rule. Bremergatan 13's door, placed in its main zone's street wall, is not seen in the photo.
- Chimney places, balcony sizes (2.8 × 1.2 m) and positions, the stair bay's width, the villa tower's plan (3.0 m square, 0.25 m past the north end and 0.30 m in front of the street wall).
- The eleven houses not seen in any photo.

## Verification

- **Zones** (`previews/block119-zones.json`): 35 zones cover the 22 outlines, 5413.5 m² of 5414.0.
  - 0.01 m² lies outside OSM and 0.42 m² of OSM is not zoned (slivers at the cuts).
  - The overlap is 0.216 m² (the OSM outlines themselves overlap by 0.225 m²).
  - Status: passed.
- **Sandbox** (prelude `rebuild_block117`):
  - Run 1 printed `BLOCK119_GEOMETRY 25` and `SANDBOX_DONE`. Degenerate faces dropped per house mesh: 0–427 (most on the two public-building meshes, from the thin rustication grooves and pilaster ends; none of the dropped faces is visible in the renders).
  - Run 2 (after the fixes below) ran the build twice in one session and printed `BLOCK119_GEOMETRY 25` both times and `SANDBOX_DONE`. Degenerate faces dropped across the 22 house meshes: 1,334 per build.
- **Comparison** with the photos (side by side in `SCR/p119/sb1/cmp_*.png` and `sb2/cmp_*.png`), rendered at the photo size from the cameras above:
  - Bremergatan 9: the tower with its cornice, arched windows and green spire, the green hipped roof, the dormer and the white front with red-brown windows match in place and size. Run 1 drew the swept gable as a half ellipse far larger than the gable; run 2 swells it above the rakes with a sheet fill.
  - Bremergatan 13: the granite plinth, the cream ground floor with its arched windows and grooves, the cornice band, the brick upper floors with cream pilasters and window surrounds, and the pale yellow range on the left match; the brick read too saturated in run 1 and was muted.
  - Stora Dammgatan 4: the red two-storey gable with the lunette, the eaves and the windows match.
  - 93292007: three storeys, the balconies, the stair bay and the dark roof match; the yellow brick read too dark in run 1 and was lightened.
  - 93333650: the eaves match; the roof was too low in run 1 (ridge raised to 10.0).
  - 93292003 and 93238223 (sd05): the white gable on the street and the long white house match.
  - 93309102 and 93333624: form and colours match, but the houses sit off their photo positions because these cameras are not resected.
  - sd02_h339 puts the camera inside pass 118's house volume (93291990/93291994 in the chunk), so 93291981 was not compared.
- **Repeatability**, run in the sandbox through a wrapper that executes the build twice in one session (`SCR/p119/build_block119_twice.py`): both runs give the same 25 meshes with the same vertex counts (5,693,149 in all, chunks included), 22 `SM_Slott119_` objects and three `SM_Slott98_Buildings_` chunks (`REPEAT119 True`).
- **Export frame check** (after the first official build failed with `SM_Slott119_93292001: no UV-derived frame for loop 97914`):
  - Reproduced in the sandbox (prelude `rebuild_block118`) with `SCR/p119/build_block119_check.py`. The wrapper runs the build, then the export tail's preparation from `rebuild_polish15.py` (triangulate, drop triangles under 1e-7 m², the UV reprojection). Then it applies `district_tangent_export`'s frame test to every pass 119 mesh.
  - The failing loop was 97914 of 93292001, the same index. It belongs to a glass triangle of the lunette in the east gable, at z 7.30: an n-gon half disc whose triangulation left a sliver along the straight sill. That sliver had two corners within 0.01 mm of each other, an area of 2.4e-6 m² (above the tail's 1e-7 cut) and no UV frame.
  - Fix: `lunette119` now builds the glass as a fan of triangles from the sill's midpoint (each about 0.023 m²), so no n-gon is triangulated. `drop_degenerate_faces119` is unchanged.
  - Result: 0 loops without a frame on all 25 meshes (22 houses and the W, M, E chunks), and `export_district_fbx` succeeded for all 25 to a temporary file under `SCR/p119`, deleted after each mesh. The lunettes still render glazed (`SCR/p119/chk2/lun.png`).
- **Pending:** the official build, its two-rebuild repeatability check and the export, which only the official build covers, and the Unreal checks. The lead fills in the build results.

## Limitations

- Only seven houses have measured heights; the rest are estimated from storeys. Roof pitches are mostly estimated.
- Bremergatan 9 stands about 0.7 m above the street on its garden terrace; the model has no terrace, stone wall or fence, and its heights are taken above the house base.
- Bremergatan 13: only the ground floor and the first band were read; the camera height is not resected (scaled by 0.9). The roof form and material are not seen. 93325643 and 93325644 are assumed to carry the same brick style.
- The houses are boxes on the OSM outline with rectangular roofs; small notches in an outline are covered by the roof.
- Window and door positions are regular bays, not the real ones.
- No fences, garden walls, garages or sheds outside the OSM outlines are modelled (the green picket fence of no. 9, the yellow-brick garden wall at no. 4, the carport beside 93333624).
- Extra views that would help, given as location (x, y), Street View heading and pitch:
  - the west end houses 93238263/93238280/93238199 from (−1220, 132), heading 340, pitch 10;
  - 93291981's street front from (−1062, 140), heading 300, pitch 10;
  - Bremergatan 13's full height from across the crossing at (−900, 245), heading 230, pitch 25;
  - Smålandsgatan 93453479 from (−690, 285), heading 180, pitch 10.

## Official build

The first official build failed at the FBX export: `SM_Slott119_93292001: no UV-derived frame for loop 97914`. The cause was a sliver in the lunette glass, fixed as described under "Export frame check". The second build passed the Blender geometry checks and the FBX export, and two rebuilds gave identical meshes. Prevhash reports the mainland chunks SM_Slott98_Buildings_W, _M and _E (in their earlier versions) as changed. That is intended, because they are re-created without this pass's 22 houses. The other changes are the earlier intended corrections. The Unreal import and its checks are deferred.
