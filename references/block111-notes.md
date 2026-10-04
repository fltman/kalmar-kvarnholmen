# Pass 111: the last street-facing pass-17 volumes (Storgatan east, Proviantgatan, Ölandsgatan, Stationsgatan, Ölandskajen, Larmtorget)

Pass 111 replaces eight scattered generic district volumes from pass 17 with detailed buildings. All eight had `detail_pass` 17 or none in `source/district17.json`; nothing above pass 17 is touched.

- **91926352 (SM_Building_91926352, 50 Storgatan): the 1940s grey-beige rendered block.**
  - The outline is split at the step in the street front (x 125.15).
  - Zone `m352`, the four-storey range on the corner (front x 111.4–125.15): a dark slate plinth to 2.10 m, four window rows (bottoms 2.30 / 5.30 / 8.35 / 11.40 m, 1.65 m high), five axes at a 2.9 m pitch in white surrounds with beige roller blinds in a fixed pattern, a cornice at 13.6–14.5 m and a flat roof. The task said "four-storey"; the resection agrees (four rows over the high plinth).
  - Zone `w352`, the wing set back 2.4 m to the east: three window rows over a plinth with basement windows, nine axes at 2.35 m, a cornice and a flat roof at 11.0 m.
  - The district had this whole outline at 7.1 m.
- **91926324: the light-grey 1.5-storey house.** Four green-framed windows (1.95–3.70 m) on a grey plinth (0.90 m), eaves at 4.3 m, a red tile saddle roof with its ridge at 9.4 m, a red dormer over the middle window, two pairs of roof lights and a chimney near the ridge.
- **91926325: the gate, the low wing and the yard.** The resection settles the task's question: the cream two-storey gable house with the lunette starts at x ≈ 168.6, east of this outline (it is 91926300, not part of this pass). 91926325 holds:
  - `gw325` (s 0–2.2 from the west corner): the green board gate (1.74 × 2.72 m) in a white wall to 3.0 m;
  - `lw325` (s 2.2–6.3): the low grey one-storey wing, eaves 3.2 m, one window in a white surround, white corner strips and a low red saddle roof (ridge 4.1 m);
  - `bk325`: the white two-storey part seen above the wing (eaves about 6.4 m), from y 4.5 to the back of the outline, with a red saddle roof;
  - `yd325` (s 6.3–9.5): an open yard behind a 2.0 m white wall with an iron gate (s 8.3–9.4).
- **91846953 (1 Proviantgatan): the sage-green two-storey house.** Zone `f953` (the front range, x ≥ 164.5):
  - a dark plinth to 0.95 m;
  - ground windows at 1.80–3.55 m and upper windows at 4.95–6.90 m, on five axes (s 2.1, 4.4, 7.15, 10.05, 12.8 from the south corner), in white surrounds with white panels under the sills;
  - a green double door at s 15.1 under a sixth upper window;
  - white corner strips and two white pilaster strips at s 5.7 and 11.5 (rusticated lines on the ground floor), a white string course at 3.9–4.5 m and a cornice at 7.6–8.4 m;
  - the central pediment over s 4.3–12.9 with its apex at 10.7 m and a lunette with three glazing bars;
  - a low red hipped roof (ridge 10.6 m).
  - The wing to the south-west (`w953`) is not seen. It is plain sage render with two rows of simple windows and a hipped roof (eaves 7.2, ridge 9.2 m), estimated.
