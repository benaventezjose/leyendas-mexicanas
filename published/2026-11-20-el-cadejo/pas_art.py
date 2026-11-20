#!/usr/bin/env python3
"""Illustrations for 'La Pascualita' (Chihuahua) — writes art/*.svg (2400x1350).
Reuses the helpers of earlier videos (beso_art.py, chars.py, base_chars.py, qm_art.py = La Quemada,
aguacate_art.py = El Callejón del Aguacate). New here: the mannequin bride (pas_*), the daughter, the mother,
the shop La Popular, hands, black widow spider, bouquet, cathedral of Chihuahua.
Usage: python3 make_art.py [name ...]   then: node /home/claude/pipeline/render_svg.js art/*.svg"""
import sys, os, math, random, re
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '/home/claude/pipeline'); sys.path.insert(0, HERE)
from art import *
from chars import place, man_full, woman_full, strands, bust_frame, SIL, hair_carmen_back
from base_chars import head, uid, grad_lin, grad_rad
import beso_art as BA
from beso_art import S, clouds, room_walls, candle_at, flame, table_wood, portrait_bg, MOONRIM
import qm_art as QM
import aguacate_art as AG

A = os.path.join(HERE, "art"); os.makedirs(A, exist_ok=True)
ART = {}
def art(fn):
    ART[fn.__name__] = fn; return fn

WARM = "#ffcf8a"; RED = "#c8141a"
LAMP_XY = QM.LAMP_XY          # (452,445) street lantern in persp_street; interiors hang their lamp here too
CANDLE_XY = (700, 640)        # candle / lamp in interiors, l_candle_glow
WIN = (880, 330, 1720, 1060)  # shop window rect in shop_front views
SK_PAS = dict(base="#e6d0c2", light="#f3e1d5", hi="#fff3ea", shadow="#b4988a", deep="#6a5048")  # porcelain
SK_HIJA = dict(base="#d8a888", light="#ecc2a4", hi="#f8d8c0", shadow="#9a6a52", deep="#52342a")
SK_MOM = dict(base="#c89878", light="#dcb092", hi="#ecc6aa", shadow="#8a5e48", deep="#46302a")


def inner(svgstr):
    """content of an svg string without the outer <svg> wrapper (defs included)"""
    return svgstr.split(">", 1)[1].rsplit("</svg>", 1)[0]

def crop(svgstr, k, cx, cy, extra=""):
    return S(f'<g transform="translate(1200,675) scale({k}) translate({-cx},{-cy})">{inner(svgstr)}</g>', extra)


# ===================================================================== the bride (mannequin / daughter)
def hair_back(seed=4):
    r = random.Random(seed)
    s = ('<path d="M-96,-70 C-110,-150 -50,-176 0,-176 C50,-176 110,-150 96,-70 C104,-20 100,40 86,80 '
         'C60,96 30,92 0,90 C-30,92 -60,96 -86,80 C-100,40 -104,-20 -96,-70 Z" fill="#0d0907"/>')
    s += strands(r, [(-80, -120, -100, -40, -84, 70), (80, -120, 100, -40, 84, 70)], 8, "#2e221c", (1.2, 2.5), (0.3, 0.7), 6)
    return s


def hair_front(seed=5, ghost=False):
    """1930 finger-wave bob, parted on the left, waves over the temples"""
    r = random.Random(seed); c = "#0b0706" if not ghost else "#1a2230"
    cap = ('M-20,-110 C-50,-108 -70,-96 -78,-64 C-86,-30 -84,0 -80,24 C-96,10 -104,-48 -94,-96 C-80,-150 -36,-172 4,-170 '
           'C46,-170 88,-146 96,-96 C104,-48 96,10 80,24 C84,0 86,-30 78,-64 C72,-92 50,-106 30,-110 C14,-104 -4,-104 -20,-110 Z')
    s = f'<path d="{cap}" fill="{c}"/>'
    # waves (S-curves) with highlights
    for side in (-1, 1):
        for i in range(2):
            y = -156 + i * 26
            x0 = side * 20; x1 = side * (80 + i * 4)
            s += (f'<path d="M{x0},{y} C{x0+side*20},{y-12} {x0+side*40},{y+18} {x0+side*58},{y+6} C{x1-side*8},{y-6} {x1},{y+10} {x1+side*6},{y+20}" '
                  f'stroke="#4a3a32" stroke-width="5" fill="none" opacity="0.55"/>')
    s += strands(r, [(-18, -112, -50, -150, -88, -90), (24, -112, 60, -156, 92, -86)], 10, "#3a2c26", (1.0, 2.2), (0.3, 0.75), 5)
    s += '<path d="M-20,-110 C-10,-140 -14,-160 -10,-170" stroke="#6a5a54" stroke-width="3" fill="none" opacity="0.5"/>'
    return s


def crown(ghost=False):
    """coronita de azahares across the top of the head"""
    s = ""; r = random.Random(9)
    for i in range(17):
        a = math.radians(200 + i * 8.6)
        x = math.cos(a) * 98; y = -78 + math.sin(a) * 100
        s += f'<circle cx="{x+r.uniform(-3,3):.1f}" cy="{y+r.uniform(-3,3):.1f}" r="{r.uniform(9,13):.1f}" fill="#f6f2e8"/>'
        for k in range(5):
            b = k * math.tau / 5 + r.uniform(0, 1)
            s += f'<ellipse cx="{x+math.cos(b)*7:.1f}" cy="{y+math.sin(b)*7:.1f}" rx="6" ry="3.5" fill="#ffffff" transform="rotate({math.degrees(b):.0f} {x+math.cos(b)*7:.1f} {y+math.sin(b)*7:.1f})"/>'
        s += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="#e8d27a"/>'
        if i % 3 == 0:
            s += f'<ellipse cx="{x*1.08:.1f}" cy="{y-8:.1f}" rx="10" ry="4" fill="#5a7a4a" transform="rotate({math.degrees(a)+90:.0f} {x*1.08:.1f} {y-8:.1f})"/>'
    return s


def veil_back(op=0.5, long=True):
    g = uid("vb")
    s = f'<defs>{grad_lin(g, [(0, "#ffffff", 0.0), (0.25, "#e8eef6", 1), (0.75, "#e8eef6", 1), (1, "#ffffff", 0.0)], -320, 0, 320, 0)}</defs>'
    bot = 640 if long else 300
    s += f'<path d="M-100,-150 C-160,-120 -200,60 -260,{bot} L260,{bot} C200,60 160,-120 100,-150 Z" fill="url(#{g})" opacity="{op}"/>'
    for i in range(9):
        x = -230 + i * 58
        s += f'<path d="M{x*0.35:.0f},-140 C{x*0.6:.0f},0 {x*0.9:.0f},200 {x:.0f},{bot}" stroke="#b8c4d4" stroke-width="4" fill="none" opacity="{op*0.5:.2f}"/>'
    return s


def veil_front(op=0.35):
    """sheer tulle falling over the sides of the face from the crown (face uncovered)"""
    g = uid("vf")
    s = f'<defs>{grad_lin(g, [(0, "#ffffff", 0.9), (0.5, "#dfe7f2", 0.2), (1, "#ffffff", 0.9)], -150, 0, 150, 0)}</defs>'
    s += (f'<path d="M-104,-120 C-140,-40 -150,100 -190,300 L-120,300 C-104,140 -96,20 -86,-80 Z M104,-120 C140,-40 150,100 190,300 L120,300 '
          f'C104,140 96,20 86,-80 Z" fill="url(#{g})" opacity="{op}"/>')
    s += f'<path d="M-104,-120 C-140,-40 -150,100 -190,300 M104,-120 C140,-40 150,100 190,300" stroke="#ffffff" stroke-width="3" fill="none" opacity="{op}"/>'
    return s


