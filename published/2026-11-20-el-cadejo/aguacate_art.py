#!/usr/bin/env python3
"""Illustrations for 'El Callejón del Aguacate' (Coyoacán) — writes art/*.svg (2400x1350).
Reuses the colonial helpers of earlier videos (beso_art.py, chars.py, base_chars.py, qm_art.py = La Quemada's make_art).
Usage: python3 make_art.py [name ...]   then: node /home/claude/pipeline/render_svg.js art/*.svg"""
import sys, os, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '/home/claude/pipeline'); sys.path.insert(0, HERE)
from art import *
from chars import place, man_full, woman_full, strands, stubble, wrinkles, angry_brows, bust_frame, SIL
from base_chars import head, uid, grad_lin, grad_rad
import beso_art as BA
from beso_art import S, lg, clouds, room_walls, candle_at, flame, table_wood, portrait_bg, MOONRIM
import qm_art as QM

A = os.path.join(HERE, "art"); os.makedirs(A, exist_ok=True)
ART = {}
def art(fn):
    ART[fn.__name__] = fn; return fn

WARM = "#ffcf8a"; RED = "#c8141a"
LAMP_XY = (330, 380)        # wall lantern in alley views (l_lamp_glow)
CANDLE_XY = (1900, 760)     # candle in interiors (l_candle_glow)
NICHE_XY = (1745, 560)      # niche centre in alley_night (l_vela_glow)
VELAC_XY = (1200, 1010)     # veladora in niche close-ups (l_vela_close)

# =========================================================== perspective
VX, VY, W0 = 1200, 640, 1150
def P(X, Y, z): return (VX + X * W0 / z, VY + Y * W0 / z)
def pts(*p): return " ".join(f"{x:.0f},{y:.0f}" for x, y in p)
def quad(a, b, c, d, fill, extra=""): return f'<polygon points="{pts(a, b, c, d)}" fill="{fill}" {extra}/>'
def affine(tl, tr, bl):
    """matrix mapping unit square (0..1) to a parallelogram tl,tr,bl"""
    a, b = tr[0] - tl[0], tr[1] - tl[1]; c, d = bl[0] - tl[0], bl[1] - tl[1]
    return f'matrix({a:.3f},{b:.3f},{c:.3f},{d:.3f},{tl[0]:.1f},{tl[1]:.1f})'

PAL = {  # wall colours per mood: (left houses, right barda, floor, sky top, sky bottom, light)
    "night": (["#3a2a2a", "#2a3040", "#3a3226", "#26303a"], "#2c2c34", "#15141a", "#030812", "#14243a", "#ffc865"),
    "dusk": (["#5a3a30", "#3a4258", "#5a4a34", "#38465a"], "#44444e", "#22202a", "#1a1a30", "#6a4a5a", "#ffc865"),
    "dawn": (["#5a4a50", "#46566e", "#5e5448", "#4a5a6e"], "#565a66", "#2a2c36", "#2a3a5a", "#c89a8a", "#ffe0a0"),
    "day": (["#c08a48", "#3a5a8a", "#b8563a", "#d0a860"], "#8a8478", "#5a5248", "#5a8ac8", "#c8dcea", "#ffe8b0"),
    "today": (["#d09a3a", "#2a4a9a", "#c0482e", "#e0b860"], "#9a9488", "#6a6258", "#6a9ad8", "#d0e4f0", "#ffe8b0"),
}
DARK = {"night": 1.0, "dusk": 0.6, "dawn": 0.45, "day": 0.0, "today": 0.0}


def canopy(cx, cy, rx, ry, seed=1, rim="#7a9cc4", dark=("#050d08", "#08140c", "#0c1a10"), n=260, fruit=12, lit=0.35, leaf=1.0):
    """avocado canopy: many oblong leaves, rim-lit on the top-right, hanging pear-shaped fruit"""
    r = random.Random(seed); s = ""
    for i in range(n):
        a = r.uniform(0, math.tau); d = math.sqrt(r.random())
        x = cx + math.cos(a) * rx * d; y = cy + math.sin(a) * ry * d
        L = r.uniform(46, 80) * leaf; W = L * 0.32; rot = r.uniform(-70, 70) + (20 if x > cx else -20)
        col = r.choice(dark)
        s += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{L:.0f}" ry="{W:.0f}" fill="{col}" transform="rotate({rot:.0f} {x:.0f} {y:.0f})"/>'
        if rim and (math.cos(a) * 0.5 - math.sin(a)) > 0.3 and d > 0.5 and r.random() < lit * 2:
            s += (f'<path d="M{x-L*0.7:.0f},{y:.0f} Q{x:.0f},{y-W*1.2:.0f} {x+L*0.7:.0f},{y:.0f}" stroke="{rim}" stroke-width="2.5" fill="none" '
                  f'opacity="{r.uniform(0.25,0.6):.2f}" transform="rotate({rot:.0f} {x:.0f} {y:.0f})"/>')
    for i in range(fruit):
        a = r.uniform(0.2, math.pi - 0.2); d = r.uniform(0.3, 0.9)
        x = cx + math.cos(a) * rx * d; y = cy + math.sin(a) * ry * d
        s += (f'<path d="M{x:.0f},{y-30:.0f} L{x:.0f},{y-6:.0f}" stroke="#05080a" stroke-width="3"/>'
              f'<path d="M{x:.0f},{y-8:.0f} C{x-10:.0f},{y-8:.0f} {x-12:.0f},{y+6:.0f} {x-18:.0f},{y+18:.0f} C{x-24:.0f},{y+34:.0f} {x-12:.0f},{y+46:.0f} {x:.0f},{y+46:.0f} '
              f'C{x+12:.0f},{y+46:.0f} {x+24:.0f},{y+34:.0f} {x+18:.0f},{y+18:.0f} C{x+12:.0f},{y+6:.0f} {x+10:.0f},{y-8:.0f} {x:.0f},{y-8:.0f} Z" fill="#0e1a0a"/>')
        if rim:
            s += f'<path d="M{x+6:.0f},{y-2:.0f} C{x+14:.0f},{y+10:.0f} {x+20:.0f},{y+26:.0f} {x+14:.0f},{y+40:.0f}" stroke="{rim}" stroke-width="2.5" fill="none" opacity="0.5"/>'
    return s


def branch(x0, y0, x1, y1, w, col="#070605", bend=0.2, seed=1):
    mx, my = (x0 + x1) / 2 + (y1 - y0) * bend, (y0 + y1) / 2 - (x1 - x0) * bend
    return f'<path d="M{x0},{y0} Q{mx:.0f},{my:.0f} {x1},{y1}" stroke="{col}" stroke-width="{w}" fill="none" stroke-linecap="round"/>'


def virgin(x, y, k=1.0, lit=1.0, dark=False):
    """Virgin figure in the Guadalupe manner (standing, hands joined, star mantle, rays). foot centre x,y; ~520 tall at k=1"""
    g = uid("vg")
    mant = "#1a4a4a" if not dark else "#0a1a1c"; robe = "#a8605a" if not dark else "#2a1614"
    s = f'<g transform="translate({x},{y}) scale({k})">'
    # rays / mandorla
    if not dark:
        s += f'<ellipse cx="0" cy="-270" rx="170" ry="300" fill="#ffcf6a" opacity="{0.18*lit:.2f}" filter="url(#blur2)"/>'
        for i in range(48):
            a = math.tau * i / 48
            s += f'<path d="M{math.cos(a)*120:.0f},{-270+math.sin(a)*240:.0f} L{math.cos(a)*175:.0f},{-270+math.sin(a)*320:.0f}" stroke="#e8b850" stroke-width="5" opacity="{0.55*lit:.2f}"/>'
    s += f'<path d="M-40,-10 C-30,-30 30,-30 40,-10 L60,0 L-60,0 Z" fill="#3a2a20"/>'   # angel/base
    s += f'<path d="M-80,-6 C-40,-36 40,-36 80,-6 C50,-20 -50,-20 -80,-6 Z" fill="#202024"/>'  # crescent
    s += f'<path d="M-70,-20 C-78,-160 -62,-300 -40,-400 L40,-400 C62,-300 78,-160 70,-20 Z" fill="{robe}"/>'
    for i in range(5):
        s += f'<path d="M{-40+i*20},-380 C{-46+i*22},-260 {-50+i*24},-140 {-56+i*28},-24" stroke="#5a2a28" stroke-width="3" fill="none" opacity="0.5"/>'
    s += f'<path d="M-46,-430 C-100,-380 -110,-200 -96,-30 C-80,-20 -70,-22 -62,-28 C-70,-180 -56,-330 -18,-420 Z" fill="{mant}"/>'
    s += f'<path d="M46,-430 C100,-380 110,-200 96,-30 C80,-20 70,-22 62,-28 C70,-180 56,-330 18,-420 Z" fill="{mant}"/>'
    s += f'<path d="M-36,-470 C-30,-500 30,-500 36,-470 C50,-440 52,-420 46,-400 L-46,-400 C-52,-420 -50,-440 -36,-470 Z" fill="{mant}"/>'
    r = random.Random(7)
    for i in range(22):
        sx = r.choice([-1, 1]) * r.uniform(52, 92); sy = r.uniform(-400, -60)
        s += f'<circle cx="{sx:.0f}" cy="{sy:.0f}" r="4" fill="#e8c860" opacity="{0.8 if not dark else 0.2}"/>'
    s += f'<path d="M-40,-470 C-30,-500 30,-500 40,-470" stroke="#e8c860" stroke-width="4" fill="none" opacity="{0.8 if not dark else 0.2}"/>'
    s += f'<ellipse cx="-6" cy="-445" rx="20" ry="25" fill="{"#c49878" if not dark else "#2a201c"}"/>'  # face, tilted
    s += f'<path d="M-16,-448 q5,-3 9,0 M2,-448 q5,-3 9,0" stroke="#3a2016" stroke-width="2" fill="none"/>'
    s += f'<path d="M-14,-360 L0,-300 L14,-360 Z" fill="{"#d4a888" if not dark else "#2a201c"}"/>'  # joined hands
    s += '</g>'
    return s


def veladora(x, y, k=1.0, lit=True, col="#c8202a", seed=1):
    s = f'<g transform="translate({x},{y}) scale({k})">'
    s += f'<rect x="-26" y="-110" width="52" height="110" rx="6" fill="{col}" opacity="0.75"/>'
    s += f'<rect x="-26" y="-110" width="52" height="110" rx="6" fill="#fff" opacity="0.12"/>'
    s += '<path d="M-18,-100 L-18,-10" stroke="#fff" stroke-width="5" opacity="0.35"/>'
    if lit:
        s += f'<ellipse cx="0" cy="-60" rx="24" ry="40" fill="#ffd27a" opacity="0.55" filter="url(#blur1)"/>'
        s += '<path d="M0,-150 C-12,-130 -10,-112 0,-106 C10,-112 12,-130 0,-150 Z" fill="#ffe8a8"/><path d="M0,-136 C-5,-126 -4,-116 0,-112 C4,-116 5,-126 0,-136 Z" fill="#fff"/>'
    else:
        s += '<path d="M0,-108 C-8,-140 12,-170 -4,-220 C-16,-260 10,-290 0,-330" stroke="#8a94a4" stroke-width="5" fill="none" opacity="0.35" filter="url(#blur1)"/>'
    s += '</g>'
    return s


