#!/usr/bin/env python3
"""Illustrations for 'El Hombre Caimán' (San Pedro Huamelula, Oaxaca) — writes art/*.svg (2400x1350).
Parts (palms, mangroves, palapas, canoes, the caiman, the Chontal king, the Huave princess, elders, fishermen) live in
caiman_parts.py; a few generic layers are reused from earlier videos (azul_art, sb_art, cadejo_art).
Usage: python3 make_art.py [name ...]   then: node /home/claude/pipeline/render_svg.js art/*.svg"""
import sys, os, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '/home/claude/pipeline'); sys.path.insert(0, HERE)
from art import *
from caiman_parts import *
from art import reflection as refl
from base_chars import villager
from beso_art import S, clouds, portrait_bg
import azul_art as AZ
import cadejo_art as CJ

A = os.path.join(HERE, "art"); os.makedirs(A, exist_ok=True)
ART = {}
def art(fn):
    ART[fn.__name__] = fn; return fn

RED = "#c8141a"
def dim(op=0.3, col="#02040a"): return f'<rect width="2400" height="1350" fill="{col}" opacity="{op}"/>'


def night_sky(mx=1750, my=280, mr=105):
    return sky("#040912", "#163049", "#0c1d30") + stars(170, 4, 760) + moon(mx, my, mr) + clouds(8, 120, 600, 5, "#2a3e58", (0.15, 0.35))


def sea(y0=880, moonx=1750):
    s = water(y0, 1350, "#18323f", "#03070c") + refl(moonx, y0 + 5, 1350, "#dfe8f2", 240, 7)
    for i in range(10):
        yy = y0 + 30 + i * i * 4.4
        s += f'<path d="M0,{yy:.0f} Q600,{yy-10:.0f} 1200,{yy:.0f} T2400,{yy:.0f}" stroke="#7a9ab0" stroke-width="{1+i*0.4:.1f}" fill="none" opacity="{0.12+i*0.02:.2f}"/>'
    return s


def warm_sky(): return sky("#e8a050", "#f6e0a0", "#f0c070")


# ============================================================ lagoon / water
@art
def lagoon_night(): return S(lagoon_bg())
@art
def lagoon_night2(): return S(lagoon_bg(moon_xy=(650, 250), mr=95))
@art
def lagoon_night3(): return S(lagoon_bg(moon_xy=(1250, 190), mr=150), clouds(16, 880, 1150, 21, "#a0b8d0", (0.08, 0.2), (300, 700), (40, 90)))
@art
def caiman_close2():
    s = sky("#030810", "#0c1c2c") + glow(700, 300, 900, "moon", 0.5)
    s += f'<g transform="translate(2400,0) scale(-1,1)">{caiman_head_close(1250, 760, 1.0, mouth=0.0)}</g>'
    s += water(1060, 1350, "#10202a", "#020406") + '<path d="M0,1060 L2400,1060" stroke="#a8c8e0" stroke-width="3" opacity="0.4"/>'
    return S(s)
@art
def lagoon_dawn(): return S(lagoon_bg(dawn=True))
@art
def lagoon_eyes():
    s = night_sky(1900, 220, 90) + ridge(700, 50, "#0a1624", 4, step=50)
    s += water(720, 1350, "#16303f", "#02060a") + refl(1900, 725, 1350, "#dfe8f2", 160, 4)
    s += mangrove(150, 760, 0.7, 3, "#02060a", MOON) + mangrove(2280, 760, 0.8, 5, "#02060a", MOON)
    for i in range(6):  # ripples around the eyes
        s += f'<ellipse cx="1200" cy="770" rx="{160+i*90}" ry="{18+i*9}" fill="none" stroke="#9ab8d0" stroke-width="3" opacity="{0.4-i*0.06:.2f}"/>'
    s += reeds(0, 2400, 1350, 9, "#020407", 90, 260)
    return S(s)
@art
def l_eyes(): return S(eyes_pair(1200, 760, 1.0))
@art
def l_caiman_swim():
    s = '<g opacity="0.95">' + caiman(1500, 1080, 0.55, flip=True, sil=True, rim="#c8dcf0") + '</g>'
    s += f'<path d="M700,1080 Q1100,1070 1500,1090" stroke="#c8dcf0" stroke-width="3" fill="none" opacity="0.4"/>'
    for i in range(4):
        s += f'<path d="M{1010-i*40},{1060-i*12} Q{900-i*80},{1080} {800-i*90},{1100+i*10}" stroke="#a8c8e0" stroke-width="3" fill="none" opacity="{0.4-i*0.08:.2f}"/>'
    s += '<rect x="400" y="1095" width="1600" height="255" fill="#050a10" opacity="0.6"/>'
    return S(s)
@art
def caiman_close():
    s = '<rect width="2400" height="1350" fill="#030609"/>' + glow(1600, 400, 900, "moon", 0.5)
    s += caiman_head_close(1250, 760, 1.0, mouth=0.45)
    s += water(1100, 1350, "#10202a", "#020406") + '<path d="M0,1100 L2400,1100" stroke="#a8c8e0" stroke-width="3" opacity="0.4"/>'
    return S(s)
@art
def caiman_full():
    s = lagoon_bg(moon_xy=(1800, 250), mr=90, mangroves=True)
    s += '<path d="M0,1080 C600,1050 1800,1050 2400,1080 L2400,1350 L0,1350 Z" fill="#141a14"/>'
    s += glow(500, 800, 500, "warm", 0.35) + caiman(1250, 1150, 1.25, flip=False, rim="#c8dcff")
    s += '<path d="M150,1150 Q700,1160 1300,1150" stroke="#a8c8e0" stroke-width="3" fill="none" opacity="0.4"/>'
    return S(s)
@art
def canoe_night():
    s = lagoon_bg(moon_xy=(1600, 260))
    s += canoe(1150, 1050, 0.9, rim=MOON) + fisher_sil(1150, 1010, 360, "stand", rim=MOON)
    s += '<path d="M1210,700 L1250,1080" stroke="#05080a" stroke-width="10"/>'
    return S(s)
@art
def canoe_far():
    s = lagoon_bg(moon_xy=(1200, 300), mr=80) + dim(0.25)
    s += canoe(1200, 960, 0.35, rim=MOON) + fisher_sil(1200, 945, 160, "stand", rim=MOON)
    s += clouds(14, 880, 1050, 12, "#a0b8d0", (0.08, 0.2), (300, 600), (40, 80))
    return S(s)
