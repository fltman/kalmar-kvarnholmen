# Pass 133: Kalmar slott, Kyrkportalen and the way up to Slottskyrkan

Pass 133 moves portal F (Kyrkportalen, 1568) to its true place on the south range's courtyard front and makes the chapel (pass 130) reachable on foot from the courtyard. It also opens the chapel's west door into Gröna salen (pass 131).

| Mesh | Category | Status | What changed |
|---|---|---|---|
| `SM_Kalmar_Slott` | Kalmar slott/Castle | re-created, `detail_pass=133`, `corrects_pass=27,124,126,127,128,129` | pass 27's middle door on the SW courtyard edge goes; Kyrkportalen's door is cut 2.37 m from the south corner and is open; the lower-row window over it goes, the middle-row window over it is shortened to sit on the portal; the windows at the old door's place return |
| `SM_Castle124_Portals` | Kalmar slott/Castle | re-created, `detail_pass=133`, `corrects_pass=124,126,129` | portal F moved and rebuilt; portals B, C, D and E unchanged |
| `SM_Castle124_Paving` | Kalmar slott/Ground | re-created, `detail_pass=133`, `corrects_pass=124,126,129` | the slab path to F follows the portal |
| `SM_Castle130_Slottskyrkan` | Kalmar slott/Interiör | re-created, `detail_pass=133`, `corrects_pass=130` | the two door leaves are taken out (the surrounds stay): the altar door and the west door stand open |
| `SM_Castle133_Kyrktrappan` | Kalmar slott/Interiör | new | Sydöstra vindelstenen: the vestibule inside Kyrkportalen, a flight under the chancel, the stair hall beyond the altar wall with a half landing, a second flight and the landing at the altar door |

No other mesh changes (sandbox: `CHANGED133` lists exactly these five). `SM_Kalmar_Slott_Towers` (pass 132) and the rooms of passes 125, 126 and 131 are untouched. `SM_Castle130_Inventarier` is not re-created.

