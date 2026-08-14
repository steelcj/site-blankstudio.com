---
dc:title: "ADR: Fact and Expression, the Locale Scope of Configuration and Accessibility Variables"
dcterms:version: "0.1.0"
dc:creator: "Christopher Steel"
dc:contributor: "Claude (Anthropic)"
dc:subject:
  - "architecture-decision-record"
  - "i18n"
  - "accessibility"
  - "multilingual"
  - "configuration"
  - "sat"
  - "dublin-core"
dc:description: >
  Proposes a naming, and a placement rule, for every variable this site
  generator resolves: a language-invariant fact and its per-locale expression
  are never the same storage location, and any variable an assistive
  technology speaks or a translator must review is always an expression, even
  when the fact behind it is a name. Models the rule on SAT's own work and
  expression identity split, and audits the site's current variables against
  it.
dc:publisher: "UniversalCake"
dcterms:created: "2026-08-14"
dcterms:modified: "2026-08-14"
dc:format: "text/markdown"
dc:language: "en"
sat:language_bcp47: "en"
dc:identifier: "adr--fact-and-expression-locale-scope-of-variables"
dcterms:rightsHolder: "Christopher Steel"
dc:rights: >
  Copyright 2026 Christopher Steel / UniversalCake.
  SPDX-License-Identifier: AGPL-3.0-or-later
sat:uuid: ""
sat:version_at_creation: ""
sat:migration_status: pre-sat
sat:changelog:
  - version: "0.1.0"
    date: "2026-08-14"
    author: "Christopher Steel"
    notes: >
      Initial draft. Names the fact/expression split already used ad hoc for
      the logo alt text, generalizes it from SAT's work/expression identity
      (ADR-010) and its archive-purity rule (ADR-012), and audits the site's
      current variable categories (brand tokens, verbal identity, accessible
      names, route slugs, chrome strings, content) against the rule. Raised
      by the user after reviewing 2026-08-13-132625-summary.md, who noted that
      "one variable, one file, one output" is a DRY habit, not a principle
      that accounts for accessibility text being inherently language-bound.
---

# ADR: Fact and Expression, the Locale Scope of Configuration and Accessibility Variables

Version: 0.1.0
Status: Draft, proposed
Style Guide: style-guide--plain-language-for-general-audiences

## Abstract

This document proposes a single organizing rule for where a variable lives in this site generator, and applies it to every category of variable currently in use: brand colors, fonts, the client's name and slogan, the text a screen reader speaks for a logo, route slugs, chrome strings, and page content. The rule has two parts. First, separate a language-invariant fact from its per-locale expression, and never store them in the same place. Second, treat anything an assistive technology speaks, or a translator must review, as an expression, even when the underlying fact is a proper noun that reads the same in every language. The second part is the one this document argues for explicitly, because it is easy to mistake a name for something locale-free when it is really a fact that has not yet been rendered into a language.

## Context

An earlier review, 2026-08-13-132625-summary.md, found a screen reader announcing a client's old name because the correct string lived in one variable and a stale duplicate lived in another, and only the duplicate was ever spoken. The fix that shipped, visible today in `src/_includes/partials/nav.njk` and `branding/_template/site.yaml`, works: `site.yaml` holds the client's name as one fact, `src/_locales/<code>.json` holds a `logoHome` pattern per language (`"{name} home"` in English, `"Accueil {name}"` in French), and the template joins them at render with a `{name}` substitution, the same mechanism `final-cta.njk` already used for `{phone}`.

 `branding/_template/assets/README.md` now documents the result for the next client: "Set `name` in `site.yaml` and the logo is named in every language."

When that fix was framed as "one variable, one file, one output," the user pushed back: that framing is a DRY habit inherited from ordinary software configuration management, and it is not wrong, but it treats the underlying question, which value belongs in which file, as settled by convenience rather than by what a variable actually is.

The user's proposed reframing is that all accessibility information is human-language specific, full stop, and that a variable's locale scope, not its file-tidiness, should be the first axis the config system organizes around. Some variables are fixed across every language this site ever ships (a color, a UUID). Others are language variables and belong in a language root. The fix above already does this correctly for the logo, but arrived at the pattern by hand, once, for one bug, rather than by naming the rule and checking every other variable category against it.

