# Pass 144: Klapphuset, red walls and a narrower pier (corrects pass 122)

Pass 144 re-creates Klapphuset (OSM 93199604, mesh `SM_Kvarnholmen_House_93199604`), the small boarded house standing in the water off Bastion Carolus Philippus. The reviewer reported: "it has become white and the pier is too wide. It should be red." Pass 122 last built the house, from the satellite only. This pass builds it from photographs.

## Why it read white

Pass 122's walls were falu red (`M_Block122_Falu`, TownIvory with a tint to sRGB 0.50/0.17/0.13). That spec is red in `exports/manifest.json`, in Blender, and in the Unreal material asset, which multiplies the texture by the same tint as every other tinted pass material. No later pass re-creates or overrides the mesh: a search of all `scripts/build_block1*.py` (and every other script) for 93199604 and Klapphuset finds only pass 17 and pass 122. The white came from everything around the red walls:

- **The roof** was `M_Block122_RoofGrey`, a mid-grey metal (sRGB 0.42/0.40/0.38, metallic 0.15). Pass 122's iteration 2 lightened it from dark to grey to match the satellite, where the sunlit roof looks pale. The real roof is black standing-seam metal. A light metal roof covers most of the house seen from the bastion or from above, and in daylight it reads close to white.
- **The pier and the east deck** were `M_Block122_Timber`, a pale grey-beige (sRGB 0.56/0.53/0.48) on the TownPaintWhite texture: a 20 × 2.2 m slab plus a 1.6 m deck along the whole east end.
- **White trim:** white corner boards (0.20 m) on all four corners, and a white eaves board (0.24 m) round the whole house.

Taken together, the pale parts were more of the house's visible area than the red walls. The sandbox measures this; see Verification.

## What the pass builds

All from `source/block144.json`, written by `scripts/prepare_block144.py`:

- **Walls:**
  - falu red lap boarding all round (`M_Block144_Falu`, sRGB 0.48/0.15/0.11 on TownIvory);
  - red corner boards and a red drip board at the floor;
  - eaves at 2.95 m above the floor (photo 2.93 m; pass 17's value kept);
  - the floor at z = 0, 1.33 m above the model's water.
- **Windows.** The only white on the house is the window frames: pairs of three-by-two-pane casements in one white surround with a sill, set high under the eaves (bottom 1.52 m, height 1.05 m, pair width 2.75 m). There are:
  - three pairs on the south front;
  - four pairs and a small two-light window on the north front;
  - two pairs on each end.
- **The entrance:**
  - the green glazed double door (frame 1.80 × 2.25 m) at the OSM entrance node;
  - it stands in a shallow red bay, 2.5 m wide and 0.25 m deep;
  - the bay has its own small hip canopy (3.4 m wide), which runs back into the main roof.
- **The roof:**
  - a low black hip of standing-seam metal (`M_Block144_Roof`, sRGB 0.13/0.13/0.14), with seams about 0.55 m apart on the long slopes;
  - an eaves overhang of 0.8 m from the outline (0.45 m beyond the wall face), with a dark fascia and soffit;
  - the ridge at 4.25 m;
  - two dark ventilators with louvres and pyramid caps, ±4.36 m from the centre.
- **Skirting:** pale grey vertical boards (`M_Block144_Skirt`, sRGB 0.55/0.55/0.53) from the floor down into the water (z −1.45) all round, as in every photo. The house's piles are hidden behind it and are not modelled.
- **The pier:**
  - a 1.9 m deck of weathered grey boards (`M_Block144_Timber`, sRGB 0.50/0.47/0.43) from the bay front to the shore point of pass 122;
  - it runs along the south wall's outward normal from 0.22 m east of the entrance node, and is 19.84 m long;
  - stringers and pairs of round piles (`M_Block144_TimberDark`) under it;
  - railings on both sides: posts every ~1.65 m fixed to the deck edge, a 0.14 m handrail board at 1.05 m and a knee rail. It is 2.2 m over the handrails.
- **No east deck.** No photo shows one; see the Measurement section.

## Measurement

| Source | What | Camera / scale | Values |
|---|---|---|---|
| Commons "Klapphuset, Kvarnholmen, Kalmar.jpg" (TS Eriksson, 2015-04-30, CC BY-SA 4.0), viewed at 1920 px, screenshot 1014 px (`SCR/p144/commons_entrance2015.jpg`) | south front, square-on from the pier's shore end | wall 105–835 px = 17.45 m (OSM), 41.9 px/m at the wall | eaves row 287, boarding bottom 410 → 2.93 m; window pairs centred 2.03, 6.50, 14.20 m from the SW corner, 2.75 × 1.05 m, bottom 1.52 m; door at 9.92 m (OSM entrance node 9.93 m); door frame about 1.9 × 2.3 m; ventilators ±4.4 m; pier about 2.1 m between the rail posts near the house; corners and fascia not white |
| Commons "Klapphuset Kalmar 03.jpg" (`commons_klapphuset03.jpg`) | north front, square-on across the water | wall 388–778 px = 17.45 m | pairs at 1.79, 5.82, 9.89, 14.05 m from the NE corner; a small window read at 16.73 m (built at 16.65 m, 0.9 m wide, to keep it clear of the corner board); skirting to the water; no deck at either end |
| Commons "Klapphuset 01.jpg" (`commons_klapphuset01.jpg`) | south front and east end, from the east shore | not resected | two pairs on the east end; pier on posts with railings; grey vertical skirting; **no deck on the east end** |
| Commons "Klapphuset entre sept 2024.jpg" (`commons_entre2024.jpg`) | south front from the pier's shore end | not resected | black standing-seam roof, green door, railings; the pier about 1.4 × the door frame at the house end (about 2.1–2.5 m, scale uncertain) |
| Google user photosphere CIHM0ogKEICAgICK9Zy3Wg (Apr 2021, viewed only), `pano_shore.jpg`, `pano_shore_zoom2x.png` | from the shore at the pier's south end, heading 15, pitch 2, vfov 90 | resected on the SW corner (u 147.5), the OSM entrance node (u 343) and the SE corner (u 458.5): camera **(426.57, 98.14)**, bearing residuals under 0.3°; pano position (427.41, 99.53) | handrails at the house end hit the door plane at −0.88 and +1.32 m from the entrance node: **2.20 m over the handrails**, axis +0.22 m east of the node; door frame −0.69…+1.11 m (1.80 m) |
| Google user photosphere CIHM0ogKEICAgICK9ZynPw (Apr 2021, viewed only), `pano_pier.jpg` | on the pier, looking at the door, vfov 75 | not resected (its heading disagrees with the model by about 12°) | entrance bay with its own hip canopy (about 1.75 × the door frame wide); rails at the door about 1.14 × the door frame apart (≈ 2.0–2.2 m) |
| Google satellite (view only), `sat30_klapp.jpg` (2 m bar = 50 px, 25 px/m), `sat125_klapp.jpg` | top-down | roof 452 px ≈ 18.1 m with the eaves | pier bright core 53–58 px = 2.1–2.3 m, soft edges to about 3 m (resampled imagery, blur); pier ≈ 20 m from the south wall to the shore; a pale band about 2 m wide east of the roof |

**The pier width.** The resected photosphere gives 2.20 m over the handrails at the house end. The deck between the posts is about 1.9 m: the 2015 photo gives about 2.1 m between the post faces, and the posts stand outside the deck edge. The satellite's bright core (2.1–2.3 m) cannot separate the deck from the handrails. Pass 122's estimate of 2.2 m was close to the overall width. But it was built as a 2.2 m pale slab with no railing, flush with the deck edge, which reads as a wider and whiter platform than the real railed walkway. The pier now has a 1.9 m deck and railings outside it.

**The east deck.** Pass 122 read the pale band east of the roof on the satellite as a 1.6 m deck. In none of the four Commons photos or the two photospheres does the east end have a deck: the skirting runs straight down to the water. The band is most likely the sunlit east hip of the roof or the skirting seen at an angle. It is not built.

## Estimated

- The west end's windows. No photo shows the west end square-on, so it has two pairs like the east end.
- The depth of the entrance bay (0.25 m), and the canopy's height and how far it projects (eaves 2.82 m, 1.45 m out from the outline). These were read by eye from the 2015 photo and the pier photosphere.
- The roof pitch and ridge (4.25 m; pass 17's 4.2 m kept). The photos are taken from too low to measure them.
- The pier's length (19.84 m). It ends at pass 122's shore point, which the satellite confirms to about ±1 m. The pier's arch and the wider landing at the shore are not modelled, so the deck is flat at z = 0.
- The colours. They were matched by eye to the overcast 2015 photos.

## Verification

- **Zones/prepare:** `KALMAR_GEO=SCR/pylib python3 scripts/prepare_block144.py` prints `BLOCK144_PREPARED OK`. Its checks: the OSM entrance node is on the ring and on the south wall line (within 0.02 m); the photo door position matches the node (within 0.1 m); the pier end projects to 20.44 m; every opening lies inside its wall, 0.3 m clear of the corners and of each other.
- **Sandbox** (`SCR/sandbox.py`, prelude 143, wrapper `SCR/p144/build_block144_check.py`), two runs. Both printed SANDBOX_DONE, with no errors.
  - **Run 1:** first build.
  - **Run 2:** the roof and the fascia/soffit rebuilt as closed solids, because run 1 left about half the roof faces pointing down after `Mesh.finish`'s normal recalculation (pass 122's roof has the same fault: only 30 of 203 m² of RoofGrey faced up). The shore camera was also raised to 1.7 m.
- **Change set:** hashes of every mesh before and after the build. Only `SM_Kvarnholmen_House_93199604` changes (`CHANGED144`).
- **Repeatability:** a second build on the result changes nothing (`REPEAT144 True`).
- **Properties:** detail_pass 144, corrects_pass 122, osm_way 93199604, reference_notes set. Materials: M_Block144_Falu/Roof/Skirt/Timber/TimberDark/Frame/DoorGreen/Vent and M_Town_Glass; nothing from pass 122. 30,432 vertices and 32,892 faces after the degenerate filter (18 faces dropped).
- **Degenerate faces:** 0 left after the build (zero area, repeated corner, under 0.1 mm).
- **Export frame check:** pass 141's wrapper of `district_tangent_export`, run after the export tail's preparation. 0 invalid tangent frames (195 repaired by the exporter's fallback), and 1 of 1 exported to FBX.
- **What reads white, measured.** The sandbox summed the face area of each material, weighted by how much it faces up (the view from the bastion or from above):
  - **Before (pass 122):** M_Larm26_Dark 171 m² (the soffit plane, facing up under a roof whose slopes partly face down), Falu 77, Timber 59, TimberDark 31, RoofGrey 30, Frame 21.
  - **After:** Roof (black) 239, Falu 67, Timber 45, Skirt 19, Frame 14.
  In pass 122's own Workbench renders the roof is light grey, and the pier and deck are the palest large surfaces (`SCR/p144/r2/before_*.png`).
- **Photo comparisons** (`SCR/p144/c_*_r2.png`: photo | before | after):
  - **`c_shore_r2.png`**, against the resected photosphere: door and window-pair positions, the black roof with its ventilators, the canopy over the bay, the railed pier to the door and the grey skirting all match. The pier's near end comes into the frame a little further left than in the photo; the model has no flared landing.
  - **`c_north_r2.png`**, against Commons 03: four pairs and the small west window. In the photo the water stands higher on the skirting than the model's fixed water plane.
  - **`c_bastion_r2.png`**, against Commons 01: no east deck; skirting all round.
  - **`c_pier_r2.png`**, against the pier photosphere: the bay, door and canopy.
  - **`c_top_r2.png`**, against the satellite: the pier position and length.
- **Official build:** done by the lead on 2026-10-04; see "Official build". Unreal: imported in the v0.1.8 public sync.

## Limitations

- The pier's shore end does not have the real flared, arched landing.
- The house's own piles and floor structure are hidden behind the skirting and are not modelled.
- The standing seams are thin rods on the long slopes only; the hip ends are plain.

## Official build

The lead built pass 144 officially on 2026-10-04.
- **Checks:** the geometry check passed on the second rebuild (True), the FBX audit passed (exit 0), and the two rebuilds gave identical meshes.
- **Prevhash:** pass 122's `SM_Kvarnholmen_House_93199604` changed as intended, and pass 143's four meshes are identical. The rest are known earlier corrections.
- **Dry renders:** cameras 805–807, 3 of 3.
