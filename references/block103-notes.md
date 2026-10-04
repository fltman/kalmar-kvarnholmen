# Pass 103: the prison building corrected

Pass 103 rebuilds the prison building of pass 85 (`SM_Prison85_Anstalten`, Anstalten Kalmar, OSM way 91053122). This deliberately changes that one pass 85 mesh. The pass 85 ground, walls, fences and Rotunda are unchanged.

## What was wrong

Pass 85 had three faults:
- **Roofs:** it cut the outline into three zones and laid a hipped roof over each zone's bounding rectangle. The roofs overlapped, and they stood far out over the walls on the diagonal parts.
- **Colour:** the walls were ochre.
- **Windows and form:** both were a generic three-storey grid with an invented central pavilion.

## What it is now

Satellite imagery and the winter photograph from the Västerport footbridge were used, both view only. They show a cross-shaped cell prison, which the outline was split into by its OSM vertices, in the frame of the main range:

- **The main cell range**, 52.5 × 13 m, runs north–south (local bearing 30).
  - Three storeys of pale cream render over a grey plinth, with small windows in dark frames, white surrounds and a cornice band.
  - A low saddle roof in dark grey sheet with hipped ends.
  - A row of chimneys along the ridge, roof hatches on the west slope and roof lights on the east slope, as the satellite image shows.
- **The cross wing**, 12.5 m wide, projects 15 m east toward the water and is taller than the main range.
  - The east gable end is a pediment over a cornice, with a chimney at the apex and a pair of windows in the tympanum.
  - Seven tall round-headed windows high up, and the single entrance in a stone surround.
  - Windows in three rows on its sides.
  - Its saddle roof runs across the main range.
- **The low annexes** in the corner south of the cross wing are one storey with flat roofs.
- **The north range** is modern: grey render, two storeys, a flat roof behind a white parapet.

## Heights

| Part | Eaves | Ridge / apex |
|---|---|---|
| Main range | 10.2 m | 13.6 m |
| Cross wing | 13.0 m | 17.8 m |
| Annexes | 4.2 m | – |
| North range | 7.0 m | – |

These are estimates. The main range comes from its storey count. The cross wing is scaled from the winter photograph against the main range, corrected for the two façades' distances from the camera (96 m and 81 m).

## Verification

- The main range and the cross wing lie within the OSM outline: 99 % of each rectangle's area.
- The Blender geometry checks passed and two rebuilds gave identical meshes.
- Passes 28–102 are unchanged, except pass 85's prison mesh, which is the intended change.
- 124 faces with no area or under 0.1 mm wide are removed before the export.
- The Unreal import and its checks are deferred.

## Limitations

- **Heights:** all are estimates.
- **The north range:** its windows are generic.
- **Back walls:** the walls towards the yard are not photographed.
- **Comparison view:** the winter photograph's camera position is not known well enough for a pixel comparison.
