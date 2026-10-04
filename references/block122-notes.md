# Pass 122: courtyard houses, back ranges and outbuildings in the east half of Kvarnholmen, and Klapphuset

Pass 122 replaces twenty-five generic pass-17 volumes that stand inside the blocks or behind the street fronts in the east half of Kvarnholmen (x > 150), between Proviantgatan and Östra Vallgatan and on Fiskaregatan. Most of them were rendered two-storey blocks with hipped roofs. It also rebuilds Klapphuset (93199604), the small boarded house standing in the water off Bastion Carolus Philippus. These buildings cannot be seen from the streets, so the pass works from top-down satellite views. **Everything in this pass is estimated.** Nothing is measured from a resected photo.

Each house keeps its mesh name and OSM outline and gets a plausible form:

- the roof form, ridge direction and roof colour read from the satellite view;
- storeys from the district volume, capped at one storey for small sheds;
- the ridge height from the boxed width and a typical pitch: about 38° for red tile, 30–32° for the tan tile and the large hips, and 22° for sheet metal;
- boarded walls (falu red, yellow, ochre) or render, matched to typical courtyard buildings;
- windows per storey, one door on the side facing the yard, a stone plinth, an eaves board, and corner boards on boarded walls;
- roof lights and chimneys on some ranges.

Five outlines are split:
- **93192407** (an L) into the north range and the south-east wing, each with its own saddle;
- **93238177** into the main range and a small flat-roofed bay on the north;
- **93238180** into two flat-roofed shed parts;
- **93238174**, a stepped strip, into a saddle-roofed middle, flat-roofed ends and a flat one-storey bay on the west;
- **93238152** into a grey-roofed east wing, a red-tiled south wing and a flat one-storey link between them.

**Klapphuset** keeps the pass-17 build's photo-based form: an eaves height of 2.95 m, a low hip (ridge 4.2 m) with two ventilators, falu red boarding and high multipane windows. The pass adds:
- lap boarding;
- a floor and a timber beam over the water;
- round piles under the house;
- the pier to the shore, placed from the satellite view: from the middle of the south side at (436.4, 122.3) to (426.8, 104.3), 2.2 m wide. Pass 17 had it from the west end of the south side;
- the deck on the east end (1.6 m with a railing), which the satellite shows as a pale strip;
- a grey roof, as the satellite shows it.

Google imagery is a working reference only. No pixel is used as a texture; materials are flat colours on the town textures.

## Measurement

**Nothing is measured.** No panorama was resected, and no camera table applies.
- **Street View.** The only captures that point at one of these houses are 91926324_h332 and 91926325_h332 (43 Storgatan, pass 111). They see 91926312 at 28 m behind the street houses, but it is not identifiable in them. They were not used.
- **Satellite captures.** The pass uses six top-down Google satellite captures, north up, 728 × 419 px (pass 122 lines in `captures.txt`):

| Capture | Centre (local) | Covers |
|---|---|---|
| sat_e1 | (215, 0) | 91926312, 93192396, 93192383, 93192368, 93192379, 91928592, 91928555, 91928547 |
| sat_e2 | (240, −38) | 91928595, 91928593 |
| sat_e3 | (270, 35) | 93192407, 93192355, 93192451, 93192363, 93192371, 93192450, 90859854 (partly under the search box) |
| sat_e4 | (350, 30) | 93238177, 93238180, 93238174, 93238167, 93238219, 93238152, 90859839 (at the edge) |
| sat_e6 | (436, 123) | 93199604 Klapphuset with its pier |
| sat_e7 | (341, −50) | 93199612 |

**Registration.** The pass reuses the pass-121 similarity transform: the 28.2° rotation, the URL centre, 0.307 m/px (from two street crossings 71.5 m apart in the road data) and a −5 px shift in x. It was checked by overlaying all district outlines and the road centrelines on every capture (`SCR/p122/ov_e*.png`, `pr_g*.png`).
- **Fit.** The street centrelines run down the middle of Proviantgatan, Storgatan, Landshövdingegatan and Norra Långgatan, and the outline corners sit on their roofs within about 1–2 m.
- **Klapphuset.** Its outline matches the south and west roof edges. The dark band north of the roof is the house's shadow on the water, not roof.
- **Limits.** This is enough to tell which roof belongs to which outline. It is not a measurement.

## Satellite reading and chosen form

Confidence: **medium** when the roof form and colour are clear; **low** when the roof is in shadow, partly hidden or ambiguous. Walls are never visible from above. Heights are eaves and ridge in metres above the ground.

