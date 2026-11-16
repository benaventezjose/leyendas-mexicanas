#!/usr/bin/env python3
"""Illustrations for 'La Mano Peluda' — writes art/*.svg (2400x1350).
Render: node /home/claude/pipeline/render_svg.js art/*.svg      Usage: python3 make_art.py [name ...]"""
import sys, os, math, random
sys.path.insert(0, '/home/claude/pipeline'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from helpers import man_sil, woman_sil, moon_sky, far_hills, wood_door
from scenery import mist as _mist, maguey, nopal, stars_sky, city_row, blur_ell
from chars import (head, hair_short, mustache, wrinkles, shirt_body, blouse_body, bust_frame, abuela_bust, abuela_head,
                   fermin_bust, sombrero, SK_OLD, SK_TOMAS)
from base_chars import uid, grad_lin, grad_rad, hand_open, hooded, jailer, villager
from art import *
from hand import hand, place

ART = {}
def art(fn):
    ART[fn.__name__] = fn
    return fn

G = lambda x, y, k, f, flip=False: f'<g transform="translate({x},{y}) scale({-k if flip else k},{k})">{f}</g>'
R = lambda c="#000", op=1.0: f'<rect width="2400" height="1350" fill="{c}" opacity="{op}"/>'
MOONRIM = "#9fc8e8"; WARM = "#ffcf8a"; RED = "#c8141a"
SK_BOY = dict(base="#a8714e", light="#c88c64", hi="#e4ad84", shadow="#6e4630", deep="#3a2216")
SK_PELU = dict(base="#b08a6c", light="#c8a284", hi="#e0bc9c", shadow="#76563e", deep="#3e2a1c")
ARM = "#b07a58"; ARM_DK = "#6a4430"


def mist(y, h=120, op=0.25, *a, **k):
    return _mist(y, h, op * 0.45, *a, **k)


def lgv(id_, stops):  # vertical gradient defs
    s = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    return f'<defs><linearGradient id="{id_}" x1="0" y1="0" x2="0" y2="1">{s}</linearGradient></defs>'


# ------------------------------------------------------------------ people
def boy_hair(seed=5, col="#0a0706"):
    r = random.Random(seed)
    s = (f'<path d="M-82,-40 C-92,-110 -50,-148 0,-150 C56,-150 94,-110 84,-40 C76,-70 60,-96 30,-102 C10,-86 -20,-84 -40,-100 '
         f'C-60,-90 -74,-70 -82,-40 Z" fill="{col}"/>')
    for _ in range(26):  # messy fringe
        x = r.uniform(-70, 70)
        s += f'<path d="M{x:.0f},-130 q{r.uniform(-14,14):.0f},26 {r.uniform(-16,16):.0f},{r.uniform(34,52):.0f}" stroke="{col}" stroke-width="{r.uniform(6,12):.0f}" fill="none" stroke-linecap="round"/>'
    for _ in range(18):
        x = r.uniform(-60, 60)
        s += f'<path d="M{x:.0f},-140 q{r.uniform(-10,10):.0f},16 {r.uniform(-10,10):.0f},30" stroke="#3a2c24" stroke-width="2" fill="none" opacity="0.6"/>'
    return s


def julian_head(look=0.0, turn=0.0, fear=False, smile=0.3, lids=0.1, rim=MOONRIM, closed=False):
    s = head(look=look, smile=(-0.9 if fear else smile), lids=(0.0 if fear else lids), rim=rim, turn=turn, sk=SK_BOY, headwrap=False,
             earring=False, lips=("#8a5440", "#9a6048"), iris="#1a0c06", brow_w=0.9, eyes_closed=closed)
    if fear:
        s += '<ellipse cx="0" cy="78" rx="13" ry="12" fill="#1e0a06"/>'
        s += '<path d="M-58,-52 Q-36,-68 -12,-50 M58,-52 Q36,-68 12,-50" stroke="#120806" stroke-width="5" fill="none"/>'
    s += boy_hair()
    return s


def pajama_body(g, rim):
    s = shirt_body(g, SK_BOY, rim, cloth=("#2a3a5a", "#7a90b8", "#a8bcdc"), sarape=False)
    for i in range(-6, 7):
        s += f'<path d="M{i*58},200 C{i*60},360 {i*64},500 {i*66},660" stroke="#e8eef8" stroke-width="7" fill="none" opacity="0.35"/>'
    return s


def julian_bust(x, y, k=1.0, rim=MOONRIM, **hk):
    g = uid("jb")
    return bust_frame(pajama_body(g, rim), julian_head(rim=rim, **hk), x, y, k)


def child_arm(pts, w=46, rim=MOONRIM, open_=True):
    """Child's thin arm along a polyline, ending in a small relaxed hand."""
    d = "M" + " L".join(f"{x:.0f},{y:.0f}" for x, y in pts)
    s = f'<path d="{d}" stroke="{rim}" stroke-width="{w+10}" fill="none" stroke-linecap="round" opacity="0.5" filter="url(#blur1)"/>'
    s += f'<path d="{d}" stroke="{ARM_DK}" stroke-width="{w}" fill="none" stroke-linecap="round"/>'
    s += f'<path d="{d}" stroke="{ARM}" stroke-width="{w*0.55}" fill="none" stroke-linecap="round" transform="translate(-6,0)" opacity="0.9"/>'
    (x0, y0), (x1, y1) = pts[-2], pts[-1]
    a = math.degrees(math.atan2(y1 - y0, x1 - x0)) - 90
    hnd = (f'<ellipse cx="0" cy="34" rx="{w*0.62:.0f}" ry="{w*0.85:.0f}" fill="{ARM}"/>'
           + "".join(f'<path d="M{dx},{50} l{dx*0.25:.0f},{l}" stroke="{ARM}" stroke-width="{w*0.24:.0f}" stroke-linecap="round"/>'
                     for dx, l in ((-18, 52), (-6, 62), (6, 60), (18, 48)))
           + f'<path d="M-24,22 l-20,36" stroke="{ARM}" stroke-width="{w*0.26:.0f}" stroke-linecap="round"/>'
           + f'<path d="M{w*0.5:.0f},10 C{w*0.7:.0f},40 {w*0.4:.0f},90 20,110" stroke="{rim}" stroke-width="3" fill="none" opacity="0.7"/>')
    s += f'<g transform="translate({x1:.0f},{y1:.0f}) rotate({a:.0f})">{hnd}</g>'
    s += f'<path d="{d}" stroke="{rim}" stroke-width="3" fill="none" transform="translate({w*0.45:.0f},0)" opacity="0.6"/>'
    return s


def peludo_head(rim=WARM, look=0.2, smile=0.6):
    s = head(look=look, smile=smile, lids=0.45, rim=rim, sk=SK_PELU, headwrap=False, earring=False, lips=("#6a3a2e", "#7e4a3c"),
             iris="#140a06", brow_w=1.8)
    s += wrinkles(heavy=0.7)
    # bald crown, black hair at the sides, thick brows, huge mustache, jowls and stubble
    s += '<path d="M-84,-30 C-92,-70 -84,-96 -66,-110 L-60,-60 Z M84,-30 C92,-70 84,-96 66,-110 L60,-60 Z" fill="#0a0706"/>'
    s += '<path d="M-64,-56 Q-38,-74 -10,-54 M64,-56 Q38,-74 10,-54" stroke="#0a0706" stroke-width="12" fill="none" stroke-linecap="round"/>'
    s += mustache(big=1.5)
    s += '<path d="M-74,40 C-80,90 -50,130 0,134 C50,130 80,90 74,40" fill="none" stroke="#0a0706" stroke-width="6" opacity="0.35" filter="url(#blur1)"/>'
    r = random.Random(3)
    for _ in range(140):
        x = r.uniform(-70, 70); y = r.uniform(70, 128)
        if abs(x) < 26 and y < 90: continue
        s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="1.6" fill="#1a100a" opacity="0.6"/>'
    s += '<path d="M-60,-112 C-30,-128 30,-128 60,-112" stroke="#f4dcc0" stroke-width="5" fill="none" opacity="0.45"/>'  # shine on scalp
    return s


def peludo_bust(x, y, k=1.0, rim=WARM):
    g = uid("pb")
    body = shirt_body(g, SK_PELU, rim, cloth=("#2a2a2a", "#bcb4a4", "#ddd6c6"), sarape=False)
    body += '<path d="M-420,320 C-400,240 -300,200 -110,190 L-40,660 L-460,660 Z M420,320 C400,240 300,200 110,190 L40,660 L460,660 Z" fill="#1a1612"/>'  # wide vest
    body += '<path d="M-110,190 C-300,200 -400,240 -420,320" stroke="' + rim + '" stroke-width="6" fill="none" opacity="0.5"/>'
    body += '<path d="M-60,430 C-20,470 40,470 90,440" stroke="#e8c060" stroke-width="5" fill="none"/><circle cx="96" cy="436" r="12" fill="#e8c060"/>'  # watch chain
    for yy in (300, 380, 460, 540):
        body += f'<circle cx="-56" cy="{yy}" r="9" fill="#3a3024"/>'
    return f'<g transform="translate({x},{y}) scale({k})"><g transform="translate(0,18) scale(0.9,0.86)">{body}</g>{peludo_head(rim)}</g>'


def coin(x, y, r_=30, tilt=0.5, op=1.0):
    return (f'<ellipse cx="{x}" cy="{y}" rx="{r_}" ry="{r_*tilt:.1f}" fill="#8a8678" opacity="{op}"/>'
            f'<ellipse cx="{x}" cy="{y-3}" rx="{r_}" ry="{r_*tilt:.1f}" fill="#d8d4c4" opacity="{op}"/>'
            f'<ellipse cx="{x}" cy="{y-3}" rx="{r_*0.7:.1f}" ry="{r_*tilt*0.7:.1f}" fill="none" stroke="#9a9484" stroke-width="2" opacity="{op}"/>'
            f'<ellipse cx="{x-r_*0.3:.1f}" cy="{y-r_*tilt*0.4:.1f}" rx="{r_*0.25:.1f}" ry="{r_*tilt*0.15:.1f}" fill="#fff" opacity="{0.7*op:.2f}"/>')


# ------------------------------------------------------------------ places
def floorboards(y0=980, col="#1a120c", line="#060403", vx=1200, n=18, lit=None):
    s = f'<rect x="0" y="{y0}" width="2400" height="{1350-y0}" fill="{col}"/>'
    for i in range(-n, n + 1):
        s += f'<path d="M{vx + i*14},{y0} L{vx + i*260},1350" stroke="{line}" stroke-width="4"/>'
    r = random.Random(4)
    for j in range(6):
        y = y0 + (1350 - y0) * (j / 6) ** 1.6
        for i in range(-n, n, 2):
            xs = vx + i * (14 + (y - y0) / (1350 - y0) * 246)
            if not (-100 < xs < 2400): continue
            s += f'<path d="M{xs:.0f},{y:.0f} l{r.uniform(40,120):.0f},0" stroke="{line}" stroke-width="2" opacity="0.6"/>'
    if lit:
        s += f'<ellipse cx="{lit[0]}" cy="{lit[1]}" rx="700" ry="160" fill="{lit[2]}" opacity="0.18" filter="url(#blur3)"/>'
    return s


def iron_bed(x, base, w=900, h=300, rim=MOONRIM, sheet="#c8ccd4", blanket="#4a2a3a", occupied=True):
    s = ""
    # legs + frame
    s += f'<rect x="{x}" y="{base-h}" width="{w}" height="40" fill="#0a0a0c"/>'
    s += f'<rect x="{x}" y="{base-h-40}" width="{w}" height="70" rx="20" fill="{sheet}"/>'  # mattress
    s += f'<path d="M{x-10},{base-h-30} C{x+w*0.3},{base-h-70 if occupied else base-h-40} {x+w*0.7},{base-h-90 if occupied else base-h-40} {x+w+10},{base-h-30} L{x+w+20},{base-h+40} L{x-20},{base-h+40} Z" fill="{blanket}"/>'
    s += f'<path d="M{x-10},{base-h-30} C{x+w*0.3},{base-h-70 if occupied else base-h-40} {x+w*0.7},{base-h-90 if occupied else base-h-40} {x+w+10},{base-h-30}" stroke="{rim}" stroke-width="4" fill="none" opacity="0.6"/>'
    for i in range(6):
        s += f'<path d="M{x+40+i*w/6:.0f},{base-h+40} q10,-30 0,-60" stroke="#000" stroke-width="5" fill="none" opacity="0.25"/>'
    s += f'<rect x="{x+10}" y="{base-h+40}" width="18" height="{h-40}" fill="#0a0a0c"/><rect x="{x+w-28}" y="{base-h+40}" width="18" height="{h-40}" fill="#0a0a0c"/>'
    # headboard bars
    hx = x - 20
    s += f'<path d="M{hx},{base} L{hx},{base-h-360} M{hx+120},{base-h-30} L{hx+120},{base-h-330}" stroke="#0c0c10" stroke-width="16"/>'
    s += f'<path d="M{hx},{base-h-360} C{hx+40},{base-h-420} {hx+90},{base-h-400} {hx+120},{base-h-330}" stroke="#0c0c10" stroke-width="14" fill="none"/>'
    for i in range(1, 4):
        s += f'<path d="M{hx},{base-h-60-i*70} L{hx+120},{base-h-60-i*70}" stroke="#0c0c10" stroke-width="8"/>'
    s += f'<circle cx="{hx}" cy="{base-h-370}" r="18" fill="#2a2418"/><circle cx="{hx-4}" cy="{base-h-374}" r="6" fill="{rim}" opacity="0.7"/>'
    s += f'<path d="M{hx+8},{base} L{hx+8},{base-h-350}" stroke="{rim}" stroke-width="3" opacity="0.5"/>'
    s += f'<ellipse cx="{x+150}" cy="{base-h-60}" rx="120" ry="40" fill="#e0e4ea"/>'  # pillow
    # under the bed: deep shadow
    s += f'<rect x="{x}" y="{base-h+40}" width="{w}" height="{h-40}" fill="#000" opacity="0.85"/>'
    s += f'<ellipse cx="{x+w/2}" cy="{base}" rx="{w*0.6}" ry="40" fill="#000" opacity="0.7" filter="url(#blur2)"/>'
    return s


def room(mood="night", candle_xy=(640, 860), bed=True, occupied=True, window=True, extra=""):
    pal = {"night": ("#101a2a", "#0a1018", "#1a140e"), "day": ("#6e5a46", "#4a3a2c", "#4a3222"),
           "dawn": ("#2a3a50", "#1c2636", "#2a2018"), "candle": ("#2a1c14", "#140c08", "#22160e")}[mood]
    s = lgv("rw" + mood, [(0, pal[1]), (1, pal[0])]) + '<rect width="2400" height="1000" fill="url(#rw' + mood + ')"/>'
    # wainscot + plaster stains
    r = random.Random(7)
    for _ in range(12):
        s += blur_ell(r.uniform(0, 2400), r.uniform(200, 900), r.uniform(80, 240), r.uniform(60, 160), "#000", 0.12, 3)
    s += f'<rect x="0" y="0" width="2400" height="90" fill="#0a0604"/>'
    for i in range(9):  # vigas
        s += f'<rect x="{i*300-20}" y="0" width="70" height="130" fill="#0e0806"/><rect x="{i*300-20}" y="120" width="70" height="10" fill="#000" opacity="0.5"/>'
    if window:
        wl = {"night": "#3a5a80", "dawn": "#9ab4cc", "day": "#f0d8a0", "candle": "#24385a"}[mood]
        s += f'<path d="M1640,260 L1640,620 L1960,620 L1960,260 Q1800,170 1640,260 Z" fill="{wl}"/>'
        if mood in ("night", "candle"):
            s += moon(1860, 340, 46, halo=2.5)
        s += '<path d="M1800,200 L1800,620 M1640,440 L1960,440" stroke="#0a0806" stroke-width="16"/>'
        s += '<path d="M1620,250 L1620,640 L1980,640 L1980,250" stroke="#0a0806" stroke-width="30" fill="none"/>'
        beam = {"night": ("#a8c8f0", 0.12), "dawn": ("#cfe0f0", 0.18), "day": ("#ffe0a0", 0.2), "candle": ("#a8c8f0", 0.06)}[mood]
        s += f'<path d="M1640,300 L1960,300 L1500,1350 L700,1350 Z" fill="{beam[0]}" opacity="{beam[1]}" filter="url(#blur3)"/>'
    s += floorboards(980, pal[2], "#050302", 1200, lit=(1200, 1150, "#a8c8f0") if mood == "night" else None)
    s += '<rect x="0" y="960" width="2400" height="24" fill="#080504"/>'
    # wardrobe
    s += '<rect x="2080" y="380" width="300" height="620" fill="#140a06"/><rect x="2100" y="400" width="125" height="560" fill="#1c100a"/><rect x="2235" y="400" width="125" height="560" fill="#1c100a"/>'
    s += f'<path d="M2080,380 L2080,1000" stroke="{MOONRIM}" stroke-width="3" opacity="0.4"/>'
    s += extra
    if bed:
        s += iron_bed(560, 1180, occupied=occupied)
    if candle_xy:
        cx, cy = candle_xy
        s += f'<rect x="{cx-90}" y="{cy}" width="180" height="20" fill="#1c100a"/><rect x="{cx-80}" y="{cy+20}" width="160" height="{1180-cy-20}" fill="#120a06"/>'
        if mood in ("night", "candle"):
            s += candle(cx, cy - 4, 70, 18) + glow(cx, cy - 90, 380, "warm", 0.9)
    return s


def puebla_domes(y=900, col="#060a12", rim=MOONRIM, lit=0.3, seed=2):
    """Skyline of Puebla: twin-towered cathedral, tiled domes, flat roofs."""
    r = random.Random(seed)
    s = city_row(y, seed, 30, col, lit)
    def dome(x, yb, w, h, tiles=True):
        o = f'<rect x="{x-w*0.55}" y="{yb-h*0.35}" width="{w*1.1}" height="{h*0.35}" fill="{col}"/>'
        o += f'<path d="M{x-w/2},{yb-h*0.35} Q{x-w/2},{yb-h*1.05} {x},{yb-h*1.05} Q{x+w/2},{yb-h*1.05} {x+w/2},{yb-h*0.35} Z" fill="{col}"/>'
        o += f'<rect x="{x-8}" y="{yb-h*1.3}" width="16" height="{h*0.28}" fill="{col}"/><path d="M{x-20},{yb-h*1.22} L{x+20},{yb-h*1.22}" stroke="{col}" stroke-width="6"/>'
        if tiles:
            for i in range(1, 6):
                o += f'<path d="M{x-w/2+i*w/6:.0f},{yb-h*0.35} Q{x-w/2+i*w/6:.0f},{yb-h*0.95} {x},{yb-h*1.05}" stroke="#1e3a5a" stroke-width="3" fill="none" opacity="0.6"/>'
        o += f'<path d="M{x-w/2},{yb-h*0.35} Q{x-w/2},{yb-h*1.05} {x},{yb-h*1.05}" stroke="{rim}" stroke-width="4" fill="none" opacity="0.55"/>'
        return o
    def tower(x, yb, w, h):
        o = f'<rect x="{x-w/2}" y="{yb-h}" width="{w}" height="{h}" fill="{col}"/>'
        for j in range(3):
            o += f'<rect x="{x-w/2+w*0.12}" y="{yb-h-90-j*80}" width="{w*0.76}" height="80" fill="{col}"/>'
            o += f'<path d="M{x-w*0.18},{yb-h-22-j*80} l0,-46 q{w*0.18},-30 {w*0.36},0 l0,46 Z" fill="#203a58" opacity="0.6"/>'
        o += f'<path d="M{x-w*0.3},{yb-h-330} Q{x},{yb-h-420} {x+w*0.3},{yb-h-330} Z" fill="{col}"/><rect x="{x-5}" y="{yb-h-470}" width="10" height="60" fill="{col}"/>'
        o += f'<path d="M{x+w/2},{yb} L{x+w/2},{yb-h-330}" stroke="{rim}" stroke-width="3" opacity="0.45"/>'
        return o
    s += tower(980, y - 40, 150, 380) + tower(1420, y - 40, 150, 380)
    s += f'<rect x="1055" y="{y-300}" width="290" height="260" fill="{col}"/><path d="M1130,{y-40} l0,-150 q70,-80 140,0 l0,150 Z" fill="#0c1420"/>'
    s += dome(1200, y - 280, 200, 200)
    s += dome(400, y - 40, 220, 220) + dome(1900, y - 20, 260, 240) + dome(2250, y, 160, 150) + dome(660, y + 10, 140, 120)
    return s


def talavera_wall(x0, y0, x1, y1, seed=1, dim=0.6):
    """Puebla style: red brick (petatillo) with inset talavera tiles in a regular diamond pattern."""
    s = f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" fill="#8a3a24"/>'
    for yy in range(int(y0), int(y1), 24):
        off = 0 if (yy // 24) % 2 else 24
        s += f'<path d="M{x0},{yy} L{x1},{yy}" stroke="#5a2414" stroke-width="2"/>'
    for j, yy in enumerate(range(int(y0) + 30, int(y1) - 40, 120)):
        for i, xx in enumerate(range(int(x0) + 40 + (60 if j % 2 else 0), int(x1) - 40, 120)):
            s += f'<g transform="translate({xx},{yy}) rotate(45)"><rect x="-30" y="-30" width="60" height="60" fill="#e8e0cc"/>'
            s += '<rect x="-24" y="-24" width="48" height="48" fill="none" stroke="#1e3e8a" stroke-width="5"/><circle r="12" fill="#1e3e8a"/><circle r="5" fill="#e8b030"/></g>'
    return s + f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" fill="#0a1424" opacity="{dim}"/>'


def balcony(x, y, w=200):
    s = f'<rect x="{x-20}" y="{y}" width="{w+40}" height="14" fill="#0a0a0c"/>'
    for i in range(int(w / 20) + 1):
        s += f'<path d="M{x+i*20},{y} L{x+i*20},{y-110}" stroke="#0a0a0c" stroke-width="5"/>'
    s += f'<rect x="{x-20}" y="{y-120}" width="{w+40}" height="10" fill="#0a0a0c"/>'
    return s


def casona_facade(lit=True, mood="night"):
    s = talavera_wall(0, 180, 2400, 1050, 3, 0.62 if mood == "night" else 0.25)
    s += '<rect x="0" y="120" width="2400" height="70" fill="#2a1c14"/><rect x="0" y="105" width="2400" height="18" fill="#c8a880" opacity="0.5"/>'
    for x in (220, 760, 1640, 2180):
        s += f'<rect x="{x-110}" y="300" width="220" height="330" fill="#0a0806"/><rect x="{x-130}" y="280" width="260" height="24" fill="#b8a07a" opacity="0.7"/>'
        if lit and x in (760, 2180):
            s += f'<rect x="{x-96}" y="314" width="192" height="300" fill="#ffc865" opacity="0.6"/>' + glow(x, 460, 260, "warm", 0.5)
        s += balcony(x - 110, 630, 220)
    # zaguán
    s += '<path d="M1000,1050 L1000,560 Q1200,420 1400,560 L1400,1050 Z" fill="#1a0e08"/>'
    s += '<path d="M970,1050 L970,550 Q1200,390 1430,550 L1430,1050" stroke="#b8a07a" stroke-width="30" fill="none" opacity="0.6"/>'
    for i in range(6):
        s += f'<path d="M{1020+i*66},560 L{1020+i*66},1050" stroke="#0a0604" stroke-width="5"/>'
    s += cobbles(1050, 1350, "#141b22", 9, True)
    if mood == "night":
        s += lamp(560, 1060, 520) + glow(560, 560, 300, "warm", 0.7)
    return s


# ================================================================== SCENES
@art
def title_bg():
    s = stars_sky("#02050c", "#14263a", 200, 3, 700) + moon(1950, 260, 90)
    s += ridge(720, 150, "#0e1a2a", 41)
    # Popocatépetl silhouette on the horizon
    s += '<path d="M120,820 L520,520 C560,490 620,490 660,520 L1060,820 Z" fill="#1a2a3e"/><path d="M500,535 C560,500 620,500 680,535 L620,600 L560,580 Z" fill="#c8d4e4" opacity="0.6"/>'
    s += puebla_domes(980, "#04070c", MOONRIM, 0.3, 4)
    s += mist(960, 120, 0.25, "#a8c0d8", 3)
    s += '<rect x="0" y="1000" width="2400" height="350" fill="#020305"/>'
    s += place(1700, 1360, -8, 0.95, hand("reach", rim=MOONRIM, seed=11, rim_side=-1))
    s += glow(1650, 1100, 500, "moon", 0.15)
    return svg(s)


@art
def bedroom_wide():
    s = room("night", (420, 860), occupied=True)
    # sleeping boy: head on pillow, arm hanging over the far edge (towards camera)
    s += G(720, 790, 0.42, julian_head(closed=True, rim=WARM))
    s += child_arm([(900, 860), (1000, 900), (1020, 1010), (1030, 1110)], w=40, rim=WARM)
    return svg(s)


@art
def bedroom_day():
    s = room("day", (420, 860), occupied=False)
    return svg(s + glow(1800, 420, 600, "warm", 0.3))


@art
def dawn_room():
    s = room("dawn", (420, 860), occupied=False)
    s += '<path d="M1000,1150 C1040,1120 1080,1130 1110,1170" stroke="#e0e4ea" stroke-width="30" fill="none" opacity="0.7"/>'  # blanket pulled to the floor
    return svg(s)


@art
def bed_empty():
    s = room("dawn", None, occupied=False)
    s += '<path d="M600,880 C700,860 900,870 1000,920 C1100,1000 1180,1100 1220,1180 L1120,1200 C1060,1100 980,1000 880,960 Z" fill="#4a2a3a"/>'  # blanket sliding off
    return svg(s)


@art
def bed_arm():
    s = R("#06090f") + glow(1700, 200, 700, "moon", 0.3)
    s += '<rect x="0" y="380" width="2400" height="150" rx="30" fill="#b8bcc6"/><rect x="0" y="360" width="2400" height="60" fill="#4a2a3a"/>'
    s += '<path d="M0,420 C600,440 1200,400 2400,430 L2400,560 L0,560 Z" fill="#4a2a3a"/>'
    s += f'<path d="M0,420 C600,440 1200,400 2400,430" stroke="{MOONRIM}" stroke-width="5" fill="none" opacity="0.6"/>'
    for i in range(10):
        s += f'<path d="M{i*260+60},440 q30,60 10,120" stroke="#1a0e16" stroke-width="10" fill="none" opacity="0.6"/>'
    s += '<rect x="0" y="560" width="2400" height="40" fill="#0a0a0c"/>'
    s += '<rect x="0" y="600" width="2400" height="750" fill="#010204"/>'
    s += floorboards(1220, "#0e0a08", "#020101", 1200, n=24)
    s += '<rect x="0" y="600" width="2400" height="620" fill="#000"/>'
    s += child_arm([(1100, 470), (1150, 650), (1180, 860), (1190, 1040)], w=60)
    s += glow(1190, 1100, 260, "moon", 0.25)
    return svg(s)


@art
def under_bed():
    s = R("#010203")
    s += '<rect x="0" y="0" width="2400" height="260" fill="#0c0c10"/><rect x="0" y="240" width="2400" height="30" fill="#1a1a20"/>'
    s += f'<path d="M0,268 L2400,268" stroke="{MOONRIM}" stroke-width="3" opacity="0.4"/>'
    s += floorboards(760, "#0c0806", "#020101", 1200, n=26)
    s += '<rect x="0" y="270" width="2400" height="490" fill="#000"/>'
    s += '<path d="M0,760 L2400,760 L2400,1350 L0,1350 Z" fill="#000" opacity="0.4"/>'
    s += glow(1200, 1250, 700, "moon", 0.25)
    # dust balls and a faint light line at the far end
    s += '<rect x="900" y="700" width="600" height="6" fill="#3a5a80" opacity="0.4" filter="url(#blur1)"/>'
    r = random.Random(5)
    for _ in range(20):
        s += f'<circle cx="{r.uniform(200,2200):.0f}" cy="{r.uniform(800,1300):.0f}" r="{r.uniform(4,14):.0f}" fill="#2a2a2e" opacity="0.5" filter="url(#blur1)"/>'
    return svg(s)


@art
def hand_under():
    s = ART["under_bed"]().replace("</svg>", "")
    s = s[s.index("<rect"):] if False else s
    body = ""
    body += child_arm([(1150, 0), (1160, 160), (1170, 330)], w=70)
    body += place(900, 1250, 52, 1.05, hand("reach", rim=MOONRIM, seed=3, rim_side=1))
    body += glow(1080, 560, 300, "moon", 0.2)
    return s + body + "</svg>"


@art
def hand_grab():
    s = R("#04060a") + glow(1200, 500, 900, "moon", 0.35)
    s += child_arm([(1300, -40), (1260, 300), (1220, 640), (1200, 820)], w=110)
    s += place(1250, 1280, -8, 1.65, hand("grab", rim=MOONRIM, seed=5, rim_side=-1))
    s += '<rect width="2400" height="1350" fill="url(#redglow)" opacity="0.10"/>'
    return svg(s)


@art
def fist_closed():
    s = R("#0c1018") + floorboards(0, "#2a2018", "#0a0806", 1200, n=20) + R("#0a1018", 0.55) + glow(1200, 600, 800, "moon", 0.35)
    g = uid("fc")
    s += f'<defs>{grad_lin(g, [(0, "#6a4430", 1), (0.5, "#b07a58", 1), (1, "#d8a07a", 1)], 0, 1100, 0, 500)}</defs>'
    s += f'<path d="M-100,1350 C200,1150 500,980 900,900 L980,1080 C600,1150 300,1300 120,1450 Z" fill="url(#{g})"/>'  # forearm
    s += f'<path d="M-100,1350 C200,1150 500,980 900,900" stroke="#cfe0f0" stroke-width="6" fill="none" opacity="0.6"/>'
    # fist: back of hand + four curled fingers + thumb
    s += f'<path d="M860,880 C960,760 1200,720 1340,780 C1440,830 1460,960 1400,1060 C1320,1160 1100,1180 980,1100 Z" fill="url(#{g})"/>'
    for i in range(4):
        x = 1250 + i * 34; y = 780 + i * 70
        s += f'<path d="M{x-120},{y+10} C{x},{y-30} {x+120},{y+10} {x+130},{y+70} C{x+120},{y+120} {x},{y+110} {x-100},{y+80}" fill="#b07a58" stroke="#5a3a28" stroke-width="5"/>'
        s += f'<path d="M{x+60},{y-4} C{x+110},{y+10} {x+130},{y+40} {x+130},{y+70}" stroke="#e8b490" stroke-width="5" fill="none" opacity="0.7"/>'
    s += '<path d="M980,1000 C1060,1080 1200,1100 1300,1060" stroke="#5a3a28" stroke-width="40" fill="none" stroke-linecap="round"/><path d="M980,1000 C1060,1080 1200,1100 1300,1060" stroke="#a8714e" stroke-width="30" fill="none" stroke-linecap="round"/>'
    s += '<path d="M1440,860 L1560,790 L1600,850 L1500,930 Z" fill="#d8c898"/><path d="M1440,860 L1560,790" stroke="#8a6a30" stroke-width="3"/>'  # yellow paper corner
    s += '<path d="M960,780 C1100,720 1260,730 1350,780" stroke="#cfe0f0" stroke-width="6" fill="none" opacity="0.7"/>'
    return svg(s)


@art
def hand_crawl_street():
    s = stars_sky("#03060c", "#18283a", 160, 9, 600) + moon(500, 220, 80)
    s += facade(0, 1000, 700, 640, "#0a0f16", 3, 0.25) + facade(1700, 1000, 700, 620, "#0a0f16", 4, 0.2)
    s += puebla_domes(800, "#070b12", MOONRIM, 0.1, 6)
    s += cobbles(1000, 1350, "#141b22", 9, True)
    s += lamp(1500, 1010, 520) + glow(1500, 510, 300, "warm", 0.6)
    s += mist(1040, 90, 0.35, "#b0c4d8", 8)
    return svg(s)


@art
def l_hand_crawl():
    s = place(1450, 800, 180, 0.6, hand("claw", rim=MOONRIM, seed=7, rim_side=1))
    s += '<ellipse cx="1450" cy="1200" rx="220" ry="26" fill="#000" opacity="0.55" filter="url(#blur2)"/>'
    return svg(s)


@art
def l_hand_reach():
    return svg(place(1700, 1380, 58, 1.0, hand("reach", rim=MOONRIM, seed=9, rim_side=1)))


@art
def puebla_road():
    s = sky("#e8a060", "#f4d0a0", "#c86a40", 0, 900)
    s += '<circle cx="700" cy="560" r="80" fill="#fff0c8" opacity="0.9"/>' + glow(700, 560, 500, "warm", 0.6)
    s += '<path d="M60,900 L560,420 C600,390 660,390 700,420 L1240,900 Z" fill="#6a5a7a"/><path d="M540,440 C600,400 660,400 720,440 L660,520 L600,500 Z" fill="#f4ece0"/>'
    s += '<path d="M1180,900 L1580,560 C1640,520 1700,520 1760,560 L2300,900 Z" fill="#5a4a6a"/><path d="M1560,580 C1640,530 1720,540 1780,580 L1700,640 Z" fill="#f4ece0" opacity="0.8"/>'
    s += ridge(940, 80, "#3a3040", 5) + '<rect x="0" y="960" width="2400" height="390" fill="#2a2018"/>'
    s += '<path d="M900,1350 L1150,960 L1250,960 L1600,1350 Z" fill="#4a3a2a"/>'
    for x in (200, 420, 1900, 2150):
        s += maguey(x, 1200, 1.4, "#1a1410")
    # an old bus on the road
    s += '<rect x="1060" y="1040" width="260" height="140" rx="20" fill="#1a1410"/><rect x="1080" y="1060" width="220" height="40" fill="#f4d0a0" opacity="0.5"/>'
    s += '<circle cx="1110" cy="1185" r="22" fill="#0a0806"/><circle cx="1270" cy="1185" r="22" fill="#0a0806"/>'
    return svg(s)


@art
def julian_portrait():
    s = sky("#c87a50", "#f0c890") + puebla_domes(1000, "#3a2a24", "#ffe0b0", 0.0, 8) + '<rect x="0" y="1000" width="2400" height="350" fill="#2a1c14"/>'
    s += R("#2a1408", 0.25)
    s += julian_bust(1200, 640, 1.55, rim="#ffd8a0", smile=0.6, look=0.1)
    return svg(s)


@art
def puebla_street():
    s = stars_sky("#0a1424", "#3a4a60", 60, 2, 300)
    s += casona_facade(True, "night")
    s += R("#2a1a10", 0.1)
    return svg(s)


@art
def zaguan():
    s = R("#120a06")
    s += '<path d="M300,1350 L300,300 Q1200,-100 2100,300 L2100,1350 Z" fill="#3a2a1c"/>'
    s += '<path d="M420,1350 L420,360 Q1200,0 1980,360 L1980,1350 Z" fill="#0c0806"/>'
    # view through to the patio with arches and geraniums
    s += '<path d="M700,1100 L700,520 Q1200,300 1700,520 L1700,1100 Z" fill="#c8a070"/>'
    for x in (820, 1080, 1340, 1600):
        s += f'<path d="M{x-110},1100 L{x-110},700 Q{x},590 {x+110},700 L{x+110},1100 Z" fill="#3a2418"/>'
    s += '<rect x="700" y="1100" width="1000" height="250" fill="#8a6a4a"/>'
    for x in range(760, 1700, 120):
        s += f'<ellipse cx="{x}" cy="1110" rx="40" ry="30" fill="#6a3a22"/>' + "".join(f'<circle cx="{x+dx}" cy="{1070+dy}" r="12" fill="#d8283a"/>' for dx, dy in ((-14, 0), (10, -10), (0, 10), (18, 6)))
    s += '<ellipse cx="1200" cy="1220" rx="200" ry="50" fill="#a88a6a"/><ellipse cx="1200" cy="1200" rx="160" ry="36" fill="#5a4a3a"/>'
    s += R("#2a1808", 0.25)
    return svg(s)


@art
def patio_day():
    s = sky("#a8c8e0", "#f4e4c8")
    s += '<rect x="0" y="300" width="2400" height="1050" fill="#c89870"/>'
    for i, x in enumerate(range(150, 2400, 420)):
        s += f'<path d="M{x-170},1000 L{x-170},560 Q{x},400 {x+170},560 L{x+170},1000 Z" fill="#3a2418"/>'
        s += f'<rect x="{x+170}" y="420" width="80" height="580" fill="#d8b088"/><rect x="{x+160}" y="980" width="100" height="40" fill="#8a6a4a"/>'
    s += '<rect x="0" y="300" width="2400" height="60" fill="#8a5a3a"/>' + balcony(200, 300, 2000).replace("#0a0a0c", "#2a1a10")
    s += '<rect x="0" y="1000" width="2400" height="350" fill="#9a7a5a"/>'
    for x in range(100, 2400, 180):
        s += f'<path d="M{x-40},1050 L{x+40},1050 L{x+30},1130 L{x-30},1130 Z" fill="#8a4a2a"/>' + "".join(
            f'<circle cx="{x+dx}" cy="{1030+dy}" r="14" fill="#d02a3a"/>' for dx, dy in ((-20, 0), (14, -16), (0, 10), (24, 6), (-6, -24)))
        s += f'<path d="M{x-40},1050 q-30,-60 -10,-90 M{x+40},1050 q30,-60 10,-90" stroke="#2a5a2a" stroke-width="8" fill="none"/>'
    s += '<ellipse cx="1200" cy="1230" rx="320" ry="70" fill="#b8a080"/><ellipse cx="1200" cy="1210" rx="260" ry="50" fill="#6a5a4a"/>'
    s += '<rect x="1180" y="1080" width="40" height="130" fill="#b8a080"/><ellipse cx="1200" cy="1080" rx="90" ry="22" fill="#b8a080"/>'
    s += R("#ffcc88", 0.08)
    return svg(s)


@art
def abuela_portrait():
    s = room("candle", None, bed=False, window=False)
    s += glow(560, 860, 500, "warm", 0.9) + candle(560, 960, 80, 20)
    s += abuela_bust(1250, 620, 1.55, rim=WARM)
    return svg(s)


@art
def abuela_bedside():
    s = room("candle", (420, 860), occupied=True)
    s += G(720, 790, 0.42, julian_head(look=0.6, rim=WARM))
    s += abuela_bust(1300, 760, 0.95, rim=WARM)
    return svg(s)


@art
def abuela_close():
    s = R("#140c08") + glow(500, 900, 900, "warm", 0.8)
    s += abuela_bust(1200, 600, 2.0, rim=WARM)
    s += R("#000", 0.15)
    return svg(s)


@art
def abuela_photo():
    s = room("day", None, bed=False, window=True)
    s += abuela_bust(1100, 620, 1.5, rim="#ffe0b0")
    # the photo in her hands
    ph = '<rect x="-150" y="-110" width="300" height="220" fill="#e8dcc0"/><rect x="-130" y="-90" width="260" height="180" fill="#8a7458"/>'
    ph += '<path d="M-70,90 l0,-80 q20,-30 40,0 l0,80 Z M30,90 l0,-110 q24,-34 48,0 l0,110 Z" fill="#3a2c1e"/>'
    s += f'<g transform="translate(1150,1180) rotate(-6)">{ph}</g>'
    s += G(980, 1220, 0.9, hand_open(0, 0, 1.0, rot=20)) + G(1330, 1210, 0.9, hand_open(0, 0, 1.0, rot=-20))
    return svg(s)


@art
def julian_bed():
    s = R("#1a1008") + glow(500, 900, 800, "warm", 0.8)
    s += '<rect x="0" y="900" width="2400" height="450" fill="#4a2a3a"/><path d="M0,900 C600,860 1800,860 2400,900" stroke="#ffcf8a" stroke-width="6" fill="none" opacity="0.6"/>'
    s += '<ellipse cx="1200" cy="820" rx="520" ry="160" fill="#e0e4ea"/>'
    s += julian_bust(1200, 600, 1.4, rim=WARM, smile=0.7, look=-0.3)
    s += '<rect x="0" y="1000" width="2400" height="350" fill="#4a2a3a"/>'
    return svg(s)


@art
def julian_covers():
    s = R("#04070c") + glow(1800, 300, 700, "moon", 0.3)
    s += '<ellipse cx="1200" cy="900" rx="700" ry="200" fill="#e0e4ea" opacity="0.8"/>'
    s += '<path d="M200,1350 C300,900 600,620 1100,600 C1600,600 2000,800 2200,1350 Z" fill="#3a2230"/>'
    s += f'<path d="M200,1350 C300,900 600,620 1100,600 C1600,600 2000,800 2200,1350" stroke="{MOONRIM}" stroke-width="6" fill="none" opacity="0.6"/>'
    for i in range(7):
        s += f'<path d="M{500+i*200},{760+abs(3-i)*30} q40,140 0,300" stroke="#1a0e16" stroke-width="14" fill="none" opacity="0.6"/>'
    # only the eyes peek out from under the blanket edge
    s += '<path d="M900,700 C1000,640 1300,640 1400,700 L1400,760 L900,760 Z" fill="#a8714e"/>'
    for x in (1080, 1220):
        s += f'<ellipse cx="{x}" cy="725" rx="34" ry="20" fill="#f0ece4"/><circle cx="{x+8}" cy="726" r="12" fill="#1a0c06"/><circle cx="{x+12}" cy="722" r="4" fill="#fff"/>'
    s += '<path d="M880,770 C1000,740 1300,740 1420,770 L1440,820 L860,820 Z" fill="#3a2230"/>'
    s += '<path d="M900,660 C1000,600 1300,600 1400,660 L1400,700 C1300,650 1000,650 900,700 Z" fill="#0a0706"/>'
    return svg(s)


@art
def candle_smoke():
    s = R("#030408") + glow(1200, 700, 600, "warm", 0.15)
    s += '<rect x="1000" y="1000" width="400" height="30" fill="#1c100a"/>' + '<rect x="1170" y="820" width="60" height="180" fill="#d8ccb0"/>'
    s += '<path d="M1200,820 l0,-26" stroke="#1a1410" stroke-width="5"/><circle cx="1200" cy="792" r="5" fill="#ff7a20"/>'
    r = random.Random(2); d = "M1200,790"; x, y = 1200, 790
    for i in range(12):
        x += r.uniform(-40, 40); y -= 60; d += f" Q{x+r.uniform(-60,60):.0f},{y+30:.0f} {x:.0f},{y:.0f}"
    s += f'<path d="{d}" stroke="#a8b0c0" stroke-width="14" fill="none" opacity="0.45" filter="url(#blur1)"/>'
    s += f'<path d="{d}" stroke="#d8e0ec" stroke-width="4" fill="none" opacity="0.5" transform="translate(10,0)"/>'
    return svg(s)


@art
def floor_scratch():
    s = floorboards(0, "#2a1c12", "#0a0604", 1200, n=14)
    s += R("#0a1220", 0.45) + glow(1200, 700, 900, "moon", 0.25)
    for i in range(5):  # five long parallel claw gouges: splintered pale wood with dark edges
        x0 = 860 + i * 95; r = random.Random(i)
        d = f"M{x0},280 C{x0+30},600 {x0+40},900 {x0+70},1260"
        s += f'<path d="{d}" stroke="#050302" stroke-width="20" fill="none" stroke-linecap="round" opacity="0.85"/>'
        s += f'<path d="{d}" stroke="#c8a070" stroke-width="9" fill="none" stroke-linecap="round"/>'
        s += f'<path d="{d}" stroke="#f0d8b0" stroke-width="3" fill="none" transform="translate(-3,0)"/>'
        for _ in range(14):
            y = r.uniform(300, 1240); xx = x0 + 30 * (y - 280) / 980 + 10
            s += f'<path d="M{xx:.0f},{y:.0f} l{r.choice((-1,1))*r.uniform(10,28):.0f},{r.uniform(-14,4):.0f}" stroke="#d8b890" stroke-width="3" opacity="0.8"/>'
    return svg(s)


@art
def kitchen_day():
    s = R("#6a4a30") + '<rect x="0" y="0" width="2400" height="140" fill="#1a0e08"/>'
    s += talavera_wall(200, 300, 2200, 760, 9, 0.45)
    s += '<rect x="200" y="760" width="2000" height="80" fill="#8a3a24"/>'
    for x in range(260, 2200, 150):
        s += f'<ellipse cx="{x}" cy="240" rx="50" ry="40" fill="#8a4a2a"/><path d="M{x},200 l0,-40" stroke="#2a1a10" stroke-width="4"/>'  # clay pots
    s += '<rect x="0" y="1000" width="2400" height="350" fill="#3a2818"/>'
    s += glow(1900, 900, 400, "warm", 0.8) + '<path d="M1800,960 L2000,960 L1960,1000 L1840,1000 Z" fill="#1a0e08"/>' + "".join(f'<path d="M{1840+i*30},960 q10,-60 0,-100" stroke="#ff9a3c" stroke-width="10" fill="none" opacity="0.7"/>' for i in range(5))
    s += abuela_bust(1000, 560, 1.1, rim="#ffd8a0")
    # metate with chiles
    s += '<path d="M700,1100 L1300,1060 L1320,1120 L720,1170 Z" fill="#4a4440"/><rect x="760" y="1170" width="40" height="80" fill="#4a4440"/><rect x="1240" y="1120" width="40" height="90" fill="#4a4440"/>'
    s += '<rect x="900" y="1040" width="300" height="40" rx="20" fill="#6a625a"/>'
    for i in range(9):
        s += f'<ellipse cx="{760+i*50}" cy="{1110-i*4}" rx="26" ry="10" fill="#6a1410" transform="rotate(-8 {760+i*50} {1110-i*4})"/>'
    s += R("#ff9a50", 0.06)
    return svg(s)


@art
def virreinato_plaza():
    s = sky("#2a2a34", "#8a7a6a")
    s += church(1500, 1000, 1.4, "#1a1814", False)
    s += facade(0, 1000, 900, 600, "#2a221c", 5, 0.1) + facade(2000, 1000, 400, 500, "#2a221c", 6, 0.1)
    s += '<rect x="0" y="1000" width="2400" height="350" fill="#3a3028"/>'
    r = random.Random(8)
    for i in range(16):
        x = 200 + i * 130 + r.uniform(-30, 30)
        s += villager(x, 1250 + r.uniform(-20, 20), r.uniform(380, 460), r.choice(("man", "woman")), "#0e0c0a", "#c8b088", i)
    s += hooded(1300, 1200, 620, "#c8b088", seed=2) + hooded(1450, 1210, 600, "#c8b088", seed=3)
    s += '<path d="M1380,560 L1380,420 M1340,460 L1420,460" stroke="#0e0c0a" stroke-width="16"/>'  # green cross of the Holy Office (dark)
    return svg(s)


@art
def accused():
    s = R("#1a1008") + glow(1200, 400, 900, "warm", 0.6)
    s += '<rect x="0" y="0" width="2400" height="1350" fill="url(#paper)"/>'
    s += jailer(700, 1300, 1000, lantern=True, facing=1)
    s += man_sil(1250, 1320, 980, hat=False, rim=WARM)
    s += '<path d="M1150,780 C1200,800 1300,800 1350,780" stroke="#8a8a8a" stroke-width="10" fill="none"/><circle cx="1180" cy="790" r="16" fill="none" stroke="#8a8a8a" stroke-width="8"/><circle cx="1320" cy="790" r="16" fill="none" stroke="#8a8a8a" stroke-width="8"/>'
    s += hooded(1800, 1320, 1050, WARM, seed=5, cross=True)
    return svg(s)


@art
def block_axe():
    s = R("#140a06") + glow(1200, 300, 900, "warm", 0.5)
    s += '<rect x="0" y="1000" width="2400" height="350" fill="#2a1c12"/>'
    s += '<path d="M900,1000 L1500,1000 L1460,1200 L940,1200 Z" fill="#3a2414"/><ellipse cx="1200" cy="1000" rx="300" ry="50" fill="#5a3a20"/>'
    # long shadow of a raised axe on the wall (implied, no gore)
    s += '<path d="M1700,120 L1760,140 L1440,900 L1400,880 Z" fill="#000" opacity="0.6" filter="url(#blur1)"/><path d="M1640,60 C1780,40 1880,140 1860,240 L1700,200 Z" fill="#000" opacity="0.6" filter="url(#blur1)"/>'
    s += man_sil(560, 1330, 1000, hat=False, rim=WARM).replace('opacity="0.7"', 'opacity="0.4"')
    return svg(s)


@art
def camposanto():
    s = stars_sky("#03060c", "#1a2838", 200, 12, 700) + moon(1800, 280, 80)
    s += far_hills(880, 12) + '<rect x="0" y="960" width="2400" height="390" fill="#05080a"/>'
    r = random.Random(12)
    for i in range(24):
        x = r.uniform(0, 2400); y = r.uniform(980, 1300); k = 0.4 + (y - 980) / 320 * 0.9
        s += f'<path d="M{x-6*k:.0f},{y:.0f} l0,{-120*k:.0f} l{-34*k:.0f},0 l0,{-14*k:.0f} l{34*k:.0f},0 l0,{-36*k:.0f} l{12*k:.0f},0 l0,{36*k:.0f} l{34*k:.0f},0 l0,{14*k:.0f} l{-34*k:.0f},0 l0,{120*k:.0f} Z" fill="#2a3440" stroke="#9fc8e8" stroke-width="2" stroke-opacity="0.5" transform="rotate({r.uniform(-12,12):.0f} {x:.0f} {y:.0f})"/>'
        s += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{60*k:.0f}" ry="{12*k:.0f}" fill="#1a1410"/>'
    s += tree(300, 1000, 700, 4, "#020406", "bare") + tree(2100, 980, 600, 5, "#020406", "bare")
    s += mist(1050, 100, 0.35, "#a8c0d8", 4)
    return svg(s)


@art
def grave_hand():
    s = stars_sky("#03060c", "#18283a", 120, 14, 500) + moon(500, 220, 70)
    s += '<rect x="0" y="800" width="2400" height="550" fill="#0a0806"/>'
    s += '<path d="M1500,300 L1700,300 L1700,820 L1500,820 Z" fill="#2a2a2e"/><path d="M1500,300 Q1600,220 1700,300" fill="#2a2a2e"/>'
    s += '<path d="M1560,420 L1640,420 M1600,380 L1600,520" stroke="#0a0a0c" stroke-width="12"/>'
    s += f'<path d="M1500,300 Q1600,220 1700,300 L1700,820" stroke="{MOONRIM}" stroke-width="4" fill="none" opacity="0.5"/>'
    s += '<path d="M700,1000 C900,940 1300,940 1500,1000 L1500,1100 L700,1100 Z" fill="#2a1c12"/>'  # mound of earth
    r = random.Random(3)
    for _ in range(40):
        x = r.uniform(800, 1400); y = r.uniform(960, 1060)
        s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(5,16):.0f}" fill="#3a2a1c"/>'
    s += place(1100, 1060, 6, 0.9, hand("claw", rim=MOONRIM, seed=13, rim_side=-1))
    for _ in range(25):
        x = r.uniform(900, 1300); y = r.uniform(880, 1040)
        s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(4,10):.0f}" fill="#3a2a1c"/>'
    s += mist(1100, 80, 0.4, "#a8c0d8", 5)
    return svg(s)


