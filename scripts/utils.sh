#!/bin/bash

# Common utility functions for dev scripts

# Get project root directory
get_project_root() {
    local script_dir=$(dirname "$(cd "$(dirname "$0")" && pwd)")
    echo "$(cd "$script_dir" && pwd)"
}

# Check and install uv if not present
ensure_uv() {
    if ! command -v uv &> /dev/null; then
        echo "Installing uv ..."
        python3 -m pip install -q uv
        # Add uv to PATH if needed
        export PATH="$HOME/Library/Python/3.8/bin:$PATH"
    fi
    # Verify installation
    if ! command -v uv &> /dev/null; then
        echo "Error: Failed to install uv. Please check Python and pip installation."
        return 1
    fi
}

# Initialize uv project if not initialized
init_uv_project() {
    local project_root=$(get_project_root)
    echo "Initializing uv project in $project_root..."
    if command -v uv &> /dev/null; then
        uv init
    else
        echo "Error: uv is not installed. Please run ensure_uv() first."
        return 1
    fi
}

# Create and activate virtual environment
create_venv() {
    local venv_dir=".venv"
    echo "Creating virtual environment in $venv_dir..."
    python3 -m venv "$venv_dir"
    source "$venv_dir/bin/activate"
    echo "Virtual environment activated."
}

# Install development dependencies
install_dev_deps() {
    echo "Installing development dependencies..."
    python3 -m pip install -q -r requirements/requirements-dev.txt
}

# Run pre-commit checks
run_pre_commit() {
    echo "Running pre-commit checks..."
    pre-commit run --all-files
}

# Run tests with coverage
run_tests() {
    echo "Running tests with coverage..."
    python3 -m pytest tests/ --cov=bosskit
}

# Generate documentation
build_docs() {
    echo "Building documentation..."
    if [ ! -d "docs/_build" ]; then
        mkdir -p docs/_build
    fi
    cd docs && make html
}

# Clean build artifacts
clean_build() {
    echo "Cleaning build artifacts..."
    find . -name "__pycache__" -type d -exec rm -rf {} +
    find . -name "*.pyc" -type f -exec rm -f {} +
    rm -rf .pytest_cache
    rm -rf .mypy_cache
    rm -rf .coverage
    rm -rf build
    rm -rf dist
    rm -rf *.egg-info
}

# Show help message
show_help() {
    echo "Usage: $0 <command>"
    echo
    echo "Available commands:"
    echo "  create_venv     Create and activate virtual environment"
    echo "  install_dev_deps Install development dependencies"
    echo "  run_pre_commit  Run pre-commit checks"
    echo "  run_tests       Run tests with coverage"
    echo "  build_docs      Build documentation"
    echo "  clean_build     Clean build artifacts"
    echo "  help            Show this help message"
}

# Run uv command with error handling
run_uv() {
    local cmd="$@"
    echo "Running: $cmd"
    if ! eval "$cmd"; then
        echo "Error: uv command failed"
        exit 1
    fi
}

# Export functions for sourcing
export -f get_project_root
export -f ensure_uv
export -f init_uv_project
export -f run_uv
