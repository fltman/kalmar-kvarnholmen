# Pass 73: the cream mansard house on Proviantgatan

Pass 73 details the district volume 93192422 on the east side of Proviantgatan, across from passes 70–71. It is a cream rendered three-storey house:
- a rusticated ground floor over a grey plinth with cellar windows, and a band over it;
- seven axes of white-framed casements in white surrounds on every storey, in groups either side of a pilaster strip that is rusticated on the ground floor, with strips at both ends;
- a profiled cornice, and a dark mansard with a dormer over each axis.

The yard and party walls keep a plain rhythm. The mesh keeps its name (`SM_Kvarnholmen_House_93192422`). The meter cabinet is omitted.

Panoramas are working references only. No pixel is used as a texture, and no panorama, depth or tile data was extracted.

## Measurement

One panorama on Proviantgatan ("18") stands about 8 m from the front. It is resected on the joint with the house to the north (y 25.41) in one heading, and on the south corner (y 11.68) in another. The base row puts the camera 2.5 m high.

| Feature | Measured (m) | Modelled (m) |
|---|---|---|
| Window axes (y) | 23.72, 21.7, 19.96, 16.42, 14.78, 12.9 | the same, 1.25 wide |
| Pilaster strip (y) | 17.5–18.7 | the same |
| Heights | plinth 0–0.98; ground windows 1.87–3.56; band 4.06–4.41; first floor 5.2–6.85; second floor 8.13–9.72; cornice 10.3–11.1 | the same |
| Mansard | top edge at 12.9 on the facade plane, about 1 m back | 14.0, 1.0 m in |

The district volume stood at 6.65 m.

The mansard's top edge was first read on the facade plane. Re-read at its depth, it reaches about 14 m. The first Unreal view hid the dormers behind the cornice, so the mansard and the dormers were raised to match.

## Verification

See `previews/block73-delivery.json`:
- every report passed;
- identical on two rebuilds;
- 21 floor samples and 19 capsule sweeps, no obstructions;
- calibration of 8 features: median 8 px, largest 16 px (the dormers);
- passes 28–72 unchanged.

## Limitations

- **The mansard** is read on one ray at an assumed depth.
- **Estimates:**
  - the flat upper roof;
  - the yard side and its irregular outline.
