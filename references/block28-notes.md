# The Larmgatan–Kaggensgatan block — pass 28

Research date: 2026-09-23.

The pass replaces the last five generic district volumes of the block bounded by Larmgatan, Södra Långgatan, Kaggensgatan and Ölandsgatan:
- **Södra Långgatan 8** (OSM way 91856615)
- **Södra Långgatan 10** (91856624), the yellow range dated 1881 on its gate piers. A rusticated quoin strip divides it into the gate house with the risalit and the corner house on Kaggensgatan.
- **Kaggensgatan 5** (91856594), the green house, with its courtyard wings
- the **courtyard house** 91856619
- **Ölandsgatan** (91856622), split into three houses: the rough-cast merchant house (Ölandsgatan 5), the lower house with the carriage gate, and the three-storey corner house on Kaggensgatan (Kaggensgatan 3).

The pass also corrects the pass 26 houses on Larmgatan, whose close-range heights proved wrong (see *Correction of pass 26*).

Panoramas and photospheres are working references only. No pixel is used as a texture, and no panorama, depth or tile data was extracted.

## Sources

- **OpenStreetMap** (`source/kvarnholmen.json`) supplies the five outlines.
- **Overpass query of 2026-09-23** for address and shop nodes. These give the house numbers used above: Södra Långgatan 8 and 10; Kaggensgatan 3, 5 A–E and 7; Ölandsgatan 5.
- **Google Street View**, official imagery of April 2025, viewed in the browser. Each position is the panorama a review camera replicates; the resected positions are given under *Measurement*.

| Panorama (reported position) | Camera | Used for |
|---|---|---|
| 56.6625147 N, 16.3626175 E, Södra Långgatan | 151 (heading 152°) | Södra Långgatan 8 straight on; the calibration view and the resection |
| 56.6625576 N, 16.3627644 E, Södra Långgatan | — | the joint between numbers 8 and 10; the west bays of number 10 |
| 56.6626415 N, 16.3630602 E, Södra Långgatan | 152 (heading 152°) | the risalit, the gate and the pediment of number 10; a calibration view |
| 56.6626813 N, 16.3632009 E, Södra Långgatan | — | the east bays and the quoin strip between the two yellow houses |
| 56.6627666 N, 16.3634847 E, Kaggensgatan corner | 153 (heading 194°) | the chamfered corner, its attic and the Kaggensgatan front |
| 56.6624715 N, 16.3624667 E, Södra Långgatan | 161 (heading 152°) | the west section of number 8, Larmgatan 10 and its oriel; a calibration view |
| 56.6620001 N, 16.3633510 E, Ölandsgatan | 156 (heading 332°) | the merchant house; a calibration view |
| 56.6620824 N, 16.3636418 E, Ölandsgatan | 157 (heading 332°) | the gate house and the corner house; a calibration view |
| 56.6621732 N, 16.3639532 E, Kaggensgatan/Ölandsgatan | — | the corner house's Kaggensgatan front |
| 56.6618722 N, 16.3629063 E, Ölandsgatan | — | Larmgatan 6 on Ölandsgatan (pass 26 check) |
| 56.6620328 N, 16.3622273 E, Larmgatan | 160 (heading 62°) | Larmgatan 8 (pass 26 check, a calibration view) |
| 56.6616055 N, 16.3626337 E, Larmgatan | 159 (heading 62°) | the Odd Fellows house (pass 26 check, a calibration view) |

- **Two contributed photospheres on Kaggensgatan**, which has no official coverage. One is a visitor's (June 2020), showing the north half of Kaggensgatan 5. The other is the café's own (August 2025), showing its south half.
- **Satellite imagery**, viewed only for roof colours: Airbus / Maxar, 2026.

## Measurement

This pass found that the method used for passes 24 and 26 measures itself. It inverted the Street View camera assuming a 2.5 m camera height at the reported panorama position, and checked the scale only against the pavement. The flaw showed when three panoramas of Södra Långgatan 8 disagreed with each other by 3–7 m, and the measured length of the front exceeded OSM's 24.15 m by a quarter.

The method is now anchored to independent references.

