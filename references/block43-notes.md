# Pass 43: Södra Långgatan 49-59, the north side east of Östra Sjögatan

Pass 43 details the Södra Långgatan front of the district volume 91846978. The volume is the long block between Södra Långgatan, Proviantgatan and Storgatan. Its street front is late-20th-century infill in the old town's forms. From west to east:

- **The cream hotel range** (Kalmar Stadshotell's annexe, number 53):
  - a garage door and two storeys of windows under a roof terrace, with a mansard dormer;
  - a gabled four-storey middle with French balconies on two axes and a roundel in the gable;
  - an open arcade with the entrances;
  - a three-storey range beyond;
  - a banded ground floor under a band.
- **The ochre range:** ochre roughcast panels in cream frames round one or two windows, a stone quoin strip at its west end, a banded ground floor, a roof terrace.
- **The blue house** (number 55):
  - four storeys between cream pilasters, with bands between the storeys;
  - roundels over the third-storey windows and a front gable with a roundel;
  - a recessed entrance.
- **The grey house:** two storeys of grey roughcast with a pale strip round one upper window, a band, and a tile roof with roof windows.
- **The salmon corner range** (number 57):
  - a salmon ground floor, a cream band and a beige upper storey;
  - a front gable with two windows and a roundel, rising from the wall face;
  - a recessed entrance and a French balcony at the corner of Proviantgatan.

The Storgatan and Proviantgatan sides and the courtyard wings stay plain at the district height, under a tile roof. The mesh keeps its name (`SM_Building_91846978`).

Panoramas are working references only. No pixel is used as a texture, and no panorama, depth or tile data was extracted.

## Sources

- **Outline:** `source/district17.json` (91846978). The street ranges run 12 m deep and are split at the measured joints (x 103.9, 113.96, 123.4, 137.56, 144.48, 158.45, 164.8). The rest is the plain block.
- **Google Street View**, official imagery of April 2025, viewed at a vertical field of view of 90° (level and 25° up). Eight panoramas were used, "49" (two), "53", "48", "55", "57", "54" and "54" at the corner, ids in `previews/block43-delivery.json`'s source notes. Review cameras 257-266.

## Measurement

**Registration.** The eight cameras are chained along the street:
- 18 pairs of window edges seen from neighbouring panoramas;
- anchored at the building's west end (x 100.12, the joint with 91846951, from "49") and at the Proviantgatan corner (x 176.97, from "54");
- one common camera height (2.41 m) ties each camera's distance to its base row.

The pairs agree to 0.00-0.24 m. The cameras stand 4.1-4.8 m from the facade.

| Feature | Measured (m) | Modelled (m) |
|---|---|---|
| Hotel/ochre ranges | first-floor windows 4.03-5.36, second 6.68-8.04, third (gable part) 9.38-10.68; cornice 9.5; band 2.98 | the same |
| Hotel gable | apex 13.9; the flanking mansard's cornice 9.5 | the same |
| Ochre range ground floor | windows 0.61-2.38; cream range 0.94-2.38 | the same |
| Blue house | windows 1.19-2.50, 4.14-5.49, 6.92-8.25, 9.64-11.12; bands 3.33-3.42, 6.07-6.29; gable apex 14.55 | the same, eaves 11.9 |
| Grey house | windows 0.65-2.53 and 4.25-5.61; band 3.44-3.49; eaves 6.9 | the same |
| Salmon range | windows 1.10-2.41 and 4.27-5.60; salmon to 3.47, cream band to 4.27; gable windows 7.04-8.16, apex 10.4; plinth 0.85 | the same |

## Verification

- **Zones:** `previews/block43-zones.json`. Nine zones cover the outline (2,299 m²).
- **Build:** one mesh, 419,272 triangles, no zero-area UV triangles.
- **Repeatability:** identical on two rebuilds.
- **Passes 28-42 unchanged:** their meshes hash identically.
- **FBX audit:** clean.
- **Unreal:** 16 materials, Nanite, clean render buffers.
- **Collision:** 143 floor samples and 126 capsule sweeps, no obstructions.
- **Calibration:** `previews/block43-calibration.json`, 24 features in five views, compared as whole views at half scale: median 10 px, largest 20 px (about 0.2 m at these distances). This is coarser than the crop-by-crop readings of earlier passes.
- **Delivery:** `previews/block43-delivery.json`; every report has passed.

**Corrected against the calibration views:**
- **The ochre panels** first covered the second window of each pair; they are now cut at every opening.
- **The salmon ground floor and the cream band** were drawn as plain boxes over the openings; they now stop at them.
- **The salmon front gable:** the cornice ran across its foot; the gable now rises from the wall face.

## Limitations

- **Estimates:**
  - the arcade's depth;
  - the hotel's mansard dormers;
  - the roof terraces;
  - the roof windows;
  - the whole Storgatan and Proviantgatan sides.
- **The blue house's medallions** are simple rings.
- **Omitted:** the hotel's signs, the house numbers, the notices, the lamp posts.
