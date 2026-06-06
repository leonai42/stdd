"""STDD main entry point for `python -m stdd`.

This module enables `python -m stdd` to work, which is more reliable
than relying on the `stdd` bash wrapper being in PATH (especially in
non-interactive shells used by Claude Code hooks).
"""

import sys
import os

# Ensure the parent dir is on sys.path so imports work
_STDD_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _STDD_ROOT not in sys.path:
    sys.path.insert(0, _STDD_ROOT)

# Also ensure the bin/ dir is discoverable if running from source
_bin_dir = os.path.join(_STDD_ROOT, "bin")
if _bin_dir not in sys.path:
    sys.path.insert(0, _bin_dir)

from stdd.cli import main

if __name__ == "__main__":
    main()
