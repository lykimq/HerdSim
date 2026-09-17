.PHONY: help install dev dev-backend dev-frontend test test-backend test-stress test-frontend lint format build clean \
	budget-help budget-test budget-pilot budget-pilot-state budget-analyse budget-scout

PYTHON ?= python
# Editable install may predate analysis/; scripts need the repo root on PYTHONPATH.
export PYTHONPATH := $(CURDIR)$(if $(PYTHONPATH),:$(PYTHONPATH),)

# Budget campaign defaults (override on the make command line).
BUDGET_INSTRUMENT ?= strombom_multi
BUDGET_LAYOUT ?= compact
BUDGET_LAYOUTS_STATE ?= compact wide split outlier_rich
BUDGET_N ?= 25 50 100
BUDGET_D ?= 1 2 3 4 6 10
BUDGET_SEEDS ?= 5
BUDGET_OUT ?= results/budget/pilot
BUDGET_MAX_TICKS ?=
WORKERS ?= 1
PACKAGE ?= A
TRIALS ?= $(BUDGET_OUT)/trials.csv
OUT ?= $(BUDGET_OUT)/package_$(shell echo $(PACKAGE) | tr A-Z a-z)

# Scout defaults (long-running; see budget-help).
SCOUT_N ?= 25 50 75 100 150 200
SCOUT_D ?= 1 2 3 4 6 10 15 20
SCOUT_SEEDS ?= 30
SCOUT_OUT ?= results/budget/scout
SCOUT_LAYOUT ?= compact

# Default target
help:
	@echo "HerdSim make targets"
	@echo ""
	@echo "  make install         Install Python (editable + dev) and frontend deps"
	@echo "  make dev             Start API + Vite together (Ctrl+C stops both)"
	@echo "  make dev-backend     Start FastAPI only (port 8000, reload)"
	@echo "  make dev-frontend    Start Vite only"
	@echo "  make test            Backend tests (no stress) + frontend tests/build"
	@echo "  make test-backend    Pytest under tests/backend/ (excludes stress)"
	@echo "  make test-stress     Pytest stress-marked backend tests"
	@echo "  make test-frontend   Node frontend tests + production build"
	@echo "  make lint            Ruff check + frontend eslint"
	@echo "  make format          Ruff format + frontend prettier"
	@echo "  make build           Frontend production build"
	@echo "  make clean           Remove caches, dist, and Vite cache"
	@echo "  make budget-help     List shepherding-budget campaign targets"
	@echo "  make budget-test     Budget stack unit tests"
	@echo "  make budget-pilot    Small Phase-1 pilot grid + Package A"
	@echo "  make help            Show this help"

# Install
install:
	pip install -e ".[dev]"
	cd frontend && npm install

# Development Servers
# One Ctrl+C stops both processes (see scripts/dev.sh).
dev:
	@exec bash scripts/dev.sh

dev-backend:
	uvicorn api.main:app --reload --port 8000

dev-frontend:
	cd frontend && npm run dev

# Testing
# Default: fast suite (stress excluded) + frontend build.
test: test-backend test-frontend

test-backend:
	pytest tests/backend/ -v -m "not stress"

test-stress:
	pytest tests/backend/ -v -m stress

