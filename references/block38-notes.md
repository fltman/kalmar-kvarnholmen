# Pass 38: number 27 and the Barometern building on Södra Långgatan

Pass 38 details the two district volumes on the north side of Södra Långgatan, opposite pass 37:

- **Number 27** (district volume 92379256), two storeys in yellow render with white trim:
  - a shop window, the glazed green door on three steps, and the wide shop window (the tattoo studio), in white surrounds;
  - a band, five windows in white surrounds under cornice heads, the eaves cornice;
  - a dark roof with two small dormers.
- **The Barometern newspaper building** (92379310), three storeys over a stone-clad ground floor, flat-roofed, in four parts from Ölandsgatan:
  - a yellow corner with an open arcade, eight axes and a pale vertical band, continuing along Ölandsgatan;
  - a tiled bay with the recessed entrance;
  - a salmon office front with pale horizontal and vertical bands and groups of narrow windows;
  - a glass and slate curtain wall with a mosaic-clad pier, a shop window and the garage door.

The two are district volumes (`SM_Building_*`), not OSM houses of the earlier passes; their outlines come from `source/district17.json`. Their meshes keep their names and replace the district ones.

Panoramas are working references only. No pixel is used as a texture, and no panorama, depth or tile data was extracted.

## Sources

- **Outlines:** `source/district17.json` (92379256, 92379310). The neighbours are the authored house 92379276 to the west, pass 34's houses beyond it, and the district volumes behind.
- **Google Street View**, official imagery of April 2025, viewed in the browser. The panoramas are those of pass 37, turned to heading 332°:

| Panorama | Camera | Used for |
|---|---|---|
| "24 Södra Långgatan" | 219 (level, pitch 5°), 220 (pitch 30°) | number 27 and the curtain wall |
| "28 Södra Långgatan" | 221 (pitch 5°), 222 (pitch 30°) | the salmon office front |
| "33 Södra Långgatan" | 223 (pitch 5°) | the tiled bay and the yellow corner |

## Measurement

- **Registration:** the camera positions of pass 37, registered on the south side's joints. The north facades lie 5.1-5.3 m from them. The base rows read 0.00-0.07 m, a check of the camera heights (2.25 m).
- The level views were taken at a tilt of 95° (5° up); all heights are read with that pitch.

| Feature | Measured (m) | Modelled (m) |
|---|---|---|
| No. 27: shop fronts | to 3.0-3.15, door from 0.54 | the same |
| No. 27: band | 3.87 | the same |
| No. 27: windows | glass 4.24-5.99, surrounds 3.97-6.21, heads 6.65-6.94 | the same |
| No. 27: eaves | 7.54 (underside) on the plane | 7.7 |
| Barometern: ground floor | windows 0.48-2.79, stone cornice 3.46 | the same |
| Barometern: windows | 4.51-6.0 and 7.62-8.97 (salmon); 4.61-6.11 and 7.70-9.14 (yellow) | the same |
| Barometern: band | 6.46-6.73 | the same |
| Barometern: parapet | 10.07-10.62 on the plane | top 10.6 |
| Curtain wall | glazing 4.13-6.05 and 7.26-9.10 | the same |

**Layout,** from the Ölandsgatan corner: the arcade 0.4-2.97 m; the yellow part to 11.5 m; the tiled bay to 14.1 m; the salmon front to 40.5 m (vertical bands at 17.23, 22.59, 27.95 and 33.31 m); the curtain wall with the mosaic pier (45.05-47.24 m) and the garage (49.9-52.3 m) to 53.0 m.

## Verification

- **Zones:** `previews/block38-zones.json`. The four zones cover both outlines (1,792 m²), with 0.2 m² not zoned and no overlap.
- **Build:** two meshes, 107,477 triangles, no zero-area UV triangles and no degenerate faces.
- **Repeatability:** two scoped rebuilds gave identical geometry, UVs and material slots.
- **Passes 26 and 28-37 unchanged:** all ten repeatability reports are byte-identical to the copies taken before the pass.
- **FBX audit:** no zero-length or non-finite normals, tangents or binormals.
- **Unreal:** 14 materials with normal and roughness maps; both meshes imported with Nanite; clean render buffers.
- **Collision:** 209 floor samples and 203 capsule sweeps. Number 27's entrance steps block the inner walking line, as they should, and it passes round them 0.8 m further out (a verified detour).
- **Calibration:** `previews/block38-calibration.json`, 30 feature groups in four views: median 4 px, largest 10 px (number 27's window heads); 28 of the 30 within 8 px.
- **Delivery:** `previews/block38-delivery.json`; every report has passed.

**Corrected against the calibration views:**
- **The review cameras.** Their pitch was first set to -5°. The panoramas' tilt of 95° means +5°.
- **Number 27's windows** were first 0.3 m too short, from a misread row. They are now 4.24-5.99 m, as measured.

## Review shots

- [number 27](../previews/block38-219_Block38_Cal_No27.png)
- [its upper storey](../previews/block38-220_Block38_Cal_No27_Roof.png)
- [the Barometern building](../previews/block38-221_Block38_Cal_Barometern.png)
- [its upper storeys](../previews/block38-222_Block38_Cal_Barometern_Roof.png)
- [the corner](../previews/block38-223_Block38_Cal_Barometern_Corner.png)
- [overview](../previews/block38-224_Block38_Aerial.png)

## Reproduction

`KALMAR_GEO=… python3 scripts/prepare_block38.py`; Blender with `scripts/rebuild_block38.py` (twice for the geometry audit) and the audits; Unreal with `resume_block38.py -HeroIdle`, then `{"execute":"validate_block38.py"}`. Backup: `source/backups/block38/`.

## Limitations

- **The rear parts** of both volumes, and number 27's roof above the eaves, are estimates.
- **The Ölandsgatan front** of the Barometern building is not seen in these panoramas. Its window rhythm repeats the yellow corner's.
- **The mosaic** on the pier is a plain tiled surface.
- **Omitted:** the newspaper's signs, the posters and the exhibition texts in the windows, the tattoo studio's lettering and flag, the street furniture.
