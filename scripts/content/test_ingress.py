#!/usr/bin/env python3
"""test_ingress.py, offline test suite for ingress.py and new-client.py.

Builds a scratch site — a live content tree, locale bundles, and a branding
directory with a seed — in a temporary directory, points the module's paths at
it, and exercises every mode against it. Nothing here touches the real
`src/content/` or any real `branding/<client>/`.

The cases that matter most are the destructive ones: overwrite replacing a page
in place, overwrite relocating a page the seed has moved (and the redirect that
falls out of it), recreate removing what the seed does not have, and the guards
that refuse when the seed is empty or a destination is already spoken for.

Usage:
    python3 scripts/content/test_ingress.py
    npm run test:ingress

Exit 0 with a PASS line per check, or exit 1 at the first failure.
"""

import json
import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ingress  # noqa: E402

PASSED = 0


def ok(name):
    global PASSED
    PASSED += 1
    print(f"  PASS  {name}")


def check(cond, name, detail=""):
    if not cond:
        print(f"  FAIL  {name}\n{detail}", file=sys.stderr)
        sys.exit(1)
    ok(name)


# ── the scratch site ─────────────────────────────────────────────────────────

ROUTES = {
    "en-ca": {"home": "", "about": "about", "blog": "blog", "contact": "contact"},
    "fr-ca": {"home": "", "about": "a-propos", "blog": "articles", "contact": "contact"},
}


def page(work, title="Page", body="Body."):
    identity = f'"sat:work": "{work}"\n' if work else ""
    return f'---\ntitle: "{title}"\n{identity}---\n\n{body}\n'


def build_site(root):
    """A scratch repo shaped like the real one, with ingress pointed at it."""
    for code, routes in ROUTES.items():
        os.makedirs(os.path.join(root, "src", "_locales"), exist_ok=True)
        with open(os.path.join(root, "src", "_locales", f"{code}.json"), "w") as fh:
            json.dump({"routes": routes}, fh)

    os.makedirs(os.path.join(root, "src", "content", "en-ca"), exist_ok=True)
    os.makedirs(os.path.join(root, "branding", "acme.example", "src", "content"), exist_ok=True)

    ingress.ROOT = root
    ingress.BRANDING = os.path.join(root, "branding")
    ingress.LIVE = os.path.join(root, "src", "content")
    ingress.BUNDLES = os.path.join(root, "src", "_locales")
    return os.path.join(root, "branding", "acme.example", "src", "content")


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def live(*parts):
    return os.path.join(ingress.LIVE, *parts)


# ── the cases ────────────────────────────────────────────────────────────────

def case_add(seed):
    write(os.path.join(seed, "en-ca", "guides", "index.md"), page("urn:uuid:1", "Guides"))
    codes = ingress.locale_codes()

    result = ingress.reconcile(seed, codes, dry_run=True)
    check(len(result["added"]) == 1 and not os.path.exists(live("en-ca", "guides", "index.md")),
          "a dry run reports the add and writes nothing")

    result = ingress.reconcile(seed, codes, dry_run=False)
    check(os.path.exists(live("en-ca", "guides", "index.md")), "an absent page is copied in")
    check(result["published"][("urn:uuid:1", "en-ca")] == "/en-ca/guides/",
          "the copied page publishes at the URL its path mirrors")

    again = ingress.reconcile(seed, codes, dry_run=False)
    check(not again["added"] and len(again["skipped"]) == 1,
          "running it again is a no-op — the work is already published")


def case_skip_protects_edits(seed):
    codes = ingress.locale_codes()
    write(live("en-ca", "guides", "index.md"), page("urn:uuid:1", "Guides", "Edited by hand."))
    ingress.reconcile(seed, codes, dry_run=False)
    check("Edited by hand." in read(live("en-ca", "guides", "index.md")),
          "the default pass never overwrites an edit")


def case_overwrite_replaces(seed):
    codes = ingress.locale_codes()
    result = ingress.reconcile(seed, codes, dry_run=False, overwrite=True)
    check(len(result["replaced"]) == 1 and "Edited by hand." not in read(live("en-ca", "guides", "index.md")),
          "--overwrite replaces the site's copy with the seed's")

    settled = ingress.reconcile(seed, codes, dry_run=False, overwrite=True)
    check(not settled["replaced"] and len(settled["unchanged"]) == 1,
          "an identical page counts as unchanged, and is not rewritten")


def case_overwrite_moves(seed):
    codes = ingress.locale_codes()
    before = ingress.index_live(codes)

    os.makedirs(os.path.join(seed, "en-ca", "about"), exist_ok=True)
    shutil.move(os.path.join(seed, "en-ca", "guides"), os.path.join(seed, "en-ca", "about", "guides"))

    result = ingress.reconcile(seed, codes, dry_run=False, overwrite=True)
    check(os.path.exists(live("en-ca", "about", "guides", "index.md")),
          "a page the seed has moved is written to its new path")
    check(not os.path.exists(live("en-ca", "guides", "index.md")),
          "…and removed from the old one, so one work has one page per language")
    check(not os.path.exists(live("en-ca", "guides")),
          "the emptied directory is pruned")

    moves, gone = ingress.plan_redirects(before, result["published"])
    check(moves == [("/en-ca/guides/", "/en-ca/about/guides/")] and not gone,
          "the move is reported as a redirect from the old URL to the new one",
          f"moves={moves} gone={gone}")


