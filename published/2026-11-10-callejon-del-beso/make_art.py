#!/usr/bin/env python3
"""Illustrations for 'El Callejón del Beso'. Usage: python3 make_art.py [name ...]  (no args = all)
Writes art/<name>.svg ; then: node /home/claude/pipeline/render_svg.js art/*.svg"""
import sys, os, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '/home/claude/pipeline'); sys.path.insert(0, HERE)
from art import *
from chars import *

A = os.path.join(HERE, "art"); os.makedirs(A, exist_ok=True)
ART = {}
def art(fn):
    ART[fn.__name__] = fn; return fn

EXTRA = '''<defs>
<filter id="plaster" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.008 0.02" numOctaves="4" seed="7" result="n"/>
<feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 1.3 -0.45"/><feComposite in2="SourceGraphic" operator="in"/></filter>
<filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.7" numOctaves="2" seed="3" result="n"/>
<feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -1.4 0.9"/><feComposite in2="SourceGraphic" operator="in"/></filter>
<filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="40"/></filter>
<linearGradient id="beamc" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#cfe0ff" stop-opacity="0.45"/><stop offset="1" stop-color="#cfe0ff" stop-opacity="0"/></linearGradient>
<linearGradient id="beamw" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#ffd27a" stop-opacity="0.6"/><stop offset="1" stop-color="#ffd27a" stop-opacity="0"/></linearGradient>
</defs>'''

def S(*parts):
    return svg(EXTRA, *parts)

def lg(id_, stops, x1=0, y1=0, x2=0, y2=1):
    s = "".join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a}"/>' for o, c, a in stops)
    return f'<defs><linearGradient id="{id_}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">{s}</linearGradient></defs>'

def _clipy(pts, y, keep_below):
    out = []
    for i in range(len(pts)):
        a, b = pts[i], pts[(i + 1) % len(pts)]
        ina = (a[1] >= y) if keep_below else (a[1] <= y); inb = (b[1] >= y) if keep_below else (b[1] <= y)
        if ina: out.append(a)
        if ina != inb:
            t = (y - a[1]) / (b[1] - a[1]); out.append((a[0] + (b[0] - a[0]) * t, y))
    return out

def poly(pts, fill, extra=""):
    pts = _clipy(_clipy(list(pts), -60, True), 1420, False)
    if len(pts) < 3: return ""
    return f'<path d="M{" L".join(f"{x:.0f},{y:.0f}" for x, y in pts)} Z" fill="{fill}" {extra}/>'

def clouds(n, y0, y1, seed, color, op=(0.3, 0.7), rx=(160, 420), ry=(40, 110), blur="blur3"):
    r = random.Random(seed)
    return f'<g filter="url(#{blur})">' + "".join(
        f'<ellipse cx="{r.uniform(-100, W+100):.0f}" cy="{r.uniform(y0, y1):.0f}" rx="{r.uniform(*rx):.0f}" ry="{r.uniform(*ry):.0f}" fill="{color}" opacity="{r.uniform(*op):.2f}"/>'
        for _ in range(n)) + '</g>'

MOONRIM = "#a8c8ff"
PAL = {"night": dict(sky=("#060c18", "#1c3048"), walls=["#2b3a4c", "#3a3244", "#24404a", "#40382e", "#2e3a52"], dark="#0a0f16", light="#ffc865"),
       "red":   dict(sky=("#12060a", "#401418"), walls=["#3a1c20", "#401a1c", "#2c1418", "#481e1a", "#381820"], dark="#0e0507", light="#ff6a40"),
       "dawn":  dict(sky=("#2a3a5c", "#e8a070"), walls=["#8a6a5a", "#6a7a8a", "#9a7a50", "#7a5a6a", "#5a7a7a"], dark="#2a2430", light="#ffe0a0"),
       "modern": dict(sky=("#1a2a4a", "#c87a5a"), walls=["#a0603a", "#3a7a8a", "#c09040", "#8a4a5a", "#5a8a6a"], dark="#1a1418", light="#ffe0a0")}

# ===================================================================== the alley (perspective, VP 1200,560)
VPX, VPY = 1200, 560
def wall_pt(side, f, yn):
    """point on a wall plane: side -1 left / +1 right, f = 0 near .. 1 vanishing, yn = height line at near edge."""
    xn = 0 if side < 0 else W
    return (xn + (VPX - xn) * f, yn + (VPY - yn) * f)

def flowerpot(x, y, k, seed, mood):
    r = random.Random(seed)
    s = f'<path d="M{x-22*k},{y} L{x+22*k},{y} L{x+16*k},{y+34*k} L{x-16*k},{y+34*k} Z" fill="#6a3a24" opacity="0.9"/>'
    for i in range(9):
        a = r.uniform(-2.6, -0.5); L = r.uniform(30, 60) * k
        s += f'<path d="M{x},{y} q{math.cos(a)*L*0.5:.0f},{math.sin(a)*L*0.8:.0f} {math.cos(a)*L:.0f},{math.sin(a)*L*0.6+20*k:.0f}" stroke="#1e3a22" stroke-width="{5*k:.1f}" fill="none"/>'
    for i in range(7):
        c = r.choice(["#b4386a", "#c24a7a", "#d8a040"] if mood != "red" else ["#7a1a2a"])
        s += f'<circle cx="{x+r.uniform(-40,40)*k:.0f}" cy="{y+r.uniform(-30,26)*k:.0f}" r="{r.uniform(5,9)*k:.1f}" fill="{c}" opacity="0.8"/>'
    return s

def rail(pts_top, pts_bot, n=14, color="#06080c", hi=None, w=1.0):
    """wrought-iron railing panel between a top edge and a bottom edge (two points each)."""
    (x0, y0), (x1, y1) = pts_top; (bx0, by0), (bx1, by1) = pts_bot
    s = f'<path d="M{x0:.0f},{y0:.0f} L{x1:.0f},{y1:.0f}" stroke="{color}" stroke-width="{12*w:.0f}" stroke-linecap="round"/>'
    s += f'<path d="M{bx0:.0f},{by0:.0f} L{bx1:.0f},{by1:.0f}" stroke="{color}" stroke-width="{9*w:.0f}"/>'
    for i in range(n + 1):
        t = i / n
        tx, ty = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t; bx, by = bx0 + (bx1 - bx0) * t, by0 + (by1 - by0) * t
        s += f'<path d="M{tx:.0f},{ty:.0f} L{bx:.0f},{by:.0f}" stroke="{color}" stroke-width="{4*w:.1f}"/>'
        if i < n:
            mx, my = (tx + bx) / 2 + (x1 - x0) / n / 2, (ty + by) / 2 + (y1 - y0) / n / 2
            rr = abs(x1 - x0) / n * 0.32
            s += f'<path d="M{mx-rr:.0f},{my:.0f} a{rr:.0f},{rr:.0f} 0 1 1 {rr:.0f},{rr:.0f} M{mx+rr:.0f},{my:.0f} a{rr:.0f},{rr:.0f} 0 1 1 {-rr:.0f},{-rr:.0f}" stroke="{color}" stroke-width="{3*w:.1f}" fill="none"/>'
    if hi:
        s += f'<path d="M{x0:.0f},{y0-5:.0f} L{x1:.0f},{y1-5:.0f}" stroke="{hi}" stroke-width="3" opacity="0.6"/>'
    return s

# balcony geometry (left one; the right one mirrors)
BL = dict(wall_top=(880, 545), wall_bot=(880, 712), out_top=(1138, 582), out_bot=(1138, 690), slab=24)
def balcony_geo(side):
    def m(p): return p if side < 0 else (W - p[0], p[1])
    return {k: (m(v) if isinstance(v, tuple) else v) for k, v in BL.items()}

def balcony(side, mood="night", door_lit=True):
    g = balcony_geo(side); p = PAL[mood]
    (wx, wty), (_, wby) = g["wall_top"], g["wall_bot"]; (ox, oty), (_, oby) = g["out_top"], g["out_bot"]
    sl = g["slab"]
    s = ""
    # door opening on the wall behind
    dx0, dx1 = (wx - 120, wx - 20) if side < 0 else (wx + 20, wx + 120)
    dtop0 = wty - 210; dtop1 = wty - 190 if side < 0 else wty - 230
    lit = p["light"] if door_lit else "#0b1018"
    s += poly([(dx0, dtop0 + (0 if side < 0 else 20)), (dx1, dtop1 + (0 if side < 0 else -20)), (dx1, wby - 4), (dx0, wby + 12)], lit)
    if door_lit:
        s += glow((dx0 + dx1) / 2, wty - 80, 260, "warm" if mood != "red" else "red", 0.6)
        s += poly([(dx0 + 10, dtop0 + 20), ((dx0 + dx1) / 2, dtop0 + 14), ((dx0 + dx1) / 2, wby), (dx0 + 10, wby + 10)], "#e8d0a0", 'opacity="0.35"')  # curtain
    s += f'<path d="M{dx0},{dtop0} L{dx1},{dtop1} M{dx0},{dtop0} L{dx0},{wby+12} M{dx1},{dtop1} L{dx1},{wby}" stroke="#2a2018" stroke-width="10" fill="none"/>'
    # slab (floor), seen from below
    s += poly([(wx, wby), (ox, oby), (ox, oby + sl), (wx, wby + sl + 16)], "#3a3530")
    s += poly([(wx, wby + sl + 16), (ox, oby + sl), (ox - (ox - wx) * 0.1, oby + sl + 26), (wx, wby + sl + 50)], "#1a1814")
    for i in range(4):  # corbels
        t = 0.15 + i * 0.25
        cx, cy = wx + (ox - wx) * t, wby + (oby - wby) * t + sl + 14
        s += f'<path d="M{cx-14},{cy} L{cx+14},{cy} L{cx+6},{cy+50} Q{cx},{cy+60} {cx-6},{cy+50} Z" fill="#24211c"/>'
    return s

