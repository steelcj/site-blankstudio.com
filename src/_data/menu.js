// The primary menu, derived from the client's content tree rather than written
// out by hand in the nav and footer partials.
//
// The structure comes from the seed tree the client owns:
//
//   branding/<client>/content/en-ca/about/      ->  an "About" menu item
//   branding/<client>/content/en-ca/services/   ->  a "Services" menu item
//
// so rebranding the template for another site is still one directory: add a
// section there and it joins the menu, remove one and it leaves. A menu item is
// named for its DIRECTORY, not for the title of the page inside it — see
// humanize() below. The locale
// directories inside the seed are the same declaration one level up — en-ca/
// present means the site has English (Canada) content, fr-ca/ means it has
// French (Canada) content.
//
// Two things are deliberately NOT taken from the seed:
//
//   Where a menu item points. The build renders src/content/ and src/pages/,
//   never the seed (see spec--content-ingress: the seed is copied into the
//   live tree by an explicit step, and building never mutates content). So a
//   section links to the routed page that owns its slug, or to the live page
//   its index.md is an expression of — never to a path that only exists in the
//   seed, which would be a menu item leading to a 404. A section with no page
//   yet is reported at build time and left out.
//
//   Home and Contact. Those are designed landing pages under src/pages/, not
//   content sections, so they are pinned rather than discovered — otherwise a
//   client who has not seeded a section would end up with a menu of one item.
//
// Per-locale resolution happens by work identity, never by path arithmetic:
// the English section legal/ and the French section mentions-legales/ are the
// same work with different slugs, which is the mirrored model the multilingual
// vocabulary describes. Falling back to a same-named directory covers a
// section whose pages do not carry a sat:work yet.

const fs = require("fs");
const path = require("path");
const matter = require("gray-matter");

const locales = require("./locales.js");
const site = require("./site.json");
const { seedContentDir } = require("../../lib/branding.js");

const LIVE_CONTENT = path.join(__dirname, "..", "content");
const BUNDLE_DIR = path.join(__dirname, "..", "_locales");

// Used when the client's site.yaml declares no `nav` block — the menu the
// template ships with.
const DEFAULT_PINNED = { before: ["home"], after: ["contact"] };
const DEFAULT_ORDER = ["about", "services", "blog"];

// Sort ranks reserved for pinned pages, outside anything `order` produces.
const PINNED_FIRST = -1000;
const PINNED_LAST = 1000;

// ── reading the trees ────────────────────────────────────────────────────────

function subdirectories(dir) {
  if (!dir || !fs.existsSync(dir)) return [];
  return fs
    .readdirSync(dir, { withFileTypes: true })
    .filter((d) => d.isDirectory() && !d.name.startsWith("_"))
    .map((d) => d.name)
    .sort();
}

function frontMatter(file) {
  if (!fs.existsSync(file)) return null;
  return matter(fs.readFileSync(file, "utf8")).data;
}

function walk(dir) {
  const out = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) out.push(...walk(full));
    else if (entry.name.endsWith(".md")) out.push(full);
  }
  return out;
}

// Everything the live tree can answer about a page, keyed both ways: by work
// identity (for translations) and by locale + top-level section (for a section
// whose pages carry no work identity yet). Same URL derivation as
// _localeTree.js's permalink, so the two cannot drift.
function readLiveTree() {
  const byWork = {};
  const bySection = {};
  // Every URL the live tree publishes, so a pinned route can be checked
  // against what will actually be built.
  const urls = new Set();

  for (const locale of locales.list) {
    const root = path.join(LIVE_CONTENT, locale.code);
    bySection[locale.code] = {};
    if (!fs.existsSync(root)) continue;

    for (const file of walk(root)) {
      const data = frontMatter(file) || {};
      if (data.draft === true) continue;

      const rel = path.relative(root, file).replace(/\\/g, "/");
      const url = `/${locale.code}/${rel.replace(/\.md$/, "").replace(/(^|\/)index$/, "")}`
        .replace(/\/+$/, "")
        .concat("/");
      const entry = { url, title: data.title, nav: data.nav };
      urls.add(url);

      const work = data["sat:work"];
      if (work) {
        if (!byWork[work]) byWork[work] = {};
        byWork[work][locale.code] = entry;
      }

      // Only a section's own index.md stands in for the section.
      if (rel.endsWith("/index.md") && rel.split("/").length === 2) {
        bySection[locale.code][rel.split("/")[0]] = entry;
      }
    }
  }

  return { byWork, bySection, urls };
}

