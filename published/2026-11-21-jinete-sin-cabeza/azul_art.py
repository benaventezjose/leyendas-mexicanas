#!/usr/bin/env python3
"""Illustrations for 'La Casa de los Azulejos' (Ciudad de México) — writes art/*.svg (2400x1350).
Reuses helpers of earlier videos (beso_art, chars, base_chars, qm_art, aguacate_art, pas_art, sb_art, cadejo_art, monja_art).
New here: Talavera tile patterns, the tiled facade of the Valle de Orizaba palace (plain / tiled / dawn / fire / today),
the grand staircase with tiled dado, don Diego (old count) with his candle and as a ghost, the son, the father,
Manuel Palacios, the 1828 riot, the Puebla talavera workshop, the Sanborns patio.
Usage: python3 make_art.py [name ...]   then: node /home/claude/pipeline/render_svg.js art/*.svg"""
import sys, os, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '/home/claude/pipeline'); sys.path.insert(0, HERE)
from art import *
from chars import place, man_full, woman_full, luis_bust, father_bust, carmen_bust, noble_bust, SIL
from base_chars import uid, grad_lin, grad_rad
import beso_art as BA
from beso_art import S, clouds, room_walls, candle_at, flame, table_wood, portrait_bg, MOONRIM
import qm_art as QM
import sb_art as SB
import cadejo_art as CJ
import monja_art as MJ

A = os.path.join(HERE, "art"); os.makedirs(A, exist_ok=True)
ART = {}
def art(fn):
    ART[fn.__name__] = fn; return fn

WARM = "#ffcf8a"; RED = "#c8141a"
inner = MJ.inner
COB = "#1d3f93"; COB2 = "#2c5cc0"; TWHITE = "#ece6d6"; TYEL = "#d9a43a"; TGREEN = "#3f7a4a"


def dim(op=0.3, col="#02040a"):
    return f'<rect width="2400" height="1350" fill="{col}" opacity="{op}"/>'


def crop(svgstr, k, cx, cy, extra=""):
    if not svgstr.lstrip().startswith("<svg"): svgstr = S(svgstr)
    return S(f'<g transform="translate(1200,675) scale({k}) translate({-cx},{-cy})">{inner(svgstr)}</g>', extra)


def ghostify(frag, op=0.9):
    """pale blue, slightly glowing version of any fragment"""
    return (f'<defs><filter id="gcm" filterUnits="userSpaceOnUse" x="0" y="0" width="2400" height="1350">'
            f'<feColorMatrix type="matrix" values="0.25 0.35 0.2 0 0.18  0.3 0.4 0.25 0 0.26  0.35 0.45 0.3 0 0.36  0 0 0 1 0"/>'
            f'<feGaussianBlur stdDeviation="1.2"/></filter></defs><g filter="url(#gcm)" opacity="{op}">{frag}</g>')


# ============================================================================ TALAVERA
def tile_motif(sz, seed=0, palette=None, crack=False):
    """one Talavera tile (sz x sz at origin): white glaze, cobalt rosette, yellow centre, corner quarter-flowers."""
    c1, c2, w, y = palette or (COB, COB2, TWHITE, TYEL)
    h = sz / 2; r = random.Random(seed)
    cid = uid("tc")
    s = f'<defs><clipPath id="{cid}"><rect width="{sz}" height="{sz}"/></clipPath></defs><g clip-path="url(#{cid})">'
    s += f'<rect width="{sz}" height="{sz}" fill="{w}"/>'
    s += f'<rect width="{sz}" height="{sz}" fill="none" stroke="#b8b09a" stroke-width="{sz*0.02:.1f}"/>'
    # rosette petals
    for i in range(8):
        a = i * 45
        s += (f'<path d="M{h},{h} C{h+sz*0.06},{h-sz*0.12} {h+sz*0.05},{h-sz*0.3} {h},{h-sz*0.36} C{h-sz*0.05},{h-sz*0.3} {h-sz*0.06},{h-sz*0.12} {h},{h} Z" '
              f'fill="{c1 if i%2==0 else c2}" transform="rotate({a} {h} {h})"/>')
    s += f'<circle cx="{h}" cy="{h}" r="{sz*0.1:.1f}" fill="{y}"/><circle cx="{h}" cy="{h}" r="{sz*0.045:.1f}" fill="{c1}"/>'
    # corner quarter flowers (they join into flowers across tiles)
    for cx, cy in ((0, 0), (sz, 0), (0, sz), (sz, sz)):
        s += f'<circle cx="{cx}" cy="{cy}" r="{sz*0.16:.1f}" fill="{c1}"/><circle cx="{cx}" cy="{cy}" r="{sz*0.08:.1f}" fill="{y}"/>'
    # tendrils
    for i in range(4):
        a = 45 + i * 90
        s += (f'<path d="M{h},{h-sz*0.38} q{sz*0.08},{-sz*0.04} {sz*0.12},{-sz*0.1}" stroke="{c1}" stroke-width="{sz*0.025:.1f}" fill="none" '
              f'transform="rotate({a} {h} {h})"/>')
    # glaze irregularity
    s += f'<rect width="{sz}" height="{sz}" fill="#fff" opacity="{r.uniform(0.0, 0.12):.2f}"/>'
    if crack:
        s += (f'<path d="M{sz*0.1},{sz*0.2} L{sz*0.38},{sz*0.42} L{sz*0.33},{sz*0.6} L{sz*0.62},{sz*0.78} L{sz*0.9},{sz*0.95} '
              f'M{sz*0.38},{sz*0.42} L{sz*0.7},{sz*0.3} L{sz*0.95},{sz*0.36} M{sz*0.33},{sz*0.6} L{sz*0.12},{sz*0.8}" '
              f'stroke="#140c08" stroke-width="{sz*0.018:.1f}" fill="none"/>')
    return s + '</g>'


def tile_pattern(pid, sz=60, palette=None):
    return (f'<defs><pattern id="{pid}" width="{sz}" height="{sz}" patternUnits="userSpaceOnUse">{tile_motif(sz, 1, palette)}</pattern></defs>')


def tiles_rect(x, y, w, h, sz=60, palette=None, pid=None):
    pid = pid or uid("tp")
    return tile_pattern(pid, sz, palette) + f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#{pid})"/>'


