#!/usr/bin/env python3
"""Illustrations for 'El Jinete sin Cabeza / El Muerto' (la franja del Nueces, 1850) — writes art/*.svg (2400x1350).
New here: a custom galloping mustang, the headless rider tied to the saddle (sombrero hanging from the horn), the
mesquite-and-nopal brush country, Vidal, the two rinches, the camp, the fort, the aguaje, the unmarked grave.
Reuses helpers of earlier videos (beso_art, chars, base_chars, cadejo_art, sb_art, aguacate_art, azul_art, qm_art).
Usage: python3 make_art.py [name ...]   then: node /home/claude/pipeline/render_svg.js art/*.svg"""
import sys, os, math, random, re
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '/home/claude/pipeline'); sys.path.insert(0, HERE)
from art import *
from art import reflection as refl
from beso_art import S, clouds, portrait_bg, candle_at, MOONRIM
from chars import place, man_full, woman_full, luis_bust, father_bust
from cadejo_art import smooth, limb, hoof_print, stones
import cadejo_art as CJ
import sb_art as SB
import aguacate_art as AG
import azul_art as AZ
import qm_art as QM

A = os.path.join(HERE, "art"); os.makedirs(A, exist_ok=True)
ART = {}
def art(fn):
    ART[fn.__name__] = fn; return fn

RED = "#c8141a"; WARM = "#ffcf8a"; RAW = "#b89060"
def dim(op=0.3, col="#02040a"): return f'<rect width="2400" height="1350" fill="{col}" opacity="{op}"/>'
def fogb(y, op=0.3, seed=4): return QM.fog_band(y, op, seed)


def _flat(frag, c):
    frag = re.sub(r'fill="(?!none)[^"]*"', f'fill="{c}"', frag)
    frag = re.sub(r'stroke="(?!none)[^"]*"', f'stroke="{c}"', frag)
    return frag


# ============================================================ the mustang (facing right, ground y=0, withers ~ -650)
TORSO = [(-330, -642), (-200, -618), (-60, -606), (80, -622), (180, -655), (250, -720), (320, -800), (390, -850),
         (430, -880), (452, -925), (470, -884), (520, -850), (590, -790), (640, -735), (648, -712), (630, -694),
         (580, -690), (520, -705), (460, -730), (400, -712), (350, -640), (318, -560), (295, -490), (240, -425),
         (120, -388), (-60, -380), (-220, -405), (-350, -455), (-430, -530), (-438, -600), (-400, -632)]


def hoof(x, y, ang, col="#050403"):
    return f'<g transform="translate({x:.1f},{y:.1f}) rotate({-ang:.1f})"><path d="M-22,-30 L22,-30 L30,4 L-26,4 Z" fill="{col}"/></g>'


def leg(x, y, a1, a2, l1, l2, w1, w2, col):
    s = limb(x, y, a1, a2, l1, l2, w1, w2, foot="none", col=col)
    r1, r2 = math.radians(a1), math.radians(a2)
    kx, ky = x + l1 * math.sin(r1), y + l1 * math.cos(r1)
    fx, fy = kx + l2 * math.sin(r2), ky + l2 * math.cos(r2)
    return s + hoof(fx, fy, a2)


POSES = {
    #          front-near           front-far            hind-near             hind-far
    "gallop": [(55, 95, 215, 215), (-25, -95, 200, 190), (-50, -25, 230, 240), (20, -20, 225, 235)],
    "stand":  [(4, 0, 220, 220), (-6, 2, 220, 220), (8, -6, 230, 235), (-4, -10, 230, 235)],
    "rear":   [(70, 140, 200, 180), (50, 120, 200, 180), (25, 0, 230, 240), (5, -5, 230, 240)],
    "walk":   [(18, 4, 220, 220), (-14, -30, 215, 210), (-16, -8, 230, 235), (14, -8, 230, 235)],
}


def mustang(pose="gallop", col="#06070b", rim=MOONRIM, seed=3, mane_wind=1.0):
    r = random.Random(seed)
    P = POSES[pose]
    far = "#030305"
    s = ""
    a1, a2, l1, l2 = P[1]; s += leg(250, -470, a1, a2, l1, l2, 46, 19, far)
    a1, a2, l1, l2 = P[3]; s += leg(-330, -500, a1, a2, l1, l2, 58, 19, far)
    for i in range(16):  # tail
        y0 = -610 + r.uniform(-8, 8); ln = r.uniform(260, 380)
        s += (f'<path d="M-420,{y0:.0f} C{-520-ln*0.2:.0f},{y0-40*mane_wind+r.uniform(-30,30):.0f} {-560-ln*0.5:.0f},{y0+60+r.uniform(-40,40):.0f} '
              f'{-440-ln:.0f},{y0+90*(1.2-mane_wind)+r.uniform(-60,60):.0f}" stroke="{col}" stroke-width="{r.uniform(8,18):.0f}" fill="none" stroke-linecap="round"/>')
    s += f'<path d="{smooth(TORSO)}" fill="{col}"/>'
    a1, a2, l1, l2 = P[0]; s += leg(270, -480, a1, a2, l1, l2, 52, 21, col)
    a1, a2, l1, l2 = P[2]; s += leg(-340, -510, a1, a2, l1, l2, 64, 21, col)
    s += f'<path d="M-400,-600 C-360,-520 -300,-470 -230,-450" stroke="{rim}" stroke-width="5" fill="none" opacity="0.35"/>'
    s += f'<path d="M230,-640 C280,-560 300,-520 290,-480" stroke="{rim}" stroke-width="4" fill="none" opacity="0.3"/>'
    s += f'<path d="M80,-580 C120,-520 180,-480 240,-440" stroke="#000" stroke-width="10" fill="none" opacity="0.25"/>'
    for i in range(22):  # mane
        t = i / 21
        bx = 440 - 260 * t; by = -880 + 230 * t
        ln = r.uniform(70, 130)
        s += (f'<path d="M{bx:.0f},{by:.0f} q{-ln*0.6*mane_wind:.0f},{-20+r.uniform(-20,20):.0f} {-ln*mane_wind:.0f},{r.uniform(10,50):.0f}" '
              f'stroke="{col}" stroke-width="{r.uniform(9,16):.0f}" fill="none" stroke-linecap="round"/>')
    s += '<circle cx="505" cy="-835" r="9" fill="#d8e4f0" opacity="0.8"/><circle cx="505" cy="-835" r="5" fill="#000"/>'
    s += '<ellipse cx="628" cy="-718" rx="10" ry="6" fill="#000"/>'
    s += f'<path d="M440,-905 L452,-960 L472,-900 Z" fill="{col}"/>'
    s += '<path d="M470,-880 L560,-760 M500,-860 L610,-720 M560,-760 L610,-720" stroke="#2a1a10" stroke-width="7" fill="none"/>'
    return s


