
.PHONY: install dev lint format typecheck test clean help setup

BLUE=\033[0;34m
GREEN=\033[0;32m
YELLOW=\033[1;33m
RED=\033[0;31m
NC=\033[0m # No Color

all: help

help:
	@echo "$(BLUE)🚀 Quantiq Development Commands$(NC)"
	@echo "$(YELLOW)Usage: make <command>$(NC)"
	@echo ""
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z_-]+:.*##/ { printf "  $(GREEN)%-15s$(NC) %s\n", $$1, $$2 }' $(MAKEFILE_LIST)
	@echo ""
	@echo "$(YELLOW)Quick start: make setup && make dev$(NC)"

setup:
	@echo "$(BLUE)🔧 Setting up Quantiq development environment...$(NC)"
	poetry install
	poetry run pre-commit install
	@echo "$(GREEN)✅ Setup completed! Run 'make dev' to start development server.$(NC)"

install:
	@echo "$(BLUE)📦 Installing dependencies...$(NC)"
	poetry install
	@echo "$(GREEN)✅ Dependencies installed$(NC)"

dev:
	@echo "$(BLUE)🚀 Starting Quantiq development server...$(NC)"
	@echo "$(YELLOW)Server will be available at: http://localhost:8000$(NC)"
	@echo "$(YELLOW)API docs will be available at: http://localhost:8000/docs$(NC)"
	poetry run uvicorn quantiq.main:app --reload --host 0.0.0.0 --port 8000

lint:
	@echo "$(BLUE)🔍 Checking code quality...$(NC)"
	poetry run ruff check .

lint-fix:
	@echo "$(BLUE)🔧 Fixing code quality issues...$(NC)"
	poetry run ruff check . --fix
	@echo "$(GREEN)✅ Code quality issues fixed$(NC)"

format:
	@echo "$(BLUE)🎨 Formatting code...$(NC)"
	poetry run ruff format .
	@echo "$(GREEN)✅ Code formatted$(NC)"

typecheck:
	@echo "$(BLUE)🔍 Running type checks...$(NC)"
	poetry run pyright .
	@echo "$(GREEN)✅ Type checking completed$(NC)"

test:
	@echo "$(BLUE)🧪 Running tests...$(NC)"
	poetry run pytest

test-cov:
	@echo "$(BLUE)🧪 Running tests with coverage...$(NC)"
	poetry run pytest --cov=quantiq --cov-report=html --cov-report=term-missing
	@echo "$(YELLOW)📊 Coverage report generated in htmlcov/$(NC)"

# Combined workflows
fix: lint-fix format
	@echo "$(GREEN)✅ Code fixed and formatted!$(NC)"

check: lint typecheck
	@echo "$(GREEN)✅ All checks passed!$(NC)"

ready: fix typecheck test
	@echo "$(GREEN)🎉 Code is ready for commit!$(NC)"

full-check: lint typecheck test
	@echo "$(GREEN)✅ Full validation completed!$(NC)"

# Environment management
clean:
	@echo "$(BLUE)🧹 Cleaning up...$(NC)"
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	rm -rf .pytest_cache/ .ruff_cache/ .mypy_cache/ htmlcov/ .coverage
	@echo "$(GREEN)✅ Cleanup completed$(NC)"

update:
	@echo "$(BLUE)⬆️  Updating dependencies...$(NC)"
	poetry update
	@echo "$(GREEN)✅ Dependencies updated$(NC)"

pre-commit:
	@echo "$(BLUE)🔍 Running pre-commit hooks...$(NC)"
	poetry run pre-commit run --all-files

install-hooks:
	poetry run pre-commit install
	@echo "$(GREEN)✅ Pre-commit hooks installed$(NC)"

db-migrate:
	@echo "$(BLUE)🗄️  Running database migrations...$(NC)"
	# poetry run alembic upgrade head

db-reset:
	@echo "$(RED)⚠️  This will delete all data! Press Ctrl+C to cancel...$(NC)"
	@sleep 3
	# Add your database reset commands here
	rm -rf quantiq/quantiq.db

# Production commands
build:
	@echo "$(BLUE)🏗️  Building application...$(NC)"
	poetry build
	@echo "$(GREEN)✅ Build completed$(NC)"

# Documentation
docs:
	@echo "$(BLUE)📚 Generating documentation...$(NC)"
	@echo "$(YELLOW)📖 API docs available at: http://localhost:8000/docs$(NC)"
	@echo "$(YELLOW)📖 ReDoc available at: http://localhost:8000/redoc$(NC)"

# Show project status
status:
	@echo "$(BLUE)📊 Quantiq Project Status$(NC)"
	@echo ""
	@echo "$(YELLOW)🐍 Python Version:$(NC)"
	@poetry run python --version
	@echo ""
	@echo "$(YELLOW)📦 Dependencies:$(NC)"
	@poetry show --only=main | head -5
	@echo ""
	@echo "$(YELLOW)🔧 Dev Dependencies:$(NC)"
	@poetry show --only=dev | head -5
	@echo ""
	@echo "$(YELLOW)🏠 Virtual Environment:$(NC)"
	@poetry env info --path
	@echo ""
	@echo "$(YELLOW)Quick commands:$(NC)"
	@echo "  make dev     - Start development server"
	@echo "  make fix     - Fix and format code"
	@echo "  make ready   - Prepare for commit"
