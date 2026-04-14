"""
parse_manuals.py
----------------
Extracts the bookmark/outline tree AND section content from each PDF in
public/ and writes public/manual-data.json for sub/manual/index.html.

Each section node in the JSON tree gains:
  "slug"     - URL-safe id for anchor links
  "content"  - HTML string of the section's page(s)
  "headings" - [{level, id, text}] for right-side in-page TOC

Requirements:
    pip install pymupdf
"""

import html as html_mod
import json
import pathlib
import re
import sys

try:
    import fitz  # PyMuPDF
except ImportError:
    sys.exit("PyMuPDF not found. Run:  pip install pymupdf")

ROOT   = pathlib.Path(__file__).parent.parent
PUBLIC = ROOT / "public"
OUT    = PUBLIC / "manual-data.json"

MANUALS = [
    ("BingoCVM 매뉴얼_관리자",       "관리자 매뉴얼"),
    ("BingoCVM 매뉴얼_사용자",       "사용자 매뉴얼"),
    ("BingoCVM 매뉴얼_자산등록상세", "자산등록 상세"),
]

# Lines to skip from page headers/footers
_SKIP = [
    re.compile(r"Copyright"),
    re.compile(r"^BingoCVM \d+\.\d+"),
    re.compile(r"^버전:\s*\d"),
    re.compile(r"^\d+\s*$"),       # standalone page numbers
    re.compile(r"^<목차>"),
    re.compile(r"^목\s*차$"),
]

# Korean dotted TOC line: "1.2. 제목·····10"
_TOC_LINE = re.compile(
    r"^(\d+(?:\.\d+)*)\.?\s+(.+?)[\u00b7\u22ef\.\s]{3,}(\d+)\s*$",
    re.MULTILINE,
)


def slugify(text: str) -> str:
    text = re.sub(r"\s+", "-", text.strip())
    text = re.sub(r"[^\w\uAC00-\uD7A3-]", "", text)
    return (text or "sec")[:60]


def _level_from_num(num: str) -> int:
    return len(num.split("."))


def _detect_page_offset(doc) -> int:
    """
    PDFs use printed (logical) page numbers in the TOC text.
    Find offset: physical_1based = printed + offset
    """
    for pg_i in range(doc.page_count):
        m = re.search(r"All Rights Reserved\.\s*(\d+)\s", doc[pg_i].get_text())
        if m:
            printed  = int(m.group(1))
            physical = pg_i + 1
            return physical - printed
    return 0


def _parse_toc_from_text(doc) -> list:
    flat = []
    in_toc = False
    _inner_num = re.compile(r'^(\d+(?:\.\d+)+)\.?\s+(.*)')
    for i in range(doc.page_count):
        text = doc[i].get_text()
        if "<목차>" in text or "목  차" in text:
            in_toc = True
        if not in_toc:
            continue
        for m in _TOC_LINE.finditer(text):
            num_str = m.group(1)
            rest    = m.group(2).strip()
            # If the title itself starts with a dotted section number (e.g.
            # "6.5. 비교보고서"), the regex captured a stray prefix digit.
            # Re-derive the real number and level from the title.
            inner = _inner_num.match(rest)
            if inner and not rest.startswith(num_str + "."):
                num_str = inner.group(1)
                rest    = inner.group(2).strip()
            flat.append({
                "level": _level_from_num(num_str),
                "title": f"{num_str}. {rest}",
                "page":  int(m.group(3)),
            })
        if in_toc and flat:
            if i + 1 < doc.page_count and not _TOC_LINE.search(doc[i + 1].get_text()):
                break
    return flat


def build_flat_toc(doc, stem: str = "") -> tuple:
    """Returns (flat_list, used_text_parse: bool)."""
    raw = doc.get_toc(simple=False)
    bookmark_entries = []
    if raw:
        bookmark_entries = [
            {"level": e[0], "title": e[1].strip(), "page": e[2]}
            for e in raw
            if e[1].strip() and e[2] >= 1  # skip empty titles and invalid pages
        ]
        # Strip document-title wrapper bookmark if present
        if bookmark_entries and _is_title_root(bookmark_entries[0], stem):
            min_level = min(e["level"] for e in bookmark_entries[1:]) if len(bookmark_entries) > 1 else 1
            bookmark_entries = [
                {**e, "level": e["level"] - bookmark_entries[0]["level"] + min_level}
                for e in bookmark_entries[1:]
            ]

    # Always also try text-parsing the <목차> page
    text_entries = _parse_toc_from_text(doc)

    # Use whichever source gives more entries (handles partial/incomplete bookmarks)
    if len(text_entries) > len(bookmark_entries):
        return text_entries, True   # used text parse → needs offset correction
    return bookmark_entries, False  # used bookmarks → page numbers are physical


def _is_title_root(entry: dict, stem: str) -> bool:
    """True if the entry is a document-title wrapper bookmark (not real content)."""
    t = entry["title"]
    # Matches the PDF filename stem or generic title patterns
    return stem and (t.lower() == stem.lower() or t.startswith(stem.split("_")[0]))


def build_tree(flat: list) -> list:
    root: list = []
    stack: list = []
    for item in flat:
        node  = {"title": item["title"], "page": item["page"], "children": []}
        level = item["level"]
        while stack and stack[-1][0] >= level:
            stack.pop()
        (stack[-1][1]["children"] if stack else root).append(node)
        stack.append((level, node))
    return root


