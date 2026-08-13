#!/usr/bin/env python3
"""Reconcile the client's seed content into the live content tree.

Implements spec--content-ingress-v0.1.0. The seed is the client-owned content
under `branding/<client>/content/`; the live tree is `src/content/`, which
is what Eleventy builds and the CMS edits. Ingress walks the seed and, for each
content file:

  1. reads its work identity (`sat:work`) and its locale (from its path);
  2. skips it when an expression of that work already exists live in that
     locale, wherever it sits — a maintainer may have edited it;
  3. copies it in when it does not, creating directories as needed;
  4. stamps a generated UUID into the seed file when it carries no identity;
  5. never deletes anything.

Running it twice with no seed change is a no-op, so it is safe at any time:
stand a new client up, or fold a newly seeded section into an existing site.

Two guards beyond the spec, both reported rather than silent:

  Routed pages win. `src/pages/` holds designed landing pages at slugs like
  /en-ca/about/. A seed file that would publish to the same URL is blocked, not
  copied, because two templates writing one permalink fails the build.

  The blog is locale-second. Posts live at `src/content/blog/<locale>/` while
  the rest of the content tree is locale-first, so a seed section named for the
  locale's blog route is mapped there instead of mirrored verbatim.

Usage:
    python3 scripts/content/ingress.py [--dry-run]
    npm run ingress

Ingress is deliberately an explicit command. `npm run build` reads the live
tree only and never mutates content.

`scripts/branding/new-client.py --recreate` imports this module and reuses the
same walk, path mapping and reconcile, so the additive command and the wipe-and-
rebuild command can never disagree about where a page belongs or what URL it
publishes at.
"""

from __future__ import annotations

import argparse
import filecmp
import glob
import json
import os
import shutil
import sys
import uuid

try:
    import yaml
except ImportError:  # pragma: no cover - same dependency build-brand.py needs
    print("[ingress] PyYAML is required: pip install pyyaml", file=sys.stderr)
    raise SystemExit(1)

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BRANDING = os.path.join(ROOT, "branding")
LIVE = os.path.join(ROOT, "src", "content")
BUNDLES = os.path.join(ROOT, "src", "_locales")

FRONT_MATTER_FENCE = "---"


def fail(msg: str) -> None:
    print(f"[ingress] {msg}", file=sys.stderr)
    sys.exit(1)


# ── the two trees ────────────────────────────────────────────────────────────

def find_client() -> str:
    """The one active branding directory; '_'-prefixed ones are templates."""
    clients = [
        os.path.basename(d)
        for d in sorted(glob.glob(os.path.join(BRANDING, "*")))
        if os.path.isdir(d) and not os.path.basename(d).startswith("_")
    ]
    if not clients:
        fail("no active branding/<client>/ directory; run `npm run new-client` first.")
    if len(clients) > 1:
        fail(
            f"multiple client branding directories ({', '.join(clients)}); exactly "
            "one un-prefixed branding/<client>/ is allowed."
        )
    return clients[0]


def locale_codes() -> list:
    """Locales the site has string bundles for, e.g. ['en-ca', 'fr-ca']."""
    return sorted(
        os.path.splitext(os.path.basename(f))[0]
        for f in glob.glob(os.path.join(BUNDLES, "*.json"))
    )


def routes_for(code: str) -> dict:
    """The locale's route table: {'about': 'about', 'blog': 'articles', ...}."""
    path = os.path.join(BUNDLES, f"{code}.json")
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as fh:
        return json.load(fh).get("routes", {})


def markdown_files(root: str) -> list:
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in sorted(dirnames) if not d.startswith("_")]
        out.extend(
            os.path.join(dirpath, name)
            for name in sorted(filenames)
            if name.endswith(".md")
        )
    return out


# ── front matter ─────────────────────────────────────────────────────────────

def read_front_matter(path: str) -> tuple:
    """(parsed dict, raw text). An unparsable or absent block reads as empty."""
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    if not text.startswith(FRONT_MATTER_FENCE):
        return {}, text
    end = text.find(f"\n{FRONT_MATTER_FENCE}", len(FRONT_MATTER_FENCE))
    if end == -1:
        return {}, text
    block = text[len(FRONT_MATTER_FENCE) : end]
    try:
        data = yaml.safe_load(block) or {}
    except yaml.YAMLError:
        data = {}
    return (data if isinstance(data, dict) else {}), text


