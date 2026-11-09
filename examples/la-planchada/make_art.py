#!/usr/bin/env python3
"""La Planchada — all illustrations. Usage: python3 make_art.py [name_filter ...]  -> art/*.svg
Then: node /home/claude/pipeline/render_svg.js art/*.svg"""
import sys, os, math, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from env import *  # noqa  (plib + pipeline art helpers)

ART = os.path.join(HERE, "art"); os.makedirs(ART, exist_ok=True)
ONLY = sys.argv[1:]
REG = {}


def art(name):
    def deco(fn):
        REG[name] = fn
        return fn
    return deco


def save(name, body):
    open(os.path.join(ART, name + ".svg"), "w", encoding="utf-8").write(body)
    print("wrote", name)


DARK = '<rect width="2400" height="1350" fill="#06090b"/>'

# ============================================================================ 1984: CORRIDOR SET
CORR = dict(vx=1200, vy=560)


@art("corr_bg")
def _():
    c, P, g = corridor("night", far_lamp_dim=True, **CORR)
    save("corr_bg", canvas(c))
    # layers that share the same perspective
    save("corr_flick", canvas(far_lamp_glow(P, g["lamp_z"][-1])))
    x, y, h = figure_at(P, 21.0)
    save("corr_ghost_far", canvas(nurse(x, y, h, "ghost", dissolve=0.25)))
    x, y, h = figure_at(P, 11.0, X=0.25)
    save("corr_ghost_back", canvas(nurse(x, y, h, "ghost", view="back", pose="hang", dissolve=0.3)))
    x, y, h = figure_at(P, 5.2, X=-0.15)
    save("corr_ghost_mid", canvas(nurse(x, y, h, "ghost", dissolve=0.2)))
    x, y, h = figure_at(P, 3.2, X=0.35)
    save("corr_ines", canvas(nurse(x, y, h * 0.98, "alive", view="back", pose="hang", pal=INES, hem=720, apron=False,
                                   cardigan="#2c3e5c", glow=False)))
    # foreground: near door frame + wheelchair silhouette (parallax)
    fg = ['<path d="M2190,0 L2400,0 L2400,1350 L2230,1350 L2230,120 Z" fill="#05090a"/>',
          '<path d="M2230,120 L2262,120 L2262,1350 L2230,1350 Z" fill="#0c1413"/>']
    wx, wy = 330, 1350   # wheelchair, side view, facing right
    sp = "".join(f'<line x1="{wx:.0f}" y1="{wy-230:.0f}" x2="{wx+math.cos(a_)*200:.0f}" y2="{wy-230+math.sin(a_)*200:.0f}" stroke="#030606" stroke-width="5"/>' for a_ in [i*math.pi/8 for i in range(16)])
    fg.append(f'<g><circle cx="{wx}" cy="{wy-230}" r="215" fill="none" stroke="#030606" stroke-width="26"/>'
              f'<circle cx="{wx}" cy="{wy-230}" r="185" fill="none" stroke="#030606" stroke-width="8"/>{sp}'
              f'<circle cx="{wx}" cy="{wy-230}" r="26" fill="#030606"/>'
              f'<path d="M{wx-130},{wy-760} L{wx-90},{wy-760} L{wx-40},{wy-330} L{wx+330},{wy-330} L{wx+330},{wy-290} L{wx-70},{wy-290} Z" fill="#030606"/>'
              f'<path d="M{wx-170},{wy-790} L{wx-90},{wy-790} L{wx-90},{wy-760} L{wx-170},{wy-770} Z" fill="#030606"/>'
              f'<path d="M{wx-60},{wy-560} L{wx+250},{wy-560} L{wx+260},{wy-530} L{wx-50},{wy-530} Z M{wx+230},{wy-545} L{wx+250},{wy-330}" fill="#030606" stroke="#030606" stroke-width="14"/>'
              f'<path d="M{wx+330},{wy-310} L{wx+420},{wy-110} L{wx+470},{wy-110}" stroke="#030606" stroke-width="18" fill="none"/>'
              f'<circle cx="{wx+430}" cy="{wy-60}" r="52" fill="none" stroke="#030606" stroke-width="18"/></g>')
    save("corr_fg", canvas(*fg))