## Vocabulary: how a value relates to language

This document's first draft proposed a fact/expression binary, then, in review, that binary did not survive: it claimed some values have "no relationship to language at all," which does not hold up (a hex code is base-16 notation, a UUID's hyphens are a formatting convention, both human-made), and it treated every proper noun as automatically fixed, which "Palmolive" versus "Brajesh"/"Vrajesh" shows is not so. The terms that replaced it, and the test that tells them apart, are defined in their own document, `vocabulary--value-language-relationships`, split out because the terms are reusable beyond the placement question this ADR asks of them, the same relationship this project's `vocabulary--multilingual-content-structure` has to `spec--content-format-for-the-publishing-vector`.

In brief, four value relationships, distinguished by one test, whether a correct alternate value exists for the same referent and what governs the choice among alternates if so, plus a fifth term for a different kind of thing entirely:

- **Fixed**, no correct alternate exists, the value constitutes the referent. A hex color, a UUID, a phone number's digits.
- **Locked**, a correct alternate exists but an owner has chosen to decline it, using one value everywhere. "Palmolive"; `site.yaml`'s `name` and `tagline` when authored as one string.
- **Transliterated**, the referent stays fixed but the written form legitimately varies by script or convention. "Brajesh" / "Vrajesh" for one Devanagari name.
- **Translated**, meaning is what must survive; wording is expected to differ by locale. `tagline` and `description` when authored as a locale map; the chrome strings in `src/_locales/<code>.json`.
- **Pattern**, not a fifth answer to the test above, a frame that positions one of the four inside locale-specific word order, independent of what fills it. `logoHome`'s `"{name} home"` / `"Accueil {name}"`; `final-cta.njk`'s `{phone}`.

The Decision and Audit sections below were written against the earlier fact/expression binary and are marked provisional until they have been checked against these five terms; they are kept rather than deleted because most of their conclusions still hold, they just need re-deriving.

## The precedent: SAT already draws this line for content

This is not a new idea for this codebase. `docs/en/docs/reference/vocabulary--multilingual-content-structure-v0-1-0.md` and `docs/en/docs/reference/spec--content-format-for-the-publishing-vector-v0-1-0.md` describe the identical split for page content, inherited from Source Archive Tools, of which this site is a publishing vector.

SAT distinguishes a **work** from its **expressions**. A work, such as "the privacy policy," has one identity, a UUID (`sat:work`), that is shared by every language version and never changes. An expression is one language's rendering of that work, with its own identity (`dc:identifier`), its own path, its own filename. `docs/en/docs/multilingual-plan.md` §6 cites SAT's ADR-010 directly on why: a field like a translation key "belongs to the published output, not to the canonical record." ADR-012 goes further and states that presentation metadata does not belong in the archive at all, only in the vector that publishes it. ADR-001 makes the same point structurally: language archives share no path relationship; `content/en-ca/legal/privacy.md` and `content/fr-ca/mentions-legales/confidentialite.md` are linked only by the shared `sat:work` UUID, resolved through a build-time lookup (`src/_data/contentWorkIndex.js`), never by matching paths or names.

Whether "work" is best modeled as one atomic idea with many renderings, or as a body of related ideas where a translation is better described as one or more interpretations of it than as a mechanical rendering, is a live question this document does not settle, raised as a tentative suggestion rather than pursued here. For an identifier-bearing thing like `sat:work`, one-UUID-many-expressions holds up regardless of the answer, because the build needs a single stable lookup key whether or not the mapping is philosophically clean. For prose content, a translator's work is arguably closer to interpretation than transcription, and modeling it as a rendering of one fixed idea may understate the judgment involved. This document keeps the identifier-level model, since that is what the build machinery actually needs, and carries the interpretation question into Open Questions rather than deciding it.

That lookup-not-fusion pattern is close to what `nav.njk` now does for the logo, just without a name that needs interpretation: `site.name` is (today, as a locked value) resolved once; `t.common.nav.logoHome` is the per-locale pattern; the template performs the lookup and substitution at render, and the two are never pre-merged into a stored string anywhere. What this ADR is working toward is a name for that pattern precise enough to apply on purpose to the next variable, once the vocabulary above has been checked against enough of them to trust it.

