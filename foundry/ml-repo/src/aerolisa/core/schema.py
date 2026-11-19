"""Schema constants shared by the local twin and the Foundry edition.

Keep these names identical to the Foundry dataset columns and ontology property
API names: an interviewer should be able to compare both editions line by line.
"""

from __future__ import annotations

# --- C-MAPSS raw layout ------------------------------------------------------
OP_SETTINGS: list[str] = ["op1", "op2", "op3"]
SENSORS: list[str] = [f"sensor_{i}" for i in range(1, 22)]
RAW_COLUMNS: list[str] = ["unit", "cycle", *OP_SETTINGS, *SENSORS]

# Near-constant under FD001's single operating condition (SAA v1, section 3.2.1).
DROPPED_SENSORS: list[str] = ["sensor_1", "sensor_5", "sensor_10", "sensor_16", "sensor_18", "sensor_19"]
INFORMATIVE_SENSORS: list[str] = [s for s in SENSORS if s not in DROPPED_SENSORS]

# Physical meaning (Saxena et al., 2008). Used for plain-English explanations.
SENSOR_DESCRIPTIONS: dict[str, str] = {
    "sensor_1": "T2 fan inlet temperature",
    "sensor_2": "T24 LPC outlet temperature",
    "sensor_3": "T30 HPC outlet temperature",
    "sensor_4": "T50 LPT outlet temperature",
    "sensor_5": "P2 fan inlet pressure",
    "sensor_6": "P15 bypass-duct pressure",
    "sensor_7": "P30 HPC outlet pressure",
    "sensor_8": "Nf physical fan speed",
    "sensor_9": "Nc physical core speed",
    "sensor_10": "epr engine pressure ratio",
    "sensor_11": "Ps30 HPC outlet static pressure",
    "sensor_12": "phi fuel flow / Ps30 ratio",
    "sensor_13": "NRf corrected fan speed",
    "sensor_14": "NRc corrected core speed",
    "sensor_15": "BPR bypass ratio",
    "sensor_16": "farB burner fuel-air ratio",
    "sensor_17": "htBleed bleed enthalpy",
    "sensor_18": "Nf_dmd demanded fan speed",
    "sensor_19": "PCNfR_dmd demanded corrected fan speed",
    "sensor_20": "W31 HPT coolant bleed",
    "sensor_21": "W32 LPT coolant bleed",
}

# --- Modelling constants -------------------------------------------------------
RUL_CAP: int = 125          # piecewise-linear target cap (Heimes, 2008)
WINDOW: int = 30            # temporal window in cycles (same as the SAA v1 LSTM)
SEED: int = 42
N_VAL_ENGINES: int = 20     # engine-level hold-out, as in SAA v1
CRITICAL_RUL: int = 50      # "critical zone" boundary used in SAA v1
ALERT_HORIZON: int = 30     # alert = "fails within 30 cycles"