1. **Field of view.** The same features were taken at headings 20° apart: a Maps marker and a door jamb. They land on the pixels predicted by a pinhole camera with the URL's `90y` as the vertical field of view, to within 1 px. Screenshots come at 1568 × 784 or 1500 × 750 pixels, so the reported size is used each time.
2. **Resection.** Two building joints known from OSM subtend a measured angle; for Södra Långgatan 8 that is 129.9°. From that angle the camera's distance to the facade is solved: 5.56–5.63 m, where the reported position implies 7.53 m. The reported panorama positions proved to be off by 1.5–3 m, both across and along the street.
3. **Camera height.** In a level view the facade point on the horizon row lies at camera height. The April 2025 imagery comes from the roof-mounted camera, 2.0–2.2 m above the facade base (2.21 m on Södra Långgatan, 2.0–2.1 m on Larmgatan), not the 2.5 m of the former mast.
4. **Heights.** Along one image column the facade points share their depth. A height is therefore the camera height times (base row − row) / (base row − horizon row). This needs neither the reported position nor the distance.
5. **Transfer between panoramas.** The resected heights of Södra Långgatan 8 anchor the other panoramas that show it: a linear fit of naive to true heights leaves residuals of at most 0.25 m. The fitted scale then corrects the horizontal positions too.

Cross-checks:
- The same windows measured at two pitches agree within 0.05 m.
- Södra Långgatan 10 gives the same cornice from three panoramas within 0.2 m.
- The measured bays and joints add up to the OSM lengths: Södra Långgatan 8 24.15 m, Södra Långgatan 10 42.83 m, and the Ölandsgatan front 52.0 m.

| Feature | Measured on the facade plane (m) | Modelled (m) |
|---|---|---|
| Södra Långgatan 8 cornice top | 8.2 | 7.8 |
| Södra Långgatan 8 pediment apex | 10.9 | 10.5 |
| Södra Långgatan 8 first-floor windows | 4.9–6.7 | 4.9–6.7 |
| Södra Långgatan 10 cornice top | 9.3 | 8.85 |
| Södra Långgatan 10 risalit pediment | 10.6 | 10.1 |
| Södra Långgatan 10 upper windows | 4.5–6.6 | 4.5–6.6 |
| Södra Långgatan 10 ground-floor arches | about 3.0 | 3.0 |
| Kaggensgatan 5 eaves | 7.8 | 7.45 |
| Ölandsgatan 5 eaves, loft hatches | 8.6, 6.8 | 8.6, 6.8 |
| Gate house on Ölandsgatan eaves | 8.1 | 8.1 |
| Corner house (Kaggensgatan 3) eaves | 10.4 | 9.8 |
| Corner house windows | 0.3–1.9, 2.8–4.7, 6.7–8.5 | the same |

**Projecting cornices.** A cornice seen from below shows its front edge. That edge's viewing ray meets the facade plane higher than the cornice really stands, so plane intersections overstate projecting cornices. A modelled cornice, which projects as well, must therefore be set lower by its own projection times the tangent of the viewing angle.

The calibration views confirmed this. The first review renders put the cornices and pediments of Södra Långgatan 8 and 10 16–22 px high, while the windows lay within 4 px. After lowering them by 0.35–0.5 m, they lie within 2–7 px. The Ölandsgatan eaves boards barely project and matched unchanged.

The flat features are unaffected: windows, bands, hatches and the frieze.

Kaggensgatan 5 was measured against the adjacent yellow house's known windows and cornice, since the photospheres' camera positions are unknown.

Estimates:
- the roof pitches and tops
- the courtyard fronts
- the courtyard wings (7.0 m and 6.4 m) and the courtyard house (6.4 m)
- the corner attic, about 2.5 m above the cornice.

## Correction of pass 26

The same anchored method re-measured the Larmgatan houses of pass 26:

| House | Pass 26 | Re-measured |
|---|---|---|
| Larmgatan 10 cornice | 10.6 (estimate) | 11.4 on the facade plane, modelled at 10.75 under its deep cornice |
| Larmgatan 8 main cornice | 11.3 | 9.9 on the facade plane, modelled at 9.6; a flush attic storey of arched lights to 12.2, and the oriel continuing as a small tower with a bell cap and finial (about 15.5 on the plane) |
| Larmgatan 6 eaves (on Ölandsgatan) | 10.0 | 10.7 on the facade plane, modelled at 10.5 |
| Odd Fellows house | parapet 11.2 (estimate) | rounded corner bays capped at 12.2 under low copper domes; only the central block rises. Its lettered frieze sits at 13.2–14.2 and its deep cornice at 15.3, whose silhouette falls on the measured 16.3 m plane height |

