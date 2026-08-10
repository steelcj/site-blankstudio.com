// Maps a work identifier to the slug of every expression of that work.
//
//   { "urn:uuid:018f2a91-…": { "en-ca": "rebrand-or-refine",
//                              "fr-ca": "refonte-ou-ajustement" } }
//
// This is the mechanism the language switcher and the hreflang block use to
// pair a post with its translations. It cannot be done by swapping a path
// segment: SAT's ADR-001 and ADR-010 make each language archive independently
// pathed on purpose, so an English post and its French translation have
// different slugs by design.
//
// `sat:work` comes from ADR-010 — a shared UUID that every expression of one
// work carries, as opposed to `dc:identifier`, which is unique per expression.
// Correspondence is derived from identity, never from names or paths.
//
// Built by reading front matter off disk rather than from an Eleventy
// collection. A collection would depend on each post's computed permalink,
// while the permalink needs the alternates that this index provides — a cycle.
// Reading the files directly breaks it, and matches how _data/i18n.js works.

const fs = require("fs");
const path = require("path");
const matter = require("gray-matter");
const locales = require("./locales.js");

const BLOG_DIR = path.join(__dirname, "..", "content", "blog");

module.exports = function () {
  const index = {};

  for (const locale of locales.list) {
    const dir = path.join(BLOG_DIR, locale.code);
    if (!fs.existsSync(dir)) continue;

    for (const file of fs.readdirSync(dir).filter((f) => f.endsWith(".md"))) {
      const { data } = matter(fs.readFileSync(path.join(dir, file), "utf8"));
      if (data.draft === true) continue;

      const work = data["sat:work"];
      if (!work) continue;

      const slug = file.replace(/\.md$/, "");
      if (!index[work]) index[work] = {};

      if (index[work][locale.code]) {
        throw new Error(
          `Two ${locale.code} posts share sat:work ${work}: ` +
            `"${index[work][locale.code]}" and "${slug}". A work has at most ` +
            `one expression per language.`
        );
      }
      index[work][locale.code] = slug;
    }
  }

  return index;
};
