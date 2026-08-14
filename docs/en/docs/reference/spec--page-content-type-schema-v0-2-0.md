---
dc:title: "Spec: Page Content-Type Schema"
dcterms:version: "0.2.0"
dc:creator: "Christopher Steel"
dc:contributor: "Claude (Anthropic)"
dc:subject:
  - "schema"
  - "content-types"
  - "plone"
  - "dublin-core"
  - "i18n"
  - "sat"
dc:description: >
  A draft field schema for this project's Page content type: the full 15-
  element Dublin Core Metadata Element Set, authored in every file whether
  populated or not, plus sat:work as the one deliberate non-DC field. Replaces
  the v0.1.0 behavior-annotated draft with the flat, converged shape reached
  through discussion.
dc:publisher: "UniversalCake"
dcterms:created: "2026-08-14"
dcterms:modified: "2026-08-14"
dc:format: "text/markdown"
dc:language: "en"
sat:language_bcp47: "en"
dc:identifier: "spec--page-content-type-schema"
dcterms:rightsHolder: "Christopher Steel"
dc:rights: >
  Copyright 2026 Christopher Steel / UniversalCake.
  SPDX-License-Identifier: AGPL-3.0-or-later
sat:uuid: ""
sat:version_at_creation: ""
sat:migration_status: pre-sat
sat:changelog:
  - version: "0.1.0"
    date: "2026-08-14"
    author: "Christopher Steel"
    notes: >
      Initial draft. Borrowed Plone's Document/Page behavior composition,
      renamed to uc.*, with fields annotated by layer (archive vs.
      publishing-vector) and vocabulary relationship. Included a blog-post
      composition and proposed dcterms:-qualified date fields.
  - version: "0.2.0"
    date: "2026-08-14"
    author: "Christopher Steel"
    notes: >
      Superseded the behavior-annotated draft after discussion. Rejected
      dcterms: qualifiers in favor of plain dc:; considered DCMI's legacy
      dot-syntax qualifiers (DC.Date.Created) and set that aside too in favor
      of the full unqualified 15-element set, authored every time, every
      file, for KISS and room for SAT to grow into. sat:work kept as the one
      deliberate non-DC field, validated against how Plone's plone.uuid and
      plone.app.multilingual keep identity and translation-grouping outside
      Dublin Core entirely. Scope narrowed to Page only; blog-post composition
      dropped. Records, but does not adopt, the idea of migrating sat:work
      into dc:relation as a group-URN.
---

# Spec: Page Content-Type Schema

Version: 0.2.0
Status: Draft — proposed
Style Guide: style-guide--plain-language-for-general-audiences

## Abstract

This document specifies the front-matter shape for the Page content type: the full 15-element Dublin Core Metadata Element Set, authored in every file, whether a given field is populated or not, plus `sat:work` as the one deliberate exception to pure Dublin Core. It replaces the v0.1.0 draft, which borrowed Plone's behavior-composition apparatus (`uc.identity`, `uc.dublincore`, `uc.routing`, and so on) with fields annotated by layer and vocabulary relationship. That structure is set aside here in favor of the flatter shape reached through discussion; see the changelog for what changed and why.

This remains a draft for discussion, not an adopted schema.

## How this shape was reached

Four decisions, in order:

1. **Plain `dc:`, not `dcterms:`.** `dcterms:` is the newer, fully qualified DCMI Terms namespace (`dcterms:created`, `dcterms:valid`, and so on). It was set aside in favor of the original 15 unqualified elements.
2. **DCMI's legacy dot syntax was considered and also set aside.** Qualified Dublin Core once expressed refinements as `Element.Qualifier` (`DC.Date.Created`, `DC.Date.Modified`) rather than promoting them to their own `dcterms:` namespace. It covers some gaps cleanly (`Date.Created` vs. `Date.Modified`) but has no legacy precedent for others (`rightsHolder`, this project's own `version`), so adopting it would mean inventing qualifiers ourselves in places and following precedent in others, an inconsistent foundation. Set aside in favor of one plain, unqualified `dc:date`.
3. **The full 15-element set, every time, every file.** Rather than deciding element-by-element whether it earns its place on a given page (the approach v0.1.0 took), every Page carries all 15, populated or not. A predictable, stable shape everywhere is worth more than a shape that varies by content, and empty fields today are exactly the room Source Archive Tools (SAT) needs to grow into as its own capabilities expand.
4. **`sat:work` stays, as the one non-DC field.** Plone's own precedent supports this rather than undercutting it: neither `plone.uuid` (object identity) nor `plone.app.multilingual` (translation grouping) is expressed as a Dublin Core term in Plone either. Both are separate, minimal facilities layered alongside DC, not folded into it. `sat:work` pairs a page to its translations, with no expression treated as canonical, the same design `plone.app.multilingual`'s translation group uses.

