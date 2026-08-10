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
