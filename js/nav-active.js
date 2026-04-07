function initNavs() {
  // Use pathname without trailing slash, then take last segment.
  const rawPath = window.location.pathname.replace(/\/$/, "").split("/").pop();
  const normalizedPath =
    rawPath === "" || rawPath === null ? "index.html" : rawPath;

  // debug
  try {
  } catch (e) {}

  const navs = document.querySelectorAll(".nav-menu");

  const normalizePath = (path) => {
    if (!path) return "index";
    // strip any leading/trailing slashes
    let p = String(path).replace(/^\//, "").replace(/\/$/, "");
    // strip .html extension
    if (p.toLowerCase().endsWith(".html")) p = p.slice(0, -5);
    if (p === "" || p.toLowerCase() === "index") return "index";
    return p;
  };

  const setActiveLink = (nav) => {
    const links = nav.querySelectorAll("a[href]");

    try {
    } catch (e) {}

    links.forEach((link) => {
      // skip purchase / external CTA links
      if (link.classList.contains("nav-buy")) return;
      if (link.target && link.target === "_blank") return;

      const underline = link.querySelector(".text-underlined");
      link.classList.remove("nav-active");
      link.classList.remove("active");
      if (underline) underline.classList.remove("is-active");

      try {
        const linkUrl = new URL(
          link.getAttribute("href"),
          window.location.href,
        );
        // remove trailing slash so split/pop returns the actual segment
        const linkSegment = linkUrl.pathname
          .replace(/\/$/, "")
          .split("/")
          .pop();
        const linkPath = normalizePath(linkSegment);
        const current = normalizePath(normalizedPath);
        if (linkPath === current) {
          link.classList.add("nav-active");
          link.classList.add("active");
          if (underline) underline.classList.add("is-active");
          try {
          } catch (e) {}
        } else {
          try {
          } catch (e) {}
        }
      } catch (e) {
        // ignore invalid URLs
      }
    });
  };

  const updateSlider = (nav) => {
    const slider = nav.querySelector(".nav-slider");
    const active = nav.querySelector("a.nav-active, a.active");
    if (!slider || !active) return;

    const navRect = nav.getBoundingClientRect();
    const activeRect = active.getBoundingClientRect();

    const left = activeRect.left - navRect.left + nav.scrollLeft;
    slider.style.width = `${activeRect.width}px`;
    slider.style.transform = `translateX(${left}px)`;
  };

  const ensureSlider = (nav) => {
    let slider = nav.querySelector(".nav-slider");
    if (!slider) {
      slider = document.createElement("div");
      slider.className = "nav-slider";
      nav.appendChild(slider);
    }
    return slider;
  };

  const initNav = (nav) => {
    setActiveLink(nav);
    ensureSlider(nav);
    updateSlider(nav);

    // Update on resize so the slider stays aligned
    window.addEventListener("resize", () => updateSlider(nav));
  };

  navs.forEach((nav) => initNav(nav));
}

// Run once DOM is ready in case navs are present in the initial HTML
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initNavs);
} else {
  initNavs();
}

// If header/footer are injected after load, listen for the includesLoaded event
document.addEventListener("includesLoaded", () => {
  try {
  } catch (e) {}
  initNavs();
  // ensure nav-toggle behavior is available after dynamic header include
  try {
    // If nav-toggle is already available, initialize it; otherwise reload and execute it
    if (window.initNavToggle) {
      window.initNavToggle();
    } else {
      // remove any existing script tags with same src (they may have been injected via innerHTML
      document
        .querySelectorAll('script[src="/js/nav-toggle.js"]')
        .forEach((el) => el.remove());
      const s = document.createElement("script");
      s.src = "/js/nav-toggle.js";
      s.defer = true;
      s.onload = function () {
        if (window.initNavToggle) window.initNavToggle();
        try {
          if (window.ensureFloatingToggle) window.ensureFloatingToggle();
        } catch (e) {}
      };
      document.body.appendChild(s);
    }
  } catch (e) {
    /* ignore */
  }
});

// also expose for manual calls
window.initNavs = initNavs;

// Fallback: if no nav-menu exists yet, observe the DOM and initialize when it's added
if (document.querySelectorAll(".nav-menu").length === 0) {
  const obs = new MutationObserver((mutations, observer) => {
    if (document.querySelectorAll(".nav-menu").length > 0) {
      try {
      } catch (e) {}
      try {
        initNavs();
      } catch (e) {
        /* ignore */
      }
      observer.disconnect();
    }
  });
  obs.observe(document.documentElement || document.body, {
    childList: true,
    subtree: true,
  });
}
