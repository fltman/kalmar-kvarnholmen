# Pass 123: correction of pass 115 (Slottshotellet, Kalmar konstmuseum, Byttan, two park buildings)

Pass 123 re-creates five of pass 115's meshes. They keep the same names and categories (`Slottsområdet/Buildings`), and each gets `detail_pass` 123 and `corrects_pass` 115. Every other pass-115 mesh and the pass-98 chunks are untouched. The five houses were already in `SLOTT98_DETAILED`, so no chunk changes.

| Mesh | Building |
|---|---|
| `SM_Slott115_93332243` | Slottshotellet |
| `SM_Slott115_91931339` | Kalmar konstmuseum |
| `SM_Slott115_91222116` | Byttan |
| `SM_Slott115_874870421` | the grey boarded park pavilion |
| `SM_Slott115_91222187` | an unidentified park building, kept in pass 115's form |

Files:
- `scripts/prepare_block123.py` re-zones the five pass-98 outlines and writes `source/block123.json` and `previews/block123-zones.json`.
- `scripts/build_block123.py` builds the five meshes.

## Sources

- Five contributor photos (`SCR/p123`, the `123|` lines in `captures.txt`), all 728 × 419 with a 90° vertical field of view:
  - `hotel_yard_main.jpg`, `hotel_yard_a.jpg` and `hotel_yard_c.jpg` from one panorama in the hotel courtyard;
  - `park_pav_a.jpg` and `park_pav_b.jpg` from one panorama in Stadsparken.
- Pass 115's photos (`SCR/p115`), mainly `konstmuseum_byttan_user_h20.jpg`, `byttan_user_h106.jpg` and `molinsgatan3_h20.jpg`.

The positions and headings of the contributor photos are unreliable, as the task warned, so no camera was resected from them. Where a position was needed, it was worked out from the plan and the content of the photos, as described below.

## Slottshotellet (93332243)

**Pass 115 had:**
- a red rendered main range (zone `shm`, s 0–16.6 along the south-east front) under a red tile hip, eaves 7.6 and ridge 12.6, with two estimated front cross gables;
- the north-east part of the outline (`shn`) under a low red hip, eaves 7.2;
- the green west wing (`shg`): a saddle roof with eaves 3.3 and ridge 7.0, slate roof, ochre trim and carved drops on the bargeboards.

The courtyard side was never seen; the main range was only seen from 55–88 m behind trees.

**How the new photos were mapped to the outline.** The outline was written in a frame along the south-east front: s along vertex 15→16 (bearing 28), t inwards towards the north-west. In that frame:
- the outline is a 27.4 × 9.9 m range (s 0–27.4, t 0–9.88);
- a 7.0 × 3.4 m risalit stands on the south-east front (s 16.2–23.2);
- two parts project into the courtyard on the north-west side:
  - a 5.1 × 2.3 m rectangle (s 2.0–7.2);
  - a 7 m wide polygonal bay (s 16.2–23.1, 4.5 m deep, with 45° chamfered corners);
- the green wing is rotated 27° at the south-west end.

The courtyard lies between this north-west side, 93332240 to the west and 93332247 to the north. The footpath through it leaves by the gate towards Molinsgatan.

The three courtyard photos come from one panorama, so their headings differ by reliable amounts (0, 130 and 250). Their content places the camera at about (−760.5, 55.0), in the passage about 3.4 m north-west of the green wing. From there:
- the north-west side of the hotel lies at local bearings 55–105;
- the gate lies at about 227;
- 93332240 lies at 300–350;
- 93332247 lies at about 15.

This matches the photos with one heading offset (local bearing ≈ photo heading − 41°). Reading the photos with that offset:
- `hotel_yard_main` (left to right):
  - the white-pillared glazed porch with the roof terrace is the polygonal bay;
  - two red bays follow, then the tall red cross gable, which is the 5.1 m projection;
  - the low green building with a black roof and scalloped ochre eaves is the green wing seen along its courtyard side, together with the link;
  - the green gable at the edge is the green wing at close range.
