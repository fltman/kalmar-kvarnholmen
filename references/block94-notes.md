# Pass 94: the south side of Fiskaregatan east of Östra Sjögatan

Pass 94 replaces four generic district volumes from pass 17 (two-storey rendered blocks under hipped roofs) with the buildings that stand on the south side of the narrow part of Fiskaregatan. Their fronts face north (bearing about 14°). They are split into six parts.

- **91885523:** a grey pebble-dash rendered office. It has a lighter semi-basement, two storeys of ribbon windows (white two-light frames between dark green posts, dark green sill bands) and a grey fascia. Above is a steep dark tiled roof with four gabled dormers. At the west end there is a recessed two-storey entrance bay. It holds a ribbed dark panel over a window, an air-conditioning unit, a dark canopy and a glazed shop front.
- **91926303:** a white rendered modernist block with a flat roof and a dark coping. Nine tall window columns on two storeys each have a brown boarded spandrel panel under the glazing, dark frames and a copper sill. Under the columns is a row of semi-basement windows.
- **91926337:** a pale blue-green vertical-boarded house with its gable to the street, on a dark plinth. It has two windows below and one in the gable, in green sashes and white surrounds, and white double bargeboards. Behind it is a low flat-roofed rear wing (estimated).
- **91926333:** a red vertical-boarded house with its gable to the street. It has two pairs of windows with yellow sashes in grey surrounds, grey corner boards and a wide grey-green bargeboard. The west 3.1 m of the outline's street front and the back of the outline form a lower red-boarded part with a flat roof (estimated, unseen).

Panoramas are working references only. No pixel is used as a texture.

## Measurement

Three panoramas from April 2025 were used. All are 696×375 crops at heading 166, pitch 15 and a vertical field of view of 90°. The facade plane is taken 0.355 m in front of the OSM line.

| Panorama | Where | Google position | Resected position | Heading used | Camera height | Resected on |
|---|---|---|---|---|---|---|
| QZ6LAylEmrO0ZCUWlQyuaA | office | (100.88, 127.86) | (99.92, 125.94) | 166 | 2.5 m (assumed) | the office's west corner (x 91.05), just right of the frame, with the distance 3.6 m from the facade set by the storey height (see below) |
| 4jTJbBk6bv09y_4ecDlMoA | blue-green house / modernist block | (123.27, 122.59) | (121.99, 121.56) | 166 | 2.6 m | the blue-green house's corners (x 122.66 and 130.39), which are also the joint with the modernist block |
| M1snxnQNlUVD6QVYA1T-aQ | red house | (143.61, 117.13) | (145.87, 114.25) | 171.3 | 2.45 m (assumed) | the red house's east corner (x 143.51), its base line and the symmetry of its gable (see below) |

**Checks on the projection.** The vertical vanishing point was found from line segments detected with OpenCV's LSD in each photo. It lies at v −498 to −558, u 337–348. This agrees with pitch 15° and f = 187.5 px (vfov 90), which predicts v −512. Roll is under 1°.

**Blue-green house and modernist block (91926337, 91926303).**
- A first fit that also freed the heading gave −3.3°. It made the modernist block's window columns shrink steadily across the photo, which they do not do in the image.
- With the heading at the nominal 166°, the columns come out evenly spaced at 1.45 m. The modernist block's basement-window bottoms then land at the facade base (−0.07 m), which is the check on the 2.6 m camera height.
- The camera is 0.6 m north of the street centreline.

**Office (91885523).**
- The east end is out of frame. The west corner (x 91.05) is just right of the frame, at the far side of the recessed bay.
- The distance from the facade was chosen at 3.6 m. This gives a floor-to-floor height of about 3.1 m (lower ribbon top to upper ribbon top) and 1.4 m wide two-light lower windows.
- The camera height of 2.5 m is assumed: the base is not in the photo.

**Red house (91926333): which width is right.**
- Resecting on both outline corners (x 134.0 and 143.51) gives a camera 5.6 m from the facade and 2 m north of the street centreline. With that camera the house's base falls 0.7 m below the bottom of the photo, which is impossible for a camera 2.5 m high. The windows also come out about 2 m tall.
- The camera was therefore resected with a height of 2.45 m and the base line in the photo (v 371) at 0.1 m, on the east corner, and with the gable apex taken as midway between the corners. This puts it 0.2 m from the street centreline.
- The red house's gable front then measures about 7.1 m (6.7 m was modelled; see Verification). The gated section east of it measures 3.6 m, against 6.0 m in OSM.
- The red house is anchored on the outline's east corner (x 143.51). The 3.1 m west of it within 91926333's front is not seen in any photo.

**Measured values.** All values are in metres. "s" is the distance along the front from the stated corner.

