"""A tiny local imitation of Foundry's ``transforms.api``.

Why it exists: to understand what Foundry does under the hood (declared inputs and
outputs -> a dependency graph -> lineage -> ordered builds -> checks on outputs),
and to run the whole Aerolisa pipeline on a laptop before running it on Foundry.

Foundry                                  | Here
-----------------------------------------|---------------------------------------
``@transform_df(Output(p), x=Input(q))`` | ``@transform(Output(p), x=Input(q))``
Spark DataFrame                          | pandas DataFrame
Dataset path / RID                       | ``data/<layer>/<name>.parquet`` or ``.csv``
Data expectations (``Check``)            | ``Output(..., checks=[callable, ...])``
Data Lineage app                         | :func:`lineage_mermaid`
"""

from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass, field
from graphlib import CycleError, TopologicalSorter
from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parents[3] / "data"

CheckFn = Callable[[pd.DataFrame], str | None]  # returns an error message, or None if OK


@dataclass(frozen=True)
class Input:
    path: str


@dataclass(frozen=True)
class Output:
    path: str
    checks: tuple[CheckFn, ...] = field(default_factory=tuple)

    def __init__(self, path: str, checks: list[CheckFn] | None = None) -> None:
        object.__setattr__(self, "path", path)
        object.__setattr__(self, "checks", tuple(checks or ()))


@dataclass
class Transform:
    name: str
    output: Output
    inputs: dict[str, Input]
    fn: Callable[..., pd.DataFrame]


REGISTRY: dict[str, Transform] = {}


def transform(output: Output, **inputs: Input):
    """Register a pure function DataFrames -> DataFrame as the producer of ``output``."""

    def decorator(fn: Callable[..., pd.DataFrame]) -> Callable[..., pd.DataFrame]:
        if output.path in REGISTRY:
            raise ValueError(f"{output.path} already has a producer: {REGISTRY[output.path].name}")
        REGISTRY[output.path] = Transform(fn.__name__, output, inputs, fn)
        return fn

    return decorator


# --- checks (a small subset of Foundry data expectations) ----------------------
def primary_key(*cols: str) -> CheckFn:
    def check(df: pd.DataFrame) -> str | None:
        if df[list(cols)].isna().any().any():
            return f"primary key {cols} has nulls"
        dups = int(df.duplicated(subset=list(cols)).sum())
        return f"primary key {cols} has {dups} duplicates" if dups else None

    check.__name__ = f"primary_key{cols}"
    return check


def non_null(*cols: str) -> CheckFn:
    def check(df: pd.DataFrame) -> str | None:
        bad = [c for c in cols if df[c].isna().any()]
        return f"nulls in {bad}" if bad else None

    check.__name__ = f"non_null{cols}"
    return check


def in_range(col: str, lo: float | None = None, hi: float | None = None) -> CheckFn:
    def check(df: pd.DataFrame) -> str | None:
        s = df[col].dropna()
        if lo is not None and (s < lo).any():
            return f"{col} has values < {lo}"
        if hi is not None and (s > hi).any():
            return f"{col} has values > {hi}"
        return None

    check.__name__ = f"in_range({col},{lo},{hi})"
    return check


# --- storage -------------------------------------------------------------------
def dataset_file(path: str, data_dir: Path = DATA_DIR) -> Path:
    return data_dir / f"{path}.csv"


def read_dataset(path: str, data_dir: Path = DATA_DIR) -> pd.DataFrame:
    return pd.read_csv(dataset_file(path, data_dir))


def write_dataset(df: pd.DataFrame, path: str, data_dir: Path = DATA_DIR) -> None:
    f = dataset_file(path, data_dir)
    f.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(f, index=False)


# --- build runner ----------------------------------------------------------------
def build_order(targets: list[str] | None = None) -> list[str]:
    """Topological order of the registered outputs needed to build ``targets``."""
    graph = {out: {i.path for i in t.inputs.values() if i.path in REGISTRY} for out, t in REGISTRY.items()}
    try:
        order = list(TopologicalSorter(graph).static_order())
    except CycleError as exc:  # pragma: no cover - defensive
        raise ValueError(f"dependency cycle: {exc.args[1]}") from exc
    if targets is None:
        return order
    needed: set[str] = set()
    stack = list(targets)
    while stack:
        node = stack.pop()
        if node in needed:
            continue
        needed.add(node)
        stack.extend(graph.get(node, ()))
    return [o for o in order if o in needed]


def build(targets: list[str] | None = None, data_dir: Path = DATA_DIR, verbose: bool = True) -> dict:
    """Run transforms in dependency order, apply checks, write outputs. Returns a run report."""
    report: dict[str, dict] = {}
    cache: dict[str, pd.DataFrame] = {}
    for out in build_order(targets):
        t = REGISTRY[out]
        kwargs = {}
        for name, inp in t.inputs.items():
            kwargs[name] = cache[inp.path] if inp.path in cache else read_dataset(inp.path, data_dir)
        t0 = time.perf_counter()
        df = t.fn(**kwargs)
        errors = [msg for chk in t.output.checks if (msg := chk(df))]
        if errors:
            raise ValueError(f"checks failed on {out}: {errors}")
        write_dataset(df, out, data_dir)
        cache[out] = df
        report[out] = {"rows": len(df), "cols": df.shape[1], "seconds": round(time.perf_counter() - t0, 2),
                       "checks_passed": len(t.output.checks)}
        if verbose:
            print(f"built {out:<45} rows={len(df):>6}  checks={len(t.output.checks)}  {report[out]['seconds']}s")
    return report


def lineage_mermaid() -> str:
    lines = ["flowchart LR"]
    ids = {p: f"d{i}" for i, p in enumerate(sorted({*REGISTRY, *(i.path for t in REGISTRY.values() for i in t.inputs.values())}))}
    for p, i in ids.items():
        lines.append(f'    {i}["{p}"]')
    for out, t in REGISTRY.items():
        for inp in t.inputs.values():
            lines.append(f"    {ids[inp.path]} -->|{t.name}| {ids[out]}")
    return "\n".join(lines)
