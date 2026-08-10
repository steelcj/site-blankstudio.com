// The locale registry.
//
// `code` is the URL segment and is lowercase, because paths are case-sensitive
// and lowercase is the convention: /en-ca/about/. `htmlLang` is the BCP 47 tag
// whose canonical form uppercases the region, and it feeds <html lang>,
// hreflang, Intl date formatting and speech synthesis: en-CA.
//
// `dir` is carried from day one even though both shipping locales are LTR.
// That is what makes a right-to-left language a config entry later rather than
// a rewrite, and it is what the ar-XB pseudo-locale below exercises.

// Font stylesheet per locale. The site self-hosts its webfonts: fonts.yaml at
// the repo root declares the families/weights, scripts/fetch-fonts.py downloads
// the woff2 into src/assets/fonts/ and generates this stylesheet. No request to
// Google on the critical path, and no outage exposure.
//
// Inter / Inter Tight / Space Mono cover Latin only — no Devanagari, Arabic or
// CJK glyphs — so a future non-Latin locale points `fonts` at its own generated
// stylesheet rather than editing every page.
const LATIN = "/css/fonts.css";

const REAL = [
  { code: "en-ca", htmlLang: "en-CA", dir: "ltr", label: "English", fonts: LATIN, uioLocale: "en_CA" },
  { code: "fr-ca", htmlLang: "fr-CA", dir: "ltr", label: "Français", fonts: LATIN, uioLocale: "fr" },
];

// Build-only test locales, never shipped. Enabled with PSEUDO=1.
//
//   en-xa  Accented and padded ~30%. Two bugs at once: any string that renders
//          as plain English was missed during extraction, and any layout that
//          overflows here will overflow in French — measured at +23% overall,
//          with nav labels up to +75%.
//   ar-xb  Same text, dir="rtl". Proves the logical-property sweep actually
//          works without committing to Arabic content.
//
// Both are noindex, excluded from the sitemap, and excluded from hreflang and
// the language switcher.
const PSEUDO = [
  { code: "en-xa", htmlLang: "en-XA", dir: "ltr", label: "Pseudo LTR", pseudo: "accent", fonts: LATIN, uioLocale: "en_CA" },
  { code: "ar-xb", htmlLang: "ar-XB", dir: "rtl", label: "Pseudo RTL", pseudo: "accent", fonts: LATIN, uioLocale: "en_CA" },
];

const enabled = process.env.PSEUDO === "1";

module.exports = {
  default: "en-ca",
  real: REAL,
  list: enabled ? [...REAL, ...PSEUDO] : REAL,
};
