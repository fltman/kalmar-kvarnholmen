# Pass 67: Norra Långgatan 51

Pass 67 details the district volume 91885524 on the north side of Norra Långgatan, east of pass 66 (number 49). It is a yellow boarded two-storey house:
- vertical board-and-batten cladding between six white pilasters with bases and capitals;
- white-framed casements in white surrounds, with a narrow pair in the east bay;
- the green double door up three stone steps under a white hood;
- a grey plinth with glass-block cellar windows under a white ledge;
- a white profiled cornice, and a red tile saddle roof with an arched red dormer.

The mesh keeps its name (`SM_Kvarnholmen_House_91885524`). The window awnings, the lamp and the shop sign are omitted.

Panoramas are working references only. No pixel is used as a texture, and no panorama, depth or tile data was extracted.

## The outline

The house stands free of its neighbours:
- **To the west**, a fenced gap of about 0.5 m separates it from number 49. The gap stays in the zone and is drawn as a shadowed recess behind a white fence, because pass 66 draws number 49's east wall only above the district height there.
- **To the east**, the district outline runs on to x 152.04 over a fenced yard gate. That strip (25 m²) is released as open ground. No other building touches it.

## Measurement

Two panoramas on Norra Långgatan were used:
- **The pass 66 panorama at number 50**, whose position is already fixed, looks along the street. It puts the plinth ends at x 134.8 and about 150.0, with both ends at the same base height.
- **The close panorama facing the house** (number 51) is resected on those two corners. It reads the pilasters and the windows. Its pilaster edges agree with the view along the street within 0.15 m.

The base row lies 0.25 m below the first assumption, so the cameras stand 2.55 m high.

| Feature | Measured (m) | Modelled (m) |
|---|---|---|
| Pilasters (x) | 135.1, 139.07, 141.75, 144.38, 146.85, 149.6 | the same, 0.56–0.6 wide |
| Window axes (x) | 137.1, 140.45, 143.1, 148.2 (narrow); upper floor also 145.7 | the same |
| Door (x) | 144.96–145.93 | centre 145.45, 1.05 wide |
| Heights | plinth 0–1.0; ground windows 1.71–3.40; upper 4.49–6.28; cornice 6.5–7.0 | the same; eaves 6.7, ridge 10.1 (estimate) |

## Verification

See `previews/block67-delivery.json`:
- every report passed;
- identical on two rebuilds;
- 25 floor samples and 23 capsule sweeps, no obstructions;
- calibration of 9 features: median 10 px, largest 14 px;
- passes 28–66 unchanged.

## Limitations

- **The east corner** is read at a grazing angle from the view along the street (±0.5 m); the close view was resected on it.
- **Estimates:**
  - the roof pitch and the ridge;
  - the rear wall.
