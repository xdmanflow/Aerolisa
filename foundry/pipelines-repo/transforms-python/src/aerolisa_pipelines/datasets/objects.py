"""Ontology backing datasets: one dataset per object type, primary key enforced.

Inputs from the aerolisa-ml repository are referenced by path: cross-repository
lineage is normal in Foundry and shows up in Data Lineage.
"""

from pyspark.sql import types as T
from transforms import expectations as E
from transforms.api import Check, Input, Output, transform, transform_df

from aerolisa_pipelines import paths
from aerolisa_pipelines.logic import objects as O


@transform_df(
    Output(paths.OBJECTS_ENGINE, checks=[
        Check(E.primary_key("engine_id"), "Primary key", on_error="FAIL"),
        Check(E.col("band").is_in("RED", "AMBER", "GREEN"), "band domain", on_error="FAIL"),
    ]),
    assignment=Input(paths.GOLD_ENGINE_ASSIGNMENT),
    snapshot=Input(paths.GOLD_ENGINE_HEALTH_SNAPSHOT),
    rec=Input(paths.GOLD_INSPECTION_RECOMMENDATION),
)
def objects_engine(assignment, snapshot, rec):
    return O.engine_objects(assignment, snapshot, rec)


@transform_df(
    Output(paths.OBJECTS_AIRCRAFT, checks=Check(E.primary_key("tail_id"), "Primary key", on_error="FAIL")),
    aircraft=Input(paths.GOLD_FLEET_AIRCRAFT),
    util=Input(paths.GOLD_AIRCRAFT_UTILIZATION_DAILY),
    rec=Input(paths.GOLD_INSPECTION_RECOMMENDATION),
)
def objects_aircraft(aircraft, util, rec):
    return O.aircraft_objects(aircraft, util, rec)


@transform_df(
    Output(paths.OBJECTS_OPERATOR, checks=Check(E.primary_key("operator_code"), "Primary key", on_error="FAIL")),
    aircraft=Input(paths.GOLD_FLEET_AIRCRAFT),
)
def objects_operator(aircraft):
    return O.operator_objects(aircraft)


WORK_ORDER_SCHEMA = T.StructType([
    T.StructField(c, T.StringType(), True) for c in
    ["work_order_id", "engine_id", "recommendation_id", "work_type", "planned_date", "status",
     "comment", "created_by", "created_at", "closed_at", "finding"]
])


@transform(out=Output(paths.WRITEBACK_WORK_ORDERS))
def writeback_work_orders_seed(ctx, out):
    """Empty seed dataset backing the WorkOrder object type. Rows are created by the
    ScheduleInspection action (Ontology edits), never by a pipeline."""
    out.write_dataframe(ctx.spark_session.createDataFrame([], WORK_ORDER_SCHEMA))
