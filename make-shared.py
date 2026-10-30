#!/usr/bin/env python3
"""
Create a standalone, share-only copy of a module page.

Usage:  python3 make-shared.py module-102.html

Output: shared/module-102.html  — the same page with
  - the whole navigation spine removed (no links to About Me or other modules)
  - the "Back to About Me" footer link removed
  - a noindex tag added so search engines don't list it
  - the stylesheet path fixed to ../styles.css
"""
import re
import sys
from pathlib import Path

if len(sys.argv) != 2:
    sys.exit("Usage: python3 make-shared.py module-102.html")

src = Path(sys.argv[1])
html = src.read_text(encoding="utf-8")

# 1. Remove the spine/nav block entirely
html = re.sub(r"<!-- =+ SPINE / NAV.*?END SPINE =+ -->", "", html, flags=re.S)

# 2. Remove the "Back to About Me" link from the footer
html = re.sub(r'<span><a href="index\.html">.*?</a></span>', "<span></span>", html)

# 3. Add noindex and fix the stylesheet path
html = html.replace(
    '<meta charset="UTF-8">',
    '<meta charset="UTF-8">\n<meta name="robots" content="noindex, nofollow">',
)
html = html.replace('href="styles.css"', 'href="../styles.css"')

# 4. Safety check: no links back into the rest of the site may remain
leftovers = re.findall(r'href="(index\.html|module-[^"]*\.html)"', html)
if leftovers:
    sys.exit(f"Refusing to write: page still links to {sorted(set(leftovers))}")

out_dir = Path("shared")
out_dir.mkdir(exist_ok=True)
out = out_dir / src.name
out.write_text(html, encoding="utf-8")
print(f"Wrote {out}")
