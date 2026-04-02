#!/usr/bin/env python3
"""Insert arch-diagram CSS before the Hero Carousel section in index.css."""
import sys, pathlib

CSS_FILE = pathlib.Path(__file__).parent.parent / "css" / "index.css"

ARCH_CSS = """\

/* ── ARCH DIAGRAM (Slide 1 right panel) ── */
.arch-diagram {
  background: linear-gradient(150deg, #0c1428 0%, #0f1e3a 60%, #091530 100%);
  border: 1px solid rgba(59, 162, 242, 0.3);
  border-radius: 16px;
  padding: 18px 16px 14px;
  position: relative;
  overflow: hidden;
  box-shadow:
    0 0 0 1px rgba(59, 162, 242, 0.08),
    0 16px 40px rgba(0, 0, 0, 0.18);
  opacity: 0;
  transform: translateY(16px);
  animation: archIn 0.6s 0.3s ease forwards;
}
@keyframes archIn {
  to { opacity: 1; transform: translateY(0); }
}
.arch-diagram::after {
  content: "";
  position: absolute;
  inset: 0;
  background:
    linear-gradient(rgba(59, 162, 242, 0.035) 1px, transparent 1px),
    linear-gradient(90deg, rgba(59, 162, 242, 0.035) 1px, transparent 1px);
  background-size: 20px 20px;
  pointer-events: none;
  z-index: 0;
}
.arch-diagram > * { position: relative; z-index: 1; }
.arch-title {
  text-align: center;
  font-size: 12.5px;
  font-weight: 700;
  color: #ddeeff;
  margin-bottom: 14px;
  letter-spacing: -0.2px;
  line-height: 1.4;
}
/* Layers */
.arch-layer {
  border-radius: 10px;
  padding: 10px 12px;
  border: 1px solid;
}
.arch-layer--ctrl {
  background: rgba(59, 162, 242, 0.09);
  border-color: rgba(59, 162, 242, 0.45);
  box-shadow: 0 0 14px rgba(59, 162, 242, 0.08) inset;
}
.arch-layer--analysis {
  background: rgba(59, 162, 242, 0.06);
  border-color: rgba(59, 162, 242, 0.35);
}
.arch-layer--infra {
  background: rgba(59, 162, 242, 0.05);
  border-color: rgba(59, 162, 242, 0.25);
}
.arch-layer-tag {
  font-size: 9.5px;
  font-weight: 700;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  color: var(--brand-cyan);
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  gap: 5px;
}
.arch-layer-tag::before {
  content: "";
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: currentColor;
  flex-shrink: 0;
}
.arch-tag--analysis { color: #6ee7b7; }
.arch-tag--infra { color: #93c5fd; }
/* Control layer */
.arch-layer-body {
  display: flex;
  align-items: center;
  gap: 10px;
}
.arch-chip-icon {
  width: 36px;
  height: 36px;
  flex-shrink: 0;
  color: var(--brand-cyan);
}
.arch-ctrl-info { flex: 1; min-width: 0; }
.arch-ctrl-name {
  font-size: 12.5px;
  font-weight: 700;
  color: #ffffff;
  line-height: 1.3;
}
.arch-ctrl-sub {
  font-size: 9.5px;
  color: rgba(255, 255, 255, 0.45);
  font-family: "IBM Plex Mono", monospace;
  margin-top: 2px;
}
.arch-stig-pill {
  flex-shrink: 0;
  padding: 4px 8px;
  background: rgba(251, 191, 36, 0.12);
  border: 1px solid rgba(251, 191, 36, 0.3);
  border-radius: 7px;
  font-size: 9px;
  font-weight: 700;
  color: #fbbf24;
  line-height: 1.35;
  text-align: center;
}
/* Connectors */
.arch-conn {
  display: flex;
  justify-content: center;
  padding: 4px 0;
}
.arch-conn-arrows {
  display: flex;
  align-items: center;
  gap: 8px;
}
.arch-conn-arrows svg {
  width: 10px;
  height: 20px;
  flex-shrink: 0;
}
.arch-conn-text {
  font-size: 9.5px;
  color: rgba(255, 255, 255, 0.38);
  text-align: center;
  line-height: 1.35;
  font-style: italic;
  max-width: 160px;
}
.arch-conn--up .arch-conn-arrows { gap: 16px; }
/* Analysis layer */
.arch-dual {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  gap: 6px;
}
.arch-dual-sep {
  font-size: 15px;
  color: var(--brand-cyan);
  opacity: 0.65;
  text-align: center;
  line-height: 1;
}
.arch-module {
  border-radius: 7px;
  padding: 7px 9px;
}
.arch-module--cce {
  background: rgba(34, 197, 94, 0.1);
  border: 1px solid rgba(34, 197, 94, 0.25);
}
.arch-module--cve {
  background: rgba(251, 191, 36, 0.08);
  border: 1px solid rgba(251, 191, 36, 0.22);
}
.arch-module-name {
  font-size: 10.5px;
  font-weight: 700;
  line-height: 1.25;
  margin-bottom: 3px;
}
.arch-module--cce .arch-module-name { color: #4ade80; }
.arch-module--cve .arch-module-name { color: #fbbf24; }
.arch-module-desc {
  font-size: 9px;
  color: rgba(255, 255, 255, 0.4);
  line-height: 1.4;
}
/* Infra layer */
.arch-infra-row {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  gap: 6px;
  align-items: start;
}
.arch-infra-divider {
  width: 1px;
  background: rgba(59, 162, 242, 0.2);
  align-self: stretch;
  margin: 2px 0;
}
.arch-infra-col { display: flex; flex-direction: column; }
.arch-infra-icons {
  display: flex;
  gap: 4px;
  margin-bottom: 5px;
}
.arch-infra-icons svg { width: 20px; height: 20px; }
.arch-infra-name {
  font-size: 10.5px;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: 2px;
}
.arch-infra-desc {
  font-size: 9px;
  color: rgba(255, 255, 255, 0.38);
  line-height: 1.4;
}
.arch-cloud-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 3px;
  margin-bottom: 5px;
}
.arch-cloud-tags span {
  font-size: 8.5px;
  font-weight: 600;
  padding: 1px 5px;
  border-radius: 3px;
  background: rgba(59, 162, 242, 0.15);
  color: var(--brand-cyan);
  border: 1px solid rgba(59, 162, 242, 0.22);
}
/* Effects bar */
.arch-effects {
  margin-top: 10px;
  padding: 8px 11px;
  background: rgba(59, 162, 242, 0.06);
  border: 1px solid rgba(59, 162, 242, 0.18);
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}
.arch-effects-title {
  font-size: 10px;
  font-weight: 700;
  color: var(--brand-cyan);
  letter-spacing: 0.4px;
  white-space: nowrap;
  flex-shrink: 0;
}
.arch-effect-items {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}
.arch-effect {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 10px;
  color: rgba(255, 255, 255, 0.6);
  white-space: nowrap;
}
.arch-effect-dot {
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background: var(--brand-cyan);
  flex-shrink: 0;
}
@media (prefers-reduced-motion: reduce) {
  .arch-diagram {
    animation: none;
    opacity: 1;
    transform: none;
  }
}
@media (max-width: 1100px) {
  .arch-diagram { max-width: 520px; }
}

"""

MARKER = "/* ── HERO CAROUSEL ── */"

def main():
    text = CSS_FILE.read_bytes().decode("utf-8")
    lf_text = text.replace("\r\n", "\n")

    if MARKER not in lf_text:
        print(f"ERROR: marker not found: {MARKER!r}", file=sys.stderr)
        sys.exit(1)

    new_text = lf_text.replace(MARKER, ARCH_CSS + MARKER, 1)
    CSS_FILE.write_bytes(new_text.replace("\n", "\r\n").encode("utf-8"))
    print("Done. CSS inserted.")

if __name__ == "__main__":
    main()
