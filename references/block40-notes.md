# Pass 40: the white corner house at Södra Långgatan and Östra Sjögatan

Pass 40 details the district volume 92412846 on the south side of Södra Långgatan, east of pass 39's grey house, at the corner of Östra Sjögatan (numbers 41-43):

- **A white-rendered two-storey stone house**, taller than the district volume (the cornice's top at 9.1 m, not 7.1):
  - on Södra Långgatan ten window axes of blue-grey casements, two leaves of three panes each with the top panes under a transom, set in plain reveals;
  - a sandstone portal with a transom light over a diamond-panelled door, on three stone steps;
  - a grey plinth, three black downpipes, iron fleur-de-lis wall anchors on every pier in two rows (between the storeys and under the cornice), quoins at the street corner;
  - a moulded brown-grey cornice;
  - a low black sheet-metal roof, hipped towards Östra Sjögatan, with two white chimneys.
- **On Östra Sjögatan** four upper windows and three lower ones, the anchors, the quoins, and a small white cabinet house at the corner.

The house is a district volume (`SM_Building_92412846`); its outline comes from `source/district17.json` and the mesh keeps its name.

Panoramas are working references only. No pixel is used as a texture, and no panorama, depth or tile data was extracted.

## Sources

- **Outline:** `source/district17.json` (92412846). The neighbours are pass 39's grey house to the west (`source/block39.json`), the district volumes 92412854 and 92412873 (the Nordstjernan brewery) behind.
- **Google Street View**, official imagery of April 2025, viewed in the browser at a vertical field of view of 75° (screenshots 1200×706):

| Panorama | Id | Camera | Used for |
|---|---|---|---|
| "41 Södra Långgatan" | s27rRh9_-DdYDQoqsUpaSQ | 235 (heading 152°, level) | the joint with the grey house, the three western axes |
| "40 Södra Långgatan" | QiGqlLZY0ThKhluoa8QCxg | 236 (heading 152°, level), 237 (pitch 25°) | the middle axes, the upper storey, the cornice and the chimneys; the corner at heading 110° |
| "43 Södra Långgatan" | 54AuXEeSudlqX1sXxnYKtQ | 238 (heading 152°, level), 239 (heading 112°, pitch 5°) | the portal and the eastern axes; the corner |
| "3 Östra Sjögatan" | jCZmk5759ASXNcai82wdcg | — (headings 205° and 285°, 90° field of view) | the Östra Sjögatan front, seen from 3.6 m |

## Measurement

**Registration.** One bundle adjustment of "40", "41" and "43" on the joint with the grey house (x 15.05), the street corner (x 47.23, seen from "40" and "43") and the edges of eight windows and the portal seen from two panoramas each: 31 bearings, residuals up to 1.5 mrad (below 1 px). The cameras stand 6.35-6.52 m from the facade, on one line; the reported positions were 0.8-1.4 m off. "3 Östra Sjögatan" is resected on the corner and the joint with the brewery (two points only; its readings are estimates).

**Camera heights** from the base rows: 2.52 m ("40"), 2.51 m ("43"); "41" has no base in view (2.50 m assumed).

| Feature | Measured (m) | Modelled (m) |
|---|---|---|
| Ground-floor windows | frames 1.44-3.55 ("40"), 1.51-3.65 ("43"), 1.33-1.45 wide | 1.47-3.60 |
| Upper windows | frames 5.48-7.60 ("40", pitched view) | 5.52-7.62 |
| Plinth | 0.56 ("40"), 0.60 ("43") | 0.58 |
| Portal | stone surround 35.46-37.36, top 3.81; opening 1.25 wide to 3.59; threshold 0.59 | the same |
| Cornice | foot 8.68, top 9.50 on the plane (its top 9.12 at a 0.4 m projection); the roof's edge 9.86 on the plane | cornice 8.70-9.12, 0.4 m out; the roof from 9.15 |
| Anchors | 7.98-8.56 under the cornice (plane); between the storeys at about 4.3-4.9 | 7.95-8.52 and 4.20-4.77 |
| Chimneys | tops seen just over the cornice from "40" | at x 30.0 and 35.4, 2.2 m behind the front, tops 13.1 |

**Axes** (x of the frames' edges, west to east): 15.99-17.32, 18.39-19.73, 20.81-22.20, 23.91-25.30, 27.43-28.83, 29.94-31.39, 32.82-34.23, the portal 35.46-37.36, 38.56-39.98, 41.55-42.97, 44.43-45.86; the corner 47.23.

## Verification

- **Zones:** `previews/block40-zones.json`. One zone covers the outline (396.8 m², 0.15 m² not zoned).
- **Build:** one mesh, 116,530 triangles, no zero-area UV triangles; 76 zero tangent frames repaired at export, as in earlier passes.
- **Repeatability:** two scoped rebuilds gave identical geometry, UVs and material slots.
- **Passes 28-39 unchanged:** their meshes in the saved scene hash identically to their repeatability reports.
- **FBX audit:** no zero-length or non-finite normals, tangents or binormals.
- **Unreal:** 11 materials with normal and roughness maps; the mesh imported with Nanite; clean render buffers.
- **Collision:** 140 floor samples and 135 capsule sweeps. The portal's steps and the cabinet house block the inner walking line, as they should, and it passes round them 0.8 m further out (two verified detours).
- **Calibration:** `previews/block40-calibration.json`, 28 features in five views: median 2.0 px, largest 9 px (the western window's top from "41", whose camera height is assumed); 27 of the 28 within 8 px.
- **Delivery:** `previews/block40-delivery.json`; every report has passed.

**Corrected against the calibration views:**
- **The wall anchors** under the cornice first stood over the windows; the panoramas put them on the piers, like the lower row. The two beside the portal were missing.
- **Two downpipes** stood 0.5 m and 0.25 m from their positions; **the chimneys** were too wide; **the quoins** too dark and too proud.

## Review shots

- [the western axes and the grey house's joint](../previews/block40-235_Block40_Cal_West.png)
- [the middle](../previews/block40-236_Block40_Cal_Middle.png) and [its upper storey and cornice](../previews/block40-237_Block40_Cal_Middle_Roof.png)
- [the portal](../previews/block40-238_Block40_Cal_Portal.png)
- [the corner](../previews/block40-239_Block40_Cal_Corner.png)
- [overview](../previews/block40-240_Block40_Aerial.png)

## Reproduction

`KALMAR_GEO=… python3 scripts/prepare_block40.py`; Blender with `scripts/rebuild_block40.py` (twice for the geometry audit) and the audits; Unreal with `resume_block40.py -HeroIdle`, then `{"execute":"validate_block40.py"}`. Backup: `source/backups/block40/`.

## Limitations

- **The roof** is not seen from the street; its pitch (about 28°) only has to stay under the sight line over the cornice. The chimneys' depth behind the front is assumed; their tops are fitted to the rays.
- **The Östra Sjögatan front** rests on one close panorama resected on two points; its window positions are estimates, and the lower window by the cabinet house is not modelled.
- **The rear** (the courtyard side) is plain, with estimated windows.
- **Omitted:** the traffic sign, the notices in the windows and on the door, the house number plates.
