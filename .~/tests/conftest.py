import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


@pytest.fixture(scope="session")
def gold():
    from aerolisa.engine_health.features import temporal_features
    from aerolisa.pipelines.cmapss import bronze_cmapss, gold_rul_labels, silver_cmapss_cycles

    bronze, rul = bronze_cmapss()
    return temporal_features(gold_rul_labels(silver_cmapss_cycles(bronze), rul))
