#!/usr/bin/env python3
"""Illustrations for 'La Mulata de Córdoba'. Usage: python3 make_art.py [name ...]  (no args = all)
Writes art/<name>.svg ; then: node /home/claude/pipeline/render_svg.js art/*.svg"""
import sys, os, math, random
sys.path.insert(0, '/home/claude/pipeline'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from art import *
from chars import *

ART = {}
def art(fn):
    ART[fn.__name__] = fn; return fn

EXTRA_DEFS = '''<defs>
<filter id="charcoal" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="3" result="t"/>
<feDisplacementMap in="SourceGraphic" in2="t" scale="7" xChannelSelector="R" yChannelSelector="G" result="d"/>
<feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="1" seed="8" result="g"/><feColorMatrix in="g" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -1.1 1.4" result="ga"/>
<feComposite in="d" in2="ga" operator="in"/></filter>
<filter id="rough" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency="0.02" numOctaves="3" seed="5" result="t"/>
<feDisplacementMap in="SourceGraphic" in2="t" scale="16" xChannelSelector="R" yChannelSelector="G"/></filter>
<filter id="stone" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.012 0.03" numOctaves="4" seed="11" result="n"/>
<feColorMatrix in="n" type="matrix" values="0 0 0 0 0.05  0 0 0 0 0.04  0 0 0 0 0.03  0 0 0 0.9 -0.25"/><feComposite in2="SourceGraphic" operator="in"/></filter>
<filter id="pits" x="0" y="0" width="100%" height="100%"><feTurbulence type="turbulence" baseFrequency="0.08" numOctaves="2" seed="21" result="n"/>
<feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -2.2 1.1"/><feComposite in2="SourceGraphic" operator="in"/></filter>
<filter id="softglow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="22" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<linearGradient id="beam" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff2d0" stop-opacity="0.55"/><stop offset="1" stop-color="#fff2d0" stop-opacity="0"/></linearGradient>
<linearGradient id="beamcold" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#cfe0ff" stop-opacity="0.5"/><stop offset="1" stop-color="#cfe0ff" stop-opacity="0"/></linearGradient>
</defs>'''

def S(*parts):
    return svg(EXTRA_DEFS, *parts)

def lingrad(id_, stops, x1=0, y1=0, x2=0, y2=1):
    s = "".join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a}"/>' for o, c, a in stops)
    return f'<defs><linearGradient id="{id_}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">{s}</linearGradient></defs>'

def radgrad(id_, stops, cx=0.5, cy=0.5, r=0.5):
    s = "".join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a}"/>' for o, c, a in stops)
    return f'<defs><radialGradient id="{id_}" cx="{cx}" cy="{cy}" r="{r}">{s}</radialGradient></defs>'

# ================================================================== helpers
def clouds(n, y0, y1, seed, color, op=(0.3, 0.7), rx=(160, 420), ry=(40, 110), blur="blur3"):
    r = random.Random(seed)
    return f'<g filter="url(#{blur})">' + "".join(
        f'<ellipse cx="{r.uniform(-100, W+100):.0f}" cy="{r.uniform(y0, y1):.0f}" rx="{r.uniform(*rx):.0f}" ry="{r.uniform(*ry):.0f}" fill="{color}" opacity="{r.uniform(*op):.2f}"/>'
        for _ in range(n)) + '</g>'

def stone_blocks(x0, y0, x1, y1, seed=1, base="#5d564b", dark="#2c2823", light="#8a8172", bh=(60, 110), bw=(110, 260), mortar="#1e1b17"):
    """Irregular coral-stone masonry."""
    r = random.Random(seed)
    s = f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" fill="{mortar}"/>'
    y = y0
    while y < y1:
        h = r.uniform(*bh); x = x0 - r.uniform(0, 120)
        while x < x1:
            w = r.uniform(*bw)
            c = r.choice([base, base, light, dark, base])
            rx = r.uniform(4, 14)
            s += f'<rect x="{x+3:.0f}" y="{y+3:.0f}" width="{w-6:.0f}" height="{h-6:.0f}" rx="{rx:.0f}" fill="{c}" opacity="{r.uniform(0.75,1):.2f}"/>'
            s += f'<rect x="{x+6:.0f}" y="{y+5:.0f}" width="{w-14:.0f}" height="4" fill="#ffffff" opacity="0.06"/>'
            x += w
        y += h
    s += f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" fill="#000" filter="url(#pits)" opacity="0.5"/>'
    s += f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" fill="#000" filter="url(#stone)"/>'
    return s

def palm(x, y, h=700, lean=0.0, seed=1, color="#0a0f0c", frond="#0d1712", nf=9):
    """Coconut/royal palm silhouette, base (x,y)."""
    r = random.Random(seed)
    tx, ty = x + lean * h, y - h
    s = f'<path d="M{x-14},{y} Q{x+lean*h*0.3:.0f},{y-h*0.5:.0f} {tx-6:.0f},{ty:.0f} L{tx+6:.0f},{ty:.0f} Q{x+lean*h*0.3+18:.0f},{y-h*0.5:.0f} {x+14},{y} Z" fill="{color}"/>'
    for i in range(nf):
        a = math.radians(-180 + i * (360 / nf) + r.uniform(-12, 12)); L = r.uniform(h * 0.32, h * 0.46)
        ex, ey = tx + math.cos(a) * L, ty + math.sin(a) * L * 0.45 + L * 0.35
        cx, cy = tx + math.cos(a) * L * 0.5, ty - abs(math.sin(a)) * L * 0.25 - 30
        s += f'<path d="M{tx:.0f},{ty:.0f} Q{cx:.0f},{cy:.0f} {ex:.0f},{ey:.0f}" stroke="{frond}" stroke-width="7" fill="none"/>'
        for j in range(14):
            t = 0.15 + j * 0.06
            px = (1 - t) ** 2 * tx + 2 * (1 - t) * t * cx + t * t * ex; py = (1 - t) ** 2 * ty + 2 * (1 - t) * t * cy + t * t * ey
            ll = L * 0.22 * (1 - t * 0.6)
            for sgn in (-1, 1):
                s += f'<path d="M{px:.0f},{py:.0f} l{sgn*ll*0.35:.0f},{ll:.0f}" stroke="{frond}" stroke-width="4" stroke-linecap="round"/>'
    return s

def banana(x, y, h=500, seed=2, color="#0b140e", hi=None):
    r = random.Random(seed); s = f'<path d="M{x-16},{y} L{x-10},{y-h*0.55:.0f} L{x+10},{y-h*0.55:.0f} L{x+16},{y} Z" fill="{color}"/>'
    for i in range(7):
        a = math.radians(-160 + i * 24 + r.uniform(-8, 8)); L = r.uniform(h * 0.45, h * 0.7)
        bx, by = x, y - h * 0.55
        ex, ey = bx + math.cos(a) * L, by + math.sin(a) * L * 0.8
        nx, ny = -(ey - by), (ex - bx); nl = math.hypot(nx, ny) or 1; nx, ny = nx / nl * L * 0.16, ny / nl * L * 0.16
        mx, my = (bx + ex) / 2, (by + ey) / 2 - L * 0.12
        s += f'<path d="M{bx:.0f},{by:.0f} Q{mx+nx:.0f},{my+ny:.0f} {ex:.0f},{ey:.0f} Q{mx-nx*0.6:.0f},{my-ny*0.6:.0f} {bx:.0f},{by:.0f} Z" fill="{color}"/>'
        if hi:
            s += f'<path d="M{bx:.0f},{by:.0f} Q{mx:.0f},{my:.0f} {ex:.0f},{ey:.0f}" stroke="{hi}" stroke-width="2" fill="none" opacity="0.5"/>'
    return s

def cane(x0, x1, y, h=420, seed=3, color="#0d160c", n=160, hi=None):
    r = random.Random(seed); s = ""
    for _ in range(n):
        x = r.uniform(x0, x1); hh = r.uniform(h * 0.6, h); lean = r.uniform(-30, 30)
        s += f'<path d="M{x:.0f},{y} Q{x+lean*0.3:.0f},{y-hh*0.5:.0f} {x+lean:.0f},{y-hh:.0f}" stroke="{color}" stroke-width="{r.uniform(3,6):.1f}" fill="none"/>'
        for j in range(3):
            t = r.uniform(0.4, 1.0); px, py = x + lean * t, y - hh * t; d = r.choice((-1, 1)); L = r.uniform(60, 140)
            s += f'<path d="M{px:.0f},{py:.0f} Q{px+d*L*0.5:.0f},{py-L*0.4:.0f} {px+d*L:.0f},{py+L*0.15:.0f}" stroke="{color}" stroke-width="{r.uniform(2.5,4.5):.1f}" fill="none" stroke-linecap="round"/>'
            if hi and r.random() < 0.3:
                s += f'<path d="M{px:.0f},{py:.0f} Q{px+d*L*0.5:.0f},{py-L*0.4:.0f} {px+d*L:.0f},{py+L*0.15:.0f}" stroke="{hi}" stroke-width="1.5" fill="none" opacity="0.5"/>'
    return s

def volcano(cx, base_y, w=1500, h=620, color="#2a3a52", snow="#e9eef5", snow_shadow="#9fb0c8", seed=4):
    """Pico de Orizaba: steep symmetric cone with a broad snow cap."""
    r = random.Random(seed)
    pts = [(cx - w / 2, base_y), (cx - w * 0.22, base_y - h * 0.62), (cx - w * 0.07, base_y - h * 0.95), (cx - 20, base_y - h),
           (cx + 30, base_y - h * 0.99), (cx + w * 0.09, base_y - h * 0.9), (cx + w * 0.25, base_y - h * 0.55), (cx + w / 2, base_y)]
    s = f'<path d="M{" L".join(f"{x:.0f},{y:.0f}" for x, y in pts)} Z" fill="{color}"/>'
    sl = h * 0.42  # snow line
    snow_d = (f"M{cx - w*0.07:.0f},{base_y-h*0.95:.0f} L{cx-20:.0f},{base_y-h:.0f} L{cx+30:.0f},{base_y-h*0.99:.0f} L{cx+w*0.09:.0f},{base_y-h*0.9:.0f} "
              f"L{cx+w*0.16:.0f},{base_y-h*0.74:.0f} ")
    xs = [cx + w * 0.16 - i * (w * 0.32 + w * 0.14) / 14 for i in range(15)]
    for i, x in enumerate(xs):
        frac = (x - (cx - w * 0.3)) / (w * 0.46 + 1)
        yy = base_y - h * 0.74 + (r.uniform(10, 70) if i % 2 else r.uniform(-10, 20)) + 20 * math.sin(i)
        snow_d += f"L{x:.0f},{yy + abs(x-cx)*0.05:.0f} "
    snow_d += f"L{cx - w*0.2:.0f},{base_y-h*0.62:.0f} Z"
    s += f'<path d="{snow_d}" fill="{snow}"/>'
    s += f'<path d="M{cx-20:.0f},{base_y-h:.0f} L{cx+30:.0f},{base_y-h*0.99:.0f} L{cx+w*0.09:.0f},{base_y-h*0.9:.0f} L{cx+w*0.16:.0f},{base_y-h*0.74:.0f} L{cx+40:.0f},{base_y-h*0.7:.0f} Z" fill="{snow_shadow}" opacity="0.7"/>'
    for i in range(9):
        x = cx - w * 0.15 + i * w * 0.04
        s += f'<path d="M{x:.0f},{base_y-h*0.8:.0f} l{r.uniform(-20,20):.0f},{r.uniform(80,200):.0f}" stroke="{snow_shadow}" stroke-width="5" opacity="0.5"/>'
    return s

def waves(y0, y1, seed=5, color="#0b1a24", crest="#9fb6c9", n=90, amp=1.0):
    r = random.Random(seed); s = ""
    for _ in range(n):
        y = r.uniform(y0, y1); x = r.uniform(-100, W); w = r.uniform(80, 260) * (0.5 + (y - y0) / (y1 - y0 + 1))
        hh = r.uniform(8, 22) * amp * (0.5 + (y - y0) / (y1 - y0 + 1))
        s += f'<path d="M{x:.0f},{y:.0f} Q{x+w*0.5:.0f},{y-hh:.0f} {x+w:.0f},{y:.0f}" stroke="{crest}" stroke-width="{1.5+hh*0.12:.1f}" fill="none" opacity="{r.uniform(0.2,0.6):.2f}"/>'
    return s

