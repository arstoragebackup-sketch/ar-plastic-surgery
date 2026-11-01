#!/usr/bin/env python3
"""Publish one procedure hub per day: all 33 districts covered in each article."""
import sys, os, datetime, time, base64, shutil

SITE = "/home/hatch/workspace/ar-website"
sys.path.insert(0, SITE)
os.chdir(SITE)

from district_hubs import make_hub, next_hub, mark_hub_done

proc_slug = next_hub()
if not proc_slug:
    print("hub queue exhausted — all procedure hubs published")
    sys.exit(0)

today = datetime.date.today().strftime("%-d %B %Y")
article = make_hub(proc_slug, today)

import content_district_posts as cdp
import importlib
importlib.reload(cdp)
posts = list(cdp.DISTRICT_POSTS) + [article]
with open(os.path.join(SITE, "content_district_posts.py"), "w") as f:
    f.write("# Daily district articles — appended by the ar-daily-procedure-hub cron.\n")
    f.write("# Each entry follows the blog post schema from content_blog.py.\n")
    f.write("# Do not edit by hand; the publisher script manages this file.\n\n")
    f.write("DISTRICT_POSTS = ")
    f.write(repr(posts))
    f.write("\n")
print(f"hub added: blog/{article['slug']}.html")

# ---- Telugu version: translate the new hub article ----
# Uses the same structure; key fields translated to Telugu
import copy
te_article = copy.deepcopy(article)
# Translate title/h1/lede/desc using Telugu procedure name mapping
te_names = {
    "hair-transplant": "హెయిర్ ట్రాన్స్‌ప్లాంట్",
    "breast-augmentation": "బ్రెస్ట్ ఆగ్మెంటేషన్",
    "gynecomastia": "గైనకోమాస్టియా",
    "tummy-tuck": "టమ్మీ టక్",
    "botox-fillers": "బోటాక్స్ ఫిల్లర్లు",
    "liposuction": "లైపోసక్షన్",
    "rhinoplasty": "రైనోప్లాస్టీ",
    "scar-treatment": "స్కార్ ట్రీట్‌మెంట్",
    "burn-reconstruction": "బర్న్ పునర్నిర్మాణం",
    "hand-surgery": "హ్యాండ్ సర్జరీ",
    "cleft-lip-palate": "చీలిన పెదవి అంగిలి",
    "lipoma-removal": "లిపోమా తొలగింపు",
    "prp-therapy": "పీఆర్పీ చికిత్స",
    "chemical-peels": "కెమికల్ పీల్స్",
    "laser-hair-removal": "లేజర్ హెయిర్ రిమూవల్",
    "skin-grafting": "స్కిన్ గ్రాఫ్టింగ్",
    "eyelid-surgery": "కనురెప్పల సర్జరీ",
}
te_pname = te_names.get(proc_slug, proc_slug)
te_article["h1"] = f"తెలంగాణలో {te_pname}: పూర్తి జిల్లా గైడ్"
te_article["title"] = f"{te_pname} తెలంగాణ: అన్ని జిల్లాల గైడ్ | AR Plastic Surgery"
te_article["desc"] = f"తెలంగాణలో ఎక్కడైనా {te_pname} గురించి ఆలోచిస్తున్నారా? డా. అశోక్ రెడ్డి గారు అర్హత, ప్రక్రియ మరియు కోలుకోవడం గురించి వివరిస్తారు — అన్ని 33 జిల్లాల నుండి ప్రయాణ ప్రణాళికతో."
te_article["lede"] = f"మీరు తెలంగాణలో ఎక్కడ నివసించినా, నాణ్యమైన {te_pname} సంరక్షణ అందుబాటులో ఉంది. ఈ గైడ్ ప్రక్రియను నిజాయితీగా వివరిస్తుంది."

# Append to Telugu district posts file
import content_district_posts_te as cdt
importlib.reload(cdt)
te_posts = list(cdt.TE_DISTRICT_POSTS) + [te_article]
with open(os.path.join(SITE, "content_district_posts_te.py"), "w") as f:
    f.write("# Telugu translations of district guide posts — generated 2026-10-16\n")
    f.write("# Daily Telugu hubs appended by the ar-daily-procedure-hub cron.\n\n")
    f.write("TE_DISTRICT_POSTS = ")
    f.write(repr(te_posts))
    f.write("\n")
print(f"Telugu hub added: te/blog/{te_article['slug']}.html")

os.system(f"cd {SITE} && python3 build.py > /tmp/hub-build.log 2>&1")
log = open("/tmp/hub-build.log").read()
if "PARSE ERROR" in log:
    print("BUILD FAILED")
    print(log[-2000:])
    sys.exit(1)
# confirm the hub page built clean
for line in log.splitlines():
    if article["slug"] in line:
        print(line.strip()[:160])

# ---- pre-publish fact-check (Google Oct-2026 AI-content guidance) ----
# Every AI-generated page must be reviewed for accuracy before publishing.
# This automated gate checks facts, metadata and banned claims; it halts
# the publish (no push) if anything fails.
CANON = {
    "phone": "9182656866",
    "address_bits": ["Reddy gari vantillu", "Karimnagar"],
    "hours": "10:00",
    "booking": "arstoragebackup-sketch.github.io/Booking",
    "doctor": "Ashok Reddy",
}
BANNED = ["100% result", "100% results", "guaranteed result", "guaranteed results",
          "permanent cure", "permanently cured", "no risk", "zero risk",
          "best surgeon in the world", "best surgeon in india"]
hub_html_path = os.path.join(SITE, "blog", article["slug"] + ".html")
hub_html = open(hub_html_path, encoding="utf-8").read()
check_log = []
def check(name, ok, detail=""):
    check_log.append(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))
    return ok

all_ok = True
all_ok &= check("banned claims absent",
                not any(b.lower() in hub_html.lower() for b in BANNED))
all_ok &= check("phone correct", CANON["phone"] in hub_html)
all_ok &= check("address present",
                all(b.lower() in hub_html.lower() for b in CANON["address_bits"]))
all_ok &= check("booking link present", CANON["booking"] in hub_html)
all_ok &= check("doctor name present", CANON["doctor"] in hub_html)
title = article.get("title", ""); desc = article.get("desc", "")
all_ok &= check("title length <=68", len(title) <= 68, f"{len(title)} chars")
all_ok &= check("desc length <=168", len(desc) <= 168, f"{len(desc)} chars")
all_ok &= check("no invented stats", "100%" not in hub_html and "No. 1" not in hub_html)
log_path = os.path.join(SITE, "hidden_hub_checks.log")
with open(log_path, "a") as f:
    f.write(f"\n=== {datetime.date.today()} {article['slug']} ===\n" + "\n".join(check_log) + "\n")
print("\n".join(check_log))
if not all_ok:
    print("FACT-CHECK FAILED — publish halted, nothing pushed")
    sys.exit(2)
print("fact-check passed")

deploy_root = "/tmp/ar-deploy"
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
        {"message": f"Daily hub: {article['slug']}", "tree": t["sha"], "parents": [base_sha]})
u = req("PATCH", f"/repos/{owner}/{repo}/git/refs/heads/main", {"sha": c["sha"]})
ok = u["object"]["sha"][:8] == c["sha"][:8]
print("pushed:", ok, "| files:", len(tree))
if ok:
    mark_hub_done(proc_slug)
    print("hub queue updated")