def niche_unit(lit=True, dark_virgin=False, toys=False):
    """niche contents drawn in a 0..100 x 0..140 box (stone frame + arch + virgin + candle)"""
    s = '<rect x="0" y="0" width="100" height="140" fill="#6a6258"/>'
    s += '<path d="M14,130 L14,50 C14,24 32,10 50,10 C68,10 86,24 86,50 L86,130 Z" fill="#1a1410"/>'
    s += '<path d="M14,130 L14,50 C14,24 32,10 50,10 C68,10 86,24 86,50 L86,130" stroke="#2a4a8a" stroke-width="6" fill="none"/>'
    s += '<path d="M8,132 L92,132 L96,140 L4,140 Z" fill="#8a8274"/>'
    s += f'<g transform="translate(50,124) scale(0.18)">{virgin(0, 0, 1.0, 0.8 if lit else 0.2, dark=dark_virgin)}</g>'
    s += f'<g transform="translate(30,131) scale(0.12)">{veladora(0, 0, 1.0, lit)}</g><g transform="translate(70,131) scale(0.12)">{veladora(0, 0, 1.0, lit, "#e8e0d0")}</g>'
    return s


def cobble_floor(z0=0.85, z1=7.0, col="#15141a", hi="#4a5060", seed=3, wet=0.0, light=None):
    r = random.Random(seed); s = ""
    z = z0
    while z < z1:
        dz = z * 0.1
        ya, yb = P(0, 0.62, z)[1], P(0, 0.62, z + dz)[1]
        n = 14
        for i in range(n):
            xa = -1.05 + 2.1 * (i + r.uniform(0.0, 0.3)) / n
            xb = xa + 2.1 / n * 0.85
            (x0, _), (x1, _) = P(xa, 0.62, z + dz * 0.5), P(xb, 0.62, z + dz * 0.5)
            cy = (ya + yb) / 2; h = abs(ya - yb) * 0.42
            s += f'<ellipse cx="{(x0+x1)/2:.0f}" cy="{cy:.0f}" rx="{abs(x1-x0)/2:.0f}" ry="{h:.1f}" fill="{col}"/>'
            if z < 3.5 and r.random() < 0.6:
                s += f'<ellipse cx="{(x0+x1)/2:.0f}" cy="{cy-h*0.35:.0f}" rx="{abs(x1-x0)/3:.0f}" ry="{h*0.35:.1f}" fill="{hi}" opacity="{0.25 + wet*0.3:.2f}"/>'
        z += dz
    return s


def callejon(mood="night", niche=True, lamp_on=True, tree=True, seed=3, plaque=False, far_lamp=True, door_lit=True):
    houses, barda, floor, st, sb, light = PAL[mood]; dk = DARK[mood]
    r = random.Random(seed)
    s = sky(st, sb)
    if mood in ("night", "dusk"):
        s += stars(120, seed, 420) + moon(1500, 150, 46)
    if mood == "dawn":
        s += glow(1200, 520, 700, "warm", 0.5)
    # floor base
    s += quad(P(-1.05, 0.62, 0.8), P(1.05, 0.62, 0.8), P(1.05, 0.62, 7), P(-1.05, 0.62, 7), "#0a0a0e" if dk > 0.5 else "#3a342c")
    s += cobble_floor(col=floor, hi="#5a6070" if dk > 0.5 else "#a89c88", seed=seed, wet=0.3 if mood == "night" else 0)
    # end wall at z=7
    s += quad(P(-1.05, -1.1, 7), P(1.05, -1.1, 7), P(1.05, 0.62, 7), P(-1.05, 0.62, 7), houses[3])
    ex, ey = P(-0.2, 0.62, 7)
    s += f'<path d="M{ex:.0f},{ey:.0f} l0,-110 q34,-30 68,0 l0,110 Z" fill="{"#ffc865" if (door_lit and dk > 0.3) else "#2a1a10"}" opacity="0.9"/>'
    # left houses: segments along z with doors and windows
    zs = [0.8, 1.35, 2.3, 3.6, 5.2, 7.0]
    for i in range(len(zs) - 1):
        za, zb = zs[i], zs[i + 1]; top = -1.0 + r.uniform(-0.15, 0.1)
        col = houses[i % len(houses)]
        s += quad(P(-1.05, top, za), P(-1.05, top, zb), P(-1.05, 0.62, zb), P(-1.05, 0.62, za), col)
        s += quad(P(-1.05, top, za), P(-1.05, top, zb), P(-1.05, top + 0.06, zb), P(-1.05, top + 0.06, za), "#000", 'opacity="0.35"')
        # zoclo (painted base band)
        s += quad(P(-1.05, 0.4, za), P(-1.05, 0.4, zb), P(-1.05, 0.62, zb), P(-1.05, 0.62, za), "#000", 'opacity="0.25"')
        # door
        zm = za + (zb - za) * 0.35; zn = za + (zb - za) * 0.6
        s += quad(P(-1.05, -0.15, zm), P(-1.05, -0.15, zn), P(-1.05, 0.62, zn), P(-1.05, 0.62, zm), "#2a1608" if dk < 0.5 else "#0c0806")
        # window
        if i % 2 == 0:
            wa, wb = za + (zb - za) * 0.7, za + (zb - za) * 0.9
            lit = dk > 0.3 and r.random() < 0.6
            s += quad(P(-1.05, -0.55, wa), P(-1.05, -0.55, wb), P(-1.05, -0.15, wb), P(-1.05, -0.15, wa), light if lit else "#0a0c10", f'opacity="{0.9 if lit else 1}"')
            for b in range(4):
                zz = wa + (wb - wa) * (b + 0.5) / 4
                s += f'<line x1="{P(-1.05,-0.55,zz)[0]:.0f}" y1="{P(-1.05,-0.55,zz)[1]:.0f}" x2="{P(-1.05,-0.15,zz)[0]:.0f}" y2="{P(-1.05,-0.15,zz)[1]:.0f}" stroke="#050505" stroke-width="{6/zz:.1f}"/>'
    s += quad(P(-1.05, -1.2, 0.8), P(-1.05, -1.2, 7), P(-1.05, 0.62, 7), P(-1.05, 0.62, 0.8), "#000", 'filter="url(#plaster)" opacity="0.45"')
    # right: stone barda (lower wall) with the avocado above
    bt = -0.45
    s += quad(P(1.05, bt, 0.8), P(1.05, bt, 7), P(1.05, 0.62, 7), P(1.05, 0.62, 0.8), barda)
    for j in range(40):  # stones
        zz = 0.85 * (7 / 0.85) ** (j / 40)
        for yy in (bt + 0.15, bt + 0.42, bt + 0.7, bt + 0.95):
            a, b = P(1.05, yy, zz), P(1.05, yy + 0.22, zz * 1.04)
            s += f'<line x1="{a[0]:.0f}" y1="{a[1]:.0f}" x2="{b[0]:.0f}" y2="{b[1]:.0f}" stroke="#000" stroke-width="{4/zz:.1f}" opacity="0.35"/>'
        a, b = P(1.05, bt, zz), P(1.05, 0.62, zz)
    s += quad(P(1.05, bt, 0.8), P(1.05, bt, 7), P(1.05, 0.62, 7), P(1.05, 0.62, 0.8), "#000", 'filter="url(#plaster)" opacity="0.4"')
    s += quad(P(1.05, bt - 0.05, 0.8), P(1.05, bt - 0.05, 7), P(1.05, bt, 7), P(1.05, bt, 0.8), "#8a8478" if dk < 0.5 else "#3a3a44")
    if niche:  # niche on the barda corner (z ~1.55)
        tl, tr, bl = P(1.05, -0.32, 1.5), P(1.05, -0.32, 1.85), P(1.05, 0.15, 1.5)
        s += f'<g transform="{affine(tl, tr, bl)}"><g transform="scale(0.01,0.00714)">{niche_unit(lit=(mood != "dawn"))}</g></g>'
    if lamp_on:
        x, y = LAMP_XY
        s += f'<path d="M{x-120},{y-60} L{x},{y-60} L{x},{y-30}" stroke="#05070a" stroke-width="10" fill="none"/>'
        s += f'<path d="M{x-34},{y-30} L{x+34},{y-30} L{x+24},{y+70} L{x-24},{y+70} Z" fill="{light if dk > 0.3 else "#e8e0c8"}"/><path d="M{x-40},{y-30} L{x+40},{y-30} L{x},{y-76} Z" fill="#05070a"/>'
        s += f'<path d="M{x-24},{y+70} L{x+24},{y+70} L{x},{y+96} Z" fill="#05070a"/>'
    if plaque:
        a, b, c = P(-1.05, -0.45, 1.05), P(-1.05, -0.45, 1.3), P(-1.05, -0.3, 1.05)
        s += (f'<g transform="{affine(a, b, c)}"><rect width="1" height="1" fill="#f0ece0"/><rect x="0.04" y="0.08" width="0.92" height="0.84" fill="none" stroke="#2a4a8a" stroke-width="0.03"/>'
              f'<text x="0.5" y="0.42" font-family="Oswald" font-size="0.22" fill="#1a2a5a" text-anchor="middle">CALLEJÓN DEL</text>'
              f'<text x="0.5" y="0.78" font-family="Oswald" font-size="0.3" fill="#1a2a5a" text-anchor="middle">AGUACATE</text></g>')
    if tree:
        rim = "#7a9cc4" if dk > 0.5 else ("#ffe0a0" if mood in ("dawn", "dusk") else "#e8f4c0")
        dcol = ("#050d08", "#08140c", "#0c1a10") if dk > 0.5 else (("#1a2a1a", "#22341e", "#2a3c22") if dk > 0.2 else ("#2a4a1e", "#335a24", "#3e6a2a"))
        tx, ty = P(1.4, -0.9, 2.6)
        s += branch(2400, 520, int(tx), int(ty), 70, "#070605" if dk > 0.3 else "#3a2a1c")
        s += branch(int(tx), int(ty), 1500, 260, 34, "#070605" if dk > 0.3 else "#3a2a1c", 0.1)
        s += canopy(1980, 230, 560, 260, seed + 10, rim, dcol, 340, 14, lit=0.4)
        s += canopy(1560, 160, 330, 160, seed + 11, rim, dcol, 160, 6, lit=0.4)
    # global darkness for night
    if dk > 0:
        s += f'<rect width="2400" height="1350" fill="#02040a" opacity="{0.25*dk:.2f}"/>'
    if mood == "today":
        s += '<path d="M0,300 C600,360 1400,330 2400,280" stroke="#111" stroke-width="4" fill="none"/><path d="M0,340 C700,400 1500,380 2400,330" stroke="#111" stroke-width="3" fill="none"/>'
        r2 = random.Random(9)
        for i in range(60):  # bougainvillea on left top
            x, y = r2.uniform(0, 700), r2.uniform(0, 260)
            s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r2.uniform(10,22):.0f}" fill="{r2.choice(["#c0306a", "#d8407a", "#a02050"])}" opacity="0.9"/>'
    return s


# =========================================================== characters
SK_SOL = dict(base="#a87e62", light="#c29a7c", hi="#d8b496", shadow="#6c4a38", deep="#38241a")
SK_KID = dict(base="#b8875e", light="#d4a47a", hi="#e8be96", shadow="#7a5236", deep="#40281a")
SK_GHO = dict(base="#7a90a8", light="#98aec4", hi="#c0d4e8", shadow="#4a5a70", deep="#1a2430")
OLIVE = ("#1c2014", "#3a4026", "#565c38")


def soldier_hair(gray=True):
    r = random.Random(4)
    s = '<path d="M-80,-40 C-88,-96 -60,-140 0,-146 C60,-140 88,-96 80,-40 C76,-70 60,-100 0,-104 C-60,-100 -76,-70 -80,-40 Z" fill="#14100c"/>'
    s += '<path d="M-80,-40 C-84,-10 -82,10 -76,26 L-70,-6 Z M80,-40 C84,-10 82,10 76,26 L70,-6 Z" fill="#14100c"/>'
    if gray:
        s += strands(r, [(-78, -40, -80, -10, -74, 20), (78, -40, 80, -10, 74, 20)], 9, "#a8a49c", (1.5, 3), (0.5, 0.9), 4)
        s += strands(r, [(-60, -110, -20, -130, 30, -120)], 6, "#8a867e", (1.5, 2.5), (0.3, 0.6), 6)
    return s


