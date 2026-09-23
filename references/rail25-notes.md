# Tracks and platforms at Kalmar C — pass 25

Research date: 2026-09-23. Railway area from the railway bridge at the north-west edge of the model to the buffer stops south-east of the station house: 15 track pieces (1 986 m), six platform areas (3 259 m²), buffer stops, dwarf signals, a pedestrian level crossing and the overhead line over tracks 1–3. Replaces the flat island surface over the track area. Photographs are working references only: no pixel is used as a texture, and nothing from Google was extracted.

## Sources

- **OpenStreetMap** (`references/osm-kvarnholmen-full.osm`): every `railway=rail` way clipped to the modelled land, the `railway=platform` areas 1a, 1b, 2a, 2b and 3, footway 308440739 with its three `railway=crossing` nodes (`crossing:barrier=full`), 7 `railway=buffer_stop`, 9 `railway=switch` and 7 `railway=signal` nodes. The signals near the station are tagged `railway:signal:main=SE:Mellansignal`, `railway:signal:main:height=dwarf`, with `railway:signal:direction` and `railway:signal:position`. Track 1 is tagged `electrified=contact_line`.
- **Photographs** (Wikimedia Commons, stored in `references/station24/`, licences in `sources.json`):

| File | Author, date, licence | Used for |
|---|---|---|
| kalmar-central-2022-2.jpg | Johannes Scherman, 2022-02-26, CC BY-SA 4.0 | Island platform 2b towards the crossing: edge zoning, shelter on blue columns with curved roof, platform clock on its own column, lattice portals with drop tubes and brown insulators, cantilevers, platform wall |
| kalmar-central-2022.jpg | Johannes Scherman, 2022-02-26, CC BY-SA 4.0 | Dwarf main signal Kac 14: body, lamp layout and visors, yellow rim and identity plate; timber sleepers with tie plates; reddish granite ballast |
| kalmar-20250715-08.jpg | AleWi, 2025-07-15, CC BY-SA 4.0 | Platform 3 with a train: warning tiles with studs, grey slabs, ribbed guidance strip, lattice portal girder and masts, tall lighting columns, timber sleepers |
| view-of-kalmar-train-station-from-the-castle-2017-07-30.jpg | public domain, 2017-07-30 | Portal spacing and girders seen from across the water |
| kalmar-centralstation-2021.jpg | Axel Pettersson, 2021-09-09, CC BY 4.0 | Platform 1 along the station house (from pass 24) |

The signal plate in the photograph reads "Kac 14" while OSM has "Kas 14"; the OSM ref is kept in the data and no signal ID is lettered in the model.

## Levels

| Level | m | Basis |
|---|---|---|
| Platform top | +0.15 | The station's platform doors (pass 24) |
| Rail top | −0.43 | 0.58 m below the platform, a common Swedish platform height; the photographs show a high platform wall consistent with it |
| Ballast top | −0.66 | Timber sleeper top 4 cm proud of it |
| Island surface | −0.115 | Unchanged district level; the cut meets it with a 1.2 m slope band |

## Geometry and interpretation

`scripts/prepare_rail25.py` (Shapely) writes `source/rail25.json`; `scripts/build_rail25.py` only extrudes it.

