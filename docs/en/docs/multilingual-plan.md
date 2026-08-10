# Multilingual + Accessibility Migration Plan — BLNK Studio

**Launch locales:** `en-CA` (default) and `fr-CA`
**Architecture goal:** support *any* language — including RTL and non-Latin scripts — without a second rebuild
**URL strategy:** every language gets a prefix, old flat URLs 301'd
**Translation workflow:** developer-managed JSON for UI strings; blog content via Sveltia now, SAT later
**Accessibility:** Infusion UI Options adjuster + self-voicing

---

## 1. The core problem

The site has no templating layer. `.eleventy.js` sets:

```js
htmlTemplateEngine: false,
```

with the comment *"Plain .html pages are copied verbatim … so the existing hand-built pages are never altered."* Seven hand-built HTML pages are copied through untouched. There is no shared layout, no partials, and no string layer.

| Surface | Current state | Why it blocks i18n |
|---|---|---|
| 7 `.html` pages, ~2,400 lines | Copied verbatim, zero templating | Cannot inject a locale or a string |
| Nav + footer | Duplicated **8 times** | Every translated nav would be duplicated 8× per language |
| ~5,300 words of copy | Hardcoded in markup | Nothing to translate against |
| Inline `<script>` blocks (8) | Contain user-facing English | A third string surface beyond HTML and JSON |
| `sitemap.xml` | Static, hand-maintained | Cannot express `hreflang` alternates |
| `readableDate` filter | Hardcodes `en-GB` | Renders English dates on French pages |
| `catSlug` filter | Maps English category words | Breaks the moment a category is translated |

**Nothing else in the stack resists this.** Eleventy 3.0, Netlify, and Sveltia are all fine. The work is almost entirely converting verbatim HTML into templates — the exact thing the current config was written to avoid.

### Pre-existing bugs this migration fixes

- `src/_includes/article.njk:60` and `:139` — `href="contact.html"` with no leading slash, on pages served at `/blog/<slug>/`. Both resolve to `/blog/<slug>/contact.html`. **Two broken links on every blog post today.**
- `src/index.html:44` — home nav links to `#top`; every other page links to `index.html`. Same nav, drifted.

---

## 2. Sequencing: layout, multilingual, or accessibility first?

**Multilingual first, accessibility second, layout folded into the first pass.**

1. **Cost of a layout change collapses after the migration.** Today a nav change is 8 coordinated edits. After Phase 2 it is one. Styling now means paying the 8× cost, then re-verifying 8 pages again.

2. **French expansion and UIO text scaling are the same failure mode.** French-Canadian copy runs ~20–25% longer than English; Infusion's text-size adjuster does the same thing on demand. The `en-XA` pseudo-locale in Phase 6 (30% padding) tests *both at once*. Build that harness first and it de-risks the accessibility work for free — do the design first and you design blind, then redesign twice.

3. **Both CSS sweeps compound.** Phase 6 converts directional properties to logical ones (47 declarations) and reworks 30 `clamp()` type declarations for UIO. A redesign after those inherits them; a redesign before means sweeping the new CSS too.

**Structural layout changes** — different nav items, sections added or removed — belong in **Phase 2**, when the markup is being rewritten anyway. Not before, not as a separate pass after.

### A layout hazard to fix during Phase 2

`src/index.html` hand-splits the hero headline for the reveal animation:

```html
<span class="line"><span>Your brand should be</span></span>
<span class="line"><span>working <em>harder</em> than</span></span>
<span class="line"><span>your portfolio.</span></span>
```

Hardcoded line breaks do not survive translation, and they do not survive text scaling either. **Fix:** store the lines as a per-locale array (`home.hero.titleLines`) and loop them. Each language controls its own break points, the animation is preserved, and UIO can reflow.

---

## 3. Target architecture

### One template per page, generated once per locale

Rather than duplicating markup into `src/en-ca/` and `src/fr-ca/`, each page stays a **single source file** and Eleventy pagination emits one output per locale:

```yaml
---
pagination:
  data: locales.list
  size: 1
  alias: locale
permalink: "/{{ locale.code }}/{{ t.routes.about }}/index.html"
---
```

One `about.njk` → `/en-ca/about/` and `/fr-ca/a-propos/`. Adding a third language is a line in a config file, not a copy of every page.

### Route slugs are per-locale data, not shared

Note the permalink above uses `t.routes.about`, not a literal. This follows from SAT's archive model (§6) and is better i18n SEO — in-language URLs rank better in that language:

```jsonc
// en-ca.json
"routes": { "about": "about", "services": "services", "freeAudit": "free-audit", "blog": "blog" }
// fr-ca.json
"routes": { "about": "a-propos", "services": "services", "freeAudit": "audit-gratuit", "blog": "articles" }
```

### File layout after migration

```
src/
  _data/
    locales.json         ← locale registry (code, htmlLang, dir, label, fonts)
    i18n.js              ← loads + deep-merges locale bundles over the default
    workIndex.js         ← sat:work / page-key → { locale: url }  (see §4, §6)
  _locales/{en-ca,fr-ca}.json  ← UI strings + route slugs, namespaced by page
  _includes/
    layouts/{base,page,article}.njk
    partials/{nav,footer,final-cta,lang-switcher,a11y-bar}.njk
  pages/*.njk            ← index, about, services, contact, free-audit, blog, privacy
  content/blog/{en-ca,fr-ca}/*.md
  sitemap.njk            ← generated, with hreflang alternates
  _redirects             ← Netlify 301s from the old flat URLs
```

### Locale registry

`src/_data/locales.json` carries `dir` from day one even though both launch locales are LTR — this is the "support all language types" requirement made structural rather than aspirational. Codes follow the IANA subtag registry, matching SAT's ADR-003.

```json
{
  "default": "en-ca",
  "list": [
    { "code": "en-ca", "htmlLang": "en-CA", "dir": "ltr", "label": "English" },
    { "code": "fr-ca", "htmlLang": "fr-CA", "dir": "ltr", "label": "Français" }
  ]
}
```

**Two fields, deliberately cased differently.** `code` is the URL segment and is lowercase, because paths are case-sensitive and lowercase is the convention — `/en-ca/about/`. `htmlLang` is the BCP 47 tag whose canonical form uppercases the region, and it feeds `<html lang>`, `hreflang`, `Intl` date formatting, and Infusion's speech-synthesis `utteranceOpts.lang` — `en-CA`. A separate `hreflang` field was dropped as redundant: it would always equal `htmlLang`, and two fields holding one value eventually disagree.

`code` is also the bundle filename (`_locales/en-ca.json`) and the key in the merged `i18n` object, so each locale has exactly one identifier.

