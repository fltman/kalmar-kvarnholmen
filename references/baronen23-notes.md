# Baronen shopping centre — pass 23

Research date: 2026-09-23. Exterior model of Baronens köpcentrum (OSM way 38033725) at Skeppsbron / Ölandshamnen, replacing the district-17 generic block. Reference pixels are working references only: no photograph or panorama is used as a texture, and none is redistributed. Street View was viewed in the browser; no panorama, depth or 3D data was extracted from Google.

## History used for interpretation

- [Kalmar läns museum, *Älskade Kvarnholmen: Baronen*](http://kvarnholmen.kalmarlansmuseum.se/baronen) (page and photograph, museum 2015). Kalmar Stormarknad opened in summer 1964 in the former Svea margarine factory at Ölandshamnen; the factory closed in 1962. Enlarged after 1972, when neighbouring properties were incorporated; renamed Baronen Köpcenter in 1977. The photograph shows the north side from Skeppsbrogatan: brick factory, glazed octagonal entrance tower, the rendered mansard house.
- [Baronen Köpcenter, *Om Baronen*](https://baronenkalmar.se/baronen/). Two public floors: plan 1 (quay level, Restaurang Bryggan) and plan 2.
- [Home Hotel Packhuset](https://www.strawberry.se/hotell/sverige/kalmar/home-hotel-packhuset/), exterior entrance photograph. An eighteenth-century warehouse converted to a hotel in the mid-1980s; cream coarse render, red barrel dormers, white metal entrance box beside the brick factory.

## Street View panoramas actually viewed

- 11 Skeppsbrogatan, April 2025, heading 150 (pano `WbxTZuyf9BbcQ7MoQCq_PQ`): entrance plaza, octagon, H&M glass link, mansard house and the brick factory's west end.
- 4 Skeppsbrogatan, April 2025: the mansard house's full north front, canopy on white columns, arched shop windows.
- Skeppsbron, April 2025, headings 168–200 (panos `lEd9yxhLie-MD6m1Q9yUYA`, `1YA5fX20RQ9eW1Q-LUnXnA`, `Im_EZVPNpGcrlodkYkG82A`): brick factory north and north-east fronts, arched corbel frieze, dog-tooth course, the three-storey cream Packhuset block.
- 1 Stuvaregatan across the basin, April 2025, headings 352–18 (pano `m3YlwKG5Taemy7ZihtIgQw`): the whole harbour side — gym end, south mansard wing, red cinema wall, pale box, single-storey quay shops with the parking deck and railing, Bryggan.
- Ölandskajen, September 2021 (panos `xTbOFeiNycf4zAQNldRuzw`, `O3m4nT5p5LG0TgzoU5-4AA`): glass pavilion, gym box with profiled cladding, red mesh screens, the garage ramp portal and the external stair.
- Business panorama of Restaurang Bryggan (VR Media International AB, June 2024): terracotta and white profiled cladding with portholes, glazed terrace, deck railing overhead.

## Orthophoto

Esri World Imagery tiles (zoom 19) were reprojected into the project frame (28.2° rotation, WGS84 origin 56.66412 N, 16.36560 E) and overlaid with the OSM outline to read the roof plan: the octagon's roof and radial ribs, the glazed dome (centre −187.6, −300.4; radius 4.2 m), the dormer rows, the two red-tiled Packhuset wings, the parking deck with bays and two roof structures, and the flat mall roofs. Imagery © Esri and its providers; used only as a visual reference, not stored in the repository.

## Calibration against the panoramas

Four panoramas were matched with model renders from the same position, heading, pitch and 50° vertical field of view (Blender Workbench, 1500 × 750). Comparisons, measured in image pixels:

| View | Checked | Result |
|---|---|---|
| Entrance, heading 150 | Octagon width and glass height; brick window rows and eaves; mansard cornice and window rows | Agree within a few pixels. The first model ended the mansard house at P11; it was extended over the mapped step P11–P12–P13–P14, leaving a 6 m glass link. |
| Packhuset, heading 200 | Brick front width, eaves, three window rows, dog-tooth course | Agree within 2–10 px. Packhuset raised from two to three storeys; eaves lowered to 8.8 m. |
| Harbour, heading 5 | Horizontal extent of every block; heights of gym end, south mansard, cinema wall, box | Box face narrowed from 37 m to 32.4 m (right edge at bearing 44.5°), box raised to 16.5 m; the south mansard wing and the cinema wall were added after this comparison. |
| Ölandskajen 2021 | Gym box and pavilion | Internally inconsistent (some parts too high, others too low), probably camera height or ground level; not used to set heights. |

**Correction found in pass 24.** These comparisons resampled the 1512 × 812 screenshots to 1500 × 750 (Blender) and 2000 × 1000 (Unreal), which stretches the photograph 7.4 % horizontally. Heights and vertical positions are unaffected. Horizontal extents read from the images — the pale box face (32.4 m), the cinema wall reaching 8.5 m past P6 and the south mansard wing ending at P6 — can be off by up to about 1 m at the frame edges. They have not been re-measured.

## Zones and what is interpreted

Zones are produced by `scripts/prepare_baronen23.py` from the OSM outline (Shapely) and stored in `source/baronen23.json`. Exposed wall intervals are computed against neighbouring zone heights, so walls above lower roofs are built only where they are visible.

| Zone | Height (m) | Basis | Remaining uncertainty |
|---|---|---|---|
| Mansard house (Coop), north and west wings | cornice 12.0, top 15.1 | Street View calibration | Rear (courtyard) faces plain; lesene rhythm simplified to every third bay |
| South mansard wing | as above | Harbour panorama, bearings −1.2° to 11.3° | Depth (26 m) inferred; hidden sides plain |
| Octagon | glass 11.3, roof 14.0 | Street View calibration, orthophoto | Regular chamfered square replaces the irregular mapped facets (15.9 m² outside OSM) |
| H&M glass link, glazed slot to the brick gable | 11.0, 7.6 | Street View | The 4 m slot is outside OSM (56 m²); filled because it is glazed in every photograph and roofed in the orthophoto |
| Brick factory (L) | eaves 10.4, ridge 13.6 | Packhuset calibration | Courtyard fronts assumed like the street fronts; dormers simplified |
| Home Hotel Packhuset (L) | eaves 8.8, ridge 12.6 | Packhuset calibration, hotel photograph | Marina front not photographed at street level: window rhythm and dormers inferred from the orthophoto |
| Inner courtyard wing, annex | 9.3 / 6.0 | Orthophoto | Not visible from public streets; render and windows inferred |
| Mall halls, south block, plant | 9.4 / 9.8 / 6.2 | Orthophoto, harbour panorama | Flat roofs; roof plant positions approximate |
| Pale box behind the deck | 16.5 | Harbour calibration | Depth (24 m) inferred |
| Cinema wall (Biostaden, OSM node 475835457) | 16.4 | Harbour calibration | Only the quay face and one side are observed |
| Gym box | 8.8 | Harbour panorama | The 2021 west view suggests ~11 m; not reconciled |
| Quay shops and parking deck | deck 4.6 | Door heights in the harbour panorama | Shop pattern is a generic interpretation; tenant names omitted |
| Glass pavilion (Mister York) | 7.6 | September 2021 panorama bearings | Outside OSM (96 m²) |

The garage ramp (`highway=service`, `tunnel=yes`, `layer=-1`) descends under the gym. The flat terrain cannot go below ground level, so the portal is a dark recess, not a working ramp. The external stair to the deck and the parking deck's vehicle ramp are not modelled.

## Materials

Existing project materials are reused where they fit: `M_Town_TileRed`, `M_Town_Glass`, `M_Street21_Concrete`, `M_Street22_DarkMetal`, `M_Kvarnholmen_Asphalt`, parking paint. Seventeen new `M_Baronen23_*` materials tint texture sets towards colours sampled from the photographs; each tint is computed against the texture's measured mean colour in linear space. Two new original texture sets come from `scripts/make_baronen23_textures.py`: `T_Baronen23Profiled_*`, white trapezoidal cladding (250 mm pitch, 4 m repeat), and `T_Baronen23Brick_*`, orange-red machine brick in cross bond (238 × 65 mm faces, 12 mm joints, 4 m repeat). The first import used the scanned `M_Landmark_BrickRed`; it read too dark and too varied against the photographs and was replaced. OpenGL normals throughout. No reference photograph enters any texture.

## Licences

Mapped footprints: © OpenStreetMap contributors, ODbL. Authored geometry and textures follow the project licence (CC BY 4.0, code MIT). Only the building's own name, BARONEN, is lettered on the octagon; tenant names and logos are omitted.