| Part | Measured | Estimated |
|---|---|---|
| 91885523 office (s from the west corner) | semi-basement to 1.47; dark green sill band 1.47–1.55; lower ribbon 1.55–3.21; spandrel 3.21–4.80; upper ribbon 4.80–6.28; fascia 6.28–7.05 with a gutter to 7.31; eaves 7.05; lower windows 1.4 wide at a 1.6 pitch from s 3.75; recess s 0–3.4: panel 4.3–6.4, window 3.1–4.3, canopy 2.03–2.55, shop front below; dormer centres about s 4.2, 7.85, 11.5 and 15.15 | the 3.6 m camera distance (sets the scale); the recess depth (1.2 m); the roof: a 52° slope (from the dormers' bases over the eaves) to a nearly flat top at 10.2 2.4 m in; dormer size (window 1.5 × 1.5, from 7.95) and their setback (0.6 m) |
| 91926303 modernist (s from the west corner) | coping top about 9.0; lower columns: panel 1.28–2.55, glazing 2.55–4.16; upper: panel 4.92–6.12, glazing 6.12–7.78; basement windows to about 0.6; columns 1.0 wide at a 1.45 pitch, the east one with its edge at s 13.65 | the west four columns (out of frame), taken to continue the pitch; no entrance modelled |
| 91926337 blue-green (s from the west corner) | eaves 5.33–5.38; wall apex 7.2 over s 4.2; bargeboard apex projects at 8.3; plinth 0.3; lower windows (with surrounds) 1.03–2.79, centred at s 2.05 and 5.15; gable window 4.05–6.09, centred at s 4.0 | ridge 7.35; the roof covering (unseen; red tile); the 5.6 m depth of the gable body; the rear wing (eaves 3.0, flat) |
| 91926333 red house (s from the east corner) | eaves 3.9–4.0 at the corner; wall apex 5.9; lower windows (with surrounds) 0.82–2.22; upper windows 2.9–4.6, straddling the eaves line; window centres about s 2.0 and 4.55; base line 0.1 | the 2.45 m camera height (sets the scale); ridge 6.1; the roof covering (unseen; red tile); the 8.3 m depth; the lower west and rear part (eaves 3.2, flat) |

## Estimated

- The roofs behind the eaves: the office's top, the two gable roofs' coverings and depths, and the rear parts. None is seen in the photos.
- The side and rear walls carry generic windows (rendered) or plain boarding (boarded houses).
- The modernist block's west half and the office's east 1–2 m are out of frame and repeat the measured pattern.

## Verification

- `scripts/prepare_block94.py` prints `BLOCK94_ZONES_OK`. The zones cover the four outlines: 498.1 m² in all, 0.0 m² not zoned, 0.0 m² outside OSM and no overlap.
- **The sandbox build** (`SCR/sandbox.py` on a copy of `source/Stortorget.blend`, prelude pass 93) prints `BLOCK94_GEOMETRY 4` and `SANDBOX_DONE` without errors, in both iterations.
  - `drop_degenerate_faces94` (zero area, repeated corner, slivers under 0.1 mm) is called right after `s21_finish` in `b94_finish`. The number of faces it removed was not recorded.
- **Renders from the resected cameras**, compared side by side with the photographs in `SCR/p94/sb2/cmp_v1.jpg`, `cmp_v2.jpg` and `cmp_v3.jpg` (aerial: `SCR/p94/sb2/air.png`):
  - *Office:*
    - The two ribbon rows, the fascia and eaves, and the recess's position match within a few pixels.
    - The dormers' positions match.
    - The dormer windows were enlarged in the second iteration. The rendered dormer windows are still a little shorter (bottom at v 28 against v 40).
  - *Blue-green house and modernist block:*
    - The first iteration (heading 162.7) drew the columns too close together further from the camera.
    - With the camera refitted at heading 166, the columns, both window rows, the copper sills, the basement windows and the coping line up within about 5 px.
    - The blue-green house's corners, eaves, gable apex and three windows line up within about 10 px.
  - *Red house:*
    - The corners, eaves, the four windows and the base line match within about 10 px. The front was narrowed from 7.25 to 6.7 m and the windows moved 0.35 m east in the second iteration.
    - The rendered gable apex is still about 25 px west of the photo's. Either the photo's apex is off the middle of the front, or a pixel reading is wrong.
- The official build and the Unreal checks are pending; the lead fills in the build results.

## Limitations

- **The red house's width.** The red house and the gated section beside it are about 2.5 m and 2.4 m narrower in the photo than in OSM, if the camera is a normal 2.45 m high. The house was anchored on the outline's east corner. The west 3.1 m of 91926333's front is a lower part whose real form is not seen. If OSM is right after all, the camera was about 3.3 m high and the heights of this house are about 1.35 times too small.
- **Camera heights.** On the office and the red house, the camera heights are assumed, because no base or door is visible. The office's camera distance was chosen from the storey height. Absolute heights there are uncertain to ±0.4 m.
- The ground under the steep views is not seen in any photo.
- **Omitted:** the signs on the office, the AC unit's pipework, downpipes, the street lamp and the aerial.
- **Views that would help** (pitch 0 to show the base and the doors):
  - the red house and the 3.6 m gap west of it (x 130.4–134.0), from about (136.0, 120.5), heading 166, pitch 5;
  - the office's east end and the modernist block's west half, from about (108.0, 124.5), heading 166, pitch 5;
  - the office roof, from about (99.0, 132.0), heading 166, pitch 30.

## Official build

The lead's build of pass 94 passed the Blender geometry checks, two rebuilds gave identical meshes, and passes 28–93 are unchanged. The Unreal import and its checks are deferred.
