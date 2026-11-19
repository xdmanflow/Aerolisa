"""Every dataset path of the Foundry edition, in one place.

Change PROJECT once to the folder you created in your Foundry space (build guide step 1).
The names after PROJECT are identical to the local twin (``python -m aerolisa.cli catalog``).
"""

PROJECT = "/YOUR-SPACE/Aerolisa"  # <-- edit me (e.g. "/Manil Doudou/Aerolisa")

# raw: files uploaded as-is (Data Connection upload, build guide step 2)
RAW_CMAPSS_FILES = f"{PROJECT}/raw/cmapss_files"

# bronze -> silver -> gold (this repository, PySpark)
BRONZE_CMAPSS_RAW = f"{PROJECT}/bronze/cmapss_raw"
BRONZE_CMAPSS_RUL = f"{PROJECT}/bronze/cmapss_rul"
SILVER_CMAPSS_CYCLES = f"{PROJECT}/silver/cmapss_cycles"
GOLD_ENGINE_CYCLE_FEATURES = f"{PROJECT}/gold/engine_cycle_features"
GOLD_ENGINE_LIFE_RECORDS = f"{PROJECT}/gold/engine_life_records"

# produced by the aerolisa-ml repository (model training template)
GOLD_FLEET_AIRCRAFT = f"{PROJECT}/gold/fleet_aircraft"
GOLD_AIRCRAFT_UTILIZATION_DAILY = f"{PROJECT}/gold/aircraft_utilization_daily"
GOLD_ENGINE_ASSIGNMENT = f"{PROJECT}/gold/engine_assignment"
GOLD_ENGINE_HEALTH_SNAPSHOT = f"{PROJECT}/gold/engine_health_snapshot"
GOLD_INSPECTION_RECOMMENDATION = f"{PROJECT}/gold/inspection_recommendation"

# ontology backing datasets (this repository, PySpark joins)
OBJECTS_ENGINE = f"{PROJECT}/objects/engine"
OBJECTS_AIRCRAFT = f"{PROJECT}/objects/aircraft"
OBJECTS_OPERATOR = f"{PROJECT}/objects/operator"
WRITEBACK_WORK_ORDERS = f"{PROJECT}/writeback/work_orders"

# optional real-data source (build guide step 14)
BRONZE_OPENSKY_FLIGHTS = f"{PROJECT}/bronze/opensky_flights"
