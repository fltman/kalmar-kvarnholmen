# Larmgatan by the station — pass 26

Research date: 2026-09-23. This pass replaces five generic district volumes on Larmgatan, between Södra Långgatan and the station square:
- the Larmgatan 1 block (OSM way 91222222), split into the bank, the later office and the lower south wing
- Larmgatan 10 (91856621)
- Larmgatan 8 (91856599)
- Larmgatan 6 (91856613)
- the Odd Fellows house at Larmgatan 2 (91856604).

Panoramas are working references only. No pixel is used as a texture, and no panorama, depth or tile data was extracted from Google.

## Sources

- **OpenStreetMap** (`source/kvarnholmen.json`): the five building outlines. It also supplies the heights of the neighbouring buildings, which decide where a wall shows above a neighbour's roof.
- **Google Street View**, viewed in the browser. The captures used are from April 2025. Each position below is the panorama the camera replicates.

| Position (WGS84) | Camera | Used for |
|---|---|---|
| 56.6619035 N, 16.3608527 E, station plaza | 137, 143 (heading 82°) | The bank's plaza front with the risalit, pediment and balcony. Also the mansard, dormers, clock lantern and south wing, and the height calibration. |
| 56.6622659 N, 16.3617759 E, Södra Långgatan | 138 (heading 250°) | The north front with the round-arched ground floor, festoons, entrance and curved gable |
| 56.6620328 N, 16.3622273 E, Larmgatan | 139, 140 (headings 25° and 62°) | Larmgatan 10 and 8. Other headings show the bank's Larmgatan front, the chamfered corner and the office. |
| 56.6617943 N, 16.3625212 E, Larmgatan at Ölandsgatan | — | Larmgatan 6, the office and the Odd Fellows house |
| 56.6614318 N, 16.3623679 E, south end of Larmgatan | 141 (heading 38°) | The Odd Fellows house with its turrets, frieze and arched ground floor |

## Measurement

Heights were measured by inverting the panorama camera, the method of pass 24. With the position, heading, pitch and vertical field of view known, a pixel's viewing ray is intersected with the vertical plane of the facade. Scale in the close views was checked against the pavement (z = 0). The distant plaza view needed a −2.13° tilt correction. Maps clamps the vertical field of view at 90°, so the wide views were rendered at 90°.

| Feature | Height (m) |
|---|---|
| Bank cornice top | 10.8 |
| Bank mansard break (1.7 m in from the wall) | 15.4 |
| Bank upper roof, lantern base | 16.6 |
| Lantern dome | 18.8 |
| Lantern spire | 21.4 |
| Larmgatan 8 cornice | 11.3 |
| Larmgatan 8 attic gable | 13.0 |
| Larmgatan 6 street front | 10.0 |

The heights below are estimates from storey counts and proportions, not measurements:
- Larmgatan 10: cornice 10.6, mansard break 14.4, top 14.9 m
- the Odd Fellows house: parapet 11.2, roof 12.6 m
- the office: 10.4 m
- the south wing: eaves 7.0, ridge 10.0 m
- the attic of Larmgatan 6: 12.7 m, with a roof top of 14.5 m

## Geometry and interpretation

`scripts/prepare_larm26.py` (Shapely) writes `source/larm26.json`. Walls are built only where they show above a neighbour's roof, and neighbours outside the pass keep their current heights. The checks:
- The five outlines cover 3,965.2 m², of which 3,960.1 m² is zoned.
- Nothing lies outside OSM, and the zones do not overlap.
- The 5.13 m² not zoned is the chamfer, the turret corners and hairline slivers.

- **Larmgatan 1 split.**
  - The red bank front on Larmgatan ends 36 m from Södra Långgatan. Its rounded corner is visible in the Larmgatan panorama.
  - South of it is the later office (248 m²). West of x = −313.2 is the lower south wing (207 m²), whose courtyard front is the mapped line at y = −112. The bank keeps 1,065 m².
  - The corner at Larmgatan/Södra Långgatan is cut back 2.2 m, as photographed.
