# Pass 88: Ölandsgatan 7, Södra Vallgatan 15, two houses further west on Södra Vallgatan and the Larmgatan pavilion

Pass 88 replaces five generic district volumes from pass 17 (two-storey blocks, 6.65 m) in the south-west of Kvarnholmen. They are split into eleven parts. The meshes keep their names.

- **92379283 (Ölandsgatan 7):** a pale green boarded two-storey house on a stone plinth, with white corner boards and a central white lesene. On the left is an arched carriage gate in a white portal with a cornice. It has four upper and three ground-floor casements in white surrounds. The red tile saddle roof carries a central dormer under a curved roof and a flue pipe.
- **92379259 (Södra Vallgatan 15):** a white boarded two-storey house on a high stone plinth, about 0.95 m. The central entrance bay stands between two broad lesenes. Steps lead up to a recessed double door, and above it is a balcony door with a French balcony. It has eight grey-green casements. On the saddle roof are an arched dormer with a red roof and two brick chimneys with white caps. A low flat-roofed rear wing fills the rest of the outline.
- **91856598:** the outline holds two buildings, worked out on the resected panorama:
  - the small brown boarded building, 4.85 m wide and 4.7 m high, under a flat roof with a metal coping. It has a carriage door under a five-light band window and a green door with a tall glazed light;
  - the yellow boarded two-storey house east of it, which takes the remaining 10.1 m. It has a hipped tile roof and a red gabled dormer.
  
  The white house on the left of the photo is 91856586, and the yellow house is part of 91856598. It is not the three-storey Ölandsgatan 8 (91856590, pass 53), which lies further east.
- **91856586:** the white functionalist house, in three parts:
  - the taller west part, with a granite-clad ground floor (a shop window and a blue door with a round light), a red-framed window, a round window and a two-storey bay projecting 0.8 m;
  - the lower east part, with a shop window, a recessed entrance, three red-framed windows and a grey awning. Its top floor is set back with a red-framed window band, and a glazed railing runs along its roof terrace;
  - the rear.
- **91856600 (Larmgatan):** confirmed as the pavilion:
  - the green boarded part at the north end, under a dark hipped roof, with a small window, an ochre door, a round window and a chimney stack;
  - the glazed café under a dark fascia;
  - the white-framed conservatory at the south end.

Panoramas are working references only. No pixel is used as a texture.

## Measurement

Five panoramas from April 2025 were used, six views in all.

| Panorama | Where | View (heading/pitch) | Google position | Resected position | Camera height |
|---|---|---|---|---|---|
| MfbpT6617re7-iDHZz-sfQ | Ölandsgatan, opposite nr 7 | 333 / 15 | (−110.51, −144.51) | (−110.79, −146.57) | 2.2 m (assumed) |
| aFgBhnfRiQbYydYUx5a_FA | Södra Vallgatan 15 | 332 / 15 and 312 / 35 | (−150.04, −173.74) | (−149.33, −175.41) | 2.3 m (assumed) |
| zOSal1XTk-exXcBxMgjoiw | Södra Vallgatan, at 91856598 | 332 / 20 | (−251.59, −172.61) | (−253.01, −175.85) | 2.3 m (assumed) |
| ifG7ttixTyM6ox2NaJdXig | Södra Vallgatan, at 91856586 | 332 / 20 | (−261.63, −172.45) | (−263.05, −175.69) | 2.3 m (assumed) |
| bqhE2ekqWjLWCY2LkN79sg | Larmgatan | 62 / 15 | (−294.06, −204.19) | (−293.0, −204.07), partly | 2.3 m (assumed) |

**Resection.**
- **Ölandsgatan 7:** resected on its two front corners (OSM vertices). The camera lies 0.8 m south of the street centreline and 2.1 m south of Google's position.
- **Södra Vallgatan 15:** resected on its two front corners, 1.7 m from Google's position.
- **91856598 and 91856586:** the two Södra Vallgatan panoramas were resected together. Each sees only one known corner, the west corner of 91856586 in one and the corner between 91856586 and 91856598 in the other. The solve assumes both share one offset from Google's positions. It gives (−1.42, −3.24), so both cameras sit 0.5 m north of the street centreline.
- **Larmgatan:** only the pavilion's north-west corner was used, with the camera assumed on the Larmgatan centreline. The south-west corner then projects within about 10 px of the end of the conservatory.

**Cameras in the model.** The facade boxes stand 0.355 m outside the OSM line. The calibration cameras 431–434 and the sandbox views therefore sit 0.355 m further out than the resected positions:
- 431: (−110.79, −146.93)
- 432: (−149.33, −175.77)
- 433: (−253.0, −176.21)
- 434: (−293.36, −204.07)

At 3.3 m from a facade, leaving this out made the render about 11 % too large, which the first sandbox run showed. The camera heights are assumed: no facade base or ground line is visible at a known height. The Ölandsgatan view puts the facade base at 0.1–0.3 m with a 2.2–2.3 m camera.

**Readings.** Pixel rays were intersected with the street-front plane (`hit.py`), and "s" is the distance along the front from its west end (on Larmgatan, from its north end). All values are in metres.

