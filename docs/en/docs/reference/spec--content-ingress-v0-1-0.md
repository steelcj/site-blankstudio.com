---
dc:title: "Specification: Content Ingress (Repeatable Seeding)"
dcterms:version: "0.1.0"
dc:creator: "Christopher Steel"
dc:contributor: "Claude (Anthropic)"
dc:subject:
  - "ingress"
  - "content"
  - "seeding"
  - "idempotent"
  - "sat"
  - "publishing-vector"
dc:description: >
  A repeatable, UUID-keyed process that reconciles seed content into the site's
  live content tree — adding what is missing, never clobbering edits made in the
  CMS — so a new client site stands up from one command and canonical starter
  sections can be pulled in over time.
dc:publisher: "UniversalCake"
dcterms:created: "2026-08-10"
dcterms:modified: "2026-08-10"
dc:format: "text/markdown"
dc:language: "en"
sat:language_bcp47: "en"
dc:identifier: "spec--content-ingress"
dcterms:rightsHolder: "Christopher Steel"
dc:rights: >
  Copyright 2026 Christopher Steel / UniversalCake.
  SPDX-License-Identifier: AGPL-3.0-or-later
sat:uuid: ""
sat:version_at_creation: ""
sat:migration_status: pre-sat
sat:changelog:
  - version: "0.1.0"
    date: "2026-08-10"
    author: "Christopher Steel"
    notes: >
      Initial draft. Specifies content ingress as a repeatable, UUID-keyed
      reconcile of seed content into the live content tree: the seed location,
      the add-if-absent / skip-if-present contract, non-destruction, reporting,
      why repeatable is preferred over a one-shot bootstrap, and interactions
      with the CMS, the build, upstream merges, and SAT. Complements the content
      format and multilingual vocabulary specs.
---

# Specification: Content Ingress (Repeatable Seeding)

Version: 0.1.0
Status: Draft — proposed
Style Guide: style-guide--plain-language-for-general-audiences

## Abstract

Content ingress reconciles **seed** content into the site's **live** content tree. Its purpose is to stand a new client site up from one command — branding plus a spine of real content — and then stay useful: it can be re-run whenever new seed content appears, adding only what is missing and never overwriting what a maintainer has edited.

It is deliberately **repeatable**, not a one-shot bootstrap. The identity carried by every content file (the work UUID, per *Content Format Specification*) is the memory, so ingress needs no "first run" flag: each run simply compares the seed to the live tree by identity and fills the gaps.

Until SAT's GUI exists, the seed is a hand-made or CMS-made stand-in for a SAT export. When SAT can export, it produces the same seed shape, and ingress consumes it unchanged — so building this now is forward-compatible with SAT rather than a detour.

## The two trees

- **Seed** — `branding/<client>/content/`, the starting content for a client. The new-client scaffold populates it from the canonical starters in `branding/_template/content/`; a team can add client-specific pages, and eventually SAT can write here. The seed is client-owned and merge-safe, like the rest of `branding/<client>/`.
- **Live** — `src/content/<locale>/…`, the content the site actually builds and the CMS edits. After ingress, this is the source of truth for maintainers.

Ingress moves content from the seed to the live tree. It never reads the live tree *back* into the seed — the two have different owners (the seed is the starting point; the live tree is the maintained reality).

## The reconcile contract

Ingress walks the seed and, for each content file:

1. Reads its **work identity** (the `sat:work` UUID) and its **locale** (from its path).
2. Asks the live tree: is there already an expression of this work in this locale? (Resolved through `contentWorkIndex`, which maps a work UUID to its per-locale URL — a work has at most one expression per language.)
3. **If absent** — copies the seed file into the live tree at its localized path, creating directories as needed. If the seed file carries no UUID, one is generated and written (the same identity-stamping the `new-content` scaffold does).
4. **If present** — skips it, leaving the live file exactly as it is. A maintainer may have edited it; ingress must not overwrite that.
5. **Never deletes.** Removing a file from the seed does not remove it from the live tree.

It finishes by **reporting** what it did: the works added and the works skipped, per locale.

Two consequences make it safe to run at any time:

- **Idempotent.** Run it twice with no seed change and the second run is a no-op — everything already exists, so everything is skipped.
- **Additive.** Add a new starter section to the seed (say `about/`, after `legal/`), run ingress, and only the new works are added; nothing else is touched.

## Why repeatable, not one-shot

A one-shot bootstrap answers only "set up a new site." A repeatable reconcile answers that *and* "bring a new canonical starter section into an existing client," and "top up a partially translated work with its missing language." Because the check is by identity, re-running is always safe, so there is no reason to make it once-only. It also composes with the canonical model: `git merge upstream` brings down improvements to the *machine* (layouts, generators), and ingress brings down additions to the *starter content* — the same drift-control philosophy, one for code and one for seed.

## Overwrite is a separate, explicit mode

The default protects live edits by skipping anything that exists. Pulling an *updated* seed page over a live one — to refresh a starter a client never customized — is a different, riskier operation and is out of the default path. If provided at all it must be explicit (a `--force`/`--update` flag) and ideally guarded, overwriting only a live page that is unchanged since it was seeded (which requires recording a content hash at ingress time). This is left as an open question rather than built by default, because silently overwriting a maintainer's work is the one thing this process must never do by accident.

## The command

Ingress is an **explicit** command — `npm run ingress` — not first-run magic wired into the build. Implicit ingress on first build is surprising and hard to reason about; an explicit command that reports what it changed is safer and clearer. Running the build never mutates the live content tree.

## Interactions

- **CMS.** After ingress, maintainers edit the live tree through the CMS. Ingress never overwrites those edits (skip-if-present), so the two coexist: ingress adds, the CMS maintains.
- **Build.** `npm run build` reads the live tree only; it neither ingresses nor mutates content. Ingress is a separate, deliberate step.
- **Upstream.** Canonical ships starter content in `branding/_template/content/`. A client repo pulls template improvements down with `git merge upstream`, then runs ingress to fold any new starter works into its live tree — additively.
- **SAT.** When SAT can export, it writes into the seed in the content format; ingress consumes it identically. SAT becomes a seed author alongside the scaffold and the CMS.

## Open questions

- Overwrite/update mode: build it now, or defer? If built, guard it with a seeded-content hash so it only refreshes untouched pages?
- Assets: does ingress also reconcile media (images) referenced by seed content, and where do those live relative to `branding/<client>/assets/` and `src/assets/`?
- Layered seed: read only `branding/<client>/content/`, or merge canonical `branding/_template/content/` under it at ingress time (client entries winning)?
- Deletion: is there ever a supervised "the seed removed this, remove it live too" mode, or is deletion always a manual CMS action?
- Locale coverage: should ingress warn when a seed work exists in one locale but not another (an incomplete mirror), tying into the missing-counterpart notices?

## License

This document, *Specification: Content Ingress (Repeatable Seeding)*, by **Christopher Steel**, with AI assistance from **Claude (Anthropic)**, is licensed under the [GNU Affero General Public License v3.0 or later](https://www.gnu.org/licenses/agpl-3.0.html).

## Changelog

| Version | Status | Notes |
| --- | --- | --- |
| 0.1.0 | Draft | Initial draft; content ingress as a repeatable, UUID-keyed reconcile (add-if-absent, skip-if-present, never delete, report), the seed and live trees, why repeatable beats one-shot, an explicit command, interactions with CMS/build/upstream/SAT, and open questions |
