# Pass 131: Kalmar slott, Gröna salen (room 87) and Förbrända salen (rooms 74 and 76)

Pass 131 builds two more state-floor interiors of Kalmar slott with pass 125's and pass 130's method:
- closed architectural solids at real scale, standing inside pass 27's hollow ranges;
- flat-colour materials on the town textures;
- cameras inside;
- a walk check.

| Mesh | Category | Status | What |
|---|---|---|---|
| `SM_Castle131_GronaSalen` | Kalmar slott/Interiör | new | Gröna salen, the room shell. It has: a wide-board floor; grey-washed beams on a board ceiling, fanning where the courtyard wall bends; eleven rectangular window niches (five on the courtyard, four on the outer front, one plus one blind in the far end wall), each with a parapet, its own window and a painted soffit; the west tower's round wall bulging into the far corner; three pedimented doors (east wall, tower wall, the chapel's west door); a hooded fireplace by the east wall |
| `SM_Castle131_GronaInventarier` | Kalmar slott/Interiör | new | nine funeral escutcheons (begravningsvapen) on rods and poles, two large carved crucifixes (outer wall, far end wall) |
| `SM_Castle131_ForbrandaSalen` | Kalmar slott/Interiör | new | Förbrända salen, the room shell. It has: a wide-board floor; a board ceiling with thin cross battens and a sloping board cove along both long walls; eight tall round-arched window niches (five on the courtyard, three on the outer front), each with a parapet and an arched window; a hooded fireplace on the outer wall; a stone fireplace with a crest panel in the north wall; plank doors in both end walls |

No existing mesh is touched (`CHANGED131` lists only the three new meshes).

## Which range, and where in it

### Olsson's plan, registered to the model

**The plan.** Martin Olsson, *Fornvännen* 69 (1974), fig. 1. It is in copyright. It was read on the DiVA PDF in the scratch directory only (p. 91, rendered at 400 dpi) and is not copied into the project; only pixel readings are kept, in `OLSSON` in `scripts/prepare_block131.py`.

**Registration.** A similarity transform was fitted to the four round towers:

| Olsson's tower | Model tower | Residual |
|---|---|---|
| II Kungsmakstornet | N | 4 px |
| IX Rödkullatornet | W | 9 px |
| VIII Södra tornet | S | 7 px |
| V Fångetornet | E | 12 px |

- The fit gives 11.47 px/m. The plan's own 0–100 m bar reads 11.37 px/m.
- The residuals are 0.35–1.0 m.
- With this fit, the model's outline lies on Olsson's walls all the way round (`SCR/p131/reg_ov.png`).
- Pass 27's two bays on the east range's outer front are Olsson's towers VI (room 75, `bay2`) and VII (room 77, `bay1`).

### Gröna salen (Olsson 87, "Stora västra salen")

Olsson's text puts room 87 in the west range ("nr 87 i västra längan"). The plan puts it between Kuretornet (I/56) and Rödkullatornet (IX/88). In the model, that is pass 27's NW range, between Kuretornet's south face (NW s ≈ 35.9) and the west tower W.

The plan's courtyard wall of 87 bends where the courtyard corner is. Beyond the bend, the room's wall is the chapel's west end wall (86), so 87 runs on into the corner where the south range begins:
- its far end wall is the south range's outer wall;
- tower IX's round wall bulges into its outer corner.

