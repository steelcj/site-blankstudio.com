---
title: "Design Token Primer — The Minimum You Need to Know"
date: 2025-11-15
description: "A plain-language introduction to design tokens: what they are, why they matter for multilingual and accessible design, and how to implement a minimal token system without a design tool subscription."
draft: false
params:
  status: "Stable"
  version: "1.0.0"
"sat:work": "urn:uuid:1af4d01e-f7af-4f7f-8376-ed1a038865f5"
---

## What is a design token?

A design token is a named value that encodes a design decision. Instead of writing `color: #0033cc` in five hundred places, you define a token — `--colour-primary: #0033cc` — and reference the token everywhere. When the decision changes, you change it in one place.

Tokens are the infrastructure layer of a design system. They are not a design tool feature or a framework requirement. They are CSS custom properties, and they work in any browser.

## Why tokens matter for accessible, multilingual design

**Accessibility** — tokens make it tractable to verify colour contrast across an entire system. If your text colour and background colour are both tokens, you can check every combination in one place rather than hunting through a codebase for hardcoded values.

**Multilingual design** — tokens make it straightforward to adjust typographic decisions for specific languages. A French interface may need slightly more generous line height than an English one. A token-based system lets you override a single value per language rather than rewriting layout rules.

**Maintainability** — a small team can maintain a token-based system because changes are localised. Replacing the primary colour takes two minutes, not two days.

## A minimal token system

A minimal token system for a small organisation typically needs four categories:

**Colour** — three to five colours maximum. A primary colour, a text colour, a background colour, a border colour, and one semantic colour (for errors or warnings if needed). Every other colour in the system should be derived from these or be black or white.

**Typography** — two to three font sizes for body text, one or two for headings, and one for small labels. A line height for each. A font stack per typeface used.

**Spacing** — four to six spacing values on a consistent scale. We recommend: 0.25rem, 0.5rem, 1rem, 2rem, 4rem. Everything else is composed from these.

**Layout** — a maximum content width (we use `70ch` as a default for body text), and a standard gap value for grid layouts.

## Implementation

In CSS:

```css
:root {
  --colour-primary:    #0033cc;
  --colour-text:       #000000;
  --colour-background: #ffffff;
  --colour-border:     #d0d0d0;

  --font-body:    "IBM Plex Sans", system-ui, sans-serif;
  --font-display: "Space Grotesk", system-ui, sans-serif;

  --size-sm:   0.875rem;
  --size-base: 1rem;
  --size-lg:   1.25rem;
  --size-xl:   1.75rem;

  --space-sm:  0.5rem;
  --space-md:  1rem;
  --space-lg:  2rem;
  --space-xl:  4rem;

  --measure:   70ch;
}
```

That is the complete token system for this site. Everything else is composition.
