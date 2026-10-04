#!/usr/bin/env python3
"""Static site generator for AR Plastic Surgery (Karimnagar).
Generates plain HTML/CSS with no build step at serve time.
Run: python3 build.py
"""
import os, re, html as htmllib
from html.parser import HTMLParser

# ---------------------------------------------------------------- config
# PLACEHOLDER: replace with the real GitHub Pages URL once the repo is created,
# e.g. https://<username>.github.io/<repo>/  (keep trailing slash off)
BASE_URL = "https://arstoragebackup-sketch.github.io/ar-plastic-surgery"

OUT = os.path.dirname(os.path.abspath(__file__))

CLINIC = {
    "name": "AR Plastic Surgery",
    "tagline": "Precision and Perfection",
    "doctor": "Dr Ashok Reddy",
    "credentials": "MBBS, DNB (Mumbai), M.Ch (Delhi), Gold Medalist",
    "specialties": "Plastic, Cosmetic, Hand & Microvascular Surgeon",
    "phone_display": "+91 91826 56866",
    "phone_tel": "+919182656866",
    "address": "Opp Reddy gari vantillu, Court Chowrasta, Jyothinagar, Karimnagar, Telangana 505001",
    "address_short": "Opp Reddy gari vantillu, Court Chowrasta, Karimnagar",
    "hours": "Monday – Sunday, 10:00 AM – 8:00 PM",
    "booking": "https://arstoragebackup-sketch.github.io/Booking/",
    "instagram": "https://www.instagram.com/karimnagar.aesthetics/",
    "lat": "18.44449",
    "lon": "79.12475",
}
TOWNS = ["Karimnagar", "Jagtial", "Sircilla", "Warangal", "Siddipet", "Peddapalli", "Vemulawada"]

