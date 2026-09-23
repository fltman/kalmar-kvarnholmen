# Kalmar C station house — pass 24

Research date: 2026-09-23. Exterior model of the station house (OSM ways 90965009 "Centralstation" and 90965025) replacing the district-17 generic volumes. Photographs and panoramas are working references only: no pixel is used as a texture. Street View was viewed in the browser; no panorama, depth or 3D data was extracted from Google.

## History used for interpretation

- [Kalmar centralstation, Swedish Wikipedia](https://sv.wikipedia.org/wiki/Kalmar_centralstation): the lower western range was built in 1874 to designs by Hjalmar Kumlien; the taller eastern block was added in 1910. Both are rendered pale yellow. The dates 1874 and 1910 are inscribed on the street front (visible in the photographs) and are lettered in the model.

## Photographs (Wikimedia Commons, stored in `references/station24/`, licences in `sources.json`)

| File | Author, date, licence | Used for |
|---|---|---|
| kalmar-centralstation-2021.jpg | Axel Pettersson, 2021-09-09, CC BY 4.0 | Platform front: 9-axis range, 7-axis block, blue awnings, station name board, canopy, south wing with dormer |
| kalmar-centralstation-maj-2022.jpg | Johannes Scherman, 2022-05-27, CC BY-SA 4.0 | Street front, tower, clock gable, lantern, copper roof with dormers and chimneys |
| stationshuset-kalmar.jpg | Klingens Järnvägar, 2020-05-01, CC BY-SA 4.0 | Street front in diffuse light, window surrounds |
| kalmar-station-20250710-04.jpg | AleWi, 2025-07-10, CC BY-SA 4.0 | Track side from across the water: roof forms, canopy length |
| kalmar-20250715-08.jpg | AleWi, 2025-07-15, CC BY-SA 4.0 | North-west end and canopy along the platform |
| others in the folder | see `sources.json` | Cross-checks only |

## Street View panoramas actually viewed

- 5 Stationsgatan, April 2025, pano `GKJn2KWTlp7KkTQ2oKAFSA` (56.6618287, 16.3603163), headings 190 and 205.
- 5 Stationsgatan east corner, April 2025, pano `9PMYu4pLL4fCbRD_U_Nf9Q` (56.661716, 16.3606067), heading 240.
- Platform crossing at the north-west end, user photosphere by Jan Kivisaar, April 2015 (56.6614452, 16.3596884): canopy and track front; not used for measurement.

## Orthophoto

Esri World Imagery tiles (zoom 19) reprojected into the project frame: copper roof with dormers and stacks, the pyramid roof with its lantern, the round tower, the small hipped south wing and the canopy strip along the platform. Imagery © Esri and its providers; visual reference only, not stored in the repository.

## Measurement by inverting the panorama camera

Street View screenshots were taken at a 50° vertical field of view in a 1512 × 812 viewport. For a pixel, the viewing ray from the pano position (car camera 2.5 m above ground, heading and pitch as set) was intersected with a vertical plane at the depth of the feature. The base of the 1910 front comes out at 0.07 m, which validates the camera. Results:

| Feature | Height (m) | Note |
|---|---|---|
| 1910 ground-floor sills / arch tops | 1.35 / 4.10 | |
| 1910 first-floor windows | 5.75–7.96 | |
| 1910 second-floor windows | 9.60–11.66 | |
| 1910 cornice (outer edge) | 13.0 | 0.78 m projection accounted for |
| attic lights / clock centre | 14.7 / 15.3 | |
| roof break (steep band to upper pyramid) | 16.1 | at a 1.6 m inset |
| lantern base / body top | 20.9 / 22.3 | |
| tower body / slate drum top | 9.4 / 11.5 | |

The model was then rendered from the same camera at the same resolution and compared pixel for pixel. Cornice, clock, attic lights, lantern and all window rows of the 1910 block agree within about 5 px; the 1874 range, its nine axes, its door, dormers and north-west gable agree after the change below.

**The 1874 range is longer than mapped.** Two independent panoramas (headings 190/205 from one pano, 240 from another) place its north-west gable 1.4–1.7 m beyond the OSM outline; the gable is moved out by 1.6 m (21.6 m² outside OSM). The regular tower circle adds 1.2 m².

The 240° view sits about 15 px higher and 10 px further left than the model over the whole frame, including the 1874 range that matches the other view. This is consistent with a tilt of about 1° in that panorama's own orientation and is not treated as a geometric error.

**Comparison images in pass 23 were resampled.** During this pass it was found that the pass-23 comparisons scaled the 1512 × 812 screenshots to 1500 × 750 (and 2000 × 1000), which stretches the photograph 7.4 % horizontally. Heights are unaffected. Horizontal extents read from those images (the pale box width, the cinema and south mansard bearings) can be off by up to about 1 m at the frame edges. From this pass on, renders are made at the screenshot's own resolution.

## Zones and interpretation

`scripts/prepare_station24.py` (Shapely) writes `source/station24.json`: the 1874 range, the 1910 block, the round corner tower (least-squares circle through the mapped bulge, radius 2.95 m) and the south wing; walls are exposed only above lower neighbours.

- 1874 range: two storeys, eave 9.3 m, nine axes per long front in three groups with pilasters, round-arched ground floor, corniced upper windows, hipped copper roof with standing seams, two round-headed dormers to the street, a box dormer to the platform, two pairs of stacks. The platform-side doors (first, middle and last axis) follow the 2021 photograph only approximately.
- 1910 block: three storeys, seven axes each side, lugged first-floor architraves, dentil cornice, steep lower roof band with attic lights and clock gables to street and platform, upper pyramid in rhombic slate, octagonal lantern with copper cap. The north-west and south-east roof sides are not photographed closely.
- Tower: rendered drum with door, oval light and round-headed windows, slate-hung upper drum with dormers, bell roof and spire; the spire top (19.5 m) and the weathervane are estimated from the 2022 photograph.
- South wing: two storeys, eave 10.2 m, hipped roof with one dormer to the platform; its heights are estimated from the 2021 photograph, not measured.
- Platform canopy: steel columns, deep fascia, light soffit, 4.3 m deep along the 1874 range from 1.2 m past its north-west end; the end conditions are interpreted.

Omitted: tenant signs and the restaurant's awnings and kiosk porch on the street front, flag poles, lamp standards, the locomotive wheel, platform furniture, interiors.

## Materials

New `M_Station24_*` materials tint project texture sets towards colours sampled from the photographs (tints computed against each texture's measured mean colour in linear space). One new original texture: `T_Station24Slate_*` (`scripts/make_station24_textures.py`), rhombic slates 0.40 m on the diagonal, 4 m repeat, OpenGL normals.

## Licences

Mapped footprints: © OpenStreetMap contributors, ODbL. Commons photographs keep their licences (see `sources.json`); they are not redistributed with the public edition. Authored geometry and textures follow the project licence (CC BY 4.0, code MIT).