@art("corr2_bg")
def _():
    # alternative angle: vanishing point to the right, more lamps off, sign "SALA DE HOMBRES"
    c, P, g = corridor("night", vx=1750, vy=600, lamps_on=[True, False, True, False, False, True, False], seed=7, gurney=False)
    sx0, sy0 = P.p(-1.3, -1.75, 6.5); sx1, sy1 = P.p(0.1, -1.35, 6.5); tp = P.p(-0.6, -2.05, 6.5)
    sign = (f'<line x1="{sx0+30:.0f}" y1="{tp[1]:.0f}" x2="{sx0+30:.0f}" y2="{sy0:.0f}" stroke="#0a0f0e" stroke-width="5"/>'
            f'<line x1="{sx1-30:.0f}" y1="{tp[1]:.0f}" x2="{sx1-30:.0f}" y2="{sy0:.0f}" stroke="#0a0f0e" stroke-width="5"/>'
            f'<rect x="{sx0:.0f}" y="{sy0:.0f}" width="{sx1-sx0:.0f}" height="{sy1-sy0:.0f}" fill="#d9e2dc" opacity="0.85"/>'
            f'<text x="{(sx0+sx1)/2:.0f}" y="{sy1-(sy1-sy0)*0.28:.0f}" font-family="Oswald" font-size="{(sx1-sx0)/8.2:.0f}" text-anchor="middle" fill="#1a2a26">SALA DE HOMBRES</text>')
    save("corr2_bg", canvas(c, sign))
    x, y, h = figure_at(P, 7.5, X=-0.9)
    save("corr2_ghost", canvas(nurse(x, y, h, "ghost", dissolve=0.25)))


@art("doorway")
def _():
    # dark doorway, face of Eulalia emerging from the black (b063 scare)
    o = ['<rect width="2400" height="1350" fill="#0c1314"/>']
    o.append('<rect x="0" y="0" width="2400" height="1350" fill="#1d2a29"/>')
    for i in range(14):  # wall tiles
        o.append(f'<line x1="0" y1="{760+i*44}" x2="2400" y2="{760+i*44}" stroke="#0c1615" stroke-width="3"/>')
    for i in range(30):
        o.append(f'<line x1="{i*84}" y1="760" x2="{i*84}" y2="1350" stroke="#0c1615" stroke-width="3"/>')
    o.append('<rect x="0" y="740" width="2400" height="26" fill="#0a1311"/>')
    o.append('<rect x="760" y="60" width="880" height="1290" fill="#0d1716"/>')   # frame
    o.append('<rect x="810" y="110" width="780" height="1240" fill="#010203"/>')  # black opening
    o.append('<path d="M810,110 L1590,110 L1590,1350 L1400,1350 Q1300,700 810,600 Z" fill="#000" opacity="0.6"/>')
    o.append(glow(1200, 120, 900, "green", 0.18))
    o.append(portrait(1200, 600, 0.82, "ghost", eyes="open"))
    # darkness eating the lower body
    d, u = lg([(0, "#010203", 0), (0.5, "#010203", 0.0), (0.72, "#010203", 0.92), (1, "#010203", 1)], 0, 0, 0, 1)
    o.append(d + f'<rect x="700" y="110" width="1000" height="1240" fill="{u}"/>')
    o.append('<rect x="0" y="0" width="810" height="1350" fill="#1d2a29"/><rect x="1590" y="0" width="810" height="1350" fill="#1d2a29"/>')
    for i in range(14):
        o.append(f'<line x1="0" y1="{760+i*44}" x2="810" y2="{760+i*44}" stroke="#0c1615" stroke-width="3"/><line x1="1590" y1="{760+i*44}" x2="2400" y2="{760+i*44}" stroke="#0c1615" stroke-width="3"/>')
    o.append('<rect x="0" y="740" width="810" height="26" fill="#0a1311"/><rect x="1590" y="740" width="810" height="26" fill="#0a1311"/>')
    o.append('<path d="M760,60 L810,110 L810,1350 L760,1350 Z M1640,60 L1590,110 L1590,1350 L1640,1350 Z" fill="#0d1716"/><rect x="760" y="60" width="880" height="50" fill="#0d1716"/>')
    save("doorway", canvas(*o))


