---
dc:title: "Asset Specification: Branding Images, Slots, and Social"
dcterms:version: "0.1.0"
dc:creator: "Christopher Steel"
dc:contributor: "Claude (Anthropic)"
dc:subject:
  - "branding"
  - "assets"
  - "images"
  - "favicon"
  - "open-graph"
  - "social"
dc:description: >
  The fixed image slots the template consumes, with per-slot role, format, and
  size; the branding/<client>/assets layout and how it overrides defaults; the
  build mechanism; and where social accounts belong (site.yaml) versus social
  share images (assets).
dc:publisher: "UniversalCake"
dcterms:created: "2026-08-09"
dcterms:modified: "2026-08-09"
dc:format: "text/markdown"
dc:language: "en"
sat:language_bcp47: "en"
dc:identifier: "asset-specification--branding-images-slots-and-social"
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
      Initial draft. Defines the fixed brand image slots the template consumes
      with per-slot format and size, the branding/<client>/assets layout and
      override-at-scaffold model, the Eleventy passthrough build mechanism, and
      the split between social accounts (data in site.yaml) and social share
      images (assets). Recommends splitting the Open Graph default off the About
      hero and parameterizing the logo path so SVG marks are possible.
---

# Asset Specification: Branding Images, Slots, and Social

Version: 0.1.0
Status: Draft — proposed
Style Guide: style-guide--plain-language-for-general-audiences

## Abstract

The template renders a fixed set of images that it references by name — a favicon, two logo lockups, a share image, some section photography, and the proof-marquee logos. This document defines those *slots*: what each is for, what format and size it should be, and where a client's files live. A client brands the site by dropping the right files into `branding/<client>/assets/`; the template wires the slots. It also settles a boundary question the sketch raised: social *accounts* are data and belong in `site.yaml`, while social *share images* are assets.

## Scope

In scope: the image slots the template consumes today, their formats and sizes, the directory layout under `branding/<client>/assets/`, and the build mechanism that serves them. Also in scope: where social accounts are declared, and the future home for social share images.

