# Pass 39: three houses on Södra Långgatan east of Västra Sjögatan

Pass 39 details three district volumes on the south side of Södra Långgatan, across Västra Sjögatan from pass 37's corner house:

- **The yellow wooden corner house** (92412832, "34" by its door), two storeys of pale yellow vertical boarding between white board pilasters:
  - on Södra Långgatan: two window axes, a frontispiece with an arched door in a white surround, a window above it and an attic storey under a pediment with an oculus, then a shop window and a glazed door under one casing with two windows above;
  - on Västra Sjögatan (24 m): four shop windows, an arched carriage gate with diagonal boarding, a door and a shop window under one transom, seven windows above, a flush attic storey;
  - a frieze and eaves cornice, a steep tile roof hipped round the corner, two gable dormers on Södra Långgatan and four on Västra Sjögatan, two chimneys;
  - a low rear part beside the courtyard.
- **The salmon house of Kalmar Stadsmission** (92412859), two storeys of render:
  - a rusticated ground floor on a panelled grey-green plinth: four windows, a glazed double door and a gateway whose doors stand 0.8 m back, all in grey-green surrounds;
  - a thin band, a plain band (where the stencilled name is) and a moulded sill band;
  - six brown casements with top lights in surrounds, a thin string and a deep cornice;
  - a low metal roof behind the cornice; a plain rear range round the courtyard.
- **The grey wooden house** (92412869, "39"), two storeys of grey-blue vertical boarding on a dark plinth:
  - four windows and a panelled double gate under a dentil cornice on the ground floor, five windows above;
  - white surrounds under head boards, white corner boards, a frieze and eaves;
  - a sheet-metal roof with a brick chimney.

The three are district volumes (`SM_Building_*`); their outlines come from `source/district17.json` and the meshes keep their names.

Panoramas are working references only. No pixel is used as a texture, and no panorama, depth or tile data was extracted.

## Sources

- **Outlines:** `source/district17.json` (92412832, 92412859, 92412869). The neighbours are the district volumes 92412841 (south of the yellow house) and 92412846 (east of the grey house); the street fronts face Södra Långgatan and Västra Sjögatan.
- **Google Street View**, official imagery of April 2025, viewed in the browser at a vertical field of view of 75° (screenshots 1200×706, one 1428×840):

| Panorama | Id | Camera | Used for |
|---|---|---|---|
| "34 Södra Långgatan" | r6QWw5u5ajnvg8QGsphMaQ | 227 (heading 140°, level), 228 (pitch 25°) | the yellow house's western bays, the frontispiece, the dormer, the roof |
| "35 Södra Långgatan" | 3c-fBP6Pz2BHPo8zbKbS7g | 225 (heading 152°, level), 226 (heading 175°, pitch 22°) | the yellow house's eastern bays; the frontispiece and dormers obliquely |
| "37 Södra Långgatan" | ZO5ckbm0mBm-lpTCBMPnJA | 230 (heading 152°, level), 231 (pitch 25°) | the salmon house straight on |
| "39 Södra Långgatan" | HebU0W3fMDCLMfT2Vtq9hA | 232 (heading 133°, level), 233 (pitch 20°) | the grey house; the salmon cornice's end |
| "6 Västra Sjögatan" | u2Gf0paIG6E7G9S_0YjRXQ | 229 (heading 62°, pitch 5°) | the yellow house's Västra Sjögatan front (also headings 20° and 105°) |

## Measurement

