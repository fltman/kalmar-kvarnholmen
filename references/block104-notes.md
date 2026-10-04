# Pass 104: Kaggensgatan at Fiskaregatan, Fiskaregatan north side, Strömgatan south side

Pass 104 replaces four generic district volumes from pass 17 with the houses on their photographed street fronts. All four OSM ways are large outlines that cover much more than the photographed houses. Each is split at the joints seen in the photos. The front houses are about 10–12.5 m deep. The unseen rest of each outline is kept low, plain and flat.

Kaggensgatan, west side (92204193, front facing local +x), south to north:
- **Cream boarded gable house** at the Fiskaregatan corner, y 146.4–157.05 (10.65 m). Its gable faces the street: eaves 5.56 m, apex 9.46 m. White corner boards, two white pilasters, three bays of white casements (ground 0.92–2.24, upper 3.80–5.06), a belt at 3.3 m and a small gable window (6.26–7.32).
- **White rendered link**, y 157.05–159.23. It has a black glazed door (0.25–2.05) and a white fascia. The upper storey has dark glazing behind a black railing, to 5.4 m. In reality the link is recessed about 1 m; the model keeps it flush (see Limitations).
- **Tan rendered two-storey house (Gardell)**, y 159.23–175.9. It has shop windows (0.65–2.30), a belt at 3.47 m, upper windows on a 2.46 m rhythm (3.95–5.30) and a cornice at 6.0 m. The steep black sheet roof (ridge 10.8 m, est.) carries six black box dormers.
- The rest of the outline is flat at 7.0 m (est.). It runs 66 m west along Fiskaregatan and covers the yard parts.

Kaggensgatan, east side (92379265, front facing local −x), south to north:
- **Yellow boarded gable house (Outnorth)** at the Fiskaregatan corner, y 146.5–155.2. Gable foot 5.25 m, apex 7.11 m, tiled roof. Three upper windows (3.45–4.65) under grey awnings, two shop windows under pale awnings, the dark sign board (2.75–3.27), a green glazed door on a step and a small gable window.
- **Low white boarded shop**, y 155.2–162.9, flat at 2.7 m. Its glazed gable front spans y 156.12–162.04 (eaves 2.68, apex 4.61). The gable has white mullions and diagonal braces and a short pale saddle roof running 6 m back. A diamond window, a white door and a low platform stand in front.
- **Grey boarded one-storey gable house**, y 162.9–170.3. Gable foot 2.81 m, apex 4.57 m, red tile. It has a big window (0.58–2.28) and a half-round fan light in the gable.
- The rest is flat at 6.0 m (est.).

Fiskaregatan, south side (92204176, front facing local +y):
- **Pale green stucco two-storey house**, x −150.1 to −141.9 (8.2 m). It has a shop window (1.32–3.12, 2.9 m wide), a brown door with a top light up steps (threshold 0.9 m, head 3.57), a window, and four upper windows (4.98–6.83). Two string courses sit at 3.7–4.2 m and the cornice at 7.57 m. The low grey saddle roof has its ridge at 9.0 m (est.).
- **Cream house with a red tiled roof**, x −141.9 to −132.0. The cornice is at 5.1 m and the upper windows at 3.0–4.66. It has an arched brown carriage gate and two red dormers. Ridge 8.3 m (est.).
- The rest is flat at 6.0 m (est.), round the courtyard.
- **OSM repair:** the way's ring has the courtyard ring spliced into the outer ring. Read as one ring, it cuts a diagonal slit through the street front, and the pass 17 volume has no straight street face (352.8 m²). The prepare script rebuilds it as the outer ring (vertices 0–3) with the courtyard (vertices 4–9) as a hole. That gives 442.6 m², exactly the `area` recorded for the way in district17. This adds 89.8 m² outside the raw ring. It is the only change to an outline.

Strömgatan, south side (550598948, front facing local +y):
- **Modern four-storey block**, the whole 42.1 m front, 12.5 m deep. The ground storey is red vertical boards on a concrete plinth (to 0.63 m), with a belt at 5.10 m. It has shop windows in red frames (0.63–3.12), a glazed door with a top light (0.21–3.10) and a black barred gate (2.8 m wide, to 2.97). Above are two storeys of red render, with windows at 5.68–7.15 and 8.53–9.94 on a 2.92 m rhythm and a grey bar French balcony on every fourth. A grey standing-seam metal top storey runs from 10.7 to 13.6 m (top est.).
- The rest of the north part (y 174.5–193) is flat at 10.7 m (est.). The big south part along Fiskaregatan (3081 m²) is flat at 9.75 m (est., the district height).

Mesh names (unchanged from district17): `SM_Kvarnholmen_House_92204193`, `_92379265`, `_92204176`, `_550598948`. None had a detail_pass above 17, and none of pass 105's buildings is touched. The panoramas are working references only. No pixel is used as a texture.

## Measurement

