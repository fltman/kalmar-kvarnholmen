# Pass 95: the south side of Fiskaregatan, east part

Pass 95 replaces four generic district volumes from pass 17 on the south side of Fiskaregatan (fronts face north onto the narrow street) with what stands there. Pass 94 covers the houses just west of these (91885523, 91926303, 91926337, 91926333) and is not touched here.

From west to east:

- **91926308 (west 3.4 m):** a pale boarded gate wall, 2.2 m high, with a green double gate and a narrow white door. The yard behind is open, so this strip of the outline is released as open ground and only the wall is drawn.
- **The cottage (across 91926308 and 91926299):** a pale boarded one-storey cottage with its gable to the street, one window in green frames reaching into the gable, white bargeboards, a tiled saddle roof and a chimney. It stands across the OSM joint between the two outlines; its mesh is 91926308.
- **91926299 (east 1.8 m):** a narrow low link between the cottage and the grey house, under a shallow tiled roof along the street. Not seen on any panorama; estimated.
- **91926297 (west 10.1 m):** the pale grey boarded two-storey house with its gable to the street. It has three window columns in dark green frames with head boards, a half-round lunette in the gable, corner and bay pilaster strips with bases, a grey stone plinth, a tiled roof and a chimney.
- **91926297 (east 3.04 m):** the gateway to the yard. It has a white boarded portal with a green gate, a rendered stone pier against the red house, and a rendered wall running about 6 m back along the passage. The strip is released as open ground.
- **91926357:** the red boarded two-storey house with white corner pilasters and two white bay pilasters. It has eight windows in white surrounds with grey-green casements, a light rendered plinth, a white eaves board and gutter, and a tiled saddle roof along the street with a chimney. A round window sits in its west gable over the gateway; that position is estimated (see Limitations).

Panoramas are working references only. No pixel is used as a texture.

## Measurement

Three Google Street View panoramas were used, all with heading 166 (looking south), pitch 15 and a vertical field of view of 90°, at 696×375. The street frame below has its origin at the front corner shared by 91926297 and 91926357, (165.91, 105.19). In that frame, s runs east along the fronts and t runs north towards the street. The facade plane is 0.355 m outside the OSM line.

| Panorama | Where | Google position (local) | Resected position | Camera height | Resected on |
|---|---|---|---|---|---|
| 4sLEL9DP1P5fYxBrNrX6xw | in front of 91926357 | (172.26, 110.09) | (170.88, 108.36), heading 166.8, pitch 14.1 | 2.3 m assumed (gives a plinth top at 0.42–0.47 m) | the red house's west corner (s 0) and its two bay pilasters, assumed symmetric about the front's centre (s 6.47); residual ≤ 4 px on the pilasters, 8–14 px at the corner |
| 8bHcZNz8Ii37yQHRReMHCw | in front of 91926297 | (162.93, 112.29) | (162.62, 110.04), heading 168.9, pitch 12.6 | 2.3 m assumed, with the grey house's plinth top at 0.45 m | the grey house's east corner, the red house's corner board at s 0, and the grey house's middle window column; residual ≤ 9 px |
| M1snxnQNlUVD6QVYA1T-aQ | pass 94's panorama in front of 91926333 | (143.61, 117.13) | (145.87, 114.25), heading 171.3, pitch 15 | 2.45 m | taken from pass 94's sandbox run, not resected here (see below) |

**Resection.** Both of this pass's cameras come out 1.4–2.3 m south of Google's position. That puts them 3.6–4.0 m from the fronts, in the middle of the narrow street.

The red house's front is read from the 357 panorama with its pilasters taken as symmetric. That gives the bay pilasters at s 4.24 and 8.70 and the window columns at s 2.14, 5.03, 7.91 and 10.80. The windows are symmetric about the front's centre to within 0.02 m. This supports reading the red house as the full 12.94 m of the 91926357 outline.

**The third panorama.** I first placed the 333 panorama with the same offset from Google as my two cameras, at (142.2, 115.3). Pass 94's in-progress sandbox run uses (145.87, 114.25), heading 171.3. With that camera, the red 333 house's east corner falls on the OSM corner at (143.51, 110.8). With mine, it falls 3.5 m off. So pass 94's camera is used. Its split puts the gate wall in the west of 91926308 and the cottage across the 308/299 joint. With my camera, the cottage would have filled 91926308 exactly. **If pass 94's final camera differs, the joint at s −19.65 should be revisited.**

**Which house is which.**
- The pale grey two-storey gable house with the lunette is the west 10.1 m of 91926297.
- The red house with the white pilasters is 91926357.
- The "red boarded house next to a rendered stone-wall gate" in the brief is the same red house, 91926357, seen from the west on the 297 panorama. The gate between it and the grey house is the east 3.04 m of 91926297.
- The pale cottage with the gable to the street, seen on pass 94's panorama, stands east of a separate green gate wall.

**Measured values.** Heights are above the street at the facade; s is in the street frame described above.