def stamp_work(path: str, text: str, work: str, dry_run: bool) -> str:
    """Write a generated identity into a seed file that has none.

    The line is appended to the existing front matter, or a block is created
    when the file has none, and the key is quoted because a bare `sat:work:`
    is not valid YAML.
    """
    line = f'"sat:work": "{work}"\n'
    if text.startswith(FRONT_MATTER_FENCE):
        end = text.find(f"\n{FRONT_MATTER_FENCE}", len(FRONT_MATTER_FENCE))
        updated = text[: end + 1] + line + text[end + 1 :]
    else:
        updated = f"{FRONT_MATTER_FENCE}\n{line}{FRONT_MATTER_FENCE}\n\n{text}"
    if not dry_run:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(updated)
    return updated


# ── paths and URLs ───────────────────────────────────────────────────────────

def locale_of(rel: str, codes: list) -> str:
    """The locale a path belongs to: the first segment that names one.

    Covers both shapes in play — `en-ca/about/index.md` in the seed and the
    locale-first live tree, and `blog/en-ca/post.md` in the live blog.
    """
    for part in rel.split("/"):
        if part in codes:
            return part
    return ""


def live_target(rel: str, code: str, routes: dict) -> str:
    """Where a seed file lands in the live tree, as a repo-relative path.

    Mirrors the seed path, except that the locale's blog section maps to the
    locale-second `blog/<locale>/` layout the post collection globs.
    """
    parts = rel.split("/")
    blog_slug = routes.get("blog")
    if len(parts) > 2 and parts[0] == code and parts[1] in {"blog", blog_slug}:
        return "/".join(["blog", code] + parts[2:])
    return rel


def url_for(rel: str, code: str, routes: dict) -> str:
    """The URL a live path publishes to, matching _localeTree.js and the blog."""
    stem = rel[: -len(".md")] if rel.endswith(".md") else rel
    parts = stem.split("/")
    if parts[0] == "blog" and len(parts) > 2 and parts[1] == code:
        slug = routes.get("blog", "blog")
        return f"/{code}/{slug}/{'/'.join(parts[2:])}/"
    if parts[-1] == "index":
        parts = parts[:-1]
    return "/" + "/".join(parts) + "/" if parts else f"/{code}/"


def routed_urls(codes: list) -> set:
    """Every URL owned by a designed page in src/pages/, across all locales.

    Read from the templates that actually exist, not from the locale bundles'
    `routes` table. The two are not the same thing: `routes` also holds slugs
    for pages that have been retired, and a slug with no template behind it owns
    nothing — blocking a content page on it would reserve a URL that nothing
    publishes. Each template declares its own `routeKey` in front matter, which
    is looked up per locale to get that language's slug.
    """
    pages_dir = os.path.join(ROOT, "src", "pages")
    if not os.path.isdir(pages_dir):
        return set()

    keys = set()
    for name in sorted(os.listdir(pages_dir)):
        if not name.endswith((".njk", ".html", ".md")):
            continue
        data, _ = read_front_matter(os.path.join(pages_dir, name))
        if data.get("routeKey"):
            keys.add(data["routeKey"])

    urls = set()
    for code in codes:
        routes = routes_for(code)
        for key in keys:
            slug = routes.get(key)
            if slug is not None:
                urls.add(f"/{code}/{slug}/" if slug else f"/{code}/")
    return urls


# ── the reconcile ────────────────────────────────────────────────────────────

def scan_live(codes: list) -> dict:
    """{(work, locale): {url, rel, path}} for everything already published.

    Overwriting needs the path as well as the URL: replacing a page in place is
    a copy over the file it is already in, while a page whose seed location has
    changed has to be written to the new path and removed from the old one —
    two files carrying one work in one language is exactly what
    contentWorkIndex refuses to build.
    """
    index = {}
    if not os.path.isdir(LIVE):
        return index
    for path in markdown_files(LIVE):
        rel = os.path.relpath(path, LIVE).replace(os.sep, "/")
        code = locale_of(rel, codes)
        if not code:
            continue
        data, _ = read_front_matter(path)
        work = data.get("sat:work")
        if work:
            index[(work, code)] = {
                "url": url_for(rel, code, routes_for(code)),
                "rel": rel,
                "path": path,
            }
    return index


