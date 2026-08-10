---
dc:title: "Licensing Analysis: Choosing a License for the Canonical Site Template"
dcterms:version: "0.1.0"
dc:creator: "Christopher Steel"
dc:contributor: "Claude (Anthropic)"
dc:subject:
  - "licensing"
  - "AGPL"
  - "dual-licensing"
  - "SWOT"
  - "template"
  - "canonical"
dc:description: >
  A team-review analysis of licensing options for the canonical site template,
  with a SWOT for each realistic option, the ownership and CLA prerequisites
  for dual-licensing, dependency compatibility, and a comparison matrix.
dc:publisher: "UniversalCake"
dcterms:created: "2026-08-09"
dcterms:modified: "2026-08-09"
dc:format: "text/markdown"
dc:language: "en"
sat:language_bcp47: "en"
dc:identifier: "licensing-analysis--canonical-site-template-license-options-swot"
dcterms:rightsHolder: "Christopher Steel"
dc:rights: >
  Copyright 2026 Christopher Steel / UniversalCake.
  SPDX-License-Identifier: AGPL-3.0-or-later
sat:uuid: ""
sat:version_at_creation: ""
sat:migration_status: pre-sat
sat:changelog:
  - version: "0.1.0"
    date: "2026-08-09"
    author: "Christopher Steel"
    notes: >
      Initial draft for team review. Frames the licensing decision for the
      canonical site template, sets out the licensing layers and dependency
      constraints, SWOTs six options (proprietary, MIT, Apache-2.0, GPL-3.0,
      AGPL-3.0, and dual AGPL plus commercial), states the copyright-ownership
      and CLA prerequisite for dual-licensing, and offers a comparison matrix,
      a leaning recommendation, and open questions for the team to settle.
---

# Licensing Analysis: Choosing a License for the Canonical Site Template

Version: 0.1.0
Status: Draft — for team review
Style Guide: style-guide--plain-language-for-general-audiences

## Not legal advice

This document is written to help the team reach a shared, informed decision. It is not legal advice, and its author is not a lawyer. Before any option here is adopted, and especially before any commercial license grant or contributor agreement is relied upon, it should be reviewed by qualified counsel. Treat the drafts and recommendations as a starting point for that conversation, not as final terms.

## Abstract

We need to choose a license for the canonical site template. The choice is shaped by three facts about how we work: the template is the trunk of a repo-per-client model, where each client site is a fork; we run this as a paid, per-client business; and we already license our documentation under AGPL-3.0-or-later. This analysis sets out what is actually being licensed, what our dependencies allow, and a SWOT for each realistic option, so the team can decide together.

The leaning is toward a dual model, AGPL-3.0-or-later for a public canonical plus a commercial grant to clients, because it fits both the existing AGPL posture and the paid business. That option carries one hard prerequisite, described below: we must own or control the copyright on everything in canonical, which means a contributor agreement for the team.

## What we are actually licensing

A site template is not one thing under one license. It has layers, and they are not all licensed the same way.

| Layer | Examples | Who it belongs to |
| --- | --- | --- |
| Template code | Eleventy config, the CSS and JS system, `scripts/fetch-fonts.py`, the accessibility integration | Us (the license under analysis governs this) |
| Default content | Dummy copy, the docs, example sections | Us, and may take a content license (e.g. Creative Commons) distinct from the code |
| Client brand assets | A client's logo, their copy, their images | The client — never ours to license |
| Third-party dependencies | Fluid Infusion, self-hosted fonts, any libraries | Their own upstream licenses, which we cannot loosen |

The license decision in this document is about the first layer, the template code, with a note on the second. It never touches a client's own brand assets, and it cannot override the fourth.

## What our dependencies allow

A license choice is only real if the dependencies permit it. Ours do, and they impose no copyleft floor.

