#!/usr/bin/env python3
"""Illustrations for 'El Cadejo' (camino real de Comitán, Chiapas) — writes art/*.svg (2400x1350).
Reuses helpers of earlier videos (beso_art, chars, base_chars, qm_art, aguacate_art, pas_art, sb_art = El Sombrerón).
New here: dog() — a detailed side-view dog (white Cadejo with paws / black Cadejo with goat hooves, matted locks,
glowing eyes, growl), the road through pines and milpa, the wooden bridge, fogón kitchen, marimba, fight, map, prints.
Usage: python3 make_art.py [name ...]   then: node /home/claude/pipeline/render_svg.js art/*.svg"""
import sys, os, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '/home/claude/pipeline'); sys.path.insert(0, HERE)
from art import *
from chars import place, man_full, woman_full, strands, bust_frame, SIL, luis_bust, father_bust, brigida_bust
from base_chars import uid, grad_lin, grad_rad
import beso_art as BA
from beso_art import S, clouds, room_walls, candle_at, flame, table_wood, portrait_bg, MOONRIM
import qm_art as QM
import pas_art as PA
import sb_art as SB
from sb_art import pines, town, horse_shape, braid, wavy

A = os.path.join(HERE, "art"); os.makedirs(A, exist_ok=True)
ART = {}
def art(fn):
    ART[fn.__name__] = fn; return fn

WARM = "#ffcf8a"; RED = "#c8141a"
inner = PA.inner


def crop(svgstr, k, cx, cy, extra=""):
    return S(f'<g transform="translate(1200,675) scale({k}) translate({-cx},{-cy})">{inner(svgstr)}</g>', extra)


def smooth(pts, closed=True, t=0.5):
    """Catmull-Rom through pts -> cubic bezier path"""
    n = len(pts); P = pts
    d = f"M{P[0][0]:.1f},{P[0][1]:.1f} "
    rng = range(n) if closed else range(n - 1)
    for i in rng:
        p0 = P[(i - 1) % n] if (closed or i > 0) else P[i]
        p1 = P[i]; p2 = P[(i + 1) % n]
        p3 = P[(i + 2) % n] if (closed or i + 2 < n) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) * t / 3, p1[1] + (p2[1] - p0[1]) * t / 3)
        c2 = (p2[0] - (p3[0] - p1[0]) * t / 3, p2[1] - (p3[1] - p1[1]) * t / 3)
        d += f"C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f} "
    return d + ("Z" if closed else "")


# ============================================================================ THE DOG
TORSO = [(-175, -335), (-60, -350), (100, -342), (250, -352), (340, -385), (405, -440), (450, -500), (500, -528),
         (548, -522), (590, -492), (640, -462), (668, -448), (672, -428), (640, -414), (590, -406), (540, -392),
         (490, -360), (440, -300), (380, -240), (260, -222), (100, -212), (-40, -222), (-140, -246), (-190, -290)]
SKULL_TOP = [(405, -440), (450, -500), (500, -528), (548, -522), (590, -492), (640, -462), (668, -448)]
BACK = [(-175, -335), (-60, -350), (100, -342), (250, -352), (340, -385), (405, -440), (450, -500)]
BELLY = [(440, -300), (380, -240), (260, -222), (100, -212), (-40, -222), (-140, -246)]
def _h(p): return (p[0] - 20, p[1] + 30) if p[0] >= 430 else ((395, -420) if p == (405, -440) else p)
TORSO = [_h(p) for p in TORSO]
TORSO = [q for q in TORSO if q not in ((440, -300), (380, -240), (260, -222))]
_i = TORSO.index((100, -212)); TORSO[_i:_i] = [(410, -280), (380, -200), (290, -190), (180, -222)]
TORSO.remove((100, -212))
SKULL_TOP = [_h(p) for p in SKULL_TOP]; BACK = [_h(p) for p in BACK]
BELLY = [(410, -280), (380, -200), (290, -190), (180, -222), (-40, -222), (-140, -246)]
HEAD_T = 'translate(-20,30)'


def limb(x, y, a1, a2, l1, l2, w1, w2, foot="paw", col="#000", hoofcol="#1a1612", fur=None, seed=1):
    """two-segment leg from joint (x,y), angles in degrees from vertical (positive = forward/right)"""
    r1, r2 = math.radians(a1), math.radians(a2)
    kx, ky = x + l1 * math.sin(r1), y + l1 * math.cos(r1)
    fx_, fy_ = kx + l2 * math.sin(r2), ky + l2 * math.cos(r2)
    def seg(x0, y0, x1, y1, wa, wb):
        dx, dy = x1 - x0, y1 - y0; L = math.hypot(dx, dy) or 1; nx, ny = -dy / L, dx / L
        return (f'<path d="M{x0+nx*wa:.1f},{y0+ny*wa:.1f} L{x1+nx*wb:.1f},{y1+ny*wb:.1f} L{x1-nx*wb:.1f},{y1-ny*wb:.1f} '
                f'L{x0-nx*wa:.1f},{y0-ny*wa:.1f} Z" fill="{col}"/>')
    def bulge(x0, y0, x1, y1, wa, wb):
        dx, dy = x1 - x0, y1 - y0; L = math.hypot(dx, dy) or 1; nx, ny = -dy / L, dx / L
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        return (f'<path d="M{x0+nx*wa:.1f},{y0+ny*wa:.1f} Q{mx+nx*wa*1.5:.1f},{my+ny*wa*1.5:.1f} {x1+nx*wb:.1f},{y1+ny*wb:.1f} '
                f'L{x1-nx*wb:.1f},{y1-ny*wb:.1f} Q{mx-nx*wa*1.3:.1f},{my-ny*wa*1.3:.1f} {x0-nx*wa:.1f},{y0-ny*wa:.1f} Z" fill="{col}"/>')
    s = bulge(x, y, kx, ky, w1, (w1 + w2) / 2.4) + f'<circle cx="{kx:.1f}" cy="{ky:.1f}" r="{(w1+w2)/2.4:.1f}" fill="{col}"/>'
    s += seg(kx, ky, fx_, fy_, (w1 + w2) / 2.4, w2 * 0.8)
    if foot == "paw":
        s += f'<ellipse cx="{fx_+14:.1f}" cy="{fy_-4:.1f}" rx="{w2*1.5:.1f}" ry="{w2*0.75:.1f}" fill="{col}"/>'
        for t in (-1, 0, 1):
            s += f'<path d="M{fx_+14+t*w2*0.7:.1f},{fy_-2:.1f} l3,8" stroke="#00000080" stroke-width="2"/>'
    elif foot == "hoof":
        # cloven goat hoof
        s += (f'<path d="M{fx_-w2*1.1:.1f},{fy_-26:.1f} L{fx_+w2*1.1:.1f},{fy_-26:.1f} L{fx_+w2*1.5:.1f},{fy_+2:.1f} '
              f'L{fx_-w2*1.3:.1f},{fy_+2:.1f} Z" fill="{hoofcol}"/>'
              f'<path d="M{fx_+w2*0.15:.1f},{fy_-20:.1f} L{fx_+w2*0.2:.1f},{fy_+2:.1f}" stroke="#000" stroke-width="5"/>'
              f'<path d="M{fx_-w2*1.1:.1f},{fy_-26:.1f} L{fx_+w2*1.1:.1f},{fy_-26:.1f}" stroke="#4a4038" stroke-width="3" opacity="0.7"/>')
        if fur:  # shaggy fetlock tuft
            r = random.Random(seed)
            for _ in range(9):
                ox = r.uniform(-w2 * 1.4, w2 * 1.4)
                s += (f'<path d="M{fx_+ox:.1f},{fy_-60:.1f} q{r.uniform(-8,8):.1f},20 {r.uniform(-10,10):.1f},{r.uniform(30,44):.1f}" '
                      f'stroke="{fur}" stroke-width="{r.uniform(4,8):.1f}" fill="none" stroke-linecap="round"/>')
    return s


