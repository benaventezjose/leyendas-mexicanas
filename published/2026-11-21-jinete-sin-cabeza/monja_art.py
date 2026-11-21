#!/usr/bin/env python3
"""Illustrations for 'La Monja de La Concepción' (Ciudad de México, siglo XVI) — writes art/*.svg (2400x1350).
Reuses helpers of earlier videos (beso_art, chars, base_chars, qm_art = La Calle de la Quemada 1550s, aguacate_art,
pas_art, sb_art, cadejo_art). New here: nun_head/nun_bust (Concepcionista habit: black veil, white wimple, white habit,
blue mantle, medallion), nun_full + ghost nun, the convent huerto with the durazno, cloister, cell, gate, Veracruz,
scaffold in the Plaza Mayor, salted lot, the church today.
Usage: python3 make_art.py [name ...]   then: node /home/claude/pipeline/render_svg.js art/*.svg"""
import sys, os, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '/home/claude/pipeline'); sys.path.insert(0, HERE)
from art import *
from chars import place, man_full, woman_full, bust_frame, luis_bust, SIL
from base_chars import uid, grad_lin, grad_rad, head
import beso_art as BA
from beso_art import S, clouds, room_walls, candle_at, flame, table_wood, portrait_bg, MOONRIM
import qm_art as QM
import pas_art as PA
import aguacate_art as AG
from aguacate_art import canopy, branch

A = os.path.join(HERE, "art"); os.makedirs(A, exist_ok=True)
ART = {}
def art(fn):
    ART[fn.__name__] = fn; return fn

WARM = "#ffcf8a"; RED = "#c8141a"
inner = PA.inner
SK_MARIA = dict(base="#dcb398", light="#efcdb2", hi="#fae2cc", shadow="#a07460", deep="#56382c")
SK_GHOST = dict(base="#b8c6d6", light="#d6e2ee", hi="#eef4fa", shadow="#7a8aa0", deep="#3a4658")


def crop(svgstr, k, cx, cy, extra=""):
    return S(f'<g transform="translate(1200,675) scale({k}) translate({-cx},{-cy})">{inner(svgstr)}</g>', extra)


def dim(op=0.3, col="#02040a"):
    return f'<rect width="2400" height="1350" fill="{col}" opacity="{op}"/>'


# ============================================================================ THE NUN
def nun_head(look=0.0, turn=0.0, lids=0.3, smile=0.1, sad=False, rim="#9fc2e8", ghost=False, hollow=False,
             eyes_closed=False, glow_eyes=False):
    g = uid("nh")
    sk = SK_GHOST if ghost else SK_MARIA
    vb = ("#1a2232", "#3a4a66", "#5a6e90") if ghost else ("#030306", "#0c0c14", "#1c1c28")
    wc = ("#9aaec6", "#d8e4f2", "#f4f8fc") if ghost else ("#9a9ca8", "#dcdee6", "#f6f6f8")
    s = (f'<defs>{grad_lin(g+"v", [(0, vb[0], 1), (0.6, vb[1], 1), (1, vb[2], 1)], -260, 0, 260, 0)}'
         f'{grad_lin(g+"w", [(0, wc[0], 1), (0.45, wc[1], 1), (0.8, wc[2], 1), (1, wc[1], 1)], -200, 0, 200, 0)}</defs>')
    # black veil behind, falling over the shoulders
    s += (f'<path d="M-140,-170 C-170,-262 170,-262 140,-170 C170,-40 190,140 230,330 C240,390 238,440 226,470 C206,400 186,310 160,262 L-160,262 C-186,310 -206,400 -226,470 C-238,440 -240,390 -230,330 C-190,140 -170,-40 -140,-170 Z" '
          f'fill="url(#{g}v)" opacity="{0.75 if ghost else 1}"/>')
    for i in range(7):
        x = -200 + i * 66
        s += f'<path d="M{x*0.45:.0f},-200 C{x*0.7:.0f},-60 {x*0.9:.0f},120 {x:.0f},{300 if abs(x)<150 else 440}" stroke="{"#0a1220" if ghost else "#000"}" stroke-width="7" fill="none" opacity="0.45"/>'
    s += f'<path d="M140,-170 C170,-40 190,140 230,330 C244,380 240,420 228,446" stroke="{rim}" stroke-width="6" fill="none" opacity="0.7"/>'
    s += f'<path d="M-140,-170 C-170,-40 -190,140 -230,330" stroke="{rim}" stroke-width="3" fill="none" opacity="0.25"/>'
    s += head(look=look, smile=(-0.35 if sad else smile), lids=(0.55 if sad else lids), rim=rim, turn=turn, eyes_closed=eyes_closed,
              sk=sk, headwrap=False, back_curls=False, earring=False, neck=False, lips=(("#8a9cb0", "#9aaec0") if ghost else ("#9a5a52", "#b46e64")),
              iris=("#0a0e18" if ghost else "#2a1a10"), brow_w=0.75)
    if sad:
        s += '<path d="M-40,-2 C-42,20 -40,40 -42,58" stroke="#cfe0ff" stroke-width="4" fill="none" opacity="0.6"/>'
    if hollow:
        for sx in (-32, 32):
            s += f'<ellipse cx="{sx + look*6:.0f}" cy="-19" rx="25" ry="15" fill="#05070c" opacity="0.92"/>'
            s += f'<ellipse cx="{sx:.0f}" cy="-12" rx="34" ry="26" fill="#2a3448" opacity="0.4" filter="url(#blur1)"/>'
    if glow_eyes:
        for sx in (-32, 32):
            s += f'<circle cx="{sx + look*6:.0f}" cy="-19" r="7" fill="#f4f8ff"/><circle cx="{sx + look*6:.0f}" cy="-19" r="18" fill="#cfe0ff" opacity="0.5" filter="url(#blur1)"/>'
    # white wimple (toca) framing the face, covering neck and chest
    wim = ("M-120,-150 C-122,-60 -126,60 -140,150 C-150,200 -172,236 -200,262 C-120,304 120,304 200,262 C172,236 150,200 140,150 C126,60 122,-60 120,-150 "
           "C100,-192 -100,-192 -122,-150 Z "
           "M-70,-96 C-30,-108 30,-108 70,-96 C82,-24 78,36 62,70 C46,100 22,118 0,121 C-22,118 -46,100 -62,70 C-78,36 -82,-24 -70,-96 Z")
    s += f'<path d="{wim}" fill="url(#{g}w)" fill-rule="evenodd" opacity="{0.85 if ghost else 1}"/>'
    s += '<path d="M-62,70 C-46,100 -22,118 0,121 C22,118 46,100 62,70" stroke="#000" stroke-width="10" fill="none" opacity="0.12" filter="url(#blur1)"/>'
    for i in range(6):
        x = -120 + i * 48
        s += f'<path d="M{x*0.55:.0f},140 C{x*0.75:.0f},200 {x*0.95:.0f},250 {x*1.1:.0f},285" stroke="#6a6e80" stroke-width="3" fill="none" opacity="0.35"/>'
    s += '<path d="M-140,160 C-90,190 90,190 140,160" stroke="#7a7e90" stroke-width="3" fill="none" opacity="0.35"/>'
    s += f'<path d="M120,-150 C122,-60 126,60 140,150 C150,200 172,236 200,262" stroke="{rim}" stroke-width="5" fill="none" opacity="0.6"/>'
    # forehead band + front of veil
    s += f'<path d="M-124,-148 C-90,-170 90,-170 124,-148 L120,-120 C80,-132 -80,-132 -120,-120 Z" fill="{wc[1]}" opacity="{0.85 if ghost else 1}"/>'
    s += f'<path d="M-132,-150 C-136,-224 136,-224 132,-150 C96,-170 -96,-170 -132,-150 Z" fill="url(#{g}v)" opacity="{0.8 if ghost else 1}"/>'
    s += f'<path d="M30,-216 C90,-208 128,-186 132,-150" stroke="{rim}" stroke-width="5" fill="none" opacity="0.75"/>'
    return s