Not in scope: enforcing sizes and formats automatically (that is the `check:brand` validator's job, planned for a later phase), social share-image "theme packs," and CMS-uploaded media (which Sveltia writes to `src/assets/uploads/` and which this spec does not govern).

## The slot model

The template refers to brand images by fixed paths under `/assets/`. Each such path is a *slot*: a role the template fills with whatever file sits at that name. A client does not edit templates to rebrand; they replace the file behind each slot. The slots below are the complete set the template consumes today.

| Slot (served at `/assets/…`) | Role | Where the template uses it | Format | Size guidance |
| --- | --- | --- | --- | --- |
| `logo-lockup-dark.png` | Primary lockup, dark ink for light backgrounds | Page loader, nav bar | SVG preferred; PNG at the fixed name for now | Displays 44–108px tall — supply SVG, or PNG ≥ 220px tall |
| `logo-lockup.png` | Lockup, light for the dark footer | Footer | SVG preferred; PNG for now | Displays ~74px tall — supply SVG, or PNG ≥ 150px tall |
| `favicon.png` | Browser tab and bookmark icon | `<link rel="icon">` (base, 404) | PNG (raster required) | 48×48 minimum; see the favicon note below |
| `og-default.jpg` | Default Open Graph / social share image | `og:image` fallback | JPG or PNG (raster; SVG is not valid for OG) | 1200×630 (1.91:1) |
| `about-work.jpg` | About hero photograph | About page | JPG | ~1600px wide |
| `contact-talk.jpg` | Contact section image | Contact page | JPG | ~1600px wide |
| `audit-review.jpg` | Free-audit section image | Free-audit page | JPG | ~1600px wide |
| `services-life.jpg` | Services section image | Services page | JPG | ~1600px wide |
| `blog-featured.jpg` | Fallback cover for the blog listing and coverless posts | Blog index, posts | JPG | ~1600×900 |
| `logos/<name>.png` | Client/portfolio marks in the proof marquee | Home page | PNG or SVG with transparency | Normalized to 75px tall — supply ≥ 150px tall or SVG |

## Format and size follow the slot, not one rule

"SVG preferred" is the right default for the logo marks, because they are drawn at several sizes (loader, nav, footer) and a vector stays crisp at all of them. But two slots must not be SVG:

The favicon must be raster. Browser and OS icon support for SVG is uneven, so ship a PNG. In practice a favicon is a *set* — a 32×32 or 48×48 `favicon.png`, a 180×180 `apple-touch-icon.png`, and ideally a multi-size `favicon.ico`. Only `favicon.png` is wired today; the other two are noted as future slots.

The Open Graph share image must be raster at a fixed aspect ratio. Facebook, LinkedIn, WhatsApp and the rest expect roughly 1200×630 (1.91:1) and do not render SVG. Today the template points its `og:image` default at `about-work.jpg`, the About hero — a different crop and purpose. This spec recommends splitting the share image into its own `og-default.jpg` slot at 1200×630 and pointing the `og:image` default there, so social cards are composed correctly rather than borrowing a hero crop.

The section photographs are ordinary raster JPGs sized for a full-width hero (~1600px wide is enough for the layout's container). The proof logos want transparency and are normalized by height, so supply them tall enough (≥ 150px) or as SVG, with consistent internal padding so wide and square marks read at equal weight.

## Where the files live

A client's images live in one directory, mirroring the served layout:

```
branding/<client>/assets/
  logo-lockup-dark.(svg|png)
  logo-lockup.(svg|png)
  favicon.png
  og-default.jpg
  about-work.jpg
  contact-talk.jpg
  audit-review.jpg
  services-life.jpg
  blog-featured.jpg
  logos/
    <mark>.png
```

Defaults live in `branding/_template/assets/`. The new-client scaffold copies `_template` into `branding/<client>/`, so a fresh client starts with working placeholder images and replaces them one slot at a time. That is the "override" step: it happens at scaffold time by swapping files, not through a build-time overlay. Because it is repo-per-client, the client directory is the single source of truth for brand images — there is no second layer to reconcile.

## How the build serves them

The brand images move *out* of `src/assets/` and into `branding/<client>/assets/`. Eleventy passthrough-copies the one active `branding/<client>/assets/` (discovered by ignoring `_`-prefixed directories, the same rule the generators use) to `/assets/`. After the move, `src/assets/` holds only what genuinely belongs to the machine: `fonts/` (generated by `fetch-fonts.py`) and `uploads/` (Sveltia CMS media). Because the brand images no longer sit in `src/assets/`, the two passthrough copies write different files into `/assets/` and never collide — there is no overlay ambiguity to reason about.

## Social: accounts are data, share images are assets

The sketch grouped "social accounts" under assets, but an account is a URL or handle, not an image. Those belong with the site's other configuration, in `branding/<client>/site.yaml`, as a structured map the template renders where present and skips where absent:

```yaml
social:
  instagram: "https://instagram.com/…"
  whatsapp: "https://wa.me/…"
  github: "https://github.com/…"
  facebook: "https://facebook.com/…"
  linkedin: "https://linkedin.com/company/…"
  x: "https://x.com/…"
  youtube: "https://youtube.com/@…"
```

Today two of these (instagram, whatsapp) already live in `site.json`'s contact block. Consolidating them into a `social:` map is part of the site-config work in the customization plan's Phase 3, which is the sensible moment to do it — the map, the footer/nav rendering, and the rest of `site.yaml` land together.

Social *share images* — a per-platform or per-campaign set of pre-composed cards — are genuinely assets. When they are needed they live under `branding/<client>/assets/social/`, a "theme pack" of raster images at each platform's ratio. This is noted as a future slot group, not built now.

## Relationship to the Canonical Loop

The slot *wiring* is template-owned: the paths the template references, the passthrough discovery, and this specification travel down the upstream path and improve for every client. The image *files* are client-owned, living only in `branding/<client>/assets/`, so they never conflict on a `git merge upstream`. This is the same boundary the customization plan relies on, applied to imagery.

## Open questions

- Do we parameterize the logo path (via `site.yaml`) so a client can ship an SVG mark, rather than exporting PNG at the fixed `logo-lockup*.png` names?
- Which favicon members do we wire beyond `favicon.png` — `apple-touch-icon.png` (180×180) and a multi-size `favicon.ico`?
- Should the `check:brand` validator (later phase) fail the build when a required slot is missing or an OG image is not 1.91:1?
- Do proof logos stay a free-form `logos/` folder, or become a declared list in `site.yaml` so the marquee order and alt text are data?

## License

This document, *Asset Specification: Branding Images, Slots, and Social*, by **Christopher Steel**, with AI assistance from **Claude (Anthropic)**, is licensed under the [GNU Affero General Public License v3.0 or later](https://www.gnu.org/licenses/agpl-3.0.html).

## Changelog

| Version | Status | Notes |
| --- | --- | --- |
| 0.1.0 | Draft | Initial draft; defines the brand image slots with per-slot format/size, the `branding/<client>/assets` layout and override-at-scaffold model, the Eleventy passthrough mechanism, and the social accounts (site.yaml) versus social share images (assets) split; recommends a dedicated `og-default.jpg` and a parameterized logo path |
