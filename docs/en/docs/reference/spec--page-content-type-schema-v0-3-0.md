---
dc:title: "Spec: Page Content-Type Schema"
dcterms:version: "0.3.0"
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
  populated or not, dot-syntax qualifiers for date role (created, modified,
  valid), and sat:work as the one deliberate non-DC field.
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
      Superseded the behavior-annotated draft. Rejected dcterms: in favor of
      plain dc:, and, in the same move, also set aside DCMI's legacy dot-
      syntax qualifiers, on the reasoning that they had no legacy precedent
      for rightsHolder and version. That reasoning did not hold up: neither
      field is part of this content schema. Adopted a single unqualified
      dc:date and flagged the created/modified/valid distinction as an
      unresolved gap. Narrowed scope to Page only.
  - version: "0.3.0"
    date: "2026-08-14"
    author: "Christopher Steel"
    notes: >
      Corrected the 0.2.0 rationale and reinstated DCMI dot-syntax qualifiers
      for date role specifically: dc:date.created, dc:date.modified,
      dc:date.valid, closing the gap 0.2.0 left open. Nowhere else in the
      schema; every other field stays a plain, unqualified dc: element.
---

# Spec: Page Content-Type Schema

Version: 0.3.0
Status: Draft — proposed
Style Guide: style-guide--plain-language-for-general-audiences

## Abstract

This document specifies the front-matter shape for the Page content type: the full 15-element Dublin Core Metadata Element Set, authored in every file whether a given field is populated or not, `sat:work` as the one deliberate non-DC field, and, new in this version, DCMI's legacy dot-syntax qualifiers (`dc:date.created`, `dc:date.modified`, `dc:date.valid`) for date role specifically. Everything else stays a single, unqualified `dc:` element.

This remains a draft for discussion, not an adopted schema.

## Correcting 0.2.0

0.2.0 rejected dot syntax along with `dcterms:`, in the same move, on the reasoning that dot syntax had no legacy precedent for fields like `rightsHolder` and `version`. That reasoning does not hold up under its own weight: neither field is part of this content schema, both belong to this project's separate documentation-frontmatter convention. Using an inconsistency in fields that were never in scope to reject a tool for fields that are in scope was a mistake, not a considered decision.

It was also a mistake against the document's own findings: 0.2.0 flagged, in its own field notes, that a single unqualified `dc:date` cannot distinguish created from modified from valid, and named that "the one place pure DC can't follow." Dot syntax is precisely the precedent that closes that gap. Discarding the tool and then separately flagging the gap it would have closed was inconsistent.

This version corrects it: dot syntax returns, scoped to date role only, where it has clean, real DCMI precedent (`Date.Created`, `Date.Modified`, `Date.Valid` are documented qualifiers of the `Date` element). It is not reintroduced anywhere else in the schema; every non-date field remains a single unqualified `dc:` element, per the KISS, full-set-every-time decision from 0.2.0, which still stands.

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
dc:date.created: "2026-08-14"
dc:date.modified: "2026-08-14"
dc:date.valid: ""
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

Carried forward from 0.2.0, with the date entry updated:

- `dc:title`, `dc:identifier`, `dc:rights`, and now `dc:date.created`/`dc:date.modified` carry real, page-specific values on every page.
- `dc:creator`, `dc:contributor`, `dc:subject` are populated when known, empty otherwise (`[]`), rather than omitted.
- `dc:publisher`, `dc:format`, `dc:language` hold the same value on effectively every page today, but are authored per file rather than left implicit.
- `dc:date.valid` is left empty (`""`) until an expiration concept is actually adopted; the field is present, not conditional.
- `dc:type` uses the DCMI Type Vocabulary's `"Text"` for now.
- `dc:source`, `dc:coverage` are left empty (`""`) on every page seen so far.
- `dc:relation` is left empty (`[]`); `sat:work` still carries the translation-pairing relationship. Migrating it into `dc:relation` remains an open question, not adopted, unchanged from 0.2.0.
- `dc:description`, `dc:date` (unqualified) — no longer used as a single generic date; replaced entirely by the qualified trio above.

## What this document does not cover

Unchanged from 0.2.0: the publishing-vector fields (`routeKey`, `pageKey`, `css`, `footerMuted`, `draft`, `nav.hidden`, `nav.label`, `order`, `image`) are out of scope, they were never proposed as DC terms. Blog-post composition is also out of scope; this document covers Page content only.

## Open questions

Carried forward from 0.2.0, unchanged, plus one new:

- Should `sat:work` migrate into `dc:relation`, holding the group URN? Still not adopted.
- Is `dc:type: "Text"` the right constant for every Page long-term?
- Does `dc:source` or `dc:coverage` ever get real use on this site?
- Should `dc:publisher`/`dc:format`/`dc:language` be hand-authored per file, or stamped by a build step from `site.yaml`/the locale registry?
- New: now that `dc:date.valid` exists as a field, does that settle the expiration question 0.1.0 and 0.2.0 both left open, or is expiration a bigger behavior change (scheduled unpublishing logic) than adding the field implies?

## License

This document, *Spec: Page Content-Type Schema*, by **Christopher Steel**, with AI assistance from **Claude (Anthropic)**, is licensed under the [GNU Affero General Public License v3.0 or later](https://www.gnu.org/licenses/agpl-3.0.html).

## Changelog

| Version | Status | Notes |
| --- | --- | --- |
| 0.1.0 | Draft | Initial draft; uc.* behavior-composition schema for page and blog-post, borrowed from Plone, annotated by layer and vocabulary relationship |
| 0.2.0 | Draft | Superseded with the full 15-element Dublin Core set, authored every time; dropped dcterms: and, on flawed reasoning, dot syntax too; kept sat:work as the sole non-DC field; narrowed scope to Page only |
| 0.3.0 | Draft | Corrected the 0.2.0 rationale; reinstated dot-syntax qualifiers for date role only (dc:date.created, dc:date.modified, dc:date.valid), closing the gap 0.2.0 left open; every other field stays unqualified |
