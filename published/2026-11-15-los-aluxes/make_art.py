#!/usr/bin/env python3
"""Illustrations for 'Los Aluxes' — writes art/*.svg (2400x1350).
Render: node /home/claude/pipeline/render_svg.js art/*.svg      Usage: python3 make_art.py [name ...]"""
import sys, os, math, random
sys.path.insert(0, '/home/claude/pipeline'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from helpers import *                      # fogon, interior, man_sil, woman_sil, moon_sky… (previous videos)
from scenery import mist, maguey, adobe
from chars import (tomas_head, fermin_head, lupe_head, shirt_body, blouse_body, bust_frame, rebozo_head, braids,
                   SK_TOMAS, SK_OLD, SK_LUPE, sombrero, hair_short, mustache, wrinkles)
from base_chars import uid, grad_lin, grad_rad, hand_open
from yuc_art import yuc_night, monte, chaca, maya_house, sac_path, hammock, ceiba, agave
import yuc_art
from alux import alux_head, alux_full, trompo_svg, SK_CLAY, SK_ALUX

ART = {}
def art(fn):
    ART[fn.__name__] = fn
    return fn

G = lambda x, y, k, f, flip=False: f'<g transform="translate({x},{y}) scale({-k if flip else k},{k})">{f}</g>'
R = lambda c="#000", op=1.0: f'<rect width="2400" height="1350" fill="{c}" opacity="{op}"/>'
MOONRIM = "#9fc8e8"; WARM = "#ffcf8a"


# ------------------------------------------------------------------ milpa pieces
def corn(x, y, h=420, seed=1, color="#0c1a12", rim=None, ears=True, w=9, bitten=False):
    r = random.Random(seed); s = ""
    tx = x + r.uniform(-14, 14)
    s += f'<path d="M{x:.0f},{y:.0f} Q{(x+tx)/2+r.uniform(-8,8):.0f},{y-h/2:.0f} {tx:.0f},{y-h:.0f}" stroke="{color}" stroke-width="{w}" fill="none"/>'
    for j in range(6):  # long arching leaves
        t = 0.18 + j * 0.13; px = x + (tx - x) * t; py = y - h * t; sd = 1 if (j + seed) % 2 else -1
        L = h * r.uniform(0.35, 0.55)
        s += (f'<path d="M{px:.0f},{py:.0f} Q{px+sd*L*0.5:.0f},{py-L*0.45:.0f} {px+sd*L:.0f},{py+L*0.15:.0f} '
              f'Q{px+sd*L*0.5:.0f},{py-L*0.3:.0f} {px:.0f},{py+8:.0f} Z" fill="{color}"/>')
        if rim and sd > 0:
            s += f'<path d="M{px:.0f},{py:.0f} Q{px+sd*L*0.5:.0f},{py-L*0.45:.0f} {px+sd*L:.0f},{py+L*0.15:.0f}" stroke="{rim}" stroke-width="2.5" fill="none" opacity="0.45"/>'
    # tassel
    for k in range(5):
        s += f'<path d="M{tx:.0f},{y-h:.0f} l{r.uniform(-30,30):.0f},{-r.uniform(30,60):.0f}" stroke="{color}" stroke-width="3"/>'
    if ears:
        ey = y - h * 0.5
        s += f'<path d="M{x+4:.0f},{ey:.0f} C{x+40:.0f},{ey-20:.0f} {x+50:.0f},{ey-80:.0f} {x+30:.0f},{ey-110:.0f} C{x+10:.0f},{ey-80:.0f} {x:.0f},{ey-40:.0f} {x+4:.0f},{ey:.0f} Z" fill="{color}"/>'
        if bitten:
            s += f'<path d="M{x+30:.0f},{ey-110:.0f} l14,-30" stroke="#d8c070" stroke-width="10"/>'
    return s


def milpa_row(y, n=30, hmin=300, hmax=460, color="#0c1a12", rim=None, seed=1, x0=-50, x1=2450, w=9):
    r = random.Random(seed); s = ""
    for i in range(n):
        x = x0 + (x1 - x0) * (i + r.uniform(0, 0.8)) / n
        s += corn(x, y + r.uniform(-10, 10), r.uniform(hmin, hmax), seed * 100 + i, color, rim, w=w)
    return s


def stones(x0, x1, y0, y1, n=40, seed=1, col="#8a8a84", rmax=12):
    r = random.Random(seed); s = ""
    for _ in range(n):
        x, y = r.uniform(x0, x1), r.uniform(y0, y1); rr = r.uniform(4, rmax)
        s += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rr:.1f}" ry="{rr*0.8:.1f}" fill="{col}"/><ellipse cx="{x-rr*0.3:.0f}" cy="{y-rr*0.3:.0f}" rx="{rr*0.35:.1f}" ry="{rr*0.25:.1f}" fill="#e8e8e0" opacity="0.5"/>'
    return s


def kahtal(x, base, k=1.0, overgrown=False, door="closed", lit=False, rim=MOONRIM, day=False):
    """Little stone house of the alux: dry-stone walls, palm roof, a small dark door."""
    r = random.Random(int(x)); s = ""
    w, h = 260 * k, 200 * k
    stone = "#5a5e5c" if day else "#252b2c"
    s += f'<rect x="{x-w/2:.0f}" y="{base-h:.0f}" width="{w:.0f}" height="{h:.0f}" fill="{stone}"/>'
    for row in range(7):
        yy = base - h + row * h / 7
        xx = x - w / 2 + (row % 2) * 18 * k
        while xx < x + w / 2 - 10:
            sw = r.uniform(30, 52) * k
            c = r.choice(("#6e7270", "#7e807a", "#5e625e")) if day else r.choice(("#2e3436", "#363c3c", "#1e2224"))
            s += f'<rect x="{xx:.0f}" y="{yy+2:.0f}" width="{min(sw, x+w/2-xx):.0f}" height="{h/7-4:.0f}" rx="{6*k:.0f}" fill="{c}"/>'
            xx += sw + 4
    # palm roof
    s += f'<path d="M{x-w/2-50*k:.0f},{base-h+10*k:.0f} L{x:.0f},{base-h-150*k:.0f} L{x+w/2+50*k:.0f},{base-h+10*k:.0f} Z" fill="{"#6a5430" if day else "#1a1610"}"/>'
    for i in range(40):
        u = r.uniform(-1, 1)
        s += f'<path d="M{x+u*(w/2+50*k):.0f},{base-h+10*k:.0f} L{x+u*14*k:.0f},{base-h-140*k:.0f}" stroke="{"#8a7044" if day else "#2a2418"}" stroke-width="2" opacity="0.7"/>'
    if rim:
        s += f'<path d="M{x:.0f},{base-h-150*k:.0f} L{x+w/2+50*k:.0f},{base-h+10*k:.0f}" stroke="{rim}" stroke-width="4" opacity="0.6"/>'
        s += f'<path d="M{x+w/2:.0f},{base-h:.0f} L{x+w/2:.0f},{base:.0f}" stroke="{rim}" stroke-width="4" opacity="0.4"/>'
    dw, dh = 70 * k, 100 * k
    if door == "closed":
        s += f'<rect x="{x-dw/2:.0f}" y="{base-dh:.0f}" width="{dw:.0f}" height="{dh:.0f}" fill="#3a2614"/><path d="M{x:.0f},{base-dh:.0f} l0,{dh:.0f}" stroke="#1a0e06" stroke-width="3"/>'
    elif door == "open":
        s += f'<rect x="{x-dw/2:.0f}" y="{base-dh:.0f}" width="{dw:.0f}" height="{dh:.0f}" fill="#020202"/>'
    elif door == "fallen":
        s += f'<rect x="{x-dw/2:.0f}" y="{base-dh:.0f}" width="{dw:.0f}" height="{dh:.0f}" fill="#020202"/>'
        s += f'<path d="M{x-dw/2-20:.0f},{base:.0f} L{x+dw/2+30:.0f},{base-14:.0f} L{x+dw/2+36:.0f},{base+6:.0f} L{x-dw/2-14:.0f},{base+16:.0f} Z" fill="#3a2614"/>'
    if lit:
        s += glow(x, base - dh / 2, 160 * k, "warm", 0.6)
    if overgrown:
        for i in range(60):
            gx = x + r.uniform(-w / 2 - 80, w / 2 + 80); gh = r.uniform(30, 150) * k
            s += f'<path d="M{gx:.0f},{base+6:.0f} q{r.uniform(-20,20):.0f},{-gh/2:.0f} {r.uniform(-40,40):.0f},{-gh:.0f}" stroke="{"#4a6a3a" if day else "#0c1a12"}" stroke-width="{r.uniform(3,7):.0f}" fill="none"/>'
        for i in range(8):  # creeping vine over the wall
            vx = x + r.uniform(-w / 2, w / 2)
            s += f'<path d="M{vx:.0f},{base:.0f} C{vx+30:.0f},{base-h*0.4:.0f} {vx-30:.0f},{base-h*0.7:.0f} {vx+r.uniform(-40,40):.0f},{base-h-20:.0f}" stroke="{"#3a5a2a" if day else "#081410"}" stroke-width="5" fill="none"/>'
    return s


