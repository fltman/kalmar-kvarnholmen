# Pass 97: six houses on Norra Långgatan and Östra Sjögatan

Pass 97 replaces six generic district volumes from pass 17, scattered along Norra Långgatan and Östra Sjögatan, with the houses that stand there. They are split into eleven parts. Each mesh keeps its name.

On Norra Långgatan:

- **91970395 (Norra Långgatan 37), `SM_Building_91970395`:** a beige vertical-boarded two-storey house with its gable to the street. It has three windows a floor in white surrounds, a small window in the gable, white corner boards, a dark plinth and a grey sheet roof. The wide rear part of the outline is not seen. It has plain walls and a flat roof (estimated).
- **91885540 (Norra Långgatan 43), `SM_Kvarnholmen_House_91885540`:** a beige rendered 1950s block, 36 m long. It has a row of semi-basement windows and three floors of two-light white windows on a 2.1 m rhythm (17 axes). The entrance has a flat canopy, and the roof is a grey sheet hip.
- **91926309 (Norra Långgatan 47), `SM_Building_91926309`:** a cream neoclassical house. Its street front has:
  - a dark stone plinth and a rusticated base;
  - eight tall round-headed windows with archivolts, keystones and an impost band;
  - a double string course;
  - eight upper windows under cornice hoods;
  - corner pilasters, a frieze and a dentil cornice;
  - a low hipped roof.

  The rear wing is not seen. It has the same height under its own hip (estimated).
- **91926329 (Norra Långgatan 55), `SM_Kvarnholmen_House_91926329`:** a cream vertical-boarded two-storey house with pilaster strips, green-grey windows in pale surrounds and white awnings over the two west upper windows. It also has a light green double door on steps, a white foundation and a red metal mansard roof with two roof lights. The east wing behind is not seen and gets the same roof (estimated).

On Östra Sjögatan:

- **91970343 (Östra Sjögatan 22), `SM_Building_91970343`:** a yellow vertical-boarded house of one and a half storeys with its gable to the street. It has three ground windows and two upper windows that reach into the gable, white corner boards and rakes, and a dark plinth. The low annex at the back is not seen and is estimated.
- **91885535, `SM_Kvarnholmen_House_91885535`:** see "Which outline is which" below. Its 5.8 m street piece is the north end of the cream rendered house of pass 62. It is drawn in pass 62's measures:
  - two pairs of round-headed windows under segmental hoods, over arched red cellar hatches;
  - two upper windows;
  - the sill band, the string course, the corbel frieze and the cornice;
  - a brown metal saddle roof.

  The long wing behind (x 69–89) is not seen. It is a plain cream two-storey block with a flat roof (estimated).

Panoramas are working references only. No pixel is used as a texture.

## Which outline is which (91885535)

The heading-62 view from Östra Sjögatan shows two houses:
- the brown/beige roughcast house with three red dormers (left) is **91885528**, the ochre house of pass 64;
- the cream stucco house with arched windows (right) is **91885537**, the cream house of pass 62.

The two houses meet directly at a downpipe, and the cream facade is flat from that joint southwards. In OSM, 91885535's west wall (x 63.0, y 102.8–108.6) stands 3.5 m behind the common facade line. On the street, the gap it leaves between the fronts of pass 62 and pass 64 is filled by the cream house: two arched pairs and two upper windows, with the same frieze and cornice.

This pass therefore **adds the 19.6 m² strip** x 59.5–63.0, y 102.8–108.6 to the zone, so that the cream piece stands flush with its neighbours. It is listed under `added` in `source/block97.json`, and the zone checks count it as part of the footprint.

**Disagreement with pass 62.** On this panorama, registered on the ochre house's corner (y 108.64), the cream house's door is at y ≈ 102.3, and its pairs are at about 107.5, 105.0, 99.9, 97.4 and 94.5. Pass 62 has the door at 98.3, a single window at 101.5 and pairs from 96.5 southwards; it was anchored on the joint with pass 61 at y 84.0. The two registrations differ by about 3.3–4 m along the street, while the pair rhythm (2.5 m) agrees.
- Pass 62 is not touched. This pass places its two pairs at y 107.45 and 104.95, so that the street reads, as on the panorama, as two pairs and then a door.
- Between them, pass 62's single window at 101.5 remains, about 1 m closer than the photo's spacing.
- The lead may want to re-register pass 62 against this view.

