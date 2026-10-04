# Pass 136: the mainland around Drottning Margaretas väg, Sankt Eriks gata, Johan III:s gata and Sankta Britas gata

Pass 98 built the mainland houses as plain volumes inside three chunk meshes. Pass 136 takes the 53 pass-98 outlines along Drottning Margaretas väg, Sankt Eriks gata, Johan III:s gata and Sankta Britas gata out of those chunks. Each becomes its own mesh `SM_Slott136_<osm id>` (category `Slottsområdet/Mainland`, `detail_pass` 136), standing on pass 98's ground height (model z 0.30).

The pass was started earlier as a parked street pass under the number 124 (plan `SCR/plan124.json`, captures `124s|` in `SCR/captures.txt`) and is renumbered here; the number 124 went to the castle. No parked script files existed for it (there is no `pending_streets124` in `.pipeline/`). The scripts follow pass 134, which finished the sibling group, closely: `scripts/prepare_block136.py` is pass 134's prepare script with this pass's selection and house table, and `scripts/build_block136.py` is pass 134's build with every prefix, name, material, marker and `detail_pass` set to 136, pass 134's one-off features (the arched entrance bays, the round gable, the glazed tower and so on) removed, and the features below added. Pass 134's fixes are kept: `TS`/`TC` are restored before the town helpers run, the house and material loops run in functions so no short global names leak, `G` is set for `steps115` only while the build runs and given back afterwards, and flat roofs drop collinear and spike vertices (`simp136`).

Each house gets:

- storeys (1, 1.5 or 2, most of the larger houses over a basement with basement windows), the eaves and ridge heights, a stone plinth;
- the roof: saddle, hip, Swedish mansard (gambrel, with gable ends) or a hipped mansard, in red or red-brown tile, dark tile or sheet metal; on the two rows on Drottning Margaretas väg and on the town houses of Sankt Eriks gata the ridge runs along the street (`ridge: 'street'`), on the brick house 93329949 at right angles to it (`ridge: 'across'`, the gable on the street);
- render in the house's colour, vertical boarding with white corner boards, or light brick;
- eaves boards, white bargeboards on the gables, gable windows on the steeper gables;
- windows per storey (casement, surround, sill), a door on the wall facing the street, steps where the door stands on the plinth;
- dormers, chimneys and the features in the table: the gables on the street front with their own width and apex (`gable_mid` with `gable_w`, `gable_top`; pass 83's `frontis83`), the curved gable's round window (`oculus`, a triangle fan), the round window over the door of the pink 1910s house (`oculus_door`) with the door in its centre bay (`door_mid`), the white oriels (`oriel`; on 93358536 placed 3 m in from the end at its pink neighbour, `oriel_near`), the brown boarded roof storey of 93329984 (`attic`), the broad wall dormers (dark brown on the white houses, dark red on the cream ones), gabled dormers, the balcony over the red block's door, the porch roof, the arched gateway, the porches with balconies on top, garage doors.

## Selection

The selection is computed in `scripts/prepare_block136.py` with pass 134's method: every outline in `source/block98.json['buildings']` within 25 m of one of the four streets (the OSM street lines in `references/osm-slott98.json`) whose nearest named street is one of them, leaving out the Stagnell chapel 500979084 (pass 107) and the ids of passes 115–119 and 134 (read from their `source/block1xx.json`). It gives exactly the 53 ids of the parked plan. No other pass touches them: a search of every `source/block*.json` finds only 93329942, in pass 134's `left_to_other_streets` (left there to Sankta Britas gata, i.e. to this pass).

Five outlines within 25 m are nearer another street and are left to the passes of those streets (`source/block136.json['left_to_other_streets']`): 93329960 and 93505743 (Stensövägen), 93358537 (Margaretaplan), 93505770 and 93566385 (Ringgatan).

**Demolished or empty sites.** Unlike pass 134's 93358501, none of the 53 outlines is a cleared site in the photos that show it; `demolished` is empty and every id gets a mesh. Eight outlines are seen in no photo (93361177, 93361185, 93361214, 93358513, 93358511, 93358540, 93358517, 93329942); they are built from their neighbours and OSM's level count, and whether they still stand as drawn is not verified.

The 53 ids: 93329935, 93329936, 93329941, 93329942, 93329949, 93329954, 93329955, 93329959, 93329963, 93329968, 93329973, 93329984, 93329985, 93329986, 93329994, 93329996, 93329997, 93358507, 93358510, 93358511, 93358513, 93358514, 93358515, 93358516, 93358517, 93358519, 93358521, 93358522, 93358523, 93358524, 93358528, 93358531, 93358534, 93358535, 93358536, 93358540, 93358549, 93361162, 93361172, 93361177, 93361185, 93361214, 93361235, 93361242, 93361247, 93460178, 93460193, 93460219, 93460227, 93460240, 93505718, 93566374, 149905963.

**Chunks.** All 53 outlines lie in pass 98's chunk W (x < −1150). The build adds them to `SLOTT98_DETAILED`, which already holds the ids of every earlier pass in the chain (pass 134's 43 built ids and its demolished 93358501 included), and calls pass 115's `slott98_chunks115({'W'}, 136, block136_names)`. The chunk is re-created by pass 98's code without these houses, keeps `detail_pass` 98 and gets `rebuilt_by_pass` 136. It is among this pass's meshes (54 names in all). M and E are not touched.

