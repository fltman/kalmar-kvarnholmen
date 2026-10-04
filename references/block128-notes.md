# Pass 128: Kalmar slott, the chimneys

Pass 128 corrects the chimneys on Kalmar slott's roofs. Pass 127 had ten:
- six tall ones about 2 m up the courtyard slopes, placed from a first, wrong reading of the 2017 courtyard photograph (two of them on SW, where the photograph actually shows SE_w);
- pass 27's four outer ones.

This pass measures them again on the 2014 Street View panoramas, the 2017 photograph and two 2021 drone photographs. It counts **fifteen**: seven on the courtyard side, the wide stack on the SE_w ridge, and seven on the outer slopes.

| Mesh | Category | Status | What changed |
|---|---|---|---|
| `SM_Kalmar_Slott` | Kalmar slott/Castle | re-created, `detail_pass=128`, `corrects_pass=27,124,126,127` | the chimney list only |

Nothing else changes. The roofs, fronts, dormers, stairs, turret and rustication are pass 127's.

**Method.** `build_block128.py` runs `build_block127.py` again in a private namespace (as pass 127 does with pass 126's code). It makes three single replacements, each asserted to occur exactly once:
- `B127D['chimneys']` is replaced by `source/block128.json`'s `chimneys`. The fields are the same (x, y, w, d, ang, z0, z1), so pass 127's `chimneys127` builds them unchanged: a salmon render box with a stone cap.
- `mark127` marks the mesh `detail_pass=128`, with these notes, `corrects_pass=27,124,126,127`.
- Pass 127's camera section is cut off. Pass 128 defines its own cameras.

After the run, `drop_degenerate_faces128` runs on the mesh. It removes 0 faces; pass 127's own `drop_degenerate_faces127` has already run. The positions are computed in `scripts/prepare_block128.py` (Shapely, on pass 127's joined roof pieces in `source/block127.json`) and written to `source/block128.json` and `previews/block128-zones.json`.

## The chimneys