def gown_body(g, rim, ghost=False, colors=("#8c8a92", "#d6d2ca", "#f6f2ea")):
    """1930 bridal gown bust: satin bodice, lace yoke, high lace collar, long sleeves (body coords like bea_body)"""
    d0, d1, d2 = colors; sk = SK_PAS
    s = (f'<defs>{grad_lin(g+"d", [(0, d0, 1), (0.45, d1, 1), (0.8, d2, 1), (1, d1, 1)], -360, 0, 360, 0)}'
         f'{grad_lin(g+"s", [(0, sk["deep"], 1), (0.4, sk["shadow"], 1), (0.75, sk["base"], 1), (1, sk["shadow"], 1)], -60, 0, 60, 0)}</defs>')
    s += f'<path d="M-44,40 C-44,90 -48,120 -60,150 L60,150 C48,120 44,90 44,40 Z" fill="url(#{g}s)"/>'
    # high lace collar
    s += f'<path d="M-52,96 C-30,110 30,110 52,96 L58,150 C30,162 -30,162 -58,150 Z" fill="{d2}" opacity="0.95"/>'
    for i in range(12):
        x = -54 + i * 10
        s += f'<circle cx="{x}" cy="{104 + 0.6*abs(x)/5:.0f}" r="4" fill="none" stroke="#a8a4a0" stroke-width="2"/>'
    # shoulders / bodice
    s += f'<path d="M-250,226 C-170,200 -100,170 -58,150 L58,150 C100,170 170,200 250,226 C320,270 350,400 360,660 L-360,660 C-350,400 -320,270 -250,226 Z" fill="url(#{g}d)"/>'
    # lace yoke (semi-transparent with pattern)
    s += f'<path d="M-200,214 C-120,190 -70,160 -58,150 L58,150 C70,160 120,190 200,214 C140,300 60,330 0,336 C-60,330 -140,300 -200,214 Z" fill="#ffffff" opacity="0.35"/>'
    r = random.Random(3)
    for i in range(46):
        x = r.uniform(-170, 170); y = r.uniform(170, 320)
        if abs(x) > 200 - (y - 170) * 0.9: continue
        rr = r.uniform(6, 12)
        s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rr:.0f}" fill="none" stroke="#9a9aa4" stroke-width="2" opacity="0.6"/>'
        s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rr*0.35:.0f}" fill="#b8b8c0" opacity="0.5"/>'
    s += '<path d="M-200,214 C-140,300 -60,330 0,336 C60,330 140,300 200,214" stroke="#ffffff" stroke-width="5" stroke-dasharray="3 7" fill="none" opacity="0.9"/>'
    # pearl buttons
    for i in range(7):
        s += f'<circle cx="0" cy="{356+i*40}" r="7" fill="#fdfaf2"/><circle cx="-2" cy="{354+i*40}" r="2.5" fill="#fff"/>'
    # satin folds
    for dd in ["M-200,330 Q-215,480 -190,660", "M200,330 Q215,480 190,660", "M-90,340 Q-80,480 -100,660", "M90,340 Q80,480 100,660"]:
        s += f'<path d="{dd}" stroke="#6a6a74" stroke-width="12" fill="none" opacity="0.35" filter="url(#blur1)"/>'
    for dd in ["M-150,340 Q-150,480 -140,660", "M150,340 Q150,480 140,660"]:
        s += f'<path d="{dd}" stroke="#ffffff" stroke-width="8" fill="none" opacity="0.4" filter="url(#blur1)"/>'
    # sleeves (puffed at shoulder)
    for side in (-1, 1):
        s += (f'<path d="M{side*250},226 C{side*340},236 {side*380},330 {side*370},430 C{side*330},410 {side*290},392 {side*244},404 '
              f'C{side*256},340 {side*244},280 {side*250},226 Z" fill="{d2}" opacity="0.95"/>')
        for k in range(4):
            s += f'<path d="M{side*(264+k*24)},{238+k*6} C{side*(292+k*20)},300 {side*(292+k*16)},360 {side*(272+k*20)},404" stroke="#9a98a0" stroke-width="4" fill="none" opacity="0.6"/>'
    if rim:
        s += f'<path d="M-250,226 C-330,270 -370,420 -380,660" stroke="{rim}" stroke-width="6" fill="none" opacity="0.6" filter="url(#blur1)"/>'
        s += f'<path d="M250,226 C330,270 370,420 380,660" stroke="{rim}" stroke-width="4" fill="none" opacity="0.35" filter="url(#blur1)"/>'
    return s


def bride_head(look=0.0, turn=0.0, lids=0.2, smile=0.12, rim="#9fc2e8", sk=None, eyes_closed=False, glass=True, ghost=False, hollow=False):
    sk = sk or SK_PAS
    s = veil_back(0.55) + hair_back()
    s += head(look=look, smile=smile, lids=lids, rim=rim, turn=turn, eyes_closed=eyes_closed, sk=sk, headwrap=False,
              lips=("#9a4448", "#b8585a"), iris="#1e140e", earring=False, brow_w=0.75)
    if glass and not eyes_closed:   # glassy catchlights
        sh = turn * 20 + look * 6
        for ex in (-31, 31):
            s += f'<circle cx="{ex+sh+5:.1f}" cy="-24" r="4.5" fill="#ffffff" opacity="0.95"/><circle cx="{ex+sh-4:.1f}" cy="-14" r="2" fill="#ffffff" opacity="0.6"/>'
    if hollow:
        for ex in (-31, 31):
            s += f'<ellipse cx="{ex}" cy="-19" rx="22" ry="16" fill="#000" opacity="0.92"/><circle cx="{ex}" cy="-19" r="4" fill="#ffffff" opacity="0.9"/>'
    s += hair_front(ghost=ghost) + crown(ghost) + veil_front(0.32)
    return s


def bride_bust(x, y, k=1.0, rim="#9fc2e8", sk=None, bouquet=True, **hk):
    g = uid("pb")
    body = gown_body(g, rim)
    if bouquet:
        body += f'<g transform="translate(0,600) scale(1.25)">{roses(0, 0, 1.0, seed=7)}</g>'
    return bust_frame(body, bride_head(rim=rim, sk=sk, **hk), x, y, k)


def roses(x, y, k=1.0, seed=7, n=13, spider=False):
    """round bridal bouquet of white roses + azahar sprigs + ribbon"""
    r = random.Random(seed); s = f'<g transform="translate({x},{y}) scale({k})">'
    s += '<path d="M-40,60 C-60,180 -70,260 -90,330 M40,60 C60,180 70,260 90,330" stroke="#f2eee4" stroke-width="22" fill="none"/>'
    s += '<path d="M-40,60 C-60,180 -70,260 -90,330" stroke="#c8c2b4" stroke-width="5" fill="none"/>'
    for i in range(14):
        a = r.uniform(0, math.tau); d = r.uniform(110, 150)
        s += f'<ellipse cx="{math.cos(a)*d:.0f}" cy="{math.sin(a)*d*0.8:.0f}" rx="40" ry="14" fill="#3a5a34" transform="rotate({math.degrees(a):.0f} {math.cos(a)*d:.0f} {math.sin(a)*d*0.8:.0f})"/>'
    pts = [(0, 0)] + [(math.cos(i * math.tau / 6) * 70, math.sin(i * math.tau / 6) * 56) for i in range(6)] + \
          [(math.cos(i * math.tau / 10 + 0.3) * 125, math.sin(i * math.tau / 10 + 0.3) * 96) for i in range(10)]
    for (px, py) in pts[:n + 4]:
        rr = r.uniform(36, 46)
        s += f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{rr:.0f}" fill="#e8e2d6"/>'
        s += f'<circle cx="{px-6:.0f}" cy="{py-8:.0f}" r="{rr*0.8:.0f}" fill="#f8f4ec"/>'
        for j in range(4):
            q = rr * (0.75 - j * 0.17); a0 = r.uniform(0, 6)
            s += f'<path d="M{px+math.cos(a0)*q:.0f},{py+math.sin(a0)*q:.0f} A{q:.0f},{q:.0f} 0 1 1 {px+math.cos(a0+4.4)*q:.0f},{py+math.sin(a0+4.4)*q:.0f}" stroke="#c4bcae" stroke-width="3" fill="none"/>'
    s += '</g>'
    return s


def mannequin_full(k=1.0, look=0.0, turn=0.0, rim="#ffe0b0", ghost=False):
    """standing bride, feet at (0,0), ~1000 tall"""
    g = uid("mf")
    d0, d1, d2 = ("#9aa6b8", "#d8e2f0", "#ffffff") if ghost else ("#8a8680", "#d8d2c6", "#f8f4ec")
    s = (f'<defs>{grad_lin(g, [(0, d0, 1), (0.45, d1, 1), (0.8, d2, 1), (1, d1, 1)], -300, 0, 300, 0)}</defs>')
    s += veil_back(0.45).replace('-260,640', '-330,1000').replace('260,640', '330,1000') if False else ""
    # long veil behind, to the floor
    s += f'<path d="M-40,-900 C-160,-760 -260,-300 -330,0 L330,0 C260,-300 160,-760 40,-900 Z" fill="#eef2f8" opacity="0.28"/>'
    # skirt (bias-cut 1930, slim to the floor with a train)
    s += f'<path d="M-90,-520 C-120,-360 -170,-160 -230,0 L250,0 C190,-160 130,-360 100,-520 Z" fill="url(#{g})"/>'
    for i in range(7):
        x = -70 + i * 26
        s += f'<path d="M{x},-500 C{x*1.3:.0f},-300 {x*1.9:.0f},-120 {x*2.4:.0f},0" stroke="#8a8a94" stroke-width="4" fill="none" opacity="0.45"/>'
    # bodice
    s += f'<path d="M-70,-760 C-100,-700 -100,-600 -90,-520 L100,-520 C110,-600 110,-700 80,-760 C40,-790 -40,-790 -70,-760 Z" fill="url(#{g})"/>'
    s += '<path d="M-70,-760 C-30,-720 40,-720 80,-760" stroke="#ffffff" stroke-width="5" stroke-dasharray="3 6" fill="none"/>'
    # arms holding bouquet at waist
    s += f'<path d="M-80,-750 C-130,-700 -130,-600 -60,-560 L-30,-580 C-80,-620 -90,-680 -60,-720 Z" fill="{d2}"/>'
    s += f'<path d="M90,-750 C140,-700 140,-600 70,-560 L40,-580 C90,-620 100,-680 70,-720 Z" fill="{d2}"/>'
    s += roses(5, -560, 0.55, seed=3)
    # neck + head
    s += f'<g transform="translate(5,-880) scale(0.62)">{bride_head(look=look, turn=turn, rim=rim, lids=0.2, smile=0.1)}</g>'
    s += f'<path d="M-230,0 C-170,-160 -120,-360 -90,-520" stroke="{rim}" stroke-width="5" fill="none" opacity="0.5" filter="url(#blur1)"/>'
    return f'<g transform="scale({k})">{s}</g>'


