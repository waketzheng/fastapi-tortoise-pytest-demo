# fastapi-tortoise-pytest-demo

Async Test Demo for FastAPI+TortoiseORM+Pytest
- Python3.10+ is required

#### Install Dependencies

```bash
just deps
# Or by pip:
#python -m venv .venv && source .venv/bin/activate
#pip install -U pip && pip install --group dev -e .
```

#### Run Test

```bash
just test
# Or:
#coverage run -m pytest -s && coverage report --omit="tests/*" -m
```

#### Report coverage

```bash
just report
```