The positions use each range's frame from pass 27/127:
- `s` runs along the range from its origin;
- `c` runs across it: inner line, ridge (pass 127's `cr`) and outer line are given for each range.

The foot is the roof height at the chimney's downhill side. The box goes 0.8 m below it, as in pass 127. The top is the foot plus the measured visible height.

| Id | Range | Side | s | c (inner / ridge / outer) | Plan size | Foot z | Top z | Top − ridge | Status | Sources |
|---|---|---|---|---|---|---|---|---|---|---|
| K | SE_w, at the SE_w/SE_e bend | courtyard | 18.67 | −12.65 (−13.99 / −5.58 / 0.84) | 1.0 × 0.8 | 18.28 | 22.78 | −2.69 | measured | pano 1 (98°, 135°), pano 2 (150°), 2017 photo |
| I | SE_w, middle, on the ridge (wide, row of flue holes) | ridge | 10.43 | −5.40 | 1.65 × 1.1 | 24.88 | 29.28 | +3.81 | measured | pano 1 (135°), pano 2 (150°), 2017 photo, outer pano |
| C | SE_e, above the eaves | courtyard | 9.71 | −12.98 (−16.36 / −5.92 / 2.06) | 0.9 × 0.8 | 18.64 | 23.14 | −2.33 | measured | pano 1 (98°, 135°), pano 2 (95°, 150°) |
| B | SE_e, east corner, high on the slope | courtyard | 20.25 | −10.76 | 0.9 × 0.8 | 19.38 | 23.38 | −2.09 | measured | pano 1 (98°, 135°), pano 2 (95°) |
| A | NE, by the east end | courtyard | 4.70 | −11.50 (−18.73 / −6.42 / 2.99) | 0.9 × 0.8 | 21.70 | 26.30 | +0.83 | estimated | pano 1 (20°, 98°) |
| N1 | NW, at the north corner (short) | courtyard | 11.50 | −16.10 (−17.98 / −7.79 / 0.00) | 0.8 × 0.7 | 18.58 | 20.28 | −5.19 | estimated | pano 2 (300°, 330°) |
| N2 | NE, north of the north corner | courtyard | 33.30 | −14.10 | 1.0 × 0.8 | 20.10 | 25.40 | −0.07 | estimated | pano 2 (330°), top only |
| W | SW, by the west corner, half way up | courtyard | 6.58 | −6.56 (−9.37 / −4.50 / 0.36) | 0.9 × 0.8 | 21.03 | 24.43 | −0.37 | measured | pano 2 (245°), drone 2021 |
| SWo1 | SW, beside the stepped gable | outer | 17.50 | −0.80 | 0.8 × 0.7 | 21.03 | 23.73 | −1.07 | estimated | drone 2021 |
| SWo2 | SW, outer row | outer | 21.37 | −2.10 | 0.9 × 0.7 | 22.24 | 25.14 | +0.34 | estimated | drone 2021, oblique 2021 |
| SWo3 | SW, outer row | outer | 24.82 | −2.10 | 0.9 × 0.7 | 22.24 | 25.14 | +0.34 | estimated | drone 2021, oblique 2021 |
| SWo4 | SW, outer row | outer | 29.19 | −2.10 | 0.9 × 0.7 | 22.24 | 25.14 | +0.34 | estimated | drone 2021, oblique 2021 |
| NEo1 | NE, outer eaves, middle (narrow) | outer | 23.00 | 2.00 | 0.9 × 0.7 | 20.62 | 24.62 | −0.85 | estimated | drone 2021, oblique 2021 |
| NEo2 | NE, outer eaves, middle (wide) | outer | 19.70 | 2.00 | 1.4 × 0.8 | 20.59 | 24.89 | −0.58 | estimated | drone 2021, oblique 2021 |
| SEo | SE_e, outer slope by the east end | outer | 22.00 | −3.00 | 0.9 × 0.7 | 23.34 | 26.34 | +0.87 | estimated | outer pano, drone 2021 |

**Against pass 127.**
- Pass 127's two SW courtyard chimneys (40 % and 58 %) do not exist. The only chimney on the SW courtyard slope is W, by the west corner.
- Pass 127's NW 50 % courtyard chimney does not exist either. No chimney stands on the NW courtyard slope between Kuretornet and the north corner.
- Pass 127's NE 26 % and 80 % chimneys become A (by the east end) and N2 (north of the corner).
- Pass 127's SE_w 45 % chimney becomes the wide ridge stack I. The 2017 photograph's other chimney is K, at the bend. Neither stands 2 m up the slope at mid-range.
- Pass 27's four outer chimneys are dropped:
  - NW 22 % and 74 %: the drone photograph shows no chimney on the NW outer slope;
  - NE 52 %, near the ridge: it becomes the pair at the NE outer eaves;
  - SE_e 55 %: it becomes SEo.
- The four outer ones on the SW range are new.

**Not modelled.**
- A short white stack where the SW and NW roofs meet at the west end. It is seen in the drone photograph only and may be a vent.
- A stack at the edge of the south tower's cap. It is seen in the drone photograph only, and its plan position falls inside the tower.
- The flue holes and the pots on the stacks.

## Measurement

### Cameras

| Source | Camera | Used for |
|---|---|---|
| Street View 2014, pano 1 `zCIfieeXGQUNANmWu_Tg9A` (courtyard), viewed only | Resected by least squares on bearings:<br>- views 98°/60y/100t, 135°/75y/108t and 20°/75y/95t;<br>- points: the east courtyard corner, the south corner, the north corner and the well.<br>Result: (−885.06, −306.46), heading offset −1.34°, residuals 0.3–1.5°. The pano lies 1.6 m in front of the NW front, not in the south corner area as its nominal position suggests. Height ZC + 2.1 (1.5–2.4 from the corner feet). | K, I, C, B, A |
| Street View 2014, pano 2 `jOXzkLldNOjrveyz1T81wg` (courtyard), viewed only | Resected the same way:<br>- views 150°/75y/105t and 255°/75y/95t;<br>- points: the east, south and west corners and the well.<br>Result: (−860.06, −308.67), heading offset −2.65°, residuals 0.4–1.6°. Height ZC + 1.9; the eaves at the bend check at z 16.85 against 17.01. | K, I, C, B, N1, N2, W |
| Street View 2014, outer pano `VgKtBpunaiGwzOIYZf4djA` (outside SE_w/SE_e, the annex front), viewed only | Two annex front corners and the east-end projection, heading 320°. Result: about (−854.4, −361.5), heading offset about −4°, residuals 0.2–1.5°. | I seen from outside, SEo |
| Commons 2017 courtyard photograph (PD) | Pass 127's camera: (−861.1, −292.66), heading 174.9, f 1890 px, horizon at row 1115 | K, I (third ray), comparison 695 |
| Commons 2021 vertical drone photograph (HaSe, `schloss-kalmar-senkrecht-luftaufnahme-2021-.jpg`) | Not resected; see the limitation below | count, SW outer row, W, NE outer pair, SEo |
| Commons 2021 oblique drone photograph from the north-east (`schloss-kalmar-luftaufnahme-2021-.jpg`) | Not resected | SW outer row (spacing), NE outer pair (position along NE, height under the NE ridge) |

### Readings

- **Triangulated** (K, I, C, B):
  - The chimney axis was read at its visible foot in each view. Its bearing rays were intersected in plan.
  - Bearing residuals: K 0.2–2.3°; I 0.3–1.0°; C ≤ 0.4°; B ≤ 0.1°.
  - The foot and top heights come from each view's elevation angles at that distance. The height used is the top minus the visible foot, which does not depend on the camera height:
    - K 4.2–5.0 m (4.5 used);
    - I 4.3–4.9 m (4.4);
    - C 4.5–4.6 m (4.5);
    - B 3.9–4.1 m (4.0).
  - Absolute tops: pano 2 gives K 23.1, C 22.9, I 29.1, B 26.1. Pano 1's elevations read about 1.8 m high at the bend eaves.
- **C.** Its triangulated point lies 0.7 m in front of pass 127's fitted SE_e eaves line. It is placed at its measured foot height (z 18.7, 1.7 m above the eaves) on the model slope, at its triangulated s.
- **B.** Its foot reads z 22.2–22.4. Pass 127's roof in the SE_e/NE corner is 2.9 m lower there (19.4), so B is set by its visible height, not its absolute top.
- **One view or one camera** (A, N1, N2, W): the foot ray was intersected with pass 127's roof.
  - A: two views from the same camera, s 4.6–4.8, c −10.9 to −12.0.
  - N1: in pano 2's 330° view it stands on the bearing of the north corner's downpipe. The model's north corner renders 6.7° away from the panorama's corner, from the resected camera. N1 is therefore placed relative to the model corner (s 11.5); the bare ray gives s 14.5.
  - N2: only its top is seen, over the NE front, 7° right of the corner. It is placed 26 m out on the ray, where its height would be 5.3 m like the other courtyard stacks, and turned by the same 6.7°.
  - W: s 6.58, c −6.56. The drone photograph agrees (s 5.6, half way up the slope).
- **Drone 2021** (the SW outer row, SWo1).
  - The tops and visible feet were read on 10× crops.
  - The positions along SW were interpolated between the west and south courtyard eaves corners. The offset was taken along the image direction of the slope.
  - The three stacks of the row stand 9–15 px past the SW ridge line, in the upper half of the outer slope (c ≈ −2.1).
  - The 2021 oblique photograph shows the same three over the SW ridge, spaced in the same ratio (0.77).
  - Their tops are set 0.3 m over the ridge. The 2017 photograph shows none of them over the ridge from the courtyard, and the oblique photograph shows them just over it from above.
- **NE outer pair.** The drone photograph puts them at the outer eaves at s 19.7 and 23.0. The oblique photograph's tower spacing gives s 20.0 and 23.5, with their tops just under the NE ridge.
- **SEo.** The outer pano's ray meets the SE_e ridge at s 21.8–22.7. The drone photograph shows the stack on the outer slope. Pano 1 does not see it over the ridge, so it is set 2.9 m out from the ridge with its top 1.1 m over it.
- **Count.** Each courtyard slope was checked whole in at least one panorama view:
  - SE_w and SE_e: pano 1 at 98° and 135°;
  - NE: pano 1 at 20°;
  - SW: pano 2 at 245°;
  - NW: pano 2 at 255° and 300°.

  No courtyard chimney was found beyond those listed.
- **Widths.** I is 1.66 m wide (pano 1 at 135°, nearly square on), K 1.0 m, C 0.8 m (pano 2). The NE outer wide stack is about 1.5 m (drone). The others are set at 0.8–0.9 m.

**Reading error.**
- The pano cameras carry 1–2° bearing residuals. The model's courtyard bend vertex (CI3) comes out 3.5–5° from the panoramas' bend downpipe when it is left out of the fit, so pass 27's outline is itself off there.
- Triangulated plan positions: about ±0.7 m (K ±1 m).
- One-view positions (A, N1, N2): ±1.5–3 m along the ray.
- Drone-only positions: ±1 m along the range, ±1 m across.
- Heights: ±0.5 m (triangulated), ±1 m (others).
- A global camera fitted to the drone photograph (11-parameter DLT on courtyard corners, eaves lines and tower finials) left residuals up to 25 px and put K 10 m off. It is not used for positions, only the local interpolation within the SW range is.

No pixel of Street View or the satellite imagery was saved or used. The panoramas were viewed in the browser and read on screen.

## The 2022 photograph

Re-reading `swe-kalmar-slott-006.jpg` against the panoramas gives a different identification from pass 127's (north corner: NW left, NE right). The photograph more likely looks at the **south corner**:
- the left front is SW, with Kyrkportalen's aedicule;
- the middle front, SE_w, is hidden behind the well;
- the right front is SE_e, with its outside stair and the red-fronted dormer;
- the cap is the south tower's.

On the north-corner reading, its right-hand chimney would stand between the north corner and the NE dormer. Pano 1 shows nothing there; on NE the dormer comes first from the north corner, then chimney A. This pass does not use the photograph for positions and does not change pass 127's camera 690. The lead may want to check it.

## Verification

- **Prepare.** `KALMAR_GEO=<pylib> python3 scripts/prepare_block128.py` prints `BLOCK128_PREPARE_OK`. It asserts:
  - every footprint corner lies on pass 127's visible roof;
  - no chimney stands within 0.8 m of a round tower or in Kuretornet;
  - no footprint meets a dormer;
  - every top clears the roof under the chimney by more than 0.8 m;
  - the NW chimneys' bottoms stay above z 17.35 (Gyllene salen's walls reach 17.27);
  - no two chimneys stand within 1.5 m of each other.