# ===================================================================== the mother
def mother_head(look=0.0, lids=0.4, smile=-0.15, rim="#ffcf8a", sad=False, mantilla=False):
    s = ""
    if mantilla:
        s += '<path d="M-130,-120 C-150,-210 150,-210 130,-120 C160,0 200,160 260,320 L-260,320 C-200,160 -160,0 -130,-120 Z" fill="#0a0a0e" opacity="0.95"/>'
    s += '<path d="M-60,-150 C-40,-200 40,-200 60,-150 C70,-120 40,-110 0,-112 C-40,-110 -70,-120 -60,-150 Z" fill="#100a08"/>'  # bun
    s += head(look=look, smile=(-0.35 if sad else smile), lids=(0.55 if sad else lids), rim=rim, sk=SK_MOM, headwrap=False,
              lips=("#7a3a36", "#8a4a44"), iris="#1a100a", earring=True, brow_w=0.95)
    cap = ('M0,-118 C-40,-118 -70,-100 -80,-60 C-84,-30 -84,0 -80,20 C-94,0 -98,-60 -88,-96 C-74,-140 -36,-158 0,-158 '
           'C36,-158 74,-140 88,-96 C98,-60 94,0 80,20 C84,0 84,-30 80,-60 C70,-100 40,-118 0,-118 Z')
    s += f'<path d="{cap}" fill="#120c0a"/>'
    r = random.Random(11)
    s += strands(r, [(-4, -118, -50, -130, -84, -50), (4, -118, 50, -130, 84, -50)], 9, "#3a302c", (1.2, 2.2), (0.4, 0.8), 4)
    s += strands(r, [(-10, -150, -50, -140, -80, -90), (10, -150, 50, -140, 80, -90)], 6, "#9a9090", (1.2, 2.2), (0.4, 0.7), 4)  # grey
    s += '<path d="M-52,58 C-46,70 -40,78 -30,82 M52,58 C46,70 40,78 30,82 M-48,-50 C-36,-56 -24,-56 -14,-50 M48,-50 C36,-56 24,-56 14,-50" stroke="#6a4434" stroke-width="2.5" fill="none" opacity="0.6"/>'
    if mantilla:
        s += '<path d="M-130,-120 C-110,-190 110,-190 130,-120 C110,-170 -110,-170 -130,-120 Z" fill="#1a1a22"/>'
        for i in range(10):
            a = -120 + i * 27
            s += f'<path d="M{a*0.5:.0f},-170 C{a*0.9:.0f},-80 {a*1.4:.0f},100 {a*2:.0f},320" stroke="#2a2a36" stroke-width="3" fill="none" opacity="0.6"/>'
    if sad:
        s += '<path d="M-42,0 C-44,22 -42,42 -44,60" stroke="#cfe0ff" stroke-width="4" fill="none" opacity="0.55"/>'
    return s


def mother_bust(x, y, k=1.0, rim="#ffcf8a", **hk):
    g = uid("mb")
    body = QM.bea_body(g, rim, ("#060608", "#121218", "#24242e"))
    return bust_frame(body, mother_head(rim=rim, **hk), x, y, k)


# ===================================================================== props
def spider(x, y, k=1.0, rot=0, shine="#a8c8ff"):
    """black widow: glossy round abdomen with red hourglass, 8 jointed legs"""
    s = f'<g transform="translate({x},{y}) rotate({rot}) scale({k})">'
    legs = [(-1, 30, 1.0), (-1, 70, 1.15), (-1, 115, 0.95), (-1, 150, 1.1), (1, 30, 1.0), (1, 70, 1.15), (1, 115, 0.95), (1, 150, 1.1)]
    for side, ang, ln in legs:
        a = math.radians(ang - 90) if side > 0 else math.radians(270 - ang)
        a = math.radians(-ang) if side > 0 else math.radians(180 + ang)
        a = math.radians(ang - 100) * 1.0
        base = (side * 16, -10 + (ang - 90) * 0.12)
        kx = base[0] + side * 120 * ln; ky = base[1] - 70 * ln + (ang - 30) * 1.1
        ex = kx + side * 90 * ln; ey = ky + 110 * ln
        s += f'<path d="M{base[0]:.0f},{base[1]:.0f} Q{(base[0]+kx)/2:.0f},{ky-20:.0f} {kx:.0f},{ky:.0f} L{ex:.0f},{ey:.0f}" stroke="#050505" stroke-width="9" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
        s += f'<path d="M{(base[0]+kx)/2:.0f},{ky-14:.0f} L{kx:.0f},{ky-2:.0f}" stroke="{shine}" stroke-width="2" opacity="0.5"/>'
    s += '<ellipse cx="0" cy="-20" rx="30" ry="26" fill="#060606"/>'
    s += '<ellipse cx="0" cy="-60" rx="14" ry="10" fill="#060606"/>'
    s += '<ellipse cx="0" cy="70" rx="78" ry="92" fill="#030303"/>'
    s += f'<ellipse cx="-26" cy="34" rx="26" ry="34" fill="{shine}" opacity="0.28" filter="url(#blur1)"/><ellipse cx="-30" cy="26" rx="8" ry="12" fill="#ffffff" opacity="0.7"/>'
    s += '<path d="M-22,52 L22,52 L4,82 L22,112 L-22,112 L-4,82 Z" fill="#d0101a"/><path d="M-22,52 L22,52 L4,82 L22,112 L-22,112 L-4,82 Z" fill="#ff4040" opacity="0.4" filter="url(#blur1)"/>'
    return s + '</g>'


def hand_svg(red_dot=False, spider_on=False, warm=False):
    """big relaxed hand (back of hand, fingers to the right) resting on satin, with knuckle creases, veins, nails,
    fingertip cracks; sleeve cuff of lace on the left"""
    sk = SK_HIJA if warm else SK_PAS
    g = uid("hd")
    s = (f'<defs>{grad_lin(g, [(0, sk["shadow"], 1), (0.5, sk["base"], 1), (1, sk["light"], 1)], 0, 900, 0, 520)}'
         f'{grad_lin(g+"f", [(0, sk["shadow"], 1), (0.6, sk["base"], 1), (1, sk["light"], 1)], 0, 60, 0, -60)}</defs>')
    # satin backdrop
    bg = "#3a2c22" if warm else "#2a3240"
    s += f'<rect width="2400" height="1350" fill="{bg}"/>'
    for i in range(14):
        y = 80 + i * 100
        s += f'<path d="M0,{y} C600,{y-60} 1400,{y+80} 2400,{y-20}" stroke="{"#5a4434" if warm else "#4a5466"}" stroke-width="{40+i%3*20}" fill="none" opacity="0.35" filter="url(#blur3)"/>'
    s += glow(1500, 500, 900, "warm" if warm else "moon", 0.5)
    # hand body (palm-down)
    s += f'<path d="M420,620 C560,560 820,520 1040,540 C1160,550 1240,580 1300,620 L1330,900 C1220,960 1060,980 900,960 C720,940 560,920 420,900 Z" fill="url(#{g})"/>'
    fingers = [(1290, 600, 1980, 520, 64), (1310, 690, 2060, 690, 66), (1300, 790, 2000, 860, 62), (1270, 880, 1820, 1010, 54)]
    for (x0, y0, x1, y1, w) in fingers:
        ang = math.degrees(math.atan2(y1 - y0, x1 - x0)); L = math.hypot(x1 - x0, y1 - y0)
        tr = f'translate({x0},{y0}) rotate({ang:.1f})'
        s += f'<g transform="{tr}"><path d="M0,{-w} C{L*0.4:.0f},{-w} {L*0.7:.0f},{-w*0.86:.0f} {L-w*0.8:.0f},{-w*0.78:.0f} C{L+w*0.2:.0f},{-w*0.7:.0f} {L+w*0.2:.0f},{w*0.7:.0f} {L-w*0.8:.0f},{w*0.78:.0f} C{L*0.7:.0f},{w*0.86:.0f} {L*0.4:.0f},{w} 0,{w} Z" fill="url(#{g}f)"/>'
        # knuckle creases at two joints
        for jx in (L * 0.38, L * 0.7):
            for q in range(3):
                s += f'<path d="M{jx-14+q*10:.0f},{-w*0.6:.0f} Q{jx-8+q*10:.0f},0 {jx-14+q*10:.0f},{w*0.6:.0f}" stroke="{sk["shadow"]}" stroke-width="2.5" fill="none" opacity="0.7"/>'
        # nail
        s += f'<path d="M{L-w*1.6:.0f},{-w*0.5:.0f} C{L-w*0.4:.0f},{-w*0.62:.0f} {L-w*0.1:.0f},{-w*0.3:.0f} {L-w*0.05:.0f},0 C{L-w*0.1:.0f},{w*0.3:.0f} {L-w*0.4:.0f},{w*0.62:.0f} {L-w*1.6:.0f},{w*0.5:.0f} Z" fill="{sk["hi"]}" stroke="{sk["shadow"]}" stroke-width="2.5"/>'
        s += f'<path d="M{L-w*1.3:.0f},{-w*0.25:.0f} C{L-w*0.8:.0f},{-w*0.3:.0f} {L-w*0.5:.0f},{-w*0.15:.0f} {L-w*0.4:.0f},0" stroke="#ffffff" stroke-width="5" fill="none" opacity="0.6"/>'
        # fingertip cracks (look like fingerprints)
        for q in range(4):
            s += f'<path d="M{L-w*0.55+q*6:.0f},{w*0.55:.0f} q8,-10 4,-20" stroke="{sk["deep"]}" stroke-width="1.6" fill="none" opacity="0.55"/>'
        s += '</g>'
    # thumb from under
    s += f'<path d="M1100,940 C1240,980 1400,1040 1520,1110 C1560,1140 1530,1190 1480,1180 C1360,1150 1200,1080 1080,1020 Z" fill="{sk["shadow"]}"/>'
    # knuckle bumps + tendons
    for (x0, y0, x1, y1, w) in fingers:
        s += f'<ellipse cx="{x0-10}" cy="{y0}" rx="40" ry="30" fill="{sk["light"]}" opacity="0.6" filter="url(#blur1)"/>'
        s += f'<path d="M{x0-30},{y0} C{x0-200},{y0+10} {x0-420},{y0+40} {x0-640},{(y0+760)/2:.0f}" stroke="{sk["light"]}" stroke-width="10" fill="none" opacity="0.35" filter="url(#blur1)"/>'
    # blue veins
    for d in ["M480,700 C700,690 820,650 980,640 C1080,634 1160,640 1230,610",
              "M480,800 C680,780 820,760 960,740 C1060,726 1140,740 1260,700", "M820,760 C900,720 980,700 1040,660",
              "M600,850 C760,840 880,820 1000,800 C1100,790 1180,820 1250,800"]:
        s += f'<path d="{d}" stroke="#7a8ab8" stroke-width="7" fill="none" opacity="0.55" filter="url(#blur1)"/><path d="{d}" stroke="#9aa8d0" stroke-width="2" fill="none" opacity="0.5"/>'
    # lace cuff
    s += '<path d="M0,500 L470,560 C500,680 500,820 470,940 L0,1000 Z" fill="#f2eee6"/>'
    r = random.Random(5)
    for i in range(30):
        cy = 560 + i * 13; cx = 470 + 18 * math.sin(i)
        s += f'<circle cx="{cx:.0f}" cy="{cy}" r="14" fill="none" stroke="#a8a4a0" stroke-width="3"/>'
    for i in range(40):
        s += f'<circle cx="{r.uniform(40,440):.0f}" cy="{r.uniform(540,960):.0f}" r="{r.uniform(8,16):.0f}" fill="none" stroke="#c0bcb4" stroke-width="2.5"/>'
    s += '<path d="M470,560 C500,680 500,820 470,940" stroke="#ffffff" stroke-width="6" stroke-dasharray="4 8" fill="none"/>'
    if red_dot:
        s += '<circle cx="560" cy="760" r="14" fill="#c8141a"/><circle cx="560" cy="760" r="40" fill="#c8141a" opacity="0.35" filter="url(#blur2)"/>'
    if spider_on:
        s += spider(330, 380, 0.9, 30)
    # rim light on top edge
    s += f'<path d="M420,620 C560,560 820,520 1040,540 C1160,550 1240,580 1300,620" stroke="{"#ffd8a0" if warm else "#c8dcff"}" stroke-width="6" fill="none" opacity="0.7" filter="url(#blur1)"/>'
    return s


