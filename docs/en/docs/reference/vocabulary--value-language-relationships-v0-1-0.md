---
dc:title: "Vocabulary and Definitions: Value-to-Language Relationships"
dcterms:version: "0.1.0"
dc:creator: "Christopher Steel"
dc:contributor: "Claude (Anthropic)"
dc:subject:
  - "vocabulary"
  - "i18n"
  - "accessibility"
  - "localization"
  - "terminology"
dc:description: >
  The project's working vocabulary for how a stored value relates to human
  language, independent of where the value lives: fixed, locked,
  transliterated, and translated, distinguished by one test, whether a
  correct alternate value exists for the same referent, and if so, what
  governs the choice among alternates. Also defines pattern, a fifth term for
  the structural frame that arranges one of the four, which does not answer
  the same test and is not commensurate with them.
dc:publisher: "UniversalCake"
dcterms:created: "2026-08-14"
dcterms:modified: "2026-08-14"
dc:format: "text/markdown"
dc:language: "en"
sat:language_bcp47: "en"
dc:identifier: "vocabulary--value-language-relationships"
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
      Initial draft. Extracted from adr--fact-and-expression-locale-scope-of-variables,
      where the terms first surfaced as a revision of an earlier, weaker
      fact/expression binary. Defines fixed, locked, transliterated, and
      translated values, distinguished by the referent-alternates test, plus
      a fifth term, pattern, for the compositional frame that arranges one of
      the four and does not answer that test itself. Split into its own
      document on the reasoning that
      the terms are reusable beyond the configuration-placement question the
      ADR asks of them, the same relationship this project's own
      vocabulary--multilingual-content-structure has to
      spec--content-format-for-the-publishing-vector.
---

# Vocabulary and Definitions: Value-to-Language Relationships

Version: 0.1.0
Status: Draft
Style Guide: style-guide--plain-language-for-general-audiences

## Abstract

This document defines the relationships a stored value can have to human language, independent of where that value happens to live in this codebase or what consumes it. It distinguishes four relationships a value can have to its referent, fixed, locked, transliterated, and translated, and states the single test that tells them apart: whether a correct alternate value exists for the same referent, and if one does, what governs the choice among the alternates. It also defines a fifth term, pattern, for the structural frame that arranges one of the four inside locale-specific grammar; pattern is not a fifth answer to the same test and is not comparable to the other four on the same terms, it names a different kind of thing. This document only names and defines the relationships. It does not decide where a variable should be stored; `adr--fact-and-expression-locale-scope-of-variables` uses these terms to argue for a placement rule, and `decision-tree--value-language-relationships-placement` turns that argument into a clickable flowchart, both should be read separately from this one.

## The test

For any value, ask: if a different string were used instead, would it still correctly identify the same thing? The answer, and if it is yes, what decides which correct string is used where, is what places a value in one of the four relationships below. Pattern, covered afterward, is a different kind of term and this test does not apply to it.

## Fixed value

A value where changing the value changes what is identified, not how it is expressed, so no correct alternate exists for the same referent. A hex color and a UUID both work this way: there is exactly one `#1a2b3c`, and exactly one thing any given `sat:work` UUID identifies. Picking a different value does not re-express the same referent, it picks a different referent. This is not a claim that such values stand outside language or notation altogether, a hex code is written in base-16, a UUID's hyphens are a formatting convention, both are human-made. It is a narrower and more durable claim: the value and the identity are the same fact, so there is nothing for a locale to localize. A phone number belongs here too, its digits identify one number, and no locale-correct alternate rendering of the same number exists, only formatting conventions around it.

## Locked value

A value where a correct alternate exists, in principle, but an owner has deliberately chosen to use one value everywhere rather than vary it. This is a choice about the value, not a property it has automatically, and it can be revised. "Palmolive" is the standing example: spelled any other way, the name would still, in principle, denote the same brand, a transliteration or a local adaptation could exist without the referent moving, but the brand chose one global spelling over varying it. A locked value is distinguished from a fixed value by exactly this: a fixed value has no correct alternate to choose against; a locked value has one and declines it.

## Transliterated value

A value where the referent stays the same, the same person, the same organization, but the written form legitimately changes by script or locale convention, without that change being a translation of meaning. A personal name originating outside the Latin script commonly has more than one accepted Latin rendering, "Brajesh" and "Vrajesh" for the same Devanagari name are both defensible, and a locale targeting a different script again, Devanagari, Cyrillic, Arabic, may need its own rendering of a name that is neither the source spelling nor a translation of it. What makes a value transliterated rather than locked is that the alternates are governed by a script or transcription convention, not by a decision to render meaning differently.

## Translated value

A value whose meaning is what has to survive, and whose wording is expected to differ by locale to carry that meaning correctly, the way a sentence does. What makes a value translated rather than transliterated or locked is that the correct alternate is judged by whether it preserves meaning, not by whether it follows a transcription convention or matches a chosen spelling.

## How the four value relationships compare

Fixed, locked, transliterated, and translated all answer the same question, the test above, about a single value and its referent. They compare directly:

| Relationship | Correct alternate exists for the same referent? | What governs the choice, if one is made |
| --- | --- | --- |
| Fixed | No | n/a, there is nothing to choose between |
| Locked | Yes, but declined | An owner's deliberate decision to use one value everywhere |
| Transliterated | Yes | Script or transcription convention |
| Translated | Yes | Preservation of meaning |

## Pattern value

A pattern is not a fifth answer to the test above, and does not belong in the table, because it is not a value with a referent in the first place. It is a structural frame that positions one of the four value kinds inside locale-specific word order or grammar, independent of what fills it: the frame's own wording and word order are always a translated value, since they are facts about the target language, while the value placed inside the frame can be fixed, locked, transliterated, or translated depending on what it names. Asking "does a correct alternate exist for the same referent" of the frame itself does not parse, a frame is not a referent-bearing value, it is the thing that holds one. `logoHome`'s `"{name} home"` in English and `"Accueil {name}"` in French is the frame; `site.name` is the fixed-or-locked value it holds.

## License

This document, *Vocabulary and Definitions: Value-to-Language Relationships*, by **Christopher Steel**, with AI assistance from **Claude (Anthropic)**, is licensed under the [GNU Affero General Public License v3.0 or later](https://www.gnu.org/licenses/agpl-3.0.html).

## Changelog

| Version | Status | Notes |
| --- | --- | --- |
| 0.1.0 | Draft | Initial draft; extracted from the ADR that first needed these terms. Defines fixed, locked, transliterated, and translated values against the referent-alternates test, plus pattern, a separate term for the frame that arranges them, not a fifth answer to the same test |
