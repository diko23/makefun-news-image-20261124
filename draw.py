"""Generate the 1024x1024 front-page world news infographic for Tuesday 24 November 2026."""

from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

WIDTH = 1024
HEIGHT = 1024

BG_PAPER = (247, 245, 240)
NAVY_DARK = (15, 23, 42)
NAVY_MID = (30, 41, 59)
CRIMSON = (185, 28, 28)
GOLD = (250, 204, 21)
TEXT_DARK = (15, 23, 42)
TEXT_MUTED = (51, 65, 85)
CARD_BG = (255, 255, 255)
CARD_BORDER = (203, 213, 225)
WHITE = (255, 255, 255)

FONT_BOLD = r"C:\Windows\Fonts\arialbd.ttf"
FONT_REG = r"C:\Windows\Fonts\arial.ttf"

CHIP_COLORS = {
    "LEAD": (185, 28, 28),
    "MARITIME": (194, 65, 12),
    "EUROPE": (29, 78, 216),
    "JUSTICE": (109, 40, 217),
    "MARKETS": (4, 120, 87),
    "GAZA": (190, 18, 60),
    "GULF": (180, 83, 9),
    "ASIA": (13, 148, 136),
    "AMERICAS": (126, 34, 206),
}

LEAD_STORY = {
    "chip": "LEAD · US / TECH & LAW",
    "chip_key": "LEAD",
    "headline": "HUAWEI GUILTY ON 10 OF 12 COUNTS",
    "subhead": (
        "US jury convicted Huawei of trade-secret theft conspiracy and bank fraud; "
        "acquitted of racketeering; sentencing Sept 2027."
    ),
}

GRID_STORIES = [
    {
        "chip": "MIDEAST · MARITIME",
        "chip_key": "MARITIME",
        "icon": "tanker",
        "headline": "HORMUZ TANKERS HIT",
        "subhead": "Iran said 4 oil tankers hit naval mines in Strait of Hormuz; IRGC attacked container ship.",
    },
    {
        "chip": "EUROPE · CONFLICT",
        "chip_key": "EUROPE",
        "icon": "radar",
        "headline": "UKRAINE HITS RUSSIAN SHIPS",
        "subhead": "Drones hit Sparta II in Gulf of Finland & corvette off Libya; Poland cited airspace breach.",
    },
    {
        "chip": "WORLD COURT · ASIA",
        "chip_key": "JUSTICE",
        "icon": "scales",
        "headline": "ICJ: MYANMAR GUILTY OF GENOCIDE",
        "subhead": "World Court ruled 9-6 Myanmar committed Rohingya genocide in 2017 (1st state guilty).",
    },
    {
        "chip": "TECH · MARKETS",
        "chip_key": "MARKETS",
        "icon": "chip",
        "headline": "HUANG BACK AT NVIDIA",
        "subhead": "Jensen Huang reinstated as CEO under 2 weeks after resigning; US blacklisted Megaspeed.",
    },
    {
        "chip": "MIDEAST · GAZA",
        "chip_key": "GAZA",
        "icon": "target",
        "headline": "ISRAEL KILLS HAMAS SECURITY CHIEF",
        "subhead": "Strikes killed Brig. Gen. Naeem Abu Nahel, internal security head, plus 6 others.",
    },
    {
        "chip": "GULF · SECURITY",
        "chip_key": "GULF",
        "icon": "tower",
        "headline": "RIYADH TOWER HIT AGAIN",
        "subhead": "Suspected Houthi drone hit Saudi PIF tower in Riyadh, 11+ wounded — 2nd hit in <1 week.",
    },
    {
        "chip": "EAST ASIA · DEFENSE",
        "chip_key": "ASIA",
        "icon": "jet",
        "headline": "RUSSIAN JETS NEAR SOUTH KOREA",
        "subhead": "Seoul told Ulleungdo islanders to shelter after jets entered air zone; fighters scrambled.",
    },
    {
        "chip": "AMERICAS · COLOMBIA",
        "chip_key": "AMERICAS",
        "icon": "shield",
        "headline": "CARTAGENA HOSTAGE CRISIS",
        "subhead": "Armed men seized a Cartagena supermarket holding 25 hostages; 5 older women released.",
    },
]


def load_font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size=size)


