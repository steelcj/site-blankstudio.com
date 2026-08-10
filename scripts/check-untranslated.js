#!/usr/bin/env node
// Reports text that renders identically in a non-default locale and the
// default one.
//
// The missing-key guard in _data/i18n.js catches strings absent from a bundle.
// It cannot catch a string that was never extracted at all — one still
// hardcoded in a template renders the same English on every locale and looks
// perfectly translated to the build. This compares the rendered output instead,
// which is the only place that mistake is visible.
//
// Run after a build:  node scripts/check-untranslated.js

const fs = require("fs");
const path = require("path");
const locales = require("../src/_data/locales.js");
const site = require("../src/_data/site.json");

const SITE = path.join(__dirname, "..", "_site");

// Text that is legitimately identical across locales: brand assets, proper
// nouns, and technical tokens that are not translated.
const ALLOWED = new Set([
  "BLNK Studio",
  "Strategy. Design. Impact.",
  "BLNK Studio - Strategy. Design. Impact.",
  "WhatsApp",
  "Instagram",
  "SEO",
  "Biryani By Kilo", "Fenesta", "Goila Butter Chicken",
  "My Home", "Naisha Vasandani Couture", "Ziggy",
  "v1.0", "01 / 01", "Meta (Facebook/Instagram)",
]);

const MIN_WORDS = 3; // shorter runs are too noisy to be useful

function textNodes(html) {
  return html
    .replace(/<(script|style)\b[^>]*>[\s\S]*?<\/\1>/gi, " ")
    .split(/<[^>]+>/)
    .map((t) => t.replace(/\s+/g, " ").trim())
    .filter(Boolean);
}

function pagesFor(code) {
  const dir = path.join(SITE, code);
  if (!fs.existsSync(dir)) return [];
  const out = [];
  (function walk(d) {
    for (const e of fs.readdirSync(d, { withFileTypes: true })) {
      const p = path.join(d, e.name);
      if (e.isDirectory()) walk(p);
      else if (e.name.endsWith(".html")) out.push(p);
    }
  })(dir);
  return out;
}

const def = locales.default;
const defaultText = new Set();
for (const f of pagesFor(def)) {
  for (const t of textNodes(fs.readFileSync(f, "utf8"))) defaultText.add(t);
}

let findings = 0;
for (const locale of locales.real) {
  if (locale.code === def) continue;

  const seen = new Set();
  for (const f of pagesFor(locale.code)) {
    for (const t of textNodes(fs.readFileSync(f, "utf8"))) {
      if (ALLOWED.has(t)) continue;
      // Strings with no letters are numbering, dates or counters — "01 / 07",
      // "+25%". Identical across locales by design.
      if (!/\p{L}{2}/u.test(t)) continue;
      // Contact details come from _data/site.json and are the same everywhere.
      if (Object.values(site.contact).some((v) => t.includes(v))) continue;
      if (t.split(" ").length < MIN_WORDS) continue;
      if (!defaultText.has(t)) continue;
      if (seen.has(t)) continue;
      seen.add(t);
      console.log(`  [${locale.code}] identical to ${def}: ${JSON.stringify(t.slice(0, 90))}`);
      findings++;
    }
  }
}

if (findings === 0) {
  console.log("  no untranslated text found in any non-default locale");
}
process.exit(findings > 0 ? 1 : 0);