@art
def canoe_close():
    s = '<rect width="2400" height="1350" fill="#030609"/>' + glow(1700, 200, 800, "moon", 0.4)
    s += water(650, 1350, "#122632", "#020406")
    s += canoe(1200, 780, 2.6, color="#0e0a08", rim=MOON)
    s += '<path d="M400,690 Q1200,720 2000,690" stroke="#3a2a1c" stroke-width="10" fill="none"/>'
    s += '<path d="M1500,300 L1700,860" stroke="#1a120a" stroke-width="22"/><path d="M1690,830 L1740,880 L1720,900 L1660,860 Z" fill="#c8ccd0"/>'
    for i in range(5):
        s += f'<ellipse cx="1200" cy="{900+i*30}" rx="{900+i*60}" ry="{40+i*8}" fill="none" stroke="#a8c8e0" stroke-width="3" opacity="{0.35-i*0.05:.2f}"/>'
    s += '<g opacity="0.55">' + caiman(1300, 1150, 0.7, sil=True, rim="#7a98b0") + '</g>'
    return S(s)
@art
def canoe_dawn():
    s = lagoon_bg(dawn=True) + canoe(1200, 1030, 0.8, color="#16141a", rim="#ffb27a")
    s += '<path d="M1080,1010 L1180,990 M1200,995 L1320,1015" stroke="#2a1a10" stroke-width="12"/>'
    return S(s)
@art
def water_face():
    s = '<rect width="2400" height="1350" fill="#02050a"/>' + water(0, 1350, "#0e2230", "#02060a")
    s += f'<g opacity="0.75" transform="translate(0,0)">{princess_bust(1200, 640, 1.6, rim="#9fc2e8", reptile=True, smile=0.0, wet=True)}</g>'
    s += '<rect width="2400" height="1350" fill="#0a2232" opacity="0.35"/>'
    for i in range(10):
        s += f'<ellipse cx="1200" cy="600" rx="{120+i*110}" ry="{40+i*40}" fill="none" stroke="#b8d0e8" stroke-width="4" opacity="{0.35-i*0.03:.2f}"/>'
    s += '<path d="M0,0 L2400,0 L2400,170 C1600,230 800,230 0,170 Z" fill="#0c0806"/><path d="M0,170 C800,230 1600,230 2400,170" stroke="#a8c8e0" stroke-width="5" fill="none" opacity="0.6"/>'
    return S(s)
@art
def reflection():
    s = night_sky(1700, 250, 90) + water(650, 1350, "#16303f", "#02060a")
    s += '<path d="M0,650 L2400,650 L2400,700 L0,720 Z" fill="#141a14"/>'
    s += king_full(800, 700, 560, torch=False, kneel=True, rim=MOON)
    s += glow(1350, 960, 380, "moon", 0.6) + '<g opacity="0.7" transform="translate(0,1400) scale(1,-1)">' + princess_full(1350, 700, 560, rim="#ffffff", fill="#8aa4c4") + '</g>'
    for i in range(8): s += f'<path d="M{900+i*20},{760+i*50} q200,-10 400,0" stroke="#a8c8e0" stroke-width="3" opacity="0.35"/>'
    return S(s)
@art
def mangrove_path():
    s = sky("#030810", "#0c1c2c") + stars(80, 9, 500) + glow(1700, 200, 600, "moon", 0.5)
    s += water(980, 1350, "#10222e", "#02060a")
    for i, x in enumerate([100, 600, 1100, 1700, 2300]):
        s += mangrove(x, 1020 + (i % 2) * 40, 1.1 + (i % 2) * 0.3, 20 + i, "#020509", MOON)
    s += king_full(1150, 1120, 520, torch=True, rim=MOON)
    s += reeds(0, 2400, 1350, 3, "#010305", 100, 200)
    return S(s)
@art
def prints_mud():
    s = '<rect width="2400" height="1350" fill="#5a5448"/>' + sky("#6a7a8a", "#4a5058", y1=500) + water(380, 560, "#5a6a78", "#3a4450")
    s += '<rect y="540" width="2400" height="810" fill="#5a5246"/>'
    r = random.Random(4)
    for i in range(80): s += f'<ellipse cx="{r.uniform(0,2400):.0f}" cy="{r.uniform(560,1350):.0f}" rx="{r.uniform(30,90):.0f}" ry="{r.uniform(6,16):.0f}" fill="#1e1c1a" opacity="0.5"/>'
    for i in range(6):  # claw prints
        px = 400 + i * 300; py = 1200 - i * 110
        s += f'<g transform="translate({px},{py}) scale({1-i*0.1})">' + "".join(f'<path d="M0,0 L{dx},-60" stroke="#141210" stroke-width="16" stroke-linecap="round"/>' for dx in (-40, -14, 14, 40)) + '<ellipse cx="0" cy="10" rx="44" ry="30" fill="#141210"/></g>'
        qx = 560 + i * 300; qy = 1260 - i * 110
        s += f'<g transform="translate({qx},{qy}) scale({1-i*0.1})"><ellipse cx="0" cy="0" rx="26" ry="50" fill="#141210"/>' + "".join(f'<circle cx="{dx}" cy="-62" r="8" fill="#141210"/>' for dx in (-18, -6, 6, 18)) + '</g>'
    s += '<path d="M600,1350 Q1100,900 2100,620" stroke="#141210" stroke-width="30" fill="none" opacity="0.4"/>'
    return S(s)


# ============================================================ villages, land, drought
@art
def village_chontal():
    s = night_sky(1900, 230, 90) + sea(900, 1900)
    s += '<path d="M0,1350 L0,700 C300,640 700,620 1100,700 C1300,740 1400,860 1500,1350 Z" fill="#070c10"/>'
    for (x, y, k, lit) in ((250, 760, 0.7, True), (520, 730, 0.6, False), (800, 760, 0.75, True), (420, 960, 0.9, True), (1050, 900, 0.8, False), (750, 1100, 1.0, True)):
        s += palapa(x, y, k, lit, "#05080c", "#0a0d0e", MOON)
    s += palm(1250, 1050, 650, 0.2, 3, "#03060a", MOON) + palm(120, 980, 560, -0.15, 4, "#03060a", MOON)
    s += glow(600, 1180, 300, "warm", 0.6)
    return S(s)
