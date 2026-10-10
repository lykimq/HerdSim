# HerdSim scaling-cli: RQ campaigns on the shared simulation engine.
# Layout: sim/ (engine) | run/ (campaigns) | analysis/ (post-run) | docs/ | results/

.PHONY: help install test test-ci test-stress lint format typecheck check clean \
	scaling-help scaling-test scaling-pilot scaling-pilot-state scaling-analyse \
	scaling-scout scaling-claim-plan scaling-claim-reseed scaling-t1-plan scaling-t1 \
	scaling-factor-sweep

UV ?= uv
# Repo root only. Do not add run/ here: run/packaging would shadow PyPI packaging.
export PYTHONPATH := $(CURDIR)$(if $(PYTHONPATH),:$(PYTHONPATH),)

help:
	@echo "HerdSim (scaling-cli): RQ protocols + shared engine"
	@echo ""
	@echo "  sim/        Tick engine (core, plugins, methods)"
	@echo "  run/        Campaigns, protocols, packaging -> make -C run help"
	@echo "  analysis/   Post-run frontiers, plots, package export"
	@echo "  results/    Trial data and packages"
	@echo "  docs/       Architecture, science, report (report contents frozen)"
	@echo ""
	@echo "Common targets:"
	@echo "  make install | test | test-ci | lint | format | typecheck | check"
	@echo "  make scaling-help | scaling-test | scaling-pilot | scaling-scout | ..."
	@echo "  Full campaign list: make -C run help"

install:
	$(UV) sync --extra dev

test test-ci:
	$(UV) run pytest tests/backend -q -m "not stress"

test-stress:
	$(UV) run pytest tests/backend -q -m stress

lint:
	$(UV) run ruff check .

format:
	$(UV) run ruff format .

typecheck:
	$(UV) run basedpyright

check: lint typecheck test-ci

clean:
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
	find . -type d -name .pytest_cache -prune -exec rm -rf {} +
	find . -type d -name .ruff_cache -prune -exec rm -rf {} +

scaling-help:
	@$(MAKE) -C run help

scaling-test scaling-pilot scaling-pilot-state scaling-analyse scaling-scout \
	scaling-claim-plan scaling-claim-reseed scaling-t1-plan scaling-t1 \
	scaling-factor-sweep:
	@$(MAKE) -C run $@