- **Bed and cut.** Ballast 1.9 m either side of each centreline; the cut adds a 1.2 m slope band up to the island surface and stops at the platforms and at parking area 90965001. Island surface left as slivers narrower than about 12 m between track beds (423 m², not within 3 m of a building) becomes yard gravel at island level, since a flat district ground between track groups read wrongly in the first Unreal shots. The island surface (`SM_Kvarnholmen_Land`) is re-triangulated around cut and gravel, and the footway layer of street chunk 07_09 is trimmed to the cut with a face down to the island level along the cut edge.
- **Track.** Rails as a 12-point flat-bottom profile (172 mm, head 72 mm) on offset curves at 753.5 mm from the centreline (1435 mm gauge plus half a head), with the head's top face in polished steel. Timber sleepers 2.6 × 0.26 × 0.16 m every 0.6 m with a tie plate under each rail; each sleeper takes its own patch of the wood texture, grain along its length. Turnouts are the crossing rails of the two mapped centrelines; switch blades, frogs and check rails are not modelled. Where the sleepers of two tracks overlap in a turnout, they sit 1.5 mm apart in height.
- **Platforms.** The mapped areas are brought to a uniform edge 1.65 m from the nearest track centre and made disjoint: trimmed where the tracing sits closer, and pulled in where a track-facing edge sits up to 0.9 m further out. OSM traces 2a at about 1.90 m, 2b and 1a at about 1.80 m; the snap adds 82.6 m² of platform. The house platform (ref 1) is added between track 1 and the station house along its length, since OSM maps only a 4 m strip there. From every track-facing edge: 0.25 m edge stone, 0.70 m light warning tiles with studs, 0.60 m grey slabs, a 0.60 m ribbed guidance strip, asphalt beyond, all as photographed on platforms 2b and 3. Tile courses and ribs follow each platform's long axis. Platform walls are light concrete from ballast to platform top.
- **Furniture.** Touching platforms are grouped (the island 2a + 2b + 3, the house side 1 + 1b, and 1a), and each group gets one row of galvanised lighting columns (8.2 m, tapered, slim luminaire) every 22 m down the middle of its widest cross-section. OSM splits the island into halves; a first placement on each half's own axis put lamps and shelters 1–2 m from the edges, in the walkway, which the collision test caught. On the island's centre line, between lamps: two glass shelters on blue columns under a curved roof, a name board "Kalmar C" and a two-faced clock on its own column. Positions are interpreted; only the shelter and clock designs follow the photographs.
- **Signals.** Seven dwarf main signals on the side given by `railway:signal:position`, facing trains arriving in `railway:signal:direction`, 1.35 m from the track centre: a dark body with five lamp positions under visors (red top, the others dark), a yellow rim and identity plate, on a short post and footing.
- **Buffer stops.** A red beam with a white band on two raking struts and a concrete footing at each mapped buffer stop, facing back along its track. The design is generic.
- **Overhead line.** Portals every 45 m on a grid tied to the crossing, wherever track 2 or 3 runs within 16 m of track 1 (seven portals). Each is a box girder of four chords with zigzag lacing, 0.6 × 0.5 m, on square lattice masts, with a drop tube and brown insulator over each electrified track. Cantilever masts (H-section, horizontal arm, diagonal strut, insulators) carry track 1 every 45 m elsewhere. The contact and messenger wires run at 5.5 and 6.8 m above rail top with droppers every 9 m: over track 1 for its whole modelled length, over tracks 2 and 3 between the first and last portal. The OSM data tags only track 1 as electrified; the photographs show wires over the island tracks. The messenger wire is straight between supports, without sag.
- **Level crossing.** Rubber panels 5 mm below rail top between the outermost rails (footway positions 5.08–11.31 m), asphalt ramps beyond them up to the footway surface (+0.015 m) at the cut edge. The ramps are about 20 % steep because they only span the ballast shoulder and slope band; the approach beyond the cut is not lowered. Full barriers as mapped: a post at the top of each ramp with its boom raised and two red lamps facing the path.

Omitted: switch machines and point rodding, cable troughs, balises, signs, the railings along the island's approach to the crossing, departure boards, benches and bins outside the shelters, trains.

## Materials

New `M_Rail25_*` materials tint texture sets towards colours read from the photographs; each tint is computed against the texture's measured mean colour in linear space. Four original texture sets from `scripts/make_rail25_textures.py`, all with a 4 m repeat and OpenGL normals: `T_Rail25Ballast_*` (crushed granite: about 45 mm stones on a wrap-around Voronoi, each with a tint from a grey/pink/rust granite palette and a tilted facet, shadowed voids holding 20 mm fill stones; a first flat-cell version read as crazy paving in close-up and was replaced), `T_Rail25Tactile_*` (ribbed guidance tiles), `T_Rail25Warning_*` (400 mm tiles with studs) and `T_Rail25Timber_*` (weathered creosoted wood with grain and drying checks along u). No reference photograph enters any texture.

## Verification

All reports in `previews/rail25-delivery.json` passed: build (no zero-area or zero-UV triangles; the crafted 3 mm bevel is left off because thin rods collapsed its overlap clamp into 1 184 zero-area faces in the first dry run), FBX vectors, repeatability (identical geometry, UV and material hashes on a second rebuild), 23 materials with normal and roughness maps, Nanite import of seven meshes, render buffers and collision. The collision test (`Unreal/Content/Python/validate_rail25.py`) takes 1 128 floor samples and 1 108 character-sized capsule sweeps: the walking line 1.2 m in from every track-facing platform edge (checked to be at platform height), the crossing along the footway (checked against its ramp profile) and the five named streets within 40 m of the tracks. All 20 obstructions are masts or furniture standing in the walkway, each with a verified detour of at most 2 m on platform ground; five raised samples are the portal masts' base plates. About 161 000 triangles in all.

The Unreal editor must be started with `DEVELOPER_DIR=/Applications/Xcode.app/Contents/Developer`; otherwise it stops at an "Xcode Not Found" dialog. `patch_pass18.py` skips meshes already listed in `previews/rail25-import.json`, so that file is deleted before re-importing changed meshes.

## Licences

Mapped geometry: © OpenStreetMap contributors, ODbL. Commons photographs keep their licences (see `sources.json`) and are not redistributed with the public edition. Authored geometry and textures follow the project licence (CC BY 4.0, code MIT). Only the station name "Kalmar C" is lettered.
