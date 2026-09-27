# Pass 70: the infill house on Proviantgatan

Pass 70 details the district volume 93238145 on the west side of Proviantgatan, south of the pass 69 corner house. It is a pale rendered two-storey infill house:
- dark-framed two-light windows on both storeys, a smooth plinth under a grey drip line, and a profiled cornice;
- the gateway at the north end with its boarded wooden gates;
- the glass stair tower with its glazed door, rising past the eaves;
- a red tile roof with white box dormers over the window axes.

The yard and gable walls keep a plain rhythm. The mesh keeps its name (`SM_Kvarnholmen_House_93238145`). The lamps and the sign are omitted.

Panoramas are working references only. No pixel is used as a texture, and no panorama, depth or tile data was extracted.

## Measurement

Two panoramas on Proviantgatan were used:
- **The north panorama** ("20") stands about 4.3 m from the front. It is resected on the joint with the corner house (y 49.48) and on its base row, with the camera 2.3 m high.
- **The south panorama** ("18") is fitted to the glass tower's edges from the north view and to its own base row. The fit leaves up to 20 px on the tower edges, perhaps because the tower stands slightly back. It puts the house's south end within 0.12 m of the district outline.

Heights are taken from the closer north view.

| Feature | Measured (m) | Modelled (m) |
|---|---|---|
| Window axes (y) | 26.72, 29.44, 32.1, 39.1, 41.5, 44.0; upper floor also 47.27 | the same, 1.2 wide |
| Gateway (y) | 45.73–49.2, 3.13 high | the same |
| Glass tower (y) | 34.23–37.32 | the same, 2.6 m past the eaves |
| Heights | plinth 0–0.82; ground windows 1.70–3.21; upper 4.43–5.99; cornice 6.96–7.64 | eaves 7.0; ridge 10.4 (estimate) |

The shared wall with the corner house rises from that house's eaves (7.2 m).

## Verification

See `previews/block70-delivery.json`:
- every report passed;
- identical on two rebuilds;
- 42 floor samples and 40 capsule sweeps, no obstructions;
- calibration of 9 features: median 10 px, largest 16 px;
- passes 28–69 unchanged.

## Limitations

- **The south panorama is fitted, not anchored**, so the south half's window axes carry about ±0.3 m.
- **Estimates:**
  - the roof;
  - the dormers' depth;
  - the stair tower's top;
  - the yard side.
