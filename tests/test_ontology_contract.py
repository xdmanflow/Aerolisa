"""Every ontology property must map to a column of its backing dataset (local twin build)."""

from pathlib import Path

import pandas as pd
import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
ONTO = yaml.safe_load((ROOT / "foundry" / "ontology" / "ontology.yaml").read_text())


@pytest.fixture(scope="module")
def built():
    import sys

    sys.path.insert(0, str(ROOT / "src"))
    from aerolisa.cli import graph  # noqa: F401
    from aerolisa.core.transforms import build

    targets = sorted({ot["backing_dataset"] for ot in ONTO["object_types"].values()})
    build(targets, verbose=False)
    return {t: pd.read_csv(ROOT / "data" / f"{t}.csv", nrows=5) for t in targets}


@pytest.mark.parametrize("name", sorted(ONTO["object_types"]))
def test_properties_exist(name, built):
    ot = ONTO["object_types"][name]
    cols = set(built[ot["backing_dataset"]].columns)
    missing = [p for p, spec in ot["properties"].items() if spec["column"] not in cols]
    assert not missing, f"{name}: {missing}"
    assert ot["primary_key"] in ot["properties"]


def test_links_point_to_real_properties():
    for link in ONTO["link_types"]:
        obj, prop = link["foreign_key"].split(".")
        assert prop in ONTO["object_types"][obj]["properties"], link
        assert link["from"] in ONTO["object_types"] and link["to"] in ONTO["object_types"]