This one file feeds the `<html lang dir>` attributes, the hreflang set, the language switcher, date formatting, font loading, **and** Infusion's self-voicing utterance language (§5).

### String resolution with fallback

`src/_data/i18n.js` deep-merges each locale over the default, so a missing French key renders **English rather than blank**, and the build reports what fell back. Templates read `{{ t.about.hero.title }}`, with `t`, `lang`, and `dir` supplied once via `eleventyComputed` in a directory data file.

---

## 4. Language switcher

~0.5 day, split across Phases 2 and 5.

### It must link to the equivalent page — and it cannot do that by path arithmetic

The common failure is a switcher that goes to the homepage, dumping the reader out of what they were reading. The *less* obvious failure is specific to this build: **because route slugs and post slugs are localized (§3, §6), you cannot derive the French URL by swapping a path segment.** `/en-ca/free-audit/` does not become `/fr-ca/free-audit/`; it becomes `/fr-ca/audit-gratuit/`.

This rules out Eleventy's `locale_links` / `locale_url` helpers, which resolve alternates structurally. Instead, build a **work index** — `src/_data/workIndex.js`, a build-time map from a stable identity to per-locale URLs:

```
"page:free-audit"                          → { en: "/en-ca/free-audit/", fr: "/fr-ca/audit-gratuit/" }
"urn:uuid:018f2a91-…"  (a post's sat:work) → { en: "/en-ca/blog/…/",     fr: "/fr-ca/articles/…/" }
```

Static pages key off the template filename; posts key off `sat:work` (§6). The switcher **and** the `hreflang` block both read from this one map, so they can never disagree. This is identity-based rather than convention-based, which is exactly ADR-010's argument for `sat:work` in the first place.

Fallback chain when a counterpart doesn't exist (Phase 4 hides untranslated posts from the other locale's listing, so this will happen): equivalent page → nearest translated ancestor (`/fr-ca/articles/`) → never the homepage, never a dead link, never hidden. Say so on arrival rather than silently landing the reader somewhere else.

### Preserve the query string and hash — specific to this site

`src/contact.html:259` reads `?package=` from the URL; Services page buttons set it to pre-fill the "Applying for: X" note and the hidden `package` field. A switcher built as a plain static `href` drops it, so a user switching language on the contact page **silently loses their package selection** and the lead arrives unattributed. Carry `location.search` and `location.hash` through the switch.

### Shape, naming, placement

- **Two locales → a direct link to the other language**, not a dropdown. One partial branches on `locales.list.length`, becoming a `<details>`/`<summary>` disclosure at three or more. `<details>` keeps it working without JS — and these are the links crawlers follow to confirm your hreflang pairs.
- **Endonyms**: `Français`, never `French`. No flags — flags are countries, and `fr-CA` vs `fr-FR` makes that awkward immediately.
- Mark the language on the link so screen readers switch pronunciation. This also drives correct self-voicing pronunciation (§5):
  ```html
  <a href="/fr-ca/a-propos/" hreflang="fr-CA" lang="fr-CA">Français</a>
  ```
- **Two insertion points required.** `src/css/home.css:531` sets `.nav__links, .nav__actions { display: none }` at the mobile breakpoint — a switcher in `nav__actions` **disappears on phones**. Render the partial in both `nav__actions` and `nav__mobile`.
- Watch `src/css/home.css:270`: `.nav__mobile.is-open { max-height: 560px }` is a hard cap sized for 5 links and 2 buttons. A language row plus an accessibility control, with wrapping French labels, can exceed it and **silently clip the last menu item**.

### No auto-redirect, no sticky persistence at launch

Phase 5 rules out `Accept-Language` redirects. Skip remembering the choice too — a stored value that overrides an explicit URL is what produces "I clicked an English link and got French," and it breaks shared links. If you want it later, use a dismissible suggestion banner, not a redirect. (This is a *different* case from the UIO preference cookie in §5, which stores an explicit user choice rather than an inferred one.)

### Accessibility

`<nav aria-label="Language">` with the label translated; `aria-current="true"` on the active locale in the dropdown variant; `:focus-visible` styled (the nav uses custom `::after` underlines that are easy to lose); Escape closes the disclosure.

---

## 5. Infusion accessibility bar + self-voicing

Fluid Infusion's UI Options (UIO) adjuster — text size, line spacing, font family, contrast themes, table of contents, link emphasis, larger inputs — plus self-voicing.

### Three things that make this unusually viable here

1. **Zero `px` font sizes.** The CSS is 106 `rem` and 30 `clamp()` declarations, no `px` type at all. UIO's text-size adjuster works by scaling the root font size, and px-based type is simply immune to it. Most sites need a full typography rewrite before UIO does anything; you don't.
2. **Infusion ships `_fr` and `_en_CA` message bundles** across the prefs framework (`contrast_fr.json`, `captions_en_CA.json`, …). The accessibility panel is localizable to exactly your two launch locales with no translation authoring. Bundles are `_fr`, not `_fr_CA` — `fr-CA` resolves to `fr` by fallback, which is correct behaviour here.
3. **There is a URL-path locale example** — `examples/framework/preferences/localizationPreference/urlPath/fr` — which matches the `/fr-ca/` prefix strategy chosen in §3 exactly. The integration pattern is already demonstrated.

### The one real CSS problem: `clamp()` and UIO do not compose

All 30 fluid-type declarations follow `clamp(Xrem, Yvw, Zrem)` — for example `clamp(2.2rem, 5.5vw, 4.3rem)`.

UIO scales the **root font size**. `vw` does not respond to root font size. So when a user doubles their text size, the `rem` bounds move but the `vw` preferred value stays put — headings scale erratically or barely at all while body copy (plain `rem`) scales fully. The type hierarchy inverts precisely for the user who most needs it.

**Fix:** give every preferred term a `rem` component — `clamp(2.2rem, 1.4rem + 2.6vw, 4.3rem)`. Thirty declarations, mechanical, and a WCAG 1.4.4 (Resize Text) improvement independent of Infusion.

### Layout collision: the fixed nav

`src/css/home.css:210` — `.nav { position: fixed; top: 0; z-index: 1000 }`, with the loader at `z-index: 9999`. UIO's separated panel mounts at the top of the document and pushes content down. With a fixed header it will overlap instead. Needs the panel above the nav in z-order and the nav's `top` offset driven by panel height on open/close. This is the most common UIO integration bug on sites with sticky headers — plan for it rather than discovering it.

### Self-voicing

Confirmed from source: `src/components/textToSpeech/js/TextToSpeech.js` wraps the browser's native `window.speechSynthesis` / `SpeechSynthesisUtterance`, exposing `utteranceOpts` with `lang` ("the BCP 47 language code for the synthesized text"), plus `voice`, `volume`, `rate`, `pitch`.

