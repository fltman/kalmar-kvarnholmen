# Pass 138: the mainland around Stensövägen, Stensviksvägen, Långviksvägen and Sturevägen

Pass 98 built the mainland houses as plain volumes inside three chunk meshes. Pass 138 takes 61 pass-98 outlines along Stensövägen, Stensviksvägen, Långviksvägen and Sturevägen out of those chunks: the town houses and blocks on Stensövägen near Ståthållaregatan, the villas further south-west on Stensövägen, and the closed villa quarter between Sturevägen, Långviksvägen and Stensviksvägen with the houses on the south side of Stensviksvägen. Each becomes its own mesh `SM_Slott138_<osm id>` (category `Slottsområdet/Mainland`, `detail_pass` 138), standing on pass 98's ground height (model z 0.30).

The scripts follow passes 134 and 136, the sibling mainland groups, closely: `scripts/prepare_block138.py` is pass 136's prepare script with this pass's selection and house table, and `scripts/build_block138.py` is pass 136's build with every prefix, name, material, marker and `detail_pass` set to 138 and the features below added. The fixes of passes 134 and 136 are kept: `TS`/`TC` are restored before the town helpers run, the house and material loops run in functions so no short global names leak, `G` is set for `steps115` only while the build runs and given back afterwards, flat roofs drop collinear and spike vertices (`simp138`, pass 134's `simp134`), and no garage carries both `garage_door` and `no_door`. Some of pass 136's one-off branches (the oriel, the boarded roof storey, the round window over a door, the canopy) are still in the build but no house of this pass uses them.

Each house gets:

- storeys (1, 1.5 or 2, the blocks over a basement with basement windows), the eaves and ridge heights, a stone plinth;
- the roof: saddle, hip or Swedish mansard (gambrel, with gable ends), in red or red-brown tile, dark tile, or flat with a glazed set-back top storey; `ridge: 'street'` puts the ridge along the street (the town houses and blocks on Stensövägen, the cream block on Långviksvägen, the yellow mansard villa), `ridge: 'across'` puts the gable on the street (93460195, 93460183, 93460157, 93460152, 93460163);
- render in the house's colour, vertical boarding with white corner boards, or brick;
- eaves boards, white bargeboards on the gables, gable windows on the steeper gables;
- windows per storey (casement, surround, sill), a door on the wall facing the street, steps where the door stands on the plinth;
- dormers, chimneys and the features in the table: the cross gables on the street front with their own width and apex (`gable_mid` with `gable_w`, `gable_top`), porches with a balcony on top (`balcony`), the balcony over a door (`entrance_balcony`), broad wall dormers and gabled dormers, with the count read on the photo where it differs from the rule (`nd`) and their colour where it differs (`dormer_mat`), garage doors. New in this pass:
  - `tower`: the tower-like top storey of 93460185, a square block 3.6 m wide rising 2.6 m over the eaves with a railing round its roof terrace;
  - `spire`: the tower of 93460161, octagonal with a spire in the photos, drawn as a square tower 3.0 m wide under a dark pyramid roof;
  - `gable_balcony`: the balcony at the eaves on the street wall (93460157's gable balcony, 93505722's black balcony);
  - `pediment`: the pedimented double door of the grey 1930s block 93460234 (white pilasters, an entablature and a triangular pediment);
  - `gable_boards`: the dark brown boarded gable of 93460152;
  - `oculus_end`: the round gable window of 93460238 (a triangle fan);
  - `glass_top`: pass 134's glazed set-back top storey, for the new house 93477789.

## Selection

The selection is computed in `scripts/prepare_block138.py`: every outline in `source/block98.json['buildings']` whose nearest named street (the OSM street lines in `references/osm-slott98.json`) is Stensövägen, Stensviksvägen, Långviksvägen or Sturevägen, leaving out every id claimed by an earlier pass (the Stagnell chapel 500979084 of pass 107, and the `ids` and `demolished` of every `source/block*.json` other than this pass's own; at the time of writing that includes passes 115–119, 134, 136 and 137, and none of pass 137's ids is among them).

