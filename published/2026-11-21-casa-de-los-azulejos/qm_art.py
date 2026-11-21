#!/usr/bin/env python3
"""Illustrations for 'La Calle de la Quemada' — writes art/*.svg (2400x1350).
Builds on the colonial helpers of 'El Callejón del Beso' (beso_art.py, chars.py, base_chars.py).
Usage: python3 make_art.py [name ...]   then: node /home/claude/pipeline/render_svg.js art/*.svg"""
import sys, os, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '/home/claude/pipeline'); sys.path.insert(0, HERE)
from art import *
from chars import *
from base_chars import head, uid, grad_lin, grad_rad
import beso_art as BA
from beso_art import (S, lg, clouds, rail, room_walls, candle_at, flame, table_wood, portrait_bg, hand, sleeve, MOONRIM, flowerpot)

A = os.path.join(HERE, "art"); os.makedirs(A, exist_ok=True)
ART = {}
def art(fn):
    ART[fn.__name__] = fn; return fn

WARM = "#ffcf8a"; RED = "#c8141a"
SK_BEA = dict(base="#d6ab90", light="#ecc6aa", hi="#f8dcc6", shadow="#9a6e58", deep="#52342a")
SK_MAR = dict(base="#c99a7a", light="#ddb294", hi="#efcaae", shadow="#8a604a", deep="#46302a")
LAMP_XY = (452, 445)          # wall lantern position in every street view (l_lamp_glow matches it)
CANDLE_XY = (700, 640)        # generic candle glow position (l_candle_glow)


# ===================================================================== perspective street (CDMX, flat, cantera + tezontle)
VX, VY, W0 = 1200, 640, 1150

def P(X, Y, z, vx=VX):
    return (vx + X * W0 / z, VY + Y * W0 / z)

def quad(pts, fill, extra=""):
    return f'<path d="M{" L".join(f"{x:.0f},{y:.0f}" for x, y in pts)} Z" fill="{fill}" {extra}/>'

def wall_win(side, z0, z1, y0, y1, lit, vx=VX, light="#ffc865", bars=True):
    X = side
    pts = [P(X, y0, z0, vx), P(X, y0, z1, vx), P(X, y1, z1, vx), P(X, y1, z0, vx)]
    s = quad(pts, light if lit else "#0b1018")
    if lit:
        cx = sum(p[0] for p in pts) / 4; cy = sum(p[1] for p in pts) / 4
        s = glow(cx, cy, abs(pts[1][0] - pts[0][0]) * 2.2 + 30, "warm", 0.5) + s
    if bars:
        for k in range(1, 4):
            zz = z0 + (z1 - z0) * k / 4
            a, b = P(X, y0, zz, vx), P(X, y1, zz, vx)
            s += f'<path d="M{a[0]:.0f},{a[1]:.0f} L{b[0]:.0f},{b[1]:.0f}" stroke="#05070a" stroke-width="{max(1.5, 30/zz):.1f}"/>'
    s += f'<path d="M{" L".join(f"{x:.0f},{y:.0f}" for x, y in pts)} Z" stroke="#6a6052" stroke-width="{max(2, 26/z0):.0f}" fill="none" opacity="0.8"/>'
    return s

def persp_street(mood="night", vx=VX, seed=3, tower=True, portal=False, lamp_on=True, whispers=False, plaque=None,
                 modern=False, moon_on=True):
    r = random.Random(seed)
    if mood == "night":
        sky_ = sky("#040912", "#16263a") + stars(120, seed, 420); walls = ["#2a3340", "#3a2a2c", "#30343c", "#432a28", "#2c3a44"]; ground = "#11161c"
    elif mood == "dusk":
        sky_ = sky("#2a2c4c", "#e09060", "#7a5a70"); walls = ["#8a6a5a", "#7a3e34", "#9a8470", "#6a3a32", "#8a7a6a"]; ground = "#4a3e3a"
    else:  # modern evening
        sky_ = sky("#1a2a4a", "#c87a5a", "#5a4a6a"); walls = ["#9a4a36", "#b8a488", "#8a3a2e", "#a89070", "#7a3a30"]; ground = "#3a3634"
    s = sky_
    if moon_on and mood == "night" and not modern:
        s += moon(vx + 520, 170, 60)
    fz = 13.0
    if tower:
        bx0, by = P(-1.3, 1.0, fz, vx); bx1, _ = P(1.3, 1.0, fz, vx)
        tw = (bx1 - bx0)
        col = "#0e141c" if mood == "night" else "#5a4a50"
        s += f'<rect x="{bx0:.0f}" y="{by-tw*1.1:.0f}" width="{tw:.0f}" height="{tw*1.1:.0f}" fill="{col}"/>'
        for side in (0, 1):
            tx = bx0 + side * tw * 0.78
            s += f'<rect x="{tx:.0f}" y="{by-tw*1.9:.0f}" width="{tw*0.22:.0f}" height="{tw*1.9:.0f}" fill="{col}"/>'
            s += f'<path d="M{tx:.0f},{by-tw*1.9:.0f} Q{tx+tw*0.11:.0f},{by-tw*2.2:.0f} {tx+tw*0.22:.0f},{by-tw*1.9:.0f} Z" fill="{col}"/>'
            s += f'<rect x="{tx+tw*0.07:.0f}" y="{by-tw*1.7:.0f}" width="{tw*0.08:.0f}" height="{tw*0.15:.0f}" fill="{"#ffb860" if mood=="night" else "#2a2024"}" opacity="0.8"/>'
        s += f'<path d="M{bx0+tw*0.38:.0f},{by:.0f} L{bx0+tw*0.38:.0f},{by-tw*0.4:.0f} Q{bx0+tw*0.5:.0f},{by-tw*0.55:.0f} {bx0+tw*0.62:.0f},{by-tw*0.4:.0f} L{bx0+tw*0.62:.0f},{by:.0f} Z" fill="#ffc865" opacity="{0.7 if mood=="night" else 0.3}"/>'
        if mood == "night":
            s += glow(bx0 + tw / 2, by - tw * 0.2, tw * 0.9, "warm", 0.6)
    s += quad([P(-1, 1, 1, vx), P(-1, 1, fz, vx), P(1, 1, fz, vx), P(1, 1, 1, vx), (2600, 1400), (-200, 1400)], ground)
    for i in range(26):
        z = 1.0 + (fz - 1.0) * (i / 26) ** 1.6
        a, b = P(-1, 1, z, vx), P(1, 1, z, vx)
        s += f'<path d="M{a[0]:.0f},{a[1]:.0f} L{b[0]:.0f},{b[1]:.0f}" stroke="#05070a" stroke-width="{max(1, 8/z):.1f}" opacity="0.6"/>'
    for i in range(-7, 8):
        a, b = P(i / 7, 1, 1, vx), P(i / 7, 1, fz, vx)
        s += f'<path d="M{a[0]:.0f},{a[1]:.0f} L{b[0]:.0f},{b[1]:.0f}" stroke="#05070a" stroke-width="3" opacity="0.35"/>'
    a, b = P(-0.02, 1, 1, vx), P(0.02, 1, fz, vx)
    s += f'<path d="M{a[0]:.0f},{a[1]:.0f} L{b[0]:.0f},{b[1]:.0f}" stroke="{"#7a9cc4" if mood=="night" else "#c8a080"}" stroke-width="8" opacity="0.25" filter="url(#blur1)"/>'
    for side in (-1, 1):
        zs = [1.0]
        while zs[-1] < fz:
            zs.append(zs[-1] * r.uniform(1.25, 1.45))
        segs = list(zip(zs[:-1], zs[1:]))[::-1]
        for j, (z0, z1) in enumerate(segs):
            h = -r.uniform(1.4, 2.3)
            col = r.choice(walls)
            pts = [P(side, 1, z0, vx), P(side, 1, z1, vx), P(side, h, z1, vx), P(side, h, z0, vx)]
            s += quad(pts, col)
            s += quad(pts, "#000", 'filter="url(#plaster)" opacity="0.45"')
            c0, c1 = P(side, h, z0, vx), P(side, h, z1, vx); c2, c3 = P(side * 1.06, h - 0.06, z1, vx), P(side * 1.06, h - 0.06, z0, vx)
            s += quad([c0, c1, c2, c3], "#1a1a20")
            rimc = MOONRIM if mood == "night" else "#ffd8a0"
            s += f'<path d="M{c3[0]:.0f},{c3[1]:.0f} L{c2[0]:.0f},{c2[1]:.0f}" stroke="{rimc}" stroke-width="{max(1.5, 8/z0):.1f}" opacity="0.45"/>'
            a, b = P(side, 1, z0, vx), P(side, h, z0, vx)
            s += f'<path d="M{a[0]:.0f},{a[1]:.0f} L{b[0]:.0f},{b[1]:.0f}" stroke="#5e564c" stroke-width="{max(2, 60/z0):.0f}" opacity="0.7"/>'
            zm = (z0 + z1) / 2; dz = (z1 - z0)
            lit = mood == "night" and r.random() < 0.45
            s += wall_win(side, zm - dz * 0.22, zm + dz * 0.22, -1.05, -0.35, lit, vx)
            if whispers and lit and z0 < 4:
                cx, cy = P(side, -0.55, zm, vx)
                s += f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{90/zm:.0f}" ry="{130/zm:.0f}" fill="#05070a"/><circle cx="{cx:.0f}" cy="{cy-150/zm:.0f}" r="{60/zm:.0f}" fill="#05070a"/>'
            t0, t1 = P(side * 0.94, -0.42, zm - dz * 0.3, vx), P(side * 0.94, -0.42, zm + dz * 0.3, vx)
            b0, b1 = P(side * 0.94, -0.12, zm - dz * 0.3, vx), P(side * 0.94, -0.12, zm + dz * 0.3, vx)
            s += rail((t0, t1), (b0, b1), 6, hi=(MOONRIM if mood == "night" else None), w=max(0.2, 1.6 / zm))
            d0, d1 = zm - dz * 0.14, zm + dz * 0.14
            s += quad([P(side, 1, d0, vx), P(side, 1, d1, vx), P(side, 0.2, d1, vx), P(side, 0.2, d0, vx)], "#1a120c")
    if portal:
        for k in range(3):
            z0 = 1.15 + k * 0.42
            a, b = P(-0.72, 1, z0, vx), P(-0.72, -0.9, z0, vx)
            s += f'<path d="M{a[0]:.0f},{a[1]:.0f} L{b[0]:.0f},{b[1]:.0f}" stroke="#2a2a30" stroke-width="{90/z0:.0f}"/>'
            c0, c1 = P(-0.72, -0.9, z0, vx), P(-0.72, -0.9, z0 + 0.42, vx)
            s += f'<path d="M{c0[0]:.0f},{c0[1]:.0f} Q{(c0[0]+c1[0])/2:.0f},{c0[1]-150/z0:.0f} {c1[0]:.0f},{c1[1]:.0f}" stroke="#2a2a30" stroke-width="{60/z0:.0f}" fill="none"/>'
        top = P(-0.72, -1.15, 1.0, vx)
        s += quad([P(-1, -1.15, 1.0, vx), P(-1, -1.15, 2.4, vx), P(-0.72, -1.15, 2.4, vx), (top[0], top[1])], "#16161c")
        s += quad([P(-1, 1, 1.0, vx), P(-1, 1, 2.4, vx), P(-1, -1.15, 2.4, vx), P(-1, -1.15, 1.0, vx)], "#000", 'opacity="0.55"')
    lx, ly = LAMP_XY
    s += f'<path d="M{lx-70},{ly-90} L{lx-10},{ly-90}" stroke="#05070a" stroke-width="10"/>'
    s += f'<path d="M{lx-34},{ly-40} L{lx+34},{ly-40} L{lx+24},{ly+40} L{lx-24},{ly+40} Z" fill="{"#ffd98a" if lamp_on else "#223"}"/>'
    s += f'<path d="M{lx-40},{ly-40} L{lx+40},{ly-40} L{lx},{ly-90} Z" fill="#05070a"/><rect x="{lx-30}" y="{ly+40}" width="60" height="10" fill="#05070a"/>'
    if lamp_on:
        s += glow(lx, ly, 420, "warm", 0.9)
        s += f'<ellipse cx="{lx+160}" cy="1270" rx="420" ry="70" fill="#ffb860" opacity="0.12" filter="url(#blur3)"/>'
    if plaque:
        px, py = P(1, -0.15, 1.3, vx)
        s += f'<g transform="translate({px-30:.0f},{py:.0f}) skewY(-20)"><rect x="-270" y="-70" width="270" height="120" fill="#e8e0cc"/><rect x="-262" y="-62" width="254" height="104" fill="none" stroke="#2a4a8a" stroke-width="6"/>'
        s += f'<text x="-135" y="-14" font-family="Cinzel" font-size="30" fill="#1a2a5a" text-anchor="middle">{plaque[0]}</text><text x="-135" y="28" font-family="Cinzel" font-size="34" fill="#1a2a5a" text-anchor="middle">{plaque[1]}</text></g>'
    if modern:
        for zz in (1.6, 3.0, 6.0):
            x0, y0 = P(1.0, -0.6, zz, vx)
            s += f'<path d="M{x0:.0f},{y0:.0f} L{x0-120/zz:.0f},{y0:.0f} L{x0-120/zz:.0f},{y0+30/zz:.0f}" stroke="#14141a" stroke-width="{14/zz+2:.0f}" fill="none"/>'
            s += glow(x0 - 120 / zz, y0 + 50 / zz, 260 / zz + 30, "white", 0.7)
        for zz in (1.3, 2.2):
            for X in (-0.8, 0.8):
                a, b = P(X, 1, zz, vx), P(X, 0.75, zz, vx)
                s += f'<path d="M{a[0]:.0f},{a[1]:.0f} L{b[0]:.0f},{b[1]:.0f}" stroke="#2a2a2e" stroke-width="{30/zz:.0f}" stroke-linecap="round"/>'
    return s


