# fastapi-tortoise-pytest-demo

Async Test Demo for FastAPI+Tortoise-orm+Pytest
- Python3.9+ is required

#### Install Dependencies

```bash
pdm deps
# Or by pip:
#python -m venv .venv && source .venv/bin/activate
#pip install -U pip && pip install --group dev -e .
```

#### Run Test

```bash
pdm test
# Or:
#coverage run -m pytest -s && coverage report --omit="tests/*" -m
```

#### Report coverage

```bash
pdm report
```
