# -*- coding: utf-8 -*-
"""Static site generator for Controlled Climate Heating & Air.

    python3 build/build.py            -> writes ./dist

Adding a service or a city means editing config.py and re-running this. Every
page, nav link, sitemap entry, and schema block is derived from that one file.
"""
import json
import os
import shutil
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import (BIZ, HOURS, SERVICES, LOCATIONS, ALSO_SERVED, GALLERY,
                    REVIEWS, REVIEWS_ARE_PLACEHOLDER, PROOF_POINTS, HOME_FAQS,
                    EMERGENCY_LINE)
import templates as T

# ---------------------------------------------------------------------------
# Reviews: prefer live Google data (build/reviews.json, written by reviews.py).
# Fall back to the placeholders in config.py and keep the warning banner up.
# ---------------------------------------------------------------------------
_RJ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reviews.json")
GOOGLE_ATTRIB = ""
if os.path.exists(_RJ):
    _d = json.load(open(_RJ, encoding="utf-8"))
    if _d.get("reviews"):
        REVIEWS = [{
            "quote": r["quote"],
            "author": r["author"],
            "city": r.get("relative_time", ""),
            "service": "Google review",
            "url": r.get("review_url") or r.get("author_url", ""),
        } for r in _d["reviews"]]
        REVIEWS_ARE_PLACEHOLDER = False
        GOOGLE_ATTRIB = _d.get("maps_url", "")
        if _d.get("rating"):
            BIZ["rating"] = _d["rating"]
        if _d.get("review_count"):
            BIZ["review_count"] = _d["review_count"]

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
DIST = os.path.join(ROOT, "dist")

PAGES = []   # (path, priority, changefreq)


def review_card(r):
    who = r["author"]
    if r.get("url"):
        who = f'<a href="{r["url"]}" rel="noopener nofollow" target="_blank" style="color:inherit">{who}</a>'
    meta = " &middot; ".join(x for x in (who, r.get("city"), r.get("service")) if x)
    return f"""<blockquote class="rev rv">
<div class="rev__stars" aria-label="5 out of 5 stars">{T.stars()}</div>
<p class="rev__q">{r['quote']}</p>
<div class="rev__m">{meta}</div>
</blockquote>"""


def review_flag():
    if GOOGLE_ATTRIB:
        return ('<p style="font-family:var(--mono);font-size:.66rem;letter-spacing:0;'
                'text-transform:uppercase;color:var(--steel);margin:0 0 22px">Reviews from '
                f'<a href="{GOOGLE_ATTRIB}" rel="noopener nofollow" target="_blank" '
                'style="color:var(--ember)">Google</a></p>')
    return ""


def proof_card(p):
    return f"""<article class="proof rv">
<div class="proof__k">{p['kicker']}</div>
<h3>{p['title']}</h3>
<p>{p['copy']}</p>
</article>"""


def social_proof_cards(limit=3):
    if REVIEWS_ARE_PLACEHOLDER:
        return "".join(proof_card(p) for p in PROOF_POINTS[:limit])
    return "".join(review_card(r) for r in REVIEWS[:limit])


def write(path, html, priority="0.6", changefreq="monthly", index=True):
    out = DIST if path in ("", "/") else os.path.join(DIST, path.strip("/"))
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    if index:
        PAGES.append((T.url(path), priority, changefreq))