def jicara(x, y, k=1.0, full=True, col="#3a2414"):
    s = f'<path d="M{x-60*k:.0f},{y:.0f} C{x-60*k:.0f},{y+60*k:.0f} {x+60*k:.0f},{y+60*k:.0f} {x+60*k:.0f},{y:.0f} Z" fill="{col}"/>'
    s += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{60*k:.0f}" ry="{14*k:.0f}" fill="{"#e8dcc0" if full else "#120a04"}"/>'
    s += f'<path d="M{x-50*k:.0f},{y+20*k:.0f} C{x-20*k:.0f},{y+40*k:.0f} {x+20*k:.0f},{y+40*k:.0f} {x+50*k:.0f},{y+20*k:.0f}" stroke="#7a5030" stroke-width="{3*k:.1f}" fill="none"/>'
    return s


def champa(x, base, k=1.0, lit=True, rim=MOONRIM):
    """Open field shelter: four poles, palm roof, hammock inside."""
    s = ""; w, h = 500 * k, 300 * k
    for px in (x - w / 2, x + w / 2):
        s += f'<path d="M{px:.0f},{base:.0f} L{px:.0f},{base-h:.0f}" stroke="#0a0806" stroke-width="{16*k:.0f}"/>'
    s += f'<path d="M{x-w/2:.0f},{base-h*0.7:.0f} Q{x:.0f},{base-h*0.3:.0f} {x+w/2:.0f},{base-h*0.7:.0f}" stroke="#7a2a24" stroke-width="{10*k:.0f}" fill="none"/>'
    s += f'<path d="M{x-w/2-90*k:.0f},{base-h+20*k:.0f} L{x:.0f},{base-h-200*k:.0f} L{x+w/2+90*k:.0f},{base-h+20*k:.0f} Z" fill="#14100a"/>'
    r = random.Random(5)
    for i in range(50):
        u = r.uniform(-1, 1)
        s += f'<path d="M{x+u*(w/2+90*k):.0f},{base-h+20*k:.0f} L{x+u*20*k:.0f},{base-h-190*k:.0f}" stroke="#2a2214" stroke-width="2" opacity="0.6"/>'
    if rim:
        s += f'<path d="M{x:.0f},{base-h-200*k:.0f} L{x+w/2+90*k:.0f},{base-h+20*k:.0f}" stroke="{rim}" stroke-width="4" opacity="0.55"/>'
    if lit:
        s += f'<ellipse cx="{x+60*k:.0f}" cy="{base-10:.0f}" rx="{40*k:.0f}" ry="{12*k:.0f}" fill="#ff7a2a"/>' + glow(x + 60 * k, base - 40 * k, 260 * k, "warm", 0.7)
    return s


def eusebio_bust(x, y, k=1.0, rim=MOONRIM, hat=True, age="man", **hk):
    g = uid("eu")
    body = shirt_body(g, SK_TOMAS, rim, cloth=("#6a6a62", "#d8d4c8", "#f4f0e4"), sarape=False)
    if age == "young":
        hk.setdefault("smile", 0.5)
    return bust_frame(body, tomas_head(rim=rim, hat=hat, **hk), x, y, k)


def abuelo_bust(x, y, k=1.0, rim=WARM, hat=True, **hk):
    g = uid("an")
    body = shirt_body(g, SK_OLD, rim, cloth=("#5e5a50", "#cfc8b6", "#ece6d6"), sarape=False)
    return bust_frame(body, fermin_head(rim=rim, hat=hat, **hk), x, y, k)


def hmen_bust(x, y, k=1.0, rim=WARM, **hk):
    g = uid("hm")
    body = shirt_body(g, SK_OLD, rim, cloth=("#4e4a42", "#bdb6a4", "#dcd6c4"), sarape=False)
    body += '<path d="M-60,240 C-30,300 30,300 60,240" stroke="#1a6a5a" stroke-width="10" fill="none"/>'  # jade/bead necklace
    for i in range(9):
        t = (i - 4) / 4; body += f'<circle cx="{t*58:.0f}" cy="{262+22*(1-t*t):.0f}" r="9" fill="#2a8a6a"/>'
    h = fermin_head(rim=rim, hat=False, **hk)
    h += '<path d="M-84,-80 C-40,-100 40,-100 84,-80 L84,-64 C40,-84 -40,-84 -84,-64 Z" fill="#e8e0cc"/>'  # white headband
    return bust_frame(body, h, x, y, k)


def juana_bust(x, y, k=1.0, rim=WARM, **hk):
    g = uid("ju")
    back = rebozo_head(color="#5a2a3a", dk="#2a0e18", hi="#8a4a5a", stripe="#d8b8a0")
    return bust_frame(blouse_body(g, SK_LUPE, rim, rebozo=("#5a2a3a", "#2a0e18", "#8a4a5a")),
                      lupe_head(rim=rim, rebozo=False, **hk), x, y, k, back=back + braids())


def child_sil(x, y, h=360, color="#04060a", rim=MOONRIM, facing=1, hand_up=False):
    k = h / 360
    s = f'<g transform="translate({x},{y}) scale({k*facing},{k})">'
    s += f'<path d="M-40,-230 C-50,-160 -46,-110 -36,-100 L-40,0 L-14,0 L0,-96 L14,0 L40,0 L36,-100 C46,-110 50,-160 40,-230 C30,-250 -30,-250 -40,-230 Z" fill="{color}"/>'
    s += f'<circle cx="0" cy="-275" r="40" fill="{color}"/>'
    s += f'<path d="M-36,-270 C-40,-310 -10,-322 0,-318 C20,-322 44,-300 38,-268" fill="{color}"/>'
    if hand_up:
        s += f'<path d="M36,-220 C70,-200 90,-170 104,-140" stroke="{color}" stroke-width="22" stroke-linecap="round" fill="none"/>'
    else:
        s += f'<path d="M36,-220 C54,-180 58,-150 52,-120" stroke="{color}" stroke-width="22" stroke-linecap="round" fill="none"/>'
    s += f'<path d="M-36,-220 C-54,-180 -58,-150 -52,-120" stroke="{color}" stroke-width="22" stroke-linecap="round" fill="none"/>'
    if rim:
        s += f'<path d="M40,-230 C50,-160 46,-110 36,-100 L40,0 M38,-268 C44,-300 20,-322 0,-318" stroke="{rim}" stroke-width="4" fill="none" opacity="0.6"/>'
    s += '</g>'
    return s


def night_milpa_base(seed=1, mx=1800, my=250, r=100):
    s = yuc_night(seed, mx, my, r)
    s += monte(820, "#061418", seed + 2, 200, 40) + mist(800, 90, 0.3, "#9ab8c4", seed)
    s += '<path d="M0,900 L2400,880 L2400,1350 L0,1350 Z" fill="#070d0c"/>'
    return s


# ================================================================== NIGHT MILPA / CASITA
@art
def milpa_night():
    s = night_milpa_base(1, 1750, 240, 100)
    s += milpa_row(900, 40, 160, 240, "#0a1a14", MOONRIM, 1, w=5)
    s += champa(500, 940, 0.45, lit=True)
    s += milpa_row(1050, 30, 300, 420, "#071210", MOONRIM, 2, w=8)
    s += mist(1000, 120, 0.25, "#a8c8c0", 4)
    s += milpa_row(1300, 22, 500, 700, "#030807", MOONRIM, 3, w=12)
    return svg(s)


@art
def milpa_day():
    s = sky("#7aa0b8", "#f0dca8") + glow(1900, 300, 600, "warm", 0.6)
    s += monte(800, "#3a5a48", 2, 200, 40) + mist(780, 80, 0.4, "#f0ece0", 2)
    s += '<path d="M0,880 L2400,860 L2400,1350 L0,1350 Z" fill="#8a7a52"/>'
    s += milpa_row(900, 40, 160, 240, "#4a7a3a", "#e8f0a0", 1, w=5)
    s += kahtal(1900, 940, 0.5, day=True, rim=None)
    s += milpa_row(1060, 30, 300, 420, "#3a6a2e", "#e8f0a0", 2, w=8)
    s += milpa_row(1320, 22, 500, 700, "#2a5222", "#d8e890", 3, w=12)
    return svg(s)


@art
def title_bg():
    s = night_milpa_base(7, 1200, 260, 130)
    s += milpa_row(900, 40, 160, 240, "#0a1a14", MOONRIM, 5, w=5)
    s += kahtal(1200, 1010, 1.0, lit=True)
    s += milpa_row(1200, 26, 360, 520, "#030807", MOONRIM, 6, w=10, x0=-100, x1=800)
    s += milpa_row(1200, 26, 360, 520, "#030807", MOONRIM, 7, w=10, x0=1600, x1=2500)
    s += mist(1100, 120, 0.3, "#b8d0d0", 3) + R("#000", 0.12)
    return svg(s)


@art
def casita_alux():
    s = night_milpa_base(3, 1900, 230, 90)
    s += monte(950, "#030a0c", 9, 300, 30)
    s += '<path d="M0,1080 L2400,1060 L2400,1350 L0,1350 Z" fill="#060a0a"/>'
    s += kahtal(1250, 1100, 1.4)
    s += jicara(1250, 1150, 0.5, full=False)
    s += milpa_row(1350, 18, 500, 700, "#020605", MOONRIM, 9, w=12, x0=-100, x1=700)
    s += milpa_row(1350, 10, 500, 700, "#020605", MOONRIM, 10, w=12, x0=1900, x1=2500)
    s += mist(1150, 110, 0.25, "#b0c8c8", 5)
    return svg(s)