def dog(kind="white", pose="stand", rim=MOONRIM, eye=None, growl=False, seed=1, hairless=False, glow_body=True,
        head_turn=False):
    """side view, facing right, ground at y=0, ~700 long, ~530 tall. kind: white | black | xolo"""
    r = random.Random(seed); g = uid("dg")
    if kind == "white":
        top, mid, bot, furc, furhi, legc = "#f6f8fc", "#d4dce8", "#8e9cb2", "#e8eef6", "#ffffff", "#c2ccda"
        foot = "paw"; eye = eye or "#2a1a10"
    elif kind == "black":
        top, mid, bot, furc, furhi, legc = "#16161c", "#0a0a0e", "#030305", "#1c1a20", "#3a3644", "#060608"
        foot = "hoof"; eye = eye or "red"
    else:  # xolo
        top, mid, bot, furc, furhi, legc = "#4a3a32", "#2e221c", "#160e0a", "#000", "#000", "#241a14"
        foot = "paw"; eye = eye or "#ffcf8a"; hairless = True
    s = f'<defs>{grad_lin(g+"b", [(0, top, 1), (0.55, mid, 1), (1, bot, 1)], 0, -540, 0, -200)}</defs>'
    # pose -> leg angles
    if pose == "walk":
        fl = [(18, -6), (-14, 4)]; rl = [(-20, 10), (14, 22)]
    elif pose == "leap":
        fl = [(60, 80), (48, 70)]; rl = [(-60, -78), (-48, -66)]
    elif pose == "crouch":
        fl = [(30, -10), (22, -6)]; rl = [(-30, 30), (-20, 34)]
    else:
        fl = [(4, -2), (-6, 2)]; rl = [(-12, 14), (4, 18)]
    body_rot = {"leap": -10, "crouch": 6, "rear": -32}.get(pose, 0)
    yoff = {"crouch": 40, "leap": -90}.get(pose, 0)
    # far legs (darker)
    far = "#5c6676" if kind == "white" else ("#020203" if kind == "black" else "#120a06")
    fur_far = None if hairless else ("#0c0c10" if kind == "black" else None)
    legs_far = limb(300, -250, fl[1][0], fl[1][1], 130, 130, 30, 20, foot, far, fur=fur_far, seed=seed + 1)
    legs_far += limb(-120, -270, rl[1][0], rl[1][1] + 30, 130, 150, 40, 20, foot, far, fur=fur_far, seed=seed + 2)
    legs_near = limb(320, -250, fl[0][0], fl[0][1], 130, 132, 34, 22, foot, legc, fur=None if hairless else furc, seed=seed + 3)
    legs_near += limb(-110, -270, rl[0][0], rl[0][1] + 30, 135, 150, 56, 22, foot, legc, fur=None if hairless else furc, seed=seed + 4)
    if pose == "rear":
        legs_far = limb(300, -250, 120, 60, 130, 120, 30, 20, foot, far)
        legs_near = limb(320, -250, 140, 80, 130, 120, 34, 22, foot, legc)
        legs_near += limb(-110, -270, -10, 10, 140, 160, 46, 22, foot, legc, fur=None if hairless else furc)
        legs_far += limb(-120, -270, 10, 20, 135, 150, 40, 20, foot, far)
    # tail
    if kind == "xolo":
        tail = '<path d="M-180,-320 C-260,-300 -300,-220 -320,-140" stroke="{c}" stroke-width="16" fill="none" stroke-linecap="round"/>'.format(c=mid)
    else:
        tp = [(-175, -330), (-250, -330), (-310, -280), (-330, -200), (-300, -190), (-290, -260), (-240, -300), (-180, -300)]
        tail = f'<path d="{smooth(tp)}" fill="{mid}"/>'
        for i in range(14):
            u = i / 13; x0 = -180 - 140 * u; y0 = -330 + 120 * u * u
            tail += (f'<path d="M{x0:.0f},{y0:.0f} q{-20-r.uniform(0,20):.0f},{10+r.uniform(0,20):.0f} {-30-r.uniform(0,30):.0f},{40+r.uniform(0,40):.0f}" '
                     f'stroke="{furc}" stroke-width="{r.uniform(5,10):.0f}" fill="none" stroke-linecap="round" opacity="0.9"/>')
    torso = TORSO
    if kind == "xolo":
        torso = [(x, y + (12 if y < -300 and x < 400 else 0)) for x, y in TORSO]
    body = f'<path d="{smooth(torso)}" fill="url(#{g}b)"/>'
    body += f'<g transform="translate(-20,30)">'
    # ear
    if kind == "xolo":
        body += '<path d="M470,-505 L455,-640 L525,-520 Z" fill="{}"/><path d="M480,-515 L466,-610 L510,-525 Z" fill="#6a4a3a"/>'.format(mid)
    else:
        body += f'<path d="M462,-500 C448,-560 452,-600 468,-622 C496,-584 520,-548 520,-515 Z" fill="{mid}"/>'
        body += f'<path d="M472,-510 C464,-552 466,-582 474,-598 C492,-570 506,-546 506,-520 Z" fill="{bot}" opacity="0.6"/>'
    body += '</g><g>'
    # shading: belly shadow + shoulder/hip muscles
    body += f'<path d="{smooth(BELLY, closed=False)}" stroke="{bot}" stroke-width="40" fill="none" opacity="0.5" filter="url(#blur2)"/>'
    body += f'<path d="M300,-360 C350,-330 370,-280 350,-240" stroke="{bot}" stroke-width="10" fill="none" opacity="0.35"/>'
    body += f'<path d="M-90,-330 C-150,-300 -160,-260 -130,-240" stroke="{bot}" stroke-width="10" fill="none" opacity="0.35"/>'
    body += '</g><g transform="translate(-20,30)">'
    # muzzle detail: nose, mouth, eye
    body += '<ellipse cx="664" cy="-440" rx="16" ry="12" fill="#0a0606"/><ellipse cx="668" cy="-444" rx="5" ry="3" fill="#ffffff" opacity="0.4"/>'
    if growl:
        body += ('<path d="M668,-426 C640,-412 600,-404 560,-402 C590,-388 630,-392 660,-404 Z" fill="#3a0c0c"/>'
                 '<path d="M650,-422 L644,-404 L640,-420 M628,-416 L622,-398 L616,-414 M606,-412 L600,-394 L594,-410 '
                 'M600,-398 L604,-414 L610,-400 M624,-400 L628,-414 L634,-402" fill="#f4eee0" stroke="#f4eee0" stroke-width="2"/>'
                 f'<path d="M600,-470 C620,-466 640,-458 660,-452" stroke="{bot}" stroke-width="4" fill="none" opacity="0.7"/>'
                 f'<path d="M590,-480 C605,-470 615,-466 630,-466 M580,-462 C600,-458 615,-456 628,-458" stroke="{bot}" stroke-width="3" fill="none" opacity="0.6"/>')
    else:
        body += f'<path d="M668,-426 C640,-416 600,-410 566,-406" stroke="{bot}" stroke-width="4" fill="none" opacity="0.8"/>'
    ex, ey = 560, -472
    if eye == "red":
        body += (f'<circle cx="{ex}" cy="{ey}" r="60" fill="url(#redglow)"/><ellipse cx="{ex}" cy="{ey}" rx="15" ry="10" fill="#ff3a1a"/>'
                 f'<ellipse cx="{ex+2}" cy="{ey}" rx="6" ry="5" fill="#fff0c0"/>')
    else:
        body += (f'<ellipse cx="{ex}" cy="{ey}" rx="12" ry="9" fill="{eye}"/><circle cx="{ex+4}" cy="{ey-3}" r="3" fill="#fff" opacity="0.9"/>'
                 f'<path d="M{ex-16},{ey-6} Q{ex},{ey-18} {ex+16},{ey-8}" stroke="{bot}" stroke-width="4" fill="none" opacity="0.6"/>')
        if eye == "#ffcf8a":
            body += f'<circle cx="{ex}" cy="{ey}" r="40" fill="url(#warmglow)" opacity="0.8"/>'
    body += '</g>'
    # fur: strands along back + neck, and matted locks (cadejos) hanging from belly / neck
    fur = ""
    if not hairless:
        for i in range(70):
            u = r.random(); j = int(u * (len(BACK) - 1)); f = u * (len(BACK) - 1) - j
            x0 = BACK[j][0] + (BACK[j + 1][0] - BACK[j][0]) * f; y0 = BACK[j][1] + (BACK[j + 1][1] - BACK[j][1]) * f + r.uniform(-4, 16)
            L = r.uniform(26, 60)
            fur += (f'<path d="M{x0:.0f},{y0:.0f} q{-L*0.5:.0f},{-6+r.uniform(-6,6):.0f} {-L:.0f},{L*0.35:.0f}" stroke="{furhi if r.random()<0.4 else furc}" '
                    f'stroke-width="{r.uniform(3,7):.1f}" fill="none" stroke-linecap="round" opacity="{r.uniform(0.5,0.95):.2f}"/>')
        locks = 22 if kind == "black" else 12
        for i in range(locks):
            u = r.random(); j = int(u * (len(BELLY) - 1)); f = u * (len(BELLY) - 1) - j
            x0 = BELLY[j][0] + (BELLY[j + 1][0] - BELLY[j][0]) * f; y0 = BELLY[j][1] + (BELLY[j + 1][1] - BELLY[j][1]) * f - 14
            L = r.uniform(40, 95) * (1.3 if kind == "black" else 0.7)
            w = r.uniform(8, 16)
            fur += (f'<path d="M{x0-w:.0f},{y0:.0f} C{x0-w:.0f},{y0+L*0.5:.0f} {x0+r.uniform(-14,14):.0f},{y0+L*0.8:.0f} {x0+r.uniform(-10,10):.0f},{y0+L:.0f} '
                    f'C{x0+w*0.4:.0f},{y0+L*0.6:.0f} {x0+w:.0f},{y0+L*0.3:.0f} {x0+w:.0f},{y0:.0f} Z" fill="{mid if kind=="black" else furc}"/>'
                    f'<path d="M{x0:.0f},{y0+4:.0f} Q{x0+3:.0f},{y0+L*0.5:.0f} {x0:.0f},{y0+L*0.85:.0f}" stroke="{furhi}" stroke-width="2" fill="none" opacity="0.4"/>')
        # neck ruff
        for i in range(26):
            a = r.uniform(-0.2, 1.0); x0 = 400 + 70 * a; y0 = -430 + 120 * a
            fur += (f'<path d="M{x0:.0f},{y0:.0f} q{-30:.0f},{r.uniform(10,30):.0f} {-r.uniform(30,60):.0f},{r.uniform(40,80):.0f}" stroke="{furc}" '
                    f'stroke-width="{r.uniform(4,9):.1f}" fill="none" stroke-linecap="round" opacity="0.85"/>')
    rimp = ""
    if rim:
        rimp = (f'<path d="{smooth(BACK + SKULL_TOP[2:], closed=False)}" stroke="{rim}" stroke-width="7" fill="none" opacity="0.85" filter="url(#blur1)"/>'
                f'<path d="M442,-470 C428,-530 432,-570 448,-592" stroke="{rim}" stroke-width="4" fill="none" opacity="0.7"/>')
    halo = ""
    if kind == "white" and glow_body:
        halo = '<ellipse cx="250" cy="-330" rx="560" ry="300" fill="url(#whiteglow)" opacity="0.45"/>'
    if kind == "black" and glow_body:
        halo = '<ellipse cx="250" cy="-300" rx="520" ry="260" fill="url(#redglow)" opacity="0.18"/>'
    core = f'{legs_far}{tail}{body}{fur}{legs_near}{rimp}'
    if head_turn:  # head looking back: mirror the head region
        pass
    return f'{s}{halo}<g transform="translate(0,{yoff}) rotate({body_rot} -120 -270)">{core}</g>'


