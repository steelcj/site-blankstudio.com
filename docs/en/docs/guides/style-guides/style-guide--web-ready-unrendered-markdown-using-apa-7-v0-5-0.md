---
dc:title: "Style Guide: Web-Ready Unrendered Markdown Using APA 7"
dcterms:version: "0.5.0"
dc:creator: "Christopher Steel"
dc:description: "Conventions for authoring web-ready markdown source files conforming to APA 7 formatting and citation standards using the Citation Anchor Pair (CAP) workflow."
dcterms:created: "2026-07-23"
dcterms:modified: "2026-07-25"
dc:format: "text/markdown"
dc:language: "en"
sat:language_bcp47: "en"
dc:identifier: "style-guide--web-ready-unrendered-markdown-using-apa-7"
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
      Compliance pass per ROADMAP.md Milestone 0.3.0. Added the required
      License section. Prefixed the title, H1, and identifier with the
      style-guide convention so all naming layers agree with the filename.
      Added a deference statement to the authoritative versioned-documents
      guide. Removed the "numbered" qualifier from body sections and added
      License to the closing sequence in the one canonical order. Repaired
      the malformed 0.2.2 changelog rows, removed stale numbered-section
      references from changelog notes, and set body headings to sentence case.
  - version: "0.4.0"
    date: "2026-07-24"
    author: "Christopher Steel"
    notes: "Recreated in the sat-doc-automa repository and brought into compliance with the markdown defaults: heading numbers removed, horizontal rules removed, spaced em dashes replaced with commas, the heading-numbering rule revised to defer to Markdown: No Heading Numbers, a stale numbered-anchor link repaired, and the outdated style-guide.md reference replaced with the versionless slug."
  - version: "0.3.0"
    date: "2026-07-23"
    author: "Christopher Steel"
    notes: "Migrated into the sat-doc-automa repository. Added frontmatter. Resolved a version inconsistency in the source (filename said 0.2.2, version block said 0.2.0) by superseding both with 0.3.0. Body content unchanged from the 0.2.2 file."
---

# Style Guide: Web-Ready Unrendered Markdown Using APA 7

Version: 0.5.0
Status: Draft
Style Guide: style-guide--versioned-documents-in-unrendered-markdown

## Abstract

This document defines the conventions for authoring web-ready markdown source files that conform to APA 7 formatting and citation standards using the Citation Anchor Pair (CAP) workflow. It is intended for authors producing technical documentation that must render correctly across a broad range of markdown renderers while maintaining academically rigorous citation practice in its unrendered source form.

For document structure, filename patterns, frontmatter, and closing sections, this guide defers to *Style Guide: Versioned Documents in Unrendered Markdown*, which is authoritative across this repository. This guide governs APA 7 formatting and citation practice.

## Sources and acknowledgements

