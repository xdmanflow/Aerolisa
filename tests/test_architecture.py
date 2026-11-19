"""Dependency rule (docs/architecture.md): domain modules import only `core`; cli imports anything."""

import ast
from pathlib import Path

import pytest

SRC = Path(__file__).resolve().parents[1] / "src" / "aerolisa"
ALLOWED = {
    "core": set(),
    "pipelines": {"core"},
    "engine_health": {"core"},
    "fleet": {"core"},
    "planner": {"core"},
    "cli": {"core", "pipelines", "engine_health", "fleet", "planner"},
}


def imported(path: Path) -> set[str]:
    found = set()
    for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
        names = [a.name for a in node.names] if isinstance(node, ast.Import) else (
            [node.module] if isinstance(node, ast.ImportFrom) and node.module and node.level == 0 else [])
        found |= {n.split(".")[1] for n in names if n.startswith("aerolisa.")}
    return found


@pytest.mark.parametrize("component", sorted(ALLOWED))
def test_dependency_rule(component):
    for f in (SRC / component).rglob("*.py"):
        illegal = imported(f) - ALLOWED[component] - {component}
        assert not illegal, f"{f.name} imports {illegal}"


def test_every_component_has_a_rule():
    assert {p.name for p in SRC.iterdir() if (p / "__init__.py").exists()} == set(ALLOWED)