def nun_body(g, rim, ghost=False):
    hab = ("#7a8aa0", "#c8d4e2", "#eef2f8") if ghost else ("#8a8a90", "#d2d0cc", "#f0eeea")
    man = ("#1a2a44", "#3a5a86", "#6a8ab8") if ghost else ("#0c1a34", "#1c3a6a", "#3a62a0")
    s = (f'<defs>{grad_lin(g+"h", [(0, hab[0], 1), (0.55, hab[1], 1), (0.85, hab[2], 1), (1, hab[1], 1)], -340, 0, 340, 0)}'
         f'{grad_lin(g+"m", [(0, man[0], 1), (0.6, man[1], 1), (1, man[2], 1)], -360, 0, 360, 0)}</defs>')
    s += f'<path d="M-250,226 C-170,236 -140,250 -130,262 L130,262 C140,250 170,236 250,226 C320,270 350,400 360,660 L-360,660 C-350,400 -320,270 -250,226 Z" fill="url(#{g}h)"/>'
    # scapular
    s += f'<path d="M-110,250 L110,250 L118,660 L-118,660 Z" fill="{hab[2]}" opacity="0.55"/>'
    for x in (-60, 0, 60):
        s += f'<path d="M{x},270 L{x*1.1:.0f},660" stroke="#6a6a74" stroke-width="3" opacity="0.3"/>'
    # blue mantle over the shoulders
    s += f'<path d="M-250,226 C-300,250 -350,380 -380,660 L-230,660 C-220,480 -200,340 -170,250 Z" fill="url(#{g}m)"/>'
    s += f'<path d="M250,226 C300,250 350,380 380,660 L230,660 C220,480 200,340 170,250 Z" fill="url(#{g}m)"/>'
    s += f'<path d="M250,226 C300,250 350,380 380,660" stroke="{rim}" stroke-width="6" fill="none" opacity="0.7"/>'
    # medallion of the Immaculate
    s += '<ellipse cx="0" cy="400" rx="62" ry="80" fill="#c9a24a"/><ellipse cx="0" cy="400" rx="50" ry="68" fill="#e8dcc0"/>'
    s += '<path d="M0,350 C-14,350 -18,366 -14,378 C-30,400 -34,440 -30,456 L30,456 C34,440 30,400 14,378 C18,366 14,350 0,350 Z" fill="#3a62a0"/>'
    s += '<ellipse cx="0" cy="362" rx="9" ry="11" fill="#d8b49a"/><path d="M-20,456 L20,456" stroke="#c9a24a" stroke-width="5"/>'
    # rosary
    for i in range(18):
        t = i / 17; px = -170 + 90 * t; py = 300 + 300 * t
        s += f'<circle cx="{px:.0f}" cy="{py:.0f}" r="7" fill="#1a1410"/><circle cx="{px-2:.0f}" cy="{py-2:.0f}" r="2" fill="#8a7a6a"/>'
    s += '<path d="M-80,600 L-80,650 M-94,616 L-66,616" stroke="#2a2018" stroke-width="7"/>'
    return s


def nun_bust(x, y, k=1.0, rim="#9fc2e8", ghost=False, **hk):
    g = uid("nb")
    return bust_frame(nun_body(g, rim, ghost), nun_head(rim=rim, ghost=ghost, **hk), x, y, k)


