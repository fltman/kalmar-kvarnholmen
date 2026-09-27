# Pass 50: house number 14 on Ölandsgatan

Pass 50 details the district volume 92379264 on the south side of Ölandsgatan, between pass 49's cream house and the yellow-and-white house to the east. It is a white roughcast two-storey house with:
- an arched gateway with open iron gates and a white passage through to the courtyard;
- two shop windows, and a round-headed door at each end (a grey roller shutter, a grey panelled door), each on a step;
- three white casements in flat surrounds upstairs;
- a grey plinth and a small cornice;
- a tile roof with two dormers at the eaves (one red, one white) and two chimneys.

The rear and the roof slopes are estimates. The mesh keeps its name (`SM_Kvarnholmen_House_92379264`).

Panoramas are working references only. No pixel is used as a texture, and no panorama, depth or tile data was extracted.

## Sources

- **Outline:** `source/block50.json` (zone `wh`, from 92379264). The neighbour probe rebuilds 92379272 with its courtyard hole, so the west end is a party wall.
- **Google Street View**, April 2025, 90° vertical field of view: two panoramas on Ölandsgatan (1372 × 871 frames). The review cameras are 295 (house) and 296 (east); 297 is an aerial view.

## Measurement

**Registration.** The two cameras are chained on nine shared edges (the east joint, the door, the shop window, the upper window, the gateway) and anchored on the west joint measured in pass 49.

The east joint comes out at x -142.92 and -142.81 (OSM -142.80). Pairs agree within 0.26 m. The cameras stand 5.7–5.8 m out, at a height of 2.40 m.

| Feature | Measured (m) | Modelled (m) |
|---|---|---|
| Doors | east x -143.5 to -144.5, sill 0.53, crown 2.74; west x -154.93 to -155.91, crown 2.42 | the same |
| Shop windows | x -145.88 to -147.65 (0.94–2.42); x -152.29 to -154.25 (0.88–2.42) | the same |
| Gateway | x -149.05 to -151.36, springing 2.45, crown 2.98 | the same |
| Upper windows | three axes, 4.19–5.59 | the same |
| Plinth, eaves | plinth 0.65; cornice 6.2–6.37 | eaves 6.3, ridge 9.0 (estimate) |
| Dormers | centres x -146.15 and -153.13, 0.3 m behind the wall line (two views); windows 6.87–7.57 | the same |

## Verification

See `previews/block50-delivery.json`:
- every report passed;
- 14,241 triangles in one mesh;
- identical on two rebuilds;
- 46 floor samples and 43 capsule sweeps, no obstructions;
- calibration of 16 features: median 8 px, largest 38 px;
- passes 28–49 unchanged.

The largest deviation is the west joint, which stays on the OSM line as in pass 49.

## Incidents

- **Disk full.** The disk filled during the second rebuild, and the `.blend` save failed. The saved file was left intact: it opened and its hashes checked. The rebuild was repeated once space returned.
- **Unreal.** The editor was killed under memory pressure, then hung once on relaunch. It was restarted, and the pass was imported and validated.

## Limitations

- **Estimates:** the roof slopes, the rear and the passage's far end.
- **Omitted:** the signs, the hanging signs, the number "14" and the pavement boards.
