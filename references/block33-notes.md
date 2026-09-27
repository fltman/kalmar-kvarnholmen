# Pass 33: Södra Långgatan 16

Pass 33 details Södra Långgatan 16 (OSM 92379302), the white corner house on the north-east corner of Södra Långgatan and Kaggensgatan. It is a three-storey house in the palace manner:

- **Ground floor:**
  - an open arcade behind the square corner pier, on both streets;
  - shop windows between plain piers, with round vents over the second one;
  - a door and a projecting risalit with the arched carriage gate and its wrought-iron gate.
- **Upper floors:**
  - above a moulded band, a console frieze under the first-floor windows;
  - window heads over a frieze with a festoon, with segmental pediments over the middle window of each wing;
  - small heads over the second-floor windows;
  - a dentilled cornice with a deep corona;
  - rusticated quoins at the corner and the east end.
- **The risalit** (0.1 m proud, with quoin strips):
  - paired pilasters with capitals round the first-floor window;
  - an entablature broken by a medallion under a segmental frame;
  - the second-floor window and a pediment standing on the cornice.

The generic houses further east on Södra Långgatan (92379287, 92379267, 92379282) are left for a later pass. They have no official panorama in front of them, only a business photosphere.

Panoramas are working references only. No pixel is used as a texture, and no panorama, depth or tile data was extracted.

## Sources

- **OpenStreetMap** (`source/kvarnholmen.json`) supplies the outline.
- **Google Street View**, official imagery of April 2025, viewed in the browser. House numbers come from the panorama labels:

| Panorama (reported position) | Camera | Used for |
|---|---|---|
| 56.662811 N, 16.3636397 E, Södra Långgatan, "16 Södra Långgatan" | 184 (heading 332°, level), 185 (heading 332°, pitch 32°) | the west wing, the corner and the arcade; calibration views |
| 56.6628557 N, 16.3637975 E, Södra Långgatan, "17 Södra Långgatan" | 186 (heading 332°, level), 187 (heading 332°, pitch 32°) | the risalit, the gate and the east wing; calibration views |
| 56.6627666 N, 16.3634847 E, the crossing (the pass 28 camera) | 188 (heading 20°) | the Kaggensgatan front; a review view |

## Measurement

The house spans the whole block front between Kaggensgatan and the neighbour to the east. OSM gives its corner and its east joint, 29.14 m apart.

**Registration.**

