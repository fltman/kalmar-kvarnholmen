# Pass 34: three houses on Södra Långgatan east of number 16

Pass 34 details the three low houses east of the pass 33 corner house on the north side of Södra Långgatan. Each generic district volume becomes a two-storey front range on the street and lower ranges behind it.

- **The Blanc house** (OSM 92379287; number 18 over its door), in pale render:
  - four slender columns framing two shop windows and the door;
  - a pilaster dividing the front, a side door and a boarded double gate;
  - four upper windows in white surrounds over panels with roundels, a moulded band and an eaves board;
  - a red tile roof with three round-headed dormers in salmon surrounds, the middle one larger with a finial, and a chimney.
- **The yellow house** (92379267; number 21 on the gate), in yellow render with white lesenes:
  - two shop windows, the door, and a red double gate under a latticed transom;
  - a moulded band;
  - five upper windows in white surrounds under fabric awnings, over panels;
  - an eaves board and a red tile roof with a large boarded dormer and two skylights.
- **The cream house** (92379282):
  - a long shop front of two windows and two doors under a fascia, between white pilasters;
  - four upper windows, an eaves board, and a dark roof with a chimney.

Panoramas are working references only. No pixel is used as a texture, and no panorama, depth or tile data was extracted.

## Sources

- **OpenStreetMap** (`source/kvarnholmen.json`) supplies the outlines. The east neighbour is the authored building 92379276 (`source/district17.json`, height 7.1 m); the west neighbour is the pass 33 corner house.
- **Google Street View**, official imagery of April 2025, viewed in the browser. The house numbers are the ones painted on the houses.

| Panorama (reported position) | Camera | Used for |
|---|---|---|
| 56.6628983 N, 16.3639509 E, "18 Södra Långgatan" | 190 (heading 345°, level), 191 (heading 345°, pitch 30°) | the Blanc house and its dormers; calibration views |
| 56.6629851 N, 16.3642463 E, "21 Södra Långgatan" | 192 (heading 332°, level), 193 (heading 332°, pitch 28°), 194 (heading 30°) | the yellow house straight on, its dormer; the cream house from the west; calibration views |
| 56.6630689 N, 16.3645392 E, "22 Södra Långgatan" | 195 (heading 285°) | the cream house from the east; a calibration view |

## Measurement

Each panorama was registered on its own house's two OSM joints:

| Panorama | Joints | Camera (model frame) | Distance to the facade | Residual |
|---|---|---|---|---|
| "18" | the Blanc house, 12.08 m apart | −154.08, −74.20 | 5.65 m | 0.014 m |
| "21" | the yellow house, 11.17 m apart | −133.32, −73.97 | 5.44 m | 0.006 m |
| "22" | the cream house, 11.97 m apart (both seen obliquely) | −113.90, −73.99 | 5.14 m | 0.005 m |

All three land on one camera track (y −74.0 to −74.2), about 1.9 m south of their reported positions, like the other panoramas on this street. The camera heights are 2.30 m and 2.20 m from the base and horizon rows. The third camera is taken at 2.20 m.

The cream house is seen only obliquely, from its two neighbours' panoramas at about 45-60° off axis. Its four upper windows come out at the same places from both sides within 0.1-0.3 m. Its window heights agree within 0.2-0.4 m, and the model takes the mean.

| Feature | Measured (m) | Modelled (m) |
|---|---|---|
| Blanc house: shop windows, door, side door, gate | 0.46-2.46; to 2.13; to 2.60; to 2.75 | the same |
| Blanc house: band | 3.06-3.28 | the same |
| Blanc house: upper windows | 3.88-5.36 (1.05 wide) | the same |
| Blanc house: eaves | board 5.63-6.08, gutter 6.31 on the facade plane | eaves 6.08 (raised 0.13 m after the calibration view) |
| Yellow house: shop windows, door, gate | 0.36-1.87; to 2.08; to 2.51, transom from 2.04 | the same |
| Yellow house: band | 2.88-3.19 | the same |
| Yellow house: upper windows | 3.61 to the fabric awnings' lower edge at 4.79 (1.1 wide) | 3.61-5.10, the awnings' lower edge at 4.79 |
| Yellow house: eaves | board 5.44-5.71, gutter 6.16 on the facade plane | eaves 5.9 |
| Yellow house: dormer | apex 7.70 on the facade plane, set back about 1 m | set back 1 m, 1.15 m wide window 1.25 m tall |
| Cream house: shop front | windows to 2.4-2.6, doors to 2.4, fascia to 3.1 | the same |
| Cream house: upper windows | 3.47-5.32 (east view), 3.65-5.69 (west view) | 3.55-5.50 |
| Cream house: eaves | 6.16-6.44 on the facade plane | 6.15 |

**Layout,** measured from each house's west joint:
- **The Blanc house:**
  - the columns at 0.13, 2.00, 3.16 and 5.06 m, with the shop windows and the door between them;
  - the dividing pilaster at 5.2-5.6 m, the side door at 6.4-7.5 m and the gate at 9.4-10.9 m;
  - the upper windows at 1.55, 3.72, 6.99 and 10.33 m;
  - the dormers at about 1.5, 5.3 and 8.7 m (corrected for their setback).
