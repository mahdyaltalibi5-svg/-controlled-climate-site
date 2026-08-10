#!/usr/bin/env python3
"""Prepare responsive image assets for the Controlled Climate site.

Source photos are real job photos supplied by the client. Each one is emitted
as JPEG + WebP at two widths so the markup can use <picture> with srcset.
"""
import os
import subprocess
import sys

SRC = "/home/claude/work/img"
OUT = "/home/claude/work/cc/src/assets/img"

# source file -> (slug, crop mode)
#   "wide"  = 16:9 landscape crop, used for hero / banners
#   "card"  = 4:3 crop, used in galleries and page banners
PHOTOS = [
    ("IMG_6180.jpg", "ductwork-trunk", "card"),
    ("IMG_5516.jpg", "ductwork-rough-in", "card"),
    ("IMG_6870.jpeg", "furnace-install", "card"),
    ("IMG_6869.jpeg", "ac-install", "card"),
    ("IMG_6215.jpg", "mini-split-indoor", "card"),
    ("IMG_6216.jpg", "mini-split-outdoor", "card"),
    ("IMG_6865.jpg", "furnace-service", "card"),
]

WIDTHS = [1400, 800, 480]


def run(args):
    subprocess.run(args, check=True)


def main():
    os.makedirs(OUT, exist_ok=True)
    for src, slug, mode in PHOTOS:
        path = os.path.join(SRC, src)
        if not os.path.exists(path):
            print("missing", path, file=sys.stderr)
            continue
        ratio = "16:9" if mode == "wide" else "4:3"
        for w in WIDTHS:
            h = int(w * 9 / 16) if mode == "wide" else int(w * 3 / 4)
            for ext, q in (("jpg", "80"), ("webp", "76")):
                dest = os.path.join(OUT, f"{slug}-{w}.{ext}")
                run([
                    "convert", path,
                    "-auto-orient",
                    "-resize", f"{w}x{h}^",
                    "-gravity", "center",
                    "-extent", f"{w}x{h}",
                    "-strip",
                    "-quality", q,
                    "-interlace", "Plane" if ext == "jpg" else "None",
                    dest,
                ])
        print("built", slug, ratio)

    # Open Graph card: 1200x630 from the trunk-line photo
    run([
        "convert", os.path.join(SRC, "IMG_6180.jpg"),
        "-auto-orient", "-resize", "1200x630^", "-gravity", "center",
        "-extent", "1200x630", "-strip", "-quality", "82",
        os.path.join(OUT, "og-card.jpg"),
    ])
    print("built og-card")


if __name__ == "__main__":
    main()


# ---------------------------------------------------------------------------
# Extra crops added in the v2 design pass:
#  - "wide" 21:9 bands for full-bleed parallax sections
#  - tight detail crops so the same seven photos yield more visual moments
# ---------------------------------------------------------------------------
EXTRA = [
    # (source, slug, aspect, gravity, zoom%)
    ("IMG_6180.jpg", "band-ductwork", (21, 9), "center", 100),
    ("IMG_5516.jpg", "band-rough-in", (21, 9), "center", 100),
    ("IMG_6870.jpeg", "band-furnace", (21, 9), "center", 100),
    ("IMG_6869.jpeg", "detail-condenser", (1, 1), "center", 170),
    ("IMG_6870.jpeg", "detail-badge", (1, 1), "south", 200),
    ("IMG_6215.jpg", "detail-head", (1, 1), "center", 150),
    ("IMG_6180.jpg", "detail-seam", (1, 1), "north", 180),
]


def extras():
    import subprocess as sp
    for src, slug, (aw, ah), grav, zoom in EXTRA:
        path = os.path.join(SRC, src)
        for w in (1600, 900, 500):
            h = int(w * ah / aw)
            for ext, q in (("jpg", "80"), ("webp", "76")):
                sp.run([
                    "convert", path, "-auto-orient",
                    "-resize", f"{int(w*zoom/100)}x{int(h*zoom/100)}^",
                    "-gravity", grav, "-extent", f"{w}x{h}",
                    "-strip", "-quality", q,
                    os.path.join(OUT, f"{slug}-{w}.{ext}"),
                ], check=True)
        print("built extra", slug)


