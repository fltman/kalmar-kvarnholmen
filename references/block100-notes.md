# Pass 100: Norra Långgatan 78–84 and the grey cottage on Östra Vallgatan

Pass 100 replaces five generic district volumes from pass 17 on the north side of east Norra Långgatan, and one on Östra Vallgatan, with the houses that stand there. From west to east:

- **93238210 (78, corner of Landshövdingegatan):** two grey boarded cottages with their gables to the street, joined by a low middle part.
  - The corner cottage is tiny: eaves 2.2 m, ridge 4.05 m. It has one window with folded-back white shutters and a flower box.
  - The taller gable house to the east has eaves 4.2 m and ridge 5.75 m. It has the same shuttered window low down and an attic window that reaches up into the gable.
  - Between them, OSM has a 3 m notch in the street front. A grey boarded screen with a green door stands across it, on the street line, with a tiled lean-to behind.
  - Both cottages have a dark plinth, white corner boards, white verge boards, red tiled roofs and chimneys.
- **93238172 (80):** the falu-red boarded two-storey house on a dark plinth.
  - Six windows with ochre frames and an ochre door on four steps.
  - Eaves 5.0 m, ridge 7.1 m, red tiled saddle roof along the street, chimney.
  - Behind it, a low rear wing under its own saddle roof.
- **93238187 (82):** the pale yellow rendered two-storey house.
  - A 1.0 m dark stone plinth with cellar windows, a string course at 4.5–5.1 m and a cornice to 8.75 m.
  - Five ground-floor windows and a green door in a niche, with its steps inside it, 1.44 m up.
  - A green carriage gate with a glazed fanlight at the west end, and seven upper windows.
  - A black hipped roof (ridge 11.9 m) with three black box dormers, the middle one wide with two windows, and a chimney.
  - A flat-roofed stair tower behind.
- **93238156 (84):** the cream rendered three-storey house.
  - Dark red window frames and a red double door 3.0 m high with a fanlight.
  - A string course over the ground floor.
  - A three-sided bay over the two upper floors on a corbel, with a window in each face.
  - Above the bay, a curved gable with its own window and a short saddle roof running back.
  - Two red-brown dormers, a cornice at 11.8 m and a dark hipped roof (ridge 15.0 m).
  - The long rear wing is flat-roofed at 10.4 m.
- **93238202 (Östra Vallgatan):** a pale grey boarded cottage.
  - Its gable faces the street, with eaves 2.0 m and ridge 3.85 m, one window, a plinth, a tiled roof and a chimney.
  - Its unseen west parts are a saddle-roofed block and a flat-roofed link.

Mesh names (unchanged from district17): `SM_Kvarnholmen_House_93238210`, `_93238172`, `_93238187`, `_93238156`, `_93238202`. The panoramas are working references only. No pixel is used as a texture.

**Outline note.** district17 stores OSM way 93238210 as one self-crossing ring of 12 vertices: a small inner yard of 7 m² is spliced into the outer ring. `prepare_block100.py` uses the first eight vertices, the outer ring that closes round the street notch, as the footprint. The inner yard is roofed over with the middle part. A 1.6 m gap between 93238210 and 93238172, with a green garage door under a tiled roof in the photo, belongs to no OSM way and is not modelled.

## Measurement

Five panoramas, pitch 15, vfov 90 (vertical).

| Panorama | Heading | Size | Reported position | Resected position | Camera height |
|---|---|---|---|---|---|
| U8kJhQDH8vMKUm9xMQx8gQ (80, red house) | 152 | 696×375 | (327.41, 69.09) | (326.33, 67.76) | 2.37 m |
| KX--cQfuPUxO-ppt1z3e6Q (82, yellow) | 154 | 632×476 | (341.07, 68.62) | (340.06, 67.91) | 2.41 m |
| cMCi1-Ayqv8D-RpCIJHc5g (84, cream) | 152 | 696×375 | (362.46, 68.82) | (362.18, 67.41) | 2.23 m |
| v0-i59NWQxYYMMEn6tZgTA (78, corner) | 149 | 632×476 | (305.93, 68.45) | (305.72, 67.59) | 2.24 m |
| bpmqiA1waZOctbXMD2aS0g (Östra Vallgatan) | 222 | 632×476 | (395.19, 44.18) | (395.01, 42.20) | 2.54 m |