Wire `lang` from the locale registry — `locales.json` already carries `htmlLang` as `en-CA` / `fr-CA`, which is exactly BCP 47. Two things to handle:

- **There is no guaranteed French voice.** `speechSynthesis.getVoices()` depends on the user's OS. With no `fr-CA` or `fr` voice installed, browsers commonly fall back to a default voice reading French text with English phonemes — unintelligible rather than merely imperfect. Detect available voices for the page locale and either warn or hide the self-voicing control.
- **The voice list loads asynchronously.** `getVoices()` frequently returns empty on first call; you must listen for `voiceschanged`. This is the standard Web Speech footgun.
- The per-link `lang` attributes specified in §4 pay off here — "Français" gets pronounced correctly mid-page.

### Performance — the biggest cost in this project

The site currently ships one 227-line vanilla JS file and no framework. Infusion is jQuery-based and substantial. Use a **custom build** (UIO + TTS only, not the full framework), load it `defer`, and mount the panel after first paint so it stays off the LCP path of a marketing site. Budget and measure this explicitly.

### Privacy policy

UIO persists preferences in a cookie. `src/privacy.html` needs a line covering it — functional/strictly-necessary category and generally consent-exempt, but it must be disclosed.

Licensing is BSD-3-Clause / ECL-2.0 — fine commercially.

---

## 6. SAT integration

SAT's pipeline is **ingress (normalize) → egress (platform-neutral) → transmog (platform-specific)**. Per ADR-012, archives are pure content: no SSG frontmatter lives in the archive. Publishing vectors read the Dublin Core sidecar and emit whatever the target SSG needs.

Custom transmogs are SAT's designed extension mechanism for egress, and normalization already happens at ingress. So the site needs **no bespoke importer and no adapter layer** — the entire integration is a new transmog target, written against a spec file. This is the sanctioned path, not a workaround, which is what makes the front-matter contract in this section worth settling precisely: whatever we specify, the vector can emit.

### Build an `eleventy-transmog` vector

ADR-017 §Context: *"Hugo is the first publishing vector implemented for SAT. The decisions made here establish patterns that subsequent vectors (mkdocs-transmog, **eleventy-transmog**, and others) will follow."*

`en/bin/transmog/definitions/frontmatter/` already holds `default-`, `github-`, `html-`, `mkdocs-`, and `pdf-frontmatter-spec.yml`. There is no Eleventy spec. That absence is the deliverable.

Following ADR-017's two-phase split:

- **Phase 1 — `eleventy-transmog`**: reads the metadata cascade, writes a cached `eleventy/frontmatter.yml` inside the document's assets directory. Requires archive write access; triggered per-document by the ADR-014 watcher.
- **Phase 2 — `eleventy-assemble`**: reads prose plus cached frontmatter and writes into `src/content/blog/<locale>/` in this repo. Requires no archive write access; triggered by operator or build pipeline.

Phase 2's output directory being the site repo keeps the boundary clean: the site never reads SAT's archive, and SAT never learns Eleventy's internals beyond one spec file.

### `sat:work` replaces the `translationKey` I proposed

ADR-010 §7 is explicit: the Hugo vector emits Hugo's `translationKey` from `sat:work` at transmog time, because *"the field belongs to the published output, not to the canonical record."* Eleventy has no built-in equivalent, so emit `sat:work` verbatim into front matter and let the work index (§4) build the pairing.

**This supersedes the `translationKey` field in my earlier draft.** Minting a parallel identity scheme when SAT already has a UUID-based one that survives renames, moves, and re-slugs would be a straightforward mistake.

### The correction this forces: localized slugs

ADR-001 and ADR-010 are explicit that language archives are independent — an English `en/produits/henson-aircraft-aluminum.md` and a French `fr/produits/henson-aluminium-aeronautique.md` *"share no structural relationship — they are in separate language archives with independent paths, filenames, and slugs. This is correct and intentional."* ADR-017 §3 adds that archives use language-native directory names (`products/` vs `produits/`).

My earlier draft assumed mirrored paths (`/en-ca/blog/x/` ↔ `/fr-ca/blog/x/`). That is wrong against SAT's model — and it is also worse i18n SEO. Three consequences, already folded into §3 and §4:

1. Route slugs move into `i18n/*.json` as per-locale data.
2. The language switcher resolves through the work index, not path arithmetic.
3. Phase 5 redirects map old flat English URLs to new **English** routes only. French routes are new URLs with no history to preserve.

### Operational hazard: two writers, one directory

Sveltia and SAT would both write markdown into `src/content/blog/<locale>/`. SAT's assemble step is generative and will overwrite. **A client edit made in Sveltia is silently destroyed on the next assemble.** Decide ownership before both are live — either SAT-managed posts live in a subdirectory Sveltia's collection does not cover, or front matter carries a `source: sat` marker that Sveltia's collection filters out.

### Do not block the site migration on SAT

ADR-017 is `status: HOLD`, pending the ADR-010 identity infrastructure (per-expression `dc:identifier`, `sat:work`) being implemented. The Eleventy vector cannot be finished until identifier minting exists.

So: **Phases 1–7 proceed on Sveltia and hand-authored markdown.** The vector lands afterwards and needs no site-side changes, provided the front-matter contract is agreed now — which is the point of specifying it while egress is still flexible:

| Field | Source | Notes |
|---|---|---|
| `title` | `dc:title` | |
| `date` | `dc:date` | ISO 8601 |
| `excerpt` | `dc:description` | Never inherits (ADR-010 §5) |
| `category` | `dc:subject` | **Locale-independent slug** — see Phase 4 |
| `lang` | archive `language.code` | Drives collection filtering |
| `sat:work` | identity record | Translation pairing (§4) |
| `dc:identifier` | identity record | Per-expression, immutable |
| `image`, `readtime`, `featured`, `draft` | site-specific | Not DC; needs a `sat:` extension or spec-level default |

That last row is the open question worth settling early: `featured`, `readtime`, and `draft` are presentation concerns with no Dublin Core equivalent, and ADR-012 says presentation metadata does not belong in the archive. Cleanest resolution is that the Eleventy frontmatter spec supplies defaults and the site treats them as optional.

---

## 7. Phased delivery

### Phase 1 — Foundation *(~0.5 day)*

**Status: complete.** `htmlTemplateEngine` set to `"njk"` (verified first that no page contains a literal `{{`, `{%` or `{#`). Added `locales.json`, `i18n.js`, `_locales/{en-ca,fr-ca}.json` with the route tables, and an empty `_redirects` plus its passthrough and a watch target on `_locales`. `readableDate` now takes an optional BCP 47 tag and defaults to the default locale.

