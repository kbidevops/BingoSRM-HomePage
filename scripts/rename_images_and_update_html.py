#!/usr/bin/env python3
"""
Rename non-ASCII image filenames in ./images to ASCII-safe names and update HTML references.
Usage:
  - Dry run: python scripts/rename_images_and_update_html.py --dry
  - Apply:    python scripts/rename_images_and_update_html.py

This script transliterates filenames using Unidecode and makes a safe slug,
ensuring unique names. It updates HTML files under `sub/` and root HTML files.
"""

import os
import re
import argparse
from unidecode import unidecode
from pathlib import Path

IMG_DIR = Path("images")
HTML_GLOB = ["sub/*.html", "*.html"]


def slug(name):
    stem, ext = os.path.splitext(name)
    s = unidecode(stem)
    s = s.lower()
    s = re.sub(r"[\s/\\]+", "-", s)
    s = re.sub(r"[^a-z0-9\-_.]", "", s)
    s = re.sub(r"-{2,}", "-", s).strip("-")
    if not s:
        s = "file"
    return s + ext


def find_html_files():
    files = []
    for pattern in HTML_GLOB:
        files.extend(Path(".").glob(pattern))
    # include any html under subfolders as well
    files.extend(Path("sub").rglob("*.html"))
    return sorted(set(files))


def main(dry):
    if not IMG_DIR.exists():
        print("images directory not found:", IMG_DIR)
        return

    mapping = {}
    for p in IMG_DIR.iterdir():
        if not p.is_file():
            continue
        try:
            p.name.encode('ascii')
            is_ascii = True
        except UnicodeEncodeError:
            is_ascii = False

        if is_ascii:
            continue

        new = slug(p.name)
        dest = IMG_DIR / new
        i = 1
        while dest.exists() and dest != p:
            dest = IMG_DIR / f"{os.path.splitext(new)[0]}-{i}{os.path.splitext(new)[1]}"
            i += 1
        mapping[str(p.name)] = str(dest.name)

    if not mapping:
        print("No non-ASCII filenames found in images/")
        return

    print("Planned renames:")
    for a,b in mapping.items():
        print(f"  {a} -> {b}")

    html_files = find_html_files()
    if html_files:
        print("\nHTML files to be updated:")
        for f in html_files:
            print(" ", f)
    else:
        print("No HTML files found to update.")

    if dry:
        print("\nDry-run mode: no files changed.")
        return

    # perform renames
    for a,b in mapping.items():
        src = IMG_DIR / a
        dst = IMG_DIR / b
        if not src.exists():
            print("WARN: source missing:", src)
            continue
        print("Renaming:", src, "->", dst)
        src.rename(dst)

    # update HTML references
    for f in html_files:
        text = f.read_text(encoding="utf-8")
        changed = False
        for a,b in mapping.items():
            if a in text:
                text = text.replace(a, b)
                changed = True
        if changed:
            print("Updating references in", f)
            f.write_text(text, encoding="utf-8")

    print("\nDone. Review changes and commit if OK.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true", help="Show actions without applying")
    args = ap.parse_args()
    main(args.dry)