def wrap_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    font: ImageFont.FreeTypeFont,
    max_width: int,
    max_lines: int,
) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for idx, word in enumerate(words):
        candidate = f"{current} {word}".strip()
        bbox = draw.textbbox((0, 0), candidate, font=font)
        if bbox[2] - bbox[0] <= max_width or not current:
            current = candidate
        else:
            lines.append(current)
            current = word
            if len(lines) == max_lines:
                remaining = " ".join(words[idx:])
                raise ValueError(f"Text overflow beyond {max_lines} lines: {remaining!r}")
    if current:
        if len(lines) >= max_lines:
            raise ValueError(f"Text overflow beyond {max_lines} lines: {current!r}")
        lines.append(current)
    return lines


def draw_chip(
    draw: ImageDraw.ImageDraw,
    x: int,
    y: int,
    label: str,
    color: tuple[int, int, int],
    font: ImageFont.FreeTypeFont,
) -> int:
    bbox = draw.textbbox((0, 0), label, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    pad_x = 10
    pad_y = 4
    w = tw + pad_x * 2
    h = th + pad_y * 2 + 2
    draw.rounded_rectangle((x, y, x + w, y + h), radius=5, fill=color)
    draw.text((x + pad_x, y + pad_y - 1), label, font=font, fill=WHITE)
    return h


def draw_globe_emblem(canvas: Image.Image, x: int, y: int, size: int) -> None:
    s = size * 3
    em = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(em)
    pad = 4
    d.ellipse((pad, pad, s - pad, s - pad), outline=(250, 204, 21, 255), width=6)
    d.ellipse((s * 0.28, pad, s * 0.72, s - pad), outline=(250, 204, 21, 220), width=4)
    d.line((pad, s // 2, s - pad, s // 2), fill=(250, 204, 21, 220), width=4)
    d.line((s // 2, pad, s // 2, s - pad), fill=(250, 204, 21, 220), width=4)
    d.arc((pad + 6, s * 0.16, s - pad - 6, s * 0.48), 15, 165, fill=(250, 204, 21, 180), width=4)
    d.arc((pad + 6, s * 0.52, s - pad - 6, s * 0.84), 195, 345, fill=(250, 204, 21, 180), width=4)
    em_small = em.resize((size, size), Image.Resampling.LANCZOS)
    canvas.paste(em_small, (x, y), em_small)


def draw_story_icon(
    canvas: Image.Image,
    x: int,
    y: int,
    size: int,
    kind: str,
    color: tuple[int, int, int],
) -> None:
    s = size * 3
    ic = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(ic)
    bg = (color[0], color[1], color[2], 24)
    fg = (color[0], color[1], color[2], 235)
    d.rounded_rectangle((2, 2, s - 3, s - 3), radius=s // 5, fill=bg, outline=(color[0], color[1], color[2], 90), width=4)

    if kind == "tanker":
        d.polygon([(s * 0.16, s * 0.58), (s * 0.84, s * 0.58), (s * 0.74, s * 0.74), (s * 0.24, s * 0.74)], fill=fg)
        d.rectangle((s * 0.30, s * 0.42, s * 0.62, s * 0.58), fill=fg)
        d.rectangle((s * 0.64, s * 0.34, s * 0.76, s * 0.58), fill=fg)
        d.polygon([(s * 0.42, s * 0.18), (s * 0.52, s * 0.38), (s * 0.34, s * 0.38)], fill=CRIMSON + (235,))
    elif kind == "radar":
        cx, cy = s // 2, s // 2
        for r in (int(s * 0.36), int(s * 0.24), int(s * 0.12)):
            d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=fg, width=4)
        d.line((cx, cy, int(cx + s * 0.28), int(cy - s * 0.24)), fill=CRIMSON + (245,), width=5)
        d.ellipse((cx + s * 0.14, cy - s * 0.22, cx + s * 0.24, cy - s * 0.12), fill=CRIMSON + (245,))
    elif kind == "scales":
        cx = s // 2
        d.line((cx, s * 0.20, cx, s * 0.78), fill=fg, width=6)
        d.line((s * 0.28, s * 0.78, s * 0.72, s * 0.78), fill=fg, width=6)
        d.line((s * 0.22, s * 0.30, s * 0.78, s * 0.30), fill=fg, width=5)
        d.polygon([(s * 0.14, s * 0.54), (s * 0.34, s * 0.54), (s * 0.24, s * 0.30)], outline=fg, width=4)
        d.polygon([(s * 0.66, s * 0.54), (s * 0.86, s * 0.54), (s * 0.76, s * 0.30)], outline=fg, width=4)
    elif kind == "chip":
        d.rounded_rectangle((s * 0.26, s * 0.26, s * 0.74, s * 0.74), radius=8, outline=fg, width=6)
        d.rectangle((s * 0.38, s * 0.38, s * 0.62, s * 0.62), fill=fg)
        for p in (0.36, 0.50, 0.64):
            d.line((s * p, s * 0.14, s * p, s * 0.26), fill=fg, width=5)
            d.line((s * p, s * 0.74, s * p, s * 0.86), fill=fg, width=5)
            d.line((s * 0.14, s * p, s * 0.26, s * p), fill=fg, width=5)
            d.line((s * 0.74, s * p, s * 0.86, s * p), fill=fg, width=5)
    elif kind == "target":
        cx, cy = s // 2, s // 2
        for r in (int(s * 0.33), int(s * 0.19)):
            d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=fg, width=5)
        d.line((cx, s * 0.12, cx, s * 0.88), fill=fg, width=4)
        d.line((s * 0.12, cy, s * 0.88, cy), fill=fg, width=4)
    elif kind == "tower":
        d.polygon([(s * 0.36, s * 0.84), (s * 0.44, s * 0.22), (s * 0.56, s * 0.22), (s * 0.64, s * 0.84)], fill=fg)
        d.line((s * 0.50, s * 0.12, s * 0.50, s * 0.24), fill=fg, width=5)
        d.polygon([(s * 0.62, s * 0.24), (s * 0.82, s * 0.32), (s * 0.64, s * 0.44)], fill=CRIMSON + (240,))
    elif kind == "jet":
        d.polygon([(s * 0.50, s * 0.16), (s * 0.82, s * 0.66), (s * 0.58, s * 0.60), (s * 0.50, s * 0.82), (s * 0.42, s * 0.60), (s * 0.18, s * 0.66)], fill=fg)
    elif kind == "shield":
        d.polygon([(s * 0.24, s * 0.22), (s * 0.76, s * 0.22), (s * 0.72, s * 0.60), (s * 0.50, s * 0.82), (s * 0.28, s * 0.60)], outline=fg, width=6)
        d.line((s * 0.50, s * 0.34, s * 0.50, s * 0.56), fill=fg, width=6)
        d.ellipse((s * 0.46, s * 0.62, s * 0.54, s * 0.70), fill=fg)
    elif kind == "gavel":
        d.line((s * 0.26, s * 0.76, s * 0.66, s * 0.36), fill=fg, width=8)
        d.polygon([(s * 0.44, s * 0.22), (s * 0.60, s * 0.14), (s * 0.78, s * 0.42), (s * 0.62, s * 0.50)], fill=fg)
        d.rounded_rectangle((s * 0.20, s * 0.76, s * 0.56, s * 0.86), radius=4, fill=fg)

    ic_small = ic.resize((size, size), Image.Resampling.LANCZOS)
    canvas.paste(ic_small, (x, y), ic_small)


def draw_masthead(canvas: Image.Image, draw: ImageDraw.ImageDraw) -> int:
    band_h = 108
    draw.rectangle((0, 0, WIDTH, band_h), fill=NAVY_DARK)
    draw.rectangle((0, 58, WIDTH, 61), fill=CRIMSON)
    draw.rectangle((0, 61, WIDTH, band_h), fill=NAVY_MID)

    f_title = load_font(FONT_BOLD, 42)
    f_edition = load_font(FONT_BOLD, 20)
    f_date = load_font(FONT_BOLD, 34)

    draw_globe_emblem(canvas, 28, 8, 44)
    draw.text((82, 9), "WORLD NEWS", font=f_title, fill=WHITE)
    ed_text = "DAILY FRONT PAGE"
    ed_bbox = draw.textbbox((0, 0), ed_text, font=f_edition)
    draw.text((WIDTH - 28 - (ed_bbox[2] - ed_bbox[0]), 20), ed_text, font=f_edition, fill=(148, 163, 184))

    date_text = "TUESDAY 24 NOVEMBER 2026"
    d_bbox = draw.textbbox((0, 0), date_text, font=f_date)
    dx = (WIDTH - (d_bbox[2] - d_bbox[0])) // 2
    draw.text((dx, 66), date_text, font=f_date, fill=GOLD)
    return band_h


def draw_lead(canvas: Image.Image, draw: ImageDraw.ImageDraw, y_top: int) -> int:
    x = 28
    w = WIDTH - 56
    h = 144
    draw.rounded_rectangle((x, y_top, x + w, y_top + h), radius=10, fill=CARD_BG, outline=CARD_BORDER, width=2)
    draw.rounded_rectangle((x + 4, y_top + 6, x + 12, y_top + h - 6), radius=4, fill=CRIMSON)

    icon_size = 94
    draw_story_icon(canvas, x + w - icon_size - 16, y_top + (h - icon_size) // 2, icon_size, "gavel", CRIMSON)

    f_chip = load_font(FONT_BOLD, 18)
    f_head = load_font(FONT_BOLD, 35)
    f_sub = load_font(FONT_REG, 21)

    cx = x + 24
    cy = y_top + 12
    ch = draw_chip(draw, cx, cy, LEAD_STORY["chip"], CHIP_COLORS["LEAD"], f_chip)
    hy = cy + ch + 8
    draw.text((cx, hy), LEAD_STORY["headline"], font=f_head, fill=TEXT_DARK)

    sy = hy + 42
    max_text_w = w - icon_size - 56
    lines = wrap_text(draw, LEAD_STORY["subhead"], f_sub, max_text_w, 2)
    for line in lines:
        draw.text((cx, sy), line, font=f_sub, fill=TEXT_MUTED)
        sy += 24
    return y_top + h


def draw_grid(canvas: Image.Image, draw: ImageDraw.ImageDraw, y_top: int) -> int:
    margin_x = 28
    col_gap = 16
    row_gap = 12
    col_w = (WIDTH - margin_x * 2 - col_gap) // 2
    card_h = 162

    f_chip = load_font(FONT_BOLD, 18)
    f_head = load_font(FONT_BOLD, 28)
    f_sub = load_font(FONT_REG, 20)

    for idx, story in enumerate(GRID_STORIES):
        row = idx // 2
        col = idx % 2
        x = margin_x + col * (col_w + col_gap)
        y = y_top + row * (card_h + row_gap)

        accent = CHIP_COLORS[story["chip_key"]]
        draw.rounded_rectangle((x, y, x + col_w, y + card_h), radius=10, fill=CARD_BG, outline=CARD_BORDER, width=2)
        draw.rounded_rectangle((x + 4, y + 6, x + 10, y + card_h - 6), radius=3, fill=accent)

        icon_size = 34
        draw_story_icon(canvas, x + col_w - icon_size - 12, y + 8, icon_size, story["icon"], accent)

        tx = x + 18
        ty = y + 10
        ch = draw_chip(draw, tx, ty, story["chip"], accent, f_chip)

        hy = ty + ch + 11
        h_lines = wrap_text(draw, story["headline"], f_head, col_w - 34, 2)
        for line in h_lines:
            draw.text((tx, hy), line, font=f_head, fill=TEXT_DARK)
            hy += 30

        sy = hy + 6
        s_lines = wrap_text(draw, story["subhead"], f_sub, col_w - 34, 2)
        for line in s_lines:
            draw.text((tx, sy), line, font=f_sub, fill=TEXT_MUTED)
            sy += 23

    return y_top + 4 * card_h + 3 * row_gap


def draw_footer(draw: ImageDraw.ImageDraw) -> None:
    y = HEIGHT - 34
    draw.rectangle((0, y, WIDTH, HEIGHT), fill=NAVY_DARK)
    f_foot = load_font(FONT_BOLD, 20)
    txt = "TUESDAY 24 NOVEMBER 2026  ·  WORLD NEWS SUMMARY  ·  9 KEY STORIES"
    bbox = draw.textbbox((0, 0), txt, font=f_foot)
    draw.text(((WIDTH - (bbox[2] - bbox[0])) // 2, y + 6), txt, font=f_foot, fill=(203, 213, 225))


def main() -> None:
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_PAPER)
    draw = ImageDraw.Draw(img)

    y = draw_masthead(img, draw)
    y = draw_lead(img, draw, y + 12)
    draw_grid(img, draw, y + 12)
    draw_footer(draw)

    out_path = Path(__file__).resolve().parent / "entry.png"
    img.save(out_path, format="PNG", optimize=True)


if __name__ == "__main__":
    main()
