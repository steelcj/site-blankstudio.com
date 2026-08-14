const fs = require("fs");
const path = require("path");

const locales = require("./src/_data/locales.js");
const site = require("./src/_data/site.json");
const { activeClient, clientDir } = require("./lib/branding.js");

// BCP 47 tag of the default locale, used whenever a date is formatted outside
// a page that knows its own locale.
const DEFAULT_LANG =
  (locales.list.find((l) => l.code === locales.default) || {}).htmlLang || "en";

// Offset of `timeZone` from UTC at a given instant, in milliseconds. Derived
// from Intl rather than hardcoded so daylight saving is handled for free:
// format the instant in the target zone, re-read those wall-clock fields as
// if they were UTC, and the difference is the offset that applied.
function zoneOffsetMs(date, timeZone) {
  const parts = new Intl.DateTimeFormat("en-US", {
    timeZone,
    hour12: false,
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  })
    .formatToParts(date)
    .reduce((acc, p) => ((acc[p.type] = p.value), acc), {});

  const asUTC = Date.UTC(
    Number(parts.year),
    Number(parts.month) - 1,
    Number(parts.day),
    Number(parts.hour) % 24, // some ICU builds emit "24" for midnight
    Number(parts.minute),
    Number(parts.second)
  );
  return asUTC - date.getTime();
}

// Normalises a stored publish date to the instant it should be rendered from.
//
// Posts authored since the datetime change carry a real offset
// ("2026-05-14T09:30:00-04:00") and pass through untouched.
//
// Older posts were authored date-only ("date: 2026-05-14"), which YAML and JS
// both resolve to exactly midnight UTC — 20:00 the previous day in Toronto,
// which would render the whole back catalogue a day early. By convention here,
// a value landing on exact UTC midnight is a calendar date rather than an
// instant, and is re-anchored to midnight in the publication zone so it renders
// as the day it was written. New posts always carry a time, so this only ever
// applies to legacy content.
function publicationInstant(value) {
  const d = new Date(value);
  const isCalendarDate =
    d.getUTCHours() === 0 &&
    d.getUTCMinutes() === 0 &&
    d.getUTCSeconds() === 0 &&
    d.getUTCMilliseconds() === 0;

  if (!isCalendarDate) return d;
  return new Date(d.getTime() - zoneOffsetMs(d, site.publicationTimeZone));
}

