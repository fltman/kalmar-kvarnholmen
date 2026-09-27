# Pass 45: the south side of Ölandsgatan west of Västra Sjögatan

Pass 45 details two district volumes on the south side of Ölandsgatan, from the corner of Västra Sjögatan westwards:

- **The yellow two-storey house** (92379262), a baroque-classical stone house:
  - five axes of white casements of many panes in flat surrounds on both storeys;
  - a blank panel between the storeys over the middle axis;
  - a grey plinth, a moulded cornice and a tile roof hipped to the street;
  - three axes on its east end to Västra Sjögatan.
- **The one-storey entrance link** (92379262): a relief panel over the green double door in a stone surround on two steps, and a glazed storey set back above.
- **The beige house of 1909** (92379262):
  - a long one-storey range of eight windows in pale surrounds;
  - a curved front gable at each end, the eastern with two windows and the western with an arched window;
  - three dormers in the tile roof between the gables.
- **The plain beige two-storey house** (92379314, Frösunda):
  - three large and three small windows on each storey;
  - the glazed entrance under a sign board;
  - a tile roof.

The Södra Vallgatan side and the courtyard wings stay plain at the district heights. The meshes keep their names (`SM_Kvarnholmen_House_92379262` and `…_92379314`).

Panoramas are working references only. No pixel is used as a texture, and no panorama, depth or tile data was extracted.

## Sources

- **Outlines:** `source/district17.json` (92379262, 92379314). Street ranges split at the measured joints (x -53.3, -56.2, -77.24).
- **Google Street View**, April 2025, 90° vertical field of view: four panoramas along Ölandsgatan ("21 Ölandsgatan" and its neighbours), review cameras 275-278.

## Measurement

**Registration.** The four cameras are chained along the street:
- five window edges seen from two panoramas;
- the link's door and two windows seen from a third;
- anchored on the Västra Sjögatan corner (x -40.7).

Pairs agree to 0.00-0.37 m. The cameras stand 4.8-5.2 m from the facade, at a height of 2.24-2.36 m.

| Feature | Measured (m) | Modelled (m) |
|---|---|---|
| Yellow house | ground windows 1.31-2.99 (surrounds), upper 4.59-6.14; plinth 0.51; eaves about 7.2-7.5 | windows 1.43-2.99 and 4.73-6.18; eaves 7.3 |
| Link | door 0.58-2.90 (surround 3.94); relief 3.3-3.9; parapet about 4.8 | the same, parapet 4.4 |
| 1909 house | windows 1.25-3.19 (surrounds); eaves 4.5-4.85; dormer windows 5.3-6.0; gables' windows 4.7-5.6 (east) and 5.1-6.5 (west, arched); gable tops about 8.1-8.3 | the same |
| Frösunda house | ground windows 1.31-2.53, small 1.37-2.17; upper 4.40-5.66, small 4.86-5.53; eaves about 6.6-6.8 | the same |

## Verification

- **Zones:** `previews/block45-zones.json`. Six zones cover the outlines (798 m²).
- **Build:** two meshes, 105,563 triangles, no zero-area UV triangles.
- **Repeatability:** identical on two rebuilds.
- **Passes 28-44 unchanged:** their meshes hash identically.
- **FBX audit:** clean.
- **Unreal:** 13 materials, Nanite, clean render buffers.
- **Collision:** 162 floor samples and 150 capsule sweeps, no obstructions.
- **Calibration:** `previews/block45-calibration.json`, 23 features in four views (whole-view comparison): median 8 px, largest 20 px (the east gable).
- **Delivery:** `previews/block45-delivery.json`; every report has passed.

## Limitations

- **The gables' outlines** follow the panoramas only roughly; the western gable's crest (a small carved top) is omitted.
- **The link's glazed storey** and all the roofs are estimates.
- **The yellow house's Västra Sjögatan end** was not measured; its three axes are placed evenly.
- **Omitted:** the date "1909", the relief's subject, the signs, the plaques and the bicycle stands.