Two deliberate departures from this plan as originally written:

- **Bundles live in `src/_locales/`, not `src/_data/i18n/`.** Eleventy auto-namespaces `_data` subdirectories, so `_data/i18n/en-ca.json` would claim the `i18n.en` key and collide with `_data/i18n.js`'s own `i18n` key. Keeping the raw bundles outside `_data/` leaves one owner for the key.
- **The `sitemap.xml` passthrough stays for now.** Removing it here would leave the live site with no sitemap for the duration of Phases 1–4, since `sitemap.njk` does not exist until Phase 5. The removal ships with its replacement.

**Dates and time zones — decided.** Full precision in storage and markup, simplicity in display.

- **Stored** as a full ISO 8601 instant carrying the author's offset (`2026-05-14T09:30:00-04:00`). `src/admin/config.yml` uses `format: "YYYY-MM-DDTHH:mm:ssZ"` with `picker_utc: false`, so the picker records the offset that actually applied.
- **Displayed** as a date only, rendered in the declared publication zone `America/Toronto` (`src/_data/site.json`). Two independent reasons to pin it: the rendered day must not depend on which machine ran the build, and it must not drift with whichever author wrote the post. A Kolkata-authored post stamped `2026-05-15T03:00:00+05:30` correctly shows the studio's day — May 14.
- **Machine-readable** through `<time datetime="…">` carrying the full instant. That is where the precision belongs, and what schema.org `datePublished` and `og:article:published_time` will want in Phase 2.
- **Legacy date-only posts** resolve to exact UTC midnight, which is 20:00 the previous day in Toronto and would render the whole back catalogue a day early. `publicationInstant()` treats an exact-UTC-midnight value as a calendar date and re-anchors it to midnight in the publication zone. Offsets come from `Intl` per instant, so daylight saving is automatic — verified that January renders `05:00Z` (EST) and May `04:00Z` (EDT).

Verified identical output with the build machine at UTC, `America/Vancouver`, and `Asia/Kolkata`. Display format is locale-native: `May 14, 2026` in en-CA, `14 mai 2026` in fr-CA.

If the site later adds events, webinars, or relative times ("posted 3 hours ago"), those are reader-facing instants and will additionally want `timeZoneName: "short"` — the storage format already supports it.

**Checkpoint met:** the only output diffs against the previous build are the 10 blog post dates (`27 May 2026` → `May 27, 2026`, en-GB → en-CA) and the new `_redirects`. All 7 HTML pages are byte-identical, confirming the Nunjucks flip is inert.

### Phase 2 — Templating extraction *(2–3 days — the bulk)*

**Status: complete.** All 7 pages converted to `src/pages/*.njk`, plus `_includes/article.njk` rebuilt on the shared shell and `404.html` repointed. Extracted `layouts/base.njk` and `partials/{nav,footer,final-cta}.njk`; `pages/pages.11tydata.js` holds the locale pagination and computes `t`, `urls` and `permalink`; `content/blog/blog.11tydata.js` does the same for posts.

Pages use Nunjucks `{% extends %}` with a `{% block scripts %}` rather than Eleventy's `layout:`, specifically so each page's inline `<script>` still renders *after* the footer where it sat originally.

**Verified** by comparing rendered visible text and tag structure against the pre-migration build. Every page and post is text-identical except three intended changes:

| Page | Diff | Why |
|---|---|---|
| all | `<html lang="en-CA" dir="ltr">` | was `lang="en"`; now driven by the locale registry |
| `services` | footer `About`/`Services` order | see drift below |
| blog posts | `13 May 2026` → `May 14, 2026` | the Phase 1 time zone fix, confirmed |

That last row is worth noting: the baseline build rendered **13 May** for a post authored `2026-05-14`, because the build machine is UTC−4. It is now correct on any machine.

**Bugs fixed as a side effect of deduplication:**

- The two `href="contact.html"` links with no leading slash on every blog post — confirmed 2 → 0.
- Every blog post declared `rel="canonical"` of `https://www.theblnkstudio.com/article.html`, a URL that does not exist. All ten posts shared it. Now derived from `page.url`.
- `404.html` used relative asset paths, but Netlify serves it at the *requested* URL — so a 404 at `/blog/foo/bar` resolved CSS to `/blog/foo/css/home.css` and rendered unstyled. Now root-relative.

**Drift found and how it was handled.** The duplicated nav and footer had diverged in five ways. Four were real per-page variation and are now parameters, not flattened: the home page's `#top` self-links, `contact`'s `tel:` mobile CTA, `free-audit`'s `#request` retarget with `aria-current="page"`, and the `footer__muted` line (a 4/4 split, preserved per page behind a flag). The fifth was accidental — `services.html` listed `Services` before `About` in the footer where the other six pages do the reverse — and is resolved to the majority order.

**Checkpoint met.**

### Phase 3 — String extraction *(1–2 days — in progress)*

~5,300 words into `en-ca.json`, namespaced. Estimate 350–450 keys, plus the route slug table.

**Slice A — contact details → `_data/site.json`. Done.** All 39 source literals for six facts (email, phone display, `tel:` href, WhatsApp, Instagram URL and handle) now resolve from one block. Verified by swapping in a placeholder Quebec number and rebuilding: **184 occurrences across 24 output files changed from a single edit, with no stale references left**. Two mechanisms made this work where front matter cannot interpolate:

- `*Contact` keys alongside the existing `*Route` keys — `ctaBtn1Contact: "phoneHref"` resolves against `site.contact` in the partial. Resolution order is `*Href` (literal) → `*Contact` → `*Route` → partial default.
- A `{phone}` placeholder in labels, so a number inside a sentence still has one source: `ctaBtn1Label: "Call {phone}"`.

**Slice B — shared chrome → `_locales/en-ca.json`. Done.** ~25 keys under `common.nav`, `common.footer` and `common.cta`, covering the nav and footer link labels, headings, aria-labels, image alt text, the tagline and the default CTA microcopy. `fr-ca.json` deliberately does not define `common` yet, which exercises the fallback: the build now reports `[i18n] fr-ca: 1 key(s) falling back to "en-ca" — common` and renders English until Phase 7 supplies French.

**Slice C — page body copy. Done.** All seven page bodies extracted, plus the user-facing English inside the inline `<script>` blocks. **`_locales/en-ca.json` now holds 520 keys** across `routes`, `common`, `home`, `about`, `services`, `blog`, `contact`, `freeAudit` and `privacy`. No English literal remains in any page body or partial.