The conventions in this document are derived from three primary sources. Formatting and citation structure follow the <a name="apa-apa7-citation"></a>[American Psychological Association (2020)](#apa-apa7-reference) publication manual, seventh edition. Markdown syntax compatibility targets the <a name="apa-commonmark-citation"></a>[CommonMark specification (MacFarlane et al., 2024)](#apa-commonmark-reference) as the broadly supported baseline, with table syntax following the <a name="apa-gfm-citation"></a>[GitHub Flavoured Markdown specification (GitHub, 2024)](#apa-gfm-reference) where CommonMark has no equivalent.

## Principles

Web-ready markdown must satisfy two simultaneous requirements. First, the rendered output must be correct, readable, and broadly compatible across platforms. Second, the unrendered source must be clean, consistent, and maintainable by any author without specialised tooling. Where APA 7 conventions translate naturally to markdown they are applied directly. Where APA 7 has no equivalent, code blocks, for example, widely adopted markdown conventions are used and defined explicitly in this document.

### Web-ready markdown is not terminal-readable plain text

These are distinct formats with different conventions and must not be conflated. **Rule: Each paragraph is a single unbroken line. Do not wrap prose at 80 characters or at any other fixed width.** Terminal-readable plain text wraps prose at 80 characters per line to ensure readability in fixed-width terminal environments. This convention has no place in web-ready markdown. Markdown renderers handle line length and wrapping entirely. Introducing artificial line breaks in markdown source does not affect rendered output but introduces inconsistency and ambiguity in the source file. A line break in markdown source is either a blank line (paragraph separator) or an intentional structural element (list item, heading, code block). It is never a prose wrap. **If you are generating or editing this document with an AI assistant: do not wrap prose lines. Every paragraph is one line, regardless of length.**

## Source file conventions

### Encoding and line endings

Source files must be UTF-8 encoded with Unix line endings (LF). Windows line endings (CRLF) are not acceptable as they introduce inconsistencies across renderers and version control systems.

### Blank lines

A single blank line separates paragraphs. A single blank line separates a heading from the content that follows it. Two consecutive blank lines are not used. Trailing whitespace on any line is not acceptable.

### Horizontal rule

Do not use horizontal rule in the content of the document

### Line length

Prose paragraphs have no maximum line length. Each paragraph is written as a single continuous line. The following are the only acceptable reasons for a line break within body content: - A blank line to separate paragraphs or precede a heading, list, or  code block - A list item (`-` or `1.`) - A heading (`#`, `##`, etc.) - A fenced code block delimiter (` ``` `) - A table row (`|`) Wrapping prose at 80 characters, 100 characters, or any other fixed width is not acceptable. It is a terminal plain text convention and does not belong in web-ready markdown.

### File naming

File names are made from a slug of H1 title, they are lowercase, hyphen-separated and include the document's version in the version block. Spaces and underscores are not used. Example: `infrastructure-shim-pattern-v0-2-0.md`.

## Document structure

APA 7 document structure is applied as follows in markdown:

### Heading hierarchy

| APA 7 Level | Markdown | Usage |
|-------------|----------|-------|
| Level 1 | `#` | Document title only |
| Level 2 | `##` | Major sections |
| Level 3 | `###` | Subsections |
| Level 4 | `####` | Sub-subsections |
| Level 5 | `#####` | Rarely used; prefer restructuring |

Headings are sentence case, not title case, except for the document title which is title case. Headings are not numbered by default; if numbering would genuinely aid cross-referencing in a specific document, ask first (see *Markdown: No Heading Numbers* in this repository's markdown defaults). A single blank line follows every heading before body text begins.

### Required sections

Every document must contain the following sections in this order:

1. Title and version block
2. Abstract
3. Sources and acknowledgements
4. Body sections
5. License
6. Resources (grouped by topic, anchor-linked)
7. References (full APA 7 entries with CAP anchors)
8. Changelog

Body sections are not numbered; the closing sequence of License, Resources, References, and Changelog is the one canonical order defined by the versioned-documents guide, with Resources and References omitted when empty.

### Version block

The version block appears immediately below the title:

```markdown
Version: 0.1.0
Status: Draft | Review | Stable
Style Guide: style-guide--versioned-documents-in-unrendered-markdown
```

## Citations: the CAP workflow

All citations use the Citation Anchor Pair (CAP) workflow, which provides bidirectional navigation between in-text citations and their reference entries in the rendered document. Every source requires exactly two anchors: an in-text anchor and a reference anchor.

### Anchor naming

Anchor identifiers are lowercase, hyphen-separated, and derived from the source being cited. Example: a citation of the Pulumi documentation would use `pulumi-docs` as its base identifier.

Repeated citations of the same source append a counter:

- First citation: `apa-pulumi-docs-citation`
- Second citation: `apa-pulumi-docs-citation-2`
- Third citation: `apa-pulumi-docs-citation-3`

The reference anchor is always singular regardless of how many times the source is cited: `apa-pulumi-docs-reference`

### In-text citation format

**Narrative citation:**

```markdown
<a name="apa-pulumi-docs-citation"></a>[Pulumi (2024)](#apa-pulumi-docs-reference)
```

**Parenthetical citation:**

```markdown
<a name="apa-pulumi-docs-citation"></a>([Pulumi, 2024](#apa-pulumi-docs-reference))
```

### Reference entry format

```markdown
<a name="apa-pulumi-docs-reference"></a>Pulumi. (2024). *Pulumi documentation*. Pulumi Inc. https://www.pulumi.com/docs/
[Return to citation](#apa-pulumi-docs-citation)
```

Each reference entry includes a return link to its first in-text citation. Where a source is cited multiple times, the return link points to the first citation only.

### URLs and DOIs

- Always use live hyperlinks, never bare URLs in prose
- Prefer DOIs (`https://doi.org/...`) when available
- No trailing period after a URL or DOI
- Include a retrieval date only for undated or frequently changing content

## Code blocks

APA 7 has no native convention for code. The following conventions apply:

### Fenced code blocks

All code uses fenced code blocks with a language identifier. The language identifier enables syntax highlighting in renderers that support it and signals intent in those that do not.

````markdown
```python
def provision(self) -> ShimOutput:
    ...
```
````

Supported language identifiers include but are not limited to: `python`, `bash`, `hcl`, `yaml`, `json`, `markdown`, `text`.

Use `text` for output, logs, and any content that is not a recognised language. Use `markdown` for examples of markdown source within a markdown document.

### Inline code

Inline code uses single backticks and is used for file names, command names, variable names, and short code references within prose. Example: the `provision()` method returns a `ShimOutput`.

### Code block placement

Code blocks are preceded and followed by a single blank line. They are not indented relative to the surrounding prose. All code must be production ready and directly usable. Illustrative placeholders are not acceptable. Where a value is environment-specific, use a clearly named variable or note the value explicitly.

## Tables

Tables use standard GitHub Flavoured Markdown (GFM) pipe syntax, which renders correctly across the broadest range of platforms. Column headers are always present. Alignment markers (`---`, `:---`, `---:`, `:---:`) are used consistently within a table. Tables are preceded and followed by a single blank line.

```markdown
| Column A | Column B | Column C |
|----------|----------|----------|
| Value    | Value    | Value    |
```

## Emphasis and bold

**Bold** is used for defined terms on first use and for the labels of definition-style paragraphs. It is not used for general emphasis or decoration.

*Italic* is used for titles of works (as per APA 7) and for technical terms being introduced for the first time where bold is not appropriate.

Emphasis is used sparingly. If everything is emphasised, nothing is.

## Lists

Unordered lists use hyphens (`-`), not asterisks or plus signs. Ordered lists use numerals followed by a period (`1.`). List items are complete sentences or consistent fragments, mixing the two within a single list is not acceptable. A blank line precedes every list. Items within a list are not separated by blank lines unless the items themselves contain multiple paragraphs.

## Resources section

The Resources section appears before the References section and groups sources by topic for quick navigation. Entries link to their internal reference anchors, not to raw URLs.

```markdown
## Resources

### Infrastructure as Code
- [Pulumi Documentation](#apa-pulumi-docs-reference)
- [HashiCorp Terraform Documentation](#apa-terraform-docs-reference)

### Configuration Management
- [Ansible Documentation](#apa-ansible-docs-reference)
```

## References section

The References section contains full APA 7 formatted entries with CAP anchors and return links. Entries are listed alphabetically by author surname or, for organisational authors, by organisation name.

```markdown
## References

<a name="apa-pulumi-docs-reference"></a>Pulumi. (2024). *Pulumi documentation*. Pulumi Inc. https://www.pulumi.com/docs/
[Return to citation](#apa-pulumi-docs-citation)

<a name="apa-ansible-docs-reference"></a>Red Hat. (2024). *Ansible documentation*. Red Hat Inc. https://docs.ansible.com/
[Return to citation](#apa-ansible-docs-citation)
```

## License

This document, *Style Guide: Web-Ready Unrendered Markdown Using APA 7*, by **Christopher Steel**, with AI assistance from **Claude Sonnet 4.6 (Anthropic)**, is licensed under the [GNU Affero General Public License v3.0 or later](https://www.gnu.org/licenses/agpl-3.0.html).

## Resources

### Document Standards
- [APA 7 Publication Manual](#apa-apa7-reference)

### Markdown References
- [GitHub Flavoured Markdown Specification](#apa-gfm-reference)
- [CommonMark Specification](#apa-commonmark-reference)

## References

<a name="apa-apa7-reference"></a>American Psychological Association. (2020). *Publication manual of the American Psychological Association* (7th ed.). https://doi.org/10.1037/0000165-000
[Return to citation](#apa-apa7-citation)

<a name="apa-gfm-reference"></a>GitHub. (2024). *GitHub flavoured markdown specification*. GitHub Inc. https://github.github.com/gfm/
[Return to citation](#apa-gfm-citation)

<a name="apa-commonmark-reference"></a>MacFarlane, J., Gruber, A., & contributors. (2024). *CommonMark specification*. CommonMark. https://spec.commonmark.org/
[Return to citation](#apa-commonmark-citation)

## Changelog

| Version | Status | Notes |
|---------|--------|-------|
| 0.5.0 | Draft | Compliance pass: added the required License section, prefixed title/H1/identifier to agree with the filename, added a deference statement, de-numbered body sections, added License to the canonical closing sequence, repaired the malformed 0.2.2 changelog rows, removed stale numbered-section references, set body headings to sentence case |
| 0.4.0 | Draft | Recreated in sat-doc-automa; compliance pass: heading numbers and horizontal rules removed, em dashes to commas, numbering rule revised to defer to the markdown defaults, stale references repaired |
| 0.3.0 | Draft | Migrated into the sat-doc-automa repository; added frontmatter; resolved the filename (0.2.2) vs version block (0.2.0) inconsistency by superseding both; body content unchanged |
| 0.2.2 | Draft | Strengthened the web-ready-versus-terminal-text rule with an explicit AI-assistant instruction; added the line-length section with an exhaustive list of acceptable line-break reasons; renumbered subsequent source-file-convention sections |
| 0.2.1 | Draft | Changed file name to be H1 title and added section on not using horizontal rules in content |
| 0.2.0 | Draft | Removed incorrect 80-char line wrapping convention; added a section distinguishing web-ready markdown from terminal-readable plain text; renumbered source file convention sections |
| 0.1.0 | Draft | Initial draft |
