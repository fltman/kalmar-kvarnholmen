# Pass 106: the north side of Södra Långgatan to Sjöfartsmuseet, and the south end of Landshövdingegatan

Pass 106 replaces eight generic district volumes from pass 17 with the houses that stand there. They are split into fourteen zones (`source/block106.json`).

On Södra Långgatan, north side (fronts face south), from west to east:

- **91928568 (60 Södra Långgatan):** a two-storey house. The ground floor is rusticated cream ashlar render on a dark stone plinth, up to a storey band at 5.0–5.6 m. The upper floor is red brick banded with cream stucco. The windows are segment-headed, with red frames and cream hoods. The centre bay stands between two pilasters and has a round-headed upper window over the dark red door, which is reached by short steps. A bracketed cornice runs at 9.4–10.1 m. The roof is a low dark sheet hip with two round-topped dormers and a brick aedicule with a round top over the centre bay. A lower back wing (zone `bkw`) is estimated at 7.0 m with a flat roof.
- **91928594 (the corner of Landshövdingegatan):** an ochre roughcast two-storey house on a grey plinth. It has red frames in light surrounds, light corner pilasters and a light eaves board. The dark red door sits up 1.2 m of steps in a stone surround, with a basement window to its left. The saddle roof runs along the street, with a round-topped red dormer over the door and a chimney. The gable faces Landshövdingegatan and has two attic windows. The east front has three window columns on both floors. A small bump at the back (`ocb`) is 3.0 m with a flat roof.
- **93199647:** a grey boarded shed on a low granite strip, with an olive garage door at its west end and the blue Sjöfartsmuseum sign. It has a flat roof at 3.3 m.
- **93199649 (Sjöfartsmuseet):** a grey stucco neo-renaissance two-storey house. Its parts:
  - a stone plinth to 1.0 m with basement windows;
  - a rusticated ground floor with eight bays, the entrance in the fourth bay from the west, with a door surround and a hood, up 1.3 m of steps;
  - a storey band at 4.4–4.6 m;
  - balustrade panels under eight round-headed upper windows, with pilasters between the windows;
  - a frieze, then a deep bracketed cornice at 9.4–10.3 m;
  - a low hipped grey sheet roof with two chimneys.

  The west side, toward the shed, has two window columns. The strip at the back (`mub`) is flat-roofed.

On Landshövdingegatan:

- **91928552:** the street frontage between the ochre corner house and the red house is a light grey board wall, 2.8 m high, with a red carved double gate (lattice panels) about 2.7 m wide. The yard behind it (zone `yd`) has a flat roof at the wall top and a red tiled lean-to along its north half. The rest of this long OSM outline is the courtyard ranges further west (`yw`, `ym`). They are not seen from the street and are modelled as plain two-storey ochre render with flat roofs at 6.0 m (estimated).
- **91928587:** a falu-red boarded house with a gambrel roof whose ridge runs along the street. The gambrel gables are at the north and south ends; the south one has three windows. The street front has two ground-floor windows, a door and two small dormers on the lower slope. The roof is red tile.
- **93199672:** the long taupe stucco three-storey house on the east side. It has twelve window columns with white surrounds, a dark granite base with a light band, a thin cornice and a low dark hipped roof. The stair bumps at the back (`tpb`) have flat roofs at the eaves height.
- **93199626:** the pink stucco corner house. It has four storeys of windows in cream surrounds, cream quoins at every corner and a tall rough stone base to 1.4 m with basement windows. A cornice runs at about 15.6 m and the roof is a low dark hip. Window columns run on the west (Landshövdingegatan), south (Södra Långgatan) and east fronts.

Note on the pass brief: it said the Landshövdingegatan fronts of 91928552 and 91928587 face west and those of 93199672 and 93199626 face east. In the model it is the other way round. 91928552 and 91928587 stand on the west side of the street, so their fronts face east. 93199672 and 93199626 stand on the east side, so their fronts face west.

Panoramas are working references only. No pixel is used as a texture.

## Measurement

Seven Google Street View panoramas were used, all at a vertical field of view of 90°.

Resection: each camera was solved from house corners on the facade plane, taken 0.355 m outside the OSM line, using bearings at the reported heading. Where only one corner was usable, the camera's distance was set so that the ground line reads z = 0 with a 2.3 m camera height (`m106.py` in the pass scratch folder). Heights scale with the assumed camera height, so they are checked against door heights.

