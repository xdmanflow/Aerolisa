from transforms.api import Pipeline

from aerolisa_pipelines.datasets import cmapss, objects

my_pipeline = Pipeline()
my_pipeline.discover_transforms(cmapss, objects)
# Step 14 (optional): add `opensky` once the Data Connection source exists.
