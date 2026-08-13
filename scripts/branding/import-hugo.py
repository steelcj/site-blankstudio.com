#!/usr/bin/env python3
"""Import a Hugo site's content into a branding directory's seed.

The left-hand side of the pipeline. `import-hugo.py` reads a Hugo project and
writes `branding/<client>/content/`; `ingress.py` then pushes that seed into
`src/content/`, where the site builds from it. Import is Hugo -> branding, never
Hugo -> site, so nothing published changes until an ingress is run deliberately.

What it maps:

  content/<lang>/…            ->  <locale>/…            (locale-first, both ways)
  section/_index.md           ->  section/index.md      (the section's own page)
  section/page/index.md       ->  section/page/index.md (page bundles kept whole)
  [languages] in hugo.toml    ->  which locale directories exist

Front matter is carried through as authored — title, description, date, draft,
and any params — with one field added: `sat:work`, the work identity this
project pairs translations by. Hugo pairs by matching relative path, which fails
the moment a slug is translated, so the pairing here is worked out from the
slugs and REPORTED for review rather than assumed. Pages matched below the
confidence threshold are imported as independent works and listed, because a
wrong pairing is worse than an absent one: it makes the language switcher send a
reader to a page about something else.

Usage:
    python3 scripts/branding/import-hugo.py --from <hugo-root> --client <name>
    python3 scripts/branding/import-hugo.py --from <hugo-root> --client <name> --write

Reports and writes nothing by default. `--write` writes, and refuses if the
target seed already holds content unless `--replace` is also given.

This handles content. Styles, fonts and assets are separate passes.
"""

from __future__ import annotations

import argparse
import difflib
import os
import re
import shutil
import sys
import tomllib
import uuid

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FENCE = "---"

# Below this, two slugs are not called the same work. Tuned against this
# project's own translations: cognates like accessibility/accessibilite/
# accesibilidad and design-token-primer/introduction-tokens-design land well
# above it, while unrelated pages in the same section land well below.
PAIR_THRESHOLD = 0.34


def fail(msg: str) -> None:
    print(f"[import-hugo] {msg}", file=sys.stderr)
    sys.exit(1)


# ── reading the Hugo site ────────────────────────────────────────────────────

def read_config(hugo_root: str) -> dict:
    for name in ("hugo.toml", "config.toml"):
        path = os.path.join(hugo_root, name)
        if os.path.isfile(path):
            with open(path, "rb") as fh:
                return tomllib.load(fh)
    fail(f"no hugo.toml or config.toml in {hugo_root}")


def content_dirs(hugo_root: str, cfg: dict) -> dict:
    """{locale: absolute content directory}, from [languages].

    Each language may name its own contentDir, which is how this site keeps
    en-ca, fr-ca and es in separate trees. A single-language site with no
    [languages] block falls back to content/ under the default language.
    """
    langs = cfg.get("languages") or {}
    if not langs:
        default = cfg.get("defaultContentLanguage", "en")
        return {default: os.path.join(hugo_root, cfg.get("contentDir", "content"))}

    out = {}
    for code, conf in langs.items():
        rel = (conf or {}).get("contentDir") or os.path.join("content", code)
        path = os.path.join(hugo_root, rel)
        if os.path.isdir(path):
            out[code] = path
    return out


def read_front_matter(path: str) -> tuple:
    """(front matter text, body text). Only YAML fences are handled.

    A Hugo site may use TOML (+++) or JSON front matter; this one uses YAML, and
    a file in another dialect is reported rather than half-converted.
    """
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    if text.startswith("+++"):
        return None, text
    if not text.startswith(FENCE):
        return "", text
    end = text.find(f"\n{FENCE}", len(FENCE))
    if end == -1:
        return "", text
    return text[len(FENCE) + 1 : end + 1], text[end + len(FENCE) + 2 :]


def title_of(front: str) -> str:
    match = re.search(r'^title:\s*"?(.*?)"?\s*$', front or "", re.MULTILINE)
    return match.group(1) if match else ""


def pages_in(content_dir: str) -> list:
    """Every page in one language, as {rel, section, slug, path, front, body}.

    `rel` is where the page lands in the seed: a section's `_index.md` becomes
    that section's `index.md`, and a page bundle keeps its directory, so the URL
    a page publishes at is the one it already has.
    """
    pages = []
    for dirpath, dirnames, filenames in os.walk(content_dir):
        dirnames[:] = [d for d in sorted(dirnames) if not d.startswith(".")]
        for name in sorted(filenames):
            if not name.endswith(".md"):
                continue
            path = os.path.join(dirpath, name)
            rel = os.path.relpath(path, content_dir).replace(os.sep, "/")
            parts = rel.split("/")

            if name == "_index.md":
                rel_out = "/".join(parts[:-1] + ["index.md"]) if len(parts) > 1 else "index.md"
                section = parts[0] if len(parts) > 1 else ""
                slug = ""
            else:
                rel_out = rel
                section = parts[0] if len(parts) > 1 else ""
                slug = parts[-2] if len(parts) > 1 and name == "index.md" else parts[-1][:-3]

            front, body = read_front_matter(path)
            pages.append({
                "rel": rel_out,
                "source": rel,
                "section": section,
                "slug": slug,
                "path": path,
                "front": front,
                "body": body,
                "title": title_of(front),
            })
    return pages


