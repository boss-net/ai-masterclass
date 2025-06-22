#!/usr/bin/env python

# Update dependencies in bosskit project using uv
import os
import subprocess
import sys

# Add project root to PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

# Import from scripts module
from scripts.utils import ensure_uv, init_uv_project, run_uv

# Initialize project and ensure uv is installed
ensure_uv()

# Skip project initialization if it's already initialized
project_root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
pyproject_path = os.path.join(project_root, "pyproject.toml")
if not os.path.exists(pyproject_path):
    print(f"Initializing uv project in {project_root}...")
    init_uv_project()
else:
    print(f"Using existing pyproject.toml at {pyproject_path}")

# Update dependencies with detailed output
try:
    print("\nUpdating dependencies...")
    run_uv("add --verbose --no-lock -r requirements/requirements.txt")
    run_uv("add --verbose --no-lock -r requirements/requirements-dev.txt")
    run_uv("add --verbose --no-lock -r requirements/requirements-test.txt")
    run_uv("lock --verbose")
except subprocess.CalledProcessError as e:
    print(f"Warning: Failed to update dependencies: {e}")

# Check lockfile sync
try:
    print("\nChecking lockfile sync...")
    run_uv("lock --check")
except subprocess.CalledProcessError as e:
    print(f"Warning: Failed to check lockfile sync: {e}")

# Show dependency tree
try:
    print("\nShowing dependency tree...")
    run_uv("tree")
except subprocess.CalledProcessError as e:
    print(f"Warning: Failed to show dependency tree: {e}")

# Show outdated packages
try:
    print("\nChecking for outdated packages...")
    run_uv("pip list --outdated")
except subprocess.CalledProcessError as e:
    print(f"Warning: Failed to check outdated packages: {e}")
