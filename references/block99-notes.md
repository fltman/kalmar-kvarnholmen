# Pass 99: the townhouse row on north Landshövdingegatan

Pass 99 replaces four generic district volumes from pass 17 on the west side of north Landshövdingegatan with the row of red boarded two-storey townhouses that stands there. Each house turns its gable east to the street, towards the water. One parameterised house is built per OSM outline, with each house's own measured window and door positions.

Common to all four:

- falu-red vertical boarding on a dark plinth (0.55 m), white corner boards where the houses meet;
- a dark saddle roof running back from the street, eaves 6.80 m, ridge 8.80 m (pitch about 28°), dark verge boards and gutters;
- on the south half of the front, a wide four-light window in each storey; on the north half, a two-light upper window over the entrance;
- the door on a threshold 0.65 m up, with four steps and a black handrail, under a small gabled porch roof (3.0 m wide, 1.15 m deep) with a red boarded gable triangle, white verge boards and white brackets.

Per house, south to north:

- **90859885:** wider windows (3.0 m), an oak door, a red tile porch roof, and a white vertical board between the upper windows (read in the photo; its purpose is unknown).
- **90859837:** a light wood door, a dark porch roof.
- **90859849:** a white door with a glazed side light on its south side, a brown porch roof.
- **90859898:** a dark brown door, a brown porch roof.

Mesh names (unchanged from district17): `SM_Kvarnholmen_House_90859885`, `_90859837`, `_90859849`, `_90859898`. Panoramas are working references only. No pixel is used as a texture.

## Measurement

Two panoramas, heading 245, pitch 15, vfov 90, 696×375.

| Panorama | Reported position | Resected position | Camera height |
|---|---|---|---|
| MZ5yNPozU4kvW800QKOMwg (opposite 90859837) | (304.82, 114.33) | (304.36, 112.65) | 2.30 m |
| oOGVHQBEwg6qBgDnTy0uUQ (opposite 90859898) | (305.17, 124.26) | (304.80, 122.37) | 2.30 m |

**Resection.** Each camera was solved by least squares from the bearings of four gable boundaries (the eave corners where neighbouring gables meet, and the row's south and north ends) on the facade plane 0.355 m outside the OSM front line. After resection the boundaries reproject within about 1–7 px of the photo at the eaves. Both cameras sit about 1.7–1.9 m south of, and 0.4 m nearer the houses than, Google's reported positions.

**Camera height and scale.** A camera height of 2.30 m puts the pavement in front of 90859898 at −0.1 m and gives door leaves of 2.1–2.2 m (threshold to head, both panoramas), which is the scale check. With 2.4 m the pavement lands at 0.0 and every height rises 0.1 m; the difference is inside the reading error.

**Values read on the facade plane** (m; s from each house's south end of the OSM front):

| | 90859885 | 90859837 | 90859849 | 90859898 |
|---|---|---|---|---|
| wide windows, s | 0.8–4.0 | 0.95–3.7 | 0.45–3.3 (two views) | 0.6–3.25 |
| upper small window, s | 4.85–6.6 | 5.0–6.4 | 4.4–6.05 | 4.6–5.95 |
| door, s | 4.7–6.7 (frame) | 5.35–6.3 | 4.45–6.1 (with side light) | 5.0–5.9 |
| porch ridge centre, s | 6.0 | 6.2 | 4.9 / 5.6 | 5.85 |

Heights, common to the row (spread over all readings about ±0.05 m): ground windows 1.97–3.40, upper windows 4.47–5.90, door threshold 0.63–0.77, door head 2.62–2.88, porch eaves 2.8–2.95 and ridge 3.7–3.9 (read on planes 1.0–1.3 m in front of the wall), gable eave corners 6.9–7.0 and ridges 8.7–8.9 on the facade plane. The eave and ridge readings are on the rake boards, which stand forward of the plane and read 0.1–0.2 m high from a low camera; eaves 6.80 and ridge 8.80 are used.

## Estimated

- The windows on 90859885 were read at about 45° and may be 10–15% too wide.
- Porch width (3.0 m) and depth (1.15 m): the porch stands forward of the wall, so its corners read too wide on the facade plane; chosen to match the renders.
- Window light division (four and two lights, no transoms), plinth height, step count, colours (sampled in shade, set to falu red).
- The rear (west) walls and the two end walls are not seen; they carry pass 26's plain casements in two storeys. The roofs are assumed to run unbroken to the back of each outline.
- Two chimney-like objects seen above the roofs did not triangulate onto these roofs (the rays pass above them), so they probably stand further back; no chimneys are modelled.

## Verification

- Zones (`previews/block99-zones.json`): one zone per house, footprint 437.4 m², zoned 437.4 m², 0.0 m² outside OSM, 0.0 m² not zoned, no overlap; `BLOCK99_ZONES_OK`.
- Sandbox (prelude: rebuild chain of pass 95) ran twice without errors (`SANDBOX_DONE`), with renders from both resected cameras at the photo size and two obliques. The first comparison matched the gable boundaries, eaves, ridges and openings; the second widened the porch roofs (2.7 → 3.0 m) and moved 90859849's side light to the south side of its door, as in the photo.
- `drop_degenerate_faces99` (with the `_thin` test) runs after `s21_finish` on each house and removes 19 faces per house in the sandbox. All have an area of 8e-5 m² or less, at the porch rods, the gutter ends and the ridge; nothing visible is lost.
- The official build, its geometry checks and the Unreal checks are pending; the lead fills in the build results.

## Limitations

- Only two views, both from the street at a near-frontal heading; the rear and the end walls are not seen.
- Porch roof colours vary between the two panoramas under different light, so the per-house porch colours are uncertain.
- Omitted: antennas, the satellite dish, the heat pump, house numbers, lamps, letter boxes, bins, planting and the fence south of the row.

## Official build

The lead's build of pass 99 passed the Blender geometry checks, two rebuilds gave identical meshes, and passes 28–98 are unchanged. The Unreal import and its checks are deferred.