def lamp_hanging(x, y, on=True):
    s = f'<path d="M{x},0 L{x},{y-60}" stroke="#0a0806" stroke-width="5"/>'
    s += f'<path d="M{x-70},{y} L{x-40},{y-60} L{x+40},{y-60} L{x+70},{y} Z" fill="#2a1e10"/>'
    if on:
        s += glow(x, y + 30, 380, "warm", 0.9) + f'<ellipse cx="{x}" cy="{y+12}" rx="40" ry="18" fill="#fff0c0"/>'
    return s


def dress_form(x, y, k=1.0, white=True, rim=WARM, veil=False):
    c = ("#d8d2c6", "#f4efe6") if white else ("#4a3a30", "#6a5446")
    s = f'<g transform="translate({x},{y}) scale({k})">'
    s += '<path d="M-10,-860 L10,-860 L10,-40 L-10,-40 Z M-120,0 L120,0 L0,-50 Z" fill="#1a120c"/>'
    s += f'<path d="M-70,-860 C-110,-820 -110,-700 -80,-620 C-120,-420 -200,-160 -240,-60 L240,-60 C200,-160 120,-420 80,-620 C110,-700 110,-820 70,-860 C30,-890 -30,-890 -70,-860 Z" fill="{c[1]}"/>'
    for i in range(7):
        xx = -60 + i * 20
        s += f'<path d="M{xx},-620 C{xx*1.4:.0f},-400 {xx*2.4:.0f},-200 {xx*3:.0f},-60" stroke="#a8a49c" stroke-width="4" fill="none" opacity="0.5"/>'
    s += f'<path d="M-240,-60 C-200,-160 -120,-420 -80,-620" stroke="{rim}" stroke-width="5" fill="none" opacity="0.6" filter="url(#blur1)"/>'
    s += '<ellipse cx="0" cy="-900" rx="34" ry="40" fill="#2a1e14"/>'
    if veil:
        s += '<path d="M-30,-930 C-120,-800 -200,-400 -260,-60 L260,-60 C200,-400 120,-800 30,-930 Z" fill="#eef2f8" opacity="0.25"/>'
    return s + '</g>'


# ===================================================================== backgrounds
@art
def street_chih(): return S(QM.persp_street("night", seed=21), QM.fog_band(1180, 0.3, 22))
@art
def street_day(): return S(QM.persp_street("dusk", seed=23, lamp_on=False))
@art
def street_today(): return S(QM.persp_street("modern", seed=25, lamp_on=False, modern=True, plaque=("CALLE", "VICTORIA")))


def shopfront_svg(mood="night", lit=True, closed=False, mannequin_in=False):
    r = random.Random(4)
    if mood == "night":
        s = sky("#040912", "#16263a") + stars(90, 3, 300); wall = "#4a4038"; wall2 = "#2a241e"; ground = "#121418"; stone = "#5a5046"
    else:
        s = sky("#5a8ac8", "#e8d8b8"); wall = "#c8a47a"; wall2 = "#9a7a56"; ground = "#7a6a5a"; stone = "#e0c49a"
    s += f'<rect x="0" y="120" width="2400" height="1000" fill="{wall}"/>'
    s += f'<rect x="0" y="120" width="2400" height="1000" fill="#000" filter="url(#plaster)" opacity="{0.55 if mood=="night" else 0.25}"/>'
    # cornice + upper floor balconies
    s += f'<rect x="0" y="110" width="2400" height="40" fill="{stone}"/><rect x="0" y="280" width="2400" height="26" fill="{stone}"/>'
    for x in (300, 1300, 2000):
        lw = mood != "night" or x == 2000
        s += f'<rect x="{x-90}" y="140" width="180" height="130" fill="{"#ffc865" if (mood=="night" and x==2000) else "#1a1410"}"/>'
        s += f'<rect x="{x-110}" y="268" width="220" height="14" fill="#0a0806"/>' + "".join(f'<path d="M{x-100+i*20},268 L{x-100+i*20},230" stroke="#0a0806" stroke-width="4"/>' for i in range(11))
    # sign
    sc = "#1a120a" if mood == "night" else "#3a2410"
    s += f'<rect x="820" y="330" width="960" height="120" fill="{sc}" stroke="#c9a24a" stroke-width="6"/>'
    s += f'<text x="1300" y="420" font-family="Cinzel" font-weight="700" font-size="92" fill="{"#e8c870" if lit else "#7a6a4a"}" text-anchor="middle" letter-spacing="10">LA POPULAR</text>'
    # display window
    x0, y0, x1, y1 = 880, 480, 1720, 1060
    if closed:
        s += f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" fill="#2a1a16"/>'
        for i in range(20):
            s += f'<rect x="{x0+i*42}" y="{y0}" width="14" height="{y1-y0}" fill="#1a100c"/>'
        s += f'<rect x="{x0}" y="{y1-12}" width="{x1-x0}" height="10" fill="#ffc865" opacity="0.7"/>'
    else:
        inside = "#e8c48a" if lit else "#3a3028"
        s += f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" fill="#4a1a1c"/>'
        for i in range(14):
            s += f'<path d="M{x0+30+i*58},{y0} C{x0+20+i*58},{y0+200} {x0+40+i*58},{y0+400} {x0+30+i*58},{y1}" stroke="#2a0a0c" stroke-width="18" fill="none" opacity="0.7"/>'
        if lit:
            s += f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" fill="{inside}" opacity="0.35"/>' + glow(1300, 640, 520, "warm", 0.75)
        s += f'<rect x="{x0}" y="{y1-60}" width="{x1-x0}" height="60" fill="#2a1e14"/>'
        if mannequin_in:
            s += place(mannequin_full(rim="#fff0c0"), 1300, 1010, 0.56)
        for i in range(3):
            xx = x0 + 120 + i * 260
            s += f'<path d="M{xx},{y0} L{xx+220},{y0} L{xx-60},{y1} L{xx-280},{y1} Z" fill="#ffffff" opacity="0.06"/>'
    s += f'<rect x="{x0-30}" y="{y0-30}" width="{x1-x0+60}" height="30" fill="{stone}"/><rect x="{x0-30}" y="{y0-30}" width="30" height="{y1-y0+60}" fill="{stone}"/>'
    s += f'<rect x="{x1}" y="{y0-30}" width="30" height="{y1-y0+60}" fill="{stone}"/><rect x="{x0-50}" y="{y1}" width="{x1-x0+100}" height="40" fill="{stone}"/>'
    # door on the left (corner) + pilasters
    s += f'<rect x="420" y="520" width="300" height="580" fill="{"#1a1008" if mood=="night" else "#4a2a14"}"/><path d="M420,520 Q570,440 720,520" fill="{stone}"/>'
    s += f'<rect x="400" y="500" width="20" height="600" fill="{stone}"/><rect x="720" y="500" width="20" height="600" fill="{stone}"/>'
    if closed:
        s += '<rect x="470" y="700" width="200" height="70" fill="#d8ccb0"/><text x="570" y="750" font-family="Oswald" font-size="44" fill="#2a1a10" text-anchor="middle">CERRADO</text>'
    s += f'<rect x="1900" y="480" width="360" height="600" fill="{wall2}"/>'
    # sidewalk + street
    s += f'<rect x="0" y="1100" width="2400" height="250" fill="{ground}"/><rect x="0" y="1100" width="2400" height="22" fill="{stone}" opacity="0.7"/>'
    for i in range(24):
        s += f'<path d="M{i*110},1122 L{i*110-60},1350" stroke="#000" stroke-width="3" opacity="0.25"/>'
    # wall lantern at LAMP_XY on the left
    lx, ly = LAMP_XY
    if mood == "night":
        s += f'<path d="M{lx-40},{ly-80} L{lx},{ly-80} L{lx},{ly-40}" stroke="#0a0806" stroke-width="8" fill="none"/>'
        s += f'<path d="M{lx-36},{ly-40} L{lx+36},{ly-40} L{lx+24},{ly+50} L{lx-24},{ly+50} Z" fill="#ffd27a"/>' + glow(lx, ly, 260, "warm", 0.8)
    return s


