# HerdSim: install, tests, lint. Campaigns: cli/campaign.py

.PHONY: help install test lint format typecheck check clean

UV ?= uv
export PYTHONPATH := $(CURDIR)$(if $(PYTHONPATH),:$(PYTHONPATH),)

help:
	@echo "HerdSim"
	@echo ""
	@echo "  make install | test | lint | format | typecheck | check | clean"
	@echo ""
	@echo "  test            unit, invariant and reproducibility tests"
	@echo ""
	@echo "Campaigns:"
	@echo "  uv run cli/campaign.py run dmin_f99_m6 --workers 16"
	@echo "  Protocol ids: protocols/configs/protocols/"

install:
	$(UV) sync --extra dev

test:
	$(UV) run pytest

lint:
	$(UV) run ruff check .
	$(UV) run ruff format --check .

format:
	$(UV) run ruff format .

typecheck:
	$(UV) run basedpyright

check: lint typecheck test

clean:
	find . -path ./.venv -prune -o -type d \( -name __pycache__ -o -name .pytest_cache -o -name .ruff_cache \) -prune -exec rm -rf {} +