- **91846937 (30 Ölandsgatan): the small yellow boarded house.** Horizontal boards, white corner boards and eaves board, two board-clad garage doors (s 0.4–2.9 and 5.1–7.6, 2.2 m high), the red door up two steps in a white pedimented surround (pediment top 3.8 m), eaves at 4.2 m and a red tile hip roof (ridge 7.2 m). The other faces are boarded and blank (not seen).
- **91931337 (Stationsgatan): the grill kiosk.** Red posts, white panels to 1.0 m, glazing at 1.0–2.65 m and green awnings on the two street faces (west and south), a dark sign band at 3.4–4.25 m above the roof edge on those faces, and a low dark hipped roof (top 5.0 m). **Correction to the task notes:** the green copper roof with lantern turrets seen in the photo is not the kiosk's. A ray through it passes the kiosk and first meets 91222222, about 39 m from the camera; the kiosk has a low dark roof behind its sign band.
- **149000060 (Ölandskajen): the white corrugated shed.** The task said "about 1.5 storeys"; it measures about 3 m.
  - East part (`e060`, s 0–17.4 from the east end): walls to 3.0 m, a low saddle roof (3.35 m), a window strip at s 12.1–17.4 (1.55–2.30 m), a blue round logo at s 4.6 and a door at s 2.4.
  - West part (`w060`): walls to 2.6 m with the roofline sweeping up in a curve to 3.6 m at the west end, a window strip at s 17.6–23.4 (2.0–2.4 m) and the second logo at s 21.3.
  - Vertical corrugation ribs every 0.3 m on all faces.
- **91072716: Gamla vattentornet.** The OSM outline is the whole tower (a ring of radius 6.7–6.9 m about (−331.3, 122.45)) plus a small annex on its east side. The pass-17 tower (eaves 60.85 m, 65 m with antennas) is replaced:
  - a brick shaft tapering from radius 6.8 m at the ground to 5.5 m at 40 m, with stone bands at 0, 9.0, 19.5 and 30.0 m, small round windows in eight vertical rows at eight levels, and the door towards the annex;
  - a stone corbel table at 39.7–41.8 m (three-step corbels, 32 round the ring) flaring to the crown;
  - the brick crown (radius 5.95 m) to 53.0 m with eight tall arched windows (44.0–46.6 m) and stone bands at 48.6 m and under the parapet;
  - a crenellated parapet (24 merlons) to 54.5 m with stone coping, and a low metal roof cap inside it;
  - the annex: a brick porch with a door and a flat roof at 4.0 m (estimated, not seen).

## Measurement

The local frame and the tools are the project's standard ones: `SCR/p100/res.py` (vfov 90), `SCR/p82/hit.py` and `meas.py` at 756 × 405. The facade plane is the OSM line offset 0.355 m outward. Heights are above the pavement at the facade.

