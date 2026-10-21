# HerdSim: install, tests, benchmarks, lint. Campaigns: cli/campaign.py

.PHONY: help install test bench lint format typecheck check clean

UV ?= uv
export PYTHONPATH := $(CURDIR)$(if $(PYTHONPATH),:$(PYTHONPATH),)

help:
	@echo "HerdSim"
	@echo ""
	@echo "  make install | test | bench | lint | format | typecheck | check | clean"
	@echo ""
	@echo "  test            unit, invariant and reproducibility tests"
	@echo "  bench           miniature real campaigns read for sense; run before a campaign session"
	@echo ""
	@echo "Campaigns:"
	@echo "  uv run cli/campaign.py run --protocol dmin_pilot --workers 16"
	@echo "  Protocol ids: protocols/configs/protocols/"

install:
	$(UV) sync --extra dev

test:
	$(UV) run python -m tests.run test

bench:
	$(UV) run python -m tests.run bench

lint:
	$(UV) run ruff check .

format:
	$(UV) run ruff format .

typecheck:
	$(UV) run basedpyright

check: lint typecheck test

clean:
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
	find . -type d -name .pytest_cache -prune -exec rm -rf {} +
	find . -type d -name .ruff_cache -prune -exec rm -rf {} +