**A deviation from passes 134 and 136.** They took only outlines within 25 m of their streets. Here that rule gives 42 outlines; the other 19 (listed with their distance in `source/block138.json['beyond_25m']`, 25.5–53.5 m) stand in the back lots of the same closed blocks, mostly sheds, garages and villas behind the street row. No other street is nearer to them, so no street pass would ever take them; they are included so the quarter is finished in one pass. That gives 61 outlines, close to the earlier estimate of about 68.

The two Stensövägen houses that pass 136 left to this pass, 93329960 and 93505743, are included.

Left out:

- `left_to_other_streets` (within 25 m of the four streets but nearer another): 93358537 (Margaretaplan), 93487556 and 93487582 (Torsgatan), 93487569 (Baldersvägen).
- `left_clipped`: 93326725 on Stensövägen at Vegagatan. Pass 98's data has this id twice, as two small pieces (17 m² and 246 m²) cut by its model box at y 320; the block stands mostly outside the model. It stays in the chunk.

**Demolished or empty sites.** None of the 61 outlines is a cleared site in the photos that show it; `demolished` is empty and every id gets a mesh. The two outlines at the east end of Stensviksvägen (93477842, 93477789) carry new white houses in the 2025 imagery, which are modelled as such. Five outlines are seen in no photo (93505682, 93460162, 93460184, 93460189, 93460155) and several only far or behind trees; they are built from their neighbours and OSM's level count, and whether they still stand as drawn is not verified.

The 61 ids: 93329947, 93329960, 93329962, 93329969, 93329999, 93361249, 93460152, 93460155, 93460157, 93460158, 93460160, 93460161, 93460162, 93460163, 93460164, 93460165, 93460166, 93460167, 93460169, 93460174, 93460176, 93460177, 93460179, 93460180, 93460181, 93460183, 93460184, 93460185, 93460189, 93460195, 93460196, 93460197, 93460199, 93460200, 93460201, 93460207, 93460208, 93460211, 93460217, 93460222, 93460224, 93460226, 93460229, 93460230, 93460232, 93460233, 93460234, 93460235, 93460237, 93460238, 93461693, 93477789, 93477842, 93487555, 93487559, 93487562, 93505682, 93505722, 93505743, 93505764, 94560067.

**Chunks.** All 61 outlines lie in pass 98's chunk W (x < −1150). The build adds them to `SLOTT98_DETAILED`, which already holds the ids of every earlier pass in the chain (passes 134's and 136's included), and calls pass 115's `slott98_chunks115({'W'}, 138, block138_names)`. The chunk is re-created by pass 98's code without these houses, keeps `detail_pass` 98 and gets `rebuilt_by_pass` 138. It is among this pass's meshes (62 names in all). M and E are not touched.

## Zones

Pass 116's slab method, as copied by passes 134 and 136:

- An outline that fills 85 % of its box in the frame of its longest edge is one zone; otherwise it is cut into slabs at its vertices and merged into a main body and wings, or flat-roofed annexes under 12 m² or narrower than 2.6 m.
- There is no explicit split in this pass.
- Each zone's walls follow the OSM outline exactly; walls against a neighbouring zone or house start at the neighbour's eaves.
- The door goes on the outer wall that faces one of the four streets; houses facing none use the nearest of Torsgatan, Baldersvägen, Margaretaplan, Gustaf Vasagatan, Drottning Margaretas väg, Johan III:s gata, Ståthållaregatan or Kalmarsundsparken within 40 m. Sheds have no door.

## Measurement

Photos: 31 Google Street View views captured for this pass with the Claude in Chrome extension (`captures.txt` lines `138|`, files `SCR/p138/`), 608 × 458, vertical field of view 90°, pitch +10°; each view's pano position and id were read back from the Maps URL after it snapped to the nearest panorama. Google imagery was used as a view-only reference; nothing was downloaded beyond the screenshots.

