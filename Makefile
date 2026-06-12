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
	@just up
	uvx prek autoupdate

lock:
	uv lock

venv:
	@just venv $(options) $(version)

venv39:
	$(MAKE) venv version=3.9

deps:
	@just deps $(options)

start:
	uvx prek install
	$(MAKE) deps

_style:
	@just _style
style: deps _style

_check:
	@just _check
check: deps _check

_lint:
	@just _lint
lint: deps _lint

_test:
	@just _test
	@just report
test: deps _test