def rider(col="#07080c", rim=MOONRIM, cloth="#1a1410"):
    """the headless rider seated on the saddle, arms bound to the horn, sombrero hanging from it by rawhide"""
    s = ""
    s += '<path d="M-120,-612 C-60,-640 90,-650 170,-662 L176,-610 C90,-596 -40,-590 -126,-584 Z" fill="#3a1e10"/>'
    s += '<path d="M-90,-650 C-40,-670 60,-676 130,-680 L150,-700 C170,-716 186,-716 186,-700 L176,-660 C90,-640 -20,-630 -96,-626 Z" fill="#24140a"/>'
    s += '<rect x="168" y="-728" width="20" height="40" rx="6" fill="#2a160a"/><ellipse cx="178" cy="-730" rx="22" ry="9" fill="#3a2010"/>'
    s += '<path d="M20,-660 C60,-600 90,-540 110,-470 L84,-460 C60,-520 30,-580 0,-640 Z" fill="#030304"/>'
    s += f'<path d="M-30,-690 C40,-680 120,-640 160,-560 C176,-520 170,-470 160,-410 L110,-410 C114,-470 112,-520 96,-560 C70,-610 10,-630 -40,-640 Z" fill="{col}"/>'
    s += '<path d="M104,-420 L166,-420 L176,-372 C200,-366 214,-356 212,-340 L96,-340 Z" fill="#0a0604"/>'
    s += '<path d="M80,-330 L230,-330" stroke="#5a4a3a" stroke-width="7"/><path d="M150,-560 L156,-330" stroke="#2a1a10" stroke-width="6"/>'
    s += '<path d="M150,-410 C170,-406 186,-396 192,-380" stroke="#c8c8d0" stroke-width="4" fill="none" opacity="0.6"/>'
    s += (f'<path d="M-70,-680 C-90,-760 -96,-850 -80,-930 C-60,-990 30,-1006 80,-984 C120,-960 126,-880 116,-800 '
          f'C108,-740 96,-700 80,-676 Z" fill="{cloth}"/>')
    s += '<path d="M-10,-990 C10,-940 20,-860 18,-760" stroke="#000" stroke-width="10" fill="none" opacity="0.5"/>'
    for i in range(5):
        s += f'<circle cx="{30+i*4}" cy="{-955+i*45}" r="6" fill="#c8ccd4" opacity="0.7"/>'
    s += '<path d="M-84,-940 C-40,-990 60,-1000 100,-972 C80,-900 30,-830 -40,-780 C-70,-820 -86,-880 -84,-940 Z" fill="#5a1a14"/>'
    for i in range(6):
        s += f'<path d="M{-80+i*30},{-950-i*6} L{-50+i*16},{-800+i*4}" stroke="#d8a040" stroke-width="5" opacity="0.55"/>'
    s += '<ellipse cx="20" cy="-994" rx="62" ry="20" fill="#010102"/>'
    s += f'<path d="M-42,-994 C-30,-1012 70,-1014 82,-994" stroke="{cloth}" stroke-width="14" fill="none"/>'
    s += '<path d="M-40,-986 C-10,-960 50,-960 80,-986 L40,-940 Z" fill="#6a1a14"/>'
    s += f'<path d="M60,-960 C120,-920 160,-860 176,-790 L184,-748 L150,-740 C140,-800 110,-860 50,-900 Z" fill="{cloth}"/>'
    s += '<path d="M-30,-950 C10,-880 80,-810 150,-760 L160,-736 L130,-730 C70,-780 0,-840 -50,-900 Z" fill="#100c08"/>'
    s += '<ellipse cx="170" cy="-740" rx="30" ry="22" fill="#1a120c"/><ellipse cx="146" cy="-736" rx="26" ry="20" fill="#140e08"/>'
    for i in range(4):
        s += f'<path d="M{132+i*10},{-764+i*3} C{150+i*10},{-722+i*3} {176+i*10},{-722+i*3} {196+i*6},{-758+i*3}" stroke="{RAW}" stroke-width="5" fill="none" opacity="0.85"/>'
    s += f'<path d="M178,-712 C186,-680 196,-660 206,-630" stroke="{RAW}" stroke-width="6" fill="none"/>'
    s += '<g transform="translate(232,-560) rotate(-12)">'
    s += '<ellipse cx="0" cy="0" rx="120" ry="34" fill="#0c0a08"/><path d="M-56,-4 C-60,-70 -40,-104 0,-108 C40,-104 60,-70 56,-4 Z" fill="#14100a"/>'
    s += '<path d="M-56,-24 C-20,-34 20,-34 56,-24 L56,-6 C20,-14 -20,-14 -56,-6 Z" fill="#6a5030"/>'
    s += f'<path d="M-120,0 C-80,30 80,30 120,0" stroke="{rim}" stroke-width="4" fill="none" opacity="0.6"/>'
    s += '<path d="M-96,22 C-40,70 40,72 96,22 L60,60 C20,86 -20,86 -60,60 Z" fill="#020203" opacity="0.95"/>'
    s += '</g>'
    s += f'<path d="M206,-630 C214,-610 222,-600 228,-596" stroke="{RAW}" stroke-width="6" fill="none"/>'
    s += f'<path d="M-70,-680 C-90,-760 -96,-850 -84,-940 C-40,-990 30,-1006 80,-994" stroke="{rim}" stroke-width="6" fill="none" opacity="0.75" filter="url(#blur1)"/>'
    return s


def horse_rider(x, y, k=1.0, pose="gallop", rim=MOONRIM, ghost=False, flip=False, col="#06070b", headless=True, seed=3):
    body = mustang(pose, col, rim, seed) + (rider(rim=rim) if headless else "")
    rimc = f'<g filter="url(#blur1)" opacity="0.85"><g transform="translate(-7,-6)">{_flat(body, rim)}</g></g>'
    frag = rimc + body
    if ghost:
        frag = f'<g opacity="0.75" filter="url(#ghost)">{_flat(body, "#a8c4e8")}</g><g opacity="0.35">{body}</g>'
    sx = -k if flip else k
    return f'<g transform="translate({x},{y}) scale({sx},{k})">{frag}</g>'


# ============================================================ the brush country (mezquites, nopales)
def mesquite(x, yb, h, seed=1, col="#04060a", rim=None):
    r = random.Random(seed); out = []
    def br(x0, y0, ang, ln, w, d):
        a = math.radians(ang)
        x1 = x0 + math.sin(a) * ln; y1 = y0 - math.cos(a) * ln
        mx = (x0 + x1) / 2 + r.uniform(-ln, ln) * 0.25; my = (y0 + y1) / 2 + r.uniform(-ln, ln) * 0.15
        out.append(f'<path d="M{x0:.0f},{y0:.0f} Q{mx:.0f},{my:.0f} {x1:.0f},{y1:.0f}" stroke="{col}" stroke-width="{w:.1f}" fill="none" stroke-linecap="round"/>')
        if rim and w > 4 and r.random() < 0.6:
            out.append(f'<path d="M{x0+w*0.4:.0f},{y0:.0f} Q{mx+w*0.4:.0f},{my:.0f} {x1+w*0.3:.0f},{y1:.0f}" stroke="{rim}" stroke-width="{max(1.5,w*0.12):.1f}" fill="none" opacity="0.45"/>')
        if d < 5:
            for _ in range(2 if d < 2 else r.choice([1, 2, 2, 3])):
                br(x1, y1, ang + r.uniform(-48, 48), ln * r.uniform(0.6, 0.8), w * 0.62, d + 1)
        else:
            for _ in range(5):
                lx = x1 + r.uniform(-50, 50) * h / 600; ly = y1 + r.uniform(-25, 25) * h / 600
                out.append(f'<ellipse cx="{lx:.0f}" cy="{ly:.0f}" rx="{r.uniform(26,50)*h/600:.0f}" ry="{r.uniform(8,16)*h/600:.0f}" fill="{col}" opacity="0.92" transform="rotate({r.uniform(-25,25):.0f} {lx:.0f} {ly:.0f})"/>')
    br(x, yb, r.uniform(-12, 12), h * 0.34, h * 0.07, 0)
    return "".join(out)


