// Directory data for blog posts.
//
// Posts live in one folder per locale — content/blog/en-ca/, content/blog/fr-ca/
// — so the locale is read off the file path rather than declared in front
// matter. That is SAT's ADR-001 model: language expressed as filesystem
// structure, with each language archive independent.

const locales = require("../../_data/locales.js");

const byCode = Object.fromEntries(locales.list.map((l) => [l.code, l]));

// content/blog/<locale>/<slug> -> the locale entry
function localeFromPath(filePathStem) {
  const code = filePathStem.split("/").at(-2);
  return byCode[code];
}

module.exports = {
  layout: "article.njk",
  pageKey: "blog",
  css: ["home", "blog", "article"],
  footerMuted: false,

  eleventyComputed: {
    locale: (data) => localeFromPath(data.page.filePathStem),

    t: (data) => data.i18n[localeFromPath(data.page.filePathStem).code],

    urls: (data) => {
      const code = localeFromPath(data.page.filePathStem).code;
      const routes = data.i18n[code].routes;
      const out = {};
      for (const [key, slug] of Object.entries(routes)) {
        out[key] = `/${code}/${slug ? slug + "/" : ""}`;
      }
      return out;
    },

    permalink: (data) => {
      const code = localeFromPath(data.page.filePathStem).code;
      const blog = data.i18n[code].routes.blog;
      return `/${code}/${blog}/${data.page.fileSlug}/index.html`;
    },

    // Only locales that actually have this post. A post with no translation
    // yet emits no hreflang at all rather than a self-referencing pair, and is
    // hidden from the other locale's listing — no thin or duplicate pages.
    alternates: (data) => {
      const work = data["sat:work"];
      if (!work) return undefined;
      const expressions = data.workIndex[work];
      if (!expressions) return undefined;

      return locales.real
        .filter((l) => expressions[l.code])
        .map((l) => ({
          code: l.code,
          hreflang: l.htmlLang,
          label: l.label,
          url: `/${l.code}/${data.i18n[l.code].routes.blog}/${expressions[l.code]}/`,
        }));
    },

    // The other locales, each with the best URL to send the reader to. A page
    // always has a real counterpart; a post may not, in which case the reader
    // goes to that locale's blog index rather than the homepage or a dead link
    // — and `fallback` lets the UI say so instead of switching silently.
    switcher: (data) => {
      const alts = data.alternates || [];
      return locales.real
        .filter((l) => l.code !== data.locale.code)
        .map((l) => {
          const hit = alts.find((a) => a.code === l.code);
          return hit
            ? { code: l.code, label: l.label, hreflang: l.htmlLang, url: hit.url, fallback: false }
            : {
                code: l.code,
                label: l.label,
                hreflang: l.htmlLang,
                url: `/${l.code}/${data.i18n[l.code].routes.blog}/`,
                fallback: true,
              };
        });
    },

    xDefault: (data) => {
      const work = data["sat:work"];
      const expressions = work && data.workIndex[work];
      const fallbackSlug = expressions && expressions[locales.default];
      if (!fallbackSlug) return undefined;
      return `/${locales.default}/${data.i18n[locales.default].routes.blog}/${fallbackSlug}/`;
    },

    // Head values derived from each post's own front matter.
    pageTitle: (data) => `${data.title} | BLNK Studio`,
    pageDescription: (data) => data.excerpt,
    ogTitle: (data) => data.title,
    ogDescription: (data) => data.excerpt,
    ogType: () => "article",
    ogImage: (data) => data.image,

    // The closing CTA copy comes from the locale bundle, same as every page.
    ctaTitle: (data) => data.i18n[localeFromPath(data.page.filePathStem).code].blog.pageCta.title,
    ctaSub: (data) => data.i18n[localeFromPath(data.page.filePathStem).code].blog.pageCta.sub,
    ctaBtn1Label: (data) => data.i18n[localeFromPath(data.page.filePathStem).code].blog.pageCta.btn1Label,
    ctaBtn2Label: (data) => data.i18n[localeFromPath(data.page.filePathStem).code].blog.pageCta.btn2Label,
  },

  ctaBtn2Route: "services",
};