@art
def casita_close():
    s = yuc_night(4, 400, 200, 70) + monte(700, "#030a0c", 9, 300, 30)
    s += '<path d="M0,1150 L2400,1130 L2400,1350 L0,1350 Z" fill="#060a0a"/>'
    s += kahtal(1200, 1200, 3.0, overgrown=True)
    s += mist(1250, 100, 0.3, "#b0c8c8", 6)
    return svg(s)


@art
def casita_dark():
    s = R("#010203")
    s += '<rect x="700" y="250" width="1000" height="1100" fill="#141a1c"/>'
    r = random.Random(3)
    for row in range(10):
        y = 250 + row * 110; xx = 700 + (row % 2) * 60
        while xx < 1700:
            w = r.uniform(110, 190)
            s += f'<rect x="{xx:.0f}" y="{y+4:.0f}" width="{min(w,1700-xx):.0f}" height="102" rx="16" fill="{r.choice(("#1c2224","#22282a","#181c1e"))}"/>'
            xx += w + 8
    s += '<rect x="960" y="560" width="480" height="790" fill="#000"/>'
    s += f'<path d="M960,560 L960,1350 M1440,560 L1440,1350" stroke="{MOONRIM}" stroke-width="5" opacity="0.4"/>'
    s += glow(1200, 1100, 300, "moon", 0.12)
    return svg(s)


@art
def clay_inside():
    s = R("#030304") + glow(1200, 900, 900, "moon", 0.25)
    s += '<path d="M300,1350 L300,200 L2100,200 L2100,1350 Z" fill="#0c0e0e"/>'
    s += stones(300, 2100, 200, 1300, 80, 4, "#151918", 40)
    s += alux_full_fig(1200, 1250, 1050, clay=True, eyes="none", mood="calm", rim="#a8c8d8")
    s += '<path d="M1080,1250 C1100,1210 1150,1200 1180,1250 Z M1220,1250 C1240,1205 1300,1210 1320,1250 Z" fill="#1a0e06"/>'  # fresh mud
    for i in range(10):
        s += f'<ellipse cx="{1100+i*24}" cy="{1240+(i%3)*6}" rx="14" ry="6" fill="#2a1a0c" opacity="0.9"/>'
    s += glow(1200, 600, 500, "moon", 0.12)
    return svg(s)


@art
def clay_trompo():
    s = R("#030304") + glow(1200, 700, 800, "moon", 0.3)
    # big clay hand (alux) holding the worn trompo
    sk = SK_CLAY
    s += f'<path d="M300,1350 C500,1150 760,1000 980,960 L1200,980 C1260,1010 1260,1090 1200,1110 L1000,1120 C820,1180 640,1300 600,1350 Z" fill="{sk["shadow"]}"/>'
    s += f'<g transform="translate(1330,760) rotate(-12)">{trompo_svg(2.6, worn=True)}</g>'
    for i, (fx, fy) in enumerate(((1180, 900), (1250, 950), (1300, 1010), (1320, 1080))):  # clay fingers curled round it
        s += f'<path d="M{fx-120},{fy+40} C{fx-40},{fy-40} {fx+80},{fy-30} {fx+120},{fy+30} C{fx+130},{fy+70} {fx+90},{fy+90} {fx+60},{fy+70} C{fx+20},{fy+30} {fx-60},{fy+60} {fx-100},{fy+90} Z" fill="{sk["base"]}"/>'
        s += f'<path d="M{fx-80},{fy+20} C{fx},{fy-30} {fx+80},{fy-20} {fx+116},{fy+28}" stroke="{sk["hi"]}" stroke-width="5" fill="none" opacity="0.6"/>'
    s += f'<path d="M1000,1100 C900,1030 940,940 1040,930 C1100,960 1120,1040 1060,1100 Z" fill="{sk["light"]}"/>'  # thumb
    r = random.Random(2)
    for _ in range(30):
        x, y = r.uniform(700, 1400), r.uniform(900, 1200)
        s += f'<path d="M{x:.0f},{y:.0f} l{r.uniform(-12,12):.0f},{r.uniform(5,16):.0f}" stroke="{sk["deep"]}" stroke-width="2.5" opacity="0.7"/>'
    s += f'<path d="M980,960 L1200,980 C1260,1010 1260,1090 1200,1110" stroke="#a8c8d8" stroke-width="5" fill="none" opacity="0.5"/>'
    return svg(s)


@art
def casita_day():
    s = sky("#88a8bc", "#efe0b8") + glow(600, 300, 500, "warm", 0.5)
    s += monte(860, "#3a5a48", 4, 260, 40)
    s += '<path d="M0,1040 L2400,1020 L2400,1350 L0,1350 Z" fill="#9a8a5e"/>'
    s += milpa_row(1040, 30, 200, 300, "#4a7a3a", "#e8f0a0", 11, w=6)
    s += kahtal(1250, 1120, 1.5, day=True, rim=None)
    s += jicara(1250, 1170, 0.5) + '<path d="M1340,1170 l40,-10 l10,20 l-40,8 Z" fill="#e8c860"/>'
    s += milpa_row(1360, 20, 480, 640, "#2a5222", "#d8e890", 12, w=12, x0=-100, x1=750)
    return svg(s)


@art
def casita_overgrown():
    s = night_milpa_base(13, 600, 220, 80)
    s += monte(1000, "#030a0c", 14, 320, 30)
    s += '<path d="M0,1100 L2400,1080 L2400,1350 L0,1350 Z" fill="#050908"/>'
    s += kahtal(1200, 1130, 1.5, overgrown=True)
    s += jicara(1260, 1180, 0.5, full=False, col="#1a120a")
    s += mist(1150, 100, 0.25, "#a8c0c0", 8)
    return svg(s)


@art
def alux_peek():
    s = yuc_night(21, 2000, 200, 70)
    s += '<path d="M0,0 L2400,0 L2400,1350 L0,1350 Z" fill="#050c0a" opacity="0.6"/>'
    s += milpa_row(1000, 30, 500, 700, "#081410", MOONRIM, 21, w=10)
    s += alux_full_fig(1200, 1240, 760, rim="#bfe0ff", mood="grin")
    s += milpa_row(1350, 14, 700, 1000, "#010403", MOONRIM, 22, w=16, x0=-200, x1=1000)
    s += milpa_row(1350, 10, 700, 1000, "#010403", MOONRIM, 23, w=16, x0=1450, x1=2600)
    s += mist(1250, 90, 0.25, "#a8c8c0", 2)
    return svg(s)


@art
def alux_scare():
    s = sky("#0a0204", "#2a0a0a") + glow(1200, 650, 900, "red", 0.45)
    s += f'<g transform="translate(1200,700) scale(3.1)">{alux_head("scare", "glow", "#ff5a3a")}</g>'
    return svg(s)


@art
def alux_close():
    s = yuc_night(22, 1900, 180, 60) + milpa_row(1200, 26, 700, 1000, "#030807", MOONRIM, 31, w=12)
    s += R("#000", 0.25)
    s += f'<g transform="translate(1200,640) scale(2.5)">{alux_head("grin", "glow", "#bfe0ff", look=0.3)}</g>'
    return svg(s)


@art
def alux_full():
    s = yuc_night(23, 600, 240, 90) + monte(880, "#061418", 2, 200, 40)
    s += '<path d="M0,1100 L2400,1080 L2400,1350 L0,1350 Z" fill="#060a09"/>'
    s += milpa_row(1100, 30, 380, 520, "#081410", MOONRIM, 33, w=9)
    s += alux_full_fig(1700, 1250, 900, rim="#bfe0ff", sling=True)
    s += mist(1200, 90, 0.25, "#a8c8c0", 2)
    return svg(s)

alux_full_fig = __import__("alux").alux_full


@art
def alux_roof():
    s = yuc_night(24, 1350, 300, 210)
    s += monte(1000, "#030a0c", 12, 220, 30)
    s += '<path d="M0,1150 L2400,1130 L2400,1350 L0,1350 Z" fill="#040807"/>'
    s += kahtal(1250, 1200, 1.9)
    s += alux_full_fig(1250, 690, 520, pose="sit", rim="#d8f0ff", mood="grin")
    s += milpa_row(1360, 16, 500, 680, "#010403", MOONRIM, 24, w=12, x0=-100, x1=600)
    return svg(s)


@art
def l_stones():
    r = random.Random(9); s = ""
    for _ in range(70):
        x, y = r.uniform(100, 2300), r.uniform(-200, 900); rr = r.uniform(7, 16)
        s += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rr:.0f}" ry="{rr*0.8:.0f}" fill="#9a9a90"/><ellipse cx="{x-rr*0.3:.0f}" cy="{y-rr*0.3:.0f}" rx="{rr*0.4:.0f}" ry="{rr*0.25:.0f}" fill="#f0f0e8" opacity="0.6"/>'
        s += f'<path d="M{x:.0f},{y-rr:.0f} l0,{-rr*3:.0f}" stroke="#c8d8e0" stroke-width="{rr*0.5:.0f}" opacity="0.15"/>'
    return svg(s)