# ===========================================================================
# HOME
# ===========================================================================
def build_home():
    svc_cards = "".join(f"""<a class="card card--{s['temp']} rv" href="/services/{s['slug']}/">
<span class="card__tag">{s['temp']}</span><h3>{s['name']}</h3><p>{s['lede']}</p><span class="card__more">See details</span></a>""" for s in SERVICES)

    shots = "".join(f"""<figure class="shot rv" style="margin:0">
<div class="reveal-img">{T.picture(slug, alt, "(max-width: 700px) 100vw, 33vw")}</div>
<figcaption class="shot__cap"><span class="shot__t">{kind} &middot; {where}</span>
<span class="shot__d">{alt}</span></figcaption></figure>""" for slug, alt, kind, where in GALLERY)

    revs = social_proof_cards(3)
    flag = review_flag()

    area_chips = "".join(f'<li><a href="/service-areas/{l["slug"]}/">{l["name"]}</a></li>' for l in LOCATIONS)
    area_extra = "".join(f"<li><span>{c}</span></li>" for c in ALSO_SERVED)

    steps = [
        ("You call, a person answers",
         "During business hours you get someone who can actually book you, not a "
         "voicemail tree. Tell us the symptom and we'll tell you whether it sounds "
         "urgent."),
        ("You get the next real window",
         "Not \"sometime Tuesday.\" We tell you the earliest realistic window before we "
         "hang up and call ahead when we're on the way."),
        ("Diagnosis before dollars",
         "We find the actual fault and show you what we found. You get the repair "
         "price before anyone touches a wrench."),
        ("Fixed, tested, cleaned up",
         "The system gets verified under load before we leave — temperature rise on "
         "heating, superheat and subcool on cooling. Then we haul our mess out."),
    ]
    step_html = "".join(f"""<div class="step rv"><div><h3>{t}</h3><p>{d}</p></div></div>""" for t, d in steps)
    discounts = [
        "Veterans",
        "Active-duty military",
        "National Guard &amp; Reserve",
        "Active law enforcement",
        "Retired law enforcement",
        "Active firefighters",
        "Retired firefighters",
        "Seniors 65+",
    ]
    discount_html = "".join(f'<li><span>{d}</span><strong>10%</strong></li>' for d in discounts)

    body = f"""
<section class="cc-inspection" aria-label="Controlled Climate HVAC precision inspection" data-hvac-scroll>
  <div class="cc-inspection__scene">
    <div class="cc-inspection__backdrop">{T.picture('ac-install', 'Controlled Climate installed outdoor air conditioner', '100vw')}</div>
    <div class="cc-inspection__shade" aria-hidden="true"></div>
    <div class="cc-inspection__model" aria-hidden="true">
      <canvas class="cc-inspection__canvas"></canvas>
      <div class="cc-inspection__halo"></div>
      <div class="cc-inspection__fallback"><span>CONTROLLED CLIMATE</span><strong>ENGINEERED FOR COMFORT.</strong></div>
    </div>
    <div class="cc-inspection__intro">
      <span class="cc-inspection__eyebrow">CONTROLLED CLIMATE HEATING &amp; AIR</span>
      <h1>Comfort,<br><em>down to the detail.</em></h1>
      <p>Heating and cooling done right, across the Salt Lake Valley.</p>
      <div class="cc-inspection__actions">
        {T.call_btn('cinematic-hero','cc-inspection__primary','Call Andrew’s team')}
        <a class="cc-inspection__secondary" href="/contact/">Request service</a>
      </div>
    </div>
    <div class="cc-inspection__tech cc-inspection__tech--one"><span>01 / AIRFLOW</span><strong>Fan &amp; motor</strong><small>Every part has a purpose.</small></div>
    <div class="cc-inspection__tech cc-inspection__tech--two"><span>02 / HEAT EXCHANGE</span><strong>Condenser coil</strong><small>Inside the system.</small></div>
    <div class="cc-inspection__tech cc-inspection__tech--three"><span>03 / HEART OF THE SYSTEM</span><strong>Compressor &amp; controls</strong><small>The details you don't see.</small></div>
    <div class="cc-inspection__final">
      <span class="cc-inspection__eyebrow">NOT JUST THE OUTSIDE.</span>
      <h2>Every part,<br><em>checked.</em></h2>
      <p>We care about what happens inside your system, because that's where reliable comfort starts.</p>
      <a href="/services/" class="cc-inspection__secondary">Explore our services</a>
    </div>
    <div class="cc-inspection__status"><span>01</span><div class="cc-inspection__meter"><i></i></div><span>03</span></div>
    <div class="cc-inspection__scroll">SCROLL TO EXPLORE <span aria-hidden="true">↓</span></div>
  </div>
</section>

<section class="intent">
<div class="wrap intent__in">
<div class="intent__head">
<p class="eyebrow rv">Start here</p>
<h2 class="rv-mask"><span>Pick the problem. Get the right next step.</span></h2>
</div>
<div class="intent__grid">
<a class="intent__item rv" href="tel:{BIZ['phone_e164']}" data-loc="intent_no_heat" data-phone="href">
<span>No heat</span><strong>Call now</strong><small>Priority scheduling</small></a>
<a class="intent__item rv" href="tel:{BIZ['phone_e164']}" data-loc="intent_no_cool" data-phone="href">
<span>No cool</span><strong>Call now</strong><small>Fast triage by phone</small></a>
<a class="intent__item rv" href="/services/furnace-installation/" data-track="intent_replace" data-loc="intent">
<span>Old system</span><strong>Replacement</strong><small>Right-sized quote</small></a>
<a class="intent__item rv" href="/services/ductwork-new-construction/" data-track="intent_new_build" data-loc="intent">
<span>Build / remodel</span><strong>Ductwork</strong><small>Rough-in and sheet metal</small></a>
</div>
</div></section>

<section class="section">
<div class="wrap">
<p class="eyebrow rv">What we do</p>
<div class="phead__grid mb-l">
<h2 style="margin:0" class="rv-mask"><span>Heating, cooling, and the ductwork in between.</span></h2>
<p class="lede rv" style="margin:0">Residential and new construction across the valley. Repairs on
every major brand, replacements sized to the house, and sheet metal built to fit.</p>
</div>
<div class="grid grid--3">{svc_cards}</div>
</div>
{T.details_strip([
  ("detail-badge", "Close detail of a newly installed Goodman furnace cabinet"),
  ("detail-condenser", "Condenser coil fins and fan guard on a new AC install"),
  ("detail-seam", "Sheet metal seam and hanger detail on a duct trunk line"),
  ("detail-head", "Ductless mini-split head vane detail"),
])}
</section>

<section class="section pricing">
<div class="wrap">
<div class="phead__grid mb-l">
<div>
<p class="eyebrow rv">Pricing transparency</p>
<h2 style="margin:0" class="rv-mask"><span>Know the entry cost before you call.</span></h2>
</div>
<p class="lede rv" style="margin:0">Controlled Climate keeps the first step clear without turning the site into a public price book. Repairs are still diagnosed, explained, and quoted before work begins.</p>
</div>
<div class="pricing__grid">
<article class="pricecard rv">
<div class="pricecard__top"><span>Standard service</span><small>Mon&ndash;Sat</small></div>
<dl>
<div><dt>Dispatch &amp; service call</dt><dd>$99</dd></div>
<div><dt>Diagnostic</dt><dd>$145</dd></div>
</dl>
</article>
<article class="pricecard pricecard--emergency rv">
<div class="pricecard__top"><span>Emergency / after-hours</span><small>Urgent calls</small></div>
<dl>
<div><dt>Emergency dispatch &amp; service call</dt><dd>$199</dd></div>
<div><dt>Emergency diagnostic</dt><dd>$245</dd></div>
</dl>
</article>
<article class="support rv">
<div class="support__head">
<p class="eyebrow">Who we support</p>
<h3>Community discounts</h3>
<p>Available to qualifying customers as a thank-you for service and support in the Salt Lake community.</p>
</div>
<ul>{discount_html}</ul>
</article>
</div>
<p class="pricing__note rv">These are initial dispatch, service-call, and diagnostic charges. Any repair, parts, equipment, or additional labor is quoted separately and approved before work begins. Discounts apply to qualifying service work and cannot be combined with other offers.</p>
</div>
</section>

{T.thermal_scrub()}

<section class="section section--ink section--process">
<div class="wrap">
<p class="eyebrow rv">What happens when you call</p>
<h2 class="mb-m rv-mask" style="max-width:18ch"><span>No mystery pricing, no runaround.</span></h2>
<div class="steps">{step_html}</div>
</div></section>

<section class="section section--tight"><div class="wrap">
<div class="phead__grid" style="align-items:center">
<div>
<p class="eyebrow rv">Who stands behind it</p>
<h2 style="max-width:16ch" class="rv-mask"><span>Owner-led. Technician accountable.</span></h2>
<p class="lede mt-s">Controlled Climate is owner-led and built around accountable field work.
Whether Andrew or a trained technician is on the call, the standard is the same: explain
what we found, price it clearly, and stand behind the work.</p>
<p style="margin-top:22px;font-size:1.05rem;color:var(--ink);border-left:3px solid var(--ember);padding-left:18px">
&ldquo;If a repair can get you through the season, we&rsquo;ll tell you that before talking replacement.&rdquo;
<span style="display:block;font-family:var(--mono);font-size:.66rem;letter-spacing:0;text-transform:uppercase;color:var(--steel);margin-top:10px">
Controlled Climate standard</span></p>
<p class="mt-m"><a class="btn btn--ghost" href="/about/">More about the shop</a></p>
</div>
<div class="banner reveal-img rv--scale rv">{T.picture('furnace-service', 'Controlled Climate service work on a Salt Lake Valley furnace and water heater', "(max-width: 860px) 100vw, 40vw")}</div>
</div></div></section>

<section class="section section--haze">
<div class="wrap">
<p class="eyebrow rv">Recent work</p>
<div class="phead__grid mb-l">
<h2 style="margin:0" class="rv-mask"><span>Actual jobs, actual photos.</span></h2>
<p class="lede" style="margin:0">Every photo below is our own work in the Salt Lake Valley.
No stock images of somebody else's install.</p>
</div>
<div class="grid grid--3">{shots}</div>
</div></section>

<section class="section">
<div class="wrap">
<p class="eyebrow rv">Reviews</p>
<div class="phead__grid mb-l">
<h2 style="margin:0" class="rv-mask"><span>{BIZ['rating']} stars across {BIZ['review_count']} Google reviews.</span></h2>
<p class="lede" style="margin:0">The pattern is simple:
show up, explain the diagnosis, and do not oversell the fix.</p>
</div>
{flag}
<div class="grid grid--3">{revs}</div>
<p class="mt-m"><a class="btn btn--ghost" href="/reviews/">Read more reviews</a></p>
</div></section>

{T.bleed_band("band-rough-in",
  "New construction duct rough-in coordinated with framing before drywall",
  "New construction",
  "The ductwork goes in before anyone can see it.",
  "That is exactly why it gets done properly. Trunk lines, takeoffs, gas piping and "
  "equipment set and sealed at the framing stage &mdash; laid out so it passes inspection "
  "the first time and moves air the way the drawings said it would.")}

<section class="section section--haze">
<div class="wrap">
<p class="eyebrow rv">Service area</p>
<h2 class="mb-m rv-mask"><span>Based in {BIZ['city']}. Working across the valley.</span></h2>
<ul class="chips mb-m">{area_chips}</ul>
<p style="color:var(--steel);font-size:.94rem;margin-bottom:12px">Also serving:</p>
<ul class="chips">{area_extra}</ul>
</div></section>

{T.faq_block(HOME_FAQS)}
{T.cta_band()}
"""

    write("", T.page(
        path="",
        title=f"HVAC in Taylorsville & Salt Lake City, UT | {BIZ['name']}",
        description=("Furnace and AC repair, replacement, and new construction ductwork in "
                     f"Taylorsville and across the Salt Lake Valley. {BIZ['rating']} stars, "
                     f"{BIZ['review_count']} Google reviews. Call {BIZ['phone_display']}."),
        body=body,
        schema=[T.biz_schema(),
                {"@context": "https://schema.org", "@type": "WebSite",
                 "@id": T.DOMAIN + "/#website",
                 "url": T.DOMAIN + "/", "name": BIZ["name"],
                 "publisher": {"@id": T.DOMAIN + "/#business"}},
                T.webpage_schema("", f"HVAC in Taylorsville & Salt Lake City, UT",
                                 "Furnace and AC repair across the Salt Lake Valley."),
                T.person_schema(),
                None if REVIEWS_ARE_PLACEHOLDER else T.review_items_schema(REVIEWS),
                T.faq_schema(HOME_FAQS)],
        preload_img="ductwork-trunk",
    ), priority="1.0", changefreq="weekly")


