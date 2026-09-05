.PHONY: install dev dev-backend dev-frontend test test-backend test-frontend lint format build clean

# ─── Install ──────────────────────────────────────────────────
install:
	pip install -e ".[dev]"
	cd frontend && npm install

# ─── Development Servers ──────────────────────────────────────
dev:
	@echo "Starting backend (port 8000) and frontend (port 5173)..."
	$(MAKE) dev-backend &
	$(MAKE) dev-frontend

dev-backend:
	uvicorn api.main:app --reload --port 8000

dev-frontend:
	cd frontend && npm run dev

# ─── Testing ──────────────────────────────────────────────────
test: test-backend test-frontend

test-backend:
	pytest tests/backend/ -v

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
