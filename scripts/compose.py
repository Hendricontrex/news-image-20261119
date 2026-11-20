#!/usr/bin/env python3
"""Compose the 19 November 2026 world-news front page.

The background (a dark dotted world map, no text) is AI-generated; every
word on the finished image is drawn here with PIL, so the letters stay
crisp and legible even at 300 px across. Layout is a newspaper front page:
a masthead naming the day, then the five biggest stories of Thursday
19 November 2026, each as one numbered card with a headline, one plain
factual subline and its dateline. Nothing here invents news: each story
was checked against UN News, Horizon, the Russell Record daily headlines
and the Foreign Exchanges world roundup for 19 November 2026.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SRC = ROOT / "news-bg.png"
OUT = ROOT / "entry.png"

SIZE = 1024
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

NAVY = (13, 26, 46)
CARD = (16, 36, 62)
GOLD = (212, 175, 105)
WHITE = (245, 246, 248)
MIST = (196, 205, 218)
ACCENTS = [(212, 175, 105), (198, 84, 76), (94, 164, 150), (216, 130, 62), (110, 148, 208)]

STORIES = [
    ("MYANMAR GUILTY OF GENOCIDE",
     "World court rules Myanmar committed genocide against the Rohingya",
     "THE HAGUE"),
    ("TRUMP, XI & PUTIN MEET",
     "Three-way summit in Shenzhen ends with a declaration toward peace",
     "SHENZHEN"),
    ("COP31 TALKS RACE FOR A DEAL",
     "Ministers meet in Antalya to unblock the climate negotiations",
     "ANTALYA"),
    ("HORMUZ CRISIS DEEPENS",
     "IEA warns of the gravest threat yet to global energy security",
     "STRAIT OF HORMUZ"),
    ("ANTHROPIC'S RECORD IPO",
     "AI firm prices shares at $83, valued at about $1.5 trillion",
     "NEW YORK"),
]


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns lines that fit max_w."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def main():
    base = Image.open(SRC).convert("RGB").resize((SIZE, SIZE), Image.LANCZOS)
    # Darken the map so white type reads over it anywhere on the page.
    dim = Image.new("RGB", base.size, (8, 16, 30))
    im = Image.blend(base, dim, 0.45)
    draw = ImageDraw.Draw(im, "RGBA")

    # ---- masthead ----
    f_mast = font(BOLD, 96)
    draw.text((SIZE // 2, 30), "WORLD NEWS", font=f_mast, fill=WHITE, anchor="ma")
    draw.rectangle([48, 138, SIZE - 48, 142], fill=GOLD)
    f_date = font(BOLD, 42)
    draw.text((SIZE // 2, 156), "THURSDAY  •  19 NOVEMBER 2026",
              font=f_date, fill=GOLD, anchor="ma")
    draw.rectangle([48, 216, SIZE - 48, 219], fill=(120, 135, 158))

    # ---- story cards ----
    y = 238
    row_h, gap = 136, 12
    f_num = font(BOLD, 58)
    f_head = font(BOLD, 37)
    f_sub = font(REG, 23)
    for i, (head, sub, tag) in enumerate(STORIES):
        accent = ACCENTS[i]
        draw.rounded_rectangle([48, y, SIZE - 48, y + row_h], radius=10,
                               fill=CARD + (228,))
        draw.rectangle([48, y + 8, 58, y + row_h - 8], fill=accent)
        draw.text((92, y + 36), f"{i + 1:02d}", font=f_num, fill=accent, anchor="lm")
        tx = 196
        lines = wrap(draw, head, f_head, SIZE - 48 - tx - 24)
        ly = y + 16
        for ln in lines[:2]:
            draw.text((tx, ly), ln, font=f_head, fill=WHITE, anchor="la")
            ly += 44
        sublines = wrap(draw, f"{sub}  —  {tag}", f_sub, SIZE - 48 - tx - 24)
        sy = y + 64
        for ln in sublines[:2]:
            draw.text((tx, sy), ln, font=f_sub, fill=MIST, anchor="la")
            sy += 29
        y += row_h + gap

    # ---- footer ----
    f_foot = font(REG, 24)
    draw.text((SIZE // 2, 982), "THE DAY IN FIVE STORIES  •  19 NOVEMBER 2026",
              font=f_foot, fill=MIST, anchor="ma")

    im.save(OUT, "PNG", optimize=True)
    print("saved", OUT, im.size, OUT.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
