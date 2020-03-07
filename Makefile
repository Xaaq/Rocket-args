.PHONY: help clean type-check lint coverage test test-all test-all-fast docs dist
.DEFAULT_GOAL = help

help: ## show this message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

clean: ## remove all build and test artifacts along with python cache
	@rm -f requirements.txt
	@rm -f .coverage
	@rm -rf dist/
	@rm -rf site/
	@rm -rf htmlcov/
	@rm -rf .tox/
	@rm -rf .mypy_cache/
	@find . -name '.pytest_cache' -exec rm -fr {} +
	@find . -name '__pycache__' -exec rm -rf {} +
	@find . -name '*.egg-info' -exec rm -fr {} +

type-check: ## check code for typing errors
	@poetry run mypy rocket_args

lint: ## check code style with flake8
	@poetry run flake8 rocket_args tests

coverage: ## check code coverage
	@poetry run coverage run --source rocket_args --module pytest
	@poetry run coverage html
	@xdg-open htmlcov/index.html

test: ## run fast tests using pytest
	@poetry run pytest tests

test-all: ## run tests against different python versions using tox
	@poetry run tox

test-all-fast: ## run tests against different python versions using tox in parallel
	@poetry run tox -p all

docs: ## build docs and launch them with live-reload
	@poetry run mkdocs serve

dist: ## builds source and wheel package
	@poetry build
