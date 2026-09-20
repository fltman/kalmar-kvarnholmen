# Pass 18 — reference corrections

This pass replaces identified generic approximations. It is a visual reconstruction, not a survey, scan or an AAA-quality claim. Ground plans originate from OpenStreetMap; unmeasured heights, depth divisions, concealed rear elevations and small carvings remain approximations.

## Photographs actually inspected

- Castenska gården / Gerdas, Storgatan 20: https://www.kalmarkusten.se/platser/castenska-garden/ — Stefan Svenaeus 2023, full facade and carved portal close-up, saved `pass18/castenska-0.jpg` and `castenska-1.jpg`. Official shop identification: https://gerdaste.se/om-oss/. Five facade axes, stepped gable, red upper casements, curved ground-floor openings, wavy stone pilasters, three stone balls, oval 1667 inscription and wrought wall anchors. Model OSM 92379312. Ornament and lettering are modeled approximations; no photographic textures were extracted.
- Ångkvarnen: https://www.kalmarkusten.se/platser/angkvarnen/ — photographed 2023, `pass18/angkvarnen-0.jpg`. Three industrial blocks with different heights and bay arrangements, raised glazed entrance, pale western office.
- Riskvarnen: https://www.kalmarkusten.se/platser/riskvarnen/ — `pass18/riskvarnen-0.jpg`, `riskvarnen-1.jpg`. This is the separate eastern complex nearest the bathhouse, OSM 91846944. Previous landmark reference had been assigned to the wrong mill. High southern industrial front and lower rear wing are now distinguished; their split is estimated.
- Gamla Varmbadhuset: https://www.kalmarkusten.se/platser/gamla-varmbadhuset/ — full exterior 2004 and portal 2024, `pass18/gamla-varmbadhuset-0.jpg`, `-1.jpg`. Pale render, green frames, three west gables, oriels, recessed iron-gated entrance and carved figure. Figure is stylised geometry, not a scan.
- Jordbroporten: https://www.kalmarkusten.se/platser/jordbroporten/ — `pass18/jordbroporten-0.jpg`. Rectangular 1931 gate with two main openings and two smaller side passages. A real central pier replaces the incorrect single arch; collision routes must use actual openings.
- Kavaljeren: https://www.kalmarkusten.se/platser/kavaljeren/ — `pass18/kavaljeren-0.jpg`, `-1.jpg`. Narrow arched opening, stone pilasters, entablature and XI crest.
- Västerport: https://www.kalmarkusten.se/platser/vasterport/ — `pass18/vasterport-0.jpg`, `-1.jpg`. Different outer dressed-stone and inner brick/rough-stone facades, two upper windows, bridge piles and diagonal rails. Tunnel still simplifies the real bent passage; this remains a fidelity limitation.
- Hotell Witt: https://www.firsthotels.com/hotels/sweden/kalmar/first-hotel-witt — `pass18/witt-0.jpg`, `witt-1.jpg`; rear inspected in Google Street View at 37 Ölandsgatan, April 2025 imagery, approx. 56.6633304, 16.3678967, heading north. Two-storey glazed rear annex, lower than street block, restaurant awning and steps; depth transition estimated. Reference was viewed directly, no Google imagery used as texture.
- Barometern entrance: https://www.svt.se/nyheter/lokalt/smaland/blod-smetat-over-tidningen-barometerns-entre-i-kalmar-alltid-allvarligt — entrance architecture only, `pass18/barometern-entre.jpg`. Address confirmed by https://www.stiftelsenbarometern.se/om/. Dark portal, recessed glass doors and pale name header. Lettering uses available type rather than a facsimile of the newspaper masthead.

## Layout repairs and ground

Four south-side Stortorget buildings use their actual front-edge widths, with roof triangles clipped to mapped footprints. In particular 92412870's rear wing no longer expands its front over 92412842.

Seven green areas and twenty parking areas follow mapped OSM polygons, clipped away from buildings, road surfaces, protected squares and fortifications. Parking bay layouts are inferred 2.5 × 5 m spaces with 6 m aisles, not a record of current markings or legal parking rules. New grass and paint texture maps are procedural originals. Dedicated normal/roughness materials preserve the texture and relief of masonry, joinery and ground. Three existing rampart turf material slots are recoloured without changing their earthwork geometry.

## Verification

See `previews/pass18-build.json`, `pass18-fbx-audit.json`, `pass18-import.json`, `pass18-render-audit.json`, `pass18-bindings.json`, `pass18-collision.json`, `pass18-storgatan-collision.json`, `pass18-gates.json` and review images. Only reports that exist and pass constitute completed checks; this document alone does not certify completion.
