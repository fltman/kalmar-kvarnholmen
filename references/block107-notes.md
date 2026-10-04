# Pass 107: Gamla kyrkogården, the Stagnell burial chapel and Bykyrkan about 1610

Pass 107 models Gamla kyrkogården (OSM way 149032114) in detail from Harald Åkerlund's grave plan, the Stagnell burial chapel (OSM way 500979084), the outline of the demolished town church Bykyrkan (Storkyrkan, S:t Nikolai) as a low kerb in today's grass, and the church itself as it stood about 1610, as a separate historical layer that can be hidden.

Background and sources are collected in `references/gamla-kyrkogarden-research.md`. All plans and photos were used as view-only references; nothing from them is used as a texture.

## Meshes

| Mesh | Category | Content |
|---|---|---|
| `SM_GamlaKyrkogarden107` | Slottsområdet/Gamla kyrkogården | lawn, gravel paths and the round gravel area, walls, two gates, 160 graves, 6 enclosures, the Kristoffer pillar, the church kerb |
| `SM_GamlaKyrkogarden107_Trees` | Slottsområdet/Vegetation | 17 old trees |
| `SM_Stagnellska107` | Slottsområdet/Gamla kyrkogården | the Stagnell burial chapel |
| `SM_Bykyrkan1610` | Historik/Bykyrkan 1610 | the church about 1610; `historical_reconstruction=True` |
| `SM_Slott98_Cemeteries` | (pass 98) | re-created, see below |
| `SM_Slott98_Trees` | (pass 98) | re-created, see below |
| `SM_Slott98_Buildings_M` | (pass 98) | re-created, see below |

## Deliberate changes to pass 98

Pass 98 treated both cemeteries generically. This pass re-creates three pass 98 meshes under their own names, with pass 98's own generation code and data (`source/block98.json`):
- **`SM_Slott98_Cemeteries`:** the generated grave rows inside Gamla kyrkogården and its boundary hedges are left out. Its lawn piece is kept. Södra kyrkogården (lawn, hedges, graves) is generated unchanged.
- **`SM_Slott98_Trees`:** the scatter trees inside Gamla kyrkogården or within 1 m of it are left out (28 trees; there are no OSM-mapped trees there). The other trees keep their pass 98 seeds, which stay tied to their index in the full list, so they are identical.
- **`SM_Slott98_Buildings_M`:** this chunk held the burial chapel as a plain one-storey box with windows. It is re-created without OSM building 500979084; every other house in it is unchanged.

These objects get `detail_pass=98` and `rebuilt_by_pass=107`. All other pass 98 meshes (ground, streets with the OSM paths, greens, the other building chunks) are untouched. The pass 98 OSM gravel paths inside the cemetery lie under the new lawn, which is 2.8 cm higher.

## Georeferencing

### Åkerlund's grave plan (pl. XIII, `pl13hi-010.png`)

- **Scale bar:** 0 and 40 m at x 1185.75 and 1776.0, so 14.756 px/m. The north arrow's shaft is vertical within about 0.5°.
- **Control points:** five wall corners of the double wall line, matched to OSM outline vertices: the south tip (where the wall stub meets the south-east boundary line), the south-west bend, the west bend, the north-west corner and the north-east corner. The north-west corner is hidden under the drawn charnel house, so it is taken as the intersection of lines fitted to the west and north walls. The sixth point is the chapel octagon's centre, matched to the centroid of OSM building 500979084.
- **Fit:** a least-squares similarity transform. It gives 14.707 px/m against 14.756 from the bar, and plan north at local bearing 27.93° against 28.2° expected.

| Control point | Residual |
|---|---|
| South tip | 3.66 m |
| South-west bend | 4.50 m |
| West bend | 2.02 m |
| North-west corner | 1.64 m |
| North-east corner | 1.78 m |
| Chapel centre | 1.25 m |
| RMS | 2.74 m |

The residuals are largest at the south-west wall. There, either the plan or the OSM outline is off by several metres. The walls follow the OSM outline, so the model stays consistent with pass 98 and its neighbours. One grave whose footprint crossed 0.6 m inside the OSM outline was pushed inwards.

### Rosman's excavation plan 1924 (pl. I, `r243-243.png`)

- **Scale:** the metre bar gives 0 and 40 m at x 1111.5 and 1881.5, so 19.25 px/m.
- **Fit:** rotation and translation, fitted to four things:
  - the chapel octagon centre (525, 852), matched to the OSM chapel;
  - the corner of the "Kyrkogårdsmur" (156, 932), matched to the grave plan's south-west bend;
  - the kink at the wall's gate end (597, 1271), matched to the grave plan's kink at the gate;
  - twelve points on the "Nuvarande kyrkogårdsgräns", against the straight OSM south-east side.