## What accessibility text specifically requires

The reason accessibility text cannot be treated as a fact even when it names an invariant thing:

An accessible name is not read in isolation. It is announced inside a sentence a screen reader constructs, "link, BLNK Studio home," and the words around the fact vary by language in ways the fact itself does not predict, word order (`{name} home` versus `Accueil {name}`), the presence or absence of an article, eventually grammatical gender or number agreement once this site ships a language that has them. A name that looks locale-free because its spelling does not change is still consumed inside a locale-bound utterance, so the variable that reaches the assistive technology has to be the resolved expression, not the fact.

This also holds for the parts of a name that never render as visible text. `branding/_template/assets/README.md` states the SVG rule that follows from it: a brand mark may draw a proper noun as a shape, because a name is the same in every language, but it must never draw a slogan that way, because a slogan is a sentence, and a sentence is an expression that has to be re-authored per locale, not redrawn. The file's own `<title>` still needs `xml:lang` on the root, because even a name-only label is being handed to something, a translator, a reader who opens the file directly, that needs to know which language it is written in to do anything correct with it.

The corollary is that a fact is genuinely safe to store once, with no locale scope, only when nothing ever renders it as language for a human. `brand.yaml`'s color tokens qualify: a hex value is consumed by CSS, never spoken, never displayed as text, so it has no expression, only itself. `fonts.yaml`'s family stacks are the same. `site.yaml`'s `url` is closer to the line, since it can appear as visible text, but it is not translated, only displayed identically everywhere, so one value with no locale map is correct. The moment a variable's consumer is a screen reader, a `<title>`, a meta description, or a sentence a translator has to approve, it needs a locale-scoped expression, even if that expression is declared once and shared across every locale on purpose, the way `tagline` in `site.yaml` can be authored as one string precisely because the owner decided this brand's slogan is not to be translated, a decision the file's shape (one string, or a map keyed by locale) exists to make explicit rather than assume.

## Audit: the site's current variable categories against the rule

| Category | Example | Ever rendered as language for a human? | Fact lives in | Expression lives in | Resolved by |
| --- | --- | --- | --- | --- | --- |
| Color tokens | `brand.yaml` hex values | No | `branding/<client>/brand.yaml` | n/a, fact only | `build-brand.py` to `src/css/brand.css` |
| Font stacks | `fonts.yaml` `tokens`/`families` | No, consumed by CSS only | `branding/<client>/fonts.yaml` | n/a, fact only | `build-brand.py`, `fetch-fonts.py` |
| Verbal identity, name | `site.yaml` `name` | Yes, it is language; currently treated as a locked value, one string, no locale map | `branding/<client>/site.yaml` | n/a today; would need the same one-string-or-locale-map shape as `tagline` if a locale required a transliterated rendering, see Open Questions | referenced, never copied, by every consumer below |
| Verbal identity, slogan/description | `site.yaml` `tagline`, `description` | Yes, and the owner chooses per client whether it is translated | `branding/<client>/site.yaml` | same file, one string or a map keyed by locale, an explicit author choice | `build-brand.py` to `src/_data/site.json`, read directly by templates |
| Logo accessible name | header/footer `alt` | Yes, spoken by a screen reader | `site.yaml` `name` | `src/_locales/<code>.json` `common.nav.logoHome` pattern | `nav.njk`/`footer.njk` at render, `{name}` substitution, or `site.yaml` `logos.alt` override when the mark itself is not the client's name |
| Brand SVG accessible name | `<title>` inside a brand asset | Only if the file is opened directly or later inlined, not today via `<img>` | the SVG file itself, one name per file, since it draws a fixed mark | n/a today, `<img>` cannot expose it, so the page's `alt` above is the only expression that reaches a reader | none yet, this is a gap, see Open Questions |
| Brand SVG longer description | `about-work.svg` `<desc>` | Yes, if the file is opened directly | currently one English sentence in the file | none, this is exactly the unresolved defect §4.2 of 2026-08-13-132625-summary.md flagged and moved out of the file's `aria-label`, but not yet into a locale-aware home | none yet, see Open Questions |
| Route slugs | `about` to `about`/`a-propos` | Yes, it is a URL a reader sees and a search engine indexes per language | n/a, slugs have no locale-free fact behind them, "about" and "a-propos" are independent authored choices | `src/_locales/<code>.json` `routes` | `_localeTree.js` `urls` computed key |
| Chrome strings | nav labels, footer copy, aria-labels | Yes | n/a, authored directly per language | `src/_locales/<code>.json`, deep-merged over the default with build-time fallback reporting | `src/_data/i18n.js` |
| Contact facts | email, phone | Yes, displayed, but not translated | `site.yaml` `contact` | same file, one value, correct because a phone number has no language | `build-brand.py` to `site.json`, read directly |
| Locale identity | `htmlLang`, `dir`, `uioLocale` | Consumed by the platform, not spoken itself, but it governs how everything else is spoken | n/a, this is the registry that defines what a locale is | `src/_data/locales.js`, one entry per shipped locale | drives `<html lang dir>`, `hreflang`, Infusion's self-voicing `utteranceOpts.lang`, date formatting |
| Page content | a privacy policy | Yes | n/a above the page level, the work identity (`sat:work`, a UUID) is the closest thing to a locale-free fact, and it identifies the work, not its wording | one Markdown file per locale under `src/content/<locale>/`, an independent expression, mirrored by meaning, not by path | `contentWorkIndex.js`, resolved by `sat:work`, never by path |

