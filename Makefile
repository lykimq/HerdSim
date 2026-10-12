# HerdSim scaling-cli: install, tests, lint. Campaigns: cli/campaign.py

.PHONY: help install test lint format typecheck check clean

UV ?= uv
# Repo root only. Do not add protocols/ here: packaging name clashes are avoided
# by using the protocols.packaging package path.
export PYTHONPATH := $(CURDIR)$(if $(PYTHONPATH),:$(PYTHONPATH),)

help:
	@echo "HerdSim (scaling-cli)"
	@echo ""
	@echo "  make install | test | lint | format | typecheck | check | clean"
	@echo ""
	@echo "Campaigns:"
	@echo "  uv run cli/campaign.py help"
	@echo "  uv run cli/campaign.py run --protocol phase1_scout --workers 18"
	@echo "  Protocol ids: protocols/configs/protocols/"

install:
	$(UV) sync --extra dev

test:
	$(UV) run pytest tests -q

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
