# Pass 87: the north side of the east end of Södra Långgatan

Pass 87 replaces four generic district volumes from pass 17 (two-storey rendered blocks with hipped roofs) with the houses that stand on the north side of the east end of Södra Långgatan. They are split into eight zones.

- **91928581 (Södra Långgatan 63):** a pale green rendered house with stone-grey window surrounds. It has two parts:
  - a three-storey main house with a lesene at its west end;
  - a two-storey west bay, 3.9 m wide, with a deep boxed cornice.
- **91928560 (Södra Långgatan 67):** a three-storey front on a grey, horizontally grooved ground floor. It has three parts:
  - a cream west part with an arched gateway behind an iron gate and a two-storey box bay that runs up to the eaves;
  - a pink east part with its own two-storey bay and a white garage door;
  - a rear wing on the outline's northern arm.
- **91928553 (Södra Långgatan 69):** an ochre roughcast front with smooth ochre lesenes at both corners and in the middle, a frieze under the eaves, a dark stone plinth, dark red frames and round-headed windows on the middle floor. A lower flat-roofed rear part fills the rest of the outline.
- **91928566:** an ochre roughcast house with a gambrel gable to the street, two attic windows and a round window in the gable, dark red frames and a grey plinth. The mesh also carries the two iron gates under small green canopies on both sides of the house, one towards no. 69 and one towards the house to the east.

Panoramas are working references only. No pixel is used as a texture.

## Measurement

Four panoramas from 2025 were used, six views in all (heading 332 at pitch 10 or 25, plus heading 302 and heading 2 at pitch 35; vfov 90, 726×420).

| Panorama | Where | Google position (local) | Resected / adopted position | Camera height |
|---|---|---|---|---|
| Urnc1M7qw_-g5JUlBC-t3Q | outside no. 63 | (207.0, −73.8) | (204.1, −76.0) | 2.4 m (assumed) |
| 01fOmpeeH6JkFcM9Ff5jew | outside no. 67 | (227.7, −74.2) | (223.6, −76.85) | 2.4 m (assumed) |
| r8j5MM8cuFiRoH_81Ksb8w | outside no. 69 | (248.1, −75.2) | (245.85, −78.56), resected | 2.4 m (assumed) |
| sud29RNebWyga1aV23dz2Q | outside 91928566 | (258.2, −75.7) | (256.28, −77.67), resected | 2.4 m (assumed) |

**Resection.**
- **No. 69 and 91928566:** each was resected on the two street corners of its house (OSM vertices), read at the plinth. Both positions lie 2–3.4 m south and 1.9–2.2 m west of Google's.
- **Nos. 63 and 67:** only one known corner is in view for each, so each position is a bearing line fixed by an assumed camera height of 2.4 m:
  - for no. 63, the west corner of the green house at (201.0, −71.88) and the wall base;
  - for no. 67, the pink/ochre joint at (239.54, −72.9) and the wall base.

  The resulting offsets from Google agree with the two full resections. A 0.3 m error in height moves these two positions about 0.4 m along the street.
- **Cross-check:** the downpipe at the cream/pink joint of no. 67 reads s 10.4 on the heading-332 view and s 11.1 on the heading-2 view, which gives a ±0.4 m spread along that front.
- **Grazing reads:** the far end of no. 67 (s > 15) is read at a grazing angle on the heading-2 view and comes out about 1.5 m short of the outline. The pink bay and the garage door are placed by eye against the outline's east end.

Heights are read on the facade plane with `hit.py`. All values are in metres; "s" is the distance along the front from its west corner.