Fluid Infusion, which powers the accessibility bar, is dual-licensed under the New BSD (3-Clause) license or the Educational Community License, Version 2.0, and the recipient chooses which to accept ([fluid-project/infusion, n.d.](#ref-infusion-license); [Fluid Project, n.d.](#ref-fluid-licensing)). Both are permissive.

The self-hosted webfonts, Inter, Inter Tight, and Space Mono, are all under the SIL Open Font License 1.1 ([Andersson, n.d.](#ref-inter-license)). The OFL permits bundling and redistribution, including in commercial and proprietary products; its only real constraints are that the fonts not be sold on their own and that reserved font names not be reused on modified versions, neither of which affects self-hosting them in a site.

The practical conclusion: because every dependency is permissive, we are free to license our own template code as permissively or as restrictively as we like, including proprietary or copyleft. Nothing upstream forces our hand.

## The options, with a SWOT for each

Each option is judged in our specific context: a paid, per-client templating business, with a distributed team, an existing AGPL docs posture, and a static Eleventy site as the product.

### Proprietary / All Rights Reserved

Keep the canonical template private. No open-source license; it is an internal toolkit, delivered to clients under contract.

| | Helpful | Harmful |
| --- | --- | --- |
| **Internal** | **Strengths:** total control over terms; the template stays a private competitive asset; no obligation to publish anything; each client deal can be priced and scoped freely. | **Weaknesses:** no community, marketing, or contribution benefit; we carry all maintenance; still needs its own EULA and delivery contract drafted; contributors must assign rights anyway. |
| **External** | **Opportunities:** maximum differentiation; freedom to sell bespoke terms; can open-source later if we choose. | **Threats:** competitors building in the open gain mindshare we cannot; harder to attract collaborators who value open work; no ecosystem forms around a closed tool. |

### MIT

The shortest permissive license. Anyone, including clients and competitors, may use, modify, and keep the result closed.

| | Helpful | Harmful |
| --- | --- | --- |
| **Internal** | **Strengths:** universally understood and trivially easy for clients; compatible with everything; near-zero friction and admin. | **Weaknesses:** gives away any moat; no patent grant; no license-based revenue lever; no share-back obligation. |
| **External** | **Opportunities:** wide adoption can drive reputation and inbound leads; a plugin/ecosystem can grow around it. | **Threats:** a competitor can fork it into a rival product with no duty to contribute back, commoditizing our differentiator. |

### Apache-2.0

Permissive like MIT, but with an explicit patent grant and clearer notice and contribution terms.

| | Helpful | Harmful |
| --- | --- | --- |
| **Internal** | **Strengths:** patent grant and contribution clarity make it enterprise-friendly; aligns cleanly with Infusion's ECL-2.0 (itself Apache-based); still simple for clients. | **Weaknesses:** slightly more ceremony (NOTICE file, headers); still surrenders the moat; no revenue lever from the license itself. |
| **External** | **Opportunities:** adoption plus patent safety attracts larger users; a strong base for an open-core model later. | **Threats:** same as MIT — competitors may take it closed and compete; our investment can benefit rivals directly. |

### GPL-3.0-or-later

Copyleft: derivatives distributed to others must also be open under the GPL. No network clause.

| | Helpful | Harmful |
| --- | --- | --- |
| **Internal** | **Strengths:** derivatives that are distributed must stay open, so a competitor cannot ship a closed fork they hand to others; improvements remain shareable. | **Weaknesses:** for a hosted website the trigger is "conveying" a copy, which is murky for a site users interact with but do not download wholesale, so it may not force sharing at all; many client legal teams are wary of GPL; no revenue lever without a dual model. |
| **External** | **Opportunities:** invites share-alike contributions; a commercial exception can be added later. | **Threats:** compatibility friction with some permissive/proprietary combinations; the hosted-site loophole undercuts the very protection it is chosen for. |

### AGPL-3.0-or-later

Copyleft plus a network clause: anyone who runs a modified version that users interact with over a network must offer that version's complete source. This is our current docs license.

| | Helpful | Harmful |
| --- | --- | --- |
| **Internal** | **Strengths:** designed to close the hosted-service loophole GPL leaves open; the strongest assurance that a public template stays open; consistent with the docs we already ship under AGPL. | **Weaknesses:** a customized client site is a modified version, so on its face AGPL would require offering that site's complete source (Eleventy templates and build config, not just what the browser sees) to visitors — unacceptable to most paying clients on its own; note too that for a purely static site with no server-side program, whether the network clause even triggers is genuinely debatable, an ambiguity counsel should resolve. |
| **External** | **Opportunities:** the natural foundation for a dual-licensing revenue model; a strong open posture and reputation; contributions stay in the commons. | **Threats:** used without a commercial option, AGPL bans at client companies could cost deals; widespread misunderstanding of the obligations can scare off users. |

### Dual: AGPL-3.0-or-later + Commercial (current leaning)

Publish canonical under AGPL, and grant each client a separate commercial license that frees their delivered site from the copyleft obligations. This is the model the team is leaning toward.

| | Helpful | Harmful |
| --- | --- | --- |
| **Internal** | **Strengths:** the public AGPL edition protects the open version and our reputation while the commercial grant frees paying clients; the license itself becomes the revenue lever; consistent with the AGPL docs; competitors cannot close the public edition. | **Weaknesses:** only works if we own or control all copyright, which means a contributor agreement for the distributed team; two sets of terms to maintain; the commercial grant needs real legal drafting; requires contribution governance. |
| **External** | **Opportunities:** a proven commercial-open-source / open-core business model; the community edition drives leads while commercial terms are upsold; the promotion gate can double as the CLA checkpoint. | **Threats:** if copyright ownership is sloppy, we cannot legally sell the exception; some enforcement burden; without a clear dual-license notice, clients may be confused about which terms apply. |

## The prerequisite that makes dual-licensing legal

Any option that involves selling a commercial exception, that is, the dual model, or relicensing later, rests on one requirement: **UniversalCake must own or control the copyright on everything in canonical.** We can only grant a client a commercial exception to code we hold the rights to relicense.

With a distributed team, this does not happen automatically. By default, each contributor owns their own contribution and, by committing it to an AGPL project, licenses it to everyone under the AGPL — including us, but only under the AGPL. To include a teammate's work in a commercially-licensed deliverable, we need each human contributor to sign a lightweight Contributor License Agreement (CLA) or copyright assignment to UniversalCake.

Two things make this lighter than it sounds. First, it maps directly onto the canonical promotion gate already described in *The Canonical Loop*: "signed CLA" becomes an acceptance criterion for a promotion into canonical, right beside "generalized," "meets spec," and "proven." Second, AI-generated portions are generally not separately copyrightable, so they create no third-party rights-holder; it is the human teammates who need to sign.

## Comparison at a glance

| Option | Competitor can close & compete | Client can keep site source private | License is a revenue lever | Needs CLA / ownership control | Fits current AGPL docs | Client legal friction |
| --- | --- | --- | --- | --- | --- | --- |
| Proprietary | No | N/A (private) | Indirect | Yes (assignment) | Neutral | Low |
| MIT | Yes | Yes | No | No | Weak | Very low |
| Apache-2.0 | Yes | Yes | No | No | Weak | Low |
| GPL-3.0 | Mostly no | Unclear | No | No | Partial | Medium |
| AGPL-3.0 | No | No | No | No | Yes | High |
| Dual AGPL + commercial | No (public edition) | Yes (via grant) | Yes | Yes | Yes | Low (with grant) |

## Leaning recommendation

On the facts we have, the dual model, AGPL-3.0-or-later on canonical plus a commercial grant to clients, is the best fit, and it is where the team is already leaning. It preserves the open posture we have committed to with the docs, it protects the public edition from being closed by competitors, it frees paying clients from obligations they will not accept, and it turns the license into a revenue lever rather than a giveaway. Its cost is governance: we must run a contributor agreement so we actually own what we sell.

The honest alternatives, depending on what the team values:

If we do not want the CLA and ownership overhead, and protecting the template from competitors is not a priority, **Apache-2.0** is the clean permissive choice — patent grant included, easy for clients, and a fine base if we later move to open-core.

If the template is purely an internal weapon and we want no public edition at all, **proprietary / all rights reserved** is coherent — but note it still requires contributor assignment, and it forgoes the marketing and community upside.

Pure **AGPL without a commercial grant** should be avoided unless we are genuinely willing to have every client publish their site's complete source, which the paid model makes unlikely.

## Open questions for the team

- Do we want a public edition of the template at all, or should canonical stay private?
- Are we willing to run a CLA or assignment for every contributor? (This is required for the dual model and for any future relicensing.)
- Will clients accept publishing their site's source? (If not, pure AGPL is out and the commercial grant is essential.)
- Should default content and docs take a separate content license (e.g. Creative Commons) from the code?
- Who is the copyright holder of record — UniversalCake as an entity, or Christopher Steel personally — and is that consistent across the repos?
- What is the contact and process by which a client obtains the commercial grant?

## License

This document, *Licensing Analysis: Choosing a License for the Canonical Site Template*, by **Christopher Steel**, with AI assistance from **Claude (Anthropic)**, is licensed under the [GNU Affero General Public License v3.0 or later](https://www.gnu.org/licenses/agpl-3.0.html).

## References

<a name="ref-infusion-license"></a>fluid-project/infusion. (n.d.). *Infusion-LICENSE.txt*. GitHub. Retrieved August 9, 2026, from https://github.com/fluid-project/infusion/blob/main/Infusion-LICENSE.txt

<a name="ref-fluid-licensing"></a>Fluid Project. (n.d.). *Fluid Licensing*. Fluid Project Wiki. Retrieved August 9, 2026, from https://fluidproject.atlassian.net/wiki/spaces/fluid/pages/11547472/Fluid+Licensing

<a name="ref-inter-license"></a>Andersson, R. (n.d.). *Inter — LICENSE.txt (SIL Open Font License 1.1)*. GitHub. Retrieved August 9, 2026, from https://github.com/rsms/inter/blob/master/LICENSE.txt

<a name="ref-agpl"></a>Free Software Foundation. (2007). *GNU Affero General Public License, version 3*. Retrieved August 9, 2026, from https://www.gnu.org/licenses/agpl-3.0.html

## Changelog

| Version | Status | Notes |
| --- | --- | --- |
| 0.1.0 | Draft | Initial draft for team review: layers, dependency constraints, SWOT of six options, the ownership/CLA prerequisite for dual-licensing, a comparison matrix, a leaning recommendation toward dual AGPL + commercial, and open questions |
