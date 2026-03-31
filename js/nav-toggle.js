function initNavToggle() {
  const toggle = document.querySelector(".nav-toggle");
  const navMenu = document.querySelector(".nav-menu");
  if (!toggle || !navMenu) return;
  try {
    console.debug("initNavToggle: found toggle and menu");
  } catch (e) {}

  function openNav() {
    document.body.classList.add("nav-open");
    toggle.setAttribute("aria-expanded", "true");
    toggle.setAttribute("aria-label", "메뉴 닫기");
    const first = navMenu.querySelector("a");
    if (first) first.focus();
  }

  function closeNav() {
    document.body.classList.remove("nav-open");
    toggle.setAttribute("aria-expanded", "false");
    toggle.setAttribute("aria-label", "메뉴 열기");
    toggle.focus();
  }

  // avoid attaching multiple listeners
  if (!toggle._navInit) {
    toggle.addEventListener("click", function () {
      const expanded = toggle.getAttribute("aria-expanded") === "true";
      if (expanded) closeNav();
      else openNav();
    });

    document.addEventListener("click", function (e) {
      if (!document.body.classList.contains("nav-open")) return;
      if (e.target.closest(".nav")) return;
      closeNav();
    });

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && document.body.classList.contains("nav-open")) {
        closeNav();
      }
    });

    toggle._navInit = true;
  }
}

// Initialize immediately in case header is present
try {
  initNavToggle();
} catch (e) {
  /* ignore */
}

// Also expose for manual initialization after dynamic includes
window.initNavToggle = initNavToggle;

// If the toggle is not visible (clipped or hidden), create a floating fallback
function ensureFloatingToggle() {
  const toggle = document.querySelector(".nav-toggle");
  if (!toggle) return;
  // Only create fallback on small screens (mobile breakpoint)
  if (window.innerWidth > 980) {
    const existing = document.querySelector('.nav-toggle-floating');
    if (existing) existing.remove();
    return;
  }
  const rect = toggle.getBoundingClientRect();
  const elAtPoint = document.elementFromPoint(rect.left + 1, rect.top + 1);
  const isVisible =
    rect.width > 0 &&
    rect.height > 0 &&
    elAtPoint &&
    !!elAtPoint.closest &&
    elAtPoint.closest(".nav-toggle");
  if (isVisible) return;

  if (document.querySelector(".nav-toggle-floating")) return;
  const floatBtn = document.createElement("button");
  floatBtn.className = "nav-toggle nav-toggle-floating";
  floatBtn.setAttribute(
    "aria-expanded",
    toggle.getAttribute("aria-expanded") || "false",
  );
  floatBtn.setAttribute(
    "aria-label",
    toggle.getAttribute("aria-label") || "메뉴 열기",
  );
  floatBtn.innerText = "☰";
  Object.assign(floatBtn.style, {
    position: "fixed",
    right: "12px",
    top: "12px",
    zIndex: 10020,
    display: "inline-flex",
    background: "transparent",
    border: "1px solid rgba(0,0,0,0.08)",
    padding: "8px 10px",
    borderRadius: "6px",
    fontSize: "18px",
    cursor: "pointer",
  });
  floatBtn.addEventListener("click", () => toggle.click());
  try {
    console.debug("ensureFloatingToggle: added floating toggle");
  } catch (e) {}
  document.body.appendChild(floatBtn);
}

// run a check after includes load and after a short delay
document.addEventListener("includesLoaded", () => {
  setTimeout(ensureFloatingToggle, 120);
  // also try on resize
  window.addEventListener("resize", () =>
    setTimeout(ensureFloatingToggle, 120),
  );
});