| Part | Measured | Estimated |
|---|---|---|
| Ölandsgatan 7 | eaves 6.2; upper windows 4.25–5.8 at s ≈ 2.3, 4.4, 7.4, 9.7; ground windows 1.95–3.35 at s 4.3, 7.4, 9.7; gate s 0.8–3.0, about 2.9 high; lesene s 5.66; dormer at s 5.8 | ridge 12.2, from the roof silhouette about 7.8 m on the facade plane, which gives a pitch near 50°; window centres within ±0.3 m |
| Södra Vallgatan 15 | eaves 6.45; plinth top 0.95; ground windows 1.95–3.25; upper windows 4.45–5.85; lesenes s 4.6–5.45 and 6.85–7.65; recess s 5.5–6.8, up to 3.1 | window centres made symmetric about the bay (measured 1.5, 3.4 / 7.8–9.0, 10.6–12.2); ridge 9.6; roof colour; chimney and dormer depth (from the 35° view) |
| Brown building | width 4.85; top 4.7; carriage door s 1.06–2.84, 2.0 high; band window s 0.8–3.1, 2.3–3.2; green door s 3.5–4.45, light to 3.1 | depth (the full outline) |
| Yellow house | eaves 6.2; upper windows 3.7–5.1 at s 6.05 and 8.45; ground windows 0.9–2.3 | the two eastern window pairs (mirrored, out of frame); ridge 9.0; dormer at s 10.9 (its left edge is at s 9.8, the rest out of frame); its door, not seen |
| 91856586, west part | ground floor (granite) to 3.2, fascia to 3.5; shop window s 0.3–3.3; door s 3.7–5.2 to 3.1; window s 0.3–2.5, 4.7–6.4; round window centre s 1.6, 8.6; bay, brought forward 0.8 m to its own plane: s 3.1–6.05, solid 3.3–4.82 and 6.6–8.0, windows 4.82–6.6 and from 8.0 | height 10.8 (the top is cut off; windows continue above 9.7); bay depth 0.8; 10 m depth of the front range |
| 91856586, east part | wall top 7.05; terrace railing to 8.25; top-floor window band about 8.3–9.2 (from both Södra Vallgatan views); windows s 7.0–8.25, 9.25–10.65, 11.95–13.25 at 4.65–6.4; awning top 3.45, s 9.7–13.4 | top-floor setback 0.6 and depth 6; awning reach |
| Pavilion | green part s 0–6.8, eaves 3.0; café s 6.8–15.0, fascia top 3.2; conservatory s 15.0–19.3, top 2.9; door s 3.4–4.4; round window s 5.6, centre 2.1 | hip ridge 4.4; the east and north walls; the café's east side |

## Verification

- **Zones:** `prepare_block88.py` prints BLOCK88_ZONES_OK. Of the 866.5 m² footprint, 0.08 m² is not zoned, nothing lies outside OSM and nothing overlaps.
- **Sandbox:** three runs of `SCR/sandbox.py` on a copy of `Stortorget.blend`. Each printed SANDBOX_DONE with no errors. Each run rendered the six photo views at 696×375 from the resected cameras, plus an aerial.
  - Run 1 found the 0.355 m wall offset: the renders were too large at close range. The Ölandsgatan 7 roof also hardly showed, since its ridge was too low.
  - Run 2 moved the cameras out and raised the ridge from 10.9 to 12.2 m. It also made the French balcony shallower and moved the chimneys of nr 15 forward on the roof, to where the 35° view shows them.
  - Run 3 corrected the bay of 91856586, which had been drawn with its wall-plane readings.
  - In the final renders, the eaves, the window rows, the brown building's top, the yellow house's windows, the bay and the pavilion's three parts agree with the photos to within about 10–20 px. The worst case is the right-hand windows of nr 15, about 20 px right of the photo.
- **Not run by this pass:** the official build, the Blender geometry checks and the Unreal import and checks. The lead runs them and fills in the results.

## Limitations

- **Camera heights** are assumed (2.2–2.3 m), so absolute heights carry about ±0.2 m.
- **The pavilion camera** rests on one corner and the centreline assumption. Its heights may be off by about 10 %.
- **Roofs:** every ridge is an estimate. The roof colours of nr 15, the yellow house and the pavilion were not seen. The tall west part of 91856586 is cut off at about 9.7 m in the photo, and its 10.8 m top is a guess.
- **Walls not facing a street:** they carry generic windows. The rear wing of nr 15 and the rear of 91856586 are plain flat-roofed volumes.
- **Omitted:**
  - signs, lettering and the house number;
  - the café terrace with its railing and furniture;
  - the air-conditioning unit, the downpipes, the handrails at nr 15 and the cellar vents;
  - the parked vehicles.
- **Extra views that would help:**
  - the roof of the yellow house and its east half, from Södra Vallgatan at about (−240, −177), heading 332 (looking straight at the front), pitch 25;
  - the top of 91856586, from about (−262, −182), heading 332, pitch 35;
  - the pavilion's north side, from about (−278, −188), heading 152, pitch 10.

## Official build

The lead's build of pass 88 passed the Blender geometry checks, two rebuilds gave identical meshes, and passes 28–87 are unchanged. The Unreal import and its checks are deferred.