def fog_band(y=1050, op=0.35, seed=4):
    return clouds(14, y - 80, y + 120, seed, "#b8c8d8", (op * 0.4, op), (300, 700), (40, 110))

# ===================================================================== characters
def hair_bea_front(seed=3):
    r = random.Random(seed)
    cap = ('M0,-104 C-30,-104 -62,-88 -74,-56 C-80,-30 -82,-6 -78,14 C-92,0 -100,-50 -92,-90 C-82,-140 -40,-168 0,-168 '
           'C40,-168 82,-140 92,-90 C100,-50 92,0 78,14 C82,-6 80,-30 74,-56 C62,-88 30,-104 0,-104 Z')
    s = f'<path d="{cap}" fill="#0b0706"/>'
    s += strands(r, [(-2, -104, -40, -110, -76, -40), (-2, -110, -50, -140, -90, -60), (2, -104, 40, -110, 76, -40),
                     (2, -110, 50, -140, 90, -60)], 9, "#3a2a22", (1.2, 2.4), (0.35, 0.8), 5)
    s += strands(r, [(-30, -160, -50, -150, -70, -120), (30, -160, 50, -150, 70, -120)], 4, "#8a7a8a", (1.5, 3), (0.25, 0.5), 3)
    for i in range(15):
        a = math.radians(200 + i * 10)
        s += f'<circle cx="{math.cos(a)*92:.0f}" cy="{-60+math.sin(a)*96:.0f}" r="5" fill="#f2ece0" opacity="0.9"/>'
    return s


def bea_head(look=0.0, turn=0.0, lids=0.25, smile=0.25, fear=False, sad=False, rim="#9fc2e8", eyes_closed=False):
    s = hair_carmen_back()
    s += head(look=look, smile=(-0.6 if fear else (-0.35 if sad else smile)), lids=(0.0 if fear else (0.55 if sad else lids)), rim=rim, turn=turn,
              eyes_closed=eyes_closed, sk=SK_BEA, headwrap=False, lips=("#8a3a3a", "#a84e4c"), iris="#20140c", earring=True, brow_w=0.8)
    if fear:
        s += '<ellipse cx="0" cy="74" rx="14" ry="10" fill="#2a0e0a"/>'
    if sad:
        s += '<path d="M-44,-2 C-46,20 -44,40 -46,58" stroke="#cfe0ff" stroke-width="4" fill="none" opacity="0.6"/>'
    s += hair_bea_front()
    return s


def bea_body(g, rim, dress=("#1c0a10", "#4a1424", "#6e2236")):
    sk = SK_BEA
    s = (f'<defs>{grad_lin(g+"d", [(0, dress[0], 1), (0.55, dress[1], 1), (0.85, dress[2], 1), (1, dress[1], 1)], -340, 0, 340, 0)}'
         f'{grad_lin(g+"s", [(0, sk["deep"], 1), (0.4, sk["shadow"], 1), (0.75, sk["base"], 1), (1, sk["shadow"], 1)], -220, 0, 220, 0)}</defs>')
    s += f'<path d="M-44,40 C-44,100 -58,150 -150,186 L150,186 C58,150 44,100 44,40 Z" fill="url(#{g}s)"/>'
    s += f'<path d="M-44,60 C-30,108 30,108 44,60 L44,40 L-44,40 Z" fill="{sk["deep"]}" opacity="0.5" filter="url(#blur1)"/>'
    for i in range(23):
        t = i / 22; px = -80 + 160 * t; py = 150 + 46 * math.sin(math.pi * t)
        s += f'<circle cx="{px:.0f}" cy="{py:.0f}" r="6" fill="#f4eee2"/><circle cx="{px-2:.0f}" cy="{py-2:.0f}" r="2" fill="#fff"/>'
    s += '<path d="M0,200 L0,236 M-12,212 L12,212" stroke="#e0bb5a" stroke-width="6" stroke-linecap="round"/>'
    s += f'<path d="M-250,226 C-170,236 -140,250 -130,262 L130,262 C140,250 170,236 250,226 C320,270 350,400 360,660 L-360,660 C-350,400 -320,270 -250,226 Z" fill="url(#{g}d)"/>'
    s += '<path d="M-150,262 L150,262 M-150,262 L-170,660 M150,262 L170,660" stroke="#c9a24a" stroke-width="7" fill="none" opacity="0.85"/>'
    for i in range(9):
        s += f'<circle cx="{-120+i*30}" cy="262" r="5" fill="#f4eee2"/>'
    for side in (-1, 1):
        s += f'<path d="M{side*250},226 C{side*330},240 {side*370},330 {side*360},420 C{side*320},400 {side*280},380 {side*240},400 C{side*250},340 {side*240},280 {side*250},226 Z" fill="{dress[2]}" opacity="0.9"/>'
        for k in range(4):
            s += f'<path d="M{side*(262+k*24)},{236+k*6} C{side*(290+k*20)},300 {side*(290+k*16)},360 {side*(270+k*20)},400" stroke="#14060a" stroke-width="4" fill="none" opacity="0.5"/>'
    for d in ["M-200,330 Q-210,480 -190,660", "M200,330 Q210,480 190,660", "M-60,300 Q-50,480 -70,660", "M60,300 Q50,480 70,660"]:
        s += f'<path d="{d}" stroke="#0a0206" stroke-width="10" fill="none" opacity="0.55" filter="url(#blur1)"/>'
    if rim:
        s += f'<path d="M-250,226 C-330,270 -370,420 -380,660" stroke="{rim}" stroke-width="5" fill="none" opacity="0.5" filter="url(#blur1)"/>'
    return s


def bea_bust(x, y, k=1.0, rim="#9fc2e8", dress=("#1c0a10", "#4a1424", "#6e2236"), **hk):
    g = uid("bb")
    return bust_frame(bea_body(g, rim, dress), bea_head(rim=rim, **hk), x, y, k)


def veil(lift=0.0, op=0.92, black=False):
    """Veil over Beatriz's head (head coords). Covers the face below the eyes; lift>0 raises the lower edge."""
    c1, c2, c3 = ("#0a0a10", "#1c1c26", "#3a3a4a") if black else ("#e8eef6", "#c8d2e0", "#ffffff")
    g = uid("v")
    s = f'<defs>{grad_lin(g, [(0, c2, 1), (0.5, c1, 1), (1, c2, 1)], -200, 0, 200, 0)}</defs>'
    s += (f'<path d="M-118,-40 C-130,-150 -70,-206 0,-208 C70,-206 130,-150 118,-40 C130,60 170,180 230,300 L-230,300 C-170,180 -130,60 -118,-40 Z" '
          f'fill="url(#{g})" opacity="{op*0.55:.2f}"/>')
    ly = 8 - lift * 160
    s += (f'<path d="M-84,{ly} C-40,{ly+14} 40,{ly+14} 84,{ly} C96,60 120,160 160,300 L-160,300 C-120,160 -96,60 -84,{ly} Z" fill="url(#{g})" opacity="{op}"/>')
    for i in range(9):
        x = -150 + i * 38
        s += f'<path d="M{x*0.5:.0f},{ly+20:.0f} C{x*0.7:.0f},120 {x*0.9:.0f},200 {x:.0f},300" stroke="{"#000" if black else "#8a96aa"}" stroke-width="5" fill="none" opacity="0.35"/>'
    for i in range(7):
        a = -150 + i * 50
        s += f'<path d="M{a*0.4:.0f},-200 C{a*0.8:.0f},-120 {a:.0f},0 {a*1.2:.0f},120" stroke="{"#000" if black else "#8a96aa"}" stroke-width="4" fill="none" opacity="0.3"/>'
    s += f'<path d="M-84,{ly} C-40,{ly+14} 40,{ly+14} 84,{ly}" stroke="{c3}" stroke-width="5" stroke-dasharray="6 6" fill="none" opacity="0.7"/>'
    return s


