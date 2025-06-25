#!/usr/bin/env python3
"""
rename_pr_to_vr_recursive.py

Recursively search under art/src/vain_ranger for any files named pr_*,
and rename them in-place so the prefix becomes vr_ instead.
"""

import sys
from pathlib import Path

def rename_pr_to_vr(root_dir: Path):
    if not root_dir.exists() or not root_dir.is_dir():
        print(f"[!] {root_dir!r} does not exist or is not a directory.")
        return

    # rglob will walk into all subfolders
    for p in root_dir.rglob("pr_*"):
        if p.is_file():
            new_name = "vr_" + p.name[len("pr_"):]
            new_path = p.with_name(new_name)
            p.rename(new_path)
            print(f"Renamed: {p.relative_to(root_dir)} → {new_name}")

if __name__ == "__main__":
    # allow overriding the root directory from CLI
    if len(sys.argv) > 1:
        root = Path(sys.argv[1]).resolve()
    else:
        # default to art/src/vain_ranger relative to this script
        root = Path(__file__).parent / "src" / "vain_ranger"

    rename_pr_to_vr(root)