# ---------------------------------------------------------------- CSS
CSS = r"""
:root{
  --navy:#0f2a4a; --navy-2:#143a63; --ink:#1d2b3a; --muted:#5a6b7d;
  --gold:#c19a3d; --gold-soft:#f6eeda; --bg:#ffffff; --bg-soft:#f5f8fb;
  --line:#e3eaf2; --radius:14px;
  --font:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
  --serif:Georgia,"Times New Roman",serif;
}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:var(--font);color:var(--ink);background:var(--bg);line-height:1.65;font-size:16.5px}
img{max-width:100%;height:auto;display:block}
a{color:var(--navy-2);text-decoration:none}
a:hover{text-decoration:underline}
.wrap{max-width:1120px;margin:0 auto;padding:0 20px}
h1,h2,h3{font-family:var(--serif);color:var(--navy);line-height:1.25}
h1{font-size:clamp(1.9rem,4.5vw,2.9rem);margin-bottom:.6rem}
h2{font-size:clamp(1.45rem,3vw,2rem);margin-bottom:.6rem}
h3{font-size:1.15rem;margin-bottom:.4rem}
.lede{font-size:1.12rem;color:var(--muted);max-width:46rem}
section{padding:3.2rem 0}
.eyebrow{display:inline-block;font-size:.78rem;letter-spacing:.14em;text-transform:uppercase;
  color:var(--gold);font-weight:700;margin-bottom:.5rem}
/* header */
.site-header{position:sticky;top:0;z-index:50;background:#fff;border-bottom:1px solid var(--line)}
.site-header.scrolled{box-shadow:0 4px 18px rgba(15,42,74,.08)}
.header-inner{display:flex;align-items:center;gap:1rem;padding:.65rem 0}
.brand{display:flex;align-items:center;gap:.7rem;margin-right:auto}
.brand img{width:52px;height:52px;border-radius:50%;object-fit:cover;border:2px solid var(--line)}
.brand-name{font-family:var(--serif);font-weight:700;color:var(--navy);font-size:1.12rem;line-height:1.2}
.brand-tag{font-size:.72rem;letter-spacing:.12em;text-transform:uppercase;color:var(--gold);font-weight:700}
nav.main-nav{display:flex;gap:1.2rem;align-items:center}
nav.main-nav a{font-weight:600;color:var(--ink);font-size:.95rem}
nav.main-nav a.active,nav.main-nav a:hover{color:var(--navy-2)}
.header-cta{display:flex;gap:.6rem;align-items:center}
.btn{display:inline-block;padding:.68rem 1.35rem;border-radius:999px;font-weight:700;font-size:.95rem;
  border:2px solid var(--navy);transition:.18s;white-space:nowrap}
.btn:hover{text-decoration:none;transform:translateY(-1px)}
.btn-solid{background:var(--navy);color:#fff}
.btn-solid:hover{background:var(--navy-2)}
.btn-gold{background:var(--gold);border-color:var(--gold);color:#fff}
.btn-gold:hover{background:#a9842f}
.btn-outline{background:#fff;color:var(--navy)}
.phone-link{font-weight:700;color:var(--navy);font-size:.95rem;white-space:nowrap}
.nav-toggle{display:none;background:none;border:0;font-size:1.7rem;color:var(--navy);cursor:pointer}
/* hero */
.hero{background:linear-gradient(180deg,#f7fafd 0%,#fff 100%);padding:4rem 0 3.4rem;position:relative;overflow:hidden}
.hero::after{content:"";position:absolute;top:-120px;right:-120px;width:380px;height:380px;border-radius:50%;
  background:radial-gradient(circle,rgba(193,154,61,.16),transparent 70%)}
.hero-grid{display:grid;grid-template-columns:1.25fr .85fr;gap:2.5rem;align-items:center;position:relative;z-index:1}
.hero h1 .accent{color:var(--gold)}
.hero-badges{display:flex;flex-wrap:wrap;gap:.55rem;margin:1.1rem 0 1.4rem}
.badge{background:#fff;border:1px solid var(--line);border-radius:999px;padding:.42rem .95rem;
  font-size:.85rem;font-weight:600;color:var(--navy)}
.badge b{color:var(--gold)}
.hero-photo{border-radius:var(--radius);overflow:hidden;box-shadow:0 18px 44px rgba(15,42,74,.16);border:6px solid #fff}
.hero-photo img{width:100%;aspect-ratio:4/4.4;object-fit:cover;object-position:top}
.hero-photo figcaption{background:var(--navy);color:#fff;padding:.8rem 1rem;font-size:.9rem}
/* trust bar */
.trust{background:var(--navy);color:#e8eef5;padding:1.6rem 0}
.trust-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:1.2rem;text-align:center}
.trust-grid .t b{display:block;font-family:var(--serif);font-size:1.35rem;color:#fff}
.trust-grid .t span{font-size:.88rem;color:#b9c7d8}
/* cards */
.card-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1.2rem;margin-top:1.6rem}
.card{background:#fff;border:1px solid var(--line);border-radius:var(--radius);padding:1.5rem;
  transition:.18s;display:flex;flex-direction:column}
.card:hover{box-shadow:0 12px 30px rgba(15,42,74,.1);transform:translateY(-2px)}
.card h3{margin-bottom:.5rem}
.card p{color:var(--muted);font-size:.96rem;flex:1}
.card .more{margin-top:.9rem;font-weight:700;font-size:.92rem}
.card .icon{font-size:1.7rem;margin-bottom:.6rem}
/* split */
.split{display:grid;grid-template-columns:.9fr 1.1fr;gap:2.6rem;align-items:center}
.split img.doc{border-radius:var(--radius);box-shadow:0 18px 44px rgba(15,42,74,.14);aspect-ratio:3/3.6;object-fit:cover;object-position:top;width:100%}
.checklist{list-style:none;margin:1rem 0}
.checklist li{padding:.45rem 0 .45rem 2rem;position:relative}
.checklist li::before{content:"✓";position:absolute;left:0;color:var(--gold);font-weight:800}
/* towns */
.town-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;margin-top:1.4rem}
.town-card{background:var(--bg-soft);border:1px solid var(--line);border-radius:var(--radius);
  padding:1.3rem;text-align:center;transition:.18s}
.town-card:hover{background:#fff;box-shadow:0 10px 26px rgba(15,42,74,.1)}
.town-card h3{margin-bottom:.3rem}
.town-card p{font-size:.88rem;color:var(--muted)}
/* faq */
details.faq{background:#fff;border:1px solid var(--line);border-radius:12px;margin-bottom:.7rem;padding:1rem 1.2rem}
details.faq summary{font-weight:700;color:var(--navy);cursor:pointer;list-style:none}
details.faq summary::-webkit-details-marker{display:none}
details.faq summary::after{content:"+";float:right;color:var(--gold);font-size:1.3rem;line-height:1}
details.faq[open] summary::after{content:"–"}
details.faq p{margin-top:.6rem;color:var(--muted)}
/* services page */
.svc-cat{margin-bottom:2.6rem}
.svc-list{display:grid;grid-template-columns:1fr 1fr;gap:1.1rem;margin-top:1.1rem}
.svc{background:#fff;border:1px solid var(--line);border-radius:var(--radius);padding:1.35rem}
.svc h3{font-size:1.08rem}
.svc h3 .tag{font-family:var(--font);font-size:.7rem;background:var(--gold-soft);color:#8a6a1f;
  border-radius:999px;padding:.15rem .6rem;margin-left:.5rem;vertical-align:middle;font-weight:700}
.svc p{font-size:.95rem;color:var(--muted);margin-top:.35rem}
/* contact */
.contact-grid{display:grid;grid-template-columns:1fr 1fr;gap:2rem;align-items:start}
.info-card{background:var(--bg-soft);border:1px solid var(--line);border-radius:var(--radius);padding:1.6rem;margin-bottom:1.1rem}
.info-card h3{margin-bottom:.4rem}
.hours-table{width:100%;border-collapse:collapse;font-size:.95rem}
.hours-table td{padding:.35rem 0;border-bottom:1px dashed var(--line)}
.hours-table td:last-child{text-align:right;font-weight:600}
.map-embed{border:0;width:100%;height:420px;border-radius:var(--radius);box-shadow:0 12px 30px rgba(15,42,74,.1)}
/* cta band */
.cta-band{background:linear-gradient(120deg,var(--navy),var(--navy-2));color:#fff;text-align:center;
  border-radius:var(--radius);padding:2.6rem 1.6rem;margin:1rem 0 0}
.cta-band h2{color:#fff}
.cta-band p{color:#cdd9e7;max-width:36rem;margin:.5rem auto 1.4rem}
.cta-band .btn-row{display:flex;gap:.8rem;justify-content:center;flex-wrap:wrap}
/* footer */
footer{background:var(--navy);color:#c4d2e3;margin-top:3.5rem}
.footer-grid{display:grid;grid-template-columns:1.3fr 1fr 1fr 1.1fr;gap:2rem;padding:2.8rem 0 2rem}
footer h4{color:#fff;font-family:var(--serif);margin-bottom:.8rem;font-size:1.05rem}
footer ul{list-style:none}
footer li{margin-bottom:.45rem;font-size:.93rem}
footer a{color:#c4d2e3}
footer a:hover{color:#fff}
.footer-brand img{width:56px;height:56px;border-radius:50%;object-fit:cover;margin-bottom:.7rem;border:2px solid rgba(255,255,255,.25)}
.footer-bottom{border-top:1px solid rgba(255,255,255,.14);padding:1.1rem 0;font-size:.85rem;
  display:flex;justify-content:space-between;flex-wrap:wrap;gap:.5rem}
/* floating call */
.float-call{position:fixed;right:18px;bottom:18px;z-index:60;width:58px;height:58px;border-radius:50%;
  background:#1faa53;color:#fff;display:flex;align-items:center;justify-content:center;
  box-shadow:0 8px 24px rgba(0,0,0,.25)}
.float-call:hover{transform:scale(1.06)}
.float-call svg{width:28px;height:28px;fill:#fff}
/* breadcrumb */
.crumb{font-size:.85rem;color:var(--muted);margin-bottom:1rem}
.crumb a{color:var(--navy-2)}
/* 404 */
.center{text-align:center;padding:4rem 0}
/* responsive */
@media(max-width:900px){
  .hero-grid,.split,.contact-grid{grid-template-columns:1fr}
  .card-grid{grid-template-columns:1fr 1fr}
  .trust-grid{grid-template-columns:1fr 1fr}
  .town-grid{grid-template-columns:1fr 1fr}
  .footer-grid{grid-template-columns:1fr 1fr}
  .svc-list{grid-template-columns:1fr}
  .hero-photo{max-width:420px}
}
@media(max-width:640px){
  nav.main-nav{display:none;position:absolute;top:100%;left:0;right:0;background:#fff;flex-direction:column;
    align-items:stretch;padding:1rem 20px 1.4rem;border-bottom:1px solid var(--line);gap:0}
  nav.main-nav.open{display:flex}
  nav.main-nav a{padding:.7rem 0;border-bottom:1px solid var(--line)}
  .nav-toggle{display:block}
  .phone-link{display:none}
  .card-grid{grid-template-columns:1fr}
  .header-cta .btn{padding:.55rem 1rem;font-size:.85rem}
}
"""

# ---------------------------------------------------------------- templates
def clinic_jsonld(page_url, description):
    return {
        "@context": "https://schema.org",
        "@type": "MedicalClinic",
        "name": CLINIC["name"],
        "slogan": CLINIC["tagline"],
        "description": description,
        "url": page_url,
        "telephone": CLINIC["phone_tel"],
        "image": f"{BASE_URL}/assets/logo.jpg",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": CLINIC["address"],
            "addressLocality": "Karimnagar",
            "addressRegion": "Telangana",
            "postalCode": "505001",
            "addressCountry": "IN",
        },
        "geo": {"@type": "GeoCoordinates", "latitude": CLINIC["lat"], "longitude": CLINIC["lon"]},
        "openingHoursSpecification": {
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
            "opens": "10:00", "closes": "20:00",
        },
        "medicalSpecialty": ["PlasticSurgery"],
        "founder": {
            "@type": "Physician",
            "name": CLINIC["doctor"],
            "medicalSpecialty": ["PlasticSurgery"],
            "description": f"{CLINIC['doctor']}, {CLINIC['credentials']}; {CLINIC['specialties']}.",
        },
        "areaServed": [{"@type": "City", "name": t} for t in TOWNS],
        "sameAs": [CLINIC["instagram"]],
        "priceRange": "₹₹",
    }

