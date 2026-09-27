# Pass 46: Ölandsgatan's south side, the salmon house to the cream house

Pass 46 details two district volumes on the south side of Ölandsgatan, west of pass 45:

- **The salmon house** (number 20, in 92379258), two storeys:
  - segmental-arched ground-floor windows in white surrounds with keystones;
  - the black panelled double door and the shop door and window under white arches;
  - upper casements in white eared surrounds, a roundel over the door;
  - a dark plinth and a white cornice.
- **The courtyard wall.** OSM has no building on the street between x -106.7 and -124; there the tall roughcast wall stands, with its arched carriage gate and a barred arched window. It is added on the street line.
- **The small grey roughcast house** (in 92379258): a white corner strip and two axes of red casements in white surrounds.
- **The cream house** (92379298):
  - a rusticated yellow ground floor with two arched windows, an arched gateway with boarded doors in a stone surround, shop windows, and a stone quoin strip;
  - a white band;
  - a cream upper storey of casements in surrounds, with small roundels between them;
  - a white cornice.

The Södra Vallgatan sides and the courtyard ranges stay plain. The meshes keep their names (`SM_Kvarnholmen_House_92379258`, `…_92379298`).

Panoramas are working references only. No pixel is used as a texture, and no panorama, depth or tile data was extracted.

## Measurement

**Registration.** Four panoramas are chained along the street:
- four pairs of window and gate edges;
- one anchor, the joint between the salmon house and the wall (x -106.7).

The pairs agree within 0.1 m, except the gate seen obliquely (0.34 m). The wall-and-grey-house joint comes out at -124.24 (OSM -124.0) and the grey-and-cream joint at -129.2 (OSM -129.84). The cameras stand 4.4-5.1 m out, 2.09 m high. The panorama in front of the salmon house disagreed by 0.7 m and was placed on the joint.

| Feature | Measured (m) | Modelled (m) |
|---|---|---|
| Salmon house | ground windows 1.09-2.9 (arched); upper 3.95-5.21; door 0.34-2.85; plinth 0.73; cornice 5.74-6.35 | the same, eaves 6.3 |
| Wall | top about 6.0; gate to 2.7; grille window 0.2-2.23; plinth 0.75 | the same |
| Grey house | windows 1.21-2.8 and 3.58-5.19 (surrounds); eaves 6.4-6.6 | the same, eaves 6.5 |
| Cream house | arched windows 1.22-2.65; band 2.9-3.7; upper 3.79-5.59; gateway 0.31-2.59; cornice 6.83-7.42 | the same, cornice top 7.4 |

## Verification

See `previews/block46-delivery.json`:
- every report passed;
- 151,728 triangles in two meshes;
- 82 floor samples and 73 capsule sweeps;
- calibration of 18 features: median 8 px, largest 30 px (the grey and cream joint, which the model keeps on the OSM line);
- passes 28-45 unchanged.

## Limitations

- **The cream house's west part** (beyond x -139) is not in the panoramas; its last axis and shop window are estimates.
- **The salmon house's two easternmost axes** are outside the level view and repeat the rhythm.
- **Estimates:** the roofs and the courtyard ranges.
- **Omitted:** the signs, the hanging sign, the house numbers.
