# Pass 140: the last mainland street houses

Pass 98 built the mainland houses as plain volumes inside three chunk meshes (W, M, E). Passes 107 and 115–139 took the houses street by street. Pass 140 takes the street houses that no street pass claimed: 21 outlines, mostly in the far west on Ringgatan, Torsgatan, Baldersvägen, Lillegårdsgatan and Margaretaplan, the clipped yellow brick block on Stensövägen at the model's north edge, and three free-standing houses a little beyond 25 m from their street (Södra vägen, Lilla Dammgatan, Söderportsgatan). Each becomes its own mesh `SM_Slott140_<osm id>` (category `Slottsområdet/Mainland`, `detail_pass` 140), standing on pass 98's ground height (model z 0.30). After this pass only yard and back buildings are left undetailed on the mainland (59 outlines, listed at the end).

Each house gets:

- storeys (1, 1.5, 2 or 3), the eaves and ridge heights, a stone plinth and, on houses over a basement, the basement windows;
- the roof: saddle, hip, Swedish mansard (gambrel, with gable ends) or flat, in red or dark tile or dark sheet metal;
- render in the house's colour, vertical boarding with white corner boards, red brick (93505709), yellow or yellow-brown brick (93487584, 93291989, 93326725);
- eaves boards, white bargeboards on the gables, gable windows on the steeper gables;
- windows per storey (casement, surround, sill), a door on the wall facing the street, steps where the door stands on the plinth;
- dormers, chimneys and these features, new in this pass or reused from passes 138 and 139:
  - 93566356 (Ringgatan, white): the iron balcony on its south-west gable at the attic floor (`end_balcony`, new);
  - 93566385 (Ringgatan, ochre): two red wall dormers;
  - 93505709 (the brick villa): the balcony in its west gable (pass 138's `gable_balcony`);
  - 93505730 and 93329952: white corner boards on rendered walls (`corners`, new);
  - 93487572 (Torsgatan, white boarded villa): the white wall dormer and two chimneys;
  - 93487556 (the yellow block at Margaretaplan): the shop with its red awnings and shop window (`shop`, new) and the first-floor balcony on its Torsgatan gable (`end_balcony`);
  - 93358537 (Margaretaplan): the white glazed bay on the upper floor at its west corner (`corner_bay`, new);
  - 93505704 (Lillegårdsgatan): the small balcony over the entrance;
  - 93291989 (Lilla Dammgatan): iron balconies on the street front (pass 139's `balconies`);
  - 93487574: a garage door.

## Selection

The selection is computed in `scripts/prepare_block140.py` from the OSM street lines in `references/osm-slott98.json` (ways with `highway` and `name`).

- **Unclaimed set.** Every outline in `source/block98.json['buildings']` whose id is not in any `source/blockN.json` with N < 140 (ids and demolished ids, passes 138 and 139 included) and is not the Stagnell chapel 500979084 (pass 107). That leaves 80 ids.
- **Street houses.** Of those, 18 lie within 25 m of a named street (any street, not a fixed list). Grouped by nearest street: Ringgatan 6 (93566356, 93566367, 93566385, 93505709, 93505730, 93505770), Torsgatan 5 (93487556, 93487572, 93487582, 93487584, 93487589), Baldersvägen 3 (93487569, 93487574, 93487591), Lillegårdsgatan 2 (93505686, 93505704), Margaretaplan 1 (93358537), Stensövägen 1 (93326725, two clipped pieces). This is the same set as pass 139's open issue 1 (its "Stensövägen 4" counted the clipped pieces twice); it includes the four outlines pass 138 left to other streets (93487556, 93487582, 93487569, 93358537) and the two pass 136 left on Ringgatan (93505770, 93566385).
- **Three a little beyond 25 m** (`STREET_EXTRA`). Pass 139's console had named five more outlines near Södra vägen, Lilla Dammgatan, Söderportsgatan and Unionsgatan. Recomputed, all lie 25 m or more from every named street: 93252863 (Saga, 26.4 m from Södra vägen), 93291989 (25.6 m from Lilla Dammgatan), 93329952 (42.4 m from Söderportsgatan), 93453481 (50.9 m from Unionsgatan) and 93453516/93453490 (30 m from Smålandsgatan, 37 m from Unionsgatan). They were checked in Street View:
  - 93252863 (Saga) stands free at the end of the garden behind the gate on Södra vägen and is seen from the street (sa1_h1, sa2_h22): taken.
  - 93291989 is a free-standing brick block on the lawn north of Lilla Dammgatan, seen between the trees (ld2_h353, 2011): taken.
  - 93329952 is the white villa on the hill above Söderportsgatan, seen from the street below (sp1_h312, sp2_h301): taken.
  - 93453481, 93453490 and 93453516 stand in the courtyard behind the street blocks on Unionsgatan and Smålandsgatan (un1_h161, sm1_h71 show only the street fronts and the gateway): yard buildings, left to the yard job.
- **Clipped outlines.** Pass 98's model box is x ≥ −1650, y ≤ 320. Four of the houses are cut by it:
  - 93326725 (Stensövägen) is cut at y 320 into two pieces, 245.6 m² (chunk M) and 17.2 m² (chunk W); its street front on Stensövägen lies outside the box. Pass 138 left it in the chunk. This pass builds it, consistently with pass 139's corner-clipped 93326740: the pieces are a visible part of a street block (sv2_h172), and leaving it would leave a street house undetailed. Both pieces are one mesh.
  - 93252863 (Saga) is cut at y 320 on its north side.
  - 93505686 (Lillegårdsgatan) and 93487574 (the garage on Baldersvägen) are cut at x −1650; only the east part of the villa lies inside.
  - Walls on the box edge are `cut` walls in `source/block140.json`: plain wall without windows, door, plinth or boards (4 cut walls). The clipped block 93326725 gets a flat roof: its real low saddle runs on out of the box, and the low hipped roof of the first sandbox run read as a pyramid on the clipped pieces (sv2_h172).
- **Yards.** The other 59 unclaimed outlines lie 25 m or more from every named street and go to `left_to_yards` (with their nearest street, distance, chunk, kind and area).

That gives 21 outlines, all built: 93252863, 93291989, 93326725, 93329952, 93358537, 93487556, 93487569, 93487572, 93487574, 93487582, 93487584, 93487589, 93487591, 93505686, 93505704, 93505709, 93505730, 93505770, 93566356, 93566367, 93566385.

**Chunks.** 18 outlines lie in pass 98's chunk W (x < −1150 by the outline centroid), and the small piece of 93326725; 93326725's large piece and 93291989 lie in M; 93252863 lies in E. The build adds the 21 ids to `SLOTT98_DETAILED` (which keeps the ids of every earlier pass in the chain) and calls pass 115's `slott98_chunks115({'W','M','E'}, 140, block140_names)`. The three chunks are re-created by pass 98's code without these houses, keep `detail_pass` 98 and get `rebuilt_by_pass` 140. They are among this pass's meshes (24 names in all).

**Passes 134, 136, 138 and 139** share these chunks (138 in W, 139 in M and E, 134/136 in W and M). In the official chain `SLOTT98_DETAILED` accumulates, so the re-created chunks leave their houses out; the sandbox check below confirms it with pass 139's chain in the prelude.

## Zones

Pass 116's slab method (as copied by passes 134–139):

- An outline that fills 85 % of its box in the frame of its longest edge is one zone; otherwise it is cut into slabs at its vertices and merged into a main body and wings, or flat-roofed annexes under 12 m² or narrower than 2.6 m (full height on blocks of three storeys or more).
- Each piece of a clipped outline is decomposed on its own.
- 93566385 is an L (the block along Ringgatan and a back wing at its north-east end). The slab method cut a flat strip off its street front; `MAINBAND` makes the band within 11.5 m of the front (vertex 2 to vertex 3) the main zone with its ridge along the street, and the rest a wing.
- 93487556's gable faces Torsgatan (ts6_h255); `RIDGE` turns its main zone so the ridge runs along the Margaretaplan front (vertex 0 to vertex 1).
- Saga (93252863) has ten small jogs of 1–2.5 m on its south front; `COARSE` finds its rectangles on the outline simplified by 1.5 m. The walls still follow the OSM outline.
- Each zone's walls follow the OSM outline exactly; walls against a neighbouring zone or house start at the neighbour's eaves.
- The door goes on the outer wall facing the house's door street (named per house where the photos show it, e.g. Margaretaplan for 93487556), else its nearest street.

## Measurement

Photos: 31 views captured for this pass with the claude-in-chrome extension in its own tab (closed afterwards), `captures.txt` lines `140|`, files in `SCR/p140/`, all 608 × 458, vertical field of view 90°, pitch +10° (sp2_h301 +15°). Imagery dates: April–June 2025, except the Torsgatan and Baldersvägen views ts1, ts2, ts7, bv1–bv3 (June 2022) and Lilla Dammgatan ld1, ld2 (June 2011). Google imagery was used as a view-only reference; nothing was downloaded.

| Files | Shows |
|---|---|
| rg1_h296, rg2_h22, rg3_h239 | the Ringgatan row 93566356, 93566367, 93566385 |
| rg4_h108, rg5_h103, rg6_h82 | 93505770, 93505730, 93505709 on the south-east side of Ringgatan |
| lg1_h341, lg2_h7, lg3_h67 | 93505686 (both sides) and 93505704 |
| ts1_h263, ts7_h345 | 93487572 |
| ts2_h310 | 93487589 behind the trees |
| ts3_h309, ts4_h294 | 93487584 and 93487582 |
| ts5_h344, ts6_h255 | 93487556 |
| mp1_h100 | 93358537 |
| bv1_h44, bv2_h184, bv3_h147 | 93487591; 93487569 (blurred by Google); 93487574 |
| sv1_h123, sv2_h172 | 93326725 (sv1 too close, not used) |
| sa1_h1, sa2_h22, sa3_h322 | Saga 93252863 |
| ld1_h10, ld2_h353 | 93291989 between the trees (2011) |
| sp1_h312, sp2_h301 | the villa on the hill 93329952 |
| un1_h161, sm1_h71 | the street fronts in front of the courtyard buildings 93453481/90/16 (identification only) |

- **Identities.** All pass-98 outlines within 70 m were projected into every view from the Google positions (`SCR/p140/ov140.py`, a copy of pass 138's overlay; overlays `ov_*.png`). Every built house was identified this way; 93487569 is behind Google's privacy blur and 93487589 behind trees.
- **Measurement.** Heights are read on the OSM wall plane with `hit` (`SCR/p140/m140.py`, vfov 90). Five cameras are resected with `SCR/p100/res.py` on two corners of the house; the others stand at the Google position. The camera is assumed 2.5 m above model zero; the base reading shows how far that is off.

| View | Google position (x, y) | Camera used (x, y) | Corners | Used for |
|---|---|---|---|---|
| rg5_h103 | (−1626.43, 256.54) | (−1628.37, 256.59) | 93505730 v0, v1 (gable) | eaves, gable apex |
| bv1_h44 | (−1639.73, 43.90) | (−1634.19, 41.98) | 93487591 v0, v3 (gable) | eaves, apex |
| ts3_h309 | (−1563.88, 94.18) | (−1564.83, 97.28) | 93487584 v1, v0 (gable) | eaves, apex |
| ts6_h255 | (−1507.66, 121.97) | (−1504.81, 121.66) | 93487556 v5, v0 (gable) | eaves, apex |
| mp1_h100 | (−1504.26, 152.35) | (−1504.46, 151.09) | 93358537 v2, v3 (v3 under the bay, less certain) | eaves |
| rg3_h239 | (−1570.42, 281.70) | Google | none | the Ringgatan row's eaves |
| all other views | Google | Google | none | identification, storeys, colours |

Resection residuals are under 4.3 px. With the Google camera, 93487556's eaves read 7.9 instead of 9.0, so unresected readings carry roughly ±1 m.

### Houses

Heights are metres above the ground (model z 0.30). "Estimated" means read from storeys, doors, windows and the roof pitch by eye.

| OSM id | Identity | Photo | Storeys | Eaves / ridge | Roof | Measured or estimated |
|---|---|---|---|---|---|---|
| 93566356 | white rendered block over a basement, attic and balcony on the south-west gable (Ringgatan 3) | rg1_h296, rg2_h22 | 2 | 6.8 / 9.4 | red tile saddle | as 93566385 (the eaves line runs on) |
| 93566367 | pale yellow rendered block over a basement | rg1_h296, rg2_h22 | 2 | 6.8 / 9.4 | red tile saddle | as 93566385 |
| 93566385 | ochre rendered block over a basement, two red wall dormers (Ringgatan 4) | rg3_h239 | 2 | 6.8 / 9.4 | red tile saddle | base z 0.46, eaves 7.1 at the east corner of the south-east front (Google camera); 6.6 above the base, 6.8 used; ridge estimated |
| 93505709 | red brick villa, balcony in the west gable | rg6_h82 | 1.5 | 4.0 / 8.2 | red tile saddle | estimated |
| 93505730 | tall pale yellow rendered house, white corner boards, gable on Ringgatan | rg5_h103 (resected) | 2 + attic | 7.8 / 11.0 | dark saddle | base reads 0.59 behind the hedge, eaves 8.74 at the west corner, gable apex 11.48 |
| 93505770 | pale yellow rendered villa, red chimney, behind shrubs | rg4_h108 | 2 | 5.8 / 9.0 | red tile hip | estimated |
| 93505686 | white rendered villa, low hipped roof, glazed veranda (east part inside the box) | lg1_h341, lg3_h67 | 2 | 6.0 / 7.8 | red tile hip | estimated |
| 93505704 | yellow rendered apartment villa over a basement with balconies | lg2_h7 | 2 | 6.6 / 9.6 | red tile hip | estimated |
| 93487572 | white boarded villa, wall dormer, two chimneys, glazed veranda (Torsgatan 8) | ts1_h263, ts7_h345 | 1.5 | 4.0 / 8.0 | red tile saddle | estimated |
| 93487589 | light rendered villa behind the trees | ts2_h310 | 1.5 | 4.0 / 7.8 | dark tile saddle | estimated |
| 93487584 | yellow-brown brick house with the steep gable on Torsgatan (Torsgatan 4) | ts3_h309 (resected) | 2 | 5.0 / 11.0 | red tile saddle | base 0.52, eaves 4.6 at the east corner, apex 11.47; the west eave reads 8.3 where the roof runs on over the bay |
| 93487582 | tall white rendered house with the dark mansard roof | ts4_h294 | 2 | 5.8 / 9.8 | dark gambrel | estimated |
| 93487556 | yellow rendered block with an attic, shop on the ground floor, balcony on the Torsgatan gable | ts6_h255 (resected), ts5_h344 | 2 + attic | 8.4 / 12.6 | red tile saddle | base 0.23, eaves 8.96–8.98 at both gable corners, apex 13.07 |
| 93358537 | yellow rendered block, dormers, red chimney, white glazed corner bay | mp1_h100 (resected) | 2 | 7.8 / 11.0 | red tile hip | base 0.07, eaves 7.83 at the west corner; ridge estimated |
| 93487591 | pale grey boarded villa with the steep gable on Baldersvägen (Baldersvägen 8) | bv1_h44 (resected) | 1.5 | 4.6 / 9.4 | red tile saddle | eaves 5.2 and 4.3 at the two corners, apex 9.7 (base behind bushes) |
| 93487569 | house behind Google's privacy blur | bv2_h184 (blurred) | 1.5 | 4.0 / 7.8 | red tile saddle | estimated, form unknown |
| 93487574 | white boarded garage (west end clipped) | bv3_h147 | 1 | 2.5 / 3.8 | dark tile saddle | estimated |
| 93326725 | yellow brick apartment block over a basement with balconies (rear part inside the box) | sv2_h172 | 3 | 10.4 / 10.65 | flat (real: low saddle) | estimated |
| 93252863 | Saga: beige rendered house with a red tile roof and a low west part (north side clipped) | sa1_h1, sa2_h22 | 2 | 5.6 / 8.8 | red tile saddle | estimated |
| 93291989 | yellow brick block with balconies behind the trees | ld2_h353 (2011) | 3 | 9.6 / 11.6 | red tile saddle | estimated |
| 93329952 | white rendered villa with corner pavilions on the hill | sp2_h301, sp1_h312 | 2 + attic | 7.4 / 10.0 | dark hip | estimated (the hill is not modelled; pass 98's ground is flat) |

Colours are read by eye from the photos and set as flat targets on the town textures (`M_Block140_<Key>`).

## Estimated

- Every value marked estimated above, and all ridge heights except the four measured gable apexes (93505730, 93487584, 93487556, 93487591).
- 93487569's form and colour (behind the privacy blur), 93487589's walls (behind trees) and 93291989 (2011 imagery, behind trees).
- The roofs and heights of the clipped houses; 93326725's real roof is a low saddle running out of the box.
- Window counts: regular bays (2.7 m on two-storey houses, 2.9 m on others), not the real positions.
- Doors: one per main zone on the street wall; the position along the wall is a rule.
- Dormer counts, chimney places, the balcony sizes and heights, the shop window and awnings, the corner bay's size.

## Verification

- **Zones** (`previews/block140-zones.json`, `BLOCK140_ZONES_OK`): 34 zones cover the 21 outlines, 4597.8 m² of 4597.8.
  - 0.01 m² lies outside OSM and 0.03 m² of OSM is not zoned (slivers at the cuts).
  - The overlap is 0.0 m²; the outlines themselves do not overlap.
  - 4 walls on the model box are marked `cut`.
  - Status: passed.
- **Sandbox**, through the wrapper `SCR/p140/build_block140_check.py` (a copy of pass 139's). The wrapper hashes every mesh in the scene before the build, runs the build twice in one session as the official build does, and hashes again. It then checks that no detailed outline is drawn by the re-created chunks W, M and E, listing passes 134, 136, 138 and 139 separately, and runs the export frame check with the export tail's preparation and `export_district_fbx` to a temporary file (deleted after each mesh). Pass 139's official rebuild script existed by the time of both runs, so the prelude was `rebuild_block139` and pass 139's houses and ids were in the scene (the wrapper would otherwise run pass 139's build first).
  - **Run 1** printed `BLOCK140_GEOMETRY 24` twice; all the checks below passed in it too. The comparisons showed two things to fix:
    - 93487572 (Torsgatan 8) had its gable on the street; the photos show the long side with the wall dormer. It now has `ridge='street'`.
    - The low hipped roof on the clipped pieces of 93326725 read as a pyramid in sv2_h172; it is now flat (see Selection).
  - **Run 2**, after the fixes:
    - `BLOCK140_GEOMETRY 24` twice: 21 houses and the chunks W, M and E.
    - Repeatability: `REPEAT140 True`. The two runs give identical geometry hashes (vertices, loops, material indices, UVs and material names) on all 24 meshes; there are 21 `SM_Slott140_` objects.
    - Hashes before and after: only `SM_Slott98_Buildings_E`, `SM_Slott98_Buildings_M` and `SM_Slott98_Buildings_W` changed (intended). There are 21 new meshes, all `SM_Slott140_*`, and none is gone. No other mesh in the scene changed; the houses of passes 134–139 are untouched.
    - Shared names: `G` and `TS` are the same after the build as before it. The build sets `G` to the ground height only while it runs, for pass 115's `steps115`, and restores `TS`/`TC` at the start.
    - Chunk exclusion (no chunk vertex more than 0.8 m inside an outline): none of this pass's outlines (18 in W, 2 in M, 1 in E) and none of the other detailed outlines in W (165) and E (52) has a chunk vertex inside. Per pass: 134 (37 ids in W, 6 in M), 136 (53 in W), 138 (61 in W) and 139 (8 in M, 11 in E) are all clear, with one known exception: pass 139's 93325650 has 51 vertices inside, all from the pass-98 roof of the unclaimed courtyard building 93325656 (a yard building, see pass 139's notes), not a failure to exclude 93325650. The chunks still draw 39 volumes in W, 11 in M and 9 in E: the 59 yard buildings. (The check tests the first piece of 93326725 only, the one in M.)
    - Export frame check: `CHECK140_TOTAL_INVALID 0 EXPORTS_OK 24 OF 24`.
    - Degenerate faces dropped by `drop_degenerate_faces140`: 422 per build over the 21 house meshes (0–101 per mesh, most on Saga 93252863 and 93487582).
    - `SANDBOX_DONE prelude 139`.
- **Comparison** with the photos. Each view is rendered at the photo size (608 × 458) from the cameras above and put side by side with the photo in `SCR/p140/sb1/cmp_*.png` and `SCR/p140/sb2/cmp_*.png`. Unresected cameras stand at the Google position, so houses sit 1–3 m off their photo positions.
  - The Ringgatan row (rg2_h22, rg3_h239): the three blocks over basements, their colours, the continuous eaves, the red roofs, the ochre block's red dormers and the white block's gable balcony match. The real row has three window rows on the white block's gable (attic); the model has two rows and a gable window.
  - 93505730 (rg5_h103, resected): the tall pale yellow gable, the dark low-pitched roof and the white corner boards match closely.
  - 93505709 (rg6_h82): the brick villa with its gable to the west and the red tile roof match in form; the model's brick reads lighter and pinker than the photo.
  - 93505770 (rg4_h108), 93505704 (lg2_h7): the yellow hipped villas match in form and colour.
  - 93487572 (ts1_h263, ts7_h345, run 2): the white boarded villa with its long side, wall dormer and two chimneys on the street and its gable to the south match; the glazed veranda is not modelled.
  - 93487584 (ts3_h309, resected) and 93487582 (ts4_h294): the brick house's steep street gable and the tall white house with the dark mansard roof match in kind. The brick house's bay and asymmetric roof are not modelled.
  - 93487556 (ts6_h255, resected): the yellow block, its gable with the balcony, the shop with the red awnings and the roof match.
  - 93358537 (mp1_h100, resected): the yellow block and its hipped roof match; the glazed corner bay is a white box with a glazed panel, simpler than the real two-storey bay.
  - 93487591 (bv1_h44, resected): the grey boarded villa and its steep gable match; the side dormer and the gable's decorated windows are not modelled.
  - 93329952 (sp2_h301): the white villa reads in the right place, lower than in the photo because the hill is not modelled; the corner pavilions are not modelled.
  - 93326725 (sv2_h172): only the clipped rear part is in the model; the block's street front lies outside the box.
  - Not compared in detail: 93487569 (blurred), 93487589 (trees), 93291989 (2011, trees), Saga (seen through the gate).

- **Official build:** done by the lead on 2026-10-04; see "Official build". The Unreal checks are pending.

## Limitations

- Five cameras are resected; the other heights are read from Google positions or estimated from storeys. Ridge heights and roof pitches are mostly estimated.
- The houses are boxes on the OSM outline with rectangular roofs; small notches are covered by the roof or by flat annexes.
- Window and door positions are regular bays, not the real ones. The veranda of 93487572, the glazed veranda of 93505686, the corner pavilions of 93329952, the round-arched and bay details are not modelled or only drawn as boxes.
- Four houses are clipped by pass 98's model box; their parts outside the box are not modelled, and the walls on the box edge are plain.
- 93329952 stands on a hill in reality; the model ground is flat.
- No fences, hedges, garden walls or sheds outside the OSM outlines are modelled.
- Extra views that would help, as location (x, y), Street View heading and pitch:
  - 93487569 without the blur is not possible; an aerial or a view from the south-east, (−1625, −5), heading 330, pitch 10;
  - 93291989 with recent imagery from Lilla Dammgatan, (−1070, 170), heading 353, pitch 10;
  - 93487589 from the path north of it, (−1595, 112), heading 160, pitch 10.

## What remains undetailed on the mainland

After this pass every mainland street house is detailed. The 59 unclaimed pass-98 outlines that remain lie 25 m or more from every named street; they are yard and back buildings (sheds, garages, courtyard wings, park buildings) and are listed in `source/block140.json['left_to_yards']`. By chunk:

- **W (39):** 1453534570, 874145313 (kiosk), 874145314 (toilets), 93238186, 93238220, 93238221, 93238239, 93238283, 93238284, 93238290, 93291962, 93291967, 93292008, 93329937, 93329938, 93329953, 93329957, 93329965, 93329980, 93329987, 93330000, 93330001, 93358502, 93358543, 93358547, 93361181, 93460156, 93460172, 93460175, 93460187, 93460194, 93460203, 93460204, 93460209, 93460214, 93487550, 93487564, 93505688, 93505695;
- **M (11):** 91970346, 93292689, 93292702, 93292706, 93293012, 93293025, 93293041, 93306352, 93325645, 93325656, 93326718;
- **E (9):** 93306356, 93333623, 93333627, 93333638, 93333658, 93333660, 93453481, 93453490, 93453516.

Borderline (25–27 m from a street, judged yard buildings by distance only, not checked in photos): 93306352 (25.1 m, Västerlånggatan), 93333658 (25.2 m, Järnvägsgatan), 93330001 (25.4 m, Ståthållaregatan), 93238239 (26.2 m, Stora Dammgatan), 93333638 (26.5 m, Västerlånggatan). 93325656 is the courtyard building whose pass-98 roof overhangs pass 139's 93325650 (see pass 139's notes).

## Official build

The lead built pass 140 officially on 2026-10-04.
- **Geometry and export:** the geometry check passed on the second rebuild (True), the FBX audit passed (exit 0), and the two rebuilds gave identical meshes.
- **Prevhash:** only intended changes. Pass 98's chunks W, M and E are re-created without this pass's 21 houses; they show up under passes 134, 136, 138 and 139. The rest are known earlier corrections.
- **Dry renders:** cameras 775–784, 10 of 10.
