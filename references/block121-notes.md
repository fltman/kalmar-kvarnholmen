# Pass 121: courtyard houses, back ranges and outbuildings in the west half of Kvarnholmen

Pass 121 replaces sixteen generic pass-17 volumes (rendered two-storey blocks with hipped roofs) that stand inside the blocks or behind the street fronts, and the sheds and pavilions in the station area by Ölandskajen. They cannot be seen from the streets, so the pass works from top-down satellite views. **Everything in this pass is estimated**; nothing is measured from a resected photo except the check of two houses on Ölandsgatan against one panorama.

Each house keeps its mesh name and OSM outline and gets a plausible form:

- the roof form, ridge direction and roof colour read from the satellite view;
- storeys from the district volume, capped at one storey for small sheds;
- boarded walls (falu red, yellow, sage green) or render, matched to the neighbours or to typical courtyard buildings;
- windows per storey, one door on the side facing the yard, a stone plinth, an eaves board, and corner boards on boarded walls;
- dormers, a wall dormer, roof lights and chimneys where the satellite or the photo shows them.

Three outlines are L-shaped and are split into a main range and a lower part: 91846989, 91846948 and 93238216. The goods shed 90965018 is split where its roof changes colour.

Google imagery is a working reference only. No pixel is used as a texture; materials are flat colours on the town textures.

## Sources and registration

Five top-down Google satellite captures, north up, 728 × 419 px (pass 121 lines in `captures.txt`):

| Capture | Centre (local) | Covers |
|---|---|---|
| sat_a1 | (−395, −175) | 90965018, 90977165, 90977169, 90965000 |
| sat_a2 | (−125, −115) | 92379273, 92379300, 92379268 |
| sat_a3 | (10, −105) | 92412871, 92412839, 92412854 |
| sat_a4 | (125, −110) | 91846989, 91846939, 91846948 |
| sat_a5 | (115, −10) | 91846923, 93238216 |

**Registration.** Each capture was registered with a similarity transform from local x,y to pixels: the 28.2° rotation of the local frame, the URL centre, a scale and an offset.
- **Scale.** The scale comes from two street crossings on sat_a2: Kaggensgatan × Södra Långgatan and Kaggensgatan × Ölandsgatan, 71.5 m apart in the road data and about 233 px apart in the image. That gives 0.307 m/px.
- **Offset.** The overlay needed a shift of −5 px in x (1.5 m).
- **Check.** The same transform was checked by overlaying all district outlines and the road centrelines on all five captures (`SCR/p121/ov_a*.png`, `cr_*.png`, `b*.png`). Street fronts and outline corners line up within about 1–2 m by eye. That is enough to tell which roof belongs to which outline. It is not a measurement: satellite roofs lean away from their footprints and overhang them.
- **Render check.** The sandbox renders north-up top-down views at the same scale (camera 200 m up, vfov 34.53° at 756 × 405), and they were set beside the captures (`c_sb*_a*.png`, `z_sb*_a*.png`). The station shed and the two pavilions fall on the same pixels in both.

**Street View.** One panorama shows two of the houses, over a garden from Ölandsgatan:

| Panorama | Where | Camera (resected by pass 111) | Used for |
|---|---|---|---|
| 91846937_h337 (JOrgcZuk…) | 30 Ölandsgatan | (130.49, −154.68, 2.58) | 91846939 and 91846989 |

The panorama shows:
- **91846989:** a white rendered two-storey house with a red tile saddle roof and three dormers, and a red boarded east gable;
- **91846939:** a pale sage-green boarded one-and-a-half-storey house with a red tile roof and a white gabled wall dormer in the middle, with white frames.

The other panoramas near these coordinates (Västra Sjögatan 4, Kaggensgatan 38, Storgatan 50, Proviantgatan 1, Stationsgatan) see only the street fronts.

## Satellite reading and chosen form

Confidence: **high** when the roof form and colour are clear and agree with a photo; **medium** when the roof is clear but the walls and height are guessed; **low** when the roof is partly in shadow or unclear; **none** when there is no satellite view.