@art
def huave_village():
    s = night_sky(600, 250, 90) + water(820, 1350, "#16303f", "#02060a") + refl(600, 825, 1350, "#dfe8f2", 200, 2)
    s += '<path d="M0,900 C600,860 1800,860 2400,900 L2400,980 C1800,950 600,950 0,980 Z" fill="#1a2028"/>'
    for (x, k, lit) in ((300, 0.5, True), (700, 0.55, False), (1100, 0.6, True), (1500, 0.5, True), (1900, 0.55, False), (2200, 0.5, True)):
        s += palapa(x, 920, k, lit, "#05080c", "#0a0d0e", MOON)
    for x in (500, 1300, 2050):
        s += canoe(x, 1080, 0.5, rim=MOON)
    s += palm(900, 930, 500, 0.15, 7, "#03060a", MOON) + palm(1750, 930, 560, -0.2, 8, "#03060a", MOON)
    s += net(1600, 1000, 1900, 1150, "#a8b8c8", 0.3, 8)
    return S(s)
@art
def milpa_coast():
    s = warm_sky() + glow(1800, 300, 500, "warm", 0.6) + sea(820, 1800).replace("#18323f", "#4a90a0").replace("#03070c", "#1a4a5a")
    s += '<path d="M0,1350 L0,820 C600,760 1400,800 2400,900 L2400,1350 Z" fill="#6a5a30"/>'
    r = random.Random(2)
    for i in range(70):
        x = r.uniform(0, 2400); y = r.uniform(850, 1300); h = r.uniform(120, 260) * (y / 1100)
        s += f'<path d="M{x:.0f},{y:.0f} L{x+r.uniform(-10,10):.0f},{y-h:.0f}" stroke="#3a5a22" stroke-width="{4*y/1100:.1f}"/>'
        for j in range(3):
            s += f'<path d="M{x:.0f},{y-h*(0.3+j*0.2):.0f} q{r.choice([-1,1])*h*0.3:.0f},{-h*0.1:.0f} {r.choice([-1,1])*h*0.4:.0f},{h*0.1:.0f}" stroke="#4a7a2a" stroke-width="{3*y/1100:.1f}" fill="none"/>'
    s += fisher_sil(1500, 1180, 380, "stand", fill="#2a2010")
    return S(s)
@art
def war_canoes():
    s = night_sky(1200, 220, 80) + water(820, 1350, "#16303f", "#02060a")
    for (x, y, k, fl) in ((650, 1050, 0.9, False), (1750, 1080, 0.9, True), (1150, 940, 0.5, False)):
        s += canoe(x, y, k, rim="#ffb060", flip=fl)
        for j in range(3):
            s += fisher_sil(x + (j - 1) * 160 * k, y - 20 * k, 300 * k, "stand", rim="#ffb060", facing=(-1 if fl else 1))
        s += glow(x + 120 * k, y - 360 * k, 300 * k, "warm", 0.9) + f'<path d="M{x+100*k},{y-60*k} L{x+120*k},{y-340*k}" stroke="#2a1a10" stroke-width="{10*k}"/>'
    for i in range(14): s += f'<path d="M{700+i*80},{1180+(i%3)*30} q40,-6 80,0" stroke="#ff9a40" stroke-width="3" opacity="0.4"/>'
    return S(s)
@art
def drought():
    s = sky("#f0e0b0", "#c88a40", "#e8b060") + glow(1200, 260, 400, "white", 1.0) + glow(1200, 260, 1100, "warm", 0.5)
    s += '<path d="M0,1350 L0,820 C500,780 1900,780 2400,820 L2400,1350 Z" fill="#9a6a38"/>'
    r = random.Random(5)
    for i in range(30):
        x = r.uniform(0, 2400); y = r.uniform(840, 1250); h = r.uniform(140, 300) * (y / 1050)
        s += f'<path d="M{x:.0f},{y:.0f} Q{x+20:.0f},{y-h*0.6:.0f} {x+r.uniform(30,90):.0f},{y-h*0.7:.0f}" stroke="#6a4a22" stroke-width="{5*y/1000:.1f}" fill="none"/>'
        for j in range(2):
            s += f'<path d="M{x+10:.0f},{y-h*(0.3+0.2*j):.0f} q{-h*0.2:.0f},{h*0.2:.0f} {-h*0.3:.0f},{h*0.4:.0f}" stroke="#7a5a2a" stroke-width="{3*y/1000:.1f}" fill="none"/>'
    for i in range(40):
        x = r.uniform(0, 2400); y = r.uniform(900, 1350)
        s += f'<path d="M{x:.0f},{y:.0f} l{r.uniform(-120,120):.0f},{r.uniform(-10,30):.0f} l{r.uniform(-80,80):.0f},{r.uniform(0,30):.0f}" stroke="#4a2e14" stroke-width="3" fill="none" opacity="0.7"/>'
    s += palm(300, 900, 520, -0.1, 9, "#4a3018") + palm(2100, 880, 600, 0.12, 10, "#4a3018")
    return S(s)
@art
def cracked_earth():
    s = '<rect width="2400" height="1350" fill="#a8743e"/>' + glow(1200, 300, 1300, "warm", 0.4)
    r = random.Random(8)
    pts = [(r.uniform(-100, 2500), r.uniform(-100, 1450)) for _ in range(70)]
    for (x, y) in pts:
        n = r.randint(3, 5)
        for j in range(n):
            a = r.uniform(0, 6.28); L = r.uniform(120, 260)
            s += f'<path d="M{x:.0f},{y:.0f} l{math.cos(a)*L*0.5:.0f},{math.sin(a)*L*0.5:.0f} l{math.cos(a+0.3)*L*0.5:.0f},{math.sin(a+0.3)*L*0.5:.0f}" stroke="#3a2210" stroke-width="{r.uniform(5,12):.0f}" fill="none" stroke-linecap="round"/>'
    s += '<g transform="translate(1250,760) rotate(-10)">' + fish(0, 0, 3.0, 0, "#8a8070") + '</g>'
    s += '<rect width="2400" height="1350" fill="#000" opacity="0.08"/>'
    return S(s)
@art
def cracked_rain():
    s = ART["cracked_earth"]().replace("#a8743e", "#4a3a2c")
    s = s[:s.rindex("</svg>")] + '<rect width="2400" height="1350" fill="#0a1a2a" opacity="0.55"/>' + "".join(
        f'<ellipse cx="{random.Random(i).uniform(0,2400):.0f}" cy="{random.Random(i+99).uniform(0,1350):.0f}" rx="{random.Random(i).uniform(30,80):.0f}" ry="{random.Random(i).uniform(8,20):.0f}" fill="none" stroke="#a8c8e0" stroke-width="3" opacity="0.5"/>' for i in range(40)) + "</svg>"
    return s
