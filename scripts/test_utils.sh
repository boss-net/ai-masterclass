#!/bin/bash

# Source the utility functions
source scripts/utils.sh

# Test getting project root
echo "Project root: $(get_project_root)"

# Test uv installation
echo "Testing uv installation..."
ensure_uv

# Test uv project initialization
echo "Testing uv project initialization..."
init_uv_project

# Test virtual environment creation
echo "Testing virtual environment creation..."
create_venv

# Test development dependencies installation
echo "Testing development dependencies installation..."
install_dev_deps

# Test pre-commit
echo "Testing pre-commit..."
run_pre_commit

# Test running tests
echo "Testing tests..."
run_tests

# Test building documentation
echo "Testing documentation build..."
build_docs

# Test cleaning build artifacts
echo "Testing clean build..."
clean_build

# Show help message
echo "Testing help message..."
show_help
