#!/usr/bin/env python3
"""Start a new client by stamping branding/<client>/ from branding/_template/.

Copies the template branding directory — brand.yaml, fonts.yaml, site.yaml, and
the assets guide — to a new directory named for the client, ready to fill in.
The generators (build-brand.py, fetch-fonts.py) then discover it automatically,
since they pick the one directory under branding/ that is not '_'-prefixed.

Usage:
    python3 scripts/branding/new-client.py <client>
    npm run new-client -- <client>            # e.g. clientbrand.com

Refuses if the target already exists (a client is never overwritten) or if the
name is reserved (starts with '_'). Warns if another active client is already
present, because the build expects exactly one.
"""

from __future__ import annotations

import glob
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BRANDING = os.path.join(ROOT, "branding")
TEMPLATE = os.path.join(BRANDING, "_template")


def fail(msg: str) -> None:
    print(f"[new-client] {msg}", file=sys.stderr)
    sys.exit(1)


def active_clients() -> list:
    return [
        os.path.basename(d)
        for d in glob.glob(os.path.join(BRANDING, "*"))
        if os.path.isdir(d) and not os.path.basename(d).startswith("_")
    ]


def main() -> int:
    args = sys.argv[1:]
    if len(args) != 1 or not args[0].strip():
        print(__doc__)
        return 1
    name = args[0].strip().strip("/")

    if name.startswith("_"):
        fail(f"'{name}' is reserved — names starting with '_' are templates, not clients.")
    if "/" in name or os.sep in name:
        fail(f"'{name}' must be a single directory name, not a path.")
    if not os.path.isdir(TEMPLATE):
        fail("branding/_template/ not found; nothing to copy from.")

    target = os.path.join(BRANDING, name)
    if os.path.exists(target):
        fail(f"branding/{name}/ already exists; refusing to overwrite it.")

    existing = [c for c in active_clients() if c != name]
    if existing:
        print(f"[new-client] warning: an active client is already present "
              f"({', '.join(sorted(existing))}). The build expects exactly one, "
              f"so remove or '_'-prefix the other before building.")

    shutil.copytree(TEMPLATE, target)
    os.makedirs(os.path.join(target, "assets"), exist_ok=True)

    print(f"[new-client] created branding/{name}/ from _template.")
    print("Next:")
    print(f"  1. Fill in branding/{name}/brand.yaml, fonts.yaml, and site.yaml (replace the TODO values).")
    print(f"  2. Add the brand images to branding/{name}/assets/ (see its README.md for the slots).")
    print( "  3. Regenerate and validate:  npm run build:fonts && npm run build")
    return 0


if __name__ == "__main__":
    sys.exit(main())
