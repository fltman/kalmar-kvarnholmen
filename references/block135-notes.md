# Pass 135: Kalmar slott, portal G and Kungsköket

Pass 135 adds two things to Kalmar slott:
1. **Portal G**, the south range's second courtyard portal (Olsson's "sydvästra borggårdsportalen"), at the walled-up south gate passage.
2. **Kungsköket**, the king's kitchen (Olsson's ground-floor room 43), with its great hearth, walkable from the courtyard through its two exits.

| Mesh | Category | Status | What changed |
|---|---|---|---|
| `SM_Kalmar_Slott` | Kalmar slott/Castle | re-created, `detail_pass=135`, `corrects_pass=27,124,126,127,128,129,133` | G's arch is cut through the SW courtyard skin and drawn open (pass 126's `arch_open126`); the lower-row window behind G goes, the middle-row window over G returns with its sill on G's cornice; SE_w's two small arched courtyard doors (pass 129) are drawn open |
| `SM_Castle124_Portals` | Kalmar slott/Castle | re-created, `detail_pass=135`, `corrects_pass=124,126,129,133` | portal G added (`portal_g135`), with the walled-up passage behind it; B–F unchanged |
| `SM_Castle124_Paving` | Kalmar slott/Ground | re-created by the composition, `detail_pass=135`, `corrects_pass=124,126,129,133` | no geometric change (same hash) |
| `SM_Castle135_Kungskoket` | Kalmar slott/Interiör | new | the kitchen's shell, hearth, fireplace, ceiling |
| `SM_Castle135_KungskoketInventarier` | Kalmar slott/Interiör | new | iron bars and pot hooks, cauldrons, the drain's guard rail, a work table and benches, firewood |

No other mesh changes. The sandbox's `CHANGED135` lists `SM_Castle124_Portals`, `SM_Castle135_Kungskoket`, `SM_Castle135_KungskoketInventarier` and `SM_Kalmar_Slott`; the paving is re-created identically. `SM_Kalmar_Slott_Towers` and the rooms of passes 125, 126, 130, 131 and 133 are not touched.

**Method.**
- `build_block135.py` takes the slice of `build_block133.py` from `def rep133` to its `print('BLOCK133_PASS129_REBUILT', …)` line. That slice re-runs pass 129's composition (passes 124–129) with pass 133's edits. It runs in a private namespace (`NSP135`), with pass 133's materials mapped by name, not re-created.
- Pass 135's replacements on that slice are each asserted to occur exactly once:
  - the marking (`detail_pass=135`, the `corrects_pass` lists above, the asserts and print labels);
  - G's arch joins Kyrkportalen's door in the hole list of the SW edge CI2–CI1 (`=[list(DOOR133)]` → `=[list(DOOR133), G]`);
  - `EDITSRC135` on the composed source: doors in `OPEN135` are drawn with `arch_open126` (as `OPEN133`); the window filter becomes `filt135(holes, filt133(filt127(holes)))`; `EXTRA135` runs in pass 27's namespace after `EXTRA133`;
  - `edit_portals133` is wrapped by `EP135`: `PORT135` (`prism_uo135`, `portal_g135`) is inserted before `_doors={`, and `portal_g135(m)` is called just before the portals' `b124_finish(m)`.
- The kitchen is built inside two functions (`kitchen135`, `furnish135`), so no short name reaches the shared namespace.
- All positions are computed in `scripts/prepare_block135.py` and written to `source/block135.json` and `previews/block135-zones.json`.

## 1. Portal G

### Sources

