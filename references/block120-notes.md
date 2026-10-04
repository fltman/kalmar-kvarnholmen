# Pass 120: correction of the fire station site at Larmgatan / Södra Kanalgatan

Pass 120 re-creates one mesh, `SM_Kvarnholmen_House_91846968`, which landmarks pass 14 built (`scripts/build_landmarks14.py`, line 183 on). The object keeps its name and category (`Kvarnholmen/Landmarks`) and carries `detail_pass=120`, `corrects_pass=14` and `osm_way=91846968`. No other mesh is touched, including the round drum 886305409 (pass 114).

The mesh has two parts.

**The old 1905 station (east half): kept verbatim.** Pass 14's code for the old station is copied unchanged into `build_block120.py` as `OLD14_CODE120`. That covers the long front with its arched vehicle doors, the rustication, the cornices, the side and rear facades, the hipped roofs and dormers, the raised west bay with its pediment, and the hose tower with its lantern. A script check compares the copy line by line with `build_landmarks14.py` lines 183 and 195–235, and all 42 lines are identical. There are three deliberate differences:

- the mesh is created by `b120_new`, not `l14_new`;
- the modern wing (pass 14's lines 184–194) is left out;
- the final `m.finish()` is replaced by `b120_finish`, which runs after the modern part. It calls `s21_finish` and then `drop_degenerate_faces120`.

The copied code runs in a private namespace, `NS120`. It is built from pass 14's own setup statements (its lines up to 16, including the exec of the four helper files) and every function pass 14 defines. The old part therefore uses pass 14's helper versions (`facade_box`, `lm_cornice`, `town_polyprofile`, `l14_*` and so on), and those versions do not leak into the shared namespace that later passes use. Nothing in the old part was "improved".

**The modern western part: rebuilt.** Pass 14 drew it as a cream box with three rows of windows, 10 m high, with balcony slabs on its north face. The photos show three different buildings:

- **The stone block (zone `stone`, 357 m²).** A five-storey corner block on Larmgatan clad in light limestone:
  - a tall ground floor with dark shop-front glazing and a granite-grey plinth;
  - three storeys of large windows over brown panels, in dark frames;
  - a coping on the parapet at 13.5 m;
  - a fifth storey (zone `stone_top`, 233 m²), flush with the Larmgatan and north faces but set back 3.0 m from the courtyard face. Its parapet is at 16.3 m. It has glazed doors onto the terrace, and a glass rail with a steel top rail runs along the courtyard edge.

  The block is a 9.2 m deep bar along the OSM west line. It reaches the measured north face about 8 m north of OSM.
- **The white wing (zone `white`, 1299 m²).** White render in two full storeys: windows on the ground floor and the first floor. A third storey sits in a dark mansard (eaves 9.3 m, flat top 12.6 m, inset 1.6 m). Its windows rise through the eaves into wall dormers with hipped dark hoods. There is a dark gutter line, and a plain white wall closes the gap under pass 14's old roof where the two parts meet.
- **The glazed pavilion (zone `pavilion`, 122 m²).** One storey in front of the white wing, between the stone block and x −240.5, with its north face in line with the stone block's:
  - floor-to-fascia glass with dark mullions every 1.5 m and two transoms;
  - a grey fascia, with its top at 5.0 m;
  - a roof terrace with a glass rail;
  - the white wing and stone walls behind the glass, built from the ground.

**The north extension.** Pass 114 put the pavilion corner near (−262, 288). The photos confirm that the modern part stands north of the OSM north face, though slightly less far than that estimate:

- the stone block's north face is at y ≈ 285.6 (OSM: 277.6 for the west part and 279.9 further east);
- the pavilion's north face runs in line with it to x −240.5.

The modern footprint is therefore pass 14's `modern` polygon with its north face, from the west line to x −240.5, moved out to y 285.6–286.0. The extension adds 194 m², and the total is now 1778 m² (OSM modern part: 1584 m²). The pavilion does not reach the drum: it stops about 7.5 m short of the drum's south side (y 293.6).

Panoramas are working references only. No pixel is used as a texture.

## Measurement

Three panoramas were used. The vertical field of view is 90°, and the bearing is the heading + 28.2°.

| Panorama | View (file in `SCR/p120/`) | Google position (local) | Resected position | Heading used | Camera height |
|---|---|---|---|---|---|
| Y9-2FdgHB50u5FEbl0dwuw | 21 Larmgatan, looking SSE (`fs_larm_h152.jpg`) | (−273.89, 299.57) | (−272.4, 301.5), estimated | 152 | 2.45 m |
| rKBf2EXlgpPpGcwYy3buRA | Södra Kanalgatan, looking S (`fs_kanal_h175.jpg`) | (−234.06, 317.75) | (−242.60, 318.71) | 162.2 (photo: 175) | 1.94 m |
| HsWLWKRmyL92sdlcqTcrww | 21 Larmgatan, looking NNE (`fs_drum_h25.jpg`) | (−278.55, 290.29) | (−277.02, 292.22), pass 114 | 25 | 2.0 m |

**Resection.**
- **Drum view.** This is pass 114's resection on the drum's silhouette tangents, reused unchanged.
- **Kanal view.** The two drum tangents (205.1° and 257.5° at image row 250) give a distance of 20.8 m to the drum centre. Combined with the bearing to the old station's west corner (OSM (−232.567, 280.42)), they fix the camera at (−242.60, 318.71) with a heading offset of −12.8°. That offset is unusually large.
  - The alternative, trusting the heading, puts the camera at (−239.33, 315.43). It would move the old station's west end 5.5 m west of OSM, and it reads the arched doors at only 3.5 m, against pass 14's 4.1 m.
  - With the solved camera, the door bases give a camera height of 1.94 m and the arch tops read 4.15 m, which matches pass 14's 4.1 m. That solution is therefore used.
- **Larmgatan view.** This camera could not be resected on two known corners, because the old station is too far off and the drum is behind it. Its heading is confirmed by Larmgatan's vanishing direction, which agrees within about 1°.
  - The position is Google's, shifted by the same offset that pass 114 found for the neighbouring drum panorama (+1.5, +1.9 m). With that position, the stone block's north-west corner (bearing 173.3°) falls 0.3 m from the OSM west line extended north. The camera height of 2.45 m then follows from that corner's base line.
  - The position is an estimate.

**Stone block.**
- **North-west corner.** It lies on the extended OSM west line at (−270.5, 285.6) (Larmgatan view, bearing 173.3°, base elevation −8.95°).
- **North-east corner.** Triangulated from the Larmgatan view (bearing 143.6°) and the drum view (112.6°): (−260.5, 285.3). The north face is therefore 9.9 m wide, and the model uses a depth of 9.2 m from the west line, which puts the corner at x −260.4.
- **Parapet at the north-west corner.** It reads 16.4 m on the Larmgatan view (top elevation 40.9° at 15.6 m). The model has 16.3 m.
- **Top-floor setback.** The north face's east column stops one storey lower, at about 13.9 m, which is the setback of the top floor. The model uses 13.5 m for the main parapet and a 3.0 m setback (estimated from the column width).
- **Storeys.** The ground floor plus four storeys, with the fifth set back as above.

**White wing.** Read on the Kanal view (camera b), on the plane of the OSM north face (y ≈ 280.3):

| Feature | Height |
|---|---|
| top of the first-floor windows | 7.9 m |
| eaves / gutter line | 9.3 m |
| top of the wall dormers | 11.3 m |
| mansard top | 12.7 m |

In the Larmgatan view, the dormer hood tops read about 12.0 m. The window bays are about 3.6 m apart.

**Pavilion.**
- **Fascia top.** It reads 4.6 m on the Kanal view (scaled to the pavilion face at y ≈ 285) and 5.6 m on the Larmgatan view. The model uses 5.0 m. The glass rail on its roof reads 5.8 m on the Kanal view.
- **East end.** It reads at x −235.8 (Kanal view), −240.7 to −248 (drum view) and about −243.7 (Larmgatan view). The model uses −240.5, which is uncertain by about ±3 m.
- **North face.** It reads 283.6–285.7. The model puts it in line with the stone block's north face.

## Estimated

- **The stone block's depth and southern extent.**
  - Only the north face and the northern part of the Larmgatan face are seen. A far roof line in the Larmgatan view is consistent with the block running at full height towards y ≈ 252, so the bar runs the whole Larmgatan frontage to the south neighbour 92204174.
  - Its courtyard face is parallel to the west line, which leaves it about 6 m deep at the south end.
  - The top floor stops at the west-line kink (y 259.76), because the setback face would otherwise pinch against the street jog.
- **The white wing.** Only the north face is seen. The whole rest of pass 14's modern polygon is modelled as this wing, with a mansard on every outer edge and a flat top. Its courtyard, south and east faces are not seen, and their windows repeat the north face's rhythm.
- **Window sizes.** Window sizes and spacing on the stone block are uniform per storey (3.3 m bays). The photo shows a wider central window on the north face; this is not reproduced.
- **Strip left out.** The small strip of the OSM outline south of the old station's west end, (−226.1, 251.2) to (−207.4, 247.8), is left out, as it was in pass 14.
- **Colours.** They are read by eye from the photos: limestone (0.75, 0.72, 0.65), brown panels (0.43, 0.29, 0.20), white render (0.93, 0.93, 0.91), dark mansard and frames, grey fascia.

## Verification

- **Zones.** `prepare_block120.py` prints `BLOCK120_ZONES_OK` (`previews/block120-zones.json`):
  - zoned area 1778.0 m² against an extended footprint of 1777.9 m²;
  - no overlap between zones, or with the old station's polygon;
  - the top floor lies inside the stone block;
  - the white wing's inset mansard ring is valid and keeps every edge's direction;
  - the smallest roof triangle altitude is 0.90 m (ear clipping that cuts the fattest ear).
- **Sandbox.** The runs (pass 119 prelude, `SCR/p120/build_block120_sb.py`, logs `SCR/p120/log_sb*.txt`) print `SANDBOX_DONE` without errors. `drop_degenerate_faces120` with the `_thin` test runs in `b120_finish`.
- **Export frame check.** The exporter's frame check (the `SCR/p119/build_block119_check.py` method) ran on the triangulated mesh in both sandbox runs: 0 invalid loops (776 loops use the exporter's fallback frame), and the test FBX export succeeded. `drop_degenerate_faces120` removed 84 faces, which leaves 93,922 polygons before triangulation.
- **The old part against pass 14.** The sandbox wrapper compared every vertex of the old part, as built by this pass before finishing, with the vertices of pass 14's object in the blend (240,670 vertices, `detail_pass` 14). That object carries the 3 mm finishing bevel, so the comparison uses the distance to the nearest vertex rather than identity. Of the 18,607 old-part vertices, 17,915 lie within 1 mm and all within 1.6 mm (largest distance 0.0016 m), so the old part comes out the same.
- **Side-by-side comparisons** at the photo size with the resected cameras: `SCR/p120/sb2/cmp_larm.png`, `cmp_kanal.png`, `cmp_drum.png`.
  - **Larmgatan view.** The stone block's corners, parapet and five storeys sit on the photo's (the north face spans u 202–344 against the photo's 216–342, and the parapet is within about 5 px). The white wing's dormer row sits where the photo has it. The pavilion's fascia reads about 15 px low against the photo; this agrees with the Larmgatan reading of 5.6 m, against 4.6 m on the Kanal view, and 5.0 m was kept as the compromise.
  - **Kanal view.** The drum, the old station's west end and the white wing's mansard and dormers line up. Pass 14's old station reads slightly lower than the photo (its eaves and cupola). That is pass 14's measurement and is left as it is.
  - **Drum view.** The stone block's north face edge and the pavilion beyond it appear at the photo's bearings.
- **Pending.** The official build and the Unreal checks are pending; the lead fills in the build results.

## Limitations

- The Larmgatan camera position is not independently resected, and the Kanal camera needs a large heading correction. The north face position (y ≈ 285.6) agrees between two cameras to about 0.7 m.
- The white wing's footprint and form beyond its north face are not seen.
- The stone block's loggias on the upper Larmgatan floors are not modelled; the windows sit in plain reveals.
- Signs, the bicycle stands, the lamp posts and the trees in front are omitted.
- Extra view that would help: a view down Larmgatan from the south end of the site, at about (−290, 240), heading 340 (bearing 8°), pitch 10. It would show the south end of the stone block and whether it really runs the whole frontage.

## Official build

The lead's build of pass 120 passed the Blender geometry checks and the FBX export, and two rebuilds gave identical meshes. Passes 28–119 are unchanged except the earlier intended changes; prevhash does not cover pass 14, whose fire-station mesh this pass deliberately re-creates. The Unreal import and its checks are deferred.