def mustache(col="#1a1410", gray=True):
    s = (f'<path d="M0,52 C-14,46 -34,46 -52,56 C-66,64 -76,76 -80,86 C-68,78 -54,72 -40,70 C-24,68 -10,66 0,62 '
         f'C10,66 24,68 40,70 C54,72 68,78 80,86 C76,76 66,64 52,56 C34,46 14,46 0,52 Z" fill="{col}"/>')
    if gray:
        r = random.Random(2)
        s += strands(r, [(-6, 56, -40, 58, -74, 82), (6, 56, 40, 58, 74, 82)], 7, "#8a8478", (1, 2), (0.4, 0.8), 3)
    return s


def kepi(rim="#9fc2e8", col="#2a2e1c"):
    s = f'<path d="M-92,-96 C-96,-150 -70,-196 0,-200 C70,-196 96,-150 92,-96 Z" fill="{col}"/>'
    s += '<path d="M-92,-112 C-30,-122 30,-122 92,-112 L92,-92 C30,-102 -30,-102 -92,-92 Z" fill="#120e08"/>'
    s += '<path d="M-96,-96 C-60,-70 60,-70 104,-94 C110,-84 104,-74 96,-70 C50,-52 -50,-54 -100,-74 C-108,-80 -104,-92 -96,-96 Z" fill="#06060a"/>'
    s += '<path d="M-90,-80 C-40,-62 40,-62 98,-80" stroke="#3a3a44" stroke-width="3" fill="none" opacity="0.7"/>'
    s += '<path d="M0,-168 L10,-148 L32,-146 L14,-132 L20,-110 L0,-122 L-20,-110 L-14,-132 L-32,-146 L-10,-148 Z" fill="#c9a24a"/>'
    s += f'<path d="M-92,-96 C-96,-150 -70,-196 0,-200" stroke="{rim}" stroke-width="4" fill="none" opacity="0.6"/>'
    return s


def soldier_head(look=0.0, turn=0.0, lids=0.35, rim="#9fc2e8", cold=False, ruin=False, ghost=False, cap=True):
    sk = SK_GHO if ghost else SK_SOL
    s = head(look=look, smile=(-0.45 if (cold or ruin) else -0.1), lids=(0.55 if cold else (0.6 if ruin else lids)), rim=rim, turn=turn, sk=sk,
             headwrap=False, earring=False, lips=("#5a3028", "#6a4038"), iris=("#0a0a10" if not ghost else "#e8f4ff"), brow_w=1.3, neck=True)
    s += stubble(random.Random(3), "#2a2220" if not ghost else "#2a3440", 180 if ruin else 90)
    s += wrinkles("#3a2418" if not ghost else "#1a2430", 0.55, 1.2 if ruin else 0.9)
    s += '<path d="M-60,-60 L-28,-66 M60,-60 L28,-66" stroke="#14100c" stroke-width="10" stroke-linecap="round"/>'
    if cold:
        s += angry_brows("#14100c", 10)
    s += '<path d="M40,10 L62,40" stroke="#5a2a20" stroke-width="4" opacity="0.6"/>'  # scar on cheek
    s += mustache("#1a1410" if not ghost else "#1a2430")
    if ruin:
        s += '<path d="M-44,-4 C-48,20 -44,40 -48,60" stroke="#cfe0ff" stroke-width="4" fill="none" opacity="0.55"/>'
        s += '<ellipse cx="-32" cy="-22" rx="26" ry="10" fill="#5a2a2a" opacity="0.3"/><ellipse cx="32" cy="-22" rx="26" ry="10" fill="#5a2a2a" opacity="0.3"/>'
    if ghost:
        s += '<circle cx="-32" cy="-28" r="9" fill="#e8f4ff" filter="url(#glow)"/><circle cx="32" cy="-28" r="9" fill="#e8f4ff" filter="url(#glow)"/>'
    if not cap:
        s += soldier_hair(True)
    else:
        s += '<path d="M-80,-40 C-84,-10 -82,10 -76,26 L-70,-6 Z M80,-40 C84,-10 82,10 76,26 L70,-6 Z" fill="#2a2620"/>'
        s += strands(random.Random(4), [(-78, -40, -80, -10, -74, 20), (78, -40, 80, -10, 74, 20)], 8, "#a8a49c", (1.5, 3), (0.5, 0.9), 4)
    if cap:
        s += kepi(rim, "#2a2e1c" if not ghost else "#2a3444")
    return s


def medal(x, y, k=1.0, ribbon=("#1a6a3a", "#f0f0f0", "#b81a2a"), metal="#d4a84a", star=False):
    s = f'<g transform="translate({x},{y}) scale({k})">'
    w = 40
    for i, c in enumerate(ribbon):
        s += f'<path d="M{-w/2 + i*w/3:.1f},-80 L{-w/2 + (i+1)*w/3:.1f},-80 L{-w/2 + (i+1)*w/3 - 4:.1f},-10 L{-w/2 + i*w/3 - 4:.1f},-10 Z" fill="{c}"/>'
    s += '<rect x="-22" y="-84" width="44" height="8" fill="#8a7030"/>'
    if star:
        pts_ = []
        for i in range(10):
            a = -math.pi / 2 + i * math.pi / 5; rr = 34 if i % 2 == 0 else 15
            pts_.append(f"{math.cos(a)*rr:.1f},{20+math.sin(a)*rr:.1f}")
        s += f'<polygon points="{" ".join(pts_)}" fill="{metal}" stroke="#6a5020" stroke-width="2"/>'
    else:
        s += f'<circle cx="0" cy="18" r="28" fill="{metal}" stroke="#6a5020" stroke-width="3"/><circle cx="0" cy="18" r="18" fill="none" stroke="#fff4c0" stroke-width="2" opacity="0.6"/>'
    s += f'<path d="M-14,4 A24,24 0 0 1 10,-4" stroke="#fff8d8" stroke-width="4" fill="none" opacity="0.7"/>'
    s += '</g>'
    return s


def soldier_body(g, rim, uni=OLIVE, medals=True, sk=SK_SOL, open_collar=False):
    s = (f'<defs>{grad_lin(g+"c", [(0, uni[0], 1), (0.6, uni[1], 1), (1, uni[2], 1)], -380, 0, 380, 0)}</defs>')
    s += f'<path d="M-52,40 C-54,110 -62,150 -72,190 L72,190 C62,150 54,110 52,40 Z" fill="{sk["shadow"]}"/>'
    s += f'<path d="M-90,160 C-220,190 -340,250 -380,660 L380,660 C340,250 220,190 90,160 Z" fill="url(#{g}c)"/>'
    if not open_collar:
        s += f'<path d="M-90,150 L-80,210 L0,230 L80,210 L90,150 C40,170 -40,170 -90,150 Z" fill="{uni[1]}"/>'
        s += '<path d="M-80,206 L0,226 L80,206" stroke="#0a0a06" stroke-width="4" fill="none"/>'
        s += '<rect x="-74" y="176" width="22" height="16" fill="#c9a24a" opacity="0.8"/><rect x="52" y="176" width="22" height="16" fill="#c9a24a" opacity="0.8"/>'
    s += '<path d="M0,230 L0,660" stroke="#0a0a06" stroke-width="5"/>'
    for b in range(6):
        s += f'<circle cx="14" cy="{270+b*66}" r="9" fill="#c9a24a"/><circle cx="11" cy="{267+b*66}" r="3" fill="#fff4c0"/>'
    # pockets with flaps
    for side in (-1, 1):
        s += f'<path d="M{side*60},330 L{side*220},330 L{side*214},470 L{side*66},470 Z" fill="#000" opacity="0.18"/>'
        s += f'<path d="M{side*56},320 L{side*224},320 L{side*220},360 L{side*140},376 L{side*60},360 Z" fill="{uni[0]}" opacity="0.8"/>'
    # folds
    for d in ["M-260,300 Q-240,460 -270,660", "M240,300 Q220,460 250,660", "M-120,480 Q-100,560 -140,660", "M140,480 Q120,560 150,660"]:
        s += f'<path d="{d}" stroke="#0a0c06" stroke-width="10" fill="none" opacity="0.5" filter="url(#blur1)"/>'
    s += '<path d="M-90,160 C-160,170 -230,190 -300,240 L-280,262 C-220,220 -150,196 -86,186 Z" fill="#0a0c06" opacity="0.3"/>'
    if medals:
        s += medal(150, 300, 1.0) + medal(205, 304, 1.0, ("#b81a2a", "#e8c84a", "#b81a2a"), "#c0c0c8") + medal(95, 302, 1.0, ("#1a3a8a", "#f0f0f0", "#1a3a8a"), star=True)
    if rim:
        s += f'<path d="M-90,160 C-220,190 -340,250 -380,660" stroke="{rim}" stroke-width="6" fill="none" opacity="0.55" filter="url(#blur1)"/>'
    return s


def soldier_bust(x, y, k=1.0, rim="#9fc2e8", medals=True, ghost=False, **hk):
    g = uid("sb")
    uni = OLIVE if not ghost else ("#141c28", "#2a3a50", "#405670")
    body = soldier_body(g, rim, uni, medals, SK_GHO if ghost else SK_SOL, open_collar=hk.get("ruin", False))
    return bust_frame(body, soldier_head(rim=rim, ghost=ghost, **hk), x, y, k)


def kid_hair(seed=5):
    r = random.Random(seed)
    s = ('<path d="M-82,-20 C-96,-96 -62,-150 0,-156 C66,-152 98,-100 84,-20 C80,-52 70,-74 50,-86 C40,-70 20,-62 -4,-70 '
         'C-20,-58 -44,-60 -60,-76 C-72,-60 -78,-40 -82,-20 Z" fill="#0c0806"/>')
    for i in range(9):  # fringe tufts
        x = -60 + i * 15
        s += f'<path d="M{x},-90 q{r.uniform(-6,6):.0f},{r.uniform(20,34):.0f} {r.uniform(4,12):.0f},{r.uniform(26,40):.0f}" stroke="#0c0806" stroke-width="12" fill="none" stroke-linecap="round"/>'
    s += strands(r, [(-60, -130, -10, -156, 50, -130)], 8, "#3a2a20", (1.5, 2.5), (0.3, 0.6), 6)
    s += '<path d="M10,-152 q10,-26 26,-30" stroke="#0c0806" stroke-width="10" fill="none" stroke-linecap="round"/>'  # cowlick
    return s


def kid_head(look=0.0, turn=0.0, smile=0.7, lids=0.0, rim="#ffd27a", fear=False, wonder=False, ghost=False):
    sk = SK_GHO if ghost else SK_KID
    s = '<g transform="scale(0.92,0.88)">'
    s += head(look=look, smile=(-0.4 if fear else smile), lids=lids, rim=rim, turn=turn, sk=sk, headwrap=False, earring=False,
              lips=("#9a5848", "#b06a58"), iris="#1a0e08" if not ghost else "#e8f4ff", brow_w=0.7, neck=True)
    s += f'<ellipse cx="-44" cy="30" rx="22" ry="14" fill="#d0705a" opacity="{0.0 if ghost else 0.28}" filter="url(#blur1)"/><ellipse cx="44" cy="30" rx="22" ry="14" fill="#d0705a" opacity="{0.0 if ghost else 0.28}" filter="url(#blur1)"/>'
    if wonder:
        s += '<ellipse cx="0" cy="76" rx="12" ry="14" fill="#3a1410"/>'
    s += '<ellipse cx="-80" cy="-6" rx="14" ry="26" fill="%s"/><ellipse cx="80" cy="-6" rx="14" ry="26" fill="%s"/>' % (sk["shadow"], sk["base"])
    s += kid_hair()
    s += '</g>'
    return s