@art
def hand_portrait():
    s = R("#04070c") + glow(1200, 600, 900, "moon", 0.35)
    s += place(1200, 1300, 0, 1.6, hand("open", rim=MOONRIM, seed=21, rim_side=-1))
    return svg(s)


@art
def hand_scare():
    s = R("#020204") + glow(1200, 700, 800, "red", 0.35)
    s += place(1250, 1500, 8, 2.1, hand("claw", rim="#ff6a50", seed=22, rim_side=-1))
    return svg(s)


@art
def door_gap():
    s = wood_door(0, 0, 2400, 900, "#2a1a10") + R("#0a1018", 0.55)
    s += '<rect x="0" y="900" width="2400" height="40" fill="#ffc865" opacity="0.15"/>'
    s += '<rect x="0" y="900" width="2400" height="40" fill="#000"/>'
    s += floorboards(940, "#1a120c", "#060403", 1200, n=22)
    s += glow(1250, 1050, 450, "moon", 0.4)
    s += place(1250, 880, 180, 0.95, hand("claw", rim=MOONRIM, seed=31, rim_side=1, wrist_fur=False))
    return svg(s)


@art
def door_candle():
    s = wood_door(300, 0, 2100, 1000, "#2a1a10") + R("#060408", 0.6)
    s += '<rect x="0" y="0" width="300" height="1000" fill="#120c0a"/><rect x="2100" y="0" width="300" height="1000" fill="#120c0a"/>'
    s += '<rect x="300" y="990" width="1800" height="24" fill="#ffc865" opacity="0.85"/>' + glow(1200, 1020, 500, "warm", 0.7)
    s += '<rect x="1000" y="990" width="140" height="24" fill="#000" opacity="0.8"/><rect x="1260" y="990" width="140" height="24" fill="#000" opacity="0.8"/>'  # feet shadows
    s += floorboards(1014, "#1a120c", "#060403", 1200, n=20) + '<path d="M300,1014 L2100,1014 L2400,1350 L0,1350 Z" fill="#ffb060" opacity="0.08"/>'
    return svg(s)


