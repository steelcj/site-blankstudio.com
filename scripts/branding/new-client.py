#!/usr/bin/env python3
"""Start a new client, and push a client's branding out over the site.

Copies the template branding directory — brand.yaml, fonts.yaml, site.yaml, and
the assets guide — to a new directory named for the client, ready to fill in.
The generators (build-brand.py, fetch-fonts.py) then discover it automatically,
since they pick the one directory under branding/ that is not '_'-prefixed.

Usage:
    python3 scripts/branding/new-client.py <client> [flags]
    npm run new-client -- <client> [flags]     # e.g. clientbrand.com

The branding directory is never destroyed here. An existing branding/<client>/
is used as it stands, and only a missing one is created. What the flags act on
is the SITE — the live content tree in src/content/ — because pushing the
branding directory out over the site is what it is for:

    --overwrite   Let the branding directory win over the site. A page it has
                  already published is replaced by the seed's version, and a
                  page whose seed location has changed is moved to the new one.
                  Live pages the seed says nothing about are left alone.
    --recreate    Rebuild the site's content from the branding directory: remove
                  what is in src/content/ and copy the seed in, so the live tree
                  ends up an exact reflection of the seed. The wider hammer — it
                  also removes live pages the seed does not have.
    --redirects   With either of those, write a 301 into src/_redirects for every
                  page whose URL changes, so a live site keeps its inbound links
                  and its rankings when sections move.
    --dry-run     Report what each of the above would do, and change nothing.
    --yes         Skip the confirmation prompt. For scripts and CI; typing the
                  answer is the safer habit.

With no flags the command only creates a missing branding directory and leaves
published content alone. Both content flags print what they will change and ask
first, and the repository is under git either way.

Ordinary day-to-day seeding is `npm run ingress`, which only ever adds what is
missing and never disturbs an edit. Reach for --overwrite when the branding
directory is right and the site has drifted from it, and for --recreate when the
site should hold nothing the branding directory does not.
"""

from __future__ import annotations

import argparse
import glob
import os
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BRANDING = os.path.join(ROOT, "branding")
TEMPLATE = os.path.join(BRANDING, "_template")

# The content half of this script — walking the seed, mapping a seed file to
# the URL it publishes at, wiping and refilling the live tree — is ingress's
# job and lives there, so the two commands cannot disagree about where a page
# belongs.
sys.path.insert(0, os.path.join(ROOT, "scripts", "content"))
import ingress  # noqa: E402


def fail(msg: str) -> None:
    print(f"[new-client] {msg}", file=sys.stderr)
    sys.exit(1)


def active_clients() -> list:
    return [
        os.path.basename(d)
        for d in glob.glob(os.path.join(BRANDING, "*"))
        if os.path.isdir(d) and not os.path.basename(d).startswith("_")
    ]


def confirm(question: str, assume_yes: bool) -> bool:
    """Ask before destroying anything. --yes answers for automation."""
    if assume_yes:
        print(f"[new-client] {question} — yes (--yes)")
        return True
    try:
        answer = input(f"[new-client] {question} [y/N] ").strip().lower()
    except EOFError:
        answer = ""
    return answer in {"y", "yes"}


# ── branding/<client>/ ───────────────────────────────────────────────────────

def stamp(name: str, target: str, args) -> None:
    """Copy branding/_template/ to branding/<name>/. Never replaces one."""
    if os.path.exists(target):
        fail(f"branding/{name}/ already exists; nothing to stamp.")

    existing = [c for c in active_clients() if c != name]
    if existing:
        print(f"[new-client] warning: an active client is already present "
              f"({', '.join(sorted(existing))}). The build expects exactly one, "
              f"so remove or '_'-prefix the other before building.")

    if args.dry_run:
        print(f"[new-client] would create branding/{name}/ from _template.")
        return

    shutil.copytree(TEMPLATE, target)
    os.makedirs(os.path.join(target, "assets"), exist_ok=True)
    print(f"[new-client] created branding/{name}/ from _template.")


# ── src/content/ ─────────────────────────────────────────────────────────────