- **Identities.** All pass-98 outlines within 70 m were projected into every view from the Google position (`SCR/p138/ov138.py`, overlays `ov_*.png`, contact sheets `sheet_*.png`); every house was matched by its place in the row and its corners. The overlays show the pano positions mostly within 1–3 m, as expected.
- **Resection.** With `SCR/p100/res.py` (vfov 90, through `SCR/p138/m138.py`) from the bearings of two outline corners that are clear in the photo; heights read on the wall plane with `hit`, camera height 2.5 assumed. Where the base of the wall is visible, it checks the camera height.

| View | Google position (x, y) | Camera used (x, y), height | Corners | Used for |
|---|---|---|---|---|
| so04_h304 | (−1392.4, 240.3) | (−1393.4, 239.0), 2.5 | 93361249's two front corners (residuals ±7 px) | base at z 0.32 (so 2.5 holds), eaves 7.7 above model zero = 7.4 above the ground |
| so05_h310 | (−1285.0, 277.1) | (−1285.7, 276.4), 2.5 | 94560067's two front corners (0 and 8 px) | base at z 0.27, eaves 7.5 → 7.2 above the ground, the dormer's top 9.6 on the front plane |
| so02_h130 | (−1410.8, 231.0) | (−1411.1, 228.7), 2.5 | 93329962's side wall, both corners (1 and 3 px) | base at z 0.4, eaves 5.3 at the corner and 5.95 further along, about 5.5 above the ground used |
| lv02_h330 (and lv02_h150, the same pano) | (−1538.3, −10.5) | (−1538.3, −9.5), 2.5 | 93460196's side wall, both corners (1 and 2 px) | eaves 6.4 above model zero on the corner; the base is behind shrubs (read at 1.5, not used) |
| lv04_h145 | (−1589.5, −15.8) | (−1589.8, −18.9), 2.5 | 93460176's two front corners (4 and 2 px) | eaves 4.2 above model zero on the front plane, the roof's top 7.3 on the front plane, the cross gable's apex 8.0; the base is behind the fence (read at 1.0, not used); 3.6 / 8.4 used |
| sv05_h150 | (−1512.1, −162.6) | (−1512.5, −164.0), 2.5 | 93460234's two front corners (2 and 7 px) | base at z 0.26, eaves 7.9 → 7.6 above the ground, the wall dormer's top 10.4 on the front plane |
| all other views | Google | Google, 2.5 | none | identification, storeys, colours, roof forms |

### Houses

Heights are metres above the ground (model z 0.30). "Estimated" means read from storeys, doors, windows and the roof pitch by eye, or taken from the neighbours.