@art
def dry_lagoon():
    s = sky("#e8c890", "#c08850") + glow(1700, 240, 500, "white", 0.8)
    s += '<path d="M0,1350 L0,760 C800,720 1600,720 2400,760 L2400,1350 Z" fill="#7a5a3a"/>'
    s += '<ellipse cx="1200" cy="900" rx="700" ry="60" fill="#8a9a9a" opacity="0.5"/>'
    r = random.Random(3)
    for i in range(30):
        s += f'<path d="M{r.uniform(0,2400):.0f},{r.uniform(950,1350):.0f} l{r.uniform(-100,100):.0f},{r.uniform(0,30):.0f}" stroke="#4a3220" stroke-width="5"/>'
    s += canoe(900, 1150, 0.9, color="#3a2614") + mangrove(200, 800, 0.8, 4, "#5a4026") + mangrove(2250, 800, 0.9, 7, "#5a4026")
    for i in range(6): s += fish(1400 + i * 110, 1200 + (i % 2) * 40, 0.8, r.uniform(-30, 30), "#a89a80")
    s += fisher_sil(1650, 1060, 420, "stand", fill="#3a2614")
    return S(s)
@art
def nets_empty():
    s = sky("#e8b878", "#b07040") + glow(600, 300, 500, "warm", 0.8)
    s += '<path d="M0,1350 L0,820 L2400,840 L2400,1350 Z" fill="#6a4a30"/>' + water(800, 900, "#9a8a7a", "#7a6a5a")
    s += fisher_sil(800, 1180, 640, "pull", fill="#1a120a", rim="#ffc070")
    s += fisher_sil(1150, 1200, 600, "pull", fill="#1a120a", rim="#ffc070", seed=2)
    s += net(1350, 980, 2100, 1250, "#e8d8b0", 0.6, 16)
    s += '<path d="M900,700 Q1200,820 1350,990" stroke="#2a1a0a" stroke-width="8" fill="none"/>'
    return S(s)
@art
def nets_close():
    s = '<rect width="2400" height="1350" fill="#5a3e28"/>' + glow(1200, 400, 1100, "warm", 0.4)
    s += net(-100, -100, 2500, 1450, "#d8c8a0", 0.7, 22)
    s += hand_open(700, 900, 3.0, -20) + hand_open(1700, 880, 3.0, 200)
    s += fish(1200, 1000, 1.6, 20, "#9a9080")
    return S(s)
@art
def council():
    s = '<rect width="2400" height="1350" fill="#0a0604"/>' + glow(1200, 950, 900, "warm", 0.8)
    s += '<path d="M200,0 L1200,-200 L2200,0 L2400,500 L0,500 Z" fill="#140c06"/>'
    s += '<path d="M1080,1050 L1200,880 L1320,1050 Z" fill="#ffb040"/><path d="M1140,1050 L1200,940 L1260,1050 Z" fill="#fff0b0"/>'
    s += '<ellipse cx="1200" cy="1060" rx="200" ry="30" fill="#1a0e06"/>'
    for i, x in enumerate([420, 700, 1700, 1980]):
        s += f'<g transform="translate({x},1180) scale(0.75)">' + elder_full_sil(rim="#ffb060", facing=(1 if x < 1200 else -1)) + '</g>'
    s += king_full(1200, 1350, 560, torch=False, rim="#ffb060")
    return S(s)


def elder_full_sil(rim="#ffb060", facing=1):
    fl = "" if facing > 0 else " scale(-1,1)"
    p = ("M0,-700 C-40,-700 -56,-660 -52,-620 C-50,-590 -36,-576 -26,-570 C-100,-550 -150,-480 -170,-380 L-210,-200 "
         "L-260,-60 L-230,0 L240,0 L230,-120 L160,-380 C140,-480 90,-550 26,-570 C36,-576 50,-590 52,-620 C56,-660 40,-700 0,-700 Z")
    return f'<g transform="scale(1){fl}"><path d="{p}" fill="#0a0604"/><path d="{p}" fill="none" stroke="{rim}" stroke-width="5" opacity="0.6" filter="url(#blur1)"/></g>'


@art
def elder_portrait(): return S(portrait_bg("candle"), elder_bust(1200, 560, 1.75, smile=-0.3, lids=0.5))
@art
def map_isthmus():
    s = '<rect width="2400" height="1350" fill="#d8c8a0"/>' + '<rect width="2400" height="1350" fill="#8a6a40" filter="url(#paper)" opacity="0.4"/>'
    s += '<path d="M0,0 L2400,0 L2400,300 C2000,340 1800,420 1500,400 C1300,600 1100,700 900,760 C700,800 400,840 0,900 Z" fill="#c8b48a"/>'
    s += '<path d="M0,900 C400,840 700,800 900,760 C1100,700 1300,600 1500,400 C1800,420 2000,340 2400,300 L2400,1350 L0,1350 Z" fill="#8aa8b0" opacity="0.7"/>'
    s += '<path d="M0,900 C400,840 700,800 900,760 C1100,700 1300,600 1500,400 C1800,420 2000,340 2400,300" stroke="#5a4a30" stroke-width="6" fill="none"/>'
    s += '<path d="M1500,450 C1600,470 1750,480 1850,440 C1800,500 1640,520 1520,500 Z" fill="#6a90a0"/>'  # lagoons
    s += '<path d="M1300,560 C1380,560 1440,540 1480,520" stroke="#6a90a0" stroke-width="20" fill="none"/>'
    for (x, y, t, sz) in ((1080, 690, "San Pedro Huamelula", 46), (1620, 380, "Lagunas huaves", 40), (1650, 250, "Istmo de Tehuantepec", 50), (600, 400, "OAXACA", 80), (800, 1100, "Océano Pacífico", 56)):
        s += f'<text x="{x}" y="{y}" font-family="IM FELL English" font-size="{sz}" fill="#3a2a18" text-anchor="middle">{t}</text>'
    s += '<circle cx="1080" cy="730" r="18" fill="#a81a1a"/>' + glow(1080, 730, 80, "red", 0.6)
    s += '<g transform="translate(2150,1100)"><path d="M0,-120 L20,0 L0,120 L-20,0 Z" fill="#3a2a18"/><text x="0" y="-140" font-family="Cinzel" font-size="40" fill="#3a2a18" text-anchor="middle">N</text></g>'
    return S(s)


