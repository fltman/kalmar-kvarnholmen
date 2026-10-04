# Pass 139: the mainland around Järnvägsgatan and Tullslätten

Pass 98 built the mainland houses as plain volumes inside three chunk meshes. Pass 139 takes the 19 pass-98 outlines along Järnvägsgatan and Tullslätten and their small side streets (Odengatan, Frejagatan, Tullbron, Unionsgatan and the Järnvägsgatan end of Södra vägen) out of those chunks. Each becomes its own mesh `SM_Slott139_<osm id>` (category `Slottsområdet/Mainland`, `detail_pass` 139), standing on pass 98's ground height (model z 0.30). This is the last mainland street group; the mainland yard buildings beyond 25 m of any street are a separate later job and are not touched.

Each house gets:

- storeys (1, 1.5, 2, 3 or 4), the eaves and ridge heights, a stone plinth and, on houses over a basement, the basement windows;
- the roof: saddle, hip, Swedish mansard (gambrel, with gable ends), hipped mansard or flat, in red, brown or dark tile, red or grey sheet metal;
- render in the house's colour, vertical boarding with white corner boards, red brick (Tullbroskolan) or yellow brick (Frejagatan 8);
- eaves boards, white bargeboards on the gables, gable windows on the steeper gables;
- windows per storey (casement, surround, sill), white, red or dark frames; a door on the wall facing the street, steps where the door stands on the plinth;
- dormers, chimneys and these features, new in this pass or reused from pass 136:
  - Järnvägsgatan 3 (93333646): white pilasters with brown capitals between every third window bay, the stone door portals with a small green copper gable roof, the brown tile hipped mansard roof with dormers;
  - Järnvägsgatan 9 (93333631): the explicit split into the higher main part and the lower east section, the gabled entrance porch;
  - Frasses (93309088): the raised roof lantern (a glazed band and its own low hip);
  - the Jugend blocks on Odengatan and Frejagatan (93325628, 93325650): iron balconies, two per upper floor on the street front;
  - Frejagatan 3 (93326740): the central gable on the street front (pass 83's `frontis83`) on a grey sheet hipped roof;
  - Frejagatan 5 (93291993): the shop windows on the ground floor;
  - Tullbroskolan (91222178): an explicit H-plan split into three parts and stepped brick gables (five steps a side) on every gable end;
  - the gymnasium (93252919): the tall hall windows and the clerestory row, the pent roof over the hall windows at 6.6 m, the buttresses between the bays and the tall chimney.

## Selection

The selection is computed in `scripts/prepare_block139.py` from the OSM street lines in `references/osm-slott98.json` (ways with `highway` and `name`). It takes every outline in `source/block98.json['buildings']` that lies within 25 m of one of the pass's streets and whose nearest named street is one of them. It leaves out the Stagnell chapel 500979084 (pass 107) and every id (and demolished id) listed in any `source/blockN.json` with N < 139, pass 138's `source/block138.json` included (it existed when this pass was finalized: 61 ids, all in chunk W).

The streets are Järnvägsgatan, Tullslätten, Tullbron, Unionsgatan, Odengatan, Frejagatan and Södra vägen.

- Odengatan meets Järnvägsgatan at its north end. Frejagatan is the next street of the same quarter, between Vegagatan and Bremergatan. Tullbron and Unionsgatan meet Järnvägsgatan and Tullslätten.
- Södra vägen is in the list for its stretch at the north end of Järnvägsgatan: the one unclaimed outline nearest it is Frasses (93309088) at the crossing; every other Södra vägen outline was claimed by earlier passes.
- None of these streets is one of pass 138's (Stensövägen, Stensviksvägen, Långviksvägen, Sturevägen); pass 138's ids are excluded explicitly anyway.

No outline within 25 m is nearer another street, so `left_to_other_streets` is empty.

**Station and railway buildings.** Kalmar C (passes 24/28, `source/station24.json`, `source/block28.json`) stands on Kvarnholmen at about (−420, −95), not in pass 98's mainland set, and no pass-98 outline along the railway part of Järnvägsgatan (south of y 40) lies within 25 m of the street. None of the 19 ids appears in any other script or source file except as a neighbour reference (passes 119 and 134 name 93325650 and 93325628 as neighbours or left-to-other-streets).

That gives 19 outlines, all built: 91222178, 91222193, 91933162, 91933165, 93252919, 93291993, 93309088, 93309089, 93309101, 93325628, 93325650, 93326740, 93326744, 93333631, 93333637, 93333642, 93333646, 93333649, 93333654.

**Clipped outline.** 93326740 touches pass 98's model box at y 320 (vertices 1 and 2 lie on it); only a corner is cut, and the house is built on the clipped outline.

**Chunks.** 8 of the outlines lie in pass 98's chunk M (−1150 ≤ x < −850, by the outline centroid) and 11 in E (x ≥ −850); none in W. The build adds the 19 ids to `SLOTT98_DETAILED` (which keeps the ids of every earlier pass in the chain) and calls pass 115's `slott98_chunks115({'M','E'}, 139, block139_names)`. The two chunks are re-created by pass 98's code without these houses, keep `detail_pass` 98 and get `rebuilt_by_pass` 139. They are among this pass's meshes (21 names in all).

**Pass 138.** Pass 138's houses lie in chunk W, which this pass does not re-create, so the two passes share no chunk. In the official chain `SLOTT98_DETAILED` accumulates, so M and E stay correct whichever pass runs later.

**Not covered by any street pass.** Within 25 m of a street there are still 19 unclaimed outlines in the far west, nearest Ringgatan (6), Torsgatan (5), Baldersvägen (3), Lillegårdsgatan (2), Stensövägen (2 pieces of the clipped 93326725) and Margaretaplan (1). Pass 138 lists four of them as left to other streets and 93326725 as clipped. They are not around Järnvägsgatan or Tullslätten, so this pass leaves them; see Limitations.

## Zones

Pass 116's slab method (as copied by passes 134 and 136):

- An outline that fills 85 % of its box in the frame of its longest edge is one zone; otherwise it is cut into slabs at its vertices and merged into a main body and wings, or flat-roofed annexes under 12 m² or narrower than 2.6 m (full height on blocks of three storeys or more).
- 93333631 has an explicit split read on `jv1_h197`: the higher main part covers the first 10.2 m of the street front from vertex 0 (south-east), and the lower east section covers the rest. Both ridges run along the street.
- Tullbroskolan (91222178) is an H in plan. The slab method gave one box over the whole H, so the outline is cut explicitly across the frame from vertex 1 to vertex 2 at 12.14 m and 34.8 m into the north wing, the middle body and the south wing. Each part is boxed with its ridge along its long side, and each is a main zone with its own door and stepped gables.
- Each zone's walls follow the OSM outline exactly; walls against a neighbouring zone or house start at the neighbour's eaves.
- The door goes on the outer wall that faces one of the pass's streets. Corner houses facing none use the nearest of Bremergatan, Vegagatan, Olof Palmes gata, Jenny Nyströms gränd, Esplanaden or Stationsgatan.

## Measurement

Photos: 28 views captured for this pass with the claude-in-chrome extension in its own tab (closed afterwards), `captures.txt` lines `139|`, files in `SCR/p139/`, all 608 × 458, vertical field of view 90°, pitch +10°. They show April 2025 imagery, except sv1_h181 (June 2025). Google imagery was used as a view-only reference; nothing was downloaded.

| Files | Pano | Shows |
|---|---|---|
| jv1_h197 | ZcX3GcGLG6LRaoCS1d5Kzg | Järnvägsgatan 9: the brown boarded villa (93333631) |
| jv2_h197 | E7mHrMK2zD6W4q4bzHFz5w | the white house with the black mansard roof (93333642) |
| jv3_h197 | kLyFip6JTLDo97PoeMXFQA | Järnvägsgatan 7 behind the hedge (93333654) |
| jv4_h159, jv5_h236 | KJWI0u7A9JaqzcOC5wMb1A, qT4CfU6aJMfRMXe4aPb07A | Järnvägsgatan 3, the long yellow block (93333646) |
| sv1_h181 | ZThv6s5V_mGmJjoQU-o4wQ | Frasses (93309088) |
| od1_h124 | LWgyYfVu_yxglUvJq7gGMg | Odengatan 1 (93333637) |
| od2_h124 | vlfXZdNVy8ob5uV-OsMHvA | Odengatan 7 (93309101) |
| od3_h346, od4_h263, od5_h21, od6_h219, od7_h188 | Z2OY3nTyyMl-qS6QWDfKCg, H5QBbDnySl85c3IJpE10dQ, yGye5LKxs2O0FYzPYqpY8A, mxOFv5mOxCPNwyLRbkLQww, nHoq53D_Aq3Gv3AxnPTBNA | the Jugend block 93325628 (close, scaffolding), the garage 93309089 |
| fj1_h162, fj2_h83, fj3_h302, fj4_h123, fj5_h303, fj6_h214, fj7_h26 | LKJivw6lk42B9wGFrtfJ8A, JvKtlApyxQhVHMdGsuGFXQ, CplSIrZXKlrY9eTIyO6VqQ, hGDsviVvAnHcQsUlmN17ug, GCPfO44ryruvzqQo6mfA0Q, Fpqt8JDw7gFTNTpRt8oCkQ, 0UUGrq_GVrDRNpUn4IfGMA | Frejagatan 3, 4, 5 and 8 |
| tb3_h8, tb4_h290, tb5_h292 | VKhoEpZxf-8FnQ-EMPjB9A, dy4zQmHX8p7LmrnmPWb4VQ, SFh-OQxkQ8Yk9NuwXaMYdw | Tullbron from Järnvägsgatan (across the railway) and from Olof Palmes gata |
| ts1_h307, ts3_h11, ts5_h48, ts6_h83 | Up1tiEs5CA-FGOqFK8rIEA (two views), eSAKTBuVXvipYp2I9cDvlQ, tYwd1TPdF1mg-gwl5lCLkw | Tullbroskolan and the white school building |
| un1_h164 | MwS6Umhs3UyRNaSMcow_wQ | the gymnasium on Unionsgatan (93252919) |

- **Identities.** All pass-98 outlines within 70 m were projected into every view from the Google positions (`SCR/p139/ov139.py`, a copy of pass 138's overlay; overlays `ov_*.png`). Every built house was identified this way, except 93333649 (it overlaps the villa's porch in jv1_h197 and is not clearly seen) and 91933162 (behind trees and buses).
- **Measurement.** Heights are read on the OSM wall plane with `hit` (`SCR/p139/m139.py`, vfov 90). Two cameras are resected with `SCR/p100/res.py` on the two front corners of the house; the others stand at the Google position at an assumed 2.5 m.

| View | Google position (x, y) | Camera used (x, y), height | Corners | Used for |
|---|---|---|---|---|
| jv1_h197 | (−791.72, 232.70) | (−793.19, 231.48), 2.31 (from the base) | 93333631 v0 and v1 | the villa's eaves and ridge |
| od2_h124 | (−946.00, 206.19) | (−947.90, 207.48), 2.5 | 93309101 v0 and v1 | the pink house's eaves and wall gable |
| jv4_h159, jv2_h197, jv3_h197, od1_h124, fj7_h26, ts1_h307, un1_h164 | Google | Google, 2.5 | none | the readings in the table, marked "pano position" |
| all other views | Google | Google, 2.5 | none | identification, storeys, colours |

With the Google camera, the resected villa's eaves read 5.3 instead of 4.6 and the pink house's 4.4 instead of 4.9. So the unresected readings below carry an uncertainty of roughly ±0.7 m.

### Houses

Heights are metres above the ground (model z 0.30). "Estimated" means read from storeys, doors, windows and the roof pitch by eye.

| OSM id | Identity | Photo | Storeys | Eaves / ridge | Roof | Measured or estimated |
|---|---|---|---|---|---|---|
| 91222178 | Tullbroskolan: red brick three-storey 1880s school with the stepped gables, arched windows and brick friezes | ts1_h307, ts5_h48, ts6_h83 | 3 | 11.5 / 15.5 | dark saddle | eaves about 9-11 above the base, inconsistent between columns (grazing view, pano position not resected; the yard lies lower than the street); 11.5 used from the three tall storeys |
| 91222193 | white rendered flat-roofed two-storey school building behind Tullbroskolan (the school yard was a building site in 2025) | ts3_h11 (behind the site fence) | 2 | 7.2 / 7.45 | dark flat | estimated |
| 91933162 | yellow rendered two-storey house with a red tile roof behind the trees at Tullbron (seen only far) | tb3_h8 (far, behind the buses) | 2 | 6.4 / 9.4 | red tile hip | estimated |
| 91933165 | yellow rendered two-storey house with the dark mansard roof and dormers at Tullbron | tb3_h8 (across the railway, about 50 m), tb4_h290 | 2 | 7 / 10.6 | dark hipped mansard | estimated |
| 93252919 | red boarded gymnasium with the big white windows, the buttresses, the pent roof over the lower hall wall, the clerestory and the tall brick chimney | un1_h164 (close) | 1 | 9.2 / 11.4 | dark saddle | base at z -0.25, the pent roof at 6.4-6.5, the clerestory window tops at 8.7-9.1, the chimney top at 12.4-12.9 (pano position, camera 2.5 assumed); so the pent 6.6 and the eaves 9.2 above the base |
| 93291993 | brown-beige rendered four-storey block with the shop windows on the ground floor and a low dark roof (Frejagatan 5) | fj4_h123 (close), fj7_h26 (right edge) | 4 | 12.4 / 13.8 | dark saddle | estimated |
| 93309088 | Frasses: grey boarded one-storey kiosk with a low hipped roof, the raised roof lantern and the blue sign | sv1_h181 (June 2025) | 1 | 3 / 4.4 | dark hip | estimated |
| 93309089 | small white garage with a red tile roof in front of the white house | od7_h188 (behind the hedge) | 1 | 2.5 / 4 | red tile saddle | estimated |
| 93309101 | pale pink rendered one-and-a-half-storey house with the red tile hipped mansard roof and the wall gable on the street (Odengatan 7) | od2_h124 (resected) | 1.5 | 4.8 / 10.8 | red tile hipped mansard | camera resected on the two front corners to (-947.90, 207.48), 2.3 m from the pano position; with a 2.5 m camera the base reads 0.58 (behind the fence), the eaves 5.46 and the wall gable apex 11.98, so about 4.9 and 11.4 above the base; 4.8 and 10.8 used (the pano-position reading gave 4.4 and 10.2) |
| 93325628 | cream rendered four-storey Jugend apartment block over a grey stone basement with the iron balconies; white with red window frames at the Vegagatan end (in scaffolding in 2025) | od6_h219, od3_h346, od4_h263, od5_h21 (close, scaffolding) | 4 | 14.2 / 17.6 | red tile saddle | estimated |
| 93325650 | white rendered four-storey Jugend corner block with the red tile roof, the rounded corner bays and the iron balconies (Frejagatan 4) | fj7_h26, fj1_h162, fj2_h83 | 4 | 14.2 / 17.6 | red tile saddle | base at z 0.38, eaves 14.6 (14.2 above it) near the west corner (fj7_h26, pano position, camera 2.5 assumed) |
| 93326740 | cream rendered four-storey 1910s apartment block with arched windows, the curved central gable over the stone portal and the grey sheet hipped roof (Frejagatan 3) | fj3_h302, fj7_h26 | 4 | 14.4 / 17.2 | grey sheet hip | base at z 0.42, eaves 14.8 (14.4 above it) and the gable apex 19.3 on the west front plane (fj7_h26, pano position, camera 2.5 assumed) |
| 93326744 | yellow brick three-storey block over a basement with a low roof and the two entrances (Frejagatan 8) | fj5_h303 | 3 | 10 / 11.8 | red sheet saddle | estimated |
| 93333631 | dark brown boarded villa with the steep brown tile roof, dormers and two red brick chimneys; the lower east section with its own roof; the gabled entrance porch (Järnvägsgatan 9) | jv1_h197 (resected) | 1.5 | 4.7 / 10.6 | dark brown tile saddle | camera resected on the two front corners to (-793.19, 231.48), 2.31 m above the ground from the base; eaves 4.6 above the ground, the ridge read at 8.9 on the front plane, carried back 4.25 m to about 10.4; the east section about 0.9 m lower (read from the pano position) |
| 93333637 | dark brown boarded one-and-a-half-storey gambrel villa with the brown tile roof, the cross gable and the glazed veranda (Odengatan 1) | od1_h124 | 1.5 | 3.6 / 8.4 | dark brown tile gambrel | eaves 4.3 (3.4 above the base at 0.9) and the roof read at 7.0 on the front plane (pano position, camera 2.5 assumed) |
| 93333642 | white rendered two-storey house with tall storeys, the black tile mansard roof and two dormers, behind the hedge on the stone wall | jv2_h197 | 2 | 8.6 / 12.2 | dark hipped mansard | eaves read at 9.1 on the OSM front plane above the street (pano position, camera 2.5 assumed; the base is behind the hedge), 8.6 used; the roof top seen at 12.0 on the front plane |
| 93333646 | long yellow rendered two-storey 1920s block over a basement with the brown tile mansard roof, round-topped dormers, white pilasters and the stone door portals (Järnvägsgatan 3) | jv4_h159, jv5_h236 | 2 | 8 / 12 | dark brown tile hipped mansard | base at z 0.65, eaves 8.7 on the street front at the north-west corner, so 8.1 above the base (jv4_h159, pano position, camera 2.5 assumed) |
| 93333649 | small dark brown boarded annex behind the villa (seen only as an overlap in jv1_h197) | not seen | 1 | 2.6 / 4 | red-brown tile saddle | estimated |
| 93333654 | yellow rendered two-storey house with a red tile roof and the gable dormer, behind the hedge (Järnvägsgatan 7) | jv3_h197 (behind the hedge) | 2 | 7 / 10.6 | red tile saddle | eaves read at 8.8 on the OSM front plane from the pano position (the base is hidden; not trusted, 7.0 used from the storeys) |

Colours are read by eye from the photos and set as flat targets on the town textures (`M_Block139_<Key>`).

## Estimated

- Every value marked estimated above, and all ridge heights except the carried-back ridges of 93333631 and 93309101 (the roofs are mostly seen only from the street).
- The roofs of the Jugend blocks 93325628 (not seen; red tile assumed like its neighbour 93325650), 93291993, 93326744, 91933162 and 91222193 (flat, seen only behind the site fence).
- The heights of the four-storey blocks other than 93325650 and 93326740 (93325628 takes their values; 93291993 is estimated from its storeys).
- Tullbroskolan's height: the readings on ts1_h307 disagree between columns, because the view grazes the front and the yard lies lower than the street. 11.5 m is used from three tall storeys. The stepped gables are a generic five-step silhouette.
- Window counts: regular bays (2.7 m on two-storey houses, 2.9 m on others), not the real positions; the arched windows of 93326740 and Tullbroskolan are drawn square.
- Doors: one per main zone on the street wall; the position along the wall is a rule.
- Dormer counts (one per 6.5 m of street slope, two on 93333642), chimney places, the balcony positions (two per upper floor on the door wall), the pilaster spacing (every third bay), the portal size, the lantern and the gymnasium's pent roof (6.6 m, from un1_h164) and buttresses.
- 93333649 (a small annex behind the villa) is identified only by its outline.

## Verification

- **Zones** (`previews/block139-zones.json`, `BLOCK139_ZONES_OK`): 46 zones cover the 19 outlines, 7956.6 m² of 7956.6.
  - 0.0 m² lies outside OSM and 0.03 m² of OSM is not zoned (slivers at the cuts).
  - The overlap is 0.006 m²; the outlines themselves do not overlap.
  - Status: passed.
- **Sandbox**, through the wrapper `SCR/p139/build_block139_check.py`. The wrapper hashes every mesh in the scene before the build, runs the build twice in one session as the official build does, and hashes again. It then checks that no detailed outline is drawn by the re-created chunks, and runs the export frame check with the export tail's preparation and `export_district_fbx` to a temporary file (deleted after each mesh).
  - **Run 1** (prelude `rebuild_block137`) printed `BLOCK139_GEOMETRY 21` twice; all the checks below passed in it too. The comparisons showed four things to fix:
    - The gymnasium's north front had come out as a flat 3.1 m annex in front of a set-back hall. It is now one box (`ONEBOX` in the prepare script).
    - The brown tile roofs of Järnvägsgatan 3, Järnvägsgatan 9 and Odengatan 1 read red; they now use a darker tile (`TileDark`).
    - The gymnasium's roof and pent roof are now dark.
    - Frasses' lantern was too small and has been enlarged.
  - **Run 2** (prelude `rebuild_block138`, so pass 138's official chain, its chunk W included, was in the scene), after the fixes:
    - `BLOCK139_GEOMETRY 21` twice: 19 houses and the chunks M and E.
    - Repeatability: `REPEAT139 True`. The two runs give identical geometry hashes (vertices, loops, material indices, UVs and material names) on all 21 meshes; there are 19 `SM_Slott139_` objects.
    - Hashes before and after: only `SM_Slott98_Buildings_E` and `SM_Slott98_Buildings_M` changed (intended). There are 19 new meshes, all `SM_Slott139_*`, and none is gone. No other mesh in the scene changed; pass 138's `SM_Slott98_Buildings_W` and its houses are untouched.
    - Shared names: `G` and `TS` are the same after the build as before it. The build sets `G` to the ground height only while it runs, for pass 115's `steps115`, and restores `TS`/`TC` at the start.
    - Chunk exclusion: none of the 106 other detailed ids in M and none of the 52 detailed ids in E (ours and others) has a chunk vertex more than 0.8 m inside its outline, with one exception. 93325650 has 51 such vertices, all from the pass-98 roof of the unclaimed courtyard building 93325656. That building is still drawn by the chunk, and its roof (pass 98's `frame98` box, 93 % fill, plus a 0.35 m overhang) reaches about 6 m² into 93325650's outline. This is the neighbour's own pass-98 geometry, not a failure to exclude 93325650, and it goes away when the yard job details 93325656. The chunks still draw 13 volumes in M and 10 in E.
    - Export frame check: `CHECK139_TOTAL_INVALID 0 EXPORTS_OK 21 OF 21`.
    - Degenerate faces dropped by `drop_degenerate_faces139`: 454 per build over the 19 house meshes (0–107 per mesh).
    - `SANDBOX_DONE prelude 138`.
  - **Pass 138 in the chunk check.** In run 1 the prelude was 137, so pass 138's houses were still drawn by chunk W. That is expected: this build does not touch W, and the global `SLOTT98_DETAILED` accumulates through the official chain. Run 2 already had pass 138's official chain in the prelude. The two passes share no chunk.
- **Comparison** with the photos. Each view is rendered at the photo size (608 × 458) from the cameras above and put side by side with the photo in `SCR/p139/sb1/cmp_*.png` and `SCR/p139/sb2/cmp_*.png`. Most cameras stand at the Google position, so houses sit 1–3 m off their photo positions.
  - Järnvägsgatan 3 (jv4_h159, jv5_h236): the long yellow block, its basement windows, the two storeys, the white pilasters, the hipped mansard roof with dormers and the red chimneys match. The photo's dormers are round-topped and fewer at the near end; the model's are boxes. The model has one portal per zone where the photo has two.
  - Järnvägsgatan 9 (jv1_h197, resected): the boarded front, the lower east section, the porch at the west end and the steep roof match in form and height. The photo has three large dormers; the model has one per 6.5 m.
  - The white house (jv2_h197): the two tall storeys, the black mansard roof and the two dormers match closely.
  - Frasses (sv1_h181): the low grey boarded kiosk and the hipped roof with the lantern match. The sign and the serving windows are drawn as plain windows.
  - Odengatan 7 (od2_h124, resected): the pink walls, the wall gable on the front, the eaves and the roof match. The real gable has a curved top; the model's is straight.
  - Odengatan 1 (od1_h124): the brown boarded villa and its roof are in place. The cross gable and the glazed veranda are not modelled.
  - The Jugend blocks (od6_h219, fj7_h26): the four storeys, the eaves, the red tile roof of 93325650 and the grey hipped roof of 93326740 match. The corner bays and towers, the wavy render bands and most iron balconies are missing; the model has two balconies per floor on one wall.
  - Tullbroskolan (ts1_h307, ts6_h83): the three brick storeys, the H plan and the stepped gables match in kind. The arched windows, the friezes and the awnings are not modelled.
  - The gymnasium (un1_h164): after the fix, the big hall windows, the pent roof, the clerestory row and the buttresses read as in the photo. The camera is not resected and stands about 2 m off.
  - Frejagatan 5 and 8 (fj4_h123, fj5_h303): the brown block's shop windows and the yellow brick block's three storeys over a basement match.
  - Not compared in detail: tb3_h8 (Tullbron, 50 m away across the railway) and od5_h21 (scaffolding).
- **Official build:** done by the lead on 2026-10-04; see "Official build". The Unreal checks are pending.

## Limitations

- Only two cameras are resected. Most heights are read from the Google positions with an assumed 2.5 m camera (about ±0.7 m) or estimated from storeys. Ridge heights and roof pitches are mostly estimated.
- The houses are boxes on the OSM outline with rectangular roofs; small notches are covered by the roof or by flat annexes (at full height on the blocks of three storeys or more).
- Window and door positions are regular bays, not the real ones. The dormer counts, balcony positions and pilaster spacing are rules. The Jugend blocks' corner bays, towers and render ornament, Tullbroskolan's arched windows and friezes, and the curved gables are not modelled.
- 93326740 is clipped by pass 98's model box at y 320 (one corner).
- 93325656, an unclaimed courtyard building still drawn by chunk M, overhangs about 6 m² into 93325650 with its pass-98 roof (see Verification); the yard job should detail it.
- No fences, hedges, garden walls or sheds outside the OSM outlines are modelled.
- **Not assigned to any street pass:** 19 unclaimed outlines within 25 m of a street in the far west of the mainland, nearest Ringgatan (93566356, 93566367, 93566385, 93505709, 93505730, 93505770), Torsgatan (93487556, 93487572, 93487582, 93487584, 93487589), Baldersvägen (93487569, 93487574, 93487591), Lillegårdsgatan (93505686, 93505704), Margaretaplan (93358537) and Stensövägen (93326725, clipped). Pass 138 left four of them (93487556, 93487582, 93487569, 93358537) to other streets. They do not belong to the Järnvägsgatan/Tullslätten group, so this pass does not take them. The lead should decide whether they go to the yard job or to a small street pass.
- Extra views that would help, as location (x, y), Street View heading and pitch:
  - Tullbron (91933165, 91933162) close up from the path at (−560, 70), heading 300, pitch 10 (no Street View coverage was found on the path itself);
  - the roof and the cross gable of Odengatan 1 (93333637) from (−880, 245), heading 110, pitch 15;
  - the white school building 91222193 from Unionsgatan at (−495, 325), heading 170, pitch 10, once the building site is cleared;
  - a resectable view of Frejagatan 3 (93326740) from the Vegagatan crossing at (−1050, 275), heading 50, pitch 20.

## Official build

The lead built pass 139 officially on 2026-10-04.
- **Geometry and export:** the geometry check passed on the second rebuild (True), the FBX audit passed (exit 0), and the two rebuilds gave identical meshes.
- **Prevhash:** only intended changes.
  - `SM_Slott98_Buildings_M` and `_E` are re-created without this pass's 19 houses. M shows under pass 134; E shows under the earlier mainland passes.
  - Pass 138's 62 meshes are identical.
  - The rest are known earlier corrections.
- **Dry renders:** cameras 765–774, 10 of 10.
