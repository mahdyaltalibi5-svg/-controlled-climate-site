# -*- coding: utf-8 -*-
"""Layout shell, reusable components, and JSON-LD builders."""

import json
import os
import html as _html
from config import BIZ, HOURS, TRACKING, SERVICES, LOCATIONS, ALSO_SERVED, EMERGENCY_LINE

DOMAIN = BIZ["domain"].rstrip("/")
PHONE = BIZ["phone_display"]
TEL = BIZ["phone_e164"]
ASSET_VERSION = (os.environ.get("VERCEL_GIT_COMMIT_SHA") or "local")[:12]


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def url(path: str) -> str:
    if path in ("", "/"):
        return DOMAIN + "/"
    return DOMAIN + "/" + path.strip("/") + "/"


def rel(path: str) -> str:
    return "/" if path in ("", "/") else "/" + path.strip("/") + "/"


def depth_prefix(path: str) -> str:
    """Relative asset prefix so the build also opens straight off the filesystem."""
    n = len([p for p in path.strip("/").split("/") if p])
    return "../" * n if n else "./"


def call_btn(loc, cls="btn btn--call", label=None):
    label = label or f'<span class="num" data-phone="display">{PHONE}</span>'
    return (f'<a class="{cls}" href="tel:{TEL}" data-loc="{loc}" data-phone="href" '
            f'aria-label="Call {BIZ["short_name"]} at {PHONE}">{label}</a>')


def stars(n=5):
    return "★" * n


# ---------------------------------------------------------------------------
# structured data
# ---------------------------------------------------------------------------
def biz_schema():
    spec = []
    for day, o, c in HOURS:
        if o:
            spec.append({
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": f"https://schema.org/{day}",
                "opens": o, "closes": c,
            })
    addr = {"@type": "PostalAddress", "addressLocality": BIZ["city"],
            "addressRegion": BIZ["region"], "addressCountry": BIZ["country"]}
    if BIZ["street"]:
        addr["streetAddress"] = BIZ["street"]
    if BIZ["postal"]:
        addr["postalCode"] = BIZ["postal"]

    data = {
        "@context": "https://schema.org",
        "@type": "HVACBusiness",
        "@id": DOMAIN + "/#business",
        "name": BIZ["name"],
        "url": DOMAIN + "/",
        "founder": {"@type": "Person", "name": BIZ.get("owner", "")},
        "telephone": PHONE,
        "image": DOMAIN + "/assets/img/og-card.jpg",
        "priceRange": "$$",
        "address": addr,
        "geo": {"@type": "GeoCoordinates", "latitude": BIZ["lat"], "longitude": BIZ["lng"]},
        "openingHoursSpecification": spec,
        "areaServed": [{"@type": "City", "name": f'{l["name"]}, UT'} for l in LOCATIONS]
                      + [{"@type": "City", "name": f"{c}, UT"} for c in ALSO_SERVED],
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": BIZ["rating"],
            "reviewCount": BIZ["review_count"],
            "bestRating": "5",
        },
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "HVAC services",
            "itemListElement": [
                {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"],
                 "url": url("services/" + s["slug"])}} for s in SERVICES
            ],
        },
    }
    if BIZ["email"]:
        data["email"] = BIZ["email"]
    sames = [x for x in (BIZ["facebook"], BIZ["google_profile"]) if x]
    if sames:
        data["sameAs"] = sames
    return data


def breadcrumbs_schema(trail):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": name, "item": url(p)}
            for i, (name, p) in enumerate(trail)
        ],
    }


def faq_schema(faqs):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs
        ],
    }


def webpage_schema(path, title, description, ptype="WebPage", image=None):
    d = {
        "@context": "https://schema.org", "@type": ptype,
        "@id": url(path) + "#webpage",
        "url": url(path), "name": title, "description": description,
        "isPartOf": {"@id": DOMAIN + "/#website"},
        "about": {"@id": DOMAIN + "/#business"},
        "inLanguage": "en-US",
        "primaryImageOfPage": {"@type": "ImageObject",
                               "url": f"{DOMAIN}/assets/img/{image or 'og-card.jpg'}"},
    }
    return d


