# Pass 42: Östra Sjögatan, from the brewery to the castle park

Pass 42 details the Östra Sjögatan front of the district volume 92412873, south of pass 40's corner house. OSM draws the whole block as one way. Along the street it holds five buildings:

- **The Nordstjernan brewery**, in brown-grey roughcast between pale stone quoin strips:
  - a central bay with two tall white frames. Each frame holds a segmental-headed window below, a recessed panel and a round-arched window above.
  - small third-storey windows and iron anchors;
  - a steep gable to about 17 m with a triple window;
  - a south bay with one great round-arched window over a white panel, and three small attic lights.
- **House 2** (roughcast):
  - three axes on three storeys in flat white surrounds;
  - a wall dormer of three lights under a small pediment.
- **A narrow house** between stone strips:
  - two axes: a ground-floor row and two upper rows;
  - a gable with a round window.
- **The grey house** ("8"):
  - two windows and a recessed entrance up three steps on the ground floor;
  - large and small blind panels where the second-storey windows would be;
  - one row of windows;
  - a shuttered attic storey in the wall face under the eaves;
  - a small gable.
- **The yellow corner house, Östra Sjögatan 1:**
  - two storeys in yellow render with cream surrounds and a double string course;
  - four windows and a panelled double door on Östra Sjögatan, and three axes to the park (estimated);
  - a tile roof with a round-headed dormer.

**The courtyard block and the Wahlberg house on the park** (Ölandsgatan 27) were modelled in pass 17 from a web photograph. The new mesh replaces that one, so their look is carried over:

- nine axes of green cross windows and the door;
- the curved central attic with its balcony;
- the height of 7.65 m.

The courtyard block's roof is now a low slope instead of pass 17's hipped roof.

The mesh keeps its name (`SM_Kvarnholmen_House_92412873`). Panoramas are working references only. No pixel is used as a texture, and no panorama, depth or tile data was extracted.

## Sources

- **Outline:** `source/district17.json`. The front ranges are split at the measured joints (y -95.0, -102.6, -106.6, -115.0, -119.1 and -126.6). They run 10 m deep, and the yellow house to the courtyard notch. The rest of the outline is the courtyard block. The neighbours are:
  - pass 40's corner house (`source/block40.json`) to the north;
  - the district volumes 92412854 and 92412839 behind.
- **Google Street View**, official imagery of April 2025, viewed at a vertical field of view of 90° (level, and 35° up). The street is narrow, so the camera stands 3.3-4.6 m from the facade.

| Panorama | Id | Camera | Used for |
|---|---|---|---|
| "3 Östra Sjögatan" | XK2J52FyqnPWxc9Qt-XajA | 248, 249 | the brewery |
| "2 Östra Sjögatan" | FKdQl_LXWwFH__pHtjsXHQ | 250, 251 | house 2; the brewery's great window from the south |
| "1 Östra Sjögatan" | k_8pBI-D3TswqdCwZg7MRw | 252, 253 | the grey house and the narrow house |
| "1 Östra Sjögatan" (south) | nBLMj0H-tSDUyrSpQRRnJw | 254, 255 | the yellow house |
| "1 Östra Sjögatan" (corner) | YofiAb26xDaM2DrV-WSN4Q | — | the yellow house's corner and park end |

## Measurement

**Registration.** The five cameras are chained along the street:
- each camera's distance to the facade comes from its base row and one common height scale;
- nine pairs of window and strip edges must fall at the same place from neighbouring panoramas;
- the chain is anchored at the yellow house's street corner (y -140.98).

The pairs agree to 0.00-0.10 m. The cameras stand 3.27-4.60 m from the facade, at a height of 2.32 m.

Heights come from the level views. The pitched views give the upper storeys only: at 3.4 m and a 35° pitch, horizontal readings there were up to 1 m off.

| Feature | Measured (m) | Modelled (m) |
|---|---|---|
| Brewery great window | glass 1.94 to the springing 5.36, crown about 6.5; 2.28 wide | the same |
| Brewery tall windows | lower 1.22-3.18 (segmental), panel 3.32-4.54, upper 4.82-7.07 (round) | the same |
| Brewery third storey, eaves, gable | windows 8.3-9.5; eaves about 11.2; gable apex about 17.7 in the pitched view | 8.30-9.50; 11.2; 17.2 |
| House 2 | windows 1.85-3.02, 4.79-5.84, 7.25-8.30; eaves about 10.0-10.9; dormer windows 10.4-11.2, pediment 12.8 | the same, eaves 10.2 |
| Narrow house | windows 1.56-2.95, 6.2-7.25, 9.27-10.16; gable to about 14.8 | the same, gable 14.6 |
| Grey house | windows 1.5-2.85 and 6.0-7.3; blind panels 3.5-4.8 and 5.1-5.45; small panels 8.2-8.6; shutters 10.45-11.55; eaves 11.8 | the same |
| Yellow house | windows 1.36-3.05 and 4.55-6.0; door 0.67-3.1; string 3.41-3.76 and 4.21-4.37; eaves 7.1 | the same |

## Verification

- **Zones:** `previews/block42-zones.json`. Eight zones cover the outline (1,069 m²).
- **Build:** one mesh, 187,716 triangles, no zero-area UV triangles.
- **Repeatability:** identical geometry on two rebuilds.
- **Passes 28-41 unchanged:** their meshes hash identically to their reports.
- **FBX audit:** clean.
- **Unreal:** 18 materials, Nanite, clean render buffers.
- **Collision:** 94 floor samples and 77 capsule sweeps. The grey house's and the yellow house's steps are passed 0.8 m further out.
- **Calibration:** `previews/block42-calibration.json`, 24 features in four level views: median 5 px, largest 20 px (house 2's downpipe, about 0.16 m). The upper storeys were checked by overlay in the pitched views.
- **Delivery:** `previews/block42-delivery.json`; every report has passed.

## Limitations

- **The brewery's gable height** rests on a steep pitched view (±0.7 m).
- **Estimates:**
  - the brewery's north end (1.4 m, plain);
  - the yellow house's park end;
  - all rear walls and the roofs.
- **The Wahlberg house and the courtyard block** are pass 17's estimate, not measured. Their roof is simplified.
- **Omitted:** the brewery's sign "Bryggeriaktiebolaget Nordstjernan", the house numbers, the street sign, the bicycles.
