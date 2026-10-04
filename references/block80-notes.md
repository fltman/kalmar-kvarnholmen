# Pass 80: the north side of Norra Långgatan east of pass 76

Pass 80 details the next stretch of the north side of Norra Långgatan, from the pass 76 white house eastwards:
- **The red boarded wall** with a brown double gate and a stained-glass window.
- **The olive boarded gable house** (90859833), with red-brown trim.
- **The long white two-storey boarded house** with a tile roof and a red dormer, and its grey-white gabled annex with a garage door. OSM maps this house only as the untagged outer way 90859904 of a multipolygon, and the district import dropped it, so the model had an empty lot here. It is a new mesh, `SM_Kvarnholmen_House_90859904`.
- **The red boarded gable house** (90859843), with white trim and window boxes.
- **The small white cottage with blue trim** (90859883), with a blue boarded fence and a red gate beside it. The strips beside the cottage are released as open ground (22.6 m² in all).

Panoramas are working references only. No pixel is used as a texture.

## Measurement

The houses are measured from the pass 77 and pass 78 panoramas ("62" and "68"), looking north across the street at about 3.4 m.

The base rows put these fronts about 0.8 m behind the district outline. As in pass 76, the fronts are kept on the outline and each camera is moved by that amount, which leaves the cameras 1.95 m above these houses.

Positions read from two headings per camera agree within about 0.2 m, with one exception. The red house's west edge reads 1.4 m east of the outline in both views; its joint with the white annex is set at the measured x 256.3.

| House | Measured (m) |
|---|---|
| Gate wall | x 229.4–233.9, 2.2 high; gate 230.43–232.17; glass window 232.27–232.93 |
| Olive house | gable front 233.9–239.05; windows 235.1 and 237.0 at 0.73–1.78 and 2.66–3.8; apex about 5.1 |
| White house | 239.05–254.5; windows 241.63, 243.97, 246.62, 251.21, 252.86; door 249.5; eaves about 4.9 |
| Annex | 254.5–256.3; garage door 254.6–256.1; gable apex about 6.2 |
| Red house | 256.3–260.9; windows 257.95 and 259.55 at 0.82–2.0 and 2.87–4.12; gable window; apex 6.0 |
| Cottage | 262.3–266.3; window 263.66–264.88 at 0.49–1.84; eaves 1.45; apex 2.8 |

## Verification

See `previews/block80-delivery.json`:
- every report passed;
- identical on two rebuilds;
- 36 floor samples and 28 capsule sweeps. The only obstruction is the white house's front steps, which have a verified detour 1.25 m out.
- passes 28–79 unchanged.

## Limitations

- **The brown boarded house** behind the gate wall is not modelled.
- **Estimates:**
  - the roofs;
  - the white house's dormer position;
  - the depths;
  - the yard sides.
