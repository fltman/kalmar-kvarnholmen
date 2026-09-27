# Pass 68: the white cottage on Norra Långgatan

Pass 68 details the district volume 91926340 on the south side of Norra Långgatan, west of the corner house on Proviantgatan. It is a white roughcast single-storey cottage:
- a green door with glazed upper panels in a white surround at the east end, and three white casements;
- a dark plinth and a white fascia under the eaves;
- a steep mansard roof of dark weathered tile with three white dormers;
- a rendered chimney with a black cowl.

The yard and side walls keep a plain rhythm. The mesh keeps its name (`SM_Kvarnholmen_House_91926340`). The aerials, the traffic signs and the street lamp are omitted.

Panoramas are working references only. No pixel is used as a texture, and no panorama, depth or tile data was extracted.

## Measurement

One panorama on Norra Långgatan ("55") stands about 6.7 m from the facade. It is resected on both corners of the cottage (x 169.65 and 159.43), and its base row puts the camera 2.15 m high.

| Feature | Measured (m) | Modelled (m) |
|---|---|---|
| Door (x) | 167.51–168.57 | centre 168.04, 1.0 wide |
| Window axes (x) | 166.08, 164.45, 161.47 | the same |
| Dormer axes (x) | 167.55, 164.38, 161.15, 0.6 m in from the wall | the same |
| Heights | plinth 0–0.45; door 0.78–2.46; windows 1.39–2.56; eaves 2.78; dormer windows 3.9–4.95; roof break about 6.1 | the same; upper roof to 6.7 (estimate) |

The district volume stood 6.65 m to the eaves. The cottage is a single storey under its roof.

## Verification

See `previews/block68-delivery.json`:
- every report passed;
- identical on two rebuilds;
- 14 floor samples and 12 capsule sweeps, no obstructions;
- calibration of 6 features: median 8 px, largest 16 px (the chimney);
- passes 28–67 unchanged.

## Limitations

- **One panorama only**, so the roof break is read on a single ray.
- **Estimates:**
  - the upper roof;
  - the chimney height;
  - the yard side.
- **The dormers** have flat hoods in the panorama and are drawn with gabled hoods.