def nun_full(rim=MOONRIM, ghost=False, fill=None, praying=True):
    """standing nun, feet at 0,0, ~1000 tall"""
    g = uid("nf")
    vb = "#2a3a58" if ghost else (fill or "#05060a")
    hab = "#c8d6ea" if ghost else "#2a2c34"
    s = f'<defs>{grad_lin(g+"h", [(0, "#0a0c12" if not ghost else "#6a7c9a", 1), (0.7, hab, 1), (1, "#4a4e5a" if not ghost else "#eef4ff", 1)], -200, 0, 200, 0)}</defs>'
    # habit
    s += f'<path d="M-120,-640 C-170,-500 -200,-250 -230,0 L230,0 C200,-250 170,-500 120,-640 Z" fill="url(#{g}h)"/>'
    for i in range(7):
        x = -180 + i * 60
        s += f'<path d="M{x*0.5:.0f},-560 C{x*0.7:.0f},-380 {x*0.9:.0f},-200 {x:.0f},0" stroke="#000" stroke-width="6" opacity="0.25" fill="none"/>'
    # mantle
    s += f'<path d="M-130,-700 C-220,-560 -260,-300 -280,0 L-170,0 C-150,-300 -130,-520 -60,-660 Z" fill="{"#3a5a8a" if ghost else "#0a1222"}"/>'
    s += f'<path d="M130,-700 C220,-560 260,-300 280,0 L170,0 C150,-300 130,-520 60,-660 Z" fill="{"#3a5a8a" if ghost else "#0a1222"}"/>'
    # veil
    s += f'<path d="M-80,-860 C-96,-920 96,-920 80,-860 C110,-780 150,-680 170,-560 C100,-530 -100,-530 -170,-560 C-150,-680 -110,-780 -80,-860 Z" fill="{vb}"/>'
    # wimple + face
    s += f'<path d="M-62,-860 C-66,-800 -80,-720 -110,-660 L110,-660 C80,-720 66,-800 62,-860 C40,-880 -40,-880 -62,-860 Z" fill="{"#eef4ff" if ghost else "#b8bcc6"}"/>'
    s += f'<ellipse cx="0" cy="-792" rx="34" ry="46" fill="{"#d0dcea" if ghost else "#6a4a3a"}"/>'
    if ghost:
        s += '<ellipse cx="-13" cy="-800" rx="9" ry="6" fill="#05070c"/><ellipse cx="13" cy="-800" rx="9" ry="6" fill="#05070c"/>'
    if praying:
        s += f'<path d="M-30,-560 C-20,-600 20,-600 30,-560 L18,-500 L-18,-500 Z" fill="{"#e8f0fa" if ghost else "#5a4034"}"/>'
        s += f'<path d="M-90,-640 C-80,-580 -50,-540 -20,-530 M90,-640 C80,-580 50,-540 20,-530" stroke="{hab}" stroke-width="40" fill="none" stroke-linecap="round"/>'
    if rim:
        s += f'<path d="M80,-860 C110,-780 150,-680 170,-560 M130,-700 C220,-560 260,-300 280,0" stroke="{rim}" stroke-width="7" fill="none" opacity="0.8"/>'
        s += f'<path d="M62,-860 C66,-800 80,-720 110,-660" stroke="{rim}" stroke-width="4" fill="none" opacity="0.6"/>'
    return s


def ghost_nun_layer(x, y, k):
    s = glow(x, y - 520 * k, 700 * k, "moon", 0.55)
    s += f'<g opacity="0.8" filter="url(#ghost)">{place(nun_full(rim="#eef6ff", ghost=True, praying=False), x, y, k)}</g>'
    # trailing mist at the hem
    r = random.Random(7)
    for i in range(14):
        s += f'<ellipse cx="{x + r.uniform(-260, 260)*k:.0f}" cy="{y + r.uniform(-60, 20)*k:.0f}" rx="{r.uniform(80,180)*k:.0f}" ry="{r.uniform(20,40)*k:.0f}" fill="#cfe0f4" opacity="{r.uniform(0.1,0.25):.2f}" filter="url(#blur3)"/>'
    return s


# ============================================================================ CONVENT PIECES
def arch_row(x0, x1, y_base, h, n, col="#1a1c26", inner_col="#04060a", rim=None, lit=None):
    w = (x1 - x0) / n; s = f'<rect x="{x0}" y="{y_base-h-60}" width="{x1-x0}" height="{h+60}" fill="{col}"/>'
    for i in range(n):
        ax = x0 + i * w + w * 0.14; aw = w * 0.72; top = y_base - h
        d = f"M{ax:.0f},{y_base} L{ax:.0f},{top+aw/2:.0f} A{aw/2:.0f},{aw/2:.0f} 0 0 1 {ax+aw:.0f},{top+aw/2:.0f} L{ax+aw:.0f},{y_base} Z"
        s += f'<path d="{d}" fill="{inner_col}"/>'
        if lit and i in lit:
            s += f'<path d="{d}" fill="#3a2410" opacity="0.8"/>' + glow(ax + aw / 2, y_base - aw * 0.4, aw * 0.9, "warm", 0.35)
        if rim:
            s += f'<path d="M{ax+aw:.0f},{y_base} L{ax+aw:.0f},{top+aw/2:.0f} A{aw/2:.0f},{aw/2:.0f} 0 0 0 {ax+aw/2:.0f},{top:.0f}" stroke="{rim}" stroke-width="4" fill="none" opacity="0.4"/>'
    s += f'<rect x="{x0}" y="{y_base-h-70}" width="{x1-x0}" height="16" fill="#000" opacity="0.4"/>'
    return s


def bell_tower(x, yb, k=1.0, col="#141824", rim=MOONRIM, bell_lit=False):
    s = f'<g transform="translate({x},{yb}) scale({k})">'
    s += f'<rect x="-110" y="-700" width="220" height="700" fill="{col}"/>'
    s += f'<rect x="-90" y="-940" width="180" height="250" fill="{col}"/>'
    s += '<path d="M-50,-700 L-50,-830 A50,50 0 0 1 50,-830 L50,-700 Z" fill="#05070c"/>'
    s += f'<path d="M-30,-760 C-30,-800 30,-800 30,-760 L38,-720 L-38,-720 Z" fill="{"#c9a24a" if bell_lit else "#2a2418"}"/>'
    s += f'<path d="M-100,-940 C-60,-1020 60,-1020 100,-940 Z" fill="{col}"/><path d="M0,-1010 L0,-1090 M-24,-1060 L24,-1060" stroke="{col}" stroke-width="12"/>'
    s += f'<path d="M110,-700 L110,0 M90,-940 L90,-700" stroke="{rim}" stroke-width="6" opacity="0.55"/>'
    return s + '</g>'


