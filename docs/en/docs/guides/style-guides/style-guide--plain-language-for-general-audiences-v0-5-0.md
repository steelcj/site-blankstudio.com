---
dc:title: "Style Guide: Plain Language for General Audiences"
dcterms:version: "0.5.0"
dc:creator: "Christopher Steel"
dc:description: "Governs the authoring of plain language documents intended for a general audience; companion to the technical documentation style guide."
dcterms:created: "2026-07-23"
dcterms:modified: "2026-07-25"
dc:format: "text/markdown"
dc:language: "en"
sat:language_bcp47: "en"
dc:identifier: "style-guide--plain-language-for-general-audiences"
dcterms:rightsHolder: "Christopher Steel"
dc:rights: >
  Copyright 2026 Christopher Steel.
  SPDX-License-Identifier: AGPL-3.0-or-later
sat:uuid: ""
sat:version_at_creation: "0.4.0"
sat:migration_status: pre-sat
sat:changelog:
  - version: "0.5.0"
    date: "2026-07-25"
    author: "Christopher Steel"
    notes: >
      Compliance pass per ROADMAP.md Milestone 0.3.0. Added a deference
      statement to the authoritative versioned-documents guide. Removed the
      "numbered" qualifier from body sections and deferred heading numbering
      to Markdown: No Heading Numbers. Added License to the closing sequence
      and aligned it to the one canonical order. Replaced double hyphens in
      prose when naming the technical guide, corrected a stale numbered-section
      reference in the changelog, and set the Sources heading to sentence case.
  - version: "0.4.0"
    date: "2026-07-24"
    author: "Christopher Steel"
    notes: "Recreated in the sat-doc-automa repository and brought into compliance with the markdown defaults: heading numbers removed, spaced em dashes replaced with commas, H1 double hyphen replaced with a colon, governing style guide reference normalized to the versionless slug. Rule content otherwise unchanged."
  - version: "0.3.0"
    date: "2026-07-23"
    author: "Christopher Steel"
    notes: "Migrated into the sat-doc-automa repository. Added frontmatter; corrected filename version separators from dots/underscores to the hyphenated convention. Body content unchanged from 0.2.0."
---

# Style Guide: Plain Language for General Audiences

Version: 0.5.0
Status: Draft
Style Guide: style-guide--technical-documentation-for-technologists

## Abstract

This style guide governs the authoring of plain language documents intended for a general audience. It is a companion to *Style Guide: Technical Documentation for Technologists*. It exists to ensure consistency across sessions and versions of any document it governs. It should be provided to any collaborators, human or AI, at the start of a new session involving the creation of plain language content.

## Sources and acknowledgements

