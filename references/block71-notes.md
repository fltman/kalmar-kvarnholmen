# Pass 71: the gable house on Proviantgatan

Pass 71 details the district volume 91926323 on the west side of Proviantgatan, south of the pass 70 infill house. It is a yellow boarded two-storey house with its gable to the street:
- vertical board-and-batten cladding between white corner boards, with two white boards dividing the front into three bays;
- three dark-framed casements on each storey in white surrounds, and one in the gable;
- a stone plinth under a white sill board, and white barge boards;
- a tile saddle roof running back from the street.

The mesh keeps its name (`SM_Kvarnholmen_House_91926323`).

Panoramas are working references only. No pixel is used as a texture, and no panorama, depth or tile data was extracted.

## The outline

The panorama puts the north corner at y 24.41, 0.63 m short of the district outline. A gap separates the house from the pass 70 infill house, closed at the street by white boarding.

The zone ends at the measured corner, and that strip (9.3 m²) is released as open ground. Pass 70 draws the infill house's south wall only above the district height (6.65 m), so this pass completes that wall below it. The boarding and a shadowed recess above it close the gap at the street.

## Measurement

One panorama on Proviantgatan ("18") stands about 4.2 m from the gable. It is resected on the south corner (y 16.55) and on the base row, with the camera 2.3 m high and residuals under 3 px.

| Feature | Measured (m) | Modelled (m) |
|---|---|---|
| North corner (y) | 24.41 | the same |
| Window axes (y) | 18.36, 20.58, 22.77; gable 20.62 | the same |
| White boards (y) | 19.55, 21.72 | the same |
| Heights | plinth 0–0.55; ground windows 1.44–2.71; upper 3.75–5.03; gable window 5.57–6.81; eaves 5.5; apex 8.0 | the same |

## Verification

See `previews/block71-delivery.json`:
- every report passed;
- identical on two rebuilds;
- 9 floor samples and 7 capsule sweeps, no obstructions;
- calibration of 6 features: median 8 px, largest 10 px;
- passes 28–70 unchanged.

## Limitations

- **The gable's boarding** is drawn plain above the eaves.
- **Estimates:**
  - the roof's rear half;
  - the yard side.
