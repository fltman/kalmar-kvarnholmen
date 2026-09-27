# Pass 57: the grey wooden house on Norra Långgatan

Pass 57 details the district volume 91970300 on the corner of Norra Långgatan and Östra Sjögatan. It is a grey-boarded two-storey wooden house.

**To Norra Långgatan:**
- twelve upper casements in white surrounds with toothed sill boards;
- a string course;
- ground-floor casements over boarded panels in white frames;
- the red glazed double door (number 39) up three steps;
- a dark boarded gateway at the west end;
- a rendered plinth with cellar vents, a cornice, and a tile roof with chimneys.

**The Östra Sjögatan end** keeps a plain two-storey rhythm; it was seen only obliquely.

The mesh keeps its name (`SM_Building_91970300`).

Panoramas are working references only. No pixel is used as a texture, and no panorama, depth or tile data was extracted.

## Sources

- **Outline:** `source/block57.json`, one zone.
- **Google Street View**, April 2025, 90° vertical field of view, pitched 15° up (1148 × 1063 frames):
  - two panoramas on Norra Långgatan ("39"), facing the house;
  - one at "44", facing the Östra Sjögatan corner.

  The review cameras are 318 (west), 319 (door) and 320 (corner); 321 is an aerial view.

## Measurement

**Registration.** The three cameras are chained on two shared window edges, spaced as their GPS positions and anchored on the Östra Sjögatan corner (x 48.28). The corner view's windows agree with the door view's within 0.2 m. The camera height is 2.13 m over the pavement, and the cameras stand 4.6–5.3 m out.

| Feature | Measured (m) | Modelled (m) |
|---|---|---|
| Upper axes (x) | 21.33, 24.37, 27.10, 28.98, 30.58, 32.33, 35.07, 37.80, 40.10, 42.12, 44.81, 46.75 | the same |
| Ground axes (x) | 24.15, 27.32, 29.48, 31.87, door 35.05, 38.17, 40.25, 42.10, 44.80, 46.72; gateway 20.65–21.80 | the same |
| Heights | plinth 0.61–0.75; panels 0.75–1.2; ground windows 1.23–2.65; door 0.84–2.57; string course 2.95–3.35; upper windows 3.80–5.30; cornice 5.7–6.35; roof edge 6.5–6.8 | the same, eaves 6.5, ridge 8.6 (estimate) |

## Verification

See `previews/block57-delivery.json`:
- every report passed;
- identical on two rebuilds;
- 92 floor samples and 90 capsule sweeps, no obstructions;
- calibration of 13 features: median 10 px, largest 25 px (the roof edge);
- passes 28–56 unchanged.

## Limitations

- **The upper axes are irregularly spaced** (1.6–3.0 m). They were read one by one, and the west ones from one view only.
- **Estimates:** the Östra Sjögatan end, the roof and the rear.
- **Omitted:** the bicycle stands, the utility box and the house number.