# ============================================================================ 1984: WARD SET
@art("ward_bg")
def _():
    w, P, g = ward("night")
    save("ward_bg", canvas(w))
    # ghost standing in the aisle between beds
    x, y, h = figure_at(P, 8.2, X=-1.2, eye=g["eye"], height=1.65)
    save("ward_ghost", canvas(nurse(x, y, h, "ghost", dissolve=0.25)))
    # foreground: iron footboard close to camera + curtain edge
    fg = []
    bx, by = 1500, 1350
    fg.append('<path d="M0,0 L330,0 Q300,300 350,700 Q300,1000 340,1350 L0,1350 Z" fill="#cbd6d1" opacity="0.92"/>')
    for i in range(7):
        x = 40 + i * 45
        fg.append(f'<path d="M{x},0 Q{x+20},500 {x+10},1350" stroke="#000" stroke-opacity="0.18" stroke-width="16" fill="none" filter="url(#blur1)"/>')
    fg.append('<rect x="0" y="0" width="400" height="16" fill="#0a0f0e"/>')
    fg.append(f'<path d="M1300,1350 L1300,900 Q1800,760 2300,900 L2300,1350" stroke="#050808" stroke-width="34" fill="none"/>')
    for i in range(1, 8):
        x = 1300 + i * 125
        fg.append(f'<line x1="{x}" y1="{900 - 140*math.sin(math.pi*i/8):.0f}" x2="{x}" y2="1350" stroke="#050808" stroke-width="16"/>')
        fg.append(f'<circle cx="{x}" cy="{900 - 140*math.sin(math.pi*i/8):.0f}" r="22" fill="#050808"/>')
    fg.append('<rect x="1290" y="1180" width="1020" height="26" fill="#050808"/>')
    save("ward_fg", canvas(*fg))


def old_man_head(cx, cy, s=1.0, col="#d8b9a0", sh="#9c7660", eyes="open"):
    """Don Refugio lying on a pillow, 3/4 view facing up-right. (cx,cy) head centre."""
    o = [f'<g transform="translate({cx},{cy}) scale({s}) rotate(-12)">']
    o.append(f'<path d="M-70,10 Q-74,-60 -10,-74 Q60,-80 76,-10 Q84,50 50,82 Q10,104 -30,90 Q-66,74 -70,10 Z" fill="{col}"/>')
    o.append(f'<path d="M40,-60 Q86,0 50,82" stroke="{sh}" stroke-width="16" fill="none" opacity="0.45" filter="url(#blur1)"/>')
    o.append(f'<path d="M-72,0 Q-80,-40 -60,-56 Q-50,-30 -58,10 Z M70,-30 Q82,-20 78,10 Q70,0 66,-20 Z" fill="#e9e6df"/>')  # white tufts
    o.append(f'<ellipse cx="-62" cy="10" rx="12" ry="20" fill="{sh}"/>')
    for sx in (-1, 1):
        ex = 6 + sx * 26
        if eyes == "open":
            o.append(f'<path d="M{ex-13},-6 Q{ex},-14 {ex+13},-6 Q{ex},0 {ex-13},-6 Z" fill="#f1ece4"/><circle cx="{ex+2}" cy="-6" r="4.5" fill="#2a1e17"/>')
        else:
            o.append(f'<path d="M{ex-13},-5 Q{ex},1 {ex+13},-5" stroke="#3a2a20" stroke-width="3" fill="none"/>')
        o.append(f'<path d="M{ex-15},-20 Q{ex},-28 {ex+15},-20" stroke="#e9e6df" stroke-width="5" fill="none"/>')
        o.append(f'<path d="M{ex-12},8 Q{ex},12 {ex+12},8" stroke="{sh}" stroke-width="2" fill="none"/>')
    o.append(f'<path d="M8,-2 Q16,24 10,34 Q4,38 -4,34" stroke="{sh}" stroke-width="3" fill="none"/>')
    o.append(f'<path d="M-22,48 Q4,38 30,46 Q10,58 -22,48 Z" fill="#e9e6df"/>')   # white moustache
    o.append(f'<path d="M-10,62 Q6,68 20,60" stroke="#8a5a48" stroke-width="3" fill="none"/>')
    for i in range(4):
        o.append(f'<path d="M{-40+i*8},{-52+i*3} Q{0},{-60+i*4} {40-i*6},{-48+i*4}" stroke="{sh}" stroke-width="1.5" fill="none" opacity="0.5"/>')
    o.append('</g>')
    return "".join(o)


