# Contributing to AI Content API

Thank you for your interest in contributing! Here's how to get started.

## Development Setup

```bash
# Clone the repository
git clone https://github.com/brolyroly007/ai-content-api.git
cd ai-content-api

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install dev dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run tests
pytest tests/ -v
```

## Code Style

- We use **Ruff** for linting and formatting
- Run `ruff check .` before committing
- Run `ruff format .` to auto-format
- Pre-commit hooks will catch most issues automatically

## Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run `pytest tests/ -v` to ensure tests pass
5. Run `ruff check .` to ensure linting passes
6. Commit your changes
7. Push to your fork
8. Open a Pull Request

## Adding a New Template

Templates are defined in `templates/registry.py`. To add a new one:

1. Create a `ContentTemplate` with a unique `id`
2. Define the input `fields` with appropriate types
3. Write a clear `system_prompt` and `user_prompt_template`
4. Register it with `_register()`

## Adding a New Provider

1. Create a new file in `providers/` (e.g., `anthropic_provider.py`)
2. Implement the `BaseProvider` interface (`generate`, `stream`, `is_available`)
3. Register it in `providers/__init__.py`
4. Add config fields in `config.py`

## Reporting Issues

Use the [GitHub Issues](https://github.com/brolyroly007/ai-content-api/issues) page.
