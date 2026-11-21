#!/usr/bin/env python3
"""Render the 21 November 2026 world-news front page as entry.png.

Everything is drawn procedurally with PIL: a newspaper front page with a
masthead naming the day, six illustrated story panels and a ticker strip
carrying the remaining stories of the day. No external assets.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 242, 231)
INK = (27, 42, 74)
RED = (179, 39, 30)
BLUE = (38, 84, 124)
GOLD = (201, 141, 38)
TEAL = (31, 110, 102)
GREY = (96, 96, 92)
LIGHT = (232, 224, 205)
WHITE = (255, 255, 255)
DARKRED = (139, 26, 22)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANSB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def center(draw, y, text, fnt, fill, x0=0, x1=W):
    w = draw.textlength(text, font=fnt)
    draw.text(((x0 + x1 - w) / 2, y), text, font=fnt, fill=fill)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_cyclone(draw, cx, cy, r, ink=INK):
    """Spiral storm bands with a calm eye."""
    for k in range(5):
        a0 = k * 1.25
        a1 = a0 + 4.6
        steps = 60
        pts = []
        for i in range(steps + 1):
            a = a0 + (a1 - a0) * i / steps
            rr = 8 + (r - 8) * i / steps
            pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
        draw.line(pts, fill=ink, width=7 - k)
    draw.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=PAPER, outline=ink, width=3)
    # rain slashes under the storm
    for i, dx in enumerate((-42, -14, 14, 42)):
        x = cx + dx
        draw.line([(x, cy + r - 6), (x - 8, cy + r + 26)], fill=BLUE, width=4)


def draw_scales(draw, cx, cy, s):
    """Balance scales of justice on a plinth."""
    draw.line([(cx, cy - s), (cx, cy + s)], fill=INK, width=6)
    draw.line([(cx - s, cy - s + 12), (cx + s, cy - s + 12)], fill=INK, width=5)
    for side in (-1, 1):
        px = cx + side * s
        draw.line([(px, cy - s + 12), (px, cy - 8)], fill=INK, width=3)
        draw.arc([px - 22, cy - 14, px + 22, cy + 26], 0, 180, fill=INK, width=4)
    draw.line([(cx - s - 6, cy + s), (cx + s + 6, cy + s)], fill=INK, width=6)
    draw.ellipse([cx - 10, cy - s - 10, cx + 10, cy - s + 10], fill=GOLD, outline=INK, width=3)


def draw_summit(draw, x0, y0, x1, y1):
    """Three leaders seated at a round table with three flags."""
    table_y = y1 - 34
    draw.ellipse([x0 + 30, table_y, x1 - 30, table_y + 26], fill=TEAL, outline=INK, width=3)
    draw.rectangle([x0 + 60, table_y + 22, x1 - 60, table_y + 30], fill=INK)
    colors = [RED, GOLD, BLUE]
    n = 3
    for i, c in enumerate(colors):
        cx = x0 + 18 + (x1 - x0 - 36) * (i + 0.5) / n
        # small flag on a short pole on the left of each figure
        fx = cx - 26
        draw.line([(fx, y0 + 2), (fx, y0 + 28)], fill=INK, width=2)
        draw.polygon([(fx, y0 + 2), (fx - 16, y0 + 7), (fx, y0 + 12)], fill=c, outline=INK)
        # seated figure: head + shoulders
        draw.ellipse([cx - 16, y0 + 26, cx + 16, y0 + 58], fill=(233, 196, 168), outline=INK, width=3)
        draw.pieslice([cx - 26, y0 + 54, cx + 26, y0 + 112], 180, 360, fill=c, outline=INK, width=3)


def draw_bridge(draw, x0, y0, x1, y1):
    """A river bridge under a blast of smoke and sparks."""
    mid_y = y0 + (y1 - y0) * 0.62
    draw.rectangle([x0, mid_y + 26, x1, y1], fill=BLUE)
    # deck and arch
    draw.line([(x0, mid_y), (x1, mid_y)], fill=INK, width=6)
    draw.arc([x0 + 18, mid_y - 34, x1 - 18, mid_y + 34], 180, 360, fill=INK, width=5)
    for fx in (x0 + 34, (x0 + x1) // 2, x1 - 34):
        draw.line([(fx, mid_y - 22), (fx, mid_y)], fill=INK, width=4)
    # explosion burst above the deck
    bx, by = (x0 + x1) // 2, mid_y - 44
    for ang in range(0, 360, 30):
        a = math.radians(ang)
        r = 26 if ang % 60 == 0 else 15
        draw.line([(bx, by), (bx + r * math.cos(a), by + r * math.sin(a))],
                  fill=GOLD, width=5)
    draw.ellipse([bx - 12, by - 12, bx + 12, by + 12], fill=RED, outline=INK, width=3)


def draw_city(draw, x0, y0, x1, y1):
    """Neon Vice City skyline at dusk."""
    draw.rectangle([x0, y0, x1, y1], fill=(43, 24, 68))
    # sun
    sx, sy = (x0 + x1) // 2, y0 + 34
    draw.ellipse([sx - 26, sy - 26, sx + 26, sy + 26], fill=(255, 122, 89), outline=GOLD, width=3)
    buildings = [(0.00, 0.48, 0.28), (0.30, 0.60, 0.22), (0.54, 0.44, 0.20),
                 (0.76, 0.64, 0.24)]
    bw_total = x1 - x0
    for fx, fh, fw in buildings:
        bx, bh, bwid = x0 + fx * bw_total, fh * (y1 - y0), fw * bw_total
        draw.rectangle([bx, y1 - bh, bx + bwid, y1], fill=(24, 14, 44),
                       outline=(255, 90, 180), width=2)
        for wy in range(int(y1 - bh) + 8, y1 - 6, 14):
            for wx in range(int(bx) + 6, int(bx + bwid) - 5, 12):
                draw.rectangle([wx, wy, wx + 4, wy + 6], fill=(255, 214, 90))
    # palm silhouettes
    for px in (x0 + 30, x1 - 34):
        draw.line([(px, y1 - 8), (px, y1 - 46)], fill=(20, 120, 70), width=4)
        for ang in (200, 240, 290, 330):
            a = math.radians(ang)
            draw.line([(px, y1 - 46), (px + 20 * math.cos(a), y1 - 46 + 12 * math.sin(a))],
                      fill=(20, 120, 70), width=3)


def draw_climate(draw, x0, y0, x1, y1):
    """A globe on the table between negotiators, with a leaf."""
    cx, cy = (x0 + x1) // 2, y0 + (y1 - y0) // 2 - 4
    r = 40
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(96, 165, 214), outline=INK, width=3)
    draw.arc([cx - r, cy - r, cx + r, cy + r], 200, 330, fill=TEAL, width=8)
    draw.arc([cx - r, cy - r, cx + r, cy + r], 20, 140, fill=TEAL, width=8)
    draw.ellipse([cx - 14, cy - 8, cx + 6, cy + 12], fill=TEAL)
    # leaf
    lx, ly = x1 - 52, y1 - 44
    draw.pieslice([lx - 18, ly - 26, lx + 18, ly + 10], 180, 360, fill=(46, 139, 63), outline=INK, width=2)
    draw.line([(lx - 14, ly - 4), (lx + 14, ly - 22)], fill=INK, width=2)
    # table line
    draw.line([(x0 + 8, y1 - 18), (x1 - 8, y1 - 18)], fill=INK, width=4)


PANELS = [
    ("CYCLONE AKVAN HITS INDIA'S EAST COAST",
     "Odisha & Andhra Pradesh brace for landfall",
     draw_cyclone, "STORM"),
    ("ICJ: MYANMAR COMMITTED GENOCIDE",
     "First state ever found guilty of genocide by a world court",
     draw_scales, "COURT"),
    ("TRUMP – XI – PUTIN MEET IN SHENZHEN",
     "First-ever trilateral summit talks global security, nuclear arms",
     draw_summit, "SUMMIT"),
    ("RUSSIA STRIKES KYIV BRIDGES",
     "At least 9 killed; Kryvyi Rih hit too — 2 dead, 42 hurt",
     draw_bridge, "WAR"),
    ("GTA VI LAUNCHES — VICE CITY OPENS",
     "After 13 years of waiting, the global rollout begins",
     draw_city, "GAMES"),
    ("COP31 TALKS ENTER FINAL STAGE",
     "Fossil fuels and climate finance on the table in Türkiye",
     draw_climate, "CLIMATE"),
]

TICKER = ("ALSO TODAY  •  EU unlocks nearly €8bn for Ukraine  •  Saudi Arabia intercepts "
          "Houthi missiles  •  JPMorgan, Visa & Mastercard report a vendor cyber incident  •  "
          "Mongolia's president resigns  •  Cricket: India fight back in Wellington, 159/1")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # thin outer frame
    d.rectangle([10, 10, W - 11, H - 11], outline=INK, width=4)
    d.rectangle([18, 18, W - 19, H - 19], outline=INK, width=1)

    # ---- masthead (auto-fit so the title never overflows) ----
    mast_size = 64
    while (mast_size > 40 and
           d.textlength("THE WORLD IN ONE DAY", font=font(SERIF, mast_size)) > W - 110):
        mast_size -= 2
    center(d, 34, "THE WORLD IN ONE DAY", font(SERIF, mast_size), INK)
    d.line([(48, 128), (W - 48, 128)], fill=INK, width=3)
    center(d, 140, "SATURDAY, 21 NOVEMBER 2026", font(SANSB, 40), RED)
    center(d, 192, "One day. Eleven stories. From a cyclone in India to a first-of-its-kind genocide verdict.",
           font(SANS, 22), GREY)
    d.line([(48, 230), (W - 48, 230)], fill=INK, width=3)

    # ---- six panels: 2 columns x 3 rows ----
    gx, gy = 36, 246
    pw, ph = 468, 200
    gapx, gapy = 16, 12
    tag_f = font(SANSB, 20)
    head_f = font(SANSB, 25)
    sub_f = font(SANS, 18)
    for i, (headline, sub, art, tag) in enumerate(PANELS):
        col, row = i % 2, i // 2
        x0 = gx + col * (pw + gapx)
        y0 = gy + row * (ph + gapy)
        x1, y1 = x0 + pw, y0 + ph
        d.rectangle([x0, y0, x1, y1], outline=INK, width=2)
        # tag chip
        tw = d.textlength(tag, font=tag_f) + 18
        d.rectangle([x0, y0, x0 + tw, y0 + 30], fill=RED)
        d.text((x0 + 9, y0 + 4), tag, font=tag_f, fill=WHITE)
        # picture area left, text right
        px0, py0, px1, py1 = x0 + 8, y0 + 38, x0 + 148, y1 - 8
        if art is draw_cyclone:
            draw_cyclone(d, (px0 + px1) // 2, (py0 + py1) // 2 - 6, 52)
        elif art is draw_scales:
            draw_scales(d, (px0 + px1) // 2, (py0 + py1) // 2, 46)
        elif art is draw_summit:
            draw_summit(d, px0, py0 + 6, px1, py1)
        elif art is draw_bridge:
            draw_bridge(d, px0, py0, px1, py1)
        elif art is draw_city:
            draw_city(d, px0, py0, px1, py1)
        elif art is draw_climate:
            draw_climate(d, px0, py0, px1, py1)
        tx = x0 + 158
        text_w = pw - 168
        ly = y0 + 42
        for line in wrap(d, headline, head_f, text_w)[:3]:
            d.text((tx, ly), line, font=head_f, fill=INK)
            ly += 30
        ly += 6
        for line in wrap(d, sub, sub_f, text_w)[:3]:
            d.text((tx, ly), line, font=sub_f, fill=GREY)
            ly += 23

    # ---- ticker strip ----
    ty0 = gy + 3 * ph + 2 * gapy + 12
    d.rectangle([36, ty0, W - 36, ty0 + 76], fill=INK)
    tick_f = font(SANS, 19)
    ly = ty0 + 7
    for line in wrap(d, TICKER, tick_f, W - 76)[:3]:
        d.text((48, ly), line, font=tick_f, fill=WHITE)
        ly += 22

    # ---- footer ----
    center(d, H - 48, "THE WORLD IN ONE DAY  •  SATURDAY 21 NOVEMBER 2026  •  ALL STORIES REPORTED TODAY",
           font(SANSB, 17), GREY)
    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
