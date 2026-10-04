# Pass 124: the approach to Kalmar slott and its courtyard

Pass 124 makes one continuous walk from Kungsgatan and Stadsparken to the castle courtyard, and corrects what pass 27 (the castle) and pass 98 (the mainland) got wrong or left out along it:

- the park end of the footbridge to the ravelin, which stood 3.8 m above pass 98's flat park with nothing under it;
- the timber bridge and the drawbridge;
- portal A with the arms tablet of 1568, and the vaulted passage under the rampart;
- Västra förborgen (the outer bailey) and portal B;
- the gate passage through Kuretornet and the west range, which pass 27 did not model (its gate was a blind recess);
- portal C and the courtyard portals D, E and F;
- the well house of 1578, which pass 27 built octagonal;
- the courtyard paving.

Route, after Olsson (1957): bridge → portal A (arms tablet 1568) → the vaulted passage under the rampart → Västra förborgen → portal B → gate passage → portal C → courtyard.

## What pass 27 had, what changed and why

### Meshes

| Mesh | Status | How |
|---|---|---|
| `SM_Castle27_Walls` | re-created, `corrects_pass=27` | pass 27's code, verbatim, with three edits (see below) |
| `SM_Kalmar_Slott` | re-created, `corrects_pass=27` | pass 27's code, verbatim, with two edits |
| `SM_Kalmar_Slott_Towers` | re-created, `corrects_pass=27` | pass 27's code, verbatim, with two edits |
| `SM_Castle27_Bridge` | re-created, `corrects_pass=27` | new code (the whole mesh is bridge) |
| `SM_Slott98_Trees` | re-created, `corrects_pass=98` | pass 98's code, verbatim; each tree's base is lifted with the park |
| `SM_Castle124_Approach` | new | the lifted park at the footbridge, the city wall, the stair, the abutment's plinth |
| `SM_Castle124_Passage` | new | the gate passage |
| `SM_Castle124_Portals` | new | portals B, C, D, E, F |
| `SM_Castle124_Well` | new | the hexagonal well house |
| `SM_Castle124_Paving` | new | slab paths in the courtyard, setts in Västra förborgen |

No other mesh is touched. `SM_Castle27_Ground`, `_Ravelin`, `_Postejer`, `_Islets`, `_Riprap`, `_Guns` and every pass 98 mesh except the trees are as before.

**Choice of method.** The three large pass 27 meshes bundle many things (the walls mesh holds the revetment, the lower wall, the counterscarp, the tunnel and the gate building; the castle mesh holds all four ranges and the well). Removing faces by region would have left holes and doubled surfaces where new parts meet old ones, so they are re-created in full, as pass 120 did with pass 14. `build_block124.py` reads `build_castle27.py` and runs it in a private namespace, `NS124`:

- pass 27's header (its JSON, `zh`, and its own exec of the baronen23 and station24 helpers) and every function it defines;
- its material keys mapped to the existing `M_Castle27_*` materials, without re-creating them (pass 27's material loop deletes and rebuilds them, which would strip the other castle meshes);
- its walls, castle and towers sections, each cut out of the file by its section comment and edited by exact string replacement. Every replacement asserts that the original text occurs exactly once, so a change to pass 27's file stops the build instead of silently doing something else.

The unchanged parts therefore come out as pass 27 built them, through pass 27's own `c27_finish` (triangulation and its sliver filter), followed by `drop_degenerate_faces124`. The bridge was rewritten instead, because nearly every part of it changes.

### Edits to pass 27's code

**Walls (`SM_Castle27_Walls`).**
- **Portal A.** Pass 27 had a grey ashlar block 6.6 m wide with a 3.4 m arch, 5.1 m high, and a raised tablet whose top stood 0.65 m above the rampart's edge. The photographs (Oregran 2014, ThomasLendt 2018, Steinkatz 2024) show a lighter, narrower block, about 1.5–1.6 times the arch width, with the tablet's cornice at the top of the wall. Now:
  - the block is 3.9 m wide (the battered revetment comes 1.35 m closer on each side), light sandstone-coloured;
  - the arch is 2.4 m wide, springs at 2.35 m and reaches 3.55 m, with a ring of voussoirs 0.42 m deep and impost blocks;
  - Mackle's tablet is a recessed field 2.8 × 2.0 m in a raised frame, on a sill, under a triglyph frieze and a cornice that ends just under the coping. The relief is blocks only: a crowned shield between two lions. No heraldry is modelled, as asked.
- **The passage under the rampart.** Pass 27: 3.2 m wide, 4.7 m high, all rubble, a cobbled floor. The 2017 Commons photograph of the curved passage shows rubble walls, a whitewashed barrel vault and a path of flat stone slabs between strips of cobbles. Now 3.0 m wide, walls 2.3 m, semicircular vault to 3.8 m, built of closed solids (pass 27's single-sided quads could face either way after the normal recalculation). A slab threshold runs from the tunnel through the block to its face. The counterscarp opening at the inner mouth is resized to match (3.0 m, 2.3 + 1.5 m).

**Castle (`SM_Kalmar_Slott`).**
- **The well house** is removed from this mesh and rebuilt in `SM_Castle124_Well`.
- **The west courtyard front** (pass 27's two collinear pieces from the courtyard's north corner) is built as one wall with the gate passage's opening, 2.8 m wide and 3.8 m high, for portal C. The windows and door of pass 27's rows are kept at their old positions except those within 2.7 m of the portal's edges, which the portal covers. One cornice runs along the whole front.

**Towers (`SM_Kalmar_Slott_Towers`).**
- Pass 27 put the castle gate as a blind recess on Kuretornet's north-east face, behind the walled gate building, where no one could reach it.
- OSM way 90613986 (`tunnel=yes`, sett) is the gate passage; it starts inside Kuretornet near its north corner and runs to the courtyard. The 1957 photograph of Västra förborgen (`dimu-021017081614.jpg`) and the postcard (`dimu-021017025491.jpg`) show portal B on a face turned towards the passage under the rampart, with the gate building's corbelled wall at right angles beside it: that is Kuretornet's north-west face.
- So the blind recess is gone, portal B's opening (2.4 m wide, 3.8 m high) is cut in the north-west face, and the passage's arch is cut where it leaves Kuretornet on the courtyard side.
- The passage line is OSM's, moved 0.9 m south-west so that portal B (4.4 m wide) stands clear of the gate building at the north corner. Its length from the north-west face to the courtyard front is 22.1 m.

### New and rebuilt parts

**The joint with the mainland (`SM_Castle124_Approach`, trees).**
- Pass 27 measured the ravelin at 5.6 m above the water and put the footbridge's park end 0.2 m lower (z 4.07). Pass 98 laid the whole mainland flat at z 0.30. The bridge's abutment box (pass 27) floated 0.35 m above the ground, and the bridge ended 3.8 m above Kungsgatan.
- OpenStreetMap shows how it really fits:
  - a city wall (way 1084130858) along the north edge of the grassed ditch round the ravelin (`landuse=grass`, way 1084130843); the bridge lands on the wall;
  - Kungsgatan (way 44397508, sett) and the park footway (440762333) arrive at the wall top;
  - a wooden stair of **30 steps** with a ramp and a handrail (way 93293022) climbs from the ditch path along the wall to the bridge. Thirty steps of about 0.125 m is 3.75 m: pass 27's height difference between the ditch and the bridge is right, and the park beside the bridge stands at the bridge's level, not at the ditch's.
- So the park is lifted, not the bridge lowered. `prepare_block124.py` takes pass 98's land inside 54 m of the landing and north of the ditch (4,676 m²), clips pass 98's own ground layers to it on a 1.5 m grid (land, the Stadsparken lawn, the paths, Kungsgatan) and writes them to `source/block124.json`. The build lays them again at their pass 98 offsets plus a lift: the full 3.72 m within 6 m of the landing, falling as a half cosine to nothing at 54 m. The steepest grade is about 1:8 (7°), the mean 1:13. Kungsgatan's sett meets the deck 15 mm below it.
- The ditch stays at 0.30. The city wall is built along the domain's ditch edge (rubble, 0.35 m thick, stone coping flush with the lawn), and a quay face where the lifted ground meets the water east of the landing.
- The wooden stair: 30 treads of 0.42 m and 0.124 m rise, 1.5 m wide, on two stringers, with posts and a rail on the open side and a rail along the wall, from the ditch path up to the abutment's top beside the deck (OSM line moved to sit 1.15 m off the wall). The footbridge's west rail is open there.
- The abutment gets a plinth from the ditch floor to its underside (in pass 27's `LowWall` material).
- Eleven pass 98 trees stand inside the lifted area. `SM_Slott98_Trees` is re-created with pass 98's code unchanged (same random streams), except that each tree's base is raised by the lift at its position, so no trunk is buried.

**The bridge and the drawbridge (`SM_Castle27_Bridge`, new code).** Pass 27 had bents every 2.7 m, the deck running into the arch, and a drawbridge frame 5.8 m out with level arms. From the photographs (Commons 2017 from the rampart, 2018 on the bridge, 2024 close-up; DigitaltMuseum 1934 west front and the 1930s–40s postcard of the drawbridge):
- bents of two piles every 2.3 m, each pile with a pale collar at the waterline, a cap beam and three stringers; posts every 1.6 m with a top rail and a knee rail;
- the deck ends at portal A's face; the last 4.2 m is the leaf, a separate panel with its own rails;
- under the leaf's hinge a pier of eight clustered piles with a heavy cap (the 2017 photograph from the rampart);
- the gallows stands on the pier: two posts beside the deck, a head beam 6.9 m above the deck (just above the rampart's edge, as in the 2024 photograph), knee braces, raking struts down to the deck on both sides;
- two lifting beams lie over the head beam: their inner ends rest on the block above the tablet, their outer ends project 1.2 m beyond the frame and stand higher (the 1934 photograph, taken from the dry moat, shows them sloping down towards the wall). Chains hang from the outer ends to the deck edge (postcard), and short chains with rings hang from the inner ends (2014 photograph);
- the footbridge from the park to the ravelin is as pass 27 built it (same line, width and levels), on the same bents, without collars (it spans the dry ditch).

**Västra förborgen and portal B (`SM_Castle124_Paving`, `SM_Castle124_Portals`).** Pass 27 showed the outer bailey as grass with a gravel path. The 1957 photographs show setts. A strip of setts 3 m wide with a slab path down the middle now follows OSM's sett footway (90613989) from the passage under the rampart to portal B. Portal B: two fluted Doric columns on tall plain pedestals (1.6 m), 3.3 m shafts, an entablature with seven triglyphs and square metope plates (Olsson: ox skulls and round shields, not modelled), a lean-to roof of sheet metal, and the round arch with impost blocks.

**The gate passage (`SM_Castle124_Passage`).** A vaulted passage 3.0 m wide, walls 2.4 m and a semicircular vault (3.9 m clear), whitewashed above a stone plinth band, with a slab path between cobbles and two iron lanterns. It rises from Västra förborgen (z 3.70) to the courtyard (z 8.18): level for 1.2 m at each end and an even ramp between. **That ramp is 22 % (12°)**: it is the 4.5 m difference between pass 27's castle foot and its courtyard level over 19.7 m. A cobbled ramp was preferred to a stair because carts used this passage. See Limitations.

**Portal C and the courtyard portals (`SM_Castle124_Portals`).**
- Portal C (Västra borggårdsportalen): two storeys. Below, two pairs of fluted columns on pedestals either side of the arch, 5.3 m entablature; above, two pairs of smaller columns either side of the arms tablet with a crowned initial block, an entablature and a low pediment; 8.4 m high in all (Mayer's lithograph puts its top at about 0.6 of the courtyard eaves height).
- D, E and F dress three of pass 27's courtyard doors and do not move them: D (Drottningtrappan, north range) with banded Doric columns, E (Kungstrappan, west range) with pilasters and a triangular pediment, F (Kyrkportalen 1568, south range) with tapering herm pilasters, a pediment and a small date tablet. Their positions on the fronts are pass 27's (the middle of the longer front pieces), not measured.
- Stair towers: none stand out from the courtyard fronts in the photographs or the lithograph, so none are modelled.

**The well house (`SM_Castle124_Well`).** Pass 27: an octagonal base, eight columns, four pediments, an octagonal lantern. Now hexagonal throughout, after Olsson (Fornvännen 1957) and the photographs (`castle27/swe-kalmar-slott-006.jpg`, 2022; `dimu-021017055878.jpg`, about 1900):
- a round platform of two steps;
- the domed shaft, 1.5 m across, dark inside;
- a hexagonal parapet with base and cap mouldings, six corner pedestals with masks, a cartouche panel on each face;
- **columns at each corner.** The close photograph shows one round Doric column on the outer part of each pedestal and one square pier inside it, under the inner edge of the entablature. Olsson's single column per pedestal is therefore right for the round order; the extra shafts in the photographs are these square piers, and in the older photograph also the far corners seen through the house. Six round columns and six square piers are modelled;
- a hexagonal entablature with triglyphs, a low pediment over each face, six curved brackets up to a moulded slab on a central drum;
- a lantern of six herm pillars, a cornice, a hexagonal dome with six round-topped gables (built as triangle fans), and the cast-iron dolphin on its nose.

Heights from the photograph of about 1900, scaled on the man standing beside the well at the same depth (1.75 m = 126 px): pedestals to 1.36 m, columns 1.8 m, entablature top 3.74 m, slab 4.85 m, herms to 6.0 m, dome to 6.9 m, dolphin's tail 7.45 m. After the first sandbox comparison the part above the entablature was raised by 0.35 m to match the 2022 photograph's proportion.

**Courtyard paving.** Pass 27's cobbles stay. The photographs (2017, 2022) and Mayer's lithograph show flat slabs round the well and slab paths across the cobbles: a slab apron from 2.3 to 3.1 m round the well and 1.2 m slab paths from it to portals C, D, E and F.

## Sources

| Source | Licence | Used for |
|---|---|---|
| OpenStreetMap: ways 91222140, 1084130858, 1084130843, 93293022, 44397508, 440762333, 90613986, 90613989 (`references/osm-slott98.json`, `references/castle27/osm-castle27.osm`) | ODbL | the joint, the wall, the stair (30 steps), the gate passage, the bailey footway |
| `commons-kalmar-castle-bridge-and-entrance-june-2018.jpg` (ThomasLendt) | CC BY-SA 4.0 | bridge, rails, portal A's block, camera 666 |
| `commons-entrance-bridge-to-the-kalmar-castle-2017-07-30.jpg` | PD | bents, pile collars, the pier under the leaf, the gallows from above |
| `commons-zugbr-cke-schloss-kalmar.jpg` (Steinkatz 2024) | CC BY 4.0 | the gallows, braces, beams; camera 667 |
| `commons-ing-ngen-till-kalmar-slott.jpg` (Oregran 2014) | CC BY-SA 3.0 | portal A, the tablet, the inner chains; camera 668 |
| `commons-kalmar-castle-entrance-corridor-2017-07-30.jpg` | PD | the passage under the rampart |
| `dimu-021017066800.jpg` (1934) and `dimu-021016518916.jpg` (Kalmar läns museum) | Public Domain Mark | the gallows and the slope of the lifting beams; the hemliga värnet |
| `dimu-021017081614.jpg` (Olsson 1957), `dimu-021017025491.jpg` (postcard) | Public Domain Mark | portal B, its position, the setts of Västra förborgen |
| `dimu-021017054934.jpg` (1972) | Public Domain Mark | the gate passage's vault at portal C |
| `commons-commission-scientifique-du-nord---a.-mayer---cour-du-ch-teau-de-kalmar.jpg` (about 1840) | PD | portal C's two storeys and height, slab paths |
| `castle27/swe-kalmar-slott-006.jpg` (-wuppertaler 2022), `castle27/kalmar-castle-internal-courtyard-2017-07-30.jpg` | CC BY-SA 4.0; PD | the well house, the columns and piers, courtyard paving, camera 669 |
| `dimu-021017055878.jpg` (about 1900) | Public Domain Mark | the well's heights (scaled on the man beside it) |
| Olsson, *Fornvännen* 1957, pp. 137–183 (DiVA; read, not copied) | open access, no licence stated | the route A–C, the portals' orders, the well house (hexagonal, six pedestals, dolphin, shaft 1.5 m) |

Google imagery was not used. No pixel of any photograph is used as a texture; the new materials (`M_Block124_*`) are flat tints on the town textures, and the rest reuses `M_Castle27_*` and `M_Block98_*`.

## Measurement

There were no Street View panoramas for this pass, and the Commons and museum photographs have no known camera positions, so no camera was resected. The four calibration cameras (666–669) are placed by eye at the photographs' viewpoints for comparison only.

| Value | Read from | Result |
|---|---|---|
| Ditch to bridge, park end | OSM stair: 30 steps | 30 × 0.125 = 3.75 m; pass 27's model has 3.77 m |
| Portal A opening | photographs: people at the gate (2018) and the arch's height/width ratio (2014: 1.52) | 2.4 × 3.55 m |
| Portal A block width | 2024 photograph: block 1.53 × arch | 3.9 m |
| Bent spacing | 2017 photograph from the rampart: about 11 bents over the fixed span | 2.3 m |
| Gallows head | 2018 and 2024 photographs: at or just above the rampart's edge | 6.9 m above the deck |
| Portal B | 1957 photograph, scaled on a 2.4 m opening | pedestals 1.6 m, shafts 3.3 m, top 6.0 m, width 4.4 m |
| Portal C height | Mayer: about 0.6 of the courtyard eaves height | 8.4 m |
| Well house | photograph of about 1900, man beside it (126 px/m) | see above |

## Estimated

- The lift's shape and radius (a half cosine over 48 m). OSM gives the wall and the stair, not the park's levels; the park beyond 54 m stays at pass 98's 0.30.
- The city wall's section, coping and colour; the quay face on the water.
- The stair's width, stringers and rails (OSM gives the count, the ramp and the handrail).
- The drawbridge's leaf length (4.2 m), the pier, the beam lengths and the chains.
- Portal B's and portal C's details: the fluting is 16 facets, the metopes are plain plates, the herms and initials are blocks.
- The positions of portals D, E and F (pass 27's doors).
- The gate passage's section, its finish and its floor (the ramp follows from pass 27's levels).
- The well house's cartouches, masks and dolphin are blocks and rods.

## Verification

- **Prepare.** `prepare_block124.py` prints `BLOCK124_PREPARE_OK`: domain 4,675.7 m², the clipped land layer 4,675.6 m² (it must cover the domain within 1 %), domain ∩ ditch 0.02 m², the landing 0.000 m from the OSM wall, stair line 13.56 m.
- **Sandbox.** Two runs (prelude pass 123; `SCR/p124/castle/build_block124_check.py`, logs `SCR/p124/castle/log1.txt`, `log2.txt`) print `SANDBOX_DONE` without errors. Each pass 27 replacement asserted its original text once. Both Kuretornet openings were cut (the build asserts two).
- **Export frame check.** The exporter's preparation and frame check (the pass 123 wrapper's method) ran on all ten meshes in both runs: 0 invalid loops in every mesh (the exporter's fallback frame covers 593 loops in the walls, 5,144 in the castle, 204 in the towers, 8 in the approach and 26 in the paving), and the test FBX export succeeded for 10 of 10.
- **`drop_degenerate_faces124`** (with the `_thin` test) runs on every pass 124 mesh, including the re-created ones after pass 27's own `c27_finish`. It removed 132 faces from the walls, 2 from the towers and none from the other eight meshes (the walls' and towers' faces are pass 27's arch-spandrel slivers that its own filter lets through).
- **Walk and joint checks** (ray casts every 0.2 m, step = height change between samples, obstruction rays at 0.45 m and 1.4 m, headroom ray 2.0 m): 
  - **The whole route** from Kungsgatan (−956.9, −123.4) over the footbridge, the ravelin path, the bridge and the leaf, through portal A, the passage under the rampart, Västra förborgen, portal B, the gate passage and portal C into the courtyard: 1,057 samples, none missing, largest step 0.046 m (the start of the passage ramp), no obstruction at either height, no headroom under 2.0 m. Height range 0.34 to 8.19.
  - **The joint**, sampled across the landing: lifted park 4.055 at 0.2–3 m north of the landing (4.030 two metres west), deck 4.072 at 0.3 m south, 4.078 at 1 m, 4.086 at 2 m. The step from the park to the deck is 17 mm.
  - **The park footway east** from the landing down the lifted park to (−903.9, −174.9): largest step 0.024 m, no obstruction; it ends at z 2.14, still on the lifted ground.
  - **The wooden stair** from the ditch path to the bridge: largest step 0.124 m (one riser), no obstruction or low headroom.
  - **The courtyard**: from portal C to portals D, E and F along the slab paths, and a ring round the well at 3.4 m: largest step 0.012 m (the slab edges), no obstruction.
  - In the first run the walk check itself started two routes at the wrong height and walked one route through portal C's pedestals; those were check errors, corrected in the second run.
  - The check also counts ray hits whose face normal points less than 45° from up. They occur only on single-triangle ground and deck faces built the way passes 27 and 98 build them (pass 98's greens, pass 27's ground and deck, and the lifted park, which reuses pass 98's method); no surface on the route is steeper than 1:4.5 (the passage ramp). They are faces whose normal the mesh finishing turned downward, as on pass 98's own ground; the lead may want to look at whether that matters in Unreal.
- **Side-by-side comparisons** with the photographs: `SCR/p124/castle/sb2/cmp_cal_bridge.jpg`, `cmp_cal_draw.jpg`, `cmp_cal_portalA.jpg`, `cmp_cal_well.jpg`. 
  - **Bridge (666, ThomasLendt 2018).** The deck, rails, the lower wall with its openings, portal A's block and the gallows sit where the photograph has them; the camera is placed by eye, so the castle behind reads somewhat larger than in the wide-angle photograph.
  - **Drawbridge (667, Steinkatz 2024).** The block's width against the arch, the tablet under the rampart's edge and the gallows' head just above it agree. The model's camera stands closer than the photographer, so the posts dominate.
  - **Portal A (668, Oregran 2014).** Arch proportions, the voussoir ring, the tablet's frame, frieze and cornice, and the chains with rings at the beams' inner ends agree in arrangement; the relief is blocks.
  - **Well house (669, 2022).** Hexagonal plan, pedestals, round columns with square piers behind, pediments, lantern and dolphin agree in arrangement and proportion after raising the upper part 0.35 m.
- **Pending.** The official build and the Unreal checks are pending; the lead fills in the build results.

## Limitations

- **The gate passage is steep (22 %).** Pass 27's courtyard is 4.5 m above its castle foot, measured from a courtyard panorama that was 13.5 m off; nothing in this pass's sources gives the courtyard level, and Kalmar slott's accessibility page mentions no steps in the passage. If the courtyard is lower, the ramp flattens by itself (it is computed from pass 27's levels), but the courtyard floor, fronts and well would have to move with it. Worth a site check.
- The lift is a smooth estimate of the park round the bridge; the real park may be level over a wider area. Pass 98's flat ground stays under the lifted surface (hidden).
- The tablet's relief, the portals' sculpture, the metopes, the masks and the dolphin are simple blocks.
- Portal B sits 0.9 m off the OSM passage line, on a reading of two photographs.
- The interior of the gate building, the hemliga värnet's interior, the second door in the counterscarp and the steps up the rampart are as pass 27 left them.
- No collision test in Unreal; the ray-cast walk is a Blender check only.
- Extra views that would help: inside the gate passage looking towards the courtyard (from about (−874, −285), heading 112, pitch 0), to settle the floor's slope; and the park end of the footbridge from Kungsgatan (about (−940, −150), heading 140, pitch −5), to see how the park meets the wall.

## Official build

The lead's build of pass 124 passed the Blender geometry checks and the FBX export, and two rebuilds gave identical meshes. Prevhash reports SM_Slott98_Trees (pass 98 and pass 107 versions) as changed. That is intended: the tree bases rise with the lifted park. The other changes are the earlier intended ones. Pass 27 is outside prevhash's range; its three re-created meshes are this pass's deliberate corrections. The Unreal import and its checks are deferred.

Lead's review note: in the drawbridge comparison, portal A's ashlar block and its tablet read larger and paler than in the photograph. The camera there is placed by eye, so this is a candidate for a later refinement, not a measured error.