The photographs confirm this. Looking along the room towards the tower (Commons 2017; Olsson's plate of 1929):
- the far end wall has two windows on the courtyard half;
- on the outer side the tower's curved wall carries a pedimented door;
- the 2015 panorama shows the other end wall (east): a pedimented door, a hooded fireplace in the outer corner and three escutcheons.

Registered plan readings (NW frame) are below. They are all ±1 m, because the residuals are 0.35–1.0 m:
- east inner face s 34.2–34.6;
- courtyard face c −16.0 / −16.7;
- outer face c −4.6 / −5.6;
- courtyard windows at s 37.0, 42.9, 47.7 and 52.1;
- outer windows at s 37.9, 41.8, 45.3, 49.1 and 53.4.

### Förbrända salen (Olsson 74 and 76, "Stora östra salen")

On the plan, 74 and 76 are one hall in the east range. It runs between tower VI (75, with the stair 72 at the north end) and tower VII (77/82 at the south end). In the model, that is pass 27's SE_e range between the two bays.
- Registered, its inner faces lie at SE_e s −1.3…−1.6 and 21.2…21.5.
- Its width is 11.1–11.4 m.
- The KMB photograph of 1923 is titled "Rum 74 och 76, Förbrända salen. Interiör mot söder efter restaureringen 1923".

The courtyard outline of SE_e (pass 27's points 3–4–5) is straight but runs 7.9° off the range's fitted axis. The outer outline (points 26–27) runs 0.5° off the courtyard outline. The hall therefore gets its own frame: *a* along the courtyard outline, *b* outwards, with the origin at outline point 26 (bay1's corner).

## Measurement

### Möller, "Calmar slott. Profiler" (1882, PK006-00041, public domain)

**Scale and floor.** Pass 127's 57.97 px/m on the 90-fot bar is used. The floor is Möller's red state-floor line. Rows and columns were read on full-resolution grid crops (`SCR/p131/g87r.png`, `g87l.png`, `g76.png`).

| Value | "Profil genom Unions-salen" (87) | "Profil genom s.k. Brända salen" (76) |
|---|---|---|
| floor row | 7147.5 | 7152.5 |
| inside width | x 5599 / 6248.5: **11.20 m** | x 1592.5 / 2294: **12.10 m** |
| courtyard wall | 1.28 m (x 5525–5599) | 1.44 m (2294–2377.5) |
| outer wall | 1.88 m (6248.5–6357.5) | 1.94 m (1480–1592.5) |
| facade to facade | 14.36 m | 15.48 m |
| ceiling beams, underside | rows 6770/6763: **6.55 m** | row 6792: **6.24 m** |
| ceiling beams, top | row 6748: 6.89 m | row 6775: 6.51 m |
| niche floor | row 7137: 0.17 m | row 7132.5: 0.35 m |
| niche head at the room face | row 6910: 4.10 m (flat) | row 6827.5: **5.60 m** (arched) |
| niche head at the glass | row 6925: 3.84 m | row 6842: 5.35 m |
| glass, sill and head | rows 7072/6925: 1.29 / 3.84 m | rows 7075/6922: 1.34 / 3.98 m |

**Unions-salen.** The section shows a post on the axis with a bolster under the ceiling beams. Neither the 1929 plate nor the modern photographs show it, so it is not built.

**Brända salen.** In 1882 the hall had a loose intermediate floor on posts ("löst, ofullständigt bjälklag"). The 1919 KMB photographs show the timber framing; the 1923 photograph shows the hall cleared.

### Facade windows (the saved scene)

The niches sit on the facade's state-row windows. They were read from `SM_Kalmar_Slott`'s glass (M_Town_Glass) on a copy of `source/Stortorget.blend` saved after pass 129's official build (`SCR/p131/dump131.py`, `dump.json`, clustered by `win.py`). The positions are in the range frames.

| Front | Windows (axis s) | Size |
|---|---|---|
| NW courtyard (Gröna) | 37.67, 41.47, 45.27, 49.07, 52.87 | 1.20 × 3.2 m, z 11.57–14.77 |
| NW outer (Gröna) | 38.32, 42.72, 47.12, 51.52 | 1.15 × 3.2 m |
| SW outer, Gröna's far end wall | 3.69 | 1.15 × 3.2 m |
| SE_e courtyard (Förbrända) | 1.16, 4.93, 9.80, 13.57, 17.33 | 1.19 × 3.2 m |
| SE_e outer (Förbrända) | 3.55, 7.91, 12.28 | 1.14 × 3.2 m |

Also read but not used (they are below the slab or in the roof):
- the lower rows (NW 8.6–9.8, SE_e 7.75–10.05);
- a courtyard dormer on SE_e (z 17.81–19.11);
- the attic windows (z 17.57–18.39).

### What is used

| Value | Source | Status | Model |
|---|---|---|---|
| Floor | pass 125's state floor | taken over | z 10.47, slab from z 10.17 |
| Gröna salen's inside width | Möller | measured | 11.39 / 11.20 / 11.03 m at s 36 / 45 / 53 (the two outlines are 1.3° apart) |
| Gröna's walls | Möller plus half the model's excess (15.01 − 14.36 m) each | fitted | courtyard 1.60 m, outer 2.20 m from the facade |
| Gröna's east face | Kuretornet's rectangle plus its 0.36 m skin and pass 126's stair (vertices to s 35.48) | from the model | s 36.08, a 0.38 m wall lining in front of Kuretornet. The plan has 34.2–34.6 |
| Gröna's far end | pass 130's chapel west wall (SW s 4.92–6.20) and the south range's outer wall | from the model | a lining at SW s 4.60–4.90 in front of the chapel wall; end wall face at SW c −1.60 (1.50 m to the outline) |
| West tower's wall in the room | pass 27's tower (r 5.865) plus its 0.36 m skin | from the model | lining r 6.25–6.45, an arc |
| Gröna's ceiling | Möller | measured | beam underside z 17.04, beams 0.24 × 0.30 m about 0.95 m apart, boards to z 17.42 |
| Beam fan at the far end | photographs 2017, 1929 | estimated | the beams turn by up to 10.6° (to square with the chapel wall) between s 50.5 and 57.5 |
| Gröna's niches | Möller (floor), facade (glass) | measured / from the model | rectangular, 1.65 m wide at the room face (end wall 1.24 m), floor z 10.65, flat head z 14.95 (Möller's 4.10 m is under the facade's glass head, 14.77) |
| Painted niche soffits | photographs | estimated | a grey-green plate with 2 × 3 light fields |
| Förbrända salen's inside width | Möller | measured | **12.10 m** (the plan has 11.1–11.4) |
| Förbrända's walls | Möller plus half the excess (16.57 − 15.48 m) each | fitted | courtyard 1.99 m, outer 2.49 m (at the middle) |
| Förbrända's ends | plan, registered | measured ±1 m | north face a 20.27; south face a −2.47, moved 0.21 m south of the plan so that the first courtyard niche (1.2 m from the courtyard corner) has a pier. Length 22.74 m |
| Förbrända's ceiling | Möller; photographs 1923/2017 | measured / estimated | board underside z 16.82, top z 16.88; thin battens; a 0.85 m cove sloping 0.55 m down to the long walls (photographs) |
| Förbrända's niches | Möller; photograph 1923 | measured | round-arched, 1.90 m wide at the room face, crown z 16.08 (room face) and 15.83 (glass), floor z 10.82 |
| Parapets in the niches | Möller (sill block at the glass) | measured / from the model | the last 0.55–0.60 m of each niche, up to the facade's sill (z 11.57) |
| Fireplaces, doors, escutcheons, crucifixes | photographs | positions estimated from the photographs (±0.5 m), forms simplified | see below |

## What the rooms have

### SM_Castle131_GronaSalen

**Walls.** The walls are cut from the two footprints in the prepare script (Shapely):
- the envelope (the walls' backs, 0.10 m inside pass 27's outline, the linings and the tower arc);
- the room.

The wall ring is split at the room's corners into six pieces: east, courtyard, chapel lining, end, tower arc and outer. Each piece is built in five horizontal bands (slab, under the niche floor, niche floor to door head, door head to niche head, niche head to ceiling top). In each band the niches and doors that are open there are cut out. The prisms' caps are triangulated, and reveal faces get a whiter plaster.

**Top band.** Its vertices take pass 127's roof underside less 0.10 m where that comes lower than the ceiling's top. That happens on 3 vertices at the courtyard wall's back (lowest z 17.17).

**Niches.** Each has:
- a parapet at the back up to the facade's sill;
- a window with frame, mullion, two transoms and small glazing bars, in a pale "daylight" tint (pass 27's glass stands behind it, in the skin);
- the painted soffit.

The last courtyard niche is skewed. Its room face (s 51.63–53.13) stops short of the bend at s 53.31, and its glass end is on the facade window (52.87).

**Far end wall.** It has the facade's window at SW s 3.69. Beside it is a blind niche at 1.55, because the photographs show two windows and the facade has one. Its pane stands 0.15 m short of the wall's back.

**Doors.** All three have a stone surround with an entablature, a triangular pediment and three ball finials (photographs 2015, 2017).
- East door, c −12.3: towards the stair hall and Kuretornet. The leaf is closed.
- Tower door, in the middle of the arc: the leaf is closed.
- Chapel door: opposite pass 130's west door (SW c −4.256, 1.10 × 2.40 m). The opening runs through the lining, and pass 130's own leaf and reveal stand behind it.

**Fireplace by the east wall** (panorama 2015): a plastered breast 1.5 m wide and 0.45 m deep, a pointed hood to 4.3 m, a stone surround and a dark hearth.

### SM_Castle131_GronaInventarier

- **Escutcheons.** Nine funeral escutcheons, as simplified carved cartouches: a painted shield, side scrolls, a helmet, a crest and mantling. Each hangs on an iron rod from the ceiling, with a pole below.
  - Three are on the east wall over the door.
  - Three are on the outer piers (s 36.8, 40.5, 44.9).
  - Three are on the courtyard piers (s 39.6, 43.4, 47.2).
- **Crucifixes.** Two large carved crucifixes:
  - one on the outer pier at s 49.3 (photographs 2015, 2017);
  - one, at 0.78 scale, on the pier between the end wall's windows (2017).

### SM_Castle131_ForbrandaSalen

- **Walls.** Long walls are built as in pass 130's `lwall130`: piers, the slab under each niche, and the arched heads as fans of slabs. End walls are boxes around the doors.
- **Niches.** Each has a parapet up to the facade's sill, and a window with an arched fanlight up to the niche's arch at the glass.
- **Fireplaces.**
  - The hooded fireplace on the outer wall, between the outer niches at SE_e 3.55 and 7.91 (1923 photograph: left wall, facing south): a brick hearth, stone jambs and mantel, and a pointed plastered hood to 4.4 m.
  - The stone fireplace in the north wall with a red crest panel above it (2017 photograph, Commons "Isabelle de Borchgrave exhibition …"): placed on the hall's axis plus 0.8 m, estimated.
- **Doors.** Plank doors, closed, in both end walls near the courtyard side. The 1923 photograph shows the south one right of centre.
- **Floor and ceiling.** Wide boards along the hall. The ceiling as above.

## Cameras

| Camera | Where (frame, position, height over the floor) | Look | Compared with |
|---|---|---|---|
| `710_Block131_Cal_Grona2017` | NW s 38.0, c −13.6, 1.55 m | +s turned 23° to the outer side, pitch 8, vfov 45.6 (Canon 500D, 18 mm, from EXIF) | Commons "Kalmar Castle Museum, Green Hall, 2017-07-30" (PD) |
| `711_Block131_Cal_Grona1929` | NW s 44.5, c −9.8, 1.40 m | +s, pitch 2, vfov 70 (estimated) | DigitaltMuseum 021017090130, Olsson 1929 (PDM) |
| `712_Block131_Cal_Forbranda1923` | hall frame a 19.7, b −8.6, 1.50 m | −a (south), pitch 1, vfov 64 (estimated) | Commons "Kalmar slott - KMB - 16001000022065" (1923, PD) |
| `713_Block131_Cal_Forbranda2017` | hall frame a 0.5, b −11.7, 1.45 m | +a (north) turned 7° outwards, pitch 9, vfov 45.6 (EXIF) | Commons "Medici family, Isabelle de Borchgrave exhibition … 2017-07-30-3" (PD) |
| `714_Block131_Aerial_WestAndEast` | aerial over the courtyard | – | – |

The cameras are placed by eye from the photographs, not resected.

## Verification

### Prepare

`KALMAR_GEO=<pylib> python3 scripts/prepare_block131.py` prints `BLOCK131_PREPARE_OK`. It asserts:
- both envelopes lie inside pass 27's outline and outside the courtyard, the four towers plus 0.36 m, and Kuretornet (both polygons) plus 0.36 m (0.000 m² each);
- no overlap with:
  - pass 125's rooms plus 2.2 m (16.7 m and 31.3 m away);
  - pass 126's stair strip (0.42 m away);
  - pass 130's chapel envelope (touching, 0 m²);
  - each other;
- every niche lies in its own wall piece, clear of the room, of the other pieces, of the doors and of the other niches (0.25 m);
- Förbrända's niches stay 0.4 m from the end walls and 0.6 m from each other, and the hood is clear of them;
- the inside widths agree with Möller (12.10 m; 11.03–11.39 m);
- the roof's underside over each room is more than 0.3 m above the ceiling's top (Gröna min z 18.22 over the room, Förbrända 18.85).

### Sandbox

Three runs were made with `SCR/p131/build_block131_check.py` (it builds twice and runs all checks) and `SCR/p131/sandbox131.py` (pass 130's copy, with the Workbench shadows off). All used prelude 130. Logs: `SCR/p131/log1.txt`–`log3.txt`. All print `SANDBOX_DONE prelude 130` without errors. The numbers below are run 3's, on the final files.

A scratch harness (`SCR/p131/fast.py`) ran the build alone on an empty scene for the design iterations (`f0`, `f1`).

**Change set and repeatability.**
- `CHANGED131 ['SM_Castle131_ForbrandaSalen', 'SM_Castle131_GronaInventarier', 'SM_Castle131_GronaSalen']`.
- `REPEAT131 True`; the second run changes nothing.

**Degenerate faces.**
- `drop_degenerate_faces131` removes 5 faces from Gröna salen (board-strip bevel slivers), 0 from the furnishings and 0 from Förbrända salen.
- Final counts: Gröna 15,736 faces, furnishings 1,918, Förbrända 20,202.

**The bevel problem.** The first version of Gröna salen lost 11,813 of 17,513 faces. The town bevel collapsed to zero width on the whole mesh, because Blender's clamp-overlap limit is global. One bad vertex anywhere stops it everywhere. Three causes were found and removed:
- zero-radius lathe tips on the pediment finials;
- spike vertices left by Shapely where a niche's footprint met the wall face exactly. The footprints now run 0.03 m into the room, and every ring is cleaned of near-straight corners and spikes;
- collinear points from densifying the top band.

**Export frame check.** This uses pass 128/130's wrapper method: the export tail's preparation, the exporter's frame test and a test FBX export.
- 0 invalid loops; 3 of 3 exports succeeded.
- Fallback frames: 366 loops in Gröna salen, 462 in Förbrända salen, 0 in the furnishings.

**Placement.**
- Every vertex of the three meshes lies in its envelope polygon and z range (`EXTENT131`).
  - In run 1, 18 of Förbrända's vertices were reported outside. Twelve lie on the envelope's edge, moved by the 3 mm bevel (the test's tolerance is now 5 mm). Six were real, 5.5 mm out: the outer niches' parapets were square to the hall's frame while the outer wall's back runs 0.5° off it. They now stop 12 mm short of the back. Run 3: 0 outside.
- Every vertex above z 15.5 has the castle roof above it (`ROOFCLEAR131`):
  - Gröna: 998 vertices, max z 17.42;
  - Förbrända: 10,376, max 16.88;
  - furnishings: 372, max 16.99.
- **Intrusions.** No vertex of any other mesh lies inside Gröna's envelope. Inside Förbrända's envelope there are 48 vertices of `SM_Kalmar_Slott`, at a 16.4–16.6, b −15.79, z 15.85–16.24. These are pass 127's courtyard cornice and corner filler by the NE/SE_e courtyard corner. They are 0.05 m inside the courtyard wall's back, in solid wall, not in the room (as pass 130 found at the chapel's corners).
- **Niches against the facade glass** (`NICHE131`). Every niche's back is 0.17–0.21 m from its facade window's glass, with along-wall offsets of 0.00–0.01 m. The blind niche has no glass, as intended.

**Walk checks.** Ray casts every 0.2 m, obstruction rays at 0.45 m and 1.4 m, and a headroom ray of 2.0 m.

| Route | Samples | Missing | Largest step | Obstructions | Low headroom | Height |
|---|---|---|---|---|---|---|
| Gröna: inside the east door → down the hall → the far corner by the end wall → the chapel door → into a courtyard niche | 204 | 0 | 0.18 (the niche floor) | see below | 0 | 10.47–10.65 |
| Förbrända: inside the north door → the length of the hall → the south door → the hood → an outer niche | 241 | 0 | 0.015 | 0 | 0 | 10.46–10.47 |
| Pass 126: courtyard → portal E → Kungstrappan → Gyllene salen → Kungsmaket | 330 | 0 | 0.167 | 0 | 0 | 5.47–10.47 |
| Gate passage B → C | 120 | 0 | 0.021 | 0 | – | 3.70–5.49 |
| Portal C → D / E / F | 35 / 42 / 187 | 0 | 0.012 | 0 | – | 5.47–5.48 |

- In run 1 the Gröna route went 0.45 m into the niche, and its last obstruction ray (0.25 m beyond the end) met the window parapet (one obstruction). Runs 2 and 3 stop 0.25 m into the niche.
- Pass 126's routes give the same numbers as in passes 127–130.

### Comparisons

The comparisons are in `SCR/p131/final/` (run 3's sandbox renders, also `SCR/p131/sb3/`).

- **`cmp_grona2017.jpg`.** These agree with the photograph:
  - the beamed ceiling;
  - the outer niches with the crucifix and escutcheons on the piers;
  - the far end wall with two windows and the crucifix between them;
  - the tower's curved wall with the pedimented door.

  The photograph looks more steeply at the outer wall. Its walls are a warm pink-beige lime that Workbench renders darker, and its niche reveals are rough and brighter.
- **`cmp_grona1929.jpg`.** The niches on both sides, the two-window end wall, and the pedimented door on the tower wall at the right. The plate's wide lens is approximated (vfov 70).
- **`cmp_forbranda1923.jpg`.** These agree with the photograph:
  - the long hall with arched niches on both sides;
  - the hooded fireplace on the left (outer) wall between the second niche and the last window;
  - the plain far end wall with the door right of centre;
  - the dark board ceiling with its cove.

  The photograph's courtyard wall shows about six niches; the model has the facade's five.
- **`cmp_forbranda2017.jpg`.** A check of arrangement only. The exhibition's hanging fabric columns, panels, lighting and tapestry hide most of the room.

### Pending

The official build is done (see "Official build"); the Unreal checks are pending.

## Mismatches with the exterior and open issues (reported, not corrected)

1. **Gröna salen's outer windows.** Olsson draws five (s 37.9–53.4). The facade has four (38.32–51.52, pass 27's even rule). The niches follow the facade.
2. **Gröna salen's courtyard windows.** Olsson draws four. The facade has five (pass 126's 3.8 m rule). The last facade window (52.87) stands at the bend, so its niche is skewed.
3. **The far end wall** (the south range's outer wall by the west tower). The 2017 and 1929 photographs show two windows with about one window's width between them; the facade has one (SW s 3.69). The second is a blind niche at s 1.55. A facade window at about SW s 1.5 would match.
4. **Window heights.** Möller's glass (sill 1.29–1.34 m, head 3.84–3.98 m above the floor) sits 0.2 m higher and is 0.6 m shorter than the facade's (1.10–4.30 m). The niches follow the facade. Gröna's flat niche heads are at 4.48 m (Möller 4.10).
5. **Range depths.** The model's west range is 0.65 m deeper than Möller's Unions-salen section, and the east range 1.1 m deeper than the Brända salen section. The rooms keep Möller's inside widths; the walls take the difference.
6. **Förbrända salen's area.** Olsson's text gives "about 440 m²" for 74 and 76. His own plan, registered, gives a hall of about 22.7 × 11.2 m. The model has 275 m² at Möller's width. The 1923 photograph's left wall (three niches and the fireplace) matches the model's outer wall. No source was found for the larger figure.
7. **Gröna salen's east end.** Kuretornet's rectangle with its skin, and pass 126's stair, leave the room's east face at s 36.08, 1.5 m east of the plan's (±1 m). Pass 126's förstuga ends against it with its own closed end wall. Gröna's east door (closed) is the place for the link (pass 126's mesh would need an opening).
8. **Pass 127's courtyard cornice** reaches 0.05 m inside Förbrända salen's courtyard wall at the NE/SE_e corner, in solid wall.
9. **Access.** All doors are closed leaves, except the chapel door, which is pass 130's closed leaf. Gröna's tower door leads into the west tower's chamber ("Runda kammaren" of the museum plan), which pass 27 builds as a closed cylinder. Förbrända's doors lead to rooms 72 and 82, which are not built. Neither hall has a stair from the courtyard in the model.

## Limitations, and what is not yet "AAA"

- **Surface.** The grisaille painting of Gröna salen's niche soffits is flat panels. The lime plaster's roughness is not modelled. The escutcheons' heraldry and carving are flat plates and simple shapes. All need hand-made or licensed textures (photographs may not be used as textures) and normal maps.
- **Lifted from photographs.** The escutcheons' number and positions are from the 2015/2017 photographs; their forms are simplified. The north fireplace in Förbrända salen is placed from one exhibition photograph and may not be on the hall's axis.
- **Not modelled.**
  - the modern chairs, lecterns, lighting rails and the radiators under Gröna salen's end windows;
  - the 2017 exhibition (fabric columns, plinths, panels);
  - the brick strip along a wall in Förbrända salen's floor (2017);
  - the Möller-era post in Unions-salen.
- **Förbrända's ceiling.** The 1923 photograph shows boards in short lengths and patches; the model has continuous boards.
- **Light.** No light sources; Workbench renders only. Unreal needs window lights and Lumen.
- **Collision.** No Unreal collision test; the walk checks are Blender ray casts.

## Sources

| Source | Licence | Used for |
|---|---|---|
| Carl Möller, "Calmar slott. Profiler", January 1882, "Profil genom Unions-salen" and "Profil genom s.k. Brända salen" (PK006-00041) | public domain | widths, wall thicknesses, ceilings, niches, window heights |
| Martin Olsson, *Fornvännen* 69 (1974), fig. 1 and text (DiVA) | in copyright; read only, not copied | room positions, registration, the plan's openings, "440 m²" |
| `commons-kalmar-castle-museum-green-hall-2017-07-30.jpg` | PD | Gröna salen; comparison 710; EXIF 18 mm |
| `commons-gr-na-salen-at-kalmar-slott-02.jpg` (Jopparn 2015, panorama) | CC BY-SA 4.0 | east wall, fireplace, doors, escutcheons, niche soffits |
| `dimu-021017090130.jpg` (Olsson 1929, Gröna salen after the restoration) | PDM | comparison 711 |
| `dimu-021017090063.jpg` (Olsson 1919, Förbrända salen) | PDM | the hall before 1923 |
| **New in `castle-sources` (with `sources.json` entries):** `commons-kalmar-slott-kmb-16001000022065.jpg` (1923, "Rum 74 och 76, Förbrända salen. Interiör mot söder efter restaureringen 1923") and `-022071.jpg` (1919) | Public domain (RAÄ/KMB, Martin Olsson) | Förbrända salen; comparison 712 |
| **New:** `commons-medici-family-isabelle-de-borchgrave-exhibition-in-kalmar-castle-2017-07-30-3.jpg` and `commons-isabelle-de-borchgrave-exhibition-in-kalmar-castle-2017-07-30.jpg` | Public domain | Förbrända salen today (identified by its arched niches and board ceiling; the files do not name the room); comparison 713; the north fireplace |
| Kalmar läns museum, "Plan över praktvåningen" (as listed in SOURCES.md) | read only | room order (10 Gröna salen, 11 the round tower's chamber, 17 Förbrända salen) |
| Pass 27 (`source/castle27.json`), passes 125–127 and 130 (`source/block125.json`, `block126.json`, `block127.json`, `block130.json`), the saved scene | project | frames, outline, towers, roof planes, facade windows, neighbouring rooms |

Google imagery was not used. No pixel of any photograph or drawing is used as a texture. The new materials (`M_Block131_*`, 29 of them) are flat tints on the town textures: TownPaintWhite, TownPaintBrown, TownPaintGreen, TownStone, TownIvory, TownMetalGrey and TownTileRed.

## Official build

The lead built pass 131 officially on 2026-10-03.
- **Checks:** the geometry check passed on the second rebuild (True) and the FBX audit passed (exit 0). The two rebuilds gave identical meshes.
- **Prevhash:**
  - Pass 130's meshes are identical.
  - The other entries are the known earlier corrections; pass 129's meshes are reported only through those.
- **Dry renders:** cameras 710–714, 5 of 5.
