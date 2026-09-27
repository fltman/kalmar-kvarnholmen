# Pass 61: Norra Långgatan 41

Pass 61 details the district volume 91885539 on the corner of Norra Långgatan and Östra Sjögatan: the pale yellow two-storey house at Norra Långgatan 41.

**To Norra Långgatan:**
- seven axes of red-brown casements in white surrounds, the ground windows over roughcast panels;
- white pilasters at the corners and flanking the middle axis;
- the carved double door (41) with a glazed transom, up a step;
- a sill band, a grey plinth and a cornice;
- a red sheet-metal gambrel roof with an ornate arched dormer.

**To Östra Sjögatan:** the gambrel gable, with four ground windows, two pairs of windows upstairs and three small windows in the gable.

The mesh keeps its name (`SM_Kvarnholmen_House_91885539`).

Panoramas are working references only. No pixel is used as a texture, and no panorama, depth or tile data was extracted.

## Measurement

**The overview.** The overview panorama at the Östra Sjögatan crossing ("44 Norra Långgatan") was resected on three corners of the house. Residuals are up to 22 px; the camera stands at (48.3, 64.4), 2.13 m high. Positions were read on each feature's own row.

**The close panorama.** The close panorama facing the door ("43 Norra Långgatan") stands 4.1 m from the facade. Its GPS position was about 1 m off along the street, so it was placed on the door measured in the overview. Its window and pilaster positions then agree with the overview within about 0.4 m. Heights come from this view.

| Feature | Measured (m) | Modelled (m) |
|---|---|---|
| South axes (x) | 60.5, 63.9, 67.0, 70.5, door 73.2, 76.4, 80.5; pilasters at 69.0–69.6 and 71.3–71.8 | the same |
| South heights | plinth 0.5–0.65; panels to 1.27; ground windows 1.35–2.85; band 3.76–3.99; upper windows 4.0–5.9; cornice 6.14–6.85; roof edge 7.1–7.3; dormer window 8.0–9.9 | the same, eaves 7.1 |
| Gable (y) | ground 82.4, 80.4, 77.3, 75.1; upper pairs 82.0/80.8 and 76.9/75.5; gable windows 81.45, 78.9, 76.2 at about 7.5–9.1; break about 9.4–9.8; apex about 10.8 | the same (break 9.6) |

## Verification

See `previews/block61-delivery.json`:
- every report passed;
- identical on two rebuilds;
- 66 floor samples and 64 capsule sweeps, no obstructions;
- calibration of 14 features: median 11 px, largest 20 px (the gable break);
- passes 28–60 unchanged.

## Limitations

- **Estimates:** the roof's rear slope, the courtyard sides and the east wall.
- **The gable's heights** come from the oblique overview only.
- **Omitted:** the traffic signs and the street-name plates.
