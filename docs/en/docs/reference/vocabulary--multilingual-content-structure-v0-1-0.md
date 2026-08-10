---
dc:title: "Vocabulary and Definitions: Multilingual Content Structure"
dcterms:version: "0.1.0"
dc:creator: "Christopher Steel"
dc:contributor: "Claude (Anthropic)"
dc:subject:
  - "vocabulary"
  - "multilingual"
  - "i18n"
  - "content-structure"
  - "translation"
  - "sat"
dc:description: >
  The project's working vocabulary for how content in multiple languages is
  organized on the filesystem and how translations are connected: language
  roots, the avoided parallel structure, mirrored translations, unmirrored
  content, and the work identity that links counterparts.
dc:publisher: "UniversalCake"
dcterms:created: "2026-08-10"
dcterms:modified: "2026-08-10"
dc:format: "text/markdown"
dc:language: "en"
sat:language_bcp47: "en"
dc:identifier: "vocabulary--multilingual-content-structure"
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
      Initial draft. Defines the multilingual content-structure vocabulary for
      the project: language root, parallel structure (avoided), mirrored
      translation, unmirrored content, work identity, and language-switch
      behaviour. Terms originate in Source Archive Tools (SAT); these are the
      project's working definitions and should be reconciled with SAT's
      canonical definitions where they differ.
---

# Vocabulary and Definitions: Multilingual Content Structure

Version: 0.1.0
Status: Draft
Style Guide: style-guide--plain-language-for-general-audiences

## Abstract

This document defines the words the project uses for organizing content in more than one language, and for connecting the translations. It distinguishes three structural relationships between a page and its counterparts in other languages — *parallel* (which we avoid), *mirrored*, and *unmirrored* — and names the mechanism that links mirrored counterparts.

The terms originate in Source Archive Tools (SAT). The definitions here are the project's working ones; where SAT states them canonically, SAT wins, and this document should be reconciled to it.

## Language root

The top-level content directory for one language edition, for example `content/en-ca/` and `content/fr-ca/`. Each language root is an **independent tree**, and a page's URL begins with its root's segment (`/en-ca/…`, `/fr-ca/…`).

Independent roots are a deliberate choice. They keep each language's tree clean and readable as translations accumulate, rather than interleaving several languages inside one shared structure.

## Parallel structure (avoided)

Every path and filename is identical across languages, differing only by the language root: `content/en-ca/home/index.md` and `content/fr-ca/home/index.md`.

This is the older approach, and **we avoid it.** It forces one language's names (usually English) onto every language, and it couples the trees so tightly that they cannot diverge where they should. It is named here only so it can be recognized and rejected.

## Mirrored translation

A page's counterpart exists in another language with a **localized path and filename**, carrying the same meaning. `content/en-ca/home/` (or `welcome/`) mirrors `content/fr-ca/accueil/`. The paths and names differ; the meaning is as close to identical as possible.

Mirrored pages share **language-neutral assets** — the same images and layout — and differ only in text, path, and localized labels. A real example is the `realisations` page on poirierpeintureplus.com: identical imagery and structure across the two languages, with translated copy and a translated form, at a French-named path.

Counterparts are connected by a shared [work identity](#work-identity), not by matching paths, so a language switcher and `hreflang` can pair them even though the paths differ. Mirrored content is the **site spine** — the pages every language edition is expected to carry: home, about, services, contact, legal.

## Unmirrored content

Each language's content stands alone, with **no required counterpart**; the editions may hold entirely different items.

The clear example is a bilingual news site: the English edition's front page is an English newspaper, and the French edition's is a French newspaper carrying different stories. Neither is a translation of the other. Because there is no counterpart, switching language cannot make a one-to-one jump; it falls back (to that language's section index, or its home) rather than following a broken pairing, and unmirrored items do not force an `hreflang` pair.

Unmirrored keeps a language's tree honest: it holds what actually exists in that language, uncrowded by untranslated stubs.

## Work identity

The shared identifier that links mirrored counterparts across language roots, **independent of path**. It is the `sat:work` front-matter field: two files carrying the same `sat:work` value are the same work in two languages. A build-time index resolves the counterparts, and that resolution drives the language switcher and the `hreflang` alternates.

The value is a **UUID** — `urn:uuid:…` — not a human-readable name, because names, slugs, and paths change over time and a stable identity must not. This is SAT's rule: correspondence is derived from an opaque, permanent identity through a lookup table, never from names or paths. SAT assigns and manages these UUIDs; this site is one **publishing vector** SAT outputs to (alongside targets such as MkDocs, HTML, and PDF), so the UUIDs it renders originate upstream in SAT.

Mirrored content carries a `sat:work`; unmirrored content carries none (or a unique one with no counterpart).

## Language-switch behaviour

For a **mirrored** page whose counterpart exists, the switcher jumps to it, resolved by work identity — `/en-ca/home/` to `/fr-ca/accueil/`, even though the paths differ.

For an **unmirrored** page there is no counterpart, so the switcher falls back — to that language's section index, or the language home — rather than offering a dead link. This is already how the blog behaves for a post that has no translation yet.

A **mirrored page whose counterpart is missing** is a distinct case, because on a mirrored site every page is *expected* to be translated. The absence is a gap to fill, not normal behaviour, so it should be surfaced — not hidden — to three audiences:

- **The visitor** who tries to switch: an honest notice rather than a silent redirect, for example "No French equivalent of this document is currently available," with the option to stay in the current language or go to that language's section index or home. The visitor never hits a dead link, and learns *why* the translation did not appear.
- **The site owner**: a build-time warning listing the mirrored works that lack a counterpart, down the same channel as the existing i18n checks — the `workIndex` already knows which they are — and optionally a visible badge in a preview build.
- **Translators**: the same gap report doubles as a translation to-do — it names exactly which pages still need a counterpart in each language.

The mirrored / unmirrored designation is what tells the system which missing counterparts to treat as gaps to report and which to accept in silence.

## How this shapes the content tree

Putting the terms together, the project's content tree is:

- Single, independent language roots (`content/en-ca/`, `content/fr-ca/`).
- Localized paths and filenames within each root — mirrored, not parallel.
- Language-neutral assets shared across editions; only text, path, and labels localize.
- Translations connected by `sat:work`, resolved at build time, never by matching paths.
- A mirrored site spine (home, about, services, contact, legal), with room for unmirrored streams (such as news) where the editions genuinely differ.

## License

This document, *Vocabulary and Definitions: Multilingual Content Structure*, by **Christopher Steel**, with AI assistance from **Claude (Anthropic)**, is licensed under the [GNU Affero General Public License v3.0 or later](https://www.gnu.org/licenses/agpl-3.0.html).

## Changelog

| Version | Status | Notes |
| --- | --- | --- |
| 0.1.0 | Draft | Initial draft; defines language root, parallel structure (avoided), mirrored translation, unmirrored content, work identity (`sat:work`, a UUID managed by SAT, of which this site is a publishing vector), and language-switch behaviour — including surfacing a missing counterpart on a mirrored page to the visitor (an honest notice), the site owner (a build warning), and translators (a to-do) — with the poirierpeintureplus and two-newspapers examples |
