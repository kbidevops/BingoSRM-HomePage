// Shared cursor script — mirror behavior from index.html
(function () {
  const dot = document.getElementById("cursorDot");
  const ring = document.getElementById("cursorRing");
  if (!dot || !ring) return;

  let mx = 0,
    my = 0,
    rx = 0,
    ry = 0;

  document.addEventListener("mousemove", (e) => {
    mx = e.clientX;
    my = e.clientY;
  });

  (function tick() {
    rx += (mx - rx) * 0.12;
    ry += (my - ry) * 0.12;
    dot.style.left = mx + "px";
    dot.style.top = my + "px";
    ring.style.left = rx + "px";
    ring.style.top = ry + "px";
    requestAnimationFrame(tick);
  })();

  // Hover enlarge targets — reuse same selectors as index for consistent UX
  const hoverTargets = document.querySelectorAll(
    "a,button,.chip:not(.empty),.bs-sol,.stat-cell,.about-cell,.partner-card,.svc-card,.plat,.tl-item,.hero-dot,.hero-arrow,.toc-link,.client-logo",
  );
  hoverTargets.forEach((el) => {
    el.addEventListener("mouseenter", () => {
      ring.style.width = "44px";
      ring.style.height = "44px";
      ring.style.borderColor = "rgba(200,0,30,0.5)";
    });
    el.addEventListener("mouseleave", () => {
      ring.style.width = "28px";
      ring.style.height = "28px";
      ring.style.borderColor = "rgba(200,0,30,0.35)";
    });
  });
})();
