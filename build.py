#!/usr/bin/env python3
"""Static site generator for AR Plastic Surgery (Karimnagar).
Generates plain HTML/CSS with no build step at serve time.
Run: python3 build.py
"""
import os, re, html as htmllib
from html.parser import HTMLParser

from content_proc_a import PROCEDURES_A
from content_proc_b import PROCEDURES_B
from content_blog import POSTS

PROCEDURES = PROCEDURES_A + PROCEDURES_B
PROC_BY_SLUG = {p["slug"]: p for p in PROCEDURES}
POST_BY_SLUG = {p["slug"]: p for p in POSTS}

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
TOWNS = ["Karimnagar", "Jagtial", "Sircilla", "Warangal", "Siddipet", "Peddapalli", "Vemulawada",
         "Nizamabad", "Khammam", "Mancherial", "Adilabad", "Bhadradri Kothagudem", "Hanamkonda",
         "Hyderabad", "Jangaon", "Jayashankar Bhupalpally", "Jogulamba Gadwal", "Kamareddy",
         "Komaram Bheem Asifabad", "Mahabubabad", "Mahabubnagar", "Medak", "Medchal-Malkajgiri",
         "Mulugu", "Nagarkurnool", "Nalgonda", "Narayanpet", "Nirmal", "Rangareddy", "Sangareddy",
         "Suryapet", "Vikarabad", "Wanaparthy", "Yadadri Bhuvanagiri"]
