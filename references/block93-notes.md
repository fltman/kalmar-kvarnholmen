# Pass 93: the east side of Landshövdingegatan

Pass 93 replaces six generic district volumes from pass 17 on the east side of Landshövdingegatan (fronts face west) with the houses that stand there. They are split into eleven zones.

From south to north:

- **93199599 (3 Landshövdingegatan):** the yellow rendered three-storey corner house with the chamfered corner on the cross street. It has a rusticated ground floor on a granite plinth, light quoins, a storey band, a deep cornice, a red entrance door with a transom in a light surround, and a hipped red sheet roof with two chimneys. Window columns run round the chamfer and along the cross-street front.
- **93238178 (7 Landshövdingegatan):** the taupe rendered two-storey corner house. It has four window columns on the street front with wide white surrounds, a light storey band and plinth, a frieze and a deep cornice, and a low grey sheet roof with a roof hatch. Window columns run along the cross-street front.
- **93238200:** a light grey vertically boarded two-storey house. It has a brown garage door at its south end, a brown door under a small canopy, a ground-floor window above a basement window, three upper windows and a red tile saddle roof. A low annex covers the bump at the back.
- **93238168:** a green-grey boarded two-storey house with a burgundy door and a burgundy garage door, one ground-floor and three upper windows, a dark low saddle roof and two chimneys. A low annex covers the bump at the back.
- **93238182:** a falu-red boarded house in three parts:
  - a gable wing to the street with blue-grey trim and two windows on each floor;
  - a lower piece south of it under a saddle roof along the street;
  - low yard ranges behind under flat roofs.

  The white gate in its own red wall, under a lean-to roof, fills the 2.4 m gap to the green-grey house.
- **93238147:** a brown boarded house with a gambrel gable to the street, on a dark plinth. It has two windows on each floor, window boxes on the ground floor and pale frames. Low yard ranges stand behind it. The burgundy gate in a brown boarded gap wall, under a lean-to roof, fills the 2.1 m gap to the red house.

The two gap walls lie outside the OSM outlines, as on the panoramas. They belong to the meshes of 93238182 and 93238147.

Panoramas are working references only. No pixel is used as a texture.

## Measurement

Four Google Street View panoramas were used, all with heading 62 (looking east), pitch 15 (the `t` value 105) and a vertical field of view of 90°, at 696×375.

| Panorama | Where | Google position (local) | Resected position | Camera height | Resected on |
|---|---|---|---|---|---|
| cgi6hOpcrFUoAgJem1LT9Q | 7 Landshövdingegatan | (301.20, 4.76) | (300.09, 3.50) | 2.43 m (base of the taupe corner) | the two vertical edges of the taupe front (y −0.01 and 9.81); residual ≤ 3.4 px |
| IbAmRQ-_WltMyqBVK3ZZ1g | 12 Landshövdingegatan | (301.21, 26.22) | (299.22, 25.18) | 2.60 m (garage threshold) | the two edges of the green-grey front (y 30.33 and 19.82); residual ≤ 1.2 px |
| HCkjMM5JmNc0GM_gQfvs9A | 16 Landshövdingegatan | (301.73, 47.53) | (300.30, 46.27) | 2.3 m assumed (base hidden by cars; plinth top reads −1.84 m) | the two edges of the gambrel front (y 50.53 and 42.65); residual ≤ 4.2 px |
| u1lWw8hu3K6Mz5n8SNDUbg | 3 Landshövdingegatan | (301.38, −25.09) | (300.0, −26.70) | 2.11 m (bottom of the granite plinth) | one corner only (the quoined SW corner of the yellow house, y −27.69); x is set to 300.0 from the other three cameras |

**Resection.** Each camera position was solved by least squares on the vertical edges of house corners. The facade plane was taken 0.355 m outside the OSM line, and the pitch was fixed at 15°. Freeing the pitch moves it to 11.8–14.8° and changes the heights by up to 10 %, so the reported pitch was kept. All four cameras come out 1.0–1.9 m west of Google's position and 1.0–1.6 m south of it. That puts them on the west half of the street, 6–7 m from the east fronts.