def at_risk(paths: list) -> tuple:
    """(untracked, modified) among these repo-relative paths, according to git.

    The difference matters when something is about to be deleted. A tracked,
    unmodified file is one `git checkout` away from coming back; a modified one
    can be restored only as far as its last commit; an untracked one is gone for
    good. This command destroyed an untracked seed once, so it says which is
    which before it does anything, rather than trusting "it's all in git".

    Returns empty lists when git is unavailable or this is not a repository —
    an absent safety net is worth saying nothing about, not worth failing over.
    """
    if not paths:
        return [], []
    try:
        proc = subprocess.run(
            ["git", "status", "--porcelain", "--untracked-files=all", "--"] + paths,
            cwd=ROOT, capture_output=True, text=True, timeout=20, check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return [], []
    if proc.returncode != 0:
        return [], []

    untracked, modified = [], []
    for line in proc.stdout.splitlines():
        if len(line) < 4:
            continue
        code, path = line[:2], line[3:].strip().strip('"')
        (untracked if code == "??" else modified).append(path)
    return untracked, modified


def describe_risk(paths: list, label: str) -> None:
    untracked, modified = at_risk(paths)
    if untracked:
        print(
            f"[new-client] {len(untracked)} of the {label} are NOT in git — nothing "
            "can bring them back afterwards:"
        )
        for path in untracked[:10]:
            print(f"  ? {path}")
        if len(untracked) > 10:
            print(f"  ? …and {len(untracked) - 10} more")
    if modified:
        print(
            f"[new-client] {len(modified)} of the {label} have uncommitted edits — "
            "git can only restore them as far as the last commit."
        )


def push_to_site(name: str, args) -> None:
    """Push the client's branding out over the site's content.

    Two strengths, one code path. --overwrite lets the seed win wherever it has
    something to say and leaves the rest of the live tree alone; --recreate
    empties the tree first, so the site ends up holding nothing the branding
    directory does not.

    The URL each work sits at is recorded before and read again after, which is
    what --redirects turns into 301s: a page that was at /en-ca/legal/privacy/
    and is now at /en-ca/about/legal/privacy/ is the same work, resolved by
    identity rather than by comparing paths.
    """
    seed = ingress.seed_dir(name)
    if not os.path.isdir(seed):
        fail(
            f"branding/{name}/content/ does not exist, so there is nothing "
            "to push out over the site."
        )

    codes = ingress.locale_codes()
    seed_files = ingress.markdown_files(seed)

    # The guard this command was missing. An empty seed says nothing about the
    # site, so --overwrite has no work to do and --recreate would empty the
    # tree and refill it with nothing — deleting a live site on the strength of
    # a directory that happens to be empty.
    if not seed_files:
        fail(
            f"branding/{name}/content/ holds no content files, so there is "
            "nothing to push. Refusing: --recreate against an empty seed would "
            "empty the site."
        )

    ingress.describe_seed(seed, codes, label="new-client")
    ingress.check_blog_sections(seed, codes, label="new-client")

    before = ingress.index_live(codes)
    live_files = ingress.markdown_files(ingress.LIVE)

    # Work the whole thing out first, on a run that writes nothing, so the
    # question below can say what will actually happen rather than how many
    # files are about to be touched.
    plan = ingress.reconcile(
        seed, codes, True, empty_tree=args.recreate, overwrite=args.overwrite
    )
    planned_moves, planned_gone = ingress.plan_redirects(before, plan["published"])
    orphans = ingress.unidentified_live(codes) if args.recreate else []

    print(
        f"[new-client] {'--recreate' if args.recreate else '--overwrite'}: "
        f"{len(seed_files)} seed file(s) against {len(live_files)} live file(s)."
    )
    ingress.report(plan, True, label="new-client")

    if planned_moves:
        print(f"[new-client] {len(planned_moves)} URL(s) would move:")
        for old, new in planned_moves:
            print(f"  → {old} -> {new}")
    if planned_gone:
        print(
            f"[new-client] {len(planned_gone)} published URL(s) would DISAPPEAR — the "
            "seed has no page for them, and there is nothing to redirect them to:"
        )
        for old in planned_gone:
            print(f"  ✗ {old}")
    if orphans:
        print(
            f"[new-client] {len(orphans)} live file(s) carry no sat:work, so they "
            "cannot be matched to the seed and would be deleted unrecorded:"
        )
        for rel in orphans:
            print(f"  ✗ src/content/{rel}")

    if args.dry_run:
        if planned_moves and not args.redirects:
            print("[new-client] --dry-run: pass --redirects to write 301s for those moves.")
        return

    # Say what git could and could not undo before asking, not after. --recreate
    # empties the whole tree, so the whole tree is at risk; --overwrite only
    # touches the paths the plan named.
    doomed = ["src/content"] if args.recreate else plan["writes"] + plan["removals"]
    describe_risk(doomed, "files about to be replaced or removed")

    question = (
        "Recreate src/content/ from the branding directory?"
        if args.recreate
        else "Let the branding directory overwrite the site's content?"
    )
    if not confirm(question, args.yes):
        fail("cancelled; nothing was changed.")

    if args.recreate:
        removed = ingress.wipe_live(False)
        print(f"[new-client] removed {len(removed)} content file(s) from src/content/")

    result = ingress.reconcile(
        seed, codes, False, empty_tree=args.recreate, overwrite=args.overwrite
    )
    ingress.report(result, False, label="new-client")

    moves, gone = ingress.plan_redirects(before, result["published"])

    if moves:
        print(f"[new-client] {len(moves)} URL(s) moved:")
        for old, new in moves:
            print(f"  → {old} -> {new}")
    if gone:
        print(
            f"[new-client] {len(gone)} URL(s) no longer exist and have no "
            "destination to redirect to:"
        )
        for old in gone:
            print(f"  ✗ {old}")

    if not args.redirects:
        if moves:
            print(
                "[new-client] no redirects written. Re-run with --redirects if "
                "this site is live and those URLs are published."
            )
        return

    action = "recreated from" if args.recreate else "overwritten by"
    written, skipped = ingress.write_redirects(
        moves,
        f"Moved when the site was {action} the {name} branding directory",
        args.dry_run,
    )
    verb = "would write" if args.dry_run else "wrote"
    print(f"[new-client] {verb} {len(written)} redirect(s) to src/_redirects.")
    for old, _ in skipped:
        print(f"  = {old} already has a rule; left as it is.")


# ── main ─────────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(
        prog="new-client",
        description="Start a new client, and push a client's branding out over the site.",
    )
    parser.add_argument("client", nargs="?", help="the client directory name, e.g. clientbrand.com")
    parser.add_argument("--overwrite", action="store_true",
                        help="let the branding directory replace the site's copy of the pages it publishes")
    parser.add_argument("--recreate", action="store_true",
                        help="rebuild src/content/ from the branding directory, removing what it does not have")
    parser.add_argument("--redirects", action="store_true",
                        help="with either of those, write 301s for the URLs that move")
    parser.add_argument("--dry-run", action="store_true", help="report what would happen, and change nothing")
    parser.add_argument("--yes", action="store_true", help="skip the confirmation prompts")
    args = parser.parse_args()

    if not args.client or not args.client.strip():
        parser.print_help()
        return 1
    name = args.client.strip().strip("/")

    if name.startswith("_"):
        fail(f"'{name}' is reserved — names starting with '_' are templates, not clients.")
    if "/" in name or os.sep in name:
        fail(f"'{name}' must be a single directory name, not a path.")
    if not os.path.isdir(TEMPLATE):
        fail("branding/_template/ not found; nothing to copy from.")
    if args.redirects and not (args.overwrite or args.recreate):
        fail("--redirects records what --overwrite or --recreate moves; pass one of those with it.")
    if args.overwrite and args.recreate:
        fail(
            "--recreate already replaces everything --overwrite would; pass one or "
            "the other, so it is clear whether pages the seed omits survive."
        )

    target = os.path.join(BRANDING, name)
    stamping = not os.path.exists(target)

    if stamping:
        stamp(name, target, args)
    else:
        print(f"[new-client] using the existing branding/{name}/.")

    if args.overwrite or args.recreate:
        push_to_site(name, args)

    if stamping:
        print("Next:")
        print(f"  1. Fill in branding/{name}/brand.yaml, fonts.yaml, and site.yaml (replace the TODO values).")
        print(f"  2. Add the brand images to branding/{name}/assets/ (see its README.md for the slots).")
        print( "  3. Regenerate and validate:  npm run build:fonts && npm run build")
    elif (args.overwrite or args.recreate) and not args.dry_run:
        print("Next:  npm run build")
    return 0


if __name__ == "__main__":
    sys.exit(main())
