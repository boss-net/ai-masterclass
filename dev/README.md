# Development Scripts

This directory contains utility scripts for development tasks using `uv` (Universal Virtualenv).

## Scripts

- `update-uv`: Updates dependencies and checks lockfile sync
- `sync-uv`: Synchronizes dependencies from lockfile
- `reformat`: Runs code formatting tools (ruff, black, isort)
- `mypy-check`: Performs type checking with mypy

## Usage

1. Ensure you have Python 3.8+ installed
2. Run any script with:
   ```bash
   ./dev/script-name
   ```

## Features

- Automatic uv installation if not present
- Project initialization if needed
- Detailed output and error handling
- Integration with pyproject.toml configuration
- Dependency graph visualization
- Outdated package checking

## Requirements

- Python 3.8+
- uv (will be installed automatically if not present)
- pyproject.toml configuration
