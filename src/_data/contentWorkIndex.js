// Maps a work identifier to the URL of every expression of that work across the
// locale-first content tree (src/content/<locale>/…), the sibling of
// _data/workIndex.js which does the same for the blog.
//
//   { "legal-privacy": { "en-ca": "/en-ca/about/legal/privacy/",
//                        "fr-ca": "/fr-ca/mentions-legales/confidentialite/" } }
//
// This is the mechanism the content model's language switcher and hreflang use
// to pair a page with its translations. The paths are localized and differ by
// design (mirrored translation), so correspondence is derived from the shared
// `sat:work` identity, never from names or paths.
//
// Built by reading front matter off disk rather than from an Eleventy
// collection: a collection would depend on each page's computed permalink,
// while the permalink needs the alternates this index provides — a cycle.
// Reading files directly breaks it, exactly as workIndex.js does for the blog.

const fs = require("fs");
const path = require("path");
const matter = require("gray-matter");
const locales = require("./locales.js");

const CONTENT_DIR = path.join(__dirname, "..", "content");

function walk(dir) {
  const out = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) out.push(...walk(full));
    else if (entry.name.endsWith(".md")) out.push(full);
  }
  return out;
}

// .../src/content/en-ca/about/legal/privacy.md  ->  /en-ca/about/legal/privacy/
// .../src/content/en-ca/about/legal/index.md    ->  /en-ca/about/legal/
function urlFor(file) {
  const rel = path.relative(CONTENT_DIR, file).replace(/\\/g, "/");
  let stem = "/" + rel.replace(/\.md$/, "");
  stem = stem.replace(/\/index$/, "");
  return stem + "/";
}

module.exports = function () {
  const index = {};

  for (const locale of locales.list) {
    const dir = path.join(CONTENT_DIR, locale.code);
    if (!fs.existsSync(dir)) continue;

    for (const file of walk(dir)) {
      const { data } = matter(fs.readFileSync(file, "utf8"));
      if (data.draft === true) continue;

      const work = data["sat:work"];
      if (!work) continue;

      if (!index[work]) index[work] = {};
      if (index[work][locale.code]) {
        throw new Error(
          `Two ${locale.code} pages share sat:work ${work}: ` +
            `"${index[work][locale.code]}" and "${urlFor(file)}". A work has at ` +
            `most one expression per language.`
        );
      }
      index[work][locale.code] = urlFor(file);
    }
  }

  return index;
};