- **Olsson 1957** (*Fornvännen*, pp. 137–183; as read by pass 133, not copied). The south range's courtyard front has two portals. F (Kyrkportalen) is the eastern one. G, the south-west portal, frames the walled-up south gate passage. It has fluted Doric columns and masks in the metopes.
- **Kalmar läns museum, "Sydvästra portalen på Kalmar slott"**, K.-G. Petersson 1960, DigitaltMuseum 021017057393 (KLMF.A15190), **PDM**. Now saved as `castle-sources/dimu-021017057393.jpg`. It shows the portal nearly square on from the courtyard, with the west courtyard corner and its downpipe at the right:
  - a fluted column on each side, on a tall pedestal;
  - a round arch with impost blocks and a keystone console;
  - an architrave, a frieze of triglyphs with masks (roundels) between them, a projecting cornice;
  - a double plank door with a transom, set back in the arch;
  - the middle-row window directly over the cornice, on the portal's axis; a segmental basement window at the right foot; a window at mid-height between the portal and the corner.
- **Street View 2014 pano 2** (`jOXzkLldNOjrveyz1T81wg`): pass 133 read G at about s 7.3–11.0 on SW (width 3.7 m) at a grazing angle.
- **No browser view this pass.** The claude-in-chrome extension was not connected, so the panoramas could not be viewed again. Camera 735 is set up for the lead's check (see Cameras).

### Reading the 1960 photograph

The scan (924 × 927 px) was read on a full-resolution crop with a pixel grid; no pixel is used.
- **Vanishing point of the front.** The cornice line ((190, 210) → (575, 265)) and the pedestal bases ((197, 740) → (535, 705)) meet at x 2343, row 518 (the horizon).
- **Projective fit along the front.** With the vanishing point known, image x maps to the position t along the front as x = 2343 + A/(t − t*). The two column axes (x 245 and 535) are t = 0 and 1. That gives A = −13 080 and t* = −6.234. The two columns' heights in the image (427 and 365 px) agree with this fit (depth ratio 1.17 against 1.16).

| Feature | x (px) | t (column spacings) | Metres (2.80 per spacing) |
|---|---|---|---|
| Portal frame, south / west edge | 185 / 575 | −0.173 / 1.164 | width **3.74** |
| Arch opening at the face | 273 / 495 | 0.085 / 0.844 | **2.13** (2.10 used), centred on the columns |
| Window over the cornice | 348 / 450 | 0.322 / 0.676 | 0.99, on the portal's axis |
| Corner downpipe | 765 | 2.055 | axis to corner **4.35** |
| Window towards the corner | 590 / 695 | 1.227 / 1.703 | 1.33, 2.0–3.4 m west of the axis |

- **Scale.** One column spacing is 2.80 m. Two independent readings agree: the window over the cornice on the model's 0.9–1.0 m middle row gives 2.82, and pano 2's 3.7 m portal width gives 2.77.
- **Heights** (vertical scale 116–127 px/m at the left column, from fits with focal lengths of 800–1200 px; 121 used):

