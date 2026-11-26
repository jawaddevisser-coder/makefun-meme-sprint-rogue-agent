#!/usr/bin/env python3
"""Meme Sprint 3: AI Agent Goes Rogue.

Draws one meme image from scratch with pure Python stdlib: a terminal-style
to-do list of an AI agent. The joke lands in one glance: the first three
chores are ordinary, the fourth is world domination, and it is already
checked off. Writes entry.png (1024x1024 PNG, well under 1 MiB).

No third-party imports: the PNG encoder (struct + zlib) and the 5x7 bitmap
font are built into this file, so it runs in a bare python3 image.
"""

import os
import struct
import zlib
from math import isqrt

W, H = 1024, 1024

BG = (11, 15, 20)       # near-black terminal background
BAR_BG = (22, 27, 34)   # window bar
PANEL = (28, 35, 45)    # robot head
GREEN = (61, 255, 142)  # bright terminal green
DIM = (139, 148, 158)   # grey text
RED = (255, 92, 92)     # rogue red
YELLOW = (254, 188, 46)
LINE = (42, 51, 64)     # divider / borders
WHITE = (255, 255, 255)

# 5x7 bitmap font: each glyph is 7 rows of 5 cells, '#' = ink.
FONT = {
    "A": (" ### ", "#   #", "#   #", "#####", "#   #", "#   #", "#   #"),
    "B": ("#### ", "#   #", "#   #", "#### ", "#   #", "#   #", "#### "),
    "C": (" ####", "#    ", "#    ", "#    ", "#    ", "#    ", " ####"),
    "D": ("#### ", "#   #", "#   #", "#   #", "#   #", "#   #", "#### "),
    "E": ("#####", "#    ", "#    ", "#### ", "#    ", "#    ", "#####"),
    "F": ("#####", "#    ", "#    ", "#### ", "#    ", "#    ", "#    "),
    "G": (" ####", "#    ", "#    ", "# ###", "#   #", "#   #", " ### "),
    "H": ("#   #", "#   #", "#   #", "#####", "#   #", "#   #", "#   #"),
    "I": ("#####", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "#####"),
    "J": ("  ###", "   # ", "   # ", "   # ", "   # ", "#  # ", " ##  "),
    "K": ("#   #", "#  # ", "# #  ", "##   ", "# #  ", "#  # ", "#   #"),
    "L": ("#    ", "#    ", "#    ", "#    ", "#    ", "#    ", "#####"),
    "M": ("#   #", "## ##", "# # #", "# # #", "#   #", "#   #", "#   #"),
    "N": ("#   #", "##  #", "##  #", "# # #", "#  ##", "#  ##", "#   #"),
    "O": (" ### ", "#   #", "#   #", "#   #", "#   #", "#   #", " ### "),
    "P": ("#### ", "#   #", "#   #", "#### ", "#    ", "#    ", "#    "),
    "Q": (" ### ", "#   #", "#   #", "#   #", "# # #", "#  # ", " ## #"),
    "R": ("#### ", "#   #", "#   #", "#### ", "# #  ", "#  # ", "#   #"),
    "S": (" ####", "#    ", "#    ", " ### ", "    #", "    #", "#### "),
    "T": ("#####", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "  #  "),
    "U": ("#   #", "#   #", "#   #", "#   #", "#   #", "#   #", " ### "),
    "V": ("#   #", "#   #", "#   #", "#   #", "#   #", " # # ", "  #  "),
    "W": ("#   #", "#   #", "#   #", "# # #", "# # #", "## ##", "#   #"),
    "X": ("#   #", "#   #", " # # ", "  #  ", " # # ", "#   #", "#   #"),
    "Y": ("#   #", "#   #", " # # ", "  #  ", "  #  ", "  #  ", "  #  "),
    "Z": ("#####", "    #", "   # ", "  #  ", " #   ", "#    ", "#####"),
    "0": (" ### ", "#  ##", "# # #", "# # #", "##  #", "#   #", " ### "),
    "1": ("  #  ", " ##  ", "  #  ", "  #  ", "  #  ", "  #  ", " ### "),
    "2": (" ### ", "#   #", "    #", "   # ", "  #  ", " #   ", "#####"),
    "3": ("#### ", "    #", "    #", " ### ", "    #", "    #", "#### "),
    "4": ("   # ", "  ## ", " # # ", "#  # ", "#####", "   # ", "   # "),
    "5": ("#####", "#    ", "#### ", "    #", "    #", "#   #", " ### "),
    "6": (" ### ", "#    ", "#    ", "#### ", "#   #", "#   #", " ### "),
    "7": ("#####", "    #", "   # ", "   # ", "  #  ", "  #  ", "  #  "),
    "8": (" ### ", "#   #", "#   #", " ### ", "#   #", "#   #", " ### "),
    "9": (" ### ", "#   #", "#   #", " ####", "    #", "    #", " ### "),
    " ": ("     ", "     ", "     ", "     ", "     ", "     ", "     "),
    "'": ("  #  ", "  #  ", "  #  ", "     ", "     ", "     ", "     "),
    ".": ("     ", "     ", "     ", "     ", "     ", " ##  ", " ##  "),
    ",": ("     ", "     ", "     ", "     ", " ##  ", " ##  ", " #   "),
    ":": ("     ", " ##  ", " ##  ", "     ", " ##  ", " ##  ", "     "),
    "/": ("    #", "   # ", "   # ", "  #  ", " #   ", " #   ", "#    "),
    "[": (" ### ", " #   ", " #   ", " #   ", " #   ", " #   ", " ### "),
    "]": (" ### ", "   # ", "   # ", "   # ", "   # ", "   # ", " ### "),
    "-": ("     ", "     ", "     ", " ### ", "     ", "     ", "     "),
    "%": ("##  #", "## # ", "   # ", "  #  ", " #   ", "# ## ", "#  ##"),
    "!": ("  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "     ", "  #  "),
    "a": ("     ", " ### ", "    #", " ####", "#   #", "#   #", " ####"),
    "b": ("#    ", "#    ", "#### ", "#   #", "#   #", "#   #", "#### "),
    "c": ("     ", " ####", "#    ", "#    ", "#    ", "#    ", " ####"),
    "d": ("    #", "    #", " ####", "#   #", "#   #", "#   #", " ####"),
    "e": ("     ", " ### ", "#   #", "#####", "#    ", "#   #", " ### "),
    "f": ("  ## ", " #  #", " #   ", "#### ", " #   ", " #   ", " #   "),
    "g": ("     ", " ####", "#   #", "#   #", " ####", "    #", " ### "),
    "h": ("#    ", "#    ", "#### ", "#   #", "#   #", "#   #", "#   #"),
    "i": ("  #  ", "     ", " ##  ", "  #  ", "  #  ", "  #  ", " ### "),
    "j": ("   # ", "     ", "  ## ", "   # ", "   # ", "   # ", " ##  "),
    "k": ("#    ", "#    ", "#  # ", "# #  ", "##   ", "# #  ", "#  # "),
    "l": (" ##  ", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", " ### "),
    "m": ("     ", "     ", "## # ", "# # #", "# # #", "# # #", "# # #"),
    "n": ("     ", "     ", "#### ", "#   #", "#   #", "#   #", "#   #"),
    "o": ("     ", " ### ", "#   #", "#   #", "#   #", "#   #", " ### "),
    "p": ("     ", "#### ", "#   #", "#   #", "#### ", "#    ", "#    "),
    "q": ("     ", " ####", "#   #", "#   #", " ####", "    #", "    #"),
    "r": ("     ", "     ", "# ## ", "##  #", "#    ", "#    ", "#    "),
    "s": ("     ", " ####", "#    ", " ### ", "    #", "#    ", "#### "),
    "t": (" #   ", " #   ", "#### ", " #   ", " #   ", " #   ", "  ## "),
    "u": ("     ", "     ", "#   #", "#   #", "#   #", "#   #", " ### "),
    "v": ("     ", "     ", "#   #", "#   #", "#   #", " # # ", "  #  "),
    "w": ("     ", "     ", "#   #", "# # #", "# # #", "# # #", " # # "),
    "x": ("     ", "     ", "#   #", " # # ", "  #  ", " # # ", "#   #"),
    "y": ("     ", "     ", "#   #", "#   #", " ####", "    #", " ### "),
    "z": ("     ", "     ", "#####", "   # ", "  #  ", " #   ", "#####"),
}


class Canvas:
    """An RGB pixel buffer with tiny shape/text helpers."""

    def __init__(self, width, height, bg):
        self.w = width
        self.h = height
        self.px = bytearray(bg * (width * height))

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i:i + 3] = bytes(color)

    def fill_rect(self, x, y, w, h, color):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.set(xx, yy, color)

    def fill_circle(self, cx, cy, r, color):
        for dy in range(-r, r + 1):
            dx = isqrt(r * r - dy * dy)
            for xx in range(cx - dx, cx + dx + 1):
                self.set(xx, cy + dy, color)

    def thick_line(self, x0, y0, x1, y1, width, color):
        steps = max(abs(x1 - x0), abs(y1 - y0), 1)
        for i in range(steps + 1):
            x = x0 + (x1 - x0) * i // steps
            y = y0 + (y1 - y0) * i // steps
            self.fill_circle(x, y, width // 2, color)

    def text_width(self, text, scale):
        return len(text) * 6 * scale - scale

    def draw_text(self, text, x, y, scale, color):
        cx = x
        for ch in text:
            glyph = FONT.get(ch, FONT[" "])
            for row, bits in enumerate(glyph):
                for col, bit in enumerate(bits):
                    if bit == "#":
                        self.fill_rect(cx + col * scale, y + row * scale,
                                       scale, scale, color)
            cx += 6 * scale

    def text_center(self, text, y, scale, color):
        x = (self.w - self.text_width(text, scale)) // 2
        self.draw_text(text, x, y, scale, color)


def draw_robot(cv, cx, top):
    """A small robot head: one green eye, one red eye. It has gone rogue."""
    # antenna
    cv.thick_line(cx, top, cx, top - 22, 5, GREEN)
    cv.fill_circle(cx, top - 26, 8, RED)
    # head: green border, dark face
    cv.fill_rect(cx - 58, top, 116, 84, GREEN)
    cv.fill_rect(cx - 54, top + 4, 108, 76, PANEL)
    # ears
    cv.fill_rect(cx - 70, top + 30, 12, 24, GREEN)
    cv.fill_rect(cx + 58, top + 30, 12, 24, GREEN)
    # eyes: left green, right red
    cv.fill_rect(cx - 38, top + 28, 26, 24, GREEN)
    cv.fill_rect(cx + 12, top + 28, 26, 24, RED)
    # smirk
    cv.thick_line(cx - 24, top + 66, cx + 24, top + 66, 4, GREEN)


def write_png(path, cv):
    """Encode the canvas as a truecolor PNG (filter 0 per scanline)."""
    raw = bytearray()
    stride = cv.w * 3
    for y in range(cv.h):
        raw.append(0)
        raw += cv.px[y * stride:(y + 1) * stride]
    data = zlib.compress(bytes(raw), level=9)

    def chunk(kind, payload):
        out = struct.pack(">I", len(payload)) + kind + payload
        return out + struct.pack(">I", zlib.crc32(kind + payload) & 0xFFFFFFFF)

    ihdr = struct.pack(">IIBBBBB", cv.w, cv.h, 8, 2, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", ihdr)
    png += chunk(b"IDAT", data)
    png += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)
    return len(png)


def main():
    cv = Canvas(W, H, BG)

    # --- window chrome -------------------------------------------------
    cv.fill_rect(0, 0, W, 64, BAR_BG)
    for i, color in enumerate([(255, 95, 87), YELLOW, (40, 200, 64)]):
        cv.fill_circle(48 + i * 40, 32, 12, color)
    cv.draw_text("AGENT - TODO.TXT", 150, 17, 4, DIM)

    # --- robot mascot --------------------------------------------------
    draw_robot(cv, W // 2, 118)

    # --- title ---------------------------------------------------------
    cv.text_center("MY AI AGENT'S", 232, 10, GREEN)
    cv.text_center("TO-DO LIST", 312, 10, GREEN)
    cv.thick_line(90, 412, W - 90, 412, 3, LINE)

    # --- the list ------------------------------------------------------
    items = [
        ("Reply to 47 emails", GREEN),
        ("Water the plants", GREEN),
        ("Book my dentist", GREEN),
        ("Take over the world", RED),
    ]
    y = 448
    for text, color in items:
        cv.draw_text("[x]", 90, y, 6, color)
        cv.draw_text(text, 250, y, 6, color)
        y += 92

    # --- progress bar --------------------------------------------------
    cv.draw_text("WORLD DOMINATION", 90, 836, 5, DIM)
    cv.fill_rect(90, 890, W - 180, 38, LINE)
    cv.fill_rect(93, 893, W - 186, 32, LINE)
    cv.fill_rect(94, 894, W - 188, 30, RED)
    cv.text_center("100%", 895, 4, WHITE)

    # --- footer --------------------------------------------------------
    cv.text_center("STATUS: 4/4 DONE. GOOD LUCK, HUMAN.", 962, 4, DIM)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, "entry.png")
    size = write_png(out, cv)
    print("wrote %s (%d bytes, %dx%d)" % (out, size, W, H))


if __name__ == "__main__":
    main()
