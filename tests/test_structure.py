"""Smoke tests: the package and every component import cleanly."""

import importlib

import pytest

import aerolisa

COMPONENTS = [
    "aerolisa.core",
    "aerolisa.pipelines",
    "aerolisa.engine_health",
    "aerolisa.fleet",
    "aerolisa.analytics",
    "aerolisa.planner",
    "aerolisa.api",
    "aerolisa.copilot",
    "aerolisa.cli",
]


def test_version():
    assert aerolisa.__version__ == "0.0.1"


@pytest.mark.parametrize("name", COMPONENTS)
def test_component_imports(name):
    assert importlib.import_module(name) is not None