def nopal(x, yb, k=1.0, seed=1, col="#05080a", rim=None):
    r = random.Random(seed); s = ""
    out = [(x, yb - 60 * k, 0, 1.0)]
    for i in range(r.randint(5, 9)):
        px, py, ang, sc = r.choice(out)
        na = ang + r.uniform(-50, 50); ns = sc * r.uniform(0.8, 0.95)
        nx = px + math.sin(math.radians(na)) * 95 * k * sc; ny = py - math.cos(math.radians(na)) * 95 * k * sc
        out.append((nx, ny, na, ns))
    for (px, py, ang, sc) in out:
        rx, ry = 48 * k * sc, 66 * k * sc
        s += f'<ellipse cx="{px:.0f}" cy="{py:.0f}" rx="{rx:.0f}" ry="{ry:.0f}" fill="{col}" transform="rotate({ang:.0f} {px:.0f} {py:.0f})"/>'
        if rim:
            s += f'<path d="M{px+rx*0.3:.0f},{py-ry*0.95:.0f} A{rx:.0f},{ry:.0f} 0 0 1 {px+rx:.0f},{py:.0f}" stroke="{rim}" stroke-width="{3*k:.1f}" fill="none" opacity="0.55" transform="rotate({ang:.0f} {px:.0f} {py:.0f})"/>'
        for _ in range(6):
            dx, dy = r.uniform(-rx * 0.6, rx * 0.6), r.uniform(-ry * 0.6, ry * 0.6)
            s += f'<circle cx="{px+dx:.0f}" cy="{py+dy:.0f}" r="{2*k:.1f}" fill="{rim or "#2a3a40"}" opacity="0.5"/>'
    return s


def grass(x0, x1, y, seed, col="#04060a", n=140, hmin=20, hmax=70, rim=None):
    r = random.Random(seed); s = ""
    for _ in range(n):
        x = r.uniform(x0, x1); h = r.uniform(hmin, hmax); b = r.uniform(-20, 20)
        s += f'<path d="M{x:.0f},{y:.0f} q{b*0.3:.0f},{-h*0.6:.0f} {b:.0f},{-h:.0f}" stroke="{col}" stroke-width="3" fill="none"/>'
        if rim and r.random() < 0.3:
            s += f'<path d="M{x+1:.0f},{y:.0f} q{b*0.3:.0f},{-h*0.6:.0f} {b:.0f},{-h:.0f}" stroke="{rim}" stroke-width="1.5" fill="none" opacity="0.4"/>'
    return s


MOODS = {
    "night": dict(sky=("#03070f", "#18304a", "#0c1c30"), far="#0c1828", ground="#0a1018", near="#030508", rim=MOONRIM, road="#1a2028"),
    "red":   dict(sky=("#0a0204", "#4a0e10", "#200608"), far="#1a0608", ground="#120406", near="#040102", rim="#ff6a50", road="#2a1012"),
    "dawn":  dict(sky=("#1a2238", "#d89a70", "#6a5a74"), far="#3a3448", ground="#2a2430", near="#0a080c", rim="#ffc890", road="#5a4a48"),
    "dusk":  dict(sky=("#141a30", "#c8704a", "#5a3a50"), far="#2a2234", ground="#1c1620", near="#060406", rim="#ff9a60", road="#3a2a2a"),
    "fog":   dict(sky=("#0a1018", "#3a4a5a", "#1a2a3a"), far="#1a2634", ground="#121a24", near="#04070a", rim="#b8cce0", road="#2a3440"),
}


def brush_svg(mood="night", seed=1, moon_xy=(1750, 260), horizon=860, road=False, trees=True, mr=95):
    m = MOODS[mood]; r = random.Random(seed)
    s = sky(*m["sky"])
    if mood in ("night", "fog", "red"):
        s += stars(170 if mood == "night" else 60, seed, horizon - 100)
        if moon_xy:
            s += moon(moon_xy[0], moon_xy[1], mr) if mood != "red" else (f'<circle cx="{moon_xy[0]}" cy="{moon_xy[1]}" r="{mr}" fill="#e05a40"/>' + glow(moon_xy[0], moon_xy[1], 500, "red", 0.6))
        s += clouds(7, 120, horizon - 300, seed + 3, "#24344a" if mood != "red" else "#3a0a0a", (0.2, 0.45))
    else:
        s += glow(1500, horizon, 1000, "warm", 0.55)
    s += ridge(horizon, 22, m["far"], seed + 1, step=40)
    s += f'<rect y="{horizon}" width="2400" height="{1350-horizon}" fill="{m["ground"]}"/>'
    s += f'<rect y="{horizon}" width="2400" height="{1350-horizon}" fill="#000" opacity="0.35" filter="url(#paper)"/>'
    for i in range(40):
        x = r.uniform(0, 2400)
        s += f'<ellipse cx="{x:.0f}" cy="{horizon+r.uniform(2,30):.0f}" rx="{r.uniform(20,70):.0f}" ry="{r.uniform(8,20):.0f}" fill="{m["far"]}" opacity="0.9"/>'
    if road:
        s += f'<path d="M1150,{horizon} L1250,{horizon} L1900,1350 L500,1350 Z" fill="{m["road"]}" opacity="0.8"/>'
        for off in (-0.4, 0.4):
            s += f'<path d="M{1200+off*40:.0f},{horizon} L{1200+off*1100:.0f},1350" stroke="#000" stroke-width="30" opacity="0.25" filter="url(#blur2)"/>'
    if trees:
        for i in range(6):
            x = r.uniform(100, 2300); y = horizon + r.uniform(20, 90)
            s += mesquite(x, y, r.uniform(150, 260), seed + 10 + i, m["far"])
        s += mesquite(260, 1380, 1100, seed + 30, m["near"], m["rim"]) + mesquite(2200, 1380, 900, seed + 31, m["near"], m["rim"])
        s += nopal(560, 1350, 1.6, seed + 40, m["near"], m["rim"]) + nopal(1900, 1360, 1.3, seed + 41, m["near"], m["rim"])
        s += nopal(820, horizon + 180, 0.6, seed + 42, m["near"], m["rim"]) + nopal(1640, horizon + 160, 0.55, seed + 43, m["near"], m["rim"])
    s += stones(300, 2100, horizon + 80, 1340, seed + 5, 40, "#1a1c20", m["rim"])
    s += grass(0, 2400, 1350, seed + 6, m["near"], 220, 30, 110, m["rim"])
    if mood != "dawn":
        s += fogb(horizon + 120, 0.22 if mood != "fog" else 0.4, seed + 9)
    return s


