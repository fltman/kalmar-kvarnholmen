# Pass 83: the warehouse row between Kom snart igen and Skeppsbron

Pass 83 replaces two generic district volumes from pass 17 with the old warehouse row. 91915622 is Kom snart igen 2. 91915624 is the row Kom snart igen 8–10 / Skeppsbron 3–9.

The row is split into nine parts:
- **The white boarded warehouse at the west end** (91915622). It has a large and a small frontispiece on the street, two on Skeppsbron, and a low metal roof.
- **Three boarded two-storey warehouses**, cream, pale cream and pale green, each about 19 m long. Each has:
  - two frontispieces on each long front, about a quarter of the length in from the ends, with deep roofs and bargeboards;
  - tall upper windows in brown frames;
  - diamond windows;
  - carriage gates under the frontispieces, and doors and a shop window below;
  - a boarded frieze with a fretted edge under the eaves.
- **The white rendered house at the east end** (Skeppsbron 9/11 side), with two small frontispieces and regular windows.
- **The three links between them**, taken as the necks between the notches in the OSM outline:
  - a boarded link;
  - the middle link, a low lean-to on Kom snart igen and a glazed two-storey front on Skeppsbron;
  - the white link with two garage doors and a black box dormer.

Panoramas are working references only. No pixel is used as a texture.

## Measurement

The green warehouse's street front was measured from the resected panorama MiXC6Owsr1cZSMy8Dt-naw, at (19.32, −281.51) with the camera 2.4 m high. All values are in metres.

| Feature | Measured |
|---|---|
| Eaves | 6.9–7.0 |
| Frontispiece apex | about 9.5 |
| Upper windows | 1.0 wide, from 3.7 to 5.6 |
| Doors and gates | 2.1–2.2 high, from about 0.6 |
| Diamond windows | centred about 4.7 up |
| Frontispiece centres | about 5 and 14 m from the east end (0.25 and 0.72 of the length) |

The far end of this front reads up to 13 % high, as distances along a facade seen at a grazing angle do. The near readings are taken.

The other boarded fronts are drawn to the same pattern, which all the panoramas show: two frontispieces a quarter in, gates under them, doors near the ends. Their exact opening positions are not measured. Heights for the west warehouse (eaves 6.6), the rendered house (eaves 7.0) and the links are estimates from the same views.

## Verification

- The zones cover the two outlines: 1175.0 m², 0.12 m² not zoned, and 0.04 m² overlap at the link cuts.
- The Blender geometry checks passed.
- Two rebuilds gave identical meshes.
- Passes 28–82 are unchanged.
- Model renders were compared with six panorama views on both streets:
  - The first comparison found the frieze and a storey band drawn too dark. Both are fixed.
- The Unreal import and its checks are deferred until the models in the area are finished.

## Limitations

- **Pattern, not measurement:** the opening positions on all fronts except the green warehouse's street front.
- **Estimates:**
  - the link heights;
  - the roof pitches;
  - the Skeppsbron panorama positions, used only for comparison.
- **Omitted:** the spiral stair at the west warehouse, signs, awnings, lamps and heat pumps.
