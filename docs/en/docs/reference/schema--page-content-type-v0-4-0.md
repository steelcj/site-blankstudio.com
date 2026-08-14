---
dc:title: "Schema: Page Content-Type — Dublin Core Field Descriptions"
dcterms:version: "0.4.0"
dc:creator: "Christopher Steel"
dc:contributor: "Claude (Anthropic)"
dc:subject:
  - "schema"
  - "dublin-core"
  - "i18n"
  - "sat"
  - "example"
dc:description: >
  Two full, worked front-matter examples for the Page content type, an
  English (en-CA) and a French (fr-CA) expression of the same SAT work,
  followed by a description of every Dublin Core element used, read in the
  context of those two examples: what each element means, and whether it
  differs or stays identical between the two, tied to the fixed, locked,
  transliterated, translated, and pattern vocabulary established earlier.
dc:publisher: "UniversalCake"
dcterms:created: "2026-08-14"
dcterms:modified: "2026-08-14"
dc:format: "text/markdown"
dc:language: "en"
sat:language_bcp47: "en"
dc:identifier: "schema--page-content-type-v0-4-0"
dcterms:rightsHolder: "Christopher Steel"
dc:rights: >
  Copyright 2026 Christopher Steel / UniversalCake.
  SPDX-License-Identifier: AGPL-3.0-or-later
sat:uuid: ""
sat:version_at_creation: ""
sat:migration_status: pre-sat
sat:changelog:
  - version: "0.4.0"
    date: "2026-08-14"
    author: "Christopher Steel"
    notes: >
      Initial version. Two full worked examples (en-CA/fr-CA About page)
      built from the schema--page-content-type-v0-4-0.yaml working artifact,
      with a Dublin Core Descriptions section walking through every element
      used, in context, including the reasoning behind dc:publisher and
      dc:rights staying locked (identical) rather than translated.
---

# Schema: Page Content-Type — Dublin Core Field Descriptions

Version: 0.4.0
Status: Draft
Style Guide: style-guide--plain-language-for-general-audiences

## Description

Here we have an example of the metadata for an about page with an English Canadian version and a version in Quebecoise.

* One value ties them together, `dc:relation.sat.work` is identical in both
* Neither page is considered to be canonical

Everything else that should differ does:

* `dc:identifier` (own UUID and slug)
* `dc:language`
*  `dc:title`
* `dc:subject`
* `dc:description` (translated)
* `dc:source` (each page's own SAT archive record, not shared)
*  `dc:publisher` and `dc:rights` stay identical on purpose
  * locked values by the earlier vocabulary, one string everywhere rather than a translated string. <- is this the correct approach as in the safe as it was decided that although traditionally this has been an English proper Noun or license name???

## English About Page DC Metadata

```yaml
# src/content/en-ca/about.md
---
dc:title: "About"
dc:creator:
  - "Christopher Steel"
dc:subject:
  - "company"
  - "team"
dc:description: "Who we are and what we do."
dc:publisher: "UniversalCake"
dc:contributor:
  - "Claude (Anthropic)"
dc:date:
  created: "2026-08-14"
  modified: "2026-08-14"
  valid: ""
dc:type: "Text"
dc:format: "text/markdown"
dc:identifier:
  - "urn:uuid:550e8400-e29b-41d4-a716-446655440000"
  - "about"
dc:source: "urn:uuid:8f14e45f-ceea-467e-bd82-fceaa1315a26"
dc:language: "en-CA"
dc:relation:
  sat:
    work: "urn:uuid:6f9619ff-8b86-d011-b42d-00c04fc964ff"
dc:coverage: ""
dc:rights: "Copyright 2026 Christopher Steel / UniversalCake."
---
```

## French About Page DC Metadata

```yaml
# src/content/fr-ca/a-propos.md
---
dc:title: "À propos"
dc:creator:
  - "Christopher Steel"
dc:subject:
  - "entreprise"
  - "équipe"
dc:description: "Qui nous sommes et ce que nous faisons."
dc:publisher: "UniversalCake"
dc:contributor:
  - "Claude (Anthropic)"
dc:date:
  created: "2026-08-14"
  modified: "2026-08-14"
  valid: ""
dc:type: "Text"
dc:format: "text/markdown"
dc:identifier:
  - "urn:uuid:a1b2c3d4-1234-5678-9abc-def012345678"
  - "a-propos"
dc:source: "urn:uuid:2c1a9e3d-6b47-4f8a-9c3e-7d5b1a8f4e21"
dc:language: "fr-CA"
dc:relation:
  sat:
    work: "urn:uuid:6f9619ff-8b86-d011-b42d-00c04fc964ff"
dc:coverage: ""
dc:rights: "Copyright 2026 Christopher Steel / UniversalCake."
---
```

## Dublin Core Descriptions

### dc:title:

dc:title is used to name the resource, the string by which it is formally known. It differs between the two examples, "About" versus "À propos", because a title is meaning-bound: the same referent (this page) is properly named in the reader's own language. A translated value, in the vocabulary's terms, the words must change for the meaning to survive.

### dc:creator:

dc:creator identifies the entity primarily responsible for making the resource. Both examples list "Christopher Steel" identically, authorship is a fact about who wrote the page, not about which language it's read in. It's a transliterated value by the vocabulary's test, the referent (the person) is fixed, and here the written form of the name doesn't vary by script, so it stays identical rather than taking a script-specific alternate.

### dc:subject:

dc:subject gives the topic of the resource, typically as keywords. It differs, `company`/`team` versus `entreprise`/`équipe`, a translated value: tags are shown to readers, so their wording follows the page's language, same referent, different words.

### dc:description:

dc:description is a summary account of the resource. It differs for the same reason as the title, "Who we are and what we do" versus "Qui nous sommes et ce que nous faisons," meaning has to survive in the reader's own language.

### dc:publisher:

dc:publisher names the entity that makes the resource available, here the organization, "UniversalCake" in both. This answers the flagged question directly: yes, this is the correct category, not an English-default oversight. It's a locked value, the vocabulary's own worked example for "locked" is exactly this case, a brand name chosen once and used everywhere. There is no correct alternate to choose among, "UniversalCake" isn't translated into a French equivalent the way "About" is, because the value itself is the name, not a description of something that could legitimately be worded differently. It stays revisable, if the organization ever adopted a distinct French-market name, that would be a deliberate re-locking, a business decision, not a translation.

### dc:contributor:

dc:contributor names an entity that made a secondary contribution. Both list "Claude (Anthropic)" identically, same reasoning as dc:creator: this identifies who, not what language the page is written in, and that fact doesn't change between expressions of the same work.

### dc\:date\:

dc:date marks a point or period in the resource's lifecycle; the nested keys here narrow which one. Both pages share the same `created`/`modified` values in this example because the two expressions happened to be authored the same day, that's a coincidence of this example, not a rule, each expression's dates are its own fact and could diverge if, say, the French translation followed weeks after the English original. `valid` is empty in both, the field exists for a future expiration date but nothing uses it yet.

### dc:type:

dc:type states the nature or genre of the resource, drawn from a controlled vocabulary, here the DCMI Type Vocabulary's `"Text"` in both. A fixed value: what kind of thing a page is doesn't change with the language it's written in.

### dc:format:

dc:format is the resource's physical or digital manifestation, `"text/markdown"` in both, fixed for the same reason as type, the file format isn't a language fact.

### dc:identifier:

dc:identifier is an unambiguous reference to the resource itself, a UUID plus a human-readable alias here. It differs between the two, `about` and `a-propos` are different files with different identities, this is the expression identity from SAT ADR-010, each language version is its own distinct, individually addressable resource, separate from the work identity below that pairs them.

### dc:source:

dc:source names a related resource from which this one is derived. It differs between the two in this example, each expression is treated as its own rendering from its own SAT archive record, rather than one language being derived from the other. Whether this project ultimately wants one shared upstream archive record instead of one per language remains an open question from the earlier draft; this example takes the per-expression reading.

### dc:language:

dc:language states the language of the resource's intellectual content, given here as a BCP-47 tag, `en-CA` and `fr-CA`. This is the one field whose entire purpose is to say which language this expression is in.

### dc:relation:

dc:relation points to a related resource, the deliberately loose, symmetric DC element with no implied hierarchy. Nested underneath it, `sat.work` carries the one value that is identical in both examples, the shared work id. This is what ties the two pages together as expressions of one work with neither treated as canonical. `dc:source` was set aside for this earlier because it implies derivation; `dc:relation` doesn't, which is why the pairing lives here.

### dc:coverage:

dc:coverage is the spatial or temporal scope of the resource's content, left empty in both. An About page isn't about a particular place or time period, so the field is present, per the full-set-every-time decision, but unused, as it will be for nearly every page on this site.

### dc:rights:

dc:rights states information about rights held in or over the resource, a copyright line here, identical in both. This is the second half of the flagged question, and it holds up for a reason beyond convenience: a copyright notice is a legal statement, and legal statements are commonly kept in one fixed, deliberately chosen wording across languages specifically to avoid the ambiguity a translation could introduce into a legal claim, the same practical reasoning that keeps "Copyright" and "©" recognizable regardless of the surrounding language. It isn't that English is the default here, it's that a single authoritative wording is often preferred over several translations that could drift from each other in legal meaning. If a client ever wanted the rights line itself translated, that would be a deliberate decision to treat it as translated rather than locked, the vocabulary doesn't forbid that, it simply isn't the default.

## License

This document, *Schema: Page Content-Type — Dublin Core Field Descriptions*, by **Christopher Steel**, with AI assistance from **Claude (Anthropic)**, is licensed under the [GNU Affero General Public License v3.0 or later](https://www.gnu.org/licenses/agpl-3.0.html).

## Changelog

| Version | Status | Notes |
| --- | --- | --- |
| 0.4.0 | Draft | Initial version; two full worked examples (en-CA/fr-CA About page) plus a Dublin Core Descriptions section covering every element in context, including the dc:publisher/dc:rights locked-value reasoning |
