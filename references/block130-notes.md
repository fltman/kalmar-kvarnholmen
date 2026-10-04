# Pass 130: Kalmar slott, the interior of Slottskyrkan (room 86)

Pass 130 builds the interior of Kalmar slott's chapel, Slottskyrkan (1589–92; room 86 in Olsson's and Möller's numbering), on the state floor of the south range. It follows pass 125's method: closed architectural solids at real scale inside pass 27's hollow range, flat-colour materials on the town textures, cameras inside, and a walk check.

| Mesh | Category | Status | What |
|---|---|---|---|
| `SM_Castle130_Slottskyrkan` | Kalmar slott/Interiör | new | the room shell: floors and chancel steps, walls in their painted zones, the barrel vault with lunettes and plaster ribs, ten window niches with their own glazing, lunette fields with stucco rosettes, psalm tablets, the sunburst with the dove, the painted drapery and altarpiece on the altar wall, two closed doors |
| `SM_Castle130_Inventarier` | Kalmar slott/Interiör | new | the furnishings: altar, communion rail and kneeler, the raised pulpit gallery, the stone font, the commander's pews with turned and crowned posts, closed pews and open benches, hymn boards, the organ, three chandeliers |

No existing mesh is touched. `SM_Kalmar_Slott`, `SM_Castle124_*`, pass 125's rooms and pass 126's Kungstrappan are unchanged (`CHANGED130` lists only the two new meshes).

## Which range, and where in it

**The south range is pass 27's `SW` range** (courtyard front seen square-on at true heading 216; pass 27's range frame: origin (−905.619, −310.763), u (0.435, −0.900), n (−0.900, −0.435); s from the west tower towards the south tower, c outwards, the courtyard front at c ≈ −9.3, the outer front at c 0…0.36).