def put(frag, x, y, k=1.0, flip=False):
    return f'<g transform="translate({x},{y}) scale({-k if flip else k},{k})">{frag}</g>'


def write(names):
    for n in names:
        open(os.path.join(A, n + ".svg"), "w").write(ART[n]())



# ============================================================================ SCENERY
def corn(x0, x1, ybase, seed, col="#05080a", n=60, hmin=120, hmax=220, hi=None):
    r = random.Random(seed); s = ""
    for _ in range(n):
        x = r.uniform(x0, x1); h = r.uniform(hmin, hmax); y = ybase + r.uniform(-8, 8); lean = r.uniform(-12, 12)
        s += f'<path d="M{x:.0f},{y:.0f} Q{x+lean/2:.0f},{y-h/2:.0f} {x+lean:.0f},{y-h:.0f}" stroke="{col}" stroke-width="{h/40:.1f}" fill="none"/>'
        for k in range(4):
            yy = y - h * (0.25 + 0.17 * k); d = 1 if (k + int(x)) % 2 else -1; L = h * r.uniform(0.25, 0.4)
            s += f'<path d="M{x+lean*(yy-y)/-h:.0f},{yy:.0f} q{d*L*0.5:.0f},{-L*0.3:.0f} {d*L:.0f},{L*0.15:.0f}" stroke="{col}" stroke-width="{h/60:.1f}" fill="none" stroke-linecap="round"/>'
        if hi and r.random() < 0.5:
            s += f'<path d="M{x+lean:.0f},{y-h:.0f} l{-4:.0f},{-18:.0f}" stroke="{hi}" stroke-width="3" opacity="0.6"/>'
    return s


def big_pine(x, yb, h, col="#020406", rim=None, seed=1):
    r = random.Random(seed); s = f'<rect x="{x-h*0.02:.0f}" y="{yb-h*0.3:.0f}" width="{h*0.04:.0f}" height="{h*0.3:.0f}" fill="{col}"/>'
    for i in range(9):
        t = i / 8; y = yb - h * 0.15 - t * h * 0.85; w = h * 0.34 * (1 - t * 0.85)
        jag = " ".join(f"L{x+w*(j/6-0.5)*2:.0f},{y+ (18 if j%2 else 0)+r.uniform(-6,6):.0f}" for j in range(7))
        s += f'<path d="M{x:.0f},{y-h*0.16:.0f} L{x-w:.0f},{y:.0f} {jag} L{x+w:.0f},{y:.0f} Z" fill="{col}"/>'
        if rim:
            s += f'<path d="M{x:.0f},{y-h*0.16:.0f} L{x+w:.0f},{y:.0f}" stroke="{rim}" stroke-width="3" opacity="0.35"/>'
    return s


def stones(x0, x1, y0, y1, seed, n=40, col="#3a3830", hi="#7a8090"):
    r = random.Random(seed); s = ""
    for _ in range(n):
        y = r.uniform(y0, y1); x = r.uniform(x0, x1); k = 0.4 + (y - y0) / max(1, y1 - y0)
        rx = r.uniform(8, 22) * k; ry = rx * 0.55
        s += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rx:.0f}" ry="{ry:.0f}" fill="{col}"/><ellipse cx="{x-rx*0.2:.0f}" cy="{y-ry*0.4:.0f}" rx="{rx*0.5:.0f}" ry="{ry*0.3:.0f}" fill="{hi}" opacity="0.35"/>'
    return s


MOODS = {
    "night": dict(sky=("#03060f", "#16263c"), far="#0d1828", mid="#08111c", ground="#0a0f16", road="#2a2a2a", road2="#14161a", rim=MOONRIM, pine="#03070b"),
    "fog": dict(sky=("#05080e", "#1c2836"), far="#18222e", mid="#0e1620", ground="#0a0e14", road="#262628", road2="#121418", rim="#9fb0c4", pine="#060a0e"),
    "dawn": dict(sky=("#2a3450", "#c08a78"), far="#4a4a62", mid="#2e3046", ground="#22222c", road="#5a4a40", road2="#3a3030", rim="#ffc8a0", pine="#141420"),
}


def road_svg(mood="night", seed=1, moon_xy=(1700, 260), vx=1250, cross=False, fog=0.22, corn_sides=True):
    m = MOODS[mood]; r = random.Random(seed)
    s = sky(*m["sky"])
    if mood != "dawn":
        s += stars(140, seed, 650)
        if moon_xy: s += moon(moon_xy[0], moon_xy[1], 85)
        s += clouds(7, 120, 520, seed + 3, "#24344a", (0.25, 0.5))
    else:
        s += glow(vx, 760, 900, "warm", 0.5)
    s += ridge(760, 90, m["far"], seed + 1, step=30) + ridge(850, 60, m["mid"], seed + 2, step=30)
    s += pines(0, 2400, 860, seed + 4, m["pine"], 50, 120, 90)
    s += f'<rect y="860" width="2400" height="490" fill="{m["ground"]}"/>'
    s += f'<path d="M{vx-30},860 L{vx+30},860 L1950,1350 L450,1350 Z" fill="{m["road"]}"/>'
    s += f'<path d="M{vx-30},860 L{vx+30},860 L1950,1350 L450,1350 Z" fill="#000" opacity="0.35" filter="url(#paper)"/>'
    for off in (-0.45, 0.45):  # ruts
        s += f'<path d="M{vx+off*20:.0f},860 L{1200+off*1000:.0f},1350" stroke="{m["road2"]}" stroke-width="40" opacity="0.5" filter="url(#blur2)"/>'
    s += stones(500, 1900, 900, 1340, seed + 5, 50, "#2c2a26", m["rim"])
    if corn_sides:
        s += corn(0, vx - 120, 1000, seed + 6, m["pine"], 50, 90, 160) + corn(vx + 120, 2400, 1000, seed + 7, m["pine"], 50, 90, 160)
        s += corn(-50, 380, 1350, seed + 8, "#020305", 22, 380, 560, m["rim"]) + corn(2050, 2450, 1350, seed + 9, "#020305", 22, 380, 560, m["rim"])
    else:
        s += big_pine(160, 1360, 1300, m["pine"], m["rim"], seed) + big_pine(2260, 1360, 1200, m["pine"], m["rim"], seed + 1)
        s += big_pine(520, 1100, 600, m["pine"], m["rim"], seed + 2) + big_pine(1950, 1080, 520, m["pine"], m["rim"], seed + 3)
    if cross:
        s += wood_cross(820, 1080, 1.0, m["rim"])
    s += QM.fog_band(980, fog, seed + 10)
    if mood == "fog":
        s += '<rect width="2400" height="1350" fill="#9aaabb" opacity="0.12"/>' + QM.fog_band(900, 0.3, seed + 11) + QM.fog_band(1150, 0.25, seed + 12)
    return s


def wood_cross(x, yb, k=1.0, rim=MOONRIM):
    s = f'<g transform="translate({x},{yb}) scale({k})">'
    s += '<rect x="-16" y="-420" width="32" height="430" fill="#14100c"/><rect x="-120" y="-330" width="240" height="30" fill="#14100c"/>'
    s += f'<path d="M16,-420 L16,10 M120,-330 L120,-300" stroke="{rim}" stroke-width="4" opacity="0.6"/>'
    s += '<path d="M-10,-300 C-30,-280 -40,-240 -30,-200" stroke="#3a3020" stroke-width="5" fill="none"/>'
    for i in range(7):  # dried cempasúchil + stones
        a = -60 + i * 20
        s += f'<circle cx="{a}" cy="{-8 - (i%2)*10}" r="14" fill="#8a4a10"/><circle cx="{a}" cy="{-8 - (i%2)*10}" r="6" fill="#c07a20"/>'
    s += stones(-90, 90, -10, 10, 3, 10, "#2a2620", rim)
    s += '<rect x="-60" y="-26" width="16" height="26" fill="#d8ccb0"/><circle cx="-52" cy="-36" r="30" fill="url(#warmglow)" opacity="0.5"/>'
    return s + '</g>'


TOMAS_WALK = man_full(hat=True, cape=False, walk=0.4, rim=MOONRIM)


@art
def road_night(): return S(road_svg("night", 1))
@art
def road_night2(): return S(road_svg("night", 5, (600, 230), vx=1150, corn_sides=False))
@art
def road_fog(): return S(road_svg("fog", 9, None, vx=1200, fog=0.3, corn_sides=False))
@art
def l_tomas_walk(): return S(put(TOMAS_WALK, 1050, 1260, 0.62))
@art
def l_black(): return S(put(dog("black", "stand", growl=True, rim="#8ea0c0"), 1420, 1060, 0.45, flip=True))
EYE = (1200, 830)
@art
def l_eyes():
    s = ""
    for dx in (-22, 22):
        s += f'<circle cx="{EYE[0]+dx}" cy="{EYE[1]}" r="70" fill="url(#redglow)" opacity="0.9"/><ellipse cx="{EYE[0]+dx}" cy="{EYE[1]}" rx="9" ry="6" fill="#ff5030"/>'
    return S(s)
@art
def l_white(): return S(put(dog("white", "walk"), 850, 1250, 0.42))
@art
def l_white_glow(): return S(glow(1200, 900, 700, "white", 0.25))
@art
def l_fire_glow(): return S(glow(800, 850, 900, "warm", 0.35))
@art
def l_fog(): return PA.ART["l_fog"]()
@art
def l_candle_glow(): return PA.ART["l_candle_glow"]()
@art
def l_smoke():
    s = clouds(10, 700, 1250, 31, "#c8b060", (0.08, 0.22), (200, 500), (40, 120)) + clouds(6, 900, 1300, 32, "#a04020", (0.06, 0.14), (200, 400), (40, 100))
    return S(s)