Four photos from three panoramas, pitch 15, vfov 90 (vertical), 756×405. Per `captures.txt`, the 92204193 photo is upscaled from a half-size tile. It was resected at the stated size; its effective resolution is half.

| Panorama (photo) | Heading | Reported position | Resected / used position | Camera height |
|---|---|---|---|---|
| Anln3lF1nEqOwrr30ISdDw (33 Kaggensgatan, looking W) | 243 | (−185.71, 159.60) | (−186.0, 157.6) | 2.25 m |
| Anln3lF1nEqOwrr30ISdDw (33 Kaggensgatan, looking E) | 63 | (−185.71, 159.60) | (−186.0, 157.6) | 2.25 m |
| xNJhTuDn9h0ti6FGaeqxTw (22 Fiskaregatan) | 152 | (−148.51, 142.14) | (−148.7, 139.95) | 2.25 m |
| _1Txv9THK8nwUCoF0r0m-Q (18 Strömgatan) | 153 | (−106.48, 212.31) | (−106.48, 210.9) | 2.5 m |

**Resection** (on facade planes 0.355 m outside the OSM lines; `SCR/p82/hit.py` and `meas.ray` with vfov 90):
- **Kaggensgatan:** the two views share one panorama with a facade on each side of the 9.7 m street. A grid search over camera x and height fits five base-row readings (three on the east facade, two on the west) to z = 0: x −186.0, height 2.25 m, residual 0.03 m². No building corner on the street fronts is in frame except, possibly, the Outnorth house's south corner. The along-street position therefore comes from the symmetry of three gables, each assumed to sit centred on its own front: the grey house apex against its north corner gives a shift of −1.5 m, and the cream house apex against its Fiskaregatan corner gives −2.1 m. The camera was set at y 157.6 (−2.0 m). With that position, the Outnorth apex reads at 151.39 against the 150.85 of a gable centred on y 146.5–155.2. If the frame-edge corner at u 742 were the Fiskaregatan corner, the shift would be −4.3 m. That contradicts the cream gable, so it was rejected; the corner is just out of frame. Scale check: the Outnorth door frame reads 0.31–2.22 m (1.9 m).
- **Fiskaregatan:** distance and height come from the base row (v 367) and the door: a 2.2–2.3 m door (frame and transom) gives a height of 2.25 m and a distance of 5.0 m. Camera y is then 139.95, 2.2 m south of the reported position. Camera x is set by the green house's west corner (u 437) on the OSM corner x −150.1: x −148.7 (0.2 m shift). The east joint of the green house then reads at x −141.9.
- **Strömgatan:** distance and height come from the base row (v 372) and the glazed door (0.21–2.18 m, a 2.0 m door at height 2.5 m): y 210.9, 1.4 m south of the reported position. No corner or joint is in frame, so x is the reported value. The window rhythm is regular, so a ±2 m error in x only shifts the gate and door along the front.

**Values read on the facade planes** (m above the street at the base row):

| House | Openings | Eaves / ridge |
|---|---|---|
| 92204193 cream gable | ground windows 0.88/0.93–2.23, upper 3.80–5.06/5.34, gable window 6.26–7.32, about 1.42 wide; window centres y 151.6 and 154.4 (third at 148.8 est., out of frame) | gable foot 5.56 (belt 5.54), apex 9.46 |
| link | door 0.30–2.03; fascia top 3.53; railing top 5.37 | 5.4 |
| 92204193 tan (Gardell) | shop windows 0.67–2.29, 1.67/1.80 wide; upper windows about 3.95–5.30, 1.0–1.24 wide at y 161.26/163.72/166.18; belt 3.47 | cornice 5.99; dormer faces about 7.6–9.1 projected on the facade plane (set back, so lower in reality) |
| 92379265 Outnorth | upper windows 3.49–4.68 at y 153.35/151.45/149.4; door 0.31–2.22 at y 153.65; sign 3.0–3.27; awning 2.55; gable window from 5.16 | gable foot 5.25 (belt 5.0), apex 7.11 |
| white shop | glass 0.47–2.22, gable glazing to about 4.2; diamond window 1.5 at y 155.87 | eaves 2.68, apex 4.61 at y 159.22 (centre of 156.12–162.04: 159.08) |
| grey gable house | window 0.58–2.29 | gable foot 2.81, apex 4.57 |
| 92204176 green | plinth top 0.54; window 1.20–3.09 (x −142.0 to −143.6); door 0.91–3.57 (x −144.3 to −145.6); shop window 1.32–3.12 (x −146.3 to −149.2); upper windows 4.98–6.83 at x −142.7/−144.7/−146.75/−148.75; band 4.17 | cornice top 7.57 |
| 92204176 cream | window 3.02–4.66 at x −139.2 to −140.7; arch top about 2.06 at the frame edge | cornice 5.11; dormer at x −139.8 to −141.3 |
| 550598948 | plinth top 0.63; gate 0–2.97 (s 16.4–19.2 from the east end); shop windows 0.63–3.12 (s 21.4–23.4, 24.4–27.1, 29.4–31.7); door 0.21–2.18 (s 27.3–28.5); windows 5.68–7.15 and 8.53–9.94, 1.5–1.9 wide | belt 5.10; render top / metal 10.70 |

