# Pass 53: Ölandsgatan 8 and the wooden house

Pass 53 details two district volumes on the south side of Ölandsgatan, west of pass 52:

- **Ölandsgatan 8** (91856590), three storeys:
  - a sandstone-clad ground floor with three shop windows and a portal (oak double doors with sidelights under a panel with the number);
  - a band over the ground floor;
  - two storeys of white casements in flat surrounds;
  - rusticated sandstone quoins at both ends, and a cornice at 11.3 m;
  - a low sheet roof, with a lantern with two windows set back on it.
- **The pale yellow wooden house** (91856614), two storeys:
  - vertical boarding between six white pilasters;
  - five upper and four ground-floor casements;
  - a panelled double door up three steps in the middle;
  - a cornice, a tile roof and a slate-hung dormer.

The meshes keep their names (`SM_Kvarnholmen_House_91856590`, `…_91856614`).

Panoramas are working references only. No pixel is used as a texture, and no panorama, depth or tile data was extracted.

## Sources

- **Outlines:** `source/block53.json`, one zone per house. The green house of pass 52 counts as a 6.3 m neighbour.
- **Google Street View**, April 2025, 90° vertical field of view (1372 × 871 frames):
  - two panoramas facing the houses;
  - one view tilted up 35° for Ölandsgatan 8's cornice and lantern.

  The review cameras are 305 (number 8) and 306 (wooden house); 307 is an aerial view.

## Measurement

**Registration.** The two panoramas are chained on nine shared edges (the wooden house's windows, number 8's west window, the joint). Pairs agree within 0.3 m.

The scale is ambiguous, and the two readings give:

| Reading | Camera height | Panoramas apart | Consequence |
|---|---|---|---|
| Anchored on the wooden house's OSM corners | 1.86 m over the pavement | 8.3 m | fits OSM exactly |
| Spaced as the panoramas' GPS positions | 2.38 m | 10.5 m | consistent with pass 52; puts number 8's east quoin at -223.1 (OSM -223.8), but the wooden house comes out 12.8 m wide against 10.0 m in OSM |

The model takes number 8 from the GPS-spaced reading, mapped onto its OSM joints (a 5 % stretch). It takes the wooden house from the reading anchored on its own corners, which keeps its proportions in its OSM width. The wooden house's heights may therefore be up to about 25 % low if OSM is too narrow.

| Feature | Measured (m) | Modelled (m) |
|---|---|---|
| Number 8 | shop windows 0.46–2.99; portal to 2.99, panel 3.21–3.78; band 3.83–3.97; windows 4.49–6.18 and 7.77–9.34; cornice 10.47–11.31; lantern about 1.5 m back, windows about 11.3–11.7 on the facade plane | the same, lantern 11.3–13.0 |
| Wooden house | ground windows 1.25–2.26; upper 3.27–4.33; door 0.88–2.36; plinth 0.51; cornice 5.21–5.65; dormer window 5.43–6.32 on the facade plane | the same, ridge 8.3 |

## Verification

See `previews/block53-delivery.json`:
- every report passed;
- 72,230 triangles in two meshes;
- identical on two rebuilds;
- 40 floor samples and 37 capsule sweeps, no obstructions;
- calibration of 13 features: median 6 px, largest 12 px;
- passes 28–52 unchanged.

## Limitations

- **The scale ambiguity** is described above.
- **Number 8's east end** (x -223.8 to about -226) is not in these panoramas. Its first ground-floor window and axis follow the rhythm.
- **Estimates:** the rear ranges and the roofs.
- **Omitted:** the shop signs, the letter boards and the house plates.
