#!/usr/bin/env python3
"""Validate the active client's branding config before a build.

Fails the build when the client's declarations are incomplete, so a
half-configured site cannot ship. This is the branding counterpart to
scripts/check-untranslated.js (npm run check:i18n): the templates assume the
required fields are present, and this script is what guarantees it.

Errors (exit 1, fail the build):
  - not exactly one active branding/<client>/ directory
  - brand.yaml is missing a colour token that src/css/home.css consumes
  - site.yaml is missing url, publicationTimeZone, or contact.email
  - a required value is still a template placeholder (TODO / example.com / …),
    i.e. the client was scaffolded but not filled in

Warnings (reported, do not fail the build):
  - a brand asset slot (favicon or a logo lockup) is absent from the client's
    assets directory

Optional fields (phone numbers, social accounts) are not required: the footer
and contact page render whatever is present, so their absence is never an error.

Dependency: PyYAML. Standard library otherwise.
"""

from __future__ import annotations

import glob
import os
import re
import sys

try:
    import yaml
except ImportError:
    sys.exit(
        "This script needs PyYAML. Install it with:\n"
        "    pip install pyyaml\n"
        "(or: pip install --break-system-packages pyyaml on a managed system)"
    )

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Every colour custom property src/css/home.css consumes through var(--…). A
# client that drops one of these leaves home.css referencing an undefined
# variable, so all of them are required.
REQUIRED_TOKENS = {
    "blue", "blue-bright", "beige",
    "bg", "bg-band", "ink", "ink-2", "card",
    "text", "text-dim", "text-mut", "on-dark", "on-dark-dim", "on-dark-mut",
    "line", "line-2", "line-dark",
}

# Brand image slots the template references by name (see the asset
# specification). Missing ones warn rather than fail, so a work-in-progress
# client still builds.
ASSET_SLOTS = ("favicon.png", "logo-lockup.png", "logo-lockup-dark.png")

# Markers left behind by branding/_template that mean "not filled in yet".
PLACEHOLDER_RE = re.compile(r"TODO|example\.com|555\s*000\s*0000|@example", re.IGNORECASE)


def find_client_dir() -> str:
    dirs = [
        d
        for d in glob.glob(os.path.join(ROOT, "branding", "*"))
        if os.path.isdir(d) and not os.path.basename(d).startswith("_")
    ]
    if not dirs:
        sys.exit("[check:brand] No client directory under branding/ (found none).")
    if len(dirs) > 1:
        names = ", ".join(sorted(os.path.basename(d) for d in dirs))
        sys.exit(f"[check:brand] Several client directories ({names}); exactly one is allowed.")
    return dirs[0]


def flatten_tokens(colors) -> set:
    """Collect every colour token name from the (possibly grouped) colors map."""
    names = set()
    if isinstance(colors, dict):
        for key, value in colors.items():
            if isinstance(value, dict):
                names.update(value.keys())
            else:
                names.add(key)
    return names


def check_brand_yaml(client_dir: str, errors: list) -> None:
    path = os.path.join(client_dir, "brand.yaml")
    if not os.path.isfile(path):
        errors.append("brand.yaml is missing.")
        return
    with open(path, "r", encoding="utf-8") as fh:
        cfg = yaml.safe_load(fh) or {}
    tokens = flatten_tokens(cfg.get("colors"))
    missing = REQUIRED_TOKENS - tokens
    if missing:
        errors.append(
            "brand.yaml is missing colour tokens home.css needs: "
            + ", ".join(sorted(missing))
        )


def _placeholder(value) -> bool:
    return isinstance(value, str) and bool(PLACEHOLDER_RE.search(value))


def check_site_yaml(client_dir: str, errors: list) -> None:
    path = os.path.join(client_dir, "site.yaml")
    if not os.path.isfile(path):
        errors.append("site.yaml is missing.")
        return
    with open(path, "r", encoding="utf-8") as fh:
        cfg = yaml.safe_load(fh) or {}

    checks = {
        "url": cfg.get("url"),
        "publicationTimeZone": cfg.get("publicationTimeZone"),
        "contact.email": (cfg.get("contact") or {}).get("email"),
    }
    for name, value in checks.items():
        if not value:
            errors.append(f"site.yaml is missing a required value: {name}.")
        elif _placeholder(value):
            errors.append(
                f"site.yaml {name} is still a template placeholder ({value!r}); "
                "fill it in for this client."
            )


def check_assets(client_dir: str, warnings: list) -> None:
    assets_dir = os.path.join(client_dir, "assets")
    for slot in ASSET_SLOTS:
        if not os.path.isfile(os.path.join(assets_dir, slot)):
            warnings.append(f"asset slot not found: assets/{slot}")


def main() -> int:
    client_dir = find_client_dir()
    client = os.path.basename(client_dir)

    errors: list = []
    warnings: list = []

    check_brand_yaml(client_dir, errors)
    check_site_yaml(client_dir, errors)
    check_assets(client_dir, warnings)

    for w in warnings:
        print(f"[check:brand] warning ({client}): {w}")

    if errors:
        print(f"\n[check:brand] {len(errors)} problem(s) in branding/{client}/:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        print("\nFill these in (or run the new-client scaffold) before building.", file=sys.stderr)
        return 1

    print(f"[check:brand] branding/{client}/ is complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