| Id | Where | Roof read from satellite | Chosen form | Confidence |
|---|---|---|---|---|
| 90965018 | goods shed by the tracks, Ölandskajen | long low pitched roof, grey-brown; the south-east 10.5 m paler | one storey, eaves 4.6, ridge 6.3, saddle along the shed; falu red boarding, sliding doors on both long sides, small high windows; the pale end as its own zone | medium (roof), low (walls) |
| 90977165 | pavilion, Stationsgatan (Pressbyrån) | flat, dark grey | one storey, flat roof at 3.6; ivory render, large windows, glazed door | medium |
| 90977169 | pavilion, Stationsgatan (pizzeria) | flat, dark grey, roof units | one storey, flat roof at 3.8; rose render, large windows, glazed door, two roof units | medium |
| 90965000 | shed at the end of the tracks | small pitched roof, dark brown-grey | one storey, eaves 2.8, ridge 3.9, saddle; falu red boarding | low |
| 92379301 | yard behind Kaggensgatan 38 | **not covered** by any capture | one storey shed, eaves 2.5, ridge 3.8, red tile saddle; falu red boarding | none |
| 92379273 | back range on Kaggensgatan, block Södra Långgatan/Ölandsgatan | dark grey sheet, ridge along the long axis (lit north slope, dark south slope); a ribbed strip at the west end | two storeys, eaves 6.65, ridge 8.7, dark metal saddle with two roof lights; grey-beige render | medium |
| 92379300 | same block, middle | red tile, ridge along the long axis | two storeys, eaves 6.65, ridge 9.5, tile saddle; ochre render | medium |
| 92379268 | same block, east of 92379300 | red tile, ridge along the long axis, hipped ends | two storeys, eaves 6.65, ridge 9.3, tile hip; yellow boarding | medium |
| 92412871 | yard off Västra Sjögatan | grey-brown, mostly in shadow | one storey, eaves 3.1, ridge 5.0, dark tile saddle; falu red boarding | low |
| 92412839 | yard, south of Södra Långgatan | grey-brown roof with a white edge along the yard (south) side | two storeys, mono-pitch falling to the yard (eaves 6.65, high side 7.6), grey sheet; pale grey render | low |
| 92412854 | back range, Södra Långgatan side | red tile with roof lights and chimneys, ridge along the long axis | two storeys, eaves 6.65, ridge 9.6, tile saddle with two roof lights; pale yellow render | medium |
| 93238216 | yard north of Storgatan (behind the town hall) | dark brown-grey, ridge along the long axis; the notch on the south | main range two storeys, eaves 6.4, ridge 8.9, dark tile saddle; the 1.8 m south strip a flat one-storey annex at 3.2; grey-beige render | low |
| 91846989 | Ölandsgatan, behind the garden | red tile, dormers on the south slope; the north-west part lower and in shadow | main range two storeys, eaves 6.65, ridge 9.9, tile saddle with three dormers; white render with a red boarded east gable (panorama); the rear west part a one-storey flat-roofed falu red annex at 3.2 | high (main), low (annex) |
| 91846939 | Ölandsgatan, behind the garden | red tile, ridge along the row, hatches on the south slope | one and a half storeys, eaves 4.4, ridge 8.2, tile saddle with a white gabled wall dormer; sage-green boarding (panorama) | high |
| 91846948 | east end of the same row | red tile continuing the row; north-east wing | one and a half storeys like 91846939: main range eaves 4.4, ridge 7.8; north-east wing eaves 4.4, ridge 7.0; yellow boarding | medium (roof), low (walls) |
| 91846923 | courtyard of the Storgatan/Proviantgatan/Södra Långgatan block | red tile hip, ridge along the long axis, hipped ends clearly visible | two storeys, eaves 6.65, ridge 10.4, tile hip with two chimneys; pale yellow render | high (roof), medium (walls) |

No outline was found empty. Every capture shows a roof where OSM has the building, so no house became a plinth.

