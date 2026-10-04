# Pass 115: Stadsparken and Slottsvägen

Pass 98 built the 412 mainland houses as plain volumes inside three chunk meshes (`SM_Slott98_Buildings_W`, `_M`, `_E`). Pass 115 takes fourteen of them out of the chunks. Each becomes its own mesh, `SM_Slott115_<osm id>` (category `Slottsområdet/Buildings`, `detail_pass` 115), with its real form.

In Stadsparken:

- **91931339, Kalmar konstmuseum:** a black block on the full angular OSM outline, 17.5 m high, clad in square black panels (ribs on a 1.25 m grid). The glazed entrance on the short north-west faces sits under a dark sign band, with a landing and three steps towards the park. There are three large windows on the upper floors.
- **91222116, Byttan:** a white rendered one-storey restaurant on a grey plinth. Its windows have dark glazing bars. The low dark roof has wide eaves (0.95 m). A white upper storey with a band of windows is set back 4.6 m and has its own low dark roof and a chimney.
- **91222187 and 874870421:** small park buildings with no usable view. They are modelled plainly as cream rendered pavilions, one under a red hipped roof and one under a low dark roof, each with one door.

On Slottsvägen:

- **93332243, Slottshotellet:** three zones.
  - The red rendered main range has white window frames and two rows of windows. Its steep red tile hipped roof has two cross gables on the south-east front, and there is a chimney.
  - The north-east wing and the small link have the same render under red tile hips.
  - The green west wing (the green house in the Molinsgatan 3 view) is vertically boarded on a grey plinth, with ochre corner boards and window frames. It has a saddle roof with its gable to the south-west, an attic window in the gable, and ochre bargeboards with a row of carved drops.
- **93332252, Västerlånggatan 1:** a salmon rendered villa under a steep brown tile saddle roof. A cross gable on the north side carries the arched glazed balcony door. Below it, an iron-railed balcony stands on the porch. There is a chimney.
- **93306354:** a red-brick house under a dark grey standing-seam saddle roof with four roof lights on the south-east slope and arched windows in the gables. A glazed timber veranda with a flat roof runs along its south-east side.
- **387312779 and 387312778:** the low dark-green boarded house with a flat roof, and the narrow dark-green shed beside it.
- **91970278:** the cream villa.
  - Two high storeys stand on a 0.95 m grey plinth, with a string course between them.
  - The ground-floor windows are arched and the upper windows rectangular.
  - The saddle roof runs along Slottsvägen. Both gables are pediments; the east one has a window and a round ornament.
  - The arched door on the east front stands on steps. The steps are their own zone, from the OSM outline's bump.
  - A lower rear part stands on the north side.
- **91970355:** a white rendered pavilion under a dark brown hipped mansard roof (steep lower slopes, low top). It has a dormer on each long side, a central chimney, arched windows on a low plinth, and one door.
- **91970390:** a cream two-storey house on a 1.0 m plinth, with eight window bays per long side. It has a flat roof with a railing, a dark grey rooftop storey set back 1.6 m from the long sides (with windows), and a glazed entrance porch under a low dark roof on the north-east front.
- **91970274, the Söderport pavilion:** cream, one storey, on a grey plinth. Tall windows under cornice hoods stand between pilaster strips. The grey saddle roof runs along the long axis. The south-west gable towards Kungsgatan is a pediment with a lunette (a fan-barred semicircular window), and the north-east gable is a plain pediment. A lower flat-roofed link stands on the north side (the narrow OSM strip).
- **564958332, KIKAIN:** a round white kiosk under a dark conical roof with serving hatches. There is no usable view; it is estimated.

### The SLOTT98_DETAILED mechanism (for later passes)

Mainland detailing will continue over several passes, so the chunks are re-created by a reusable function in `scripts/build_block115.py`:

- **`SLOTT98_DETAILED`** is a global set of the OSM ids (strings) that later passes model as their own meshes. It is initialised as `globals().get('SLOTT98_DETAILED',set())|{'500979084'}`, which adds the Stagnell chapel that pass 107 took out. Pass 115 then adds its fourteen ids, from `source/block115.json['ids']`.
- **`slott98_key115(b)`** gives the chunk key of a pass-98 building record by pass 98's rule: centroid x < −1150 is 'W', < −850 is 'M', otherwise 'E'.
- **`slott98_chunks115(keys, by_pass=115, names=None)`** re-creates `SM_Slott98_Buildings_<key>` for each key in `keys`. It uses pass 98's exact chunk code: pass 98's materials (`B98[...]`), its wall-colour list (copied as `WALLS98_115`, because `M` and other globals are reassigned by later passes), the ground height 0.30 as a literal, `frame98`, `plain`, `bz_wall`, `inset_roof` and `facade_box`. It skips every id in `SLOTT98_DETAILED`.
  - The objects keep `detail_pass` 98 and `reference_notes` `references/block98-notes.md`, and get `rebuilt_by_pass` = `by_pass`.
  - A later pass passes `names=blockN_names`, so the chunks are listed among its own meshes.
  - A chunk left with no house is not created.
