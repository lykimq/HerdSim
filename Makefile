.PHONY: help install dev dev-backend dev-frontend test test-backend test-stress test-frontend lint format build clean

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
