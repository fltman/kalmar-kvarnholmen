# Pass 49: Ölandsgatan's south side, the cream house to the Kaggensgatan corner

Pass 49 details the district volume 92379272 on the south side of Ölandsgatan, between the white house (92379264) and the Kaggensgatan corner. It holds two houses:

- **The cream roughcast house**, two storeys and nearly blank to the street:
  - one white casement over a segmental-arched gateway;
  - the gateway has an iron gate just inside and a boarded passage through to the courtyard;
  - a grey plinth, a white cornice, and a tile roof with one white dormer.
- **The ochre wooden corner house**:
  - vertical boarding between corner and middle pilasters;
  - three shop windows and three brown casements in white surrounds;
  - a cornice band;
  - a boarded mansard storey with three windows, hipped at both ends, under a shallow sheet roof.

The district volume's single height (9.75 m) is replaced by the measured heights. The courtyard ranges and the Kaggensgatan side stay plain, at an estimated 7.0 m. The mesh keeps its name (`SM_Kvarnholmen_House_92379272`).

Panoramas are working references only. No pixel is used as a texture, and no panorama, depth or tile data was extracted.

## Sources

- **Outline:** `source/block49.json`, three zones from 92379272:
  - `cr` runs to the measured joint at x -170.64 and to the courtyard at y -156.8;
  - `yw` is taken 8.6 m deep along Kaggensgatan;
  - `bk` is the courtyard ranges.
- **Google Street View**, April 2025, 90° vertical field of view: three panoramas on Ölandsgatan, plus one view from the corner tilted up 30° for the mansard. The review cameras are 291 (gateway), 292 (joint) and 293 (corner); 294 is an aerial view.
- **Not covered:** the Kaggensgatan lane has no Street View coverage.

## Measurement

**Registration.** The three cameras are chained and anchored on the Kaggensgatan corner (x -181.98):
- five edges between the first two panoramas (the window, the gateway, the joint);
- eight edges between the last two (the windows and the middle pilaster).

Pairs agree within 0.41 m. The cameras stand 5.3–5.6 m from the facade, at a height of 2.39 m.

| Feature | Measured (m) | Modelled (m) |
|---|---|---|
| Cream house | window 4.22–5.68 (surround) at x -165.93 to -167.67; gateway x -165.69 to -168.44, springing 1.82, crown 2.58; plinth 0.93; cornice 6.5–7.04 | the same, eaves 6.8, ridge 9.3 |
| East joint | x -156.32 | kept on the OSM line (-156.93) |
| Wooden house | shop windows 1.1–3.37 (surrounds); upper 4.08–6.14; cornice band 6.35–6.68; plinth 1.0; middle pilaster x -176.74 to -177.35 | the same |
| Mansard | windows 7.4–9.0 on the face; top edge 10.3–10.5 on the facade plane | face inset 0.35 m to 10.4, ends hipped 1.6 m, upper roof to 11.15 |
| Dormer | centre about x -166.9, about 0.6 m behind the wall line (two views) | the same, window 1.15 × 1.1 |

## Verification

See `previews/block49-delivery.json`:
- every report passed;
- 72,661 triangles in one mesh;
- identical on two rebuilds;
- 63 floor samples and 58 capsule sweeps, no obstructions;
- calibration of 21 features: median 8 px, largest 55 px;
- passes 28–48 unchanged.

The largest deviation is the east joint, which the model keeps on the OSM line. The dormer lands 30–40 px off in both views.

## Limitations

- **Estimates:**
  - the courtyard ranges and their height;
  - the Kaggensgatan side;
  - the mansard's upper slope;
  - the passage's far end.
- **The ends of the wooden house.** Its mansard hips follow the tilted view only roughly.
- **Omitted:** the signs, the letter boxes, the pavement boards and the street-name plate.
