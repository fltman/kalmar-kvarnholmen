# Pass 15 — surface polish and completion of remaining facades

This pass completes the 267 objects still categorized as building massing after pass 14. Footprints, courtyards, original roof topology, height assumptions and mapped passages are retained. Exposed wall intervals are computed against neighboring footprints. Individual facade styles, window counts, doors and trim for these buildings are inferred, not photographic reconstructions. Party walls remain solid where neighboring buildings meet. Each completed object stores this provenance.

The previously researched landmarks retain their shapes and receive small edge bevels and improved surfaces. New material recipes use the physical dimensions supplied by Poly Haven, with modest color adjustments for plaster and buff brick. The rubble material is enlarged to a 2.8 m tile for the fortification masonry; this is an artistic material choice, not a masonry survey.

## Material sources

All downloaded material maps are CC0 assets: https://polyhaven.com/license . Original files, metadata, download URLs and MD5 verification are under `references/polyhaven15/`. These are generic surface scans, not photos of the Kalmar buildings.

- Stone wall: https://polyhaven.com/a/stone_wall
- Dressed stone: https://polyhaven.com/a/stone_wall_02
- Red brick: https://polyhaven.com/a/brick_wall_001
- Buff brick: https://polyhaven.com/a/brick_wall_003
- Plaster: https://polyhaven.com/a/plastered_wall_02
- Clay roof tiles: https://polyhaven.com/a/clay_roof_tiles_02
- Street setts: https://polyhaven.com/a/cobblestone_floor_08
- Grass surface: https://polyhaven.com/a/sparse_grass
- Bridge timber: https://polyhaven.com/a/wood_planks_grey
- Asphalt: https://polyhaven.com/a/asphalt_02

Base color, OpenGL normal, roughness and AO maps are 2K. Sixteen-bit scalar source maps are scaled to eight-bit rather than clipped, and the working normal maps are renormalized after resampling. Texture-sample inputs use the actual UE 5.8 UVs pin; connections in the added material graph are checked. Unreal flips the normal green channel for its tangent convention; color maps are sRGB and data maps linear. World-space macro variation and a restrained low-level dampening mask reduce uniformity without painting directional light into the base color. Water normals use a deterministic sum of differently oriented periodic waves instead of straight, identical ripple bands.

## Limits

This is a broad environment art pass. It is not a claim that 267 individual facades have been verified against Street View, that the district is survey accurate, or that it now meets a finished AAA production standard. Individual shopfronts, landmark ornament, planting and Ravelinen Prins Carl remain future work. The original church lighting and authored interiors are preserved.
