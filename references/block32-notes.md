# Pass 32: Larmgatan 22 and 24

Pass 32 starts on the block north of Storgatan. Two generic district volumes on its Larmgatan front become the houses that stand on them:

- **Larmgatan 22** (OSM 92204181), pale green, two storeys:
  - two wide segmental-arched shop windows and a round-arched door;
  - a plain frieze over the shop floor, whose historic shop lettering is omitted;
  - five upper windows in beige surrounds;
  - a cornice with a low iron railing and two arched dormers.
- **Larmgatan 24** (OSM 92204160), white, three storeys and an attic:
  - shop fronts and seven window axes;
  - balconies with wrought-iron railings on consoles over the middle three axes, on both upper floors;
  - pediments over the middle first-floor windows, and cornice heads over the others with panels and roundels below;
  - a dentilled main cornice;
  - an attic of three dormers: a wide one with three lights and two with one light.

Behind both front ranges lie lower courtyard wings.

The Storgatan corner houses south and east of them (Larmgatan 18 and 20, Storgatan 3 and 5) belong to the older authored Storgatan block and are unchanged. The houses further north on Larmgatan (92204190 and 92204168) had already been detailed in an earlier pass.

Panoramas are working references only. No pixel is used as a texture, and no panorama, depth or tile data was extracted.

## Sources

- **OpenStreetMap** (`source/kvarnholmen.json`) supplies the outlines. The authored Storgatan buildings (`source/storgatan.json`, heights from `source/district17.json`) are the neighbours to the south.
- **Google Street View**, official imagery of April 2025, viewed in the browser. House numbers are read from the panorama labels:

| Panorama (reported position) | Camera | Used for |
|---|---|---|
| 56.663094 N, 16.3612 E, Larmgatan, "22 Larmgatan" | 179 (heading 62°, level), 180 (heading 62°, pitch 28°) | Larmgatan 22: the whole front, the cornice and the dormers; calibration views |
| 56.6631748 N, 16.3611258 E, Larmgatan, "24 Larmgatan" | 181 (heading 62°, level), 182 (heading 62°, pitch 35°) | Larmgatan 24: the whole front, both balconies, the cornice and the attic; calibration views |

## Measurement

Each panorama was registered on its own house's two OSM joints:
- Larmgatan 22: the downpipes at both party walls, which lie 12.26 m apart;
- Larmgatan 24: the north pilaster and the joint with Larmgatan 22, 15.70 m apart.

The two cameras land on the same track, 7.02 m and 7.06 m from the facade line, with residuals of 0.02 m and 0.01 m. Their positions are 1.9 m south of the reported ones, as on the other Larmgatan panoramas.

The facade bases are hidden behind café terraces, so the camera height is taken as 2.48 m, from the two registered Larmgatan panoramas of passes 30 and 31 (2.48-2.50 m).

| Feature | Measured (m) | Modelled (m) |
|---|---|---|
| Larmgatan 22: shop windows | sill 0.85, crowns 3.54-3.61 | 0.85, 3.57 |
| Larmgatan 22: door arch | top 3.24 | 3.25 |
| Larmgatan 22: shop-floor cornice, frieze | 3.8-3.85, 4.0-4.5 | 3.72-3.88, 3.97-4.60 |
| Larmgatan 22: upper windows | 4.87-6.6 (1.0 wide) | 4.90-6.60 |
| Larmgatan 22: cornice | 7.35-7.7 on the facade plane | 7.5 |
| Larmgatan 22: dormers | tops about 8.75 on the facade plane, 1.4-1.55 m wide | 1.5 m wide, tops 9.45 |
| Larmgatan 24: shop-floor cornice | 3.80-4.32 | the same |
| Larmgatan 24: first-floor windows | 5.10-7.12 (1.0-1.15 wide), pediments to 7.93 | the same |
| Larmgatan 24: first-floor balcony | slab 4.37, rail to 5.54 on the facade plane | slab 4.25, rail to 5.12 |
| Larmgatan 24: second-floor windows | 8.94-11.11 | the same |
| Larmgatan 24: second-floor balcony | slab 8.49, rail to 10.07 on the facade plane | slab 8.30, rail to 9.17 |
| Larmgatan 24: main cornice | 11.8-13.35 on the facade plane | 12.6 with dentils |
| Larmgatan 24: attic dormers | visible above the cornice, caps about 15.2 | 15.1 + cap |

**Corrected against the calibration views.**

- **The attic of Larmgatan 24.** The first build set the attic dormers 0.4 m behind the wall line with tops at 14.2. In the calibration view the cornice then hid them completely, while the panorama shows 1.9 m of them above it. The sight line over the cornice's front edge fixes where they can stand. They now stand just behind the wall line, with their caps at 15.2 m, so they read as a set-back attic storey. They run back to the flat roof top.
- **The dormers of Larmgatan 22** were first built round-topped and 1.3 m wide, which put them 16 px (0.6 m) too high. They are 1.5 m wide under segmental red-brown roofs.
- **The balconies of Larmgatan 24** read high on the facade plane, as projecting parts do. They were lowered 0.15-0.2 m after the first review shots put them 8-17 px high.

