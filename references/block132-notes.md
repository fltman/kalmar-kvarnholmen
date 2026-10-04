# Pass 132: Kalmar slott, the tower caps

Pass 132 rebuilds the copper caps of the castle's five towers after Carl Möller's drawings for new tower roofs of 1885 and checks them against today's photographs. Pass 27 modelled the caps by eye from aerials and Street View. Passes 124, 125 and 126 re-created `SM_Kalmar_Slott_Towers` but left the caps alone. This pass re-creates the mesh again with new caps:

| Mesh | Status | How |
|---|---|---|
| `SM_Kalmar_Slott_Towers` | re-created, `corrects_pass='27,124,125,126'`, `detail_pass=132` | pass 126's composition of pass 124's code (which re-runs pass 27's towers section), in a private namespace, with only the towers section run and two asserted replacements: the round towers' cap loop becomes `caps132(...)`, and Kuretornet's roof (from `# Square bell roof in copper:` to `c27_finish(m)`) becomes `kure132(...)`. Pass 125's cut for the door into Kungsmaket is applied again afterwards. |

No other mesh changes. The tower bodies, wall tops, cornices, windows, Kuretornet's walls and portal B, `SM_Kalmar_Slott` (ranges and roofs), the portals and the interiors (passes 125, 126, 130 and 131) are untouched.

## Sources

**Carl Möller, "Ritning till nytt tak å …", Riksarkivet, Överintendentsämbetet, dossier PK006, sheets 00048–00052, May–September 1885 (public domain).** Each sheet has an elevation, a plan and a section, a scale bar in fot (1 fot = 0.2969 m), and written dimensions. A note says the timber sizes are in verktum and everything else in fot and decimal lines.

| Sheet | Title on the sheet | Drawn | Model tower |
|---|---|---|---|
| PK006-00048 | Vattentornet | May 1885 | Kuretornet (`KRECT` in pass 27) |
| PK006-00049 | norra tornet | July 1885 | N |
| PK006-00050 | Södra tornet | August 1885 | S |
| PK006-00051 | Vestra tornet | August 1885 | W |
| PK006-00052 | Östra tornet | September 1885 | E |

**Photographs (working references only, no pixels used):**
- `castle27/kalmar-castle-internal-courtyard-2017-07-30.jpg` (Commons 2017, PD). This shows the south tower's cap. Camera: pass 127's resection.
- `castle27/swe-kalmar-slott-006.jpg` (-wuppertaler 2022, CC BY-SA 4.0). This shows the east tower's cap. Camera: pass 129's resection.
- `castle27/kalmarcastlejuly2019.jpg` (Iamstockton 2019, CC BY-SA 4.0). A drone view from the east-north-east showing all five caps.
- `castle27/kalmar-slott-fr-n-ovan.jpg` (Baiduzha 2020, CC BY-SA 4.0). This shows Kuretornet's cap close up.
- `castle27/schloss-kalmar-senkrecht-luftaufnahme-2021-.jpg` (HaSe 2021). An oblique aerial.

No Street View or satellite imagery was opened for this pass, and the browser was not used.

## Which tower is which

- **"Vattentornet" is Kuretornet.**
  - It is the only square tower. Its sheet has a square bell roof with four lucarnes, four corner aedicules, an open octagonal lantern, a dome, a bulb, a ball and a crown. This is exactly the cap of the square gate tower in every photograph, for example the 2020 aerial: square copper bell, round-headed lucarnes, small corner pinnacles, an open lantern and a gilded crown.
  - Its height on the sheet fits too. The crown stands 91 fot (27.0 m) above the eaves, so with pass 27's cornice at 32.0 m above the water the crown reaches 59.0 m. Pass 27 measured Kuretornet's crown at 59.0 m from Street View.
  - The museum's state-floor plan also uses the name "Vattentornet" here. Olsson's tower III Vattentornet is a different tower, but the 1885 sheet names follow the 19th-century usage (see `castle-sources/SOURCES.md`).
  - The brief's guess, "the big square keep, likely Kungsmakstornet or Kärnan", does not fit. Kungsmakstornet is Olsson's tower II, the model's north round tower, where pass 125 put Kungsmaket.
- **Norra, Södra, Västra and Östra tornet are the model's N, S, W and E.** The evidence:
  1. **The cap shapes in the 2019 drone view**, which looks from the east-north-east with Stadsparken's woods behind and the sound on the left. Left to right: the S cap (bell, dark drum, ogee dome), the E cap in front (bell, drum, cushion, bulb), the W cap far behind (bell, drum, tall pear bulb), Kuretornet, and the N cap on the right (a low wide bell, drum and small onion). Each matches the sheet of the same name.
  2. **The two courtyard photographs.** Their cameras were resected by pass 127 and pass 129 without reference to the caps. They show the Södra sheet's cap (2017, camera heading 174.9: closed octagonal drum, ogee dome, small lantern, fleur and vane) and the Östra sheet's cap (2022, heading 81.5: drum, block, faceted cushion and bulb, dark disc, ball, fleur, vane).
  3. **The drawn wall diameters** rank as the model's OSM radii do, except E: S 41.2 > N 39.7 > W 37.7 fot, against the model's S 13.44 > N 12.70 > W 11.73 m. E is drawn at 40.1 fot, but the model's E radius is the smallest, 11.36 m. That is either OSM or the sheet; this pass does not change the walls.
  4. **The heights.** Pass 27 measured the W and S finials from Street View at 44.2 and 42.6 m above the water. Möller's caps put them at 44.6 and 42.85 m (+0.40 and +0.25 m).

## Measurement

The sheets were read on full-resolution crops (about 11,100 × 7,300 px; `SCR/p132/cr.py`). Scales:
- **Vattentornet:** the written vertical chain (9.00, 9.00, 11.25, 4.25, 10.00, 3.50 fot) gives 52.0–52.7 px/fot, and the bar gives 52.2 px/fot (0–40 fot at x 4613/5144/5658/6177/6701).
- **Norra:** 10.50 and 8.15 fot give 52.2 and 53.0 px/fot, read at 52.5.
- **Södra:** the 9.00 fot drum gives 51.9 px/fot, read at 52.5.
- **Västra:** the 9.75 fot bulb gives 52.7 px/fot, read at 52.6.
- **Östra:** the 9.80 fot bulb gives 51.9 px/fot, read at 52.2.

**How the profiles were read.**
- **Bell outlines** were traced automatically (`SCR/p132/prof.py`): the right-hand outline, as the darkest non-red pixel per row every 25 px (0.48 fot). They were cleaned by hand where a dimension line, the corner aedicule or text stood in the way, and at the shoulder under the drum.
- **Plinths, drums, necks, bulbs, balls and finials** were read point by point. Precision is about ±0.2 fot (6 cm).
- **Reference levels.** Heights are measured from the eaves line, the top of the cornice where the copper starts. In the model this is pass 27's wall top `z1`, and `ZK` for Kuretornet.
- **Read against written totals.** N 60.0 against 60.50 written, S 58.1 against 57.90, W 65.0 against 65.20, E 67.9 against 67.30 (E before this pass's change to the neck), Kuretornet 87.8 against 88.0 to the crown's base.

### Kuretornet (Vattentornet), in fot from the eaves

| Part | Heights | Widths | Model |
|---|---|---|---|
| Wall at the top, eaves | wall 47.0, eaves 48.9 wide; cornice 1.25 + 1.25 with consoles; five openings 3.25 wide, 5.00 high | | walls are pass 27's; the bell's base is fitted to the model's 17.1 × 16.0 m wall plus 0.62 m for the cornice |
| Bell, square, concave-convex | 0 → 23.5 | half-width 24.45 at the eaves, 20.2 at 3.4, 18.4 at 9.9, 17.6 at 16.4, 15.8 at 21.0, 13.7 at 23.3 | horizontal scale runs from the model's eaves (0.36/0.34 m per fot) to Möller's 0.2969 at the top |
| Lucarnes, one per face | base 0.5–2.15; columns to 10.6; entablature 10.6–12.8; round head with fan, r about 3.9, to 17.2; finial to 21.8 | 7.60 over the capitals, 7.10, 4.90; opening 3.70; volutes to a half-width of 6.2 | front plane at 21.0 fot (scaled) from the axis |
| Corner aedicules | pedestal 0–2.50, column 2.50–10.75 (Ø 1.10, capital 1.35), entablature to 12.85 (2.10), box to 16.85 (4.00), finial to 22.05 (5.20) | centre 22.97 from the axis | on the wall's corners, 0.16 m inside; the entablature runs back into the bell |
| Plinth, octagonal | 23.5 → 30.5 (7.00) | 25.00 base, 17.65 waist, 20.50 torus, 17.65 top | |
| Lantern, open, octagonal | 30.5 → 41.0 (10.50) | 16.50 over the columns, 6.85 a face, 15.75 inside; arched openings 3.00 wide | paired columns at each corner, arches springing at 37.2 |
| Entablature | 41.0 → 44.5 (3.50) | cornice 19.6 | |
| Dome, octagonal, bell-shaped | 44.5 → 54.5 (10.00) | 19.6 at the base, 13.1 at 5.0, 9.5 at 8.4 | ribs on the eight corners |
| Neck | 54.5 → 58.75 (4.25) | waist 3.20, torus 6.4 | |
| Bulb | 58.75 → 70.0 (11.25) | 6.40 | |
| Ball | 70.0 → 79.0 (9.00) | ball 4.75 with a band | |
| Rod, plate, candelabra (three small crowns) | 79.0 → 87.8 (9.00) | arms 6.0 across | |
| Crown | 87.8 → about 90.9 | 3.1 | gilt (pass 27's `Gold`) |

### Round towers, in fot from the eaves

| | N (Norra) | S (Södra) | W (Västra) | E (Östra) |
|---|---|---|---|---|
| Wall drawn / model | 39.7 / 42.8 (r 6.349 m) | 41.2 / 45.3 (r 6.719) | 37.7 / 39.5 (r 5.865) | 40.1 / 38.3 (r 5.678) |
| Eaves, valance | eaves 42.3; cornice 1.20; no valance | eaves 44.3; cornice 1.20 + valance 1.80 | eaves 42.2; cornice 1.20 + valance 2.60 | eaves 43.3; cornice 1.20 + valance 1.80 |
| Bell: height, sides (plan) | 18.0, 12 | 17.5 (17.7 read), 16 | 19.25 (19.1 read), 10 | 19.0 (19.2 read), 16 |
| Bell half-widths at h 0 / 4.8 / 9.5 / 14.3 / top | 21.4 / 16.5 / 15.2 / 13.4 / 7.6 | 22.2 / 16.0 / 14.3 / 12.4 / 7.6 | 20.1 / 15.8 / 14.4 / 13.0 / 7.5 | 21.5 / 15.7 / 14.1 / 12.7 / 7.6 |
| Drum (closed, with corner pilasters) | flare 2.75 from the 14.40 plate; drum 7.50 high, 8.20 wide, 10 sides | 9.00 high, 14.00 wide, 8 sides; cornice 16.2 | 8.25 high, 13.7 wide, 12 sides; cornice 15.0 | 9.00 high, 14.00 wide, 8 sides; cornice 16.5 |
| Above the drum | concave neck 4.50 to a waist of 4.35; onion 8.15 high, 7.90 wide | ogee dome 9.65 high; disc 4.20; small lantern 3.60 with four spikes | concave neck 5.50, torus 7.2; pear bulb 9.75 high, 9.0 wide; disc 5.4 | (sheet: concave neck 6.20 to 7.70); cushion 3.90 high, 10.30 wide; bulb 9.80 high, 6.55 wide; disc 5.65 |
| Ball, ornament, vane, tip | ball 3.10; fleur at 51.4; vane ("E XIV") at 56.8; tip 60.0 | fleur 49.65; vane ("1886") 55.1; tip 58.1 | ball 3.50; crown ring 4.1; vane 61.6; tip 65.0 | ball 3.10; fleur 59.2; vane 64.6; tip 67.9 |
| Tip in the model, m above the water | 42.41 | 42.85 (Street View: 42.6) | 44.60 (Street View: 44.2) | 45.46 |

**Horizontal scale of the bells.** At the eaves, the drawn wall is scaled to the model's wall (N 0.320, S 0.326, W 0.311, E 0.283 m per fot). The scale runs linearly to Möller's 0.2969 at the bell's top. The drums and everything above them have Möller's own dimensions. Each bell base reaches 0.40–0.53 m outside the wall, over pass 27's cornice at r + 0.24. The bells and the parts above them are faceted, with the number of sides read from the plans. They are rotated so that a face looks away from the castle's centre. The orientation of the plans on the sheets is not geographic.

## What is estimated, and where the photographs differ

- **East tower.** Möller drew a concave neck, 6.20 fot high, from the drum's cornice to a 7.70 fot band. The 2022 photograph shows a flat cornice and a straight octagonal block of about that band's width, carrying the cushion. The photograph wins: the model has a straight block 3.85 half-width, 28.1 to 33.5 fot. In the photograph the cushion, bulb, disc and ball are faceted (eight sides), as built. The bell has more standing seams than the model's sixteen corner ribs.
- **South tower.** Pass 27 had an open octagonal lantern. Both the sheet and the 2017 photograph show a closed, copper-clad drum, so it is now closed. In the 2017 photograph the drum and dome read about 25 % taller, and the finial about 20 % shorter, than in the model at the same camera, with the same drum width and the same total. The difference is within the camera's uncertainty (pass 127's residual is 35 px) and the shoulder of the bell, which hides the drum's foot differently. Möller's dimensions are kept.
- **Kuretornet.** The 2019 and 2020 photographs show the lucarnes larger relative to the bell than the model's. Möller's lucarnes are absolute, but the model's bell is stretched about 20 % horizontally to meet OSM's 17.1 × 16.0 m outline, where the sheet's wall is 47 fot (13.95 m) square. Either OSM's outline includes more than the tower's top, or the tower tapers. The walls were left as they are.
- **North tower.** At the right of the elevation, Möller draws an adjoining cornice 13.5 fot (4.0 m) below the tower's eaves. If that is the range's outer eaves (z 20.27, pass 127), the tower's eaves would be about 1.2 m higher than pass 27's estimate (z 23.27). It was not changed: the identification is not certain, and the brief asks for minimal changes to the bodies.
- **Ornaments.** The fleurs, the vanes (their lettering is not modelled), the crown, the candelabra, the lucarnes' fans and the volutes are simplified solids. The vanes' directions are chosen.
- **Ribs.** Copper ribs are modelled only on the bells' corners, Kuretornet's four hips and the lantern dome's eight corners.

## Joints

- **Roofs.** Pass 127 cut the range roofs 0.15 m inside pass 27's bells. The new bells are narrower than pass 27's in places at roof height, so a vertex of a bell ring is kept out to pass 27's bell less 0.05 m wherever the roof stands over it. The test is a ray up from the point, taken 0.2 m lower and at half a vertex step to each side. The roof's cut edge therefore stays inside the copper.
- **Wall tops.** Each round bell starts at the wall top with a soffit ring from 0.06 m inside the wall to the bell's base polygon. Kuretornet's bell starts from its wall rectangle in the same way.
- **Kuretornet's lantern** stands on the plinth, which stands on the closed top of the bell.

## Verification (sandbox, prelude 131)

- **Prepare.** `prepare_block132.py` prints `BLOCK132_PREPARE_OK`. It checks that the heights are monotonic, that the read totals are within 1 fot of the written ones, that each bell base covers pass 27's cornice, and that the crown is within 0.3 m of pass 27's 59.0.
- **Change set.** Mesh hashes were taken before and after the build in the sandbox. Only `SM_Kalmar_Slott_Towers` changed.
- **Repeatability.** A second run of the build changes nothing (identical vertex hash and face count).
- **Mesh.** 241,030 faces after the export preparation. `c27_finish` removed 51 slivers, and `drop_degenerate_faces132` found 0 more. Pass 125's cut removed 4 faces again. Vertex z runs from 3.47 to 57.67, the crown at 58.99 m above the water.
- **Export frame check** (the pass 130 wrapper's method): 0 invalid loops, and the test FBX export succeeded. The exporter's fallback covers 214 loops. Pass 125 reported 204 for the towers mesh.
- **Clashes with `SM_Kalmar_Slott`.** No vertex of the castle mesh lies more than 0.25 m inside any new bell above 0.3 m over the wall top. Below 0.3 m the only such vertices are the roofs' own edges at the wall line, under the eaves. No castle vertex stands above Kuretornet's cornice within 12 m of its axis.
- **Pass 131's rooms** (Gröna salen, its furniture, Förbrända salen) reach at most z 17.42. The lowest wall top is z 23.27, and the tower bodies are unchanged, so nothing of this pass enters them.
- **Roof joints** (360 azimuths per tower; where a range roof stands at pass 27's bell less 0.10 m, a horizontal ray is cast inward from 0.30 m outside that bell, just under the roof's surface, and must meet the copper within 0.45 m, before the roof's cut edge):
  - N: 0 gaps of 43 azimuths under a roof;
  - S: 1 of 2;
  - W: 0 of 11;
  - E: 1 of 22.
  The two remaining azimuths are at the ridge apices (z 25.33 and 25.47). The first runs of the check were wrong: the ray started inside the bulged copper. Where the bell is held out under a roof, it shows a small saddle-shaped step of up to about 0.4 m at the ridge (`ba_jointN.jpg`, `ba_jointE.jpg`), like a flashing.
- **Photo matches** (`SCR/p132/sb4/`):
  - **`cmp_south2017_zoom.jpg`.** The 2017 photograph, before, after. The closed octagonal drum, the ogee dome, the small spiked lantern, the fleur and the vane replace pass 27's open lantern and cone.
  - **`cmp_east2022_zoom.jpg`.** The 2022 photograph, before, after. The drum, the block, cushion, bulb, dark disc, ball, fleur and vane replace pass 27's open lantern.
  - **`cmp_drone2019.jpg`.** A view placed by eye from the east-north-east, with the five caps in the photograph's order. It is not a measured match.
  - **Other views:** `ba_kure.jpg` (Kuretornet from the outer bailey), `ba_air.jpg`, `ba_jointN.jpg` and `ba_jointE.jpg` (the roof joints).
- **Official build:** done by the lead on 2026-10-03; see "Official build". The Unreal checks are pending.

## Cameras

`715_Block132_Cal_SouthCap2017`, `716_Block132_Cal_EastCap2022`, `717_Block132_Drone2019`, `718_Block132_Kuretornet`, `719_Block132_Aerial_Caps`.

## Limitations

- **Wall tops and footprints are pass 27's.** This covers the north tower's eaves level, Kuretornet's 17 × 16 m outline against Möller's 14 m square, and E's radius.
- **The bells' outlines are Möller's 1885 design.** Only the east tower's neck was corrected from a photograph. Of the five caps, only the south and east caps were compared with photographs taken from measured cameras.
- **The interiors of the caps are not modelled.** Kuretornet's open lantern shows the closed top of the bell and the ceiling.
- **Extra views that would help:**
  - the north tower's cap from the bridge (local about (−895, −230), heading 125, pitch 20), to settle its drum, onion and eaves level;
  - the west tower's cap from the south-west rampart (about (−930, −345), heading 30, pitch 25).

## Official build

The lead built pass 132 officially on 2026-10-03.
- **Geometry and export:** the geometry check passed on the second rebuild (True), the FBX audit passed (exit 0), and the two rebuilds gave identical meshes.
- **Prevhash:** only intended changes.
  - Pass 126's `SM_Kalmar_Slott_Towers` now shows as changed, because this pass re-creates it.
  - Pass 131's three meshes are identical.
  - The other entries are known earlier corrections.
- **Dry renders:** cameras 715–719, 5 of 5.