def faq_jsonld(faqs):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in faqs
        ],
    }

def head(title, desc, path, extra_jsonld=None, og_image="/assets/logo.jpg"):
    import json
    url = BASE_URL + path
    schemas = [clinic_jsonld(url, desc)]
    if extra_jsonld:
        schemas.append(extra_jsonld)
    ld = "\n".join(
        '<script type="application/ld+json">\n' + json.dumps(s, ensure_ascii=False, indent=2) + "\n</script>"
        for s in schemas
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{htmllib.escape(title)}</title>
<meta name="description" content="{htmllib.escape(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow">
<meta property="og:type" content="website">
<meta property="og:site_name" content="AR Plastic Surgery">
<meta property="og:title" content="{htmllib.escape(title)}">
<meta property="og:description" content="{htmllib.escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE_URL}{og_image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{htmllib.escape(title)}">
<meta name="twitter:description" content="{htmllib.escape(desc)}">
<meta name="twitter:image" content="{BASE_URL}{og_image}">
<link rel="icon" href="/assets/logo.jpg" type="image/jpeg">
<link rel="stylesheet" href="/assets/style.css">
{ld}
</head>"""

def header(active):
    def a(href, label, key):
        cls = ' class="active"' if key == active else ""
        return f'<a href="{href}"{cls}>{label}</a>'
    return f"""<body>
<header class="site-header" id="siteHeader">
  <div class="wrap header-inner">
    <a class="brand" href="/index.html" aria-label="AR Plastic Surgery home">
      <img src="/assets/logo.jpg" alt="AR Plastic Surgery logo" width="52" height="52">
      <span><span class="brand-name">AR Plastic Surgery</span><br><span class="brand-tag">Precision and Perfection</span></span>
    </a>
    <button class="nav-toggle" id="navToggle" aria-label="Open menu" aria-expanded="false">☰</button>
    <nav class="main-nav" id="mainNav" aria-label="Primary">
      {a('/index.html','Home','home')}
      {a('/about.html','About','about')}
      {a('/services.html','Services','services')}
      {a('/contact.html','Contact','contact')}
    </nav>
    <div class="header-cta">
      <a class="phone-link" href="tel:{CLINIC['phone_tel']}">{CLINIC['phone_display']}</a>
      <a class="btn btn-gold" href="{CLINIC['booking']}" target="_blank" rel="noopener">Book Online</a>
    </div>
  </div>
</header>"""

def footer():
    town_links = "\n".join(
        f'<li><a href="/{t.lower()}-plastic-surgeon.html">Plastic Surgeon in {t}</a></li>'
        for t in ["Siddipet", "Sircilla", "Peddapalli", "Vemulawada"]
    )
    return f"""<footer>
  <div class="wrap footer-grid">
    <div class="footer-brand">
      <img src="/assets/logo.jpg" alt="AR Plastic Surgery logo" width="56" height="56">
      <h4>AR Plastic Surgery</h4>
      <p style="font-size:.93rem">Precision and Perfection. Full-scope plastic, cosmetic, hand &amp; microvascular surgery in Karimnagar, Telangana — led by {CLINIC['doctor']}, {CLINIC['credentials']}.</p>
    </div>
    <div>
      <h4>Explore</h4>
      <ul>
        <li><a href="/index.html">Home</a></li>
        <li><a href="/about.html">About {CLINIC['doctor']}</a></li>
        <li><a href="/services.html">All Services</a></li>
        <li><a href="/contact.html">Contact &amp; Directions</a></li>
        <li><a href="{CLINIC['booking']}" target="_blank" rel="noopener">Book Online</a></li>
      </ul>
    </div>
    <div>
      <h4>Areas We Serve</h4>
      <ul>
        {town_links}
        <li style="color:#8fa2b8;font-size:.88rem">Also: Jagtial, Warangal &amp; nearby districts</li>
      </ul>
    </div>
    <div>
      <h4>Visit Us</h4>
      <ul>
        <li>{CLINIC['address']}</li>
        <li>{CLINIC['hours']}</li>
        <li><a href="tel:{CLINIC['phone_tel']}">{CLINIC['phone_display']}</a></li>
        <li><a href="{CLINIC['instagram']}" target="_blank" rel="noopener">Instagram</a></li>
      </ul>
    </div>
  </div>
  <div class="wrap footer-bottom">
    <span>© 2026 AR Plastic Surgery, Karimnagar. All rights reserved.</span>
    <span>Plastic · Cosmetic · Hand &amp; Microvascular Surgery</span>
  </div>
</footer>
<a class="float-call" href="tel:{CLINIC['phone_tel']}" aria-label="Call AR Plastic Surgery now">
  <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.6 21 3 13.4 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.2.2 2.4.6 3.6.1.3 0 .7-.2 1l-2.3 2.2z"/></svg>
</a>
<script>
(function(){{
  var t=document.getElementById('navToggle'),n=document.getElementById('mainNav'),hd=document.getElementById('siteHeader');
  if(t){{t.addEventListener('click',function(){{var o=n.classList.toggle('open');t.setAttribute('aria-expanded',o);}});}}
  window.addEventListener('scroll',function(){{hd.classList.toggle('scrolled',window.scrollY>8);}},{{passive:true}});
}})();
</script>
</body>
</html>"""

def cta_band():
    return f"""<div class="wrap"><div class="cta-band">
  <h2>Not sure which treatment is right for you?</h2>
  <p>Every plan at AR Plastic Surgery starts with an honest consultation — what surgery can and cannot do, explained before anything is decided.</p>
  <div class="btn-row">
    <a class="btn btn-gold" href="{CLINIC['booking']}" target="_blank" rel="noopener">Book Online</a>
    <a class="btn btn-outline" href="tel:{CLINIC['phone_tel']}">Call {CLINIC['phone_display']}</a>
  </div>
</div></div>"""

def faq_block(faqs):
    items = "\n".join(
        f"<details class=\"faq\"><summary>{htmllib.escape(q)}</summary><p>{a}</p></details>"
        for q, a in faqs
    )
    return f"""<section aria-label="Frequently asked questions"><div class="wrap">
<span class="eyebrow">FAQ</span><h2>Common questions</h2>
<div style="margin-top:1.2rem;max-width:52rem">{items}</div>
</div></section>"""

# ---------------------------------------------------------------- services data
SERVICES = [
 ("Aesthetic Surgery", [
  ("fue-hair-transplant", "FUE Hair Transplantation",
   "Follicular Unit Extraction moves individual hair follicles from denser donor areas to areas of thinning. The technique is designed to avoid a linear scar, leaving tiny dot-like marks instead. Each case is planned around your hairline, density and likely future pattern — and results develop gradually over months, varying from person to person."),
  ("gynecomastia-surgery", "Gynecomastia Surgery",
   "Surgery for enlarged male breast tissue, combining gland and fat removal with chest contouring. Consultations are fully private, and the approach aims for a flatter, more masculine chest contour through discreetly placed incisions."),
  ("liposuction", "Liposuction",
   "Targeted removal of localised fat deposits that persist despite diet and exercise — such as the abdomen, flanks, thighs or chin. It is a body-contouring procedure, not a weight-loss treatment, performed through small incisions and planned around your frame."),
  ("rhinoplasty", "Rhinoplasty",
   "Reshaping of the nose for appearance, breathing, or both. The plan balances facial harmony with function; swelling settles gradually over several months, so the final shape takes time to emerge."),
  ("breast-surgery", "Breast Surgery",
   "Augmentation, reduction and reconstruction. Augmentation aims to enhance proportion; reduction can relieve the physical strain of overly heavy breasts; reconstruction rebuilds the breast after mastectomy or injury. Every plan is individual, and your surgeon will discuss realistic outcomes openly."),
  ("tummy-tuck", "Tummy Tuck (Abdominoplasty)",
   "Removes excess abdominal skin and tightens the underlying muscles — commonly considered after major weight loss or pregnancy. It is not a substitute for weight loss, and the scar is placed low so it can usually be concealed."),
 ]),
 ("Reconstructive & Hand Surgery", [
  ("scar-keloid", "Scar & Keloid Treatment",
   "Surgical revision, injections or combined approaches designed to make scars less noticeable or to release tight, restrictive scars. Keloids can recur after treatment, so your surgeon will explain the plan — and the likely course — honestly before you decide."),
  ("burn-reconstruction", "Burn Reconstruction",
   "Contracture release, skin grafting and staged procedures that aim to restore movement and appearance after burns have healed. Reconstruction is planned step by step, around what matters most to you."),
  ("cleft-lip-palate", "Cleft Lip & Palate Repair",
   "Staged surgical correction of cleft lip and palate, planned from the earliest months of life as part of long-term team care. Early assessment helps map the full journey ahead."),
  ("hand-trauma", "Hand Trauma Surgery",
   "Care for fractures, cuts, crush injuries and dislocations of the hand and wrist. The goal is to restore movement, strength and sensation — and timely assessment gives the best chance of a good recovery."),
  ("tendon-nerve-repair", "Tendon & Nerve Repair",
   "Delicate repair of divided or damaged tendons and nerves, followed by guided rehabilitation. Recovery takes patience and structured hand therapy, which your surgeon will coordinate."),
  ("microsurgery", "Microsurgery",
   "Surgery under high magnification to rejoin tiny blood vessels and nerves — the foundation of replantation surgery and complex reconstruction after trauma."),
  ("artery-repair", "Artery Repair Surgery",
   "Repair of damaged arteries, often in the hand and limbs after injury, to restore blood flow. Vascular injuries are time-sensitive, so urgent assessment matters."),
  ("lipoma-removal", "Lipoma Removal",
   "Removal of benign fatty lumps through small incisions, with attention to the final scar. Most lipomas are harmless — but any new, growing or painful lump should be examined first."),
 ]),
 ("Non-Surgical Aesthetics", [
  ("botox", "Botox",
   "Relaxes targeted facial muscles to soften expression lines such as frown lines and crow's feet. Effects are temporary — typically lasting a few months — and maintenance sessions are needed to sustain them."),
  ("dermal-fillers", "Dermal Fillers",
   "Adds volume to soften folds or restore contour in areas like the cheeks and lips. Results are temporary and vary between individuals; your doctor will recommend the product and amount suited to your face."),
  ("prp", "PRP Therapy",
   "Uses concentrated platelets from your own blood, applied to the scalp or skin to support hair and skin quality. The evidence base is still developing — your doctor will explain candidly what PRP can and cannot do for your concern."),
  ("chemical-peels", "Chemical Peels",
   "Controlled exfoliation to improve skin texture, tone and superficial marks. The depth of the peel is matched to your skin type and concern, with aftercare guidance for the healing days."),
  ("laser-treatments", "Laser Treatments",
   "Light-based treatments for unwanted hair, pigmentation and skin texture. Multiple sessions are usually needed, and suitability depends on your skin type — assessed at consultation."),
 ]),
]

def services_grid(ids=None, link_contact=True):
    out = []
    for cat, items in SERVICES:
        cards = []
        for sid, name, desc in items:
            if ids and sid not in ids:
                continue
            cards.append(
                f'<article class="svc" id="{sid}"><h3>{htmllib.escape(name)}</h3><p>{desc}</p></article>'
            )
        if cards:
            out.append(f'<div class="svc-cat"><h2 style="font-size:1.4rem">{cat}</h2>'
                       f'<div class="svc-list">{"".join(cards)}</div></div>')
    return "\n".join(out)

# ---------------------------------------------------------------- index.html
INDEX_FAQS = [
 ("What is the difference between plastic surgery and cosmetic surgery?",
  "Plastic surgery focuses on restoring form and function — treating burns, injuries, congenital conditions, hand and nerve damage, and scars. Cosmetic surgery focuses on refining and enhancing appearance, from rhinoplasty and hair transplantation to Botox and fillers. Both should be performed by a qualified plastic surgeon."),
 ("Do I need a referral to book a consultation?",
  "No. You can call us directly on +91 91826 56866 or use our online booking page to reserve a slot. Walk-in consultations are also welcome during clinic hours, subject to availability."),
 ("Which towns do you serve?",
  "The clinic is in Karimnagar and regularly receives patients from Jagtial, Sircilla, Warangal, Siddipet, Peddapalli, Vemulawada and nearby districts across Telangana."),
 ("What are your clinic hours?",
  "We are open every day — Monday to Sunday — from 10:00 AM to 8:00 PM."),
 ("How do I book an appointment?",
  "Call +91 91826 56866 or book online through our booking page. Booking ahead helps us give your consultation unhurried time."),
 ("Is my consultation confidential?",
  "Yes. All consultations at AR Plastic Surgery are private, and your information is handled with strict confidentiality."),
]

def page_index():
    title = "AR Plastic Surgery | Plastic Surgeon in Karimnagar"
    desc = ("Dr Ashok Reddy (MBBS, DNB, M.Ch, Gold Medalist) leads AR Plastic Surgery, Karimnagar — "
            "plastic, cosmetic, hand & microvascular surgery. Open daily 10 AM–8 PM.")
    svc_cards = [
        ("✂️", "Aesthetic Surgery",
         "Hair transplant, gynecomastia surgery, liposuction, rhinoplasty, breast surgery and tummy tuck — planned and performed by a qualified plastic surgeon.",
         "/services.html#fue-hair-transplant"),
        ("🤲", "Reconstructive & Hand Surgery",
         "Burn reconstruction, cleft repair, scar revision, hand trauma, tendon & nerve repair and microsurgery — restoring form and function.",
         "/services.html#scar-keloid"),
        ("✨", "Non-Surgical Aesthetics",
         "Botox, dermal fillers, PRP, chemical peels and laser treatments — subtle, doctor-led rejuvenation without surgery.",
         "/services.html#botox"),
    ]
    cards = "\n".join(
        f'<article class="card"><div class="icon" aria-hidden="true">{i}</div><h3>{t}</h3><p>{p}</p>'
        f'<a class="more" href="{l}">Explore services →</a></article>'
        for i, t, p, l in svc_cards
    )
    town_cards = "\n".join(
        f'<a class="town-card" href="/{t.lower()}-plastic-surgeon.html"><h3>{t}</h3><p>Plastic surgeon for {t} patients</p></a>'
        for t in ["Siddipet", "Sircilla", "Peddapalli", "Vemulawada"]
    )
    body = f"""
<main>
<section class="hero"><div class="wrap hero-grid">
  <div>
    <span class="eyebrow">Karimnagar · Telangana</span>
    <h1>Plastic, Cosmetic &amp; Hand Surgery — <span class="accent">Precision and Perfection</span></h1>
    <p class="lede">AR Plastic Surgery is Karimnagar's full-scope plastic surgery practice, led by {CLINIC['doctor']} — {CLINIC['credentials']}, {CLINIC['specialties']}.</p>
    <div class="hero-badges">
      <span class="badge"><b>Gold Medalist</b> plastic surgeon</span>
      <span class="badge">Open <b>every day</b> 10 AM – 8 PM</span>
      <span class="badge"><b>4.9★</b> rated on Google</span>
    </div>
    <div class="btn-row" style="display:flex;gap:.8rem;flex-wrap:wrap">
      <a class="btn btn-gold" href="{CLINIC['booking']}" target="_blank" rel="noopener">Book Online</a>
      <a class="btn btn-outline" href="tel:{CLINIC['phone_tel']}">Call {CLINIC['phone_display']}</a>
    </div>
  </div>
  <figure class="hero-photo">
    <img src="/assets/dr-ashok-reddy.jpg" alt="{CLINIC['doctor']}, plastic surgeon at AR Plastic Surgery Karimnagar" width="640" height="704" fetchpriority="high">
    <figcaption>{CLINIC['doctor']} — {CLINIC['credentials']}</figcaption>
  </figure>
</div></section>

<div class="trust"><div class="wrap trust-grid">
  <div class="t"><b>Gold Medalist</b><span>M.Ch Plastic Surgery</span></div>
  <div class="t"><b>19</b><span>Surgeon-led services</span></div>
  <div class="t"><b>7 days</b><span>Open Mon–Sun, 10 AM–8 PM</span></div>
  <div class="t"><b>17 towns</b><span>Service area across Telangana</span></div>
</div></div>

<section><div class="wrap">
  <span class="eyebrow">What we treat</span>
  <h2>Complete plastic surgery, under one roof</h2>
  <p class="lede">From reconstructive surgery after trauma and burns to cosmetic procedures and non-surgical aesthetics — every treatment is planned by a qualified plastic surgeon.</p>
  <div class="card-grid">{cards}</div>
</div></section>

<section style="background:var(--bg-soft)"><div class="wrap split">
  <img class="doc" src="/assets/dr-ashok-reddy.jpg" alt="Portrait of {CLINIC['doctor']}" width="540" height="648" loading="lazy">
  <div>
    <span class="eyebrow">Meet your surgeon</span>
    <h2>{CLINIC['doctor']}</h2>
    <p><strong>{CLINIC['credentials']}</strong><br>{CLINIC['specialties']}.</p>
    <ul class="checklist">
      <li>Honest consultations — what surgery can and cannot do, explained first</li>
      <li>Safety-first planning with natural-looking results as the goal</li>
      <li>Full-scope expertise: cosmetic, reconstructive, hand &amp; microvascular</li>
      <li>Strict confidentiality for every patient</li>
    </ul>
    <a class="btn btn-solid" href="/about.html">More about {CLINIC['doctor']} →</a>
  </div>
</div></section>

<section><div class="wrap">
  <span class="eyebrow">Areas we serve</span>
  <h2>Karimnagar's plastic surgery practice for all of Telangana</h2>
  <p class="lede">Patients visit us from across the region — including Jagtial, Warangal and nearby districts. Dedicated guides for our neighbouring towns:</p>
  <div class="town-grid">{town_cards}</div>
</div></section>

{faq_block(INDEX_FAQS)}
{cta_band()}
</main>"""
    return head(title, desc, "/index.html", faq_jsonld(INDEX_FAQS)) + header("home") + body + footer()

# ---------------------------------------------------------------- about.html
def page_about():
    title = "About Dr Ashok Reddy | AR Plastic Surgery Karimnagar"
    desc = ("Meet Dr Ashok Reddy — MBBS, DNB (Mumbai), M.Ch (Delhi), Gold Medalist in plastic, "
            "cosmetic, hand & microvascular surgery at AR Plastic Surgery, Karimnagar.")
    body = f"""
<main><section><div class="wrap">
  <nav class="crumb" aria-label="Breadcrumb"><a href="/index.html">Home</a> › About</nav>
  <span class="eyebrow">About the clinic</span>
  <h1>{CLINIC['doctor']} &amp; AR Plastic Surgery</h1>
  <p class="lede">A surgeon-led practice built on a simple standard: precision and perfection — in planning, in technique, and in aftercare.</p>
</div></section>
<section style="padding-top:0"><div class="wrap split">
  <img class="doc" src="/assets/dr-ashok-reddy.jpg" alt="{CLINIC['doctor']}, {CLINIC['specialties']}, AR Plastic Surgery Karimnagar" width="540" height="648">
  <div>
    <h2>{CLINIC['doctor']}</h2>
    <p><strong>{CLINIC['credentials']}</strong></p>
    <p>{CLINIC['specialties']}.</p>
    <p>{CLINIC['doctor']} trained at premier institutions — DNB in Mumbai and M.Ch in plastic surgery in Delhi, earning a Gold Medal — before establishing AR Plastic Surgery in Karimnagar to bring full-scope specialist care closer to home for Telangana's patients.</p>
    <p>His practice spans the complete breadth of the specialty: cosmetic procedures such as hair transplantation, gynecomastia surgery and rhinoplasty; reconstructive work including burns, cleft repair and scar revision; and the demanding field of hand &amp; microvascular surgery — tendon, nerve and artery repair under magnification.</p>
    <ul class="checklist">
      <li>Consultations that start with listening, not selling</li>
      <li>Clear explanation of options, recovery and realistic outcomes</li>
      <li>Continuity of care — the surgeon who plans your treatment performs it</li>
    </ul>
  </div>
</div></section>
<section style="background:var(--bg-soft)"><div class="wrap">
  <span class="eyebrow">Our philosophy</span>
  <h2>Why "Precision and Perfection"</h2>
  <div class="card-grid">
    <article class="card"><div class="icon" aria-hidden="true">🎯</div><h3>Precision in planning</h3><p>No two faces, hands or bodies are alike. Every treatment begins with careful assessment and a plan tailored to the individual — never a one-size-fits-all protocol.</p></article>
    <article class="card"><div class="icon" aria-hidden="true">🛡️</div><h3>Safety first</h3><p>Elective or essential, every procedure is weighed for risk and benefit with you. If surgery is not the right answer, you will be told so.</p></article>
    <article class="card"><div class="icon" aria-hidden="true">🤝</div><h3>Honest conversations</h3><p>What a procedure can and cannot achieve, how recovery really feels, and what results to reasonably expect — discussed openly before anything is decided.</p></article>
  </div>
</div></section>
<section><div class="wrap">
  <span class="eyebrow">Visit us</span>
  <h2>The clinic</h2>
  <p>AR Plastic Surgery is located at {CLINIC['address']}, open <strong>{CLINIC['hours']}</strong>. Patients travel to us from {", ".join(TOWNS[:-1])} and {TOWNS[-1]}, and nearby districts.</p>
  <p style="margin-top:1rem"><a class="btn btn-solid" href="/contact.html">Directions &amp; contact →</a>
  <a class="btn btn-outline" href="/services.html" style="margin-left:.6rem">View services →</a></p>
</div></section>
{cta_band()}
</main>"""
    return head(title, desc, "/about.html") + header("about") + body + footer()

# ---------------------------------------------------------------- services.html
def page_services():
    title = "Plastic & Cosmetic Surgery Services | AR Karimnagar"
    desc = ("Explore 19 surgeon-led services at AR Plastic Surgery, Karimnagar: hair transplant, "
            "gynecomastia, liposuction, rhinoplasty, hand surgery, Botox, lasers & more.")
    body = f"""
<main><section><div class="wrap">
  <nav class="crumb" aria-label="Breadcrumb"><a href="/index.html">Home</a> › Services</nav>
  <span class="eyebrow">Our services</span>
  <h1>Plastic, cosmetic &amp; reconstructive surgery services</h1>
  <p class="lede">Nineteen treatments across aesthetic surgery, reconstructive &amp; hand surgery, and non-surgical aesthetics — each described plainly, so you know what to expect. Every plan starts with a consultation at our Karimnagar clinic.</p>
  <div style="margin-top:2rem">{services_grid()}</div>
  <p style="margin-top:1.6rem;color:var(--muted);font-size:.95rem">Results vary from person to person. Your surgeon will discuss realistic outcomes, recovery and alternatives at your consultation — before anything is decided.</p>
</div></section>
{cta_band()}
</main>"""
    return head(title, desc, "/services.html") + header("services") + body + footer()

# ---------------------------------------------------------------- town pages
def town_page(town, title, desc, h1_intro, sections_html, faqs):
    town_links = " · ".join(
        f'<a href="/{t.lower()}-plastic-surgeon.html">{t}</a>'
        for t in ["Siddipet", "Sircilla", "Peddapalli", "Vemulawada"] if t != town
    )
    body = f"""
<main><section><div class="wrap">
  <nav class="crumb" aria-label="Breadcrumb"><a href="/index.html">Home</a> › Plastic surgeon for {town} patients</nav>
  <span class="eyebrow">{town} · Telangana</span>
  <h1>Plastic Surgeon for {town} Patients</h1>
  <p class="lede">{h1_intro}</p>
</div></section>
<section style="padding-top:0"><div class="wrap">
{sections_html}
<div class="info-card" style="margin-top:2rem">
  <h3>Visiting from {town}</h3>
  <p><strong>Address:</strong> {CLINIC['address']}<br>
  <strong>Hours:</strong> {CLINIC['hours']}<br>
  <strong>Phone:</strong> <a href="tel:{CLINIC['phone_tel']}">{CLINIC['phone_display']}</a></p>
  <p style="margin-top:.8rem"><a class="btn btn-gold" href="{CLINIC['booking']}" target="_blank" rel="noopener">Book Online</a>
  <a class="btn btn-outline" href="/contact.html" style="margin-left:.6rem">Directions →</a></p>
</div>
<p style="margin-top:1.4rem;font-size:.93rem;color:var(--muted)">Also serving: {town_links}</p>
</div></section>
{faq_block(faqs)}
{cta_band()}
</main>"""
    return (head(title, desc, f"/{town.lower()}-plastic-surgeon.html", faq_jsonld(faqs))
            + header("") + body + footer())

def page_siddipet():
    return town_page(
        "Siddipet",
        "Plastic Surgeon for Siddipet | AR Plastic Surgery",
        ("Siddipet patients visit AR Plastic Surgery, Karimnagar for hand surgery, cleft repair, "
         "burn reconstruction & cosmetic procedures by Dr Ashok Reddy, Gold Medalist."),
        ("Siddipet has good skin and hair clinics — but some treatments need a full-scope plastic surgeon, "
         "not a skin clinic. For hand surgery, cleft repair and burn reconstruction, our October 2026 review "
         "of local listings found no dedicated local provider; the nearest full-scope option is AR Plastic Surgery in Karimnagar."),
        """<h2>Care that is hard to find locally in Siddipet</h2>
<p>Led by <strong>Dr Ashok Reddy — MBBS, DNB (Mumbai), M.Ch (Delhi), Gold Medalist</strong>, plastic, cosmetic, hand &amp; microvascular surgeon, the clinic covers the procedures local listings rarely offer:</p>
<ul class="checklist">
<li><strong>Hand surgery &amp; microvascular repair</strong> — tendon injuries, fractures, nerve repair and microsurgical reconstruction.</li>
<li><strong>Cleft lip &amp; palate repair</strong> — staged surgical correction, planned from the earliest months of life.</li>
<li><strong>Burn reconstruction</strong> — contracture release and staged rebuilding after burns have healed.</li>
<li><strong>Scar revision, skin grafting, facial trauma</strong> — reconstructive procedures that need a plastic surgeon's planning.</li>
</ul>
<h2 style="margin-top:1.8rem">Surgeon-led cosmetic care</h2>
<p>For <a href="/services.html#fue-hair-transplant">hair transplant</a>, <a href="/services.html#gynecomastia-surgery">gynecomastia surgery</a>, <a href="/services.html#liposuction">liposuction</a> and <a href="/services.html#rhinoplasty">rhinoplasty</a>, the difference at AR is that every case is planned and performed by a qualified plastic surgeon — not delegated. Consultations are confidential. <strong>Free OP consultations are available every Wednesday.</strong></p>
<p>Many Siddipet patients combine their consultation with a single day trip. Call or book online to reserve your slot.</p>""",
        [
         ("Do you treat patients from Siddipet?",
          "Yes — patients from Siddipet and other towns across Telangana visit the Karimnagar clinic regularly."),
         ("Is hand surgery available without going to Hyderabad?",
          "Yes. Dr Ashok Reddy is a trained hand & microvascular surgeon, and the clinic manages hand injuries and tendon and nerve problems without referral to Hyderabad."),
         ("How do I book?",
          "Call +91 91826 56866 or use the online booking page. Wednesday OP consultations are free."),
        ])

def page_sircilla():
    return town_page(
        "Sircilla",
        "Plastic Surgeon for Sircilla | AR Plastic Surgery",
        ("A real plastic surgery practice near Sircilla — AR Plastic Surgery, Karimnagar. Gynecomastia, "
         "liposuction, hair transplant & hand surgery by Dr Ashok Reddy."),
        ("Search for plastic surgery from Sircilla and you will mostly find directory listings and out-of-town "
         "hospital chains. Behind those listings, patients still need one thing: a real plastic surgeon, reachable "
         "nearby. AR Plastic Surgery in Karimnagar is that practice — a dedicated plastic, cosmetic, hand &amp; "
         "microvascular surgery clinic, not a skin clinic and not a listing page."),
        """<h2>Procedures Sircilla patients ask about most</h2>
<ul class="checklist">
<li><strong><a href="/services.html#gynecomastia-surgery">Gynecomastia surgery</a></strong> — confidential consultations and a scar-minimal approach, performed by a gold-medalist plastic surgeon.</li>
<li><strong><a href="/services.html#liposuction">Liposuction &amp; body contouring</a></strong> — targeted fat removal through small, discreet incisions, planned around your frame.</li>
<li><strong><a href="/services.html#lipoma-removal">Lipoma removal</a> &amp; scar revision</strong> — small procedures, done precisely, with attention to the final scar.</li>
<li><strong><a href="/services.html#fue-hair-transplant">Hair transplant (FUE)</a></strong> — surgeon-led, planned by Dr Reddy personally.</li>
<li><strong>Hand surgery, burn reconstruction, skin grafting</strong> — reconstructive care with no dedicated local provider in Sircilla.</li>
</ul>
<h2 style="margin-top:1.8rem">What to expect</h2>
<p>Every treatment begins with an honest consultation: what surgery can and cannot do, the plan, the recovery — explained before anything is decided. <strong>Free OP consultations every Wednesday.</strong> Led by <strong>Dr Ashok Reddy — MBBS, DNB (Mumbai), M.Ch (Delhi), Gold Medalist</strong>; the clinic holds a 4.9-star Google rating and is open <strong>every day, 10:00 AM – 8:00 PM</strong>.</p>
<p>Sircilla is a short drive from Karimnagar — most consultations fit into a single visit.</p>""",
        [
         ("Do you treat patients from Sircilla?",
          "Yes — Sircilla is within the clinic's regular service area, alongside other Telangana towns."),
         ("Is gynecomastia surgery confidential?",
          "Yes. Consultations are private, and the procedure uses a scar-minimal approach."),
         ("How do I book?",
          "Call +91 91826 56866 or book online. Wednesday OP consultations are free."),
        ])

def page_peddapalli():
    return town_page(
        "Peddapalli",
        "Plastic Surgeon for Peddapalli | AR Plastic Surgery",
        ("Peddapalli patients choose AR Plastic Surgery, Karimnagar for rhinoplasty, facelift, burns, cleft "
         "& cosmetic surgery by gold-medalist Dr Ashok Reddy."),
        ("Search for a plastic surgeon in Peddapalli and you will mostly find pages written for the town — not "
         "surgeons in it. Our October 2026 review found no local provider at all for rhinoplasty, facelift, "
         "blepharoplasty (eyelid surgery), skin grafting, burn reconstruction or cleft repair. AR Plastic Surgery "
         "is the real practice behind the keywords: a full-scope plastic surgery clinic in nearby Karimnagar."),
        """<h2>The specialist Peddapalli's search results are missing</h2>
<p>If you live in Peddapalli and need any of these, the genuine specialist option is Dr Ashok Reddy's practice in Karimnagar — led by <strong>Dr Ashok Reddy, MBBS, DNB (Mumbai), M.Ch (Delhi), Gold Medalist</strong>, plastic, cosmetic, hand &amp; microvascular surgeon.</p>
<h2 style="margin-top:1.6rem">Procedures worth the trip from Peddapalli</h2>
<ul class="checklist">
<li><strong><a href="/services.html#rhinoplasty">Rhinoplasty</a></strong> — functional and aesthetic nose correction, planned for your face.</li>
<li><strong>Facelift &amp; blepharoplasty</strong> — facial rejuvenation with natural-looking results as the goal.</li>
<li><strong><a href="/services.html#burn-reconstruction">Burn reconstruction</a> &amp; skin grafting</strong> — staged rebuilding after burns and complex wounds.</li>
<li><strong><a href="/services.html#cleft-lip-palate">Cleft lip &amp; palate repair</a></strong> — staged correction from the earliest months of life.</li>
<li><strong>Hair transplant (FUE), gynecomastia, liposuction, tummy tuck, scar revision</strong> — the full cosmetic and reconstructive range, all surgeon-led.</li>
</ul>
<p style="margin-top:1.2rem"><strong>Free OP consultations every Wednesday.</strong> One trip covers consultation and planning; surgery and follow-ups are scheduled around you. Before choosing any clinic, check who actually performs the surgery — AR's procedures are done by a qualified plastic surgeon at a real clinic you can visit.</p>""",
        [
         ("Do you treat patients from Peddapalli?",
          "Yes — Peddapalli is one of the towns the clinic regularly serves across Telangana."),
         ("Why not just pick the top-ranked page for my town?",
          "Rankings can be bought with town-targeted pages. Check who actually performs the surgery: AR's procedures are done by a qualified plastic surgeon at a real clinic you can visit in Karimnagar."),
         ("How do I book?",
          "Call +91 91826 56866 or use the online booking page."),
        ])

