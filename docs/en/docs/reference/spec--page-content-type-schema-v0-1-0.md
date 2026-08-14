---
dc:title: "Spec: Page Content-Type Schema"
dcterms:version: "0.1.0"
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
  A draft field schema for this project's page and blog-post content types,
  borrowing Plone's behavior-composition shape (a type's own schema is empty;
  fields come from named, reusable behaviors it lists) and reshaping it for
  this project: uc.* behaviors instead of plone.*, uc.markdown instead of
  rich text, and every field annotated with the vocabulary relationship from
  vocabulary--value-language-relationships and the archive-vs-publishing-
  vector layer it belongs to.
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
      Initial draft. Borrows Plone's Document/Page behavior composition
      (plone.dublincore, plone.richtext, plone.relateditems, and so on),
      renamed to uc.* and reshaped around this project's archive/publishing-
      vector split and the fixed/locked/transliterated/translated/pattern
      vocabulary. Proposes three field groups not currently in the front
      matter (tags, creator/contributor/rights, expiration date), each
      flagged status: proposed rather than adopted. Deliberately does not
      port Plone's title-driven routing, versioning, or locking behaviors.
---

# Spec: Page Content-Type Schema

Version: 0.1.0
Status: Draft — proposed
Style Guide: style-guide--plain-language-for-general-audiences

## Abstract

This document drafts a field schema for the `page` and `blog-post` content types, in the shape Plone uses for its own `Document` (Page) type: a content type's own schema is empty, and its fields come from named, reusable behaviors it composes. The behaviors here are renamed to this project's own domain (`uc.*` instead of `plone.*`, `uc.markdown` instead of rich text) and every field carries two things Plone's schema does not track: which **layer** it belongs to, the SAT archive or this site's publishing vector, and its **relationship to language**, using the fixed, locked, transliterated, translated, and pattern terms from `vocabulary--value-language-relationships-v0-1-0.md`.

This is a draft for discussion, not an adopted schema. Fields marked `status: proposed` do not exist in the project today; see `audit--project-variables-fixed-vs-language-root-v0-1-0.md` for what currently exists.

## Why behaviors, reshaped

Plone's `Document` FTI has an empty schema of its own (`document.xml` has no fields); everything comes from the behaviors it lists: `plone.dublincore`, `plone.richtext`, `plone.relateditems`, `plone.versioning`, `plone.tableofcontents`, `plone.excludefromnavigation`, `plone.namefromtitle`, `plone.shortname`, `plone.locking`. That composition idea, organize the field list into named, reusable groups rather than one flat list, is worth borrowing.

What is not borrowed, and why, is covered in its own section below; in short, several Plone behaviors solve problems specific to a live ZODB object database (versioning, locking) or to title-driven routing (namefromtitle, shortname), neither of which fits this project's git-backed, locale-first, directory-routed architecture.

## The two layers

Every field below is marked `layer: archive` or `layer: publishing-vector`:

- **archive** — the kind of fact `spec--content-format-for-the-publishing-vector-v0-1-0.md` already treats as Dublin Core metadata: title, description, body, identity. Portable. The same fact regardless of which vector eventually renders it.
- **publishing-vector** — this site's own routing and presentation: `routeKey`, `css`, `nav.hidden`, and the like. These belong to *this* vector's front matter, not to the archive record, the same distinction that spec already draws between the "recommended metadata" and vector-specific fields like `draft`.

Plone has no equivalent split, a Document's fields all live in one object. This project's split is the real architectural difference from Plone, and it is why the behavior list below does not map onto Plone's one-to-one.

## The schema