Extraction ran through a helper that verifies each string matches **exactly once** before substituting, so nothing was silently mis-replaced. Four things it caught that hand-editing would not have:

- **Short strings collide.** "All" also occurs inside "All articles", "Read" inside "Read article", "Subscribe" inside "Unsubscribe". The matcher anchors on element-content (`>text<`) and attribute-value (`="text"`) boundaries before falling back to a bare match.
- **Repeated labels get one key, not many.** "Enquire" appears 7× on services and "Read Article" 3× on the home page; these are single shared keys rather than duplicates a translator would have to keep in sync.
- **Front matter had to be excluded** from the search — "Work With Us" is legitimately both a hero button and `ctaBtn1Label`, which otherwise read as an ambiguous double match.
- **Contractions.** Writing "We are not" where the source says "We're not" fails loudly as MISSING rather than silently skipping.

Bundle strings render with `| safe` for the same reason the base layout's copy fields do: they hold the exact HTML fragment from the source (`SEO &amp; Content`, `We're`), and autoescaping would double-encode them into `&amp;amp;` and `&#39;`. They are build-time authored constants, never user input.

Inline script strings are injected with `| dump`, which JSON-encodes the value into a valid JS string literal rather than splicing raw text into quotes.

**Not extracted, deliberately:** section numbering (`P/01`, `01 / 07`), animated counter start values (`+0%`, `0+`), and the `&rarr;` glyphs. These are not translatable content.

Verified after each slice: every page and post is still text-identical to the pre-migration build, with only the two known intended diffs. The comparison collapses whitespace (HTML does too, so re-wrapping a paragraph into a single-line bundle string is not a content change) and excludes `<script>`/`<style>` contents, which are not visible text.

With all eight namespaces now present in `en-ca.json` and absent from `fr-ca.json`, the build reports:

```
[i18n] fr-ca: 8 key(s) falling back to "en-ca" — common, privacy, about, blog, contact, freeAudit, home, services
```

French pages render complete English until Phase 7 supplies translations.

**Content issues logged during Phase 2, to resolve here.** Phase 2 was a pure refactor and preserved all of these verbatim:

1. **CTA label does not match its link.** On the blog index and every blog post, the primary button reads "Get a Free Audit" but points at the contact page. Either relabel it or repoint it at `freeAudit`. Currently carried in `pages/blog.njk` and `content/blog/blog.11tydata.js` as `ctaBtn1Label`.
2. **`privacy` has no Open Graph tags at all** — no `og:title`, `og:description`, or `og:type`, unlike every other page. The base layout makes the block conditional so the gap is preserved. Add them or decide it is deliberate.
3. **The `footer__muted` line is a 4/4 split** — "Response within 24 hrs · Mon–Sat" appears on home, about, services and privacy but not on contact, free-audit, blog or article. Preserved per page behind `footerMuted`. Pick one and drop the flag.
4. **Blog posts emitted two `og:image` tags** when a post had a cover image — one from the post, one hardcoded. The shared layout now emits one, preferring the post's own.

**Contact details are the highest-value extraction, and they are changing shortly.** `hello@theblnkstudio.com` appears 13 times across 8 files, the phone number 38 times, the Instagram handle 18, and `wa.me` links 26 — roughly 95 literals expressing four facts. These belong in `src/_data/site.json` (already created for `publicationTimeZone`) rather than the locale bundles, since they are identical in every language. The phone number is moving to a North American / Quebec number and the email addresses are changing, so this extraction converts an error-prone 95-literal edit into a 4-line one.

Do not miss the **third string surface**: the 8 inline `<script>` blocks hold user-facing English — `"Applying for: "`, `"Sending..."`, `"Send the brief"`, and the mailto fallback subject and body in `contact.html` and `free-audit.html`. Move these to `data-` attributes on the form, populated from `t`. `src/js/main.js` is already clean and should stay locale-free.
**Checkpoint:** zero English literals in `src/pages/` or `_includes/`, verified by grep.

### Phase 4 — Blog *(~1 day — done)*

**Status: complete**, and the language switcher from §4 shipped with it, having been blocked on this phase's work index through Phases 2 and 5.

- Posts moved to `content/blog/{en-ca,fr-ca}/`. Locale is read off the **file path**, not declared in front matter — SAT's ADR-001 model of language as filesystem structure.
- Every post carries `"sat:work"` (quoted; the key contains a colon). All ten English posts were assigned UUIDs.
- `category` is now a locale-independent slug (`branding`, `websites`, `seo`, `social`, `growth`); labels come from `blog.filters.*` in the bundle. The `catSlug` filter is deleted.
- One `posts_<locale>` collection per locale, so the folder *is* the filter — an untranslated post simply does not appear in the other locale's listing.
- `src/_data/workIndex.js` maps `sat:work` → `{ locale: slug }`.
- `src/admin/config.yml` now has two collections, one per locale folder, with a "Translation link (sat:work)" field so an editor can pair a translation from the dashboard.

**The work index is built by reading front matter off disk, not from an Eleventy collection.** A collection would depend on each post's computed permalink, while the permalink needs the alternates the index provides — a cycle. Reading files directly breaks it, matching how `_data/i18n.js` already works. It also throws if two posts in the same locale share a `sat:work`, which fails the build with a named message rather than silently producing a broken pair.

**Proven end to end** with one translated post: `/en-ca/blog/rebrand-or-refine/` ↔ `/fr-ca/articles/refondre-ou-ajuster/`. Deliberately different slugs, paired only by identity — reciprocal hreflang on both, both in the sitemap, category and date rendered per locale (`Branding` / `Image de marque`, `May 21, 2026` / `21 mai 2026`) off the same `datetime` instant. Untranslated posts emit **no** hreflang rather than a self-referencing pair.

**Language switcher (§4) — shipped.** A direct link to the other language, becoming a `<details>` disclosure at three or more locales. Rendered twice, into `nav__actions` and `nav__mobile`, because `home.css:531` hides `.nav__actions` at the mobile breakpoint. Endonyms, `lang`/`hreflang` on each link, and `switcher` computed per page so every target is resolved through the work index. A post with no counterpart falls back to that locale's blog index and is marked `data-fallback="true"` — never the homepage, never a dead link. `main.js` carries `location.search` and `location.hash` across the switch, which is what stops `/contact/?package=Website%20Sprint` from losing the package selection.

**Verified:** 16 pages hreflang-reciprocal, 25 sitemap URLs (16 with alternates), and **zero broken switcher links** across the whole build.

#### Original notes for this phase

