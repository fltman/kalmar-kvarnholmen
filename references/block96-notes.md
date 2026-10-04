# Pass 96: north Proviantgatan, east side, and the west end of Fiskaregatan's south side

Pass 96 replaces five generic district volumes from pass 17 with what stands there. Four of them front the east side of north Proviantgatan (fronts face west); one fronts the south side of Fiskaregatan just east of the corner (front faces north). The L-shaped 90859848 runs round the corner and fronts both streets.

From south to north on Proviantgatan, then east on Fiskaregatan:

- **90859877:** the red boarded house with its gable to Proviantgatan. It is one and a half storeys: eaves 3.9 m on the long sides, three windows in the gable and two windows below (a third, south one is estimated). It has darker red corner boards and bargeboards, white window frames, a grey plinth, a dark tiled saddle roof across the street and a chimney.
- **The gateway (gap 88.8–92.4):** between the red house and the cottage. It has a green double gate between white posts under a white beam, in a white boarded wall 2.3 m high. It stands in the 3.5 m gap between the two outlines and is part of the cottage's mesh.
- **90859878:** the small white boarded cottage with its gable to the street, eaves 1.9 m and ridge 3.55 m. It has one window in a green frame that reaches into the gable, white bargeboards, a tiled roof and a chimney on the north slope.
- **90859832:** the grey rendered two-storey house on a brown base, 1.3 m high. Its street front has four window columns: narrow, double, double, narrow. The windows have white surrounds and brown joinery. It has a white cornice and a low black sheet hipped roof. Its south side, facing the lane, is rendered white with three tall narrow windows on each floor.
- **90859848, west wing:** the ochre rendered two-storey house on the same brown base. It has two window columns on Proviantgatan, two peaked dark-brown dormers and a tiled saddle roof along the street. A white rendered gable stands above the grey house's roof.
- **90859848, north range:** the long ochre range on Fiskaregatan, 43 m, under a tiled saddle roof that is hipped over the corner. It is seen only at its east end, so its windows, chimneys and roof are estimated.
- **90859847:** the long white stucco house on Fiskaregatan.
  - **Ground floor:** rusticated, with eight round-arched windows and the red arched double door with a fanlight in the middle, on two steps.
  - **Upper floor:** nine windows with head mouldings, pilaster strips at the corners and either side of the centre and side bays, a string course and a heavy cornice.
  - **Roof:** two baroque gables over the side bays (concave shoulders, a segmental cap, two arched windows each), three red dormers and a red-brown sheet saddle roof.
  - A small flat-roofed yard annex fills the notch at the south-west corner. It is not seen and is estimated.

Panoramas are working references only. No pixel is used as a texture.

## Which house is which

The brief listed the houses without assigning them. The resection settles it:
- the red boarded house is 90859877;
- the green gate fills the gap between 90859877 and 90859878;
- the white boarded gable cottage is 90859878;
- the grey rendered corner house is 90859832. Its south corner faces the lane to the cottage; it is not on a street corner;
- the ochre house with two dormers is 90859848.

The grey façade seen on the 832 panorama and the grey façade seen on the 848 panorama are the same façade. Both show four columns, with an open window in the second upper one from the north. So the grey rendered two-storey house to the right on the 848 panorama is 90859832 again, not a sixth building.

## Measurement

Four Google Street View panoramas were used, all 696×375 crops with a vertical field of view of 90° and a pitch of 15°. The facade plane is taken 0.355 m outside the OSM line. Each camera was resected by least squares on the vertical edges of house corners, with the pitch held at 15°. Camera heights come from the street at the facade foot.