@art
def shop_front(): return S(shopfront_svg("night"), QM.fog_band(1260, 0.3, 5))
@art
def shop_day(): return S(shopfront_svg("day"))
@art
def shop_closed(): return S(shopfront_svg("night", lit=False, closed=True), QM.fog_band(1260, 0.3, 6))
@art
def l_mannequin(): return S(place(mannequin_full(rim="#fff0c0"), 1300, 1010, 0.56))
@art
def l_window_glow(): return S(glow(1300, 700, 700, "warm", 0.45))
@art
def man_window():
    s = shopfront_svg("night", mannequin_in=True) + QM.fog_band(1260, 0.3, 7)
    s += place(man_full(hat=True, cape=False, rim="#ffd8a0", fill="#030304"), 1000, 1560, 1.0)
    return S(s)
@art
def crowd_window(): return S(shopfront_svg("day", mannequin_in=True))
@art
def l_crowd():
    s = ""
    for i, x in enumerate([200, 520, 860, 1500, 1820, 2150]):
        f = woman_full(rebozo_head=True, rim="#ffe8c0", fill="#14100c") if i % 2 == 0 else man_full(hat=True, cape=False, rim="#ffe8c0", fill="#14100c")
        s += place(f, x, 1450, 0.85 + (i % 3) * 0.05, flip=(i > 2))
    return S(s)


def window_close_svg(look=-0.9, turn=-0.55, glow_eyes=False, lids=0.22, closed=False, hollow=False, bgk="warm"):
    s = '<rect width="2400" height="1350" fill="#2a0c0e"/>'
    for i in range(30):
        s += f'<path d="M{i*84},0 C{i*84-20},400 {i*84+20},900 {i*84},1350" stroke="#140406" stroke-width="30" fill="none" opacity="0.7"/>'
        s += f'<path d="M{i*84+30},0 C{i*84+10},400 {i*84+50},900 {i*84+30},1350" stroke="#5a1e22" stroke-width="8" fill="none" opacity="0.5"/>'
    s += glow(1200, 420, 900, "warm" if bgk == "warm" else "moon", 0.65)
    s += bride_bust(1200, 560, 1.75, rim="#fff0d0", look=look, turn=turn, lids=lids, smile=0.1, eyes_closed=closed, hollow=hollow)
    if glow_eyes:
        s += ''.join(f'<circle cx="{1200+x_*1.75:.0f}" cy="{560-19*1.75:.0f}" r="70" fill="url(#whiteglow)" opacity="0.9"/><circle cx="{1200+x_*1.75:.0f}" cy="{560-19*1.75:.0f}" r="9" fill="#ffffff"/>' for x_ in (-31, 31))
    # glass: reflections + frame
    for x in (300, 700, 1800):
        s += f'<path d="M{x},0 L{x+160},0 L{x-240},1350 L{x-400},1350 Z" fill="#ffffff" opacity="0.07"/>'
    s += '<path d="M1900,0 L1940,0 L1540,1350 L1500,1350 Z" fill="#ffffff" opacity="0.12"/>'
    s += '<rect x="0" y="0" width="2400" height="40" fill="#5a5046"/><rect x="0" y="1300" width="2400" height="50" fill="#3a3028"/>'
    return s


@art
def window_close(): return S(window_close_svg())
@art
def window_turned():
    s = window_close_svg(look=0.0, turn=0.0, lids=0.0, glow_eyes=False, bgk="moon") + '<rect width="2400" height="1350" fill="#04081a" opacity="0.45"/>'
    s += ''.join(f'<circle cx="{1200+x_*1.75:.0f}" cy="{560-19*1.75:.0f}" r="70" fill="url(#whiteglow)" opacity="0.9"/><circle cx="{1200+x_*1.75:.0f}" cy="{560-19*1.75:.0f}" r="8" fill="#ffffff"/>' for x_ in (-31, 31))
    return S(s)
@art
def eyes_close(): return S(f'<rect width="2400" height="1350" fill="#1a0a0c"/>' + glow(1200, 500, 1200, "moon", 0.4) + bride_bust(1200, 720, 4.2, rim="#e8f0ff", look=0.0, lids=0.12, bouquet=False))
@art
def eyes_shut(): return S(f'<rect width="2400" height="1350" fill="#1a0a0c"/>' + glow(1200, 500, 1200, "moon", 0.4) + bride_bust(1200, 720, 4.2, rim="#e8f0ff", eyes_closed=True, bouquet=False))
@art
def face_flash():
    s = '<rect width="2400" height="1350" fill="#dfe6f0"/>' + glow(1200, 600, 1000, "white", 0.8)
    s += f'<g filter="url(#ghost)">{bride_bust(1200, 640, 2.6, rim="#ffffff", look=0.0, lids=0.0, hollow=True, bouquet=False)}</g>'
    s += '<rect width="2400" height="1350" fill="#c8d4e4" opacity="0.25"/>'
    return S(s)
@art
def title_bg():
    s = sky("#02050c", "#0c1626") + glow(1200, 520, 1100, "moon", 0.35)
    s += f'<g transform="translate(1200,1010) scale(0.4) translate(-1300,-700)">{shopfront_svg("night", mannequin_in=True)}</g>'
    s += '<rect width="2400" height="1350" fill="#02050c" opacity="0.55"/>' + QM.fog_band(1100, 0.4, 9) + QM.fog_band(1250, 0.45, 10)
    return S(s)
@art
def l_bride_ghost():
    return S(f'<g filter="url(#ghost)" opacity="0.85">{place(mannequin_full(rim="#ffffff", ghost=True), 1200, 1200, 0.62)}</g>')
@art
def l_veil_wind():
    s = '<path d="M1100,300 C1300,260 1500,380 1600,560 C1700,760 1640,980 1760,1150 C1500,1100 1300,1000 1200,820 C1100,640 1180,460 1100,300 Z" fill="#eef4ff" opacity="0.4" filter="url(#blur2)"/>'
    for i in range(6):
        s += f'<path d="M{1120+i*20},{320+i*10} C{1300+i*30},{400+i*40} {1400+i*30},{700+i*30} {1500+i*40},{1100}" stroke="#ffffff" stroke-width="4" fill="none" opacity="0.3"/>'
    return S(s)
@art
def l_walker(): return S(place(man_full(hat=False, cape=False, walk=0.3, rim=MOONRIM, fill="#020305"), 1160, 1420, 1.0))
@art
def l_lamp_glow(): return S(glow(LAMP_XY[0], LAMP_XY[1] + 20, 560, "warm", 0.5))
@art
def l_candle_glow(): return S(glow(CANDLE_XY[0], CANDLE_XY[1] - 200, 900, "warm", 0.4))
@art
def l_fog(): return S(clouds(18, 900, 1400, 31, "#b0c4d8", (0.08, 0.2), (300, 700), (60, 140)))


# ----------------------------------------------------- Chihuahua
@art
def desert():
    s = sky("#2a3a6a", "#f0a060", "#a06a6a")
    s += ridge(620, 90, "#5a3a4a", 3) + ridge(720, 70, "#3a2a34", 5) + ridge(860, 40, "#2a1e1a", 7)
    s += '<rect x="0" y="900" width="2400" height="450" fill="#3a2a1e"/>'
    r = random.Random(8)
    for i in range(30):  # creosote bushes
        x = r.uniform(0, 2400); y = r.uniform(920, 1340); k = 0.4 + (y - 900) / 450
        s += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{40*k:.0f}" ry="{18*k:.0f}" fill="#1a140c"/>'
    for x, y, k in [(300, 1250, 1.4), (1950, 1200, 1.1), (1500, 1000, 0.6)]:  # yuccas
        s += f'<path d="M{x},{y} L{x-10*k},{y-260*k} L{x+10*k},{y-260*k} Z" fill="#120c08"/>'
        for j in range(16):
            a = math.radians(-160 + j * 9)
            s += f'<path d="M{x},{y-260*k} L{x+math.cos(a)*120*k:.0f},{y-260*k+math.sin(a)*120*k:.0f}" stroke="#120c08" stroke-width="{7*k:.0f}"/>'
    # far town with two towers
    s += '<rect x="1000" y="840" width="420" height="40" fill="#2a1e1a"/><rect x="1150" y="770" width="30" height="80" fill="#2a1e1a"/><rect x="1240" y="770" width="30" height="80" fill="#2a1e1a"/>'
    s += '<circle cx="1700" cy="420" r="70" fill="#ffe0a0" opacity="0.9"/>' + glow(1700, 420, 400, "warm", 0.6)
    return S(s)
@art
def mine(): return BA.mine()


