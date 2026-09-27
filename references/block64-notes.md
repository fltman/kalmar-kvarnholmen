# Pass 64: the ochre house at Östra Sjögatan and Fiskaregatan

Pass 64 details the district volume 91885528 on the corner of Östra Sjögatan and Fiskaregatan. It is an ochre roughcast two-storey house.

**To Östra Sjögatan:**
- six axes of green-framed casements in white surrounds, the upper ones under small green hoods;
- a pale green plinth with barred cellar windows;
- the eaves;
- a tile roof with four red dormers.

**The long Fiskaregatan side** is seen only at the corner and keeps the same rhythm.

The mesh keeps its name (`SM_Kvarnholmen_House_91885528`).

Panoramas are working references only. No pixel is used as a texture, and no panorama, depth or tile data was extracted.

## Measurement

**Registration.** Two panoramas on Östra Sjögatan ("19" and "21"). Each is anchored on one end of the house (y 108.64 and 129.99) and on its base row, with the cameras 2.6 m high. Their shared windows disagreed by 0.5 m, and the difference was split between them.

| Feature | Measured (m) | Modelled (m) |
|---|---|---|
| Axes (y) | 127.97, 124.49, 121.4, 118.04, 114.63, 111.17; dormers over the middle four | the same |
| Heights | plinth 0–0.83; ground windows 1.73–3.68; upper 5.04–6.85; eaves 7.03–7.61; dormer windows about 8.9–9.9 | the same, eaves 7.4, ridge 10.8 (estimate) |

## Verification

See `previews/block64-delivery.json`:
- every report passed;
- identical on two rebuilds;
- 104 floor samples and 102 capsule sweeps, no obstructions;
- calibration of 10 features: median 8 px, largest 20 px (the dormers from the corner);
- passes 28–63 unchanged.

## Limitations

- **The Fiskaregatan side** repeats the measured rhythm.
- **Estimates:** the roof and the courtyard side.
- **Omitted:** the shop sign and the street lamp.
