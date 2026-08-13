#!/usr/bin/env python3
"""Validate the active client's branding config before a build.

Fails the build when the client's declarations are incomplete, so a
half-configured site cannot ship. This is the branding counterpart to
scripts/check-untranslated.js (npm run check:i18n): the templates assume the
required fields are present, and this script is what guarantees it.

Errors (exit 1, fail the build):
  - not exactly one active branding/<client>/ directory
  - brand.yaml is missing a colour token that src/css/home.css consumes
  - site.yaml is missing name, url, publicationTimeZone, or contact.email
  - a required value is still a template placeholder (TODO / example.com / …),
    i.e. the client was scaffolded but not filled in

Warnings (reported, do not fail the build):
  - a file site.yaml's `logos` block points at is absent from the client's
    assets directory

Optional fields (phone numbers, social accounts) are not required: the footer
and contact page render whatever is present, so their absence is never an error.

Dependency: PyYAML. Standard library otherwise.
"""

from __future__ import annotations

import argparse
import glob
import os
import re
import shutil
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
# Kept as the fallback names only: what a client is actually checked against is
# whatever its site.yaml `logos` block publishes. See check_assets().
ASSET_SLOTS = ("favicon.png", "logo-lockup.png", "logo-lockup-dark.png")

# Markers left behind by branding/_template that mean "not filled in yet".
PLACEHOLDER_RE = re.compile(
    r"TODO|example\.com|555\s*000\s*0000|@example|Example Studio", re.IGNORECASE
)


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


# ── filling in what is missing ───────────────────────────────────────────────

# The values this script refuses to build without, in the order it asks for
# them: (dotted key, prompt, hint, validator).
REQUIRED = [
    ("name", "Site name", "the entity in the copyright line, e.g. Vishpala",
     lambda v: len(v) > 1),
    ("url", "Site URL", "e.g. https://vishpala.com",
     lambda v: v.startswith("http://") or v.startswith("https://")),
    ("contact.email", "Contact email", "e.g. hello@vishpala.com",
     lambda v: "@" in v and "." in v.split("@")[-1]),
    ("publicationTimeZone", "Publication time zone", "e.g. America/Toronto",
     lambda v: "/" in v),
]


def set_value(text: str, dotted: str, value: str) -> str:
    """Write one value into site.yaml, leaving the rest of the file alone.

    Edited line by line rather than round-tripped through the YAML parser,
    because the file is more comment than data — every block explains itself to
    whoever fills it in next, and a dump would throw all of that away.
    """
    line_re = {
        "name": r"^(name:).*$",
        "url": r"^(url:).*$",
        "publicationTimeZone": r"^(publicationTimeZone:).*$",
        # Indented, so it only matches the key inside the contact block.
        "contact.email": r"^(\s+email:).*$",
    }[dotted]

    replacement = f'\\1 "{value}"'
    new_text, count = re.subn(line_re, replacement, text, count=1, flags=re.MULTILINE)
    if count:
        return new_text

    # The key is not in the file at all — append it, nested if it needs to be.
    if dotted == "contact.email":
        return new_text.rstrip("\n") + f'\n\ncontact:\n  email: "{value}"\n'
    return new_text.rstrip("\n") + f'\n{dotted}: "{value}"\n'


def fill_in(client_dir: str, client: str) -> bool:
    """Ask for the required values that are absent or still placeholders.

    Only ever runs at a terminal. In CI, on Netlify, or under any other
    non-interactive build there is nobody to ask, so the checks below report the
    problem and fail as they always have — a build that pauses for input where
    no input can arrive is worse than one that stops with a reason.

    Creates site.yaml from the template first if the client has none.
    """
    path = os.path.join(client_dir, "site.yaml")

    if not os.path.isfile(path):
        template = os.path.join(ROOT, "branding", "_template", "site.yaml")
        if not os.path.isfile(template):
            return False
        shutil.copyfile(template, path)
        print(f"[check:brand] branding/{client}/site.yaml did not exist; "
              "started one from branding/_template/site.yaml.")

    with open(path, "r", encoding="utf-8") as fh:
        text = fh.read()
    cfg = yaml.safe_load(text) or {}

    def current(dotted):
        node = cfg
        for part in dotted.split("."):
            node = (node or {}).get(part) if isinstance(node, dict) else None
        return node

    wanted = [r for r in REQUIRED if not current(r[0]) or _placeholder(current(r[0]))]
    if not wanted:
        return False

    print(f"\n[check:brand] branding/{client}/site.yaml needs "
          f"{len(wanted)} value(s) before this site can build.\n")

    filled = 0
    for dotted, label, hint, valid in wanted:
        while True:
            try:
                answer = input(f"  {label} ({hint}): ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                return filled > 0
            if not answer:
                print("    skipped — the build will stop on this one.")
                break
            if not valid(answer):
                print(f"    that does not look like a {label.lower()}; try again.")
                continue
            text = set_value(text, dotted, answer)
            filled += 1
            break

    if filled:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
        print(f"\n[check:brand] wrote {filled} value(s) into branding/{client}/site.yaml.")
    return filled > 0


def check_site_yaml(client_dir: str, errors: list) -> dict:
    """Validate site.yaml, and hand it back so the asset check can read it."""
    path = os.path.join(client_dir, "site.yaml")
    if not os.path.isfile(path):
        errors.append("site.yaml is missing.")
        return {}
    with open(path, "r", encoding="utf-8") as fh:
        cfg = yaml.safe_load(fh) or {}

    checks = {
        "name": cfg.get("name"),
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

    return cfg


def check_assets(client_dir: str, site_cfg: dict, warnings: list) -> None:
    """Check the files the client's own site.yaml points at.

    The slots were once fixed .png names, which meant a client shipping SVG
    marks — as this template's `logos` block has allowed since site.yaml gained
    one — was warned about three files it had deliberately not created, while a
    genuinely missing SVG went unmentioned. What matters is whether the paths
    site.yaml publishes actually resolve to a file in this client's assets/.
    """
    assets_dir = os.path.join(client_dir, "assets")
    logos = (site_cfg or {}).get("logos") or {}

    # Falls back to the .png slots the generator itself defaults to, so a client
    # that declares no logos block is still checked against what will be served.
    declared = {
        "dark": logos.get("dark", "/assets/logo-lockup-dark.png"),
        "light": logos.get("light", "/assets/logo-lockup.png"),
        "favicon": logos.get("favicon", "/assets/favicon.png"),
    }

    for slot, url in declared.items():
        name = url.split("/assets/", 1)[-1] if "/assets/" in url else url.lstrip("/")
        if not os.path.isfile(os.path.join(assets_dir, name)):
            warnings.append(
                f"site.yaml names {slot} as {url}, but assets/{name} does not exist"
            )


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate the active client's branding config.")
    ap.add_argument("--no-prompt", action="store_true",
                    help="never ask for missing values, even at a terminal")
    args = ap.parse_args()

    client_dir = find_client_dir()
    client = os.path.basename(client_dir)

    # Ask before reporting: a value supplied now is one fewer error to print,
    # and the answer is written where it belongs rather than told to the user.
    if not args.no_prompt and sys.stdin.isatty():
        fill_in(client_dir, client)

    errors: list = []
    warnings: list = []

    check_brand_yaml(client_dir, errors)
    site_cfg = check_site_yaml(client_dir, errors)
    check_assets(client_dir, site_cfg, warnings)

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