# ============================================================================ FACADE
def facade_svg(mood="night", tiled=True, modern=False, people=False):
    """Frontal view of the Valle de Orizaba palace on calle de San Francisco (Madero): two storeys + entresuelo,
    tiled walls framed by grey cantera, iron balconies, merlons/pinnacles on the parapet, central portal."""
    skies = {"night": ("#040a16", "#14283e"), "dawn": ("#2a3a5e", "#e8a070"), "day": ("#4a78a8", "#b8d0e0"),
             "fire": ("#0a0204", "#4a1408"), "today": ("#06101e", "#1a3048"), "plain": ("#5a7898", "#d0c0a0")}
    s = sky(*skies[mood])
    if mood in ("night", "today"): s += stars(60, 3, 220) + glow(2050, 120, 420, "moon", 0.6)
    if mood == "fire": s += glow(400, 200, 900, "red", 0.7) + glow(2100, 300, 700, "red", 0.5)
    if mood == "dawn": s += glow(1900, 330, 900, "warm", 0.6)
    X0, X1, YT, YB = 120, 2280, 150, 1240
    stone = {"night": "#3a3c48", "dawn": "#8a7a72", "day": "#a8a092", "fire": "#4a2a22", "today": "#40424e", "plain": "#9a8e80"}[mood]
    wallc = {"night": "#2a2c36", "dawn": "#9a8478", "day": "#b4a898", "fire": "#3a1e18", "today": "#2e303a", "plain": "#a49688"}[mood]
    pal = None
    if mood in ("night", "today"): pal = ("#162a5a", "#22407a", "#7a8498", "#7a6a40")
    if mood == "fire": pal = ("#2a1a40", "#3a2a58", "#c09070", "#d08a40")
    if mood == "dawn": pal = ("#1d3f93", "#2c5cc0", "#f2d8c0", "#e0a040")
    # main wall
    s += f'<rect x="{X0}" y="{YT}" width="{X1-X0}" height="{YB-YT}" fill="{wallc}"/>'
    if tiled:
        s += tiles_rect(X0, YT + 40, X1 - X0, YB - YT - 40, 46, pal)
    else:
        s += f'<rect x="{X0}" y="{YT}" width="{X1-X0}" height="{YB-YT}" fill="#000" filter="url(#plaster)" opacity="0.4"/>'
    # cantera bands: floor lines, pilasters
    for yy in (520, 880):
        s += f'<rect x="{X0-20}" y="{yy}" width="{X1-X0+40}" height="36" fill="{stone}"/><rect x="{X0-20}" y="{yy+30}" width="{X1-X0+40}" height="8" fill="#000" opacity="0.35"/>'
    for xx in (X0, 760, 1640, X1 - 60):
        s += f'<rect x="{xx}" y="{YT}" width="60" height="{YB-YT}" fill="{stone}"/><rect x="{xx+50}" y="{YT}" width="10" height="{YB-YT}" fill="#000" opacity="0.3"/>'
    # parapet with merlons / pinnacles
    s += f'<rect x="{X0-30}" y="{YT-10}" width="{X1-X0+60}" height="56" fill="{stone}"/>'
    for i in range(23):
        x = X0 + 20 + i * 94
        s += f'<path d="M{x},{YT-10} L{x},{YT-50} Q{x+18},{YT-90} {x+36},{YT-50} L{x+36},{YT-10} Z" fill="{stone}"/>'
        s += f'<circle cx="{x+18}" cy="{YT-92}" r="9" fill="{stone}"/>'
    rimc = {"night": MOONRIM, "today": MOONRIM, "fire": "#ff7040", "dawn": "#ffd8a0", "day": "#fff0d0", "plain": "#fff0d0"}[mood]
    s += f'<path d="M{X0-30},{YT-10} L{X1+30},{YT-10}" stroke="{rimc}" stroke-width="4" opacity="0.6"/>'
    lit = mood in ("night", "fire", "today")
    # windows: upper floor balconies + entresuelo small windows + ground doors
    cols = [300, 520, 980, 1200, 1420, 1880, 2100]
    for i, x in enumerate(cols):
        # upper balcony window
        s += f'<rect x="{x-80}" y="250" width="160" height="250" fill="{stone}"/>'
        glass = "#ffc865" if (lit and i in (1, 4, 5)) else "#0a0e16"
        if mood == "fire" and i in (2, 4): glass = "#ff8040"
        s += f'<rect x="{x-62}" y="268" width="124" height="232" fill="{glass}" opacity="{0.85 if glass != "#0a0e16" else 1}"/>'
        s += f'<path d="M{x},268 L{x},500" stroke="#05070a" stroke-width="8"/>'
        if glass != "#0a0e16": s += glow(x, 380, 200, "warm" if glass == "#ffc865" else "red", 0.45)
        s += BA.rail(((x - 110, 450), (x + 110, 450)), ((x - 110, 520), (x + 110, 520)), 7, hi=rimc)
        s += f'<rect x="{x-120}" y="516" width="240" height="18" fill="#1a1820"/>'
        # entresuelo window (with iron grille)
        if x != 1200:
            s += f'<rect x="{x-70}" y="610" width="140" height="160" fill="{stone}"/><rect x="{x-56}" y="624" width="112" height="132" fill="#080a10"/>'
            for k in range(5): s += f'<rect x="{x-50+k*24}" y="624" width="6" height="132" fill="#1a1c22"/>'
        # ground floor shop door
        if x not in (1200,):
            s += f'<path d="M{x-80},{YB} L{x-80},1000 Q{x},950 {x+80},1000 L{x+80},{YB} Z" fill="{stone}"/>'
            dc = "#ffcf8a" if (modern and lit) else "#120c08"
            s += f'<path d="M{x-64},{YB} L{x-64},1010 Q{x},968 {x+64},1010 L{x+64},{YB} Z" fill="{dc}" opacity="{0.8 if modern else 1}"/>'
    # central portal (two storeys high, cantera, columns)
    s += f'<rect x="1040" y="590" width="320" height="{YB-590}" fill="{stone}"/>'
    s += f'<path d="M1080,{YB} L1080,860 Q1200,760 1320,860 L1320,{YB} Z" fill="#160e08"/>'
    if modern and lit: s += f'<path d="M1100,{YB} L1100,880 Q1200,790 1300,880 L1300,{YB} Z" fill="#ffcf8a" opacity="0.55"/>' + glow(1200, 1050, 380, "warm", 0.5)
    for xx in (1050, 1316):
        s += f'<rect x="{xx}" y="640" width="34" height="{YB-640}" fill="#000" opacity="0.18"/>'
    s += f'<path d="M1040,600 L1360,600 L1330,560 L1070,560 Z" fill="{stone}"/>'
    s += f'<rect x="1130" y="620" width="140" height="160" fill="#0a0e16"/>' + (f'<rect x="1140" y="630" width="120" height="140" fill="#ffc865" opacity="0.5"/>' if lit else "")
    # street + lamps
    s += cobbles(YB, 1350, "#141820" if mood != "day" else "#5a5048")
    if lit:
        s += lamp(80, 1300, 520, "#05070a", True) + lamp(2330, 1300, 520, "#05070a", True)
    if mood == "fire":
        s += clouds(14, 0, 500, 9, "#2a0a06", (0.3, 0.6)) + glow(1200, 1350, 1200, "red", 0.4)
    if mood == "night":
        s += clouds(10, 1100, 1350, 5, "#b0c4d8", (0.08, 0.18))
    if people:
        r = random.Random(4)
        for i in range(9):
            x = 200 + i * 240 + r.randint(-40, 40)
            s += villager_sil(x, 1330, r.randint(330, 380), r)
    return s