@art
def empeno_ext():
    s = sky("#2a2a34", "#5a5a60") + R("#000", 0.2)
    s += facade(0, 1050, 2400, 720, "#2a221c", 7, 0.0)
    s += '<rect x="700" y="520" width="1000" height="530" fill="#100a06"/>'
    s += '<rect x="700" y="420" width="1000" height="90" fill="#c8b088"/><text x="1200" y="488" text-anchor="middle" font-family="Rye" font-size="62" fill="#2a1a10">CASA DE EMPEÑO</text>'
    s += '<rect x="760" y="580" width="400" height="300" fill="#ffc865" opacity="0.5"/>' + glow(960, 730, 300, "warm", 0.5)
    for i, (x, y) in enumerate(((820, 640), (900, 700), (1000, 660), (1080, 760), (860, 800))):
        s += f'<circle cx="{x}" cy="{y}" r="22" fill="#3a2a1c"/>'  # objects in the window
    s += '<path d="M1300,1050 L1300,620 L1620,620 L1620,1050 Z" fill="#0a0604"/>'
    s += '<rect x="0" y="1050" width="2400" height="300" fill="#3a3028"/>' + woman_sil(1450, 1260, 560, "#0e0c0a", "#c8b088")
    s += R("#ffe0b0", 0.05)
    return svg(s)