# ===========================================================================
# SERVICES
# ===========================================================================
def build_services_hub():
    cards = "".join(f"""<a class="card card--{s['temp']} rv" href="/services/{s['slug']}/">
<h3>{s['name']}</h3><p>{s['lede']}</p><span class="card__more">See details</span></a>""" for s in SERVICES)
    body = f"""{T.crumbs([("Home", "/"), ("Services", "/services/")])}
<section class="section section--tight"><div class="wrap">
<p class="eyebrow">Services</p>
<h1>What we work on</h1>
<p class="lede mt-s">Residential heating and cooling across Salt Lake County, plus new
construction ductwork and custom sheet metal. Repairs on every major brand.</p>
<div class="grid grid--3 mt-l">{cards}</div>
</div></section>
{T.cta_band()}"""
    write("services", T.page(
        path="services",
        title=f"HVAC Services in the Salt Lake Valley | {BIZ['name']}",
        description=("Furnace repair and replacement, AC repair and installation, ductless "
                     "mini-splits, ductwork, and seasonal maintenance across Salt Lake County. "
                     f"Call {BIZ['phone_display']}."),
        body=body,
        schema=[T.breadcrumbs_schema([("Home", "/"), ("Services", "/services/")])],
    ), priority="0.9")


def build_service(svc):
    path = f"services/{svc['slug']}"
    blocks = "".join(f"""<div class="prose__block rv"><h3>{h}</h3><p>{p}</p></div>"""
                     for h, p in svc["body"])
    other = "".join(f'<li><a href="/services/{s["slug"]}/">{s["name"]}</a></li>'
                    for s in SERVICES if s["slug"] != svc["slug"])
    areas = "".join(f'<li><a href="/service-areas/{l["slug"]}/">{l["name"]}</a></li>' for l in LOCATIONS)
    temp_cls = "plate--cold" if svc["temp"] == "cold" else ""

    body = f"""{T.crumbs([("Home", "/"), ("Services", "/services/"), (svc['name'], "/" + path + "/")])}
<section class="phead"><div class="wrap">
<div class="phead__grid">
<div>
<span class="plate {temp_cls} mb-m"><span class="dot"></span>{svc['name']} &middot; Salt Lake Valley</span>
<h1>{svc['h1']}</h1>
<p class="lede mt-s">{svc['lede']}</p>
<div class="hero__actions" style="margin-top:26px">
{T.call_btn('page_head', 'btn btn--call', f'Call {BIZ["phone_display"]}')}
<a class="btn btn--ghost" href="#request" data-track="scroll_to_form" data-loc="page_head">Request a callback</a>
</div>
</div>
<div class="banner reveal-img rv--scale rv">{T.picture(svc['photo'], svc['photo_alt'], "(max-width: 860px) 100vw, 40vw")}</div>
</div></div></section>
<hr class="seam">

<section class="section section--tight"><div class="wrap">
<div class="phead__grid" style="align-items:start">
<div class="prose">{blocks}</div>
<div id="request" style="position:sticky;top:96px">
{T.lead_form(svc['slug'], 'Get this handled', service_default=svc['slug'])}
</div>
</div></div></section>

<section class="section section--haze section--tight"><div class="wrap">
<p class="eyebrow rv">Where we work</p>
<h2 class="mb-m rv-mask"><span>{svc['name']} across the Salt Lake Valley</span></h2>
<ul class="chips">{areas}</ul>
</div></section>

{T.faq_block(svc['faqs'], f"{svc['name']} — common questions")}

<section class="section section--tight"><div class="wrap">
<p class="eyebrow">Also from us</p>
<ul class="chips">{other}</ul>
</div></section>
{T.cta_band()}"""

    write(path, T.page(
        path=path,
        title=svc["title"].format(city=BIZ["city"], biz=BIZ["short_name"]),
        description=svc["meta"].format(city=BIZ["city"], phone=BIZ["phone_display"]),
        body=body,
        og_image=f"{svc['photo']}-1400.jpg",
        schema=[T.breadcrumbs_schema([("Home", "/"), ("Services", "/services/"), (svc["name"], "/" + path + "/")]),
                T.service_schema(svc),
                T.webpage_schema(path, svc["h1"], svc["lede"], "WebPage", f"{svc['photo']}-1400.jpg"),
                T.faq_schema(svc["faqs"])],
    ), priority="0.9")


