.PHONY: install dev dev-backend dev-frontend test test-backend test-stress test-frontend lint format build clean

# ─── Install ──────────────────────────────────────────────────
install:
	pip install -e ".[dev]"
	cd frontend && npm install

# ─── Development Servers ──────────────────────────────────────
# One Ctrl+C stops both processes (see scripts/dev.sh).
dev:
	@exec bash scripts/dev.sh

dev-backend:
	uvicorn api.main:app --reload --port 8000

dev-frontend:
	cd frontend && npm run dev

# ─── Testing ──────────────────────────────────────────────────
# Default: fast suite (stress excluded) + frontend build.
test: test-backend test-frontend

test-backend:
	pytest tests/backend/ -v -m "not stress"

test-stress:
	pytest tests/backend/ -v -m stress

test-frontend:
	cd frontend && npm run build

# ─── Code Quality ────────────────────────────────────────────
lint:
	ruff check .
	cd frontend && npx eslint src/

format:
	ruff format .
	cd frontend && npx prettier --write src/

# ─── Build ────────────────────────────────────────────────────
build:
	cd frontend && npm run build

# ─── Clean ────────────────────────────────────────────────────
clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache .ruff_cache
	cd frontend && rm -rf dist node_modules/.vite
