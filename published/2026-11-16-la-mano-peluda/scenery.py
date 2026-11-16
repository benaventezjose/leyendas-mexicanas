"""Shared scenery helpers (from the previous videos)."""
import math, random, sys
sys.path.insert(0, "/home/claude/pipeline")
from art import *
from base_chars import uid

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

