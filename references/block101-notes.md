# Pass 101: Östra Vallgatan 7–9, the grey house and three gable cottages

Pass 101 replaces four generic district volumes from pass 17 on the west side of Östra Vallgatan, south of the gate by pass 100's grey cottage (93238202), with the houses that stand there. From south to north:

- **93238179 (7 Östra Vallgatan):** the light grey rendered two-storey house.
  - Measured: it stands on the north 6.7 m of the 10.5 m OSM front only (s 3.85–10.51 from the south end). The south 3.85 m of the same way is a grey boarded shed. Its boarded front is about 3.4 m high at the south end and rises to 3.9 m at the house, under a lean-to roof.
  - The house has a black plinth, a door and two windows below, three windows above, dark red casements in pale surrounds, a pale frieze, a black roof edge at 5.63–5.82 m and a black railing round its low roof (top rail 6.19 m). It also has two chimneys and black downpipes at both corners.
- **93238159:** the yellow boarded cottage with its gable to the street. It has one window with dark frames and a flower box, white corner and verge boards, and a red tiled roof.
- **93238211:** the sage green boarded cottage, gable to the street. It has a tall window with dark plum-red frames and a flower box.
- **93238209:** the low yellow boarded cottage, gable to the street. It has a low window and a small attic vent. The brown boarded gate (1.7 m) across the 1.5 m gap to 93238202 is modelled on the street line as part of this mesh.

Mesh names (unchanged from district17): `SM_Kvarnholmen_House_93238179`, `_93238159`, `_93238211`, `_93238209`. All four had no detail pass above 17. 93238202 (pass 100) is not touched. The panoramas are working references only. No pixel is used as a texture.

**Which outline is which.** The OSM corners were projected into both resected views. South to north, they are: grey house + shed = 93238179, yellow = 93238159, green = 93238211, low yellow = 93238209, then the gate and 93238202. The 2.0 m gap between 93238159 and 93238211 (y 32.2–34.2) is a real passage. The north camera sees the yellow side wall of 93238159 through it. The 1.0 m gap between 93238179 and 93238159 is also open in the photos.

## Measurement

Two panoramas, pitch 15, vfov 90 (vertical). Points were taken on the facade planes 0.355 m outside the OSM lines, with `SCR/p100/res.py` (vfov 90).