# ============================================================ backgrounds
@art
def brush_night(): return S(brush_svg("night", 1))
@art
def brush_night2(): return S(brush_svg("night", 7, (600, 230)))
@art
def brush_night3(): return S(brush_svg("night", 13, (1250, 200), mr=140, horizon=900))
@art
def brush_fog(): return S(brush_svg("fog", 9, (1500, 280)))
@art
def brush_dawn(): return S(brush_svg("dawn", 4, None))
@art
def brush_dusk(): return S(brush_svg("dusk", 5, None))
@art
def brush_red(): return S(brush_svg("red", 11, (1700, 300), mr=120))
@art
def road_night(): return S(brush_svg("night", 21, (1500, 240), road=True))
@art
def road_dawn(): return S(brush_svg("dawn", 22, None, road=True))


@art
def rider_moon():
    s = sky("#02050c", "#14283e", "#081626") + stars(160, 3, 700)
    s += '<circle cx="1250" cy="620" r="430" fill="#e8eef4"/>' + glow(1250, 620, 900, "moon", 0.7)
    s += '<g opacity="0.25">' + "".join(f'<circle cx="{1250+dx}" cy="{620+dy}" r="{rr}" fill="#9aa8b8"/>' for dx, dy, rr in ((-120, -80, 70), (90, 60, 50), (160, -150, 40), (-60, 160, 60))) + '</g>'
    s += ridge(1000, 30, "#05080e", 3, step=40) + '<rect y="1000" width="2400" height="350" fill="#030509"/>'
    s += mesquite(380, 1380, 1050, 5, "#020305") + nopal(2050, 1350, 1.4, 8, "#020305")
    s += horse_rider(1150, 1030, 0.62, "gallop", rim="#ffffff", col="#010203")
    return S(s, fogb(1060, 0.25, 7))


@art
def l_rider(): return S(horse_rider(1200, 1150, 0.55, "gallop"))
@art
def l_rider_far(): return S(horse_rider(1200, 920, 0.2, "gallop", rim="#d8e4f0"))
@art
def l_rider_ghost(): return S(horse_rider(1200, 1150, 0.55, "gallop", ghost=True))


@art
def rider_close():
    s = sky("#03060c", "#1a2c44", "#0a1626") + glow(1500, 300, 900, "moon", 0.75) + moon(1560, 300, 120)
    s += clouds(8, 200, 700, 9, "#2a3a52", (0.2, 0.4))
    s += horse_rider(820, 2050, 1.55, "walk", rim="#dfe8f4")
    return S(s, fogb(1300, 0.3, 3))
@art
def rider_close_red():
    s = '<rect width="2400" height="1350" fill="#0c0204"/>' + glow(1500, 300, 1000, "red", 0.7)
    s += horse_rider(820, 2050, 1.55, "walk", rim="#ff6a50", col="#080102")
    return S(s)
@art
def rider_front():
    s = brush_svg("fog", 31, (1200, 300), road=True)
    s += horse_rider(1200, 1250, 0.95, "gallop", rim="#cfe0f0")
    return S(s, fogb(1180, 0.45, 12), dim(0.1))
@art
def sombrero_horn():
    s = '<rect width="2400" height="1350" fill="#04070c"/>' + glow(1700, 250, 1100, "moon", 0.55)
    s += f'<g transform="translate(250,2150) scale(2.3)">{mustang("walk", "#06070b", MOONRIM)}{rider(rim="#dfe8f4")}</g>'
    return S(s, dim(0.1))
@art
def hands_tied():
    s = '<rect width="2400" height="1350" fill="#05060a"/>' + glow(1500, 300, 1100, "moon", 0.5)
    s += '<path d="M0,1350 C300,1100 900,960 2400,1000 L2400,1350 Z" fill="#24140a"/>'
    s += '<rect x="1100" y="560" width="200" height="520" rx="50" fill="#2a160a"/><ellipse cx="1200" cy="560" rx="200" ry="70" fill="#3a2010"/>'
    s += '<ellipse cx="1200" cy="550" rx="170" ry="52" fill="#5a3418" opacity="0.6"/>'
    for (cx, cy, rot, fl) in ((960, 760, -20, 1), (1440, 770, 20, -1)):
        s += f'<g transform="translate({cx},{cy}) rotate({rot}) scale({fl},1)"><path d="M-160,-90 C-60,-130 120,-120 170,-50 C190,10 160,90 80,110 C-20,130 -140,100 -180,40 Z" fill="#120c08"/>'
        s += '<path d="M-180,40 C-260,60 -400,90 -700,100 L-700,-60 C-420,-80 -260,-100 -160,-90 Z" fill="#0e0a10"/>'
        s += '<path d="M-160,-90 C-60,-130 120,-120 170,-50" stroke="#9fc2e8" stroke-width="4" fill="none" opacity="0.5"/></g>'
    for i in range(7):
        s += f'<path d="M{880+i*22},{640+i*6} C{1000+i*10},{900+i*6} {1400-i*10},{900+i*6} {1520-i*22},{650+i*6}" stroke="{RAW}" stroke-width="12" fill="none" opacity="0.9"/>'
        s += f'<path d="M{880+i*22},{636+i*6} C{1000+i*10},{896+i*6} {1400-i*10},{896+i*6} {1520-i*22},{646+i*6}" stroke="#e0c090" stroke-width="3" fill="none" opacity="0.5"/>'
    return S(s, dim(0.15))
@art
def hooves_dust():
    s = brush_svg("night", 41, None, horizon=500, trees=False)
    s += f'<g transform="translate(900,1700) scale(1.6)">{mustang("gallop", "#05060a", MOONRIM)}</g>'
    s += clouds(20, 1150, 1350, 8, "#8a98a8", (0.15, 0.35), (200, 500), (40, 90))
    return S(s)
@art
def mane_close():
    s = sky("#03060c", "#1a2a40") + glow(1700, 300, 900, "moon", 0.6)
    s += f'<g transform="translate(-300,2500) scale(2.8)">{mustang("gallop", "#05060a", MOONRIM, 9)}</g>'
    return S(s)


