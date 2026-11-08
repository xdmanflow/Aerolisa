"""Enforce the dependency rule from docs/architecture.md.

Each component may only import the Aerolisa components listed in ALLOWED.
Cross-component imports must be absolute (``from aerolisa.core import ...``).
"""

import ast
from pathlib import Path

import pytest

SRC = Path(__file__).resolve().parents[1] / "src" / "aerolisa"

ALLOWED: dict[str, set[str]] = {
    "core": set(),
    "pipelines": {"core"},
    "engine_health": {"core"},
    "fleet": {"core"},
    "analytics": {"core"},
    "planner": {"core", "engine_health", "fleet"},
    "api": {"core", "engine_health", "fleet", "analytics", "planner"},
    "copilot": {"core", "api", "planner"},
    "cli": {
        "core",
        "pipelines",
        "engine_health",
        "fleet",
        "analytics",
        "planner",
        "api",
        "copilot",
    },
}


def imported_components(path: Path) -> set[str]:
    """Return the Aerolisa components imported (absolutely) by a Python file."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    found: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            names = [node.module]
        else:
            continue
        for name in names:
            parts = name.split(".")
            if parts[0] == "aerolisa" and len(parts) > 1:
                found.add(parts[1])
    return found


@pytest.mark.parametrize("component", sorted(ALLOWED))
def test_dependency_rule(component: str) -> None:
    allowed = ALLOWED[component] | {component}
    for py_file in (SRC / component).rglob("*.py"):
        illegal = imported_components(py_file) - allowed
        assert not illegal, (
            f"{py_file.relative_to(SRC)} imports {sorted(illegal)}; "
            f"{component} may only import {sorted(allowed)}"
        )


def test_every_component_has_a_rule() -> None:
    packages = {p.name for p in SRC.iterdir() if (p / "__init__.py").exists()}
    assert packages == set(ALLOWED), "add new components to ALLOWED and docs/architecture.md"