## What is estimated

Everything in the table above. In detail:
- **Heights.** Eaves are the district volume's H (6.65 m for two storeys) for the ranges. Sheds are capped at one storey (2.5–3.1 m), and the pavilions take the district one-storey height. The heights of 91846939 and 91846948 (1.5 storeys, eaves 4.4) follow the panorama's proportions, but they are not resected measurements. Ridge heights come from typical pitches: about 35–40° for tile roofs, about 18° for sheet roofs, and a low pitch on the goods shed.
- **Wall materials and colours.** These are not visible from above. They are chosen as typical courtyard buildings (boarded falu red outbuildings, yellow and sage boarding, rendered back ranges), except for 91846989 and 91846939, which come from the panorama.
- **Openings.** Windows, doors and their placement are generic: a bay of about 2.9 m, rows per storey, and the door on the wall that best faces the yard.
- **Fill walls.** Where a house is now lower than its pass-17 volume and a taller neighbour touches it, a plain wall in a neutral render colour (M_Block121_Party) closes the band from the new eaves up to the old height. The neighbour's own party wall may have been built only above the old height. This happens at 91846989's annex (against 91846934) and at 91846948 (against 91846953 and 91846979).

## Verification

- **Zones** (`previews/block121-zones.json`): footprint 2090.8 m², zoned 2090.7 m², outside OSM 0.04 m², OSM not zoned 0.15 m², overlap 0.002 m²; status passed.
- **Sandbox, iteration 1** (prelude pass 119): SANDBOX_DONE without errors, 16 meshes. `drop_degenerate_faces121` removed 0–32 degenerate faces per mesh (the hidden gable and roof slivers).
  - The top-down renders were set beside the satellite captures.
  - The panorama view 651 was set beside its photo. 91846939's eaves and ridge, its wall dormer and colour, and 91846989's white walls, three dormers and tile roof sit where the photo has them.
- **Iteration 2:**
  - the goods shed's paler south-east roof section;
  - a lighter grey-brown on the shed roof;
  - 91846989's red boarded east gable and end wall, seen in the panorama.
- **Iteration 2 results:** SANDBOX_DONE without errors (prelude 119, 16 meshes). In the view 651 comparison the red east gable now sits where the photo has it.
- **Export frame check:** run in iteration 2 with `SCR/p121/build_block121_check.py`, the pass 119 wrapper adapted to pass 121, after the export tail's preparation, on all 16 meshes. Every mesh had 0 invalid tangent frames (CHECK121_TOTAL_INVALID 0), and 16 of 16 test FBX exports succeeded.
- **Repeatability:** not tested. The build deletes and recreates its 16 objects and its materials, and it has no detail_pass guard, so a second run should rebuild the same meshes. The sandbox ran it only once per iteration.
- **Pending:** the official build and the Unreal checks; the lead fills in the build results.

## Limitations

- **Satellite reading.** All roof readings come from a single satellite epoch at about 0.3 m/px. Shadows hide parts of 92412871, 92412839 and 93238216, and their roof form is a guess.
- **No satellite view.** 92379301 (14 m², behind Kaggensgatan 38) is not in any capture. It is a generic red shed.
- **Heights.** No height in this pass is measured.
- **Simplified roofs.**
  - L-shaped outlines are simplified to a main range plus a flat or saddle-roofed part.
  - Roofs are fitted to the outline's minimum rotated rectangle, so they overhang slightly where the outline is not quite rectangular (92412839, 92412854).
- **Fill walls.** These are neutral render, not the neighbour's own facade.

## Extra views that would help

- A top-down satellite capture centred on (−152, 178) (92379301).
- An oblique aerial or a view into the yard off Västra Sjögatan 4 (about (5, −108), looking north-east), for 92412871 and 92412839.

## Official build

The lead's build of pass 121 passed the Blender geometry checks and the FBX export, and two rebuilds gave identical meshes. Passes 28–120 are unchanged except the earlier intended changes. The Unreal import and its checks are deferred.
