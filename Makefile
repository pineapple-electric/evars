.PHONY: help
help:
	@echo Targets:
	@echo "    clean         Remove artifacts"
	@echo "    format        Format the code"
	@echo "    lint          Lint the code"
	@echo "    release       Package the code for release"
	@echo "    test          Run the tests"

.PHONY: clean
clean:
	find . -type d -name __pycache__ -delete
	rm -rf build
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf dist
	rm -rf evars.egg-info
	rm -rf .mypy_cache
	rm -rf .pytest_cache

# Aggregate targets
.PHONY: format
format: black

.PHONY: lint
lint: bandit mypy pylint

.PHONY: release
release: sdist wheel

.PHONY: test
test: pytest

# Command targets
.PHONY: bandit
bandit:
	bandit -c bandit.yaml -r src

.PHONY: black
black:
	black --line-length=79 src

.PHONY: mypy
mypy:
	mypy src

.PHONY: pytest
pytest:
	pytest --cov=src --cov-report=html src

.PHONY: pylint
pylint:
	pylint src || echo Status: $$?

.PHONY: sdist
sdist:
	python -m build --sdist

.PHONY: wheel
wheel:
	python -m build --wheel
