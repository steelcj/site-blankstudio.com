---
dc:title: "Style Guide: Navigation and Accessibility"
dcterms:version: "0.2.0"
dc:creator: "Christopher Steel"
dc:description: "Governs the use of real ATX headings, rather than bolded pseudo-headings, for accessibility and deep-linking across OSAT Fluent and Universal Cake documentation."
dcterms:created: "2026-07-21"
dcterms:modified: "2026-07-25"
dc:format: "text/markdown"
dc:language: "en"
sat:language_bcp47: "en"
dc:identifier: "style-guide--navigation-accessibility"
dcterms:rightsHolder: "Christopher Steel"
dc:rights: >
  Copyright 2026 Christopher Steel.
  SPDX-License-Identifier: AGPL-3.0-or-later
sat:uuid: ""
sat:version_at_creation: "0.4.0"
sat:migration_status: pre-sat
sat:changelog:
  - version: "0.2.0"
    date: "2026-07-25"
    author: "Christopher Steel"
    notes: >
      Compliance pass per ROADMAP.md Milestone 0.3.0. Corrected the
      identifier to use the double-hyphen semantic separator matching the
      filename and sibling documents. Fixed the second W3C reference URL,
      which pointed at WCAG20 rather than WCAG21. Added a deference statement
      to the authoritative versioned-documents guide.
  - version: "0.1.1"
    date: "2026-07-24"
    author: "Christopher Steel"
    notes: "Recreated in the sat-doc-automa repository; normalized the Style Guide reference to the versionless slug per the versioned-documents guide's own version block convention."
  - version: "0.1.0"
    date: "2026-07-21"
    author: "Christopher Steel"
    notes: "Initial draft. Codifies the rule against bolded pseudo-headings, grounded in WCAG 2.1 and in how markdown renderers generate anchor IDs."
---

# Style Guide: Navigation and Accessibility

Version: 0.2.0
Status: Draft
Style Guide: style-guide--versioned-documents-in-unrendered-markdown

## Abstract

This style guide governs how headings are used in markdown documents across OSAT Fluent and Universal Cake, specifically the rule against using bold text as a substitute for real headings. It exists because this is easy to get subtly wrong: bolded text visually resembles a heading and reads correctly to a sighted person scanning the page, while carrying none of the structural information a heading actually needs to carry. It should be provided to any collaborator, human or AI, before editing or generating markdown documentation for either project.

For document structure, filename patterns, frontmatter, and closing sections, this guide defers to *Style Guide: Versioned Documents in Unrendered Markdown*, which is authoritative across this repository. This guide governs heading semantics and accessibility.

## Purpose

Documents in this project are frequently organized into per-platform or per-topic sections, Linux, macOS, and Windows being the most common case. The question this guide answers is narrow but consequential: when marking the start of one of those sections, is a real heading (`## Windows`) used, or is bold text at the start of a paragraph (`**Windows**`) used instead. This guide requires the former, always, and explains why the latter is not a lighter-weight equivalent.

## The rule

Use real ATX headings (`#`, `##`, `###`, and so on) for every section boundary, including per-platform and per-topic subsections. Never use bold text at the start of a line as a substitute for a heading.

This applies regardless of how minor the section feels. A three-line note under a bolded label is still a structural claim, it says "everything that follows, until the next one of these, belongs together," and that claim needs to be made in a form other than emphasis can read it.

## Why this matters: accessibility

Bold text and headings look similar to a sighted reader but are not equivalent in the underlying document structure, and that gap is exactly where the harm happens.

When a markdown renderer converts `## Windows` to HTML, it produces a real `<h2>` element. When it converts `**Windows**` to HTML, it produces a `<strong>` element, which conveys emphasis, not structure. Screen readers build a navigable outline of a page from heading elements specifically; most screen reader users jump between sections using a dedicated heading-navigation command (for example, the H key in NVDA, JAWS, and VoiceOver) rather than reading linearly from the top. A `<strong>` element does not appear in that outline at all. The section is, for a screen reader user relying on that navigation pattern, invisible as a section, even though its content is still read aloud in sequence.