def city_business_schema(loc):
    """Per-city entity with a real service radius — the thing that actually
    helps a service-area business rank in nearby towns."""
    return {
        "@context": "https://schema.org",
        "@type": "HVACBusiness",
        "name": f'{BIZ["name"]} — {loc["name"]}',
        "parentOrganization": {"@id": DOMAIN + "/#business"},
        "url": url("service-areas/" + loc["slug"]),
        "telephone": PHONE,
        "image": DOMAIN + "/assets/img/og-card.jpg",
        "priceRange": "$$",
        "address": {"@type": "PostalAddress", "addressLocality": loc["name"],
                    "addressRegion": "UT", "addressCountry": "US"},
        "areaServed": {"@type": "GeoCircle",
                       "geoMidpoint": {"@type": "GeoCoordinates",
                                       "latitude": BIZ["lat"], "longitude": BIZ["lng"]},
                       "geoRadius": "32000"},
        "aggregateRating": {"@type": "AggregateRating", "ratingValue": BIZ["rating"],
                            "reviewCount": BIZ["review_count"], "bestRating": "5"},
    }


def review_items_schema(reviews):
    """Only emit Review schema when the text is real — fabricated reviews in
    structured data is a manual-action risk, not a shortcut."""
    if not reviews:
        return None
    return {
        "@context": "https://schema.org",
        "@type": "HVACBusiness",
        "@id": DOMAIN + "/#business",
        "name": BIZ["name"],
        "review": [{
            "@type": "Review",
            "reviewRating": {"@type": "Rating", "ratingValue": "5", "bestRating": "5"},
            "author": {"@type": "Person", "name": r["author"]},
            "reviewBody": r["quote"],
        } for r in reviews],
    }


def person_schema():
    return {
        "@context": "https://schema.org", "@type": "Person",
        "name": BIZ.get("owner", ""), "jobTitle": "Owner & Operator",
        "worksFor": {"@id": DOMAIN + "/#business"},
        "url": url("about"),
    }


def service_schema(svc, city=None):
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "serviceType": svc["name"],
        "provider": {"@id": DOMAIN + "/#business"},
        "areaServed": {"@type": "City", "name": f'{city or "Salt Lake City"}, UT'},
        "url": url("services/" + svc["slug"]),
    }


def ld(*objs):
    return "\n".join(
        f'<script type="application/ld+json">{json.dumps(o, ensure_ascii=False, separators=(",", ":"))}</script>'
        for o in objs if o
    )


# ---------------------------------------------------------------------------
# analytics
# ---------------------------------------------------------------------------
def analytics_head():
    t = TRACKING
    out = []
    if t["gtm_id"]:
        out.append(
            "<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),"
            "event:'gtm.js'});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'"
            "?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;"
            f"f.parentNode.insertBefore(j,f);}})(window,document,'script','dataLayer','{t['gtm_id']}');</script>")
    elif t["ga4_id"] or t["google_ads_id"]:
        primary = t["ga4_id"] or t["google_ads_id"]
        out.append(f'<script async src="https://www.googletagmanager.com/gtag/js?id={primary}"></script>')
        cfgs = "".join(f"gtag('config','{i}');" for i in (t["ga4_id"], t["google_ads_id"]) if i)
        out.append("<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}"
                   f"gtag('js',new Date());{cfgs}</script>")
    if t["meta_pixel_id"]:
        out.append(
            "<script>!function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?"
            "n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;n.push=n;"
            "n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;"
            "s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,document,'script',"
            f"'https://connect.facebook.net/en_US/fbevents.js');fbq('init','{t['meta_pixel_id']}');"
            "fbq('track','PageView');</script>")
    return "\n".join(out)


