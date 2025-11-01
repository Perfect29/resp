.PHONY: help install dev build test clean docker-build docker-up docker-down deploy

help:
	@echo "Available commands:"
	@echo "  make install     - Install all dependencies"
	@echo "  make dev         - Start development servers"
	@echo "  make build       - Build for production"
	@echo "  make test        - Run tests"
	@echo "  make clean       - Clean build artifacts"
	@echo "  make docker-build - Build Docker images"
	@echo "  make docker-up   - Start Docker services"
	@echo "  make docker-down - Stop Docker services"

install:
	pip install -r requirements.txt
	cd frontend && npm install --legacy-peer-deps

dev:
	@echo "Starting development servers..."
	@echo "Backend: http://localhost:8000"
	@echo "Frontend: http://localhost:5173"
	uvicorn app.main:app --reload &
	cd frontend && npm run dev

build:
	pip install -r requirements.txt
	cd frontend && npm ci --legacy-peer-deps && npm run build

test:
	pytest tests/ -v || true

clean:
	find . -type d -name __pycache__ -exec rm -r {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf frontend/dist frontend/.vite frontend/.turbo
	rm -rf .pytest_cache .mypy_cache .ruff_cache

docker-build:
	docker build -t ai-visibility-tracker-backend .
	cd frontend && docker build -t ai-visibility-tracker-frontend .

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

deploy: build docker-build
	@echo "Build complete. Ready for deployment!"