// The routeKey each designed page in src/pages/ claims. A pinned menu item is
// only real if something publishes its URL — a template here, or a content page
// in the live tree. Pinning by route name alone is what left a Contact link in
// the nav after contact.njk was deleted: the slug was still in the locale
// bundle, so the menu went on pointing at a page nobody builds any more.
function routedKeys() {
  const dir = path.join(__dirname, "..", "pages");
  if (!fs.existsSync(dir)) return new Set();
  const keys = new Set();
  for (const name of fs.readdirSync(dir)) {
    if (!/\.(njk|html|md)$/.test(name)) continue;
    const data = frontMatter(path.join(dir, name)) || {};
    if (data.routeKey) keys.add(data.routeKey);
  }
  return keys;
}

// The `routes` table of a locale, with the default locale's underneath so a
// bundle that has not been translated yet still resolves every key.
function routesFor(code) {
  const read = (c) => {
    const file = path.join(BUNDLE_DIR, `${c}.json`);
    if (!fs.existsSync(file)) return {};
    return JSON.parse(fs.readFileSync(file, "utf8")).routes || {};
  };
  return { ...read(locales.default), ...read(code) };
}

function urlForRoute(code, slug) {
  return `/${code}/${slug ? slug + "/" : ""}`;
}

// A directory name as a menu label: "about" -> "About", "case-studies" ->
// "Case Studies".
//
// The label is the DIRECTORY name, never the index.md `title`. A section's page
// is free to be titled "About Vishpala" or "What We Do and Why" — that is the
// page's own heading, written for someone already reading it. The menu names
// the place, and the place is the directory. Keeping the two apart means
// editing a page's headline cannot silently rewrite the navigation.
//
// `nav.label` in the section's index.md still wins, for the case where the
// directory name has to stay a URL slug but the menu should read differently.
function humanize(name) {
  return name
    .split(/[-_]+/)
    .filter(Boolean)
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(" ");
}

// The directory a live URL sits in: /fr-ca/mentions-legales/ -> mentions-legales
function dirOfUrl(url) {
  const parts = (url || "").split("/").filter(Boolean);
  return parts.length > 1 ? parts[parts.length - 1] : "";
}

// ── the sections ─────────────────────────────────────────────────────────────

// The client's sections, read from the seed's default-locale directory. The
// default locale defines the shape of the menu for every language: a section
// the client has not translated yet should still appear in French pointing at
// its French counterpart when one exists, rather than making each language
// invent its own menu from whatever happens to be translated.
//
// Falls back to the live tree when there is no seed at all, so a checkout with
// no branding/<client>/ still builds a sensible menu.
function readSections() {
  const seed = seedContentDir();
  const seedLocale = seed && path.join(seed, locales.default);
  const source =
    seedLocale && fs.existsSync(seedLocale)
      ? seedLocale
      : path.join(LIVE_CONTENT, locales.default);

  return subdirectories(source).map((name) => {
    const data = frontMatter(path.join(source, name, "index.md")) || {};
    const nav = data.nav || {};
    return {
      name,
      work: data["sat:work"],
      label: nav.label || humanize(name),
      hidden: nav.hidden === true,
    };
  });
}

// A section named for a route ("about") or for a route's slug in the default
// language ("free-audit" for the freeAudit route) is that page, not a new one.
function routeKeyFor(name, defaultRoutes) {
  if (name in defaultRoutes) return name;
  const hit = Object.entries(defaultRoutes).find(([, slug]) => slug === name);
  return hit ? hit[0] : null;
}

// ── assembly ─────────────────────────────────────────────────────────────────

const navConfig = site.nav || {};
const pinnedBefore = navConfig.before || DEFAULT_PINNED.before;
const pinnedAfter = navConfig.after || DEFAULT_PINNED.after;
const orderList = navConfig.order || DEFAULT_ORDER;

