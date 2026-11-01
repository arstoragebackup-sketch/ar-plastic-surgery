#!/usr/bin/env python3
"""Publish one district article per day: generate, rebuild, deploy."""
import sys, os, datetime, time, base64

SITE = "/home/hatch/workspace/ar-website"
sys.path.insert(0, SITE)
os.chdir(SITE)

from district_articles import make_article, next_queue_item, mark_done

item = next_queue_item()
if not item:
    print("queue exhausted — all district articles published")
    sys.exit(0)

district_slug, proc_slug = item
today = datetime.date.today().strftime("%-d %B %Y")
article = make_article(district_slug, proc_slug, today)

# append to content_district_posts.py
sys.path.insert(0, SITE)
import content_district_posts as cdp
import importlib
importlib.reload(cdp)
posts = list(cdp.DISTRICT_POSTS) + [article]
with open(os.path.join(SITE, "content_district_posts.py"), "w") as f:
    f.write("# Daily district articles — appended by the ar-daily-district-article cron.\n")
    f.write("# Each entry follows the blog post schema from content_blog.py.\n")
    f.write("# Do not edit by hand; the publisher script manages this file.\n\n")
    f.write("DISTRICT_POSTS = ")
    f.write(repr(posts))
    f.write("\n")
print(f"article added: blog/{article['slug']}.html")

# rebuild
os.system(f"cd {SITE} && python3 build.py > /tmp/article-build.log 2>&1")
log = open("/tmp/article-build.log").read()
if "PARSE ERROR" in log:
    print("BUILD FAILED")
    print(log[-2000:])
    sys.exit(1)
print("build ok")

# deploy: same static file set as the main pipeline
import shutil
deploy_root = "/tmp/ar-deploy"
shutil.rmtree(deploy_root, ignore_errors=True)
os.makedirs(deploy_root)
os.system(f"cd {SITE} && cp *.html robots.txt sitemap.xml {deploy_root}/ 2>/dev/null; "
          f"cp -r assets blog procedures te stories {deploy_root}/ && touch {deploy_root}/.nojekyll")
sys.path.insert(0, "/home/hatch/workspace/skills/github/bin")
from gh import req
owner, repo, root = "arstoragebackup-sketch", "ar-plastic-surgery", deploy_root
ref = req("GET", f"/repos/{owner}/{repo}/git/ref/heads/main")
base_sha = ref["object"]["sha"]

def make_blob(p):
    with open(p, "rb") as fh:
        content = base64.b64encode(fh.read()).decode()
    for _ in range(5):
        b = req("POST", f"/repos/{owner}/{repo}/git/blobs",
                {"content": content, "encoding": "base64"})
        if b.get("sha"):
            return b["sha"]
        time.sleep(2)
    raise RuntimeError("blob failed")

tree, files = [], []
for dirpath, _, fns in os.walk(root):
    for fn in fns:
        p = os.path.join(dirpath, fn)
        files.append((os.path.relpath(p, root).replace(os.sep, "/"), p))
for rel, p in sorted(files):
    tree.append({"path": rel, "mode": "100644", "type": "blob", "sha": make_blob(p)})
    time.sleep(0.1)
t = req("POST", f"/repos/{owner}/{repo}/git/trees", {"base_tree": base_sha, "tree": tree})
c = req("POST", f"/repos/{owner}/{repo}/git/commits",
        {"message": f"Daily article: {article['slug']}", "tree": t["sha"], "parents": [base_sha]})
u = req("PATCH", f"/repos/{owner}/{repo}/git/refs/heads/main", {"sha": c["sha"]})
ok = u["object"]["sha"][:8] == c["sha"][:8]
print("pushed:", ok, "| files:", len(tree))
if ok:
    mark_done(district_slug, proc_slug)
    print("queue updated")