## The schema

```yaml
---
dc:title: "About"
dc:creator:
  - "Christopher Steel"
dc:subject:
  - "company"
  - "team"
dc:description: "Who we are and what we do."
dc:publisher: "UniversalCake"
dc:contributor: []
dc:date: "2026-08-14"
dc:type: "Text"
dc:format: "text/markdown"
dc:identifier:
  - "urn:uuid:550e8400-e29b-41d4-a716-446655440000"
  - "about"
sat:work: "urn:uuid:6f9619ff-8b86-d011-b42d-00c04fc964ff"
dc:source: ""
dc:language: "en-CA"
dc:relation: []
dc:coverage: ""
dc:rights: "Copyright 2026 Christopher Steel / UniversalCake."
---
```

## Field notes

All 15 DCMES elements, in DCMI's canonical listing order, are present regardless of whether this particular page has content for them:

- `dc:title`, `dc:description`, `dc:date`, `dc:identifier`, `dc:rights` carry real, page-specific values on every page; these were never in question.
- `dc:creator`, `dc:contributor`, `dc:subject` are populated when known, empty otherwise (`[]`), rather than omitted.
- `dc:publisher`, `dc:format`, `dc:language` hold the same value on effectively every page today (the org name, `text/markdown`, the page's locale), but are authored per file rather than left implicit, per the full-set-every-time decision.
- `dc:type` uses the DCMI Type Vocabulary's `"Text"` for now; a project-specific value only becomes useful once a second Page subtype exists.
- `dc:source`, `dc:coverage` are left empty (`""`) on every page seen so far; nothing in this content is derived from a prior source or scoped to a specific place or time, but the field stays present rather than conditional.
- `dc:relation` is left empty (`[]`) here. `sat:work` is the field actually carrying the translation-pairing relationship for now; folding that into `dc:relation` was discussed and is recorded as an open question below, not adopted.

## What this document does not cover

The publishing-vector fields from the v0.1.0 draft (`routeKey`, `pageKey`, `css`, `footerMuted`, `draft`, `nav.hidden`, `nav.label`, `order`, `image`) are out of scope here. This document is about the Dublin Core question specifically; those fields were never proposed as DC terms and their treatment is unchanged from the earlier draft. Blog-post composition is also out of scope; this document covers Page content only.

## Open questions

- Should `sat:work` migrate into `dc:relation`, holding the group URN rather than a separate `sat:` field? Considered during drafting: `dc:relation` is the DC element built for a symmetric, non-hierarchical relationship, which fits the no-canonical-expression design better than `dc:source` (which implies derivation) would. Pointing `dc:relation` at the shared group id rather than at each sibling's own identifier preserves the decoupling property Plone's translation group is built around, adding a third locale would not require editing the existing two. Not adopted; recorded here as the leading option if this changes.
- Is `dc:type: "Text"` the right constant for every Page, or should it vary once the site has more than one kind of page-like content?
- Does `dc:source` ever get used, e.g., to record that a page was migrated from a prior site or rendered from a SAT archive record, or does the identity pairing already cover that?
- Does `dc:coverage` ever apply to this site's content, or is it permanently empty for a company site with no place- or time-scoped pages?
- `dc:publisher`, `dc:format`, and `dc:language` are the same value on nearly every page; is authoring them per file the right call long-term, or should a build step stamp them from `site.yaml`/the locale registry instead of hand-authoring?

## License

This document, *Spec: Page Content-Type Schema*, by **Christopher Steel**, with AI assistance from **Claude (Anthropic)**, is licensed under the [GNU Affero General Public License v3.0 or later](https://www.gnu.org/licenses/agpl-3.0.html).

## Changelog

| Version | Status | Notes |
| --- | --- | --- |
| 0.1.0 | Draft | Initial draft; a uc.* behavior-composition schema for page and blog-post content types, borrowed from Plone's Document/Page shape, annotated by layer and vocabulary relationship |
| 0.2.0 | Draft | Superseded the behavior-annotated shape with the full 15-element Dublin Core set, authored every time; dropped dcterms: and the considered dot-syntax alternative; kept sat:work as the sole non-DC field; narrowed scope to Page only; recorded the dc:relation migration idea as an open question, not adopted |
