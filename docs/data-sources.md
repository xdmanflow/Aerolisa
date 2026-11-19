# Data sources

| Source | Used for | Status | Terms |
|---|---|---|---|
| NASA C-MAPSS turbofan degradation simulation, FD001 (Saxena et al., 2008) | engine health, research | ✅ in `data/raw/cmapss/` | public NASA dataset |
| Simulated fleet (`aerolisa.fleet.simulate`, seed 42) | aircraft, utilisation, engine assignment | ✅ generated, `simulated = true` everywhere | own |
| OpenSky Network (flights by aircraft) | real cycles per airframe (optional step 16) | 📐 connector written | non-commercial research terms; raw data never republished |
| C-MAPSS FD002–FD004, N-CMAPSS | multi-condition / realistic flights (next) | 📐 | public NASA datasets |
| Others per use case | see [use-cases.md](use-cases.md) | 📐 | checked per source before use |

## FD001 files (committed)
| File | Rows | Content |
|---|---|---|
| `train_FD001.txt` | 20,631 | 100 engines run to failure (lifetimes 128–362 cycles, mean 206.3) |
| `test_FD001.txt` | 13,096 | 100 engines truncated before failure |
| `RUL_FD001.txt` | 100 | true RUL at the truncation point |

Columns: unit, cycle, 3 operational settings, 21 sensors (meaning in `src/aerolisa/core/schema.py`).

## Simulation disclaimer (shown in every app)
Engines are NASA C-MAPSS simulations assigned to a simulated A320-family fleet with fictitious registrations.
Their health has no relation to any real aircraft or engine.
