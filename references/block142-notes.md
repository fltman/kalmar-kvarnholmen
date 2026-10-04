# Pass 142: the mainland yard buildings

Pass 98 built the mainland houses as plain volumes inside three chunk meshes (W, M, E). Passes 107 and 115–141 took them street by street; pass 140 took the last street houses and listed the 59 outlines that were left, all 25 m or more from every named street, in `source/block140.json['left_to_yards']`. Pass 142 takes all 59. Each becomes its own mesh `SM_Slott142_<osm id>` (category `Slottsområdet/Mainland`, `detail_pass` 142), standing on pass 98's ground height (model z 0.30).

**After this pass pass 98's chunks W, M and E hold no building.** Each chunk mesh still exists and exports, but holds only a hidden marker quad under the ground (see "The emptied chunks").

The buildings are:

- garages, garage rows and sheds in the back lots (Sankt Eriks gata, Drottning Margaretas väg, Ringgatan, Folkungagatan, Kungsgatan, Frejagatan, Bremergatan, the villas north of Kalmarsundsparken);
- outbuildings and back wings behind the villas and town blocks (Ståthållaregatan, Johan III:s gata, Västerlånggatan, Torsgatan, Molinsgatan, Kungsgatan);
- three sections of pass 134's 1940s terrace row (13E/13F) and pass 119's row 13G/13H on the footpaths north of Stora Dammgatan, and three houses of the row 1E/1F behind Sankta Britas gata;
- the villas on the private drive north of Kalmarsundsparken (3, 7, 9, 15A and three more) and the villa at Västerlånggatan 28 in its large garden;
- the two houses at Södra kyrkogården;
- the yellow former barracks on Gamla torget (91970346, 806 m²);
- Café Flädern's yellow boarded house and its annexes off Västerlånggatan;
- the three courtyard houses behind Unionsgatan and Smålandsgatan (4C, 4D and the cross-hipped house);
- the ice cream kiosk and the public toilets in Kalmarsundsparken.

Each building gets:

- its roof: saddle, hip, shed (`mono`, new: a single slope falling to the door side, the high wall and the side triangles in the wall material) or flat; red, brown or dark tile, grey or dark sheet metal; the ridge direction from the satellite view (on the long axis, or the short axis for the terrace row sections as pass 134 had them, `ridge='short'`);
- render in a colour, or vertical boarding with white corner boards;
- eaves boards, white bargeboards on the gables, gable windows on the steeper gables;
- windows per storey, a plinth, basement windows where the floor stands 1 m up;
- a door on the outer wall facing the nearest named street within 60 m; where no wall faces a street within 60 m (the kiosk, the toilets, the cemetery buildings), on the longest outer wall;
- garage doors on the garages (`garage_door` only, never together with `no_door`, as pass 136 fixed);
- dormers and chimneys where the satellite shows them, the central gable of the villa at 3 Kalmarsundsparken (`gable_mid`, as seen on ks1_h346), the barracks' dormers on its long wing and its south block with its own low hipped roof (`parts`, new: the zone that contains a given point gets its own height and roof).

## Selection

`scripts/prepare_block142.py` computes the set: every outline in `source/block98.json['buildings']` whose id is not in any `source/blockN.json` (any N except 142; ids and demolished ids, passes 139, 140 and 141 included) and is not the Stagnell chapel 500979084 (pass 107). That gives 59 ids, and the script asserts that they are exactly pass 140's `left_to_yards`. The check was also run by hand: 411 pass-98 ids, 59 unclaimed, no difference to the list in either direction.

- **No other unclaimed outline.** There is none: every other pass-98 outline is claimed.
- **The earlier yard passes.** Passes 121 and 122 worked on courtyard buildings on Kvarnholmen, which are pass-17 volumes in `source/district17.json`, not pass-98 outlines. None of the 59 ids is in `source/district17.json`, and none is in the 42 entries of the yard list those passes used (`SCR/yards.json`), so there is no overlap.
- **The borderline outlines** named by pass 140 (25–27 m from a street) are yard or back buildings on the satellite views, so they belong here:
  - 93306352 is the L-shaped back wing behind Västerlånggatan 13A;
  - 93333658 is a yellow two-storey house standing back from Järnvägsgatan behind the trees;
  - 93330001 is a small house with a grey hipped roof in the back lot behind Ståthållaregatan;
  - 93238239 is the end section of the terrace row 13G/13H, which faces a footpath, not Stora Dammgatan;
  - 93333638 is Café Flädern's house, standing back in its garden.
