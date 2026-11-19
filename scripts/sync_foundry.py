"""Copy the tested `aerolisa` package into the Foundry ML repository (single source of truth).

    python scripts/sync_foundry.py          # copy
    python scripts/sync_foundry.py --check  # fail if the Foundry copy is out of date (used by tests/CI)

In Foundry: paste/commit foundry/ml-repo/src/aerolisa next to model_adapters/ and model_training/.
"""

from __future__ import annotations

import filecmp
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "aerolisa"
DST = ROOT / "foundry" / "ml-repo" / "src" / "aerolisa"
SKIP = {"cli", "__pycache__"}


def files(base: Path) -> list[Path]:
    return sorted(p.relative_to(base) for p in base.rglob("*.py") if not SKIP & set(p.relative_to(base).parts))


def check() -> list[str]:
    problems = [f"missing or stale: {rel}" for rel in files(SRC) if not (DST / rel).exists() or not filecmp.cmp(SRC / rel, DST / rel, shallow=False)]
    if DST.exists():
        problems += [f"extra: {rel}" for rel in files(DST) if not (SRC / rel).exists()]
    return problems


def sync() -> None:
    if DST.exists():
        shutil.rmtree(DST)
    for rel in files(SRC):
        (DST / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(SRC / rel, DST / rel)
    print(f"synced {len(files(SRC))} files -> {DST.relative_to(ROOT)}")


if __name__ == "__main__":
    if "--check" in sys.argv:
        p = check()
        print("\n".join(p) or "Foundry copy is up to date")
        sys.exit(1 if p else 0)
    sync()