@art
def road_walk_two():
    s = road_svg("night", 13, (1900, 240), vx=1300)
    s += put(TOMAS_WALK, 1080, 1260, 0.62) + put(dog("white", "walk"), 1180, 1262, 0.36)
    return S(s)
@art
def hooves():
    s = '<rect width="2400" height="1350" fill="#06080c"/>' + glow(1300, 700, 1100, "moon", 0.35)
    s += '<path d="M0,1000 C600,960 1800,980 2400,1000 L2400,1350 L0,1350 Z" fill="#1a1a1c"/>'
    s += stones(0, 2400, 1000, 1340, 41, 70, "#2e2c2a", "#8a96a8")
    # two huge goat legs stepping, with shaggy fur
    for lx, ang, lift in ((1050, 6, 0), (1500, -10, -60)):
        s += f'<g transform="translate({lx},{1060+lift}) rotate({ang})">'
        s += '<path d="M-95,-1100 C-100,-700 -80,-400 -60,-120 L60,-120 C80,-400 100,-700 95,-1100 Z" fill="#050507"/>'
        r = random.Random(lx)
        for _ in range(40):
            y = r.uniform(-1080, -140); x = r.choice((-1, 1)) * r.uniform(50, 100)
            s += f'<path d="M{x:.0f},{y:.0f} q{x*0.4:.0f},40 {x*0.2+r.uniform(-20,20):.0f},{r.uniform(70,140):.0f}" stroke="#16161c" stroke-width="{r.uniform(6,12):.0f}" fill="none" stroke-linecap="round"/>'
        s += '<path d="M-60,-1100 C-70,-700 -50,-400 -40,-120" stroke="#8ea0c0" stroke-width="5" fill="none" opacity="0.6" filter="url(#blur1)"/>'
        s += '<path d="M-70,-130 L70,-130 L96,0 L-90,0 Z" fill="#1e1a16"/><path d="M6,-120 L10,0" stroke="#000" stroke-width="12"/>'
        s += '<path d="M-70,-130 L70,-130" stroke="#6a5e50" stroke-width="5"/><path d="M60,-130 L96,0" stroke="#8ea0c0" stroke-width="4" opacity="0.6"/>'
        s += '</g>'
    s += '<ellipse cx="1500" cy="1010" rx="160" ry="30" fill="#c8b060" opacity="0.08" filter="url(#blur3)"/>'
    return S(s, QM.fog_band(1180, 0.18, 42))
@art
def black_eyes():
    s = '<rect width="2400" height="1350" fill="#020203"/>' + glow(1200, 620, 900, "red", 0.35)
    # shaggy head silhouette, front view
    head = "M1200,330 C1360,330 1470,420 1500,560 C1530,700 1460,820 1380,880 C1330,920 1260,960 1200,970 C1140,960 1070,920 1020,880 C940,820 870,700 900,560 C930,420 1040,330 1200,330 Z"
    s += f'<path d="{head}" fill="#060608"/>'
    s += '<path d="M960,430 L900,180 L1080,370 Z M1440,430 L1500,180 L1320,370 Z" fill="#060608"/>'
    s += '<path d="M960,430 L900,180 L1080,370 M1440,430 L1500,180 L1320,370" stroke="#c03020" stroke-width="5" fill="none" opacity="0.5"/>'
    r = random.Random(5)
    for _ in range(80):
        a = r.uniform(0, math.pi); x = 1200 + math.cos(a) * r.uniform(260, 320); y = 640 + math.sin(a) * r.uniform(240, 330)
        s += f'<path d="M{x:.0f},{y:.0f} q{r.uniform(-20,20):.0f},40 {r.uniform(-30,30):.0f},{r.uniform(60,140):.0f}" stroke="#0a0a0e" stroke-width="{r.uniform(8,16):.0f}" fill="none" stroke-linecap="round"/>'
    s += '<path d="M1110,820 C1150,880 1250,880 1290,820 C1260,860 1140,860 1110,820 Z" fill="#000"/><ellipse cx="1200" cy="800" rx="46" ry="30" fill="#000"/>'
    for ex in (1080, 1320):
        s += f'<circle cx="{ex}" cy="590" r="150" fill="url(#redglow)"/><path d="M{ex-50},590 Q{ex},550 {ex+50},590 Q{ex},620 {ex-50},590 Z" fill="#ff3a14"/><ellipse cx="{ex}" cy="590" rx="10" ry="22" fill="#200000"/>'
    s += f'<path d="{head}" stroke="#c03020" stroke-width="5" fill="none" opacity="0.35" filter="url(#blur1)"/>'
    return S(s, QM.fog_band(1150, 0.3, 6))
def head_close(kind, growl=False, bg=None, eye=None, rim=MOONRIM, k=2.6):
    bg = bg or (portrait_bg("moon") if kind == "white" else '<rect width="2400" height="1350" fill="#030305"/>' + glow(1500, 500, 900, "red", 0.4))
    d = dog(kind, "stand", growl=growl, eye=eye, rim=rim, seed=7)
    return S(bg, f'<g transform="translate(1200,675) scale({k}) translate(-480,440)">{d}</g>', QM.fog_band(1300, 0.18, 4))
@art
def white_close(): return head_close("white")
@art
def white_growl(): return head_close("white", growl=True, k=3.0)
@art
def white_look():
    s = portrait_bg("moon")
    return S(s, f'<g transform="translate(1200,675) scale(-2.2,2.2) translate(-420,430)">{dog("white","stand",seed=8)}</g>', QM.fog_band(1300, 0.18, 4))
@art
def black_close(): return head_close("black", growl=True, rim="#c06050", k=2.8)
@art
def white_full():
    s = road_svg("night", 21, (1200, 300), vx=1200, cross=False)
    s += glow(1200, 1080, 500, "white", 0.45) + put(dog("white", "stand", seed=3), 980, 1200, 0.65)
    return S(s)
@art
def black_full():
    s = road_svg("fog", 23, None, vx=1200, fog=0.28, corn_sides=False) + '<rect width="2400" height="1350" fill="#000" opacity="0.3"/>'
    s += put(dog("black", "stand", growl=True, rim="#c06050", seed=4), 1520, 1220, 0.75, flip=True)
    s += chain_svg(1400, 1210, 0.7)
    return S(s, QM.fog_band(1260, 0.2, 24))
def chain_svg(x, y, k=1.0, n=14):
    s = f'<g transform="translate({x},{y}) scale({k})">'
    for i in range(n):
        cx = -i * 46; cy = math.sin(i * 0.7) * 8
        if i % 2:
            s += f'<ellipse cx="{cx}" cy="{cy}" rx="30" ry="9" fill="none" stroke="#2a2420" stroke-width="10"/><ellipse cx="{cx}" cy="{cy-3}" rx="30" ry="9" fill="none" stroke="#8a6a50" stroke-width="3" opacity="0.6"/>'
        else:
            s += f'<ellipse cx="{cx}" cy="{cy}" rx="30" ry="18" fill="none" stroke="#2a2420" stroke-width="10"/><path d="M{cx-26},{cy-8} A30,18 0 0 1 {cx+26},{cy-8}" fill="none" stroke="#b08a60" stroke-width="3" opacity="0.6"/>'
    return s + '</g>'
@art
def chain():
    s = '<rect width="2400" height="1350" fill="#06070a"/>' + glow(1600, 900, 900, "red", 0.3)
    s += '<path d="M0,900 C600,880 1800,890 2400,900 L2400,1350 L0,1350 Z" fill="#16161a"/>' + stones(0, 2400, 920, 1340, 51, 60, "#2a2826", "#8a8a96")
    s += chain_svg(2200, 1080, 1.8, 26)
    s += '<g transform="translate(2150,1060)"><path d="M-70,-130 L70,-130 L96,0 L-90,0 Z" fill="#1e1a16"/><path d="M6,-120 L10,0" stroke="#000" stroke-width="12"/><path d="M-60,-700 L60,-700 L70,-130 L-70,-130 Z" fill="#050507"/></g>'
    return S(s, QM.fog_band(1250, 0.15, 52))
@art
def moon_two():
    s = sky("#02040a", "#121e30") + stars(200, 61, 900) + moon(1200, 560, 380)
    s += '<path d="M0,1080 C500,980 900,960 1200,960 C1500,960 1900,980 2400,1080 L2400,1350 L0,1350 Z" fill="#020305"/>'
    s += put(dog("white", "stand", seed=11, glow_body=True), 560, 970, 0.75) + put(dog("black", "stand", growl=True, seed=12, rim="#ffffff"), 1840, 970, 0.75, flip=True)
    return S(s, QM.fog_band(1050, 0.3, 62))
@art
def title_bg():
    s = road_svg("night", 71, (1200, 380), vx=1200, fog=0.28, corn_sides=False) + '<rect width="2400" height="1350" fill="#000" opacity="0.25"/>'
    s += put(dog("white", "stand", seed=13), 520, 1250, 0.5) + put(dog("black", "stand", growl=True, seed=14, rim="#9fb0d0"), 1880, 1250, 0.5, flip=True)
    return S(s)