# ===========================================================================
# SERVICE AREAS
# ===========================================================================
def build_areas_hub():
    cards = "".join(f"""<a class="card rv" href="/service-areas/{l['slug']}/">
<h3>{l['name']}, UT</h3><p>{l['lede']}</p><span class="card__more">Service in {l['name']}</span></a>"""
                    for l in LOCATIONS)
    extra = "".join(f"<li><span>{c}</span></li>" for c in ALSO_SERVED)
    body = f"""{T.crumbs([("Home", "/"), ("Service areas", "/service-areas/")])}
<section class="section section--tight"><div class="wrap">
<p class="eyebrow">Service area</p>
<h1>Where we work</h1>
<p class="lede mt-s">We're based in {BIZ['city']} and cover Salt Lake County. If you're on
this list, you're in our normal service radius — no travel surcharge.</p>
<div class="grid grid--3 mt-l">{cards}</div>
<h2 class="mt-l mb-m" style="font-size:1.3rem">Also serving</h2>
<ul class="chips">{extra}</ul>
</div></section>
{T.cta_band()}"""
    write("service-areas", T.page(
        path="service-areas",
        title=f"HVAC Service Areas — Salt Lake County, UT | {BIZ['name']}",
        description=("Furnace and AC service in Taylorsville, Salt Lake City, West Valley City, "
                     "West Jordan, Murray, Kearns, Millcreek, Holladay, and Sandy. "
                     f"Call {BIZ['phone_display']}."),
        body=body,
        schema=[T.breadcrumbs_schema([("Home", "/"), ("Service areas", "/service-areas/")])],
    ), priority="0.8")