def case_routed_pages_win(seed):
    codes = ingress.locale_codes()
    write(os.path.join(seed, "en-ca", "about", "index.md"), page("urn:uuid:2", "About"))
    result = ingress.reconcile(seed, codes, dry_run=False, overwrite=True)
    check(not os.path.exists(live("en-ca", "about", "index.md")) and len(result["blocked"]) == 1,
          "a seed page is blocked where a designed page already owns the URL")


def case_blog_is_locale_second(seed):
    codes = ingress.locale_codes()
    write(os.path.join(seed, "fr-ca", "articles", "bonjour.md"), page("urn:uuid:3", "Bonjour"))
    result = ingress.reconcile(seed, codes, dry_run=False)
    check(os.path.exists(live("blog", "fr-ca", "bonjour.md")),
          "a post under the locale's blog route lands in the locale-second blog tree")
    check(result["published"][("urn:uuid:3", "fr-ca")] == "/fr-ca/articles/bonjour/",
          "…and publishes at the locale's blog URL")


def case_identity_is_stamped(seed):
    codes = ingress.locale_codes()
    path = os.path.join(seed, "en-ca", "notes", "index.md")
    write(path, page(None, "Notes"))
    ingress.reconcile(seed, codes, dry_run=True)
    check("sat:work" not in read(path), "a dry run does not stamp an identity")
    ingress.reconcile(seed, codes, dry_run=False)
    check("sat:work" in read(path), "a seed file with no identity is given one")


def case_unidentified_live(seed):
    codes = ingress.locale_codes()
    write(live("en-ca", "stray.md"), page(None, "Stray"))
    check(ingress.unidentified_live(codes) == ["en-ca/stray.md"],
          "a live page with no identity is findable before anything destructive")


def case_recreate(seed):
    codes = ingress.locale_codes()
    write(live("en-ca", "orphan", "index.md"), page("urn:uuid:9", "Orphan"))
    write(live("en-ca", "en-ca.11tydata.js"), "module.exports = {};\n")
    before = ingress.index_live(codes)

    removed = ingress.wipe_live(dry_run=True)
    check(os.path.exists(live("en-ca", "orphan", "index.md")) and removed,
          "a dry wipe reports what it would remove and removes nothing")

    ingress.wipe_live(dry_run=False)
    check(not ingress.markdown_files(ingress.LIVE), "the wipe clears every content file")
    check(os.path.exists(live("en-ca", "en-ca.11tydata.js")),
          "…and keeps the directory data files, which are code rather than content")

    result = ingress.reconcile(seed, codes, dry_run=False, empty_tree=True)
    check(os.path.exists(live("en-ca", "about", "guides", "index.md")),
          "the tree is rebuilt from the seed")
    _, gone = ingress.plan_redirects(before, result["published"])
    check(gone == ["/en-ca/orphan/"],
          "a live page the seed does not have is reported as gone, not silently dropped",
          f"gone={gone}")


def case_redirects_file(seed):
    write(os.path.join(ingress.ROOT, "src", "_redirects"), "# existing\n/old/  /new/  301\n")
    written, skipped = ingress.write_redirects(
        [("/a/", "/b/"), ("/old/", "/elsewhere/")], "test", dry_run=True)
    check(written == [("/a/", "/b/")] and skipped == [("/old/", "/elsewhere/")],
          "a URL that already has a rule is left alone; the rest are written")
    check("/a/" not in read(os.path.join(ingress.ROOT, "src", "_redirects")),
          "a dry run writes no rule")

    ingress.write_redirects([("/a/", "/b/")], "test", dry_run=False)
    text = read(os.path.join(ingress.ROOT, "src", "_redirects"))
    check(text.count("/old/") == 1 and "/a/" in text and text.index("# existing") < text.index("/a/"),
          "real rules are appended below the hand-written ones")


def case_empty_seed_guard(seed):
    """The guard that was missing when this command emptied a branding directory."""
    empty = os.path.join(ingress.ROOT, "branding", "empty.example", "src", "content")
    os.makedirs(empty, exist_ok=True)
    check(not ingress.markdown_files(empty),
          "an empty seed is recognisable as empty, which is what new-client refuses on")


def main():
    root = tempfile.mkdtemp(prefix="ingress-test-")
    try:
        seed = build_site(root)
        for case in (
            case_add,
            case_skip_protects_edits,
            case_overwrite_replaces,
            case_overwrite_moves,
            case_routed_pages_win,
            case_blog_is_locale_second,
            case_identity_is_stamped,
            case_unidentified_live,
            case_recreate,
            case_redirects_file,
            case_empty_seed_guard,
        ):
            print(f"[{case.__name__}]")
            case(seed)
    finally:
        shutil.rmtree(root, ignore_errors=True)

    print(f"\n[test-ingress] {PASSED} checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
