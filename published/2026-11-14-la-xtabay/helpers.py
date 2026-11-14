#!/usr/bin/env python3
"""Illustrations for 'El Nahual' — writes art/*.svg (2400x1350).
Render: node /home/claude/pipeline/render_svg.js art/*.svg      Usage: python3 make_art.py [name ...]"""
import sys, os, math, random
sys.path.insert(0, '/home/claude/pipeline'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from art import *
from scenery import *
from chars import *

ART0 = {}
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