- `hotel_yard_c` looks out through the gate. The green wing is on the left. The dark grey-green two-storey wing with the terrace railing and blue dormers is on the right: that is **93332240**, which the Molinsgatan photo also shows at its left edge. The grey boarded two-storey house beyond the gate is across Molinsgatan, most likely **387312777**.
- `hotel_yard_a`: the dark wing again (93332240), and the low dark-roofed restaurant ranges with glazing to the north, which are **93332247** (and probably 1433973300).

The dark wing, the restaurant ranges and the gate house are therefore **not part of this outline**. They stay as pass-98 chunk volumes, as the task required the chunks to be left alone.

**What pass 123 builds** (zones `hm`, `hr`, `hx`, `hp`, `hg`, `hl`):
- **Main range `hm`.** Red render on a 0.5 m plinth, two storeys of windows in white surrounds, and grey pilaster strips at the ends and between bay pairs.
  - The red tile hip (eaves 7.6, ridge 12.6) covers the whole 27.4 m range.
  - The courtyard slope has two dark dormers: the wide triple one above the porch (s 20.6) and a single one beside the cross gable (s 10.3).
  - There are two chimneys.
  - The green courtyard door, with a lantern, is at s 8.7, left of the cross gable as in the photo.
- **Courtyard cross gable `hx`.** It projects 2.3 m and is 5.1 m wide. It has two storeys of windows plus the gable storey with its attic window, a narrow stair window, and dark verges.
  - The gable rises from the main eaves (7.6) to an apex of 10.2.
  - Its roof runs back into the main slope.
- **Glazed porch `hp`.** It is 3.6 m high, with white posts, a 0.75 m white parapet, glazing with white mullions and a white fascia. The roof terrace has a dark timber railing.
  - The glass door is on the face looking straight into the courtyard, under a red awning (the photo shows one).
- **Front risalit `hr`.** It carries a cross gable towards Slottsvägen (apex 11.1) with an attic window, and the main entrance under a flat canopy on brackets.
- **Green wing `hg`.** Pass 115's form is kept: eaves 3.3, ridge 7.0, gables to the south-west and north-east, attic windows in both gables, and ochre bargeboards with carved drops. It is refined to match the photos:
  - the roof is **black** (both courtyard photos and the Molinsgatan photo show a very dark roof);
  - a **scalloped ochre trim** runs along both eaves, as on the courtyard photos;
  - the windows are **cross-barred** (diagonals in each sash) in ochre frames with ochre surrounds;
  - the corner boards are ochre.
- **Link `hl`.** The 4.9 m² strip between the wing and the cross gable: green boards and a flat black roof at 3.1 m with an ochre fascia.

**Heights.** The storey rows were read from `hotel_yard_main`:
- the ground-floor and first-floor rows are 53 px apart, taken as about 3.0–3.2 m;
- the main eaves come out at about 6.9–7.6 m above the ground, which agrees with pass 115's 7.6, so 7.6 is kept;
- the cross gable's eave stubs sit at the main eave height;
- its rise is about 0.48 × its width, after correcting the photo's vertical squash. The squash was measured on a window, whose width-to-height ratio is 1.25 in the photo against about 1.56 in reality. For 5.1 m that gives a rise of about 2.5 m, so the apex is drawn at 10.2.

The ridge (12.6), the risalit gable (11.1) and the dormer sizes are estimates.

**Differences from the task's description.**
- The photos show the main roof in **red tile** (the Molinsgatan view shows the same), not dark. The dark roof in `hotel_yard_main` is the green wing's. The main roof stays red.
- The pilaster strips on the main range are **grey**, not white. The white pillars belong to the porch.

## Kalmar konstmuseum (91931339)

**Pass 115 had** one black prism, 17.5 m high, on the whole outline, with rib panels on a 1.25 m grid, a glazed entrance under a sign band on the short north-west faces, three large windows, and the landing and steps.

**Reading the outline.** The outline was written in a frame along its south-east side (vertex 4→5, s), with t towards the north-west. It consists of:
- a 17.4 × 17.3 m core;
- a 3.8 m wide strip on the south-west side, against Byttan (s −3.8–0, t 8.7–20.8);
- a stepped north-west front: t 20.8 at s −3.8–0.55, t 23.1 at s 0.55–6.7, t 21.7 at s 6.7–12.3 and t 17.3 at s 12.3–17.4.

