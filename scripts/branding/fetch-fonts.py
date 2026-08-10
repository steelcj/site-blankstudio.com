#!/usr/bin/env python3
"""Download the website's webfonts locally from a single YAML declaration.

Reads the active client's `branding/<client>/fonts.yaml`, asks the Google Fonts
CSS2 API for the declared families/weights/styles as woff2, keeps only the
requested character subsets, writes each file into the configured fonts
directory, and generates the @font-face stylesheet that points at those local
files.

Why it works: the CSS2 API returns different formats depending on the requesting
browser. Send a modern Chrome User-Agent and it answers with woff2 @font-face
blocks, each preceded by a `/* <subset> */` comment and carrying a
gstatic.com download URL. We parse those blocks, filter by subset, download the
files, and rewrite each `src:` to the local path.

Client discovery: fonts.yaml is client-owned and lives in branding/<client>/,
named for the client. This script globs `branding/*/fonts.yaml`, ignores any
`_`-prefixed directory (branding/_template), and expects exactly one active
client. Output paths in fonts.yaml (src/assets/fonts, src/css/fonts.css) are
resolved from the repo root, NOT the config's directory, so the generated files
land in src/ even though the config now lives under branding/<client>/.

Usage:
    python3 scripts/branding/fetch-fonts.py               # discovers the client
    python3 scripts/branding/fetch-fonts.py path/to/fonts.yaml
    python3 scripts/branding/fetch-fonts.py --dry-run     # show what would happen

Dependency: PyYAML (`pip install pyyaml`). Standard library otherwise.

Re-run whenever a fonts.yaml changes, then commit the updated files.
"""

from __future__ import annotations

import argparse
import glob
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

try:
    import yaml
except ImportError:
    sys.exit(
        "This script needs PyYAML. Install it with:\n"
        "    pip install pyyaml\n"
        "(or: pip install --break-system-packages pyyaml on a managed system)"
    )

# scripts/branding/fetch-fonts.py -> repo root is three directories up. Output
# paths are resolved against this, so they land in src/ regardless of where the
# config file sits.
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# A real browser UA is required — without it the API returns legacy .ttf instead
# of woff2. This string just needs to look like a current Chrome.
BROWSER_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

CSS2_ENDPOINT = "https://fonts.googleapis.com/css2"

# One @font-face block, with the subset name from the comment immediately above
# it. re.DOTALL so the block body spans lines.
FACE_RE = re.compile(
    r"/\*\s*(?P<subset>[\w-]+)\s*\*/\s*@font-face\s*\{(?P<body>[^}]*)\}",
    re.DOTALL,
)


def find_client_config() -> str:
    """Return the one active client's fonts.yaml, or exit with a clear error.

    A directory whose name starts with '_' (branding/_template) is a seed and is
    skipped, so only a real client directory counts.
    """
    matches = [
        path
        for path in glob.glob(os.path.join(REPO_ROOT, "branding", "*", "fonts.yaml"))
        if not os.path.basename(os.path.dirname(path)).startswith("_")
    ]
    if not matches:
        sys.exit(
            "No client fonts.yaml found. Expected exactly one "
            "branding/<client>/fonts.yaml (directories starting with '_' are "
            "ignored)."
        )
    if len(matches) > 1:
        names = ", ".join(sorted(os.path.basename(os.path.dirname(m)) for m in matches))
        sys.exit(
            f"Ambiguous fonts config: found several client directories ({names}). "
            "Exactly one un-prefixed branding/<client>/ is allowed."
        )
    return matches[0]


def _field(body: str, name: str) -> str:
    """Pull a single declared value (e.g. font-weight) out of a @font-face body."""
    m = re.search(rf"{name}\s*:\s*([^;]+);", body)
    return m.group(1).strip() if m else ""


def slug(text: str) -> str:
    """'Inter Tight' -> 'inter-tight' for use in filenames."""
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def build_family_param(name: str, weights: list[int], styles: list[str]) -> str:
    """Assemble one CSS2 `family=` value from a family's requested permutations.

    Axis values in a CSS2 request must be listed in a strict order. With italics
    present the tuple form `ital,wght@0,400;1,400` is required (ital axis first,
    tuples sorted ascending); with normal only, the shorter `wght@400;500` form
    is used.
    """
    has_italic = any(s == "italic" for s in styles)
    family = name.replace(" ", "+")

    if has_italic:
        tuples = []
        for style in styles:
            ital = 1 if style == "italic" else 0
            for w in weights:
                tuples.append((ital, w))
        tuples.sort()
        axis = "ital,wght@" + ";".join(f"{i},{w}" for i, w in tuples)
    else:
        axis = "wght@" + ";".join(str(w) for w in sorted(weights))

    return f"{family}:{axis}"


