# Pass 91: the east end of Storgatan

Pass 91 replaces five generic district volumes from pass 17 with the houses that stand there. The volumes are split into eight zones.

On the north side (fronts facing south), west to east:

- **93192424:** a red boarded house with its gable to the street, black bargeboards and a black corner board. The gable front runs from x 259.6 to 266.45, so its east 0.8 m lies inside the outline of 93192442. The grey double door sits under the east half of the gable, with one window below and one in the gable.
- **93192442:** a green boarded gable house from x 266.45 to 270.85, with two windows below and one above. East of it is the gateway: a red double door in a yellow boarded wall with white posts and a white beam, under a tiled lean-to. The gateway's wall continues across the 1.5 m gap to 93192397, which is outside the OSM outlines.
- **93192397:** a yellow boarded gable house from x 273.93, with two windows below and one in the gable. The low yellow boarded link west of it is part of the gateway.

On the south side (fronts facing north):

- **91928597:** a cream stucco shop with a stepped gable. The gable has five steps a side, each with a grey coping, and a finial on top. Below the gable are corner pilasters with caps, a portal round the big shop window (with its crest and cross), a glass door and a second window. The shop had `detail_pass` 17 in the district-17 source audit, so no later pass had detailed it. Its roof is a saddle running back from the street.
- **91928575 (Storgatan 65):** a grey boarded two-storey house on a dark plinth, with three windows a floor, white corner boards, a frieze and a dark tiled saddle roof. Its west gable carries two windows.

**93192417**, the westmost of the four north-side volumes, is in none of the photographs. It keeps its pass-17 volume.

Panoramas are working references only. No pixel is used as a texture.

## Measurement

Three panoramas from April 2025 were used. All are 696×375 crops with a vertical field of view of 90°.

| Panorama | Where | Google position | Resected position | Camera height | Resected on |
|---|---|---|---|---|---|
| 6hF44bWMAmz8ho823D5heQ | 68 Storgatan | (271.26, −2.92) | (269.68, −3.92) | 2.4 m | the shop's corners x 275.19 and 265.24, on the plane 0.355 m in front of the outline |
| QA6zmsid1HPB6KKEKcKmIw | 63 Storgatan | (281.38, −2.96) | (279.89, −4.55) | 2.4 m | the yellow house's east corner (x 279.75, see below) and the east corner of 93192387 (x 294.9, grazing) |
| KXLIRvp9y9hjPEGL0CIWBg | 65 Storgatan | (291.04, −4.05) | (289.74, −4.20) | see below | the corners of 91928575 (x 295.35 and 279.97) |

**Reading heights.** Heights are read on the facade plane, 0.355 m in front of the OSM line, where the model's walls stand. They are given above the pavement.

**The 68 panorama.** The shop's pavement line reads −2.39 m, which gives a camera height of 2.4 m.

The same camera, turned north (heading 332), places the north side as follows:

- the red gable apex at x 263.15;
- the green house from x 266.46 to 270.79, with its apex at x 268.74 (the outline's centre is 268.70);
- the red double door from x 270.96 to 272.53;
- the yellow link from x 272.9 to 273.93;
- the yellow gable apex at x 276.84 (the outline's centre is 276.73).

The apexes agree with the outlines to within 0.1 m. This settled which photographed house belongs to which volume:

- the red house is 93192424;
- the green house is 93192442;
- the red gate is in the gap;
- the yellow house is 93192397.

**The 63 panorama.**
- The yellow house's east corner was taken as x 279.75: the apex at 276.84, assumed symmetric, gives a 5.8 m front.
- The green gate right of the yellow house then spans x 279.75 to 282.74. It lies inside the outline of **93192387**, which is not in this pass. The green two-storey house's front starts at x 282.7.

**The 65 panorama.**
- On this panorama the pavement line reads −2.75 m. Read directly, the eaves would be 7.4 m with a 2.75 m camera.
- The 68 panorama, using its own resected camera, reads the eaves of 65's street front at 6.4 m and its upper-window head at 5.6 m.
- The two panoramas therefore disagree in scale by about 15 %. The front is either shorter than the 15.4 m in OSM, or the 65 camera is higher than it seems.
- The model follows the 68 panorama: the readings of the 65 panorama are scaled by 2.4/2.75.

All values are in metres above the pavement; "s" is the distance along a front from its east corner.

| Part | Measured | Estimated |
|---|---|---|
| Red house (93192424) | apex 5.2 at x 263.15; right bargeboard slope 35° (foot at x 265.8, height 3.37); upper window x 262.4–263.9, height 3.0–4.2; lower window x 263.2–264.1, height 1.1–2.2; grey door x 265.07–266.3, top 2.2; black board at x 264.5 | eaves 2.9 from apex and slope; ridge across the street at x 263.0; the west ground window (out of frame); the depth and roof behind |
| Green house (93192442) | front x 266.46–270.79; eaves board foot 4.48; apex 5.68; lower windows x 267.46–268.54 and 269.15–270.07, height 1.09–2.11; upper window x 268.25–269.34, height 2.93–4.23 | eaves 4.35 and ridge 5.6 (bargeboard thickness taken off); the roof behind |
| Gateway | door x 270.96–272.53, beam top 2.29; lean-to eaves 3.2 | door height 2.15; the lean-to's depth and pitch; the flat roofs behind |
| Yellow house (93192397) | west corner x 273.93; eaves board foot 3.76; apex 5.25 at x 276.84; lower windows from x 274.55 and up to 278.68, height 1.02–2.15; gable window x 275.67–277.12, height 2.75–4.12 | eaves 3.6, ridge 5.2; the window widths |
| Shop (91928597) | front 9.95 (OSM). Stepped-gable edges at s 0.55, 1.25, 2.0, 2.8, 3.56 and 4.47, with step tops 5.93, 6.72, 7.61, 8.49 and 9.38, mirrored about s 4.915 (west base edge read at s 9.39). Top block s 4.47–5.36 to 9.9; finial 10.9. Pilaster caps 4.3–4.5. Portal s 2.9–7.2 to 4.35, crest to 7.0. Shop window s 3.54–6.59, 0.65–3.3. Door s 0.86–1.66 to 2.6. Second window s 7.3–9.2 to 2.6 | eaves 4.5 and ridge 9.3, with the slope set to pass under each step's inner corner; the 38 m roof running back from the street (not seen); the side walls |
| Storgatan 65 (91928575) | window centres: upper s 2.78, 8.15, 11.94 and lower s 2.90, 8.18, 11.95. From the 68 panorama: front eaves 6.4; west gable apex 10.2 near mid-depth; west gable windows 4.3 m from the front corner, heights 4.3–5.65 and 6.4–8.0 | eaves 6.3 and window heights (scaled; see above); ridge 10.6 (about 40°, so that the roof shows above the eaves as it does in the photo); window widths |

## Verification

- `scripts/prepare_block91.py` prints `BLOCK91_ZONES_OK`. The zones cover the five outlines: 702.9 m² in all, 0.01 m² not zoned, 0.01 m² outside OSM and no overlap.
- **The sandbox build** (`SCR/sandbox.py` on a copy of `source/Stortorget.blend`) prints `BLOCK91_GEOMETRY 5` and `SANDBOX_DONE` without errors.
  - `drop_degenerate_faces91` removed 30, 26, 18, 14 and 14 faces from the five meshes, for the FBX export: faces with zero area, a repeated corner, or a sliver thinner than 0.1 mm.
  - Renders before and after the drop are pixel-identical (`sb2` against `sb3`).
- **Renders from the resected cameras**, compared side by side with the photographs in `SCR/p91/sb2/c1.png` to `c5.png`:
  - *North side (68 panorama):* the green and yellow gables, the windows, the gate and the yellow link match to a few pixels.
  - *First comparison:* it put the red house's apex about 80 px too far left. A narrow red gable on the red volume alone did not fit. The fix was to carry the red gable over the door bay to x 266.45. The apex now falls within about 15 px.
  - *The shop (68 panorama, heading 152):* the front's width, the steps, the portal and the windows line up. The step copings are drawn as plain dark blocks; the real ones have rounded ends.
  - *Storgatan 65:* the window positions match. Under the resected 65 camera the model's eaves sit about 20 px too low, and its windows are narrower than in the photo. This is the 15 % scale conflict described above.
- The official build and the Unreal checks are pending; the lead fills in the build results.

## Limitations

- **93192417** is not modelled. A view from about (256, −5), heading 332, pitch 20 would show it.
- **Estimated:**
  - everything behind the street fronts: depths, rear walls, the roofs behind the gables, and the generic windows on side and rear walls;
  - the shop's roof over its 38 m depth;
  - the height of Storgatan 65, given the scale conflict between the panoramas.
- **Not modelled, because they lie outside these volumes:**
  - the green gate and the green two-storey house of 93192387 (63 Storgatan);
  - the low grey boarded wing with a door in the 4.8 m gap between the shop and Storgatan 65, which is not in OSM.
- **Omitted:** signs, the hanging shop sign, house numbers, the street lamp, pipes, the plants and the cars.

## Official build

The lead's build of pass 91 passed the Blender geometry checks, two rebuilds gave identical meshes, and passes 28–90 are unchanged. The Unreal import and its checks are deferred.