def veiled_bust(x, y, k=1.0, rim="#9fc2e8", black=False, full_cover=False, lift=0.0, look=0.0, lids=0.35, glow_eyes=False):
    g = uid("vb")
    body = bea_body(g, rim, ("#0a0a0e", "#1a1a22", "#2a2a36") if black else ("#1c0a10", "#3a1420", "#5a2030"))
    hd = bea_head(rim=rim, look=look, lids=lids, smile=0.0)
    hd += veil(black=black, lift=lift, op=0.96)
    if full_cover:
        hd += f'<path d="M-104,-140 C-60,-190 60,-190 104,-140 L100,30 C40,40 -40,40 -100,30 Z" fill="{"#14141c" if black else "#dfe6ef"}" opacity="0.9"/>'
    if glow_eyes:
        hd += ''.join(f'<circle cx="{x_}" cy="-19" r="30" fill="url(#whiteglow)"/><circle cx="{x_}" cy="-19" r="7" fill="#ffffff"/>' for x_ in (-31, 31))
    return f'<g transform="translate({x},{y}) scale({k})"><g transform="translate(0,18) scale(0.74,0.86)">{body}</g>{hd}</g>'


def hair_martin(seed=6):
    r = random.Random(seed)
    s = ('<path d="M-84,-20 C-98,-90 -70,-160 -6,-168 C56,-172 98,-130 90,-40 C86,-74 70,-98 40,-110 C10,-100 -30,-104 -60,-92 C-72,-70 -78,-46 -84,-20 Z" fill="#0c0806"/>')
    s += '<path d="M-84,-20 C-88,8 -84,34 -76,56 L-68,20 C-70,0 -72,-14 -74,-30 Z M90,-30 C90,0 86,30 78,54 L70,18 C72,0 74,-12 76,-36 Z" fill="#0c0806"/>'
    s += strands(r, [(-60, -150, -20, -168, 40, -150), (-40, -130, 0, -150, 60, -120)], 8, "#3a2a20", (1.5, 3), (0.3, 0.6), 8)
    s += ('<g transform="translate(0,12) scale(0.8,0.9)"><path d="M-4,58 C-20,54 -40,52 -60,42 C-70,36 -74,26 -68,20 C-62,36 -40,40 -6,44 Z M4,58 C20,54 40,52 60,42 C70,36 74,26 68,20 C62,36 40,40 6,44 Z" fill="#0c0806"/></g>')
    s += '<path d="M-22,96 C-18,110 -8,140 0,156 C8,140 18,110 22,96 C10,102 -10,102 -22,96 Z" fill="#0c0806"/>'
    s += strands(r, [(-10, 100, -4, 128, 0, 150), (10, 100, 4, 128, 0, 150)], 5, "#3a2a20", (1, 2), (0.3, 0.6), 3)
    return s


def plumed_hat(rim="#9fc2e8", plume="#0a0a0e"):
    s = '<path d="M-170,-120 C-120,-150 130,-150 180,-118 C150,-96 -140,-96 -170,-120 Z" fill="#08080a"/>'
    s += '<path d="M-96,-128 C-100,-200 -60,-238 10,-240 C76,-238 104,-200 100,-128 Z" fill="#0c0c10"/>'
    s += '<path d="M-96,-140 C-30,-150 40,-150 100,-140 L100,-124 C40,-134 -30,-134 -96,-124 Z" fill="#6a1a1a"/>'
    for i in range(16):
        t = i / 15
        s += f'<path d="M60,-200 C{120+t*60:.0f},{-260-t*30:.0f} {200+t*30:.0f},{-230+t*40:.0f} {240-t*10:.0f},{-150+t*70:.0f}" stroke="{plume}" stroke-width="{14-t*6:.0f}" fill="none" stroke-linecap="round"/>'
    s += f'<path d="M60,-200 C150,-280 230,-240 240,-150" stroke="{rim}" stroke-width="3" fill="none" opacity="0.5"/>'
    s += f'<path d="M-170,-120 C-120,-150 130,-150 180,-118" stroke="{rim}" stroke-width="4" fill="none" opacity="0.6"/>'
    return s


def martin_head(look=0.0, turn=0.0, lids=0.35, smile=0.25, rim="#9fc2e8", cold=False, hat=True):
    s = head(look=look, smile=(-0.3 if cold else smile), lids=(0.5 if cold else lids), rim=rim, turn=turn, sk=SK_MAR, headwrap=False,
             earring=False, lips=("#7a4038", "#8a5048"), iris="#140c08", brow_w=1.2, neck=True)
    if cold:
        s += angry_brows("#0c0806", 9)
    s += hair_martin()
    if hat:
        s += plumed_hat(rim)
    return s


def martin_body(g, rim, doublet=("#060608", "#16161c", "#2a2a34")):
    s = (f'<defs>{grad_lin(g+"c", [(0, doublet[0], 1), (0.6, doublet[1], 1), (1, doublet[2], 1)], -380, 0, 380, 0)}</defs>')
    s += f'<path d="M-52,40 C-54,110 -62,150 -72,190 L72,190 C62,150 54,110 52,40 Z" fill="{SK_MAR["shadow"]}"/>'
    s += f'<path d="M-90,170 C-220,200 -340,260 -380,660 L380,660 C340,260 220,200 90,170 Z" fill="url(#{g}c)"/>'
    s += '<path d="M-150,230 L150,230 L130,660 L-130,660 Z" fill="#1a1a22"/>'
    for i in range(7):
        s += f'<path d="M{-120+i*40},250 L{-110+i*36},660" stroke="#5a1a1a" stroke-width="8" opacity="0.7"/>'
    for b in range(7):
        s += f'<circle cx="0" cy="{280+b*50}" r="8" fill="#c9a24a"/>'
    for i in range(14):
        a = math.pi * i / 13
        s += f'<ellipse cx="{math.cos(a)*-95:.0f}" cy="{185+math.sin(a)*22:.0f}" rx="22" ry="26" fill="#ece6d8" stroke="#a8a090" stroke-width="2"/>'
    s += '<path d="M-180,240 L200,600" stroke="#3a2414" stroke-width="26"/><path d="M-180,240 L200,600" stroke="#c9a24a" stroke-width="3" opacity="0.6"/>'
    if rim:
        s += f'<path d="M-90,170 C-220,200 -340,260 -380,660" stroke="{rim}" stroke-width="6" fill="none" opacity="0.55" filter="url(#blur1)"/>'
    return s


def martin_bust(x, y, k=1.0, rim="#9fc2e8", **hk):
    g = uid("mb")
    return bust_frame(martin_body(g, rim), martin_head(rim=rim, **hk), x, y, k)


def rapier(x, y, ang, k=1.0, shine=True):
    gid = uid("rb")
    s = lg(gid, [(0, "#f4f8ff", 1), (0.5, "#8a94a4", 1), (1, "#5a6474", 1)])
    s += f'<path d="M0,-9 L1200,-3 L1240,0 L1200,3 L0,9 Z" fill="url(#{gid})"/>'
    if shine:
        s += '<path d="M10,-4 L1180,-1" stroke="#ffffff" stroke-width="3" opacity="0.7"/>'
    s += '<path d="M-10,-120 L-10,120" stroke="#b08a3a" stroke-width="16" stroke-linecap="round"/>'
    s += '<path d="M-10,-60 C40,-90 70,-40 40,0 C70,40 40,90 -10,60" stroke="#b08a3a" stroke-width="10" fill="none"/>'
    s += '<path d="M-10,0 C-60,-70 -150,-70 -180,-20" stroke="#b08a3a" stroke-width="10" fill="none"/>'
    s += '<rect x="-200" y="-18" width="190" height="36" rx="12" fill="#2a1a10"/>'
    for i in range(9):
        s += f'<path d="M{-190+i*20},-16 L{-180+i*20},16" stroke="#8a6a3a" stroke-width="5"/>'
    s += '<circle cx="-215" cy="0" r="30" fill="#c9a24a"/><circle cx="-222" cy="-8" r="10" fill="#f0d890" opacity="0.7"/>'
    return f'<g transform="translate({x},{y}) rotate({ang}) scale({k})">{s}</g>'


def guitar(x, y, ang, k=1.0, broken=False, col="#6a3a1a"):
    s = f'<path d="M0,-80 C60,-90 90,-50 80,-10 C100,10 120,60 90,100 C60,140 -60,140 -90,100 C-120,60 -100,10 -80,-10 C-90,-50 -60,-90 0,-80 Z" fill="{col}"/>'
    s += '<circle cx="0" cy="20" r="26" fill="#140a04"/>'
    s += '<rect x="-14" y="-400" width="28" height="330" fill="#3a2010"/><rect x="-22" y="-470" width="44" height="80" rx="6" fill="#2a160a"/>'
    if broken:
        s += '<path d="M-40,-60 L-10,0 L-50,40 L0,70 L-20,110" stroke="#0a0604" stroke-width="10" fill="none"/>'
        s += '<path d="M-14,-300 L14,-290 L-6,-270" stroke="#0a0604" stroke-width="12" fill="none"/>'
        s += '<path d="M-10,-400 C-80,-300 60,-200 -30,-100 M6,-400 C90,-320 -40,-200 40,-80" stroke="#c8c0b0" stroke-width="2" fill="none" opacity="0.8"/>'
    else:
        for i in range(4):
            s += f'<path d="M{-9+i*6},-450 L{-9+i*6},60" stroke="#e8e0cc" stroke-width="1.5" opacity="0.8"/>'
    return f'<g transform="translate({x},{y}) rotate({ang}) scale({k})">{s}</g>'


