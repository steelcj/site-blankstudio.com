---
dc:title: "Implementation Plan: Client Customization and Brand Config System"
dcterms:version: "0.1.0"
dc:creator: "Christopher Steel"
dc:contributor: "Claude (Anthropic)"
dc:subject:
  - "customization"
  - "brand"
  - "eleventy"
  - "configuration"
  - "canonical"
  - "template"
dc:description: >
  A phased plan to make client customization fast and merge-safe: extract the
  colour palette into brand.yaml, colocate the client-owned surface in a branding/
  folder, add a scaffold and a validator, and hold a clean template-owned /
  client-owned boundary so canonical updates keep merging.
dc:publisher: "UniversalCake"
dcterms:created: "2026-08-09"
dcterms:modified: "2026-08-09"
dc:format: "text/markdown"
dc:language: "en"
sat:language_bcp47: "en"
dc:identifier: "implementation-plan--client-customization-brand-config-system"
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
      Initial draft. Phased implementation plan for the client customization
      and brand config system: extract the palette to brand.yaml and a
      generated brand.css, establish the branding/ client-owned folder, relocate
      fonts.yaml and asset sources, consolidate site config, add a new-client
      scaffold and a check:brand validator, wire the generators into the build,
      and document the template-owned / client-owned boundary.
---

# Implementation Plan: Client Customization and Brand Config System

Version: 0.1.0
Status: Draft — proposed
Style Guide: style-guide--plain-language-for-general-audiences

## Abstract

native to your Eleventy + Sveltia stack.

**Customization & brand config** — a six-phase plan: extract the palette out of `home.css` into `brand.yaml` → a generated `brand.css`, colocate the whole client-owned surface in a `branding/` folder (brand.yaml, fonts.yaml, site.yaml, assets), add a `new-client` scaffold and a `check:brand` validator, wire the generators into the build, and document the template-owned/client-owned boundary so `git merge upstream` keeps working.

## Goal