@art
def l_eyes_gold():
    r = random.Random(12); s = ""
    for _ in range(6):
        x, y = r.uniform(200, 2200), r.uniform(800, 1150); d = 16
        for dx in (-d, d):
            s += f'<circle cx="{x+dx:.0f}" cy="{y:.0f}" r="22" fill="url(#warmglow)"/><ellipse cx="{x+dx:.0f}" cy="{y:.0f}" rx="6" ry="5" fill="#ffd040"/>'
    return svg(s)


@art
def l_corn_fg():
    s = milpa_row(1450, 8, 900, 1200, "#010202", None, 40, w=18, x0=-200, x1=500)
    s += milpa_row(1450, 8, 900, 1200, "#010202", None, 41, w=18, x0=1950, x1=2700)
    return svg(s)


@art
def l_brush_fg():
    return yuc_art.ART["l_brush_fg"]()


@art
def l_fire_glow():
    return yuc_art.ART["l_fire_glow"]()


@art
def l_candle_glow():
    return svg(glow(1600, 700, 420, "warm", 0.8))


@art
def l_alux_walk():
    return svg(alux_full_fig(700, 1150, 300, pose="walk", rim="#bfe0ff"))


@art
def l_copal():
    r = random.Random(6); s = ""
    for i in range(9):
        x = r.uniform(900, 1500); y = r.uniform(300, 900)
        s += (f'<path d="M{x:.0f},{y+300:.0f} C{x+r.uniform(-120,120):.0f},{y+150:.0f} {x+r.uniform(-160,160):.0f},{y:.0f} {x+r.uniform(-200,200):.0f},{y-250:.0f}" '
              f'stroke="#e8e4dc" stroke-width="{r.uniform(20,50):.0f}" fill="none" opacity="{r.uniform(0.12,0.3):.2f}" filter="url(#blur3)"/>')
    return svg(s)


# ================================================================== INTERIORS / RITUAL
@art
def champa_inside():
    s = R("#050403")
    # palm roof from inside: radiating poles
    for i in range(16):
        a = math.radians(200 + i * 9)
        s += f'<path d="M1200,-200 L{1200+math.cos(a)*2400:.0f},{-200-math.sin(a)*1600:.0f}" stroke="#1e160c" stroke-width="22"/>'
    r = random.Random(4)
    for _ in range(400):
        x = r.uniform(0, 2400); y = r.uniform(0, 700)
        s += f'<path d="M{x:.0f},{y:.0f} l{r.uniform(-30,30):.0f},{r.uniform(20,60):.0f}" stroke="#3a2a16" stroke-width="2" opacity="0.6"/>'
    s += '<path d="M0,700 L2400,700 L2400,1350 L0,1350 Z" fill="#120c06"/>'
    for i in range(30):  # wall of sticks
        x = i * 82
        s += f'<path d="M{x},700 L{x},1050" stroke="#0a0604" stroke-width="22"/><path d="M{x+10},700 L{x+10},1050" stroke="#3a2a16" stroke-width="3" opacity="0.6"/>'
    s += '<rect x="0" y="1050" width="2400" height="300" fill="#1a1008"/>'
    s += hammock(250, 640, 1350, 620, 260)
    s += fogon(1200, 1240, 1.0)
    s += glow(1200, 1100, 700, "warm", 0.5)
    s += '<path d="M1980,1040 L2040,640" stroke="#6a6a6a" stroke-width="10"/><path d="M2040,640 C2060,600 2120,600 2130,640 L2050,680 Z" fill="#8a8a8a"/>'  # machete on the wall
    return svg(s)


@art
def champa_out():
    s = night_milpa_base(31, 1800, 230, 90)
    s += milpa_row(950, 30, 200, 300, "#0a1a14", MOONRIM, 31, w=6)
    s += champa(1200, 1150, 1.3, lit=True)
    s += milpa_row(1360, 20, 480, 650, "#020605", MOONRIM, 32, w=12)
    return svg(s)


@art
def footprints_ash():
    s = R("#1a1614")
    r = random.Random(5)
    for _ in range(500):
        x, y = r.uniform(0, 2400), r.uniform(0, 1350)
        s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(2,10):.0f}" fill="{r.choice(("#4a4644","#6a6460","#2a2624","#8a8480"))}" opacity="0.7"/>'
    s += '<ellipse cx="1200" cy="700" rx="1100" ry="500" fill="#8a8480" opacity="0.25" filter="url(#blur4)"/>'
    for i in range(3):  # charred sticks
        s += f'<path d="M{200+i*700},{1250-i*400} l{500},{-120+i*60}" stroke="#0a0806" stroke-width="40" stroke-linecap="round"/>'
    for i, (x, y) in enumerate(((600, 1150), (780, 1000), (900, 870), (1080, 740), (1180, 610), (1360, 490), (1440, 360), (1620, 250))):
        side = 1 if i % 2 else -1
        fx, fy = x + side * 40, y
        s += f'<g transform="translate({fx},{fy}) rotate(-35) scale(1.6)" opacity="0.92">'
        s += '<path d="M0,40 C-22,40 -26,10 -20,-10 C-14,-34 14,-34 18,-10 C24,10 22,40 0,40 Z" fill="#141210"/>'
        for tx, ty, tr in ((-16, -38, 7), (-6, -44, 7), (5, -44, 6), (14, -40, 5), (21, -32, 4)):
            s += f'<circle cx="{tx}" cy="{ty}" r="{tr}" fill="#141210"/>'
        s += '</g>'
    return svg(s)


@art
def tool_tree():
    s = night_milpa_base(41, 2150, 170, 80)
    # ramón tree with a coa hanging at the top
    s += '<path d="M1180,1350 C1200,1000 1150,700 1220,400 L1290,400 C1260,700 1300,1000 1320,1350 Z" fill="#050706"/>'
    for a, L in ((-50, 600), (-20, 500), (20, 520), (55, 600), (-80, 400), (80, 380)):
        x1 = 1250 + math.sin(math.radians(a)) * L; y1 = 420 - math.cos(math.radians(a)) * L * 0.6
        s += f'<path d="M1250,440 Q{(1250+x1)/2:.0f},{(440+y1)/2-60:.0f} {x1:.0f},{y1:.0f}" stroke="#050706" stroke-width="26" fill="none" stroke-linecap="round"/>'
    r = random.Random(3)
    for _ in range(300):
        x = 1250 + r.gauss(0, 420); y = 200 + r.gauss(0, 140)
        s += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r.uniform(20,40):.0f}" ry="{r.uniform(10,18):.0f}" fill="#06100c" transform="rotate({r.uniform(0,180):.0f} {x:.0f} {y:.0f})"/>'
    s += '<path d="M1500,170 L1500,330" stroke="#c8c0a8" stroke-width="4"/>'
    s += '<path d="M1500,330 L1500,560" stroke="#5a3a1e" stroke-width="16"/><path d="M1470,560 C1470,620 1540,640 1560,560 Z" fill="#a8a8a8"/>'
    s += f'<path d="M1508,330 L1508,560" stroke="{MOONRIM}" stroke-width="3" opacity="0.6"/>' + glow(1500, 450, 200, "moon", 0.35)
    s += milpa_row(1350, 20, 380, 520, "#020605", MOONRIM, 42, w=10)
    return svg(s)


@art
def corn_bitten():
    s = sky("#2a3a3c", "#7a8a80")
    s += milpa_row(1000, 20, 500, 700, "#1a2a20", "#c8d8b0", 51, w=10)
    # big close ear of corn, kernels bitten away
    s += '<g transform="translate(1200,700) rotate(-18)">'
    s += '<path d="M-150,-420 C-260,-200 -240,250 -60,450 L60,450 C240,250 260,-200 150,-420 C80,-470 -80,-470 -150,-420 Z" fill="#e8d070"/>'
    r = random.Random(7)
    for row in range(16):
        for col in range(9):
            x = -128 + col * 32; y = -380 + row * 52
            if abs(x) > 170 - abs(y) * 0.05: continue
            bite = (row in (5, 6, 7, 10, 11) and col in (2, 3, 4, 5, 6)) or (row in (3, 4) and col in (5, 6, 7))
            if bite:
                s += f'<ellipse cx="{x}" cy="{y}" rx="13" ry="20" fill="#8a7a50"/><path d="M{x-8},{y-6} l8,10 l8,-10" stroke="#5a4a2a" stroke-width="3" fill="none"/>'
            else:
                s += f'<ellipse cx="{x}" cy="{y}" rx="14" ry="22" fill="#f4dc80"/><ellipse cx="{x-4}" cy="{y-6}" rx="5" ry="8" fill="#fff4c0" opacity="0.7"/>'
    s += '<path d="M-200,450 C-300,200 -340,-100 -200,-500 C-180,-200 -140,200 -60,460 Z" fill="#5a7a3a"/><path d="M200,450 C300,200 330,-100 210,-480 C190,-200 140,200 60,460 Z" fill="#4a6a2e"/>'
    s += '</g>'
    return svg(s)


@art
def thief_stones():
    s = night_milpa_base(61, 1900, 220, 90)
    s += milpa_row(1000, 30, 300, 420, "#081410", MOONRIM, 61, w=8)
    s += glow(1100, 900, 500, "moon", 0.45)
    s += man_sil(1100, 1250, 640, hat=True, color="#04060a", rim="#d8f0ff", facing=-1, bag=True)
    s += '<path d="M1060,820 C1000,760 960,760 930,800" stroke="#04060a" stroke-width="40" fill="none" stroke-linecap="round"/>'  # arm up shielding
    s += milpa_row(1360, 18, 480, 650, "#020605", MOONRIM, 62, w=12)
    return svg(s)