Split posts into `content/blog/{en-ca,fr-ca}/`; move the existing 10 to `en/`. Add `sat:work` to front matter (§6) — not `translationKey`. Replace `catSlug` with a locale-independent `category` slug (`branding`, `seo`, `websites`, `social`, `growth`), display labels moving to `i18n/*.json`. Locale-filter the `posts` collection. Build `workIndex.js`.

Untranslated posts are **hidden from the other locale's listing**, and hreflang alternates are emitted only for locales that actually have that post — no thin or duplicate pages. Update `src/admin/config.yml` with one Sveltia collection per locale folder.

### Phase 5 — Routing, redirects, SEO *(~0.5 day — done)*

**Status: complete.** `src/_redirects` carries 11 rules covering every pre-migration URL; `sitemap.xml` is now generated by `src/sitemap.njk` (24 URLs, 14 with reciprocal hreflang); canonical, the full hreflang set and `x-default` are emitted from `base.njk`. Blog posts moved under the locale prefix in this phase rather than Phase 4, so no URL is left on the old flat scheme. All three Netlify forms carry a hidden `locale` field, and `robots.txt` now disallows `/admin/`.

`alternates` and `xDefault` are computed once per page in `pages.11tydata.js` and read by *both* the `<head>` block and the sitemap, so the two cannot drift. They are keyed off `routeKey`, not path arithmetic — `/en-ca/about/` → `/fr-ca/a-propos/` cannot be derived by swapping a segment.

**Three bugs found during verification:**

1. **Every `/fr-ca/` page was missing from the sitemap.** Eleventy's `pagination.addAllPagesToCollections` defaults to `false`, so `collections.all` held only the *first* output of each paginated template. The French pages were real and indexable but absent from the sitemap — a silent half-launch. Now set explicitly.
2. **`/admin/`, the Sveltia CMS dashboard, was being listed** in the sitemap. Excluded, and disallowed in `robots.txt`.
3. **Three blog posts had hardcoded `/free-audit.html` links in their markdown.** The redirects would have caught them, but internal links should not take a 301 hop — and hardcoding a locale breaks the moment a post is translated. Markdown renders through Nunjucks here, so they became `{{ urls.freeAudit }}` and now follow the post's own locale. All 49 rendered links resolve to `/en-ca/free-audit/`.

**Verified:** content still identical to the pre-migration build; 14/14 locale pages hreflang-reciprocal; `x-default` on French pages points at the English original; zero stale flat URLs anywhere in the output.

**Deferred to Phase 7:** the root `404.html` is still English-only. Netlify serves only `/404.html`, so it should be bilingual — that needs French copy.

---

#### Original notes for this phase

```
/                 /en-ca/             301
/about.html       /en-ca/about/       301
/services.html    /en-ca/services/    301
/contact.html     /en-ca/contact/     301
/free-audit.html  /en-ca/free-audit/  301
/blog.html        /en-ca/blog/        301
/privacy.html     /en-ca/privacy/     301
/blog/:slug/      /en-ca/blog/:slug/  301
```

`sitemap.xml` becomes `sitemap.njk` with `xhtml:link rel="alternate"` per URL group, driven by the work index. Canonical + full hreflang set including `x-default` → `/en-ca/`.

**Do not auto-redirect on `Accept-Language`** — Google discourages it and it traps users. **404:** Netlify serves only the root `404.html`; a `/fr-ca/404/` will not be picked up, so keep the root one bilingual. **Netlify Forms:** keep one form `name` per form type across locales so submissions land in one inbox, and add a hidden `locale` field so you know the lead's language.

Post-deploy: resubmit the sitemap and expect a few weeks of settling.

### Phase 6 — Any-language readiness *(~1 day — done)*

**Status: complete.** 51 declarations converted to logical properties; two `left:` kept physical on purpose and commented; both pseudo-locales working; fonts driven by the locale registry; two build guards in place.

**Logical CSS sweep.** `margin/padding/border-left|right` → `-inline-start|end`, `text-align: left` → `start`, and `left:` → `inset-inline-start` **only where it positions directional decoration** (checkmark and badge markers, the nav underline). Two stayed physical and say why in a comment:

- `.cursor-glow` is positioned by `main.js` from raw mouse coordinates, so it must not mirror.
- `.nav` is full-bleed at `width: 100%`, where direction is irrelevant.

The sweep also caught something the original estimate missed: **four asymmetric four-value `padding` shorthands** — `padding: 12px 0 12px 30px` — reserving space for the very markers being made logical. Converting the marker without the padding would have broken RTL in a way that only shows up visually. Now `padding-block` / `padding-inline`.

**Pseudo-locales**, enabled with `PSEUDO=1` (`npm run build:pseudo`) and never present otherwise:

| | | |
|---|---|---|
| `en-xa` | accented, padded ~30%, bracketed | catches strings the extraction missed *and* predicts French overflow |
| `ar-xb` | same text, `dir="rtl"` | proves the logical-property sweep works without committing to Arabic |

Generated from the default bundle at build time, with `routes` restored untouched afterwards — accenting a route slug would produce permalinks that 404. HTML tags, entities and `{placeholder}` tokens pass through unmodified. Verified `noindex` on every pseudo page, zero entries in the sitemap, and zero references from real pages' hreflang or switcher.

**Fonts** moved into the locale registry (`locale.fonts`). Inter / Inter Tight / Space Mono are Latin-only, so a future Devanagari, Arabic or CJK locale overrides one config field instead of every page.

**Two build guards, both verified by deliberately breaking them:**

1. **Missing keys fail a production build.** `ELEVENTY_RUN_MODE === "build"` throws with the offending keys named; serve/watch only warns, so a translator can work through a bundle without the site refusing to build. Confirmed Eleventy sets that variable on a plain `npm run build`, so it fires on Netlify.
2. **`npm run check:i18n`** compares rendered output across locales and reports text identical to the default. This catches the one thing the key guard cannot: a string still hardcoded in a template, which renders the same English everywhere and looks perfectly translated to the build. Proven by planting `Legal information here` in the footer partial. Numbers, contact details from `site.json` and an explicit brand allow-list are excluded, so a clean run means something.

#### Original notes for this phase

**Logical CSS properties** — convert `margin/padding/border-left|right`, `left`/`right`, `text-align`, and `float` to their logical equivalents. **47 declarations across 1,323 lines**; the CSS is already mostly flex/grid, so this is a couple of hours. This single sweep makes RTL a config change later rather than a rewrite.

**Pseudo-locales**, build-only, generated from `en-ca.json`, `noindex`'d, excluded from sitemap and hreflang, gated behind an env var:
- `en-XA` — accented and 30% padded. Catches strings missed during extraction (they stay plain English) *and* predicts both French overflow and UIO text-scaling overflow.
- `ar-XB` — mirrored RTL, proving the logical-property sweep worked without committing to Arabic content.

