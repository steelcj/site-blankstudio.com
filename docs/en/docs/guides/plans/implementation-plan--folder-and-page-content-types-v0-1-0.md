---
dc:title: "Implementation Plan: Folder and Page Content Types"
dcterms:version: "0.1.0"
dc:creator: "Christopher Steel"
dc:contributor: "Claude (Anthropic)"
dc:subject:
  - "content-types"
  - "eleventy"
  - "sveltia"
  - "folder"
  - "page"
  - "schema"
  - "behaviors"
dc:description: >
  A phased plan to add two native content types to the Eleventy and Sveltia
  template, modelled on the uc.app.contenttypes vocabulary: Page, a markdown
  content item, and Folder, a container that organizes items.
dc:publisher: "UniversalCake"
dcterms:created: "2026-08-09"
dcterms:modified: "2026-08-09"
dc:format: "text/markdown"
dc:language: "en"
sat:language_bcp47: "en"
dc:identifier: "implementation-plan--folder-and-page-content-types"
dcterms:rightsHolder: "Christopher Steel"
dc:rights: >
  Copyright 2026 Christopher Steel / UniversalCake.
  SPDX-License-Identifier: AGPL-3.0-or-later
sat:uuid: ""
sat:version_at_creation: ""
sat:migration_status: pre-sat
sat:changelog:
  - version: "0.1.0"
    date: "2026-08-09"
    author: "Christopher Steel"
    notes: >
      Initial draft. Phased plan to realize Folder and Page as native content
      types on the Eleventy and Sveltia template, modelled on the
      uc.app.contenttypes vocabulary. Covers the Page item type, the Folder
      container type, behaviors as reusable conventions, a content validator,
      and coexistence with the existing bespoke njk pages.
---

# Implementation Plan: Folder and Page Content Types

Version: 0.1.0
Status: Draft — proposed
Style Guide: style-guide--plain-language-for-general-audiences

## Abstract

**Folder & Page content types** — a five-phase plan mapping the `uc.app.contenttypes` vocabulary onto the stack without importing its code: Page as a per-locale markdown item reusing the blog's proven `sat:work`/routing machinery, Folder as a container, behaviors as reusable front-matter conventions, a `check:content` validator, and a clear rule for when to use a content-type Page versus a bespoke `.njk` template page.

On your mid-turn point — yes, and I've made it the explicit organizing principle of the content-types plan: **the content tree is the file tree.** A Folder is a real directory, a Page is a real file inside it, containment is just a file living in a directory, and a Page's URL mirrors its path on disk — no database, no hidden index. The only place that isn't perfectly clean is the Sveltia layer (its nested-folder support is limited), which I've flagged as the one open decision rather than a filesystem problem.

## Goal

Give the template two first-class, editor-friendly content types, modelled on the `uc.app.contenttypes` vocabulary but realized natively in Eleventy and Sveltia:

- **Page** — an *item*: standard page content authored in markdown.
- **Folder** — a *container*: a directory that organizes Pages and other items.

Keeping the UniversalCake names and container-versus-item shape means the template's content model reads the same as the wider UC vocabulary, which eases both authoring and any future migration, while the runtime stays the static Eleventy and Sveltia stack we actually ship on.

Organizing principle: the content tree is the file tree. A Folder is a real directory and a Page is a real file inside it, so containment is nothing more than a file living in a directory, and a Page's URL mirrors its path on disk. There is no database and no hidden index — what you see in the repo is the content structure. Eleventy already builds this way, which is why the plan below adds conventions and layouts rather than a content system.

## How the uc.app.contenttypes model maps here

The `uc.app.contenttypes` framework is a CMS runtime and is not present in this repo. This plan borrows its *model*, not its code, and binds each concept to something Eleventy and Sveltia already do.

| uc.app.contenttypes concept | Realized here as |
| --- | --- |
| Container vs item | A Folder is a directory with an index and children; a Page is a markdown leaf file |
| Schema (fields per type) | A front-matter contract per type, plus the matching Sveltia collection fields |
| Behaviors (publishing, tags, relations) | Reusable front-matter conventions and shared `*.11tydata.js` helpers |
| Content Types control panel | Sveltia CMS collections in `src/admin/config.yml` |
| `uc.api.content.create()` | Authoring a markdown file (by hand or through Sveltia) under the type's folder |

## Current state

Today the template has two different content shapes, and neither is a general markdown Page. Bespoke pages are hand-authored Nunjucks templates in `src/pages/` (`services.njk`, `blog.njk`, `contact.njk`, `free-audit.njk`); each declares a `routeKey`, extends `layouts/base.njk`, is paginated once per locale by `src/pages/pages.11tydata.js`, and pulls its copy from the `src/_locales/<code>.json` bundle through the `t` object. Blog posts are the closest thing to an item type: per-locale markdown in `src/content/blog/<code>/`, rendered by `article.njk`, editable in Sveltia, with translations paired through a `sat:work` value resolved via `workIndex`. There is no container ("Folder") concept anywhere, and no markdown "Page" that an editor can create.

The Page type below deliberately reuses the blog's proven machinery — per-locale folders, `sat:work` pairing, computed permalinks and `alternates` — rather than inventing a parallel one.

## Phases

### Phase 1 — The Page content type (item)

Add a markdown Page type authored per locale, editable in Sveltia, slotting into the existing i18n routing.

