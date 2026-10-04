# Pass 75: the corner of Proviantgatan and Norra Långgatan

Pass 75 details the district volume 93192446 on the corner of Proviantgatan and Norra Långgatan. It is split at measured joints into four houses:
- **The last metre of the narrow white house** with the red door. The rest of it is in pass 74.
- **Number 20**, a cream three-storey house on Proviantgatan:
  - a rusticated ground floor over a granite plinth with vents;
  - the red door with its fanlight, in a dark stone surround up four steps;
  - a band, and five axes of dark green casements in white surrounds;
  - hoods over the first floor, a cornice and a dark mansard with dormers.
- **Number 22**, the light ochre corner house: two storeys with white corner strips, white-framed windows on both fronts, the red door (22) in a stone surround on Proviantgatan, and a hipped roof with a dormer.
- **The dark ochre roughcast range** on Norra Långgatan: dark-framed windows (two small ones in the middle), a blue-grey plinth, a white cornice, and six large red boarded wall dormers on a low dark roof.

The mesh keeps its name (`SM_Kvarnholmen_House_93192446`). The signs, lamps and letterbox are omitted.

Panoramas are working references only. No pixel is used as a texture, and no panorama, depth or tile data was extracted.

## Measurement

- **Number 20** is read from the pass 70 panorama facing it ("20 Proviantgatan"). On the district outline its base row lies at 0 with a camera 2.3 m high, and its joints lie at y 37.53 and 49.53.
- **The western panorama on Norra Långgatan** ("54") is resected on the corner house's west corner and on its base row. Its height is ambiguous along the corner ray; a 2.3 m camera puts it on its reported position.
- **The eastern panorama** ("61") is resected on the range's east end (x 222.74) and on the corner. It then predicts the joint between the range and the corner house within 3 px, and puts its base row at 0.

| House | Feature | Modelled (m) |
|---|---|---|
| Number 20 | window axes (y) | 48.23, 45.8, 43.3 (upper floors), 40.84, 38.4; door 43.47 |
| Number 20 | heights | plinth 0–0.92; ground windows 1.97–3.86; band 4.75–5.45; first floor 5.45–7.42; second floor 9.01–10.81; cornice to 12.9 |
| Number 22 | Proviantgatan axes (y) | door 50.95; windows 54.07, 56.96, 59.28 (ground floor) and 51.47, 54.13, 57.05, 59.46 (upper) |
| Number 22 | Norra Långgatan axes (x) | 191.4, 195.77 |
| Number 22 | heights | ground windows about 1.4–3.3; upper windows about 4.4–6.5; eaves 7.8 |
| Range | window axes (x) | 220.27, 217.36, 214.9, 211.3, 208.35, 206.1 (small), 203.43, 200.33 |
| Range | heights | ground windows 0.93–2.5; upper windows 3.65–5.25; eaves 6.9 |

The range's floor heights read from the two cameras differ by about 0.35 m, because the street slopes; their mean is used.

The dormers were first drawn as roof dormers, which came out small, with long bodies over the low roof. They are rebuilt as wall dormers with short bodies and gables, and the roof behind them is darkened and lowered, as the panoramas show sky above the eaves between the dormers.

## Verification

See `previews/block75-delivery.json`:
- every report passed;
- identical on two rebuilds;
- 102 floor samples and 96 capsule sweeps, no obstructions;
- calibration of 13 features: median 8 px, largest 16 px;
- passes 28–74 unchanged.

## Limitations

- **Estimates:**
  - number 20's mansard;
  - the corner house's roof;
  - the range's roof;
  - the yard sides.
- **The joint between number 20 and the corner house** lies 0.54 m north of the district outline's corner. The zones follow the measurement.
