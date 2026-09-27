# Pass 37: three houses on Södra Långgatan east of the wooden house

Pass 37 details OSM way 92379313, the next generic volume east of pass 35's wooden house. The way reaches the corner of Ölandsgatan and holds three houses:

- **The grey house**, three storeys in grey-brown render:
  - an iron gate, three shop windows, a window and the entrance in a stone surround;
  - a thin band;
  - eleven axes of blue-grey casements in white surrounds on both upper floors;
  - a white frieze under the eaves and a dark metal roof.
- **The yellow house** (number 28), two storeys in apricot render:
  - a wooden garage door (dated 1951), shop windows in stone surrounds and a glazed door;
  - a thin band, ten axes of casements;
  - a tile roof.
- **The corner house** on Ölandsgatan, two storeys and an attic in grey-brown render:
  - three shop windows in brown surrounds, a band;
  - six axes of green casements in white surrounds on two floors, and the same storeys on the Ölandsgatan end;
  - a tile roof hipped toward Ölandsgatan, with a dormer and a chimney.

The large courtyard block behind the three front ranges (2,750 m², to Ölandsgatan) is not seen from Södra Långgatan. It is a plain two-storey range under an inset roof.

Panoramas are working references only. No pixel is used as a texture, and no panorama, depth or tile data was extracted.

## Sources

- **OpenStreetMap** (`source/kvarnholmen.json`) supplies the outline. The neighbours are:
  - the wooden house of pass 35 (`source/block35.json`) to the west;
  - the generic volumes 92379283 and others behind.
- **Google Street View**, official imagery of April 2025, viewed in the browser:

| Panorama (reported position) | Camera | Used for |
|---|---|---|
| 56.6631557 N, 16.3648348 E, "24 Södra Långgatan" | 213 (heading 152°, level), 214 (heading 152°, pitch 30°) | the grey house straight on, from both ends (headings 110° and 205°); calibration views |
| 56.6632402 N, 16.3651281 E, "28 Södra Långgatan" | 215 (heading 152°, level), 216 (heading 152°, pitch 30°) | the yellow house; its east joint from the west (heading 112°); calibration views |
| 56.6633432 N, 16.3654915 E, "33 Södra Långgatan" | 217 (heading 152°, level) | the corner house; a calibration view |

## Measurement

**Registration.** Each panorama is registered on its own house's two joints, which are seen in the panorama at other headings:
- **"24"** on the joint with the wooden house (heading 205°) and the joint with the yellow house (heading 110°, measured from "28"). It stands 5.90 m from the facade. The base reads 0.07 m.
- **"28"** on the joint with the grey house and the joint with the corner house. It stands 6.21 m from the facade. The base reads 0.02 m.
- **"33"** on the OSM corner at Ölandsgatan and the joint with the yellow house. It stands 6.13 m from the facade; the base reads -0.2 m in a pitched-down view.
- The joint between the yellow house and the corner house is triangulated from "28" and "33" at 51.2 m from the wooden house.
- The first attempt, with the cameras on the pass 35 track, put them 0.3-0.5 m too far north. The heights then disagreed with the base rows by up to 1 m (in "33", where the facade base is hidden by parked cars, a level-view reading of the kerb had to be replaced by the pitched-down view).

| Feature | Measured (m) | Modelled (m) |
|---|---|---|
| Grey house: shop windows | 4.81-8.32, 9.14-12.61, 13.49-16.98 along the front; tops 3.1 | the same, sills 0.45 |
| Grey house: gate, window, entrance | gate 1.62-4.03 (top 3.1); window 17.65-19.43 (0.75-3.05); entrance surround 20.02-22.71 (top 3.5) | the same |
| Grey house: band | 3.53-3.72 | a band at 3.57-3.67 |
| Grey house: windows | 4.60-6.49 and 7.62-9.19 (surrounds), 1.43 wide | openings 4.70-6.39 and 7.72-9.09, 1.23 wide, in 0.10 m surrounds |
| Grey house: frieze, eaves | frieze 9.82-10.4; the roof edge 11.02 on the plane | frieze to 10.3, eaves 10.35 |
| Yellow house: ground floor | garage 26.25-29.87 (top 2.68); shop windows 31.19-34.91, 36.18-40.03, 41.21-44.04 (tops 2.68) | the same, and a shop window and a door east of them (estimated) |
| Yellow house: windows | 4.06-5.52 and 7.12-8.46, 1.3 wide | the same |
| Yellow house: eaves | 9.22 (the underside), roof edge 9.54 on the plane | 9.2 |
| Corner house: shop windows | 51.64-55.07, 55.37-59.07, 59.45-62.96; 0.25-2.27 | the same |
| Corner house: band | 2.97-3.17 | the same |
| Corner house: windows | 3.63-5.63 and 6.61-8.37 (surrounds), 1.65 wide | openings 3.75-5.51 and 6.72-8.26, 1.36 wide |

