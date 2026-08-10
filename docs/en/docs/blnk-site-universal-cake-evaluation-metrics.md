# BLNK Studio Site: Universal Cake Evaluation

Version: 0.1.0
Status: Draft
Style Guide: apa7-markdown-authoring

## Abstract

This document evaluates the BLNK Studio website against the Universal Cake Evaluation Metrics v0.3.1. The site is an Eleventy-generated static site published on Netlify, bilingual in `en-CA` and `fr-CA`, carrying a Fluid Infusion accessibility panel. It rates Strong on content endurance, exit and portability, compatibility, and interaction patterns, and Weak on environment. The dominant finding is that the site's own code is 20 KB gzipped while a first visit to the home page transfers roughly 815 KB, because images and third-party webfonts account for 97.5 per cent of the payload. Two gates require attention before the site could move past assess: webfonts served from a third party expose every visitor's address with no opt-out, and the repository carries no licence file. Three accessibility defects are recorded, one of which is a WCAG failure. All measurements were taken on 7 August 2026 against the local production build.

## Sources and Acknowledgements

The evaluation framework is <a name="apa-uc-metrics-citation"></a>[Steel (2026)](#apa-uc-metrics-reference), applied at version 0.3.1 without modification. Accessibility conformance is assessed against <a name="apa-wcag-citation"></a>[W3C (2023)](#apa-wcag-reference). Energy figures are derived using the model published by <a name="apa-swd-citation"></a>[Sustainable Web Design (2024)](#apa-swd-reference) and are marked Inferred throughout, since no direct power measurement was taken. Licence terms for the two runtime dependencies are read from their published package metadata: <a name="apa-eleventy-citation"></a>[Eleventy (2026)](#apa-eleventy-reference) and <a name="apa-infusion-citation"></a>[Fluid Project (2026)](#apa-infusion-reference). Cache partitioning behaviour, which bears on the webfont finding, follows <a name="apa-chrome-cache-citation"></a>[Chrome Developers (2020)](#apa-chrome-cache-reference).

## 1. Scope and method

### 1.1 What was evaluated

The subject is the BLNK Studio marketing site as built from the repository at commit depth 27, comprising seven page templates rendered into two locales, eleven blog posts, a Sveltia CMS dashboard, and a Fluid Infusion preferences panel. The evaluation covers the site as a product delivered to visitors, and the repository as a product delivered to whoever maintains it next.

### 1.2 Method

All figures were measured against `_site/`, the production build, on 7 August 2026. Transfer weights were taken as gzipped bytes for text assets and actual file bytes for images, since images are already compressed. Webfont weight was measured by fetching the Google Fonts stylesheet with a desktop user agent, extracting the `latin` subset declarations, and downloading each file. Ratings carry evidence tags per the framework: Verified where measured directly, Inferred where reasoned from architecture, Claimed where asserted but unchecked.

**Limitation.** No browser-based audit was run. Assistive-technology behaviour is assessed from markup inspection rather than from screen-reader testing, so accessibility ratings below the gate level carry Inferred rather than Verified tags where they depend on runtime behaviour.

## 2. Gates

The framework treats four criteria as gates. A failed gate cannot be offset by strength elsewhere.

| Gate | Result | Basis |
|------|--------|-------|
| Telemetry or content exposure that cannot be disabled | **At risk** | No first-party telemetry, but third-party webfonts expose every visitor to Google with no opt-out |
| Licence incompatible with the project | **At risk** | Dependencies are compatible; the repository itself declares no licence |
| Accessibility floor, content unreachable via assistive technology | **Pass** | Content is reachable; three defects recorded that fall short of the floor |
| No exit, data cannot be extracted in usable form | **Pass** | Content is Markdown and JSON in Git |

### 2.1 Telemetry and third-party exposure

No analytics, tag manager, or tracking pixel is present. A search for `gtag`, `googletagmanager`, `analytics`, `hotjar`, `mixpanel`, `plausible`, `segment` and `facebook` across the built output returned only false positives: `Symbol.toStringTag` inside Infusion's minified bundle, and the word "analytics" inside the site's own privacy copy. That part is clean and Verified.

The exposure is webfonts. Every page loads three families from `fonts.googleapis.com` and `fonts.gstatic.com`, which transmits the visitor's IP address and user agent to a third party on every first visit, with no mechanism for the visitor to decline. Under a strict reading of the gate this is content exposure that cannot be disabled.

This is recorded as **at risk** rather than failed because the exposure is a delivery choice rather than instrumentation, and because the remedy is well understood and already documented for this codebase: self-host the font files. The site already self-hosts four typefaces for the accessibility panel under `/assets/lib/`, so the pattern exists in the repository. Resolving this would also remove the 393 KB third-party transfer discussed in section 6.

### 2.2 Licence

The two runtime dependencies are compatibly licensed: Eleventy under MIT <a name="apa-eleventy-citation-2"></a>([Eleventy, 2026](#apa-eleventy-reference)) and Infusion under BSD-3-Clause or ECL-2.0 <a name="apa-infusion-citation-2"></a>([Fluid Project, 2026](#apa-infusion-reference)). Neither constrains a commercial site.

The repository contains no `LICENSE` file. For a client site this is a live question rather than an oversight to wave through: it leaves ownership of the template code, the content, and the translations unstated at exactly the point where a studio hands work to a client. Recorded as at risk pending a decision, not as a failure.

## 3. Inclusive

### 3.1 Accessibility, alternative methods of interacting with content

**Rating: Strong. Evidence: Verified.**

The site carries a Fluid Infusion preferences panel offering reader-controlled text size, line spacing, typeface, contrast theme, table of contents, and input enhancement. This is materially more than assistive-technology tolerance; it is reader-adjustable presentation built into the page.

Measured markup facts across the full build:

- 103 `img` elements, **0 without an `alt` attribute**; 12 carry `alt=""`, correct for decorative images
- Contact form: 6 visible fields, 6 `label` elements, 6 `aria-label` attributes
- Single `h1` per page with a coherent `h2`/`h3` structure
- `lang` and `dir` set from the locale registry; 9 elements carry `lang` on the home page, including per-language markup on the language switcher so a screen reader changes pronunciation mid-page
- Reciprocal `hreflang` across 16 pages

The fluid type scale multiplies its viewport term by `--fl-textSize-factor`, so the reader's text-size choice scales headings proportionally rather than leaving them near-static while body copy grows. Directional CSS was converted to logical properties, which is what makes a right-to-left language a configuration change rather than a rewrite.

**Three defects are recorded.**

First, and the most serious: **form validation communicates errors by border colour alone.** The handler sets `el.style.borderColor` with no accompanying text, no `aria-invalid`, no `role="alert"`, and no `aria-live` region. A screen-reader user receives no indication that submission failed or which field is at fault, and a user who cannot distinguish the red border receives none either. This fails WCAG 2.2 success criteria 1.4.1 Use of Color and 3.3.1 Error Identification <a name="apa-wcag-citation-2"></a>([W3C, 2023](#apa-wcag-reference)).

Second, there is **no skip link**. Every page places the navigation before the main content, so a keyboard or screen-reader user traverses the full navigation on every page. This fails WCAG 2.4.1 Bypass Blocks.

Third, **images carry no `width` and `height` attributes** (0 of 103), so the page reflows as images load. This is a stability rather than a reachability problem, but it disproportionately affects readers using magnification.

None of these makes content unreachable, so the accessibility gate passes. All three are cheap to fix and should be, particularly the first.

### 3.2 Multilingual integration

**Rating: Strong. Evidence: Verified.**

The site ships `en-CA` and `fr-CA` at full parity: 579 string keys, both locales complete, with a build guard that fails a production build when a locale is missing keys the default has. Route slugs are localised, so the French site reads `/fr-ca/a-propos/` rather than a translated page on an English URL.

On the framework's specific question — whether adding a language is a data file anyone can supply or a code change only maintainers can make — this rates Strong. A new language requires one entry in `src/_data/locales.js` and one JSON file in `src/_locales/`. No template, stylesheet, or build change is needed. Blog posts pair across languages by a shared `sat:work` identifier rather than by matching filenames, so translations may carry their own slugs.

**Named limitation.** The French bundle is machine-drafted and carries a `_draft` marker; every build prints a warning that it has not been reviewed by a translator. It is complete but not verified copy, and should not be treated as shipped French.

### 3.3 Economic accessibility

**Rating: Moderate. Evidence: Verified.**

The site is free to read, requires no account, and its own code is very light: 20 KB gzipped for HTML, CSS and JavaScript on the home page. On old or low-end hardware it is static HTML with no framework runtime, which is close to a best case.

The limitation is bandwidth, and it is significant. A first visit to the home page transfers approximately **815 KB**, of which 402 KB is images and 393 KB is webfonts. On a metered or intermittent connection that is a meaningful cost for a marketing page, and it is not the site's own code that causes it. Detailed in section 6.

### 3.4 Cognitive accessibility

**Rating: Moderate. Evidence: Inferred.**

Copy is direct and largely free of jargon, page structure is conventional, and the forms are short with plain labels. Navigation is consistent across pages.

Against this: the form error behaviour described in section 3.1 is the opposite of forgiving. It fails without explaining, which is precisely the pattern the framework's "forgiving of errors, and does it explain them without blame" question is aimed at. Rated Moderate rather than Strong on that basis, and Inferred because no reading-level measurement or user testing was performed.

### 3.5 Representation

**Rating: Unknown.**

No public information establishes whether disabled people are represented on the team or its advisory structure, or whether user research with affected communities is compensated and ongoing. Per the framework's instruction, the absence of this from public documentation is itself recorded as a data point.

One observation cuts in a positive direction without resolving the question: the site carries a reader-controlled accessibility panel, which is uncommon on a studio marketing site and suggests the concern is at least present in the design process.

### 3.6 Compatibility

**Rating: Strong. Evidence: Verified.**

The deliverable is static HTML, CSS and a small amount of vanilla JavaScript, with no framework runtime and no build-time browser targeting. It renders on any browser supporting `clamp()` and CSS custom properties, which is universal among browsers still receiving security updates. There is no dependence on a specific operating system, input device, or output device. The accessibility panel requires JavaScript, but the site's content does not.

### 3.7 Resilience

**Rating: Moderate. Evidence: Verified.**

The built artifact is self-contained HTML with no licence server, no expiring token, and no API dependency. If the build tooling vanished tomorrow, `_site/` would continue to serve indefinitely from any static host. That is a strong position.

Two limitations prevent a Strong rating. Webfonts are fetched live from a third party, so a Google Fonts outage or a network-level block degrades typography on every page. And there is no service worker or offline provision, so the site does not function offline once loaded beyond whatever the browser cache retains incidentally.

## 4. Agency

### 4.1 Sovereignty and privacy

**Rating: Moderate. Evidence: Verified.** The owner and user answers diverge, and the framework asks that both be recorded.

**Owner: Strong.** Content is Markdown, configuration is JSON and JavaScript, and everything lives in Git. The build is Eleventy under MIT. Nothing prevents self-hosting, modifying, forking, or redistributing. Netlify can be replaced by any static host without changing a file, since the build output is plain HTML.

**User: Moderate.** Three third parties are involved in a visitor's interaction, and the visitor can decline none of them:

- **Google** receives the visitor's IP address and user agent on every first page load, via the webfont request
- **Netlify** receives and stores every contact and audit form submission; the site holds no copy, and there is no stated retention period
- **GitHub** holds the content repository and authenticates CMS editors

The privacy policy discloses the accessibility preferences cookie accurately, including that it is functional rather than analytic. It does not mention the webfont request or name Netlify as the processor of form submissions. That is a disclosure gap rather than a misstatement.

### 4.2 Power-imbalance proxies, vendor to user

**Rating: Strong. Evidence: Verified.** The framework's reversibility question — what it would cost the weaker party to walk away — is answered unusually well here.

| Proxy | Finding |
|-------|---------|
| Exit cost | Low. Content is 11 Markdown files and 2 JSON files in Git. Migrating to another static generator is hours, not weeks, and no data is held by a vendor |
| Data portability, machine-readable | Yes. Markdown with YAML front matter and plain JSON, both parseable without reverse-engineering |
| Data portability, human-readable | Yes. Both formats open in any text editor and read as prose |
| Terms-of-service volatility | Not applicable to the site itself. Applies to Netlify and GitHub as platforms, assessed in section 8.1 |
| Pricing asymmetry | Not applicable. The site charges visitors nothing and gates nothing |

The one asymmetry worth naming: form submissions rest with Netlify, and a visitor who has sent a project brief has no mechanism to retrieve or delete it other than asking. That is a small surface, but it is the one place where the user's exit cost is not zero.

### 4.3 Interaction patterns

**Rating: Strong. Evidence: Verified.** Assessed row by row against the framework's table.

| Pattern | Finding |
|---------|---------|
| Honest defaults | Pass. No pre-selected upsell; form defaults are empty or neutral |
| Easy exit | Pass. Nothing to cancel; no account, no subscription |
| Forgiveness | Partial. No destructive actions exist, but form errors are not explained (section 3.1) |
| Natural stopping points | Pass. No infinite scroll, no autoplay, no chained content |
| Quiet by default | Pass. No notifications, no modals, no interstitials, no exit-intent popup |
| Plain asking | Pass. The newsletter form states what it is; declining is simply not filling it in |
| Visible costs | Pass. Service packages state what they include; the free audit states its limit of ten per week before asking |
| Leaves you whole | Pass. Nothing is retained from the visitor that they would need back |

The framework offers a worked positive anchor: "an accessibility bar that lets a visitor make a page readable, saves the choice locally, and gets out of the way." The site implements precisely that. Preferences save to a local cookie, apply on return, and the panel closes without re-engaging.

One deliberate design decision aligns with this section and is worth recording: the language switcher does not auto-redirect based on browser language, and does not persist a language preference that would override an explicitly requested URL. A reader who follows an English link receives the English page.

## 5. Security

**Rating: Moderate. Evidence: Verified for surface, Inferred for practice.**

**Data collected and where it rests.** Contact and audit form submissions rest with Netlify. A functional cookie holding accessibility preferences rests on the visitor's device. No other collection was found.

**Supply chain.** Two declared dependencies — Eleventy as a development dependency and Infusion as a runtime dependency — resolving to 175 packages in total. Infusion is vendored as a prebuilt bundle served from `/assets/vendor/`, so its runtime code is pinned to a reviewed artifact rather than resolved at request time. No install scripts execute arbitrary code.

**Attack surface.** Static HTML with no server-side execution, no database, and no authenticated user area. The surface is close to minimal. The exception is the Sveltia CMS dashboard at `/admin/`, which authenticates against GitHub; it is excluded from the sitemap and disallowed in `robots.txt`, but it is publicly reachable and its security rests on GitHub's OAuth.

**Vulnerability reporting.** No `SECURITY.md` exists and no reporting route is published. Rated as a gap. For a marketing site the consequence is limited, but the framework asks the question of the artifact, and the answer is that a finder has nowhere to report.

**Assessment method.** Static inspection of the built output and dependency tree on 7 August 2026 using grep and `npm ls`. No network monitoring, no dependency CVE scan, and no penetration testing were performed, so patch responsiveness is Unknown rather than rated.

## 6. Sustainability and environment

**Rating: Weak. Evidence: Verified for transfer, Inferred for energy.**

This is the site's weakest pillar, and the cause is specific rather than diffuse.

### 6.1 Measured transfer weight

First-visit transfer per page, gzipped for text and actual bytes for images.

| Page | HTML | CSS + JS | Images | Fonts | Total |
|------|-----:|---------:|-------:|------:|------:|
| Home | 5 KB | 15 KB | 402 KB | 393 KB | **815 KB** |
| About | 4 KB | 16 KB | 204 KB | 393 KB | 617 KB |
| Blog index | 4 KB | 16 KB | 228 KB | 393 KB | 641 KB |
| Services | 7 KB | 17 KB | 94 KB | 393 KB | 511 KB |
| Contact | 4 KB | 16 KB | 94 KB | 393 KB | 507 KB |

**The site's own code is 20 KB. Images and webfonts are 795 KB, or 97.5 per cent of a first visit to the home page.**

### 6.2 Where the weight is

**Webfonts, 393 KB.** The stylesheet request asks for ten weights across three families. A Latin-script visitor downloads ten `woff2` files averaging 39 KB each. This is measured, not estimated. Two levers apply: request only the weights the stylesheets actually use, and self-host so the transfer is first-party and cacheable under the site's own origin. Modern browsers partition the HTTP cache by site <a name="apa-chrome-cache-citation-2"></a>([Chrome Developers, 2020](#apa-chrome-cache-reference)), so the historical argument that a visitor arrives with Google's fonts already cached no longer holds.

**Images, 94–402 KB per page.** All 16 images are JPEG or PNG. There is no WebP or AVIF, no `srcset`, and no `loading="lazy"` on any of the 103 `img` elements. A phone downloads the same bytes as a desktop, and every image on a page downloads whether or not it is ever scrolled into view.

**A 1.1 MB stray file ships to production.** `src/assets/uploads/kyojuro-rengoku-4k-wallpaper--24373.jpg` is an anime wallpaper unrelated to the site, committed to the repository and published in the build output. It is not referenced by any page, so it costs no visitor bandwidth, but it is 19 per cent of the deployed site by size and should be deleted.

### 6.3 Energy

**Evidence: Inferred.** Applying the Sustainable Web Design model <a name="apa-swd-citation-2"></a>([Sustainable Web Design, 2024](#apa-swd-reference)) to the measured 815 KB first-visit home page places it above the median for a marketing page, driven entirely by images and fonts rather than by computation. No direct power measurement was taken, so this is a derived figure and is not rated as though measured.

The structural picture is better than the transfer figure suggests. A static site performs no server-side rendering per request, so the provider-side energy per visit is a file read. There is no database, no application server, and no build work at request time. Repeat visits transfer 15 KB of cacheable CSS and JavaScript. Fixing the images and fonts would move this pillar from Weak to Strong without touching the architecture.

### 6.4 Hardware

No hardware upgrade is implied for visitors, the owner, or the host. The site runs on any device with a current browser, and the build runs on any machine with Node.

## 7. The product or service itself

### 7.1 Longevity

**Rating: Moderate. Evidence: Verified.**

Eleventy is mature, MIT-licensed, and widely used, with no vendor dependency. The critical property is that its output is plain HTML: if Eleventy were abandoned tomorrow, the built site would continue to serve, and the Markdown sources would remain usable by any successor generator.

Against this, the project itself is young at 27 commits with a single primary contributor, and the accessibility panel introduces a dependency on Fluid Infusion, a smaller project than Eleventy with a narrower contributor pool. That dependency is lazily loaded and non-essential to content, so its failure mode is graceful.

### 7.2 Content endurance

**Rating: Strong. Evidence: Verified.**

Content is Markdown with YAML front matter, authored outside the tool and merely rendered by it. In the framework's terms this is an enhancement layer rather than a container: removing Eleventy leaves the content whole. Blog posts carry `sat:work` identifiers, so translation relationships survive migration rather than depending on the generator's conventions.

### 7.3 Exit and portability

**Rating: Strong. Evidence: Verified. Gate: Pass.**

Every artifact is an open format in a Git repository: Markdown for posts, JSON for interface strings, CSS and JavaScript as plain text. There is no proprietary format anywhere in the content path and no database to export. A realistic migration to Hugo, Astro or Jekyll would be a template rewrite with the content carried across untouched.

### 7.4 Adjustability and support

**Rating: Strong. Evidence: Verified.**

The fork-and-fix path is fully open. Source is readable and commented, with the non-obvious decisions explained in place — why the date filter pins a time zone, why two `left` properties stay physical, why the work index reads front matter rather than a collection. A migration plan and a colours-and-fonts guide accompany the repository. A competent front-end developer could take this over without consulting the original author.

### 7.5 Market position

**Rating: Moderate. Evidence: Inferred.**

The site itself is not a platform and holds no market position. The proxies apply to the infrastructure it rests on.

| Proxy | Finding |
|-------|---------|
| Market concentration | Netlify is one of several comparable static hosts; GitHub is dominant in code hosting; Google Fonts is dominant in webfont delivery |
| Take rate | None. No transactions flow through any platform |
| API stability | Netlify's build contract is a shell command and an output directory, among the most stable interfaces available. Netlify Forms is proprietary and is the one lock-in point |
| Forkability | High. The repository is self-contained; hosting is replaceable without file changes |
| Contributor concentration | High, effectively single-author. This is the honest number the framework asks for, and it is a bus-factor risk |

The concentration risk is real but shallow: replacing Netlify means moving a build command, and replacing Google Fonts means self-hosting files already documented. Netlify Forms is the only component whose replacement would require a code change.

## 8. Scorecard

| Metric area | Rating | Evidence | Notes |
|-------------|--------|----------|-------|
| Accessibility, alternative interaction | Strong | Verified | Infusion panel; 103/103 images with `alt`; 6/6 fields labelled. Three defects, one a WCAG failure |
| Multilingual integration | Strong | Verified | 579 keys, both locales complete, new language is one data file. French is machine-drafted |
| Economic and cognitive accessibility | Moderate | Verified | 20 KB own code; 815 KB first visit. Form errors not explained |
| Representation | Unknown | — | No public information; absence recorded as a data point |
| Compatibility | Strong | Verified | Static HTML, no framework runtime, no device assumptions |
| Resilience | Moderate | Verified | Self-contained build; live third-party font dependency; no offline support |
| Agency, sovereignty and privacy | Moderate | Verified | Owner Strong, user Moderate. Three third parties the visitor cannot decline |
| Agency, power-imbalance proxies | Strong | Verified | Exit cost low; portability both machine- and human-readable |
| Agency, interaction patterns | Strong | Verified | Eight of eight rows pass; forgiveness partial |
| Environment, direct and indirect | Weak | Verified transfer, Inferred energy | 97.5% of payload is images and fonts; no WebP, `srcset` or lazy loading; 1.1 MB stray file |
| Security | Moderate | Verified surface | Minimal attack surface; 175 packages; no `SECURITY.md`; patch responsiveness Unknown |
| Longevity | Moderate | Verified | Eleventy mature and MIT; project young, single contributor |
| Content endurance | Strong | Verified | Markdown enhanced, not contained |
| Exit and portability | Strong | Verified | Open formats throughout; no database |
| Adjustability and support | Strong | Verified | Open licence path, documented, readable |
| Market position | Moderate | Inferred | Replaceable infrastructure; Netlify Forms the one lock-in |
| Gates | **2 at risk** | Verified | Third-party font exposure with no opt-out; no repository licence |

## 9. Recommendations in priority order

1. **Fix form error handling.** Add a text message, `aria-invalid`, and an `aria-live` region. This is the only WCAG failure found and it affects the site's primary conversion path.
2. **Self-host the webfonts.** Removes 393 KB of third-party transfer, resolves the exposure gate, and removes a live third-party dependency from every page load. The procedure is documented in the colours-and-fonts guide.
3. **Optimise images.** Convert to WebP or AVIF, add `srcset`, add `loading="lazy"`, add `width` and `height`. This addresses the Environment rating and the layout-stability defect together.
4. **Delete the stray upload.** `kyojuro-rengoku-4k-wallpaper--24373.jpg` is 19 per cent of the deployed site and belongs to nothing.
5. **Add a skip link.** One element, resolves WCAG 2.4.1.
6. **Add a licence file.** Decide and record who owns the template, the content, and the translations.
7. **Trim the font weight request** from ten weights to those actually used.
8. **Disclose the webfont request and name Netlify** as form processor in the privacy policy.
9. **Add a `SECURITY.md`** with a reporting route.
10. **Commission a translator review** of the French bundle and remove the `_draft` marker.

Items 2, 3, 4 and 7 together would move Environment from Weak to Strong and cut a first visit from roughly 815 KB to well under 200 KB.

## Resources

### Evaluation framework
- [Universal Cake Evaluation Metrics v0.3.1](#apa-uc-metrics-reference)

### Accessibility standards
- [W3C Web Content Accessibility Guidelines 2.2](#apa-wcag-reference)

### Sustainability
- [Sustainable Web Design Model](#apa-swd-reference)

### Dependencies and platform behaviour
- [Eleventy](#apa-eleventy-reference)
- [Fluid Project Infusion](#apa-infusion-reference)
- [Chrome Developers on HTTP cache partitioning](#apa-chrome-cache-reference)

## References

<a name="apa-chrome-cache-reference"></a>Chrome Developers. (2020). *Gaining security and privacy by partitioning the cache*. Google LLC. https://developer.chrome.com/blog/http-cache-partitioning/
[Return to citation](#apa-chrome-cache-citation)

<a name="apa-eleventy-reference"></a>Eleventy. (2026). *Eleventy, a simpler static site generator*. https://www.11ty.dev
[Return to citation](#apa-eleventy-citation)

<a name="apa-infusion-reference"></a>Fluid Project. (2026). *Infusion documentation: Preferences framework*. Inclusive Design Research Centre, OCAD University. https://docs.fluidproject.org/infusion/development/
[Return to citation](#apa-infusion-citation)

<a name="apa-uc-metrics-reference"></a>Steel, C. (2026). *Universal Cake evaluation metrics* (Version 0.3.1). UniversalCake.
[Return to citation](#apa-uc-metrics-citation)

<a name="apa-swd-reference"></a>Sustainable Web Design. (2024). *Estimating digital emissions*. https://sustainablewebdesign.org/estimating-digital-emissions/
[Return to citation](#apa-swd-citation)

<a name="apa-wcag-reference"></a>W3C. (2023). *Web Content Accessibility Guidelines (WCAG) 2.2*. World Wide Web Consortium. https://www.w3.org/TR/WCAG22/
[Return to citation](#apa-wcag-citation)

## Changelog

| Version | Status | Notes |
|---------|--------|-------|
| 0.1.0 | Draft | Initial evaluation against Universal Cake Evaluation Metrics v0.3.1; measurements taken 7 August 2026 against the local production build |
