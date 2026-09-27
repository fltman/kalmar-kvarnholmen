# Pass 54: the classical building at the east end of Ölandsgatan

Pass 54 details the district volume 91285838 on the south side of Ölandsgatan, at its east end (Ölandsgatan 32–41 in Street View's labels). It is a classical two-storey building.

**The front** is symmetrical, in three parts:
- wings of three axes;
- two risalits projecting 0.35 m under pediments, each with a round-headed niche over its upper window (the west risalit holds a door up steps, the east one an arched window);
- a centre of three axes under a set-back attic with its own pediment.

**The details:**
- round-headed ground-floor windows on a granite plinth;
- a string course, and upper casements under small cornices;
- a main cornice at 9.2 m;
- a low hipped sheet roof with two small pedimented dormers;
- the east wing's door.

**The annex:** a one-storey wing with a large and a small arched window, and a rounded east end.

The Skeppsbrogatan side stays plain. The mesh keeps its name (`SM_Kvarnholmen_House_91285838`).

Panoramas are working references only. No pixel is used as a texture, and no panorama, depth or tile data was extracted.

## Sources

- **Outline:** `source/block54.json`, two zones. The main block runs to the annex joint (x 141.3); the annex takes the rounded end.
- **Google Street View**, April 2025, 90° vertical field of view, pitched 10° up (1372 × 871 frames): three panoramas on Ölandsgatan, facing the building. The review cameras are 308 (west), 309 (centre) and 310 (east); 311 is an aerial view.

## Measurement

**Registration.** The cameras are chained on eight shared edges (the risalits, the centre and east wing windows), anchored on the west corner (x 105.56) and spaced as their GPS positions. The middle panorama's facade foot is hidden by the steps, so its distance was solved from the shared edges.

Pairs agree within 0.43 m. The camera height comes out at 2.62 m, and the cameras stand 7.9–9.3 m out.

| Feature | Measured (m) | Modelled (m) |
|---|---|---|
| Axes | west wing 108.0 / 110.75 / 113.5; west risalit 115.15–119.5; centre 120.95 / 123.6 / 126.14; east risalit 127.9–132.25; east wing 133.3 / 136.15 / 138.97; annex joint 141.3 | the same |
| Heights | plinth 0.45–0.49; ground arches 1.38–3.4; string course 4.26–4.75; upper windows 4.85–7.08 (west) / 5.17–7.51 (east); main cornice 8.38–9.08 (west) / 9.12–9.58 (east); pediment apex 11.52 | the averages; pediments to 11.55 |
| Annex | large arched window x 146.1–148.95, 0.8–3.37; small x 142.9–144.4, 1.29–3.37; cornice 4.49–5.17 | the same, eaves 5.2 |

## Verification

See `previews/block54-delivery.json`:
- every report passed;
- 76,368 triangles in one mesh;
- identical on two rebuilds;
- 117 floor samples and 110 capsule sweeps, no obstructions;
- calibration of 17 features: median 8 px, largest 20 px (the east risalit);
- passes 28–53 unchanged.

## Limitations

- **Estimates:**
  - the attic's height, and the roof and dormers;
  - the Skeppsbrogatan side;
  - the annex's rounded end.
- **The risalit niches and mouldings** are simplified to a band and a rounded moulding.
- **Omitted:** the signs, the railings, the bicycle stands and the heat pump.
