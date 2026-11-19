.PHONY: install test lint build lineage catalog research sync clean

install:
	pip install -e ".[dev,research]"

test:
	pytest -q

lint:
	ruff check src tests scripts research/run_experiments.py foundry

build:
	python -m aerolisa.cli build

lineage:
	python -m aerolisa.cli lineage

catalog:
	python -m aerolisa.cli catalog

research:
	python research/run_experiments.py

sync:
	python scripts/sync_foundry.py

clean:
	rm -rf .pytest_cache .ruff_cache build dist *.egg-info data/bronze data/silver data/gold data/objects data/writeback
