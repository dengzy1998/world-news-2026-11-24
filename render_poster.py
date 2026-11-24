#!/usr/bin/env python3
"""Render the 24 November 2026 world-news poster (1024x1024 PNG).

Written fresh for news-image-20261124 from the stories ledger in stories.md.
Deterministic: no network, no clock, no randomness. Renders entry.png.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 232)
INK = (25, 25, 25)
MUTED = (90, 86, 76)
RED = (166, 30, 30)
BLUE = (30, 78, 138)
TEAL = (15, 107, 92)
GOLD = (154, 106, 0)
LINE = (201, 194, 176)
CARD = (255, 255, 255)
MAPFILL = (216, 210, 192)
MAPLINE = (138, 132, 113)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    path = os.path.join(FONT_DIR, name)
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


F_TITLE = font("DejaVuSans-Bold.ttf", 46)
F_DATE = font("DejaVuSans-Bold.ttf", 19)
F_SUB = font("DejaVuSans-Bold.ttf", 13)
F_SECTION = font("DejaVuSans-Bold.ttf", 12)
F_TAG = font("DejaVuSans-Bold.ttf", 11)
F_LEAD_HEAD = font("DejaVuSans-Bold.ttf", 16)
F_LEAD_SUM = font("DejaVuSans.ttf", 12)
F_GRID_HEAD = font("DejaVuSans-Bold.ttf", 12)
F_GRID_SUM = font("DejaVuSans.ttf", 11)
F_ONE = font("DejaVuSans.ttf", 10)
F_ONE_B = font("DejaVuSans-Bold.ttf", 10)
F_SMALL = font("DejaVuSans.ttf", 10)
F_SMALL_B = font("DejaVuSans-Bold.ttf", 10)
F_TINY = font("DejaVuSans.ttf", 9)
F_MAP_NUM = font("DejaVuSans-Bold.ttf", 10)

# --- story data: (number, region, tag, headline, summary, source) ---
LEADS = [
    (1, "BUSINESS · TECH", "Nvidia brings Huang back as CEO after Trump push",
     "Nvidia rehires Jensen Huang after Trump pressure; shares jump about a third.",
     "Japan Times · Sunday Guardian", RED),
    (2, "US POLITICS", "Gomez resigns after ethics panel finds misconduct",
     "Gomez quits, effective 1 Dec, after the panel finds evidence of sexual misconduct.",
     "Associated Press", BLUE),
    (3, "WAR · EUROPE", "Russian strikes on Kyiv region kill at least 14",
     "Russian strikes hit Kyiv region, killing 14 and damaging homes in Dymer.",
     "Associated Press", INK),
]

GRID = [
    (4, "TECH · LAW", "States sue Musk firms over Grok's sexualised images",
     "Several US states sue, alleging the AI chatbot generated sexualised images.",
     "AP", RED),
    (5, "AI GOVERNANCE", "UN chief wants AI risk rules within a year",
     "The secretary-general urges a global framework to manage AI risks.",
     "Manila Times", TEAL),
    (6, "DIPLOMACY", "India, China hold military talks in Arunachal",
     "Commanders meet to reduce tensions along the disputed border.",
     "Times of India", BLUE),
    (7, "ENVIRONMENT", "Gaza war leaves toxic contamination for decades",
     "Oxfam/CEOBS report: explosives poisoned air, soil and water.",
     "Disclosure News", TEAL),
    (8, "SPORT", "Gukesh defends chess title as Geneva opens",
     "India's Gukesh begins his defence against Uzbekistan's Sindarov.",
     "Times of India", GOLD),
    (9, "DISASTER", "6.7 quake hits Peru; no deaths reported",
     "A strong earthquake strikes Peru with no immediate deaths reported.",
     "Manila Times", INK),
    (10, "CONFLICT", "Houthis launch revenge strikes on Riyadh",
     "Houthi forces strike the Saudi capital in retaliation.",
     "Manila Times", RED),
    (11, "DIPLOMACY", "Taiwan warns Canada over deeper China ties",
     "Taipei cautions Ottawa that closer Beijing ties carry risks.",
     "Manila Times", BLUE),
]

# one-liners: (number, region, text)
ONELINERS = [
    (12, "US", "Vance tapped as Trump's emissary to Nvidia board."),
    (13, "US", "Nvidia faces a US accounting probe amid turmoil."),
    (14, "US", "Pentagon moves to restrict US-Canada defence ties."),
    (15, "US", "Trump vows to work with Democrats to cap card interest at 10%."),
    (16, "AS", "Rohingya hail ICJ genocide verdict against Myanmar."),
    (17, "AS", "11 dead after tainted alcohol in India's Manipur."),
    (18, "ME", "Iran strikes 3 tankers, shows off missile launchers."),
    (19, "AS", "North Korea ready to expand ties with other countries."),
    (20, "AS", "Nepal PM in India for economic, energy talks."),
    (21, "AS", "Thai court upholds verdict for opposition lawmaker."),
    (22, "AS", "More bodies found after Indonesia candy factory fire."),
    (23, "AF", "Drones hit homes and a UN building in Sudan's capital."),
    (24, "EU", "Thousands protest closure of Turkey media outlets."),
    (25, "EU", "Macron eyes constitutional changes to curb spending."),
    (26, "US", "Storms and airline glitches threaten Thanksgiving travel."),
    (27, "AS", "Modi opens AI centre at IIT Patna, Rs 400-crore park."),
    (28, "AS", "Russian cargo ship Sparta II ablaze after drone strike."),
    (29, "AS", "India's private-sector activity strengthens in November."),
    (30, "US", "Trump posts AI-edited Huang meme: 'I made the deal'."),
    (31, "US", "Trump signals possible healthcare deal with Democrats."),
    (32, "US", "Rocky Mountain Nutrition recalls powders over milk allergen."),
    (33, "US", "Bay Area flood watch as king tides threaten Thanksgiving."),
    (34, "EU", "Cruise survivors slam Schettino's early release."),
    (35, "AF", "Tinubu admits villa hit by power and water cuts."),
    (36, "WORLD", "CLAIM: Allies say Russia may launch a space weapon next month."),
    (37, "AS", "Restored Shuri Castle main hall reopens in Okinawa."),
    (38, "NA", "49ers rout Vikings in Mexico City; NFL slate ends."),
    (39, "AS", "Thailand to ban chemical exports over river pollution."),
    (40, "AS", "South Korea names new foreign, unification ministers."),
    (41, "AS", "China sets 2030 targets for elderly care, childcare."),
    (42, "AS", "CLAIM: WSJ — Trump's outreach to Kim was rebuffed."),
    (43, "AS", "Taliban strike women's names from Balkh documents."),
    (44, "EU", "India vs New Zealand first Test ends in a draw."),
]

# timeline: (hour_utc, label)
TIMELINE = [
    (0.75, "Peru quake"), (1.5, "Gomez out"), (2.0, "Huang back"),
    (5.5, "India-China"), (7.0, "Indonesia toll"),
    (9.5, "Kyiv strikes"), (11.0, "Houthis hit Riyadh"),
    (13.0, "UN AI call"), (15.0, "Sudan drones"),
    (17.0, "Trump card cap"), (19.0, "Chess opens"), (21.0, "Sue Musk"),
]

DATE_CHECK = [
    "COP31 ends with no deal — announced 23 Nov (BBC).",
    "Russian corvette sunk off Benghazi — 22 Nov.",
    "BepiColombo enters Mercury orbit — 21 Nov.",
    "Alcaraz wins ATP Finals — final played 22 Nov.",
    "Tamagotchi turns 30 — 23 Nov.",
    "Fiona the hippo dies, Cincinnati Zoo — 19 Nov.",
    "Ukraine warship-sinking claim — Monday 23 Nov.",
]

# map dots: (story number, lon, lat)
DOTS = [(1, -122, 37), (2, -77, 39), (3, 30.5, 50.5), (4, -100, 39),
        (5, -74, 41), (6, 94, 28), (7, 34.5, 31.5), (8, 6.1, 46.2),
        (9, -75, -10), (10, 46.7, 24.6), (11, 121, 25)]

CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 70),
     (-75, 62), (-60, 47), (-70, 42), (-80, 32), (-85, 25), (-97, 26),
     (-105, 20), (-110, 23), (-125, 40), (-145, 60), (-165, 60)],
    [(-80, 10), (-70, 11), (-60, 5), (-50, 0), (-40, -5), (-35, -10),
     (-40, -20), (-48, -28), (-58, -35), (-65, -40), (-70, -50), (-73, -35),
     (-75, -20), (-80, -5)],
    [(-10, 36), (-5, 43), (0, 50), (5, 58), (10, 57), (18, 56), (23, 60),
     (30, 70), (35, 68), (40, 60), (30, 50), (28, 45), (20, 40), (12, 44),
     (3, 42), (-2, 37), (-9, 38)],
    [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (30, 31), (35, 28),
     (40, 15), (48, 11), (51, 2), (40, -5), (35, -15), (30, -25), (20, -35),
     (15, -30), (12, -18), (9, -1), (8, 4), (-8, 5), (-15, 11)],
    [(40, 70), (50, 72), (60, 70), (70, 72), (80, 73), (90, 75), (110, 76),
     (130, 72), (150, 70), (170, 66), (178, 65), (170, 60), (160, 55),
     (155, 50), (145, 45), (140, 40), (135, 35), (130, 33), (127, 35),
     (122, 38), (120, 30), (110, 20), (108, 12), (105, 8), (100, 6),
     (97, 10), (95, 16), (90, 22), (85, 20), (80, 13), (77, 8), (72, 20),
     (66, 25), (60, 25), (55, 26), (50, 29), (48, 30), (44, 29), (40, 32),
     (38, 36), (35, 36), (30, 36), (27, 37), (23, 36), (26, 40), (28, 45),
     (30, 50), (32, 55), (35, 60), (38, 65)],
    [(113, -22), (114, -30), (115, -35), (120, -34), (129, -32), (137, -35),
     (140, -38), (145, -38), (150, -37), (153, -32), (153, -27), (150, -22),
     (146, -19), (142, -11), (137, -12), (132, -12), (126, -14), (122, -17),
     (118, -20)],
]


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap to a pixel width; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill=INK, leading=None):
    lh = leading if leading is not None else int(fnt.size * 1.25)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def draw_lead_art(draw, box, kind, accent):
    """Small programmatic illustration for a lead card."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=accent)
    if kind == "chip":
        # microchip with pins and a rising chart line
        cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
        draw.rectangle([cx - 42, cy - 26, cx + 42, cy + 26], fill=(255, 255, 255))
        draw.rectangle([cx - 42, cy - 26, cx + 42, cy + 26], outline=INK, width=2)
        for px in range(cx - 30, cx + 31, 15):
            draw.line([px, cy - 34, px, cy - 26], fill=(255, 255, 255), width=3)
            draw.line([px, cy + 26, px, cy + 34], fill=(255, 255, 255), width=3)
        for py in range(cy - 15, cy + 16, 15):
            draw.line([cx - 50, py, cx - 42, py], fill=(255, 255, 255), width=3)
            draw.line([cx + 42, py, cx + 50, py], fill=(255, 255, 255), width=3)
        draw.line([cx - 30, cy + 14, cx - 10, cy - 4, cx + 8, cy + 4, cx + 30, cy - 14],
                  fill=RED, width=4)
        draw.text((x0 + 10, y0 + 6), "+33%", font=F_TAG, fill=(255, 255, 255))
        draw.text((x1 - 52, y1 - 20), "NVDA", font=F_TAG, fill=(255, 255, 255))
    elif kind == "dome":
        cx = (x0 + x1) // 2
        base = y1 - 18
        draw.ellipse([cx - 34, base - 34, cx + 34, base + 2], fill=(255, 255, 255))
        draw.rectangle([cx - 40, base, cx + 40, base + 12], fill=(255, 255, 255))
        for i in range(5):
            px = cx - 32 + i * 16
            draw.rectangle([px, base - 22, px + 7, base], fill=(255, 255, 255))
        draw.rectangle([cx - 2, base - 52, cx + 2, base - 34], fill=(255, 255, 255))
        draw.text((x0 + 10, y0 + 6), "RESIGNS", font=F_TAG, fill=(255, 255, 255))
        draw.text((x1 - 58, y1 - 20), "DEC 1", font=F_TAG, fill=(255, 255, 255))
    else:  # "blast": skyline with radiating lines
        cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
        for k in range(8):
            ang = k * 45
            import math
            r = 46
            ex = cx + int(r * math.cos(math.radians(ang)))
            ey = cy + int(r * math.sin(math.radians(ang)))
            draw.line([cx, cy, ex, ey], fill=(255, 200, 90), width=3)
        draw.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=(255, 200, 90))
        for bx, bh in [(x0 + 18, 26), (x0 + 52, 40), (x0 + 92, 30), (x0 + 128, 46),
                       (x0 + 168, 34), (x0 + 204, 42), (x0 + 240, 28)]:
            draw.rectangle([bx, y1 - 16 - bh, bx + 26, y1 - 16], fill=(20, 20, 28))
        draw.text((x0 + 10, y0 + 6), "KYIV", font=F_TAG, fill=(255, 255, 255))
        dead = "14 DEAD"
        tw = draw.textlength(dead, font=F_TAG)
        draw.text((x1 - 8 - tw, y1 - 20), dead, font=F_TAG, fill=(255, 255, 255))


