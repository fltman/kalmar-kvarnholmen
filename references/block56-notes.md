# Pass 56: the green wooden house on Västra Sjögatan

Pass 56 details the district volume 92379307 on Västra Sjögatan, between pass 55's stone-clad building and pass 38's Barometern building. The model had shown a pink rendered volume here. It is in fact a green-boarded two-storey wooden house:
- vertical boarding between six white pilasters, on a grey rendered plinth with a dark sill;
- five axes of green six-light casements in white surrounds on both storeys;
- the middle ground axis is a panelled white door under a pedimented porch hood, up five steps;
- a frieze and a dentil cornice;
- a tile roof with a snow rail and two chimneys.

The mesh keeps its name (`SM_Building_92379307`).

Panoramas are working references only. No pixel is used as a texture, and no panorama, depth or tile data was extracted.

## Sources

- **Outline:** `source/block56.json`, one zone. Pass 55's building counts as an 11.9 m neighbour, and pass 38's Barometern building as 10.6 m.
- **Google Street View**, April 2025, 90° vertical field of view, pitched 20° up (1148 × 1063 frames): two panoramas on Västra Sjögatan ("9"). The review cameras are 315 (porch) and 316 (north); 317 is an aerial view.

## Measurement

**Registration.** The two cameras are chained on two shared window edges and anchored on both corners: the joint with pass 55 (y -26.81) and the south corner (-42.47). Residuals are within 0.22 m, the camera height is 2.41 m, and the cameras stand 6.1 m out.

| Feature | Measured (m) | Modelled (m) |
|---|---|---|
| Axes (y) | -41.12, -38.08, -34.72 (door -34.58), -31.78, -28.77 | the same |
| Pilasters (y) | -42.2, -39.81, -36.4, -33.37, -30.58, -27.07 | the same |
| Heights | plinth 0.87, sill to 1.04; ground windows 2.06–3.9 (surrounds 1.86–4.09); door 1.49–3.67, porch hood 4.09–4.28, steps to 1.4; upper windows 5.41–7.35; frieze and cornice 7.53–8.43; roof edge 8.81 | the same, eaves 8.5, ridge 10.8 (estimate) |

## Verification

See `previews/block56-delivery.json`:
- every report passed;
- 38,994 triangles in one mesh;
- identical on two rebuilds;
- 52 floor samples and 48 capsule sweeps, no obstructions;
- calibration of 12 features: median 10 px, largest 35 px (the pilasters at the edge of the close view);
- passes 28–55 unchanged.

## Limitations

- **Estimates:** the roof, the rear wings and the south wall (partly behind the Barometern building's glazed bay).
- **Omitted:** the signs and the seasonal decorations.
