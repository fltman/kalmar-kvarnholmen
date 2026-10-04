# Pass 125: the first interior rooms of Kalmar slott (Gyllene salen, Kungsmaket)

Pass 125 builds the first rooms inside Kalmar slott, in the way the project built the cathedral's interior (`scripts/build_interior.py`): closed architectural solids at real scale, flat-colour materials, cameras inside, and a walk check. The rooms are on the state floor (praktvåningen) of the west range, between the north round tower (Olsson's tower II, Kungsmakstornet) and Kuretornet:

- **Gyllene salen** (Olsson's room 59), Johan III's hall with the coffered ceiling of the 1570s;
- **Kungsmaket** (room 62), Erik XIV's chamber of about 1560, inside Kungsmakstornet;
- **a stand-in for room 61a** (Panelade salen, now part of Grå salen), which lies between the two. Olsson (1974) writes that this room served as Kungsmaket's anteroom ("försal"), so the two rooms do not adjoin; the walk from one to the other goes through 61a.

| Mesh | Category | What |
|---|---|---|
| `SM_Castle125_GyllenSalen` | Kalmar slott/Interiör | Gyllene salen: floor, walls, three window niches, fireplace, doors, frieze, coffered ceiling |
| `SM_Castle125_Kungsmaket` | Kalmar slott/Interiör | Kungsmaket: parquet, intarsia panelling, hunting frieze, cornice, ceiling, three niches, fireplace, the door passage to 61a |
| `SM_Castle125_Forrum` | Kalmar slott/Interiör | 61a: a plain room with a board floor and a beamed ceiling, and the doors to both rooms |
| `SM_Kalmar_Slott_Towers` | (pass 27/124's mesh) | **one box cut** out of the north tower's cylinder skin, where Kungsmaket's door passage crosses it |

No exterior mesh is moved or rebuilt. Pass 27 builds each range as a hollow shell (0.35 m skins outside its outline, plus the roof), so the rooms are closed solids standing inside that shell. The only exception is the north tower: pass 27 builds it as one closed cylinder, and Kungsmaket sits inside it, so the passage from Kungsmaket to 61a has to cross the cylinder's skin. The build cuts a box of 1.2 × 1.1 × 2.35 m out of the skin there (s −0.70…0.50, c −1.75…−0.65, z 10.42…12.77 in the room frame). The cut lies inside the west range, under its roof, so it cannot be seen from outside. The skin is split by four planes and the pieces inside the box are deleted. It removes 4 faces. Before cutting, the build probes 25 points on the cylinder inside the box; if no surface is left there, it skips the cut. So a second run changes nothing. **`SM_Kalmar_Slott_Towers` is listed in `block125_names` because it changes**; prevhash will report it.

## Frame and placement

All room geometry is built in one frame: s runs along pass 27's outer front of the west range, from outline point 55 at the north tower to point 56 by Kuretornet, and c points outwards. Pass 27's fitted range axis turned out to be 3.8° off that front. The first sandbox run used the fitted axis, and the rooms' outer walls stood up to 0.8 m outside the facade skin. The frame was changed to follow the front. `prepare_block125.py` checks that the whole envelope of Gyllene salen's walls lies inside pass 27's outline, clear of the courtyard ring and of Kuretornet's ring plus its 0.36 m skin (0.000 m² overlap each).

**Which rooms, where.** Olsson's plan in *Fornvännen* 69 (1974), fig. 1, was read on DiVA but not copied. It has a 0–100 m bar, which reads as 4.28 px/m in the DiVA scan. Along the west range, from tower II to Kuretornet, it shows 62 (in the round tower), 61a, 59 and then Kuretornet (56). In the plan:

- tower II's centre to Kuretornet's north-east face is 25.7 m; pass 27's OpenStreetMap model has 23.5 m;
- Gyllene salen is 13.4 × 13.5 m inside, which agrees with Mandelgren's nearly square ceiling plan;
- 61a is about 7.6 × 10 m;
- the walls are 1.6–2.0 m thick.

The plan's lengths along the range are scaled by 0.92 to fit the model. Gyllene salen becomes **12.4 m** along the range (s 4.6–17.0) by **12.9 m** across (c −15.0 to −2.1). Its south wall stands against Kuretornet's face; Kuretornet's skin reaches s 17.75, and pass 124's gate passage starts beyond s 18.9.

**Kungsmaket.** The 1780 plan of room 62 (Krigsarkivet, reproduced in Olsson 1964, fig. 15, read only) shows a room about 6.0 × 5.6 m, centred in the tower's thick walls (about 3 m). It has four openings:
- a wide window niche;
- a narrow passage on each of two opposite sides;
- the privy ("cloaque") recess.

The room is centred on pass 27's tower centre and aligned with the range. The window niche faces outwards (+c), which Olsson's plate calls "the west window niche"; it lies in the direction of the tower's free face. The +s passage is the door to 61a. The −s niche leads towards the small tower XII and is closed by a door. The −c niche is the privy recess, which the Olsson plate calls "the east niche".

**61a** lies between them, at s 0.3–3.2 and c −11.5 to −0.5. The model leaves only 2.9 m along the range for it, where the plan has 7.6 m, because pass 27's tower and Kuretornet are 2.2 m closer together than in the plan and Gyllene salen keeps its plan size.

**The floor (z 10.47, 11.80 m above the water).**
- Pass 27 measured the outer main-floor windows at 7.9–11.1 m above the castle foot (Street View, resected within 0.5 m), which is z 11.57–14.77.
- In both interior photographs of Gyllene salen, the glazing sill stands about one glass width above the floor: 1.0 widths in the Olsson plate of the 1930s, 1.3 in the 2009 panorama.
- So the floor is put 1.10 m below pass 27's sill.
- Kungsmaket and 61a share this floor. The 1780 plan and the panorama show no steps between the rooms.

## Measured, read from text, estimated

| Value | Source | Status | Result |
|---|---|---|---|
| Room order 62 – 61a – 59 – Kuretornet | Olsson 1974, fig. 1 and text | read from the plan | as built |
| Gyllene salen 13.4 × 13.5 m (plan), 12.4 × 12.9 m (model) | Olsson 1974, fig. 1, scaled at 4.28 px/m, then × 0.92 | measured on the plan (±0.5 m at this scan resolution) | s 4.6–17.0, c −15.0 to −2.1 |
| Kungsmaket about 6.0 × 5.6 m, walls about 3 m | 1780 plan (Olsson 1964, fig. 15), scaled on pass 27's tower diameter of 12.7 m | measured on the plan, relative scale | 6.0 × 5.6 m |
| Panelling 2.6 m high | SOURCES.md (Kalmar slott, Wikipedia) | from text, unverified | 2.6 m |
| Kungsmaket 4.3 m to the ceiling | panorama: the panelling is 0.6 of the wall height | measured on the photograph | 4.3 m |
| Floor 1.1 m below the outer sill | interior photographs: sill height in glass widths | measured on the photographs | z 10.47 |
| Gyllene salen 6.2 m to the coffer soffit | photographs: ceiling about 5.5 (2009) and 5.9 (1930s) glass widths above the floor; with pass 27's glass width of 1.15 m that gives 6.3–6.7 m. Capped so that the ceiling's top (z 17.12) stays below pass 27's top-floor windows (z 17.57) | measured, then capped by the exterior | 6.2 m, ceiling structure to 6.65 m |
| Ceiling layout 4 × 4 | Mandelgren 1848 (`dimu-021017081741.jpg`) | read from the drawing | 16 large coffers, 40 elongated, 25 node fields |
| Widths of the coffer bands | ceiling photograph 2017: elongated coffer about 0.35 of a large one, a flat strip between coffers | measured on the photograph (perspective, ±20 %) | band 0.9 m, coffer 0.7 m, strip 0.2 m |
| Coffer depth 0.23 m (large), 0.09 m (elongated) | photographs | estimated | |
| Niche width 2.2 m, head 4.85 m above the floor | 1930s plate: niche about 2 glass widths, its head about 0.6 m above the glass | measured on the photograph | |
| Window size 1.15 × 3.2 m | pass 27 | pass 27's value | |
| Kungsmaket niche 2.5 m wide, 1.6 m deep, springing 2.6 m | panorama | estimated from the photograph | |
| Fireplaces, door surrounds, frieze motifs, bosses, pendant | photographs | proportions estimated; shapes simplified | |

## What each room has

### Gyllene salen
- **Ceiling** (Mandelgren 1848; ceiling photograph 2017). Four by four large octagonal coffers (squares with chamfered corners), an elongated hexagonal coffer along every rib between two crossings, and an X-shaped flat field at every crossing. Each coffer stands 0.10 m inside its tile, so a flat cream strip 0.2 m wide runs between neighbours, as in the photograph.
  - **Large coffers**, from the soffit inwards: a red line, a wide sloping cream bevel, a gilt moulding, a grey-blue step, a gilt fillet, and a dark carved panel. On the panel are a gilt rosette and four leaves in gilt and red, as simple solids.
  - **Elongated coffers**: a red line, a cream bevel, a gilt moulding, and a panel with three gilt blocks.
  - **Crossings**: a gilt boss at every crossing, and the carved pendant at the central one.
  - **Construction**: every element is a closed solid up to a common top. The flat soffit between the coffers is triangulated in the prepare script (Shapely, constrained Delaunay, 482 triangles), so there are no large n-gons.
- **Frieze and cornice.** A grey painted frieze from the niche heads to the soffit, with:
  - red lines at its top and bottom;
  - two grey-blue scroll bands;
  - red winged beasts every 1.3 m (thin plates);
  - a cream and gilt cornice.
- **Walls.** Rough whitewash (flat colour), 2.1 m thick outside and 1.35–1.7 m thick elsewhere.
- **Windows.** Two deep niches in the outer wall on pass 27's window axes, and one niche in the courtyard wall on pass 27's courtyard window axis. Each niche has a raised stone floor, a soffit of small gilt-ribbed coffers with tiny bosses, and a stone window board. The glazing is a pale pane, 1.15 × 3.2 m, with a frame, a mullion and two transoms.
- **Fireplace** between the two west windows (panorama; Olsson plates of 1958): stone jambs, a mantel, a sloping hood under a pointed gable, three pinnacles, and a dark hearth.
- **Doors.**
  - The open door to 61a in the north wall, with a stone surround: jambs, frieze, cornice, a pediment and three ball finials (1930s plate).
  - Closed doors:
    - to Kuretornet (south wall), with the red painted surround seen in the panorama;
    - to the king's förstuga (55) at the south wall's east end, with a pedimented surround;
    - to 61b at the courtyard wall's north end, with a pedimented surround.
- **Floor.** Wide boards, 0.30 m, running towards the windows.

### Kungsmaket
- **Panelling.** A dark dado, intarsia fields with darker inner panels, fluted pilasters with gilt capitals, and an entablature with a gilt fillet up to 2.6 m.
- **Hunting frieze.** Painted landscape (green below, sky above) from 2.6 to 3.95 m, with low-relief running deer with antlers, hares and trees as convex plates (Johan III's stucco hunting frieze of 1572–73).
- **Cornice.** Dentilled.
- **Ceiling.** Flat intarsia bands with a dark inlay line and lozenges at the crossings, framing four by four sunk coffers. Each coffer has a gilt frame, a carved gilt boss and four leaf blocks.
- **West niche.**
  - an arched opening with a gilt archivolt;
  - a barrel vault in blue and gilt bands with two gilt ribs, and the painted medallion of about 1560 as a gilt and blue disc at the crown;
  - panelled sides, and benches with red cushions on both sides;
  - the window wall: a leaded window 1.4 × 2.3 m with mullion and transom and lozenge cames, with intarsia panels either side.
- **North and east niches.** Arched niches with blue and gilt vaults; the north one is closed by a door.
- **Fireplace** (panorama: black and carved). Ebony-coloured jambs with turned figures standing for the caryatids, a frieze, an overmantel with a gilt cartouche, and a cornice.
- **Floor.** Two-tone parquet in squares of 0.47 m. The photograph shows a diamond pattern; see Limitations.
- **The door passage to 61a.** 1.0 m wide and 2.25 m high, through the tower wall, plastered.

### 61a (stand-in)
- A board floor, plain plaster walls and a beamed ceiling 4.5 m high.
- The plain stone surround of the passage door on the 61a side.
- No window: pass 27 has no outer window in this stretch.

## Mismatches with the exterior (reported, not corrected)

1. **Gyllene salen's outer windows.** Pass 27 puts the main-floor windows of front 55–56 every 4.4 m, at s 3.62, 8.02 and 12.42; the interior follows 8.02 and 12.42.
   - In the 2009 panorama the two niches stand near the room's corners, at about 24 % and 85 % of the wall from the south. That is s ≈ 14.0 and 6.5, about 7.5 m apart, with the fireplace between them.
   - Pass 27's third window, at s 3.62, falls in the wall between Gyllene salen and 61a and is seen from neither room.
   - Pass 27's row comes from an even spacing rule, not from a measurement of each window.
2. **The courtyard side.**
   - **One window instead of two.** Pass 27's courtyard outline (OSM) turns the courtyard's north corner at s 13.3, so only the south 3.7 m of Gyllene salen's east wall faces the courtyard, and pass 27 has one window there (s 15.36). The 1930s plate shows two windows in that wall. Olsson's plan puts the courtyard's corner at Gyllene salen's north wall, about 7 m further north. The interior has one courtyard window, on pass 27's axis.
   - **Height.** Pass 27's courtyard first-floor windows (sill z 13.77) stand **3.3 m** above the state floor, while its outer windows stand 1.1 m above it. The photographs show both sides at the same height, so the interior uses the outer level on both sides. Behind the courtyard niche's pane, pass 27's courtyard window opening sits 2.2 m higher.
3. **Kungsmaket's window.**
   - Pass 27's only main-level window in the north tower points from the castle's centroid, 54° away from the west niche, towards the tower's outer diagonal.
   - The exterior has no window at the west niche. The niche's glazing stands inside the tower wall, 1.6 m from the room, without an opening behind it.
4. **The courtyard level.**
   - The state floor stands only 2.3 m above pass 27's courtyard (z 8.17). Kalmar slott's accessibility page gives 7 steps from the courtyard to the entrance and 24 more to the state floor, about 5 m.
   - Pass 124 already doubted the courtyard level, because its gate passage needs a 22 % ramp.
   - A courtyard about 2.5 m lower (about 7 m above the water) would put pass 27's courtyard windows about 0.6 m above the state floor, consistent with the outer row. It would also flatten pass 124's ramp to about 10 %.
   - This pass changes neither.
5. **Kungstrappan and the förstuga (55).**
   - In Olsson's plan these lie between Kuretornet and the courtyard front, where pass 124's gate passage now runs. The passage's vault crown at the courtyard end (about z 12.4) rises 1.9 m above the state floor.
   - So a förstuga at the state floor cannot be built over the passage with the present courtyard level. That is a third sign that the courtyard is too high.

## How a walker reaches the rooms

The rooms are enclosed inside the castle volume; no opening from outside is cut in this pass.
- Inside, the three rooms join: Gyllene salen → the stone-framed door in its north wall → 61a → the passage through the tower wall → Kungsmaket. The walk check below walks this route.
- **Recommended way in, for a later pass or for Unreal.** Kungstrappan (55), from courtyard portal E.
  - Portal E is pass 27's courtyard door on the west front, at about s 29.0, c −15.7 in this frame; pass 124 dressed it with pilasters and a pediment.
  - A stair inside, between Kuretornet's courtyard face and the courtyard front, climbs 2.3 m at today's levels (about 14 risers) to a förstuga at z 10.47.
  - From the förstuga, the closed pedimented door at Gyllene salen's south-east corner (c −13.3) opens into the hall.
  - This needs a clean opening in pass 27's courtyard skin behind portal E (its door is a blind leaf) and an answer to mismatch 5. Until then, Unreal can place the player inside Gyllene salen (camera 671's position) or teleport through the closed förstuga door.

## Cameras

The sandbox renders use the same positions as these cameras; the Workbench shadows are off in the sandbox copy, because a closed room is otherwise entirely in shadow.

| Camera | Where | Compared with |
|---|---|---|
| 671_Block125_Cal_GyllenePano | Gyllene salen centre, looking west (+c), 1.6 m | Baboş 2009 panorama, centre crop |
| 672_Block125_Cal_GylleneEast | near the south-west corner, looking east | Olsson plate, 1930s (`dimu-021017089031.jpg`) |
| 673_Block125_Cal_GylleneCeiling | looking up 42° to the south-east | Commons ceiling photograph 2017 |
| 674_Block125_Cal_KungsmaketPano | Kungsmaket, east side, looking at the west niche | Baboş 2009 panorama, centre crop |
| 675_Block125_Cal_KungsmaketCeiling | Kungsmaket centre, looking up | Olsson plate of the ceiling (`dimu-021017089028.jpg`) |
| 676_Block125_Forrum | 61a, looking towards the passage | – |
| 677_Block125_Gyllene_DoorNorth | Gyllene salen, towards the door to 61a | – |
| 678_Block125_Aerial_WestRange | aerial over the west range | – |

No camera is resected. The photographs have no known positions, so the cameras are placed by eye, as in pass 124.

## Verification

- **Prepare.** `KALMAR_GEO=SCR/pylib python3 scripts/prepare_block125.py` prints `BLOCK125_PREPARE_OK`:
  - every room lies inside pass 27's outline, outside the courtyard and outside Kuretornet plus 0.36 m (0.000 m² each);
  - Gyllene salen's wall envelope is clear of all three skins;
  - Gyllene salen and 61a lie outside the tower circle, and Kungsmaket inside it;
  - pass 124's gate passage edge (s 18.92) is clear of the south wall (s 17.70);
  - the ceiling's coffers plus the flat triangles cover the ceiling exactly (difference 0.000 m²).
- **Sandbox.**
  - Five runs, with prelude pass 124: `SCR/p125/log1.txt`–`log5.txt`. Runs 1–3 were the design iterations; runs 4–5 checked repeatability. Run 5, on the final files, prints `SANDBOX_DONE` without errors.
  - The sandbox needed a shim (`SCR/p125/sandbox125.py`). Pass 124's committed build asserts that `M_Castle27_Gate` exists, but the saved `Stortorget.blend` no longer has it: pass 124 removed its last user, the old gate block, so the material was not saved. The shim re-creates it from `M_Castle27_Trim` before pass 124 runs. **The lead should look at this, since an official rebuild from the saved blend may stop at the same assertion.**
- **`drop_degenerate_faces125`** (with the `_thin` test) runs on all four meshes after `s21_finish`. In runs 3–5 it removed 65 faces from Gyllene salen and 77 from Kungsmaket; these are bevel slivers on the thin plates and lathe tips. It removed none from 61a and none from the tower.
- **Export frame check** (`SCR/p125/build_block125_check.py`, the pass 123/124 wrapper's method): 0 invalid loops in all four meshes, and the test FBX export succeeded for 4 of 4. The exporter's fallback covers 344 loops in Gyllene salen, 52 in 61a, 12 in Kungsmaket and 204 in the towers, the same 204 as before the cut.
- **Walk check** (ray casts every 0.2 m; obstruction rays at 0.45 m and 1.4 m; a headroom ray of 2.0 m), from Gyllene salen's centre through the north door, across 61a, through the passage and into Kungsmaket's west niche: 138 samples, none missing, largest step 0.03 m (the board edges), no obstruction, no low headroom. Floor 10.44–10.47.
- **Repeatability.** Runs 4 and 5 execute the build a second time on the result of the first, as the official build does, and compare the vertex and face hashes of the four meshes.
  - In run 4 the tower mesh changed on the second run, because re-splitting the skin along the same planes added edges.
  - The probe described above was added. In run 5 all four meshes are identical after the second run: `REPEAT125 True`, and the second run reports `BLOCK125_CUT already open`.
- **Side-by-side comparisons** (`SCR/p125/sb3/`):
  - **`cmp_gyllene_pano.jpg`.** The two niches with their coffered soffits, the fireplace between them, the frieze with red beasts, the cornice and the ceiling's rhythm agree in arrangement. The niches stand closer together than in the photograph (mismatch 1), and the room reads somewhat higher.
  - **`cmp_gyllene_east.jpg`.** The pedimented doors and the ceiling pattern agree. The photograph shows two courtyard windows, the model one (mismatch 2).
  - **`cmp_gyllene_ceiling.jpg`, `cmp_gyllene_mandelgren.jpg`.**
    - These agree: the octagon, hexagon and node pattern, the cream bevels with gilt and grey-blue steps, the bosses and the pendant.
    - The real panels carry dense carved and gilded ornament, and the soffit has painted black arabesques. Here these are a few solids and flat colour.
  - **`cmp_kungsmaket_pano.jpg`, `sheet.jpg`.**
    - The arched niche with benches, the panelling, pilasters and entablature, the green and blue hunting frieze with animals, the dentilled cornice and the coffered ceiling agree in arrangement.
    - The niche's vault ornament is bands, not strapwork, and the intarsia is two tones, not pictures.
  - **`cmp_kungsmaket_ceiling.jpg`.**
- **Pending.** The official build and the Unreal checks are pending; the lead fills in the build results.

## Limitations, and what is not yet "AAA"

The user asked for an AAA interior. This pass gets the architecture, proportions and ornament layout from the sources, within the project's rule of flat-colour materials and no photo textures. It is not AAA yet. These steps remain:

- **Surface detail.**
  - Normal and roughness maps for rough whitewash, wide boards, gilding, carved panels and intarsia, as the cathedral's material passes made.
  - Sculpted or carved relief for the coffer panels, the pendant, the fireplace caryatids, the stucco animals and the vault strapwork, which are simple solids here.
  - Intarsia patterns, the frieze's painting and the soffit arabesques, which need either licensed texture work or hand-made patterns, since photographs may not be used as textures.
- **Light.** Window-sized light sources and Lumen setup in Unreal, as in the cathedral's quality pass 3.
- **Fit.**
  - Kungsmaket's parquet is a chequer, not the diamond pattern in the photograph.
  - 61a is a plain stand-in for the panelled room.
  - The outer window spacing follows pass 27 (mismatch 1).
  - Gyllene salen's ceiling height is capped by pass 27's exterior.
- **Furniture.** None, as in the cathedral's first pass: no chests, throne, portraits, tapestry or the king's bed (*konungssängen*) with its screen (*skranket*) shown on the 1780 plan.
- **Collision.** No collision test in Unreal; the walk check is a Blender check only.

**Left for later passes.**
- **Rooms:** Slottskyrkan; Gröna salen (Stora västra salen, south of Kuretornet); Grå salen (61a + 61b, done properly); Kungstrappan and the förstuga (55); Rutsalen and Drottningsalen (north range); Förbrända salen; Kungsköket; Kuretornet's rooms.
- **Access:** the opening from the courtyard via portal E.
- **Exterior corrections:** the courtyard level (mismatches 4 and 5), the outer and courtyard window rows (mismatches 1 and 2) and the tower window (mismatch 3).

**Views that would help:**
- inside Gyllene salen with a known camera position, to measure the ceiling height and the niches' positions directly;
- the west front of the west range between Kungsmakstornet and Kuretornet, square on, to count and place the main-floor windows; for example from the outer bailey at about local (−885, −262), heading 120, pitch 15.

## Sources

| Source | Licence | Used for |
|---|---|---|
| Olsson, *Fornvännen* 69 (1974), pp. 89–104, fig. 1 (DiVA) | open access, no licence stated, in copyright; **read only, not copied** | room order and positions, scale, Gyllene salen's size, wall thicknesses, 61a as anteroom |
| Olsson, *Fornvännen* 1964:4, fig. 15: 1780 plan of room 62 (Krigsarkivet) (DiVA) | as above; **read only** | Kungsmaket's size and niches |
| `dimu-021017081741.jpg`, Mandelgren 1848 | Public Domain Mark | the ceiling's 4 × 4 layout |
| `commons-kalmar-castle-golden-hall-ceiling-2017-07-30.jpg` | PD | coffer profiles, colours, bosses, pendant |
| `commons-kalmar-slott.gyllene-salen.jpg` (Baboş 2009) | CC BY 3.0 | the west wall, niches, fireplace, frieze, door, floor |
| `dimu-021017089031.jpg`, `dimu-021017081612.jpg` (Olsson plates) | Public Domain Mark | the east wall, pedimented doors, the förstuga portal |
| `commons-kalmar-slott.kungsgemaket.jpg` (Baboş 2009) | CC BY 3.0 | Kungsmaket's panelling, niche, frieze, fireplace, ceiling |
| `dimu-021017089028.jpg`, `dimu-021017436079.jpg` (Olsson plates) | Public Domain Mark | Kungsmaket's ceiling and the niche medallion |
| Kalmar slott, accessibility page | – | step counts (the courtyard-level check) |
| pass 27 (`source/castle27.json`) and pass 124 (`source/block124.json`) | project | frame, window rows, levels, the gate passage |

Google imagery was not used. No pixel of any photograph is used as a texture: the new materials (`M_Block125_*`, 25 of them) are flat tints on the town textures. The two Olsson PDFs were downloaded to the scratch directory only, to read, and deleted afterwards.

## Official build

The lead's build of pass 125 passed the Blender geometry checks and the FBX export, and two rebuilds gave identical meshes. Prevhash reports pass 124's SM_Kalmar_Slott_Towers as changed. That is intended: the passage is cut through the north tower wall into Kungsmaket. The other changes are the earlier intended ones.

Before the build, the lead made `scripts/build_block124.py` tolerant of pass-27 materials that are missing from the saved blend. M_Castle27_Gate has no users after pass 124 and is dropped on save, so it is now re-created from M_Castle27_Trim. No mesh uses it, so pass 124's geometry is unchanged; the repeatability hashes for pass 124 still match. The Unreal import and its checks are deferred.

Lead's review: the coffer grid, the room proportions, the frieze bands and the window niches match the photographs. The carved and gilt ornament, the intarsia and the painted frieze are represented only by simple solids and flat colours. Reaching the photographs' richness needs textures (painted and intarsia patterns, gilding), normal and roughness maps and sculpted relief.
