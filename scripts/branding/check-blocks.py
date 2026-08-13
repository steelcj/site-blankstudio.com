#!/usr/bin/env python3
"""Check every extracted block against the source lines it claims to be a copy of.

A block library is copies, not imports: `branding/_original.com/blocks/
method/step-list.njk` is a slice of `src/pages/index.njk`, and nothing
keeps the two in step. Each file records its provenance in its own header —

    Copied from   src/pages/index.njk lines 184-231, at repo version 0.2.1

— and this reads that line back, re-slices the source, and compares. A file that
no longer matches is either a block that has been edited on purpose (re-stamp it,
or drop the claim) or a source that has moved on without the copy (re-extract).

Exits non-zero if anything has drifted, so it can gate a release.

Usage:
    python3 scripts/branding/check-blocks.py [--quiet]
    npm run check:blocks
"""

from __future__ import annotations

import argparse
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BRANDING = os.path.join(ROOT, "branding")

# "Copied from   src/pages/index.njk lines 12-51, at repo version 0.2.1"
CLAIM = re.compile(r"Copied from\s+(\S+) lines (\d+)-(\d+)")

# Where the header comment ends, per file type. Everything after it is the slice.
FENCES = {".njk": "#}\n", ".css": " */\n"}


def block_dirs() -> list:
    """Every blocks/ directory under branding/, active client or parked."""
    return sorted(glob.glob(os.path.join(BRANDING, "*", "blocks")))


def source_slice(relpath: str, start: int, end: int) -> str:
    with open(os.path.join(ROOT, relpath), encoding="utf-8") as fh:
        return "".join(fh.readlines()[start - 1 : end])


def check(path: str) -> str:
    """"" when the file matches its claim, else why it does not."""
    with open(path, encoding="utf-8") as fh:
        text = fh.read()

    claim = CLAIM.search(text)
    if not claim:
        return "no provenance header"

    relpath, start, end = claim.group(1), int(claim.group(2)), int(claim.group(3))
    if not os.path.exists(os.path.join(ROOT, relpath)):
        return f"source {relpath} no longer exists"

    fence = FENCES.get(os.path.splitext(path)[1])
    if not fence or fence not in text:
        return "header comment is not closed as expected"

    if text.split(fence, 1)[1] != source_slice(relpath, start, end):
        return f"differs from {relpath} lines {start}-{end}"
    return ""


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify extracted blocks against their sources.")
    parser.add_argument("--quiet", action="store_true", help="print only failures")
    args = parser.parse_args()

    roots = block_dirs()
    if not roots:
        print("[check:blocks] no branding/*/blocks/ directory; nothing to check.")
        return 0

    checked = drifted = 0
    for root in roots:
        for dirpath, _, names in os.walk(root):
            for name in sorted(names):
                if os.path.splitext(name)[1] not in FENCES:
                    continue
                path = os.path.join(dirpath, name)
                rel = os.path.relpath(path, ROOT)
                checked += 1
                problem = check(path)
                if problem:
                    drifted += 1
                    print(f"[check:blocks] DRIFTED {rel} — {problem}")

    if drifted:
        print(
            f"[check:blocks] {drifted} of {checked} block file(s) no longer match their "
            "source. Re-extract them, or update the header if the change was deliberate."
        )
        return 1

    if not args.quiet:
        print(f"[check:blocks] {checked} block file(s) match their source exactly.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