## Measurement

Seven views from six panoramas (696×375, vertical field of view 90°) were used. Positions are in the local frame.

| View | Panorama | Google position | Resected camera | Height | Anchors |
|---|---|---|---|---|---|
| 37, heading 332 | aBgfQJ8z7PZVytxwmD4ZRA | (16.94, 70.05) | (15.80, 67.54) | 2.60 | both front corners on the facade plane (x 11.39, 18.61) |
| 22, heading 242 | cehOCjZG1Tk46TC_doz8Qw | (53.82, 96.42) | (53.70, 94.64) | 2.45 | both front corners (y 90.44, 97.75) |
| 17, heading 62 | ZfgrPLMgCeHz4Yx-3ZhvIw | (53.91, 106.92) | (52.50, 104.90) | 2.30 | the ochre corner (y 108.64); distance from pass 62's storey heights (see below) |
| 43, headings 332 and 302 | pHzk52tfy1hk6VKkwTz9vQ | (104.11, 70.83) | (104.1, 68.5) | 2.36 | distance from the storey height (2.8 m); no corner seen |
| 47, heading 152 | QP-BeywVy-fSGsYuq7XjjQ | (124.41, 70.90) | (124.70, 69.46) | 2.65 | the east corner; distance from a symmetric front of eight bays |
| 55, heading 332 | -Lx9Iv-XmmCXSCwGQZQb3g | (165.89, 69.89) | (164.20, 68.30) | 2.40 | the west corner; distance from the door height (2.1 m) |

**Notes on the resections.**
- **37 and 22:** two known corners each, with zero residual. Both cameras lie near the street centreline, 2.5 m and 1.8 m from Google's positions.
- **17:** a least-squares fit on the ochre house's four corner and axis positions gave a camera only 1.9 m from the opposite facades, with pass 62's heights reading 20% too high. Pass 64's axis spacing (3.46 m) is the inconsistent input there. With the camera 6.9 m from the facade (pass 62's distance), pass 62's heights read within 0.1–0.2 m (cornice 9.1 against 8.9; upper windows 5.48–7.05 against 5.36–6.91). That camera was kept, with y set by the ochre corner.
- **43:** only the close and steep views exist. The distance (3.7 m) is chosen so that the three window rows stand 2.8 m apart. It is consistent with the eaves line along the whole front, but it is not checked against a known length.
- **47:** with one corner, the distance was chosen where the eight arched bays come out symmetric in the 24.85 m front (2.73 m spacing, first axis 2.67 m from the corner). That distance also lies within 1.5 m of Google's position.
  - The arched and upper rows only give the same spacing with an effective pitch of 16°, not the 20° asked for, so 16° is used.
  - This is the least certain scale in the pass: ±8%.
- **55:** the door height of 2.1–2.3 m and a level base gave a distance of 4.5 m (±0.5).

All values are in metres above the street at the facade; "s" is the distance along the OSM front from its first corner.

