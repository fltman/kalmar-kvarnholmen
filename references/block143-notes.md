# Pass 143: Kalmar slott, Rutsalen (room 63) and Drottningsalen (room 65)

Pass 143 builds two more state-floor rooms of Kalmar slott, in the queen's apartment (Drottningvåningen). It uses the method of passes 125, 130 and 131:
- closed architectural solids at real scale, standing inside pass 27's hollow range;
- flat-colour materials on the town textures;
- cameras inside;
- a walk check.

| Mesh | Category | Status | What |
|---|---|---|---|
| `SM_Castle143_Rutsalen` | Kalmar slott/Interiör | new | Rutsalen, the room shell. It has: a two-tone square parquet; a flat whitewashed board ceiling with a moulded cornice; three courtyard window niches reaching the floor, with sloping flat heads, each on its facade window with its own glazing and a panelled parapet; the deep niche in the spine wall with a closed door at its back; the 0.45 m partition with the open door to Drottningsalen; a closed door to Grå salen (61b) in the west wall |
| `SM_Castle143_RutsalenPaneler` | Kalmar slott/Interiör | new | the intarsia panelling to 3.04 m round the room. It has: a plinth; a panelled pedestal course; paired fluted columns on pedestals with a narrow inlaid field between them; wide fields with an octagonal inlaid picture, a base panel and an arabesque frieze panel; an entablature with triglyph blocks and a cornice that breaks forward over the columns |
| `SM_Castle143_Drottningsalen` | Kalmar slott/Interiör | new | Drottningsalen, the room shell. It has: wide boards on the floor and the ceiling, both running across the room; three round-arched courtyard niches, one step (0.15 m) up, on the facade windows, each with an arched fanlight; two round-arched niches in the spine wall, one with a closed door at its back and one with a bench; a closed door in the east wall towards Drottningtrappan (66); a cornice |
| `SM_Castle143_DrottningDekor` | Kalmar slott/Interiör | new | the stone fireplace in the spine wall; its painted pediment and pinnacles; the painted pedimented surrounds of the two doors; the painted draped dado; the painted scroll frieze under the ceiling; the painted coffers on the courtyard niches' vaults |

No existing mesh is touched (`CHANGED143` lists only the four new meshes).

## Which range, and where in it

### The north range is the model's NE range