The museum photo (camera north-west of the entrance, looking south-east) shows, from right to left:
- Byttan;
- the low glazed entrance with the "Kalmar konstmuseum" sign band. This is the 3.8 m strip: its north-west face is in line with Byttan's park front;
- the tall tower directly left of it, with the banners. This is the 6.2 m front at t 23.1;
- a lower volume further left whose upper part is cantilevered over a dark recess on a slanting soffit, with a still higher volume behind it.

**Massing built:**
- `ml` entrance link: 4.6 m high. Both ends are glazed with dark mullions and a black sign band. Pass 115's landing and three steps are kept, widened 3.4 m along Byttan's front.
- `mt` tower: s 0–6.7 over the full depth, **18.5 m**.
- `mc` core: s 6.7–17.4, **16.0 m**.
- `mf` front block: s 6.7–12.3, t 17.3–21.7, top 14.0. It is cantilevered over a recess on a soffit that slants from 6.0 m by the tower to 8.0 m at its north-east end. The recess wall below is black with a glazed band.
- **Tall glazed slot:** the 1.4 m face between the tower and the front block (OSM vertices 9–10), glazed from the ground to 15.2 m with dark transoms.
- Cladding: shingle courses, with a lip every 0.77 m and staggered vertical joints about 0.9 m apart, on all black walls.
- Two large windows: one high on the park (north-east) face of the core, one on the south-east face. Their places are not verified.

**Height reasoning (the tower, 18.5 m):**
- About 24 shingle courses can be counted on the tower face, from the grass to the top edge, in the museum photo (a brightness profile and an enlarged strip).
- Near the base, the glazed entrance storey (from the floor to the underside of the sign band) spans 53 px, about 4.2 courses at the same distance. Taking that storey as 3.2–3.4 m gives a course of about 0.77 m, so 24 × 0.77 ≈ 18.5 m.
- The entrance is slightly farther from the camera than the tower face, which would make the true value a little lower. The uncertainty in the storey height spans about 17–20 m. Pass 115's own reading of the same photo with an assumed camera gave 18–20 m.
- 18.5 m is drawn, one course above pass 115's 17.5.
- The lower volume's top meets the tower at about course 19, which is about 14.5 m. This is drawn as the front block's 14.0 top. The higher volume behind it is drawn at 16.0 (estimated).

## Byttan (91222116)

**Pass 115 had:**
- the white rendered storey (eaves 3.9) under a low dark roof with 0.95 m eaves, on a grey plinth, with dark-barred windows;
- an upper storey set back 4.6 m on every side (a 9 × 17 m box to 7.0 m) with a band of windows;
- a chimney.

**Changes, from pass 115's two photos:**
- **The park front.** Byttan's north-west front (OSM 0→1) is in line with the museum's entrance face, which places the photos' features along it.
- **The upper storey** is not centred. In the museum photo it starts a little south-west of the junction with the museum and covers less than the front. In `byttan_user_h106` it covers the middle and far part of the front, with the chimney at its north-east end.
  - It is now a 10 × 9 m box in the front's frame (s 3.6–13.6 from the museum end, t 3.5–12.5), white, from 4.6 to 7.3 m (model z).
  - It has a band of 1.2 m windows in dark frames, a white cornice, a low dark roof with a 0.6 m overhang, and the white chimney at its north-east end.
- **The terrace.** A 2.4 m deep stone terrace (0.5 m high) runs along the park front from s 6.0 to 17.4. It has an iron railing on its outer edge, as in `byttan_user_h106`. It is open towards the museum steps.
- **The glass door** is on the park front at s 4.6, by the museum steps.

The positions along the front are read from the two photos without a resected camera (perspective is only roughly allowed for), so they are estimates within about ±2 m.

## The park pavilion (874870421) and 91222187