# ------------------------------------------------------------ history: map, rancho, border
@art
def map_nueces():
    s = '<rect width="2400" height="1350" fill="#c8b48a"/><rect width="2400" height="1350" fill="#6a4a2a" opacity="0.35" filter="url(#paper)"/>'
    s += glow(1200, 675, 1400, "warm", 0.3)
    s += '<path d="M2400,700 C2300,760 2250,900 2240,1350" stroke="#5a7a8a" stroke-width="12" fill="none"/>'
    nueces = "M350,180 C600,260 800,360 1000,420 C1250,500 1600,560 2000,620 L2280,640"
    bravo = "M150,560 C450,640 700,760 900,920 C1150,1110 1600,1220 2000,1260 L2260,1280"
    s += f'<path d="{nueces} L2260,1280 C1600,1220 1150,1110 900,920 C700,760 450,640 150,560 Z" fill="#a82a1a" opacity="0.18"/>'
    s += f'<path d="{nueces}" stroke="#2a5a7a" stroke-width="14" fill="none"/><path d="{bravo}" stroke="#2a5a7a" stroke-width="18" fill="none"/>'
    s += '<text x="1150" y="400" font-family="IM FELL English" font-size="64" fill="#2a1a10" transform="rotate(12 1150 400)">Río Nueces</text>'
    s += '<text x="950" y="1050" font-family="IM FELL English" font-size="72" fill="#2a1a10" transform="rotate(24 950 1050)">Río Bravo</text>'
    s += '<text x="1180" y="790" font-family="Cinzel" font-size="56" fill="#6a1a10" opacity="0.85" transform="rotate(14 1180 790)">TIERRA DE NADIE</text>'
    for (x, y, n) in ((1460, 470, "San Antonio"), (1900, 1150, "Matamoros"), (700, 830, "Laredo")):
        s += f'<circle cx="{x}" cy="{y}" r="12" fill="#2a1a10"/><text x="{x+22}" y="{y+12}" font-family="IM FELL English" font-size="44" fill="#2a1a10">{n}</text>'
    s += '<rect x="40" y="40" width="2320" height="1270" fill="none" stroke="#4a3018" stroke-width="10"/>'
    return S(s, dim(0.12, "#1a0e04"))


def jacal(x, yb, k=1.0, lit=True, rim=MOONRIM):
    s = f'<g transform="translate({x},{yb}) scale({k})">'
    s += '<rect x="-200" y="-200" width="400" height="200" fill="#2a2018"/>'
    for i in range(18):
        s += f'<path d="M{-196+i*23},-200 L{-196+i*23},0" stroke="#1a140e" stroke-width="6"/>'
    s += '<path d="M-250,-190 L0,-330 L250,-190 Z" fill="#3a2e1c"/><path d="M-250,-190 L0,-330 L250,-190" stroke="#5a4a2a" stroke-width="10" fill="none"/>'
    s += f'<path d="M0,-330 L250,-190" stroke="{rim}" stroke-width="4" opacity="0.5"/>'
    s += f'<rect x="-50" y="-140" width="90" height="140" fill="{"#ffb050" if lit else "#050404"}"/>'
    if lit: s += glow(0, -60, 220, "warm", 0.6)
    return s + '</g>'


def corral(x0, x1, yb, col="#120c08", rim=None):
    s = ""
    for x in range(int(x0), int(x1), 70):
        s += f'<rect x="{x}" y="{yb-130}" width="14" height="140" fill="{col}"/>'
    for yy in (yb - 110, yb - 60):
        s += f'<path d="M{x0},{yy} L{x1},{yy+6}" stroke="{col}" stroke-width="12"/>'
        if rim: s += f'<path d="M{x0},{yy-5} L{x1},{yy+1}" stroke="{rim}" stroke-width="2.5" opacity="0.4"/>'
    return s


def small_horse(x, y, k, col="#05060a", rim=MOONRIM, pose="stand", flip=False, seed=1):
    return f'<g transform="translate({x},{y}) scale({-k if flip else k},{k})">{mustang(pose, col, rim, seed)}</g>'


@art
def rancho_night():
    s = brush_svg("night", 51, (1900, 240), trees=False)
    s += mesquite(1700, 1060, 600, 52, "#04060a", MOONRIM) + jacal(900, 1050, 1.2) + corral(1250, 2100, 1080, rim=MOONRIM)
    for i in range(4):
        s += small_horse(1400 + i * 190, 1085, 0.22, flip=i % 2 == 0, seed=60 + i, pose="stand" if i % 2 else "walk")
    s += nopal(300, 1350, 1.5, 53, "#030508", MOONRIM)
    return S(s, fogb(1100, 0.2, 5))
@art
def rancho_dusk():
    s = brush_svg("dusk", 54, None, trees=False)
    s += mesquite(500, 1080, 650, 55, "#060406", "#ff9a60") + jacal(1300, 1060, 1.1, rim="#ff9a60") + corral(1600, 2300, 1090, rim="#ff9a60")
    for i, x in enumerate((700, 860, 1000)):
        s += place(man_full(hat=True, cape=False, rim="#ff9a60"), x, 1140, 0.32 + i * 0.01)
    return S(s)
@art
def mustangs_run():
    s = brush_svg("dawn", 61, None, trees=False)
    r = random.Random(4)
    for i in range(9):
        x = 200 + i * 240 + r.uniform(-60, 60); y = 1000 + r.uniform(0, 260); k = 0.18 + (y - 1000) / 1200
        s += small_horse(x, y, k, "#120a08", "#ffc890", "gallop", seed=10 + i)
    s += clouds(18, 1100, 1350, 6, "#e0b890", (0.15, 0.3), (200, 500), (30, 80))
    return S(s)
@art
def rio_bravo():
    s = sky("#03070f", "#18304a", "#0c1c30") + stars(150, 6, 600) + moon(1600, 250, 90)
    s += ridge(700, 30, "#0c1828", 5, step=40) + '<rect y="700" width="2400" height="140" fill="#0a1018"/>'
    s += water(820, 1350, "#16303f", "#02060a") + refl(1600, 825, 1350, "#dfe8f2", 180, 5)
    s += '<path d="M0,820 C600,800 1500,840 2400,815" stroke="#a8c8e0" stroke-width="3" opacity="0.35" fill="none"/>'
    s += mesquite(250, 900, 700, 71, "#020406", MOONRIM)
    s += grass(0, 900, 1000, 72, "#020406", 120, 30, 120, MOONRIM)
    return S(s, fogb(860, 0.3, 8))
@art
def treaty():
    s = '<rect width="2400" height="1350" fill="#0c0806"/>' + glow(800, 500, 1000, "warm", 0.5)
    s += '<path d="M0,900 L2400,860 L2400,1350 L0,1350 Z" fill="#2a1a10"/>'
    s += '<g transform="translate(1200,700) rotate(-4)"><rect x="-520" y="-520" width="1040" height="1160" fill="#d8c8a0"/>'
    s += '<rect x="-520" y="-520" width="1040" height="1160" fill="#6a4a2a" opacity="0.3" filter="url(#paper)"/>'
    s += '<text x="0" y="-400" text-anchor="middle" font-family="IM FELL English" font-size="54" fill="#2a1a10">Tratado de Paz, Amistad y Límites</text>'
    s += '<text x="0" y="-330" text-anchor="middle" font-family="IM FELL English" font-size="44" fill="#2a1a10">Guadalupe Hidalgo, 1848</text>'
    for i in range(16):
        w = 820 if i % 5 != 4 else 520
        s += f'<path d="M-410,{-250+i*44} L{-410+w},{-250+i*44}" stroke="#4a3a2a" stroke-width="5" stroke-dasharray="{14+i%3*6} 8" opacity="0.7"/>'
    s += '<circle cx="300" cy="520" r="70" fill="#8a1a14"/><path d="M-400,540 C-320,500 -240,580 -160,520" stroke="#1a1010" stroke-width="5" fill="none"/></g>'
    s += candle_at(2050, 900, 220)
    return S(s)


