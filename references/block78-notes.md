# Pass 78: the 1887 house on Norra Långgatan

Pass 78 details the district volume 93192377 on the south side of Norra Långgatan, east of the pass 77 block. It is a cream rendered two-storey house of 1887:
- a granite plinth, four axes of green-framed casements over sunk panels on the ground floor, and the green carriage gate with its lattice transom at the west end;
- a band between the storeys and five upper windows;
- a cornice with a roof rail, and a boarded dormer with a pair of windows over the middle axis.

The mesh keeps its name (`SM_Kvarnholmen_House_93192377`). The meter cabinet and the lamp are omitted.

Panoramas are working references only. No pixel is used as a texture, and no panorama, depth or tile data was extracted.

## Measurement

One panorama on Norra Långgatan ("68") stands about 7.5 m from the front. It is resected on the house's east corner (x 265.6) at heading 152, and on its joint with the pass 77 block (x 253.6) at heading 202. The two headings agree on all window axes within 0.2 m. The base row lies at 0, with a camera 2.3 m high.

| Feature | Measured (m) | Modelled (m) |
|---|---|---|
| Window axes (x) | 264.12, 261.88, 259.71, 257.51; upper floor also 255.36 | the same |
| Gate (x) | 254.35–256.5, 0.52–3.15 | the same |
| Heights | plinth 0–0.52; ground windows 1.43–3.22; band 3.8–4.4; upper windows 4.52–6.30; cornice 7.35–7.9 | the same; roof to 9.6 (estimate) |

## Verification

See `previews/block78-delivery.json`:
- every report passed;
- identical on two rebuilds;
- 18 floor samples and 16 capsule sweeps, no obstructions;
- calibration of 9 features: median 8 px, largest 14 px;
- passes 28–77 unchanged.

## Limitations

- **The dormer** was brought forward after the first comparison hid it behind the cornice. Its depth is an estimate.
- **Estimates:**
  - the roof;
  - the yard side.