def draw_map(draw, x0, y0, x1, y1):
    def px(lon, lat):
        fx = (lon + 170.0) / 360.0
        fy = (85.0 - lat) / 145.0
        return (x0 + int(fx * (x1 - x0)), y0 + int(fy * (y1 - y0)))

    for poly in CONTINENTS:
        pts = [px(lon, lat) for lon, lat in poly]
        draw.polygon(pts, fill=MAPFILL, outline=MAPLINE)
    for num, lon, lat in DOTS:
        cx, cy = px(lon, lat)
        draw.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=RED, outline=(255, 255, 255), width=1)
        label = str(num)
        tw = draw.textlength(label, font=F_MAP_NUM)
        draw.text((cx - tw / 2, cy - 7), label, font=F_MAP_NUM, fill=(255, 255, 255))
    draw.text((x0, y1 - 12), "SCHEMATIC — NOT TO SCALE", font=F_TINY, fill=MUTED)


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 6], fill=RED)
    d.text((16, 14), "THE WORLD TODAY", font=F_TITLE, fill=INK)
    date_lines = ["TUESDAY", "24 NOVEMBER 2026"]
    dx = W - 16
    for i, line in enumerate(date_lines):
        tw = d.textlength(line, font=F_DATE)
        d.text((dx - tw, 16 + i * 24), line, font=F_DATE, fill=RED if i == 0 else INK)
    d.text((16, 66), "44 STORIES  ·  6 REGIONS  ·  ONE PAGE  —  TUESDAY 24 NOVEMBER 2026",
           font=F_SUB, fill=MUTED)
    d.line([16, 88, W - 16, 88], fill=INK, width=2)

    # ---- lead cards ----
    kinds = ["chip", "dome", "blast"]
    lead_y, lead_h, lead_w, gap = 96, 196, 322, 8
    for i, (num, region, head, summ, src, accent) in enumerate(LEADS):
        x0 = 16 + i * (lead_w + gap)
        x1 = x0 + lead_w
        d.rectangle([x0, lead_y, x1, lead_y + lead_h], fill=CARD, outline=LINE, width=1)
        draw_lead_art(d, (x0 + 1, lead_y + 1, x1 - 1, lead_y + 92), kinds[i], accent)
        y = lead_y + 98
        d.text((x0 + 10, y), f"{num} · {region}", font=F_TAG, fill=accent)
        y += 16
        lines = wrap(d, head, F_LEAD_HEAD, lead_w - 20)
        y = text_block(d, x0 + 10, y, lines[:2], F_LEAD_HEAD, leading=19)
        y += 3
        lines = wrap(d, summ, F_LEAD_SUM, lead_w - 20)
        y = text_block(d, x0 + 10, y, lines[:2], F_LEAD_SUM, leading=15)
        d.text((x0 + 10, y + 2), "Source: " + src, font=F_TINY, fill=MUTED)

    # ---- grid cards ----
    grid_y, grid_h, grid_w = 300, 104, 242
    for row in range(2):
        for col in range(4):
            item = GRID[row * 4 + col]
            num, region, head, summ, src, accent = item
            x0 = 16 + col * (grid_w + gap)
            x1 = x0 + grid_w
            y0 = grid_y + row * (grid_h + gap)
            d.rectangle([x0, y0, x1, y0 + grid_h], fill=CARD, outline=LINE, width=1)
            d.ellipse([x0 + 8, y0 + 8, x0 + 26, y0 + 26], fill=accent)
            label = str(num)
            tw = d.textlength(label, font=F_SMALL_B)
            d.text((x0 + 17 - tw / 2, y0 + 11), label, font=F_SMALL_B, fill=(255, 255, 255))
            d.text((x0 + 32, y0 + 10), region, font=F_TAG, fill=accent)
            lines = wrap(d, head, F_GRID_HEAD, grid_w - 16)
            y = text_block(d, x0 + 8, y0 + 30, lines[:2], F_GRID_HEAD, leading=14)
            lines = wrap(d, summ, F_GRID_SUM, grid_w - 16)
            text_block(d, x0 + 8, y + 2, lines[:2], F_GRID_SUM, leading=13)

    # ---- timeline strip ----
    tl_y0, tl_y1 = 524, 594
    d.rectangle([16, tl_y0, W - 16, tl_y1], fill=(255, 255, 255), outline=LINE, width=1)
    base = tl_y0 + 40
    d.line([24, base, W - 24, base], fill=INK, width=1)
    for h in range(0, 25, 4):
        x = 24 + int(h / 24.0 * (W - 48))
        d.line([x, base - 3, x, base + 3], fill=INK, width=1)
        lab = f"{h:02d}:00" + (" UTC" if h == 24 else "")
        tw = d.textlength(lab, font=F_TINY)
        lx = min(max(x - tw / 2, 24), W - 24 - tw)
        d.text((lx, base + 5), lab, font=F_TINY, fill=MUTED)
    # stagger event labels across three rows so neighbours never share one
    rows = {"near": base - 15, "below": base + 17, "far": base - 27}
    order = ["near", "below", "far"]
    for i, (hour, lab) in enumerate(TIMELINE):
        x = 24 + int(hour / 24.0 * (W - 48))
        d.ellipse([x - 3, base - 3, x + 3, base + 3], fill=RED)
        tw = d.textlength(lab, font=F_TINY)
        lx = min(max(x - tw / 2, 24), W - 24 - tw)
        d.text((lx, rows[order[i % 3]]), lab, font=F_TINY, fill=INK)

    # ---- one-liners (3 columns) ----
    ol_y0 = 602
    d.text((16, ol_y0), "THE REST OF THE DAY — 33 MORE STORIES", font=F_SECTION, fill=INK)
    d.line([16, ol_y0 + 17, 690, ol_y0 + 17], fill=INK, width=1)
    col_w, col_gap = 219, 7
    cols = [ONELINERS[i:i + 11] for i in range(0, 33, 11)]
    for ci, col in enumerate(cols):
        cx = 16 + ci * (col_w + col_gap)
        y = ol_y0 + 24
        for num, region, text in col:
            head = f"{num}. [{region}] "
            first = head + text
            lines = wrap(d, first, F_ONE, col_w)
            y = text_block(d, cx, y, lines[:2], F_ONE, leading=12)
            y += 4

    # ---- map ----
    map_x0, map_y0, map_x1, map_y1 = 698, 602, 1008, 772
    d.text((map_x0, map_y0), "WHERE IT HAPPENED — STORIES 1–11", font=F_SECTION, fill=INK)
    d.rectangle([map_x0, map_y0 + 20, map_x1, map_y1], fill=(255, 255, 255), outline=LINE, width=1)
    draw_map(d, map_x0 + 4, map_y0 + 24, map_x1 - 4, map_y1 - 4)

    # ---- date check ----
    dc_y0 = 782
    d.text((map_x0, dc_y0), "DATE CHECK — OLDER STORIES WE LEFT OUT", font=F_SECTION, fill=RED)
    d.line([map_x0, dc_y0 + 17, map_x1, dc_y0 + 17], fill=RED, width=1)
    y = dc_y0 + 24
    for item in DATE_CHECK:
        lines = wrap(d, "· " + item, F_SMALL, map_x1 - map_x0)
        y = text_block(d, map_x0, y, lines, F_SMALL, leading=13)
        y += 3
    y += 4
    lines = wrap(d, "Everything above happened, or was first reported, on 24 November 2026.",
                 F_SMALL, map_x1 - map_x0)
    text_block(d, map_x0, y, lines, F_SMALL, leading=13)

    # ---- footer ----
    d.line([16, 1010, W - 16, 1010], fill=LINE, width=1)
    d.text((16, 1014),
           "CLAIM = an unverified claim, attributed to its source.  Sources: AP · Japan Times · Manila Times · "
           "Sunday Guardian · Times of India · Disclosure News · Oxfam/CEOBS.",
           font=F_TINY, fill=MUTED)
    return img


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    render().save(out, "PNG", optimize=True)
    print("wrote", out)