Content lives at `src/content/pages/<code>/<slug>.md`, mirroring the blog's per-locale layout so locale is read from the path. Each Page's front matter is its schema: `title`, `slug`, `description` (SEO), optional `ogImage`, `sat:work` (translation pairing), `draft`, and the markdown `body`. A new layout `src/_includes/layouts/page.njk` renders the body inside the `base.njk` chrome. A new `src/content/pages/pages.11tydata.js` sets `layout: page.njk`, derives locale from the path, computes the permalink from the slug, and reuses the blog's `sat:work`/`workIndex` logic for `alternates`, `switcher`, and `xDefault`. Two Sveltia collections, "Pages (English)" and "Pages (Français)", expose the schema over `src/content/pages/<code>/`.

Deliverables: `page.njk`, `src/content/pages/pages.11tydata.js`, the two Sveltia collections in `src/admin/config.yml`, and one example Page per locale.

Done when: an editor can create a markdown Page in Sveltia, it builds at the right per-locale URL with correct `<title>`, description, and hreflang, and its translation pairs through `sat:work`.

### Phase 2 — The Folder content type (container)

Add a Folder type that organizes Pages, again per locale.

A Folder is a directory `src/content/pages/<code>/<folder>/` containing an `index.md` (the Folder's own metadata: `title`, `description`, and an ordering field) and its child `.md` Pages. A layout `src/_includes/layouts/folder.njk` renders the Folder's title and a listing of its published children. An Eleventy collection gathers each Folder's children by directory so the listing and any Folder-driven navigation read from one source. The allowed-children rule is stated in the schema (a Folder contains Pages and Folders; a Page contains nothing).

On disk this is entirely natural: the directory contains the files, and that containment *is* the content model. The friction is only at the CMS layer, because Sveltia has limited nested-folder support, so the CMS representation is a design choice to settle in this phase: either one collection per Folder, or the nested/beta collection mode. This is recorded as an open question below.

Deliverables: `folder.njk`, a `children`-by-directory Eleventy collection, the `index.md` convention documented, and one example Folder with two child Pages per locale.

Done when: a Folder renders its own page plus a listing of its published children in the right order, and adding a child Page makes it appear with no template edit.

### Phase 3 — Behaviors as reusable conventions

Model the uc "behaviors" as reusable front-matter conventions plus shared `*.11tydata.js` helpers, so a type gains a feature by opting in rather than by bespoke code.

Publishing dates: an `effective` / `expires` pair (and the existing `draft` flag) filtered in a shared helper so future-dated or expired items do not build into collections. Tags: a `tags` array feeding Eleventy collections for tag listings. Relations: a `related` list of slugs, resolved to links at render. Each behavior is documented once and applied by adding the field, mirroring how a uc behavior is attached to a type.

Deliverables: a `src/_includes/lib/behaviors.js` (or equivalent shared helpers), documented front-matter fields, and the Page and Folder types opting into publishing dates.

Done when: setting `draft`, `effective`, or `expires` on any item changes whether it builds, through one shared code path used by both types.

### Phase 4 — Schema validation

Add `scripts/check-content.js`, wired as `npm run check:content`, mirroring the existing `check:i18n`. It asserts the required front-matter fields per type, that every `slug` is unique within a locale, that a Folder's children are allowed types, and that `sat:work` pairings resolve. Wire it into the build alongside the other checks.

Deliverables: `scripts/check-content.js`, the `check:content` script, and its place in the build pipeline.

Done when: a Page missing a required field, or a duplicate slug, fails `npm run build` with a message naming the file and the problem.

### Phase 5 — Coexistence and migration

State plainly when to use which shape, so the two do not blur. The bespoke `src/pages/*.njk` remain "template pages": developer-owned, design-heavy landing pages (home, services) whose copy lives in the locale bundles. The Page and Folder types are for standard content pages an editor creates and maintains in markdown. Optionally migrate a simple existing page (for example a future "privacy" page) to the Page type as a worked example.

Deliverables: a short "which type do I use" note in the content-types documentation, and one optional migrated example.

Done when: a teammate can decide, without asking, whether a new page is a template page or a Page content type.

## Relationship to the Canonical Loop

The content-type *machinery* is template-owned and travels down the [upstream](implementation-plan--client-customization-brand-config-system-v0-1-0.md) path: the layouts (`page.njk`, `folder.njk`), the `*.11tydata.js` data files, the behavior helpers, the Sveltia collection definitions, and the validator. The actual Folder and Page *content* a client authors is client-owned, exactly like their blog posts. This keeps the same boundary the customization plan relies on: improving the Page type in canonical merges cleanly into a client fork without touching the client's own pages.

## Risks and open questions

Sveltia and Decap have limited support for arbitrarily nested folder collections, so the Folder authoring experience is the main risk; the CMS representation (one collection per Folder versus nested mode) needs a decision, and deep hierarchies may need to be kept shallow. Reusing the blog's `sat:work`/`workIndex` for Pages assumes that index is generalizable beyond posts; confirm it keys cleanly across content types. Folder listings and navigation should read from one Eleventy collection to avoid two sources of truth for child order.

Open questions:

- Sveltia representation of Folders: one collection per Folder, or nested/beta mode?
- Do Pages route under a locale-translated segment like blog posts (`routeKey`-style), or by raw slug and folder path?
- Should Folder ordering be a manual weight, alphabetical, or by date, as the default behavior?
- Does the existing `workIndex` generalize to Pages and Folders, or does it need a content-type-aware key?

## License

This document, *Implementation Plan: Folder and Page Content Types*, by **Christopher Steel**, with AI assistance from **Claude (Anthropic)**, is licensed under the [GNU Affero General Public License v3.0 or later](https://www.gnu.org/licenses/agpl-3.0.html).

## Changelog

| Version | Status | Notes |
| --- | --- | --- |
| 0.1.0 | Draft | Initial draft; maps the uc.app.contenttypes model onto Eleventy and Sveltia and plans the Page item type, the Folder container type, behaviors as reusable conventions, a `check:content` validator, and coexistence with the existing njk pages |