def index_live(codes: list) -> dict:
    """{(work, locale): url} for everything already published."""
    return {key: entry["url"] for key, entry in scan_live(codes).items()}


def unidentified_live(codes: list) -> list:
    """Live pages carrying no sat:work, as repo-relative paths.

    Everything else in this module reasons about identity, so a page without
    one is invisible to it: it cannot be matched to a seed file, cannot be
    recognised as moved, and cannot be redirected. A wipe-and-rebuild would
    remove it and never put it back. Callers list these before doing anything
    destructive, because they are the pages a report would otherwise lose.
    """
    out = []
    if not os.path.isdir(LIVE):
        return out
    for path in markdown_files(LIVE):
        rel = os.path.relpath(path, LIVE).replace(os.sep, "/")
        if not locale_of(rel, codes):
            continue
        data, _ = read_front_matter(path)
        if not data.get("sat:work"):
            out.append(rel)
    return out


def seed_dir(client: str) -> str:
    return os.path.join(BRANDING, client, "content")


# ── recreating the live tree ─────────────────────────────────────────────────

def wipe_live(dry_run: bool) -> list:
    """Delete every content file in the live tree, keeping its machinery.

    Only markdown goes: `src/content/` also holds directory-data files
    (`_localeTree.js`, `<locale>.11tydata.js`, `blog.11tydata.js`) that are code
    rather than content, and a tree without them does not build. Directories
    left empty are pruned so a removed section does not linger as an empty
    folder; a directory still holding a data file stays.
    """
    removed = []
    if not os.path.isdir(LIVE):
        return removed

    for path in markdown_files(LIVE):
        removed.append(os.path.relpath(path, LIVE).replace(os.sep, "/"))
        if not dry_run:
            os.remove(path)

    if not dry_run:
        prune_empty_dirs()

    return removed


def prune_empty_dirs() -> None:
    """Drop directories the live tree no longer has anything in.

    A section that was emptied — wiped, or moved somewhere else — should not
    linger as an empty folder. A directory still holding a data file stays,
    since those are code rather than content.
    """
    for dirpath, dirnames, filenames in os.walk(LIVE, topdown=False):
        if dirpath != LIVE and not dirnames and not filenames:
            os.rmdir(dirpath)


def plan_redirects(before: dict, after: dict) -> tuple:
    """Compare two {(work, locale): url} maps into (moves, gone).

    A work published at one URL before and another after has moved, and the old
    URL needs a 301. A work with no URL after has no destination to point at,
    so it is reported rather than redirected — inventing a target would send
    readers somewhere that does not answer their request.
    """
    moves, gone = [], []
    for key, old in sorted(before.items(), key=lambda kv: kv[1]):
        new = after.get(key)
        if new is None:
            gone.append(old)
        elif new != old:
            moves.append((old, new))
    return moves, gone


def write_redirects(moves: list, note: str, dry_run: bool) -> tuple:
    """Append 301s for moved URLs to src/_redirects. Returns (written, skipped).

    A source path already present in the file is left alone: the existing rule
    was written deliberately, possibly by hand, and Netlify applies the first
    match anyway, so a second rule for the same source would be dead text.
    """
    path = os.path.join(ROOT, "src", "_redirects")
    existing = ""
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            existing = fh.read()

    sources = {
        line.split()[0]
        for line in existing.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }

    written = [(old, new) for old, new in moves if old not in sources]
    skipped = [(old, new) for old, new in moves if old in sources]

    if written and not dry_run:
        width = max(len(old) for old, _ in written) + 2
        block = [
            "",
            f"# --- {note} ---",
            "#",
            "# Written by scripts/branding/new-client.py --redirects. Each line is a",
            "# content URL that moved when the live tree was recreated from the",
            "# branding directory. Netlify applies the first matching rule, so these",
            "# sit at the end, below the hand-written rules above.",
        ]
        block += [f"{old:<{width}}{new:<{width}}301" for old, new in written]
        with open(path, "a", encoding="utf-8") as fh:
            fh.write("\n".join(block) + "\n")

    return written, skipped