| OSM id | Identity | Photo | Storeys | Eaves / ridge | Roof | Walls | Measured or estimated |
|---|---|---|---|---|---|---|---|
| 93329947 | white rendered two-storey corner house with a red tile roof and the dark red boarded wall dormer | so03_h140 (left) | 2 | 6.6 / 10.0 | red tile saddle | white render | estimated |
| 93329960 | beige rendered two-storey corner house with a red tile roof, dormers, a balcony and the shop door | so01_h150 (close), so08_h105 (left) | 2 | 6.4 / 9.8 | red tile saddle | beige render | estimated |
| 93329962 | pink rendered two-storey corner house with a red-brown tile roof, two chimneys and the café door | so02_h130 (resected) | 2 | 5.5 / 8.6 | red-brown tile saddle | pink render | base at z 0.4, eaves 5.3 at the corner and 5.95 along the front, i.e. about 5.5 above the ground (camera resected on the side wall's two corners to (-1411.1, 228.7)) |
| 93329969 | light rendered two-storey house behind the street row (seen only far) | so03_h140 (far, centre) | 2 | 5.8 / 8.8 | red tile saddle | pale cream render | estimated |
| 93329999 | pink rendered two-storey house with a red-brown tile roof (the east part of the pink house) | so02_h130 (right edge) | 2 | 5.5 / 8.6 | red-brown tile saddle | pink render | as 93329962 (the same facade continues) |
| 93361249 | pale yellow rendered two-storey block over a basement with a red tile roof and three broad dormers | so04_h304 (resected) | 2 over a basement | 7.4 / 10.8 | red tile saddle | pale yellow render | base at z 0.32, eaves 7.7 above model zero, i.e. 7.4 above the ground (camera resected on the front corners to (-1393.4, 239.0)) |
| 93460152 | low white rendered one-storey villa with the dark brown boarded gable and a dark tile roof | su01_h100 (left) | 1 | 2.9 / 5.8 | dark saddle | white render | estimated |
| 93460155 | small shed in the back lot (not seen) | not seen | 1 | 2.4 / 3.6 | red tile saddle | grey boards | estimated |
| 93460157 | white rendered one-and-a-half-storey villa with a dark tile roof, the balcony on the street gable and a dormer | sv03_h324 (close) | 1.5 | 4.2 / 8.4 | dark saddle | white render | estimated |
| 93460158 | beige-brown brick two-storey block behind the trees | sv08_h140 (right) | 2 | 6.2 / 9.2 | red tile saddle | beige-brown brick | estimated |
| 93460160 | low white rendered house with a dark roof | lv01_h335 (right) | 1 | 2.8 / 5.0 | dark saddle | white render | estimated |
| 93460161 | white boarded villa with the octagonal tower, the cross gable, the balcony and the glazed porch | lv02_h150 (right), lv03_h145 (left) | 1.5 | 4.6 / 9.0 | red tile saddle | white boards | estimated |
| 93460162 | white rendered one-and-a-half-storey house in the back lot (not seen) | not seen | 1.5 | 4.0 / 7.8 | red tile saddle | white render | estimated |
| 93460163 | yellow boarded two-storey house with a red tile roof, the broad gable and white trim | sv06_h151 (left) | 2 | 5.6 / 9.2 | red tile saddle | yellow boards | estimated |
| 93460164 | white rendered two-storey villa with a red tile hipped roof, dormers and the balcony over the door | sv02_h338 (centre) | 2 | 6.0 / 9.4 | red tile hip | white render | estimated |
| 93460165 | white rendered two-storey block behind the trees | sv08_h140 (left) | 2 | 6.2 / 9.4 | red tile saddle | white render | estimated |
| 93460166 | white rendered one-and-a-half-storey villa with a red tile roof and the dark red wall dormer | sv01_h338 (left) | 1.5 | 4.0 / 8.0 | red tile saddle | white render | estimated |
| 93460167 | small shed behind the tower villa | lv03_h145 (behind) | 1 | 2.4 / 3.6 | red tile saddle | white boards | estimated |
| 93460169 | white rendered one-and-a-half-storey house behind the tower villa (seen only in part) | lv01_h155 (behind) | 1.5 | 4.0 / 7.8 | red tile saddle | white render | estimated |
| 93460174 | small shed between the villas | su02_h90 (behind) | 1 | 2.4 / 3.6 | red tile saddle | grey boards | estimated |
| 93460176 | yellow boarded one-and-a-half-storey villa with a red tile mansard roof and the central cross gable with the balcony over the porch | lv04_h145 (resected) | 1.5 | 3.6 / 8.4 | red tile gambrel | yellow boards | eaves 3.9 above the ground on the front plane, the roof top at 7.3 on the front plane and the cross gable's apex at 8.0 (camera resected on the front corners to (-1589.8, -18.9)); the base is behind the fence |
| 93460177 | white boarded one-and-a-half-storey villa with a red tile roof and the cross gable on the street | lv01_h335 (centre) | 1.5 | 4.0 / 8.2 | red tile saddle | white boards | estimated |
| 93460179 | white boarded one-storey house with a dark tile roof behind the birch | su04_h60 (right), su01_h100 (right) | 1 | 3.0 / 5.8 | dark saddle | white boards | estimated |
| 93460180 | yellow rendered one-and-a-half-storey house with a red tile roof and dormers | sv04_h146 (right), sv05_h150 (left) | 1.5 | 4.6 / 8.8 | red tile saddle | yellow render | estimated |
| 93460181 | garage beside the yellow house | sv06_h151 (centre) | 1 | 2.5 / 3.6 | red tile saddle | yellow boards | estimated |
| 93460183 | olive-green boarded one-and-a-half-storey villa with a red tile roof and the decorated gable on the street | lv02_h150 (left) | 1.5 | 4.0 / 8.4 | red tile saddle | olive-green boards | estimated |
| 93460184 | small white rendered house in the back lot (not seen) | not seen | 1 | 3.0 / 5.4 | red tile saddle | white render | estimated |
| 93460185 | white rendered two-and-a-half-storey villa with the tower-like top storey and the roof terrace | lv01_h155 (centre) | 2 | 6.0 / 8.6 | red tile hip | white render | estimated |
| 93460189 | small garage in the back lot (not seen; the white garage with the green sheet roof on sv02_h338 stands nearer the street and has no OSM outline) | not seen | 1 | 2.5 / 3.6 | red tile saddle | grey boards | estimated |
| 93460195 | white rendered one-and-a-half-storey house with the gable on the street and a lower beige wing with the entrance | lv03_h325 (close) | 1.5 | 4.2 / 8.4 | red tile saddle | white render | estimated |
| 93460196 | cream rendered two-storey block with a red tile roof, three dark red wall dormers and the balcony on the gable | lv02_h330 (resected) | 2 | 6.6 / 10.0 | red tile saddle | cream render | eaves 6.4 above model zero on the corner (camera resected on the side wall's two corners to (-1538.3, -9.5)); the base is behind the shrubs (read at 1.5, not used) |
| 93460197 | grey boarded garage with the green door | su05_h60 (right) | 1 | 2.5 / 3.6 | dark saddle | grey boards | estimated |
| 93460199 | cream rendered one-and-a-half-storey house in the back lot (seen only far) | sv01_h338 (far right) | 1.5 | 4.0 / 7.8 | red tile saddle | cream render | estimated |
| 93460200 | yellow boarded one-and-a-half-storey house with a red tile roof and two gabled dormers | sv02_h338 (left), sv01_h338 (right) | 1.5 | 3.8 / 7.8 | red tile saddle | yellow boards | estimated |
| 93460201 | small shed in the garden | lv03_h145 (behind) | 1 | 2.4 / 3.6 | red tile saddle | grey boards | estimated |
| 93460207 | small shed behind the hedge | lv03_h145 (right, behind the hedge) | 1 | 2.4 / 3.6 | red tile saddle | grey boards | estimated |
| 93460208 | white shed with the red door | sv05_h150 (left) | 1 | 2.4 / 3.6 | red tile saddle | white render | estimated |
| 93460211 | garage behind the white house | su01_h100 (behind the hedge) | 1 | 2.5 / 3.6 | dark saddle | grey boards | estimated |
| 93460217 | white rendered one-and-a-half-storey house with a red tile roof (seen only far) | lv01_h155 (far left) | 1.5 | 4.0 / 7.8 | red tile saddle | white render | estimated |
| 93460222 | white rendered two-storey block with a low red tile roof and the garage doors | sv04_h146 (left) | 2 | 5.8 / 7.6 | red tile saddle | white render | estimated |
| 93460224 | yellow boarded one-and-a-half-storey villa with a red tile roof and the central cross gable with the balcony over the porch | sv07_h153 (centre) | 1.5 | 4.0 / 8.6 | red tile saddle | yellow boards | estimated |
| 93460226 | small outbuilding behind the tower villa | lv03_h145 (behind) | 1 | 2.4 / 3.6 | red tile saddle | white boards | estimated |
| 93460229 | garage behind the low white house | lv01_h335 (right, behind) | 1 | 2.5 / 3.6 | dark saddle | white boards | estimated |
| 93460230 | small shed behind the white house | su01_h100 (behind the hedge) | 1 | 2.4 / 3.6 | dark saddle | grey boards | estimated |
| 93460232 | grey-blue boarded one-and-a-half-storey villa with a red tile roof, the cross gable with the balcony over the glazed veranda | su02_h90 (right), su05_h60 (centre) | 1.5 | 4.2 / 8.6 | red tile saddle | grey-blue boards | estimated |
| 93460233 | white rendered one-and-a-half-storey villa with a dark tile roof behind the trees | su03_h120 (centre) | 1.5 | 3.8 / 7.6 | dark saddle | white render | estimated |
| 93460234 | light grey rendered two-storey 1930s block over a basement with a red tile hipped roof, the central wall dormer, the pedimented double door and red-brown window frames | sv05_h150 (resected) | 2 over a basement | 7.6 / 11.0 | red-brown tile hip | grey-white render | eaves 7.9 above model zero, i.e. 7.6 above the ground, the wall dormer's top 10.4 on the front plane (camera resected on the front corners to (-1512.5, -164.0)); the base is behind the fence |
| 93460235 | small shed behind the brick block | sv08_h140 (behind) | 1 | 2.4 / 3.6 | red tile saddle | grey boards | estimated |
| 93460237 | light rendered one-and-a-half-storey house in the back lot (seen only far) | sv06_h151, sv07_h153 (behind the trees) | 1.5 | 4.0 / 7.8 | red tile saddle | pale cream render | estimated |
| 93460238 | salmon boarded one-and-a-half-storey house with a red tile roof and the round gable window | su02_h90 (left), lv04_h145 (right) | 1.5 | 4.2 / 8.4 | red tile saddle | salmon boards | estimated |
| 93461693 | small outbuilding behind the villa | su01_h100 (behind) | 1 | 2.4 / 3.6 | dark saddle | white render | estimated |
| 93477789 | new white rendered two-storey house with the set-back glazed top storey | sv04_h330 (right) | 2 | 5.8 / 6.1 | dark flat | white render | estimated |
| 93477842 | new white rendered two-storey house with a low red tile roof and solar panels | sv04_h330 (left) | 2 | 5.8 / 7.4 | red tile saddle | white render | estimated |
| 93487555 | small outbuilding behind the cream house | so07_h137 (right edge, behind) | 1 | 2.4 / 3.6 | red tile saddle | white render | estimated |
| 93487559 | beige rendered one-storey villa with a dark tile hipped roof and a chimney | so07_h137 (centre) | 1 | 3.1 / 6.2 | dark hip | beige render | estimated |
| 93487562 | cream rendered one-and-a-half-storey house with a red tile roof and the cross gable | so07_h137 (right) | 1.5 | 4.0 / 8.0 | red tile saddle | pale cream render | estimated |
| 93505682 | cream rendered one-and-a-half-storey villa with a dark roof and a chimney (not seen clearly) | not seen | 1.5 | 3.8 / 7.8 | dark saddle | cream render | estimated |
| 93505722 | grey-white rendered one-and-a-half-storey villa with a dark tile mansard roof and the black balcony | so10_h20 (centre), so06_h333 (left) | 1.5 | 3.6 / 7.8 | dark gambrel | grey-white render | estimated |
| 93505743 | white boarded one-and-a-half-storey house with a red tile roof behind the trees | so06_h333, so10_h20 (right) | 1.5 | 4.0 / 8.0 | red tile saddle | white boards | estimated |
| 93505764 | grey-white rendered wing of the mansard villa with a dark roof | so10_h20 (behind) | 1 | 3.0 / 5.4 | dark saddle | grey-white render | estimated |
| 94560067 | white rendered two-storey block over a basement with a red tile roof and the central gabled wall dormer | so05_h310 (resected) | 2 over a basement | 7.2 / 10.6 | red tile saddle | white render | base at z 0.27, eaves 7.5 and the dormer top 9.6 on the front plane (camera resected on the front corners to (-1285.7, 276.4)); eaves 7.2 above the ground |

Colours are read by eye from the photos and set as flat targets on the town textures (`M_Block138_<Key>`); there is no blue or pink town texture, so the grey-blue, salmon, olive and pink walls are tints on TownPaintWhite, TownPaintGreen and TownIvory.

## Estimated

- Every value marked estimated above, and all ridge heights (the roofs are seen only from the street; ridges are set from the eaves, the depth and a usual pitch).
- The five houses seen in no photo (see Selection) and the back-lot houses seen only far or behind trees: their whole form.
- Window counts: regular bays (2.7 m on two-storey houses, 2.9 m on one-storey houses), not the real positions.
- Doors: one per house on the street wall, by a rule (near one end on fronts longer than 6 m; in the centre on 93460234).
- Dormer counts by the rule (one per 6.5 m of street slope) except where `nd` gives the count seen; chimney places; the balcony, tower and porch sizes; the gable widths.
- The towers: which end of the front 93460185's top storey and 93460161's tower stand at, their sizes, and the square plan of 93460161's octagonal tower.
- Roof forms where only one slope or one end is seen (the hips of 93487559 and 93460164, 93505722's mansard, 93460185's hip under the tower).
- Camera heights: every height read from a non-resected pano position carries about ±0.5 m; on the resected views the camera height is assumed 2.5 m and checked against the base where it is visible (so04, so05, so02, sv05).

## Verification

- **Zones** (`previews/block138-zones.json`, `BLOCK138_ZONES_OK`): 80 zones cover the 61 outlines, 7311.7 m² of 7311.8; 0.02 m² lies outside OSM and 0.11 m² of OSM is not zoned (slivers at the cuts); the overlap is 0.008 m² (the OSM outlines themselves overlap by 0.005 m²). Status: passed.
- **Dry run.** Before each sandbox run the build was executed in plain Python with stub helpers (`SCR/p138/mock138.py`, pass 136's `mock136.py` renumbered), which checks names, face indices and material keys; it also confirms that `G` and `TS` come back unchanged.
- **Sandbox**, three runs through the wrapper `SCR/p138/build_block138_check.py` (pass 136's wrapper renumbered, with pass 136's ids added to the chunk test). It hashes every mesh in the scene before the build, runs the build twice in one session, hashes again, checks the chunk, and then runs the export frame check. Runs 1 and 2 used prelude `rebuild_block136`; run 3, after the lead's official build of pass 137, used prelude `rebuild_block137`. Run 1's FBX step failed only because a renumbering had broken the wrapper's temporary file path (fixed); its other checks matched run 2's. Run 3 is the final code:
  - `BLOCK138_GEOMETRY 62` twice (61 houses and the W chunk);
  - repeatability: `REPEAT138 True`: the two runs give identical geometry hashes (vertices, loops, material indices, UVs and material names) on all 62 meshes; 61 `SM_Slott138_` objects;
  - hashes before and after: changed only `SM_Slott98_Buildings_W` (intended); 61 new meshes, all `SM_Slott138_*`; none gone. No other mesh in the scene changed;
  - the chunk: all 43 of pass 134's built ids, all 53 of pass 136's and all 61 of this pass's are in `SLOTT98_DETAILED`, and no vertex of the re-created `SM_Slott98_Buildings_W` lies inside any of those 157 outlines more than 0.8 m from its walls (`CHUNKW_INSIDE … {}` for each pass), so the houses of passes 134 and 136 do not reappear in the chunk;
  - shared names: `G` and `TS` are the same after the build as before it (`G` is a dict left by an earlier pass; the build sets it to the ground height only while it runs);
  - export frame check: `CHECK138_TOTAL_INVALID 0 EXPORTS_OK 62 OF 62`: 0 loops without a frame on all 62 meshes, and `export_district_fbx` succeeded for all 62 to a temporary file under `SCR/p138`, deleted after each mesh;
  - `SANDBOX_DONE prelude 137`, exit 0.
  - degenerate faces dropped by `drop_degenerate_faces138`: 1,078 per build over the 61 house meshes (0–58 per mesh).
- **Comparison** with the photos, rendered at the photo size (608 × 458) from the cameras in the table (resected where noted, else the Google position at 2.5 m), side by side in `SCR/p138/sb1/cmp_*.png`, `sb2/cmp_*.png` and `sb3/cmp_*.png` (the final ones are `sb3`); `sb3/aerial.png` is an overview of the quarter:
  - Stensövägen near Ståthållaregatan (so04_h304, so05_h310, so02_h130, resected): the pale yellow block with its three dormers, the white block with the central gabled dormer and the pink corner house land on the photo's outlines, eaves and roof lines within a few pixels; the dormer sizes and the pink house's café front are estimated.
  - Långviksvägen: the yellow mansard villa 93460176 (lv04_h145, resected) matches in eaves, mansard, cross gable with the balcony and the porch; the salmon house 93460238 beside it matches in kind. The cream block 93460196 (lv02_h330, resected) matches in eaves and its three dark red wall dormers. The olive villa 93460183 and the tower villa 93460161 (lv02_h150) match in colour, gable and the tower's place; the olive villa's outline splits into two zones, so it shows a second, smaller gable the photo does not have. The white boarded villa 93460177 (lv01_h335) and the tower-topped house 93460185 (lv01_h155) match in kind; the real 93460185 is taller and narrower than the model.
  - Stensviksvägen: the grey 1930s block 93460234 (sv05_h150, resected) matches in eaves, hipped roof, wall dormer, red-brown frames and the pedimented double door; the yellow boarded house 93460163 (sv06_h151) had its ridge along the street in run 1 and has the gable on the street since run 2, as in the photo; the white villas 93460164, 93460166 and 93460157, the yellow villas 93460200 and 93460224 and the two new white houses (93477842, 93477789 with its glazed top storey) match in kind.
  - Sturevägen: the grey-blue villa 93460232 with the cross gable and balcony (su02_h90) matches in kind; the low villa 93460152 (su01_h100) has its gable on the street since run 2 with the brown boarded triangle, which renders lighter than the photo's dark brown under the studio light.
  - Stensövägen south-west (so07_h137, so10_h20): the beige hipped villa, the cream house with the cross gable and the grey-white mansard villa match in kind.
  - Not useful: lv03_h325 (the Google position is too close to 93460195 and the camera ends up at its wall; not resected), so01_h150 (the camera stands at the corner house's wall), so06_h333 and so09_h300 (hedges).
- **Official build:** done by the lead on 2026-10-04; see "Official build". The Unreal checks are pending.

## Limitations

- 31 views cover the 61 houses; five houses are not seen at all and about fifteen only far, in part or behind trees and hedges.
- Six houses have measured values (93329999 takes 93329962's); six cameras are resected (lv02_h330 and lv02_h150 share one pano). Ridge heights and roof pitches are estimated.
- The houses are boxes on the OSM outline with rectangular roofs; small notches are covered by the roof or by flat annexes. The tower of 93460161 is square, not octagonal.
- Window and door positions are regular bays, not the real ones; the dormer counts are rules except where read.
- The white garage with the green sheet roof seen on sv02_h338 has no OSM outline and is not modelled; neither are fences, hedges or garden walls.
- Extra views that would help, as location (x, y), Street View heading and pitch:
  - 93505682 and 93505764 on Stensövägen from Torsgatan's corner (−1610, 195), heading 60, pitch 10;
  - 93460195 from across Långviksvägen (−1560, −5), heading 330, pitch 10 (the pano used stood at its wall);
  - the back lots between Stensviksvägen and Långviksvägen (93460162, 93460184, 93460189, 93460199) from the lane at (−1570, −95), heading 300, pitch 10;
  - 93460155 and 93460237 on the south side of Stensviksvägen, from (−1495, −175), heading 160, pitch 10.

## Official build

The lead built pass 138 officially on 2026-10-04.
- **Geometry and export:** the geometry check passed on the second rebuild (True), the FBX audit passed (exit 0), and the two rebuilds gave identical meshes.
- **Prevhash:** only intended changes.
  - Pass 136's `SM_Slott98_Buildings_W` is re-created here without this pass's 61 houses.
  - Pass 137's six meshes are identical.
  - The rest are known earlier corrections.
- **Dry renders:** cameras 755–764, 10 of 10.