@art("bed12_bg")
def _():
    # close view of bed 12: pillow, don Refugio, blanket, bedside table with glass + pills, IV stand, curtain, moonlit window
    o = ['<rect width="2400" height="1350" fill="#18211f"/>']
    o.append('<rect x="0" y="0" width="2400" height="760" fill="#2c3a37"/><rect x="0" y="760" width="2400" height="590" fill="#14231e"/>')
    o.append('<rect x="0" y="748" width="2400" height="18" fill="#0d1815"/>')
    # window with moonlight
    o.append('<rect x="1560" y="80" width="560" height="560" fill="#0d1516"/><rect x="1590" y="110" width="500" height="500" fill="#6b8597"/>')
    o.append(glow(1840, 360, 700, "moon", 0.55))
    o.append('<rect x="1835" y="110" width="12" height="500" fill="#0d1516"/><rect x="1590" y="355" width="500" height="12" fill="#0d1516"/>')
    o.append(moon(1960, 220, 46, halo=3))
    o.append('<polygon points="1590,610 2090,610 1700,1350 900,1350" fill="#cfe2ef" opacity="0.06"/>')
    # curtain at left
    o.append(curtain(Persp(), 0, 0, 0, 0, 1, folds=1) if False else "")
    o.append('<path d="M0,0 L520,0 Q480,500 540,1350 L0,1350 Z" fill="#a9b8b3" opacity="0.85"/>')
    for i in range(8):
        o.append(f'<path d="M{30+i*62},0 Q{50+i*62},600 {40+i*66},1350" stroke="#000" stroke-opacity="0.2" stroke-width="20" fill="none" filter="url(#blur2)"/>')
    # iron headboard
    o.append('<path d="M640,1350 L640,420 Q1050,300 1460,420 L1460,1350" stroke="#0a100f" stroke-width="26" fill="none"/>')
    for i in range(1, 8):
        x = 640 + i * 102.5
        yy = 420 - 120 * math.sin(math.pi * i / 8)
        o.append(f'<line x1="{x:.0f}" y1="{yy:.0f}" x2="{x:.0f}" y2="900" stroke="#0a100f" stroke-width="12"/><circle cx="{x:.0f}" cy="{yy:.0f}" r="16" fill="#0a100f"/>')
    o.append('<rect x="630" y="890" width="840" height="20" fill="#0a100f"/>')
    # mattress + pillow + head + blanket
    o.append('<path d="M560,900 L1540,900 L1700,1350 L380,1350 Z" fill="#d6e0dc"/>')
    o.append('<path d="M700,760 Q1050,700 1400,760 Q1460,840 1380,920 Q1050,960 720,920 Q640,840 700,760 Z" fill="#eef3f1"/>')
    o.append('<path d="M720,900 Q1050,950 1380,900" stroke="#b9c6c1" stroke-width="6" fill="none"/>')
    o.append(old_man_head(1050, 790, 1.9))
    o.append('<path d="M420,1350 L560,1010 Q1050,940 1560,1010 L1700,1350 Z" fill="#8fa29c"/>')       # blanket
    o.append('<path d="M560,1010 Q1050,940 1560,1010 L1580,1060 Q1050,990 540,1060 Z" fill="#e3ebe8"/>')  # folded sheet
    o.append('<path d="M760,1060 Q900,1180 820,1350 M1180,1050 Q1260,1200 1220,1350 M1000,1040 Q1040,1200 990,1350" stroke="#5f716b" stroke-width="10" fill="none" opacity="0.5"/>')
    # hand resting on blanket
    o.append('<path d="M1260,1040 Q1320,1020 1380,1040 Q1400,1070 1360,1080 Q1300,1086 1262,1070 Z" fill="#d8b9a0"/>')
    # bedside table + glass + pills + "12"
    o.append('<rect x="1700" y="860" width="420" height="490" fill="#1c2724"/><rect x="1680" y="840" width="460" height="30" fill="#26332f"/>')
    o.append('<rect x="1760" y="960" width="300" height="12" fill="#121a18"/><circle cx="1910" cy="1100" r="14" fill="#5a6662"/>')
    o.append('<path d="M1790,700 L1850,700 L1844,838 L1796,838 Z" fill="#cfe6e8" opacity="0.5"/><rect x="1796" y="770" width="48" height="68" fill="#9fc7cf" opacity="0.4"/>')
    o.append('<ellipse cx="1990" cy="836" rx="60" ry="10" fill="#e8eeec"/><circle cx="1975" cy="828" r="9" fill="#f6f6f2"/><circle cx="2000" cy="830" r="8" fill="#e8c46a"/>')
    o.append('<text x="1475" y="400" font-family="Oswald" font-size="64" fill="#cfd9d4" opacity="0.6">12</text>')
    # IV stand with bottle (suero)
    o.append('<line x1="2240" y1="120" x2="2240" y2="1350" stroke="#3b4846" stroke-width="12"/><line x1="2140" y1="150" x2="2340" y2="150" stroke="#3b4846" stroke-width="10"/>')
    o.append('<path d="M2140,160 L2200,160 L2196,330 Q2170,350 2144,330 Z" fill="#d6ece8" opacity="0.6"/><rect x="2146" y="250" width="50" height="80" fill="#a6d6cb" opacity="0.5"/>')
    o.append('<path d="M2170,350 Q2150,700 1400,1060" stroke="#d6ece8" stroke-opacity="0.35" stroke-width="4" fill="none"/>')
    save("bed12_bg", canvas(*o))
    # ghost nurse standing at the bedside, reaching to the blanket (layer)
    save("bed12_ghost", canvas(nurse(1560, 1500, 1350, "ghost", pose="reach", dissolve=0.35)))


