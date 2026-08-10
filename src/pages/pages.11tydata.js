// Directory data for every top-level page.
//
// Each page in this folder is authored once and emitted once per locale: the
// pagination block below walks locales.list, and eleventyComputed derives the
// output path and the string bundle for whichever locale is being rendered.
//
// Route slugs are per-locale (ADR-001 in SAT treats language archives as
// independently pathed, and in-language URLs rank better), so a page declares
// a `routeKey` in its front matter — "about" — and the slug for that key is
// looked up in the locale's bundle: "about" in en, "a-propos" in fr.

module.exports = {
  pagination: {
    data: "locales.list",
    size: 1,
    alias: "locale",
    // Defaults to false, which puts only the FIRST pagination output into
    // collections — every non-default locale would then be missing from the
    // generated sitemap while still being a real, indexable page.
    addAllPagesToCollections: true,
  },

  eleventyComputed: {
    // The active locale's string bundle, already merged over the default.
    t: (data) => data.i18n[data.locale.code],

    // Page metadata and CTA copy resolve from the locale bundle, not from
    // front matter. Front matter is plain YAML with no access to the active
    // locale, so anything left there renders in English on every locale — an
    // English <title>, meta description and Open Graph card on French pages,
    // which is an SEO problem rather than a cosmetic one.
    //
    // Undefined is deliberate where a page has no such copy: the nav and CTA
    // partials fall back to their own defaults.
    pageTitle: (data) => data.i18n[data.locale.code][data.routeKey]?.meta?.title,
    pageDescription: (data) => data.i18n[data.locale.code][data.routeKey]?.meta?.description,
    ogTitle: (data) => data.i18n[data.locale.code][data.routeKey]?.meta?.ogTitle,
    ogDescription: (data) => data.i18n[data.locale.code][data.routeKey]?.meta?.ogDescription,

    ctaTitle: (data) => data.i18n[data.locale.code][data.routeKey]?.pageCta?.title,
    ctaSub: (data) => data.i18n[data.locale.code][data.routeKey]?.pageCta?.sub,
    ctaBtn1Label: (data) => data.i18n[data.locale.code][data.routeKey]?.pageCta?.btn1Label,
    ctaBtn2Label: (data) => data.i18n[data.locale.code][data.routeKey]?.pageCta?.btn2Label,
    ctaMicro: (data) => data.i18n[data.locale.code][data.routeKey]?.pageCta?.micro,

    navCtaLabel: (data) => data.i18n[data.locale.code][data.routeKey]?.pageNav?.ctaLabel,
    mobileCta1Label: (data) => data.i18n[data.locale.code][data.routeKey]?.pageNav?.mobileCta1Label,
    mobileCta2Label: (data) => data.i18n[data.locale.code][data.routeKey]?.pageNav?.mobileCta2Label,

    // Every route as a ready-to-use URL for the active locale, so templates
    // write {{ urls.about }} rather than assembling paths inline. Keeping this
    // in one place is what makes the language switcher and the hreflang block
    // agree in Phase 4 — they read the same derived table.
    urls: (data) => {
      const routes = data.i18n[data.locale.code].routes;
      const out = {};
      for (const [key, slug] of Object.entries(routes)) {
        out[key] = `/${data.locale.code}/${slug ? slug + "/" : ""}`;
      }
      return out;
    },

    permalink: (data) => {
      const slug = data.i18n[data.locale.code].routes[data.routeKey];
      if (slug === undefined) {
        throw new Error(
          `Page "${data.page.inputPath}" declares routeKey "${data.routeKey}", ` +
            `which has no slug in _locales/${data.locale.code}.json`
        );
      }
      return `/${data.locale.code}/${slug ? slug + "/" : ""}index.html`;
    },

    // Every locale's URL for THIS page, keyed off routeKey rather than by
    // swapping a path segment — the French slugs differ ("a-propos",
    // "audit-gratuit"), so path arithmetic would produce URLs that 404.
    //
    // One source for both the hreflang block and the sitemap, so the two can
    // never disagree. Phase 4 extends the same idea to posts via sat:work.
    // Pseudo-locales are excluded: they are build-only test targets and must
    // never be advertised to a search engine or offered to a reader.
    alternates: (data) =>
      data.locales.real.map((l) => {
        const slug = data.i18n[l.code].routes[data.routeKey];
        return {
          code: l.code,
          hreflang: l.htmlLang,
          label: l.label,
          url: `/${l.code}/${slug ? slug + "/" : ""}`,
        };
      }),

    // The other locales, each with the best URL to send the reader to. A page
    // always has a real counterpart; a post may not, in which case the reader
    // goes to that locale's blog index rather than the homepage or a dead link
    // — and `fallback` lets the UI say so instead of switching silently.
    switcher: (data) => {
      const alts = data.alternates || [];
      return data.locales.real
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

    // x-default points at the default locale rather than a language selector:
    // there is no selector page, and the default locale is a real, complete
    // version of every page.
    xDefault: (data) => {
      const slug = data.i18n[data.locales.default].routes[data.routeKey];
      return `/${data.locales.default}/${slug ? slug + "/" : ""}`;
    },
  },
};