def kid_body(g, rim, ghost=False):
    sk = SK_GHO if ghost else SK_KID
    shirt = ("#5a5040", "#a89878", "#c8b898") if not ghost else ("#2a3a50", "#5a6a80", "#8a9ab0")
    s = (f'<defs>{grad_lin(g+"s", [(0, shirt[0], 1), (0.6, shirt[1], 1), (1, shirt[2], 1)], -300, 0, 300, 0)}</defs>')
    s += f'<path d="M-46,40 C-46,100 -50,130 -60,170 L60,170 C50,130 46,100 46,40 Z" fill="{sk["shadow"]}"/>'
    s += f'<path d="M-70,150 C-180,180 -260,230 -280,660 L280,660 C260,230 180,180 70,150 Z" fill="url(#{g}s)"/>'
    s += f'<path d="M-70,150 L-30,230 L0,190 L30,230 L70,150 C40,164 -40,164 -70,150 Z" fill="{shirt[2]}"/>'
    for i in range(6):  # stripes
        s += f'<path d="M-270,{300+i*60} C-100,{290+i*60} 100,{290+i*60} 270,{300+i*60}" stroke="{"#5a6a8a" if not ghost else "#a0b0c8"}" stroke-width="10" fill="none" opacity="0.45"/>'
    for side in (-1, 1):  # suspenders
        s += f'<path d="M{side*120},180 C{side*110},350 {side*100},500 {side*96},660" stroke="#2a1a10" stroke-width="26" fill="none"/>'
    s += '<path d="M-180,400 Q-150,430 -120,420 M180,400 Q150,430 120,420" stroke="#000" stroke-width="10" fill="none" opacity="0.3"/>'
    if rim:
        s += f'<path d="M-70,150 C-180,180 -260,230 -280,660" stroke="{rim}" stroke-width="6" fill="none" opacity="0.55" filter="url(#blur1)"/>'
    return s


def kid_bust(x, y, k=1.0, rim="#ffd27a", ghost=False, **hk):
    g = uid("kb")
    return bust_frame(kid_body(g, rim, ghost), kid_head(rim=rim, ghost=ghost, **hk), x, y, k)


def trompo(x, y, k=1.0, lying=False, spin=False, light="#ffcf8a", col="#9a3a1a"):
    rot = 78 if lying else (8 if spin else 0)
    s = f'<g transform="translate({x},{y}) rotate({rot}) scale({k})">'
    s += f'<path d="M0,0 L-6,-40 C-60,-60 -80,-110 -70,-150 C-60,-190 60,-190 70,-150 C80,-110 60,-60 6,-40 Z" fill="{col}"/>'
    for i, c in enumerate(["#e8c060", "#2a6a4a", "#e8c060"]):
        yy = -150 + i * 26
        s += f'<path d="M{-70+i*6},{yy} C-30,{yy+12} 30,{yy+12} {70-i*6},{yy}" stroke="{c}" stroke-width="9" fill="none"/>'
    s += '<path d="M-20,-188 C-14,-210 14,-210 20,-188 Z" fill="#5a2a10"/>'
    s += '<path d="M0,0 L0,14" stroke="#b8b8c0" stroke-width="7"/>'
    s += f'<path d="M50,-180 C70,-150 72,-110 52,-70" stroke="{light}" stroke-width="6" fill="none" opacity="0.5"/>'
    if spin:
        s += '<ellipse cx="0" cy="-130" rx="96" ry="22" fill="none" stroke="#fff" stroke-width="3" opacity="0.25"/><ellipse cx="0" cy="-110" rx="110" ry="26" fill="none" stroke="#fff" stroke-width="2" opacity="0.15"/>'
    s += '</g>'
    if spin:
        s += f'<ellipse cx="{x}" cy="{y+14*k}" rx="{60*k:.0f}" ry="{10*k:.0f}" fill="#000" opacity="0.4"/>'
    return s


def cordel(x, y, k=1.0):
    return f'<path d="M{x},{y} c{60*k:.0f},{-20*k:.0f} {120*k:.0f},{30*k:.0f} {180*k:.0f},{0:.0f} s{90*k:.0f},{40*k:.0f} {160*k:.0f},{10*k:.0f}" stroke="#d8c8a0" stroke-width="{6*k:.1f}" fill="none"/>'


# silhouettes (feet at 0,0; height ~1000 at k=1)
def soldier_sil(rim="#a8c8ff", fill=SIL, bow=False, walk=0.0, raise_hand=False, kneel=False, rim_op=0.8):
    hx = 30 if bow else 0; hy = -840 if bow else -880
    s = ""
    if kneel:
        s += '<path d="M-80,-400 L-90,-180 L-170,-170 L-180,0 L-90,0 L-60,-120 L70,-120 L110,0 L200,0 L150,-200 L90,-400 Z"/>'
        hx, hy = 40, -620
        s += f'<path d="M-100,-660 C-120,-560 -110,-480 -90,-400 L100,-400 C110,-480 118,-560 90,-660 C40,-700 -60,-700 -100,-660 Z"/>'
        s += f'<path d="M80,-620 C140,-580 160,-540 150,-500 L120,-520 Z"/>'
    else:
        st = walk * 60
        s += f'<path d="M-70,-460 L{-80-st:.0f},0 L{-20-st:.0f},0 L-10,-380 L10,-380 L{30+st:.0f},0 L{90+st:.0f},0 L70,-460 Z"/>'
        s += f'<path d="M{-100-st:.0f},0 L{-10-st:.0f},0 L{-10-st:.0f},-40 L{-90-st:.0f},-40 Z M{20+st:.0f},0 L{110+st:.0f},0 L{110+st:.0f},-40 L{30+st:.0f},-40 Z"/>'  # boots
        s += '<path d="M-120,-800 C-140,-680 -110,-560 -90,-440 L90,-440 C110,-560 140,-680 120,-800 C60,-830 -60,-830 -120,-800 Z"/>'
        s += '<path d="M-96,-470 L96,-470 L96,-440 L-96,-440 Z" fill="#000"/>'
        if raise_hand:
            s += '<path d="M110,-790 C170,-860 200,-950 210,-1040 L250,-1030 C250,-930 220,-830 150,-760 Z"/><ellipse cx="232" cy="-1060" rx="38" ry="50"/>'
            s += '<path d="M-110,-780 C-150,-680 -160,-600 -150,-520 L-120,-520 C-120,-600 -110,-680 -86,-740 Z"/>'
        else:
            s += '<path d="M-112,-790 C-150,-680 -160,-600 -150,-500 L-118,-500 C-118,-600 -110,-680 -88,-740 Z M112,-790 C150,-680 160,-600 150,-500 L118,-500 C118,-600 110,-680 88,-740 Z"/>'
    # head + kepi
    s += f'<ellipse cx="{hx}" cy="{hy}" rx="62" ry="72"/>'
    s += f'<path d="M{hx-66},{hy-30} C{hx-70},{hy-90} {hx-40},{hy-120} {hx},{hy-122} C{hx+40},{hy-120} {hx+70},{hy-90} {hx+66},{hy-30} Z"/>'
    s += f'<path d="M{hx-10},{hy-34} C{hx+30},{hy-30} {hx+80},{hy-26} {hx+108},{hy-12} L{hx+60},{hy-10} Z"/>'
    s += f'<path d="M{hx-40},{hy+72} L{hx+40},{hy+72} L{hx+44},{hy+100} L{hx-44},{hy+100} Z"/>'
    out = f'<g fill="{fill}">{s}</g>'
    if rim:
        out += (f'<g fill="none" stroke="{rim}" stroke-width="7" opacity="{rim_op}" filter="url(#blur1)">'
                f'<path d="M{hx+66},{hy-30} C{hx+70},{hy-90} {hx+40},{hy-120} {hx},{hy-122}"/>'
                f'<path d="M{hx+62},{hy} C{hx+60},{hy+40} {hx+40},{hy+60} {hx+20},{hy+70}"/>'
                + ('' if kneel else '<path d="M120,-800 C140,-680 110,-560 90,-440"/><path d="M150,-760 C160,-640 160,-580 150,-500"/>') + '</g>')
    return out


def kid_sil(rim="#a8c8ff", fill=SIL, girl=False, reach=False, trompo_hand=False, rim_op=0.8):
    s = ""
    if girl:
        s += '<path d="M-130,-60 C-110,-200 -80,-330 -60,-420 L60,-420 C80,-330 110,-200 130,-60 Z"/>'
        s += '<path d="M-36,-60 L-40,0 L-10,0 L-8,-60 Z M8,-60 L10,0 L40,0 L36,-60 Z"/>'
        s += '<path d="M-60,-420 C-70,-470 -60,-500 0,-510 C60,-500 70,-470 60,-420 Z"/>'
        s += '<path d="M-56,-560 C-90,-500 -96,-420 -80,-360 L-56,-420 Z M56,-560 C90,-500 96,-420 80,-360 L56,-420 Z"/>'
    else:
        s += '<path d="M-50,-260 L-56,0 L-14,0 L-6,-200 L6,-200 L14,0 L56,0 L50,-260 Z"/>'
        s += '<path d="M-64,-280 L64,-280 L60,-200 L-60,-200 Z"/>'  # short pants
        s += '<path d="M-70,-500 C-80,-420 -70,-340 -64,-270 L64,-270 C70,-340 80,-420 70,-500 C30,-516 -30,-516 -70,-500 Z"/>'
    if reach:
        s += '<path d="M60,-490 C110,-470 150,-440 180,-400 L160,-384 C130,-420 100,-440 56,-450 Z"/>'
        s += '<path d="M-64,-490 C-90,-430 -96,-380 -90,-320 L-70,-320 C-72,-380 -66,-430 -48,-470 Z"/>'
    else:
        s += '<path d="M-66,-490 C-92,-430 -98,-380 -92,-300 L-70,-300 C-72,-380 -66,-430 -50,-470 Z M66,-490 C92,-430 98,-380 92,-300 L70,-300 C72,-380 66,-430 50,-470 Z"/>'
    s += '<ellipse cx="0" cy="-580" rx="58" ry="66"/>'
    s += '<path d="M-60,-600 C-60,-660 -20,-660 0,-650 C20,-662 60,-656 62,-596 C50,-620 30,-630 0,-628 C-30,-630 -50,-620 -60,-600 Z"/>'
    out = f'<g fill="{fill}">{s}</g>'
    if trompo_hand:
        out += trompo(92, -260, 0.32, light=rim or "#ffcf8a")
    if rim:
        out += (f'<g fill="none" stroke="{rim}" stroke-width="6" opacity="{rim_op}" filter="url(#blur1)"><path d="M58,-600 C62,-560 52,-530 30,-516"/>'
                f'<path d="M70,-500 C80,-420 70,-340 64,-270"/></g>')
    return out


def shadows_wall(kind="raise", mood="blood"):
    """shadow-theatre on an adobe wall: the big shadow of the soldier and the small one of the child"""
    s = '<rect width="2400" height="1350" fill="#5a2a1c"/>' if mood == "blood" else '<rect width="2400" height="1350" fill="#3a3a48"/>'
    s += '<rect width="2400" height="1350" fill="#000" filter="url(#plaster)" opacity="0.5"/>'
    s += glow(700, 1100, 1300, "red" if mood == "blood" else "warm", 0.5)
    s += '<path d="M0,1180 L2400,1180 L2400,1350 L0,1350 Z" fill="#140806"/>'
    s += f'<g opacity="0.88" filter="url(#blur1)">{place(soldier_sil(rim=None, fill="#0a0202", raise_hand=(kind == "raise")), 1050, 1200, 1.08)}'
    s += f'{place(kid_sil(rim=None, fill="#0a0202", reach=True), 1560, 1200, 0.95, flip=True)}</g>'
    return s


def write(names):
    for n in names:
        if n in ART:
            open(os.path.join(A, n + ".svg"), "w", encoding="utf-8").write(ART[n]())
    print("svg written:", len([n for n in names if n in ART]))


# =========================================================== scenes
GROUND = lambda z: P(0, 0.62, z)[1]