**Resection.** All points were taken on the facade planes 0.355 m outside the OSM lines.
- Four cameras are solved from the bearings of two house corners: red 321.51 and 330.44; yellow 330.44 and 349.87; cream 349.87 and 363.57; corner cottage 307.69 and 312.92. These are exact fits with no redundancy.
- The Östra Vallgatan camera is a three-point least-squares fit, on the corners of cottage 93238209 and the south corner of 93238202.
- Corners were read low on the facade where possible. In the yellow and cream photos, vertical edges near the frame edge lean less than a 15° pitch predicts, so readings high up near the edges are less reliable.
- All cameras sit 0.7–2.0 m nearer the houses than Google's reported positions.

Note for later passes: `p82/meas.py` `resect2` calls `ray` with its default vfov of 75. For vfov-90 photos it gives cameras that are too far away. A copy with vfov 90 was used here (`SCR/p100/res.py`).

**Camera height and scale checks.**
- **Yellow 82:** the pavement gives 2.41 m. The green door leaf measures 2.27 m (1.44–3.71), inside the 2.0–2.3 m range. Seen from the cream camera, 82's eaves read 8.2–8.5 m, against 8.28 m eaves and 8.76 m cornice top from its own camera. The two cameras agree.
- **Red 80:** the pavement is hidden by a car. The height comes from the top of 82's gate surround, seen in both the red and the yellow views (3.47 m against 3.97 m at 1.87 m), which gives 2.37 m. Gate widths agree within 7%.
- **Red house door:** the leaf reads 1.86 m, below the usual range. Either the door is low (the house is old) or this view's scale is about 10% small. The heights are used as measured.
- **Cream 84:** the arched double door reads 0.05–3.06 m (springing 2.69 m) and 1.9 m wide.
- **Corner cottage:** the ground beside it gives 2.24 m. Its very low eaves (2.1–2.2 m) are matched by cottage 93238209 seen from the independent Östra Vallgatan camera (eaves 2.1–2.3 m, ridge 3.7 m).

**Values read on the facade planes** (m; s from the west end of each Norra Långgatan front, from the south end on Östra Vallgatan):

| House | Openings (s centre, width, bottom–top) | Eaves / ridge |
|---|---|---|
| 93238210 corner cottage | window 2.55, 1.15, 1.44–2.54; shutters 1.37–3.65 | gable feet 2.1–2.2, apex 4.05 |
| 93238210 gable house (from the red camera) | window 1.10, 1.15, 1.34–2.57; attic window 1.17, 1.1, 3.39–4.57 | gable feet 4.15–4.19, apex 5.74 |
| 93238172 red | ground windows 1.14 / 5.27 / 7.17, 1.05, 1.67–2.73; door 2.81, 1.06, 0.74–2.60; upper windows 1.81 / 5.16 / 7.16, 0.92, 3.69–4.60; plinth top 0.83 | eaves 5.0; ridge 7.1 (ridge line projected onto the plane 3.4 m back) |
| 93238187 yellow | gate 0.15–2.45, to 3.97 with surround; ground windows 3.46 / 5.8 / 12.24 / 15.1 / 17.68, about 1.3, 1.96–3.91; door 9.1, 1.11, 1.44–3.71; upper windows 1.3 / 3.4 / 5.8 / 9.05 / 12.24 / 14.85 / 17.4, 1.96–2.06 high, 5.17–7.23; plinth top 1.01; band 4.50–5.11 | eaves 8.28, cornice top 8.76 |
| 93238156 cream | door 12.02, 1.9, 0.05–3.06; ground windows 2.2 / 5.35 / 8.17, 1.6, 1.30–3.06; band 3.96; upper windows 2.32 (1.5) and 11.3 (1.38), 4.88–6.56 and 8.08–9.74; bay 4.93–8.45, corbel foot 3.25; dormers 0.3–2.3 and 10.25–12.2, top 13.15 | cornice 11.8; curved gable apex 14.36 |
| 93238202 grey | window from 1.07, partly out of frame, 1.21–2.12 | gable foot 1.9–2.0; rake rising 0.65 m per m |

