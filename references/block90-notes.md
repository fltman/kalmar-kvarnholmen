# Pass 90: the north side of east Storgatan, from the red cottage to the brick corner house

Pass 90 replaces five generic district volumes from pass 17 (two-storey blocks, 6.65 m) on the north side of east Storgatan, east of Proviantgatan. They are split into ten parts. The meshes keep their names.

- **93192351:** the red boarded cottage. It is one storey (eaves 2.95 m) on a low grey plinth, with three white-framed casements, white corner boards and an eaves board. The front range, 7.2 m deep, carries a red tile hipped roof with a break below the top, an arched red dormer with a round-headed window, and two chimneys: a rendered one on the east hip and a small one behind. A low flat-roofed rear part fills the rest of the outline.
- **93192354:** a two-storey boarded pair, mirror-symmetric about its middle (x 208.45):
  - the grey west half has vertical boards;
  - the white east half has horizontal boards.

  Each half has three casements on the ground floor and two windows upstairs: a large three-light one with a transom, and a smaller two-light one. There is a storey band on a stone plinth. Each half has a gabled dormer, and a snow guard runs along the eaves. The west gable wall, seen from the cottage panorama, is pale render.
- **93192423:** the cream boarded two-storey house with brown (teak) frames:
  - a central olive double door on a stone step;
  - four casements below and five above, the upper ones with a painted panel under the glass;
  - a storey band, a broad frieze under the eaves and an olive-grey plinth;
  - two gabled dormers, a brick chimney and a snow guard.

  The rear wing is a flat-roofed volume.
- **93192353:** the ochre rendered house with its gable on the street. It has white bargeboards, white corner pilasters and two casements on each floor in white surrounds. The tile saddle roof has its ridge running back from the street.
- **93192374:** two buildings and a rear part:
  - the low boarded yellow link at the west end, 3.4 m of the front, with the white double carriage gate;
  - the three-storey brick and stucco house from about 1890, from x 238.5 to the east end. It has a granite plinth and a rusticated stucco ground floor with the arched red double door (west bay) and four arched windows. Above a stucco band, the brick upper floors have stucco window surrounds with heads and sills, a cornice under the arched top-floor windows, pilasters between them, the main cornice with brackets, and quoins at the west corner. There are five bays at 3.1 m;
  - the rear parts behind both, as flat-roofed volumes.

**Corrections to the brief:**
- The white boarded house left of the cream house is the east half of 93192354, not a separate building.
- The cream house has two gabled dormers, not three. The third dormer in the photo belongs to the white half of 93192354.
- The ochre gable house is 93192353, which no panorama shows head-on.
- The brick house is the eastern 15.1 m of 93192374. The gate link takes the western 3.4 m.

Panoramas are working references only. No pixel is used as a texture.

## Measurement

Four panoramas from April 2025 were used, one view each at heading 332, which looks straight at the fronts. The fronts run along the model x axis, so x is used for positions along the street.

| Panorama | Where | View (heading/pitch) | Google position | Resected position (facade frame) | Camera height |
|---|---|---|---|---|---|
| x4uubzk9NfELeLvfWX88AQ | opposite the cottage, Storgatan 58 | 332 / 15 | (191.95, −2.35) | (190.93, −5.01) | 2.4 m (assumed) |
| sRnC-HF-aJquBydtqHus4A | opposite the pair, Storgatan 60 | 332 / 15 | (210.76, −2.41) | (208.55, −4.12) | 2.4 m (assumed) |
| 5jsHZ4H5LgklWdsRh36RNw | opposite the cream house, Storgatan 62 | 332 / 15 | (221.04, −2.54) | (218.73, −4.48) | 2.4 m (assumed) |
| u611VtYYWxCgDN1Ae7e86w | opposite the brick house, Storgatan 64 | 332 / 20 | (241.18, −2.85) | (240.43, −4.80) | 2.4 m (assumed) |