AREA_PHOTOS = ["furnace-install", "ac-install", "ductwork-trunk", "mini-split-indoor",
               "furnace-service", "ductwork-rough-in", "mini-split-outdoor"]
AREA_ALTS = {
    "furnace-install": "Newly installed gas furnace with custom sheet metal transition",
    "ac-install": "Air conditioning condenser set level on a new pad",
    "ductwork-trunk": "Custom sheet metal trunk line and takeoffs",
    "mini-split-indoor": "Ductless mini-split head mounted in a finished room",
    "furnace-service": "Furnace and water heater during a service call",
    "ductwork-rough-in": "Overhead duct layout coordinated with framing",
    "mini-split-outdoor": "Mini-split condenser wall-mounted on brackets",
}


def build_area(loc):
    path = f"service-areas/{loc['slug']}"
    photo = AREA_PHOTOS[LOCATIONS.index(loc) % len(AREA_PHOTOS)]
    svc_cards = "".join(f"""<a class="card card--{s['temp']} rv" href="/services/{s['slug']}/">
<h3>{s['name']}</h3><p>{s['lede']}</p>
<span class="card__more">{s['name']} in {loc['name']}</span></a>""" for s in SERVICES)
    nearby = [l for l in LOCATIONS if l["slug"] != loc["slug"]][:6]
    near_chips = "".join(f'<li><a href="/service-areas/{l["slug"]}/">{l["name"]}</a></li>' for l in nearby)

    faqs = [
        (f"Do you charge extra to come out to {loc['name']}?",
         f"No. {loc['name']} is inside our normal service radius from the shop in "
         f"{BIZ['city']} — there's no travel surcharge."),
        (f"How fast can you get to {loc['name']}?",
         "No-heat and no-cool calls get priority scheduling. Call and we'll give you "
         "the earliest realistic arrival window before you hang up."),
        (f"Do you handle both repairs and replacements in {loc['name']}?",
         "Both, plus maintenance, ductwork, and new construction. Most systems we look "
         "at can be repaired — we'll tell you honestly when replacement is the better spend."),
    ]

    body = f"""{T.crumbs([("Home", "/"), ("Service areas", "/service-areas/"), (loc['name'], "/" + path + "/")])}
<section class="phead"><div class="wrap">
<div class="phead__grid">
<div>
<span class="plate mb-m"><span class="dot"></span>{loc['name']}, Utah</span>
<h1>HVAC in {loc['name']}, UT</h1>
<p class="lede mt-s">{loc['lede']}</p>
<div class="hero__actions" style="margin-top:26px">
{T.call_btn('page_head', 'btn btn--call', f'Call {BIZ["phone_display"]}')}
<a class="btn btn--ghost" href="#request" data-track="scroll_to_form" data-loc="page_head">Request a callback</a>
</div>
</div>
<div class="banner reveal-img rv--scale rv">{T.picture(photo, AREA_ALTS[photo] + f' — {loc["name"]}, Utah', "(max-width: 860px) 100vw, 40vw")}</div>
</div></div></section>
<hr class="seam">

<section class="section section--tight"><div class="wrap">
<div class="phead__grid" style="align-items:start">
<div class="prose">
<div class="prose__block"><h3>What we see in {loc['name']} homes</h3><p>{loc['context']}</p></div>
<div class="prose__block"><h3>Neighborhoods and landmarks we cover</h3>
<p>{loc['landmarks']}, and everything around them. {loc['name']} is inside our standard
service radius from {BIZ['city']} — no travel surcharge, with priority scheduling for
no-heat and no-cool calls during heating and cooling season.</p></div>
<div class="prose__block"><h3>Emergency service</h3><p>{EMERGENCY_LINE} If the heat is out in
January or the AC quit in July, call rather than filling out the form — you'll get a faster answer.</p></div>
</div>
<div id="request" style="position:sticky;top:96px">
{T.lead_form(loc['slug'], f'Service in {loc["name"]}',
             sub=f"Tell us what's going on. We'll call back with the next available window for {loc['name']}.",
             city_value=loc['name'])}
</div>
</div></div></section>

<section class="section section--haze section--tight"><div class="wrap">
<p class="eyebrow rv">Services in {loc['name']}</p>
<h2 class="mb-l rv-mask"><span>What we handle here</span></h2>
<div class="grid grid--3">{svc_cards}</div>
</div></section>

{T.faq_block(faqs, f"{loc['name']} — common questions")}

<section class="section section--tight"><div class="wrap">
<p class="eyebrow">Nearby</p>
<ul class="chips">{near_chips}</ul>
</div></section>
{T.cta_band(f"Need HVAC service in {loc['name']}?",
            "Call and talk to someone who works on these systems. No-heat and no-cool calls get priority scheduling.")}"""

    write(path, T.page(
        path=path,
        title=f"HVAC {loc['name']}, UT — Furnace & AC Repair | {BIZ['short_name']}",
        description=(f"Furnace and AC repair, replacement, and maintenance in {loc['name']}, Utah. "
                     f"Priority scheduling for no-heat and no-cool calls. {BIZ['rating']} stars, "
                     f"{BIZ['review_count']} reviews. Call {BIZ['phone_display']}."),
        body=body,
        schema=[T.breadcrumbs_schema([("Home", "/"), ("Service areas", "/service-areas/"),
                                      (loc["name"], "/" + path + "/")]),
                T.city_business_schema(loc),
                T.webpage_schema(path, f"HVAC in {loc['name']}, UT", loc["lede"], "WebPage", f"{photo}-1400.jpg"),
                T.faq_schema(faqs),
                {"@context": "https://schema.org", "@type": "Service",
                 "serviceType": "HVAC repair and installation",
                 "provider": {"@id": T.DOMAIN + "/#business"},
                 "areaServed": {"@type": "City", "name": f"{loc['name']}, UT"}}],
    ), priority="0.8" if loc.get("primary") else "0.7")


