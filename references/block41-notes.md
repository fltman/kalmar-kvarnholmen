# Pass 41: the north range, Södra Långgatan 39-43

Pass 41 details the district volume 92412838, the 50 m range on the north side of Södra Långgatan opposite passes 39 and 40, from the garage yard to Östra Sjögatan. It is a white-rendered two-storey range in two builds on one grey plinth, under one string course, one moulded cornice and a copper-green sheet roof:

- **The western build** (dated 1940 on the wall):
  - two garages with boarded doors under glazed transoms;
  - two doors in stone surrounds with recessed panels over them;
  - rectangular windows in flat surrounds, and one wide window of twelve lights with bars behind the glass;
  - a lunette gable with a scrolled outline, standing on the cornice.
- **The eastern build** (dated 1888), from a quoin strip:
  - segmental-headed ground-floor windows in surrounds;
  - a rusticated round-arched portal with voussoirs and a keystone over a glazed double door on three steps (number 43);
  - a baroque central gable with a cartouche, scroll volutes and a segmental-headed window.
- **Both:** sixteen upper windows (two leaves under a transom) in flat surrounds with aprons down to the string course; iron wall anchors, black downpipes, quoins at both ends.
- **The Östra Sjögatan end** repeats the eastern build's storeys (five axes).

The mesh keeps its district name (`SM_Building_92412838`).

Panoramas are working references only. No pixel is used as a texture, and no panorama, depth or tile data was extracted.

## Sources

- **Outline:** `source/district17.json` (92412838). Three zones: the front range (to y -61.3), the east wing on Östra Sjögatan and the courtyard wing (plain, at the district height).
- **Google Street View**, official imagery of April 2025, viewed in the browser at a vertical field of view of 90° (the camera stands only 4.3-5.1 m from this facade):

| Panorama | Id | Camera | Used for |
|---|---|---|---|
| "43 Södra Långgatan" | 54AuXEeSudlqX1sXxnYKtQ | 241 (level), 242 (pitch 20°) | the portal, the central gable, the eastern end (heading 15°) |
| "40 Södra Långgatan" | QiGqlLZY0ThKhluoa8QCxg | 243 (level) | the 1888 build, the quoin strip; both gables in the pitched view |
| "41 Södra Långgatan" | s27rRh9_-DdYDQoqsUpaSQ | 244 (level), 245 (pitch 20°) | the 1940 build, the wide window, the lunette gable |
| "39 Södra Långgatan" | HebU0W3fMDCLMfT2Vtq9hA | 246 (level) | the garages and the first door |
| "37 Södra Långgatan" | ZO5ckbm0mBm-lpTCBMPnJA | — | the western end (the quoins by the garage yard) |
| Östra Sjögatan | foizEM9g0Ep5oeyvrTLoMg | — | the Östra Sjögatan end (estimated positions) |

## Measurement

**Registration.** The panoramas are those of passes 39 and 40, registered there on the south side. Their positions put the north facade 1.5 m too far away: window widths then grew towards the edges of the 90° views. The distances were re-solved as a chain:
- 18 pairs of window edges seen from two neighbouring panoramas must fall at the same x;
- the building's west end (x -2.9, seen from "37") and east corner (x 47.11, seen from "43") anchor the chain;
- one common height (the string course's top, 4.60 m) ties each camera's distance to its base row.

The fit leaves pairs 0-0.22 m apart and the ends 0.02-0.06 m. The cameras stand 4.30-5.11 m from the facade at heights of 2.46-2.54 m. The real facade runs 0.3-0.8 m north of the OSM line; the model keeps the OSM line, and the review cameras keep their measured distance from the model's wall face.

**Projecting parts triangulated from two panoramas** (gaps 0.02-0.20 m):

- **The central gable** ("43" and "40"):
  - window 9.60-10.45, 0.13 m behind the wall face;
  - moulded ledge 10.62-10.78, about 0.45 m out;
  - crown 11.78, 0.56 m out.
  - Read on the facade plane, the crown had come out at 13.15.
- **The lunette gable** ("41" and "40"):
  - its foot and the lunette's base 8.43-8.46, and the lunette's crown 8.78, all 0.3-0.4 m in front of the wall: the gable stands on the cornice.

| Feature | Measured (m) | Modelled (m) |
|---|---|---|
| Plinth | 0.60-0.79 | 0.75 |
| Ground windows (1888) | 1.58-3.15, crowns 3.30-3.38; 0.94-1.07 wide | 1.58-3.20, crown 3.38 |
| Ground windows (1940) | 1.45-3.58 | the same |
| Wide window | 15.37-19.59, 1.50-3.59 | the same |
| Portal | stone 33.65-37.24; opening 34.45-36.36 from 0.75; keystone top 3.98 | the same |
| String course | 4.55-4.63 | 4.50-4.62 |
| Upper windows | 5.22-5.29 to 7.36-7.61 | 5.25-7.55 |
| Cornice | underside 7.99-8.14; the eaves line in the pitched views | 8.0 to a corona 0.45 m out, top 8.75 |
| Gables | as triangulated above; the lunette gable's top 10.2 (from one view, at its face) | the same |

## Verification

- **Zones:** `previews/block41-zones.json`. Three zones cover the outline (670.2 m²).
- **Build:** one mesh, 179,388 triangles, no zero-area UV triangles. Many zero tangent frames were repaired at export (the arches and volutes); the FBX audit is clean.
- **Repeatability:** two scoped rebuilds gave identical geometry, UVs and material slots.
- **Passes 28-40 unchanged:** their meshes in the saved scene hash identically to their repeatability reports.
- **FBX audit:** no zero-length or non-finite normals, tangents or binormals.
- **Unreal:** 12 materials with normal and roughness maps; Nanite; clean render buffers.
- **Collision:** 190 floor samples and 182 capsule sweeps. Two verified detours: the portal steps, and street furniture on Östra Sjögatan.
- **Calibration:** `previews/block41-calibration.json`, 25 features in four views: median 3 px, largest 18 px; 23 of the 25 within 8 px. The two outliers are on the gables:
  - the central crown, 14 px;
  - the lunette gable's position along the street, 18 px (about 0.4 m).
- **Delivery:** `previews/block41-delivery.json`; every report has passed.

## Review shots

- [the portal](../previews/block41-241_Block41_Cal_Portal.png) and [the central gable](../previews/block41-242_Block41_Cal_Portal_Roof.png)
- [the 1888 build](../previews/block41-243_Block41_Cal_1888.png)
- [the 1940 build](../previews/block41-244_Block41_Cal_1940.png) and [the lunette gable](../previews/block41-245_Block41_Cal_1940_Roof.png)
- [the garages](../previews/block41-246_Block41_Cal_Garages.png)
- [overview](../previews/block41-247_Block41_Aerial.png)

## Reproduction

`KALMAR_GEO=… python3 scripts/prepare_block41.py`; Blender with `scripts/rebuild_block41.py` (twice for the geometry audit) and the audits; Unreal with `resume_block41.py -HeroIdle` (or `{"execute":"refresh_block41.py"}` in a running editor), then `{"execute":"validate_block41.py"}`. Backup: `source/backups/block41/`.

## Limitations

- **The facade line** is modelled on the OSM line, which the measurements put 0.3-0.8 m too far south.
- **Estimates:**
  - the gables' outlines between the triangulated points;
  - the central gable's cartouche, which is a simple block and ring;
  - the Östra Sjögatan end;
  - the courtyard wing;
  - the roof's pitch.
- **Omitted:** the house numbers, the dates, the hanging sign, the notices, the bicycle stands.