## Estimated

- All ridges except the gable apexes of the cream, Outnorth, shop and grey gable houses. Ridge heights estimated: 92204193 tan 10.8 m, 92204176 green 9.0 m and cream 8.3 m. The 550598948 top storey (13.6 m) is cut off in the photo.
- Roof forms: the tan house's steep saddle (the photo shows a steep black sheet roof with dormers; mansard or saddle is not decidable). The green house's low saddle. The dormer depths and sizes, fitted to the photo.
- The depth of every front zone (10–12.5 m) and every rest zone marked est. in `source/block104.json`, with their heights, plain casement walls and flat roofs. The Fiskaregatan sides of 92204193, 92379265 and 550598948 are street fronts that were not photographed.
- The north part of the tan house beyond the frame (y 167–175.9): windows, shop windows and the door continue the seen rhythm. The cream gable house's south bay (y 148.8) is out of frame.
- The east 5 m of the 92204176 cream house: two upper and two ground windows, and the second dormer at x −134.6.
- The 550598948 ground floor away from the photographed 15 m (shop windows at s 4.2/8.0/11.8/34.5/38.3), and the window rhythm continued over the whole front. Which windows carry French balconies is a regular every-fourth pattern, not the photographed one.

## Verification

- `KALMAR_GEO=SCR/pylib python3 scripts/prepare_block104.py` prints `BLOCK104_ZONES_OK`: footprint 7643.0 m² (with the repaired 92204176), zoned 7642.9 m², outside OSM 0.0 m², OSM not zoned 0.05 m², overlap 0.0 m². Repair check: the repaired 92204176 is 442.6 m², equal to district17's recorded area (442.6 m²). The raw ring is 352.8 m².
- Sandbox (prelude rebuild_block103), two runs. Both print `BLOCK104_GEOMETRY 4` and `SANDBOX_DONE` without errors. `drop_degenerate_faces104` (with the `_thin` test) runs on every object right after `s21_finish`. It dropped 44 / 105 / 60 / 37 faces on 92204193 / 92379265 / 92204176 / 550598948. The printed samples are zero-area or sliver faces (area 0 to 6e-5 m²): at arch crowns (y176 gate, z 2.6), on wall-strip seams (z 4.5–4.7 on the Outnorth front, 9.98 on the Strömgatan front), and where walls meet the flat roofs of the rest zones. Not every dropped face was inspected.
- Renders at 756×405 from the resected cameras were compared side by side with each photo (`SCR/p104/cmp_2_*.jpg`; run 1: `cmp_1_*.jpg`). Corners, joints, window columns, gable apexes, eaves and the base rows line up within a few to about 20 pixels. Examples: Outnorth windows at u 505/575/648 against 500/570/640 in the photo; green house upper windows at u 143/213/283/353 against 140/212/287/360; the Strömgatan floors at v 105–145 and 37–68 in both. Run 2 changed only the Gardell dormers (larger, closer to the eaves), the tan colour, the ridge of the tan house and the rest roofs (light grey instead of near-black).
- The official build, the FBX export check and the Unreal checks are pending; the lead fills in the build results.

## Limitations

- The Kaggensgatan camera's along-street position rests on gable symmetry, not on visible corners. Joints there can carry about ±0.5 m. A view at about (−186, 150), heading 63 and pitch 15, would show the Outnorth house's Fiskaregatan corner. The same spot at heading 243 would show the cream house's corner.
- The Gardell dormers in the render are still smaller and set higher than in the photo, and the steep roof shows less. The roof may be a mansard.
- The link is modelled flush with the street. In the photo it is recessed about 1 m between the cream and tan houses.
- The large unseen rest zones (1792 m² behind 92204193, 3081 m² of 550598948 along Fiskaregatan) are plain flat boxes. They replace hipped generic volumes, and from the air they read as big flat roofs. Views of the Fiskaregatan sides would let a later pass detail them.
- The 18 Strömgatan camera's x is unresected, so the gate and door positions along the 42 m front can be off by about ±2 m.
- The 92204176 OSM repair changes its outline. If the lead prefers the raw ring, the prepare check `repair_176` shows the difference (89.8 m²).
- Drainpipes, lamps, the parking and bicycle signs, the projecting shop signs, the Gardell lettering, the street furniture and the cream modern house west of 92204176 (92204157, not in this pass) are omitted.

## Official build

The lead's build of pass 104 passed the Blender geometry checks and the FBX export, and two rebuilds gave identical meshes. Passes 28–103 are unchanged, except pass 85's prison building, which pass 103 deliberately corrected. The Unreal import and its checks are deferred.