def veiled_full(rim=MOONRIM, black=False, fill=None, ghost=False):
    fill = fill or ("#06060a" if black else "#0c0a12")
    s = woman_full(rebozo_head=False, rim=rim, fill=fill)
    vcol = "#e4eaf4" if not black else "#16161e"
    s += (f'<path d="M-62,-900 C-70,-950 -36,-972 0,-972 C36,-972 70,-950 62,-900 C80,-820 120,-700 160,-560 C100,-540 -100,-540 -160,-560 C-120,-700 -80,-820 -62,-900 Z" '
          f'fill="{vcol}" opacity="{0.9 if not ghost else 0.7}"/>')
    for i in range(6):
        x = -120 + i * 48
        s += f'<path d="M{x*0.3:.0f},-940 C{x*0.6:.0f},-820 {x*0.9:.0f},-680 {x:.0f},-560" stroke="{"#7a8aa0" if not black else "#000"}" stroke-width="4" fill="none" opacity="0.45"/>'
    return s


def man_sword(rim=MOONRIM, fill=SIL, lunge=False):
    s = man_full(hat=True, cape=True, rim=rim, fill=fill, walk=(0.6 if lunge else 0.2))
    s += f'<path d="M60,-1000 C120,-1060 180,-1040 200,-970" stroke="{fill}" stroke-width="14" fill="none" stroke-linecap="round"/>'
    s += f'<path d="M80,-760 C160,-720 240,-700 320,-700 L320,-670 C230,-660 150,-680 70,-700 Z" fill="{fill}"/>'
    s += rapier(330, -686, -8 if lunge else -20, 0.6)
    return s


# ===================================================================== backgrounds
@art
def street_night(): return S(persp_street("night"), fog_band(1180, 0.3))
@art
def street_run(): return S(persp_street("night", seed=5), fog_band(1200, 0.3, 6))
@art
def street_portal(): return S(persp_street("night", seed=7, portal=True), fog_band(1180, 0.25, 8))
@art
def street_whispers(): return S(persp_street("night", seed=9, whispers=True), fog_band(1180, 0.25, 10))
@art
def street_day(): return S(persp_street("dusk", seed=11, lamp_on=False))
@art
def street_today(): return S(persp_street("modern", seed=13, lamp_on=False, modern=True, plaque=("CALLE DE", "JESÚS MARÍA")))
@art
def title_bg():
    return S(persp_street("night", seed=3), fog_band(1150, 0.45, 12), fog_band(1300, 0.4, 13),
             '<rect width="2400" height="1350" fill="#06101c" opacity="0.35"/>')
@art
def street_sign():
    s = sky("#040912", "#16263a") + stars(60, 3, 300)
    s += '<rect x="0" y="0" width="1500" height="1350" fill="#3a2a2c"/><rect x="0" y="0" width="1500" height="1350" fill="#000" filter="url(#plaster)" opacity="0.5"/>'
    s += '<rect x="1500" y="0" width="900" height="1350" fill="#1e2028"/><rect x="1500" y="0" width="900" height="1350" fill="#000" filter="url(#plaster)" opacity="0.5"/>'
    s += '<rect x="1450" y="0" width="100" height="1350" fill="#6a6052"/><path d="M1450,0 L1450,1350" stroke="#a89880" stroke-width="6" opacity="0.6"/>'
    for y in range(80, 1350, 120):
        s += f'<path d="M1450,{y} L1550,{y}" stroke="#3a342c" stroke-width="4"/>'
    s += glow(560, 380, 700, "warm", 0.9)
    s += '<rect x="640" y="560" width="760" height="300" rx="10" fill="#e8e0cc"/><rect x="660" y="580" width="720" height="260" fill="none" stroke="#2a4a8a" stroke-width="10"/>'
    s += '<text x="1020" y="690" font-family="Cinzel" font-size="56" fill="#1a2a5a" text-anchor="middle">CALLE DE LA</text>'
    s += '<text x="1020" y="800" font-family="Cinzel" font-size="96" fill="#1a2a5a" text-anchor="middle">QUEMADA</text>'
    s += '<rect x="640" y="560" width="760" height="300" fill="#000" filter="url(#grain)" opacity="0.25"/>'
    s += '<path d="M300,320 L460,320" stroke="#05070a" stroke-width="12"/>'
    s += '<path d="M420,330 L500,330 L486,440 L434,440 Z" fill="#ffd98a"/><path d="M412,330 L508,330 L460,270 Z" fill="#05070a"/>'
    s += '<rect x="0" y="1200" width="2400" height="150" fill="#11161c"/>' + clouds(10, 1150, 1350, 4, "#b8c8d8", (0.1, 0.25))
    return S(s)


@art
def aguacate():
    s = sky("#040912", "#14243a") + stars(140, 21, 500) + moon(1800, 200, 55)
    s += '<path d="M0,0 L760,180 L760,1100 L0,1350 Z" fill="#5a3a2c"/><path d="M0,0 L760,180 L760,1100 L0,1350 Z" fill="#000" filter="url(#plaster)" opacity="0.55"/>'
    s += '<path d="M2400,0 L1640,180 L1640,1100 L2400,1350 Z" fill="#3a3a48"/><path d="M2400,0 L1640,180 L1640,1100 L2400,1350 Z" fill="#000" filter="url(#plaster)" opacity="0.55"/>'
    s += '<path d="M760,1100 L1640,1100 L2400,1350 L0,1350 Z" fill="#16141a"/>'
    for i in range(12):
        y = 1100 + i * 22
        s += f'<path d="M{760-i*64},{y} L{1640+i*64},{y}" stroke="#05070a" stroke-width="3" opacity="0.5"/>'
    s += '<rect x="760" y="560" width="880" height="540" fill="#0a0e16"/>'
    s += '<path d="M1080,1100 C1100,900 1060,760 1120,620 C1150,560 1200,540 1240,560 C1220,640 1260,780 1250,1100 Z" fill="#0a0806"/>'
    s += '<path d="M1120,640 C1000,560 900,560 820,500 M1220,600 C1320,520 1460,520 1560,460" stroke="#0a0806" stroke-width="40" fill="none"/>'
    r = random.Random(5)
    for i in range(70):
        x, y = r.uniform(640, 1760), r.uniform(220, 640)
        s += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r.uniform(60,140):.0f}" ry="{r.uniform(30,70):.0f}" fill="{r.choice(["#06100a", "#0a160e", "#0c1a12"])}" transform="rotate({r.uniform(-30,30):.0f} {x:.0f} {y:.0f})"/>'
    for i in range(40):
        x, y = r.uniform(700, 1700), r.uniform(240, 600)
        s += f'<path d="M{x:.0f},{y:.0f} q30,-20 60,-4" stroke="#7a9cc4" stroke-width="3" fill="none" opacity="0.35"/>'
    for i in range(10):
        x, y = r.uniform(800, 1600), r.uniform(420, 640)
        s += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="14" ry="22" fill="#1a2a12"/><path d="M{x-6:.0f},{y-10:.0f} q-2,10 2,18" stroke="#7a9cc4" stroke-width="2" fill="none" opacity="0.5"/>'
    s += lamp(1900, 1250, 520, True)
    s += place(man_full(hat=True, cape=True, rim=MOONRIM, fill="#020305"), 1180, 1110, 0.28)
    s += clouds(10, 1000, 1300, 9, "#b8c8d8", (0.08, 0.2))
    return S(s)


def plaza_svg(night=False):
    if night:
        s = sky("#040912", "#16263a") + stars(140, 4, 500)
    else:
        s = sky("#26304e", "#e8a070", "#8a6a7a") + glow(1700, 700, 900, "warm", 0.5)
    s += f'<path d="M1300,760 L1640,520 L1700,540 L1760,520 L2100,760 Z" fill="{"#0e1420" if night else "#6a6a8a"}"/>'
    s += '<path d="M1600,550 L1640,520 L1700,540 L1760,520 L1800,560 L1740,580 L1660,575 Z" fill="#e8eef6" opacity="0.8"/>'
    s += f'<path d="M1900,760 L2200,600 L2400,680 L2400,760 Z" fill="{"#0c121c" if night else "#5a5a7a"}"/>'
    c = "#0e141c" if night else "#7a5a50"
    s += f'<rect x="300" y="520" width="700" height="420" fill="{c}"/><path d="M300,520 L650,400 L1000,520 Z" fill="{c}"/>'
    s += f'<rect x="600" y="300" width="100" height="240" fill="{c}"/><path d="M590,300 L650,250 L710,300 Z" fill="{c}"/>'
    s += f'<path d="M610,270 L690,270 M650,236 L650,290" stroke="{"#c9a24a" if not night else "#8a7a5a"}" stroke-width="8"/>'
    for i in range(8):
        x = 1000 + i * 40
        s += f'<path d="M{x},940 L{x},{500+i*10}" stroke="#3a2a1a" stroke-width="6"/>'
    for j in range(6):
        s += f'<path d="M1000,{560+j*70} L1300,{560+j*70}" stroke="#3a2a1a" stroke-width="5"/>'
    s += '<rect x="1020" y="700" width="260" height="240" fill="%s"/>' % ("#141a22" if night else "#9a7a62")
    p = "#121820" if night else "#8a5a46"
    s += f'<rect x="1500" y="640" width="900" height="300" fill="{p}"/>'
    for i in range(9):
        s += window(1540 + i * 96, 700, 50, 80, lit=night and i % 3 != 1, arch=True)
    s += f'<rect x="0" y="940" width="2400" height="410" fill="{"#11161c" if night else "#6a5a50"}"/>'
    s += water(1150, 1350, "#1b2e3d" if night else "#5a7a8a", "#070c14" if night else "#2a3a4a")
    s += '<path d="M500,1220 C600,1250 900,1250 1000,1220 L980,1240 C900,1265 600,1265 520,1240 Z" fill="#1a100a"/>'
    s += place(man_full(hat=True, cape=False, rim="#ffd8a0", fill="#0a0806"), 760, 1225, 0.22)
    s += '<path d="M800,1000 L850,1240" stroke="#0a0806" stroke-width="6"/>'
    for i, x in enumerate((1300, 1420, 1700, 1880, 2050, 250, 120)):
        f = woman_full(rebozo_head=True, rim="#ffd8a0", fill="#0a0806") if i % 2 else man_full(hat=True, cape=False, rim="#ffd8a0", fill="#0a0806")
        s += place(f, x, 1120, 0.18)
    return s