def fortress(x, y, k=1.0, color="#1b2129", lit=True, light="#e0a85a", detail=True):
    """San Juan de Ulúa: low coral-stone walls with pointed bastions, the tall 'caballero alto' tower and a lighthouse tower.
    (x,y) = centre of the waterline; ~1500*k wide."""
    s = ""
    def P(pts): return " ".join(f"{x + px*k:.0f},{y + py*k:.0f}" for px, py in pts)
    # outer wall + bastions
    s += f'<polygon points="{P([(-760,0),(-760,-120),(-700,-150),(-620,-120),(-560,-150),(560,-150),(640,-120),(720,-150),(780,-120),(780,0)])}" fill="{color}"/>'
    s += f'<polygon points="{P([(-820,0),(-700,-150),(-600,0)])}" fill="{color}"/>'
    s += f'<polygon points="{P([(600,0),(720,-150),(840,0)])}" fill="{color}"/>'
    # inner walls stepping up
    s += f'<polygon points="{P([(-520,-150),(-520,-230),(520,-230),(520,-150)])}" fill="{color}"/>'
    s += f'<polygon points="{P([(-300,-230),(-300,-300),(300,-300),(300,-230)])}" fill="{color}"/>'
    # caballero alto (square tower) + lighthouse tower
    s += f'<polygon points="{P([(-80,-300),(-80,-470),(90,-470),(90,-300)])}" fill="{color}"/>'
    s += f'<polygon points="{P([(-96,-470),(106,-470),(106,-490),(-96,-490)])}" fill="{color}"/>'
    s += f'<polygon points="{P([(380,-230),(380,-430),(450,-430),(450,-230)])}" fill="{color}"/>'
    s += f'<polygon points="{P([(370,-430),(460,-430),(415,-480)])}" fill="{color}"/>'
    # crenellation notches
    for px in range(-500, 520, 70):
        s += f'<rect x="{x+px*k:.0f}" y="{y-250*k:.0f}" width="{30*k:.0f}" height="{20*k:.0f}" fill="{color}"/>'
    for px in range(-740, 780, 90):
        s += f'<rect x="{x+px*k:.0f}" y="{y-170*k:.0f}" width="{36*k:.0f}" height="{22*k:.0f}" fill="{color}"/>'
    if detail:
        for px in range(-700, 760, 140):
            s += f'<rect x="{x+px*k:.0f}" y="{y-90*k:.0f}" width="{22*k:.0f}" height="{14*k:.0f}" fill="#06080b"/>'
        s += f'<path d="M{x-40*k:.0f},{y:.0f} L{x-40*k:.0f},{y-70*k:.0f} A{40*k:.0f},{40*k:.0f} 0 0 1 {x+40*k:.0f},{y-70*k:.0f} L{x+40*k:.0f},{y:.0f} Z" fill="#06080b"/>'
    if lit:
        for (px, py) in [(-40, -400), (30, -400), (400, -380), (-400, -200), (200, -270), (-200, -270)]:
            s += glow(x + px * k + 10 * k, y + py * k + 15 * k, 70 * k, "warm", 0.6)
            s += f'<rect x="{x+px*k:.0f}" y="{y+py*k:.0f}" width="{20*k:.0f}" height="{30*k:.0f}" fill="{light}"/>'
        s += glow(x + 415 * k, y - 450 * k, 160 * k, "warm", 0.9)
    return s

def ship(x, y, k=1.0, mode="charcoal", seed=1, jitter=True, water=True):
    """Brigantine, waterline centre (x,y); ~900*k wide. mode: charcoal (lines) | color (filled, glowing) | silhouette | ghost."""
    r = random.Random(seed)
    hull = "M-460,-160 L-390,-160 L-380,-96 L360,-96 C390,-96 420,-104 450,-130 C430,-40 360,20 210,36 L-300,36 C-390,24 -440,-50 -460,-160 Z"
    masts = [(-120, -96, -700), (180, -96, -660)]
    sails = []
    for mx, _, top in masts:
        for (y0, y1, w) in [(-150, -320, 320), (-340, -480, 260), (-496, -600, 200)]:
            if y1 < top + 20: continue
            bil = 26
            sails.append(f"M{mx-w/2},{y0+ (y1-y0)} Q{mx},{y1-bil} {mx+w/2},{y1} L{mx+w/2+8},{y0} Q{mx},{y0+bil} {mx-w/2-8},{y0} Z")
    jibs = ["M200,-600 L560,-210 L250,-170 Z", "M190,-480 L470,-180 L230,-150 Z"]
    spanker = "M-130,-150 L-130,-560 L-380,-200 L-370,-150 Z"
    rig = [(-120, -700, -440, -160), (-120, -700, 120, -110), (180, -660, 600, -190), (180, -660, -60, -110), (-120, -560, 180, -560),
           (-120, -680, 180, -640), (450, -130, 620, -240)]
    def strokes(d, col, w, op=1.0, n=2):
        out = ""
        for i in range(n if jitter else 1):
            dx, dy = (r.uniform(-3, 3), r.uniform(-3, 3)) if i else (0, 0)
            out += f'<path d="{d}" stroke="{col}" stroke-width="{w*2.1*(1 if i==0 else 0.6):.1f}" fill="none" opacity="{op*(1 if i==0 else 0.6):.2f}" stroke-linecap="round" stroke-linejoin="round" transform="translate({dx:.1f},{dy:.1f})"/>'
        return out
    s = ""
    if mode == "charcoal":
        c = "#141210"
        s += strokes(hull, c, 9)
        s += strokes("M-380,-60 L400,-60 M-360,-20 L380,-20", c, 4, 0.7)
        for gx in range(-320, 340, 80):
            s += f'<rect x="{gx}" y="-50" width="26" height="22" stroke="{c}" stroke-width="7" fill="none" opacity="0.85"/>'
        for (mx, yb, top) in masts:
            s += strokes(f"M{mx},{yb} L{mx},{top}", c, 9)
        s += strokes("M450,-130 L640,-250", c, 7)
        for d in sails + jibs + [spanker]:
            s += strokes(d, c, 6)
        for (a, b, cc, d) in rig:
            s += strokes(f"M{a},{b} L{cc},{d}", c, 3, 0.8, 1)
        for d in sails:  # sail hatching
            pass
        s += strokes("M180,-660 L180,-720 L250,-700 L180,-690", c, 4)
        # hatching shadows on sails
        for (mx, _, top) in masts:
            for j in range(10):
                yy = -170 - j * 40
                if yy < top + 40: break
                s += f'<path d="M{mx+40},{yy} l70,-26" stroke="{c}" stroke-width="5" opacity="0.55"/>'
        # waves under the hull
        for i in range(9):
            wx = -560 + i * 140
            s += strokes(f"M{wx},70 q35,-40 70,0 q35,40 70,0", c, 6, 0.9)
        return f'<g transform="translate({x},{y}) scale({k})" filter="url(#charcoal)">{s}</g>'
    if mode == "color":
        g = "shp" + str(seed)
        s += (f'<defs><linearGradient id="{g}h" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6b3e1e"/><stop offset="1" stop-color="#2a1608"/></linearGradient>'
              f'<linearGradient id="{g}s" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#e8d6b0"/><stop offset="0.6" stop-color="#fff4da"/><stop offset="1" stop-color="#d9c294"/></linearGradient></defs>')
        s += f'<g filter="url(#softglow)" opacity="0.55"><path d="{hull}" fill="#ffcf70"/>{"".join(f"<path d=\"{d}\" fill=\"#ffe2a0\"/>" for d in sails + jibs + [spanker])}</g>'
        for d in jibs + [spanker]:
            s += f'<path d="{d}" fill="url(#{g}s)" stroke="#8a6a3a" stroke-width="3"/>'
        for (mx, yb, top) in masts:
            s += f'<path d="M{mx},{yb} L{mx},{top}" stroke="#4a2c14" stroke-width="12"/>'
        s += '<path d="M450,-130 L640,-250" stroke="#4a2c14" stroke-width="9"/>'
        for d in sails:
            s += f'<path d="{d}" fill="url(#{g}s)" stroke="#8a6a3a" stroke-width="3"/>'
        for (a, b, cc, d) in rig:
            s += f'<path d="M{a},{b} L{cc},{d}" stroke="#3a2a1a" stroke-width="2.5" opacity="0.9"/>'
        s += '<path d="M180,-660 L180,-720 L260,-700 L180,-688 Z" fill="#b3122e"/>'
        s += f'<path d="{hull}" fill="url(#{g}h)" stroke="#d9a84a" stroke-width="4"/>'
        s += '<path d="M-380,-60 L400,-60" stroke="#d9a84a" stroke-width="5"/><path d="M-370,-20 L380,-20" stroke="#8a5a2a" stroke-width="3"/>'
        for gx in range(-320, 340, 80):
            s += f'<rect x="{gx}" y="-50" width="26" height="22" fill="#ffd27a"/>'
        s += '<rect x="-440" y="-150" width="40" height="40" fill="#ffd27a"/>'
        if water: s += f'<ellipse cx="40" cy="90" rx="720" ry="80" fill="#1f4a72" opacity="0.9" filter="url(#blur2)"/>'
        if water: s += f'<ellipse cx="40" cy="80" rx="600" ry="55" fill="#2c6290" opacity="0.9" filter="url(#blur1)"/>'
        for i in (range(9) if water else []):
            wx = -560 + i * 140
            s += f'<path d="M{wx},50 q35,-38 70,0" stroke="#e6f4ff" stroke-width="8" fill="none" opacity="{0.95 - abs(i-4)*0.15:.2f}" stroke-linecap="round"/>'
        if water: s += '<path d="M-600,100 q120,-20 240,0 q120,20 240,0 q120,-20 240,0 q120,20 240,0" stroke="#7fb0d8" stroke-width="5" fill="none" opacity="0.7"/>'
        return f'<g transform="translate({x},{y}) scale({k})">{s}</g>'
    col = "#05070a" if mode == "silhouette" else "#d9d2c2"
    s += f'<path d="{hull}" fill="{col}"/>'
    for (mx, yb, top) in masts:
        s += f'<path d="M{mx},{yb} L{mx},{top}" stroke="{col}" stroke-width="12"/>'
    for d in sails + jibs + [spanker]:
        s += f'<path d="{d}" fill="{col}"/>'
    s += f'<path d="M450,-130 L640,-250" stroke="{col}" stroke-width="9"/>'
    for (a, b, cc, d) in rig:
        s += f'<path d="M{a},{b} L{cc},{d}" stroke="{col}" stroke-width="3"/>'
    return f'<g transform="translate({x},{y}) scale({k})">{s}</g>'

def charcoal_sea(x0, x1, y0, y1, seed=2, gap=None):
    """Hand-drawn charcoal waves across a wall; gap=(gx0,gx1,gy0) leaves an empty area (where the ship was)."""
    r = random.Random(seed); s = ""; c = "#151311"
    rows = int((y1 - y0) / 70)
    for j in range(rows):
        y = y0 + j * 70 + r.uniform(-8, 8); x = x0 + r.uniform(-40, 0)
        while x < x1:
            w = r.uniform(110, 190)
            if gap and gap[0] < x + w / 2 < gap[1] and y < gap[2]:
                x += w; continue
            s += f'<path d="M{x:.0f},{y:.0f} q{w*0.25:.0f},{-w*0.3:.0f} {w*0.5:.0f},0 q{w*0.12:.0f},{w*0.12:.0f} {w*0.05:.0f},{-w*0.1:.0f} M{x+w*0.5:.0f},{y:.0f} q{w*0.25:.0f},{w*0.25:.0f} {w*0.5:.0f},0" stroke="{c}" stroke-width="{r.uniform(9,14):.1f}" fill="none" stroke-linecap="round" opacity="{r.uniform(0.7,0.95):.2f}"/>'
            x += w
    # horizon line + a few birds + a sun
    s += f'<path d="M{x0},{y0-30} L{x1},{y0-34}" stroke="{c}" stroke-width="10" opacity="0.85"/>'
    for i in range(5):
        bx, by = r.uniform(x0 + 100, x1 - 100), r.uniform(y0 - 420, y0 - 200)
        if gap and gap[0] - 60 < bx < gap[1] + 60: continue
        s += f'<path d="M{bx:.0f},{by:.0f} q30,-26 60,0 q30,-26 60,0" stroke="{c}" stroke-width="9" fill="none"/>'
    return f'<g filter="url(#charcoal)">{s}</g>'

def write(name, content):
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "art", name + ".svg"), "w").write(content)

