# Whole-house refinement, pass 17

The mapped inventory is 338 numbered building objects, plus the cathedral, town hall, Stadshotellet, theatre and Frimurarehotellet. The church's many mesh pieces count as one building. This is coverage of the current mapped reconstruction, not a claim that every real-world shed is present in OSM.

303 previously generic houses were rebuilt; 35 previously individually worked numbered buildings and the five named landmarks retain their authored geometry. The generated report must verify all expected assets exist and have materials, and that no pending entry remains.

## Geometry and material changes

Exposed elevations are computed against **all** mapped neighbours, including the older square/corridor buildings. Shared walls are masked. Recorded courtyard rings and lower-level mapped passages remain in use. Recessed windows have casement divisions, stepped trim, hinges, folded sheet-metal sills, lintels and jamb returns. Street shopfronts and rear windows have different proportions. Small service buildings have simpler doors and ventilation instead of elaborate street ornament. Doors interrupt the stone plinth. Gutters have a channel section, brackets and attached downpipes.

137 sufficiently rectangular footprints are eligible for a continuous ridge roof; complex clipped roofs remain, with five identified house roofs and the old water tower handled separately. The rectangular inference is a geometric cleanup, not photographic verification of those roofs.

123 rectangular roofs were rebuilt with coherent ridges; two missing flat caps were repaired.

Eight dedicated materials use the project's original procedural colour, normal and roughness maps, with fine continuous plaster instead of the scan containing regular seams. Existing landmark materials and the nine pass-16 street houses are unchanged. Source normals and tangent frames are validated in FBX and again against Unreal's actual render buffers.

## New direct visual references

Photographs by Stefan Svenaeus, viewed in this pass, are retained locally **only as visual reference**, not projected into textures. Architectural descriptions on Kalmarkusten cite Kalmar kulturmiljöportal (Wahlbergska: Kalmar Lexikon). All coordinates and scale estimates remain approximate.

| Object | Source | Applied observations |
|---|---|---|
| 93238156 | [Norra Långgatan 84 / Repslagaren 27](https://www.kalmarkusten.se/platser/norra-langgatan-84-i-kalmar/) | Yellow three-storey facade, red cross windows, central projecting oriel, curved attic outline, red metal roof. Oriel curvature is approximated with facets. |
| 90859847 | [Fiskaregatan 3 / Skoflickaren 3](https://www.kalmarkusten.se/platser/fiskargatan-3-i-kalmar/) | Pale two-storey facade, red joinery, round-headed ground windows, central entrance, pilasters, horizontal base courses, attic and red roof. |
| 91926329 | [Bokbindaren 10](https://www.kalmarkusten.se/platser/fastigheten-bokbindaren-10-i-korsningen-proviantgatan-norra-langgatan-i-kalmar/) | Green-grey battened timber, paired casements, panelled door, red broken-pitch roof. |
| 92379265 | [Gesällen 23](https://www.kalmarkusten.se/platser/gesallen-23-i-korsningen-fiskargatan-kaggensgatan-i-kalmar/) | Ochre timber shop corner, light trim, green joinery, red tile roof. The OSM footprint contains attached volumes; unseen shop bays remain inferred. |
| 92412873 | [Wahlbergska / Ölandsgatan 27](https://www.kalmarkusten.se/platser/olandsgatan-27/) | Pale classical frontage, green cross windows, curved central attic, supported balcony and red metal roof. Rear/side volumes remain estimates. |

## Limits

This pass finishes **processing** the remaining generic building inventory. It does not make all 343 buildings individually photo-accurate or establish finished AAA quality. For 296 newly refined houses, heights, fenestration and hidden elevations remain estimates based on mapped footprint, earlier palette and building type. No new Street View panoramas were visited in this pass. Earlier pass-16 panoramas remain documented in street16-notes.md. Modern tenants/signage are not inferred from old photographs.

Additional direct reference: [Gamla vattentornet, photographed 2023](https://www.kalmarkusten.se/platser/kalmar-gamla-vattentorn/). Brick, narrow slit windows, stone string courses and brackets, crenellated crown and six poles were interpreted from the photograph. The [Kalmar läns museum description](https://kvarnholmen.kalmarlansmuseum.se/gamla-vattentornet) supports the 65 m height and fifteen storeys. This replaces a generic cylindrical residential facade. No flags or current occupancies are assumed.

Additional direct reference: [Klapphuset](https://www.kalmarkusten.se/platser/klapphuset/) (photograph viewed in this pass). The generic two-storey house is replaced by a low red weatherboard boathouse, high white multipane windows, a dark hipped roof, two ventilators and a timber skirt. A narrow supported deck joins its entrance to the mapped shoreline. Deck dimensions are estimates, not a surveyed bridge. Station and Baronen photos downloaded during research were not used to claim individually reconstructed elevations in this pass.