**Resection.** All rays were intersected with the facade plane 0.355 m south of the OSM line, so the positions above are already the model's camera positions. No extra offset is needed, unlike pass 88.
- **Cottage:** resected on its two front corners (OSM x 188.3 and 197.7). Both corners are clearly visible.
- **Cream house:** resected on the joint with the white house (x 216.9, a pair of downpipes) and on the assumption that the door stands in the middle of the 11.8 m front, at x 222.8. That assumption gives a plausible door (2.25 m high, 1.6 m wide) and a facade base about 0.3 m above the street. It also leaves the upper windows symmetric about the door.
- **Pair:** neither end of the pair is in the frame. The left edge of the photo is mid-facade, not the corner. The two white-house upper windows were located from the cream-house camera (x 210.9 and 214.0) and used to fix the camera's x. The camera's y was set so that the white house's eaves come out at the same height in both views.
- **Brick house:** resected on the corner of the ochre gable house (x 235.1, its white pilaster) and on its gable apex, assumed at the middle of the 6.4 m front (x 231.9). The brick house's west corner then falls at x 238.5, and its five bays fall at a regular 3.1 m with the middle bay at the middle of 238.5–253.6.

**A scale conflict that is not resolved.** The p89 photos (heading 152) from the same Storgatan 60 and 64 panoramas were resected on the south-side OSM corners. They put the cameras 2–3 m further south than the north-side resections do, and they cannot both be right in a street 10.5 m wide between facade planes. A plain two-corner resection of the north side would also give heights about 30–40 % too large, for example a 3 m door. The positions above were chosen so that known sizes are plausible: doors, storey heights, and a facade base near the street. The sandbox renders then line up with the photos (see Verification). Absolute heights should still be taken as ±10 %.

**Readings.** These are heights above the street with a 2.4 m camera, in metres.

| Part | Measured | Estimated |
|---|---|---|
| Cottage | eaves 2.95 (model; the reading was 2.82); windows 1.0–2.55 at x 189.6, 191.8, 194.1 (widths 1.37–1.65, 1.4 used); no openings east of x 195; dormer about 0.9 m window | roof top 6.9 and the break in the roof (from the sandbox match); front range depth 7.2; dormer and chimney positions (dormer x 193.4 after the setback); plinth 0.3; the rear part |
| Pair | joint x 208.45–208.55; eaves board top 7.3, gutter 6.5 (model eaves 6.75); band about 3.06; plinth top about 0.5; ground windows 1.22–2.74, 1.35 wide, at 202.7, 205.2, 207.0 and 210.1, 211.8, 214.6 (mirror-symmetric to ±0.2); large upper windows 3.53–5.66, 2.3 wide, at 206.0 and 211.0; smaller upper windows at 202.5 and 214.6; dormers at 203.2 and 213.9 on the facade plane | dormers at 202.4 and 214.5 after the 1 m setback; ridge 9.9; the western 2.5 m and the eastern 2.3 m of the front (out of frame); the pale west gable wall |
| Cream house | eaves 6.44 (model 6.25 after the sandbox); band 2.76–3.0; plinth top 0.27; door x 222.0–223.6, 0.37–2.62; ground windows 1.11–2.58 at 218.4, 220.25 and 224.75; upper panel 3.1–3.68, glass 3.68–5.0, windows at 218.35, 220.2, 223.0 and 225.0; dormers at 218.4 and 222.6 on the facade plane | fifth upper window and fourth ground window (x 227.2), made symmetric about the door; dormers at 218.35 and 223.3 after the setback; ridge 8.9; chimney position; the rear wing |
| Ochre gable house | corner pilaster x 235.1; eaves at the corner 3.94; apex 6.03; ground window 0.64–1.93 and upper window 2.96–4.23 at x 233.15 | the western windows (x 230.65, mirrored); no door is seen on the street (it is out of frame); roof depth (the whole outline) |
| Link | gate x 235.35–237.6, 0–2.36; boarded frieze to the gutter at about 3.6 | link depth 6 m; flat roof (not seen) |
| Brick house | west corner x 238.5; granite plinth top 0.63; ground arched windows sill 1.66, apex 3.67, 1.5 wide; door x 238.7–241.1, apex 3.72; band 4.39–5.52; first-floor windows 5.52–7.69, 1.43 wide, at 239.8, 242.9, 245.9, 249.3; cornice 9.66; top-floor arches 9.94–11.77; wall still rising at the top of the image (12.8) | bays made regular at 3.1 m about the front's middle; top-floor arches and cornice lowered 0.3 m after the sandbox; eaves 13.2 and roof 15.2; front range 10.4 m deep (the step in the OSM outline); the rear parts at 6.5 |