@art("pov_bg")
def _():
    # lying in bed looking toward the foot of the bed and the dark ward; lamp above
    o = ['<rect width="2400" height="1350" fill="#0b1112"/>']
    w, P, g = ward("night", vx=1200, vy=420, n_beds=4, F=700, lamps=False)
    o.append(f'<g opacity="0.75">{w}</g>')
    o.append('<rect width="2400" height="1350" fill="#060a0b" opacity="0.45"/>')
    # own blanket (lying down, looking at the feet)
    o.append('<path d="M-50,1350 L-50,1180 Q400,1080 800,1030 Q1000,1000 1200,1000 Q1400,1000 1600,1030 Q2000,1080 2450,1180 L2450,1350 Z" fill="#6f817c"/>')
    o.append('<path d="M760,1060 Q900,960 1040,1010 Q1100,960 1200,1000 Q1300,960 1360,1010 Q1500,960 1640,1060" fill="#869893"/>')
    o.append('<path d="M300,1350 Q600,1150 900,1060 M2100,1350 Q1800,1150 1500,1060 M1200,1350 L1200,1080" stroke="#4c5d58" stroke-width="20" fill="none" opacity="0.55" filter="url(#blur1)"/>')
    o.append('<path d="M-50,1180 Q400,1080 800,1030 Q1000,1000 1200,1000 Q1400,1000 1600,1030 Q2000,1080 2450,1180" stroke="#a7b8b3" stroke-width="8" fill="none" opacity="0.6"/>')
    # iron footboard of own bed
    o.append('<path d="M620,1100 L620,720 Q1200,600 1780,720 L1780,1100" stroke="#050909" stroke-width="28" fill="none"/>')
    for i in range(1, 9):
        x = 620 + i * 128.9
        yy = 720 - 120 * math.sin(math.pi * i / 9)
        o.append(f'<line x1="{x:.0f}" y1="{yy:.0f}" x2="{x:.0f}" y2="1000" stroke="#050909" stroke-width="13"/><circle cx="{x:.0f}" cy="{yy:.0f}" r="17" fill="#050909"/>')
    o.append('<rect x="605" y="985" width="1190" height="22" fill="#050909"/>')
    save("pov_bg", canvas(*o))
    # pale ghost hand reaching down from top (toward forehead / camera)
    hnd = ['<g transform="translate(1250,-120) rotate(12) scale(5.2)" filter="url(#softedge2)">',
           '<g filter="url(#blur3)" opacity="0.6" fill="#bff4ff"><path d="M-30,-60 L30,-60 L34,40 Q40,110 30,150 L-30,150 Q-40,100 -34,40 Z"/></g>',
           '<path d="M-26,-80 L26,-80 L28,20 L-28,20 Z" fill="#e8f2f5"/>',  # cuff
           '<path d="M-28,10 L28,10 L26,24 L-26,24 Z" fill="#c6d6dc"/>',
           hand(0, 50, 1.25, "#e3edf0", "#9fb3bd", 0, "open"), '</g>']
    save("pov_hand", canvas(*hnd))
    # Eulalia leaning in over the patient (seen from below, close)
    save("pov_nurse", canvas(f'<g transform="rotate(180 1200 675) scale(1,1)"></g>', portrait(1250, 640, 1.25, "ghost")))