def cathedral_svg(mood="day"):
    if mood == "day":
        s = sky("#3a6ab0", "#f0d0a0"); st = "#c8a072"; dk = "#8a6440"; hi = "#f0d0a0"
    else:
        s = sky("#040912", "#1a2a44") + stars(100, 4, 400); st = "#5a4a3e"; dk = "#2a2018"; hi = "#a8c8ff"
    cx = 1200
    s += f'<rect x="{cx-420}" y="480" width="840" height="720" fill="{st}"/>'
    s += f'<rect x="{cx-420}" y="480" width="840" height="720" fill="#000" filter="url(#plaster)" opacity="0.25"/>'
    for side in (-1, 1):  # towers
        tx = cx + side * 520
        s += f'<rect x="{tx-130}" y="300" width="260" height="900" fill="{st}"/>'
        for lv, (yy, w) in enumerate([(300, 260), (130, 210), (-20, 160)]):
            s += f'<rect x="{tx-w/2:.0f}" y="{yy-150 if lv else yy-150}" width="{w}" height="150" fill="{st}"/>' if lv else ""
            s += f'<rect x="{tx-w/2-12:.0f}" y="{yy-12}" width="{w+24}" height="22" fill="{hi}" opacity="0.6"/>'
        s += f'<rect x="{tx-105}" y="150" width="210" height="160" fill="{st}"/><rect x="{tx-80}" y="20" width="160" height="140" fill="{st}"/>'
        s += f'<path d="M{tx-50},210 L{tx-50},150 Q{tx},110 {tx+50},150 L{tx+50},210 Z" fill="{dk}"/><path d="M{tx-35},90 Q{tx},60 {tx+35},90 L{tx+35},140 L{tx-35},140 Z" fill="{dk}"/>'
        s += f'<path d="M{tx-80},20 Q{tx},-60 {tx+80},20 Z" fill="{st}"/><path d="M{tx},-60 L{tx},-110 M{tx-16},-90 L{tx+16},-90" stroke="{dk}" stroke-width="8"/>'
        for j in range(3):
            s += f'<rect x="{tx-90+j*70}" y="{420}" width="30" height="{700}" fill="{dk}" opacity="0.25"/>'
    # baroque central body: three tiers of columns + niches
    for tier, (y, h) in enumerate([(700, 500), (520, 180), (380, 140)]):
        w = 700 - tier * 180
        s += f'<rect x="{cx-w/2}" y="{y}" width="{w}" height="{h}" fill="{st}"/>'
        for j in range(5 - tier):
            xx = cx - w / 2 + 40 + j * (w - 80) / max(1, 4 - tier)
            s += f'<rect x="{xx-14:.0f}" y="{y+10}" width="28" height="{h-20}" fill="{hi}" opacity="0.45"/>'
        s += f'<rect x="{cx-w/2-10}" y="{y-14}" width="{w+20}" height="18" fill="{hi}" opacity="0.6"/>'
        for j in range(2 - (tier == 2)):
            nx = cx - w / 4 + j * w / 2 if tier < 2 else cx
            s += f'<path d="M{nx-36:.0f},{y+h-30} L{nx-36:.0f},{y+60} Q{nx:.0f},{y+20} {nx+36:.0f},{y+60} L{nx+36:.0f},{y+h-30} Z" fill="{dk}"/>'
            s += f'<path d="M{nx:.0f},{y+70} C{nx-14:.0f},{y+80} {nx-18:.0f},{y+h-40} {nx:.0f},{y+h-40} C{nx+18:.0f},{y+h-40} {nx+14:.0f},{y+80} {nx:.0f},{y+70} Z" fill="{st}" opacity="0.8"/>'
    s += f'<path d="M{cx-130},1200 L{cx-130},940 Q{cx},820 {cx+130},940 L{cx+130},1200 Z" fill="{dk}"/>'
    s += f'<path d="M{cx-130},1200 L{cx-130},940 Q{cx},820 {cx+130},940 L{cx+130},1200" stroke="{hi}" stroke-width="10" fill="none" opacity="0.6"/>'
    s += f'<circle cx="{cx}" cy="600" r="46" fill="{dk}"/><path d="M{cx-120},380 Q{cx},250 {cx+120},380 Z" fill="{st}"/>'
    s += '<rect x="0" y="1200" width="2400" height="150" fill="#3a2e24"/>' if mood == "day" else '<rect x="0" y="1200" width="2400" height="150" fill="#0c0e12"/>'
    return s


@art
def cathedral(): return S(cathedral_svg("day"))
@art
def cathedral_bells():
    s = crop(S(cathedral_svg("day")), 2.0, 1200, 250)
    return s
@art
def plaza_couple():
    s = cathedral_svg("day") + '<rect width="2400" height="1350" fill="#e8a060" opacity="0.15"/>'
    s += place(woman_full(rim="#ffe0b0", fill="#1a0c10"), 1000, 1340, 0.95) + place(man_full(hat=True, cape=False, rim="#ffe0b0", fill="#0a0808"), 1300, 1340, 1.0, flip=True)
    s += f'<g transform="translate(1140,640) scale(0.4)">{roses(0, 0, 1.0, seed=2)}</g>'
    return S(s)


# ----------------------------------------------------- interiors
def shop_room(dark=False):
    s = room_walls("#4a3428" if not dark else "#1a1418", "#1a0e08" if not dark else "#06040a", "#2a1a10")
    # shelves with boxes on the right
    s += '<rect x="1650" y="250" width="700" height="800" fill="#2a1a10"/>'
    for j in range(5):
        y = 290 + j * 150
        s += f'<rect x="1650" y="{y+110}" width="700" height="16" fill="#4a3020"/>'
        for i in range(5):
            s += f'<rect x="{1680+i*130}" y="{y+40}" width="110" height="70" fill="{["#e8dcc0","#d8c8a8","#f0e8d8"][(i+j)%3]}"/><rect x="{1680+i*130}" y="{y+68}" width="110" height="10" fill="#a8946a"/>'
    # counter
    s += '<rect x="300" y="860" width="1100" height="220" fill="#3a2416"/><rect x="280" y="840" width="1140" height="30" fill="#6a4a2a"/>'
    s += '<rect x="320" y="880" width="1060" height="180" fill="#5a4030" opacity="0.4"/>'
    for i in range(3):
        s += f'<path d="M{400+i*340},880 L{600+i*340},880 L{500+i*340},1060 L{300+i*340},1060 Z" fill="#ffffff" opacity="0.06"/>'
    # bolts of fabric on counter
    for i, c in enumerate(["#f4efe6", "#e8e0d0", "#d8ccb8", "#fffaf0"]):
        s += f'<rect x="{420+i*200}" y="780" width="170" height="60" rx="30" fill="{c}"/>'
    # dress forms
    s += dress_form(1000, 1080, 0.82, veil=True) + dress_form(1420, 1080, 0.7)
    s += lamp_hanging(LAMP_XY[0], LAMP_XY[1], on=not dark)
    return s


@art
def shop_interior(): return S(shop_room())
@art
def crate():
    s = shop_room()
    s += '<path d="M1500,1260 L2200,1260 L2200,760 L1500,760 Z" fill="#8a6a40"/><path d="M1500,760 L1620,680 L2300,680 L2200,760 Z" fill="#a8884e"/><path d="M2200,760 L2300,680 L2300,1180 L2200,1260 Z" fill="#6a4e2e"/>'
    for y in (820, 960, 1100, 1220):
        s += f'<rect x="1500" y="{y}" width="700" height="12" fill="#5a4024"/>'
    s += '<text x="1850" y="940" font-family="Oswald" font-size="76" fill="#1a1008" text-anchor="middle" opacity="0.85">FRÁGIL</text>'
    s += '<text x="1850" y="1060" font-family="IM FELL English" font-size="64" fill="#1a1008" text-anchor="middle" opacity="0.8">Paris — Chihuahua</text>'
    s += '<path d="M1560,1250 C1580,1240 1600,1230 1640,1262 M1700,700 C1720,690 1760,720 1780,700" stroke="#d8ccb0" stroke-width="6" fill="none" opacity="0.6"/>'
    return S(s)
@art
def curtain():
    s = room_walls("#3a2420", "#0c0806", "#2a1a10") + lamp_hanging(LAMP_XY[0], LAMP_XY[1])
    s += '<rect x="700" y="160" width="1300" height="20" fill="#c9a24a"/>'
    for i in range(22):
        x = 720 + i * 58
        s += f'<path d="M{x},180 C{x-20},500 {x+20},800 {x},1100" stroke="#7a1a1e" stroke-width="64" fill="none"/>'
        s += f'<path d="M{x+18},180 C{x-2},500 {x+38},800 {x+18},1100" stroke="#b03036" stroke-width="12" fill="none" opacity="0.6"/>'
    s += glow(1350, 600, 700, "warm", 0.5)
    # shadow of the mannequin and of a woman reaching
    s += f'<g opacity="0.55" filter="url(#blur2)">{place(mannequin_full(rim="#000"), 1420, 1080, 0.78)}</g>'
    s += '<rect x="700" y="180" width="1300" height="920" fill="#5a0c10" opacity="0.35"/>'
    s += place(woman_full(rim="#ffd8a0", fill="#0c0606"), 500, 1250, 0.95)
    return S(s)
@art
def mirror_shop():
    s = room_walls("#3a2a22", "#0c0806") + lamp_hanging(LAMP_XY[0], LAMP_XY[1])
    s += '<ellipse cx="1300" cy="640" rx="470" ry="560" fill="#c9a24a"/><ellipse cx="1300" cy="640" rx="430" ry="520" fill="#141820"/>'
    s += glow(1300, 500, 600, "warm", 0.4)
    s += f'<g opacity="0.92">{bride_bust(1300, 540, 1.15, rim=WARM, sk=SK_HIJA, look=-0.1, lids=0.25, smile=0.45, bouquet=False)}</g>'
    s += '<path d="M1000,300 L1100,280 L900,1000 L800,1020 Z" fill="#ffffff" opacity="0.08"/>'
    return S(s)
