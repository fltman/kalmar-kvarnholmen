# Pass 59: the green wooden house on Fiskaregatan

Pass 59 details the district volume 91970317 on Fiskaregatan, west of pass 58. The model had shown a yellow rendered volume here. It is in fact a green-boarded two-storey wooden house:
- vertical boarding with white pilasters at the corners and between the parts;
- six white casements upstairs (a narrow one at the east end) and four below;
- the black boarded gateway at the east end, under a white hood with a panel;
- a black plinth with three cellar windows and a white cornice;
- a tile roof with a snow rail and three boarded dormers.

The mesh keeps its name (`SM_Kvarnholmen_House_91970317`).

Panoramas are working references only. No pixel is used as a texture, and no panorama, depth or tile data was extracted.

## Sources

- **Outline:** `source/block59.json`, one zone. Pass 58's range counts as a 5.3 m neighbour.
- **Google Street View**, April 2025, 90° vertical field of view, pitched 20° up (1148 × 1063 frames): two panoramas on Fiskaregatan ("40" and "49"). The review cameras are 326 (gateway) and 327 (west); 328 is an aerial view.

## Measurement

**Registration.** Each panorama is anchored on one end (the joint with pass 58 at x 20.41; the west corner at 5.94), and their spacing follows the GPS positions. The two windows seen from both agree within 0.15 m. The camera height is 2.27 m over the pavement.

| Feature | Measured (m) | Modelled (m) |
|---|---|---|
| Upper axes (x) | 19.8 (narrow), 17.45, 14.88, 12.95, 9.6, 7.5 | the same |
| Ground | windows at 14.98, 12.74, 9.6, 7.5; gateway 19.91–17.31, to 2.57, hood 2.69–3.32 | the same (gateway 2.3 m) |
| Heights | plinth 0–1.1; ground windows 1.93–3.57; upper 4.38–5.85; eaves 6.05–6.3; dormer windows about 7.0–7.95 | the same, ridge 9.0 (estimate) |

## Verification

See `previews/block59-delivery.json`:
- every report passed;
- identical on two rebuilds;
- 33 floor samples and 29 capsule sweeps, no obstructions;
- calibration of 11 features: median 12 px, largest 25 px (the dormers);
- passes 28–58 unchanged.

## Limitations

- **Estimates:** the roof, the courtyard wings and the dormers' exact depth.
- **The two ground windows at the west end** read about 1 m apart in the two views. The model centres them under the upper windows.
