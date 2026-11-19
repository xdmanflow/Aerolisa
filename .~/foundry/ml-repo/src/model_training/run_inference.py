"""Batch inference: every observed cycle of every in-service engine -> EngineHealthSnapshot rows."""

from model_training import paths
from palantir_models.transforms import ModelInput
from transforms.api import Input, Output, transform

KEEP_SENSORS = ["sensor_11_mean", "sensor_4_mean", "sensor_9_mean", "sensor_7_mean"]


@transform(
    features=Input(paths.GOLD_ENGINE_CYCLE_FEATURES),
    model=ModelInput(paths.MODEL_ENGINE_HEALTH),
    out=Output(paths.GOLD_ENGINE_HEALTH_SNAPSHOT),
)
def compute(features, model, out):
    df = features.pandas()
    fleet = df[df["split"] == "test"].reset_index(drop=True)
    pred = model.transform(fleet).df_out
    pred = pred.merge(fleet[["cycle_id", "rul", *KEEP_SENSORS]], on="cycle_id")
    pred["snapshot_id"] = pred["cycle_id"]
    pred["is_latest"] = pred["cycle"] == pred.groupby("engine_id")["cycle"].transform("max")
    pred = pred.rename(columns={"rul": "rul_truth_simulation_only"}).drop(columns=["cycle_id"])
    num = pred.select_dtypes("number").columns
    pred[num] = pred[num].round(3)
    out.write_pandas(pred)
