.PHONY: install test lint format app api build quality lineage up down clean

install:
	pip install -e ".[core,data,dev]"

test:
	pytest -q

lint:
	ruff check .
	ruff format --check .

format:
	ruff format .
	ruff check --fix .

# From M1
app:
	streamlit run app/Home.py

# From M2 (needs the CLI entry point enabled in pyproject.toml)
build:
	aerolisa build --all

quality:
	aerolisa quality

lineage:
	aerolisa lineage

# From M7
api:
	uvicorn aerolisa.api.main:app --reload

up:
	docker compose up -d

down:
	docker compose down

clean:
	rm -rf .pytest_cache .ruff_cache build dist *.egg-info