# ============================================================ people
@art
def king_portrait(): return S(portrait_bg("moon"), king_bust(1200, 560, 1.75, look=-0.15, turn=-0.1))
@art
def king_resolve(): return S(portrait_bg("candle"), king_bust(1200, 560, 1.75, rim="#ffb860", look=0.2, lids=0.3, smile=-0.2))
@art
def king_fear(): return S(portrait_bg("moon"), king_bust(1200, 560, 1.75, look=0.4, turn=0.15, shock=True), glow(2000, 900, 500, "warm", 0.35))
@art
def king_shore():
    s = lagoon_bg(moon_xy=(1500, 260), mr=95)
    s += '<path d="M0,1080 C700,1040 1700,1040 2400,1080 L2400,1350 L0,1350 Z" fill="#141a18"/>'
    s += king_full(900, 1200, 620, torch=True, rim=MOON)
    return S(s)
@art
def king_walk_bg():
    s = lagoon_bg(moon_xy=(1900, 230), mr=80)
    s += '<path d="M0,1150 C700,1110 1700,1120 2400,1150 L2400,1350 L0,1350 Z" fill="#101614"/>'
    return S(s)
@art
def l_king_walk(): return S(king_full(800, 1240, 560, torch=True, rim=MOON))
@art
def l_torch_glow(): return S(glow(1200, 600, 1100, "warm", 0.25))
@art
def king_kneel():
    s = lagoon_bg(moon_xy=(1700, 250), mr=95) + '<path d="M0,1060 C700,1020 1700,1020 2400,1060 L2400,1350 L0,1350 Z" fill="#161c18"/>'
    s += king_full(1000, 1230, 760, torch=False, kneel=True, rim="#ffd090")
    s += caiman(1640, 1180, 0.42, flip=True, rim="#ffd090")
    s += glow(300, 600, 500, "warm", 0.5) + '<path d="M300,620 L280,1100" stroke="#2a1a10" stroke-width="16"/>'
    return S(s)
@art
def huave_king(): return S(portrait_bg("candle"), elder_bust(1200, 560, 1.75, smile=-0.1, lids=0.4, color=("#1a2a3a", "#4a6a8a", "#7a9ab8"), band="#b8402a"))
@art
def huave_king_smile(): return S(portrait_bg("candle"), elder_bust(1200, 560, 1.75, smile=0.6, lids=0.55, look=0.2, color=("#1a2a3a", "#4a6a8a", "#7a9ab8"), band="#b8402a"))
@art
def huave_king_call():
    s = lagoon_bg(moon_xy=(1300, 280), mr=100) + '<path d="M0,1080 C700,1040 1700,1040 2400,1080 L2400,1350 L0,1350 Z" fill="#141a18"/>'
    s += king_full(1000, 1250, 680, torch=False, arms_up=True, rim=MOON)
    s += glow(1700, 600, 400, "warm", 0.6) + '<path d="M1700,620 L1690,1120" stroke="#2a1a10" stroke-width="14"/>'
    return S(s)
@art
def princess_portrait(): return S(portrait_bg("moon"), princess_bust(1200, 560, 1.75, look=0.2, lids=0.3, smile=0.25))
@art
def princess_soft(): return S(portrait_bg("moon"), glow(1200, 500, 900, "moon", 0.4), princess_bust(1200, 560, 1.75, look=0.0, lids=0.35, smile=0.55, rim="#dfeaff"))
@art
def princess_eyes(): return S(portrait_bg("ghost"), princess_bust(1200, 560, 1.75, look=0.0, smile=0.05, reptile=True, wet=True, rim="#dfeaff"))
@art
def princess_shore():
    s = lagoon_bg(moon_xy=(1200, 300), mr=110) + '<path d="M0,1080 C700,1040 1700,1040 2400,1080 L2400,1350 L0,1350 Z" fill="#141a18"/>'
    return S(s)
@art
def l_princess(): return S(princess_full(1200, 1180, 640, rim="#dfeaff", back=True))
@art
def fisher_portrait(): return S(portrait_bg("moon"), fisher_bust(1200, 560, 1.75, look=-0.2, smile=0.1))
@art
def fisher_laugh(): return S(portrait_bg("candle"), fisher_bust(1200, 560, 1.75, rim="#ffb860", look=0.3, smile=0.9, lids=0.35, laugh=True))
@art
def fisher_mute(): return S(portrait_bg("ghost"), fisher_bust(1200, 560, 1.75, rim="#dfeaff", shock=True))


# ============================================================ wedding, rain, abundance
@art
def wedding_ancient():
    s = lagoon_bg(moon_xy=(1200, 230), mr=110) + '<path d="M0,1040 C700,1000 1700,1000 2400,1040 L2400,1350 L0,1350 Z" fill="#1a1e1a"/>'
    # arbor of palm leaves with flowers
    s += '<path d="M900,1080 L900,560 M1500,1080 L1500,560" stroke="#0a0806" stroke-width="30"/><path d="M860,580 Q1200,420 1540,580" stroke="#0a0806" stroke-width="40" fill="none"/>'
    r = random.Random(3)
    for i in range(50):
        t = i / 49; x = 860 + 680 * t; y = 580 - math.sin(t * math.pi) * 140
        s += f'<circle cx="{x+r.uniform(-30,30):.0f}" cy="{y+r.uniform(-20,30):.0f}" r="{r.uniform(10,18):.0f}" fill="{r.choice(["#e0507a","#f0c040","#ffffff","#f08a30"])}" opacity="0.9"/>'
    for i in range(80):
        s += f'<circle cx="{r.uniform(700,1700):.0f}" cy="{r.uniform(1060,1300):.0f}" r="{r.uniform(5,12):.0f}" fill="{r.choice(["#e0507a","#f0c040","#ffffff","#f08a30"])}" opacity="0.8"/>'
    for x in (700, 1700):
        s += glow(x, 760, 260, "warm", 0.9) + f'<path d="M{x},780 L{x},1100" stroke="#2a1a10" stroke-width="14"/>'
    for i, x in enumerate([200, 380, 2020, 2200]):
        s += f'<g transform="translate({x},1200) scale(0.7)">' + elder_full_sil(rim=MOON, facing=(1 if x < 1200 else -1)) + '</g>'
    return S(s)
@art
def l_copal():
    return S(clouds(14, 500, 1100, 17, "#d8d0c0", (0.08, 0.2), (80, 220), (120, 300), "blur4"))
