# Pass 31: Larmgatan 16

Pass 31 details Larmgatan 16 (OSM 92204162), the yellow house north of the pass 30 corner building. The generic district volume becomes:
- **the front range on Larmgatan:** two storeys under a steep red-tiled roof with three dormers. The front stands between white rusticated lesenes. The ground floor has:
  - a central carriage passage with an iron gate, under a cartouche with the house number;
  - a door on steps and a shop window under an awning either side;
  - a white moulded cornice above.

  Upstairs, five windows in white surrounds under cornice heads, with a pediment on the middle one, below a dentilled main cornice.
- **two lower courtyard wings:** plain two-storey ranges under tiled roofs.

Panoramas are working references only. No pixel is used as a texture, and no panorama, depth or tile data was extracted.

## Sources

- **OpenStreetMap** (`source/kvarnholmen.json`) supplies the outline.
- The north neighbour, Larmgatan 18, is not in the district outlines. It belongs to the authored Storgatan block (`source/storgatan.json`, building 92204199, eaves 8.2 m) and is taken from there, so the north walls are party walls.
- **Google Street View**, official imagery of April 2025, viewed in the browser:

| Panorama (reported position) | Camera | Used for |
|---|---|---|
| 56.662611 N, 16.3616932 E, Larmgatan, straight in front of the house | 176 (heading 62°, level), 177 (heading 62°, pitch 28°) | the whole front, the cornice, the roof and the dormers; calibration views |

## Measurement

The panorama was registered on the house's two OSM joints, which lie 11.56 m apart:
- the north joint at the edge of the north lesene;
- the south joint at the downpipe next to the pass 30 corner building's north gable bay.

Both joints land within 0.03 m. The camera stands 5.33 m from the facade and 2.48 m above its base, like the other Larmgatan panorama in pass 30 (2.50 m). Its position is 1.95 m south of the reported one.

Heights refer to the Larmgatan facade base.

| Feature | Measured (m) | Modelled (m) |
|---|---|---|
| Plinth | 0.50 | 0.50 |
| Shop windows (frame) | to 3.16 | 0.60-3.05, awning above |
| Doors | to 2.50 | 0.30-2.50, on two steps |
| Carriage passage | arch top 2.89 | 2.30 + 0.59 arch |
| Cartouche | 3.09-3.64 | the same |
| Shop-floor cornice | 3.61-3.94 | the same |
| Upper windows | 4.70-6.69 (1.0-1.09 wide) | the same, 1.05 wide |
| Middle pediment, cornice heads | 7.68, 7.56 | 7.68, 7.4 |
| Main cornice | 7.85-8.2 after allowing for its projection | 8.2 with dentils |
| Dormers | base 9.0, top 10.7, 1.5-1.8 wide | windows 8.97-10.17, top 10.9 |

**Layout,** measured from the north joint:
- the lesenes, 0-0.79 m and 10.76-11.56 m;
- the shop windows, 0.86-3.35 m and 8.35-10.76 m;
- the doors, 3.81-4.67 m and 6.97-7.88 m;
- the passage, 4.96-6.64 m;
- the five upper windows, centred at 1.42, 3.47, 5.84, 8.16 and 10.20 m, symmetric about the passage;
- the dormers at 2.40, 5.87 and 9.26 m.

The outer dormers stand between the window axes. The first build put them over the second and fourth windows, and the pitched calibration view showed them 20 px low and too close together.

**Roof.** Tiles are visible just above the cornice from the street, so the lower slope is steeper than the 47° view ray. It is modelled as a mansard-like steep lower slope (8.2 to 10.3 m, 1.2 m in) and a low upper slope to a narrow flat top at 11.8 m. The upper slope and the top are estimates. The party walls to the north and south take no inset.

## Verification

- **Zones:** `previews/block31-zones.json`. The three zones cover the outline exactly. Both roof rings are valid polygons inside the front range.
- **Build:** `previews/block31-build.json`. One mesh of 49,484 triangles, no zero-area UV triangles, and four degenerate faces at the arched passage, which the export removes.
- **Repeatability:** `previews/block31-repeatability.json`. Two scoped rebuilds gave identical geometry, UVs and material slots.
- **Passes 26 and 28-30 unchanged:** the pass 31 rebuild re-runs their builders for their helpers.
  - Their meshes in the saved blend still match `previews/block28-repeatability.json`, `block29-repeatability.json` and `block30-repeatability.json`. All three reports are byte-identical to the copies taken before the pass.
  - Their FBX files were not rewritten.
- **FBX audit:** `previews/block31-fbx-audit.json`. No zero-length or non-finite normals, tangents or binormals.
- **Unreal:**
  - 8 materials with normal and roughness maps;
  - the mesh imported with Nanite;
  - render buffers without zero or non-finite vectors.
- **Collision:** `previews/block31-collision.json`. 75 floor samples and 69 capsule sweeps along walking lines 1.2 and 2.0 m outside the front and along the streets, with no floor failure and no obstruction.
- **Calibration:** `previews/block31-calibration.json` compares 22 features in two views. Each feature is read in the panorama, then marked on the Unreal review shot of the same camera.
  - Median deviation 3 px, largest 14 px (the dormer tops); 21 of the 22 lie within 8 px.
- **Delivery:** `previews/block31-delivery.json` collects all of the above; every report has passed.

## Review shots

Straight from Unreal:
- [the front](../previews/block31-176_Block31_Cal_Front.png)
- [the cornice and the dormers](../previews/block31-177_Block31_Cal_Roof.png)
- [overview](../previews/block31-178_Block31_Aerial.png)

## Reproduction

1. `KALMAR_GEO=… python3 scripts/prepare_block31.py`
2. In Blender, `scripts/rebuild_block31.py`. It re-runs the pass 26 and 28-30 builders for their helpers but exports only the pass 31 mesh.
3. `scripts/audit_block31_fbx.py` and `scripts/audit_block31_geometry.py` (run the latter after two rebuilds), then the pass 28-30 geometry audits.
4. Unreal, with `DEVELOPER_DIR=/Applications/Xcode.app/Contents/Developer`:
   - `resume_block31.py -HeroIdle`;
   - shots after the Nanite build;
   - then `{"execute":"validate_block31.py"}`.

Backup: `source/backups/block31/`.

## Limitations

- **Roof.** The upper slope, the ridge and the courtyard wings are estimates.
- **Heights.** They refer to the Larmgatan base. The pass 30 corner building refers to the Södra Långgatan base, which lies 0.17 m higher, so the two houses' heights differ by that datum where they meet.
- **Omitted:** tenant names on the awnings and the hanging signs.