| Panorama | Crop | Heading | Size | Reported position | Resected position | Camera height |
|---|---|---|---|---|---|---|
| YAp5dc49AzvpMLxyfCBXaA (7, "grey camera") | 93238179_h243 | 243 | 632×476 | (394.93, 24.07) | (394.11, 22.50) | 2.05 m |
| bpmqiA1waZOctbXMD2aS0g (11, "north camera") | 93238209_h243 | 243 | 700×375 | (395.19, 44.18) | (395.01, 42.20), from pass 100 | 2.05 m in this crop |
| bpmqiA1waZOctbXMD2aS0g | 93238202_h222 (pass 100's photo) | 222 | 632×476 | as above | as above | 2.54 m (pass 100) |

**Grey camera resection.** The camera is a three-point least-squares fit on the grey house's north corner (93238179 at y 26.73), the south corner of 93238159 and the north corner of 93238159. Its height, 2.05 m, comes from the gravel at the foot of the grey house.
- A first fit on both corners of the 93238179 outline put the camera 11.6 m from the facade at 3.2 m height. That fit gave a 3.0 m door, 2.5 m windows and 9 m eaves, which is impossible. The rendered house is in fact narrower than its OSM way.
- With the fit on the north corner, the yellow cottage and the ground, the house's south corner falls at s 3.52–4.14 (top and base readings), taken as 3.85. The yellow cottage's corners fall at s −0.23 and 4.45, against its 4.44 m outline.
- Scale check: the door leaf is 1.85 m (0.25–2.10). That is at the low end of the range, but it agrees with the independent north camera's 1.9 m. The fascia agrees too: 5.63 m from this camera, and 5.6–5.9 m from the north camera above its local ground.

**North camera.** Pass 100 resected this camera at (395.01, 42.20) on the corners of 93238209 and 93238202. The projected OSM corners fall on the cottage corners in both crops within a few pixels.
- In the heading-243 crop, the cottage bases read 0.47–0.55 m at a 2.54 m camera height. A height of 2.05–2.07 m puts them on the ground. Heights from this crop are given above the local ground.
- In the heading-222 crop, pass 100's 2.54 m fits. The two crops of one panorama disagree by about 25 px vertically (about 6° of pitch), probably from panorama tilt.
- Cross-check: 93238159's eaves read 2.16 m above ground from the north camera and 2.15–2.20 m from the grey camera. The two views agree.

**Values read on the facade planes** (m; s from the south end of each OSM front; heights above the ground at the house):

| House | Openings (s centre, width, bottom–top) | Eaves / ridge |
|---|---|---|
| 93238179 house | double door 5.25, 1.55, 0.25–2.10; ground windows 7.61 (1.10) and 9.37 (1.15), 0.93–2.10; upper windows 5.25 (1.03), 7.65 (1.10), 9.39 (1.15), 3.00–4.57; plinth top 0.42 | fascia 5.63, roof edge 5.82, railing top 6.19, chimney tops 6.6 (on the facade plane) |
| 93238179 shed | — | boarded front top 3.42 at s 0.7, 3.92 at the house |
| 93238159 yellow | window 2.2, about 1.0–1.3, 0.82–2.05 | eaves 2.11–2.20, apex 3.97 (grey cam) / 4.31 (north cam, oblique) |
| 93238211 green | window about 1.9–2.0, about 1.0–1.3, 0.73–2.24 | eaves 2.25, apex 4.07 |
| 93238209 low yellow | window 2.3, about 1.05–1.2, 0.47–1.78; attic vent 2.4, 0.45, 2.27–2.83 | eaves 1.55–1.64, apex 3.30 |
| gate (209 to 202) | the whole 1.54 m gap | top about 1.6–1.7 |

## Estimated

- **Roof of 93238179:** it is not seen above its black edge. It is modelled as a low black hip (eaves 5.75 m, top 6.35 m) inside the railing. The chimneys are placed 1.2 m behind the front, with tops at 7.05 m.
- **Shed depth and roof:** the shed is taken as the full depth of the OSM way's south part. The lean-to slope is the one read on its front, carried through to the back.
- **Ridges of the cottages:** the gable apexes are read on the facade plane. The ridges run straight back over the whole OSM depth (7.7–9.2 m). The cottage backs are not seen.
- **Window widths:** the windows are seen obliquely and regularised to 0.95–1.15 m. The window centres on the cottages are read from the image fractions between the corners, as the plane readings are poor at grazing angles.
- **Colours:** taken from the photos by eye.
- **Unseen walls:** side and rear walls carry plain walls (pass 26 casements where they fit; none fit under the cottages' low eaves).

## Verification

- **Zones** (`previews/block101-zones.json`): 5 zones in 4 meshes, footprint 207.0 m², zoned 207.0 m², 0.0 m² outside OSM, 0.0 m² not zoned, overlap 0.0 m². `prepare_block101.py` prints `BLOCK101_ZONES_OK`.
- **Sandbox:** three runs, with prelude the rebuild chain of pass 100. All printed `SANDBOX_DONE` without errors.
  - Renders were made from the grey camera and the north camera (both crops), cropped to the photo sizes and compared side by side (`SCR/p101/cmp_3_v179.jpg`, `cmp_3_v209.jpg`, `cmp_3_v222.jpg`), plus one aerial (`SCR/p101/sb3/air.png`).
  - In the grey view, the house corners, the fascia, the railing, both window rows, the door and the yellow cottage's gable, window and corners line up with the photo within a few pixels.
  - In the north heading-243 view, the three gables, their feet and apexes, the windows and the gate line up.
  - In the heading-222 crop the model sits about 25 px high at 2.05 m. The calibration camera 496 therefore uses pass 100's 2.54 m.
  - Run 2 darkened the gate. Run 3 replaced the door (a pale panel from `door83`'s frame colour) with dark panelled leaves.
- **Degenerate faces:** `drop_degenerate_faces101`, with the `_thin` test, runs after `s21_finish` on each house. In the sandbox it removes 4, 8, 8 and 8 faces from 93238179, 93238159, 93238211 and 93238209. The sampled faces have areas of 5e-5 m² or less, at the gutter rods and the shed roof edge.
- **Pending:** the official build, its geometry checks and the Unreal checks. The lead fills in the build results.

## Limitations

- **Two views only:** both are from the street at oblique headings. The backs of all four houses, and the roof of 93238179, are not seen.
- **OSM against photo:** the grey house is about 6.7 m wide, not the 10.5 m of its OSM way. The shed fills the rest, but how deep the shed really is behind its front is unknown.
- **Camera height:** the north panorama's two crops disagree on pitch by about 6°. Heights are given above the ground at each house, which both cameras agree on to 0.05 m on 93238159.
- **Outside OSM:** the grey boarded fence south of 93238179 (it continues about 2.6 m south of the way) and the low recessed infill between 93238211 and 93238209 are not modelled.
- **Omitted:** the roof mast on 93238179, house numbers, signs, the lamp post, bicycles, planters, the bench, climbing plants and cars.

## Official build

The lead's build of pass 101 passed the Blender geometry checks, two rebuilds gave identical meshes, and passes 28–100 are unchanged. The Unreal import and its checks are deferred.