@art
def fiesta():
    s = sky("#05070f", "#1a1a2c") + stars(80, 81, 400) + town(980, 82, "night", 30) + church(1200, 960, 1.2)
    s += '<rect y="960" width="2400" height="390" fill="#1a1410"/>' + glow(1200, 980, 1100, "warm", 0.6)
    s += papel_picado(160, "#b3122e", 10, 3) + papel_picado(300, "#e0a020", 10, 4, 0.8) + papel_picado(440, "#2a7aa0", 10, 5, 0.7)
    for i in range(12):  # lanterns
        s += glow(120 + i * 200, 520 + (i % 2) * 30, 60, "warm", 0.9)
    # marimba with 4 players
    s += '<g transform="translate(1200,1180)"><rect x="-420" y="-160" width="840" height="40" fill="#3a2010"/>'
    for i in range(28):
        s += f'<rect x="{-410+i*30}" y="-170" width="24" height="{30+ (i%3)*4}" fill="#8a5a2a"/><rect x="{-404+i*30}" y="-120" width="12" height="{60+i*3}" fill="#2a1408"/>'
    s += '<path d="M-400,-120 L-420,0 M400,-120 L420,0" stroke="#2a1408" stroke-width="14"/></g>'
    for i, x in enumerate((900, 1100, 1300, 1500)):
        s += put(man_full(hat=True, cape=False, rim=WARM, fill="#0a0604"), x, 1230, 0.42)
    for i in range(14):  # dancers
        x = 150 + i * 160 + (i % 3) * 30
        if 700 < x < 1700: continue
        f = woman_full(rim=WARM, fill="#0c0806") if i % 2 else man_full(hat=True, cape=False, walk=0.3, rim=WARM, fill="#0c0806")
        s += put(f, x, 1330, 0.42, flip=bool(i % 3))
    return S(s, '<rect width="2400" height="1350" fill="#ff8030" opacity="0.06"/>')
@art
def marimba():
    s = '<rect width="2400" height="1350" fill="#0c0604"/>' + glow(1200, 400, 1300, "warm", 0.55)
    for i in range(22):
        x = -100 + i * 120; w = 104; h = 520 - i * 10
        s += f'<path d="M{x},{560} L{x+w},{560} L{x+w-6},{560+40} L{x+6},{600} Z" fill="#7a4a20"/>'
        s += f'<rect x="{x}" y="{520}" width="{w}" height="44" fill="#a8703a"/><rect x="{x}" y="520" width="{w}" height="8" fill="#e0a868" opacity="0.7"/>'
        s += f'<circle cx="{x+w/2}" cy="542" r="5" fill="#3a2010"/>'
        s += f'<rect x="{x+w/2-26}" y="610" width="52" height="{h}" fill="#2a1408"/><rect x="{x+w/2-26}" y="610" width="10" height="{h}" fill="#6a3a18" opacity="0.6"/>'
    for x, y, a in ((800, 300, 20), (1100, 260, -15), (1500, 330, 30), (1750, 280, -25)):
        s += f'<g transform="translate({x},{y}) rotate({a})"><rect x="-6" y="0" width="12" height="260" fill="#c8a070"/><circle cx="0" cy="0" r="30" fill="#2a1a18"/><circle cx="-8" cy="-8" r="8" fill="#6a5a50"/></g>'
    s += '<rect y="1100" width="2400" height="250" fill="#000" opacity="0.5" filter="url(#blur3)"/>'
    return S(s)
@art
def kitchen():
    s = room_walls("#2a1e16", "#0c0806", "#1a120c")
    s += '<path d="M500,820 L1300,820 L1300,1120 L500,1120 Z" fill="#4a3020"/><path d="M500,820 L1300,820" stroke="#8a6040" stroke-width="10"/>'
    s += '<ellipse cx="900" cy="800" rx="300" ry="40" fill="#1a1a1a"/><ellipse cx="900" cy="796" rx="280" ry="30" fill="#2a2a2a"/>'
    s += glow(900, 900, 500, "warm", 0.9) + flame(760, 900, 1.6) + flame(900, 910, 2.0) + flame(1040, 900, 1.5)
    s += '<path d="M600,900 L1200,900 L1200,1000 L600,1000 Z" fill="#000" opacity="0.4"/>'
    for i, (x, h) in enumerate(((1500, 220), (1650, 180), (1800, 260))):
        s += f'<path d="M{x-80},{1120} C{x-110},{1120-h*0.5} {x-90},{1120-h} {x-40},{1120-h} L{x+40},{1120-h} C{x+90},{1120-h} {x+110},{1120-h*0.5} {x+80},{1120} Z" fill="#6a3a20"/>'
        s += f'<path d="M{x-40},{1120-h} C{x-30},{1120-h*0.6} {x-60},{1120-h*0.3} {x-70},{1100}" stroke="#ffb860" stroke-width="5" fill="none" opacity="0.5"/>'
    s += '<g transform="translate(1900,1300) scale(0.9)">' + woman_full(rebozo_head=True, old=True, rim="#ffb860", fill="#0c0806") + '</g>'
    s += '<path d="M0,0 L2400,0 L2400,120 L0,120 Z" fill="#0a0604"/>'
    for i in range(6): s += f'<rect x="{i*420}" y="100" width="40" height="60" fill="#1a0e08"/>'
    return S(s)



# ---------------------------------------------------------------- people
def tomas(**kw):
    return luis_bust(1200, 560, 1.75, **kw)
def palm_hat(cx, cy, k=1.0, rim=MOONRIM):
    s = f'<g transform="translate({cx},{cy}) scale({k})">'
    s += '<ellipse cx="0" cy="0" rx="330" ry="62" fill="#8a6a3a"/><ellipse cx="0" cy="-8" rx="300" ry="46" fill="#a8844a"/>'
    s += '<path d="M-140,-10 C-140,-150 -90,-200 0,-206 C90,-200 140,-150 140,-10 Z" fill="#b8945a"/>'
    s += '<path d="M-140,-30 C-60,-10 60,-10 140,-30 L140,-60 C60,-40 -60,-40 -140,-60 Z" fill="#3a2010"/>'
    for i in range(14):
        s += f'<path d="M{-300+i*44},-10 Q{-290+i*44},20 {-280+i*44},34" stroke="#6a4a24" stroke-width="3" fill="none" opacity="0.5"/>'
    s += f'<path d="M-330,0 C-200,-60 200,-60 330,0" stroke="{rim}" stroke-width="5" fill="none" opacity="0.5"/>'
    return s + '</g>'
HATP = (1200 - 8, 560 - 125 * 1.75 + 62)
@art
def tomas_portrait(): return S(portrait_bg("moon"), tomas(look=-0.2, turn=-0.1), palm_hat(HATP[0], HATP[1], 1.0))
@art
def tomas_smile(): return S(portrait_bg("candle"), tomas(look=0.3, turn=0.1, smile=0.8, rim="#ffb860"), palm_hat(HATP[0], HATP[1], 1.0, "#ffb860"))
@art
def tomas_fear(): return S(portrait_bg("moon"), tomas(look=0.5, turn=0.15, shock=True), palm_hat(HATP[0], HATP[1], 1.0))
@art
def tomas_trance(): return S(portrait_bg("red"), tomas(look=0.0, lids=0.65, smile=0.0, rim="#ff6040"), palm_hat(HATP[0], HATP[1], 1.0, "#ff6040"))
@art
def tomas_pray():
    s = portrait_bg("moon") + tomas(look=0.0, lids=0.85, smile=0.0)
    # joined hands in front of chest
    s += '<g transform="translate(1200,1180)">'
    s += '<path d="M-150,170 C-110,60 -60,-40 -30,-140 C-20,-180 0,-200 10,-180 C40,-120 30,20 60,170 Z" fill="#a8774f"/>'
    s += '<path d="M150,170 C110,60 60,-40 30,-140 C20,-180 0,-200 -10,-180 C-40,-120 -30,20 -60,170 Z" fill="#c99668"/>'
    for i in range(4): s += f'<path d="M{-14+i*2},{-160+i*30} L{18},{-150+i*30}" stroke="#6c4630" stroke-width="3" opacity="0.6"/>'
    s += '</g>'
    return S(s, palm_hat(HATP[0], HATP[1], 1.0))
@art
def old_tomas(): return S(portrait_bg("candle"), father_bust(1200, 560, 1.75, rim="#ffb860"))
@art
def abuela(): return S(portrait_bg("candle"), brigida_bust(1200, 560, 1.75))
@art
def red_flash(): return PA.ART["red_flash"]()


# ---------------------------------------------------------------- places
def adobe_house(x, yb, k=1.0, door_lit=True):
    s = f'<g transform="translate({x},{yb}) scale({k})">'
    s += '<rect x="-420" y="-380" width="840" height="380" fill="#3a2a22"/><rect x="-420" y="-380" width="840" height="380" fill="#000" filter="url(#plaster)" opacity="0.4"/>'
    s += '<path d="M-480,-370 L0,-560 L480,-370 Z" fill="#4a1a12"/>'
    for i in range(16): s += f'<path d="M{-470+i*60},-372 L{-10+i*0.5},-555" stroke="#2a0a06" stroke-width="5" opacity="0.6"/>'
    s += '<path d="M-480,-370 L480,-370" stroke="#1a0804" stroke-width="12"/>'
    if door_lit:
        s += glow(-60, -150, 380, "warm", 0.9) + '<rect x="-140" y="-300" width="160" height="300" fill="#ffb860"/><rect x="-140" y="-300" width="160" height="300" fill="#c86020" opacity="0.4"/>'
    else:
        s += '<rect x="-140" y="-300" width="160" height="300" fill="#0a0604"/>'
    s += '<rect x="180" y="-260" width="110" height="110" fill="#1a0e08"/><path d="M190,-250 L280,-250 M235,-260 L235,-150" stroke="#000" stroke-width="10"/>'
    s += '<rect x="-160" y="-310" width="200" height="14" fill="#1a0e08"/>'
    return s + '</g>'
@art
def house():
    s = road_svg("night", 91, (1900, 220), vx=1200, corn_sides=True)
    s += '<rect y="900" width="2400" height="450" fill="#0a0e14" opacity="0.6"/>' + adobe_house(1250, 1080, 1.1) + glow(1180, 1060, 500, "warm", 0.35)
    s += corn(1700, 2400, 1150, 92, "#020305", 20, 260, 420, MOONRIM)
    return S(s)