def villager_sil(x, y, h, r, col="#06070a"):
    k = h / 900
    hat = r.random() < 0.6
    s = f'<g transform="translate({x},{y}) scale({k})" fill="{col}">'
    s += '<path d="M-60,0 L-50,-430 C-70,-520 -80,-640 -60,-700 C-30,-740 30,-740 60,-700 C80,-640 70,-520 50,-430 L60,0 Z"/>'
    s += '<ellipse cx="0" cy="-780" rx="48" ry="56"/>'
    if hat: s += '<path d="M-110,-810 C-60,-830 60,-830 110,-810 C80,-796 -80,-796 -110,-810 Z"/><path d="M-44,-812 C-40,-880 40,-880 44,-812 Z"/>'
    return s + '</g>'


@art
def facade_night(): return S(facade_svg("night"))
@art
def facade_red(): return S(facade_svg("fire"))
@art
def facade_dawn(): return S(facade_svg("dawn"))
@art
def facade_day(): return S(facade_svg("day", people=True))
@art
def facade_plain(): return S(facade_svg("plain", tiled=False, people=True))
@art
def facade_today(): return S(facade_svg("today", modern=True))
def door_svg(open_=False):
    s = '<rect width="2400" height="1350" fill="#04060c"/>' + tiles_rect(0, 0, 2400, 1150, 120, ("#162a5a", "#22407a", "#7a8498", "#7a6a40"))
    s += '<rect x="560" y="60" width="1280" height="1090" fill="#3a3c48"/>'
    s += '<path d="M680,1150 L680,520 Q1200,140 1720,520 L1720,1150 Z" fill="#4a4c58"/>'
    s += '<path d="M680,520 Q1200,140 1720,520" stroke="#7a9cc4" stroke-width="6" fill="none" opacity="0.6"/>'
    if open_:
        s += '<path d="M760,1150 L760,560 Q1200,240 1640,560 L1640,1150 Z" fill="#ffc865" opacity="0.55"/>' + glow(1200, 900, 600, "warm", 0.7)
        s += '<path d="M760,1150 L760,560 Q900,450 1000,420 L1000,1150 Z" fill="#2a1a0e"/><path d="M1640,1150 L1640,560 Q1500,450 1400,420 L1400,1150 Z" fill="#2a1a0e"/>'
    else:
        s += '<path d="M760,1150 L760,560 Q1200,240 1640,560 L1640,1150 Z" fill="#2a1a0e"/>'
        for i in range(7):
            for j in range(9):
                s += f'<circle cx="{840+i*120}" cy="{620+j*60}" r="12" fill="#8a7a5a"/>'
        s += '<path d="M1200,320 L1200,1150" stroke="#120a06" stroke-width="16"/>'
        s += '<circle cx="1140" cy="860" r="34" stroke="#9a8a6a" stroke-width="10" fill="none"/><circle cx="1260" cy="860" r="34" stroke="#9a8a6a" stroke-width="10" fill="none"/>'
    s += cobbles(1150, 1350, "#141820")
    s += glow(2200, 100, 700, "moon", 0.4)
    return s


@art
def door_night(): return S(door_svg(False), clouds(8, 1050, 1350, 3, "#b0c4d8", (0.1, 0.2)), dim(0.15))
@art
def door_open():
    s = door_svg(True)
    s += f'<g transform="translate(1180,1170) rotate(18)">{tile_motif(160, 2, crack=True)}</g>'
    s += place(woman_full(rebozo_head=True, candle=True, old=True, rim="#ffb860"), 1000, 1160, 0.7)
    return S(s, clouds(8, 1050, 1350, 5, "#b0c4d8", (0.1, 0.2)))


@art
def tile_close():
    s = '<rect width="2400" height="1350" fill="#0a0a0a"/>' + tiles_rect(-60, -60, 2600, 1500, 300)
    s += '<rect width="2400" height="1350" fill="#000" filter="url(#grain)" opacity="0.15"/>'
    return S(s, glow(1500, 400, 1100, "warm", 0.25))
@art
def tile_close2():
    pal = ("#1d3f93", "#2c5cc0", "#ece6d6", "#d9a43a")
    s = tiles_rect(-80, -80, 2600, 1500, 220, pal)
    s += '<rect width="2400" height="1350" fill="url(#beamw)" opacity="0.35"/>'
    return S(s)
@art
def tile_crack():
    s = '<rect width="2400" height="1350" fill="#060303"/>' + glow(1200, 675, 1000, "red", 0.5)
    s += f'<g transform="translate(1200,700) rotate(14) translate(-420,-420)">{tile_motif(840, 5, crack=True)}</g>'
    s += '<rect width="2400" height="1350" fill="#400" opacity="0.25"/>'
    return S(s)
@art
def tile_stacks():
    s = room_walls("#3a2a1c", "#100a06", "#1a120a") + glow(1700, 300, 900, "warm", 0.5)
    for row in range(4):
        for i in range(9):
            x = 260 + i * 210; y = 1180 - row * 120
            s += f'<g transform="translate({x},{y}) skewX(-8)">{tile_motif(150, i + row, None)}</g>'
            s += f'<rect x="{x}" y="{y+150}" width="150" height="16" fill="#2a1c10"/>'
    s += '<path d="M200,1330 L2200,1330" stroke="#000" stroke-width="40"/>'
    return S(s)
@art
def painting_tile():
    s = '<rect width="2400" height="1350" fill="#120c08"/>' + glow(900, 500, 1000, "warm", 0.6)
    s += table_wood(860)
    s += f'<g transform="translate(820,560) rotate(-6)"><rect x="-10" y="-10" width="520" height="520" fill="#a89a80"/>{tile_motif(500, 7)}</g>'
    # hand with brush
    s += '<path d="M1800,1350 C1700,1100 1560,900 1380,820 C1340,800 1300,820 1310,860 C1330,900 1400,930 1460,990 C1520,1060 1600,1200 1640,1350 Z" fill="#b07a58"/>'
    s += '<path d="M1380,820 C1340,800 1300,820 1310,860" stroke="#ffcf8a" stroke-width="6" fill="none" opacity="0.6"/>'
    s += '<path d="M1330,830 L1120,690" stroke="#5a3a1a" stroke-width="16" stroke-linecap="round"/><path d="M1120,690 L1060,650" stroke="#1d3f93" stroke-width="22" stroke-linecap="round"/>'
    for i, c in enumerate((COB, TYEL, TGREEN, "#8a2a1a")):
        s += f'<ellipse cx="{500+i*140}" cy="1180" rx="56" ry="26" fill="#d8d0c0"/><ellipse cx="{500+i*140}" cy="1176" rx="40" ry="16" fill="{c}"/>'
    s += candle_at(300, 980, 220)
    return S(s)