Plain language principles in this document follow the <a name="apa-plain-language-citation"></a>[Plain Language Action and Information Network (2011)](#apa-plain-language-reference) federal plain language guidelines, the authoritative plain language standard used by the United States government. Reading level measurement uses the <a name="apa-flesch-kincaid-citation"></a>[Flesch (1948)](#apa-flesch-kincaid-reference) readability formula and its refinement by <a name="apa-kincaid-citation"></a>[Kincaid et al. (1975)](#apa-kincaid-reference), which together form the Flesch-Kincaid grade level scale. Document structure and citation practice follow the <a name="apa-apa7-citation"></a>[American Psychological Association (2020)](#apa-apa7-reference) publication manual, seventh edition.

## Purpose

This style guide governs the authoring of plain language documents intended for a general audience. It is a companion to *Style Guide: Technical Documentation for Technologists*. Where that guide governs precise, peer-to-peer technical writing, this guide governs writing for a general audience. The two share the same document conventions, versioning, structure, markdown formatting, and authoring process, so that a project can produce both technical and plain language documentation without maintaining two incompatible systems. Those shared conventions, filename patterns, frontmatter, structure, and closing sections, are defined by *Style Guide: Versioned Documents in Unrendered Markdown*, which is authoritative; this guide governs plain-language register and audience.

It exists to ensure consistency across sessions and versions of any document it governs. It should be provided to any collaborators, human or AI, at the start of a new session involving the creation of plain language content.

## Versioning this style guide

The style guide itself is versioned using semantic versioning (MAJOR.MINOR.PATCH):

- **PATCH**, spelling, grammar, or clarification of existing rules with no change to intent
- **MINOR**, new rules added, or existing rules meaningfully refined
- **MAJOR**, a fundamental change in approach, audience, or scope

The version and status (Draft, Review, Stable) appear in the header of this document and in any document it governs. Changes are noted in the changelog section at the bottom of this document. The style guide version in use should be referenced in the header of any document it governs.

## Intended reader

A general audience with mixed ages, backgrounds, and levels of technical familiarity. The reader may have no prior knowledge of the subject. They should not need to re-read a sentence to understand it.

The goal is immediate comprehension. A reader should be able to pick up any document governed by this style guide and follow it without difficulty, regardless of their background.

## Voice and register

Write in the author's voice. Correct spelling and grammar but do not rewrite. Offer suggestions for improvements in clarity as a summary, then go through one section at a time until the author is satisfied.

Documents governed by this style guide target a Flesch-Kincaid grade level of 7 or below <a name="apa-flesch-kincaid-citation-2"></a>([Flesch, 1948](#apa-flesch-kincaid-reference)). This is a plain language standard used by governments, health communicators, and major publications worldwide. It does not mean writing for children. It means writing so that anyone can read without friction, including experts, who read plain language faster and prefer it <a name="apa-plain-language-citation-2"></a>([Plain Language Action and Information Network, 2011](#apa-plain-language-reference)).

To achieve this:

- Use short sentences. Aim for an average of 15 words. Never exceed 25.
- Use common words. If a simpler word works, use it.
- Define any term that a general reader may not know, the first time it appears.
- Avoid jargon, acronyms, and abbreviations unless they are defined inline.
- Write in active voice. Passive voice is acceptable only when the actor is unknown or unimportant.
- Avoid filler phrases. Every sentence should carry meaning.

## Tone by section type

**Introductory sections**, warm and direct. Establish what the document is about and why it matters to the reader. Do not assume prior knowledge. Do not front-load detail.

**Explanatory sections**, clear and patient. Build understanding one idea at a time. Use examples and analogies where they help. Do not use an analogy that requires as much explanation as the thing it is explaining.

**Instructional sections**, precise and sequential. If you think numbered steps would be helpful then explain why and specifically request permission to use them. Use plain imperatives ("click Save", "open the terminal"). Do not skip steps that feel obvious, what is obvious to the author is often not obvious to the reader.

**Reference sections**, concise and scannable. Use short entries. Readers coming to a reference section already have context, do not re-explain, just inform.

## Decisions and rationale

Every significant decision about how a document is written must be documented:

1. What was decided
2. Why it was decided
3. What alternatives were considered and why they were not chosen

This applies especially to decisions about terminology, structure, and the level of detail provided. A plain language document involves real editorial choices. Those choices should be traceable.

## Terminology

Use the simplest term that is accurate. Do not use a technical term where a plain word works. When a technical term is necessary, define it in plain language the first time it appears. Definitions should be inline, do not send the reader to a glossary unless the document is long enough to warrant one.

Prefer consistent terms over varied ones. Do not alternate between "computer", "machine", and "device" to avoid repetition. Pick one and use it throughout.

## Structure

Documents governed by this style guide follow this general structure:

1. **Title and version block**, as defined by *Style Guide: Versioned Documents in Unrendered Markdown*
2. **Abstract**, two to four sentences. What is this document, and who is it for?
3. **Body sections**, with plain language headings that describe the content, not the category. Headings are not numbered (see *Markdown: No Heading Numbers*); number them only if explicitly requested.
4. **License**, the document's licence statement
5. **Resources**, grouped by topic, linked to reference anchors
6. **References**, full APA 7 entries with CAP anchors
7. **Changelog**, versioned table of changes

Sections are composed paragraph by paragraph. Each paragraph covers one idea. If a paragraph requires more than five sentences, consider whether it contains two ideas that should be separated.

Use standard markdown headings:

- `#` Document title
- `##` Major sections
- `###`, `####`, `#####`, `######` for nested subheadings

Never use bold in markdown headings.

### File naming

File names are slugs of the H1 title. They are lowercase and hyphen-separated. The document version is appended using the format `vMAJOR-MINOR-PATCH.`

Example:

 ```bash
 git--a-plain-language-guide-v0-1-0.md
 ```

## Code and examples

Plain language documents may include code blocks, terminal output, or file examples where the subject requires it. All code must be production ready and directly usable. Illustrative placeholders are not acceptable. Where a value is environment-specific, use a clearly named variable or note the value explicitly.

When introducing code in a plain language document, always precede it with a sentence explaining what it does and what the reader should expect to see.

## Authoring process

Work one paragraph at a time. Agree each paragraph before moving to the next. Spelling and grammar are corrected by the collaborator without changing the author's intent or voice. Factual corrections are flagged as questions before being applied.

At the start of each new session, provide this style guide and the current state of the document being worked on. This gives a new collaborator the context needed to continue coherently.

Plain language documents should be reviewed for reading level before they are marked Stable. A Flesch-Kincaid grade level of 7 or below is the target <a name="apa-kincaid-citation-2"></a>([Kincaid et al., 1975](#apa-kincaid-reference)). Most word processors and many online tools can measure this.

## Resources

### Plain language standards

- [Federal Plain Language Guidelines](#apa-plain-language-reference)

### Readability measurement

- [Flesch Reading Ease formula](#apa-flesch-kincaid-reference)
- [Flesch-Kincaid Grade Level scale](#apa-kincaid-reference)

### Document standards

- [APA 7 Publication Manual](#apa-apa7-reference)

## References

<a name="apa-apa7-reference"></a>American Psychological Association. (2020). *Publication manual of the American Psychological Association* (7th ed.). https://doi.org/10.1037/0000165-000
[Return to citation](#apa-apa7-citation)

<a name="apa-flesch-kincaid-reference"></a>Flesch, R. (1948). A new readability yardstick. *Journal of Applied Psychology*, *32*(3), 221–233. https://doi.org/10.1037/h0057532
[Return to citation](#apa-flesch-kincaid-citation)

<a name="apa-kincaid-reference"></a>Kincaid, J. P., Fishburne, R. P., Rogers, R. L., & Chissom, B. S. (1975). *Derivation of new readability formulas (Automated Readability Index, Fog Count and Flesch Reading Ease Formula) for Navy enlisted personnel* (Research Branch Report 8-75). Naval Technical Training Command. https://apps.dtic.mil/sti/citations/ADA006655
[Return to citation](#apa-kincaid-citation)

<a name="apa-plain-language-reference"></a>Plain Language Action and Information Network. (2011). *Federal plain language guidelines*. United States Government. https://www.plainlanguage.gov/guidelines/
[Return to citation](#apa-plain-language-citation)

## Changelog

| Version | Status | Notes |
|---------|--------|-------|
| 0.5.0 | Draft | Compliance pass: deference statement added, body sections de-numbered and heading numbering deferred to the markdown default, License added to the closing sequence, double hyphens in prose replaced, stale numbered-section reference and Sources heading case corrected |
| 0.4.0 | Draft | Recreated in sat-doc-automa; compliance pass: heading numbers removed, em dashes to commas, H1 retitled with colon, style guide reference normalized |
| 0.3.0 | Draft | Migrated into the sat-doc-automa repository; added frontmatter; corrected filename version separators to the hyphenated convention; body content unchanged |
| 0.2.0 | Draft | Added a file naming rule: lowercase hyphen-separated slug of the H1 title with the version suffix appended |
| 0.1.0 | Draft | Initial draft |
