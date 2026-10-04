# Pass 98: the mainland between Kvarnholmen and the castle

Until pass 98, the castle (pass 27) and the prison patch (pass 85) stood alone in open water. Pass 98 adds the mainland between them and Kvarnholmen, from Västerport south-west to Kalmarsundsparken:

- **Ground:** the land face between the OpenStreetMap coastlines inside the box x −1650…−470, y −560…320. Land the model already has is subtracted: Kvarnholmen with the station, the castle island with its ravelin and islets, and the prison patch. The result is about 72 ha, laid at model z 0.30, with a bank down to the water along the shore.
- **Streets and paths:** Slottsvägen and the other streets in asphalt, with widths by road class. Park and cemetery paths are in gravel.
- **Parks:** Stadsparken (the castle park), the Krusenstjernska garden, Kalmarsundsparken, and the smaller greens and gardens.
- **Trees:** 1,076 in all. The 117 trees mapped in OSM come first; the rest are scattered evenly through the parks and cemeteries, clear of paths and buildings.
- **Cemeteries:** Gamla kyrkogården (9,272 m²) and Södra kyrkogården (38,370 m²).
  - Lawns with 7,238 headstones and grave slabs in rows aligned with each cemetery's long edge.
  - Clipped hedges along their bounds.
- **Buildings:** the 412 houses of the blocks round these areas, as plain volumes.
  - Storeys come from OSM building:levels, otherwise 1 or 2 by size.
  - Walls have windows on each storey.
  - Hipped roofs on compact plans; flat roofs behind a parapet on large or irregular ones.
  - Wall colours vary by building.

## Sources and accuracy

This pass gives context at street-plan accuracy, from OpenStreetMap (`references/osm-slott98.json`, ODbL). No panorama was used. Building heights, colours and roof forms are generic, not measured.

## Verification

- The preparation checks passed: land about 720,000 m², two cemeteries, 412 buildings.
- A sandbox build (prelude pass 96) ran without errors. Aerial renders from the castle, the park and the cemetery showed:
  - the castle now sits in its setting on the mainland;
  - the streets meet the earlier Kvarnholmen streets;
  - the cemeteries show their grave rows and hedges.
- Faces with no area or under 0.1 mm wide are removed before the export.
- The Unreal import and its checks are deferred.

## Limitations

- **Generic buildings:** the houses are not detailed; each is a plain volume.
- **Not modelled here:** Kalmar domkyrka and other landmarks on the mainland, which earlier passes may have.
- **Ground:** flat at one level, with no terrain.
- **Water edges:** they follow OSM's coastline, which in places is approximate.

## Official build

The lead's build of pass 98 passed the Blender geometry checks, two rebuilds gave identical meshes, and passes 28–97 are unchanged. The Unreal import and its checks are deferred.

## Changed in pass 107

Pass 107 re-created SM_Slott98_Cemeteries, SM_Slott98_Trees and SM_Slott98_Buildings_M with this pass's own code, leaving out the generated graves, hedges and trees inside Gamla kyrkogården and the plain box at the burial chapel (OSM 500979084). Gamla kyrkogården is now detailed from the 1944/1974 grave plan; see references/block107-notes.md.