- Olsson (room 86) and the state-floor plan at Kalmar läns museum (…10 Gröna salen, 11 the round tower's chamber, 12 Slottskyrkan, 13 Sydöstra vindelstenen…) put the chapel in the south range, between the west corner and the south-east stair. In the model's naming that is SW, between the west tower (W) and the south tower (S).
- Pass 27 already has the chapel's roof turret on the SW ridge (s 13.75), and pass 127 found SW's middle courtyard row crossing the state-floor slab, which fits a tall room with other floor levels below.

**The s-interval: 6.20–27.77 (inside the walls).**
- The SW courtyard front runs from the west courtyard corner (s 6.07) to the south corner (s 27.84), 21.8 m. The 1780 plan's inside length is 21.57 m.
- The two end walls are therefore put at the courtyard corners: the west wall's inner face at s 6.20, the altar wall's at s 27.77. The west wall (1.28 m) and the altar wall (0.93 m) stand inside the corner blocks where SW meets NW and SE_w.

**The altar is at the +s end (by the south tower).**
- The plan's thick wall (1.72 m, four deep splayed niches) is the outer wall and its thin wall (1.19 m, six small windows) the courtyard wall; Möller's section has the same (outer 1.89 m, courtyard 1.27 m, labelled "Jordlinie" and "Gård").
- Facing the altar, the plan has the courtyard wall on the left. In the SW frame a viewer facing +s has the courtyard (−c) on the left, so the altar is at +s, by the south tower (true heading about 126, the liturgical east end).
- The photographs agree: facing the altar, the pulpit gallery stands against the left wall with a window behind it (Commons 2015, 2017), and the door beside the altar is on the right, at the outer wall, as the plan's door at the altar end.

## Measurement

### The plan of about 1780 (Krigsarkivet 0424:058:212a, public domain)

- **Scale.** The bar in alnar has its ticks 0/10/20/30 at x 735/1371/2009/2643 on the 3587 × 2558 scan: **63.6 px per aln**. With 1 aln = 0.5938 m that is **107.1 px/m**.
- **Inside the walls:** 2310 × 766 px = **21.57 × 7.15 m**.
- **Walls:** outer (top in the drawing) 1.72 m, courtyard (bottom) 1.19 m, altar end 0.93 m, west end 1.28 m.
- **Windows.** Read by grey-run detection along the wall rows, checked on grid crops:
  - courtyard wall: six windows at a regular 3.67 m, 1.1 m wide at the room face and 0.92 m at the glass, the first 1.93 m and the last 20.37 m from the altar wall;
  - outer wall: four deep splayed niches, 1.8 m wide at the room face and about 1.2 m at the glass, 1.56, 7.63, 13.54 and 17.33 m from the altar wall (irregular).
- **Doors:** a 1.1 m door in the west end wall, 0.57 m off the axis towards the outer wall; a narrow door (0.65 m) in the altar wall by the outer corner.
- **Furnishings** (the key: a altar, b pulpit, c commander's pew, d priest's pew, e closed pews, f open pews):
  - altar against the end wall, 2.3 × 0.75 m;
  - a horseshoe communion rail 2.73 m deep and 4.6 m wide;
  - the chancel line (double line) 3.75 m from the altar wall;
  - d along the courtyard wall from the altar wall, 3.4 m long, then b;
  - an unlabelled round object 0.5 m across beside d (the stone font of the photographs);
  - the two c pews with posts at their four corners (drawn as circles);
  - closed pews at a 0.92 m pitch (partitions at x 1157–2244), open benches at 0.97 m (x 2244–2868);
  - an aisle 2.1 m wide on the axis.

### Möller, "Profil genom Kyrkan" (1882, PK006-00041, public domain)

Scale: pass 127's 57.97 px/m on the 90-fot bar, checked (17.21 px per fot). Floor reference: Möller's red state-floor line, row 9927, as pass 127.

| Value | Rows / columns | Result |
|---|---|---|
| Inside width | x 5721–6144 | **7.30 m** (plan 7.15) |
| Courtyard wall, outer wall | x 5647.5–5721, 6144–6253.75 | 1.27 m, 1.89 m |
| Vault springing | row 9745 | **3.14 m** above the floor (z 13.61) |
| Vault crown | row 9612 | **5.43 m** (z 15.90) |
| Vault section | checked at x 5740 and 5780 | a half-ellipse, semi-axes 3.65 × 2.29 m |
| Courtyard window | rows 9850 / 9660 | sill 1.33 m, head 4.60 m |
| Outer window | rows 9852 / 9662 | sill 1.29 m, head 4.57 m |
| Niche head at the room face | row 9690 | 4.0 m (it rises outwards to the glass) |
| Vault back / attic floor | row 9527 | 6.90 m |
| Mezzanine window under the chapel (courtyard side) | rows 9922–9995 | z 9.30–10.56 |

The section is cut through a window bay. Short lines from the wall heads up to the vault are read as the lunettes' groins.

**Photographic check of the heights.** On the 2017 nave photograph (Commons, PD), the altar wall's width (7.15 m = 825 px on a 1.5× crop) gives 115 px/m in the wall's plane. The door beside the altar then reads 2.26 m. The end wall's arch springs 2.78 m above the chancel floor (z 13.53) and has its crown 5.13 m above it (z 15.88). Both agree with Möller within 0.1 m.

### What is used

| Value | Source | Status | Model |
|---|---|---|---|
| Inside 21.57 × 7.15 m | plan, scale bar | measured | s 6.20–27.77, c −8.40 to −1.25 |
| Floor | pass 125's state floor; Möller's chapel floor on the red line | taken over | z 10.47 |
| Vault: half-elliptic barrel, springing z 13.61, crown z 15.90 | Möller; checked on the 2017 photograph | measured | as read |
| Lunettes over every niche, 2.5 m (courtyard) / 2.9 m (outer) wide, crown z 15.36 | photographs (2009, 2015, 2017); Möller's groin lines | estimated | horizontal transverse barrels, each on its own half of the vault |
| Ribs: two longitudinal ribs 1.55 m from the crown, transverse ribs at 3.9 m, five crown medallions, groin ribs, diagonals from the lunette crowns, pier ribs, wall arches | photographs | arrangement read, sizes estimated (bands 0.24 m wide, 0.035 m deep, red edge lines) | |
| Wall thickness: outer 1.15 m, courtyard 0.85 m | the model's range is 9.73 m deep (Möller 10.46); the plan's inside width is kept | fitted | see Mismatches |
| Window niches on the facade's windows | sandbox scene, prelude 128 (pass 126/127's rows) | from the model | see below |
| Niche sill z 11.57, glass 3.2 m high | facade (Möller: 11.80, 3.27 m) | from the model | |
| Wall zones: pale lower zone to 1.75 m, band to 2.0 m, salmon upper zone; ochre altar wall | photographs | estimated | |
| Chancel: two risers of 0.14 m, 3.77 m deep | plan (line); photographs (two steps) | measured / estimated | z 10.75 |
| Furnishing positions | plan | measured (±0.1 m) | |
| Furnishing heights and forms | photographs | estimated | |
| Organ at the west end | 2015 panorama | estimated; not in the 1780 plan | 2.1 × 0.85 m, 3.6 m high |