def peach_tree(x, yb, k=1.0, rim=MOONRIM, mood="night", seed=3, bloom=False):
    """old twisted peach tree: crooked trunk, spreading low branches, lanceolate leaves, round peaches"""
    r = random.Random(seed)
    trunk = "#06050a" if mood != "dawn" else "#1a1418"
    s = f'<g transform="translate({x},{yb}) scale({k})">'
    s += f'<path d="M-60,0 C-50,-120 -80,-220 -40,-330 C-20,-390 30,-420 20,-500 L70,-500 C80,-420 40,-380 50,-320 C80,-220 50,-110 70,0 Z" fill="{trunk}"/>'
    s += f'<path d="M50,-320 C80,-220 50,-110 70,0" stroke="{rim}" stroke-width="5" fill="none" opacity="0.6"/>'
    for (a, b, c, d, w) in ((20, -460, -420, -620, 34), (40, -470, 460, -640, 32), (-20, -360, -380, -420, 26), (40, -380, 380, -470, 24), (40, -500, 60, -780, 26), (-10, -480, -200, -760, 22)):
        s += branch(a, b, c, d, w, trunk, 0.15)
    dark = ("#040a08", "#07120c", "#0a180f") if mood != "dawn" else ("#1a2a1e", "#24382a", "#304a36")
    s += canopy(0, -640, 560, 230, seed, rim if rim else None, dark, n=520, fruit=0, lit=0.5, leaf=0.9)
    for i in range(34):
        a = r.uniform(0.1, math.pi - 0.1); d = r.uniform(0.25, 0.95)
        px = math.cos(a) * 520 * d; py = -640 + math.sin(a) * 220 * d
        rr = r.uniform(16, 24)
        col = "#c87a4a" if mood == "dawn" else "#8a4a32"
        s += f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{rr:.0f}" fill="{col}"/>'
        s += f'<circle cx="{px+rr*0.3:.0f}" cy="{py-rr*0.3:.0f}" r="{rr*0.55:.0f}" fill="{"#f0b080" if mood=="dawn" else "#c8806a"}" opacity="0.55"/>'
        s += f'<path d="M{px:.0f},{py-rr:.0f} C{px+3:.0f},{py-rr*0.4:.0f} {px+2:.0f},{py+rr*0.4:.0f} {px:.0f},{py+rr:.0f}" stroke="#4a2018" stroke-width="2" fill="none" opacity="0.5"/>'
    if bloom:
        for i in range(70):
            a = r.uniform(0, math.tau); d = math.sqrt(r.random())
            px = math.cos(a) * 540 * d; py = -640 + math.sin(a) * 230 * d
            s += f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{r.uniform(5,9):.0f}" fill="#f4c8d4" opacity="0.75"/>'
    return s + '</g>'


def huerto_svg(mood="night", seed=1, tree_x=1150, ghost=False):
    if mood == "dawn":
        s = sky("#2a3450", "#e8a880", "#8a7088") + glow(1900, 900, 900, "warm", 0.4)
        wall = "#4a3a40"; ground = "#2a2a22"; rim = "#ffd0a0"
    elif mood == "red":
        s = sky("#0a0204", "#3a0a10") + glow(1200, 500, 900, "red", 0.5); wall = "#140608"; ground = "#0a0404"; rim = "#ff6a50"
    else:
        s = sky("#030812", "#1a2a44") + stars(160, seed, 600) + moon(1880, 230, 95) + glow(1880, 230, 500, "moon", 0.5)
        wall = "#121620"; ground = "#0a0e12"; rim = MOONRIM
    s += bell_tower(380, 760, 0.8, col=wall, rim=rim)
    s += arch_row(0, 2400, 900, 330, 9, col=wall, inner_col="#020306", rim=rim, lit=(1, 6) if mood == "night" else None)
    s += f'<rect x="0" y="560" width="2400" height="22" fill="{rim}" opacity="0.15"/>'
    s += f'<rect x="0" y="900" width="2400" height="450" fill="{ground}"/>'
    r = random.Random(seed + 5)
    for i in range(110):  # herbs, beds
        x = r.uniform(0, 2400); y = r.uniform(930, 1350); h = r.uniform(20, 60) * (y / 1000)
        s += f'<path d="M{x:.0f},{y:.0f} q{r.uniform(-12,12):.0f},{-h:.0f} {r.uniform(-20,20):.0f},{-h*1.4:.0f}" stroke="#05080a" stroke-width="5" fill="none"/>'
    s += f'<path d="M0,1180 C600,1120 1800,1120 2400,1180" stroke="{rim}" stroke-width="2" opacity="0.15" fill="none"/>'
    # stone well
    s += '<ellipse cx="1950" cy="1050" rx="150" ry="40" fill="#05060a"/><rect x="1800" y="960" width="300" height="90" fill="#151820"/>'
    s += f'<path d="M2100,960 L2100,1050" stroke="{rim}" stroke-width="5" opacity="0.5"/><path d="M1830,960 L1830,820 L2070,820 L2070,960" stroke="#0a0c10" stroke-width="18" fill="none"/>'
    s += peach_tree(tree_x, 1150, 1.0, rim=rim, mood=mood, seed=seed + 2)
    if ghost:
        s += ghost_nun_layer(tree_x, 1150, 0.55)
    return s


@art
def huerto(): return S(huerto_svg("night", 1), QM.fog_band(1120, 0.25, 3))
@art
def huerto_fog(): return S(huerto_svg("night", 4), QM.fog_band(1060, 0.4, 5), QM.fog_band(1200, 0.35, 6), dim(0.15))
@art
def huerto_dawn(): return S(huerto_svg("dawn", 7), QM.fog_band(1150, 0.2, 8))
@art
def huerto_red(): return S(huerto_svg("red", 9), QM.fog_band(1150, 0.2, 10))
@art
def huerto_ghost(): return S(huerto_svg("night", 11, ghost=True), QM.fog_band(1120, 0.3, 12))
@art
def l_ghost_nun():  # transparent layer placed at the tree of 'huerto' (tree base 1150,1150)
    return S(ghost_nun_layer(1150, 1150, 0.55))