@art
def alley_night(): return S(callejon("night"), QM.fog_band(1180, 0.28))
@art
def alley_deep(): return S(callejon("night", niche=False, seed=8), QM.fog_band(1150, 0.35, 5), '<rect width="2400" height="1350" fill="#020610" opacity="0.15"/>')
@art
def alley_dusk(): return S(callejon("dusk", seed=5, lamp_on=False), QM.fog_band(1180, 0.2, 7))
@art
def alley_dawn(): return S(callejon("dawn", seed=6, lamp_on=False, door_lit=False), QM.fog_band(1160, 0.35, 9))
@art
def alley_day(): return S(callejon("day", seed=4, lamp_on=False, door_lit=False))
@art
def alley_today(): return S(callejon("today", seed=12, lamp_on=False, door_lit=False, plaque=True))
@art
def title_bg(): return S(callejon("night", seed=14, niche=True), '<rect width="2400" height="1350" fill="#000" opacity="0.4"/>', QM.fog_band(1100, 0.4, 3))
@art
def students():
    s = callejon("night", seed=16, niche=True)
    s += '<rect width="2400" height="1350" fill="#000" opacity="0.25"/>'
    for i, (x, k, f) in enumerate([(820, 0.42, False), (1000, 0.46, True), (1240, 0.44, False), (1440, 0.4, True)]):
        y = 1180
        s += f'<path d="M{x+30},{y-330*k/0.44} L{x+600 if not f else x-600},{y-120} L{x+600 if not f else x-600},{y+80} Z" fill="#fff8d8" opacity="0.10" filter="url(#blur2)"/>'
        s += place(woman_full(rim=MOONRIM) if i % 2 else man_full(hat=False, cape=False, rim=MOONRIM), x, y, k, flip=f)
    return S(s, QM.fog_band(1200, 0.3, 4))

@art
def cobbles_night():
    s = sky("#030812", "#0a1424") + quad((0, 600), (2400, 600), (2400, 1350), (0, 1350), "#0a0a0e")
    r = random.Random(3)
    for row in range(16):
        y = 620 + row ** 1.6 * 9; h = 10 + row * 4.2
        for i in range(int(40 - row * 1.5)):
            w = 2400 / (40 - row * 1.5)
            x = i * w + r.uniform(-w * 0.2, w * 0.2) + (w / 2 if row % 2 else 0)
            s += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{w*0.44:.0f}" ry="{h*0.55:.0f}" fill="#16161e"/><ellipse cx="{x:.0f}" cy="{y-h*0.18:.0f}" rx="{w*0.3:.0f}" ry="{h*0.25:.0f}" fill="#5a6478" opacity="0.28"/>'
    s += '<rect x="0" y="0" width="2400" height="640" fill="#14141c"/><rect x="0" y="0" width="2400" height="640" fill="#000" filter="url(#plaster)" opacity="0.5"/>'
    s += '<rect x="0" y="560" width="2400" height="80" fill="#0a0a10"/>'
    s += glow(1200, 300, 900, "moon", 0.35)
    return S(s)

@art
def cobbles_dusk(): return S(ART["cobbles_night"](), '<rect width="2400" height="1350" fill="#2a1a2a" opacity="0.25"/>')

@art
def trompo_day():
    s = ART["cobbles_night"]().replace('fill="#16161e"', 'fill="#6a5e50"').replace('fill="#14141c"', 'fill="#b8864a"').replace('fill="#0a0a0e"', 'fill="#3a3228"')
    s += '<rect width="2400" height="1350" fill="#ffd090" opacity="0.18"/>'
    s += trompo(1150, 1060, 2.4, lying=True, light="#fff0c0") + cordel(1350, 1110, 1.6)
    for x, c in [(700, "#3a8ac8"), (760, "#c83a3a"), (1720, "#3ac86a")]:
        s += f'<circle cx="{x}" cy="1150" r="22" fill="{c}" opacity="0.9"/><circle cx="{x-7}" cy="1143" r="7" fill="#fff" opacity="0.7"/>'
    return s.replace('</svg>', '') + '</svg>' if False else _fix_end(s)

@art
def trompo_still():
    s = ART["cobbles_night"]()
    s = s[:-6] if s.endswith('</svg>') else s
    return S(ART["cobbles_night"]().split('</svg>')[0].split('>', 1)[1] if False else '', ) if False else _trompo_still()

def _fix_end(s):
    body = s.replace('</svg>', '')
    return body + '</svg>'

def _trompo_still():
    base = ART["cobbles_night"]()
    extra = trompo(1500, 1000, 2.0, lying=True, light="#a8c8ff") + '<ellipse cx="1400" cy="1030" rx="260" ry="30" fill="#000" opacity="0.4"/>'
    return base.replace('</svg>', extra + '<rect width="2400" height="1350" fill="#04081a" opacity="0.2"/></svg>')

@art
def l_trompo(): return S(trompo(1200, 1010, 1.6, spin=True, light="#a8c8ff"))

@art
def niche_close(): return S(_niche_close(True))
@art
def niche_dark(): return S(_niche_close(False))
def _niche_close(lit=True, soldier=False, toys=True):
    s = '<rect width="2400" height="1350" fill="#4a4640"/>'
    r = random.Random(4)
    for row in range(9):  # stone blocks
        for i in range(8):
            x = i * 320 + (160 if row % 2 else 0) - 100; y = row * 160
            s += f'<rect x="{x+6}" y="{y+6}" width="308" height="148" rx="14" fill="{r.choice(["#5a5650", "#504c46", "#605a52"])}"/>'
    s += '<rect width="2400" height="1350" fill="#000" filter="url(#plaster)" opacity="0.55"/>'
    # niche
    s += '<path d="M820,1060 L820,420 C820,240 1000,140 1200,140 C1400,140 1580,240 1580,420 L1580,1060 Z" fill="#120e0c"/>'
    s += '<path d="M820,1060 L820,420 C820,240 1000,140 1200,140 C1400,140 1580,240 1580,420 L1580,1060" stroke="#2a4a8a" stroke-width="44" fill="none"/>'
    for i in range(18):  # talavera tiles on the frame
        t = i / 17; a = math.pi * (1 - t)
        x = 1200 + math.cos(a) * 380; y = 420 - math.sin(a) * 280 if True else 0
        s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="10" fill="#e8e0c8" opacity="0.8"/>'
    for y in range(460, 1060, 60):
        s += f'<circle cx="820" cy="{y}" r="10" fill="#e8e0c8" opacity="0.8"/><circle cx="1580" cy="{y}" r="10" fill="#e8e0c8" opacity="0.8"/>'
    s += '<path d="M760,1060 L1640,1060 L1680,1120 L720,1120 Z" fill="#8a8274"/><path d="M720,1120 L1680,1120 L1680,1150 L720,1150 Z" fill="#3a362e"/>'
    s += virgin(1200, 1030, 1.6, 1.0 if lit else 0.15, dark=not lit)
    s += veladora(1020, 1060, 1.2, lit) + veladora(VELAC_XY[0], 1062, 1.35, lit, "#e8e0d0") + veladora(1380, 1060, 1.2, lit, "#2a6a3a")
    # cempasuchil + toys
    for x in (900, 1500):
        for j in range(5):
            fx_, fy = x + r.uniform(-50, 50), 1040 - r.uniform(0, 60)
            s += f'<circle cx="{fx_:.0f}" cy="{fy:.0f}" r="22" fill="{"#e88a10" if lit else "#4a3010"}"/><circle cx="{fx_:.0f}" cy="{fy:.0f}" r="10" fill="{"#c86a00" if lit else "#3a2008"}"/>'
    if toys:
        s += trompo(1110, 1112, 0.34, lying=True, light="#ffcf8a") + '<circle cx="1290" cy="1100" r="10" fill="#3a8ac8"/><circle cx="1316" cy="1104" r="10" fill="#c83a3a"/>'
    if lit:
        s += glow(1200, 900, 900, "warm", 0.45)
    else:
        s += '<rect width="2400" height="1350" fill="#02040a" opacity="0.55"/>' + glow(1200, 400, 1000, "moon", 0.25)
    s += '<path d="M0,1150 L2400,1150 L2400,1350 L0,1350 Z" fill="#14120e"/>'
    if soldier:
        s += place(soldier_sil(rim="#a8c8ff", fill="#03050a", bow=True), 1900, 1340, 1.15)
        s += '<rect width="2400" height="1350" fill="#04081a" opacity="0.2"/>'
    return s

@art
def niche_soldier(): return S(_niche_close(True, soldier=True))
@art
def niche_toys(): return S(f'<g transform="translate(-1800,-1700) scale(2.5)">{_niche_close(True)}</g>')
@art
def kneel_niche():
    s = _niche_close(True, toys=False)
    s += place(soldier_sil(rim="#ffcf8a", fill="#050403", kneel=True, rim_op=0.9), 1780, 1330, 1.25, flip=True)
    return S(s)
@art
def veladoras():
    s = '<rect width="2400" height="1350" fill="#0c0806"/>' + glow(1200, 800, 1400, "warm", 0.6)
    r = random.Random(6)
    for row in range(4):
        for i in range(12 - row):
            x = 160 + i * (2080 / (11 - row)) + r.uniform(-30, 30) if (11 - row) else 1200
            y = 760 + row * 170
            k = 1.0 + row * 0.45
            s += glow(x, y - 90 * k, 160 * k, "warm", 0.5) + veladora(x, y, k, True, r.choice(["#c8202a", "#e8e0d0", "#2a6a3a", "#c8a020"]))
    s += virgin(1200, 640, 0.9, 0.7)
    return S(s)
@art
def l_vela_glow(): return S(glow(NICHE_XY[0], NICHE_XY[1], 340, "warm", 0.5))
@art
def l_vela_close(): return S(glow(VELAC_XY[0], VELAC_XY[1] - 120, 950, "warm", 0.45))
@art
def l_lamp_glow(): return S(glow(LAMP_XY[0], LAMP_XY[1] + 20, 560, "warm", 0.5))
@art
def l_candle_glow(): return S(glow(CANDLE_XY[0], CANDLE_XY[1] - 240, 900, "warm", 0.4))
@art
def l_fog(): return S(clouds(18, 900, 1400, 31, "#b0c4d8", (0.08, 0.2), (300, 700), (60, 140)))
@art
def l_branches():
    s = canopy(1900, -40, 700, 220, 41, "#7a9cc4", n=260, fruit=9, lit=0.3, leaf=1.5) + canopy(300, -60, 420, 150, 42, "#7a9cc4", n=120, fruit=3, lit=0.3, leaf=1.5)
    return S(s)
@art
def l_child_ghost():
    z = 3.2; y = GROUND(z)
    return S(f'<g filter="url(#ghost)" opacity="0.7">{place(kid_sil(rim="#e8f4ff", fill="#8aa4c4", trompo_hand=True), 1330, y, 0.38)}</g>', glow(1330, y - 120, 160, "moon", 0.5))
@art
def l_soldier_ghost():
    z = 4.0; y = GROUND(z)
    s = place(soldier_sil(rim="#cfe0ff", fill="#02030a"), 1330, y, 0.31)
    s += f'<circle cx="1323" cy="{y-275:.0f}" r="4" fill="#e8f4ff" filter="url(#glow)"/><circle cx="1341" cy="{y-275:.0f}" r="4" fill="#e8f4ff" filter="url(#glow)"/>'
    return S(s)
@art
def l_walker(): return S(place(man_full(hat=False, cape=False, walk=0.3, rim=MOONRIM, fill="#020305"), 1160, 1420, 1.0))
@art
def l_soldier_walk(): return S(place(soldier_sil(rim="#fff0c0", fill="#14160c", walk=0.4), 760, GROUND(2.2), 0.48))
@art
def l_child_follow(): return S(place(kid_sil(rim="#fff0c0", fill="#1a140c", trompo_hand=True), 420, GROUND(1.9), 0.4))
@art
def l_lanterns():
    s = ""
    for i, x in enumerate([500, 760, 1020, 1300]):
        y = 1260; k = 0.55 - i * 0.03
        s += place(woman_full(rebozo_head=True, rim="#ffcf8a") if i == 0 else man_full(hat=True, cape=False, lantern=True, rim="#ffcf8a"), x, y, k)
        s += glow(x + 90 * k / 0.55, y - 430 * k / 0.55, 170, "warm", 0.7)
    return S(s)

