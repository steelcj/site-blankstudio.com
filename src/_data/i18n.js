// Loads the per-locale string bundles from src/_locales/ and exposes them as
// the global `i18n` data key, shaped { en: {...}, fr: {...} }.
//
// Why the bundles live in src/_locales/ and not src/_data/i18n/:
// Eleventy auto-namespaces subdirectories of _data/, so _data/i18n/en.json
// would already claim the `i18n.en` key — colliding with this file's own
// `i18n` key. Keeping the raw bundles outside _data/ leaves one owner for the
// key. JSON is not in templateFormats, so nothing in _locales/ is rendered or
// copied to the output.
//
// Every non-default locale is deep-merged over the default bundle, so a key
// that has not been translated yet renders in the default language rather
// than as an empty string. Keys that fall back are reported at build time.
// Phase 6 turns that report into a build failure.

const fs = require("fs");
const path = require("path");
const locales = require("./locales.js");

const BUNDLE_DIR = path.join(__dirname, "..", "_locales");

function isPlainObject(value) {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

// Values from `over` win; nested objects merge rather than replace. Arrays are
// treated as whole values so a translated list never half-inherits.
function deepMerge(base, over) {
  const out = { ...base };
  for (const [key, value] of Object.entries(over)) {
    out[key] =
      isPlainObject(value) && isPlainObject(base[key])
        ? deepMerge(base[key], value)
        : value;
  }
  return out;
}

// Dotted paths present in `base` but absent from `over`.
function missingKeys(base, over, prefix = "") {
  const missing = [];
  for (const [key, value] of Object.entries(base)) {
    const dotted = prefix ? `${prefix}.${key}` : key;
    if (!(key in over)) {
      missing.push(dotted);
    } else if (isPlainObject(value) && isPlainObject(over[key])) {
      missing.push(...missingKeys(value, over[key], dotted));
    }
  }
  return missing;
}


// Latin letters mapped to accented look-alikes. Still readable, but visibly
// not English, so a string that renders plain is one the extraction missed.
const ACCENT = {
  a:"á",b:"ƀ",c:"ç",d:"ð",e:"é",f:"ƒ",g:"ĝ",h:"ĥ",i:"í",j:"ĵ",k:"ķ",l:"ļ",m:"ɱ",
  n:"ñ",o:"ó",p:"þ",q:"ǫ",r:"ŕ",s:"š",t:"ţ",u:"ú",v:"ṽ",w:"ŵ",x:"ẋ",y:"ý",z:"ž",
  A:"Á",B:"Ɓ",C:"Ç",D:"Ð",E:"É",F:"Ƒ",G:"Ĝ",H:"Ĥ",I:"Í",J:"Ĵ",K:"Ķ",L:"Ļ",M:"Ṁ",
  N:"Ñ",O:"Ó",P:"Þ",Q:"Ǫ",R:"Ŕ",S:"Š",T:"Ţ",U:"Ú",V:"Ṽ",W:"Ŵ",X:"Ẋ",Y:"Ý",Z:"Ž",
};

// HTML tags, entities and {placeholders} pass through untouched — accenting
// them would corrupt the markup or break the {phone} substitution.
const PASSTHROUGH = /(<[^>]+>|&[a-zA-Z#0-9]+;|\{[a-zA-Z]+\})/g;
// Anchored and non-global: .test() on a /g regex advances lastIndex between
// calls, so reusing PASSTHROUGH for the per-part check would give results that
// depend on the previous part's length.
const IS_PASSTHROUGH = /^(<[^>]+>|&[a-zA-Z#0-9]+;|\{[a-zA-Z]+\})$/;

function pseudoString(value) {
  const accented = value
    .split(PASSTHROUGH)
    .map((part) =>
      IS_PASSTHROUGH.test(part) ? part : part.replace(/[a-zA-Z]/g, (c) => ACCENT[c] || c)
    )
    .join("");

  // Pad ~30% to model translation expansion. Brackets make truncation obvious.
  const letters = value.replace(PASSTHROUGH, "").length;
  const pad = "·".repeat(Math.max(1, Math.round(letters * 0.3)));
  return `[${accented} ${pad}]`;
}

function pseudoBundle(source) {
  // Arrays must stay arrays — hero titleLines is one, and turning it into an
  // object would break the {% for %} that renders it.
  if (Array.isArray(source)) return source.map(pseudoString);
  const out = {};
  for (const [key, value] of Object.entries(source)) {
    if (typeof value === "object" && value !== null) out[key] = pseudoBundle(value);
    else if (typeof value === "string") out[key] = pseudoString(value);
    else out[key] = value;
  }
  return out;
}


function readBundle(code) {
  const file = path.join(BUNDLE_DIR, `${code}.json`);
  if (!fs.existsSync(file)) return {};
  return JSON.parse(fs.readFileSync(file, "utf8"));
}

module.exports = function () {
  const fallback = readBundle(locales.default);
  const bundles = {};

  for (const locale of locales.list) {
    // Pseudo-locales are generated from the default bundle rather than read
    // from disk. `routes` is restored untouched afterwards: those values are
    // URL slugs, and accenting them would produce permalinks that 404.
    if (locale.pseudo) {
      const generated = pseudoBundle(fallback);
      generated.routes = fallback.routes;
      delete generated._draft;
      bundles[locale.code] = generated;
      continue;
    }

    const own = readBundle(locale.code);

    if (locale.code === locales.default) {
      bundles[locale.code] = own;
      continue;
    }

    bundles[locale.code] = deepMerge(fallback, own);

    // A bundle carrying _draft is machine-drafted and has not been through a
    // translator. Warn on every build so it cannot be shipped by accident.
    if (own._draft) {
      console.warn(`[i18n] WARNING ${locale.code} is DRAFT — ${own._draft}`);
    }

    const missing = missingKeys(fallback, own);
    if (missing.length) {
      const detail =
        `${locale.code} is missing ${missing.length} key(s) present in ` +
        `"${locales.default}": ${missing.join(", ")}`;

      // A production build must not ship a locale with silent English
      // fallbacks. During serve/watch it is only a warning, so a translator
      // can work through the bundle without the site refusing to build.
      if (process.env.ELEVENTY_RUN_MODE === "build") {
        throw new Error(`[i18n] ${detail}`);
      }
      console.log(`[i18n] ${detail}`);
    }
  }

  return bundles;
};
