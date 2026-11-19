"""Aerolisa: data & AI for aerospace operations, built on an aviation ontology.

Local twin of the Palantir Foundry edition. Every function in ``engine_health``,
``fleet`` and ``planner`` is pure (DataFrames in, DataFrames out) so the exact same
code runs here, in tests, and inside Foundry transforms (see ``foundry/``).
"""

__version__ = "1.0.0"