@art
def l_ghost_nun_far():
    return S(ghost_nun_layer(1150, 1120, 0.38))


@art
def durazno_close():
    s = sky("#030812", "#14223a") + stars(120, 21, 1350) + moon(1850, 300, 130) + glow(1850, 300, 600, "moon", 0.6)
    s += peach_tree(1100, 2300, 2.3, rim=MOONRIM, seed=22, bloom=True)
    return S(s, dim(0.1))


@art
def durazno_bloom():
    s = sky("#1a2238", "#5a4a6a") + glow(1700, 400, 700, "moon", 0.5)
    s += peach_tree(1200, 1900, 1.9, rim="#e8d0e0", seed=24, bloom=True, mood="dawn")
    return S(s)


@art
def fallen_peaches():
    """grass under the tree at dawn: fallen peaches, petals, a black veil lying on the grass (implied, no body)"""
    s = '<rect width="2400" height="1350" fill="#141a18"/>' + glow(1900, 0, 1100, "warm", 0.35)
    r = random.Random(31)
    for i in range(500):
        x = r.uniform(0, 2400); y = r.uniform(0, 1350); h = r.uniform(30, 90)
        s += f'<path d="M{x:.0f},{y:.0f} q{r.uniform(-15,15):.0f},{-h:.0f} {r.uniform(-25,25):.0f},{-h*1.3:.0f}" stroke="{r.choice(["#0a120e","#16221a","#22302a"])}" stroke-width="5" fill="none"/>'
    # veil
    s += ('<path d="M700,820 C820,700 1100,660 1350,720 C1560,770 1700,900 1640,1000 C1500,1080 1200,1040 1000,1090 C820,1130 640,1020 700,820 Z" fill="#06060a"/>'
          ''.join(f'<path d="M{720+i*60},{860+i*12} C{880+i*50},{780+i*20} {1150+i*30},{760+i*25} {1380+i*20},{800+i*30}" stroke="#262836" stroke-width="{8-i*0.6:.0f}" fill="none" opacity="0.75"/>' for i in range(8))
          + '<path d="M700,820 C760,900 820,1000 1000,1090" stroke="#9fb0c8" stroke-width="4" fill="none" opacity="0.35"/>'
          '<path d="M1350,720 C1560,770 1700,900 1640,1000" stroke="#ffd0a0" stroke-width="5" fill="none" opacity="0.5"/>')
    for i in range(14):
        x = r.uniform(200, 2200); y = r.uniform(300, 1250); rr = r.uniform(26, 40)
        if 650 < x < 1700 and 650 < y < 1100: continue
        s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rr:.0f}" fill="#c87a4a"/><circle cx="{x+rr*0.3:.0f}" cy="{y-rr*0.3:.0f}" r="{rr*0.5:.0f}" fill="#f0b080" opacity="0.5"/>'
    for i in range(90):
        s += f'<ellipse cx="{r.uniform(0,2400):.0f}" cy="{r.uniform(0,1350):.0f}" rx="9" ry="6" fill="#f4c8d4" opacity="{r.uniform(0.5,0.9):.2f}" transform="rotate({r.uniform(0,180):.0f} 0 0)"/>'
    return S(s, dim(0.15, "#0a0a1a"))


@art
def cloister():
    s = sky("#030812", "#16243a") + glow(1200, 120, 600, "moon", 0.4)
    s += arch_row(0, 2400, 760, 360, 7, col="#1a1e2a", inner_col="#06080e", rim=MOONRIM)
    s += arch_row(0, 2400, 1180, 300, 5, col="#20242e", inner_col="#05070c", rim=MOONRIM, lit=(1,))
    s += '<rect x="0" y="1180" width="2400" height="170" fill="#0e1016"/>'
    # fountain
    s += '<ellipse cx="1200" cy="1060" rx="300" ry="50" fill="#0a0c12"/><rect x="900" y="980" width="600" height="80" fill="#1a1e28"/>'
    s += '<rect x="1170" y="860" width="60" height="130" fill="#1a1e28"/><ellipse cx="1200" cy="860" rx="110" ry="24" fill="#20242e"/>'
    s += place(nun_full(rim=WARM), 640, 1180, 0.22)
    return S(s, QM.fog_band(1150, 0.2, 41))


@art
def cell():
    s = room_walls("#232430", "#08080e", "#141218")
    s += '<rect x="1500" y="330" width="260" height="300" fill="#1a3048"/>' + glow(1630, 470, 420, "moon", 0.9)
    for i in range(5):
        s += f'<rect x="{1515+i*55}" y="330" width="14" height="300" fill="#05060a"/>'
    s += '<path d="M1500,630 L1250,1350 L1950,1350 L1760,630 Z" fill="#9fc2e8" opacity="0.08"/>'
    # cot
    s += '<rect x="300" y="900" width="900" height="70" fill="#2a2018"/><rect x="300" y="860" width="900" height="50" fill="#5a5a66"/>'
    s += '<rect x="320" y="970" width="30" height="160" fill="#140e0a"/><rect x="1150" y="970" width="30" height="160" fill="#140e0a"/>'
    # crucifix
    s += '<path d="M750,260 L750,560 M660,340 L840,340" stroke="#1a120c" stroke-width="22"/><path d="M750,360 L750,470" stroke="#8a6a5a" stroke-width="10"/>'
    s += candle_at(1300, 980, 160) + '<rect x="1250" y="980" width="200" height="200" fill="#1a120c"/>'
    return S(s)


@art
def cell_nun():
    s = inner(ART["cell"]())
    s += place(nun_full(rim=WARM), 1000, 1200, 0.6)
    return S(s)