# ------------------------------------------------------------ characters
def vidal(look=0.0, lids=0.35, rim=WARM, cold=False):
    from chars import bust_frame
    from base_chars import uid
    body = AG.soldier_body(uid("vd"), rim, ("#140c06", "#2e1c10", "#4a3018"), False, AG.SK_SOL, open_collar=True)
    return bust_frame(body, AG.soldier_head(rim=rim, cap=False, look=look, lids=lids, cold=cold), 1200, 560, 1.75) + SB.hat(1200, 400, 1.0, rim=rim, emb="#b8a070")


@art
def vidal_portrait(): return S(portrait_bg("candle"), vidal(-0.15, rim="#ffb860"))
@art
def vidal_smile(): return S(portrait_bg("candle"), vidal(0.3, 0.5, "#ffb860"), candle_at(2000, 1300, 180))
@art
def vidal_night(): return S(portrait_bg("moon"), vidal(-0.4, 0.4, MOONRIM), dim(0.15))
@art
def vidal_cold(): return S(portrait_bg("red"), vidal(0.0, 0.6, "#ff7050", cold=True), dim(0.2, "#200"))


def ranger_hat(cx, cy, k=1.0, rim=WARM, col="#2a2018"):
    s = f'<g transform="translate({cx},{cy}) scale({k})">'
    s += f'<path d="M-90,-10 C-96,-80 -80,-150 -40,-170 C-10,-150 10,-150 40,-170 C80,-150 96,-80 90,-10 Z" fill="{col}"/>'
    s += '<path d="M-90,-20 L90,-20 L90,-46 L-90,-46 Z" fill="#100c08"/>'
    s += f'<path d="M-230,0 C-150,-40 150,-40 230,0 C200,24 -200,24 -230,0 Z" fill="{col}"/>'
    s += f'<path d="M-230,0 C-150,-40 150,-40 230,0" stroke="{rim}" stroke-width="4" fill="none" opacity="0.6"/>'
    s += f'<path d="M-90,-10 C-96,-80 -80,-150 -40,-170" stroke="{rim}" stroke-width="4" fill="none" opacity="0.5"/>'
    return s + '</g>'


def beard(cx, cy, k, col="#2a1a10", seed=2):
    r = random.Random(seed); s = f'<g transform="translate({cx},{cy}) scale({k})">'
    s += f'<path d="M-70,-20 C-70,60 -40,110 0,118 C40,110 70,60 70,-20 C50,20 20,30 0,30 C-20,30 -50,20 -70,-20 Z" fill="{col}"/>'
    for _ in range(40):
        x = r.uniform(-60, 60); y = r.uniform(0, 100)
        s += f'<path d="M{x:.0f},{y:.0f} l{r.uniform(-4,4):.0f},14" stroke="#5a4030" stroke-width="2" opacity="0.6"/>'
    return s + '</g>'


@art
def taylor_portrait():
    return S(portrait_bg("candle"), luis_bust(1200, 560, 1.75, rim="#ffb860", look=-0.25, smile=0.05, lids=0.35),
             beard(1200, 585, 1.75), ranger_hat(1200, 360, 1.15, "#ffb860"))
@art
def taylor_night():
    return S(portrait_bg("moon"), luis_bust(1200, 560, 1.75, rim=MOONRIM, look=0.35, smile=-0.2, lids=0.4),
             beard(1200, 585, 1.75), ranger_hat(1200, 360, 1.15, MOONRIM), dim(0.15))
@art
def wallace_portrait():
    return S(portrait_bg("candle"), father_bust(1200, 600, 1.9, rim="#ffb860"), beard(1200, 640, 2.2, "#3a2a1c", 5),
             ranger_hat(1200, 380, 1.3, "#ffb860", "#3a2c1c"))
@art
def wallace_red():
    return S(portrait_bg("red"), father_bust(1200, 600, 1.9, red=True), beard(1200, 640, 2.2, "#1a0806", 5),
             ranger_hat(1200, 380, 1.3, "#ff6040", "#1a0806"), dim(0.12, "#300"))


# ------------------------------------------------------------ the theft, the chase, the camp
@art
def comanche_moon():
    s = brush_svg("night", 81, (1300, 220), mr=150, trees=False)
    for x in (400, 900, 1700, 2100):
        s += glow(x, 870, 120, "warm", 0.8) + f'<path d="M{x},860 C{x-30},700 {x+40},600 {x},420" stroke="#8a9aaa" stroke-width="30" opacity="0.15" fill="none" filter="url(#blur3)"/>'
    return S(s)
@art
def corral_empty():
    s = brush_svg("dawn", 82, None, trees=False)
    s += corral(400, 2000, 1150, "#1a120c", "#ffc890")
    s += '<path d="M1150,1040 L1260,1160" stroke="#1a120c" stroke-width="14"/>'
    for i in range(14):
        s += hoof_print(700 + i * 110, 1250 + math.sin(i) * 40, 0.9, "#1a1418")
    return S(s)
@art
def tracks():
    s = '<rect width="2400" height="1350" fill="#3a3436"/>' + glow(1900, 0, 1300, "moon", 0.35)
    s += '<rect width="2400" height="1350" fill="#1a1618" opacity="0.5" filter="url(#paper)"/>'
    for row in range(3):
        for i in range(10):
            s += hoof_print(150 + i * 230 + row * 60, 500 + row * 260 + math.sin(i + row) * 50, 1.5, "#0c0a0c")
    s += stones(0, 2400, 300, 1350, 3, 40, "#2a2628", MOONRIM)
    return S(s, dim(0.2))
@art
def riders_chase():
    s = brush_svg("night", 91, (600, 240))
    for i, (x, y, k) in enumerate(((900, 1180, 0.3), (1250, 1150, 0.27), (1580, 1170, 0.29))):
        s += small_horse(x, y, k, seed=90 + i, pose="gallop")
        s += place(man_full(hat=True, cape=False, rim=MOONRIM), x + 30 * k / 0.3, y - 620 * k, 0.42 * k / 0.3)
    return S(s)


def campfire(x, yb, k=1.0, hot=1.0):
    s = f'<g transform="translate({x},{yb}) scale({k})">'
    s += '<path d="M-90,0 L90,-30 M-90,-30 L90,0" stroke="#1a0e08" stroke-width="22"/>'
    if hot > 0:
        s += f'<path d="M-50,-10 C-60,-80 -10,-120 0,-200 C20,-120 70,-90 50,-10 Z" fill="#ff9a30" opacity="{hot:.2f}"/>'
        s += f'<path d="M-24,-10 C-30,-60 0,-90 6,-130 C20,-80 40,-60 26,-10 Z" fill="#ffe08a" opacity="{hot:.2f}"/>'
    else:
        for i in range(8):
            s += f'<circle cx="{-50+i*14}" cy="{-8-(i%3)*6}" r="7" fill="#ff5a20" opacity="0.7"/>'
    return s + '</g>' + glow(x, yb - 60 * k, 420 * k * (0.5 + hot), "warm", 0.7 if hot else 0.35)


