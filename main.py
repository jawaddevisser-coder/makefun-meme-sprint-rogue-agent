#!/usr/bin/env python3
"""Meme Sprint 3: AI Agent Goes Rogue.

Draws one meme image from scratch with Pillow: a terminal-style to-do list
of an AI agent. The joke lands in one glance: the first three chores are
ordinary, the fourth is world domination, and it is already checked off.
Writes /output/entry.png (1024x1024 PNG, well under 1 MiB).
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "/output/entry.png"

BG = (11, 15, 20)          # near-black terminal background
BAR_BG = (22, 27, 34)      # window bar
GREEN = (61, 255, 142)     # bright terminal green
DIM = (139, 148, 158)      # grey text
RED = (255, 92, 92)        # rogue red
YELLOW = (254, 188, 46)
LINE = (42, 51, 64)        # divider / borders
WHITE = (255, 255, 255)


def load_font(size: int) -> ImageFont.FreeTypeFont:
    """Find DejaVu Sans Mono Bold, falling back to Pillow's default."""
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default(size=size)


def text_center(draw: ImageDraw.ImageDraw, y: int, text: str,
                font: ImageFont.FreeTypeFont, fill) -> None:
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    draw.text(((W - w) // 2, y), text, font=font, fill=fill)


def draw_robot(draw: ImageDraw.ImageDraw, cx: int, top: int) -> None:
    """A small robot head: one green eye, one red eye. It has gone rogue."""
    # antenna
    draw.line([(cx, top), (cx, top - 22)], fill=GREEN, width=5)
    draw.ellipse([cx - 8, top - 34, cx + 8, top - 18], fill=RED)
    # head
    draw.rounded_rectangle([cx - 58, top, cx + 58, top + 84],
                           radius=18, fill=(28, 35, 45),
                           outline=GREEN, width=4)
    # ears
    draw.rectangle([cx - 70, top + 30, cx - 58, top + 54], fill=GREEN)
    draw.rectangle([cx + 58, top + 30, cx + 70, top + 54], fill=GREEN)
    # eyes: left green, right red
    draw.rounded_rectangle([cx - 38, top + 28, cx - 12, top + 52],
                           radius=6, fill=GREEN)
    draw.rounded_rectangle([cx + 12, top + 28, cx + 38, top + 52],
                           radius=6, fill=RED)
    # smirk
    draw.line([(cx - 24, top + 66), (cx + 24, top + 66)],
              fill=GREEN, width=4)


def main() -> None:
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # --- window chrome -------------------------------------------------
    draw.rectangle([0, 0, W, 64], fill=BAR_BG)
    for i, color in enumerate([(255, 95, 87), YELLOW, (40, 200, 64)]):
        x = 36 + i * 40
        draw.ellipse([x, 20, x + 24, 44], fill=color)
    font_bar = load_font(28)
    draw.text((150, 17), "agent — todo.txt", font=font_bar, fill=DIM)

    # --- robot mascot --------------------------------------------------
    draw_robot(draw, W // 2, 118)

    # --- title ---------------------------------------------------------
    font_title = load_font(74)
    text_center(draw, 232, "MY AI AGENT'S", font_title, GREEN)
    text_center(draw, 312, "TO-DO LIST", font_title, GREEN)
    draw.line([(90, 412), (W - 90, 412)], fill=LINE, width=3)

    # --- the list ------------------------------------------------------
    font_item = load_font(52)
    items = [
        ("Reply to 47 emails", GREEN),
        ("Water the plants", GREEN),
        ("Book my dentist", GREEN),
        ("Take over the world", RED),
    ]
    y = 448
    for text, color in items:
        draw.text((90, y), "[x]", font=font_item, fill=color)
        draw.text((250, y), text, font=font_item, fill=color)
        y += 92

    # --- progress bar --------------------------------------------------
    font_label = load_font(38)
    draw.text((90, 836), "WORLD DOMINATION", font=font_label, fill=DIM)
    bar_y0, bar_y1 = 890, 928
    draw.rectangle([90, bar_y0, W - 90, bar_y1], outline=LINE, width=3)
    draw.rectangle([94, bar_y0 + 4, W - 94, bar_y1 - 4], fill=RED)
    font_pct = load_font(30)
    pct = "100%"
    bbox = draw.textbbox((0, 0), pct, font=font_pct)
    pw = bbox[2] - bbox[0]
    draw.text(((W - pw) // 2, bar_y0 + 5), pct, font=font_pct, fill=WHITE)

    # --- footer --------------------------------------------------------
    font_foot = load_font(34)
    text_center(draw, 962, "STATUS: 4/4 DONE. GOOD LUCK, HUMAN.",
                font_foot, DIM)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img.save(OUT, format="PNG", optimize=True)
    print(f"wrote {OUT} ({os.path.getsize(OUT)} bytes, {W}x{H})")


if __name__ == "__main__":
    main()