| Panorama | Where, heading/pitch, size | Google position (local) | Resected position | Resected on |
|---|---|---|---|---|
| loPhdJetNUW8mxsA-tKU4Q | 60 Södra Långgatan, 332/20, 756×405 | (268.20, −76.15) | (265.37, −78.29), h 2.3 | the west corner of 91928568 and the ground line (one corner) |
| UMc-8fKeDuAdUaRXwmvmpw | 75 Södra Långgatan, 332/20, 756×405 | (292.19, −77.18) | (291.05, −79.32), h 2.3 | the SE corner of 91928594 and the ground line; the door reads 2.14 m |
| jNQVnyzUFoAWkOapC6uV0A | 78 Södra Långgatan, 331/20, 756×405 | (352.33, −78.02) | (351.94, −79.86), h 2.3 | the museum's west corner and the ground line (two-corner resection disagreed, see below) |
| VWDFnhm4bg8LsUPHqh_Wnw | 81 Södra Långgatan, 331/20, 700×375 | (374.42, −77.44) | (374.47, −79.93), h 2.4 | both corners of the museum front (two-point resection); the ground reads −0.1 m at h 2.3 |
| wuxO1DUNUjvnBbpHXmZAfw | 6 Landshövdingegatan, 242/15, 756×405 (upscaled half tile) | (299.95, −56.51) | (299.43, −57.95), h 2.3 | the NE corner of 91928594 and the ground line of the board wall |
| jn-nOPxAsqN6cHDS_cAlzA | 1 Landshövdingegatan, 62/15, 756×405 | (300.39, −45.66) | (298.76, −47.51), h 2.3 | the taupe/pink boundary (left edge of the pink quoins) and the base of the taupe front |
| KTjIsd-VcvY7fpAP3r52_w | 6 Landshövdingegatan, 62/15, 756×405 | (300.73, −67.23) | (300.0, −69.0), h 2.3 (adjusted) | two corners of the pink front gave (298.89, −69.30), whose scale contradicts the 1 panorama; the camera was moved to 5 m from the front (see below) |

**Measured values** (heights above the street; s along the front from its west or north OSM corner):
- *91928568 (60 panorama):*
  - dark plinth to 0.6 m;
  - ground windows 1.45–3.79 m;
  - door 0.9–3.6 m (2.7 m including the lintel area; a tall old door);
  - storey band 5.0–5.6 m;
  - upper windows 5.7–7.9 m;
  - cornice 9.7–10.1 m, taken as a 10.0 m wall top;
  - dormer tops about 10.7 m, aedicule top about 11.8 m or higher;
  - columns at s 1.8 and 4.2, the centre bay (pilasters at s 5.56 and 8.57, window at s 7.07), and s 9.8 and 12.2; the door at s 6.7–6.8.
- *91928594 (75 panorama):*
  - plinth 0.7 m;
  - ground windows 1.85–3.20 m;
  - door 1.22–3.36 m;
  - upper windows 4.51–6.44 m;
  - eaves 7.95 m;
  - window columns at s 3.4, 5.7, 11.5 and 13.8, the door at s 8.8–8.9 and the upper middle window at s 8.6.
  - The 6 Landshövdingegatan panorama shows a third row of windows at about 8.8–10.4 m on the east end. That makes the east end a gable, so the ridge is estimated at 11.3 m.
- *93199647 (78 panorama):*
  - wall top 3.05–3.25 m, taken as 3.3 m;
  - garage door about 2.2 m high and 2.0–2.2 m wide at the west end.
- *93199649 (81 panorama):*
  - plinth to 1.0 m;
  - rusticated band to 1.7 m;
  - ground windows 1.93–4.03 m;
  - band 4.4 m;
  - balustrade 5.1–5.5 m;
  - round-headed upper windows 5.5–7.4 m;
  - frieze 8.7 m;
  - cornice 9.4–10.3 m;
  - door 1.3–3.8 m in its surround;
  - eight bays at a 2.7 m spacing from s 2.6, with the door in the fourth bay (read at s 10.2–12.0).
- *91928552 (6 panorama, from the upscaled tile):*
  - board wall 2.75–2.85 m;
  - gate at s 4.9–7.7, top about 2.9 m.
- *93199672 (1 panorama):*
  - dark base 0–0.52 m with a light band above it;
  - windows 1.86–3.93, 5.16–7.06 and 8.72–10.47 m, about 1.3 m wide;
  - eaves 11.6 m;
  - window columns spaced 2.38 m, the southernmost at s 28.82.
- *93199626 (6 and 1 panoramas):*
  - stone base to about 1.4 m;
  - window bottoms at 2.0, 5.6, 9.25 and 12.8 m.
  - The 1 panorama reads the pink's rows next to the taupe corner at 5.63, 9.31 and 12.69 m, and they rise above the taupe eaves. The 6 panorama reads the columns on the west front at s 2.2, 4.6, 7.2, 9.7 and 12.3.

**Scale conflict on the pink house.** The two-corner resection on the 6 panorama gives storeys of 4.35 m. The 1 panorama sees the same pink front next to the taupe house at nearly the same distance as the taupe front, and there the storeys are 3.6 m. The 1 panorama is consistent with the taupe house's normal 1.3 × 2.05 m windows, so its scale is used. The 6 panorama's heights were rescaled by 0.82 about the camera height. Its horizontal positions are kept, because they are anchored on both corners. For the same reason, the sandbox camera for the 6 panorama is placed at 5 m from the front, not at the resected 6.2 m.

