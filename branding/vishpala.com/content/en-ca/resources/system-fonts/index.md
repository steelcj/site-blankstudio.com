---
title: "Typography — System Fonts and Atkinson Hyperlegible"
date: 2026-06-15
description: "How vishpala.com approaches typography: system-ui as the default, with Atkinson Hyperlegible available as a user-selectable accessible alternative, self-hosted with no external dependencies."
draft: false
params:
  status: "Stable"
  version: "1.1.0"
"sat:work": "urn:uuid:a93c44cd-7489-410b-8c4f-c7a76f3dba63"
---

## The approach

This site uses `system-ui, sans-serif` — the device's native font stack — as its default typography. No fonts are loaded from external sources. As a user-selectable alternative, Atkinson Hyperlegible is available and self-hosted: all font files are served directly from this site with no third-party requests.

The font switcher (`Aa`) in the site header lets you choose between the two options. Your preference is saved and applied on every subsequent visit.

## System-ui — the default

System fonts are the typefaces operating system vendors have spent the most resources optimising for screen legibility at every size, display density, and accessibility setting. San Francisco on macOS and iOS, Segoe UI on Windows, and Roboto on Android are each the product of significant investment in hinting, spacing, and rendering.

System fonts respond correctly to the user's own font preferences. If a user has configured their operating system to use a larger default font size or a specific typeface for readability reasons, `system-ui` inherits those preferences. For users who depend on those preferences, that inheritance is important.

`system-ui` introduces no external dependency of any kind and imposes no infrastructure maintenance burden.

## Atkinson Hyperlegible — the accessible alternative

Atkinson Hyperlegible was designed by the Braille Institute specifically for readers with low vision. Each character is uniquely formed to prevent misreading — the letterforms for commonly confused pairs (1/l/I, 0/O, rn/m) are deliberately differentiated. The Braille Institute released it under the SIL Open Font Licence 1.1, permitting free use and redistribution.

The font is served entirely from this site's own infrastructure. The eight font files — regular, italic, bold, and bold-italic in latin and latin-extended ranges — are loaded only when you choose Atkinson, and only from this domain. No third-party requests are made.

The Inclusive Design Research Centre at OCAD University, whose work directly informs our accessibility practice, documents Atkinson Hyperlegible as a recommended typeface for low-vision accessibility.

## Sovereignty and performance

Neither typography option loads fonts from Google Fonts or any other external source. There is no connection to a third-party font delivery network and no disclosure of visitor IP addresses to font providers.

When system-ui is active, text renders immediately using a font already present on the device — no network request, no flash of invisible text, no layout shift. When Atkinson Hyperlegible is active, the font files are loaded from this server on first use and cached by the browser thereafter.

## Changelog

| Version | Date | Notes |
|---------|------|-------|
| 1.1.0 | 2026-06-28 | Updated to reflect addition of Atkinson Hyperlegible as a user-selectable option |
| 1.0.0 | 2026-06-15 | Initial version |
