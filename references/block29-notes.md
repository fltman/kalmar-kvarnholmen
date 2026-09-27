# Pass 29: the north side of Södra Långgatan, Larmgatan–Kaggensgatan

Pass 29 details the south half of the block between Larmgatan, Södra Långgatan, Kaggensgatan and Storgatan. Five generic district volumes become the houses that stand on them:

- **Södra Långgatan 9** (OSM 92204156), with its rear wing and the small courtyard house 92204161.
- **Södra Långgatan 11** (92204198).
- **Södra Långgatan 13–15**, the long ochre house (92204187 west of the downpipe joint).
- **Kaggensgatan 9**, the three-storey corner house (92204187 east of the joint).
- **Kaggensgatan 11 A–D** (92204189): the yellow range on Kaggensgatan and the courtyard houses behind the gated passage.

The corner building on Larmgatan (Larmgatan 14–16, OSM 92204170 and 92204162), with its oriels and gables, is left for a later pass. It keeps its district geometry.

Panoramas and photospheres are working references only. No pixel is used as a texture, and no panorama, depth or tile data was extracted.

## Sources

- **OpenStreetMap** (`source/kvarnholmen.json`) supplies the five outlines.
- **Overpass query of 2026-09-23** for address nodes. These give the house numbers: Södra Långgatan 9, 11, 13 and 15; Kaggensgatan 9, 11 and 11 A–D; Larmgatan 14 and 16.
- **Google Street View**, official imagery of April 2025, viewed in the browser:

| Panorama (reported position) | Camera | Used for |
|---|---|---|
| 56.6625147 N, 16.3626175 E | 163 (heading 332°) | Södra Långgatan 9 and 11 straight on; the scale on the north side; a calibration view |
| 56.6625576 N, 16.3627644 E | 164, 167 (headings 332° and 5°) | Södra Långgatan 11, the west end of the ochre house and its step |
| 56.6626415 N, 16.3630602 E | 165 (heading 332°) | the ochre house: window rows, band, gateway, shop fronts, dormers; a calibration view |
| 56.6626813 N, 16.3632009 E | 166 (heading 345°) | the east end of the ochre house and the corner house's south front; a calibration view |
| 56.6627666 N, 16.3634847 E | — | the corner house's two fronts and the Kaggensgatan range, seen from the crossing |
| 56.6624715 N, 16.3624667 E | — | Södra Långgatan 9 and the east end of the Larmgatan corner building |