## Estimated

- **Ridges and roof forms:** 82's black hipped roof (11.9 m) and 84's dark hipped roof (15.0 m) are not seen from the street. 84's pitch follows the roof faces already authored in district17 (about 33°). The red house's ridge was read from one view only. 93238202's ridge, 3.85 m, comes from the rake slope.
- **Dormers on 82:**
  - They stand behind the facade plane, so their readings were scaled by about 1.14.
  - Centres 2.3, 9.4 and 16.7 m, widths 3.0, 5.4 and 3.0 m, with tops near 10.9 m.
  - The window pairs are approximate.
- **Bay and gable on 84:**
  - The bay's depth (0.70 m) and its chamfered plan are set to match the photo.
  - The curve of the gable is a nine-point polyline.
  - The short saddle roof behind the gable is assumed.
- **Window sizes:** windows near the edges of the frame were read obliquely and regularised to common widths.
- **Window divisions and colours:** light division, cellar windows, plinth heights and colours are taken from the photo by eye.
- **93238210:**
  - The middle part (eaves 2.6 m, ridge 3.6 m) and the lean-to are not measured.
  - The notch screen's green door was read on the street plane at x 314.25–315.2. Its sill height is uncertain, so it is modelled from ground level.
- **Unseen parts:** the parts behind the street fronts are not seen. That is the red house's rear wing, 82's stair tower (flat, 8.2 m), 84's rear wing (flat, 10.4 m, as in district17's authored roof) and the west parts of 93238202. They carry plain walls with pass 26 casements.
- **Chimneys:** those on 82, 210 and 202 are placed from the photos without triangulation. The one on the red house is assumed.

## Verification

- **Zones** (`previews/block100-zones.json`): 12 zones in 5 meshes, footprint 751.0 m², zoned 751.0 m², 0.05 m² outside OSM, 0.05 m² not zoned, overlap 0.012 m². `prepare_block100.py` prints `BLOCK100_ZONES_OK`.
- **Sandbox:** two runs, with prelude the rebuild chain of pass 99. Both printed `SANDBOX_DONE` without errors.
  - Renders were made from all five resected cameras, cropped to the photo sizes and compared side by side (`SCR/p100/cmp_2_v*.jpg`), plus one aerial.
  - In the comparisons, house corners, eaves, cornices, window rows and columns, doors, the gate, the bay, the curved gable, and the dormer positions and heights line up with the photos within a few pixels. On the cream house the bay and the window columns fall within about 5 px.
  - The second run brightened the roof tiles and set 82's steps into the door niche. In the first run they had run 2.6 m out over the pavement.
- **Degenerate faces:** `drop_degenerate_faces100`, with the `_thin` test, runs after `s21_finish` on each house. In the sandbox it removes 34, 28, 4, 43 and 28 faces from 93238210, 93238172, 93238187, 93238156 and 93238202. The sampled faces all have areas of 6e-5 m² or less, at gutter rods, rake ends and parapet joins.
- **Pending:** the official build, its geometry checks and the Unreal checks. The lead fills in the build results.

## Limitations

- **One view per house:** each house is seen in one panorama from the street, at near-frontal headings. The 93238210 gable house is seen only obliquely from the red camera. The rears are not seen.
- **Ground level:** the red house's ground line is hidden by a car, so its camera height comes from a cross-check against the yellow view.
- **Not in any OSM way:** the green garage between 93238210 and 93238172 is not modelled.
- **Neighbours:** the houses around 93238202 on Östra Vallgatan (the yellow and green cottages 93238209 and 93238211) and the red gable house east of 84 are not part of this pass. They stay generic.
- **Omitted:** signs, the street-name sign, the construction fence, pipes, lamps, the open window sash, antennas, planting and cars.

## Official build

The lead's build of pass 100 passed the Blender geometry checks, two rebuilds gave identical meshes, and passes 28–99 are unchanged. The Unreal import and its checks are deferred.

## Later finding

Pass 101, measured against the ground in two views, found 93238202's eaves and ridge about 0.5 m too high here (the camera height of the bpmqiA1 panorama). A correction is pending.
