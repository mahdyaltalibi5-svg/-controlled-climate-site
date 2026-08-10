# Controlled Climate Heating & Air — website

Static site. No framework, no build dependencies beyond Python 3 and (for
regenerating images) ImageMagick. 23 pages, zero third-party requests on first
paint, no web fonts.

```
build/config.py      ← ALL content lives here. This is the only file Andrew touches.
build/templates.py   ← layout, components, JSON-LD
build/build.py       ← generator:  python3 build/build.py  →  dist/
build/images.py      ← regenerates responsive image sets from source photos
src/assets/          ← css, js, images (copied into dist as-is)
dist/                ← the deployable site (generated — never edit by hand)
vercel.json          ← deploy config, caching, security headers
```

Rebuild after any content change:

```bash
python3 build/build.py
```

---

## 1. Deploy

**Vercel (recommended)**

1. Push this folder to a Git repo.
2. Import into Vercel. It reads `vercel.json`, runs `python3 build/build.py`,
   serves `dist/`.
3. Add the domain `controlledclimatehvac.com` + `www` in Vercel → Domains.
4. In GoDaddy: `A @ → 76.76.21.21` and `CNAME www → cname.vercel-dns.com`.

**Zero-build fallback:** `dist/` is a plain static folder. Drag it into Vercel,
Netlify, or any host. Nothing needs to run server-side.

---

## 2. Before launch — the ⚠️ CONFIRM list

Everything below is in `build/config.py`, marked `⚠️ CONFIRM`. Get these from
Andrew, then rebuild:

| Item | Why it matters |
|---|---|
| Business email | Shows in schema + contact |
| Street address + ZIP | **Only include if the GBP has a verified address.** If he's service-area-only on Google, leave `street` empty — a mismatch hurts local rankings |
| Year founded | Trust signal on the about page |
| Utah DOPL license number | Prints in the footer; homeowners look for it |
| Real hours | Google shows "Opens 7 AM Mon". The rest of the week is currently a guess |
| Google Business Profile share link | Enables the "Read all on Google" button |

**Reviews are placeholders.** `REVIEWS` in `config.py` currently holds four
written-for-layout quotes and there's a yellow warning banner on the page so
they can't ship by accident. Pull four real ones off the Google profile, paste
them in, and set `REVIEWS_ARE_PLACEHOLDER = False`.

The rating (5.0) and review count (40) *are* real and appear in
`aggregateRating` schema — update them when the count moves.

---

## 3. Tracking

Fill in `TRACKING` in `config.py` and rebuild. Nothing else changes.

```python
TRACKING = {
    "ga4_id": "G-XXXXXXXXXX",
    "gtm_id": "",                 # use GTM *or* GA4 direct, not both
    "google_ads_id": "AW-XXXXXXXXX",
    "call_conversion_label": "AW-XXXXXXXXX/AbC-D_efGh",
    "meta_pixel_id": "",
    "form_endpoint": "https://…",
}
```

### What's already instrumented

Every one of these fires a `dataLayer` push with full attribution attached:

| Event | Fires when |
|---|---|
| `call_click` | any `tel:` link — header, hero, sticky bar, footer, page body |
| `text_click` | the SMS link in the sticky bar |
| `form_submit` | a lead form posts successfully |
| `book_click` | "Request a time" / "Book" buttons |
| `scroll_depth` | 50 / 75 / 90% of a page |

Each payload also carries `link_location` (`hero`, `sticky_bar`, `footer`, …)
so you can see *which* CTA is actually producing calls, not just that calls
happened.

### Lead-source attribution — the part most contractor sites skip

`site.js` stores **first touch** and **last touch** in first-party
localStorage. That means when someone clicks a Google ad in July, forgets about
it, and calls in September, the lead still carries `first_source: google_ads`.

Every event and every form submission includes:

```
first_source, first_landing, first_seen,
last_source, last_landing, gclid, utm_campaign, page
```

Sources are classified automatically: `google_ads`, `google_organic`, `meta`,
`yelp`, `nextdoor`, `referral:<domain>`, `direct`.

**In GA4:** create custom dimensions for `first_source` and `link_location`, then
mark `call_click` and `form_submit` as key events. That's the whole reporting
setup.

### Form endpoint

The form posts JSON. Any of these work — pick one and paste the URL:

- **GHL** — inbound webhook trigger, maps straight into the pipeline
- **Formspree** — `https://formspree.io/f/xxxx`, fastest to stand up
- **Zapier / Make** — catch hook → wherever

Until an endpoint is set, the form shows a message pointing to the phone number
instead of silently failing. It's never a dead end.

### Call tracking (when you're ready)

Don't hardcode a second number. `site.js` has dynamic number insertion built in:

```js
window.CCHA.config.trackingNumbers = {
  google_ads:     { display: "(801) 555-0101", e164: "+18015550101" },
  google_organic: { display: "(801) 555-0102", e164: "+18015550102" },
  default:        { display: "(801) 680-7406", e164: "+18016807406" }
};
```

Every phone number on the page carries `data-phone`, so it swaps automatically
by traffic source. **Keep `default` set to the real GBP number** — the number
Google sees must match the Business Profile or NAP consistency breaks.

---

## 4. SEO structure

- Unique title, meta description, and canonical on all 23 pages
- `HVACBusiness` schema with real `aggregateRating`, hours, geo, and 18 cities
  in `areaServed`
- `Service` + `FAQPage` schema on every service and location page
- `BreadcrumbList` on every interior page
- Silo: home → services hub → 7 service pages, home → areas hub → 9 city pages,
  cross-linked both directions
- `sitemap.xml` + `robots.txt` generated on every build
- Semantic single `<h1>` per page, real `<h2>`/`<h3>` outline

**Location pages are written, not spun.** Each city page has genuinely
different content about that city's housing stock and the problems that come
with it. This is the difference between ranking and getting filtered as doorway
pages — do not templatize them when adding cities.

**Adding a city:** append a dict to `LOCATIONS` in `config.py` with real local
detail, rebuild, resubmit the sitemap. Nav, footer, sitemap, schema, and
internal links update automatically.

---

## 5. Speed

- No web fonts (system stack) — zero render-blocking font requests
- No JS framework; one deferred ~4kb script
- WebP + JPEG at 480/800/1400 with correct `sizes`, explicit `width`/`height`
  so there's no layout shift
- Hero image preloaded, everything below the fold lazy
- Assets fingerprint-cached for a year via `vercel.json`

Regenerate images after adding photos to `/home/claude/work/img`:
`python3 build/images.py`

---

## 6. Phase 2 — the chatbot

Deliberately not built yet, per the brief: launch clean, collect data, then add
it. The site is ready for it — drop the widget in `templates.py:page()` right
before `</body>`.

When you do build it, the qualification logic that matters:

**Don't shut down price shoppers.** Someone asking "how much for a furnace" is a
real buyer with no frame of reference. Give a range, then earn the call.

Suggested flow:

1. **Triage first, always.** "Is your system running right now?" No heat / no
   cool → skip everything else, push to call, show the number. Emergencies
   convert on the phone, not in chat.
2. **Repair or replace?** Age of system + symptom. Over 15 years + major
   symptom → replacement conversation. Under 10 → repair, book the diagnostic.
3. **Qualify without interrogating.** City (are we in area), homeowner or
   renter, single system or multiple. Three questions, not ten.
4. **Give the range.** "Full furnace replacements in the valley usually land
   between $X and $Y depending on size and efficiency. Want a firm number? It's
   a free estimate." Price transparency filters tire-kickers *for* you and
   builds trust with the serious ones.
5. **One clear exit.** Call now / book an estimate / text a photo. Not four
   options.

Everything the bot collects should push the same `dataLayer` shape as the form
(`form_submit` with attribution attached) so chat leads and form leads land in
the same reporting.

CRM integration order: form endpoint → GHL → chatbot. In that order, because
each one is only useful once the previous one is producing data.


---

## 7. Tracking dashboard — `/dashboard/`

`noindex`, `Disallow`-ed in robots.txt, and not in the sitemap. Not linked from
anywhere on the site — you have to type the URL.

Out of the box it reads the first-party event log in `localStorage`, so it shows
**this browser only**. That makes it a genuinely useful QA tool: tap a call
button on your phone, load `/dashboard/`, confirm the event fired with the right
`link_location` and source. No waiting on GA4's 24–48h processing.

To make it a real all-visitor dashboard, point it at an endpoint:

```js
// build/templates.py → site_config_js()
analyticsEndpoint: "https://your-endpoint"
```

Events are sent with `navigator.sendBeacon` (fires even as the page unloads, so
you don't lose the click that navigated away). The dashboard then requests
`?summary=1` and expects `{ events: [...] }` back.

Cheapest working backend: a Vercel Function writing to Vercel KV, or a Google
Apps Script bound to a Sheet. Either is under 30 lines. Do this **after** GA4 is
running — GA4 is the system of record; this is the fast read.

## 8. Logo

The mark in the header is a clean vector redraw of the flame-and-ice badge on
the sticker in Andrew's own install photo. Get the real file from him, drop it
in `src/assets/img/`, and set:

```python
BIZ["logo_file"] = "logo.png"
```

That swaps it everywhere — header, footer, and mobile. Ask for SVG or a
transparent PNG at 512px minimum.