@art
def cell_window():
    """María at the barred window of her cell, seen from outside"""
    s = '<rect width="2400" height="1350" fill="#151820"/><rect width="2400" height="1350" fill="#000" filter="url(#plaster)" opacity="0.5"/>'
    s += '<rect x="700" y="160" width="1000" height="1100" fill="#06060a"/>' + glow(1200, 700, 700, "warm", 0.45)
    s += nun_bust(1200, 640, 1.45, rim=WARM, look=0.4, lids=0.45, sad=True)
    for i in range(8):
        s += f'<rect x="{730+i*130}" y="160" width="26" height="1100" fill="#040406"/><rect x="{748+i*130}" y="160" width="6" height="1100" fill="#9fc2e8" opacity="0.4"/>'
    for y in (420, 800):
        s += f'<rect x="700" y="{y}" width="1000" height="24" fill="#040406"/>'
    s += '<rect x="640" y="120" width="60" height="1200" fill="#1e222c"/><rect x="1700" y="120" width="60" height="1200" fill="#1e222c"/>'
    return S(s, dim(0.15))


# ---- portraits
@art
def nun_portrait(): return S(portrait_bg("candle"), nun_bust(1200, 560, 1.75, rim=WARM, look=-0.2, lids=0.35, smile=0.0))
@art
def nun_sad(): return S(portrait_bg("moon"), nun_bust(1200, 560, 1.75, rim=MOONRIM, look=0.3, sad=True), dim(0.2))
@art
def nun_pray(): return S(portrait_bg("candle"), nun_bust(1200, 560, 1.75, rim=WARM, eyes_closed=True, smile=-0.1))
@art
def nun_ghost(): return S(portrait_bg("ghost"), nun_bust(1200, 560, 1.75, rim="#e8f2ff", ghost=True, hollow=True, smile=-0.2), dim(0.1, "#0a1a3a"))
@art
def nun_flash():
    s = '<rect width="2400" height="1350" fill="#0a0204"/>' + glow(1200, 500, 1100, "red", 0.5)
    s += nun_bust(1200, 760, 3.6, rim="#ff8a70", ghost=True, hollow=True, glow_eyes=True, smile=-0.4)
    return S(s)
@art
def maria_lady(): return S(portrait_bg("moon"), QM.bea_bust(1200, 560, 1.75, rim=MOONRIM, dress=("#0a1420", "#1a3a5a", "#2a5a7a"), look=0.15, lids=0.3, smile=0.35))
@art
def maria_soft(): return S(portrait_bg("candle"), QM.bea_bust(1200, 560, 1.75, rim=WARM, dress=("#0a1420", "#1a3a5a", "#2a5a7a"), look=-0.25, lids=0.4, smile=0.6))
@art
def maria_sad(): return S(portrait_bg("moon"), QM.bea_bust(1200, 560, 1.75, rim=MOONRIM, dress=("#0a1420", "#1a3a5a", "#2a5a7a"), look=0.3, sad=True), dim(0.2))
@art
def maria_fear(): return S(portrait_bg("candle"), QM.bea_bust(1200, 560, 1.75, rim="#ffb860", dress=("#0a1420", "#1a3a5a", "#2a5a7a"), look=-0.5, turn=-0.15, fear=True))
@art
def alonso(): return S(portrait_bg("candle"), QM.martin_bust(1200, 560, 1.75, rim=WARM, look=0.2, cold=True), candle_at(1950, 1300, 160))
@art
def alonso_red(): return S(portrait_bg("red"), QM.martin_bust(1200, 560, 1.75, rim="#ff6a50", look=0.0, cold=True))
@art
def gil(): return QM.ART["gonzalo_portrait"]()
@art
def brothers():
    s = portrait_bg("candle") + QM.martin_bust(780, 620, 1.35, rim=WARM, look=0.4, cold=True)
    s += QM.martin_bust(1640, 640, 1.3, rim=WARM, look=-0.4, cold=True, hat=False)
    return S(s, candle_at(1210, 1250, 180))
@art
def arrutia(): return S(portrait_bg("moon"), luis_bust(1200, 560, 1.75, look=-0.2, turn=-0.1))
@art
def arrutia_smile(): return S(portrait_bg("candle"), luis_bust(1200, 560, 1.75, rim=WARM, look=0.25, smile=0.8))
@art
def arrutia_shock(): return S(portrait_bg("moon"), luis_bust(1200, 560, 1.75, look=0.3, shock=True), dim(0.2))


# ---- places
@art
def plaza_1560(): return QM.ART["plaza_1550"]()
@art
def ciudad_noche(): return QM.ART["palacio_night"]()
@art
def casa_avila(): return QM.ART["casona"]()
@art
def convent_ext():
    s = BA.temple_facade().replace("#c07060", "#3a4a66").replace("#5a4a70", "#2a3048").replace("#1a2240", "#050a14")
    return s.replace("</svg>", dim(0.35, "#06101e") + QM.fog_band(1250, 0.3, 51) + '</svg>')
@art
def convent_gate():
    s = inner(ART["convent_ext"]())
    s += place(man_full(hat=True, cape=True, rim=MOONRIM), 1500, 1250, 0.42)
    return S(s)
@art
def chapel(): return BA.ART["temple_interior"]()
@art
def corridor(): return QM.ART["corridor"]()
@art
def kneel(): return QM.ART["kneel"]()
@art
def courtship():
    s = inner(QM.ART["balcony_night"]())
    return S(s)


@art
def letter():
    s = BA.letters_table().replace("Tuyo siempre, L.", "Perdonadme. A.")
    return s
@art
def letter_close():
    s = '<rect width="2400" height="1350" fill="#0a0604"/>' + table_wood(300) + glow(1900, 300, 700, "warm", 0.5)
    s += '<path d="M500,180 L1900,140 L1960,1240 L540,1290 Z" fill="#e2d4b0"/><path d="M500,180 L1900,140 L1960,1240 L540,1290 Z" fill="#000" filter="url(#plaster)" opacity="0.15"/>'
    lines = ["Señora mía:", "Asuntos de mi oficio me obligan", "a partir lejos de esta ciudad.", "No me esperéis.", "Que Dios os guarde.", "                        A."]
    for i, t in enumerate(lines):
        s += f'<text x="660" y="{360+i*150}" font-family="IM FELL English" font-size="{78 if i else 86}" fill="#2a1a10" transform="rotate(-1.5 1200 700)">{t}</text>'
    s += '<circle cx="1700" cy="1120" r="60" fill="#8a1a1a"/><circle cx="1690" cy="1110" r="40" fill="#a82a2a"/>'
    return S(s, dim(0.1, "#0a0604"))


