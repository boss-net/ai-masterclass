#!/bin/bash

# Common utility functions for dev scripts

# Get project root directory
get_project_root() {
    local script_dir=$(dirname "$(realpath "$0")")
    echo "$(dirname "$script_dir")"
}

# Check and install uv if not present
ensure_uv() {
    if ! command -v uv &> /dev/null; then
        echo "Installing uv ..."
        pip install -q uv
    fi
}

# Initialize uv project if not initialized
init_uv_project() {
    local project_root=$(get_project_root)
    if [ ! -f "$project_root/uv.lock" ]; then
        echo "Initializing uv project ..."
        cd "$project_root"
        uv init --project bosskit
    fi
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
