# Contributing

Thanks for helping improve `hybrid-cache`.

## Set Up

```bash
uv sync --all-groups
```

## Check Your Changes

Run the same checks used by CI:

```bash
uv run ruff check .
uv run ruff format --check .
uv run ty check
uv run pytest
uv build --no-sources
```

## Work on Documentation

The documentation site is built with Zensical.

```bash
uv run zensical serve
uv run zensical build --clean --strict
```

Documentation should stay focused on people using `hybrid-cache` in their applications. Follow the Diataxis structure in `docs/`: tutorials, how-to guides, reference, and explanation.

## Pull Requests

Keep pull requests focused on one change. Include tests for behavior changes, update documentation when user-facing behavior changes, and make sure the checks above pass before opening a PR.