def balcony_rails(side, mood="night"):
    g = balcony_geo(side)
    (wx, wty), (_, wby) = g["wall_top"], g["wall_bot"]; (ox, oty), (_, oby) = g["out_top"], g["out_bot"]
    s = rail(((wx, wty), (ox, oty)), ((wx, wby), (ox, oby)), 12, hi=MOONRIM if mood != "red" else "#ff6a50")
    # short side panel facing the other balcony
    dx = 30 * (1 if side < 0 else -1)
    s += rail(((ox, oty), (ox + dx, oty - 14)), ((ox, oby), (ox + dx, oby - 8)), 2)
    s += flowerpot(wx + (ox - wx) * 0.15, wty + (oty - wty) * 0.15 + 6, 0.9, 3 + side, mood)
    return s

def alley_walls(mood="night", lamp_on=True):
    p = PAL[mood]; r = random.Random(4)
    s = sky(*p["sky"])
    if mood != "red":
        s += stars(60, 3, 500)
    s += glow(1200, 120, 520, "moon" if mood != "red" else "red", 0.9)
    # far end: stairs climbing and a small lit lamp
    s += poly([(1080, 330), (1320, 330), (1320, 700), (1080, 700)], "#101820" if mood == "night" else p["dark"])
    for i in range(8):
        y = 700 - i * 18
        s += poly([(1080 + i * 6, y), (1320 - i * 6, y), (1320 - i * 6, y - 18), (1080 + i * 6, y - 18)], ["#2a323c", "#1e252e"][i % 2] if mood != "red" else ["#3a1a1c", "#2a1214"][i % 2])
    s += glow(1250, 450, 160, "warm" if mood != "red" else "red", 0.8)
    s += window(1230, 420, 40, 60, True)
    # walls (house blocks with different colours)
    for side in (-1, 1):
        cuts = [0.0, 0.28, 0.55, 0.78, 0.9]
        for i in range(len(cuts) - 1):
            f0, f1 = cuts[i], cuts[i + 1]
            top0 = wall_pt(side, f0, -1700 + i * 120); top1 = wall_pt(side, f1, -1700 + i * 120)
            bot0 = wall_pt(side, f0, 1900); bot1 = wall_pt(side, f1, 1900)
            col = p["walls"][(i * 2 + (side > 0)) % len(p["walls"])]
            gid = f"wl{side+1}{i}"
            shade_dir = (0, 0, 1, 0) if side < 0 else (1, 0, 0, 0)
            s += lg(gid, [(0, col, 1), (1, p["dark"], 1)], *shade_dir)
            s += poly([top0, top1, bot1, bot0], f"url(#{gid})")
            s += poly([top0, top1, bot1, bot0], "#000", 'filter="url(#plaster)" opacity="0.6"')
            # roof cornice line
            s += f'<path d="M{top0[0]:.0f},{top0[1]:.0f} L{top1[0]:.0f},{top1[1]:.0f}" stroke="#05070a" stroke-width="22"/>'
            # vertical seam between houses
            s += f'<path d="M{top1[0]:.0f},{top1[1]:.0f} L{bot1[0]:.0f},{bot1[1]:.0f}" stroke="#05070a" stroke-width="8" opacity="0.7"/>'
            # small windows on upper floors
            for yy in (-500, 300):
                fm = (f0 + f1) / 2
                a = wall_pt(side, fm - (f1 - f0) * 0.18, yy); b = wall_pt(side, fm + (f1 - f0) * 0.18, yy)
                c = wall_pt(side, fm + (f1 - f0) * 0.18, yy - 260); d = wall_pt(side, fm - (f1 - f0) * 0.18, yy - 260)
                if i == 2 and yy == 300:  # balcony level: drawn by balcony()
                    continue
                litw = r.random() < 0.35
                s += poly([a, b, c, d], p["light"] if litw else "#0a0e14", 'opacity="0.9"')
                s += f'<path d="M{(a[0]+b[0])/2:.0f},{(a[1]+b[1])/2:.0f} L{(c[0]+d[0])/2:.0f},{(c[1]+d[1])/2:.0f}" stroke="#05070a" stroke-width="5"/>'
            # bougainvillea spill on some walls
            if (i + side) % 3 == 0:
                rr = random.Random(i * 7 + side)
                a = wall_pt(side, f0 + 0.03, -1100 + i * 120)
                for _ in range(70):
                    fx = rr.uniform(f0, f1); yy = rr.uniform(-1500, -600)
                    x, y = wall_pt(side, fx, yy)
                    if 0 < y < 1350:
                        s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rr.uniform(6,16)*(1-fx*0.7):.0f}" fill="{rr.choice(["#8a2a5a", "#a03a6a", "#1e3a24"]) if mood != "red" else "#2a0a10"}" opacity="0.7"/>'
    # moon rim on the wall edges (top cornices)
    for side in (-1, 1):
        a = wall_pt(side, 0.0, -1700); b = wall_pt(side, 0.9, -1700 + 360)
        s += f'<path d="M{a[0]:.0f},{a[1]:.0f} L{b[0]:.0f},{b[1]:.0f}" stroke="{MOONRIM if mood != "red" else "#ff5040"}" stroke-width="5" opacity="0.5" filter="url(#blur1)"/>'
    # ground: stepped stone floor
    for i in range(12):
        f = 0.9 - i * 0.075
        y0 = wall_pt(-1, f, 1900)[1]; y1 = wall_pt(-1, max(f - 0.075, 0), 1900)[1]
        xl0 = wall_pt(-1, f, 1900)[0]; xr0 = wall_pt(1, f, 1900)[0]
        xl1 = wall_pt(-1, max(f - 0.075, 0), 1900)[0]; xr1 = wall_pt(1, max(f - 0.075, 0), 1900)[0]
        s += poly([(xl0, y0), (xr0, y0), (xr1, y1), (xl1, y1)], ["#262a30", "#1c2026"][i % 2] if mood != "red" else ["#2a1416", "#1e0e10"][i % 2])
        s += f'<path d="M{xl0:.0f},{y0:.0f} L{xr0:.0f},{y0:.0f}" stroke="{"#8aa0b8" if mood != "red" else "#a04030"}" stroke-width="3" opacity="0.35"/>'
    # wall lamp (farol) on the left, lower
    lx, ly = wall_pt(-1, 0.45, 700)
    s += f'<path d="M{lx:.0f},{ly:.0f} l60,10 l0,20" stroke="#05070a" stroke-width="8" fill="none"/>'
    s += f'<path d="M{lx+36:.0f},{ly+30:.0f} l48,0 l-8,70 l-32,0 Z" fill="{"#ffd98a" if lamp_on else "#20242a"}"/><path d="M{lx+30:.0f},{ly+30:.0f} l60,0 l-30,-26 Z" fill="#05070a"/>'
    return s

def alley_people(which, mood="night", ghost=False):
    """layer with characters on the alley balconies + the railings drawn again on top. which: set of 'carmen','luis','kiss','talk'."""
    s = ""
    fill = "#dfeaff" if ghost else SIL
    rimc = None if ghost else (MOONRIM if mood != "red" else "#ff6040")
    cid = "balcclip"
    s += f'<defs><clipPath id="{cid}"><path d="M0,0 L2400,0 L2400,700 L0,700 Z"/></clipPath></defs><g clip-path="url(#{cid})">'
    k = 0.37
    if "kiss" in which:
        s += place(profile_figure("woman", lean=16, fill=fill, rim=rimc), 1166, 486, k)
        s += place(profile_figure("man", lean=10, fill=fill, rim=rimc), 1238, 474, k, flip=True)
    else:
        if "carmen" in which:
            s += place(profile_figure("woman", lean=6, arm="reach" if "talk" in which else None, fill=fill, rim=rimc), 1052, 486, k)
        if "luis" in which:
            s += place(profile_figure("man", lean=6, arm="reach" if "talk" in which else None, fill=fill, rim=rimc), 1348, 474, k, flip=True)
    s += "</g>"
    if not ghost:
        if "carmen" in which or "kiss" in which: s += balcony_rails(-1, mood)
        if "luis" in which or "kiss" in which: s += balcony_rails(1, mood)
        s = f'<g>{s}</g>'
    else:
        s = f'<g filter="url(#ghost)" opacity="0.55">{s}</g>'
    return s

def alley_full(mood="night"):
    return alley_walls(mood) + balcony(-1, mood, True) + balcony(1, mood, mood != "red") + balcony_rails(-1, mood) + balcony_rails(1, mood)

CLOSE = 'transform="translate(1200,590) scale(2.1) translate(-1200,-590)"'

@art
def alley_low(): return S(alley_full("night"))
@art
def alley_low_red(): return S(alley_full("red"), '<rect width="2400" height="1350" fill="#400" opacity="0.15"/>')
CROPS = {}  # name -> (svg, scale, cx, cy): rendered big with render_svg --width, then cropped (resvg cannot filter off-canvas items)
def crop_art(name, scale=2.1, cx=1200, cy=590):
    def deco(fn):
        CROPS[name] = (fn, scale, cx, cy); return fn
    return deco

