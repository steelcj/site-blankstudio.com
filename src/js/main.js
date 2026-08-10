/* ============================================================
   BLNK STUDIO - Home interactions
   ============================================================ */
(function () {
  "use strict";

  const prefersReduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- Screenshot / static mode (?shot) ---------- */
  const SHOT = location.search.includes("shot");
  if (SHOT) {
    const apply = () => {
      document.getElementById("loader")?.classList.add("is-done");
      const h = document.getElementById("hero");
      if (h) h.style.minHeight = "780px";
      document.querySelectorAll(".reveal").forEach((el) => el.classList.add("is-in"));
      document.getElementById("hero")?.classList.add("is-in");
      document.querySelector(".timeline")?.classList.add("is-in");
      document.querySelectorAll(".count").forEach((el) => {
        el.textContent = (el.dataset.prefix || "") + el.dataset.target + (el.dataset.suffix || "");
      });
    };
    document.addEventListener("DOMContentLoaded", apply);
    apply();
    return;
  }

  /* ---------- Loader ---------- */
  window.addEventListener("load", () => {
    const loader = document.getElementById("loader");
    if (!loader) return;
    setTimeout(() => loader.classList.add("is-done"), 700);
  });

  /* ---------- Current year ---------- */
  const year = document.getElementById("year");
  if (year) year.textContent = new Date().getFullYear();

  /* Language switcher: carry the current query string and hash across the
     switch. The Services page links to /contact/?package=Website%20Sprint and
     the contact page reads that param to pre-fill the brief — a plain href
     would drop it, and the lead would arrive unattributed. Locale-agnostic:
     it only copies whatever is already in the address bar. */
  var keep = document.querySelectorAll("a[data-keep-location]");
  if (keep.length && (location.search || location.hash)) {
    Array.prototype.forEach.call(keep, function (a) {
      a.setAttribute("href", a.getAttribute("href") + location.search + location.hash);
    });
  }

  /* ---------- Nav scroll state ---------- */
  const nav = document.getElementById("nav");
  const onScroll = () => {
    if (window.scrollY > 30) nav.classList.add("is-scrolled");
    else nav.classList.remove("is-scrolled");
  };
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  /* ---------- Mobile menu ---------- */
  const toggle = document.getElementById("navToggle");
  const mobile = document.getElementById("navMobile");
  if (toggle && mobile) {
    const close = () => {
      toggle.classList.remove("is-open");
      mobile.classList.remove("is-open");
      toggle.setAttribute("aria-expanded", "false");
    };
    toggle.addEventListener("click", () => {
      const open = toggle.classList.toggle("is-open");
      mobile.classList.toggle("is-open", open);
      toggle.setAttribute("aria-expanded", String(open));
    });
    mobile.querySelectorAll("a").forEach((a) => a.addEventListener("click", close));
  }

  /* ---------- Hero title reveal ---------- */
  const hero = document.getElementById("hero");
  if (hero) requestAnimationFrame(() => setTimeout(() => hero.classList.add("is-in"), 300));

  /* ---------- Scroll reveal (IntersectionObserver) ---------- */
  const revealEls = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && !prefersReduced) {
    const io = new IntersectionObserver(
      (entries, obs) => {
        entries.forEach((e) => {
          if (e.isIntersecting) {
            e.target.classList.add("is-in");
            obs.unobserve(e.target);
          }
        });
      },
      { threshold: 0.15, rootMargin: "0px 0px -8% 0px" }
    );
    revealEls.forEach((el) => io.observe(el));
  } else {
    revealEls.forEach((el) => el.classList.add("is-in"));
  }

  /* ---------- Timeline line draw ---------- */
  const timeline = document.querySelector(".timeline");
  if (timeline && "IntersectionObserver" in window) {
    const tio = new IntersectionObserver(
      (entries, obs) => {
        entries.forEach((e) => {
          if (e.isIntersecting) {
            e.target.classList.add("is-in");
            obs.unobserve(e.target);
          }
        });
      },
      { threshold: 0.3 }
    );
    tio.observe(timeline);
  }

  /* ---------- Animated counters ---------- */
  const counters = document.querySelectorAll(".count");
  const animateCount = (el) => {
    const target = parseFloat(el.dataset.target) || 0;
    const prefix = el.dataset.prefix || "";
    const suffix = el.dataset.suffix || "";
    const dur = 1600;
    const start = performance.now();
    const tick = (now) => {
      const p = Math.min((now - start) / dur, 1);
      const eased = 1 - Math.pow(1 - p, 3); // easeOutCubic
      el.textContent = prefix + Math.round(eased * target) + suffix;
      if (p < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  };
  if (counters.length && "IntersectionObserver" in window && !prefersReduced) {
    const cio = new IntersectionObserver(
      (entries, obs) => {
        entries.forEach((e) => {
          if (e.isIntersecting) {
            animateCount(e.target);
            obs.unobserve(e.target);
          }
        });
      },
      { threshold: 0.6 }
    );
    counters.forEach((c) => cio.observe(c));
  } else {
    counters.forEach((el) => {
      el.textContent = (el.dataset.prefix || "") + el.dataset.target + (el.dataset.suffix || "");
    });
  }

  /* ---------- Cursor glow (desktop, fine pointer only) ---------- */
  const glow = document.querySelector(".cursor-glow");
  if (glow && window.matchMedia("(pointer: fine)").matches && !prefersReduced) {
    let gx = 0, gy = 0, cx = 0, cy = 0;
    window.addEventListener("mousemove", (e) => {
      gx = e.clientX; gy = e.clientY;
      glow.style.opacity = "1";
    });
    const render = () => {
      cx += (gx - cx) * 0.12;
      cy += (gy - cy) * 0.12;
      glow.style.transform = `translate(${cx}px, ${cy}px) translate(-50%, -50%)`;
      requestAnimationFrame(render);
    };
    render();
  }

  /* ---------- Card spotlight (cursor follow) ---------- */
  if (window.matchMedia("(pointer: fine)").matches && !prefersReduced) {
    document.querySelectorAll(".spotlight").forEach((card) => {
      card.addEventListener("mousemove", (e) => {
        const r = card.getBoundingClientRect();
        card.style.setProperty("--mx", ((e.clientX - r.left) / r.width) * 100 + "%");
        card.style.setProperty("--my", ((e.clientY - r.top) / r.height) * 100 + "%");
      });
    });

    /* ---------- Magnetic buttons ---------- */
    document.querySelectorAll(".btn--primary, .btn--outline").forEach((btn) => {
      btn.addEventListener("mousemove", (e) => {
        const r = btn.getBoundingClientRect();
        const mx = e.clientX - r.left - r.width / 2;
        const my = e.clientY - r.top - r.height / 2;
        btn.style.transform = `translate(${mx * 0.18}px, ${my * 0.28}px)`;
      });
      btn.addEventListener("mouseleave", () => { btn.style.transform = ""; });
    });
  }

  /* ---------- Scroll-spy active nav ---------- */
  const navLinks = Array.from(document.querySelectorAll(".nav__links a"));
  const spyTargets = navLinks
    .map((a) => {
      const id = a.getAttribute("href");
      return id && id.startsWith("#") ? { a, el: document.querySelector(id) } : null;
    })
    .filter((x) => x && x.el);
  if (spyTargets.length && "IntersectionObserver" in window) {
    const spy = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) {
            const id = "#" + e.target.id;
            navLinks.forEach((a) =>
              a.classList.toggle("is-active", a.getAttribute("href") === id)
            );
          }
        });
      },
      { rootMargin: "-45% 0px -50% 0px" }
    );
    spyTargets.forEach((t) => spy.observe(t.el));
  }

  /* ---------- FAQ accordion ---------- */
  document.querySelectorAll(".faq-item").forEach((item) => {
    const btn = item.querySelector(".faq-q");
    const ans = item.querySelector(".faq-a");
    if (!btn || !ans) return;
    btn.addEventListener("click", () => {
      const open = item.classList.toggle("is-open");
      btn.setAttribute("aria-expanded", String(open));
      ans.style.maxHeight = open ? ans.scrollHeight + "px" : "";
    });
  });

  /* ---------- Subtle parallax on hero orbs ---------- */
  const orbs = document.querySelectorAll(".hero__orb");
  if (orbs.length && !prefersReduced) {
    window.addEventListener("scroll", () => {
      const y = window.scrollY;
      orbs.forEach((orb, i) => {
        const speed = i === 0 ? 0.15 : -0.1;
        orb.style.transform = `translateY(${y * speed}px)`;
      });
    }, { passive: true });
  }
})();