# ================================================================== FORTRESS / CELL / CHARCOAL
@art
def ulua_storm():
    return S(sky('#05080c', '#1c2a33', mid='#0e171f'),
             clouds(40, 0, 600, 3, '#2a3a46', (0.4, 0.8)), clouds(25, 100, 650, 4, '#04070a', (0.5, 0.9)),
             glow(600, 260, 500, 'white', 0.25),
             '<ellipse cx="1350" cy="760" rx="1300" ry="260" fill="#5a7488" opacity="0.55" filter="url(#blur4)"/>',
             clouds(18, 380, 700, 8, '#8aa2b4', (0.15, 0.35), (200, 500), (20, 50)),
             water(880, 1350, '#0f1d26', '#03070b'), waves(890, 1350, 6, crest='#7f98ab', n=160),
             '<g filter="url(#blur2)" opacity="0.8">' + fortress(1350, 900, 1.05, '#9fb6c9', lit=False, detail=False) + '</g>',
             fortress(1350, 900, 1.05, '#0b1016', lit=True),
             waves(880, 940, 16, crest='#cfe0ee', n=60, amp=1.6),
             '<rect x="0" y="880" width="2400" height="40" fill="#0f1d26" opacity="0.5" filter="url(#blur2)"/>')

@art
def ulua_waves_fg():
    r = random.Random(9); s = ""
    for i in range(5):
        y = 1180 + i * 40; x = -200 + r.uniform(0, 200)
        while x < 2600:
            w = r.uniform(300, 600); h = r.uniform(50, 110)
            s += f'<path d="M{x:.0f},{y+60:.0f} Q{x+w*0.35:.0f},{y-h:.0f} {x+w*0.6:.0f},{y-h*0.4:.0f} Q{x+w*0.75:.0f},{y:.0f} {x+w:.0f},{y+60:.0f} Z" fill="#050b10"/>'
            s += f'<path d="M{x+w*0.2:.0f},{y-h*0.2:.0f} Q{x+w*0.4:.0f},{y-h*1.0:.0f} {x+w*0.6:.0f},{y-h*0.4:.0f}" stroke="#9fb6c9" stroke-width="4" fill="none" opacity="0.4"/>'
            x += w * 0.8
    s += '<rect x="0" y="1260" width="2400" height="90" fill="#03070b"/>'
    return S(s)

@art
def bolt():
    r = random.Random(4); x, y = 760, 0; d = f"M{x},{y}"
    while y < 820:
        x += r.uniform(-60, 60); y += r.uniform(40, 90); d += f" L{x:.0f},{y:.0f}"
    return S(f'<path d="{d}" stroke="#dfe9ff" stroke-width="18" fill="none" filter="url(#blur2)" opacity="0.8"/><path d="{d}" stroke="#ffffff" stroke-width="5" fill="none"/>')

@art
def stairs():
    vx, vy = 1200, 560
    s = '<rect width="2400" height="1350" fill="#0b0a09"/>'
    s += stone_blocks(0, 0, 2400, 1350, 3, base="#3f382f", dark="#211d18", light="#5b5143")
    # vaulted opening/arch receding
    for i, sc in enumerate([1.0, 0.72, 0.52, 0.37, 0.26]):
        w = 1500 * sc; h = 1250 * sc
        s += f'<path d="M{vx-w/2:.0f},{vy+h*0.55:.0f} L{vx-w/2:.0f},{vy-h*0.15:.0f} A{w/2:.0f},{w/2*0.75:.0f} 0 0 1 {vx+w/2:.0f},{vy-h*0.15:.0f} L{vx+w/2:.0f},{vy+h*0.55:.0f}" stroke="#16130f" stroke-width="{40*sc:.0f}" fill="none" opacity="0.9"/>'
    s += f'<path d="M{vx-750},{1350} L{vx-750},{vy-190} A750,560 0 0 1 {vx+750},{vy-190} L{vx+750},1350 Z" fill="#000" opacity="0.35"/>'
    # steps going down toward the vanishing point
    for i in range(16):
        t0 = i / 16; t1 = (i + 1) / 16
        y0 = 1350 - (1350 - vy - 60) * (1 - (1 - t0) ** 1.6); y1 = 1350 - (1350 - vy - 60) * (1 - (1 - t1) ** 1.6)
        w0 = 1500 * (1 - t0 * 0.8); w1 = 1500 * (1 - t1 * 0.8)
        col = ["#4a4237", "#2a251f"][i % 2]
        s += f'<polygon points="{vx-w0/2:.0f},{y0:.0f} {vx+w0/2:.0f},{y0:.0f} {vx+w1/2:.0f},{y1:.0f} {vx-w1/2:.0f},{y1:.0f}" fill="{col}"/>'
        s += f'<line x1="{vx-w0/2:.0f}" y1="{y0:.0f}" x2="{vx+w0/2:.0f}" y2="{y0:.0f}" stroke="#7a6a52" stroke-width="{4*(1-t0)+1:.1f}" opacity="0.6"/>'
    s += f'<polygon points="0,1350 {vx-750},1350 {vx-170},{vy+40} {vx-170},{vy-200} {vx-750},{vy-560} 0,{vy-560}" fill="#000" opacity="0.45"/>'
    s += f'<polygon points="2400,1350 {vx+750},1350 {vx+170},{vy+40} {vx+170},{vy-200} {vx+750},{vy-560} 2400,{vy-560}" fill="#000" opacity="0.55"/>'
    s += f'<line x1="{vx-750}" y1="1350" x2="{vx-170}" y2="{vy+40}" stroke="#7a6a52" stroke-width="6" opacity="0.5"/><line x1="{vx+750}" y1="1350" x2="{vx+170}" y2="{vy+40}" stroke="#7a6a52" stroke-width="6" opacity="0.4"/>'
    s += f'<rect x="{vx-170}" y="{vy-200}" width="340" height="240" fill="#020202"/>'
    s += f'<rect width="2400" height="1350" fill="url(#warmglow)" opacity="0"/>'
    s += glow(vx, 900, 900, 'warm', 0.45)
    s += '<path d="M0,0 L2400,0 L2400,1350 L0,1350 Z" fill="none"/>'
    # wet sheen and chains on the wall
    s += f'<path d="M260,300 q10,80 0,160 q-10,80 0,160" stroke="#6a6458" stroke-width="10" fill="none" stroke-dasharray="20 8"/><circle cx="260" cy="300" r="16" stroke="#6a6458" stroke-width="6" fill="none"/>'
    return S(s)

@art
def jailer_l():
    return S(jailer(1200, 1330, 1150))

@art
def jailer_shock():
    return S(jailer(1200, 1330, 1150, mouth_open=1.0, lantern_up=True))

@art
def jailer_close():
    s = '<rect width="2400" height="1350" fill="#0c0806"/>' + stone_blocks(0, 0, 2400, 1350, 7, base="#3a3027", dark="#1a1510", light="#54473a")
    s += '<rect width="2400" height="1350" fill="#000" opacity="0.45"/>'
    s += glow(1500, 900, 900, 'warm', 0.8)
    s += f'<g transform="translate(1100,560) scale(2.6)">{male_profile("jailer", "#ffd27a", 1.0, "#ffb070")}</g>'
    s += '<path d="M600,1350 C640,1180 800,1110 960,1100 C1060,1090 1160,1110 1240,1180 C1300,1240 1320,1300 1330,1350 Z" fill="#3e352b"/>'
    return S(s)

@art
def cellgate():
    s = '<rect width="2400" height="1350" fill="#0a0908"/>' + stone_blocks(0, 0, 2400, 1350, 5, base="#40392f", dark="#1d1915", light="#5c5244")
    s += '<path d="M700,1350 L700,420 A500,330 0 0 1 1700,420 L1700,1350 Z" fill="#000"/>'
    s += '<path d="M700,1350 L700,420 A500,330 0 0 1 1700,420 L1700,1350" stroke="#1a1612" stroke-width="40" fill="none"/>'
    # iron bars
    for i in range(11):
        x = 760 + i * 88
        s += f'<rect x="{x}" y="160" width="20" height="1190" fill="#1b1b1d"/><rect x="{x+3}" y="160" width="5" height="1190" fill="#6a6e74" opacity="0.6"/>'
    for y in (420, 760, 1100):
        s += f'<rect x="720" y="{y}" width="960" height="26" fill="#1b1b1d"/><rect x="720" y="{y+3}" width="960" height="5" fill="#7a7e84" opacity="0.5"/>'
    # padlock and hasp
    s += '<rect x="1210" y="740" width="90" height="110" rx="10" fill="#2a2620"/><path d="M1225,742 L1225,700 A30,30 0 0 1 1285,700 L1285,742" stroke="#3a352c" stroke-width="16" fill="none"/>'
    s += '<rect x="1218" y="750" width="74" height="10" fill="#8a7a5a" opacity="0.6"/><circle cx="1255" cy="800" r="9" fill="#050505"/>'
    s += glow(300, 700, 800, 'warm', 0.55)
    s += '<rect width="2400" height="1350" fill="#000" opacity="0.15"/>'
    return S(s)