**Font strategy** — move the Google Fonts link into `base.njk`, driven by the locale registry. Inter / Inter Tight / Space Mono have no Devanagari, Arabic, or CJK coverage, so a future locale needs a per-locale stack; this makes that a config entry.

**Build guard** — fail the build when a locale JSON is missing keys the default has; grep built HTML for suspicious untranslated literals.

### Phase 7 — French integration and QA *(draft French landed early)*

**A machine-drafted `fr-ca.json` is in place at 100% coverage (575/575 keys)**, produced ahead of schedule so the layout risk could be measured against real French and so the translator has a base to react to rather than a blank file. It is **not reviewed copy**. The bundle carries a `_draft` key and every build prints:

```
[i18n] WARNING fr-ca is DRAFT — MACHINE-DRAFT — not reviewed by a translator.
```

Remove the `_draft` key once a translator has passed over it; the warning disappears with it.

**A real gap surfaced while checking the French output.** French pages were rendering an English `<title>`, meta description, Open Graph card and CTA copy — 55 strings that Phase 3 had deliberately skipped because they lived in front matter, which is plain YAML with no access to the active locale. This is an SEO defect, not a cosmetic one: it would have shipped French pages advertising themselves to search engines in English. Those strings moved into the bundle under `<ns>.meta`, `<ns>.pageCta` and `<ns>.pageNav`, resolved through `eleventyComputed`. **Front matter now holds only structural values** — `routeKey`, `pageKey`, `css`, `footerMuted`, route and contact references — and no copy at all.

**Measured expansion, which is the point of drafting early:**

| Page | EN | FR | Δ |
|---|---:|---:|---:|
| home | 4,827 | 6,013 | +24% |
| about | 3,693 | 4,678 | +26% |
| services | 11,310 | 13,691 | +21% |
| contact | 4,108 | 4,719 | +14% |
| free-audit | 4,167 | 4,860 | +16% |
| privacy | 3,073 | 3,955 | +28% |
| blog | 4,570 | 4,953 | +8% |
| **overall** | **23,587** | **28,899** | **+23%** |

98 individual strings grew more than 40%. The pressure is concentrated exactly where §2 predicted:

- **Nav labels grow hardest** — `Home` → `Accueil` (+75%), `About` → `À propos` (+60%), `Get Free Audit` → `Obtenir un audit gratuit` (+71%). The desktop nav is five links at `gap: 36px` plus a button; this is the component most likely to break first.
- **Hand-split hero lines grow 35–64%** — `services.showcase.titleLine1` +64%, `services.packages.titleLine1` +50%, `about.hero.titleLine2` +38%. Confirms the §2 recommendation to hold the lines as a per-locale array so each language sets its own break points.
- **Buttons** — `home.hero.ctaSecondary` +58% (24 → 38 characters).

Verified throughout: the English build stayed byte-identical, and hreflang/sitemap are unaffected (24 URLs, 14 with alternates).

#### Integration and QA — done

**Hero headlines now hold a per-locale array.** The five heroes had their line breaks hardcoded as separate `titleLine1/2/3` keys baked into three `<span class="line">` elements, so every language was forced onto the English break points. Each hero is now one `titleLines` array and the markup loops over it, which lets a locale use a different number of lines. English output is byte-identical.

That immediately paid for itself. The French, translated 1:1 onto the English breaks, had lines running far past the longest English line the layout was built around:

| Hero | Before | After | Lines |
|---|---:|---:|---|
| about | +52% | +0% | 2 → 3 |
| services | +48% | +9% | 3 → 4 |
| freeAudit | +39% | +13% | 3 → 4 |
| home | +20% | +0% | 3 → 3 |
| contact | +6% | +6% | 3 → 3 |

Rebalancing also caught a stray space before a period in the free-audit headline, an artifact of joining a suffix key. A translator can retune any of these without touching markup.

**Two nav constraints fixed, both flagged in §4 and §5:**

- `.nav__mobile.is-open` had a hard `max-height: 560px` sized for 5 links and 2 buttons. The menu now also carries a language row — 8 items — so the cap would silently clip the last one. Now `min(80vh, 760px)` with `overflow-y: auto`, which keeps the max-height transition working instead of truncating.
- `.nav__links` had a fixed `gap: 36px`. With French labels 60–75% longer plus the switcher, the row overflowed just above the 900px breakpoint. Now `clamp(18px, 2.4vw, 36px)`, which compresses before it breaks. Estimated fit at 900px: English ~732px, French ~804px.

**Bilingual 404.** Netlify serves one `/404.html` for every miss on the domain regardless of locale, so it cannot use the locale templates. It now carries both languages, each block with its own `lang` attribute so a screen reader switches pronunciation mid-page.

**Forms verified in both locales.** Both form types keep the *same* `name` across locales (`contact`, `audit`) so submissions land in one Netlify inbox, with the hidden `locale` field distinguishing them. Labels, placeholders, submit text, success copy and the mailto fallback subject/body all render French on French pages.

**Not verified: visual layout.** No headless browser runs in this environment, so every overflow figure above is a calculated estimate from string lengths, not a measurement. Run `npm run build:pseudo` and view `/en-xa/` to see the padded worst case, and `/fr-ca/` for the real copy.

#### Remaining for this phase

Populate `fr-ca.json`, fix the overflows `en-XA` predicted, verify hreflang reciprocity through the work index, test both form paths including the mailto fallback.

### Phase 8 — Infusion accessibility bar *(implemented, not yet run in a browser)*

**The `clamp()` fix described below was wrong, and is superseded.** Measuring it first showed why: within a 5% visual budget the achievable `rem` fraction was only 0.10–0.20, and it bought *nothing* — ×1.12 stayed ×1.12 at 1280px, because at 2× the `min` bound already dominates the `vw` term. Getting real scaling that way needed a full fluid-curve rewrite costing up to **27% deviation** at tablet widths.

Reading `Enactors.js` gave the actual answer: the textSize enactor publishes **`--fl-textSize-factor`** on `<html>`. So only the `vw` term needs scaling — the `rem` bounds already respond to the changed root size:

```css
font-size: clamp(2.15rem, calc(4.8vw * var(--fl-textSize-factor, 1)), 3.95rem);
```

Verified numerically: **byte-identical rendering when Infusion is absent** (the fallback of `1`), and **exactly ×2.00 at every viewport** when the reader sets 2× — against ×1.12–×2.00 erratic before. Applied to all 30 fluid declarations.