This is not a hypothetical edge case; it is the direct subject of two Web Content Accessibility Guidelines (WCAG) 2.1 success criteria. Success Criterion 1.3.1, Info and Relationships (Level A), requires that structure conveyed visually also be conveyed programmatically, and its own guidance uses this exact scenario as a worked example: large, bold text before a block of content is visually inferred to be a heading, but that inference is not available to a screen reader unless the heading is actually marked up as one (World Wide Web Consortium Web Accessibility Initiative, n.d.-a). Success Criterion 2.4.6, Headings and Labels (Level AA), separately requires that where headings are used, they describe the content that follows (World Wide Web Consortium Web Accessibility Initiative, n.d.-b). Bolded pseudo-headings can satisfy 2.4.6 by being descriptive while still failing 1.3.1 outright, because the failure is structural, not editorial. Good wording does not fix a missing heading element.

## Why this matters: navigation and deep linking

The second failure mode is independent of accessibility and affects every reader equally, sighted or not.

Most markdown renderers, including the one used to render documents in this project's repositories, automatically generate a slug-based `id` attribute on every real heading element, and that `id` becomes a stable, linkable URL fragment (`#windows`, `#macos`, and so on). This is what makes a table of contents clickable, what makes a link from one document into a specific section of another possible, and what makes it possible to send someone a link that opens directly to the relevant part of a long document instead of the top of it. Bold text does not receive an `id`. There is no fragment to link to, no entry a generated table of contents can point at, and no way to reference that section from elsewhere without describing its location in prose instead of linking to it directly.

For a project with as much cross-referenced documentation as this one, style guides referencing other style guides, READMEs referencing ROADMAP items, FAQ entries referencing foundational documents, this is not a cosmetic loss. It removes a mechanism the rest of the documentation set actively depends on.

## Examples

Correct, a real heading:

```markdown
## Windows

There is no system Python by default...
```

Incorrect, a bolded pseudo-heading:

```markdown
**Windows.** There is no system Python by default...
```

The incorrect form is not wrong because of tone or wording; the sentence content could be identical in both cases. It is wrong because `**Windows.**` never becomes a heading element, no matter how it reads.

## Scope

This rule applies to every markdown document produced for OSAT Fluent or Universal Cake: READMEs, style guides, FAQs, evaluation documents, and ROADMAP files alike. It applies at every heading depth, `##` platform sections nested under a `###` subsection are held to the same rule as top-level `##` sections. There is no length threshold below which a bolded label becomes acceptable; a one-sentence section still needs a real heading if it is being presented as a distinct section rather than folded into the surrounding paragraph.

## License

This document, *Style Guide: Navigation and Accessibility*, by **Christopher Steel**, with AI assistance from **Claude Sonnet 4.6 (Anthropic)**, is licensed under the [GNU Affero General Public License v3.0 or later](https://www.gnu.org/licenses/agpl-3.0.html).

## References

World Wide Web Consortium Web Accessibility Initiative. (n.d.-a). *Understanding Success Criterion 1.3.1: Info and relationships*. W3C. Retrieved July 21, 2026, from https://www.w3.org/WAI/WCAG21/Understanding/info-and-relationships.html

World Wide Web Consortium Web Accessibility Initiative. (n.d.-b). *Understanding Success Criterion 2.4.6: Headings and labels*. W3C. Retrieved July 21, 2026, from https://www.w3.org/WAI/WCAG21/Understanding/headings-and-labels

## Changelog

| Version | Status | Notes |
|---------|--------|-------|
| 0.2.0 | Draft | Compliance pass: identifier corrected to the double-hyphen separator, second W3C URL corrected from WCAG20 to WCAG21, deference statement added |
| 0.1.1 | Draft | Recreated in sat-doc-automa; Style Guide reference normalized to the versionless slug |
| 0.1.0 | Draft | Initial draft |