**Pass 115 had** both as plain cream rendered pavilions, chosen without any view:
- 91222187 under a red hip;
- 874870421 under a low dark roof.

**Identification.** The two park photos come from one panorama, given at (−754.9, −103.8). Kalmar slott at the far left of `park_pav_b` anchors the heading: with the castle at local bearing ≈220 and at −36° from the view centre, `park_pav_b` looks along about 256, and `park_pav_a` (90° to the right) along about 346. Then:
- **`park_pav_a`, the grey boarded pavilion with the glazed front and dark roof, is 874870421.** It appears at +35° from the centre, which predicts bearing 21; the outline's bearing from the panorama is 20 (23 m away).
- The dark flat-roofed building with the white fascia at the right edge (+55 to +63°, bearing about 41–49) is the museum and Byttan direction (bearings 44–49), not a park outline.
- **`park_pav_b`, the open shelter with the dark roof on posts and the white back wall, is not 91222187.** The shelter stands at about bearing 236–251, while 91222187 lies at 277, 97 m away, where a 13.6 m building would look about half as wide as the shelter does. No pass-98 outline lies in the shelter's direction within about 100 m, so the shelter appears not to be mapped in OSM. The render from the same camera (`SCR/p123/sb1/cmp_pb.png`) shows the castle in place and open park where the shelter is.
- No photo therefore identifies 91222187. It is re-created in pass 115's form: a cream rendered pavilion under a red tile hip, with eaves 3.0, top 5.6 and one door, now in pass 123's code.

**874870421, as built** (frame along its south side, OSM vertex 3→4):
- **Main body `pv`:** 10.5 × 5.6 m in grey vertical boards with white corner boards, eaves 2.7, and a dark saddle roof (ridge 4.6) along the south side with white bargeboards and white eave trim.
  - The **east gable end is glazed** from 0.8 m up to the eaves, and so is the **east half of the south side**, with white mullions and transoms, as in the photo.
  - The west half of the south side has one window.
- **Annex `pn`:** the rest of the irregular OSM hexagon (51.5 m²), in grey boards with windows, flat dark roof at 2.6 m, and a door on its north-west side. Its form is estimated; the photo shows only the main body.

## Measurement summary

