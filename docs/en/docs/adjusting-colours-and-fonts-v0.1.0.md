# Adjusting Colours and Fonts

Version: 0.1.0
Status: Draft
Style Guide: apa7-markdown-authoring

## Abstract

This guide explains how to change the BLNK Studio site's colour palette and typography, how to add a new typeface, and where to obtain licensed font files.

Every colour and typeface on the site resolves from a single block of CSS custom properties in `src/css/home.css`, and every webfont request resolves from a single field in `src/_data/locales.js`.

Editing either of those two places changes the whole site; editing anywhere else creates a value that will drift out of step.

The guide also covers the two constraints that are easy to violate without noticing: the fluid type scale carries a factor that the accessibility panel depends on, and a typeface that lacks coverage for a language will silently fall back to a system font on that language's pages.

## Sources and Acknowledgements

Typeface licensing terms and download procedures are drawn from the vendors' own documentation: <a name="apa-google-fonts-citation"></a>[Google Fonts (2026)](#apa-google-fonts-reference) for the three families currently in use, and <a name="apa-fontsource-citation"></a>[Fontsource (2026)](#apa-fontsource-reference) for self-hosted npm-packaged equivalents. The variable-font and `font-display` behaviour described in section 3 follows <a name="apa-mdn-fontface-citation"></a>[MDN Web Docs (2026)](#apa-mdn-fontface-reference). Contrast requirements referenced in section 2.3 are defined by <a name="apa-wcag-citation"></a>[W3C (2023)](#apa-wcag-reference). The accessibility typefaces bundled with the preferences panel are documented by <a name="apa-infusion-citation"></a>[Fluid Project (2026)](#apa-infusion-reference).

## 1. Where the values live

### 1.1 One source for colour, one for type

Two files govern the site's appearance. Everything else consumes them.

| Concern | File | What it holds |
|---------|------|---------------|
| Colour and type tokens | `src/css/home.css` | The `:root` block defining every colour and font stack |
| Webfont loading | `src/_data/locales.js` | The `LATIN` constant holding the font stylesheet URL |

`src/css/home.css` is loaded on every page. The other six stylesheets — `about.css`, `article.css`, `audit.css`, `blog.css`, `contact.css`, `services.css` — are page-specific and consume the tokens without redefining them. A colour changed in `:root` propagates to all seven.

### 1.2 The token block

The `:root` block in `src/css/home.css` is the palette in full.

```css
:root {
  /* Brand */
  --blue: #3b6ef5;
  --blue-bright: #3b82ff;
  --beige: #eae3da;

  /* Surfaces */
  --bg: #fbfaf7;          /* warm near-white page base */
  --bg-band: #f1efe9;     /* subtle warm band (proof / testimonial) */
  --ink: #050d1c;         /* deep navy / near-black (dark sections) */
  --ink-2: #0a1322;       /* footer */
  --card: #fbfaf7;

  /* Text */
  --text: #11141c;
  --text-dim: #565d6b;
  --text-mut: #8b919d;    /* mono labels */
  --on-dark: #eef0f5;
  --on-dark-dim: #99a0b0;
  --on-dark-mut: #5d6577;

  /* Lines */
  --line: rgba(5, 13, 28, 0.12);
  --line-2: rgba(5, 13, 28, 0.20);
  --line-dark: rgba(238, 240, 245, 0.13);

  /* Type */
  --font-head: "Inter Tight", "Inter", system-ui, sans-serif;
  --font-body: "Inter", system-ui, sans-serif;
  --font-mono: "Space Mono", ui-monospace, "SFMono-Regular", monospace;
}
```

## 2. Changing colours

### 2.1 Editing a token

Change the value in `:root` and rebuild. To warm the page background, edit one line.

```css
--bg: #faf7f2;
```

```bash
npm run build
```

Nothing else needs touching. The value is referenced as `var(--bg)` throughout the stylesheets.

### 2.2 Light and dark surfaces are separate token sets