**Layout.**
- Larmgatan 22, measured from the north joint:
  - the arched shop windows, centred at 2.70 and 7.03 m;
  - the door at 10.60 m;
  - the upper windows at 1.77, 3.64, 6.04, 8.05 and 10.62 m;
  - the dormers at 3.70 and 7.94 m, corrected for their setback.
- Larmgatan 24, measured from the north end:
  - the window axes at 1.55, 3.46, 5.77, 7.87, 9.99, 12.30 and 14.20 m;
  - the balconies over the middle three axes (4.15-10.76 m);
  - the attic dormers at 1.08-3.58, 5.24-10.44 and 12.05-14.55 m.

## Geometry

**Larmgatan 22.**
- The segmental shop-window arches use the closed spandrel prisms of pass 29, so the edge bevel stays intact.
- The round-arched door, the plinth, the shop-floor cornice and the frieze band.
- Upper windows in beige surrounds.
- The cornice with a two-rail iron railing.
- Two dormers with round-headed windows under segmental red-brown roofs, on a dark metal roof with fire walls at both party walls, and a chimney.

**Larmgatan 24.**
- Shop windows and glazed doors between narrow piers.
- Upper windows in white surrounds. Pediments over the middle first-floor axes; cornice heads and panels with roundels over and under the others.
- Two balconies on five consoles each, with wrought-iron railings.
- A frieze and a dentilled cornice.
- The attic dormers and a chimney.

The 12 new `M_Block32_*` materials tint existing texture sets. There are no new texture sets.

## Verification

- **Zones:** `previews/block32-zones.json`.
  - The zones cover both outlines, with 0.09 m² not zoned and 0.03 m² outside OSM.
  - Both roof rings are valid polygons inside their front ranges.
- **Build:** `previews/block32-build.json`. Two meshes, 82,882 triangles, no zero-area UV triangles and no degenerate faces.
- **Repeatability:** `previews/block32-repeatability.json`. Two scoped rebuilds gave identical geometry, UVs and material slots.
- **Passes 26 and 28-31 unchanged:**
  - Their meshes in the saved blend still match the repeatability reports of passes 28-31. All four reports are byte-identical to the copies taken before the pass.
  - Their FBX files were not rewritten.
- **FBX audit:** `previews/block32-fbx-audit.json`. No zero-length or non-finite normals, tangents or binormals.
- **Unreal:**
  - 12 materials with normal and roughness maps;
  - both meshes imported with Nanite;
  - render buffers without zero or non-finite vectors.
- **Collision:** `previews/block32-collision.json`. 110 floor samples and 101 capsule sweeps along walking lines 1.2 and 2.0 m outside both fronts and along Larmgatan, Storgatan and Norra Långgatan, with no floor failure and no obstruction.
- **Calibration:** `previews/block32-calibration.json` compares 42 features in four views. Each feature is read in the panorama, then marked on the Unreal review shot of the same camera.
  - Median deviation 3 px, largest 9 px; 41 of the 42 lie within 8 px.
  - The largest are Larmgatan 22's dormer top in the level view and its cornice top edge, both 8-9 px.
- **Delivery:** `previews/block32-delivery.json` collects all of the above; every report has passed.

## Review shots

Straight from Unreal:
- [Larmgatan 22](../previews/block32-179_Block32_Cal_L22.png)
- [Larmgatan 22, the cornice and the dormers](../previews/block32-180_Block32_Cal_L22_Roof.png)
- [Larmgatan 24](../previews/block32-181_Block32_Cal_L24.png)
- [Larmgatan 24, the balconies and the attic](../previews/block32-182_Block32_Cal_L24_Roof.png)
- [overview](../previews/block32-183_Block32_Aerial.png)

## Reproduction

1. `KALMAR_GEO=… python3 scripts/prepare_block32.py`
2. In Blender, `scripts/rebuild_block32.py`. It re-runs the pass 26 and 28-31 builders for their helpers but exports only the pass 32 meshes.
3. `scripts/audit_block32_fbx.py` and `scripts/audit_block32_geometry.py` (run the latter after two rebuilds), then the pass 28-31 geometry audits.
4. Unreal, with `DEVELOPER_DIR=/Applications/Xcode.app/Contents/Developer`:
   - `resume_block32.py -HeroIdle`;
   - shots after the Nanite build;
   - then `{"execute":"validate_block32.py"}`.

Backup: `source/backups/block32/`.

## Limitations

- **Camera height.** It is assumed from the neighbouring panoramas (2.48 m), since the facade bases are hidden. An error of 0.05 m would shift all heights by about 2 %.
- **Roofs and wings.** The roofs behind the cornices and the courtyard wings are estimates.
- **Omitted:** the café terraces, awnings, tenant signs and the historic shop lettering on Larmgatan 22.