def check_blog_sections(seed: str, codes: list, label: str = "ingress") -> list:
    """Warn about a seed section that looks like the blog but is not named for it.

    Posts publish through the collection that globs `src/content/blog/<locale>/`,
    reached by naming the seed section "blog" or the locale's own blog route
    slug ("articles" in fr-ca). A section of dated, index-less pages under any
    other name — `blogue/`, say, when the route is `articles` — would be copied
    in as ordinary content pages at a URL the blog listing never looks at, and
    the listing would come out empty. Cheaper to say so than to guess.
    """
    warnings = []
    for code in codes:
        root = os.path.join(seed, code)
        if not os.path.isdir(root):
            continue
        blog_names = {"blog", routes_for(code).get("blog")}
        for name in sorted(os.listdir(root)):
            section = os.path.join(root, name)
            if not os.path.isdir(section) or name in blog_names:
                continue
            files = [f for f in os.listdir(section) if f.endswith(".md")]
            if not files or "index.md" in files:
                continue
            dated = all(
                read_front_matter(os.path.join(section, f))[0].get("date")
                for f in files
            )
            if dated:
                warnings.append(
                    f"{code}/{name}/ holds {len(files)} dated page(s) with no "
                    f"index.md, which is the shape of a blog, but this locale's "
                    f"blog route is \"{routes_for(code).get('blog')}\". Rename it "
                    "to that (or to \"blog\") if these are posts, or the blog "
                    "listing will not find them."
                )
    for warning in warnings:
        print(f"[{label}] warning: {warning}")
    return warnings


def describe_seed(seed: str, codes: list, label: str = "ingress") -> None:
    """Report which of the seed's locale directories the site can publish."""
    seed_locales = [
        d for d in sorted(os.listdir(seed)) if os.path.isdir(os.path.join(seed, d))
    ]
    # A '_'-prefixed directory is parked on purpose — a language held back from
    # publication, the same convention branding/_template/ uses one level up —
    # so it is named as parked rather than reported as an unknown locale.
    parked = [d for d in seed_locales if d.startswith("_")]
    known = [d for d in seed_locales if d in codes]
    unknown = [d for d in seed_locales if d not in codes and d not in parked]

    print(f"[{label}] locales in the seed: {', '.join(known) or 'none'}")
    if parked:
        print(f"[{label}] parked, not published: {', '.join(parked)}")
    for code in unknown:
        print(
            f"[{label}] SKIP  {code}/ — no src/_locales/{code}.json, so the site "
            "has no such locale."
        )


