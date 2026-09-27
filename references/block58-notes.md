# Pass 58: the yellow house on Fiskaregatan

Pass 58 details the district volume 91970261 on the corner of Fiskaregatan and Östra Sjögatan. It has two parts.

**The pale yellow boarded range**, two storeys, to Fiskaregatan:
- nine axes of red-brown casements in white surrounds on both storeys;
- pilasters at the ends and between the axes;
- a dark plinth and a cornice;
- a tile roof with a snow rail and chimneys.

**The taller corner wing:**
- a mansard roof whose upright gable stands to Fiskaregatan, with two small windows;
- two axes on each storey below;
- corner pilasters with capitals;
- the Östra Sjögatan side plain.

The mesh keeps its name (`SM_Kvarnholmen_House_91970261`).

Panoramas are working references only. No pixel is used as a texture, and no panorama, depth or tile data was extracted.

## Sources

- **Outline:** `source/block58.json`, two zones cut at the measured joint (x 41.2). The wing's roof ring keeps the street edge upright and slopes the other sides in 1.8 m.
- **Google Street View**, April 2025, 90° vertical field of view, pitched 15–20° up (1148 × 1063 frames): three panoramas on Fiskaregatan ("51"). The review cameras are 322 (west), 323 (middle) and 324 (wing); 325 is an aerial view.

## Measurement

**Registration.** The three cameras are chained on four shared window edges, spaced as their GPS positions and anchored on both ends (x 20.41 and 48.63). Residuals are 0.1–0.8 m (the west anchor 0.47 m). The camera height is 2.03 m over the pavement.

| Feature | Measured (m) | Modelled (m) |
|---|---|---|
| Range axes (x) | upper 22.36 … 39.87 (nine); ground 22.12 … 40.15 | the same |
| Range heights | plinth 0.7; ground windows 1.57–2.64; upper 3.71–4.80; cornice 5.0–5.42 | the same, eaves 5.3, ridge 7.7 (estimate) |
| Wing | x 41.2–48.63; ground windows 1.37–2.51; upper 3.6–5.17; side eaves 5.8; gable windows 6.26–7.28; mansard break 7.7 at x 43.36 and 46.68 | the same, upper hip to 8.6 (estimate) |

## Verification

See `previews/block58-delivery.json`:
- every report passed;
- identical on two rebuilds;
- 73 floor samples and 69 capsule sweeps, no obstructions;
- calibration of 14 features: median 9 px, largest 30 px (the gable windows and the joint pilaster);
- passes 28–57 unchanged.

## Limitations

- **Estimates:** the mansard's upper hip, the Östra Sjögatan side and the rear.
- **Observed but not changed:** the house to the west on Fiskaregatan is green-boarded with a garage door, while the model shows a yellow rendered volume there.
