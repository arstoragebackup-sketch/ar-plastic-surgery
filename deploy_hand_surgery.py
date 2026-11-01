#!/usr/bin/env python3
"""One-off deploy: push the full rebuilt site (hand surgery improvements)."""
import os, sys, shutil, base64, time

SITE = "/home/hatch/workspace/ar-website"
deploy_root = "/tmp/ar-deploy-hs"
shutil.rmtree(deploy_root, ignore_errors=True)
os.makedirs(deploy_root)
os.system(f"cd {SITE} && cp *.html robots.txt sitemap.xml {deploy_root}/ 2>/dev/null; "
          f"cp -r assets blog procedures te stories {deploy_root}/ && touch {deploy_root}/.nojekyll")

sys.path.insert(0, "/home/hatch/workspace/skills/github/bin")
sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
from gh import req
owner, repo, root = "arstoragebackup-sketch", "ar-plastic-surgery", deploy_root
ref = req("GET", f"/repos/{owner}/{repo}/git/ref/heads/main")
base_sha = ref["object"]["sha"]

def make_blob(p):
    with open(p, "rb") as fh:
        content = base64.b64encode(fh.read()).decode()
    for _ in range(8):
        try:
            b = req("POST", f"/repos/{owner}/{repo}/git/blobs",
                    {"content": content, "encoding": "base64"})
            if isinstance(b, dict) and b.get("sha"):
                return b["sha"]
        except Exception:
            pass
        time.sleep(3)
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
        {"message": "Hand surgery SEO: expanded guide (+3 sections, 8 FAQs), internal links from all 4 hand procedure pages + tendon article", "tree": t["sha"], "parents": [base_sha]})
u = req("PATCH", f"/repos/{owner}/{repo}/git/refs/heads/main", {"sha": c["sha"]})
ok = u["object"]["sha"][:8] == c["sha"][:8]
print("pushed:", ok, "| commit:", c["sha"][:8], "| files:", len(tree))
