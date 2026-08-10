# branding/ — the per-client customization surface

Everything that makes a site *this client's* lives in one directory here:
`branding/<client>/`, named for the client (for example `branding/clientbrand.com/`).
Nothing else in the repository is edited to rebrand a site.

## The one rule

**Edit only inside `branding/<client>/`. Never hand-edit the shared machine.**

The shared machine — `src/css/home.css`, `src/js/`, `.eleventy.js`, the layouts
and partials, and `scripts/` — is template-owned. It comes from the canonical
template and is improved there, then merged down. Because a client's directory
never exists in canonical, `git merge upstream` can never touch it: the files a
client edits most have, by design, zero merge surface. This is the boundary the
[Canonical Loop](../docs/en/docs/guides/workflows/workflow--canonical-loop-fork-customize-and-promote-client-sites-v0-1-2.md)
workflow depends on. Move a value into `branding/<client>/` and it is a merge
conflict you will never have.

If a client genuinely needs a change to a template-owned file, that is a signal
to promote the change up into canonical, not to hand-edit it here.

## What's in here

- `branding/<client>/` — the active client. Exactly one non-`_` directory is
  expected; the generators and the build discover it automatically.
- `branding/_template/` — the canonical seed. `npm run new-client` copies it to
  start a client. It is template-owned; edit it in canonical, not per client.
  Any `_`-prefixed directory (`_template`, `_example`) is ignored by discovery.

## What a client directory holds

| File | What it controls | Generated into |
| --- | --- | --- |
| `brand.yaml` | The colour palette (grouped tokens) | `src/css/brand.css` |
| `fonts.yaml` | Webfont families, weights, subsets | `src/css/fonts.css` + `src/assets/fonts/` |
| `site.yaml` | URL, timezone, contact, social | `src/_data/site.json` |
| `assets/` | Logo, favicon, imagery, proof logos | copied to `/assets/` |

Required values are `url`, `publicationTimeZone`, and `contact.email`, plus the full colour palette. Phones and social accounts are optional — templates render whatever is present. See the [Asset Specification](../docs/en/docs/guides/branding/asset-specification--branding-images-slots-and-social-v0-1-0.md) for the image slots.

## How it becomes the site

Two generators (Python, in `scripts/branding/`) turn the declarations into what
Eleventy builds, and the config outputs are regenerated and validated on every
`npm run build`:

```bash
npm run new-client -- <client>   # stamp branding/<client>/ from _template
npm run build:fonts              # fonts.yaml -> fonts.css + woff2 (needs network)
npm run build:brand              # brand.yaml -> brand.css, site.yaml -> site.json
npm run check:brand              # fail if required config is missing or a TODO
npm run build                    # prebuild runs build:brand + check:brand, then Eleventy
```

The generated files (`brand.css`, `fonts.css`, `site.json`) are committed but
template-owned outputs — do not edit them by hand; edit the YAML and regenerate.

## Starting a client

1. `npm run new-client -- <client>` (for example `clientbrand.com`).
2. Fill in the copied `brand.yaml`, `fonts.yaml`, and `site.yaml` — replace the
   `TODO` values.
3. Drop the brand images into `branding/<client>/assets/` (see its `README.md`).
4. `npm run build:fonts && npm run build`. `check:brand` fails the build until
   every required value is filled in.

## More

- [Implementation plan: customization and brand config](../docs/en/docs/guides/plans/implementation-plan--client-customization-brand-config-system-v0-1-0.md)
- [The Canonical Loop workflow](../docs/en/docs/guides/workflows/workflow--canonical-loop-fork-customize-and-promote-client-sites-v0-1-2.md)
- [Asset specification](../docs/en/docs/guides/branding/asset-specification--branding-images-slots-and-social-v0-1-0.md)
