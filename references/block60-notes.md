# Pass 60: Fiskaregatan 36 and the beige house with the apothecary

Pass 60 details the Fiskaregatan range of the district volume 91856608, a block-sized volume. The range runs from the passage by pass 59 to the Västra Sjögatan corner and holds two houses.

**The grey roughcast house** (number 36), with its gambrel gable to the street:
- the arched door in a sandstone surround, and two windows beside it;
- a band, four windows upstairs and four in the gable;
- white edge boards along the gable, and a granite plinth.

**The beige two-storey house:**
- six axes of white casements in flat surrounds on both storeys;
- a band and a granite plinth;
- a tile roof with three dark-red dormers and a snow rail;
- at the Västra Sjögatan corner, the apothecary's bay with an arched portal in a stone surround.

The block's Västra Sjögatan and Norra Långgatan ranges keep the district height of 7.1 m for later passes. The mesh keeps its name (`SM_Building_91856608`).

Panoramas are working references only. No pixel is used as a texture, and no panorama, depth or tile data was extracted.

## Sources

- **Outline:** `source/block60.json`, three zones:
  - `gr`, the grey house: x 0.77 to -8.0, to y 124.5;
  - `bg`, the beige house: to the corner;
  - `rs`, the rest.
- **Google Street View**, April 2025, 90° vertical field of view, pitched 20° up (1148 × 1063 frames): three panoramas on Fiskaregatan ("36" and "47"). The review cameras are 329 (grey), 330 (beige) and 331 (corner); 332 is an aerial view.

## Measurement

**Registration.** The three cameras are chained on eight shared edges (the joint, windows, the corner bay's pilaster), spaced as their GPS positions and anchored on the Västra Sjögatan corner (x -26.15). Residuals are within 0.17 m, the camera height is 2.57 m, and the cameras stand 7–7.4 m out.

**Method.** From this pass on, positions in the pitched views are read on each feature's own row. The pitched view's keystone moves a vertical edge's image across the rows. Passes 53–59 read positions on the horizon row, which put their ground-floor openings up to about 0.3 m off. Their calibrations show 10–30 px on the ground rows.

| Feature | Measured (m) | Modelled (m) |
|---|---|---|
| Grey house | east edge 0.6 (ground); joint about -8.0; door 0.2–3.0 at x 0.19 to -1.53; ground windows 1.2–2.72; band 3.66–3.94; upper 4.85–6.65; gable windows 7.82–9.36; side eaves 8.15; break 10.75; apex 12.37 | the same (break inset 1.05, apex 12.4) |
| Beige house | axes -9.70 … -20.64 (six); ground windows 0.93–2.96; band 3.73–4.01; upper 4.91–6.72; eaves 7.33–7.61; dormer windows 8.1–9.1; corner bay from -22.1 with the portal (x -23.04 to -24.64, to 3.23) | the same, eaves 7.45 |

## Verification

See `previews/block60-delivery.json`:
- every report passed;
- identical on two rebuilds;
- 79 floor samples and 72 capsule sweeps;
- one obstruction, street furniture on Västra Sjögatan, with a verified detour;
- calibration of 16 features: median 10 px, largest 65 px (the grey house's east edge at the gable, and its gambrel break at 50 px);
- passes 28–59 unchanged.

## Limitations

- **The grey house's gable** reads wider in the panorama than the OSM front allows (its east edge and break about 1 m further out). The model keeps the OSM line.
- **Estimates:**
  - the roofs;
  - the block's Västra Sjögatan and Norra Långgatan ranges (district height);
  - the passage between the grey house and pass 59.
- **Omitted:** the apothecary's sign and posters.
