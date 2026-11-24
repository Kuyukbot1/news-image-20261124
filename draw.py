#!/usr/bin/env python3
"""Draw the 24 November 2026 news front page (1024x1024) with Pillow.

Fresh build for make.fun news-image-20261124. All 50 stories come from
RESEARCH_24NOV.md. Deterministic: no random, no network, no time calls.
Run: python3 draw.py  ->  writes entry.png next to this file.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BASE = os.path.dirname(os.path.abspath(__file__))

CREAM = (247, 240, 220)
PAPER = (250, 244, 228)
NAVY = (20, 38, 74)
NAVY2 = (28, 52, 96)
INK = (26, 26, 26)
GREY = (90, 88, 80)
RED = (176, 42, 42)
GOLD = (201, 162, 39)
GOLD_L = (232, 205, 110)
LINE = (180, 168, 138)
SEA = (214, 230, 240)
LAND = (232, 218, 188)
LAND_L = (185, 167, 122)
WHITE = (255, 255, 255)
GREEN = (46, 125, 50)
BLUE = (42, 93, 176)
AMBER = (192, 122, 0)
PURPLE = (106, 63, 160)
TEAL = (0, 131, 143)

REGION_COLOR = {
    "Americas": RED, "Europe": BLUE, "Mideast": AMBER, "Africa": GREEN,
    "Asia": PURPLE, "Oceania": TEAL, "Global": (85, 85, 85),
}

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, font, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_lines(d, x, y, text, font, width, fill, leading=None):
    lines = wrap(d, text, font, width)
    lh = leading or int(font.size * 1.25)
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y


# ---------------------------------------------------------------- scenes
def scene_nvidia(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 60, 30))
    d.rectangle([x, y, x + w, y + 14], fill=(10, 40, 20))
    d.text((x + 6, y + 2), "NVDA", font=F(SANS_B, 9), fill=GOLD_L)
    # chip
    cx, cy, cw, ch = x + w // 2 - 26, y + h // 2 - 8, 52, 30
    d.rectangle([cx, cy, cx + cw, cy + ch], fill=(118, 185, 0), outline=(200, 230, 120))
    d.rectangle([cx + 8, cy + 7, cx + cw - 8, cy + ch - 7], fill=(16, 60, 30))
    d.text((cx + 13, cy + 9), "AI", font=F(SANS_B, 11), fill=(118, 185, 0))
    for i in range(5):
        px = cx + 6 + i * 10
        d.line([px, cy - 5, px, cy], fill=(118, 185, 0), width=2)
        d.line([px, cy + ch, px, cy + ch + 5], fill=(118, 185, 0), width=2)
    # rising arrow
    pts = [(x + 8, y + h - 12), (x + w * 0.35, y + h * 0.55),
           (x + w * 0.6, y + h * 0.62), (x + w - 12, y + 20)]
    d.line(pts, fill=(140, 220, 90), width=3, joint="curve")
    d.polygon([(x + w - 12, y + 20), (x + w - 24, y + 20), (x + w - 12, y + 32)],
              fill=(140, 220, 90))
    d.text((x + w - 52, y + h - 16), "+31%", font=F(SANS_B, 12), fill=(140, 220, 90))


def scene_korea(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(178, 214, 235))
    d.rectangle([x, y + h - 22, x + w, y + h], fill=(90, 140, 90))
    # island
    d.ellipse([x + w * 0.32, y + h - 34, x + w * 0.68, y + h - 8], fill=(120, 165, 110))
    d.polygon([(x + w * 0.45, y + h - 34), (x + w * 0.55, y + h - 34),
               (x + w * 0.5, y + h - 52)], fill=(90, 130, 90))
    # radar tower
    d.line([x + w * 0.5, y + h - 30, x + w * 0.5, y + 26], fill=INK, width=3)
    d.ellipse([x + w * 0.5 - 8, y + 14, x + w * 0.5 + 8, y + 30], fill=WHITE,
              outline=INK)
    d.arc([x + w * 0.5 - 22, y + 2, x + w * 0.5 + 22, y + 46], 200, 340,
          fill=RED, width=2)
    d.arc([x + w * 0.5 - 32, y - 8, x + w * 0.5 + 32, y + 56], 200, 340,
          fill=RED, width=2)
    # jets
    for jx, jy in [(x + 12, y + 22), (x + w - 34, y + 34)]:
        d.polygon([(jx, jy), (jx + 18, jy + 4), (jx, jy + 8)], fill=(60, 60, 60))
    d.rectangle([x + 4, y + 4, x + 44, y + 16], fill=RED)
    d.text((x + 7, y + 5), "ALERT", font=F(SANS_B, 8), fill=WHITE)


def scene_nato(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(200, 222, 240))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(140, 170, 120))
    # AWACS plane with dome
    px, py = x + w * 0.18, y + h * 0.42
    d.ellipse([px + 18, py - 16, px + 52, py + 2], fill=WHITE, outline=INK)
    d.polygon([(px, py), (px + 78, py - 2), (px + 86, py + 6), (px + 8, py + 10)],
              fill=(220, 225, 230), outline=INK)
    d.polygon([(px + 70, py - 2), (px + 88, py - 2), (px + 80, py + 6)],
              fill=(180, 185, 190), outline=INK)
    d.polygon([(px + 30, py + 8), (px + 40, py + 8), (px + 34, py + 20)],
              fill=(180, 185, 190), outline=INK)
    d.text((px + 20, py + 2), "AWACS", font=F(SANS_B, 7), fill=NAVY)
    # radar waves (hero only; the mini scene keeps the plane and flag)
    if w >= 120:
        for r in (14, 24):
            d.arc([x + w - 46 - r, y + 12 - r, x + w - 46 + r, y + 12 + r],
                  270, 90, fill=RED, width=2)
        d.text((x + w - 62, y + 2), "POLAND", font=F(SANS_B, 8), fill=RED)
    d.rectangle([x + 4, y + h - 22, x + 60, y + h - 8], fill=WHITE)
    d.rectangle([x + 4, y + h - 22, x + 60, y + h - 15], fill=WHITE)
    d.rectangle([x + 4, y + h - 22, x + 28, y + h - 15], fill=RED)
    d.text((x + 32, y + h - 21), "PL", font=F(SANS_B, 7), fill=RED)


def scene_hormuz(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(170, 205, 225))
    # strait banks
    d.polygon([(x, y + h * 0.55), (x + w * 0.42, y + h * 0.55),
               (x + w * 0.42, y + h), (x, y + h)], fill=(190, 175, 130))
    d.polygon([(x + w, y + h * 0.45), (x + w * 0.62, y + h * 0.45),
               (x + w * 0.62, y + h), (x + w, y + h)], fill=(190, 175, 130))
    # tankers in the strait
    for tx, ty, tc in [(x + w * 0.44, y + h * 0.58, RED),
                       (x + w * 0.46, y + h * 0.72, (60, 60, 60))]:
        d.rectangle([tx, ty, tx + 34, ty + 10], fill=tc)
        d.rectangle([tx + 22, ty - 8, tx + 30, ty], fill=tc)
    # blockade ship
    d.polygon([(x + 8, y + h * 0.62), (x + 44, y + h * 0.62),
               (x + 40, y + h * 0.72), (x + 12, y + h * 0.72)], fill=NAVY)
    d.rectangle([x + 22, y + h * 0.52, x + 26, y + h * 0.62], fill=NAVY)
    d.text((x + 6, y + 4), "HORMUZ", font=F(SANS_B, 7), fill=NAVY)
    d.text((x + 6, y + 15), "BLOCKADE", font=F(SANS_B, 7), fill=RED)


def scene_gaza(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 205, 170))
    # ruined buildings
    d.polygon([(x + 6, y + h), (x + 6, y + h * 0.45), (x + 22, y + h * 0.38),
               (x + 30, y + h * 0.55), (x + 30, y + h)], fill=(120, 105, 85))
    d.polygon([(x + 36, y + h), (x + 36, y + h * 0.55), (x + 52, y + h * 0.5),
               (x + 60, y + h * 0.68), (x + 60, y + h)], fill=(100, 88, 70))
    d.rectangle([x + 66, y + h * 0.6, x + w - 6, y + h], fill=(140, 125, 100))
    # smoke
    for cx, cy, r in [(x + 16, y + 18, 7), (x + 26, y + 12, 9), (x + 44, y + 22, 7)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(150, 150, 150))
    # aid truck
    d.rectangle([x + w - 46, y + h - 24, x + w - 8, y + h - 10], fill=WHITE,
                outline=INK)
    d.text((x + w - 44, y + h - 22), "AID", font=F(SANS_B, 8), fill=RED)
    d.ellipse([x + w - 40, y + h - 10, x + w - 34, y + h - 4], fill=INK)
    d.ellipse([x + w - 18, y + h - 10, x + w - 12, y + h - 4], fill=INK)
    d.rectangle([x + 4, y + 4, x + 74, y + 16], fill=RED)
    d.text((x + 7, y + 5), "3 KILLED", font=F(SANS_B, 8), fill=WHITE)


def scene_court(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(225, 220, 205))
    # courthouse
    d.polygon([(x + w * 0.2, y + 12), (x + w * 0.5, y + 2), (x + w * 0.8, y + 12)],
              fill=NAVY)
    for i in range(4):
        cx = x + w * (0.25 + i * 0.17)
        d.rectangle([cx - 4, y + 14, cx + 4, y + h - 26], fill=WHITE, outline=NAVY)
    d.rectangle([x + w * 0.15, y + h - 26, x + w * 0.85, y + h - 20], fill=NAVY)
    # gavel
    d.line([x + w - 30, y + h - 34, x + w - 12, y + h - 16], fill=(120, 80, 40),
           width=4)
    d.rectangle([x + w - 34, y + h - 40, x + w - 18, y + h - 30], fill=(120, 80, 40))
    d.text((x + 6, y + 4), "2nd CIRCUIT", font=F(SANS_B, 8), fill=NAVY)
    d.text((x + 6, y + 15), "34 COUNTS", font=F(SANS_B, 8), fill=RED)


def scene_cricket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(150, 200, 130))
    d.rectangle([x + w * 0.3, y + 8, x + w * 0.7, y + h - 8], fill=(205, 180, 120))
    # stumps + batsman
    d.line([x + w * 0.5, y + h - 30, x + w * 0.5, y + h - 44], fill=(240, 220, 120),
           width=3)
    d.ellipse([x + w * 0.38, y + h * 0.42, x + w * 0.46, y + h * 0.52],
              fill=(200, 150, 100))
    d.line([x + w * 0.42, y + h * 0.52, x + w * 0.42, y + h * 0.72],
           fill=(30, 60, 120), width=5)
    d.line([x + w * 0.42, y + h * 0.72, x + w * 0.36, y + h - 8], fill=INK, width=3)
    d.line([x + w * 0.42, y + h * 0.72, x + w * 0.48, y + h - 8], fill=INK, width=3)
    d.line([x + w * 0.44, y + h * 0.55, x + w * 0.58, y + h * 0.68],
           fill=(200, 170, 110), width=3)
    # scoreboard
    d.rectangle([x + 4, y + 4, x + w - 4, y + 20], fill=NAVY)
    d.text((x + w // 2, y + 6), "720/9  DRAW", font=F(SANS_B, 8), fill=WHITE,
           anchor="ma")


def scene_football(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(90, 160, 90))
    d.rectangle([x, y + h * 0.55, x + w, y + h], fill=(60, 130, 60))
    # stands
    d.rectangle([x, y, x + w, y + h * 0.3], fill=(200, 60, 60))
    for i in range(12):
        d.ellipse([x + 6 + i * (w - 12) // 12, y + 6, x + 12 + i * (w - 12) // 12,
                   y + 12], fill=WHITE)
    # scoreboard
    d.rectangle([x + 4, y + h * 0.32, x + w - 4, y + h * 0.52], fill=NAVY)
    d.text((x + w // 2, y + h * 0.35), "LIV 4-0 MUN", font=F(SANS_B, 8),
           fill=WHITE, anchor="ma")
    # ball
    bx, by = x + w * 0.5, y + h * 0.72
    d.ellipse([bx - 9, by - 9, bx + 9, by + 9], fill=WHITE, outline=INK)
    d.polygon([(bx, by - 4), (bx + 4, by), (bx, by + 4), (bx - 4, by)],
              fill=INK)


def scene_chess(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(235, 220, 190))
    sq = min(w, h) // 8
    ox, oy = x + (w - sq * 8) // 2, y + (h - sq * 8) // 2
    for r in range(8):
        for c in range(8):
            if (r + c) % 2 == 0:
                d.rectangle([ox + c * sq, oy + r * sq, ox + (c + 1) * sq,
                             oy + (r + 1) * sq], fill=(120, 90, 60))
    # king + queen pieces
    for px, py, col in [(ox + 3 * sq, oy + 6 * sq, WHITE),
                        (ox + 4 * sq, oy + 1 * sq, INK)]:
        d.ellipse([px, py, px + sq, py + sq], fill=col, outline=INK)
        d.rectangle([px + sq * 0.2, py - 4, px + sq * 0.8, py + 2], fill=col,
                    outline=INK)
    d.rectangle([x + 4, y + 4, x + 56, y + 18], fill=NAVY)
    d.text((x + 7, y + 5), "GAME 1", font=F(SANS_B, 8), fill=WHITE)


def scene_markets(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(20, 40, 70))
    # bars
    vals = [0.25, 0.2, 0.3, 0.22, 0.45, 0.55, 0.75, 0.95]
    bw = w / len(vals)
    for i, v in enumerate(vals):
        bh = v * (h - 38)
        d.rectangle([x + i * bw + 2, y + h - 8 - bh, x + (i + 1) * bw - 2, y + h - 8],
                    fill=(60, 140, 220) if i < 6 else (80, 200, 100))
    d.text((x + 6, y + 4), "DOW +1,448", font=F(SANS_B, 10), fill=WHITE)
    d.text((x + 6, y + 17), "NASDAQ +6.5%", font=F(SANS_B, 10), fill=(120, 220, 140))


def scene_fifa(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(200, 225, 200))
    # trophy
    tx, ty = x + w * 0.5, y + h * 0.45
    d.polygon([(tx - 12, ty - 16), (tx + 12, ty - 16), (tx + 6, ty + 2),
               (tx - 6, ty + 2)], fill=GOLD, outline=(120, 90, 0))
    d.rectangle([tx - 8, ty + 2, tx + 8, ty + 10], fill=GOLD, outline=(120, 90, 0))
    d.rectangle([tx - 14, ty + 10, tx + 14, ty + 16], fill=GOLD,
                outline=(120, 90, 0))
    # flags row
    flags = [(RED, WHITE, BLUE), (GREEN, WHITE, RED), (BLUE, (255, 210, 0), RED),
             (NAVY, WHITE, RED)]
    fw = (w - 16) // 4
    for i, (c1, c2, c3) in enumerate(flags):
        fx = x + 8 + i * fw
        d.rectangle([fx, y + h - 22, fx + fw - 3, y + h - 15], fill=c1)
        d.rectangle([fx, y + h - 15, fx + fw - 3, y + h - 8], fill=c2)
    d.text((x + 6, y + 4), "2031 · 2035", font=F(SANS_B, 10), fill=NAVY)
    d.text((x + 6, y + 17), "48 TEAMS", font=F(SANS_B, 8), fill=RED)


def scene_denmark(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(190, 210, 230))
    # row houses
    cols = [RED, (220, 180, 60), (60, 120, 180), (200, 90, 90)]
    hw = (w - 12) // 4
    for i, c in enumerate(cols):
        hx = x + 6 + i * hw
        d.rectangle([hx, y + h * 0.4, hx + hw - 3, y + h - 10], fill=c)
        d.polygon([(hx, y + h * 0.4), (hx + (hw - 3) // 2, y + h * 0.28),
                   (hx + hw - 3, y + h * 0.4)], fill=(90, 60, 40))
        d.rectangle([hx + hw // 2 - 3, y + h - 26, hx + hw // 2 + 3, y + h - 10],
                    fill=INK)
    # danish flag (hero only; the mini scene keeps the "91 LEASES" tag)
    if w >= 120:
        d.rectangle([x + w - 30, y + 4, x + w - 6, y + 20], fill=RED)
        d.rectangle([x + w - 24, y + 4, x + w - 22, y + 20], fill=WHITE)
        d.rectangle([x + w - 30, y + 10, x + w - 6, y + 12], fill=WHITE)
    d.text((x + 6, y + 4), "91 LEASES", font=F(SANS_B, 8), fill=NAVY)


def scene_border(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(205, 225, 235))
    # mountains
    d.polygon([(x, y + h), (x + w * 0.3, y + 12), (x + w * 0.55, y + h)],
              fill=(120, 140, 160))
    d.polygon([(x + w * 0.4, y + h), (x + w * 0.7, y + 6), (x + w, y + h)],
              fill=(90, 110, 135))
    d.polygon([(x + w * 0.3 - 8, y + 12), (x + w * 0.3 + 8, y + 12),
               (x + w * 0.3, y + 26)], fill=WHITE)
    # table with two flags
    d.rectangle([x + w * 0.25, y + h - 30, x + w * 0.75, y + h - 24], fill=(120, 80, 40))
    d.line([x + w * 0.3, y + h - 24, x + w * 0.3, y + h - 8], fill=(120, 80, 40),
           width=2)
    d.line([x + w * 0.7, y + h - 24, x + w * 0.7, y + h - 8], fill=(120, 80, 40),
           width=2)
    # india flag
    d.rectangle([x + w * 0.3, y + h - 52, x + w * 0.46, y + h - 30], fill=WHITE,
                outline=INK)
    d.rectangle([x + w * 0.3, y + h - 52, x + w * 0.46, y + h - 45], fill=(255, 153, 51))
    d.rectangle([x + w * 0.3, y + h - 37, x + w * 0.46, y + h - 30], fill=(19, 136, 8))
    # china flag
    d.rectangle([x + w * 0.54, y + h - 52, x + w * 0.7, y + h - 30], fill=RED,
                outline=INK)
    d.text((x + w * 0.56, y + h - 50), "★", font=F(SANS_B, 8), fill=(255, 222, 0))
    d.text((x + 6, y + 4), "ARUNACHAL", font=F(SANS_B, 8), fill=NAVY)


def scene_leaks(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(225, 215, 195))
    # sealed files
    for i, fx in enumerate([x + 8, x + w * 0.4]):
        d.rectangle([fx, y + 22, fx + w * 0.28, y + h - 12], fill=WHITE, outline=INK)
        d.line([fx + 4, y + 30, fx + w * 0.28 - 4, y + 30], fill=GREY)
        d.line([fx + 4, y + 38, fx + w * 0.28 - 4, y + 38], fill=GREY)
        d.line([fx + 4, y + 46, fx + w * 0.28 - 8, y + 46], fill=GREY)
        d.ellipse([fx + w * 0.1, y + 54, fx + w * 0.18, y + 62], fill=RED)
    # stamp
    d.rectangle([x + w - 52, y + 6, x + w - 4, y + 22], outline=RED, width=2)
    d.text((x + w - 49, y + 8), "SECRET", font=F(SANS_B, 8), fill=RED)
    # gavel
    d.line([x + w * 0.55, y + h - 22, x + w * 0.75, y + h - 6], fill=(120, 80, 40),
           width=3)
    d.rectangle([x + w * 0.5, y + h - 28, x + w * 0.62, y + h - 18], fill=(120, 80, 40))


def scene_smog(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(200, 190, 160))
    # hazy skyline
    for i, (bx, bw, bh) in enumerate([(0, 18, 40), (20, 14, 55), (38, 20, 35),
                                      (62, 16, 50), (82, 22, 42)]):
        d.rectangle([x + bx, y + h - 10 - bh, x + bx + bw, y + h - 10],
                    fill=(140, 130, 110))
    d.rectangle([x, y + h - 10, x + w, y + h], fill=(110, 100, 85))
    # AQI gauge
    gx, gy = x + w - 44, y + 6
    d.rectangle([gx, gy, gx + 38, gy + 18], fill=RED)
    d.text((gx + 3, gy + 2), "500+", font=F(SANS_B, 9), fill=WHITE)
    # mask
    d.ellipse([x + w * 0.3, y + h * 0.55, x + w * 0.7, y + h * 0.8], fill=WHITE,
              outline=INK)
    d.line([x + w * 0.3, y + h * 0.62, x + w * 0.18, y + h * 0.5], fill=INK, width=2)
    d.line([x + w * 0.7, y + h * 0.62, x + w * 0.82, y + h * 0.5], fill=INK, width=2)
    d.text((x + 6, y + 4), "LAHORE", font=F(SANS_B, 8), fill=RED)


SCENES = {1: scene_nvidia, 2: scene_korea, 3: scene_nato, 4: scene_hormuz,
          5: scene_gaza, 6: scene_court, 7: scene_cricket, 8: scene_football,
          9: scene_chess, 10: scene_markets, 11: scene_fifa, 12: scene_denmark,
          13: scene_border, 14: scene_leaks, 15: scene_smog}

FEATURES = [
    (1, "US", "TECH", "Nvidia brings back Jensen Huang; shares soar 31%",
     "Board reinstates its co-founder 11 days after he quit; the stock adds "
     "~$952bn, the biggest one-day gain ever.", "CONFIRMED · REUTERS", "Americas"),
    (2, "ASIA", "SECURITY", "Seoul sounds island air alert as jets near Ulleung",
     "Alert at 07:52, lifted in minutes; jets entered the defence zone, "
     "the military says.", "REPORTED · REUTERS", "Asia"),
    (3, "EUROPE", "NATO", "NATO to send AWACS to Poland after missile landings",
     "Early-warning jets join the eastern flank after three Russian Kh-101 "
     "missiles came down on Friday.", "CONFIRMED · REUTERS", "Europe"),
    (4, "MIDDLE EAST", "IRAN WAR", "Iran vows 'all its tools' on US blockade",
     "Tehran: an act of war. Trump dares Iran to test Hormuz.",
     "CONFIRMED · REUTERS", "Mideast"),
    (5, "MIDDLE EAST", "GAZA", "Israeli strikes kill 3 in Gaza; land 'poisoned'",
     "UNRWA worker dead; report: Gaza's soil toxic for decades.",
     "CONFIRMED · REUTERS", "Mideast"),
    (6, "US", "COURTS", "Appeals court gives Trump path to erase case",
     "2nd Circuit revives bid to move the case to federal court.",
     "CONFIRMED · AP", "Americas"),
    (7, "OCEANIA", "CRICKET", "India–New Zealand Test ends in a draw",
     "Level after India's 720/9; NZ fight back on the final day.",
     "CONFIRMED · SPORTSTAR", "Oceania"),
    (8, "EUROPE", "FOOTBALL", "Liverpool thrash 10-man Man Utd 4–0",
     "Pochettino loses his first match; four different scorers.",
     "CONFIRMED · BBC", "Europe"),
    (9, "EUROPE", "CHESS", "Gukesh–Sindarov title match begins",
     "Game 1 at 15:00 CET; the youngest pairing in title history.",
     "CONFIRMED · CHESS.COM", "Europe"),
    (10, "GLOBAL", "MARKETS", "Wall Street roars back: Dow +1,448",
     "Nasdaq +6.5%, best since April 2025; gold up, Bitcoin $61k.",
     "CONFIRMED · IBD", "Global"),
    (11, "GLOBAL", "FOOTBALL", "FIFA names 2031 and 2035 Cup hosts",
     "US-led bid takes 2031; UK 2035, the first 48-team editions.",
     "CONFIRMED · FIFA", "Global"),
    (12, "EUROPE", "LAW", "Denmark court backs 'ghetto law' evictions",
     "Ending 91 leases was not discrimination; hard line upheld.",
     "CONFIRMED · REUTERS", "Europe"),
    (13, "ASIA", "DIPLOMACY", "India and China hold border talks",
     "Commanders meet in Arunachal to ease frontier tensions.",
     "CONFIRMED · TOI", "Asia"),
    (14, "ASIA", "ESPIONAGE", "China sentences official to death for leaks",
     "100 reports leaked, 35 state secrets, the court finds.",
     "CONFIRMED · TOI", "Asia"),
    (15, "ASIA", "POLLUTION", "Lahore tops world pollution ranking",
     "AQI tops 500; eight Pakistan cities among the world's worst.",
     "REPORTED · TOI", "Asia"),
]

ALSO_ON = [
    "Poland: Russian drone briefly violates airspace",
    "Germany: Bundeswehr to use Kyiv's Delta tool",
    "Germany: hundreds of schools hit by hoax bomb threats",
    "Russia: Murmansk governor held over graft",
    "France: condemns Polish airspace violation",
    "Estonia: PM denies Trump urged end to Ukraine aid",
    "Belgium: transport hit by nationwide union protest",
    "UK: King Charles reached out to Meghan",
    "Netherlands: activist, 28, dies by euthanasia",
    "Iran: singer flogged 74 times with her team",
    "US: sanctions dozens over Iran shadow banking",
    "Israel: 23 suicides in forces in 2026, most in 16 yrs",
    "Iraq: driver held over digging near oil pipeline",
    "Gaza: Hamas seeks prompt talks after aid deaths",
    "US: Trump pauses Army's Iowa chemical detonation",
    "US: O'Hare briefly grounds flights in rush",
    "El Salvador: Bukele seeks a third term",
    "Haiti: 3 Salvadoran soldiers die in blast",
    "Chile: peso weakest in 4+ years as copper slides",
    "Argentina: risk premium tops 1,000bp",
    "Colombia: man hit by firebomb in protests",
    "India: SC grants bail to Godhra convict",
    "Pakistan: 4.0 quake near Afghan border",
    "Bangladesh: Grameen Bank branches targeted",
    "North Korea: Kim receives India's new envoy",
    "India: journalist 'stopped at Delhi airport'",
    "Japan: police warned over probe data on AI search",
    "South Korea: SK hynix surges after Huang return",
    "India: East Bengal face decisive ACL2 test",
    "Libya: UN demands probe into Benghazi attacks",
    "South Sudan: at least 24 civilians killed",
    "DR Congo: Ebola tops 11,000 cases, toll 5,358",
    "Kenya: joins Africa CDC board for two years",
    "Nigeria: 24 dead as boat of mourners capsizes",
    "Ghana: beat Morocco 1–0 to win amputee cup",
]

DATE_CHECK = [
    "COP31 collapse, no deal (22 Nov)",
    "Merkury corvette sunk off Benghazi (22 Nov)",
    "Democrats clinch 258 House seats (23 Nov)",
    "Indonesia factory fire kills 24 (23 Nov)",
    "Verstappen wins Las Vegas GP (22 Nov)",
    "Alcaraz wins maiden ATP Finals (22 Nov)",
    "India 720/9, record Test total in NZ (23 Nov)",
    "Korea minister quits over AI exam scandal (23 Nov)",
    "Bitcoin retakes $60,000 (22–23 Nov)",
    "Mexico arrests 'Chapo Isidro' (21 Nov)",
]

TIMELINE = [  # (ruler hour, label, above?)
    (0, "22:52 Seoul: Ulleung alert", True),
    (4, "04:00 Arunachal talks", False),
    (9, "09:00 'ghetto law' upheld", False),
    (14, "14:00 Gukesh–Sindarov G1", True),
    (20, "19:46 FIFA: 2031/2035 hosts", False),
    (21, "21:00 Dow +1,448", True),
]

PINS = [  # (number, lon, lat, region) — nudged so no two pins collide
    (1, -122.0, 37.4, "Americas"), (2, 130.9, 37.5, "Asia"),
    (3, 26.0, 55.0, "Europe"), (4, 56.5, 26.6, "Mideast"),
    (5, 34.5, 31.5, "Mideast"), (6, -80.0, 44.0, "Americas"),
    (7, 170.0, -41.0, "Oceania"), (8, -8.0, 55.0, "Europe"),
    (9, 0.0, 42.0, "Europe"), (10, -68.0, 38.0, "Americas"),
    (11, 12.0, 49.0, "Europe"), (12, 18.0, 59.0, "Europe"),
    (13, 94.0, 28.0, "Asia"), (14, 116.4, 39.9, "Asia"),
    (15, 74.3, 31.5, "Asia"),
]

CONTINENTS = {
    "NA": [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-80, 73),
           (-65, 60), (-55, 47), (-70, 42), (-80, 32), (-90, 21), (-97, 16),
           (-105, 20), (-117, 33), (-125, 40), (-125, 49), (-140, 60),
           (-155, 58), (-168, 66)],
    "SA": [(-80, 10), (-60, 10), (-50, 0), (-40, -5), (-35, -10), (-40, -20),
           (-48, -28), (-58, -35), (-65, -41), (-70, -52), (-73, -50),
           (-70, -30), (-80, -15), (-80, 5)],
    "EU": [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (10, 59),
           (18, 56), (21, 55), (24, 58), (28, 60), (30, 70), (40, 68), (45, 65),
           (40, 55), (35, 50), (28, 45), (23, 40), (19, 42), (12, 44), (3, 43),
           (-2, 37), (-10, 36)],
    "AF": [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (30, 31),
           (35, 28), (43, 12), (51, 11), (48, 0), (40, -10), (35, -20),
           (32, -29), (20, -35), (15, -30), (12, -18), (9, -1), (9, 4),
           (-8, 5), (-17, 15)],
    "AS": [(40, 68), (50, 70), (60, 70), (70, 72), (80, 73), (90, 75),
           (110, 76), (130, 72), (150, 70), (170, 67), (178, 65), (170, 60),
           (162, 56), (158, 52), (150, 60), (142, 55), (140, 45), (135, 35),
           (130, 33), (127, 35), (122, 40), (120, 30), (110, 20), (105, 10),
           (100, 8), (95, 15), (90, 22), (85, 20), (80, 8), (75, 10), (70, 22),
           (60, 25), (55, 26), (50, 29), (48, 30), (43, 35), (40, 40),
           (38, 45), (35, 50), (40, 55), (45, 60), (40, 68)],
    "OC": [(113, -22), (114, -30), (115, -35), (125, -32), (130, -32),
           (135, -35), (140, -38), (145, -38), (150, -37), (153, -27),
           (150, -22), (146, -19), (142, -15), (142, -11), (136, -12),
           (132, -11), (126, -14), (122, -17), (118, -20), (113, -22)],
}


def render_scene(n, w, h):
    """Draw one scene onto its own canvas so nothing can spill past its box."""
    im = Image.new("RGB", (w, h), (255, 255, 255))
    dd = ImageDraw.Draw(im)
    SCENES[n](dd, 0, 0, w, h)
    return im


def draw():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)

    # ---- masthead
    d.rectangle([0, 0, W, 124], fill=NAVY)
    d.rectangle([0, 121, W, 124], fill=GOLD)
    d.text((16, 12), "THE DAY IN WORLD NEWS", font=F(SANS_B, 13), fill=GOLD_L)
    d.text((W - 16, 12), "TUESDAY · 24 NOVEMBER 2026", font=F(SANS_B, 11),
           fill=(200, 205, 220), anchor="ra")
    d.text((16, 32), "Tuesday 24 November 2026", font=F(SERIF_B, 58), fill=WHITE)
    d.text((16, 102), "50 STORIES  ·  7 REGIONS  ·  EVERY ONE FROM THIS TUESDAY",
           font=F(SANS_B, 12), fill=GOLD_L)

    # ---- UTC timeline ruler (strip 124-170; labels above / below the line)
    d.rectangle([0, 124, W, 170], fill=PAPER)
    d.line([16, 140, W - 16, 140], fill=NAVY, width=2)
    for hh in (0, 6, 12, 18, 24):
        tx = 16 + hh / 24 * (W - 32)
        d.line([tx, 136, tx, 144], fill=NAVY, width=2)
        anc = "ma"
        if hh == 0:
            anc = "la"
        elif hh == 24:
            anc = "ra"
        d.text((tx, 158), "%02d:00" % hh, font=F(SANS, 8), fill=GREY, anchor=anc)
    for hour, label, above in TIMELINE:
        fx = 16 + hour / 24 * (W - 32)
        fx = min(max(fx, 20), W - 20)
        d.ellipse([fx - 4, 136, fx + 4, 144], fill=RED, outline=WHITE)
        ly = 126 if above else 146
        if fx < 90:
            anc, lx = "la", 20
        elif fx > W - 110:
            anc, lx = "ra", W - 16
        else:
            anc, lx = "ma", fx
        d.text((lx, ly), label, font=F(SANS_B, 8), fill=INK, anchor=anc)
    d.text((W - 16, 126), "TIMES UTC", font=F(SANS_B, 8), fill=GREY, anchor="ra")

    # ---- hero row: features 1-3
    cw, ch, gap, x0, y0 = 328, 204, 8, 8, 172
    for i in range(3):
        n, region, topic, head, deck, label, reg = FEATURES[i]
        x = x0 + i * (cw + gap)
        d.rectangle([x, y0, x + cw, y0 + ch], fill=WHITE, outline=LINE)
        img.paste(render_scene(n, cw - 2, 102), (x + 1, y0 + 1))
        d.text((x + 10, y0 + 108), "%d  %s · %s" % (n, region, topic),
               font=F(SANS_B, 10), fill=REGION_COLOR[reg])
        text_lines(d, x + 10, y0 + 122, head, F(SANS_B, 14), cw - 20, INK,
                   leading=16)
        text_lines(d, x + 10, y0 + 156, deck, F(SANS, 10), cw - 20, GREY,
                   leading=12)
        d.text((x + 10, y0 + 188), label, font=F(SANS_B, 8),
               fill=REGION_COLOR[reg])

    # ---- grid rows: features 4-15
    gw, gh, gx0, gy0 = 247, 88, 8, 380
    for i in range(4, 16):
        n, region, topic, head, deck, label, reg = FEATURES[i - 1]
        r, c = divmod(i - 4, 4)
        x = gx0 + c * (gw + gap)
        y = gy0 + r * (gh + 4)
        d.rectangle([x, y, x + gw, y + gh], fill=WHITE, outline=LINE)
        img.paste(render_scene(n, 82, gh - 2), (x + 1, y + 1))
        tx = x + 90
        d.text((tx, y + 4), "%d  %s · %s" % (n, region, topic),
               font=F(SANS_B, 8), fill=REGION_COLOR[reg])
        text_lines(d, tx, y + 15, head, F(SANS_B, 11), gw - 98, INK, leading=13)
        text_lines(d, tx, y + 43, deck, F(SANS, 9), gw - 98, GREY, leading=11)
        d.text((tx, y + 76), label, font=F(SANS_B, 7), fill=REGION_COLOR[reg])

    # ---- world map
    d.text((8, 656), "WHERE IT HAPPENED", font=F(SANS_B, 11), fill=NAVY)
    d.line([150, 663, W - 8, 663], fill=LINE, width=1)
    mx0, my0, mw, mh = 8, 672, W - 16, 108
    d.rectangle([mx0, my0, mx0 + mw, my0 + mh], fill=SEA, outline=LINE)

    def proj(lon, lat):
        px = mx0 + (lon + 180) / 360 * mw
        py = my0 + (90 - lat) / 150 * mh
        return (px, py)

    for poly in CONTINENTS.values():
        d.polygon([proj(lo, la) for lo, la in poly], fill=LAND, outline=LAND_L)
    for num, lon, lat, reg in PINS:
        px, py = proj(lon, lat)
        col = REGION_COLOR[reg]
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=col, outline=WHITE)
        d.text((px, py - 5), str(num), font=F(SANS_B, 8), fill=WHITE, anchor="ma")
    # legend
    lx = mx0 + 8
    ly = my0 + mh - 16
    d.rectangle([lx - 4, ly - 3, mx0 + 560, ly + 11], fill=(255, 255, 255, 200))
    for name in ["Americas", "Europe", "Mideast", "Africa", "Asia", "Oceania",
                 "Global"]:
        d.ellipse([lx, ly, lx + 8, ly + 8], fill=REGION_COLOR[name])
        d.text((lx + 11, ly - 1), name, font=F(SANS, 8), fill=INK)
        lx += 11 + d.textlength(name, font=F(SANS, 8)) + 12

    # ---- also on
    d.text((8, 784), "ALSO ON 24 NOVEMBER", font=F(SANS_B, 11), fill=NAVY)
    d.line([168, 791, W - 8, 791], fill=LINE, width=1)
    colw = 328
    for idx, item in enumerate(ALSO_ON):
        col, row = divmod(idx, 12)
        x = 8 + col * (colw + 8)
        y = 800 + row * 11
        num = 16 + idx
        d.text((x, y), "%d." % num, font=F(SANS_B, 9), fill=RED)
        d.text((x + 24, y), item, font=F(SANS, 9), fill=INK)

    # ---- date check box (3 columns x 4 rows; the 11th slot is "Not yet")
    d.rectangle([8, 936, W - 8, 996], outline=RED, width=1, fill=(252, 238, 232))
    d.text((16, 940), "DATE CHECK — LEFT OUT AS OLDER NEWS",
           font=F(SANS_B, 10), fill=RED)
    dc_items = DATE_CHECK + ["Not yet: Gukesh–Sindarov Game 2, Wed 25 Nov"]
    for i, item in enumerate(dc_items):
        col, row = divmod(i, 4)
        x = 16 + col * 334
        y = 956 + row * 10
        if i == len(dc_items) - 1:
            d.text((x, y), item, font=F(SANS_B, 8), fill=RED)
        else:
            d.text((x, y), "✕ " + item, font=F(SANS, 8), fill=(90, 60, 55))

    # ---- footer
    d.text((8, 998),
           "Every story was reported on 24 November 2026; disputed claims are attributed.",
           font=F(SANS, 9), fill=GREY)
    d.text((8, 1010),
           "Sources: AP, Reuters, AFP, BBC, Al Jazeera, UN News. Original drawings.",
           font=F(SANS, 9), fill=GREY)

    out = os.path.join(BASE, "entry.png")
    img.save(out, "PNG")
    print("wrote", out, img.size)


if __name__ == "__main__":
    draw()
