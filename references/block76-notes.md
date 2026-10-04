# Pass 76: the north side of Norra Långgatan opposite pass 75

Pass 76 details the district volumes 90859889, 90859896 and 90859844 on the north side of Norra Långgatan, split at their measured joints:
- **The green boarded cottage** on the corner of Proviantgatan: red-framed windows in white surrounds, white corner boards, a cross gable towards the street and a tile roof.
- **The two carriage gates** (57 and 59), blue and grey between white posts, in front of a yard.
- **The red boarded house with white windows**, white corner boards and a chimney with a red cowl.
- **The red boarded house with green-framed windows**, the orange chevron door (61) up a stone step, and two brick chimneys.
- **A narrow red boarded passage door.**
- **The white roughcast house** with its off-centre gable to the street, red windows and red barge boards, and a low annex behind.

The meshes keep their names (`SM_Kvarnholmen_House_90859889`, `…_90859896`, `…_90859844`). The traffic sign and the lamps are omitted.

Panoramas are working references only. No pixel is used as a texture, and no panorama, depth or tile data was extracted.

## Measurement

The houses are measured across the street from the two pass 75 panoramas ("54" and "61"), whose positions were resected there. The north side's base row lies about 0.3 m below theirs, so the cameras stand 1.95 m above these houses.

| Feature | Measured (m) | Modelled (m) |
|---|---|---|
| Green cottage | windows 195.67, 197.39 (both storeys); cross gable about 190.3–194.3, apex 4.8 | the same; eaves 3.4 |
| Gates | posts 198.3, 200.16–200.43, 202.1–202.3; height 2.3 | the same |
| Red house, white windows | x 202.3–209.7 (the joint reads 209.3 and 210.1); windows 204.35, 207.45 | the same; eaves 4.1 |
| Red house, green windows | x 209.7–221.8; ground windows 210.9, 212.25, 213.76, 215.9, 217.38; door 219.85 | the same |
| Heights (red houses) | ground windows 0.86–2.14; upper windows 2.94–3.88 | the same |
| White house | x 222.45–229.5; gable apex 5.76 at x 224.74, eaves 3.93 (west) and 2.82 (east); windows 223.93, 225.41, 228.12 (ground), 223.87, 225.36 (gable) | the same |

## The outline

- **The gate strip** (x 198.3–202.3) is a yard behind the gates. It is released as open ground (20 m²), and the gates are drawn in the street plane.
- **The red and the white house** meet at x 221.8, 0.6 m east of the district outline's joint. The zones follow the measurement.

## Verification

See `previews/block76-delivery.json`:
- every report passed;
- identical on two rebuilds;
- 44 floor samples and 36 capsule sweeps, no obstructions;
- calibration of 15 features: median 10 px, largest 14 px;
- passes 28–75 unchanged.

## Limitations

- **Estimates:**
  - the roofs behind the ridges;
  - the chimney heights;
  - the yards;
  - the back annex.
- **The green cottage's west end** (x 188.5–190.3) is seen only at a grazing angle.