| Part | Above the courtyard (m) |
|---|---|
| Plinth / pedestal die / pedestal cap | 0–0.20 / 0.20–1.05 / 1.05–1.17 |
| Column shaft to the capital's top | 1.17–3.53 |
| Architrave / frieze / cornice | 3.53–3.73 / 3.73–4.11 / 4.11–**4.40** (z 9.87) |
| Arch: springing / crown | **2.00** / 3.05 (photograph: 1.9–2.25 / 3.06–3.33) |
| Window over the portal: sill | 4.42 (the model's middle row is at 4.43, z 9.90) |

### Where it goes

- On the model's SW window column at **s 10.27**, where pass 27/127 have a lower-row and a middle-row window. The photograph's window over the cornice stands on the portal's axis, as at Kyrkportalen (pass 133).
- That puts the axis **4.20 m** from the model's west courtyard corner (CI0, s 6.07). The photograph gives 4.35 m from the corner downpipe.
- Pass 133's pano 2 reading was 8.6–9.2. That view is grazing, and pass 133 found a 0.5 m offset between the panorama's corners and the model's.
- The portal spans s 8.40–12.14; its arch is u 7.602 on the edge CI2–CI1 (whose end CI1 is at s 7.91). It is 11.2 m clear of Kyrkportalen.

### What is built (`portal_g135`, in `SM_Castle124_Portals`)

- A stone field round the arch (0.145 m proud of the face, so pass 126's open-arch trim of the facade is inside it); jambs, impost blocks and the arch ring (0.24 m) with a keystone console up to the architrave.
- Pedestals 0.80 m wide on plinths, a column (`column124`, r 0.17) on each side at ±1.40 m, capitals.
- Architrave, frieze with 9 triglyphs and 8 masks (each a block with a smaller raised block), cornice in two steps (W + 0.20 and W + 0.34).
- **The walled-up passage.** The arch is open through the courtyard skin. Behind it are a 0.30 m reveal (jambs and soffit, one prism with a triangulated cap), the blind masonry (`M_Block135_Infill`, 0.30 m), and on it the double plank door to the springing with a transom and a boarded tympanum (a triangle fan), and iron strap hinges. Nothing behind it is walkable; a ray from the courtyard through the arch meets the door 2.2–2.3 m in (`GBLIND135`).
- Materials: `M_Block135_PortalStone` (as F's weathered grey), `M_Block135_PortalDoor`, `M_Block135_Infill`, `M_Block135_Iron`.

### The facade

- G's arch is a door hole on the SW edge (2.10 m, springing 2.00, r 1.05), drawn open by `arch_open126`.
- Pass 127's rule (no window within 1.2 m beside a door or 1.6 m over its arch) removes the lower-row window at s 10.27 (behind the portal) and the middle-row window over it. **`filt135`** puts the middle-row window back with its sill on the cornice (z 9.89, head 11.10), as in the photograph.
- The basement window at G's foot and the mid-height window towards the corner are not in the model's rows and are not added.

## 2. Kungsköket

### Sources

- **DigitaltMuseum, Kalmar läns museum** (all **PDM**). Dagmar Selling's 1969 series "Bottenvåningen, östra längan rum 43 – Kungsköket" (021017090083–090103) shows each wall, the hearth, the flue and the drain. Two sketches (021017083364, 083365, the latter already here) show the hearth under the cross wall's arch and the beamed ceiling. The captions name the walls:
  - "Östra väggen … (sjösidan)": the east wall is the outer wall (the sea side);
  - "Västra väggen, mittpartiet med den sydliga utgången till borggården" and "Västra väggen, norra delen med den nordliga utgången till borggården": the west wall is the courtyard wall, with **two** exits, the southern one in its middle part;
  - "Spisen, östra väggen (från trappan i Norra muren)": a stair in the north wall;
  - "Trumma (avloppsränna) utmed Norra muren": a drain along the north wall;
  - "Norra murens övre del, sedd genom mellanväggens valv": a cross wall with a wide arch;
  - "Spisens södra sida", "Spisens norra del", "Skorstenspipa": the hearth seen from both sides, and the flue.
  - K. Pettersson's 1972–74 photographs (no licence stated, not saved) name "stora spisar" and "Sydliga dörrnischen".
- **Saved to `castle-sources/` with `sources.json` entries** (PDM, downloaded at 1200 px): `dimu-021017090086.jpg`, `-090089`, `-090090`, `-090101`, `-090103`, `dimu-021017083364.jpg`, and the portal photograph `dimu-021017057393.jpg`.
- **The museum's state-floor plan** (KLMF.Slott003-57, viewed only, as registered in `SOURCES.md`): room 16 "Salen över Kungsköket" lies between 15 (the south tower's chamber) and 17 (Förbrända salen).
- **Möller 1882** (`riksarkivet/PK006-00041`), "Profil genom s.k. Brända salen": under Förbrända salen the ground floor has a flat timber floor on posts, not a vault, and a vaulted cellar below. It is a section through SE_e, not through the kitchen (see below).
- **Status of the Lindegren sketch** (`dimu-021017083365.jpg`, 1969). It is a pencil perspective, not a measured drawing: two arched openings on two faces of a block (the hearth), a rubble base and beams. It is used only for the arrangement. Its sister sketch 083364 has the same block under a wide arch. A third sketch (083369) is captioned "bottenvåningen i södra längan"; it has no licence and was not used.

### Which range, and where in it

1. **Olsson's compass.** Olsson's "south range" is the model's SW range (the chapel), whose courtyard front faces true 216 + 180. His compass is therefore turned about 40° from true. His "east range" is the model's SE_w and SE_e, and their courtyard walls are his "west walls".
2. **Förbrända salen is not over the kitchen.** The museum plan has "Salen över Kungsköket" (16) as a separate room between the south tower (15) and Förbrända salen (17). Pass 131 put Förbrända salen in SE_e between the two bays, from the bend northwards. A museum photograph names the "door between rooms 76 and 82 in the east range": room 82 is the hall south of Förbrända salen.
3. **The two exits.** SE_w's courtyard front has exactly two small arched doors (pass 129, measured on the 2014 panoramas), at s 9.48 and 17.22. The southern one is at the middle of the front: "mittpartiet med den sydliga utgången".
4. **Result.** The kitchen is the ground floor of SE_w, from the south tower's corner to the wall under room 82's north end (where SE_e begins). Möller's section through SE_e (under Förbrända salen) shows a different room.

### Heights

- **Two window rows.** The model's SE_w courtyard front has two lower rows (pass 127, measured on Street View 2014): sills z 6.30 (1.25 × 1.20 m) and z 9.95 (1.25 × 1.15 m, a row that pass 127 noted crosses the other ranges' state-floor slab). The 1969 photographs of the west wall show exactly that: low windows, and high windows just under the ceiling.
- **Reading the photographs.** Read as fractions of the floor-to-ceiling height on the far wall:

| Photograph | Low sill | High sill | Floor | Ceiling |
|---|---|---|---|---|
| 090101, west wall south | 0.18 | 0.74 | z 5.13 | z 11.6 |
| 090103, west wall north | 0.15 | 0.70 | z 5.30 | z 11.9 |

- **Steps.** Both photographs show steps up into the exits (three in 090101).
- **Pass 127** also measured SE_w's upper windows 1.3 m higher than the other ranges' (sill 12.9). The hall over the kitchen stands higher.
- **Built:** floor **z 5.10**, three risers of 0.127 m down from the threshold (ZC + 0.012); joists z 11.18–11.43; boards to **z 11.55**, under the facade's state-floor row (sill 11.57).
- **This departs from the brief's ceiling at z 10.17.** The evidence above puts the kitchen ceiling about 1.4 m higher. SE_w has no state-floor slab or room in the model, so nothing clashes; Förbrända salen's floor (z 10.17–10.47) is in SE_e, 0.38 m from the kitchen's envelope in plan. If a later pass builds "Salen över Kungsköket", its floor should go on z 11.55 or higher.

### What is used

| Value | Source | Status | Model |
|---|---|---|---|
| Range and ends | the reasoning above; pass 27's outline | from the model | SE_w, s 1.80–18.40 (south wall face by the south tower, north wall face under room 82's north end) |
| Width | range depth minus walls | fitted | 9.0 m (south) to 10.5 m (north); courtyard wall 2.0 m, outer wall 2.3 m |
| Floor, ceiling | photographs, facade rows | measured ±0.2 m | z 5.10 / 11.18–11.55 |
| Exits | pass 129's doors | from the model | s 9.48 and 17.22, 0.95 m wide; niches 1.35 m wide, flat head z 8.00; landing at the threshold, two treads, the floor |
| Window niches | the facade's glass (saved scene, `SCR/p135/dump135.py`) | from the model | courtyard lower row s 2.45, 6.25, 13.84 (sill 6.30); courtyard upper row s 2.45, 6.25, 10.05, 13.84, 17.64 (sill 9.95); outer s 4.02, 9.02, 14.01 (sill 8.52, 0.62 m) |
| Cross wall | photographs 090084, 090086, 090089; sketch 083364 | position estimated | s 11.45–12.45 (between the window columns 10.05 and 13.84), arch 7.5 m wide, springing z 6.90, crown z 9.70 |
| Great hearth | photographs 090088–090090; sketches | estimated | 3.6 × 3.0 m brick stack, 0.5 m walls, to z 7.70; two arches on the long faces (1.10 m, springing +1.25), one on the short faces (1.20 m); a fire bed; a tapering hood to z 9.54 and the flue into the arch's crown |
| Small fireplace | photograph 090100 ("södra väggen, västra delen") | estimated | in the south wall, 2.0 m from the courtyard wall face: a 2.8 m breast to z 7.50 with a 1.6 m arched opening, a hood to the joists |
| Stair in the north wall | captions 090086, photograph 090083 | estimated | 1.1 m niche by the east corner, four risers of 0.18 to a closed plank door |
| Drain | 090085 | estimated | along the north wall, 0.50 m wide, 0.12 m deep |

