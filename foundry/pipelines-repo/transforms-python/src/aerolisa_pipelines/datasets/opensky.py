"""OPTIONAL (build guide step 14): real flights from the OpenSky Network.

Replaces the simulated utilisation with real cycles per airframe. Not needed for the
predictive-maintenance MVP; switch it on once the rest works.

Foundry setup: create a REST API *Source* in Data Connection for ``opensky-network.org``
(OAuth2 client credentials from your OpenSky account; store them as source secrets),
then reference it below. External transforms syntax changes between Foundry releases:
compare with the "External transforms" page of your Foundry docs before building.

OpenSky rules (non-commercial research): respect the time-window limit of the
flights-by-aircraft endpoint and your daily credits; never republish raw data.
"""

import json
from datetime import datetime, timedelta, timezone

from pyspark.sql import types as T
from transforms.api import Output, transform
from transforms.external.systems import Source, external_systems

from aerolisa_pipelines import paths

AIRFRAMES_ICAO24: list[str] = []  # fill with the icao24 hex codes you choose (one operator, A320 family)
SCHEMA = T.StructType([T.StructField("icao24", T.StringType()), T.StructField("day", T.StringType()),
                       T.StructField("payload", T.StringType()), T.StructField("fetched_at", T.StringType())])


@external_systems(opensky=Source("ri.magritte..source.REPLACE-WITH-YOUR-SOURCE-RID"))
@transform(out=Output(paths.BRONZE_OPENSKY_FLIGHTS))
def bronze_opensky_flights(ctx, out, opensky):
    conn = opensky.get_https_connection()
    client = conn.get_client()
    base = conn.url
    token = opensky.get_secret("access_token")  # or fetch one with the client-credentials flow
    now = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    rows = []
    for icao in AIRFRAMES_ICAO24:
        for d in range(1, 3):  # last 2 days per run; incremental history is built by scheduling
            begin, end = now - timedelta(days=d), now - timedelta(days=d - 1)
            r = client.get(f"{base}/api/flights/aircraft", params={"icao24": icao, "begin": int(begin.timestamp()),
                                                                    "end": int(end.timestamp())},
                           headers={"Authorization": f"Bearer {token}"}, timeout=30)
            if r.status_code == 200:
                rows.append((icao, begin.date().isoformat(), json.dumps(r.json()), now.isoformat()))
    out.write_dataframe(ctx.spark_session.createDataFrame(rows, SCHEMA))
