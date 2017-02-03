# Default tests run with make test and make quick-tests
NOSE_TESTS?=tests galaxy_utils
# Default environment for make tox
ENV?=py27
# Extra arguments supplied to tox command
ARGS?=
# Location of virtualenv used for development.
VENV?=.venv
# Open resource on Mac OS X or Linux
OPEN_RESOURCE=bash -c 'open $$0 || xdg-open $$0'
# Source virtualenv to execute command (flake8, sphinx, twine, etc...)
IN_VENV=if [ -f $(VENV)/bin/activate ]; then . $(VENV)/bin/activate; fi;
# TODO: add this upstream as a remote if it doesn't already exist.
UPSTREAM?=galaxyproject
SOURCE_DIR?=galaxy_utils
BUILD_SCRIPTS_DIR=scripts
VERSION?=$(shell python $(BUILD_SCRIPTS_DIR)/print_version_for_release.py $(SOURCE_DIR))
# TODO: get a RTD
DOC_URL?=https://galaxy_utils.readthedocs.org
PROJECT_URL?=https://github.com/galaxyproject/sequence_utils
PROJECT_NAME?=sequence_utils
TEST_DIR?=tests
DOCS_DIR?=docs
ITEM?=

.PHONY: clean-pyc clean-build docs clean

help:
	@egrep '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

install: ## install into Python envirnoment
	python setup.py install

setup-venv: ## setup a development virutalenv in current directory
	if [ ! -d $(VENV) ]; then virtualenv $(VENV); exit; fi;
	$(IN_VENV) pip install -r requirements.txt && pip install -r dev-requirements.txt

setup-git-hook-lint: ## setup precommit hook for linting project
	cp $(BUILD_SCRIPTS_DIR)/pre-commit-lint .git/hooks/pre-commit

setup-git-hook-lint-and-test: ## setup precommit hook for linting and testing project
	cp $(BUILD_SCRIPTS_DIR)/pre-commit-lint-and-test .git/hooks/pre-commit

flake8: ## check style using flake8 for current Python (faster than lint)
	$(IN_VENV) flake8 $(SOURCE_DIR)  $(TEST_DIR)

lint: ## check style using tox and flake8 for Python 2 and Python 3
	$(IN_VENV) tox -e py27-lint && tox -e py34-lint

lint-readme: ## check README formatting for PyPI
	$(IN_VENV) python setup.py check -r -s

test: ## run tests with the default Python (faster than tox)
	$(IN_VENV) nosetests $(NOSE_TESTS)

tool-tests: ## Run tools-devteam tool tests against library in current state
	bash tests/planemo_test.bash

tox: ## run tests with tox in the specified ENV, defaults to py27
	$(IN_VENV) tox -e $(ENV) -- $(ARGS)

_coverage-report: ## build coverage report with the default Python
	coverage run --source $(SOURCE_DIR) setup.py $(TEST_DIR)
	coverage report -m
	coverage html

_open-coverage: ## open coverage report using open
	open htmlcov/index.html || xdg-open htmlcov/index.html

coverage: _coverage-report open-coverage ## check code coverage quickly with the default Python

open-history:  # view HISTORY.rst as HTML.
	rst2html HISTORY.rst > /tmp/seq_util_history.html
	$(OPEN_RESOURCE) /tmp/seq_util_history.html

ready-docs:  ## rebuild docs folder ahead of running docs or lint-docs
	rm -f $(DOCS_DIR)/$(SOURCE_DIR).rst
	rm -f $(DOCS_DIR)/modules.rst
	$(IN_VENV) sphinx-apidoc -f -o $(DOCS_DIR)/ $(SOURCE_DIR) $(SOURCE_DOC_EXCLUDE)

docs: ready-docs ## generate Sphinx HTML documentation, including API docs
	$(IN_VENV) $(MAKE) -C $(DOCS_DIR) clean
	$(IN_VENV) $(MAKE) -C $(DOCS_DIR) html

lint-docs: ready-docs
	$(IN_VENV) $(MAKE) -C $(DOCS_DIR) clean
	$(IN_VENV) $(MAKE) -C $(DOCS_DIR) html 2>&1 | python $(BUILD_SCRIPTS_DIR)/lint_sphinx_output.py

_open-docs:
	$(OPEN_RESOURCE) $(DOCS_DIR)/_build/html/index.html

open-docs: docs _open-docs ## generate Sphinx HTML documentation and open in browser

open-rtd: docs ## open docs on readthedocs.org
	$(OPEN_RESOURCE) $(PROJECT_URL)

open-project: ## open project on github
	$(OPEN_RESOURCE) $(PROJECT_URL)

dist: clean ## package
	$(IN_VENV) python setup.py sdist bdist_egg bdist_wheel
	ls -l dist

release-test-artifacts: dist ## Package and Upload to Test PyPi
	$(IN_VENV) twine upload -r test dist/*
	$(OPEN_RESOURCE) https://testpypi.python.org/pypi/$(PROJECT_NAME)

release-aritfacts: release-test-artifacts ## Package and Upload to PyPi
	@while [ -z "$$CONTINUE" ]; do \
		read -r -p "Have you executed release-test and reviewed results? [y/N]: " CONTINUE; \
	done ; \
	[ $$CONTINUE = "y" ] || [ $$CONTINUE = "Y" ] || (echo "Exiting."; exit 1;)
	@echo "Releasing"
	$(IN_VENV) twine upload dist/*

commit-version: ## Update version and history, commit.
	$(IN_VENV) python $(BUILD_SCRIPTS_DIR)/commit_version.py $(SOURCE_DIR) $(VERSION)

new-version: ## Mint a new version
	$(IN_VENV) python $(BUILD_SCRIPTS_DIR)/new_version.py $(SOURCE_DIR) $(VERSION)

release-local: commit-version release-aritfacts new-version

push-release: ## Push a tagged release to github
	git push $(UPSTREAM) master
	git push --tags $(UPSTREAM)

release: release-local push-release ## package, review, and upload a release

add-history: ## Reformat HISTORY.rst with data from Github's API
	$(IN_VENV) python $(BUILD_SCRIPTS_DIR)/bootstrap_history.py $(ITEM)