# (display name, url slug) for every town/district guide page
DISTRICT_PAGES = [
    ("Siddipet", "siddipet"), ("Sircilla", "sircilla"),
    ("Peddapalli", "peddapalli"), ("Vemulawada", "vemulawada"),
    ("Warangal", "warangal"), ("Nizamabad", "nizamabad"), ("Khammam", "khammam"),
    ("Mancherial", "mancherial"), ("Jagtial", "jagtial"), ("Adilabad", "adilabad"),
    ("Bhadradri Kothagudem", "bhadradri-kothagudem"), ("Hanamkonda", "hanamkonda"),
    ("Hyderabad", "hyderabad"), ("Jangaon", "jangaon"),
    ("Jayashankar Bhupalpally", "jayashankar-bhupalpally"),
    ("Jogulamba Gadwal", "jogulamba-gadwal"), ("Kamareddy", "kamareddy"),
    ("Komaram Bheem Asifabad", "komaram-bheem-asifabad"), ("Mahabubabad", "mahabubabad"),
    ("Mahabubnagar", "mahabubnagar"), ("Medak", "medak"),
    ("Medchal-Malkajgiri", "medchal-malkajgiri"), ("Mulugu", "mulugu"),
    ("Nagarkurnool", "nagarkurnool"), ("Nalgonda", "nalgonda"), ("Narayanpet", "narayanpet"),
    ("Nirmal", "nirmal"), ("Peddapalli District", "peddapalli-district"),
    ("Rajanna Sircilla", "rajanna-sircilla"), ("Rangareddy", "rangareddy"),
    ("Sangareddy", "sangareddy"), ("Siddipet District", "siddipet-district"),
    ("Suryapet", "suryapet"), ("Vikarabad", "vikarabad"), ("Wanaparthy", "wanaparthy"),
    ("Yadadri Bhuvanagiri", "yadadri-bhuvanagiri"),
]
# legacy alias kept for compatibility
DISTRICTS = [d for d, _ in DISTRICT_PAGES]

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
/* blog */
.byline{color:var(--muted);font-size:.92rem;margin:.4rem 0 1.6rem}
.post-list{display:grid;gap:1.1rem;margin-top:1.6rem}
.post-card{background:#fff;border:1px solid var(--line);border-radius:var(--radius);padding:1.5rem;transition:.18s}
.post-card:hover{box-shadow:0 12px 30px rgba(15,42,74,.1)}
.post-card .post-date{font-size:.82rem;color:var(--gold);font-weight:700;letter-spacing:.06em;text-transform:uppercase}
.post-card h3{margin:.35rem 0 .4rem;font-size:1.25rem}
.post-card p{color:var(--muted);font-size:.96rem}
.rel-box{background:var(--bg-soft);border:1px solid var(--line);border-radius:var(--radius);padding:1.4rem 1.6rem;margin-top:2.2rem}
.rel-box h3{margin-bottom:.6rem}
.rel-box ul{list-style:none;display:grid;gap:.4rem}
.rel-box a{font-weight:600}
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
        "image": f"{BASE_URL}/assets/logo.png",
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

def head(title, desc, path, extra_jsonld=None, og_image="/assets/logo.png",
         asset_prefix="assets/", og_type="website"):
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
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="AR Plastic Surgery">
<meta property="og:title" content="{htmllib.escape(title)}">
<meta property="og:description" content="{htmllib.escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE_URL}{og_image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{htmllib.escape(title)}">
<meta name="twitter:description" content="{htmllib.escape(desc)}">
<meta name="twitter:image" content="{BASE_URL}{og_image}">
<link rel="icon" href="{asset_prefix}logo.png" type="image/png">
<link rel="stylesheet" href="{asset_prefix}style.css">
{ld}
</head>"""

def header(active, root=""):
    def a(href, label, key):
        cls = ' class="active"' if key == active else ""
        return f'<a href="{root}{href.lstrip("/")}"{cls}>{label}</a>'
    return f"""<body>
<header class="site-header" id="siteHeader">
  <div class="wrap header-inner">
    <a class="brand" href="{root}index.html" aria-label="AR Plastic Surgery home">
      <img src="{root}assets/logo.png" alt="Dr. Ashok Reddy — Plastic Surgery" width="52" height="52">
      <span><span class="brand-name">AR Plastic Surgery</span><br><span class="brand-tag">Precision and Perfection</span></span>
    </a>
    <button class="nav-toggle" id="navToggle" aria-label="Open menu" aria-expanded="false">☰</button>
    <nav class="main-nav" id="mainNav" aria-label="Primary">
      {a('/index.html','Home','home')}
      {a('/about.html','About','about')}
      {a('/services.html','Services','services')}
      {a('/procedures/index.html','Procedures','procedures')}
      {a('/blog/index.html','Blog','blog')}
      {a('/contact.html','Contact','contact')}
    </nav>
    <div class="header-cta">
      <a class="phone-link" href="tel:{CLINIC['phone_tel']}">{CLINIC['phone_display']}</a>
      <a class="btn btn-gold" href="{CLINIC['booking']}" target="_blank" rel="noopener">Book Online</a>
    </div>
  </div>
</header>"""

def footer(root=""):
    town_links = "\n".join(
        f'<li><a href="{root}{slug}-plastic-surgeon.html">Plastic Surgeon in {name}</a></li>'
        for name, slug in DISTRICT_PAGES
    )
    return f"""<footer>
  <div class="wrap footer-grid">
    <div class="footer-brand">
      <img src="{root}assets/logo.png" alt="AR Plastic Surgery logo" width="60" height="60">
      <h4>AR Plastic Surgery</h4>
      <p style="font-size:.93rem">Precision and Perfection. Full-scope plastic, cosmetic, hand &amp; microvascular surgery in Karimnagar, Telangana — led by {CLINIC['doctor']}, {CLINIC['credentials']}.</p>
    </div>
    <div>
      <h4>Explore</h4>
      <ul>
        <li><a href="{root}index.html">Home</a></li>
        <li><a href="{root}about.html">About {CLINIC['doctor']}</a></li>
        <li><a href="{root}services.html">All Services</a></li>
        <li><a href="{root}procedures/index.html">Procedures</a></li>
        <li><a href="{root}blog/index.html">Blog</a></li>
        <li><a href="{root}contact.html">Contact &amp; Directions</a></li>
        <li><a href="{CLINIC['booking']}" target="_blank" rel="noopener">Book Online</a></li>
      </ul>
    </div>
    <div>
      <h4>Areas We Serve</h4>
      <ul>
        {town_links}
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

def cta_band(root=""):
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

# ---------------------------------------------------------------- procedures & blog framework
PROC_CATS = [
    ("Cosmetic Surgery", "cosmetic-surgery",
     ["fue-hair-transplant", "gynecomastia-surgery", "liposuction", "rhinoplasty",
      "breast-augmentation", "breast-reduction", "tummy-tuck", "facelift",
      "eyelid-surgery-blepharoplasty", "lipoma-removal"]),
    ("Reconstructive Surgery", "reconstructive-surgery",
     ["breast-reconstruction", "burn-reconstruction", "scar-keloid-treatment",
      "cleft-lip-palate-repair"]),
    ("Hand & Microvascular Surgery", "hand-microvascular-surgery",
     ["hand-trauma-surgery", "tendon-repair", "nerve-repair-microsurgery",
      "carpal-tunnel-release", "microsurgery-free-flap", "fingertip-replantation"]),
    ("Non-Surgical Aesthetics", "non-surgical-aesthetics",
     ["botox-treatment", "dermal-fillers", "prp-therapy", "chemical-peels",
      "laser-treatments"]),
]

# service id (services.html) -> procedure page (relative to site root)
PROC_LINK = {
    "fue-hair-transplant": "procedures/fue-hair-transplant.html",
    "gynecomastia-surgery": "procedures/gynecomastia-surgery.html",
    "liposuction": "procedures/liposuction.html",
    "rhinoplasty": "procedures/rhinoplasty.html",
    "breast-surgery": "procedures/index.html#cosmetic-surgery",
    "tummy-tuck": "procedures/tummy-tuck.html",
    "scar-keloid": "procedures/scar-keloid-treatment.html",
    "burn-reconstruction": "procedures/burn-reconstruction.html",
    "cleft-lip-palate": "procedures/cleft-lip-palate-repair.html",
    "hand-trauma": "procedures/hand-trauma-surgery.html",
    "tendon-nerve-repair": "procedures/tendon-repair.html",
    "microsurgery": "procedures/microsurgery-free-flap.html",
    "artery-repair": "procedures/index.html#hand-microvascular-surgery",
    "lipoma-removal": "procedures/lipoma-removal.html",
    "botox": "procedures/botox-treatment.html",
    "dermal-fillers": "procedures/dermal-fillers.html",
    "prp": "procedures/prp-therapy.html",
    "chemical-peels": "procedures/chemical-peels.html",
    "laser-treatments": "procedures/laser-treatments.html",
}

def procedure_jsonld(proc, url):
    return {
        "@context": "https://schema.org",
        "@type": "MedicalProcedure",
        "name": proc["name"],
        "description": proc["desc"],
        "url": url,
        "procedureType": ("Non-surgical" if proc["category"] == "Non-Surgical Aesthetics"
                          else "Surgical"),
        "performer": {
            "@type": "Physician",
            "name": CLINIC["doctor"],
            "medicalSpecialty": ["PlasticSurgery"],
            "description": f"{CLINIC['doctor']}, {CLINIC['credentials']}; {CLINIC['specialties']}.",
        },
    }

def blogposting_jsonld(post, url):
    return {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": post["h1"],
        "description": post["desc"],
        "url": url,
        "image": f"{BASE_URL}/assets/logo.png",
        "author": {
            "@type": "Person",
            "name": CLINIC["doctor"],
            "jobTitle": CLINIC["specialties"],
            "description": f"{CLINIC['doctor']}, {CLINIC['credentials']}.",
        },
        "publisher": {
            "@type": "Organization",
            "name": CLINIC["name"],
            "logo": {"@type": "ImageObject", "url": f"{BASE_URL}/assets/logo.png"},
        },
        "datePublished": "2026-10-04",
        "mainEntityOfPage": {"@type": "WebPage", "@id": url},
    }

def esc_paras(paras):
    return "\n".join(f"<p>{htmllib.escape(p)}</p>" for p in paras)

def page_procedure(proc):
    slug = proc["slug"]
    path = f"/procedures/{slug}.html"
    url = BASE_URL + path
    faqs = proc["faqs"]
    rel_cards = []
    for r in proc["related"]:
        rp = PROC_BY_SLUG.get(r)
        if not rp:
            continue
        teaser = htmllib.escape(rp["desc"][:120]).rsplit(" ", 1)[0] + "…"
        rel_cards.append(
            f'<article class="card"><h3>{htmllib.escape(rp["name"])}</h3><p>{teaser}</p>'
            f'<a class="more" href="{r}.html">Learn more →</a></article>'
        )
    town_links = " · ".join(
        f'<a href="../{t.lower()}-plastic-surgeon.html">Plastic surgeon for {t} patients</a>'
        for t in proc["towns"]
    )
    journey = "\n".join(
        f"<h3>{htmllib.escape(step)}</h3><p>{htmllib.escape(text)}</p>"
        for step, text in proc["journey"]
    )
    risks = "\n".join(f"<li>{htmllib.escape(r)}</li>" for r in proc["risks"])
    body = f"""
<main><section><div class="wrap">
  <nav class="crumb" aria-label="Breadcrumb"><a href="../index.html">Home</a> › <a href="index.html">Procedures</a> › {htmllib.escape(proc["name"])}</nav>
  <span class="eyebrow">{htmllib.escape(proc["category"])}</span>
  <h1>{htmllib.escape(proc["name"])} in Karimnagar</h1>
  <p class="lede">{htmllib.escape(proc["lede"])}</p>
</div></section>
<section style="padding-top:0"><div class="wrap">
  <h2>Overview</h2>
  {esc_paras(proc["overview"])}
  <h2 style="margin-top:2rem">Our approach</h2>
  {esc_paras(proc["approach"])}
  <h2 style="margin-top:2rem">What to expect</h2>
  {journey}
  <h2 style="margin-top:2rem">Risks and limitations — stated honestly</h2>
  <p>Every procedure carries trade-offs. Before you decide, {CLINIC["doctor"]} will discuss these with you directly:</p>
  <ul class="checklist">
  {risks}
  </ul>
  <h2 style="margin-top:2.2rem">Related procedures</h2>
  <div class="card-grid">{"".join(rel_cards)}</div>
  <div class="rel-box">
    <h3>Visiting from nearby?</h3>
    <p>{town_links}</p>
  </div>
</div></section>
{faq_block(faqs)}
{cta_band(root="../")}
</main>"""
    return (head(proc["title"], proc["desc"], path,
                 [procedure_jsonld(proc, url), faq_jsonld(faqs)],
                 asset_prefix="../assets/")
            + header("procedures", root="../") + body + footer(root="../"))

def page_procedures_index():
    title = "All Procedures | Plastic, Cosmetic & Hand Surgery Karimnagar"
    desc = ("Browse every procedure at AR Plastic Surgery, Karimnagar: cosmetic surgery, reconstruction, "
            "hand & microvascular surgery and non-surgical aesthetics.")
    sections = []
    for cat_name, cat_id, slugs in PROC_CATS:
        cards = []
        for s in slugs:
            p = PROC_BY_SLUG.get(s)
            if not p:
                continue
            teaser = htmllib.escape(p["desc"][:120]).rsplit(" ", 1)[0] + "…"
            cards.append(
                f'<article class="card"><h3>{htmllib.escape(p["name"])}</h3><p>{teaser}</p>'
                f'<a class="more" href="{s}.html">Learn more →</a></article>'
            )
        sections.append(
            f'<div class="svc-cat" id="{cat_id}"><h2 style="font-size:1.4rem">{htmllib.escape(cat_name)}</h2>'
            f'<div class="card-grid">{"".join(cards)}</div></div>'
        )
    body = f"""
<main><section><div class="wrap">
  <nav class="crumb" aria-label="Breadcrumb"><a href="../index.html">Home</a> › Procedures</nav>
  <span class="eyebrow">Procedures A–Z</span>
  <h1>Every procedure, explained plainly</h1>
  <p class="lede">Twenty-five detailed guides across cosmetic surgery, reconstruction, hand &amp; microvascular surgery and non-surgical aesthetics — each written to answer the questions patients actually ask. Results vary from person to person; your consultation is where your plan takes shape.</p>
  <div style="margin-top:2rem">{"".join(sections)}</div>
</div></section>
{cta_band(root="../")}
</main>"""
    return (head(title, desc, "/procedures/index.html", asset_prefix="../assets/")
            + header("procedures", root="../") + body + footer(root="../"))

def page_blog_index():
    title = "Blog | Patient Education | AR Plastic Surgery Karimnagar"
    desc = ("Patient-education articles by Dr Ashok Reddy, Karimnagar: hair transplant questions, gynecomastia "
            "facts, hand surgery guidance, Botox myths and recovery guides.")
    cards = []
    for post in POSTS:
        cards.append(
            f'<article class="post-card"><div class="post-date">{htmllib.escape(post["date"])}</div>'
            f'<h3>{htmllib.escape(post["h1"])}</h3><p>{htmllib.escape(post["desc"])}</p>'
            f'<a class="more" style="font-weight:700;font-size:.92rem" href="{post["slug"]}.html">Read the article →</a></article>'
        )
    body = f"""
<main><section><div class="wrap">
  <nav class="crumb" aria-label="Breadcrumb"><a href="../index.html">Home</a> › Blog</nav>
  <span class="eyebrow">Patient education</span>
  <h1>The AR Plastic Surgery blog</h1>
  <p class="lede">Honest, jargon-free guides by {CLINIC["doctor"]} — written to help you understand your options before you ever step into the clinic.</p>
  <div class="post-list">{"".join(cards)}</div>
</div></section>
{cta_band(root="../")}
</main>"""
    return (head(title, desc, "/blog/index.html", asset_prefix="../assets/")
            + header("blog", root="../") + body + footer(root="../"))

def page_blog_post(post):
    slug = post["slug"]
    path = f"/blog/{slug}.html"
    url = BASE_URL + path
    faqs = post.get("faqs", [])
    sections = "\n".join(
        f"<h2>{htmllib.escape(h)}</h2>\n{esc_paras(paras)}"
        for h, paras in post["sections"]
    )
    rel_items = "\n".join(
        f'<li><a href="../procedures/{r}.html">{htmllib.escape(PROC_BY_SLUG[r]["name"])}</a></li>'
        for r in post["related_procedures"] if r in PROC_BY_SLUG
    )
    body = f"""
<main><section><div class="wrap" style="max-width:46rem">
  <nav class="crumb" aria-label="Breadcrumb"><a href="../index.html">Home</a> › <a href="index.html">Blog</a> › Article</nav>
  <span class="eyebrow">Patient education · {htmllib.escape(post["date"])}</span>
  <h1>{htmllib.escape(post["h1"])}</h1>
  <p class="lede">{htmllib.escape(post["lede"])}</p>
  <p class="byline">By {CLINIC["doctor"]}, {CLINIC["credentials"]} — {CLINIC["specialties"]}</p>
  {sections}
  <div class="rel-box">
    <h3>Related procedures</h3>
    <ul>{rel_items}</ul>
  </div>
</div></section>
{faq_block(faqs) if faqs else ""}
{cta_band(root="../")}
</main>"""
    extra = [blogposting_jsonld(post, url)]
    if faqs:
        extra.append(faq_jsonld(faqs))
    return (head(post["title"], post["desc"], path, extra, asset_prefix="../assets/", og_type="article")
            + header("blog", root="../") + body + footer(root="../"))

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
   "Care for fractures, cuts, crush injuries and dislocations of the hand and wrist. The goal is to restore movement, strength and sensation — and timely assessment offers the greatest chance of a good recovery."),
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
            learn = ""
            if sid in PROC_LINK:
                learn = f'<a class="more" href="{PROC_LINK[sid]}">Learn more →</a>'
            cards.append(
                f'<article class="svc" id="{sid}"><h3>{htmllib.escape(name)}</h3><p>{desc}</p>{learn}</article>'
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
         "services.html#fue-hair-transplant"),
        ("🤲", "Reconstructive & Hand Surgery",
         "Burn reconstruction, cleft repair, scar revision, hand trauma, tendon & nerve repair and microsurgery — restoring form and function.",
         "services.html#scar-keloid"),
        ("✨", "Non-Surgical Aesthetics",
         "Botox, dermal fillers, PRP, chemical peels and laser treatments — subtle, doctor-led rejuvenation without surgery.",
         "services.html#botox"),
    ]
    cards = "\n".join(
        f'<article class="card"><div class="icon" aria-hidden="true">{i}</div><h3>{t}</h3><p>{p}</p>'
        f'<a class="more" href="{l}">Explore services →</a></article>'
        for i, t, p, l in svc_cards
    )
    town_cards = "\n".join(
        f'<a class="town-card" href="{t.lower()}-plastic-surgeon.html"><h3>{t}</h3><p>Plastic surgeon for {t} patients</p></a>'
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
    <img src="assets/dr-ashok-reddy.jpg" alt="{CLINIC['doctor']}, plastic surgeon at AR Plastic Surgery Karimnagar" width="640" height="704" fetchpriority="high">
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
  <img class="doc" src="assets/dr-ashok-reddy.jpg" alt="Portrait of {CLINIC['doctor']}" width="540" height="648" loading="lazy">
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
    <a class="btn btn-solid" href="about.html">More about {CLINIC['doctor']} →</a>
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
  <nav class="crumb" aria-label="Breadcrumb"><a href="index.html">Home</a> › About</nav>
  <span class="eyebrow">About the clinic</span>
  <h1>{CLINIC['doctor']} &amp; AR Plastic Surgery</h1>
  <p class="lede">A surgeon-led practice built on a simple standard: precision and perfection — in planning, in technique, and in aftercare.</p>
</div></section>
<section style="padding-top:0"><div class="wrap split">
  <img class="doc" src="assets/dr-ashok-reddy.jpg" alt="{CLINIC['doctor']}, {CLINIC['specialties']}, AR Plastic Surgery Karimnagar" width="540" height="648">
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
  <p>AR Plastic Surgery is located at {CLINIC['address']}, open <strong>{CLINIC['hours']}</strong>. Patients travel to us from Karimnagar, Warangal, Nizamabad, Khammam and districts across Telangana — see the <a href="contact.html">areas we serve</a>.</p>
  <p style="margin-top:1rem"><a class="btn btn-solid" href="contact.html">Directions &amp; contact →</a>
  <a class="btn btn-outline" href="services.html" style="margin-left:.6rem">View services →</a></p>
</div></section>
<section style="background:var(--bg-soft)"><div class="wrap">
  <span class="eyebrow">The surgeon</span>
  <h2>Meet {CLINIC['doctor']}</h2>
  <div class="card-grid" style="grid-template-columns:repeat(auto-fit,minmax(220px,1fr))">
    <figure class="card" style="padding:.6rem"><img src="assets/dr-ashok-reddy-2.png" alt="{CLINIC['doctor']}, plastic surgeon at AR Plastic Surgery Karimnagar" loading="lazy" style="width:100%;height:auto;border-radius:.6rem"><figcaption style="padding:.6rem .2rem;font-size:.9rem">{CLINIC['doctor']} — {CLINIC['credentials']}</figcaption></figure>
    <figure class="card" style="padding:.6rem"><img src="assets/dr-ashok-reddy-3.jpg" alt="{CLINIC['doctor']}, {CLINIC['specialties']}, AR Plastic Surgery Karimnagar" loading="lazy" style="width:100%;height:auto;border-radius:.6rem"><figcaption style="padding:.6rem .2rem;font-size:.9rem">{CLINIC['doctor']} — {CLINIC['specialties']}</figcaption></figure>
  </div>
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
  <nav class="crumb" aria-label="Breadcrumb"><a href="index.html">Home</a> › Services</nav>
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
def town_page(town, title, desc, h1_intro, sections_html, faqs, slug=None, h1_text=None):
    slug = slug or town.lower().replace(" ", "-")
    h1_text = h1_text or f"Plastic Surgeon for {town} Patients"
    town_links = " · ".join(
        f'<a href="{s}-plastic-surgeon.html">{n}</a>'
        for n, s in DISTRICT_PAGES if s != slug
    )
    body = f"""
<main><section><div class="wrap">
  <nav class="crumb" aria-label="Breadcrumb"><a href="index.html">Home</a> › Plastic surgeon for {town} patients</nav>
  <span class="eyebrow">{town} · Telangana</span>
  <h1>{h1_text}</h1>
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
  <a class="btn btn-outline" href="contact.html" style="margin-left:.6rem">Directions →</a></p>
</div>
<p style="margin-top:1.4rem;font-size:.93rem;color:var(--muted)">Also serving: {town_links}</p>
</div></section>
{faq_block(faqs)}
{cta_band()}
</main>"""
    return (head(title, desc, f"/{slug}-plastic-surgeon.html", faq_jsonld(faqs))
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
<p>For <a href="services.html#fue-hair-transplant">hair transplant</a>, <a href="services.html#gynecomastia-surgery">gynecomastia surgery</a>, <a href="services.html#liposuction">liposuction</a> and <a href="services.html#rhinoplasty">rhinoplasty</a>, the difference at AR is that every case is planned and performed by a qualified plastic surgeon — not delegated. Consultations are confidential. <strong>Free OP consultations are available every Wednesday.</strong></p>
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
<li><strong><a href="services.html#gynecomastia-surgery">Gynecomastia surgery</a></strong> — confidential consultations and a scar-minimal approach, performed by a gold-medalist plastic surgeon.</li>
<li><strong><a href="services.html#liposuction">Liposuction &amp; body contouring</a></strong> — targeted fat removal through small, discreet incisions, planned around your frame.</li>
<li><strong><a href="services.html#lipoma-removal">Lipoma removal</a> &amp; scar revision</strong> — small procedures, done precisely, with attention to the final scar.</li>
<li><strong><a href="services.html#fue-hair-transplant">Hair transplant (FUE)</a></strong> — surgeon-led, planned by Dr Reddy personally.</li>
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
<li><strong><a href="services.html#rhinoplasty">Rhinoplasty</a></strong> — functional and aesthetic nose correction, planned for your face.</li>
<li><strong>Facelift &amp; blepharoplasty</strong> — facial rejuvenation with natural-looking results as the goal.</li>
<li><strong><a href="services.html#burn-reconstruction">Burn reconstruction</a> &amp; skin grafting</strong> — staged rebuilding after burns and complex wounds.</li>
<li><strong><a href="services.html#cleft-lip-palate">Cleft lip &amp; palate repair</a></strong> — staged correction from the earliest months of life.</li>
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
<li><strong><a href="services.html#hand-trauma">Hand &amp; microvascular surgery</a></strong> — tendon, nerve and artery repair under magnification.</li>
<li><strong><a href="services.html#breast-surgery">Breast reduction &amp; augmentation</a></strong> — surgeon-led breast surgery with full aftercare.</li>
<li><strong><a href="services.html#burn-reconstruction">Burn reconstruction</a>, skin grafting, scar revision</strong> — staged, specialist care.</li>
<li><strong>Facelift, <a href="services.html#cleft-lip-palate">cleft repair</a></strong> — genuine expertise a short trip away.</li>
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

# ---------------------------------------------------------------- district pages
def page_warangal():
    return town_page(
        "Warangal",
        "Plastic Surgeon for Warangal | AR Plastic Surgery",
        ("Warangal patients visit AR Plastic Surgery, Karimnagar for full-scope plastic, cosmetic and hand "
         "surgery led by Dr Ashok Reddy — MBBS, DNB, M.Ch, Gold Medalist."),
        ("Warangal has no shortage of hospitals — but a dedicated plastic surgery practice, where one "
         "gold-medalist surgeon plans and performs your procedure from first consultation to aftercare, "
         "is harder to find. That depth of specialist care is why patients from Warangal make the trip to "
         "AR Plastic Surgery in Karimnagar."),
        """<h2>Why the trip from Warangal is worth it</h2>
<p>Led by <strong>Dr Ashok Reddy — MBBS, DNB (Mumbai), M.Ch (Delhi), Gold Medalist</strong>, plastic, cosmetic, hand &amp; microvascular surgeon, the clinic offers something general hospitals rarely match: complete continuity, with the same surgeon at every step.</p>
<ul class="checklist">
<li><strong>Hand &amp; microvascular surgery</strong> — <a href="procedures/tendon-repair.html">tendon repair</a>, <a href="procedures/nerve-repair-microsurgery.html">nerve repair</a>, <a href="procedures/microsurgery-free-flap.html">microsurgical reconstruction</a> and <a href="procedures/hand-trauma-surgery.html">hand trauma care</a> under magnification.</li>
<li><strong>Surgeon-led cosmetic procedures</strong> — <a href="procedures/fue-hair-transplant.html">FUE hair transplant</a>, <a href="procedures/gynecomastia-surgery.html">gynecomastia surgery</a>, <a href="procedures/rhinoplasty.html">rhinoplasty</a> and <a href="procedures/liposuction.html">liposuction</a>, planned and performed by Dr Reddy himself — never delegated.</li>
<li><strong>Reconstructive expertise</strong> — <a href="procedures/burn-reconstruction.html">burn reconstruction</a>, <a href="procedures/scar-keloid-treatment.html">scar revision</a> and <a href="procedures/cleft-lip-palate-repair.html">cleft lip &amp; palate repair</a>.</li>
<li><strong>Non-surgical aesthetics</strong> — <a href="procedures/botox-treatment.html">Botox</a>, fillers, PRP and lasers, doctor-administered.</li>
</ul>
<h2 style="margin-top:1.8rem">Planning your visit from Warangal</h2>
<p>Karimnagar is well connected to Warangal by road, so most consultations fit comfortably into a day trip. <strong>Free OP consultations are held every Wednesday</strong> — an easy way to meet the surgeon, understand your options and get an honest opinion before committing to anything. The clinic is open <strong>every day, 10:00 AM – 8:00 PM</strong>, and holds a 4.9-star Google rating. Call <a href="tel:+919182656866">+91 91826 56866</a> or <a href="contact.html">book online</a> to reserve your slot.</p>""",
        [
         ("Do you treat patients from Warangal?",
          "Yes — patients from Warangal and other Telangana districts visit the Karimnagar clinic regularly."),
         ("Will the same surgeon handle my whole treatment?",
          "Yes. Dr Ashok Reddy plans and performs the procedures himself, and oversees aftercare — the same surgeon from consultation to follow-up."),
         ("How do I book?",
          "Call +91 91826 56866 or use the online booking page. Wednesday OP consultations are free."),
        ])

def page_nizamabad():
    return town_page(
        "Nizamabad",
        "Plastic Surgeon for Nizamabad | AR Plastic Surgery",
        ("Nizamabad patients travel to AR Plastic Surgery, Karimnagar for reconstructive, hand and cosmetic "
         "surgery by Dr Ashok Reddy — MBBS, DNB, M.Ch, Gold Medalist."),
        ("Some medical needs are straightforward to handle locally; others need a plastic surgeon — burns, deep "
         "cuts, hand injuries, non-healing wounds, cleft conditions and deformities. For patients in Nizamabad, "
         "the nearest full-scope practice is AR Plastic Surgery in Karimnagar, led by a gold-medalist surgeon."),
        """<h2>Reconstructive care worth travelling for</h2>
<p><strong>Dr Ashok Reddy — MBBS, DNB (Mumbai), M.Ch (Delhi), Gold Medalist</strong> — is a plastic, cosmetic, hand &amp; microvascular surgeon. The reconstructive side of the practice covers the problems that most affect daily life:</p>
<ul class="checklist">
<li><strong><a href="procedures/burn-reconstruction.html">Burn reconstruction</a></strong> — contracture release and staged rebuilding after burns have healed.</li>
<li><strong><a href="procedures/hand-trauma-surgery.html">Hand trauma surgery</a></strong> — fractures, cuts and crush injuries; timely specialist care protects movement and sensation.</li>
<li><strong><a href="procedures/scar-keloid-treatment.html">Scar &amp; keloid treatment</a></strong> — surgical revision and combined approaches for restrictive or prominent scars.</li>
<li><strong><a href="procedures/cleft-lip-palate-repair.html">Cleft lip &amp; palate repair</a></strong> — staged correction planned from the earliest months of life.</li>
</ul>
<h2 style="margin-top:1.8rem">Cosmetic procedures, honestly planned</h2>
<p>For <a href="procedures/fue-hair-transplant.html">hair transplant (FUE)</a>, <a href="procedures/gynecomastia-surgery.html">gynecomastia surgery</a>, <a href="procedures/liposuction.html">liposuction</a> and <a href="procedures/rhinoplasty.html">rhinoplasty</a>, consultations are private and pressure-free: what the procedure can and cannot do, explained before anything is decided.</p>
<h2 style="margin-top:1.8rem">Making the journey simple</h2>
<p>Nizamabad is well connected to Karimnagar by road. <strong>Free OP consultations every Wednesday</strong> mean your first visit costs nothing but the trip — and the clinic is open <strong>every day, 10:00 AM – 8:00 PM</strong>. Call <a href="tel:+919182656866">+91 91826 56866</a> or <a href="contact.html">book online</a>.</p>""",
        [
         ("Do you treat patients from Nizamabad?",
          "Yes — Nizamabad is within the clinic's service area across Telangana."),
         ("My burn scar restricts movement — can it be improved?",
          "Possibly. Burn contractures can often be released surgically, but it needs an in-person assessment — book a Wednesday free OP to discuss it."),
         ("How do I book?",
          "Call +91 91826 56866 or book online. Wednesday OP consultations are free."),
        ])

def page_khammam():
    return town_page(
        "Khammam",
        "Plastic Surgeon for Khammam | AR Plastic Surgery",
        ("Khammam patients choose AR Plastic Surgery, Karimnagar for cleft repair, burns, scars and cosmetic "
         "surgery with Dr Ashok Reddy — MBBS, DNB, M.Ch, Gold Medalist."),
        ("From Khammam in southern Telangana, specialist plastic surgery has traditionally meant a long journey "
         "to Hyderabad. AR Plastic Surgery in Karimnagar offers a closer full-scope alternative — reconstructive, "
         "cosmetic and hand surgery under one roof, led by a gold-medalist surgeon."),
        """<h2>Cleft, burns and scar care for Khammam families</h2>
<p>Some of the most life-changing plastic surgery is reconstructive. <strong>Dr Ashok Reddy — MBBS, DNB (Mumbai), M.Ch (Delhi), Gold Medalist</strong> — provides:</p>
<ul class="checklist">
<li><strong><a href="procedures/cleft-lip-palate-repair.html">Cleft lip &amp; palate repair</a></strong> — staged surgical correction from the earliest months of life, as part of long-term care.</li>
<li><strong><a href="procedures/burn-reconstruction.html">Burn reconstruction</a></strong> — releasing tight scars and rebuilding form and movement, step by step.</li>
<li><strong><a href="procedures/scar-keloid-treatment.html">Scar revision</a></strong> — making prominent or restrictive scars less noticeable.</li>
<li><strong><a href="procedures/hand-trauma-surgery.html">Hand surgery</a></strong> — tendon, nerve and fracture care by a trained microvascular surgeon.</li>
</ul>
<h2 style="margin-top:1.8rem">Confidential cosmetic consultations</h2>
<p>Concerns like <a href="procedures/gynecomastia-surgery.html">gynecomastia</a>, hair loss (<a href="procedures/fue-hair-transplant.html">FUE transplant</a>), body contour (<a href="procedures/liposuction.html">liposuction</a>, <a href="procedures/tummy-tuck.html">tummy tuck</a>) or nose shape (<a href="procedures/rhinoplasty.html">rhinoplasty</a>) are discussed in fully private consultations — with honest guidance on whether surgery is even the right answer.</p>
<h2 style="margin-top:1.8rem">Visit us from Khammam</h2>
<p>The road journey to Karimnagar is straightforward, and <strong>free OP consultations every Wednesday</strong> make the first trip easy to justify. Open <strong>daily, 10:00 AM – 8:00 PM</strong>; 4.9-star Google rating. Call <a href="tel:+919182656866">+91 91826 56866</a> or <a href="contact.html">book online</a>.</p>""",
        [
         ("Do you treat patients from Khammam?",
          "Yes — patients from Khammam and districts across Telangana visit the Karimnagar clinic."),
         ("At what age should cleft treatment start?",
          "Assessment can begin in the earliest months of life, with staged surgery planned from there. An early consultation helps map the full journey."),
         ("How do I book?",
          "Call +91 91826 56866 or book online. Wednesday OP consultations are free."),
        ])

def page_mancherial():
    return town_page(
        "Mancherial",
        "Plastic Surgeon for Mancherial | AR Plastic Surgery",
        ("Hand injuries and specialist plastic surgery for Mancherial patients at AR Plastic Surgery, Karimnagar "
         "— Dr Ashok Reddy, MBBS, DNB, M.Ch, Gold Medalist."),
        ("In Mancherial's coal belt and industrial landscape, hand injuries are an everyday risk — and a crushed, "
         "cut or fractured hand needs a specialist quickly, not a general dressing. AR Plastic Surgery in "
         "Karimnagar is the nearest practice with a trained hand &amp; microvascular surgeon."),
        """<h2>Hand injuries can't wait — and shouldn't travel far</h2>
<p>Vascular, tendon and nerve injuries are time-sensitive: the sooner a specialist assesses them, the better the chance of restoring movement, strength and sensation. <strong>Dr Ashok Reddy — MBBS, DNB (Mumbai), M.Ch (Delhi), Gold Medalist</strong> — is trained in hand &amp; microvascular surgery:</p>
<ul class="checklist">
<li><strong><a href="procedures/hand-trauma-surgery.html">Hand trauma surgery</a></strong> — fractures, deep cuts, crush injuries and dislocations.</li>
<li><strong><a href="procedures/tendon-repair.html">Tendon repair</a> &amp; <a href="procedures/nerve-repair-microsurgery.html">nerve repair</a></strong> — delicate reconstruction under magnification, with guided rehabilitation.</li>
<li><strong>Artery repair</strong> — restoring blood flow after vascular injury, urgently assessed.</li>
<li><strong><a href="procedures/fingertip-replantation.html">Fingertip replantation</a> &amp; <a href="procedures/carpal-tunnel-release.html">carpal tunnel release</a></strong> — from emergencies to chronic hand conditions.</li>
</ul>
<h2 style="margin-top:1.8rem">Beyond emergency care</h2>
<p>The same precision serves <a href="procedures/scar-keloid-treatment.html">scar revision</a> after healed injuries, <a href="procedures/burn-reconstruction.html">burn reconstruction</a>, and cosmetic procedures — <a href="procedures/fue-hair-transplant.html">hair transplant</a>, <a href="procedures/gynecomastia-surgery.html">gynecomastia surgery</a>, <a href="procedures/liposuction.html">liposuction</a> — all planned and performed by the surgeon himself.</p>
<h2 style="margin-top:1.8rem">Getting here from Mancherial</h2>
<p>Karimnagar is an easy road trip from Mancherial. For non-urgent concerns, <strong>free OP consultations every Wednesday</strong> are the ideal first step. For hand emergencies, call <a href="tel:+919182656866">+91 91826 56866</a> immediately — the clinic is open <strong>every day, 10:00 AM – 8:00 PM</strong>. You can also <a href="contact.html">book online</a>.</p>""",
        [
         ("I injured my hand at work — what should I do?",
          "Keep the hand still, control bleeding with gentle pressure, and call +91 91826 56866 promptly — tendon, nerve and vessel injuries are time-sensitive."),
         ("Do you treat patients from Mancherial?",
          "Yes — Mancherial is within the clinic's regular service area."),
         ("How do I book a non-urgent consultation?",
          "Call +91 91826 56866 or book online. Wednesday OP consultations are free."),
        ])

def page_jagtial():
    return town_page(
        "Jagtial",
        "Plastic Surgeon for Jagtial | AR Plastic Surgery",
        ("Jagtial's nearest plastic surgery practice: AR Plastic Surgery, Karimnagar. Dr Ashok Reddy "
         "— MBBS, DNB, M.Ch, Gold Medalist — cosmetic, hand & reconstructive."),
        ("Jagtial is a short drive from Karimnagar — close enough that there is no reason to settle for a skin "
         "clinic when you need a plastic surgeon, and no need to travel all the way to Hyderabad either. "
         "AR Plastic Surgery is the nearest full-scope practice: cosmetic, reconstructive, hand &amp; "
         "microvascular surgery under one roof."),
        """<h2>Everything a skin clinic can't offer</h2>
<p>Led by <strong>Dr Ashok Reddy — MBBS, DNB (Mumbai), M.Ch (Delhi), Gold Medalist</strong>, plastic, cosmetic, hand &amp; microvascular surgeon, the clinic covers the procedures that need genuine surgical training:</p>
<ul class="checklist">
<li><strong><a href="procedures/hand-trauma-surgery.html">Hand surgery</a> &amp; <a href="procedures/microsurgery-free-flap.html">microsurgery</a></strong> — tendon, nerve and vessel repair under magnification.</li>
<li><strong><a href="procedures/cleft-lip-palate-repair.html">Cleft lip &amp; palate repair</a></strong> — staged correction from infancy.</li>
<li><strong><a href="procedures/burn-reconstruction.html">Burn reconstruction</a> &amp; skin grafting</strong> — restoring movement and appearance.</li>
<li><strong><a href="procedures/scar-keloid-treatment.html">Scar revision</a>, <a href="procedures/lipoma-removal.html">lipoma removal</a>, facial trauma care</strong> — precise, scar-conscious surgery.</li>
</ul>
<h2 style="margin-top:1.8rem">Cosmetic care close to home</h2>
<p><a href="procedures/fue-hair-transplant.html">FUE hair transplant</a>, <a href="procedures/gynecomastia-surgery.html">gynecomastia surgery</a>, <a href="procedures/rhinoplasty.html">rhinoplasty</a>, <a href="procedures/liposuction.html">liposuction</a>, <a href="procedures/tummy-tuck.html">tummy tuck</a>, <a href="procedures/botox-treatment.html">Botox</a> and lasers — every cosmetic case is planned and performed by Dr Reddy personally, starting with a confidential consultation.</p>
<h2 style="margin-top:1.8rem">A neighbourly visit</h2>
<p>Being nearby means follow-ups are easy too — an important part of any surgical plan. <strong>Free OP consultations every Wednesday</strong>, open <strong>daily 10:00 AM – 8:00 PM</strong>, 4.9-star Google rating. Call <a href="tel:+919182656866">+91 91826 56866</a> or <a href="contact.html">book online</a>.</p>""",
        [
         ("Do you treat patients from Jagtial?",
          "Yes — Jagtial is one of the closest towns the clinic serves."),
         ("Is follow-up difficult if I come from Jagtial?",
          "No — the short distance makes follow-up visits straightforward, which is ideal for surgical aftercare."),
         ("How do I book?",
          "Call +91 91826 56866 or book online. Wednesday OP consultations are free."),
        ])

def page_adilabad():
    return town_page(
        "Adilabad",
        "Plastic Surgeon for Adilabad | AR Plastic Surgery",
        ("Adilabad patients travel to AR Plastic Surgery, Karimnagar for specialist plastic, hand and cosmetic "
         "surgery by Dr Ashok Reddy — MBBS, DNB, M.Ch, Gold Medalist."),
        ("From Adilabad in northern Telangana, specialist plastic surgery has usually meant Hyderabad or Nagpur. "
         "AR Plastic Surgery in Karimnagar is a closer full-scope alternative — a real plastic surgery practice "
         "led by a gold-medalist surgeon, without the metro journey."),
        """<h2>Specialist care, closer than you think</h2>
<p><strong>Dr Ashok Reddy — MBBS, DNB (Mumbai), M.Ch (Delhi), Gold Medalist</strong> — practices the full breadth of plastic, cosmetic, hand &amp; microvascular surgery:</p>
<ul class="checklist">
<li><strong><a href="procedures/cleft-lip-palate-repair.html">Cleft lip &amp; palate repair</a></strong> — staged correction from the earliest months of life.</li>
<li><strong><a href="procedures/burn-reconstruction.html">Burn reconstruction</a></strong> — contracture release and staged rebuilding.</li>
<li><strong><a href="procedures/hand-trauma-surgery.html">Hand trauma</a>, <a href="procedures/tendon-repair.html">tendon</a> &amp; <a href="procedures/nerve-repair-microsurgery.html">nerve repair</a></strong> — microsurgical expertise for injuries and deformities.</li>
<li><strong><a href="procedures/scar-keloid-treatment.html">Scar revision</a></strong> — for restrictive or prominent scars.</li>
<li><strong>Cosmetic procedures</strong> — <a href="procedures/fue-hair-transplant.html">hair transplant</a>, <a href="procedures/gynecomastia-surgery.html">gynecomastia</a>, <a href="procedures/rhinoplasty.html">rhinoplasty</a>, <a href="procedures/liposuction.html">liposuction</a> — confidential, surgeon-led.</li>
</ul>
<h2 style="margin-top:1.8rem">Planning the trip from Adilabad</h2>
<p>It is the longest journey on this page — so we make it count. <strong>Free OP consultations every Wednesday</strong> mean your assessment visit costs nothing; surgery and follow-ups are then scheduled around you, with as few trips as safely possible. The clinic is open <strong>every day, 10:00 AM – 8:00 PM</strong> and holds a 4.9-star Google rating. Call <a href="tel:+919182656866">+91 91826 56866</a> or <a href="contact.html">book online</a> to plan your visit.</p>""",
        [
         ("Do you treat patients from Adilabad?",
          "Yes — patients from Adilabad and across northern Telangana visit the Karimnagar clinic."),
         ("How many trips will treatment need?",
          "It depends on the procedure. The Wednesday free OP covers assessment and planning; surgery and follow-ups are scheduled to minimise travel while keeping care safe."),
         ("How do I book?",
          "Call +91 91826 56866 or book online. Wednesday OP consultations are free."),
        ])

def page_bhadradri_kothagudem():
    return town_page(
        "Bhadradri Kothagudem",
        "Plastic Surgeon for Bhadradri Kothagudem | AR Plastic Surgery",
        ("Hand trauma and reconstructive surgery for Bhadradri Kothagudem patients at AR Plastic Surgery, "
         "Karimnagar — Dr Ashok Reddy, MBBS, DNB, M.Ch, Gold Medalist."),
        ("Bhadradri Kothagudem pairs heavy industry — the Singareni coal belt around Kothagudem — with some of "
         "Telangana's most remote mandals. Both realities point to the same need: when a hand is crushed, a burn "
         "scar tightens, or a child needs cleft care, there should be a specialist within reach. AR Plastic "
         "Surgery in Karimnagar is the nearest full-scope practice for the district."),
        """<h2>Industrial injuries need a microvascular surgeon</h2>
<p>Heavy work injures hands — crush injuries, deep lacerations, fractures. <strong>Dr Ashok Reddy — MBBS, DNB (Mumbai), M.Ch (Delhi), Gold Medalist</strong> — is a trained hand &amp; microvascular surgeon, equipped for what these injuries demand:</p>
<ul class="checklist">
<li><strong><a href="procedures/hand-trauma-surgery.html">Hand trauma surgery</a></strong> — urgent assessment of fractures, cuts and crush injuries.</li>
<li><strong><a href="procedures/tendon-repair.html">Tendon</a> &amp; <a href="procedures/nerve-repair-microsurgery.html">nerve repair</a></strong> — reconstruction under magnification, with guided rehabilitation.</li>
<li><strong><a href="procedures/microsurgery-free-flap.html">Microsurgical reconstruction</a></strong> — for complex tissue loss after trauma.</li>
</ul>
<h2 style="margin-top:1.8rem">Reconstructive care for the district's families</h2>
<p>Beyond the workplace: <a href="procedures/burn-reconstruction.html">burn reconstruction</a>, <a href="procedures/cleft-lip-palate-repair.html">cleft lip &amp; palate repair</a> and <a href="procedures/scar-keloid-treatment.html">scar revision</a> — staged, specialist care that changes daily life. Cosmetic consultations (<a href="procedures/fue-hair-transplant.html">hair transplant</a>, <a href="procedures/gynecomastia-surgery.html">gynecomastia</a>, <a href="procedures/rhinoplasty.html">rhinoplasty</a>) are private and pressure-free.</p>
<h2 style="margin-top:1.8rem">Reaching us from the east</h2>
<p>The district is large, so plan around <strong>free OP consultations every Wednesday</strong> — assessment and planning in one visit, surgery scheduled to minimise return trips. For hand emergencies, call <a href="tel:+919182656866">+91 91826 56866</a> at once; the clinic is open <strong>every day, 10:00 AM – 8:00 PM</strong>. You can also <a href="contact.html">book online</a>.</p>""",
        [
         ("Do you treat patients from Bhadradri Kothagudem?",
          "Yes — patients from Kothagudem, Bhadrachalam and across the district visit the Karimnagar clinic."),
         ("A worker injured his hand — how urgent is it?",
          "Very. Tendon, nerve and vessel injuries are time-sensitive — call +91 91826 56866 promptly for guidance."),
         ("How do I book?",
          "Call +91 91826 56866 or book online. Wednesday OP consultations are free."),
        ])

def page_hanamkonda():
    return town_page(
        "Hanamkonda",
        "Plastic Surgeon for Hanamkonda | AR Plastic Surgery",
        ("Hanamkonda patients visit AR Plastic Surgery, Karimnagar for cosmetic, hand and non-surgical "
         "treatments by Dr Ashok Reddy — MBBS, DNB, M.Ch, Gold Medalist."),
        ("Hanamkonda sits at the heart of the Warangal urban region — close enough that a specialist "
         "consultation is a day trip, not an expedition. For working professionals and families here, "
         "AR Plastic Surgery in Karimnagar offers the city's most personal route to cosmetic and hand care: "
         "one surgeon, from first conversation to final follow-up."),
        """<h2>The easy first step: a free Wednesday consultation</h2>
<p>Considering <a href="procedures/fue-hair-transplant.html">hair transplant</a>, <a href="procedures/gynecomastia-surgery.html">gynecomastia surgery</a>, <a href="procedures/rhinoplasty.html">rhinoplasty</a> or <a href="procedures/liposuction.html">liposuction</a>? Start with a <strong>free OP consultation every Wednesday</strong> — meet <strong>Dr Ashok Reddy (MBBS, DNB Mumbai, M.Ch Delhi, Gold Medalist)</strong>, ask everything, and leave with an honest opinion. No pressure, no obligation.</p>
<h2 style="margin-top:1.8rem">Non-surgical options, doctor-administered</h2>
<p>Not everything needs an operating theatre. The clinic offers <a href="procedures/botox-treatment.html">Botox</a>, dermal fillers, <a href="procedures/prp-therapy.html">PRP therapy</a>, <a href="procedures/chemical-peels.html">chemical peels</a> and <a href="procedures/laser-treatments.html">laser treatments</a> — subtle rejuvenation planned by a plastic surgeon, with realistic expectations set upfront.</p>
<h2 style="margin-top:1.8rem">Hand expertise on call</h2>
<p>As a trained hand &amp; microvascular surgeon, Dr Reddy also manages <a href="procedures/hand-trauma-surgery.html">hand injuries</a>, <a href="procedures/tendon-repair.html">tendon problems</a> and <a href="procedures/carpal-tunnel-release.html">carpal tunnel</a> — the repetitive-strain complaints of desk and trade work alike. The clinic is open <strong>every day, 10:00 AM – 8:00 PM</strong>; call <a href="tel:+919182656866">+91 91826 56866</a> or <a href="contact.html">book online</a>.</p>""",
        [
         ("Do you treat patients from Hanamkonda?",
          "Yes — Hanamkonda is part of the Warangal urban region the clinic regularly serves."),
         ("I want a consultation but not surgery yet — is that okay?",
          "Absolutely. Many consultations end with advice, not an operation. Wednesday OP consultations are free."),
         ("How do I book?",
          "Call +91 91826 56866 or book online."),
        ])

def page_hyderabad():
    return town_page(
        "Hyderabad",
        "Plastic Surgeon for Hyderabad | AR Plastic Surgery",
        ("Why Hyderabad patients travel to AR Plastic Surgery, Karimnagar: one gold-medalist surgeon from "
         "consultation to aftercare. Dr Ashok Reddy — MBBS, DNB, M.Ch."),
        ("Hyderabad has no shortage of plastic surgeons — so why do patients from the city travel to Karimnagar? "
         "Because at AR Plastic Surgery, your entire journey is with one person: <strong>Dr Ashok Reddy — MBBS, "
         "DNB (Mumbai), M.Ch (Delhi), Gold Medalist</strong> — who consults, operates and follows up himself. "
         "No hand-offs between departments, no unfamiliar face on the day of surgery."),
        """<h2>Personal care, by design</h2>
<p>Large hospital systems do excellent work — but many patients prefer a practice built around a single surgeon. At AR, the consultation is unhurried, the surgical plan is the surgeon's own, and aftercare is with the same doctor who operated. That continuity is the reason people make the trip.</p>
<h2 style="margin-top:1.8rem">What Hyderabad patients come for</h2>
<ul class="checklist">
<li><strong>Surgeon-led cosmetic procedures</strong> — <a href="procedures/fue-hair-transplant.html">FUE hair transplant</a>, <a href="procedures/gynecomastia-surgery.html">gynecomastia surgery</a>, <a href="procedures/rhinoplasty.html">rhinoplasty</a>, <a href="procedures/liposuction.html">liposuction</a>, <a href="procedures/tummy-tuck.html">tummy tuck</a> — planned and performed by Dr Reddy personally.</li>
<li><strong><a href="procedures/hand-trauma-surgery.html">Hand &amp; microvascular surgery</a></strong> — tendon, nerve and microsurgical reconstruction, a genuine subspecialty.</li>
<li><strong>Reconstructive work</strong> — <a href="procedures/burn-reconstruction.html">burn reconstruction</a>, <a href="procedures/scar-keloid-treatment.html">scar revision</a>, <a href="procedures/cleft-lip-palate-repair.html">cleft repair</a>.</li>
<li><strong>Doctor-led aesthetics</strong> — <a href="procedures/botox-treatment.html">Botox</a>, fillers, PRP, peels and lasers.</li>
</ul>
<h2 style="margin-top:1.8rem">Planned around a single trip</h2>
<p><strong>Free OP consultations every Wednesday</strong> let you meet the surgeon before deciding anything. Surgery and follow-ups are then scheduled to minimise travel — many patients combine consultation and planning in one visit. The clinic holds a 4.9-star Google rating and is open <strong>every day, 10:00 AM – 8:00 PM</strong>. Call <a href="tel:+919182656866">+91 91826 56866</a> or <a href="contact.html">book online</a>.</p>""",
        [
         ("Why would I travel from Hyderabad to Karimnagar?",
          "For continuity: one gold-medalist surgeon consults, operates and follows up with you personally — a different experience from a large hospital system."),
         ("Do you treat Hyderabad patients?",
          "Yes — patients from Hyderabad, Secunderabad and surrounding areas visit the clinic regularly."),
         ("How do I book?",
          "Call +91 91826 56866 or book online. Wednesday OP consultations are free."),
        ])

def page_jangaon():
    return town_page(
        "Jangaon",
        "Plastic Surgeon for Jangaon | AR Plastic Surgery",
        ("Jangaon patients visit AR Plastic Surgery, Karimnagar for full-scope plastic, cosmetic and hand "
         "surgery by Dr Ashok Reddy — MBBS, DNB, M.Ch, Gold Medalist."),
        ("Jangaon sits between Hyderabad and Warangal — well placed, but with no full-scope plastic surgery "
         "practice of its own. For everything from hand injuries to hair transplant, the nearest dedicated "
         "option is AR Plastic Surgery in Karimnagar, led by a gold-medalist surgeon."),
        """<h2>Full-scope care, without the metro trip</h2>
<p><strong>Dr Ashok Reddy — MBBS, DNB (Mumbai), M.Ch (Delhi), Gold Medalist</strong> — practices plastic, cosmetic, hand &amp; microvascular surgery. For Jangaon, that means:</p>
<ul class="checklist">
<li><strong><a href="procedures/hand-trauma-surgery.html">Hand surgery</a></strong> — injuries, tendon and nerve problems treated by a trained microvascular surgeon.</li>
<li><strong>Cosmetic procedures</strong> — <a href="procedures/fue-hair-transplant.html">hair transplant (FUE)</a>, <a href="procedures/gynecomastia-surgery.html">gynecomastia</a>, <a href="procedures/liposuction.html">liposuction</a>, <a href="procedures/rhinoplasty.html">rhinoplasty</a> — confidential, surgeon-led.</li>
<li><strong>Reconstructive</strong> — <a href="procedures/burn-reconstruction.html">burns</a>, <a href="procedures/scar-keloid-treatment.html">scars</a>, <a href="procedures/cleft-lip-palate-repair.html">cleft repair</a>, skin grafting.</li>
<li><strong>Non-surgical</strong> — <a href="procedures/botox-treatment.html">Botox</a>, fillers, PRP, peels, lasers.</li>
</ul>
<h2 style="margin-top:1.8rem">A straightforward visit</h2>
<p>Jangaon's central location makes Karimnagar an easy trip. <strong>Free OP consultations every Wednesday</strong>, open <strong>daily 10:00 AM – 8:00 PM</strong>, 4.9-star Google rating. Call <a href="tel:+919182656866">+91 91826 56866</a> or <a href="contact.html">book online</a>.</p>""",
        [
         ("Do you treat patients from Jangaon?",
          "Yes — Jangaon is within the clinic's service area across Telangana."),
         ("Is a consultation worth the trip if I'm unsure about surgery?",
          "Yes — many consultations end with advice rather than an operation, and Wednesday OP consultations are free."),
         ("How do I book?",
          "Call +91 91826 56866 or book online."),
        ])

def page_jayashankar_bhupalpally():
    return town_page(
        "Jayashankar Bhupalpally",
        "Plastic Surgeon for Jayashankar Bhupalpally | AR Plastic Surgery",
        ("Reconstructive and hand surgery for Jayashankar Bhupalpally patients at AR Plastic Surgery, Karimnagar "
         "— Dr Ashok Reddy, MBBS, DNB, M.Ch, Gold Medalist."),
        ("Jayashankar Bhupalpally's forests and distance from the big cities shouldn't decide who gets specialist "
         "care. For cleft conditions, burn scars, hand injuries and deformities, AR Plastic Surgery in Karimnagar "
         "is the nearest full-scope plastic surgery practice — led by a gold-medalist surgeon."),
        """<h2>Specialist care shouldn't depend on your pin code</h2>
<p><strong>Dr Ashok Reddy — MBBS, DNB (Mumbai), M.Ch (Delhi), Gold Medalist</strong> — is a plastic, cosmetic, hand &amp; microvascular surgeon. The procedures that matter most in remote districts:</p>
<ul class="checklist">
<li><strong><a href="procedures/cleft-lip-palate-repair.html">Cleft lip &amp; palate repair</a></strong> — staged correction from the earliest months of life.</li>
<li><strong><a href="procedures/burn-reconstruction.html">Burn reconstruction</a></strong> — releasing contractures, restoring movement.</li>
<li><strong><a href="procedures/hand-trauma-surgery.html">Hand trauma</a> &amp; <a href="procedures/tendon-repair.html">tendon repair</a></strong> — injuries treated before they become permanent disability.</li>
<li><strong><a href="procedures/scar-keloid-treatment.html">Scar revision</a></strong> — for restrictive or prominent scars.</li>
</ul>
<h2 style="margin-top:1.8rem">Cosmetic care too</h2>
<p><a href="procedures/fue-hair-transplant.html">Hair transplant (FUE)</a>, <a href="procedures/gynecomastia-surgery.html">gynecomastia surgery</a> and <a href="procedures/rhinoplasty.html">rhinoplasty</a> are available with the same confidential, pressure-free consultations.</p>
<h2 style="margin-top:1.8rem">Planning a long journey</h2>
<p>Because the trip is long, we plan efficiently: <strong>free OP consultations every Wednesday</strong> for assessment, then surgery scheduled to minimise return visits. Open <strong>every day, 10:00 AM – 8:00 PM</strong>. Call <a href="tel:+919182656866">+91 91826 56866</a> or <a href="contact.html">book online</a>.</p>""",
        [
         ("Do you treat patients from Jayashankar Bhupalpally?",
          "Yes — patients from across this remote district visit the Karimnagar clinic."),
         ("My child has a cleft lip — when should we come?",
          "As early as possible — assessment can begin in the first months of life, with staged surgery planned from there."),
         ("How do I book?",
          "Call +91 91826 56866 or book online. Wednesday OP consultations are free."),
        ])

def page_jogulamba_gadwal():
    return town_page(
        "Jogulamba Gadwal",
        "Plastic Surgeon for Jogulamba Gadwal | AR Plastic Surgery",
        ("Reconstructive, hand and cosmetic surgery for Jogulamba Gadwal patients at AR Plastic Surgery, "
         "Karimnagar — Dr Ashok Reddy, MBBS, DNB, M.Ch, Gold Medalist."),
        ("Jogulamba Gadwal, on Telangana's southern border, is far from every metro — which is exactly why a "
         "reachable full-scope practice matters. For burns, cleft care, hand injuries and honest cosmetic "
         "consultations, AR Plastic Surgery in Karimnagar is the specialist option for the district."),
        """<h2>What the district needs most</h2>
<p><strong>Dr Ashok Reddy — MBBS, DNB (Mumbai), M.Ch (Delhi), Gold Medalist</strong> — plastic, cosmetic, hand &amp; microvascular surgeon:</p>
<ul class="checklist">
<li><strong><a href="procedures/burn-reconstruction.html">Burn reconstruction</a></strong> — contracture release and staged rebuilding after burns heal.</li>
<li><strong><a href="procedures/cleft-lip-palate-repair.html">Cleft lip &amp; palate repair</a></strong> — staged correction from infancy.</li>
<li><strong><a href="procedures/hand-trauma-surgery.html">Hand trauma surgery</a></strong> — fractures, cuts and crush injuries assessed by a microvascular specialist.</li>
<li><strong><a href="procedures/scar-keloid-treatment.html">Scar revision</a></strong> — for scars that restrict movement or draw stares.</li>
</ul>
<h2 style="margin-top:1.8rem">And for personal concerns</h2>
<p>Hair loss, gynecomastia, body contour or nose shape — <a href="procedures/fue-hair-transplant.html">FUE hair transplant</a>, <a href="procedures/gynecomastia-surgery.html">gynecomastia surgery</a>, <a href="procedures/liposuction.html">liposuction</a> and <a href="procedures/rhinoplasty.html">rhinoplasty</a> begin with a private consultation where you'll hear what surgery can and cannot do.</p>
<h2 style="margin-top:1.8rem">Worth the journey south to north</h2>
<p>It's a long trip, so make the first one count: <strong>free OP consultations every Wednesday</strong>. Open <strong>daily, 10:00 AM – 8:00 PM</strong>; 4.9-star Google rating. Call <a href="tel:+919182656866">+91 91826 56866</a> or <a href="contact.html">book online</a>.</p>""",
        [
         ("Do you treat patients from Jogulamba Gadwal?",
          "Yes — patients from Gadwal and surrounding areas visit the Karimnagar clinic."),
         ("Is it worth travelling so far for a consultation?",
          "Wednesday OP consultations are free, so your first visit is purely information — many patients find one trip enough to decide."),
         ("How do I book?",
          "Call +91 91826 56866 or book online."),
        ])

def page_kamareddy():
    return town_page(
        "Kamareddy",
        "Plastic Surgeon for Kamareddy | AR Plastic Surgery",
        ("Hand trauma, reconstructive and cosmetic surgery for Kamareddy patients at AR Plastic Surgery, "
         "Karimnagar — Dr Ashok Reddy, MBBS, DNB, M.Ch, Gold Medalist."),
        ("Kamareddy's agricultural landscape means hands take the brunt of daily work — cuts, crush injuries, "
         "fractures. When a hand injury needs more than a dressing, the nearest trained hand &amp; microvascular "
         "surgeon is <strong>Dr Ashok Reddy</strong> at AR Plastic Surgery in Karimnagar."),
        """<h2>Hands are a surgeon's most delicate work</h2>
<p><strong>Dr Ashok Reddy — MBBS, DNB (Mumbai), M.Ch (Delhi), Gold Medalist</strong> — specialises in hand &amp; microvascular surgery:</p>
<ul class="checklist">
<li><strong><a href="procedures/hand-trauma-surgery.html">Hand trauma surgery</a></strong> — urgent care for fractures, deep cuts and crush injuries.</li>
<li><strong><a href="procedures/tendon-repair.html">Tendon repair</a></strong> — restoring finger movement after division or injury.</li>
<li><strong><a href="procedures/nerve-repair-microsurgery.html">Nerve repair</a></strong> — microsurgical reconnection for numbness and lost function.</li>
<li><strong><a href="procedures/carpal-tunnel-release.html">Carpal tunnel release</a></strong> — for chronic numbness and night pain in the hand.</li>
</ul>
<h2 style="margin-top:1.8rem">The full practice, for everything else</h2>
<p><a href="procedures/burn-reconstruction.html">Burn reconstruction</a>, <a href="procedures/cleft-lip-palate-repair.html">cleft repair</a>, <a href="procedures/scar-keloid-treatment.html">scar revision</a> — plus cosmetic procedures (<a href="procedures/fue-hair-transplant.html">hair transplant</a>, <a href="procedures/gynecomastia-surgery.html">gynecomastia</a>, <a href="procedures/rhinoplasty.html">rhinoplasty</a>) with confidential consultations.</p>
<h2 style="margin-top:1.8rem">Visit us from Kamareddy</h2>
<p>Well connected by road to Karimnagar. <strong>Free OP consultations every Wednesday</strong>; open <strong>every day, 10:00 AM – 8:00 PM</strong>. For hand emergencies call <a href="tel:+919182656866">+91 91826 56866</a> immediately — or <a href="contact.html">book online</a> for planned visits.</p>""",
        [
         ("Do you treat patients from Kamareddy?",
          "Yes — Kamareddy is within the clinic's service area across northern Telangana."),
         ("My finger was cut deeply — can it be saved?",
          "It depends on the injury and timing — call +91 91826 56866 promptly; tendon and nerve injuries are time-sensitive."),
         ("How do I book?",
          "Call +91 91826 56866 or book online. Wednesday OP consultations are free."),
        ])

def page_komaram_bheem_asifabad():
    return town_page(
        "Komaram Bheem Asifabad",
        "Plastic Surgeon for Komaram Bheem Asifabad | AR Plastic Surgery",
        ("Reconstructive and hand surgery access for Komaram Bheem Asifabad patients at AR Plastic Surgery, "
         "Karimnagar — Dr Ashok Reddy, MBBS, DNB, M.Ch, Gold Medalist."),
        ("Komaram Bheem Asifabad's forests and tribal mandals are among Telangana's most remote — and distance "
         "should never decide whether a child with a cleft lip or a worker with a hand injury sees a specialist. "
         "AR Plastic Surgery in Karimnagar is the nearest full-scope plastic surgery practice for the district."),
        """<h2>Care that reaches the far districts</h2>
<p><strong>Dr Ashok Reddy — MBBS, DNB (Mumbai), M.Ch (Delhi), Gold Medalist</strong> — plastic, cosmetic, hand &amp; microvascular surgeon. For this district, the most needed procedures:</p>
<ul class="checklist">
<li><strong><a href="procedures/cleft-lip-palate-repair.html">Cleft lip &amp; palate repair</a></strong> — staged correction from the earliest months of life.</li>
<li><strong><a href="procedures/burn-reconstruction.html">Burn reconstruction</a></strong> — releasing contractures, restoring movement and appearance.</li>
<li><strong><a href="procedures/hand-trauma-surgery.html">Hand trauma surgery</a></strong> — fractures, cuts and crush injuries with specialist assessment.</li>
<li><strong><a href="procedures/scar-keloid-treatment.html">Scar revision</a></strong> — for restrictive or prominent scars.</li>
</ul>
<h2 style="margin-top:1.8rem">One planned trip</h2>
<p>Long journeys demand efficient planning: <strong>free OP consultations every Wednesday</strong> cover assessment and a clear plan, with surgery scheduled to minimise return trips. Open <strong>every day, 10:00 AM – 8:00 PM</strong>. Call <a href="tel:+919182656866">+91 91826 56866</a> or <a href="contact.html">book online</a>.</p>""",
        [
         ("Do you treat patients from Komaram Bheem Asifabad?",
          "Yes — patients from Asifabad and surrounding mandals visit the Karimnagar clinic."),
         ("How do we plan treatment with such a long journey?",
          "Start with a free Wednesday OP consultation — assessment and planning in one visit, then surgery scheduled around minimal travel."),
         ("How do I book?",
          "Call +91 91826 56866 or book online."),
        ])

def page_mahabubabad():
    return town_page(
        "Mahabubabad",
        "Plastic Surgeon for Mahabubabad | AR Plastic Surgery",
        ("Full-scope plastic, hand and cosmetic surgery for Mahabubabad patients at AR Plastic Surgery, Karimnagar "
         "— Dr Ashok Reddy, MBBS, DNB, M.Ch, Gold Medalist."),
        ("Mahabubabad is rural central Telangana — the kind of district where specialist surgery has always meant "
         "a metro trip. AR Plastic Surgery in Karimnagar changes that equation: a full-scope plastic, cosmetic, "
         "hand &amp; microvascular practice led by a gold-medalist surgeon, within a manageable journey."),
        """<h2>One practice, the complete specialty</h2>
<p><strong>Dr Ashok Reddy — MBBS, DNB (Mumbai), M.Ch (Delhi), Gold Medalist</strong> — covers the breadth of plastic surgery:</p>
<ul class="checklist">
<li><strong>Reconstructive</strong> — <a href="procedures/burn-reconstruction.html">burn reconstruction</a>, <a href="procedures/cleft-lip-palate-repair.html">cleft repair</a>, <a href="procedures/scar-keloid-treatment.html">scar revision</a>, skin grafting.</li>
<li><strong><a href="procedures/hand-trauma-surgery.html">Hand &amp; microvascular</a></strong> — <a href="procedures/tendon-repair.html">tendon</a> and <a href="procedures/nerve-repair-microsurgery.html">nerve repair</a>, fractures, microsurgical reconstruction.</li>
<li><strong>Cosmetic</strong> — <a href="procedures/fue-hair-transplant.html">FUE hair transplant</a>, <a href="procedures/gynecomastia-surgery.html">gynecomastia surgery</a>, <a href="procedures/liposuction.html">liposuction</a>, <a href="procedures/rhinoplasty.html">rhinoplasty</a> — confidential and surgeon-led.</li>
<li><strong>Non-surgical</strong> — <a href="procedures/botox-treatment.html">Botox</a>, fillers, PRP, peels, lasers.</li>
</ul>
<h2 style="margin-top:1.8rem">Start with a free Wednesday consultation</h2>
<p>Every treatment begins with an honest conversation about what surgery can and cannot do. <strong>Free OP consultations every Wednesday</strong>; open <strong>daily, 10:00 AM – 8:00 PM</strong>; 4.9-star Google rating. Call <a href="tel:+919182656866">+91 91826 56866</a> or <a href="contact.html">book online</a>.</p>""",
        [
         ("Do you treat patients from Mahabubabad?",
          "Yes — Mahabubabad is within the clinic's service area across Telangana."),
         ("What does a first consultation involve?",
          "An unhurried discussion of your concern, examination, and honest advice on options — free on Wednesdays."),
         ("How do I book?",
          "Call +91 91826 56866 or book online."),
        ])

def page_mahabubnagar():
    return town_page(
        "Mahabubnagar",
        "Plastic Surgeon for Mahabubnagar | AR Plastic Surgery",
        ("Mahabubnagar patients visit AR Plastic Surgery, Karimnagar for specialist plastic, hand and "
         "cosmetic surgery — Dr Ashok Reddy, MBBS, DNB, M.Ch, Gold Medalist."),
        ("Mahabubnagar — Palamuru — is one of Telangana's largest districts, yet dedicated plastic surgery "
         "remains hard to access locally. Whether it's a hand injury, a child's cleft condition, or a personal "
         "cosmetic concern, AR Plastic Surgery in Karimnagar offers the district a genuine specialist option."),
        """<h2>A district-scale answer to specialist surgery</h2>
<p>Led by <strong>Dr Ashok Reddy — MBBS, DNB (Mumbai), M.Ch (Delhi), Gold Medalist</strong>, plastic, cosmetic, hand &amp; microvascular surgeon, the clinic serves:</p>
<ul class="checklist">
<li><strong><a href="procedures/hand-trauma-surgery.html">Hand surgery</a></strong> — trauma, tendon and nerve repair by a trained microvascular surgeon.</li>
<li><strong><a href="procedures/burn-reconstruction.html">Burn reconstruction</a> &amp; <a href="procedures/cleft-lip-palate-repair.html">cleft repair</a></strong> — staged, life-changing reconstructive care.</li>
<li><strong><a href="procedures/scar-keloid-treatment.html">Scar revision</a></strong> — for scars that restrict or distress.</li>
<li><strong>Confidential cosmetic care</strong> — <a href="procedures/fue-hair-transplant.html">hair transplant</a>, <a href="procedures/gynecomastia-surgery.html">gynecomastia</a>, <a href="procedures/rhinoplasty.html">rhinoplasty</a>, <a href="procedures/liposuction.html">liposuction</a>, <a href="procedures/botox-treatment.html">Botox</a>.</li>
</ul>
<h2 style="margin-top:1.8rem">Make the trip worthwhile</h2>
<p><strong>Free OP consultations every Wednesday</strong> — meet the surgeon, get an honest opinion, plan everything in one visit. Open <strong>every day, 10:00 AM – 8:00 PM</strong>; 4.9-star Google rating. Call <a href="tel:+919182656866">+91 91826 56866</a> or <a href="contact.html">book online</a>.</p>""",
        [
         ("Do you treat patients from Mahabubnagar?",
          "Yes — patients from Mahabubnagar and the Palamuru region visit the clinic."),
         ("Is cosmetic surgery confidential?",
          "Completely. Consultations are private, and your information stays between you and the clinic."),
         ("How do I book?",
          "Call +91 91826 56866 or book online. Wednesday OP consultations are free."),
        ])

def page_medak():
    return town_page(
        "Medak",
        "Plastic Surgeon for Medak | AR Plastic Surgery",
        ("Medak patients visit AR Plastic Surgery, Karimnagar for full-scope plastic, hand and cosmetic surgery "
         "by Dr Ashok Reddy — MBBS, DNB, M.Ch, Gold Medalist."),
        ("Medak's historic towns sit close enough to Hyderabad to feel its pull — but a full-scope plastic "
         "surgery practice doesn't require the metro. AR Plastic Surgery in Karimnagar offers Medak a closer "
         "specialist option, led by a gold-medalist surgeon."),
        """<h2>Closer than Hyderabad, fuller than a clinic</h2>
<p><strong>Dr Ashok Reddy — MBBS, DNB (Mumbai), M.Ch (Delhi), Gold Medalist</strong> — plastic, cosmetic, hand &amp; microvascular surgeon. What Medak patients come for:</p>
<ul class="checklist">
<li><strong><a href="procedures/hand-trauma-surgery.html">Hand surgery</a></strong> — injuries, <a href="procedures/tendon-repair.html">tendon</a> and <a href="procedures/nerve-repair-microsurgery.html">nerve repair</a> under magnification.</li>
<li><strong>Cosmetic procedures</strong> — <a href="procedures/fue-hair-transplant.html">FUE hair transplant</a>, <a href="procedures/gynecomastia-surgery.html">gynecomastia</a>, <a href="procedures/rhinoplasty.html">rhinoplasty</a>, <a href="procedures/liposuction.html">liposuction</a> — planned and performed by the surgeon himself.</li>
<li><strong>Reconstructive</strong> — <a href="procedures/burn-reconstruction.html">burns</a>, <a href="procedures/cleft-lip-palate-repair.html">cleft repair</a>, <a href="procedures/scar-keloid-treatment.html">scar revision</a>.</li>
<li><strong>Aesthetics</strong> — <a href="procedures/botox-treatment.html">Botox</a>, fillers, PRP, peels, lasers.</li>
</ul>
<h2 style="margin-top:1.8rem">An easy decision to explore</h2>
<p><strong>Free OP consultations every Wednesday</strong> — come, meet the surgeon, hear an honest opinion. Open <strong>daily, 10:00 AM – 8:00 PM</strong>; 4.9-star Google rating. Call <a href="tel:+919182656866">+91 91826 56866</a> or <a href="contact.html">book online</a>.</p>""",
        [
         ("Do you treat patients from Medak?",
          "Yes — Medak is within the clinic's service area."),
         ("Do I need a referral?",
          "No — call or book directly; walk-ins are welcome during clinic hours."),
         ("How do I book?",
          "Call +91 91826 56866 or book online. Wednesday OP consultations are free."),
        ])

def page_medchal_malkajgiri():
    return town_page(
        "Medchal-Malkajgiri",
        "Plastic Surgeon for Medchal-Malkajgiri | AR Plastic Surgery",
        ("Medchal-Malkajgiri patients travel to AR Plastic Surgery, Karimnagar for personal, surgeon-led plastic "
         "surgery — Dr Ashok Reddy, MBBS, DNB, M.Ch, Gold Medalist."),
        ("Living in Hyderabad's urban sprawl means world-class hospitals on every corner — and also long queues, "
         "rotating doctors, and ten-minute consultations. Many patients from Medchal-Malkajgiri travel to AR "
         "Plastic Surgery in Karimnagar for the opposite experience: one gold-medalist surgeon, unhurried, from "
         "first conversation to final follow-up."),
        """<h2>An antidote to the hospital machine</h2>
<p>At AR, <strong>Dr Ashok Reddy — MBBS, DNB (Mumbai), M.Ch (Delhi), Gold Medalist</strong> — consults, operates and follows up himself. No hand-offs, no unfamiliar face on surgery day. For patients tired of being a file number, that continuity is worth the trip.</p>
<h2 style="margin-top:1.8rem">What the trip covers</h2>
<ul class="checklist">
<li><strong>Cosmetic</strong> — <a href="procedures/fue-hair-transplant.html">FUE hair transplant</a>, <a href="procedures/gynecomastia-surgery.html">gynecomastia</a>, <a href="procedures/rhinoplasty.html">rhinoplasty</a>, <a href="procedures/liposuction.html">liposuction</a>, <a href="procedures/tummy-tuck.html">tummy tuck</a>.</li>
<li><strong><a href="procedures/hand-trauma-surgery.html">Hand &amp; microvascular</a></strong> — a true subspecialty: tendon, nerve, microsurgical reconstruction.</li>
<li><strong>Reconstructive</strong> — <a href="procedures/burn-reconstruction.html">burns</a>, <a href="procedures/scar-keloid-treatment.html">scars</a>, <a href="procedures/cleft-lip-palate-repair.html">cleft repair</a>.</li>
<li><strong>Aesthetics</strong> — <a href="procedures/botox-treatment.html">Botox</a>, fillers, PRP, peels, lasers.</li>
</ul>
<h2 style="margin-top:1.8rem">Planned around your schedule</h2>
<p><strong>Free OP consultations every Wednesday</strong>; surgery scheduled to minimise travel. Open <strong>every day, 10:00 AM – 8:00 PM</strong>; 4.9-star Google rating. Call <a href="tel:+919182656866">+91 91826 56866</a> or <a href="contact.html">book online</a>.</p>""",
        [
         ("Why travel from Medchal to Karimnagar?",
          "For personal continuity — one surgeon handles your consultation, operation and aftercare, unlike a rotating hospital team."),
         ("Do you treat patients from Medchal-Malkajgiri?",
          "Yes — patients from across the Hyderabad urban region visit regularly."),
         ("How do I book?",
          "Call +91 91826 56866 or book online. Wednesday OP consultations are free."),
        ])

def page_mulugu():
    return town_page(
        "Mulugu",
        "Plastic Surgeon for Mulugu | AR Plastic Surgery",
        ("Reconstructive and hand surgery access for Mulugu patients at AR Plastic Surgery, Karimnagar — "
         "Dr Ashok Reddy, MBBS, DNB, M.Ch, Gold Medalist."),
        ("Mulugu's forests and tribal heartland are among Telangana's most beautiful — and most distant from "
         "specialist care. For cleft conditions, burn scars and hand injuries, AR Plastic Surgery in Karimnagar "
         "is the nearest full-scope plastic surgery practice for the district."),
        """<h2>Bringing the specialty to the forest district</h2>
<p><strong>Dr Ashok Reddy — MBBS, DNB (Mumbai), M.Ch (Delhi), Gold Medalist</strong> — plastic, cosmetic, hand &amp; microvascular surgeon:</p>
<ul class="checklist">
<li><strong><a href="procedures/cleft-lip-palate-repair.html">Cleft lip &amp; palate repair</a></strong> — staged correction from the earliest months of life.</li>
<li><strong><a href="procedures/burn-reconstruction.html">Burn reconstruction</a></strong> — releasing contractures, restoring movement.</li>
<li><strong><a href="procedures/hand-trauma-surgery.html">Hand trauma surgery</a></strong> — specialist assessment before injuries become permanent disability.</li>
<li><strong><a href="procedures/scar-keloid-treatment.html">Scar revision</a></strong> — for restrictive or prominent scars.</li>
</ul>
<h2 style="margin-top:1.8rem">One efficient trip</h2>
<p><strong>Free OP consultations every Wednesday</strong> — assessment and a clear plan in a single visit, surgery scheduled to minimise return travel. Open <strong>every day, 10:00 AM – 8:00 PM</strong>. Call <a href="tel:+919182656866">+91 91826 56866</a> or <a href="contact.html">book online</a>.</p>""",
        [
         ("Do you treat patients from Mulugu?",
          "Yes — patients from Mulugu and surrounding mandals visit the Karimnagar clinic."),
         ("The journey is long — how do we plan it?",
          "Begin with a free Wednesday OP consultation: assessment and planning in one visit, then surgery scheduled around minimal travel."),
         ("How do I book?",
          "Call +91 91826 56866 or book online."),
        ])

def page_nagarkurnool():
    return town_page(
        "Nagarkurnool",
        "Plastic Surgeon for Nagarkurnool | AR Plastic Surgery",
        ("Reconstructive, hand and cosmetic surgery for Nagarkurnool patients at AR Plastic Surgery, Karimnagar "
         "— Dr Ashok Reddy, MBBS, DNB, M.Ch, Gold Medalist."),
        ("Nagarkurnool's rural mandals and Nallamala fringe are far from specialist surgery — which matters when "
         "the need is a child's cleft lip, a burn contracture, or a hand injury. AR Plastic Surgery in "
         "Karimnagar is the reachable full-scope option for the district."),
        """<h2>The procedures rural districts need most</h2>
<p><strong>Dr Ashok Reddy — MBBS, DNB (Mumbai), M.Ch (Delhi), Gold Medalist</strong> — plastic, cosmetic, hand &amp; microvascular surgeon:</p>
<ul class="checklist">
<li><strong><a href="procedures/cleft-lip-palate-repair.html">Cleft lip &amp; palate repair</a></strong> — staged correction from infancy.</li>
<li><strong><a href="procedures/burn-reconstruction.html">Burn reconstruction</a></strong> — restoring movement and appearance, step by step.</li>
<li><strong><a href="procedures/hand-trauma-surgery.html">Hand trauma</a> &amp; <a href="procedures/tendon-repair.html">tendon repair</a></strong> — timely specialist care for injuries.</li>
<li><strong><a href="procedures/scar-keloid-treatment.html">Scar revision</a></strong> — for scars that restrict or distress.</li>
</ul>
<h2 style="margin-top:1.8rem">Cosmetic concerns welcome too</h2>
<p><a href="procedures/fue-hair-transplant.html">Hair transplant</a>, <a href="procedures/gynecomastia-surgery.html">gynecomastia</a>, <a href="procedures/rhinoplasty.html">rhinoplasty</a> — private consultations, honest opinions, surgeon-performed procedures.</p>
<h2 style="margin-top:1.8rem">Planning your visit</h2>
<p><strong>Free OP consultations every Wednesday</strong>; open <strong>daily, 10:00 AM – 8:00 PM</strong>; 4.9-star Google rating. Call <a href="tel:+919182656866">+91 91826 56866</a> or <a href="contact.html">book online</a>.</p>""",
        [
         ("Do you treat patients from Nagarkurnool?",
          "Yes — Nagarkurnool is within the clinic's service area across Telangana."),
         ("My child's burn scar is tightening — can it be released?",
          "Often, yes — but it needs an in-person assessment. A free Wednesday OP is the right first step."),
         ("How do I book?",
          "Call +91 91826 56866 or book online."),
        ])

def page_nalgonda():
    return town_page(
        "Nalgonda",
        "Plastic Surgeon for Nalgonda | AR Plastic Surgery",
        ("Nalgonda patients visit AR Plastic Surgery, Karimnagar for full-scope plastic, hand and cosmetic "
         "surgery — Dr Ashok Reddy, MBBS, DNB, M.Ch, Gold Medalist."),
        ("Nalgonda is one of Telangana's biggest districts — and a district this size deserves a genuine "
         "specialist option. For hand injuries, reconstructive needs and cosmetic procedures, AR Plastic Surgery "
         "in Karimnagar offers Nalgonda a full-scope practice led by a gold-medalist surgeon."),
        """<h2>What Nalgonda patients come for</h2>
<ul class="checklist">
<li><strong><a href="procedures/hand-trauma-surgery.html">Hand surgery</a></strong> — trauma, <a href="procedures/tendon-repair.html">tendon</a> and <a href="procedures/nerve-repair-microsurgery.html">nerve repair</a> by a trained microvascular surgeon.</li>
<li><strong>Reconstructive</strong> — <a href="procedures/burn-reconstruction.html">burn reconstruction</a>, <a href="procedures/cleft-lip-palate-repair.html">cleft repair</a>, <a href="procedures/scar-keloid-treatment.html">scar revision</a>.</li>
<li><strong>Cosmetic, surgeon-led</strong> — <a href="procedures/fue-hair-transplant.html">FUE hair transplant</a>, <a href="procedures/gynecomastia-surgery.html">gynecomastia</a>, <a href="procedures/rhinoplasty.html">rhinoplasty</a>, <a href="procedures/liposuction.html">liposuction</a>, <a href="procedures/tummy-tuck.html">tummy tuck</a>.</li>
<li><strong>Aesthetics</strong> — <a href="procedures/botox-treatment.html">Botox</a>, fillers, PRP, peels, lasers.</li>
</ul>
<h2 style="margin-top:1.8rem">Led by Dr Ashok Reddy</h2>
<p><strong>MBBS, DNB (Mumbai), M.Ch (Delhi), Gold Medalist</strong> — plastic, cosmetic, hand &amp; microvascular surgeon. Every case is planned and performed by the surgeon himself, starting with an honest consultation.</p>
<h2 style="margin-top:1.8rem">Visit us</h2>
<p><strong>Free OP consultations every Wednesday</strong>; open <strong>every day, 10:00 AM – 8:00 PM</strong>; 4.9-star Google rating. Call <a href="tel:+919182656866">+91 91826 56866</a> or <a href="contact.html">book online</a>.</p>""",
        [
         ("Do you treat patients from Nalgonda?",
          "Yes — patients from Nalgonda visit the Karimnagar clinic regularly."),
         ("What should I bring to my first consultation?",
          "Any previous medical records, prescriptions or photos related to your concern — and your questions."),
         ("How do I book?",
          "Call +91 91826 56866 or book online. Wednesday OP consultations are free."),
        ])

def page_narayanpet():
    return town_page(
        "Narayanpet",
        "Plastic Surgeon for Narayanpet | AR Plastic Surgery",
        ("Hand care and specialist plastic surgery for Narayanpet patients at AR Plastic Surgery, Karimnagar "
         "— Dr Ashok Reddy, MBBS, DNB, M.Ch, Gold Medalist."),
        ("Narayanpet's handlooms are famous — and hands that weave for a living deserve a hand specialist when "
         "something goes wrong. For overuse injuries, carpal tunnel, cuts and fractures, AR Plastic Surgery in "
         "Karimnagar offers the district a trained hand &amp; microvascular surgeon."),
        """<h2>Hands that work hard need specialist care</h2>
<p>Repetitive hand work — weaving, craft, farm labour — wears on tendons and nerves over time. <strong>Dr Ashok Reddy — MBBS, DNB (Mumbai), M.Ch (Delhi), Gold Medalist</strong> — is a trained hand &amp; microvascular surgeon:</p>
<ul class="checklist">
<li><strong><a href="procedures/carpal-tunnel-release.html">Carpal tunnel release</a></strong> — for numbness, tingling and night pain in the hand.</li>
<li><strong><a href="procedures/tendon-repair.html">Tendon repair</a></strong> — restoring finger movement after injury or division.</li>
<li><strong><a href="procedures/hand-trauma-surgery.html">Hand trauma surgery</a></strong> — fractures, deep cuts and crush injuries.</li>
<li><strong><a href="procedures/nerve-repair-microsurgery.html">Nerve repair</a></strong> — microsurgical reconnection for lost sensation and function.</li>
</ul>
<h2 style="margin-top:1.8rem">The complete practice behind it</h2>
<p><a href="procedures/burn-reconstruction.html">Burn reconstruction</a>, <a href="procedures/cleft-lip-palate-repair.html">cleft repair</a>, <a href="procedures/scar-keloid-treatment.html">scar revision</a> — and cosmetic procedures (<a href="procedures/fue-hair-transplant.html">hair transplant</a>, <a href="procedures/gynecomastia-surgery.html">gynecomastia</a>, <a href="procedures/rhinoplasty.html">rhinoplasty</a>) with private consultations.</p>
<h2 style="margin-top:1.8rem">Visit us from Narayanpet</h2>
<p><strong>Free OP consultations every Wednesday</strong>; open <strong>daily, 10:00 AM – 8:00 PM</strong>. Call <a href="tel:+919182656866">+91 91826 56866</a> or <a href="contact.html">book online</a>.</p>""",
        [
         ("My hands go numb at night — what could it be?",
          "It may be carpal tunnel or another nerve issue — but only an examination can tell. Book a Wednesday free OP for an assessment."),
         ("Do you treat patients from Narayanpet?",
          "Yes — Narayanpet is within the clinic's service area."),
         ("How do I book?",
          "Call +91 91826 56866 or book online. Wednesday OP consultations are free."),
        ])

def page_nirmal():
    return town_page(
        "Nirmal",
        "Plastic Surgeon for Nirmal | AR Plastic Surgery",
        ("Hand trauma and full-scope plastic surgery for Nirmal patients at AR Plastic Surgery, Karimnagar — "
         "Dr Ashok Reddy, MBBS, DNB, M.Ch, Gold Medalist."),
        ("Nirmal's famed woodcraft is hand work — and hands that carve, cut and shape deserve specialist care "
         "when injured. Beyond craft injuries, the district needs reconstructive and cosmetic expertise too. "
         "AR Plastic Surgery in Karimnagar is the nearest full-scope practice."),
        """<h2>For the district's working hands</h2>
<p><strong>Dr Ashok Reddy — MBBS, DNB (Mumbai), M.Ch (Delhi), Gold Medalist</strong> — trained hand &amp; microvascular surgeon:</p>
<ul class="checklist">
<li><strong><a href="procedures/hand-trauma-surgery.html">Hand trauma surgery</a></strong> — cuts, fractures and crush injuries, urgently assessed.</li>
<li><strong><a href="procedures/tendon-repair.html">Tendon</a> &amp; <a href="procedures/nerve-repair-microsurgery.html">nerve repair</a></strong> — microsurgical reconstruction with guided rehabilitation.</li>
<li><strong><a href="procedures/carpal-tunnel-release.html">Carpal tunnel release</a></strong> — for chronic hand numbness.</li>
</ul>
<h2 style="margin-top:1.8rem">Reconstructive and cosmetic, under one roof</h2>
<p><a href="procedures/burn-reconstruction.html">Burn reconstruction</a>, <a href="procedures/cleft-lip-palate-repair.html">cleft repair</a>, <a href="procedures/scar-keloid-treatment.html">scar revision</a> — plus <a href="procedures/fue-hair-transplant.html">hair transplant</a>, <a href="procedures/gynecomastia-surgery.html">gynecomastia</a>, <a href="procedures/rhinoplasty.html">rhinoplasty</a> and <a href="procedures/botox-treatment.html">Botox</a>, all surgeon-led.</p>
<h2 style="margin-top:1.8rem">Getting here</h2>
<p>Well connected north to Karimnagar. <strong>Free OP consultations every Wednesday</strong>; open <strong>every day, 10:00 AM – 8:00 PM</strong>. For hand emergencies call <a href="tel:+919182656866">+91 91826 56866</a> at once — or <a href="contact.html">book online</a>.</p>""",
        [
         ("Do you treat patients from Nirmal?",
          "Yes — Nirmal is within the clinic's service area across northern Telangana."),
         ("A craft tool cut my finger deeply — can it be repaired?",
          "Possibly — timing matters greatly with tendon and nerve injuries. Call +91 91826 56866 promptly."),
         ("How do I book?",
          "Call +91 91826 56866 or book online. Wednesday OP consultations are free."),
        ])

def page_peddapalli_district():
    return town_page(
        "Peddapalli District",
        "Plastic Surgeon for Peddapalli District | AR Plastic Surgery",
        ("District-wide plastic, hand and cosmetic surgery for Peddapalli district — AR Plastic Surgery, "
         "Karimnagar. Dr Ashok Reddy, MBBS, DNB, M.Ch, Gold Medalist."),
        ("This is the district-level guide — for Peddapalli town itself, see our <a href=\"peddapalli-plastic-surgeon.html\">Peddapalli town guide</a>. "
         "Across the wider district, from the Ramagundam industrial belt to its rural mandals, the pattern is the same: "
         "hand injuries at work, and reconstructive and cosmetic needs with no local specialist. AR Plastic Surgery in "
         "Karimnagar serves the whole district."),
        """<h2>The district picture: industry + villages</h2>
<p>Peddapalli district pairs thermal power and coal-linked industry around Ramagundam with farming villages — both produce hand injuries that need a specialist. <strong>Dr Ashok Reddy — MBBS, DNB (Mumbai), M.Ch (Delhi), Gold Medalist</strong> — is a trained hand &amp; microvascular surgeon:</p>
<ul class="checklist">
<li><strong><a href="procedures/hand-trauma-surgery.html">Hand trauma surgery</a></strong> — industrial and agricultural injuries, urgently assessed.</li>
<li><strong><a href="procedures/tendon-repair.html">Tendon</a> &amp; <a href="procedures/nerve-repair-microsurgery.html">nerve repair</a></strong> — microsurgical reconstruction.</li>
<li><strong><a href="procedures/burn-reconstruction.html">Burn reconstruction</a></strong> — including workplace and household burns.</li>
<li><strong><a href="procedures/cleft-lip-palate-repair.html">Cleft repair</a> &amp; <a href="procedures/scar-keloid-treatment.html">scar revision</a></strong> — for families across the district.</li>
</ul>
<h2 style="margin-top:1.8rem">Cosmetic care for the district</h2>
<p><a href="procedures/fue-hair-transplant.html">FUE hair transplant</a>, <a href="procedures/gynecomastia-surgery.html">gynecomastia surgery</a>, <a href="procedures/rhinoplasty.html">rhinoplasty</a>, <a href="procedures/liposuction.html">liposuction</a> — confidential consultations, procedures performed by the surgeon himself. If you're in Peddapalli town, our <a href="peddapalli-plastic-surgeon.html">town guide</a> has town-specific detail.</p>
<h2 style="margin-top:1.8rem">Visit us</h2>
<p><strong>Free OP consultations every Wednesday</strong>; open <strong>daily, 10:00 AM – 8:00 PM</strong>; 4.9-star Google rating. Call <a href="tel:+919182656866">+91 91826 56866</a> or <a href="contact.html">book online</a>.</p>""",
        [
         ("How is this different from the Peddapalli town guide?",
          "The town guide focuses on Peddapalli town; this page covers the wider district — Ramagundam, surrounding towns and rural mandals."),
         ("Do you treat industrial hand injuries?",
          "Yes — hand trauma, tendon and nerve injuries are a core specialty. Call +91 91826 56866 promptly for urgent injuries."),
         ("How do I book?",
          "Call +91 91826 56866 or book online. Wednesday OP consultations are free."),
        ])

def page_rajanna_sircilla():
    return town_page(
        "Rajanna Sircilla",
        "Plastic Surgeon for Rajanna Sircilla | AR Plastic Surgery",
        ("District-wide plastic and hand surgery for Rajanna Sircilla — AR Plastic Surgery, Karimnagar. "
         "Dr Ashok Reddy, MBBS, DNB, M.Ch, Gold Medalist."),
        ("This is the district guide — for Sircilla town itself, see our <a href=\"sircilla-plastic-surgeon.html\">Sircilla town guide</a>. "
         "Rajanna Sircilla district is Telangana's textile heartland, and textile work is hand work: powerloom injuries, "
         "repetitive strain, cuts. The district also needs reconstructive and cosmetic expertise. AR Plastic Surgery in "
         "Karimnagar covers it all."),
        """<h2>A textile district needs a hand surgeon</h2>
<p>Powerlooms don't forgive inattention — and when they injure a hand, the difference between a dressing and a specialist decides the outcome. <strong>Dr Ashok Reddy — MBBS, DNB (Mumbai), M.Ch (Delhi), Gold Medalist</strong> — trained hand &amp; microvascular surgeon:</p>
<ul class="checklist">
<li><strong><a href="procedures/hand-trauma-surgery.html">Hand trauma surgery</a></strong> — loom and machinery injuries, urgently assessed.</li>
<li><strong><a href="procedures/tendon-repair.html">Tendon repair</a></strong> — restoring movement after cuts.</li>
<li><strong><a href="procedures/carpal-tunnel-release.html">Carpal tunnel release</a></strong> — for chronic numbness from repetitive work.</li>
<li><strong><a href="procedures/scar-keloid-treatment.html">Scar revision</a></strong> — after healed workplace injuries.</li>
</ul>
<h2 style="margin-top:1.8rem">Beyond the workplace</h2>
<p><a href="procedures/burn-reconstruction.html">Burn reconstruction</a>, <a href="procedures/cleft-lip-palate-repair.html">cleft repair</a> — and cosmetic procedures (<a href="procedures/fue-hair-transplant.html">hair transplant</a>, <a href="procedures/gynecomastia-surgery.html">gynecomastia</a>, <a href="procedures/liposuction.html">liposuction</a>) with confidential consultations. Sircilla town residents: see the <a href="sircilla-plastic-surgeon.html">town guide</a>.</p>
<h2 style="margin-top:1.8rem">Close enough for easy follow-up</h2>
<p>The district borders Karimnagar — follow-up visits are straightforward. <strong>Free OP consultations every Wednesday</strong>; open <strong>daily, 10:00 AM – 8:00 PM</strong>. Call <a href="tel:+919182656866">+91 91826 56866</a> or <a href="contact.html">book online</a>.</p>""",
        [
         ("How is this different from the Sircilla town guide?",
          "The town guide focuses on Sircilla town; this page covers the whole Rajanna Sircilla district including Vemulawada and surrounding areas."),
         ("Do you treat powerloom hand injuries?",
          "Yes — hand trauma is a core specialty. For urgent injuries, call +91 91826 56866 immediately."),
         ("How do I book?",
          "Call +91 91826 56866 or book online. Wednesday OP consultations are free."),
        ])

def page_rangareddy():
    return town_page(
        "Rangareddy",
        "Plastic Surgeon for Rangareddy | AR Plastic Surgery",
        ("Rangareddy patients travel to AR Plastic Surgery, Karimnagar for personal, surgeon-led plastic surgery "
         "— Dr Ashok Reddy, MBBS, DNB, M.Ch, Gold Medalist."),
        ("Rangareddy rings Hyderabad — close to every big hospital, yet many of its residents travel to AR Plastic "
         "Surgery in Karimnagar. The reason is the same one Hyderabad patients give: a practice built around one "
         "gold-medalist surgeon, who consults, operates and follows up himself."),
        """<h2>Continuity the city can't offer</h2>
<p><strong>Dr Ashok Reddy — MBBS, DNB (Mumbai), M.Ch (Delhi), Gold Medalist</strong> — plastic, cosmetic, hand &amp; microvascular surgeon. At AR, your surgical plan is the surgeon's own, and aftercare is with the same doctor who operated — a contrast many patients actively seek out.</p>
<h2 style="margin-top:1.8rem">What Rangareddy patients come for</h2>
<ul class="checklist">
<li><strong>Cosmetic, surgeon-performed</strong> — <a href="procedures/fue-hair-transplant.html">FUE hair transplant</a>, <a href="procedures/gynecomastia-surgery.html">gynecomastia</a>, <a href="procedures/rhinoplasty.html">rhinoplasty</a>, <a href="procedures/liposuction.html">liposuction</a>, <a href="procedures/tummy-tuck.html">tummy tuck</a>.</li>
<li><strong><a href="procedures/hand-trauma-surgery.html">Hand &amp; microvascular</a></strong> — tendon, nerve and microsurgical reconstruction, including industrial injuries from the district's pharma and manufacturing belt.</li>
<li><strong>Reconstructive</strong> — <a href="procedures/burn-reconstruction.html">burns</a>, <a href="procedures/scar-keloid-treatment.html">scars</a>, <a href="procedures/cleft-lip-palate-repair.html">cleft repair</a>.</li>
<li><strong>Aesthetics</strong> — <a href="procedures/botox-treatment.html">Botox</a>, fillers, PRP, peels, lasers.</li>
</ul>
<h2 style="margin-top:1.8rem">Planned around minimal travel</h2>
<p><strong>Free OP consultations every Wednesday</strong>; surgery and follow-ups scheduled efficiently. Open <strong>every day, 10:00 AM – 8:00 PM</strong>; 4.9-star Google rating. Call <a href="tel:+919182656866">+91 91826 56866</a> or <a href="contact.html">book online</a>.</p>""",
        [
         ("Why travel from Rangareddy to Karimnagar?",
          "For one-surgeon continuity — consultation, operation and aftercare with the same gold-medalist surgeon, rather than a rotating hospital team."),
         ("Do you treat industrial hand injuries?",
          "Yes — hand trauma, tendon and nerve injuries are a core specialty. Call promptly for urgent injuries."),
         ("How do I book?",
          "Call +91 91826 56866 or book online. Wednesday OP consultations are free."),
        ])

def page_sangareddy():
    return town_page(
        "Sangareddy",
        "Plastic Surgeon for Sangareddy | AR Plastic Surgery",
        ("Industrial hand trauma and full-scope plastic surgery for Sangareddy patients at AR Plastic Surgery, "
         "Karimnagar — Dr Ashok Reddy, MBBS, DNB, M.Ch, Gold Medalist."),
        ("Sangareddy's industrial belt — Zaheerabad's factories and the district's manufacturing units — runs on "
         "hands, and injured hands need a specialist fast. AR Plastic Surgery in Karimnagar is the nearest "
         "practice with a trained hand &amp; microvascular surgeon, alongside full cosmetic and reconstructive care."),
        """<h2>When the factory floor injures a hand</h2>
<p>Machinery injuries are often the worst hand injuries — crush, degloving, amputation. <strong>Dr Ashok Reddy — MBBS, DNB (Mumbai), M.Ch (Delhi), Gold Medalist</strong> — is trained for exactly this:</p>
<ul class="checklist">
<li><strong><a href="procedures/hand-trauma-surgery.html">Hand trauma surgery</a></strong> — urgent specialist assessment.</li>
<li><strong><a href="procedures/microsurgery-free-flap.html">Microsurgical reconstruction</a></strong> — rejoining tiny vessels and nerves, rebuilding tissue.</li>
<li><strong><a href="procedures/tendon-repair.html">Tendon</a> &amp; <a href="procedures/nerve-repair-microsurgery.html">nerve repair</a></strong> — with structured rehabilitation.</li>
<li><strong><a href="procedures/fingertip-replantation.html">Fingertip replantation</a></strong> — where salvage is possible.</li>
</ul>
<h2 style="margin-top:1.8rem">The wider practice</h2>
<p><a href="procedures/burn-reconstruction.html">Burn reconstruction</a>, <a href="procedures/scar-keloid-treatment.html">scar revision</a>, <a href="procedures/cleft-lip-palate-repair.html">cleft repair</a> — and cosmetic procedures (<a href="procedures/fue-hair-transplant.html">hair transplant</a>, <a href="procedures/gynecomastia-surgery.html">gynecomastia</a>, <a href="procedures/rhinoplasty.html">rhinoplasty</a>) with confidential consultations.</p>
<h2 style="margin-top:1.8rem">Act fast on injuries</h2>
<p>For hand emergencies, call <a href="tel:+919182656866">+91 91826 56866</a> immediately — time decides outcomes. For planned care, <strong>free OP consultations every Wednesday</strong>; open <strong>daily, 10:00 AM – 8:00 PM</strong>. <a href="contact.html">Book online</a>.</p>""",
        [
         ("A machine injured a worker's hand — what now?",
          "Keep the hand still, preserve any amputated tissue in a clean cool bag, and call +91 91826 56866 immediately — these injuries are time-critical."),
         ("Do you treat patients from Sangareddy?",
          "Yes — Sangareddy is within the clinic's service area."),
         ("How do I book planned care?",
          "Call +91 91826 56866 or book online. Wednesday OP consultations are free."),
        ])

def page_siddipet_district():
    return town_page(
        "Siddipet District",
        "Plastic Surgeon for Siddipet District | AR Plastic Surgery",
        ("District-wide plastic, hand and cosmetic surgery for Siddipet district — AR Plastic Surgery, Karimnagar. "
         "Dr Ashok Reddy, MBBS, DNB, M.Ch, Gold Medalist."),
        ("This is the district guide — for Siddipet town itself, see our <a href=\"siddipet-plastic-surgeon.html\">Siddipet town guide</a>. "
         "Beyond the town, Siddipet district's mandals have the same gap the town has: no dedicated plastic surgery "
         "practice. For hand injuries, reconstructive needs and cosmetic procedures, the district's nearest "
         "full-scope option is AR Plastic Surgery in Karimnagar."),
        """<h2>Beyond the town: the district's needs</h2>
<p><strong>Dr Ashok Reddy — MBBS, DNB (Mumbai), M.Ch (Delhi), Gold Medalist</strong> — plastic, cosmetic, hand &amp; microvascular surgeon:</p>
<ul class="checklist">
<li><strong><a href="procedures/hand-trauma-surgery.html">Hand surgery</a></strong> — trauma, <a href="procedures/tendon-repair.html">tendon</a> and <a href="procedures/nerve-repair-microsurgery.html">nerve</a> care by a microvascular specialist.</li>
<li><strong><a href="procedures/burn-reconstruction.html">Burn reconstruction</a> &amp; <a href="procedures/cleft-lip-palate-repair.html">cleft repair</a></strong> — staged reconstructive care for families.</li>
<li><strong><a href="procedures/scar-keloid-treatment.html">Scar revision</a></strong> — for restrictive or prominent scars.</li>
<li><strong>Cosmetic, confidential</strong> — <a href="procedures/fue-hair-transplant.html">hair transplant</a>, <a href="procedures/gynecomastia-surgery.html">gynecomastia</a>, <a href="procedures/liposuction.html">liposuction</a>, <a href="procedures/rhinoplasty.html">rhinoplasty</a>.</li>
</ul>
<h2 style="margin-top:1.8rem">Siddipet town residents</h2>
<p>See the <a href="siddipet-plastic-surgeon.html">Siddipet town guide</a> for town-specific detail. For everyone in the district: <strong>free OP consultations every Wednesday</strong>, open <strong>daily 10:00 AM – 8:00 PM</strong>, 4.9-star Google rating. Call <a href="tel:+919182656866">+91 91826 56866</a> or <a href="contact.html">book online</a>.</p>""",
        [
         ("How is this different from the Siddipet town guide?",
          "The town guide focuses on Siddipet town; this page serves the wider district's towns and mandals."),
         ("Do you treat patients from rural mandals?",
          "Yes — patients from across the district visit the Karimnagar clinic."),
         ("How do I book?",
          "Call +91 91826 56866 or book online. Wednesday OP consultations are free."),
        ])

def page_suryapet():
    return town_page(
        "Suryapet",
        "Plastic Surgeon for Suryapet | AR Plastic Surgery",
        ("Full-scope plastic, hand and cosmetic surgery for Suryapet patients at AR Plastic Surgery, Karimnagar "
         "— Dr Ashok Reddy, MBBS, DNB, M.Ch, Gold Medalist."),
        ("Suryapet sits on the highway network of southern Telangana — well travelled, but with no full-scope "
         "plastic surgery practice of its own. For hand injuries, reconstructive needs and cosmetic procedures, "
         "AR Plastic Surgery in Karimnagar is the specialist option for the district."),
        """<h2>What Suryapet patients come for</h2>
<ul class="checklist">
<li><strong><a href="procedures/hand-trauma-surgery.html">Hand surgery</a></strong> — trauma, <a href="procedures/tendon-repair.html">tendon</a> and <a href="procedures/nerve-repair-microsurgery.html">nerve repair</a> by a trained microvascular surgeon.</li>
<li><strong>Reconstructive</strong> — <a href="procedures/burn-reconstruction.html">burn reconstruction</a>, <a href="procedures/cleft-lip-palate-repair.html">cleft repair</a>, <a href="procedures/scar-keloid-treatment.html">scar revision</a>.</li>
<li><strong>Cosmetic, surgeon-led</strong> — <a href="procedures/fue-hair-transplant.html">FUE hair transplant</a>, <a href="procedures/gynecomastia-surgery.html">gynecomastia</a>, <a href="procedures/rhinoplasty.html">rhinoplasty</a>, <a href="procedures/liposuction.html">liposuction</a>.</li>
<li><strong>Aesthetics</strong> — <a href="procedures/botox-treatment.html">Botox</a>, fillers, PRP, peels, lasers.</li>
</ul>
<h2 style="margin-top:1.8rem">Led by Dr Ashok Reddy</h2>
<p><strong>MBBS, DNB (Mumbai), M.Ch (Delhi), Gold Medalist</strong> — plastic, cosmetic, hand &amp; microvascular surgeon. Every case planned and performed by the surgeon himself, beginning with an honest consultation.</p>
<h2 style="margin-top:1.8rem">Visit us</h2>
<p><strong>Free OP consultations every Wednesday</strong>; open <strong>every day, 10:00 AM – 8:00 PM</strong>; 4.9-star Google rating. Call <a href="tel:+919182656866">+91 91826 56866</a> or <a href="contact.html">book online</a>.</p>""",
        [
         ("Do you treat patients from Suryapet?",
          "Yes — Suryapet is within the clinic's service area across Telangana."),
         ("Can consultation and planning happen in one visit?",
          "Usually, yes — many patients complete assessment and planning in a single Wednesday free OP visit."),
         ("How do I book?",
          "Call +91 91826 56866 or book online."),
        ])

def page_vikarabad():
    return town_page(
        "Vikarabad",
        "Plastic Surgeon for Vikarabad | AR Plastic Surgery",
        ("Reconstructive, hand and cosmetic surgery for Vikarabad patients at AR Plastic Surgery, Karimnagar — "
         "Dr Ashok Reddy, MBBS, DNB, M.Ch, Gold Medalist."),
        ("Vikarabad's Ananthagiri forests draw weekend travellers — but for its residents, specialist surgery has "
         "meant a Hyderabad trip. AR Plastic Surgery in Karimnagar offers the district a closer full-scope "
         "alternative, led by a gold-medalist surgeon."),
        """<h2>A closer specialist option</h2>
<p><strong>Dr Ashok Reddy — MBBS, DNB (Mumbai), M.Ch (Delhi), Gold Medalist</strong> — plastic, cosmetic, hand &amp; microvascular surgeon:</p>
<ul class="checklist">
<li><strong><a href="procedures/hand-trauma-surgery.html">Hand surgery</a></strong> — trauma, <a href="procedures/tendon-repair.html">tendon</a> and <a href="procedures/nerve-repair-microsurgery.html">nerve repair</a>.</li>
<li><strong><a href="procedures/burn-reconstruction.html">Burn reconstruction</a> &amp; <a href="procedures/cleft-lip-palate-repair.html">cleft repair</a></strong> — staged reconstructive care.</li>
<li><strong><a href="procedures/scar-keloid-treatment.html">Scar revision</a></strong> — for restrictive or prominent scars.</li>
<li><strong>Cosmetic, confidential</strong> — <a href="procedures/fue-hair-transplant.html">hair transplant</a>, <a href="procedures/gynecomastia-surgery.html">gynecomastia</a>, <a href="procedures/rhinoplasty.html">rhinoplasty</a>, <a href="procedures/botox-treatment.html">Botox</a>.</li>
</ul>
<h2 style="margin-top:1.8rem">Planning your visit</h2>
<p><strong>Free OP consultations every Wednesday</strong> — assessment and planning in one trip. Open <strong>every day, 10:00 AM – 8:00 PM</strong>; 4.9-star Google rating. Call <a href="tel:+919182656866">+91 91826 56866</a> or <a href="contact.html">book online</a>.</p>""",
        [
         ("Do you treat patients from Vikarabad?",
          "Yes — Vikarabad is within the clinic's service area."),
         ("Is it closer than Hyderabad for specialist care?",
          "For most of the district, yes — and a Wednesday free OP makes the first visit easy to plan."),
         ("How do I book?",
          "Call +91 91826 56866 or book online."),
        ])

def page_wanaparthy():
    return town_page(
        "Wanaparthy",
        "Plastic Surgeon for Wanaparthy | AR Plastic Surgery",
        ("Reconstructive, hand and cosmetic surgery for Wanaparthy patients at AR Plastic Surgery, Karimnagar — "
         "Dr Ashok Reddy, MBBS, DNB, M.Ch, Gold Medalist."),
        ("Wanaparthy's rural mandals are far from specialist surgery — which matters most when the need is urgent "
         "or life-changing: a hand injury, a child's cleft lip, a burn contracture. AR Plastic Surgery in "
         "Karimnagar is the reachable full-scope practice for the district."),
        """<h2>What a rural district needs from a plastic surgeon</h2>
<p><strong>Dr Ashok Reddy — MBBS, DNB (Mumbai), M.Ch (Delhi), Gold Medalist</strong> — plastic, cosmetic, hand &amp; microvascular surgeon:</p>
<ul class="checklist">
<li><strong><a href="procedures/hand-trauma-surgery.html">Hand trauma surgery</a></strong> — timely specialist care for injuries.</li>
<li><strong><a href="procedures/cleft-lip-palate-repair.html">Cleft lip &amp; palate repair</a></strong> — staged correction from infancy.</li>
<li><strong><a href="procedures/burn-reconstruction.html">Burn reconstruction</a></strong> — restoring movement and appearance.</li>
<li><strong><a href="procedures/scar-keloid-treatment.html">Scar revision</a></strong> — for scars that restrict or distress.</li>
</ul>
<h2 style="margin-top:1.8rem">Personal concerns, privately handled</h2>
<p><a href="procedures/fue-hair-transplant.html">Hair transplant</a>, <a href="procedures/gynecomastia-surgery.html">gynecomastia</a>, <a href="procedures/rhinoplasty.html">rhinoplasty</a> — confidential consultations and surgeon-performed procedures.</p>
<h2 style="margin-top:1.8rem">Make the journey count</h2>
<p><strong>Free OP consultations every Wednesday</strong>; open <strong>daily, 10:00 AM – 8:00 PM</strong>. Call <a href="tel:+919182656866">+91 91826 56866</a> or <a href="contact.html">book online</a>.</p>""",
        [
         ("Do you treat patients from Wanaparthy?",
          "Yes — Wanaparthy is within the clinic's service area across Telangana."),
         ("How do we minimise travel for treatment?",
          "Start with a free Wednesday OP — assessment and planning in one visit, then surgery scheduled around minimal travel."),
         ("How do I book?",
          "Call +91 91826 56866 or book online."),
        ])

def page_yadadri_bhuvanagiri():
    return town_page(
        "Yadadri Bhuvanagiri",
        "Plastic Surgeon for Yadadri Bhuvanagiri | AR Plastic Surgery",
        ("Full-scope plastic, hand and cosmetic surgery for Yadadri Bhuvanagiri patients at AR Plastic Surgery, "
         "Karimnagar — Dr Ashok Reddy, MBBS, DNB, M.Ch, Gold Medalist."),
        ("Yadadri Bhuvanagiri is known across Telangana for its temple — but its residents need everyday specialist "
         "care too. For hand injuries, reconstructive needs and cosmetic procedures, AR Plastic Surgery in "
         "Karimnagar is the district's nearest full-scope practice."),
        """<h2>Complete specialty, one roof</h2>
<p>Led by <strong>Dr Ashok Reddy — MBBS, DNB (Mumbai), M.Ch (Delhi), Gold Medalist</strong>, plastic, cosmetic, hand &amp; microvascular surgeon:</p>
<ul class="checklist">
<li><strong><a href="procedures/hand-trauma-surgery.html">Hand surgery</a></strong> — trauma, <a href="procedures/tendon-repair.html">tendon</a> and <a href="procedures/nerve-repair-microsurgery.html">nerve repair</a>.</li>
<li><strong>Reconstructive</strong> — <a href="procedures/burn-reconstruction.html">burn reconstruction</a>, <a href="procedures/cleft-lip-palate-repair.html">cleft repair</a>, <a href="procedures/scar-keloid-treatment.html">scar revision</a>.</li>
<li><strong>Cosmetic</strong> — <a href="procedures/fue-hair-transplant.html">FUE hair transplant</a>, <a href="procedures/gynecomastia-surgery.html">gynecomastia</a>, <a href="procedures/rhinoplasty.html">rhinoplasty</a>, <a href="procedures/liposuction.html">liposuction</a> — confidential, surgeon-led.</li>
<li><strong>Aesthetics</strong> — <a href="procedures/botox-treatment.html">Botox</a>, fillers, PRP, peels, lasers.</li>
</ul>
<h2 style="margin-top:1.8rem">Visit us</h2>
<p><strong>Free OP consultations every Wednesday</strong>; open <strong>every day, 10:00 AM – 8:00 PM</strong>; 4.9-star Google rating. Call <a href="tel:+919182656866">+91 91826 56866</a> or <a href="contact.html">book online</a>.</p>""",
        [
         ("Do you treat patients from Yadadri Bhuvanagiri?",
          "Yes — the district is within the clinic's service area."),
         ("What happens at a first consultation?",
          "An unhurried discussion, examination, and honest advice on your options — free on Wednesdays."),
         ("How do I book?",
          "Call +91 91826 56866 or book online."),
        ])

# ---------------------------------------------------------------- contact.html
def page_contact():
    title = "Contact & Book Appointment | AR Plastic Surgery"
    desc = ("Visit AR Plastic Surgery, Opp Reddy gari vantillu, Court Chowrasta, Karimnagar. "
            "Open Mon–Sun 10 AM–8 PM. Call +91 91826 56866 or book online.")
    map_q = "AR+Plastic+Surgery+Karimnagar+Telangana"
    district_guide_links = " · ".join(
        f'<a href="{slug}-plastic-surgeon.html">{name}</a>' for name, slug in DISTRICT_PAGES
    )
    body = f"""
<main><section><div class="wrap">
  <nav class="crumb" aria-label="Breadcrumb"><a href="index.html">Home</a> › Contact</nav>
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
      <p>The clinic welcomes patients from across Telangana. Find your district guide:</p>
      <p style="margin-top:.6rem">Town &amp; district guides: {district_guide_links}</p>
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
<p><a class="btn btn-solid" href="index.html">Home</a>
<a class="btn btn-outline" href="services.html" style="margin-left:.6rem">Services</a>
<a class="btn btn-outline" href="contact.html" style="margin-left:.6rem">Contact</a></p>
</div></section></main>"""
    return head(title, desc, "/404.html") + header("") + body + footer()

# ---------------------------------------------------------------- build + validate
PAGES = [
    ("index.html", page_index, 1.0),
    ("about.html", page_about, 0.8),
    ("services.html", page_services, 0.9),
    ("siddipet-plastic-surgeon.html", page_siddipet, 0.8),
    ("sircilla-plastic-surgeon.html", page_sircilla, 0.8),
    ("peddapalli-plastic-surgeon.html", page_peddapalli, 0.8),
    ("vemulawada-plastic-surgeon.html", page_vemulawada, 0.8),
    ("warangal-plastic-surgeon.html", page_warangal, 0.8),
    ("nizamabad-plastic-surgeon.html", page_nizamabad, 0.8),
    ("khammam-plastic-surgeon.html", page_khammam, 0.8),
    ("mancherial-plastic-surgeon.html", page_mancherial, 0.8),
    ("jagtial-plastic-surgeon.html", page_jagtial, 0.8),
    ("adilabad-plastic-surgeon.html", page_adilabad, 0.8),
    ("bhadradri-kothagudem-plastic-surgeon.html", page_bhadradri_kothagudem, 0.8),
    ("hanamkonda-plastic-surgeon.html", page_hanamkonda, 0.8),
    ("hyderabad-plastic-surgeon.html", page_hyderabad, 0.8),
    ("jangaon-plastic-surgeon.html", page_jangaon, 0.8),
    ("jayashankar-bhupalpally-plastic-surgeon.html", page_jayashankar_bhupalpally, 0.8),
    ("jogulamba-gadwal-plastic-surgeon.html", page_jogulamba_gadwal, 0.8),
    ("kamareddy-plastic-surgeon.html", page_kamareddy, 0.8),
    ("komaram-bheem-asifabad-plastic-surgeon.html", page_komaram_bheem_asifabad, 0.8),
    ("mahabubabad-plastic-surgeon.html", page_mahabubabad, 0.8),
    ("mahabubnagar-plastic-surgeon.html", page_mahabubnagar, 0.8),
    ("medak-plastic-surgeon.html", page_medak, 0.8),
    ("medchal-malkajgiri-plastic-surgeon.html", page_medchal_malkajgiri, 0.8),
    ("mulugu-plastic-surgeon.html", page_mulugu, 0.8),
    ("nagarkurnool-plastic-surgeon.html", page_nagarkurnool, 0.8),
    ("nalgonda-plastic-surgeon.html", page_nalgonda, 0.8),
    ("narayanpet-plastic-surgeon.html", page_narayanpet, 0.8),
    ("nirmal-plastic-surgeon.html", page_nirmal, 0.8),
    ("peddapalli-district-plastic-surgeon.html", page_peddapalli_district, 0.8),
    ("rajanna-sircilla-plastic-surgeon.html", page_rajanna_sircilla, 0.8),
    ("rangareddy-plastic-surgeon.html", page_rangareddy, 0.8),
    ("sangareddy-plastic-surgeon.html", page_sangareddy, 0.8),
    ("siddipet-district-plastic-surgeon.html", page_siddipet_district, 0.8),
    ("suryapet-plastic-surgeon.html", page_suryapet, 0.8),
    ("vikarabad-plastic-surgeon.html", page_vikarabad, 0.8),
    ("wanaparthy-plastic-surgeon.html", page_wanaparthy, 0.8),
    ("yadadri-bhuvanagiri-plastic-surgeon.html", page_yadadri_bhuvanagiri, 0.8),
    ("contact.html", page_contact, 0.8),
    ("404.html", page_404, 0.0),
    ("procedures/index.html", page_procedures_index, 0.9),
    ("blog/index.html", page_blog_index, 0.9),
]
for _p in PROCEDURES:
    PAGES.append((f"procedures/{_p['slug']}.html",
                  (lambda pp: lambda: page_procedure(pp))(_p), 0.8))
for _b in POSTS:
    PAGES.append((f"blog/{_b['slug']}.html",
                  (lambda bb: lambda: page_blog_post(bb))(_b), 0.7))

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
    for fname, fn, priority in PAGES:
        page_html = fn()
        path = os.path.join(OUT, fname)
        os.makedirs(os.path.dirname(path), exist_ok=True)
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
        if fname != "404.html" and priority > 0:
            sitemap_urls.append((fname, priority))
    # robots.txt
    with open(os.path.join(OUT, "robots.txt"), "w") as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: {BASE_URL}/sitemap.xml\n")
    # sitemap.xml
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.0.9">']
    for u, pr in sitemap_urls:
        sm.append(f"  <url><loc>{BASE_URL}/{u}</loc><changefreq>monthly</changefreq><priority>{pr}</priority></url>")
    sm.append("</urlset>")
    with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
        f.write("\n".join(sm))
    print(f"\nsitemap: {len(sitemap_urls)} urls | robots.txt written")

if __name__ == "__main__":
    main()