**Loading strategy — the real size lever.** Trimming was investigated and rejected on evidence: `dist/infusion-uio.js` contains zero demo/test code, `build:dist:uio` is literally `-i fluid-ui-options` (so the prebuilt bundle *is* the minimal custom build), and `buildModules.js` sets `compress: false, mangle: false` deliberately because the IoC resolves grades by string. **176 KB gzip is the floor.**

So `src/js/a11y.js` (1.9 KB gzip) loads Infusion **on demand**: on click, or eagerly when a marker cookie shows the reader already uses the bar, so their saved preferences apply without a visible reflow. **First-paint JS is 4.5 KB gzip with zero Infusion references**; visitors who never open the bar pay nothing.

**Other findings worth recording:**

- `fluid.uiOptions.multilingual(container, {locale, direction})` maps directly onto the locale registry. Infusion ships `en_CA` and `fr` bundles but **no `fr_CA`**, so the registry carries a `uioLocale` field mapping `fr-ca → fr`.
- **Self-voicing is not in `fluid.uiOptions`' default preference list** — the defaults are textSize, lineSpace, textFont, contrast, tableOfContents, enhanceInputs. `fluid.prefs.speak` has to be requested explicitly, and is.
- Speech synthesis gets the page's BCP 47 tag (`fr-CA`), not the message-bundle locale (`fr`), distributed onto `fluid.textToSpeech`'s `utteranceOpts.lang`.
- The fixed nav offsets itself from `--a11y-panel-h`, published by a `ResizeObserver` on the panel — no dependency on Infusion's own classes or open/close events.
- The toggle renders in **both** `nav__actions` and `nav__mobile`; the first pass put it only in the former, which `home.css:531` hides on phones — the same trap the language switcher had.
- `privacy` gained an accessibility-cookie section in both locales.

**Verified working in a browser (Brave and Firefox).** The panel opens, closes, and applies text size, fonts, contrast, line spacing and table of contents in both locales. Getting there took five real bugs, none of which source-reading alone would have found:

1. **The separated panel does not render its own scaffold.** It looks for `.flc-slidingPanel-panel` *inside* the container and fails construction if absent — `SeparatedPanelPrefsEditor.html` is only the inner form. The outer markup (two panel bars, Show/Hide, Reset, the empty panel div) has to be in the page. It is not in the npm package because demos are excluded; it came from `demos/uiOptions/index.html`. That demo also confirmed the `auxiliarySchema` and `tocTemplate`/`tocMessage` overrides were already correct.
2. **Fonts 404'd.** The stylesheets reference `../../../lib/<pkg>/fonts/…`, which from `/assets/vendor/infusion/css/` resolves to `/assets/lib/…`. The four font packages are now published there.
3. **`framework/core/css/fluid.css` was missing.** Found by diffing against the working reference implementation at idrc.ocadu.ca, which loads it alongside the three preferences stylesheets.
4. **The panel rendered underneath the fixed nav.** It sat in normal flow with no stacking context while `.nav` is `position: fixed; z-index: 1000`, so clicks on Show/Hide were landing on the nav. Now `position: relative; z-index: 1100`.
5. **Self-voicing wedges the whole editor — disabled.** See below.

**Self-voicing is off.** Enabling `fluid.prefs.speak` from the panel stops the editor responding entirely, in both Brave and Firefox. It is a trap rather than a plain bug: the setting persists in Infusion's preferences cookie, so the next page load re-enacts it and breaks the panel again before the reader can switch it off — recovery meant clearing cookies by hand. Leaving the preference out of the list means the enactor is never constructed, so a `speak: true` already stored in a reader's cookie is inert, which releases anyone stuck.

Two contributing factors were found, neither a complete explanation: `fluid.textToSpeech.isSupported()` only checks that `window.speechSynthesis` exists, never that a voice is available, and nothing in the preferences framework gates on it — which explains Brave, whose fingerprinting shield leaves the API present but returns no voices. It also fails in Firefox, where voices are present, so that is not the root cause. The reference implementation omits this preference too. The flag `ENABLE_SELF_VOICING` in `src/js/a11y.js` re-enables it for investigation.

**Also learned:** self-voicing would need no language wiring. `Orator.js:1011` reads the language from the nearest `[lang]` attribute, and `base.njk` already sets `<html lang>` from the locale registry — so French pages would voice as French for free.

**My own design error, worth recording:** the ☉ launcher initially also drove open/close, giving two state paths over one jQuery animation. `showPanel`/`hidePanel` are model changes and `refreshView` runs the animation off them, so an interrupted animation left the DOM and model disagreeing. It is now purely a launcher — it loads Infusion, opens the panel once, and hides itself, leaving Infusion's own Show/Hide as the single owner.

Still outstanding: a real performance measurement, and restyling/repositioning the launcher.

#### Original notes for this phase

Custom Infusion build (UIO + TTS only); `clamp()` rework across 30 declarations; panel mount with fixed-nav z-index and offset handling; message bundles wired to `_fr` / `_en_CA`; self-voicing `lang` fed from the locale registry with voice-availability detection and the `voiceschanged` handler; privacy policy line; performance measurement against the pre-Infusion baseline.

### Phase 9 — SAT `eleventy-transmog` vector *(separate track, blocked)*

Blocked on ADR-010 identity infrastructure landing in SAT. Needs no site-side changes if the §6 front-matter contract is agreed now.

---

## 8. Effort summary

| Phase | Work | Estimate |
|---|---|---|
| 1 | Foundation and config | 0.5 d |
| 2 | Templating extraction | 2–3 d |
| 3 | String extraction | 1–2 d |
| 4 | Blog i18n + work index | 1 d |
| 5 | Routing, redirects, SEO | 0.5 d |
| 6 | Any-language readiness | 1 d |
| 7 | French integration and QA | 0.5 d |
| | **Multilingual subtotal** | **~7–9 days** |
| 8 | Infusion accessibility bar | 2.5–3.5 d |
| | **Site total** | **~9.5–12.5 days** |
| 9 | SAT Eleventy vector | separate track, blocked |

Excludes French translation production. Phases 1–3 are sequential; 4–6 can overlap; 8 depends on 6 for the `clamp()` and pseudo-locale work.

---

## 9. Open questions

1. **Presentation metadata in SAT** (§6) — `featured`, `readtime`, and `draft` have no Dublin Core equivalent, and ADR-012 keeps presentation concerns out of the archive. Recommend the Eleventy frontmatter spec supplies defaults and the site treats them as optional. Confirm before the spec is written.
2. **Content ownership between Sveltia and SAT** (§6) — decide before both write to `src/content/blog/`, or client edits get silently overwritten.
3. **Localized route slugs** — §3 proposes `a-propos` and `audit-gratuit`. Worth a marketing decision, not just a technical one, since these become the public French URLs.