# ===========================================================================
# REVIEWS / ABOUT / CONTACT / THANK YOU / 404
# ===========================================================================
def build_reviews():
    flag = review_flag()
    revs = social_proof_cards(6 if REVIEWS_ARE_PLACEHOLDER else len(REVIEWS))
    gplink = (f'<a class="btn btn--ghost" href="{BIZ["google_profile"]}" rel="noopener" '
              f'data-track="review_outbound" data-loc="reviews_page">Read all on Google</a>'
              if BIZ["google_profile"] else
              '<!-- Paste the Google Business Profile link into BIZ["google_profile"] to enable this button -->')

    body = f"""{T.crumbs([("Home", "/"), ("Reviews", "/reviews/")])}
<section class="section section--tight"><div class="wrap">
<p class="eyebrow">Reviews</p>
<h1>{BIZ['rating']} stars, {BIZ['review_count']} reviews</h1>
<p class="lede mt-s">Customers call for speed, clarity, and work that holds up. Controlled
Climate is built around those three promises on every repair, replacement, and rough-in.</p>
<div class="mt-l">{flag}</div>
<div class="grid grid--2">{revs}</div>
<p class="mt-l">{gplink}</p>
</div></section>
{T.cta_band("Want to be the next one?",
            "Call and we'll get you on the schedule. No-heat and no-cool calls get priority scheduling.")}"""
    write("reviews", T.page(
        path="reviews",
        title=f"Reviews — {BIZ['rating']} Stars from {BIZ['review_count']} Customers | {BIZ['name']}",
        description=(f"{BIZ['rating']} stars across {BIZ['review_count']} Google reviews for furnace "
                     "and AC service in Taylorsville, Salt Lake City, and the surrounding valley."),
        body=body,
        schema=[T.breadcrumbs_schema([("Home", "/"), ("Reviews", "/reviews/")]),
                T.webpage_schema("reviews", "Reviews", "Customer reviews.", "WebPage"),
                None if REVIEWS_ARE_PLACEHOLDER else T.review_items_schema(REVIEWS)],
    ), priority="0.7")


def build_about():
    shots = "".join(f"""<figure class="shot rv" style="margin:0">
<div class="reveal-img">{T.picture(slug, alt, "(max-width: 700px) 100vw, 33vw")}</div>
<figcaption class="shot__cap"><span class="shot__t">{kind} &middot; {where}</span>
<span class="shot__d">{alt}</span></figcaption></figure>""" for slug, alt, kind, where in GALLERY[:3])

    body = f"""{T.crumbs([("Home", "/"), ("About", "/about/")])}
<section class="phead"><div class="wrap">
<div class="phead__grid">
<div>
<span class="plate mb-m"><span class="dot"></span>Taylorsville, Utah</span>
<h1>Straight answers about your system</h1>
<p class="lede mt-s">{BIZ['name']} is an owner-led HVAC contractor in {BIZ['city']},
serving Salt Lake City and the surrounding valley. Heating, cooling, commercial
refrigeration, gas lines, and new-construction rough-in — residential and commercial.</p>
</div>
<div class="banner reveal-img rv--scale rv">{T.picture('ductwork-rough-in', 'Duct rough-in coordinated with framing on a new construction job', "(max-width: 860px) 100vw, 40vw")}</div>
</div></div></section>
<hr class="seam">

<section class="section section--tight"><div class="wrap narrow prose">
<div class="prose__block"><h3>Owner-led. Technician accountable.</h3>
<p>Andrew Scoggan leads Controlled Climate, but the promise is bigger than one person
showing up forever. Every technician is expected to diagnose carefully, explain the
options, quote before work begins, and leave work they can stand behind.</p></div>
<div class="prose__block"><h3>Why homeowners call us back</h3>
<p>Most people's experience with HVAC contractors is a number on an invoice and no
explanation of how it got there. We do it the other way around: find the actual fault,
show you what we found, quote the repair before touching it, and tell you honestly when
a repair isn't worth the money. That's the whole model, and it's why the reviews read
the way they do.</p></div>
<div class="prose__block"><h3>Residential, commercial, and new construction</h3>
<p>Day to day that means furnace and AC service calls across Salt Lake County. It also
means walk-in coolers and rooftop units on the commercial side, gas line runs, and duct
design and sheet metal fabrication for new builds. Both sides make the other better:
designing duct systems from scratch teaches you why one bedroom can run warm.</p></div>
<div class="prose__block"><h3>What we won't do</h3>
<p>Sell you a system you don't need. Quote a replacement without a load calculation.
Top off a leaking refrigerant charge every summer instead of finding the leak. Leave a
job without verifying the system under load.</p></div>
</div></section>

<section class="section section--haze section--tight"><div class="wrap">
<p class="eyebrow">The work</p><h2 class="mb-l">A few recent jobs</h2>
<div class="grid grid--3">{shots}</div>
</div></section>
{T.cta_band()}"""
    write("about", T.page(
        path="about",
        title=f"About {BIZ['name']} — Taylorsville, UT HVAC Contractor",
        description=("Taylorsville-based HVAC contractor serving Salt Lake City and the surrounding "
                     "valley. Furnace repair, air conditioning, ductwork, and new construction."),
        body=body,
        schema=[T.breadcrumbs_schema([("Home", "/"), ("About", "/about/")]),
                T.webpage_schema("about", "About", "Owner-led HVAC in Taylorsville.", "AboutPage"),
                T.person_schema()],
    ), priority="0.6")