# ── pairing translations ─────────────────────────────────────────────────────

def normalise(slug: str) -> str:
    """A slug reduced to something comparable across languages.

    Word order differs between languages — design-token-primer against
    introduction-tokens-design — so the words are sorted before comparison, and
    accents are folded so accessibilite and accesibilidad start alike.
    """
    folded = (slug.lower()
              .replace("é", "e").replace("è", "e").replace("ê", "e")
              .replace("á", "a").replace("í", "i").replace("ó", "o")
              .replace("ú", "u").replace("ñ", "n").replace("ç", "c"))
    return "".join(sorted(re.split(r"[-_]+", folded)))


def score(a: str, b: str) -> float:
    return difflib.SequenceMatcher(None, normalise(a), normalise(b)).ratio()


def parse_pairs(values: list) -> dict:
    """--pair about/about=fr-ca:a-propos,es:acerca-de  ->  {(section, slug): {...}}

    Some translations share no letters at all — privacy and confidentialité,
    self-hosting-decision-framework and cadre-auto-hébergement — and no
    similarity measure will ever match them. Rather than lower the threshold
    until unrelated pages start pairing, those are stated outright, on the
    command line, where the decision is visible in the shell history.
    """
    out = {}
    for value in values or []:
        key, _, targets = value.partition("=")
        if not targets:
            fail(f"--pair {value} should read section/slug=locale:slug[,locale:slug]")
        section, _, slug = key.partition("/")
        mapping = {}
        for target in targets.split(","):
            locale, _, target_slug = target.partition(":")
            if not target_slug:
                fail(f"--pair {value}: '{target}' should read locale:slug")
            mapping[locale.strip()] = target_slug.strip()
        out[(section.strip(), slug.strip())] = mapping
    return out


def pair_translations(by_locale: dict, default: str, stated: dict) -> tuple:
    """Give every page a work identity, shared with its translations.

    Pairings stated with --pair are taken as given. The rest are matched within
    a section, against the default language, best score first, and only above
    the threshold. Everything else becomes its own work — an unpaired page is
    simply one with no translation yet, which the site models already.
    """
    works = {}          # (locale, rel) -> work uuid
    report = []         # (section, default slug, {locale: (slug, score)})

    for page in by_locale[default]:
        work = f"urn:uuid:{uuid.uuid4()}"
        works[(default, page["rel"])] = work
        report.append({"section": page["section"], "slug": page["slug"] or "(index)",
                       "work": work, "matches": {},
                       "stated": stated.get((page["section"], page["slug"]), {})})

    for locale, pages in by_locale.items():
        if locale == default:
            continue
        taken = set()
        by_slug = {p["slug"]: p for p in pages}

        # Stated pairings first, so nothing else can claim those pages.
        for entry in report:
            want = entry["stated"].get(locale)
            page = by_slug.get(want) if want else None
            if page:
                works[(locale, page["rel"])] = entry["work"]
                entry["matches"][locale] = (page["slug"], 1.0)
                taken.add(page["rel"])
            elif want:
                fail(f"--pair names {locale}:{want}, which is not a page in that language")
        # Best matches first, so a strong pairing is never displaced by a weak
        # one competing for the same page.
        candidates = []
        for entry in report:
            for page in pages:
                if page["section"] != entry["section"]:
                    continue
                # A section index only ever pairs with a section index.
                if (entry["slug"] == "(index)") != (page["slug"] == ""):
                    continue
                candidates.append((score(entry["slug"], page["slug"] or "index"), entry, page))
        candidates.sort(key=lambda c: -c[0])

        # Entries already settled by --pair are out of the running.
        matched_entries = {id(e) for e in report if locale in e["matches"]}
        for value, entry, page in candidates:
            key = id(entry)
            if key in matched_entries or page["rel"] in taken:
                continue
            if entry["slug"] == "(index)" and page["slug"] == "":
                value = 1.0
            elif value < PAIR_THRESHOLD:
                continue
            matched_entries.add(key)
            taken.add(page["rel"])
            works[(locale, page["rel"])] = entry["work"]
            entry["matches"][locale] = (page["slug"] or "(index)", value)

        for page in pages:
            if page["rel"] not in taken:
                works[(locale, page["rel"])] = f"urn:uuid:{uuid.uuid4()}"

    return works, report