# ---------------------------------------------------------- characters scenes
@art
def soldier_portrait(): return S(portrait_bg("candle"), soldier_bust(1200, 560, 1.75, rim=WARM, look=-0.15, lids=0.4), candle_at(CANDLE_XY[0], CANDLE_XY[1] + 500, 170))
@art
def soldier_cold(): return S(portrait_bg("moon"), soldier_bust(1200, 560, 1.75, rim=MOONRIM, look=0.5, cold=True), '<rect width="2400" height="1350" fill="#04081a" opacity="0.25"/>')
@art
def soldier_ruin(): return S(portrait_bg("moon"), soldier_bust(1200, 560, 1.75, rim=MOONRIM, look=-0.3, ruin=True, cap=False, medals=False), '<rect width="2400" height="1350" fill="#04081a" opacity="0.3"/>')
@art
def soldier_shadow():
    s = portrait_bg("moon") + soldier_bust(1200, 560, 1.75, rim="#cfe0ff", look=0.2, cold=True)
    s += '<defs><linearGradient id="shd" x1="0" y1="0" x2="1" y2="0"><stop offset="0.3" stop-color="#000" stop-opacity="0.3"/><stop offset="0.6" stop-color="#000" stop-opacity="0.85"/><stop offset="1" stop-color="#000" stop-opacity="0.95"/></linearGradient></defs>'
    s += '<rect x="0" y="0" width="2400" height="1350" fill="url(#shd)"/>'
    return S(s)
@art
def soldier_ghost_close():
    s = '<rect width="2400" height="1350" fill="#02040a"/>' + glow(1200, 500, 900, "moon", 0.4)
    s += f'<g filter="url(#ghost)">{soldier_bust(1200, 560, 1.75, rim="#e8f4ff", ghost=True, cold=True)}</g>'
    s += '<rect width="2400" height="1350" fill="#04081a" opacity="0.35"/>'
    s += '<circle cx="1144" cy="502" r="16" fill="#e8f4ff" filter="url(#glow)"/><circle cx="1256" cy="502" r="16" fill="#e8f4ff" filter="url(#glow)"/>'
    return S(s)
@art
def ghost_flash():
    s = '<rect width="2400" height="1350" fill="#c8d8e8"/>'
    s += f'<g filter="url(#ghost)">{soldier_bust(1200, 600, 2.3, rim="#ffffff", ghost=True, cold=True)}</g>'
    s += '<rect width="2400" height="1350" fill="#000" opacity="0.15"/>'
    s += '<circle cx="1126" cy="524" r="22" fill="#000"/><circle cx="1274" cy="524" r="22" fill="#000"/>'
    return S(s)
@art
def soldier_flash():
    s = _niche_close(False) + '<rect width="2400" height="1350" fill="#c8d8ff" opacity="0.35"/>'
    s += place(soldier_sil(rim="#ffffff", fill="#000", bow=False), 1700, 1360, 1.35)
    s += '<circle cx="1690" cy="178" r="12" fill="#fff" filter="url(#glow)"/><circle cx="1730" cy="178" r="12" fill="#fff" filter="url(#glow)"/>'
    return S(s)
@art
def medals_close():
    g = uid("mc")
    s = f'<defs>{grad_lin(g, [(0, OLIVE[0], 1), (0.5, OLIVE[1], 1), (1, OLIVE[2], 1)], 0, 0, 2400, 0)}</defs><rect width="2400" height="1350" fill="url(#{g})"/>'
    s += '<rect width="2400" height="1350" fill="#000" filter="url(#plaster)" opacity="0.35"/>'
    s += '<path d="M600,0 L600,1350" stroke="#0a0a06" stroke-width="10"/>'
    for b in range(4):
        s += f'<circle cx="640" cy="{150+b*340}" r="36" fill="#c9a24a"/><circle cx="628" cy="{138+b*340}" r="12" fill="#fff4c0"/>'
    s += '<path d="M900,620 L2000,620 L1980,1100 L920,1100 Z" fill="#000" opacity="0.2"/><path d="M880,600 L2020,600 L2000,760 L1450,820 L900,760 Z" fill="#1c2014" opacity="0.7"/>'
    s += medal(1100, 420, 3.4, ("#1a3a8a", "#f0f0f0", "#1a3a8a"), star=True) + medal(1450, 430, 3.4) + medal(1800, 440, 3.4, ("#b81a2a", "#e8c84a", "#b81a2a"), "#c0c0c8")
    s += glow(1450, 500, 900, "warm", 0.35)
    for d in ["M300,0 Q340,600 260,1350", "M2200,0 Q2160,700 2240,1350"]:
        s += f'<path d="{d}" stroke="#05060a" stroke-width="40" fill="none" opacity="0.5" filter="url(#blur2)"/>'
    return S(s)
@art
def hands_shake():
    s = portrait_bg("candle") + '<rect width="2400" height="1350" fill="#000" opacity="0.2"/>'
    sk = SK_SOL
    for side in (-1, 1):
        x = 1200 + side * 330
        s += f'<g transform="translate({1200 + side * 420},760) scale({side*1.8},1.8)">'
        s += f'<path d="M-500,120 L-120,40 L-110,200 L-500,300 Z" fill="{OLIVE[1]}"/><path d="M-140,30 L-110,210" stroke="#c9a24a" stroke-width="8"/>'
        s += (f'<path d="M-120,40 C-60,10 20,0 80,20 C140,40 190,60 210,100 C220,130 200,150 170,140 C150,134 130,128 110,130 '
              f'C150,150 180,180 180,210 C178,236 150,240 130,226 C110,210 90,196 70,196 C60,214 40,228 10,226 C-40,222 -90,214 -110,200 Z" fill="{sk["base"]}"/>')
        for j in range(4):
            s += f'<path d="M{60+j*30},{60+j*20} C{110+j*20},{80+j*20} {150+j*10},{100+j*24} {170},{120+j*30}" stroke="{sk["deep"]}" stroke-width="4" fill="none" opacity="0.5"/>'
        s += f'<path d="M-40,60 C0,80 40,90 90,70" stroke="{sk["shadow"]}" stroke-width="6" fill="none" opacity="0.7"/>'
        if side == 1:
            s += '<path d="M-60,120 L40,150" stroke="#6a2a20" stroke-width="7" opacity="0.7"/>'  # scar
        s += f'<path d="M-120,40 C-60,10 20,0 80,20 C140,40 190,60 210,100" stroke="#ffd29a" stroke-width="5" fill="none" opacity="0.6"/></g>'
    return S(s)
@art
def hand_raise(): return S(shadows_wall("raise", "blood"))
@art
def red_flash(): return S(f'<g transform="translate(-900,-500) scale(1.7)">{shadows_wall("raise", "blood")}</g>', '<rect width="2400" height="1350" fill="#ff2010" opacity="0.25"/>')
@art
def child_portrait(): return S(portrait_bg("candle").replace("#0c0806", "#3a2a1a"), glow(1700, 300, 900, "warm", 0.5), kid_bust(1200, 600, 1.75, rim="#ffd27a", look=0.1, smile=0.8))
@art
def child_look(): return S(portrait_bg("candle").replace("#0c0806", "#2a2420"), glow(1800, 200, 900, "warm", 0.45), kid_bust(1200, 620, 1.75, rim="#ffd27a", look=0.6, turn=0.15, smile=0.4, wonder=True))

@art
def girl_ghost():
    s = callejon("night", seed=18, niche=True) + '<rect width="2400" height="1350" fill="#02040a" opacity="0.3"/>'
    y = GROUND(2.6)
    s += f'<g filter="url(#ghost)" opacity="0.8">{place(kid_sil(rim="#ffffff", fill="#c8d8ec", girl=True), 1150, y, 0.5)}</g>' + glow(1150, y - 160, 260, "moon", 0.6)
    s += f'<text x="2280" y="1280" font-family="Oswald" font-size="64" fill="#e8f4ff" text-anchor="end" opacity="0.7">2:47 a. m.</text>'
    return S(s, QM.fog_band(1180, 0.35, 21))
@art
def devil_wall():
    s = '<rect width="2400" height="1350" fill="#3a1410"/><rect width="2400" height="1350" fill="#000" filter="url(#plaster)" opacity="0.55"/>' + glow(500, 900, 1200, "red", 0.5)
    sh = place(man_full(hat=True, cape=True, rim=None, fill="#050101"), 1500, 1350, 1.3)
    s += f'<g opacity="0.9" filter="url(#blur1)">{sh}'
    s += '<path d="M1420,255 C1400,180 1380,120 1340,80 C1400,110 1440,170 1450,250 Z M1590,255 C1610,180 1630,120 1670,80 C1610,110 1570,170 1560,250 Z" fill="#050101"/></g>'
    s += '<circle cx="1478" cy="318" r="9" fill="#ff3020" filter="url(#glow)"/><circle cx="1530" cy="318" r="9" fill="#ff3020" filter="url(#glow)"/>'
    s += '<path d="M0,1200 L2400,1200 L2400,1350 L0,1350 Z" fill="#0a0202"/>'
    return S(s)

# ---------------------------------------------------------- places
@art
def coyotes():
    s = sky("#040a18", "#1a2a44") + stars(200, 3, 700) + moon(1650, 330, 150)
    s += ridge(900, 80, "#0c1420", 4) + ridge(1040, 60, "#070c12", 6)
    for x in range(0, 2400, 300):
        s += tree(x + 120, 1080, 160, x, "#05080c", "bare")
    # nopales and magueyes
    r = random.Random(8)
    for x in (200, 2100, 2280):
        for j in range(6):
            cx, cy = x + r.uniform(-90, 90), 1120 - j * 40 - r.uniform(0, 60)
            s += f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="44" ry="64" fill="#03060a" transform="rotate({r.uniform(-30,30):.0f} {cx:.0f} {cy:.0f})"/>'
    for x in (500, 1900):
        for j in range(14):
            a = math.radians(-160 + j * 10)
            s += f'<path d="M{x},1200 Q{x+math.cos(a)*120:.0f},{1200+math.sin(a)*200:.0f} {x+math.cos(a)*260:.0f},{1200+math.sin(a)*300:.0f}" stroke="#03060a" stroke-width="26" fill="none" stroke-linecap="round"/>'
    # two coyotes howling on a rock
    s += '<path d="M900,1100 C960,980 1300,960 1420,1100 Z" fill="#05080c"/>'
    for (x, y, k, f) in [(1040, 1010, 1.25, False), (1330, 1030, 1.0, True)]:
        c = ('<path d="M-60,0 C-90,-40 -96,-110 -70,-170 C-56,-210 -30,-250 -6,-290 L10,-330 C20,-360 40,-400 70,-430 L80,-470 L96,-436 '
             'L120,-462 L118,-420 C140,-400 170,-396 200,-404 L196,-384 C170,-372 140,-364 120,-350 C100,-320 90,-280 84,-240 '
             'C96,-180 100,-100 90,-40 L110,0 L60,0 L50,-60 L20,-60 L20,0 Z" fill="#020305"/>')
        c += '<path d="M-60,-10 C-120,-20 -170,0 -200,30 C-150,10 -110,6 -60,10 Z" fill="#020305"/>'
        c += '<path d="M10,-330 C20,-360 40,-400 70,-430 L80,-470 L96,-436 L120,-462 L118,-420 C140,-400 170,-396 200,-404" stroke="#a8c8ff" stroke-width="4" fill="none" opacity="0.7"/>'
        c += '<path d="M84,-240 C96,-180 100,-100 90,-40" stroke="#a8c8ff" stroke-width="3" fill="none" opacity="0.4"/>'
        s += place(c, x, y, k, flip=f)
    s += '<rect width="2400" height="1350" fill="#02040a" opacity="0.1"/>'
    return S(s)