## Zones

Pass 116's slab method, as copied by pass 134:

- An outline that fills 85 % of its box in the frame of its longest edge is one zone; otherwise it is cut into slabs at its vertices and merged into a main body and wings, or flat-roofed annexes under 12 m² or narrower than 2.6 m.
- There is no explicit split in this pass.
- Each zone's walls follow the OSM outline exactly; walls against a neighbouring zone or house start at the neighbour's eaves.
- The door goes on the outer wall that faces one of the four streets; corner houses facing none use the nearest of Stensövägen, Margaretaplan, Ringgatan, Torsgatan, Långviksvägen, Ståthållaregatan or Gustaf Vasagatan. 93329986 faces no street within 40 m and has no door.

## Measurement

Photos: the 16 views captured for the parked pass (`captures.txt` lines `124s|`, files `SCR/p124/`, copied to `SCR/p136/`), all 728 × 419, vertical field of view 90°, pitch +10°. Google imagery was used as a view-only reference. **No new views were captured:** the Claude in Chrome extension was not connected in this session (`tabs_context_mcp` reported "Browser extension is not connected"), so there are no `136|` lines.

- **Identities.** All OSM outlines within 70–90 m were projected into every view from the Google positions (`SCR/p136/ov136.py`, `vis136.py`, and `ov2.py`, which draws only the walls facing the camera with the ids; overlays `ov_*.png`, `ov2_*.png`), and every house was matched to the photo by its place in the row, its corners and the section joints.
- **Resection.** With `SCR/p100/res.py` (vfov 90) from the bearings of outline corners or section joints that are clear in the photo (`SCR/p136/rs.py`); heights read on the wall plane with `hit`. Where the base of the wall is visible, heights are given above the base (which takes out the camera height); otherwise above model z 0.30 with the camera at 2.5.

| View | Google position (x, y) | Camera used (x, y), height | Corners | Used for |
|---|---|---|---|---|
| dm01_h24 | (−1428.2, 35.2) | (−1427.6, 33.5), 2.5 | four joints of the southern row on Drottning Margaretas väg: 93358522's south corner, 93358522/93358514, 93358514/93358534, 93358521/93358510 (residuals 5–11 px) | eaves 7.5 (93358522, 93358514) and 6.9 (93358534), the gables' apex 9.4 on the front plane; the base is behind the fence |
| dm02_h24 | (−1469.7, 87.9) | (−1471.0, 86.0), 2.3 | four joints of the same row, 93358531's north corner to 93358516/93358549 (residuals 2–8 px) | base at model z 0.49 with the camera at 2.5, hence 2.3 used; eaves 8.1 (93358531, 93358528), 8.45 (93358516), gable apexes 12.3, all above the base |
| dm05_h51 | (−1567.8, 303.5) | (−1568.3, 302.7), 2.5 | 93361172's two front corners | base at z 0.37; eaves 7.1 (93361172) and 7.2 (93361235) above it |
| se02_h231 | (−1358.6, 64.0) | (−1358.5, 61.3), 2.8 | 93358523's two front corners | base at −0.02 with the camera at 2.5, hence 2.8 used; eaves 7.15 and pediment apex 9.6 above the base |
| j302_h340 | (−1405.7, 163.9) | (−1406.7, 161.0), 2.5 | 93329997's two front corners | eaves 8.4 and the central gable at 11.6 on the front plane; the base is behind the hedge (±0.4) |
| dm03_h39, se02_h231 (93358536, 93358507), sb01_h235, j301_h161 | Google | Google, 2.5 | none | 93361162 eaves 7.2 above the base; 93358536 7.3, 93358507 7.5, 93329941 5.5 above the base; 93329984 read at 9.7, not used (see the table) |
| all other views | Google | Google, 2.5 | none | identification, storeys, colours |