test-frontend:
	node --test tests/frontend/*.test.js
	cd frontend && npm run build

# Code Quality
# Frontend eslint/prettier use npx (not pinned in package.json).
lint:
	ruff check .
	cd frontend && npx eslint src/

format:
	ruff format .
	cd frontend && npx prettier --write src/

# Build
build:
	cd frontend && npm run build

# Clean
clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache .ruff_cache
	cd frontend && rm -rf dist node_modules/.vite

# ---------------------------------------------------------------------------
# Shepherding budget campaigns (docs/research/budget/main_shepherding_budget_plan.md)
# ---------------------------------------------------------------------------
# Override examples:
#   make budget-pilot BUDGET_MAX_TICKS=3000 WORKERS=1
#   make budget-analyse PACKAGE=A TRIALS=results/budget/pilot/trials.csv OUT=results/budget/pilot/package_a

budget-help:
	@echo "Shepherding budget targets"
	@echo ""
	@echo "  make budget-test          Unit tests for the budget stack"
	@echo "  make budget-pilot         Phase-1 pilot: compact layout, Package A analyse"
	@echo "  make budget-pilot-state   Same N/D grid over all X0 layouts, Package B"
	@echo "  make budget-analyse       Analyse trials (PACKAGE, TRIALS, OUT)"
	@echo "  make budget-scout         Fuller scout grid (LONG-RUNNING)"
	@echo ""
	@echo "Pilot defaults (override on the command line):"
	@echo "  BUDGET_INSTRUMENT=$(BUDGET_INSTRUMENT)"
	@echo "  BUDGET_LAYOUT=$(BUDGET_LAYOUT)   (state: BUDGET_LAYOUTS_STATE)"
	@echo "  BUDGET_N=$(BUDGET_N)"
	@echo "  BUDGET_D=$(BUDGET_D)"
	@echo "  BUDGET_SEEDS=$(BUDGET_SEEDS)"
	@echo "  BUDGET_OUT=$(BUDGET_OUT)"
	@echo "  BUDGET_MAX_TICKS=<empty uses protocol time_limit_t0=10000>"
	@echo "  WORKERS=$(WORKERS)"
	@echo ""
	@echo "Analyse defaults:"
	@echo "  PACKAGE=$(PACKAGE)  TRIALS=$(TRIALS)  OUT=$(OUT)"
	@echo ""
	@echo "Scout defaults (long-running; one instrument, one layout):"
	@echo "  SCOUT_N=$(SCOUT_N)"
	@echo "  SCOUT_D=$(SCOUT_D)"
	@echo "  SCOUT_SEEDS=$(SCOUT_SEEDS)"
	@echo "  SCOUT_OUT=$(SCOUT_OUT)"
	@echo "  SCOUT_LAYOUT=$(SCOUT_LAYOUT)"

budget-test:
	$(PYTHON) -m pytest tests/backend/correctness/test_budget_stack.py -q

# Optional --max-ticks only when BUDGET_MAX_TICKS is set.
BUDGET_MAX_TICKS_FLAG = $(if $(BUDGET_MAX_TICKS),--max-ticks $(BUDGET_MAX_TICKS),)

budget-pilot:
	@mkdir -p $(BUDGET_OUT)
	$(PYTHON) scripts/budget/run_grid.py \
		--output $(BUDGET_OUT) \
		--instruments $(BUDGET_INSTRUMENT) \
		--layouts $(BUDGET_LAYOUT) \
		--n $(BUDGET_N) \
		--d $(BUDGET_D) \
		--seeds $(BUDGET_SEEDS) \
		--workers $(WORKERS) \
		--campaign-id budget_pilot \
		$(BUDGET_MAX_TICKS_FLAG)
	$(MAKE) budget-analyse PACKAGE=A TRIALS=$(BUDGET_OUT)/trials.csv OUT=$(BUDGET_OUT)/package_a

budget-pilot-state:
	@mkdir -p $(BUDGET_OUT)/state
	$(PYTHON) scripts/budget/run_grid.py \
		--output $(BUDGET_OUT)/state \
		--instruments $(BUDGET_INSTRUMENT) \
		--layouts $(BUDGET_LAYOUTS_STATE) \
		--n $(BUDGET_N) \
		--d $(BUDGET_D) \
		--seeds $(BUDGET_SEEDS) \
		--workers $(WORKERS) \
		--campaign-id budget_pilot_state \
		$(BUDGET_MAX_TICKS_FLAG)
	$(MAKE) budget-analyse PACKAGE=B TRIALS=$(BUDGET_OUT)/state/trials.csv OUT=$(BUDGET_OUT)/state/package_b

budget-analyse:
	$(PYTHON) scripts/budget/analyse.py \
		--package $(PACKAGE) \
		--trials $(TRIALS) \
		--output $(OUT)

# Fuller scout: still a protocol subset vs full claim-grade sweep. LONG-RUNNING.
budget-scout:
	@echo "NOTE: budget-scout is long-running (many N x D x seeds cells)."
	@mkdir -p $(SCOUT_OUT)
	$(PYTHON) scripts/budget/run_grid.py \
		--output $(SCOUT_OUT) \
		--instruments $(BUDGET_INSTRUMENT) \
		--layouts $(SCOUT_LAYOUT) \
		--n $(SCOUT_N) \
		--d $(SCOUT_D) \
		--seeds $(SCOUT_SEEDS) \
		--workers $(WORKERS) \
		--campaign-id budget_scout \
		$(BUDGET_MAX_TICKS_FLAG)
	$(MAKE) budget-analyse PACKAGE=A TRIALS=$(SCOUT_OUT)/trials.csv OUT=$(SCOUT_OUT)/package_a