@art
def plaza_1550(): return S(plaza_svg(False))


def palacio_svg(night=False):
    s = (sky("#040912", "#16263a") + stars(100, 6, 400)) if night else sky("#2a3050", "#d89070", "#7a5a70")
    c = "#2a2a34" if night else "#8a4a38"
    s += f'<rect x="0" y="300" width="2400" height="860" fill="{c}"/><rect x="0" y="300" width="2400" height="860" fill="#000" filter="url(#plaster)" opacity="0.45"/>'
    s += '<rect x="0" y="280" width="2400" height="40" fill="#1a1418"/>'
    for i in range(12):
        s += f'<rect x="{i*210+40}" y="230" width="90" height="60" fill="#1a1418"/>'
    for row, y in enumerate((420, 760)):
        for i in range(11):
            x = 90 + i * 210
            if 1000 < x < 1350 and row == 1: continue
            s += window(x, y, 80, 160, lit=night and (i + row) % 3 == 0, arch=True)
            s += rail(((x - 20, y + 120), (x + 100, y + 120)), ((x - 20, y + 180), (x + 100, y + 180)), 5, hi=(MOONRIM if night else None), w=0.6)
    s += '<path d="M1060,1160 L1060,820 Q1200,700 1340,820 L1340,1160 Z" fill="#6a5a50"/><path d="M1090,1160 L1090,840 Q1200,740 1310,840 L1310,1160 Z" fill="#140a06"/>'
    s += '<path d="M1180,560 L1220,560 L1220,640 L1180,640 Z" fill="#c9a24a" opacity="0.7"/>'
    s += f'<rect x="0" y="1160" width="2400" height="190" fill="{"#11161c" if night else "#5a4a44"}"/>' + cobbles(1170, 1350)
    if night:
        for x in (700, 1700):
            s += lamp(x, 1250, 420, True)
        s += place(man_full(hat=True, cape=True, rim=MOONRIM, fill="#020305", lantern=True), 1500, 1260, 0.3)
        s += place(man_full(hat=True, cape=True, rim=MOONRIM, fill="#020305"), 1580, 1260, 0.3)
    else:
        for i, x in enumerate((300, 520, 1700, 1950, 2150)):
            f = woman_full(rebozo_head=True, rim="#ffd8a0", fill="#0a0806") if i % 2 else man_full(hat=True, cape=True, rim="#ffd8a0", fill="#0a0806")
            s += place(f, x, 1300, 0.28)
    return s

@art
def palacio(): return S(palacio_svg(False))
@art
def palacio_night(): return S(palacio_svg(True), fog_band(1250, 0.25))


@art
def casona():
    s = sky("#060c18", "#1c3048") + stars(80, 6, 300) + moon(1980, 140, 50)
    s += '<rect x="250" y="160" width="1900" height="1100" fill="#4a2a28"/><rect x="250" y="160" width="1900" height="1100" fill="#000" filter="url(#plaster)" opacity="0.5"/>'
    s += f'<rect x="220" y="130" width="1960" height="50" fill="#5e564c"/><path d="M220,130 L2180,130" stroke="{MOONRIM}" stroke-width="4" opacity="0.5"/>'
    for x in (250, 2090):
        s += f'<rect x="{x}" y="160" width="60" height="1100" fill="#6a6052"/>'
    for x in (480, 1640):
        s += f'<rect x="{x-20}" y="290" width="300" height="400" fill="#7a6e5e"/><rect x="{x}" y="310" width="260" height="360" fill="#0a0e14"/>'
        s += window(x + 40, 330, 180, 320, lit=(x == 1640), arch=True)
        s += rail(((x - 50, 600), (x + 310, 600)), ((x - 50, 700), (x + 310, 700)), 9, hi=MOONRIM) + f'<rect x="{x-70}" y="700" width="400" height="22" fill="#2a2420"/>'
    s += '<path d="M940,1260 L940,820 Q1200,680 1460,820 L1460,1260 Z" fill="#7a6e5e"/><path d="M980,1260 L980,840 Q1200,720 1420,840 L1420,1260 Z" fill="#2a1a0e"/>'
    for i in range(5):
        for j in range(8):
            s += f'<circle cx="{1020+i*90}" cy="{880+j*45}" r="7" fill="#8a7a5a"/>'
    s += '<path d="M1200,760 L1200,1260" stroke="#120a06" stroke-width="10"/>'
    s += '<rect x="1110" y="560" width="180" height="140" fill="#7a6e5e"/><text x="1200" y="650" font-family="Cinzel" font-size="40" fill="#2a2018" text-anchor="middle">E · G</text>'
    lx, ly = LAMP_XY
    s += f'<path d="M{lx-70},{ly-90} L{lx-10},{ly-90}" stroke="#05070a" stroke-width="10"/><path d="M{lx-34},{ly-40} L{lx+34},{ly-40} L{lx+24},{ly+40} L{lx-24},{ly+40} Z" fill="#ffd98a"/>'
    s += f'<path d="M{lx-40},{ly-40} L{lx+40},{ly-40} L{lx},{ly-90} Z" fill="#05070a"/>' + glow(lx, ly, 420, "warm", 0.9)
    s += '<rect x="0" y="1260" width="2400" height="90" fill="#11161c"/>' + cobbles(1260, 1350)
    return S(s)


def balcony_svg(with_bea=False):
    s = sky("#050a14", "#1a2a40") + stars(50, 12, 200)
    s += '<rect x="0" y="0" width="2400" height="1350" fill="#3e2828"/><rect width="2400" height="1350" fill="#000" filter="url(#plaster)" opacity="0.55"/>'
    s += '<path d="M0,0 L2400,0 L2400,90 L0,140 Z" fill="#0a1424"/>' + glow(1200, 0, 700, "moon", 0.6)
    s += '<path d="M820,820 L820,200 Q1100,100 1380,200 L1380,820 Z" fill="#ffc865"/>' + glow(1100, 500, 600, "warm", 0.6)
    s += '<path d="M840,820 C880,620 850,360 900,210 L1060,160 C980,360 1040,620 1000,820 Z" fill="#e8d0a0" opacity="0.45"/>'
    if with_bea:
        s += bea_bust(1120, 470, 0.95, rim=WARM, look=0.5, lids=0.3, smile=0.3)
    s += '<path d="M820,820 L820,200 Q1100,100 1380,200 L1380,820" stroke="#6a6052" stroke-width="34" fill="none"/>'
    s += '<path d="M700,820 L1500,820 L1560,880 L640,880 Z" fill="#3a3530"/>'
    s += rail(((660, 620), (1540, 620)), ((660, 860), (1540, 860)), 12, hi=MOONRIM, w=1.4)
    s += flowerpot(760, 610, 2.2, 5, "night") + flowerpot(1460, 610, 2.0, 6, "night")
    s += '<rect x="0" y="1180" width="2400" height="170" fill="#11161c"/>' + cobbles(1190, 1350)
    return s

@art
def balcony_night(): return S(balcony_svg(False))
@art
def beatriz_balcony(): return S(balcony_svg(True))


@art
def watcher_close():
    s = f'<g transform="translate(1200,700) scale(1.8) translate(-1200,-700)">{persp_street("night", seed=7, portal=True)}</g>'
    s += '<rect width="2400" height="1350" fill="#02040a" opacity="0.45"/>'
    fig = man_full(hat=True, cape=True, rim=MOONRIM, fill="#020305")
    fig += '<path d="M60,-1000 C120,-1060 180,-1040 200,-970" stroke="#020305" stroke-width="14" fill="none" stroke-linecap="round"/>'
    s += place(fig, 980, 1400, 1.2)
    s += '<circle cx="1000" cy="345" r="6" fill="#ffd98a" opacity="0.9"/><circle cx="1040" cy="345" r="6" fill="#ffd98a" opacity="0.9"/>'
    return S(s, fog_band(1250, 0.3))


def ballroom_svg(couple=False):
    s = '<rect width="2400" height="1350" fill="#140c08"/>'
    s += lg("bw", [(0, "#3a2414", 1), (1, "#120a06", 1)]) + '<rect width="2400" height="900" fill="url(#bw)"/>'
    s += '<rect width="2400" height="900" fill="#000" filter="url(#plaster)" opacity="0.4"/>'
    for i in range(6):
        x = 120 + i * 400
        s += f'<path d="M{x},820 L{x},300 Q{x+90},200 {x+180},300 L{x+180},820 Z" fill="#0c1424"/>' + glow(x + 90, 400, 160, "moon", 0.4)
        s += f'<rect x="{x+220}" y="260" width="120" height="420" fill="#5a1a1a"/><rect x="{x+230}" y="270" width="100" height="400" fill="none" stroke="#c9a24a" stroke-width="4"/>'
    s += '<path d="M0,900 L2400,900 L2400,1350 L0,1350 Z" fill="#2a1a10"/>'
    for i in range(16):
        s += f'<path d="M{i*200-400},1350 L{1200+(i*200-1600)*0.3:.0f},900" stroke="#140a04" stroke-width="5" opacity="0.6"/>'
    for j in range(5):
        s += f'<path d="M0,{920+j*90} L2400,{920+j*90}" stroke="#140a04" stroke-width="4" opacity="0.5"/>'
    for cx in (600, 1200, 1800):
        s += f'<path d="M{cx},0 L{cx},160" stroke="#2a1a0a" stroke-width="6"/><ellipse cx="{cx}" cy="190" rx="170" ry="30" fill="none" stroke="#c9a24a" stroke-width="10"/>'
        s += glow(cx, 160, 380, "warm", 0.8)
        for k in range(9):
            x = cx - 160 + k * 40
            s += f'<rect x="{x-5}" y="140" width="10" height="40" fill="#efe4c8"/>' + f'<path d="M{x},118 q7,10 0,20 q-7,-10 0,-20 Z" fill="#fff0b0"/>'
    r = random.Random(3)
    for i in range(9):
        x = 200 + i * 250 + r.uniform(-40, 40); y = 1040 + (i % 2) * 70; k = 0.32 + (i % 2) * 0.04
        if couple and 850 < x < 1550: continue
        s += place(woman_full(rim="#ffb860", fill="#0a0604"), x, y, k) + place(man_full(hat=False, cape=True, rim="#ffb860", fill="#0a0604"), x + 90 * k / 0.32, y, k * 1.05, flip=True)
    if couple:
        s += glow(1200, 760, 500, "warm", 0.5)
        s += place(woman_full(rim="#ffd8a0", fill="#1a0610"), 1100, 1260, 0.62)
        s += place(man_full(hat=True, cape=True, rim="#ffd8a0", fill="#060406"), 1300, 1260, 0.66, flip=True)
    s += clouds(8, 200, 700, 5, "#ffd8a0", (0.03, 0.08), (200, 400), (60, 140))
    return s