@art("station_bg")
def _():
    # 1984 nurses' station: desk, warm desk lamp, charts, rotary phone, wall clock, medicine cabinet, window to corridor
    o = ['<rect width="2400" height="1350" fill="#24312e"/>']
    o.append('<rect x="0" y="780" width="2400" height="570" fill="#15231f"/>')
    for i in range(12):
        o.append(f'<line x1="0" y1="{790+i*48}" x2="2400" y2="{790+i*48}" stroke="#0d1916" stroke-width="3"/>')
    o.append('<rect x="0" y="770" width="2400" height="20" fill="#0d1916"/>')
    # medicine cabinet (left)
    o.append('<rect x="140" y="160" width="560" height="760" fill="#cdd6d2"/><rect x="170" y="190" width="500" height="380" fill="#6e8a86"/>')
    for sy in (310, 440):
        o.append(f'<rect x="170" y="{sy}" width="500" height="10" fill="#9fb0ab"/>')
    r = random.Random(4)
    for sy in (190, 320, 450):
        x = 190
        while x < 640:
            bw = r.choice([30, 40, 50]); bh = r.choice([70, 90, 110])
            col = r.choice(["#d9a35a", "#a9c7d4", "#e8e2d4", "#6b4a2a", "#b8d6b0"])
            o.append(f'<rect x="{x}" y="{sy+120-bh}" width="{bw}" height="{bh}" rx="5" fill="{col}" opacity="0.85"/><rect x="{x+bw*0.2}" y="{sy+120-bh-14}" width="{bw*0.6}" height="16" fill="#333"/>')
            x += bw + 12
    o.append('<line x1="420" y1="190" x2="420" y2="570" stroke="#cdd6d2" stroke-width="8"/>')
    o.append('<rect x="170" y="600" width="500" height="290" fill="#b9c4bf"/><circle cx="400" cy="740" r="10" fill="#555"/><circle cx="440" cy="740" r="10" fill="#555"/>')
    # wall clock
    o.append(clock_face(1220, 230, 120, 2, 30))
    # bulletin board with papers
    o.append('<rect x="1520" y="140" width="520" height="380" fill="#6a5238"/>')
    for (px, py, rot) in ((1560, 180, -4), (1700, 170, 3), (1860, 190, -2), (1600, 330, 2), (1780, 320, -3)):
        o.append(f'<rect x="{px}" y="{py}" width="140" height="170" fill="#e8e4d8" transform="rotate({rot} {px+70} {py+85})"/>')
        o.append(f'<circle cx="{px+70}" cy="{py+10}" r="7" fill="#b03030"/>')
    # desk
    o.append('<rect x="760" y="760" width="1640" height="60" fill="#3a2c20"/><rect x="760" y="820" width="1640" height="530" fill="#2a2018"/>')
    o.append('<rect x="820" y="880" width="420" height="160" fill="#231a13"/><circle cx="1030" cy="960" r="10" fill="#8a7458"/>')
    # charts / clipboards
    o.append('<rect x="1300" y="700" width="300" height="70" fill="#e8e4d8" transform="rotate(-3 1450 735)"/>')
    o.append('<rect x="1330" y="660" width="260" height="60" fill="#d9d2c0" transform="rotate(4 1460 690)"/>')
    # rotary phone
    o.append('<path d="M1700,760 L1720,690 Q1800,670 1880,690 L1900,760 Z" fill="#141414"/><circle cx="1800" cy="725" r="28" fill="#2a2a2a"/><circle cx="1800" cy="725" r="10" fill="#555"/>')
    o.append('<path d="M1690,690 Q1800,620 1910,690 L1890,700 Q1800,650 1710,700 Z" fill="#0c0c0c"/>')
    # desk lamp (warm)
    o.append('<path d="M2080,760 L2200,760 L2160,740 L2120,740 Z" fill="#1a1a14"/><line x1="2140" y1="740" x2="2100" y2="560" stroke="#1a1a14" stroke-width="12"/>')
    o.append('<line x1="2100" y1="560" x2="2000" y2="520" stroke="#1a1a14" stroke-width="12"/><path d="M1930,560 L2060,480 L2090,530 L1990,600 Z" fill="#2a3a2a"/>')
    o.append(glow(1990, 600, 520, "warm", 0.75))
    o.append('<polygon points="1960,590 2040,560 2300,760 1650,760" fill="url(#warmcone)" opacity="0.8"/>')
    o.append('<ellipse cx="1950" cy="770" rx="420" ry="40" fill="#ffd590" opacity="0.18" filter="url(#blur2)"/>')
    # coffee cup
    o.append('<path d="M1620,700 L1680,700 L1674,760 L1626,760 Z" fill="#e8e4d8"/><path d="M1680,712 Q1704,722 1678,742" stroke="#e8e4d8" stroke-width="6" fill="none"/>')
    save("station_bg", canvas(*o))
    # Amparo handing keys to Inés (two figures, layer)
    am = nurse(1050, 1420, 1080, "alive", pal=AMPARO, hem=720, apron=False, cardigan="#5a2630", glasses=True, pose="reach", glow=False)
    ine = nurse(1560, 1440, 1060, "alive", pal=INES, hem=720, apron=False, cardigan="#2c3e5c", pose="clasp", glow=False)
    keys = '<g transform="translate(1268,940)"><circle cx="0" cy="0" r="18" fill="none" stroke="#d9c27a" stroke-width="6"/><path d="M8,14 L20,60 M-6,16 L-14,58" stroke="#d9c27a" stroke-width="7"/></g>'
    save("station_figs", canvas(am, ine, keys))
    # sleeping night nurse + ghost hand on her shoulder
    sl = ['<g transform="translate(1250,770)">',
          # folded arms on the desk (navy cardigan sleeves)
          '<path d="M-330,0 Q-320,-70 -200,-80 L180,-80 Q290,-76 300,0 Z" fill="#2c3e5c"/>',
          '<path d="M-330,0 Q-320,-70 -200,-80 L180,-80" stroke="#1b2740" stroke-width="6" fill="none"/>',
          '<path d="M-60,-20 Q-40,-60 20,-62" stroke="#1b2740" stroke-width="5" fill="none"/>',
          '<ellipse cx="250" cy="-30" rx="46" ry="30" fill="#d9b294"/>',
          # back + shoulders rising behind the arms
          '<path d="M-250,-60 Q-260,-300 -60,-330 Q150,-340 240,-200 Q270,-120 240,-60 Z" fill="#2c3e5c"/>',
          '<path d="M-150,-300 Q-20,-350 120,-300 L100,-250 Q0,-280 -120,-250 Z" fill="#f0f4f2"/>',
          # head resting sideways on the arms, hair dark with bun, cap slipped
          '<ellipse cx="-20" cy="-150" rx="120" ry="92" fill="#2b1d16"/>',
          '<ellipse cx="-110" cy="-200" rx="44" ry="40" fill="#2b1d16" stroke="#140d09" stroke-width="4"/>',
          '<path d="M30,-110 Q100,-120 110,-80 Q60,-60 20,-80 Z" fill="#d9b294"/>',
          '<path d="M-40,-250 L80,-262 L96,-212 L-30,-196 Z" fill="#f0f4f2" stroke="#a9b8b4" stroke-width="3" transform="rotate(-18 30 -230)"/>',
          '</g>']
    gh = ['<g transform="translate(860,300) rotate(-38) scale(2.2)" filter="url(#softedge2)">',
          '<g filter="url(#blur3)" opacity="0.6" fill="#bff4ff"><path d="M-30,-160 L30,-160 L30,40 L-30,40 Z"/><ellipse cx="0" cy="70" rx="40" ry="50"/></g>',
          '<path d="M-26,-180 L26,-180 L24,10 L-24,10 Z" fill="#e8f2f5"/><path d="M-27,-10 L27,-10 L25,10 L-25,10 Z" fill="#b9ccd3"/>',
          hand(0, 44, 1.0, "#e3edf0", "#9fb3bd", 0, "open"), '</g>']
    save("station_sleep", canvas(*sl))
    save("station_ghosthand", canvas(*gh))