- **The bank.**
  - Terracotta render over a 1.17 m granite plinth, with a floor band, frieze, dentil cornice and a copper mansard in two stages.
  - Larmgatan has nine axes between pilasters, with stucco festoons above the upper windows.
  - The plaza front has five axes and a pedimented centre risalit, 5.2 m wide and 0.35 m proud, with an oval light and a balcony door. Comparison with the plaza panorama moved the risalit 1.3 m north of the wall's centre.
  - Södra Långgatan has ten axes, with round-arched ground-floor windows and keystones. The entrance is on the fourth axis, with steps, a portal surround and a curved gable above the cornice carrying an oval light and a cartouche.
  - The chamfer has rusticated banding and a corner balcony.
  - Round-headed copper dormers sit over the street fronts.
  - The octagonal copper clock lantern stands near the north-west corner. It has four dials, an onion dome, a ball and a spire.
- **Office and south wing.**
  - The office has three storeys of yellow-brown render and a flat roof. On Larmgatan it has a glazed entrance under a canopy on two tie rods.
  - The south wing has two storeys of ochre render, a copper hip roof and a chimney.
- **Larmgatan 10.** Cream render. The shop floor alternates wide windows with narrow doors, with red awnings on Södra Långgatan. The windows have cornice heads, and a round oriel with five lights on the second floor overhangs the corner. The red metal mansard has dormers with red hoods.
- **Larmgatan 8.**
  - Orange render with grey-green stone trim over a dark stone shop floor, with shop windows under white awnings and a central door.
  - A corbelled three-sided oriel rises through the first and second floors on the centre axis.
  - The second floor has twin round-headed windows under shared surrounds, and there is a bracket frieze under the cornice.
  - An arched attic gable carries an arched window, and the slate hip roof has two dormers.
- **Larmgatan 6.**
  - Red brick with light stone bands.
  - Both street fronts have large pub glazing, under black awnings on Larmgatan. Iron railings stand at alternate top-floor windows and along the parapet.
  - A set-back attic storey (1.4 m) sits on the flat roof, with a low tiled hip roof. The attic's form is an interpretation of what shows above the parapet.
- **The Odd Fellows house.**
  - Cream Jugendstil render with dark green joinery. On Larmgatan the ground floor is round-arched with awnings and has the entrance on the third axis. A first-floor balcony is on the second axis.
  - The frieze is lettered ODD FELLOWS between red roundels.
  - Round turrets fill both Larmgatan corners (radius 2.4 m, cutting 2.47 m² from the outline). Their windows are on the diagonal, and each has a drum above the parapet with six arched lights and a copper cap and finial.
  - A copper roof sits behind the parapet.
- **Courtyard and party-wall fronts** get plain casements and plinths. They are at most partly visible in the panoramas, so their layout is an interpretation.

Tenant names, shop signs and logos are omitted. Only the building's own name, ODD FELLOWS, is lettered.

## Materials

The 26 new `M_Larm26_*` materials tint existing texture sets towards colours read from the panoramas. Each tint is computed against the texture's measured mean colour in linear space. No new texture sets.

## Verification

All reports in `previews/larm26-delivery.json` passed:
- **Build:** 696,880 triangles, with no zero-area or zero-UV triangles.
- **FBX vectors:** no zero or non-finite normals, tangents or binormals.
- **Repeatability:** a second rebuild gave identical geometry, UV and material hashes.
- **Materials:** all 26 materials have normal and roughness maps.
- **Import and render:** the five meshes import with Nanite, and their render buffers pass.

The collision test (`Unreal/Content/Python/validate_larm26.py`) takes 868 floor samples and 847 character-sized capsule sweeps. It covers:
- walking lines 1.2 m and 2.0 m outside every street front
- Larmgatan, Södra Långgatan, Ölandsgatan and Stationsgatan within 40 m of the five buildings.

The only obstruction is the bank's entrance steps on Södra Långgatan. They reach 1.55 m from the wall, so they block 4.1 m of the 1.2 m line. A verified detour passes 0.8 m further out, and the 2.0 m line is clear. The first run also flagged two faults in the test itself:
- The office's line started in the re-entrant corner against the south wing's window sill. Free line ends now start 0.3 m beyond the walking-line distance from the corner.
- The detour check treated each blocked segment of the steps separately. Consecutive blocked segments now count as one obstacle.

The Unreal editor crashes during its own shutdown, after the level and assets have been saved. The same happened after every Unreal session of passes 23–25.

## Licences

Mapped geometry: © OpenStreetMap contributors, ODbL. Street View imagery was only viewed, and nothing from it is stored or redistributed. Authored geometry follows the project licence (CC BY 4.0, code MIT).