**Which house is which.** The resection settles this:
- On the 7 panorama, the taupe house in the centre is 93238178. The grey-white boarded house with the garage door on the left is 93238200.
- On the 12 panorama, the green-grey house is 93238168. The light grey house on the right is 93238200 again. The red house on the left is 93238182. The white gate stands in the gap between the outlines at y 30.33–32.70.
- On the 16 panorama, the brown gambrel house is 93238147. The red gate stands in the gap at y 40.57–42.65. The red house beyond it is 93238182. The low grey house on the left is 93238210, which is not in this pass.
- On the 3 panorama, the yellow three-storey house is 93199599. Its quoined corner falls on the OSM corner at y −27.69. The taupe three-storey house to the right is the next volume south, 93199672. That one is not in this pass and is left as it was. The pass brief guessed that 93199599 might be the taupe house; it is not.

**Scale conflict.** The 7 and 12 panoramas disagree by about 10 % on the light grey house 93238200, which both of them show:
- The 7 panorama, with a 2.43 m camera, reads its eaves at 6.23 m and its garage door at 2.0 m.
- The 12 panorama, with a 2.60 m camera and seen at a grazing angle, reads the eaves at about 6.9 m. On its own house, 93238168, it reads the doors at 2.34 m.

The 7 panorama is the more consistent one: its doors are of normal height and its camera height is typical. Its scale is used. The heights read on the 12 panorama are multiplied by 0.90. Pass 91 found a similar 15 % conflict on the panoramas next to this street.

**Measured values** (heights above the facade base; the positions of openings are model y on the front line):
- *93199599 (3 panorama):*
  - granite plinth 0.35 m;
  - rusticated ground floor up to the band at 3.9–4.3 m;
  - cornice 9.9–10.6 m, taken as a 10.8 m wall top;
  - window columns at y −25.91, −23.63, −21.31, −18.97 and −16.69, spaced 2.3 m;
  - windows: ground floor 1.20–2.85 m, first floor 4.30–6.05 m, second floor 7.35–8.95 m;
  - the red door under the first column, from 0.45 m to 2.85 m including its transom.
- *93238178 (7 panorama):*
  - plinth 0.5 m;
  - storey band 3.55–3.75 m;
  - cornice underside 6.45 m, cornice top about 7.3–7.5 m (wall top taken as 7.3 m);
  - four window columns at y 1.35, 3.89, 6.27 and 8.19;
  - windows 1.40–3.10 m and 3.85–5.65 m.
- *93238200 (7 panorama):*
  - eaves 6.25 m;
  - garage door at y 11.2, 2.3 m wide and 2.0 m high;
  - upper windows 4.05–5.45 m, at y 11.1 and 14.4.
  The 12 panorama gives the door, the ground-floor window and the basement window, and an upper window at y 17.8. Those were read on a grazing view and shifted by the 1.2 m offset between the two panoramas.
- *93238168 (12 panorama, ×0.90):*
  - eaves 6.2 m;
  - ground-floor window at y 28.15, 1.65–3.05 m;
  - burgundy door at y 24.73, 2.1 m high;
  - garage door at y 21.53, 2.8 m wide and 2.15 m high;
  - upper windows at y 28.16, 24.72 and 21.21, 4.2–5.7 m.
- *93238147 (16 panorama):*
  - side eaves 3.1 m;
  - gambrel knuckles 5.35 m high, 0.95 m in from the wall faces (5.6 m and 5.2 m read on the two sides);
  - ridge 7.4 m, at the middle of the front (read 0.1 m off the middle);
  - ground-floor windows 1.25–2.55 m at y 47.88 and 45.03;
  - attic windows 3.85–5.25 m;
  - the gate in the gap 2.2 m high, and the gap wall's roof edge at about 3.9 m.