@crop_art("balcony_close")
def _bc(): return S(alley_full("night"))
@art
def l_carmen_balc(): return S(alley_people({"carmen"}))
@art
def l_luis_balc(): return S(alley_people({"luis"}))
@art
def l_kiss_balc(): return S(alley_people({"kiss"}))
@art
def l_ghosts(): return S(alley_people({"kiss"}, ghost=True))
@art
def l_kiss_far(): return S(f'<g {CLOSE}>{alley_people({"kiss"})}</g>')
@art
def l_couple_talk(): return S(f'<g {CLOSE}>{alley_people({"carmen", "luis", "talk"})}</g>')
@art
def l_ghosts_close(): return S(f'<g {CLOSE}>{alley_people({"kiss"}, ghost=True)}</g>')
@art
def l_lamp_glow():
    lx, ly = wall_pt(-1, 0.45, 700)
    return S(glow(lx + 60, ly + 70, 420, "warm", 0.7), glow(lx + 60, ly + 70, 120, "warm", 0.9))
@art
def l_shadow_watcher_low():
    return S(place(man_full(hat=True, cape=True, rim=MOONRIM), 330, 1500, 1.05))



# ===================================================================== stepped alley (looking up the steps)
STEP3 = None
def steps_scene(mood="night", people=False):
    p = PAL[mood]; r = random.Random(8)
    s = sky(*p["sky"])
    if mood == "night": s += stars(80, 9, 400)
    s += glow(1200, 200, 600, "moon" if mood == "night" else "warm", 0.8)
    # far houses at the top of the steps
    s += poly([(900, 260), (1500, 260), (1500, 620), (900, 620)], p["walls"][3])
    s += poly([(900, 260), (1500, 260), (1500, 620), (900, 620)], "#000", 'filter="url(#plaster)" opacity="0.5"')
    s += window(1060, 380, 70, 110, True, True, light=p["light"]) + window(1270, 380, 70, 110, mood != "night", True, light=p["light"])
    # steps: from far (y=620, narrow) to near (y=1350, wide)
    n = 14
    for i in range(n):
        t0, t1 = i / n, (i + 1) / n
        y0 = 620 + (1350 - 620) * (t0 ** 1.35); y1 = 620 + (1350 - 620) * (t1 ** 1.35)
        hw0 = 300 + 900 * t0; hw1 = 300 + 900 * t1
        tread = y0 + (y1 - y0) * 0.45
        top_c = ["#3a3e46", "#34383f"][i % 2] if mood != "modern" else ["#8a7a6a", "#7a6a5a"][i % 2]
        s += poly([(1200 - hw0, y0), (1200 + hw0, y0), (1200 + hw1, tread), (1200 - hw1, tread)], top_c)
        s += poly([(1200 - hw1, tread), (1200 + hw1, tread), (1200 + hw1, y1), (1200 - hw1, y1)], "#161a20" if mood != "modern" else "#4a3a30")
        s += f'<path d="M{1200-hw1:.0f},{tread:.0f} L{1200+hw1:.0f},{tread:.0f}" stroke="{MOONRIM if mood == "night" else "#ffd8a0"}" stroke-width="3" opacity="0.4"/>'
        for k in range(int(6 + 10 * t0)):  # stone joints
            xx = 1200 - hw0 + r.uniform(0, 2 * hw0)
            s += f'<path d="M{xx:.0f},{y0+2:.0f} l{(xx-1200)*0.05:.0f},{(tread-y0)*0.9:.0f}" stroke="#1a1e24" stroke-width="2" opacity="0.6"/>'
    # walls on both sides, tall, with doors and lamps
    for side in (-1, 1):
        xn = 0 if side < 0 else W; xf = 900 if side < 0 else 1500
        col = p["walls"][0 if side < 0 else 2]
        gid = f"sw{side+1}{mood}"
        s += lg(gid, [(0, p["dark"], 1), (1, col, 1)], *((0, 0, 1, 0) if side < 0 else (1, 0, 0, 0)))
        s += poly([(xn, -100), (xf, 120), (xf, 640), (xn, 1450)], f"url(#{gid})")
        s += poly([(xn, -100), (xf, 120), (xf, 640), (xn, 1450)], "#000", 'filter="url(#plaster)" opacity="0.55"')
        for j, f in enumerate((0.35, 0.68)):
            x = xn + (xf - xn) * f
            yt = -100 + 220 * f + 200; yb = 1450 - 810 * f
            dw = 160 * (1 - f * 0.6)
            s += poly([(x, yt + 260), (x + side * dw, yt + 270 + 20 * f), (x + side * dw, yb - 40 * f), (x, yb)], "#0a0c10")
            if j == 0:
                s += poly([(x, yt + 60), (x + side * dw * 0.9, yt + 70), (x + side * dw * 0.9, yt + 200), (x, yt + 200)], p["light"] if r.random() < 0.6 else "#0c1016")
        # bougainvillea
        rr = random.Random(side + 30)
        for _ in range(90):
            x = rr.uniform(min(xn, xf), max(xn, xf)) if side < 0 else rr.uniform(xf, xn)
            y = rr.uniform(-50, 260)
            s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rr.uniform(8,22):.0f}" fill="{rr.choice(["#8a2a5a", "#a03a6a", "#1e3a24", "#6a1e48"])}" opacity="0.75"/>'
    s += lamp(560, 1100, 520, lit=True) if mood != "modern" else lamp(560, 1100, 520, lit=True)
    return s

STEP3_Y = 620 + (1350 - 620) * ((11 / 14) ** 1.35)  # the third step from the bottom

@art
def alley_steps(): return S(steps_scene("night"))
@art
def alley_modern():
    s = steps_scene("modern")
    r = random.Random(5)
    # tourists queueing on the steps (silhouettes) + papel picado
    for i, (x, y, h) in enumerate(((760, 1350, 520), (900, 1220, 420), (1500, 1300, 480), (1640, 1350, 560), (1080, 900, 260), (1320, 860, 240))):
        if i % 2 == 0:
            s += place(woman_full(rim="#ffd8a0", fill="#120c10"), x, y, h / 1000)
        else:
            s += place(man_full(hat=False, cape=False, rim="#ffd8a0", fill="#120c10"), x, y, h / 1000)
    s += papel_picado(30, n=9, seed=4, opacity=0.85)
    return S(s, '<rect width="2400" height="1350" fill="#ffb070" opacity="0.06"/>')
@art
def l_step_glow():
    y = STEP3_Y
    return S(f'<ellipse cx="1200" cy="{y+20:.0f}" rx="520" ry="60" fill="url(#warmglow)" opacity="0.8"/>',
             f'<path d="M{1200-470},{y+8:.0f} L{1200+470},{y+8:.0f}" stroke="#ffd27a" stroke-width="6" opacity="0.7" filter="url(#blur1)"/>')
@art
def l_luis_walk(): return S(place(man_full(hat=True, cape=False, walk=0.4, rim=MOONRIM), 980, 1290, 0.62))
@art
def l_shadow_watcher(): return S(place(man_full(hat=True, cape=True, rim=MOONRIM), 1420, 760, 0.3), glow(1420, 520, 60, "white", 0.0))
@art
def l_couple_steps():
    y = STEP3_Y + 30
    return S(place(profile_figure("woman", lean=12, rim="#ffd8a0"), 1150, y - 330, 0.55),
             place(profile_figure("man", lean=8, rim="#ffd8a0"), 1252, y - 340, 0.58, flip=True),
             poly([(1080, y - 10), (1330, y - 10), (1340, y + 20), (1070, y + 20)], SIL))