**Registration.** Reported panorama positions were 1.0-1.6 m off, as before.
- **"39"** on the grey house's two joints (x 2.89 and 15.05): 7.08 m from the facade. The field of view was checked by shooting the gate's edge at headings 20° apart (predicted 887.7 px, found 888).
- **"37"** on the salmon house's joints (x -13.31 and 2.89): 7.09 m out, on the same camera line as "39" (y -73.79 both), which confirms both.
- **"6 Västra Sjögatan"** on the corner (y -80.80) and the joint with the green house (y -104.81), seen at headings 20° and 105°: 6.44 m out.
- **"34" and "35"** in one small bundle adjustment: the corner, the salmon joint, a pilaster and both edges of one window seen from both; residuals 0-5.8 mrad (up to 3 px). "35" stands 6.72 m out, "34" 5.98 m.
- **Roll:** "37" is rolled 0.67° and "6 Västra Sjögatan" 0.8° (level window rows sloped across the frame); both are corrected in the readings.
- **Camera heights** from each house's own base: 2.30 m ("37"), 2.35 m ("39"), 2.39 m ("35", at the salmon joint), 2.50 m ("34", at the corner), 2.46 m ("6"). The street falls about 0.2 m towards Västra Sjögatan.
- **Projecting parts triangulated from two panoramas:** the salmon cornice's front top edge at the grey house's joint ("37" and "39", gap 0.08 m): 7.70 m high, 0.82 m out of the facade. From "34" and "35", triangulated with the review cameras (which stand 0.355 m out like the model's walls, so the points are in the model's frame): the pediment apex 10.82 m and the attic window's top 8.55 m, both in the wall face; the western dormer's window 7.88-8.60 and apex 9.48 m, its front also in the wall face (gaps 0.05-0.49 m).

| Feature | Measured (m) | Modelled (m) |
|---|---|---|
| Grey house: ground windows | glass 1.79-3.30, surrounds from 1.65, head caps to 3.80 | openings 1.77-3.32 in 0.12 m surrounds, heads to 3.80 |
| Grey house: gate | opening 2.04 wide to 3.25; dentils 3.58-3.68; cornice to 3.84 | the same |
| Grey house: upper windows | glass 4.60-6.07, surrounds from 4.41, heads to 6.72 | openings 4.53-6.09, heads to 6.72 |
| Grey house: plinth, frieze, eaves | plinth 0.75; frieze from 6.55; gutter 7.0-7.2 on the plane | the same; eaves 6.95 |
| Grey house: roof | the ridge line and the chimney just over the eaves | a pitch of about 41°, the ridge strip at 11.35 |
| Salmon house: upper windows | surrounds 4.53-6.56, 1.35-1.47 wide | openings 4.62-6.40 in 0.12 m surrounds |
| Salmon house: ground floor | plinth 1.18; windows 1.25-3.22 (surrounds); door and gateway to 3.02-3.03; rustication every 0.30 m | the same |
| Salmon house: bands | 3.74-3.82; sill band 4.09-4.58; string 7.06-7.19 | the same |
| Salmon house: cornice | 7.55-8.29 on the plane; the front top edge triangulated at 7.70, 0.82 m out of the facade | wall 7.45, corona top 7.70, 0.83 m out |
| Yellow house: upper windows | surrounds 4.13-6.20 ("35"), 4.35-6.55 ("34"), 4.27-6.30 ("6"); triangulated 4.23-6.40 | 4.25-6.33 |
| Yellow house: ground windows | surrounds 1.05-3.15; shop windows 0.95-3.30 | the same |
| Yellow house: plinth, frieze, eaves | plinth 0.72-0.81; frieze from 6.7-6.9; cornice top 7.30 (triangulated, gap 0.37) | plinth 0.80, frieze 6.75-6.95, eaves 7.30 |
| Yellow house: frontispiece | attic window to 8.55, pediment base cornice to 8.6, apex 10.82 (triangulated) | attic window 7.45-8.45, pediment 8.40-10.82 |
| Yellow house: Västra Sjögatan | gate 2.42 wide, springing 2.67, crown 3.12; door 0.76 wide to 2.57, transom to 3.0; attic window 7.42-8.25 | the same |
| Yellow house: roof | the ridge 12.3-12.6 behind the front | a pitch of about 56°, the ridge strip at 12.6 |

**Layout of the yellow house**, Södra Långgatan (x): corner pilaster at the salmon joint -13.33 to -13.75; windows -14.55 to -15.94; pilaster -16.67 to -17.08; windows -18.00 to -19.40; the frontispiece between pilasters -20.25 to -20.70 and -22.08 to -22.67 (door centre -21.39); the shop casing -23.49 to -27.51 (window -23.72 to -26.14, door -26.40 to -27.30) under windows -23.53 to -24.98 and -26.02 to -27.48; corner pilaster -28.44 to -28.90. Västra Sjögatan (y): pilasters at -80.79, -87.45, -92.12, -95.85, -98.72 and -104.30; the gate -96.30 to -98.72; the door and shop window -99.96 to -103.63.

## Verification