def site_config_js():
    return (
        "<script>window.CCHA={config:{"
        f'phoneDisplay:{json.dumps(PHONE)},'
        f'phoneE164:{json.dumps(TEL)},'
        f'formEndpoint:{json.dumps(TRACKING["form_endpoint"])},'
        f'adsConversion:{json.dumps(TRACKING["call_conversion_label"])},'
        'thankYouUrl:"/thank-you/",'
        "debug:false"
        "}};</script>"
    )


# ---------------------------------------------------------------------------
# chrome
# ---------------------------------------------------------------------------
LOGO = """<svg class="brand__mark" viewBox="0 0 100 100" aria-hidden="true" focusable="false">
<defs>
<path id="ccArc" d="M12,54 A38,38 0 0 1 88,54" fill="none"/>
<linearGradient id="ccFlame" x1="0" y1="1" x2="0" y2="0">
<stop offset="0%" stop-color="#b0380d"/><stop offset="45%" stop-color="#de4a15"/>
<stop offset="100%" stop-color="#f5a524"/></linearGradient>
<linearGradient id="ccIce" x1="0" y1="0" x2="0" y2="1">
<stop offset="0%" stop-color="#4fb3cc"/><stop offset="100%" stop-color="#14606f"/></linearGradient>
</defs>
<text font-family="var(--mono, monospace)" font-size="10.5" font-weight="500" letter-spacing="0"
      fill="currentColor"><textPath href="#ccArc" startOffset="50%" text-anchor="middle">CONTROLLED CLIMATE</textPath></text>
<path d="M50 34c5 6 9 11 9 16.5 0 3-1.7 5.4-4.3 6.6 1-2.6.4-5.2-1.6-7.4.1 2.6-.8 4.3-2.6 5.2-1.6.8-3.3.2-3.9-1.4-.5-1.4 0-2.8 1.2-4-2.9 1.4-4.6 3.9-4.6 7 0 .2 0 .4.1.6-2-1.3-3.3-3.5-3.3-6.6C40 45 45 39.9 50 34z" fill="url(#ccFlame)"/>
<path d="M23 60h54l-27-9z" fill="#0f1c22" opacity=".92"/>
<path d="M50 62 34 79h32zM50 62 26 71l8 8zM50 62l24 9-8 8z" fill="url(#ccIce)" opacity=".95"/>
<g stroke="#7fd0e4" stroke-width="1.6" stroke-linecap="round" opacity=".85">
<path d="M50 64v13M44 68l6 4 6-4M44 74l6-4 6 4"/></g>
</svg>"""


def brand_mark(on_dark=False):
    """Andrew's real logo when the file is present, the vector mark otherwise."""
    f = BIZ.get("logo_file")
    if f:
        return (f'<img class="brand__mark" src="/assets/img/{f}" alt="" width="46" height="46" '
                f'decoding="async">')
    return LOGO


def header(active=""):
    nav_items = [
        ("Services", "/services/", "services"),
        ("Service areas", "/service-areas/", "areas"),
        ("Reviews", "/reviews/", "reviews"),
        ("About", "/about/", "about"),
        ("Contact", "/contact/", "contact"),
    ]
    cur = ' aria-current="page"'
    links = "".join(
        '<a href="%s"%s>%s</a>' % (h, cur if k == active else "", t)
        for t, h, k in nav_items
    )
    return f"""<header class="hdr">
<div class="wrap hdr__in">
<a class="brand" href="/" aria-label="{BIZ['name']} home">{brand_mark()}
<span class="brand__txt"><span class="brand__name">Controlled Climate</span>
<span class="brand__sub">Salt Lake</span></span></a>
<nav class="nav" id="nav" aria-label="Main">{links}</nav>
<div class="hdr__cta">
<a class="hdr__phone" href="tel:{TEL}" data-loc="header" data-phone="href"><span data-phone="display">{PHONE}</span></a>
{call_btn("header_btn", "btn btn--call", "Call now")}
<button class="burger" type="button" aria-label="Menu" aria-expanded="false" aria-controls="nav">
<span></span><span></span><span></span></button>
</div></div></header>"""


