# Brand assets for this client

Drop the client's brand images in this directory. The build copies it to
`/assets/` on the site, so keep the filenames — they are fixed slots the
template references by name. Full details are in the asset specification:
`docs/en/docs/guides/branding/asset-specification--branding-images-slots-and-social-v0-1-0.md`.

Required (the build warns until these exist):

- `favicon.png` — browser tab icon (PNG, 48×48 or larger)
- `logo-lockup-dark.png` — dark logo for light backgrounds (loader, nav)
- `logo-lockup.png` — light logo for the dark footer

Recommended:

- `og-default.jpg` — social share image (raster, 1200×630)

Section imagery (optional, one per page):

- `about-work.jpg`, `contact-talk.jpg`, `audit-review.jpg`,
  `services-life.jpg`, `blog-featured.jpg`

Proof logos (optional):

- `logos/<name>.png` — client or portfolio marks for the home-page marquee