# ===================================================================== city views
def houses_hill(x0, x1, ybase, slope, seed, pal, lit=0.35, scale=1.0):
    r = random.Random(seed); s = ""
    x = x0
    while x < x1:
        w = r.uniform(70, 150) * scale; h = r.uniform(60, 130) * scale
        y = ybase - (x - x0) * slope + r.uniform(-20, 20)
        col = r.choice(pal)
        s += f'<rect x="{x:.0f}" y="{y-h:.0f}" width="{w:.0f}" height="{h+400:.0f}" fill="{col}"/>'
        s += f'<rect x="{x:.0f}" y="{y-h:.0f}" width="{w:.0f}" height="6" fill="#05070a" opacity="0.6"/>'
        for k in range(int(w // (40 * scale))):
            if r.random() < lit:
                s += f'<rect x="{x+12*scale+k*38*scale:.0f}" y="{y-h+20*scale:.0f}" width="{14*scale:.0f}" height="{22*scale:.0f}" fill="#ffc865"/>'
                s += glow(x + 19 * scale + k * 38 * scale, y - h + 31 * scale, 30 * scale, "warm", 0.5)
            else:
                s += f'<rect x="{x+12*scale+k*38*scale:.0f}" y="{y-h+20*scale:.0f}" width="{14*scale:.0f}" height="{22*scale:.0f}" fill="#0a0e14" opacity="0.7"/>'
        x += w * r.uniform(0.75, 1.0)
    return s

def basilica(x, yb, k, col, dome="#c9a040", lit=True):
    s = f'<rect x="{x-160*k}" y="{yb-300*k}" width="{320*k}" height="{300*k}" fill="{col}"/>'
    s += f'<rect x="{x+150*k}" y="{yb-520*k}" width="{110*k}" height="{520*k}" fill="{col}"/>'
    s += f'<path d="M{x+140*k},{yb-520*k} L{x+205*k},{yb-640*k} L{x+270*k},{yb-520*k} Z" fill="{col}"/>'
    s += f'<path d="M{x-110*k},{yb-300*k} Q{x},{yb-520*k} {x+110*k},{yb-300*k} Z" fill="{dome}"/>'
    s += f'<rect x="{x-6*k}" y="{yb-560*k}" width="{12*k}" height="{60*k}" fill="{col}"/>'
    if lit:
        s += glow(x, yb - 200 * k, 320 * k, "warm", 0.6)
        for i in range(3):
            s += window(x - 90 * k + i * 70 * k, yb - 240 * k, 40 * k, 70 * k, True)
    return s

def city(mood="night"):
    p = PAL[mood]
    s = sky(*p["sky"], mid=("#1a2a44" if mood == "night" else "#c07a6a"))
    if mood == "night":
        s += stars(160, 2, 600) + moon(1820, 230, 80)
    else:
        s += glow(1700, 700, 900, "warm", 0.7)
    s += ridge(560, 140, "#101a28" if mood == "night" else "#4a4a62", 4)
    # the mine headframe on the far hill
    s += f'<g fill="none" stroke="{"#05070a" if mood == "night" else "#2a2230"}" stroke-width="8"><path d="M420,520 L470,340 L520,520 M440,450 L500,450 M455,390 L485,390"/></g><circle cx="470" cy="336" r="16" fill="#05070a"/>'
    pal = p["walls"] + ["#3a4a3a", "#4a3a52"]
    s += houses_hill(-50, 1200, 1050, -0.45, 1, pal, 0.35 if mood == "night" else 0.1, 1.1)
    s += houses_hill(1150, 2450, 560, -0.40, 2, pal, 0.35 if mood == "night" else 0.1, 1.1)
    s += houses_hill(-50, 2450, 1180, 0.0, 3, pal, 0.3 if mood == "night" else 0.1, 1.5)
    s += basilica(1180, 1000, 0.9, "#c08a4a" if mood != "night" else "#3a3040", "#d8a840" if mood != "night" else "#8a7040", mood == "night")
    s += houses_hill(-50, 2450, 1330, 0.0, 6, pal, 0.25, 2.0)
    s += clouds(8, 900, 1300, 3, "#9fb0c8" if mood == "night" else "#f0d0c0", (0.08, 0.2), (300, 700), (60, 140))
    return s

@art
def gto_panorama(): return S(city("night"))
@art
def gto_dawn(): return S(city("dawn"))
@art
def moon_sky():
    s = sky("#040810", "#1a2c44", "#0c1828") + stars(260, 5, 1000) + moon(1200, 420, 150)
    s += ridge(1020, 160, "#0a121c", 8) + ridge(1120, 90, "#05080e", 9)
    s += houses_hill(-50, 2450, 1250, 0.0, 9, ["#06090e", "#080b10"], 0.25, 1.0)
    return S(s)
@art
def l_clouds(): return S(clouds(14, 80, 700, 21, "#2a3a52", (0.25, 0.55), (220, 520), (40, 100)), clouds(8, 100, 600, 22, "#8aa4c4", (0.06, 0.14), (200, 400), (30, 70)))
@art
def l_fog(): return S(clouds(18, 900, 1400, 31, "#b0c4d8", (0.08, 0.2), (300, 700), (60, 140)))
@art
def rooftops():
    s = sky("#050a14", "#1c3048") + stars(200, 11, 700) + moon(600, 260, 110)
    s += houses_hill(-50, 2450, 900, -0.05, 12, ["#141c28", "#1a2230", "#20202c"], 0.3, 1.6)
    s += basilica(1700, 960, 0.8, "#10141c", "#4a4030", True)
    r = random.Random(13); s2 = ""
    for i in range(9):  # near flat roofs with water tanks and laundry lines
        x = i * 280 - 40; y = 1060 + r.uniform(-40, 40)
        s2 += f'<rect x="{x}" y="{y}" width="290" height="400" fill="#06080c"/><rect x="{x}" y="{y}" width="290" height="5" fill="{MOONRIM}" opacity="0.4"/>'
        if i % 3 == 1:
            s2 += f'<path d="M{x+30},{y-90} Q{x+150},{y-60} {x+270},{y-90}" stroke="#06080c" stroke-width="3" fill="none"/>'
            for k in range(4):
                s2 += f'<rect x="{x+60+k*55}" y="{y-80+k%2*6}" width="34" height="44" fill="#1c2430"/>'
    return S(s, s2)
@art
def volcanoes():
    s = sky("#0a1228", "#d0806a", "#5a4a7a") + stars(80, 4, 300)
    # Iztaccíhuatl: long ridge like a sleeping woman (head, chest, knees, feet)
    s += '<path d="M200,900 C320,760 420,700 520,690 C600,684 640,640 700,640 C760,640 800,600 900,560 C980,530 1060,560 1120,600 C1180,640 1260,620 1320,660 C1400,720 1500,800 1560,900 Z" fill="#3a3a5a"/>'
    s += '<path d="M480,700 C560,680 620,650 700,644 C770,640 820,596 900,566 C970,540 1060,566 1110,604 C1170,640 1250,626 1300,660 C1200,650 1120,640 1040,600 C960,570 880,620 780,660 C700,690 600,700 480,700 Z" fill="#e8ecf4"/>'
    # Popocatépetl: perfect cone with smoke
    s += '<path d="M1500,900 L1900,420 C1920,400 1960,400 1980,420 L2400,900 Z" fill="#2e3050"/>'
    s += '<path d="M1780,560 L1900,420 C1920,400 1960,400 1980,420 L2100,560 C2040,540 2000,580 1940,550 C1880,580 1840,540 1780,560 Z" fill="#eef0f6"/>'
    s += clouds(10, 200, 400, 6, "#9a8aa0", (0.3, 0.6), (80, 200), (40, 90), "blur2").replace('cx="', 'cx="', 1)
    s += ridge(980, 90, "#141428", 5) + ridge(1100, 60, "#07070f", 6)
    return S(s)

# ===================================================================== mine & money
@art
def mine():
    s = sky("#060a12", "#1a2434") + stars(80, 2, 400)
    s += '<path d="M0,700 C400,560 800,520 1200,600 C1600,680 2000,560 2400,620 L2400,1350 L0,1350 Z" fill="#1a1612"/>'
    # tunnel mouth with timber frame
    s += '<path d="M780,1350 L820,760 Q1200,560 1580,760 L1620,1350 Z" fill="#020203"/>'
    s += '<path d="M800,1350 L840,780 L1560,780 L1600,1350" stroke="#4a3220" stroke-width="44" fill="none"/>'
    s += '<path d="M820,780 L1580,780" stroke="#5a3e26" stroke-width="56"/>'
    for i in range(6):  # inner frames receding
        k = 1 - i * 0.14
        s += f'<path d="M{1200-330*k:.0f},{1300-20*i:.0f} L{1200-330*k:.0f},{820+40*i:.0f} L{1200+330*k:.0f},{820+40*i:.0f} L{1200+330*k:.0f},{1300-20*i:.0f}" stroke="#2a1c12" stroke-width="{24*k:.0f}" fill="none" opacity="{1-i*0.12:.2f}"/>'
    s += glow(1200, 1050, 300, "warm", 0.7)
    # rail tracks
    s += '<path d="M900,1350 L1150,900 M1500,1350 L1250,900" stroke="#6a6a70" stroke-width="10"/>'
    for i in range(8):
        y = 1340 - i * 55
        s += f'<path d="M{880+i*34},{y} L{1520-i*34},{y}" stroke="#2a1c12" stroke-width="{16-i}"/>'
    # oil lamps and miners
    for x in (700, 1700):
        s += f'<path d="M{x},700 L{x},820" stroke="#2a1c12" stroke-width="8"/>' + glow(x, 840, 220, "warm", 0.9) + f'<rect x="{x-14}" y="820" width="28" height="40" fill="#ffd98a"/>'
    s += place(man_full(hat=True, cape=False, walk=0.3, rim="#ffb860"), 560, 1330, 0.55)
    s += place(man_full(hat=False, cape=False, walk=-0.3, rim="#ffb860"), 1880, 1350, 0.6)
    s += '<g fill="none" stroke="#05070a" stroke-width="12"><path d="M1900,640 L1990,300 L2080,640 M1925,540 L2055,540 M1950,440 L2030,440"/></g><circle cx="1990" cy="296" r="30" fill="#05070a"/>'
    s += f'<path d="M0,1250 L2400,1250 L2400,1350 L0,1350 Z" fill="#0a0806"/>'
    return S(s)

def table_wood(y0=760):
    r = random.Random(3)
    s = lg("wood", [(0, "#3a2414", 1), (1, "#120a06", 1)]) + f'<rect x="0" y="{y0}" width="2400" height="{1350-y0}" fill="url(#wood)"/>'
    for i in range(30):
        y = y0 + r.uniform(0, 590)
        s += f'<path d="M0,{y:.0f} Q1200,{y+r.uniform(-20,20):.0f} 2400,{y+r.uniform(-30,30):.0f}" stroke="#4a3020" stroke-width="{r.uniform(1,4):.1f}" fill="none" opacity="0.5"/>'
    return s

def candle_at(x, y, h=200):
    return (glow(x, y - h - 40, 700, "warm", 0.95) + f'<rect x="{x-26}" y="{y-h}" width="52" height="{h}" rx="8" fill="#e8dcc0"/>'
            f'<path d="M{x-26},{y-h} q26,14 52,0" stroke="#c8b898" stroke-width="5" fill="none"/>'
            f'<path d="M{x+18},{y-h} q6,40 -2,70" stroke="#d8ccb0" stroke-width="8" fill="none"/>'
            f'<ellipse cx="{x}" cy="{y}" rx="70" ry="16" fill="#8a7040"/>')
FLAME_XY = (1560, 500)
def flame(x, y, k=1.0):
    return (f'<path d="M{x},{y-60*k} Q{x+22*k},{y-20*k} {x},{y+12*k} Q{x-22*k},{y-20*k} {x},{y-60*k} Z" fill="#ffd36a"/>'
            f'<path d="M{x},{y-40*k} Q{x+10*k},{y-12*k} {x},{y+6*k} Q{x-10*k},{y-12*k} {x},{y-40*k} Z" fill="#fff8e0"/>')
@art
def l_flame():
    x, y = FLAME_XY
    return S(glow(x, y, 260, "warm", 0.6), flame(x, y, 1.0))

@art
def coins():
    s = '<rect width="2400" height="1350" fill="#0a0604"/>' + table_wood(700)
    s += candle_at(1560, 760, 200)
    r = random.Random(4)
    for (cx, cy, n) in ((700, 900, 14), (950, 960, 9), (1200, 880, 18), (500, 1060, 6)):
        for i in range(n):
            s += f'<ellipse cx="{cx}" cy="{cy-i*14}" rx="90" ry="28" fill="#8a8a90"/><ellipse cx="{cx}" cy="{cy-i*14-4}" rx="88" ry="26" fill="#c8c8d0"/>'
        s += f'<ellipse cx="{cx}" cy="{cy-n*14-4}" rx="88" ry="26" fill="#e0e0e8"/><ellipse cx="{cx-20}" cy="{cy-n*14-10}" rx="40" ry="8" fill="#ffffff" opacity="0.6"/>'
        s += f'<text x="{cx}" y="{cy-n*14+4}" font-family="Cinzel" font-size="22" fill="#8a8a92" text-anchor="middle">8 R</text>'
    for i in range(30):
        x, y = r.uniform(300, 1900), r.uniform(1000, 1300)
        s += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="60" ry="20" fill="#b8b8c0" transform="rotate({r.uniform(-20,20):.0f} {x:.0f} {y:.0f})"/><ellipse cx="{x-10:.0f}" cy="{y-5:.0f}" rx="24" ry="5" fill="#fff" opacity="0.5"/>'
    # ledger
    s += '<path d="M1700,1000 L2300,950 L2350,1250 L1740,1310 Z" fill="#d8c8a0"/><path d="M2020,975 L2045,1280" stroke="#8a7a5a" stroke-width="4"/>'
    for i in range(10):
        s += f'<path d="M{1760+i*2},{1040+i*24} L{2000+i*2},{1020+i*24}" stroke="#4a3a2a" stroke-width="3" opacity="0.6" stroke-dasharray="20 8 40 6"/>'
    return S(s)

@art
def letters_table():
    s = '<rect width="2400" height="1350" fill="#0a0604"/>' + table_wood(640)
    s += candle_at(1560, 760, 200)
    # folded letter + an open one
    s += '<path d="M500,820 L1300,760 L1360,1220 L540,1290 Z" fill="#e6d8b8"/><path d="M500,820 L1300,760 L1330,990 L520,1050 Z" fill="#efe4c8"/>'
    s += '<path d="M520,1050 L1330,990" stroke="#b8a888" stroke-width="3"/>'
    r = random.Random(7)
    for i in range(12):
        y = 850 + i * 34
        if 1030 < y < 1060: continue
        x0 = 570; x1 = 1260 - r.uniform(0, 200)
        d = f"M{x0},{y-(x0-500)*0.075:.0f}"
        x = x0
        while x < x1:
            x += r.uniform(14, 30); d += f" q{r.uniform(-4,4):.0f},{r.uniform(-14,-4):.0f} {r.uniform(8,16):.0f},{r.uniform(-2,2):.0f}"
        s += f'<path d="{d}" stroke="#2a1c14" stroke-width="2.6" fill="none" opacity="0.8" transform="rotate(-4 900 1000)"/>'
    s += '<text x="1000" y="1200" font-family="IM FELL English" font-style="italic" font-size="54" fill="#3a2418" transform="rotate(-4 1000 1200)">Tuyo siempre, L.</text>'
    s += '<circle cx="1240" cy="1180" r="40" fill="#5a1a14"/><circle cx="1240" cy="1180" r="26" fill="#7a2a20"/>'
    # quill + inkwell
    s += '<ellipse cx="1900" cy="1060" rx="110" ry="30" fill="#0a0808"/><path d="M1810,1060 L1810,940 Q1900,900 1990,940 L1990,1060 Z" fill="#14121a"/><ellipse cx="1900" cy="940" rx="90" ry="24" fill="#1e1c26"/>'
    s += '<path d="M1880,940 C1960,700 2100,500 2250,360 C2200,520 2080,720 1900,940 Z" fill="#d8d0c0"/><path d="M1880,940 C1990,700 2120,520 2250,360" stroke="#8a8270" stroke-width="3" fill="none"/>'
    return S(s)

@art
def dagger_bg():
    s = '<rect width="2400" height="1350" fill="#0a0406"/>'
    s += lg("velvet", [(0, "#2a0c10", 1), (1, "#0a0204", 1)]) + '<rect width="2400" height="1350" fill="url(#velvet)"/>'
    for i in range(10):
        s += f'<path d="M{i*260-100},0 C{i*260},500 {i*260-200},900 {i*260+60},1350" stroke="#000" stroke-width="60" opacity="0.3" fill="none" filter="url(#blur2)"/>'
    s += glow(1500, 300, 900, "warm", 0.45)
    # dagger lying diagonally: blade, guard (quillons), grip with wire, pommel
    s += '<g transform="rotate(-14 1200 700)">'
    s += lg("blade", [(0, "#f4f8ff", 1), (0.48, "#9aa4b4", 1), (0.52, "#3a4250", 1), (1, "#7a8494", 1)])
    s += '<path d="M1290,640 L2150,676 L2220,700 L2150,724 L1290,760 Z" fill="url(#blade)"/>'
    s += '<path d="M1290,700 L2200,700" stroke="#ffffff" stroke-width="3" opacity="0.7"/>'
    s += '<path d="M1300,650 L2140,682" stroke="#ffffff" stroke-width="5" opacity="0.5" filter="url(#blur1)"/>'
    s += '<path d="M1250,520 C1280,560 1290,620 1290,700 C1290,780 1280,840 1250,880 L1300,880 C1320,820 1330,760 1330,700 C1330,640 1320,580 1300,520 Z" fill="#b08a3a"/>'
    s += '<circle cx="1260" cy="520" r="22" fill="#c9a24a"/><circle cx="1260" cy="880" r="22" fill="#c9a24a"/>'
    s += '<rect x="960" y="660" width="290" height="80" rx="30" fill="#2a1a10"/>'
    for i in range(14):
        s += f'<path d="M{975+i*20},662 L{985+i*20},738" stroke="#8a6a3a" stroke-width="5"/>'
    s += '<circle cx="930" cy="700" r="56" fill="#b08a3a"/><circle cx="916" cy="684" r="18" fill="#f0d890" opacity="0.7"/>'
    s += '<circle cx="1290" cy="700" r="20" fill="#7a1a14"/>'
    s += '</g>'
    s += '<circle cx="1980" cy="560" r="40" fill="url(#whiteglow)"/>'
    return S(s)

# ===================================================================== interiors
def room_walls(base="#2a2028", dark="#0c080c", floor="#1a120c"):
    s = lg("rw", [(0, base, 1), (1, dark, 1)]) + '<rect width="2400" height="1350" fill="url(#rw)"/>'
    s += '<rect width="2400" height="1350" fill="#000" filter="url(#plaster)" opacity="0.5"/>'
    s += f'<path d="M0,1080 L2400,1080 L2400,1350 L0,1350 Z" fill="{floor}"/>'
    for i in range(14):
        s += f'<path d="M{i*200-200},1350 L{1200+(i*200-1400)*0.4:.0f},1080" stroke="#0a0604" stroke-width="4" opacity="0.6"/>'
    s += '<path d="M0,1080 L2400,1080" stroke="#3a2a1c" stroke-width="12"/>'
    return s

def carmen_room_svg(red=False):
    s = room_walls("#2a2a3c" if not red else "#3a1416", "#0a0a12" if not red else "#120406")
    # tall balcony door open with moonlight
    s += '<path d="M1500,1080 L1500,300 Q1700,180 1900,300 L1900,1080 Z" fill="#0c1a2c"/>'
    s += '<path d="M1520,1080 L1520,320 Q1700,210 1880,320 L1880,1080 Z" fill="#1a3048"/>'
    s += glow(1700, 400, 320, "moon", 0.9)
    s += rail(((1520, 820), (1880, 820)), ((1520, 1060), (1880, 1060)), 9, hi=MOONRIM, w=1.2)
    s += '<path d="M1500,1080 L1500,300 Q1700,180 1900,300 L1900,1080" stroke="#1a120c" stroke-width="30" fill="none"/>'
    s += '<path d="M1500,310 C1440,500 1460,800 1420,1080 L1360,1080 C1400,800 1380,500 1470,300 Z" fill="#c8bca0" opacity="0.55"/>'  # curtain
    s += '<path d="M1520,1080 L1300,1350 L2200,1350 L1880,1080 Z" fill="url(#beamc)" opacity="0.6"/>'
    # canopy bed
    s += '<rect x="200" y="760" width="900" height="320" fill="#3a2a2a"/><rect x="200" y="740" width="900" height="60" fill="#e8dcc8"/>'
    s += '<path d="M200,800 L1100,800 L1140,1000 L160,1000 Z" fill="#6a2a34" opacity="0.9"/>' if not red else '<path d="M200,800 L1100,800 L1140,1000 L160,1000 Z" fill="#4a1014"/>'
    for x in (210, 1090):
        s += f'<rect x="{x-14}" y="300" width="28" height="780" fill="#1a100a"/>'
    s += '<path d="M180,300 L1120,300 L1120,360 Q650,420 180,360 Z" fill="#4a3a4a"/><path d="M180,360 C160,500 200,650 180,760 L240,760 C230,600 240,480 230,360 Z" fill="#5a4a5a" opacity="0.8"/>'
    # crucifix + small altar with candle
    s += '<path d="M1220,400 L1220,620 M1160,460 L1280,460" stroke="#1a100a" stroke-width="22"/>'
    s += '<rect x="1150" y="900" width="160" height="180" fill="#1a120c"/>' + candle_at(1230, 900, 90)
    if red:
        s += '<rect width="2400" height="1350" fill="#ff2010" opacity="0.08"/>' + glow(1230, 700, 700, "red", 0.4)
    return s

@art
def carmen_room(): return S(carmen_room_svg(False))
@art
def carmen_room_red(): return S(carmen_room_svg(True))
@art
def l_carmen_window(): return S(place(woman_full(rim=MOONRIM, fill="#0a0c14"), 1690, 1120, 0.8))
@art
def l_father_dagger(): return S(place(man_full(hat=False, cape=True, dagger=True, rim="#ff6040", fill="#060304"), 640, 1260, 1.05), glow(860, 700, 160, "red", 0.5))

@art
def father_study():
    s = room_walls("#2a2018", "#0a0604")
    # bookcase
    s += '<rect x="80" y="200" width="700" height="880" fill="#1a100a"/>'
    r = random.Random(2)
    for row in range(5):
        y = 240 + row * 170
        s += f'<rect x="100" y="{y+140}" width="660" height="16" fill="#0a0604"/>'
        x = 110
        while x < 740:
            w = r.uniform(18, 40); h = r.uniform(100, 138)
            s += f'<rect x="{x:.0f}" y="{y+140-h:.0f}" width="{w:.0f}" height="{h:.0f}" fill="{r.choice(["#3a1a14", "#2a2a1a", "#1a2028", "#4a3a20"])}"/>'
            x += w + 2
    # window with bars
    s += '<rect x="960" y="260" width="340" height="460" fill="#0e1a2a"/>' + glow(1130, 400, 260, "moon", 0.7)
    for i in range(5): s += f'<rect x="{975+i*72}" y="260" width="10" height="460" fill="#0a0604"/>'
    # desk with papers + candle
    s += '<path d="M1100,900 L2300,900 L2300,1150 L1100,1150 Z" fill="#2a1a0e"/><path d="M1080,880 L2320,880 L2320,920 L1080,920 Z" fill="#3a2414"/>'
    s += '<path d="M1700,860 L2000,850 L2010,880 L1700,890 Z" fill="#d8c8a0"/>'
    s += candle_at(1560, 880, 200)
    for i in range(6):
        s += f'<ellipse cx="{1300+i*30}" cy="{876-i*8}" rx="46" ry="12" fill="#c8c8d0"/>'
    return S(s)
@art
def l_father_back(): return S(place(man_full(hat=False, cape=True, rim="#ffb860"), 1250, 1350, 1.1))

@art
def stairs_interior():
    s = room_walls("#2a2420", "#080604", "#120c08")
    # staircase rising from lower-left to upper-right
    for i in range(14):
        x = 300 + i * 120; y = 1250 - i * 70
        s += f'<path d="M{x},{y} L{x+120},{y} L{x+120},{y+70} L{x},{y+70} Z" fill="{["#3a2a1c", "#2a1c12"][i%2]}"/>'
        s += f'<path d="M{x},{y} L{x+120},{y}" stroke="#ffb860" stroke-width="3" opacity="0.3"/>'
    s += '<path d="M300,1320 L300,1350 L2000,1350 L2000,330 Z" fill="#120a06"/>'
    # banister
    s += '<path d="M260,1080 L1960,90" stroke="#1a100a" stroke-width="26"/>'
    for i in range(15):
        x = 300 + i * 120
        s += f'<path d="M{x+60},{1250-i*70} L{x+60},{1056-i*70+20}" stroke="#1a100a" stroke-width="12"/>'
    s += glow(2100, 200, 500, "warm", 0.5) + '<rect x="2000" y="60" width="260" height="320" fill="#ffc865" opacity="0.4"/>'
    # niche with a saint
    s += '<path d="M560,560 L560,360 Q620,300 680,360 L680,560 Z" fill="#0c0806"/>' + candle_at(620, 560, 50)
    return S(s)
@art
def l_father_climb(): return S(place(man_full(hat=False, cape=True, dagger=True, step_up=True, rim="#ffb860"), 900, 960, 0.95),
                              '<g opacity="0.35" filter="url(#blur2)">' + place(man_full(hat=False, cape=True, dagger=True, step_up=True, fill="#000", rim=None), 1500, 900, 1.6) + '</g>')
@art
def l_brigida(): return S(place(woman_full(rebozo_head=True, candle=True, old=True, rim="#ffb860"), 700, 1270, 0.85))

@art
def door_burst():
    s = room_walls("#1e1a22", "#06050a")
    s += '<path d="M800,1080 L800,280 L1600,280 L1600,1080 Z" fill="#ffd9a0"/>' + glow(1200, 650, 900, "warm", 0.8)
    s += '<path d="M800,1080 L400,1350 L2000,1350 L1600,1080 Z" fill="url(#warmglow)" opacity="0.6"/>'
    s += '<path d="M800,280 L560,200 L560,1180 L800,1080 Z" fill="#2a1a0e"/>'  # door swung open
    for i in range(4): s += f'<circle cx="{620+i*40}" cy="{500+i*120}" r="10" fill="#6a5030"/>'
    s += '<path d="M780,1080 L780,260 L1620,260 L1620,1080" stroke="#1a100a" stroke-width="40" fill="none"/>'
    s += place(woman_full(rebozo_head=True, old=True, rim="#ffd27a", fill="#0a0806"), 420, 1330, 0.75)
    return S(s)
@art
def l_father_door(): return S(place(man_full(hat=False, cape=True, dagger=True, rim="#fff0c0", fill="#050304"), 1200, 1100, 0.8))

@art
def house_facade():
    s = sky("#060c18", "#1c3048") + stars(80, 6, 300) + glow(1900, 120, 500, "moon", 0.7)
    s += f'<rect x="300" y="160" width="1800" height="1100" fill="#3a3448"/>' + '<rect x="300" y="160" width="1800" height="1100" fill="#000" filter="url(#plaster)" opacity="0.55"/>'
    s += f'<rect x="270" y="130" width="1860" height="50" fill="#1a1820"/><path d="M270,130 L2130,130" stroke="{MOONRIM}" stroke-width="4" opacity="0.5"/>'
    # cantera frames
    for x in (520, 1700):
        s += f'<rect x="{x-20}" y="300" width="220" height="330" fill="#6a5a50"/><rect x="{x}" y="320" width="180" height="300" fill="#0a0e14"/>'
        for i in range(6): s += f'<rect x="{x+10+i*30}" y="320" width="8" height="300" fill="#05070a"/>'
    s += '<rect x="1060" y="280" width="280" height="380" fill="#6a5a50"/><rect x="1080" y="300" width="240" height="360" fill="#0a0e14"/>'
    s += rail(((1010, 560), (1390, 560)), ((1010, 680), (1390, 680)), 10, hi=MOONRIM) + '<rect x="990" y="680" width="420" height="24" fill="#2a2420"/>'
    # big portal (zaguán)
    s += '<path d="M940,1260 L940,860 Q1200,720 1460,860 L1460,1260 Z" fill="#7a6a5a"/>'
    s += '<path d="M980,1260 L980,880 Q1200,760 1420,880 L1420,1260 Z" fill="#2a1a0e"/>'
    for i in range(5):
        for j in range(8):
            s += f'<circle cx="{1020+i*90}" cy="{900+j*45}" r="7" fill="#8a7a5a"/>'
    s += '<path d="M1200,800 L1200,1260" stroke="#120a06" stroke-width="10"/>'
    s += '<circle cx="1170" cy="1080" r="18" stroke="#8a7a5a" stroke-width="6" fill="none"/><circle cx="1230" cy="1080" r="18" stroke="#8a7a5a" stroke-width="6" fill="none"/>'
    s += lamp(700, 1260, 400, True) + cobbles(1260, 1350)
    return S(s)
WIN_RED = [(1200, 480), (610, 470), (1790, 470)]
@art
def l_window_red(): return S(*[glow(x, y, 260, "red", 0.8) + f'<rect x="{x-110}" y="{y-170}" width="220" height="330" fill="#ff5030" opacity="0.25"/>' for x, y in WIN_RED[:1]])

@art
def temple_facade():
    s = sky("#1a2240", "#c07060", "#5a4a70") + glow(1200, 900, 900, "warm", 0.4)
    k = 1.25; x = 1200; yb = 1150
    col = "#b88a6a"
    s += f'<rect x="{x-560}" y="{yb-880}" width="1120" height="880" fill="{col}"/>'
    s += '<rect x="640" y="270" width="1120" height="880" fill="#000" filter="url(#plaster)" opacity="0.35"/>'
    for side in (-1, 1):
        tx = x + side * 460
        s += f'<rect x="{tx-110}" y="{yb-1150}" width="220" height="1150" fill="#a87a5c"/>'
        s += f'<path d="M{tx-80},{yb-1150} Q{tx},{yb-1300} {tx+80},{yb-1150} Z" fill="#9a6e52"/>'
        s += f'<path d="M{tx-40},{yb-1000} L{tx-40},{yb-1060} A40,40 0 0 1 {tx+40},{yb-1060} L{tx+40},{yb-1000} Z" fill="#1a1410"/>'
    # baroque portal: columns + niches + door
    for i in range(4):
        cx = 900 + i * 200
        s += f'<rect x="{cx-22}" y="{yb-640}" width="44" height="640" fill="#d8b090"/><rect x="{cx-30}" y="{yb-660}" width="60" height="24" fill="#c8a080"/>'
    s += f'<path d="M1060,{yb} L1060,{yb-380} Q1200,{yb-520} 1340,{yb-380} L1340,{yb} Z" fill="#1a0e08"/>'
    s += glow(1200, yb - 200, 260, "warm", 0.7)
    s += f'<path d="M1080,{yb} L1080,{yb-370} Q1200,{yb-490} 1320,{yb-370} L1320,{yb} Z" fill="#ffc865" opacity="0.55"/>'
    s += f'<circle cx="1200" cy="{yb-760}" r="70" fill="#3a2a20"/><circle cx="1200" cy="{yb-760}" r="54" fill="#e0b060" opacity="0.7"/>'
    s += '<path d="M0,1150 L2400,1150 L2400,1350 L0,1350 Z" fill="#2a2024"/>'
    for i, (px, h) in enumerate(((300, 420), (420, 380), (1900, 400), (2050, 440), (2200, 360))):
        s += place(woman_full(rebozo_head=True, rim="#ffb880", fill="#120c10") if i % 2 == 0 else man_full(hat=True, cape=False, rim="#ffb880", fill="#120c10"), px, 1320, h / 1000)
    return S(s)
@art
def l_brigida_carmen():
    return S(place(woman_full(rebozo_head=True, old=True, rim="#ffb880", fill="#0c080c"), 800, 1330, 0.5),
             place(woman_full(rebozo_head=False, rim="#ffd8a0", fill="#0c0a14"), 950, 1330, 0.48))

@art
def temple_interior():
    s = '<rect width="2400" height="1350" fill="#0c0806"/>'
    # nave vanishing to a golden altar
    s += '<path d="M700,0 L1700,0 L1500,500 L900,500 Z" fill="#1a120c"/>'
    s += '<path d="M950,300 L1450,300 L1450,900 L950,900 Z" fill="#6a4a1a"/>' + glow(1200, 600, 600, "warm", 0.9)
    r = random.Random(2)
    for i in range(40):  # gilded retablo detail
        x = r.uniform(960, 1440); y = r.uniform(310, 890)
        s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(6,18):.0f}" fill="#e0b050" opacity="0.6"/>'
    for i in range(5):
        s += f'<rect x="{980+i*100}" y="320" width="20" height="570" fill="#c89838" opacity="0.8"/>'
    s += '<path d="M1160,420 L1160,620 M1100,480 L1220,480" stroke="#2a1a08" stroke-width="16"/>'
    # columns either side
    for side in (-1, 1):
        for i, f in enumerate((0.0, 0.35, 0.6)):
            x = 1200 + side * (1150 - f * 800); w = 200 - f * 120
            s += f'<rect x="{x-w/2:.0f}" y="0" width="{w:.0f}" height="{1350-f*500:.0f}" fill="{["#2a2018", "#221a12", "#1a140e"][i]}"/>'
            s += f'<rect x="{x-w/2+w*0.1 if side<0 else x+w/2-w*0.18:.0f}" y="0" width="{w*0.08:.0f}" height="{1350-f*500:.0f}" fill="#ffb860" opacity="0.25"/>'
    # pews + kneeling people
    for i in range(6):
        y = 1350 - i * 80; hw = 900 - i * 90
        s += f'<rect x="{1200-hw}" y="{y-40}" width="{hw*2}" height="30" fill="#140c06"/>'
    for i in range(10):
        x = 500 + i * 150 + r.uniform(-30, 30)
        s += place(woman_full(rebozo_head=True, fill="#080506", rim="#ffb860"), x, 1200 - (i % 3) * 60, 0.25 + (i % 3) * 0.02)
    # candles
    for i in range(12):
        x = 960 + i * 44
        s += candle_at(x, 920, 60).replace('r="700"', 'r="80"')
    s += clouds(8, 200, 700, 5, "#ffd8a0", (0.04, 0.1), (200, 400), (60, 140))
    return S(s)
@art
def l_luis_column(): return S(place(man_full(hat=False, cape=False, rim="#ffb860"), 1780, 1150, 0.6))

@art
def plazuela():
    s = sky("#08101e", "#22344c") + stars(120, 8, 400) + moon(1900, 220, 70)
    s += houses_hill(-50, 2450, 820, 0.0, 21, PAL["night"]["walls"], 0.4, 3.0)
    # narrow alley opening in the middle
    s += '<path d="M1120,1100 L1120,520 L1280,520 L1280,1100 Z" fill="#05070a"/>' + glow(1200, 700, 200, "warm", 0.6)
    s += '<rect x="0" y="1050" width="2400" height="300" fill="#2a2a30"/>' + cobbles(1100, 1350)
    s += lamp(700, 1120, 460, True) + lamp(1700, 1120, 460, True)
    # small fountain / pedestal
    s += '<ellipse cx="1200" cy="1230" rx="260" ry="50" fill="#4a4a50"/><rect x="1170" y="1080" width="60" height="150" fill="#3a3a40"/><ellipse cx="1200" cy="1080" rx="90" ry="20" fill="#5a5a60"/>'
    s += '<text x="1200" y="500" font-family="Cinzel" font-size="40" fill="#d8c8a0" text-anchor="middle" opacity="0.85">CALLEJÓN DEL BESO</text>'
    return S(s)

@art
def docs():
    s = '<rect width="2400" height="1350" fill="#1a120a"/>'
    s += '<path d="M260,140 L2140,110 L2180,1240 L230,1270 Z" fill="#d8c49a"/><path d="M260,140 L2140,110 L2180,1240 L230,1270 Z" fill="#000" filter="url(#plaster)" opacity="0.35"/>'
    # hand-drawn map of the cañada
    s += '<path d="M400,1000 C700,820 900,880 1200,700 C1500,520 1700,560 2000,380" stroke="#4a6a8a" stroke-width="10" fill="none" opacity="0.7"/>'
    r = random.Random(4)
    for i in range(60):
        x = r.uniform(400, 2000); y = 1000 - (x - 400) * 0.38 + r.uniform(-160, 160)
        s += f'<rect x="{x:.0f}" y="{y:.0f}" width="{r.uniform(20,40):.0f}" height="{r.uniform(16,30):.0f}" fill="none" stroke="#5a3a20" stroke-width="3" opacity="0.7"/>'
    for (x, y) in ((500, 400), (900, 260), (1700, 1000), (1900, 900)):
        s += f'<path d="M{x-120},{y+60} L{x},{y-60} L{x+120},{y+60}" stroke="#5a3a20" stroke-width="5" fill="none"/>'
    s += '<text x="1200" y="250" font-family="IM FELL English" font-size="96" fill="#3a2414" text-anchor="middle">Santa Fe y Real de Minas de Guanaxuato</text>'
    s += '<circle cx="1210" cy="690" r="40" stroke="#8a1a14" stroke-width="6" fill="none"/><text x="1270" y="660" font-family="IM FELL English" font-style="italic" font-size="48" fill="#8a1a14">¿aquí?</text>'
    s += '<circle cx="1900" cy="1120" r="80" stroke="#3a2414" stroke-width="5" fill="none"/><path d="M1900,1040 L1900,1200 M1820,1120 L1980,1120" stroke="#3a2414" stroke-width="4"/>'
    return S(s)

@art
def empty_balcony():
    s = sky("#0a1424", "#3a4a6a") + glow(1200, 200, 700, "moon", 0.8)
    s += '<rect x="0" y="0" width="2400" height="1350" fill="#2a3448"/>' + '<rect width="2400" height="1350" fill="#000" filter="url(#plaster)" opacity="0.5"/>'
    s += '<path d="M700,1000 L700,180 Q1200,40 1700,180 L1700,1000 Z" fill="#05070a"/>'
    s += '<path d="M760,1000 C800,700 760,400 820,190 L1000,140 C900,400 980,700 940,1000 Z" fill="#cfc6b0" opacity="0.55"/>'  # curtain blowing
    s += '<path d="M680,1000 L1720,1000 L1800,1080 L600,1080 Z" fill="#4a4440"/><path d="M600,1080 L1800,1080 L1800,1120 L600,1120 Z" fill="#1a1814"/>'
    s += rail(((620, 760), (1780, 760)), ((620, 1060), (1780, 1060)), 16, hi=MOONRIM, w=1.6)
    # jasmine flower fallen on the balcony floor
    for a in range(5):
        ang = math.radians(a * 72)
        s += f'<ellipse cx="{1350+math.cos(ang)*18:.0f}" cy="{1040+math.sin(ang)*8:.0f}" rx="16" ry="8" fill="#efe6d2" transform="rotate({a*72} {1350+math.cos(ang)*18:.0f} {1040+math.sin(ang)*8:.0f})"/>'
    s += '<circle cx="1350" cy="1040" r="7" fill="#d9a63a"/>'
    s += '<path d="M0,1120 L2400,1120 L2400,1350 L0,1350 Z" fill="#0a0e14"/>'
    return S(s)

# ===================================================================== hands
def hand(x, y, k, rot, sk, flip=False, limp=False):
    """slender hand reaching +x, wrist at 0,0 (based on base_chars.hand_open with a new skin)."""
    c = sk["base"]
    s = (f'<path d="M-260,-40 L0,-26 L0,22 L-260,40 Z" fill="{sk["shadow"]}"/>'
         f'<path d="M0,-22 C30,-30 70,-30 92,-24 C112,-20 136,-16 150,-8 C158,-4 156,6 146,6 C130,4 112,2 98,6 '
         f'C120,10 140,14 148,20 C154,26 148,34 138,32 C120,28 104,24 92,26 C110,32 124,38 128,44 C130,52 122,56 114,52 '
         f'C100,46 86,40 76,40 C84,48 90,56 88,62 C84,68 76,66 70,60 C56,48 40,34 24,28 C10,24 0,20 -4,10 Z" fill="{c}"/>'
         f'<path d="M30,-24 C50,-28 80,-28 100,-20" stroke="{sk["hi"]}" stroke-width="5" fill="none" opacity="0.6"/>'
         f'<path d="M98,6 C106,4 116,2 126,4 M92,26 C100,26 110,28 118,30 M76,40 C84,40 92,44 100,48" stroke="{sk["deep"]}" stroke-width="2.5" fill="none" opacity="0.6"/>'
         f'<path d="M-260,-40 L0,-26" stroke="{MOONRIM}" stroke-width="4" opacity="0.5"/>')
    fl = " scale(1,-1)" if flip else ""
    return f'<g transform="translate({x},{y}) rotate({rot}) scale({k}){fl}">{s}</g>'

def sleeve(x, y, k, rot, col, lace=True):
    s = f'<path d="M-520,-90 L-240,-60 L-240,60 L-520,100 Z" fill="{col}"/>'
    if lace:
        s += '<path d="M-250,-64 C-230,-40 -240,0 -226,30 C-240,50 -236,60 -250,66" stroke="#e8e0cc" stroke-width="16" fill="none"/>'
    return f'<g transform="translate({x},{y}) rotate({rot}) scale({k})">{s}</g>'

def hands_svg(kiss=False):
    s = sky("#050a14", "#1a2a40") + glow(1200, 200, 800, "moon", 0.9) + stars(60, 7, 400)
    s += f'<g {CLOSE.replace("2.1", "4.2")}>' + "</g>"
    # two railings converging
    s += rail(((0, 900), (1050, 760)), ((0, 1350), (1050, 1150)), 7, hi=MOONRIM, w=2.4)
    s += rail(((2400, 900), (1350, 760)), ((2400, 1350), (1350, 1150)), 7, hi=MOONRIM, w=2.4)
    s += '<path d="M0,0 L900,0 L1050,760 L0,900 Z" fill="#141c28"/><path d="M2400,0 L1500,0 L1350,760 L2400,900 Z" fill="#1a1a28"/>'
    s += '<path d="M0,0 L900,0 L1050,760 L0,900 Z M2400,0 L1500,0 L1350,760 L2400,900 Z" fill="#000" filter="url(#plaster)" opacity="0.5"/>'
    s += '<path d="M1050,760 L1350,760 L1500,0 L900,0 Z" fill="#0a1424" opacity="0.5"/>'
    if not kiss:
        s += sleeve(1010, 720, 1.4, -8, "#1a3448") + hand(1010, 720, 1.4, -8, SK_CARMEN)
        s += f'<g transform="translate(2400,0) scale(-1,1)">' + sleeve(1060, 700, 1.4, 6, "#3e2a1a", lace=False) + hand(1060, 700, 1.4, 6, SK_LUIS, flip=True) + '</g>'
    else:
        # her limp hand hanging over the railing; his face (silhouette) kissing it
        s += sleeve(1000, 800, 1.4, 24, "#1a3448") + hand(1000, 800, 1.4, 30, SK_CARMEN)
        s += place(profile_figure("man", lean=-25, rim=MOONRIM), 1500, 760, 1.6, flip=True)
        s += f'<g transform="translate(2400,0) scale(-1,1)">' + hand(1110, 900, 1.3, -30, SK_LUIS, flip=True) + '</g>'
    return s
@art
def hands_reach(): return S(hands_svg(False))
@art
def hand_kiss(): return S(hands_svg(True), '<rect width="2400" height="1350" fill="#0a1830" opacity="0.15"/>')

# ===================================================================== portraits
def portrait_bg(kind="moon"):
    if kind == "moon":
        return sky("#060c18", "#1a2a40") + glow(1700, 300, 900, "moon", 0.8) + clouds(8, 100, 900, 3, "#2a3a52", (0.2, 0.4))
    if kind == "candle":
        return '<rect width="2400" height="1350" fill="#0c0806"/>' + glow(700, 600, 1100, "warm", 0.6) + '<rect width="2400" height="1350" fill="#000" filter="url(#plaster)" opacity="0.6"/>'
    if kind == "red":
        return '<rect width="2400" height="1350" fill="#0c0204"/>' + glow(1200, 600, 1200, "red", 0.55)
    if kind == "ghost":
        return '<rect width="2400" height="1350" fill="#02050a"/>' + glow(1200, 500, 1000, "moon", 0.6)
@art
def carmen_portrait(): return S(portrait_bg("moon"), carmen_bust(1200, 560, 1.75, look=0.2, lids=0.3, smile=0.1))
@art
def carmen_portrait_fear(): return S(portrait_bg("candle"), carmen_bust(1200, 560, 1.75, look=-0.6, turn=-0.2, fear=True, rim="#ffb860"))
@art
def carmen_portrait_ghost():
    return S(portrait_bg("ghost"), f'<g filter="url(#ghost)" opacity="0.8">' + carmen_bust(1200, 560, 1.75, eyes_closed=False, lids=0.0, smile=-0.2, rim="#dfeaff", wind=1.0) + '</g>',
             '<rect width="2400" height="1350" fill="#6a9ac8" opacity="0.25" style="mix-blend-mode:color"/>',
             ''.join(f'<circle cx="{x}" cy="502" r="16" fill="#e8f4ff" opacity="0.9"/>' for x in (1146, 1254)))
@art
def luis_portrait(): return S(portrait_bg("moon"), luis_bust(1200, 560, 1.75, look=-0.2, turn=-0.1))
@art
def father_portrait(): return S(portrait_bg("candle"), father_bust(1200, 560, 1.75, rim="#ffb860"))
@art
def father_portrait_red(): return S(portrait_bg("red"), father_bust(1200, 560, 1.75, red=True))
@art
def brigida_portrait(): return S(portrait_bg("candle"), brigida_bust(1200, 560, 1.75))
@art
def suitor_portrait(): return S(portrait_bg("candle"), noble_bust(1200, 560, 1.75), candle_at(2000, 1300, 160))
@art
def balcony_pov():
    """view from Luis' balcony across the alley to Carmen's lit window."""
    s = sky("#050a14", "#1a2a40") + stars(50, 12, 200)
    s += '<rect x="0" y="0" width="2400" height="1350" fill="#2b3a4c"/><rect width="2400" height="1350" fill="#000" filter="url(#plaster)" opacity="0.55"/>'
    s += '<path d="M0,0 L2400,0 L2400,90 L0,140 Z" fill="#0a1424"/>' + glow(1200, 0, 700, "moon", 0.7)
    s += '<path d="M820,900 L820,260 Q1100,160 1380,260 L1380,900 Z" fill="#ffc865"/>' + glow(1100, 560, 600, "warm", 0.6)
    s += '<path d="M840,900 C880,700 850,420 900,270 L1060,220 C980,420 1040,700 1000,900 Z" fill="#e8d0a0" opacity="0.45"/>'
    s += '<path d="M820,900 L820,260 Q1100,160 1380,260 L1380,900" stroke="#2a2018" stroke-width="24" fill="none"/>'
    s += '<path d="M700,900 L1500,900 L1560,960 L640,960 Z" fill="#3a3530"/>'
    s += rail(((660, 700), (1540, 700)), ((660, 940), (1540, 940)), 12, hi=MOONRIM, w=1.4)
    s += flowerpot(760, 690, 2.2, 5, "night") + flowerpot(1460, 690, 2.0, 6, "night")
    # Luis' own railing in the foreground (blurred)
    s += f'<g filter="url(#blur1)">' + rail(((0, 1180), (2400, 1220)), ((0, 1450), (2400, 1450)), 10, w=3.0) + '</g>'
    return S(s)
@art
def l_carmen_window_far(): return S(place(woman_full(rim="#ffd8a0", fill="#0a0608"), 1120, 880, 0.55))


def run(names):
    for n in names:
        if n in ART:
            open(os.path.join(A, n + ".svg"), "w", encoding="utf-8").write(ART[n]())
    print("svg written:", len(names))
    import subprocess
    from PIL import Image
    B = os.path.join(HERE, "build"); os.makedirs(B, exist_ok=True)
    for n, (fn, sc, cx, cy) in CROPS.items():
        if names and n not in names: continue
        src = os.path.join(B, n + ".svg"); open(src, "w").write(fn())
        subprocess.run(["node", "/home/claude/pipeline/render_svg.js", src, "--width", str(int(W * sc))], check=True, capture_output=True)
        im = Image.open(src[:-4] + ".png").convert("RGB")
        x0 = int((cx - cx / sc) * sc); y0 = int((cy - cy / sc) * sc)
        im.crop((x0, y0, x0 + W, y0 + H)).save(os.path.join(A, n + ".png"))
        print("crop", n)

if __name__ == "__main__":
    run(sys.argv[1:] or (list(ART) + list(CROPS)))