// Position in the client's declared order. A section is looked up by its own
// name first and by the route it stands in for second, so `order` can name
// either. Anything unlisted sorts after the listed items, alphabetically, so a
// newly seeded section appends to the menu rather than landing somewhere
// arbitrary.
function rankFor(...keys) {
  for (const key of keys) {
    const i = orderList.indexOf(key);
    if (i !== -1) return i;
  }
  return orderList.length;
}

function routeItem(key, code, routes, exists) {
  const slug = routes[key];
  if (slug === undefined) return null;
  if (!exists(key, urlForRoute(code, slug))) return null;
  return {
    key,
    routeKey: key,
    // Rendered through t.common.nav[labelKey], so a pinned page keeps the
    // translated label it already has in the locale bundles.
    labelKey: key,
    label: null,
    url: urlForRoute(code, slug),
    rank: rankFor(key),
  };
}

module.exports = function () {
  const { byWork, bySection, urls } = readLiveTree();
  const routed = routedKeys();
  const sections = readSections().filter((s) => !s.hidden);
  const defaultRoutes = routesFor(locales.default);
  const orphans = [];
  const menu = {};

  for (const locale of locales.list) {
    const code = locale.code;
    const routes = routesFor(code);
    const items = [];

    // Pinned pages bracket the sections: those declared `before` come first in
    // the order they are declared, those declared `after` come last, whatever
    // the client seeds in between. PINNED_FIRST/LAST put them outside the range
    // `order` can address rather than competing with it.
    const exists = (key, url) => routed.has(key) || urls.has(url);

    pinnedBefore.forEach((key, i) => {
      const item = routeItem(key, code, routes, exists);
      if (item) items.push({ ...item, rank: PINNED_FIRST + i });
    });

    for (const section of sections) {
      const routeKey = routeKeyFor(section.name, defaultRoutes);

      // A designed landing page owns this slug: link to it. Same existence
      // test as the pinned items — a section named for a route whose page is
      // not built falls through to the content lookup below rather than
      // producing a link to nothing.
      if (
        routeKey &&
        routes[routeKey] !== undefined &&
        exists(routeKey, urlForRoute(code, routes[routeKey]))
      ) {
        items.push({
          key: section.name,
          routeKey,
          labelKey: routeKey,
          label: section.label,
          url: urlForRoute(code, routes[routeKey]),
          rank: rankFor(section.name, routeKey),
        });
        continue;
      }

      // Otherwise the section is a content page. Prefer the expression of the
      // same work in this locale (localized slug and label), then a
      // same-named directory, then leave the section out of this language.
      const paired = section.work && byWork[section.work] && byWork[section.work][code];
      const sameName = bySection[code][section.name];
      const live = paired || sameName;

      if (!live) {
        orphans.push(`${section.name} (${code})`);
        continue;
      }

      items.push({
        key: section.name,
        routeKey: null,
        labelKey: null,
        // The localized directory names the place in that language:
        // mentions-legales/ reads "Mentions Legales" to a French reader, where
        // the English section is "Legal". The page's own title is not used.
        label:
          (live.nav && live.nav.label) ||
          humanize(dirOfUrl(live.url)) ||
          section.label,
        url: live.url,
        rank: rankFor(section.name),
      });
    }

    pinnedAfter.forEach((key, i) => {
      const item = routeItem(key, code, routes, exists);
      if (item) items.push({ ...item, rank: PINNED_LAST + i });
    });

    // Two sources can name the same destination — a pinned route and a section
    // of the same name. First one wins, which keeps the pinned spine stable.
    const seen = new Set();
    menu[code] = items
      .filter((item) => (seen.has(item.key) ? false : seen.add(item.key)))
      .sort((a, b) => a.rank - b.rank || a.key.localeCompare(b.key));
  }

  // A section the client has seeded but not yet ingressed has no page to point
  // at. Silence would look like the seed being ignored, so say so once.
  if (orphans.length) {
    console.log(
      `[menu] ${orphans.length} seeded section(s) have no page yet and are not ` +
        `in the menu: ${orphans.join(", ")}. Add the content under ` +
        `src/content/<locale>/ (or run ingress) to include them.`
    );
  }

  return menu;
};
