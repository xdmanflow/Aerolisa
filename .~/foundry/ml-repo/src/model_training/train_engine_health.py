"""Train and publish the engine-health model + a metrics dataset (one row per model version).

Foundry concepts: ``ModelOutput.publish``, model versions, ``@configure`` resources,
pandas inside a transform, metrics as a dataset you can chart in Quiver/Workshop.
"""

import json
from datetime import datetime, timezone

import pandas as pd
from model_adapters.adapter import EngineHealthAdapter
from model_training import paths
from palantir_models.transforms import ModelOutput
from transforms.api import Input, Output, configure, transform

from aerolisa.engine_health.bundle import train_bundle


@configure(profile=["DRIVER_MEMORY_MEDIUM"])  # drop this line if the profile is not enabled on your tier
@transform(
    features=Input(paths.GOLD_ENGINE_CYCLE_FEATURES),
    model_output=ModelOutput(paths.MODEL_ENGINE_HEALTH),
    metrics_out=Output(paths.GOLD_ENGINE_HEALTH_MODEL_METRICS),
)
def compute(features, model_output, metrics_out):
    df = features.pandas()
    bundle = train_bundle(df)                       # same function as the local twin and the research
    model_output.publish(model_adapter=EngineHealthAdapter(bundle))
    row = {"model_version": bundle.version, "trained_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "metrics_json": json.dumps(bundle.metrics)}
    row.update({k: float(v) for k, v in bundle.metrics.items() if isinstance(v, (int, float))})
    metrics_out.write_pandas(pd.DataFrame([row]))
