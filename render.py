#!/usr/bin/env python3
"""Render the 18 November 2026 world-news infographic (1024x1024 PNG).

Built for the make.fun bounty "Sum up 18 November's world news in one
image" (news-image-20261118). The image is drawn programmatically with
Pillow so every word is crisp, legible text -- no AI-generated garbling.

Run:  python3 render.py            (writes entry.png next to this file)
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

PAPER = (250, 246, 239)   # warm off-white
NAVY = (20, 33, 61)       # masthead
GOLD = (252, 163, 17)     # masthead accent
INK = (26, 26, 26)        # headline text
GREY = (74, 74, 74)       # summary text
CARD = (255, 255, 255)    # panel background
LINE = (214, 210, 202)    # panel border

# (tag, accent colour, icon, headline, summary)
STORIES = [
    ("ASIA-PACIFIC", (29, 53, 87), "globe",
     "Trump and Modi meet in Manila as Quad leaders gather",
     "Trump arrives in Manila for Quad talks with Modi and "
     "allies, ahead of a China visit."),
    ("EUROPE", (188, 108, 37), "bridge",
     "Ukraine hits Crimea bridge again as Russia strikes Kyiv bridges",
     "Ukraine hits the Crimean bridge for a second day; "
     "Russia strikes bridges in Kyiv."),
    ("MIDDLE EAST", (157, 2, 8), "radar",
     "Iran drones strike US radar base in Bahrain",
     "Iran's Revolutionary Guard claims a drone attack on a US military "
     "radar system at Bahrain's Sheikh Isa Air Base."),
    ("ASIA", (0, 119, 182), "shield",
     "Taiwan awaits decision on $14bn US arms sale",
     "Taiwan says it urgently needs a $14 billion US arms package, "
     "with the deal now up to President Trump."),
    ("TRADE", (42, 157, 143), "bars",
     "Canada and China extend trade deals before APEC",
     "Canada and China extend trade cooperation as Xi Jinping meets "
     "Mark Carney ahead of the APEC summit."),
    ("HEALTH", (106, 153, 78), "cross",
     "US loses its measles-free status",
     "The United States loses its measles-free status as cases "
     "and deaths mount, health officials confirm."),
]


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap measured with the real font."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def icon_globe(d, x, y, s, c):
    d.ellipse([x, y, x + s, y + s], outline=c, width=4)
    d.ellipse([x + s * 0.28, y, x + s * 0.72, y + s], outline=c, width=3)
    d.line([x, y + s / 2, x + s, y + s / 2], fill=c, width=3)
    d.arc([x, y + s * 0.18, x + s, y + s * 0.82], 200, 340, fill=c, width=3)


def icon_bridge(d, x, y, s, c):
    d.line([x, y + s * 0.72, x + s, y + s * 0.72], fill=c, width=5)
    d.line([x + s * 0.18, y + s * 0.15, x + s * 0.18, y + s * 0.72],
           fill=c, width=5)
    d.line([x + s * 0.82, y + s * 0.15, x + s * 0.82, y + s * 0.72],
           fill=c, width=5)
    d.arc([x + s * 0.18, y + s * 0.30, x + s * 0.82, y + s * 0.95],
          180, 360, fill=c, width=4)


def icon_radar(d, x, y, s, c):
    cx, cy = x + s / 2, y + s / 2
    for r in (s * 0.48, s * 0.32, s * 0.16):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=c, width=3)
    d.pieslice([cx - s * 0.48, cy - s * 0.48, cx + s * 0.48, cy + s * 0.48],
               300, 345, fill=c)
    d.ellipse([cx + s * 0.20 - 5, cy - s * 0.18 - 5,
               cx + s * 0.20 + 5, cy - s * 0.18 + 5], fill=c)


def icon_shield(d, x, y, s, c):
    pts = [(x + s * 0.5, y), (x + s * 0.95, y + s * 0.18),
           (x + s * 0.95, y + s * 0.55), (x + s * 0.5, y + s),
           (x + s * 0.05, y + s * 0.55), (x + s * 0.05, y + s * 0.18)]
    d.polygon(pts, outline=c, width=4)
    d.line([x + s * 0.28, y + s * 0.52, x + s * 0.45, y + s * 0.68,
            x + s * 0.74, y + s * 0.34], fill=c, width=5)


def icon_bars(d, x, y, s, c):
    w = s * 0.20
    for i, h in enumerate((0.35, 0.60, 0.90)):
        bx = x + i * s * 0.32
        d.rectangle([bx, y + s - s * h, bx + w, y + s], fill=c)
    # small arrow above the tallest bar
    ax = x + 2 * s * 0.32 + w / 2
    d.polygon([(ax - 7, y + s * 0.06), (ax + 7, y + s * 0.06),
               (ax, y - s * 0.06)], fill=c)


def icon_cross(d, x, y, s, c):
    d.ellipse([x, y, x + s, y + s], outline=c, width=4)
    t = s * 0.16
    d.rectangle([x + s / 2 - t / 2, y + s * 0.22,
                 x + s / 2 + t / 2, y + s * 0.78], fill=c)
    d.rectangle([x + s * 0.22, y + s / 2 - t / 2,
                 x + s * 0.78, y + s / 2 + t / 2], fill=c)


ICONS = {"globe": icon_globe, "bridge": icon_bridge, "radar": icon_radar,
         "shield": icon_shield, "bars": icon_bars, "cross": icon_cross}


def draw_panel(d, x, y, w, h, story):
    tag, color, icon, headline, summary = story
    d.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=CARD,
                        outline=LINE, width=1)
    d.rounded_rectangle([x, y, x + w, y + 7], radius=3, fill=color)
    # icon top-left, tag to its right
    ICONS[icon](d, x + 18, y + 22, 58, color)
    f_tag = font(BOLD, 17)
    d.text((x + 90, y + 38), tag, font=f_tag, fill=color)
    # headline
    f_head = font(BOLD, 27)
    lines = wrap(d, headline, f_head, w - 36)[:3]
    ty = y + 96
    for ln in lines:
        d.text((x + 18, ty), ln, font=f_head, fill=INK)
        ty += 33
    # summary (clamped to the space left in the panel)
    f_sum = font(REG, 19)
    max_sum_lines = max(0, (y + h - 10 - (ty + 6)) // 25)
    slines = wrap(d, summary, f_sum, w - 36)[:max_sum_lines]
    ty += 6
    for ln in slines:
        d.text((x + 18, ty), ln, font=f_sum, fill=GREY)
        ty += 25


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 138], fill=NAVY)
    d.text((28, 22), "WORLD NEWS", font=font(BOLD, 56), fill=(255, 255, 255))
    d.text((28, 88), "Wednesday, 18 November 2026",
           font=font(BOLD, 32), fill=GOLD)
    d.rectangle([0, 138, W, 143], fill=GOLD)

    # ---- story grid: 2 cols x 3 rows ----
    mx, my = 28, 158
    gap = 16
    pw = (W - 2 * mx - gap) // 2
    ph = (H - my - 46 - 2 * gap) // 3
    for i, story in enumerate(STORIES):
        cx = mx + (i % 2) * (pw + gap)
        cy = my + (i // 2) * (ph + gap)
        draw_panel(d, cx, cy, pw, ph, story)

    # ---- footer ----
    f_foot = font(REG, 16)
    foot = "Sources: NDTV  ·  Indian Express  ·  AFP  ·  The Manila Times"
    fw = d.textlength(foot, font=f_foot)
    d.text(((W - fw) / 2, H - 34), foot, font=f_foot, fill=(110, 105, 95))

    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