def clock_face(cx, cy, r, hh, mm, rim="#1a1a1a", face="#ece8dc", hands_only=False):
    o = []
    if not hands_only:
        o.append(f'<circle cx="{cx}" cy="{cy}" r="{r*1.12}" fill="{rim}"/><circle cx="{cx}" cy="{cy}" r="{r}" fill="{face}"/>')
        for i in range(60):
            a = math.radians(i * 6); l = 0.14 if i % 5 == 0 else 0.05
            o.append(f'<line x1="{cx+math.sin(a)*r*0.92:.1f}" y1="{cy-math.cos(a)*r*0.92:.1f}" x2="{cx+math.sin(a)*r*(0.92-l):.1f}" y2="{cy-math.cos(a)*r*(0.92-l):.1f}" stroke="#1a1a1a" stroke-width="{r*0.03 if i%5==0 else r*0.012:.1f}"/>')
        for n in range(1, 13):
            a = math.radians(n * 30)
            o.append(f'<text x="{cx+math.sin(a)*r*0.66:.1f}" y="{cy-math.cos(a)*r*0.66+r*0.07:.1f}" font-family="Cinzel" font-size="{r*0.2:.0f}" text-anchor="middle" fill="#1a1a1a">{n}</text>')
    ah = math.radians((hh % 12) * 30 + mm * 0.5); am = math.radians(mm * 6)
    o.append(f'<line x1="{cx}" y1="{cy}" x2="{cx+math.sin(ah)*r*0.5:.1f}" y2="{cy-math.cos(ah)*r*0.5:.1f}" stroke="#0a0a0a" stroke-width="{r*0.06:.1f}" stroke-linecap="round"/>')
    o.append(f'<line x1="{cx}" y1="{cy}" x2="{cx+math.sin(am)*r*0.78:.1f}" y2="{cy-math.cos(am)*r*0.78:.1f}" stroke="#0a0a0a" stroke-width="{r*0.035:.1f}" stroke-linecap="round"/>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{r*0.05:.1f}" fill="#0a0a0a"/>')
    return "".join(o)


