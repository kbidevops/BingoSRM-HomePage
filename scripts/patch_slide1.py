#!/usr/bin/env python3
"""Replace the zt-cards section in slide 1 with the arch-diagram."""
import re, sys, pathlib

HTML_FILE = pathlib.Path(__file__).parent.parent / "index.html"

ARCH_DIAGRAM = """\
            <div class="arch-diagram">
              <div class="arch-title">BingoCVM 제로트러스트 통합 진단 아키텍처</div>

              <!-- Control Layer (제어층) -->
              <div class="arch-layer arch-layer--ctrl">
                <div class="arch-layer-tag">제어층</div>
                <div class="arch-layer-body">
                  <svg class="arch-chip-icon" viewBox="0 0 40 40" fill="none">
                    <rect x="6" y="6" width="28" height="28" rx="5" stroke="currentColor" stroke-width="1.5" fill="rgba(59,162,242,0.12)"/>
                    <rect x="11" y="11" width="18" height="18" rx="2.5" stroke="currentColor" stroke-width="1" fill="rgba(59,162,242,0.06)" stroke-dasharray="3 2"/>
                    <text x="20" y="25" text-anchor="middle" fill="currentColor" font-size="11" font-weight="bold" font-family="sans-serif">AI</text>
                    <line x1="6" y1="15" x2="1" y2="15" stroke="currentColor" stroke-width="1.2"/>
                    <line x1="6" y1="25" x2="1" y2="25" stroke="currentColor" stroke-width="1.2"/>
                    <line x1="34" y1="15" x2="39" y2="15" stroke="currentColor" stroke-width="1.2"/>
                    <line x1="34" y1="25" x2="39" y2="25" stroke="currentColor" stroke-width="1.2"/>
                    <line x1="15" y1="6" x2="15" y2="1" stroke="currentColor" stroke-width="1.2"/>
                    <line x1="25" y1="6" x2="25" y2="1" stroke="currentColor" stroke-width="1.2"/>
                    <line x1="15" y1="34" x2="15" y2="39" stroke="currentColor" stroke-width="1.2"/>
                    <line x1="25" y1="34" x2="25" y2="39" stroke="currentColor" stroke-width="1.2"/>
                  </svg>
                  <div class="arch-ctrl-info">
                    <div class="arch-ctrl-name">BingoCVM AI 엔진</div>
                    <div class="arch-ctrl-sub">Zero Trust Policy Engine</div>
                  </div>
                  <div class="arch-stig-pill">STIG 가이드<br />학습 AI</div>
                </div>
              </div>

              <!-- Connector: ctrl ↔ analysis -->
              <div class="arch-conn">
                <div class="arch-conn-arrows">
                  <svg viewBox="0 0 8 16" fill="none"><path d="M4 0v12M1 9l3 4 3-4" stroke="#3ba2f2" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                  <span class="arch-conn-text">실시간 진단 명령 및 제로트러스트 정책 적용</span>
                  <svg viewBox="0 0 8 16" fill="none"><path d="M4 16V4M1 7l3-4 3 4" stroke="#3ba2f2" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                </div>
              </div>

              <!-- Analysis Layer (분석층) -->
              <div class="arch-layer arch-layer--analysis">
                <div class="arch-layer-tag arch-tag--analysis">분석층 | CCE + CVE 통합 모듈</div>
                <div class="arch-dual">
                  <div class="arch-module arch-module--cce">
                    <div class="arch-module-name">CCE (설정 취약점)</div>
                    <div class="arch-module-desc">시스템 설정 오류, 컴플라이언스 미준수 진단</div>
                  </div>
                  <div class="arch-dual-sep">&#8644;</div>
                  <div class="arch-module arch-module--cve">
                    <div class="arch-module-name">CVE (알려진 취약점)</div>
                    <div class="arch-module-desc">글로벌 보안 약점, OS/SW 취약점 실시간 매핑</div>
                  </div>
                </div>
              </div>

              <!-- Connector: infra → analysis -->
              <div class="arch-conn arch-conn--up">
                <div class="arch-conn-arrows">
                  <svg viewBox="0 0 8 16" fill="none"><path d="M4 16V4M1 7l3-4 3 4" stroke="#3ba2f2" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                  <svg viewBox="0 0 8 16" fill="none"><path d="M4 16V4M1 7l3-4 3 4" stroke="#3ba2f2" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                </div>
              </div>

              <!-- Target Layer (대상층) -->
              <div class="arch-layer arch-layer--infra">
                <div class="arch-layer-tag arch-tag--infra">대상층 | 하이브리드 인프라</div>
                <div class="arch-infra-row">
                  <div class="arch-infra-col">
                    <div class="arch-infra-icons">
                      <svg viewBox="0 0 20 20" fill="none"><rect x="1" y="2" width="18" height="10" rx="1.5" stroke="#7a90b0" stroke-width="1.2"/><rect x="1" y="14" width="18" height="5" rx="1.5" stroke="#7a90b0" stroke-width="1.2"/><circle cx="15" cy="16.5" r="1" fill="#7a90b0"/></svg>
                      <svg viewBox="0 0 20 20" fill="none"><rect x="2" y="3" width="16" height="14" rx="1.5" stroke="#7a90b0" stroke-width="1.2"/><line x1="6" y1="9" x2="14" y2="9" stroke="#7a90b0" stroke-width="1"/><line x1="6" y1="12" x2="14" y2="12" stroke="#7a90b0" stroke-width="1"/></svg>
                    </div>
                    <div class="arch-infra-name">온프레미스</div>
                    <div class="arch-infra-desc">Legacy 서버 · 네트워크 · 데이터센터</div>
                  </div>
                  <div class="arch-infra-divider"></div>
                  <div class="arch-infra-col">
                    <div class="arch-cloud-tags">
                      <span>AWS</span><span>Azure</span><span>GCP</span>
                    </div>
                    <div class="arch-infra-name">클라우드</div>
                    <div class="arch-infra-desc">AWS, Azure, GCP 등 가상화 환경</div>
                  </div>
                </div>
              </div>

              <!-- Key Effects -->
              <div class="arch-effects">
                <div class="arch-effects-title">주요 효과</div>
                <div class="arch-effect-items">
                  <div class="arch-effect"><span class="arch-effect-dot"></span>보안 강화</div>
                  <div class="arch-effect"><span class="arch-effect-dot"></span>비용 절감</div>
                  <div class="arch-effect"><span class="arch-effect-dot"></span>컴플라이언스 달성</div>
                </div>
              </div>
            </div>"""

def main():
    text = HTML_FILE.read_bytes().decode("utf-8")
    # Normalise to LF for matching, then restore CRLF when writing
    lf_text = text.replace("\r\n", "\n")

    # Match from <div class="zt-cards"> to </div> (the zt-cards closing at 12-space indent)
    # followed by a newline and the hero-right </div> at 10-space indent
    pattern = re.compile(
        r'            <div class="zt-cards">.*?            </div>\n(?=          </div>)',
        re.DOTALL,
    )
    replaced, count = pattern.subn(ARCH_DIAGRAM + "\n", lf_text)
    if count == 0:
        print("ERROR: pattern not found!", file=sys.stderr)
        sys.exit(1)

    # Write back with CRLF
    HTML_FILE.write_bytes(replaced.replace("\n", "\r\n").encode("utf-8"))
    print(f"Done. Replaced {count} occurrence(s).")

if __name__ == "__main__":
    main()