def build_contact():
    hrs = "".join(
        f'<tr><td style="padding:7px 22px 7px 0;font-family:var(--mono);font-size:.78rem;letter-spacing:0;text-transform:uppercase;color:var(--steel)">{d}</td>'
        f'<td style="padding:7px 0;font-family:var(--mono);font-size:.9rem;color:var(--ink)">{T._h(o) + "–" + T._h(c) if o else "Closed"}</td></tr>'
        for d, o, c in HOURS)
    areas = "".join(f'<li><a href="/service-areas/{l["slug"]}/">{l["name"]}</a></li>' for l in LOCATIONS)

    body = f"""{T.crumbs([("Home", "/"), ("Contact", "/contact/")])}
<section class="section section--tight"><div class="wrap">
<p class="eyebrow">Contact</p>
<div class="phead__grid" style="align-items:start">
<div>
<h1>Get on the schedule</h1>
<p class="lede mt-s">Fastest route is the phone — someone picks up during business hours.
If it's after hours, the form gets you into the callback queue.</p>

<div class="mt-l" style="display:flex;flex-wrap:wrap;gap:12px">
{T.call_btn('contact', 'btn btn--call', f'Call {BIZ["phone_display"]}')}
<a class="btn btn--ghost" href="sms:{BIZ['phone_e164']}" data-loc="contact">Text us a photo</a>
</div>

<h2 class="mt-l" style="font-size:1.25rem">Hours</h2>
<table style="border-collapse:collapse;margin-top:8px">{hrs}</table>
<p class="mt-s" style="font-size:.9rem;color:var(--steel)">{EMERGENCY_LINE}</p>

<h2 class="mt-l" style="font-size:1.25rem">Service area</h2>
<p style="color:var(--steel);font-size:.94rem">Based in {BIZ['city']}, covering Salt Lake County.</p>
<ul class="chips mt-s">{areas}</ul>
</div>
<div>{T.lead_form('contact', 'Request a callback',
      sub="Fill this out and we'll call you back with the next available window.")}</div>
</div></div></section>"""
    write("contact", T.page(
        path="contact",
        title=f"Contact — {BIZ['name']} | {BIZ['phone_display']}",
        description=(f"Call {BIZ['phone_display']} for furnace and AC service in Taylorsville, Salt "
                     "Lake City, and the surrounding valley. Priority scheduling for no-heat and no-cool calls."),
        body=body,
        schema=[T.breadcrumbs_schema([("Home", "/"), ("Contact", "/contact/")]),
                T.webpage_schema("contact", "Contact", "Call for furnace and AC service.", "ContactPage"),
                T.biz_schema()],
    ), priority="0.8")


def build_thanks():
    body = f"""<section class="section"><div class="wrap narrow center">
<span class="plate mb-m"><span class="dot"></span>Request received</span>
<h1>Got it — we'll call you back.</h1>
<p class="lede" style="margin:18px auto 0">We'll get back to you with the next available window. If it's
urgent and you'd rather not wait, call us directly.</p>
<div class="hero__actions" style="justify-content:center;margin-top:32px">
{T.call_btn('thank_you', 'btn btn--call', f'Call {BIZ["phone_display"]}')}
<a class="btn btn--ghost" href="/">Back to the site</a>
</div></div></section>"""
    write("thank-you", T.page(
        path="thank-you", title=f"Thanks — we'll be in touch | {BIZ['short_name']}",
        description="Your service request was received.", body=body, noindex=True,
    ), index=False)


def build_404():
    svc = "".join(f'<li><a href="/services/{s["slug"]}/">{s["name"]}</a></li>' for s in SERVICES)
    body = f"""<section class="section"><div class="wrap narrow">
<span class="plate mb-m"><span class="dot"></span>Error 404</span>
<h1>That page isn't here.</h1>
<p class="lede mt-s">The system still is. Pick a service below or call and we'll sort it out.</p>
<ul class="chips mt-l">{svc}</ul>
<div class="hero__actions" style="margin-top:32px">
{T.call_btn('404', 'btn btn--call', f'Call {BIZ["phone_display"]}')}
<a class="btn btn--ghost" href="/">Go home</a></div>
</div></section>"""
    html = T.page(path="404", title="Page not found | " + BIZ["short_name"],
                  description="Page not found.", body=body, noindex=True)
    with open(os.path.join(DIST, "404.html"), "w", encoding="utf-8") as f:
        f.write(html)