| Fit | px/m | Chapel | Wall corner | Gate kink | SE line RMS / max |
|---|---|---|---|---|---|
| Bar scale (used) | 19.25 | 1.10 m | 0.45 m | 1.65 m | 0.36 / 0.69 m |
| Free scale (check) | 18.80 | 1.09 m | 0.24 m | 1.72 m | 0.22 / 0.44 m |

### The 1610 reconstruction on Rosman's foundations

- **The church frame:** I measured Olsson's reconstructed plan of about 1610 (pl. II, rendered from `v158.pdf` p. 244 at 150 dpi; bar 19.69 px/m) in a church frame. The frame has u east along the axis from the west face of Södra valvet, and v north of the axis.
- **Fit to Rosman:** rotation and translation in Rosman's pixels, fitted to:
  - the Kalkkoret north-west corner, residual 0.46 m;
  - the octagon, which pl. II draws on the south wall line at u 13.7 m, residual 0.61 m;
  - the outer face of the excavated north wall, residual RMS 0.06 m.
- **Church axis:** local bearing 109.4°, true bearing 81.2°. The research file estimated about 80°.
- **Corners in the project frame:**
  - the Södra valvet south-west corner is at (−968.1, 16.5);
  - the high choir's east tip is at (−890.0, 6.5);
  - the burial chapel stands at the porch (Vapenhuset), as the sources say.
- **Agreement with the research file:** the corners lie 2–4 m from its estimates.

## What is measured and what is estimated

**Measured (from the scaled plans, as above):**
- the positions, sizes and orientations of the graves and enclosures;
- the centre lines of the paths (2.0–2.4 m between the drawn lines; built 2.1 m wide);
- the round gravel area (radius 3.98 m to the middle of the drawn line);
- the gate positions;
- the church's plan in every part, and its position and axis.

**Measured from Olsson's elevations (pl. V, VII):**
- the tower walls (26 m) and the spire tips (52.5 m);
- the nave eaves (13.5 m) and ridge (22 m);
- the chapel-row eaves (6.3 m) and gable peaks (13 m);
- the turret (about 30 m);
- the high choir: eaves 8 m, ridge 14.5 m.

**From the sources:**
- the walls: 0.75 m thick, 1.0–1.3 m high, with no wall on the south-east side (RAÄ);
- the Kristoffer pillar's sizes;
- the recorded sizes of the notable graves;
- the chapel's form and details (Sveriges kyrkor vol. 162 no. 1).

**Estimated:**
- **Grave types and heights:** taken from the drawn shape.
  - Bars are standing stones (0.8–1.6 m) or, every third, cast-iron crosses.
  - Blobs are lying slabs (0.12–0.24 m).
  - About a quarter of the mid-sized blobs are chest tombs (0.5–0.65 m).
  - Small blobs are low blocks.
- **Materials:** varied by a hash of the position.
- **The chapel:** walls 3.25 m and roof 3.0 m with its point, scaled from the photos against the door. Its width, 4.86 m across the corners, comes from OSM.
- **The chapel's orientation:** one face is set exactly to true north for the door. The OSM octagon has a corner, not a face, near north, and a traced octagon's rotation is not reliable.
- **The trees:** positions, species and sizes. The positions follow the research: chestnuts south and east of the Kristoffer pillar, a group on the church site, a few along the south-east path, a weeping ash near the chapel and the rest spread over the lawn. They keep clear of graves, paths and the walls.
- **The church:** window sizes and positions (one pointed window per chapel bay, after pl. V), the roof overhangs and the spires' flared feet. The north chapel row is given gables to the north like the south row, but no north elevation was available.
- **The tower:** 9 × 14 m, as the brief and Olsson give it. Pl. II draws the tower block about 9 × 16.5 m.
- **The church kerb:** the outline of the reconstructed footprint where it lies more than 1 m inside today's cemetery (171 m), built as limestone slabs 0.3 m wide and 0.12 m above the grass. Where the real kerb stones stand is not documented (research file, open question 4).

## Graves

The plan was segmented automatically:
- **Solid blobs:** connected components after a morphological opening with a 9 px disc, which removes the drawn lines.
- **Thin bars (headstones):** components with a stroke half-width of 3.8 px or more. Digits measure 2.7 px. Thinner bars that are not aligned with a neighbouring glyph of text height are also taken.

