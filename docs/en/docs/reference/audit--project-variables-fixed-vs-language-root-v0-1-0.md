---
dc:title: "Audit: Project Variables, Fixed vs. Language Root"
dcterms:version: "0.1.0"
dc:creator: "Christopher Steel"
dc:contributor: "Claude (Anthropic)"
dc:subject:
  - "audit"
  - "i18n"
  - "configuration"
  - "accessibility"
dc:description: >
  Every variable the site generator defines or reads outside branding/,
  sorted into two categories: fixed (no correct alternate exists for the
  referent, so no locale scope is needed) and language-root candidates
  (human-language content, already locale-scoped or not yet). Uses the terms
  from vocabulary--value-language-relationships and the test from
  decision-tree--value-language-relationships-placement.
dc:publisher: "UniversalCake"
dcterms:created: "2026-08-14"
dcterms:modified: "2026-08-14"
dc:format: "text/markdown"
dc:language: "en"
sat:language_bcp47: "en"
dc:identifier: "audit--project-variables-fixed-vs-language-root"
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
      Initial draft. Surveyed .eleventy.js, src/_data/*.js, src/admin/config.yml,
      src/_includes/**/*.njk, src/pages/pages.11tydata.js, and content/blog
      front matter, excluding everything under branding/, and sorted every
      variable found into fixed and language-root candidates. Flags two
      findings: the CMS field labels in src/admin/config.yml are hardcoded
      English in both locale collections, and the locale registry's `label`
      field is human language but correctly locked as an endonym. A first
      pass, not exhaustive at the string-literal level.
---

# Audit: Project Variables, Fixed vs. Language Root

Version: 0.1.0
Status: Draft
Style Guide: style-guide--plain-language-for-general-audiences

## Abstract

This document sorts every variable the site generator defines or reads, outside `branding/`, into two categories: **fixed**, meaning no correct alternate value exists for the same referent so no locale scope is needed, and **language-root candidates**, meaning the value is human language and either already lives in a locale-scoped location or does not yet. The terms follow `vocabulary--value-language-relationships-v0-1-0.md`; the test applied to each variable is the same one `decision-tree--value-language-relationships-placement-v0-1-0.md` states formally. This is a first pass at the level of named variables and front-matter fields, not an enumeration of every one of the roughly 575 individual keys inside the locale bundles, that level of detail is noted where it applies and can be produced separately if wanted.

## Method and scope

Excluded entirely: everything under `branding/`, including `branding/_template/` and every `branding/<client>/` directory, per your instruction. This means `site.yaml`'s `name`, `tagline`, `description`, `logos`, `contact`, `social`, and `nav` fields, and `brand.yaml` and `fonts.yaml`'s tokens, are not listed here, even though templates outside `branding/` read them, they are authored and defined inside the excluded directory. `src/_data/site.json` is the generated mirror of `site.yaml` and is excluded on the same basis.

Surveyed: `.eleventy.js`, every file in `src/_data/`, `src/admin/config.yml`, every `.njk` file under `src/_includes/`, `src/pages/pages.11tydata.js`, `src/content/blog/blog.11tydata.js`, `src/content/_localeTree.js`, and the front-matter fields visible in content and blog posts. Not line-by-line grepped for every hardcoded string, the site's own `npm run check:i18n` already does that mechanically at build time; this is a pass at the level of named, reusable variables.

## Fixed variables

No correct alternate exists for the same referent, so these need no locale scope regardless of how many languages the site ships.

