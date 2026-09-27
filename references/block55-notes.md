# Pass 55: the stone-clad building on Storgatan and Västra Sjögatan

Pass 55 details the district volume 92379255 on the corner of Storgatan and Västra Sjögatan. It is a limestone-clad three-storey commercial building with a flat roof.

**To Västra Sjögatan:**
- seven axes of white casements set flush in the slab cladding, on two storeys;
- a dark fascia at the roof;
- at street level, from the south: a garage door, a shopfront, the entrance (number 13) in a broad carved stone surround, a wide shop window, and an open arcade under the corner with a square pier.

**The long Storgatan side** is a pedestrian street and not in Street View. It repeats the same rhythm as an estimate, with shopfronts and the arcade's first bay.

The mesh keeps its name (`SM_Building_92379255`).

Panoramas are working references only. No pixel is used as a texture, and no panorama, depth or tile data was extracted.

## Sources

- **Outline:** `source/block55.json`, one zone.
- **Google Street View**, April 2025, 90° vertical field of view, pitched 20° up (1148 × 1063 frames, the browser window's size in this session):
  - two panoramas on Västra Sjögatan, "13" and "9";
  - one view towards the Storgatan corner.

  The review cameras are 312 (entrance) and 313 (south end); 314 is an aerial view. On Storgatan only a user photosphere exists, and it was not used.

## Measurement

**Registration.** The two cameras are chained on three shared window edges and anchored on the joint with the wooden house to the south (y -26.81), spaced as their GPS positions. Residuals are within 0.25 m, the camera height is 2.38 m, and the cameras stand 5.8–5.9 m out.

| Feature | Measured (m) | Modelled (m) |
|---|---|---|
| Axes (y) | -25.65, -23.2, -20.7, -18.17, -15.55, -12.9, -10.3 | the same |
| Windows | first floor 5.19–7.12; second floor 8.44/8.61–10.44 | 5.19–7.12; 8.52–10.44 |
| Fascia | 11.35–12.2 | top 11.9 |
| Street level | shop windows 0.44–2.53; sign band 3.2–3.7; entrance y -18.7 to -17.41, 0.48–3.2, surround y -19.84 to -16.86; garage y -26.34 to -23.79, to 3.24; corner pier y -11.81 to -11.28 | the same; arcade 2.4 m deep (estimate) |

## Verification

See `previews/block55-delivery.json`:
- every report passed;
- 36,586 triangles in one mesh;
- identical on two rebuilds;
- 144 floor samples and 141 capsule sweeps;
- one obstruction, Storgatan's street furniture, with a verified detour;
- calibration of 12 features: median 8 px, largest 30 px (the shop window's edge);
- passes 28–54 unchanged.

## Limitations

- **The Storgatan side** is an estimate.
- **Also estimates:** the arcade's depth, the rear and the courtyard sides.
- **The slab grid** is drawn as horizontal joints only.
- **Omitted:** the signs, the awnings and the motifs of the entrance reliefs.
- **Observed but not changed:** the house to the south (92379307) is a green-boarded wooden house with white pilasters, while the model shows a pink rendered volume there.
