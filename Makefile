# HerdSim -- basic project targets (install, dev, test, lint, build).
# Shepherding-budget campaigns live in Makefile.budget:
#   make -f Makefile.budget help
#   make budget-help

.PHONY: help install dev dev-backend dev-frontend test test-backend test-stress \
	test-frontend lint format build clean budget-help \
	budget-test budget-pilot budget-pilot-state budget-analyse budget-scout \
	budget-factor-sweep

UV ?= uv
# Editable install may predate analysis/; scripts need the repo root on PYTHONPATH.
export PYTHONPATH := $(CURDIR)$(if $(PYTHONPATH),:$(PYTHONPATH),)

# Default target
help:
	@echo "HerdSim -- basic targets"
	@echo ""
	@echo "  make help            Show this help"
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
	@echo ""
	@echo "Shepherding-budget campaigns (separate Makefile):"
	@echo "  make -f Makefile.budget help"
	@echo "  make budget-help              (same as above)"

# Install (uv-managed .venv; avoids system pip / PEP 668)
install:
	$(UV) sync --extra dev
	cd frontend && npm install

# Development Servers
# One Ctrl+C stops both processes (see scripts/dev.sh).
dev:
	@exec bash scripts/dev.sh

dev-backend:
	$(UV) run uvicorn api.main:app --reload --port 8000

dev-frontend:
	cd frontend && npm run dev

# Testing
# Default: fast suite (stress excluded) + frontend build.
test: test-backend test-frontend

test-backend:
	$(UV) run pytest tests/backend/ -v -m "not stress"

test-stress:
	$(UV) run pytest tests/backend/ -v -m stress

test-frontend:
	node --test tests/frontend/*.test.js
	cd frontend && npm run build

# Code Quality
# Frontend eslint/prettier use npx (not pinned in package.json).
lint:
	$(UV) run ruff check .
	cd frontend && npx eslint src/

format:
	$(UV) run ruff format .
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
# Forward budget targets to Makefile.budget (keeps existing make budget-* habit)
# ---------------------------------------------------------------------------
budget-help:
	@$(MAKE) -f Makefile.budget help

budget-test budget-pilot budget-pilot-state budget-analyse budget-scout budget-factor-sweep:
	@$(MAKE) -f Makefile.budget $@