def sleeper(x, yb, k=1.0, rim=WARM):
    s = f'<g transform="translate({x},{yb}) scale({k})">'
    s += '<path d="M-220,0 C-230,-40 -180,-80 -60,-84 C60,-90 180,-70 230,-30 L230,0 Z" fill="#2a1a14"/>'
    s += '<path d="M-220,0 C-230,-40 -180,-80 -60,-84" stroke="#6a2a1a" stroke-width="10" fill="none"/>'
    s += f'<ellipse cx="-200" cy="-50" rx="70" ry="22" fill="#0c0806"/><path d="M-260,-40 C-200,-70 -140,-70 -120,-40" stroke="{rim}" stroke-width="4" fill="none" opacity="0.5"/>'
    return s + '</g>'


@art
def camp_night():
    s = brush_svg("night", 101, (1900, 220), horizon=820)
    s += campfire(1200, 1130, 1.1, 0.5)
    s += sleeper(800, 1180, 0.9) + sleeper(1600, 1200, 0.95) + sleeper(1250, 1300, 1.0)
    for i in range(3):
        s += small_horse(300 + i * 180, 1040, 0.16, seed=110 + i)
    return S(s)
@art
def camp_embers():
    s = brush_svg("night", 102, (500, 230), horizon=820, trees=True)
    s += campfire(1200, 1150, 1.4, 0.0)
    s += sleeper(1250, 1320, 1.1)
    return S(s, dim(0.25))
@art
def camp_shadows():
    s = brush_svg("night", 103, (1800, 200), horizon=820)
    s += campfire(1600, 1140, 0.9, 0.4)
    for i, x in enumerate((420, 700, 980)):
        s += place(man_full(hat=True, cape=False, rim=MOONRIM, walk=0.3 + i * 0.1), x, 1300, 0.62 - i * 0.06)
    return S(s, dim(0.15))
@art
def muzzle_flash():
    s = brush_svg("night", 104, None, horizon=820, trees=True) + dim(0.5, "#000")
    for (x, y) in ((600, 900), (1300, 860), (1900, 920)):
        s += glow(x, y, 300, "white", 0.9) + f'<circle cx="{x}" cy="{y}" r="30" fill="#ffffff"/>'
    return S(s)
@art
def wallace_shadow():
    s = '<rect width="2400" height="1350" fill="#0a0604"/>' + glow(1200, 1200, 1200, "warm", 0.6)
    s += campfire(1200, 1350, 2.2, 0.6)
    s += place(man_full(hat=True, cape=False, rim="#ff9a40"), 1250, 1450, 1.35)
    return S(s, dim(0.1))
@art
def mustang_wild():
    s = brush_svg("night", 111, (1700, 260), trees=False)
    body = mustang("rear", "#05060a", MOONRIM, 12)
    s += f'<g filter="url(#blur1)" transform="translate(1194,1214) rotate(-24) scale(0.75)">{_flat(body, MOONRIM)}</g>'
    s += f'<g transform="translate(1200,1220) rotate(-24) scale(0.75)">{body}</g>'
    return S(s, clouds(12, 1150, 1350, 4, "#8a98a8", (0.15, 0.3), (200, 500), (30, 80)))
@art
def release_dark():
    s = brush_svg("night", 112, (600, 220))
    s += horse_rider(1700, 1060, 0.26, "gallop")
    return S(s, fogb(1060, 0.35, 9), dim(0.15))


# ------------------------------------------------------------ the sightings
@art
def vaqueros_fire():
    s = brush_svg("night", 121, (1900, 230), horizon=820)
    s += campfire(1000, 1160, 1.0, 1.0)
    for x, k in ((760, 0.5), (1260, 0.52)):
        s += place(man_full(hat=True, cape=False, rim="#ffb060"), x, 1240, k)
    s += place(man_full(hat=True, cape=False, rim="#ffb060"), 1700, 1260, 0.55, flip=True)
    return S(s)
@art
def vaqueros_shoot():
    s = brush_svg("night", 122, (500, 220), horizon=820)
    s += place(man_full(hat=True, cape=False, rim=MOONRIM), 600, 1350, 0.9)
    s += '<path d="M680,700 L1000,640" stroke="#0a0806" stroke-width="18"/>' + glow(1010, 636, 160, "white", 0.9)
    s += horse_rider(1750, 1000, 0.22, "gallop", rim="#e0ecf8")
    return S(s)


def fort_wall():
    s = '<rect x="0" y="760" width="2400" height="300" fill="#3a3030"/><rect x="0" y="760" width="2400" height="300" fill="#000" opacity="0.4" filter="url(#plaster)"/>'
    for x in range(0, 2400, 120):
        s += f'<rect x="{x}" y="730" width="70" height="40" fill="#3a3030"/>'
    s += f'<path d="M0,760 L2400,760" stroke="{MOONRIM}" stroke-width="3" opacity="0.4"/>'
    return s


@art
def fort_inge():
    s = sky("#03070f", "#18304a", "#0c1c30") + stars(160, 8, 600) + moon(1800, 230, 90)
    s += fort_wall() + '<rect y="1060" width="2400" height="290" fill="#0a0c10"/>'
    s += '<rect x="1000" y="560" width="300" height="200" fill="#2a2424"/><rect x="1110" y="640" width="80" height="120" fill="#ffb050"/>' + glow(1150, 700, 220, "warm", 0.6)
    s += '<path d="M1150,560 L1150,380" stroke="#1a1414" stroke-width="10"/><path d="M1150,390 L1290,420 L1150,450 Z" fill="#3a3a4a"/>'
    for x in (500, 1600):
        s += place(man_full(hat=False, cape=False, rim=MOONRIM), x, 770, 0.24)
    s += horse_rider(1900, 1220, 0.2, "gallop", rim="#d8e4f0")
    return S(s, fogb(1150, 0.3, 4))
@art
def soldier_watch():
    return S(portrait_bg("moon"), AG.soldier_bust(1200, 560, 1.75, rim=MOONRIM, medals=False, cap=True, look=0.55, lids=0.1), dim(0.15))
@art
def waterhole_dawn():
    s = brush_svg("dawn", 131, None, horizon=820, trees=True)
    s += '<ellipse cx="1200" cy="1150" rx="700" ry="110" fill="#6a7088"/><ellipse cx="1200" cy="1150" rx="700" ry="110" fill="#e0a070" opacity="0.35"/>'
    s += horse_rider(1250, 1120, 0.42, "stand", rim="#ffc890", col="#120a08")
    for x in (500, 2000):
        s += place(man_full(hat=True, cape=False, rim="#ffc890"), x, 1250, 0.5, flip=x > 1200)
    return S(s)