### What is built

**`SM_Castle135_Kungskoket`**
- Walls: four wall pieces (courtyard, outer, south, north) cut from the envelope in `prepare_block135.py`, in horizontal bands. In each band the niches, exits and the stair that are open there are cut out (Shapely). Every band is a closed prism with triangulated caps. The envelope stops 0.05 m short of pass 133's stair hall and pass 130's chapel at the south courtyard corner, and of the towers and bay1.
- Splayed window niches through the walls to the facade's glass, with a white frame, mullion and transom at the glass (pass 27's glass stands in the skin behind).
- The exits: the skin's arch is open; inside are a landing at the threshold, two treads and the floor. Each plank leaf stands open against its niche's side.
- The cross wall with its wide arch (a vertical-plane prism), up to the joists.
- The great hearth under the arch: four brick walls with round-headed openings, a fire bed, a soot-dark top, a stone plinth, the white hood (a frustum) and the flue box into the cross wall's crown.
- The small fireplace in the south wall, the drain with stone curbs, the stair in the north wall with its closed door.
- 18 dark joists across the range (0.22 × 0.25 m at 0.90 m) and a board ceiling.
- Materials: `M_Block135_Lime`, `Reveal`, `Brick`, `Soot`, `Cobble`, `Flag`, `Drain`, `Joist`, `Board`, `Plank`, `Frame`.