@art
def abuela_door():
    s = '<rect width="2400" height="1350" fill="#05070c"/>' + '<rect x="0" y="0" width="2400" height="1350" fill="#2a2018" opacity="0.6" filter="url(#plaster)"/>'
    s += '<rect x="800" y="150" width="800" height="1200" fill="#ffb060"/>' + glow(1200, 800, 900, "warm", 0.9)
    s += '<rect x="800" y="150" width="800" height="1200" fill="#c86020" opacity="0.35"/>'
    s += '<rect x="760" y="110" width="40" height="1240" fill="#1a0e08"/><rect x="1600" y="110" width="40" height="1240" fill="#1a0e08"/><rect x="760" y="110" width="880" height="50" fill="#1a0e08"/>'
    s += put(woman_full(rebozo_head=True, old=True, rim="#ffd27a", fill="#060402"), 1200, 1330, 1.2)
    s += '<path d="M800,1350 L0,1350 L0,1200 Z" fill="#000" opacity="0.4"/><path d="M1600,1350 L2400,1350 L2400,1150 Z" fill="#ffb060" opacity="0.15"/>'
    return S(s)
def plate(x, y, k=1.0, full=True, mood="warm"):
    s = f'<g transform="translate({x},{y}) scale({k})">'
    s += '<ellipse cx="0" cy="0" rx="230" ry="70" fill="#5a2a14"/><ellipse cx="0" cy="-10" rx="200" ry="56" fill="#8a4a24"/>'
    s += '<path d="M-200,-10 C-180,30 180,30 200,-10" stroke="#c88050" stroke-width="5" fill="none" opacity="0.6"/>'
    for i in range(12): s += f'<path d="M{-150+i*27},{-30+ (i%2)*8} l8,10" stroke="#e8c070" stroke-width="5" opacity="0.6"/>'
    if full:
        for i in range(5):
            s += f'<ellipse cx="{(i-2)*6}" cy="{-30-i*12}" rx="150" ry="42" fill="#e8d4a0"/><ellipse cx="{(i-2)*6}" cy="{-30-i*12}" rx="150" ry="42" fill="none" stroke="#b89860" stroke-width="3"/>'
        s += '<ellipse cx="30" cy="-84" rx="16" ry="6" fill="#8a6030" opacity="0.6"/><ellipse cx="-50" cy="-80" rx="12" ry="5" fill="#8a6030" opacity="0.6"/>'
    else:
        s += '<ellipse cx="0" cy="-14" rx="150" ry="36" fill="#6a3418" opacity="0.6"/>'
    return s + '</g>'
@art
def door_plate():
    s = '<rect width="2400" height="1350" fill="#06080e"/>' + glow(700, 600, 900, "warm", 0.7)
    s += '<rect x="200" y="0" width="900" height="1000" fill="#ffb060" opacity="0.85"/><rect x="200" y="0" width="900" height="1000" fill="#c86020" opacity="0.4"/>'
    s += '<rect x="1100" y="0" width="1300" height="1000" fill="#2a2018"/><rect x="1100" y="0" width="1300" height="1000" fill="#000" filter="url(#plaster)" opacity="0.5"/><rect x="1100" y="0" width="60" height="1000" fill="#140a06"/>'
    s += '<path d="M0,1000 L2400,1000 L2400,1350 L0,1350 Z" fill="#1a140e"/><rect x="150" y="960" width="1100" height="60" fill="#3a2a1a"/>'
    s += stones(1300, 2400, 1050, 1340, 93, 30, "#2a2420", MOONRIM) + plate(1500, 1120, 1.4)
    s += '<path d="M1100,1000 L1700,1350 L1100,1350 Z" fill="#ffb060" opacity="0.1"/>'
    return S(s)
@art
def plate_empty():
    s = '<rect width="2400" height="1350" fill="#3a3a48"/>' + glow(1600, 300, 1200, "warm", 0.35)
    s += '<path d="M0,800 L2400,800 L2400,1350 L0,1350 Z" fill="#4a3c32"/>' + stones(0, 2400, 820, 1340, 94, 40, "#3a3028", "#c8b8a8")
    s += plate(1200, 1060, 2.0, full=False)
    for dx, dy in ((-560, 30), (-420, 160), (420, 120), (560, 260), (700, 60)):
        s += paw_print(1200 + dx, 1060 + dy, 1.1, "#2a2018")
    return S(s)
def paw_print(x, y, k=1.0, col="#1a120c"):
    s = f'<g transform="translate({x},{y}) scale({k})"><ellipse cx="0" cy="0" rx="34" ry="26" fill="{col}"/>'
    for dx, dy in ((-36, -34), (-12, -48), (14, -48), (38, -34)): s += f'<ellipse cx="{dx}" cy="{dy}" rx="11" ry="14" fill="{col}"/>'
    return s + '</g>'
def hoof_print(x, y, k=1.0, col="#120c08"):
    return (f'<g transform="translate({x},{y}) scale({k})"><path d="M-30,30 C-40,-10 -30,-40 -6,-46 L-6,30 Z" fill="{col}"/>'
            f'<path d="M30,30 C40,-10 30,-40 6,-46 L6,30 Z" fill="{col}"/></g>')
@art
def prints():
    s = '<rect width="2400" height="1350" fill="#4a3e36"/>' + glow(1800, 0, 1200, "warm", 0.3)
    s += '<rect width="2400" height="1350" fill="#2a2018" opacity="0.5" filter="url(#paper)"/>'
    s += '<path d="M0,0 L2400,0 L2400,240 C1600,300 800,200 0,280 Z" fill="#3a4a5a" opacity="0.7"/>'
    r = random.Random(95)
    for i in range(9):
        s += paw_print(200 + i * 240, 700 + math.sin(i) * 120, 1.5, "#1a120c")
    for i in range(9):
        s += hoof_print(300 + i * 230, 950 + math.cos(i) * 110, 1.6, "#0c0604")
    for _ in range(30):
        x = r.uniform(0, 2400); y = r.uniform(400, 1350)
        s += f'<path d="M{x:.0f},{y:.0f} l{r.uniform(-60,60):.0f},{r.uniform(-10,10):.0f}" stroke="#6a5a4a" stroke-width="3" opacity="0.5"/>'
    return S(s)
def bridge_svg(mood="night", seed=1):
    m = MOODS[mood]
    s = sky(*m["sky"])
    if mood != "dawn": s += stars(120, seed, 500) + moon(1800, 240, 80)
    else: s += glow(1400, 700, 1000, "warm", 0.5)
    s += ridge(700, 100, m["far"], seed + 1, step=30) + pines(0, 2400, 760, seed + 2, m["pine"], 60, 160, 90)
    s += f'<rect y="760" width="2400" height="590" fill="{m["ground"]}"/>'
    s += f'<path d="M0,980 C600,940 1800,960 2400,990 L2400,1350 L0,1350 Z" fill="{"#0c1a26" if mood!="dawn" else "#4a5a6a"}"/>'
    s += reflection(1800 if mood != "dawn" else 1400, 990, 1350)
    s += reeds(0, 600, 1060, seed + 3, m["pine"], 60, 160) + reeds(1800, 2400, 1060, seed + 4, m["pine"], 60, 160)
    # wooden bridge (planks + rails), slight arc
    s += '<path d="M300,860 C900,800 1500,800 2100,860 L2100,900 C1500,840 900,840 300,900 Z" fill="#2a1e14"/>'
    for i in range(60):
        x = 320 + i * 30; y = 860 - math.sin((x - 300) / 1800 * math.pi) * 60
        s += f'<rect x="{x}" y="{y-6:.0f}" width="24" height="44" fill="#3a2a1c"/>'
    for x in range(320, 2101, 180):
        y = 860 - math.sin((x - 300) / 1800 * math.pi) * 60
        s += f'<rect x="{x}" y="{y-120:.0f}" width="22" height="300" fill="#1a120c"/>'
        s += f'<path d="M{x+22},{y-120:.0f} L{x+22},{y+180:.0f}" stroke="{m["rim"]}" stroke-width="3" opacity="0.4"/>'
    s += '<path d="M300,740 C900,680 1500,680 2100,740" stroke="#1a120c" stroke-width="18" fill="none"/>'
    s += f'<path d="M300,732 C900,672 1500,672 2100,732" stroke="{m["rim"]}" stroke-width="3" fill="none" opacity="0.5"/>'
    s += big_pine(120, 1300, 1200, m["pine"], m["rim"], seed) + big_pine(2300, 1300, 1100, m["pine"], m["rim"], seed + 5)
    return s
@art
def bridge(): return S(bridge_svg("night", 101), QM.fog_band(900, 0.25, 102))
@art
def bridge_dawn(): return S(bridge_svg("dawn", 103), QM.fog_band(900, 0.25, 104))
def bridge_persp(seed=1, red=False):
    s = sky("#02040a", "#121c2a") + glow(1200, 760, 700, "red" if red else "moon", 0.3)
    s += pines(0, 2400, 780, seed, "#04070c", 120, 260, 70)
    s += '<rect y="780" width="2400" height="570" fill="#05080c"/>'
    vx, vy = 1200, 780
    s += f'<path d="M{vx-90},{vy} L{vx+90},{vy} L2000,1350 L400,1350 Z" fill="#1e160e"/>'
    for i in range(26):
        t = (i / 25) ** 2.2; y = vy + (1350 - vy) * t; hw = 90 + (800 - 90) * t
        s += f'<path d="M{vx-hw:.0f},{y:.0f} L{vx+hw:.0f},{y:.0f}" stroke="#0a0604" stroke-width="{2+10*t:.1f}"/>'
        s += f'<path d="M{vx-hw:.0f},{y-3-6*t:.0f} L{vx+hw:.0f},{y-3-6*t:.0f}" stroke="#4a3a28" stroke-width="{1+3*t:.1f}" opacity="0.5"/>'
    for side in (-1, 1):
        for i in range(8):
            t = (i / 7) ** 2.2; y = vy + (1350 - vy) * t; x = vx + side * (110 + 900 * t); h = 60 + 600 * t
            s += f'<rect x="{x-6-10*t:.0f}" y="{y-h:.0f}" width="{12+20*t:.0f}" height="{h:.0f}" fill="#0c0806"/>'
        s += f'<path d="M{vx+side*110},{vy-60} L{vx+side*1010},{1350-660}" stroke="#0c0806" stroke-width="16"/>'
        s += f'<path d="M{vx+side*110},{vy-64} L{vx+side*1010},{1350-668}" stroke="{MOONRIM}" stroke-width="3" opacity="0.4"/>'
    return s