- **Pass 115 calls it** for the chunks its houses sit in: 'M' (91970390, 91970274, 91970355, 91222187) and 'E' (the rest).
- **A later pass** (Gamla stan, for example) does this:

  ```
  SLOTT98_DETAILED|={...its ids...}
  slott98_chunks115({...its chunk keys...}, NNN, blockNNN_names)
  ```

  Because the set accumulates, the chunks it re-creates also stay without the houses of passes 107 and 115. Note that the order matters: pass 115 must be in the build chain before the later pass.

## Measurement

The photos were captured for the pass (`SCR/p115`, `captures.txt` lines starting `115|`). The vertical field of view is 90°, and the images are 700 × 375 (Västerlånggatan 756 × 405).

- **Identities.** These were resolved by projecting all OSM outlines into each view (bearing ranges and distances from the pano positions; outline overlays):
  - Slottsvägen 6 (h200): the cream villa with the pediment is 91970278.
  - ZuP (h160): the white mansard pavilion is 91970355; the white house at the right edge is 91970390.
  - tSy4 (h127): the cream house with the rooftop storey is 91970390.
  - Kungsgatan 3 (h18): the Söderport pavilion is 91970274.
  - Slottsvägen 3 (h300): the red-brick house with the glazed veranda is 93306354 (u 95–289). The dark-green low building is 387312779 (u 345–441, 25–35 m). The red rendered house with two steep gables, 55–88 m away, is Slottshotellet 93332243.
  - Västerlånggatan 1 (h144): the salmon villa is 93332252, with Slottshotellet red to its right.
  - Molinsgatan 3 (h20): the green boarded gable house faces the camera with its gable. It is the south-west wing of the Slottshotellet outline (gable edge 8.8 m in OSM), with the red main range behind it to the right.
