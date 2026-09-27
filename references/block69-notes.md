# Pass 69: the corner house on Norra Långgatan and Proviantgatan

Pass 69 details the district volume 91926315 on the corner of Norra Långgatan and Proviantgatan (Proviantgatan 23), east of the pass 68 cottage. It is a pale yellow rendered two-storey corner house with a canted corner:
- a rusticated ground floor over a granite plinth with cellar windows;
- brown-framed casements over sunk panels;
- the brown double door (23) up three stone steps on Proviantgatan;
- a white band between the storeys, and upper windows in white surrounds that run down to the band over sunk panels;
- a white cornice, and a hipped sheet-metal roof with a chimney.

The mesh keeps its name (`SM_Kvarnholmen_House_91926315`). The street-name plates, the traffic sign, the letterbox and the street lamp are omitted.

Panoramas are working references only. No pixel is used as a texture, and no panorama, depth or tile data was extracted.

## Measurement

Two panoramas were used:
- **The panorama at the crossing** is resected on the west end of the Norra Långgatan front (x 169.65) and on the fold of the canted corner (x 175.41). The district outline's three corner points do not fit one camera within 20 px. The corner's two short faces are therefore kept as drawn, and only the long fronts carry measured windows.
- **The Proviantgatan panorama** stands about 4.3 m from that front. It is resected on the front's north corner (y 58.90) and on the joint with the white house to the south (y 49.48). Its base row agrees with a camera 2.3 m high.

| Feature | Measured (m) | Modelled (m) |
|---|---|---|
| Norra Långgatan axes (x) | 173.8, 171.15 | the same |
| Proviantgatan axes (y) | 50.65, 52.33, 56.17, 57.95; door 53.72–54.86 | the same |
| Heights | plinth 0–0.72; ground windows 1.69–3.16; band 3.63–3.98; upper windows 4.54–6.06; cornice 6.7–7.2 | the same; ridge 8.6 (estimate) |

The two fronts' floor heights differ by up to 0.2 m, because the street slopes. The Proviantgatan values are used for both.

The west wall rises from the pass 68 cottage's eaves (2.78 m), not from the district height, so no gap opens above the cottage roof.

## Verification

See `previews/block69-delivery.json`:
- every report passed;
- identical on two rebuilds;
- 31 floor samples and 29 capsule sweeps, no obstructions;
- calibration of 11 features: median 8 px, largest 16 px;
- passes 28–68 unchanged.

## Limitations

- **The canted corner** follows the district outline; its window position is estimated.
- **Estimates:**
  - the roof;
  - the rear and yard walls.