Olsson's "norra längan" runs from tower II (Kungsmakstornet) to tower V (Fångetornet). Pass 131's registration of his plan to the four round towers (Olsson II, IX, VIII, V = pass 27's N, W, S, E; 11.47 px/m) puts it on **pass 27's NE range** (outward normal true 40). The model's NW range is Olsson's west range: Gyllene salen (59) at its north end (pass 125) and Gröna salen (87) at its south end (pass 131).

Olsson's text gives:
- rooms 63 and 65 were one hall, "Norra salen", divided by 1563;
- tower III (Vattentornet) "ingår med hela sin södra vägg i Rutsalens norra vägg";
- "Både Drottningsalen nr 65 och Rutsalen nr 63 har tre stora fönster vardera mot borggården";
- room 63 measures "11 × 10,5 m";
- 63's east wall (the wall to 65) is "av normal tjocklek, i huvudvåningen 45 cm".

### Olsson's plan, rectified into the NE frame

The plan (Fornvännen 69, 1974, fig. 1, in copyright) was read in the scratch directory only. Pass 131's registration was used to resample it into the NE range frame (`SCR/p143/pz.png`); only the readings are kept, in `OLSSON` in `scripts/prepare_block143.py`. They are all ±1 m.

| | Room 63 (Rutsalen) | Room 65 (Drottningsalen) |
|---|---|---|
| along the range (NE s) | ~18.0 to ~27.2; its west wall is skewed (s 26.3–28.0) | ~6.2 to ~16.9 |
| outer face (NE c) | −5.0 | −5.8 |
| courtyard face (NE c) | ~−15.0 | ~−15.0 |
| courtyard windows (NE s) | ~19.7, 22.9, 25.9 | ~8.0, 11.7, 15.3 |
| outer windows (NE s) | – (tower III) | ~8.2, 13.9 |

The 63/65 wall is drawn at s 16.9–18.1. Rooms 61b and 61a (Grå salen) follow to the west, towards Gyllene salen; Drottningtrappan, room 68 and tower IV follow to the east.

## Measurement

### Möller, "Calmar slott. Profiler" (1882, PK006-00041, public domain)

**Identification.** The caption reads **'Profil genom s.k. "Rut-salen"' (N:o 63 å planen af öfre våningen)** (`SCR/p143/moller_caption_rutsalen.png`). It is "Rut-salen", not "Röd-salen". Pass 127's `MOLLER` entry "Rutsalen (63)" is the same section.

**Scale.** The 90-fot bar's ticks were located on the full-resolution sheet:
- 0–90 fot reads 17.21 px/fot, which is **57.95 px/m** (Swedish fot 0.2969 m);
- 40–90 fot reads 57.70 px/m.

Pass 127's 57.97 px/m is kept; the readings agree within 0.4 %.

**Which side is the courtyard.** The annotation "Gård" and the courtyard ground (row 10254) are on the left, and "Jordlinie" (row ~10323) is on the right. So the left wall is the courtyard wall, as pass 127 read it.

**Readings.** Rows and columns were read on grid crops of the full-resolution sheet (`SCR/p143/r1.png`, `r_court.png`, `r_spine.png`, `r_out.png`). Heights are over the red state-floor line (row 9926).

| Value | Pixels | Metres |
|---|---|---|
| courtyard wall | x 3345–3417 | 1.24 |
| hall (courtyard face to spine face) | x 3417–4044 | **10.82** |
| spine wall | x 4044–4188 | **2.48** |
| outer rooms (their own floors; later building) | x 4188–4483 | 5.09 |
| outer wall | x 4483–4528 | 0.78 |
| facade to facade | x 3345–4528 | 20.41 |
| ceiling boards, underside | row 9562 | **6.28** |
| ceiling, top | row 9538 | 6.69 |
| courtyard glass, sill and head | rows 9858 / 9712 | 1.17 / 3.69 |
| courtyard niche head at the room face | row 9700 | 3.90 (the niche reaches the floor) |
| spine niche head, room face / back | rows 9700 / 9716 | 3.90 / 3.62 |
| spine niche depth | x 4044–4170 | 2.17 |
| door at the spine niche's back | rows 9795–9905 | 1.90 high |
| panelling (boiserie) top | row 9750 | **3.04** |

**Annotations** (left side, the hall): "Hjelpligt golf [the attic]. Hvitlimmad underpanel. Limfärgade väggar. Det rika boiseriet totalt uppruttet och maskstunget. — Parkettgolf: fullgodt skick." So in 1882 the hall had a whitewashed board ceiling, lime-painted walls, the rich panelling and a parquet floor.

The section shows a deep niche in the spine wall opposite a courtyard window niche. A rail or bench is drawn inside the spine niche (rows 9800–9845); it is not built.

### Facade windows (the saved scene)

The niches sit on the facade's state-row windows. They were read from `SM_Kalmar_Slott`'s glass on a copy of `source/Stortorget.blend` saved after pass 141's build (`SCR/p143/dump143.py`, `dump.json`).

- **NE courtyard front.** Windows 1.20 × 3.20 m, z 11.57–14.77, at NE s 0.64, 5.94, 9.74, 13.54, 19.15, 22.95 and 26.75. There is none between 13.54 and 19.15.
  - Rutsalen gets 19.15, 22.95 and 26.75, which are Olsson's three.
  - Drottningsalen gets 5.94, 9.74 and 13.54.
- **NE outer front.** The state row is at NE s 1.82, 6.17, 10.53, 14.88, 19.24 and 23.60. It lies behind the spine wall, in the space of Möller's outer rooms, which are not built.

### What is used

| Value | Source | Status | Model |
|---|---|---|---|
| Frame | pass 27's NE courtyard outline (points 6–8, collinear within 1 mm) | from the model | a along the outline (0.44° off pass 27's NE axis), b outwards, origin pass 27's NE origin |
| Floor | pass 125's state floor | taken over | z 10.47, slab from z 10.17 |
| Inside width (across) | Möller | measured | **10.82 m** (Olsson's text: 11) |
| Courtyard wall | Möller 1.24 m plus half the model's excess (22.42 − 20.41 m), as pass 131 | fitted | 2.245 m from the skin face; the room face is at NE c −16.76 (plan −15.0) |
| Spine wall | Möller | measured | 2.48 m; room face NE c −5.94 (plan −5.0 / −5.8), back −3.46 |
| Rutsalen's length | Olsson's text (10.5 m), centred on the middle courtyard window | from text | NE s 17.76–28.26 (plan ~18.0–27.2; the skewed west wall is built square) |
| Partition 63/65 | Olsson's text | from text | 0.45 m (the plan draws ~1.2 m) |
| Drottningsalen's length | the facade's three windows; the east face keeps a 0.25 m pier beside the first niche | from the model | NE s 5.36–17.31, **11.95 m** (plan ~6.2–16.9, 10.7 m) |
| End walls | plan (~1.2 m) | estimated | east 1.0 m, west 1.2 m |
| Ceiling | Möller | measured | board underside z 16.75, top z 17.16. Drottningsalen gets the same height (the 1933 photograph's niche-to-ceiling ratio, 1.6 × 3.9 m, agrees) |
| Courtyard wall's top at its back | pass 127's roof underside less 0.10 m | from the model | z 17.10–17.16 (all 41 samples clipped) |
| Rutsalen's courtyard niches | Möller (to the floor, flat sloping head); facade (glass) | measured / from the model | 1.65 m wide at the room face; head z 14.97 at the room face, 14.82 at the glass (Möller's 3.90 / 3.69 m are under the facade's glass head, 14.77) |
| Drottningsalen's courtyard niches | photographs 1922/1933 (round-arched); facade (glass) | estimated / from the model | 1.65 m wide, floor +0.15, springing z 14.60, crown 15.43 (room face) and 15.25 (glass). The first niche is skewed: its room face is 0.36 m west of its facade window |
| Parapets | facade sill | from the model | the last 0.59 m of each niche, up to z 11.57 |
| Spine niches | Möller (Rutsalen); photograph 1933 (Drottningsalen) | measured / estimated | Rutsalen: rectangular, 1.80 m wide, opposite the middle window, door 1.0 × 1.90 m. Drottningsalen: arched, a door niche 2.0 m wide at NE s ~14.2 (crown 3.90 m) and a bench niche 1.5 m wide at ~8.5 (crown 3.30 m, 1.6 m deep) |
| Panelling | Möller (height); photographs (form) | measured / estimated | 3.04 m; modules of 0.80 m column pairs and wide fields of 0.9–2.3 m |
| Parquet | Möller ("Parkettgolf") | pattern estimated | squares of 0.60 m, two tones |
| Fireplace | KMB 1922; photograph 1933 | estimated (±0.15 m) | 1.70 m wide, opening 1.10 × 1.35 m, consoles 0.42 m deep, overmantel to 2.26 m; painted pediment to 2.95 m, pinnacles to 3.82 m |
| Painted dado, frieze | photographs 1922/1933 | estimated | dado to 1.28 m; frieze 0.70 m under a 0.10 m cornice |

## What the rooms have

### Rutsalen (SM_Castle143_Rutsalen, SM_Castle143_RutsalenPaneler)

- **Walls.** Long walls are built as in pass 131's `lwall131`: piers, the slab under each niche, the niche's head. The courtyard wall's back follows the roof. The end walls are boxes around their doors.
- **Niches.** The three courtyard niches reach the floor (Möller), have flat sloping heads, a panelled parapet at the back and a window with a mullion, transoms and glazing bars. The spine niche is 2.17 m deep, with a closed door through the last 0.30 m of the wall.
- **Doors.**
  - The open door to Drottningsalen, 1.25 × 2.40 m, framed in the panelling.
  - The closed door to Grå salen (61b) in the west wall. The museum calls it "Dörr mellan grå salen och rutsalen" (KLM 021017083334).
- **Panelling.** It is built from the photographs (view only) and kept simple:
  - pedestal course;
  - paired fluted columns (lathe solids with base and capital);
  - narrow inlaid fields between the pairs;
  - wide fields with an octagonal inlaid picture showing a building under a gable (the photographs show architectural intarsia, among them Kalmar cathedral);
  - triglyph frieze and cornice.

  Piers shorter than 2.2 m get a single field.
- **Floor and ceiling.** Square parquet; whitewashed boards with a two-step moulded cornice.

### Drottningsalen (SM_Castle143_Drottningsalen, SM_Castle143_DrottningDekor)

- **Walls.** The same method, with round-arched niche heads (fans of slabs).
- **Courtyard niches.** Each has a parapet and a window with an arched fanlight up to the arch at the glass. The vaults carry painted grey coffers (detail 021017081516, "Fönsternisch, Valv, Kalkmålning", 1922).
- **Spine wall** (1933 photograph, looking north-east, i.e. at the spine wall):
  - the door niche on the left;
  - the fireplace in the middle;
  - the bench niche on the right.
- **Fireplace** (KMB 1922, "Spiseln med rest av överstycke i kalkmålning"):
  - plinths, scroll consoles with fluted fronts;
  - a lintel with six triglyph blocks, the shelf;
  - an overmantel with an oval cartouche and two side panels, a top cornice.

  The pediment and three pinnacles above are lime painting in the 1933 photograph, so they are flat painted plates.
- **Painted work** (trompe-l'oeil):
  - pedimented surrounds with three pinnacles round the east door and the door to Rutsalen (021016468882; 1933);
  - a pale draped dado with darker folds and swags;
  - a grey scroll frieze, as a band with lines and roundels.
- **Floor and ceiling.** Wide boards (1922 photograph), a board ceiling across the room (1933).

## Cameras

| Camera | Where (room frame a, b; height over the floor) | Look | Compared with |
|---|---|---|---|
| `800_Block143_Cal_Drottningsalen1933NE` | a 15.9, 7.96 m in front of the spine face; 1.50 m | towards the spine wall, turned 34.5° east; pitch 9; vfov 52 | KLM 021017088983 (1933, PDM). Camera fitted on four columns (the corner, both niches, the fireplace), residuals ≤15 px |
| `801_Block143_Cal_Drottningsalen_DoorRutsalen` | 8.0 m in front of the partition, on the room's axis; 1.60 m | +a (towards Rutsalen); pitch −1; vfov 52 | KLM 021016468882 (PDM), by eye |
| `802_Block143_Cal_RutsalenWindows` | Rutsalen's north-west corner | towards the partition/courtyard corner; pitch 3; vfov 55 | KLM 021016783105 (no licence; view only), by eye |
| `803_Block143_Cal_RutsalenPanel` | a 21.6, 3.2 m from the courtyard face; 1.55 m | towards the spine wall; pitch 6; vfov 50 | KLM 021016986299 (no licence; view only), arrangement only |
| `804_Block143_Aerial_NorthRange` | over the courtyard | towards the NE range | – |

## Verification

### Prepare

`KALMAR_GEO=<pylib> python3 scripts/prepare_block143.py` prints `BLOCK143_PREPARE_OK`. It asserts:
- both envelopes lie inside pass 27's outline and outside the courtyard, the four towers plus 0.36 m, Kuretornet plus 0.36 m and both bays (0.000 m² each);
- no overlap with:
  - pass 125's rooms plus 1.6 m (Rutsalen's envelope is 2.77 m from Gyllene salen's room);
  - pass 126's stair strip, checked to a 20 (pass 131's proxy runs to a 30, which reaches into this range's west end, where pass 126 has no geometry; the saved scene has no pass 126 vertex in the zone);
  - pass 131's envelopes;
  - each other;
- the niches keep 0.25 m from the end walls and 0.45 m from each other;
- the fireplace is clear of the spine niches, and the doors keep 0.4 m from the corners;
- every niche head is at least 0.85 m under the ceiling;
- Rutsalen is 10.5 × 10.82 m;
- the roof's underside over the rooms is more than 0.3 m above the ceiling's top (min z 18.40);
- the courtyard wall's back stays above the ceiling boards (min z 17.095);
- the niche backs are 0.10–0.30 m from the facade glass (0.25 m).

### Sandbox

The check harness is `SCR/p143/build_block143_check.py` with `SCR/p143/sandbox143.py` (pass 131's copy, Workbench shadows off). It builds twice and runs all checks. A scratch harness (`SCR/p143/fast.py`) built the pass alone on an empty scene for the design iteration.

- **Run 1** used prelude 141 and printed `SANDBOX_DONE prelude 141` without errors (`SCR/p143/log1.txt`).
- **Run 2** used prelude 142 (`log2.txt`). Its only change is the walk route, which in run 1 went 1.2 m into a Rutsalen niche, onto its parapet. The numbers below are run 2's.

**Change set and repeatability.**
- `CHANGED143 ['SM_Castle143_DrottningDekor', 'SM_Castle143_Drottningsalen', 'SM_Castle143_Rutsalen', 'SM_Castle143_RutsalenPaneler']`.
- `REPEAT143 True`; the second run changes nothing.

**Degenerate faces.**
- `drop_degenerate_faces143` removes 0 faces from each mesh.
- Faces: Rutsalen 11,466, panelling 4,358, Drottningsalen 7,409, Dekor 3,849.

**The bevel problem** (as in pass 131). In the first scratch build the town bevel collapsed on Drottningsalen (5,555 faces dropped) and partly on Rutsalen (347). There were two causes:
- the half-disc fans at the backs of the arched spine niches had their centre on the chord, which gave zero-area triangles;
- the ceiling's joint lines were 4 mm high.

The fans now start from the springing point, and the joint lines are gone. One collinear inlay motif in the panelling was also replaced.

**Export frame check** (pass 137's wrapper): 0 invalid loops; 4 of 4 exports succeeded. Fallback frames: Rutsalen 28 loops, panelling 0, Drottningsalen 204, Dekor 31.

**Placement.**
- `EXTENT143`: every vertex of the four meshes lies in its envelope and z 10.17–17.16: 0 outside.
- `ROOFCLEAR143`: every vertex above z 15.5 has the castle roof above it (Rutsalen 360 vertices, Drottningsalen 2,208, Dekor 2,020; 0 not under the roof).
- **Intrusions.** No vertex of any other mesh is inside Drottningsalen's envelope. Inside Rutsalen's envelope there are 12 vertices of `SM_Kalmar_Slott`, at a 29.47–29.53, b −18.13, z 16.02–16.24. That is pass 127's courtyard cornice or corner filler by the NE/NW courtyard corner, 0.27 m inside the courtyard wall's back, in the solid corner of the west and courtyard walls, not in the room (as pass 131 found at Förbrända salen's corner).

**Niches against the facade glass** (`NICHE143`). Rays from the room outwards through each courtyard niche, on its axis and ±0.4 m, at z 12.4 and 13.9, meet the niche's own frame and pane 2.19–2.26 m in, then pass 27's glass (`M_Town_Glass`) at 2.495 m. The niche back is 0.25 m from the facade glass, with 0.00 m offset along the wall. The one exception is Drottningsalen's skewed first niche: at −0.4 m from its glass axis the ray meets the pier, as intended (the room face is 0.36 m west of the window).

**Walk checks.** Ray casts every 0.2 m, obstruction rays at 0.45 m and 1.4 m, and a headroom ray of 2.0 m.

| Route | Samples | Missing | Largest step | Obstructions | Low headroom | Height |
|---|---|---|---|---|---|---|
| Pass 143: Drottningsalen by the east door → past the fireplace → into a courtyard niche (one step) → through the open door → Rutsalen → into a courtyard niche → into the spine niche → by the west door | 286 | 0 | 0.15 (the niche step) | 0 | 0 | 10.455–10.62 |
| Pass 135: kitchen | 423 | 0 | 0.128 | 0 | 0 | 5.10–5.48 |
| Pass 133: courtyard → Kyrkportalen → stair → chancel | 328 | 0 | 0.176 | 0 | 0 | 5.47–10.75 |
| Pass 133: Gröna salen → chapel | 46 | 0 | 0.012 | 0 | 0 | 10.47–10.48 |
| Pass 130: chapel | 117 | 0 | 0.14 | 0 | 0 | 10.46–10.75 |
| Pass 129: portal C → D's stair → landing | 125 | 0 | 0.163 | 0 | – | 5.47–5.96 |
| Pass 133: portal C → Kyrkportalen | 206 | 0 | 0.012 | 0 | – | 5.47–5.48 |
| Pass 131: Gröna salen / Förbrända salen | 204 / 241 | 0 | 0.18 / 0.015 | 0 | 0 | 10.46–10.65 |
| Pass 126: courtyard → portal E → Kungstrappan → Gyllene salen → Kungsmaket | 330 | 0 | 0.167 | 0 | 0 | 5.47–10.47 |
| Gate passage B → C; portal C → D / E / F | 120; 35 / 42 / 187 | 0 | ≤0.021 | 0 | – | 3.70–5.49 |

All earlier routes give the same numbers as in pass 137. The earlier rooms' roof clearance (`ROOFCLEAR131`) is unchanged.

In run 1 the new route went 1.2 m into Rutsalen's middle courtyard niche, where the parapet begins 1.19 m in. It climbed the parapet (step 1.10 m) and its obstruction ray met it twice. The rest of the route was clean: the door, both rooms, Drottningsalen's niche step (0.15 m) and the spine niche. Run 2 stops 0.8 m into the niche.

### Run 2

Run 2 printed `SANDBOX_DONE prelude 142` without errors. Every check above has the same numbers as in run 1, except the new walk: 286 samples, 0 missing, largest step 0.15 m (Drottningsalen's niche step), 0 obstructions, 0 low headroom, z 10.455–10.62. Pass 142 changes no castle mesh.

### Comparisons

The comparisons are in `SCR/p143/final/` (photograph | sandbox render).

- **`cmp_800.jpg`** (021017088983, 1933). These agree with the photograph:
  - the spine wall's arched door niche, the fireplace with its painted pediment and pinnacles, and the smaller arched bench niche;
  - the east wall's door with its painted pedimented surround;
  - the draped dado, the scroll frieze and the board ceiling.

  The real niches' arches are slightly flatter; the photograph's dado drapery and frieze scrolls are finer than the flat bands.
- **`cmp_801.jpg`** (021016468882). The partition with the pedimented painted surround round the door to Rutsalen, and the panelling and parquet seen through the door. The photograph's small wall cupboard recess by the courtyard corner is not built.
- **`cmp_802.jpg`** (021016783105, view only). The panelled walls and the three courtyard windows. In the photograph:
  - the windows look lower-sitting (sill about 0.9 m) and wider, with shallow reveals;
  - the panelling runs across the piers and under the windows.

  The model's niches follow Möller (deep, to the floor) and the facade's glass.
- **`cmp_803.jpg`** (021016986299, view only). The arrangement of the panelling: paired fluted columns, octagonal pictures, the entablature. The real intarsia is far richer.

### Pending

The official build is done (see "Official build"); the Unreal import is part of the v0.1.8 sync.

## Mismatches with the exterior and the sources, and open issues (reported, not corrected)

1. **Drottningsalen's windows.** Olsson draws three courtyard windows at NE s ~8.0, 11.7 and 15.3. The facade has 5.94, 9.74 and 13.54, and nothing between 13.54 and 19.15. The niches follow the facade, so Drottningsalen is 11.95 m long (plan 10.7 m) and its east face (5.36) is 0.8 m east of the plan's. The first niche is skewed.
2. **Window heights.** Möller's courtyard glass is 1.17–3.69 m over the floor; the facade's is 1.10–4.30 m (z 11.57–14.77). The niches follow the facade, and Rutsalen's flat niche heads are at 4.50 m (Möller 3.90 m).
3. **Range depth.** The model's NE range is 22.42 m skin to skin; Möller's section is 20.41 m. The room keeps Möller's width; the courtyard wall takes half the excess (2.245 m against Möller's 1.24 m). Olsson's plan puts the courtyard face about 1.7 m further in (c −15.0).
4. **The 63/65 partition.** Olsson's text gives 0.45 m; his plan draws about 1.2 m. The text is used.
5. **Rutsalen's west wall** is skewed on the plan (s 26.3–28.0); it is built square at s 28.26.
6. **The ceiling.** Möller (1882) and the early 20th-century photograph show a flat ceiling with a cornice; that is what is built. The project's SOURCES.md (from Kulturvärden 1/2025) and secondary web texts mention a painted and gilded coffered ceiling in Rutsalen; no image of it was available with a licence, and its date is not clear (the 1580s?). It may be what visitors see today.
7. **The name.** No source in hand explains "Rutsalen" (Olsson's English summary calls it "Chequer Hall"). Möller records a parquet floor; the photographs show panelling with square and octagonal fields. The parquet's square pattern is estimated, not documented.
8. **The outer side.** Behind the spine wall the model has no rooms: Möller's 5.1 m outer rooms (with their own floor levels) and tower III are not built. The NE outer front's state-row windows light that empty space. The doors at the backs of the spine niches are closed leaves.
9. **Access.** The rooms are connected to each other (open door), but not to any built route.
   - Rutsalen's west door leads to 61b (part of Grå salen, not built). Gyllene salen's door to 61b (pass 125) is also closed.
   - Drottningsalen's east door leads to Drottningens förstuga (66) and Drottningtrappan (not built; pass 124's portal D dresses its courtyard door).
   - Kungstrappan's hall (55) and Gröna salen's east door are in the west range and do not reach these rooms.

   Access is open; Unreal can place the player inside (camera 800's position).
10. **Pass 127's courtyard cornice** reaches 0.27 m inside Rutsalen's courtyard wall at the NE/NW courtyard corner, in solid wall.

## Limitations, and what is not yet "AAA"

- **Surface.** All of these are flat colours and would need hand-made or licensed textures and normal maps (photographs may not be used as textures):
  - the intarsia (17 kinds of wood, per the secondary texts) is flat plates in two tones;
  - the painted drapery, frieze scrolls and niche coffers are simple bands, roundels and squares;
  - the lime plaster's roughness is not modelled.
- **Lifted from photographs.** The positions of the fireplace, the spine niches and the east door are estimated from one 1933 photograph (±0.5 m). The panelling's module is estimated.
- **Not modelled:** the paintings and chests in the photographs, the wall cupboard recess, curtains, modern lighting and radiators, and the photograph's floor of loose boards during the 1930s work (021017034874).
- **Light.** No light sources; Workbench renders only.
- **Collision.** No Unreal collision test; the walk checks are Blender ray casts.

## Sources

| Source | Licence | Used for |
|---|---|---|
| Carl Möller, "Calmar slott. Profiler", January 1882, 'Profil genom s.k. "Rut-salen"' (PK006-00041) | public domain | identification, width, wall thicknesses, ceiling, niches, panelling height, parquet |
| Martin Olsson, *Fornvännen* 69 (1974), fig. 1 and text (DiVA) | in copyright; read only, not copied | range, room positions, windows, "11 × 10,5 m", the 0.45 m partition, tower III |
| **New in `castle-sources`** (with `sources.json` entries): `dimu-021017088983.jpg` (Drottningsalen looking north-east, 1933), `dimu-021016468882.jpg` (Drottningsalen, the door to Rutsalen), `dimu-021017081516.jpg` (window-niche vault, 1922), `dimu-021017081519.jpg` (frieze, 1933) | PDM (Kalmar läns museum) | Drottningsalen; comparisons 800 and 801 |
| **New:** `commons-kalmar-slott-kmb-16001000022069.jpg` ("Andra våningen, rum 65, Drottningsalen. Spiseln med rest av överstycke i kalkmålning före konserveringen", Martin Olsson 1922) | public domain (RAÄ/KMB) | the fireplace |
| DigitaltMuseum, Kalmar läns museum, without a stated licence: 021016783105, 021016769128, 021016986299, 021017036107, 021017036112/113, 021017090149/150, 021016517061, 021016519933, 021016519960, 021017083334, 021017083389, 021017083397, 021017083402 | no licence stated: viewed only, not saved in the project | Rutsalen's panelling and windows; Drottningsalen's niches and fireplace; doors |
| Kulturvärden 1/2025, "Kungligt i Kalmar" (SFV, text only) | read only | intarsia panelling; Rutsalen as the queen's representation room |
| Pass 27 (`source/castle27.json`), passes 125–127, 130, 131 and 135 (`source/block1xx.json`), the saved scene | project | frame, outline, towers, roof planes, facade windows, neighbouring rooms |

The DigitaltMuseum metadata was read through its public API, and Commons through its API; the browser was not used. Google imagery was not used. No pixel of any photograph or drawing is used as a texture. The new materials (`M_Block143_*`, 29 of them) are flat tints on the town textures: TownPaintWhite, TownPaintBrown, TownStone, TownIvory and TownMetalGrey.

## Official build

The lead built pass 143 officially on 2026-10-04.
- **Checks:** the geometry check passed on the second rebuild (True), and the FBX audit passed (exit 0). The two rebuilds gave identical meshes.
- **Prevhash:** pass 142's 62 meshes are identical. Everything else listed is a known earlier correction, so nothing outside the four new meshes changed.
- **Dry renders:** cameras 800–804, 5 of 5.