| Source | Variable | What it is |
| --- | --- | --- |
| `src/_data/locales.js`, per registry entry | `code`, `dir`, `fonts`, `uioLocale`, `pseudo`, `htmlLang` | URL segment, text direction, font stylesheet path, Infusion locale key, pseudo-locale flag, BCP 47 tag. Machine identifiers; `htmlLang` drives which pronunciation an assistive technology picks, but the tag itself is not spoken text |
| `src/_data/locales.js` | `default` | which registry entry is the default locale |
| Content and blog front matter | `sat:work`, `dc:identifier` | UUIDs, identity only |
| Page and content front matter | `routeKey`, `pageKey` | internal keys into a locale bundle's `routes` table or template branching, never displayed |
| Page and content front matter | `css` | stylesheet basenames to load |
| Page, content, and blog front matter | `footerMuted`, `draft`, `featured`, `nav.hidden`, `showLoader` (page override) | booleans |
| Content front matter | `order` | numeric sort key |
| Blog front matter | `category` | a language-independent slug; its display label is a language-root variable, see below |
| Blog front matter | `date` | a stored ISO 8601 instant; its human-rendered form is computed by the `readableDate` filter, not stored separately |
| Blog front matter | `image` | a file path |
| Nav, footer, and final-cta front-matter params | `ctaId`, `navCtaContact`/`navCtaRoute`, `mobileCta1Contact`/`mobileCta1Route`, `mobileCta2Contact`/`mobileCta2Route`, `ctaBtn1Contact`/`ctaBtn1Route`, `ctaBtn2Contact`/`ctaBtn2Route` | routing keys, resolved against `site.contact` or `urls`, never displayed themselves |
| `.eleventy.js` | `dir.input`/`includes`/`output`, `htmlTemplateEngine`, `templateFormats` | build configuration |
| `.eleventy.js` | filter and collection names: `byPath`, `childrenOf`, `pickFeatured`, `readableDate`, `isoDate`, `posts_<locale>`, `content_<locale>` | code identifiers |
| `.eleventy.js` | `ELEVENTY_RUN_MODE`, `PSEUDO` | environment and build flags |
| `.eleventy.js` | the Infusion vendor path, every passthrough-copy source and destination | file paths |
| `src/pages/pages.11tydata.js` | `DEFAULT_LANG` | fallback BCP 47 tag used outside a page that knows its own locale |
| `src/_data/menu.js` | `DEFAULT_PINNED`, `DEFAULT_ORDER`, `PINNED_FIRST`, `PINNED_LAST` | structural constants; `DEFAULT_ORDER`'s values (`"about"`, `"services"`, `"blog"`) are route keys, not display text |
| `src/_data/menu.js` output | `key`, `routeKey`, `labelKey`, `url`, `rank` | machine keys, resolved URLs, sort ranks |
| `src/_data/workIndex.js`, `src/_data/contentWorkIndex.js` | the work-UUID to `{locale: slug}` index | an index of identifiers |
| `src/_data/buildYear.js` | the computed year | a number, identical in every locale |
| `src/_includes/layouts/base.njk` | the `og:type` default `"website"`, the `robots` `noindex` keyword, `googleSiteVerification` | protocol-standard or machine tokens, not prose |

## Language-root variables

Human language: either wording is expected to differ by locale to preserve meaning (translated), or the written form legitimately varies by script or convention while the referent stays fixed (transliterated).

### Already correctly locale-scoped

| Source | Variable | Notes |
| --- | --- | --- |
| `src/_locales/en-ca.json`, `src/_locales/fr-ca.json` | ~575 keys across `common.nav.*` (including the `logoHome` pattern), `common.footer.*`, `common.cta.*`, `common.a11y.*`, `routes.*`, and per-page namespaces (`home`, `about`, `services`, `blog`, `contact`, `freeAudit`, `privacy`) each with `meta.*`, `pageCta.*`, `pageNav.*`, `hero.titleLines`, and body copy | Not individually enumerated here, listed by namespace; ask if you want the full key list |
| `src/_locales/<code>.json` | `blog.filters.*` | the display labels for the fixed `category` slugs above |
| `src/content/<locale>/**/*.md`, `src/content/blog/<locale>/*.md` | `title`, `description`/`excerpt`, `body`, `nav.label` (section label override), `readtime` | already locale-scoped by directory, one file per language |
| `src/_data/locales.js`, per registry entry | `label` | the endonym, `"English"` / `"Français"`. Human language, but correctly a locked value, an endonym is shown the same way regardless of the viewer's locale by convention, not translated per viewer, so one string per registry entry is right as it stands |

### Not yet locale-scoped, worth a decision

| Source | Variable | Finding |
| --- | --- | --- |
| `src/admin/config.yml` | Field labels: `"Title"`, `"Category"`, `"Publish date"`, `"Short summary"`, `"Read time"`, `"Cover image"`, `"Feature on this listing?"`, `"Save as draft (hide from site)"`, `"Translation link (sat:work)"`, `"Body"` | Hardcoded English in **both** the `blog_en` and `blog_fr` collections. The `blog_fr` collection's own label and description text is translated (`"Articles en francais..."`), but its field-level labels are not, an editor working in the French collection still sees English field names. This file sits outside the site's `_locales` mechanism entirely, a static YAML the CMS reads directly, so there is no existing bundle for it. Worth a decision: does this matter, since only content editors see it, not site visitors, or should Sveltia's own i18n widget config be used to translate it? |

## License

This document, *Audit: Project Variables, Fixed vs. Language Root*, by **Christopher Steel**, with AI assistance from **Claude (Anthropic)**, is licensed under the [GNU Affero General Public License v3.0 or later](https://www.gnu.org/licenses/agpl-3.0.html).

## Changelog

| Version | Status | Notes |
| --- | --- | --- |
| 0.1.0 | Draft | Initial draft; every variable outside branding/ sorted into fixed and language-root candidates, with the CMS field-label gap and the locale-registry endonym flagged for a decision |