| House | Measured | Estimated |
|---|---|---|
| 37 (91970395) | plinth 0–0.44; ground windows 1.37–2.87 at s 1.26, 3.26, 5.26; upper 4.23–5.76; eaves 6.7; gable window 7.0–7.75; ridge 8.9 at the middle of the front | depth of the gable roof (the whole narrow part, 17.4 m); the rear part (eaves 6.0, flat roof); the side windows |
| 22 (91970343) | plinth 0–0.57; ground windows 1.34–2.89 at s 1.66, 3.74, 5.78; upper windows 3.94–5.76 at s 2.58, 4.75; eaves 5.1; ridge 7.72 at the middle | the annex (3.2 m, flat); the roof material |
| 91885535 street piece | the facade line is flush with pass 62 and pass 64; the axes are at y 107.45 and 104.95 | heights taken from pass 62, not re-measured; the roof (11.0, as pass 62); the rear wing (eaves 6.65, flat) |
| 43 (91885540) | semi-basement windows 0.36–1.08; window rows 2.23, 5.03, 7.80 (1.5 m high, about 1.35 m wide); axes 2.1 m apart (measured 15.7–24.0 m along); entrance about s 11.8, 1.8 m wide; eaves 10.35 | the axes beyond s 25 (rhythm); the hip roof to 12.6; the chimneys; the other walls |
| 47 (91926309) | plinth 0–0.49; rusticated base to 2.35; base cornice 2.35–2.55; arched windows 2.76–5.67, 1.52 wide; string course 6.59–6.93; upper windows 7.57–9.35, 1.15 wide; hoods to about 10.0; frieze 10.0–10.85; cornice to 11.8 | the west end (out of frame; mirrored); the roof (13.4); the rear wing; the side walls |
| 55 (91926329) | foundation 0–0.35; ground windows 1.41–2.86 at s 1.8, 5.6; upper windows 3.98–5.20; pilasters at s 3.6 and 7.5; door bay about s 7.7–9.0; gutter 5.85; the roof's top edge about 1 m inside the front at about 8.6 (mansard break) | the east half of the front (windows at s 11.3 and 13.7, pilasters at 9.3 and 12.5); the double door's second leaf; the upper roof (9.3); the east wing |

## Verification

- **Zones** (`previews/block97-zones.json`, status passed):
  - footprint 2046.3 m², including the 19.6 m² added strip;
  - 2046.2 m² zoned, 0.27 m² of OSM not zoned and 0.15 m² outside it;
  - no overlap.
- **Sandbox:** two sandbox runs (prelude: committed passes up to 95) printed `BLOCK97_GEOMETRY 6` and `SANDBOX_DONE` without errors.
- **Export safety:** `drop_degenerate_faces97` (with the `_thin` test) ran on every mesh after `s21_finish`. It removed these faces, mostly the slivers of the arched spandrels and gable joints:
  - 37: 18
  - 22: 12
  - 91885535: 90
  - 43: 0
  - 47: 189
  - 55: 28
- **Comparison:** the resected views were rendered at the photos' own size and set side by side with the panoramas:
  - **37, 22 and 47:** the eaves, ridges, window rows and bays line up within a few pixels.
  - **43:** the rows line up, and the axes are within about 0.2 m.
  - **17:** the cream piece and its cornice continue pass 62 and pass 64 as on the photo. The offset of pass 62's own door is described above.
  - **55:** in the first run the mansard's lower slope was too shallow and hardly visible. It was steepened (break 0.95 m inside the outline), and the second run matches the photo's roof band and roof lights.
- **Pending:** the official build, the geometry audits and the Unreal checks; the lead fills in the build results.

## Limitations

- **Scale:** the 43 and 47 views have no second known point. Their distances rest on a storey height and on facade symmetry, so their heights may be off by up to about 8%.
- **91885535:** the added strip departs from OSM on purpose, and the conflict with pass 62's door position is unresolved; see above.
- **Not seen and estimated:**
  - the rear parts of 37, 22, 91885535, 47 and 55, which carry generic windows and simple roofs;
  - the east half of 55's front;
  - the west end of 47's front;
  - all roofs except 37's and 22's gables and 55's lower slope.
- **Omitted:** signs, lamps, downpipes, the wall-mounted boxes, the plank and picket fences, the green gate north of 22 (not in this pass's outlines) and the TV aerials.
- **Extra views that would help:**
  - Norra Långgatan at about (95, 66), heading 332, pitch 20, for the west end and the full height of 43;
  - about (112, 67), heading 152, pitch 15, for the west end of 47;
  - about (175, 67), heading 332, pitch 15, for the east half of 55.

## Official build

The lead's build of pass 97 passed the Blender geometry checks, two rebuilds gave identical meshes, and passes 28–96 are unchanged. The Unreal import and its checks are deferred.
