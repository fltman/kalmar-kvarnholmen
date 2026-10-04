# Pass 109: north-west Kvarnholmen — Larmgatan, Strömgatan, Norra Långgatan and Västra Vallgatan

Pass 109 replaces seven generic district volumes from pass 17 with the houses that stand there. They are split into eleven zones (`source/block109.json`). Two of the volumes are stored in the district as `SM_Building_<id>` (91846958 and 91846925, the Storgatan list); the rest are `SM_Kvarnholmen_House_<id>`. The build reuses those names.

Which outline is which was settled by resection (each photo's building was located against the OSM outlines, not assumed from the pass brief):

- **92204179 (38 Larmgatan):** the red boarded wall is this 6.0 m outline. The low green boarded cottage with the red tile roof stands to its south on another outline and is not part of this pass. Modelled as a small falu-red boarded outbuilding: vertical boards and corner boards, a low stone plinth, a flat wall top at 3.8 m, and a low saddle roof (ridge 4.4 m) that cannot be seen from the street behind the wall top.
- **92204177 (40 Larmgatan):** one OSM ring holding the office block and its wing. The joint on the street front is at y = 194.8, 11.6 m from the north corner, and the outline is cut there.
  - Zone `o177` (north range): the 1950s three-storey office block in cream render. Shop windows sit under a long canvas awning. Above are red-brown brick bands at 3.26–4.55 m and 5.90–7.50 m, and dark window ribbons of seven panes at 4.55–5.90 m and 7.50–8.80 m. A thin dark roof slab sits at 10.1 m, with a brick lift house (top about 12.6 m) on the flat roof. The other outer faces (including the Strömgatan side) repeat the ribbon-and-band pattern, which is estimated.
  - Zone `w177`: the two-storey wing, flat roof at 7.1 m. Its first bay has one upper window and the glazed shop door under the navy 'Ludvig & Co' fascia (2.78–3.43 m). After it come shop windows, an ochre brick band at 3.42–4.55 m, and an upper ribbon of eleven panes at 4.55–5.90 m.
- **92204174 (1 Strömgatan):** the 29.2 m south front.
  - Zone `sw174` (west end to x = −276.2, where the downpipe marks the joint): cream render with a third storey of round-headed windows, quoins at the Larmgatan corner, and a low hipped roof.
  - Zone `sf174`: the two-storey ochre street range on a grey plinth. It has shop windows under navy fascias, two pedimented white door surrounds with grey panelled double doors, two boarded-up windows, a white cornice at 7.7–8.3 m and a dark sheet saddle roof with two small red gabled dormers. A third door surround (its pediment is just visible at the right edge of the photo), a shop window and two upper windows at the east end are extrapolated.
  - Zone `sb174`: the back ranges behind y = 229.0. Not seen; plain two-storey ochre render with a flat roof at 7.0 m.
- **886305409 (50 Larmgatan):** the whole outline is the round office drum (19 facets of 2.8–2.9 m, radius about 8.8 m). The pass brief's "2.8 m of street front" is one facet, not a fragment. The drum is modelled in full: four bands of glass and light and dark grey panels in a chequer, vertical fins at the facet joints, floor bands, a parapet and a flat roof at 9.6 m. The stone-clad modern block to its right in the photo is another outline.
- **91846958 (4 Norra Långgatan):** the cream corner house.
  - Zone `c958`: the street block with the chamfered corner. It stands on a grey plinth to about 1.1 m and has green window frames, the green boarded door with a glazed top light, and three rows of windows on the front and the chamfer. The eaves are at 10.0 m under a dark hipped roof (ridge estimated at 12.8 m). The photo caption calls it four storeys, but three rows of windows are measured below the eaves on both the front and the chamfer.
  - Zone `w958`: the south wing. Not seen; plain, flat roof at 10.0 m.
- **91846925:** the grey boarded two-storey house (zone `g925`). It has vertical boards, white corner boards and three white pilasters, white bands at 0.8 m and 3.3 m and under the eaves, four window columns with red frames in white surrounds, a dark plinth, eaves at 6.85 m and a muted tile saddle roof (ridge estimated at 9.0 m). The white rendered gateway with the red gate leaf (the east half of the passage open) closes the 3.1 m gap to the corner house and belongs to this mesh.
- **91846945:** the large block between Norra Långgatan, Larmgatan and Västra Vallgatan. There is no usable photo (the only image was an interior). It is modelled at a generic level matching its neighbours: plain rendered three-storey walls with simple windows on every outer face, a plinth, a cornice band, and a flat roof at the district height of 9.75 m. Everything about it is estimated.

Panoramas are working references only. No pixel is used as a texture; all materials are flat tints on the town textures.

## Measurement

Six Google Street View panoramas were used, all at a vertical field of view of 90° and 756×405. The bearing is the heading + 28.2°, and the pitch is 15° up throughout.

Resection: each camera was solved on the facade plane, taken 0.355 m outside the OSM line, using the reported heading (`SCR/p100/res.py` and `SCR/p82/hit.py`). Where only one corner was usable, the camera's distance from the facade was set so that the ground line reads z = 0 at the stated camera height.

| Panorama | Where, heading, notes | Google position (local) | Resected position | Resected on |
|---|---|---|---|---|
| bwGTdi_Nk-UuwSElbqP7Qw | 38 Larmgatan, 61 (upscaled half tile) | (−289.85, 164.61) | (−291.50, 163.25), h 2.35 | both ends of the red wall (two-corner resection) |
| TYAg2QberOQX-fB6EpE6_A | 40 Larmgatan, 61 | (−290.11, 194.77) | (−290.85, 193.81), h 2.3 | the office's north corner and the ground line at the Ludvig door |
| NEMUiPZCHf9ioDLkCsuJ_g | 1 Strömgatan, 333 | (−270.82, 214.89) | (−270.82, 213.17), h 2.3 | the ground line only; x kept from Google (no OSM vertex in view) |
| qzjtLjyN1xtmtmwQmPg9cg | 50 Larmgatan, 86 | (−268.84, 309.19) | (−268.75, 308.41), h 2.0 | the drum's two silhouette tangents (radius to the facade surface 9.17 m) |
| lI6ZldcBs0LxEWZS6fC36w | 4 Norra Långgatan, 152 | (−329.88, 71.20) | (−330.52, 69.57), h 2.05 | three corners (the east corner and both ends of the chamfer); bearing residuals ≤ 0.6° |
| ng-1o5NwBhp5eSqg6iJifw | Norra Långgatan, 152 | (−319.00, 71.03) | (−320.20, 69.56), h 2.3 | the grey house's west corner and the ground line; this puts the cream corner 0.5 m from its OSM corner |

**Measured values** (heights above the street; s along the front from the named OSM corner):

- *92204179:* wall top 3.75–3.85 m (taken as 3.8 m); the wall spans the full 6.0 m outline.
- *92204177* (s from the north corner):
  - the office/wing joint at s 11.6;
  - office:
    - roof slab edge 10.1 m;
    - ribbon windows 4.54–5.89 m and 7.51–8.78 m, from s 1.2 to 11.0;
    - brick bands 3.26–4.54 m and 5.89–7.42 m;
    - awning about 2.9 m;
    - lift house 4.3–8.1 along the front, top reading 11.3–11.5 m on the facade plane (it is set back, so it is modelled at about 12.6 m);
  - wing:
    - parapet 7.06–7.30 m;
    - upper ribbon 4.55–5.85 m from s 15.3 to past 26.7 (nine panes in view);
    - first-bay window s 12.0–14.1;
    - ochre brick band 3.42–4.55 m;
    - navy fascia 2.78–3.43 m;
    - glazed door s 12–14.6.
- *92204174* (s from the west corner):
  - plinth to 0.53 m;
  - shop windows 0.8–3.3 m;
  - door 1 s 9.5–11.0 (surround 9.4–11.5), top 2.98 m;
  - door 2 s 13.9–15.7 (surround 13.4–16.0);
  - pediments 3.74–4.45 m;
  - upper windows 4.45–6.21 m at s 7.9, 10.1, 12.6, 14.6, 17.3, 20.1 and 22.5;
  - cornice 7.69–8.20 m, roof edge 8.36 m;
  - the downpipe and the west-end joint at s 6.65;
  - west-end upper windows s 3.1 and 5.3, round-headed third-floor windows reading 8.4–9.6+ m;
  - dormers at s 12.6 and 18.6.
- *886305409:* storey lines about 2.3, 5.1 and 8.1 m, top 9.6 m (with the camera at 2.0 m; at 2.3 m the base reads +0.58 m, so 2.0 m was taken).
- *91846958* (with the camera at 2.05 m):
  - plinth top about 1.0 m;
  - ground windows 2.2–3.8 m;
  - second row 5.2–6.8 m;
  - third row from 8.35 m;
  - eaves 10.0–10.2 m (on the chamfer);
  - door 0.12–3.53 m;
  - window columns at s 1.3, 3.6 and 5.7 from the east corner, the door at s 5.1–6.1.
  - The chamfer rows read 0.3–0.6 m lower than the front rows; the front was followed.
- *91846925* (s from the east corner):
  - eaves 6.80–7.07 m;
  - upper windows 4.04–5.55 m;
  - ground windows 1.67–2.9 m;
  - plinth 0.65–0.9 m;
  - window columns at s 2.4, 4.4, 7.0 and 9.4;
  - pilasters at about s 3.4, 5.7 and 8.2;
  - gateway lintel about 2.8 m, red gate leaf 2.56 m high on the west half.

## Estimated

- Every ridge height and roof form except the measured eaves. Ridges: 4.4 m on 92204179, 11.3 m on the 1 Strömgatan range, 12.6 m on its west end, 12.8 m on the corner house, 9.0 m on the grey house.
- The roof materials, which are not visible from the street. The exception is the Strömgatan range, where the dark sheet and red dormers are seen.
- The eaves of the 1 Strömgatan west end (10.6 m) and its Larmgatan face.
- All back ranges and courtyard faces: `w177` except its street front, `sb174`, `w958`, all walls of 91846945, and the Strömgatan face of the office block.
- The east end of the 1 Strömgatan front beyond s ≈ 22.5.
- 91846945 entirely.
- The 1 Strömgatan camera's position along the street. No OSM vertex is in view, so x is taken from Google (typically 1.5–3.5 m off). The positions of the doors and the 3-storey/2-storey joint along that front may be off by up to about 2 m.

## Verification

- `prepare_block109.py` prints `BLOCK109_ZONES_OK`. Footprint 3011.2 m², zoned 3011.2 m², outside OSM 0.0 m², OSM not zoned 0.0 m², overlap 0.0 m², every zone non-empty.
- Sandbox: three runs (`SCR/p109/sb1`–`sb3`; the prelude was pass 107 for runs 1–2 and pass 108 for run 3). All ended in `SANDBOX_DONE` without errors. `BLOCK109_GEOMETRY 7`.
- `drop_degenerate_faces109`, with the `_thin` test, ran on every mesh after `s21_finish`. Faces dropped: 92204179 14, 92204177 23, 92204174 62, 886305409 19, 91846958 4, 91846925 14, 91846945 13. These are zero-area or sliver faces at abutting boxes and roof edges. The aerial renders were checked to confirm that the flat roofs (drum, office, 91846945) and the hipped roofs are still closed.
- Side-by-side comparisons at each photo's size, with the resected cameras (`SCR/p109/cmp_3_v*.jpg`):
  - the office and wing: the brick bands, ribbons, awning, fascia, parapet and lift house line up;
  - the Strömgatan front: the windows, door surrounds with pediments, shop windows, boarded windows, cornice and dormers line up;
  - the corner house: the window rows, door and plinth line up;
  - the grey house and gateway: the eaves, pilasters, windows and gate line up;
  - the drum: the silhouette and height match;
  - the red outbuilding: the wall extent and top match.

  The visible differences are signage, lamps, cars, the flag poles and the fact that the textures are flat tints.
- **Pending:** the official build, the FBX export and the Unreal checks. The lead fills in the build results.

## Limitations

- The Strömgatan side of the office block, the courtyards of 40 Larmgatan and 1 Strömgatan, the Västra Vallgatan face of the corner house and the whole of 91846945 are not photographed. Extra views would settle them:
  - Strömgatan looking south at the office block's north face: about (−270, 212), heading 152, pitch 15;
  - Larmgatan looking east at 91846945: about (−290, 100), heading 62, pitch 15;
  - Norra Långgatan looking north at 91846945's south face: about (−310, 70), heading 332, pitch 15;
  - Västra Vallgatan looking south-east at the corner house's west face: about (−340, 60), heading 62, pitch 15.
- The 1 Strömgatan camera could only be fixed in depth, not along the street (see Estimated).
- The drum's chequer of glass and panels is a regular pattern, not a facet-by-facet copy.
- The Kalmarhem sign, the Ludvig & Co lettering, flags, lamps and the green downpipe of the corner house are omitted.

## Official build

The lead's build of pass 109 passed the Blender geometry checks and the FBX export, and two rebuilds gave identical meshes. Passes 28–108 are unchanged except the earlier intended changes (pass 85's prison building, corrected by pass 103, and pass 98's three meshes re-created by pass 107). The Unreal import and its checks are deferred.