@art
def bridge_far(): return S(bridge_persp(111), QM.fog_band(840, 0.18, 112), '<rect width="2400" height="1350" fill="#000" opacity="0.15"/>')
@art
def bridge_steps():
    s = bridge_persp(113, red=True)
    s += '<g transform="translate(1200,1400) scale(1.4)"><path d="M-160,-400 C-170,-300 -180,-150 -190,-30 L-80,-20 C-80,-150 -60,-300 -40,-400 Z" fill="#06070a"/>'
    s += '<path d="M40,-400 C70,-300 110,-200 140,-80 L250,-100 C220,-220 160,-330 150,-400 Z" fill="#06070a"/>'
    s += '<path d="M-200,-40 L-60,-30 L-50,0 L-210,0 Z M130,-100 L270,-120 L290,-90 L140,-70 Z" fill="#1a120c"/></g>'
    s += glow(1200, 760, 300, "red", 0.5)
    for dx in (-18, 18): s += f'<ellipse cx="{1200+dx}" cy="770" rx="7" ry="5" fill="#ff5030"/>'
    return S(s, QM.fog_band(820, 0.3, 114))
@art
def standoff():
    s = bridge_persp(121) + '<rect width="2400" height="1350" fill="#000" opacity="0.1"/>'
    s += put(dog("black", "stand", growl=True, rim="#c06050", seed=21), 1330, 930, 0.32, flip=True)
    s += put(dog("white", "crouch", growl=True, seed=22), 820, 1240, 0.62)
    s += put(man_full(hat=True, cape=False, rim=MOONRIM), 380, 1420, 0.75)
    return S(s, QM.fog_band(880, 0.25, 122))
@art
def white_leap():
    s = bridge_persp(131) + '<rect width="2400" height="1350" fill="#000" opacity="0.2"/>'
    for i in range(10):
        s += f'<path d="M{200+i*30},{700+i*28} L{900+i*20},{680+i*26}" stroke="#ffffff" stroke-width="{4+i%3*3}" opacity="0.25" filter="url(#blur1)"/>'
    s += put(dog("white", "leap", growl=True, seed=23), 1000, 1150, 0.95)
    return S(s)
def sparks(cx, cy, seed, n=40, spread=500):
    r = random.Random(seed); s = ""
    for _ in range(n):
        a = r.uniform(0, 2 * math.pi); d = r.uniform(30, spread); L = r.uniform(10, 40)
        x = cx + math.cos(a) * d; y = cy + math.sin(a) * d * 0.6
        s += f'<path d="M{x:.0f},{y:.0f} l{math.cos(a)*L:.0f},{math.sin(a)*L*0.6:.0f}" stroke="#ffd080" stroke-width="{r.uniform(2,5):.1f}" opacity="{r.uniform(0.5,1):.2f}"/>'
    return s + glow(cx, cy, 400, "warm", 0.4)
@art
def fight():
    s = sky("#02040a", "#16203a") + moon(1200, 520, 330) + stars(100, 141, 400)
    s += '<path d="M0,1050 C800,1000 1600,1000 2400,1050 L2400,1350 L0,1350 Z" fill="#030406"/>'
    s += f'<g transform="translate(980,1060) scale(0.85) rotate(-35)">{dog("white", "rear", growl=True, seed=24)}</g>'
    s += f'<g transform="translate(1460,1060) scale(-0.85,0.85) rotate(-35)">{dog("black", "rear", growl=True, seed=25, rim="#ffffff")}</g>'
    s += sparks(1220, 700, 141)
    return S(s, QM.fog_band(1080, 0.3, 142))
@art
def fight2():
    s = '<rect width="2400" height="1350" fill="#04060a"/>' + glow(1200, 700, 1000, "moon", 0.35)
    s += f'<g filter="url(#blur3)" opacity="0.85"><g transform="translate(900,980) scale(0.9) rotate(20)">{dog("white", "leap", seed=26)}</g>'
    s += f'<g transform="translate(1600,820) scale(-0.9,0.9) rotate(-160 250 -300)">{dog("black", "leap", growl=True, seed=27)}</g></g>'
    s += sparks(1250, 760, 143, 60, 600)
    return S(s, QM.fog_band(900, 0.3, 144), QM.fog_band(1200, 0.3, 145))
@art
def cross_road():
    s = road_svg("night", 151, (1800, 230), vx=1350)
    s += wood_cross(1200, 1150, 1.4)
    return S(s)
@art
def pines_bg():
    s = road_svg("night", 161, (700, 200), vx=1200, corn_sides=False)
    for i, x in enumerate((600, 850, 1600, 1850, 2050)):
        s += big_pine(x, 1060 - i % 2 * 40, 700 + (i % 3) * 120, "#03060a", MOONRIM, 160 + i)
    return S(s)
@art
def milpa():
    s = road_svg("night", 171, (1500, 260), vx=900, corn_sides=False)
    s += corn(1100, 2400, 1150, 172, "#020305", 60, 300, 520, MOONRIM) + corn(0, 500, 1250, 173, "#020305", 20, 400, 600, MOONRIM)
    s += put(TOMAS_WALK, 820, 1160, 0.45)
    return S(s)
@art
def drunk():
    s = road_svg("night", 181, (1700, 230), vx=1500, corn_sides=False)
    s += '<path d="M600,1200 C600,900 620,600 560,300 L700,300 C720,600 760,900 780,1200 Z" fill="#05070a"/>'
    s += '<path d="M640,400 C500,300 400,250 300,240 M700,380 C820,280 960,240 1060,250" stroke="#05070a" stroke-width="40" fill="none"/>'
    # man sitting against trunk, hat over face
    s += '<g transform="translate(760,1220)"><path d="M-60,0 L-80,-300 C-60,-360 40,-360 60,-300 L80,-120 L320,-110 L340,0 Z" fill="#07090c"/>'
    s += '<ellipse cx="-10" cy="-380" rx="60" ry="66" fill="#07090c"/>' + palm_hat(-10, -400, 0.42) + '<rect x="230" y="-60" width="26" height="70" fill="#2a4a3a" opacity="0.8"/></g>'
    s += glow(1300, 1170, 400, "white", 0.4) + put(dog("white", "crouch", seed=31), 1180, 1230, 0.45)
    return S(s)
@art
def lost_man():
    s = '<rect width="2400" height="1350" fill="#04060a"/>' + glow(1200, 500, 900, "moon", 0.3)
    for i in range(14):
        x = 80 + i * 170 + (i % 3) * 30; w = 40 + (i % 4) * 20
        s += f'<path d="M{x},1350 C{x+10},900 {x-10},400 {x+20},0 L{x+20+w},0 C{x+w},400 {x+w+10},900 {x+w},1350 Z" fill="#020305"/>'
        s += f'<path d="M{x+20+w},0 C{x+w},400 {x+w+10},900 {x+w},1350" stroke="{MOONRIM}" stroke-width="3" opacity="0.25"/>'
    s += put(man_full(hat=False, cape=False, walk=0.2, rim=MOONRIM), 1250, 1200, 0.5, flip=True)
    return S(s, QM.fog_band(1150, 0.35, 191), '<rect width="2400" height="1350" fill="#40607a" opacity="0.12"/>')
@art
def burnt():
    s = bridge_svg("dawn", 201) + '<rect width="2400" height="1350" fill="#000" opacity="0.2"/>'
    s += '<ellipse cx="1300" cy="1180" rx="520" ry="120" fill="#0a0604" opacity="0.9"/><ellipse cx="1300" cy="1180" rx="440" ry="96" fill="#000" opacity="0.8"/>'
    r = random.Random(202)
    for _ in range(80):
        a = r.uniform(0, 2 * math.pi); d = r.uniform(0.3, 1.1); x = 1300 + math.cos(a) * 480 * d; y = 1180 + math.sin(a) * 110 * d
        s += f'<path d="M{x:.0f},{y:.0f} l{r.uniform(-6,6):.0f},{-r.uniform(10,40):.0f}" stroke="#1a0e08" stroke-width="3"/>'
    s += '<path d="M1290,1170 q20,-10 40,6 q-10,14 -40,-6" fill="#f4f6fa"/>'
    return S(s)
@art
def fur_close():
    s = '<rect width="2400" height="1350" fill="#0c0806"/>' + glow(1200, 600, 900, "moon", 0.4)
    r = random.Random(211)
    for _ in range(300):
        x = r.uniform(0, 2400); y = r.uniform(500, 1350); h = r.uniform(40, 160)
        s += f'<path d="M{x:.0f},{y:.0f} q{r.uniform(-20,20):.0f},{-h/2:.0f} {r.uniform(-30,30):.0f},{-h:.0f}" stroke="{r.choice(["#0a0604","#1a1008","#2a2018","#000"])}" stroke-width="{r.uniform(4,10):.0f}" fill="none"/>'
    s += glow(1200, 820, 500, "white", 0.5)
    for i in range(70):
        a = r.uniform(-0.5, 0.5); L = r.uniform(200, 520)
        s += f'<path d="M{1000+r.uniform(-30,30):.0f},{800+r.uniform(-30,30):.0f} C{1100:.0f},{760+a*200:.0f} {1250:.0f},{860+a*300:.0f} {1000+L:.0f},{820+a*260:.0f}" stroke="{r.choice(["#ffffff","#e8eef6","#c8d0dc"])}" stroke-width="{r.uniform(2,5):.1f}" fill="none" opacity="0.85"/>'
    return S(s)
