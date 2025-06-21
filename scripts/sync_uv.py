#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Syncs dependencies with uv and checks for any inconsistencies.
"""

import os
import subprocess
import sys

# Add project root to PYTHONPATH so we can import scripts.utils when running standalone
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from scripts.utils import ensure_uv, init_uv_project, run_uv

if __name__ == "__main__":
    # Initialize project and ensure uv is installed
    ensure_uv()
    init_uv_project()

    # Sync dependencies with detailed output
    print("Syncing dependencies...")
    run_uv("sync --verbose")

    # Show installed packages
    print("\nInstalled packages:")
    run_uv("pip list")

    # Check uv.lock is in sync with pyproject.toml
    try:
        run_uv("lock --check")
    except subprocess.CalledProcessError:
        print("Lockfile out of sync – consider running update_uv.py to regenerate it.")
