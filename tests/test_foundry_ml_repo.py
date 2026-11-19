"""Runs the Foundry ML repository code (foundry/ml-repo) locally with tiny fakes of
`transforms.api` and `palantir_models`, to catch wiring bugs before pasting into Foundry.
PySpark transforms (foundry/pipelines-repo) are tested inside Foundry instead."""

import importlib
import subprocess
import sys
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ML = ROOT / "foundry" / "ml-repo" / "src"


class FakeIO:
    def __init__(self, df=None):
        self.df = df

    def pandas(self):
        return self.df.copy()

    def write_pandas(self, df):
        self.df = df


def _install_fakes():
    api = types.ModuleType("transforms.api")
    api.transform = lambda **kw: (lambda fn: fn)
    api.configure = lambda **kw: (lambda fn: fn)
    api.Input = api.Output = lambda path, **kw: path
    sys.modules["transforms"] = types.ModuleType("transforms")
    sys.modules["transforms.api"] = api

    pm = types.ModuleType("palantir_models")

    class ModelAdapter:
        pass

    pm.ModelAdapter = ModelAdapter
    pm.auto_serialize = lambda **kw: (lambda fn: fn)
    pm.Pandas = lambda columns: columns
    ser = types.ModuleType("palantir_models.serializers")
    ser.DillSerializer = lambda: None
    tr = types.ModuleType("palantir_models.transforms")
    tr.ModelOutput = tr.ModelInput = lambda path, **kw: path
    sys.modules.update({"palantir_models": pm, "palantir_models.serializers": ser, "palantir_models.transforms": tr})


def test_ml_repo_end_to_end(gold):
    _install_fakes()
    sys.path.insert(0, str(ML))
    try:
        for m in [m for m in sys.modules if m == "aerolisa" or m.startswith("aerolisa.")]:
            del sys.modules[m]
        train = importlib.import_module("model_training.train_engine_health")
        infer = importlib.import_module("model_training.run_inference")
        fp = importlib.import_module("model_training.fleet_and_planner")
        adapter_mod = importlib.import_module("model_adapters.adapter")
        assert "foundry" in adapter_mod.__file__

        published = {}

        class FakeModelOutput:
            def publish(self, model_adapter):
                published["adapter"] = model_adapter

        metrics = FakeIO()
        train.compute(FakeIO(gold), FakeModelOutput(), metrics)
        assert metrics.df["alert_threshold_cycles"].iloc[0] == 25
        assert abs(metrics.df["test_rmse"].iloc[0] - 13.98) < 0.05

        class FakeModelInput:
            def transform(self, df):
                return types.SimpleNamespace(df_out=published["adapter"].predict(df))

        snap = FakeIO()
        infer.compute(FakeIO(gold), FakeModelInput(), snap)
        assert len(snap.df) == 13096 and snap.df["snapshot_id"].is_unique and snap.df["is_latest"].sum() == 100

        ac, ut = FakeIO(), FakeIO()
        fp.fleet_aircraft(ac)
        fp.aircraft_utilization_daily(ut, ac)
        from aerolisa.fleet.simulate import assign_engines

        assign = FakeIO(assign_engines(ac.df, sorted(gold.loc[gold.split == "test", "engine_id"].unique())))
        rec = FakeIO()
        fp.inspection_recommendation(rec, snap, assign, ac, ut, metrics)
        assert len(rec.df) == 100 and rec.df["rank"].tolist() == list(range(1, 101))
        assert set(rec.df["band"]) <= {"RED", "AMBER", "GREEN"}
    finally:
        sys.path.remove(str(ML))
        for m in [m for m in sys.modules if m.split(".")[0] in {"aerolisa", "model_training", "model_adapters", "transforms", "palantir_models"}]:
            del sys.modules[m]


def test_foundry_copy_is_in_sync():
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "sync_foundry.py"), "--check"], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout
