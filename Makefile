.PHONY: help install test clean

# Default target
help:
	@echo "Available commands:"
	@echo "  install    - Install dependencies for all services"
	@echo "  test       - Run tests for all services"
	@echo "  clean      - Clean build artifacts and cache"
	@echo "  extractor  - Run commands for extractor-api service"

# Install dependencies for all services
install:
	@echo "Installing dependencies for extractor-api..."
	cd extractor-api && make install

# Run tests for all services
test:
	@echo "Running tests for extractor-api..."
	cd extractor-api && make test

# Clean build artifacts and cache
clean:
	@echo "Cleaning build artifacts..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".coverage" -exec rm -rf {} + 2>/dev/null || true
	cd extractor-api && make clean

# Commands for extractor-api service
extractor:
	@echo "Use 'make extractor-<command>' to run extractor-api commands"
	@echo "Available commands: install, test, run, clean"

extractor-install:
	cd extractor-api && make install

extractor-test:
	cd extractor-api && make test

extractor-run:
	cd extractor-api && make run

extractor-clean:
	cd extractor-api && make clean 