| Id | Where | Roof read from satellite | Chosen form | Confidence |
|---|---|---|---|---|
| 91926312 | yard by the parking lot east of Proviantgatan | small pale tan pitched roof, ridge along the long axis | one-storey shed, eaves 2.9, ridge 4.2; tan tile saddle; yellow boarding | low |
| 93192396 | back range, Proviantgatan/Storgatan block | red tile, ridge along the long axis, pale strip on the south eaves | two storeys, eaves 6.65, ridge 8.8; tile saddle; ochre render | medium |
| 93192383 | yard link between 93192396 and 93192379 | flat, pale grey | one storey, flat roof at 3.55; pale grey render | medium |
| 93192368 | yard range, Storgatan side | red tile, ridge along the long axis, chimney | two storeys, eaves 6.65, ridge 9.05; tile saddle with chimney; pale yellow render | medium |
| 93192379 | yard range, Norra Långgatan side | dark grey, part of a larger dark roof | two storeys, eaves 6.65, ridge 8.3; dark sheet saddle; grey-beige render | medium (roof), low (walls) |
| 93192407 | L-shaped back range behind Storgatan | red tile; ridge along the north range and along the south-east wing; a roof light | two storeys; north range ridge 9.2 with a roof light, wing ridge 9.6; tile saddles; yellow render | medium |
| 93192355 | yard house, Storgatan side | red-orange tile, ridge along the long axis | one storey, eaves 3.55, ridge 5.6; tile saddle; yellow boarding | medium |
| 93192451 | yard house, Norra Långgatan side | deep red tile, continuing a longer red roof | one storey, eaves 3.55, ridge 5.6; tile saddle; falu red boarding | medium (roof), low (walls) |
| 93192363 | yard house between 93192451 and 93192371 | tan/light brown, ridge along the long axis | one storey, eaves 3.55, ridge 5.3; tan tile saddle; ochre boarding | low |
| 93192371 | yard house towards Landshövdingegatan | tan-orange tile, ridge along the long axis | one storey, eaves 3.55, ridge 5.2; tan tile saddle; yellow boarding | medium (roof), low (walls) |
| 93192450 | back range, Landshövdingegatan | tan-orange tile with a roof light, ridge along the long axis | two storeys, eaves 6.65, ridge 8.4; tan tile saddle with a roof light; pale yellow render | medium |
| 90859854 | Fiskaregatan | red-brown; mostly under the search box in sat_e3 | one storey, eaves 3.55, ridge 5.2; brown tile saddle; falu red boarding | low |
| 90859839 | Fiskaregatan/Landshövdingegatan | blue-grey sheet, ridge along the long axis (sat_e4 edge) | two storeys, eaves 6.65, ridge 7.8; grey sheet saddle; rose render | low |
| 91928592 | yard south of Storgatan, by Södra Långgatan | dark grey, narrow | one-storey shed, eaves 3.0, ridge 3.75; dark sheet saddle; falu red boarding | low |
| 91928555 | yard range, Storgatan/Södra Långgatan block | dull brown-red tile, hipped ends | two storeys, eaves 6.65, ridge 8.9; brown tile hip; ivory render | medium (roof), low (walls) |
| 91928547 | free-standing house in the same yard, garden to the south | grey-brown, nearly square, hipped | two storeys, eaves 6.65, ridge 9.7; grey-brown sheet hip with chimney; yellow render | medium |
| 91928595 | yard range, Storgatan/Landshövdingegatan block | pale beige-grey, flat with small dark squares | two storeys, flat roof at 6.65; ivory render | low |
| 91928593 | yard range north of 91928595 | light brown tile, uniform, pale strip on the south edge | two storeys, eaves 6.65, ridge 8.9; tan tile saddle along the long axis; ochre render | low |
| 93238177 | yard range off Norra Långgatan, east block | pale orange tile, ridge along the long axis; a small bay to the north | two storeys, eaves 6.65, ridge 9.05; tan tile saddle; yellow render. The north bay is one storey and flat at 3.2 | medium |
| 93238180 | yard shed south of 93238177 | dark grey (beside a larger dark roof) | one-storey sheds, flat at 3.0 and 2.7; falu red boarding | low |
| 93238174 | narrow stepped back range | red-brown tile in the middle; flat pale parts (terraces) at the ends | two storeys; middle tile saddle, ridge 8.7; ends flat at 6.65; west bay flat at 3.2; rose render | low |
| 93238167 | narrow shed south of Norra Långgatan | dark, in shadow | one-storey shed, eaves 3.0, ridge 3.6; dark sheet saddle; falu red boarding | low |
| 93238219 | long back range from Norra Långgatan | red-brown tile, ridge along the long axis, chimneys | two storeys, eaves 6.65, ridge 8.65; brown tile saddle with two chimneys; pale yellow render | medium |
| 93238152 | L-shaped yard complex towards Östra Vallgatan | grey in the east wing and the link; salmon-red tile in the south wing | east wing two storeys, grey sheet saddle, ridge 7.4; south wing two storeys, tile saddle, ridge 9.1; the link one storey and flat at 3.4; grey-beige and yellow render | low |
| 93199612 | yard house, Storgatan/Södra Långgatan, east block | salmon-red tile, hipped, vents and chimneys | two storeys, eaves 6.65, ridge 10.1; tile hip with two chimneys; yellow render | medium |
| 93199604 | Klapphuset, in the water off Bastion Carolus Philippus | grey low hip with two ventilators; pale pier from the middle of the south side to the shore; pale deck strip on the east end | one storey on piles, eaves 2.95, ridge 4.2 (pass-17 values); lap-boarded falu red, high windows, door at the pier; pier 20 m × 2.2 m; east deck 1.6 m | medium (form and pier), low (walls, from pass 17) |