After checking the overlay, six false hits were dropped (a digit 8, the chapel's number 1, two arrow heads of the charnel house outline, and the outlines of nos. 20 and 45, which are modelled separately). Five missed bars were added (nos. 155, 90, 158, 23 and 51; they touch a line or a digit).

The result is 160 graves: 112 blobs and 48 bars. The plan numbers about 170, and some numbers have no drawn shape of their own.

The notable graves were matched to their research-file positions as the nearest detected shape:

| No. | Monument | Model | Match |
|---|---|---|---|
| 15 | Per Wijk | black granite obelisk 3.5 m on a round mound 3 m across | 0.0 m (in its square) |
| 28 | Bishop Magnus Stagnelius | cast-iron cross 1.87 × 1.07 m on a pedestal | 1.2 m |
| 53 | Wigander | cast-iron cross 2.5 × 1.19 m | 1.9 m |
| 73 | Jäger | cast-iron cross 1.36 × 0.88 m | 2.2 m |
| 54 | Ekman | grey limestone tumba 2.07 × 1.52 × 0.56 m | 2.0 m |
| 50 | Swarss | tumba 2.23 × 1.62 × 0.55 m in a 1.33 m railing | 2.1 m |
| 74 | Kinnecke | red limestone pillar, 2.5 m in all | 0.5 m |
| 96 | Balabrega | Höganäs urn 1.06 m on a 0.57 m slab | 3.2 m |
| 139 | Korsseman | red limestone obelisk, 2.4 m in all | 1.5 m |
| 166–168 | Grip, Lillie, Stierna | limestone slabs 1.8 × 1.5, 2.36 × 1.2, 2.1 × 1.24 m | 1.8, 3.1, 1.6 m |
| 20 | Johansson | white marble urn monument about 2.25 m | 1.0 m |
| 22 | Nordenanckar | Kolmården marble cross 1.27 m | 1.9 m |

The second Nordenanckar stone (no. 23) was not separated from the other bars, so it is a generic stone.

The enclosures were read by hand, because their outlines are broken by posts and gate openings, except no. 153:
- iron railings: no. 36 (3.2 × 3.2 m, with two cast-iron crosses inside), no. 44 (5.4 × 3.7 m on limestone blocks), no. 18 and no. 153;
- stone kerbs: nos. 34 and 35.

The Kristoffer pillar stands on the nave centre line at the chainage of plan no. 45. The plan's no. 45 lies 2.6 m off the reconstructed axis, within the georeferencing error. The bronze statuette is about 0.85 m, scaled from the 2014 photos against the 2.1 m pillar.

## Verification

- **Prepare checks** (`previews/block107-zones.json`, status passed):
  - lawn 8 808.3 m² + gravel 463.5 m² = the outline's 9 271.8 m², with 0.000 m² overlap;
  - no grave outside the outline;
  - all key notables matched;
  - 264.1 m of wall;
  - the church footprint is 2 139 m², of which 1 956 m² lies inside today's cemetery.
- **Sandbox:** three sandbox runs (prelude: rebuild chain of pass 106), all ending with SANDBOX_DONE without errors. Renders are in `SCR/p107/sb1`, `sb2`, `sb2h` and `sb3`. The build has an environment switch `BLOCK107_HIDE_HISTORY`, used only to render today's views without the 1610 church; it does nothing in an official build.
  - **Iteration 1** showed pass 98's generic box at the chapel's place, which led to the re-created `SM_Slott98_Buildings_M`, and too many trees.
  - **Iteration 2:** the chapel from the north-east agrees in form and proportion with the 2014 photos (Commons, `Kalmar_Ödekyrkogården_02/05`): ochre octagon, recessed panels, light frieze, black bell roof with a point, the black door on the north. The 1610 church agrees with Olsson's south elevation (saw-tooth gables, turret, tower with the spire profile) and west elevation (tower between the two west gables, twin spires).
  - **Iteration 3:** the gate, the north-east passage and the 1500s slabs.
- **Pending:** the official build, the FBX export (degenerate faces are removed in `b107_finish` with `drop_degenerate_faces107`) and the Unreal checks. The lead fills in the build results.

## Limitations

- **The plans and OSM** disagree by up to 4.5 m at the south-west wall. Interior features follow the plan through the fitted transform; the walls follow OSM.
- **The north-east passage:** the grave plan ends at the north-east corner. The path is continued to the north-east gate through the 28 m passage that OSM has there. That passage is drawn with walls on its north-west side and at its end only.
- **The graves:** only their footprints are measured. Types, heights, inscriptions and decoration are generic, except the notable ones. The detection may miss very small marks and merges graves that touch (for example nos. 135–136).
- **The old trees:** the museum's tree map (about 50 trees) was not available as data, so the 17 trees are placed plausibly, not surveyed. Pass 98's dense scatter is gone.
- **Bykyrkan 1610:**
  - it is simplified massing: no buttresses, no interior and no vaults;
  - the north side is inferred;
  - it overlaps the 1906 hospital building at its east end and today's chapel at the porch, as expected for a historical layer;
  - the burial chapel is later than 1610 and is not part of the reconstruction.
- **The chapel roof:** whether it has six or eight roof faces is uncertain. It is built with eight, to follow the walls.
- **No Street View panorama** was used.

## Official build

The lead's build of pass 107 passed the Blender geometry checks and the FBX export, and two rebuilds gave identical meshes. Passes 28–106 are unchanged except the intended changes: pass 85's prison building (corrected by pass 103) and pass 98's SM_Slott98_Cemeteries, SM_Slott98_Trees and SM_Slott98_Buildings_M (re-created here without their generic treatment of Gamla kyrkogården). The Unreal import and its checks are deferred.
