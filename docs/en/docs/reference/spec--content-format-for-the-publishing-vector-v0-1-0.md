---
dc:title: "Content Format Specification: The Web Publishing Vector"
dcterms:version: "0.1.0"
dc:creator: "Christopher Steel"
dc:contributor: "Claude (Anthropic)"
dc:subject:
  - "content-format"
  - "publishing-vector"
  - "sat"
  - "dublin-core"
  - "accessibility"
  - "multilingual"
  - "metadata"
dc:description: >
  The content-file format this Eleventy site consumes as a SAT publishing
  vector: where a content file lives, its metadata (Dublin Core), its body, and
  the multilingual and accessibility rules — the shared target for authoring by
  hand, by CMS, or by SAT export.
dc:publisher: "UniversalCake"
dcterms:created: "2026-08-10"
dcterms:modified: "2026-08-10"
dc:format: "text/markdown"
dc:language: "en"
sat:language_bcp47: "en"
dc:identifier: "spec--content-format-for-the-publishing-vector"
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
      Initial draft. Specifies the content-file format for this Eleventy site as
      a SAT publishing vector, on three commitments — accessibility, multilingual
      support, and metadata. Covers the path-is-URL convention, a Dublin Core
      metadata contract (work vs expression identity, dc:identifier as a list,
      the sat:work pairing, portability, and the current interim), the body and
      accessibility rules, the three authoring paths, and how the vector consumes
      a file. Recommends, but does not yet require, migrating the content front
      matter to Dublin Core.
---

# Content Format Specification: The Web Publishing Vector

Version: 0.1.0
Status: Draft — proposed
Style Guide: style-guide--plain-language-for-general-audiences

## Abstract

This document specifies what a content file *is* for this website, considered as one **publishing vector** of Source Archive Tools (SAT). It defines where a content file lives, the metadata it carries, the shape of its body, and the multilingual and accessibility rules it must satisfy.

The format has one guiding constraint: it must be authorable three ways that all produce the same file — **by hand** in a text editor, **by a CMS** in the browser, and **by SAT** exporting from its archive. SAT is the eventual power tool, but until its GUI exists most content will be maintained by hand or in a CMS, so the format cannot depend on SAT to be correct.

It is written to three commitments: excellent accessibility, first-class multilingual support, and portable, meaningful metadata. Each has a section below.

## Commitment 1 — Accessibility

Every content file resolves to a page that is accessible by construction, not as an afterthought:

- The page is delivered in the shared shell, which provides real landmarks (`<main>`, `<nav>`, `<footer>`), a skip target, and the Infusion accessibility bar (text size, contrast, spacing, and a reading tool), loaded on demand.
- The document language and direction come from the file's locale (`<html lang dir>`), so a screen reader pronounces the page correctly and a right-to-left language lays out correctly.
- The front-matter `title` is rendered as the single `<h1>`; the body starts at `<h2>`. Headings are real headings, never bold text, so the assistive-technology outline is complete. This is the rule in *Style Guide: Navigation and Accessibility*.
- Images carry meaningful `alt` text (or empty `alt` when decorative). Motion respects `prefers-reduced-motion`.
- The target is WCAG 2.1 AA.

A content file that renders inaccessible output is a defect in the file or the layout, not an acceptable state.

## Commitment 2 — Multilingual

The vector implements the model defined in *Vocabulary and Definitions: Multilingual Content Structure*. In brief:

- **Single, independent language roots** — `src/content/<locale>/…`, each a clean tree.
- **Mirrored translations** carry localized paths and filenames with the same meaning (`/en-ca/legal/privacy/` ↔ `/fr-ca/mentions-legales/confidentialite/`), paired by a shared work identity, never by matching paths.
- **Unmirrored content** stands alone per language, with no required counterpart.
- A **missing counterpart on a mirrored page** is surfaced — an honest notice to the visitor, a build warning to the owner, and a to-do for translators — rather than a silent redirect.

The metadata section below defines the identity that makes this work.

## Commitment 3 — Metadata (Dublin Core)

Metadata is where this vector and SAT most deeply agree, and where the format should be most careful, because metadata is what survives when a file is moved, renamed, or re-published to another vector.

### Align with Dublin Core

SAT's canonical metadata is Dublin Core, and this repository's own documents already use Dublin Core front matter (`dc:title`, `dcterms:modified`, `dc:identifier`, and the `sat:` extensions). Dublin Core is also a portable standard any tool understands. Therefore this vector's content metadata **should be expressed in Dublin Core**, so that a file is legible to SAT, to this site, and to any future vector without translation.

### Two identities: work and expression

The subtlety that governs the metadata is the distinction SAT already draws (ADR-010), between a **work** and its **expressions**:

- A **work** is the abstract content — "the privacy policy." Its identity is **shared by every language version**, and it is what pairs translations.
- An **expression** is one language version of that work — the English privacy page, the French one. Each expression has its **own** identity, unique to that file.

Keeping these separate is what lets translations be linked by identity while each file remains individually addressable.

### The recommended metadata

Every content file should carry:

- `dc:title` — the page title. Rendered as `<title>` and the `<h1>`.
- `dc:language` (or `sat:language_bcp47`) — the BCP-47 tag, e.g. `en-CA`. The vector also derives locale from the path, but stating it in metadata keeps the file self-describing and portable.
- An **expression identity** — `dc:identifier`, as a **list**, holding a permanent opaque id and, optionally, a human-readable one:

  ```yaml
  dc:identifier:
    - "urn:uuid:550e8400-e29b-41d4-a716-446655440000"   # permanent, opaque
    - "legal-privacy-en"                                 # human-readable, optional
  ```

  This is the portable, DC-native way to say "this file's stable id is the UUID, and here is a friendly alias." It is better than a single bespoke field because names, slugs, and paths change while the UUID does not, and because any DC consumer already understands `dc:identifier`.

- A **work identity** — the shared id that links this expression to its translations. Today this is `sat:work` (a UUID shared by every language twin). It is deliberately *not* the same as `dc:identifier`: `dc:identifier` is unique per expression, `sat:work` is shared across the work. In pure Dublin Core this relationship can also be stated as `dcterms:isVersionOf` pointing at a work URI; whether to express the pairing as `sat:work` or as a DC relation is an open question below. Either way it stays a UUID, resolved through a lookup table, never a name.

Optional, where useful:

- `dc:description` — a short summary, used for the meta description.
- `dcterms:modified` / `dc:date` — last-updated, for display and `<time>`.
- `dc:type` — the resource type (`policy`, `article`, …), which can select a layout or drive listings.
- `draft: true` — excluded from the build.

### The current interim

The legal section, the first built to this model, currently uses `title`, `description`, and `sat:work` (a UUID) rather than the Dublin Core forms above. That is a valid interim: Eleventy reads `title`/`description` directly, and `sat:work` pairs the translations. Migrating to Dublin Core is a two-part change — rewrite the front-matter keys, and map them in the content directory data (`dc:title` → the template's `title`, the UUID in `dc:identifier`/`sat:work` → the pairing key). It is recommended, not urgent, and is captured in the open questions.

## Where a content file lives

A content file is a Markdown file under a locale root, and **its path is its URL**:

```
src/content/en-ca/legal/privacy.md          ->  /en-ca/legal/privacy/
src/content/en-ca/legal/index.md            ->  /en-ca/legal/
src/content/fr-ca/mentions-legales/…​.md      ->  /fr-ca/mentions-legales/…/
```

The path is localized (mirrored), the directory is the semantic unit (`legal/` means "these are legal pages"), and a folder's `index.md` is that folder's own page. The vector computes the URL by dropping the leading `content` segment; nothing else assigns it.

## The body

The body is Markdown (CommonMark). It begins at `<h2>` — the `<h1>` is the title. It uses real headings for structure, meaningful link text, and `alt` text on images. It carries no presentational HTML that the shell or the design system already provides. Because the same body may one day be published to another vector, it stays portable: no vector-specific shortcodes beyond what this spec defines.

## The three authoring paths

All three produce the identical file described above:

- **By hand** — a developer creates the Markdown file. To remove the one rough edge (nobody should hand-type a UUID), a `new-content` scaffold stamps a fresh file with the front matter filled in and an identity generated.
- **By CMS** — a client edits in the browser (Sveltia), once the CMS is extended to this content tree. The identity fields carry generated defaults, so a client never sees a UUID.
- **By SAT** — SAT's transmog exports from its archive into this shape, mapping its canonical Dublin Core record and the work UUID from its lookup table into the file's front matter, the same way it targets MkDocs, HTML, and PDF.

The format is the contract between them. No path is privileged; SAT is one author among three.

## How the vector consumes a file

At build time the vector:

1. Derives the **locale** from the path's first segment and the **URL** from the whole path (minus `content`).
2. Reads the **work identity** and resolves counterparts through a build-time index (`contentWorkIndex`), which reads front matter off disk to avoid the permalink-versus-alternates cycle. This drives the language switcher, the `hreflang` alternates, and the missing-counterpart notices.
3. Maps **metadata** to the shell: title to `<title>`/`<h1>`, description to the meta description, language to `<html lang dir>`.
4. Renders the **body** in the shared, accessible shell.

## Open questions

- Adopt Dublin Core front matter (`dc:title`, `dc:description`, `dc:identifier`, `dc:language`) for content now, or keep the `title`/`description`/`sat:work` interim until the migration is scheduled?
- Express the work pairing as `sat:work` (SAT's established field) or as a pure-DC `dcterms:isVersionOf` relation to a work URI? The vector can consume either; consistency with SAT decides it.
- Should `dc:identifier` always include a human-readable alias, or only the UUID?
- Is the mirrored/unmirrored designation a per-section setting (directory data) or a per-file flag, and where is it declared?
- Which `dc:type` values does the vector recognize, and do they select layouts or only drive listings?

## License

This document, *Content Format Specification: The Web Publishing Vector*, by **Christopher Steel**, with AI assistance from **Claude (Anthropic)**, is licensed under the [GNU Affero General Public License v3.0 or later](https://www.gnu.org/licenses/agpl-3.0.html).

## Changelog

| Version | Status | Notes |
| --- | --- | --- |
| 0.1.0 | Draft | Initial draft; the content-file format for this SAT publishing vector on three commitments (accessibility, multilingual, metadata), with the path-is-URL convention, a Dublin Core metadata contract distinguishing work and expression identity, the three authoring paths, and how the vector consumes a file |