### Window niches and the facade

The niches stand on the facade windows of the scene the sandbox builds (`SM_Kalmar_Slott`'s glass, read in the prelude 128 scene and checked again in the prelude 129 run, `NICHE130`, offsets ≤ 0.01 m):

| Side | Niche axis (room / glass) | Facade window | Plan window | Facade − plan |
|---|---|---|---|---|
| courtyard | 7.55 (blind) | none | 7.39 | – |
| courtyard | 10.27 | 10.27 | 11.20 | −0.93 |
| courtyard | 14.07 | 14.07 | 14.91 | −0.84 |
| courtyard | 17.87 | 17.87 | 18.50 | −0.63 |
| courtyard | 21.67 | 21.67 | 22.21 | −0.54 |
| courtyard | 25.47 | 25.47 | 25.84 | −0.37 |
| outer | 10.94 | 10.94 | 10.47 | +0.47 |
| outer | 15.34 | 15.34 | 14.30 | +1.04 |
| outer | 22.42 | 22.42 | 20.18 | +2.24 |
| outer | 26.26 / 26.82 (skewed) | 26.82 | 26.26 | +0.56 |

- Courtyard niches: 1.45 m wide at the room face, 1.30 m at the glass. Outer niches: 1.80 m and 1.30 m.
- Each niche has an elliptic head that rises from z 14.6 (room face) to z 15.07 (glass), a limestone sill, and its own window: a green frame, two mullions, a transom, glazing bars and a fanlight, glazed in a pale "daylight" tint. Pass 27's glass stands behind it, in the skin.
- The outer niche by the altar wall is splayed asymmetrically, as the plan draws its outer niches. Its room-side axis is at the plan's s 26.26, its glass on the facade window at 26.82. On the facade axis the lunette would have run into the altar wall.
- The plan's sixth courtyard window (s 7.39) has no facade window. It is built as a blind niche at s 7.55 with its pane against the shell, as pass 126 did with Gyllene salen's north niche.

## What the room has

### SM_Castle130_Slottskyrkan

- **Floors.**
  - Nave: wide boards under the pews and 0.3 m red-brown tiles in the aisle, on a dark bedding slab (so the joints are not see-through).
  - Two limestone risers (0.14 m) at s 23.56–24.0, then grey flags of 0.62 m in the chancel (z 10.75).
- **Walls.**
  - Closed solids from z 10.17 (under the floor) to z 16.60. The long walls' openings are built as slabs (piers per paint band, a parapet under each sill, and the niche heads as fans of slabs), so splayed and skewed niches stay closed solids.
  - Paint zones: lower zone, band, upper zone. The altar wall is ochre all over; the west wall's upper zone is lighter.
- **Vault.** One closed solid: the intrados as a 360 × 120 grid (s every 0.06 m; across the room evenly in the ellipse's angle, so it is dense near the walls), the top at z 16.60 and the sides.
  - The intrados is the half-ellipse or, where higher, a lunette over a niche, applied only on that niche's half of the vault.
  - The groins are where the two surfaces meet.
- **Ribs.** Bands following the intrados, standing 0.035 m into the room along its normal, with thin red edge lines:
  - the two longitudinal ribs;
  - transverse ribs between them;
  - five ring medallions on the crown, with short crown ribs;
  - every lunette's groin;
  - diagonals from each lunette crown to the longitudinal rib;
  - pier ribs from the springing between lunettes;
  - the wall arches at both end walls.
- **Lunette fields.** Grey-blue between the niche head and the lunette, each with three white stucco rosettes, each rosette a disc, a boss and eight petals.
- **Psalm tablets.** On every pier wider than 1.25 m (two on the long outer pier): dark slate with an arched head, a light border and lines of text as strips, 0.82 × 1.12 m, their tops at the springing.
- **The sunburst with the dove** above the pulpit gallery's west end, on the vault surface over the courtyard pier: 24 gilt rays, a gilt disc, and a white dove.
- **Altar wall.**
  - The painted canopy: a white baldachin top and white drapery with yellow lining, as plates.
  - The altarpiece: a gilt frame 1.30 × 1.85 m, a dark painting, a gilt crest and apron.
- **Doors.** Both closed: panelled grey-green leaves set back in the reveal, a brass handle, a stone surround with a cornice.
  - West door 1.10 × 2.40 m.
  - Altar door 0.90 × 2.20 m at c −2.00. The plan's door is 0.65 m wide; it is moved 0.2 m from the plan so that the communion rail's end meets the wall beside it.

### SM_Castle130_Inventarier

- **Altar.**
  - Limestone table 2.3 × 0.8 m, 1.0 m high, on a platform inside the rail, with a white cloth and a green antependium with a gilt cartouche.
  - Two blue and gilt candlesticks with candles, and a small gilt crucifix.
- **Communion rail.** Half-elliptic (2.73 m deep, 4.63 m wide), 0.95 m high, green-grey, with raised panels and gilt cartouches on every second segment, a dark cap and base, and a white kneeler round it.
- **Hymn boards.** Two, black in gilt frames with crests, either side of the altarpiece.
- **Pulpit gallery** (b over d), along the courtyard wall from the altar wall to s 23.69:
  - a dark panelled base with six red-brown panels;
  - a deck 1.40 m above the chancel floor;
  - a 1.10 m parapet of six green-grey panels with gilt frames and lozenge cartouches, the fourth glazed;
  - pilasters, gilt drops under the deck, cornices;
  - a turned post under the west end;
  - a book desk.
- **Stone font.** Red-brown marble, octagonal foot and round bowl (Commons 2015, nos. 03 and 04), at the plan's round mark.
- **Commander's pews** (c). Two enclosures 1.15 m high, with a gilt strip and panels on their fronts, a seat, and at each corner a turned post 2.4 m high: a green shaft, two red melon knops, a baluster and a gilt crown.
- **Closed pews** (e). Ten rows each side at the plan's partitions:
  - partitions 1.05 m high with brown top rails;
  - seats and book shelves;
  - panelled ends with doors at the aisle;
  - a closing panel on the outer side.
- **Open benches** (f). Oak, with seat, back, ends and a centre support: six rows on the courtyard side and four on the outer side, where the organ now stands.
- **Organ.** At the west wall, on the outer side of the door: a wooden base, three cased pipe fields with tin pipes (the middle one higher), a console and a bench.
- **Chandeliers.** Three, of crystal, on the crown at s 11, 17 and 23: a rod, a turned baluster, two tiers of arms (8 and 6) with brass cups, candles and drops. Their lowest point is 3.0 m above the floor.

The furnishings are finished without the town's 3 mm edge bevel. On these small close-set parts the bevel only produced collapsed slivers: in the first run 21,524 of 30,805 faces were degenerate, and a candle tip had no UV frame for the export. The same world-scale UVs as `s21_finish` are written instead. The shell keeps the bevel.

## Cameras

| Camera | Where (s, c, height over the floor) | Look | Compared with |
|---|---|---|---|
| `705_Block130_Cal_Nave2017` | 12.80, −4.80, 1.91 | +s, pitch 12, vfov 49.4 | Commons 2017-07-30, the nave towards the altar (PD) |
| `706_Block130_Cal_Altar2017` | 17.60, −4.80, 2.45 | +s, pitch 4, vfov 58 | Commons 2017-07-30-2, the chancel (PD) |
| `707_Block130_Cal_Pulpit2015` | 26.60, −3.40, 1.75 | towards the courtyard wall, pitch 9, vfov 62 | Jopparn 2015 no. 05, the pulpit gallery (CC BY-SA 4.0) |
| `708_Block130_WestEnd` | 23.00, −7.00, 2.00 | −s, pitch 6, vfov 64 | Jopparn 2015 no. 08 (panorama), left half |
| `709_Block130_Aerial_SouthRange` | aerial over the SW range | – | – |

**Camera 705** is placed from the photograph, not resected:
- the eye height comes from the horizon (row 1740 of 2380), read at the altar wall's scale;
- the distance comes from the aisle's width at the front pews against the altar wall's width;
- the focal length (2587 px on the full image) follows from the two.

The others are placed by eye.

## Verification

- **Prepare.** `KALMAR_GEO=<pylib> python3 scripts/prepare_block130.py` prints `BLOCK130_PREPARE_OK`. It asserts:
  - the envelope (room plus walls) lies inside pass 27's outline, outside the courtyard, the four towers plus 0.36 m and Kuretornet plus 0.36 m (0.000 m² each);
  - no overlap with pass 125's rooms plus 2.2 m (36.4 m away) or pass 126's stair (18.4 m away);
  - the end walls stand within 0.3 m of the courtyard corners (6.07 and 27.84);
  - the plan's width agrees with Möller's within 0.3 m;
  - every lunette is clear of the end walls and of its neighbours, and every niche's head stays under its lunette at the wall face (so the vault never covers a niche mouth);
  - the crown is 0.7 m under the top, and the top is 1.0 m under pass 127's roof over the courtyard wall (z 17.61).
- **Sandbox.** Three runs with the wrapper `SCR/p130/build_block130_check.py` and a sandbox copy with the Workbench shadows off (`SCR/p130/sandbox130.py`, as pass 125 did; a closed room is otherwise in shadow). Logs: `SCR/p130/log1.txt`–`log3.txt`.
  - Runs 1 and 2 used prelude 128. Run 1 stopped at the wrapper's own name clash. Run 2 printed `SANDBOX_DONE`, but the furnishings failed the export check.
  - Run 3, on the final files, used prelude 129 (the lead's official pass 129 build had appeared). It prints `SANDBOX_DONE prelude 129` without errors.
  - A scratch harness (`SCR/p130/fast.py`) ran the build alone on an empty scene with the project's `Mesh`/`mat`/`s21_finish`, for the design iterations of the renders.
- **Change set and repeatability** (run 3). The build is run twice on the same scene:
  - `CHANGED130 ['SM_Castle130_Inventarier', 'SM_Castle130_Slottskyrkan']`;
  - `REPEAT130 True`; the second run changes nothing.
- **Degenerate faces.**
  - `drop_degenerate_faces130` (with the `_thin` test) removes 1,396 faces from the shell: 1,376 bevel slivers in the vault's first, 1.2 mm cells at the springing, and 20 on gilt plates.
  - It removes 132 from the furnishings: the zero-radius tips of the lathes (chandelier drops and cups).
- **Final counts.** Shell 305,052 faces; furnishings 9,260.
- **Export frame check** (pass 128's wrapper method: the export tail's preparation, the exporter's frame test and a test FBX export):
  - 0 invalid loops, 2 of 2 exports succeeded;
  - fallback frames: 233 loops in the shell, 2 in the furnishings.
- **Placement.**
  - Every vertex of both meshes lies in the envelope s 4.92–28.70, c −9.25 to −0.10, z 10.17–16.60 (`EXTENT130`, 0 outside).
  - Every vertex above z 15.5 (145,544 of the shell, 12 of the furnishings) has the castle roof above it (`ROOFCLEAR130`, 0 not under the roof).
  - No vertex of any other mesh lies inside the envelope, except 72 of `SM_Kalmar_Slott`, listed in Mismatches 5: pass 127's courtyard cornice and wall-top fillers at the two courtyard corners, inside the chapel's courtyard wall, not in the room.
  - Gyllene salen, Kungsmaket, 61a and Kungstrappan are 18–36 m away.
- **Walk checks** (ray casts every 0.2 m; obstruction rays at 0.45 m and 1.4 m; a headroom ray of 2.0 m):

| Route | Samples | Missing | Largest step | Obstructions | Low headroom | Height |
|---|---|---|---|---|---|---|
| Chapel: inside the west door → aisle → chancel steps → round the rail's north side → the altar door | 117 | 0 | 0.14 (one riser) | 0 | 0 | 10.46–10.75 |
| Pass 126: courtyard → portal E → Kungstrappan → Gyllene salen → Kungsmaket | 330 | 0 | 0.167 | 0 | 0 | 5.47–10.47 |
| Gate passage B → C | 120 | 0 | 0.021 | 0 | – | 3.70–5.49 |
| Portal C → D / E / F | 35 / 42 / 187 | 0 | 0.012 | 0 | – | 5.47–5.48 |

  Pass 126's routes give the same numbers as in passes 127 and 128.
- **Comparisons** (`SCR/p130/sb3/`, also copied to `SCR/p130/final/`; `sheet.jpg` stacks all four):
  - **`cmp_nave2017.jpg`.** These agree:
    - the vault's height and section;
    - the lunettes on both sides with their rosette fields;
    - the rib net with the crown medallions;
    - the tablets on the piers;
    - the pew blocks and aisle;
    - the crowned posts, the pulpit gallery on the left, and the altar wall with canopy, altarpiece, hymn boards and the door on the right.

    The Workbench light leaves the vault dark. The photograph's ribs are wider and patterned, and its walls carry stencilled red ornament that is flat colour here.
  - **`cmp_altar2017.jpg`.** The chancel with the rail, altar, gallery, posts and the sunburst. The photograph's gallery and rail are richer (carved scrolls, a bombé front).
  - **`cmp_pulpit2015.jpg`.**
    - These agree: the gallery's panels with one glazed, the window centred behind it, the rosette field over the window, the sunburst left of it, the font, and the rail in the foreground.
    - The photograph's parapet panels have arched tops and carved scrolls.
  - **`cmp_westend.jpg`.** The organ on the outer side of the west door and the long view along the courtyard side. The panorama's projection differs, so this is a check of arrangement only.
- **Official build:** done by the lead on 2026-10-03; see "Official build". The Unreal checks are pending.

## Mismatches with the exterior and open issues (reported, not corrected)

1. **The courtyard state row** (pass 126's 3.8 m rule) stands 0.4–0.9 m west of the plan's regular row (3.67 m pitch). The plan's sixth window, 1.2 m from the west wall, has no facade window; it is a blind niche here. Shifting the row 0.6 m east and adding a window at s ≈ 7.0 would match the plan within 0.3 m.
2. **The outer state row** (pass 27's even rule) differs from the plan's irregular niches by 0.5–2.2 m. The third outer window (facade 22.42, plan 20.18) is the worst. The niches follow the facade; the one by the altar is skewed.
3. **The courtyard middle row** (9.9–11.1, pass 127) crosses the chapel's floor (z 10.47). Möller shows this row as the mezzanine's window under the chapel, with its head at the chapel's floor beam (z 9.30–10.56). The chapel's courtyard wall stands behind these panes from z 10.17 up, so they show the wall, not a room.
4. **Window heights.** Möller's sills and heads (z 11.80/15.07) are 0.2–0.3 m above the facade's (11.57/14.77). The niches follow the facade.
5. **Pass 127's courtyard cornice and corner fillers** reach 0.15–0.18 m into the chapel's courtyard wall at both courtyard corners (s 6.1–6.9 and 27.8, z 15.68–16.24). They are inside solid wall, out of sight.
6. **Wall thickness.** Pass 27's SW range is 9.73 m deep; Möller has 10.46 m. With the plan's inside width (7.15 m) the walls are 1.15 m (outer) and 0.85 m (courtyard), against 1.7–1.9 and 1.2–1.3 m in the sources.
7. **Access is open.**
   - The chapel is reached through its west door (from the west corner and the round tower's chamber, room 11 of the museum plan, not built) and through the door beside the altar (towards the south-east stair, not built). Both are closed leaves.
   - Portal F (Kyrkportalen) is pass 124's door at the middle of the SW courtyard front (s 17.2–18.6). Pass 129 found the real portal 3–3.5 m from the south corner (s ≈ 24.3–24.8). It was left in place there.
   - Neither position has a stair up to the chapel in the model. Connecting the courtyard to the chapel needs the stair from F (not documented in the open sources) and an opening in pass 27's shell, so it is left open. Unreal can place the player inside (camera 705's position).
8. **Present-day furnishing.** The 1780 plan is followed. The modern photographs show differences:
   - an aisle about 1.7 m wide at the front pews, where the plan has 2.1 m;
   - open benches along one side of the west part;
   - the organ;
   - the pulpit as a long raised gallery over the priest's pew.

   The gallery and the organ are taken from the photographs; the pew blocks keep the plan's lengths.

## Limitations, and what is not yet "AAA"

- **Surface.**
  - The red stencil patterns of the walls and window reveals, the lace pattern of the lower zone, the ribs' meander patterns, the tablets' painted texts and the painted drapery are flat colours.
  - They need hand-made or licensed textures (photographs may not be used as textures) and normal and roughness maps.
- **Carving.**
  - The gallery's and rail's gilt scrolls are lozenges and frames.
  - The altarpiece is a frame with a dark field, and the crests are flat plates.
  - The posts' crowns and the chandeliers' crystal are simple lathes.
- **Not modelled:**
  - the wall sconces;
  - the votive ship model;
  - the tablets inside the niches beside the windows;
  - the painted cherubs over the lunettes;
  - the gallery's stair;
  - the inscriptions;
  - the modern chairs under the gallery.
- **Light.** No light sources; Workbench renders only. Unreal needs window lights and Lumen, as in pass 125.
- **Collision.** No Unreal collision test; the walk check is a Blender ray cast.

## Sources

| Source | Licence | Used for |
|---|---|---|
| Krigsarkivet 0424:058:212a, "Plan af Calmare Slotts Kyrka N:o 1", about 1780 (`castle-sources/riksarkivet/KrA-0424-058-212a_c1780_plan-slottskyrkan.jpg`) | public domain | length, width, walls, windows, doors, all furnishing positions |
| Carl Möller, "Calmar slott. Profiler", January 1882, "Profil genom Kyrkan (N:o 86)" (PK006-00041) | public domain | vault section and heights, window heights, wall thicknesses, mezzanine row |
| `commons-kalmar-slott.slottskyrka.jpg` (Baboş 2009) | CC BY 3.0 | vault, lunettes, tablets, pews |
| `commons-slottskyrkan-i-kalmar-slott-08.jpg` (Jopparn 2015, panorama) | CC BY-SA 4.0 | west end, organ, posts, windows; comparison 708 |
| **New in `castle-sources` (with `sources.json` entries):** `commons-kalmar-castle-church-2017-07-30.jpg` and `-2.jpg` (2017) | Public domain | comparisons 705 and 706; the height check |
| **New:** `commons-slottskyrkan-i-kalmar-slott-01.jpg`, `-03.jpg`, `-05.jpg`, `-10.jpg` (Jopparn 2015) | CC BY-SA 4.0 | altar wall, the font, the pulpit gallery, the sunburst; comparison 707 |
| Commons category "Interior of Kalmar slottskyrka" (53 files), viewed | per file | identification of the furnishings; previews of 20 files were viewed in the scratch directory only |
| Kalmar läns museum, "Plan över praktvåningen" (as listed in SOURCES.md) | read only | the room order in the south range |
| Pass 27 (`source/castle27.json`), pass 125–127 (`source/block125.json`, `block126.json`, `block127.json`), the sandbox scene | project | frame, outline, levels, roof, facade windows |

Google imagery was not used. No pixel of any photograph or drawing is used as a texture: the new materials (`M_Block130_*`, 41 of them) are flat tints on the town textures (TownPaintWhite, TownIvory, TownPaintBrown, TownPaintGreen, TownStone, TownTileRed, TownMetalGrey).

## Official build

The lead built pass 130 officially on 2026-10-03.
- **Checks:** the geometry check passed on the second rebuild (True), the FBX audit passed (exit 0), and the two rebuilds gave identical meshes.
- **Prevhash:** pass 129's three meshes are identical. Everything else listed is a known earlier correction, so nothing outside the two new meshes changed.
- **Dry renders:** cameras 705–709, 5 of 5.