@art
def ballroom(): return S(ballroom_svg(False))
@art
def ballroom_couple(): return S(ballroom_svg(True))


@art
def martin_portrait(): return S(portrait_bg("candle"), martin_bust(1200, 620, 1.65, rim=WARM, look=-0.2, lids=0.35, smile=0.35), candle_at(2050, 1300, 160))
@art
def martin_jealous(): return S(portrait_bg("moon"), martin_bust(1200, 620, 1.65, rim=MOONRIM, look=0.6, cold=True), '<rect width="2400" height="1350" fill="#04081a" opacity="0.25"/>')
@art
def martin_red(): return S(portrait_bg("red"), martin_bust(1200, 620, 1.65, rim="#ff6040", look=0.0, cold=True), '<rect width="2400" height="1350" fill="#2a0004" opacity="0.2"/>')
@art
def gonzalo_portrait(): return S(portrait_bg("candle"), father_bust(1200, 560, 1.75, rim="#ffb860"), candle_at(400, 1300, 180))
@art
def beatriz_portrait(): return S(portrait_bg("moon"), bea_bust(1200, 560, 1.75, rim=MOONRIM, look=0.15, lids=0.3, smile=0.2))
@art
def beatriz_soft(): return S(portrait_bg("candle"), bea_bust(1200, 560, 1.75, rim=WARM, look=-0.2, lids=0.35, smile=0.55))
@art
def beatriz_sad(): return S(portrait_bg("moon"), bea_bust(1200, 560, 1.75, rim=MOONRIM, look=0.3, sad=True), '<rect width="2400" height="1350" fill="#04081a" opacity="0.2"/>')
@art
def beatriz_fear(): return S(portrait_bg("candle"), bea_bust(1200, 560, 1.75, rim="#ffb860", look=-0.5, turn=-0.15, fear=True))


@art
def veiled_eyes(): return S(portrait_bg("ghost"), veiled_bust(1200, 560, 1.75, rim=MOONRIM, look=0.0, lids=0.2))
@art
def veil_black(): return S(portrait_bg("moon"), veiled_bust(1200, 560, 1.75, rim=MOONRIM, black=True, look=0.25, lids=0.4))
@art
def veil_hand():
    s = portrait_bg("ghost") + veiled_bust(1000, 560, 1.6, rim=MOONRIM, full_cover=True)
    s += '<g transform="translate(2400,0) scale(-1,1)">' + sleeve(620, 640, 1.8, -16, "#14141c", lace=True) + hand(620, 640, 1.8, -16, SK_MAR) + '</g>'
    return S(s)
@art
def veil_flash():
    s = '<rect width="2400" height="1350" fill="#e8eef6"/>' + glow(1200, 500, 1200, "white", 0.9)
    s += '<g transform="translate(1200,620) scale(1.9)">' + '<path d="M-260,700 C-250,300 -200,200 -120,150 L120,150 C200,200 250,300 260,700 Z" fill="#05060a"/>'
    s += '<ellipse cx="0" cy="-20" rx="100" ry="128" fill="#05060a"/>'
    s += veil(lift=1.6, op=0.85)
    s += ''.join(f'<circle cx="{x}" cy="-19" r="40" fill="url(#whiteglow)"/><circle cx="{x}" cy="-19" r="12" fill="#ffffff"/>' for x in (-31, 31))
    s += '</g><rect width="2400" height="1350" fill="#a0b8d8" opacity="0.15"/>'
    return S(s)
@art
def veil_lift():
    s = portrait_bg("ghost") + veiled_bust(1200, 560, 1.75, rim=MOONRIM, lift=0.9, lids=0.25)
    s += glow(1200, 640, 560, "white", 0.95) + glow(1200, 660, 320, "white", 0.95)
    s += '<g transform="translate(2400,0) scale(-1,1)">' + sleeve(860, 360, 1.5, 30, "#14141c") + hand(860, 360, 1.5, 30, SK_MAR) + '</g>'
    s += sleeve(760, 400, 1.5, 24, "#14141c") + hand(760, 400, 1.5, 24, SK_MAR)
    return S(s)
@art
def ghost_close():
    s = portrait_bg("ghost") + f'<g filter="url(#ghost)" opacity="0.85">{veiled_bust(1200, 560, 1.75, rim="#dfeaff", black=True, lids=0.0)}</g>'
    return S(s, '<rect width="2400" height="1350" fill="#6a9ac8" opacity="0.18"/>', fog_band(1200, 0.4))
@art
def ghost_flash():
    s = '<rect width="2400" height="1350" fill="#02050a"/>' + glow(1200, 500, 1100, "moon", 0.8)
    s += f'<g filter="url(#ghost)">{veiled_bust(1200, 560, 1.9, rim="#ffffff", black=True, lift=1.0, lids=0.0, glow_eyes=True)}</g>'
    s += '<rect width="2400" height="1350" fill="#c8141a" opacity="0.12"/>'
    return S(s)


@art
def letters(): return BA.letters_table().replace("Tuyo siempre, L.", "Vuestro, M. de S.")
@art
def sword_hilt():
    s = '<rect width="2400" height="1350" fill="#0c0e14"/>' + glow(1500, 500, 800, "moon", 0.5)
    for i in range(8):
        s += f'<path d="M{i*300-100},0 C{i*300},500 {i*300-200},900 {i*300+60},1350" stroke="#000" stroke-width="80" opacity="0.4" fill="none" filter="url(#blur2)"/>'
    s += rapier(1300, 760, 160, 1.4)
    s += '<path d="M1220,640 C1260,600 1340,600 1380,640 C1400,680 1390,740 1360,760 C1320,780 1260,776 1230,750 C1200,720 1200,670 1220,640 Z" fill="#1a1410"/>'
    s += '<path d="M1230,640 C1280,620 1340,620 1376,648" stroke="#8a9cbc" stroke-width="4" fill="none" opacity="0.6"/>'
    s += '<path d="M1300,640 C1500,560 1900,500 2400,460 L2400,800 C1900,800 1520,800 1370,760 Z" fill="#0a0a0e"/>'
    return S(s)
@art
def swords():
    s = '<rect width="2400" height="1350" fill="#04060a"/>' + glow(1200, 600, 900, "moon", 0.6)
    s += rapier(300, 1000, -24, 1.25) + f'<g transform="translate(2400,0) scale(-1,1)">{rapier(300, 1000, -24, 1.25)}</g>'
    r = random.Random(4)
    s += glow(1200, 560, 260, "white", 0.95)
    for i in range(40):
        a = r.uniform(0, math.tau); d = r.uniform(30, 300)
        s += f'<path d="M1200,560 L{1200+math.cos(a)*d:.0f},{560+math.sin(a)*d:.0f}" stroke="#ffe0a0" stroke-width="{r.uniform(1.5,4):.1f}" opacity="{r.uniform(0.4,1):.2f}"/>'
    return S(s)
@art
def fallen():
    s = '<rect width="2400" height="1350" fill="#0e1218"/>' + glow(1600, 300, 900, "moon", 0.4)
    s += cobbles(0, 1350, "#1c232c")
    s += guitar(1000, 900, 70, 1.4, broken=True)
    s += '<ellipse cx="1700" cy="980" rx="260" ry="80" fill="#0a0a0e"/><path d="M1580,980 C1580,880 1620,840 1700,840 C1780,840 1820,880 1820,980 Z" fill="#14141a"/>'
    s += '<ellipse cx="1760" cy="1010" rx="120" ry="30" fill="#5a0a0e" opacity="0.8"/><ellipse cx="1840" cy="1060" rx="90" ry="22" fill="#3a0608" opacity="0.7"/>'
    s += '<path d="M1460,980 C1560,940 1840,940 1940,980" stroke="#7a9cc4" stroke-width="4" fill="none" opacity="0.5"/>'
    s += clouds(10, 1100, 1350, 3, "#b8c8d8", (0.1, 0.25))
    return S(s)
@art
def fallen_lantern():
    s = '<rect width="2400" height="1350" fill="#0e1218"/>' + cobbles(0, 1350, "#1c232c")
    s += '<g transform="translate(900,900) rotate(-70)"><path d="M-60,-80 L60,-80 L44,80 L-44,80 Z" fill="#3a2a10"/><path d="M-50,-70 L50,-70 L36,70 L-36,70 Z" fill="#ffb860" opacity="0.5"/><path d="M-70,-80 L70,-80 L0,-150 Z" fill="#1a1208"/></g>'
    s += glow(900, 900, 380, "warm", 0.7)
    s += rapier(1100, 1100, -6, 1.0)
    s += '<path d="M1100,1220 C1300,1180 1600,1240 1900,1190" stroke="#5a0a0e" stroke-width="18" fill="none" opacity="0.6"/>'
    s += clouds(10, 1100, 1350, 7, "#b8c8d8", (0.1, 0.2))
    return S(s)


@art
def church_ext():
    s = BA.temple_facade().replace("#c07060", "#3a4a66").replace("#5a4a70", "#2a3048").replace("#1a2240", "#050a14")
    return s.replace("</svg>", '<rect width="2400" height="1350" fill="#06101e" opacity="0.35"/></svg>')
@art
def church_mass(): return BA.temple_interior()
@art
def wedding():
    s = BA.temple_interior()
    add = place(veiled_full(rim="#ffd8a0", fill="#1a1418"), 1130, 1000, 0.4) + place(man_full(hat=False, cape=True, rim="#ffd8a0", fill="#08060a"), 1270, 1000, 0.42, flip=True)
    return s.replace("</svg>", add + "</svg>")
@art
def charity():
    s = BA.temple_facade()
    add = place(woman_full(rim="#ffd8a0", fill="#1a0a12"), 1000, 1300, 0.62)
    add += '<path d="M1060,820 L1150,880" stroke="#1a0a12" stroke-width="30" stroke-linecap="round"/><circle cx="1160" cy="884" r="10" fill="#e0c060"/>'
    for x in (1240, 1400):
        add += f'<path d="M{x-80},1310 C{x-80},1180 {x-40},1120 {x},1110 C{x+40},1120 {x+80},1180 {x+80},1310 Z" fill="#0c0806"/><circle cx="{x}" cy="1090" r="34" fill="#0c0806"/>'
        add += f'<path d="M{x-80},1310 C{x-80},1180 {x-40},1120 {x},1110" stroke="#ffb880" stroke-width="5" fill="none" opacity="0.6"/>'
    add += glow(1000, 900, 300, "warm", 0.4)
    return s.replace("</svg>", add + "</svg>")