@art
def wall_base():
    """Lime-plastered coral-stone cell wall: smooth enough for charcoal to read, with stains, cracks and bare patches."""
    r = random.Random(12)
    s = '<rect width="2400" height="1350" fill="#8b8070"/>'
    s += '<rect width="2400" height="1350" fill="#000" filter="url(#stone)" opacity="0.8"/>'
    # faint block outlines showing through the plaster
    y = 0
    while y < 1350:
        h = r.uniform(150, 230); x = -r.uniform(0, 200)
        while x < 2400:
            w = r.uniform(280, 520)
            s += f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" rx="18" fill="none" stroke="#5d5446" stroke-width="5" opacity="0.35"/>'
            x += w
        y += h
    # bare stone patches where plaster fell (irregular)
    for j, (px, py, w, h) in enumerate([(80, 80, 380, 240), (1950, 60, 420, 300), (2050, 1050, 340, 260), (60, 1080, 300, 230)]):
        cx_, cy_ = px + w / 2, py + h / 2; pts = []
        for a in range(0, 360, 20):
            rr_ = r.uniform(0.6, 1.0)
            pts.append(f"{cx_ + math.cos(math.radians(a))*w/2*rr_:.0f},{cy_ + math.sin(math.radians(a))*h/2*rr_:.0f}")
        cid = f"patch{j}"
        s += f'<defs><clipPath id="{cid}"><polygon points="{" ".join(pts)}"/></clipPath></defs>'
        s += f'<g clip-path="url(#{cid})" opacity="0.8">{stone_blocks(px, py, px+w, py+h, int(px), base="#6d6353", dark="#463e32", light="#8a7f6c", bh=(50,80), bw=(80,150), mortar="#3a332a")}</g>'
        s += f'<polygon points="{" ".join(pts)}" fill="none" stroke="#a89c86" stroke-width="8" opacity="0.45"/>'
    s += '<g filter="url(#blur3)">' + "".join(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="#3a3328" opacity="0.4"/>' for x, y, rx, ry in [(300, 1250, 500, 200), (2100, 150, 350, 160), (1900, 1300, 600, 160), (1200, 0, 700, 90)]) + '</g>'
    for i in range(14):  # water streaks
        x = r.uniform(0, 2400)
        s += f'<path d="M{x:.0f},0 q{r.uniform(-20,20):.0f},{r.uniform(200,500):.0f} {r.uniform(-10,10):.0f},{r.uniform(300,800):.0f}" stroke="#4e4538" stroke-width="{r.uniform(10,30):.0f}" fill="none" opacity="0.25" filter="url(#blur2)"/>'
    s += '<path d="M1600,0 L1580,120 L1620,200 L1590,330 L1610,400" stroke="#2a251e" stroke-width="5" fill="none"/><path d="M420,1350 L460,1220 L430,1120 L470,1010" stroke="#2a251e" stroke-width="5" fill="none"/>'
    return S(s)

@art
def wall_sea():
    return S(charcoal_sea(120, 2280, 900, 1300, 2))

@art
def wall_sea_gap():
    return S(charcoal_sea(120, 2280, 900, 1300, 2, gap=(560, 1840, 1060)),
             f'<g filter="url(#blur3)" opacity="0.55">{ship(1200, 960, 1.22, "silhouette").replace("#05070a", "#1a120a")}</g>',
             f'<g filter="url(#blur1)" opacity="0.6">{ship(1200, 960, 1.18, "ghost").replace("#d9d2c2", "#f4ecd8")}</g>')

@art
def wall_drawings():
    c = "#151311"; s = ""
    # flowers (left), birds, Orizaba with snow (right), a little hummingbird
    for (fx_, fy, k) in [(330, 520, 1.0), (520, 640, 0.8), (240, 760, 0.7)]:
        s += f'<path d="M{fx_},{fy} q-10,160 10,300" stroke="{c}" stroke-width="5" fill="none"/>'
        for a in range(0, 360, 45):
            ax, ay = fx_ + math.cos(math.radians(a)) * 46 * k, fy + math.sin(math.radians(a)) * 46 * k
            s += f'<ellipse cx="{ax:.0f}" cy="{ay:.0f}" rx="{30*k:.0f}" ry="{14*k:.0f}" transform="rotate({a} {ax:.0f} {ay:.0f})" stroke="{c}" stroke-width="4" fill="none"/>'
        s += f'<circle cx="{fx_}" cy="{fy}" r="{14*k:.0f}" fill="{c}"/>'
        s += f'<path d="M{fx_},{fy+150} q-60,-40 -90,-10 q40,30 90,10 M{fx_+4},{fy+200} q60,-40 90,-10 q-40,30 -90,10" stroke="{c}" stroke-width="4" fill="none"/>'
    s += f'<path d="M1500,700 L1800,300 L1830,290 L2150,700" stroke="{c}" stroke-width="7" fill="none"/>'
    s += f'<path d="M1690,440 L1740,470 L1780,430 L1830,480 L1880,440 L1930,470" stroke="{c}" stroke-width="5" fill="none"/>'
    for i in range(12):
        s += f'<path d="M{1560+i*45},{700-i*8} l40,-30" stroke="{c}" stroke-width="3" opacity="0.6"/>'
    for (bx, by) in [(900, 300), (1010, 260), (1100, 330), (980, 380)]:
        s += f'<path d="M{bx},{by} q25,-22 50,0 q25,-22 50,0" stroke="{c}" stroke-width="5" fill="none"/>'
    s += f'<path d="M1200,560 q40,-30 80,-10 l60,-20 l-50,40 q-30,40 -90,30 z M1240,550 l-30,-50 l40,40" stroke="{c}" stroke-width="4" fill="none"/>'
    s = s.replace('stroke-width="4"', 'stroke-width="9"').replace('stroke-width="5"', 'stroke-width="11"').replace('stroke-width="7"', 'stroke-width="14"').replace('stroke-width="3"', 'stroke-width="6"')
    return S(f'<g filter="url(#charcoal)">{s}</g>')

@art
def ship_charcoal():
    return S(ship(1200, 960, 1.18, "charcoal"))

@art
def ship_color():
    return S(ship(1200, 960, 1.18, "color"))

@art
def ship_glow():
    return S(f'<g filter="url(#blur4)">{ship(1200, 960, 1.18, "silhouette").replace("#05070a", "#ffc860")}</g>', glow(1210, 700, 900, 'warm', 0.7))

@art
def window_beam():
    return S('<path d="M1880,60 L2060,60 L1700,1350 L1250,1350 Z" fill="url(#beamcold)" filter="url(#blur3)"/>',
             '<rect x="1860" y="40" width="220" height="150" fill="#cfe0ff" opacity="0.6"/>' + "".join(f'<rect x="{1880+i*48}" y="40" width="12" height="150" fill="#111"/>' for i in range(5)))



# ================================================================== CÓRDOBA
def lit_church(x, yb, k=1.0, wall="#e9d9b8", side="#b49a74", trim="#c98e4a", dark="#3a2a1e", two_towers=True):
    s = ""
    def R(px, py, w, h, c): return f'<rect x="{x+px*k:.0f}" y="{yb+py*k:.0f}" width="{w*k:.0f}" height="{h*k:.0f}" fill="{c}"/>'
    # nave + dome behind
    s += f'<ellipse cx="{x+260*k:.0f}" cy="{yb-560*k:.0f}" rx="{120*k:.0f}" ry="{110*k:.0f}" fill="{side}"/>'
    s += R(250, -720, 20, 60, side) + R(234, -700, 52, 10, side)
    s += f'<path d="M{x+140*k:.0f},{yb-560*k:.0f} A{120*k:.0f},{110*k:.0f} 0 0 1 {x+380*k:.0f},{yb-560*k:.0f}" fill="#e8c88a" opacity="0.5"/>'
    s += R(-200, -520, 400, 520, wall)
    s += f'<path d="M{x-210*k:.0f},{yb-520*k:.0f} Q{x:.0f},{yb-700*k:.0f} {x+210*k:.0f},{yb-520*k:.0f} Z" fill="{wall}"/>'
    s += f'<path d="M{x-210*k:.0f},{yb-520*k:.0f} Q{x:.0f},{yb-700*k:.0f} {x+210*k:.0f},{yb-520*k:.0f}" stroke="{trim}" stroke-width="{10*k:.0f}" fill="none"/>'
    # baroque portal
    s += R(-110, -420, 220, 420, "#d8c29a") + R(-120, -430, 240, 14, trim)
    for px in (-100, 70):
        s += R(px, -410, 30, 410, "#c4a678")
    s += f'<path d="M{x-60*k:.0f},{yb:.0f} L{x-60*k:.0f},{yb-230*k:.0f} A{60*k:.0f},{60*k:.0f} 0 0 1 {x+60*k:.0f},{yb-230*k:.0f} L{x+60*k:.0f},{yb:.0f} Z" fill="{dark}"/>'
    s += f'<circle cx="{x:.0f}" cy="{yb-350*k:.0f}" r="{36*k:.0f}" fill="{dark}"/><circle cx="{x:.0f}" cy="{yb-350*k:.0f}" r="{36*k:.0f}" fill="none" stroke="{trim}" stroke-width="{6*k:.0f}"/>'
    s += R(-4, -660, 8, 70, dark) + R(-24, -640, 48, 8, dark)
    towers = (-1, 1) if two_towers else (1,)
    for sd in towers:
        tx = sd * 290
        s += R(tx - 90, -760, 180, 760, wall)
        s += R(tx - 90 + (90 if sd < 0 else 0), -760, 90, 760, side) if sd > 0 else R(tx - 90, -760, 40, 760, side)
        for lvl, (yy, ww) in enumerate([(-760, 180), (-900, 150), (-1010, 120)]):
            s += R(tx - ww / 2, yy - (140 if lvl < 2 else 100), ww, 140 if lvl < 2 else 100, wall)
            s += R(tx - ww / 2 - 8, yy - 10, ww + 16, 14, trim)
            if lvl < 2:
                s += f'<path d="M{x+(tx-28)*k:.0f},{yb+(yy-20)*k:.0f} L{x+(tx-28)*k:.0f},{yb+(yy-90)*k:.0f} A{28*k:.0f},{28*k:.0f} 0 0 1 {x+(tx+28)*k:.0f},{yb+(yy-90)*k:.0f} L{x+(tx+28)*k:.0f},{yb+(yy-20)*k:.0f} Z" fill="{dark}"/>'
                s += f'<circle cx="{x+tx*k:.0f}" cy="{yb+(yy-70)*k:.0f}" r="{16*k:.0f}" fill="#b08a3a"/>'
        s += f'<path d="M{x+(tx-60)*k:.0f},{yb-1110*k:.0f} Q{x+tx*k:.0f},{yb-1220*k:.0f} {x+(tx+60)*k:.0f},{yb-1110*k:.0f} Z" fill="{trim}"/>'
        s += R(tx - 4, -1290, 8, 90, dark) + R(tx - 20, -1260, 40, 8, dark)
    return s

def portales(x0, x1, yb, h=420, wall="#e2cfa6", shade="#8a6f4e", col="#d6bf92", n=None, upper=True, dark="#2a1d14"):
    """Two-storey arcade (portales) facing the viewer."""
    s = f'<rect x="{x0}" y="{yb-h-(260 if upper else 0)}" width="{x1-x0}" height="{h+(260 if upper else 0)}" fill="{wall}"/>'
    n = n or int((x1 - x0) / 170)
    aw = (x1 - x0) / n
    for i in range(n):
        ax = x0 + i * aw
        s += f'<path d="M{ax+18:.0f},{yb} L{ax+18:.0f},{yb-h*0.62:.0f} A{aw/2-18:.0f},{aw/2-18:.0f} 0 0 1 {ax+aw-18:.0f},{yb-h*0.62:.0f} L{ax+aw-18:.0f},{yb} Z" fill="{shade}"/>'
        s += f'<path d="M{ax+18:.0f},{yb} L{ax+18:.0f},{yb-h*0.62:.0f} A{aw/2-18:.0f},{aw/2-18:.0f} 0 0 1 {ax+aw-18:.0f},{yb-h*0.62:.0f}" stroke="{dark}" stroke-width="3" fill="none" opacity="0.4"/>'
        s += f'<rect x="{ax+aw*0.3:.0f}" y="{yb-h*0.5:.0f}" width="{aw*0.4:.0f}" height="{h*0.5:.0f}" fill="{dark}" opacity="0.55"/>'
        if upper:
            s += f'<rect x="{ax+aw*0.3:.0f}" y="{yb-h-200:.0f}" width="{aw*0.4:.0f}" height="150" fill="{dark}" opacity="0.8"/>'
            s += f'<rect x="{ax+aw*0.22:.0f}" y="{yb-h-56:.0f}" width="{aw*0.56:.0f}" height="8" fill="{dark}"/>'
            s += "".join(f'<rect x="{ax+aw*0.24+j*aw*0.07:.0f}" y="{yb-h-92:.0f}" width="3" height="40" fill="{dark}"/>' for j in range(8))
    s += f'<rect x="{x0-10}" y="{yb-h-(270 if upper else 10)}" width="{x1-x0+20}" height="22" fill="{col}"/>'
    s += f'<rect x="{x0}" y="{yb-h+2}" width="{x1-x0}" height="14" fill="{col}"/>'
    # tile roof edge
    s += f'<rect x="{x0-20}" y="{yb-h-(300 if upper else 40)}" width="{x1-x0+40}" height="34" fill="#9a4a2a"/>'
    s += "".join(f'<path d="M{x0-20+j*24},{yb-h-(300 if upper else 40)+34} q12,10 24,0" stroke="#6a2e1a" stroke-width="5" fill="none"/>' for j in range(int((x1-x0+40)/24)))
    return s

def hills(y, amp, color, seed, step=60):
    return ridge(y, amp, color, seed, rough=0.5, step=step)

@art
def cordoba_plaza():
    s = sky('#7fb2d6', '#f2d7a8', mid='#bcd2d6')
    s += clouds(14, 80, 380, 21, '#ffffff', (0.4, 0.8), (140, 320), (30, 70), 'blur2')
    s += volcano(1850, 860, 1300, 640, '#6d86a3', '#ffffff', '#b9c8dc')
    s += hills(900, 160, '#4f7a5a', 31) + hills(960, 110, '#3d6648', 33)
    s += lit_church(1050, 1080, 0.62)
    s += portales(1500, 2400, 1080, 300)
    s += portales(-20, 640, 1080, 300)
    s += palm(780, 1120, 640, -0.08, 3, '#203a26', '#2a5034')
    s += palm(1420, 1120, 560, 0.1, 4, '#203a26', '#2a5034')
    s += '<rect x="0" y="1080" width="2400" height="270" fill="#bfa47a"/>'
    s += cobbles(1090, color='#a98e66', wet=False).replace('#1d2630', '#8e7552')
    # fountain
    s += '<ellipse cx="1180" cy="1230" rx="220" ry="40" fill="#8e7552"/><rect x="1150" y="1120" width="60" height="110" fill="#d6c3a0"/><ellipse cx="1180" cy="1120" rx="90" ry="20" fill="#cbb48e"/>'
    s += villager(400, 1260, 230, 'woman', '#2a1f18') + villager(470, 1265, 260, 'man', '#2a1f18') + villager(1650, 1240, 240, 'woman', '#2a1f18', facing=-1) + villager(1980, 1280, 260, 'man', '#2a1f18')
    return S(s)

@art
def cane_fields():
    s = sky('#3a4a78', '#f0a050', mid='#c27a6a')
    s += glow(700, 900, 700, 'warm', 0.8)
    s += volcano(1700, 900, 1400, 640, '#5a5a7a', '#ffd8c0', '#c9a0a8')
    s += hills(930, 140, '#3a3a40', 41) + hills(990, 90, '#2a2a2c', 43)
    # trapiche (sugar mill) with chimney + smoke
    s += '<rect x="300" y="760" width="260" height="200" fill="#1e1a18"/><path d="M280,760 L580,760 L520,700 L340,700 Z" fill="#2a2220"/><rect x="480" y="520" width="50" height="240" fill="#1e1a18"/>'
    s += '<g filter="url(#blur2)">' + "".join(f'<circle cx="{505+i*28+(i%2)*10}" cy="{500-i*55}" r="{30+i*12}" fill="#9a8a8a" opacity="{0.5-i*0.05:.2f}"/>' for i in range(8)) + '</g>'
    s += '<rect x="0" y="980" width="2400" height="370" fill="#26301a"/>'
    for i, (yy, h_, c_) in enumerate([(1060, 300, '#2f3d1c'), (1170, 360, '#22301a'), (1350, 460, '#121a0c')]):
        s += cane(-50, 2450, yy, h_, 50 + i, c_, 260 + i * 60, hi='#c9b060' if i < 2 else None)
    for (wx, wy, sz, f) in [(980, 1080, 210, 1), (1200, 1100, 230, -1), (1500, 1070, 200, 1)]:
        s += villager(wx, wy, sz, 'man', '#120e08', facing=f)
        s += f'<path d="M{wx+f*30},{wy-sz*0.5:.0f} l{f*60},{-40}" stroke="#120e08" stroke-width="6"/>'
    return S(s)

@art
def orizaba():
    s = sky('#203a62', '#f6c89a', mid='#8aa6c4') + stars(40, 7, 300, '#ffffff')
    s += volcano(1250, 1000, 2000, 860, '#4a5f86', '#fbfbff', '#aab8d4', seed=9)
    s += '<path d="M1255,140 L1280,141 L1430,226 L1750,640 L2250,1000 L1300,1000 Z" fill="#1e2c48" opacity="0.45"/>'
    r = random.Random(14)
    for i in range(16):
        x0 = 1250 + r.uniform(-260, 260); x1 = 1250 + (x0 - 1250) * 3.2
        s += f'<path d="M{x0:.0f},{300+r.uniform(0,120):.0f} Q{(x0+x1)/2+r.uniform(-40,40):.0f},{620:.0f} {x1:.0f},{1000}" stroke="#2a3a5c" stroke-width="{r.uniform(4,10):.0f}" fill="none" opacity="0.45"/>'
    s += hills(1010, 220, '#2a3a58', 15) + hills(1080, 160, '#1e2a40', 16)
    s += '<path d="M1230,140 L1280,141 L1430,300 L1300,260 Z" fill="#ffe0c0" opacity="0.5"/>'
    return S(s)

@art
def orizaba_clouds():
    return S(clouds(70, 880, 1250, 61, '#f4e2d4', (0.6, 0.95), (220, 520), (50, 120), 'blur3'),
             clouds(40, 1000, 1350, 62, '#ffffff', (0.7, 1.0), (240, 520), (60, 130), 'blur2'))

@art
def yanga():
    s = sky('#1a2240', '#c86a4a', mid='#5a4a6a')
    s += hills(620, 260, '#3a4a5a', 71) + hills(760, 220, '#2a3644', 72) + hills(880, 160, '#1c2630', 73)
    s += '<g filter="url(#blur3)"><rect x="0" y="700" width="2400" height="140" fill="#c8b0a8" opacity="0.35"/></g>'
    # palenque huts on the slope
    for (hx, hy, k) in [(700, 930, 1.0), (880, 950, 0.9), (1040, 925, 1.1), (560, 960, 0.8), (1200, 960, 0.85)]:
        s += f'<rect x="{hx-60*k:.0f}" y="{hy-70*k:.0f}" width="{120*k:.0f}" height="{70*k:.0f}" fill="#120c0a"/><path d="M{hx-90*k:.0f},{hy-66*k:.0f} L{hx:.0f},{hy-170*k:.0f} L{hx+90*k:.0f},{hy-66*k:.0f} Z" fill="#1a120c"/>'
        s += f'<rect x="{hx-12*k:.0f}" y="{hy-50*k:.0f}" width="{24*k:.0f}" height="{50*k:.0f}" fill="#ffb060" opacity="0.8"/>'
    for (fx_, fy) in [(800, 990), (1120, 985)]:
        s += glow(fx_, fy - 30, 160, 'warm', 0.9) + f'<path d="M{fx_-20},{fy} Q{fx_},{fy-80} {fx_+20},{fy} Z" fill="#ffcf60"/>'
        s += f'<g filter="url(#blur2)"><circle cx="{fx_+10}" cy="{fy-160}" r="40" fill="#8a7a80" opacity="0.4"/><circle cx="{fx_+30}" cy="{fy-260}" r="60" fill="#8a7a80" opacity="0.3"/></g>'
    s += '<path d="M0,1100 C400,1000 900,1040 1300,1080 C1700,1110 2100,1060 2400,1000 L2400,1350 L0,1350 Z" fill="#07090b"/>'
    # people standing on the ridge, looking at the horizon
    for (vx, vy, sz, kind, f) in [(1550, 1080, 380, 'man', 1), (1680, 1074, 340, 'woman', 1), (1790, 1070, 300, 'child', 1), (1460, 1084, 360, 'man', -1), (1900, 1066, 350, 'man', 1)]:
        s += villager(vx, vy, sz, kind, '#07090b', rim='#ff9a5a', facing=f)
    s += tree(300, 1150, 600, 23, '#07090b', 'ahuehuete')
    return S(s)

@art
def house_night():
    s = sky('#060b16', '#1f3448', mid='#0e1a2a') + stars(200, 81, 700) + moon(1900, 230, 80)
    s += hills(860, 120, '#0c1620', 82)
    s += palm(1600, 1000, 700, 0.12, 83, '#05080a', '#08100c') + palm(2100, 980, 620, -0.1, 84, '#05080a', '#08100c')
    # adobe house with tile roof and porch
    s += '<rect x="560" y="640" width="900" height="420" fill="#4a3a2e"/>'
    s += '<rect x="560" y="640" width="900" height="420" fill="#000" filter="url(#stone)" opacity="0.6"/>'
    s += '<path d="M500,660 L1520,660 L1460,560 L560,560 Z" fill="#5a2a1a"/>' + "".join(f'<path d="M{510+j*30},660 l60,-100" stroke="#3a1a10" stroke-width="5"/>' for j in range(34))
    s += '<path d="M480,700 L1540,700 L1540,690 L480,690 Z" fill="#2a1a10"/>'
    for px in (520, 900, 1500):
        s += f'<rect x="{px}" y="700" width="22" height="380" fill="#2a1a10"/>'
    s += '<path d="M480,700 L1540,700 L1580,760 L440,760 Z" fill="#6a3424"/>'
    # door open with warm light + window
    s += glow(760, 900, 420, 'warm', 0.9) + '<rect x="700" y="820" width="130" height="240" fill="#ffc870"/><rect x="700" y="820" width="40" height="240" fill="#7a4a24"/>'
    s += glow(1200, 880, 300, 'warm', 0.7) + '<rect x="1130" y="830" width="140" height="110" fill="#ffd27a"/><rect x="1196" y="830" width="8" height="110" fill="#2a1a10"/><rect x="1130" y="880" width="140" height="8" fill="#2a1a10"/>'
    # drying herbs hanging from the porch beam
    r = random.Random(85)
    for i in range(16):
        hx = 600 + i * 55 + r.uniform(-10, 10)
        s += f'<path d="M{hx:.0f},760 l0,{r.uniform(20,40):.0f}" stroke="#1a1208" stroke-width="2"/>'
        s += herb_bundle(hx, 830, 0.35, 180 + r.uniform(-10, 10), seed=i).replace('#5f8a3a', '#2e4a22').replace('#7aa04a', '#3a5a2a').replace('#4f7a32', '#28401c')
    # clay pots with plants
    for (px, py) in [(470, 1080), (1580, 1090), (1680, 1100)]:
        s += f'<path d="M{px-50},{py-90} L{px+50},{py-90} L{px+36},{py} L{px-36},{py} Z" fill="#6a3020"/>' + banana(px, py - 90, 260, px, '#0e1a10')
    s += '<rect x="0" y="1060" width="2400" height="290" fill="#0a0d0a"/>'
    s += '<path d="M700,1060 L830,1060 L1000,1350 L560,1350 Z" fill="#ffb860" opacity="0.18"/>'
    return S(s)

@art
def plants_fg():
    s = banana(150, 1450, 1100, 91, '#020403') + banana(2300, 1500, 1200, 92, '#020403')
    s += banana(380, 1480, 700, 93, '#030604') + banana(2050, 1450, 650, 94, '#030604')
    r = random.Random(95)
    for _ in range(40):
        x = r.choice([r.uniform(0, 600), r.uniform(1800, 2400)]); L = r.uniform(150, 380); a = r.uniform(-140, -40)
        ex, ey = x + math.cos(math.radians(a)) * L, 1350 + math.sin(math.radians(a)) * L
        s += f'<path d="M{x:.0f},1350 Q{(x+ex)/2+r.uniform(-60,60):.0f},{(1350+ey)/2-40:.0f} {ex:.0f},{ey:.0f}" stroke="#020403" stroke-width="{r.uniform(6,14):.0f}" fill="none" stroke-linecap="round"/>'
    return S(s)

@art
def herbs_table():
    s = '<rect width="2400" height="1350" fill="#1a110b"/>'
    s += '<rect width="2400" height="900" fill="#3a2618" filter="url(#stone)"/><rect width="2400" height="900" fill="#2a1a10" opacity="0.6"/>'
    s += glow(1300, 700, 1100, 'warm', 0.75)
    # hanging herbs from a beam
    s += '<rect x="0" y="40" width="2400" height="40" fill="#1a0f08"/>'
    r = random.Random(101)
    for i in range(12):
        hx = 150 + i * 190 + r.uniform(-30, 30)
        s += f'<path d="M{hx:.0f},80 l0,{60:.0f}" stroke="#1a1208" stroke-width="3"/>' + herb_bundle(hx, 230, 0.95, 180 + r.uniform(-8, 8), seed=100 + i)
    # table
    s += '<path d="M0,1000 L2400,960 L2400,1350 L0,1350 Z" fill="#5a3a20"/>' + "".join(f'<path d="M0,{1040+j*60} L2400,{1000+j*60}" stroke="#3a2412" stroke-width="4" opacity="0.6"/>' for j in range(6))
    # molcajete (stone mortar) with pestle
    s += '<ellipse cx="800" cy="1010" rx="220" ry="60" fill="#2a2622"/><path d="M580,1010 C590,1130 700,1170 800,1170 C900,1170 1010,1130 1020,1010 Z" fill="#3a3530"/>'
    s += '<path d="M640,1160 l-20,50 M960,1160 l20,50 M800,1170 l0,50" stroke="#2a2622" stroke-width="30" stroke-linecap="round"/>'
    s += '<ellipse cx="800" cy="1010" rx="180" ry="44" fill="#2a2420"/>' + "".join(f'<ellipse cx="{700+i*24+(i%3)*6}" cy="{1000+(i%2)*14}" rx="16" ry="7" fill="{["#4a6a2a","#3e5a24","#6a8a3a"][i%3]}" transform="rotate({i*37} {700+i*24} {1000+(i%2)*14})"/>' for i in range(9))
    s += '<rect x="820" y="880" width="46" height="170" rx="20" fill="#4a4540" transform="rotate(25 840 960)"/>'
    # copal burner (sahumerio) + smoke source
    s += '<path d="M1450,1000 C1450,940 1650,940 1650,1000 L1610,1070 L1490,1070 Z" fill="#8a4a2a"/><rect x="1530" y="1070" width="40" height="70" fill="#7a3a20"/><ellipse cx="1550" cy="1140" rx="80" ry="18" fill="#6a321c"/>'
    s += glow(1550, 960, 140, 'red', 0.6) + '<ellipse cx="1550" cy="960" rx="80" ry="16" fill="#ff7a30" opacity="0.8"/>'
    # candle + jars
    s += candle(1950, 1000, 160, 40)
    for (jx, c) in [(2150, '#3a5a6a'), (2280, '#6a5a2a'), (300, '#5a3a5a')]:
        s += f'<rect x="{jx-50}" y="860" width="100" height="160" rx="20" fill="{c}" opacity="0.85"/><rect x="{jx-40}" y="845" width="80" height="20" fill="#2a1a10"/>'
    s += '<g opacity="0.9">' + "".join(f'<ellipse cx="{1150+i*40}" cy="{1060+(i%2)*10}" rx="26" ry="10" fill="{c}" transform="rotate({i*30} {1150+i*40} {1060+(i%2)*10})"/>' for i, c in enumerate(["#5f8a3a", "#e0c040", "#4f7a32", "#b3122e", "#7aa04a"])) + '</g>'
    return S(s)

@art
def copal_smoke():
    r = random.Random(103); s = '<g filter="url(#blur3)">'
    for i in range(18):
        y = 940 - i * 50; x = 1550 + math.sin(i * 0.7) * 40 * (1 + i * 0.15)
        s += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{40+i*9}" ry="{30+i*5}" fill="#e8e0d8" opacity="{0.42-i*0.02:.2f}"/>'
    return S(s + '</g>')

@art
def sickroom():
    s = '<rect width="2400" height="1350" fill="#2a1c14"/><rect width="2400" height="1350" fill="#000" filter="url(#stone)" opacity="0.7"/>'
    s += glow(1500, 600, 1000, 'warm', 0.7)
    s += '<rect x="1900" y="200" width="260" height="360" fill="#0a1020"/>' + "".join(f'<rect x="{1900+j*65}" y="200" width="10" height="360" fill="#2a1a10"/>' for j in range(5))
    s += moon(2060, 300, 40)
    s += '<rect x="0" y="1060" width="2400" height="290" fill="#1a110a"/>'
    # bed with child
    s += '<rect x="700" y="880" width="1100" height="200" rx="20" fill="#4a3020"/><rect x="680" y="760" width="40" height="320" fill="#3a2414"/>'
    s += '<path d="M730,880 C900,820 1500,820 1790,880 L1790,960 L730,960 Z" fill="#c9b8a0"/>'
    s += '<path d="M900,880 C1000,800 1500,800 1780,860 L1790,960 L900,960 Z" fill="#8a3a2a"/>' + "".join(f'<path d="M{950+j*90},850 l40,100" stroke="#e2a11b" stroke-width="6" opacity="0.6"/>' for j in range(9))
    s += '<ellipse cx="820" cy="850" rx="90" ry="40" fill="#e8dcc8"/>'
    s += f'<g transform="translate(850,815) rotate(-75) scale(0.3)">{head(look=0, smile=0, lids=0, rim=None, eyes_closed=True, earring=False, back_curls=False, wrap="#2a1a10", wrap_hi="#3a2a1a", wrap_dk="#1a0f08")}</g>'
    # mother kneeling at the foot of the bed (silhouette)
    s += '<path d="M1880,1080 C1880,980 1900,900 1950,860 C1930,820 1940,770 1990,760 C2040,760 2060,810 2040,850 C2100,880 2130,980 2130,1080 Z" fill="#0d0907"/>'
    s += mulata_full(560, 1080, 900, look=0.4, rim='#ffd27a', props='herbs', turn=0.3)
    return S(s)

@art
def door_queue():
    s = sky('#2a3a5a', '#f2b07a', mid='#b07a7a') + glow(1900, 1000, 700, 'warm', 0.8)
    s += hills(900, 120, '#2a2a34', 111)
    s += '<rect x="80" y="560" width="760" height="520" fill="#3a2e24"/><path d="M40,580 L880,580 L820,480 L100,480 Z" fill="#4a2418"/>'
    s += '<rect x="360" y="800" width="140" height="280" fill="#ffc870"/>' + glow(430, 940, 300, 'warm', 0.8)
    s += banana(900, 1080, 500, 112, '#14100c') + palm(2200, 1080, 600, -0.1, 113, '#100c0a', '#14100c')
    s += '<rect x="0" y="1070" width="2400" height="280" fill="#1a1410"/>'
    q = [(620, 'woman', 330), (760, 'child', 200), (900, 'man', 360), (1060, 'woman', 320), (1200, 'man', 350), (1340, 'woman', 300), (1460, 'man', 370), (1600, 'woman', 310), (1720, 'child', 190), (1830, 'man', 340)]
    for i, (qx, kind, h_) in enumerate(q):
        s += villager(qx, 1110 + (i % 3) * 8, h_, kind, '#0c0a08', rim='#ffb070', facing=-1)
    return S(s)

@art
def bust_bg():
    s = '<rect width="2400" height="1350" fill="#140c08"/>' + glow(1700, 600, 1100, 'warm', 0.55) + glow(500, 300, 700, 'moon', 0.4)
    r = random.Random(121)
    s += '<g filter="url(#blur3)">' + "".join(f'<circle cx="{r.uniform(1300,2400):.0f}" cy="{r.uniform(100,1300):.0f}" r="{r.uniform(30,90):.0f}" fill="#ffb860" opacity="{r.uniform(0.15,0.4):.2f}"/>' for _ in range(16)) + '</g>'
    s += banana(2300, 1500, 900, 122, '#0a0706') + banana(100, 1500, 800, 123, '#0a0706')
    return S(s)

@art
def bust_l():
    return S(mulata_bust(1200, 560, 1.75, look=0.15, smile=0.55))

@art
def bust_herbs():
    return S(mulata_bust(1150, 520, 1.6, look=-0.25, smile=0.45, herbs=True))

@art
def bust_closed():
    return S(mulata_bust(1200, 560, 1.75, look=0, smile=0.3, eyes_closed=True))

@art
def street_night():
    s = sky('#050a14', '#1a2a3a', mid='#0c1626') + stars(120, 131, 500) + moon(1250, 200, 70)
    s += facade(-40, 1100, 700, 600, '#0a0f15', 3, 0.5) + facade(1650, 1100, 800, 640, '#0a0f15', 5, 0.4)
    s += church(1180, 1000, 0.75, '#070b10')
    s += lamp(700, 1150) + lamp(1700, 1150)
    s += cobbles(1100)
    return S(s)

@art
def objects():
    s = '<rect width="2400" height="1350" fill="#140c08"/>' + glow(1200, 700, 1000, 'warm', 0.7)
    s += '<path d="M0,820 L2400,780 L2400,1350 L0,1350 Z" fill="#4a3018"/>' + "".join(f'<path d="M0,{860+j*80} L2400,{820+j*80}" stroke="#2a1a0c" stroke-width="4" opacity="0.6"/>' for j in range(7))
    # folded letter with wax seal
    s += '<path d="M700,900 L1180,860 L1220,1100 L740,1150 Z" fill="#e8dcc0"/><path d="M700,900 L960,1010 L1180,860" stroke="#b8a888" stroke-width="5" fill="none"/>'
    s += '<circle cx="960" cy="1010" r="40" fill="#8a1a1a"/><circle cx="960" cy="1010" r="26" fill="#a82424"/>'
    s += "".join(f'<path d="M{760+j*6},{960+j*30} l{300-j*20},-25" stroke="#4a3a2a" stroke-width="3" opacity="0.5"/>' for j in range(5))
    # gold ring
    s += '<ellipse cx="1500" cy="1020" rx="70" ry="28" fill="none" stroke="#e5b54e" stroke-width="16"/><ellipse cx="1500" cy="1012" rx="70" ry="28" fill="none" stroke="#ffe6a0" stroke-width="4" opacity="0.7"/><circle cx="1500" cy="986" r="16" fill="#b3122e"/>'
    s += candle(1850, 900, 200, 46) + herb_bundle(450, 980, 1.1, -70)
    return S(s)


# ================================================================== ALCALDE / RUMOURS / INQUISITION
@art
def alcalde_door():
    s = sky('#2a2a4a', '#e09a6a', mid='#9a6a7a') + glow(300, 900, 600, 'warm', 0.6)
    s += '<rect x="900" y="300" width="1500" height="800" fill="#4a3a2e"/><rect x="900" y="300" width="1500" height="800" fill="#000" filter="url(#stone)" opacity="0.6"/>'
    s += '<path d="M860,320 L2400,320 L2400,220 L940,220 Z" fill="#5a2a1a"/>'
    s += '<rect x="1300" y="560" width="300" height="540" fill="#1a0f08"/>' + glow(1450, 820, 350, 'warm', 0.8) + '<rect x="1320" y="580" width="260" height="520" fill="#ffc870" opacity="0.9"/>'
    s += '<rect x="1290" y="550" width="320" height="20" fill="#2a1a10"/>'
    s += banana(2250, 1100, 520, 141, '#100c0a') + banana(820, 1100, 420, 142, '#100c0a')
    s += '<rect x="0" y="1090" width="2400" height="260" fill="#1a1410"/>'
    for (vx, kind, h_) in [(150, 'woman', 300), (250, 'man', 330), (2330, 'woman', 290)]:
        s += villager(vx, 1110, h_, kind, '#0c0a08', rim='#ffb070')
    s += alcalde(820, 1180, 980, rim='#ffb070', hat_in_hand=True)
    s += mulata_full(1460, 1150, 900, look=-0.6, rim='#ffd27a', props=None, turn=-0.25)
    return S(s)

@art
def alcalde_l():
    return S(alcalde(1200, 1330, 1150, rim='#9fc2e8'))

@art
def alcalde_study():
    s = '<rect width="2400" height="1350" fill="#1a120c"/><rect width="2400" height="1350" fill="#000" filter="url(#stone)" opacity="0.7"/>'
    s += glow(1300, 760, 900, 'warm', 0.85)
    # giant shadow of the alcalde on the wall
    s += f'<g opacity="0.55" filter="url(#blur2)" transform="translate(1600,1350) scale(1.9) translate(-1600,-1350)">{alcalde(1700, 1350, 1000, rim=None)}</g>'.replace('#0b0b0e', '#000').replace('#30303c', '#000')
    s += '<rect x="0" y="0" width="2400" height="1350" fill="#140c06" opacity="0.25"/>'
    s += '<path d="M500,960 L1900,960 L2000,1060 L400,1060 Z" fill="#4a2c16"/><rect x="420" y="1060" width="1580" height="290" fill="#2a1a0c"/>'
    s += candle(1250, 960, 180, 44)
    s += '<path d="M1450,930 L1800,920 L1820,1000 L1460,1010 Z" fill="#e8dcc0"/>' + "".join(f'<path d="M{1480},{945+j*12} l{300-j*30},-4" stroke="#3a2a1a" stroke-width="3" opacity="0.6"/>' for j in range(5))
    s += '<path d="M1700,930 L1600,760" stroke="#f0ece0" stroke-width="10"/><path d="M1600,760 q-40,40 -10,110 q20,-60 10,-110" fill="#f0ece0"/>'
    s += '<rect x="1880" y="900" width="60" height="60" rx="10" fill="#1a1a1a"/>'
    s += alcalde(820, 1330, 1150, rim='#ffb070')
    return S(s)

@art
def gossip():
    s = '<rect width="2400" height="1350" fill="#0a0e16"/>'
    s += portales(-40, 2440, 1150, 760, wall="#2a2a30", shade="#121218", col="#34343c", upper=False, dark="#06060a")
    s += lamp(1200, 1150, 520) + glow(1200, 600, 700, 'warm', 0.5)
    s += cobbles(1150)
    for (vx, kind, h_, f) in [(820, 'woman', 560, 1), (960, 'woman', 600, -1), (1080, 'woman', 540, -1), (1480, 'woman', 580, 1), (1610, 'woman', 560, -1)]:
        s += villager(vx, 1230, h_, kind, '#030405', rim='#ffb070', facing=f, face=['#8a5a3a', '#c99a7a', '#6a4028', '#b07a56', '#9a6a4a'][int(vx) % 5])
    return S(s)

@art
def rooftops():
    s = sky('#03060e', '#14243a', mid='#0a1424') + stars(220, 151, 900) + moon(1750, 280, 140)
    r = random.Random(152)
    x = -100
    while x < 2500:
        w = r.uniform(260, 460); yb = r.uniform(900, 1050); h = r.uniform(80, 160)
        s += f'<rect x="{x:.0f}" y="{yb:.0f}" width="{w:.0f}" height="{1350-yb:.0f}" fill="#060a10"/>'
        s += f'<path d="M{x-20:.0f},{yb:.0f} L{x+w*0.5:.0f},{yb-h:.0f} L{x+w+20:.0f},{yb:.0f} Z" fill="#0c1018"/>'
        for j in range(int(w / 26)):
            s += f'<path d="M{x+j*26:.0f},{yb:.0f} L{x+w*0.5:.0f},{yb-h:.0f}" stroke="#141a24" stroke-width="3" opacity="0.6"/>'
        if r.random() < 0.5:
            s += f'<rect x="{x+w*0.4:.0f}" y="{yb+60:.0f}" width="50" height="70" fill="#ffc865" opacity="0.8"/>'
        x += w + r.uniform(-20, 40)
    s += church(1100, 1000, 0.7, '#05080d')
    return S(s)

@art
def flyer():
    # rumour image: a dark shape with spread rebozo crossing the moon
    s = '<g transform="translate(1200,500) rotate(-12)">'
    s += '<path d="M0,0 C-120,-40 -260,-20 -380,40 C-260,30 -150,50 -60,90 C-40,160 0,220 30,260 C40,200 60,140 70,90 C160,60 270,50 380,60 C260,0 130,-30 0,0 Z" fill="#020305"/>'
    s += '<circle cx="10" cy="-30" r="34" fill="#020305"/></g>'
    return S(s)

@art
def church_interior():
    s = '<rect width="2400" height="1350" fill="#120a06"/>'
    s += glow(1200, 520, 1100, 'warm', 0.65)
    # golden retablo
    s += '<rect x="700" y="80" width="1000" height="900" fill="#3a2410"/>'
    for i in range(5):
        cx_ = 800 + i * 200
        s += f'<rect x="{cx_-18}" y="120" width="36" height="820" fill="#c9962e"/><rect x="{cx_-26}" y="110" width="52" height="20" fill="#e8c060"/>'
        s += "".join(f'<circle cx="{cx_}" cy="{160+j*60}" r="10" fill="#f0d070" opacity="0.6"/>' for j in range(13))
    for i in range(4):
        nx = 900 + i * 200
        s += f'<path d="M{nx-60},700 L{nx-60},420 A60,60 0 0 1 {nx+60},420 L{nx+60},700 Z" fill="#1a0f06"/>'
        s += f'<path d="M{nx-30},690 L{nx-30},470 Q{nx},430 {nx+30},470 L{nx+30},690 Z" fill="#8a5a2a" opacity="0.8"/>'
    s += '<path d="M700,80 Q1200,-60 1700,80" stroke="#e8c060" stroke-width="20" fill="none"/>'
    s += '<rect x="900" y="980" width="600" height="120" fill="#2a1a0c"/><rect x="880" y="970" width="640" height="20" fill="#c9962e"/>'
    for cx_ in (960, 1080, 1320, 1440):
        s += candle(cx_, 970, 110, 22)
    s += '<rect x="0" y="1100" width="2400" height="250" fill="#0a0604"/>'
    for (bx, by) in [(300, 1200), (1700, 1220)]:
        s += f'<rect x="{bx}" y="{by}" width="500" height="30" fill="#2a1a0c"/>'
    s += '<g transform="translate(1250,1260) scale(0.5)">' + mulata_backview(0, 0, 900, rim='#ffcf70', reach=False, face_left=True) + '</g>'
    for (vx, kind, h_) in [(500, 'woman', 330), (620, 'man', 360), (1800, 'woman', 320), (1950, 'woman', 340)]:
        s += villager(vx, 1260, h_, kind, '#050302', rim='#ffb070')
    return S(s)

@art
def denuncia():
    s = '<rect width="2400" height="1350" fill="#0e0805"/>' + glow(1100, 700, 1000, 'warm', 0.75)
    s += '<path d="M0,700 L2400,680 L2400,1350 L0,1350 Z" fill="#3a2410"/>'
    s += '<path d="M500,330 L1700,300 L1760,1200 L460,1240 Z" fill="#e8dcc0"/><path d="M500,330 L1700,300 L1760,1200 L460,1240 Z" fill="#000" filter="url(#stone)" opacity="0.25"/>'
    s += '<text x="1100" y="470" text-anchor="middle" font-family="IM FELL English" font-size="78" fill="#2a1a0c" transform="rotate(-1.4 1100 470)">Al Santo Oficio</text>'
    s += '<text x="1100" y="560" text-anchor="middle" font-family="IM FELL English" font-style="italic" font-size="48" fill="#3a2a1a" transform="rotate(-1.4 1100 560)">denuncia contra una mujer de esta villa</text>'
    r = random.Random(161)
    for j in range(9):
        y = 650 + j * 58; w = r.uniform(700, 1000)
        s += f'<path d="M{620},{y} ' + " ".join(f"q{r.uniform(10,22):.0f},{r.uniform(-8,8):.0f} {r.uniform(24,40):.0f},0" for _ in range(int(w/34))) + f'" stroke="#3a2a1a" stroke-width="4" fill="none" opacity="0.75" transform="rotate(-1.4 1100 {y})"/>'
    s += '<circle cx="1500" cy="1120" r="60" fill="#7a1010"/><circle cx="1500" cy="1120" r="42" fill="#9a1818"/><path d="M1475,1120 L1525,1120 M1500,1095 L1500,1145" stroke="#5a0808" stroke-width="8"/>'
    s += '<path d="M1900,1240 L1650,680" stroke="#f0ece0" stroke-width="12"/><path d="M1650,680 q-70,90 -10,210 q40,-110 10,-210" fill="#f0ece0"/>'
    s += candle(2150, 1000, 220, 50)
    return S(s)

@art
def tribunal():
    s = '<rect width="2400" height="1350" fill="#100606"/>'
    s += '<rect x="0" y="0" width="2400" height="1000" fill="#3a0c0c"/>' + "".join(f'<path d="M{x},0 q20,500 0,1000" stroke="#1e0404" stroke-width="40" fill="none" opacity="0.6"/>' for x in range(60, 2400, 140))
    # green cross of the Holy Office
    s += glow(1200, 220, 360, 'red', 0.35)
    s += '<g transform="translate(1200,60) scale(0.62) translate(-1200,-120)"><path d="M1170,120 L1230,120 L1230,260 L1330,260 L1330,320 L1230,320 L1230,560 L1170,560 L1170,320 L1070,320 L1070,260 L1170,260 Z" fill="#1f5a2a" stroke="#3a8a46" stroke-width="7"/><path d="M1180,130 L1190,550" stroke="#5aaa66" stroke-width="6" opacity="0.6"/></g>'
    s += '<rect x="300" y="880" width="1800" height="160" fill="#1a0a06"/><rect x="280" y="860" width="1840" height="30" fill="#5a3a1a"/>'
    for cx_ in (520, 1880):
        s += candle(cx_, 860, 160, 34)
    for i, (hx, h_) in enumerate([(760, 700), (1200, 760), (1640, 700)]):
        s += hooded(hx, 1000, h_, rim='#ff5a3a', eyes=(i == 1), cross=False, seed=i)
    s += '<rect x="300" y="960" width="1800" height="400" fill="#140806"/>'
    return S(s)

@art
def hooded_l():
    return S(hooded(900, 1350, 1250, rim='#c0141a', seed=4), hooded(1500, 1350, 1300, rim='#c0141a', eyes=True, seed=5, candle=True))

@art
def arrest():
    s = sky('#020308', '#0e1420') + stars(60, 171, 500, '#8090a0')
    s += '<rect x="1300" y="500" width="900" height="600" fill="#14100c"/><path d="M1260,520 L2240,520 L2180,420 L1320,420 Z" fill="#1a0e08"/>'
    s += '<rect x="1600" y="760" width="140" height="340" fill="#ffc870" opacity="0.7"/>'
    s += palm(2300, 1100, 600, -0.1, 172, '#020304', '#040605')
    s += '<rect x="0" y="1080" width="2400" height="270" fill="#050403"/>'
    for (hx, h_, sd) in [(500, 900, 1), (800, 960, 2), (1100, 920, 3)]:
        s += hooded(hx, 1150, h_, rim='#ff7a3a', seed=sd)
        tx, ty = hx + 120, 1150 - h_ * 0.62
        s += f'<path d="M{tx},{ty} L{tx+20},{ty+260}" stroke="#2a1a0c" stroke-width="14"/>' + glow(tx, ty - 30, 240, 'warm', 0.9)
        s += f'<path d="M{tx-26},{ty} Q{tx},{ty-110} {tx+26},{ty} Z" fill="#ffb040"/><path d="M{tx-12},{ty} Q{tx},{ty-60} {tx+12},{ty} Z" fill="#fff0b0"/>'
    s += f'<g opacity="0.9">{alcalde(260, 1160, 900, rim="#ff9a5a")}</g>'
    return S(s)

@art
def ulua_dusk():
    s = sky('#1a2440', '#f0a070', mid='#a07090') + clouds(16, 150, 500, 181, '#ffc8a0', (0.3, 0.6), (200, 400), (30, 60))
    s += glow(400, 760, 500, 'warm', 0.9) + '<circle cx="400" cy="780" r="90" fill="#ffd8a0"/>'
    s += water(820, 1350, '#3a4a6a', '#0a1020') + reflection(400, 830, 1350, '#ffd0a0', 220)
    s += fortress(1400, 840, 1.1, '#1a1a24', lit=True)
    s += waves(830, 1350, 182, crest='#e0b090', n=120)
    # small boat approaching with figures
    s += '<path d="M700,1080 L1000,1080 L960,1120 L740,1120 Z" fill="#0a0a10"/><path d="M850,1080 L850,900 L960,1060 Z" fill="#1a1a24"/>'
    s += villager(780, 1082, 110, 'woman', '#0a0a10') + villager(900, 1082, 120, 'man', '#0a0a10')
    return S(s)

@art
def cell():
    s = '<rect width="2400" height="1350" fill="#16120e"/>' + stone_blocks(0, 0, 2400, 1350, 191, base="#4a4236", dark="#28231c", light="#625746", bh=(90, 150), bw=(180, 360))
    s += '<rect width="2400" height="1350" fill="#000" opacity="0.35"/>'
    s += '<rect x="1760" y="120" width="300" height="200" fill="#5a7090"/>' + "".join(f'<rect x="{1770+i*58}" y="120" width="14" height="200" fill="#111"/>' for i in range(6))
    s += '<rect x="0" y="1120" width="2400" height="230" fill="#1e1914"/>'
    r = random.Random(192)
    s += "".join(f'<path d="M{x:.0f},{1180+r.uniform(0,120):.0f} l{r.uniform(-60,60):.0f},{r.uniform(-14,14):.0f}" stroke="#8a7a50" stroke-width="3" opacity="0.6"/>' for x in [r.uniform(200, 900) for _ in range(120)])
    s += '<rect x="1500" y="1150" width="120" height="60" fill="#3a2a1a"/><path d="M1600,1150 L1640,1150 L1640,1200" stroke="#555" stroke-width="10" fill="none"/>'
    s += candle(1300, 1170, 70, 22)
    return S(s)

@art
def cell_beam():
    return S('<path d="M1760,320 L2060,320 L1500,1350 L900,1350 Z" fill="url(#beamcold)" filter="url(#blur3)"/>')

@art
def mulata_stand():
    return S(mulata_full(1200, 1320, 1150, look=0.3, rim='#ffd27a', props='charcoal', turn=0.25))

@art
def mulata_reach():
    return S(mulata_full(1000, 1320, 1100, look=0.6, rim='#ffd27a', props='charcoal', pose='reach', turn=0.35))

@art
def mulata_herbs():
    return S(mulata_full(1200, 1320, 1150, look=-0.2, rim='#9fc2e8', props='herbs'))

@art
def mulata_back():
    return S(mulata_backview(1100, 1330, 1150, rim='#ffd27a', reach=True, face_left=True))

@art
def ship_storm():
    s = sky('#03060a', '#1a2a36', mid='#0a141c') + clouds(40, 0, 600, 201, '#1e2c38', (0.4, 0.8)) + glow(1500, 250, 600, 'white', 0.3)
    s += water(820, 1350, '#0c1a24', '#02060a') + waves(830, 1350, 202, crest='#8fa8bb', n=180, amp=1.4)
    s += '<g opacity="0.85">' + fortress(500, 860, 0.45, '#070a0e', lit=True) + '</g>'
    s += f'<g filter="url(#blur4)" opacity="0.9">{glow(1450, 650, 500, "warm", 1.0)}</g>'
    s += ship(1450, 900, 0.8, "color", water=False) + waves(900, 1000, 203, crest="#ffe0a0", n=30, amp=1.2)
    return S(s)

@art
def ship_far():
    s = sky('#03060a', '#1a2a36', mid='#0a141c') + clouds(40, 0, 600, 211, '#1e2c38', (0.4, 0.8))
    s += water(760, 1350, '#0c1a24', '#02060a') + waves(770, 1350, 212, crest='#8fa8bb', n=160, amp=1.2)
    s += glow(1700, 700, 260, 'warm', 0.9) + ship(1700, 770, 0.22, "color", water=False)
    return S(s)

@art
def pyre():
    s = sky('#2a1a2a', '#c86a4a', mid='#6a3a4a')
    s += lit_church(1200, 1000, 0.55, wall="#3a2a2a", side="#2a1c1c", trim="#4a3020", dark="#140a0a")
    s += portales(-40, 760, 1000, 300, wall="#3a2a2a", shade="#1a1010", col="#4a3434", dark="#0a0606") + portales(1640, 2440, 1000, 300, wall="#3a2a2a", shade="#1a1010", col="#4a3434", dark="#0a0606")
    s += '<rect x="0" y="1000" width="2400" height="350" fill="#1a1010"/>'
    # stake + wood pile (empty, implied)
    s += '<rect x="1185" y="620" width="30" height="460" fill="#1a0e08"/>'
    r = random.Random(221)
    for j in range(40):
        a = r.uniform(-60, 60); L = r.uniform(140, 260)
        s += f'<rect x="{1200-L/2:.0f}" y="{1060+r.uniform(-60,40):.0f}" width="{L:.0f}" height="20" rx="8" fill="{r.choice(["#2a1a0e","#3a2412","#1e120a"])}" transform="rotate({a*0.3:.0f} 1200 1060)"/>'
    s += glow(1200, 1100, 400, 'red', 0.35)
    for i in range(16):
        x = 200 + i * 130 + r.uniform(-30, 30)
        if 1000 < x < 1400: continue
        s += villager(x, 1350, r.uniform(380, 480), r.choice(['man', 'woman']), '#050303', rim='#ff7a4a', facing=1 if x < 1200 else -1)
    return S(s)

# ================================================================== ENDING
@art
def archive():
    s = '<rect width="2400" height="1350" fill="#0e0a07"/>' + glow(1200, 700, 1000, 'warm', 0.6)
    r = random.Random(231)
    for sh in range(5):
        y = 120 + sh * 200
        s += f'<rect x="0" y="{y+160}" width="2400" height="24" fill="#3a2410"/>'
        x = 0
        while x < 2400:
            w = r.uniform(60, 150); h = r.uniform(110, 160)
            s += f'<rect x="{x:.0f}" y="{y+160-h:.0f}" width="{w-6:.0f}" height="{h:.0f}" fill="{r.choice(["#c8b890","#b0a07a","#d8c8a0","#8a7a5a"])}" opacity="0.85"/>'
            s += f'<rect x="{x:.0f}" y="{y+160-h*0.6:.0f}" width="{w-6:.0f}" height="8" fill="#6a2a1a" opacity="0.8"/>'
            x += w
    s += '<rect width="2400" height="1350" fill="#000" opacity="0.35"/>'
    s += '<path d="M0,1080 L2400,1060 L2400,1350 L0,1350 Z" fill="#2a1a0c"/>'
    s += '<path d="M700,1100 L1600,1080 L1640,1300 L680,1320 Z" fill="#e2d4b0"/>'
    s += '<text x="1160" y="1170" text-anchor="middle" font-family="IM FELL English" font-size="54" fill="#2a1a0c" transform="rotate(-1 1160 1170)">Proceso contra la mulata…</text>'
    s += "".join(f'<path d="M760,{1210+j*28} l{760-j*60},-14" stroke="#3a2a1a" stroke-width="4" opacity="0.6"/>' for j in range(3))
    s += '<text x="1450" y="1290" font-family="IM FELL English" font-style="italic" font-size="40" fill="#8a1a1a" transform="rotate(-1 1450 1290)">¿?</text>'
    s += candle(1900, 1080, 180, 40)
    return S(s)

@art
def opera():
    s = '<rect width="2400" height="1350" fill="#080406"/>'
    s += '<rect x="300" y="120" width="1800" height="900" fill="#0c1a2a"/>' + glow(1200, 500, 700, 'white', 0.35)
    s += ship(1200, 820, 0.7, "silhouette").replace('#05070a', '#1a2a3a')
    s += '<path d="M300,880 q150,-40 300,0 q150,40 300,0 q150,-40 300,0 q150,40 300,0 q150,-40 300,0 q150,40 300,0 L2100,1020 L300,1020 Z" fill="#14283a"/>'
    s += mulata_full(1200, 1000, 520, rim='#ffffff', props=None)
    # red velvet curtains + proscenium
    for sd in (-1, 1):
        x0 = 0 if sd < 0 else 2100
        s += f'<rect x="{x0}" y="0" width="300" height="1350" fill="#6a0c14"/>' + "".join(f'<path d="M{x0+20+j*50},0 q{sd*20},600 0,1350" stroke="#3a0408" stroke-width="18" fill="none"/>' for j in range(6))
    s += '<path d="M0,0 L2400,0 L2400,160 Q1200,60 0,160 Z" fill="#7a1018"/><path d="M0,160 Q1200,60 2400,160" stroke="#c9962e" stroke-width="14" fill="none"/>'
    s += '<rect x="280" y="1020" width="1840" height="40" fill="#c9962e"/><rect x="0" y="1060" width="2400" height="290" fill="#050203"/>'
    for i in range(28):
        hx = 60 + i * 85
        s += f'<circle cx="{hx}" cy="{1160+(i%2)*20}" r="38" fill="#020101"/><rect x="{hx-50}" y="{1180+(i%2)*20}" width="100" height="200" rx="40" fill="#020101"/>'
    s += '<path d="M1200,0 L900,1020 L1500,1020 Z" fill="#fff8e0" opacity="0.08"/>'
    return S(s)

@art
def manila():
    s = sky('#3a3a6a', '#ffb070', mid='#e07a7a') + glow(1700, 760, 600, 'warm', 0.9) + '<circle cx="1700" cy="770" r="110" fill="#ffe0a0"/>'
    s += water(820, 1350, '#6a4a6a', '#1a1428') + reflection(1700, 830, 1350, '#ffd0a0', 240)
    s += hills(830, 90, '#3a2a40', 241)
    # stone church + nipa huts
    s += lit_church(600, 860, 0.4, wall="#2a1e28", side="#1e1620", trim="#3a2a30", dark="#0e0a10", two_towers=False)
    for hx in (900, 1050, 1180):
        s += f'<rect x="{hx-50}" y="790" width="100" height="70" fill="#1a1218"/><path d="M{hx-80},795 L{hx},720 L{hx+80},795 Z" fill="#241a20"/><path d="M{hx-50},860 l0,30 M{hx+50},860 l0,30" stroke="#1a1218" stroke-width="8"/>'
    s += palm(300, 900, 560, 0.1, 242, '#120c14', '#160e18') + palm(1350, 880, 480, -0.15, 243, '#120c14', '#160e18')
    # galleon at anchor
    s += ship(2050, 920, 0.45, "silhouette").replace('#05070a', '#140e18')
    # pier with the woman
    s += '<rect x="0" y="1010" width="1500" height="40" fill="#1a1016"/>' + "".join(f'<rect x="{x}" y="1050" width="20" height="200" fill="#140c12"/>' for x in range(40, 1500, 160))
    s += mulata_full(1150, 1012, 380, rim='#ffb070', props='herbs')
    for (vx, kind, h_) in [(600, 'man', 330), (720, 'man', 350)]:
        s += villager(vx, 1012, h_, kind, '#0c080c', rim='#ffb070', facing=1)
    return S(s)

@art
def cafetal():
    s = sky('#03060a', '#0e1a20') + '<rect x="0" y="700" width="2400" height="650" fill="#050a08"/>'
    s += hills(760, 140, '#08100c', 251)
    r = random.Random(252)
    for row, (yy, sc, col) in enumerate([(820, 0.5, '#0c1a12'), (920, 0.7, '#0a160e'), (1060, 0.9, '#08120a')]):
        for i in range(14):
            x = i * 180 + r.uniform(-40, 40) + row * 60
            s += f'<g transform="translate({x:.0f},{yy}) scale({sc})">'
            for j in range(12):
                a = r.uniform(-160, -20); L = r.uniform(80, 180)
                ex, ey = math.cos(math.radians(a)) * L, math.sin(math.radians(a)) * L
                s += f'<path d="M0,0 L{ex:.0f},{ey:.0f}" stroke="{col}" stroke-width="5"/>'
                s += f'<ellipse cx="{ex:.0f}" cy="{ey:.0f}" rx="30" ry="14" fill="{col}" transform="rotate({a:.0f} {ex:.0f} {ey:.0f})"/>'
                if r.random() < 0.4:
                    s += "".join(f'<circle cx="{ex*0.6+k*8:.0f}" cy="{ey*0.6+6:.0f}" r="6" fill="#8a1a1a"/>' for k in range(3))
            s += '</g>'
    s += mulata_full(1500, 950, 300, rim='#9fc2e8', props='herbs')
    s += '<g filter="url(#blur3)"><rect x="0" y="880" width="2400" height="140" fill="#9fb0c0" opacity="0.15"/></g>'
    return S(s)

@art
def cafetal_fg():
    r = random.Random(261); s = ""
    for i in range(10):
        x = r.choice([r.uniform(-100, 500), r.uniform(1900, 2500)]); y = r.uniform(1150, 1450)
        for j in range(10):
            a = r.uniform(-170, -10); L = r.uniform(180, 360)
            ex, ey = x + math.cos(math.radians(a)) * L, y + math.sin(math.radians(a)) * L
            s += f'<path d="M{x:.0f},{y:.0f} L{ex:.0f},{ey:.0f}" stroke="#020403" stroke-width="9"/><ellipse cx="{ex:.0f}" cy="{ey:.0f}" rx="70" ry="30" fill="#020403" transform="rotate({a:.0f} {ex:.0f} {ey:.0f})"/>'
            if r.random() < 0.3:
                s += "".join(f'<circle cx="{(x+ex)/2+k*14:.0f}" cy="{(y+ey)/2:.0f}" r="10" fill="#5a0e0e"/>' for k in range(3))
    return S(s)

@art
def ruda_door():
    s = '<rect width="2400" height="1350" fill="#0a0806"/>'
    s += '<rect x="0" y="0" width="2400" height="1050" fill="#3a2e24"/><rect x="0" y="0" width="2400" height="1050" fill="#000" filter="url(#stone)" opacity="0.7"/>'
    s += '<rect x="800" y="80" width="700" height="980" fill="#2a1a0e"/><rect x="820" y="100" width="520" height="960" fill="#4a2c14"/>'
    s += '<rect x="1340" y="100" width="140" height="960" fill="#ffc870" opacity="0.85"/>' + glow(1410, 700, 500, 'warm', 0.7)
    s += '<path d="M1340,1060 L1480,1060 L1900,1350 L1300,1350 Z" fill="#ffb860" opacity="0.25"/>'
    s += '<rect x="0" y="1050" width="2400" height="300" fill="#1a140e"/><rect x="760" y="1040" width="780" height="40" fill="#2a2018"/>'
    s += herb_bundle(1100, 1060, 1.6, -78, seed=271)
    s += '<rect width="2400" height="1350" fill="#06101a" opacity="0.25"/>'
    return S(s)

@art
def llorona():
    s = sky('#03060c', '#14222e', mid='#0a141e') + stars(140, 281, 600) + moon(600, 260, 90)
    s += ridge(780, 120, '#08121a', 282) + water(860, 1350, '#0e1c26', '#03070b') + reflection(600, 865, 1350, '#dfe8f0', 180)
    s += ghost_woman(1600, 1100, 640)
    s += tree(2200, 1150, 900, 283, '#020406', 'willow', -0.1) + reeds(0, 2400, 1250, 284, '#020406', 160, 220)
    return S(s)

@art
def title_bg():
    base = ART["wall_base"]()
    return base


# ================================================================== positioned layers / extras
@art
def mulata_left():
    return S(mulata_full(380, 1330, 1050, look=0.7, rim='#ffd27a', props='charcoal', turn=0.4))

@art
def jailer_right():
    return S(jailer(2080, 1340, 1100, facing=-1, lantern_up=True))

@art
def jailer_right_shock():
    return S(jailer(2080, 1340, 1100, facing=-1, lantern_up=True, mouth_open=1.0))

@art
def twin():
    return S(mulata_full(620, 1240, 760, look=0.4, rim='#9fc2e8', props='herbs'),
             f'<g opacity="0.6">{mulata_full(1800, 1240, 760, look=-0.4, rim="#cfe0ff", props="herbs", turn=-0.3)}</g>')

@art
def strange_lights():
    r = random.Random(301); s = '<g filter="url(#blur3)">'
    for i in range(14):
        c = r.choice(['#7fe0c0', '#c090ff', '#ffd27a', '#80c0ff'])
        s += f'<circle cx="{r.uniform(600,1600):.0f}" cy="{r.uniform(500,950):.0f}" r="{r.uniform(40,110):.0f}" fill="{c}" opacity="{r.uniform(0.3,0.7):.2f}"/>'
    return S(s + '</g>')

@art
def profile_close():
    s = '<rect width="2400" height="1350" fill="#0c0806"/>' + glow(1900, 600, 1100, 'warm', 1.0) + glow(2100, 500, 600, 'white', 0.5)
    s += f'<g transform="translate(2500,520)">{ship(0, 300, 1.2, "color", water=False)}</g>'
    s += '<rect width="2400" height="1350" fill="#000" opacity="0.15"/>'
    s += f'<g transform="translate(1050,560) scale(2.6)">{head_profile(rim="#ffd27a", lit=0.9)}</g>'
    s += '<path d="M600,1350 C620,1180 700,1100 820,1070 C900,1050 1000,1060 1080,1100 C1160,1150 1240,1250 1260,1350 Z" fill="#1d2a4e"/>'
    s += "".join(f'<path d="M{640+i*40},1350 C{680+i*36},1220 {760+i*30},1130 {860+i*22},1080" stroke="{REB[i%4]}" stroke-width="4" fill="none" opacity="0.5"/>' for i in range(14))
    s += '<path d="M1080,1100 C1160,1150 1240,1250 1260,1350" stroke="#ffd27a" stroke-width="8" fill="none" opacity="0.8" filter="url(#blur1)"/>'
    return S(s)

@art
def face_close():
    return S(mulata_bust(1200, 700, 3.0, look=0.1, smile=0.55))

@art
def face_close_eyes():
    return S(mulata_bust(1200, 700, 3.0, look=0.25, smile=0.4, lids=0.3))

@art
def lantern_pool():
    return S('<ellipse cx="1200" cy="720" rx="1100" ry="700" fill="url(#warmglow)" opacity="0.75"/>')

if __name__ == "__main__":
    names = sys.argv[1:] or list(ART)
    os.makedirs("art", exist_ok=True)
    for n in names:
        write(n, ART[n]())
        print("wrote", n)
