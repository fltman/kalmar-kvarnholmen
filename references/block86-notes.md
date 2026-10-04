# Pass 86: the west side of the Proviantgatan row

Pass 86 replaces five generic district volumes from pass 17 (6.65 m blocks) on the east side of eastern Kvarnholmen, along the west side of the Proviantgatan row, with the houses that stand there. Two volumes are split, which gives seven parts. From south to north:

- **91928565 (Proviantgatan 6):** a pale vertical-boarded house of one and a half storeys on a high stone plinth. It has four windows, a recessed entrance at the top of a stone stair with an iron rail, three dormers, a chimney and a tiled saddle roof with gables at both ends.
- **91928576:** a small pink rendered cottage with two windows, white corner boards and a steep tiled saddle roof with a chimney. The long outline is split into this front range (5.2 m deep) and a lower range behind it under a saddle roof across the plot.
- **91928540 (Proviantgatan 8):** a cream rendered two-storey house:
  - a rusticated ground floor and a storey band;
  - five upper windows with relief diamond panels under them, and four lower windows, all in dark green frames;
  - the red double door in green framing under a glazed transom;
  - a tiled mansard roof with two red dormers.
- **91928545 (Proviantgatan 10):** a red vertical-boarded two-storey house with white window surrounds, white corner boards and eaves board, under a low hipped dark metal roof.
- **91928582 (Proviantgatan 12):** a narrow sage-green rendered corner house of two storeys. It has stone quoins, a storey cornice with panels under the upper windows, a deep main cornice and a low hipped metal roof. The rest of the L-shaped outline is a lower rear wing with a flat roof.

Panoramas are working references only. No pixel is used as a texture.

## Measurement

Four panoramas were used, all at heading 62 (looking east at the fronts), pitch 10 and vertical fov 90, 726×420 px. Resected positions are in the local frame.

| Panorama | Where | Google position | Resected position | Camera height | Resected on |
|---|---|---|---|---|---|
| h0Ym-YPyMwJO9vAWLZvunQ | Proviantgatan 6 | (183.99, −64.56) | (181.8, −66.85) | 2.3 m | the house's south corner, plus the facade base read as ground level (one bearing only) |
| SVddiexv6scAsGwz3bLb5w | Proviantgatan 8 | (184.56, −44.59) | (181.43, −46.99) | 2.3 m | the cream/pink joint and the pink cottage's south corner |
| 1kEN_v_4ckV1Dgn6AyUE2Q | Proviantgatan 10 | (184.60, −34.04) | (181.7, −36.2) | 2.3 m | the red/cream joint and three cream upper-window centres measured from the no. 8 camera (residuals ≤0.3 m) |
| Cibo0KrPHo2Fu0x5LaVJJw | Proviantgatan 12 | (184.22, −13.49) | (181.5, −16.63) | 2.3 m | the two street corners of the green house |

**Resection.** All four resected positions lie 2.2–3.1 m west and 2.2–3.1 m south of Google's positions, in the west half of the street. The offset is the same for all four, which supports the solutions.

**Camera height.** The facade base reads 0.0–0.1 m with a 2.3 m camera on the no. 10 and no. 12 panoramas, and −0.13 m at the pink cottage.

**Identification.** The resections settle which house is which outline:
- the cream house with the diamonds and the double door is 91928540;
- the red boarded house is 91928545;
- the pink cottage is 91928576.

The red house's north wall is the red wall seen behind the fence from no. 12. Its eaves line there reads about 6.2 m, so the north side is an eaves side. That is why the red roof is hipped.

**Plane offset.** Heights were first read on the OSM line, but the model's facade surface stands 0.355 m outside it. The first sandbox comparison showed upper features up to 0.4 m too high. Heights on the 4.1–4.7 m sight lines were therefore scaled about 8% towards the camera height. The values below are the corrected model values.

All values are in metres. "s" is the distance along the front from its north end.

