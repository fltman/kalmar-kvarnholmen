# Pass 85: Anstalten Kalmar, west of Västerport

Pass 85 adds the prison, Anstalten Kalmar (OSM way 91053122, Ravelinsgatan 2), and its surroundings on the mainland shore west of Västerport. The prison lies outside the district model, so the pass also adds the ground it stands on.

## What the pass adds

### Ground

- **The shore patch.** It is bounded by the OSM coastline (way 90822660) opposite Västerport and closed inland along a cut line that clears the walls, Ravelinsgatan and the Rotunda. Its area is 17,704 m², and it is laid at model z 0.30.
- **Surfaces.** The patch is grass. Ravelinsgatan is 6 m of asphalt and the service road 4 m. The walled yard is gravel.
- **The bank.** It drops 2.5 m out from the coast to below the water line.

### The prison

The building has three storeys of ochre render over a grey plinth, with white cornices and corner pilasters, under low hipped metal roofs with rows of chimneys. Its outline is split into three ranges:
- **The front range** faces Västerport and the water. Its central pavilion projects at the OSM risalit corners and carries a pediment, a round clock window and an arched entrance.
- **The long cell range** runs at a bearing of 30°. It is 13.1 m deep, which is the distance between its parallel west and east faces in OSM.
- **The north range** runs across the top, 12 m deep.

### Walls and the Rotunda

- **Walls and fences:** the OSM barriers.
  - The north-west yard wall is 4.5 m high.
  - The other walls are 3 m high.
  - The fences are 2.4 m high.
- **The Rotunda** by Ravelinsgatan (OSM way 1118433612) is a white octagon with a deep cornice and a low roof.

The panoramas are working references only. No pixel is used as a texture.

## Measurement

Two views show the prison:
- a user panorama on the footbridge from Västerport, in winter, which shows the front range, the pavilion and the north range;
- Google Street View on Olof Palmes gata (pano SFh-OQxkQ8Yk9NuwXaMYdw, April 2025), which shows the Rotunda, the wall and the prison behind it.

Neither is close enough to measure from, so these heights are estimates from storey counts:

| Part | Eaves | Roof top |
|---|---|---|
| Front range | 11.0 m | 13.4 m |
| Cell range | 11.0 m | 13.6 m |
| North range | 10.6 m | 13.0 m |
| Pavilion pediment | – | 15.7 m |

## Verification

- The building zones cover the outline: 1528.4 of 1533.5 m². The 5 m² of slivers dropped at the range joints lie under the roofs.
- The prison and all walls lie on the ground patch.
- The Blender geometry checks passed.
- Two rebuilds gave identical meshes.
- Passes 28–84 are unchanged.
- Model renders were compared with both views:
  - The comparison found the Rotunda's pointed roof wrong; it now has a low roof behind a cornice.
  - The user panorama's position is not known precisely, so that comparison shows only the arrangement of the ranges.
- The Unreal import and its checks are deferred.

## Limitations

- **Estimates:**
  - all heights;
  - the opening grid, which is generic for three storeys;
  - the ground level.
- **Ground:** only the patch round the prison is modelled. The rest of the mainland is not.
- **Omitted:** the yard's interior buildings and security details.

## Corrected in pass 103

The prison building of this pass (`SM_Prison85_Anstalten`) was rebuilt in pass 103 as the cross-shaped cell prison that satellite imagery and the winter photograph show. The boxed hipped roofs here overlapped, and the walls and windows were generic. See `references/block103-notes.md`.
