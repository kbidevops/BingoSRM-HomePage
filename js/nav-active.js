document.addEventListener("DOMContentLoaded", () => {
  const rawPath = window.location.pathname.split("/").pop();
  const normalizedPath =
    rawPath === "" || rawPath === null ? "index.html" : rawPath;

  const navs = document.querySelectorAll("nav.for-pc");

  const normalizePath = (path) => {
    if (!path || path === "" || path === "index") return "index.html";
    return path;
  };

  const setActiveLink = (nav) => {
    const links = nav.querySelectorAll("a[href]");

    links.forEach((link) => {
      const underline = link.querySelector(".text-underlined");
      link.classList.remove("nav-active");
      if (underline) underline.classList.remove("is-active");

      try {
        const linkUrl = new URL(link.getAttribute("href"), window.location.href);
        const linkPath = normalizePath(linkUrl.pathname.split("/").pop());
        const current = normalizePath(normalizedPath);

        if (linkPath === current) {
          link.classList.add("nav-active");
          if (underline) underline.classList.add("is-active");
        }
      } catch (e) {
        // ignore invalid URLs
      }
    });
  };

  const updateSlider = (nav) => {
    const slider = nav.querySelector(".nav-slider");
    const active = nav.querySelector("a.nav-active");
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
});
