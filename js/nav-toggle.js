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

function initNavBuyDropdown() {
  const btn = document.getElementById("navBuyBtn");
  const menu = document.getElementById("navBuyMenu");
  if (!btn || !menu || btn._buyInit) return;

  function openMenu() {
    menu.classList.add("open");
    btn.setAttribute("aria-expanded", "true");
  }
  function closeMenu() {
    menu.classList.remove("open");
    btn.setAttribute("aria-expanded", "false");
  }

  btn.addEventListener("click", function (e) {
    e.stopPropagation();
    menu.classList.contains("open") ? closeMenu() : openMenu();
  });

  document.addEventListener("click", function (e) {
    if (!e.target.closest("#navBuyWrap")) closeMenu();
  });

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") closeMenu();
  });

  btn._buyInit = true;
}

// Initialize immediately in case header is present
try {
  initNavToggle();
  initNavBuyDropdown();
} catch (e) {
  /* ignore */
}

// Also expose for manual initialization after dynamic includes
window.initNavToggle = initNavToggle;
window.initNavBuyDropdown = initNavBuyDropdown;

// Re-initialize after dynamic header injection
document.addEventListener("includesLoaded", () => {
  initNavToggle();
  initNavBuyDropdown();
});