- **Sandbox.** Prelude pass 127; `SCR/p128/build_block128_check.py`; logs `SCR/p128/log1.txt` and `log2.txt`. Both runs print `SANDBOX_DONE` without errors. Run 2 moved N1 and N2 relative to the model's north corner and lowered the SW outer row and SEo (see Comparisons); the numbers below are run 2's.
- **Change set.** Every mesh in the scene was hashed before and after the build. Only `SM_Kalmar_Slott` changes (`CHANGED128 ['SM_Kalmar_Slott']`).
- **Repeatability.** The build ran twice on the same scene: `REPEAT128 True`, and the second run changes nothing.
- **Chimneys.**
  - A downward ray just outside each footprint corner meets the roof above the chimney's bottom in every case, so no chimney floats.
  - No vertex of pass 125/126's rooms lies under any chimney's footprint above its bottom. Under N1 and N2 the hall's highest vertex is at z 16.18; N1's bottom is at 17.78 and N2's at 19.30.
- **Export frame check.** Pass 127's wrapper: the export tail's preparation, the exporter's frame test and a test FBX export. Result: 0 invalid loops, 1 of 1 exports succeeded. The fallback frame covers 5,664 loops (pass 127: 5,659).
- **Walk checks.** Pass 126's routes, re-run:
  - courtyard → portal E → Kungstrappan → Gyllene salen → Kungsmaket: 330 samples, 0 missing, largest step 0.167, 0 obstructions, 0 low headroom;
  - gate passage: 120 samples, step 0.021;
  - portal C → D / E / F: 35 / 42 / 187 samples, step 0.012, 0 obstructions.
  
  These are the same numbers as pass 127.
