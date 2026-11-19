"""C-MAPSS ingestion: raw text files -> bronze -> silver -> gold (pandas twin).

The PySpark version that runs on Foundry is ``foundry/pipelines-repo/.../cmapss_*.py``;
both follow the same contract (dataset names, columns, primary keys, checks), and
``tests/test_pipelines.py`` pins the contract on the local side.
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import numpy as np
import pandas as pd

from aerolisa.core.schema import OP_SETTINGS, RAW_COLUMNS, RUL_CAP, SENSORS

RAW_DIR = Path(__file__).resolve().parents[3] / "data" / "raw" / "cmapss"


def engine_id(subset: str, split: str, unit: int) -> str:
    """Stable primary key of the Engine object, e.g. ``FD001-FLEET-007``.

    ``HIST`` engines are the run-to-failure training history; ``FLEET`` engines are
    the in-service engines (C-MAPSS test units) that the operational app monitors.
    """
    role = "HIST" if split == "train" else "FLEET"
    return f"{subset}-{role}-{int(unit):03d}"


# --- bronze ----------------------------------------------------------------------
def read_raw_file(path: Path) -> pd.DataFrame:
    """Raw C-MAPSS text file as received, plus ingestion metadata (bronze)."""
    df = pd.read_csv(path, sep=r"\s+", header=None, names=RAW_COLUMNS, engine="python")
    df["source_file"] = path.name
    df["ingested_at"] = datetime.now(UTC).isoformat(timespec="seconds")
    return df


def read_rul_file(path: Path) -> pd.DataFrame:
    rul = pd.read_csv(path, sep=r"\s+", header=None, names=["rul_at_cutoff"], engine="python")
    rul["unit"] = np.arange(1, len(rul) + 1)
    rul["source_file"] = path.name
    return rul


def bronze_cmapss(raw_dir: Path = RAW_DIR, subset: str = "FD001") -> tuple[pd.DataFrame, pd.DataFrame]:
    frames = [read_raw_file(raw_dir / f"{split}_{subset}.txt") for split in ("train", "test")]
    return pd.concat(frames, ignore_index=True), read_rul_file(raw_dir / f"RUL_{subset}.txt")


# --- silver ----------------------------------------------------------------------
def silver_cmapss_cycles(bronze: pd.DataFrame, subset: str = "FD001") -> pd.DataFrame:
    """Typed, named, one row per engine-cycle; keeps all 21 sensors (selection is a gold choice)."""
    df = bronze.copy()
    df["split"] = np.where(df["source_file"].str.startswith("train"), "train", "test")
    df["subset"] = subset
    df["unit"] = df["unit"].astype(int)
    df["cycle"] = df["cycle"].astype(int)
    for c in OP_SETTINGS + SENSORS:
        df[c] = df[c].astype(float)
    df["engine_id"] = [engine_id(subset, s, u) for s, u in zip(df["split"], df["unit"], strict=True)]
    df["cycle_id"] = df["engine_id"] + "-" + df["cycle"].astype(str).str.zfill(3)
    cols = ["cycle_id", "engine_id", "subset", "split", "unit", "cycle", *OP_SETTINGS, *SENSORS]
    return df[cols].sort_values(["engine_id", "cycle"]).reset_index(drop=True)


# --- gold: labels ----------------------------------------------------------------
def gold_rul_labels(cycles: pd.DataFrame, rul_file: pd.DataFrame) -> pd.DataFrame:
    """True RUL for every cycle.

    train: RUL = last cycle - cycle (engines run to failure).
    test:  RUL = (last observed cycle + RUL at cutoff) - cycle (ground truth from NASA).
    """
    df = cycles.copy()
    last = df.groupby("engine_id")["cycle"].transform("max")
    df["rul"] = last - df["cycle"]
    test = df["split"] == "test"
    cutoff = df.loc[test, "unit"].map(rul_file.set_index("unit")["rul_at_cutoff"])
    df.loc[test, "rul"] = df.loc[test, "rul"] + cutoff
    df["rul"] = df["rul"].astype(int)
    df["rul_capped"] = df["rul"].clip(upper=RUL_CAP)
    df["failure_cycle"] = (df["cycle"] + df["rul"]).astype(int)
    return df