@art
def weaving():
    s = '<rect width="2400" height="1350" fill="#120a06"/>' + glow(1700, 400, 900, "warm", 0.5)
    s += '<path d="M300,1350 L700,600 L1900,600 L2200,1350 Z" fill="#1e140c"/>'
    # white cotton dress with embroidered flowers and fish on a frame
    s += '<path d="M800,320 L1600,320 L1700,1150 L700,1150 Z" fill="#ece6d6"/><path d="M800,320 L1600,320" stroke="#3a2a1a" stroke-width="20"/>'
    r = random.Random(6)
    for i in range(30):
        x = r.uniform(780, 1620); y = r.uniform(700, 1100)
        if i % 3 == 0: s += fish(x, y, 0.6, r.uniform(-20, 20), "#3a8aa0")
        else:
            c = r.choice(["#d23a5a", "#e0a020", "#3a8a6a"])
            for a in range(6): s += f'<circle cx="{x+math.cos(a)*14:.0f}" cy="{y+math.sin(a)*14:.0f}" r="9" fill="{c}"/>'
    s += '<path d="M1080,320 L1080,520 L1320,520 L1320,320" stroke="#c8a040" stroke-width="10" fill="none"/>'
    s += hand_open(650, 900, 2.0, 30) + hand_open(1750, 900, 2.0, 160)
    return S(s)
@art
def crowd_shore():
    s = lagoon_bg(moon_xy=(1800, 240), mr=85) + '<path d="M0,1000 C700,960 1700,960 2400,1000 L2400,1350 L0,1350 Z" fill="#121614"/>'
    r = random.Random(5)
    for row, (y, h) in enumerate(((1120, 420), (1250, 520), (1380, 640))):
        for i in range(9):
            x = 120 + i * 270 + r.uniform(-50, 50) + row * 60
            kind = r.choice(["man", "woman", "fisher"])
            if kind == "fisher": s += fisher_sil(x, y, h, "stand", rim=MOON, seed=i)
            else: s += villager(x, y, h, kind, "#04060a", rim="#5a7a9a", seed=i)
    for x in (500, 1900): s += glow(x, 800, 300, "warm", 0.8) + f'<path d="M{x},820 L{x-10},1150" stroke="#2a1a10" stroke-width="14"/>'
    return S(s)
@art
def kiss_ancient():
    s = '<rect width="2400" height="1350" fill="#030609"/>' + glow(1300, 500, 1000, "moon", 0.5) + glow(500, 700, 500, "warm", 0.5)
    # big profile of the king leaning to the caiman's snout he holds in his arms
    p = ("M700,240 C620,240 560,300 560,380 C560,430 580,470 600,500 C580,520 560,540 570,560 C590,570 610,575 620,590 "
         "C610,620 630,640 650,650 C640,700 660,740 700,760 C760,800 820,820 860,860 L860,1350 L0,1350 L0,700 C200,600 400,560 500,520 C480,420 520,300 700,240 Z")
    s += f'<path d="{p}" fill="#05080b"/><path d="{p}" fill="none" stroke="{MOON}" stroke-width="7" opacity="0.7" filter="url(#blur1)"/>'
    s += '<path d="M700,240 C620,200 500,240 450,360 C420,460 380,600 300,700 L520,520 C500,420 560,300 700,240 Z" fill="#05080b"/>'
    s += '<path d="M480,300 C520,250 600,230 700,236" stroke="#d8c890" stroke-width="14" fill="none"/>'
    s += caiman_head_close(1600, 700, 0.55, mouth=0.0, rim=MOON).replace('translate(1600,700) scale(0.55)', 'translate(1640,700) scale(-0.55,0.55)')
    s += '<path d="M600,800 C800,1000 1200,1000 1400,900 L1500,1350 L500,1350 Z" fill="#06090c"/>'
    return S(s)
@art
def storm_village():
    s = sky("#05080e", "#1a2638") + clouds(26, -50, 600, 8, "#2a3448", (0.5, 0.9), (300, 700), (80, 200))
    s += '<path d="M1300,0 L1240,300 L1320,320 L1200,700" stroke="#e8f0ff" stroke-width="10" fill="none"/>' + glow(1260, 360, 600, "white", 0.5)
    s += sea(950, 1260).replace("#18323f", "#22343e")
    s += '<path d="M0,1350 L0,820 C400,780 900,800 1300,900 L1500,1350 Z" fill="#06090c"/>'
    for (x, y, k) in ((250, 900, 0.7), (600, 930, 0.8), (950, 1050, 0.9)):
        s += palapa(x, y, k, True, "#05080c", "#0a0d0e", "#c8d8f0")
    s += palm(1700, 1100, 700, -0.25, 3, "#03060a", "#c8d8f0") + palm(2100, 1080, 650, -0.3, 4, "#03060a", "#c8d8f0")
    return S(s)
@art
def rain_joy():
    s = sky("#0a1420", "#2a3a4a") + clouds(20, -50, 500, 9, "#3a4a5a", (0.5, 0.8), (300, 700), (80, 200))
    s += '<path d="M0,1350 L0,950 C800,920 1600,920 2400,950 L2400,1350 Z" fill="#1a1814"/>'
    s += palapa(300, 960, 0.7, True, "#05080c", "#0a0d0e") + palapa(2100, 960, 0.75, True, "#05080c", "#0a0d0e")
    r = random.Random(2)
    for i in range(7):
        x = 500 + i * 230 + r.uniform(-40, 40)
        if i % 3 == 1: s += king_full(x, 1230, 520, torch=False, arms_up=True, rim="#c8d8f0").replace("#c8ccd0", "#3a3e44")
        elif i % 3 == 0: s += villager(x, 1260, 560, "woman", "#05070a", rim="#8aa0c0", seed=i)
        else: s += villager(x, 1300, 340, "child", "#05070a", rim="#8aa0c0", seed=i)
    for i in range(40): s += f'<ellipse cx="{r.uniform(0,2400):.0f}" cy="{r.uniform(1000,1350):.0f}" rx="{r.uniform(30,80):.0f}" ry="8" fill="none" stroke="#a8c8e0" stroke-width="3" opacity="0.4"/>'
    return S(s)
@art
def fish_abundance():
    s = sky("#f0b878", "#f8e0b0") + glow(1700, 500, 600, "warm", 0.8) + water(700, 1000, "#c89a7a", "#6a5a5a")
    s += canoe(1200, 960, 1.6, color="#2a1a10", rim="#ffd0a0")
    r = random.Random(4)
    s += '<path d="M500,880 C800,1300 1600,1300 1900,880 Z" fill="#c8c0a8" opacity="0.25"/>' + net(500, 880, 1900, 1280, "#efe0c0", 0.6, 18)
    for i in range(70):
        s += fish(r.uniform(650, 1750), r.uniform(950, 1250), r.uniform(0.6, 1.0), r.uniform(-60, 60), r.choice(["#d8e0e8", "#b8c8d0", "#e8e8e0"]))
    s += fisher_sil(600, 900, 520, "pull", fill="#2a1a10", rim="#ffd0a0") + fisher_sil(1850, 900, 520, "pull", fill="#2a1a10", rim="#ffd0a0", facing=-1)
    return S(s)
