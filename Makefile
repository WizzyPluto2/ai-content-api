.PHONY: help install dev test test-cov lint format type-check run run-dev docker-build docker-up docker-down clean

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install production dependencies
	pip install -r requirements.txt

dev: ## Install all dependencies + pre-commit hooks
	pip install -r requirements-dev.txt
	pre-commit install

test: ## Run tests
	pytest tests/ -v --tb=short

test-cov: ## Run tests with coverage report
	pytest tests/ -v --tb=short --cov=. --cov-report=term-missing

lint: ## Run linter (Ruff)
	ruff check .

format: ## Format code (Ruff)
	ruff format .

type-check: ## Run type checker (mypy)
	mypy --ignore-missing-imports providers/ templates/ database/ api/

run: ## Run the API server
	python app.py

run-dev: ## Run with auto-reload
	uvicorn app:app --reload --host 0.0.0.0 --port 8000

docker-build: ## Build Docker image
	docker build -t ai-content-api .

docker-up: ## Start with Docker Compose (includes Ollama)
	docker compose up -d

docker-down: ## Stop Docker Compose
	docker compose down

clean: ## Remove build artifacts and cache
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .ruff_cache -exec rm -rf {} + 2>/dev/null || true
	rm -rf build/ dist/ *.egg-info/ data/test*.db test_data/
