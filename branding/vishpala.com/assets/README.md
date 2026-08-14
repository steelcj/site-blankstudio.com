# Vishpala (test client) — De Stijl assets

Generated vector assets in a De Stijl / Mondrian theme: a logo mark, the two
logo lockups, and a composition for the hero slots.

- `favicon.svg` — the Mondrian mark
- `logo-lockup-dark.svg` — mark + wordmark for light backgrounds (nav, loader)
- `logo-lockup.svg` — mark + white wordmark for the dark footer
- `about-work.svg` — a De Stijl composition for a hero/section slot

## Type

This client downloads no webfonts. It is set in `system-ui` throughout, with a
monospace stack where a monospace face is meant — the reasoning is at the top of
`../fonts.yaml`, and the site argues the same position on its own
`resources/system-fonts` page.

Practically, that means `families: []` and nothing in `src/assets/fonts/`.
Changing it — here or for any client — is the "Type" section of
`../../_template/assets/README.md`: which block does what, which weights this
template's CSS actually uses, and the order to run the two generators in.

Note on wiring: the template references the brand images by fixed `.png`/`.jpg`
slot names (`logo-lockup-dark.png`, `about-work.jpg`, …). These are delivered
as `.svg`, so to make them appear in the built site either rasterize them to the
slot names, or add the "logo path in `site.yaml`" enhancement from the asset
specification so the template can reference `.svg` directly. The **theme itself**
(colours) needs none of this — it renders from `brand.yaml` → `brand.css`.