@art
def sewing():
    s = room_walls("#2a1e18", "#0a0604") + table_wood(980) + candle_at(CANDLE_XY[0], CANDLE_XY[1] + 340, 160)
    s += dress_form(1400, 1100, 0.95, rim=WARM)
    s += place(woman_full(rim="#ffd8a0", fill="#0c0806", old=True), 950, 1300, 1.0)
    s += '<path d="M1080,760 C1150,740 1200,760 1250,720" stroke="#e8dcc0" stroke-width="3" fill="none"/>'
    for i in range(5):
        s += f'<circle cx="{600+i*40}" cy="{1000}" r="12" fill="{["#e8dcc0","#c8141a","#2a4a8a","#e8c870","#fff"][i]}"/>'
    return S(s)
@art
def back_room():
    s = room_walls("#2a1c18", "#06040a", "#140c08")
    s += '<path d="M900,1080 L900,300 Q1200,200 1500,300 L1500,1080 Z" fill="#ffc865" opacity="0.85"/>' + glow(1200, 700, 700, "warm", 0.7)
    s += '<path d="M940,1080 L940,320 Q1060,280 1120,290 L1120,1080 Z" fill="#7a1a1e" opacity="0.9"/>'
    s += '<rect x="1150" y="860" width="320" height="220" fill="#2a1a10"/><path d="M1160,860 C1200,800 1420,800 1460,860 Z" fill="#e8e0d0"/>'
    s += place(woman_full(rim="#ffd8a0", fill="#0a0604"), 1300, 1080, 0.62)
    s += '<path d="M1500,1080 L2400,1350 L2400,1080 Z" fill="#000" opacity="0.4"/>'
    s += '<path d="M1640,260 C1700,300 1780,640 1820,1080 L2200,1080 C2100,700 1900,360 1640,260 Z" fill="#000" opacity="0.55" filter="url(#blur2)"/>'
    s += candle_at(CANDLE_XY[0], CANDLE_XY[1] + 400, 140)
    return S(s)
@art
def back_door():
    s = sky("#040912", "#16263a") + stars(80, 9, 300)
    s += '<rect x="0" y="200" width="2400" height="900" fill="#3a3430"/><rect x="0" y="200" width="2400" height="900" fill="#000" filter="url(#plaster)" opacity="0.5"/>'
    s += '<rect x="1000" y="500" width="320" height="600" fill="#ffc865"/>' + glow(1160, 800, 500, "warm", 0.8)
    s += '<path d="M1000,500 L1100,540 L1100,1100 L1000,1100 Z" fill="#2a1a10"/>'
    s += '<rect x="0" y="1100" width="2400" height="250" fill="#121418"/>'
    m = man_full(hat=True, cape=True, walk=0.4, rim="#ffd8a0", fill="#030304")
    s += place(m, 1500, 1300, 0.8) + '<rect x="1580" y="980" width="110" height="80" rx="10" fill="#050505"/><path d="M1600,980 Q1635,950 1670,980" stroke="#050505" stroke-width="8" fill="none"/>'
    lx, ly = LAMP_XY
    s += f'<path d="M{lx-36},{ly-40} L{lx+36},{ly-40} L{lx+24},{ly+50} L{lx-24},{ly+50} Z" fill="#ffd27a"/>'
    return S(s, QM.fog_band(1250, 0.3, 12))
@art
def gossip():
    s = QM.persp_street("dusk", seed=27, lamp_on=False) + '<rect width="2400" height="1350" fill="#2a1a10" opacity="0.25"/>'
    s += place(woman_full(rebozo_head=True, rim="#ffd8a0", fill="#120a08", old=True), 900, 1550, 1.4)
    s += place(woman_full(rebozo_head=True, rim="#ffd8a0", fill="#0c0606"), 1420, 1550, 1.35, flip=True)
    return S(s)
@art
def photographer():
    s = shopfront_svg("day", mannequin_in=True) + '<rect width="2400" height="1350" fill="#3a2a1a" opacity="0.2"/>'
    s += '<path d="M600,1340 L760,880 L920,1340 M760,880 L760,1340" stroke="#0c0806" stroke-width="16" fill="none"/>'
    s += '<rect x="640" y="760" width="250" height="160" fill="#1a120c"/><circle cx="900" cy="840" r="50" fill="#0a0806" stroke="#8a7a5a" stroke-width="8"/>'
    s += '<path d="M640,760 C560,740 480,820 460,1000 L640,960 Z" fill="#050404"/>'
    s += place(man_full(hat=False, cape=False, rim="#ffe0b0", fill="#050404"), 520, 1400, 0.9)
    s += glow(980, 820, 200, "white", 0.8)
    return S(s)


# ----------------------------------------------------- wedding
@art
def daughter_portrait(): return S(portrait_bg("candle"), daughter_plain(1200, 560, 1.75))


def daughter_plain(x, y, k):
    """the daughter alive, everyday blouse, no veil"""
    g = uid("dp")
    body = QM.bea_body(g, WARM, ("#2a2a4a", "#4a5a8a", "#6a7aa8"))
    hd = hair_back() + head(look=0.2, smile=0.55, lids=0.22, rim=WARM, sk=SK_HIJA, headwrap=False, lips=("#9a4448", "#b8585a"),
                            iris="#1e140e", earring=True, brow_w=0.75) + hair_front()
    return bust_frame(body, hd, x, y, k)
@art
def daughter_bride(): return S(portrait_bg("candle"), bride_bust(1200, 560, 1.75, rim=WARM, sk=SK_HIJA, look=-0.15, lids=0.3, smile=0.4))
@art
def mother_portrait(): return S(portrait_bg("candle"), mother_bust(1200, 560, 1.75, rim="#ffb860", look=0.1))
@art
def mother_grief(): return S(portrait_bg("moon"), mother_bust(1200, 560, 1.75, rim=MOONRIM, look=0.35, sad=True, mantilla=True), '<rect width="2400" height="1350" fill="#04081a" opacity="0.2"/>')
@art
def bouquet():
    s = '<rect width="2400" height="1350" fill="#1a1210"/>' + glow(1200, 600, 900, "warm", 0.6)
    s += '<path d="M0,1350 C400,1000 900,1000 1200,1100 C1500,1000 2000,1000 2400,1350 Z" fill="#f2eee6" opacity="0.85"/>'
    s += roses(1200, 600, 2.4, seed=5)
    return S(s)
@art
def l_spider(): return S(spider(1500, 700, 0.45, 20))
@art
def spider_close():
    s = '<rect width="2400" height="1350" fill="#0c0a10"/>' + glow(1200, 600, 900, "moon", 0.45)
    s += roses(700, 900, 2.6, seed=8) + roses(1900, 400, 1.6, seed=9)
    s += '<rect width="2400" height="1350" fill="#0a0c18" opacity="0.35"/>'
    s += spider(1300, 620, 2.2, 15)
    return S(s)
@art
def hand_close(): return S(hand_svg())
@art
def wrist_close(): return S(hand_svg(red_dot=True, spider_on=True, warm=True))
@art
def wedding(): return QM.ART["wedding"]()
@art
def altar_blur(): return S(f'<g filter="url(#blur3)">{inner(QM.ART["wedding"]())}</g>', '<rect width="2400" height="1350" fill="#fff0d0" opacity="0.12"/>')
@art
def veil_floor():
    s = '<rect width="2400" height="1350" fill="#120c0a"/>'
    for i in range(12):  # floor tiles in perspective
        s += f'<path d="M{i*240-400},1350 L{1200+(i*240-1600)*0.3:.0f},300" stroke="#2a1e18" stroke-width="5"/>'
    for j in range(8):
        y = 300 + j * j * 18
        s += f'<path d="M0,{y} L2400,{y}" stroke="#2a1e18" stroke-width="4"/>'
    s += glow(1500, 300, 900, "warm", 0.4)
    s += '<path d="M500,1000 C700,820 1000,760 1300,800 C1600,840 1900,960 2100,1200 C1700,1260 1200,1300 800,1250 C600,1220 480,1120 500,1000 Z" fill="#eef2f8" opacity="0.75"/>'
    for i in range(10):
        s += f'<path d="M{600+i*140},{1000-i*10} C{700+i*140},{1050} {650+i*150},{1150} {700+i*150},{1260}" stroke="#9aa6b8" stroke-width="5" fill="none" opacity="0.4"/>'
    s += roses(1800, 1150, 0.9, seed=4)
    r = random.Random(3)
    for i in range(26):
        x, y = r.uniform(1300, 2300), r.uniform(950, 1340)
        s += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="16" ry="9" fill="#f4f0e6" transform="rotate({r.uniform(0,180):.0f} {x:.0f} {y:.0f})"/>'
    return S(s)
@art
def sickbed(): return QM.ART["sickbed"]()
@art
def candle_out():
    s = '<rect width="2400" height="1350" fill="#06070a"/>' + glow(1200, 700, 500, "moon", 0.25)
    s += '<rect x="1160" y="700" width="80" height="400" rx="10" fill="#d8ccb0"/><ellipse cx="1200" cy="1100" rx="140" ry="30" fill="#4a3a24"/>'
    s += '<path d="M1200,700 L1200,660" stroke="#1a1a1a" stroke-width="6"/>'
    s += '<path d="M1200,660 C1170,580 1240,520 1200,440 C1160,360 1240,300 1210,200" stroke="#9aa4b4" stroke-width="12" fill="none" opacity="0.4" filter="url(#blur2)"/>'
    return S(s)
