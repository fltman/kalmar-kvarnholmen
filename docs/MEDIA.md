# Building photographs and flythroughs

The media export shows the public Unreal scene after refinement pass 22. Its target is a searchable offline gallery with one photograph per building record, plus two silent H.264 films. Completion is recorded separately for each render in `media/*-frames/render-status.json`; preparing the assets does not mean that the export has finished.

| Output | Coverage | Format |
| --- | --- | --- |
| House gallery | 338 mapped building records and five separately grouped landmarks | 343 lossless PNG originals, 1920 × 1080; JPEG viewing copies |
| Street flythrough | Stortorget, Storgatan, Larmgatan, Norra Långgatan, Kaggensgatan, Fiskaregatan | 84 seconds, 1920 × 1080, 24 fps |
| Cathedral flythrough | Central aisle, altar, pulpit, organ gallery and vaults | 44 seconds, 1920 × 1080, 24 fps |

All three exports use Movie Render Queue, Cinematic scalability, 64 spatial samples, full-resolution textures, LOD 0, high-quality shadows and lossless PNG intermediates. The deferred renderer uses the project's Lumen lighting. This is not a path-traced render. Films use H.264 CRF 14 with the veryslow encoder preset; the original frames remain available locally.

A mapped building record can contain several connected wings. The gallery follows the project's mesh inventory rather than claiming 343 separately surveyed historical buildings. Tight courtyards and large buildings sometimes need an elevated camera. The models remain a work in progress; images are renders of the reconstruction, not reference photographs.

## Reproduce

Use the public assets pinned by `assets/manifest.json`, Unreal Engine 5.8 with the Python, Sequencer Scripting and Movie Render Queue plugins, Python 3 with Pillow, and FFmpeg. Close the editor before running the standalone export to avoid duplicating the city's memory footprint. Allow substantial rendering time and disk space.

1. Generate flight paths with `python3 scripts/plan_media_routes.py`.
2. In the editor, run `media_plan_houses.py`, `media_repair_views.py`, and `media_validate_routes.py` from `Unreal/Content/Python`. Read the reports under `media/` before rendering. Camera selection uses mapped footprints and visibility traces, with reviewed overrides in `source/media_camera_overrides.json`. It still requires visual review.
3. Optionally run `media_capture_houses.py` for quick 1600 × 1000 framing previews. These are not the final high-quality exports. Correct camera records before building the final still sequence.
4. Run `media_build_films.py`, `media_build_hq_presets.py`, and `media_build_hq_houses.py` in that order. They create editable Level Sequences and saved Movie Render Queue presets. They refuse to overwrite existing assets; deliberately rename or remove obsolete export assets before rebuilding. The house script saves the export assets. Save the map and close the editor before the next step.
5. Run `python3 scripts/render_houses_hq.py --probe` for a high-resolution still, or `python3 scripts/render_media_hq.py hq-probe` for eight film frames. Review the results. Then run `python3 scripts/export_media.py` for houses, streets and cathedral sequentially, followed by frame verification, film encoding and gallery creation. For raw rendering only, use `python3 scripts/render_houses_hq.py`, then `python3 scripts/render_media_hq.py street` and `python3 scripts/render_media_hq.py church`. Set `UNREAL_EDITOR` or pass `--engine` if the engine executable is elsewhere. On macOS, prefix the command with `caffeinate -i` to prevent sleep during the export. The house runner starts a fresh Unreal process for each building to release graphics allocations between cameras, keeping the quality settings unchanged. It resumes from successfully verified house frames. Existing unverified frames are never silently overwritten; inspect and move incomplete attempts aside before resuming. Film renders require a fresh output folder.
6. The complete export runner performs this step automatically. For a manual workflow, after successful completion reports, run `python3 scripts/encode_media_films.py`, then `python3 scripts/build_media_gallery.py`. The gallery builder verifies full-resolution originals and links or copies them into `../Kvarnholmen-media/original/`. Open `../Kvarnholmen-media/index.html` directly in a browser; no server or internet access is required.

The standalone runners write `media/hq-progress.json` and per-job logs. Open `../Kvarnholmen-media/export-status.html` to see frame counts without a server; its timestamp indicates whether the exporter is still updating. It checks frame counts and pipeline completion, and stops before exhausting disk space. A process exit alone is not treated as a successful render. Video encoding verifies resolution, frame count, duration and complete decoding.

`media_controller.py` is an optional local dispatcher for an already-open editor. Start it once, then write `{"execute":"media_capture_houses.py"}` (or another export script filename) to `media/request.json`. It only accepts a script in the project's Python directory. The dispatcher is intended for a trusted local project and has no network listener.

`media_contact_sheet.py` creates labelled QA sheets from original PNGs. Route validation uses sphere traces through the actual Unreal world. Validation checks camera clearance, not historical accuracy or every visual obstruction. Generated media, local logs and temporary QA files are ignored by Git.

## Reuse and attribution

Original render work: **Kalmar Kvarnholmen by Anders Bjarby and contributors, CC BY 4.0**. Geographic data: **© OpenStreetMap contributors, ODbL 1.0**. See [LICENSE](../LICENSE) and [THIRD_PARTY.md](../THIRD_PARTY.md) for material and engine asset terms. The films have no music or narration.
