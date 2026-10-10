# HerdSim scaling-cli: research-question campaigns on the shared simulation engine.
# Platform GUI lives on main; this branch is RQ / protocol only.

.PHONY: help install test test-ci test-stress lint format typecheck check clean \
	scaling-help scaling-test scaling-pilot scaling-pilot-state scaling-analyse \
	scaling-scout scaling-claim-plan scaling-claim-reseed scaling-t1-plan scaling-t1 \
	scaling-factor-sweep

UV ?= uv
export PYTHONPATH := $(CURDIR):$(CURDIR)/scaling$(if $(PYTHONPATH),:$(PYTHONPATH),)

help:
	@echo "HerdSim (scaling-cli branch): RQ protocols + shared engine"
	@echo ""
	@echo "  Engine:   core/ plugins/ methods/ services/shared/ analysis/"
	@echo "  Campaigns: scaling/  (make -C scaling help)"
	@echo ""
	@echo "Common targets:"
	@echo "  make install | test | test-ci | lint | format | typecheck | check"
	@echo "  make scaling-help | scaling-test | scaling-pilot | scaling-scout | ..."
	@echo "  Full campaign list: make -C scaling help"
	@echo ""
	@echo "Platform GUI is not on this branch (see main)."

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
	@$(MAKE) -C scaling help

scaling-test scaling-pilot scaling-pilot-state scaling-analyse scaling-scout \
	scaling-claim-plan scaling-claim-reseed scaling-t1-plan scaling-t1 \
	scaling-factor-sweep:
	@$(MAKE) -C scaling $@
