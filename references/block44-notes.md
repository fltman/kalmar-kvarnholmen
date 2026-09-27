# Pass 44: the stone corner house at Västra Sjögatan and Ölandsgatan

Pass 44 details the district volume 92412862, south of pass 39's yellow house, at the corner of Västra Sjögatan and Ölandsgatan:

- **The stone corner house** (17th century), in white roughcast between fluted pilasters on a grey plinth:
  - **On Ölandsgatan:**
    - five axes of tall dark casements in flat surrounds on both storeys, with basement grilles;
    - the sandstone portal over the third axis: a round-arched opening on steps, pilasters on pedestals, an entablature, and a crest (the date panel) with finials;
    - a moulded cornice;
    - a tile roof with two eyebrow dormers and two chimneys;
    - a stepped gable to the east.
  - **To Västra Sjögatan:** three axes under a curved baroque gable, with three small windows and a blind panel under its top. A bronze relief sits between the ground-floor windows.
- **The white house 2 Västra Sjögatan:**
  - a roughcast ground floor with a small window, the panelled door with a transom on three steps, and three windows;
  - a band, and four upper windows in a smooth upper storey;
  - the cornice and a tile roof.
- **The yellow wooden house on Ölandsgatan:**
  - boarding between white pilaster boards;
  - two windows with white shutters and the red door with a transom;
  - a tile roof hipped all round, with a segmental dormer.
- **The grey board gate** between the corner house and the yellow house.
- **The courtyard wings:** plain and estimated.

The mesh keeps its name (`SM_Kvarnholmen_House_92412862`). Panoramas are working references only. No pixel is used as a texture, and no panorama, depth or tile data was extracted.

## Sources

- **Outline:** `source/district17.json` (92412862). Zones:
  - the corner house, x -29.3 to -12.6 and y -128.55 to -141.3;
  - the white house, to y -116.7 and 7 m deep;
  - the yellow house, x -9 to 2.3;
  - the courtyard wings (the rest).
- **Google Street View**, April 2025, 90° vertical field of view:

| Panorama | Id | Camera | Used for |
|---|---|---|---|
| "23 Ölandsgatan" | VwT5iylO-D6gWXOw4-4gQQ | 268 (pitch 5°), 269 (30°) | the corner house's Ölandsgatan front, the portal, the dormers |
| "25 Ölandsgatan" | PCba0AEbGS3ErCwy_Pt4hg | 270 | the east end, the stepped gable, the gate, the yellow house |
| "2 Västra Sjögatan" | (at 56.6630021 N, 16.366042 E) | 271 | the white house and the joint |
| "3 Västra Sjögatan" | H5sPRVMTssmXmcBUV_hcFw | 272, 273 (30°) | the west gable |

## Measurement

**Registration**, one chain per street:

- **Ölandsgatan:**
  - the portal's and two windows' edges and a downpipe, seen from both panoramas;
  - anchored on the west corner (x -29.3), the corner house's east end (x -12.7) and the yellow house's east end (x 2.3);
  - pairs within 0.12 m, anchors within 0.02 m;
  - the cameras stand 7.7 and 9.2 m out, at heights of 2.36 and 2.51 m.
- **Västra Sjögatan:**
  - the gable house's north pilaster and two windows, seen from both panoramas;
  - anchored on the joint with the green wooden house (y -116.7) and the south corner (y -141.0);
  - pairs within 0.11 m;
  - the cameras stand 6.4 m out, 2.51 m high.

| Feature | Measured (m) | Modelled (m) |
|---|---|---|
| Corner house, Ölandsgatan | ground windows (surrounds) 1.76-4.16; upper 6.06-8.33; plinth 0.52; cornice 8.9-9.8 on the plane | windows 1.90-4.08 and 6.12-8.26; cornice top 9.5 |
| Portal | opening 1.47 wide, springing about 3.0, crown 3.8; entablature to 4.1; crest to 5.9 | the same |
| Axes (x) | -27.74/-26.10, -24.82/-23.17, portal -22.52/-19.77, -18.84/-17.00, -15.94/-14.42; east end -12.7 | the same |
| West gable | cornice 9.2-9.5; windows 10.2-11.8; apex 17.9 | the same |
| White house | ground windows 2.0-4.25 (surrounds); door 0.12-4.25 with a transom; band 4.97-5.1; upper 5.88-8.19; cornice 8.8-9.4 | the same, eaves 9.0 |
| Yellow house | x -8.72 to 2.29; windows 1.26-2.87 with shutters; door 0.94-2.87; eaves 4.4-4.7; dormer to 6.15 | the same |

## Verification

- **Zones:** `previews/block44-zones.json`. Four zones cover the outline (560.7 m²).
- **Build:** one mesh, 102,929 triangles, no zero-area UV triangles.
- **Repeatability:** identical on two rebuilds.
- **Passes 28-43 unchanged:** their meshes hash identically.
- **FBX audit:** clean.
- **Unreal:** 14 materials, Nanite, clean render buffers.
- **Collision:** 150 floor samples and 140 capsule sweeps, no obstructions.
- **Calibration:** `previews/block44-calibration.json`, 23 features in four views, compared as whole views: median 10 px, largest 20 px (about 0.2 m).
- **Delivery:** `previews/block44-delivery.json`; every report has passed.

**Corrected against the calibration views:**
- **The west gable** first rose as a plain curve over the whole width; it now has the baroque outline drawing in to a narrow top.
- **The gable windows** are now larger and closer together.
- **The white house** is split from the corner house at the measured joint (y -128.55), not at OSM's vertex (y -134.1).

## Limitations

- **The east gable's steps** follow the pitched view only roughly.
- **The portal's crest** and the bronze relief are simplified; the inscription is omitted.
- **Estimates:** the courtyard wings and the roofs' far slopes.
