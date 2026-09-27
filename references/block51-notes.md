# Pass 51: Ölandsgatan's north side, Kronan to pass 48

Pass 51 details the Ölandsgatan range of the district volume 92379292. It runs from the Kaggensgatan corner to pass 48's yellow house and holds three buildings:

- **Kronan**, the white stone house on the corner, with its gable to the street:
  - sandstone quoins at both corners;
  - two tall ground-floor windows with cellar lights, and two upper windows;
  - a boarded door with a menu case;
  - a row of cross-shaped wall anchors;
  - in the gable, a boarded hatch and a round opening under the apex.
- **The low range**, a blank limewashed wall:
  - a heavy cornice;
  - a segmental carriage arch in a white moulding, with its boarded leaves folded open;
  - a door up three steps.
- **The old stone house**, with a half gable that rises east to the party wall with pass 48:
  - one window with a cellar hatch below;
  - a small window high in the gable.

The rest of the block (the Kaggensgatan and Storgatan sides, the courtyard ranges) keeps the district height of 9.75 m under an estimated roof. The mesh keeps its name (`SM_Kvarnholmen_House_92379292`).

Panoramas are working references only. No pixel is used as a texture, and no panorama, depth or tile data was extracted.

## Sources

- **Outline:** `source/block51.json`, four zones cut from 92379292 (its courtyard hole kept):
  - `kr` runs to Kronan's east quoin and is 14 m deep;
  - `lr` runs to the courtyard;
  - `eg` runs to pass 48's joint and is 12 m deep;
  - `bk` is the rest.

  The rear zone's simplification leaves a 0.33 m² sliver past the OSM line. It is accepted up to 0.5 m² for this 1087 m² block.
- **Google Street View**, April 2025, 90° vertical field of view (1372 × 871 frames): three panoramas on Ölandsgatan, facing north, plus two views tilted up 30–35° for the gables. The review cameras are 298 (stone house), 299 (arch) and 300 (Kronan); 301 is an aerial view.

## Measurement

**Registration.** The three cameras are chained on ten shared edges (the arch, Kronan's windows and door) and anchored on the Kaggensgatan corner and pass 48's joint.

The cameras are re-solved for the north facade; the distances found for the south facade in pass 49 do not carry over. Pairs agree within 0.6 m (Kronan's upper windows) and otherwise within 0.3 m. The cameras stand 5.7–6.0 m out, at a height of 2.27 m.

| Feature | Measured (m) | Modelled (m) |
|---|---|---|
| Kronan | x -182.63 to -171.69; ground windows 1.74–4.32; upper 6.48–8.41; door 0–1.99 at x -177.75 to -176.46; plinth 1.1; eaves 9.8; apex 15.9 (x -176.7); hatch 10.05–12.31; round opening 14.0 | the same, ridge 15.6 |
| Low range | arch x -169.0 to -166.35, springing 2.75, crown 3.2; door x -160.9 to -160.02, sill 1.13, head 2.99; cornice 6.35–7.5; plinth 1.0 | the same |
| Old stone house | x -159.82 to -152.99; window 2.21–3.26; gable window 7.58–8.84; hatch 0–0.88; the gable from 7.84 (west) to about 13.3 at the party wall | the same |

## Verification

See `previews/block51-delivery.json`:
- every report passed;
- 188,341 triangles in one mesh (the whole block);
- identical on two rebuilds;
- 67 floor samples and 60 capsule sweeps, no obstructions;
- calibration of 17 features: median 8 px, largest 18 px (the cornice);
- passes 28–50 unchanged.

## Limitations

- **The gables** were read on the facade plane from the tilted views.
- **The old stone house's roof shape** behind its half gable is an estimate.
- **Estimates:**
  - the low range's roof;
  - Kronan's depth (14 m);
  - the rest of the block.
- **Omitted:** the signs, the menu board, the street lamp and the street-name plate.