@art
def abuelo_portrait():
    s = sky("#6a8aa0", "#e8c890") + glow(1800, 300, 600, "warm", 0.5)
    s += milpa_row(1100, 30, 400, 600, "#3a5a2e", "#e8f0a0", 71, w=8)
    s += R("#000", 0.2)
    s += abuelo_bust(1200, 560, 1.5, rim="#fff0c8", smile=0.4)
    return svg(s)


@art
def abuelo_candle():
    s = interior("#3a2418", "#1a100a", (1700, 800)) + R("#000", 0.35)
    s += abuelo_bust(1150, 560, 1.6, rim=WARM, smile=-0.2, lids=0.3)
    s += candle(1750, 900, 120, 26)
    return svg(s)


@art
def abuelo_offering():
    s = night_milpa_base(72, 1900, 230, 80)
    s += '<path d="M0,1100 L2400,1080 L2400,1350 L0,1350 Z" fill="#060a09"/>'
    s += kahtal(1500, 1130, 1.3, lit=True, door="closed")
    s += jicara(1500, 1180, 0.5)
    s += man_sil(950, 1300, 680, hat=True, color="#05060a", rim=WARM, facing=1, pose="kneel") if False else man_sil(1000, 1300, 680, hat=True, color="#05060a", rim=WARM, facing=1)
    s += glow(1500, 1150, 400, "warm", 0.5)
    return svg(s)


@art
def ofrenda_jicara():
    s = R("#0a0806") + glow(1200, 700, 900, "warm", 0.45)
    s += '<path d="M0,900 L2400,900 L2400,1350 L0,1350 Z" fill="#2a1a0e"/>'
    s += jicara(1200, 860, 3.5)
    s += '<ellipse cx="1200" cy="860" rx="200" ry="44" fill="#f0e6c8"/><ellipse cx="1160" cy="850" rx="70" ry="12" fill="#ffffff" opacity="0.6"/>'
    s += candle(700, 900, 260, 40) + candle(1750, 900, 200, 36)
    for i in range(5):  # elotes
        s += f'<g transform="translate({1550+i*70},{1050}) rotate({-60+i*8})"><ellipse cx="0" cy="0" rx="34" ry="110" fill="#e8c860"/><path d="M-34,0 C-50,80 -20,140 0,160 C20,140 50,80 34,0" fill="#6a8a3a"/></g>'
    for i in range(6):  # tortillas
        s += f'<ellipse cx="{500+i*8}" cy="{1120-i*14}" rx="170" ry="40" fill="#e8d8a8" stroke="#b8a070" stroke-width="3"/>'
    return svg(s)


@art
def eusebio_young():
    s = sky("#6a8aa0", "#e8c890") + glow(600, 300, 600, "warm", 0.5)
    s += milpa_row(1100, 30, 400, 600, "#3a5a2e", "#e8f0a0", 81, w=8) + R("#000", 0.15)
    s += eusebio_bust(1200, 600, 1.35, rim="#fff0c8", age="young", hat=False)
    return svg(s)


@art
def eusebio_portrait():
    s = sky("#2a1a14", "#6a3a22") + glow(700, 600, 700, "warm", 0.45)
    s += eusebio_bust(1200, 560, 1.5, rim=WARM, smile=0.25, look=-0.2)
    return svg(s)


@art
def eusebio_scared():
    s = yuc_night(82, 600, 300, 160) + milpa_row(1200, 30, 500, 700, "#04100c", MOONRIM, 82, w=10)
    s += eusebio_bust(1200, 560, 1.55, rim="#bfe0ff", fear=True)
    return svg(s)


@art
def eusebio_gun():
    s = night_milpa_base(83, 1900, 230, 90)
    s += milpa_row(1000, 30, 300, 420, "#081410", MOONRIM, 83, w=8)
    s += kahtal(1850, 1060, 0.7)
    s += man_sil(800, 1300, 720, hat=True, color="#03040a", rim=MOONRIM, facing=1)
    s += '<path d="M830,850 L1180,760" stroke="#03040a" stroke-width="22" stroke-linecap="round"/><path d="M1060,790 L1260,740" stroke="#1a1a1a" stroke-width="10"/>'
    s += f'<path d="M830,840 L1260,734" stroke="{MOONRIM}" stroke-width="3" opacity="0.5"/>'
    s += milpa_row(1360, 14, 480, 650, "#020605", MOONRIM, 84, w=12, x0=1300, x1=2600)
    return svg(s)


@art
def eusebio_fever():
    s = interior("#2a1c14", "#0e0a06", (1800, 700)) + R("#000", 0.3)
    s += hammock(200, 520, 2200, 520, 280)
    s += '<g transform="translate(1150,760) rotate(-78)">' + eusebio_bust(0, 0, 0.95, rim=WARM, hat=False, lids=0.0, smile=-0.6, fear=True) + '</g>'
    s += '<path d="M200,560 Q1200,1000 2200,560 L2200,700 Q1200,1180 200,700 Z" fill="#7a2a24" opacity="0.92"/>'
    for i in range(12):
        s += f'<path d="M{300+i*160},{640+math.sin(i/11*math.pi)*380:.0f} l20,60" stroke="#e8b030" stroke-width="6" opacity="0.6"/>'
    s += candle(1950, 1000, 120, 26)
    return svg(s)


@art
def eusebio_kneel():
    s = night_milpa_base(85, 2000, 220, 80)
    s += '<path d="M0,1100 L2400,1080 L2400,1350 L0,1350 Z" fill="#060a09"/>'
    s += kahtal(1600, 1120, 1.5, lit=True, overgrown=True)
    s += jicara(1600, 1170, 0.55)
    for x in (1380, 1820):
        s += candle(x, 1160, 90, 20)
    # kneeling man, seen from behind-left
    s += ('<g transform="translate(900,1250)"><path d="M-120,0 C-140,-80 -100,-140 -40,-150 L-60,-330 C-80,-420 -40,-480 20,-480 C80,-470 110,-410 90,-330 L60,-150 '
          'C120,-140 160,-80 140,0 Z" fill="#05060a"/><circle cx="30" cy="-540" r="58" fill="#05060a"/>'
          '<path d="M40,-400 C120,-380 180,-360 230,-330" stroke="#05060a" stroke-width="40" stroke-linecap="round" fill="none"/>'
          f'<path d="M90,-330 L60,-150 C120,-140 160,-80 140,0 M80,-560 C100,-520 90,-500 84,-490" stroke="{WARM}" stroke-width="5" fill="none" opacity="0.7"/></g>')
    s += mist(1200, 80, 0.2, "#a8c0c0", 3)
    return svg(s)


@art
def hammock_empty():
    s = interior("#141a1e", "#06080a", (1700, 400))
    s += R("#02060c", 0.35)
    s += hammock(300, 520, 2100, 500, 300)
    s += '<path d="M1900,200 L2300,200 L2300,1100 L1900,1100 Z" fill="#7aa0c0" opacity="0.25"/>' + glow(2100, 650, 500, "moon", 0.4)
    s += '<path d="M1700,1250 L2300,1100 L2400,1350 L1500,1350 Z" fill="#7aa0c0" opacity="0.15"/>'
    s += f'<g transform="translate(900,1250) rotate(30)">{trompo_svg(0.0001)}</g>'
    return svg(s)


@art
def juana_portrait():
    s = interior("#4a3a2a", "#1a120c", (1750, 700)) + R("#000", 0.35)
    s += juana_bust(1150, 560, 1.5, rim=WARM, smile=0.2)
    return svg(s)


@art
def juana_scared():
    s = yuc_night(91, 1800, 260, 120) + milpa_row(1200, 30, 500, 700, "#04100c", MOONRIM, 91, w=10)
    s += juana_bust(1200, 560, 1.55, rim="#bfe0ff", fear=True)
    return svg(s)


@art
def juana_door():
    s = yuc_night(92, 600, 250, 80) + monte(900, "#061418", 6, 220, 40)
    s += '<rect x="1300" y="0" width="1100" height="1350" fill="#120c08"/>'
    s += '<path d="M1500,250 L1900,250 L1900,1350 L1500,1350 Z" fill="#e8a050"/>' + glow(1700, 700, 500, "warm", 0.8)
    s += woman_sil(1600, 1300, 760, color="#0a0604", rim=WARM, facing=-1)
    for i in range(4):
        s += f'<ellipse cx="{1250-i*6}" cy="{1290-i*12}" rx="100" ry="24" fill="#e8d8a8" stroke="#a89060" stroke-width="3"/>'
    s += milpa_row(1350, 14, 380, 520, "#010403", MOONRIM, 92, w=10, x0=-100, x1=1200)
    return svg(s)