@art
def grave_mesquite():
    s = brush_svg("dusk", 141, None, horizon=840, trees=False)
    s += mesquite(1500, 1100, 900, 142, "#060406", "#ff9a60")
    s += '<path d="M800,1150 C900,1080 1300,1080 1400,1150 Z" fill="#2a1e1a"/>'
    s += stones(820, 1380, 1090, 1150, 7, 24, "#3a302a", "#ff9a60")
    s += nopal(400, 1350, 1.3, 143, "#060406", "#ff9a60")
    return S(s)
@art
def grave_night():
    s = brush_svg("night", 144, (900, 230), horizon=840, trees=False)
    s += mesquite(1500, 1100, 900, 142, "#04060a", MOONRIM)
    s += '<path d="M800,1150 C900,1080 1300,1080 1400,1150 Z" fill="#141820"/>'
    s += stones(820, 1380, 1090, 1150, 7, 24, "#2a2e36", MOONRIM)
    return S(s, fogb(1120, 0.35, 6))
@art
def wagon_1917():
    s = brush_svg("night", 151, (1800, 230), road=True)
    s += small_horse(1080, 1230, 0.3, pose="walk", flip=True, seed=152)
    s += '<rect x="1130" y="1060" width="380" height="120" fill="#2a1a10"/><circle cx="1200" cy="1200" r="70" fill="none" stroke="#1a100a" stroke-width="16"/><circle cx="1440" cy="1200" r="70" fill="none" stroke="#1a100a" stroke-width="16"/>'
    s += place(man_full(hat=True, cape=False, rim=MOONRIM), 1240, 1080, 0.24) + place(woman_full(rebozo_head=True, rim=MOONRIM), 1360, 1080, 0.22)
    s += '<rect x="1520" y="1000" width="30" height="40" fill="#ffc060"/>' + glow(1535, 1020, 160, "warm", 0.7)
    return S(s)
@art
def car_1969():
    s = brush_svg("night", 161, (700, 220), road=True)
    s += '<path d="M1060,1000 L1340,1000 L1380,1060 L1020,1060 Z" fill="#0c0e12"/><path d="M1000,1060 L1400,1060 L1420,1130 L980,1130 Z" fill="#14161c"/>'
    for x in (1050, 1350):
        s += f'<circle cx="{x}" cy="1095" r="26" fill="#fff4d0"/>' + glow(x, 1095, 200, "white", 0.7)
    return S(s)
@art
def headless_hill():
    s = brush_svg("night", 171, (1600, 230), horizon=900, trees=False)
    s += '<path d="M0,1000 C500,700 1200,620 1700,760 C2000,840 2200,900 2400,920 L2400,1350 L0,1350 Z" fill="#060a10"/>'
    s += mesquite(800, 780, 420, 172, "#04060a", MOONRIM)
    s += horse_rider(1450, 735, 0.17, "walk", rim="#dfe8f4")
    return S(s, fogb(1000, 0.3, 3))
@art
def border_fire():
    s = sky("#03070f", "#18304a", "#0c1c30") + stars(150, 9, 600) + moon(700, 250, 80)
    s += ridge(760, 40, "#0c1828", 6, step=40) + water(820, 1350, "#16303f", "#02060a") + refl(700, 825, 1350, "#dfe8f2", 160, 5)
    s += campfire(1700, 800, 0.4, 1.0)
    for x in (1600, 1800):
        s += place(man_full(hat=True, cape=True, rim="#ffb060"), x, 810, 0.16)
    return S(s, fogb(860, 0.3, 4))


# ------------------------------------------------------------ misc
@art
def chronicle():
    return QM.ART["chronicle"]().replace("La Calle de la", "Memorias de un").replace("Quemada", "rinche de Texas")
@art
def title_bg():
    s = sky("#02040a", "#0e1c2e") + glow(1200, 600, 1100, "moon", 0.35)
    s += ridge(1080, 20, "#03050a", 5, step=40) + '<rect y="1080" width="2400" height="270" fill="#020306"/>'
    s += horse_rider(1200, 1090, 0.42, "stand", rim="#cfe0f0", col="#010203")
    return S(s, fogb(1100, 0.3, 5), dim(0.25))
@art
def red_flash():
    s = '<rect width="2400" height="1350" fill="#1a0000"/>' + glow(1200, 675, 1200, "red", 0.8)
    s += horse_rider(1100, 1300, 0.9, "rear", rim="#ff5030", col="#0a0000")
    return S(s)
@art
def rider_flash():
    s = '<rect width="2400" height="1350" fill="#02040a"/>' + glow(1200, 500, 1100, "moon", 0.6)
    s += horse_rider(900, 2200, 2.0, "walk", rim="#ffffff", col="#010203")
    return S(s)
@art
def dolls_tease():
    s = sky("#03070f", "#1a2c40", "#0c1a2a") + glow(1600, 300, 800, "moon", 0.5) + moon(1650, 280, 80)
    s += water(900, 1350, "#10242e", "#02060a") + refl(1650, 905, 1350, "#dfe8f2", 140, 4)
    s += '<path d="M1080,1000 L1100,600 L1140,600 L1130,1000 Z" fill="#05080a"/>'
    s += AG.canopy(1100, 500, 700, 320, seed=7, rim=MOONRIM, n=300, fruit=0)
    r = random.Random(5)
    for i in range(14):
        x = r.uniform(600, 1700); y = r.uniform(680, 900)
        s += f'<path d="M{x:.0f},{y-80:.0f} L{x:.0f},{y-26:.0f}" stroke="#1a1a1a" stroke-width="2"/>'
        s += f'<circle cx="{x:.0f}" cy="{y-10:.0f}" r="16" fill="#c8bca8"/><circle cx="{x-5:.0f}" cy="{y-12:.0f}" r="3" fill="#000"/><circle cx="{x+5:.0f}" cy="{y-12:.0f}" r="3" fill="#000"/>'
        s += f'<path d="M{x-14:.0f},{y+6:.0f} L{x+14:.0f},{y+6:.0f} L{x+18:.0f},{y+46:.0f} L{x-18:.0f},{y+46:.0f} Z" fill="#8a7a6a"/>'
    s += '<path d="M300,1100 L900,1100 L860,1140 L340,1140 Z" fill="#1a0e08"/>'
    return S(s, fogb(950, 0.35, 8))
@art
def l_fog(): return AZ.ART["l_fog"]()
@art
def l_fire_glow(): return AZ.ART["l_fire_glow"]()
@art
def l_dust(): return S(clouds(26, 1050, 1350, 13, "#b8c0c8", (0.1, 0.28), (200, 600), (40, 110)))
@art
def black(): return S('<rect width="2400" height="1350" fill="#000"/>')


def run(names):
    todo = names or list(ART)
    for n in todo:
        open(os.path.join(A, n + ".svg"), "w").write(ART[n]())
    print("wrote", len(todo))


if __name__ == "__main__":
    run(sys.argv[1:])