Make branding a client site fast, obvious, and safe to merge. A teammate should be able to see the whole customization surface in one place, fill it in, and have the build tell them when something is missing, without ever hand-editing the shared machine. The deeper aim is drift control: every per-client value we move into a data file is a merge conflict we do not get when a canonical fix comes down the [upstream](#the-boundary-that-holds-it-together) path.

This plan builds on the model in *The Canonical Loop*: canonical is the trunk, each client is a fork, and the win comes from a disciplined split between what the template owns and what a client owns.

## Current state

The template is already about 80 percent config-driven, which is the reason this plan is small rather than a rewrite.

Fonts are declarative: `fonts.yaml` at the repo root is read by `scripts/fetch-fonts.py`, which downloads the woff2 files into `src/assets/fonts/` and generates `src/css/fonts.css`. Languages are a registry in `src/_data/locales.js`. URL, contact details, and the publication timezone live in `src/_data/site.json`. All display copy is externalized into `src/_locales/<code>.json` string bundles. Logos, favicon, and images are files under `src/assets/`. There is already an i18n validator, `scripts/check-untranslated.js`, wired as `npm run check:i18n`.

The one thing that is not data yet is the colour palette. It is hard-coded as `:root` custom properties in `src/css/home.css` (`--blue`, `--beige`, `--ink`, and the rest). That is the single seam that forces a client to hand-edit a template-owned file, which is exactly what breaks a clean `git merge upstream`.

## Target design

One client-owned directory, named for the client, holds everything that varies per client. In a client repo that is `branding/<client>/`, for example `branding/clientbrand.com/`, containing:

- `branding/<client>/brand.yaml` — the colour palette and any theme tokens.
- `branding/<client>/fonts.yaml` — moved here from the repo root, unchanged in shape.
- `branding/<client>/assets/` — the source logo, favicon, and imagery.
- `branding/<client>/site.yaml` — the client-owned values that currently sit inside `src/_data/site.json` (URL, contact block, timezone).

Naming the directory after the client is not cosmetic; it is what keeps upstream merges clean. Canonical ships only a template directory, `branding/_template/`, and never a real client directory, so `branding/<client>/` exists only in the client's fork. Because that path is never present upstream, `git merge upstream` can never touch it: the files a client edits most have, by construction, zero merge surface. A single fixed `branding/brand.yaml` would instead be shipped as a placeholder by canonical and filled in by the client, so every canonical change to it would conflict on merge — exactly the drift we are trying to avoid.

Because the directory name varies per repo, the generators discover it rather than hard-code it: they glob `branding/*/` for the one active client directory, ignore any `_`-prefixed template such as `branding/_template/`, and error clearly if they find zero or more than one. This keeps "one client per repo" honest and stays forward-compatible if we ever build several clients from one repo.

The branding scripts that process this surface are themselves template-owned machinery, so they live under `scripts/branding/`, on the opposite side of the boundary from the client data they read. The config and the tool that reads it sit apart on purpose: `branding/<client>/fonts.yaml` is the client's data, `scripts/branding/fetch-fonts.py` is the template's tool.

Two generators turn that declarative surface into what Eleventy builds, mirroring the pattern the font script already established:

- `scripts/branding/fetch-fonts.py` (the existing font script, relocated here) reads the active `branding/<client>/fonts.yaml`.
- `scripts/branding/build-brand.py` (new) reads `branding/<client>/brand.yaml` and writes `src/css/brand.css` with the `:root` custom properties, and reads `branding/<client>/site.yaml` to produce `src/_data/site.json`.

Everything else stays template-owned and byte-identical across clients: `src/css/home.css` keeps using `var(--blue)` but no longer declares the palette; `.eleventy.js`, `src/js/`, the layouts, and the scripts are never hand-edited per client.

## Phases

### Phase 1 — Make colour declarative

Extract the `:root` palette out of `src/css/home.css` into a generated `src/css/brand.css`. Author the values in the active `branding/<client>/brand.yaml` (seeded from `branding/_template/brand.yaml`), and add `scripts/branding/build-brand.py` to render them into the custom-property block. Load `brand.css` before `home.css` so the variables are defined when `home.css` consumes them.

Deliverables: `branding/_template/brand.yaml` and the client copy `branding/<client>/brand.yaml`, `scripts/branding/build-brand.py`, generated `src/css/brand.css`, the `:root` palette removed from `home.css`, and the stylesheet link order updated in `src/_includes/layouts/base.njk`.

Done when: a full build produces a site visually identical to today, and changing a hex value in `brand.yaml` then rebuilding changes the site, with no edit to `home.css`.

### Phase 2 — Establish the branding/ folder

Create `branding/<client>/` and move the client-owned files into it. Move `fonts.yaml` to `branding/<client>/fonts.yaml`. Relocate the font script to `scripts/branding/fetch-fonts.py` and change it in two ways: discover its config by globbing `branding/*/fonts.yaml` (expecting one active client), and resolve its **output** paths relative to the repo root rather than the config file's own directory. The script currently derives `root` from the config's directory, so a nested `fonts.yaml` would otherwise write `src/assets/fonts` *inside* `branding/<client>/`. Move the source logo, favicon, and hero imagery into `branding/<client>/assets/`, and add a copy step (in `scripts/branding/build-brand.py` or an Eleventy passthrough) so they land at their served paths under `src/assets/`.

Deliverables: populated `branding/<client>/` directory, the `branding/_template/` seed, `scripts/branding/fetch-fonts.py` (relocated) updated for discovery and repo-root-relative output, and copy wiring for assets.

Done when: `branding/<client>/` contains the entire visual identity of the site, the fonts still land in `src/assets/fonts` as before, and nothing a designer touches to rebrand lives outside `branding/<client>/`.

### Phase 3 — Consolidate site config

Introduce `branding/<client>/site.yaml` for the client-owned values now embedded in `src/_data/site.json` (URL, contact, timezone), and have `build-brand.py` generate `src/_data/site.json` from it. Keep `site.json` as the generated file Eleventy reads, so no template code changes.

Deliverables: `branding/<client>/site.yaml`, generation of `src/_data/site.json`, `site.json` marked generated (header comment, and consider git-ignoring it once generation is reliable).

Done when: editing contact details or the URL is done only in `branding/<client>/site.yaml`, and the rendered site reflects it after a build.

### Phase 4 — New-client scaffold

Add `scripts/branding/new-client.py` that takes a client name and stamps `branding/<client>/` by copying `branding/_template/`, with clearly marked `TODO` placeholders (palette, fonts, site values, asset filenames), so starting a client is one command rather than copy-and-edit archaeology.

Deliverables: `scripts/branding/new-client.py`, the `branding/_template/` seed directory, and an `npm run new-client -- <client>` entry.

Done when: running the scaffold with a client name produces a `branding/<client>/` a teammate can fill in top to bottom with no guesswork, and `branding/_template/` is left untouched.

### Phase 5 — Validator and build wiring

Add `scripts/branding/check-brand.js`, wired as `npm run check:brand`, mirroring the existing `check:i18n`. It fails the build when a required key is missing, a `TODO` placeholder survives, or an expected asset file is absent. Then wire the generators and checks into the build so they cannot be forgotten: `build` runs `fetch-fonts`, `build-brand`, and the checks before `eleventy`.

Deliverables: `scripts/branding/check-brand.js`, `check:brand` script, and an updated `build` pipeline (a `prebuild` step or `npm-run-all`).

Done when: a site with an unfilled placeholder fails `npm run build` with a clear message naming the missing piece, and a complete `branding/` builds clean.

### Phase 6 — Document the boundary

Write a short `branding/README.md` listing the client-owned surface and the one rule: edit only inside `branding/`, never the shared machine. Cross-link *The Canonical Loop* so the merge-down habit is stated where a teammate will see it.

Deliverables: `branding/README.md`, a link from the customization step of *The Canonical Loop*.

Done when: a new teammate can rebrand a site from the README alone and knows why they must not touch `home.css`.

## The boundary that holds it together

This plan is only half about convenience. The other half is that a clean `branding/` boundary is what keeps `git merge upstream` viable, so canonical fixes reach shipped client sites without colliding with hand-edited values.

| Template-owned (never hand-edited per client) | Client-owned (the customization surface) |
| --- | --- |
| `src/css/home.css`, `src/js/`, `.eleventy.js`, layouts and partials, `scripts/*` (including `scripts/branding/`), `branding/_template/` | `branding/<client>/brand.yaml`, `branding/<client>/fonts.yaml`, `branding/<client>/site.yaml`, `branding/<client>/assets/` |
| The i18n machinery and locale structure | The values inside `src/_locales/<code>.json` |
| Generated `src/css/brand.css`, `src/css/fonts.css`, `src/_data/site.json` | The inputs those files are generated from |

The one seam that resists a clean split is `src/_locales/<code>.json`: its keys are template-owned but its values are client copy. That is an acceptable small merge surface; readable JSON conflicts are fine, and splitting defaults from overrides can wait until it actually hurts.

## Risks and mitigations

Moving `fonts.yaml` and the site values changes paths that scripts and Eleventy rely on; mitigate by updating each script's default in the same commit and adding a smoke build to CI. Nesting `fonts.yaml` under `branding/<client>/` exposes a specific gotcha: `fetch-fonts.py` resolves its output paths relative to the config file's directory, so the Phase 2 fix must switch output resolution to the repo root, or the generated fonts and stylesheet land inside `branding/<client>/`. Directory discovery has its own failure mode: a leftover demo directory alongside the real client would make the `branding/*/` glob match two, so keep template and demo directories `_`-prefixed (`branding/_template/`, `branding/_example/`) so discovery ignores them, and have the scaffold leave exactly one un-prefixed client directory. The generated `brand.css` must load before `home.css` or the variables are undefined at first paint; mitigate by fixing the link order in `base.njk` in Phase 1 and checking the built HTML. Generating `src/_data/site.json` risks a stale committed copy diverging from `site.yaml`; mitigate by generating it in `prebuild` and, once trusted, git-ignoring the output.

## Open questions

- Do we generate `src/_data/site.json` and git-ignore it, or keep it committed for readability?
- Should `brand.yaml` carry only colours, or also spacing, radius, and other theme tokens now hard-coded in `home.css`?
- Resolved in Phase 1: `build-brand.py` is Python, matching `fetch-fonts.py` and reusing PyYAML, so both generators share one language and no Node YAML dependency is added.
- Do we want the scaffold to also open a checklist issue, tying into the canonical promotion gate?
- Do client directories use the domain (`clientbrand.com`) or a short slug as their name, and is that convention recorded anywhere the generators or CI depend on?

## License

This document, *Implementation Plan: Client Customization and Brand Config System*, by **Christopher Steel**, with AI assistance from **Claude (Anthropic)**, is licensed under the [GNU Affero General Public License v3.0 or later](https://www.gnu.org/licenses/agpl-3.0.html).

## Changelog

| Version | Status | Notes |
| --- | --- | --- |
| 0.1.0 | Draft | Six-phase plan to extract colour to `brand.yaml`, add scaffold and `check:brand` validator, wire the build, and document the template-owned / client-owned boundary. The client-owned surface lives in a per-client directory `branding/<client>/`, with canonical shipping only `branding/_template/`, so it never conflicts on upstream merges; generators discover the active client directory by glob, and `fetch-fonts.py` resolves output relative to the repo root; the branding scripts live under `scripts/branding/` (template-owned), separate from the client data in `branding/<client>/` |