@art
def beatriz_window():
    s = BA.carmen_room_svg(False)
    s += place(woman_full(rim=MOONRIM, fill="#0a0c14"), 1690, 1120, 0.8)
    return S(s)
@art
def confront():
    s = room_walls("#2a1e18", "#0a0604")
    s += '<rect x="900" y="260" width="600" height="700" fill="#0c1420"/>' + glow(1200, 500, 360, "moon", 0.6)
    for i in range(6): s += f'<rect x="{900+i*120}" y="260" width="12" height="700" fill="#0a0604"/>'
    s += candle_at(1200, 1080, 160)
    s += place(profile_figure("woman", lean=-4, rim=WARM, fill="#120608"), 760, 640, 1.55)
    s += place(profile_figure("man", lean=2, rim=WARM, fill="#060406"), 1640, 620, 1.65, flip=True)
    return S(s)
@art
def mirror():
    s = room_walls("#2a1a18", "#0a0604")
    s += '<path d="M900,940 L900,260 Q1200,120 1500,260 L1500,940 Z" fill="#c9a24a"/><path d="M930,930 L930,280 Q1200,160 1470,280 L1470,930 Z" fill="#0c1018"/>'
    s += f'<g opacity="0.8">{bea_bust(1200, 560, 1.0, rim=WARM, look=0.0, lids=0.3, smile=0.0)}</g>'
    s += '<path d="M930,930 L930,280 Q1200,160 1470,280 L1470,930 Z" fill="#8ab0d0" opacity="0.08"/>'
    s += '<path d="M800,940 L1600,940 L1700,1080 L700,1080 Z" fill="#2a1a10"/>' + candle_at(1600, 960, 140)
    # Beatriz seen from behind (dark head + shoulders) in the foreground
    s += '<path d="M700,1350 C720,1150 860,1080 1000,1060 L1400,1060 C1540,1080 1680,1150 1700,1350 Z" fill="#0a0406"/>'
    s += '<ellipse cx="1200" cy="930" rx="150" ry="180" fill="#0a0406"/><ellipse cx="1200" cy="1060" rx="110" ry="60" fill="#0a0406"/>'
    s += f'<path d="M1050,900 C1060,800 1120,760 1200,750 C1280,760 1340,800 1350,900" stroke="{WARM}" stroke-width="6" fill="none" opacity="0.5" filter="url(#blur1)"/>'
    return S(s)
@art
def mirror_close():
    s = '<rect width="2400" height="1350" fill="#0a0604"/>'
    s += '<path d="M500,1350 L500,180 Q1200,-60 1900,180 L1900,1350 Z" fill="#c9a24a"/><path d="M560,1350 L560,220 Q1200,0 1840,220 L1840,1350 Z" fill="#0c1018"/>'
    s += bea_bust(1200, 600, 1.6, rim=WARM, look=0.0, lids=0.4, smile=-0.1)
    s += '<path d="M560,1350 L560,220 Q1200,0 1840,220 L1840,1350 Z" fill="#8ab0d0" opacity="0.1"/>'
    s += '<path d="M700,300 L1000,240" stroke="#ffffff" stroke-width="20" opacity="0.15" filter="url(#blur2)"/>'
    s += glow(1800, 900, 600, "warm", 0.6)
    return S(s)
@art
def corridor():
    s = '<rect width="2400" height="1350" fill="#06080c"/>'
    cols = ["#2a2420", "#241e1a", "#1e1814", "#18140f", "#14100c", "#100c0a"]
    for k in range(5, -1, -1):
        z = 1 + k * 0.6
        w = 1600 / z; h = 1200 / z; x0 = 1200 - w / 2; y1 = 700 + 600 / z
        s += f'<path d="M{x0-80/z:.0f},{y1:.0f} L{x0-80/z:.0f},{y1-h:.0f} L{x0+w+80/z:.0f},{y1-h:.0f} L{x0+w+80/z:.0f},{y1:.0f} L{x0+w:.0f},{y1:.0f} L{x0+w:.0f},{y1-h*0.55:.0f} Q1200,{y1-h*1.0:.0f} {x0:.0f},{y1-h*0.55:.0f} L{x0:.0f},{y1:.0f} Z" fill="{cols[k]}"/>'
    s += '<path d="M0,1350 L960,920 L1440,920 L2400,1350 Z" fill="#1a140e"/>'
    s += glow(1200, 760, 300, "moon", 0.4) + candle_at(1900, 1250, 120)
    s += place(woman_full(candle=True, rim=WARM, fill="#120608"), 1500, 1200, 0.5)
    return S(s)


def brazier_svg(x, y, k=1.0, hot=1.0):
    s = '<path d="M-220,0 C-200,90 200,90 220,0 Z" fill="#2a1a0e"/>'
    s += '<ellipse cx="0" cy="0" rx="230" ry="46" fill="#3a2414"/>'
    r = random.Random(7)
    for i in range(70):
        cx, cy = r.uniform(-190, 190), r.uniform(-30, 20)
        col = r.choice(["#ff4a1a", "#ff8a2a", "#ffcf6a", "#c81a0a", "#2a0a04", "#3a1206"])
        s += f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{r.uniform(14,30):.0f}" ry="{r.uniform(8,16):.0f}" fill="{col}"/>'
    s += f'<ellipse cx="0" cy="-10" rx="200" ry="40" fill="url(#redglow)" opacity="{0.8*hot}"/>'
    s += '<path d="M-150,60 L-200,260 M150,60 L200,260 M0,80 L0,270" stroke="#1a100a" stroke-width="22" stroke-linecap="round"/>'
    return glow(x, y - 60 * k, 700 * k, "red", 0.7 * hot) + f'<g transform="translate({x},{y}) scale({k})">{s}</g>'


def santa_lucia(x, y, k=1.0):
    s = '<path d="M-180,340 L-180,-220 Q0,-400 180,-220 L180,340 Z" fill="#1a0e0a"/>'
    s += '<path d="M-90,320 C-100,120 -80,-40 -50,-120 L50,-120 C80,-40 100,120 90,320 Z" fill="#7a1a24"/>'
    s += '<path d="M-60,-120 C-80,-60 -100,40 -110,140 L-40,140 C-40,40 -30,-40 -20,-110 Z" fill="#2a4a7a"/>'
    s += '<path d="M-56,-170 C-56,-240 56,-240 56,-170 C60,-120 70,-80 80,-40 L-80,-40 C-70,-80 -60,-120 -56,-170 Z" fill="#e8e0d0" opacity="0.9"/>'
    s += '<ellipse cx="0" cy="-160" rx="34" ry="42" fill="#e8c8a8"/><path d="M-14,-168 q6,-4 10,0 M4,-168 q6,-4 10,0" stroke="#3a2010" stroke-width="3" fill="none"/>'
    s += '<path d="M-8,-138 q8,4 16,0" stroke="#9a5a4a" stroke-width="3" fill="none"/>'
    s += '<circle cx="0" cy="-180" r="80" fill="none" stroke="#e0b860" stroke-width="5" opacity="0.8"/>'
    s += '<path d="M60,-80 C100,-160 120,-220 110,-300" stroke="#3a7a3a" stroke-width="8" fill="none"/>'
    for i in range(8):
        s += f'<path d="M{110-i*2},{-300+i*26} l{-26+i},-10 M{110-i*2},{-300+i*26} l20,-14" stroke="#3a7a3a" stroke-width="4"/>'
    return glow(x, y - 100 * k, 360 * k, "warm", 0.6) + f'<g transform="translate({x},{y}) scale({k})">{s}</g>'


@art
def brasero_room():
    s = room_walls("#24181a", "#06040a")
    s += '<rect x="1600" y="260" width="420" height="560" fill="#0c1420"/>' + glow(1810, 420, 260, "moon", 0.5)
    for i in range(5): s += f'<rect x="{1600+i*100}" y="260" width="12" height="560" fill="#0a0604"/>'
    s += santa_lucia(500, 640, 0.9) + '<rect x="300" y="960" width="400" height="120" fill="#1a100a"/>'
    s += candle_at(420, 960, 60).replace('r="700"', 'r="160"') + candle_at(580, 960, 80).replace('r="700"', 'r="160"')
    s += brazier_svg(1200, 1100, 1.0)
    s += place(profile_figure("woman", lean=8, rim="#ff7040", fill="#0a0406"), 1560, 760, 1.2, flip=True)
    return S(s)
@art
def coals():
    s = '<rect width="2400" height="1350" fill="#060204"/>' + brazier_svg(1200, 1000, 3.4)
    r = random.Random(9)
    for i in range(60):
        x, y = r.uniform(300, 2100), r.uniform(100, 800)
        s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(2,6):.1f}" fill="#ffb060" opacity="{r.uniform(0.3,0.9):.2f}"/>'
    return S(s)
@art
def altar():
    s = room_walls("#24181a", "#06040a")
    s += santa_lucia(1200, 640, 1.8)
    s += '<rect x="700" y="1000" width="1000" height="120" fill="#1a100a"/>'
    for x in (820, 960, 1440, 1580):
        s += candle_at(x, 1000, 120).replace('r="700"', 'r="220"')
    s += place(profile_figure("woman", lean=-10, rim=WARM, fill="#0a0406"), 420, 760, 1.5)
    return S(s)
@art
def shadow_wall():
    s = '<rect width="2400" height="1350" fill="#1a0a08"/>' + '<rect width="2400" height="1350" fill="#000" filter="url(#plaster)" opacity="0.5"/>'
    s += glow(1200, 1350, 1300, "red", 0.9)
    s += '<g opacity="0.85" filter="url(#blur2)">' + place(profile_figure("woman", lean=34, rim=None, fill="#050102"), 1100, 500, 3.0) + '</g>'
    s += '<path d="M0,1180 L2400,1180 L2400,1350 L0,1350 Z" fill="#0a0404"/>'
    return S(s)
@art
def door_burst():
    s = BA.door_burst()
    return s.replace("</svg>", clouds(16, 200, 1200, 4, "#5a4a44", (0.15, 0.35), (200, 500), (60, 160)) + glow(1200, 900, 600, "red", 0.4) + "</svg>")