**The 78 panorama.** A two-corner resection, from the board wall's west end and the museum's corner, put the ground at +0.5 m and the garage door at 1.7 m. The one-corner fit on the museum's corner gives 2.2 m for the door and 3.25 m for the wall. That fit is used. The board wall's visible west end then lies about 2.6 m west of the OSM corner. Either the shed is longer than its outline or the heading is off; the model keeps the OSM outline.

## Estimated, not measured

- **All ridges and roof forms behind the eaves.** None of the photographs shows a roof surface. The rises are 1.6 m (91928568, museum), 2.0 m (taupe), 2.2 m (pink) and 3.4 m (ochre, from the attic windows in the east gable).
- **91928568:** the back wing (7.0 m, flat) and the exact form of the centre aedicule.
- **91928552:** everything behind the board wall: the yard roof, the lean-to and the courtyard ranges `yw` and `ym` (6.0 m, flat, ochre). The tiled lean-to is placed where the photograph shows red tiles behind the wall on the north side.
- **91928587:** the whole house is seen only from the yard to the south, on the upscaled half-size tile. The red boarded walls and the gambrel profile are read from that view: knee about 4 m, top about 7.8 m. The apex reads off-centre, which is not reliable. The house is taken as eaves 3.9 m, knee 6.3 m and ridge 8.0 m, with the ridge along the street. Its street front (windows, door, dormers) is invented to a plausible pattern.
- **93199672:** the north part of the front (s 0–8, outside the view; columns continued at the same spacing), the back and the stair bumps.
- **93199626:** the south and east fronts are not photographed square-on. They use the west front's 2.5 m column spacing and the same four rows. The top of the house is cut off in all views. The cornice at 15.6–15.8 m comes from the storey height and the four rows. The pass brief called it three storeys; the photographs show four rows of windows. The oculi (round windows) seen on the 75 and 78 panoramas are not modelled.
- **The museum:** the back and the east end. The balustraded bridge to the eastern neighbour, seen on the 81 panorama, is not modelled.
- **Not in the outlines and not modelled:** the white board fence between the pink house and the grey shed on Södra Långgatan.

## Verification

- `KALMAR_GEO=… python3 scripts/prepare_block106.py` prints `BLOCK106_ZONES_OK`:
  - footprint 2005.0 m², zoned 2004.8 m²;
  - 0.08 m² zoned outside the OSM outlines;
  - 0.34 m² of the OSM outlines not zoned (slivers under 1 m² along the cut lines, mostly in 91928552);
  - overlap 0.022 m².
- **Sandbox** (prelude: rebuild chain of pass 103): `SANDBOX_DONE`, eight meshes built. `drop_degenerate_faces106` (with the `_thin` test) removed zero-area, repeated-corner and sliver faces in every mesh except 93199626, mostly the coplanar ends of thin trim boxes:
  - 91928568: 72; 93199649: 53; 91928552: 30; 91928587: 24; 91928594: 12; 93199672: 10; 93199647: 4; 93199626: 0.
- **Comparison with the photographs.** All seven views were rendered at the photographs' size with the resected cameras and put side by side (`cmp*_v*.jpg` in the pass scratch folder). What matches:
  - the window rows and columns, eaves and cornice lines of 91928568, 91928594, the museum, the taupe and the pink house, to within a few pixels;
  - the board wall and gate of 91928552;
  - the museum's eight bays and the door position.

  The 78 view still shows the garage door about 70 px right of the photograph, because of the camera conflict described above. The first iteration's steps projected about 2 m; they were reduced to short steps, mostly within the door recesses. There were three sandbox runs; each ended in `SANDBOX_DONE` with no errors. The third run checked the aerial camera, which was moved to the north side because the 28 m mill block south of Södra Långgatan hid the block from the south.
- **Official build and Unreal checks:** pending. The lead fills in the build results.

## Limitations

- The heights scale with assumed camera heights of 2.3–2.4 m. They are checked against door heights of 2.1 m (ochre) and 2.5–2.7 m (the tall doors of 91928568 and the museum). Expect errors of about ±5–10 %.
- Brick, rustication and boards are modelled as relief strips on flat colours. There are no textures from the photographs.
- 91928587 and the courtyard ranges of 91928552 are the weakest parts. An extra view is wanted:
  - Landshövdingegatan at local (300.5, −41.5), heading 242, pitch 15, for the street front of 91928587;
  - Landshövdingegatan at local (301.0, −30.0), heading 62, pitch 25, for the north part and the roof of the taupe house.

## Official build

The lead's build of pass 106 passed the Blender geometry checks and the FBX export, and two rebuilds gave identical meshes. Passes 28–105 are unchanged, except pass 85's prison building, which pass 103 deliberately corrected. The Unreal import and its checks are deferred.