**`SM_Castle135_KungskoketInventarier`**
- Iron trammel bars across the hearth's four long-face arches, with pot hooks (photographs 090088, 090090).
- Two cauldrons (one on the fire bed, one on the floor).
- The timber guard rail along the drain (photographs 090083, 090097, 090103).
- A work table with two benches by the outer wall, and a stack of firewood by the courtyard wall. These two are estimated: the 1969 photographs show a work site, not a furnished kitchen.

## Cameras

| Camera | Where | Look | Compared with |
|---|---|---|---|
| `735_Block135_Cal_Pano2_PortalG` | pano 2 (−860.06, −308.67), ZC + 1.9 (pass 128's resection) | true 229.37 (**URL 232h**), pitch 5, vfov 40 | Street View 2014 pano 2 — **not compared** (no browser this pass) |
| `736_Block135_Cal_Photo1960_PortalG` | SW s 14.31, 9.6 m in front of the face, ZC + 2.1 | 27.8° right of square on, pitch 3.1, vfov 50.1 | the 1960 photograph 021017057393 |
| `737_Block135_Kungskoket_Hearth` | SE_w s 16.9, c −5.0, floor + 1.5 | south at the hearth under the arch, pitch 9, vfov 64 | 090089 ("Spisens norra del"), by eye |
| `738_Block135_Kungskoket_WestWall` | SE_w s 8.6, c −2.4, floor + 1.5 | west at the courtyard wall, pitch 8, vfov 66 | 090101 ("västra väggen, södra delen"), by eye |
| `739_Block135_Aerial_SouthCourtyard` | over the courtyard | SE_w's front and the SW front with G | – |

Camera 736 comes from the projective fit (yaw 27.8°, pitch 3.1°, f 991 px), with its distance and height set on sandbox run 2: run 2's camera at 8.0 m made the portal 20 % too large.

## Estimated

- G: the scale (2.80 m per column spacing, two agreeing readings), the column and pedestal sizes, the frieze's masks as blocks, the recess's depth (0.30 m) and the door. The arch is built centred, although in the photograph it may sit slightly towards the south column.
- The kitchen's range and extent: inferred from captions, the museum plan and the model's doors. No ground-floor plan was found.
- The position of the cross wall, the hearth and the small fireplace along the room; the hearth's size; the north-wall stair; the drain; all furnishings.
- The wall thicknesses (2.0 and 2.3 m).

## Verification

### Prepare

`KALMAR_GEO=<pylib> python3 scripts/prepare_block135.py` prints `BLOCK135_PREPARE_OK`. It asserts:
- the kitchen's envelope inside pass 27's body and outside the courtyard, the four towers plus 0.36 m and the two bays (0.000 m² each);
- no overlap with pass 125's rooms (38.6 m away), pass 126's stair strip (26.8 m), Gröna salen (21.9 m), Förbrända salen (0.38 m), pass 133's stair hall (0.05 m) or pass 130's chapel (0.30 m);
- every niche, exit and the stair inside its own wall piece, 0.15 m clear of each other, of the cross wall and of the fireplace;
- the hearth and its plinth inside the arch's opening, the hood under the arch (the flue meets the crown), passages of 1.66 m on both sides of the hearth, 3.27 m headroom under the arch in the east passage;
- the walk route in the room, the exits or the courtyard, clear of the hearth, the drain and the cross wall's piers (0.3 m);
- the ceiling's top under the facade's state-floor row (0.02 m);
- G's arch inside its edge, the portal on the front (CI1 at s 7.91), 11.2 m from Kyrkportalen, the window over it 0.03 m above the cornice; the recess inside the body and clear of Gröna salen and pass 133's stair hall.

### Sandbox

Three runs with `SCR/p135/build_block135_check.py` (it builds twice and runs all checks) and `SCR/p135/sandbox135.py` (pass 133's copy, Workbench shadows off), prelude 133. Logs: `SCR/p135/log1.txt`–`log3.txt`.
- **Run 1** built, passed the change-set, repeatability, placement and export checks, then stopped in the walk section (a name from pass 133's wrapper, `_ST`, was not copied).
- **Run 2** printed `SANDBOX_DONE prelude 133`. The new kitchen walk had 13 obstructions: the courtyard leg passed through the well house, one point stood on a bench, and the west passage's route point was in the cross wall's pier (a sign error in the prepare script). The route was fixed (a waypoint west of the well; the pier check added to the prepare script). Camera 736 was moved back.
- **Run 3** is the final run on the final files; the numbers below are run 3's.

**Change set and repeatability** (run 3):
- `CHANGED135 ['SM_Castle124_Portals', 'SM_Castle135_Kungskoket', 'SM_Castle135_KungskoketInventarier', 'SM_Kalmar_Slott']`; the paving is re-created with the same hash;
- `REPEAT135 True`; the second run changes nothing.

**Polygons and degenerate faces.**
- `SM_Kalmar_Slott` 313,159 faces, Portals 10,638 (with G), Paving 1,040, Kungskoket 6,134, furnishings 1,964.
- `drop_degenerate_faces135` (and pass 133's own filter inside the composition) removes 0 faces from each of the five meshes.

**Export frame check** (pass 131/133's wrapper: the export tail's preparation, the exporter's frame test, a test FBX export of each mesh):
- 0 invalid loops; 5 of 5 exports succeeded.
- Fallback frames: `SM_Kalmar_Slott` 5,658 loops, Portals 0, Paving 15, Kungskoket 175, furnishings 3.

**Placement.**
- Every vertex of both kitchen meshes lies in the envelope and in z 4.80–11.55 (`EXTENT135`, 0 outside; the furnishings reach z 6.41).
- `INTRUDE135`: no vertex of any other mesh in the kitchen's envelope or G's recess, except the facade's open-arch thresholds (24 and 6 vertices at z 5.47–5.48; see open issue 7).
- `GBLIND135`: rays from the courtyard through G's arch at 1.0 and 2.0 m meet `SM_Castle124_Portals` (the door on the infill) 2.30 and 2.21 m in.
- No kitchen vertex is above z 15.5 (`ROOFCLEAR`).

**Walk checks.** Ray casts every 0.2 m, obstruction rays at 0.45 and 1.4 m, a 2.0 m headroom ray.

| Route | Samples | Missing | Largest step | Obstructions | Low headroom | Height |
|---|---|---|---|---|---|---|
| **New:** gate passage's courtyard end → west of the well → the south exit → down its steps → the south part → the east passage under the arch → the north part → the west passage back → the north exit → up its steps → the courtyard | 423 | 0 | 0.128 (one riser) | 0 | 0 | 5.10–5.48 |
| Pass 133: courtyard → Kyrkportalen → stair → altar door → chancel → aisle → rail | 328 | 0 | 0.176 | 0 | 0 | 5.47–10.75 |
| Pass 133: Gröna salen → west door → aisle | 46 | 0 | 0.012 | 0 | 0 | 10.47–10.48 |
| Pass 130: chapel | 117 | 0 | 0.14 | 0 | 0 | 10.46–10.75 |
| Pass 131: Gröna salen / Förbrända salen | 204 / 241 | 0 | 0.18 / 0.015 | 0 | 0 | 10.46–10.65 |
| Pass 126: courtyard → portal E → Kungstrappan → Gyllene salen → Kungsmaket | 330 | 0 | 0.167 | 0 | 0 | 5.47–10.47 |
| Gate passage B → C | 120 | 0 | 0.021 | 0 | – | 3.70–5.49 |
| Portal C → D (old) / E / F (old) | 35 / 42 / 187 | 0 | 0.012 | 0 | – | 5.47–5.48 |
| Pass 129: portal C → D's stair → landing | 125 | 0 | 0.163 | 0 | – | 5.47–5.96 |
| Pass 133: portal C → Kyrkportalen's slab path target | 206 | 0 | 0.012 | 0 | – | 5.47–5.48 |

The earlier routes give the same numbers as in pass 133.

**Comparisons** (`SCR/p135/final/`):
- **`cmp_g1960.jpg`** (photograph | camera 736). The portal's proportions, the single fluted columns on tall pedestals, the triglyph frieze, the cornice, the window on the cornice and the set-back double door agree. In the render the corner stands somewhat nearer the portal (0.71 of the frame against 0.82); the camera is fitted, not resected.
- **`cmp_hearth_090089.jpg`**, **`cmp_hearthsouth_090090.jpg`**: the hearth under the wide arch, with arched openings and the hood rising into the crown. The photographs' stack is rounder and rougher.
- **`cmp_westwall_090101.jpg`**, **`cmp_westnorth_090103.jpg`**: the courtyard wall with low windows, high windows under the ceiling, the exits up a few steps, the dark joists. The photographs show one high window where the model has the facade's columns (three on the south part).
- Other views: `klong.png` (along the room), `kdoor.png` (the open south exit from the courtyard), `kstep.png` (the exit's steps), `gsq.png` (G square on), `739.png` (aerial), `735.png` (pano 2 at G, not compared).

### Pending

The official build is done (see "Official build"); the Unreal checks are pending.

## Mismatches and open issues

1. **The kitchen's height departs from the brief** (ceiling z 11.55, not 10.17); see Heights. A later "Salen över Kungsköket" must start at or above z 11.55.
2. **No ground-floor plan.** The kitchen's ends, the cross wall's place and the hearth's size are read from photographs. A ground-floor plan (Riksarkivet PK006 00003–06, Litt B, reading room only) would settle them, and whether the room is one space or two.
3. **Camera 735** (pano 2 at G) was not compared: the browser extension was not connected. Suggested check: pano `jOXzkLldNOjrveyz1T81wg`, URL 232h, 40y, 95t.
4. **G's photograph details not modelled:** the basement window at its foot, the mid-height window between the portal and the corner, the carved masks and the scrollwork; the photograph's door may be recessed deeper than 0.30 m.
5. **The 1960 camera** is fitted, not resected: the focal length is assumed (991 px), so its distance (9.6 m) was set by eye on the render.
6. **The SE_w door on the outer front** (pass 27's rule, s 9.0, sill z 3.67) stays a closed facade door with the kitchen's solid outer wall behind it. The 1969 photographs show no door in the east wall.
7. **Thresholds.** The facade's open-arch thresholds (pass 126's `arch_open126`, 0.012 m slabs) reach 0.02 m behind the courtyard line, inside the kitchen's envelope and G's recess (`INTRUDE135`: 24 and 6 vertices at z 5.47–5.48). They are the walking surface at the doors, not an obstruction.
8. **Hearth form.** The photographs show rounded corners and a conical hood; the model has a square stack and a four-sided hood.
9. **Collision.** No Unreal collision test; the walk checks are Blender ray casts.

## Sources

| Source | Licence | Used for |
|---|---|---|
| Kalmar läns museum, "Sydvästra portalen på Kalmar slott", K.-G. Petersson 1960 (DigitaltMuseum 021017057393; `castle-sources/dimu-021017057393.jpg`) | PDM | G's form, size and place; camera 736 |
| Kalmar läns museum, D. Selling 1969, "Bottenvåningen, östra längan rum 43 – Kungsköket" (DigitaltMuseum 021017090083–090103; saved: 090086, 090089, 090090, 090101, 090103; 090102 already saved) | PDM | the kitchen: walls, exits, hearth, cross wall, stair, drain, heights; comparisons |
| Kalmar läns museum, sketches of room 43 (021017083364 saved; 083365 already saved) | PDM (a drawing; treated with care) | the hearth under the arch, the beamed ceiling |
| Kalmar läns museum, K. Pettersson 1972–74 (021017034828, 035034, 034986) | no licence stated; titles read only | "stora spisar", "sydliga dörrnischen" |
| Kalmar läns museum, "Kalmar slott, plan över praktvåningen" (KLMF.Slott003-57) | no licence stated; viewed only (pass 133) | room 16 "Salen över Kungsköket" beside 17 Förbrända salen |
| Martin Olsson, *Fornvännen* 1957 (as read by pass 133) | read only | portal G's description and its place at the walled-up gate passage |
| C. Möller, "Calmar slott. Profiler", 1882 (PK006-00041) | public domain | the ground floor under Brända salen (SE_e): a timber floor, not a vault |
| Google Street View 2014, pano `jOXzkLldNOjrveyz1T81wg` (pass 133's reading) | viewed only (by pass 133) | G's width and approximate place |
| Passes 27, 124–133 (`castle27.json`, `block127.json`, `block129.json`, `block130.json`, `block131.json`, `block133.json`) and the saved scene's facade glass | project | frames, rows, doors, neighbours |

The DigitaltMuseum metadata was read through its public API. No pixel of any photograph or drawing is used as a texture. The new materials (`M_Block135_*`, 17 of them) are flat tints on TownPaintWhite, TownTileRed, TownStone, TownPaintBrown and TownMetalGrey.

## Official build

The lead built pass 135 officially on 2026-10-03.
- **Geometry and export:** the geometry check passed on the second rebuild (True), the FBX audit passed (exit 0), and the two rebuilds gave identical meshes.
- **Prevhash:** only intended changes.
  - From pass 133, `SM_Kalmar_Slott` and `SM_Castle124_Portals` changed; `SM_Castle124_Paving` was re-created with the same hash.
  - Pass 134's 45 meshes are identical.
  - The rest are known earlier corrections. `SM_Castle130_Slottskyrkan` is listed because pass 133 re-created it.
- **Dry renders:** cameras 735–739, 5 of 5.