# ===========================================================================
# SITEMAP / ROBOTS
# ===========================================================================
def build_dashboard():
    body = """<section class="section section--tight"><div class="wrap">
<p class="eyebrow">Internal &middot; not indexed</p>
<h1>Where the leads are coming from</h1>
<p class="lede mt-s" id="dash-note">Loading…</p>

<div class="dash mt-l">
<div class="stat"><div class="stat__k" id="s-leads">0</div><div class="stat__l">Lead actions</div></div>
<div class="stat"><div class="stat__k" id="s-calls">0</div><div class="stat__l">Calls started</div></div>
<div class="stat"><div class="stat__k" id="s-forms">0</div><div class="stat__l">Forms sent</div></div>
<div class="stat"><div class="stat__k" id="s-views">0</div><div class="stat__l">Page views</div></div>
<div class="stat"><div class="stat__k" id="s-rate">0%</div><div class="stat__l">Views to leads</div></div>
</div>

<h2 class="mt-l" style="font-size:1.35rem">Lead source</h2>
<p style="color:var(--steel);font-size:.92rem;max-width:60ch">First and last touch are both
stored, so an ad click in July that calls in September still shows as Google Ads.</p>
<div id="t-source" class="mt-s"></div>

<h2 class="mt-l" style="font-size:1.35rem">Which button they tapped</h2>
<p style="color:var(--steel);font-size:.92rem;max-width:60ch">If the sticky bar is producing
most of the calls, that tells you where to put the next one.</p>
<div id="t-cta" class="mt-s"></div>

<h2 class="mt-l" style="font-size:1.35rem">Page they converted on</h2>
<p style="color:var(--steel);font-size:.92rem;max-width:60ch">City and service pages earning
calls are the ones worth expanding.</p>
<div id="t-page" class="mt-s"></div>

<h2 class="mt-l" style="font-size:1.35rem">All events</h2>
<div id="t-event" class="mt-s"></div>

<h2 class="mt-l" style="font-size:1.35rem">Recent activity</h2>
<div id="t-recent" class="mt-s"></div>

<p class="mt-l"><button class="btn btn--ghost" id="dash-clear" type="button">Clear local events</button></p>
</div></section>
<script src="/assets/js/dashboard.js" defer></script>"""
    write("dashboard", T.page(
        path="dashboard", title="Tracking dashboard | " + BIZ["short_name"],
        description="Internal lead tracking.", body=body, noindex=True,
    ), index=False)


def build_html_sitemap():
    svc = "".join(f'<li><a href="/services/{x["slug"]}/">{x["name"]}</a></li>' for x in SERVICES)
    loc = "".join(f'<li><a href="/service-areas/{x["slug"]}/">{x["name"]}, UT</a></li>' for x in LOCATIONS)
    body = f"""{T.crumbs([("Home", "/"), ("Site map", "/sitemap/")])}
<section class="section section--tight"><div class="wrap">
<p class="eyebrow rv">Site map</p>
<h1>Every page</h1>
<div class="grid grid--3 mt-l">
<div><h2 style="font-size:1.2rem">Services</h2><ul class="ftr-list">{svc}</ul></div>
<div><h2 style="font-size:1.2rem">Service areas</h2><ul class="ftr-list">{loc}</ul></div>
<div><h2 style="font-size:1.2rem">Company</h2><ul class="ftr-list">
<li><a href="/">Home</a></li><li><a href="/about/">About</a></li>
<li><a href="/reviews/">Reviews</a></li><li><a href="/contact/">Contact</a></li></ul></div>
</div></div></section>
{T.cta_band()}"""
    write("sitemap", T.page(
        path="sitemap",
        title=f"Site map | {BIZ['name']}",
        description="Every page on the Controlled Climate Heating & Air site.",
        body=body,
        schema=[T.breadcrumbs_schema([("Home", "/"), ("Site map", "/sitemap/")])],
    ), priority="0.3")


def build_sitemap():
    today = date.today().isoformat()
    urls = "".join(
        f"<url><loc>{u}</loc><lastmod>{today}</lastmod>"
        f"<changefreq>{cf}</changefreq><priority>{p}</priority></url>"
        for u, p, cf in PAGES)
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
           + urls + "</urlset>")
    with open(os.path.join(DIST, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(xml)

    robots = (f"User-agent: *\nAllow: /\n"
              f"Disallow: /dashboard/\nDisallow: /thank-you/\n\n"
              f"Sitemap: {T.DOMAIN}/sitemap.xml\n")
    with open(os.path.join(DIST, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots)


# ===========================================================================
def main():
    if os.path.exists(DIST):
        shutil.rmtree(DIST)
    os.makedirs(DIST)
    shutil.copytree(os.path.join(SRC, "assets"), os.path.join(DIST, "assets"))

    build_home()
    build_services_hub()
    for s in SERVICES:
        build_service(s)
    build_areas_hub()
    for l in LOCATIONS:
        build_area(l)
    build_reviews()
    build_about()
    build_contact()
    build_thanks()
    build_html_sitemap()
    build_dashboard()
    build_404()
    build_sitemap()

    print(f"Built {len(PAGES)} indexed pages + thank-you + 404 -> {DIST}")
    for u, p, _ in PAGES:
        print("  ", p, u)


if __name__ == "__main__":
    main()
