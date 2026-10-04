# Pass 112: corrections to four meshes (9 Larmgatan block, Gamla vattentornet, 92204191, 93238202)

Pass 112 is a correction pass. It deletes and re-creates four meshes that earlier passes built but got wrong. Each object is removed unconditionally (no `detail_pass` guard) and rebuilt under its old mesh name and category, with `detail_pass` 112 and `corrects_pass` set to the pass it replaces. No other mesh is touched.

| Mesh | Replaces pass | Category |
|---|---|---|
| `SM_Kvarnholmen_House_91846945` | 109 | Kvarnholmen/Larmgatan (109 used Kvarnholmen/Västra Vallgatan) |
| `SM_Kvarnholmen_House_91072716` | 111 | Kvarnholmen/Larmtorget |
| `SM_Kvarnholmen_House_92204191` | 105 | Kvarnholmen/Kaggensgatan (105 used Kvarnholmen/Strömgatan) |
| `SM_Kvarnholmen_House_93238202` | 100 | Kvarnholmen/Östra Vallgatan |

**Category note.** Two categories differ from the earlier passes, because the photographed fronts face Larmgatan and Kaggensgatan. If the build or the Unreal import keys on the category, the lead may want the old categories back. They are the second argument of `b112_new`.

Files: `scripts/prepare_block112.py` (zones → `source/block112.json`, `previews/block112-zones.json`) and `scripts/build_block112.py`.

## 1. 91846945: the 9 Larmgatan block (replaces pass 109)

Pass 109 had no photo. It built the whole outline as a generic three-storey volume at 9.75 m. The outline (about 1,000 m²) holds more than the restaurant, so it is split into six zones:

- **`r945`, the restaurant at 9 Larmgatan** (y 91.7–110.55 on Larmgatan, measured; back to x −310.1).
  - **Ground floor:** salmon render to 3.15 m, with a salmon base band at 3.15–3.85 m. Behind the terrace are four glazed openings and a glazed door, all estimated.
  - **Upper storey:** white render. Five arched windows on a 2.88 m pitch at y 95.3 / 98.2 / 101.1 / 103.9 / 106.8. They are 1.25 m wide, with sills at 4.9 m and arches to 6.95 m. Each has a black dome awning (to about 7.15 m) with a red band.
  - **Top:** a salmon cornice at 8.0–8.75 m.
  - **North end:** a salmon pilaster at y 110.0–110.55.
  - **Roof:** a low grey hipped roof to 10.6 m (estimated, not visible from the street).
  - **Terrace:** a black awning from 3.1 m at the wall to 2.45 m at 3.6 m out. It stands on light posts with a low glass screen and continues along the north house to y 118.5.
- **`se945`, the south range, east part** (y < 91.7, x > −310.1).
  - The Larmgatan front carries on in the same white and salmon design. One window was measured at y 89.4–90.8, 4.3–6.3 m high. It is rectangular, with a French balcony rail. Four more windows follow on the same pitch (estimated).
  - Above the cornice, a salmon gable faces Larmgatan. Its rake was measured rising about 0.57 m per m from y 91.7 (8.8 m) to y 87.3 (11.3 m). The roof is a red tile saddle running east–west, with the ridge at 13.45 m (extrapolated from the rake).
  - The Norra Långgatan face is not seen. It is given the same treatment (estimated).
- **`sw945`, the south range, west part, at Västerport** (x < −310.1). This is the "cream/red-pilaster house" in the tower photo.
  - **Ground floor:** red-brown to 3.10 m under a black awning, with a string course at 3.10–3.25 m.
  - **Upper floors:** cream render with two window rows, at 3.76–5.18 m and 6.07–7.52 m. The windows are 1.0 m wide, white, in groups.
  - **Pilasters:** red-brown, at the corner (s 0–0.5 from the west corner), at s 2.6–3.3, and repeated.
  - **Cornice:** red-brown at 7.88–9.35 m, with its lip to 9.6 m at the corner.
  - Windows at s 1.46, 4.08, 5.66 and 7.24 were measured. The rest of the front repeats that rhythm. The west face (seen edge-on) and the roof (a low hip to 11.2 m) are estimated.