def fab():
    return f"""<a class="fab" href="tel:{TEL}" data-loc="fab" data-phone="href"
aria-label="Call {BIZ['short_name']} at {PHONE}">
<span class="fab__ring"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.2.4 2.4.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.4 0 .8-.2 1l-2.3 2.2z"/></svg></span>
<span class="fab__txt"><small>Call now &middot; Mon&ndash;Sat</small><span class="num" data-phone="display">{PHONE}</span></span></a>"""


def callbar():
    return f"""<nav class="callbar" aria-label="Quick contact">
<a class="is-primary" href="tel:{TEL}" data-loc="sticky_bar" data-phone="href">
<strong>Call now</strong><span data-phone="display">{PHONE}</span></a>
<a href="sms:{TEL}" data-loc="sticky_bar"><strong>Text</strong><span>Send a photo</span></a>
<a href="/contact/" data-track="book_click" data-loc="sticky_bar"><strong>Book</strong><span>Request a time</span></a>
</nav>"""


def footer():
    svc_links = "".join(f'<li><a href="/services/{s["slug"]}/">{s["name"]}</a></li>' for s in SERVICES)
    loc_links = "".join(f'<li><a href="/service-areas/{l["slug"]}/">{l["name"]}</a></li>' for l in LOCATIONS[:6])
    hrs = []
    for day, o, c in HOURS:
        if o:
            hrs.append(f'<li>{day[:3]} <span style="color:#fff">{_h(o)}–{_h(c)}</span></li>')
        else:
            hrs.append(f'<li>{day[:3]} <span>Closed</span></li>')
    return f"""<footer class="ftr">
<div class="wrap">
<div class="ftr__grid">
<div>
<a class="brand" href="/" style="margin-bottom:16px">{brand_mark(True)}
<span class="brand__txt"><span class="brand__name" style="color:#fff">Controlled Climate</span>
<span class="brand__sub">Heating &amp; Air</span></span></a>
<p style="max-width:34ch;margin:14px 0 18px">{BIZ['tagline']} Serving {BIZ['city']} and the Salt Lake Valley.</p>
<a class="ftr__phone" href="tel:{TEL}" data-loc="footer" data-phone="href"><span data-phone="display">{PHONE}</span></a>
<p style="margin-top:14px;font-size:.85rem">{EMERGENCY_LINE}</p>
</div>
<div><h4>Services</h4><ul>{svc_links}</ul></div>
<div><h4>Service areas</h4><ul>{loc_links}<li><a href="/service-areas/">All areas →</a></li></ul></div>
<div><h4>Hours</h4><ul style="font-family:var(--mono);font-size:.78rem;letter-spacing:0">{''.join(hrs)}</ul>
<h4 style="margin-top:26px">More</h4><ul><li><a href="/about/">About</a></li>
<li><a href="/reviews/">Reviews</a></li><li><a href="/contact/">Contact</a></li>
<li><a href="/sitemap/">Site map</a></li>
{'<li><a href="' + BIZ['facebook'] + '" rel="noopener">Facebook</a></li>' if BIZ['facebook'] else ''}</ul></div>
</div>
<div class="ftr__legal">
<span>&copy; {2026} {BIZ['name']}. {BIZ['city']}, Utah.</span>
<span>Licensed &amp; insured HVAC contractor{(' &middot; Lic. ' + BIZ['license']) if BIZ['license'] else ''}</span>
</div></div></footer>"""


def _h(t):
    h, m = t.split(":")
    h = int(h)
    ap = "am" if h < 12 else "pm"
    h12 = h % 12 or 12
    return f"{h12}{'' if m == '00' else ':' + m}{ap}"


