.PHONY: help
help:
	@echo Targets:
	@echo "    clean         Remove artifacts"
	@echo "    format        Format the code"
	@echo "    lint          Lint the code"
	@echo "    release       Package the code for release"
	@echo "    test          Run the tests with Nose"

.PHONY: clean
clean:
	find . -type d -name __pycache__ -delete
	rm -rf build
	rm -rf .coverage
	rm -rf cover
	rm -rf dist
	rm -rf evars.egg-info
	rm -rf .mypy_cache

# Aggregate targets
.PHONY: format
format: black

.PHONY: lint
lint: bandit mypy pylint

.PHONY: release
release: sdist wheel

.PHONY: test
test: nosetests

# Command targets
.PHONY: bandit
bandit:
	bandit -c bandit.yaml -r src/evars

.PHONY: black
black:
	black --line-length=79 src

.PHONY: mypy
mypy:
	mypy src/evars

.PHONY: nosetests
nosetests:
	nosetests --with-coverage --cover-html

.PHONY: pylint
pylint:
	pylint --ignore localtypes.py src/evars || echo Status: $$?
	pylint --class-naming-style=UPPER_CASE src/evars/localtypes.py || echo Status: $$?

.PHONY: sdist
sdist:
	python -m build --sdist

.PHONY: wheel
wheel:
	python -m build --wheel