| Photo (pano id) | Google position (x, y) | Resected camera (x, y, h) | Method | Measured |
|---|---|---|---|---|
| 91926352_h332 (v5zzUgNr…) | (117.81, −4.23) | (117.07, −6.55, 2.55) | Four-point resection on both corners of the four-storey front (plinth top and cornice). h from the plinth foot. | Plinth top 2.10; window rows 2.27–3.88, 5.23–6.94, 8.28–10.03, 11.41–13.16; cornice 13.63–14.53; axes measured within 0.15 m of the symmetric 2.9 m pitch; wing cornice 10.6 |
| 91926324_h332 (S8CmMDRN…) | (148.67, −4.40) | (146.08, −7.10, 2.78) | Three-point resection: both corners of the house and the end of the wing above its eaves. h from the plinth foot. | Plinth 0.9; windows 1.95–3.72; eaves 4.32; skyline 9.3–9.7 at the mid-depth plane; dormer top 9.1; chimney top 11.0; window axes s 2.0 / 4.15 / 6.55 / 8.55 (OSM s); wing cornice 11.5 (0.9 m above the other photo's 10.6; 11.0 used) |
| 91926325_h332 (3lneHnOK…) | (158.84, −4.45) | (158.01, −7.58, 2.72) | Four observations on the 1.5-storey house corners and the block's east end. Residual about 1.3 m on the house's west corner (grazing). | Gate s 0.36–2.09, top 2.98; wing s 2.2–6.2, eaves 3.18, window 1.50–2.79 at s 4.26; back part eaves about 6.3–6.6 (front plane assumed at y 4–5); yard wall 1.97, iron gate s 8.2–9.5; the cream house's corner pilaster at s 11.8 (x 168.6) |
| 91846953_h242 (gHt8HbMK…) | (184.16, −106.61) | (182.81, −109.60, 2.50) | Resection on the south corner (foot and eaves) and the pediment's centre line. h from the plinth foot. | Plinth 0.93; ground windows 1.75–3.6; string course 3.9–4.5; upper windows 4.83–7.0; cornice 7.4–8.3; pediment apex 10.7, span s 4.94–13.58 (centred within 0.6 m of the front's middle, 8.6 used); pilasters s 5.4–6.0, 11.6–12.3 |
| 91846937_h337 (JOrgcZuk…) | (131.40, −149.39) | (130.49, −154.68, 2.58) | Two-corner resection (foot and eaves of both corners). | Eaves 4.19; ridge line 7.2 at the ridge plane; door s 3.4–4.33, 0.6–2.84; pediment top 3.8; panels s 0.1–2.87 and 5.15–7.9; boards above 2.2 |
| 91931337_h31 (bTPWhIQY…) | (−367.02, −127.14) | (−369.51, −132.93, 2.5 assumed) | Three-corner resection (SW, NW, SE corners). The kiosk's foot is hidden behind a van, so h is assumed. | Roof edge about 3.4; sign top about 4.4; awning about 3.2 |
| 149000060_h141 (66Wg02io…, upscaled half tile) | (−417.96, −254.26) | (−417.75, −256.60, 2.5) | One corner (the east end) plus the distance from the ground line at the image centre for h 2.5. The far curve then lands at s 30.1 against the 30.8 m outline, which supports h 2.5. | East part eaves 2.96, roof edge about 3.2–3.35; west part eaves 2.6, the curve up to about 3.3–3.6 at the end; joint s 17.4; window strips as above |
| 91072716_h250_p20 (r12kdG9_…) | (−288.03, 101.90) | (−288.03, 101.90, 2.5), nominal, not resected | Only the tower top over the restaurant is seen; no known corners. Heights from the ray elevation at the tower's near face (centre distance 47.9 m minus radius 6.5). As a check, the same camera puts the restaurant's cornice at 10.5 m, which is plausible for its two tall storeys. | Parapet top 54.5; antenna tips about 58.5; crown at the corbel table about 40–42.5; with the camera ±2 m along the view: parapet 52.2–56.7. Silhouette half-angle 6.66° → crown radius about 5.6 m at 47.9 m |

## Estimated

- **The water tower's height.** The task expected about 30 m. The photo does not allow that: the parapet top is 53.6° above the horizontal at about 41 m, which puts it at about 54.5 m (52–57 m for ±2 m on the camera position). The pano could not be resected, and the tower's bearing in the photo is 4° off the bearing from the nominal pano position, so the camera is probably 3 m or so off sideways. If the crown has the outline's full radius (6.8 m) rather than the 5.6 m its silhouette gives at the nominal distance, the camera would be about 55 m away and the parapet about 63 m (the pass-17 value). **The height is therefore settled only to about 52–63 m, with 54.5 m modelled.** It is not 30 m. The shaft below 40 m, its taper, the round windows, the bands and the door are not seen and are estimated, as is the annex.
- **91926352.** The rear of the four-storey range (to y 31.9), the wing's back and the roof form (flat behind the cornice) are not seen. The wing's height (11.0 m) is the mean of two readings (10.6 and 11.5).
- **91926324.** The ridge is at the mid-depth plane (9.4 m from a skyline reading of 9.3–9.7 m). The chimney's position in depth is estimated.
- **91926325.** The joint at y 4.5 (the back of the wing), the width and roof of the two-storey part and everything behind the street wall are estimated.
- **91846953.** The wing `w953` entirely, the roof's height (ridge 10.6 m) and the door's exact width.
- **91846937.** The garage doors are read as doors from their handles and vents; the other three faces are not seen.
- **91931337.** The camera height (the foot is hidden), the roof form behind the sign band and the north and east faces.
- **149000060.** The roof's form on the east part, the back (south) face and the curve's exact shape. The photo is an upscaled half tile.
- **All houses.** Colours are judged by eye from the photos.

## Verification