@art
def mateo_corn():
    s = yuc_night(93, 1300, 230, 110)
    s += monte(860, "#061418", 2, 220, 40) + '<path d="M0,960 L2400,940 L2400,1350 L0,1350 Z" fill="#060c0a"/>'
    s += milpa_row(980, 34, 260, 380, "#081410", MOONRIM, 93, w=7)
    s += '<path d="M1020,1350 C1100,1180 1180,1060 1250,980 L1290,980 C1260,1060 1260,1180 1320,1350 Z" fill="#1a2a28" opacity="0.6"/>'  # path between rows
    s += mist(1100, 100, 0.25, "#b0c8c8", 4)
    s += glow(1250, 1000, 420, "moon", 0.35)
    s += child_sil(1150, 1280, 470, color="#0a0e14", rim="#e8f6ff", facing=1, hand_up=True)
    s += alux_full_fig(1330, 1270, 300, pose="walk", rim="#e8f6ff", eyes="glow", facing=-1)
    s += milpa_row(1360, 10, 600, 800, "#010403", MOONRIM, 94, w=14, x0=-200, x1=800)
    s += milpa_row(1360, 10, 600, 800, "#010403", MOONRIM, 95, w=14, x0=1750, x1=2600)
    return svg(s)


@art
def mateo_found():
    s = sky("#4a6070", "#c8a888") + glow(2000, 900, 600, "warm", 0.45)
    s += monte(900, "#1a2a28", 3, 260, 40) + mist(900, 120, 0.5, "#d8dce0", 2)
    s += '<path d="M0,1080 L2400,1060 L2400,1350 L0,1350 Z" fill="#3a3a2a"/>'
    s += kahtal(1500, 1120, 1.4, day=True, rim=None, overgrown=True)
    s += jicara(1500, 1170, 0.5, full=False)
    # curled sleeping child
    s += ('<g transform="translate(900,1180)"><path d="M-220,30 C-240,-40 -160,-90 -60,-80 C40,-90 160,-60 200,0 C220,40 180,60 120,56 L-180,56 C-220,56 -230,46 -220,30 Z" fill="#c8c0b0"/>'
          '<circle cx="-240" cy="-20" r="62" fill="#5a3a26"/><path d="M-300,-30 C-300,-90 -200,-100 -190,-50 C-220,-70 -260,-60 -300,-30 Z" fill="#0c0806"/>'
          '<path d="M180,40 C210,60 240,60 260,44 C250,70 200,80 170,64 Z" fill="#2a1a0c"/>'  # muddy feet
          '<ellipse cx="-110" cy="30" rx="40" ry="20" fill="#5a3a26"/></g>')
    s += stones(700, 1000, 1210, 1240, 12, 3, "#e8c860", 7)  # corn kernels
    s += mist(1200, 100, 0.3, "#e8e4dc", 6)
    return svg(s)


@art
def trompo():
    s = R("#1a120a") + glow(1200, 700, 800, "warm", 0.4)
    s += '<path d="M0,900 L2400,860 L2400,1350 L0,1350 Z" fill="#3a2a1a"/>'
    s += stones(0, 2400, 900, 1350, 60, 8, "#4a3a2a", 16)
    s += f'<g transform="translate(1200,780) rotate(14)">{trompo_svg(2.4)}</g>'
    s += '<path d="M1340,600 C1500,520 1640,640 1560,760 C1500,860 1700,920 1820,860" stroke="#e8d8b0" stroke-width="7" fill="none"/>'  # string
    s += '<ellipse cx="1240" cy="1180" rx="160" ry="20" fill="#000" opacity="0.4" filter="url(#blur2)"/>'
    return svg(s)


@art
def hmen_portrait():
    s = interior("#3a2418", "#1a100a", (1700, 800)) + R("#000", 0.3)
    s += hmen_bust(1150, 560, 1.55, rim=WARM, smile=0.0, lids=0.5)
    s += candle(1750, 900, 140, 26)
    return svg(s)


def altar_table(cx=1200, top=820, k=1.0, food=True):
    s = f'<rect x="{cx-600*k:.0f}" y="{top:.0f}" width="{1200*k:.0f}" height="{40*k:.0f}" fill="#4a2e18"/>'
    for lx in (cx - 560 * k, cx + 540 * k):
        s += f'<rect x="{lx:.0f}" y="{top+40*k:.0f}" width="{24*k:.0f}" height="{400*k:.0f}" fill="#2a1a0c"/>'
    # arch of branches over the table
    s += f'<path d="M{cx-560*k:.0f},{top:.0f} C{cx-560*k:.0f},{top-700*k:.0f} {cx+560*k:.0f},{top-700*k:.0f} {cx+560*k:.0f},{top:.0f}" stroke="#1a2a14" stroke-width="{24*k:.0f}" fill="none"/>'
    r = random.Random(3)
    for _ in range(60):
        t = r.uniform(0, 1); x = cx - 560 * k + 1120 * k * t; y = top - 4 * 520 * k * t * (1 - t)
        s += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{28*k:.0f}" ry="{12*k:.0f}" fill="#2a4a22" transform="rotate({r.uniform(0,180):.0f} {x:.0f} {y:.0f})"/>'
    s += f'<path d="M{cx:.0f},{top:.0f} L{cx:.0f},{top-260*k:.0f} M{cx-70*k:.0f},{top-190*k:.0f} L{cx+70*k:.0f},{top-190*k:.0f}" stroke="#d8c8a0" stroke-width="{16*k:.0f}"/>'  # wooden cross
    if food:
        for i, x in enumerate((-400, -200, 200, 400)):
            s += jicara(cx + x * k, top - 6, 0.6 * k, full=True)
        for i in range(5):
            s += f'<ellipse cx="{cx-20*k:.0f}" cy="{top-8-i*10*k:.0f}" rx="{110*k:.0f}" ry="{20*k:.0f}" fill="#e8d8a8" stroke="#a89060" stroke-width="2"/>'
        for x in (-500, -300, 300, 500):
            s += candle(cx + x * k, top, 120 * k, 20 * k)
        s += f'<path d="M{cx+120*k:.0f},{top:.0f} C{cx+100*k:.0f},{top-30*k:.0f} {cx+160*k:.0f},{top-30*k:.0f} {cx+150*k:.0f},{top:.0f} Z" fill="#6a3a1a"/>'  # copal burner
    return s


@art
def ritual_altar():
    s = night_milpa_base(101, 2000, 200, 70)
    s += '<path d="M0,1000 L2400,980 L2400,1350 L0,1350 Z" fill="#0a0c0a"/>'
    s += altar_table(1200, 860, 1.25)
    s += glow(1200, 800, 700, "warm", 0.45)
    return svg(s)


@art
def ritual_wide():
    s = night_milpa_base(102, 1900, 200, 80)
    s += milpa_row(960, 34, 260, 380, "#081410", MOONRIM, 102, w=7)
    s += '<path d="M0,1050 L2400,1030 L2400,1350 L0,1350 Z" fill="#070a08"/>'
    s += altar_table(1200, 1000, 0.6)
    s += glow(1200, 980, 500, "warm", 0.5)
    s += man_sil(1200, 1250, 520, hat=False, color="#05060a", rim=WARM, facing=-1)  # jmen
    s += '<path d="M1240,960 C1300,900 1340,860 1360,800" stroke="#05060a" stroke-width="20" stroke-linecap="round"/>'
    for i in range(7):
        s += f'<path d="M1360,800 l{-40+i*14},{-60-i%3*14}" stroke="#2a4a22" stroke-width="6"/>'  # sip'che branch
    for x, f in ((700, 1), (1650, -1), (1850, -1)):
        s += man_sil(x, 1300, 560, hat=True, color="#05060a", rim=WARM, facing=f)
    s += woman_sil(500, 1300, 520, color="#05060a", rim=WARM, facing=1)
    s += kahtal(2150, 1060, 0.5)
    return svg(s)


@art
def barro_pit():
    s = yuc_night(111, 1900, 200, 80)
    s += '<rect x="0" y="0" width="2400" height="1350" fill="#04080a" opacity="0.4"/>'
    s += '<path d="M0,700 C400,620 800,640 1200,680 C1600,640 2000,620 2400,700 L2400,1350 L0,1350 Z" fill="#14110c"/>'
    s += '<ellipse cx="1200" cy="1050" rx="760" ry="200" fill="#020406"/>'
    s += '<ellipse cx="1200" cy="1080" rx="640" ry="140" fill="#0a1e24"/>' + glow(1200, 1080, 500, "moon", 0.3)
    s += '<path d="M440,1000 C600,900 900,880 1000,900 C1000,960 700,1000 440,1040 Z" fill="#5a3a22"/>'  # clay bank
    s += man_sil(820, 940, 460, hat=True, color="#05060a", rim=MOONRIM, facing=1)
    s += man_sil(560, 960, 430, hat=False, color="#05060a", rim=MOONRIM, facing=1)
    for x in (300, 2100):  # roots hanging into the cenote
        for i in range(6):
            s += f'<path d="M{x+i*30},680 C{x+i*30-20},800 {x+i*30+20},900 {x+i*30},{1000+i*10}" stroke="#0a0806" stroke-width="6" fill="none"/>'
    return svg(s)


