#!/usr/bin/env -S just --justfile
# ^ A shebang isn't required, but allows a justfile to be executed
#   like a script, with `./justfile lint`, for example.
# Use powershell for Windows so that 'Git Bash' and 'PyCharm Terminal' get the same result

set windows-shell := ["powershell.exe", "-NoLogo", "-Command"]

VENV_CREATE := "uvx pdm venv create --with-pip"
PY_EXEC := if os_family() == "windows" { ".venv/Scripts/python.exe" } else { ".venv/bin/python" }

default:
    @just --list

_uv_venv *args:
    {{ VENV_CREATE }} --with uv {{ args }}

_win_venv *args:
    if (Test-Path '~/AppData/Roaming/uv/tools/rust-just') { just _uv_venv {{ args }}} else { {{ VENV_CREATE }} {{ args }}}

[unix]
venv *args:
    @if test ! -e .venv; then just _uv_venv {{ args }}; fi
[windows]
venv *args:
    @if (-Not (Test-Path '.venv')) { just _win_venv {{ args }}}

_pypi *args:
    @just fast pypi --quiet

up *args: venv
    @just _pypi --reverse
    uv lock --upgrade {{ args }}
    @just _uv_deps {{ args }}
    @just _pypi

_uv_deps *args:
    uv sync --all-extras --all-groups {{ args }}

# Install dependencies
deps options="" *args: venv
    @just _pypi --reverse
    @just _uv_deps {{ options }} {{ args }}
    @just _pypi

add *args: venv
    @just _pypi --reverse
    uv add {{ args }}
    @just _pypi

shell *args: venv
    uv run --no-sync tortoise shell {{ args }}

# Runserver
dev *args:
    uv run --no-sync app/main.py {{ args }}

_style *args:
    just _ruff format {{ args }}
    just _ruff check --fix {{ args }}

_ruff command *args:
    uvx ruff {{ command }} {{ args }}

style: deps _style

_codeqc:
    uvx ty check
    uv run --no-sync mypy app
    uvx pyright --pythonpath={{PY_EXEC}} app

codeqc: deps _codeqc

_check:
    just _ruff format --check
    just _ruff check
    just _codeqc

check: deps _check

_lint: _style _codeqc

lint: deps _lint

_test *args:
    uv run --no-sync coverage run -m pytest {{ args }}
test *args: deps _test

report:
    uv run --no-sync coverage report -m

fast command *args:
    uvx --from fast-dev-cli fast {{ command }} {{ args }}

version part="patch" *args:
    @just fast bump {{ part }} {{ args }}

bump *args:
    @just version patch --commit {{ args }}

tag *args:
    @just fast tag {{ args }}

# Bump version with patch part(0.1.1->0.1.2) and auto mark tag
release: venv bump tag
    git --no-pager log -1

# Bump version with minor part(0.1.1->0.2.0) and auto mark tag
minor *args:
    @just version minor --commit {{ args }}
    git --no-pager log -1
    @just tag