@art
def coins():
    s = '<rect width="2400" height="1350" fill="#0a0806"/>' + table_wood(600) + candle_at(1900, 760, 200)
    s += '<path d="M700,820 C700,700 1000,680 1100,760 C1180,820 1160,960 1000,990 C820,1020 700,940 700,820 Z" fill="#3a2414"/>'
    s += '<path d="M800,700 C860,640 960,640 1000,700" stroke="#1a100a" stroke-width="20" fill="none"/>'
    r = random.Random(61)
    for i in range(26):
        x = r.uniform(1050, 1650); y = r.uniform(880, 1150)
        s += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="44" ry="18" fill="#a8842a"/><ellipse cx="{x:.0f}" cy="{y-4:.0f}" rx="40" ry="14" fill="#e0bb5a"/>'
    s += place(man_full(hat=False, cape=True, rim=WARM), 450, 1350, 0.75)
    return S(s)


@art
def veracruz():
    s = sky("#030812", "#1a2a44") + stars(200, 71, 700) + moon(600, 260, 80) + glow(600, 260, 400, "moon", 0.5)
    s += water(820, 1350, "#0e1e2e", "#03080e") + reflection(600, 830, 1300)
    s += '<path d="M1500,820 L1560,760 L2200,760 L2260,820 Z" fill="#05070c"/><rect x="1640" y="680" width="80" height="80" fill="#05070c"/>'
    s += glow(1680, 700, 60, "warm", 0.8)
    # galleon
    g = '<path d="M-300,0 C-280,60 260,60 320,-20 L340,-80 L-320,-80 Z" fill="#020306"/>'
    g += '<path d="M-260,-80 L-260,-200 L-180,-200 L-180,-80 Z" fill="#020306"/>'
    for mx, mh in ((-120, 520), (60, 600), (220, 420)):
        g += f'<path d="M{mx},-80 L{mx},{-80-mh}" stroke="#020306" stroke-width="12"/>'
        for j in range(3):
            y = -80 - mh + 60 + j * mh * 0.28; w = 120 - j * 10
            g += f'<path d="M{mx-w},{y} C{mx-w*0.6},{y+70} {mx+w*0.6},{y+70} {mx+w},{y} L{mx+w-10},{y+110} C{mx+w*0.5},{y+150} {mx-w*0.5},{y+150} {mx-w+10},{y+110} Z" fill="#0a0e16"/>'
            g += f'<path d="M{mx-w},{y} C{mx-w*0.6},{y+70} {mx+w*0.6},{y+70} {mx+w},{y}" stroke="{MOONRIM}" stroke-width="3" fill="none" opacity="0.5"/>'
    s += f'<g transform="translate(1150,880) scale(0.9)">{g}</g>'
    s += '<rect x="0" y="1180" width="900" height="170" fill="#06080c"/>'
    s += place(man_full(hat=True, cape=True, rim=MOONRIM), 420, 1200, 0.32)
    return S(s, QM.fog_band(900, 0.2, 72))


@art
def scaffold():
    """Plaza Mayor at dawn, 1566: a black-draped scaffold, crowd, the cathedral works (implied execution, nothing shown)"""
    s = sky("#1a2034", "#c88a6a", "#5a4a5a") + glow(1700, 700, 900, "warm", 0.35)
    s += '<path d="M0,760 L2400,760 L2400,1350 L0,1350 Z" fill="#2a2420"/>'
    s += '<rect x="200" y="420" width="800" height="340" fill="#3a2e2a"/><rect x="560" y="260" width="90" height="180" fill="#3a2e2a"/><path d="M605,200 L605,270 M575,226 L635,226" stroke="#3a2e2a" stroke-width="10"/>'
    s += '<rect x="1500" y="520" width="900" height="240" fill="#2e2622"/>'
    for i in range(9):
        s += window(1540 + i * 96, 580, 50, 80, lit=False, arch=True)
    # scaffold
    s += '<rect x="900" y="760" width="620" height="170" fill="#050304"/><rect x="900" y="740" width="620" height="30" fill="#0a0606"/>'
    for i in range(7):
        s += f'<path d="M{920+i*100},770 L{940+i*100},930" stroke="#1a1010" stroke-width="5" opacity="0.6"/>'
    s += place(man_full(hat=False, cape=True, rim="#ffb080", fill="#050304"), 1050, 745, 0.18)
    s += place(man_full(hat=True, cape=True, rim="#ffb080", fill="#050304"), 1300, 745, 0.18)
    r = random.Random(81)
    for i in range(70):
        x = r.uniform(0, 2400); y = r.uniform(1000, 1360)
        if 880 < x < 1540 and y < 1100: continue
        f = woman_full(rebozo_head=True, rim="#ffb080", fill="#050304") if r.random() < 0.4 else man_full(hat=r.random() < 0.6, cape=r.random() < 0.5, rim="#ffb080", fill="#050304")
        s += place(f, x, y, 0.14 + (y - 1000) / 1400)
    return S(s, dim(0.2, "#0a0408"))


