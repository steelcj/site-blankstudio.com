# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Repository versions are independent of the document versions under
`docs/en/docs/`, which carry their own version lines and changelogs.

## [Unreleased]

## [0.2.2] - 2026-08-12

### Added

- Menu derived from the client's content tree. `src/_data/menu.js` reads the
  sections out of `branding/<client>/content/<locale>/` — one directory per
  section — and the nav and footer render that list instead of a hardcoded set
  of links. Adding a section to the branding directory adds a menu item; the
  locale directories in the same tree are what declare which languages a site
  has. Item labels and URLs resolve per locale: a section whose name matches a
  route uses that page's translated label and localized slug, and a content
  section pairs with its translation through `sat:work`, so `legal/` in English
  points French readers at `mentions-legales/`. A section with no page yet is
  reported at build time and left out rather than linked to a 404.
- Optional `nav` block in `branding/<client>/site.yaml` (`before`, `after`,
  `order`), passed through to `src/_data/site.json` by `build-brand.py`. It pins
  the designed landing pages around the sections and orders the sections;
  unlisted sections append alphabetically. Omitted, it defaults to home first
  and contact last.
- `npm run ingress` (`scripts/content/ingress.py`), implementing
  spec--content-ingress-v0.1.0: reconciles the seed content tree into
  `src/content/`, keyed by `sat:work` identity — adds what is missing, skips
  what already exists in that locale, stamps a generated UUID into a seed file
  that carries none, and never deletes. Blocks, and reports, a seed file whose
  URL is already owned by a designed page in `src/pages/` or by a file already
  in the live tree. `--dry-run` reports without writing. The build never runs
  it; it reads the live tree only.
- `lib/branding.js`, the one lookup for the active `branding/<client>/`
  directory, now shared by `.eleventy.js` and `src/_data/menu.js`.
- `branding/_original.com/`, the home page taken apart into a block library. Each
  block is filed as `blocks/<role>/<pattern>.njk` beside the `.css`
  it owns, where the role is what the block does for a reader (Statement,
  Credibility, Catalogue, Position, Method, Endorsement, Feed, Conversion) and
  the pattern is how it is built and behaves (`hero-split`, `metric-row`,
  `logo-marquee`, `card-grid`, `split-pillars`, `step-list`, `quote-block`,
  `post-grid`, `cta-band`). `_shared/` carries what every block assumes:
  foundations, section shell, reveal motion, reduced motion, responsive stack.
  Markup and styles are verbatim slices, and each file's header records its
  role, surface, motion, data keys, anchor, known issues, and the source file
  and line range it came from. The directory is `_`-prefixed, so it is a parked
  reference that no build ever reads.
- `npm run check:blocks` (`scripts/branding/check-blocks.py`) re-reads those
  provenance headers, re-slices each source, and reports any block that has
  drifted from the lines it claims to copy — the thing a library of copies
  otherwise has no way to notice. Exits non-zero, so it can gate a release.

- Flags on `npm run new-client -- <client>`, which until now could only create a
  client that did not exist yet. They act on the SITE, never on a branding
  directory: this command no longer deletes `branding/<client>/` under any flag,
  and an existing one is used as it stands.
  - `--overwrite` lets the branding directory win over the site: a page it has
    already published is replaced by the seed's version, a page whose seed
    location has changed is written to the new path and removed from the old,
    and live pages the seed says nothing about are left alone. An identical page
    is reported as unchanged and not rewritten.
  - `--recreate` is the wider hammer: it empties `src/content/` and rebuilds it
    from the seed, so the live tree ends up an exact reflection of the branding
    directory. Directory-data files (`_localeTree.js`, `*.11tydata.js`) are kept,
    being code rather than content, and directories left empty are pruned.
  - `--redirects`, with either, writes a 301 into `src/_redirects` for every page
    whose URL changes. Moves are resolved by `sat:work` identity, comparing where
    each work sat before with where it lands after; a work that no longer exists
    is reported rather than redirected somewhere invented, and a source path that
    already has a rule is left alone.
  - `--dry-run` reports the whole plan without touching anything, `--yes` answers
    the confirmations for CI, and the two content flags are mutually exclusive so
    it is always clear whether pages the seed omits survive.

  Both content flags now work the plan out on a run that writes nothing, print
  it — including which URLs would move, which would disappear, and which live
  files carry no `sat:work` and so cannot be matched to the seed at all — and
  only then ask. The question is answerable because it states consequences
  rather than file counts.

  The content half is imported from `scripts/content/ingress.py` rather than
  reimplemented, so `npm run ingress` and the flags agree on where a page
  belongs. Ingress gained the same `--overwrite` mode, and a check for a seed
  section of dated, index-less pages not named for the locale's blog route,
  since its posts would publish where the blog listing never looks.

### Fixed

- Guards on the commands that write over existing work, after `--overwrite`
  emptied a client's branding directory:
  - `new-client` refuses `--overwrite` and `--recreate` when the seed holds no
    content files at all. An empty seed says nothing about the site, so
    `--recreate` against one would have deleted a live site on the strength of
    an empty directory.
  - Before either flag destroys anything, it asks git which of the affected
    paths are untracked (nothing can bring them back) and which merely have
    uncommitted edits (git can restore them as far as the last commit), and says
    so. "It's all in git" was the assumption that made the first loss permanent.
  - `build-brand.py` skips generation, loudly, when the client's `site.yaml`
    still holds template placeholders while `src/_data/site.json` is filled in —
    the shape a reset branding directory has. It writes neither output, so a
    build keeps using the last good `site.json` and `brand.css` instead of
    stamping `example.com` and the template palette over them. `--force` writes
    anyway.
- `npm run test:ingress` (`scripts/content/test_ingress.py`), 26 offline checks
  against a scratch site built in a temp directory: add, skip-if-present,
  overwrite in place, overwrite relocating a page and the redirect that falls
  out of it, the wipe keeping data files and pruning empty directories, a live
  page the seed lacks being reported as gone, routed-page collisions, the
  locale-second blog mapping, identity stamping, and the redirect file's
  append-below-hand-written-rules behaviour. Nothing in it touches the real
  content tree or any real branding directory.

### Changed

- Foundations and Legal became subsections of About in the live English tree,
  matching the seed: `src/content/en-ca/foundations/` and
  `src/content/en-ca/legal/` moved to `src/content/en-ca/about/…`, so they now
  publish under `/en-ca/about/foundations/` and `/en-ca/about/legal/`.
  Absolute links inside the moved pages were rewritten, and `src/_redirects`
  gained 301s for both sections and every page in them. The French tree keeps
  `mentions-legales/` at the top of the locale, so no French URL moved; the
  hreflang alternates, language switcher and sitemap followed the English move
  on their own, through the shared `sat:work` identity.
- The vishpala.com seed's French blog directory renamed from `blogue/` to
  `articles/`, matching `routes.blog` in `src/_locales/fr-ca.json` and the URLs
  the site already publishes. Under the old name a recreate would have placed
  the posts as ordinary content pages at `/fr-ca/blogue/…`, leaving the listing
  at `/fr-ca/articles/` empty.

## [0.2.1] - 2026-08-10

- added vishpala.com branding example

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