1. **A first joint fit.** Both panoramas were first fitted together, on the corner, the east joint and features seen in both (a downpipe and the gate's edges). The fit left residuals of 3 px. But the two panoramas' heights then disagreed by 8 % and the window widths by 6 %. At 55-65° off axis, the downpipe (in front of the facade) and the recessed gate edges bias the columns.
2. **The final registration** uses only points on the facade line:
   - the west panorama from the corner and the east joint, both visible in one view (5.18 m from the facade line);
   - the east panorama from the east joint and the requirement that both cameras stand at the same height (5.26 m).

   The heights of the two panoramas then agree within 1-2 %:
   - first-floor sills 5.55 and 5.47 m;
   - second-floor windows 9.29-11.04 m and 9.30-11.07 m.

   The gate's centre lands at x −166.30 and −166.28 from the two views.
3. **Camera height.** 2.34 m above the facade base, from the base and horizon rows.

| Feature | Measured (m) | Modelled (m) |
|---|---|---|
| Plinth | 0.6 | 0.6 |
| Shop windows | 0.67-3.2 | 0.67-3.2 |
| Band | 4.40-4.70 | the same |
| First-floor windows | 5.50-7.35 (1.07 wide) | the same |
| First-floor heads (ledge), segmental pediments | ledge underside 7.95-8.1 and crest 8.5-8.75 on the facade plane | ledge 7.92-8.24, crest 8.51, over a festoon frieze |
| Second-floor windows | 9.25-11.03 | the same |
| Cornice | top 13.6 on the facade plane; triangulated top 11.91, 0.8 m out | top 11.91, corona 0.8 m out, dentils 11.65-11.79 |
| Risalit windows | 5.49-7.31, 9.30-11.07 on the facade plane | 5.43-7.22, 9.17-10.90 (the risalit face 0.1 m proud) |
| Risalit capitals, entablature, medallion | to 7.63, 7.98-8.50, centre 8.31 on the facade plane; medallion triangulated 8.24 | to 7.28, 7.61-8.09, centre 8.10 |
| Risalit segmental frame | to 9.21 on the facade plane; triangulated 8.63, 0.47 m out | to 8.68 |
| Risalit pediment | apex 14.97 on the facade plane; triangulated 12.99, 0.81 m out (rays 0.03 m apart) | apex 12.99, 0.8 m out, 5.2 m wide |
| Gate | 14.04-16.28 m along the front, arch top 3.78, surround to 4.12, jambs 0.37-0.50 wide | the same, jambs 0.40 |

**Layout,** measured from the corner along Södra Långgatan:
- the corner pier, 0-1.20 m;
- the arcade, 1.20-2.69 m;
- shop windows at 3.56-7.08 m and 8.55-12.06 m;
- the risalit, 12.8-17.7 m;
- shop windows at 18.19-21.38 m and 22.22-23.59 m, then the door at 24.43-25.37 m;
- the east end with quoins at 29.14 m;
- the upper windows at 2.79, 4.92, 7.02, 9.11 and 11.26 m, the risalit axis at 15.2 m, and then 18.73, 20.73, 22.85, 24.93 and 27.0 m. Those at 7.02 and 22.85 m carry the segmental pediments.

On Kaggensgatan, seen from the crossing, the windows stand at 1.30, 3.27, 5.18 (segmental pediment), 7.17, 9.14 and 11.7 m from the corner, and a downpipe at 10.31 m. The further axes and the Kaggensgatan ground floor are estimated, since the photospheres there do not show this front.

**Projecting parts need both panoramas.** A height read on the facade plane is right only for flat features. For a projecting part the plane intersection overstates the height: along one ray, a lower point further out looks the same as a higher point on the facade.

With two panoramas the ambiguity goes away. Their rays through the same feature cross at the feature itself:
- The pediment's apex: 12.99 m high and 0.81 m in front of the facade line (rays 0.03 m apart). The plane reading was 14.97 m.
- The segmental frame over the medallion: 8.63 m, 0.47 m out.
- The medallion: 8.24 m, 0.18 m out (rays 0.17 m apart, since its centre is harder to read).

What follows from the triangulation:
- **The main cornice.** Its top is at 11.91 m with a corona about 0.8 m deep, not at 12.6 m with 0.43 m. Both render on the same sight line from the street, but only the lower, deeper cornice carries the pediment at its measured apex.
- **The risalit** stands only about 0.1 m proud. The first build set it 0.3 m proud.
- **The window heads.** Their ledges and segmental pediments were set lower than their projection allows. They are now 0.3 m higher, over a frieze with a festoon, as in the panorama.

**Corrected against the calibration views.**
- **The risalit medallion** was first placed over the entablature, centred at 8.8 m. In the panorama it sits in the entablature, with the segmental frame springing from the entablature's top and arching over it. The entablature is now broken by the medallion.
- **The gate's surround** was 0.31 m wide. The frontal panorama shows jambs of 0.37-0.50 m. It now has 0.40 m jambs and a 0.28 m arch band with a keystone. Its left edge in the oblique view went from 29 px to 9 px, its crown from 14 px to 7 px.
- **The gate's grille** stood 0.65 m deep in its opening. The deep reveal it left showed in the oblique view, which the panorama does not show, so the grille now stands nearly flush.

## Geometry

- **Walls.** The front walls, and the risalit as a second wall 0.1 m proud with its own openings and returns.
- **Ground floor.**
  - The corner arcade, with the pier's inner faces, the end and back walls, a ceiling at the band and a paved floor.
  - Shop windows, the door, round vents and the plinth.
  - The gate: an iron grille in an arched surround with a keystone and side blocks, and closed spandrel prisms at the arch.
- **Upper floors.**
  - Windows in moulded surrounds on console friezes.
  - Heads over a festoon frieze between consoles, with segmental pediments on the middle axes. Their outlines skip the arc's duplicated end points, which would otherwise make degenerate faces.
  - Second-floor heads.
- **Top.** A dentilled cornice with a corona 0.8 m deep, and quoins at both ends of the front.
- **The risalit.** Paired pilasters with capitals, the broken entablature, the medallion with its frame, and the pediment standing on the corona with its roof piece.
- **Roof.** A dark metal roof from the cornice at 11.9 m, with slopes to both streets over a 5 m inset and fire walls to the neighbours.

The 8 new `M_Block33_*` materials tint existing texture sets. There are no new texture sets.

## Verification

- **Zones:** `previews/block33-zones.json`. The zone is the OSM outline, and the roof ring is a valid polygon inside it.
- **Build:** `previews/block33-build.json`. One mesh of 117,496 triangles, no zero-area UV triangles and no degenerate faces.
- **Repeatability:** `previews/block33-repeatability.json`. Two scoped rebuilds gave identical geometry, UVs and material slots.
- **Passes 26 and 28-32 unchanged:**
  - Their meshes in the saved blend still match the repeatability reports of passes 28-32. All five reports are byte-identical to the copies taken before the pass.
  - Their FBX files were not rewritten.
- **FBX audit:** `previews/block33-fbx-audit.json`. No zero-length or non-finite normals, tangents or binormals.
- **Unreal:**
  - 8 materials with normal and roughness maps;
  - the mesh imported with Nanite;
  - render buffers without zero or non-finite vectors.
- **Collision:** `previews/block33-collision.json`. 157 floor samples and 153 capsule sweeps along walking lines 1.2 and 2.0 m outside both fronts, round the corner pier, and along Södra Långgatan and Kaggensgatan, with no floor failure and no obstruction.
- **Calibration:** `previews/block33-calibration.json` compares 44 features in four views. Each feature is read in the panorama, then marked on the Unreal review shot of the same camera.
  - Median deviation 3 px, largest 12 px; 40 of the 44 lie within 8 px.
  - The four above 8 px are window bottoms in the steep views. The project's shared window helper has a metal weather sill 0.3 m proud of the wall, and it hides the lower part of the glass from below; the real sills are shallower. The helper is used by every earlier pass and was not changed.
  - The dentil band cannot be read in the Unreal lighting and is excluded.
- **Delivery:** `previews/block33-delivery.json` collects all of the above; every report has passed.

## Review shots

Straight from Unreal:
- [the west wing and the corner](../previews/block33-184_Block33_Cal_West.png)
- [the west wing's upper floors and cornice](../previews/block33-185_Block33_Cal_West_Roof.png)
- [the risalit and the east wing](../previews/block33-186_Block33_Cal_East.png)
- [the risalit's pediment and medallion](../previews/block33-187_Block33_Cal_East_Roof.png)
- [the corner from the crossing](../previews/block33-188_Block33_Corner.png)
- [overview](../previews/block33-189_Block33_Aerial.png)

## Reproduction

1. `KALMAR_GEO=… python3 scripts/prepare_block33.py`
2. In Blender, `scripts/rebuild_block33.py`. It re-runs the pass 26 and 28-32 builders for their helpers but exports only the pass 33 mesh.
3. `scripts/audit_block33_fbx.py` and `scripts/audit_block33_geometry.py` (run the latter after two rebuilds), then the pass 28-32 geometry audits.
4. Unreal, with `DEVELOPER_DIR=/Applications/Xcode.app/Contents/Developer`:
   - `resume_block33.py -HeroIdle`;
   - shots after the Nanite build;
   - then `{"execute":"validate_block33.py"}`.

Backup: `source/backups/block33/`.

## Limitations

- **Kaggensgatan.** The front beyond the first six axes, and its whole ground floor, are estimates.
- **Roof.** The roof behind the cornice is not visible from the street.
- **Omitted:** tenant signs, awnings and the illuminated lettering.
