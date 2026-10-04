# Pass 79: green areas and the city wall

The user asked for an extra review of the green areas and the city wall. Pass 79 renders the model from five April 2025 Street View panoramas and compares the views:
- two on Skeppsbrogatan;
- two on Södra Vallgatan;
- one on Östra Vallgatan.

It fixes what disagrees, as new meshes plus one corrected pass 14 mesh:
- `SM_Kvarnholmen_Green79_Lawns`
- `SM_Kvarnholmen_Green79_Glacis`
- `SM_Kvarnholmen_Trees79`
- `SM_Kvarnholmen_Hedge79`
- `SM_Kvarnholmen_Ringmur_Sodra` (the correction)

Panoramas are working references only. No pixel is used as a texture.

## Findings and changes

1. **The southern wall's inner side was wrong.** Pass 14 built the whole OSM city-wall ring as 4.25 m masonry, including the rampart's inner side facing Södra Vallgatan. The panoramas there show a grass slope, about 5 m wide, from the park up to the rampart top (about 3 m). A row of pollarded limes stands on the crest, and there is a low parapet only on the outer edge.
   - The inner runs are removed from `SM_Kvarnholmen_Ringmur_Sodra`: the long run round the bastion gorge, and the inner segment of the west run. The passage walls and the end walls are kept.
   - A grass slope (the glacis) replaces the removed runs, and 54 limes stand along the crest. The limes reach about 3.1 m above the rampart top and stand 5 m apart, as measured.
   - This changes a pass 14 mesh. Its geometry differs from earlier releases by design.
2. **The outer wall along Skeppsbrogatan** measured 3.9–4.1 m, against 4.25 m (4.4 m with coping) in the model, which is left as it is. A clipped hedge about 1.3 m high stands on its crest, and it is added along the outer faces seen from the street: the bastion's flanks and the long southern runs.
3. **Green areas pass 18 left grey:**
   - the mapped village greens (35773131 by Västerport, 128278550 and 128278551) and the common;
   - the three playgrounds, drawn as sand;
   - the east bastions. OSM leaves them untagged, but the panorama at Östra Vallgatan shows lawn from the street, past the low walls, down to the shore, with trees and a playground.
4. **Trees:**
   - the 27 mapped trees on land;
   - an estimated planting of mature trees in the parks and lawns, on a jittered 13 m grid kept 3 m clear of paths, walls and buildings.
   - A tree is kept only where the ground under it is open. Five trees fell inside a house (a garden OSM puts inside the pass 37 block) and were dropped; 128 are kept.

## Verification

See `previews/block79-delivery.json`:
- every report passed;
- identical on two rebuilds;
- passes 28–78 unchanged.

The collision test covers the named streets within 25 m of anything new and the mapped park paths near the trees: 2,128 ground samples and 2,047 character-width capsule sweeps, with the capsule riding the local ground. Nothing this pass added obstructs them. The validator lists 16 obstructions at the gate tunnels separately. A plain capsule 1.05 m up, tested through both gates, explains them:
- **Jordbroporten:** the 1931 gate has two main openings and a real central pier (pass 18). Kaggensgatan's centreline runs into that pier, while the opening 0.85 m to the east is clear.
- **Kavaljersporten:** clear at all three offsets. Those hits come from the validator's ground probe finding the rampart top above the tunnel vault.

Neither is a fault in the model.

## Limitations

- **Tree positions in the parks** are estimates except for the mapped trees and the lime row. The crowns are simple clustered forms.
- **The wall stone** keeps pass 14's warm rubble texture, while the real walls are grey-pink granite fieldstone with pale mortar. Changing it would change a material shared with other landmarks, so it is left for a separate decision.
- **The west, north and Regeringen walls** have only user photospheres, no official panoramas, and were not re-measured.