The table's two gap rows, the SVG's own `<title>`/`<desc>`, are the concrete case this rule was missing before it had a name. They are addressed as open questions rather than decided here, because closing them is a design choice about how much investment a brand-asset SVG deserves, not a mechanical application of the rule.

## Decision

Provisional, written against the earlier fact/expression binary before the Vocabulary section above replaced it with four value relationships plus the separate pattern term. Kept here as a working draft rather than removed, because the two tests still point the right direction for most of the variables in the audit table, but they need re-deriving against fixed, locked, transliterated, and translated values, and against pattern on its own terms, before this section can be called settled. `decision-tree--value-language-relationships-placement-v0-1-0.md` is that re-derivation, a clickable flowchart asking the three questions the four relationships answer differently and stating where each belongs; it has not yet been merged into or reconciled with the two tests below.

Adopt the fact/expression split as the default rule for every variable this generator resolves, stated as two tests to apply before adding or moving a variable:

1. Does this value ever reach a human as language, spoken or read, including inside an accessible name, a `<title>`, a meta tag, or translated prose? If no, it is a fact, and belongs in the brand or template layer with no locale scope, `brand.yaml`, `fonts.yaml`, or the invariant parts of `site.yaml`.
2. If yes, is the wording, word order, or presence of the value itself something a translator would need to approve separately from the fact it names? If yes, it is an expression, and the fact it depends on must be referenced, never copied, the way `logoHome`'s `{name}` references `site.name`. If the owner has decided a particular expression is not to be translated (a slogan kept identical across locales, for instance), that is still a locale-aware decision, expressed by the one-string-or-locale-map shape already used for `tagline`, `description`, and `logos.alt`, not by placing the string somewhere the locale layer cannot see it.

Nothing here changes today's file layout; `branding/<client>/*.yaml` and `src/_locales/<code>.json` already sit either side of this line for every variable audited above except the two SVG gaps. What changes is that the split is now a named rule to check a new variable against, not a pattern that has to be re-derived from the last incident.

## Consequences

**What this resolves.** The class of bug in 2026-08-13-132625-summary.md, a fact duplicated into an expression's storage location, stops being something a reviewer has to notice by inspection and becomes something a reviewer can check against a named rule: does this new variable's home match what it is, a fact or an expression, and if it is an expression, is its fact referenced or copied.