@art
def empeno_int():
    s = R("#1a0e08") + '<rect x="0" y="0" width="2400" height="900" fill="#2a1a10"/>'
    for y in (260, 480, 700):
        s += f'<rect x="0" y="{y}" width="2400" height="20" fill="#0a0604"/>'
    r = random.Random(6)
    for y in (260, 480, 700):  # shelves of pawned things
        x = 40
        while x < 2360:
            kind = r.choice(("clock", "jar", "box", "iron", "shoe", "guitar"))
            if kind == "clock":
                s += f'<rect x="{x}" y="{y-150}" width="80" height="150" fill="#3a2414"/><circle cx="{x+40}" cy="{y-100}" r="26" fill="#d8ccb0"/>'; x += 110
            elif kind == "jar":
                s += f'<ellipse cx="{x+40}" cy="{y-50}" rx="40" ry="50" fill="#5a3a22"/>'; x += 100
            elif kind == "box":
                s += f'<rect x="{x}" y="{y-70}" width="120" height="70" fill="#4a2a18"/>'; x += 140
            elif kind == "iron":
                s += f'<path d="M{x},{y} L{x+90},{y} L{x+70},{y-50} L{x+20},{y-50} Z" fill="#2a2a2a"/>'; x += 110
            elif kind == "shoe":
                s += f'<path d="M{x},{y} L{x+70},{y} L{x+70},{y-30} L{x+20},{y-40} Z" fill="#1a1010"/>'; x += 90
            else:
                s += f'<ellipse cx="{x+50}" cy="{y-60}" rx="50" ry="60" fill="#6a4020"/><rect x="{x+40}" y="{y-200}" width="20" height="100" fill="#3a2414"/>'; x += 120
    s += '<rect x="0" y="900" width="2400" height="450" fill="#140a06"/><rect x="0" y="880" width="2400" height="40" fill="#5a3a22"/>'
    s += '<path d="M1600,880 L1600,720 M1520,720 L1680,720 M1520,720 L1490,800 M1550,720 L1580,800 M1650,720 L1620,800 M1680,720 L1710,800" stroke="#c8a060" stroke-width="5" fill="none"/>'
    s += '<path d="M1480,800 Q1535,830 1590,800 M1610,800 Q1665,830 1720,800" stroke="#c8a060" stroke-width="6" fill="none"/>'
    s += "".join(coin(900 + i * 50, 870 - (i % 3) * 8, 26) for i in range(8))
    s += glow(1200, 700, 700, "warm", 0.6) + candle(1200, 870, 70, 18)
    return svg(s)