```yaml
# uc-schema--page-content-type, draft v0.1.0
#
# A content type's own field list is normally empty; fields come from the
# behaviors it composes, in Plone's shape. Every field carries:
#   relationship  fixed | locked | transliterated | translated | pattern
#                 (vocabulary--value-language-relationships-v0-1-0)
#   layer         archive | publishing-vector
#   status        proposed, when the field does not exist in the project today

behaviors:

  uc.identity:
    layer: archive
    fields:
      dc:identifier:
        type: list<string>
        relationship: fixed
        required: true
        notes: >
          Permanent opaque id (UUID) plus an optional human-readable alias,
          per spec--content-format. Per expression, not shared across locales.
      sat:work:
        type: uuid
        relationship: fixed
        required: true
        notes: >
          Translation-group id shared by every expression of one work; no
          expression is canonical. Same shape as Plone's
          plone.app.multilingual translation group, arrived at independently.

  uc.dublincore:
    layer: archive
    fields:
      dc:title:
        type: string
        relationship: translated
        required: true
      dc:description:
        type: text
        relationship: translated
        required: false
      dc:subject:
        type: list<string>
        relationship: translated
        status: proposed
        required: false
        notes: >
          Tags. Not in the current front matter. If adopted, these are shown
          to visitors, so they are translated values, not a fixed slug like
          blog's `category`.
      dc:creator:
        type: list<string>
        relationship: transliterated
        status: proposed
        required: false
        notes: >
          Person names. The referent is fixed; the written form may legally
          vary by script, the vocabulary's own worked example.
      dc:contributor:
        type: list<string>
        relationship: transliterated
        status: proposed
        required: false
      dc:rights:
        type: text
        relationship: locked
        status: proposed
        required: false
        notes: >
          One rights statement everywhere, by default. Revisit as translated
          only if a client wants locale-specific wording.
      dcterms:created:
        type: datetime
        relationship: fixed
        required: false
      dcterms:modified:
        type: datetime
        relationship: fixed
        required: false

  uc.markdown:
    layer: archive
    fields:
      body:
        type: markdown
        relationship: translated
        required: true
        primary: true
        notes: >
          Renamed from plone.richtext. Markdown (CommonMark), not stored
          HTML, per spec--content-format. One field, same as Plone's `text`.

  uc.categorization:
    layer: publishing-vector
    fields:
      category:
        type: slug
        relationship: fixed
        required: false
        notes: >
          Blog only. The slug is fixed; its display label is a locale-bundle
          key (blog.filters.*), not stored here.
      nav.label:
        type: string
        relationship: translated
        required: false
      nav.hidden:
        type: boolean
        relationship: fixed
        required: false
      featured:
        type: boolean
        relationship: fixed
        required: false
      order:
        type: integer
        relationship: fixed
        required: false

  uc.publication:
    layer: archive
    fields:
      date:
        type: datetime
        relationship: fixed
        required: true
        notes: >
          Stored instant; its human-rendered form is locale-bound via the
          readableDate filter, not stored separately.
      dcterms:valid:
        type: datetime
        relationship: fixed
        status: proposed
        required: false
        notes: "Expiration date. No equivalent exists today; Plone's IPublication.expires."

  uc.routing:
    layer: publishing-vector
    fields:
      routeKey:
        type: string
        relationship: fixed
        required: false
      pageKey:
        type: string
        relationship: fixed
        required: false
      css:
        type: list<string>
        relationship: fixed
        required: false
      footerMuted:
        type: boolean
        relationship: fixed
        required: false
      draft:
        type: boolean
        relationship: fixed
        required: false
      image:
        type: path
        relationship: fixed
        required: false
      readtime:
        type: string
        relationship: fixed
        required: false
        notes: >
          Currently authored, not computed; a candidate to derive from body
          length instead of storing, unrelated to the language question.

content-types:

  page:
    title: Page
    behaviors: [uc.identity, uc.dublincore, uc.markdown, uc.routing]
    fields: {}   # empty, like Plone's Document.xml; everything comes from behaviors

  blog-post:
    title: Blog Post
    behaviors:
      - uc.identity
      - uc.dublincore
      - uc.markdown
      - uc.categorization
      - uc.publication
      - uc.routing
    fields: {}
```

## What this deliberately does not borrow

- **`plone.namefromtitle` / `plone.shortname`** — Plone computes the URL segment from the title, editor-overridable. This project routes by locale-first directory plus `routeKey`/`pageKey`, a mirrored scheme the ADR and multilingual vocabulary already depend on. Title-driven routing would fight that, not extend it.
- **`plone.versioning` / `plone.locking`** — both exist because Plone stores content in a live ZODB object database. This project's content is files in git; git already supplies revision history, and file-based, single-writer-at-a-time editing through Sveltia does not have the concurrent-editors problem locking solves.
- **A `language` field** — Plone stores it because Plone has one flat content tree. This project's locale is structural, the directory a file lives under, so a stored `language` field would duplicate `locales.js` rather than add information.
- **Workflow states** (draft / pending / published / private) — a bigger behavior change than a schema borrows. This project keeps the existing flat `draft` boolean; whether to adopt real workflow states is a separate decision, not implied by this schema.

## Open questions

- Adopt `dc:subject` (tags), `dc:creator`/`dc:contributor`, `dc:rights`, and `dcterms:valid` (expiration), or leave them out until a concrete need appears?
- Should `uc.dublincore` and `uc.markdown` (the archive layer) live in a physically separate front-matter block from `uc.routing`/`uc.categorization` (the publishing-vector layer), or continue as one merged file the way content front matter works today, per the "current interim" note in spec--content-format?
- If `dc:creator`/`dc:contributor` are adopted, do they resolve to the same DC fields this project's own documentation already uses (`dc:creator: "Christopher Steel"`), or does content need a distinct, possibly multi-value, per-post form?
- Is `readtime` worth computing from `body` instead of storing, now that the two are formally separated into different behaviors?

## License

This document, *Spec: Page Content-Type Schema*, by **Christopher Steel**, with AI assistance from **Claude (Anthropic)**, is licensed under the [GNU Affero General Public License v3.0 or later](https://www.gnu.org/licenses/agpl-3.0.html).

## Changelog

| Version | Status | Notes |
| --- | --- | --- |
| 0.1.0 | Draft | Initial draft; a uc.* behavior-composition schema for page and blog-post content types, borrowed from Plone's Document/Page shape, reshaped around the archive/publishing-vector layer split and the fixed/locked/transliterated/translated/pattern vocabulary. Three field groups flagged proposed: tags, creator/contributor/rights, expiration date |