The site alternates light and dark sections. Dark sections carry the class `on-dark`, and rules scoped to that class swap in the `--on-dark*` and `--line-dark` tokens rather than recomputing colours.

```css
.on-dark .btn--outline { border-color: var(--line-dark); color: var(--on-dark); }
```

Changing `--text` therefore affects light sections only. The dark equivalent is `--on-dark`. Changing one without the other is the most common way to end up with a palette that looks correct on the home page and wrong in the footer.

### 2.3 Verify contrast after any text or surface change

`--text-mut` at `#8b919d` on `--bg` at `#fbfaf7` is close to the WCAG AA threshold for normal-size text, which requires a contrast ratio of at least 4.5:1 <a name="apa-wcag-citation-2"></a>([W3C, 2023](#apa-wcag-reference)). Any change that lightens a text token or darkens a light surface should be re-checked before it ships. The site's accessibility panel also offers reader-selectable contrast themes, but those are an accommodation and do not excuse an inaccessible default palette.

## 3. Changing fonts

### 3.1 The three roles

The site uses three typefaces, each bound to a role rather than to a specific element. Their usage counts across the stylesheets indicate how visible a change to each will be.

| Token | Typeface | Role | References in CSS |
|-------|----------|------|-------------------|
| `--font-head` | Inter Tight | Headings and display type | 29 |
| `--font-body` | Inter | Body copy | 5 |
| `--font-mono` | Space Mono | Eyebrows, labels, metadata, UI chrome | 61 |

The low count for `--font-body` is expected: body text inherits from the `body` rule rather than being set per component.

### 3.2 Swapping a typeface

Changing a typeface requires editing two files, because the font stack and the font download are declared separately.

First, change the stack in `src/css/home.css`.

```css
--font-head: "Fraunces", "Inter Tight", system-ui, sans-serif;
```

Second, change the request in `src/_data/locales.js` so the browser actually downloads it.

```javascript
const LATIN =
  "https://fonts.googleapis.com/css2?family=Fraunces:wght@400;600;700" +
  "&family=Inter:wght@400;500;600&family=Space+Mono:wght@400;700&display=swap";
```

Editing only the first produces a silent fallback to the next stack entry. Editing only the second downloads a font nothing uses.

### 3.3 Request only the weights in use

The current request asks for eight weights across three families. Each weight is a separate download. Inter Tight is requested at `400;500;600;700;800`; if the design uses only 600 and 800, requesting the other three wastes bandwidth on every first visit. Trim the URL to what the stylesheets actually reference.

### 3.4 The fluid type scale carries an accessibility factor

Every fluid heading size on the site follows this shape.

```css
font-size: clamp(2.3rem, calc(6.4vw * var(--fl-textSize-factor, 1)), 5rem);
```

The `var(--fl-textSize-factor, 1)` term is not decorative. Viewport units do not respond to a changed root font size, so without that factor the accessibility panel's text-size control moves body copy while leaving headings nearly static, inverting the type hierarchy for the reader who most needs it enlarged. The fallback of `1` means the expression renders identically when the panel is absent.

**Preserve the factor when editing any fluid size.** Change the minimum, the viewport coefficient, or the maximum freely, but keep the `calc(... * var(--fl-textSize-factor, 1))` wrapper on the middle term.

### 3.5 Fonts are declared per locale

The font URL is a field on each locale in `src/_data/locales.js`, not a global constant baked into the layout.

```javascript
const REAL = [
  { code: "en-ca", htmlLang: "en-CA", dir: "ltr", label: "English", fonts: LATIN, uioLocale: "en_CA" },
  { code: "fr-ca", htmlLang: "fr-CA", dir: "ltr", label: "Français", fonts: LATIN, uioLocale: "fr" },
];
```

`src/_includes/layouts/base.njk` emits whichever value the active locale carries.

```html
<link href="{{ locale.fonts }}" rel="stylesheet" />
```

Both current locales share the `LATIN` constant because both are Latin-script. This structure exists so that a locale needing different glyphs can override one field rather than requiring changes to every page.

### 3.6 Script coverage is the constraint that bites

Inter, Inter Tight and Space Mono cover Latin. None covers Devanagari, Arabic, Hebrew, or CJK. Adding a locale in any of those scripts without giving it its own font stack produces pages that silently fall back to a system font, which will not match the design and may not match across operating systems.

Give such a locale its own constant and point its `fonts` field at it.

```javascript
const DEVANAGARI =
  "https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@400;600;700" +
  "&family=Space+Mono:wght@400;700&display=swap";

const REAL = [
  { code: "en-ca", htmlLang: "en-CA", dir: "ltr", label: "English", fonts: LATIN, uioLocale: "en_CA" },
  { code: "fr-ca", htmlLang: "fr-CA", dir: "ltr", label: "Français", fonts: LATIN, uioLocale: "fr" },
  { code: "hi-in", htmlLang: "hi-IN", dir: "ltr", label: "हिन्दी", fonts: DEVANAGARI, uioLocale: "en_CA" },
];
```

The matching `--font-head` and `--font-body` stacks must also list the new family ahead of the Latin ones, since CSS selects per glyph and will use the first stack entry that can render each character.

## 4. Adding a new font

### 4.1 Choosing between hosted and self-hosted

Two delivery methods are available, and the site already uses both.

| Method | Used for | Trade-off |
|--------|----------|-----------|
| Google Fonts CDN | The three brand typefaces | No files to manage; a third-party request on every page |
| Self-hosted files | The accessibility panel's four typefaces | Full control and no third-party request; files to store and serve |

Self-hosting removes a cross-origin request and the privacy question that comes with it. Since browsers partition their HTTP cache by site, a visitor gains nothing from having downloaded a Google-hosted font on another domain, which removes the historical argument for the CDN.

### 4.2 Where to download fonts

| Source | Coverage | Notes |
|--------|----------|-------|
| [Google Fonts](https://fonts.google.com) | Large open-licence library | Download the family as a ZIP, or link the CDN stylesheet <a name="apa-google-fonts-citation-2"></a>([Google Fonts, 2026](#apa-google-fonts-reference)) |
| [Fontsource](https://fontsource.org) | The same open families, npm-packaged | Installs as a dependency; suits self-hosting <a name="apa-fontsource-citation-2"></a>([Fontsource, 2026](#apa-fontsource-reference)) |
| [Font Squirrel](https://www.fontsquirrel.com) | Curated free-for-commercial-use | Verify the licence per family |
| [The League of Moveable Type](https://www.theleagueofmoveabletype.com) | Open-source originals | Small, high-quality catalogue |
| Type foundries | Commercial licensed faces | Purchase a webfont licence explicitly; a desktop licence does not permit web embedding |

**Check the licence before shipping any typeface.** Open Font Licence and Apache 2.0 permit commercial web use and self-hosting. A commercial foundry licence is usually tiered by monthly page views and often forbids serving the files from a CDN you do not control.

### 4.3 Self-hosting a font

The site already publishes self-hosted fonts for the accessibility panel, so the pattern exists to follow. In `.eleventy.js`:

```javascript
eleventyConfig.addPassthroughCopy({
  [`${INFUSION}/src/lib/atkinson-hyperlegible`]: "assets/lib/atkinson-hyperlegible",
  [`${INFUSION}/src/lib/opendyslexic`]: "assets/lib/opendyslexic",
  [`${INFUSION}/src/lib/opensans`]: "assets/lib/opensans",
  [`${INFUSION}/src/lib/roboto-slab`]: "assets/lib/roboto-slab",
});
```

To self-host a brand typeface, place the `.woff2` files under `src/assets/fonts/`, which is already copied by the existing `addPassthroughCopy("src/assets")` rule, then declare the faces in `src/css/home.css` above the `:root` block.

```css
@font-face {
  font-family: "Fraunces";
  src: url("/assets/fonts/fraunces-latin-variable.woff2") format("woff2-variations");
  font-weight: 100 900;
  font-style: normal;
  font-display: swap;
}
```

`font-display: swap` renders text immediately in the fallback face and swaps when the webfont arrives, which avoids invisible text during loading <a name="apa-mdn-fontface-citation-2"></a>([MDN Web Docs, 2026](#apa-mdn-fontface-reference)).

With the face declared locally, remove that family from the `LATIN` URL in `src/_data/locales.js`. Leaving it in downloads the font twice.

### 4.4 Prefer WOFF2 and variable fonts

WOFF2 is supported by every browser the site targets, so older `.woff`, `.ttf` and `.eot` formats are unnecessary weight. A variable font replaces several static weight files with one, which is why the accessibility panel's Open Sans ships as `open-sans-latin-wght-normal.woff2` — a single file covering the full weight axis.

## 5. Fonts belonging to the accessibility panel

Four additional typefaces are served for the preferences panel and are not part of the brand palette <a name="apa-infusion-citation-2"></a>([Fluid Project, 2026](#apa-infusion-reference)).

| Typeface | Purpose |
|----------|---------|
| Open Sans | The panel's own interface type |
| OpenDyslexic | Reader-selectable, weighted letterforms intended to reduce transposition |
| Atkinson Hyperlegible | Reader-selectable, designed for low vision with highly distinguishable characters |
| Roboto Slab | Reader-selectable serif alternative |

These are published to `/assets/lib/` because the panel's stylesheets reference them by relative path. **Do not repurpose them for brand styling and do not remove them.** A reader who has selected OpenDyslexic loses that setting if the files stop being served.

## 6. Verifying a change

Run the build and confirm both locales, since a font or colour change affects every page.

```bash
npm run build
npm start
```

Check the following before considering a change complete.

- Light and dark sections both, since they draw on separate token sets
- Both `/en-ca/` and `/fr-ca/`, since French text runs roughly 23 per cent longer and reflows differently
- The accessibility panel's text-size control at maximum, confirming headings still scale with body copy
- The browser network panel, confirming no font is downloaded twice and no requested weight is unused

The pseudo-locale build exaggerates text length by roughly 30 per cent and is the fastest way to see whether a type change breaks a layout.

```bash
npm run build:pseudo
```

## Resources

### Font libraries
- [Google Fonts](#apa-google-fonts-reference)
- [Fontsource](#apa-fontsource-reference)

### Web typography specifications
- [MDN Web Docs on @font-face](#apa-mdn-fontface-reference)

### Accessibility standards
- [W3C Web Content Accessibility Guidelines 2.2](#apa-wcag-reference)
- [Fluid Project Infusion](#apa-infusion-reference)

## References

<a name="apa-fontsource-reference"></a>Fontsource. (2026). *Fontsource: Self-host open source fonts in neatly bundled NPM packages*. https://fontsource.org
[Return to citation](#apa-fontsource-citation)

<a name="apa-infusion-reference"></a>Fluid Project. (2026). *Infusion documentation: Preferences framework*. Inclusive Design Research Centre, OCAD University. https://docs.fluidproject.org/infusion/development/
[Return to citation](#apa-infusion-citation)

<a name="apa-google-fonts-reference"></a>Google Fonts. (2026). *Google Fonts*. Google LLC. https://fonts.google.com
[Return to citation](#apa-google-fonts-citation)

<a name="apa-mdn-fontface-reference"></a>MDN Web Docs. (2026). *@font-face*. Mozilla Foundation. https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face
[Return to citation](#apa-mdn-fontface-citation)

<a name="apa-wcag-reference"></a>W3C. (2023). *Web Content Accessibility Guidelines (WCAG) 2.2*. World Wide Web Consortium. https://www.w3.org/TR/WCAG22/
[Return to citation](#apa-wcag-citation)

## Changelog

| Version | Status | Notes |
|---------|--------|-------|
| 0.1.0 | Draft | Initial draft covering colour tokens, type roles, adding and self-hosting fonts, and the accessibility text-size factor |