def page_vemulawada():
    return town_page(
        "Vemulawada",
        "Plastic Surgeon for Vemulawada | AR Plastic Surgery",
        ("Hand & microvascular surgery, breast procedures, burns and cosmetic care for Vemulawada patients "
         "at AR Plastic Surgery, Karimnagar. Dr Ashok Reddy."),
        ("Vemulawada has almost no local plastic surgery presence — our October 2026 review found no local "
         "provider for hand surgery, facelift, burns or cleft care, and only directory listings for the rest. "
         "The nearest full-scope option is AR Plastic Surgery in Karimnagar, a short journey away."),
        """<h2>Hand surgery — the specialty nobody local offers</h2>
<p><strong>Dr Ashok Reddy — MBBS, DNB (Mumbai), M.Ch (Delhi), Gold Medalist</strong> — is a trained <strong>hand &amp; microvascular surgeon</strong>: tendon and nerve repair, fractures, and microsurgical reconstruction. Across every town we studied, hand surgery has no local competition. If you are in Vemulawada with a hand injury or deformity, this is the closest specialist care — without the trip to Hyderabad.</p>
<h2 style="margin-top:1.8rem">Procedures Vemulawada patients travel for</h2>
<ul class="checklist">
<li><strong><a href="/services.html#hand-trauma">Hand &amp; microvascular surgery</a></strong> — tendon, nerve and artery repair under magnification.</li>
<li><strong><a href="/services.html#breast-surgery">Breast reduction &amp; augmentation</a></strong> — surgeon-led breast surgery with full aftercare.</li>
<li><strong><a href="/services.html#burn-reconstruction">Burn reconstruction</a>, skin grafting, scar revision</strong> — staged, specialist care.</li>
<li><strong>Facelift, <a href="/services.html#cleft-lip-palate">cleft repair</a></strong> — genuine expertise a short trip away.</li>
<li><strong>Hair transplant (FUE), gynecomastia, liposuction, rhinoplasty</strong> — cosmetic procedures planned and performed by the surgeon himself.</li>
</ul>
<p style="margin-top:1.2rem">The clinic holds a <strong>4.9-star Google rating</strong> and is open <strong>every day, 10:00 AM – 8:00 PM</strong>. <strong>Free OP consultations every Wednesday.</strong> Many patients complete consultation and planning in a single visit.</p>""",
        [
         ("Do you treat patients from Vemulawada?",
          "Yes — Vemulawada is within the clinic's service area across Telangana."),
         ("I injured my hand — do I need to go to Hyderabad?",
          "Not necessarily. Dr Reddy's hand & microvascular training covers most hand injuries and tendon and nerve problems right here in Karimnagar."),
         ("How do I book?",
          "Call +91 91826 56866 or book online. Wednesday OP consultations are free."),
        ])