@art
def altar_box():
    s = '<rect width="2400" height="1350" fill="#0c0806"/>' + table_wood(900) + candle_at(1800, 900, 260)
    s += '<rect x="600" y="160" width="520" height="700" fill="#3a2410"/><rect x="630" y="190" width="460" height="640" fill="#1a2a5a"/>'
    s += '<path d="M860,260 C780,300 760,500 720,800 L1000,800 C960,500 940,300 860,260 Z" fill="#2a4a9a"/><circle cx="860" cy="290" r="44" fill="#c89870"/>'
    s += '<path d="M800,240 C860,200 920,240 940,300 C900,260 830,250 800,240 Z" fill="#2a4a9a"/>' + glow(860, 290, 140, "warm", 0.6)
    for i in range(16): s += f'<path d="M860,290 L{860+math.cos(i/16*2*math.pi)*120:.0f},{290+math.sin(i/16*2*math.pi)*120:.0f}" stroke="#ffd27a" stroke-width="3" opacity="0.5"/>'
    s += '<path d="M1150,1000 L1650,1000 L1700,1160 L1100,1160 Z" fill="#5a3418"/><path d="M1100,1160 L1700,1160 L1700,1200 L1100,1200 Z" fill="#3a2010"/>'
    s += '<path d="M1150,1000 L1650,1000 L1600,860 L1200,860 Z" fill="#6a4020"/>'
    for i in range(40):
        s += f'<path d="M{1250+i*6},1060 C1350,{1030+i%5*6} 1450,{1080-i%7*5} {1550-i%4*10},{1050+i%6*4}" stroke="#f4f6fa" stroke-width="3" fill="none" opacity="0.8"/>'
    return S(s)
@art
def map():
    s = '<rect width="2400" height="1350" fill="#c8b08a"/><rect width="2400" height="1350" fill="#6a4a2a" filter="url(#paper)" opacity="0.5"/>'
    s += '<rect width="2400" height="1350" fill="#7aa0b0" opacity="0.35"/>'
    land = [(0, 120), (700, 140), (1000, 260), (1100, 420), (1150, 520), (1400, 470), (1600, 380), (1700, 420), (1650, 560), (1560, 620),
            (1720, 680), (1900, 700), (2050, 760), (2100, 880), (2200, 1000), (2300, 1150), (2380, 1300), (2250, 1350), (2050, 1180),
            (1850, 1080), (1650, 1020), (1450, 960), (1250, 870), (1000, 760), (700, 680), (300, 560), (0, 480)]
    s += f'<path d="{smooth(land)}" fill="#d8c4a0" stroke="#5a3a1a" stroke-width="6"/>'
    s += f'<path d="{smooth(land)}" fill="#8a6a40" opacity="0.15" filter="url(#paper)"/>'
    s += '<path d="M1080,520 C1150,620 1260,700 1350,760 C1400,820 1450,860 1500,900" stroke="#5a3a1a" stroke-width="4" stroke-dasharray="14 10" fill="none"/>'
    s += '<path d="M1200,600 C1300,640 1420,640 1520,620 C1600,700 1620,820 1500,900 C1380,860 1250,800 1150,700 Z" fill="#b3122e" opacity="0.25"/>'
    labels = [("MÉXICO", 500, 350, 64), ("Chiapas", 1310, 720, 50), ("Comitán", 1420, 800, 34), ("Guatemala", 1600, 960, 44),
              ("El Salvador", 1700, 1110, 34), ("Honduras", 1900, 960, 36), ("Nicaragua", 2020, 1080, 36), ("Costa Rica", 2120, 1240, 32),
              ("Océano Pacífico", 600, 1050, 54), ("Golfo de México", 1300, 220, 50)]
    for t, x, y, sz in labels:
        s += f'<text x="{x}" y="{y}" font-family="IM FELL English" font-size="{sz}" fill="#3a2410" text-anchor="middle" font-style="italic">{t}</text>'
    s += '<circle cx="1420" cy="760" r="12" fill="#b3122e"/>'
    s += '<rect width="2400" height="1350" fill="none" stroke="#3a2410" stroke-width="30"/>'
    return S(s)
@art
def book():
    s = '<rect width="2400" height="1350" fill="#0c0806"/>' + table_wood(700) + candle_at(2050, 760, 220)
    s += '<path d="M500,1250 L1180,1180 L1180,520 L520,590 Z" fill="#e8dcc0"/><path d="M1180,1180 L1900,1250 L1880,590 L1180,520 Z" fill="#f0e6cc"/>'
    s += '<path d="M1180,520 L1180,1180" stroke="#8a7a5a" stroke-width="6"/>'
    s += '<text x="850" y="760" font-family="IM FELL English" font-size="58" fill="#2a1a0a" text-anchor="middle" transform="rotate(-5 850 760)">LEYENDAS</text>'
    s += '<text x="850" y="840" font-family="IM FELL English" font-size="44" fill="#2a1a0a" text-anchor="middle" transform="rotate(-5 850 840)">de Guatemala</text>'
    s += '<text x="850" y="960" font-family="IM FELL English" font-size="32" fill="#4a3a2a" text-anchor="middle" transform="rotate(-5 850 960)">Madrid · 1930</text>'
    for i in range(14):
        y = 640 + i * 38
        s += f'<path d="M1240,{y} L1820,{y+20}" stroke="#6a5a4a" stroke-width="5" stroke-dasharray="{30+i%3*10} 10" opacity="0.6"/>'
    s += '<path d="M1300,1000 C1350,960 1420,940 1500,960 C1560,940 1640,950 1700,990 L1680,1060 L1320,1050 Z" fill="#1a120c" opacity="0.8"/>'
    s += '<circle cx="1660" cy="985" r="6" fill="#b3122e"/>'
    return S(s, '<rect width="2400" height="1350" fill="#ffb060" opacity="0.06"/>')
@art
def braid_scene():
    s = '<rect width="2400" height="1350" fill="#0c0806"/><rect width="2400" height="900" fill="#2a2018" filter="url(#plaster)" opacity="0.6"/>'
    s += table_wood(880) + candle_at(500, 920, 240)
    s += braid(wavy(900, 1000, 1900, 1080, 30, 3, 2), 40, "#0c0806", "#6a5040", seed=3)
    # the wall shadow becomes a dog
    s += f'<g opacity="0.75" filter="url(#blur2)">{put(dog("black", "stand", seed=41, rim=None, glow_body=False), 1100, 820, 0.85)}</g>'
    s += '<circle cx="1700" cy="460" r="36" fill="url(#redglow)" opacity="0.8"/>'
    return S(s)
@art
def xolo():
    s = '<rect width="2400" height="1350" fill="#1a0c06"/>' + glow(1500, 500, 1100, "warm", 0.5)
    s += '<path d="M0,1000 C700,960 1700,980 2400,1010 L2400,1350 L0,1350 Z" fill="#0c1a2a"/>' + reflection(1500, 1010, 1350, "#ffcf8a")
    # stepped pyramid far
    for i in range(6):
        w = 900 - i * 140; s += f'<rect x="{1500-w/2}" y="{900-i*70}" width="{w}" height="72" fill="#2a1408"/>'
    s += '<rect x="1440" y="420" width="120" height="70" fill="#2a1408"/>'
    s += put(dog("xolo", "walk", seed=51), 700, 1080, 0.75)
    s += f'<g opacity="0.55" filter="url(#ghost)">{put(man_full(hat=False, cape=False, walk=0.3, rim="#ffe0a0", fill="#d8e4f0"), 420, 1120, 0.6)}</g>'
    # glyph border
    for i in range(24):
        s += f'<rect x="{i*100+20}" y="40" width="60" height="60" fill="none" stroke="#c87a30" stroke-width="6" opacity="0.6"/><circle cx="{i*100+50}" cy="70" r="10" fill="#c87a30" opacity="0.6"/>'
    return S(s)
@art
def arrieros():
    s = road_svg("night", 221, (500, 220), vx=1600, corn_sides=False)
    for i in range(4):
        s += horse_shape(1100 + i * 260, 1080 - i * 20, 220, rim=MOONRIM, mule=True, packs=True, seed=i)
    s += put(man_full(hat=True, cape=False, walk=0.3, rim=MOONRIM), 2100, 1060, 0.35)
    s += glow(780, 1110, 300, "white", 0.4) + put(dog("white", "walk", seed=52), 640, 1140, 0.3)
    return S(s)
@art
def convent():
    return S(inner(BA.ART["temple_facade"]()), '<rect width="2400" height="1350" fill="#02040e" opacity="0.6"/>', glow(1800, 250, 300, "moon", 0.5), QM.fog_band(1200, 0.3, 231))


@art
def abuela2(): return S(portrait_bg("ghost"), brigida_bust(1200, 560, 1.75), '<rect width="2400" height="1350" fill="#3a5a8a" opacity="0.18"/>')
@art
def road_night3(): return S(road_svg("night", 301, (1500, 200), vx=1000, corn_sides=True))
@art
def bridge2(): return S(bridge_svg("night", 311), QM.fog_band(950, 0.2, 312), '<rect width="2400" height="1350" fill="#000" opacity="0.15"/>')

@art
def test_dogs():
    s = sky("#060c18", "#1a2a40") + glow(1200, 600, 900, "moon", 0.5)
    s += '<rect y="1100" width="2400" height="250" fill="#0c1018"/>'
    s += put(dog("white", "walk"), 250, 600, 0.9) + put(dog("black", "stand", growl=True), 1350, 600, 0.9)
    s += put(dog("white", "leap", growl=True), 300, 1300, 0.8) + put(dog("xolo", "stand"), 1450, 1300, 0.8)
    return S(s)


if __name__ == "__main__":
    write(sys.argv[1:] or [n for n in ART if not n.startswith("test")])