# ---------------------------------------------------------------------------
# reusable blocks
# ---------------------------------------------------------------------------
def picture(slug, alt, sizes="(max-width: 700px) 100vw, 50vw", cls="", lazy=True, w=1400, h=1050):
    load = 'loading="lazy" decoding="async"' if lazy else 'fetchpriority="high" decoding="async"'
    return f"""<picture>
<source type="image/webp" sizes="{sizes}" srcset="/assets/img/{slug}-480.webp 480w, /assets/img/{slug}-800.webp 800w, /assets/img/{slug}-1400.webp 1400w">
<img src="/assets/img/{slug}-800.jpg" sizes="{sizes}" srcset="/assets/img/{slug}-480.jpg 480w, /assets/img/{slug}-800.jpg 800w, /assets/img/{slug}-1400.jpg 1400w" alt="{alt}" width="{w}" height="{h}" class="{cls}" {load}>
</picture>"""


def wide(slug, alt, sizes="100vw", lazy=True):
    """21:9 band image for full-bleed sections."""
    load = 'loading="lazy" decoding="async"' if lazy else 'fetchpriority="high" decoding="async"'
    return f"""<picture>
<source type="image/webp" sizes="{sizes}" srcset="/assets/img/{slug}-500.webp 500w, /assets/img/{slug}-900.webp 900w, /assets/img/{slug}-1600.webp 1600w">
<img src="/assets/img/{slug}-900.jpg" sizes="{sizes}" srcset="/assets/img/{slug}-500.jpg 500w, /assets/img/{slug}-900.jpg 900w, /assets/img/{slug}-1600.jpg 1600w" alt="{alt}" width="1600" height="686" {load}></picture>"""


def square(slug, alt, sizes="(max-width: 700px) 50vw, 25vw"):
    return f"""<picture>
<source type="image/webp" sizes="{sizes}" srcset="/assets/img/{slug}-500.webp 500w, /assets/img/{slug}-900.webp 900w">
<img src="/assets/img/{slug}-500.jpg" sizes="{sizes}" srcset="/assets/img/{slug}-500.jpg 500w, /assets/img/{slug}-900.jpg 900w" alt="{alt}" width="900" height="900" loading="lazy" decoding="async"></picture>"""


def details_strip(items):
    """Tight crops used as texture between content sections."""
    cells = "".join(f'<div class="reveal-img">{square(slug, alt)}</div>' for slug, alt in items)
    return f'<div class="details">{cells}</div>'