# ---------------------------------------------------------------- contact.html
def page_contact():
    title = "Contact & Book Appointment | AR Plastic Surgery"
    desc = ("Visit AR Plastic Surgery, Opp Reddy gari vantillu, Court Chowrasta, Karimnagar. "
            "Open Mon–Sun 10 AM–8 PM. Call +91 91826 56866 or book online.")
    map_q = "AR+Plastic+Surgery+Karimnagar+Telangana"
    body = f"""
<main><section><div class="wrap">
  <nav class="crumb" aria-label="Breadcrumb"><a href="/index.html">Home</a> › Contact</nav>
  <span class="eyebrow">Get in touch</span>
  <h1>Contact &amp; book your appointment</h1>
  <p class="lede">Call, book online, or walk in during clinic hours — every consultation starts with an honest conversation.</p>
</div></section>
<section style="padding-top:0"><div class="wrap contact-grid">
  <div>
    <div class="info-card">
      <h3>📍 Clinic address</h3>
      <p>{CLINIC['name']}<br>{CLINIC['address']}</p>
      <p style="margin-top:.8rem"><a class="btn btn-solid" href="https://www.google.com/maps/search/?api=1&amp;query={map_q}" target="_blank" rel="noopener">Get Directions</a></p>
    </div>
    <div class="info-card">
      <h3>📞 Phone &amp; booking</h3>
      <p><a href="tel:{CLINIC['phone_tel']}" style="font-size:1.3rem;font-weight:800;color:var(--navy)">{CLINIC['phone_display']}</a></p>
      <p style="margin-top:.8rem"><a class="btn btn-gold" href="{CLINIC['booking']}" target="_blank" rel="noopener">Book Online</a></p>
    </div>
    <div class="info-card">
      <h3>🕙 Clinic hours</h3>
      <table class="hours-table">
        <tr><td>Monday – Sunday</td><td>10:00 AM – 8:00 PM</td></tr>
      </table>
      <p style="margin-top:.6rem;font-size:.92rem;color:var(--muted)">Open all seven days. Booking ahead is recommended.</p>
    </div>
    <div class="info-card">
      <h3>🗺️ Areas we serve</h3>
      <p>{", ".join(TOWNS)} and nearby districts. <a href="/siddipet-plastic-surgeon.html">Siddipet</a> · <a href="/sircilla-plastic-surgeon.html">Sircilla</a> · <a href="/peddapalli-plastic-surgeon.html">Peddapalli</a> · <a href="/vemulawada-plastic-surgeon.html">Vemulawada</a> patients — see your town guide.</p>
    </div>
  </div>
  <div>
    <iframe class="map-embed" title="Map — AR Plastic Surgery, Karimnagar"
      src="https://www.google.com/maps?q={map_q}&amp;output=embed"
      loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
    <p style="margin-top:.8rem;font-size:.93rem;color:var(--muted)">Find us opposite Reddy gari vantillu on Malkapur Road, near Court Chowrasta, Jyothinagar, Karimnagar.</p>
  </div>
</div></section>
{cta_band()}
</main>"""
    return head(title, desc, "/contact.html") + header("contact") + body + footer()