- *93238182 (16 panorama, red front plane):*
  - gable apex 6.4–6.7 m at y 37.3, close to the middle of the wing's front (38.0);
  - verge feet 4.5–4.8 m at y 40.0 and 34.6;
  - two windows on each floor, at y 38.42 and 36.87: 1.3–2.7 m and 3.45–4.8 m.
  The 12 panorama sees the piece south of the gable with horizontal eaves at about 4.7 m (scaled).

## Estimated

- **Roofs:**
  - the ridge heights of 93238200 (8.65 m) and 93238168 (7.8 m), and the roof of the red south piece (5.9 m): only the eaves edges are visible;
  - the yellow house's hipped roof (rise 2.6 m with a flat top) and the taupe house's low roof (rise 1.2 m);
  - the chimneys and the roof hatch.
- **The cross-street fronts of 93199599 and 93238178,** including the chamfer: window columns at the street front's spacing, on all storeys. The panoramas only graze them. The yellow house's dormer, seen on the 7 panorama, is not modelled.
- **The south piece of 93238182:** its windows (one per floor at y 34.2) and its roof.
- **The yard ranges** behind 93238182 and 93238147, and the annexes on the back bumps of 93238200 and 93238168: 3.0 m high under flat dark roofs, with plain windows. No photo shows them.
- **Colours** are matched by eye to the panoramas.

## Verification

- **Zone check** (`previews/block93-zones.json`, BLOCK93_ZONES_OK):
  - footprint 780.8 m², zoned 780.4 m²;
  - 0.01 m² outside OSM and 0.41 m² of OSM not zoned (slivers at the cut lines);
  - overlap 0.002 m².
- **Sandbox** (SCR/sandbox.py on a copy of `source/Stortorget.blend`, prelude rebuild_block91):
  - it prints `BLOCK93_GEOMETRY 6` and `SANDBOX_DONE` without errors;
  - `drop_degenerate_faces93` runs on every mesh after `s21_finish`. In the sandbox it removed no faces from the two rendered houses, and 14, 12, 39 and 40 faces from the four boarded ones (93238200, 93238168, 93238182, 93238147). The sample centres lie on eaves and ridge lines, where faces collapse after `s21_finish`.
- **Renders from the resected cameras,** compared side by side with the photographs in `SCR/p93/sb2/cmp_A.jpg` to `cmp_D.jpg`:
  - *taupe house (A):* window columns, storey band and cornice line match within a few pixels. The garage door of 93238200 sits at its place on the left.
  - *green-grey house (B):* door, garage and window positions match. The eaves of 93238168 and 93238200 render about 15 px lower than in the photo. This is the 10 % scale conflict described above, resolved in favour of the 7 panorama.
  - *gambrel house (C):* the gambrel outline, the knuckles, the windows, the gate in the gap and the red gable match within about 10 px. The house on the left is 93238210 (generic, not in this pass), so it does not match the low grey house in the photo.
  - *yellow house (D):* the quoins, the door, the five window columns and all three storey levels match. The first render (sb1) used an unresected camera with the corner 60 px off; it was corrected before sb2.
- The official build and the Unreal checks are pending; the lead fills in the build results.

## Limitations

- The heights rest on the 7 panorama's scale. If the 12 panorama is right, the boarded houses are about 10 % too low.
- The yellow house's camera has only one corner to resect on, and its x is taken from the other three cameras.
- The roofs above the eaves are not visible on any panorama, and nor are the rear and yard elevations.
- 93238210 (north of the gambrel house) and 93199672 (south of the yellow house) are visible on the photos but are outside this pass.
- Gutters, downpipes, signs, the parking sign, the lamp post, the meter boxes, the wall plants, the satellite dishes and the window boxes' plants are omitted.
- The yellow house's dormer is not modelled.

## Official build

The lead's build of pass 93 passed the Blender geometry checks, two rebuilds gave identical meshes, and passes 28–92 are unchanged. The Unreal import and its checks are deferred.