- **Resection** was done by grid search on outline corners. The base rows were placed at z 0.30 (pass 98's ground), with the camera at z 2.5.

| Panorama (view) | Google position (x, y) | Resected (x, y) | Residual | Used for |
|---|---|---|---|---|
| kOADR4wBvuoy64hD2udb9A (Slottsvägen 6, h200) | (−781.5, −24.1) | (−781.2, −24.5) | 0.7 px | villa 91970278 |
| ZuP-kkRxDpw64MShFT3Iug (h160) | (−849.0, −30.0) | (−850.5, −31.6) | 6.7 px | pavilion 91970355 |
| tSy4kkSIzJOmqQ_y9u40TA (h127) | (−878.1, −30.8) | (−879.8, −31.6) | 7.3 px | 91970390 |
| Pe8f9R_Exr-ebUPMJB2oAQ (Kungsgatan 3, h18) | (−967.5, −99.4) | (−971.6, −101.5) | 7.2 px | Söderport 91970274 |
| wiH30m_WF90DChHSHAanxQ (Slottsvägen 3, h300) | (−762.9, −12.8) | (−770.5, −10.1) | 2.0 px (bearings only) | 93306354 |
| 939kj68J7l-wmZk_djciOw (Molinsgatan 3, h20) | (−763.9, 42.5) | not resected; about (−766, 41.5) from the gable's apparent size | – | green wing |
| sdkNcTMSMMxaerNpYty3Ag (Västerlånggatan 1, h144) | (−717.5, 98.2) | not resected | – | 93332252 |
| CIHM0ogKEICAgIDcr5vTyw (USERPHOTO, h20 and h106) | (−715.4, −40.5) | unreliable; not resected | – | museum, Byttan |

The Slottsvägen 3 resection moves the camera 8 m, which is more than the usual pano error, so its heights are the weakest of the measured ones.

Measured heights (metres above the ground, read on the plane of the named wall):

| House | Measured | Estimated |
|---|---|---|
| 91970278 villa | cornice 8.9; pediment apex about 12.1; string course 4.9; east front 11.5 m with a pediment over its full width | window and door sizes; the rear part; roof colour |
| 91970355 pavilion | eaves 3.5–3.7; mansard break about 5.6–6.3 and top about 6.4–7.0 (both read on the wall plane, so they are low); arched window 0.6–2.6 | dormer size; chimney |
| 91970390 | cornice 7.5–7.9; rooftop storey top about 9.1–9.6; porch top about 3.2; facade 21.3 m with 8–9 bays | rooftop storey set-back (1.6 m) and height (2.4 m), drawn at 10.2 |
| 91970274 Söderport | cornice 4.0–5.3 and apex 7.2–8.7 (two readings; the base row misses by 8 px), drawn at 4.4 / 7.8; windows about 1.0–3.3 | side windows; the north link (3.0 m) |
| 93306354 | gable apex 8.0; eaves 4.5; gable half-width 3.7 m, so the brick body is about 7.5–7.8 m deep and the veranda takes the rest of the 10.8 m OSM depth; veranda top about 3.6 | roof lights (four, from the photo's count); door |
| Slottshotellet green wing | eaves about 3.1–3.3 and ridge about 7.0 from the gable's angular size (camera not resected) | attic window; door |
| Slottshotellet red main range | eaves in the 8–11 m range from a far (55–88 m) view, drawn at 7.6 | ridge 12.6; the cross gables' place and size; the north-east wing (7.2 / 11.0) |
| 93332252 villa | – | eaves 3.7, ridge 8.4, cross gable at 4.6 m from the east end (read on the photo at 28 % of the facade), balcony |
| Konstmuseum | – | 17.5 m (the user photo, read with an assumed camera height of 2.6 m, gives 18–20 m; one height for the whole block, as perspective explains the apparent step) |
| Byttan | wall about 3.8 m (user photo, scaled) | the upper storey's inset and height (7.0) |
| 387312779, 387312778 | top about 3–4.4 (far) | drawn at 3.4 and 2.6 |
| 91222187, 874870421, KIKAIN | – | all (no view) |

Colours are read by eye from the photos and set as flat targets on the town textures.

## Estimated

- Anything in the "Estimated" column above.
- Backs and sides not seen in any view. They repeat the street-front window pattern (bays at the zone's spacing), without special detail.
- Doors on unseen sides: one per house, placed on a plausible wall.
- The museum's large upper windows and their positions. The real building has a few large windows; their places are not verified.
- The park pavilions and KIKAIN. Their form is a guess.

## Verification

- **Zones** (`previews/block115-zones.json`): the 20 zones cover the 14 outlines, 2828.5 m² in all.
  - 0.0 m² lies outside OSM and 0.02 m² of OSM is not zoned.
  - The overlap is 0.088 m², exactly the overlap of the OSM outlines themselves (the museum and Byttan touch).
  - Status: passed.
- **Sandbox** (prelude rebuild_block113): two runs.
  - The first stopped on a zone without a front (fixed: zones without one fall back to their longest edge, and `shn` uses the main range's front).
  - The second printed `BLOCK115_GEOMETRY 16` and `SANDBOX_DONE`.
  - Degenerate faces dropped per mesh: 0–372 (the villa 372, from the arched heads and pediment rods; the mansard 153).
- **Chunk identity**, run in the same sandbox through a wrapper (`SCR/p115/build_block115_verify.py`):
  - A snapshot of `SM_Slott98_Buildings_M` (pass 107's version) and `_E` (pass 98's) was taken before the build.
  - After the build, `slott98_chunks115({'M','E'})` was run again with only the chapel in the set. Both chunks came out identical to the snapshot: the same vertex count (2,010,430 and 1,194,827), the same sorted vertex coordinates to 0.1 mm, and the same per-face materials.
  - Pass 115's chunks have 1,931,658 and 992,037 vertices.
- **Comparison** with the photos (side-by-side images in `SCR/p115/sb2/cmp_*.png`), rendered from the resected cameras at the photo size:
  - Villa 91970278: form, pediment, arched ground floor and string course match. The model stands a little closer in the frame (camera residual).
  - Pavilion 91970355: the mansard, dormer and arched windows match.
  - 91970390: the bays, porch, rooftop storey and railing match. The photo's stair-window offset in the left bays is not modelled.
  - Söderport: the pediment, lunette and windows match in place and size.
  - 93306354 and 387312779: the gable, roof lights and veranda read correctly, and the dark-green house sits at the right place.
  - Green wing: gable form, colours, ochre trim and attic window match. The camera is estimated.
  - Västerlånggatan 1: the form and colours match; the view is mostly hedge.
  - Museum: the black block, glazed entrance, steps and Byttan beside it read correctly. The camera is invented, since the user photo is unreliable.
- **Pending:** the official build, the repeatability check of two rebuilds and the export, which only the official build covers, and the Unreal checks. The lead fills in the build results.

## Limitations

- The museum is one prism on the OSM outline at one height. The real building's stepped and angled volumes, its exact window openings and the "KK" sign are not modelled. Its panel grid is a rib pattern, not individual shingles.
- Slottshotellet is the least certain building. Its main range was only seen from 55–88 m behind trees, so the storey count, the cross gables and the north-east wing are estimates.
- Byttan's roof shape and upper storey are from one unreliable user photo.
- Window patterns are regular bays. Actual window counts are matched only on the measured fronts (91970390, Söderport, villa 91970278).
- Extra views that would help, given as location (x, y), Street View heading and pitch:
  - Slottshotellet's south-east front from Slottsvägen near (−735, 30), heading 0, pitch 10;
  - the museum's park side from (−700, −20), heading 160, pitch 20;
  - Byttan's south side from (−715, −85), heading 30, pitch 5.

## Official build

The lead's build of pass 115 passed the Blender geometry checks and the FBX export, and two rebuilds gave identical meshes. Prevhash reports pass 98's SM_Slott98_Buildings_E and _M and pass 107's SM_Slott98_Buildings_M as changed. That is intended: the chunks are re-created without the fourteen buildings, and every other house in them is identical (checked in the sandbox, see above). The other changes are the earlier intended corrections. The Unreal import and its checks are deferred.
