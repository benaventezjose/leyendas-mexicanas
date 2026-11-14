#!/usr/bin/env python3
"""Illustrations for 'La Xtabay' — writes art/*.svg (2400x1350).
Render: node /home/claude/pipeline/render_svg.js art/*.svg      Usage: python3 make_art.py [name ...]"""
import sys, os, math, random
sys.path.insert(0, '/home/claude/pipeline'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from helpers import *          # village/interior helpers from the previous video (fogon, interior, man_sil, moon_sky…)
from xchars import *
from xchars import xtabay_bust as xbust

ART = {}
def art(fn):
    ART[fn.__name__] = fn
    return fn

G = lambda x, y, k, f, flip=False: f'<g transform="translate({x},{y}) scale({-k if flip else k},{k})">{f}</g>'
R = lambda c="#000", op=1.0: f'<rect width="2400" height="1350" fill="{c}" opacity="{op}"/>'
NIGHT_TOP, NIGHT_BOT = "#02070c", "#10303a"   # Yucatán night: teal


# ------------------------------------------------------------------ Yucatán scenery
def ceiba(x, base, k=1.0, color="#03070a", rim="#9cc8e0", seed=3, thorns=True, glow_=False):
    """Sacred ceiba (yaxché): straight massive trunk, flaring buttress roots, horizontal tiered branches, flat crown."""
    r = random.Random(seed)
    s = f'<g transform="translate({x},{base}) scale({k})">'
    # crown: flat umbrella of foliage clumps
    for i in range(70):
        cx = r.uniform(-900, 900); cy = -1050 + abs(cx) * 0.12 + r.uniform(-90, 60)
        s += f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{r.uniform(80,170):.0f}" ry="{r.uniform(40,80):.0f}" fill="{color}"/>'
    # main horizontal limbs
    for side in (-1, 1):
        for j, (y0, L) in enumerate(((-760, 760), (-900, 880), (-640, 520))):
            s += (f'<path d="M0,{y0} C{side*L*0.3:.0f},{y0-60} {side*L*0.6:.0f},{y0-120} {side*L:.0f},{y0-200-j*30}" '
                  f'stroke="{color}" stroke-width="{46-j*10}" fill="none" stroke-linecap="round"/>')
            for q in range(3):
                bx = side * L * (0.4 + q * 0.2)
                s += f'<path d="M{bx:.0f},{y0-80-q*30} l{side*r.uniform(40,120):.0f},{-r.uniform(80,160):.0f}" stroke="{color}" stroke-width="16" stroke-linecap="round"/>'
    # trunk with buttresses
    s += (f'<path d="M-70,-1000 C-80,-700 -90,-400 -110,-200 C-160,-110 -330,-40 -460,0 L460,0 C330,-40 160,-110 110,-200 '
          f'C90,-400 80,-700 70,-1000 Z" fill="{color}"/>')
    for bx, w in ((-300, 70), (-150, 60), (170, 60), (320, 70)):  # buttress ridges
        s += f'<path d="M{bx*0.3:.0f},-260 C{bx*0.6:.0f},-120 {bx:.0f},-40 {bx*1.3:.0f},0 L{bx*1.3+w*(1 if bx>0 else -1):.0f},0 C{bx*1.1:.0f},-60 {bx*0.5:.0f},-160 {bx*0.2:.0f},-280 Z" fill="#000" opacity="0.45"/>'
    if thorns:
        for i in range(60):
            ty = r.uniform(-980, -220); tx = r.choice((-1, 1)) * r.uniform(60, 80) * (1 + (-ty < 300) * 0.4)
            s += f'<path d="M{tx:.0f},{ty:.0f} l{(-1 if tx<0 else 1)*14},-4 l{(-1 if tx<0 else 1)*-14},-8 Z" fill="{color}"/>'
            s += f'<circle cx="{r.uniform(-50,50):.0f}" cy="{ty:.0f}" r="{r.uniform(3,6):.1f}" fill="#000" opacity="0.6"/>'
    s += f'<path d="M-70,-1000 C-80,-700 -90,-400 -110,-200 C-160,-110 -330,-40 -460,0" stroke="{rim}" stroke-width="5" fill="none" opacity="0.5" filter="url(#blur1)"/>'
    s += f'<path d="M70,-1000 C80,-700 90,-400 110,-200" stroke="{rim}" stroke-width="3" fill="none" opacity="0.25"/>'
    if glow_:
        s += '<ellipse cx="0" cy="-30" rx="600" ry="120" fill="url(#moonglow)" opacity="0.4"/>'
    s += '</g>'
    return s


def monte(y, color="#040a0c", seed=1, h=260, n=40, x0=-100, x1=2500, rim=None):
    """Low dry Yucatecan scrub forest: rounded bushes with thin trunks, a few taller chacás."""
    r = random.Random(seed); s = ""
    for _ in range(n):
        x = r.uniform(x0, x1); hh = r.uniform(h * 0.5, h * 1.2); yy = y + r.uniform(-20, 20)
        s += f'<path d="M{x:.0f},{yy:.0f} l{r.uniform(-20,20):.0f},{-hh*0.6:.0f}" stroke="{color}" stroke-width="10"/>'
        for j in range(4):
            s += f'<ellipse cx="{x+r.uniform(-90,90):.0f}" cy="{yy-hh*r.uniform(0.6,1.0):.0f}" rx="{r.uniform(60,130):.0f}" ry="{r.uniform(40,80):.0f}" fill="{color}"/>'
        if rim and r.random() < 0.5:
            s += f'<path d="M{x-60:.0f},{yy-hh:.0f} q60,-40 120,0" stroke="{rim}" stroke-width="3" fill="none" opacity="0.3"/>'
    s += f'<rect x="0" y="{y}" width="2400" height="{1350-y}" fill="{color}"/>'
    return s


def chaca(x, base, h=700, seed=1, bark="#3a1a14", rim="#d07060"):
    """Chacá (palo mulato): twisting reddish trunk with peeling bark."""
    r = random.Random(seed)
    s = f'<path d="M{x-30},{base} C{x-40},{base-h*0.4} {x+30},{base-h*0.6} {x},{base-h} L{x+20},{base-h} C{x+50},{base-h*0.6} {x-10},{base-h*0.4} {x+30},{base} Z" fill="{bark}"/>'
    for i in range(5):
        a = r.uniform(-1, 1)
        s += f'<path d="M{x+10},{base-h*(0.55+i*0.08):.0f} q{a*120:.0f},-{r.uniform(80,160):.0f} {a*260:.0f},-{r.uniform(120,240):.0f}" stroke="{bark}" stroke-width="{14-i*2}" fill="none"/>'
    for i in range(8):
        yy = base - r.uniform(0.1, 0.9) * h
        s += f'<path d="M{x-10:.0f},{yy:.0f} q14,-10 26,0" stroke="{rim}" stroke-width="3" fill="none" opacity="0.35"/>'
    s += f'<path d="M{x-30},{base} C{x-40},{base-h*0.4} {x+30},{base-h*0.6} {x},{base-h}" stroke="{rim}" stroke-width="4" fill="none" opacity="0.4"/>'
    return s


def sac_path(y_far=760, color="#c8d4d0", op=0.55, x_far=1200, w_far=40):
    """Sacbé-like white limestone path running into the distance."""
    s = f'<path d="M{x_far-w_far},{y_far} L{x_far+w_far},{y_far} L1900,1350 L500,1350 Z" fill="{color}" opacity="{op}"/>'
    r = random.Random(4)
    for _ in range(140):
        t = r.random(); yy = y_far + (1350 - y_far) * t; half = w_far + (700 - w_far) * t
        s += f'<ellipse cx="{x_far + r.uniform(-half, half):.0f}" cy="{yy:.0f}" rx="{2+t*10:.1f}" ry="{1+t*4:.1f}" fill="#0a1214" opacity="0.4"/>'
    return s


def maya_house(x, base, k=1.0, lit=True, wall="#c8c2b0", roof="#3a2c18", door_lit=None, night=True):
    """Traditional Maya house: oval whitewashed walls, very steep palm-thatch (huano) roof, door in the middle."""
    s = f'<g transform="translate({x},{base}) scale({k})">'
    wc = "#2a3436" if night else wall
    s += f'<path d="M-300,0 L-300,-210 C-300,-240 300,-240 300,-210 L300,0 Z" fill="{wc}"/>'
    s += '<path d="M-300,0 L-300,-210 C-300,-240 -200,-240 -200,-230 L-200,0 Z" fill="#000" opacity="0.25"/>'
    # thatch
    s += f'<path d="M-360,-190 C-330,-200 -150,-560 0,-580 C150,-560 330,-200 360,-190 C200,-170 -200,-170 -360,-190 Z" fill="{roof}"/>'
    r = random.Random(int(x))
    for i in range(60):
        xx = r.uniform(-330, 330)
        s += f'<path d="M{xx:.0f},-185 L{xx*0.25:.0f},{-560+abs(xx)*0.3:.0f}" stroke="#000" stroke-width="3" opacity="0.3"/>'
    s += f'<path d="M-360,-190 C-200,-170 200,-170 360,-190" stroke="#000" stroke-width="8" opacity="0.4" fill="none"/>'
    dl = lit if door_lit is None else door_lit
    s += f'<path d="M-50,0 L-50,-160 L50,-160 L50,0 Z" fill="{"#ffb050" if dl else "#050505"}"/>'
    if dl:
        s += '<circle cx="0" cy="-80" r="200" fill="url(#warmglow)" opacity="0.65"/>'
        s += '<path d="M-50,0 L50,0 L140,60 L-140,60 Z" fill="#ffb050" opacity="0.25"/>'
    s += '<path d="M-150,-560 C-50,-590 50,-590 150,-560" stroke="#9fc2e8" stroke-width="3" fill="none" opacity="0.25"/>'
    s += '</g>'
    return s


def agave(x, y, k=1.0, color="#4e6a62", dk="#24342e", seed=1):
    """Henequen plant: rosette of long rigid grey-green spiked leaves."""
    r = random.Random(seed); s = f'<g transform="translate({x},{y}) scale({k})">'
    for i in range(16):
        a = -170 + i * 160 / 15 + r.uniform(-5, 5); L = r.uniform(170, 240)
        ax, ay = math.cos(math.radians(a)) * L, math.sin(math.radians(a)) * L
        px, py = -math.sin(math.radians(a)) * 12, math.cos(math.radians(a)) * 12
        c = color if i % 2 else dk
        s += f'<path d="M{px:.0f},{py:.0f} L{ax:.0f},{ay:.0f} L{-px:.0f},{-py:.0f} Z" fill="{c}"/>'
    s += '</g>'
    return s


def hammock(x0, y0, x1, y1, sag=170, col="#c8303a", col2="#e8b030"):
    mx = (x0 + x1) / 2; my = max(y0, y1) + sag
    s = f'<path d="M{x0},{y0} Q{mx},{my+60} {x1},{y1} Q{mx},{my-40} {x0},{y0} Z" fill="{col}"/>'
    for i in range(10):
        t = i / 9
        s += f'<path d="M{x0},{y0} Q{mx},{my-40+t*100} {x1},{y1}" stroke="{col2 if i%3==0 else "#7a1820"}" stroke-width="3" fill="none" opacity="0.6"/>'
    return s


def tomb(x, base, k=1.0, col="#6a6a66", cross=True):
    s = f'<g transform="translate({x},{base}) scale({k})">'
    s += f'<path d="M-200,0 L-180,-90 L180,-90 L200,0 Z" fill="{col}"/><path d="M-180,-90 L180,-90 L170,-110 L-170,-110 Z" fill="#8a8a84"/>'
    if cross:
        s += f'<path d="M-10,-110 L-10,-330 L10,-330 L10,-110 Z M-70,-270 L70,-270 L70,-250 L-70,-250 Z" fill="#3a2a1c"/>'
    s += '</g>'
    return s


def vine_flowers(x0, x1, y0, y1, n=40, seed=1, glow=False):
    r = random.Random(seed); s = ""
    for i in range(6):
        s += f'<path d="M{x0},{r.uniform(y0,y1):.0f} C{x0+(x1-x0)*0.3:.0f},{r.uniform(y0,y1):.0f} {x0+(x1-x0)*0.7:.0f},{r.uniform(y0,y1):.0f} {x1},{r.uniform(y0,y1):.0f}" stroke="#1e3a22" stroke-width="7" fill="none"/>'
    for _ in range(n * 2):
        lx, ly = r.uniform(x0, x1), r.uniform(y0, y1)
        s += f'<path d="M{lx:.0f},{ly:.0f} c20,-30 50,-30 60,0 c-10,30 -40,30 -60,0 Z" fill="#2a5a32" transform="rotate({r.uniform(0,360):.0f} {lx:.0f} {ly:.0f})"/>'
    for _ in range(n):
        s += trumpet(r.uniform(x0, x1), r.uniform(y0, y1), r.uniform(0.6, 1.1), r.uniform(-60, 60), glow=glow)
    return s


def tzacam_plant(x, y, k=1.0, flowers=True, col="#4a6a3a", dk="#24361e", seed=2):
    """Small globular Mammillaria cactus covered in white spines, with a ring of small flowers."""
    r = random.Random(seed); s = f'<g transform="translate({x},{y}) scale({k})">'
    for cx, cy, rr in ((0, -110, 120), (-150, -70, 80), (140, -60, 86)):
        g = uid("tz")
        s += f'<defs>{grad_rad(g, [(0, col, 1), (1, dk, 1)], 0.4, 0.35, 0.7)}</defs>'
        s += f'<circle cx="{cx}" cy="{cy}" r="{rr}" fill="url(#{g})"/>'
        for i in range(int(rr * 0.9)):
            a = r.uniform(0, 6.28); d = rr * math.sqrt(r.random())
            px, py = cx + math.cos(a) * d, cy + math.sin(a) * d * 0.95
            for j in range(4):
                b = r.uniform(0, 6.28)
                s += f'<path d="M{px:.0f},{py:.0f} l{math.cos(b)*14:.0f},{math.sin(b)*14:.0f}" stroke="#e8e4d4" stroke-width="1.4" opacity="0.8"/>'
        if flowers:
            for i in range(9):
                a = -2.6 + i * 0.27
                s += flower(cx + math.cos(a) * rr * 0.8, cy + math.sin(a) * rr * 0.8, rr * 0.16, "#b8a070", "#6a5a2a", 6, i * 15)
    s += '</g>'
    return s


def yuc_night(seed=1, mx=1750, my=260, r=105):
    return moon_sky(seed, mx, my, r, NIGHT_TOP, NIGHT_BOT)


# ================================================================== NIGHT / MONTE
@art
def monte_path():
    s = yuc_night(2, 1200, 230, 95)
    s += monte(780, "#06121a", 3, 160, 50) + mist(760, 80, 0.3, "#9ab8c4", 2)
    s += sac_path(760)
    s += chaca(420, 1150, 800, 1) + chaca(1950, 1180, 900, 2)
    s += monte(1180, "#020608", 7, 300, 26, -200, 700) + monte(1180, "#020608", 8, 300, 26, 1700, 2600)
    s += '<rect x="0" y="1180" width="2400" height="170" fill="#000" opacity="0"/>'
    s += mist(1100, 140, 0.25, "#b0c8d0", 5)
    return svg(s)


@art
def monte_path_day():
    s = sky("#7a8c94", "#d4d8d0") + monte(780, "#2a3634", 3, 160, 50) + mist(760, 80, 0.5, "#e8ece8", 2)
    s += sac_path(760, "#e8e6dc", 0.8)
    s += chaca(420, 1150, 800, 1, "#6a3a2a", "#e0a080") + chaca(1950, 1180, 900, 2, "#6a3a2a", "#e0a080")
    s += monte(1180, "#141c1a", 7, 300, 26, -200, 700) + monte(1180, "#141c1a", 8, 300, 26, 1700, 2600)
    s += ceiba(1200, 790, 0.22, "#1a2422", "#e8ece8", thorns=False)
    s += mist(1050, 160, 0.4, "#f0f2ee", 5)
    return svg(s)


@art
def monte_dense():
    s = yuc_night(5, 600, 200, 70)
    s += monte(700, "#071419", 11, 220, 50) + mist(700, 120, 0.3, "#8ab0bc", 3)
    for i, x in enumerate((200, 520, 880, 1560, 1900, 2250)):
        s += chaca(x, 1300, 1000 + (i % 3) * 120, i + 3, "#1a0e0c", "#7aa8bc")
    s += monte(1050, "#030708", 13, 380, 40) + mist(1000, 160, 0.3, "#9ab8c4", 7)
    r = random.Random(2)
    for _ in range(40):  # hanging vines
        x = r.uniform(0, 2400)
        s += f'<path d="M{x:.0f},0 C{x+r.uniform(-40,40):.0f},{r.uniform(200,400):.0f} {x+r.uniform(-60,60):.0f},{r.uniform(400,600):.0f} {x+r.uniform(-30,30):.0f},{r.uniform(500,800):.0f}" stroke="#020506" stroke-width="{r.uniform(3,8):.0f}" fill="none"/>'
    return svg(s)


@art
def ceiba_night():
    s = yuc_night(3, 1850, 230, 110)
    s += monte(900, "#061418", 4, 200, 40) + mist(900, 100, 0.35, "#a8c8d0", 6)
    s += '<ellipse cx="1200" cy="1180" rx="900" ry="120" fill="#24343a" opacity="0.8"/>'  # moonlit clearing
    s += ceiba(1200, 1180, 1.0)
    s += monte(1290, "#010304", 9, 200, 30)
    s += mist(1150, 120, 0.3, "#c0d8e0", 8)
    return svg(s)


@art
def l_xtabay_back():
    return svg(xtabay_full(1520, 1185, 430, back=True, comb=True))


@art
def l_xtabay_front():
    return svg(xtabay_full(1200, 1160, 560, back=False, comb=False))


@art
def l_lencho_walk():
    return svg(man_walk(980, 1120, 300, facing=1, lantern=True))


@art
def l_brush_fg():
    r = random.Random(4); s = ""
    for cx, cy in ((0, 1350), (2400, 1350), (200, 1400), (2200, 1420)):
        for i in range(30):
            a = r.uniform(-170, -10); L = r.uniform(200, 420)
            ax, ay = cx + math.cos(math.radians(a)) * L, cy + math.sin(math.radians(a)) * L
            s += f'<path d="M{cx},{cy} Q{(cx+ax)/2+r.uniform(-60,60):.0f},{(cy+ay)/2:.0f} {ax:.0f},{ay:.0f}" stroke="#010203" stroke-width="{r.uniform(10,26):.0f}" fill="none" stroke-linecap="round"/>'
            s += f'<ellipse cx="{ax:.0f}" cy="{ay:.0f}" rx="{r.uniform(30,60):.0f}" ry="{r.uniform(12,22):.0f}" fill="#010203" transform="rotate({a:.0f} {ax:.0f} {ay:.0f})"/>'
    return svg(s)


@art
def l_wisp():
    r = random.Random(6); s = ""
    for i in range(7):
        y = r.uniform(400, 1000)
        s += (f'<path d="M{r.uniform(1400,2400):.0f},{y:.0f} C{r.uniform(1000,1400):.0f},{y-r.uniform(60,160):.0f} {r.uniform(600,1000):.0f},{y+r.uniform(60,160):.0f} {r.uniform(0,600):.0f},{y-r.uniform(0,120):.0f}" '
              f'stroke="#f4f0e0" stroke-width="{r.uniform(10,30):.0f}" fill="none" opacity="{r.uniform(0.15,0.35):.2f}" filter="url(#blur3)"/>')
    for _ in range(14):
        s += trumpet(r.uniform(200, 2200), r.uniform(300, 1100), r.uniform(0.3, 0.5), r.uniform(0, 360), "#ffffff").replace("<g ", '<g opacity="0.5" ')
    return svg(s)


@art
def l_eyes():
    r = random.Random(8); s = ""
    for _ in range(9):
        x, y = r.uniform(150, 2250), r.uniform(450, 1000); d = r.uniform(18, 30)
        for dx in (-d, d):
            s += f'<circle cx="{x+dx:.0f}" cy="{y:.0f}" r="22" fill="url(#redglow)"/><ellipse cx="{x+dx:.0f}" cy="{y:.0f}" rx="7" ry="5" fill="#ff3a20"/>'
    return svg(s)


@art
def l_fire_glow():
    return svg(glow(1200, 1220, 520, "warm", 0.8) + glow(1200, 1250, 220, "warm", 0.9))


@art
def l_candle_glow():
    return svg(glow(1750, 640, 320, "warm", 0.85))


@art
def title_bg():
    s = yuc_night(7, 1720, 300, 120)
    s += monte(900, "#05121a", 2, 220, 50) + mist(880, 120, 0.4, "#a8c8d0", 1)
    s += ceiba(1200, 1150, 0.95, "#020507", "#bfe0f0", glow_=True)
    s += monte(1260, "#010203", 5, 180, 30)
    s += '<rect x="0" y="0" width="2400" height="1350" fill="#000" opacity="0.15"/>'
    return svg(s)


@art
def roots():
    """Close on the buttress roots: walls of wood with a black gap between them."""
    s = yuc_night(9, 300, 160, 70)
    s += monte(700, "#061418", 4, 160, 40)
    s += '<path d="M900,0 L1500,0 L1520,1350 L880,1350 Z" fill="#030608"/>'  # trunk fills top
    for side in (-1, 1):
        for j in range(3):
            x0 = 1200 + side * (120 + j * 80)
            s += (f'<path d="M{x0},{-50} C{x0+side*40},{500} {x0+side*(300+j*200)},{900+j*60} {x0+side*(700+j*260)},1350 L{1200+side*(80+j*60)},1350 '
                  f'C{1200+side*(80+j*40)},1000 {1200+side*(60+j*40)},500 {1200+side*(40+j*30)},-50 Z" fill="{["#0a1418", "#071014", "#050a0c"][j]}"/>')
            s += f'<path d="M{x0},{-50} C{x0+side*40},{500} {x0+side*(300+j*200)},{900+j*60} {x0+side*(700+j*260)},1350" stroke="#7aa8c0" stroke-width="5" fill="none" opacity="{0.45-j*0.12:.2f}" filter="url(#blur1)"/>'
    s += '<path d="M1110,1350 C1130,1000 1160,700 1200,500 C1240,700 1270,1000 1290,1350 Z" fill="#000"/>'
    s += mist(1250, 120, 0.3, "#9ab8c4", 4)
    return svg(s)


@art
def roots_dark():
    s = roots().replace("</svg>", "")
    s += '<ellipse cx="1200" cy="1000" rx="240" ry="380" fill="#000" opacity="0.7" filter="url(#blur3)"/>'
    # torn white shirt glimpse and a limp hand in the dark gap (implied, no gore)
    s += '<path d="M1140,1150 C1170,1100 1240,1100 1270,1150 L1290,1350 L1120,1350 Z" fill="#8a948c" opacity="0.55"/>'
    s += '<path d="M1180,1180 l20,40 l-12,30 M1230,1170 l-10,60" stroke="#1a1a1a" stroke-width="4" opacity="0.6"/>'
    s += '<path d="M1290,1200 C1340,1220 1380,1260 1390,1300 C1370,1310 1340,1290 1320,1280 Z" fill="#5a4a40" opacity="0.7"/>'
    for i in range(6):
        s += f'<path d="M{1150+i*20},{1160+i*12} l{30+i*4},-8" stroke="#6a1a14" stroke-width="2" opacity="0.5"/>'
    return s + "</svg>"


@art
def roots_hat():
    s = roots().replace("</svg>", "")
    s += '<g transform="translate(1500,1250) rotate(-12) scale(0.9)">' + sombrero(tilt=0) + '</g>'
    s += '<rect width="2400" height="1350" fill="#c8d8e0" opacity="0.08"/>'
    return s + "</svg>"


@art
def xtabentun_night():
    s = yuc_night(12, 2000, 200, 80) + monte(800, "#061418", 6, 200, 40)
    s += '<rect x="0" y="0" width="2400" height="1350" fill="#000" opacity="0.35"/>'
    s += vine_flowers(0, 2400, 300, 1300, 70, 4, glow=True)
    s += mist(900, 160, 0.2, "#e8f0f0", 3)
    return svg(s)


@art
def xtabentun_flower():
    s = sky("#0e2a30", "#3a6a68") + glow(1200, 600, 900, "white", 0.35)
    s += vine_flowers(-100, 2500, 100, 1300, 30, 9)
    s += trumpet(1200, 760, 4.2, -8, glow=True) + trumpet(820, 900, 2.6, -40) + trumpet(1650, 980, 2.8, 30)
    return svg(s)


@art
def tzacam():
    s = sky("#0a1418", "#24363a") + '<ellipse cx="1200" cy="1150" rx="1300" ry="260" fill="#1a1612"/>'
    r = random.Random(3)
    for _ in range(160):
        s += f'<ellipse cx="{r.uniform(0,2400):.0f}" cy="{r.uniform(1000,1350):.0f}" rx="{r.uniform(6,20):.0f}" ry="{r.uniform(4,10):.0f}" fill="#3a342c" opacity="0.7"/>'
    s += tzacam_plant(1200, 1120, 2.6) + tzacam_plant(400, 1180, 1.1, seed=5) + tzacam_plant(2000, 1200, 1.3, seed=7)
    s += glow(1200, 700, 500, "moon", 0.3)
    return svg(s)


@art
def comb_spines():
    s = sky("#040a10", "#0e2028") + glow(1300, 500, 700, "moon", 0.45)
    r = random.Random(5)
    for i in range(160):  # cascade of hair filling the frame
        x = 700 + i * 6 + r.uniform(-10, 10)
        s += f'<path d="M{x:.0f},-20 C{x+r.uniform(-60,60):.0f},400 {x+r.uniform(-80,80):.0f},900 {x+r.uniform(-40,40)+80:.0f},1380" stroke="{["#07060a","#0c0e16","#2a3650"][i%3]}" stroke-width="{r.uniform(4,10):.1f}" fill="none"/>'
    s += G(1300, 700, 2.4, comb_hand())
    return svg(s)


@art
def xtabay_back():
    s = yuc_night(14, 600, 220, 90)
    s += '<path d="M1600,0 C1580,400 1600,900 1560,1350 L2400,1350 L2400,0 Z" fill="#030608"/>'  # trunk right
    s += '<path d="M1600,0 C1580,400 1600,900 1560,1350" stroke="#9cc8e0" stroke-width="6" fill="none" opacity="0.4"/>'
    s += monte(1000, "#061418", 5, 200, 30, -100, 1600)
    s += '<ellipse cx="1000" cy="1300" rx="900" ry="120" fill="#22343a"/>'
    s += xtabay_full(1050, 1300, 980, back=True, comb=True, hair_len=1.05)
    s += mist(1250, 100, 0.25, "#c0d8e0", 2)
    return svg(s)


@art
def xtabay_profile():
    """Three-quarter view looking back over the shoulder, hair falling, moon behind."""
    s = yuc_night(15, 1600, 330, 260) + monte(1100, "#04101a", 7, 160, 30)
    s += xbust(1150, 560, 1.5, look=0.8, turn=0.45, smile=0.6, lids=0.35)
    return svg(s)


@art
def xtabay_bust():
    s = yuc_night(16, 1200, 330, 300) + monte(1150, "#04101a", 2, 180, 30)
    s += xbust(1200, 560, 1.55, smile=0.55, lids=0.25)
    return svg(s)


@art
def xtabay_scare():
    s = sky("#000000", "#0a1418") + glow(1200, 500, 700, "moon", 0.25)
    s += xbust(1200, 560, 1.7, scare=2, rim="#c0e0ff")
    s += '<rect width="2400" height="1350" fill="#2a0000" opacity="0.15"/>'
    return svg(s)


@art
def hair_snakes():
    s = sky("#020507", "#0a1a20") + glow(1200, 450, 600, "moon", 0.3)
    s += xbust(1200, 600, 1.4, scare=1, smile=0.7, lids=0.1)
    return svg(s)


@art
def l_tendrils():
    r = random.Random(11); s = ""
    for i in range(12):
        side = -1 if i % 2 else 1
        x0 = 1200 + side * r.uniform(160, 260); y0 = r.uniform(300, 900)
        pts = [(x0, y0)]
        for j in range(5):
            pts.append((pts[-1][0] + side * r.uniform(60, 110), pts[-1][1] + r.uniform(-90, 90)))
        d = f"M{pts[0][0]:.0f},{pts[0][1]:.0f} " + " ".join(f"Q{(a[0]+b[0])/2 + side*20:.0f},{(a[1]+b[1])/2 - 60*(1 if k%2 else -1):.0f} {b[0]:.0f},{b[1]:.0f}" for k, (a, b) in enumerate(zip(pts, pts[1:])))
        s += f'<path d="{d}" stroke="#07060a" stroke-width="{r.uniform(16,28):.0f}" fill="none" stroke-linecap="round"/>'
        s += f'<path d="{d}" stroke="#4a6080" stroke-width="2" fill="none" opacity="0.5"/>'
        hx, hy = pts[-1]
        s += f'<ellipse cx="{hx:.0f}" cy="{hy:.0f}" rx="26" ry="16" fill="#07060a"/><circle cx="{hx+side*12:.0f}" cy="{hy-4:.0f}" r="3" fill="#e8f4ff"/>'
        s += f'<path d="M{hx+side*24:.0f},{hy:.0f} l{side*18},-4 m0,4 l{side*-4},6" stroke="#a01818" stroke-width="2"/>'
    return svg(s)


@art
def utz_pact():
    s = sky("#000000", "#14060a") + glow(1200, 900, 700, "red", 0.35)
    s += monte(700, "#050203", 9, 300, 50) + monte(1000, "#020101", 10, 300, 40)
    # Utz Colel's pale ghost rising from the grave, arms open to the dark
    s += tomb(1200, 1250, 1.3, "#2a2426", cross=False)
    s += f'<g opacity="0.85">{ghost_woman(1200, 1120, 640, "#d8dce4", 0.7)}</g>'
    s += mist(1150, 140, 0.35, "#8a5a60", 3)
    return svg(s)


@art
def xtabay_guardian():
    """Forest spirit version: the woman among animals under the ceiba, calm, fireflies."""
    s = sky("#06141a", "#2a5a58") + glow(1200, 500, 800, "moon", 0.35)
    s += monte(900, "#081a1c", 3, 200, 50)
    s += ceiba(1200, 1220, 0.9, "#041014", "#c0e8e0", thorns=False)
    s += xtabay_full(1200, 1200, 520, comb=False, rim="#d0f0e0")
    # deer and birds as silhouettes
    s += '<g transform="translate(650,1200) scale(1.2)"><path d="M0,0 L10,-120 C20,-170 80,-180 140,-170 L170,-230 L150,-250 L190,-240 L200,-200 C210,-190 210,-170 190,-160 L180,-120 L190,0 L172,0 L160,-110 L60,-110 L40,0 Z" fill="#030a0c"/><path d="M180,-245 l-20,-60 l10,30 l-30,-20 M195,-240 l10,-60 l-8,30 l26,-20" stroke="#030a0c" stroke-width="6" fill="none"/></g>'
    s += '<g transform="translate(1760,1200) scale(-1.0,1.0)"><path d="M0,0 L10,-120 C20,-170 80,-180 140,-170 L170,-230 L150,-250 L190,-240 L200,-200 C210,-190 210,-170 190,-160 L180,-120 L190,0 L172,0 L160,-110 L60,-110 L40,0 Z" fill="#030a0c"/></g>'
    for x, y in ((900, 520), (1500, 480), (1650, 600)):
        s += f'<path d="M{x},{y} q20,-20 40,0 q20,-20 40,0" stroke="#030a0c" stroke-width="7" fill="none"/>'
    return svg(s)


# ================================================================== VILLAGE / HACIENDA / PEOPLE
def warm_sky():
    return sky("#3a2a3a", "#e8a060", "#b0605a")


@art
def hacienda():
    s = warm_sky() + glow(1700, 760, 500, "warm", 0.6)
    s += ridge(820, 30, "#4a3a3a", 2)
    # casco: arcade of arches + tall brick chimney
    s += '<rect x="500" y="560" width="1100" height="300" fill="#6a4a3a"/>'
    for i in range(9):
        x = 560 + i * 115
        s += f'<path d="M{x},860 L{x},680 A45,45 0 0 1 {x+90},680 L{x+90},860 Z" fill="#2a1a16"/>'
    s += '<rect x="480" y="540" width="1140" height="30" fill="#8a6a50"/><path d="M500,540 L560,470 L1540,470 L1600,540 Z" fill="#5a3a2a"/>'
    s += '<path d="M1750,860 L1780,300 L1840,300 L1870,860 Z" fill="#5a2e22"/><rect x="1770" y="280" width="80" height="30" fill="#3a1e16"/>'
    s += '<path d="M1810,280 C1780,200 1860,150 1820,60 C1900,120 1980,60 2100,90" stroke="#8a7a7a" stroke-width="40" fill="none" opacity="0.4" filter="url(#blur3)"/>'
    for row in range(5):
        y = 900 + row * 100
        for i in range(14):
            s += agave(i * 190 + (row % 2) * 95, y, 0.45 + row * 0.18, "#5a7068", "#2a3832", row * 20 + i)
    return svg(s)


@art
def henequen():
    s = warm_sky() + ridge(700, 20, "#5a4a44", 3)
    for row in range(6):
        y = 740 + row * 120
        for i in range(12):
            s += agave(i * 230 + (row % 2) * 115 - 60, y, 0.35 + row * 0.25, "#5a7068", "#2a3832", row * 30 + i)
    # workers cutting pencas, silhouettes
    s += man_sil(700, 1060, 380, hat=True, machete=True, color="#120c0a", rim="#ffb070")
    s += man_sil(1500, 1000, 300, hat=True, machete=True, color="#120c0a", rim="#ffb070", facing=-1)
    s += '<path d="M1600,1000 l200,0 l-20,-70 l-160,0 Z" fill="#5a7068"/>'  # bundle of leaves
    return svg(s)


@art
def lencho_portrait():
    s = sky("#2a1a14", "#6a3a22") + glow(700, 600, 700, "warm", 0.45)
    s += lencho_bust(1200, 560, 1.5, rim="#ffcf8a", smile=0.4)
    return svg(s)


@art
def lencho_drunk():
    s = sky("#1a0e0a", "#4a2a18") + glow(1800, 500, 600, "warm", 0.6)
    s += lencho_bust(1150, 600, 1.45, rim="#ffcf8a", lids=0.6, smile=-0.2, look=-0.5)
    s += '<g transform="translate(1650,1100)"><path d="M-40,0 L-50,-200 C-50,-240 -20,-260 -20,-300 L-20,-360 L20,-360 L20,-300 C20,-260 50,-240 50,-200 L40,0 Z" fill="#2a4a2a" opacity="0.85"/><path d="M-30,-180 L30,-180 L30,-80 L-30,-80 Z" fill="#c8b070" opacity="0.7"/></g>'
    return svg(s)


@art
def lencho_scared():
    s = yuc_night(17, 600, 300, 160) + monte(1100, "#04101a", 4, 160, 30)
    s += lencho_bust(1200, 560, 1.55, rim="#bfe0ff", fear=True)
    return svg(s)


@art
def casa_maya():
    s = yuc_night(18, 1800, 240, 90) + monte(860, "#061418", 2, 200, 40)
    s += maya_house(1100, 1080, 1.2, lit=True)
    s += maya_house(2050, 980, 0.6, lit=False) + maya_house(300, 990, 0.65, lit=False)
    s += '<path d="M0,1080 L2400,1060 L2400,1350 L0,1350 Z" fill="#070d10"/>'
    s += '<path d="M0,1150 Q600,1120 1200,1150 T2400,1140" stroke="#5a6a6a" stroke-width="40" fill="none" opacity="0.4"/>'  # albarrada stone wall
    r = random.Random(3)
    for _ in range(80):
        s += f'<ellipse cx="{r.uniform(0,2400):.0f}" cy="{1145+r.uniform(-15,15):.0f}" rx="{r.uniform(14,24):.0f}" ry="{r.uniform(8,14):.0f}" fill="#1a2224"/>'
    return svg(s)


def house_inside(lit=True):
    s = interior("#4a3a2a" if lit else "#1a2228", "#1a120c" if lit else "#080a0c", (1750, 700))
    s += hammock(300, 500, 1300, 480, 220)
    # altar: shelf with Virgin image and candle
    s += '<rect x="1600" y="720" width="320" height="24" fill="#2a1a10"/>'
    s += '<path d="M1700,720 L1700,520 C1700,480 1820,480 1820,520 L1820,720 Z" fill="#1a3a6a"/><ellipse cx="1760" cy="600" rx="40" ry="70" fill="#d8c08a" opacity="0.7"/>'
    s += '<path d="M1760,560 C1720,560 1720,640 1760,700 C1800,640 1800,560 1760,560 Z" fill="#2a4a8a"/>'
    for i in range(10):
        a = math.radians(-90 + (i - 4.5) * 14)
        s += f'<path d="M1760,600 l{math.cos(a)*110:.0f},{math.sin(a)*110:.0f}" stroke="#f0c860" stroke-width="3" opacity="0.6"/>'
    if lit:
        s += candle(1750, 700, 40, 14)
    else:
        s += '<rect x="1743" y="660" width="14" height="40" fill="#c8c0b0"/><path d="M1750,660 C1740,600 1770,560 1745,500" stroke="#a0a8b0" stroke-width="5" fill="none" opacity="0.5" filter="url(#blur1)"/>'
    return s


@art
def house_inside_dark():
    s = house_inside(False)
    s += woman_sil(700, 1300, 700, color="#05070a", rim="#7a9cc4")
    s += '<rect width="2400" height="1350" fill="#02060c" opacity="0.35"/>'
    return svg(s)


@art
def candelaria_portrait():
    s = house_inside(True) + '<rect width="2400" height="1350" fill="#000" opacity="0.35"/>'
    s += candelaria_bust(1100, 560, 1.5, rim="#ffcf8a", smile=0.3)
    return svg(s)


@art
def candelaria_close():
    s = sky("#1a0e08", "#3a2414") + glow(1700, 500, 600, "warm", 0.6)
    s += candelaria_bust(1150, 560, 1.7, rim="#ffcf8a", smile=-0.3, lids=0.1, look=0.6)
    return svg(s)


@art
def candelaria_door():
    s = yuc_night(19, 600, 250, 80) + monte(900, "#061418", 6, 220, 40)
    s += '<rect x="1300" y="0" width="1100" height="1350" fill="#120c08"/>'
    s += '<path d="M1500,250 L1900,250 L1900,1350 L1500,1350 Z" fill="#e8a050"/>' + glow(1700, 700, 500, "warm", 0.8)
    s += woman_sil(1680, 1300, 820, color="#0a0604", rim="#ffcf8a", facing=-1)
    s += '<path d="M1560,800 C1540,860 1560,900 1590,880" stroke="#c8a860" stroke-width="5" fill="none"/><path d="M1585,880 l0,26 m-10,-14 l20,0" stroke="#c8a860" stroke-width="5"/>'  # rosary
    s += monte(1300, "#010304", 3, 120, 20, -100, 1300)
    return svg(s)


@art
def candelaria_fire():
    s = interior("#3a2418", "#1a100a", (1200, 1100)) + fogon(1200, 1250, 1.2)
    s += candelaria_bust(1200, 560, 1.25, rim="#ffb060", smile=-0.4, lids=0.2)
    s += '<path d="M1300,1150 C1500,1000 1700,1100 1900,900 C2000,800 2100,850 2200,700" stroke="#050505" stroke-width="4" fill="none" opacity="0.8"/>'  # the long hair burning away
    return svg(s)


@art
def cantina():
    s = interior("#5a3a22", "#2a180c", (1200, 500))
    s += '<rect x="200" y="300" width="2000" height="20" fill="#2a1a0e"/>'
    r = random.Random(4)
    for i in range(26):  # bottles on a shelf
        x = 240 + i * 75; h = r.uniform(90, 150)
        s += f'<path d="M{x},{300} L{x},{300-h*0.6:.0f} C{x},{300-h*0.75:.0f} {x+10},{300-h*0.8:.0f} {x+10},{300-h:.0f} L{x+20},{300-h:.0f} C{x+20},{300-h*0.8:.0f} {x+30},{300-h*0.75:.0f} {x+30},{300-h*0.6:.0f} L{x+30},300 Z" fill="{r.choice(["#2a4a2a","#5a3a1a","#3a2a1a","#6a5a3a"])}" opacity="0.9"/>'
    s += lamp(1200, 0, 420, lit=True) if False else glow(1200, 450, 500, "warm", 0.8)
    s += '<rect x="0" y="900" width="2400" height="80" fill="#3a2010"/><rect x="0" y="980" width="2400" height="370" fill="#1a0e06"/>'
    for i, x in enumerate((400, 800, 1650, 2050)):
        s += man_sil(x, 1350, 640 + (i % 2) * 60, hat=True, color="#0a0604", rim="#ffb060", facing=(1 if i < 2 else -1))
    s += man_sil(1220, 1350, 700, hat=True, color="#0a0604", rim="#ffcf8a")
    return svg(s)


@art
def cantina_out():
    s = yuc_night(20, 1900, 220, 80)
    s += '<rect x="0" y="400" width="900" height="800" fill="#1a1e22"/><rect x="300" y="700" width="200" height="500" fill="#e8a050"/>' + glow(400, 950, 400, "warm", 0.7)
    s += '<path d="M0,1200 L2400,1180 L2400,1350 L0,1350 Z" fill="#0a0e10"/>' + sac_path(800, op=0.35, x_far=1700, w_far=30)
    s += monte(900, "#061418", 4, 200, 30, 900, 2500)
    s += man_walk(800, 1250, 520, facing=1, lantern=True, drunk=True)
    return svg(s)


@art
def abuela_fire():
    s = interior("#3a2418", "#1a100a", (1200, 1100)) + fogon(1200, 1250, 1.3)
    s += woman_sil(700, 1300, 620, color="#0a0604", rim="#ffb060", facing=1)
    s += man_sil(1750, 1300, 640, hat=False, color="#0a0604", rim="#ffb060", facing=-1)
    for x in (1500, 1950):
        s += woman_sil(x, 1300, 360, color="#0a0604", rim="#ffb060", facing=-1)
    return svg(s)


@art
def abuela_portrait():
    s = interior("#3a2418", "#1a100a", (1200, 1300)) + '<rect width="2400" height="1350" fill="#000" opacity="0.3"/>'
    s += abuela_bust(1200, 560, 1.55, rim="#ffb060")
    return svg(s)


@art
def village_old():
    s = sky("#6a8a94", "#e8d8b0") + glow(1900, 400, 500, "warm", 0.5)
    s += monte(780, "#3a4a40", 2, 160, 40)
    for i, (x, k) in enumerate(((300, 0.7), (900, 0.85), (1650, 0.75), (2200, 0.6))):
        s += maya_house(x, 900 + k * 60, k, lit=False, night=False, roof="#6a5030", door_lit=False)
    s += '<path d="M0,960 L2400,940 L2400,1350 L0,1350 Z" fill="#b8a888"/>'
    s += '<ellipse cx="1250" cy="1150" rx="120" ry="40" fill="#5a5a50"/><ellipse cx="1250" cy="1145" rx="90" ry="26" fill="#1a2024"/>'  # well
    for x, f in ((500, 1), (1700, -1), (1950, -1)):
        s += woman_sil(x, 1250, 380, color="#2a2420", rim=None, facing=f)
    s += man_sil(800, 1240, 380, hat=True, color="#2a2420", rim=None)
    return svg(s)


@art
def xkeban_portrait():
    s = sky("#4a3a3a", "#d89a60") + glow(1700, 500, 700, "warm", 0.5)
    s += vine_flowers(1700, 2500, 100, 1300, 18, 3)
    s += xkeban_bust(1100, 560, 1.5, rim="#ffd6a0")
    return svg(s)


@art
def xkeban_kind():
    s = sky("#5a6a74", "#e8c890") + monte(800, "#4a5a48", 5, 140, 40)
    s += '<path d="M0,900 L2400,880 L2400,1350 L0,1350 Z" fill="#a89878"/>'
    s += maya_house(400, 920, 0.7, lit=False, night=False, roof="#6a5030", door_lit=False)
    # Xkeban kneeling, giving water to an old sick man, dogs around her
    s += xkeban_bust(1250, 790, 0.95, rim="#ffd6a0", look=-0.8, turn=-0.3)
    s += man_sil(800, 1300, 560, hat=False, color="#3a2a22", rim="#ffd6a0", pose="stand")
    for x, f in ((1650, 1), (1900, -1), (2150, 1)):
        s += (f'<g transform="translate({x},1300) scale({f*0.9},0.9)"><path d="M-120,0 L-110,-90 C-120,-140 -60,-170 40,-160 C80,-200 120,-210 140,-180 L170,-160 L150,-140 C130,-130 120,-110 120,-90 L130,0 L110,0 L95,-70 L-60,-70 L-90,0 Z" fill="#3a2a1e"/>'
              f'<path d="M-115,-120 C-150,-140 -170,-110 -180,-80" stroke="#3a2a1e" stroke-width="12" fill="none"/></g>')
    return svg(s)


@art
def utz_portrait():
    s = sky("#1a2430", "#5a6a7a") + glow(1700, 400, 500, "moon", 0.35)
    s += utz_bust(1150, 560, 1.5)
    return svg(s)


@art
def utz_disdain():
    s = sky("#3a4a58", "#a8b0b4") + monte(800, "#2a343a", 6, 140, 40)
    s += '<path d="M0,900 L2400,880 L2400,1350 L0,1350 Z" fill="#6a6a64"/>'
    s += maya_house(2000, 920, 0.8, lit=False, night=False, roof="#3a3a34", door_lit=False)
    s += utz_bust(1450, 720, 1.15, look=1.0, turn=0.35)
    s += man_sil(550, 1350, 620, hat=False, color="#14181c", rim="#a8c8e8", facing=1)
    s += '<path d="M640,980 C700,960 760,950 820,940" stroke="#14181c" stroke-width="34" stroke-linecap="round"/>'  # outstretched hand
    return svg(s)


@art
def xkeban_hammock():
    s = interior("#4a3424", "#1a120c", (1200, 700))
    s += '<rect width="2400" height="1350" fill="#ffd6a0" opacity="0.06"/>'
    s += hammock(350, 520, 2050, 520, 260, "#d8b890", "#f0e0c0")
    s += '<path d="M800,700 C1000,650 1400,650 1650,700 C1500,760 1000,760 800,700 Z" fill="#e8dcc4"/>'  # covered body, peaceful
    s += '<ellipse cx="760" cy="690" rx="60" ry="46" fill="#a87252"/><path d="M700,680 C720,630 800,630 820,680" fill="#0b0807"/>'
    s += vine_flowers(600, 1800, 560, 760, 18, 5, glow=True)
    for x in (700, 1300, 1800):
        s += (f'<g transform="translate({x},1250) scale(0.8)"><path d="M-160,0 C-160,-60 -100,-90 0,-90 C60,-120 120,-120 140,-80 L160,-60 L120,-40 C110,-20 80,0 60,0 Z" fill="#2a1e14"/></g>')
    return svg(s)


@art
def xkeban_grave():
    s = yuc_night(22, 1700, 220, 90) + monte(860, "#061418", 3, 200, 40)
    s += '<path d="M0,1000 L2400,980 L2400,1350 L0,1350 Z" fill="#0a1214"/>'
    s += tomb(1200, 1150, 1.4, "#3a4a4a") + glow(1200, 1000, 500, "white", 0.4)
    s += vine_flowers(800, 1600, 900, 1150, 40, 7, glow=True)
    for x, f in ((650, 1), (1800, -1)):
        s += (f'<g transform="translate({x},1200) scale({f*0.9},0.9)"><path d="M-120,0 L-110,-90 C-120,-140 -60,-170 40,-160 C80,-200 120,-210 140,-180 L170,-160 L150,-140 C130,-130 120,-110 120,-90 L130,0 L110,0 L95,-70 L-60,-70 L-90,0 Z" fill="#030608"/></g>')
    return svg(s)


@art
def utz_funeral():
    s = sky("#0a0c10", "#2a2a30") + monte(800, "#0c0e10", 4, 180, 40)
    s += '<path d="M0,950 L2400,930 L2400,1350 L0,1350 Z" fill="#141414"/>'
    s += '<path d="M900,1000 L1500,1000 L1460,1080 L940,1080 Z" fill="#3a2a1a"/>'  # coffin
    r = random.Random(5)
    for i in range(14):
        x = 150 + i * 165 + r.uniform(-30, 30); f = 1 if x < 1200 else -1
        s += woman_sil(x, 1300, r.uniform(380, 480), color="#050505", rim="#ffb060", facing=f) if i % 2 else man_sil(x, 1300, r.uniform(400, 480), hat=True, color="#050505", rim="#ffb060", facing=f)
        s += candle(x + 40 * f, 1100, 30, 10)
    # sickly green haze over the coffin
    s += '<ellipse cx="1200" cy="900" rx="500" ry="220" fill="#7a8a30" opacity="0.25" filter="url(#blur4)"/>'
    return svg(s)


@art
def utz_grave():
    s = sky("#4a5058", "#9aa0a0") + monte(800, "#2a3030", 3, 180, 40)
    s += '<path d="M0,1000 L2400,980 L2400,1350 L0,1350 Z" fill="#3a3630"/>'
    s += tomb(1200, 1150, 1.4, "#6a6a66")
    s += tzacam_plant(1200, 1060, 1.0, seed=4) + tzacam_plant(950, 1180, 0.6, seed=8) + tzacam_plant(1480, 1190, 0.7, seed=9)
    for i in range(10):  # wilted, vanished bouquet stems
        s += f'<path d="M{1000+i*40},1150 q-10,-40 -30,-50" stroke="#4a4030" stroke-width="4" fill="none"/>'
    s += mist(1100, 120, 0.3, "#c8ccc8", 2)
    return svg(s)


@art
def fist_closed():
    s = sky("#06101a", "#1a2a30") + glow(1200, 600, 600, "moon", 0.35)
    sk = SK_TOMAS
    s += f'<path d="M600,1350 C800,1100 950,900 1050,820 L1300,820 C1300,1000 1100,1250 1000,1350 Z" fill="#c8c8c0" opacity="0.8"/>'  # torn sleeve
    s += f'<path d="M1000,620 C1100,560 1350,560 1420,640 C1480,720 1460,860 1380,900 C1280,950 1100,930 1040,880 C980,820 960,680 1000,620 Z" fill="{sk["base"]}"/>'
    for i in range(4):
        s += f'<path d="M{1050+i*80},640 C{1040+i*80},720 {1080+i*80},760 {1120+i*80},740" stroke="{sk["deep"]}" stroke-width="6" fill="none" opacity="0.7"/>'
    s += f'<path d="M1000,700 C960,760 1000,820 1080,820 C1140,820 1160,780 1150,740" fill="{sk["light"]}" stroke="{sk["deep"]}" stroke-width="4"/>'  # thumb
    for i in range(10):
        s += f'<path d="M{1020+i*40},{700+(i%3)*50} l{30+i%3*10},{20+i%4*8}" stroke="#7a2018" stroke-width="2.5" opacity="0.55"/>'  # fine scratches
    s += '<path d="M1420,760 C1600,700 1800,820 2000,700 C2150,620 2300,700 2450,640" stroke="#050505" stroke-width="5" fill="none"/>'  # a hair escaping the fist
    return svg(s)


@art
def fist_open():
    s = sky("#06101a", "#1a2a30") + glow(1200, 650, 600, "moon", 0.4)
    sk = SK_TOMAS
    s += f'<path d="M700,1350 C850,1150 950,1000 1000,950 L1350,950 C1300,1100 1200,1250 1150,1350 Z" fill="#c8c8c0" opacity="0.8"/>'
    s += f'<path d="M950,800 C900,700 1050,620 1200,620 C1350,620 1480,700 1460,820 C1440,940 1300,1000 1150,990 C1020,980 980,900 950,800 Z" fill="{sk["base"]}"/>'
    for i, (x, a) in enumerate(((1000, -120), (1110, -100), (1220, -90), (1330, -80))):
        s += f'<path d="M{x},680 l{math.cos(math.radians(a))*230:.0f},{math.sin(math.radians(a))*230:.0f}" stroke="{sk["base"]}" stroke-width="80" stroke-linecap="round"/>'
        s += f'<path d="M{x},680 l{math.cos(math.radians(a))*230:.0f},{math.sin(math.radians(a))*230:.0f}" stroke="{sk["light"]}" stroke-width="20" stroke-linecap="round" opacity="0.4"/>'
    s += f'<path d="M1420,820 L1600,700" stroke="{sk["base"]}" stroke-width="86" stroke-linecap="round"/>'
    s += '<path d="M1080,840 L1300,770" stroke="#f0e8d4" stroke-width="8" stroke-linecap="round"/><path d="M1300,770 l14,-4" stroke="#f0e8d4" stroke-width="3"/>'  # the spine
    s += ('<path d="M1100,830 C1180,860 1250,790 1300,810 C1400,850 1500,760 1600,800 C1750,860 1850,700 2000,760 C2150,820 2250,700 2450,760" stroke="#050505" stroke-width="5" fill="none"/>'
          '<path d="M1150,850 C1250,900 1300,950 1250,1050 C1200,1150 1300,1250 1250,1400" stroke="#050505" stroke-width="5" fill="none"/>')
    return svg(s)


@art
def search_dawn():
    s = sky("#5a6a78", "#d8c8b8") + monte(800, "#2a3436", 2, 180, 50) + mist(800, 120, 0.5, "#e8ecec", 2)
    s += sac_path(800, "#e0ddd2", 0.7)
    s += monte(1180, "#0e1416", 5, 260, 24, -200, 700) + monte(1180, "#0e1416", 6, 260, 24, 1700, 2600)
    for i, x in enumerate((900, 1050, 1250, 1400)):
        s += man_sil(x, 1050 + i * 20, 300, hat=True, machete=True, color="#14181a", rim="#f0d8c0", facing=1 if i % 2 else -1)
    s += woman_sil(1150, 1150, 330, color="#14181a", rim="#f0d8c0")
    return svg(s)


# ================================================================== HISTORY
@art
def landa_book():
    s = interior("#3a2418", "#1a100a", (1750, 640))
    s += '<rect x="0" y="900" width="2400" height="450" fill="#2a180c"/>'
    s += '<path d="M600,980 L1200,900 L1800,980 L1800,1040 L1200,960 L600,1040 Z" fill="#e8dcb8"/>'
    s += '<path d="M600,980 L1200,900 L1200,960 L600,1040 Z" fill="#d8c8a0"/>'
    r = random.Random(4)
    for side in (-1, 1):
        for i in range(12):
            y = 950 + i * 6 - (1 if side < 0 else 0) * 0
            x0 = 1200 + side * 60; x1 = 1200 + side * 560
            s += f'<path d="M{x0},{920+i*8} L{x1},{1000+i*8-50}" stroke="#3a2a1a" stroke-width="2" opacity="0.5" stroke-dasharray="{r.randint(6,20)} 6"/>'
    s += '<path d="M1500,880 C1560,700 1640,600 1700,560" stroke="#e8e0d0" stroke-width="10" fill="none"/>'  # quill
    s += candle(1750, 700, 90, 22) if False else candle(1750, 880, 120, 26)
    return svg(s)


@art
def old_book():
    s = interior("#2a1e18", "#140c08", (1750, 640))
    s += '<rect x="0" y="900" width="2400" height="450" fill="#2a180c"/>'
    s += '<path d="M700,1000 L1600,1000 L1650,880 L750,880 Z" fill="#6a2a1a"/><path d="M750,880 L1650,880 L1640,860 L760,860 Z" fill="#e8dcc0"/>'
    s += '<text x="1180" y="980" text-anchor="middle" font-family="Cinzel" font-size="40" fill="#e0c070" transform="skewX(-10)">EL MAYAB</text>'
    s += candle(1750, 880, 120, 26)
    return svg(s)


@art
def codex():
    s = sky("#c8a870", "#a88050")
    r = random.Random(2)
    for i in range(5):  # folded screen-fold pages
        x = 150 + i * 430
        s += f'<rect x="{x}" y="150" width="410" height="1050" fill="#e8d8b0"/><rect x="{x}" y="150" width="410" height="1050" fill="none" stroke="#7a5a30" stroke-width="4"/>'
        for row in range(3):
            y = 220 + row * 330
            s += f'<path d="M{x+20},{y+300} L{x+390},{y+300}" stroke="#a83a20" stroke-width="6"/>'
            for g in range(3):  # glyph cartouches
                gx = x + 40 + g * 120
                s += f'<rect x="{gx}" y="{y}" width="100" height="90" rx="22" fill="{r.choice(["#3a6a7a","#a83a20","#d8a040"])}" opacity="0.8" stroke="#2a1a10" stroke-width="4"/>'
                s += f'<circle cx="{gx+35}" cy="{y+40}" r="12" fill="#2a1a10"/><path d="M{gx+20},{y+70} q30,-20 60,0" stroke="#2a1a10" stroke-width="4" fill="none"/>'
            # stylized seated figure
            fx_ = x + 120 + (row % 2) * 160
            s += f'<g transform="translate({fx_},{y+280})"><path d="M-40,0 L-30,-80 L30,-80 L50,0 Z" fill="#c86a3a" stroke="#2a1a10" stroke-width="4"/><circle cx="0" cy="-110" r="32" fill="#c8884a" stroke="#2a1a10" stroke-width="4"/><path d="M-30,-140 L30,-150 L20,-130 Z" fill="#3a6a7a"/><circle cx="8" cy="-112" r="5" fill="#2a1a10"/></g>'
    s += '<rect width="2400" height="1350" fill="#3a2010" opacity="0.15"/>'
    return svg(s)


@art
def ceiba_sacred():
    """Three worlds: stars above, the living earth, the underworld roots below."""
    s = sky("#020610", "#0e2a3a")
    s += stars(260, 9, 500)
    s += '<rect x="0" y="760" width="2400" height="590" fill="#050403"/>'
    s += '<path d="M0,760 L2400,760" stroke="#c89a50" stroke-width="4" opacity="0.6"/>'
    s += monte(770, "#0a1a18", 5, 140, 40)
    s += ceiba(1200, 770, 0.75, "#0a1c1a", "#c0e8d8", thorns=False)
    r = random.Random(3)
    for i in range(16):  # roots into the underworld
        a = r.uniform(-1, 1)
        s += f'<path d="M{1200+a*80:.0f},770 C{1200+a*300:.0f},950 {1200+a*700:.0f},1100 {1200+a*1100:.0f},{r.uniform(1150,1350):.0f}" stroke="#2a1a10" stroke-width="{r.uniform(8,26):.0f}" fill="none"/>'
    s += glow(1200, 1250, 500, "red", 0.35) + glow(1200, 250, 500, "moon", 0.4)
    s += '<text x="620" y="220" font-family="Cinzel" font-size="50" fill="#c0d8e0" opacity="0.7">CIELO</text>'
    s += '<text x="620" y="720" font-family="Cinzel" font-size="50" fill="#e0c890" opacity="0.7">TIERRA</text>'
    s += '<text x="620" y="1150" font-family="Cinzel" font-size="50" fill="#d07060" opacity="0.7">XIBALBÁ</text>'
    return svg(s)


@art
def bottle():
    s = interior("#3a2418", "#1a100a", (1750, 640)) + '<rect x="0" y="1000" width="2400" height="350" fill="#2a180c"/>'
    g = uid("bt")
    s += f'<defs>{grad_lin(g, [(0, "#6a3a08", 0.9), (0.5, "#e8a830", 0.85), (1, "#8a5010", 0.9)], 1000, 0, 1400, 0)}</defs>'
    s += f'<path d="M1050,1000 L1050,620 C1050,560 1150,540 1160,480 L1160,300 L1240,300 L1240,480 C1250,540 1350,560 1350,620 L1350,1000 Z" fill="url(#{g})"/>'
    s += '<rect x="1150" y="260" width="100" height="50" fill="#3a2010"/><rect x="1080" y="700" width="240" height="180" fill="#f0e8d0"/>'
    s += '<text x="1200" y="790" text-anchor="middle" font-family="Cinzel" font-size="34" fill="#3a2010">XTABENTÚN</text>'
    s += trumpet(1200, 850, 0.6)
    s += '<path d="M1080,640 C1120,600 1160,620 1180,660" stroke="#fff" stroke-width="8" fill="none" opacity="0.4"/>'
    for x, y in ((700, 950), (800, 990)):  # star anise
        for i in range(8):
            a = math.radians(i * 45)
            s += f'<ellipse cx="{x+math.cos(a)*24:.0f}" cy="{y+math.sin(a)*12:.0f}" rx="16" ry="8" fill="#5a2a14" transform="rotate({i*45} {x+math.cos(a)*24:.0f} {y+math.sin(a)*12:.0f})"/>'
    s += '<path d="M1500,1000 C1500,900 1700,900 1700,1000 Z" fill="#c88a20"/><path d="M1600,900 L1600,860" stroke="#6a4a20" stroke-width="10"/>'  # honey pot
    s += candle(1750, 880, 120, 26)
    return svg(s)


@art
def aluxes_tease():
    s = yuc_night(30, 1900, 230, 90) + monte(850, "#061418", 3, 200, 40)
    s += '<path d="M0,1000 L2400,980 L2400,1350 L0,1350 Z" fill="#0a1210"/>'
    r = random.Random(5)
    for i in range(30):  # milpa: maize stalks
        x = r.uniform(0, 2400); h = r.uniform(260, 420); y = r.uniform(1000, 1100)
        s += f'<path d="M{x:.0f},{y:.0f} L{x+r.uniform(-10,10):.0f},{y-h:.0f}" stroke="#14281a" stroke-width="8"/>'
        for j in range(4):
            sd = 1 if j % 2 else -1
            s += f'<path d="M{x:.0f},{y-h*(0.3+j*0.15):.0f} q{sd*60},-30 {sd*130},10" stroke="#14281a" stroke-width="7" fill="none"/>'
    # three tiny figures with glowing eyes among the maize
    for x, y, k in ((900, 1150, 1.0), (1250, 1180, 0.85), (1550, 1140, 0.9)):
        s += f'<g transform="translate({x},{y}) scale({k})"><path d="M-50,0 C-60,-80 -50,-120 0,-130 C50,-120 60,-80 50,0 Z" fill="#030606"/><circle cx="0" cy="-150" r="42" fill="#030606"/><path d="M-50,-170 L0,-230 L50,-170 Z" fill="#030606"/><circle cx="-14" cy="-152" r="7" fill="#ffd060"/><circle cx="14" cy="-152" r="7" fill="#ffd060"/></g>'
    s += mist(1150, 100, 0.3, "#a8c8c0", 3)
    return svg(s)


if __name__ == "__main__":
    os.makedirs("art", exist_ok=True)
    names = sys.argv[1:] or list(ART)
    for n in names:
        open(f"art/{n}.svg", "w").write(ART[n]())
    print(len(names), "svg written")