- **The courtyard buildings** 93453481, 93453490 and 93453516 behind the Unionsgatan and Smålandsgatan blocks are built here; pass 140 had left them to this job.

By chunk (pass 98's rule, outline centroid x < −1150 W, < −850 M, else E): W 39, M 11, E 9.

**Clipped outlines.** Three outlines touch pass 98's model box (x ≥ −1650, y ≤ 320):
- 93361181 (the garage behind Folkungagatan) and 93453516 (courtyard house 4D), at y 320;
- 93460194 (villa 15A), at x −1650.
Walls on the box edge are `cut` walls (5 in all): plain wall without windows, door, plinth or boards.

## Zones

The zones use pass 116's slab method, as copied by passes 134–140:
- An outline that fills 85 % of its box in the frame of its longest edge is one zone.
- Otherwise it is cut into slabs and merged into a main body and wings. Flat-roofed annexes are used for pieces under 12 m² or narrower than 2.6 m; they get full height on blocks of three storeys or more.
- `COARSE` finds the rectangles on the outline simplified by 1.0–1.5 m, for three outlines with many small jogs: 93329957 (the villa with the round bay), 91970346 (the barracks) and 93333638 (Café Flädern). The walls still follow the OSM outline.
- Walls against a neighbouring zone or house start at the neighbour's eaves. Where a later pass built the neighbour, its own eaves height is used (from its `source/blockN.json`), not pass 98's volume. The row sections 93238220, 93238239, 93291967 and 93306352's wing join pass 134's, pass 119's and pass 116's houses this way.

## Measurement

**Satellite captures.** There are 24 top-down Google satellite captures, `sat_s1`–`sat_s24`. They are `captures.txt` lines `142|`, files in `SCR/p142/`, north up, 1014 × 764 px.
- They were taken with the claude-in-chrome extension in its own tab (closed afterwards). The URL form is `@lat,lon,90m/data=!3m1!1e3`; Google turns it into 125 m. Nothing was downloaded.
- **Registration.** The transform is a similarity: the 28.2° rotation of the local frame, the URL centre at the middle of the window (507, 382), and 0.161 m/px. The scale comes from the map's 10 m scale bar (62 px).
- **Registration check.** All pass-98 outlines and road areas were overlaid on every capture (`SCR/p142/ov142.py`, `ov_sat_*.png`). Outline corners fall on the roof edges within about 1–2 m with no offset, except where tall roofs lean away from nadir. The courtyard houses on sat_s19 sit about 5 m west of their outlines. This is enough to say which roof belongs to which outline. It is not a measurement.
- **Per-building crops.** Each outline was cropped at 3× from the capture where it lies furthest from the edge (`crop_<id>.png`, sheets `sheet0`–`sheet9.png`).

**Street View.** Four views were captured, 1014 × 764, vertical field of view 90°, all April 2025:

| File | Pano id | Shows | Camera used (x, y) |
|---|---|---|---|
| gt1_h330 | 268wvSIorLBfGEAWXfpqDQ | the barracks' south block from Gamla torget | resected on 91970346 vertices 9, 10, 11 to (−890.60, −43.09); Google (−889.49, −41.94); residuals −4.0, 1.9, 7.0 px |
| gk1_h150 | HMYERPXeSygO89UuI_Bnaw | the barracks' long wing from the path by Gamla kyrkogården | Google (−881.22, 18.12); grazing view, not used for heights |
| vl1_h340 | aKt9tgr6HyBOu_N2nIinQw | Café Flädern over the garden from 7 Västerlånggatan | Google (−825.73, 127.28) |
| ks1_h346 | ns83HJ25q1MqamcdIAf9bg | the villas 93460175 and 93460156 from 3 Kalmarsundsparken | Google (−1421.54, −285.16) |

Two other attempts showed nothing useful, so they were not kept: a 2011 view near Västerlånggatan 28 (trees, a street garage) and the requested Gamla torget pano, which snapped to the one used.

**Measured values.** Only on gt1_h330, read with `hit` on the OSM wall planes (`SCR/p142/m142.py`, a copy of pass 140's tool, vfov 90; camera 2.5 m assumed):
- the south block's corner (vertex 10) reads base z 0.25, cornice 12.96;
- at vertex 11 it reads base 0.63, cornice 12.73;
- at vertex 9 it reads base 0.47, cornice 12.42.

That gives eaves of about 12.4 m above the ground. The long wing's cornice runs on at the same height in gk1_h150, which is used only to see that. All the barracks' zones therefore get eaves 12.4.

**Shadows.** The satellite imagery has long shadows to the north-north-west, but this pass did not turn shadow lengths into heights. The shadows run together and fall on other roofs, and no capture had a clean shadow of a building of known height to calibrate against. They were used only to tell sunlit slopes from slopes in shadow (see below).

**Reading roof colour.** Many roofs show a dark north slope and an orange south slope. ks1_h346 shows that 93460175, whose satellite roof is mostly dark, has a red tile roof. So a dark north slope with an orange sunlit slope was read as red tile. Only roofs that are dark or grey on both slopes were taken as dark or grey.

### Buildings

Heights are metres above the ground (model z 0.30). Confidence: **high** when the roof is clear and a photo agrees; **medium** when the roof is clear and the height is from storeys or the neighbour; **low** when the roof is partly hidden or unclear. Every height except the barracks' eaves is estimated.

| OSM id | Chunk | Building | Storeys | Eaves / ridge | Roof | Walls | Satellite reading | Confidence |
|---|---|---|---|---|---|---|---|---|
| 93306356 | E | back house behind Molinsgatan | 1.5 | 3.6 / 6.4 | red tile saddle | render Cream | sat_s18: red tile saddle, half in the shadow of the block | low |
| 93333623 | E | flat-roofed annex beside Café Flädern | 1 | 3.4 / 3.65 | pale flat | render WhiteRender | sat_s17: pale tan flat roof | medium |
| 93333627 | E | house 1B with the dark roof behind Bremergatan | 2 | 5.8 / 8.6 | dark sheet saddle | render GreyWhite | sat_s17: dark grey roof | low |
| 93333638 | E | Café Flädern: yellow boarded one-and-a-half-storey house with a red tile roof and its wings | 1.5 | 4.8 / 9.0 | red tile saddle | boards YellowBoard | sat_s17: red tile roofs, the main roof along the long axis with hipped wings | high (roof, colour); medium (height) |
| 93333658 | E | yellow rendered two-storey house with the red tile roof behind Järnvägsgatan | 2 | 6.0 / 9.4 | red tile saddle | render Yellow | sat_s17: red tile cross-gabled roof, the yellow walls seen beside it | medium |
| 93333660 | E | long garage with the dark roof behind Bremergatan | 1 | 2.6 / 4.0 | dark sheet saddle | boards GreyBoard | sat_s17: long dark grey saddle | medium |
| 93453481 | E | courtyard house 4C with the brown tile hipped roof | 2 | 7.5 / 11.5 | brown tile hip | render Cream | sat_s19: brown tile hipped roof with chimneys, a pale flat terrace roof on the east part | medium (roof); low (height) |
| 93453490 | E | courtyard house with the brown tile cross-hipped roof | 2 | 7.5 / 11.5 | brown tile hip | render Cream | sat_s19: brown tile cross-hipped roof | medium (roof); low (height) |
| 93453516 | E | courtyard house 4D with the brown tile hipped roof (north edge on the model box) | 2 | 7.5 / 11.5 | brown tile hip | render Cream | sat_s19: brown tile hipped roof, joined to the Smålandsgatan block | medium (roof); low (height) |
| 91970346 | M | yellow rendered three-storey former barracks on Gamla torget: the long wing with the dark roof and dormers, the south block with a low roof and iron balconies | 3 | 12.4 / 15.4 | dark sheet saddle | render Yellow | sat_s20: dark roof with dormers on the long wing, the south block's low roof | high (form); measured eaves |
| 93292689 | M | long garage and store building behind Kungsgatan 5 | 1 | 3.0 / 4.6 | grey sheet saddle | boards GreyBoard | sat_s12: long grey roof | medium |
| 93292702 | M | small shed in the garden east of Västerlånggatan | 1 | 2.3 / 3.0 | grey sheet shed (mono) | boards White | sat_s22: small pale roof under trees | low |
| 93292706 | M | small shed in the back lot west of it | 1 | 2.3 / 3.0 | grey sheet shed (mono) | boards GreyBoard | sat_s12: pale roof, small | low |
| 93293012 | M | house at Södra kyrkogården (no. 3) | 1.5 | 4.0 / 7.8 | brown tile hip | render WhiteRender | sat_s14: brown tile hipped roof | medium |
| 93293025 | M | long service building at Södra kyrkogården | 1 | 3.2 / 6.2 | red tile saddle | render WhiteRender | sat_s14: long red tile saddle along the long axis | medium |
| 93293041 | M | small shed at the cemetery yard, under the trees | 1 | 2.3 / 3.0 | grey sheet shed (mono) | boards GreyBoard | sat_s14: mostly hidden by trees | low |
| 93306352 | M | back wing behind Västerlånggatan 13A | 1.5 | 4.0 / 7.0 | brown tile saddle | boards YellowBoard | sat_s22: L-shaped, brown saddle, a darker low part | low |
| 93325645 | M | long garage and store building in the courtyard behind Frejagatan | 1 | 3.0 / 4.4 | dark sheet saddle | boards GreyBoard | sat_s15: long dark grey roof | medium |
| 93325656 | M | courtyard building behind Vegagatan (its pass-98 roof used to overhang pass 139's 93325650) | 2 | 5.8 / 8.4 | brown tile saddle | render Cream | sat_s15: brown saddle on the north-east part, a grey flat part to the south-west | low |
| 93326718 | M | back house 20C behind Kungsgatan | 1.5 | 4.2 / 7.8 | brown tile saddle | render Cream | sat_s16: brown-red tile saddle along the long axis | medium |
| 1453534570 | W | long boarded shed against the wall of the rose garden (Kalmar rosenträdgård) | 1 | 2.6 / 4.4 | brown tile saddle | boards RedBoard | sat_s1: saddle along the long axis, the south slope pale brown, the north slope in shadow | medium |
| 874145313 | W | the ice cream kiosk (Kalmar Glasskiosk) | 1 | 2.6 / 3.1 | grey sheet shed (mono) | boards White | sat_s10: small grey roof | medium |
| 874145314 | W | the public toilets in the park | 1 | 2.6 / 3.6 | dark tile saddle | boards RedBoard | sat_s10: dark brown low saddle, a pale strip on the north edge | medium |
| 93238186 | W | small garden shed east of the rose garden | 1 | 2.3 / 3.0 | dark sheet shed (mono) | boards RedBoard | sat_s1: a small dark roof, partly under trees | low |
| 93238220 | W | section of the 1940s terrace row (13E/13F) behind Ståthållaregatan, joining pass 134's 93238253 | 2 | 7.0 / 9.4 | red tile saddle | render Cream | sat_s21: the red tile roofs of the stepped row, a chimney on each section | medium (heights as pass 134's neighbour) |
| 93238221 | W | one-and-a-half-storey house in the garden south of the rose garden (no. 24) | 1.5 | 4.2 / 8.4 | red tile saddle | boards YellowBoard | sat_s1: red tile saddle along the long axis with dormers on both slopes | medium |
| 93238239 | W | north-east end section of the terrace row 13G/13H on the footpath north of Stora Dammgatan, joining pass 119's 93238263 | 1.5 | 3.8 / 6.6 | red tile saddle | render Cream | sat_s21: red tile roof continuous with the row, two dark roof windows | medium (heights as pass 119's neighbour, which may be low) |
| 93238283 | W | two-storey house in the garden west of Västerlånggatan 28 (near the drive) | 2 | 5.8 / 8.6 | brown tile hip | render Cream | sat_s2: brown tile hipped roof with a light terrace in the middle | low |
| 93238284 | W | section of the 1940s terrace row (13F) behind Ståthållaregatan | 2 | 7.0 / 9.4 | red tile saddle | render Red | sat_s21: red tile roof of the row's south-west end | medium (heights as the row) |
| 93238290 | W | long boarded garage beside it | 1 | 2.6 / 3.8 | grey sheet saddle | boards RedBoard | sat_s2: long grey roof, partly under trees | low |
| 93291962 | W | terrace house 1E behind Sankta Britas gata | 2 | 5.8 / 7.8 | red tile saddle | render White | sat_s3: red tile roof with a chimney, one of the row 1A-1F | medium (heights as pass 119's 93292003) |
| 93291967 | W | terrace house 1F, joining pass 119's white house 93292003 | 2 | 5.8 / 7.8 | red tile saddle | render White | sat_s3: red tile roof with a chimney | medium (heights as pass 119's 93292003) |
| 93292008 | W | north section of the same row | 2 | 5.8 / 7.8 | red tile saddle | render White | sat_s3: red tile roof with a chimney, level with 1E | medium |
| 93329937 | W | small house in the block's back lot with a red tile roof and a flat-roofed part | 1.5 | 3.8 / 6.6 | red tile saddle | render Cream | sat_s11: red tile saddle on the north-west part, a brown-grey low roof on the rest | low |
| 93329938 | W | L-shaped one-storey house with the red tile hipped roof | 1 | 3.0 / 5.6 | red tile hip | render WhiteRender | sat_s3: L-shaped hipped roof, red tile | high (roof); medium (height) |
| 93329953 | W | two-storey villa with the red tile hipped roof (no. 6) | 2 | 5.8 / 9.2 | red tile hip | render PaleYellowRender | sat_s3: square red tile hipped roof with cross gables | medium |
| 93329957 | W | villa with the cross-gabled red tile roof and the round bay, Västerlånggatan 28, in its large garden | 1.5 | 4.2 / 8.4 | red tile hip | render WhiteRender | sat_s2: red tile roof with several hipped and gabled parts and a rounded bay | medium |
| 93329965 | W | one-and-a-half-storey house with a wing, Wollinska Stiftelsen | 1.5 | 4.0 / 7.6 | red tile hip | render Yellow | sat_s3: red tile hipped roof with a short wing | medium |
| 93329980 | W | flat-roofed outbuilding | 1 | 3.2 / 3.45 | grey flat | render GreyWhite | sat_s3: light grey flat roof | high (roof); medium (height) |
| 93329987 | W | small red tile outbuilding | 1 | 2.5 / 3.8 | red tile saddle | boards RedBoard | sat_s3: small red tile saddle | medium |
| 93330000 | W | one-and-a-half-storey house with dormers behind Ståthållaregatan | 1.5 | 4.0 / 8.0 | red tile saddle | render Cream | sat_s3: red tile saddle with dormers, a dark annex on the north-west side | medium |
| 93330001 | W | small one-storey house with the grey hipped roof (no. 1) | 1 | 3.0 / 5.4 | grey sheet hip | render WhiteRender | sat_s3: grey sheet hipped roof | medium |
| 93358502 | W | garage in the back lot of Sankt Eriks gata | 1 | 2.5 / 3.0 | grey sheet shed (mono) | boards GreyBoard | sat_s4: grey roof, low | medium |
| 93358543 | W | garage with the pale ribbed sheet roof | 1 | 2.5 / 3.0 | grey sheet shed (mono) | boards GreyBoard | sat_s4: pale grey ribbed roof | medium |
| 93358547 | W | garage beside it | 1 | 2.5 / 3.0 | grey sheet shed (mono) | boards GreyBoard | sat_s4: grey roof | medium |
| 93361181 | W | L-shaped garage building behind the Folkungagatan rows (north side clipped by the model box) | 1 | 2.6 / 4.0 | grey sheet saddle | boards GreyBoard | sat_s6: grey sheet saddle | medium |
| 93460156 | W | villa with the red tile roof and the white gable (FL-Net) | 1.5 | 4.2 / 8.4 | red tile saddle | render Cream | sat_s7: red tile roof | medium |
| 93460172 | W | two-storey villa with the hipped roof and the low front part | 2 | 5.6 / 8.6 | red tile hip | render WhiteRender | sat_s7: roof mostly in shadow, the south slope and the front part red tile | low |
| 93460175 | W | white rendered villa with the red tile roof and the central gable, 3 Kalmarsundsparken | 1.5 | 4.0 / 8.2 | red tile saddle | render WhiteRender | sat_s7: red tile roof, the north slope in shadow, the gable on the south slope | high |
| 93460187 | W | two-storey villa with the cross-hipped red tile roof (no. 7) | 2 | 5.6 / 9.0 | red tile hip | render Cream | sat_s7: red tile cross-hipped roof | medium |
| 93460194 | W | villa with the red tile hipped roof and dormers (15A; west end clipped by the model box) | 1.5 | 4.2 / 8.0 | red tile hip | render PaleYellowRender | sat_s8: red-brown tile hipped roof with dormers | medium |
| 93460203 | W | garage north of the villas | 1 | 2.5 / 3.0 | grey sheet shed (mono) | boards GreyBoard | sat_s7: grey roof | medium |
| 93460204 | W | two-storey villa with the cross-hipped red tile roof (no. 9) | 2 | 5.6 / 9.0 | red tile hip | render WhiteRender | sat_s8: red tile cross-hipped roof with dormers | medium |
| 93460209 | W | garage beside the villa | 1 | 2.5 / 3.8 | red tile saddle | boards GreyBoard | sat_s7: red tile roof | medium |
| 93460214 | W | boarded garage with the brown roof off Gustaf Vasagatan | 1 | 2.6 / 4.4 | brown tile saddle | boards RedBoard | sat_s9: brown saddle along the long axis | medium |
| 93487550 | W | villa with the cross-hipped red tile roof (no. 2) behind Torsgatan | 1.5 | 4.0 / 8.0 | red tile hip | render WhiteRender | sat_s23: red tile cross-hipped roof | medium |
| 93487564 | W | house behind Torsgatan with a red tile saddle and flat-roofed additions | 1.5 | 3.6 / 6.8 | red tile saddle | render Cream | sat_s5: red tile saddle on the west part, grey and pale flat roofs on the rest | low |
| 93505688 | W | red-roofed garage behind Ringgatan | 1 | 2.5 / 3.8 | red tile saddle | boards GreyBoard | sat_s24: red tile saddle | medium |
| 93505695 | W | garage row behind Drottning Margaretas väg | 1 | 2.5 / 3.8 | red tile saddle | boards GreyBoard | sat_s24: red tile saddle on the south-west part, grey flat roof on the rest | medium |


Colours are flat targets on the town textures (`M_Block142_<Key>`, pass 140's table). Wall colours of buildings not seen from a street are a plausible choice, not a reading.

## Estimated

- Every height except the barracks' eaves: from storeys, roof pitch, the joined neighbour (the terrace rows) and the type (garages 2.5 / 3.6–3.8 as in passes 136–139).
- Wall colours and boarding/render for every building not seen in Street View (all but 91970346, 93333638, 93460175 and 93460156).
- The courtyard houses' height (7.5 / 11.5); no view shows them.
- Window and door positions (regular bays, door rule), dormer counts, chimney places.
- 93238239 and the row 13G/13H: the satellite shows the row's roofs continuous with dormers, like the 1940s rows; pass 119's neighbour 93238263 has 3.8 / 6.6, which this pass follows so the roofs join. The real row may be a storey taller.

## The emptied chunks

Every id of pass 98's chunks is now in `SLOTT98_DETAILED`, so `slott98_chunks115({'W','M','E'}, 142, block142_names)` draws no geometry for them. That function then removes the old chunk object, keeps its name in `block142_names` and creates no new object (`if not m.v: continue`, because a list of names was passed). Two simpler choices were tested or traced first, and both fail:

- **An empty mesh object** (no vertices, a UV map named `UVMap`) was put through the export tail's steps in Blender on its own (`SCR/p142/emptytest.py`). `calc_tangents` raises "Tangent space computation needs a UV Map, "UVMap" not found" (the map has no loops), so `export_district_fbx` raises too, and the official build's tail (which calls `calc_tangents` on every name without a guard) would stop. The FBX audit itself would accept an empty mesh: it takes `min(lens) if lens else None` and only fails on an exception.
- **Removing the chunks.** The names `SM_Slott98_Buildings_W/M/E` are in `block98_names` and in the name lists of passes 115–140. `rebuild_polish15`'s export tail looks up `bpy.data.objects[name]` for every one of them, and so do the geometry audit and the lead's `prevhash.py` for the earlier passes' repeatability reports. A missing object raises `KeyError`. The stale FBX files and manifest entries of the chunks, still holding the 59 volumes, would also stay in `exports/`.

**Chosen.** Each emptied chunk keeps one marker (`chunk_stubs142` in the build):
- a 0.4 × 0.4 m horizontal quad, two-sided, in pass 98's grey;
- at model z 0.20, 0.10 m under pass 98's ground (0.30);
- at a point on open land at least 5 m from any building outline. The prepare script checks this (`source/block142.json['chunk_stubs']`, `checks['stubs']`):
  - W at (−1380, −330), in Kalmarsundsparken, 46.4 m clear;
  - M at (−950, 40), on Gamla kyrkogården, 25.7 m clear;
  - E at (−700, 40), 33.6 m clear.

The marker is finished like the chunk: pass 115's finisher, `detail_pass` 98, `rebuilt_by_pass` 142, plus `chunk_empty_stub` True. Its name stays in `block142_names` exactly once. So the chunk meshes exist, export (8 vertices, 2 faces each) and pass the frame check. The manifest gets a real entry for each, and the FBX audit sees normal vectors.

For the lead:
- A later pass that calls `slott98_chunks115` with a list of names will meet the same empty case. It must keep the markers (call `chunk_stubs142()` again) or handle it in the same way.
- If the chunks should rather be retired, that means removing the three names from every earlier pass's list, removing their FBX files and manifest entries, and changing `prevhash.py`. That is a lead decision, and this pass did not do it.

## Verification

- **Zones** (`previews/block142-zones.json`, `BLOCK142_ZONES_OK`): 59 outlines, 6645.5 m² of 6645.5 zoned.
  - 0.05 m² lies outside OSM and 0.09 m² of OSM is not zoned.
  - The overlap is 0.035 m², equal to the outlines' own overlap.
  - There are 5 cut walls, no building is left in the chunks (W 0, M 0, E 0), and the stub points pass their checks.
  - The prepare script gives an identical `source/block142.json` when run twice (same md5).
- **Sandbox**, through the wrapper `SCR/p142/build_block142_check.py`, a copy of pass 140's. The prelude was `rebuild_block141` (pass 141's official chain).
  - The wrapper hashes every mesh before the build and runs the build twice in one session, as the official build does.
  - It hashes again, then checks the chunk exclusion per pass for passes 134, 136, 138, 139, 140 and 142.
  - Last, it runs the export frame check with the export tail's preparation and `export_district_fbx` to a temporary file, which is deleted after each mesh.
  - **Run 1:**
    - `BLOCK142_GEOMETRY 62` twice: 59 buildings and the three chunks.
    - `REPEAT142 True 62 62 59 3`: the two runs give identical geometry hashes on all 62 meshes. There are 59 `SM_Slott142_` objects and 3 chunk objects.
    - Hashes before and after: only `SM_Slott98_Buildings_E`, `_M` and `_W` changed (intended); 59 new meshes, all `SM_Slott142_*`; none gone.
    - Shared names: `G` and `TS` are the same after the build as before.
    - Chunk exclusion: no chunk vertex lies more than 0.8 m inside any outline. That holds for this pass's 39/11/9 ids and for every other detailed id: W 183, M 116, E 53. Per pass, passes 134 (W 37, M 6), 136 (W 53), 138 (W 61), 139 (M 8, E 11), 140 (W 18, M 2, E 1) and 142 are all clear.
    - Pass 139's known exception is gone with 93325656 now built: the pass-98 roof of 93325656 overhung its 93325650.
    - `CHUNK142_LEFT`: 0 volumes in each chunk, 8 vertices each (the marker), all at z 0.20.
    - Export frame check: `CHECK142_TOTAL_INVALID 0 EXPORTS_OK 62 OF 62`.
    - `drop_degenerate_faces142` dropped 2030 faces over the two builds.
    - `SANDBOX_DONE prelude 141`.
  - **Run 2**, after one change: 93333623's flat roof is pale (`LightBrick`) instead of grey, as on sat_s17. Everything else is the same as run 1:
    - `BLOCK142_GEOMETRY 62` twice and `REPEAT142 True 62 62 59 3`.
    - Only the three chunks changed; 59 new meshes; none gone.
    - `G` and `TS` are unchanged.
    - No chunk vertex lies inside any outline, for any pass.
    - `CHUNK142_LEFT` is 0 / 0 / 0, with the markers at z 0.20.
    - `CHECK142_TOTAL_INVALID 0 EXPORTS_OK 62 OF 62`.
    - 2030 faces dropped over the two builds.
    - `SANDBOX_DONE prelude 141`.
- **Comparison.**
  - **Top-down.** Renders north up at the capture scale were set beside every satellite capture: camera 200 m above the ground, vfov 34.18° at 1014 × 764, which gives 0.161 m/px. They are in `SCR/p142/sb1/cmp_top_s*.png` (24 captures) and `sb2/`.
    - Footprints, ridge directions and roof colours agree on the captures checked: s3 (the Ståthållaregatan blocks: the hipped villas, the L-shaped hip, the grey flat outbuilding, the grey hip, the row 1E/1F), s7 (the Kalmarsundsparken villas and garages), s14 (the cemetery houses), s17 (Café Flädern, the dark-roofed house and garage, the yellow house), s19 (the three brown hipped courtyard houses), s20 (the barracks' dark long wing and the low-roofed south block) and s21 (the terrace rows).
    - Simplified: the round bay of 93329957 and the cross gables of the villas are covered by one hip roof with wings. Café Flädern's north wing reads as a second saddle.
  - **Street View.**
    - gt1_h330 (resected): the yellow three-storey south block, its stone plinth, the eaves height and the low roof match closely. The iron balconies are not modelled.
    - ks1_h346: the white villa with the red tile roof and the central gable matches in form, colour and position.
    - vl1_h340: Café Flädern's yellow boarded house with red tile roofs reads in the right place behind the garden.
- **Official build:** done by the lead on 2026-10-04; see "Official build". The Unreal checks are pending.

## Limitations

- Almost everything is estimated: the roofs are read from one satellite epoch at about 0.16 m/px, the heights from storeys and type. Only the barracks' eaves are measured.
- Simple forms: one roof per zone, regular windows, the door by rule. Verandas, glazed porches, balconies (including the barracks' iron balconies and its gallery over the ground-floor projection on the long wing), the roof terrace of 93238283 and 93453481 and the round bay of 93329957 are not modelled.
- The barracks' long wing has a one-storey projection with a roof gallery along its east side (gk1_h150). The model takes the whole outline to the eaves of 12.4.
- The courtyard houses behind Unionsgatan and Smålandsgatan are not seen from any street. Their storeys and height are a guess from the roof size.
- The terrace row 13G/13H follows pass 119's low estimate for continuity (see Estimated).
- No fences, hedges, garden walls, greenhouses or sheds without an OSM outline are modelled.
- Three outlines are clipped by pass 98's model box; their parts outside it are not modelled.
- Extra views that would help, as location (x, y), Street View heading and pitch:
  - the courtyard behind Unionsgatan through the gateway on Smålandsgatan: (−705, 300), heading 60, pitch 15;
  - the terrace row 13G/13H from the footpath: (−1225, 150), heading 330, pitch 10;
  - Södra kyrkogården's service building from the cemetery drive: (−1030, −225), heading 60, pitch 10.

## Official build

The lead built pass 142 officially on 2026-10-04.
- **Checks:** the geometry check passed on the second rebuild (True), the FBX audit passed (exit 0), and the two rebuilds gave identical meshes.
- **Prevhash:** only intended changes.
  - Pass 140's chunks W, M and E are re-created as empty stubs.
  - Pass 141's towers are identical.
  - The rest are known earlier corrections.
- **Dry renders:** cameras 790–797, 8 of 8.