No outline was found empty. Every capture shows a roof where OSM has the building, so no house became a plinth.

## What is estimated

Everything in the table above. In detail:
- **Heights.** Eaves are the district volume's H: 6.65 m for two storeys and 3.55 m for one. Sheds are capped at 2.7–3.0 m. Ridges come from the pitches above.
- **Wall materials and colours.** These are not visible from above. They are chosen as typical courtyard buildings, with the district volume's colour kept where it was plausible.
- **Openings.** Windows and doors are generic:
  - a bay of about 2.9 m (4 m on sheds and Klapphuset), with rows per storey;
  - the door on the wall that best faces the yard;
  - on Klapphuset, the door is at the pier.
- **Fill walls.** Where a house is now lower than its pass-17 volume and a taller neighbour touches it, a plain wall in a neutral render colour closes the band from the new eaves up to the old height. This happens at 91928592, 93238167 and the 93238152 link.
- **Klapphuset.**
  - The floor is at z = 0, 1.33 m above the model's water plane (z = −1.33).
  - Piles reach down to −2.3.
  - The pier ends on the shore terrain, which it meets in the sandbox render.

## Verification

- **Zones** (`previews/block122-zones.json`): footprint 2157.8 m², zoned 2157.7 m², outside OSM 0.08 m², OSM not zoned 0.19 m², overlap 0.0 m²; status passed.
- **Sandbox, iteration 1** (prelude pass 120): SANDBOX_DONE, no errors, 26 meshes. `drop_degenerate_faces122` removed 0–40 degenerate faces per mesh (hidden gable and roof slivers, collapsed corners).
  - North-up top-down renders at the capture scale were set beside the captures (`SCR/p122/z_sb*_e*.png`). The roofs fall on the same outlines, and the roof colours and ridge directions agree with the reading above.
  - Klapphuset, its pier and the east deck fall on the satellite pixels (`z_sb*_e6.png`).
  - Seven oblique views were checked by eye (`SCR/p122/sheet_sb*.png`).
- **Iteration 2** (SANDBOX_DONE, no errors):
  - a lighter brown tile on 93238219 and 91928555, closer to the satellite;
  - a grey roof on Klapphuset;
  - a weathered grey pier and deck instead of brown, as on the satellite view.
- **Export frame check** (`SCR/p122/build_block122_check.py`, the pass-119 wrapper adapted, run on the copy after the export tail's preparation, together with the sandbox): 0 invalid tangent frames, and 26 of 26 meshes exported to FBX in both iterations. `drop_degenerate_faces122` with the `_thin` test runs on every mesh.
- **Pending:** the official build and the Unreal checks; the lead fills in the build results.

## Limitations

- **Satellite reading.**
  - All roof readings come from one satellite epoch at about 0.3 m/px.
  - 90859854 is mostly under the search box in sat_e3, and 90859839 sits at the edge of sat_e4.
  - Shadows hide 93238167 and 93238180.
  - The pale flat parts of 93238174 may be terraces rather than roofs.
- **Heights.** No height in this pass is measured.
- **Simplified roofs.**
  - Roofs are fitted to each zone's minimum rotated rectangle, so they overhang slightly where the outline is not quite rectangular (93238219, the 93238152 wings, the middle of 93238174).
  - The stepped and L-shaped outlines are simplified to saddle parts plus flat parts.
- **Fill walls.** These are neutral render, not the neighbour's own facade.
- **Klapphuset's walls.** These follow pass 17's photo description; no photo was used in this pass.

## Extra views that would help

- A satellite capture centred on (262, 108), without the search box over 90859854 and 90859839.
- An oblique aerial over the east block from the south-west, about (320, −10, 45 m), looking north-north-east, to confirm the stepped 93238174 and the 93238152 complex.
- A shore photo of Klapphuset from Bastion Carolus Philippus, about (420, 100), heading about 15°, to confirm the walls and the pier.

## Official build

The lead's build of pass 122 passed the Blender geometry checks and the FBX export, and two rebuilds gave identical meshes. Passes 28–121 are unchanged except the earlier intended changes. Klapphuset (93199604) had a pass-17 build at detail_pass 17 and is re-created here. The Unreal import and its checks are deferred.