@art
def two_peoples():
    s = '<rect width="2400" height="1350" fill="#0a0604"/>' + glow(1200, 900, 1000, "warm", 0.8)
    s += '<path d="M1080,1080 L1200,900 L1320,1080 Z" fill="#ffb040"/><path d="M1140,1080 L1200,960 L1260,1080 Z" fill="#fff0b0"/>'
    for i in range(5):
        s += fisher_sil(300 + i * 150, 1250, 560 - i * 20, "stand", fill="#0a0604", rim="#ffb060", facing=1, seed=i)
        s += villager(2100 - i * 150, 1260, 540 - i * 20, ("woman" if i % 2 else "man"), "#0a0604", rim="#ffb060", seed=i)
    s += '<path d="M960,860 Q1200,700 1440,860" stroke="#ffd090" stroke-width="4" fill="none" opacity="0.4"/>'
    for i in range(30):
        s += f'<circle cx="{random.Random(i).uniform(900,1500):.0f}" cy="{random.Random(i+5).uniform(400,850):.0f}" r="4" fill="#ffb040" opacity="0.7"/>'
    return S(s)


# ============================================================ today: Huamelula
def church_white(x, yb, k=1.0, lit=True, night=False):
    w = "#c8c0b0" if not night else "#3a4250"; d = "#9a907e" if not night else "#20262e"
    s = f'<g transform="translate({x},{yb}) scale({k})">'
    s += f'<rect x="-300" y="-520" width="600" height="520" fill="{w}"/><path d="M-300,-520 L0,-700 L300,-520 Z" fill="{w}"/>'
    s += f'<rect x="-460" y="-820" width="180" height="820" fill="{w}"/><rect x="280" y="-820" width="180" height="820" fill="{w}"/>'
    for tx in (-370, 370):
        s += f'<path d="M{tx-90},-820 Q{tx},-960 {tx+90},-820 Z" fill="{d}"/><path d="M{tx},-960 L{tx},-1040 M{tx-20},-1010 L{tx+20},-1010" stroke="{d}" stroke-width="10"/>'
        s += f'<path d="M{tx-40},-760 L{tx-40},-660 Q{tx},-700 {tx+40},-660 L{tx+40},-760 Q{tx},-800 {tx-40},-760 Z" fill="#0a0806"/>'
    s += f'<path d="M-90,0 L-90,-260 Q0,-360 90,-260 L90,0 Z" fill="{"#ffb658" if lit else "#1a1410"}"/>'
    if lit: s += glow(0, -150, 300, "warm", 0.6)
    s += f'<circle cx="0" cy="-440" r="60" fill="{d}"/>'
    return s + '</g>'


@art
def church_huamelula():
    s = sky("#5a90c8", "#f0d8a8", "#a8c0d8") + glow(2000, 300, 500, "warm", 0.6)
    s += '<path d="M0,1350 L0,1060 L2400,1040 L2400,1350 Z" fill="#a8885a"/>'
    s += church_white(1200, 1080, 0.95, lit=False)
    s += palm(300, 1100, 760, -0.15, 2, "#2a3a2a") + palm(2150, 1100, 820, 0.12, 3, "#2a3a2a")
    s += papel_picado(120, "#d23a5a", 10, 3, 0.85)
    return S(s)
@art
def church_night():
    s = night_sky(1900, 230, 90) + '<path d="M0,1350 L0,1060 L2400,1040 L2400,1350 Z" fill="#0c0e10"/>'
    s += church_white(1200, 1080, 0.95, lit=True, night=True)
    s += palm(300, 1100, 760, -0.15, 2, "#03060a", MOON) + palm(2150, 1100, 820, 0.12, 3, "#03060a", MOON)
    s += papel_picado(120, "#b3122e", 10, 3, 0.6)
    return S(s)
@art
def church_fiesta():
    s = sky("#e88a50", "#f8d8a0", "#f0a870")
    s += '<path d="M0,1350 L0,1060 L2400,1040 L2400,1350 Z" fill="#8a6a40"/>'
    s += church_white(1200, 1080, 0.9, lit=True)
    s += papel_picado(80, "#d23a5a", 10, 3, 0.9) + papel_picado(260, "#2a8ac0", 10, 5, 0.85)
    r = random.Random(7)
    for i in range(22):
        s += villager(r.uniform(0, 2400), r.uniform(1220, 1380), r.uniform(380, 520), r.choice(["man", "woman", "woman"]), "#1a120a", seed=i)
    return S(s)
@art
def caiman_bride():
    s = '<rect width="2400" height="1350" fill="#2a1408"/>' + glow(1200, 600, 1300, "warm", 0.6)
    s += papel_picado(60, "#d23a5a", 10, 3, 0.9) + papel_picado(220, "#f0c040", 10, 4, 0.7)
    r = random.Random(8)
    for i in range(60): s += f'<circle cx="{r.uniform(0,2400):.0f}" cy="{r.uniform(1050,1350):.0f}" r="{r.uniform(8,16):.0f}" fill="{r.choice(["#e0507a","#f0c040","#ffffff","#f08a30"])}" opacity="0.8"/>'
    # held in two arms
    s += caiman(1150, 900, 0.95, dress=True, rim="#ffd090", body="#3a4a34", belly="#9a9a7a")
    s += hand_open(800, 980, 1.6, -30) + hand_open(1350, 980, 1.6, 200)
    s += '<path d="M500,1350 C600,1100 800,1000 900,990 L1400,990 C1500,1000 1700,1100 1800,1350 Z" fill="#e8e0d0" opacity="0.15"/>'
    return S(s)
@art
def bride_close():
    s = '<rect width="2400" height="1350" fill="#2a1408"/>' + glow(1300, 500, 1100, "warm", 0.6)
    s += caiman(600, 1100, 2.1, dress=True, rim="#ffd090", body="#3a4a34", belly="#9a9a7a")
    return S(s)