@art
def taller():
    s = '<rect width="2400" height="1350" fill="#140a06"/>'
    # adobe arches and kiln
    s += '<path d="M0,1350 L0,300 L2400,300 L2400,1350 Z" fill="#2a1a10"/>'
    s += '<path d="M1500,1250 L1500,620 Q1800,420 2100,620 L2100,1250 Z" fill="#3a2214"/><path d="M1640,1250 L1640,860 Q1800,760 1960,860 L1960,1250 Z" fill="#ff6a20"/>'
    s += glow(1800, 1050, 700, "red", 0.7) + glow(1800, 1050, 400, "warm", 0.8)
    s += clouds(8, 300, 700, 4, "#3a2a20", (0.3, 0.5))
    # shelves of plates and pots
    for row in range(3):
        y = 520 + row * 220
        s += f'<rect x="120" y="{y+120}" width="1200" height="20" fill="#1a0e06"/>'
        for i in range(8):
            x = 190 + i * 145
            if (i + row) % 2:
                s += f'<ellipse cx="{x}" cy="{y+70}" rx="58" ry="52" fill="#e8e0cc"/><circle cx="{x}" cy="{y+70}" r="34" fill="none" stroke="{COB}" stroke-width="10"/><circle cx="{x}" cy="{y+70}" r="10" fill="{TYEL}"/>'
            else:
                s += f'<path d="M{x-40},{y+120} C{x-70},{y+60} {x-40},{y+20} {x-20},{y+10} L{x+20},{y+10} C{x+40},{y+20} {x+70},{y+60} {x+40},{y+120} Z" fill="#e8e0cc"/><path d="M{x-48},{y+70} L{x+48},{y+70}" stroke="{COB}" stroke-width="12"/>'
    s += '<rect x="120" y="1200" width="2280" height="150" fill="#0c0604"/>'
    s += place(man_full(hat=False, cape=False, rim="#ffb860"), 1380, 1300, 0.7)
    s += '<rect width="2400" height="1350" fill="#000" filter="url(#plaster)" opacity="0.4"/>'
    return S(s)
@art
def tiling_work():
    s = facade_svg("plain", tiled=False)
    # half-tiled wall: tiles on left two thirds with scaffold
    s += f'<g clip-path="url(#tw)"><defs><clipPath id="tw"><path d="M120,190 L1500,190 L1500,1240 L120,1240 Z"/></clipPath></defs>{tiles_rect(120, 190, 1400, 1050, 46)}</g>'
    for x in range(1450, 2300, 200):
        s += f'<rect x="{x}" y="300" width="14" height="940" fill="#4a3018"/>'
    for y in (520, 880):
        s += f'<rect x="1430" y="{y}" width="860" height="22" fill="#5a3a1c"/>'
    s += place(man_full(hat=True, cape=False, rim="#fff0d0"), 1650, 520, 0.38) + place(man_full(hat=True, cape=False, rim="#fff0d0"), 1980, 880, 0.38, flip=True)
    return crop(s, 1.15, 1250, 700)