# ---------------------------------------------------------------- 404.html
def page_404():
    title = "Page Not Found | AR Plastic Surgery"
    desc = "The page you are looking for could not be found. Return to AR Plastic Surgery, Karimnagar."
    body = """<main><section class="center"><div class="wrap">
<span class="eyebrow">404</span>
<h1>That page isn't here</h1>
<p class="lede" style="margin:0 auto 1.6rem">The page you were looking for may have moved. Here are some useful places instead:</p>
<p><a class="btn btn-solid" href="/index.html">Home</a>
<a class="btn btn-outline" href="/services.html" style="margin-left:.6rem">Services</a>
<a class="btn btn-outline" href="/contact.html" style="margin-left:.6rem">Contact</a></p>
</div></section></main>"""
    return head(title, desc, "/404.html") + header("") + body + footer()

# ---------------------------------------------------------------- build + validate
PAGES = [
    ("index.html", page_index),
    ("about.html", page_about),
    ("services.html", page_services),
    ("siddipet-plastic-surgeon.html", page_siddipet),
    ("sircilla-plastic-surgeon.html", page_sircilla),
    ("peddapalli-plastic-surgeon.html", page_peddapalli),
    ("vemulawada-plastic-surgeon.html", page_vemulawada),
    ("contact.html", page_contact),
    ("404.html", page_404),
]