| House | Measured | Estimated |
|---|---|---|
| 63 | west bay 3.9 wide (lesene s 3.55–3.88); window columns s 2.05, 5.6, 9.2; rows 1.55–3.05, 4.15–5.6, 6.5–7.8 (main part only); plinth 0.92; west-bay cornice underside 6.1–6.2, top about 7.0–7.5; main eaves about 8.8–9.0 | the column at s 12.8 and the east end (out of view); no door modelled; both roofs (pitch, ridge 12.2 and 7.9, grey sheet covering) |
| 67 | gateway s 0.35–2.65, top about 2.9; ground windows s 3.9–5.7, 8.2–9.25, 11.5–13.5, rows 1.65–2.95; grey ground floor to 3.05–3.1; cream bay about s 3.0–6.1, underside 3.25; upper rows 4.3–5.8 and 6.9–8.3; lesenes s 6.9 and 14.35; cream/pink joint s 10.4–11.1; eaves about 9.4–9.7 | pink bay s 15.0–18.4 and its top (8.9); the east window column s 20.6; garage door s 19.8–22.6; ground window under the pink bay; bay depths 0.8; roof ridge 13.0; the rear wing (6.4 eaves, hipped) |
| 69 | lesenes s 0–0.46, 3.9–4.7, 8.2–9.1; window centres s 2.5 and 6.75; rows 1.95–3.15, arched 3.7–4.85 (spring 4.45), 6.65–7.45; stone plinth 0.75; eaves soffit 8.9 | the low hipped roof (ridge 10.6), unseen above the eaves; rear part 6.4 with a flat roof |
| 91928566 | front 9.64 between the corners (resection); window centres s 2.0, 5.3, 7.9; rows 1.65–3.05, 4.3–5.75; attic windows 7.0–8.4 at s about 3.1 and 6.6; round window centre 9.65 at s 4.8; gambrel knee about 8.8 at 0.8–1.0 in from the walls; apex 11.8; eave tip about 6.35; plinth 0.8 | wall eaves 6.8; the rear gable (mirrored); side windows; chimney positions; gate and canopy heights (2.2 and 2.75) |

The arched middle-floor windows of no. 69 sit only about 0.55 m above the tops of the ground-floor windows. That is how the panorama reads, and the view from no. 67 shows the same close spacing, so it is kept.

## Verification

- **Zones:** `scripts/prepare_block87.py` prints `BLOCK87_ZONES_OK`. The zones cover the four outlines, 874.2 m² in all, with 0.0 m² outside OSM, 0.0 m² not zoned and no overlap.
- **Sandbox:** two sandbox runs (`SCR/sandbox.py` on a copy of `Stortorget.blend`) printed `BLOCK87_GEOMETRY 4` and `SANDBOX_DONE` with no errors.
- **Panorama comparison:** the six views were rendered from the adopted cameras at the photos' size and compared side by side (`SCR/p87/sb1/cmp1–3.jpg`).
  - Plinths, window rows, lesenes, the grey ground floor and the eave lines of all four houses fall within a few pixels to about 20 px of the photos.
  - The gambrel profile and round window of 91928566 match closely.
  - The cream bay of no. 67 and the arched gateway sit where the photo shows them.
  - Two aerial renders show the roofs closed, with no gaps between the zones.
- **Pending:** the official build, the Blender geometry checks and the Unreal import and checks. The lead fills in the build results.

## Limitations

- **Camera positions:** the positions for nos. 63 and 67 depend on an assumed camera height. Positions along those fronts are good to about ±0.5 m.
- **Out of view or estimated:**
  - the east end of no. 63, which may carry its entrance;
  - the east third of no. 67's front;
  - all roofs: coverings, pitches and ridges. The steep street views show only the eaves.
  - all rear and side walls (generic windows);
  - the rear wing of no. 67 and the rear part of no. 69.
- **Simplified:** the bays are rectangular boxes; the photo suggests the pink bay may have canted sides.
- **Omitted:**
  - downpipes, vents, the meter cabinet, street lamps and the "Utfart" sign;
  - house numbers;
  - the climbing plants behind the gates;
  - the yellow boarded shed and fence between no. 63 and the house to its west, which is not in this pass's scope.

## Official build

The lead's build of pass 87 passed the Blender geometry checks, two rebuilds gave identical meshes, and passes 28–86 are unchanged. The Unreal import and its checks are deferred.