# ── writing the seed ─────────────────────────────────────────────────────────

def with_identity(front: str, body: str, work: str) -> str:
    """The page as it will be written: front matter plus its work identity."""
    front = (front or "").rstrip("\n")
    return f'{FENCE}\n{front}\n"sat:work": "{work}"\n{FENCE}\n\n{body.lstrip(chr(10))}'


def main() -> int:
    ap = argparse.ArgumentParser(description="Import a Hugo site's content into a branding seed.")
    ap.add_argument("--from", dest="hugo", required=True, help="the Hugo project root")
    ap.add_argument("--client", required=True, help="the branding directory to write into")
    ap.add_argument("--pair", action="append", metavar="SECTION/SLUG=LOCALE:SLUG",
                    help="state a translation pairing the slugs cannot show; repeatable")
    ap.add_argument("--write", action="store_true", help="write the seed (otherwise report only)")
    ap.add_argument("--replace", action="store_true", help="allow writing into a seed that already has content")
    args = ap.parse_args()

    hugo_root = os.path.abspath(os.path.expanduser(args.hugo))
    if not os.path.isdir(hugo_root):
        fail(f"{hugo_root} is not a directory")

    cfg = read_config(hugo_root)
    default = cfg.get("defaultContentLanguage", "en")
    dirs = content_dirs(hugo_root, cfg)
    if default not in dirs:
        fail(f"defaultContentLanguage is {default}, but there is no content directory for it")

    print(f"[import-hugo] {hugo_root}")
    print(f"[import-hugo] baseURL {cfg.get('baseURL', '(none)')}, default language {default}")

    by_locale = {code: pages_in(path) for code, path in sorted(dirs.items())}
    for code, pages in by_locale.items():
        toml_fm = [p["source"] for p in pages if p["front"] is None]
        print(f"[import-hugo] {code}: {len(pages)} page(s) from {os.path.relpath(dirs[code], hugo_root)}")
        for source in toml_fm:
            print(f"  ! {source} uses TOML front matter, which this pass does not convert")

    works, report = pair_translations(by_locale, default, parse_pairs(args.pair))
    others = [c for c in by_locale if c != default]

    print(f"\n[import-hugo] translation pairing ({default} against {', '.join(others)}):")
    unpaired = 0
    for entry in sorted(report, key=lambda e: (e["section"], e["slug"])):
        cells = []
        for code in others:
            if code in entry["matches"]:
                slug, value = entry["matches"][code]
                cells.append(f"{code}:{slug} ({value:.2f})")
            else:
                cells.append(f"{code}:—")
                unpaired += 1
        print(f"  {entry['section'] or '(root)':<10} {entry['slug']:<38} {'  '.join(cells)}")

    orphans = []
    for code in others:
        claimed = {rel for (loc, rel) in works if loc == code}
        matched = {p["rel"] for p in by_locale[code]
                   if works.get((code, p["rel"])) in {e["work"] for e in report}}
        orphans += [f"{code}/{p['rel']}" for p in by_locale[code] if p["rel"] in claimed - matched]

    if orphans:
        print(f"\n[import-hugo] {len(orphans)} page(s) with no counterpart in {default}, "
              "imported as their own work:")
        for line in orphans:
            print(f"  ? {line}")

    attrs = sum(len(re.findall(r"\{[#.][A-Za-z0-9_-]+\}", p["body"] or ""))
                for pages in by_locale.values() for p in pages)
    if attrs:
        print(f"\n[import-hugo] {attrs} Goldmark attribute(s) like {{#id}} in the content. "
              "Eleventy's markdown does not read those; they would render as literal text.")

    target = os.path.join(ROOT, "branding", args.client, "content")
    if not args.write:
        print(f"\n[import-hugo] report only. Pass --write to create {os.path.relpath(target, ROOT)}/")
        return 0

    if os.path.isdir(target) and any(f.endswith(".md") for _, _, fs in os.walk(target) for f in fs):
        if not args.replace:
            fail(f"{os.path.relpath(target, ROOT)}/ already holds content; pass --replace to replace it.")
        shutil.rmtree(target)

    written = 0
    for code, pages in by_locale.items():
        for page in pages:
            if page["front"] is None:
                continue
            out = os.path.join(target, code, page["rel"])
            os.makedirs(os.path.dirname(out), exist_ok=True)
            with open(out, "w", encoding="utf-8") as fh:
                fh.write(with_identity(page["front"], page["body"], works[(code, page["rel"])]))
            written += 1

    print(f"\n[import-hugo] wrote {written} page(s) to {os.path.relpath(target, ROOT)}/")
    print("Next:  npm run ingress -- --dry-run   (to see what would reach the site)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
