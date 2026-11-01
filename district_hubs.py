# Daily procedure-hub engine: one procedure per day, each article covering
# ALL 33 Telangana districts with travel/planning guidance per district.
# Procedure-hub engine: one procedure per day, each article covering
# ALL 33 Telangana districts. Phase 1: 10 procedures; Phase 2: 8 more.

from district_articles import DISTRICTS, ARTICLE_PROCEDURES

HUB_ORDER = [
    "hair-transplant",
    "breast-augmentation",
    "gynecomastia",
    "tummy-tuck",
    "botox-fillers",
    "liposuction",
    "rhinoplasty",
    "scar-treatment",
    "hand-surgery",
    "burn-reconstruction",
    # Phase 2 (owner-approved 2026-10-11) — ranked by SEO gap report
    # NOTE 2026-10-13: facelift removed from queue at owner's request ("Stop facelift do another")
    "cleft-lip-palate",
    "lipoma-removal",
    "prp-therapy",
    "chemical-peels",
    "laser-hair-removal",
    "skin-grafting",
    "eyelid-surgery",
]

HUB_QUEUE_FILE = "/home/hatch/workspace/ar-website/district_hub_queue.json"


def make_hub(proc_slug, date_str):
    proc = ARTICLE_PROCEDURES[proc_slug]
    pname = proc["name"]
    slug = f"{proc_slug}-telangana-district-guide"
    h1 = f"{pname} in Telangana: Complete District Guide"
    title = f"{pname} Telangana: All Districts Guide | AR Plastic Surgery"
    if len(title) > 68:
        title = f"{pname} Telangana District Guide | AR Plastic Surgery"
    desc = (f"Considering {pname.lower()} anywhere in Telangana? Dr Ashok Reddy (MBBS, DNB, M.Ch, Gold Medalist) "
            f"covers candidacy, procedure and recovery — with travel planning for patients from all 33 districts.")
    if len(desc) > 168:
        desc = (f"{pname} in Telangana — candidacy, procedure, recovery and travel planning for all 33 districts. "
                f"By Dr Ashok Reddy, AR Plastic Surgery, Karimnagar.")
    lede = (f"Wherever you live in Telangana, quality {pname.lower()} care is within reach. This guide explains "
            f"the procedure honestly — who it suits, what happens, how recovery works — and then gives "
            f"district-by-district travel planning for all 33 Telangana districts to reach AR Plastic Surgery "
            f"in Karimnagar, led by Dr Ashok Reddy (MBBS, DNB Mumbai, M.Ch Delhi, Gold Medalist).")

    sections = [(h, list(ps)) for h, ps in proc["sections"]]

    # district-by-district sections
    for dslug, dname, dkm, dnote in DISTRICTS:
        if dkm == 0:
            body = (f"AR Plastic Surgery is right here in {dname} — {dnote}. Consultation, procedure and "
                    f"all follow-ups happen close to home.")
        else:
            body = (f"{dname} is about {dkm} km from Karimnagar — {dnote}. Plan a morning consultation so "
                    f"assessment and planning finish in one visit; the team will help schedule your procedure "
                    f"day and follow-ups around your travel.")
        sections.append((f"{pname} for {dname} Patients", [body]))

    sections.append(
        ("Why Patients Across Telangana Choose AR Plastic Surgery",
         ["Dr Ashok Reddy was awarded the Gold Medal for Plastic & Reconstructive Surgery at ABVIMS, "
          "Dr RML Hospital, New Delhi. Every consultation starts with an honest question — do you actually "
          "need this procedure? — and the answer is sometimes no.",
          "That honesty is why patients travel from all 33 districts. The clinic is open all seven days, "
          "10 AM to 8 PM, and the team helps outstation patients "
          "plan visits efficiently."]))

    return {
        "slug": slug,
        "h1": h1,
        "title": title,
        "desc": desc,
        "lede": lede,
        "date": date_str,
        "sections": sections,
        "faqs": proc["faqs"],
        "related_procedures": proc["related"],
    }


def next_hub():
    import json, os
    done = []
    if os.path.exists(HUB_QUEUE_FILE):
        done = json.load(open(HUB_QUEUE_FILE))
    for p in HUB_ORDER:
        if p not in done:
            return p
    return None


def mark_hub_done(proc_slug):
    import json, os
    done = []
    if os.path.exists(HUB_QUEUE_FILE):
        done = json.load(open(HUB_QUEUE_FILE))
    done.append(proc_slug)
    json.dump(done, open(HUB_QUEUE_FILE, "w"))