**Colours** were picked by eye from the photos:
- cottage: falu red, white frames;
- the pair: grey-blue and white boards, pale grey trim;
- cream boards with teak frames, an olive door and an olive-grey plinth;
- ochre render;
- yellow boards on the link;
- red brick with ochre stucco and red frames;
- red tile roofs on the cottage and the ochre house, grey sheet metal on the others.

## Verification

- **Zones:** `prepare_block90.py` prints BLOCK90_ZONES_OK. The footprint is 710.7 m², and 710.6 m² of it is zoned. 0.04 m² is not zoned, 0.01 m² lies outside OSM, and the overlap is 0.012 m².
- **Sandbox:** three runs of `SCR/sandbox.py` on a copy of `Stortorget.blend`. Each printed BLOCK90_GEOMETRY 5 and SANDBOX_DONE with no errors. Runs 1 and 2 rendered the four photo views at 696×375 from the cameras above, plus an aerial (`SCR/p90/sb2/cmp_*.jpg`, `SCR/p90/sb2/aer.png`).
  - Run 1 showed the pair's eaves about 7 px high and the cream house's eaves about 8 px high. It also showed the brick house's top floor a little high and the cottage roof too low. The pair's west gable wall was boarded where the photo shows render, and the cream door's panels were in the trim colour.
  - Run 2 made these corrections:
    - eaves: pair 6.9 → 6.75, cream house 6.4 → 6.25;
    - the top-floor arches and the cornice moved down 0.3 m;
    - cottage roof top 6.4 → 6.9;
    - the pale gable wall;
    - olive door panels;
    - a lighter brick.
  - In the final renders, these agree with the photos to within about 5–12 px:
    - the cottage's corners, windows and eaves;
    - the pair's joint, window rows, band, eaves and dormers;
    - the cream house's joint, window rows, door and band;
    - the ochre gable, the gate link and the brick house's bays, arches, band and cornices.
  - The worst case is the cottage's roof break, which the model draws lower and less pronounced than the photo shows.
  - Run 3 added `drop_degenerate_faces90`, called in `b90_finish` right after `s21_finish`. It deletes zero-area faces and faces with a repeated corner, which break the FBX export with tangent frames. It dropped 7, 45, 11, 10 and 60 faces from 93192351, 93192354, 93192423, 93192353 and 93192374 respectively. Most are the zero-height closing faces of the hip and gable roofs and of the board strips. The brick-house view rendered pixel-identical to run 2, and the aerial view showed no visible change to these houses. The run printed SANDBOX_DONE with no errors. This run's prelude already included pass 89.
- **Not run by this pass:** the official build, the Blender geometry checks and the Unreal import and checks. The lead runs them and fills in the results.

## Limitations

- **Scale:** see the scale conflict above. The camera positions rest partly on assumptions: the cream door centred, the ochre gable centred, and the pair placed from the cream-house view. Heights are therefore about ±10 %, and the camera height (2.4 m) is assumed.
- **Roofs:** every ridge and roof depth is an estimate. The cottage's roof is a two-stage hip that only approximates the photo's broken roof. The brick house's roof is not seen.
- **Not seen:** the ochre house's west half and any street door. 93192353 is only seen obliquely from the brick-house panorama. If a better view is wanted: local (232.0, −4.5), heading 332, pitch 15.
- **Walls not facing a street:** they carry generic windows. The rear parts of the cottage, the cream house and the brick house are plain flat-roofed volumes.
- **Omitted:**
  - the street lamps, the parking meter and the sign;
  - the electrical cabinet, the satellite dish, downpipes and gutters' outlets;
  - the brick house's carved keystones and console details, and the door's grille pattern, which is only suggested.

## Official build

The lead's build of pass 90 passed the Blender geometry checks, two rebuilds gave identical meshes, and passes 28–89 are unchanged. The Unreal import and its checks are deferred.