- **Roof clearance.** All 54,748 vertices of Gyllene salen above z 15.5 still meet the castle roof above them.
- **Comparisons** (`SCR/p128/sb2/`):
  - **`cmp_courtyard2017.jpg`** (the 2017 photograph above the render). It is rendered level and cropped to the photograph's horizon at row 1115. K stands at the bend and I near the SE_w ridge, as in the photograph. The render sits 50–90 px low against the photograph overall: pass 127's camera.
  - **The pano views 696–698** (`p1e_sv.jpg`, `p1s_sv.jpg`, `p2s_sv.jpg`, plus `p2n_sv.jpg` and `p2w_sv.jpg`) were compared on screen with the live panoramas. In pano 1 at 98°, A, B, C, K and I stand at 302/518/637/928/1185 px in the panorama and at 305/515/660/920/1185 px in the render. Run 1 showed SEo over the SE_e ridge and the SW row over the SW ridge where the panoramas and the 2017 photograph show none; both were lowered or moved in run 2.
  - **`air.png`** and **`top.png`**: the roofs from above.
- **Official build:** done by the lead on 2026-10-03; see "Official build". The Unreal checks are pending.

## Limitations

- Only five chimneys are triangulated or measured from two cameras. A, N1 and N2 depend on one camera, and the outer chimneys on the drone photographs alone.
- The chimneys are plain boxes with a stone cap. The flue holes (I has a row of them), the chimney pots and the paired flues are not modelled.
- Where pass 127's roof is lower than the real one (the SE_e/NE east corner), B's top is set by its visible height, not its measured absolute top (26.1).
- Pass 127's dormers are unchanged. The panoramas show the red-fronted dormer on SE_e beside the bend, not on SE_w.
- Pass 27's outline at the SE bend and the north corner is 1.5–2.5 m off the panoramas.

