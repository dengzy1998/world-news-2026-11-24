#!/usr/bin/env python3
"""Entrypoint for the news-image-20261124 entry (standard library only).

Copies the pre-rendered poster (entry.png, produced by render_poster.py
from the sourced 24 November 2026 stories ledger) to
$MAKEFUN_OUTPUT_DIR/entry.png. No network, no extra packages.
"""
import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, os.path.join(out_dir, "entry.png"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