@art
def lake():
    s = sky("#0a1426", "#2a4060") + stars(120, 5, 500) + moon(600, 260, 90)
    s += BA.volcanoes().split('<svg')[0] if False else ""
    s += '<path d="M1300,700 L1600,420 L1680,440 L1760,400 L2100,700 Z" fill="#1a2638"/><path d="M1560,450 L1600,420 L1680,440 L1760,400 L1720,470 L1640,460 Z" fill="#d8e4f0" opacity="0.7"/>'
    s += '<path d="M200,700 C400,560 600,600 700,560 C800,600 950,620 1100,700 Z" fill="#141e2e"/>'
    s += ridge(720, 30, "#0c1420", 3) + water(720, 1350)
    s += reflection(600, 730, 1350, "#e8eef5", 160)
    s += reeds(0, 900, 1250, 4) + reeds(1700, 2400, 1280, 5)
    s += '<path d="M1100,1050 L1500,1050 L1460,1085 L1140,1085 Z" fill="#05080c"/>' + place(woman_full(rim="#a8c8ff").replace('', ''), 1300, 1052, 0.18)
    s += '<path d="M1380,900 L1360,1052" stroke="#05080c" stroke-width="6"/>'
    return S(s)
@art
def plaza_coyoacan():
    s = sky("#1a2a50", "#e8a070", "#7a6a8a")
    s += '<rect x="700" y="400" width="900" height="700" fill="#b8865a"/><rect x="700" y="400" width="900" height="700" fill="#000" filter="url(#plaster)" opacity="0.4"/>'
    s += '<path d="M700,400 L1150,250 L1600,400 Z" fill="#a07448"/>'
    s += '<rect x="1600" y="160" width="260" height="940" fill="#c09060"/><rect x="1640" y="220" width="180" height="160" rx="80" fill="#1a1010"/><path d="M1600,160 L1730,60 L1860,160 Z" fill="#8a6040"/>'
    s += '<circle cx="1730" cy="300" r="40" fill="#5a3a20"/>'
    s += '<path d="M1030,1100 L1030,760 C1030,680 1270,680 1270,760 L1270,1100 Z" fill="#2a1608"/><path d="M1030,760 C1030,680 1270,680 1270,760" stroke="#e8c890" stroke-width="30" fill="none"/>'
    s += '<circle cx="1150" cy="560" r="70" fill="#2a1a10" stroke="#e8c890" stroke-width="16"/>'
    for x in (760, 1500):
        s += f'<rect x="{x}" y="620" width="40" height="480" fill="#e0c090"/>'
    s += '<rect x="0" y="1100" width="2400" height="250" fill="#5a4a3a"/>'
    for x in (150, 450, 2050, 2300):
        s += canopy(x, 700, 230, 280, x, "#ffd8a0", ("#1a2a12", "#22341a", "#2a3c20"), 160, 0, 0.5) + f'<rect x="{x-20}" y="900" width="40" height="220" fill="#2a1a10"/>'
    s += place(man_full(hat=True, cape=False, rim="#ffd8a0"), 520, 1250, 0.4) + place(woman_full(rebozo_head=True, rim="#ffd8a0"), 1900, 1240, 0.38)
    x, y = LAMP_XY
    s += lamp(x, 1200, 820, True)
    return S(s)
def chapel(mood="warm"):
    if mood == "warm":
        s = sky("#4a6aa8", "#f0c890", "#c89a8a"); wall = "#e0a830"; lit = 0
    elif mood == "night":
        s = sky("#030812", "#14243a") + stars(150, 9, 500) + moon(500, 200, 60); wall = "#5a4a2a"; lit = 1
    else:
        s = sky("#2a3a5a", "#c89a8a"); wall = "#8a7040"; lit = 0
    s += f'<rect x="800" y="420" width="800" height="700" fill="{wall}"/><rect x="800" y="420" width="800" height="700" fill="#000" filter="url(#plaster)" opacity="0.35"/>'
    s += f'<path d="M800,420 C900,360 1000,330 1200,320 C1400,330 1500,360 1600,420 Z" fill="{wall}"/>'
    s += f'<path d="M1040,320 L1040,160 C1040,100 1360,100 1360,160 L1360,320 Z" fill="{wall}"/>'  # espadaña
    s += '<path d="M1100,300 L1100,190 C1100,150 1180,150 1180,190 L1180,300 Z M1220,300 L1220,190 C1220,150 1300,150 1300,190 L1300,300 Z" fill="#1a1010"/>'
    s += '<path d="M1120,230 C1120,200 1160,200 1160,230 L1166,260 L1114,260 Z" fill="#8a6a30"/><path d="M1240,230 C1240,200 1280,200 1280,230 L1286,260 L1234,260 Z" fill="#8a6a30"/>'
    s += '<path d="M1200,80 L1200,130 M1180,100 L1220,100" stroke="#1a1010" stroke-width="10"/>'
    s += '<path d="M1080,1120 L1080,780 C1080,700 1320,700 1320,780 L1320,1120 Z" fill="#3a1e0a"/><path d="M1080,780 C1080,700 1320,700 1320,780" stroke="#f0e0c0" stroke-width="26" fill="none"/>'
    s += '<path d="M1140,560 L1140,500 C1140,460 1260,460 1260,500 L1260,560 Z" fill="%s"/>' % ("#ffc865" if lit else "#1a1010")
    s += '<rect x="0" y="1120" width="2400" height="230" fill="#4a3a2a"/>' if mood != "night" else '<rect x="0" y="1120" width="2400" height="230" fill="#0c0a0c"/>'
    for x in (300, 600, 1850, 2150):
        dk = mood != "warm"
        s += canopy(x, 640, 230, 300, x + 3, "#ffd8a0" if not dk else "#7a9cc4", ("#05100a", "#08140c", "#0c1a10") if dk else ("#1a3a12", "#22441a", "#2a4c20"), 170, 0, 0.5) + f'<rect x="{x-18}" y="860" width="36" height="270" fill="#1a1008"/>'
    if mood == "night":
        s += '<rect width="2400" height="1350" fill="#02040a" opacity="0.3"/>'
    return s
@art
def santa_catarina(): return S(chapel("warm"))
@art
def santa_catarina_dawn(): return S(chapel("dawn"), QM.fog_band(1150, 0.4, 3))
@art
def pueblo_1930():
    s = sky("#7a9ac0", "#f0dcb0")
    s += '<path d="M1500,700 L1750,470 L1820,490 L1900,450 L2200,700 Z" fill="#8a9ab0"/><path d="M1700,520 L1750,470 L1820,490 L1900,450 L1870,520 L1790,510 Z" fill="#f0f0f0"/>'
    s += '<path d="M300,700 C500,580 700,620 800,580 C900,620 1050,640 1200,700 Z" fill="#9aa8b8"/>'
    s += '<rect x="0" y="700" width="2400" height="650" fill="#a8925a"/>'
    for i in range(12):
        s += f'<path d="M0,{740+i*50} L2400,{730+i*52}" stroke="#7a6a3a" stroke-width="{4+i}" opacity="0.4"/>'
    s += '<path d="M1000,1350 L1150,700 L1250,700 L1500,1350 Z" fill="#c8a878"/>'
    r = random.Random(3)
    for i, x in enumerate([180, 420, 640, 1600, 1840, 2100]):
        w = r.uniform(180, 260); h = r.uniform(120, 170); y = 760 + i % 3 * 10
        s += f'<rect x="{x}" y="{y-h}" width="{w:.0f}" height="{h:.0f}" fill="#c8a070"/><rect x="{x+w*0.4:.0f}" y="{y-h*0.6:.0f}" width="{w*0.2:.0f}" height="{h*0.6:.0f}" fill="#4a2a18"/>'
        s += f'<path d="M{x-10},{y-h} L{x+w+10:.0f},{y-h} L{x+w:.0f},{y-h-20:.0f} L{x},{y-h-20:.0f} Z" fill="#8a5030"/>'
    for x in range(1300, 2400, 220):
        s += f'<path d="M{x},700 L{x},560 M{x-30},580 L{x+30},580" stroke="#3a2a1a" stroke-width="8"/>'
    s += '<path d="M1300,580 Q1410,600 1520,580 Q1630,600 1740,580 Q1850,600 1960,580 Q2070,600 2180,580" stroke="#3a2a1a" stroke-width="2" fill="none"/>'
    s += place(man_full(hat=True, cape=False, rim=None, fill="#3a2a1a"), 1220, 900, 0.22)
    for x in (100, 900, 2300):
        s += canopy(x, 600, 160, 160, x, None, ("#4a5a2a", "#5a6a32", "#3a4a22"), 100, 0)
    return S(s)
@art
def kids_play():
    s = callejon("day", seed=4, lamp_on=False, door_lit=False, niche=False)
    for i, (x, z, kw) in enumerate([(-0.4, 1.8, dict(reach=True)), (0.2, 2.4, dict(trompo_hand=True)), (0.55, 3.2, dict(girl=True)), (-0.1, 4.0, {})]):
        px, py = P(x, 0.62, z)
        s += place(kid_sil(rim="#fff0c0", fill="#2a2018", **kw), px, py, 0.85 / z, flip=(i % 2 == 1))
    s += trompo(*P(0.05, 0.62, 1.6), 0.5, spin=True, light="#fff0c0")
    return S(s)
@art
def house_soldier():
    s = sky("#030812", "#14243a") + stars(150, 11, 500) + moon(2050, 180, 60)
    s += '<rect x="300" y="380" width="1300" height="800" fill="#3a2a2a"/><rect x="300" y="380" width="1300" height="800" fill="#000" filter="url(#plaster)" opacity="0.5"/>'
    s += '<rect x="300" y="1040" width="1300" height="140" fill="#1a1010"/>'
    s += '<rect x="280" y="360" width="1340" height="40" fill="#1a1416"/>'
    s += '<path d="M700,1180 L700,700 C700,640 960,640 960,700 L960,1180 Z" fill="#1a0e06"/>'
    for i in range(4):
        s += f'<path d="M{720+i*62},700 L{720+i*62},1170" stroke="#0a0604" stroke-width="6"/>'
    s += '<circle cx="920" cy="950" r="10" fill="#8a7040"/>'
    s += window(1300, 620, 200, 280, True, arch=True)
    s += '<rect x="1600" y="640" width="800" height="540" fill="#2c2c34"/><rect x="1600" y="640" width="800" height="540" fill="#000" filter="url(#plaster)" opacity="0.4"/><rect x="1600" y="620" width="800" height="30" fill="#3a3a44"/>'
    s += branch(2400, 700, 1900, 420, 60) + branch(1900, 420, 1500, 200, 30)
    s += canopy(1950, 330, 520, 300, 5, "#7a9cc4", n=360, fruit=16) + canopy(1400, 220, 300, 160, 6, "#7a9cc4", n=150, fruit=5)
    s += '<rect x="0" y="1180" width="2400" height="170" fill="#0a0a0e"/>' + glow(1400, 760, 400, "warm", 0.6)
    return S(s, QM.fog_band(1220, 0.3, 4))
@art
def door_closed():
    s = '<rect width="2400" height="1350" fill="#b07848"/><rect width="2400" height="1350" fill="#000" filter="url(#plaster)" opacity="0.35"/>'
    s += '<path d="M800,1350 L800,300 C800,180 1600,180 1600,300 L1600,1350 Z" fill="#c8a070"/>'
    s += '<path d="M860,1350 L860,320 C860,230 1540,230 1540,320 L1540,1350 Z" fill="#4a2a12"/>'
    for i in range(1, 6):
        s += f'<path d="M{860+i*113},{300 if i in (2,3,4) else 330} L{860+i*113},1350" stroke="#2a1608" stroke-width="10"/>'
    for y in (520, 980):
        s += f'<rect x="860" y="{y}" width="680" height="24" fill="#1a1008"/>'
        for x in range(900, 1540, 80):
            s += f'<circle cx="{x}" cy="{y+12}" r="9" fill="#5a4a30"/>'
    s += '<circle cx="1460" cy="800" r="26" fill="none" stroke="#6a5a3a" stroke-width="9"/>'
    s += '<path d="M0,1250 L2400,1250 L2400,1350 L0,1350 Z" fill="#5a4a3a"/>' + glow(400, 200, 900, "warm", 0.3)
    return S(s)