The other views are grazing or too far for a height (se01_h51 and se02_h51 put the camera inside or beside the near house; the readings were discarded).

### Houses

Heights are metres above the ground (model z 0.30). "Estimated" means read from storeys, doors, windows and the roof pitch by eye, or taken from the neighbours.

| OSM id | Identity | Photo | Storeys | Eaves / ridge | Roof | Walls | Measured or estimated |
|---|---|---|---|---|---|---|---|
| 93329935 | pink rendered two-and-a-half-storey house with a red tile roof and gabled dormers | se02_h51 (left) | 2 | 6.5 / 10.2 | red tile saddle | pink render | eaves about 6.5 (a grazing view from the pano position; estimated) |
| 93329936 | cream rendered two-storey 1990s terrace with red tile roofs and gabled dormers | j301_h341 (right) | 2 | 5.6 / 8.8 | red tile saddle | cream render | estimated |
| 93329941 | yellow rendered one-and-a-half-storey house in 18th-century style with a brown tile mansard roof, the curved gable and dormers, behind the green door gateway | sb01_h235 (close) | 1.5 | 5.5 / 10.0 | red-brown tile gambrel | yellow render | base at -0.25, eaves 5.5 above it, gable apex about 10.6 (camera 2.5 assumed, pano position) |
| 93329942 | yellow rendered two-storey house with a red tile roof (not seen) | not seen | 2 | 5.8 / 9.2 | red tile saddle | yellow render | estimated |
| 93329949 | light brick one-and-a-half-storey house with a black tile mansard roof (gable on the street) and solar panels | se01_h51 (close) | 1.5 | 3.4 / 8.0 | dark gambrel | light brick | estimated |
| 93329954 | low white house with a red tile roof at the garden wall | j301_h341 | 1 | 2.8 / 5.0 | red tile saddle | white render | estimated |
| 93329955 | long low white house with a red tile roof behind the white garden wall | j301_h341 | 1 | 3.0 / 5.4 | red tile saddle | white render | estimated |
| 93329959 | low ochre house with a red sheet roof behind the picket fence | sb01_h235 (behind the fence) | 1 | 2.8 / 4.6 | red sheet saddle | ochre render | estimated |
| 93329963 | cream rendered two-storey 1990s terrace house with a red tile roof (the east end of the terrace) | j301_h341 (far right) | 2 | 5.6 / 8.8 | red tile saddle | cream render | estimated |
| 93329968 | small shed between the villas | se02_h51 (behind the hedge) | 1 | 2.4 / 3.6 | red tile saddle | grey boards | estimated |
| 93329973 | sage-green boarded one-and-a-half-storey villa with a red tile roof, the glazed gable bay and the round window | se02_h51 (right) | 1.5 | 4.2 / 8.8 | red tile saddle | sage-green boards | estimated |
| 93329984 | white boarded two-storey block over a basement with the brown boarded roof storey and a low dark roof | j301_h161 (close, scaffolding) | 2 over a basement | 8.2 / 9.4 | dark saddle | white boards | read at 9.7 from the pano position (not resected, 8 m away); 8.2 used from the storeys |
| 93329985 | small outbuilding behind the brick house | se01_h51 (behind) | 1 | 2.5 / 3.8 | dark saddle | white render | estimated |
| 93329986 | low white rendered house with a red tile roof | j302_h340 (right) | 1 | 3.0 / 5.4 | red tile saddle | white render | estimated |
| 93329994 | red boarded one-and-a-half-storey house with white corner boards and a red tile roof | sb01_h235 (left edge) | 1.5 | 4.4 / 8.0 | red tile saddle | falu red boards | estimated |
| 93329996 | red boarded shed | sb01_h235 (left, far) | 1 | 2.4 / 3.6 | red tile saddle | falu red boards | estimated |
| 93329997 | white rendered two-storey house over a basement with a red tile hipped roof and the central gable | j302_h340 (resected) | 2 over a basement | 8.4 / 11.6 | red tile hip | white render | eaves 8.4 and central gable apex 11.6 (on the front plane; 11.2 used, the gable is lower than the ridge in the comparison) above the estimated ground (camera resected on the two front corners to (-1406.7, 161.0); the base is behind the hedge) |
| 93358507 | orange rendered two-storey town house | se02_h231 (right edge) | 2 | 7.6 / 10.8 | red tile saddle | orange render | eaves 7.5 above the base (camera 2.5 assumed, pano position) |
| 93358510 | white rendered section of the southern row with the broad dark brown wall dormer and round roof lights | dm01_h24 (left edge) | 2 over a basement | 6.9 / 10.6 | red tile saddle | white render | estimated |
| 93358511 | small garage (not seen) | not seen | 1 | 2.5 / 3.6 | red tile saddle | grey boards | estimated |
| 93358513 | cream rendered two-storey town house (not seen) | not seen | 2 | 7.0 / 10.2 | red tile saddle | cream render | estimated |
| 93358514 | white rendered section of the southern row with the curved central gable and its round window | dm01_h24 (resected) | 2 over a basement | 7.5 / 11.1 | red tile saddle | white render | eaves 7.5 and gable apex 9.4 on the front plane (same camera) |
| 93358515 | red-brown boarded two-storey house with a red tile roof at the south end | dm01_h24 (far right) | 2 | 5.6 / 9.0 | red tile saddle | falu red boards | estimated |
| 93358516 | yellow-green rendered section of the southern row with the broad gable on the avenue | dm02_h24 (resected) | 2 over a basement | 8.45 / 12.6 | red tile saddle | yellow-green render | base at z 0.49 with the camera at 2.5 (so the camera is about 2.0 above the ground), eaves 8.45 and gable apex 12.3 above the ground |
| 93358517 | white rendered one-and-a-half-storey house with a red tile roof (not seen) | not seen | 1.5 | 4.2 / 7.8 | red tile saddle | white render | estimated |
| 93358519 | white rendered two-storey house with a red tile hipped roof | dm03_h39 (far) | 2 | 6.2 / 9.4 | red tile hip | white render | estimated |
| 93358521 | white rendered section of the southern row with dormers | dm01_h24 | 2 over a basement | 6.9 / 10.6 | red tile saddle | white render | estimated |
| 93358522 | cream-white rendered south end of the southern row, with the gable on the avenue | dm01_h24 (resected) | 2 over a basement | 7.5 / 11.1 | red tile saddle | pale cream render | eaves 7.5 and gable apex 9.4 on the front plane (camera resected on four section joints to (-1427.6, 33.5), 2.5 m assumed; the base is behind the fence) |
| 93358523 | pink rendered two-storey 1910s house with the pedimented centre bay, white pilasters and the round window over the door | se02_h231 (resected) | 2 | 7.2 / 10.3 | red tile saddle | pink render | eaves 7.15 and pediment apex 9.6 above the base (camera resected on the two front corners to (-1358.5, 61.3)) |
| 93358524 | cream rendered two-and-a-half-storey house with a red tile roof and dark red dormers | se01_h231 (right) | 2 | 6.8 / 10.6 | red tile saddle | light yellow render | estimated |
| 93358528 | grey rendered section of the southern row with the central gable over the white bay window and dormers | dm02_h24 (resected) | 2 over a basement | 8.1 / 12.0 | red tile saddle | grey render | eaves 8.1 and gable apex 12.3 above the ground (same camera, base visible) |
| 93358531 | grey rendered north end of the southern row with dormers and the arched gateway | dm02_h24 (resected) | 2 over a basement | 8.1 / 12.0 | red tile saddle | grey render | eaves 8.1 above the ground (same camera) |
| 93358534 | white rendered section of the southern row with dormers | dm01_h24 (behind the tree) | 2 over a basement | 6.9 / 10.6 | red tile saddle | white render | eaves 6.9 on the front plane (same camera) |
| 93358535 | white rendered two-storey 1940s block over a basement with balconies on the gable | se01_h231 (close) | 2 over a basement | 6.6 / 9.6 | grey sheet saddle | white render | estimated |
| 93358536 | dark boarded two-storey house with the white oriel on the upper floor | se02_h231 (left) | 2 | 7.3 / 10.4 | dark saddle | dark grey boards | eaves 7.3 above the base (camera 2.5 assumed, pano position) |
| 93358540 | small garage (not seen) | not seen | 1 | 2.5 / 3.6 | red tile saddle | grey boards | estimated |
| 93358549 | yellow rendered one-and-a-half-storey section of the southern row, lower, with a red tile roof, dormers and the porch roof | dm02_h24 (behind the tree) | 1.5 | 5.0 / 9.0 | red tile saddle | yellow render | eaves seen at 4.4 on the front plane (the wall stands back, so higher; 5.0 used) |
| 93361162 | white rendered two-storey block over a basement at the south end of the northern row, with the broad dark wall dormers and the side balconies | dm03_h39 | 2 over a basement | 7.2 / 10.6 | red tile saddle | white render | eaves 7.2 above the base (camera 2.5 assumed, pano position) |
| 93361172 | red rendered two-storey block over a basement with the balcony over the door and a small dormer, at the north end of the northern row | dm05_h51 (resected) | 2 over a basement | 7.1 / 10.4 | red tile saddle | red render | base at z 0.37, eaves 7.1 above it (camera resected on the two front corners to (-1568.3, 302.7)) |
| 93361177 | cream rendered two-storey block over a basement (not seen; as its neighbours) | not seen | 2 over a basement | 7.2 / 10.6 | red tile saddle | pale cream render | estimated |
| 93361185 | cream rendered two-storey block over a basement (not seen; as its neighbours) | not seen | 2 over a basement | 7.2 / 10.6 | red tile saddle | cream render | estimated |
| 93361214 | white rendered two-storey block over a basement (not seen; as its neighbours) | not seen | 2 over a basement | 7.2 / 10.6 | red tile saddle | white render | estimated |
| 93361235 | cream rendered two-storey block over a basement with the dark red wall dormers | dm05_h51 | 2 over a basement | 7.2 / 10.6 | red tile saddle | cream render | eaves 7.2 above the base (camera resected on 93361172's two front corners) |
| 93361242 | light yellow rendered two-storey block over a basement with red dormers | dm05_h51 | 2 over a basement | 7.2 / 10.6 | red tile saddle | light yellow render | estimated |
| 93361247 | white rendered two-storey block with the dark metal-clad roof storey (a modern roof extension) | dm05_h51 (right edge) | 2 over a basement | 7.2 / 10.4 | dark hipped mansard | white render | estimated |
| 93460178 | cream rendered two-storey villa with a red tile roof and two chimneys | dm02_h204 (right) | 2 | 5.4 / 8.8 | red tile saddle | cream render | estimated |
| 93460193 | white garage with a dark roof behind the villa | dm02_h204 (centre, far) | 1 | 2.6 / 4.0 | dark saddle | white render | estimated |
| 93460219 | yellow boarded one-and-a-half-storey villa with a red tile hipped mansard roof and two dormers | dm01_h204 | 1.5 | 3.8 / 8.6 | red tile hipped mansard | yellow boards | estimated |
| 93460227 | yellow boarded villa with a brown tile roof, the cross gable over the glazed veranda with the balcony | dm02_h204 | 1.5 | 4.6 / 9.0 | red-brown tile saddle | yellow boards | estimated |
| 93460240 | red boarded two-storey house with a red tile roof and white trim | dm01_h204 (right edge) | 2 | 5.6 / 9.0 | red tile saddle | falu red boards | estimated |
| 93505718 | white rendered one-and-a-half-storey villa with a red tile roof, the cross gable with the balcony and the glazed veranda | dm04_h219 | 1.5 | 4.0 / 8.4 | red tile saddle | white render | estimated |
| 93566374 | beige-yellow rendered two-storey block over a basement with a red-brown tile roof | dm05_h231 (right) | 2 over a basement | 6.6 / 9.2 | red-brown tile saddle | light yellow render | estimated |
| 149905963 | white rendered one-and-a-half-storey house with a red tile roof (seen only far) | j302_h340 (far right) | 1.5 | 4.0 / 7.4 | red tile saddle | white render | estimated |

Colours are read by eye from the photos and set as flat targets on the town textures (`M_Block136_<Key>`); there is no blue or pink town texture, so pink, sage and yellow are tints on TownIvory, TownPaintGreen and TownPaintWhite.

## Estimated

- Every value marked estimated above, and all ridge heights (the roofs are seen only from the street; ridges are set from the eaves, the depth and a usual pitch).
- The eight houses seen in no photo (see Selection): their whole form.
- Window counts: regular bays (2.7 m on two-storey houses, 2.9 m on one-storey houses), not the real positions.
- Doors: one per house on the street wall, by a rule (near one end on fronts longer than 6 m; in the centre on 93358523; near the west end on 93358531's arched gateway).
- Dormer counts (one per 6.5 m of street slope, two on the houses marked so), chimney places, the oriel and balcony sizes, the gable widths, the roof storey of 93329984 (7 × 6 m at most, 1.6 m over the ridge).
- The roof forms where only one slope or one end is seen: 93460219's hipped mansard, 93329949's mansard with the gable on the street, the hips of 93358519 and 93329997.
- The pass-98 camera heights: the heights read from a non-resected pano position (dm03_h39, sb01_h235 and the se02_h231 neighbours) carry about ±0.5 m.

## Verification

- **Zones** (`previews/block136-zones.json`, `BLOCK136_ZONES_OK`): 75 zones cover the 53 outlines, 8022.0 m² of 8022.1; 0.04 m² lies outside OSM and 0.07 m² of OSM is not zoned (slivers at the cuts); the overlap is 0.017 m² (the OSM outlines themselves overlap by 0.016 m²). Status: passed.
- **Dry run.** Before each sandbox run the build was executed in plain Python with stub helpers (`SCR/p136/mock136.py`), which checks names, face indices and material keys. It caught one inherited bug: pass 134's garages carry both `garage_door` and `no_door`, so no garage door is drawn; here the garages have `garage_door` only.
- **Sandbox** (prelude `rebuild_block135`), three runs through the wrapper `SCR/p136/build_block136_check.py` (pass 134's wrapper, renumbered), which hashes every mesh in the scene before the build, runs the build twice in one session, hashes again, checks the chunk, and then runs the export frame check. All three runs printed the same check results; run 3 is the final code:
  - `BLOCK136_GEOMETRY 54` twice (53 houses and the W chunk);
  - repeatability: `REPEAT136 True`: the two runs give identical geometry hashes (vertices, loops, material indices, UVs and material names) on all 54 meshes; 53 `SM_Slott136_` objects;
  - hashes before and after: changed only `SM_Slott98_Buildings_W` (intended); 53 new meshes, all `SM_Slott136_*`; none gone. No other mesh in the scene changed;
  - the chunk: all 43 of pass 134's built ids and all 53 of this pass's are in `SLOTT98_DETAILED`, and no vertex of the re-created `SM_Slott98_Buildings_W` lies inside any of those 96 outlines more than 0.8 m from its walls (`CHUNKW_INSIDE … {}`), so pass 134's houses do not reappear in the chunk. (Runs 1 and 2 used a test that counted every vertex inside the outline shrunk by 0.3 m; it flagged one outline in each set, 93238253 and 93358531, where an undetailed pass-98 neighbour shares a wall and its 0.35 m eaves and facade trim reach over; the 0.8 m test in run 3 removes that false positive.)
  - shared names: `G` and `TS` are the same after the build as before it (`G` is a dict left by an earlier pass; the build sets it to the ground height only while it runs);
  - export frame check: `CHECK136_TOTAL_INVALID 0 EXPORTS_OK 54 OF 54`: 0 loops without a frame on all 54 meshes, and `export_district_fbx` succeeded for all 54 to a temporary file under `SCR/p136`, deleted after each mesh;
  - degenerate faces dropped by `drop_degenerate_faces136`: 1,058 per build over the 53 house meshes (0–62 per mesh);
  - `SANDBOX_DONE prelude 135`, exit 0.
- **Comparison** with the photos, rendered at the photo size from the cameras above (side by side in `SCR/p136/sb1/cmp_*.png`, `sb2/cmp_*.png`, `sb3/cmp_*.png`; the final ones are `sb3`):
  - The southern row on Drottning Margaretas väg (dm01_h24, dm02_h24, resected): the sections' places, colours, eaves and the gables (93358522, 93358514, 93358528, 93358516) land on the photo's within a few pixels; the lower yellow section 93358549 with its porch roof matches. The curved gable of 93358514 is drawn as a straight-sided gable with the round window; the gables' white trim and the bay under 93358528's gable are simpler than in the photo.
  - The northern row (dm05_h51, resected; dm03_h39): the red block with the balcony over the door, the cream blocks with the red wall dormers and the base line match. The dark roof storey of 93361247 is a hipped mansard in dark metal; the photo's is a flatter modern box. The white house with dormers left of 93361172 in this view is not in pass 98's data at all (no OSM outline in `source/block98.json`), so it is missing from the model.
  - 93358523 (se02_h231, resected): run 1 had the door off-centre and the round window in the pediment; now the door stands in the centre bay with the round window over it, as in the photo, and the eaves and the pediment match. The dark boarded neighbour's oriel was off-frame and too high in runs 1–2; now it sits 3 m from the pink house over the ground floor as in the photo. The pilasters and the stone door surround are not modelled.
  - 93329997 (j302_h340, resected): the white block, the windows and the hipped tile roof match; the central gable is still steeper and taller than the photo's.
  - 93329984 (j301_h161): the white boarded front, the basement windows and the brown boarded roof storey match in kind; the roof storey in the photo is taller with a flatter gable.
  - 93329949 (se01_h51): run 1 had the ridge along the street; the gable is now on the street as in the photo. The solar panels are not modelled; this camera is not resected and stands closer than the photo's.
  - The villas (dm01_h204, dm02_h204, dm04_h219), 93329941 (sb01_h235), the S:t Eriks gata houses (se01_h231, se02_h51) and the Johan III:s gata houses (j301_h341): forms and colours match in kind; these cameras are not resected and stand 1–4 m off, so the houses sit off their photo positions.
- **Official build:** done by the lead on 2026-10-04; see "Official build". The Unreal checks are pending.

## Limitations

- No new photos could be taken (the browser extension was not connected); 16 views cover the 53 houses, eight houses are not seen at all and several only far or at a grazing angle.
- About seventeen houses have measured values; five cameras are resected. Ridge heights and roof pitches are estimated.
- The houses are boxes on the OSM outline with rectangular roofs; small notches are covered by the roof or by flat annexes.
- Window and door positions are regular bays, not the real ones; the dormer counts are rules.
- No fences, garden walls, hedges or gateways outside the OSM outlines are modelled (the picket fences on Drottning Margaretas väg and Sankta Britas gata, the white garden wall on Johan III:s gata, the green door gateway of 93329941).
- Extra views that would help, as location (x, y), Street View heading and pitch:
  - the middle of the northern row on Drottning Margaretas väg (93361185, 93361177, 93361214) from (−1532, 225), heading 50, pitch 10;
  - Sankt Eriks gata's west side between 93358535 and 93358507 (93358513) from (−1362, 90), heading 230, pitch 10;
  - the south end of Sankt Eriks gata (93358511, 93358540, 93358515) from (−1360, 25), heading 250, pitch 10;
  - the corner of Johan III:s gata and Margaretaplan (93358517, 93358519) from (−1430, 165), heading 160, pitch 10;
  - the south end of Sankta Britas gata (93329942, 93329994) from (−1285, 20), heading 250, pitch 10.

## Official build

The lead built pass 136 officially on 2026-10-04.
- **Geometry and export:** the geometry check passed on the second rebuild (True), the FBX audit passed (exit 0), and the two rebuilds gave identical meshes.
- **Prevhash:** only intended changes.
  - Pass 134's `SM_Slott98_Buildings_W` changed; this pass re-creates it without its 53 houses.
  - Pass 135's five meshes are identical.
  - The rest are known earlier corrections.
- **Dry renders:** cameras 740–746, 7 of 7.
