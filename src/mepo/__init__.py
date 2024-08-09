"""Ensure Python version"""

import sys

PY_VERSION = (3, 9, 0)
if sys.version_info < PY_VERSION:
    sys.exit(f"ERROR: Python version needs to be >= {PY_VERSION}")
