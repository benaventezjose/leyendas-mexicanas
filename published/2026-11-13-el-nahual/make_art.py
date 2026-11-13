#!/usr/bin/env python3
"""Illustrations for 'El Nahual' — writes art/*.svg (2400x1350).
Render: node /home/claude/pipeline/render_svg.js art/*.svg      Usage: python3 make_art.py [name ...]"""
import sys, os, math, random
sys.path.insert(0, '/home/claude/pipeline'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from art import *
from scenery import *
from chars import *

ART = {}
def art(fn):
    ART[fn.__name__] = fn
    return fn

G = lambda x, y, k, f, flip=False: f'<g transform="translate({x},{y}) scale({-k if flip else k},{k})">{f}</g>'
R = lambda c="#000", op=1.0: f'<rect width="2400" height="1350" fill="{c}" opacity="{op}"/>'

# ------------------------------------------------------------------ village pieces
def tile_house(x, base, w=420, h=230, wall="#1a1c22", roof="#2a1612", lit=True, cross=False, door_lit=False, seed=1, rim="#7a9cc4", scratched=False):
    r = random.Random(seed)
    s = f'<rect x="{x-w/2:.0f}" y="{base-h:.0f}" width="{w}" height="{h}" fill="{wall}"/>'
    for _ in range(int(w / 30)):  # adobe blocks / cracked plaster
        bx = r.uniform(x - w / 2, x + w / 2 - 40); by = r.uniform(base - h + 20, base - 10)
        s += f'<rect x="{bx:.0f}" y="{by:.0f}" width="{r.uniform(30,60):.0f}" height="{r.uniform(14,22):.0f}" fill="#000" opacity="0.18"/>'
    # tile roof with overhang
    s += f'<path d="M{x-w/2-50:.0f},{base-h+10:.0f} L{x-w/2+20:.0f},{base-h-90:.0f} L{x+w/2-20:.0f},{base-h-90:.0f} L{x+w/2+50:.0f},{base-h+10:.0f} Z" fill="{roof}"/>'
    for i in range(int(w / 26) + 4):
        tx = x - w / 2 - 40 + i * 26
        s += f'<path d="M{tx:.0f},{base-h+8:.0f} L{tx+16:.0f},{base-h-86:.0f}" stroke="#000" stroke-width="4" opacity="0.35"/>'
    s += f'<path d="M{x-w/2+20:.0f},{base-h-90:.0f} L{x+w/2-20:.0f},{base-h-90:.0f}" stroke="{rim}" stroke-width="3" opacity="0.5"/>'
    # door + window
    dx = x - w * 0.18
    s += f'<rect x="{dx-38:.0f}" y="{base-150:.0f}" width="76" height="150" fill="{"#e8a050" if door_lit else "#2a1a10"}"/>'
    s += f'<rect x="{dx-38:.0f}" y="{base-150:.0f}" width="76" height="150" fill="none" stroke="#0a0604" stroke-width="6"/>'
    for i in range(4):
        s += f'<path d="M{dx-38+i*19:.0f},{base-150:.0f} l0,150" stroke="#0a0604" stroke-width="2" opacity="0.6"/>'
    wx = x + w * 0.22
    s += f'<rect x="{wx-40:.0f}" y="{base-170:.0f}" width="80" height="70" fill="{"#ffc865" if lit else "#06080c"}"/>'
    s += f'<path d="M{wx:.0f},{base-170:.0f} l0,70 M{wx-40:.0f},{base-135:.0f} l80,0" stroke="#0a0604" stroke-width="6"/>'
    if lit:
        s += glow(wx, base - 135, 150, "warm", 0.6)
    if cross:
        for cx_ in (dx, wx):
            cy_ = base - 205 if cx_ == dx else base - 205
            s += f'<path d="M{cx_-6:.0f},{cy_-34:.0f} l12,0 l0,22 l20,0 l0,12 l-20,0 l0,34 l-12,0 l0,-34 l-20,0 l0,-12 l20,0 Z" fill="#eef0f2"/>'
    s += f'<path d="M{x-w/2:.0f},{base-h:.0f} L{x-w/2:.0f},{base:.0f}" stroke="{rim}" stroke-width="4" opacity="0.4"/>'
    return s


def reed_hut(x, base, k=1.0, glow_=True, ruin=False, door=True):
    s = ""
    w, h = 520 * k, 300 * k
    if not ruin:
        s += f'<rect x="{x-w/2:.0f}" y="{base-h:.0f}" width="{w:.0f}" height="{h:.0f}" fill="#0c0a08"/>'
        for i in range(int(w / (14 * k))):
            xx = x - w / 2 + i * 14 * k
            s += f'<path d="M{xx:.0f},{base-h:.0f} l0,{h:.0f}" stroke="#000" stroke-width="{4*k:.1f}"/>'
            if glow_ and i % 3 == 1:
                s += f'<path d="M{xx+7*k:.0f},{base-h+10:.0f} l0,{h-20:.0f}" stroke="#ff5a1a" stroke-width="{2.4*k:.1f}" opacity="{0.35+0.4*((i*7)%5)/5:.2f}"/>'
        # thatched (zacate) roof
        s += f'<path d="M{x-w/2-80*k:.0f},{base-h+30*k:.0f} L{x:.0f},{base-h-230*k:.0f} L{x+w/2+80*k:.0f},{base-h+30*k:.0f} Z" fill="#14100a"/>'
        rr = random.Random(3)
        for i in range(70):
            u = rr.uniform(-1, 1)
            s += f'<path d="M{x+u*(w/2+80*k):.0f},{base-h+30*k:.0f} L{x+u*20*k:.0f},{base-h-200*k:.0f}" stroke="#2a2214" stroke-width="2" opacity="0.6"/>'
        if door:
            s += f'<rect x="{x-50*k:.0f}" y="{base-200*k:.0f}" width="{100*k:.0f}" height="{200*k:.0f}" fill="{"#d84a12" if glow_ else "#050403"}" opacity="0.9"/>'
        if glow_:
            s += glow(x, base - 100 * k, 380 * k, "red", 0.55)
    else:
        for i in range(18):
            rr = random.Random(i)
            xx = x - w / 2 + i * w / 18
            s += f'<path d="M{xx:.0f},{base:.0f} l{rr.uniform(-40,40):.0f},{-rr.uniform(40,180)*k:.0f}" stroke="#0c0a08" stroke-width="{8*k:.0f}" stroke-linecap="round"/>'
        s += f'<path d="M{x-w/2:.0f},{base:.0f} L{x-w/4:.0f},{base-120*k:.0f} L{x+w/3:.0f},{base-40*k:.0f} L{x+w/2:.0f},{base:.0f} Z" fill="#100c08"/>'
    return s


def fence(x0, x1, y, h=170, color="#07080b", rim="#7a9cc4", seed=2, gap=None):
    r = random.Random(seed); s = ""
    x = x0
    while x < x1:
        hh = h * r.uniform(0.85, 1.1)
        if not (gap and gap[0] < x < gap[1]):
            s += f'<path d="M{x:.0f},{y:.0f} L{x+r.uniform(-6,6):.0f},{y-hh:.0f}" stroke="{color}" stroke-width="22" stroke-linecap="round"/>'
            s += f'<path d="M{x-8:.0f},{y-hh+6:.0f} l0,{hh*0.6:.0f}" stroke="{rim}" stroke-width="3" opacity="0.35"/>'
        x += r.uniform(90, 130)
    for yy in (y - h * 0.35, y - h * 0.75):
        s += f'<path d="M{x0:.0f},{yy:.0f} L{x1:.0f},{yy+r.uniform(-10,10):.0f}" stroke="{color}" stroke-width="12"/>'
    return s


def hen(x, y, k=1.0, color="#06070a", dead=False, turkey=False):
    if turkey:
        b = (f'M{-80*k},{-40*k} C{-120*k},{-140*k} {-40*k},{-200*k} {10*k},{-150*k} C{30*k},{-200*k} {50*k},{-230*k} {60*k},{-220*k} '
             f'C{80*k},{-210*k} {70*k},{-170*k} {60*k},{-140*k} C{90*k},{-110*k} {100*k},{-40*k} {40*k},0 L{-40*k},0 Z')
        return f'<path d="{b}" fill="{color}" transform="translate({x},{y})"/>'
    if dead:
        b = f'M{-60*k},0 C{-60*k},{-40*k} {40*k},{-50*k} {70*k},{-20*k} L{100*k},{-10*k} L{70*k},0 Z'
        return (f'<g transform="translate({x},{y}) rotate({(x*7)%40-20})"><path d="{b}" fill="{color}"/>'
                f'<path d="M{-60*k},0 L{-90*k},{-30*k} M{-60*k},0 L{-96*k},{-6*k}" stroke="{color}" stroke-width="{8*k:.0f}"/></g>')
    b = (f'M{-60*k},{-20*k} C{-90*k},{-80*k} {-70*k},{-120*k} {-40*k},{-90*k} C{-10*k},{-70*k} {20*k},{-80*k} {30*k},{-110*k} '
         f'C{40*k},{-140*k} {70*k},{-140*k} {72*k},{-110*k} L{92*k},{-100*k} L{70*k},{-92*k} C{70*k},{-60*k} {50*k},{-10*k} 0,0 Z')
    return f'<path d="{b}" fill="{color}" transform="translate({x},{y})"/><path d="M{x},{y} l-10,30 M{x+10},{y} l10,30" stroke="{color}" stroke-width="5"/>'


def feathers(x0, x1, y0, y1, n=80, seed=3, col="#c8c0b0"):
    r = random.Random(seed); s = ""
    for _ in range(n):
        x = r.uniform(x0, x1); y = r.uniform(y0, y1); a = r.uniform(0, 360); L = r.uniform(16, 40)
        s += f'<path d="M0,0 C{L*0.3:.0f},{-L*0.25:.0f} {L*0.7:.0f},{-L*0.2:.0f} {L:.0f},0 C{L*0.7:.0f},{L*0.2:.0f} {L*0.3:.0f},{L*0.25:.0f} 0,0 Z" fill="{col}" opacity="{r.uniform(0.4,0.85):.2f}" transform="translate({x:.0f},{y:.0f}) rotate({a:.0f})"/>'
    return s


def paw(x, y, k=1.0, col="#05060a", op=0.85, ang=0):
    s = f'<ellipse cx="0" cy="20" rx="34" ry="28" fill="{col}"/>'
    for dx, dy in ((-34, -24), (-12, -42), (12, -42), (34, -24)):
        s += f'<ellipse cx="{dx}" cy="{dy}" rx="12" ry="16" fill="{col}"/><path d="M{dx},{dy-16} l{dx*0.1:.0f},-14" stroke="{col}" stroke-width="5"/>'
    return f'<g transform="translate({x},{y}) rotate({ang}) scale({k})" opacity="{op}">{s}</g>'


def footprint_human(x, y, k=1.0, col="#05060a", op=0.85, ang=0):
    s = '<path d="M-22,60 C-34,20 -30,-30 -14,-56 C0,-74 22,-66 26,-40 C30,-10 24,30 22,60 C16,80 -16,80 -22,60 Z" fill="' + col + '"/>'
    for i, (dx, dy, rr) in enumerate(((-18, -84, 11), (0, -92, 9), (14, -88, 8), (24, -78, 7), (32, -64, 6))):
        s += f'<circle cx="{dx}" cy="{dy}" r="{rr}" fill="{col}"/>'
    return f'<g transform="translate({x},{y}) rotate({ang}) scale({k})" opacity="{op}">{s}</g>'


def fogon(x, y, k=1.0, fire=True, embers_only=False):
    """Three-stone hearth (tenamaxtles) with comal and fire."""
    s = ""
    for dx in (-90, 0, 90):
        s += f'<ellipse cx="{x+dx*k:.0f}" cy="{y:.0f}" rx="{48*k:.0f}" ry="{40*k:.0f}" fill="#1a1410"/><path d="M{x+dx*k-40*k:.0f},{y-12*k:.0f} q{40*k:.0f},{-30*k:.0f} {80*k:.0f},0" stroke="#ff8a3a" stroke-width="{4*k:.0f}" fill="none" opacity="0.6"/>'
    s += f'<ellipse cx="{x:.0f}" cy="{y+20*k:.0f}" rx="{150*k:.0f}" ry="{30*k:.0f}" fill="#ff6a1a" opacity="0.35" filter="url(#blur2)"/>'
    r = random.Random(5)
    for _ in range(26):
        s += f'<circle cx="{x+r.uniform(-110,110)*k:.0f}" cy="{y+r.uniform(0,30)*k:.0f}" r="{r.uniform(3,8)*k:.1f}" fill="{r.choice(["#ff8a2a","#ffcf5a","#c8320a"])}"/>'
    if fire and not embers_only:
        s += brazier(x, y - 10 * k, 1.3 * k).split('<path', 1)[1].join(['<path', '']) if False else ""
        for i in range(7):
            dx = (i - 3) * 26 * k; hh = (170 - abs(i - 3) * 34) * k
            s += f'<path d="M{x+dx-22*k:.0f},{y-10*k:.0f} C{x+dx-30*k:.0f},{y-hh*0.5:.0f} {x+dx+12*k:.0f},{y-hh*0.7:.0f} {x+dx:.0f},{y-hh:.0f} C{x+dx+30*k:.0f},{y-hh*0.6:.0f} {x+dx+26*k:.0f},{y-30*k:.0f} {x+dx+22*k:.0f},{y-10*k:.0f} Z" fill="{"#ff9a2a" if i%2 else "#ffb84a"}" opacity="0.9"/>'
        s += f'<path d="M{x-30*k:.0f},{y-10*k:.0f} C{x-30*k:.0f},{y-80*k:.0f} {x:.0f},{y-110*k:.0f} {x:.0f},{y-140*k:.0f} C{x+20*k:.0f},{y-90*k:.0f} {x+30*k:.0f},{y-50*k:.0f} {x+30*k:.0f},{y-10*k:.0f} Z" fill="#fff0b0"/>'
        s += glow(x, y - 70 * k, 520 * k, "warm", 0.9)
    return s


def interior(wall="#3a2418", floor="#1a100a", lit=(1200, 1000), seed=4):
    """Adobe hut interior lit by a low fire: back wall with rough plaster, beams, hanging herbs, floor."""
    r = random.Random(seed)
    g = uid("iw")
    s = (f'<defs><radialGradient id="{g}" cx="{lit[0]/2400:.2f}" cy="{lit[1]/1350:.2f}" r="0.8">'
         f'<stop offset="0" stop-color="#8a4a22"/><stop offset="0.35" stop-color="{wall}"/><stop offset="1" stop-color="#07050a"/></radialGradient></defs>')
    s += f'<rect width="2400" height="1350" fill="url(#{g})"/>'
    for _ in range(90):
        x = r.uniform(0, 2400); y = r.uniform(0, 1000)
        s += f'<path d="M{x:.0f},{y:.0f} l{r.uniform(-60,60):.0f},{r.uniform(10,50):.0f}" stroke="#000" stroke-width="{r.uniform(1,3):.1f}" opacity="0.25"/>'
    s += f'<path d="M0,1040 L2400,1000 L2400,1350 L0,1350 Z" fill="{floor}"/>'
    for i in range(5):
        s += f'<rect x="0" y="{40+i*8}" width="2400" height="34" fill="#0c0806" transform="rotate({-0.5+i*0.2} 1200 60)" opacity="0.9"/>' if i == 0 else ""
    s += '<rect x="0" y="40" width="2400" height="46" fill="#0c0806"/>'
    for x in range(100, 2400, 380):
        s += f'<rect x="{x}" y="0" width="40" height="90" fill="#0c0806"/>'
    return s


def herbs_hanging(x, y, k=1.0, seed=1):
    r = random.Random(seed); s = f'<path d="M{x},{y-80*k} L{x},{y}" stroke="#2a1a0e" stroke-width="3"/>'
    for i in range(14):
        a = r.uniform(-30, 30); L = r.uniform(80, 160) * k
        s += f'<path d="M{x},{y} q{a*0.6:.0f},{L*0.5:.0f} {a:.0f},{L:.0f}" stroke="#1c2a12" stroke-width="{r.uniform(3,6):.0f}" fill="none"/>'
        s += f'<ellipse cx="{x+a:.0f}" cy="{y+L:.0f}" rx="10" ry="5" fill="#2a3a18" transform="rotate({a} {x+a:.0f} {y+L:.0f})"/>'
    return s


def man_sil(x, y, h=700, hat=True, machete=False, lantern=False, color=SIL, rim="#9fc2e8", facing=1, pose="stand", bag=False):
    k = h / 1000
    d = ("M-44,-930 C-48,-985 48,-985 44,-930 L50,-880 C70,-862 120,-840 130,-780 L150,-500 L118,-490 L110,-430 "
         "L86,0 L22,0 L6,-390 L-6,-390 L-22,0 L-86,0 L-110,-430 L-118,-490 L-150,-500 L-130,-780 C-120,-840 -70,-862 -50,-880 Z")
    if pose == "crouch":
        d = ("M-44,-640 C-48,-695 48,-695 44,-640 L50,-590 C80,-570 140,-540 150,-470 L170,-260 L130,-250 L150,0 L80,0 L60,-200 "
             "L-40,-220 L-60,0 L-130,0 L-110,-260 L-140,-280 L-130,-480 C-120,-540 -80,-570 -50,-590 Z")
    if pose == "climb":
        d = ("M-24,-930 C-28,-985 68,-985 64,-930 L70,-880 C100,-860 150,-830 160,-760 L170,-520 L134,-510 L150,-300 L200,-200 L190,0 L130,0 L120,-180 "
             "L40,-320 L-40,-160 L-110,0 L-170,-20 L-100,-200 L-90,-440 L-120,-480 L-100,-770 C-90,-840 -50,-862 -30,-880 Z")
    top = -930 if pose != "crouch" else -640
    s = ""
    if rim:
        s += f'<path d="{d}" fill="{rim}" filter="url(#blur2)" opacity="0.7"/>'
    s += f'<path d="{d}" fill="{color}"/>'
    if hat:
        s += f'<path d="M-170,{top-30} C-110,{top-56} 110,{top-56} 170,{top-30} C110,{top-12} -110,{top-12} -170,{top-30} Z M-56,{top-34} C-58,{top-130} 58,{top-130} 56,{top-34} Z" fill="{color}"/>'
        if rim:
            s += f'<path d="M-170,{top-30} C-110,{top-56} 110,{top-56} 170,{top-30}" stroke="{rim}" stroke-width="5" fill="none" opacity="0.6"/>'
    if machete:
        s += f'<path d="M140,-500 L200,-520 L420,-700 C440,-716 450,-700 436,-684 L230,-480 Z" fill="#1a1c22"/><path d="M220,-520 L428,-694" stroke="#dfe8f4" stroke-width="5" opacity="0.8"/>'
    if lantern:
        s += f'<path d="M-140,-480 L-140,-420" stroke="{color}" stroke-width="6"/><rect x="-170" y="-420" width="60" height="80" rx="8" fill="#ffc865"/>'
        s += f'<circle cx="-140" cy="-380" r="160" fill="url(#warmglow)" opacity="0.8"/>'
    if bag:
        s += f'<path d="M100,-760 C180,-700 200,-560 160,-470 C120,-440 60,-470 70,-560 Z" fill="{color}"/>'
    fl = "" if facing > 0 else " scale(-1,1)"
    return f'<g transform="translate({x},{y}) scale({k}){fl}">{s}</g>'


def woman_sil(x, y, h=650, color=SIL, rim="#9fc2e8", facing=1, pot=False):
    k = h / 1000
    d = ("M0,-1000 C-56,-1000 -86,-956 -88,-896 C-92,-830 -130,-790 -150,-690 C-180,-500 -210,-250 -230,0 L230,0 "
         "C210,-250 180,-500 150,-690 C130,-790 92,-830 88,-896 C86,-956 56,-1000 0,-1000 Z")
    s = (f'<path d="{d}" fill="{rim}" filter="url(#blur2)" opacity="0.7"/>' if rim else "") + f'<path d="{d}" fill="{color}"/>'
    s += f'<path d="M-150,-690 C-200,-600 -230,-480 -250,-380 L-200,-380 C-180,-480 -150,-580 -120,-640 Z" fill="{color}"/>'  # rebozo end
    if pot:
        s += f'<ellipse cx="170" cy="-520" rx="90" ry="70" fill="{color}"/><path d="M110,-580 L230,-580" stroke="{color}" stroke-width="20"/>'
    fl = "" if facing > 0 else " scale(-1,1)"
    return f'<g transform="translate({x},{y}) scale({k}){fl}">{s}</g>'


def cross_cal(x, y, s_=1.0, scratched=False, col="#f0f2f4"):
    k = s_
    d = f"M{x-14*k},{y-120*k} l{28*k},0 l0,{60*k} l{50*k},0 l0,{28*k} l{-50*k},0 l0,{110*k} l{-28*k},0 l0,{-110*k} l{-50*k},0 l0,{-28*k} l{50*k},0 Z"
    s = f'<path d="{d}" fill="{col}" opacity="0.92"/>'
    s += f'<path d="{d}" fill="none" stroke="#9aa4ae" stroke-width="{3*k}" opacity="0.5"/>'
    r = random.Random(int(x))
    for _ in range(14):  # brush drips
        xx = x + r.uniform(-60, 60) * k; yy = y + r.uniform(-40, 70) * k
        s += f'<path d="M{xx:.0f},{yy:.0f} l0,{r.uniform(8,30)*k:.0f}" stroke="{col}" stroke-width="{3*k:.1f}" opacity="0.6"/>'
    if scratched:
        for i in range(4):
            x0 = x - 70 * k + i * 34 * k
            s += f'<path d="M{x0:.0f},{y-170*k:.0f} C{x0+20*k:.0f},{y-60*k:.0f} {x0+10*k:.0f},{y+60*k:.0f} {x0+40*k:.0f},{y+170*k:.0f}" stroke="#0a0604" stroke-width="{14*k:.0f}" fill="none" stroke-linecap="round"/>'
            s += f'<path d="M{x0+6*k:.0f},{y-160*k:.0f} C{x0+26*k:.0f},{y-60*k:.0f} {x0+16*k:.0f},{y+60*k:.0f} {x0+46*k:.0f},{y+160*k:.0f}" stroke="#c8a888" stroke-width="{3*k:.1f}" fill="none" opacity="0.6"/>'
    return s


def wood_door(x0=600, y0=80, x1=1800, y1=1350, col="#3a2416"):
    s = f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" fill="{col}"/>'
    r = random.Random(4); n = 7; w = (x1 - x0) / n
    for i in range(n):
        s += f'<rect x="{x0+i*w:.0f}" y="{y0}" width="{w-6:.0f}" height="{y1-y0}" fill="#000" opacity="{r.uniform(0.05,0.3):.2f}"/>'
        for _ in range(10):
            yy = r.uniform(y0, y1)
            s += f'<path d="M{x0+i*w+8:.0f},{yy:.0f} q{w*0.4:.0f},{r.uniform(-20,20):.0f} {w-20:.0f},{r.uniform(-10,10):.0f}" stroke="#1a0e08" stroke-width="2" fill="none" opacity="0.5"/>'
        s += f'<path d="M{x0+i*w+w-6:.0f},{y0} l0,{y1-y0}" stroke="#0a0604" stroke-width="6"/>'
    for yy in (y0 + 200, y1 - 260):
        s += f'<rect x="{x0}" y="{yy}" width="{x1-x0}" height="60" fill="#24160c"/>'
        for i in range(n):
            s += f'<circle cx="{x0+i*w+w/2:.0f}" cy="{yy+30}" r="9" fill="#0a0806"/>'
    return s


def moon_sky(seed=1, mx=1750, my=300, r=110, top="#03060e", bot="#16283a", n=220):
    return stars_sky(top, bot, n, seed, 800) + moon(mx, my, r)


def far_hills(y=900, seed=3):
    return ridge(y - 120, 160, "#0c1622", seed) + ridge(y, 110, "#070d15", seed + 3)

# ================================================================== SCENES
@art
def village_night():
    s = moon_sky(1, 1900, 260, 120) + ridge(760, 260, "#0a121c", 2) + ridge(880, 120, "#060b12", 5)
    s += mist(860, 90, 0.18, "#9ab4cc", 2)
    s += tile_house(500, 1130, 460, 220, seed=1) + tile_house(1080, 1110, 380, 200, lit=False, seed=2) + tile_house(1640, 1140, 520, 240, seed=3)
    s += tile_house(2200, 1120, 360, 200, lit=False, seed=4)
    s += church(1300, 960, 0.55)
    s += ground(1140, "#05070a", 16, 4)
    s += maguey(180, 1250, 1.4, rim="#7a9cc4") + maguey(2250, 1280, 1.6, rim="#7a9cc4", seed=3) + nopal(880, 1250, 1.2)
    s += f'<path d="M1000,1350 C1100,1250 1250,1200 1300,1150" stroke="#1a2230" stroke-width="80" fill="none" opacity="0.6"/>'
    return svg(s)


@art
def village_dawn():
    s = sky("#2a3a52", "#e8a070", "#7a6a80") + ridge(760, 260, "#3a4458", 2) + ridge(880, 120, "#262c3a", 5)
    s += mist(860, 90, 0.35, "#f0d0c0", 2)
    s += tile_house(500, 1130, 460, 220, wall="#3a3434", roof="#4a2418", seed=1, lit=False, cross=True, rim="#ffb080")
    s += tile_house(1080, 1110, 380, 200, wall="#34302e", roof="#42200e", lit=False, seed=2, cross=True, rim="#ffb080")
    s += tile_house(1640, 1140, 520, 240, wall="#3a3434", roof="#4a2418", seed=3, lit=False, rim="#ffb080")
    s += church(1300, 960, 0.55, "#2a2a34", False)
    s += ground(1140, "#1a1614", 16, 4)
    s += maguey(180, 1250, 1.4, "#14181a") + maguey(2250, 1280, 1.6, "#14181a", 3)
    return svg(s)


@art
def hill_moon():
    s = moon_sky(2, 1500, 330, 150, "#02040a", "#142436")
    s += ridge(700, 330, "#03060a", 9, 0.7) + mist(980, 120, 0.25, "#8aa4c0", 4)
    s += ground(1180, "#020305", 30, 3)
    for i, x in enumerate((200, 420, 760, 1900, 2150)):
        s += maguey(x, 1220 + (i % 2) * 40, 1.3 + (i % 3) * 0.2, "#020305", i, "#7a9cc4")
    return svg(s)


@art
def title_bg():
    s = moon_sky(4, 1850, 330, 220, "#010206", "#0c1626", 260)
    s += ridge(1050, 120, "#020306", 5) + ground(1180, "#010203", 14, 2)
    s += G(900, 1170, 0.8, beast_body(rim="#9fc2e8", eyes=True, head_low=False))
    s += maguey(220, 1270, 1.5, "#010203", 2, "#6a8cb4") + maguey(2150, 1260, 1.7, "#010203", 3, "#6a8cb4")
    return svg(s)


@art
def crosses_doors():
    s = sky("#05080e", "#18283a") + moon(300, 200, 80)
    s += tile_house(500, 1220, 700, 520, cross=True, seed=6, lit=True) + tile_house(1450, 1240, 780, 560, cross=True, seed=7, lit=False)
    s += tile_house(2250, 1220, 520, 480, cross=True, seed=8, lit=True)
    s += ground(1230, "#06080c", 10, 3)
    s += candle(820, 1215, 50) + glow(820, 1180, 120, "warm", 0.8) + candle(1700, 1230, 50) + glow(1700, 1200, 120, "warm", 0.8)
    return svg(s)


@art
def couple_dawn():
    s = sky("#3a4a66", "#f0b070", "#9a7a8a") + ridge(820, 240, "#4a5268", 3) + ridge(940, 140, "#2c3244", 6)
    s += mist(900, 100, 0.35, "#ffd8c0", 1)
    # milpa rows on the slope
    for i in range(40):
        x = 60 + i * 60
        s += f'<path d="M{x},1300 L{x+10},{1060 - (i%5)*8}" stroke="#1a2014" stroke-width="7"/><path d="M{x+10},{1100-(i%5)*8} l-40,-30 M{x+8},{1150-(i%5)*8} l40,-30" stroke="#1a2014" stroke-width="5"/>'
    s += tile_house(1900, 1180, 420, 210, wall="#3a3434", roof="#4a2418", lit=False, rim="#ffb080")
    s += ground(1200, "#14100c", 20, 3)
    s += man_sil(900, 1260, 640, rim="#ffb070", bag=True) + woman_sil(1180, 1260, 560, rim="#ffb070", facing=-1, pot=True)
    s += hen(1400, 1250, 0.7, "#14100c") + hen(1500, 1270, 0.6, "#14100c") + hen(1600, 1240, 0.9, "#14100c", turkey=True)
    return svg(s)


@art
def lupe_portrait():
    s = sky("#2a3a52", "#c8906a") + tile_house(1900, 1200, 700, 600, wall="#2a2624", roof="#3a1a10", lit=False, rim="#ffb080")
    s += f'<rect width="2400" height="1350" fill="#000" opacity="0.25"/>'
    s += lupe_bust(1150, 560, 2.2, rim="#ffcf9a", smile=0.45, look=0.2)
    return svg(s)


@art
def lupe_scared():
    s = R("#07080e") + glow(700, 700, 900, "warm", 0.5)
    s += lupe_bust(1200, 560, 2.3, rim="#9fc2e8", fear=True, look=0.8, turn=0.15)
    return svg(s)


@art
def lupe_window():
    s = R("#06070c") + window(1700, 300, 520, 700, lit=False, arch=False)
    s += f'<rect x="1440" y="300" width="520" height="700" fill="#16283a"/>' + moon(1800, 470, 70) + stars(60, 3, 900)
    s += f'<path d="M1700,300 l0,700 M1440,650 l520,0" stroke="#05070a" stroke-width="22"/>'
    s += lupe_bust(1000, 560, 2.1, rim="#9fc2e8", look=0.9, turn=0.3, smile=0.0, lids=0.1)
    s += candle(600, 1180, 70) + glow(600, 1120, 320, "warm", 0.9)
    return svg(s)


@art
def altar_candle():
    s = interior("#2a1a12", "#120a06", (1200, 700))
    s += '<rect x="700" y="760" width="1000" height="420" fill="#1c120a"/><rect x="680" y="740" width="1040" height="30" fill="#2a1a0e"/>'
    s += papel_picado(120, "#8a1a2a", 6, 3, 0.7)
    # saint image (generic, framed), vase of cempasúchil, glass of water, candle
    s += '<rect x="1060" y="360" width="280" height="370" fill="#3a2a14"/><rect x="1080" y="380" width="240" height="330" fill="#1a2a3a"/>'
    s += '<path d="M1200,420 C1160,420 1150,470 1160,500 C1130,520 1120,600 1110,700 L1290,700 C1280,600 1270,520 1240,500 C1250,470 1240,420 1200,420 Z" fill="#6a5a8a" opacity="0.8"/>'
    s += '<circle cx="1200" cy="450" r="60" fill="none" stroke="#f4d47a" stroke-width="5" opacity="0.7"/>'
    s += flowers(820, 960, 700, 18, 3)
    s += '<path d="M1450,740 L1440,640 L1520,640 L1510,740 Z" fill="#9ab8d0" opacity="0.5"/><path d="M1446,670 L1514,670" stroke="#dfeaf4" stroke-width="3" opacity="0.6"/>'
    s += candle(1300, 740, 80) + glow(1300, 650, 380, "warm", 1.0)
    return svg(s)


@art
def corral_dawn():
    s = sky("#2a3a52", "#a8b8c8", "#6a7a90") + far_hills(820, 4).replace("#0c1622", "#3a4a5a").replace("#070d15", "#2a3442")
    s += mist(900, 120, 0.4, "#d8e2ea", 3)
    s += ground(1060, "#1c2026", 16, 3) + fence(0, 2400, 1080, 200, "#14161a", "#d8e2ea")
    s += tile_house(2100, 1060, 440, 240, wall="#2a2a2e", roof="#3a1e14", lit=False, rim="#d8e2ea")
    s += woman_sil(700, 1260, 600, "#0c0e12", "#d8e2ea", 1, True)
    s += feathers(900, 1900, 1150, 1330, 70, 4)
    for x in (1100, 1350, 1600, 1800):
        s += hen(x, 1250 + (x % 7) * 6, 0.9, "#0c0e12", dead=True)
    return svg(s)


@art
def dead_hens():
    s = R("#1a1e24") + f'<rect y="0" width="2400" height="500" fill="#2a3440"/>' + fence(0, 2400, 520, 400, "#0c0e12", "#c8d4e0")
    s += mist(500, 100, 0.35, "#d8e2ea", 5)
    r = random.Random(8)
    for i in range(9):
        s += hen(r.uniform(200, 2200), r.uniform(800, 1250), r.uniform(1.6, 2.4), "#0a0c10", dead=True)
    s += feathers(0, 2400, 650, 1350, 260, 9, "#d8d0c4")
    s += paw(1300, 1120, 1.8, "#05060a", 0.8, 10) + paw(1700, 980, 1.7, "#05060a", 0.75, 14)
    return svg(s)


@art
def tracks_mud():
    s = R("#20242a")
    r = random.Random(3)
    for _ in range(200):
        s += f'<ellipse cx="{r.uniform(0,2400):.0f}" cy="{r.uniform(0,1350):.0f}" rx="{r.uniform(20,90):.0f}" ry="{r.uniform(8,30):.0f}" fill="{r.choice(["#14181c","#2c3036","#1a1d22"])}" opacity="0.7"/>'
    for i in range(5):
        s += paw(380 + i * 420, 1000 - i * 140 + (i % 2) * 120, 2.6, "#07080a", 0.9, 70)
    s += f'<path d="M0,0 L2400,0 L2400,1350 L0,1350 Z" fill="url(#moonglow)" opacity="0.15"/>'
    s += hen(300, 300, 1.0, "#0a0c10", dead=True) + feathers(0, 2400, 0, 1350, 50, 2, "#d8d0c4")
    return svg(s)


@art
def footprint():
    s = R("#1e2228")
    r = random.Random(5)
    for _ in range(180):
        s += f'<ellipse cx="{r.uniform(0,2400):.0f}" cy="{r.uniform(0,1350):.0f}" rx="{r.uniform(20,90):.0f}" ry="{r.uniform(8,30):.0f}" fill="{r.choice(["#14181c","#2c3036","#1a1d22"])}" opacity="0.7"/>'
    s += paw(500, 900, 2.6, "#07080a", 0.85, 80) + paw(980, 760, 2.6, "#07080a", 0.85, 80)
    s += footprint_human(1550, 700, 3.4, "#07080a", 0.95, -12)
    s += fence(1900, 2400, 1350, 1300, "#07080a", "#c8d4e0")
    s += glow(1600, 640, 500, "moon", 0.35)
    return svg(s)


@art
def dogs_roofs():
    s = moon_sky(5, 1200, 300, 140) + ridge(820, 200, "#070c14", 3)
    xs = (300, 820, 1350, 1880)
    for i, x in enumerate(xs):
        s += tile_house(x, 1250, 460, 300, lit=(i % 2 == 0), seed=i + 10)
    # dogs on rooftops howling (head up)
    for i, x in enumerate(xs):
        y = 1250 - 300 - 90
        d = (f"M{-90},0 L{-80},-60 C-60,-90 20,-90 50,-70 L80,-140 L96,-170 L110,-150 L120,-180 L126,-140 C130,-120 120,-90 100,-70 L90,0 L74,0 L70,-40 L-50,-40 L-60,0 Z "
             f"M-90,-40 C-130,-50 -150,-80 -150,-110 C-130,-80 -110,-66 -86,-60 Z")
        s += f'<g transform="translate({x+(i%2)*60-40},{y}) scale({1.1 if i%2 else -1.1},1.1)"><path d="{d}" fill="#020305"/><path d="{d}" fill="none" stroke="#9fc2e8" stroke-width="3" opacity="0.5"/></g>'
    return svg(s)


@art
def bedroom_dark():
    s = interior("#1a1420", "#0a0608", (500, 1100))
    s += f'<rect width="2400" height="1350" fill="#04060c" opacity="0.5"/>'
    # petate with two sleeping shapes under a blanket
    s += '<path d="M500,1150 L1900,1110 L2000,1300 L420,1340 Z" fill="#3a2a16"/>'
    for i in range(30):
        s += f'<path d="M{500+i*48},{1150-i*1.3:.0f} L{430+i*52},{1340-i*1.3:.0f}" stroke="#241a0c" stroke-width="3"/>'
    s += '<path d="M600,1200 C700,1100 1000,1080 1300,1100 C1600,1110 1800,1150 1880,1200 L1900,1290 L560,1300 Z" fill="#3a1418"/>'
    s += '<path d="M600,1200 C700,1100 1000,1080 1300,1100" stroke="#8a4a3a" stroke-width="5" fill="none" opacity="0.5"/>'
    s += '<ellipse cx="560" cy="1150" rx="70" ry="50" fill="#0a0806"/><ellipse cx="760" cy="1120" rx="70" ry="50" fill="#0a0806"/>'
    # door on the right with a sliver of moonlight underneath
    s += '<rect x="1950" y="420" width="360" height="640" fill="#140c08"/><rect x="1950" y="1052" width="360" height="10" fill="#9fc2e8" opacity="0.8"/>'
    s += candle(300, 1060, 40) + glow(300, 1020, 200, "warm", 0.7)
    return svg(s)


@art
def tomas_portrait():
    s = sky("#0a1220", "#24384c") + fence(0, 2400, 1350, 500, "#05070a", "#7a9cc4")
    s += f'<rect width="2400" height="1350" fill="#000" opacity="0.3"/>'
    s += tomas_bust(1200, 600, 2.2, rim="#9fc2e8", look=0.4, lids=0.1)
    return svg(s)


@art
def tomas_wait():
    s = moon_sky(6, 2000, 260, 110) + far_hills(880, 6)
    s += ground(1100, "#04060a", 14, 2) + fence(0, 2400, 1130, 260, "#05070a", "#7a9cc4")
    s += man_sil(1100, 1300, 700, machete=True, lantern=False, pose="crouch", rim="#9fc2e8")
    s += hen(700, 1290, 0.8, "#05070a") + hen(1600, 1300, 0.8, "#05070a")
    s += tile_house(2200, 1080, 380, 220, seed=12, lit=True)
    return svg(s)


@art
def corral_night():
    s = moon_sky(7, 600, 280, 100) + far_hills(860, 8)
    s += ground(1080, "#05070b", 14, 3)
    s += mist(1080, 80, 0.25, "#9ab4cc", 7)
    s += fence(0, 2400, 1250, 300, "#04060a", "#8aa4c0", 4)
    s += maguey(2200, 1100, 1.2, "#04060a", 1, "#7a9cc4")
    return svg(s)


@art
def fence_gap():
    s = R("#010203")
    # looking out through a gap between two fence posts: moonlit yard, a shape far away
    s += '<rect x="900" y="0" width="600" height="1350" fill="#0c1826"/>'
    s += f'<g>{moon_sky(9, 1200, 200, 60)}</g>'.replace('<rect', '<rect clip-path="url(#gp)"', 0)
    s += '<defs><clipPath id="gp"><path d="M820,0 L1580,0 L1560,1350 L840,1350 Z"/></clipPath></defs>'
    s += f'<g clip-path="url(#gp)">{moon_sky(9, 1200, 220, 60)}{ridge(800, 80, "#070d15", 3)}{ground(1000, "#0a1018", 10, 2)}'
    s += G(1150, 1100, 0.5, beast_body(rim="#9fc2e8", eyes=True), True) + mist(1050, 60, 0.3, "#9ab4cc", 2) + '</g>'
    for x0, x1 in ((0, 840), (1560, 2400)):
        s += f'<rect x="{x0}" y="0" width="{x1-x0}" height="1350" fill="#060403"/>'
        r = random.Random(x0)
        for _ in range(40):
            yy = r.uniform(0, 1350)
            s += f'<path d="M{x0+10},{yy:.0f} q{(x1-x0)/2:.0f},{r.uniform(-20,20):.0f} {x1-x0-20},0" stroke="#1a120c" stroke-width="3" fill="none"/>'
    s += '<path d="M840,0 L840,1350 M1560,0 L1560,1350" stroke="#7a9cc4" stroke-width="6" opacity="0.6"/>'
    return svg(s)


@art
def beast_side():
    s = moon_sky(10, 1700, 320, 140, "#02040a", "#122030") + ridge(900, 140, "#05080e", 4)
    s += ground(1150, "#020305", 14, 3) + mist(1150, 100, 0.3, "#8aa4c0", 3)
    s += G(1050, 1200, 1.15, beast_body(rim="#a8c8ff", eyes=True, head_low=True))
    s += maguey(200, 1300, 1.6, "#020305", 4, "#7a9cc4") + nopal(2200, 1320, 1.4, "#020305")
    return svg(s)


@art
def beast_eyes():
    s = R("#020306") + glow(1200, 500, 1100, "moon", 0.35)
    s += G(1200, 560, 1.9, beast_head(eyes="human", lids=0.35, smile=0.0))
    return svg(s)


@art
def beast_smile():
    s = R("#020306") + glow(1200, 500, 1100, "moon", 0.3)
    s += G(1200, 520, 1.8, beast_head(eyes="human", lids=0.55, smile=1.0))
    return svg(s)


@art
def beast_door():
    s = sky("#2a3644", "#7a8a9a") + far_hills(900, 11).replace("#0c1622", "#3a4654").replace("#070d15", "#2a3440")
    s += ground(1120, "#14181c", 14, 3) + mist(1100, 120, 0.45, "#c8d4e0", 3)
    s += reed_hut(1500, 1140, 1.4, glow_=False)
    s += G(1050, 1230, 0.9, beast_body(rim="#d8e2ea", eyes=True, head_low=False, limp=True))
    return svg(s)


@art
def l_beast_walk():
    return svg(G(700, 1200, 0.75, beast_body(rim="#a8c8ff", eyes=True, limp=False)))


@art
def l_eyes():
    s = ""
    for x in (1150, 1250):
        s += f'<circle cx="{x}" cy="640" r="70" fill="url(#warmglow)"/><ellipse cx="{x}" cy="640" rx="16" ry="8" fill="#ffd27a"/>'
    return svg(s)


@art
def l_fire_glow():
    return svg(glow(1200, 1000, 900, "warm", 0.6) + glow(1200, 1100, 400, "red", 0.5))


@art
def l_lantern_glow():
    return svg(glow(700, 1000, 600, "warm", 0.55))


@art
def l_candle_glow():
    return svg(glow(600, 1100, 520, "warm", 0.5))


@art
def strike():
    s = R("#04060c") + moon(1900, 260, 120)
    s += ground(1150, "#020305", 14, 3)
    # the machete arc as a bright slash + the beast lunging
    s += '<path d="M600,300 C1100,250 1500,600 1700,1000" stroke="#eef6ff" stroke-width="40" fill="none" opacity="0.9" filter="url(#blur2)" stroke-linecap="round"/>'
    s += '<path d="M600,300 C1100,250 1500,600 1700,1000" stroke="#ffffff" stroke-width="10" fill="none" stroke-linecap="round"/>'
    s += G(1300, 1200, 1.0, beast_body(rim="#a8c8ff", eyes=True, head_low=False), True)
    s += man_sil(500, 1350, 900, machete=False, rim="#9fc2e8")
    for i in range(6):
        s += f'<circle cx="{1500+i*40}" cy="{820+i*30}" r="{10-i}" fill="#5a0a0a"/>'
    return svg(s)


@art
def blood_trail():
    s = moon_sky(11, 1300, 240, 90) + ridge(600, 300, "#05080e", 12)
    s += ground(900, "#0a0e14", 30, 3)
    s += '<path d="M1200,1350 C1100,1200 1300,1100 1250,980 C1220,900 1260,820 1300,700" stroke="#1a2230" stroke-width="140" fill="none" opacity="0.8"/>'
    r = random.Random(2)
    for i in range(40):
        t = i / 40
        x = 1200 - 100 * math.sin(t * 3) + r.uniform(-30, 30); y = 1350 - t * 640
        s += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{14*(1-t*0.7):.0f}" ry="{8*(1-t*0.7):.0f}" fill="#5a0a0a"/>'
    s += reed_hut(1320, 690, 0.35)
    s += maguey(500, 1200, 1.4, "#020305", 1, "#7a9cc4") + maguey(1900, 1150, 1.2, "#020305", 2, "#7a9cc4")
    return svg(s)


@art
def hut_hill():
    s = moon_sky(12, 500, 260, 100) + ridge(800, 140, "#070c14", 2)
    s += '<path d="M0,1350 L0,1100 C600,900 1200,820 1700,800 C2000,790 2300,860 2400,900 L2400,1350 Z" fill="#04060a"/>'
    s += reed_hut(1500, 830, 0.9)
    for i, x in enumerate((300, 650, 1000, 1180, 1900, 2200)):
        s += maguey(x, 1000 + (i % 3) * 120 if x < 1200 else 1000, 1.0 + (i % 2) * 0.5, "#020305", i, "#7a9cc4")
    s += '<path d="M200,1350 C500,1150 900,980 1450,830" stroke="#141c28" stroke-width="40" fill="none" opacity="0.7"/>'
    return svg(s)


@art
def hut_door():
    s = R("#030408") + moon(300, 220, 80)
    s += '<rect x="700" y="100" width="1000" height="1250" fill="#0c0a08"/>'
    for i in range(70):
        s += f'<path d="M{700+i*14},100 l0,1250" stroke="#000" stroke-width="5"/>'
    s += '<path d="M1000,300 L1400,300 L1450,1350 L950,1350 Z" fill="#d8501a" opacity="0.85"/>'
    s += glow(1200, 900, 600, "red", 0.7) + glow(1200, 1000, 300, "warm", 0.8)
    s += '<path d="M1000,300 L1400,300 L1450,1350 L950,1350 Z" fill="url(#warmglow)" opacity="0.3"/>'
    s += man_sil(400, 1350, 1100, machete=True, rim="#ff8a4a", facing=1)
    return svg(s)


@art
def hut_inside():
    s = interior("#3a2014", "#160c06", (1200, 1000))
    s += herbs_hanging(400, 200, 1.0, 1) + herbs_hanging(1900, 220, 1.2, 2) + herbs_hanging(2200, 180, 0.9, 3)
    s += '<rect x="1700" y="600" width="300" height="20" fill="#2a1a0e"/>'  # shelf with jars
    for i in range(5):
        s += f'<path d="M{1720+i*56},600 C{1712+i*56},560 {1716+i*56},530 {1740+i*56},526 C{1764+i*56},530 {1768+i*56},560 {1760+i*56},600 Z" fill="#4a2a18"/>'
    s += fogon(1200, 1080, 1.4)
    # the folded thing by the fire (only a dark shape here)
    s += '<path d="M600,1150 C620,1100 860,1090 940,1130 C960,1170 900,1200 760,1200 C660,1200 600,1190 600,1150 Z" fill="#1a0e08"/>'
    s += '<path d="M610,1140 C700,1110 860,1100 930,1128" stroke="#ff9a50" stroke-width="5" fill="none" opacity="0.7"/>'
    return svg(s)


@art
def skin_by_fire():
    s = interior("#3a2014", "#160c06", (1700, 1000))
    s += fogon(1900, 1100, 1.2)
    s += '<path d="M200,1350 L300,980 L1500,960 L1600,1350 Z" fill="#3a2a16"/>'  # petate
    for i in range(26):
        s += f'<path d="M{300+i*46},980 L{200+i*54},1350" stroke="#241a0c" stroke-width="4"/>'
    # folded clothes: manta shirt + sombrero + huaraches
    s += '<path d="M380,1180 C400,1080 700,1060 800,1100 C820,1180 760,1240 560,1250 C440,1250 370,1230 380,1180 Z" fill="#cfc6b0"/><path d="M400,1170 C500,1130 700,1120 790,1140" stroke="#8a826e" stroke-width="5" fill="none"/>'
    s += '<ellipse cx="560" cy="1060" rx="220" ry="50" fill="#a88a50"/><ellipse cx="560" cy="1040" rx="80" ry="50" fill="#8a7040"/>'
    # the folded skin: pale-brown, soft folds, a tuft of white hair and an empty face fold (no gore)
    sk = SK_OLD
    s += (f'<path d="M840,1190 C860,1120 1060,1090 1260,1100 C1400,1110 1450,1170 1420,1220 C1340,1262 1000,1270 880,1250 C846,1236 836,1214 840,1190 Z" fill="{sk["base"]}"/>'
          f'<path d="M1380,1210 C1420,1240 1440,1280 1436,1330 L1470,1340 L1458,1300 L1486,1338 L1490,1296 L1512,1330 L1506,1286 C1500,1250 1470,1220 1420,1200 Z" fill="{sk["shadow"]}"/>'
          f'<path d="M1436,1330 C1440,1290 1430,1250 1400,1222" stroke="{sk["hi"]}" stroke-width="4" fill="none" opacity="0.5"/>'
          f'<path d="M880,1150 C960,1100 1160,1090 1350,1130" stroke="{sk["shadow"]}" stroke-width="10" fill="none" opacity="0.8"/>'
          f'<path d="M900,1200 C1000,1170 1200,1170 1370,1190" stroke="{sk["shadow"]}" stroke-width="8" fill="none" opacity="0.7"/>'
          f'<path d="M870,1120 C960,1070 1150,1050 1300,1080" stroke="{sk["hi"]}" stroke-width="5" fill="none" opacity="0.6"/>')
    # sagging face fold on top: hollow eyes, mustache, white hair
    s += f'<path d="M1000,1110 C1010,1040 1190,1030 1220,1100 C1200,1130 1040,1140 1000,1110 Z" fill="{sk["light"]}"/>'
    s += '<path d="M1040,1080 q24,-16 46,0 q-22,10 -46,0 Z M1132,1074 q24,-16 46,0 q-22,10 -46,0 Z" fill="#100604"/>'
    s += f'<path d="M1100,1090 q6,16 -2,26" stroke="{sk["deep"]}" stroke-width="4" fill="none"/>'
    s += f'<g transform="translate(1108,1062) scale(1,0.7)">{mustache(gray=True, big=0.7)}</g>'
    s += strands(random.Random(3), [(1010, 1060, 1060, 1020, 1120, 1040), (1100, 1046, 1160, 1020, 1220, 1070)], 10, "#e8e4dc", (1.5, 3), (0.5, 0.9), 8)
    s += glow(1300, 1100, 500, "warm", 0.6)
    return svg(s)


@art
def plaza_morning():
    s = sky("#5a7a9a", "#f0c890") + church(1250, 900, 1.0, "#4a3e3a", False)
    s += tile_house(350, 1000, 600, 320, wall="#6a5a4a", roof="#6a2a18", lit=False, rim="#ffd0a0", seed=21)
    s += tile_house(2100, 1000, 560, 300, wall="#6a5a4a", roof="#6a2a18", lit=False, rim="#ffd0a0", seed=22)
    s += papel_picado(220, "#c8283a", 9, 4, 0.9)
    s += ground(1000, "#5a4a3a", 6, 2) + cobbles(1000, 1350, "#4a3e34", 3, False)
    s += tree(1800, 1040, 520, 5, "#1a1a14", "ahuehuete")
    # bench with the old man seen from afar
    s += '<rect x="1400" y="1090" width="420" height="24" fill="#2a1a10"/><rect x="1420" y="1110" width="16" height="80" fill="#2a1a10"/><rect x="1790" y="1110" width="16" height="80" fill="#2a1a10"/>'
    s += man_sil(1600, 1190, 380, color="#1a140e", rim=None, pose="crouch")
    s += woman_sil(700, 1250, 420, "#2a2018", None) + man_sil(900, 1260, 440, color="#2a2018", rim=None)
    return svg(s)


@art
def plaza_dogs():
    s = sky("#4a5a7a", "#e8a070") + tile_house(700, 1000, 900, 380, wall="#4a3e34", roof="#5a2414", lit=False, rim="#ffc090", seed=23)
    s += ground(1000, "#3a2e24", 8, 3)
    # carreta with dogs hiding underneath
    s += '<rect x="1300" y="900" width="700" height="120" fill="#2a1a0e"/>'
    for cx in (1420, 1880):
        s += f'<circle cx="{cx}" cy="1080" r="110" fill="none" stroke="#1a0e06" stroke-width="22"/>'
        for a in range(0, 360, 45):
            s += f'<path d="M{cx},1080 l{110*math.cos(math.radians(a)):.0f},{110*math.sin(math.radians(a)):.0f}" stroke="#1a0e06" stroke-width="10"/>'
    for i, x in enumerate((1520, 1700)):
        s += f'<path d="M{x-80},1180 C{x-80},1120 {x+40},1100 {x+80},1130 L{x+110},1110 L{x+120},1140 C{x+120},1170 {x+90},1180 {x+60},1180 Z" fill="#0a0806"/>'
        s += f'<circle cx="{x+96}" cy="1140" r="5" fill="#ffd27a"/>'
    s += man_sil(400, 1290, 620, color="#100c08", rim="#ffc090")  # don Fermín passing, long shadow
    s += '<path d="M400,1290 L1300,1340 L1300,1350 L380,1350 Z" fill="#000" opacity="0.4"/>'
    return svg(s)


@art
def fermin_portrait():
    s = sky("#5a6a8a", "#e8b080") + church(1900, 1100, 1.0, "#3a302c", False)
    s += f'<rect width="2400" height="1350" fill="#000" opacity="0.25"/>'
    s += fermin_bust(1150, 560, 2.2, rim="#ffd0a0", smile=0.5, lids=0.45)
    return svg(s)


@art
def bandage_hand():
    s = sky("#5a6a8a", "#e8b080") + f'<rect width="2400" height="1350" fill="#000" opacity="0.3"/>'
    s += fermin_bust(800, 500, 1.8, rim="#ffd0a0", smile=0.2, lids=0.5, look=0.6)
    s += G(1550, 1150, 2.6, bandaged_hand())
    return svg(s)


@art
def fermin_eyes():
    s = R("#140c08") + glow(1200, 600, 900, "warm", 0.35)
    s += fermin_bust(1200, 700, 3.4, rim="#ffd0a0", smile=0.0, lids=0.4, hat=True)
    return svg(s)


@art
def fermin_sinister():
    s = R("#0a0404") + glow(1200, 700, 900, "red", 0.4)
    s += fermin_bust(1200, 680, 3.2, rim="#ff5a3a", smile=0.7, lids=0.55, eyes="nahual", look=0.2)
    return svg(s)


@art
def healer_herbs():
    s = interior("#3a2418", "#1a100a", (1200, 900))
    s += herbs_hanging(300, 150, 1.2, 4) + herbs_hanging(700, 120, 1.0, 5) + herbs_hanging(1700, 160, 1.1, 6) + herbs_hanging(2100, 140, 1.0, 7)
    s += '<rect x="600" y="900" width="1200" height="40" fill="#2a1a0e"/>'
    # copal brazier with smoke, eggs in a bowl, bundles of herbs
    s += '<path d="M1100,900 L1130,820 L1270,820 L1300,900 Z" fill="#3a2214"/>' + glow(1200, 820, 200, "warm", 0.8)
    for i in range(5):
        s += f'<path d="M{1180+i*10},810 C{1150+i*20},700 {1250-i*10},600 {1200+i*14},{460-i*30}" stroke="#c8c0b8" stroke-width="{14-i*2}" fill="none" opacity="0.25" filter="url(#blur2)"/>'
    s += '<ellipse cx="800" cy="890" rx="120" ry="30" fill="#5a3a20"/>' + "".join(f'<ellipse cx="{760+i*40}" cy="870" rx="22" ry="28" fill="#efe6d2"/>' for i in range(3))
    s += herb_bundle_h(1500, 880) + herb_bundle_h(1620, 870)
    s += candle(1700, 900, 60)
    return svg(s)


def herb_bundle_h(x, y):
    r = random.Random(x); s = ""
    for i in range(14):
        a = r.uniform(-25, 25)
        s += f'<path d="M{x},{y} l{a*2:.0f},-{r.uniform(80,140):.0f}" stroke="#2a4a20" stroke-width="5"/>'
    s += f'<rect x="{x-14}" y="{y-30}" width="28" height="14" fill="#a8231a"/>'
    return s


@art
def codex_paper():
    s = R("#c9a874") + f'<rect width="2400" height="1350" filter="url(#paper)" fill="#b8925a" opacity="0.5"/>'
    s += glow(1200, 600, 1200, "warm", 0.3)
    # codex-style figures: a man, a dotted line, and a jaguar / dog sign
    def glyph_man(x, y, k):
        return (f'<g transform="translate({x},{y}) scale({k})" stroke="#1a0e06" stroke-width="6" fill="none">'
                f'<circle cx="0" cy="-200" r="60" fill="#c8583a"/><path d="M-30,-140 L-40,40 L40,40 L30,-140 Z" fill="#e8dcc0"/>'
                f'<path d="M-40,-100 L-110,-40 M40,-100 L110,-60 M-30,40 L-50,160 M30,40 L50,160"/><circle cx="20" cy="-210" r="8" fill="#1a0e06"/></g>')
    def glyph_jaguar(x, y, k):
        sp = "".join(f'<circle cx="{-60+i*30}" cy="{-40+(i%2)*30}" r="9" fill="#1a0e06"/>' for i in range(6))
        return (f'<g transform="translate({x},{y}) scale({k})" stroke="#1a0e06" stroke-width="6">'
                f'<path d="M-120,0 C-120,-80 60,-100 100,-60 L160,-120 L180,-60 C200,-20 160,20 120,20 L120,100 L90,100 L80,30 L-60,30 L-70,100 L-100,100 Z" fill="#e8b040"/>{sp}'
                f'<circle cx="150" cy="-70" r="8" fill="#1a0e06"/><path d="M-120,0 C-170,0 -200,-40 -200,-80" fill="none"/></g>')
    s += glyph_man(700, 800, 1.6) + glyph_jaguar(1650, 760, 1.7)
    s += '<path d="M900,600 C1100,500 1300,500 1450,600" stroke="#1a0e06" stroke-width="6" stroke-dasharray="4 24" stroke-linecap="round" fill="none"/>'
    for i in range(8):  # day-sign dots and step-fret border
        s += f'<circle cx="{400+i*90}" cy="1150" r="22" fill="#a8231a" stroke="#1a0e06" stroke-width="4"/>'
    for x in range(0, 2400, 120):
        s += f'<path d="M{x},60 l40,0 l0,40 l40,0 l0,-40 l40,0" stroke="#1a0e06" stroke-width="10" fill="none"/>'
        s += f'<path d="M{x},1300 l40,0 l0,-40 l40,0 l0,40 l40,0" stroke="#1a0e06" stroke-width="10" fill="none"/>'
    return svg(s)


@art
def tonal_wheel():
    s = R("#120a06") + glow(1200, 675, 1000, "warm", 0.45)
    s += '<circle cx="1200" cy="675" r="560" fill="#b8925a"/><circle cx="1200" cy="675" r="560" fill="none" stroke="#3a2010" stroke-width="16"/>'
    s += '<circle cx="1200" cy="675" r="380" fill="none" stroke="#3a2010" stroke-width="10"/><circle cx="1200" cy="675" r="160" fill="#c8583a" stroke="#3a2010" stroke-width="10"/>'
    for i in range(20):
        a = math.radians(i * 18)
        x0, y0 = 1200 + 380 * math.cos(a), 675 + 380 * math.sin(a)
        x1, y1 = 1200 + 560 * math.cos(a), 675 + 560 * math.sin(a)
        s += f'<path d="M{x0:.0f},{y0:.0f} L{x1:.0f},{y1:.0f}" stroke="#3a2010" stroke-width="6"/>'
        am = math.radians(i * 18 + 9); xm, ym = 1200 + 470 * math.cos(am), 675 + 470 * math.sin(am)
        s += f'<circle cx="{xm:.0f}" cy="{ym:.0f}" r="30" fill="{["#a8231a","#2e6a5a","#e8b040","#1a0e06"][i%4]}" opacity="0.85"/>'
        for d in range(i % 4 + 1):
            s += f'<circle cx="{xm + (d-1.5)*14:.0f}" cy="{ym+44:.0f}" r="5" fill="#1a0e06"/>'
    # face of the sun in the centre
    s += '<circle cx="1160" cy="650" r="14" fill="#1a0e06"/><circle cx="1240" cy="650" r="14" fill="#1a0e06"/><path d="M1150,720 Q1200,750 1250,720" stroke="#1a0e06" stroke-width="10" fill="none"/>'
    for i in range(8):
        a = math.radians(i * 45)
        s += f'<path d="M{1200+160*math.cos(a):.0f},{675+160*math.sin(a):.0f} L{1200+250*math.cos(a+0.15):.0f},{675+250*math.sin(a+0.15):.0f} L{1200+250*math.cos(a-0.15):.0f},{675+250*math.sin(a-0.15):.0f} Z" fill="#e8b040" stroke="#3a2010" stroke-width="5"/>'
    return svg(s)


@art
def baby_animal():
    s = interior("#2a1a12", "#120a06", (900, 900))
    # a mother cradling a newborn wrapped in a rebozo; on the wall, the shadow of its tonal animal (a deer)
    s += woman_sil(900, 1350, 900, "#0c0806", "#ffb070")
    s += '<ellipse cx="1020" cy="800" rx="110" ry="60" fill="#3a1a28"/>'
    deer = ("M0,0 C40,-60 160,-70 240,-40 L300,-120 L290,-200 L310,-200 L320,-130 L340,-210 L356,-206 L340,-110 C360,-90 380,-60 370,-40 L330,-40 "
            "C320,0 300,40 290,80 L300,220 L280,220 L262,90 L80,90 L70,220 L50,220 L40,90 C10,70 -10,40 0,0 Z")
    s += f'<g transform="translate(1500,520) scale(1.6)"><path d="{deer}" fill="#000" opacity="0.55" filter="url(#blur1)"/></g>'
    s += candle(600, 1100, 60) + glow(600, 1040, 300, "warm", 0.9)
    return svg(s)


@art
def shadow_transform():
    s = interior("#4a2414", "#1a0c06", (1200, 1150))
    s += fogon(1200, 1200, 1.2)
    # man's shadow on the wall bending into a crouch + a second, already half-animal shadow
    s += f'<g opacity="0.75" filter="url(#blur1)">{man_sil(700, 1040, 900, color="#000", rim=None, hat=False)}</g>'
    s += f'<g opacity="0.75" filter="url(#blur1)">{man_sil(1150, 1040, 900, color="#000", rim=None, hat=False, pose="crouch")}</g>'
    s += f'<g opacity="0.75" filter="url(#blur1)" transform="translate(1650,1040) scale(0.9)">{beast_body(rim=None, fill="#000", eyes=False, head_low=False)}</g>'
    s += '<path d="M820,560 C900,480 1000,480 1080,560" stroke="#000" stroke-width="10" fill="none" opacity="0.5" marker-end=""/>'
    s += '<path d="M1270,560 C1360,480 1470,480 1550,560" stroke="#000" stroke-width="10" fill="none" opacity="0.5"/>'
    return svg(s)


@art
def shadow_dog():
    s = interior("#5a1a0e", "#1a0806", (1200, 1150))
    s += fogon(1200, 1200, 1.4)
    s += f'<g opacity="0.85" filter="url(#blur1)">{G(1300, 1050, 1.5, beast_body(rim=None, fill="#000", eyes=False, head_low=False))}</g>'
    s += '<circle cx="1980" cy="460" r="60" fill="url(#redglow)"/><ellipse cx="1980" cy="460" rx="14" ry="7" fill="#ffb040"/>'
    return svg(s)


@art
def sahagun_desk():
    s = interior("#2a1c14", "#0e0a08", (900, 800))
    s += '<rect x="400" y="860" width="1500" height="50" fill="#2a1a0e"/><rect x="460" y="910" width="40" height="440" fill="#1a1008"/><rect x="1800" y="910" width="40" height="440" fill="#1a1008"/>'
    # open book with codex-like drawings and Latin-script lines
    s += '<path d="M800,860 L1000,780 L1200,820 L1400,780 L1600,860 L1200,880 Z" fill="#e8dcc0"/><path d="M1200,820 L1200,880" stroke="#8a7a5a" stroke-width="4"/>'
    for i in range(7):
        s += f'<path d="M{880+i*6},{810+i*10} L{1160},{830+i*8}" stroke="#4a3a2a" stroke-width="2" opacity="0.6"/>'
    s += '<path d="M1300,820 C1320,800 1380,800 1400,820 L1420,800 L1430,830 C1400,850 1320,850 1300,820 Z" fill="#a8231a" opacity="0.8"/>'
    # the friar: hooded silhouette writing, quill
    s += '<path d="M300,1350 C300,1100 340,900 420,800 C430,700 520,620 600,640 C680,660 720,760 700,840 C760,900 820,980 860,1350 Z" fill="#1a120c"/>'
    s += '<path d="M420,800 C430,700 520,620 600,640" stroke="#ffcf8a" stroke-width="6" fill="none" opacity="0.6"/>'
    s += '<path d="M760,860 L900,700" stroke="#efe6d2" stroke-width="6"/><path d="M900,700 C930,640 960,620 980,610 C960,660 930,690 900,700 Z" fill="#efe6d2"/>'
    s += candle(1700, 860, 90) + glow(1700, 760, 420, "warm", 1.0)
    return svg(s)


@art
def jaguar_mirror():
    s = R("#030508") + moon_sky(13, 1900, 250, 90) + f'<rect width="2400" height="1350" fill="#000" opacity="0.3"/>'
    s += ridge(1000, 100, "#020406", 3)
    # jungle leaves framing
    r = random.Random(4)
    for _ in range(30):
        x = r.choice([r.uniform(0, 500), r.uniform(1900, 2400)]); y = r.uniform(200, 1350); a = r.uniform(-60, 60); L = r.uniform(160, 300)
        s += f'<path d="M0,0 C{L*0.3:.0f},{-L*0.3:.0f} {L*0.8:.0f},{-L*0.2:.0f} {L:.0f},0 C{L*0.8:.0f},{L*0.2:.0f} {L*0.3:.0f},{L*0.3:.0f} 0,0 Z" fill="#03080a" transform="translate({x:.0f},{y:.0f}) rotate({a:.0f})"/>'
    # smoking obsidian mirror behind
    s += '<circle cx="1200" cy="560" r="300" fill="#05060a" stroke="#7a6a3a" stroke-width="14"/><circle cx="1200" cy="560" r="300" fill="url(#moonglow)" opacity="0.15"/>'
    for i in range(6):
        s += f'<path d="M{1100+i*40},300 C{1050+i*50},200 {1200+i*10},120 {1150+i*30},{20}" stroke="#a8b4c0" stroke-width="{24-i*2}" fill="none" opacity="0.18" filter="url(#blur3)"/>'
    # jaguar: crouching side silhouette with spots, golden rim
    d = ("M720,1000 C760,880 900,840 1060,850 C1200,860 1320,850 1400,830 C1460,780 1520,760 1590,770 L1600,730 L1630,770 C1690,780 1740,820 1750,870 "
         "L1790,900 L1750,930 C1720,960 1680,970 1640,965 C1600,990 1560,1010 1520,1030 C1530,1100 1560,1160 1600,1200 L1520,1200 C1480,1160 1460,1110 1450,1060 "
         "C1300,1080 1100,1080 960,1070 C940,1120 960,1170 1000,1200 L920,1200 C880,1170 860,1120 860,1070 C800,1060 750,1040 720,1000 Z "
         "M720,1000 C620,1010 540,980 500,900 C480,860 470,820 490,790 C500,850 560,930 720,960 Z")
    s += f'<path d="{d}" fill="#e8b040" filter="url(#blur2)" opacity="0.5"/><path d="{d}" fill="#120a04"/>'
    for _ in range(40):
        x = r.uniform(800, 1450); y = r.uniform(880, 1060)
        s += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="16" ry="11" fill="none" stroke="#5a3a10" stroke-width="5"/>'
    s += '<ellipse cx="1690" cy="850" rx="14" ry="7" fill="#ffd27a"/><circle cx="1690" cy="850" r="40" fill="url(#warmglow)"/>'
    return svg(s)


@art
def church_village():
    s = moon_sky(14, 600, 250, 100) + ridge(800, 160, "#070c14", 5)
    s += church(1300, 1100, 1.5) + tile_house(400, 1150, 420, 220, seed=31) + tile_house(2100, 1150, 460, 220, seed=32, lit=False)
    s += ground(1150, "#04060a", 10, 2) + cobbles(1150, 1350)
    s += mist(1150, 90, 0.25, "#9ab4cc", 9)
    return svg(s)


@art
def animals_row():
    s = moon_sky(15, 1200, 250, 90) + ridge(900, 80, "#05080e", 6) + ground(1100, "#020305", 10, 4)
    s += mist(1100, 80, 0.25, "#8aa4c0", 2)
    # black dog
    s += G(350, 1150, 0.45, beast_body(rim="#9fc2e8", eyes=True, head_low=False))
    # coyote (thinner, howling) - reuse dog sitting
    s += G(1000, 1150, 0.55, beast_body(rim="#9fc2e8", eyes=True, sit=True))
    # giant turkey
    s += f'<g transform="translate(1450,1150) scale(2.2)">{hen(0, 0, 1.0, "#020305", turkey=True)}</g>'
    s += '<circle cx="1585" cy="790" r="26" fill="url(#warmglow)"/><circle cx="1585" cy="790" r="5" fill="#ffd27a"/>'
    # burro
    burro = ("M-200,-300 C-150,-340 60,-340 120,-310 L180,-420 L170,-520 L190,-520 L210,-440 L230,-530 L250,-525 L240,-420 C280,-380 300,-330 290,-300 L240,-300 "
             "C220,-280 200,-260 180,-250 L180,0 L150,0 L140,-220 L-150,-220 L-160,0 L-190,0 L-200,-220 C-230,-240 -240,-280 -200,-300 Z")
    s += f'<g transform="translate(1900,1150) scale(0.75)"><path d="{burro}" fill="#9fc2e8" filter="url(#blur2)" opacity="0.6"/><path d="{burro}" fill="#020305"/><circle cx="250" cy="-360" r="30" fill="url(#warmglow)"/></g>'
    # cat on two legs
    cat = "M-40,0 L-30,-160 C-60,-200 -50,-260 -20,-280 L-30,-330 L0,-300 L30,-330 L22,-280 C50,-260 60,-200 30,-160 L40,0 L20,0 L10,-120 L-10,-120 L-20,0 Z M30,-120 C90,-140 110,-220 90,-260"
    s += f'<g transform="translate(2250,1150) scale(1.1)"><path d="{cat}" fill="#020305" stroke="#9fc2e8" stroke-width="3"/><circle cx="-10" cy="-240" r="5" fill="#ffd27a"/><circle cx="14" cy="-240" r="5" fill="#ffd27a"/></g>'
    return svg(s)


@art
def abuela_portrait():
    s = interior("#3a2014", "#160c06", (500, 1000)) + f'<rect width="2400" height="1350" fill="#000" opacity="0.2"/>'
    s += herbs_hanging(2000, 150, 1.1, 8)
    s += abuela_bust(1250, 560, 2.2, rim="#ffcf8a")
    return svg(s)


@art
def salt_ash():
    s = interior("#3a2014", "#160c06", (1200, 1100))
    s += '<path d="M200,1350 L400,1050 L2000,1030 L2200,1350 Z" fill="#2a1e12"/>'
    # two hands: one pouring salt from a bag, one sprinkling ash from a jícara
    def hand(x, y, flip=1, k=1.0):
        sk = SK_TOMAS
        h = (f'M0,0 C40,-20 120,-30 180,-20 C210,-14 230,0 220,20 L160,26 C190,40 200,60 180,70 L120,66 C140,86 120,100 100,96 L40,90 C10,80 -10,40 0,0 Z')
        return f'<g transform="translate({x},{y}) scale({flip*k},{k})"><path d="M-300,40 L0,-10 L10,90 L-300,140 Z" fill="#cfc6b0"/><path d="{h}" fill="{sk["base"]}"/><path d="M0,0 C40,-20 120,-30 180,-20" stroke="{sk["hi"]}" stroke-width="5" fill="none"/></g>'
    s += '<path d="M500,500 C460,620 600,700 760,640 C820,600 800,480 720,440 Z" fill="#d8cfb8"/>'  # salt bag
    s += hand(420, 600, 1, 1.4)
    for i in range(260):
        r = random.Random(i)
        s += f'<circle cx="{760 + r.gauss(0, 30) + i*0.4:.0f}" cy="{660 + i*1.6 + r.uniform(-10,10):.0f}" r="{r.uniform(2,5):.1f}" fill="#f4f2ee" opacity="0.85"/>'
    s += '<path d="M1600,560 C1600,660 1820,660 1820,560 Z" fill="#6a3a1a"/><path d="M1600,560 L1820,560" stroke="#a86a3a" stroke-width="6"/>'
    s += hand(1980, 620, -1, 1.4)
    for i in range(160):
        r = random.Random(1000 + i)
        s += f'<circle cx="{1640 + r.gauss(0, 50) - i*0.6:.0f}" cy="{620 + i*2.4 + r.uniform(-10,10):.0f}" r="{r.uniform(3,9):.1f}" fill="#5a5a5a" opacity="{r.uniform(0.3,0.8):.2f}"/>'
    s += '<path d="M700,1180 C900,1100 1500,1100 1700,1180 C1500,1230 900,1230 700,1180 Z" fill="#8a6046" opacity="0.8"/>'  # what lies below (hinted)
    s += glow(1200, 1150, 600, "warm", 0.6)
    return svg(s)


@art
def scissors_candle():
    s = wood_door(0, 0, 2400, 1350, "#2a1a10") + f'<rect width="2400" height="1350" fill="#000" opacity="0.35"/>'
    s += cross_cal(1200, 470, 2.2)
    # open scissors hanging in a cross shape
    s += '<g transform="translate(1200,900) rotate(45)"><path d="M-8,-260 L8,-260 L14,0 L-14,0 Z" fill="#9aa4ae"/><circle cx="0" cy="60" r="50" fill="none" stroke="#5a5a5a" stroke-width="16"/></g>'
    s += '<g transform="translate(1200,900) rotate(-45)"><path d="M-8,-260 L8,-260 L14,0 L-14,0 Z" fill="#c0c8d0"/><circle cx="0" cy="60" r="50" fill="none" stroke="#5a5a5a" stroke-width="16"/></g>'
    s += '<path d="M1200,700 L1200,0" stroke="#3a2a1a" stroke-width="5"/><circle cx="1200" cy="900" r="16" fill="#4a4a4a"/>'
    s += candle(700, 1300, 110) + candle(1700, 1300, 110) + glow(700, 1180, 420, "warm", 0.9) + glow(1700, 1180, 420, "warm", 0.9)
    return svg(s)


@art
def door_scratch():
    s = wood_door(500, 0, 1900, 1350, "#2e1c10") + R("#000", 0.45)
    s += '<rect x="500" y="1300" width="1400" height="50" fill="#9fc2e8" opacity="0.6"/>'  # moonlight under the door
    s += '<path d="M800,1300 C900,1320 1000,1320 1100,1300 L1100,1350 L800,1350 Z" fill="#000" opacity="0.8"/>'  # a shadow blocking the light
    for i in range(4):
        x0 = 980 + i * 50
        s += f'<path d="M{x0},420 C{x0+30},600 {x0+10},800 {x0+40},1000" stroke="#c8a070" stroke-width="5" fill="none" opacity="0.8"/>'
        s += f'<path d="M{x0+4},420 C{x0+34},600 {x0+14},800 {x0+44},1000" stroke="#0a0604" stroke-width="8" fill="none" opacity="0.6"/>'
    s += candle(300, 1300, 80) + glow(300, 1220, 350, "warm", 0.6)
    return svg(s)


@art
def door_outside():
    s = moon_sky(16, 2000, 220, 90) + tile_house(1100, 1250, 1200, 700, cross=True, seed=33, lit=True)
    s += ground(1250, "#04060a", 8, 3) + mist(1250, 100, 0.3, "#9ab4cc", 5)
    # beast standing on hind legs against the door, from behind
    d = ("M0,0 L-30,-200 C-60,-260 -80,-380 -60,-480 C-50,-560 -20,-600 10,-620 L-10,-700 L30,-660 L60,-700 L60,-620 C90,-590 110,-540 100,-480 "
         "C90,-400 70,-280 60,-200 L40,0 Z M-60,-480 C-120,-520 -150,-600 -140,-660 L-110,-660 C-110,-600 -80,-540 -40,-520 Z M100,-480 C160,-520 180,-600 160,-660 L130,-660 C140,-600 120,-540 80,-520 Z "
         "M-30,-200 C-100,-180 -160,-120 -180,-60 C-140,-110 -90,-150 -20,-170 Z")
    s += f'<g transform="translate(940,1250) scale(1.0)"><path d="{d}" fill="#9fc2e8" filter="url(#blur2)" opacity="0.7"/><path d="{d}" fill="#020305"/></g>'
    s += maguey(2100, 1320, 1.5, "#020305", 2, "#7a9cc4")
    return svg(s)


@art
def cross_scratched():
    s = sky("#4a5a6e", "#b8c4d0") + f'<rect x="0" y="0" width="2400" height="1350" fill="#5a5048"/>'
    r = random.Random(6)
    for _ in range(140):
        s += f'<rect x="{r.uniform(0,2400):.0f}" y="{r.uniform(0,1350):.0f}" width="{r.uniform(60,140):.0f}" height="{r.uniform(26,40):.0f}" fill="#000" opacity="{r.uniform(0.05,0.18):.2f}"/>'
    s += cross_cal(1200, 640, 3.4, scratched=True)
    s += f'<rect width="2400" height="1350" fill="#9ab0c8" opacity="0.12"/>'
    return svg(s)


@art
def malinche_lights():
    s = moon_sky(17, 400, 220, 80, "#03050c", "#16243a")
    # La Malinche: broad, eroded volcano
    s += '<path d="M200,1100 C500,900 800,620 1100,480 C1180,450 1260,450 1340,490 C1600,620 1900,880 2300,1100 Z" fill="#0a1220"/>'
    s += '<path d="M1100,480 C1180,450 1260,450 1340,490 C1300,520 1240,530 1180,520 Z" fill="#8a9ab0" opacity="0.4"/>'
    s += ridge(1100, 60, "#05080e", 4) + city_row(1180, 3, 22, "#04060a", 0.4)
    s += ground(1200, "#020305", 8, 2)
    # balls of fire flying over the slopes
    for x, y, rr in ((900, 700, 30), (1500, 640, 24), (1700, 820, 18), (1180, 820, 20)):
        s += f'<circle cx="{x}" cy="{y}" r="{rr*5}" fill="url(#warmglow)"/><circle cx="{x}" cy="{y}" r="{rr}" fill="#ffd27a"/>'
        s += f'<path d="M{x},{y} C{x-80},{y-20} {x-160},{y+10} {x-260},{y-10}" stroke="#ff8a2a" stroke-width="{rr*0.8:.0f}" opacity="0.35" fill="none" filter="url(#blur2)"/>'
    return svg(s)


@art
def cocoyoc_street():
    s = sky("#05080e", "#1a2838") + stars(80, 9, 500)
    # modern street: concrete houses, streetlamp, cables, white crosses painted on doors/windows
    for i, x in enumerate((300, 900, 1500, 2100)):
        w = 560
        s += f'<rect x="{x-w/2}" y="{500 + (i%2)*60}" width="{w}" height="{800-(i%2)*60}" fill="{["#2a3036","#2e2a30","#28302e","#30302a"][i]}"/>'
        s += f'<rect x="{x-w/2}" y="{500 + (i%2)*60}" width="{w}" height="20" fill="#14181c"/>'
        s += f'<rect x="{x-180}" y="1000" width="140" height="300" fill="#4a4e54"/>'  # metal door
        s += f'<rect x="{x+40}" y="{760}" width="160" height="130" fill="{"#ffc865" if i==1 else "#0c1016"}"/>'
        s += cross_cal(x - 110, 1130, 0.55) + cross_cal(x + 120, 830, 0.4)
    s += '<path d="M0,420 C600,470 1200,460 2400,400 M0,450 C700,500 1500,480 2400,440" stroke="#05070a" stroke-width="4" fill="none"/>'
    s += lamp(1200, 1320, 900, "#05070a", True) + glow(1200, 420, 500, "warm", 0.5)
    s += f'<rect x="0" y="1300" width="2400" height="50" fill="#14181c"/>'
    return svg(s)


@art
def path_hill():
    s = moon_sky(18, 1800, 240, 100) + ridge(700, 200, "#070c14", 7)
    s += '<path d="M0,1350 L0,1000 C500,900 1000,760 1500,700 C1900,660 2200,700 2400,740 L2400,1350 Z" fill="#05080c"/>'
    s += '<path d="M600,1350 C800,1100 1100,900 1450,720" stroke="#1a2230" stroke-width="90" fill="none" opacity="0.8"/>'
    s += reed_hut(1500, 710, 0.32)
    for i, (x, y) in enumerate(((300, 1150), (550, 1250), (1000, 1020), (1250, 900), (1750, 820), (2000, 900), (2250, 1150))):
        s += maguey(x, y, 1.0 + (i % 3) * 0.3, "#020305", i, "#7a9cc4")
    return svg(s)


@art
def tomas_climb():
    s = moon_sky(19, 600, 250, 100) + ridge(800, 160, "#070c14", 9)
    s += '<path d="M0,1350 L0,1200 C800,1050 1500,850 2400,700 L2400,1350 Z" fill="#04060a"/>'
    s += man_sil(1100, 1110, 720, machete=False, lantern=True, pose="climb", rim="#9fc2e8", bag=True)
    s += maguey(500, 1300, 1.4, "#020305", 1, "#7a9cc4") + maguey(1800, 960, 1.2, "#020305", 2, "#7a9cc4")
    return svg(s)


@art
def fermin_ritual():
    s = interior("#4a2414", "#1a0c06", (1200, 1100))
    s += herbs_hanging(300, 160, 1.1, 9) + herbs_hanging(2100, 160, 1.0, 10)
    s += fogon(1200, 1220, 1.3)
    # old man standing, arms raised, seen from the side with long shadow on the wall
    s += f'<g opacity="0.6" filter="url(#blur1)">{man_sil(1500, 1080, 1100, color="#000", rim=None)}</g>'
    s += man_sil(900, 1290, 820, color="#0c0806", rim="#ff9a50", hat=True)
    s += '<path d="M800,620 C760,520 740,440 760,380 M1000,620 C1040,520 1060,440 1040,380" stroke="#0c0806" stroke-width="40" fill="none" stroke-linecap="round" transform="translate(-10,40)"/>'
    for i in range(5):
        s += f'<path d="M{1180+i*10},1100 C{1150+i*20},900 {1250-i*10},700 {1200+i*14},{460-i*30}" stroke="#c8c0b8" stroke-width="{14-i*2}" fill="none" opacity="0.2" filter="url(#blur2)"/>'
    return svg(s)


@art
def fermin_back():
    s = interior("#4a2414", "#1a0c06", (1400, 1100))
    s += fogon(1500, 1240, 1.2)
    # bare back of the old man, shirt falling, sombrero on the floor; a dark seam running down the spine
    sk = SK_OLD
    s += (f'<path d="M760,1350 C760,1150 740,900 780,760 C800,700 880,660 960,650 L1100,650 C1180,660 1260,700 1280,760 C1320,900 1300,1150 1300,1350 Z" fill="{sk["shadow"]}"/>'
          f'<path d="M1100,650 C1180,660 1260,700 1280,760 C1320,900 1300,1150 1300,1350 L1180,1350 C1200,1100 1200,850 1160,700 Z" fill="{sk["light"]}" opacity="0.7"/>'
          f'<path d="M1030,660 C1030,800 1034,1000 1030,1350" stroke="#2a0a06" stroke-width="10" fill="none"/>'
          f'<path d="M1030,660 C1030,800 1034,1000 1030,1350" stroke="#ff7a2a" stroke-width="3" fill="none" opacity="0.6"/>'
          f'<path d="M1030,700 C990,720 960,760 950,800" stroke="{sk["deep"]}" stroke-width="5" fill="none" opacity="0.6"/>')
    # head from behind: white hair, ears
    s += '<path d="M940,640 C930,700 1130,700 1120,640 Z" fill="#5a3c2a"/><ellipse cx="1030" cy="560" rx="110" ry="130" fill="#6a6660"/>'
    s += strands(random.Random(5), [(940, 500, 1000, 450, 1100, 470), (930, 560, 980, 640, 1000, 680), (1130, 560, 1080, 640, 1060, 680), (1030, 440, 1040, 560, 1030, 680)], 12, "#c8c4bc", (2, 4), (0.3, 0.6), 14)
    s += '<path d="M1140,520 C1150,600 1130,660 1100,690" stroke="#ff9a50" stroke-width="8" fill="none" opacity="0.6" filter="url(#blur1)"/>'
    s += '<path d="M920,560 C900,560 900,600 922,606 M1140,560 C1160,560 1160,600 1138,606" stroke="#5a3c2a" stroke-width="16" fill="none"/>'
    s += '<path d="M760,1350 C800,1250 900,1220 1000,1260 C1100,1220 1240,1250 1300,1350 Z" fill="#cfc6b0"/>'  # shirt fallen to the waist
    s += '<ellipse cx="500" cy="1280" rx="220" ry="50" fill="#a88a50"/><ellipse cx="500" cy="1260" rx="80" ry="50" fill="#8a7040"/>'
    s += f'<path d="M1300,760 C1320,900 1310,1150 1300,1350" stroke="#ff9a50" stroke-width="10" fill="none" opacity="0.6" filter="url(#blur1)"/>'
    return svg(s)


@art
def dawn_hill():
    s = sky("#2a3450", "#f0a060", "#8a6a7a") + glow(1700, 760, 500, "warm", 0.9)
    s += ridge(760, 200, "#2a2c3a", 3) + mist(820, 100, 0.4, "#ffd8c0", 4)
    s += '<path d="M0,1350 L0,1100 C600,900 1200,820 1700,800 C2000,790 2300,860 2400,900 L2400,1350 Z" fill="#14121a"/>'
    s += reed_hut(1500, 830, 0.9, glow_=False)
    for i, x in enumerate((300, 650, 1000, 1900, 2200)):
        s += maguey(x, 1040 if x < 1200 else 980, 1.1, "#0c0a10", i, "#ffb080")
    return svg(s)


@art
def hut_empty_dawn():
    s = interior("#3a3436", "#1a1618", (1800, 500))
    s += '<path d="M1700,0 L2100,0 L1600,1350 L1100,1350 Z" fill="#ffd8a0" opacity="0.12"/>'  # light through a broken wall
    s += fogon(1200, 1150, 1.3, fire=False, embers_only=True).replace("#ff8a2a", "#3a3436").replace("#ffcf5a", "#4a4446").replace("#c8320a", "#2a2426")
    s += '<path d="M500,1220 C520,1140 760,1120 860,1160 C880,1230 820,1280 620,1290 C500,1290 490,1260 500,1220 Z" fill="#a8a090"/>'  # clothes
    r = random.Random(3)
    for _ in range(60):  # salt
        s += f'<circle cx="{r.uniform(900,1500):.0f}" cy="{r.uniform(1180,1300):.0f}" r="{r.uniform(2,5):.1f}" fill="#f4f2ee" opacity="0.8"/>'
    s += strands(r, [(1300, 1220, 1400, 1180, 1500, 1230), (1320, 1240, 1420, 1200, 1520, 1250)], 30, "#050505", (2, 4), (0.6, 1.0), 20)
    return svg(s)


@art
def hut_ruin():
    s = sky("#3a4658", "#a0aab8") + ridge(780, 200, "#3a4250", 3) + mist(820, 120, 0.4, "#d8e2ea", 5)
    s += '<path d="M0,1350 L0,1050 C600,920 1200,880 1700,870 C2000,870 2300,920 2400,950 L2400,1350 Z" fill="#1c1e22"/>'
    s += reed_hut(1300, 960, 1.2, glow_=False, ruin=True)
    for i, x in enumerate((300, 600, 2000, 2250)):
        s += maguey(x, 1150, 1.3, "#0c0e12", i)
    return svg(s)


@art
def road_dog():
    s = moon_sky(20, 1900, 220, 90) + ridge(820, 100, "#070c14", 4)
    s += '<path d="M800,1350 C1000,1100 1100,950 1150,820 L1250,820 C1300,950 1500,1100 1800,1350 Z" fill="#1a2230"/>'
    s += ground(830, "#04060a", 8, 2).replace('fill="#04060a"', 'fill="#04060a" opacity="0.0"')
    s += tile_house(350, 1200, 600, 420, cross=True, lit=True, seed=40)
    s += G(1700, 1150, 0.7, beast_body(rim="#9fc2e8", eyes=True, sit=True), True)
    s += mist(1150, 100, 0.3, "#9ab4cc", 3) + maguey(2250, 1300, 1.5, "#020305", 5, "#7a9cc4")
    return svg(s)


@art
def xtabay_tease():
    s = moon_sky(21, 1700, 260, 120, "#02060a", "#0e2228")
    s += ground(1150, "#020406", 10, 2)
    # ceiba: huge straight trunk with buttress roots and flat crown
    s += '<path d="M1050,1200 C1000,1100 1080,900 1100,600 L1180,600 C1200,900 1280,1100 1230,1200 C1300,1220 1350,1260 1400,1280 L880,1280 C930,1260 980,1220 1050,1200 Z" fill="#030608"/>'
    s += '<path d="M600,620 C800,520 1000,500 1140,560 C1300,500 1600,520 1750,620 C1500,600 1300,640 1140,620 C1000,640 800,620 600,620 Z" fill="#030608"/>'
    for i in range(14):
        s += f'<path d="M1140,600 L{700+i*75},{560+(i%3)*30}" stroke="#030608" stroke-width="18"/>'
    # woman with very long hair, white huipil, glowing faintly beside the trunk
    s += ghost_woman(1400, 1180, 620, "#e9f1f7", 0.75)
    return svg(s)


if __name__ == "__main__":
    os.makedirs("art", exist_ok=True)
    names = sys.argv[1:] or list(ART)
    for n in names:
        open(f"art/{n}.svg", "w").write(ART[n]())
    print(len(names), "svg written")