@art
def hands_clay():
    s = R("#0e0806") + glow(1200, 700, 800, "warm", 0.45)
    s += '<path d="M0,950 L2400,950 L2400,1350 L0,1350 Z" fill="#3a2414"/>'
    s += f'<g transform="translate(1200,700) scale(0.75)">{alux_full_fig(0, 300, 900, clay=True, eyes="none", mood="calm", rim=None)}</g>'
    sk = SK_OLD
    for sx in (-1, 1):  # two old hands shaping it
        s += (f'<g transform="translate({1200+sx*330},{780}) scale({sx},1)"><path d="M300,300 C200,240 120,160 90,60 C80,20 100,0 130,10 L160,60 '
              f'C150,0 170,-50 200,-40 C220,-30 220,0 214,40 C230,-20 260,-30 280,-10 C290,20 270,80 270,120 C320,140 360,200 400,300 Z" fill="{sk["base"]}"/>'
              f'<path d="M90,60 C100,0 130,10 160,60" stroke="{WARM}" stroke-width="5" fill="none" opacity="0.7"/>'
              f'<path d="M110,80 C140,100 160,100 180,90" stroke="{sk["deep"]}" stroke-width="3" fill="none"/></g>')
    s += candle(1850, 950, 160, 30)
    return svg(s)


@art
def palm_blood():
    s = R("#0a0604") + glow(1200, 600, 800, "warm", 0.4)
    s += '<path d="M0,1050 L2400,1050 L2400,1350 L0,1350 Z" fill="#3a2414"/>'
    s += f'<g transform="translate(1200,1080) scale(0.55)">{alux_full_fig(0, 0, 1000, clay=True, eyes="none", mood="calm", rim=None)}</g>'
    sk = SK_OLD
    s += (f'<g transform="translate(1250,200)"><path d="M-260,-200 C-200,-100 -160,0 -180,80 C-200,160 -120,240 0,240 C120,240 200,180 210,80 '
          f'C220,0 260,-60 300,-200 Z" fill="{sk["base"]}"/>'
          f'<path d="M-120,120 C-40,160 60,150 140,90" stroke="{sk["deep"]}" stroke-width="5" fill="none"/>'
          f'<path d="M-100,60 C-20,90 60,80 120,40" stroke="{sk["deep"]}" stroke-width="4" fill="none" opacity="0.7"/>'
          f'<path d="M-180,80 C-200,160 -120,240 0,240" stroke="{WARM}" stroke-width="6" fill="none" opacity="0.6"/></g>')
    for i, y in enumerate((500, 640, 760)):  # drops falling
        s += f'<path d="M1240,{y-30} C1226,{y} 1222,{y+20} 1240,{y+26} C1258,{y+20} 1254,{y} 1240,{y-30} Z" fill="#8a0a0e"/>'
    s += '<ellipse cx="1220" cy="808" rx="18" ry="8" fill="#6a0a0c"/>'
    s += candle(600, 1050, 180, 30)
    return svg(s)


@art
def clay_figure():
    s = R("#0a0604") + glow(1200, 700, 900, "warm", 0.45)
    s += '<path d="M0,1100 L2400,1100 L2400,1350 L0,1350 Z" fill="#3a2414"/>'
    s += alux_full_fig(1200, 1130, 950, clay=True, eyes="none", mood="calm", rim=WARM)
    s += candle(650, 1100, 200, 34) + candle(1780, 1100, 160, 30)
    return svg(s)


@art
def altar_empty():
    s = R("#0c1014") + glow(1700, 400, 700, "moon", 0.35)
    s += '<path d="M1500,0 L2000,0 L1900,1100 L1600,1100 Z" fill="#9ab8d0" opacity="0.12"/>'
    s += '<path d="M0,1100 L2400,1100 L2400,1350 L0,1350 Z" fill="#1a1612"/>'
    s += '<path d="M1060,1100 C1080,1080 1140,1076 1160,1100 M1240,1100 C1260,1080 1320,1076 1340,1100" stroke="#5a3a22" stroke-width="10" fill="none"/>'  # clay marks where it stood
    for i, (x, y) in enumerate(((1380, 1150), (1480, 1210), (1580, 1260), (1700, 1320))):
        s += f'<g transform="translate({x},{y}) rotate(60) scale(0.9)"><path d="M0,24 C-14,24 -16,6 -12,-6 C-8,-20 8,-20 10,-6 C14,6 12,24 0,24 Z" fill="#5a3a22"/></g>'
    for x in (650, 1750):
        s += f'<rect x="{x-14}" y="1040" width="28" height="60" fill="#c8c0b0"/><path d="M{x},1040 C{x-10},980 {x+20},940 {x-6},880" stroke="#a0a8b0" stroke-width="5" fill="none" opacity="0.5" filter="url(#blur1)"/>'
    return svg(s)


@art
def abuelo_hammock():
    s = interior("#2a1c14", "#0e0a06", (1800, 700)) + R("#000", 0.3)
    s += hammock(200, 520, 2200, 520, 280)
    s += '<path d="M200,560 Q1200,1000 2200,560 L2200,680 Q1200,1150 200,680 Z" fill="#e8e0cc" opacity="0.9"/>'
    s += '<g transform="translate(1000,760) rotate(-80)">' + abuelo_bust(0, 0, 0.8, rim=WARM, hat=False, lids=1.0, smile=0.1) + '</g>'
    s += candle(1800, 1050, 150, 26) + candle(600, 1050, 120, 22)
    return svg(s)


# ================================================================== CANCÚN
@art
def cancun_build():
    s = sky("#5aa0c8", "#f0e0b8") + glow(1800, 300, 500, "warm", 0.5)
    s += '<path d="M0,760 L2400,740 L2400,900 L0,920 Z" fill="#2a9ab0"/>'  # sea / lagoon
    for i in range(14):
        s += f'<path d="M{i*180},{780+i%3*30} l120,0" stroke="#e8f4f0" stroke-width="3" opacity="0.5"/>'
    s += '<path d="M0,880 L2400,860 L2400,1350 L0,1350 Z" fill="#e8dcc0"/>'  # sand
    s += monte(900, "#2a4a30", 21, 120, 30, -100, 900)
    # unfinished concrete buildings with scaffolds
    for x, w, h in ((1100, 260, 380), (1450, 300, 460), (1850, 240, 300)):
        s += f'<rect x="{x}" y="{880-h}" width="{w}" height="{h}" fill="#b8b4ac"/>'
        for fy in range(880 - h, 880, 60):
            s += f'<path d="M{x},{fy} l{w},0" stroke="#6a6660" stroke-width="5"/>'
        for fx in range(x, x + w, 40):
            s += f'<path d="M{fx},{880-h} l0,-60" stroke="#5a5650" stroke-width="3"/>'
    s += '<path d="M2100,880 L2100,300 L2130,300 L2130,880 M1900,320 L2400,320" stroke="#c8a030" stroke-width="12"/><path d="M2300,320 L2300,520" stroke="#3a3a3a" stroke-width="3"/>'  # crane
    for x in (300, 500, 700, 950):
        s += man_sil(x, 1250, 300, hat=True, color="#3a2a1a", rim=None, facing=1)
    s += '<rect x="560" y="1150" width="120" height="100" fill="#8a8a84"/><rect x="580" y="1110" width="100" height="40" fill="#9a9a94"/>'  # blocks
    return svg(s)


@art
def workers_fire():
    s = yuc_night(121, 1900, 180, 60)
    s += '<path d="M0,800 L2400,780 L2400,880 L0,900 Z" fill="#0a1e2a"/>'
    s += '<path d="M0,880 L2400,860 L2400,1350 L0,1350 Z" fill="#1a1610"/>'
    s += fogon(1200, 1220, 1.4)
    s += glow(1200, 1150, 700, "warm", 0.6)
    for x, f, h in ((700, 1, 560), (900, 1, 500), (1550, -1, 540), (1750, -1, 600)):
        s += man_sil(x, 1300, h, hat=True, color="#0a0604", rim="#ffb060", facing=f)
    return svg(s)


@art
def bridge_night():
    s = yuc_night(122, 400, 220, 90)
    s += '<path d="M0,900 L2400,880 L2400,1350 L0,1350 Z" fill="#06141c"/>'
    for i in range(20):
        s += f'<path d="M{i*130},{960+i%4*60} l90,0" stroke="#9ab8d0" stroke-width="2" opacity="0.3"/>'
    # half-built bridge deck on columns
    s += '<path d="M0,560 L1500,560 L1500,620 L0,620 Z" fill="#2a3036"/>'
    for x in (200, 650, 1100, 1550, 2000):
        s += f'<rect x="{x}" y="{620 if x < 1500 else 520}" width="90" height="{500 if x < 1500 else 600}" fill="#1e2428"/>'
        s += f'<path d="M{x+90},{620 if x<1500 else 520} l0,500" stroke="{MOONRIM}" stroke-width="3" opacity="0.5"/>'
    for i in range(8):  # bent rebar sticking up from the unfinished end
        s += f'<path d="M{1520+i*10},560 C{1530+i*10},480 {1600+i*20},450 {1650+i*25},{470+i*5}" stroke="#6a5040" stroke-width="5" fill="none"/>'
    s += '<path d="M0,560 L1500,560" stroke="#9fc8e8" stroke-width="3" opacity="0.5"/>'
    s += mist(950, 100, 0.3, "#a8c8d0", 3)
    return svg(s)