| Photo (panorama) | Camera used | How it was found | Used for |
|---|---|---|---|
| `hotel_yard_main`, `_a`, `_c` (CIHM0ogKEICAgICzsc_hLw) | (−760.5, 55.0), 1.7 m; local bearing = heading − 41° | from the plan and the content of all three photos (not resected) | hotel zones, storey rows, cross gable, porch, green wing |
| `molinsgatan3_h20` (pass 115) | pass 115's (−766.0, 41.5) | pass 115 | green wing roof colour, 93332240 at the left |
| `konstmuseum_byttan_user_h20` (pass 115) | (−713.7, −39.7), 1.7 m, heading 100 (also pass 115's invented camera) | estimated from the entrance's place in the frame | museum massing, course count, Byttan upper storey |
| `byttan_user_h106` (pass 115) | pass 115's camera, heading 184 | estimated | Byttan upper storey, terrace and railing |
| `park_pav_a`, `park_pav_b` (CIHM0ogKEICAgID4-fOpJw) | the given position; local bearing = heading + 146° | heading anchored on Kalmar slott | pavilion identification |

| Building | Measured (photo readings) | Estimated |
|---|---|---|
| Slottshotellet | main eaves about 6.9–7.6 (drawn 7.6); cross gable rise ≈ 0.48 × width (apex 10.2); order of the parts along the courtyard side | ridge 12.6; risalit gable 11.1; dormer sizes and places; porch height 3.6; all of the south-east and north-east sides |
| Konstmuseum | about 24 shingle courses on the tower; entrance storey ≈ 4.2 courses; lower volume top ≈ course 19 | tower 18.5 (range 17–20), core 16.0, front block 14.0, soffit 6.0–8.0, slot height, window places |
| Byttan | order of features along the park front | upper storey extent (±2 m), terrace depth, door place |
| 874870421 | glazing pattern and roof form (photo at an unresected camera) | all heights; the annex |
| 91222187 | – | all (no view) |

Colours are read by eye from the photos and set as flat targets on the town textures (`M_Block123_*`).

## Verification

- **Zones** (`previews/block123-zones.json`): 14 zones cover the five outlines, 1520.5 m² in all.
  - 0.08 m² lies outside OSM and 0.12 m² of OSM is not zoned.
  - The overlap is 0.088 m², exactly the overlap of the OSM outlines themselves (the museum and Byttan touch).
  - Status: passed.
- **Sandbox** (prelude `rebuild_block122`): two runs, both printing `BLOCK123_GEOMETRY 5` and `SANDBOX_DONE`.
  - The second run used 91222187 in pass 115's form and ran the export check below.
  - Degenerate faces dropped by `drop_degenerate_faces123` (with the `_thin` test):
    - hotel 69;
    - museum 18;
    - Byttan 0;
    - pavilion 1126, mostly board strips cut by the glazing openings;
    - 91222187 0.
- **Export frame check** (`SCR/p123/build_block123_check.py`, the pass-119 wrapper pointed at this build): after the build it ran the export preparation and the exporter's tangent-frame test on all five meshes. Result: `CHECK123_TOTAL_INVALID 0`, `EXPORTS_OK 5 OF 5`. Repaired frames were 28–384 per mesh, with no invalid loops.
- **Comparison with the photos** (side by side in `SCR/p123/sb2/cmp_*.png`; the aerials are in `sb2/airs.png`, `airh2.png` and `airm2.png`):
  - `cmp_main2` and `cmp_main`, hotel courtyard: the porch with its terrace, the red bays, the dormers and the cross gable with its attic window appear in the photo's order, with the green wing with the black roof, scallops and cross-barred windows at the right. The camera is not resected, so sizes in the frame differ.
  - `cmp_yc`, the view to the gate: the green wing's courtyard side reads correctly. 93332240 at the right is still pass 98's plain volume.
  - `cmp_km2`, museum: the stepped tower, the cantilevered front block, the entrance link and Byttan with its terrace and upper storey stand in the photo's order. The camera is estimated.
  - `cmp_pa`: the grey pavilion's glazed east end and glazed south half match the photo.
  - `cmp_pb`: the castle is in place, and the shelter's position has no building, as discussed.
- **Pending:** the official build, the repeatability check of two rebuilds, the FBX export in the official chain, and the Unreal checks. The lead fills in the build results.

## Limitations

- **Unresected cameras.** None of the cameras could be resected, so all photo readings are ratios within a photo (storeys, courses, window proportions), not absolute measurements.
- **Slottshotellet:**
  - The south-east and north-east sides are still estimates: the front risalit gable and its entrance, the window bays and the chimneys.
  - The courtyard wings that the photos show (the dark grey-green wing with its terrace and blue dormers, and the restaurant ranges) belong to the outlines 93332240 and 93332247 (and probably 1433973300), which stay as pass-98 chunk volumes. A later pass could model them.
- **Konstmuseum:**
  - The park and lake sides are not seen.
  - The window places on them and the core's height are estimates.
  - The shingles are courses and joints, not individual panels.
  - The banners and the KK sign are not modelled.
- **Byttan:** the south-east and south-west sides are not seen. The timber annex at the south-west end of the park front (seen in both photos) is not modelled.
- **Park buildings:**
  - 91222187 remains unidentified.
  - The open shelter of `park_pav_b` does not seem to be in OSM, so it is not modelled.
  - The pavilion's annex is a guess.
- **Extra views that would help,** given as location (x, y), Street View heading and pitch:
  - the hotel's south-east front from Slottsvägen near (−725, 35), heading 300, pitch 10;
  - the museum's park side from (−670, −30), heading 200, pitch 15;
  - 91222187 from the park path near (−835, −95), heading 250, pitch 5.

## Official build

The lead's build of pass 123 passed the Blender geometry checks and the FBX export, and two rebuilds gave identical meshes. Prevhash reports pass 115's five corrected meshes as changed; that is intended. The other changes are the earlier intended ones. The Unreal import and its checks are deferred.