The bank was confirmed: its distant plaza calibration view agrees in angular width and height within 3 %.

The Odd Fellows house also had the wrong form. Its turrets rose above the parapet, but the real corner bays are lower than the central block. Its street front now has three bays of paired windows, with the balcony on the second floor over the portal, which lies 2.2 m north of the centre.

The likely causes of the pass 26 errors:
- The old measuring script hard-coded a 1500 × 750 screenshot, while pass 26's notes and camera helper record a 1512 × 812 viewport. If those screenshots were measured with it, the centre row was off by 31 px. This was not re-run to confirm.
- The reported panorama positions and the 2.5 m camera height were used unchecked.
- Larmgatan 10 and the Odd Fellows house were estimated from storey counts, not measured.

Larmgatan 10 also gains its rectangular oriel on Södra Långgatan, over the first floor, which pass 26 had left out.

## Correction of pass 24

The station house of pass 24 was measured with the same unanchored method, and the same check was applied to it. Both of its panoramas were resected against the 1910 block's corner at the step and the round tower's silhouette.

| Panorama | Reported position off by | Distance to the 1910 front |
|---|---|---|
| 56.6618287 N, 16.3603163 E | (−0.25, −1.10) m | 26.0 m |
| 56.661716 N, 16.3606067 E | (0.10, −1.45) m | 19.7 m |

The facade bases then come out at z = 0 with a camera height of 2.22 m. The two panoramas agree within 0.1–0.25 m:

| Feature | Pass 24 | Re-measured (plane) | Modelled |
|---|---|---|---|
| 1910 ground-floor arch tops | 4.10 | 3.7–3.8 | 3.82 |
| 1910 first-floor windows | 5.75–7.96 | 5.2–7.4 | 5.36–7.41 |
| 1910 second-floor windows | 9.60–11.66 | 8.9–10.9 | 8.95–10.87 |
| 1910 cornice | 13.0 | 12.2–12.4 | 12.15 |
| Clock centre | 15.3 | 14.9–15.1 | 15.0 |
| Roof break (1.6 m in) | 16.1 | 15.1 | 15.15 |
| Lantern base | 20.9 | 20.8 at its front edge | 20.9 |
| Tower body / spire | 9.4 / 19.5 | 8.8–9.0 / 18.8 | 8.9 / 18.8 |
| 1874 eave | 9.3 | 8.8–9.1 | 8.9 |

The 1874 windows were already right. The 1874 range's north-west end lies 23.0–23.2 m from the 1910 step in both panoramas, so pass 24's extension beyond OSM holds, trimmed from 1.6 to 1.3 m (17.5 m² outside OSM).

A new calibration camera, `162_Station_Cal_Resected`, replicates the first panorama at its resected position. In a Blender render the corrected window rows, cornice, clock, roof break, tower and lantern base lie within 0–4 px of the panorama, and the step and the 1874 end within 9 px.

## Geometry and interpretation

`scripts/prepare_block28.py` (Shapely) writes `source/block28.json`. `scripts/build_block28.py` builds five meshes; `scripts/rebuild_block28.py` also rebuilds the pass 26 houses with `scripts/build_larm26.py`.

The zones:
- Södra Långgatan 10 is split at the quoin strip (x = −204.0).
- The gate house keeps a 12 m street range. Behind it lie the glazed courtyard and the lower south-west wing, as seen from above.
- The corner of the corner house is cut back 2.4 m on both streets.
- Kaggensgatan 5 has an 11.6 m street range and two courtyard wings.
- The Ölandsgatan front is split at the two downpipes (x = −227.8 and −212.0).

Nothing lies outside OSM and the zones do not overlap. The 2.97 m² not zoned is the chamfer and hairline slivers.

The houses:
- **Södra Långgatan 8.**
  - Orange render and eleven bays of 2.0 m: 3 + 5 + 3.
  - White lesenes run full height at the ends and the section joints, and between every bay on the ground floor.
  - Tall ground-floor windows, a white string course and frieze band, and the cornice.
  - The pediment over the middle five bays has a stucco cartouche and two rosettes.
  - An arched door in the east section and a carved double door with a fanlight in the west.
  - The first-floor windows sit in the render without surrounds, as photographed.
  - A grey metal roof with a cross gable behind the pediment.
