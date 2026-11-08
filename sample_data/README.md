# Sample data

Tiny files so tests, CI and the public demo run offline. Every file < 1 MB.

| File | Content | Origin |
|---|---|---|
| `cmapss/train_FD001_sample.txt` | A few units, truncated | Slice of the public NASA dataset |
| `airports_sample.csv` | ~20 airports | OurAirports (public domain) |
| `aircraft_registry_sample.csv` | A handful of **fictional** airframes | Synthetic |
| `flights_sample.csv` | A few weeks of flights for those airframes | **Synthetic** (OpenSky data is never committed) |

Create them with a script in `src/aerolisa/pipelines/` (e.g. `make_samples`), seeded, so they can be regenerated.
