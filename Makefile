# Firefly SBOM Tool - Development Makefile

.PHONY: help install install-dev test test-unit test-integration lint format clean docs build

# Default target
help:
	@echo "Firefly SBOM Tool - Development Commands"
	@echo "========================================"
	@echo ""
	@echo "Installation:"
	@echo "  install      Install the package in production mode"
	@echo "  install-dev  Install the package in development mode with all dependencies"
	@echo ""
	@echo "Testing:"
	@echo "  test         Run all tests with coverage"
	@echo "  test-unit    Run only unit tests"
	@echo "  test-integration  Run only integration tests"
	@echo ""
	@echo "Code Quality:"
	@echo "  lint         Run linting checks (flake8, mypy)"
	@echo "  format       Format code with black and isort"
	@echo "  format-check Check if code formatting is correct"
	@echo ""
	@echo "Documentation:"
	@echo "  docs         Generate documentation"
	@echo ""
	@echo "Maintenance:"
	@echo "  clean        Clean build artifacts and cache files"
	@echo "  build        Build distribution packages"

# Installation targets
install:
	pip install .

install-dev:
	pip install -e .
	pip install -r requirements-dev.txt

# Testing targets
test:
	pytest tests/ --cov=src/firefly_sbom --cov-report=term-missing --cov-report=html

test-unit:
	pytest tests/unit/ -v

test-integration:
	pytest tests/integration/ -v

# Code quality targets
lint:
	@echo "Running flake8..."
	flake8 src/ tests/
	@echo "Running mypy..."
	mypy src/

format:
	@echo "Formatting with black..."
	black src/ tests/
	@echo "Sorting imports with isort..."
	isort src/ tests/

format-check:
	@echo "Checking format with black..."
	black --check src/ tests/
	@echo "Checking import sorting with isort..."
	isort --check-only src/ tests/

# Documentation
docs:
	@echo "Generating documentation..."
	cd docs && make html

# Maintenance targets
clean:
	@echo "Cleaning build artifacts..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	@echo "Building distribution packages..."
	python setup.py sdist bdist_wheel

# Development workflow
dev-setup: install-dev
	@echo "Setting up development environment..."
	pre-commit install

# Quick development checks
quick-check: format-check lint test-unit
	@echo "Quick development checks passed!"

# Full CI pipeline
ci: format-check lint test
	@echo "CI pipeline completed successfully!"
