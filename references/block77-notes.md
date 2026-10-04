# Pass 77: the red cottage and the yellow apartment block on Norra Långgatan

Pass 77 details the district volumes 93192402 and 93192406 on the south side of Norra Långgatan, east of pass 75:
- **The red boarded cottage** with its gable to the street: grey weathered corner and barge boards, two yellow-framed windows below and one in the gable.
- **The yellow rendered apartment block:**
  - a grey plinth with cellar windows and a raised ground floor;
  - white-framed windows, and the recessed entrance with the stair window over it;
  - recessed loggias with white balcony fronts at both ends;
  - a cornice and a tile roof.
- **The iron gate** between the cottage and the pass 75 range.

The meshes keep their names (`SM_Kvarnholmen_House_93192402`, `…_93192406`). The meter cabinet and the lamp are omitted.

Panoramas are working references only. No pixel is used as a texture, and no panorama, depth or tile data was extracted.

## Measurement

One panorama on Norra Långgatan ("62") stands about 7.7 m from the fronts. It is resected on both corners of the cottage (x 229.1 and 224.3). Its base row lies at 0, with a camera 2.3 m high. A second heading along the block puts the block's east end at x 253.0, within 0.5 m of the district outline.

| Feature | Measured (m) | Modelled (m) |
|---|---|---|
| Cottage | windows 227.24, 225.71 at 1.28–2.37; gable window 226.53 at 3.53–4.83; eaves about 4.45; apex 6.04 | the same |
| Block | loggias 229.6–233.45 and 248.7–252.6; windows 236.0, 238.55, 246.9 (both floors) and 242.34 (upper); entrance 241.2–243.0 | the same |
| Block heights | plinth 0–1.0; ground windows 2.16–3.82; upper windows 5.05–6.69; cornice 7.82 | the same; roof to 10.2 (estimate) |

## Verification

See `previews/block77-delivery.json`:
- every report passed;
- identical on two rebuilds;
- 47 floor samples and 43 capsule sweeps, no obstructions;
- calibration of 9 features: median 10 px, largest 16 px;
- passes 28–76 unchanged.

## Limitations

- **The block's far windows** are read at a grazing angle (about ±0.3 m).
- **Estimates:**
  - the roofs;
  - the loggia depth;
  - the yards.
