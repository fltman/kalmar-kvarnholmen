# Pass 52: Ölandsgatan's south side west of Kaggensgatan

Pass 52 details two district volumes on the south side of Ölandsgatan, west of the Kaggensgatan crossing:

- **The cream corner house** (91856606):
  - to Ölandsgatan, three tall shop windows and a glazed door under four red-framed casements;
  - white corner pilasters with capitals at the eaves (10.25 m);
  - a steep street gable with two small windows, rising to about 13.4 m, under a hipped top.

  Its long side on Kaggensgatan (shops under awnings, upper windows, dormers) was seen only obliquely from the crossing, because the pedestrian street has no Street View coverage. It keeps a plain rhythm.
- **The grey-white house with green windows** (91856592), 17.6 m long:
  - five shop windows and a green door, with five casements in flat surrounds above;
  - a pilaster strip and a cornice at 6.3 m;
  - a tile roof with two roof lights.

The meshes keep their names (`SM_Kvarnholmen_House_91856606`, `…_91856592`).

Panoramas are working references only. No pixel is used as a texture, and no panorama, depth or tile data was extracted.

## Sources

- **Outlines:** `source/block52.json`, one zone per house.
- **Google Street View**, April 2025, 90° vertical field of view (1372 × 871 frames):
  - "5 Ölandsgatan", facing the corner house;
  - "3 Ölandsgatan", facing the west end of the green house;
  - a view tilted up 35° for the corner house's gable;
  - an oblique view from the crossing.

  The review cameras are 302 (corner) and 303 (green house); 304 is an aerial view. A user-contributed photosphere at the crossing was not used.

## Measurement

**Registration.** The two panoramas share no edge, so each is anchored on the houses' own corners and joints:
- the Kaggensgatan corner (x -194.94);
- the joint between the two houses (-206.24);
- the joint with Ölandsgatan 8 (-223.80);
- the facade foot.

Anchor residuals are 0.03–0.14 m. The camera height comes out at 2.64 m, higher than the usual 2.2–2.4 m, so heights may read up to about 0.2 m high.

| Feature | Measured (m) | Modelled (m) |
|---|---|---|
| Corner house | shop windows 0.75–4.14; door 0.2–4.14; upper windows 6.37–8.37; plinth 0.45; eaves (pilaster capitals) 10.25; street gable to about 13.4 (on the facade plane), gable windows about 10.35–11.75 | the same, hip to 15.9 (estimate) |
| Green house | shop windows 0.56–2.58; upper 3.6–5.1; door to 2.48; cornice 6.3; roof top about 8.3 on the facade plane | the same, ridge 9.2 |

## Verification

See `previews/block52-delivery.json`:
- every report passed;
- 66,910 triangles in two meshes;
- identical on two rebuilds;
- 72 floor samples and 67 capsule sweeps, no obstructions;
- calibration of 14 features: median 8 px, largest 15 px (the east corner pilaster);
- passes 28–51 unchanged.

## Limitations

- **The Kaggensgatan side** of the corner house is a plain estimate.
- **Estimates:**
  - the green house's hidden middle axis (about x -214.9);
  - both roofs;
  - the rear wings.
- **Omitted:** the shop signs, the posters, the parking sign and the awnings on Kaggensgatan.