@art
def sickbed():
    s = room_walls("#2a1e18", "#0a0604")
    s += '<rect x="500" y="760" width="1300" height="320" fill="#2a1a12"/><rect x="480" y="700" width="1340" height="80" fill="#e8e0d0"/>'
    s += '<path d="M500,780 L1800,780 L1840,1000 L460,1000 Z" fill="#6a5a5a"/>'
    s += '<ellipse cx="700" cy="700" rx="150" ry="60" fill="#f0eadc"/>'
    s += '<path d="M620,700 C620,640 700,610 760,630 C800,650 800,700 780,730 Z" fill="#ece6d8"/>'
    s += '<path d="M820,720 C1100,700 1500,720 1760,760" stroke="#4a3a3a" stroke-width="40" fill="none" opacity="0.5"/>'
    s += candle_at(1950, 1000, 130) + candle_at(320, 1000, 90)
    s += place(man_full(hat=False, cape=True, rim=WARM, fill="#080406"), 1500, 1250, 0.7)
    s += place(woman_full(rebozo_head=True, old=True, rim=WARM, fill="#080406"), 300, 1300, 0.6)
    return S(s)
@art
def veiled_chair():
    s = room_walls("#22283a", "#08080e")
    s += '<path d="M1400,1080 L1400,260 Q1650,140 1900,260 L1900,1080 Z" fill="#0c1a2c"/><path d="M1420,1080 L1420,280 Q1650,170 1880,280 L1880,1080 Z" fill="#1a3048"/>'
    s += glow(1650, 400, 360, "moon", 0.9) + '<path d="M1420,1080 L1150,1350 L2300,1350 L1880,1080 Z" fill="url(#beamc)" opacity="0.6"/>'
    s += '<path d="M1400,1080 L1400,260 Q1650,140 1900,260 L1900,1080" stroke="#1a120c" stroke-width="30" fill="none"/>'
    s += '<path d="M940,1080 L940,420 Q1100,360 1260,420 L1260,1080 Z" fill="#1a0e0a"/><path d="M960,500 L1240,500" stroke="#c9a24a" stroke-width="5" opacity="0.5"/>'
    s += place(veiled_full(rim=MOONRIM, fill="#14101a"), 1100, 1180, 0.82)
    return S(s)
@art
def kneel():
    s = room_walls("#22283a", "#08080e")
    s += '<path d="M1500,1080 L1500,260 Q1750,140 2000,260 L2000,1080 Z" fill="#1a3048"/>' + glow(1750, 400, 360, "moon", 0.9)
    s += '<path d="M600,1080 L600,420 Q760,360 920,420 L920,1080 Z" fill="#1a0e0a"/>'
    s += place(veiled_full(rim=MOONRIM, fill="#14101a"), 760, 1180, 0.82)
    man = ('<path d="M0,0 C-20,-60 -40,-160 -40,-260 C-40,-340 -10,-400 40,-420 C100,-430 140,-380 150,-300 C160,-200 200,-100 260,-40 L300,0 Z"/>'
           '<path d="M-40,-80 L-200,-80 L-210,0 L-40,0 Z"/>'
           '<path d="M40,-400 C-20,-380 -90,-330 -150,-300 L-160,-270 C-90,-290 -20,-320 30,-340 Z"/>'
           '<ellipse cx="40" cy="-490" rx="60" ry="70"/>'
           '<path d="M120,-380 C220,-300 300,-120 340,0 L180,0 C160,-100 130,-220 90,-300 Z"/>')
    s += f'<g transform="translate(1180,1080)"><g fill="#060406">{man}</g><path d="M40,-560 C100,-560 120,-520 104,-470 M150,-300 C160,-200 200,-100 260,-40" stroke="{MOONRIM}" stroke-width="6" fill="none" opacity="0.7" filter="url(#blur1)"/></g>'
    s += '<path d="M0,1080 L2400,1080" stroke="#3a2a1c" stroke-width="12"/>'
    return S(s)
@art
def hands_hold():
    s = '<rect width="2400" height="1350" fill="#06080e"/>' + glow(1200, 600, 900, "moon", 0.6)
    s += sleeve(1180, 700, 2.0, 10, "#2a2a36", lace=True) + hand(1180, 700, 2.0, 10, SK_BEA)
    s += '<g transform="translate(2400,0) scale(-1,1)">' + sleeve(1060, 760, 2.1, -8, "#0c0c10", lace=False) + hand(1060, 760, 2.1, -8, SK_MAR, flip=True) + '</g>'
    s += '<path d="M200,1100 C600,1000 1800,1000 2200,1100 L2400,1350 L0,1350 Z" fill="#e4eaf4" opacity="0.25"/>'
    return S(s)
@art
def stairs(): return BA.stairs_interior()


@art
def chronicle():
    s = '<rect width="2400" height="1350" fill="#0a0604"/>' + table_wood(700) + candle_at(1900, 760, 220)
    s += '<path d="M300,760 C600,700 900,720 1200,780 L1200,1260 C900,1200 600,1190 300,1240 Z" fill="#d8c8a0"/>'
    s += '<path d="M2100,760 C1800,700 1500,720 1200,780 L1200,1260 C1500,1200 1800,1190 2100,1240 Z" fill="#e2d4b0"/>'
    s += '<path d="M1200,780 L1200,1260" stroke="#8a7a5a" stroke-width="6"/>'
    s += '<text x="750" y="860" font-family="IM FELL English" font-size="54" fill="#3a2414" text-anchor="middle">La Calle de la</text>'
    s += '<text x="750" y="930" font-family="IM FELL English" font-size="64" fill="#3a2414" text-anchor="middle">Quemada</text>'
    r = random.Random(3)
    for i in range(8):
        y = 980 + i * 30
        s += f'<path d="M380,{y} L{1100 - r.uniform(0, 140):.0f},{y}" stroke="#4a3424" stroke-width="5" stroke-dasharray="{r.randint(20,60)} 10 {r.randint(30,80)} 12" opacity="0.65"/>'
    s += f'<g opacity="0.75">{place(veiled_full(rim=None, fill="#3a2414"), 1650, 1180, 0.36)}</g>'
    s += '<rect x="300" y="700" width="1800" height="560" fill="#000" filter="url(#grain)" opacity="0.2"/>'
    return S(s)
@art
def chronicle_page():
    s = '<rect width="2400" height="1350" fill="#d8c8a0"/><rect width="2400" height="1350" fill="#000" filter="url(#plaster)" opacity="0.3"/>'
    s += '<rect x="200" y="140" width="2000" height="1080" fill="none" stroke="#5a3a24" stroke-width="6"/>'
    s += '<text x="1200" y="300" font-family="IM FELL English" font-size="100" fill="#3a2414" text-anchor="middle">Leyendas de la Ciudad de México</text>'
    s += '<rect x="600" y="400" width="1200" height="700" fill="#cbb890" stroke="#3a2414" stroke-width="5"/>'
    for i in range(58):
        s += f'<path d="M600,{400+i*12} L1800,{400+i*12}" stroke="#3a2414" stroke-width="1.5" opacity="0.25"/>'
    s += place(veiled_full(rim=None, fill="#2a1a10", black=True), 1080, 1060, 0.55) + place(man_full(hat=True, cape=True, rim=None, fill="#2a1a10"), 1320, 1060, 0.58, flip=True)
    s += '<path d="M640,1060 L1760,1060" stroke="#2a1a10" stroke-width="5"/>'
    s += '<rect width="2400" height="1350" fill="#000" filter="url(#grain)" opacity="0.15"/>'
    return S(s)
@art
def black(): return S('<rect width="2400" height="1350" fill="#000"/>')


# ===================================================================== transparent layers
@art
def l_candle_glow(): return S(glow(CANDLE_XY[0], CANDLE_XY[1], 900, "warm", 0.35))
@art
def l_lamp_glow(): return S(glow(LAMP_XY[0], LAMP_XY[1], 520, "warm", 0.5))
@art
def l_coals_glow(): return S(glow(1200, 1150, 1100, "red", 0.45))
@art
def l_fog(): return S(clouds(18, 900, 1400, 31, "#b0c4d8", (0.08, 0.2), (300, 700), (60, 140)))
@art
def l_martin_run():
    fig = man_full(hat=True, cape=True, rim=MOONRIM, fill="#020305", walk=0.7)
    fig += '<path d="M-90,-780 C-220,-760 -330,-640 -400,-520 C-300,-540 -220,-560 -150,-620 Z" fill="#020305"/>'
    fig += '<path d="M60,-1000 C120,-1060 180,-1040 200,-970" stroke="#020305" stroke-width="14" fill="none" stroke-linecap="round"/>'
    return S(place(fig, 1200, 1180, 0.55))
@art
def l_watcher():
    fig = man_full(hat=True, cape=True, rim=MOONRIM, fill="#020305")
    fig += '<path d="M60,-1000 C120,-1060 180,-1040 200,-970" stroke="#020305" stroke-width="14" fill="none" stroke-linecap="round"/>'
    return S(place(fig, 520, 1220, 0.62))
@art
def l_duel():
    return S(place(man_sword(rim=MOONRIM, fill="#020305", lunge=True), 860, 1230, 0.62),
             place(man_sword(rim="#ffcf8a", fill="#06040a"), 1560, 1230, 0.6, flip=True))
@art
def l_serenade():
    fig = man_full(hat=True, cape=False, rim="#ffcf8a", fill="#06040a")
    return S(place(fig, 1000, 1290, 0.42), guitar(1050, 1000, -60, 0.5))
@art
def l_couple_walk():
    return S(place(veiled_full(rim="#ffd8a0", black=True, fill="#0a0608"), 1080, 1240, 0.5),
             place(man_full(hat=True, cape=True, rim="#ffd8a0", fill="#060406", walk=0.2), 1210, 1240, 0.53))
@art
def l_ghost_veil():
    fig = veiled_full(rim="#dfeaff", black=False, fill="#9ab4d4", ghost=True)
    return S(f'<g filter="url(#ghost)" opacity="0.75">{place(fig, 1360, 1000, 0.36)}</g>', glow(1360, 760, 220, "moon", 0.5))


def run(names):
    for n in names:
        if n in ART:
            open(os.path.join(A, n + ".svg"), "w", encoding="utf-8").write(ART[n]())
    print("svg written:", len([n for n in names if n in ART]))


@art
def duel_street(): return S(persp_street("night", seed=15), fog_band(1200, 0.3, 16))

if __name__ == "__main__":
    run(sys.argv[1:] or list(ART))