@art
def procession():
    s = sky("#e89050", "#f8dca0") + '<path d="M0,1350 L0,950 L2400,930 L2400,1350 Z" fill="#9a7a4a"/>'
    for (x, k) in ((200, 0.6), (700, 0.55), (1700, 0.6), (2200, 0.55)):
        s += f'<g transform="translate({x},960) scale({k})"><rect x="-260" y="-420" width="520" height="420" fill="#d8b890"/><rect x="-260" y="-440" width="520" height="30" fill="#8a3a2a"/><rect x="-60" y="-260" width="120" height="260" fill="#3a2010"/></g>'
    s += papel_picado(70, "#d23a5a", 10, 3, 0.9) + papel_picado(240, "#3a9a6a", 10, 6, 0.85)
    r = random.Random(3)
    for i in range(16):
        x = 100 + i * 150 + r.uniform(-30, 30)
        if i == 8: continue
        s += villager(x, 1300 + r.uniform(-20, 40), r.uniform(460, 560), r.choice(["man", "woman"]), "#1a100a", seed=i)
    s += '<g transform="translate(1250,860) scale(0.55)">' + caiman(0, 0, 1.0, dress=True, rim="#ffd090") + '</g>' + hand_open(1080, 900, 1.0, -30) + hand_open(1420, 900, 1.0, 200)
    s += villager(1250, 1320, 560, "woman", "#1a100a", seed=99)
    return S(s)
@art
def dance_mayor():
    s = '<rect width="2400" height="1350" fill="#1a0c06"/>' + glow(1200, 500, 1200, "warm", 0.7)
    s += papel_picado(60, "#d23a5a", 10, 3, 0.9) + papel_picado(200, "#2a8ac0", 10, 5, 0.85)
    s += '<path d="M1080,1250 L1050,950 L1350,950 L1320,1250 Z" fill="#0a0604"/>'
    s += villager(1200, 1300, 900, "man", "#0a0604", rim="#ffc070")
    s += '<g transform="translate(1200,830) scale(0.42)">' + caiman(0, 0, 1.0, dress=True, rim="#ffd090") + '</g>'
    r = random.Random(4)
    for i in range(12):
        x = r.uniform(0, 2400)
        if 850 < x < 1550: continue
        s += villager(x, 1360, r.uniform(500, 700), r.choice(["man", "woman"]), "#0a0604", rim="#ffa050", seed=i)
    for i in range(50): s += f'<rect x="{r.uniform(0,2400):.0f}" y="{r.uniform(0,900):.0f}" width="14" height="8" fill="{r.choice(["#e0507a","#f0c040","#ffffff","#40a0d0"])}" opacity="0.8" transform="rotate({r.uniform(0,90):.0f})"/>'
    return S(s)
@art
def kiss_today():
    s = '<rect width="2400" height="1350" fill="#1a0c06"/>' + glow(1200, 500, 1000, "warm", 0.6) + papel_picado(60, "#d23a5a", 10, 3, 0.7)
    p = ("M700,300 C620,300 560,360 560,440 C560,490 580,530 600,560 C580,580 560,600 570,620 C590,630 610,635 620,650 "
         "C610,680 630,700 650,710 C640,760 660,800 700,820 C760,860 820,880 860,920 L860,1350 L0,1350 L0,760 C200,660 400,620 500,580 C480,480 520,360 700,300 Z")
    s += f'<path d="{p}" fill="#0a0604"/><path d="{p}" fill="none" stroke="#ffc070" stroke-width="7" opacity="0.7" filter="url(#blur1)"/>'
    s += '<path d="M700,300 C600,280 520,320 500,380 L700,330 Z" fill="#0a0604"/><path d="M480,330 C560,250 700,240 860,300 L700,320 Z" fill="#0a0604"/>'
    s += '<g transform="translate(1600,760) scale(-0.6,0.6)">' + caiman(-950, 60, 1.0, dress=True, rim="#ffd090") + '</g>'
    return S(s)
@art
def copal_altar():
    s = '<rect width="2400" height="1350" fill="#0e0806"/>' + glow(1200, 700, 1000, "warm", 0.6)
    s += '<path d="M300,900 L2100,900 L2200,1350 L200,1350 Z" fill="#3a2214"/><path d="M300,900 L2100,900" stroke="#e8e0cc" stroke-width="20"/>'
    r = random.Random(2)
    for i in range(90): s += f'<circle cx="{r.uniform(320,2080):.0f}" cy="{r.uniform(820,940):.0f}" r="{r.uniform(10,20):.0f}" fill="{r.choice(["#f08a30","#f0c040","#e0507a","#ffffff"])}"/>'
    for x in (600, 900, 1500, 1800): s += candle_like(x, 900)
    s += '<path d="M1120,900 L1140,780 L1260,780 L1280,900 Z" fill="#6a4a2a"/>' + glow(1200, 700, 200, "warm", 0.6)
    for i in range(4): s += fish(800 + i * 240, 1000, 1.0, 0, "#c8d0d8")
    s += '<path d="M700,1080 C900,1060 1500,1060 1700,1080" stroke="#e0b040" stroke-width="8" fill="none"/>'
    s += '<path d="M800,1150 L1000,1110 L1200,1150 L1400,1110 L1600,1150" stroke="#f0c040" stroke-width="40" fill="none" opacity="0.8"/>'
    return S(s)


def candle_like(x, y):
    return glow(x, y - 200, 220, "warm", 0.8) + f'<rect x="{x-18}" y="{y-160}" width="36" height="160" fill="#efe6d0"/><path d="M{x},{y-210} Q{x+16},{y-180} {x},{y-160} Q{x-16},{y-180} {x},{y-210} Z" fill="#ffd36a"/>'


# ============================================================ misc
@art
def rider_road(): return CJ.ART["road_fog"]()
@art
def title_bg():
    s = '<rect width="2400" height="1350" fill="#020407"/>' + glow(1200, 700, 1000, "moon", 0.3)
    s += water(900, 1350, "#0e202c", "#010305")
    s += '<g opacity="0.9">' + eyes_pair(1200, 1000, 2.6) + '</g>'
    return S(s)
@art
def red_flash():
    s = '<rect width="2400" height="1350" fill="#1a0000"/>' + glow(1200, 675, 1200, "red", 0.8)
    s += '<g opacity="0.8">' + caiman_head_close(1250, 760, 0.9, eye="#ff3020", rim="#ff6040", mouth=0.5) + '</g>'
    return S(s)
@art
def l_fog(): return AZ.ART["l_fog"]()
@art
def l_fire_glow(): return AZ.ART["l_fire_glow"]()
@art
def l_candle_glow(): return AZ.ART["l_candle_glow"]()


def run(names):
    todo = names or list(ART)
    for n in todo:
        open(os.path.join(A, n + ".svg"), "w").write(ART[n]())
    print("wrote", len(todo))


if __name__ == "__main__":
    run(sys.argv[1:])
