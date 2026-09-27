# Pass 47: the north side of Ölandsgatan, opposite pass 46

Pass 47 details two district volumes on the north side of Ölandsgatan:

- **The cream two-storey house** (92379306):
  - a banded ground floor on a salmon plinth, with five brown casements in plain surrounds;
  - a band and five upper casements;
  - the eaves and a tile roof with two dormers.
- **The narrow white wooden house** (number 13, in 92379253): vertical boarding, a white garage door, one upper window.
- **The white stone house** (in 92379253):
  - four axes of white casements in flat surrounds with aprons, on both storeys;
  - a band, and a grey plinth with cellar lights;
  - a sheet roof with a terrace railing.

The rear wing stays plain. The meshes keep their names (`SM_Kvarnholmen_House_92379306`, `…_92379253`). Panoramas are working references only; no pixel is used as a texture.

## Measurement

**Registration.** Two panoramas of pass 46 ("7 Ölandsgatan", heading 332°) are chained:
- six shared window and garage edges;
- the joint between the cream house and the wooden house (x -129.2).

The pairs agree within 0.16 m. The cameras stand 5.4 and 5.8 m from the facade, 2.1 m high.

| Feature | Measured (m) | Modelled (m) |
|---|---|---|
| Cream house | ground windows 1.24-2.89 (surrounds); band 3.41-3.55; upper 4.01-5.6; plinth 0.82; eaves 6.53; dormers over x -134.5 and -131.7 | the same |
| Wooden house | garage x -128.9 to -127.06, 0.2-2.95; upper window 4.16-5.79 | the same |
| Stone house | ground windows 1.71-3.09; upper 4.17-5.88; band about 3.5-4.0; plinth 0.98; eaves 6.4-6.7 | the same, eaves 6.6 |

## Verification

See `previews/block47-delivery.json`:
- every report passed;
- 50,358 triangles in two meshes;
- 58 floor samples and 51 capsule sweeps;
- calibration of 12 features: median 8 px, largest 30 px (the cream house's roof);
- passes 28-46 unchanged.

## Limitations

- **The cream house's roof** shows more above the eaves in the panorama than in the model; its pitch and the dormers are estimates.
- **The green wooden house** east of the stone house (with the arched gate) is outside these two volumes and is not changed.
- **Omitted:** the house number plates and the lamp post.