@art
def door_night():
    s = ART["door_closed"]().replace('fill="#b07848"', 'fill="#2a2030"').replace('fill="#c8a070"', 'fill="#3a3238"').replace('fill="#4a2a12"', 'fill="#140a06"')
    return s.replace('</svg>', '<rect width="2400" height="1350" fill="#02040a" opacity="0.55"/><rect x="860" y="1340" width="680" height="10" fill="#ffc865" opacity="0.8"/></svg>')
@art
def room_soldier(): return S(_room(True))
@art
def room_dark(): return S(_room(False))
def _room(uniform=True):
    s = room_walls("#3a2a22", "#0c0806", "#1a120c")
    s += '<rect x="250" y="760" width="900" height="320" fill="#2a1c14"/><rect x="230" y="700" width="60" height="400" fill="#1a1008"/><rect x="250" y="720" width="900" height="80" fill="#d8ccb0"/>'
    s += '<path d="M300,800 C500,780 800,800 1100,790 L1100,900 L300,900 Z" fill="#8a7a6a"/>'
    s += '<rect x="900" y="300" width="300" height="220" fill="#1a1008"/><rect x="920" y="320" width="260" height="180" fill="#8a7a60"/>'
    s += place(soldier_sil(rim=None, fill="#3a3020"), 1000, 480, 0.15) + place(soldier_sil(rim=None, fill="#3a3020"), 1060, 480, 0.14) + place(soldier_sil(rim=None, fill="#3a3020"), 1120, 480, 0.15)
    s += '<rect x="1600" y="760" width="600" height="40" fill="#3a2414"/><rect x="1620" y="800" width="30" height="300" fill="#2a1a0c"/><rect x="2150" y="800" width="30" height="300" fill="#2a1a0c"/>'
    if uniform:
        s += '<path d="M1400,700 L1440,1100 L1380,1100 Z" fill="#2a1a0c"/>'
        s += f'<path d="M1300,560 C1340,540 1460,540 1500,560 L1540,820 L1260,820 Z" fill="{OLIVE[1]}"/>' + medal(1440, 640, 0.8) + medal(1480, 642, 0.8, ("#b81a2a", "#e8c84a", "#b81a2a"), "#c0c0c8")
        s += f'<g transform="translate(1760,760) scale(0.7)">{kepi("#ffcf8a")}</g>'
    else:
        s += '<path d="M1700,760 L1760,700 L1840,760 Z" fill="#c8c0b0" opacity="0.6"/><path d="M1880,760 L1960,740 L2010,760 Z" fill="#c8c0b0" opacity="0.5"/>'
        s += place(soldier_sil(rim="#ffcf8a", fill="#050403", bow=True), 1350, 1180, 0.55)
    s += candle_at(CANDLE_XY[0], CANDLE_XY[1], 150)
    s += '<rect width="2400" height="1350" fill="#000" opacity="%s"/>' % ("0.15" if uniform else "0.35")
    return s
@art
def war_memory():
    s = sky("#1a0404", "#c83a10", "#6a1408") + glow(1200, 900, 1400, "red", 0.6)
    s += ridge(1000, 80, "#2a0806", 3) + ridge(1100, 50, "#120202", 5)
    s += clouds(14, 200, 900, 7, "#3a0a06", (0.3, 0.6))
    for (x, k, f) in [(500, 0.55, False), (800, 0.5, False), (1650, 0.6, True), (1950, 0.52, True)]:
        s += place(soldier_sil(rim="#ff8040", fill="#0a0202", walk=0.5), x, 1200, k, flip=f)
        s += f'<path d="M{x+(60 if not f else -60)},{1200-420*k/0.55:.0f} L{x+(260 if not f else -260)},{1200-640*k/0.55:.0f}" stroke="#0a0202" stroke-width="12"/>'
    s += '<path d="M1100,1200 L1100,1080 L1180,1000 L1300,1000 L1340,1060 L1380,1060 L1380,1200 Z" fill="#0a0202"/>'  # horse-ish ruin
    s += '<rect x="0" y="1200" width="2400" height="150" fill="#080101"/>'
    return S(s)
def war_flash(): return S(f'<g transform="translate(-600,-350) scale(1.5)">{ART["war_memory"]().split(">",1)[1].rsplit("</svg>",1)[0]}</g>', '<rect width="2400" height="1350" fill="#ffd0a0" opacity="0.3"/>')
@art
def search_night():
    s = sky("#030812", "#14243a") + stars(150, 13, 500) + moon(1900, 200, 55)
    s += ridge(900, 40, "#0a1018", 3)
    for x in (200, 700, 1500, 2200):
        s += canopy(x, 640, 240, 260, x + 1, "#7a9cc4", n=170, fruit=0) + f'<rect x="{x-18}" y="860" width="36" height="200" fill="#05080a"/>'
    s += '<rect x="0" y="1000" width="2400" height="350" fill="#0c0c10"/>' + cobble_floor(2.0, 9, "#15141a").replace('', '') if False else '<rect x="0" y="1000" width="2400" height="350" fill="#0c0c10"/>'
    s += '<path d="M0,1040 L2400,1020" stroke="#1a1a22" stroke-width="20"/>'
    return S(s, QM.fog_band(1100, 0.35, 8))
@art
def crowd_dawn():
    s = chapel("dawn") + '<rect width="2400" height="1350" fill="#1a2030" opacity="0.4"/>'
    s += canopy(1200, 260, 900, 300, 77, "#ffe0a0", ("#0c1410", "#121c14", "#18241a"), 400, 18, 0.4)
    for i in range(9):
        x = 250 + i * 240; k = 0.5 + (i % 3) * 0.05
        s += place(woman_full(rebozo_head=True, rim="#ffe0a0", fill="#05060a") if i % 2 else man_full(hat=True, cape=False, rim="#ffe0a0", fill="#05060a"), x, 1350, k, flip=(i > 4))
    return S(s, QM.fog_band(1200, 0.35, 11))
@art
def dawn_flash():
    s = '<rect width="2400" height="1350" fill="#e8e0d8"/>'
    s += canopy(1200, 500, 1100, 520, 78, None, ("#1a1a1a", "#222", "#2a2a2a"), 500, 22)
    s += branch(1200, 1350, 1200, 500, 160, "#111") + branch(1200, 700, 600, 300, 60, "#111") + branch(1200, 650, 1800, 260, 60, "#111")
    return S(s)
@art
def tree_close():
    s = sky("#5a8ac8", "#e8dcb0")
    s += branch(1100, 1350, 1150, 600, 220, "#3a2a1c", 0.05) + branch(1150, 700, 500, 300, 90, "#3a2a1c") + branch(1150, 680, 1900, 260, 90, "#3a2a1c")
    s += '<path d="M1040,1350 C1060,1100 1050,900 1080,700" stroke="#5a4430" stroke-width="20" fill="none" opacity="0.6"/>'
    s += canopy(1200, 300, 1300, 360, 51, "#f0f8c0", ("#2a4a1e", "#335a24", "#3e6a2a"), 600, 26, 0.5, 1.4)
    return S(s)
@art
def tree_moon():
    s = sky("#030812", "#1a2a44") + stars(160, 17, 1300) + moon(1700, 820, 120)
    s += branch(1000, 1350, 1100, 640, 200, "#030405", 0.05) + branch(1100, 760, 400, 360, 80, "#030405") + branch(1100, 720, 2000, 300, 80, "#030405")
    s += canopy(1200, 260, 1300, 360, 52, "#a8c8ff", n=600, fruit=24, lit=0.5, leaf=1.4)
    return S(s)
@art
def tree_shadow(): return S(ART["tree_moon"]().split(">", 1)[1].rsplit("</svg>", 1)[0], '<rect width="2400" height="1350" fill="#02040a" opacity="0.3"/>')
@art
def chronicle():
    s = room_walls("#2a2018", "#0c0806", "#1a120c") + table_wood(760)
    s += '<path d="M500,900 L1200,860 L1900,900 L1900,1300 L1200,1260 L500,1300 Z" fill="#d8ccb0"/><path d="M1200,860 L1200,1260" stroke="#8a7a60" stroke-width="6"/>'
    s += '<text x="850" y="960" font-family="IM FELL English" font-size="54" fill="#2a1a10" text-anchor="middle">Leyendas de</text><text x="850" y="1030" font-family="IM FELL English" font-size="64" fill="#2a1a10" text-anchor="middle">Coyoacán</text>'
    for i in range(6):
        s += f'<path d="M620,{1080+i*30} L1100,{1076+i*30}" stroke="#6a5a48" stroke-width="5" opacity="0.6"/>'
    s += '<text x="1550" y="950" font-family="IM FELL English" font-size="44" fill="#2a1a10" text-anchor="middle" font-style="italic">El Callejón del Aguacate</text>'
    for i in range(9):
        s += f'<path d="M1290,{1000+i*30} L1820,{996+i*30}" stroke="#6a5a48" stroke-width="5" opacity="0.6"/>'
    s += candle_at(CANDLE_XY[0], CANDLE_XY[1], 160).replace(f'x="{CANDLE_XY[0]-26}"', f'x="{CANDLE_XY[0]-26}"')
    return S(s)
@art
def pascualita():
    s = '<rect width="2400" height="1350" fill="#0a0c14"/>'
    s += '<rect x="500" y="200" width="1400" height="1000" fill="#3a2a1a"/>' + glow(1200, 600, 900, "warm", 0.7)
    s += '<rect x="500" y="200" width="1400" height="1000" fill="none" stroke="#1a1008" stroke-width="40"/>'
    s += '<text x="1200" y="170" font-family="Cinzel" font-size="80" fill="#e8d8b0" text-anchor="middle">VESTIDOS DE NOVIA</text>'
    s += '<path d="M1200,360 C1150,360 1130,420 1140,470 C1150,520 1250,520 1260,470 C1270,420 1250,360 1200,360 Z" fill="#e8d0b8"/>'
    s += '<path d="M1140,420 C1100,500 1080,600 1100,680 L1300,680 C1320,600 1300,500 1260,420 C1280,380 1240,340 1200,340 C1160,340 1120,380 1140,420 Z" fill="#2a1a10" opacity="0.8"/>'
    s += '<path d="M1170,440 q10,-8 20,0 M1210,440 q10,-8 20,0" stroke="#1a0e08" stroke-width="5" fill="none"/><circle cx="1180" cy="446" r="6" fill="#140a06"/><circle cx="1220" cy="446" r="6" fill="#140a06"/>'
    s += '<path d="M1110,540 C1140,520 1260,520 1290,540 L1320,700 C1420,900 1480,1100 1500,1180 L900,1180 C920,1100 980,900 1080,700 Z" fill="#f4efe6"/>'
    for i in range(8):
        s += f'<path d="M{1100+i*28},700 C{1060+i*40},900 {1000+i*60},1080 {960+i*70},1180" stroke="#c8c0b4" stroke-width="5" fill="none" opacity="0.6"/>'
    s += '<path d="M1140,340 C1000,400 940,700 900,1100" stroke="#fff" stroke-width="40" fill="none" opacity="0.25" filter="url(#blur2)"/>'
    s += '<path d="M0,1200 L2400,1200 L2400,1350 L0,1350 Z" fill="#05060a"/>'
    return S(s)
@art
def black(): return S('<rect width="2400" height="1350" fill="#000"/>')


if __name__ == "__main__":
    write(sys.argv[1:] or list(ART))