- **Södra Långgatan 10, gate house.**
  - A granite plinth, a banded ground floor with round-arched shop windows spanning two bays each, and an entablature.
  - Corinthian pilasters with window crowns between them upstairs, then the architrave, a frieze and the dentil cornice.
  - Twelve bays in two groups of six either side of the risalit.
  - The risalit stands 0.25 m proud. It has paired pilasters and a crowned window over a panel, and a rusticated carriage gate with voussoirs under a pediment with modillions. Its piers are dated 1881; the date is not lettered.
  - Quoin strips at the west end and at the joint with the corner house.
- **Södra Långgatan 10, corner house.**
  - Four bays on Södra Långgatan and ten on Kaggensgatan in the same order.
  - The chamfer has rusticated piers, the shop door, a tall window between pilasters, and the segmental attic with its oculus.
- **Kaggensgatan 5.**
  - Green render and a banded ground floor with voussoirs over segmental shop windows.
  - Two doors with an oculus above each, and the carriage gateway with an iron gate in the middle.
  - Maroon awnings over the café's windows (unlettered), white window surrounds upstairs.
  - Quoins at the north end, a tile roof and a wide red dormer with four lights.
- **Ölandsgatan 5.**
  - Rough-cast render, shop windows under white awnings, two doors, and upstairs one round-arched and two square windows.
  - Three loft hatches, a timber hoisting beam with its block, iron wall anchors, an eaves board and gutter, and a dark tile roof.
- **The gate house on Ölandsgatan.**
  - Rough-cast render, the red round-arched carriage gate with anchors, four upper windows and one ground-floor window.
  - The tall blank loft wall, a tile roof and chimneys.
- **The corner house (Kaggensgatan 3).**
  - Smooth white render with grey quoins, three storeys of red-framed windows and a door.
  - A tile roof with three dormers.
- **The courtyard house:** plain rough-cast walls and a metal roof.

Tenant names, signs and awning lettering are omitted.

## Materials

The 25 new `M_Block28_*` materials tint existing texture sets towards colours read from the panoramas. There are no new texture sets.

## Verification

All reports in `previews/block28-delivery.json` passed:
- **Zoning:** `block28-zones`, `larm26-zones` and `station24-zones`.
- **Build:** ten meshes, 1,011,511 triangles. The five new houses have 348,534 and the five rebuilt pass 26 houses 662,977. There are no zero-area UV triangles.
- **FBX vectors:** no zero or non-finite normals, tangents or binormals.
- **Repeatability:** identical geometry, UV and material hashes on a second rebuild.
- **Materials:** 25 materials with normal and roughness maps.
- **Import and render:** Nanite import and render buffers pass.
- **Station house:** rebuilt with repeatable hashes, clean FBX vectors, materials, import and render buffers, and the collision test (128 floor samples, 119 capsule sweeps, no obstruction).

**Collision.** `Unreal/Content/Python/validate_block28.py` covers both passes. It takes 1,252 floor samples and 1,216 character-width capsule sweeps along walking lines 1.2 and 2.0 m outside every street front, and along Larmgatan, Södra Långgatan, Ölandsgatan, Stationsgatan and Kaggensgatan within 40 m. The only obstruction is the bank's entrance steps from pass 26, with a verified detour 0.8 m further out.

The first run also stopped at the white awnings on Ölandsgatan, whose front bars hung at 1.8–1.9 m. They were raised to clear the pavement by 2 m.

**Calibration.** `previews/block28-calibration.json` compares 71 features in eight views, each a Street View panorama and the review render of the same camera at the same pitch and vertical field of view. One of the views is the station house. The median deviation is 3.5 px and the largest 16.5 px (the corner house's first-floor windows); 63 of the 71 lie within 8 px.

The cameras stand their measured distance from the modelled facade surface, because the model's wall slabs stand 0.355 m proud of the OSM line. Placed at the OSM distance, the renders came out 4–7 % too large. Earlier passes' calibration cameras stood at the reported panorama positions and did not allow for this.

## Limitations

The following are estimates:
- the roof shapes and tops
- the courtyard fronts, wings and the courtyard house
- the positions of the Kaggensgatan openings, from photospheres without known camera positions.

The Odd Fellows house's upper block depth and the Larmgatan 6 front on Larmgatan were not re-measured. The camera height, 2.0–2.2 m, limits the accuracy of the heights to about ±5 %.

## Licences

Mapped geometry: © OpenStreetMap contributors, ODbL. Street View and the photospheres were only viewed. Authored geometry follows the project licence (CC BY 4.0, code MIT).
