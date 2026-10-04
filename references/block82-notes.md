# Pass 82: the north side of Kom snart igen and Skeppsbron 13

Pass 82 replaces four generic district volumes from pass 17 (two-storey rendered blocks) with the low boarded houses that stand there. They are split into eight parts.

On the north side of Kom snart igen:

- **91915626 (Kom snart igen 1):** an orange vertical-boarded house on a grey plinth. Its east wall has three round windows, and the south slope of its hipped tile roof carries three red dormers. A dark boarded annex fills the rest of the outline behind it.
- **91915628 (Kom snart igen 5):** a yellow boarded house with three windows under blue awnings, two roof lights and a chimney.
- **91915620 (Kom snart igen 7 / Skeppsbron 11):** a yellow corner house with three parts:
  - the main house, with two doors on stone steps, two red box dormers, a roof light and two chimneys;
  - a lower west part with a window under a green awning;
  - a north wing under a saddle roof.

On Skeppsbron:

- **91915631 (Skeppsbron 13):** a yellow café under a dark saddle roof, with a flat-roofed annex at its south end.

Panoramas are working references only. No pixel is used as a texture.

## Measurement

Four panoramas from April 2025 were used.

| Panorama | Where | Resected position | Camera height |
|---|---|---|---|
| XEsLZaaW-fR0-Kc6vxf6xQ | Kom snart igen 6 | (−9.84, −274.6) | 2.2 m |
| MiXC6Owsr1cZSMy8Dt-naw | Kom snart igen 7 | (19.32, −281.51) | 2.4 m |
| DD0edgVts1ty3E5i3YPoxw | Skeppsbron 11 | not resected | – |
| 5SepBcPoAn4fHGQNcw4L_Q | Skeppsbron 15 | not resected | – |

**Resection.** Each of the two Kom snart igen panoramas was resected on two house corners. The positions they give lie on the street centreline, and 3.4 m and 2.4 m south of the positions Google reports. The heading-62 view of the Kom snart igen 7 panorama puts the house's east corner within 0.3 m of the outline. The Kom snart igen 6 panorama puts the orange house's east wall at 8.0 m, against 8.2 m in OSM.

**Orange house.**
- The eaves are at 3.0 m, and the boarding starts 0.56 m above the ground.
- The hip apex reads 6.66 m, which gives a roof pitch of about 42°.
- The round windows are 1.5, 4.0 and 6.5 m along the east wall, with centres 1.8 m up and about 0.65 m across.

**Kom snart igen 7.** Read on the frontal heading-2 view:
- a door 2.0 m high, on steps 0.6 m high;
- two double windows from 1.5 to 2.8 m;
- the gutter at 3.3 m.

All values are in metres; "s" is the distance along the front.

| Part | Measured | Estimated |
|---|---|---|
| Orange house | eaves 3.0; apex 6.66; round windows at s 1.52, 4.03, 6.50 on the east wall | door and windows on the street front (read at a grazing angle, scaled to the outline, ±0.5 m); dormer positions |
| Yellow house (nr 5) | eaves about 3.0 | window centres at s 3.9, 7.4, 11.1 (grazing view, ±0.5 m); ridge 6.8 |
| Corner house, main part (nr 7) | door s 4.8–5.8; windows s 1.0–2.9 and 6.6–8.6 (scaled 0.95 to the outline); eaves 3.2 | ridge 6.9; dormers at x 20.2 and 24.4; the east window |
| Corner house, west part and north wing | – | heights; west-part window |
| Café and annex | – | all heights and openings (far, oblique views only) |

## Verification

- The zones cover the four outlines: 952.0 m² in all, 0.04 m² not zoned, and no overlap.
- The Blender geometry checks passed.
- Two rebuilds gave identical meshes.
- Passes 28–81 are unchanged.
- Model renders from the resected cameras were compared with the panoramas:
  - The first comparison found a chimney drawn on the facade line, too low a roof on the yellow house, and roof lights under the slope. All three are fixed.
- The Unreal import and its checks are deferred until the models in the area are finished.

## Limitations

- **The street fronts:** the panoramas pass within 4 m of these fronts, so openings away from the cameras were read at grazing angles.
- **Estimates:**
  - the dark annex, the north wing and the café, apart from their outlines;
  - the roofs, apart from the orange house's;
  - the walls not facing the streets, which carry generic windows.
- **Omitted:** signs, awning lettering, heat pumps, meter boxes and the small yellow shed south of the café, which is not in OSM.