@art
def bent_rebar():
    s = R("#0a1014") + glow(1700, 300, 700, "moon", 0.3)
    s += '<path d="M0,900 L2400,900 L2400,1350 L0,1350 Z" fill="#3a3c3c"/>'
    r = random.Random(4)
    for i in range(12):
        x = 500 + i * 120
        s += f'<path d="M{x},1350 L{x},800 C{x},{600+r.uniform(-60,60):.0f} {x+r.uniform(-300,300):.0f},{550:.0f} {x+r.uniform(-400,400):.0f},{r.uniform(400,700):.0f}" stroke="#6a4a3a" stroke-width="14" fill="none"/>'
        s += f'<path d="M{x+4},1350 L{x+4},800" stroke="#c8a890" stroke-width="3" opacity="0.4"/>'
    s += stones(300, 2100, 1100, 1340, 30, 6, "#5a5c5c", 26)
    return svg(s)


@art
def bridge_shrine():
    s = yuc_night(123, 1900, 200, 70)
    s += '<path d="M0,250 L2400,250 L2400,360 L0,360 Z" fill="#1e2428"/>'
    for x in (300, 1900):
        s += f'<rect x="{x}" y="360" width="160" height="900" fill="#141a1e"/>'
    s += '<path d="M0,1050 L2400,1030 L2400,1350 L0,1350 Z" fill="#0c1012"/>'
    # small stepped pyramid shrine
    for i in range(5):
        w = 420 - i * 70; h = 50
        s += f'<rect x="{1200-w/2:.0f}" y="{1080-(i+1)*h:.0f}" width="{w}" height="{h}" fill="{"#4a4e4c" if i%2 else "#3e4240"}"/>'
        s += f'<path d="M{1200+w/2:.0f},{1080-(i+1)*h:.0f} l0,{h}" stroke="{MOONRIM}" stroke-width="3" opacity="0.5"/>'
    s += '<rect x="1170" y="900" width="60" height="70" fill="#020202"/>'
    for x in (1020, 1380):
        s += candle(x, 1090, 80, 18)
    s += jicara(1200, 1110, 0.4)
    s += mist(1100, 100, 0.25, "#a8c0c8", 9)
    return svg(s)


@art
def milpa_burn():
    s = sky("#2a1810", "#c8602a") + glow(1200, 900, 1000, "red", 0.4)
    s += monte(820, "#140806", 3, 200, 40)
    s += '<path d="M0,900 L2400,880 L2400,1350 L0,1350 Z" fill="#1a0c06"/>'
    r = random.Random(3)
    for _ in range(40):  # burning stumps and smoke
        x = r.uniform(0, 2400); y = r.uniform(930, 1300)
        s += f'<path d="M{x:.0f},{y:.0f} l{r.uniform(-10,10):.0f},{-r.uniform(30,90):.0f}" stroke="#0a0604" stroke-width="{r.uniform(10,22):.0f}"/>'
        s += f'<ellipse cx="{x:.0f}" cy="{y-30:.0f}" rx="{r.uniform(10,30):.0f}" ry="{r.uniform(20,50):.0f}" fill="#ff8a2a" opacity="0.6" filter="url(#blur2)"/>'
    for _ in range(12):
        x = r.uniform(0, 2400)
        s += f'<path d="M{x:.0f},1100 C{x+100:.0f},800 {x-100:.0f},500 {x+r.uniform(-200,200):.0f},100" stroke="#5a4a40" stroke-width="{r.uniform(60,120):.0f}" fill="none" opacity="0.25" filter="url(#blur4)"/>'
    s += man_sil(1700, 1300, 620, hat=True, color="#050302", rim="#ff9a50", facing=-1)
    return svg(s)


# ================================================================== HISTORY
@art
def ruins_dawn():
    s = sky("#2a3a5a", "#f0a868") + glow(1800, 700, 700, "warm", 0.7)
    s += monte(950, "#1a2018", 2, 160, 40)
    # stepped pyramid (Puuc/Ek Balam style)
    for i in range(7):
        w = 1300 - i * 150; h = 70
        s += f'<rect x="{1100-w/2:.0f}" y="{1000-(i+1)*h:.0f}" width="{w}" height="{h}" fill="{"#3a3028" if i%2 else "#4a3e32"}"/>'
        s += f'<path d="M{1100+w/2:.0f},{1000-(i+1)*h:.0f} l0,{h}" stroke="#ffc880" stroke-width="5" opacity="0.6"/>'
    s += '<rect x="960" y="370" width="280" height="140" fill="#3a3028"/><rect x="1060" y="420" width="80" height="90" fill="#0a0806"/>'
    s += '<path d="M1040,1000 L1040,510 L1160,510 L1160,1000 Z" fill="#2e261e" opacity="0.8"/>'  # stair
    s += '<path d="M0,1000 L2400,980 L2400,1350 L0,1350 Z" fill="#1a1a12"/>'
    s += mist(1000, 120, 0.4, "#f0d0b0", 2)
    return svg(s)


@art
def stone_figures():
    s = sky("#3a3a5a", "#f0b070") + glow(1900, 900, 800, "warm", 0.7)
    s += '<path d="M0,0 L2400,0" />'
    for i in range(4):  # big steps of a temple, close
        s += f'<rect x="0" y="{700+i*170}" width="2400" height="170" fill="{"#5a4a3a" if i%2 else "#4a3c30"}"/>'
        s += f'<path d="M0,{700+i*170} L2400,{700+i*170}" stroke="#ffd0a0" stroke-width="5" opacity="0.6"/>'
    for x, y, h, sl in ((600, 870, 380, False), (1200, 870, 420, True), (1700, 1040, 360, False)):
        s += alux_full_fig(x, y, h, clay=True, eyes="none", mood="calm", rim="#ffd0a0", sling=sl).replace("#8a5a3a", "#7a7064").replace("#a8724c", "#948a7c").replace("#5a3622", "#5a5248").replace("#c99068", "#b8ae9e").replace("#6a4228", "#6a6258").replace("#9a6a46", "#8a8274").replace("#b8865e", "#a89e8e")
    return svg(s)


@art
def figurines():
    s = R("#1a120a") + glow(1200, 600, 900, "warm", 0.4)
    s += '<path d="M0,900 L2400,860 L2400,1350 L0,1350 Z" fill="#4a3420"/>'
    r = random.Random(5)
    for _ in range(200):
        x, y = r.uniform(0, 2400), r.uniform(880, 1350)
        s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(3,9):.0f}" fill="#2a1c10" opacity="0.6"/>'
    # three small earthen figurines half-dug, one tilted
    for x, rot, h in ((800, -8, 520), (1250, 4, 620), (1700, 20, 460)):
        fig = alux_full_fig(0, 0, h, clay=True, eyes="none", mood="calm", rim="#ffd0a0")
        s += f'<g transform="translate({x},1150) rotate({rot})">{fig}</g>'
    s += '<path d="M0,1180 C400,1150 800,1170 1200,1160 C1600,1150 2000,1170 2400,1160 L2400,1350 L0,1350 Z" fill="#3a2614"/>'
    s += '<path d="M300,1300 L700,1000" stroke="#6a4a2a" stroke-width="22" stroke-linecap="round"/><path d="M700,1000 L760,940 L800,1000 Z" fill="#8a8a8a"/>'  # coa
    return svg(s)


@art
def mano_tease():
    s = R("#0a1020") + glow(600, 300, 500, "moon", 0.35)
    s += '<path d="M0,700 L2400,700 L2400,820 L0,820 Z" fill="#e8e4dc"/><path d="M0,820 L2400,820 L2400,880 L0,880 Z" fill="#2a1a10"/>'  # bed edge
    s += '<path d="M0,880 L2400,880 L2400,1350 L0,1350 Z" fill="#0e1424"/>' + glow(1200, 1150, 500, "moon", 0.25)
    # child's arm hanging over the edge
    s += '<path d="M700,760 C720,860 740,960 760,1040" stroke="#8a6044" stroke-width="56" stroke-linecap="round" fill="none"/>'
    # hairy hand reaching up from the dark
    s += '<path d="M1300,1350 C1280,1200 1220,1100 1060,1060 C1000,1040 980,1000 1000,980 C1040,960 1100,1000 1140,1020 C1100,950 1080,880 1110,860 C1150,850 1170,920 1190,980 C1190,900 1200,840 1240,840 C1280,850 1270,930 1260,990 C1290,930 1320,880 1350,900 C1380,920 1340,1000 1320,1060 C1380,1100 1400,1200 1420,1350 Z" fill="#060404"/>'
    r = random.Random(2)
    for _ in range(160):
        x = r.uniform(1000, 1420); y = r.uniform(860, 1350)
        s += f'<path d="M{x:.0f},{y:.0f} l{r.uniform(-14,14):.0f},{r.uniform(-20,-6):.0f}" stroke="#2a2420" stroke-width="2"/>'
    s += '<path d="M1110,860 C1150,850 1170,920 1190,980 M1240,840 C1280,850 1270,930 1260,990" stroke="#9ab0e0" stroke-width="5" fill="none" opacity="0.8"/>'
    s += '<path d="M1300,1350 C1280,1200 1220,1100 1060,1060 C1000,1040 980,1000 1000,980" stroke="#9ab0e0" stroke-width="4" fill="none" opacity="0.6"/>'
    return svg(s)


@art
def monte_dense():
    return yuc_art.ART["monte_dense"]()


if __name__ == "__main__":
    os.makedirs("art", exist_ok=True)
    names = sys.argv[1:] or list(ART)
    for n in names:
        open(f"art/{n}.svg", "w").write(ART[n]())
    print(len(names), "svg written")