- **The yellow house:**
  - the shop windows at 0.55-3.15 m and 5.72-7.78 m, the door at 4.02-4.89 m and the gate at 8.59-10.56 m;
  - the upper windows at 1.75, 3.69, 5.58, 7.30 and 9.60 m;
  - the dormer over the middle.
- **The cream house:**
  - the shop windows at 1.15-4.02 m and 7.27-10.66 m, the doors at 4.15-5.46 m and 5.8-7.2 m;
  - the upper windows at 2.6, 5.3, 7.8 and 9.8 m;
  - the pilasters at both ends.

The two views place the cream house's doors differently, so the model has both.

## Geometry

- **Front ranges.** A roof with slopes to the street and the courtyard, and fire walls at the party walls. The roof tops (9.3-9.4 m) are estimates.
- **Front details.** Shop fronts with their frames and plinths; the Blanc house's columns and the yellow house's latticed transom. Upper windows in white surrounds with panels (roundels on the Blanc house), fabric awnings on the yellow house, bands, eaves boards and gutters.
- **Dormers.** Round-headed with salmon surrounds on the Blanc house, a boarded gable dormer on the yellow house.
- **Rear ranges.** Plain two-storey ranges under tiled or dark roofs.

The 15 new `M_Block34_*` materials tint existing texture sets. There are no new texture sets.

## Verification

- **Zones:** `previews/block34-zones.json`. The six zones cover the three outlines, with 0.09 m² not zoned. The three roof rings are valid polygons.
- **Build:** `previews/block34-build.json`. Three meshes, 90,722 triangles, no zero-area UV triangles and no degenerate faces.
- **Repeatability:** `previews/block34-repeatability.json`. Two scoped rebuilds gave identical geometry, UVs and material slots.
- **Passes 26 and 28-33 unchanged:**
  - Their meshes in the saved blend match the repeatability reports of passes 28-33. All six reports are byte-identical to the copies taken before the pass.
  - Their FBX files were not rewritten.
- **FBX audit:** `previews/block34-fbx-audit.json`. No zero-length or non-finite normals, tangents or binormals.
- **Unreal:**
  - 15 materials with normal and roughness maps;
  - the three meshes imported with Nanite;
  - render buffers without zero or non-finite vectors.
- **Collision:** `previews/block34-collision.json`. 91 floor samples and 83 capsule sweeps along walking lines 1.2 and 2.0 m outside the three fronts and along the streets, with no floor failure and no obstruction.
- **Calibration:** `previews/block34-calibration.json` compares 51 features in five views. Each feature is read in the panorama, then marked on the Unreal review shot of the same camera.
  - Median deviation 3 px, largest 11 px; 48 of the 51 lie within 8 px.
  - The three at 11 px belong to the obliquely seen cream house: its window tops, which the two views place 0.37 m apart, and one window edge 70° off axis.
- **Delivery:** `previews/block34-delivery.json` collects all of the above; every report has passed.

**Corrected against the calibration views:**
- The Blanc house's eaves were raised 0.13 m. The gutter was 13 px low.
- The yellow house's windows reach under the fabric awnings. The panorama's "window top" was the awnings' lower edge, and in the first build the awnings hung 0.25 m low.
- The yellow house's dormer was made taller and wider. It was 11-17 px low.

## Review shots

Straight from Unreal:
- [the Blanc house](../previews/block34-190_Block34_Cal_Blanc.png)
- [its dormers](../previews/block34-191_Block34_Cal_Blanc_Roof.png)
- [the yellow house](../previews/block34-192_Block34_Cal_Yellow.png)
- [its dormer](../previews/block34-193_Block34_Cal_Yellow_Roof.png)
- [the cream house from the west](../previews/block34-194_Block34_Cal_Cream_West.png)
- [the cream house from the east](../previews/block34-195_Block34_Cal_Cream_East.png)
- [overview](../previews/block34-196_Block34_Aerial.png)

## Reproduction

1. `KALMAR_GEO=… python3 scripts/prepare_block34.py`
2. In Blender, `scripts/rebuild_block34.py`. It re-runs the pass 26 and 28-33 builders for their helpers but exports only the pass 34 meshes.
3. `scripts/audit_block34_fbx.py` and `scripts/audit_block34_geometry.py` (run the latter after two rebuilds), then the pass 28-33 geometry audits.
4. Unreal, with `DEVELOPER_DIR=/Applications/Xcode.app/Contents/Developer`:
   - `resume_block34.py -HeroIdle`;
   - shots after the Nanite build;
   - then `{"execute":"validate_block34.py"}`.

Backup: `source/backups/block34/`.

## Limitations

- **Roofs and rear ranges.** The roofs above the eaves, the chimneys' heights and the rear ranges are estimates.
- **The cream house** is measured only from oblique views, so its heights are good to about ±0.2 m.
- **Omitted:** tenant signs, the awning texts and shop lettering, the café furniture and the street furniture.