**Layout,** from the joint with the wooden house:
- the grey house to 25.5 m:
  - window axes at 1.30, 3.42, 5.59, 7.74, 9.84, 12.02, 14.13, 16.30, 19.27, 21.20 and 23.55 m;
  - the gate at the west end, the entrance at the east end;
- the yellow house to 51.2 m, with ten axes from 26.93 m, 2.49 m apart;
- the corner house to the OSM corner at 63.5 m, with six axes at 52.67-61.99 m.

## Geometry

- **Front ranges:**
  - the three street fronts with their openings, surrounds, bands, friezes and eaves;
  - the gate's iron bars and the garage door's boards;
  - saddle roofs with fire walls at the party walls; the corner house's roof is hipped toward Ölandsgatan.
- **The corner house's Ölandsgatan end:** the two window storeys over a plain ground floor.
- **The courtyard block:** plain walls with casements and an inset roof.

The 14 new `M_Block37_*` materials tint existing texture sets. There are no new texture sets.

## Verification

- **Zones:** `previews/block37-zones.json`. The four zones cover the outline (3,597 m²), with 0.01 m² not zoned, no overlap and nothing outside OSM.
- **Build:** `previews/block37-build.json`. One mesh of 160,968 triangles, no zero-area UV triangles and no degenerate faces.
- **Repeatability:** `previews/block37-repeatability.json`. Two scoped rebuilds gave identical geometry, UVs and material slots.
- **Passes 26 and 28-36 unchanged:** their meshes in the saved blend match the repeatability reports of passes 28-36. All nine reports are byte-identical to the copies taken before the pass.
- **FBX audit:** `previews/block37-fbx-audit.json`. No zero-length or non-finite normals, tangents or binormals.
- **Unreal:** 14 materials with normal and roughness maps; the mesh imported with Nanite; render buffers without zero or non-finite vectors.
- **Collision:** `previews/block37-collision.json`. 213 floor samples and 203 capsule sweeps along walking lines 1.2 and 2.0 m outside the three fronts and the Ölandsgatan end, and along the streets, with no floor failure and no obstruction.
- **Calibration:** `previews/block37-calibration.json` compares 34 feature groups in four views, in side-by-side crops of the panorama and the Unreal review shot at the same angular scale (one value per group, its worst member).
  - Median deviation 3 px, largest 13 px; 33 of the 34 lie within 8 px.
  - The largest is the corner house's shop window bottoms. The facade base there reads -0.2 m, since the pavement falls toward Ölandsgatan, and parked cars hide part of the window bottoms.
- **Delivery:** `previews/block37-delivery.json` collects all of the above; every report has passed.

**Corrected against the calibration views.**
- **The renders.** The grey and grey-brown renders were made cooler; they had rendered pink-beige.
- **The grey house's downpipes** moved to 4.32 and 17.40 m. They had been placed from the camera before its registration, 0.8 m off.
- **The corner house's shop windows** now reach down to 0.05 m.
- **The Unreal reimport.** The first rerun had kept the previous mesh, because the old import report was not removed. It was run again with the report removed.

## Review shots

Straight from Unreal:
- [the grey house](../previews/block37-213_Block37_Cal_Grey.png)
- [its upper storeys](../previews/block37-214_Block37_Cal_Grey_Roof.png)
- [the yellow house](../previews/block37-215_Block37_Cal_Yellow.png)
- [its upper storey](../previews/block37-216_Block37_Cal_Yellow_Roof.png)
- [the corner house](../previews/block37-217_Block37_Cal_Corner.png)
- [overview](../previews/block37-218_Block37_Aerial.png)

## Reproduction

1. `KALMAR_GEO=… python3 scripts/prepare_block37.py`
2. In Blender, `scripts/rebuild_block37.py`. It re-runs the pass 26 and 28-36 builders for their helpers but exports only the pass 37 mesh.
3. `scripts/audit_block37_fbx.py` and `scripts/audit_block37_geometry.py` (run the latter after two rebuilds), then the pass 28-36 geometry audits.
4. Unreal, with `DEVELOPER_DIR=/Applications/Xcode.app/Contents/Developer`:
   - `resume_block37.py -HeroIdle`;
   - shots after the Nanite build;
   - then `{"execute":"validate_block37.py"}`.

Backup: `source/backups/block37/`.

## Limitations

- **The courtyard block** (most of the way's area) is not seen from the street. Its height and form are estimates.
- **The roofs** above the eaves are estimates.
- **The yellow house's east end** (the shop window and door east of 44 m) is seen only obliquely and estimated.
- **The corner house's Ölandsgatan end** is not seen in these panoramas. Its window rhythm is assumed.
- **Omitted:** the posters covering the shop windows, the shop lettering (the toy shop's sign), tenant signs and the street furniture.