@art
def red_flash(): return S('<rect width="2400" height="1350" fill="#5a0004"/>' + glow(1200, 675, 1100, "red", 0.9))
@art
def white_flash(): return S('<rect width="2400" height="1350" fill="#f4f0ea"/>')


# ----------------------------------------------------- legend / history / end
@art
def magician():
    s = sky("#030612", "#142238") + stars(140, 5, 700) + moon(1650, 300, 130) + glow(1650, 300, 600, "moon", 0.6)
    s += '<rect x="0" y="1150" width="2400" height="200" fill="#0a0c10"/>'
    m = ('<path d="M-180,0 C-170,-300 -150,-600 -90,-760 L90,-760 C150,-600 170,-300 180,0 Z" fill="#030304"/>'  # cape
         '<path d="M-60,-760 C-60,-820 -50,-860 0,-866 C50,-860 60,-820 60,-760 Z" fill="#030304"/>'
         '<rect x="-70" y="-1050" width="140" height="190" fill="#030304"/><rect x="-110" y="-872" width="220" height="22" rx="8" fill="#030304"/>'
         '<rect x="-70" y="-900" width="140" height="26" fill="#3a0a10"/>'
         '<path d="M150,-500 L240,0" stroke="#030304" stroke-width="14"/><circle cx="150" cy="-500" r="16" fill="#c9a24a"/>')
    m += f'<path d="M-90,-760 C-150,-600 -170,-300 -180,0 M-70,-1050 L-70,-872" stroke="{MOONRIM}" stroke-width="7" fill="none" opacity="0.8"/>'
    m += '<circle cx="-22" cy="-800" r="6" fill="#ffffff"/><circle cx="22" cy="-800" r="6" fill="#ffffff"/>'
    s += place(m, 1200, 1200, 1.0) + QM.fog_band(1180, 0.4, 3)
    return S(s)
@art
def ballroom(): return QM.ART["ballroom"]()
@art
def l_dance():
    s = place(mannequin_full(rim="#ffffff", ghost=True), 1150, 1180, 0.5) + place(man_full(hat=False, cape=True, rim="#ffffff", fill="#c8d4e8"), 1300, 1180, 0.52, flip=True)
    return S(f'<g filter="url(#ghost)" opacity="0.75">{s}</g>')
@art
def archive():
    s = AG.ART["chronicle"]()
    return s.replace("Leyendas de</text>", "Crónicas de</text>").replace("Coyoacán</text>", "Chihuahua</text>").replace("El Callejón del Aguacate", "La Pascualita, 1930")
@art
def shoes():
    s = '<rect width="2400" height="1350" fill="#0c0a0c"/>' + table_wood(800).replace("#3a2414", "#2a2018") + glow(1200, 400, 900, "moon", 0.45)
    for x, rot in [(950, -8), (1450, 6)]:
        s += f'<g transform="translate({x},900) rotate({rot})">'
        s += '<path d="M-250,60 C-240,-40 -120,-80 0,-70 C120,-60 220,-30 250,30 L230,90 C100,120 -100,120 -250,60 Z" fill="#f2eee6"/>'
        s += '<path d="M-40,-60 C-10,-110 60,-110 90,-60" stroke="#f2eee6" stroke-width="16" fill="none"/>'
        s += '<path d="M180,40 L200,180 L240,180 L240,40 Z" fill="#e0dace"/>'
        s += '<path d="M-250,60 C-100,120 100,120 230,90 L232,110 C100,140 -100,140 -250,80 Z" fill="#7a5a3a"/>'
        r = random.Random(x)
        for i in range(40):
            s += f'<circle cx="{r.uniform(-240,230):.0f}" cy="{r.uniform(80,130):.0f}" r="{r.uniform(2,6):.1f}" fill="#a07a4a"/>'
        s += '<path d="M-200,0 C-100,-50 50,-50 200,0" stroke="#ffffff" stroke-width="6" fill="none" opacity="0.5"/></g>'
    r = random.Random(1)
    for i in range(80):
        s += f'<circle cx="{r.uniform(700,1700):.0f}" cy="{r.uniform(1000,1100):.0f}" r="{r.uniform(2,5):.1f}" fill="#8a6a40" opacity="0.8"/>'
    return S(s)
@art
def sombreron():
    s = sky("#030612", "#16243a") + stars(120, 6, 600) + moon(600, 260, 90) + ridge(900, 60, "#0a1018", 4)
    s += '<rect x="0" y="1050" width="2400" height="300" fill="#0a0c10"/>'
    for x in (300, 1900, 2150):
        s += f'<rect x="{x-120}" y="820" width="240" height="230" fill="#141418"/><path d="M{x-150},830 L{x},740 L{x+150},830 Z" fill="#0c0c10"/><rect x="{x-30}" y="900" width="60" height="70" fill="#ffc865"/>'
    m = man_full(hat=False, cape=True, rim=MOONRIM, fill="#030304")
    s += place(m, 1200, 1150, 0.55)
    s += '<ellipse cx="1200" cy="625" rx="230" ry="46" fill="#030304"/><path d="M1130,620 C1140,540 1260,540 1270,620 Z" fill="#030304"/>'
    s += f'<path d="M970,625 C1050,600 1350,600 1430,625" stroke="{MOONRIM}" stroke-width="5" fill="none" opacity="0.8"/>'
    s += '<path d="M1290,850 L1420,760 L1440,780 L1310,880 Z" fill="#2a1a10"/><ellipse cx="1300" cy="880" rx="50" ry="40" fill="#2a1a10"/>'
    return S(s, QM.fog_band(1150, 0.35, 4))


# ----------------------------------------------------- variants (so no picture is reused more than ~3 times)
@art
def window_reflect():
    s = window_close_svg(look=-0.6, turn=-0.35)
    s += f'<g opacity="0.22">{place(man_full(hat=False, cape=False, rim="#ffffff", fill="#c8d4e8"), 1850, 1500, 1.25)}</g>'
    s += '<rect width="2400" height="1350" fill="#0a1830" opacity="0.25"/>'
    return S(s)
@art
def window_waist():
    s = '<rect width="2400" height="1350" fill="#2a0c0e"/>'
    for i in range(30):
        s += f'<path d="M{i*84},0 C{i*84-20},400 {i*84+20},900 {i*84},1350" stroke="#140406" stroke-width="30" fill="none" opacity="0.7"/>'
    s += glow(1200, 400, 900, "warm", 0.6)
    s += bride_bust(1200, 330, 0.95, rim="#fff0d0", look=0.5, turn=0.3, lids=0.3)
    s += f'<g transform="translate(1200,1000) scale(0.9)">{roses(0, 0, 1.0, seed=12)}</g>'
    for x in (500, 1700):
        s += f'<path d="M{x},0 L{x+160},0 L{x-240},1350 L{x-400},1350 Z" fill="#ffffff" opacity="0.07"/>'
    s += '<rect x="0" y="1300" width="2400" height="50" fill="#3a3028"/>'
    return S(s)
@art
def window_dress2():
    s = '<rect width="2400" height="1350" fill="#0c1424"/>'
    for i in range(30):
        s += f'<path d="M{i*84},0 C{i*84-20},400 {i*84+20},900 {i*84},1350" stroke="#060a14" stroke-width="30" fill="none" opacity="0.7"/>'
        s += f'<path d="M{i*84+30},0 C{i*84+10},400 {i*84+50},900 {i*84+30},1350" stroke="#1e2e4a" stroke-width="8" fill="none" opacity="0.5"/>'
    s += glow(1200, 420, 900, "moon", 0.6)
    g = uid("d2")
    body = gown_body(g, "#cfe0ff", colors=("#8a7a66", "#d8c8aa", "#f2e6cc"))
    hd = bride_head(rim="#cfe0ff", look=0.3, turn=0.15, lids=0.25, smile=0.05)
    s += bust_frame(body, hd, 1200, 560, 1.75)
    for x in (300, 900, 1900):
        s += f'<path d="M{x},0 L{x+120},0 L{x-280},1350 L{x-400},1350 Z" fill="#ffffff" opacity="0.06"/>'
    return S(s)
@art
def eyes_side():
    return S('<rect width="2400" height="1350" fill="#0a0a14"/>' + glow(1500, 500, 1000, "moon", 0.45) +
             bride_bust(1050, 760, 4.8, rim="#e8f0ff", look=0.9, turn=0.35, lids=0.15, bouquet=False))
@art
def street_chih2(): return S(QM.persp_street("night", seed=31, whispers=True), QM.fog_band(1200, 0.35, 32))
@art
def street_chih3(): return S(QM.persp_street("night", seed=33, portal=True), QM.fog_band(1180, 0.3, 34))
@art
def shop_fog():
    s = shopfront_svg("night", mannequin_in=True) + '<rect width="2400" height="1350" fill="#02040c" opacity="0.35"/>'
    s += moon(2150, 70, 50) + QM.fog_band(1000, 0.35, 41) + QM.fog_band(1250, 0.5, 42)
    return S(s)
@art
def mother_dark(): return S(portrait_bg("moon"), mother_bust(1200, 600, 1.9, rim=MOONRIM, look=-0.4, lids=0.5, smile=-0.25), '<rect width="2400" height="1350" fill="#04081a" opacity="0.3"/>')
@art
def daughter_veil(): return S(portrait_bg("moon"), bride_bust(1200, 600, 1.9, rim=MOONRIM, sk=SK_HIJA, look=0.35, turn=0.2, lids=0.35, smile=0.25))


def write(names):
    for n in names:
        open(os.path.join(A, n + ".svg"), "w").write(ART[n]())


if __name__ == "__main__":
    write(sys.argv[1:] or list(ART))