- **A contributed photosphere on Kaggensgatan** (a visitor's, June 2020). It shows the corner house's Kaggensgatan front: the door with its oculus, the arched shop windows and the upper windows. Kaggensgatan has no official coverage here.
- **Satellite imagery**, viewed only for roof colours and shapes: Airbus / Maxar, 2026.

## Measurement

The method is pass 28's (see `references/block28-notes.md`):

- the field of view is the URL's vertical `90y`;
- heights are taken along an image column from the facade base;
- the scale comes from building joints known from OSM.

The panoramas stand on the south side of the street, so each camera was registered again on the north facades.

1. **Scale on the north side.** In the level view from the first panorama, the joints of Södra Långgatan 9 (OSM 12.04 m apart) and the OSM street width give the same distance to the north facades, 5.6–5.75 m.
2. **The north pavement lies lower.** With that distance, the camera stands 2.35–2.4 m above the north facade bases, against 2.21 m above the south bases in pass 28. The street falls about 0.15–0.2 m towards the north side. Each height below is taken from its own house's base.
3. **Windows as a common scale.** From the ochre house eastwards there are no OSM joints in view. There, the ochre house's twelve upper windows serve as the common scale: the same windows are seen from three panoramas, and its gateway is seen from two.
4. **The ochre house stands 0.55 m forward.** Its west end shows a brown side wall beside Södra Långgatan 11 from both panoramas west of it. The step accounts for:
   - the width of the brown strip seen from two positions;
   - the window heights measured from the neighbouring panorama.

   Without the step, the four panoramas disagree by 8–10 %.
5. **Södra Långgatan 11 is 11.2 m wide**, against OSM's 10.83 m. This is measured between its quoin strips in two panoramas. The joint with the ochre house moves 0.37 m east.

| Feature | Measured (m) | Modelled (m) |
|---|---|---|
| Södra Långgatan 9 gutter band | 5.80–6.03 | 5.71–5.93 |
| Södra Långgatan 9 wall gable apex | 8.09 | 8.04 |
| Södra Långgatan 9 upper windows | 3.69–5.08 (1.0 wide) | the same |
| Södra Långgatan 11 cornice top | 6.88 | 6.68 |
| Södra Långgatan 11 segmental gable | 8.0 | 8.0 |
| Södra Långgatan 11 upper windows | 3.56–5.45 (glass), 3.40–5.69 (surround) | 3.56–5.45, 3.38–5.63 |
| Ochre house band | 3.99–4.35 | 4.00–4.33 |
| Ochre house upper windows | 5.17–6.91 | 5.20–6.93 |
| Ochre house cornice | 7.25–7.9 (eaves edge after correction) | 7.25–7.75 |
| Ochre house gateway, transom and arch | 2.27, 3.29 | 2.27, 3.29 |
| Corner house band | 4.46–4.88 | the same |
| Corner house first-floor windows | 5.78–7.65 | the same |
| Corner house second-floor windows | 9.0–11.2 | 9.15–11.0 |
| Corner house eaves | 11.75 (after correction) | 11.55 + gutter |
| Kaggensgatan range eaves | about 7.3 | 7.15 |

Plane intersections of projecting cornices and eaves are too high, as in pass 28. The ochre house's eaves edge measures 8.4 m and the corner house's 12.8 m. After correcting for their projection they stand at 7.9 m and 11.75 m.

**Layouts.** Both houses are positioned from the panoramas:

- Södra Långgatan 9: the upper windows sit at 2.14, 4.45, 6.51, 8.53 and 10.62 m from its west joint.
- Södra Långgatan 11: 1.82, 5.34, 7.77 and 9.63 m. The last two are a close pair.
- The ochre house: twelve upper windows at a 2.33 m pitch from 2.0 m. The wall over the gateway is wider, and the gateway is centred 19.73 m from the west end.
- The corner house: windows at 2.35, 5.43 and 7.92 m from the downpipe joint.

These were checked against the panoramas and corrected once. The first build placed Södra Långgatan 11's windows from a joint misread by 0.38 m in the second panorama, and the corner house's third window 0.65 m too far east.

## Geometry

**Södra Långgatan 9.**
- Cream render, with white lesenes at both ends.
- A white frieze under a red-brown gutter band.
- Five casement windows with grey awnings.
- A wide arched doorway, a door beside an iron gate, between two shop windows with purple and red awnings.
- The wall gable over the middle bays: its lunette, and its roof running back into the tiled main roof.
- The rear wing and the courtyard house are plain two-storey ranges under tiled roofs.

**Södra Långgatan 11.**
- Beige rough-cast, and red-brown casements in flat white surrounds.
- White quoins at both ends.
- The stepped white surround of the courtyard passage: block jambs, three steps and a keystone, with iron gate leaves.
- A moulded cornice broken by the segmental gable with its fan light.
- Two round dormers over the outer windows, and a chimney.
- Shop windows under red and green awnings.

**Södra Långgatan 13–15, the ochre house.**
- A grey-white shop floor under a white band, with an ochre upper floor.
- The brown west end: the side wall and a 0.6 m strip of the front.
- White quoins, and eleven wrought-iron sign brackets on the band.
- Five shop windows and three doors, and red and grey awnings.
- The arched carriage gateway: a fanlight over the transom, an iron gate and a white surround.
- Twelve upper windows with white surrounds, and a white cornice.
- Four red dormers in two pairs, on a grey metal roof.

**Kaggensgatan 9, the corner house.**
- Orange rough-cast, with a light stone plinth.
- Smooth bands and window surrounds, and a frieze under the eaves with a brass-coloured gutter.
- Iron wall anchors, and sconces between the first-floor windows.
- On Södra Långgatan: two arched shop windows, one under a black awning. The segmental heads are drawn on the true circle and the openings are closed with spandrel prisms.
- On Kaggensgatan:
  - the door under an oculus in an ochre keyhole surround;
  - two arched shop windows under black awnings;
  - a small arched door at the north end.
- A hipped tiled roof with an eyebrow dormer on each front, and a chimney.

**Kaggensgatan 11 A–D.**
- The yellow range on Kaggensgatan: eight bays, shop windows under black awnings and a door.
- Upper windows with white surrounds, a white cornice, and five red dormers on a tiled roof.
- The courtyard houses: plain two-storey ranges under tiled roofs.
- A gate wall with an iron gate closes the passage between the corner house and the range.

The 28 new `M_Block29_*` materials tint existing texture sets towards colours read from the panoramas. There are no new texture sets.

## Verification

- **Zones:** `previews/block29-zones.json`.
  - The zones cover the five outlines, with 0.2 m² not zoned.
  - 22.4 m² lie outside OSM: the ochre house's and corner house's measured step onto the street.
- **Build:** `previews/block29-build.json`.
  - Five meshes, 336,475 triangles, no zero-area UV triangles.
  - Every mesh has at most 18 degenerate faces, which the export removes.
- **Repeatability:** `previews/block29-repeatability.json`. Three scoped rebuilds gave identical geometry, UVs and material slots.
- **Pass 26 and 28 unchanged:** the pass 29 rebuild re-runs the pass 26 and 28 builders for their helpers.
  - Their meshes in the saved blend still match `previews/block28-repeatability.json`.
  - Their FBX files were not rewritten.
- **FBX audit:** `previews/block29-fbx-audit.json`. No zero-length or non-finite normals, tangents or binormals.
- **Unreal:**
  - 28 materials with normal and roughness maps (`block29-materials.json`);
  - five meshes imported with Nanite (`block29-import.json`);
  - render buffers without zero or non-finite vectors (`block29-render-audit.json`).
- **Collision:** `previews/block29-collision.json`.
  - 288 floor samples and 274 capsule sweeps along walking lines 1.2 and 2.0 m outside every street front, and along Södra Långgatan, Kaggensgatan, Larmgatan and Storgatan.
  - No floor failures and no unresolved obstruction.
  - The corner house's entrance steps on Kaggensgatan block the 1.2 m line for 2.1 m; a verified detour passes 0.8 m out.
- **Calibration:** `previews/block29-calibration.json` compares 33 features in three views. Each feature is read in the panorama, then marked on the Unreal review shot of the same camera.
  - Median deviation 7 px, largest 27 px; 21 of the 33 lie within 8 px.
  - The largest deviations are the ochre house's dormers in the steep view 166. The near-frontal view 165 matches them within 5 px; the two panoramas disagree by about 0.5 m on their height.
  - The next largest is the crest of Södra Långgatan 11's segmental gable, 22 px.
- **Delivery:** `previews/block29-delivery.json` collects all of the above; every report has passed.

Review shots taken right after a reimport showed Nanite fallback meshes: the lunette and the awnings of Södra Långgatan 9 were missing. The delivered shots were taken two minutes after the import.

**Corrected against the calibration views:**
- Södra Långgatan 11's segmental gable had a triangular roof piece in front of it. It now has a curved roof, and the gable is 2.8 m wide.
- The round dormers stand right behind the cornice.
- The ochre house's dormers were raised about 0.4 m.
- The eyebrow dormers of the corner house stand straight behind the gutter. At 0.45 m up the roof, the eaves hid them completely.
- The corner house's raised doors had floating treads; they have two stone steps.

**A mesh-wide bevel collapse was found and fixed.** The first build of 92204187 had 12,235 degenerate faces:

- The 3 mm edge bevel clamps its width globally.
- The corner house's shop windows had flat elliptical heads, rising 0.14 m over 3 m. Their wall holes gave n-gons whose limit collapsed the bevel over the whole mesh.
- The openings are now rectangular up to the crown, with closed spandrel prisms under a true segmental head.

## Limitations

- **Roofs.** The roof tops, the rear wings and the courtyard houses are estimates. The ochre house's roof pitch (top 12.3 m) is not visible from the street.
- **Corner house width.** The panoramas suggest the corner house's south front is 1–1.5 m narrower than OSM:
  - the eaves corner and the window margin seen from the crossing both point that way;
  - its corner stays on OSM to keep the Kaggensgatan alignment.
- **Kaggensgatan 11 A–D** was measured obliquely from the crossing, against the corner house's known window rows, to about ±0.3 m.
- **Dormer positions** on the ochre house are good to about ±0.5 m.
- **Tenant signs, shop lettering and the date over Södra Långgatan 9's door** are omitted.

## Review shots

Straight from Unreal:
- [Södra Långgatan 9 and 11](../previews/block29-163_Block29_Cal_SL9.png)
- [Södra Långgatan 11](../previews/block29-164_Block29_Cal_SL11.png)
- [the ochre house](../previews/block29-165_Block29_Cal_Ochre.png)
- [the corner house](../previews/block29-166_Block29_Corner_House.png)
- [the ochre house's west end](../previews/block29-167_Block29_Ochre_West.png)
- [overview](../previews/block29-168_Block29_Aerial.png)

## Reproduction

1. `KALMAR_GEO=… python3 scripts/prepare_block29.py`
2. In Blender, `scripts/rebuild_block29.py`. It re-runs the pass 26 and 28 builders for their helpers but exports only the pass 29 meshes.
3. `scripts/audit_block29_fbx.py` and `scripts/audit_block29_geometry.py` (run the latter after two rebuilds), then `scripts/audit_block28_geometry.py` to confirm that the pass 26/28 meshes are unchanged.
4. Unreal, with `DEVELOPER_DIR=/Applications/Xcode.app/Contents/Developer`:
   - `resume_block29.py -HeroIdle`;
   - wait for the Nanite builds before taking shots;
   - then `{"execute":"validate_block29.py"}`.

Backup: `source/backups/block29/`.
