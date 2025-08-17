help:
	@echo  "Asynctor development makefile"
	@echo
	@echo  "Usage: make <target>"
	@echo  "Targets:"
	@echo  "    up      Updates dev/test dependencies"
	@echo  "    deps    Ensure dev/test dependencies are installed"
	@echo  "    check   Checks that build is sane"
	@echo  "    test    Runs all tests"
	@echo  "    style   Auto-formats the code"
	@echo  "    lint    Auto-formats the code and check type hints"
	@echo  "    build   Build wheel file and tar file from source to dist/"

up:
	uv lock --upgrade
	$(MAKE) deps options=--frozen
	pre-commit autoupdate

lock:
	uv lock

venv:
	pdm venv create $(options) $(version)

venv39:
	$(MAKE) venv version=3.9

deps:
	uv sync --all-extras --all-groups --inexact $(options)

start:
	pre-commit install
	$(MAKE) deps

_style:
	ruff format
	ruff check --fix
style: deps _style

_check:
	ruff format --check
	ruff check
	mypy .
check: deps _check

_lint:
	$(MAKE) _style
	mypy .
lint: deps _lint

_test:
	coverage run -m pytest
	coverage report -m
test: deps _test
