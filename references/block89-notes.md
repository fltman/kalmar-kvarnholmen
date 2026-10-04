# Pass 89: the south side of east Storgatan (nr 60–64 and the two lots east of them)

Pass 89 replaces five generic district volumes from pass 17 with the houses that stand on the south side of Storgatan between x 202 and x 265. Each volume is one house, so each is one zone. West to east:

- **91928538 (Storgatan 60):** a pale green rendered two-storey house with six bays. It has a grey-green panelled double door, a carriage gateway with a fanlight at the west end, a storey band, panels under the upper windows, and a dark tiled hip roof with two roof lights and a chimney.
- **91928591 (Storgatan 62):** a yellow vertical-boarded two-storey house. White pilasters stand at the corners and either side of the middle bays. There are four windows a floor, and the ground-floor ones have small gabled crowns. A pediment with a lunette stands over the middle bays, under a low grey metal saddle roof.
- **91928561 (Storgatan 64):** a long pale yellow rendered two-storey house on a dark plinth, with eight bays. It has a brown door on steps in the middle and a storey band. The red tiled saddle roof carries two red dormers. Both gables are ochre render, and the east one has two windows and a lunette.
- **91928583:** a small green boarded house with its gable to the street and two cream-framed windows a floor.
- **91928590:** a green boarded wall with a black double gate, and a low red metal shed roof behind it.

Two small street-front pieces are added to the neighbouring meshes, although they lie outside the OSM outlines:
- the yellow boarded fence in the 1.4 m gap between 62 and 64, in the mesh of 62;
- the low yellow boarded gateway with red-panelled double doors in the 3 m gap between 64 and the green house, in the mesh of 64. It is a front wall with a narrow tiled lean-to behind it.

The stepped-gable stucco shop east of the gate (91928597) is not touched. In the sandbox it still carries `detail_pass` 17.

Panoramas are working references only. No pixel is used as a texture.

## Measurement

Five panoramas from April 2025 were used, all at heading 152 (looking south at the fronts), pitch 15 and a vertical field of view of 90.

| Panorama | Where | Google position | Resected position | Camera height |
|---|---|---|---|---|
| sRnC-HF-aJquBydtqHus4A | Storgatan 60 | (210.76, −2.41) | (208.69, −3.56) | 2.4 m |
| 5jsHZ4H5LgklWdsRh36RNw | Storgatan 62 | (221.04, −2.54) | (219.15, −3.10) | 2.4 m |
| u611VtYYWxCgDN1Ae7e86w | Storgatan 64 | (241.18, −2.85) | (239.36, −3.71) | 2.4 m |
| RtCz5AnpW9Ih62WNRWQ8-g | green house and gate | (261.21, −2.95) | (260.1, −2.8), see below | 2.4 m (assumed) |
| 6hF44bWMAmz8ho823D5heQ | Storgatan 68 (shop) | (271.26, −2.92) | (269.68, −4.4) | only horizontal readings used |