def _pages_to_html(doc, start_page: int, end_page: int) -> str:
    """Extract text from pages [start_page, end_page] (1-based) as HTML."""
    end_page = min(end_page, doc.page_count)
    if start_page > end_page:
        end_page = start_page

    html_parts: list = []

    for pg_i in range(start_page - 1, end_page):
        page = doc[pg_i]

        # ── Table detection ──────────────────────────────────────────────
        table_areas: list = []
        table_items: list = []
        try:
            for tab in page.find_tables():
                table_areas.append(fitz.Rect(tab.bbox))
                rows = tab.extract()
                if not rows:
                    continue
                t: list = ["<table>"]
                for r_i, row in enumerate(rows):
                    t.append("<tr>")
                    for cell in row:
                        tag = "th" if r_i == 0 else "td"
                        val = html_mod.escape(str(cell or "").strip())
                        t.append(f"<{tag}>{val}</{tag}>")
                    t.append("</tr>")
                t.append("</table>")
                table_items.append((tab.bbox[1], "\n".join(t)))
        except Exception:
            pass

        # ── Text blocks ──────────────────────────────────────────────────
        text_items: list = []
        data = page.get_text("dict", sort=True)

        for block in data.get("blocks", []):
            if block.get("type") != 0:
                continue
            if any(fitz.Rect(block["bbox"]).intersects(ta) for ta in table_areas):
                continue

            lines: list = []
            max_size = 0.0
            has_bold  = False
            for ln in block["lines"]:
                ln_txt = ""
                for span in ln["spans"]:
                    max_size = max(max_size, span.get("size", 0))
                    if span.get("flags", 0) & 16:
                        has_bold = True
                    ln_txt += span.get("text", "")
                ln_txt = ln_txt.strip()
                if ln_txt:
                    lines.append(ln_txt)

            if not lines:
                continue
            full = " ".join(lines)
            if any(p.search(full) for p in _SKIP):
                continue

            safe = html_mod.escape(full)
            y    = block["bbox"][1]

            m_hd = re.match(r"^(\d+(?:\.\d+)*)\.?\s+\S", full)
            if m_hd:
                depth = len(m_hd.group(1).split("."))
                tag   = {1: "h2", 2: "h3", 3: "h4"}.get(depth, "h4")
                sid   = slugify(full)
                text_items.append((y, f'<{tag} id="{sid}">{safe}</{tag}>'))
            elif max_size >= 14.5 or has_bold:
                text_items.append((y, f"<h3>{safe}</h3>"))
            else:
                text_items.append((y, f"<p>{safe}</p>"))

        merged = table_items + text_items
        merged.sort(key=lambda x: x[0])
        html_parts.extend(h for _, h in merged)

    return "\n".join(html_parts)


def _add_content(tree: list, doc, total_pages: int) -> None:
    flat: list = []
    def walk(nodes):
        for n in nodes:
            flat.append(n)
            walk(n["children"])
    walk(tree)

    for i, node in enumerate(flat):
        start = node["page"]
        end   = flat[i + 1]["page"] - 1 if i + 1 < len(flat) else total_pages
        end   = max(end, start)

        node["slug"]    = slugify(node["title"])
        content         = _pages_to_html(doc, start, end)
        node["content"] = content

        node["headings"] = [
            {"level": m.group(1), "id": m.group(2), "text": html_mod.unescape(m.group(3))}
            for m in re.finditer(
                r"<(h[2-4])[^>]*id=\"([^\"]*)\"[^>]*>([^<]+)<", content
            )
        ]


# ── Main ──────────────────────────────────────────────────────────────────────

data = []
for stem, label in MANUALS:
    pdf_path = PUBLIC / f"{stem}.pdf"
    if not pdf_path.exists():
        print(f"  [SKIP] {pdf_path.name}")
        continue

    doc           = fitz.open(str(pdf_path))
    flat, used_text = build_flat_toc(doc, stem)
    total_pages   = doc.page_count

    if not flat:
        flat = [{"level": 1, "title": label, "page": 1}]
        print(f"  [WARN] {pdf_path.name}: no TOC; stub created")
    else:
        src = "text-parsed" if used_text else "bookmarks"
        if used_text:
            offset = _detect_page_offset(doc)
            if offset:
                for item in flat:
                    item["page"] = max(1, item["page"] + offset)
                print(f"  [OK]   {pdf_path.name}  ({src})  offset={offset:+d}  entries={len(flat)}")
            else:
                print(f"  [OK]   {pdf_path.name}  ({src})  entries={len(flat)}")
        else:
            print(f"  [OK]   {pdf_path.name}  ({src})  entries={len(flat)}")

    tree = build_tree(flat)
    print(f"         extracting content …", end="", flush=True)
    _add_content(tree, doc, total_pages)
    print(" done")
    doc.close()

    data.append({
        "id":          stem.replace(" ", "_"),
        "label":       label,
        "file":        f"/public/{pdf_path.name}",
        "total_pages": total_pages,
        "toc":         tree,
    })

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nWrote {OUT}  ({OUT.stat().st_size // 1024} KB)")