| Panorama (pano id) | Google position (local) | Resected position, heading | Camera height | Resected on |
|---|---|---|---|---|
| D_MegOfSc-wKLsQsALsJmg (878, h 62) | (184.05, 97.99) | (182.16, 96.58), 64.99 | 2.25 (cottage and red-house bases at −2.25/−2.34/−2.08) | 832's south-west and south-east corners, the cottage's two front corners, the red house's north-west corner. Residual ≤ 6 px, except 13 px at the cottage's south corner. |
| 6U2iN-u9PYRJaifUfV7H3g (832, h 63) | (183.96, 108.49) | (181.92, 105.62), 58.77 | 2.39 | 832's south-west corner and its four window columns at the positions measured on the 848 panorama. Residual ≤ 13 px; the cottage's corners are then off by 10–58 px (see below). |
| 9v-t34-vaXhrcFzgCoJP_A (848, h 63) | (183.82, 118.95) | (181.54, 116.77), 63.4 | 2.29 | the ochre/grey joint (the OSM vertex at y 119.4), 848's chamfer corner (y 129.1) and 832's south-west corner. All three agree to 3 px with a 0.4° heading change. |
| pn4Vz675-fH2GDu7tiUo7w (847, h 150) | (255.80, 141.90) | (254.6, 140.1), 150.86 | 2.24 | 847's two front corners. A free fit gave (254.61, 140.58), but it made the 27.4 m front 29.9 m long, so the camera was moved 0.5 m towards the façade to match the outline's length. |

**The 832 panorama.** Fitted on the grey corner and the cottage alone, it gives (184.1, 104.9), only 4.3 m from the façade. With that camera the grey house's windows land 1.55 times closer together than on the 848 panorama, and the grey façade comes out only 9.6 m long instead of 15.6 m.

The 848 camera is better supported:
- its three corner points agree to 3 px;
- it puts the grey façade's south end on the OSM corner without that corner being used in the fit;
- its windows are symmetric about the façade within 0.8 m.

So the 832 camera was re-resected on the 848 panorama's window positions. The result, (181.92, 105.62), sits like the other three cameras, 1.7–2.3 m west and 2–3 m south of Google's position. With it, the joint downpipe at the left edge falls on the OSM joint. The cottage's corners still miss on this panorama by up to 58 px, so the cottage is measured only on the 878 panorama.

**Measured values.** Heights are above the street at the facade. Positions are local y on Proviantgatan, and u from the middle of the front (positive westwards) on Fiskaregatan.

| Part | Measured | Estimated |
|---|---|---|
| Red house (877) | north-west corner y 88.77 (OSM 88.83); eaves at the corner 3.93; apex 6.4 as read, taken as 6.2 because the bargeboard apex projects; upper (gable) windows 3.21–4.21, spaced about 1.6 m; lower windows 1.05–2.08, about 0.9 m wide; base −2.08 | the gable windows set symmetric about the front (the reading is 0.6 m south of symmetric); the third lower window; depth, roof and chimney from the outline |
| Gateway | gate opening about y 89.6–91.9; gate leaves 2.0 high, beam 2.3–2.45 | gate wall in the OSM front line |
| Cottage (878) | front y 92.7–98.8 (5.9–6.1 m; OSM 6.03); eaves 1.85–1.89 (taken as 1.9); apex 3.55; window 0.8–2.08 high and 1.1 m wide, centre y 95.8 | window centred on the front (y 95.4); chimney position from the 832 panorama |
| Grey house (832) | base top 1.24–1.36; lower windows 2.07–3.53; upper windows 4.95–6.41; cornice 6.75–7.16 (taken as 6.85); gutter 7.41; columns at s 3.76, 6.76, 11.1 and 14.08 from the south corner; south side: three tall windows per floor at x 192.2–194.6 | window widths (0.95 narrow and 1.75 double; the two panoramas disagree); roof pitch (15°, the roof is not visible from the street); the south windows' heights (grazing view) |
| Ochre wing (848 west) | joint y 119.84 (OSM 119.76); north end y 129.0–129.5 (chamfer 129.1); base top 1.41; lower windows 2.14–3.59; upper windows 4.83–6.27; cornice 7.04, gutter 7.38; window columns y 122.6 and 125.6; dormer windows 7.72–8.77, dormer tops about 9.8 | ridge 11.8 (41°, chosen so that the tiles show above the cornice as on the photo); dormer setback and size; the white south gable; the corner hip |
| Ochre north range (848) | east end ochre, eaves near 7.0, tile roof (backlit) on the 847 panorama | everything else: generic windows on two floors, ridge 11.65, two chimneys |
| White house (847) | front length scaled to the outline (0.942); plinth to 0.34; arched windows 1.22 to an arch top of 2.97, 1.35 wide; door arch top 3.03, centred; string course about 3.7; upper windows 4.48–6.36, 1.15 wide; cornice bottom 7.81, top 8.15 (eaves taken as 7.85); columns at u ±3.18, ±5.48, ±7.82, ±11.13 (symmetric to 0.1 m); pilasters ±1.85, ±9.4; baroque gables centred ±5.6, 4.1 m wide, top about 12.4; red dormers at u 0 and ±10.9 | gable shape (concave shoulders, segmental cap), dormer setback and size (the photo is against the sun), the cornice's projection, roof ridge 11.2 and material, the notch annex |

