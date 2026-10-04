# Pass 108: Kaggensgatan

Pass 108 replaces five generic district volumes from pass 17 on Kaggensgatan with detailed houses. Kaggensgatan runs south–north here at x ≈ −185. The houses on its west side (x ≈ −191/−192) face east, and the houses on its east side (x ≈ −179/−181) face west. The south part of the street, near Storgatan, is pedestrian, and there is no Google car imagery of it. Two of the five houses therefore rest on contributor 360 photos only.

- **92204167 (west side, just north of Storgatan): the brown brick shop house (Klintheims Skor).**
  - The task notes called it four storeys. The photo shows three: a shop floor and two window rows, with a low dark box on the flat roof.
  - The yellow three-storey house to its left in the photo is the corner house 92204203 (Storgatan pass), not this one. Scaled at the same distance, the yellow front measures about 10.8 m, which matches 92204203's 11.0 m OSM front. The brick front measures about 16.3 m, not the 24.8 m OSM front.
  - The outline is therefore split at y 30.9. The brick zone (s 0–16.3 from the south joint) has these parts:
    - glazed shopfronts between four brick-brown piers, with the glazed entrance doors in the middle shop;
    - a white fascia sign (no lettering);
    - two rows of nine dark-framed windows, one at 6.00–7.55 m and one at 9.15–10.70 m, at a 1.75 m pitch;
    - a metal coping at 11.5 m, a flat roof and a dark roof box (6.5 × 4 m, 1.1 m high).
  - The northern 8.5 m (a lighter facade, only glimpsed at the photo's right edge) is plain beige render with three window levels and a hipped tile roof. Its eaves (10.5 m) and ridge (12.3 m) are estimated.
- **92379295 (SM_Building_92379295, the south-east corner of Storgatan and Kaggensgatan): salmon render on a grey stone base.** This mesh was built by the Storgatan extension pass (the 'bank' profile). The pass 108 build replaces the whole object.
  - The photographed stretch of the Kaggensgatan front is about 12 m. It has these parts:
    - two arched shop windows (2.7 m wide, glass to 3.75 m), with navy fascia bands and cream arched surrounds;
    - between them, a door in a cream surround;
    - cream pilasters on either side;
    - a red arched gate to the south.
  - Over the whole front: a cream string course at 4.8 m and upper windows in cream surrounds on two floors (5.7 and 9.3 m) at a 2.95 m pitch. The upper windows were measured over the seen stretch and carried along the front.
  - The rest of the ground floor, and the whole Storgatan front, are plain rectangular windows in the same materials.
  - The eaves stay at the district value of 13.3 m. The roof is a red tile mansard (rise 2.5 m, 3 m inset, flat top), estimated.
- **92379291 (38 Kaggensgatan, corner of Strömgatan): cream render on a grey plinth.**
  - Ground floor: eight windows with white awnings, the red door up two steps, and the red arched carriage gate with a glazed fanlight. It has horizontal grooves.
  - Nine first-floor windows in white surrounds.
  - A red-brown line on the string course (4.1 m) and on the cornice (7.9 m), and downpipes.
  - Two curved gables (s 3.7–12.1 and 16.1–23.8) standing on the cornice, up to 11.1 and 11.45 m, with three and two pairs of narrow arched windows.
  - A red brick mansard (top 11.0 m) with four arched dormers: at the north end, between the gables, and two at the south end.
  - The Strömgatan wing (OSM x −168.9 to −153.6) is not seen. It has plain cream walls and the same mansard.
- **92204171 (west side, 40 Kaggensgatan area): the modern white four-storey frame house.** The task notes suggested the beige house in the photo was 92204171. The resection shows otherwise:
  - The beige three-storey house with the dormered roof, left of the bar gate, is **92204191**. That house was built in pass 105 as a small green house seen obliquely, and this pass does not touch it. The photo shows it as beige render with a brick-red roof and a dormer, so it could be revisited.
  - The gate fills the 4.7 m OSM gap (y 231.6–236.3). The white frame house is 92204171.
  - Its frame covers s 0.3–9.4 from the south corner.
  - Only the garage storey runs on to the north corner at s 11.5, so the outline is split at y 245.66.
  - Frame block features:
    - a ground floor set back 0.3 m, with a dark wall, black garage doors and the red band at 1.7–2.1 m;
    - white slab edges at 3.1, 5.9, 8.6 and 11.3 m, 1.7 m deep, with glazed balustrades;
    - the dark recessed wall 1.0–1.35 m behind the facade line, with large glazed openings;
    - white side columns and a roof frame at 12.9 m.
  - The garage storey north of it is 3.1 m high. The rear part beyond x −207.45 is not seen and is kept at 6.65 m, plain grey render, with a flat roof.
- **92379305 (40c Kaggensgatan, corner of Strömgatan): the 1960s three-storey office.**
  - A 1.2 m window module (42 modules over 50.3 m) between projecting concrete fins.
  - Dark spandrel panels, and window rows at 4.05–5.50 and 7.00–8.40 m.
  - Shopfronts between piers every four modules (4.79 m), a dark fascia, and a blue awning strip at 3.0–3.25 m.
  - A blue awning box over the top windows, a metal fascia to 9.7 m, and a flat roof.
  - One glazed entrance at s 27.6.
  - The Strömgatan front (33.4 m) gets the same treatment, but it is not seen.

## Measurement

The local frame and the tools are the project's standard ones: `SCR/p100/res.py`, `SCR/p82/hit.py` and `meas.py` with vfov 90 at 756 × 405. The facade plane used is the OSM line offset 0.355 m outward.

| Photo | Pano (Google position) | Resected / assumed camera (x, y, h) | Method | Measured |
|---|---|---|---|---|
| 92379291_h64 (38 Kaggensgatan, Google) | vUSLijmb… (−186.03, 190.85) | (−187.10, 190.47, 2.40) | Distance from the pavement line at the image centre (v 332 → 7.5 m at h 2.4). Position along the street from the south corner pipe (u 728, v 200) set to the OSM corner y 175.84. Door height check: about 2.2 m. | Cornice 7.9; string course 4.06; first-floor windows 4.54–6.61; ground openings to 3.27; gate 3.0 wide, spring 2.71, crown 3.29; plinth 0.6; gables s 3.7–12.1 / 16.1–23.8, shoulders about 10.3–10.6, tops 11.1 / 11.45; gable windows 8.2–9.8; first-floor axes s 2.15, 4.80, 7.74, 10.87, 13.84, 17.75, 21.62, 24.96, 28.34; joint pipe s 15.2 |
| 92204171_h241 and 92379305_h61 (same pano, Google) | 4whHB613… (−184.03, 237.75) | (−184.60, 236.50, 2.40) | A two-corner resection on the frame edges gave x −182.5, which contradicts the ground lines. The ground lines in both views give distances of 6.5 m (west) and 5.2 m (east) for h 2.36–2.4, which sum to the 11.6 m street width. y is set so that the bar gate spans the OSM gap 231.6–236.3 (it measures 4.2 m). | West: frame s 0.54–9.23; slabs 3.16, 5.65 (likely 5.9), 8.51, 11.3; top 12.9; red band 1.68–2.07. East: shop top 3.03; awning 3.2; windows 4.05–5.50 and 7.01–8.39; awning 8.8; roof edge 9.5–9.7; piers at y 244.3, 239.4, 234.5, 229.8 (4.8 m) |
| 92204167_h243 (USERPHOTO) | contributor 360, position and heading unreliable | approx. (−184.3, 17.3, 1.55) | No resection. The scale comes from the yellow neighbour's 11 m OSM front and a 3.05 m storey pitch (about 24.6 px/m at the facade). | Brick front about 16.3 m; shop top 4.0; window rows 6.0–7.6 and 9.15–10.7; parapet 11.5; nine windows per row, about 1.2 m wide |
| 92379295_h62 (USERPHOTO) | contributor 360, position and heading unreliable | approx. (−184.8, −28.7, 1.54) | Scaled from the door: an opening of 2.3 m gives a distance of 3.24 m and a camera height of 1.54 m. The position along the front is the pano's nominal one (door at s 20.6) and is not known. | Ground floor to the string course 4.8; arched windows 2.7 × (2.25 + 0.95 arch), sill 0.55; door 1.0 × 2.3; stone base 0.45; upper-window pitch 2.95; upper sills about 5.7 |

## Estimated

- **92204167.** The joint at y 30.9 has an uncertainty of about ±1.5 m. The northern part (style, eaves 10.5 m, hipped roof) is estimated. The positions of the piers and windows carry about ±0.8 m.
- **92379295.**
  - The placement of the photographed stretch along the 36 m front is unknown (±5 m).
  - The rest of the Kaggensgatan front, the Storgatan front, the upper-floor height of 9.3 m and the eaves (13.3 m, kept from the district value) are estimated. So is the mansard.
  - The Storgatan pass's arched 'bank' front and pediments on Storgatan are replaced by plain windows. The Storgatan front was not photographed in this pass.
- **92379291.**
  - The roof above the mansard and the gables is not seen. Its flat top at 11.0 m is estimated.
  - The ground window at s 1.6 (only partly in view) is estimated, as are the dormer sizes.
  - The concave gable shoulders are modelled as convex quarter-ellipses.
  - The Strömgatan wing is estimated.
- **92204171.** The window layout of the recessed wall, the slab depth (1.7 m), the depth of the frame block and the whole rear part are estimated.
- **92379305.** The north part of the front (y > 248) and the whole Strömgatan front are not seen. The office treatment is carried over them. The door position is approximate.
- **All houses.** Colours are judged by eye from the photos.

## Verification

- `KALMAR_GEO=SCR/pylib python3 scripts/prepare_block108.py` prints `BLOCK108_ZONES_OK`:
  - footprint 3903.7 m², zoned 3903.6 m²;
  - outside OSM 0.01 m², OSM not zoned 0.08 m², overlap 0.0 m².
- Sandbox (prelude: rebuild chain 107) ran twice and printed `SANDBOX_DONE` with no errors.
  - `BLOCK108_GEOMETRY 5`.
  - `drop_degenerate_faces108` (with the `_thin` test) removed 2 / 57 / 311 / 4 / 2 faces from 92204167 / 92379295 / 92379291 / 92204171 / 92379305. These are zero-length rod segments at repeated arc points and coincident caps; no visible part went missing in the renders.
- Renders at the photos' own size, with the cameras above, were compared side by side with the photos (`SCR/p108/cmp1_v*.jpg`):
  - **38 Kaggensgatan:** the cornice, string course, window axes, gate, gables and mansard dormers line up within about 0.3 m. The model's gables are rounder than the real concave-shouldered ones.
  - **40c:** the module, the pier rhythm, the two window rows, the blue strips and the roof edge agree.
  - **White frame house:** the frame position, slab levels and garage band agree. The real frame's top storey is cut off in both.
  - **The two contributor photos:** proportions, storey count and opening rhythm agree. Positions cannot be checked.
  - Close aerials (`SCR/p108/sb2/aN.png`, `aS.png`) show the roofs closing correctly.
- The official build, the export check and the Unreal checks are pending; the lead fills in the build results.

## Limitations

- **Contributor photos.** Two houses rest on contributor 360 photos whose positions and headings are unreliable. Their scale comes from door and storey heights, and the lead camera `535_Block108_Cal_Brick` is approximate.
- **92204167 split.** The split of 92204167 at y 30.9 is a judgement from a scaled photo. A Google or contributor view from further north on the pedestrian street would settle it.
- **Neighbours seen in the photos.** In the photos, the yellow corner house 92204203 shows a three-storey front on Kaggensgatan. The model currently has a blank beige wall there (Storgatan pass). The beige house 92204191 differs from its pass 105 model. Neither is changed here.
- **Omitted.** Shop lettering, lamps, the flag pole, the cars and the slender posts in front of the white frame house are omitted.

## Official build

The lead's build of pass 108 passed the Blender geometry checks and the FBX export, and two rebuilds gave identical meshes. Passes 28–107 are unchanged except the earlier intended changes (pass 85's prison building, corrected by pass 103, and pass 98's three meshes re-created by pass 107). The Unreal import and its checks are deferred.
