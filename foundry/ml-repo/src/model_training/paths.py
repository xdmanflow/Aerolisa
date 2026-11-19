"""Dataset and model paths for the aerolisa-ml repository (keep in sync with aerolisa_pipelines/paths.py)."""

PROJECT = "/YOUR-SPACE/Aerolisa"  # <-- edit me

GOLD_ENGINE_CYCLE_FEATURES = f"{PROJECT}/gold/engine_cycle_features"
SILVER_CMAPSS_CYCLES = f"{PROJECT}/silver/cmapss_cycles"
GOLD_ENGINE_LIFE_RECORDS = f"{PROJECT}/gold/engine_life_records"

MODEL_ENGINE_HEALTH = f"{PROJECT}/models/engine-health-model"
GOLD_ENGINE_HEALTH_MODEL_METRICS = f"{PROJECT}/gold/engine_health_model_metrics"
GOLD_ENGINE_HEALTH_SNAPSHOT = f"{PROJECT}/gold/engine_health_snapshot"

GOLD_FLEET_AIRCRAFT = f"{PROJECT}/gold/fleet_aircraft"
GOLD_AIRCRAFT_UTILIZATION_DAILY = f"{PROJECT}/gold/aircraft_utilization_daily"
GOLD_ENGINE_ASSIGNMENT = f"{PROJECT}/gold/engine_assignment"
GOLD_INSPECTION_RECOMMENDATION = f"{PROJECT}/gold/inspection_recommendation"
GOLD_RELIABILITY_KM = f"{PROJECT}/gold/reliability_km"

AS_OF = "2026-11-19"  # demo "today"; switch to date.today().isoformat() for a live schedule
