# Goal 1: Simulate + frontend (API, Vite, UI Experiments).
# From repo root: make -C platform help   or   make help

.PHONY: help install dev dev-backend dev-frontend test test-backend test-stress \
	test-frontend lint format typecheck build clean

ROOT := $(abspath $(CURDIR)/..)
UV ?= uv
export PYTHONPATH := $(ROOT):$(ROOT)/platform:$(ROOT)/scaling$(if $(PYTHONPATH),:$(PYTHONPATH),)

help:
	@echo "HerdSim platform -- Simulate + frontend"
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
	@echo "  make typecheck       Python static type check (basedpyright)"
	@echo "  make build           Python typecheck + frontend production build"
	@echo "  make clean           Remove caches, dist, and Vite cache"
	@echo ""
	@echo "Scaling protocols: make -C ../scaling help"

install:
	cd $(ROOT) && $(UV) sync --extra dev
	cd frontend && npm install

dev:
	@exec bash scripts/dev.sh

dev-backend:
	cd $(ROOT) && $(UV) run uvicorn api.main:app --reload --port 8000

dev-frontend:
	cd frontend && npm run dev

test: test-backend test-frontend

test-backend:
	cd $(ROOT) && $(UV) run pytest tests/backend/ -v -m "not stress"

test-stress:
	cd $(ROOT) && $(UV) run pytest tests/backend/ -v -m stress

test-frontend:
	cd $(ROOT) && node --test tests/frontend/*.test.js
	cd frontend && npm run build

lint:
	cd $(ROOT) && $(UV) run ruff check .
	cd frontend && npx eslint src/

format:
	cd $(ROOT) && $(UV) run ruff format .
	cd frontend && npx prettier --write src/

typecheck:
	cd $(ROOT) && $(UV) run basedpyright --project $(ROOT) --level error

build: typecheck
	cd frontend && npm run build

clean:
	cd $(ROOT) && find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	cd $(ROOT) && rm -rf .pytest_cache .ruff_cache
	cd frontend && rm -rf dist node_modules/.vite