def reconcile(
    seed: str,
    codes: list,
    dry_run: bool,
    empty_tree: bool = False,
    overwrite: bool = False,
) -> dict:
    """Reconcile the seed into the live tree. Returns what happened, and where
    each work landed.

    `published` maps (work, locale) to the URL that work now has in the live
    tree, whether this run copied it in, moved it, or found it already there.
    That is what lets a caller work out which URLs moved.

    Default is add-if-absent: a work already published in that language is left
    exactly as it is, because a maintainer may have edited it.

    `overwrite` makes the seed authoritative over pages that already exist. A
    page still at its seeded location is replaced; a page whose seed location
    has changed is written to the new one and removed from the old, which is a
    move and wants a redirect. Live pages the seed says nothing about are not
    touched — that is what separates this from a wipe-and-rebuild.

    `empty_tree` says the live tree has just been wiped, or would be on a real
    run — so nothing counts as already present, and a dry run reports the same
    plan the real run will carry out instead of "everything is already there".
    Files this run has placed are still tracked, so two seed files claiming one
    destination are caught either way.
    """
    existing = {} if empty_tree else scan_live(codes)
    live_index = {key: entry["url"] for key, entry in existing.items()}
    reserved = routed_urls(codes)
    published = dict(live_index)
    placed = set()

    added, skipped, blocked, stamped = [], [], [], []
    replaced, moved, unchanged = [], [], []
    # Repo-relative live paths this run writes to and removes, so a caller can
    # ask git what it could restore without re-parsing the report lines.
    writes, removals = [], []

    for path in markdown_files(seed):
        rel = os.path.relpath(path, seed).replace(os.sep, "/")
        code = locale_of(rel, codes)
        if not code:
            continue

        routes = routes_for(code)
        data, text = read_front_matter(path)

        work = data.get("sat:work")
        if not work:
            work = f"urn:uuid:{uuid.uuid4()}"
            stamp_work(path, text, work, dry_run)
            stamped.append(rel)

        live = existing.get((work, code))
        if live and not overwrite:
            skipped.append(f"{rel} -> {live['url']}")
            continue

        target_rel = live_target(rel, code, routes)
        target = os.path.join(LIVE, target_rel)
        url = url_for(target_rel, code, routes)

        if url in reserved:
            blocked.append(f"{rel} -> {url} (owned by a page in src/pages/)")
            continue
        if target_rel in placed:
            blocked.append(f"{rel} -> src/content/{target_rel} (already claimed this run)")
            continue
        # A destination already holding a different work is a genuine clash, and
        # is left alone in every mode: overwriting is the seed replacing its own
        # page, never one work landing on top of another.
        if os.path.exists(target) and not empty_tree and (not live or live["rel"] != target_rel):
            blocked.append(f"{rel} -> src/content/{target_rel} (file already there)")
            continue

        if live and live["rel"] == target_rel:
            if filecmp.cmp(path, live["path"], shallow=False):
                unchanged.append(f"{rel} -> {url}")
                published[(work, code)] = url
                placed.add(target_rel)
                continue
            if not dry_run:
                shutil.copy2(path, target)
            replaced.append(f"{rel} -> src/content/{target_rel}")
            writes.append(f"src/content/{target_rel}")
        elif live:
            if not dry_run:
                os.makedirs(os.path.dirname(target), exist_ok=True)
                shutil.copy2(path, target)
                os.remove(live["path"])
            moved.append(f"src/content/{live['rel']} -> src/content/{target_rel}")
            writes.append(f"src/content/{target_rel}")
            removals.append(f"src/content/{live['rel']}")
        else:
            if not dry_run:
                os.makedirs(os.path.dirname(target), exist_ok=True)
                shutil.copy2(path, target)
            added.append(f"{rel} -> src/content/{target_rel}")
            writes.append(f"src/content/{target_rel}")

        placed.add(target_rel)
        live_index[(work, code)] = url
        published[(work, code)] = url

    if not dry_run and moved:
        prune_empty_dirs()

    return {
        "added": added,
        "replaced": replaced,
        "moved": moved,
        "unchanged": unchanged,
        "skipped": skipped,
        "blocked": blocked,
        "stamped": stamped,
        "published": published,
        "writes": writes,
        "removals": removals,
    }


def report(result: dict, dry_run: bool, label: str = "ingress") -> None:
    """Print the tally, then every line that changed something.

    Unchanged and skipped pages are counted but not listed: on a settled site
    they are almost everything, and burying three real changes under thirty
    "already fine" lines is how a report stops being read.
    """
    counts = [
        f"{'would add' if dry_run else 'added'} {len(result['added'])}",
        f"replaced {len(result.get('replaced', []))}",
        f"moved {len(result.get('moved', []))}",
        f"unchanged {len(result.get('unchanged', []))}",
        f"skipped {len(result['skipped'])}",
        f"blocked {len(result['blocked'])}",
    ]
    print(f"\n[{label}] {', '.join(counts)}")

    for line in result["added"]:
        print(f"  + {line}")
    for line in result.get("replaced", []):
        print(f"  ± {line}")
    for line in result.get("moved", []):
        print(f"  → {line}")
    for line in result["blocked"]:
        print(f"  ! {line}")

    if result["stamped"]:
        word = "would stamp" if dry_run else "stamped"
        print(f"[{label}] {word} a generated sat:work into {len(result['stamped'])} seed file(s):")
        for line in result["stamped"]:
            print(f"  ~ {line}")
    if result["blocked"]:
        print(
            f"[{label}] blocked entries were left alone — a destination held by a "
            "designed page, or by a different work. Resolve each one by hand."
        )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Reconcile seed content into the live content tree."
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="let the seed replace pages that already exist, and relocate ones it has moved",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="report what would happen, and change nothing",
    )
    args = parser.parse_args()

    client = find_client()
    seed = seed_dir(client)
    if not os.path.isdir(seed):
        fail(f"branding/{client}/content/ does not exist; nothing to ingress.")

    codes = locale_codes()
    print(f"[ingress] client: {client}")
    describe_seed(seed, codes)
    check_blog_sections(seed, codes)

    if args.overwrite:
        print(
            "[ingress] --overwrite: the seed is authoritative over pages it "
            "already published. Live pages it says nothing about are untouched."
        )

    report(reconcile(seed, codes, args.dry_run, overwrite=args.overwrite), args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
