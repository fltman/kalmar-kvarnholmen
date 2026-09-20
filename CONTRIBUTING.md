# Contributing

Contributions in Swedish or English are welcome. Open an issue for a building or area before a large edit, so two people do not unknowingly replace the same binary assets.

## A useful building contribution

1. Identify the building, address and OSM ID if available. Asset names usually include that ID.
2. Explain what is wrong and cite dated references. Distinguish observed details from inferred or measured dimensions. Link research photos instead of uploading material without redistribution rights.
3. Create a branch. Edit a focused generator under `scripts/`, or edit the Blender object directly and describe that choice.
4. Export only the changed meshes. Update their records in `exports/manifest.json` and corresponding Unreal assets when possible. Do not regenerate the whole island to change one doorway.
5. Show before/after views from the same camera, including a close-up and the neighbouring buildings. Check roof intersections, missing faces, normal-map direction, material scale and entrances.
6. Check collision with a player-sized capsule and an actual Play In Editor walk where navigation changed. Record engine/tool versions and the tests you actually ran.
7. Submit a pull request listing changed object names, sources, screenshots, remaining approximations, and validation.

## Repository conventions

- Large binary assets are release downloads, not Git blobs. For asset changes, upload your changed assets to a release in your fork and link it in the PR, with checksums and screenshots. Maintainers review and publish new bundles with `tools/package_assets.py --version vX.Y.Z --output /path/to/release-files`, then update `assets/manifest.json` in Git. Keep code/data changes in the PR; never commit LFS pointers or a huge binary by accident.
- Blender uses metres; Unreal uses centimetres. Export conversion maps Blender `(x,y,z)` to Unreal `(100*x,-100*y,100*z)`. Origin and rotation are recorded in `source/site.json` and `source/storgatan.json`.
- Texture paths in the Blender source must stay relative. Keep normal maps linear; the Unreal import config handles the green-channel convention.
- Do not commit editor caches, autosaves, local backups, credentials, private screenshots or downloaded research photos/PDFs.
- Raw mapped data and derived geographic JSON retain OpenStreetMap attribution and ODbL terms.
- Do not introduce CC BY-SA or other Unreal-incompatible content into the Unreal scene. CC0 and appropriately attributed CC BY assets are preferred; record every external asset in THIRD_PARTY.md.
- Direct edits to a generated `.blend` object can be overwritten by regeneration. Update the generator or clearly document and preserve the manual override.

## Local tools and checks

Opening the supplied scene does not require regeneration. For the Python preprocessing tools, install `requirements.txt` in a virtual environment. Blender scripts run inside Blender; Unreal scripts run inside Unreal with its Python plugin enabled.

```sh
python -m compileall -q scripts Unreal/Content/Python
python tools/validate_repository.py
blender --background --python-exit-code 1 --python scripts/rebuild_pass18.py
```

The last command replaces the objects in the current correction pass and exports them. **Use a branch and save manual work first.** `scripts/build_blender.py` is a full destructive scene regeneration and should only be used intentionally. Older numbered pass scripts describe historical stages and may overwrite later fixes.

In Unreal, `Unreal/Content/Python/patch_pass18.py` imports the changed exports. Its report acts as a checkpoint: remove the local `previews/pass18-import.json` before intentionally reimporting modified assets. `check_pass18.py` validates render buffers, material bindings and collision; `review_hero.py` provides review captures. Test reports are evidence for a particular snapshot, not permanent guarantees.

By contributing original code you offer it under MIT; by contributing original art or documentation you offer it under CC BY 4.0. Keep third-party and OSM licenses intact. State if a contribution contains AI-assisted or inferred details. Do not claim another author's work as your own.