## Verification

- **Zone checks** (`previews/block96-zones.json`): footprint 1155.9 m², zoned 1156.0 m², 0.09 m² outside OSM, 0.01 m² not zoned, overlap 0.002 m². The prepare script prints `BLOCK96_ZONES_OK`.
- **Sandbox (prelude: pass 95), four iterations.**
  - Each run rendered the four resected views at 696×375 and two aerials. The renders were compared side by side with the photos and, for the 878 and 847 views, as edge overlays.
  - **Run 1:** placement was good on all four views. On the 847 view, the door, the arched and upper windows and the gables' outlines land within about 5–10 px. The run showed loose dormer roofs (a missing angle argument), a cornice that projected too far and stood too high, and a ridge on the red house that was slightly high.
  - **Runs 2–3:** fixed those. They lowered 847's eaves to 7.85 and shortened its cornice; moved the red dormers forward so they show over the cornice as on the photo; enlarged the ochre dormers and steepened the ochre roof; and lowered the red house's ridge to 6.2.
  - **Run 3** was killed when the machine ran out of memory, after its four street views were saved.
  - **Run 4** repeated it in full: it printed `BLOCK96_GEOMETRY 5` and `SANDBOX_DONE prelude 95` with no errors. The comparisons are `SCR/p96/cmp4.png` (photo left, render right) and the aerials `SCR/p96/aer4cmp.png`; the aerials show the ochre L with its hipped corner and the 847 roof, gables and dormers.
- **`drop_degenerate_faces96`** is called right after `s21_finish` in `b96_finish`, with the `_thin` test. In the sandbox it removed 8 (877), 8 (878), 0 (832), 35 (848) and 264 (847) faces. The sample centres lie on gable rakes, roof edges and the arched openings' heads, which are where the bevel collapses slivers.
- **Pending:** the official build, the Blender geometry checks and the Unreal checks. The lead fills in their results.

## Limitations

- **Two panoramas disagree on the 832 camera** (see Measurement). The model follows the OSM outline and the 848 panorama. Grey window widths are a compromise between the two panoramas.
- **Red house front** is cut off at the right edge of the only view, so its south lower window is estimated. The measured windows sit about 0.6 m south of symmetric; they are modelled symmetric.
- **Not seen:**
  - 848's north range on Fiskaregatan, apart from its east end;
  - the chamfered corner, apart from a dark railing at the edge of the 848 panorama;
  - all yard and back walls, which carry generic windows;
  - 847's yard annex;
  - the roofs of 832 and 847, which are not visible from the street.
- **Omitted:** signs, the parking sign, lamp posts, bushes, electricity cabinets, downpipes, the TV aerial, the railing at the chamfer, and the cars.
- **Extra views that would help:**
  - 848's north range: from (215.0, 140.0), heading 152, pitch 15;
  - the corner and chamfer: from (184.0, 137.0), heading 107, pitch 15;
  - the red house's whole front: from (182.5, 86.0), heading 62, pitch 10.

## Official build

The lead's build of pass 96 passed the Blender geometry checks, two rebuilds gave identical meshes, and passes 28–95 are unchanged. The Unreal import and its checks are deferred.
