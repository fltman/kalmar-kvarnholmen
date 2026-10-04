# Pass 81: the east end of Norra Långgatan, x 268–296, both sides

Pass 81 details the last stretch of Norra Långgatan before Ölandsgatan. The five district volumes here are split at measured joints into eleven small boarded houses.

South side:
- **The yellow gable cottage** (93192447), with a weathered board gate at its west end.
- **The red-brown double gate (72)** over the released strip east of it, with a low tiled roof behind.
- **The green cottage** (93192416), with a gable and a window box.
- **The grey-green gable house** (93192390), with a lunette window in the gable and a gateway range with a grey-green double door on its east side.
- **The orange corner cottage** (93192433), with a gable window.

North side:
- **A white boarded wall with a green door (73)**, with the wall run segmented round the doors.
- **The grey-green cottage** (90859897).
- **A red house and the white gable house** (90859890).
- **The small white house** (90859875), with a green door.
- **The small red house** (90859864), with a pilastered door (77).
- **The big red corner house** (90859880), with dark corner boards.

The gate strips (33.9 m² in all) are released as open ground, and their gates are drawn in the street plane.

Panoramas are working references only. No pixel is used as a texture.

## Measurement

Two panoramas on Norra Långgatan are used:

| Panorama | Model position | Camera height |
|---|---|---|
| 5nWH-bnHsLCou2BOT60bjA | (273.61, 68.0) | 2.30 m |
| aoZer_KBSq4yvV28a2lk3g | (294.64, 67.2) | 2.16 m |

Each panorama is resected on a house corner and on both base rows.

The horizontal width and the vertical field of view cannot be separated from one side of the street alone. They are fixed by fitting the south and north fronts together, which gives a vertical field of view of about 90–94°.

Looking south (heading 152), image right is west. An early fit had the two sides swapped.

All values are in metres.

| House | Front x | Eaves | Apex | Openings (centre x, sill, width, height) |
|---|---|---|---|---|
| Yellow cottage | 268.6–273.3 | 3.04 | 4.22 | window 270.85, 0.92, 1.38 × 1.65 |
| Gate 72 | 273.6–276.1 | – | – | double gate, height 2.16 |
| Green cottage | 276.1–281.6 | 1.92 | 3.39 | window 279.0, 0.92, 1.49 × 1.30 |
| Grey-green house | 281.6–288.7 | 4.20 | 6.38 | windows 285.2 and 287.0 on both floors; lunette 285.97 at 4.75 |
| Gateway range | 288.7–291.1 | 4.16 | 5.40 | double door 290.13, 1.83 × 2.41 |
| Orange cottage | 291.1–296.0 | 3.67 | 5.43 | windows 292.95 and 294.49; gable window 293.71 at 2.95 |
| Door 73 | 270.5–271.8 | – | – | green door, height 2.16, wall 2.25 |
| Grey-green cottage | 272.4–276.8 | 1.78 | 3.22 | window 274.75, 1.08, 1.07 × 1.18 |
| Red house | 276.8–279.7 | 2.90 | 4.20 | window 278.2 |
| White gable house | 279.7–284.6 | 4.37 | 5.62 | windows 281.2 and 283.0 on both floors |
| Small white house | 284.6–287.6 | 2.93 | 4.00 | door 284.75; window 286.36 |
| Small red house | 287.6–292.6 | 2.70 | 3.90 | window 288.6; door 290.55 between pilasters 289.89 and 291.09 |
| Red corner house | 292.6–296.4 | 3.80 | 5.52 | windows 294.72 at 0.65 and 2.49 |

## Verification

- The Blender geometry checks passed.
- Two rebuilds gave identical meshes.
- Passes 28–80 are unchanged.
- Each house was compared against the panoramas from the five calibrated cameras.
- An earlier Unreal import found window boxes too deep and windows drawn on a short slanted step out in the street. Both are fixed.
- The Unreal import and its checks are deferred until the models in the area are finished.

## Limitations

- **Estimates:**
  - the roofs of the irregular ranges (gateway range, red house, small white house, small red house), which are simple saddle roofs over the bounding rectangle;
  - the depths;
  - the yard sides.
- **Omitted:** signs, the lamp, the parking meter and the house numbers.
