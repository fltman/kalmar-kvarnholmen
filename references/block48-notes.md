# Pass 48: the pale yellow house with the gateway on Ölandsgatan

Pass 48 details the district volume 92379261 on the north side of Ölandsgatan, west of pass 47. It is a pale yellow two-storey house with:
- three ground-floor and four upper casements, with brown frames in flat white surrounds;
- the gateway passage at the east end, with a white lintel beam and white reveals, and an iron gate just behind the front;
- a buff plinth, a white cornice, and a dark sheet roof with one dormer and a snow rail.

The courtyard and rear sides stay plain at the district height. The mesh keeps its name (`SM_Kvarnholmen_House_92379261`).

Panoramas are working references only. No pixel is used as a texture, and no panorama, depth or tile data was extracted.

## Sources

- **Outline:** `source/block48.json` (zone `yh`, from 92379261).
- **Google Street View**, April 2025, 90° vertical field of view: two panoramas on Ölandsgatan, one in front of the gateway and one in front of the west joint. The review cameras are 288 (west) and 289 (gateway); 290 is an aerial view.

## Measurement

**Registration.** The two cameras are chained on four shared window edges and the gateway, and anchored on both joints. The cameras stand 5.35–5.50 m from the facade, at a height of 2.11 m.

| Feature | Measured (m) | Modelled (m) |
|---|---|---|
| Upper windows | 4.43–6.33 (surrounds) | the same |
| Ground windows | 1.57–3.30 (surrounds) | the same |
| Gateway | x -144.65 to -141.79; opening to 3.19, beam to 3.6 | the same |
| Plinth | 0.59 | 0.59 |
| Eaves | gutter and cornice 6.6–7.2 | eaves 7.0 |
| Dormer | x about -147.4, front about 0.4 m behind the wall line (from the two views) | the same |

## Verification

See `previews/block48-delivery.json`:
- every report passed;
- 20,133 triangles in one mesh;
- identical on two rebuilds;
- 39 floor samples and 36 capsule sweeps, no obstructions;
- calibration of 13 features: median 6 px, largest 46 px;
- passes 28–47 unchanged.

The largest deviation is the dormer. The two panoramas place it differently, about 40 px each way, so the model splits the difference.

## Limitations

- **Estimates:** the roof, its railing, the passage's far end and the courtyard sides.
- **Omitted:** the company sign, the parking sign, the house plaque and the utility cabinet.
- **The white stone house to the west** (in 92379259's frontage) is not in OSM's front and is not modelled here; the neighbouring generic volume stays as it was.