def thermal_scrub():
    """Signature interaction: one control that is the whole business."""
    cold = json.dumps({
        "mode": "Cooling",
        "title": "Air conditioning, room by room.",
        "copy": "A system that's oversized cools fast, shuts off, and leaves the back "
                "bedroom ten degrees behind. We measure the load and balance the airflow "
                "so the house matches the thermostat.",
        "links": [["AC repair", "/services/ac-repair/"],
                  ["AC installation", "/services/ac-installation/"],
                  ["Mini-splits", "/services/ductless-mini-splits/"],
                  ["Refrigeration", "/services/commercial-refrigeration/"]],
    })
    hot = json.dumps({
        "mode": "Heating",
        "title": "Furnaces that don't quit in January.",
        "copy": "Sized to the house, vented right, and tested under load before we leave "
                "\u2014 because the coldest night of the year is a bad time to find out it "
                "was done cheap.",
        "links": [["Furnace repair", "/services/furnace-repair/"],
                  ["Furnace replacement", "/services/furnace-installation/"],
                  ["Gas lines", "/services/gas-lines/"],
                  ["Tune-ups", "/services/maintenance/"]],
    })
    cold = cold.replace("&", "&amp;").replace("'", "&#39;")
    hot = hot.replace("&", "&amp;").replace("'", "&#39;")
    return f"""<section class="scrub" data-scrub data-cold='{cold}' data-hot='{hot}'>
<div class="scrub__bg">
<img class="is-cold" src="/assets/img/mini-split-outdoor-1400.jpg" alt="" loading="lazy" decoding="async" width="1400" height="1050">
<img class="is-hot" src="/assets/img/furnace-install-1400.jpg" alt="" loading="lazy" decoding="async" width="1400" height="1050">
</div>
<div class="scrub__wash"></div>
<div class="wrap scrub__in">
<div class="scrub__head">
<div>
<p class="eyebrow rv" style="color:#93a2ad">Both halves of the job</p>
<div class="scrub__temp" data-scrub-temp>68&deg;</div>
<div class="scrub__mode" data-scrub-mode>Cooling</div>
</div>
<div style="flex:1;min-width:280px">
<h2 data-scrub-title>Air conditioning, room by room.</h2>
<p class="scrub__copy" data-scrub-copy></p>
</div>
</div>
<div class="scrub__track" role="slider" tabindex="0" aria-label="Drag between cooling and heating"
     aria-valuemin="0" aria-valuemax="100" aria-valuenow="50">
<div class="scrub__fill"></div><div class="scrub__handle"></div>
</div>
<div class="scrub__labels"><span>&larr; Cooling</span><span>Drag the dial</span><span>Heating &rarr;</span></div>
<ul class="scrub__list" data-scrub-list></ul>
</div></section>"""


def bleed_band(slug, alt, eyebrow, title, copy, cta=True):
    actions = ""
    if cta:
        actions = (f'<div class="hero__actions" style="margin-top:30px">{call_btn("bleed", "btn btn--call")}'
                   f'<a class="btn btn--onink-ghost" href="/contact/" data-track="book_click" data-loc="bleed">Request a time</a></div>')
    return f"""<section class="bleed">
<div class="bleed__media px" data-px="70">{wide(slug, alt)}</div>
<div class="wrap bleed__in">
<p class="eyebrow rv">{eyebrow}</p>
<h2 class="rv-mask"><span>{title}</span></h2>
<p class="lede rv" style="color:#b7c3cc">{copy}</p>
{actions}
</div></section>"""


def headline(lines):
    """Masked, line-by-line headline used for the load sequence."""
    return "".join(f'<span class="reveal-line"><span>{l}</span></span>' for l in lines)


def lead_form(name="quote", heading="Request service", sub=None, service_default="", city_value=""):
    opts = "".join(
        f'<option value="{s["name"]}"{" selected" if s["slug"] == service_default else ""}>{s["name"]}</option>'
        for s in SERVICES)
    sub = sub or "Tell us what's going on and we'll call you back with the next available window."
    city_attr = f' value="{_html.escape(city_value, quote=True)}"' if city_value else ""
    return f"""<form class="qform" data-lead="{name}" novalidate>
<h2>{heading}</h2>
<p class="qform__sub">{sub}</p>
<div class="field"><label for="{name}-n">Name</label>
<input id="{name}-n" name="name" type="text" autocomplete="name" required></div>
<div class="field"><label for="{name}-p">Phone</label>
<input id="{name}-p" name="phone" type="tel" autocomplete="tel" inputmode="tel" required></div>
<div class="field"><label for="{name}-c">City</label>
<input id="{name}-c" name="city" type="text" autocomplete="address-level2" placeholder="Taylorsville"{city_attr}></div>
<div class="field"><label for="{name}-s">What do you need?</label>
<select id="{name}-s" name="service"><option value="">Not sure yet</option>{opts}</select></div>
<div class="field"><label for="{name}-m">Details</label>
<textarea id="{name}-m" name="message" placeholder="Furnace is blowing cold air, started last night…"></textarea></div>
<label class="vh" for="{name}-hp">Leave blank</label>
<input class="vh" id="{name}-hp" name="company" type="text" tabindex="-1" autocomplete="off">
<button class="btn btn--call btn--wide" type="submit">Request a callback</button>
<div class="form-note" role="status" aria-live="polite"></div>
<p class="qform__fine">Or call <a href="tel:{TEL}" data-loc="form_fine" data-phone="href" style="color:var(--ember);font-weight:600"><span data-phone="display">{PHONE}</span></a> — someone picks up during business hours.</p>
</form>"""