**What it costs.** Every fact that reaches an accessible surface now needs an author to also confirm its expression pattern renders correctly in every shipped locale, not just supply the fact and assume the join works. Adding a locale is not just adding a bundle, it means checking every `{placeholder}` pattern (`logoHome`, `ctaBtn1Label`'s `{phone}`) against the new language's grammar, since `{name} home` versus `Accueil {name}` is a word-order difference this project has already hit once and a gender-agreement difference it has not hit yet.

**What is deliberately out of scope.** This document does not resolve the two SVG gap rows, does not propose an ICU MessageFormat or similar grammar-aware templating layer (the `{name}`/`{phone}` substitution is adequate for the two locales shipped today and the languages closest to them, but will not survive a language with grammatical gender or plural-dependent word forms without revisiting), and does not touch how SAT itself organizes facts and expressions upstream, only how this publishing vector already mirrors that organization for its own configuration.

## Open questions for the owner

1. `about-work.svg`'s `<desc>` currently holds one English sentence, moved out of `aria-label` by the prior fix but not yet given a locale home, because the file is loaded via `<img>` today and nothing reads its internal text regardless. Decide now, while the fix is cheap, or defer until the file is actually inlined: if a locale-aware description is wanted before then, the two options in `branding/_template/assets/README.md` apply, one file per locale, or inline the SVG and template the text; a third option is to accept that the file's own `<desc>` is unreachable prose maintained for the day it is inlined, and treat the page's own alt text as the only expression that matters until that day.
2. Should brand SVGs that are logos, not illustrations, gain a `<title>` even though nothing reads it today, purely so the file is correct the day it is opened directly or inlined? The asset README already recommends this; this ADR treats it as settled practice, not a new question, unless the owner disagrees.
3. The `{name}`/`{phone}` substitution pattern has no answer for grammatical agreement, gendered articles, or pluralization once a locale that needs them ships. This is not urgent for `en-ca`/`fr-ca`, but the site's stated architecture goal, given at the top of `multilingual-plan.md`, is "support *any* language, including RTL and non-Latin scripts, without a second rebuild," so worth deciding now whether that goal extends to grammatically complex agreement or stops at script direction and translation.
4. SAT's own reconciliation is still open, per the vocabulary document's own changelog: "these are the project's working definitions and should be reconciled with SAT's canonical definitions where they differ." This ADR borrows the work/expression language on the assumption that borrowing holds; if SAT's own ADR-010 is revised upstream, this document's Decision section should be checked against it.
5. `site.yaml`'s `name` is currently a locked value by default, one string, no locale map, with no mechanism for a transliterated rendering. Decide whether it needs the same one-string-or-locale-map shape already used for `tagline`, `description`, and `logos.alt`, so a client whose name requires a different written form in a non-Latin-script locale has a place to put it, rather than the site defaulting to the English spelling everywhere because nothing prompted the question.
6. Whether a "work" is better modeled as one idea with many renderings or as a body of ideas where a translation is one or more interpretations of it, raised in "The precedent: SAT already draws this line for content" above as a tentative suggestion, not pursued in this draft. Worth a separate conversation before it is folded into or rejected from this document, since it bears more on how content translation is reviewed than on where a configuration variable is stored.

## Related

`docs/en/docs/reference/decision-tree--value-language-relationships-placement-v0-1-0.md` (a clickable flowchart re-deriving the Decision section's placement rule against the current vocabulary), `docs/en/docs/reference/vocabulary--value-language-relationships-v0-1-0.md` (the fixed/locked/transliterated/translated/pattern terms this ADR argues a placement rule from), `docs/en/docs/reference/vocabulary--multilingual-content-structure-v0-1-0.md` (work identity, mirrored versus unmirrored content), `docs/en/docs/reference/spec--content-format-for-the-publishing-vector-v0-1-0.md` (the work/expression identity distinction, citing SAT ADR-010), `docs/en/docs/multilingual-plan.md` §6 (SAT integration, ADR-001, ADR-010, ADR-012, ADR-017), `branding/_template/assets/README.md` ("Logos, and the text a screen reader speaks"), `branding/_template/site.yaml` (the verbal identity block), `2026-08-13-132625-summary.md` (the incident this rule generalizes from).

## License

This document, *ADR: Fact and Expression, the Locale Scope of Configuration and Accessibility Variables*, by **Christopher Steel**, with AI assistance from **Claude (Anthropic)**, is licensed under the [GNU Affero General Public License v3.0 or later](https://www.gnu.org/licenses/agpl-3.0.html).

## Changelog

| Version | Status | Notes |
| --- | --- | --- |
| 0.1.0 | Draft | Initial draft. Names the fact/expression split, models it on SAT's work/expression identity and archive-purity ADRs, audits the site's current variable categories against it, and raises the two SVG description gaps and grammatical-agreement limits as open questions |