| Part | Measured | Estimated |
|---|---|---|
| Gate wall (west of 91926308) | green double gate s −22.83 to −20.70, 2.1 m high; white door s −20.65 to −19.91; wall top 2.23 | the door's height |
| Cottage | west eave end s −19.65; gable apex s −17.26 at 4.01 (ridge 3.90); eaves 2.41; window s −18.05 to −16.93, from 1.5 to 2.6 m | east eave end (taken as symmetric, s −14.87); depth (the outlines); chimney |
| Link (91926299) | – | everything: eaves 2.5, ridge 3.3, pale boards |
| Grey house | east corner s −3.04; eaves 4.95–5.04 (taken as 5.10); gable apex 7.73 (ridge 7.60); plinth top 0.39–0.45; ground-floor windows 1.57–2.89, upper windows 4.22–5.25; lunette from 6.09 to 6.71, about 1.2 m wide; window columns 2.62 and 2.72 m apart | west corner at the OSM corner (s −13.10); window columns centred on the front (s −5.40, −8.07, −10.74); the inner pilaster strips; roof tiles (seen in colour on the 357 panorama); chimney |
| Gateway | portal opening s −2.85 to −1.15, top 2.36; pier s −0.95 to 0.1, top 3.86; the passage wall's top about 3.5–3.8 | the passage wall's length (6 m) and thickness |
| Red house | eaves board 5.75, gutter 5.89; plinth top 0.42; ground-floor windows 1.36/1.42–2.90, upper windows 3.87–5.40; windows 1.0 m wide inside 1.23 m surrounds; bay pilasters s 4.24 and 8.70 | the ridge (8.30, about 30°; the roof is not visible from the street); the roof material; the chimney; the round window's place |

## Verification

- **Zone checks** (`previews/block95-zones.json`): footprint 272.0 m² after release, zoned 272.0 m², 0.0 m² outside OSM, 0.0 m² not zoned, no overlap. 60.3 m² is released (the two gateways). The prepare script prints `BLOCK95_ZONES_OK`.
- **Sandbox, two runs.** Both printed `SANDBOX_DONE` with no errors (prelude: pass 92).
  - Each run rendered the three resected views at the panoramas' own size, an aerial view and an oblique street view. The renders were compared side by side with the photos (`SCR/p95/sb2/cmp_*.png`).
  - **Run 1:** on the grey house, the lunette, the apex, both window rows and the east corner land within about 5 px of the photo. On the red house, the window rows, all four pilasters and the eaves line land within about 5–8 px. On pass 94's panorama, the cottage window, the gable apex, the green gate and the white door land within about 5 px.
  - **Run 2:** removed the generic windows that run 1 had put on the red house's west wall. The 297 panorama shows none there.
- **`drop_degenerate_faces95`** is called right after `s21_finish` in `b95_finish`, with the `_thin` test. In the sandbox it removed 24, 8, 25 and 26 faces from 91926308, 91926299, 91926297 and 91926357. The sample centres lie on eaves, ridge and gable lines and in the lunette and the round window.
- **Pending:** the official build, the Blender geometry checks, the repeat build and the Unreal checks. The lead fills in their results.

## Limitations

- **The red gable over the gateway.** The 297 panorama shows a red gable with a round window and a small window rising behind the passage wall. Its rake does not fit the red house's west gable at the OSM position: the model's apex projects about 35 px to the right of where the photo shows it, and the photo's far eave corner is about 1 m lower. Either the red house's west wall stands 1–2 m east of the OSM corner, or the gable belongs to a building in the yard. The two panoramas also disagree by about 1 m on where the gateway pier stands. The model keeps the OSM outline and puts the round window on the red house's west gable as an estimate.
- **Omitted:**
  - the low red boarded piece with a green cap at the red house's west corner, because its position is inconsistent between the two panoramas (it appears to stand in front of the facade plane);
  - the lamp post, the TV aerial, the downpipes, house numbers and the yard behind the gates.
- **Grey house width.** Its window columns centre at s −7.65, 0.4 m east of the centre of the outline-based front (s −8.07). The model centres the gable and the columns on the outline.
- **Estimated:**
  - the narrow link in 91926299 (not seen);
  - all back and side walls, which carry generic windows;
  - the roofs' depths, which follow the outlines;
  - the red house's ridge and roof material;
  - the camera heights, assumed at 2.3 m on this pass's two panoramas.
- **Extra views that would settle the open points:**
  - from (160.5, 111.0), heading 122, pitch 15: into the gateway and onto the red west gable;
  - from (180.0, 108.0), heading 166, pitch 15: the red house's east corner;
  - from (151.0, 113.0), heading 166, pitch 15: the link in 91926299 and the cottage's east eave.

## Official build

The lead's build of pass 95 passed the Blender geometry checks, two rebuilds gave identical meshes, and passes 28–94 are unchanged. The Unreal import and its checks are deferred.