- **`n945`, the cream house north of the restaurant** (y 110.55–127, front range to x −300.6).
  - Cream render with an upper window row at 3.10–4.30 m. The windows are 1.3 m wide, at y 111.3 / 113.3 / 115.4 / 117.4, with the rest at the same 2.0 m pitch.
  - Eaves at 5.2 m. A red tile saddle runs along the street, ridge 7.6 m. A chimney stands at y 113.2.
  - The ground floor is behind the terrace awning: windows and a door, estimated.
- **`k945` (a small rear piece) and `nb945` (the north house's back part):** plain and flat at 6.5 m and 4.5 m. Not seen.

## 2. 91072716: Gamla vattentornet (replaces pass 111)

The lead asked for an extra-careful review of the tower, so it was checked against four photos:

| Photo | Reliability | What it settled |
|---|---|---|
| `tower_lI6Z_h335_p25` (Google, pano lI6Z) | **The geometry reference.** Camera resected by pass 109 on outline corners and checked here, see Measurement. | Every absolute height on the tower: merlons, crown band, crown windows, corbel table, the upper bands and window rows. The radius of the crown and of the upper shaft. The angular position of the window columns. |
| `91846945_h255_p8` and pass 111's `91072716_h250_p20` (Google, pano r12kdG9) | Camera found from the tower (see Measurement), so it is no independent check of the tower's height. It does rule out 65 m (below). | The crown's design: tall narrow arched windows, the arcaded corbel table and the crenellation. |
| `tower_moat_full_user` (contributor photo, winter) | Position and heading unreliable. Pitch read as about 25° from the tower's own lean and the far shore (the capture says 35). | **Ratios only.** It shows that the tower stands on the rampart, with its foot well above the moat. It confirms the slender, nearly straight shaft under a wider crown, and window rows and thin bands going on down the shaft below the tree line of the Google view. |
| `tower_moat_crown_user` (the same photo) | Heavily distorted, no scale. | **Details only.** The arcade of small round arches with light outlines, the crenellated parapet, the shaft windows as pairs of small stacked lights in light surrounds, and many thin light bands. |

### Height: 54.0 m, not 65 m

Pass 111 measured the tower on one photo of its crown, from a panorama it could not resect, and found the parapet at 54.5 m (52–63 m). The lead then took the published 65 m and lengthened the shaft by 10.5 m. The lI6Z photo shows the whole tower above Västerport's vault, down to about 26.5 m, where a tree hides the rest.

**The Google pano clearly contradicts 65 m.** On the tower's near face, 46.9–47.3 m from the camera, it reads (heights above the street level the camera stands on):

| Feature | Height (m) |
|---|---|
| Merlon tops | 53.4 (52.5 for the outline radius 6.8, 53.8 for 5.6) |
| Crown band | 48.3 |
| Crown windows | 44.4–47.6 |
| Corbel table | 39.7–41.9 |

These agree with pass 111's reading from the other panorama: parapet 54.5 m, corbel table 40.0–41.8 m.

A 65 m tower would put its merlons at v ≈ 94 in this photo. The photographed top is at v 122, 28 px lower. The lengthened model's corbel table (50.2–52.3 m) would fall where the photo shows the crown windows. To read 65 m, the camera would have to be about 63 m from the axis instead of 52.9 m, and the house corner 5.4 m from the camera rules that out. A pano tilt error would have to be about 7°. The house in the same view reads plausibly (string course 3.3 m, cornice 9.6 m), which argues against that.

For the restaurant camera (r12kdG9) to show a 65 m tower, it would have to stand inside the buildings across Larmgatan. The street's far wall is at x −284.5, and the camera would need to be at x ≈ −282.5.

**So the tower is built 54.0 m to its merlon tops** (the mean of 53.4 and 54.5), and the shaft is not lengthened. The two values are in the zones (`t716`: `height` 52.5 is the parapet base, `top` 54.0). Raising both by the same amount in `prepare_block112.py` would lengthen the brick crown, not the shaft.

Where 65 m could come from, unchecked: pass 17's volume had its eaves at 60.85 m and 65 m "with antennas". A height above sea level would also be larger than the height above the street. Neither is checked.

### Ground at the foot (asked by the lead)

**The model has no rampart here.** A ray cast on the pass 111 blend found the ground flat at z ≈ 0 all round the tower (lawn 0.03–0.04 m, street 0.01–0.02 m, land −0.12 m, water −1.33 m), the same as at the Google cameras on Norra Långgatan and Larmgatan.

The moat photo shows the foot well above the moat. In proportion, the corbel table (its middle) stands 0.74 of the way up from the visible foot to the merlons: (top − foot)/(corbel − foot) = 1.35. With the lI6Z heights, that puts the visible foot about 5.0 m above the street level (4.6–5.3 for pitch 24–26°; 0.9 m at pitch 15° and 8.7 m at 35°). The pitch rests on the photo having no roll, so the figure is rough: **about 5 m, uncertain by about ±2 m.**

The model therefore stands the brick shaft on a battered stone base, 0–5.0 m, that fills the OSM ring (radius 6.8 → 6.6 m, with a coping). It stands in for the raised ground, which belongs to the terrain meshes and is not in this pass. The door towards the annex is in the base, and the annex (estimated) is kept as pass 111 had it. Setting `FT112 = 0` in `build_block112.py` drops the base and stands the shaft on the street, if a terrain pass models the rampart instead.

### Shaft, crown, windows and bands

- **Shaft-to-crown ratio.** From the foot (5.0 m) to the corbel table (39.7 m) is 34.7 m. From there to the merlons (54.0 m) is 14.3 m, a ratio of about 2.4. The moat photo's ratio, (top − foot)/(corbel − foot) = 1.35, matches this by construction, given the same foot height. Pass 111's lengthened version had 50.5 m of shaft under 14.5 m of crown, a ratio of about 3.5.
- **Taper.**
  - lI6Z: radius about 5.1–5.4 m at 33–36 m, about 5.6 m at the corbel table, about 6.0 m on the crown.
  - Moat photo, corrected for the depth difference along its pitched axis: the shaft at 20–30 m is about 0.86–0.9 of the crown's width, and nearly straight.
  - Model: the shaft tapers only slightly, from 6.0 m at its foot to 5.2 m under the corbel table, and the crown is 5.95 m. Pass 111 had 6.8 → 5.5 m. The OSM ring (6.8 m) is wider than the measured shaft and crown; it may trace the crown and parapet from above, or the base.
- **Corbel table.** Brick, as both the lI6Z photo and the moat crown photo show a brick arcade with light outlines. Thin stone rings run at its foot and top. It flares from 5.2 m to the crown between 39.7 and 41.9 m, with three-step brick corbels (32 round the ring).
- **Shaft windows.** Narrow openings (0.42 m) in stone surrounds, each split by a transom into two stacked lights, as the moat crown photo shows.
  - Seen in lI6Z: 33.0–35.6 m and 27.6–29.6 m.
  - The moat photo shows rows going on down to about 12 m. They are placed at the same 5.4 m step (22.2, 16.8, 11.4 and 6.0 m, estimated).
  - Eight columns, 22.5° either side of the line to the lI6Z camera (the two visible columns), starting at 23.3° in model angle.
- **Crown windows.** Eight tall arched windows at 44.4–47.6 m on the same columns, with a transom at 46.0 m. There is a sill band at 44.2 m and a band at 48.2 m.
  - The r12kdG9 crop suggests a closer spacing (about 24°) than lI6Z (about 45°). Eight are modelled.
- **Bands.**
  - Seen in lI6Z: 30.2, 32.1, 36.0 and 38.6–39.4 m, modelled at 30.1, 32.0, 35.9 and 38.5 m.
  - Below the tree line, the moat photo shows thin light bands all down the shaft. They are placed every 3.6 m from 8.6 to 26.6 m (estimated).
- **Parapet and cap.** As pass 111, on the lI6Z top: 52.5–54.0 m, 24 merlons with stone coping, and a low cap. The moat crown photo shows the crenellation.

## 3. 92204191: the beige house on Kaggensgatan (replaces pass 105)

### What pass 105 had

Pass 105 saw this house only obliquely, through a gap from Strömgatan. It modelled it as a green house with an orange saddle roof along Strömgatan and generic openings, with eaves at 6.3 m. It read the eaves at "about 6.4 m (one reading)" on the house's west end.

### Identification

Pass 108's 40 Kaggensgatan photo shows the house's **east face on Kaggensgatan** and its north face. Pass 108 resected that camera at (−184.60, 236.50, h 2.40). With that camera, the OSM outline projects onto the beige house:

- the north-east corner (−190.91, 231.61) reads at s 13.85–14.22 along the front, against 13.58 on the outline;
- the projected eaves line runs along the cornice.

So the beige house is 92204191, which confirms pass 108's identification. Its east face is a different face from the one pass 105 measured.

### Combined

- **Eaves.** This photo gives the cornice top at 6.44 m above the house's base, and pass 105 read about 6.4 m on the other side. The model uses 6.30 m, lowered after the first render put the cornice about 6 px high. Its lip reaches about 6.4 m.
- **Colour.** Beige render on every face. The north face is lit and reads paler. Pass 105's green is dropped.
- **Kaggensgatan front** (s from the south-east corner). Readings are shifted by −0.4 m along the front (the corner offset), and heights are taken above the house's base, which read 0.42 m.
  - Plinth to 0.30 m; cornice band 5.85–6.45 m.
  - Ground windows at s 9.96 and 12.38, 1.09–2.54 m. A dark door at s 8.35, 0.30–2.46 m, with a step.
  - Upper windows at s 7.39, 9.92 and 12.41, 3.68–5.26 m.
  - All windows have dark frames in light surrounds with sills.
  - South of s 6.6 (out of frame): two more axes at s 2.39 and 4.89 (estimated).
- **Roof.** A red-brown hipped roof (ridge 9.2 m) that cannot be seen from the street, with a large red-brown box dormer towards Kaggensgatan:
  - its front 0.5 m behind the wall face, s 6.5–9.3, top 9.25 m;
  - a four-light window at 6.95–8.05 m;
  - its north cheek sloping down to the roof at s 11.6, and a flat lid.
  - A chimney stands near the north-east corner.
- **North face.** Blank, with one small high window (seen).
- **South (Strömgatan) and west faces.** Not seen in this photo, so the openings there are estimated.

## 4. 93238202: the pale grey cottage on Östra Vallgatan (replaces pass 100)

**There is no new photo, so this correction is not a new measurement.** It comes from the lead's review of pass 101's finding: pass 101, measured against the ground in two views, found the bpmqiA1 camera about 0.5 m lower than the 2.54 m pass 100 used (cottage bases read 0.47–0.55 m). Every height pass 100 read from that camera therefore drops by 0.5 m. The design is pass 100's, unchanged:

| | Pass 100 | Pass 112 |
|---|---|---|
| Street gable: eaves / ridge | 2.00 / 3.85 | 1.50 / 3.35 |
| Window | 1.15–2.10 | 0.65–1.60 |
| West block (estimated): eaves / ridge | 2.20 / 4.20 | 1.70 / 3.70 |
| Flat link (estimated) | 2.40 | 1.90 |

The plinth (to 0.40 m), the boards, the corner boards, the tiled roof and the chimney (0.6 m below to 0.9 m above the ridge) keep pass 100's form. The two estimated parts behind are lowered by the same 0.5 m so that they stay in the same relation to the street gable. The new heights sit with pass 101's neighbour 93238209 (eaves 1.55–1.64, apex 3.30).

## Measurement

All photos are 756×405 except the tower photo (728×419). The vertical field is 90°. Points are taken on the facade planes 0.355 m outside the OSM lines, using `SCR/p82/hit.py` (vfov 90).

| Photo (pano) | Reported position | Camera used | How |
|---|---|---|---|
| `91846945_h255_p8` (r12kdG9) and pass 111's `91072716_h250_p20` (same pano) | (−288.03, 101.90) | (−288.48, 98.83), h 2.4 (assumed); pitch 6.5° (photo says 8) and 18.5° (photo says 20) | See "Camera r12kdG9" below. |
| `tower_lI6Z_h335_p25` (lI6Z) | (−329.88, 71.20) | (−330.52, 69.57, 2.05), pass 109's resection of the same pano (heading 152) | Checked in this view: the projected SW corner of 91846945, 5.4 m away, falls on the photographed corner, with the corner line's slope du/dv 0.367 against 0.366 projected and the cornice at 9.6 m. The tower's axis projects within 0.2 px of the silhouette's centre. |
| `tower_moat_full_user` / `tower_moat_crown_user` (user photo CIHM0og…, winter) | (−357.27, 109.13), unreliable | not resected; ratios only (pitch about 25° from the tower's lean, 24.9°, and the far shore, about 25°) | A rough camera on the tower's bearing at 72 m from the axis and 7.0 m up (the two-point fit to the top and corbel table) was used for one illustrative render. |
| `92204191_from40Kaggensgatan_h241_p15` (4whHB6) | (−184.03, 237.75) | (−184.60, 236.50, 2.40), pass 108's | The NE corner reads 0.3–0.6 m long. Readings were shifted −0.4 m along the front, and heights taken above the base reading (0.42 m), equivalent to a camera at 1.98 m. |

**Camera r12kdG9.** The restaurant photo has no outline corner in view, so the camera was found from the tower:

- **Bearing.** The tower's axis is at bearing −60.6°, which puts the camera on a line through (−331.3, 122.45).
- **Distance.** Along that line, the distance is where the tower's top, corbel top and corbel foot (53.4 / 41.5 / 39.7 m, from the tower photo) fit best: 48.9 m from the axis, with residuals −0.26 / +0.60 / −0.20 m.
- **Pitch.** It comes from the lean of two terrace posts, 6.0° and 6.8°.
- **Checks on this camera:**
  - the window sills come out level along the front (4.84–4.93 m);
  - the base band is level (3.84 / 3.85 m at both ends);
  - the window pitch is even (2.81–2.93 m) and the windows are 1.24–1.27 m wide;
  - the terrace's glass screen lands about 3.4 m in front of the camera, so the terrace is about 3 m deep, as seen;
  - the 250-heading view of the same pano gives the same sills (4.95 m), band (3.92 m) and cornice (8.67 m) at pitch 18.5°.
- **Error.** With the nominal pitch of 8°, the camera would sit 2 m nearer the wall and every height on the restaurant would drop by about 0.6–0.7 m, so heights there carry about ±0.5 m.

**Values read** (m above the pavement; y in local coordinates, s along the named front):

| House | Read | Value |
|---|---|---|
| Restaurant (r945) | base band | 3.14–3.85 |
| | upper sills | 4.84–4.93 |
| | window or awning tops | 7.11–7.17 |
| | cornice | 8.0–8.75 |
| | window centres y | 95.3 / 98.2 / 101.1 / 103.9 / 106.8 |
| | north end y | 110.55 |
| se945, Larmgatan | window | y 89.4–90.8, 4.3–6.3 |
| | gable rake | y 91.7 at 8.8 → y 87.3 at 11.3 |
| sw945, Norra Långgatan | string course | 3.09–3.25 |
| | lower windows | 3.76–5.18 |
| | upper windows | 6.06–7.53 |
| | window heads | s 0.6–2.0, 3.6–4.6, 5.2–6.1, 6.7–7.4 |
| | pilasters | s −0.2–0.3 and 2.55–3.25 |
| | cornice | 7.88–9.35, 9.6 at the corner |
| n945 (on the wall line) | upper windows | 3.09–4.30, y 110.7–118.0 |
| | eaves | 4.9–5.2 |
| | chimney | y 113.2 |
| | ridge | about 8.0 if the ridge is 4 m back |
| Tower | as in section 2 | |
| 92204191 | as in section 3 | |

## Estimated

- **91846945:**
  - the restaurant's and the south range's ground-floor openings;
  - the restaurant's and the west house's roofs;
  - the east part's south face on Norra Långgatan;
  - the west house's windows beyond s 7.5 and its west face;
  - the ridge of the gable roof (extrapolated from about 4.4 m of rake);
  - the north house's ground floor, its windows beyond y 118 and its ridge (7.6 m);
  - the split lines x −310.1 and x −300.6;
  - the back pieces.
  - The split between the restaurant and the south range (y 91.7) is where the gable's rake starts and the cornice line has no break, so the east part may in fact be the same building as the restaurant under a different roof.
- **Tower:** the foot's height (about 5 m from ratios in an unreliable photo) and the stone base standing in for the rampart, the shaft's detail below 26.5 m (rows and bands placed at regular steps where the moat photo shows that they continue), the door, the annex, and the exact number of crown windows.
- **92204191:** the south and west faces' openings, the roof form (hidden; a hip is assumed), the dormer's depth and lid, and the chimney's position.
- **93238202:** everything, as stated above: the correction is the lead's, not a new reading.
- **Colours** are by eye.

## Verification

- **Zones** (`previews/block112-zones.json`): 12 zones in 4 meshes, footprint 1220.3 m², zoned 1220.2 m², 0.0 m² outside OSM, 0.04 m² not zoned, overlap 0.013 m². `prepare_block112.py` prints `BLOCK112_ZONES_OK`.
- **Sandbox:** four runs, all with the pass 111 prelude. All printed `BLOCK112_GEOMETRY 4` and `SANDBOX_DONE` with no errors. Runs 3 and 4 followed the lead's request for a closer tower review: base, taper, bands, paired windows.
  - Renders were made at photo size from the cameras above. The tower view was rendered 756×405 at vfov 88.06° (the photo's focal length) and cropped to the photo.
  - Side-by-side and 50% blends of the final run are in `SCR/p112/cmp4_v945.jpg`, `cmp4_v945b.jpg`, `cmp4_vtw.jpg` and `cmp4_v191.jpg`. `SCR/p112/ztw4.png` puts the lI6Z tower and the moat photo next to their renders. The dormer close-up from run 1 is `SCR/p112/z191dorm.png`. Aerials, the moat view and the 93238202 street view are in `SCR/p112/sb4/`.
- **Restaurant.** The five arched windows, the awnings, the base band, the cornice and the north end line up within a few pixels in both headings. In the 250 view, the French-balcony window and the salmon gable rake at the top left fall where the photo has them.
- **Tower.** In the lI6Z view, the top (v 122), the corbel table, the crown windows and the two window columns line up. In the moat view (illustrative camera), the size and the shaft-to-crown proportion match. The photo's strong lean is not reproduced, which suggests the user photo's projection or roll differs from the capture's values. The west house's corner, cornice, pilasters and windows line up roughly. Its west face reads somewhat wider in the render.
- **92204191.** Windows, door, plinth and cornice line up. In run 1 the dormer was too small and low, and the cornice about 6 px high. Run 2 matches the dormer's top and window band, and the cornice.
- **Degenerate faces.** `drop_degenerate_faces112`, with the `_thin` test, runs on each mesh right after `s21_finish`. Faces dropped in run 2: 91846945 194, 91072716 5, 92204191 0, 93238202 28. The sampled ones are:
  - 91846945: 2e-6 m² triangles at the arched holes' spring and crown, in `bz_wall`'s spandrel prisms;
  - the tower: the cap's zero-radius top ring, plus four zero-area quads at 4.02 m along the annex's joint with the tower (pass 111 also dropped 5);
  - 93238202: gable rod and gutter ends, the same count as pass 100's 28.
  - No hole is visible in the renders.
- **Pending:** the official build, the FBX export check and the Unreal checks. The lead fills in the build results.

## Limitations

- **Restaurant camera.** It cannot be resected on outline corners. Its scale rests on the tower heights from the other photo and on a pitch read from post lean, so heights on 9 Larmgatan carry about ±0.5 m.
- **Tower height.** The model now disagrees with the published 65 m by 11 m. Two Google panoramas support 53.4–54.5 m above the street, so it is built to 54.0 m, but the lead should decide. The foot's height (about 5 m) comes from an unreliable photo, and the terrain under the tower is flat in the model. The lower shaft is seen only in that photo, at low resolution.
- **The rest of the 945 block.** The Norra Långgatan face of the east part, the restaurant's ground floor, the roofs and the back are not photographed.
- **Extra views that would help:**
  - Gamla vattentornet's lower shaft, clear of the tree: local (−333, 98), Street View heading 335, pitch 35.
  - 91846945's south face east of x −310: local (−302, 70), heading 332, pitch 15.
  - The north cream house head-on: local (−289.5, 119), heading 242, pitch 15.
  - 92204191's Strömgatan face: local (−195, 212), heading 333, pitch 15 (as pass 105 asked).
- **Omitted:** sign lettering, the round restaurant sign, tables, chairs, plants, flags, lamps and downpipes.

## Official build

The lead's build of pass 112 passed the Blender geometry checks and the FBX export, and two rebuilds gave identical meshes. The prevhash check reports the four intended corrections and nothing else: pass 100 (93238202), pass 105 (92204191), pass 109 (91846945) and pass 111 (91072716), besides the earlier intended changes to pass 85 and pass 98. The Unreal import and its checks are deferred.

**The lead's decision on the tower height.** Pass 111's build had set the tower to 65 m from Swedish Wikipedia ("65 meter högt"). That figure carries no source in the article. The same article gives 15 storeys, which fits about 54 m better than 65 m. This pass measured 53.4 m to the merlons from the lI6Z pano, whose camera is resected, and found that 65 m is ruled out by the house corner 5.4 m from the camera. A measurement against a resected camera outweighs an unsourced figure, so the lead kept this pass's 54.0 m. If a reliable source for 65 m turns up (for example a building permit or a land survey), the `t716` zone values can be raised.