## Sources

| Source | Licence | Used for |
|---|---|---|
| Google Street View 2014: courtyard panos `zCIfieeXGQUNANmWu_Tg9A` and `jOXzkLldNOjrveyz1T81wg`, outer pano `VgKtBpunaiGwzOIYZf4djA` | viewed only | chimney bearings, heights, count |
| `castle27/kalmar-castle-internal-courtyard-2017-07-30.jpg` (Commons 2017) | PD | K and I, comparison 695 |
| `castle27/schloss-kalmar-senkrecht-luftaufnahme-2021-.jpg`, `castle27/schloss-kalmar-luftaufnahme-2021-.jpg` (HaSe 2021) | as in castle27/sources.json | count, outer chimneys |
| `castle27/swe-kalmar-slott-006.jpg` (-wuppertaler 2022) | CC BY-SA 4.0 | re-read only (see above) |
| Pass 127 (`source/block127.json`), pass 27 (`source/castle27.json`) | project | roof surface, range frames, dormers, towers |

The chimneys keep pass 27's materials (salmon render, stone caps); no new material is added.

## Official build

The lead built pass 128 officially on 2026-10-03.
- **Checks:** the geometry check passed on the second rebuild (True), the FBX audit passed (exit 0), and the two rebuilds gave identical meshes.
- **Prevhash:** pass 127's `SM_Kalmar_Slott` is changed as intended. The other entries are the known intended corrections from earlier passes.
- **Dry renders:** cameras 695–699 rendered (5 of 5).
- **Unreal:** the import is deferred.