@art
def solar_sal():
    """the razed lot of the Ávila houses, sown with salt — rubble and white crust under the moon"""
    s = sky("#040912", "#1a2638") + stars(120, 91, 500) + moon(1800, 240, 80) + glow(1800, 240, 400, "moon", 0.5)
    s += '<rect x="0" y="560" width="500" height="400" fill="#141820"/><rect x="1900" y="520" width="500" height="440" fill="#141820"/>'
    for i in range(3):
        s += window(80 + i * 140, 640, 60, 100, lit=i == 1, arch=True) + window(1980 + i * 140, 620, 60, 100, lit=i == 2, arch=True)
    s += '<rect x="0" y="940" width="2400" height="410" fill="#1a1c22"/>'
    r = random.Random(92)
    for i in range(200):
        x = r.uniform(400, 2000); y = r.uniform(960, 1350)
        s += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r.uniform(20,90):.0f}" ry="{r.uniform(6,20):.0f}" fill="#dfe6ef" opacity="{r.uniform(0.25,0.6):.2f}"/>'
    for i in range(40):
        x = r.uniform(450, 1950); y = r.uniform(900, 1100); w = r.uniform(40, 140); h = r.uniform(20, 70)
        s += f'<path d="M{x:.0f},{y:.0f} l{w:.0f},{-h*0.3:.0f} l{w*0.2:.0f},{h:.0f} l{-w:.0f},{h*0.2:.0f} Z" fill="#0c0e14"/>'
    s += '<rect x="1100" y="620" width="40" height="340" fill="#0a0c12"/><rect x="1060" y="600" width="120" height="40" fill="#0a0c12"/>'
    return S(s, QM.fog_band(1100, 0.2, 93))


@art
def concepcion_today():
    s = sky("#0a1426", "#3a4a6a") + glow(1200, 600, 900, "warm", 0.25)
    s += '<rect x="0" y="1080" width="2400" height="270" fill="#1a1a20"/><rect x="0" y="1060" width="2400" height="30" fill="#2a2a30"/>'
    # tezontle church with a two-section tower and a dome
    c = "#4a1e1c"; st = "#9a8a7a"
    s += f'<rect x="500" y="520" width="1100" height="560" fill="{c}"/><rect x="500" y="520" width="1100" height="560" fill="#000" filter="url(#plaster)" opacity="0.35"/>'
    s += f'<path d="M1150,520 C1150,330 1450,330 1450,520 Z" fill="#3a2a2a"/><rect x="1285" y="270" width="30" height="80" fill="{st}"/>'
    s += f'<rect x="300" y="300" width="260" height="780" fill="{c}"/><rect x="320" y="120" width="220" height="200" fill="{c}"/><path d="M320,120 C360,40 500,40 540,120 Z" fill="{c}"/>'
    s += f'<path d="M380,300 L380,200 A50,50 0 0 1 480,200 L480,300 Z" fill="#0a0806"/><path d="M370,500 L370,420 A60,60 0 0 1 490,420 L490,500 Z" fill="#0a0806"/>'
    s += f'<rect x="300" y="300" width="260" height="20" fill="{st}"/><rect x="300" y="520" width="1300" height="18" fill="{st}"/>'
    s += f'<path d="M850,1080 L850,780 A110,110 0 0 1 1070,780 L1070,1080 Z" fill="#1a100a"/><path d="M820,1080 L820,760 M1100,1080 L1100,760" stroke="{st}" stroke-width="22"/>'
    s += glow(960, 900, 300, "warm", 0.5)
    for x in (200, 1800, 2200):
        s += f'<path d="M{x},1080 L{x},700 L{x+50},700" stroke="#0a0a0e" stroke-width="10" fill="none"/>' + glow(x + 50, 710, 160, "warm", 0.7)
    s += '<rect x="1700" y="900" width="200" height="120" rx="20" fill="#0a0c12"/><circle cx="1740" cy="1030" r="26" fill="#05060a"/><circle cx="1870" cy="1030" r="26" fill="#05060a"/>'
    return S(s)


@art
def reja():
    s = '<rect width="2400" height="1350" fill="#10131a"/><rect width="2400" height="1350" fill="#000" filter="url(#plaster)" opacity="0.5"/>'
    s += '<rect x="900" y="250" width="900" height="700" fill="#2a1a0c"/>' + glow(1350, 600, 600, "warm", 0.6)
    s += place(nun_full(rim=WARM), 1380, 1050, 0.62)
    for i in range(10):
        s += f'<rect x="{900+i*95}" y="250" width="22" height="700" fill="#030304"/>'
    for y in (420, 640, 860):
        s += f'<rect x="900" y="{y}" width="900" height="18" fill="#030304"/>'
    s += '<rect x="860" y="950" width="980" height="60" fill="#1e222c"/><rect x="0" y="1010" width="2400" height="340" fill="#08090c"/>'
    s += place(man_full(hat=True, cape=True, rim=MOONRIM), 560, 1400, 0.95)
    return S(s, dim(0.1))


@art
def book():
    s = QM.ART["chronicle"]().replace(">La Calle de la<", ">La Monja de<").replace(">Quemada<", ">La Concepción<")
    return s


@art
def title_bg():
    s = huerto_svg("night", 101, tree_x=1750)
    return S(s, QM.fog_band(1120, 0.35, 102), dim(0.25))


@art
def bells():
    s = sky("#030812", "#1a2a44") + stars(160, 111, 900) + moon(1900, 260, 90) + glow(1900, 260, 500, "moon", 0.5)
    s += bell_tower(1100, 1500, 1.25, col="#141824", bell_lit=True) + glow(1100, 1500-1.25*760, 160, "warm", 0.5)
    return S(s, QM.fog_band(1200, 0.3, 112))


@art
def nuns_line():
    """nuns walking in a line along the cloister with candles"""
    s = inner(ART["cloister"]())
    for i in range(6):
        x = 300 + i * 300
        s += place(nun_full(rim=WARM), x, 1300, 0.38) + glow(x, 1300 - 210, 90, "warm", 0.6) + flame(x, 1300 - 215, 0.6)
    return S(s)


@art
def l_fog(): return PA.ART["l_fog"]()
@art
def l_candle_glow(): return PA.ART["l_candle_glow"]()
@art
def l_moon_glow(): return S(glow(1150, 600, 800, "moon", 0.35))
@art
def red_flash(): return PA.ART["red_flash"]()
@art
def white_flash(): return PA.ART["white_flash"]()
@art
def black(): return S('<rect width="2400" height="1350" fill="#000"/>')


def write(names):
    for n in names:
        open(os.path.join(A, n + ".svg"), "w").write(ART[n]())


if __name__ == "__main__":
    write(sys.argv[1:] or [n for n in ART if not n.startswith("test")])
