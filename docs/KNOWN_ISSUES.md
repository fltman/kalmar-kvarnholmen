# Known limitations and useful next contributions

- Most background facades are inferred from footprints and broad height estimates. Having windows on every mesh is not the same as faithfully reconstructing every real building.
- Heights and small carvings are generally estimated. Sculpture details are stylised, not scans.
- Västerport's exterior has reference-based detailing, but its tunnel still simplifies the real bent passage.
- Parking polygons are mapped; painted bays are schematic 2.5 × 5 m cells with 6 m aisles, not an inventory of real markings or parking rules. Grass surfaces need more vegetation and edge treatment.
- The cathedral's public-edition altar canvas is neutral: the earlier photo is excluded for license compatibility. A compatible photograph or original historically supported reconstruction is welcome.
- Shop signs are approximate and may depict older photographed appearances. No current business inventory is implied.
- Lumen / Nanite are enabled, but the scene is not performance-optimised or packaged. A previous broad district editor capture was about 15 FPS on the development machine; this is not a target performance claim.
- Only the recorded macOS authoring environment has been tested. Windows/Linux testing, portable launchers and a reproducible end-to-end regeneration workflow are useful contributions.
- Large binary files live in versioned GitHub release bundles and are difficult to merge. Coordinate edits to the shared Blender file and Unreal map; share changed assets through a fork release linked from your PR.
- Passes 23–25 (Baronen, the Kalmar C station house, the station's tracks and platforms) are applied by their scoped rebuild scripts on top of the released scene; `scripts/build_kvarnholmen.py` alone does not reproduce them. Railway turnouts have no switch blades, frogs or point machines, and the overhead messenger wire has no sag.
