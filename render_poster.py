#!/usr/bin/env python3
"""Render the 24 November 2026 world-news poster, v2 (1024x1024 PNG).

Iteration on v1 (rank 73/9063, score 0.740839, round 2). Changes:
- 52 stories (was 44): 3 leads + 12 grid cards (was 8) + 37 one-liners.
- 7 regions (Oceania added via Solomon Islands treaty).
- Fixed lead art: Capitol dome now drawn with a dark outline so it reads as a
  building instead of a white blob; Kyiv blast gets a proper skyline with lit
  windows and a clearer burst.
- Map pins: true location shown as a small dot, numbered badge offset with a
  leader line where pins cluster (US east coast, Europe/Middle East).
- Timeline: "Sue Musk" replaced by the bigger "Huawei guilty" verdict (20:41 UTC).
- DATE CHECK trimmed to 4 items so the right column fits.
Deterministic: no network, no clock, no randomness. Renders entry.png.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 232)
INK = (25, 25, 25)
MUTED = (90, 86, 76)
RED = (166, 30, 30)
BLUE = (30, 78, 138)
NAVY = (16, 42, 84)
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
    (12, "TECH · LAW", "US jury finds Huawei guilty of trade-secret theft",
     "Huawei convicted of stealing trade secrets and bank fraud; acquitted of racketeering.",
     "AP", RED),
    (13, "SPACE", "China launches Shenzhou 24 with Pakistani astronaut",
     "Shenzhou 24 carries two Chinese and a Pakistani astronaut to Tiangong station.",
     "AP", TEAL),
    (14, "DIPLOMACY", "Solomon Islands names Australia top security partner",
     "New treaty makes Australia its primary security partner, excluding China.",
     "AP", BLUE),
    (15, "DISASTER", "Turkish military helicopter crash kills 5",
     "Air Force helicopter crashes after takeoff from Eskisehir on a training flight.",
     "AP", INK),
]

# one-liners: (number, region, text)
ONELINERS = [
    (16, "US", "Vance tapped as Trump's emissary to Nvidia board."),
    (17, "US", "Nvidia faces a US accounting probe amid turmoil."),
    (18, "US", "Pentagon moves to restrict US-Canada defence ties."),
    (19, "US", "Trump vows to work with Democrats to cap card interest at 10%."),
    (20, "AS", "Rohingya hail ICJ genocide verdict against Myanmar."),
    (21, "AS", "11 dead after tainted alcohol in India's Manipur."),
    (22, "ME", "Iran strikes 3 tankers, shows off missile launchers."),
    (23, "AS", "North Korea ready to expand ties with other countries."),
    (24, "AS", "Nepal PM in India for economic, energy talks."),
    (25, "AS", "Thai court upholds verdict for opposition lawmaker."),
    (26, "AS", "More bodies found after Indonesia candy factory fire."),
    (27, "AF", "Drones hit homes and a UN building in Sudan's capital."),
    (28, "EU", "Thousands protest closure of Turkey media outlets."),
    (29, "EU", "Macron eyes constitutional changes to curb spending."),
    (30, "US", "Storms and airline glitches threaten Thanksgiving travel."),
    (31, "AS", "Modi opens AI centre at IIT Patna, Rs 400-crore park."),
    (32, "AS", "Russian cargo ship Sparta II ablaze after drone strike."),
    (33, "AS", "India's private-sector activity strengthens in November."),
    (34, "US", "Trump posts AI-edited Huang meme: 'I made the deal'."),
    (35, "US", "Trump signals possible healthcare deal with Democrats."),
    (36, "US", "Rocky Mountain Nutrition recalls powders over milk allergen."),
    (37, "US", "Bay Area flood watch as king tides threaten Thanksgiving."),
    (38, "EU", "Cruise survivors slam Schettino's early release."),
    (39, "AF", "Tinubu admits villa hit by power and water cuts."),
    (40, "WORLD", "CLAIM: Allies say Russia may launch a space weapon next month."),
    (41, "AS", "Restored Shuri Castle main hall reopens in Okinawa."),
    (42, "NA", "49ers rout Vikings in Mexico City; NFL slate ends."),
    (43, "AS", "Thailand to ban chemical exports over river pollution."),
    (44, "AS", "South Korea names new foreign, unification ministers."),
    (45, "AS", "China sets 2030 targets for elderly care, childcare."),
    (46, "AS", "CLAIM: WSJ — Trump's outreach to Kim was rebuffed."),
    (47, "AS", "Taliban strike women's names from Balkh documents."),
    (48, "EU", "India vs New Zealand first Test ends in a draw."),
    (49, "WORLD", "UN: five women killed every hour by a partner or family member."),
    (50, "AF", "Fighting traps Ebola responders inside a DR Congo hospital."),
    (51, "LATAM", "Car bomb destroys buildings in Colombian city; no deaths confirmed."),
    (52, "AS", "Blast at Hanoi hot-pot eatery kills 6, injures over a dozen."),
]

# timeline: (hour_utc, label)
TIMELINE = [
    (0.75, "Peru quake"), (1.5, "Gomez out"), (2.0, "Huang back"),
    (5.5, "India-China"), (7.0, "Indonesia toll"),
    (9.5, "Kyiv strikes"), (11.0, "Houthis hit Riyadh"),
    (13.0, "UN AI call"), (15.0, "Sudan drones"),
    (17.0, "Trump card cap"), (19.0, "Chess opens"), (20.7, "Huawei guilty"),
]

DATE_CHECK = [
    "COP31 ends with no deal — announced 23 Nov (BBC).",
    "Russian corvette sunk off Benghazi — 22 Nov.",
    "BepiColombo enters Mercury orbit — 21 Nov.",
    "Alcaraz wins ATP Finals — final played 22 Nov.",
]

# map dots: (story number, lon, lat, badge_dx, badge_dy)
DOTS = [(1, -122, 37, 0, 0), (2, -77, 39, -18, 10), (3, 30.5, 50.5, 0, -15),
        (4, -100, 39, 12, -10), (5, -74, 41, 16, -12), (6, 94, 28, 0, 0),
        (7, 34.5, 31.5, 20, 10), (8, 6.1, 46.2, 0, 0), (9, -75, -10, 0, 0),
        (10, 46.7, 24.6, 14, -8), (11, 121, 25, 0, 0), (12, -74, 40.7, 2, 15),
        (13, 100, 41, 0, 0), (14, 160, -9.5, 0, 0), (15, 30.5, 39.8, -18, 6)]

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
        cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
        draw.rectangle([cx - 42, cy - 24, cx + 42, cy + 24], fill=(255, 255, 255))
        draw.rectangle([cx - 42, cy - 24, cx + 42, cy + 24], outline=INK, width=2)
        for px in range(cx - 30, cx + 31, 15):
            draw.line([px, cy - 31, px, cy - 24], fill=(255, 255, 255), width=3)
            draw.line([px, cy + 24, px, cy + 31], fill=(255, 255, 255), width=3)
        for py in range(cy - 12, cy + 13, 12):
            draw.line([cx - 49, py, cx - 42, py], fill=(255, 255, 255), width=3)
            draw.line([cx + 42, py, cx + 49, py], fill=(255, 255, 255), width=3)
        draw.line([cx - 30, cy + 13, cx - 10, cy - 3, cx + 8, cy + 3, cx + 30, cy - 13],
                  fill=RED, width=4)
        draw.text((x0 + 10, y0 + 6), "+33%", font=F_TAG, fill=(255, 255, 255))
        draw.text((x1 - 52, y1 - 20), "NVDA", font=F_TAG, fill=(255, 255, 255))
    elif kind == "dome":
        # US Capitol: white dome + columns, outlined in dark navy so it reads
        # as a building against the blue field (v1 was an unoutlined blob).
        cx = (x0 + x1) // 2
        base = y1 - 14
        # dome
        draw.ellipse([cx - 30, base - 34, cx + 30, base + 2], fill=(255, 255, 255),
                     outline=NAVY, width=2)
        draw.rectangle([cx - 34, base - 6, cx + 34, base], fill=(255, 255, 255),
                       outline=NAVY, width=2)
        # lantern + flag pole
        draw.rectangle([cx - 5, base - 44, cx + 5, base - 34], fill=(255, 255, 255),
                       outline=NAVY, width=1)
        draw.line([cx, base - 56, cx, base - 44], fill=(255, 255, 255), width=2)
        draw.polygon([(cx, base - 56), (cx + 12, base - 53), (cx, base - 50)],
                     fill=(255, 255, 255), outline=NAVY)
        # colonnade: navy columns on white entablature
        draw.rectangle([cx - 44, base - 2, cx + 44, base + 10], fill=(255, 255, 255),
                       outline=NAVY, width=2)
        for i in range(6):
            px = cx - 38 + i * 14
            draw.rectangle([px, base - 2, px + 5, base + 10], fill=NAVY)
        draw.rectangle([cx - 48, base + 10, cx + 48, base + 14], fill=(255, 255, 255),
                       outline=NAVY, width=1)
        draw.text((x0 + 10, y0 + 6), "RESIGNS", font=F_TAG, fill=(255, 255, 255))
        draw.text((x1 - 58, y1 - 20), "DEC 1", font=F_TAG, fill=(255, 255, 255))
    else:  # "blast": orange burst over a Kyiv skyline with lit windows
        cx, cy = (x0 + x1) // 2, (y0 + y1) // 2 - 6
        for k in range(8):
            ang = k * 45 + 10
            r = 40
            ex = cx + int(r * math.cos(math.radians(ang)))
            ey = cy + int(r * math.sin(math.radians(ang)))
            draw.line([cx, cy, ex, ey], fill=(255, 190, 80), width=3)
        draw.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=(255, 210, 110),
                     outline=(255, 255, 255), width=2)
        draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(255, 255, 255))
        # skyline: grey towers with lit windows, ground line
        towers = [(x0 + 14, 22), (x0 + 46, 34), (x0 + 82, 26), (x0 + 116, 40),
                  (x0 + 152, 30), (x0 + 188, 38), (x0 + 224, 24), (x0 + 258, 32)]
        for bx, bh in towers:
            draw.rectangle([bx, y1 - 12 - bh, bx + 24, y1 - 12], fill=(70, 70, 82),
                           outline=(25, 25, 25), width=1)
            for wy in range(y1 - 12 - bh + 5, y1 - 14, 9):
                for wx in (bx + 5, bx + 14):
                    draw.rectangle([wx, wy, wx + 3, wy + 3], fill=(255, 200, 90))
        draw.line([x0, y1 - 12, x1, y1 - 12], fill=(25, 25, 25), width=2)
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
    for num, lon, lat, dx, dy in DOTS:
        cx, cy = px(lon, lat)
        bx, by = cx + dx, cy + dy
        # true-location dot
        draw.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=RED)
        if dx or dy:
            draw.line([cx, cy, bx, by], fill=RED, width=1)
        draw.ellipse([bx - 9, by - 9, bx + 9, by + 9], fill=RED,
                     outline=(255, 255, 255), width=1)
        label = str(num)
        tw = draw.textlength(label, font=F_MAP_NUM)
        draw.text((bx - tw / 2, by - 7), label, font=F_MAP_NUM, fill=(255, 255, 255))
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
    d.text((16, 66), "52 STORIES  ·  7 REGIONS  ·  ONE PAGE  —  TUESDAY 24 NOVEMBER 2026",
           font=F_SUB, fill=MUTED)
    d.line([16, 88, W - 16, 88], fill=INK, width=2)

    # ---- lead cards ----
    kinds = ["chip", "dome", "blast"]
    lead_y, lead_h, lead_w, gap = 96, 184, 322, 8
    for i, (num, region, head, summ, src, accent) in enumerate(LEADS):
        x0 = 16 + i * (lead_w + gap)
        x1 = x0 + lead_w
        d.rectangle([x0, lead_y, x1, lead_y + lead_h], fill=CARD, outline=LINE, width=1)
        draw_lead_art(d, (x0 + 1, lead_y + 1, x1 - 1, lead_y + 80), kinds[i], accent)
        y = lead_y + 86
        d.text((x0 + 10, y), f"{num} · {region}", font=F_TAG, fill=accent)
        y += 16
        lines = wrap(d, head, F_LEAD_HEAD, lead_w - 20)
        y = text_block(d, x0 + 10, y, lines[:2], F_LEAD_HEAD, leading=19)
        y += 3
        lines = wrap(d, summ, F_LEAD_SUM, lead_w - 20)
        y = text_block(d, x0 + 10, y, lines[:2], F_LEAD_SUM, leading=15)
        d.text((x0 + 10, y + 2), "Source: " + src, font=F_TINY, fill=MUTED)

    # ---- grid cards (3 rows x 4) ----
    grid_y, grid_h, grid_w = 288, 96, 242
    for row in range(3):
        for col in range(4):
            item = GRID[row * 4 + col]
            num, region, head, summ, src, accent = item
            x0 = 16 + col * (grid_w + gap)
            x1 = x0 + grid_w
            y0 = grid_y + row * (grid_h + 6)
            d.rectangle([x0, y0, x1, y0 + grid_h], fill=CARD, outline=LINE, width=1)
            d.ellipse([x0 + 8, y0 + 7, x0 + 26, y0 + 25], fill=accent)
            label = str(num)
            tw = d.textlength(label, font=F_SMALL_B)
            d.text((x0 + 17 - tw / 2, y0 + 10), label, font=F_SMALL_B, fill=(255, 255, 255))
            d.text((x0 + 32, y0 + 9), region, font=F_TAG, fill=accent)
            lines = wrap(d, head, F_GRID_HEAD, grid_w - 16)
            y = text_block(d, x0 + 8, y0 + 28, lines[:2], F_GRID_HEAD, leading=13)
            lines = wrap(d, summ, F_GRID_SUM, grid_w - 16)
            text_block(d, x0 + 8, y + 2, lines[:2], F_GRID_SUM, leading=12)

    # ---- timeline strip ----
    tl_y0, tl_y1 = 596, 656
    d.rectangle([16, tl_y0, W - 16, tl_y1], fill=(255, 255, 255), outline=LINE, width=1)
    base = tl_y0 + 32
    d.line([24, base, W - 24, base], fill=INK, width=1)
    for h in range(0, 25, 4):
        x = 24 + int(h / 24.0 * (W - 48))
        d.line([x, base - 3, x, base + 3], fill=INK, width=1)
        lab = f"{h:02d}:00" + (" UTC" if h == 24 else "")
        tw = d.textlength(lab, font=F_TINY)
        lx = min(max(x - tw / 2, 24), W - 24 - tw)
        d.text((lx, base + 6), lab, font=F_TINY, fill=MUTED)
    # stagger event labels across three rows so neighbours never share one
    rows = {"near": base - 13, "below": base + 18, "far": base - 25}
    order = ["near", "below", "far"]
    for i, (hour, lab) in enumerate(TIMELINE):
        x = 24 + int(hour / 24.0 * (W - 48))
        d.ellipse([x - 3, base - 3, x + 3, base + 3], fill=RED)
        tw = d.textlength(lab, font=F_TINY)
        lx = min(max(x - tw / 2, 24), W - 24 - tw)
        d.text((lx, rows[order[i % 3]]), lab, font=F_TINY, fill=INK)

    # ---- one-liners (3 columns) ----
    ol_y0 = 664
    d.text((16, ol_y0), "THE REST OF THE DAY — 37 MORE STORIES", font=F_SECTION, fill=INK)
    d.line([16, ol_y0 + 17, 690, ol_y0 + 17], fill=INK, width=1)
    col_w, col_gap = 219, 7
    cols = [ONELINERS[0:13], ONELINERS[13:25], ONELINERS[25:37]]
    for ci, col in enumerate(cols):
        cx = 16 + ci * (col_w + col_gap)
        y = ol_y0 + 24
        for num, region, text in col:
            first = f"{num}. [{region}] " + text
            lines = wrap(d, first, F_ONE, col_w)
            y = text_block(d, cx, y, lines[:2], F_ONE, leading=11)
            y += 2

    # ---- map ----
    map_x0, map_y0, map_x1, map_y1 = 698, 664, 1008, 836
    d.text((map_x0, map_y0), "WHERE IT HAPPENED — STORIES 1–15", font=F_SECTION, fill=INK)
    d.rectangle([map_x0, map_y0 + 20, map_x1, map_y1], fill=(255, 255, 255), outline=LINE, width=1)
    draw_map(d, map_x0 + 4, map_y0 + 24, map_x1 - 4, map_y1 - 4)

    # ---- date check ----
    dc_y0 = 846
    d.text((map_x0, dc_y0), "DATE CHECK — OLDER STORIES WE LEFT OUT", font=F_SECTION, fill=RED)
    d.line([map_x0, dc_y0 + 17, map_x1, dc_y0 + 17], fill=RED, width=1)
    y = dc_y0 + 24
    for item in DATE_CHECK:
        lines = wrap(d, "· " + item, F_SMALL, map_x1 - map_x0)
        y = text_block(d, map_x0, y, lines, F_SMALL, leading=12)
        y += 3
    y += 4
    lines = wrap(d, "Everything above happened, or was first reported, on 24 November 2026.",
                 F_SMALL, map_x1 - map_x0)
    text_block(d, map_x0, y, lines, F_SMALL, leading=12)

    # ---- footer ----
    d.line([16, 1008, W - 16, 1008], fill=LINE, width=1)
    d.text((16, 1012),
           "CLAIM = an unverified claim, attributed to its source.  Sources: AP · AFP · Japan Times · "
           "Manila Times · Sunday Guardian · Times of India · Disclosure News · UN News · Oxfam/CEOBS.",
           font=F_TINY, fill=MUTED)
    return img


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    render().save(out, "PNG", optimize=True)
    print("wrote", out)
