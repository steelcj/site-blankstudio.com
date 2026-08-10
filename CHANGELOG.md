# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Repository versions are independent of the document versions under
`docs/en/docs/`, which carry their own version lines and changelogs.

## [Unreleased]

## [0.2.0] - 2026-08-10

### Added

- Locale-first content model. Content lives under `src/content/<locale>/…` with
  the file path mirroring the URL. A shared directory-data factory
  (`src/content/_localeTree.js`) supplies each language root, a build-time index
  (`src/_data/contentWorkIndex.js`) pairs translations by their `sat:work` UUID
  read off disk, and `src/_includes/layouts/page.njk` renders the markdown.
  Translations are mirrored — localized paths connected by identity, not by
  matching paths — driving the language switcher and `hreflang`.
- Legal section, the first content built to that model:
  `src/content/en-ca/legal/` (privacy, terms, cookies, accessibility, index)
  with its French mirror `src/content/fr-ca/mentions-legales/` (confidentialite,
  conditions, cookies, accessibilite, index), paired by shared `sat:work` UUIDs
  and switchable both ways.
- Site configuration consolidated into `branding/<client>/site.yaml` (URL,
  timezone, a `contact` block, and a `social` map);
  `scripts/branding/build-brand.py` generates `src/_data/site.json` from it
  alongside `src/css/brand.css`.
- Logo and favicon paths parameterized: a `logos` block in `site.yaml` (dark,
  light, favicon — any format) flows into `site.json`, and the templates read
  `site.logos.*` instead of hardcoded `/assets/…png`, defaulting to the `.png`
  slots. A client can now ship SVG marks.
- `check:brand` validator (`scripts/branding/check-brand.py`), run in a
  `prebuild` step: fails the build on missing required config (the colour
  tokens, `url`, `publicationTimeZone`, `contact.email`) or leftover
  `TODO`/`example` placeholders, and warns on missing asset slots.
- `new-client` scaffold (`scripts/branding/new-client.py`) that stamps
  `branding/<client>/` from `branding/_template/`, and `branding/README.md`
  documenting the template-owned / client-owned boundary.
- Reference specifications under `docs/en/docs/reference/`: the multilingual
  content-structure vocabulary, the publishing-vector content-format
  specification, and the content-ingress specification.
- Release runbook at
  `docs/en/docs/guides/devops/runbook--cutting-and-publishing-releases-v0-1-0.md`,
  covering first-time setup and the recurring cut, push, and publish ceremony.
- Vishpala test client (`branding/vishpala.com/`): a De Stijl / Mondrian theme
  with SVG logo lockups, favicon, and a composition, exercising the branding and
  logo-path systems end to end.

### Changed

- The footer's contact links route to the contact page's method sections
  (`#email`, `#phone`, `#whatsapp`, `#instagram`) rather than duplicating direct
  `tel:`/`wa.me`/external links; the contact page gained matching anchors.
  `nav.njk` and the final-CTA buttons still read the flat `site.contact` keys.

## [0.1.0] - 2026-08-10

### Added

- Branding configuration system. The client-owned brand surface lives in a
  per-client directory `branding/<client>/`, with `branding/_template/` as the
  canonical seed; the generators discover the one active client by glob and
  ignore `_`-prefixed templates.
- Colour palette made declarative: `branding/<client>/brand.yaml` is rendered
  into `src/css/brand.css` by `scripts/branding/build-brand.py`, and consumed by
  `home.css` (loaded after `brand.css`). `npm run build:brand` regenerates it.
- Font pipeline relocated: `fonts.yaml` now lives in `branding/<client>/`, and
  `scripts/branding/fetch-fonts.py` discovers it and resolves its output paths
  from the repo root. `npm run build:fonts` regenerates the webfonts.
- Brand assets moved out of `src/assets/` into `branding/<client>/assets/`,
  served via an Eleventy passthrough that discovers the active client;
  `src/assets/` now holds only generated fonts and Sveltia uploads.
- Documentation under `docs/en/docs/`: the Canonical Loop workflow, the
  mermaid-navigation style guide, the template licensing analysis, the branding
  asset specification, and the customization and content-type implementation
  plans.
- Release tooling: `cut-release.py`, `publish-release.py`, and `bump-version.py`
  (synced from the `sat-doc-automa` canonical project), with this `VERSION` and
  `CHANGELOG.md`.

### Changed

- `src/css/home.css` no longer declares the colour custom properties; it keeps
  only the type and layout tokens, so it stays byte-identical to canonical and
  merges cleanly.

### Fixed

- Contact and communications links: WhatsApp, phone, email, and the Instagram
  account.