# ============================================================================ STAIRCASE
def stairs_svg(mood="night", modern=False, blood=False, mural=False):
    """The grand staircase: steps rising from lower-left to a landing (descanso) at upper right, tiled dado,
    stone banister, arched opening. Landing at about (1720, 420)."""
    bg = {"night": ("#1a1c26", "#06070c"), "candle": ("#2a2018", "#0a0604"), "today": ("#3a2e24", "#120c08"), "dark": ("#0e1018", "#030406")}[mood]
    s = f'<rect width="2400" height="1350" fill="{bg[1]}"/>'
    s += f'<rect x="0" y="0" width="2400" height="1350" fill="{bg[0]}" opacity="0.8"/>'
    s += '<rect width="2400" height="1350" fill="#000" filter="url(#plaster)" opacity="0.5"/>'
    pal = ("#1d3f93", "#2c5cc0", "#d8d0bc", "#c89a3a") if mood == "today" else ("#142858", "#1e3a78", "#5a6274", "#6a5a34")
    # tiled dado following the stairs
    s += f'<defs><clipPath id="dado"><path d="M0,1350 L0,1100 L1700,300 L2400,300 L2400,560 L1760,560 L0,1350 Z"/></clipPath></defs>'
    s += f'<g clip-path="url(#dado)">{tiles_rect(0, 280, 2400, 1100, 70, pal)}</g>'
    # mural wall area (abstract warm/dark brushwork, not a reproduction)
    if mural:
        s += '<path d="M200,880 L1600,220 L1600,60 L200,60 Z" fill="#4a3424" opacity="0.65"/>'
        r = random.Random(3)
        for i in range(26):
            x = r.randint(260, 1560); y = r.randint(80, 760 - (x - 200) // 3)
            s += f'<path d="M{x},{y} q{r.randint(-120,120)},{r.randint(-80,80)} {r.randint(-200,200)},{r.randint(-60,120)}" stroke="{r.choice(["#7a5032", "#2a1a10", "#9a6a40", "#3a2a1e"])}" stroke-width="{r.randint(20,60)}" fill="none" opacity="0.5" stroke-linecap="round"/>'
    # steps
    for i in range(13):
        x = 160 + i * 118; y = 1240 - i * 64
        c = ["#3a3430", "#2a2420"][i % 2] if mood != "dark" else ["#1a1a20", "#121218"][i % 2]
        s += f'<path d="M{x},{y} L{x+130},{y} L{x+130},{y+64} L{x},{y+64} Z" fill="{c}"/>'
        hi = "#ffb860" if mood in ("candle", "today") else "#7a9cc4"
        s += f'<path d="M{x},{y} L{x+130},{y}" stroke="{hi}" stroke-width="3" opacity="0.35"/>'
    under = {"night": "#14161e", "candle": "#1e1610", "today": "#2a2018", "dark": "#0a0b10"}[mood]
    s += f'<path d="M160,1304 L160,1350 L1820,1350 L1820,472 Z" fill="{under}"/>'
    s += f'<path d="M160,1304 L1820,472" stroke="#000" stroke-width="18" opacity="0.5"/>'
    s += '<path d="M1300,1350 L1300,1060 Q1420,960 1540,1060 L1540,1350 Z" fill="#05060a"/>'
    s += '<path d="M1300,1350 L1300,1060 Q1420,960 1540,1060 L1540,1350" stroke="#3a3430" stroke-width="20" fill="none"/>'
    # landing
    s += '<path d="M1690,472 L2400,472 L2400,560 L1690,560 Z" fill="#2a2420"/><path d="M1690,472 L2400,472" stroke="#ffb860" stroke-width="3" opacity="0.4"/>'
    # stone banister
    s += '<path d="M100,1110 L1700,290 L2400,290" stroke="#4a4440" stroke-width="34" fill="none"/>'
    s += '<path d="M100,1094 L1700,274 L2400,274" stroke="#8a9cb4" stroke-width="4" fill="none" opacity="0.35"/>'
    for i in range(14):
        x = 200 + i * 112
        y0 = 1240 - i * 61; y1 = 1050 - i * 57
        s += f'<path d="M{x},{y0} C{x-14},{(y0+y1)/2} {x+14},{(y0+y1)/2} {x},{y1}" stroke="#3a3430" stroke-width="22" fill="none"/>'
    # arch on landing
    s += '<path d="M1860,472 L1860,180 Q2060,40 2260,180 L2260,472 Z" fill="#05060a"/>'
    s += '<path d="M1860,472 L1860,180 Q2060,40 2260,180 L2260,472" stroke="#4a4440" stroke-width="30" fill="none"/>'
    if modern:
        s += '<path d="M2060,0 L2060,120" stroke="#2a2018" stroke-width="6"/>' + '<circle cx="2060" cy="150" r="40" fill="#ffd8a0"/>' + glow(2060, 150, 500, "warm", 0.6)
    if blood:
        s += '<ellipse cx="1900" cy="520" rx="160" ry="22" fill="#4a0608" opacity="0.8"/><path d="M1800,530 C1780,600 1760,650 1740,700" stroke="#3a0406" stroke-width="10" opacity="0.6"/>'
    return s


@art
def stairs(): return S(stairs_svg("night"), glow(2060, 320, 500, "moon", 0.25))
@art
def stairs_dark(): return S(stairs_svg("dark"), clouds(10, 600, 1350, 6, "#8aa0c0", (0.05, 0.12)), dim(0.2))
@art
def stairs_today(): return S(stairs_svg("today", modern=True, mural=True))
@art
def stairs_ghost(): return S(stairs_svg("dark"), glow(1980, 300, 600, "moon", 0.4), clouds(10, 600, 1350, 8, "#8aa0c0", (0.05, 0.12)))
@art
def stairs_pov():
    s = stairs_svg("dark")
    return crop(s, 1.5, 1100, 760, glow(1980, 300, 500, "moon", 0.3))


def diego_figure(rim=WARM, ghost=False, reach=False):
    """old count in levita, long white hair, holding a candle (candle hand at about (+170,-560))."""
    fill = "#9ab0cc" if ghost else "#06070a"
    s = f'<g fill="{fill}">'
    s += '<path d="M-70,-480 C-74,-330 -84,-200 -92,-10 L-44,-6 C-34,-160 -14,-300 -4,-420 C10,-300 30,-160 44,-8 L96,-12 C90,-170 80,-330 66,-480 Z"/>'
    # levita (frock coat) with tails
    s += '<path d="M-96,-760 C-120,-640 -130,-520 -120,-380 L-150,-260 C-90,-240 -40,-250 0,-280 C40,-250 90,-240 140,-260 L116,-380 C124,-520 114,-640 96,-760 C60,-800 -60,-800 -96,-760 Z"/>'
    # stooped head
    s += '<ellipse cx="30" cy="-850" rx="54" ry="64"/><path d="M-20,-890 C-50,-860 -60,-800 -70,-760 L-30,-770 C-20,-820 0,-860 20,-880 Z" opacity="0.9"/>'
    # arm with candle
    s += '<path d="M80,-740 C140,-700 170,-640 180,-570 L150,-560 C140,-620 110,-670 60,-700 Z"/>'
    if reach:
        s += '<path d="M-80,-740 C-160,-720 -240,-700 -320,-690 L-324,-660 C-240,-664 -150,-680 -70,-690 Z"/><path d="M-320,-700 C-350,-710 -370,-690 -360,-670 C-350,-650 -330,-656 -320,-664 Z"/>'
    s += '</g>'
    s += '<rect x="160" y="-640" width="20" height="70" fill="#e8dcc0"/>' + f'<path d="M170,-680 Q182,-660 170,-640 Q158,-660 170,-680 Z" fill="#ffdf8a"/>'
    s += f'<circle cx="170" cy="-650" r="200" fill="url(#warmglow)" opacity="{0.4 if ghost else 0.8}"/>'
    # white hair
    hair = "#e8eef8" if ghost else "#cfd4dc"
    for i in range(9):
        s += f'<path d="M{-10+i*8},-906 C{-30+i*4},-880 {-40+i*2},-840 {-44+i*3},-800" stroke="{hair}" stroke-width="5" fill="none" opacity="0.7"/>'
    s += f'<path d="M80,-740 C150,-690 176,-620 180,-570 M30,-914 C70,-910 90,-870 84,-820 M96,-760 C114,-640 124,-520 116,-380" stroke="{rim}" stroke-width="6" fill="none" opacity="0.8" filter="url(#blur1)"/>'
    return s


@art
def l_diego_candle(): return S(place(diego_figure(WARM), 1900, 476, 0.42))
@art
def l_ghost_diego(): return S(ghostify(place(diego_figure("#e8f2ff", ghost=True, reach=True), 1960, 476, 0.42) + glow(1960, 300, 300, "moon", 0.5), 0.85))
@art
def l_float_candle():
    x, y = 1960, 250
    return S(glow(x, y, 420, "warm", 0.55), f'<rect x="{x-10}" y="{y}" width="20" height="70" fill="#f0e6d0" opacity="0.9"/><path d="M{x},{y-40} Q{x+12},{y-18} {x},{y} Q{x-12},{y-18} {x},{y-40} Z" fill="#ffe7a0"/>')
@art
def l_intruder():
    fig = man_full(hat=True, cape=True, dagger=True, step_up=True, rim="#7a9cc4", fill="#030305")
    return S(place(fig, 720, 1010, 0.5))
@art
def l_candle_glow(): return S(glow(1900, 330, 900, "warm", 0.35))
@art
def l_fire_glow(): return S(glow(600, 300, 1100, "red", 0.4), glow(1900, 400, 900, "red", 0.3))
@art
def l_fog(): return S(clouds(18, 900, 1400, 31, "#b0c4d8", (0.08, 0.2), (300, 700), (60, 140)))


# ============================================================================ PEOPLE (busts)
def diego_bust(x, y, k, rim=WARM, ghost=False, **kw):
    b = noble_bust(x, y, k)
    return b


@art
def diego_portrait(): return S(portrait_bg("candle"), diego_bust(1200, 560, 1.75), candle_at(1900, 1300, 240))
@art
def diego_shock(): return S(portrait_bg("red"), diego_bust(1200, 560, 1.85), dim(0.15, "#300"))
@art
def ghost_diego(): return S(portrait_bg("ghost"), ghostify(diego_bust(1200, 560, 1.75), 0.85), dim(0.15, "#0a1a3a"))
@art
def ghost_eyes():
    s = '<rect width="2400" height="1350" fill="#010206"/>'
    s += ghostify(diego_bust(1200, 760, 3.4), 0.6)
    s += glow(1080, 885, 80, "white", 0.8) + glow(1300, 885, 80, "white", 0.8)
    return S(s, dim(0.25, "#020814"))
@art
def ghost_flash():
    s = '<rect width="2400" height="1350" fill="#000"/>' + ghostify(diego_bust(1200, 640, 2.8), 1.0)
    s += glow(1112, 525, 70, "white", 0.9) + glow(1290, 525, 70, "white", 0.9)
    return S(s)
@art
def father_portrait(): return S(portrait_bg("candle"), father_bust(1200, 560, 1.75, rim="#ffb860"))
@art
def father_angry(): return S(portrait_bg("red"), father_bust(1200, 560, 1.8, rim="#ff7050"), dim(0.12, "#300"))
@art
def father_tear(): return S(portrait_bg("moon").replace("#060c18", "#3a4a6a").replace("#1a2a40", "#c8906a"), father_bust(1200, 560, 1.75, rim="#ffd8a0"),
                            '<path d="M1140,470 C1136,500 1134,520 1138,540" stroke="#e8f2ff" stroke-width="7" opacity="0.8" fill="none"/>')
@art
def father_window():
    s = BA.carmen_room_svg(False)
    s += place(man_full(hat=False, cape=True, rim="#9fc2e8"), 1650, 1120, 0.85)
    return S(s, dim(0.15))
@art
def son_portrait(): return S(portrait_bg("candle"), luis_bust(1200, 560, 1.75, rim=WARM, look=-0.2, smile=0.5))
@art
def son_smile(): return S(portrait_bg("candle"), luis_bust(1200, 560, 1.75, rim=WARM, look=0.25, smile=0.9, lids=0.3))
@art
def son_shame(): return S(portrait_bg("moon"), luis_bust(1200, 600, 1.75, rim=MOONRIM, look=0.4, smile=-0.4, lids=0.6, turn=0.15), dim(0.2))
@art
def son_night(): return S(portrait_bg("candle"), luis_bust(1200, 560, 1.75, rim="#ffb860", look=-0.1, smile=0.0, lids=0.35), candle_at(1950, 1300, 200))
@art
def son_rich():
    chain = '<path d="M960,1000 C1080,1120 1320,1120 1440,1000" stroke="#d9a43a" stroke-width="10" fill="none"/><circle cx="1200" cy="1110" r="26" fill="#d9a43a"/>'
    return S(portrait_bg("moon").replace("#060c18", "#3a4a6a").replace("#1a2a40", "#c8906a"), luis_bust(1200, 560, 1.75, rim="#ffd8a0", look=0.1, smile=0.15, lids=0.35), chain)
@art
def son_room():
    s = room_walls("#2a2028", "#0c080c", "#1a120c") + table_wood(980) + candle_at(700, 980, 140)
    s += '<rect x="1500" y="260" width="420" height="560" fill="#0a0e18"/><rect x="1520" y="280" width="380" height="520" fill="#14243a"/>' + glow(1700, 500, 400, "moon", 0.3)
    s += place(man_full(hat=False, cape=False, rim="#ffb860"), 1100, 1150, 0.7)
    return S(s)
@art
def graciana(): return S(portrait_bg("moon"), carmen_bust(1200, 560, 1.75, look=0.15, lids=0.3, smile=0.2))
@art
def graciana_fear(): return S(portrait_bg("candle"), carmen_bust(1200, 560, 1.75, rim="#ffb860", look=-0.5, turn=-0.15, fear=True))
@art
def graciana_window(): return BA.ART["carmen_room"]()
@art
def countess(): return S(portrait_bg("candle"), QM.bea_bust(1200, 560, 1.75, rim=WARM, dress=("#0a1430", "#1d3f93", "#3a64b8"), look=-0.1, lids=0.3, smile=0.3))
@art
def palacios(): return S(portrait_bg("candle"), QM.martin_bust(1200, 620, 1.65, rim=WARM, look=0.2, cold=True), candle_at(1950, 1300, 160))
@art
def palacios_red(): return S(portrait_bg("red"), QM.martin_bust(1200, 620, 1.7, rim="#ff6a50", look=0.0, cold=True))


# ============================================================================ PLACES & PROPS
@art
def street_colonial():
    r = random.Random(21); s = QM.persp_street("dusk", seed=21, lamp_on=False)
    for i in range(7): s += villager_sil(300 + i * 300 + r.randint(-40, 40), 1300 + r.randint(-30, 30), r.randint(380, 470), r)
    return S(s, '<rect width="2400" height="1350" fill="#ffb060" opacity="0.08"/>')
@art
def street_dawn(): return QM.ART["street_day"]()
@art
def patio_old():
    s = room_walls("#3a3028", "#0e0a08", "#2a2018") + glow(1200, 300, 1100, "moon", 0.35)
    for i in range(6):
        x = 220 + i * 400
        s += f'<path d="M{x},1200 L{x},560 Q{x+200},380 {x+400},560" stroke="#5a4a3c" stroke-width="60" fill="none"/>'
    s += '<rect x="0" y="1200" width="2400" height="150" fill="#1a140e"/><ellipse cx="1200" cy="1180" rx="260" ry="60" fill="#3a3028"/><rect x="1180" y="1000" width="40" height="180" fill="#3a3028"/>'
    return S(s)
@art
def carriage():
    s = facade_svg("plain", tiled=False)
    c = '<g transform="translate(850,1250)" fill="#05060a">'
    c += '<path d="M-300,-120 L-260,-380 L260,-380 L300,-120 Z"/><circle cx="-200" cy="-60" r="110" fill="none" stroke="#05060a" stroke-width="24"/><circle cx="200" cy="-60" r="110" fill="none" stroke="#05060a" stroke-width="24"/>'
    c += '<circle cx="0" cy="-260" r="50" fill="#c9a24a"/><path d="M300,-200 L700,-220" stroke="#05060a" stroke-width="16"/>'
    c += '<path d="M640,-260 C660,-420 760,-500 900,-480 L940,-420 C900,-380 860,-300 850,-160 L820,0 L790,0 L780,-160 L700,-160 L690,0 L660,0 Z"/></g>'
    return crop(s + c, 1.3, 1200, 900)
@art
def gambling():
    s = '<rect width="2400" height="1350" fill="#0c0806"/>' + glow(1200, 500, 1100, "warm", 0.6)
    s += clouds(12, 200, 700, 5, "#6a5040", (0.1, 0.25))  # cigar smoke
    s += table_wood(820)
    r = random.Random(5)
    for i in range(7):
        x = 300 + i * 270; y = 820
        s += place(man_full(hat=r.random() < 0.5, cape=False, rim="#ffb860"), x, y + 120, 0.55, flip=i % 2 == 0) if i != 3 else ""
    # cards, dice, coins
    for i in range(6):
        x = 800 + i * 140; y = 960 + (i % 2) * 40
        s += f'<g transform="translate({x},{y}) rotate({r.randint(-30,30)})"><rect x="-50" y="-70" width="100" height="140" rx="8" fill="#ece6d6"/><circle cx="0" cy="0" r="22" fill="{RED if i%2 else COB}"/></g>'
    for i in range(14):
        s += f'<ellipse cx="{600+r.randint(0,1200)}" cy="{1080+r.randint(0,180)}" rx="34" ry="12" fill="#c9a24a"/>'
    s += luis_bust(1200, 660, 0.55, rim="#ffb860", smile=0.9, look=0.2)
    s += candle_at(1200, 900, 120)
    return S(s)
@art
def dice_close():
    s = '<rect width="2400" height="1350" fill="#0c0806"/>' + glow(1200, 400, 1000, "warm", 0.6) + table_wood(600)
    for x, y, a in ((950, 820, -12), (1350, 860, 20)):
        s += f'<g transform="translate({x},{y}) rotate({a})"><rect x="-130" y="-130" width="260" height="260" rx="30" fill="#ece6d6"/><rect x="-130" y="-130" width="260" height="260" rx="30" fill="none" stroke="#ffcf8a" stroke-width="5" opacity="0.6"/>'
        for px, py in ((-70, -70), (70, 70), (0, 0), (-70, 70), (70, -70)):
            s += f'<circle cx="{px}" cy="{py}" r="22" fill="#140c08"/>'
        s += '</g>'
    r = random.Random(2)
    for i in range(20): s += f'<ellipse cx="{300+r.randint(0,1800)}" cy="{1050+r.randint(0,250)}" rx="60" ry="22" fill="#c9a24a" opacity="0.9"/><ellipse cx="{300+r.randint(0,1800)}" cy="{1050+r.randint(0,250)}" rx="60" ry="22" fill="#8a6a2a"/>'
    return S(s)
@art
def confront():
    s = room_walls("#2a2420", "#0a0806", "#1a120c") + glow(1200, 400, 1000, "warm", 0.4)
    s += '<rect x="900" y="200" width="600" height="700" fill="#0a0e18"/><rect x="920" y="220" width="560" height="660" fill="#3a4a66" opacity="0.6"/>' + glow(1200, 500, 500, "white", 0.3)
    s += place(man_full(hat=False, cape=True, rim="#ffd8a0"), 760, 1250, 0.95)
    s += place(man_full(hat=False, cape=False, rim="#ffd8a0"), 1640, 1250, 0.85, flip=True)
    for x in (300, 2100): s += place(woman_full(rebozo_head=True, rim="#ffb860"), x, 1270, 0.6)
    return S(s)
@art
def road_dawn(): return CJ.ART["road_fog"]() if "road_fog" in CJ.ART else CJ.ART["road_night"]()
@art
def road_mules(): return SB.ART["road_mules"]()
@art
def l_mules(): return SB.ART["l_mules"]()
@art
def mine(): return BA.ART["mine"]()
@art
def coins(): return BA.ART["coins"]()
@art
def rider_return():
    s = facade_svg("plain", tiled=False)
    s += place(SB_rider(), 1500, 1250, 1.0)
    return crop(s, 1.3, 1300, 850)


def SB_rider():
    c = '<g fill="#05060a">'
    c += '<path d="M-300,-420 C-200,-520 100,-520 260,-460 C330,-520 380,-600 420,-640 L470,-600 C440,-520 400,-460 360,-380 L330,-200 L300,0 L270,0 L270,-200 L-200,-220 L-240,0 L-270,0 L-280,-240 C-320,-280 -330,-360 -300,-420 Z"/>'
    c += '<path d="M-60,-500 C-70,-620 -50,-720 0,-760 C40,-740 60,-640 50,-500 Z"/><ellipse cx="0" cy="-800" rx="44" ry="52"/>'
    c += '<path d="M-100,-830 C-50,-850 50,-850 100,-830 C70,-816 -70,-816 -100,-830 Z"/><path d="M-40,-834 C-36,-890 36,-890 40,-834 Z"/>'
    c += '<path d="M-50,-720 C-120,-640 -150,-560 -170,-480 L-100,-480 C-90,-560 -70,-640 -40,-700 Z"/></g>'
    c += '<path d="M-100,-830 C-50,-850 50,-850 100,-830 M0,-760 C40,-740 60,-640 50,-500 M260,-460 C330,-520 380,-600 420,-640" stroke="#fff0d0" stroke-width="5" fill="none" opacity="0.6"/>'
    return c


@art
def volcanoes_dawn(): return BA.ART["volcanoes"]()
@art
def plaza_1820(): return QM.ART["plaza_1550"]()
@art
def riot_night():
    s = QM.palacio_svg(True)
    s += glow(600, 900, 900, "red", 0.7) + glow(1800, 950, 800, "red", 0.6)
    s += clouds(16, 0, 700, 12, "#2a0806", (0.3, 0.6))
    r = random.Random(8)
    for i in range(16):
        s += villager_sil(100 + i * 150 + r.randint(-30, 30), 1340, r.randint(300, 420), r)
    for x in (500, 1300, 2000):
        s += f'<path d="M{x},1350 C{x-60},1180 {x+40},1120 {x},980 C{x+70},1100 {x+90},1200 {x+40},1350 Z" fill="#ff7a20" opacity="0.9"/>' + glow(x, 1150, 360, "warm", 0.8)
    return S(s, '<rect width="2400" height="1350" fill="#400" opacity="0.2"/>')
@art
def riot_street():
    s = QM.persp_street("night", seed=17)
    s += glow(1200, 700, 900, "red", 0.6) + clouds(14, 100, 700, 14, "#2a0806", (0.3, 0.55))
    r = random.Random(9)
    for i in range(6):
        s += villager_sil(500 + i * 260, 1300 - (i % 2) * 40, 420, r)
    return S(s, '<rect width="2400" height="1350" fill="#300" opacity="0.25"/>')
@art
def parian():
    s = sky("#0a0204", "#3a0c06") + glow(1200, 700, 1300, "red", 0.7)
    for i in range(10):
        x = 120 + i * 230
        s += f'<rect x="{x}" y="620" width="200" height="560" fill="#1a0c08"/><path d="M{x-10},620 L{x+100},520 L{x+210},620 Z" fill="#120806"/>'
        s += f'<rect x="{x+50}" y="900" width="100" height="280" fill="#ff7a20" opacity="{0.4 + (i%3)*0.2:.1f}"/>'
    s += clouds(18, 0, 700, 21, "#1a0604", (0.35, 0.7))
    r = random.Random(11)
    for i in range(12): s += villager_sil(80 + i * 200 + r.randint(-30, 30), 1350, r.randint(380, 460), r)
    s += cobbles(1180, 1350, "#1a0c08")
    return S(s)
@art
def window_break():
    s = '<rect width="2400" height="1350" fill="#04060c"/>' + tiles_rect(0, 0, 2400, 1350, 90, ("#142858", "#1e3a78", "#4a5266", "#5a4a2a"))
    s += '<rect x="760" y="240" width="880" height="900" fill="#3a3c48"/><rect x="820" y="300" width="760" height="780" fill="#020306"/>'
    for k in range(7): s += f'<rect x="{850+k*105}" y="300" width="16" height="780" fill="#1a1c22"/>'
    s += '<path d="M1060,300 L1060,1080" stroke="#020306" stroke-width="60"/>'  # one bar bent away
    s += '<path d="M1040,300 C1000,600 1100,800 1040,1080" stroke="#2a2c34" stroke-width="16" fill="none"/>'
    s += '<rect x="820" y="300" width="760" height="780" fill="#1a2a44" opacity="0.6"/>' + glow(1200, 700, 600, "moon", 0.55)
    s += place(man_full(hat=True, cape=True, rim="#cfe0ff"), 1180, 1200, 0.85)
    s += glow(2100, 200, 600, "moon", 0.4) + clouds(8, 1000, 1350, 3, "#8aa0c0", (0.06, 0.14))
    return S(s, dim(0.15))
@art
def dagger(): return BA.ART["dagger_bg"]()
@art
def candle_floor():
    s = '<rect width="2400" height="1350" fill="#060504"/>' + glow(1200, 760, 900, "warm", 0.55)
    s += '<path d="M0,900 L2400,900 L2400,1350 L0,1350 Z" fill="#1a1612"/>'
    s += tiles_rect(0, 400, 2400, 500, 100, ("#142858", "#1e3a78", "#5a6274", "#6a5a34"))
    s += '<rect x="0" y="880" width="2400" height="26" fill="#2a2420"/>'
    s += '<g transform="translate(1200,1040) rotate(-80)"><rect x="-22" y="-160" width="44" height="200" fill="#e8dcc0"/></g>'
    s += '<path d="M1060,1010 Q1080,970 1070,940 Q1050,980 1060,1010 Z" fill="#ffdf8a"/>' + glow(1066, 990, 220, "warm", 0.9)
    s += '<ellipse cx="1500" cy="1150" rx="300" ry="40" fill="#3a0608" opacity="0.55"/>'
    return S(s)
@art
def fallen_stairs():
    s = stairs_svg("candle", blood=True)
    s += '<path d="M1760,520 C1800,470 1900,450 2040,470 C2100,480 2120,510 2100,530 L1760,540 Z" fill="#06060a"/>'
    s += '<ellipse cx="2080" cy="478" rx="34" ry="26" fill="#cfd4dc"/>'
    s += '<g transform="translate(1720,540) rotate(-75)"><rect x="-10" y="-70" width="20" height="80" fill="#e8dcc0"/></g>'
    s += '<path d="M1650,528 Q1660,505 1655,490 Q1644,508 1650,528 Z" fill="#ffdf8a"/>' + glow(1655, 515, 420, "warm", 0.8)
    return S(s, dim(0.15))
@art
def servants_light():
    s = stairs_svg("candle")
    for i, x in enumerate((460, 640, 820)):
        y = 1240 - (i + 2) * 64
        s += place(woman_full(rebozo_head=True, candle=True, old=i == 1, rim="#ffb860"), x, y + 20, 0.42)
    return S(s, glow(700, 900, 700, "warm", 0.4))
@art
def servant_bed():
    s = room_walls("#201a18", "#080606", "#120c0a") + candle_at(500, 1000, 120)
    s += '<rect x="900" y="900" width="1200" height="260" fill="#3a3028"/><path d="M900,900 C1200,820 1700,820 2100,900" fill="#d8d0c0"/>'
    s += '<ellipse cx="1050" cy="860" rx="110" ry="70" fill="#e8e0d0"/>'
    s += '<path d="M1040,820 C1000,800 980,760 1010,730 C1040,710 1090,720 1100,760" fill="#1a120c"/>'
    s += '<rect x="1600" y="180" width="300" height="600" fill="#05060a"/>'
    return S(s)
@art
def watcher_street():
    s = BA.alley_full("night")
    s += place(man_full(hat=True, cape=True, rim=MOONRIM), 1200, 1250, 0.7)
    return S(s)
@art
def ballroom(): return QM.ART["ballroom"]()
@art
def waiter_stairs():
    s = stairs_svg("candle")
    s += place(man_full(hat=False, cape=False, rim="#ffb860"), 600, 1170, 0.42)
    return S(s)
@art
def revolution():
    s = facade_svg("day", tiled=True)
    s = s.replace(sky("#4a78a8", "#b8d0e0"), sky("#8a8070", "#d8c8a8"))
    r = random.Random(14)
    for i in range(10):
        x = 160 + i * 230
        s += villager_sil(x, 1340, 400, r)
        s += f'<path d="M{x+30},{1340-380} L{x+90},{1340-520}" stroke="#06070a" stroke-width="10"/>'
    return S(s, '<rect width="2400" height="1350" fill="#5a4020" opacity="0.15"/>')


def patio_svg(night=False):
    s = room_walls("#3a2e24", "#0c0806", "#2a2018") if not night else room_walls("#14161e", "#040406", "#0e0e12")
    # glass ceiling glow
    s += glow(1200, 0, 1300, "white" if not night else "moon", 0.35)
    for i in range(5):
        x = 200 + i * 500
        s += f'<path d="M{x},1050 L{x},420 Q{x+250},250 {x+500},420 L{x+500},1050" stroke="#5a4a3a" stroke-width="54" fill="none"/>'
    s += tiles_rect(0, 980, 2400, 90, 90)
    s += '<rect x="0" y="1070" width="2400" height="280" fill="#1a120c"/>'
    # tables
    for i in range(6):
        x = 260 + i * 380
        s += f'<ellipse cx="{x}" cy="1180" rx="140" ry="34" fill="{"#e8e0d0" if not night else "#3a3a44"}"/><rect x="{x-8}" y="1180" width="16" height="140" fill="#1a120c"/>'
        if not night: s += f'<path d="M{x-200},1300 L{x-180},1120 M{x+200},1300 L{x+180},1120" stroke="#2a1c10" stroke-width="12"/>'
    # hanging lamps
    for x in (500, 1200, 1900):
        s += f'<path d="M{x},0 L{x},300" stroke="#1a120c" stroke-width="5"/><circle cx="{x}" cy="320" r="34" fill="{"#ffd8a0" if not night else "#2a2a30"}"/>'
        if not night: s += glow(x, 320, 300, "warm", 0.6)
    return s


@art
def patio_today(): return S(patio_svg(False))
@art
def patio_night(): return S(patio_svg(True), clouds(10, 700, 1350, 9, "#8aa0c0", (0.05, 0.12)))
@art
def chronicle(): return QM.ART["chronicle"]().replace("La Calle de la", "Crónicas de la").replace("Quemada", "Ciudad de México")
@art
def book(): return MJ.ART["book"]().replace("La Monja de", "La Casa de").replace("La Concepción", "los Azulejos")
@art
def river_night(): return CJ.ART["bridge"]() if "bridge" in CJ.ART else SB.ART["valley_night"]()
@art
def title_bg():
    s = '<rect width="2400" height="1350" fill="#02040a"/>' + f'<g opacity="0.35">{tiles_rect(0, 0, 2400, 1350, 150, ("#142858", "#1e3a78", "#3a4256", "#5a4a2a"))}</g>'
    s += glow(1200, 675, 1100, "moon", 0.4) + dim(0.35)
    return S(s)
@art
def red_flash():
    s = '<rect width="2400" height="1350" fill="#1a0000"/>' + glow(1200, 675, 1200, "red", 0.8)
    s += '<g transform="translate(1250,640) rotate(-28)"><path d="M-40,-520 L40,-520 L20,380 L0,440 L-20,380 Z" fill="#dfe6ee"/><path d="M-140,-540 L140,-540" stroke="#b08a3a" stroke-width="40"/><rect x="-26" y="-760" width="52" height="220" fill="#2a1a10"/></g>'
    return S(s)
@art
def black(): return S('<rect width="2400" height="1350" fill="#000"/>')


def run(names):
    todo = names or list(ART)
    for n in todo:
        open(os.path.join(A, n + ".svg"), "w").write(ART[n]())
    print("wrote", len(todo))


if __name__ == "__main__":
    run(sys.argv[1:])