- **Zones:** `previews/block39-zones.json`. Five zones cover the three outlines (839.8 m²), 0.05 m² not zoned, no overlap.
- **Build:** three meshes, 117,378 triangles, no zero-area UV triangles; 175 zero tangent frames repaired at export, as in earlier passes.
- **Repeatability:** two scoped rebuilds gave identical geometry, UVs and material slots.
- **Passes 28-38 unchanged:** their meshes in the saved scene hash identically to their repeatability reports. (Pass 26's own report was already out of date before this pass: pass 28 corrected those houses, and pass 28's report covers them.)
- **FBX audit:** no zero-length or non-finite normals, tangents or binormals.
- **Unreal:** 17 materials with normal and roughness maps; the three meshes imported with Nanite; clean render buffers.
- **Collision:** 184 floor samples and 174 capsule sweeps. The frontispiece's and the shop door's steps block the inner walking line, as they should, and it passes round them 0.8 m further out (two verified detours).
- **Calibration:** `previews/block39-calibration.json`, 58 features in nine views: median 4 px, largest 15 px (the pediment apex from "35", which "34" puts within 1 px); 52 of the 58 within 8 px. The yellow house's upper floor reads 8-10 px high from "35" and "6" and within 1-7 px from "34": the spread of the two oblique cameras. Excluded: the street corner seen from "34" (about 40 px), because the model's walls stand 0.355 m out of both OSM lines, so a convex corner is wider than the building (the project's convention; the review camera is shifted for one face only).
- **Delivery:** `previews/block39-delivery.json`; every report has passed.

**Corrected against the calibration views:**
- **The roofs** were first too flat (45° on the yellow house, 32° on the grey one): the panoramas show the tile roof and the grey house's ridge and chimney above the eaves, which the first renders hid.
- **The frontispiece** moved 0.1 m west, halfway between the positions read from "34" and "35" (they disagreed by 0.2 m).
- **The attic, the pediment and the dormers** were first solved against the review cameras without their 0.355 m shift (the pediment came out 0.6 m too low); re-triangulated in the model's frame. The attic windows were at first hidden behind the attic storey's own body; the dormers stood 0.4 m inside the roof instead of in the wall face.
- **The salmon cornice** first projected 0.47 m from the wall; the triangulated 0.82 m is measured from the facade, not from the OSM line.
- **The street corner:** the two fronts' wall slabs, each 0.355 m out of its OSM line, left an open notch at the corner; a corner post now fills it.

## Review shots

- [the yellow house from "35"](../previews/block39-225_Block39_Cal_Yellow.png) and [its roof](../previews/block39-226_Block39_Cal_Yellow_Roof.png)
- [the corner from "34"](../previews/block39-227_Block39_Cal_Corner.png) and [its roof](../previews/block39-228_Block39_Cal_Corner_Roof.png)
- [Västra Sjögatan](../previews/block39-229_Block39_Cal_Vsj.png)
- [the salmon house](../previews/block39-230_Block39_Cal_Salmon.png) and [its cornice](../previews/block39-231_Block39_Cal_Salmon_Roof.png)
- [the grey house](../previews/block39-232_Block39_Cal_Grey.png) and [its roof](../previews/block39-233_Block39_Cal_Grey_Roof.png)
- [overview](../previews/block39-234_Block39_Aerial.png)

## Reproduction

`KALMAR_GEO=… python3 scripts/prepare_block39.py`; Blender with `scripts/rebuild_block39.py` (twice for the geometry audit) and the audits; Unreal with `resume_block39.py -HeroIdle`, then `{"execute":"validate_block39.py"}`. Backup: `source/backups/block39/`.

## Limitations

- **Heights of the yellow house** rest on two oblique panoramas that disagree by up to 0.15 m (about 3 %); the model takes their triangulated mean.
- **The dormers' gables** come from the shared `roof_dormer` helper, whose gable rise is fixed: the apexes stand about 0.2 m lower than the triangulated 9.48 m.
- **The Västra Sjögatan attic's** top and pediment, the rear parts, the courtyard walls and the roofs' far slopes are estimates. So are the positions of the east dormer on Södra Långgatan and the four on Västra Sjögatan (read on the facade plane, not triangulated).
- **The salmon house's roof** is not seen from the street; it is a low slope behind the cornice.
- **Omitted:** the shop lettering, the stencilled name "KALMAR STADSMISSION", the signs, the street furniture, the bicycles.