**Method.**
- **Passes 124–129.** `build_block133.py` takes the slice of `build_block129.py` from `def rep129` to `NS129=dict(globals())`. That slice gives pass 129's composed source (pass 127's file with the edits of passes 128 and 129, which runs pass 124's code as pass 126 composed it, which runs pass 27's code). The slice runs in a private namespace (`NSC133`). Pass 133's single replacements are each asserted to occur exactly once:
  - the marking (`detail_pass=133`, the `corrects_pass` lists above);
  - `EXTRA133` (new helper `filt133`) runs in pass 27's namespace after `EXTRA129`;
  - in pass 27's `front`, the door in `OPEN133` is drawn with pass 126's `arch_open126` (as portal E's door);
  - the window filter becomes `filt133(filt127(holes))`;
  - pass 129's `doors129` gets an entry for the SW courtyard edge (CI2–CI1), so pass 27's middle-door rule no longer applies there;
  - pass 129's `edit_portals129` is wrapped by `edit_portals133`. After pass 129's edits, it inserts `PORT133`, puts F at its `u`, replaces pass 124's F body (9 lines, asserted) with `portal_f133`, and moves the paving target.
- **Pass 130.** The slice of `build_block130.py` from `def b130_new` to the furnishings header runs in its own namespace. Pass 130's 41 materials are mapped by name and not re-created: re-creating them would strip `SM_Castle130_Inventarier`. Two edits are made: the marking, and the 6 lines that draw the two leaves (asserted).
- **Positions.** They are computed in `scripts/prepare_block133.py` and written to `source/block133.json` and `previews/block133-zones.json`.

## 1. Kyrkportalen: where it is and what it looks like

### Sources

- **Olsson 1957** (*Fornvännen*, pp. 137–183, read on DiVA, not copied). He writes that the south range's courtyard front has two portals, and that F is the eastern one.
  - F has two fluted Doric columns on each side of the round-arched door.
  - Above them is an entablature with triglyphs and plain metopes.
  - On it stand four herms, male and female alternating, on Ionic capitals. They carry a second entablature.
  - Between the herms is a cartouche with Johan III's crowned initials and 1568.
  - On top is a segmental tablet with the arms held by two lions.
  - The other portal, G (the south-west portal, "sydvästra borggårdsportalen"), frames the walled-up south gate passage.
- **Street View 2014.** The two courtyard panoramas were viewed only, from pass 128's resected cameras. No pixel was saved.
- **The 2017 courtyard photograph** (Commons, PD), with pass 127's resected camera 689.

### Readings

Each reading is a ray intersected with the SW courtyard face. The positions are taken from the south corner downpipe in the same view, because the panoramas' corners differ from pass 27's by 0.3–1.2 m.

| View | Angle to the front | Corner (model 27.84) | Door axis from the corner | Portal width | Portal edge from the corner |
|---|---|---|---|---|---|
| Pano 2 `jOXzkLldNOjrveyz1T81wg`, URL 207h 40y 95t | 76–80° (square on) | 28.36 | **2.64 m** | 4.40 m (4.0 scaled) | 0.37 m |
| Photograph 2017, camera 689 | 57–62° | 29.04 | **3.49 m** | 4.94 m | 1.02 m |
| Pano 1 `zCIfieeXGQUNANmWu_Tg9A`, URL 162h 60y 95t | 26–35° (grazing) | 27.55 | 4.89 m | 4.8 m | 2.4 m |
| Pass 129 (pano 1 at 140°, pano 2 at 235°) | – | – | 3–3.5 m | – | – |

- Pano 1 sees the front at a grazing angle. There, a 1 m error in the camera position moves the reading about 2 m along the front, so it is not used.
- In pano 2 and in the 2017 photograph, the state-floor window and the small window over the tablet stand on the portal's axis. That window column is pass 126's row at u −7.60 on the CI2–CI1 edge (s 25.47). The chapel's courtyard niche (pass 130) stands on it.
- **Used:** F's axis on that column, **s 25.47, 2.37 m from the south corner**. That is within 0.3 m of pano 2, the square-on view. Pass 124 had it at s 17.87, 7.6 m further west.

**Heights** were read on pano 2: pitch +5, f 1107 px, 33.2 m to the face, camera ZC + 1.9. They are scaled per front between the courtyard (row 576) and the courtyard eaves (row 172, z 17.01), as in pass 129 (factor 0.94).

| Part | Above the courtyard (m) |
|---|---|
| Pedestal tops | 0.58 |
| Column tops (lower order) | 2.40 |
| Lower entablature top | 2.89 |
| Herm storey, to the upper cornice | 4.23 |
| Upper cornice top | 4.40 |
| Segmental tablet top | **4.94** (z 10.41) |
| Door: springing / crown | 1.46 / 2.14 |
| Window over the portal: sill / head | 4.97 / 5.65 (z 10.44 / 11.12) |

- **Widths.** The portal is 4.0 m wide in pano 2 (scaled) and 4.9 m in the photograph; 4.2 m is used. The door is 1.38 m (1.40 used). The window over the portal is 1.02 m (the model's row has 0.90 m).

### What is built (`portal_f133`)

- The parts:
  - pedestals 0.58 m high;
  - paired fluted Doric columns at ±0.95 and ±1.80 m, to 2.40 m;
  - an entablature with seven triglyph blocks, to 2.89 m;
  - four herms at the same axes: a tapering term, a bust and head, an Ionic capital;
  - the cartouche (1.30 m wide) with a field and a small crown block;
  - the upper entablature and cornice, to 4.40 m;
  - the segmental tablet, 1.90 m wide, to 4.94 m, with the arms and the two lions as blocks;
  - jambs and an arch ring on the door.
- Back plates stand beside the door only. In sandbox run 3 a full-width plate closed the doorway, and the walk check found it.
- The materials are two new flat tints, `M_Block133_PortalStone` and `M_Block133_PortalTablet`, on TownStone. The portal is weathered grey in both pano 2 and the photograph, darker than pass 27's light trim.

### The facade

- **The door.** Pass 27's door rule put a door at the middle of the SW edge (s 17.17–18.57, crown 7.87). It goes. Kyrkportalen's door is cut at u −7.60 (1.40 m wide, springing 1.46 m, crown z 7.63) and drawn open: an arch, jambs, a threshold, no leaf.
- **No window over a door.** Pass 127's rule is kept: no window within 1.2 m beside a door or 1.6 m above its arch.
  - It removes the lower-row window at s 25.47 (z 6.77–8.03), which the new opening and the portal cover.
  - The lower-row and middle-row windows at s 17.87, which pass 27's middle door had removed, return.
- **The middle-row window over the portal.** It was at s 25.47 with its sill at z 9.9. The panorama and the photograph show it standing on the portal's tablet. It is shortened to sill z 10.46 and head z 11.10, so 0.64 m high (`filt133`). It is not moved: its axis is the portal's.

## 2. The way up to the chapel

### What the sources say

1. **Kalmar läns museum, "Kalmar slott, plan över praktvåningen"** (KLMF.Slott003-57, DigitaltMuseum 021016586266; viewed, no licence stated, not copied).
   - Room 13, "Sydöstra vindelstenen", is a narrow stair hall immediately beyond the chapel's altar wall (12). It runs across the range from the courtyard side to the outer wall.
   - Its treads are drawn as lines across the courtyard half, so the flight runs across the range.
   - At its outer end there is a door into the chapel beside the altar, and an opening on to room 14 (Förrum) and the south tower's chamber (15).
   - On the other side of the chapel, the wall between Gröna salen (10) and the chapel has a door near the outer wall.
2. **Krigsarkivet 0424:058:212a** (about 1780, public domain; pass 130). The chapel has exactly two doors: one in the west end wall, off axis towards the outer wall, and a narrow one in the altar wall by the outer corner. There is no door in the courtyard wall.
3. **Olsson 1974, fig. 1** (the main floor about 1574; in copyright, read only, as registered by pass 131). Beyond room 86's altar end, a passage runs in the cross wall from the courtyard side to the outer corner. It has a square well at the courtyard corner, where the museum plan has room 13.
4. **The name and the place.** Olsson calls F "Kyrkportalen". Measured above, it stands 2.4–3.5 m from the south corner, at the courtyard foot of room 13.

None of the open sources draws the ground floor. The link from the portal to the foot of the stair is therefore not documented. It is built as the simplest arrangement that fits the documented parts:
- the portal;
- the stair hall beyond the altar wall, with its flight across the range;
- the altar door.

The visitor route of today (the museum's own route through the state floor) was not found in a source and is not modelled.

### What is built (`SM_Castle133_Kyrktrappan`)

Everything is in pass 27's SW range frame: s along the range, c outwards; the courtyard line is at c −9.37.

- **The vestibule** inside the portal: s 24.20–26.50, c −9.33 to −7.45. It has stone flags at the courtyard level and a threshold slab through the door.
- **Flight 1**, along the courtyard wall under the chancel:
  - 14 risers of 0.176 m and treads of 0.26 m, from s 26.50 to 29.88;
  - lane c −9.25 to −7.45 (1.8 m);
  - a plastered ceiling at z 10.00–10.15 under the chapel's floor slab (z 10.17);
  - least headroom over a tread under the chapel 2.95 m;
  - a spine wall on its inner side and an end wall behind the vestibule;
  - a wall piece by the south corner, where pass 27's courtyard skin ends.
- **The stair hall** (room 13), beyond the altar wall's back:
  - s 28.70 to 31.25 (to 30.1 at the outer wall, clipped by the south tower plus its skin and a 0.2 m lining);
  - c −9.25 to −1.25;
  - walls 0.20–1.15 m thick, the outer one as thick as the chapel's;
  - a ceiling at z 14.20–14.35.
- **The half landing** at z 7.934 (s 29.88–31.25, c −9.25 to −7.45).
- **Flight 2**, across the range towards the outer wall, as the museum plan draws it:
  - 16 risers of 0.176 m, treads 0.26 m, from c −7.45 to −3.55;
  - lane s 29.88–31.25, at least 1.26 m wide where the tower lining clips it;
  - a full-height spine wall between it and the top of flight 1.
- **The top landing** at z 10.75, the chancel's level (pass 130: the state floor plus two risers of 0.14 m). It spans c −3.55 to −1.25 and s 28.70 to the tower lining, and it is in front of the altar door (c −2.00, 0.90 × 2.20 m).
- **Details:**
  - a plain stone surround on the stair hall's side of the altar door;
  - oak handrails on the spine walls along both flights.
- **The rise.** 30 risers of 0.176 m: z 5.47 to 10.75, 5.28 m. The tread is 0.26 m, so 2R + T = 0.61.

Every face is a closed prism with triangulated caps (`prism133`), finished with `s21_finish` and `drop_degenerate_faces133`.

### Chapel and Gröna salen

- The museum plan shows a door in the wall between Gröna salen and the chapel near the outer wall. The 1780 plan has the chapel's west door at the same place (c −4.256).
- Pass 131's chapel door in Gröna salen's lining has no leaf of its own. Pass 130's leaf closed the opening.
- With the leaf taken out, the opening runs from Gröna salen through the lining and the chapel's west wall into the nave.

## Cameras

| Camera | Where | Look | Compared with |
|---|---|---|---|
| `720_Block133_Cal_Pano2_PortalF` | pano 2 (−860.06, −308.67), ZC + 1.9 | true 204.35 (URL 207h), pitch 5, vfov 40 | Street View 2014 pano 2 (on screen) |
| `721_Block133_Cal_Pano1_PortalF` | pano 1 (−885.06, −306.46), ZC + 2.1 | true 160.66 (URL 162h), pitch 5, vfov 60 | Street View 2014 pano 1 (on screen) |
| `722_Block133_Vestibule` | SW s 25.2, c −8.9, ZC + 1.6 | up flight 1, pitch 18, vfov 74 | – |
| `723_Block133_AltarDoor` | SW s 25.0, c −3.2, chancel + 1.6 | the open altar door and the landing behind it | – |
| `724_Block133_Aerial_SouthCorner` | over the courtyard | the south corner | – |

The 2017 photograph is compared at pass 127's camera 689 (`cmp_2017.jpg`).

## Estimated

- The ground-floor link from the portal to the stair: the vestibule, flight 1 under the chancel and the half landing. Not documented; see above.
- The stair hall's walls, ceiling and the stair's tread. The flight across the range is the museum plan's; its length follows from the riser rule.
- Room 13's extent beyond s 30.1. The museum plan is schematic, and the model's south tower limits it.
- Portal F's details: fluting as 16 facets, the herms as terms with block heads, the cartouche, arms and lions as blocks.
- The portal's width (4.2 m, between 4.0 and 4.9 m).

## Verification

### Prepare

`KALMAR_GEO=<pylib> python3 scripts/prepare_block133.py` prints `BLOCK133_PREPARE_OK`. It asserts:
- riser ≤ 0.18 m (0.176) and 0.58 ≤ 2R + T ≤ 0.66 (0.612);
- headroom under the chapel ≥ 2.0 m (2.95);
- the envelope (stair hall and ground-floor hall) inside pass 27's body and outside the courtyard and all four towers plus 0.36 m (0.000 m² each);
- no overlap with pass 125's rooms plus 2.2 m (43.8 m away), pass 126's stair strip (27.1 m), Gröna salen (18.0 m) or Förbrända salen (18.9 m);
- the stair hall clear of the chapel's envelope (0.000 m²). The ground-floor hall lies under the chapel (9.4 m²), below its slab;
- the top landing covers the altar door;
- flight 2 at least 1.0 m wide (1.26);
- the portal inside its edge and 0.27 m clear of the south corner.

### Sandbox

Four runs were made with `SCR/p133/build_block133_check.py` (it builds twice and runs all checks) and `SCR/p133/sandbox133.py` (a copy with the Workbench shadows off, as passes 125, 130 and 131 did for closed rooms). Logs: `SCR/p133/log1.txt`–`log4.txt`.
- **Run 1** (prelude 131) stopped at the asserted line count of pass 124's F body (9 lines, not 10).
- **Run 2** (prelude 132) built and passed the change-set, repeatability and export checks. Its first render then hung in the Workbench draw with 0 % CPU while the machine was swapping. It was killed, and its buffered walk output was lost. The wrapper now prints line-buffered.
- **Run 3** (prelude 132) printed `SANDBOX_DONE prelude 132`. The only failure was the new walk's 6 obstructions: the portal's full-width back plate in the doorway, fixed as above.
- **Run 4**, on the final files, printed `SANDBOX_DONE prelude 132` without errors. The numbers below are run 4's.

**Change set and repeatability** (run 4; run 3 the same):
- `CHANGED133 ['SM_Castle124_Paving', 'SM_Castle124_Portals', 'SM_Castle130_Slottskyrkan', 'SM_Castle133_Kyrktrappan', 'SM_Kalmar_Slott']`;
- `REPEAT133 True`; the second run changes nothing.

**Polygons and degenerate faces.**
- Final counts: `SM_Kalmar_Slott` 312,516 (pass 129: 311,152; the windows at the old door's place are back), Portals 8,314, Paving 1,040, Slottskyrkan 304,532 (pass 130: 305,052; the two leaves are gone), Kyrktrappan 1,574.
- `drop_degenerate_faces133` removes 0 faces from each of the five meshes.
- Pass 130's own filter, run inside its re-created code, still removes the vault's bevel slivers before that.

**Export frame check** (pass 131's wrapper method: the export tail's preparation, the exporter's frame test, a test FBX export of each mesh):
- 0 invalid loops; 5 of 5 exports succeeded.
- Fallback frames: `SM_Kalmar_Slott` 5,671 loops (pass 129: 5,656), Portals 0, Paving 15, Slottskyrkan 233 (pass 130: 233), Kyrktrappan 28.

**Placement.**
- Every vertex of `SM_Castle133_Kyrktrappan` lies in the envelope (stair hall, or ground-floor hall with the corner piece) and in z 5.17–14.35 (`EXTENT133`, 0 outside).
  - In run 2, 6 vertices of the corner wall piece were outside, because the envelope had no corner piece then. The envelope was corrected.
- No vertex of any other mesh lies inside either envelope (`INTRUDE133`, 0 for `SM_Kalmar_Slott`, the towers, pass 27's walls and ground, the pass 130 meshes and the rest).
- No vertex of the stair hall is above z 15.5. The ceiling's top is z 14.35, under the courtyard eaves (z 17.01) (`ROOFCLEAR`).

**Walk checks.** Ray casts every 0.2 m, obstruction rays at 0.45 and 1.4 m, a 2.0 m headroom ray.

| Route | Samples | Missing | Largest step | Obstructions | Low headroom | Height |
|---|---|---|---|---|---|---|
| **New:** courtyard (the gate passage's end) → Kyrkportalen → vestibule → flight 1 → half landing → flight 2 → landing → altar door → chancel → down the chancel steps into the aisle → back up to the communion rail | 328 | 0 | 0.176 (one riser) | 0 | 0 | 5.47–10.75 |
| **New:** Gröna salen → the open west door → the nave aisle | 46 | 0 | 0.012 | 0 | 0 | 10.47–10.48 |
| Pass 130: chapel, west door → aisle → chancel → altar door | 117 | 0 | 0.14 | 0 | 0 | 10.46–10.75 |
| Pass 131: Gröna salen (east door → hall → chapel door → niche) | 204 | 0 | 0.18 (niche floor) | 0 | 0 | 10.47–10.65 |
| Pass 131: Förbrända salen | 241 | 0 | 0.015 | 0 | 0 | 10.46–10.47 |
| Pass 126: courtyard → portal E → Kungstrappan → Gyllene salen → Kungsmaket | 330 | 0 | 0.167 | 0 | 0 | 5.47–10.47 |
| Gate passage B → C | 120 | 0 | 0.021 | 0 | – | 3.70–5.49 |
| Portal C → D (pass 126's old target) / E / F (old target) | 35 / 42 / 187 | 0 | 0.012 | 0 | – | 5.47–5.48 |
| Pass 129: portal C → portal D's stair → landing | 125 | 0 | 0.163 | 0 | – | 5.47–5.96 |
| **New:** portal C → Kyrkportalen's slab path target (`to_F133`) | 206 | 0 | 0.012 | 0 | – | 5.47–5.48 |

In run 3 the new route had 6 obstructions (0.45 and 1.4 m) on the portal's full-width back plate in the doorway; the plate was split, and run 4 has none.

The earlier routes give the same numbers as in passes 129–131.
- `to_F` is pass 131's route to the old F target at the middle of SW, kept for comparison. It now ends in front of the windows that returned.
- `to_F133` is the slab path's new target in front of Kyrkportalen.

**Comparisons** (`SCR/p133/final/`):
- **`cmp_2017.jpg`** and **`cmp_2017_portalF.jpg`** (photograph | render, camera 689).
  - The portal stands where the photograph has it: render x 442–507 against 440–510 of 693, and 0.3–0.5 m from the corner.
  - The window over the tablet and the state-floor window above it are on its axis.
  - The photograph's portal is darker and its upper storey richer (carved herms, the cartouche's scrollwork).
- **Pano views** (720, 721), compared on screen with the live panoramas; no pixel of the panoramas is kept.
  - In pano 2 the portal spans x 590–733 with its top at row 400, and the corner downpipe is at 582. The render puts the portal at x 595–740 with its top at row 398, and the corner at 605. Pass 27's south corner is 0.5 m off, as pass 129 found.
  - The small window over the tablet: pano x 637–670, rows 375–399; render 655–688, rows 375–397.
- **Interior views:** `722.png` (vestibule and flight 1), `b_flight2.png` (flight 2 from the half landing), `723.png` (the open altar door from the chancel), `b_grona.png` (from Gröna salen through the open west door into the nave), `b_hall.png` (down flight 1).

**Official build:** done by the lead on 2026-10-03; see "Official build". The Unreal checks are pending.

## Mismatches and open issues

1. **Portal G is not modelled.** Olsson's south-west courtyard portal (fluted Doric columns, masks in the metopes) frames the walled-up south gate passage. Pano 2 sees it at about s 7.3–11.0 (door at about 9.1, before the 0.5 m corner shift). There is no door there in the model. It would need its own pass, with the walled-up passage.
2. **The ground-floor link is inferred.** The open sources draw only the state floor. A ground-floor or cellar plan (Riksarkivet PK006, Hawerman 1847, Litt B; reading room only) would settle whether Kyrkportalen opens straight onto the stair. That would make the stair a newel stair at the corner, as its name "vindelsten" suggests, and the museum plan's straight treads would then be a simplification.
3. **Room 13's size.** It is 2.55 m wide (s 28.70–31.25), limited at the outer end by the model's south tower. The museum plan's room 13 is narrower, and also opens on to room 14 and the tower chamber (15). Those openings and rooms are not built.
4. **The rest of the ground floor** under the chapel is not built (pass 27's hollow range). The vestibule and flight 1 are closed by a spine wall.
5. **Window sizes.** The window over the portal is 1.02 m wide in the panorama; the model's row is 0.90 m.
6. **Pass 27's south corner** is about 0.5 m off along SW (pano 2 and the photograph). Positions here are measured from the corner as seen in each view.
7. **Collision.** No Unreal collision test; the walk checks are Blender ray casts.

## Sources

| Source | Licence | Used for |
|---|---|---|
| Martin Olsson, "Kalmar slotts portaler och brunnsbyggnaden på slottets borggård", *Fornvännen* 1957, pp. 137–183 (DiVA diva2:1224675) | open access, no licence stated; read only, not copied | portal F's form, its name and its place as the eastern of the south range's two portals; portal G |
| Martin Olsson, *Fornvännen* 69 (1974), fig. 1 | in copyright; read only (pass 131's scratch copy) | the passage beyond room 86's altar end |
| Kalmar läns museum, "Kalmar slott, plan över praktvåningen" (KLMF.Slott003-57, DigitaltMuseum 021016586266) | no licence stated; viewed only | room 13 Sydöstra vindelstenen, its flight, the altar door; the door between Gröna salen and the chapel |
| Krigsarkivet 0424:058:212a, about 1780 (pass 130) | public domain | the chapel's two doors |
| Google Street View 2014, courtyard panoramas `zCIfieeXGQUNANmWu_Tg9A` and `jOXzkLldNOjrveyz1T81wg` | viewed only | portal F's place, width and heights; the window over it |
| `castle27/kalmar-castle-internal-courtyard-2017-07-30.jpg` (Commons 2017) | PD | portal F's place, the window column; comparison |
| Passes 27, 124–131 (`source/castle27.json`, `block127.json`, `block129.json`, `block130.json`, `block131.json`) | project | frames, outline, rows, doors, the chapel's envelope and doors |

No pixel of any panorama, photograph or drawing is used as a texture. The new materials (`M_Block133_*`: Plaster, Step, Flag, Oak, Stone, PortalStone, PortalTablet) are flat tints on TownPaintWhite, TownStone and TownPaintBrown.

## Official build

The lead built pass 133 officially on 2026-10-03.
- **Checks:** the geometry check passed on the second rebuild (True), the FBX audit passed (exit 0), and the two rebuilds gave identical meshes.
- **Prevhash:** only intended changes.
  - Pass 129's `SM_Kalmar_Slott`, `SM_Castle124_Portals` and `SM_Castle124_Paving`, and pass 130's `SM_Castle130_Slottskyrkan`, are re-created by this pass.
  - Pass 132's towers are identical.
  - The other entries are known earlier corrections.
- **Dry renders:** cameras 720–724, 5 of 5.
