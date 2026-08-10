#!/usr/bin/env python3
"""
Pull real Google reviews into the site.

Run this once to find the Place ID, then any time you want to refresh:

    export GOOGLE_MAPS_API_KEY=AIza...
    python3 build/reviews.py --find "Controlled Climate Heating & Air Taylorsville UT"
    # copy the place_id it prints into PLACE_ID below (or set GOOGLE_PLACE_ID)
    python3 build/reviews.py

It writes build/reviews.json. If that file exists, build.py uses it instead of
the placeholders in config.py and drops the warning banner automatically.

WHY THIS INSTEAD OF COPY-PASTE
------------------------------
Google's terms don't allow scraping and hardcoding review text. The Places API
does allow displaying it, provided the author's name links back to the review
and Google is credited — which this script and the templates handle.

It also means the reviews refresh themselves. When the count goes from 40 to
60, the site updates on the next build instead of going stale.

LIMIT: the Places API returns the 5 reviews Google considers most relevant, not
all of them. For a full scrolling wall of reviews you need a paid widget
(Elfsight, Trustindex, Reviews on My Website) or Andrew pasting his favourites
into config.py by hand — which he's free to do with his own reviews.

Cost: Place Details with the reviews field is a paid SKU, but Google's monthly
free credit covers a build-time call by an enormous margin.
"""
import argparse
import json
import os
import sys
import urllib.request
import urllib.error

API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY", "")
PLACE_ID = os.environ.get("GOOGLE_PLACE_ID", "")   # paste it here once you have it

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reviews.json")
MIN_RATING = 5          # only surface 5-star reviews on the site
MAX_REVIEWS = 5


def _req(url, method="GET", body=None, fields=""):
    headers = {"X-Goog-Api-Key": API_KEY, "Content-Type": "application/json"}
    if fields:
        headers["X-Goog-FieldMask"] = fields
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        sys.exit(f"Google API error {e.code}: {e.read().decode()[:500]}")


def find(query):
    r = _req("https://places.googleapis.com/v1/places:searchText", "POST",
             {"textQuery": query},
             "places.id,places.displayName,places.formattedAddress,places.rating,"
             "places.userRatingCount")
    for p in r.get("places", []):
        print(f"{p['id']}\n  {p['displayName']['text']} — {p.get('formattedAddress','')}\n"
              f"  {p.get('rating','?')} stars, {p.get('userRatingCount','?')} reviews\n")
    if not r.get("places"):
        print("No match. Try including the phone number in the query.")


def fetch():
    r = _req(f"https://places.googleapis.com/v1/places/{PLACE_ID}", "GET", None,
             "reviews,rating,userRatingCount,googleMapsUri")
    out = []
    for rev in r.get("reviews", []):
        if rev.get("rating", 0) < MIN_RATING:
            continue
        author = rev.get("authorAttribution", {})
        out.append({
            "quote": (rev.get("originalText") or rev.get("text") or {}).get("text", "").strip(),
            "author": author.get("displayName", "Google reviewer"),
            "author_url": author.get("uri", ""),
            "photo": author.get("photoUri", ""),
            "rating": rev.get("rating", 5),
            "relative_time": rev.get("relativePublishTimeDescription", ""),
            "review_url": rev.get("googleMapsUri", ""),
        })
    payload = {
        "source": "google_places_api",
        "rating": str(r.get("rating", "")),
        "review_count": str(r.get("userRatingCount", "")),
        "maps_url": r.get("googleMapsUri", ""),
        "reviews": out[:MAX_REVIEWS],
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    print(f"Wrote {len(payload['reviews'])} reviews to {OUT}")
    print(f"Live rating: {payload['rating']} from {payload['review_count']} reviews")
    print("Now run: python3 build/build.py")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--find", metavar="QUERY", help="look up the Place ID and exit")
    a = ap.parse_args()
    if not API_KEY:
        sys.exit("Set GOOGLE_MAPS_API_KEY first. See README section 3.")
    if a.find:
        find(a.find)
    elif not PLACE_ID:
        sys.exit("Set GOOGLE_PLACE_ID (or edit PLACE_ID in this file). "
                 "Run with --find to look it up.")
    else:
        fetch()
