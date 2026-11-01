"""Regenerate sitemap.xml with full coverage + lastmod dates.

- Preserves existing priorities/changefreq from the current sitemap.xml
- Scans the whole site tree for .html files so no page is ever left out
  (e.g. blog/hair-transplant-karimnagar-guide.html, which build.py's PAGES misses)
- Adds <lastmod> from each file's mtime so Google prioritises fresh recrawls
- Rewrites robots.txt with the sitemap reference
"""
import os, re, datetime

SITE = "/home/hatch/workspace/ar-website"
BASE_URL = "https://surgery.arplasticsurgery.co.in"
SKIP = {"404.html"}

# sensible defaults for newly discovered pages
def default_priority(rel):
    if rel == "index.html":
        return ("1.0", "monthly")
    if rel in ("services.html", "about.html", "contact.html"):
        return ("0.9", "monthly")
    if rel.startswith("procedures/"):
        return ("0.8", "monthly")
    if rel.startswith("blog/"):
        return ("0.7", "monthly")
    if rel.startswith("stories/"):
        return ("0.6", "monthly")
    if rel.startswith("te/"):
        return ("0.6", "monthly")
    if "plastic-surgeon" in rel:
        return ("0.8", "monthly")
    return ("0.5", "monthly")

# 1. read existing sitemap to preserve priorities
existing = {}
sm_path = os.path.join(SITE, "sitemap.xml")
if os.path.exists(sm_path):
    xml = open(sm_path).read()
    for m in re.finditer(
        r"<url><loc>([^<]+)</loc><changefreq>([^<]*)</changefreq><priority>([^<]*)</priority>",
        xml,
    ):
        loc, cf, pr = m.groups()
        rel = loc.replace(BASE_URL + "/", "")
        existing[rel] = (pr, cf or "monthly")

# 2. scan all html files
pages = []
for root, dirs, files in os.walk(SITE):
    dirs[:] = [d for d in dirs if d not in ("__pycache__", ".git")]
    for fn in files:
        if not fn.endswith(".html"):
            continue
        full = os.path.join(root, fn)
        rel = os.path.relpath(full, SITE)
        if os.path.basename(rel) in SKIP:
            continue
        pages.append((rel, full))

# 3. build entries
entries = []
added = []
for rel, full in sorted(pages):
    if rel in existing:
        pr, cf = existing[rel]
    else:
        pr, cf = default_priority(rel)
        added.append(rel)
    lm = datetime.date.fromtimestamp(os.path.getmtime(full)).isoformat()
    entries.append(
        f"  <url><loc>{BASE_URL}/{rel}</loc>"
        f"<lastmod>{lm}</lastmod>"
        f"<changefreq>{cf}</changefreq>"
        f"<priority>{pr}</priority></url>"
    )

sm = ['<?xml version="1.0" encoding="UTF-8"?>',
      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
sm.extend(entries)
sm.append("</urlset>")
with open(sm_path, "w") as f:
    f.write("\n".join(sm) + "\n")

with open(os.path.join(SITE, "robots.txt"), "w") as f:
    f.write(f"User-agent: *\nAllow: /\n\nSitemap: {BASE_URL}/sitemap.xml\n")

print(f"sitemap: {len(entries)} urls ({len(added)} newly added), lastmod included")
for a in added:
    print("  +", a)