| Part | Measured | Estimated |
|---|---|---|
| Proviantgatan 6 | eaves 4.05 (gutter 4.2–4.5 on the OSM line); plinth 0.9; windows at s 10.9 and 13.2, sills 1.85, 1.4 wide; entrance recess s 7.2–8.6 from 1.2 m; dormers at s 2.8, 8.1, 13.1; chimney at s 11 | the two north windows (s 2.5 and 4.7; grazing, mirrored about the door); ridge 8.7 (the ridge line reads 9.2 if the roof is symmetric, but the ridge end does not fit any symmetric depth; see Limitations); stair depth; dormer form |
| Pink cottage | eaves 3.1; windows at s 2.2 and 4.6, 1.4–2.7; plinth about 0.6 | the front range's depth (5.2) and ridge 7.0, from a ridge line read 2.6 m behind the front; the rear range (eaves 2.9, ridge 4.6) |
| Proviantgatan 8 | five upper windows at s 1.35, 3.4, 5.55, 7.9, 10.4 (two cameras); lower windows below the first four; double door at s 9.3–11.4; storey band 3.25; diamond panels 3.6; cornice about 6.4–6.7; dormers at s 3.8 and 8.5 (triangulated from two cameras), 1.7 wide | the mansard form (a steep lower slope, implied because the tiles are visible above a 6.4 m eaves from a 2.3 m camera at 4.5 m); break and ridge (10.1); chimneys |
| Proviantgatan 10 | windows at s 5.75 and 8.1 on both floors (1.2–2.7 and 3.8–5.3); eaves 6.1 with the roof edge just above; plinth 0.5; north wall an eaves wall without openings | the third window pair (s 3.4, partly out of frame); the door and window at s 1.2; hip roof ridge 8.2; the east wall (not seen) |
| Proviantgatan 12 | front 6.0 m between the quoins; windows at s 1.7 and 4.1 on both floors (1.65–3.1 and 4.55–6.15); storey cornice 3.7–4.6; main cornice top about 7.0; plinth 0.6–0.75 | main block depth (9.9); hip roof (top 8.2); chimney; the rear wing (eaves 3.6, flat roof) |

## Verification

- `prepare_block86.py` prints BLOCK86_ZONES_OK. The zones cover the five outlines:
  - 647.4 m² footprint, 647.5 m² zoned;
  - 0.05 m² outside OSM and 0.02 m² not zoned;
  - no overlap.
- The sandbox build (passes 26–85, then pass 86 on a copy of `Stortorget.blend`) prints BLOCK86_GEOMETRY 5 and SANDBOX_DONE without errors.
- Workbench renders from the four resected cameras were compared side by side with the panoramas, in three iterations:
  - **First comparison:** the upper features came out too high because of the plane offset described above. It also showed a side-running stair at no. 6, where the photo shows a stair running out to the street. The red house's north wall had generic windows that the photo does not show. All three are fixed.
  - **Final comparison:** windows, door, joints, cornices and eaves agree within about 10 px. Colours are close.
- The official build and the Unreal import and checks are pending. The lead fills in the build results.

## Limitations

- **The roof of no. 6:** the photo shows more roof than the model. The ridge end seen at the south gable fits a ridge only 0.7–1.8 m behind the front, which the roof's mid-line reading contradicts. A similar mismatch appears at the pink cottage. A small error in the camera's y or the gable plane may explain it. The model keeps a symmetric saddle with a ridge at 8.7 m.
- **The mansard on no. 8** is inferred, not seen in profile. An aerial or rear view would settle it.
- **No view shows:**
  - the rear wings (the pink cottage's rear range, the green house's main-block depth and its wing);
  - the east walls;
  - the north side of the green house on the cross street.

  These carry generic windows or none.
- **Grazing reads:** openings far from each camera were read at grazing angles (±0.3–0.5 m).
- **Omitted:**
  - the red board fence between nos 10 and 12, which is not in OSM;
  - street signs, the lamp post, plants, the meter box at no. 8, downpipes and the basement vents of the pink cottage.

## Official build

The lead's build of pass 86 passed the Blender geometry checks, two rebuilds gave identical meshes, and passes 28–85 are unchanged. The Unreal import and its checks are deferred.