@art
def peludo_portrait():
    s = ART["empeno_int"]().replace("</svg>", "")
    s += R("#000", 0.45)[:-2] + "/>"
    s += peludo_bust(1200, 560, 1.5)
    return s + "</svg>"


@art
def peludo_hands():
    s = R("#140a06") + glow(1200, 500, 900, "warm", 0.6)
    s += '<rect x="0" y="900" width="2400" height="450" fill="#3a2414"/><path d="M0,900 L2400,900" stroke="#ffcf8a" stroke-width="4" opacity="0.5"/>'
    s += "".join(coin(700 + (i % 6) * 90, 1000 + (i // 6) * 60, 40) for i in range(12))
    s += '<rect x="1200" y="960" width="200" height="120" fill="#d8c898" transform="rotate(-8 1300 1020)"/>'  # a ring box / ticket
    s += '<circle cx="1300" cy="1000" r="30" fill="none" stroke="#e8c060" stroke-width="10"/>'
    s += place(950, 1200, 70, 0.95, hand("cup", rim=WARM, seed=41, rim_side=-1, nails=False, wrist_fur=False, hair=0.8))
    s += place(1750, 1200, -60, 0.95, hand("claw", rim=WARM, seed=42, rim_side=1, nails=False, wrist_fur=False, hair=0.8))
    s += '<path d="M600,1350 C700,1250 800,1200 900,1180 L1000,1350 Z M1900,1350 C1820,1260 1760,1220 1700,1200 L1560,1350 Z" fill="#1a1612"/>'  # sleeves
    return svg(s)


@art
def empeno_woman():
    s = sky("#0a1220", "#2a3a4a")
    s += facade(0, 1050, 2400, 720, "#141a22", 7, 0.0)
    s += '<rect x="700" y="520" width="1000" height="530" fill="#100a06"/><rect x="760" y="580" width="400" height="300" fill="#ffc865" opacity="0.35"/>'
    s += '<rect x="0" y="1050" width="2400" height="300" fill="#1a2028"/>'
    s += woman_sil(1700, 1280, 800, "#05070a", MOONRIM, facing=-1)
    s += villager(500, 1280, 620, "man", "#05070a", MOONRIM, 4, -1)
    return svg(s)


@art
def panteon():
    s = stars_sky("#03060c", "#1a2838", 180, 15, 700) + moon(600, 260, 85)
    s += '<rect x="0" y="760" width="2400" height="90" fill="#141a22"/><rect x="1050" y="560" width="300" height="290" fill="#141a22"/>'
    s += '<path d="M1080,850 L1080,640 Q1200,560 1320,640 L1320,850 Z" fill="#05080c"/>'  # cemetery gate
    for i in range(14):
        s += f'<path d="M{1090+i*16},850 L{1090+i*16},650" stroke="#0a0e14" stroke-width="5"/>'
    s += '<rect x="0" y="850" width="2400" height="500" fill="#070a0e"/>'
    r = random.Random(15)
    for i in range(14):
        x = r.uniform(0, 2400); y = r.uniform(900, 1250); k = 0.5 + (y - 900) / 350
        s += f'<path d="M{x-60*k:.0f},{y:.0f} L{x-60*k:.0f},{y-160*k:.0f} Q{x:.0f},{y-220*k:.0f} {x+60*k:.0f},{y-160*k:.0f} L{x+60*k:.0f},{y:.0f} Z" fill="#1a2028"/>'
        s += f'<path d="M{x-60*k:.0f},{y-160*k:.0f} Q{x:.0f},{y-220*k:.0f} {x+60*k:.0f},{y-160*k:.0f}" stroke="{MOONRIM}" stroke-width="3" fill="none" opacity="0.5"/>'
    s += tree(250, 900, 650, 7, "#020406", "ahuehuete") + man_sil(1900, 1250, 560, hat=True, lantern=True)
    s += mist(950, 90, 0.4, "#a8c0d8", 6)
    return svg(s)


@art
def panteonero():
    s = ART["panteon"]().replace("</svg>", "") + R("#000", 0.5)[:-2] + "/>"
    s += fermin_bust(1200, 600, 1.5, rim="#ffcf8a", hat=True, lids=0.2, smile=-0.4)
    return s + "</svg>"


@art
def l_lantern_glow():
    return svg(glow(700, 900, 700, "warm", 0.55))


@art
def l_candle_glow():
    return svg(glow(800, 800, 1100, "warm", 0.35))


@art
def storm_domes():
    s = sky("#05070c", "#1a2230") + blur_ell(1600, 200, 800, 200, "#2a3448", 0.6, 3) + blur_ell(500, 260, 700, 160, "#222a38", 0.6, 3)
    s += '<path d="M1500,0 L1460,200 L1520,210 L1430,480" stroke="#e8f0ff" stroke-width="6" fill="none" opacity="0.8" filter="url(#glow)"/>'
    s += puebla_domes(1050, "#03050a", "#c8d8f0", 0.15, 9)
    s += '<rect x="0" y="1050" width="2400" height="300" fill="#020305"/>'
    return svg(s)


@art
def l_window_rain():
    r = random.Random(4); s = ""
    for _ in range(140):
        x = r.uniform(1640, 1960); y = r.uniform(260, 620)
        s += f'<path d="M{x:.0f},{y:.0f} l{r.uniform(-3,3):.0f},{r.uniform(20,50):.0f}" stroke="#cfe0ff" stroke-width="2" opacity="0.6"/>'
    return svg(s)


def marble(x, y, r_=26):
    return (f'<circle cx="{x}" cy="{y}" r="{r_}" fill="#1e5ab4"/><circle cx="{x}" cy="{y}" r="{r_}" fill="url(#whiteglow)" opacity="0.4"/>'
            f'<path d="M{x-r_*0.6},{y} Q{x},{y-r_*0.6} {x+r_*0.6},{y+r_*0.2}" stroke="#8ad0ff" stroke-width="{r_*0.2:.0f}" fill="none"/>'
            f'<circle cx="{x-r_*0.35}" cy="{y-r_*0.4}" r="{r_*0.2}" fill="#fff" opacity="0.9"/>' + glow(x, y, r_ * 4, "moon", 0.35))


@art
def marble_bed():
    s = room("night", (420, 860), occupied=True)
    s += G(720, 790, 0.42, julian_head(closed=True, rim=WARM))
    s += marble(470, 845, 14)
    return svg(s)


@art
def marble_floor():
    s = floorboards(500, "#1e160e", "#070403", 1200, n=16) + R("#0a1220", 0.45) + R("#000", 0)
    s += '<rect x="0" y="0" width="2400" height="500" fill="#000"/><rect x="0" y="440" width="2400" height="60" fill="#0a0a0c"/>'
    s += marble(1200, 980, 40) + glow(1200, 1000, 500, "moon", 0.15)
    return svg(s)


@art
def marble_under():
    s = ART["under_bed"]().replace("</svg>", "")
    s += marble(1200, 980, 34)
    return s + "</svg>"


@art
def hand_marble():
    s = R("#010204") + floorboards(800, "#0c0806", "#020101", 1200, n=20) + R("#000", 0.4)
    s += place(1300, 1400, -20, 1.4, hand("claw", rim=MOONRIM, seed=51, rim_side=-1))
    s += marble(1180, 860, 38)
    return svg(s)


@art
def julian_peek():
    s = R("#04070c") + glow(1900, 200, 800, "moon", 0.35)
    s += '<rect x="0" y="760" width="2400" height="120" rx="30" fill="#c8ccd4"/><path d="M0,780 C600,760 1800,760 2400,780 L2400,900 L0,900 Z" fill="#3a2230"/>'
    s += '<rect x="0" y="900" width="2400" height="450" fill="#000"/>'
    s += f'<path d="M0,780 C600,760 1800,760 2400,780" stroke="{MOONRIM}" stroke-width="5" fill="none" opacity="0.6"/>'
    s += G(1200, 690, 1.35, julian_head(fear=True, look=0.0))
    return svg(s)


@art
def old_photo():
    s = R("#3a2418")
    s += '<rect x="500" y="160" width="1400" height="1030" fill="#ece2c8" transform="rotate(-3 1200 675)"/>'
    p = '<rect x="560" y="220" width="1280" height="860" fill="#8a7454"/>'
    p += '<path d="M560,780 L1840,780 L1840,1080 L560,1080 Z" fill="#6a5a40"/>'
    for x in (700, 1100, 1500):
        p += f'<path d="M{x-120},780 L{x-120},440 Q{x},340 {x+120},440 L{x+120},780 Z" fill="#4a3a28"/>'
    # two children: girl with braids, older boy
    p += '<path d="M960,1000 L1000,700 C1000,640 1080,640 1080,700 L1120,1000 Z" fill="#2a2018"/><circle cx="1040" cy="650" r="50" fill="#5a4630"/>'
    p += '<path d="M995,650 C980,720 985,780 990,820 M1085,650 C1100,720 1095,780 1090,820" stroke="#1a140e" stroke-width="16" fill="none"/>'
    p += '<path d="M1260,1000 L1300,640 C1300,570 1400,570 1400,640 L1440,1000 Z" fill="#2a2018"/><circle cx="1350" cy="590" r="56" fill="#5a4630"/>'
    p += '<path d="M1300,560 C1320,520 1380,520 1400,560" stroke="#1a140e" stroke-width="20" fill="none"/>'
    p += '<rect x="560" y="220" width="1280" height="860" fill="url(#paper)"/>'
    s += f'<g transform="rotate(-3 1200 675)">{p}</g>' + '<rect width="2400" height="1350" fill="#c89a60" opacity="0.18"/>'
    return svg(s)


@art
def chucho_fountain():
    s = ART["patio_day"]().replace("</svg>", "")
    s += R("#2a1c10", 0.35)[:-2] + "/>"
    s += '<path d="M1140,1200 L1150,1080 C1150,1030 1250,1030 1250,1080 L1260,1200 Z" fill="#1a120c"/><circle cx="1200" cy="1030" r="44" fill="#1a120c"/>'
    s += '<path d="M1150,1080 L1100,1180 M1250,1080 L1300,1180" stroke="#1a120c" stroke-width="22"/>'
    return s + "</svg>"


@art
def wrist_marks():
    s = R("#d8ccb4") + '<rect width="2400" height="1350" fill="url(#paper)"/>' + floorboards(0, "#c8b090", "#8a7458", 1200, n=12) + R("#e8dcc4", 0.5)
    g = uid("wm")
    s += f'<defs>{grad_lin(g, [(0, "#6a4430", 1), (0.45, "#b07a58", 1), (0.8, "#d8a07a", 1), (1, "#a8714e", 1)], 0, 960, 0, 520)}</defs>'
    s += f'<path d="M-100,620 C500,560 1100,540 1600,560 L1600,900 C1100,900 500,920 -100,980 Z" fill="url(#{g})"/>'
    # small hand at the right, relaxed
    s += f'<path d="M1560,560 C1700,520 1860,540 1960,600 C2100,620 2240,640 2300,700 C2260,740 2120,720 2000,700 C2080,760 2060,820 1980,840 C1880,900 1700,910 1560,900 Z" fill="url(#{g})"/>'
    for i in range(3):
        s += f'<path d="M{1990+i*20},{720+i*40} C{2120+i*20},{740+i*40} {2220},{770+i*40} {2260-i*20},{800+i*44}" stroke="#a8714e" stroke-width="46" fill="none" stroke-linecap="round"/>'
    r = random.Random(4)
    for i in range(5):  # finger-shaped bruises wrapping the wrist
        x = 1000 + i * 110
        s += f'<path d="M{x},{545} C{x+30},{650} {x+20},{780} {x+40},{900}" stroke="#4a2a5a" stroke-width="{58-i*3}" fill="none" stroke-linecap="round" opacity="0.6" filter="url(#blur1)"/>'
        s += f'<path d="M{x+6},{560} C{x+30},{650} {x+24},{780} {x+44},{890}" stroke="#7a3a4a" stroke-width="20" fill="none" stroke-linecap="round" opacity="0.4" filter="url(#blur1)"/>'
    return svg(s + R("#2a1a10", 0.12))


@art
def coin_pillow():
    s = R("#1a1008") + glow(600, 800, 900, "warm", 0.7)
    s += '<ellipse cx="1200" cy="800" rx="1000" ry="380" fill="#d8dce2"/>'
    for i in range(8):
        s += f'<path d="M{400+i*200},560 q40,200 -20,460" stroke="#a8acb4" stroke-width="8" fill="none" opacity="0.6"/>'
    s += '<path d="M200,900 C600,980 1400,1000 2200,900 L2400,1350 L0,1350 Z" fill="#e8ecf0"/>'
    s += coin(1200, 960, 90, 0.5) + glow(1200, 960, 260, "white", 0.4)
    return svg(s)


@art
def julian_pulled():
    s = R("#020305") + glow(1200, 300, 900, "moon", 0.3)
    s += '<rect x="0" y="600" width="2400" height="120" fill="#c8ccd4"/><rect x="0" y="560" width="2400" height="60" fill="#3a2230"/>'
    s += '<rect x="0" y="720" width="2400" height="630" fill="#000"/>'
    s += G(900, 520, 1.2, julian_head(fear=True, look=0.4, turn=0.2))
    s += child_arm([(1050, 640), (1200, 760), (1320, 960), (1380, 1150)], w=80)
    s += place(1420, 1500, -10, 1.1, hand("grab", rim=MOONRIM, seed=61, rim_side=-1))
    return svg(s)


@art
def abyss():
    s = R("#000")
    s += '<rect x="0" y="0" width="2400" height="200" fill="#0a0a0e"/><rect x="0" y="180" width="2400" height="30" fill="#1a1a1e"/>'
    for i in range(8):  # receding floorboard edges falling into the void
        y = 260 + i * 80; w = 1200 - i * 130
        s += f'<path d="M{1200-w},{y} L{1200+w},{y}" stroke="#1a120c" stroke-width="{14-i}" opacity="{0.8-i*0.09:.2f}"/>'
    s += glow(1200, 1150, 600, "moon", 0.18) + glow(1200, 1150, 200, "warm", 0.25)
    return svg(s)


@art
def l_coins():
    r = random.Random(7); s = ""
    for _ in range(26):
        x = r.uniform(700, 1700); y = r.uniform(500, 1300); rr = r.uniform(10, 28)
        s += coin(round(x), round(y), round(rr), r.uniform(0.3, 0.7), op=round(r.uniform(0.3, 0.8), 2))
    return svg(s)


@art
def coin_give():
    s = R("#020305") + glow(1200, 700, 800, "moon", 0.3)
    s += child_arm([(1200, -60), (1210, 200), (1220, 420)], w=90)
    s += coin(1250, 600, 46, 0.7) + glow(1250, 600, 200, "white", 0.5)
    s += place(1250, 1420, 0, 1.25, hand("cup", rim=MOONRIM, seed=71, rim_side=-1)).replace("scale(1.25)", "scale(1.25,-1.25)") if False else ""
    s += place(1250, 1420, 0, 1.15, hand("cup", rim=MOONRIM, seed=71, rim_side=-1))
    return svg(s)


@art
def julian_floor():
    s = room("dawn", None, bed=False, window=True)
    s += '<rect x="400" y="900" width="1600" height="60" fill="#0a0a0c"/><rect x="400" y="860" width="1600" height="60" fill="#c8ccd4"/>'  # bed edge
    s += '<rect x="420" y="960" width="18" height="220" fill="#0a0a0c"/><rect x="1960" y="960" width="18" height="220" fill="#0a0a0c"/>'
    s += '<path d="M800,1180 C820,1100 960,1060 1100,1080 C1260,1100 1360,1140 1380,1180 Z" fill="#7a90b8"/>'  # curled-up boy in pajamas
    s += G(760, 1130, 0.38, julian_head(closed=True, rim="#cfe0f0"))
    s += '<rect x="400" y="960" width="1600" height="230" fill="#0a1220" opacity="0.35"/>'
    return svg(s)


def boleta_paper(red=False):
    s = '<path d="M700,200 L1720,180 L1740,1160 L690,1180 Z" fill="#d8c48a"/>'
    s += '<path d="M700,200 L1720,180 L1740,1160 L690,1180 Z" fill="url(#paper)"/>'
    r = random.Random(3)
    for _ in range(14):
        s += blur_ell(r.uniform(720, 1700), r.uniform(220, 1140), r.uniform(30, 120), r.uniform(20, 80), "#8a6a30", 0.25, 2)
    s += '<text x="1220" y="330" text-anchor="middle" font-family="IM FELL English" font-size="64" fill="#3a2a14">Casa de Empeño</text>'
    s += '<text x="1220" y="400" text-anchor="middle" font-family="IM FELL English" font-size="40" fill="#3a2a14">Puebla de los Ángeles</text>'
    s += '<path d="M780,440 L1660,430" stroke="#3a2a14" stroke-width="3"/>'
    for i, t in enumerate(("Prenda:  un anillo de oro", "Nombre:  ________________", "Plazo:  tres meses", "Interés:  ________")):
        s += f'<text x="800" y="{540+i*90}" font-family="IM FELL English" font-size="48" fill="#3a2a14" font-style="italic">{t}</text>'
    s += '<text x="1240" y="630" font-family="IM FELL English" font-size="44" fill="#2a1a0a" font-style="italic">Ma. de la Luz</text>'
    if red:
        s += '<text x="1220" y="1030" text-anchor="middle" font-family="IM FELL English" font-size="96" fill="#a8141a" transform="rotate(-6 1220 1030)">Abono 1 de 3</text>'
    else:
        s += '<text x="1220" y="1030" text-anchor="middle" font-family="IM FELL English" font-size="96" fill="#a8141a" opacity="0.35" transform="rotate(-6 1220 1030)">Abono 1 de 3</text>'
    s += '<path d="M690,1180 L760,1100 L820,1170 L900,1120 L960,1180 Z" fill="#3a2418"/>'  # torn corner
    return s


@art
def boleta():
    return svg(R("#2a1c12") + glow(1200, 600, 900, "warm", 0.4) + boleta_paper(False))


@art
def boleta_red():
    return svg(R("#2a1c12") + glow(1200, 600, 900, "warm", 0.4) + boleta_paper(True))


@art
def julian_old():
    s = R("#140c08") + glow(600, 900, 900, "warm", 0.8) + candle(560, 1000, 90, 22)
    s += fermin_bust(1300, 600, 1.5, rim=WARM, hat=False, lids=0.4, smile=0.0)
    return svg(s)


@art
def radio_night():
    s = R("#100a06") + glow(1200, 700, 900, "warm", 0.6)
    s += '<rect x="0" y="1000" width="2400" height="350" fill="#2a1a10"/><path d="M0,1000 L2400,1000" stroke="#ffcf8a" stroke-width="4" opacity="0.5"/>'
    s += '<rect x="800" y="560" width="800" height="460" rx="40" fill="#4a2a14"/><rect x="830" y="590" width="740" height="400" rx="30" fill="#5e3a1c"/>'
    s += '<rect x="880" y="640" width="400" height="300" rx="20" fill="#2a1a0c"/>'
    for i in range(10):
        s += f'<path d="M900,{660+i*28} L1260,{660+i*28}" stroke="#4a3018" stroke-width="8"/>'
    s += '<rect x="1320" y="660" width="210" height="90" rx="8" fill="#ffd27a"/>' + glow(1425, 705, 200, "warm", 0.8)
    s += '<path d="M1340,720 L1510,720" stroke="#6a3a10" stroke-width="3"/><path d="M1400,680 L1400,740" stroke="#c8141a" stroke-width="4"/>'
    s += '<circle cx="1370" cy="860" r="40" fill="#2a1a0c"/><circle cx="1480" cy="860" r="40" fill="#2a1a0c"/>'
    s += '<path d="M900,640 C1100,600 1400,600 1560,640" stroke="#ffcf8a" stroke-width="4" fill="none" opacity="0.6"/>'
    return svg(s)


@art
def quemada_tease():
    s = stars_sky("#05060c", "#2a1a1a", 120, 30, 500)
    s += facade(0, 1050, 1000, 700, "#0e0a0a", 31, 0.2) + facade(1400, 1050, 1000, 700, "#0e0a0a", 32, 0.2)
    s += cobbles(1050, 1350, "#1a1414", 31, True)
    s += glow(1200, 800, 700, "red", 0.35) + glow(1200, 900, 400, "warm", 0.6)
    s += woman_sil(1200, 1180, 760, "#050304", "#ff8a50")
    s += '<path d="M1060,1180 C1080,900 1120,600 1150,420 L1250,420 C1280,600 1320,900 1340,1180" fill="#050304" opacity="0.6"/>'  # long veil
    return svg(s)


if __name__ == "__main__":
    os.makedirs("art", exist_ok=True)
    names = sys.argv[1:] or list(ART)
    for n in names:
        open(f"art/{n}.svg", "w").write(ART[n]())
    print(len(names), "svg written")
