# Vishpala (test client) — De Stijl assets

Generated vector assets in a De Stijl / Mondrian theme: a logo mark, the two
logo lockups, and a composition for the hero slots.

- `favicon.svg` — the Mondrian mark
- `logo-lockup-dark.svg` — mark + wordmark for light backgrounds (nav, loader)
- `logo-lockup.svg` — mark + white wordmark for the dark footer
- `about-work.svg` — a De Stijl composition for a hero/section slot

Note on wiring: the template references the brand images by fixed `.png`/`.jpg`
slot names (`logo-lockup-dark.png`, `about-work.jpg`, …). These are delivered
as `.svg`, so to make them appear in the built site either rasterize them to the
slot names, or add the "logo path in `site.yaml`" enhancement from the asset
specification so the template can reference `.svg` directly. The **theme itself**
(colours) needs none of this — it renders from `brand.yaml` → `brand.css`.