- `KALMAR_GEO=SCR/pylib python3 scripts/prepare_block111.py` prints `BLOCK111_ZONES_OK`:
  - footprint 1789.3 m², zoned 1789.2 m²;
  - outside OSM 0.06 m², OSM not zoned 0.2 m², overlap 0.03 m².
- The sandbox (prelude: rebuild chain 109 in the first run, 110 in the later runs) ran three times and printed `SANDBOX_DONE` with no errors, and `BLOCK111_GEOMETRY 8`.
- `drop_degenerate_faces111`, with the `_thin` test, runs on every mesh right after `s21_finish`. Faces dropped in the last run: 91926352 5, 91926324 30, 91926325 28, 91846953 34, 91846937 0, 91931337 22, 149000060 162, 91072716 5. These are zero-area or sliver faces left by the edge bevel at abutting boxes, roof edges and the shed's rib and curve strips; they were not inspected one by one. In the first two runs the tower lost 1355 and 1739 faces, from double-sided round-window and arched-glass faces lying a few millimetres from their frames. Those faces were made single-sided, and the tower now loses 5. The renders show no visible holes.
- Renders at the photos' own size with the resected cameras were compared side by side with the photos (`SCR/p111/cmp3_c*.jpg`):
  - **50 Storgatan:** the four-storey front's edges, plinth, window rows and cornice line up; the set-back wing's cornice is about 0.3 m high in the render.
  - **The 1.5-storey house:** corners, eaves, windows, dormer and roof lights line up; the ridge reads right.
  - **91926325:** gate, wing, window, yard wall and iron gate line up; the two-storey part behind is a little wider than the real one.
  - **1 Proviantgatan:** the south corner, window axes, pilasters, bands, cornice and pediment line up within about 0.3 m.
  - **30 Ölandsgatan:** corners, eaves, roof, door and panels line up.
  - **The kiosk:** it sits about 1 m narrower in the render than in the photo (the resection used grazing corners).
  - **The shed:** the east end, both window strips, the logos and the upswept west end line up.
  - **The water tower:** the restaurant in front is pass 109's generic 9.75 m volume and stands higher in the render than the real one, so only the top of the crown shows; a separate close view (`SCR/p111/sb3/tw2.png`) shows the corbel table, the arched windows and the crenellations.
- The official build, the export check and the Unreal checks are pending; the lead fills in the build results.

## Limitations

- **The water tower** rests on one photo of its top from a pano that cannot be resected. A view of the whole tower would settle its height and the shaft's details: for example from Västra Vallgatan at about (−334, 76), 46 m south of the tower: heading about 335 (bearing about 3), pitch 25.
- **91926325's back part** and the yard are only seen over the street wall.
- **The kiosk's sides** away from the street and its roof are not seen.
- **Omitted.** Signs' lettering, the kiosk's menu boards, lamps, pipes, antennas, the cars and the trees.

## Official build

**Tower height, changed by the lead.** Swedish Wikipedia ("Gamla vattentornet i Kalmar") gives the tower's height as 65 m, which is above the photo's 52–63 m range. The pano could not be resected, so the lead took the published value. `build_block111.py` now lengthens the shaft by `D111 = 65.0 − max(TOPZ, CR+1.40)` (10.5 m) and lifts the corbel table, crown, parapet and cap by the same amount, so the proportions read from the photo are kept. Two round-window rows (42.0 and 46.5 m) and a stone band at 40.5 m were added to the longer shaft; they are estimated. The highest point of the saved mesh is 65.0 m. The 54.5 m parapet reading above therefore no longer matches the model: either the nominal pano position is several metres off, or the crown is larger than its silhouette suggested.

**Build result.** The build passed the Blender geometry checks and the FBX export, and two rebuilds gave identical meshes. Passes 28–110 are unchanged except the earlier intended changes (pass 85's prison building, corrected by pass 103, and pass 98's three meshes re-created by pass 107). The Unreal import and its checks are deferred.

**Seen in the calibration render.** The building in front of the tower in the 9 Larmgatan view is a generic three-storey volume. The photo shows a white two-storey restaurant with arched windows, so that building needs a later pass.
