// Shared directory-data factory for the locale-first content tree.
//
// src/content/en-ca/en-ca.11tydata.js and src/content/fr-ca/fr-ca.11tydata.js
// each export `require("../_localeTree.js")(code)`, so both language roots share
// one implementation and differ only by their locale code. Everything under a
// root is that language's content, and its URL mirrors its file path:
//
//   src/content/en-ca/legal/privacy.md          -> /en-ca/legal/privacy/
//   src/content/fr-ca/mentions-legales/…/…​.md   -> /fr-ca/mentions-legales/…/
//
// Translations are paired by sat:work through _data/contentWorkIndex.js, not by
// matching paths — the mirrored model from the multilingual vocabulary.

const locales = require("../_data/locales.js");

module.exports = function localeTree(code) {
  const LOCALE = locales.list.find((l) => l.code === code);

  return {
    layout: "layouts/page.njk",
    css: ["home", "article"],

    eleventyComputed: {
      locale: () => LOCALE,
      t: (data) => data.i18n[code],

      urls: (data) => {
        const routes = data.i18n[code].routes;
        const out = {};
        for (const [key, slug] of Object.entries(routes)) {
          out[key] = `/${code}/${slug ? slug + "/" : ""}`;
        }
        return out;
      },

      // URL mirrors the file path: drop the leading "content" segment, and let a
      // folder's index.md resolve to the folder itself.
      permalink: (data) => {
        let stem = data.page.filePathStem.replace(/^\/?content/, "");
        stem = stem.replace(/\/index$/, "");
        return `${stem}/index.html`;
      },

      pageTitle: (data) => data.title,
      pageDescription: (data) => data.description,

      // Every expression of this work, self included, for the hreflang block.
      // Resolved by sat:work identity, never by path.
      alternates: (data) => {
        const work = data["sat:work"];
        if (!work) return undefined;
        const expr = data.contentWorkIndex[work];
        if (!expr) return undefined;
        return locales.real
          .filter((l) => expr[l.code])
          .map((l) => ({ code: l.code, hreflang: l.htmlLang, label: l.label, url: expr[l.code] }));
      },

      // The language switcher: a counterpart that exists is a direct link; a
      // missing one falls back to that language's home, flagged so the UI can
      // tell a real translation from a fallback (and so a future build check can
      // warn the owner and translators about the gap on a mirrored page).
      switcher: (data) => {
        const work = data["sat:work"];
        const expr = (work && data.contentWorkIndex[work]) || {};
        return locales.real
          .filter((l) => l.code !== code)
          .map((l) =>
            expr[l.code]
              ? { code: l.code, label: l.label, hreflang: l.htmlLang, url: expr[l.code], fallback: false }
              : { code: l.code, label: l.label, hreflang: l.htmlLang, url: `/${l.code}/`, fallback: true }
          );
      },

      xDefault: (data) => {
        const work = data["sat:work"];
        const expr = (work && data.contentWorkIndex[work]) || {};
        return expr[locales.default] || `/${locales.default}/`;
      },
    },
  };
};