class Checker(HTMLParser):
    def __init__(self):
        super().__init__()
        self.h1 = 0; self.title = ""; self.desc = ""; self._in_title = False
        self.errors = []
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "h1": self.h1 += 1
        if tag == "title": self._in_title = True
        if tag == "meta" and d.get("name") == "description": self.desc = d.get("content", "")
        if tag == "img" and not d.get("alt"): self.errors.append("img missing alt")
    def handle_endtag(self, tag):
        if tag == "title": self._in_title = False
    def handle_data(self, data):
        if self._in_title: self.title += data

BANNED = [r"\bbest plastic surgeon\b", r"\bguarantee[ds]?\b", r"\bpermanent results?\b",
          r"\bpainless\b", r"\bscarless\b", r"\b100%\b", r"\bno\.?\s*1\b"]

def main():
    os.makedirs(os.path.join(OUT, "assets"), exist_ok=True)
    with open(os.path.join(OUT, "assets", "style.css"), "w") as f:
        f.write(CSS)
    sitemap_urls = []
    for fname, fn in PAGES:
        page_html = fn()
        path = os.path.join(OUT, fname)
        with open(path, "w") as f:
            f.write(page_html)
        # validate
        c = Checker()
        try:
            c.feed(page_html)
        except Exception as e:
            print(f"!! PARSE ERROR {fname}: {e}")
        tl, dl = len(c.title.strip()), len(c.desc.strip())
        flags = []
        if fname != "404.html" and c.h1 != 1: flags.append(f"h1 count={c.h1}")
        if not (45 <= tl <= 68): flags.append(f"title len={tl}")
        if not (140 <= dl <= 168): flags.append(f"desc len={dl}")
        flags += c.errors
        for pat in BANNED:
            if re.search(pat, page_html, re.I):
                flags.append(f"banned phrase: {pat}")
        status = "OK " if not flags else "WARN " + "; ".join(flags)
        print(f"{status} {fname} | title[{tl}] {c.title.strip()[:60]} | desc[{dl}]")
        if fname != "404.html":
            sitemap_urls.append(fname)
    # robots.txt
    with open(os.path.join(OUT, "robots.txt"), "w") as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: {BASE_URL}/sitemap.xml\n")
    # sitemap.xml
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.0.9">']
    for u in sitemap_urls:
        sm.append(f"  <url><loc>{BASE_URL}/{u}</loc><changefreq>monthly</changefreq><priority>0.8</priority></url>")
    sm.append("</urlset>")
    with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
        f.write("\n".join(sm))
    print(f"\nsitemap: {len(sitemap_urls)} urls | robots.txt written")

if __name__ == "__main__":
    main()
