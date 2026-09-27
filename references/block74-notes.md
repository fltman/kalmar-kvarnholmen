# Pass 74: the beige house and the red-door house on Proviantgatan

Pass 74 details the district volume 93192350 on the east side of Proviantgatan, north of the pass 73 mansard house. It holds two fronts:
- **The beige rendered three-storey house:** a grey plinth with cellar windows, a grooved grey ground floor under a band, three axes of wide white-framed casements in white surrounds on every storey, a cornice, and a tile roof with white box dormers.
- **The southern part of the narrow white three-storey house** with the red panelled door and wide upper windows. The house continues into the next volume (93192446, not detailed).

The mesh keeps its name (`SM_Kvarnholmen_House_93192350`). The street lamp is omitted.

Panoramas are working references only. No pixel is used as a texture, and no panorama, depth or tile data was extracted.

## Measurement

No panorama stands in front of this front. Two panoramas whose cameras are already fixed see it at about 95 degrees to each other: pass 73's from the south and pass 70's from the north.

The three vertical joints they share triangulate on one straight line about 0.8 m in front of the district outline:
- beige house / pass 73 house: y 25.73;
- white house / beige house: y 34.30;
- white house / the next house: y 37.31.

The joint to the pass 73 house lies 0.32 m north of the outline's. The front is kept on the outline, and positions along it are read on the triangulated line and shifted by those 0.32 m.

| Feature | Read (m) | Modelled (m) |
|---|---|---|
| Beige house | y 25.41–33.98; window axes 27.04, 29.83, 32.52, about 1.5 wide | the same, 1.45 wide |
| White house | y 33.98–36.53 in this volume; red door about 35.4 | the same |
| Heights | plinth 0–1.46; ground windows 1.97–3.61; band 4.22–4.44; upper rows from 4.75 and 7.28; cornice 11.2–12.0 | the same; upper windows 1.9 high; roof to 14.5 (estimate) |

The window heights read from the oblique south view grow with height (1.64, 1.89 and 2.06 m). The upper two rows are drawn 1.9 m high.

## Verification

See `previews/block74-delivery.json`:
- every report passed;
- identical on two rebuilds;
- 15 floor samples and 11 capsule sweeps, no obstructions;
- calibration of 7 features: median 12 px, largest 16 px;
- passes 28–73 unchanged.

## Limitations

- **Every reading is oblique**, so window positions carry about ±0.3 m.
- **The front** is kept on the district outline, though the triangulation puts it 0.8 m further out.
- **Estimates:**
  - the roofs and the dormer depths;
  - the white house's upper windows;
  - the yard side.