**Resection.**
- The panoramas at 60, 62 and 64 were each resected on the two front corners of their house (OSM vertices), read at the storey-band height.
- In each, the pavement line at the facade then reads 2.4 m below the camera, so 2.4 m was taken as the camera height.
- Check on 64: the door reads 2.3 m high on steps 0.8 m high.
- The resected positions lie 1.2–2.1 m west of and 0.6–1.2 m south of the reported ones.
- **The green-house panorama does not resect cleanly.** Four corners (the shop's west pilaster, both corners of the green house and the east corner of 64) leave residuals of about 20 px.
  - The two green-house corners alone put the camera at (260.45, −1.5). There the pavement reads 2.8 m below the camera.
  - The camera was therefore taken where the pavement reads 2.4 m below (y −2.8), with x set from the green-house corners: (260.1, −2.8).
  - At that position the green house reads about 5.5 m wide, against 6.4 m in OSM. Its heights are uncertain by about ±10 %.
- **The Storgatan 68 panorama** was resected on the shop's two pilaster edges. It is used only for the gate's position and width, which agree with the green-house panorama to about 0.3 m.

**Eaves.** The eaves were read at the gutter line on the facade plane. The gutters stand about 0.5 m in front of the wall, so the modelled eaves are 0.2–0.3 m below those readings: 6.15 for 60 (read 6.35) and 7.1 for 64 (read 7.35). The first sandbox comparison showed the eaves too high with the raw readings.

**Ridges.**
- The roof crest seen over the eaves was taken to be the ridge at mid-depth. This gives 10.6 m for 60 (pitch about 44°) and 13.8 m for 64 (about 47°).
- The east gable apex of 64, read on the green-house panorama, gives 12.2–12.9 m. That panorama resects poorly, so the frontal reading was kept.

All values are in metres above the pavement; "s" is the distance from the front's east corner.

| House | Measured | Estimated |
|---|---|---|
| 60 | eaves 6.15 (gutter); storey band 3.3; upper windows s 1.75, 3.56, 5.96, 8.23, 9.97, 12.61, from 3.93 to 5.3; ground windows s 1.77, 3.52, 8.24, 10.0, from 1.35 to 2.8; door s 5.85, 0.5 to 2.8; gateway s 11.4–13.9, to 2.8 | ridge 10.6 (from the crest); window widths 0.95; roof lights and chimney positions |
| 62 | eaves 6.0 (frieze top 6.13); upper windows s 2.0, 4.37, 6.74, 9.13, from 3.85 to 5.25; ground windows same s, from 1.05 to 2.6; pilasters s 3.36 and 7.98; pediment s 3.8–8.2 (modelled 4.4 wide at s 5.67), apex 7.5 | ridge 8.2; the roof over the pediment |
| 64 | eaves 7.1 (gutter); storey band 3.8; upper windows s 2.21, 4.45, 6.87, 8.79, 11.14, 13.79, 16.35, 18.92, from 4.48 to 6.25; ground windows s 2.34, 4.5, 6.83, 8.86, 13.79, 16.41, 19.01, from 1.25 to 3.0; door s 11.1, 0.8 to 3.1; dormers s 5.6 and 15.6 | ridge 13.8 (from the crest); plinth 0.9; dormer size; east-gable windows (heights from the poorly resected panorama, positions made symmetric); the west gable is plain |
| Green house (91928583) | windows s 1.75 and 3.85; ground windows 1.0 to 2.4; upper windows 3.4 to 4.55; eaves 4.1; apex 6.2 | modelled wall height 4.3 and ridge 6.3, so that the upper windows fit under the wall top; ±10 % on all heights (see above) |
| Wall and gate (91928590) | gate s 3.2–5.9, top 2.4; wall top 2.9 | the shed roof behind (flat, red metal) |
| Fence and gateway in the gaps | – | all sizes (fence 2.6 high; gateway 3.1 high, doors 2.2 × 2.6) |

**Colours** were matched by eye to the photographs, as flat target colours on the town textures.

## Verification

- **Zones** (`previews/block89-zones.json`): the five zones cover the outlines exactly: 617.5 m², no area outside OSM, none unzoned and no overlap.
- **Sandbox:** three sandbox runs, each ending with SANDBOX_DONE and no errors. Renders from the resected cameras were put side by side with the panoramas (`cmp_r60`, `cmp_r62`, `cmp_r64`, `cmp_r90`).
  - The first comparison showed the eaves too high and almost no roof visible over 64. The eaves were lowered to the gutter readings, and the ridge of 64 was raised from 13.0 to 13.8.
  - The first comparison also showed a glazed door on 60, where the real door is panelled. It is fixed.
  - The green house came out too large and too low against the photograph from the panorama's reported position. Its camera and heights were re-read.
  - In the final renders, the window rows, storey bands, door, gateway, pediment, dormers and gate line up with the photographs to within a few pixels on 60, 62 and 64, and to about 10–15 px on the green house.
- **The official build, the Blender geometry checks and the Unreal checks are pending.** The lead fills in their results.

## Limitations

- **The green house and the gate** come from one poorly resecting panorama, so their heights carry about ±10 %. The visible front of the green house also seems narrower than its OSM outline (about 5.5 m against 6.4 m).
- **The roof of 64** is still a little lower in the comparison than in the photograph. The ridge is a crest reading that assumes the ridge lies at mid-depth.
- **Walls not facing the street** carry generic windows, and the ochre colour of the gables of 64 is extended down their full height.
- **The fence and the gateway in the gaps** lie outside the OSM outlines and are not covered by the zone checks.
- **Omitted:** signs, house numbers, lamps, downpipes, the gate fanlight's tracery and the cars.

## Official build

The lead's build of pass 89 passed the Blender geometry checks, two rebuilds gave identical meshes, and passes 28–88 are unchanged. Before the export, faces with no area, a repeated corner or a width under 0.1 mm are removed (the tangent export rejected one such sliver in no. 64's roof). The Unreal import and its checks are deferred.
