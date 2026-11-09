#!/usr/bin/env python3
"""Illustrations for 'La Llorona' — writes art/*.svg (2400x1350). Render: node /home/claude/pipeline/render_svg.js art/*.svg
Usage: python3 make_art.py [name ...]   (no names = all)"""
import sys, os, math, random
sys.path.insert(0, '/home/claude/pipeline'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from art import *
from chars import *

ART = {}
def art(fn):
    ART[fn.__name__] = fn
    return fn

def blur_ell(cx, cy, rx, ry, col, op, f=3):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{col}" opacity="{op}" filter="url(#blur{f})"/>'

def mist(y, h=120, op=0.25, col="#c8d8e6", seed=1, n=9, x0=0, x1=2400):
    r = random.Random(seed)
    return "".join(blur_ell(r.uniform(x0, x1), y + r.uniform(-h / 3, h / 3), r.uniform(250, 520), h * r.uniform(0.5, 1), col, round(op * r.uniform(0.6, 1.2), 2)) for _ in range(n))

def ripples(cx, cy, n=5, rx=120, ry=22, col="#cfe1f0", op=0.5, step=1.5):
    return "".join(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx*(1+i*step*0.4):.0f}" ry="{ry*(1+i*step*0.4):.0f}" fill="none" stroke="{col}" stroke-width="{3-i*0.4:.1f}" opacity="{op*(1-i/n):.2f}"/>' for i in range(n))

def willow_curtain(x0, x1, ytop=0, seed=3, color="#020406", n=70, L=(300, 800)):
    r = random.Random(seed); out = [f'<path d="M{x0-100},{ytop-10} Q{(x0+x1)/2},{ytop+120} {x1+100},{ytop-10}" stroke="{color}" stroke-width="26" fill="none"/>']
    for _ in range(n):
        x = r.uniform(x0, x1); l = r.uniform(*L); b = r.uniform(-40, 40)
        y0 = ytop + 60 * (1 - ((x - (x0 + x1) / 2) / ((x1 - x0) / 2 + 1)) ** 2)
        out.append(f'<path d="M{x:.0f},{y0:.0f} Q{x+b:.0f},{y0+l*0.5:.0f} {x+b*1.6:.0f},{y0+l:.0f}" stroke="{color}" stroke-width="{r.uniform(1.5,4):.1f}" fill="none"/>')
        for k in range(int(l / 40)):
            yy = y0 + k * 40 + r.uniform(0, 20); xx = x + b * (k * 40 / l) * 1.3
            out.append(f'<ellipse cx="{xx:.0f}" cy="{yy:.0f}" rx="4" ry="11" fill="{color}" transform="rotate({r.uniform(-30,30):.0f} {xx:.0f} {yy:.0f})"/>')
    return "".join(out)

def heno(x, y, w=200, L=260, seed=4, color="#1b2a2f", n=18):
    """Spanish moss (heno) hanging from ahuehuete branches."""
    r = random.Random(seed); out = []
    for _ in range(n):
        xx = x + r.uniform(-w / 2, w / 2); l = r.uniform(L * 0.4, L)
        out.append(f'<path d="M{xx:.0f},{y} q{r.uniform(-15,15):.0f},{l*0.5:.0f} {r.uniform(-10,10):.0f},{l:.0f}" stroke="{color}" stroke-width="{r.uniform(2,6):.1f}" fill="none" opacity="{r.uniform(0.5,0.9):.2f}"/>')
    return "".join(out)

def ground(y, color="#020406", amp=30, seed=2):
    r = random.Random(seed); pts = " ".join(f"{x},{y + r.uniform(-amp, amp):.0f}" for x in range(0, 2401, 120))
    return f'<polygon points="0,1350 {pts} 2400,1350" fill="{color}"/>'

def sil_person(x, y, h, kind="man", color="#030405", rim=None, facing=1):
    """Custom silhouette people (shadow theatre): kind man|woman|child|girl|charro|friar. (x,y)=feet."""
    u = h / 100.0; f = facing; p = []
    if kind in ("man", "charro"):
        p.append(f'<ellipse cx="{x}" cy="{y-90*u}" rx="{5*u}" ry="{6*u}"/>')
        if kind == "charro":
            p.append(f'<ellipse cx="{x}" cy="{y-94*u}" rx="{17*u}" ry="{2.6*u}"/><path d="M{x-6*u},{y-95*u} Q{x-5*u},{y-108*u} {x},{y-109*u} Q{x+5*u},{y-108*u} {x+6*u},{y-95*u} Z"/>')
        else:
            p.append(f'<ellipse cx="{x}" cy="{y-94*u}" rx="{10*u}" ry="{2*u}"/><path d="M{x-5*u},{y-95*u} L{x-4.5*u},{y-103*u} L{x+4.5*u},{y-103*u} L{x+5*u},{y-95*u} Z"/>')
        p.append(f'<path d="M{x-12*u},{y-80*u} Q{x},{y-86*u} {x+12*u},{y-80*u} L{x+13*u},{y-50*u} L{x+9*u},{y-46*u} L{x+7*u},{y} L{x+2*u},{y} L{x},{y-40*u} L{x-2*u},{y} L{x-7*u},{y} L{x-9*u},{y-46*u} L{x-13*u},{y-50*u} Z"/>')
        p.append(f'<path d="M{x-12*u},{y-80*u} Q{x-22*u},{y-60*u} {x-20*u},{y-35*u} L{x+20*u},{y-35*u} Q{x+22*u},{y-60*u} {x+12*u},{y-80*u} Z" opacity="0.95"/>')  # cape
    elif kind == "woman":
        p.append(f'<ellipse cx="{x}" cy="{y-91*u}" rx="{5*u}" ry="{6*u}"/>')
        p.append(f'<path d="M{x-6*u},{y-95*u} Q{x-14*u},{y-70*u} {x-13*u},{y-55*u} L{x+13*u},{y-55*u} Q{x+14*u},{y-70*u} {x+6*u},{y-95*u} Q{x},{y-99*u} {x-6*u},{y-95*u} Z"/>')  # rebozo
        p.append(f'<path d="M{x-9*u},{y-58*u} Q{x-14*u},{y-25*u} {x-19*u},{y} L{x+19*u},{y} Q{x+14*u},{y-25*u} {x+9*u},{y-58*u} Z"/>')
        p.append(f'<path d="M{x-4*u*f},{y-88*u} q{-3*u*f},{12*u} {-2*u*f},{24*u}" stroke="{color}" stroke-width="{2.2*u}" fill="none"/>')  # braid
    elif kind in ("child", "girl"):
        p.append(f'<ellipse cx="{x}" cy="{y-86*u}" rx="{7.5*u}" ry="{8.5*u}"/>')
        if kind == "girl":
            p.append(f'<path d="M{x-6*u},{y-82*u} q{-5*u},{14*u} {-3*u},{26*u} M{x+6*u},{y-82*u} q{5*u},{14*u} {3*u},{26*u}" stroke="{color}" stroke-width="{3*u}" fill="none"/>')
            p.append(f'<path d="M{x-9*u},{y-74*u} L{x+9*u},{y-74*u} L{x+16*u},{y-22*u} L{x-16*u},{y-22*u} Z"/><rect x="{x-6*u}" y="{y-24*u}" width="{4*u}" height="{24*u}"/><rect x="{x+2*u}" y="{y-24*u}" width="{4*u}" height="{24*u}"/>')
        else:
            p.append(f'<ellipse cx="{x}" cy="{y-92*u}" rx="{12*u}" ry="{2.6*u}"/><path d="M{x-6*u},{y-93*u} Q{x},{y-103*u} {x+6*u},{y-93*u} Z"/>')
            p.append(f'<path d="M{x-10*u},{y-75*u} L{x+10*u},{y-75*u} L{x+11*u},{y-40*u} L{x+8*u},{y} L{x+2*u},{y} L{x},{y-36*u} L{x-2*u},{y} L{x-8*u},{y} L{x-11*u},{y-40*u} Z"/>')
    elif kind == "friar":
        p.append(f'<path d="M{x-9*u},{y-82*u} Q{x-10*u},{y-102*u} {x+2*u*f},{y-102*u} Q{x+12*u},{y-100*u} {x+10*u},{y-82*u} Z"/>')
        p.append(f'<path d="M{x-14*u},{y-82*u} Q{x-22*u},{y-40*u} {x-22*u},{y} L{x+22*u},{y} Q{x+22*u},{y-40*u} {x+14*u},{y-82*u} Z"/>')
    body = "".join(p)
    s = ""
    if rim:
        s += f'<g fill="{rim}" filter="url(#blur1)" opacity="0.9" transform="translate({-3*f},-2)">{body}</g>'
    return s + f'<g fill="{color}">{body}</g>'

def horse(x, y, h, color="#030405", rim=None, facing=1, rider=None, eyes=None):
    """Horse silhouette (standing, head forward) with optional rider: None|'caballero'|'charro'. (x,y)=hooves baseline, h=withers height."""
    s = h / 400.0
    d = ("M-245,-385 C-150,-372 -40,-368 60,-385 C100,-395 130,-410 150,-440 C185,-500 215,-545 248,-568 L256,-600 L268,-570 "
         "C290,-560 310,-530 330,-490 C345,-460 362,-440 366,-424 C368,-410 352,-402 338,-406 C318,-412 300,-420 286,-432 "
         "C270,-440 255,-440 240,-450 C222,-420 205,-370 186,-320 C180,-290 170,-268 160,-255 "
         "L168,-140 L172,-30 L182,0 L150,0 L152,-30 L146,-140 L132,-240 "
         "L118,-240 L110,-140 L104,-30 L112,0 L84,0 L86,-30 L92,-140 L96,-245 "
         "C40,-250 -60,-250 -140,-262 L-150,-160 L-170,-110 L-160,-30 L-150,0 L-178,0 L-184,-30 L-196,-110 L-186,-170 "
         "L-205,-180 L-238,-118 L-232,-30 L-222,0 L-252,0 L-258,-30 L-264,-120 L-258,-200 C-272,-260 -272,-340 -245,-385 Z")
    tail = "M-245,-378 C-290,-370 -318,-300 -318,-200 C-316,-150 -300,-120 -290,-110 C-296,-170 -290,-250 -262,-320 Z"
    mane = "M150,-440 C185,-500 215,-545 248,-568 C236,-540 214,-500 196,-470 C180,-450 168,-430 160,-420 Z M150,-440 l-12,40 l24,-30 l-4,40 l22,-36 Z"
    parts = f'<path d="{d}"/><path d="{tail}"/><path d="{mane}"/>'
    if rider:
        hat = ('<ellipse cx="32" cy="-602" rx="82" ry="12"/><path d="M4,-606 Q6,-660 32,-664 Q58,-660 60,-606 Z"/>' if rider == "charro"
               else '<ellipse cx="32" cy="-600" rx="56" ry="9"/><path d="M12,-602 L16,-640 L48,-640 L52,-602 Z"/>')
        parts += ('<ellipse cx="32" cy="-578" rx="21" ry="25"/>' + hat +
                  '<path d="M0,-552 Q30,-562 58,-550 L62,-470 L48,-400 L-6,-396 L-10,-470 Z"/>'
                  '<path d="M2,-548 Q-50,-500 -90,-400 L-40,-392 Q-20,-470 20,-520 Z"/>'
                  '<path d="M8,-410 C30,-400 60,-380 66,-330 L52,-252 L36,-252 L48,-330 C40,-360 20,-380 -2,-392 Z"/>'
                  '<path d="M52,-540 Q90,-500 110,-460 L98,-452 Q80,-488 46,-516 Z"/>')
    body = f'<g transform="translate({x},{y}) scale({s*facing},{s})">{parts}</g>'
    out = ""
    if rim:
        out += f'<g fill="{rim}" filter="url(#blur1)" opacity="0.95"><g transform="translate({x+4*facing},{y-3}) scale({s*facing},{s})">{parts}</g></g>'
    out += f'<g fill="{color}">{body}</g>'
    if eyes:
        ex, ey = x + 300 * s * facing, y - 525 * s
        out += f'<circle cx="{ex}" cy="{ey}" r="{16*s}" fill="{eyes}" opacity="0.6" filter="url(#blur1)"/><circle cx="{ex}" cy="{ey}" r="{4.5*s}" fill="#ffd0b0"/>'
        if rider:
            for dx in (-7, 9):
                rx_, ry_ = x + (40 + dx) * s * facing, y - 580 * s
                out += f'<circle cx="{rx_}" cy="{ry_}" r="{10*s}" fill="{eyes}" opacity="0.6" filter="url(#blur1)"/><circle cx="{rx_}" cy="{ry_}" r="{3*s}" fill="#ffe0c0"/>'
    return out

# ============================================================================ RIVER (cold open)
@art
def rio_bg():
    return svg(sky('#040a13', '#1d3344', mid='#0c1a28'), stars(220, 3, 700), moon(1660, 250, 92),
               ridge(720, 150, '#0d1824', 5), ridge(790, 80, '#0a131d', 11, step=30),
               tree(330, 800, 520, 21, '#04080d', 'willow', 0.1), tree(2060, 805, 470, 8, '#04080d', 'willow', -0.1),
               tree(780, 800, 300, 5, '#060b11', 'willow'), reeds(0, 2400, 805, 7, '#04080d', 140, 90),
               water(800, 1350, '#1a2d3d', '#04080e'), reflection(1660, 805, 1350, width=200),
               mist(800, 90, 0.35, seed=3), mist(1000, 140, 0.18, seed=4))

@art
def rio_fg():
    return svg(willow_curtain(-80, 700, -20, 5, n=60, L=(250, 750)),
               '<path d="M0,1180 C300,1150 600,1220 1000,1240 C1500,1265 1900,1210 2400,1190 L2400,1350 L0,1350 Z" fill="#020407"/>',
               reeds(0, 2400, 1250, 3, '#020407', 170, 230),
               '<path d="M0,1180 C300,1150 600,1220 1000,1240" stroke="#5d7a92" stroke-width="3" fill="none" opacity="0.35"/>')

@art
def ll_far():      # tiny figure on the far bank, across the river
    return svg(place(llorona('stand', seed=3, mist=True), 1420, 840, 300))

@art
def ll_mid():      # medium, standing at the water's edge
    return svg(place(llorona('stand', seed=6), 1450, 1230, 820))

@art
def ll_big():      # tall, close, centred
    return svg(place(llorona('stand', seed=7, wind=1.4), 1200, 1500, 1500))

@art
def ll_reach():
    return svg(place(llorona('reach', seed=4, wind=1.2), 1000, 1420, 1250))

@art
def ll_face():
    return svg(llorona_face(cy=760, s=1.55))

@art
def ll_scream():
    return svg(llorona_face(scream=True, cy=740, s=1.6, seed=8))

@art
def cielo_luna():
    clouds = "".join(blur_ell(x, y, rx, ry, c, o, 3) for (x, y, rx, ry, c, o) in [
        (500, 420, 520, 70, '#2a3a4c', 0.8), (1700, 520, 600, 80, '#1d2b3a', 0.9), (1100, 300, 420, 50, '#33475a', 0.6),
        (2100, 260, 380, 60, '#253547', 0.7), (900, 700, 700, 90, '#0e1824', 0.9)])
    return svg(sky('#03070d', '#132232', mid='#0a1420'), stars(260, 9, 1000), moon(1200, 560, 160, halo=5),
               clouds, blur_ell(1200, 600, 300, 40, '#9fb6cc', 0.25, 2), ridge(1150, 90, '#05090e', 4), mist(1200, 100, 0.2, seed=8))

# ============================================================================ COLONIAL CITY
def facade_g(x, y, s, w, h, seed, lit, color="#0c1219"):
    return f'<g transform="translate({x},{y}) scale({s})">{facade(0, 0, w, h, color=color, seed=seed, lit=lit)}</g>'

@art
def calle():
    r = random.Random(12)
    road = '<polygon points="0,1350 2400,1350 1500,880 1100,880" fill="#121a22"/>'
    cob = "".join(f'<path d="M{1100 - (i/14)**1.7*1100:.0f},{880 + (i/14)**1.7*470:.0f} L{1500 + (i/14)**1.7*900:.0f},{880 + (i/14)**1.7*470:.0f}" stroke="#25313c" stroke-width="{1+i*0.3:.1f}" opacity="0.6"/>' for i in range(1, 15))
    wet = "".join(f'<ellipse cx="{r.uniform(900,1700):.0f}" cy="{r.uniform(960,1330):.0f}" rx="{r.uniform(40,160):.0f}" ry="{r.uniform(4,10):.0f}" fill="#9cb4c8" opacity="{r.uniform(0.08,0.2):.2f}"/>' for _ in range(26))
    left = ('<polygon points="0,180 900,640 1100,880 0,1350" fill="#0b1118"/>'
            '<polygon points="0,140 900,610 900,640 0,180" fill="#151e28"/>')
    right = ('<polygon points="2400,220 1560,650 1500,880 2400,1350" fill="#0a1017"/>'
             '<polygon points="2400,180 1560,620 1560,650 2400,220" fill="#141d27"/>')
    wins = ""
    for i, t in enumerate([0.12, 0.3, 0.48, 0.64, 0.78]):
        # left side windows in perspective
        x = t * 900; top = 180 + t * 460 + 60 * (1 - t); hh = 320 * (1 - t * 0.75); ww = 150 * (1 - t * 0.7)
        lit = i in (1, 3)
        wins += f'<polygon points="{x:.0f},{top+40:.0f} {x+ww:.0f},{top+40+ww*0.5:.0f} {x+ww:.0f},{top+40+ww*0.5+hh:.0f} {x:.0f},{top+40+hh:.0f}" fill="{"#e8a94e" if lit else "#060a0e"}" opacity="{0.9 if lit else 1}"/>'
        if lit: wins += glow(x + ww / 2, top + 40 + hh / 2, ww * 2, 'warm', 0.5)
        x2 = 2400 - t * 840; top2 = 220 + t * 430 + 60 * (1 - t)
        lit2 = i in (2,)
        wins += f'<polygon points="{x2:.0f},{top2+40:.0f} {x2-ww:.0f},{top2+40+ww*0.5:.0f} {x2-ww:.0f},{top2+40+ww*0.5+hh:.0f} {x2:.0f},{top2+40+hh:.0f}" fill="{"#e8a94e" if lit2 else "#060a0e"}"/>'
        if lit2: wins += glow(x2 - ww / 2, top2 + 40 + hh / 2, ww * 2, 'warm', 0.5)
        # balcony rails
        wins += f'<path d="M{x-10:.0f},{top+40+hh*0.62:.0f} l{ww+20:.0f},{(ww+20)*0.5:.0f}" stroke="#04070a" stroke-width="{8*(1-t*0.6):.0f}"/>'
    far = (f'<g transform="translate(1300,880) scale(0.42)">{church(0, 0, 1.0, "#0a1119")}</g>'
           '<rect x="1100" y="700" width="140" height="180" fill="#0d151e"/><rect x="1380" y="690" width="120" height="190" fill="#0d151e"/>')
    return svg(sky('#050b14', '#24384a', mid='#0f1d2b'), stars(120, 4, 500), moon(1520, 200, 70),
               far, road, cob, wet, left, right, wins, lamp(620, 1060, 520), lamp(1880, 1000, 440),
               '<ellipse cx="620" cy="1080" rx="260" ry="40" fill="#e8a94e" opacity="0.18" filter="url(#blur2)"/>',
               mist(900, 80, 0.25, seed=12, x0=900, x1=1700))

@art
def campanario():
    arch = ('<path d="M700,1350 L700,500 A500,500 0 0 1 1700,500 L1700,1350 Z" fill="#0d1a28"/>'
            '<path d="M780,1350 L780,520 A420,420 0 0 1 1620,520 L1620,1350 Z" fill="url(#moonglow)" opacity="0.4"/>')
    stone = "".join(f'<rect x="{x}" y="{y}" width="{w}" height="58" fill="#1a1712" stroke="#0a0806" stroke-width="5"/>'
                    for (x, y, w) in [(xx, yy, 180) for yy in range(0, 1350, 62) for xx in range(-90 if (yy // 62) % 2 else 0, 2400, 186)])
    mask = ('<defs><mask id="archm"><rect width="2400" height="1350" fill="#fff"/><path d="M760,1350 L760,520 A440,440 0 0 1 1640,520 L1640,1350 Z" fill="#000"/></mask></defs>')
    town = (f'<g opacity="0.9"><rect x="760" y="1000" width="880" height="350" fill="#060b11"/>' +
            "".join(f'<rect x="{760+i*70}" y="{1000-random.Random(i).uniform(0,120):.0f}" width="66" height="400" fill="#070c12"/>' for i in range(13)) +
            "".join(window(800 + i * 140, 1060, 26, 40, i % 3 == 0, False) for i in range(6)) + '</g>')
    sky_in = sky('#06101c', '#22394d', mid='#0f2030')
    return svg(sky_in, stars(80, 6, 900), moon(1350, 380, 70), town,
               f'{mask}<g mask="url(#archm)">{stone}<rect width="2400" height="1350" fill="#000" opacity="0.35"/></g>',
               '<path d="M760,520 A440,440 0 0 1 1640,520" stroke="#2b261d" stroke-width="30" fill="none"/>',
               '<rect x="1150" y="80" width="100" height="40" fill="#0a0806"/>',
               '<rect x="700" y="1300" width="1000" height="50" fill="#0a0806"/>')

@art
def campana():
    g = uid("bell")
    return svg(f'<defs><linearGradient id="{g}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#2a1d0e"/><stop offset="0.35" stop-color="#9a7238"/><stop offset="0.55" stop-color="#d6a85c"/><stop offset="1" stop-color="#3a2810"/></linearGradient></defs>'
               '<rect x="1190" y="100" width="20" height="160" fill="#140e08"/>'
               '<rect x="1060" y="96" width="280" height="30" rx="8" fill="#1b130a"/>'
               f'<path d="M1200,250 C1120,250 1090,300 1085,420 C1080,560 1040,640 980,700 L1420,700 C1360,640 1320,560 1315,420 C1310,300 1280,250 1200,250 Z" fill="url(#{g})"/>'
               '<rect x="972" y="690" width="456" height="30" rx="12" fill="#6f5024"/>'
               '<path d="M1080,470 L1320,470 M1060,600 L1340,600" stroke="#4a3416" stroke-width="8"/>'
               '<ellipse cx="1200" cy="740" rx="32" ry="38" fill="#1b130a"/>'
               '<path d="M1270,300 C1290,380 1296,500 1330,640" stroke="#ffe2a8" stroke-width="6" fill="none" opacity="0.6"/>')

@art
def ventana():
    """Colonial interior: barred window with moonlight, candle, mother hugging child."""
    walls = ('<rect width="2400" height="1350" fill="#120c08"/>'
             '<rect x="0" y="1080" width="2400" height="270" fill="#0b0705"/>')
    win = ('<rect x="1400" y="250" width="560" height="640" fill="#0d1d2e"/>'
           '<rect x="1400" y="250" width="560" height="640" fill="url(#moonglow)"/>'
           + "".join(f'<rect x="{1430+i*70}" y="250" width="14" height="640" fill="#080504"/>' for i in range(8)) +
           '<rect x="1380" y="230" width="600" height="30" fill="#2a1d12"/><rect x="1380" y="880" width="600" height="40" fill="#2a1d12"/>'
           '<polygon points="1400,890 1960,890 2300,1350 1100,1350" fill="#9fc0dd" opacity="0.10"/>')
    shutter = ('<path d="M1240,240 L1400,250 L1400,890 L1240,900 Z" fill="#1d130b"/><path d="M1960,250 L2120,240 L2120,900 L1960,890 Z" fill="#1d130b"/>')
    table = '<rect x="350" y="900" width="700" height="30" fill="#2a1a0e"/><rect x="400" y="930" width="24" height="250" fill="#1a1009"/><rect x="980" y="930" width="24" height="250" fill="#1a1009"/>'
    fam = (f'<g fill="#050302">'
           '<ellipse cx="760" cy="590" rx="46" ry="56"/>'
           '<path d="M700,560 Q680,700 640,900 L560,1200 L1000,1200 L930,900 Q880,700 820,560 Q760,520 700,560 Z"/>'  # rebozo over head & back
           '<ellipse cx="900" cy="720" rx="34" ry="40"/>'
           '<path d="M860,760 Q840,860 850,1000 L980,1000 Q980,860 950,760 Z"/>'
           '<path d="M800,700 Q880,700 930,760 L920,790 Q860,740 800,750 Z"/></g>')
    rim = ('<path d="M820,560 Q880,700 930,900" stroke="#ffb860" stroke-width="5" fill="none" opacity="0.6" filter="url(#blur1)"/>'
           '<path d="M930,690 Q940,720 934,760" stroke="#ffb860" stroke-width="4" fill="none" opacity="0.6"/>')
    return svg(walls, glow(560, 820, 700, 'warm', 0.55), win, shutter, table, candle(560, 900, 70, 18), fam, rim,
               '<rect x="0" y="0" width="2400" height="1350" fill="url(#paper)"/>')

@art
def plaza():
    r = random.Random(21)
    lake = water(760, 900, '#2b4458', '#0f1c28') + reflection(1800, 765, 900, width=160)
    ground_ = '<polygon points="0,1350 2400,1350 2400,900 0,900" fill="#141b22"/>'
    stones = "".join(f'<path d="M0,{900+i*i*3.6:.0f} L2400,{900+i*i*3.6:.0f}" stroke="#1f2a34" stroke-width="2"/>' for i in range(1, 14))
    cat = f'<g transform="translate(560,900) scale(0.62)">{church(0, 0, 1.0, "#0a1119")}</g>'
    arcade = ('<rect x="1050" y="720" width="700" height="180" fill="#0b121a"/>' +
              "".join(f'<path d="M{1070+i*84},900 L{1070+i*84},800 A32,32 0 0 1 {1134+i*84},800 L{1134+i*84},900 Z" fill="#05090d"/>' for i in range(8)))
    return svg(sky('#060c16', '#2a4256', mid='#122436'), stars(140, 7, 600), moon(1800, 330, 80),
               ridge(700, 120, '#16263a', 9), ridge(760, 60, '#1a2c40', 3, step=30), lake,
               mist(770, 50, 0.3, seed=21), cat, arcade, ground_, stones,
               '<ellipse cx="1500" cy="1050" rx="600" ry="60" fill="#a8c6e0" opacity="0.07" filter="url(#blur3)"/>')

@art
def ll_kneel():
    """La Llorona kneeling, seen from behind, veil flowing, in the plaza."""
    g = uid("kn")
    x, y = 1500, 1080
    return svg(f'<defs><linearGradient id="{g}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f4f8fb"/><stop offset="1" stop-color="#9db2c4"/></linearGradient></defs>',
               blur_ell(x, y - 100, 220, 160, '#cfe4f7', 0.25, 4),
               f'<path d="M{x-120},{y} C{x-110},{y-80} {x-80},{y-150} {x-50},{y-170} L{x+50},{y-170} C{x+80},{y-150} {x+110},{y-80} {x+140},{y} Z" fill="url(#{g})"/>',
               f'<ellipse cx="{x}" cy="{y-200}" rx="28" ry="34" fill="#050607"/>',
               hair_clumps(random.Random(3), [(x - 15, y - 210), (x + 15, y - 210)], (110, 160), 12, (10, 16), clumps=6, per=2),
               f'<path d="M{x-34},{y-226} C{x-80},{y-160} {x-140},{y-60} {x-170},{y+6} L{x+190},{y+6} C{x+150},{y-60} {x+80},{y-160} {x+34},{y-226} Q{x},{y-246} {x-34},{y-226} Z" fill="#eef5fb" opacity="0.45"/>',
               f'<path d="M{x-150},{y+4} C{x-60},{y+20} {x+80},{y+20} {x+200},{y+4}" stroke="#ffffff" stroke-width="3" fill="none" opacity="0.5"/>',
               blur_ell(x, y + 6, 240, 30, '#dbe9f5', 0.5, 2))

@art
def lago():
    return svg(sky('#050a12', '#20364a', mid='#0e1c2a'), stars(160, 13, 650), moon(700, 260, 70),
               ridge(700, 140, '#101d2b', 2), ridge(760, 50, '#0d1824', 8, step=26),
               water(760, 1350, '#203547', '#03070c'), reflection(700, 765, 1350, width=150),
               ripples(1500, 905, 6, 90, 14, op=0.35), mist(780, 80, 0.4, seed=5), mist(1000, 160, 0.15, seed=6),
               reeds(0, 900, 1300, 5, '#020407', 80, 330), reeds(1900, 2400, 1320, 9, '#020407', 50, 300))

@art
def cronista():
    """Early-1900s desk: oil lamp, open old book with an engraving of a veiled woman, stacked books."""
    r = random.Random(4)
    desk = '<rect x="0" y="900" width="2400" height="450" fill="#1e120a"/><rect x="0" y="900" width="2400" height="14" fill="#3a2414"/>'
    book = ('<path d="M600,1180 L1200,1110 L1800,1180 L1800,1230 L1200,1160 L600,1230 Z" fill="#2e1c10"/>'
            '<path d="M640,1170 Q900,1080 1200,1100 L1200,820 Q900,800 660,880 Z" fill="#d9c8a4"/>'
            '<path d="M1760,1170 Q1500,1080 1200,1100 L1200,820 Q1500,800 1740,880 Z" fill="#e2d2ae"/>'
            '<path d="M1200,820 L1200,1100" stroke="#8a7650" stroke-width="4"/>')
    lines = "".join(f'<path d="M{700+r.uniform(0,20):.0f},{910+i*24} Q900,{870+i*24} {1160-r.uniform(0,60):.0f},{860+i*24+2}" stroke="#5a4a32" stroke-width="5" opacity="0.6" fill="none"/>' for i in range(10))
    title = '<text x="1460" y="880" text-anchor="middle" font-family="IM FELL English" font-size="40" fill="#3a2a18">La Llorona</text>'
    engraving = (f'<g transform="translate(1320,1060) scale(0.19)"><rect x="-120" y="-860" width="1120" height="820" fill="#c8b48c"/>'
                 f'<g opacity="0.85">{place(llorona("stand", seed=9, glow=False, rim=None, mist=False), 440, -60, 760)}</g></g>')
    eng_tint = '<rect x="1297" y="896" width="213" height="156" fill="#7a5a30" opacity="0.35"/>'
    stack = "".join(f'<rect x="{1900+r.uniform(-10,10):.0f}" y="{900-(i+1)*70}" width="{360+r.uniform(-30,30):.0f}" height="66" rx="6" fill="{c}"/>' for i, c in enumerate(["#3b1f14", "#22301f", "#4a3018", "#1f2236"]))
    lamp_ = ('<ellipse cx="380" cy="700" rx="160" ry="200" fill="#ffd98a" opacity="0.18" filter="url(#blur3)"/>'
             '<path d="M330,890 L430,890 L410,840 L350,840 Z" fill="#6b4a20"/><ellipse cx="380" cy="760" rx="70" ry="90" fill="#fff0c8" opacity="0.55"/>'
             '<path d="M380,700 Q395,740 380,770 Q365,740 380,700 Z" fill="#ffd27a"/><rect x="345" y="600" width="70" height="40" fill="#3a2a14"/>')
    return svg('<rect width="2400" height="900" fill="#0d0805"/>', glow(380, 740, 1100, 'warm', 0.7), desk, stack, book, lines, title, engraving, eng_tint, lamp_,
               '<rect width="2400" height="1350" fill="url(#paper)"/>')


# ============================================================================ fixes / refinements of batch 1
def mother_child(x, y, s=1.0, color="#050302", rim="#ffb860"):
    """Seated mother in rebozo hugging a child, profile facing right. (x,y) = seat base."""
    body = (
        '<path d="M-60,-430 C-20,-470 50,-470 70,-420 C90,-380 86,-330 60,-300 C110,-260 150,-200 160,-120 L170,0 L-140,0 '
        'C-150,-120 -140,-250 -100,-330 C-110,-370 -90,-410 -60,-430 Z"/>'
        '<ellipse cx="40" cy="-380" rx="40" ry="48"/>'
        '<path d="M70,-392 L88,-372 L70,-362 Z"/>'
        '<ellipse cx="150" cy="-250" rx="44" ry="50"/>'
        '<path d="M110,-210 C90,-150 100,-60 130,-20 L230,-20 C240,-90 220,-170 190,-210 Z"/>'
        '<path d="M50,-300 C100,-300 160,-280 200,-240 L190,-215 C150,-250 100,-262 60,-262 Z"/>'
        '<path d="M30,-330 C-10,-260 -20,-120 -30,0" stroke="#000" stroke-width="6" fill="none" opacity="0.4"/>')
    rimp = ('<path d="M-60,-430 C-20,-470 50,-470 70,-420 C90,-380 86,-330 60,-300" stroke="RIM" stroke-width="7" fill="none" opacity="0.7"/>'
            '<path d="M194,-284 C200,-250 196,-226 190,-210" stroke="RIM" stroke-width="5" fill="none" opacity="0.6"/>'
            '<path d="M60,-300 C110,-260 150,-200 160,-120" stroke="RIM" stroke-width="5" fill="none" opacity="0.5"/>').replace("RIM", rim)
    return f'<g transform="translate({x},{y}) scale({s})"><g fill="{color}">{body}</g><g filter="url(#blur1)">{rimp}</g>{rimp}</g>'

@art
def ventana():
    """Colonial interior: barred window with moonlight, candle, mother hugging child."""
    walls = ('<rect width="2400" height="1350" fill="#120c08"/>'
             '<rect x="0" y="1080" width="2400" height="270" fill="#0b0705"/>')
    win = ('<rect x="1400" y="250" width="560" height="640" fill="#0d1d2e"/>'
           '<rect x="1400" y="250" width="560" height="640" fill="url(#moonglow)"/>'
           + "".join(f'<rect x="{1430+i*70}" y="250" width="14" height="640" fill="#080504"/>' for i in range(8)) +
           '<rect x="1380" y="230" width="600" height="30" fill="#2a1d12"/><rect x="1380" y="880" width="600" height="40" fill="#2a1d12"/>'
           '<polygon points="1400,920 1960,920 2250,1350 1150,1350" fill="#9fc0dd" opacity="0.05"/>'
           + "".join(f'<polygon points="{1440+i*70},920 {1452+i*70},920 {1500+i*100},1350 {1480+i*100},1350" fill="#000" opacity="0.25"/>' for i in range(8)))
    shutter = ('<path d="M1240,240 L1400,250 L1400,890 L1240,900 Z" fill="#1d130b"/><path d="M1960,250 L2120,240 L2120,900 L1960,890 Z" fill="#1d130b"/>'
               '<path d="M1260,300 L1380,305 M1260,500 L1380,505 M1260,700 L1380,705" stroke="#120b06" stroke-width="10"/>')
    table = '<rect x="250" y="900" width="560" height="30" fill="#2a1a0e"/><rect x="290" y="930" width="24" height="250" fill="#1a1009"/><rect x="760" y="930" width="24" height="250" fill="#1a1009"/>'
    bench = '<rect x="760" y="1080" width="520" height="40" fill="#1a1009"/>'
    return svg(walls, glow(520, 820, 760, 'warm', 0.6), win, shutter, table, candle(500, 900, 70, 18), bench,
               mother_child(960, 1090, 1.15), '<rect x="0" y="0" width="2400" height="1350" fill="url(#paper)"/>')

@art
def ll_kneel():
    """La Llorona kneeling, seen from behind, veil flowing on the stones, in the plaza."""
    g = uid("kn"); r = random.Random(3)
    x, y = 1500, 1080
    folds = "".join(f'<path d="M{x+dx*0.2:.0f},{y-200} C{x+dx*0.5:.0f},{y-130} {x+dx*0.85:.0f},{y-60} {x+dx:.0f},{y+4}" stroke="#ffffff" stroke-width="{r.uniform(2,4):.1f}" opacity="{r.uniform(0.2,0.45):.2f}" fill="none"/>' for dx in (-150, -90, -40, 10, 60, 120, 180))
    return svg(f'<defs><linearGradient id="{g}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f4f8fb"/><stop offset="1" stop-color="#9db2c4"/></linearGradient></defs>',
               blur_ell(x, y - 110, 240, 170, '#cfe4f7', 0.22, 4),
               f'<path d="M{x-130},{y} C{x-140},{y-60} {x-110},{y-150} {x-40},{y-180} C{x+20},{y-196} {x+70},{y-170} {x+100},{y-120} C{x+130},{y-70} {x+150},{y-30} {x+150},{y} Z" fill="url(#{g})"/>',
               f'<ellipse cx="{x-50}" cy="{y-196}" rx="27" ry="32" fill="#050607" transform="rotate(-25 {x-50} {y-196})"/>',
               hair_clumps(r, [(x - 60, y - 205), (x - 40, y - 210)], (90, 140), 10, (10, 16), clumps=6, per=2, dx_bias=10),
               f'<path d="M{x-80},{y-160} C{x-140},{y-200} {x-190},{y-250} {x-215},{y-300} L{x-200},{y-310} C{x-170},{y-262} {x-120},{y-220} {x-60},{y-185} Z" fill="url(#{g})"/>',
               f'<path d="M{x-218},{y-300} l-8,-22 l6,-2 l8,18 l-2,-24 l6,0 l2,24 l4,-20 l6,2 l-4,24 Z" fill="#e3ebf1"/>',
               f'<path d="M{x-82},{y-216} C{x-150},{y-140} {x-200},{y-50} {x-230},{y+6} L{x+230},{y+6} C{x+170},{y-60} {x+90},{y-150} {x+10},{y-215} Q{x-40},{y-240} {x-82},{y-216} Z" fill="#eef5fb" opacity="0.42"/>',
               folds, f'<path d="M{x-220},{y+4} C{x-80},{y+22} {x+80},{y+22} {x+230},{y+4}" stroke="#ffffff" stroke-width="3" fill="none" opacity="0.5"/>',
               blur_ell(x, y + 6, 280, 32, '#dbe9f5', 0.45, 2))

# ============================================================================ MARÍA'S STORY
def braid(x0, y0, x1, y1, w=26, color="#070505", hl="#3a2a24"):
    n = int(math.hypot(x1 - x0, y1 - y0) / (w * 0.9)); out = []
    for i in range(n):
        t = i / n; x = x0 + (x1 - x0) * t + math.sin(t * 3) * 6; y = y0 + (y1 - y0) * t; ww = w * (1 - t * 0.35)
        ang = 25 if i % 2 else -25
        out.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{ww*0.62:.0f}" ry="{ww*0.55:.0f}" fill="{color}" transform="rotate({ang} {x:.0f} {y:.0f})"/>'
                   f'<path d="M{x-ww*0.4:.0f},{y-ww*0.1:.0f} q{ww*0.4:.0f},{-ww*0.3:.0f} {ww*0.8:.0f},0" stroke="{hl}" stroke-width="2" fill="none" opacity="0.7" transform="rotate({ang} {x:.0f} {y:.0f})"/>')
    return "".join(out)

def maria_face(cx=1200, cy=640, s=1.0, sad=False):
    g = uid("mf")
    defs = (f'<defs><radialGradient id="{g}sk" cx="0.38" cy="0.4" r="0.75"><stop offset="0" stop-color="#e2a77a"/><stop offset="0.55" stop-color="#b9774c"/><stop offset="1" stop-color="#6e3f25"/></radialGradient>'
            f'<linearGradient id="{g}rb" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2f4b5a"/><stop offset="1" stop-color="#16262f"/></linearGradient>'
            f'<linearGradient id="{g}bl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f3e9d8"/><stop offset="1" stop-color="#c9b89a"/></linearGradient></defs>')
    L = []
    L.append('<path d="M-170,-120 C-180,-260 -90,-300 0,-300 C90,-300 180,-260 170,-120 C175,-40 170,40 150,90 L-150,90 C-170,40 -175,-40 -170,-120 Z" fill="#0a0706"/>')
    L.append(f'<path d="M-70,150 L-80,330 Q0,360 80,330 L70,150 Z" fill="url(#{g}sk)"/>')
    L.append(f'<path d="M-460,700 C-430,500 -300,400 -120,370 Q0,400 120,370 C300,400 430,500 460,700 Z" fill="url(#{g}bl)"/>')
    L.append("".join(f'<circle cx="{-110+i*20}" cy="{372+abs(i-5.5)*1.8:.0f}" r="6" fill="{["#b5332e","#2f6d4a","#d39a2b"][i%3]}"/>' for i in range(12)))
    L.append('<path d="M-120,370 Q0,410 120,370" stroke="#8a2c26" stroke-width="5" fill="none"/>')
    L.append(f'<path d="M-470,700 C-450,520 -360,420 -230,390 C-200,470 -190,560 -150,700 Z" fill="url(#{g}rb)"/>'
             f'<path d="M470,700 C450,520 360,420 230,390 C200,470 190,560 150,700 Z" fill="url(#{g}rb)"/>')
    L.append("".join(f'<path d="M{-430+i*12},{560+i*10} L{-200+i*6},{420+i*16}" stroke="#4d7384" stroke-width="2" opacity="0.5"/>' for i in range(10)))
    L.append("".join(f'<path d="M{430-i*12},{560+i*10} L{200-i*6},{420+i*16}" stroke="#4d7384" stroke-width="2" opacity="0.5"/>' for i in range(10)))
    L.append(f'<path d="M-150,-70 C-155,-210 -80,-262 0,-262 C80,-262 155,-210 150,-70 C148,40 120,140 70,200 C45,226 20,236 0,236 C-20,236 -45,226 -70,200 C-120,140 -148,40 -150,-70 Z" fill="url(#{g}sk)"/>')
    L.append('<ellipse cx="-92" cy="70" rx="44" ry="30" fill="#c9604a" opacity="0.25" filter="url(#blur2)"/><ellipse cx="92" cy="70" rx="44" ry="30" fill="#c9604a" opacity="0.2" filter="url(#blur2)"/>')
    for sx in (-1, 1):
        ex = sx * 64
        L.append(f'<path d="M{ex-46},-10 Q{ex},-46 {ex+46},-10 Q{ex},14 {ex-46},-10 Z" fill="#f1e6d6"/>')
        if sad:
            L.append(f'<circle cx="{ex+sx*2}" cy="-6" r="21" fill="#3a2214"/><circle cx="{ex+sx*2}" cy="-6" r="11" fill="#0a0503"/><circle cx="{ex+sx*2+6}" cy="-12" r="4" fill="#fff"/>')
            L.append(f'<path d="M{ex-48},-12 Q{ex},-40 {ex+48},-12 L{ex+48},-30 L{ex-48},-30 Z" fill="#9a5c38"/>')   # heavy lids
            L.append(f'<path d="M{ex-sx*8},8 C{ex-sx*12},60 {ex-sx*4},110 {ex-sx*10},170" stroke="#dfeaf2" stroke-width="7" fill="none" opacity="0.75"/>')
        else:
            L.append(f'<circle cx="{ex+sx*2}" cy="-14" r="21" fill="#3a2214"/><circle cx="{ex+sx*2}" cy="-14" r="11" fill="#0a0503"/><circle cx="{ex+sx*2+7}" cy="-21" r="5" fill="#fff"/>')
        L.append(f'<path d="M{ex-50},-8 Q{ex},-52 {ex+50},-10" stroke="#120a06" stroke-width="7" fill="none" stroke-linecap="round"/>')
        L.append(f'<path d="M{ex+sx*46},-12 l{sx*14},-10" stroke="#120a06" stroke-width="5" stroke-linecap="round"/>')
        L.append(f'<path d="M{ex-sx*30},-76 Q{ex+sx*10},-102 {ex+sx*56},-80" stroke="#140c08" stroke-width="8" fill="none" stroke-linecap="round"/>')
    L.append('<path d="M-4,-6 C-8,40 -22,70 -26,88 Q0,104 26,88 C22,70 8,40 4,-6" fill="#a8653f" opacity="0.5"/>'
             '<path d="M-24,90 Q-12,84 -4,92 M4,92 Q12,84 24,90" stroke="#4a2414" stroke-width="5" fill="none"/>')
    L.append('<path d="M-52,150 Q-24,130 0,140 Q24,130 52,150 Q24,158 0,156 Q-24,158 -52,150 Z" fill="#8f3b30"/>'
             '<path d="M-52,150 Q0,190 52,150 Q24,158 0,156 Q-24,158 -52,150 Z" fill="#a8483a"/>'
             '<path d="M-48,151 Q0,160 48,151" stroke="#4a1a14" stroke-width="3" fill="none"/>'
             '<path d="M-10,166 Q0,170 10,166" stroke="#e8a080" stroke-width="3" fill="none" opacity="0.6"/>')
    L.append('<path d="M0,-266 C-100,-270 -170,-210 -168,-90 L-150,-60 C-150,-170 -90,-236 -2,-244 Z" fill="#0a0706"/>'
             '<path d="M0,-266 C100,-270 170,-210 168,-90 L150,-60 C150,-170 90,-236 2,-244 Z" fill="#0a0706"/>'
             '<path d="M-6,-262 C-60,-256 -120,-220 -150,-150" stroke="#4a3830" stroke-width="3" fill="none" opacity="0.7"/>'
             '<path d="M6,-262 C60,-256 120,-220 150,-150" stroke="#4a3830" stroke-width="3" fill="none" opacity="0.5"/>')
    L.append(braid(-150, 40, -200, 640, 34) + braid(150, 40, 190, 620, 34))
    L.append('<path d="M-205,600 l-20,40 l40,-6 Z M195,590 l-16,44 l38,-10 Z" fill="#b5332e"/>')
    L.append('<circle cx="-152" cy="40" r="22" fill="none" stroke="#d8a840" stroke-width="5"/><circle cx="152" cy="40" r="22" fill="none" stroke="#d8a840" stroke-width="5"/>')
    L.append('<path d="M-150,-70 C-148,40 -120,140 -70,200" stroke="#ffcf8a" stroke-width="16" fill="none" opacity="0.45" filter="url(#blur2)"/>')
    return defs + f'<g transform="translate({cx},{cy}) scale({s})">{"".join(L)}</g>'

@art
def maria():
    wall = ('<rect width="2400" height="1350" fill="#7a4a2a"/>' + "".join(
        f'<rect x="{x}" y="{y}" width="230" height="100" fill="#6a3f22" opacity="0.35" stroke="#4d2c16" stroke-width="3"/>'
        for y in range(0, 1350, 104) for x in range(-115 if (y // 104) % 2 else 0, 2400, 234)))
    bug = "".join(f'<circle cx="{random.Random(i).uniform(0,700):.0f}" cy="{random.Random(i+50).uniform(0,500):.0f}" r="{random.Random(i+9).uniform(14,30):.0f}" fill="{["#b3245a","#d0346e","#8e1c48"][i%3]}" opacity="0.9"/>' for i in range(60))
    return svg(wall, glow(400, 300, 1200, 'warm', 0.6), bug, maria_face(1250, 560, 1.15),
               '<rect width="2400" height="1350" fill="url(#paper)"/>')

@art
def pueblo():
    r = random.Random(5)
    houses = ""
    for i, (x, w, h) in enumerate([(120, 360, 260), (520, 300, 220), (1500, 340, 240), (1880, 420, 280)]):
        y = 1000
        houses += (f'<rect x="{x}" y="{y-h}" width="{w}" height="{h}" fill="#4a2c1c"/>'
                   f'<rect x="{x-10}" y="{y-h-14}" width="{w+20}" height="18" fill="#3a2214"/>'
                   + "".join(f'<rect x="{x-6+k*26}" y="{y-h-26}" width="14" height="14" fill="#2a170c"/>' for k in range(int(w / 26) + 1)) +
                   f'<rect x="{x+w*0.4:.0f}" y="{y-150}" width="{w*0.2:.0f}" height="150" fill="#1d0f08"/>'
                   f'<rect x="{x+w*0.12:.0f}" y="{y-h+60}" width="46" height="60" fill="#1d0f08"/>')
    ch = f'<g transform="translate(1140,1000) scale(0.55)">{church(0, 0, 1.0, "#3c2416", lit_windows=False)}</g>'
    volcano = '<path d="M500,760 L1000,330 Q1060,300 1120,330 L1700,760 Z" fill="#6b4a3a"/><path d="M960,365 Q1060,290 1160,365 L1120,420 Q1060,380 1000,420 Z" fill="#efe0cc"/>'
    river = '<path d="M0,1180 C600,1120 1200,1260 2400,1150 L2400,1350 L0,1350 Z" fill="#6f8a8c"/>' + "".join(f'<path d="M{r.uniform(0,2300):.0f},{r.uniform(1200,1330):.0f} l{r.uniform(40,120):.0f},0" stroke="#e8d8b0" stroke-width="3" opacity="0.5"/>' for _ in range(30))
    magueys = "".join(f'<g transform="translate({x},1100)">' + "".join(f'<path d="M0,0 Q{a*0.5:.0f},-80 {a:.0f},-{140+abs(a)*0.3:.0f} Q{a*0.35:.0f},-60 8,0 Z" fill="#2d3a22"/>' for a in (-120, -70, -25, 20, 70, 115)) + '</g>' for x in (80, 380, 2250))
    return svg(sky('#d89a5a', '#f2cf8e', mid='#e8b070'), glow(1800, 420, 900, 'warm', 0.7),
               '<circle cx="1800" cy="440" r="90" fill="#fff0c0" opacity="0.9"/>', volcano,
               ridge(820, 120, '#8a5c3e', 3), ground(1000, '#5a3a24', 10), houses, ch,
               '<rect x="0" y="1000" width="2400" height="200" fill="#6a4628"/>', river, magueys,
               '<rect width="2400" height="1350" fill="url(#paper)"/>')

@art
def caballero():
    return svg(horse(1100, 1180, 430, '#0c0705', '#ffcf8a', 1, 'caballero'))

@art
def visita():
    wall = '<rect x="0" y="380" width="2400" height="970" fill="#1a120d"/>' + "".join(f'<path d="M0,{y} L2400,{y}" stroke="#120b07" stroke-width="3"/>' for y in range(430, 1150, 70))
    door = ('<rect x="1100" y="560" width="300" height="560" fill="#ffcf7a"/>' + glow(1250, 840, 600, 'warm', 0.8) +
            '<path d="M1100,560 L1020,580 L1020,1130 L1100,1120 Z" fill="#3a2414"/>')
    woman = sil_person(1260, 1120, 470, 'woman', '#120904')
    man = sil_person(1600, 1180, 560, 'man', '#030202', '#ffb15a', -1)
    return svg(sky('#060b14', '#1c2c3c'), stars(140, 8, 380), moon(400, 200, 60), wall,
               '<rect x="-20" y="360" width="2440" height="36" fill="#0f0905"/>', door, woman, glow(1225, 780, 120, 'warm', 0.9), man,
               '<rect x="0" y="1150" width="2400" height="200" fill="#0b0705"/>',
               '<polygon points="1100,1150 1400,1150 1600,1350 900,1350" fill="#ffcf7a" opacity="0.18"/>')

@art
def familia():
    t = tree(1700, 1080, 780, 31, '#1a0e08', 'ahuehuete', -0.05)
    people = (sil_person(900, 1100, 430, 'woman', '#1a0e08', None, 1) + sil_person(1250, 1100, 300, "man", "#1a0e08") +
              sil_person(1430, 1100, 210, 'child', '#1a0e08') + sil_person(1560, 1100, 180, 'girl', '#1a0e08'))
    toy = '<circle cx="1360" cy="985" r="16" fill="#1a0e08"/><path d="M1360,1000 l0,30" stroke="#1a0e08" stroke-width="5"/>'
    return svg(sky('#e8a860', '#f6d9a0', mid='#efbe78'), '<circle cx="600" cy="760" r="140" fill="#fff2c8" opacity="0.95"/>',
               glow(600, 760, 900, 'warm', 0.8), ridge(900, 100, '#b0703e', 4), ridge(980, 50, '#8a5432', 7),
               '<rect x="0" y="1080" width="2400" height="270" fill="#1a0e08"/>', t, people, toy,
               reeds(0, 2400, 1100, 3, '#1a0e08', 60, 90), '<rect width="2400" height="1350" fill="url(#paper)"/>')

@art
def boda():
    r = random.Random(8)
    ch = f'<g transform="translate(1350,1000) scale(1.05)">{church(0, 0, 1.0, "#6a4a32", lit_windows=True)}</g>'
    door = '<path d="M1277,1000 L1277,790 A73,73 0 0 1 1423,790 L1423,1000 Z" fill="#ffd890"/>' + glow(1350, 900, 300, 'warm', 0.8)
    couple = sil_person(1320, 1010, 190, 'man', '#2a1a10') + sil_person(1385, 1010, 175, "woman", "#efe4cf")
    crowd = "".join(sil_person(x, 1040 + r.uniform(0, 30), r.uniform(150, 190), r.choice(['man', 'woman']), '#3a2618') for x in list(range(950, 1250, 60)) + list(range(1480, 1800, 60)))
    petals = "".join(f'<circle cx="{r.uniform(1100,1650):.0f}" cy="{r.uniform(700,1000):.0f}" r="{r.uniform(3,7):.0f}" fill="#fff4e0" opacity="0.8"/>' for _ in range(50))
    maria_back = ('<g fill="#0d0805"><ellipse cx="420" cy="760" rx="70" ry="84"/>'
                  '<path d="M330,720 Q300,900 240,1350 L700,1350 Q600,900 520,720 Q430,660 330,720 Z"/>'
                  '<path d="M380,800 q-20,120 -10,240" stroke="#0d0805" stroke-width="24" fill="none"/></g>'
                  '<path d="M520,720 Q600,900 700,1350" stroke="#ffcf8a" stroke-width="8" fill="none" opacity="0.5" filter="url(#blur1)"/>')
    return svg(sky('#d8b88a', '#f2e0bc'), '<rect x="0" y="1000" width="2400" height="350" fill="#a07850"/>',
               ch, door, crowd, couple, petals, papel_picado(40, n=9, seed=4, opacity=0.85), maria_back, '<rect width="2400" height="1350" fill="url(#paper)"/>')

@art
def orilla_ninos():
    fam = ('<g fill="#030405">' + sil_person(1150, 1120, 420, "woman", "#030405") +
           sil_person(1000, 1120, 190, "child", "#030405") + sil_person(1290, 1120, 165, "girl", "#030405") +
           '<path d="M1010,1010 Q1060,990 1110,960" stroke="#030405" stroke-width="12" fill="none"/>'
           '<path d="M1190,960 Q1240,990 1282,1020" stroke="#030405" stroke-width="12" fill="none"/></g>')
    rimf = ('<g filter="url(#blur1)" opacity="0.8">' + sil_person(1153, 1118, 420, "woman", "#bcd8f0") + sil_person(1003, 1118, 190, "child", "#bcd8f0") + sil_person(1293, 1118, 165, "girl", "#bcd8f0") + '</g>')
    return svg(sky('#03070d', '#22394c', mid='#0d1b2a'), stars(150, 21, 600), moon(1200, 420, 260, halo=3.2),
               ridge(820, 90, '#0a1520', 13), water(820, 1120, '#3a5468', '#0b1520'), reflection(1200, 825, 1120, width=380),
               mist(830, 60, 0.3, seed=9), '<path d="M0,1100 C600,1080 1800,1090 2400,1100 L2400,1350 L0,1350 Z" fill="#020305"/>',
               reeds(0, 800, 1110, 4, '#020305', 50, 160), reeds(1600, 2400, 1110, 6, '#020305', 50, 160), rimf, fam)

@art
def rio_crecido():
    r = random.Random(14)
    waves = ""
    for i in range(70):
        y = 760 + (i / 70) ** 1.3 * 600; x = r.uniform(-100, 2400); w = 60 + (y - 760) * 0.6
        waves += f'<path d="M{x:.0f},{y:.0f} q{w/2:.0f},{-w*0.18:.0f} {w:.0f},0" stroke="#c8d8e4" stroke-width="{1+(y-760)/150:.1f}" fill="none" opacity="{r.uniform(0.2,0.55):.2f}"/>'
    branches = "".join(f'<path d="M{x},{y} l{r.uniform(60,160):.0f},{r.uniform(-30,30):.0f} m-40,0 l30,-30" stroke="#05080b" stroke-width="8" fill="none"/>' for x, y in [(400, 1000), (1500, 1120), (1900, 900), (900, 1250)])
    clouds = "".join(blur_ell(r.uniform(0, 2400), r.uniform(80, 500), r.uniform(300, 600), r.uniform(60, 120), '#1a2430', 0.9, 3) for _ in range(9))
    return svg(sky('#0a1018', '#2a3846'), clouds, '<path d="M1600,0 L1560,180 L1620,200 L1540,420" stroke="#e6f0ff" stroke-width="5" fill="none" opacity="0.7" filter="url(#glow)"/>',
               ridge(720, 140, '#0b1219', 3), tree(250, 760, 420, 2, '#05080b', 'bare', 0.25), tree(2150, 770, 380, 6, '#05080b', 'bare', -0.3),
               water(740, 1350, '#2a3c4a', '#070c11'), waves, branches, mist(760, 70, 0.3, seed=15))

@art
def ondas():
    straw = "".join(f'<path d="M{math.cos(t)*62:.0f},{math.sin(t)*22-6:.0f} L{math.cos(t)*150:.0f},{math.sin(t)*48:.0f}" stroke="#8a6a32" stroke-width="2" opacity="0.6"/>' for t in [i * 0.35 for i in range(18)])
    hat = ('<g transform="translate(1320,820) rotate(-8)">'
           '<ellipse cx="0" cy="6" rx="160" ry="52" fill="#0c141a" opacity="0.6" filter="url(#blur2)"/>'
           '<ellipse cx="0" cy="0" rx="152" ry="50" fill="#b8924e"/>' + straw +
           '<ellipse cx="0" cy="0" rx="152" ry="50" fill="none" stroke="#7a5a28" stroke-width="5"/>'
           '<path d="M-64,-6 C-66,-60 -34,-92 0,-92 C34,-92 66,-60 64,-6 Z" fill="#d2ad62"/>'
           '<path d="M-20,-86 C-6,-60 -4,-30 -8,-6" stroke="#9a7838" stroke-width="5" fill="none"/>'
           '<path d="M-64,-12 C-30,6 30,6 64,-12 L64,-28 C30,-10 -30,-10 -64,-28 Z" fill="#5a1e18"/>'
           '<path d="M30,-80 C50,-60 58,-40 56,-20" stroke="#f2dca0" stroke-width="5" fill="none" opacity="0.7"/></g>')
    flower = '<g transform="translate(820,960)">' + "".join(f'<ellipse cx="{math.cos(a)*18:.0f}" cy="{math.sin(a)*8:.0f}" rx="20" ry="9" fill="#f2f2ea" transform="rotate({math.degrees(a):.0f})"/>' for a in [i * 0.9 for i in range(7)]) + '<circle r="7" fill="#e8c860"/></g>'
    return svg(water(0, 1350, '#1c3040', '#03070b'), reflection(1650, 0, 1350, width=260, seed=3),
               ripples(1320, 830, 8, 170, 46, op=0.55, step=1.6), ripples(820, 965, 5, 60, 16, op=0.4),
               hat, flower)

@art
def maria_agua():
    g = uid("ma")
    return svg(f'<defs><clipPath id="{g}"><rect x="0" y="0" width="2400" height="1000"/></clipPath></defs>',
               f'<g clip-path="url(#{g})">{place(llorona("reach", seed=12, glow=False, wind=2.0, mist=False), 1150, 1700, 1300)}</g>',
               '<path d="M700,1000 Q1150,960 1650,1000 Q1150,1040 700,1000 Z" fill="#dfe9f2" opacity="0.6"/>',
               ripples(1150, 1002, 4, 260, 26, op=0.5))

@art
def juicio():
    r = random.Random(2)
    clouds = "".join(blur_ell(r.uniform(0, 2400), r.uniform(0, 420), r.uniform(300, 600), r.uniform(80, 150), '#1c2733', 0.95, 3) for _ in range(12))
    beam = '<polygon points="1100,0 1300,0 1520,1150 880,1150" fill="#dfeeff" opacity="0.22" filter="url(#blur3)"/><polygon points="1160,0 1240,0 1330,1150 1070,1150" fill="#ffffff" opacity="0.18" filter="url(#blur2)"/>'
    return svg(sky('#05080d', '#121b25'), clouds, blur_ell(1200, 60, 260, 90, '#ffffff', 0.6, 3), beam,
               '<path d="M0,1150 C600,1120 1800,1130 2400,1150 L2400,1350 L0,1350 Z" fill="#05070a"/>',
               blur_ell(1200, 1150, 300, 30, '#dfeeff', 0.4, 2),
               place(llorona("mourn", seed=13, glow=True, mist=True), 1200, 1160, 300))


# ============================================================================ PRE-HISPANIC / HISTORY
def pyramid(x, y, w, h, color="#2a1c12", steps=5, shrines=2, lit=None, hi="#5a4030"):
    """Mexica stepped pyramid with central double staircase and shrines on top."""
    s = ""
    for i in range(steps):
        ww = w * (1 - i * 0.13); hh = h / steps; yy = y - (i + 1) * hh
        s += f'<rect x="{x-ww/2:.0f}" y="{yy:.0f}" width="{ww:.0f}" height="{hh+1:.0f}" fill="{color}"/><rect x="{x-ww/2:.0f}" y="{yy:.0f}" width="{ww:.0f}" height="4" fill="{hi}" opacity="0.6"/>'
    tw = w * (1 - steps * 0.13)
    s += f'<polygon points="{x-w*0.16:.0f},{y} {x+w*0.16:.0f},{y} {x+tw*0.3:.0f},{y-h} {x-tw*0.3:.0f},{y-h}" fill="{hi}" opacity="0.55"/>'
    s += "".join(f'<path d="M{x-w*0.16+(w*0.16-tw*0.3)*k/12:.0f},{y-h*k/12:.0f} L{x+w*0.16-(w*0.16-tw*0.3)*k/12:.0f},{y-h*k/12:.0f}" stroke="{color}" stroke-width="2"/>' for k in range(12))
    if shrines:
        sw = tw * 0.42
        for j, sx in enumerate([x - tw * 0.24, x + tw * 0.24] if shrines == 2 else [x]):
            s += f'<rect x="{sx-sw/2:.0f}" y="{y-h-sw*0.9:.0f}" width="{sw:.0f}" height="{sw*0.9:.0f}" fill="{color}"/>'
            s += f'<rect x="{sx-sw*0.2:.0f}" y="{y-h-sw*0.55:.0f}" width="{sw*0.4:.0f}" height="{sw*0.55:.0f}" fill="{lit or "#0a0604"}"/>'
            roof = (f'<polygon points="{sx-sw*0.6:.0f},{y-h-sw*0.9:.0f} {sx+sw*0.6:.0f},{y-h-sw*0.9:.0f} {sx+sw*0.45:.0f},{y-h-sw*1.5:.0f} {sx-sw*0.45:.0f},{y-h-sw*1.5:.0f}" fill="{color}"/>'
                    + "".join(f'<rect x="{sx-sw*0.45+k*sw*0.18:.0f}" y="{y-h-sw*1.68:.0f}" width="{sw*0.1:.0f}" height="{sw*0.2:.0f}" fill="{color}"/>' for k in range(6)))
            s += roof
            if lit: s += glow(sx, y - h - sw * 0.3, sw * 1.2, 'warm', 0.8)
    return s

def canoe(x, y, L=260, color="#050302", poler=True):
    s = f'<path d="M{x-L/2},{y} Q{x},{y+28} {x+L/2},{y} L{x+L/2-20},{y-10} L{x-L/2+20},{y-10} Z" fill="{color}"/>'
    if poler:
        s += sil_person(x - L * 0.2, y - 8, L * 0.55, 'man', color)
        s += f'<path d="M{x-L*0.32},{y-L*0.45} L{x-L*0.6},{y+40}" stroke="{color}" stroke-width="5"/>'
    return s

@art
def tenochtitlan():
    r = random.Random(3)
    volc = ('<path d="M200,700 L620,360 Q680,330 740,360 L1150,700 Z" fill="#2a3440"/><path d="M590,385 Q680,330 770,385 L730,420 Q680,395 630,420 Z" fill="#c9d2da" opacity="0.8"/>'
            '<path d="M1300,700 C1450,560 1560,500 1700,470 C1800,450 1900,500 2000,540 C2100,590 2250,650 2400,700 Z" fill="#26303c"/><path d="M1640,480 C1700,460 1800,460 1860,490 L1800,510 C1760,490 1700,490 1660,505 Z" fill="#c9d2da" opacity="0.7"/>')
    houses = "".join(f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{860-y:.0f}" fill="#120c08"/>' for x, y, w in [(r.uniform(0, 2400), r.uniform(800, 830), r.uniform(60, 140)) for _ in range(60)])
    fires = "".join(glow(x, y, 50, 'warm', 0.8) + f'<circle cx="{x}" cy="{y}" r="5" fill="#ffd27a"/>' for x, y in [(r.uniform(0, 2400), r.uniform(800, 850)) for _ in range(18)])
    temples = (pyramid(1200, 860, 620, 300, '#1c120b', 5, 2, lit='#ff9a3c') + pyramid(640, 860, 300, 150, '#160e09', 4, 1, lit='#ffb050') +
               pyramid(1760, 860, 280, 140, '#160e09', 4, 1) + pyramid(260, 860, 200, 100, '#120b07', 3, 1))
    lake = water(860, 1350, '#3a3a40', '#0b0b10') + reflection(1200, 865, 1200, color='#ffb050', width=120, seed=2) + reflection(1900, 865, 1350, width=160, seed=7)
    causeway = '<polygon points="0,1000 2400,940 2400,960 0,1024" fill="#100a06"/>'
    canoes = canoe(500, 1180, 300) + canoe(1600, 1100, 220) + canoe(2000, 1260, 360)
    return svg(sky('#05080e', '#2a2a30', mid='#12151c'), stars(200, 31, 600), moon(1900, 220, 70), volc,
               mist(700, 60, 0.2, seed=3), houses, temples, fires, lake, causeway, canoes, mist(900, 50, 0.25, seed=7))

@art
def cometa():
    g = uid("co")
    return svg(f'<defs><linearGradient id="{g}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff3c0" stop-opacity="0"/><stop offset="0.5" stop-color="#ffb048" stop-opacity="0.8"/><stop offset="1" stop-color="#ff6020" stop-opacity="1"/></linearGradient></defs>',
               f'<path d="M1500,-40 C1520,200 1560,420 1640,640 L1460,640 C1480,420 1490,200 1500,-40 Z" fill="url(#{g})" filter="url(#blur2)"/>',
               f'<path d="M1500,0 C1510,220 1530,420 1580,620 L1500,620 C1500,420 1500,220 1500,0 Z" fill="#fff0c0" opacity="0.7" filter="url(#blur1)"/>',
               blur_ell(1550, 640, 160, 60, '#ff8a30', 0.6, 3))

@art
def templo_fuego():
    r = random.Random(9)
    flames = "".join(f'<path d="M{x:.0f},{y:.0f} Q{x-30+r.uniform(-20,20):.0f},{y-h*0.5:.0f} {x+r.uniform(-30,30):.0f},{y-h:.0f} Q{x+40:.0f},{y-h*0.5:.0f} {x+50:.0f},{y:.0f} Z" fill="{c}" opacity="0.9"/>'
                     for x, y, h, c in [(r.uniform(950, 1400), r.uniform(430, 470), r.uniform(150, 380), r.choice(['#ff7a20', '#ffb040', '#ff5010', '#ffd070'])) for _ in range(26)])
    smoke = "".join(blur_ell(r.uniform(900, 1600), r.uniform(0, 300), r.uniform(120, 260), r.uniform(80, 160), '#1a1410', 0.8, 3) for _ in range(9))
    return svg(sky('#0c0604', '#3a160a', mid='#200c06'), smoke, glow(1200, 400, 900, 'warm', 0.9), glow(1200, 420, 500, 'red', 0.5),
               pyramid(1200, 1350, 1500, 880, '#1a0d07', 6, 1, lit='#ffb050', hi='#6a2c14'), flames,
               '<rect width="2400" height="1350" fill="url(#paper)"/>')

@art
def codice():
    """Florentine-Codex-style painting on amate: weeping woman with speech scrolls over the lake city."""
    r = random.Random(4)
    paper = '<rect width="2400" height="1350" fill="#d6c19a"/>' + "".join(f'<path d="M{r.uniform(0,2400):.0f},{r.uniform(0,1350):.0f} l{r.uniform(-200,200):.0f},{r.uniform(-30,30):.0f}" stroke="#b49a6c" stroke-width="{r.uniform(1,4):.1f}" opacity="0.5"/>' for _ in range(260))
    frame = '<rect x="320" y="120" width="1760" height="1110" fill="none" stroke="#8a2a1c" stroke-width="10"/><rect x="340" y="140" width="1720" height="1070" fill="none" stroke="#1a120a" stroke-width="4"/>'
    ink = 'stroke="#1a120a" stroke-width="7" stroke-linejoin="round"'
    woman = (f'<g transform="translate(1000,1000)">'
             f'<path d="M-170,0 C-180,-120 -150,-260 -80,-300 L60,-300 C120,-240 150,-120 160,0 Z" fill="#e8e0cc" {ink}/>'          # kneeling skirt+huipil
             f'<path d="M-120,-160 L120,-160 M-140,-80 L140,-80" stroke="#8a2a1c" stroke-width="12"/>'
             + "".join(f'<path d="M{-110+i*40},-130 l14,-18 l14,18" stroke="#2a5a6a" stroke-width="6" fill="none"/>' for i in range(6)) +
             f'<path d="M-60,-300 C-70,-360 -40,-420 10,-420 C60,-420 80,-380 70,-330 C66,-310 50,-300 30,-298 Z" fill="#c08a5a" {ink}/>'   # head
             f'<path d="M-50,-380 C-60,-440 -30,-480 0,-470 C-20,-450 -30,-420 -20,-395 Z M10,-410 C10,-470 50,-490 70,-470 C50,-460 40,-440 40,-410 Z" fill="#1a120a"/>'  # horn hair
             f'<path d="M-62,-340 C-80,-300 -84,-240 -70,-200" stroke="#1a120a" stroke-width="22" fill="none"/>'
             f'<circle cx="40" cy="-360" r="9" fill="#1a120a"/>'
             f'<path d="M48,-345 q6,30 -4,60 q16,-10 18,-30" fill="#2f7fa0" stroke="#1a120a" stroke-width="3"/><path d="M52,-300 q8,30 -2,50" stroke="#2f7fa0" stroke-width="9" fill="none"/>'  # tears
             f'<path d="M60,-210 C120,-230 150,-260 140,-300" stroke="#c08a5a" stroke-width="26" fill="none" stroke-linecap="round"/><path d="M60,-210 C120,-230 150,-260 140,-300" stroke="#1a120a" stroke-width="4" fill="none"/>'
             '</g>')
    scrolls = "".join(f'<path d="M{1090+i*90},{650-i*70} c40,-40 100,-30 100,20 c0,40 -60,40 -60,10 c0,-20 30,-20 30,0" stroke="#1a120a" stroke-width="7" fill="#7fb8c8" opacity="0.95"/>' for i in range(4))
    city = (f'<g transform="translate(1650,980) scale(0.55)">{pyramid(0, 0, 500, 260, "#c9a26a", 5, 2, hi="#8a5a2a")}</g>'
            '<path d="M1450,990 C1550,1010 1750,1010 1900,990" stroke="#2f7fa0" stroke-width="14" fill="none"/>'
            + "".join(f'<path d="M{1420+i*60},1030 q15,-12 30,0 q15,12 30,0" stroke="#2f7fa0" stroke-width="6" fill="none"/>' for i in range(9)))
    glyph = '<g transform="translate(560,330)"><circle r="70" fill="#e0b040" stroke="#1a120a" stroke-width="7"/>' + "".join(f'<path d="M0,0 L{math.cos(a)*120:.0f},{math.sin(a)*120:.0f}" stroke="#c0441c" stroke-width="12"/>' for a in [i * 0.785 for i in range(8)]) + '<circle r="44" fill="#f0d070" stroke="#1a120a" stroke-width="5"/></g>'
    return svg(paper, frame, glyph, city, woman, scrolls, '<rect width="2400" height="1350" fill="url(#paper)"/>')

@art
def sahagun():
    win = ('<path d="M1500,900 L1500,420 A200,200 0 0 1 1900,420 L1900,900 Z" fill="#0e1a28"/>'
           '<path d="M1500,900 L1500,420 A200,200 0 0 1 1900,420 L1900,900 Z" fill="url(#moonglow)" opacity="0.6"/>'
           '<circle cx="1760" cy="430" r="44" fill="#e8ecef" opacity="0.9"/><path d="M1700,420 L1700,900 M1500,640 L1900,640" stroke="#0c0805" stroke-width="16"/>')
    wall = '<rect width="2400" height="1350" fill="#160e09"/>' + "".join(f'<rect x="{x}" y="{y}" width="196" height="96" fill="none" stroke="#0d0805" stroke-width="5"/>' for y in range(0, 1100, 100) for x in range(-100 if (y // 100) % 2 else 0, 2400, 200))
    desk = '<rect x="300" y="980" width="1300" height="40" fill="#2a1a0e"/><rect x="340" y="1020" width="40" height="330" fill="#1a1009"/><rect x="1520" y="1020" width="40" height="330" fill="#1a1009"/>'
    pages = ('<path d="M820,975 L1260,975 L1290,940 L860,935 Z" fill="#d8c8a2"/>'
             + "".join(f'<path d="M{880+i*8},{944+i*3} L{1240+i*4},{946+i*3}" stroke="#5a4a32" stroke-width="3" opacity="0.6"/>' for i in range(8)) +
             '<g transform="translate(400,560) rotate(-6)"><rect width="300" height="220" fill="#d6c19a"/><rect x="10" y="10" width="280" height="200" fill="none" stroke="#8a2a1c" stroke-width="5"/>'
             f'<g transform="translate(150,190) scale(0.28)">{pyramid(0, 0, 500, 260, "#a07a4a", 5, 2, hi="#6a4a2a")}</g></g>')
    friar = ('<g fill="#060403">'
             '<path d="M1000,560 C960,560 930,600 930,650 C930,690 945,720 960,740 C900,780 870,880 860,1000 L880,1350 L1180,1350 L1200,1000 C1200,880 1160,780 1100,740 C1110,700 1100,640 1080,600 C1060,570 1030,560 1000,560 Z"/>'  # hooded robe
             '<path d="M1080,760 C1130,800 1170,860 1200,930 L1180,950 C1150,890 1110,840 1060,810 Z"/>'   # arm to desk
             '<ellipse cx="1205" cy="945" rx="22" ry="14"/></g>'
             '<path d="M1205,940 L1270,860" stroke="#e8e0d0" stroke-width="5"/><path d="M1270,860 q20,-30 10,-50 q-10,25 -16,46" fill="#f2ead8"/>'   # quill
             '<path d="M1080,600 C1100,640 1110,700 1100,740 C1160,780 1200,880 1200,1000" stroke="#ffb860" stroke-width="7" fill="none" opacity="0.7" filter="url(#blur1)"/>'
             '<path d="M1020,600 C1040,620 1046,660 1040,690" stroke="#ffb860" stroke-width="5" fill="none" opacity="0.5"/>')
    return svg(wall, win, glow(1400, 860, 700, 'warm', 0.65), desk, pages, candle(1400, 975, 90, 20), friar,
               '<rect width="2400" height="1350" fill="url(#paper)"/>')

def cihuacoatl_scene(fig=True):
    r = random.Random(17)
    stalls = ""
    for i in range(7):
        x = 150 + i * 340 + r.uniform(-40, 40); y = 1060 + r.uniform(-20, 20)
        stalls += (f'<path d="M{x-150},{y-220} L{x+150},{y-230} L{x+130},{y-190} L{x-130},{y-180} Z" fill="#0c0806"/>'
                   f'<path d="M{x-130},{y-190} L{x-128},{y} M{x+130},{y-190} L{x+128},{y}" stroke="#0c0806" stroke-width="8"/>'
                   + "".join(f'<ellipse cx="{x-90+k*60}" cy="{y-10}" rx="26" ry="18" fill="#140d08"/>' for k in range(4)))
    torches = "".join(glow(x, 820, 160, 'warm', 0.7) + f'<path d="M{x},{830} l0,240" stroke="#0a0604" stroke-width="10"/><path d="M{x},790 q14,24 0,44 q-14,-20 0,-44 Z" fill="#ffc060"/>' for x in (420, 1950))
    cradle = ('<g transform="translate(1265,640) rotate(14)"><path d="M-70,-130 L70,-130 L80,120 L-80,120 Z" fill="#6a4a28" stroke="#2a1a0c" stroke-width="6"/>'
              + "".join(f'<path d="M-76,{-110+k*24} L76,{-110+k*24}" stroke="#3a2812" stroke-width="5"/>' for k in range(10)) + '</g>'
              '<path d="M1200,505 C1220,470 1270,470 1300,520" stroke="#3a2812" stroke-width="8" fill="none"/>')
    return svg(sky('#04070b', '#1a2028', mid='#0b1016'), stars(120, 5, 500), moon(600, 200, 60),
               '<rect x="0" y="1050" width="2400" height="300" fill="#0b0806"/>', stalls, torches, cradle if fig else "",
               place(llorona('stand', seed=21, veil_on=False, horns=True, wind=0.5), 1180, 1200, 900) if fig else
               ('<g transform="translate(1200,1120)"><path d="M-110,-70 L110,-70 L120,40 L-120,40 Z" fill="#5a3a1c" stroke="#2a1a0c" stroke-width="6"/>'
                + "".join(f'<path d="M-116,{-50+k*20} L116,{-50+k*20}" stroke="#3a2812" stroke-width="5"/>' for k in range(5)) +
                '<path d="M-100,-70 C-60,-100 60,-100 100,-70 Z" fill="#d8ccb0"/></g>' + glow(1200, 1080, 300, 'white', 0.25)),
               mist(1150, 90, 0.25, seed=17))

@art
def cihuacoatl():
    return cihuacoatl_scene(True)

@art
def tianguis():
    return cihuacoatl_scene(False)

def cuna_scene(blade_on=True):
    r = random.Random(23)
    weave = "".join(f'<path d="M{700+k*40},{560} L{760+k*36},{1100}" stroke="#4a3018" stroke-width="10"/>' for k in range(24))
    weave += "".join(f'<path d="M{690+j*3},{600+j*55} L{1700-j*3},{600+j*55}" stroke="#7a5428" stroke-width="16" opacity="0.9"/>' for j in range(10))
    basket = ('<path d="M640,560 C620,800 680,1060 760,1120 L1640,1120 C1720,1060 1780,800 1760,560 Z" fill="#5a3a1c"/>' + weave +
              '<path d="M640,560 C900,600 1500,600 1760,560 C1500,520 900,520 640,560 Z" fill="#2a1a0c"/>'
              '<path d="M700,580 C900,640 1500,640 1700,580 C1500,700 900,700 700,580 Z" fill="#120a04"/>')
    cloth = '<path d="M720,600 C860,560 1000,700 1120,640 C1260,580 1400,680 1680,600 C1600,720 900,740 720,600 Z" fill="#d8ccb0" opacity="0.85"/>'
    rr = random.Random(5)
    scars = "".join(f'<polygon points="{x},{y} {x+rr.uniform(20,40):.0f},{y+rr.uniform(-14,14):.0f} {x+rr.uniform(10,30):.0f},{y+rr.uniform(16,30)*(1 if y<0 else -1):.0f}" fill="{rr.choice(["#6e6a62","#8a857a","#5a5650","#a8a296"])}"/>'
                    for x in range(-180, 200, 34) for y in (-24, 0, 22))
    blade = ('<g transform="translate(1200,640) rotate(-14)">'
             '<path d="M-230,0 C-150,-60 100,-70 240,-4 C100,58 -150,56 -230,0 Z" fill="#7a766c"/>' + scars +
             '<path d="M-230,0 C-150,-60 100,-70 240,-4" stroke="#d8d4c8" stroke-width="5" fill="none" opacity="0.8"/>'
             '<path d="M-230,0 C-150,56 100,58 240,-4" stroke="#2a2824" stroke-width="5" fill="none"/>'
             '<path d="M-230,0 L240,-4" stroke="#4a4740" stroke-width="3" opacity="0.6"/></g>')
    return svg('<rect width="2400" height="1350" fill="#0a0604"/>', glow(1200, 600, 1000, 'warm', 0.55), glow(1900, 300, 600, 'red', 0.25),
               basket, cloth if blade_on else '<path d="M700,600 C860,520 1000,640 1120,560 C1260,500 1400,620 1700,580 C1680,700 900,760 700,600 Z" fill="#d8ccb0"/><path d="M800,600 C1000,560 1300,600 1600,590" stroke="#9a8e74" stroke-width="5" fill="none"/>',
               blade if blade_on else "", '<rect x="0" y="1120" width="2400" height="230" fill="#060302"/>',
               '<rect width="2400" height="1350" fill="url(#paper)"/>')

@art
def malinche():
    sea = water(820, 1350, '#6a6a68', '#2a2a2a')
    def ship(x, y, s):
        return (f'<g transform="translate({x},{y}) scale({s})" fill="#1c1610"><path d="M-260,0 L260,0 L210,90 L-200,90 Z"/><path d="M-260,0 L-300,-60 L-200,-10 Z"/>'
                '<rect x="-6" y="-420" width="12" height="420"/><rect x="-160" y="-320" width="10" height="320"/><rect x="140" y="-260" width="10" height="260"/>'
                '<path d="M-110,-400 Q0,-360 110,-400 L100,-200 Q0,-170 -100,-200 Z" fill="#cfc4ac"/><path d="M-230,-300 Q-155,-270 -80,-300 L-90,-150 Q-155,-130 -220,-150 Z" fill="#cfc4ac"/>'
                '<path d="M100,-240 Q145,-215 190,-240 L184,-120 Q145,-104 106,-120 Z" fill="#cfc4ac"/></g>')
    ships = ship(1500, 840, 0.6) + ship(2050, 860, 0.45) + ship(1150, 830, 0.3)
    cortes = ('<g fill="#120c08">'
              '<path d="M1880,1350 L1890,1000 C1890,960 1910,940 1940,930 L2060,930 C2090,940 2110,960 2110,1000 L2120,1350 Z"/>'
              '<ellipse cx="2000" cy="880" rx="44" ry="52"/><path d="M1930,860 Q2000,780 2070,860 Z"/><path d="M1900,862 L2100,862 L2080,846 L1920,846 Z"/>'
              '<path d="M1990,790 Q2000,760 2010,790 Z"/><path d="M1960,900 Q2000,960 2040,900 L2030,940 Q2000,960 1970,940 Z"/></g>')
    huipil = "".join(f'<path d="M{-200+i*36},{450} l18,-22 l18,22" stroke="#8a2a1c" stroke-width="8" fill="none"/>' for i in range(12)) + '<path d="M-230,480 C-80,500 120,500 280,480" stroke="#2a5a6a" stroke-width="10" fill="none"/>'
    mal = (f'<g transform="translate(720,560)">'
           '<path d="M-330,790 C-320,560 -230,360 -60,330 L120,330 C260,370 330,560 340,790 Z" fill="#e2d6bc"/>' + huipil +
           '<path d="M-330,790 C-320,560 -230,360 -60,330" stroke="#1a120a" stroke-width="4" fill="none" opacity="0.5"/>'
           '<path d="M-40,180 L-50,340 L110,340 L90,180 Z" fill="#9a6a44"/>'
           '<path d="M-110,-60 C-120,-200 -20,-260 60,-250 C150,-240 190,-170 186,-90 C184,-60 196,-30 214,0 C220,14 206,22 192,22 C196,40 192,56 182,62 C188,80 180,100 160,104 C160,140 140,170 100,176 C40,184 -30,170 -80,120 C-120,80 -110,0 -110,-60 Z" fill="#b07a4e"/>'  # face profile facing right
           '<path d="M-110,-60 C-130,-220 0,-290 80,-260 C150,-240 186,-190 190,-130 C150,-180 90,-200 40,-190 C0,-180 -40,-120 -60,-40 C-70,40 -80,120 -60,180 C-120,140 -116,40 -110,-60 Z" fill="#0a0706"/>'  # hair
           f'{braid(-70, 140, -150, 600, 40)}'
           '<path d="M80,-110 Q120,-122 150,-104" stroke="#120a06" stroke-width="7" fill="none"/><path d="M100,-80 Q125,-92 146,-80 Q125,-68 100,-80 Z" fill="#1a0e08"/>'
           '<path d="M150,50 Q170,58 186,54" stroke="#5a2a1a" stroke-width="6" fill="none"/>'
           '<circle cx="30" cy="0" r="16" fill="none" stroke="#d8a840" stroke-width="5"/>'
           '<path d="M186,-90 C184,-60 196,-30 214,0" stroke="#ffe0a0" stroke-width="10" fill="none" opacity="0.5" filter="url(#blur1)"/>'
           '</g>')
    return svg(sky('#9a9488', '#d8d0bc', mid='#bcb4a2'), '<circle cx="1700" cy="420" r="70" fill="#f4eedc"/>', glow(1700, 420, 500, 'white', 0.6),
               sea, ships, '<path d="M0,1100 C800,1060 1600,1120 2400,1080 L2400,1350 L0,1350 Z" fill="#8a7a5e"/>', cortes, mal,
               '<rect width="2400" height="1350" fill="url(#paper)"/>')


# ============================================================================ XOCHIMILCO / VARIANTS / MODERN
def trajinera_g(x, y, s=1.0, name="Rosita", lit=True, dark=False):
    """Side view of a trajinera with painted arch and name; (x,y)= waterline centre."""
    hull = "#0c2a2a" if not dark else "#06100f"
    flowers = "".join(f'<circle cx="{-330+i*44}" cy="{-228+ (8 if i%2 else 0)}" r="13" fill="{["#d8344a","#f0b030","#3a9a5a","#e86a20","#c02870"][i%5]}"/>' for i in range(16))
    g = (f'<path d="M-420,0 L420,0 L460,-60 L-460,-60 Z" fill="{hull}"/><path d="M-460,-60 L460,-60 L455,-74 L-455,-74 Z" fill="#c9a040"/>'
         f'<rect x="-360" y="-200" width="720" height="16" fill="#3a2a18"/>'                       # roof beam
         f'<path d="M-380,-200 L380,-200 L360,-170 L-360,-170 Z" fill="#5a1e18"/>'
         + "".join(f'<rect x="{-340+i*170}" y="-170" width="14" height="96" fill="#2a1c10"/>' for i in range(5)) +
         f'<path d="M-380,-196 Q0,-300 380,-196 L380,-250 Q0,-350 -380,-250 Z" fill="#e6c25a"/>'     # arch board
         + flowers +
         f'<text x="0" y="-262" text-anchor="middle" font-family="Rye" font-size="56" fill="#b0202e">{name}</text>'
         + ''.join(f'<rect x="{-300+i*130}" y="-120" width="90" height="46" fill="#2a1c10"/>' for i in range(5)))
    out = f'<g transform="translate({x},{y}) scale({s})">{g}</g>'
    if lit:
        out += glow(x - 300 * s, y - 120 * s, 120 * s, 'warm', 0.7) + f'<circle cx="{x-300*s}" cy="{y-130*s}" r="{10*s}" fill="#ffd27a"/>'
    out += f'<g transform="translate({x},{y}) scale({s})"><path d="M-420,4 Q0,40 420,4" stroke="#9fb6c9" stroke-width="3" fill="none" opacity="0.4"/></g>'
    return out

def ahuehuete_heno(x, y, size, seed, color="#05090b"):
    return tree(x, y, size, seed, color, 'ahuehuete') + heno(x, y - size * 0.55, size * 0.7, size * 0.35, seed, '#0e1a1e', 26)

@art
def xochimilco():
    r = random.Random(41)
    canal = '<polygon points="0,1350 2400,1350 1500,780 1100,780" fill="#0e1e26"/>' + reflection(1300, 785, 1350, width=90, seed=4)
    banks = ('<polygon points="0,700 1100,780 0,1350" fill="#040808"/><polygon points="2400,700 1500,780 2400,1350" fill="#040808"/>')
    trees = (ahuehuete_heno(300, 900, 900, 3) + ahuehuete_heno(820, 800, 520, 5) + ahuehuete_heno(1980, 880, 820, 7) + ahuehuete_heno(1640, 790, 420, 9))
    boats = trajinera_g(560, 1180, 0.75, "Lupita") + trajinera_g(1850, 1220, 0.7, "Rosita", lit=False)
    return svg(sky('#040a10', '#1a3038', mid='#0b1a20'), stars(120, 41, 500), moon(1320, 230, 70),
               ridge(760, 60, '#08131a', 4), canal, banks, trees, boats, mist(800, 90, 0.35, seed=41), mist(1000, 120, 0.2, seed=42))

@art
def trajinera():
    return svg(trajinera_g(1200, 1000, 1.0, "Llorona", lit=False, dark=True), ripples(1200, 1010, 4, 520, 30, op=0.35))

@art
def espectaculo():
    r = random.Random(7)
    water_ = water(760, 1350, '#0f1d26', '#03070a')
    torches = "".join(f'<path d="M{x},{y} l0,{-90*s:.0f}" stroke="#0a0604" stroke-width="{8*s:.0f}"/>' + glow(x, y - 100 * s, 120 * s, 'warm', 0.85) +
                      f'<path d="M{x},{y-128*s:.0f} q{10*s:.0f},{20*s:.0f} 0,{36*s:.0f} q{-10*s:.0f},{-16*s:.0f} 0,{-36*s:.0f} Z" fill="#ffc060"/>' + reflection(x, y, y + 200 * s, '#ffb050', 30 * s, int(x))
                      for x, y, s in [(700, 900, 0.8), (1000, 880, 0.7), (1450, 880, 0.7), (1750, 900, 0.8), (500, 960, 1.0), (1950, 960, 1.0)])
    stage = ('<polygon points="900,860 1500,860 1560,900 840,900" fill="#0a0806"/>'
             '<polygon points="1080,0 1320,0 1420,860 980,860" fill="#dfeeff" opacity="0.12" filter="url(#blur2)"/>')
    dancers = "".join(f'<g fill="#0a0604">{sil_person(x, 860, 150, "man", "#0a0604")}<path d="M{x-30},{860-150} q30,-70 60,0" stroke="#0a0604" stroke-width="8" fill="none"/></g>' for x in (930, 1000, 1400, 1470))
    audience = ""
    for i in range(30):
        x = r.uniform(-50, 2450); y = r.uniform(1180, 1350); s = r.uniform(0.9, 1.4)
        audience += f'<ellipse cx="{x:.0f}" cy="{y-70*s:.0f}" rx="{26*s:.0f}" ry="{32*s:.0f}" fill="#020303"/><path d="M{x-60*s:.0f},{y+60} Q{x:.0f},{y-60*s:.0f} {x+60*s:.0f},{y+60}" fill="#020303"/>'
    candles = "".join(glow(x, y, 26, 'warm', 0.9) + f'<circle cx="{x}" cy="{y}" r="4" fill="#ffe0a0"/>' for x, y in [(r.uniform(0, 2400), r.uniform(1150, 1330)) for _ in range(22)])
    boats_fg = '<path d="M-100,1210 Q1200,1150 2500,1210 L2500,1350 L-100,1350 Z" fill="#0b0605"/>' + "".join(f'<rect x="{x}" y="1150" width="16" height="70" fill="#0b0605"/>' for x in range(100, 2400, 300))
    return svg(sky('#03060a', '#101c24'), stars(160, 70, 600), ridge(760, 40, '#050a0e', 3), water_, mist(860, 70, 0.4, seed=71),
               stage, torches, dancers, place(llorona('stand', seed=31, wind=1.5), 1200, 860, 330),
               boats_fg, audience, candles)

@art
def abuela():
    fire = ('<path d="M560,1010 L940,1010 L900,1100 L600,1100 Z" fill="#1a0e08"/>' + glow(750, 940, 600, 'warm', 0.9) +
            "".join(f'<path d="M{x},1000 Q{x-20},{940} {x+5},{880-(i%3)*30} Q{x+30},{940} {x+40},1000 Z" fill="{c}"/>' for i, (x, c) in enumerate([(640, '#ff7a20'), (700, '#ffb040'), (760, '#ff5a10'), (810, '#ffd070')])) +
            '<ellipse cx="750" cy="880" rx="190" ry="20" fill="#2a1a10"/><rect x="560" y="860" width="380" height="14" fill="#3a2414" opacity="0"/>')
    pots = "".join(f'<g transform="translate({x},420)"><path d="M0,0 l0,60" stroke="#2a1a10" stroke-width="4"/><path d="M-50,70 Q-60,150 0,160 Q60,150 50,70 Z" fill="#3a2214"/><ellipse cx="0" cy="70" rx="40" ry="10" fill="#1a0e08"/></g>' for x in (1350, 1500, 1650))
    abuela_ = ('<g fill="#080403">'
               '<path d="M1080,640 C1040,640 1010,680 1012,730 C960,770 930,860 920,1000 L900,1200 L1260,1200 L1240,1000 C1230,860 1190,770 1150,740 C1160,690 1130,640 1080,640 Z"/>'
               '<path d="M1012,730 C990,700 1000,650 1040,630 C1090,610 1140,630 1152,690 Z"/>'
               '<path d="M1020,820 C980,860 960,900 950,940 L980,950 C990,910 1010,880 1040,850 Z"/></g>'
               '<path d="M1012,730 C990,700 1000,650 1040,630 C1060,624 1080,624 1094,628" stroke="#ffb060" stroke-width="7" fill="none" opacity="0.8"/>'
               '<path d="M1012,740 C960,780 930,860 920,1000" stroke="#ffb060" stroke-width="6" fill="none" opacity="0.6" filter="url(#blur1)"/>')
    kids = (sil_person(380, 1200, 280, 'child', '#080403', '#ffb060', 1) + sil_person(480, 1200, 250, 'girl', '#080403', '#ffb060', 1) +
            sil_person(1420, 1200, 300, 'girl', '#080403', '#ffb060', -1))
    return svg('<rect width="2400" height="1350" fill="#140b06"/>', '<rect x="0" y="1150" width="2400" height="200" fill="#0b0604"/>',
               glow(750, 900, 1400, 'warm', 0.55), pots, fire, abuela_, kids, '<rect width="2400" height="1350" fill="url(#paper)"/>')

@art
def arroyo():
    r = random.Random(52)
    mesas = ('<path d="M0,760 L200,760 L260,560 L700,560 L760,760 L1500,760 L1560,610 L1900,610 L1960,760 L2400,760 L2400,900 L0,900 Z" fill="#2a1a20"/>'
             '<path d="M260,560 L700,560 L704,580 L256,580 Z M1560,610 L1900,610 L1904,626 L1556,626 Z" fill="#5a3a3a" opacity="0.6"/>')
    land = '<rect x="0" y="880" width="2400" height="470" fill="#140c0c"/>'
    ditch = '<path d="M0,1180 C500,1120 900,1240 1400,1180 C1800,1130 2100,1200 2400,1160 L2400,1230 C2100,1270 1800,1200 1400,1250 C900,1310 500,1190 0,1250 Z" fill="#2b3a48"/>' + "".join(f'<path d="M{x},{1200+r.uniform(-20,20):.0f} l80,0" stroke="#8aa0b4" stroke-width="3" opacity="0.4"/>' for x in range(50, 2400, 180))
    cotton = tree(1900, 1150, 600, 61, '#0a0606', 'bare', 0.05) + tree(2200, 1160, 420, 62, '#0a0606', 'bare', -0.1)
    saguaro = "".join(f'<g fill="#0c0808"><rect x="{x-18}" y="{y-260}" width="36" height="260" rx="18"/><path d="M{x-18},{y-140} l-50,0 q-16,0 -16,-16 l0,-70 q0,-14 14,-14 q14,0 14,14 l0,52 l38,0 Z"/><path d="M{x+18},{y-180} l40,0 l0,-50 q0,-14 14,-14 q14,0 14,14 l0,66 q0,16 -16,16 l-52,0 Z"/></g>' for x, y in [(300, 1000), (760, 960)])
    house = ('<rect x="1100" y="820" width="420" height="200" fill="#1a0f0c"/><rect x="1090" y="806" width="440" height="18" fill="#120a08"/>'
             + "".join(f'<rect x="{1100+k*50}" y="830" width="12" height="10" fill="#0a0604"/>' for k in range(9)) +
             window(1180, 880, 70, 80, True, False) + '<rect x="1360" y="890" width="70" height="130" fill="#ffcf7a"/>' + glow(1395, 950, 200, 'warm', 0.7))
    kids = sil_person(700, 1160, 150, 'child', '#050303') + sil_person(800, 1160, 130, 'girl', '#050303') + sil_person(1395, 1020, 120, 'woman', '#120806')
    return svg(sky('#120c1c', '#6a3a40', mid='#2a1a30'), stars(90, 52, 420), moon(1700, 240, 64), glow(1200, 800, 1400, 'red', 0.2),
               mesas, land, saguaro, house, ditch, cotton, kids, mist(1200, 50, 0.18, col='#b8a8b8', seed=52))

@art
def carretera():
    road = '<polygon points="900,1350 2000,1350 1290,760 1230,760" fill="#16191c"/>' + "".join(f'<polygon points="{1260+(i/10)**2*10:.0f},{760+(i/10)**2*590:.0f} {1262+(i/10)**2*14:.0f},{760+(i/10)**2*590:.0f} {1264+(i/10)**2*20:.0f},{780+(i/10)**2*640:.0f} {1260+(i/10)**2*12:.0f},{780+(i/10)**2*640:.0f}" fill="#c8b060" opacity="0.7"/>' for i in range(1, 10))
    canal = '<polygon points="0,1350 700,1350 1200,760 1150,760" fill="#1d3040"/>' + reflection(800, 900, 1350, width=60, seed=8)
    poles = "".join(f'<rect x="{1330+(1-k)*900:.0f}" y="{760-(1-k)*700:.0f}" width="{4+(1-k)*14:.0f}" height="{(1-k)*800+40:.0f}" fill="#05070a"/><rect x="{1310+(1-k)*900:.0f}" y="{770-(1-k)*700:.0f}" width="{40+(1-k)*80:.0f}" height="{2+(1-k)*8:.0f}" fill="#05070a"/>' for k in (0.2, 0.55, 0.8, 0.92))
    wires = '<path d="M1330,820 Q1700,640 2420,180" stroke="#05070a" stroke-width="3" fill="none"/>'
    lights = glow(1262, 770, 90, 'white', 0.9) + '<circle cx="1252" cy="772" r="5" fill="#fff"/><circle cx="1272" cy="772" r="5" fill="#fff"/>'
    return svg(sky('#03060a', '#18222e'), stars(140, 81, 600), ridge(760, 60, '#070c11', 6), canal, road, poles, wires, lights,
               '<polygon points="0,1350 0,900 1150,760 700,1350" fill="#040608" opacity="0.0"/>',
               place(llorona('reach', seed=41, wind=1.2), 1090, 900, 230), mist(860, 60, 0.3, seed=81), reeds(0, 600, 1350, 8, '#020305', 60, 120))

@art
def cuarto():
    win = ('<rect x="1300" y="180" width="700" height="760" fill="#13283a"/><rect x="1300" y="180" width="700" height="760" fill="url(#moonglow)"/>'
           '<path d="M1650,180 L1650,940 M1300,560 L2000,560" stroke="#0a1018" stroke-width="18"/>'
           '<rect x="1270" y="150" width="760" height="40" fill="#0d151d"/><rect x="1270" y="930" width="760" height="40" fill="#0d151d"/>')
    curtain = "".join(f'<path d="M{x},150 C{x+20},400 {x-20},700 {x+10},1000" stroke="#c8d8e8" stroke-width="{w}" fill="none" opacity="{o}"/>' for x, w, o in [(1320, 60, 0.18), (1400, 40, 0.14), (1480, 70, 0.16), (1560, 50, 0.12), (1700, 60, 0.15), (1790, 44, 0.13), (1880, 70, 0.17), (1960, 50, 0.15)])
    curtain = f'<g filter="url(#blur1)">{curtain}</g>'
    bed = ('<path d="M0,1080 C400,1040 900,1060 1200,1100 L1200,1350 L0,1350 Z" fill="#1a2430"/>'
           '<path d="M0,1080 C400,1040 900,1060 1200,1100" stroke="#5a7088" stroke-width="5" fill="none" opacity="0.6"/>'
           '<path d="M100,1150 C300,1120 500,1170 700,1140 M300,1250 C500,1200 800,1260 1000,1220" stroke="#0e141c" stroke-width="10" fill="none"/>')
    stand = ('<rect x="2050" y="930" width="300" height="420" fill="#0c1016"/>'
             '<rect x="2100" y="880" width="160" height="56" rx="8" fill="#05080b"/><text x="2180" y="922" text-anchor="middle" font-family="Oswald" font-size="40" fill="#ff2a1a">00:00</text>'
             + glow(2180, 905, 80, 'red', 0.5) + '<rect x="2280" y="840" width="40" height="90" rx="6" fill="#9fb6c9" opacity="0.3"/>')
    return svg('<rect width="2400" height="1350" fill="#070b10"/>', glow(1650, 560, 900, 'moon', 0.9), win, curtain, bed, stand,
               '<polygon points="1300,940 2000,940 2300,1350 900,1350" fill="#9fc0dd" opacity="0.06"/>')

@art
def cortina_sombra():
    """Shadow of a veiled woman behind the curtain (aligned with cuarto window)."""
    return svg(f'<g opacity="0.85" filter="url(#blur2)"><g fill="#03060a">'
               '<ellipse cx="1650" cy="390" rx="62" ry="78"/>'
               '<path d="M1580,350 C1520,450 1480,700 1440,940 L1860,940 C1820,700 1780,450 1720,350 Q1650,300 1580,350 Z"/>'
               '<path d="M1600,470 C1570,560 1560,640 1570,700 L1590,700 C1590,640 1600,560 1620,480 Z"/></g></g>'
               + drips(random.Random(2), [(1500 + i * 40, 945) for i in range(9)], '#9fb6c9', 0.6, 1.5))

@art
def perro():
    wall = '<path d="M0,960 L2400,940 L2400,1040 L0,1060 Z" fill="#1a1410"/><rect x="0" y="1040" width="2400" height="310" fill="#090706"/>'
    nopal = "".join(f'<ellipse cx="{x+dx}" cy="{y+dy}" rx="{rx}" ry="{ry}" fill="#060908" transform="rotate({a} {x+dx} {y+dy})"/>' for x, y in [(300, 940), (2050, 930)] for dx, dy, rx, ry, a in [(0, 0, 50, 80, 0), (-60, -110, 40, 64, -25), (55, -120, 38, 60, 20), (-10, -220, 32, 52, 5)])
    dog = ('<g fill="#030303" transform="translate(1480,1045) scale(1.7)">'
           '<path d="M-100,0 C-105,-50 -95,-110 -50,-135 C-10,-155 20,-185 40,-225 L46,-262 L30,-292 L58,-275 C80,-300 100,-320 128,-352 '
           'L140,-348 C128,-322 110,-300 98,-286 L110,-282 C96,-270 86,-258 82,-240 C80,-210 76,-180 70,-150 C66,-110 64,-60 70,-20 '
           'L80,0 L50,0 L46,-20 C40,-60 30,-80 20,-90 C10,-60 0,-30 -10,0 Z"/>'
           '<path d="M-100,-10 C-140,-20 -170,-10 -190,10 L-186,18 C-160,4 -130,0 -100,4 Z"/></g>'
           '<path d="M1480,1045" />')
    return svg(sky('#03070c', '#1c2c3a'), stars(220, 91, 700), moon(1700, 300, 120, halo=4), ridge(900, 80, '#070c12', 5),
               '<rect x="400" y="700" width="380" height="250" fill="#0c0a08"/><rect x="390" y="690" width="400" height="16" fill="#0a0806"/>',
               window(500, 760, 60, 80, True, False), wall, nopal, dog, '<path d="M1820,580 q30,-20 60,-10 M1830,620 q40,-26 80,-14" stroke="#9fb6c9" stroke-width="4" fill="none" opacity="0.5"/>', mist(940, 60, 0.2, seed=91))

@art
def charro():
    road = '<polygon points="700,1350 1700,1350 1260,860 1140,860" fill="#14110f"/>'
    cact = "".join(f'<g fill="#050404"><rect x="{x-14}" y="{y-200}" width="28" height="200" rx="14"/><path d="M{x-14},{y-110} l-40,0 q-12,0 -12,-12 l0,-50 q0,-12 12,-12 q12,0 12,12 l0,38 l28,0 Z"/></g>' for x, y in [(380, 1000), (2050, 990)])
    return svg(sky('#05040a', '#2a1418', mid='#140a10'), stars(160, 99, 600), moon(1200, 420, 220, color='#f0e0d0', halo=3),
               ridge(880, 90, '#0a0608', 9), '<rect x="0" y="860" width="2400" height="490" fill="#0a0707"/>', road, cact,
               horse(1220, 1120, 360, '#020101', '#ff6a4a', 1, 'charro', '#ff2a1a'), mist(1100, 70, 0.2, col='#c8a8a8', seed=99))

@art
def camino():
    r = random.Random(13)
    path = '<path d="M900,1350 C1000,1200 1150,1050 1230,900 L1300,900 C1300,1050 1350,1200 1500,1350 Z" fill="#1a1c1e"/>'
    prints = "".join(f'<ellipse cx="{1200+ (1-t)*70 + (14 if i%2 else -14)*(1-t):.0f}" cy="{900+(1-t)*420:.0f}" rx="{14*(1-t)+3:.0f}" ry="{6*(1-t)+2:.0f}" fill="#4a6478" opacity="0.6"/>' for i, t in enumerate([k / 12 for k in range(12)]))
    grass = reeds(0, 950, 1300, 21, '#020305', 160, 260) + reeds(1550, 2400, 1300, 22, '#020305', 160, 260)
    river = water(860, 900, '#2a4458', '#122230') + reflection(1700, 862, 900, width=140)
    pole = '<rect x="560" y="300" width="18" height="900" fill="#05070a"/><rect x="520" y="300" width="120" height="14" fill="#05070a"/>' + glow(630, 330, 220, 'warm', 0.6) + '<circle cx="630" cy="322" r="10" fill="#ffd27a"/>'
    return svg(sky('#03070c', '#1a2a38'), stars(140, 13, 500), moon(1700, 260, 60), ridge(840, 70, '#08111a', 2), river,
               '<rect x="0" y="895" width="2400" height="455" fill="#0b0f12"/>', mist(900, 50, 0.4, seed=13), path, prints, pole, grass)

@art
def espalda():
    """'No voltees': you in the foreground, wide-eyed; behind you, close, she leans toward your shoulder."""
    bg = sky('#02050a', '#0e1822') + mist(900, 200, 0.12, seed=3)
    her = blur_ell(1560, 700, 600, 700, "#bcd8f0", 0.12, 4) + f'<g opacity="0.92">{place(llorona("stand", seed=51, wind=0.6, glow=False, mist=False, nofx_low=True), 1560, 2300, 2300)}</g>'
    you = ('<g fill="#020304">'
           '<path d="M300,1350 C320,1150 420,1040 560,1000 C600,990 640,960 650,930 L800,930 C810,960 850,990 890,1000 C1030,1040 1130,1150 1150,1350 Z"/>'
           '<path d="M600,700 C600,560 660,470 725,470 C790,470 850,560 850,700 C850,800 800,900 725,930 C650,900 600,800 600,700 Z"/></g>'
           '<path d="M850,700 C850,800 800,900 725,930" stroke="#9fc4e6" stroke-width="7" fill="none" opacity="0.7"/>'
           '<path d="M890,1000 C1030,1040 1130,1150 1150,1350" stroke="#9fc4e6" stroke-width="7" fill="none" opacity="0.5"/>'
           '<ellipse cx="690" cy="690" rx="16" ry="10" fill="#dfe9f2"/><ellipse cx="770" cy="690" rx="16" ry="10" fill="#dfe9f2"/>'
           '<circle cx="694" cy="690" r="6" fill="#05080b"/><circle cx="774" cy="690" r="6" fill="#05080b"/>'
           '<path d="M600,640 C590,560 650,450 725,452 C800,450 860,560 852,640 C840,580 790,520 725,520 C660,520 610,580 600,640 Z" fill="#05070a"/>')
    return svg(bg, her, you)

@art
def ll_hands():
    """Two pale wet hands reaching towards the camera from the dark."""
    def big_hand(x, y, ang, s, flip=1):
        fingers = ""
        for dx, L, w in [(-44, 230, 34), (-14, 270, 36), (18, 262, 35), (48, 210, 31)]:
            fingers += f'<path d="M{dx-w/2},-40 C{dx-w/2},{-40-L*0.5} {dx*1.2-w/2},{-40-L+20} {dx*1.2},{-40-L} C{dx*1.2+w/2},{-40-L+20} {dx+w/2},{-40-L*0.5} {dx+w/2},-40 Z"/>'
        thumb = '<path d="M-66,0 C-100,-30 -126,-90 -134,-150 C-136,-172 -110,-178 -104,-158 C-96,-112 -82,-74 -56,-50 Z"/>'
        palm = '<path d="M-66,-60 L70,-60 C80,0 76,60 60,110 L-60,110 C-74,60 -78,0 -66,-60 Z"/>'
        sleeve = '<path d="M-90,100 C-100,300 -120,500 -160,700 L190,700 C150,500 120,300 90,100 Z" fill="url(#hsl)"/>'
        lines = ''.join(f'<path d="M{dx-10},{-40-L*k:.0f} q10,6 20,0" stroke="#7a8a98" stroke-width="3" fill="none"/>' for dx, L in [(-44, 230), (-14, 270), (18, 262), (48, 210)] for k in (0.35, 0.65))
        return (f'<g transform="translate({x},{y}) rotate({ang}) scale({s*flip},{s})">{sleeve}'
                f'<g fill="url(#hsk)" stroke="#6a7a88" stroke-width="3">{palm}{thumb}{fingers}</g>{lines}'
                '</g>')
    defs = ('<defs><linearGradient id="hsk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f2f6f8"/><stop offset="1" stop-color="#9aa8b4"/></linearGradient>'
            '<linearGradient id="hsl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#dfe8ef"/><stop offset="1" stop-color="#5a6a78" stop-opacity="0.2"/></linearGradient></defs>')
    r = random.Random(9)
    return svg(defs, blur_ell(1200, 900, 700, 400, '#bcd8f0', 0.12, 4), big_hand(820, 900, -18, 1.25), big_hand(1580, 900, 18, 1.25, -1),
               drips(r, [(r.uniform(650, 1750), r.uniform(950, 1250)) for _ in range(16)], size=2.5))


@art
def cuna():
    return cuna_scene(True)

@art
def cuna_tapada():
    return cuna_scene(False)

@art
def maria_triste():
    wall = '<rect width="2400" height="1350" fill="#1c2630"/>' + "".join(f'<rect x="{x}" y="{y}" width="230" height="100" fill="#16202a" opacity="0.6" stroke="#10181f" stroke-width="3"/>' for y in range(0, 1350, 104) for x in range(-115 if (y // 104) % 2 else 0, 2400, 234))
    return svg(wall, glow(1700, 300, 900, 'moon', 0.8), maria_face(1250, 560, 1.15, sad=True), '<rect width="2400" height="1350" fill="url(#paper)"/>')

# ---- ghost placements for specific backgrounds
@art
def ll_far_calle():
    return svg(place(llorona('stand', seed=61), 1330, 935, 300))

@art
def ll_callejon():
    return svg(place(llorona('stand', seed=62, wind=1.6), 900, 1110, 600))

@art
def ll_far_xochi():
    return svg(place(llorona('stand', seed=63, wind=1.2), 1300, 905, 230))

@art
def ll_far_alba():
    return svg(place(llorona('stand', seed=64), 1480, 835, 250))

@art
def ll_far_puente():
    return svg(place(llorona("mourn", seed=65), 1480, 700, 210))

@art
def presagio_fig():
    return svg(blur_ell(1200, 520, 260, 360, '#cfe4f7', 0.18, 4),
               place(llorona('reach', seed=66, veil_on=False, horns=True, wind=2.2, mist=True, glow=False), 1150, 980, 640))

# ---- new backgrounds
@art
def callejon():
    r = random.Random(71)
    walls = ('<polygon points="0,0 820,260 820,1150 0,1350" fill="#10161d"/><polygon points="2400,0 1580,260 1580,1150 2400,1350" fill="#0d1218"/>'
             + "".join(f'<path d="M0,{y} L820,{260+(y)*0.66:.0f}" stroke="#0a0e13" stroke-width="3"/>' for y in range(80, 1350, 90))
             + "".join(f'<path d="M2400,{y} L1580,{260+(y)*0.66:.0f}" stroke="#090c10" stroke-width="3"/>' for y in range(80, 1350, 90)))
    sky_ = '<rect x="820" y="0" width="760" height="1150" fill="#16283a"/>' + moon(1350, 160, 50) + stars(30, 7, 260)
    arch = ('<path d="M820,520 L1580,520 L1580,620 C1500,560 900,560 820,620 Z" fill="#0b1016"/>'
            '<path d="M760,460 L1640,460 L1640,525 L760,525 Z" fill="#0d131a"/>')
    far = '<rect x="820" y="620" width="760" height="530" fill="#0c1218"/>' + "".join(window(880 + i * 180, 760, 50, 90, i == 2, True) for i in range(4))
    ground_ = '<polygon points="0,1350 820,1150 1580,1150 2400,1350" fill="#151c23"/>' + "".join(f'<path d="M{820-(i/8)**1.5*820:.0f},{1150+(i/8)**1.5*200:.0f} L{1580+(i/8)**1.5*820:.0f},{1150+(i/8)**1.5*200:.0f}" stroke="#222c36" stroke-width="2"/>' for i in range(1, 9))
    niche = ('<path d="M300,560 L300,420 A60,60 0 0 1 420,420 L420,560 Z" fill="#2a1a10"/>' + glow(360, 520, 160, 'warm', 0.9) +
             '<path d="M342,540 Q360,450 378,540 Z" fill="#c9a0a8"/><circle cx="360" cy="460" r="12" fill="#e8d0b0"/>' + candle(360, 556, 26, 10))
    lamp_ = lamp(2050, 1250, 640)
    return svg(sky_, far, arch, walls, ground_, niche, lamp_, mist(1150, 60, 0.3, seed=71, x0=700, x1=1700))

@art
def ondas_lago():
    r = random.Random(9)
    return svg(water(0, 1350, '#1a2e3e', '#03070b'), reflection(1200, 0, 1350, width=300, seed=8),
               ripples(1200, 700, 7, 220, 50, op=0.35, step=1.8), mist(500, 200, 0.18, seed=9),
               reeds(0, 500, 1350, 4, '#020407', 40, 420), reeds(1900, 2400, 1350, 5, '#020407', 40, 420))

@art
def rio_orilla():
    r = random.Random(33)
    stones = "".join(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rx:.0f}" ry="{rx*0.45:.0f}" fill="#0a0e12"/><path d="M{x-rx*0.7:.0f},{y-rx*0.3:.0f} Q{x:.0f},{y-rx*0.55:.0f} {x+rx*0.6:.0f},{y-rx*0.32:.0f}" stroke="#4a6074" stroke-width="3" fill="none" opacity="0.6"/>'
                     for x, y, rx in [(r.uniform(900, 2400), r.uniform(1230, 1330), r.uniform(40, 120)) for _ in range(16)])
    roots = "".join(f'<path d="M{100+i*40},{700} C{200+i*60},{900} {300+i*80},{1100} {500+i*120},{1300}" stroke="#04070a" stroke-width="{40-i*5}" fill="none"/>' for i in range(6))
    return svg(sky('#03070d', '#1c3040', mid='#0b1724'), stars(160, 33, 600), moon(1500, 220, 80),
               ridge(760, 70, '#0a141e', 33), water(760, 1250, '#22384a', '#060b11'), reflection(1500, 765, 1250, width=180),
               '<path d="M0,1250 C600,1240 1100,1210 1700,1230 C2000,1220 2200,1210 2400,1200 L2400,1350 L0,1350 Z" fill="#0b1015"/>', stones,
               tree(220, 760, 900, 33, '#03060a', 'ahuehuete', 0.1), heno(260, 300, 500, 300, 3, '#0e1a1e', 30),
               reeds(1900, 2400, 1250, 6, '#020407', 60, 220), mist(800, 70, 0.35, seed=33))

@art
def puerta():
    wall = '<rect x="0" y="0" width="2400" height="1350" fill="#140e0a"/>' + "".join(f'<path d="M0,{y} L1500,{y}" stroke="#0e0906" stroke-width="3"/>' for y in range(60, 1150, 72))
    out_ = ('<rect x="1500" y="0" width="900" height="1350" fill="#0a1520"/>' + moon(2050, 240, 60) + stars(50, 4, 500) +
            '<polygon points="1500,1150 2400,1100 2400,1350 1500,1350" fill="#0c0f12"/><path d="M1700,1350 C1850,1200 2000,1150 2250,1100" stroke="#1d242b" stroke-width="80" fill="none"/>'
            + tree(2250, 1110, 420, 4, '#03060a', 'bare', -0.1))
    door = '<rect x="1440" y="300" width="70" height="1050" fill="#2a1a0e"/>'
    inside = ('<path d="M200,1180 L1100,1180 L1150,1240 L150,1240 Z" fill="#3a2a18"/>'
              '<ellipse cx="420" cy="1160" rx="120" ry="40" fill="#0a0604"/><ellipse cx="320" cy="1150" rx="50" ry="40" fill="#0a0604"/>'
              '<ellipse cx="760" cy="1166" rx="110" ry="36" fill="#0a0604"/><ellipse cx="860" cy="1154" rx="44" ry="36" fill="#0a0604"/>')
    woman = ('<g fill="#060302"><ellipse cx="1360" cy="760" rx="44" ry="54"/>'
             '<path d="M1300,740 C1270,820 1260,920 1250,1000 C1230,1060 1240,1120 1300,1160 L1480,1160 C1490,1100 1450,1020 1430,960 C1420,880 1420,800 1410,740 Q1360,700 1300,740 Z"/></g>'
             '<path d="M1410,740 C1420,800 1420,880 1430,960 C1450,1020 1490,1100 1480,1160" stroke="#8fb0d0" stroke-width="6" fill="none" opacity="0.6" filter="url(#blur1)"/>')
    return svg(wall, glow(600, 1000, 900, 'warm', 0.45), out_, door, inside, candle(1050, 1180, 50, 14), woman, '<rect width="2400" height="1350" fill="url(#paper)"/>')

@art
def rio_alba():
    shawl = ('<path d="M1700,1010 C1740,980 1790,990 1830,1020 C1840,1080 1820,1140 1800,1180 C1780,1140 1760,1100 1720,1080 Z" fill="#e8e4dc" opacity="0.9"/>'
             '<path d="M1720,1080 l-6,40 M1740,1090 l-4,44 M1760,1100 l-2,40 M1800,1180 l2,26" stroke="#e8e4dc" stroke-width="3"/>')
    return svg(sky('#5a6670', '#c8b8b0', mid='#8a929a'), glow(1700, 640, 900, 'white', 0.45), ridge(760, 90, '#4a5560', 7), ridge(820, 50, '#3a444e', 2),
               water(820, 1350, '#7a8892', '#28323a'), reflection(1700, 825, 1350, color='#f0e6e0', width=240),
               tree(380, 860, 560, 77, '#1a2228', 'willow', 0.1), tree(1760, 1000, 260, 78, '#10161b', 'bare', -0.2),
               '<path d="M1400,1010 C1600,980 2000,990 2400,1000 L2400,1060 C2000,1040 1600,1040 1400,1030 Z" fill="#141a1f"/>', shawl,
               reeds(0, 900, 1340, 7, '#10161b', 80, 260), mist(860, 100, 0.45, col='#e6e2de', seed=77), mist(1100, 160, 0.25, col='#e6e2de', seed=78))

@art
def presagio():
    r = random.Random(81)
    roofs = ""
    for i in range(12):
        x = i * 220 - 60 + r.uniform(-30, 30); y = 980 + r.uniform(-40, 60); w = r.uniform(220, 300)
        roofs += f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{1350-y:.0f}" fill="#0d0907"/><rect x="{x-6:.0f}" y="{y-10:.0f}" width="{w+12:.0f}" height="14" fill="#1c1612"/><rect x="{x-6:.0f}" y="{y-10:.0f}" width="{w+12:.0f}" height="3" fill="#6a7a8a" opacity="0.6"/>'
    people = "".join(sil_person(x, y, h, k, '#030202') for x, y, h, k in [(380, 990, 190, 'man'), (450, 995, 170, 'woman'), (1580, 975, 200, 'man'), (1650, 980, 120, 'child'), (2050, 1010, 180, 'woman'), (900, 1030, 150, 'woman')])
    arms = '<path d="M395,840 l40,-60 M1600,820 l30,-70 M2060,860 l-30,-60" stroke="#030202" stroke-width="12" stroke-linecap="round"/>'
    temple = f'<g transform="translate(1850,1000) scale(0.7)">{pyramid(0, 0, 620, 300, "#120c08", 5, 2, lit="#ff9a3c")}</g>'
    return svg(sky('#03050a', '#1a1e28', mid='#0a0e16'), stars(260, 81, 900), moon(400, 200, 46, phase=0.35),
               temple, roofs, people, arms, mist(1000, 60, 0.18, seed=81))

@art
def cruce():
    r = random.Random(91)
    paths = ('<polygon points="0,1350 700,1350 1250,860 1150,860" fill="#1e1a16"/><polygon points="1700,1350 2400,1350 1280,860 1180,860" fill="#1e1a16"/>'
             '<polygon points="0,1000 0,1100 2400,1030 2400,960" fill="#1a1612"/>')
    altar = ('<rect x="1100" y="900" width="200" height="110" fill="#2a2420"/><rect x="1080" y="890" width="240" height="16" fill="#3a322a"/>'
             + glow(1200, 880, 160, 'warm', 0.7) + candle(1160, 892, 30, 10) + candle(1240, 892, 30, 10) +
             '<path d="M1200,880 C1180,820 1230,780 1200,700 C1190,660 1210,630 1200,600" stroke="#9aa0a8" stroke-width="10" fill="none" opacity="0.35" filter="url(#blur1)"/>')
    ghosts = "".join(f'<g opacity="{o}">{place(llorona("stand", seed=92+i, veil_on=False, horns=True, glow=True, wind=0.8), x, y, h)}</g>'
                     for i, (x, y, h, o) in enumerate([(700, 1030, 380, 0.45), (1700, 1010, 330, 0.4), (1420, 900, 200, 0.35)]))
    return svg(sky('#03060a', '#16202a'), stars(180, 91, 700), moon(1900, 220, 50, phase=0.4), ridge(860, 70, '#060a0e', 91),
               '<rect x="0" y="860" width="2400" height="490" fill="#0c0b0a"/>', paths, altar,
               tree(250, 1000, 700, 93, '#030507', 'bare', 0.2), ghosts, mist(980, 90, 0.4, seed=91))

@art
def cielo_luna2():
    r = random.Random(12)
    clouds = "".join(blur_ell(r.uniform(0, 2400), r.uniform(150, 900), r.uniform(300, 700), r.uniform(50, 110), r.choice(['#141c26', '#1c2632', '#0e141c']), 0.9, 3) for _ in range(10))
    return svg(sky('#020409', '#0e1822'), stars(300, 12, 1100), moon(1500, 380, 120, phase=0.42), clouds,
               tree(500, 1350, 900, 12, '#010203', 'bare', 0.15), ridge(1250, 60, '#010203', 12))

@art
def ventana_moderna():
    r = random.Random(5)
    outside = ('<rect x="600" y="150" width="1200" height="1000" fill="#0c1a28"/>' + glow(1350, 420, 600, 'moon', 0.9) + moon(1350, 420, 70) + stars(60, 5, 900) +
               ridge(950, 80, '#05090e', 5).replace('points="0,', 'points="0,') )
    frame = ('<rect width="2400" height="1350" fill="#0a0d12"/>')
    sash = ('<rect x="580" y="130" width="1240" height="40" fill="#5a6470"/><rect x="580" y="1130" width="1240" height="50" fill="#5a6470"/>'
            '<rect x="580" y="130" width="40" height="1050" fill="#5a6470"/><rect x="1780" y="130" width="40" height="1050" fill="#5a6470"/>'
            '<rect x="1180" y="130" width="36" height="1050" fill="#4a535e"/>'
            '<rect x="500" y="1180" width="1400" height="40" fill="#2a3038"/>')
    plant = '<g transform="translate(760,1180)">' + "".join(f'<path d="M0,0 Q{a*0.4:.0f},-60 {a:.0f},-{120+abs(a)*0.2:.0f}" stroke="#0a120c" stroke-width="10" fill="none"/>' for a in (-80, -40, 0, 40, 80)) + '<rect x="-40" y="-20" width="80" height="60" fill="#1a1612"/></g>'
    return svg(frame, outside, '<g clip-path="none">' + '</g>', sash, plant)

@art
def cortina():
    folds = "".join(f'<path d="M{x},120 C{x+25},400 {x-25},800 {x+10},1180" stroke="#c8d8e8" stroke-width="{w}" fill="none" opacity="{o}"/>'
                    for x, w, o in [(640 + i * 75, 50 + (i % 3) * 18, 0.10 + (i % 4) * 0.03) for i in range(16)])
    return svg('<rect x="560" y="100" width="1280" height="20" rx="8" fill="#1a1e24"/>',
               '<rect x="600" y="120" width="1200" height="1060" fill="#c8d8e8" opacity="0.10"/>', f'<g filter="url(#blur1)">{folds}</g>',
               "".join(f'<circle cx="{620+i*75}" cy="118" r="10" fill="#2a3038"/>' for i in range(17)))

@art
def sombra_moderna():
    return svg(f'<g opacity="0.9" filter="url(#blur2)"><g fill="#02050a">'
               '<ellipse cx="1200" cy="400" rx="70" ry="88"/>'
               '<path d="M1120,360 C1050,480 1000,800 960,1180 L1440,1180 C1400,800 1350,480 1280,360 Q1200,300 1120,360 Z"/>'
               '<path d="M1140,520 C1100,640 1090,760 1100,840 L1124,840 C1120,760 1130,640 1160,530 Z"/>'
               '<path d="M1270,520 C1330,600 1400,640 1470,650 L1470,672 C1390,670 1320,630 1260,560 Z"/></g></g>'
               '<path d="M1468,650 l30,-8 l4,8 l-30,10 Z M1470,664 l34,0 l0,8 l-34,0 Z" fill="#02050a" opacity="0.8" filter="url(#blur1)"/>')

@art
def rio_puente():
    stone = "#1e2730"
    body = f'<rect x="0" y="742" width="2400" height="300" fill="{stone}"/>'
    openings = "".join(f'<path d="M{x-190},1042 L{x-190},960 A190,150 0 0 1 {x+190},960 L{x+190},1042 Z" fill="#101c26"/>'
                       f'<path d="M{x-190},960 A190,150 0 0 1 {x+190},960" stroke="#4a5c6e" stroke-width="5" fill="none" opacity="0.7"/>'
                       + "".join(f'<path d="M{x-190+k*38},{960-150*math.sin(math.pi*k/10):.0f} l{(k-5)*3},-22" stroke="#141b22" stroke-width="4"/>' for k in range(1, 10))
                       for x in range(240, 2400, 480))
    blocks = "".join(f'<path d="M0,{y} L2400,{y}" stroke="#151c23" stroke-width="3"/>' for y in (790, 840, 890))
    top = '<rect x="0" y="700" width="2400" height="44" fill="#232d37"/><rect x="0" y="698" width="2400" height="6" fill="#6a7e92" opacity="0.6"/>'
    refl = "".join(f'<path d="M{x-190},1042 A190,110 0 0 0 {x+190},1042" stroke="{stone}" stroke-width="30" fill="none" opacity="0.5"/>' for x in range(240, 2400, 480))
    lamps = lamp(700, 702, 300) + lamp(2000, 702, 300, lit=False)
    return svg(sky('#03070d', '#1a2c3c', mid='#0b1724'), stars(200, 44, 600), moon(1700, 230, 80),
               ridge(720, 100, '#0a141e', 44), water(1040, 1350, '#1e3242', '#04080d'), reflection(1700, 1045, 1350, width=200),
               refl, body, blocks, openings, top, lamps, mist(1060, 60, 0.3, seed=44), reeds(0, 2400, 1350, 45, '#020407', 40, 160))


if __name__ == "__main__":
    os.makedirs("art", exist_ok=True)
    names = sys.argv[1:] or list(ART)
    for n in names:
        open(f"art/{n}.svg", "w").write(ART[n]())
        print("wrote", n)