def cta_band(title="Need it fixed soon?",
             copy="Call and talk to someone who works on these systems, not a call center. No-heat and no-cool calls get priority scheduling across the Salt Lake Valley."):
    return f"""<section class="band"><div class="wrap band__in">
<div><h2 class="rv-mask"><span>{title}</span></h2><p class="rv">{copy}</p></div>
<div class="band__actions">{call_btn('band', 'btn btn--call')}
<a class="btn btn--onink-ghost" href="/contact/" data-track="book_click" data-loc="band">Request a time</a></div>
</div></section>"""


def faq_block(faqs, heading="Common questions"):
    items = "".join(
        f'<details class="rv"><summary>{q}</summary><div>{a}</div></details>' for q, a in faqs)
    return f"""<section class="section section--tight"><div class="wrap narrow">
<p class="eyebrow rv">FAQ</p><h2 class="mb-m rv-mask"><span>{heading}</span></h2>
<div class="faq">{items}</div></div></section>"""


def crumbs(trail):
    parts = []
    for i, (name, p) in enumerate(trail):
        if i == len(trail) - 1:
            parts.append(f"<span aria-current='page'>{name}</span>")
        else:
            parts.append(f'<a href="{rel(p)}">{name}</a>')
    return '<div class="wrap"><nav class="crumbs" aria-label="Breadcrumb">' + \
           "<span>/</span>".join(parts) + "</nav></div>"


# ---------------------------------------------------------------------------
# page shell
# ---------------------------------------------------------------------------
def esc(t):
    """Escape for use inside HTML attributes / <title>, leaving existing entities alone."""
    import re as _re
    t = _re.sub(r"&(?!#?\w+;)", "&amp;", t)
    return t.replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def page(*, path, title, description, body, schema=None, og_image="og-card.jpg",
         noindex=False, preload_img=None):
    canon = url(path)
    title = esc(title)
    description = esc(description)
    robots = "noindex,nofollow" if noindex else "index,follow,max-image-preview:large"
    pre = ""
    if preload_img:
        pre = (f'<link rel="preload" as="image" type="image/webp" '
               f'imagesrcset="/assets/img/{preload_img}-480.webp 480w, '
               f'/assets/img/{preload_img}-800.webp 800w, '
               f'/assets/img/{preload_img}-1400.webp 1400w" imagesizes="100vw">')
    return f"""<!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canon}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#12161a">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{esc(BIZ['name'])}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{DOMAIN}/assets/img/{og_image}">
<meta name="twitter:card" content="summary_large_image">
<link rel="preload" as="style" href="/assets/css/site.css?v={ASSET_VERSION}">
<link rel="stylesheet" href="/assets/css/inspection.css?v={ASSET_VERSION}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap">
{pre}
<link rel="stylesheet" href="/assets/css/site.css?v={ASSET_VERSION}">
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
{analytics_head()}
{site_config_js()}
{ld(*(schema or []))}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="progress" aria-hidden="true"></div>
{header(_active_for(path))}
<main id="main">
{body}
</main>
{footer()}
{fab()}
{callbar()}
<script src="/assets/js/site.js?v={ASSET_VERSION}" defer></script>
</body>
</html>"""


def _active_for(path):
    p = path.strip("/")
    if p.startswith("services"):
        return "services"
    if p.startswith("service-areas"):
        return "areas"
    if p.startswith("reviews"):
        return "reviews"
    if p.startswith("about"):
        return "about"
    if p.startswith("contact"):
        return "contact"
    return ""