def fetch_css(families: list[dict], display: str) -> str:
    """Request the combined CSS2 stylesheet for every declared family."""
    params = [("family", build_family_param(f["name"], f["weights"], f.get("styles", ["normal"])))
              for f in families]
    params.append(("display", display))
    # doseq keeps each family= as its own repeated key; safe=":;@,+" preserves the
    # axis punctuation the API expects rather than percent-encoding it.
    query = urllib.parse.urlencode(params, doseq=True, safe=":;@,+")
    url = f"{CSS2_ENDPOINT}?{query}"

    req = urllib.request.Request(url, headers={"User-Agent": BROWSER_UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        sys.exit(f"Google Fonts returned HTTP {e.code} for:\n  {url}\n"
                 "Check the family names and weights in fonts.yaml.")
    except urllib.error.URLError as e:
        sys.exit(f"Could not reach Google Fonts ({e.reason}). Are you online?")


def download(url: str, dest: str) -> int:
    """Fetch a font binary to dest; return bytes written."""
    req = urllib.request.Request(url, headers={"User-Agent": BROWSER_UA})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = resp.read()
    with open(dest, "wb") as fh:
        fh.write(data)
    return len(data)


def main() -> None:
    ap = argparse.ArgumentParser(description="Download the site's webfonts locally from fonts.yaml.")
    ap.add_argument("config", nargs="?", default=None,
                    help="path to the YAML declaration; if omitted, the active "
                         "branding/<client>/fonts.yaml is discovered")
    ap.add_argument("--dry-run", action="store_true",
                    help="report what would be downloaded without writing anything")
    args = ap.parse_args()

    config = args.config or find_client_config()
    if not os.path.isfile(config):
        sys.exit(f"Config not found: {config}")

    with open(config, "r", encoding="utf-8") as fh:
        cfg = yaml.safe_load(fh)

    if cfg.get("provider", "google") != "google":
        sys.exit(f"Unsupported provider: {cfg.get('provider')!r} (only 'google').")

    display = cfg.get("display", "swap")
    wanted_subsets = set(cfg.get("subsets", ["latin"]))
    families = cfg["families"]
    out = cfg["output"]

    # Outputs are resolved from the repo root, not the config's directory, so the
    # fonts and stylesheet land in src/ even though fonts.yaml lives under
    # branding/<client>/.
    fonts_dir = os.path.join(REPO_ROOT, out["fonts_dir"])
    css_file = os.path.join(REPO_ROOT, out["css_file"])
    css_href = out["css_href"].rstrip("/")

    print(f"Requesting {len(families)} families from Google Fonts "
          f"(subsets: {', '.join(sorted(wanted_subsets))})…")
    css = fetch_css(families, display)

    faces = list(FACE_RE.finditer(css))
    if not faces:
        sys.exit("No @font-face blocks parsed — the API response was unexpected.")

    if not args.dry_run:
        os.makedirs(fonts_dir, exist_ok=True)

    rules: list[str] = []
    kept = skipped = total_bytes = 0

    for m in faces:
        subset = m.group("subset")
        body = m.group("body")
        if subset not in wanted_subsets:
            skipped += 1
            continue

        family = _field(body, "font-family").strip("'\"")
        style = _field(body, "font-style") or "normal"
        weight = _field(body, "font-weight")
        urange = _field(body, "unicode-range")

        src_match = re.search(r"url\((https://[^)]+\.woff2)\)", body)
        if not src_match:
            skipped += 1
            continue
        remote_url = src_match.group(1)

        filename = f"{slug(family)}-{subset}-{weight}-{style}.woff2"
        dest = os.path.join(fonts_dir, filename)
        local_href = f"{css_href}/{filename}"

        if args.dry_run:
            print(f"  would fetch {family} {weight} {style} [{subset}] -> {filename}")
        else:
            size = download(remote_url, dest)
            total_bytes += size
            print(f"  {filename}  ({size // 1024} KB)")

        # unicode-range is preserved so the browser only downloads the subset it
        # actually needs for the text on the page.
        rule = (
            "@font-face {\n"
            f"  font-family: '{family}';\n"
            f"  font-style: {style};\n"
            f"  font-weight: {weight};\n"
            f"  font-display: {display};\n"
            f"  src: url('{local_href}') format('woff2');\n"
            + (f"  unicode-range: {urange};\n" if urange else "")
            + "}"
        )
        rules.append(rule)
        kept += 1

    header = (
        "/* GENERATED by scripts/branding/fetch-fonts.py from branding/<client>/fonts.yaml — do not edit by hand.\n"
        "   Re-run the script to regenerate. Self-hosted webfonts for the site as a\n"
        "   whole; the Infusion add-on's fonts live under assets/vendor/infusion/. */\n\n"
    )
    stylesheet = header + "\n\n".join(rules) + "\n"

    if args.dry_run:
        print(f"\nDry run: {kept} faces would be written to {out['fonts_dir']}, "
              f"{skipped} skipped. Stylesheet -> {out['css_file']}.")
        return

    os.makedirs(os.path.dirname(css_file), exist_ok=True)
    with open(css_file, "w", encoding="utf-8") as fh:
        fh.write(stylesheet)

    print(f"\nDone. {kept} files ({total_bytes // 1024} KB) in {out['fonts_dir']}, "
          f"{skipped} subsets skipped.")
    print(f"Wrote {out['css_file']} with {kept} @font-face rules.")


if __name__ == "__main__":
    main()
