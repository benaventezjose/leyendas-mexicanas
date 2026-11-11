#!/usr/bin/env python3
"""Illustrations for 'Popocatépetl e Iztaccíhuatl' — writes art/*.svg (2400x1350).
Render: node /home/claude/pipeline/render_svg.js art/*.svg      Usage: python3 make_art.py [name ...]"""
import sys, os, math, random
sys.path.insert(0, '/home/claude/pipeline'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from art import *
from chars import *

ART = {}
def art(fn):
    ART[fn.__name__] = fn
    return fn

G = lambda x, y, k, f, flip=False: f'<g transform="translate({x},{y}) scale({-k if flip else k},{k})">{f}</g>'

def blur_ell(cx, cy, rx, ry, col, op, f=3):
    return f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{rx:.0f}" ry="{ry:.0f}" fill="{col}" opacity="{op}" filter="url(#blur{f})"/>'

def mist(y, h=120, op=0.25, col="#c8d8e6", seed=1, n=9, x0=0, x1=2400):
    r = random.Random(seed)
    return "".join(blur_ell(r.uniform(x0, x1), y + r.uniform(-h / 3, h / 3), r.uniform(250, 520), h * r.uniform(0.5, 1), col, round(op * r.uniform(0.6, 1.2), 2)) for _ in range(n))

def ground(y, color="#020406", amp=30, seed=2):
    r = random.Random(seed); pts = " ".join(f"{x},{y + r.uniform(-amp, amp):.0f}" for x in range(0, 2401, 120))
    return f'<polygon points="0,1350 {pts} 2400,1350" fill="{color}"/>'

def lg(id_, stops, vertical=True):
    s = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    return f'<defs><linearGradient id="{id_}" x1="0" y1="0" x2="{0 if vertical else 1}" y2="{1 if vertical else 0}">{s}</linearGradient></defs>'

# ------------------------------------------------------------------ volcanoes
def popo(cx, base, w, h, rock="#1a2a3a", snow="#e4ecf4", snow_line=0.42, seed=3, crater=True, lit="#ffffff", dark="#0c1620"):
    """Symmetric cone with crater + snow cap streaks. base=y of the base, w=half-width at base, h=height."""
    r = random.Random(seed); top = base - h; cw = w * 0.12
    pts = [(cx - w, base)]
    for i in range(1, 12):
        t = i / 12; pts.append((cx - w + (w - cw) * t + r.uniform(-8, 8), base - h * (t ** 1.18) + r.uniform(-6, 6)))
    pts += [(cx - cw, top), (cx - cw * 0.4, top + 10), (cx + cw * 0.4, top + 8), (cx + cw, top)]
    for i in range(11, 0, -1):
        t = i / 12; pts.append((cx + w - (w - cw) * t + r.uniform(-8, 8), base - h * (t ** 1.18) + r.uniform(-6, 6)))
    pts.append((cx + w, base))
    P = " ".join(f"{x:.0f},{y:.0f}" for x, y in pts)
    g = uid("pp")
    s = lg(g, [(0, rock), (1, dark)], vertical=False)
    s += f'<polygon points="{P}" fill="url(#{g})"/>'
    # snow cap with ragged streaks running down the gullies
    sl = base - h * (1 - snow_line)
    cap = [(cx - cw, top), (cx + cw, top)]
    wl = (cx - (w - cw) * (1 - ((base - sl) / h) ** (1 / 1.18)) - cw) if False else None
    def xat(y, side):
        t = ((base - y) / h) ** (1 / 1.18); return cx + side * (w - (w - cw) * t)
    sp = [f"{cx-cw:.0f},{top}", f"{cx+cw:.0f},{top}"]
    ys = sl
    right = []; left = []
    n = 18
    for i in range(n + 1):
        u = i / n
        x = xat(sl, 1) - u * (xat(sl, 1) - xat(sl, -1))
        d = r.uniform(-40, 120) if i % 2 else r.uniform(-30, 30)
        right.append(f"{x:.0f},{sl + d * (1 - abs(u-0.5)*1.2):.0f}")
    s += f'<polygon points="{cx-cw:.0f},{top} {cx+cw:.0f},{top} {xat(sl,1):.0f},{sl:.0f} {" ".join(right)} {xat(sl,-1):.0f},{sl:.0f}" fill="{snow}"/>'
    # shading: left half darker snow
    s += f'<polygon points="{cx-cw:.0f},{top} {cx-cw*0.2:.0f},{top} {cx-w*0.25:.0f},{sl+60:.0f} {xat(sl,-1):.0f},{sl:.0f}" fill="#7f93a8" opacity="0.55"/>'
    for i in range(9):
        side = r.choice((-1, 1)); u = r.uniform(0.1, 0.85)
        x0 = cx + side * (cw + (xat(sl, 1) - cx - cw) * u); y0 = top + (sl - top) * u + r.uniform(10, 40); L = r.uniform(40, 130) * (1 - u * 0.5)
        dx = side * L * (w / h) * 0.9; wd = r.uniform(5, 12)
        s += f'<path d="M{x0-wd:.0f},{y0:.0f} L{x0+dx:.0f},{y0+L:.0f} L{x0+wd:.0f},{y0:.0f} Z" fill="{snow}" opacity="0.7"/>'
    if crater:
        s += f'<ellipse cx="{cx}" cy="{top+6}" rx="{cw*0.9:.0f}" ry="10" fill="#2a3440"/>'
    s += f'<path d="M{cx+cw:.0f},{top} L{xat(sl,1):.0f},{sl:.0f}" stroke="{lit}" stroke-width="5" opacity="0.5" filter="url(#blur1)"/>'
    return s

def izta(x0, x1, base, h, rock="#1a2a3a", snow="#e4ecf4", dark="#0c1620", seed=4):
    """Sleeping-woman ridge: feet (left) - knees - chest (highest) - head (right), as seen from the west."""
    W = x1 - x0
    prof = [(0.0, 0.0), (0.06, 0.28), (0.12, 0.5), (0.18, 0.62), (0.22, 0.66), (0.27, 0.62), (0.33, 0.74), (0.38, 0.86), (0.42, 0.82),
            (0.48, 0.8), (0.55, 0.92), (0.6, 1.0), (0.66, 0.98), (0.71, 0.9), (0.75, 0.84), (0.79, 0.86), (0.83, 0.8), (0.87, 0.72),
            (0.9, 0.74), (0.93, 0.62), (0.97, 0.3), (1.0, 0.0)]
    r = random.Random(seed)
    pts = [(x0 + W * u, base - h * v + (r.uniform(-5, 5) if 0 < v < 1 else 0)) for u, v in prof]
    P = " ".join(f"{x:.0f},{y:.0f}" for x, y in pts)
    g = uid("iz")
    s = lg(g, [(0, rock), (1, dark)])
    s += f'<polygon points="{P} {x1},{base} {x0},{base}" fill="url(#{g})"/>'
    # snow: follow the ridge down by a ragged band
    top = " ".join(f"{x:.0f},{y:.0f}" for x, y in pts[2:-2])
    bot = []
    for x, y in reversed(pts[2:-2]):
        bot.append(f"{x + r.uniform(-20, 20):.0f},{y + h * r.uniform(0.1, 0.5):.0f}")
        bot.append(f"{x + r.uniform(10, 40):.0f},{y + h * r.uniform(0.05, 0.2):.0f}")
    s += f'<polygon points="{top} {" ".join(bot)}" fill="{snow}"/>'
    for i in range(0):
        u = r.uniform(0.12, 0.92); x = x0 + W * u
        y = min(yy for (xx, yy) in pts if abs(xx - x) < W * 0.06) if any(abs(xx - x) < W * 0.06 for xx, yy in pts) else base - h * 0.6
        L = h * r.uniform(0.08, 0.2); wd = r.uniform(5, 12)
        s += f'<path d="M{x-wd:.0f},{y+h*0.28:.0f} L{x+r.uniform(-20,20):.0f},{y+h*0.28+L:.0f} L{x+wd:.0f},{y+h*0.28:.0f} Z" fill="{snow}" opacity="0.6"/>'
    s += f'<polyline points="{top}" stroke="#ffffff" stroke-width="5" fill="none" opacity="0.55" filter="url(#blur1)"/>'
    return s

def plume(x, y, scale=1.0, col="#b8c2cc", op=0.5, seed=5, drift=1.0):
    r = random.Random(seed); s = ""
    for i in range(16):
        t = i / 15
        s += blur_ell(x + drift * 500 * t * scale + r.uniform(-30, 30), y - 520 * t * scale, (60 + 260 * t) * scale, (50 + 120 * t) * scale, col, round(op * (1 - t * 0.6), 2), 3 if i % 3 else 2)
    return s

def pines(y, x0=0, x1=2400, n=40, hmin=120, hmax=320, color="#04080c", seed=3, rim=None):
    r = random.Random(seed); s = ""
    for _ in range(n):
        x = r.uniform(x0, x1); h = r.uniform(hmin, hmax); w = h * 0.28; yy = y + r.uniform(-20, 30)
        tiers = "".join(f'<path d="M{x-w*(1-k*0.2):.0f},{yy-h*k*0.25:.0f} L{x:.0f},{yy-h*(0.4+k*0.2):.0f} L{x+w*(1-k*0.2):.0f},{yy-h*k*0.25:.0f} Z"/>' for k in range(4))
        s += f'<g fill="{color}">{tiers}<rect x="{x-4:.0f}" y="{yy-20:.0f}" width="8" height="30"/><path d="M{x},{yy-h} L{x-w*0.3:.0f},{yy-h*0.6:.0f} L{x+w*0.3:.0f},{yy-h*0.6:.0f} Z"/></g>'
        if rim:
            s += f'<path d="M{x:.0f},{yy-h:.0f} L{x+w:.0f},{yy:.0f}" stroke="{rim}" stroke-width="2" opacity="0.35"/>'
    return s

def maguey(x, y, k=1.0, color="#04070a", seed=1, rim=None):
    r = random.Random(seed); s = ""
    for i in range(11):
        a = math.radians(-90 + (i - 5) * 15 + r.uniform(-5, 5)); L = (160 + r.uniform(-40, 50)) * k * (1 - abs(i - 5) * 0.06)
        ex, ey = x + math.cos(a) * L, y + math.sin(a) * L
        nx, ny = -math.sin(a) * 14 * k, math.cos(a) * 14 * k
        s += f'<path d="M{x+nx:.0f},{y+ny:.0f} Q{(x+ex)/2+nx:.0f},{(y+ey)/2+ny:.0f} {ex:.0f},{ey:.0f} Q{(x+ex)/2-nx:.0f},{(y+ey)/2-ny:.0f} {x-nx:.0f},{y-ny:.0f} Z" fill="{color}"/>'
        if rim and i > 5:
            s += f'<path d="M{x:.0f},{y:.0f} Q{(x+ex)/2+nx:.0f},{(y+ey)/2+ny:.0f} {ex:.0f},{ey:.0f}" stroke="{rim}" stroke-width="2" fill="none" opacity="0.4"/>'
    return s

def nopal(x, y, k=1.0, color="#04070a"):
    pads = [(0, -60, 40, 60, 0), (-50, -150, 34, 50, -25), (50, -150, 34, 50, 25), (-20, -240, 28, 42, -10), (70, -240, 26, 40, 30)]
    return "".join(f'<ellipse cx="{x+dx*k:.0f}" cy="{y+dy*k:.0f}" rx="{rx*k:.0f}" ry="{ry*k:.0f}" fill="{color}" transform="rotate({a} {x+dx*k:.0f} {y+dy*k:.0f})"/>' for dx, dy, rx, ry, a in pads)

def temple(x, base, w=420, h=360, color="#0a0f16", lit="#ffb060", fire=True, steps=4, shrine=True):
    s = ""
    for i in range(steps):
        ww = w * (1 - i * 0.18); hh = h / steps
        s += f'<rect x="{x-ww/2:.0f}" y="{base-hh*(i+1):.0f}" width="{ww:.0f}" height="{hh+1:.0f}" fill="{color}"/>'
        s += f'<path d="M{x-ww/2:.0f},{base-hh*(i+1):.0f} L{x+ww/2:.0f},{base-hh*(i+1):.0f}" stroke="{lit}" stroke-width="2" opacity="0.25"/>'
    s += f'<path d="M{x-w*0.1:.0f},{base} L{x-w*0.06:.0f},{base-h} L{x+w*0.06:.0f},{base-h} L{x+w*0.1:.0f},{base} Z" fill="#141c26"/>'
    for i in range(10):
        yy = base - h * i / 10
        s += f'<path d="M{x-w*0.1+i*w*0.004:.0f},{yy:.0f} L{x+w*0.1-i*w*0.004:.0f},{yy:.0f}" stroke="#05080c" stroke-width="3"/>'
    if shrine:
        tw = w * 0.36
        s += f'<rect x="{x-tw/2:.0f}" y="{base-h-tw*0.6:.0f}" width="{tw:.0f}" height="{tw*0.6:.0f}" fill="{color}"/>'
        s += f'<path d="M{x-tw/2-10:.0f},{base-h-tw*0.6:.0f} L{x:.0f},{base-h-tw*1.05:.0f} L{x+tw/2+10:.0f},{base-h-tw*0.6:.0f} Z" fill="{color}"/>'
        s += f'<rect x="{x-tw*0.14:.0f}" y="{base-h-tw*0.42:.0f}" width="{tw*0.28:.0f}" height="{tw*0.42:.0f}" fill="{lit}" opacity="0.85"/>'
    if fire:
        s += glow(x, base - h - (w * 0.2 if shrine else 0), 160, "warm", 0.8)
    return s

def adobe(x, base, w=160, h=100, color="#0a0f14", door=True, lit=None):
    s = f'<rect x="{x-w/2:.0f}" y="{base-h:.0f}" width="{w}" height="{h}" fill="{color}"/>'
    s += f'<rect x="{x-w/2-6:.0f}" y="{base-h-10:.0f}" width="{w+12}" height="12" fill="{color}"/>'
    if door:
        s += f'<rect x="{x-14:.0f}" y="{base-56:.0f}" width="28" height="56" fill="{lit or "#020304"}" opacity="{0.8 if lit else 1}"/>'
    return s

def city_row(base, seed=1, n=26, color="#080c12", lit=0.3, x0=0, x1=2400, hscale=1.0):
    r = random.Random(seed); s = ""
    for _ in range(n):
        x = r.uniform(x0, x1); w = r.uniform(90, 220); h = r.uniform(60, 130) * hscale
        s += adobe(x, base + r.uniform(-10, 10), w, h, color, True, "#ffb060" if r.random() < lit else None)
    return s

def stars_sky(top="#060b16", bot="#1c3248", n=220, seed=1, ymax=900):
    return sky(top, bot) + stars(n, seed, ymax)

def snowflakes(n=500, seed=1, op=0.8):
    r = random.Random(seed)
    return "".join(f'<circle cx="{r.uniform(0,2400):.0f}" cy="{r.uniform(0,1350):.0f}" r="{r.choice([1.5,2,2.5,3,4,6])}" fill="#ffffff" opacity="{r.uniform(0.3,op):.2f}"/>' for _ in range(n))

def flowers(x0, x1, y, n=60, seed=1, cols=("#e8a020", "#f0c040", "#c84a20", "#efe6d2")):
    r = random.Random(seed); s = ""
    for _ in range(n):
        x = r.uniform(x0, x1); yy = y + r.uniform(-24, 18); k = r.uniform(0.6, 1.3); c = r.choice(cols)
        s += f'<circle cx="{x:.0f}" cy="{yy:.0f}" r="{12*k:.0f}" fill="{c}"/><circle cx="{x:.0f}" cy="{yy:.0f}" r="{5*k:.0f}" fill="#7a3a10" opacity="0.6"/>'
        s += f'<path d="M{x-14*k:.0f},{yy:.0f} q14,-10 28,0" stroke="#2a4a20" stroke-width="3" fill="none" opacity="0.6"/>'
    return s

def brazier(x, y, k=1.0):
    s = f'<path d="M{x-70*k},{y} L{x-50*k},{y+90*k} L{x+50*k},{y+90*k} L{x+70*k},{y} Z" fill="#1a0e08"/>'
    s += f'<path d="M{x-70*k},{y} L{x+70*k},{y}" stroke="#ffa040" stroke-width="{5*k}" opacity="0.6"/>'
    for i in range(5):
        dx = (i - 2) * 22 * k
        s += f'<path d="M{x+dx},{y} C{x+dx-20*k},{y-60*k} {x+dx+10*k},{y-100*k} {x+dx},{y-140*k+abs(i-2)*30*k} C{x+dx+24*k},{y-80*k} {x+dx+20*k},{y-40*k} {x+dx},{y} Z" fill="#ffb040" opacity="0.85"/>'
    s += f'<path d="M{x},{y} C{x-20*k},{y-50*k} {x},{y-80*k} {x},{y-110*k} C{x+16*k},{y-60*k} {x+14*k},{y-30*k} {x},{y} Z" fill="#fff0b0"/>'
    return s

def pillar(x, y0, y1, w=90, color="#100a08", lit="#ff9a50", mural=True):
    s = f'<rect x="{x-w/2}" y="{y0}" width="{w}" height="{y1-y0}" fill="{color}"/>'
    s += f'<rect x="{x+w/2-10}" y="{y0}" width="10" height="{y1-y0}" fill="{lit}" opacity="0.25"/>'
    if mural:
        for i in range(int((y1 - y0) / 90)):
            yy = y0 + 40 + i * 90
            s += f'<path d="M{x-w/2+10},{yy} l{w/4},-20 l{w/4},20 l{w/4},-20 l{w/4-20},20" stroke="#8a2a1a" stroke-width="5" fill="none" opacity="0.6"/>'
    return s

def hall(lit="#ff9a50"):
    """Palace hall of the lord of Tlaxcala: painted pillars, red-and-ochre mural, brazier light."""
    s = sky("#0c0806", "#2a160c")
    s += '<rect x="0" y="0" width="2400" height="180" fill="#080504"/>'
    s += '<rect x="0" y="180" width="2400" height="60" fill="#3a1a10"/>'
    for i in range(30):
        x = i * 82
        s += f'<path d="M{x},230 l40,-40 l40,40" stroke="#c8902a" stroke-width="6" fill="none" opacity="0.6"/>'
    s += '<rect x="0" y="240" width="2400" height="640" fill="#2a160e"/>'
    # mural: procession of warriors and serpent band
    r = random.Random(4)
    for i in range(12):
        x = 140 + i * 190
        s += f'<g opacity="0.35">{G(x, 820, 0.42, warrior_sil(r.choice(["march","stand"]), fill="#7a2a18", rim=None, seed=i))}</g>'
    s += '<path d="M0,860 C200,820 400,900 600,860 C800,820 1000,900 1200,860 C1400,820 1600,900 1800,860 C2000,820 2200,900 2400,860" stroke="#3a7a5a" stroke-width="22" fill="none" opacity="0.5"/>'
    s += '<rect x="0" y="880" width="2400" height="470" fill="#140a06"/>'
    for i in range(14):
        s += f'<path d="M{i*200},1350 L{1200 + (i*200-1200)*0.3:.0f},880" stroke="#2a160e" stroke-width="3" opacity="0.7"/>'
    for x in (260, 760, 1640, 2140):
        s += pillar(x, 180, 900, 120)
    s += glow(1200, 760, 900, "warm", 0.55)
    # dais with a seat of jaguar skin
    s += '<rect x="960" y="760" width="480" height="120" fill="#1e100a"/><rect x="960" y="760" width="480" height="10" fill="#c8902a" opacity="0.5"/>'
    return s

# ------------------------------------------------------------------ BACKGROUNDS
@art
def volcanoes_night():
    s = stars_sky("#040812", "#1a3046", 260, 3, 800) + moon(1900, 260, 70)
    s += ridge(980, 60, "#0e1824", 9)
    s += popo(800, 1040, 620, 720, rock="#1c2c3e", dark="#0a121c", snow="#dfe8f2", seed=5)
    s += izta(1250, 2400, 1040, 430, rock="#1a2a3a", dark="#0a121c", snow="#d8e2ee", seed=6)
    s += glow(800, 330, 160, "red", 0.35)
    s += mist(1000, 120, 0.3, "#8aa4bc", 3, 12)
    s += ground(1150, "#03060a", 30, 4) + pines(1170, 0, 2400, 50, 80, 200, "#020407", 5)
    s += city_row(1240, 5, 30, "#020407", 0.25, hscale=0.6)
    return svg(s)

@art
def volcanoes_dawn():
    s = sky("#1a2a48", "#e8a070", "#8a7a9a") + stars(40, 2, 300)
    s += glow(1500, 900, 900, "warm", 0.5)
    s += ridge(1000, 70, "#4a4a62", 8)
    s += popo(800, 1060, 620, 720, rock="#5a5a78", dark="#2a2a40", snow="#fff0e8", lit="#ffd0a0", seed=5)
    s += izta(1250, 2400, 1060, 430, rock="#5a5a78", dark="#2a2a40", snow="#ffeee6", seed=6)
    s += mist(1020, 140, 0.4, "#e8c0b0", 4, 14)
    s += ground(1160, "#120e18", 30, 4) + pines(1180, 0, 2400, 40, 80, 200, "#0a080e", 6)
    s += "".join(maguey(x, 1300, 0.9, "#06050a", i) for i, x in enumerate((150, 600, 1500, 2150)))
    return svg(s)

@art
def snow_slope():
    s = sky("#0a1424", "#3a5470") + plume(1800, 300, 1.2, "#c8d4e0", 0.4, 2)
    s += '<polygon points="0,1350 0,900 600,760 1300,520 2000,300 2400,200 2400,1350" fill="#9fb4c8"/>'
    s += '<polygon points="0,1350 0,1000 700,860 1400,640 2100,420 2400,340 2400,1350" fill="#c8d6e4"/>'
    r = random.Random(3)
    for _ in range(40):
        x = r.uniform(0, 2400); y = 1350 - (x / 2400) * 900 + r.uniform(-60, 200)
        s += f'<path d="M{x:.0f},{y:.0f} q{r.uniform(40,140):.0f},{r.uniform(-30,-10):.0f} {r.uniform(160,300):.0f},{r.uniform(-60,-20):.0f}" stroke="#7f94aa" stroke-width="{r.uniform(3,8):.0f}" fill="none" opacity="0.5"/>'
    for _ in range(14):
        x = r.uniform(0, 2400); y = 1350 - (x / 2400) * 900 + r.uniform(0, 260)
        s += f'<path d="M{x:.0f},{y:.0f} l40,-40 l50,30 l-20,20 Z" fill="#2a3644"/>'
    s += mist(900, 200, 0.4, "#e4ecf4", 6, 12)
    return svg(s)

@art
def carry_close():
    s = sky("#0a1424", "#5a7490") + snowflakes(300, 4, 0.6)
    s += '<polygon points="0,1350 0,1100 2400,900 2400,1350" fill="#c8d6e4"/>'
    s += G(1150, 1360, 1.08, popo_carry(rim="#e4f0ff"))
    s += mist(1200, 160, 0.45, "#e4ecf4", 7, 10)
    return svg(s)

@art
def summit_kneel():
    s = stars_sky("#030610", "#24384e", 200, 6, 700) + moon(500, 220, 60)
    s += '<path d="M0,1350 L0,1000 C500,900 900,860 1200,850 C1500,860 1900,900 2400,1000 L2400,1350 Z" fill="#b8c8d8"/>'
    s += '<path d="M0,1350 L0,1080 C600,980 1000,960 1200,960 C1500,970 1900,1010 2400,1080 L2400,1350 Z" fill="#dce6f0"/>'
    s += glow(1300, 900, 600, "warm", 0.45)
    s += '<ellipse cx="1060" cy="1010" rx="420" ry="48" fill="#3a2a1a"/>' + flowers(660, 1460, 1000, 120, 3)
    s += G(1040, 975, 0.78, lying_woman())
    s += G(1500, 1040, 0.72, warrior_sil("torch", torch=True, rim="#ffc070", facing=-1))
    return svg(s)

@art
def torch_close():
    s = sky("#040608", "#1a1410")
    s += glow(1200, 520, 900, "warm", 0.9)
    s += '<path d="M1180,1350 L1214,640" stroke="#2a160a" stroke-width="60" stroke-linecap="round"/>'
    s += '<path d="M1150,700 l120,0 l-14,60 l-92,0 Z" fill="#3a2410"/>'
    for i, (dx, hh) in enumerate([(-50, 300), (0, 460), (50, 340), (-20, 380), (30, 260)]):
        s += f'<path d="M{1210+dx},700 C{1150+dx},{700-hh*0.4} {1180+dx},{700-hh*0.8} {1210+dx*0.5},{700-hh} C{1250+dx},{700-hh*0.6} {1270+dx},{700-hh*0.3} {1210+dx},700 Z" fill="{["#c84a10","#ffb040","#ff8a20","#ffd060","#ff7020"][i]}" opacity="0.85"/>'
    s += '<path d="M1210,700 C1170,600 1190,520 1210,440 C1240,520 1250,600 1210,700 Z" fill="#fff4c0"/>'
    s += snowflakes(200, 8, 0.6)
    return svg(s)

@art
def popo_face_snow():
    s = sky("#06080c", "#2a3848") + glow(1200, 700, 800, "warm", 0.35)
    s += popo_bust(1200, 560, 2.3, rim="#dfeaff", lids=0.0, eyes_closed=True, frost=True)
    s += snowflakes(400, 9, 0.8)
    return svg(s)

@art
def izta_ghost_cloud():
    s = sky("#040810", "#1a2a3c") + stars(120, 4, 600)
    s += izta(0, 2400, 1250, 360, rock="#14202e", dark="#060a10", snow="#c8d4e0", seed=8)
    s += ('<defs><linearGradient id="gfade" x1="0" y1="0" x2="0" y2="1350" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#fff"/><stop offset="0.55" stop-color="#fff"/><stop offset="0.85" stop-color="#fff" stop-opacity="0"/></linearGradient>'
          '<mask id="gmask" maskUnits="userSpaceOnUse" x="0" y="0" width="2400" height="1350"><rect width="2400" height="1350" fill="url(#gfade)"/></mask></defs>')
    s += f'<g mask="url(#gmask)"><g opacity="0.5" filter="url(#ghost)">{izta_bust(1200, 480, 1.9, rim="#dfeaff", pale=True, eyes_closed=True, wind=0.6)}</g></g>'
    s += mist(700, 260, 0.5, "#9fb4c8", 9, 12)
    return svg(s)

@art
def valley_dawn():
    s = sky("#2a3a5a", "#f0b080", "#a88a9a")
    s += popo(600, 900, 420, 520, rock="#6a6a86", dark="#3a3a54", snow="#fff2ea", seed=2)
    s += izta(950, 1900, 900, 300, rock="#6a6a86", dark="#3a3a54", snow="#ffeee6")
    s += mist(900, 120, 0.45, "#f0d0c0", 5, 14)
    s += '<rect x="0" y="960" width="2400" height="390" fill="#6a7a9a" opacity="0.6"/>'
    s += f'<rect x="0" y="960" width="2400" height="390" fill="url(#moonglow)" opacity="0.2"/>'
    s += ground(1000, "#2a2430", 20, 3) + ground(1150, "#120e16", 40, 5)
    s += "".join(maguey(x, 1320, 1.1, "#06050a", i, "#ffb080") for i, x in enumerate((200, 700, 1700, 2250)))
    s += "".join(nopal(x, 1320, 1.0, "#06050a") for x in (450, 1950))
    return svg(s)

@art
def tenochtitlan():
    s = sky("#1a2240", "#d89a70", "#7a6a8a")
    s += popo(2050, 820, 300, 380, rock="#5a5a78", dark="#3a3a54", snow="#fff0e6", seed=2)
    s += izta(1250, 1900, 820, 200, rock="#5a5a78", dark="#3a3a54", snow="#ffece2")
    s += ridge(840, 40, "#3a3850", 5)
    s += water(860, 1350, "#6a6a8a", "#1a1a2a")
    s += reflection(1200, 870, 1300, "#ffd0a0", 300)
    # island city with twin temple, causeway
    s += '<ellipse cx="1200" cy="930" rx="760" ry="70" fill="#14121c"/>'
    s += city_row(930, 7, 50, "#14121c", 0.35, 500, 1900, 0.6)
    s += temple(1200, 920, 380, 300, "#100e18", "#ffb060")
    s += temple(860, 930, 220, 160, "#100e18", "#ffb060", shrine=True)
    s += temple(1540, 930, 220, 160, "#100e18", "#ffb060", shrine=True)
    s += '<path d="M0,1000 L500,940" stroke="#100e18" stroke-width="16"/><path d="M1900,940 L2400,1010" stroke="#100e18" stroke-width="16"/>'
    r = random.Random(2)
    for _ in range(12):
        x = r.uniform(100, 2300); y = r.uniform(1050, 1300)
        s += f'<path d="M{x-60:.0f},{y:.0f} Q{x:.0f},{y+20:.0f} {x+60:.0f},{y:.0f} Z" fill="#06050a"/><path d="M{x+20:.0f},{y:.0f} l20,-60" stroke="#06050a" stroke-width="4"/>'
    s += mist(900, 80, 0.3, "#f0c0a0", 3, 10)
    return svg(s)

@art
def tribute_line():
    s = sky("#2a2030", "#c88a5a") + glow(1800, 700, 700, "warm", 0.6)
    s += ridge(900, 60, "#3a2a2a", 3) + ground(1050, "#1a1010", 20, 2)
    r = random.Random(5)
    for i in range(9):
        x = 150 + i * 250
        s += G(x, 1180 + r.uniform(-10, 10), 0.62, warrior_sil("march", shield=False, weapon=False, crest=False, fill="#0a0606", rim="#ffb070"))
        # bundle on the back with tumpline
        s += f'<rect x="{x-110}" y="{1180-560}" width="90" height="140" rx="16" fill="#3a2414"/><path d="M{x-70},{1180-560} q30,-40 60,-10" stroke="#3a2414" stroke-width="6" fill="none"/>'
    s += '<rect x="0" y="1180" width="2400" height="170" fill="#0a0606"/>'
    s += "".join(maguey(x, 1340, 0.8, "#050303", i) for i, x in enumerate((80, 900, 1600, 2300)))
    return svg(s)

@art
def tlaxcala_city():
    s = stars_sky("#060a18", "#3a3a5a", 150, 5, 600)
    s += glow(1200, 1200, 1100, "warm", 0.35)
    s += popo(1700, 760, 300, 360, rock="#1e2a3c", dark="#0e1420", snow="#d8e2ee", seed=4)
    s += izta(1950, 2500, 760, 200, rock="#1e2a3c", dark="#0e1420", snow="#d0dae6")
    s += ridge(820, 80, "#121a26", 6) + ridge(900, 70, "#0a1018", 7)
    s += temple(800, 1000, 460, 360, "#06080c", "#ffb060")
    s += temple(1350, 1030, 260, 200, "#06080c", "#ffb060")
    s += city_row(1080, 9, 40, "#05070a", 0.35, 0, 2400, 0.8)
    s += ground(1180, "#030405", 20, 9)
    s += "".join(maguey(x, 1330, 1.0, "#020304", i, "#ffb070") for i, x in enumerate((120, 2000, 2300)))
    return svg(s)

@art
def copal_temple():
    s = sky("#0a0606", "#2a1610") + glow(1200, 800, 900, "warm", 0.6)
    s += '<rect x="0" y="900" width="2400" height="450" fill="#1a0e08"/>'
    s += '<path d="M700,1350 L900,800 L1500,800 L1700,1350 Z" fill="#2a1a10"/>'
    for i in range(8):
        s += f'<path d="M{700+i*25},{1350-i*69} L{1700-i*25},{1350-i*69}" stroke="#120a06" stroke-width="6"/>'
    s += brazier(1200, 760, 1.4)
    r = random.Random(7)
    for i in range(14):
        t = i / 13
        s += blur_ell(1200 + math.sin(t * 6) * 120, 640 - t * 600, 60 + t * 200, 40 + t * 80, "#d8c8b0", round(0.35 * (1 - t * 0.5), 2), 3)
    s += G(800, 1250, 0.55, warrior_sil("stand", shield=False, weapon=False, crest=True, rim="#ffb060", fill="#050303"))
    s += G(1600, 1250, 0.55, warrior_sil("stand", shield=False, weapon=False, crest=True, rim="#ffb060", fill="#050303"), True)
    return svg(s)

@art
def palace_hall():
    return svg(hall())

@art
def izta_portrait():
    s = sky("#0a0606", "#2a160c") + glow(700, 700, 900, "warm", 0.55)
    for x in (300, 2100):
        s += pillar(x, 0, 1350, 160)
    s += izta_bust(1200, 520, 2.1, rim="#ffd090", lids=0.3, smile=0.2)
    return svg(s)

@art
def izta_moon():
    s = stars_sky("#040812", "#1a2a40", 160, 7, 700) + moon(1900, 260, 80)
    s += tree(250, 1350, 900, 4, "#020407", "ahuehuete")
    s += izta_bust(1200, 540, 2.0, rim="#cfe4ff", lids=0.45, smile=0.0, wind=0.4)
    s += reeds(1600, 2400, 1350, 2, "#020407", 60, 220)
    return svg(s)

@art
def izta_shock():
    s = sky("#06080c", "#1a2230") + glow(1200, 700, 800, "moon", 0.6)
    s += izta_bust(1200, 540, 2.2, rim="#dfeaff", shock=True)
    return svg(s)

@art
def izta_awake():
    s = sky("#020408", "#1a2a3a") + glow(1200, 520, 900, "moon", 0.8)
    s += snowflakes(300, 2, 0.8)
    s += f'<g filter="url(#ghost)">{izta_bust(1200, 560, 2.4, rim="#ffffff", pale=True, ghost_eyes=True, wind=1.0)}</g>'
    s += '<rect width="2400" height="1350" fill="#7ab0ff" opacity="0.1"/>'
    return svg(s)

@art
def market():
    s = sky("#2a2a40", "#e0a070") + glow(1600, 600, 800, "warm", 0.5)
    s += popo(1900, 760, 260, 300, rock="#6a6080", dark="#3a3450", snow="#fff0e0") + izta(200, 900, 760, 160, rock="#6a6080", dark="#3a3450", snow="#ffeee0")
    s += city_row(820, 3, 30, "#2a1a1a", 0.0, hscale=0.8)
    s += '<rect x="0" y="830" width="2400" height="520" fill="#4a3020"/>'
    r = random.Random(3)
    for i in range(9):  # stalls with awnings and goods
        x = 120 + i * 270
        s += f'<path d="M{x-110},{900} L{x+110},{900} L{x+130},{960} L{x-130},{960} Z" fill="{r.choice(["#8a2a1a","#c8902a","#2e6a5a","#d8d0c0"])}"/>'
        s += f'<path d="M{x-120},960 L{x-120},1150 M{x+120},960 L{x+120},1150" stroke="#1a0e08" stroke-width="10"/>'
        for k in range(6):
            s += f'<circle cx="{x-90+k*36}" cy="1120" r="{r.uniform(12,20):.0f}" fill="{r.choice(["#e8a020","#a82a1a","#3a7a2a","#d8c8a0","#6a3a1a"])}"/>'
        s += f'<rect x="{x-120}" y="1140" width="240" height="20" fill="#2a1810"/>'
        s += G(x + 60, 1240, 0.3, woman_sil(rim=None, fill="#120a08", facing=r.choice((-1, 1))))
    s += '<rect x="0" y="1250" width="2400" height="100" fill="#2a1a10"/>'
    return svg(s)

@art
def lovers_tree():
    s = stars_sky("#030712", "#14283a", 220, 8, 800) + moon(1700, 240, 90)
    s += ridge(900, 60, "#0a1420", 4)
    s += water(940, 1350, "#16283a", "#04080e") + reflection(1700, 945, 1350, "#dfe8f2", 160)
    s += tree(700, 1180, 1100, 6, "#020406", "ahuehuete")
    s += ground(1180, "#020406", 18, 7)
    s += reeds(1400, 2400, 1250, 5, "#020406", 90, 200)
    return svg(s)

@art
def stars_water():
    s = sky("#02040c", "#0e1c30") + stars(400, 11, 700)
    s += '<path d="M0,400 C600,300 1800,300 2400,420" stroke="#cfd8ff" stroke-width="140" fill="none" opacity="0.06" filter="url(#blur3)"/>'
    s += water(720, 1350, "#0a1828", "#02040a")
    r = random.Random(5)
    for _ in range(160):
        x = r.uniform(0, 2400); y = r.uniform(740, 1340)
        s += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r.uniform(2,8):.0f}" ry="1.6" fill="#dfe8ff" opacity="{r.uniform(0.2,0.6):.2f}"/>'
    s += reeds(0, 700, 1350, 9, "#010204", 50, 260) + reeds(1800, 2400, 1350, 10, "#010204", 50, 260)
    return svg(s)

@art
def popo_portrait():
    s = sky("#0a0606", "#2a160c") + glow(1700, 700, 900, "warm", 0.55)
    s += popo_bust(1200, 520, 2.1, rim="#ffd090", lids=0.15, smile=0.1)
    return svg(s)

@art
def popo_grief():
    s = sky("#06040a", "#2a0e0e") + glow(1200, 760, 900, "red", 0.35)
    s += popo_bust(1200, 520, 2.2, rim="#ff9a70", grief=True)
    return svg(s)

@art
def popo_kneel_hall():
    s = hall()
    s += G(1200, 760, 0.62, father_bust(0, 0, 1.0, rim="#ffd090"))
    s += G(1250, 1290, 0.55, warrior_sil("kneel", rim="#ffc070", fill="#06040a", facing=1, weapon=False))
    return svg(s)

@art
def father_portrait():
    s = sky("#0a0606", "#2a160c") + glow(1500, 700, 900, "warm", 0.5)
    for x in (250, 2150):
        s += pillar(x, 0, 1350, 160)
    s += father_bust(1200, 520, 2.1, rim="#ffd090")
    return svg(s)

@art
def rival_portrait():
    s = sky("#080202", "#3a0a08") + glow(1500, 800, 900, "red", 0.5)
    s += rival_bust(1200, 520, 2.1, rim="#ff5a3a")
    return svg(s)

@art
def war_drums():
    s = sky("#1a0404", "#7a2a10") + glow(1200, 1000, 1000, "red", 0.5)
    s += popo(1200, 900, 500, 500, rock="#2a0e0a", dark="#120404", snow="#e0a090", seed=4)
    s += ground(1000, "#0a0202", 20, 3)
    for i, x in enumerate((500, 900, 1500, 1900)):
        s += f'<rect x="{x-60}" y="1060" width="120" height="200" rx="20" fill="#2a1008"/><ellipse cx="{x}" cy="1060" rx="60" ry="18" fill="#c8a070"/>'
        s += G(x + 120, 1300, 0.45, warrior_sil("stand", shield=False, weapon=False, fill="#050101", rim="#ff6a3a"), i % 2 == 0)
    return svg(s)

@art
def runner_maguey():
    s = stars_sky("#040810", "#1a2a3a", 150, 9, 700) + moon(600, 260, 70)
    s += popo(1900, 860, 360, 420, rock="#16222e", dark="#0a1018", snow="#c8d4e0") + ridge(900, 60, "#0c141e", 8)
    s += ground(1000, "#060a10", 20, 4)
    for i in range(18):
        s += maguey(i * 140 + (60 if i % 2 else 0), 1080 + (i % 3) * 20, 0.6, "#04070a", i, "#8aa4c0")
    s += ground(1250, "#020305", 20, 6)
    for i in range(8):
        s += maguey(i * 330 + 100, 1350, 1.3, "#010203", 30 + i)
    return svg(s)

@art
def hands_ribbon():
    s = sky("#06080e", "#1a2232") + glow(1200, 700, 800, "moon", 0.6)
    # his forearm (horizontal) and her two hands tying a woven ribbon
    s += f'<path d="M0,760 C400,720 900,700 1500,720 C1600,724 1680,740 1720,780 C1700,830 1620,850 1500,850 C900,860 400,860 0,880 Z" fill="{SK_POPO["base"]}"/>'
    s += f'<path d="M0,760 C400,720 900,700 1500,720" stroke="{SK_POPO["hi"]}" stroke-width="10" fill="none" opacity="0.6"/>'
    s += f'<path d="M0,880 C400,860 900,860 1500,850" stroke="{SK_POPO["deep"]}" stroke-width="16" fill="none" opacity="0.6"/>'
    s += '<path d="M1000,700 C1040,690 1080,690 1100,700 L1110,860 C1080,870 1040,872 1010,866 Z" fill="#e8e0cc"/>'
    for k in range(6):
        s += f'<path d="M1010,{720+k*26} L1104,{716+k*26}" stroke="#a8231a" stroke-width="7"/>'
        s += f'<path d="M1030,{732+k*26} l12,-10 l12,10 l12,-10 l12,10" stroke="#2e8a7a" stroke-width="4" fill="none"/>'
    s += '<path d="M1100,780 C1160,820 1180,900 1150,1000 M1100,790 C1200,830 1240,900 1240,980" stroke="#e8e0cc" stroke-width="22" fill="none" stroke-linecap="round"/>'
    for hx, flip in ((900, False), (1260, True)):
        f = -1 if flip else 1
        s += f'<g transform="translate({hx},780) scale({f},1)">'
        s += f'<path d="M-260,-200 C-160,-170 -80,-120 -20,-80 C20,-60 60,-40 90,-20 C110,-6 110,14 90,20 C60,20 30,10 0,0 C-60,10 -120,0 -260,-40 Z" fill="{SK_IZTA["base"]}"/>'
        for j in range(4):
            s += f'<path d="M-20,{-70+j*22} C30,{-60+j*22} 80,{-40+j*20} 110,{-30+j*18} C120,{-22+j*18} 116,{-10+j*18} 100,{-8+j*18}" stroke="{SK_IZTA["shadow"]}" stroke-width="3" fill="none"/>'
        s += f'<path d="M-260,-200 C-160,-170 -80,-120 -20,-80" stroke="{SK_IZTA["hi"]}" stroke-width="8" fill="none" opacity="0.6"/>'
        s += '<path d="M-200,-190 C-180,-160 -180,-90 -200,-50" stroke="#e8e0cc" stroke-width="60" fill="none" opacity="0.9"/>'  # huipil sleeve
        s += '</g>'
    return svg(s)

@art
def army_depart():
    s = sky("#2a2a48", "#f0b070", "#a07a8a") + glow(1900, 800, 700, "warm", 0.6)
    s += popo(500, 820, 360, 420, rock="#5a5070", dark="#2a2440", snow="#fff0e0") + izta(800, 1500, 820, 200, rock="#5a5070", dark="#2a2440", snow="#ffeee0")
    s += ground(880, "#3a2a2a", 20, 2)
    r = random.Random(4)
    for row, (y, k, n) in enumerate([(960, 0.2, 40), (1060, 0.3, 28), (1220, 0.46, 16)]):
        for i in range(n):
            x = i * (2400 / n) + r.uniform(-20, 20) + row * 40
            s += G(x, y, k, warrior_sil(r.choice(["march", "march", "stand"]), fill=["#2a1a1a", "#160c0c", "#060303"][row], rim="#ffb070" if row == 2 else None, seed=i))
        if row == 1:
            for i in range(5):  # banners (quachpantli)
                x = 300 + i * 450
                s += f'<path d="M{x},{y-380} L{x},{y-180}" stroke="#160c0c" stroke-width="6"/><path d="M{x},{y-380} l70,20 l-10,50 l-60,-10 Z" fill="#a8231a"/>'
    s += mist(1250, 80, 0.3, "#c8a080", 4, 10)
    return svg(s)

@art
def izta_temple_top():
    s = sky("#2a2a48", "#f0b070", "#a07a8a") + glow(1700, 900, 800, "warm", 0.6)
    s += ridge(1000, 60, "#5a4a60", 2) + ground(1100, "#3a2a30", 15, 2)
    s += '<path d="M200,1350 L400,1050 L1100,1050 L1300,1350 Z" fill="#1a1018"/>'
    s += '<rect x="560" y="880" width="380" height="170" fill="#1a1018"/><path d="M540,880 L750,760 L960,880 Z" fill="#1a1018"/>'
    s += G(980, 1080, 0.45, woman_sil(rim="#ffb070", fill="#0a0608", crown=True, hair_wind=0.8, facing=1))
    r = random.Random(2)
    for i in range(50):  # army as a thin line far away
        x = 1700 + i * 14 + r.uniform(-4, 4)
        s += f'<rect x="{x:.0f}" y="{1080 + r.uniform(-4,4):.0f}" width="4" height="12" fill="#2a1a20"/>'
    s += mist(1090, 40, 0.4, "#f0c0a0", 3, 8, 1500, 2400)
    return svg(s)

@art
def battle_sky():
    s = sky("#1a0404", "#a03a10", "#5a1408") + glow(1200, 1100, 1200, "red", 0.6)
    s += ridge(1000, 80, "#2a0806", 6) + ground(1150, "#0a0202", 30, 5)
    for i in range(10):
        s += plume(200 + i * 240, 1100, 0.8, "#2a0a06", 0.5, i, 0.4)
    return svg(s)

@art
def popo_battle():
    s = sky("#1a0404", "#a03a10") + glow(1200, 1000, 1000, "red", 0.5)
    s += ground(1150, "#0a0202", 30, 5)
    s += G(1150, 1250, 0.95, warrior_sil("fight", rim="#ffb070", fill="#050101", cape=True))
    s += G(1700, 1250, 0.8, warrior_sil("fight", rim="#ff6a3a", fill="#050101", seed=2), True)
    s += G(500, 1300, 0.7, warrior_sil("march", rim="#ff6a3a", fill="#050101", seed=3))
    return svg(s)

@art
def camp_night():
    s = stars_sky("#040608", "#1a1a24", 200, 12, 700)
    s += ridge(920, 70, "#0a0c12", 3) + ground(1050, "#05060a", 20, 4)
    for x in (500, 1300, 2000):
        s += brazier(x, 1080, 0.7) + glow(x, 1040, 300, "warm", 0.6)
        for k in range(4):
            s += G(x - 220 + k * 140, 1150, 0.3, warrior_sil("kneel", rim="#ffb060", fill="#030304", weapon=False, seed=k), k % 2 == 0)
    s += ground(1250, "#020203", 10, 6)
    return svg(s)

@art
def izta_grief():
    s = sky("#06040a", "#1a1014") + glow(1200, 900, 900, "warm", 0.4)
    s += '<rect x="0" y="0" width="2400" height="1350" fill="#120a0a" opacity="0.6"/>'
    s += '<rect x="900" y="200" width="600" height="700" fill="#0a1220"/>' + moon(1300, 380, 50, halo=3)
    s += '<rect x="900" y="200" width="600" height="700" fill="none" stroke="#2a1810" stroke-width="40"/>'
    s += '<rect x="0" y="1050" width="2400" height="300" fill="#0a0606"/>'
    s += G(1180, 1250, 0.75, woman_sil(rim="#ffd090", fill="#06040a", arms="hands", facing=-1, dress="#d8d0c4"))
    return svg(s)

@art
def flowers_floor():
    s = sky("#080404", "#1a0e08") + glow(1200, 800, 900, "warm", 0.5)
    s += '<rect x="0" y="700" width="2400" height="650" fill="#1a0e08"/>'
    r = random.Random(3)
    for i in range(40):
        x = 900 + r.uniform(-300, 400); y = 960 + r.uniform(-60, 80)
        s += f'<path d="M{x:.0f},{y:.0f} q{r.uniform(-60,60):.0f},{r.uniform(-20,20):.0f} {r.uniform(-120,120):.0f},{r.uniform(-30,30):.0f}" stroke="#2a4a1a" stroke-width="4" fill="none"/>'
    s += flowers(600, 1500, 970, 60, 4, ("#efe6d2", "#f0c040", "#e8a020"))
    s += '<path d="M600,1000 C900,940 1300,960 1700,1010" stroke="#c8902a" stroke-width="10" fill="none" opacity="0.7"/>'
    return svg(s)

@art
def izta_window():
    s = sky("#020408", "#0a1420")
    s += '<rect x="0" y="0" width="2400" height="1350" fill="#0a0606"/>'
    s += '<rect x="700" y="150" width="1000" height="900" fill="#0e1a2c"/>'
    s += f'<g>{stars(80, 3, 500)}</g>'
    s += moon(1450, 360, 60, halo=4)
    s += popo(1000, 900, 260, 320, rock="#16222e", dark="#0a1018", snow="#c8d4e0") + ridge(930, 30, "#0a1018", 2)
    s += '<rect x="700" y="150" width="1000" height="900" fill="none" stroke="#1a100a" stroke-width="60"/>'
    s += '<rect x="0" y="1050" width="2400" height="300" fill="#060404"/>'
    s += G(900, 1180, 0.7, woman_sil(rim="#cfe4ff", fill="#04030a", facing=1, hair_wind=0.0, dress="#c8ccd4"))
    return svg(s)

@art
def izta_bed():
    s = sky("#040608", "#141a22") + glow(1200, 600, 900, "moon", 0.5)
    s += '<rect x="0" y="760" width="2400" height="590" fill="#0e0c0c"/>'
    s += '<rect x="560" y="860" width="1300" height="80" rx="10" fill="#6a5430"/>'
    for i in range(26):
        s += f'<path d="M{580+i*50},864 L{580+i*50},936" stroke="#4a3820" stroke-width="4"/>'
    s += G(1240, 890, 1.15, lying_woman())
    s += flowers(560, 1860, 960, 50, 6, ("#efe6d2", "#f0c040"))
    for x in (420, 1980):
        s += candle(x, 900, 80, 20) + glow(x, 820, 220, "warm", 0.6)
    for i in range(10):
        t = i / 9
        s += blur_ell(420 + 20 * math.sin(t * 5), 780 - t * 500, 30 + 120 * t, 20 + 40 * t, "#c8c0b0", round(0.3 * (1 - t), 2), 3)
    return svg(s)

@art
def return_gate():
    s = sky("#2a2a48", "#f0a070", "#a07a8a") + glow(1200, 800, 800, "warm", 0.5)
    s += popo(1900, 760, 300, 360, rock="#5a5070", dark="#2a2440", snow="#fff0e0")
    s += temple(1200, 960, 520, 420, "#120c12", "#ffb060", fire=False)
    s += city_row(1000, 4, 30, "#0e0a0e", 0.0, hscale=0.9)
    s += '<rect x="0" y="1000" width="2400" height="350" fill="#2a1e1e"/>'
    s += '<path d="M1000,1350 L1150,1000 L1250,1000 L1400,1350 Z" fill="#3a2a26"/>'
    return svg(s)

@art
def army_return():
    s = sky("#2a2a48", "#f0a070", "#a07a8a") + glow(500, 800, 800, "warm", 0.5)
    s += popo(1700, 820, 360, 420, rock="#5a5070", dark="#2a2440", snow="#fff0e0") + izta(1900, 2600, 820, 200, rock="#5a5070", dark="#2a2440", snow="#ffeee0")
    s += ground(900, "#3a2a2a", 20, 2)
    r = random.Random(8)
    for row, (y, k, n) in enumerate([(980, 0.22, 30), (1090, 0.32, 20)]):
        for i in range(n):
            x = i * (2400 / n) + r.uniform(-20, 20)
            s += G(x, y, k, warrior_sil("march", fill=["#2a1a1a", "#160c0c"][row], rim=None, seed=i), True)
    s += G(1200, 1300, 0.6, warrior_sil("march", fill="#060303", rim="#ffc070", cape=True), True)
    return svg(s)

@art
def rival_flee():
    s = sky("#100204", "#4a0a0a") + glow(1700, 900, 800, "red", 0.4)
    s += ridge(950, 90, "#1a0406", 3) + ground(1150, "#060101", 30, 5)
    s += pines(1150, 0, 2400, 30, 200, 500, "#030001", 7)
    s += G(1300, 1230, 0.55, warrior_sil("run", rim="#ff4a2a", fill="#030001", crest=True, weapon=False))
    return svg(s)

@art
def citlaltepetl():
    s = stars_sky("#030610", "#1a2a40", 220, 13, 900) + moon(500, 240, 50)
    s += popo(1500, 1000, 700, 760, rock="#1a2638", dark="#080e16", snow="#dfe8f2", seed=11, crater=False)
    s += mist(1000, 160, 0.35, "#8aa4bc", 5, 14)
    s += ground(1150, "#020407", 30, 8) + pines(1180, 0, 2400, 40, 80, 220, "#010204", 9)
    return svg(s)

@art
def procession_valley():
    s = stars_sky("#040812", "#1c3044", 200, 14, 700) + moon(1950, 230, 60)
    s += popo(900, 900, 560, 620, rock="#1c2c3e", dark="#0a121c", snow="#dfe8f2", seed=5)
    s += izta(1300, 2400, 900, 380, rock="#1a2a3a", dark="#0a121c", snow="#d8e2ee", seed=6)
    s += mist(900, 100, 0.35, "#8aa4bc", 4, 12)
    s += ground(1000, "#060a10", 20, 3)
    s += '<path d="M0,1300 C600,1200 900,1120 1400,1060 C1700,1030 2000,1010 2400,1000" stroke="#1a2430" stroke-width="40" fill="none"/>'
    s += "".join(maguey(x, 1330, 1.1, "#010203", i, "#8aa4c0") for i, x in enumerate((150, 700, 2100)))
    return svg(s)

@art
def pines_climb():
    s = sky("#0a1424", "#3a5470") + plume(1500, 200, 1.0, "#a8b4c0", 0.35, 4)
    s += '<polygon points="0,1350 0,900 800,640 1500,400 2400,300 2400,1350" fill="#1a2634"/>'
    s += '<polygon points="900,600 1500,400 2400,300 2400,600 1600,560" fill="#c8d6e4" opacity="0.8"/>'
    s += pines(800, 0, 1200, 30, 200, 380, "#04080c", 3, "#9fb4c8") + pines(1150, 0, 2400, 40, 300, 560, "#020406", 4, "#9fb4c8")
    s += mist(900, 160, 0.35, "#c8d8e6", 3, 10)
    return svg(s)

@art
def snow_cover():
    s = sky("#0a1424", "#4a6480") + snowflakes(600, 5, 0.9)
    s += '<path d="M0,1350 L0,1000 C500,900 900,860 1200,850 C1500,860 1900,900 2400,1000 L2400,1350 Z" fill="#c8d8e8"/>'
    s += G(1040, 975, 0.78, lying_woman(dress="#f4f8fc", skin="#dfe6ee", hair="#9fb0c4", rim="#ffffff"))
    s += f'<g opacity="0.7">{G(1500, 1040, 0.72, warrior_sil("torch", torch=True, rim="#ffffff", fill="#a8b8c8", facing=-1))}</g>'
    s += '<path d="M0,1350 L0,1060 C500,1000 900,980 1200,990 C1500,1000 1900,1020 2400,1060 L2400,1350 Z" fill="#e8f0f8"/>'
    s += mist(1000, 200, 0.5, "#ffffff", 8, 12)
    return svg(s)

@art
def transform():
    s = stars_sky("#02040c", "#1a2c44", 320, 15, 900) + glow(1200, 500, 1200, "white", 0.4)
    s += popo(800, 1100, 640, 760, rock="#2a3c52", dark="#0c1624", snow="#f4f8ff", seed=5)
    s += izta(1250, 2400, 1100, 460, rock="#2a3c52", dark="#0c1624", snow="#eef4ff", seed=6)
    s += f'<g opacity="0.25" filter="url(#ghost)">{G(1820, 650, 0.9, lying_woman(dress="#ffffff", skin="#ffffff", hair="#cfe0ff"))}</g>'
    s += mist(1100, 160, 0.4, "#9fb8d6", 6, 14)
    return svg(s)

@art
def popo_crater_smoke():
    s = stars_sky("#040608", "#2a2024", 160, 16, 600) + glow(1200, 600, 700, "red", 0.4)
    s += popo(1200, 1500, 1500, 1100, rock="#2a2a34", dark="#0c0c12", snow="#d8dce4", seed=9)
    s += glow(1200, 420, 300, "red", 0.6)
    return svg(s)

@art
def codex_paper():
    g = uid("cx")
    s = lg(g, [(0, "#d8c4a0"), (1, "#b89a70")]) + f'<rect width="2400" height="1350" fill="url(#{g})"/>'
    s += '<rect width="2400" height="1350" filter="url(#paper)" fill="#000"/>'
    s += '<rect x="80" y="80" width="2240" height="1190" fill="none" stroke="#8a2a1a" stroke-width="14"/>'
    # stylised mountains (tepetl glyphs) and footprints, codex style
    for x, lab in ((700, 0), (1300, 1)):
        s += f'<path d="M{x-200},900 C{x-180},600 {x-80},440 {x},430 C{x+80},440 {x+180},600 {x+200},900 Z" fill="#3a7a5a" stroke="#1a1008" stroke-width="8"/>'
        s += f'<path d="M{x-200},900 L{x+200},900 L{x+180},960 L{x-180},960 Z" fill="#c8902a" stroke="#1a1008" stroke-width="8"/>'
        s += f'<path d="M{x-90},560 C{x-40},520 {x+40},520 {x+90},560" stroke="#f4efe4" stroke-width="40" fill="none"/>'
    s += "".join(blur_ell(700 + i * 40, 380 - i * 50, 40 + i * 6, 26, "#6a6a6a", 0.6, 1) for i in range(5))
    for i in range(9):
        x = 1600 + i * 70; y = 1000 - i * 50
        s += f'<ellipse cx="{x}" cy="{y}" rx="16" ry="26" fill="#1a1008" transform="rotate(40 {x} {y})"/>'
    s += G(1900, 900, 0.35, warrior_sil("stand", fill="#8a2a1a", rim=None))
    return svg(s)

@art
def izta_sleeping():
    s = sky("#4a6a9a", "#e8c8a0", "#9ab0c8")
    s += izta(100, 2300, 1000, 520, rock="#6a7690", dark="#3a4460", snow="#ffffff", seed=6)
    s += mist(1000, 120, 0.45, "#f0e0d0", 4, 14)
    s += ground(1120, "#2a3040", 20, 3) + pines(1140, 0, 2400, 50, 60, 160, "#141820", 2)
    return svg(s)

@art
def cortes_pass():
    s = sky("#1a2a40", "#9ab0c8")
    s += popo(300, 1000, 700, 760, rock="#2a3448", dark="#121a28", snow="#eef4fa", seed=5)
    s += izta(1700, 2900, 1000, 440, rock="#2a3448", dark="#121a28", snow="#e8f0f8", seed=6)
    s += '<path d="M0,1350 L0,1050 C800,960 1600,960 2400,1050 L2400,1350 Z" fill="#c8d4e0"/>'
    for i in range(6):  # horsemen silhouettes with lances
        x = 900 + i * 120; y = 1080 - i * 6
        s += (f'<g fill="#0a0c10"><ellipse cx="{x}" cy="{y-60}" rx="60" ry="24"/><path d="M{x+50},{y-70} l40,-36 l12,10 l-30,40 Z"/>'
              f'<path d="M{x-40},{y-50} l-6,50 M{x-20},{y-50} l4,50 M{x+30},{y-50} l-4,50 M{x+46},{y-50} l8,50" stroke="#0a0c10" stroke-width="9"/>'
              f'<path d="M{x-6},{y-80} l0,-46 l20,0 l0,46 Z"/><circle cx="{x+4}" cy="{y-136}" r="13"/><path d="M{x-12},{y-146} q16,-20 32,0 Z"/>'
              f'<path d="M{x+10},{y-110} L{x+80},{y-230}" stroke="#0a0c10" stroke-width="4"/></g>')
    s += mist(1050, 100, 0.4, "#e8f0f8", 5, 12)
    return svg(s)

@art
def calendar_wall():
    s = sky("#1a1008", "#3a2410") + glow(1200, 400, 900, "warm", 0.5)
    s += '<rect x="0" y="0" width="2400" height="1350" fill="#5a3a20" opacity="0.6"/>'
    for i in range(30):
        s += f'<path d="M0,{i*46} L2400,{i*46}" stroke="#3a2410" stroke-width="2" opacity="0.4"/>'
    # a calendar print on the wall: simple, original stylised volcano scene (not a copy of any painting)
    s += '<rect x="820" y="180" width="760" height="960" fill="#e8dcc0"/><rect x="850" y="210" width="700" height="620" fill="#2a3a5a"/>'
    s += f'<g transform="translate(850,210) scale(0.2917,0.4593)">{popo(700, 1350, 600, 900, rock="#4a5a7a", dark="#2a3450", snow="#fff4e8", seed=2)}{izta(1000, 2400, 1350, 500, rock="#4a5a7a", dark="#2a3450", snow="#fff0e6")}</g>'
    s += '<rect x="850" y="850" width="700" height="250" fill="#f4ecd8"/>'
    for r_ in range(4):
        for c in range(7):
            s += f'<rect x="{870+c*96}" y="{880+r_*52}" width="80" height="40" fill="none" stroke="#8a6a4a" stroke-width="2"/>'
    s += '<circle cx="1200" cy="160" r="12" fill="#1a1008"/><path d="M1200,160 L900,182 M1200,160 L1500,182" stroke="#1a1008" stroke-width="3"/>'
    s += '<rect x="0" y="1180" width="2400" height="170" fill="#1a0e06"/>' + candle(400, 1180, 90, 22) + glow(400, 1080, 260, "warm", 0.7)
    s += '<path d="M1900,1180 l0,-120 l200,0 l0,120" fill="#2a1a0e"/>'
    return svg(s)

@art
def eruption_town():
    s = sky("#0a0404", "#3a1410") + stars(60, 3, 300)
    s += plume(1200, 420, 1.6, "#4a3a38", 0.7, 6, 0.6)
    s += popo(1200, 1050, 800, 640, rock="#1a1418", dark="#08060a", snow="#8a7a80", seed=7)
    s += glow(1200, 420, 380, "red", 0.9)
    r = random.Random(3)
    for _ in range(30):  # incandescent rocks
        a = r.uniform(-2.4, -0.7); L = r.uniform(80, 320)
        s += f'<path d="M1200,420 q{math.cos(a)*L*0.5:.0f},{math.sin(a)*L:.0f} {math.cos(a)*L:.0f},{math.sin(a)*L*0.6+L*0.5:.0f}" stroke="#ff8a30" stroke-width="{r.uniform(2,5):.1f}" fill="none" opacity="0.8"/>'
    s += ground(1150, "#050203", 20, 4)
    s += city_row(1250, 6, 40, "#030102", 0.4, hscale=0.7)
    s += church(2000, 1250, 0.7, "#030102")
    return svg(s)

@art
def offering_cave():
    s = sky("#040608", "#1a1612")
    s += '<path d="M0,0 L2400,0 L2400,1350 L0,1350 Z" fill="#0a0806"/>'
    s += '<path d="M400,1350 C380,900 600,500 1200,460 C1800,500 2020,900 2000,1350 Z" fill="#1a1410"/>'
    s += glow(1200, 1000, 700, "warm", 0.6)
    s += '<rect x="800" y="1000" width="800" height="60" fill="#2a1a10"/>' + flowers(820, 1580, 990, 70, 9)
    for x in (880, 1000, 1400, 1520):
        s += candle(x, 990, 70, 16)
    s += '<path d="M1150,1000 l100,0 l-20,-60 l-60,0 Z" fill="#6a3a1a"/>'  # clay incense burner
    for i in range(10):
        t = i / 9
        s += blur_ell(1200 + 30 * math.sin(t * 6), 930 - t * 400, 30 + 100 * t, 20 + 30 * t, "#c8c0b0", round(0.35 * (1 - t), 2), 3)
    s += G(560, 1300, 0.4, woman_sil(rim="#ffb060", fill="#030202", facing=1))
    s += G(1850, 1300, 0.42, warrior_sil("stand", shield=False, weapon=False, crest=False, rim="#ffb060", fill="#030202"), True)
    return svg(s)

@art
def nahual_tease():
    s = stars_sky("#020306", "#0e1418", 200, 17, 700) + moon(1300, 700, 230, halo=3.2)
    s += ridge(980, 60, "#05080a", 4) + ground(1100, "#020304", 20, 5)
    s += pines(1120, 0, 900, 20, 200, 420, "#010203", 3) + pines(1120, 1900, 2400, 10, 200, 420, "#010203", 4)
    # coyote-like beast silhouette on a rock, glowing eyes
    s += '<path d="M1000,1100 C1100,1000 1400,1000 1500,1100 Z" fill="#010203"/>'
    s += ('<path d="M1080,1010 C1100,940 1180,900 1280,900 C1330,880 1360,840 1380,800 L1400,760 L1420,800 L1450,780 L1440,840 C1470,860 1480,880 1470,900 '
          'L1420,910 C1400,940 1390,980 1380,1010 L1350,1010 L1350,960 C1300,960 1220,960 1180,970 L1170,1010 L1140,1010 L1140,970 C1110,980 1090,1000 1080,1010 Z" fill="#010203"/>')
    s += '<path d="M1080,1000 C1020,980 990,940 1000,900" stroke="#010203" stroke-width="24" fill="none" stroke-linecap="round"/>'
    s += '<circle cx="1432" cy="830" r="30" fill="url(#redglow)"/><circle cx="1432" cy="830" r="6" fill="#ffb040"/>'
    s += '<path d="M1290,900 C1330,880 1360,840 1380,800" stroke="#8aa4c0" stroke-width="4" fill="none" opacity="0.6" filter="url(#blur1)"/>'
    return svg(s)

@art
def izta_pale():
    s = sky("#02040a", "#101c2c") + glow(1500, 400, 800, "moon", 0.6)
    s += '<rect x="1500" y="0" width="900" height="1350" fill="#0e1a2c" opacity="0.6"/>'
    s += izta_bust(1100, 540, 2.15, rim="#dfeaff", pale=True, lids=0.6, smile=-0.3)
    s += f'<g opacity="0.5">{tears(0.7).replace("<path", "<path transform=\'translate(1100,540) scale(2.15)\'").replace("<circle", "<circle transform=\'translate(1100,540) scale(2.15)\'")}</g>'
    return svg(s)

@art
def izta_night():
    s = stars_sky("#030610", "#1a2c44", 260, 21, 900) + moon(400, 260, 70)
    s += izta(100, 2300, 1000, 520, rock="#1c2a3c", dark="#0a1220", snow="#d4deea", seed=6)
    s += mist(1000, 120, 0.35, "#8aa4bc", 4, 14)
    s += ground(1120, "#03060a", 20, 3) + pines(1140, 0, 2400, 50, 60, 160, "#020407", 2)
    s += city_row(1230, 8, 30, "#020407", 0.3, hscale=0.6)
    return svg(s)

@art
def ash_city():
    s = sky("#2a2624", "#6a625a")
    s += popo(1900, 700, 380, 420, rock="#3a3434", dark="#1a1818", snow="#8a8480") + plume(1900, 290, 1.2, "#4a4440", 0.7, 3, -0.8)
    s += '<rect x="0" y="760" width="2400" height="590" fill="#3a3632"/>'
    for i in range(12):
        x = i * 220
        s += f'<rect x="{x}" y="{560 + (i*37)%120}" width="200" height="{240 - (i*37)%120}" fill="#1e1c1a"/>'
        for k in range(6):
            s += f'<rect x="{x+20+(k%3)*60}" y="{600 + (i*37)%120 + (k//3)*60}" width="30" height="30" fill="#8a7a5a" opacity="0.5"/>'
    for i, x in enumerate((300, 900, 1500, 2050)):  # parked cars covered in ash
        s += f'<path d="M{x-150},1150 L{x-120},1080 C{x-80},1030 {x+60},1030 {x+110},1080 L{x+150},1150 Z" fill="#2a2826"/><rect x="{x-160}" y="1140" width="320" height="50" rx="16" fill="#2a2826"/>'
        s += f'<path d="M{x-120},1080 C{x-80},1030 {x+60},1030 {x+110},1080" stroke="#b8b0a6" stroke-width="16" fill="none"/>'
        s += f'<circle cx="{x-90}" cy="1195" r="30" fill="#0a0a0a"/><circle cx="{x+90}" cy="1195" r="30" fill="#0a0a0a"/>'
    s += snowflakes(900, 31, 0.7).replace("#ffffff", "#9a928a")
    return svg(s)

@art
def tiemperos_slope():
    s = stars_sky("#040608", "#1a1a22", 200, 23, 700)
    s += popo(1500, 1500, 1500, 1200, rock="#1a1e26", dark="#08090c", snow="#c8ccd4", seed=9)
    s += glow(1500, 300, 260, "red", 0.4) + plume(1500, 300, 0.9, "#6a6670", 0.4, 4)
    r = random.Random(4)
    for i in range(9):  # procession with candles up the slope
        x = 300 + i * 170; y = 1340 - i * 60
        s += G(x, y, 0.22, woman_sil(rim="#ffb060", fill="#020203") if i % 2 else warrior_sil("march", shield=False, weapon=False, crest=False, rim="#ffb060", fill="#020203"))
        s += glow(x + 30, y - 160, 60, "warm", 0.9) + f'<circle cx="{x+30}" cy="{y-160}" r="5" fill="#fff0b0"/>'
    s += pines(1350, 1600, 2400, 14, 200, 420, "#010102", 5)
    return svg(s)

# ------------------------------------------------------------------ LAYERS (transparent)
@art
def l_clouds():
    r = random.Random(4); s = ""
    for _ in range(14):
        s += blur_ell(r.uniform(0, 2400), r.uniform(80, 500), r.uniform(200, 520), r.uniform(40, 90), "#8aa0b8", round(r.uniform(0.15, 0.35), 2), 3)
    return svg(s)

@art
def l_smoke():
    return svg(plume(800, 330, 1.0, "#9aa6b2", 0.55, 3, 1.0))

@art
def l_snowfall():
    return svg(snowflakes(700, 21, 0.9))

@art
def l_torch_glow():
    return svg(glow(1520, 650, 380, "warm", 0.8) + glow(1520, 650, 120, "warm", 0.9))

@art
def l_popo_carry():
    return svg(G(1000, 1180, 0.85, popo_carry(rim="#e4f0ff")))

@art
def l_popo_carry_small():
    return svg(G(900, 1250, 0.32, popo_carry(rim="#cfe4ff")))

@art
def l_torches_city():
    r = random.Random(5)
    return svg("".join(glow(r.uniform(200, 2200), r.uniform(950, 1150), r.uniform(40, 90), "warm", 0.8) for _ in range(30)))

@art
def l_brazier():
    return svg(brazier(560, 980, 1.2) + glow(560, 900, 320, "warm", 0.8) + brazier(1840, 980, 1.2) + glow(1840, 900, 320, "warm", 0.8))

@art
def l_izta_walk():
    return svg(G(900, 1270, 0.42, woman_sil(rim="#ffe0b0", fill="#e8e0d0", crown=True, dress="#f4efe4")))

@art
def l_suitors():
    s = ""
    for i, x in enumerate((700, 1000, 1400, 1700)):
        s += G(x, 1250, 0.5, warrior_sil("stand", shield=False, weapon=False, rim="#ffb060", fill="#06040a", seed=i), x > 1200)
    s += G(1200, 900, 0.36, woman_sil(rim="#ffd090", fill="#06040a", crown=True, dress="#e8e0d0"))
    return svg(s)

@art
def l_lovers():
    s = G(1020, 1180, 0.36, warrior_sil("stand", shield=False, weapon=False, rim="#cfe4ff", fill="#020406"))
    s += G(1180, 1180, 0.33, woman_sil(rim="#cfe4ff", fill="#020406", facing=-1, dress="#c8ccd4"))
    return svg(s)

@art
def l_runner():
    return svg(G(500, 1230, 0.5, warrior_sil("run", rim="#cfe4ff", fill="#020305", weapon=False)))

@art
def l_rival_run():
    return svg(G(500, 1230, 0.5, warrior_sil("run", rim="#ff8a6a", fill="#020305", weapon=False, seed=9)))

@art
def l_kneeling_warriors():
    s = G(1200, 760, 0.6, father_bust(0, 0, 1.0, rim="#ffd090"))
    for i, x in enumerate((600, 900, 1500, 1800)):
        s += G(x, 1300, 0.45, warrior_sil("kneel", rim="#ffb060", fill="#06040a", weapon=False, seed=i), x > 1200)
    return svg(s)

@art
def l_rival_kneel():
    s = G(1200, 760, 0.6, father_bust(0, 0, 1.0, rim="#ffd090"))
    s += G(900, 900, 0.36, woman_sil(rim="#ffd090", fill="#06040a", crown=True, dress="#e8e0d0"))
    s += G(1250, 1290, 0.55, warrior_sil("kneel", rim="#ff6a3a", fill="#06040a", weapon=False, shield=False, seed=9), True)
    return svg(s)

@art
def l_battle():
    r = random.Random(3); s = ""
    for i in range(10):
        x = 120 + i * 240 + r.uniform(-40, 40)
        s += G(x, 1230 + r.uniform(-30, 30), r.uniform(0.45, 0.6), warrior_sil(r.choice(["fight", "march", "fight"]), rim="#ff6a3a", fill="#050101", seed=i), i % 2 == 1)
    for _ in range(20):  # arrows in the sky
        x = r.uniform(0, 2400); y = r.uniform(200, 700)
        s += f'<path d="M{x:.0f},{y:.0f} l60,20" stroke="#050101" stroke-width="4"/>'
    return svg(s)

@art
def l_rival_sneak():
    return svg(G(1500, 1240, 0.42, warrior_sil("march", rim="#ff8a6a", fill="#020203", shield=False, weapon=False, seed=9), True))

@art
def l_candles():
    s = ""
    for x in (300, 520, 1900, 2120):
        s += candle(x, 1250, 80, 18) + glow(x, 1170, 200, "warm", 0.7)
    return svg(s)

@art
def l_crowd_silent():
    r = random.Random(7); s = ""
    for i in range(16):
        x = 100 + i * 150 + r.uniform(-30, 30)
        if 900 < x < 1500: continue
        s += G(x, 1300, r.uniform(0.38, 0.46), woman_sil(rim="#cfe4ff", fill="#05060a", facing=1 if x < 1200 else -1) if i % 2 else warrior_sil("stand", shield=False, weapon=False, crest=False, rim="#cfe4ff", fill="#05060a"), x > 1200)
    return svg(s)

@art
def l_eruption_glow():
    return svg(glow(1200, 420, 520, "red", 0.7))

IZ_PROF = [(0.0, 0.0), (0.06, 0.28), (0.12, 0.5), (0.18, 0.62), (0.22, 0.66), (0.27, 0.62), (0.33, 0.74), (0.38, 0.86), (0.42, 0.82),
           (0.48, 0.8), (0.55, 0.92), (0.6, 1.0), (0.66, 0.98), (0.71, 0.9), (0.75, 0.84), (0.79, 0.86), (0.83, 0.8), (0.87, 0.72),
           (0.9, 0.74), (0.93, 0.62), (0.97, 0.3), (1.0, 0.0)]

@art
def l_izta_outline():
    """Ghostly outline of the sleeping woman along the izta_sleeping ridge (feet left, head right)."""
    x0, x1, base, h = 100, 2300, 1000, 520
    P = lambda u, v, lift=34: (x0 + (x1 - x0) * u, base - h * v - lift)
    pts = [P(u, v) for u, v in IZ_PROF[2:-2]]
    d = "M" + " L".join(f"{x:.0f},{y:.0f}" for x, y in pts)
    s = f'<path d="{d}" fill="none" stroke="#ffffff" stroke-width="9" opacity="0.85" filter="url(#ghost)" stroke-linejoin="round"/>'
    hx, hy = P(0.885, 0.76, 60)
    s += f'<ellipse cx="{hx:.0f}" cy="{hy:.0f}" rx="70" ry="52" fill="none" stroke="#ffffff" stroke-width="7" opacity="0.7" filter="url(#ghost)"/>'
    for u, v, t in ((0.885, 0.76, "CABEZA"), (0.6, 1.0, "PECHO"), (0.38, 0.86, "RODILLAS"), (0.2, 0.64, "PIES")):
        x, y = P(u, v, 110)
        s += f'<text x="{x:.0f}" y="{y:.0f}" font-family="Cinzel" font-size="48" fill="#ffffff" opacity="0.9" text-anchor="middle" filter="url(#ghost)">{t}</text>'
    return svg(s)


if __name__ == "__main__":
    os.makedirs("art", exist_ok=True)
    names = sys.argv[1:] or list(ART)
    for n in names:
        open(f"art/{n}.svg", "w").write(ART[n]())
    print(len(names), "svg written")
