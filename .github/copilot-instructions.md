# Copilot Instructions

## Commands

```bash
uv sync --all-groups              # install deps
uv run pytest -m "not integration"           # unit tests only (no external services)
uv run pytest tests/test_flask.py::test_index  # single test
uv run pytest -m integration                 # requires GOOGLE_CLOUD_PROJECT + Firestore
uv run ruff check .
uv run ruff format .
```

## Conventions

- **Tests**: No marker = unit test, no external deps. `@pytest.mark.integration` = requires live Firestore and network. Fixtures skip via `pytest.skip()` when `GOOGLE_CLOUD_PROJECT` is unset. `conftest.py` calls `load_dotenv()` — use a `.env` file for local dev.
- **`asyncio_mode = "auto"`**: Do not add `@pytest.mark.asyncio` to individual async tests; pytest-asyncio picks them up automatically.
- **All runtime config comes from Firestore**, not environment variables. The only env var is `GOOGLE_CLOUD_PROJECT`. Adding new config means adding a field to the `parameter/param_1` Firestore document and a corresponding `@property` in `configuration.py`.
- **Ruff**: line-length 120, rules E/F/I/UP. Use Python 3.14+ syntax (`X | Y` unions, `list[X]`, walrus operator, etc.).