@art("clock")
def _():
    o = ['<rect width="2400" height="1350" fill="#2a3835"/>']
    for i in range(16):
        o.append(f'<line x1="0" y1="{i*90}" x2="2400" y2="{i*90}" stroke="#22302d" stroke-width="2"/>')
    o.append(glow(1200, 675, 900, "green", 0.25))
    o.append(f'<ellipse cx="1220" cy="720" rx="560" ry="560" fill="#000" opacity="0.5" filter="url(#blur4)"/>')
    o.append(clock_face(1200, 675, 470, 3, 0))
    o.append('<path d="M760,300 Q1200,180 1640,300" stroke="#fff" stroke-opacity="0.18" stroke-width="40" fill="none" filter="url(#blur2)"/>')
    o.append('<text x="1200" y="560" font-family="Oswald" font-size="26" fill="#4a4a44" text-anchor="middle" letter-spacing="5">SALUBRIDAD</text>')
    save("clock", canvas(*o))


@art("chart84")
def _():
    # nursing sheet (hoja de enfermería) with the 3 a.m. medicines already ticked
    o = ['<rect width="2400" height="1350" fill="#1d1712"/>']
    o.append(glow(1300, 500, 1300, "warm", 0.55))
    o.append('<g transform="rotate(-4 1200 675)">')
    o.append('<rect x="520" y="60" width="1400" height="1400" fill="#e9e3d2"/>')
    o.append('<rect x="520" y="60" width="1400" height="1400" fill="#000" opacity="0.05" filter="url(#paper)"/>')
    o.append('<text x="1220" y="160" font-family="Oswald" font-size="58" text-anchor="middle" fill="#2a2a2a">HOJA DE ENFERMERÍA</text>')
    o.append('<text x="600" y="240" font-family="Oswald" font-size="34" fill="#3a3a3a">HOSPITAL JUÁREZ · SALA DE HOMBRES · CAMA 12</text>')
    cols = [600, 840, 1290, 1520, 1840]
    for i, hd in enumerate(["HORA", "MEDICAMENTO", "DOSIS", "FIRMA"]):
        o.append(f'<text x="{cols[i]+20}" y="320" font-family="Oswald" font-size="32" fill="#333">{hd}</text>')
    for k in range(11):
        y = 340 + k * 90
        o.append(f'<line x1="600" y1="{y}" x2="1840" y2="{y}" stroke="#7a7466" stroke-width="2"/>')
    for x in cols:
        o.append(f'<line x1="{x}" y1="280" x2="{x}" y2="1240" stroke="#7a7466" stroke-width="2"/>')
    rows = [("22:00", "Penicilina", "1 amp.", "I. R."), ("23:00", "Suero glucosado", "500 ml", "I. R."), ("01:00", "Paracetamol", "500 mg", "I. R."),
            ("03:00", "Penicilina", "1 amp.", None), ("03:00", "Cambio de suero", "500 ml", None)]
    for k, (h, m, d, f) in enumerate(rows):
        y = 340 + k * 90 + 62
        o.append(f'<text x="620" y="{y}" font-family="Lora" font-style="italic" font-size="44" fill="#1b2a5a">{h}</text>')
        o.append(f'<text x="860" y="{y}" font-family="Lora" font-style="italic" font-size="40" fill="#1b2a5a">{m}</text>')
        o.append(f'<text x="1305" y="{y}" font-family="Lora" font-style="italic" font-size="40" fill="#1b2a5a">{d}</text>')
        if f:
            o.append(f'<text x="1520" y="{y}" font-family="Lora" font-style="italic" font-size="40" fill="#1b2a5a">{f}</text>')
        else:  # mysterious ticks in faded old ink
            o.append(f'<path d="M1540,{y-20} l22,24 l50,-56" stroke="#4a3a2a" stroke-width="7" fill="none" opacity="0.85"/>')
    o.append('</g>')
    # pen
    o.append('<g transform="rotate(32 1900 1000)"><rect x="1700" y="985" width="520" height="34" rx="16" fill="#1a1a1a"/><path d="M1700,985 L1640,1002 L1700,1019 Z" fill="#c9c9c9"/></g>')
    save("chart84", canvas(*o))


if __name__ == "__main__":
    for extra in ("art_b.py", "art_c.py"):
        p = os.path.join(HERE, extra)
        if os.path.exists(p):
            exec(compile(open(p, encoding="utf-8").read(), p, "exec"), globals())
    for name, fn in REG.items():
        if ONLY and not any(f in name for f in ONLY):
            continue
        fn()
