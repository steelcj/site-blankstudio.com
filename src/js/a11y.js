/*
  Accessibility bar loader.

  Infusion's UI Options bundle is ~176 KB gzip against this site's own ~2 KB, so
  it is never on the critical path. This stub is a few hundred bytes and does
  two things:

    1. Loads Infusion on demand when the reader opens the bar.
    2. Loads it eagerly on pages where the reader has already saved
       preferences, so their settings apply immediately instead of the page
       rendering unstyled-for-them and then shifting.

  The marker for (2) is written alongside Infusion's own preferences cookie.
  Checking our own marker avoids parsing Infusion's cookie format and keeps the
  fast path to a single string test.

  Every visitor who never opens the bar pays nothing.
*/
(function () {
  "use strict";

  var VENDOR = "/assets/vendor/infusion";
  var MARKER = "blnk-a11y-used";

  var config = document.getElementById("a11y-config");
  if (!config) return;

  var locale = config.getAttribute("data-uio-locale") || "en_CA";
  var direction = config.getAttribute("data-direction") || "ltr";
  var pageLang = config.getAttribute("data-lang") || "en-CA";

  var loading = false;
  var loaded = false;

  function asset(tag, attrs) {
    var el = document.createElement(tag);
    for (var k in attrs) el.setAttribute(k, attrs[k]);
    document.head.appendChild(el);
    return el;
  }

  function styles() {
    [
      // Order matters: the base sheet first, matching the reference site.
      "fluid.css",
      "PrefsEditor.css",
      "SeparatedPanelPrefsEditor.css",
      "Enactors.css",
      "Contrast.css"
    ].forEach(function (f) {
      asset("link", { rel: "stylesheet", href: VENDOR + "/css/" + f });
    });
  }

  /* Self-voicing takes its language from the nearest [lang] attribute in the
     DOM (Orator.js), and base.njk sets <html lang> from the locale registry —
     so fr-CA pages are voiced as French without any extra configuration.

     What that cannot do is conjure a voice the OS does not have. With no
     French voice installed, browsers fall back to a default voice reading
     French text with English phonemes, which is worse than silence. Detect it
     and say so, rather than leaving it to be discovered by a French reader. */
  function checkVoice() {
    if (!window.speechSynthesis) {
      return console.warn("[a11y] no speechSynthesis in this browser; self-voicing unavailable");
    }
    var base = pageLang.split("-")[0].toLowerCase();
    var report = function () {
      var voices = speechSynthesis.getVoices() || [];
      if (!voices.length) return; // not populated yet; voiceschanged will re-fire
      var match = voices.filter(function (v) {
        return (v.lang || "").toLowerCase().indexOf(base) === 0;
      });
      if (!match.length) {
        console.warn(
          "[a11y] no '" + base + "' speech voice installed — self-voicing will " +
          "read " + pageLang + " text with a default voice and wrong phonemes"
        );
      }
    };
    // getVoices() is commonly empty on first call; the event is the reliable path.
    speechSynthesis.addEventListener("voiceschanged", report);
    report();
  }

  /* Self-voicing (fluid.prefs.speak) is DISABLED.
     ------------------------------------------------------------------
     Enabling it from the panel wedges the whole preferences editor, in both
     Brave and Firefox — the Show/Hide toggle stops responding and no further
     preference can be changed.

     It is also a trap rather than merely a bug: the setting persists in
     Infusion's preferences cookie, so on the next page load it is re-enacted
     immediately and breaks the panel again before the reader can turn it off.
     Recovery required clearing cookies by hand.

     Leaving it out of `preferences` means the enactor is never constructed, so
     a `speak: true` value already stored in someone's cookie is now inert —
     this both fixes the fault and releases anyone already stuck.

     Two contributing factors found, neither a complete explanation:
       - fluid.textToSpeech.isSupported() only checks that
         window.speechSynthesis exists, never that a voice is available, and
         nothing in the preferences framework gates on it. Brave's
         fingerprinting shield leaves the API present but returns no voices.
       - It fails in Firefox too, where voices ARE present, so the missing
         voice check is not the root cause.

     The reference implementation at idrc.ocadu.ca also omits this preference.
     Re-enable only behind a browser test that actually exercises speaking. */
  var ENABLE_SELF_VOICING = false;

  function voicesAvailable() {
    if (!window.speechSynthesis) return false;
    try {
      return (speechSynthesis.getVoices() || []).length > 0;
    } catch (e) {
      return false;
    }
  }

  function prefs() {
    var list = [
      "fluid.prefs.textSize",
      "fluid.prefs.lineSpace",
      "fluid.prefs.textFont",
      "fluid.prefs.contrast",
      "fluid.prefs.tableOfContents",
      "fluid.prefs.enhanceInputs"
    ];
    if (ENABLE_SELF_VOICING && voicesAvailable()) list.push("fluid.prefs.speak");
    return list;
  }

  function mount() {
    /* global fluid */
    if (typeof fluid === "undefined") {
      console.error("[a11y] infusion-uio.js loaded but `fluid` is undefined");
      return;
    }
    if (!fluid.uiOptions || !fluid.uiOptions.multilingual) {
      console.error("[a11y] fluid.uiOptions.multilingual missing from the bundle");
      return;
    }

    // Infusion reports component construction problems through its own logger;
    // without this, a failed mount is silent.
    if (fluid.setLogging) fluid.setLogging(true);

    var options = {
      // speak = self-voicing. It is NOT in fluid.uiOptions' default preference
      // list, so it has to be requested explicitly.
      preferences: prefs(),
      locale: locale,
      direction: direction,
      auxiliarySchema: {
        terms: {
          templatePrefix: VENDOR + "/html",
          messagePrefix: VENDOR + "/messages"
        },
        // These two default to paths relative to Infusion's own source tree
        // ("../../components/tableOfContents/html/..."), which 404 once the
        // package is served from /assets.
        "fluid.prefs.tableOfContents": {
          enactor: {
            tocTemplate: VENDOR + "/toc/TableOfContents.html",
            tocMessage: VENDOR + "/messages/tableOfContents-enactor.json"
          }
        }
      }
    };

    // Reveal BEFORE constructing. jQuery measures height as 0 inside a
    // display:none ancestor, and the sliding panel animates with slideDown()
    // — built while hidden, it opens from 0 to 0 and appears to do nothing.
    document.getElementById("uioPanel").classList.add("is-ready");

    try {
      window.__a11y = fluid.uiOptions.multilingual("#uioPanel", options);
      console.info("[a11y] accessibility bar ready");


    } catch (e) {
      console.error("[a11y] mount threw:", e && (e.stack || e.message || e));
      document.getElementById("uioPanel").classList.remove("is-ready");
      return;
    }

    try {
      document.cookie = MARKER + "=1; path=/; max-age=31536000; SameSite=Lax";
    } catch (e) {}
  }

  function load(then) {
    if (loaded) return then && then();
    if (loading) return;
    loading = true;
    styles();
    var s = document.createElement("script");
    s.src = VENDOR + "/infusion-uio.js";
    s.onerror = function () {
      loading = false;
      console.error("[a11y] failed to load " + s.src);
    };
    s.onload = function () {
      loaded = true;
      mount();
      trackHeight();
      checkVoice();
      if (then) then();
    };
    document.head.appendChild(s);
  }

  /* The nav is position:fixed at top:0, so an in-flow panel above it would be
     covered. Publishing the panel's measured height lets the nav offset itself
     instead — no dependency on Infusion's own classes or open/close events. */
  function trackHeight() {
    var panel = document.getElementById("uioPanel");
    if (!panel || typeof ResizeObserver === "undefined") return;

    /* This callback writes a custom property that drives .nav's `top`, so it
       mutates layout from inside a layout observer. Adjusting fonts or line
       spacing resizes the panel continuously, and Firefox responds to a
       ResizeObserver loop by dropping notifications — which can leave the
       observer, and handlers sharing the frame, wedged.

       Two guards: only write when the value actually changed, and defer the
       write out of the observation callback via requestAnimationFrame. */
    var last = null;
    var pending = false;

    new ResizeObserver(function () {
      if (pending) return;
      pending = true;
      requestAnimationFrame(function () {
        pending = false;
        var h = panel.offsetHeight;
        if (h === last) return;
        last = h;
        document.documentElement.style.setProperty("--a11y-panel-h", h + "px");
      });
    }).observe(panel);
  }

  /* Infusion's own panel bar has a Show/Hide control, but it only exists once
     the bundle has loaded. This button is the entry point before that, and
     should keep working afterwards rather than becoming inert — so the first
     click loads and opens, and later clicks toggle the same sliding panel. */
  function slidingPanel() {
    try {
      return window.__a11y.prefsEditorLoader.slidingPanel;
    } catch (e) {
      return null;
    }
  }


  function openPanel() {
    var sp = slidingPanel();
    if (!sp) return;
    if (!sp.model.isShowing) sp.showPanel();
  }

  // Dump model-vs-DOM state. The sliding panel animates off a model change, so
  // an animation interrupted mid-flight — which a preference change resizing
  // the panel will do — can leave the two disagreeing, and the toggle then
  // looks dead. Callable from the console as __a11yState().
  window.__a11yState = function () {
    var sp = slidingPanel();
    var panel = document.querySelector(".flc-slidingPanel-panel");
    var cs = panel && getComputedStyle(panel);
    var state = {
      modelIsShowing: sp ? sp.model.isShowing : "(no slidingPanel)",
      panelDisplay: cs && cs.display,
      panelHeight: panel && panel.offsetHeight,
      panelInlineStyle: panel && panel.getAttribute("style"),
      jqAnimating: !!(window.jQuery && panel && window.jQuery(panel).is(":animated")),
      visibleToggles: [].slice.call(document.querySelectorAll(".flc-slidingPanel-toggleButton"))
        .filter(function (b) { return b.offsetParent !== null; }).length,
      navTop: getComputedStyle(document.getElementById("nav")).top
    };
    console.log("[a11y] state:", state);
    return state;
  };

  window.addEventListener("error", function (e) {
    console.error("[a11y] uncaught error:", e.message, e.filename + ":" + e.lineno);
  });

  /* There is no separate launcher. The scaffold's own Show/Hide button is the
     entry point: it is inert until Infusion loads, so this captures the first
     click, loads the bundle, and opens the panel. Infusion binds its own
     handler to the same button when it constructs and owns every click after
     that — hence the `loaded` guard, and the capture phase so this runs first. */
  document.addEventListener("click", function (ev) {
    if (loaded || loading) return;
    if (!ev.target.closest || !ev.target.closest(".flc-slidingPanel-toggleButton")) return;
    ev.preventDefault();
    load(function () { setTimeout(openPanel, 0); });
  }, true);

  // Returning reader who already uses the bar: load so their saved settings
  // apply immediately, without waiting for a click. The panel stays closed —
  // applying preferences is not the same as asking for the editor.
  if (document.cookie.indexOf(MARKER + "=1") !== -1) load();
})();