module.exports = function (eleventyConfig) {
  // Copy static asset folders straight through, untouched.
  eleventyConfig.addPassthroughCopy("src/css");
  eleventyConfig.addPassthroughCopy("src/js");
  eleventyConfig.addPassthroughCopy("src/assets");
  eleventyConfig.addPassthroughCopy("src/admin");
  eleventyConfig.addPassthroughCopy("src/robots.txt");
  eleventyConfig.addPassthroughCopy("src/_redirects");

  // Client brand assets live outside src/, in branding/<client>/assets/, so a
  // rebrand is one directory. Discover the one active client (ignoring
  // _-prefixed templates) and copy its assets over /assets/, alongside the
  // generated fonts and the Sveltia uploads that stay in src/assets/. Brand
  // images no longer live in src/assets, so the two copies write different
  // files into /assets/ and never collide.
  const client = activeClient();
  if (client && clientDir("assets")) {
    const rel = path.posix.join("branding", client, "assets");
    eleventyConfig.addPassthroughCopy({ [rel]: "assets" });
  }

  // The same directory also holds the seed content tree that src/_data/menu.js
  // reads the menu out of. Data files are not watched through their own
  // require()s, so without this a section added to the seed only appears after
  // a restart.
  eleventyConfig.addWatchTarget("branding");

  // Infusion (accessibility bar). Served from /assets/vendor/infusion/ and
  // loaded on demand by src/js/a11y.js, never on the critical path — the JS
  // alone is ~176 KB gzip against the site's own 2 KB.
  const INFUSION = "node_modules/infusion";
  eleventyConfig.addPassthroughCopy({
    [`${INFUSION}/dist/infusion-uio.js`]: "assets/vendor/infusion/infusion-uio.js",
    [`${INFUSION}/src/framework/preferences/html`]: "assets/vendor/infusion/html",
    [`${INFUSION}/src/framework/preferences/messages`]: "assets/vendor/infusion/messages",
    [`${INFUSION}/src/framework/preferences/css`]: "assets/vendor/infusion/css",
    // Infusion's base stylesheet. The working reference implementation at
    // idrc.ocadu.ca loads this alongside the preferences CSS; without it the
    // panel body's display:table layout has no base rules to build on.
    [`${INFUSION}/src/framework/core/css/fluid.css`]: "assets/vendor/infusion/css/fluid.css",
    [`${INFUSION}/src/framework/preferences/fonts`]: "assets/vendor/infusion/fonts",
    // The table-of-contents enactor ships its own template and messages
    // outside the preferences directory, referenced by a relative path that
    // does not survive being served from /assets. a11y.js overrides both.
    [`${INFUSION}/src/components/tableOfContents/html`]: "assets/vendor/infusion/toc",
  });

  // The UIO stylesheets reference webfonts as ../../../lib/<pkg>/fonts/…, which
  // from /assets/vendor/infusion/css/ resolves to /assets/lib/<pkg>/fonts/.
  // Only the four font packages are published — the rest of src/lib (jquery,
  // hypher) is already inside the bundle.
  eleventyConfig.addPassthroughCopy({
    [`${INFUSION}/src/lib/atkinson-hyperlegible`]: "assets/lib/atkinson-hyperlegible",
    [`${INFUSION}/src/lib/opendyslexic`]: "assets/lib/opendyslexic",
    [`${INFUSION}/src/lib/opensans`]: "assets/lib/opensans",
    [`${INFUSION}/src/lib/roboto-slab`]: "assets/lib/roboto-slab",
  });

  // The dev server does not read src/_redirects — that file is Netlify's, and
  // it is what sends "/" to the default locale in production. Locally, "/" is
  // simply a path nothing is written to, so it served the 404 page and made
  // every `npm start` look broken. This mirrors the one rule that matters for
  // getting into the site, so local and production agree on where "/" goes.
  //
  // 302 rather than the production 301: a permanent redirect is cached by the
  // browser, and a cached redirect to a locale is a nuisance the day the
  // default changes.
  eleventyConfig.setServerOptions({
    onRequest: {
      "/": () => ({
        status: 302,
        headers: { Location: `/${locales.default}/` },
        body: "",
      }),
    },
  });

  // sitemap.xml is now generated by src/sitemap.njk with hreflang alternates.
  // No passthrough copy — the two would fight over the same output path.

  // String bundles are plain JSON outside _data/, so Eleventy does not watch
  // them on its own. Without this, editing a translation needs a full restart.
  eleventyConfig.addWatchTarget("src/_locales");

  // One posts collection per locale. Posts live in content/blog/<locale>/, so
  // the folder is the filter — a post with no translation simply does not
  // appear in the other locale's listing.
  for (const locale of locales.list) {
    eleventyConfig.addCollection(`posts_${locale.code}`, function (api) {
      return api
        .getFilteredByGlob(`src/content/blog/${locale.code}/*.md`)
        .filter((p) => p.data.draft !== true)
        .sort((a, b) => new Date(b.data.date) - new Date(a.data.date));
    });
  }

  // One content collection per locale: every page in that language's tree.
  // The blocks on a designed page read this rather than a hand-written list,
  // so adding a directory under content/<locale>/ adds a card — the same rule
  // that already governs the menu.
  for (const locale of locales.list) {
    eleventyConfig.addCollection(`content_${locale.code}`, function (api) {
      return api
        .getFilteredByGlob(`src/content/${locale.code}/**/*.md`)
        .filter((p) => p.data.draft !== true);
    });
  }

  // The page at a path inside a locale tree, e.g. "areas" or "about/contact".
  // Templates ask for a place in the content tree and get whatever URL that
  // place resolves to, so a localized slug never has to be written into a
  // template. Returns undefined when the page is not built, which is what lets
  // a caller leave a link out rather than emit one that 404s.
  eleventyConfig.addFilter("byPath", function (pages, relPath) {
    if (!pages || !relPath) return undefined;
    const tail = `/${relPath.replace(/^\/|\/$/g, "")}/`;
    return pages.find((p) => p.url && p.url.endsWith(tail));
  });

  // The pages one level below a parent URL — the children of a section, not
  // its whole subtree. Ordered by an optional `order` in front matter, then by
  // title, so a section can fix its own sequence without the template knowing
  // anything about it.
  eleventyConfig.addFilter("childrenOf", function (pages, parentUrl) {
    if (!pages || !parentUrl) return [];
    return pages
      .filter((p) => p.url && p.url !== parentUrl && p.url.startsWith(parentUrl))
      .filter((p) => !p.url.slice(parentUrl.length).replace(/\/$/, "").includes("/"))
      .sort(
        (a, b) =>
          (a.data.order || 0) - (b.data.order || 0) ||
          (a.data.title || "").localeCompare(b.data.title || "")
      );
  });

  // Pick the post flagged "featured" in the dashboard, else the newest.
  eleventyConfig.addFilter("pickFeatured", function (posts) {
    if (!posts || !posts.length) return null;
    return posts.find((p) => p.data.featured) || posts[0];
  });

  // Human-friendly date in the reader's language, e.g. "Jun 05, 2026" in
  // en-CA and "05 juin 2026" in fr-CA. Pass the page's BCP 47 tag explicitly
  // once pages know their own locale: {{ date | readableDate(locale.htmlLang) }}
  //
  // timeZone is pinned to the declared publication zone on purpose, for two
  // separate reasons:
  //
  //   1. Without a fixed zone, formatting happens in whatever zone the build
  //      machine is in, so any builder west of the stored instant shows posts
  //      a day early. The rendered day must not depend on who ran the build.
  //   2. Posts are stamped with the author's own offset, which may be Toronto
  //      or Kolkata. Pinning to one zone means the byline always reads as the
  //      studio's publication day rather than drifting with the author.
  //
  // Legacy date-only posts ("date: 2026-05-14") parse as UTC midnight, which
  // is 20:00 the previous day in Toronto — so those are normalised in
  // publicationInstant() below before they reach any formatter.
  eleventyConfig.addFilter("readableDate", function (d, lang) {
    if (!d) return "";
    return publicationInstant(d).toLocaleDateString(lang || DEFAULT_LANG, {
      year: "numeric",
      month: "short",
      day: "2-digit",
      timeZone: site.publicationTimeZone,
    });
  });

  // Machine-readable instant for <time datetime="...">, schema.org
  // datePublished and og:article:published_time. Full ISO 8601 with offset.
  eleventyConfig.addFilter("isoDate", function (d) {
    if (!d) return "";
    return publicationInstant(d).toISOString();
  });

  return {
    dir: { input: "src", includes: "_includes", output: "_site" },
    // .html pages are processed as Nunjucks so they can take a layout, a
    // locale and translated strings. Verified before flipping this: no page
    // contains a literal {{, {% or {# that Nunjucks would try to evaluate.
    htmlTemplateEngine: "njk",
    markdownTemplateEngine: "njk",
    templateFormats: ["html", "njk", "md"],
  };
};
