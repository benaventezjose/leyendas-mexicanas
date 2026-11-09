#!/usr/bin/env python3
"""Illustrations for 'El Charro Negro'. Usage: python3 make_art.py [name ...]  (no args = all)
Writes art/<name>.svg ; render with node /home/claude/pipeline/render_svg.js art/*.svg"""
import sys, os, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'lib'))
from scenery import *

A = {}
def art(fn): A[fn.__name__] = fn; return fn
MOONRIM = "#a9c6e6"; RED = "#ff5a2a"

# ------------------------------------------------------------------ the old road
def _road_world(red=False, moon_xy=(1650, 300), moon_r=95):
    if red:
        s = sky('#0d0206', '#4a0e0c', mid='#22060a') + stars(90, 3, 600, '#ffb0a0')
        s += glow(1200, 470, 900, 'red', 0.55) + f'<circle cx="1200" cy="470" r="230" fill="#c8361e"/><circle cx="1200" cy="470" r="230" fill="url(#redglow)"/>'
        s += cloud_band(520, '#1a0406', 5, 9, 0.85, 40) + cloud_band(380, '#2a0808', 8, 6, 0.6, 30)
        far, mid, ground = '#1a0507', '#100304', '#0a0304'
    else:
        s = sky('#050a14', '#22344a', mid='#0c1626') + stars(170, 2, 700)
        s += moon(*moon_xy, moon_r) + cloud_band(moon_xy[1] + 20, '#1a2738', 4, 8, 0.75, 34) + cloud_band(480, '#162232', 9, 7, 0.6, 40)
        far, mid, ground = '#0f1a28', '#0a121c', '#080d14'
    s += ridge(790, 150, far, 4, step=30) + ridge(840, 80, mid, 11, step=30)
    s += f'<rect x="0" y="820" width="2400" height="530" fill="{ground}"/>'
    if not red: s += village_lights(250, 720, 812, 14, 4)
    s += road(520, 1880, 1230, 812, '#2b2a2a' if not red else '#2a0f0c', '#141518' if not red else '#120506', 1350, 220)
    # ruts and stones
    r = random.Random(8)
    for i in range(70):
        y = r.uniform(840, 1340); k = (y - 812) / 538
        x = 1230 + (r.uniform(-1, 1)) * (30 + 640 * k)
        s += f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(2+10*k)}" ry="{f(1+4*k)}" fill="#0c0d10" opacity="0.7"/>'
    # magueyes receding along road
    for i, (x, y, sz) in enumerate([(980, 840, 40), (1500, 850, 50), (860, 880, 80), (1640, 900, 95), (640, 960, 160), (1860, 990, 190), (330, 1080, 260), (2150, 1110, 300)]):
        s += maguey(x, y, sz, i + 3, '#04070b' if not red else '#070203', rim=None if red else '#5f7fa3')
    s += posts([1010, 940, 820, 600, 250], [830, 860, 905, 990, 1140], [40, 60, 95, 160, 270], '#04070b')
    s += grass(1340, 0, 2400, '#05080c', 160, 70, 3)
    return s

@art
def road_bg(): return svg(_road_world(False))
@art
def road_red(): return svg(_road_world(True))
@art
def road_fg():
    return svg(maguey(170, 1420, 560, 31, '#020407', rim='#5f7fa3'), nopal(2230, 1420, 250, 7, '#020407'),
               grass(1350, 0, 2400, '#020407', 260, 120, 9), '<path d="M0,1300 Q500,1270 900,1330 L900,1350 L0,1350 Z" fill="#020407"/>')

@art
def loma_moon():
    s = sky('#03070f', '#1d2c42', mid='#0a1424') + stars(200, 6, 900)
    s += f'<circle cx="1300" cy="560" r="1100" fill="url(#moonglow)"/>' + moon(1300, 560, 300, halo=2.2)
    s += cloud_band(700, '#0d1622', 2, 6, 0.55, 30)
    s += ridge(1000, 90, '#0a1220', 13, step=30)
    s += '<path d="M0,1350 L0,1080 Q600,1000 1100,985 Q1500,975 1900,1030 Q2200,1060 2400,1120 L2400,1350 Z" fill="#020407"/>'
    s += maguey(420, 1050, 150, 4, '#020407') + maguey(2050, 1060, 120, 7, '#020407') + grass(1000, 700, 1900, '#020407', 80, 40, 2)
    return svg(s)

# ------------------------------------------------------------------ riders (transparent layers)
@art
def rider_moon(): return svg(place(horse_and_rider('walk', MOONRIM, 3), 760, 1300, 1.02))
@art
def rider_red(): return svg(place(horse_and_rider('walk', RED, 3), 760, 1300, 1.02))
@art
def rider_gallop(): return svg(place(horse_and_rider('gallop', MOONRIM, 5, steam=False), 900, 1250, 0.95))
@art
def rider_hill(): return svg(place(horse_and_rider('walk', '#dfe9f5', 3), 900, 1000, 0.62))
@art
def rider_fire():
    rider_ = horse_and_rider('gallop', '#ffb060', 5, steam=False)
    wom = ('<g transform="translate(250,-650) scale(0.55)">' + woman_seated() + '</g>')
    back = (f'<g filter="url(#blur2)">{flame_tongues(-80, 700, -380, 260, 560, 40, 4, ("#c02a0a", "#ff5a14"), 0.75, 300, -1.1)}</g>'
            f'<g filter="url(#blur1)">{flame_tongues(-40, 680, -420, 180, 420, 46, 5, ("#ff7a1a", "#ffb030"), 0.7, 260, -1.2)}</g>')
    front = f'<g filter="url(#blur1)" opacity="0.35">{flame_tongues(80, 600, -520, 80, 200, 20, 6, ("#ff9a2a", "#ffd060"), 0.7, 200, -1.0)}</g>'
    return svg(place(glow(300, -500, 700, 'red', 0.9) + back + rider_ + wom, 900, 1250, 0.95))

def woman_seated(rim="#ffd0a0"):
    sh = ('<path d="M-60,-20 Q-90,120 -40,260 L60,250 Q90,120 60,-20 Z"/>'
          '<path d="M-50,-20 Q-56,-140 -40,-210 Q0,-236 40,-210 Q56,-140 52,-20 Z"/>'
          '<path d="M-30,-300 Q-36,-260 -22,-235 L22,-230 Q36,-240 40,-265 L50,-275 L40,-285 Q40,-315 20,-328 Q-18,-338 -30,-300 Z"/>')
    reb = 'M-48,-330 Q-8,-360 34,-332 Q50,-290 44,-260 L36,-270 Q30,-312 0,-318 Q-34,-312 -38,-270 Q-60,-180 -150,-120 L-170,-150 Q-90,-220 -48,-330 Z'
    arms = '<path d="M30,-190 Q120,-160 170,-120" stroke="#000" stroke-width="34" fill="none" stroke-linecap="round"/>'
    return lit(sh + arms, rim, top="#e8d6c0", base="#8a7a6a", bot="#3a2a20", y0=-340, y1=260, halo=0.3) + lit(f'<path d="{reb}"/>', rim, top="#3a3446", base="#201a2c", y0=-360, y1=-100, halo=0.2)

# ------------------------------------------------------------------ charro close-ups
@art
def charro_front():
    return svg(place(charro_front_fig(), 1200, 1300, 1.0))
def charro_front_fig(): return charro_front_(hand_out=True)
from cn import charro_front as charro_front_

@art
def charro_portrait():
    bg = sky('#04070d', '#18263a') + f'<circle cx="1500" cy="420" r="700" fill="url(#moonglow)"/>' + moon(1700, 260, 80, halo=3)
    bg += ridge(1100, 80, '#070c14', 5) + '<rect x="0" y="1100" width="2400" height="250" fill="#05080d"/>'
    return svg(bg, place(charro_front_(hand_out=False, bag=False, upper=True), 1200, 3720, 2.85))

@art
def charro_skull():
    bg = sky('#0a0103', '#3a0606', mid='#1a0204') + glow(1200, 600, 1000, 'red', 0.7)
    return svg(bg, place(charro_front_(face='skull', bag=False, rim=RED, eyes='#ff4a1a', upper=True), 1200, 3550, 2.7))

@art
def horse_head():
    bg = sky('#04080f', '#1c2a3e') + stars(80, 9, 700) + f'<circle cx="600" cy="300" r="600" fill="url(#moonglow)"/>' + moon(520, 260, 90, halo=2.5)
    bg += cloud_band(800, '#0a1220', 3, 8, 0.6, 60)
    # horse scaled so the head fills the right half; flip to face left
    h = horse('walk', rim=MOONRIM, seed=3, saddle=False, steam=False)
    st = ''
    r = random.Random(4)
    for i in range(9):
        x = 815 + i * 40 + r.uniform(-10, 10); y = -610 + i * 10 + r.uniform(-15, 15)
        st += f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{24+i*12}" ry="{12+i*6}" fill="#e6eef5" opacity="{0.3-i*0.028:.2f}" filter="url(#blur2)"/>'
    return svg(bg, f'<g transform="translate(3150,2950) scale(-3.05,3.05)">{h}</g>')

@art
def steam():
    r = random.Random(4); s = ''
    for i in range(10):
        x = 740 - i * 52 + r.uniform(-10, 10); y = 1060 + i * 18 + r.uniform(-15, 15)
        s += f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{50+i*26}" ry="{24+i*12}" fill="#e6eef5" opacity="{0.42-i*0.035:.2f}" filter="url(#blur3)"/>'
    return svg(s)

@art
def anselmo_side(): return svg(place(campesino('walk', MOONRIM), 1930, 1290, 0.78))

@art
def spurs():
    bg = '<rect width="2400" height="1350" fill="#04070c"/>' + f'<circle cx="1700" cy="200" r="900" fill="url(#moonglow)"/>'
    bg += '<rect x="0" y="1180" width="2400" height="170" fill="#0c0f14"/>'
    return svg(bg, place(horse_and_rider('walk', MOONRIM, 3, steam=False), 1200 - 432 * 3.2 + 200, 675 + 392 * 3.2 + 60, 3.2))

@art
def hooves():
    bg = sky('#060b16', '#26364a') + f'<circle cx="1200" cy="420" r="900" fill="url(#moonglow)"/>'
    bg += '<rect x="0" y="1150" width="2400" height="200" fill="#1d1d20"/>' + '<rect x="0" y="1150" width="2400" height="30" fill="#141518" opacity="0.8" filter="url(#blur2)"/>'
    r = random.Random(3)
    for i in range(40):
        bg += f'<ellipse cx="{r.uniform(0,2400):.0f}" cy="{r.uniform(1170,1340):.0f}" rx="{r.uniform(5,22):.0f}" ry="{r.uniform(3,8):.0f}" fill="#0c0c0e" opacity="0.8"/>'
    dust = ''.join(f'<ellipse cx="{x}" cy="{1010+r.uniform(-20,10):.0f}" rx="{r.uniform(80,180):.0f}" ry="{r.uniform(25,50):.0f}" fill="#8c8a86" opacity="0.22" filter="url(#blur3)"/>' for x in (520, 900, 1700, 2000))
    return svg(bg, place(horse('walk', rim=MOONRIM, seed=3, saddle=False, steam=False, eye=False), 120, 1250, 2.55), dust.replace('1010+','1225+'))

# ------------------------------------------------------------------ coins
def glove_hand(x, y, s=1.0, rot=0, sil=SIL):
    """Black-gloved hand palm up (holding from below), fingers to the right."""
    sh = ('<path d="M-260,40 Q-200,-10 -120,-20 L40,-40 Q90,-48 140,-30 L260,-20 Q290,-12 284,10 Q278,28 250,26 L150,24 '
          'Q170,40 230,48 Q262,56 256,80 Q248,98 222,94 L130,84 Q150,104 196,116 Q222,126 212,148 Q200,164 176,156 L100,138 '
          'Q40,150 -40,140 L-260,120 Z"/>')
    s_ = lit(sh, MOONRIM, top="#2a3444", base="#0a0b0f", bot="#040405", y0=-60, y1=160, off=(-4, 6), halo=0.25, outline="#000")
    s_ += f'<path d="M-250,40 L-250,120" stroke="{sil}" stroke-width="10"/><path d="M-232,36 L-232,122" stroke="{sil}" stroke-width="4" opacity="0.7"/>'
    s_ += '<path d="M150,24 Q120,30 100,20 M130,84 Q100,80 80,70 M100,138 Q70,128 50,118" stroke="#1d2532" stroke-width="5" fill="none"/>'
    return f'<g transform="translate({x},{y}) rotate({rot}) scale({s})">{s_}</g>'

def coin(x, y, r=40, tilt=0.45, seed=0, ash=0.0):
    rr = random.Random(seed)
    s = f'<g transform="translate({f(x)},{f(y)}) rotate({rr.uniform(-25,25):.0f}) scale(1,{tilt})">'
    if ash < 1:
        s += f'<circle r="{r}" fill="#b07a1a"/><circle r="{r*0.92}" fill="#f2c14e"/><circle r="{r*0.72}" fill="none" stroke="#b8860b" stroke-width="{r*0.06}"/>'
        s += f'<path d="M{-r*0.3},{-r*0.1} Q0,{-r*0.45} {r*0.3},{-r*0.1} Q0,{r*0.35} {-r*0.3},{-r*0.1} Z" fill="#c9952a"/>'
        s += f'<circle cx="{-r*0.35}" cy="{-r*0.35}" r="{r*0.18}" fill="#fff3c0" opacity="0.7"/>'
    if ash > 0:
        s += f'<circle r="{r*1.02}" fill="#6f6a66" opacity="{min(1,ash):.2f}"/><circle r="{r*0.7}" fill="#8a8580" opacity="{min(1,ash)*0.8:.2f}"/>'
        for k in range(6):
            a = rr.uniform(0, 6.28); d = rr.uniform(0, r * 0.8)
            s += f'<circle cx="{f(math.cos(a)*d)}" cy="{f(math.sin(a)*d)}" r="{f(r*rr.uniform(0.08,0.2))}" fill="#3a3634" opacity="{min(1,ash):.2f}"/>'
    return s + '</g>'

@art
def coins_hand():
    bg = sky('#04070d', '#141e2c') + f'<circle cx="1200" cy="560" r="800" fill="url(#warmglow)" opacity="0.55"/>'
    s = glove_hand(1120, 900, 1.9, -6)
    # leather bag sitting in the palm, open, overflowing
    s += (f'<path d="M820,820 Q760,600 900,470 L1380,470 Q1520,600 1460,820 Q1140,930 820,820 Z" fill="#3b2514"/>'
          f'<path d="M860,800 Q1140,890 1420,800" stroke="#1f1209" stroke-width="10" fill="none"/>'
          f'<path d="M900,470 Q1140,520 1380,470" stroke="#c9a46a" stroke-width="10" fill="none"/>'
          f'<path d="M940,600 Q980,700 960,790 M1300,600 Q1280,700 1310,790" stroke="#22150b" stroke-width="6" fill="none"/>')
    s += '<ellipse cx="1140" cy="470" rx="250" ry="60" fill="#ffcf5a" opacity="0.6" filter="url(#blur3)"/>'
    r = random.Random(2)
    for i in range(34):
        s += coin(1140 + r.uniform(-230, 230), 470 + r.uniform(-60, 30) - (abs(r.gauss(0, 1)) * 40), r.uniform(34, 46), 0.42, i)
    for i, (x, y) in enumerate([(1480, 900), (1560, 1000), (1420, 1060)]):
        s += coin(x, y, 40, 0.5, 50 + i)
    s += '<g filter="url(#blur2)">' + ''.join(f'<circle cx="{r.uniform(900,1400):.0f}" cy="{r.uniform(380,500):.0f}" r="{r.uniform(3,8):.0f}" fill="#fff0b0" opacity="0.8"/>' for _ in range(25)) + '</g>'
    return svg(bg, s)

@art
def coins_reach():
    """Anselmo's bare trembling hand reaching toward the glowing bag held by the gloved hand."""
    bg = sky('#04070d', '#18222f') + glow(1500, 600, 700, 'warm', 0.6)
    s = glove_hand(1650, 760, 1.4, -4)
    s += (f'<path d="M1440,700 Q1400,540 1500,450 L1820,450 Q1920,540 1880,700 Q1660,780 1440,700 Z" fill="#3b2514"/>'
          f'<path d="M1500,450 Q1660,490 1820,450" stroke="#c9a46a" stroke-width="8" fill="none"/>')
    r = random.Random(5)
    for i in range(22): s += coin(1660 + r.uniform(-150, 150), 450 + r.uniform(-40, 20), r.uniform(26, 34), 0.42, i)
    s += '<ellipse cx="1660" cy="450" rx="180" ry="50" fill="#ffcf5a" opacity="0.6" filter="url(#blur3)"/>'
    # bare hand (campesino, manta sleeve) from the left
    hand = ('<path d="M-200,820 L380,700 Q470,680 560,690 L700,700 Q740,705 738,730 Q734,752 700,750 L600,744 '
            'Q640,760 760,762 Q796,766 794,792 Q790,816 756,814 L620,806 Q650,826 740,834 Q772,840 768,866 Q762,888 730,884 L600,870 '
            'Q620,890 680,900 Q706,908 700,930 Q692,950 664,944 L540,920 Q440,930 380,920 L-200,1000 Z"/>')
    s += lit(hand, '#ffd08a', top="#8a6448", base="#5a3e2a", bot="#2a1a10", y0=680, y1=1000, off=(3, 7), halo=0.25, outline="#120a05")
    s += lit('<path d="M-200,780 L300,690 Q330,800 300,940 L-200,1040 Z"/>', '#ffd08a', top="#d8d2c4", base="#9a948a", bot="#4a4640", y0=680, y1=1040, halo=0.2)
    s += '<path d="M560,740 Q600,760 640,770 M600,810 Q640,820 680,830" stroke="#2a1a10" stroke-width="4" fill="none" opacity="0.7"/>'
    return svg(bg, s)

@art
def coins_ash():
    bg = '<rect width="2400" height="1350" fill="#1a1715"/>' + sky('#2a2420', '#14110f', y0=0, y1=1350)
    bg += f'<circle cx="1800" cy="-100" r="1200" fill="url(#warmglow)" opacity="0.35"/>'
    r = random.Random(9)
    for i in range(160):
        bg += f'<ellipse cx="{r.uniform(0,2400):.0f}" cy="{r.uniform(0,1350):.0f}" rx="{r.uniform(4,26):.0f}" ry="{r.uniform(3,12):.0f}" fill="{r.choice(["#0e0c0b","#2b2522","#3a332e"])}" opacity="0.7"/>'
    s = ''
    for i in range(26):
        x = r.uniform(300, 2100); y = r.uniform(300, 1150); ash = min(1.0, max(0.0, (x - 700) / 900))
        s += coin(x, y, r.uniform(48, 64), 0.5, i, ash)
        if ash > 0.3:
            s += f'<ellipse cx="{f(x)}" cy="{f(y-60)}" rx="40" ry="90" fill="#9a9590" opacity="{0.15*ash:.2f}" filter="url(#blur3)"/>'
    s += '<g filter="url(#blur2)">' + ''.join(f'<circle cx="{r.uniform(1100,2200):.0f}" cy="{r.uniform(200,1200):.0f}" r="{r.uniform(2,6):.0f}" fill="#ff8a3a" opacity="{r.uniform(0.3,0.8):.2f}"/>' for _ in range(30)) + '</g>'
    return svg(bg, s)

# ------------------------------------------------------------------ village & cantina
def quinque(x, y, s=1.0):
    return (glow(x, y + 40 * s, 260 * s, 'warm', 0.9) + f'<path d="M{x},{y-120*s} L{x},{y-30*s}" stroke="#120a05" stroke-width="{4*s}"/>'
            f'<path d="M{x-28*s},{y-30*s} L{x+28*s},{y-30*s} L{x+18*s},{y} L{x-18*s},{y} Z" fill="#1a1008"/>'
            f'<ellipse cx="{x}" cy="{y+30*s}" rx="{22*s}" ry="{34*s}" fill="#ffe2a0" opacity="0.85"/><ellipse cx="{x}" cy="{y+40*s}" rx="{8*s}" ry="{14*s}" fill="#fff8e0"/>'
            f'<path d="M{x-30*s},{y+66*s} L{x+30*s},{y+66*s} L{x+20*s},{y+90*s} L{x-20*s},{y+90*s} Z" fill="#1a1008"/>')

def seated_man(x, y, s=1.0, facing=1, rim="#ffb060", hat="palma", color_top="#2a1a10"):
    """seated man at a table, waist up, profile. (x,y) = seat/waist point."""
    sh = ('<path d="M-70,0 Q-80,-120 -60,-220 Q-30,-270 20,-268 Q66,-250 72,-200 Q80,-100 70,0 Z"/>'
          '<path d="M-28,-300 Q-36,-250 -20,-226 L22,-222 Q40,-232 44,-260 L58,-272 L46,-282 Q48,-312 24,-326 Q-14,-340 -28,-300 Z"/>'
          '<path d="M30,-220 Q90,-150 150,-110 L170,-80 Q120,-70 30,-140 Z"/>')
    if hat == "palma":
        sh += '<path d="M-180,-318 Q-80,-345 30,-345 Q140,-345 220,-318 Q130,-304 30,-306 Q-80,-304 -180,-318 Z"/><path d="M-30,-334 Q-30,-405 26,-412 Q80,-405 82,-334 Z"/>'
    return f'<g transform="translate({x},{y}) scale({s*facing},{s})">' + lit(sh, rim, top="#3a2416", base="#140c07", bot="#080503", y0=-420, y1=0, off=(5, 6), halo=0.3) + '</g>'

@art
def cantina_ext():
    s = sky('#060a14', '#1e2c3e') + stars(120, 5, 500) + moon(400, 220, 70)
    s += ridge(760, 80, '#0c1520', 2)
    s += '<rect x="0" y="1000" width="2400" height="350" fill="#16171a"/>'
    s += adobe_house(-60, 1010, 560, 380, '#0d1219', False, True)
    s += adobe_house(1820, 1010, 640, 400, '#0d1219', False, False)
    # cantina facade
    s += '<rect x="520" y="480" width="1300" height="540" fill="#1a1612"/><rect x="500" y="460" width="1340" height="40" fill="#0e0c0a"/>'
    s += glow(1170, 820, 520, 'warm', 0.9)
    s += '<rect x="1040" y="640" width="260" height="380" fill="#ffc865"/><rect x="1040" y="640" width="260" height="380" fill="url(#warmglow)"/>'
    s += '<path d="M1040,720 L1165,720 L1165,930 L1040,930 Z M1175,720 L1300,720 L1300,930 L1175,930 Z" fill="#3a2010"/>'
    for k in range(6):
        s += f'<rect x="{1050+k*20}" y="735" width="8" height="180" fill="#21130a"/><rect x="{1185+k*20}" y="735" width="8" height="180" fill="#21130a"/>'
    s += window(680, 650, 160, 220, True, False) + window(1500, 650, 160, 220, True, False)
    s += '<rect x="760" y="520" width="820" height="100" fill="#2a1a12" stroke="#c9a46a" stroke-width="4"/>'
    s += '<text x="1170" y="592" text-anchor="middle" font-family="Rye" font-size="66" fill="#e8c88a">CANTINA EL OLVIDO</text>'
    s += papel_picado(380, '#b3122e', 7, 4, 0.55)
    s += lamp(450, 1020, 360)
    # tied horse (ordinary horse, no fire)
    s += place(horse('walk', rim='#ffb060', seed=8, saddle=True, steam=False, eye=False), 1900, 1060, 0.55, flip=True)
    s += f'<rect x="1600" y="900" width="14" height="120" fill="#0b0805"/><rect x="1590" y="905" width="260" height="10" fill="#0b0805"/>'
    s += '<rect x="0" y="1010" width="2400" height="12" fill="#0a0a0c"/>'
    s += f'<g transform="translate(0,0)">{place(campesino("walk", "#ffb060"), 1020, 1150, 0.42)}</g>'
    return svg(s)

@art
def cantina_int():
    s = '<rect width="2400" height="1350" fill="#140c07"/>'
    s += '<rect x="0" y="0" width="2400" height="900" fill="#24160c"/>'
    for i in range(14):  # wall planks
        s += f'<rect x="{i*175}" y="0" width="6" height="900" fill="#1a0f08"/>'
    # shelves with bottles
    r = random.Random(3)
    for row, y in enumerate((300, 470)):
        s += f'<rect x="1400" y="{y}" width="900" height="16" fill="#120a05"/>'
        for k in range(16):
            x = 1420 + k * 54 + r.uniform(-6, 6); h = r.uniform(70, 120); c = r.choice(['#3c5a2a', '#5a3a1a', '#7a6a4a', '#2a3a3a'])
            s += f'<rect x="{f(x)}" y="{f(y-h)}" width="30" height="{f(h)}" rx="6" fill="{c}" opacity="0.85"/><rect x="{f(x+10)}" y="{f(y-h-30)}" width="10" height="34" fill="{c}"/><rect x="{f(x+4)}" y="{f(y-h+10)}" width="5" height="{f(h-20)}" fill="#ffe0a0" opacity="0.25"/>'
    # bar counter
    s += '<rect x="1300" y="720" width="1100" height="80" fill="#3a2414"/><rect x="1300" y="800" width="1100" height="550" fill="#22140a"/>'
    for k in range(7): s += f'<rect x="{1340+k*150}" y="830" width="110" height="420" fill="none" stroke="#120a05" stroke-width="6"/>'
    s += '<rect x="0" y="900" width="1300" height="450" fill="#1a0f08"/>'
    s += quinque(500, 140, 1.3) + quinque(1250, 120, 1.1) + quinque(1950, 140, 1.2)
    # tables + men silhouettes
    s += '<ellipse cx="520" cy="1030" rx="320" ry="40" fill="#2e1c0e"/><rect x="505" y="1040" width="30" height="300" fill="#140c07"/>'
    s += seated_man(300, 1040, 1.25, 1) + seated_man(760, 1040, 1.2, -1)
    s += seated_man(1650, 760, 1.0, 1, hat="palma") + seated_man(2050, 760, 1.05, -1)
    # guitarist in the corner
    s += seated_man(120, 820, 0.9, 1)
    s += '<g transform="translate(200,760) rotate(-25)"><ellipse cx="0" cy="0" rx="70" ry="56" fill="#5a3418"/><ellipse cx="-60" cy="10" rx="50" ry="44" fill="#5a3418"/><rect x="40" y="-8" width="200" height="16" fill="#2a160a"/><circle cx="-20" cy="0" r="16" fill="#140a04"/></g>'
    s += '<g opacity="0.25" filter="url(#blur3)"><ellipse cx="900" cy="350" rx="700" ry="120" fill="#d8c0a0"/><ellipse cx="1600" cy="200" rx="600" ry="90" fill="#d8c0a0"/></g>'
    return svg(s)

@art
def anselmo_table():
    s = '<rect width="2400" height="1350" fill="#120a06"/>' + glow(1300, 700, 900, 'warm', 0.75)
    s += '<rect x="0" y="0" width="2400" height="760" fill="#1e120a" opacity="0.8"/>'
    s += '<path d="M200,880 L2400,820 L2400,1350 L0,1350 L0,900 Z" fill="#3a2414"/><path d="M200,880 L2400,820" stroke="#5a3a20" stroke-width="6"/>'
    r = random.Random(2)
    for i in range(10): s += f'<path d="M0,{960+i*40} L2400,{900+i*44}" stroke="#2a180c" stroke-width="3" opacity="0.6"/>'
    # mezcal bottle + glasses + candle
    s += '<path d="M1500,860 L1500,560 Q1500,520 1530,500 L1530,420 L1570,420 L1570,500 Q1600,520 1600,560 L1600,860 Z" fill="#4a5a2a" opacity="0.9"/><rect x="1512" y="600" width="16" height="230" fill="#e8f0c0" opacity="0.3"/>'
    s += '<rect x="1505" y="640" width="90" height="120" fill="#d8c08a" opacity="0.8"/><text x="1550" y="710" text-anchor="middle" font-family="Rye" font-size="26" fill="#3a2010">MEZCAL</text>'
    for x in (1700, 1820, 1380):
        s += f'<path d="M{x},870 L{x+8},790 L{x+62},790 L{x+70},870 Z" fill="#cfe0e0" opacity="0.35"/><path d="M{x+6},850 L{x+10},820 L{x+60},820 L{x+64},850 Z" fill="#e8c070" opacity="0.6"/>'
    s += candle(1980, 860, 110, 26)
    s += seated_man(700, 1250, 2.1, 1, rim="#ffb060")
    # his hand gripping the glass
    s += '<ellipse cx="1370" cy="840" rx="46" ry="34" fill="#1a0f08"/>'
    return svg(s)

def face_profile(x, y, s=1.0, facing=1, rim="#ffb060", skin_top="#8a5a3a", old=False, scared=False, hat=True, white=False):
    """Detailed head & shoulders profile. (x,y)=chin-ish anchor. Local units ~ head 300 tall."""
    head = ('M-120,-80 Q-150,-220 -80,-300 Q0,-360 90,-320 Q140,-290 150,-230 Q154,-200 170,-170 Q190,-140 176,-126 '
            'Q164,-118 168,-104 Q176,-90 162,-80 Q170,-60 156,-46 Q150,-20 120,-10 Q90,0 60,10 Q0,30 -40,20 Q-100,0 -120,-80 Z')
    neck = 'M-70,0 Q-60,80 -90,160 L140,160 Q90,90 80,10 Z'
    shoulders = 'M-300,160 Q-200,110 -60,120 L120,120 Q260,130 340,200 L340,360 L-300,360 Z'
    sh = f'<path d="{shoulders}"/><path d="{neck}"/><path d="{head}"/>'
    ear = '<path d="M-30,-170 Q-60,-190 -60,-140 Q-58,-100 -26,-110 Z"/>'
    hatp = ''
    if hat:
        hatp = ('<path d="M-360,-290 Q-120,-360 120,-350 Q330,-340 420,-280 Q300,-260 100,-262 Q-150,-262 -360,-290 Z"/>'
                '<path d="M-110,-300 Q-120,-460 10,-480 Q130,-470 140,-300 Z"/>')
    g = lit(sh + ear + hatp, rim, top=skin_top, base="#2a1a12", bot="#0c0806", y0=-480, y1=360, off=(-9 if facing > 0 else 9, 6), halo=0.3, outline="#050302")
    det = ''
    # eye
    if scared:
        det += '<ellipse cx="95" cy="-205" rx="22" ry="16" fill="#e8e2d8"/><circle cx="104" cy="-205" r="8" fill="#140c08"/><path d="M68,-232 Q100,-250 126,-228" stroke="#120a06" stroke-width="7" fill="none"/>'
        det += '<path d="M150,-60 Q140,-40 120,-44" stroke="#120a06" stroke-width="6" fill="none"/>'
        det += '<path d="M40,-260 q8,30 0,52" stroke="#d8e8f0" stroke-width="5" fill="none" opacity="0.7"/><ellipse cx="42" cy="-200" rx="6" ry="9" fill="#d8e8f0" opacity="0.8"/>'
    else:
        det += '<path d="M80,-205 Q100,-215 122,-205 Q100,-196 80,-205 Z" fill="#100906"/><path d="M72,-228 Q100,-240 126,-226" stroke="#120a06" stroke-width="8" fill="none"/>'
    if old:
        det += ('<path d="M120,-60 Q60,-50 40,-10 Q60,-30 100,-36 Q130,-40 150,-60 Z" fill="#d8d4cc"/>'
                '<path d="M60,-130 Q40,-100 50,-70 M30,-250 Q60,-262 90,-255 M20,-150 Q10,-120 20,-90 M70,-160 Q60,-150 74,-140" stroke="#120a06" stroke-width="4" fill="none" opacity="0.8"/>'
                '<path d="M-80,-280 Q-120,-240 -125,-180" stroke="#cfcac2" stroke-width="10" fill="none" opacity="0.7"/>')
    else:
        det += '<path d="M120,-62 Q90,-58 70,-40 Q100,-48 140,-60 Z" fill="#100906"/>'
    if white:
        det += '<path d="M-110,-290 Q-150,-220 -130,-150 Q-110,-200 -60,-250 Z" fill="#e0e4e8"/>'
    det += '<path d="M-60,-140 Q-20,-110 20,-60" stroke="#120a06" stroke-width="3" fill="none" opacity="0.5"/>'
    return f'<g transform="translate({x},{y}) scale({s*facing},{s})">{g}{det}</g>'

def face2(x, y, s=1.0, rim="#ffb060", rim2=None, skin=("#8a5a3e", "#4a2e20", "#1a0e08"), old=False, scared=False, hat=True,
          white=False, sarape=True, light_from=1):
    """Detailed head-and-shoulders profile facing right. (x,y) = chin base. light_from: 1 = key light from the face side."""
    P = [(-100, -300), (0, -345), (90, -322), (126, -272), (142, -228), (133, -206), (160, -170), (184, -140), (190, -126),
         (178, -117), (162, -116), (160, -104), (170, -92), (160, -82), (166, -70), (150, -58), (162, -36), (150, -8),
         (110, 2), (64, 4), (20, -30), (-20, -70), (-60, -100), (-110, -150), (-126, -230)]
    head = spline(P, True, 0.85)
    neck = 'M-70,-90 Q-76,10 -100,80 L110,80 Q84,40 84,24 Q90,10 70,0 Z'
    shoulders = 'M-420,110 Q-260,50 -100,58 L110,58 Q300,70 430,170 L470,420 L-460,420 Z'
    ear = 'M-8,-188 Q-40,-196 -42,-150 Q-40,-104 -6,-110 Q-20,-150 -8,-188 Z'
    out = ''
    out += lit(f'<path d="{shoulders}"/>', rim, top="#d8d4c8" if not old else "#cfc8b8", base="#8a867c", bot="#3a3630", y0=50, y1=420, off=(-8*light_from, 6), halo=0.25, outline="#050302")
    if sarape:
        sar = 'M-420,140 Q-250,60 -60,90 Q60,120 140,240 L170,420 L-200,420 Q-300,320 -420,200 Z'
        out += lit(f'<path d="{sar}"/>', rim, top="#7a3426", base="#4a1c16", bot="#200c0a", y0=120, y1=420, off=(-8*light_from, 6), halo=0)
        for k in range(5):
            out += f'<path d="M{-400+k*20},{170+k*36} Q{-120},{110+k*40} {120-k*10},{240+k*30}" stroke="#d8a85a" stroke-width="7" fill="none" opacity="0.55"/>'
    out += lit(f'<path d="{neck}"/><path d="{head}"/><path d="{ear}"/>', rim, top=skin[0], base=skin[1], bot=skin[2], y0=-350, y1=150, off=(-9*light_from, 5), halo=0.3, outline="#050302")
    det = ''
    det += '<path d="M-14,-176 Q-30,-150 -16,-122" stroke="#1a0c06" stroke-width="5" fill="none" opacity="0.7"/>'
    det += '<path d="M-60,-100 Q-40,-60 -2,-40 Q40,-18 70,0" stroke="#000" stroke-width="10" fill="none" opacity="0.25"/>'
    det += '<path d="M150,-118 Q140,-140 120,-150" stroke="#000" stroke-width="5" fill="none" opacity="0.35"/>'
    det += '<path d="M156,-80 L140,-82" stroke="#1a0a06" stroke-width="5" stroke-linecap="round"/>'
    if scared:
        det += '<path d="M86,-212 Q112,-232 136,-210 Q112,-190 86,-212 Z" fill="#ece6da"/><circle cx="120" cy="-211" r="9" fill="#120804"/><circle cx="123" cy="-214" r="3" fill="#fff"/>'
        det += '<path d="M78,-236 Q110,-258 140,-240" stroke="#120804" stroke-width="8" fill="none" stroke-linecap="round"/>'
        det += '<path d="M60,-262 q10,34 2,58" stroke="#cfe2ee" stroke-width="5" fill="none" opacity="0.75"/><ellipse cx="63" cy="-200" rx="7" ry="10" fill="#cfe2ee" opacity="0.85"/>'
        det += '<path d="M150,-82 Q156,-74 150,-66" stroke="#120804" stroke-width="4" fill="none"/>'
    else:
        det += '<path d="M92,-210 Q114,-222 134,-208 Q114,-200 92,-210 Z" fill="#100804"/><path d="M84,-230 Q110,-246 140,-232" stroke="#120804" stroke-width="9" fill="none" stroke-linecap="round"/>'
    if old:
        det += '<path d="M170,-96 Q120,-92 92,-50 Q118,-70 150,-74 Q172,-80 176,-96 Z" fill="#e2ded6"/>'
        det += ''.join(f'<path d="{d}" stroke="#120804" stroke-width="4" fill="none" opacity="0.75"/>' for d in
                       ('M60,-150 Q44,-110 54,-74', 'M40,-262 Q76,-276 110,-268', 'M44,-286 Q80,-300 116,-290', 'M76,-180 Q64,-170 78,-160', 'M100,-186 Q92,-176 106,-170', 'M20,-120 Q10,-90 24,-60'))
        det += '<path d="M-96,-160 Q-130,-200 -120,-250" stroke="#d8d4cc" stroke-width="14" fill="none" opacity="0.8"/>'
    if white:
        det += ''.join(f'<path d="M{-112+k*6},{-150-k*4} Q{-140+k*8},{-240} {-60+k*14},{-332+k*6}" stroke="#e6e8ea" stroke-width="7" fill="none" opacity="0.8"/>' for k in range(6))
    if rim2:
        front = spline(P[3:18], False, 0.85)
        det += f'<path d="{front}" stroke="{rim2}" stroke-width="7" fill="none" opacity="0.8" filter="url(#blur1)"/>'
    hatp = ''
    if hat:
        brim = 'M-360,-262 Q-120,-322 140,-318 Q360,-310 430,-262 Q340,-238 140,-244 Q-120,-240 -360,-262 Z'
        crown = 'M-120,-296 Q-130,-440 10,-458 Q150,-446 160,-300 Q20,-286 -120,-296 Z'
        hatp = lit(f'<path d="{brim}"/><path d="{crown}"/>', rim, top="#a8884e", base="#6a5030", bot="#2a1e10", y0=-460, y1=-240, off=(-6*light_from, 5), halo=0.25, outline="#0a0603")
        for k in range(14):
            xx = -320 + k * 52
            hatp += f'<path d="M{xx},-282 L{xx+26},-298" stroke="#3a2a14" stroke-width="3" opacity="0.6"/>'
        for k in range(6):
            hatp += f'<path d="M{-110+k*8},{-310-k*24} Q{20},{-326-k*26} {150-k*8},{-312-k*24}" stroke="#3a2a14" stroke-width="3" fill="none" opacity="0.5"/>'
        hatp += '<path d="M-122,-300 Q20,-284 160,-304" stroke="#2a1a0a" stroke-width="14" fill="none"/>'
        hatp += '<path d="M-200,-250 Q20,-232 300,-246" stroke="#000" stroke-width="40" fill="none" opacity="0.35" filter="url(#blur2)"/>'
    return f'<g transform="translate({x},{y}) scale({s})">{out}{det}{hatp}</g>'

@art
def oldman():
    s = '<rect width="2400" height="1350" fill="#0e0805"/>' + glow(1500, 620, 900, 'warm', 0.8)
    s += quinque(1900, 60, 1.3)
    s += face2(1050, 900, 1.6, rim="#ffb060", skin=("#a87850", "#5a3824", "#1a0e08"), old=True, sarape=False)
    s += '<rect x="0" y="1180" width="2400" height="170" fill="#2e1c0e"/>'
    s += candle(1700, 1200, 100, 24)
    return svg(s)

@art
def black_hand():
    s = '<rect width="2400" height="1350" fill="#120a06"/>' + glow(1500, 400, 900, 'warm', 0.7) + candle(1950, 900, 140, 30)
    s += '<path d="M0,900 L2400,860 L2400,1350 L0,1350 Z" fill="#3a2414"/>'
    for i in range(8): s += f'<path d="M0,{950+i*50} L2400,{910+i*55}" stroke="#2a180c" stroke-width="3" opacity="0.6"/>'
    hand = ('<path d="M-300,780 Q100,700 520,700 Q640,690 760,700 L1020,690 Q1070,690 1068,722 Q1062,750 1020,750 L860,752 '
            'Q900,770 1080,772 Q1130,774 1126,808 Q1120,838 1074,834 L880,826 Q920,846 1060,852 Q1104,858 1098,890 Q1090,918 1048,912 L860,896 '
            'Q890,916 960,928 Q996,936 988,962 Q978,986 940,980 L760,956 Q600,990 480,960 L-300,1000 Z"/>')
    s += lit(hand, '#ffb060', top="#4a3a30", base="#141110", bot="#060505", y0=680, y1=1000, off=(4, 8), halo=0.2, outline="#000")
    r = random.Random(6)
    for i in range(40):
        x = r.uniform(400, 1040); y = r.uniform(710, 960)
        s += f'<path d="M{f(x)},{f(y)} l{r.uniform(-30,30):.0f},{r.uniform(-14,14):.0f} l{r.uniform(-20,20):.0f},{r.uniform(-10,10):.0f}" stroke="#7a6a60" stroke-width="2" fill="none" opacity="0.55"/>'
    for i in range(10):
        x = r.uniform(500, 1000); y = r.uniform(720, 940)
        s += f'<circle cx="{f(x)}" cy="{f(y)}" r="3" fill="#ff7a2a" opacity="0.5" filter="url(#blur1)"/>'
    s += lit('<path d="M-300,740 L500,690 Q540,840 500,980 L-300,1060 Z"/>', '#ffb060', top="#cfc6b6", base="#8a8478", bot="#3a3630", y0=680, y1=1060, halo=0.2)
    return svg(s)

@art
def milpa():
    s = sky('#3a2a1a', '#c98a4a', mid='#8a5a30') + f'<circle cx="1800" cy="420" r="120" fill="#ffd8a0" opacity="0.9"/>' + glow(1800, 420, 600, 'warm', 0.6)
    s += ridge(820, 90, '#5a3a24', 3) + '<rect x="0" y="860" width="2400" height="490" fill="#6a4a30"/>'
    r = random.Random(4)
    for i in range(120):  # cracks
        x = r.uniform(0, 2400); y = r.uniform(900, 1350)
        s += f'<path d="M{f(x)},{f(y)} l{r.uniform(-60,60):.0f},{r.uniform(-10,20):.0f} l{r.uniform(-40,40):.0f},{r.uniform(-10,20):.0f}" stroke="#3a2614" stroke-width="3" fill="none"/>'
    for row in range(5):
        y0 = 880 + row * 110; sc = 0.5 + row * 0.35
        for k in range(int(26 - row * 3)):
            x = k * (2400 / (26 - row * 3)) + r.uniform(-20, 20) + row * 30
            h = 260 * sc
            s += f'<path d="M{f(x)},{f(y0)} Q{f(x+r.uniform(-15,15))},{f(y0-h*0.5)} {f(x+r.uniform(-30,30))},{f(y0-h)}" stroke="#3a2614" stroke-width="{4*sc:.1f}" fill="none"/>'
            for j in range(3):
                yy = y0 - h * (0.3 + j * 0.2); d = r.choice([-1, 1])
                s += f'<path d="M{f(x)},{f(yy)} Q{f(x+d*50*sc)},{f(yy-10*sc)} {f(x+d*70*sc)},{f(yy+60*sc)}" stroke="#4a3018" stroke-width="{3*sc:.1f}" fill="none"/>'
    s += place(campesino('stand', '#ffd8a0', sarape=False), 1500, 1000, 0.32)
    return svg(s)

@art
def anselmo_walk(): return svg(place(campesino('walk', MOONRIM), 1200, 1260, 0.95))
@art
def anselmo_walk_small(): return svg(place(campesino('walk', MOONRIM), 1250, 1060, 0.42))

@art
def anselmo_face():
    s = sky('#060a14', '#1a2638') + glow(2300, 700, 900, 'red', 0.55) + f'<circle cx="300" cy="300" r="600" fill="url(#moonglow)"/>'
    s += face2(980, 930, 1.75, rim=MOONRIM, rim2="#ff3a1a", skin=("#7a5a4a", "#3e2a22", "#120a08"), scared=True, light_from=1)
    return svg(s)

@art
def anselmo_old():
    s = '<rect width="2400" height="1350" fill="#0c0806"/>' + glow(700, 700, 700, 'warm', 0.7)
    # window open to night road
    s += '<rect x="1300" y="250" width="700" height="760" fill="#0a1424"/>'
    s += f'<g>{sky("#071020", "#1c2a40", y0=250, y1=1010)}</g>'
    s += '<g clip-path="url(#winclip)"></g>'
    s += moon(1820, 380, 50, halo=2.5) + '<path d="M1300,860 Q1600,820 2000,850 L2000,1010 L1300,1010 Z" fill="#05080e"/>'
    s += maguey(1450, 880, 90, 3, '#03050a') + maguey(1880, 870, 60, 5, '#03050a')
    s += '<rect x="1300" y="250" width="700" height="760" fill="none" stroke="#1a1008" stroke-width="40"/>'
    s += '<path d="M2000,250 L2260,190 L2260,1080 L2000,1010 Z" fill="#2a180c"/><path d="M2020,300 L2240,250 M2020,560 L2240,540 M2020,820 L2240,830" stroke="#140a04" stroke-width="12"/>'
    s += '<path d="M1300,250 L1100,200 L1100,1060 L1300,1010 Z" fill="#2a180c"/>'
    s += '<rect x="0" y="1060" width="2400" height="290" fill="#1a0f08"/>' + candle(600, 1100, 120, 28)
    s += face2(980, 1150, 1.2, rim="#ffb060", skin=("#a87a5a", "#5a3a28", "#1a0e08"), old=True, hat=False, white=True, sarape=False)
    return svg(s)

# ------------------------------------------------------------------ origin
def kneeling_man(x, y, s=1.0, rim="#ffd08a"):
    """young man kneeling, manta clothes dimly lit"""
    sh = ('<path d="M-60,-300 Q-80,-420 -40,-520 Q0,-560 50,-540 Q90,-500 80,-400 Q70,-320 60,-300 Z"/>'
          '<path d="M-70,-300 L90,-300 Q150,-260 200,-120 L200,0 L120,0 L120,-120 Q60,-200 -40,-200 Q-120,-150 -160,0 L-240,0 Q-200,-200 -70,-300 Z"/>'
          '<path d="M-20,-620 Q-28,-570 -14,-546 L26,-542 Q44,-552 48,-580 L60,-590 L48,-600 Q50,-632 26,-646 Q-12,-660 -20,-620 Z"/>'
          '<path d="M40,-500 Q120,-450 160,-380 L180,-360 Q120,-350 50,-420 Z"/>')
    return f'<g transform="translate({x},{y}) scale({s})">' + lit(sh, rim, top="#7a8088", base="#33373c", bot="#16181b", y0=-660, y1=0, off=(5, 6), halo=0.3) + '</g>'

@art
def crossroads():
    s = sky('#03050a', '#141c28', mid='#0a1018')
    s += cloud_band(200, '#1c2634', 1, 10, 0.9, 110) + cloud_band(420, '#121a26', 6, 9, 0.8, 80)
    s += '<path d="M1500,0 L1460,160 L1530,170 L1420,420 L1500,430 L1380,700" stroke="#e8f0ff" stroke-width="10" fill="none" filter="url(#glow)"/>'
    s += ridge(760, 110, '#0a0f17', 4) + '<rect x="0" y="800" width="2400" height="550" fill="#0b0e12"/>'
    s += '<path d="M0,1120 Q1200,980 2400,1100 L2400,1210 Q1200,1060 0,1240 Z" fill="#26252a"/>'
    s += '<path d="M1080,800 L1180,800 Q1260,1100 1560,1350 L760,1350 Q1000,1100 1080,800 Z" fill="#26252a"/>'
    s += '<rect x="1316" y="560" width="26" height="560" fill="#0a0806"/><rect x="1236" y="660" width="186" height="24" fill="#0a0806"/>'
    s += place(campesino('stand', '#ffd08a', sarape=False, tone=('#6a727c', '#3a4048', '#181c20')), 1080, 1190, 0.62)
    s += candle(1230, 1185, 50, 14)
    s += tree(500, 1000, 700, 8, '#05070a', 'bare', 0.1)
    return svg(s)

@art
def devil():
    sh = ('<path d="M-140,-1050 Q-170,-700 -230,-80 Q-120,-40 0,-50 Q120,-40 230,-80 Q170,-700 140,-1050 Q80,-1100 0,-1095 Q-80,-1100 -140,-1050 Z"/>'
          '<path d="M-50,-1160 Q-56,-1110 -40,-1085 Q0,-1068 40,-1085 Q56,-1110 50,-1160 Q30,-1200 0,-1200 Q-30,-1200 -50,-1160 Z"/>'
          '<path d="M-200,-1190 Q0,-1215 200,-1190 Q100,-1172 0,-1175 Q-100,-1172 -200,-1190 Z"/><path d="M-70,-1185 L-62,-1330 L62,-1330 L70,-1185 Z"/>'
          '<path d="M-62,-1300 Q-110,-1350 -100,-1420 Q-78,-1360 -48,-1330 Z"/><path d="M62,-1300 Q110,-1350 100,-1420 Q78,-1360 48,-1330 Z"/>'
          '<path d="M140,-1000 Q220,-800 240,-560 L262,-550 L258,-80 L244,-80 L236,-540 Q200,-760 120,-900 Z"/>'
          '<path d="M-90,-80 L-70,0 L-20,0 L-30,-80 Z M30,-80 L20,0 L70,0 L90,-80 Z"/>')
    body = lit(sh, '#ff4a2a', top="#2a0c0c", base="#0a0405", bot="#040202", y0=-1420, y1=0, off=(6, 8), halo=0.45, outline="#000")
    eyes = ''.join(f'<circle cx="{x}" cy="-1140" r="30" fill="url(#redglow)"/><ellipse cx="{x}" cy="-1140" rx="9" ry="5" fill="#ffcf6a"/>' for x in (-20, 20))
    smile = '<path d="M-26,-1110 Q0,-1096 26,-1110" stroke="#ff6a3a" stroke-width="3" fill="none" opacity="0.8"/>'
    chain = '<path d="M-40,-760 Q0,-720 40,-760" stroke="#c9a46a" stroke-width="5" fill="none"/>'
    return svg(place(body + eyes + smile + chain, 1250, 1320, 0.92))

@art
def boy_window():
    s = sky('#2a2018', '#4a3a28') + '<rect x="0" y="1000" width="2400" height="350" fill="#3a2c1e"/>'
    s += '<rect x="900" y="200" width="1500" height="820" fill="#5a4630"/>'
    s += '<rect x="1150" y="320" width="900" height="560" fill="#e8c88a"/>' + glow(1600, 600, 600, 'warm', 0.7)
    s += f'<g transform="translate(1600,640)">' + sombrero(0, 0, 640, 260, sil="#8a6a2a")[0].replace('<path ', '<path fill="#2a1a10" ') + sombrero(0, 0, 640, 260, sil="#e8c060")[1] + '</g>'
    s += '<rect x="1150" y="320" width="900" height="560" fill="none" stroke="#2a1a10" stroke-width="30"/><rect x="1590" y="320" width="20" height="560" fill="#2a1a10"/>'
    s += '<text x="1600" y="280" text-anchor="middle" font-family="Rye" font-size="70" fill="#2a1a10">SOMBRERERÍA</text>'
    s += place(campesino('stand', '#ffe0b0', sarape=False, hat=False), 700, 1180, 0.62, flip=False)
    s += adobe_house(-50, 1010, 500, 330, '#4a3826', False, False, '#3a2c1e')
    return svg(s)

@art
def hacienda_party():
    s = sky('#0a0810', '#2a1a18') + stars(60, 3, 300)
    s += '<rect x="0" y="380" width="2400" height="700" fill="#2a1c14"/>'
    for i in range(7):
        x = 60 + i * 340
        s += f'<path d="M{x},1080 L{x},640 A150,150 0 0 1 {x+300},640 L{x+300},1080 Z" fill="#3a2414"/>'
        s += f'<path d="M{x+20},1080 L{x+20},650 A130,130 0 0 1 {x+280},650 L{x+280},1080 Z" fill="#ffb860" opacity="0.55"/>'
        s += glow(x + 150, 700, 260, 'warm', 0.8)
    s += '<rect x="0" y="1080" width="2400" height="270" fill="#4a3018"/>'
    s += papel_picado(140, '#b3122e', 9, 3, 0.9) + papel_picado(330, '#e7a21b', 8, 5, 0.8)
    for i, x in enumerate([300, 620, 1700, 2050, 2250]):
        s += figure(x, 1250, 430 + (i % 2) * 40, hat='sombrero' if i % 2 == 0 else None, dress='trousers' if i % 2 == 0 else 'skirt', pose=['walk', 'arms_up', 'walk', 'arms_up', 'stand'][i], rim='#ffb860', facing=1 if i % 2 else -1)
    s += place(charro_front_(rim='#ffcc80', eyes=None, bag=False, cape=False), 1200, 1300, 0.88)
    return svg(s)

@art
def hacienda_crosses():
    s = sky('#040810', '#1a2638') + stars(140, 8, 600) + moon(1950, 230, 80)
    s += ridge(760, 100, '#0a121c', 5) + '<rect x="0" y="900" width="2400" height="450" fill="#0b1018"/>'
    s += '<rect x="500" y="520" width="1100" height="400" fill="#121a24"/><rect x="480" y="500" width="1140" height="30" fill="#0a0f16"/>'
    for i in range(6): s += f'<path d="M{560+i*175},920 L{560+i*175},740 A55,55 0 0 1 {670+i*175},740 L{670+i*175},920 Z" fill="#080c12"/>'
    s += window(760, 600, 70, 100, True) + window(1300, 600, 70, 100, False)
    s += church(1900, 920, 0.55, '#0e151f', True)
    r = random.Random(3)
    for i in range(46):
        x = r.uniform(0, 2400); y = r.uniform(930, 1340); k = 0.5 + (y - 900) / 450 * 1.6
        s += f'<rect x="{f(x-4*k)}" y="{f(y-90*k)}" width="{f(8*k)}" height="{f(90*k)}" fill="#05080c"/><rect x="{f(x-26*k)}" y="{f(y-70*k)}" width="{f(52*k)}" height="{f(7*k)}" fill="#05080c"/>'
    for x in (300, 2200):
        s += f'<rect x="{x-10}" y="560" width="20" height="360" fill="#05080c"/><rect x="{x-70}" y="620" width="140" height="18" fill="#05080c"/>'
    return svg(s)

@art
def gamble():
    s = '<rect width="2400" height="1350" fill="#0c0705"/>' + glow(1200, 600, 1000, 'warm', 0.6)
    s += '<rect x="0" y="0" width="2400" height="820" fill="#1a0e09" opacity="0.6"/>'
    s += place(charro_front_(rim="#ffb060", eyes=None, bag=False, cape=False, upper=True), 1200, 1330, 0.95)
    s += '<path d="M0,820 L2400,820 L2400,1350 L0,1350 Z" fill="#3a1a12"/><path d="M0,820 L2400,820" stroke="#6a3a1a" stroke-width="8"/>'
    for x in (400, 820, 1580, 2000): s += candle(x, 860, 160 if x % 2 else 120, 26)
    r = random.Random(4)
    for i in range(12):
        x = r.choice([r.uniform(150, 900), r.uniform(1500, 2250)]); y = r.uniform(900, 1300)
        s += f'<g transform="translate({f(x)},{f(y)}) rotate({r.uniform(-40,40):.0f}) scale(1,0.6)"><rect x="-55" y="-80" width="110" height="160" rx="10" fill="#efe6d4"/><rect x="-45" y="-70" width="90" height="140" rx="6" fill="none" stroke="#b3122e" stroke-width="3"/><circle r="18" fill="{r.choice(["#b3122e","#1a1a1a","#c9a46a"])}"/></g>'
    for i in range(36): s += coin(r.uniform(500, 1900), r.uniform(900, 1300), 34, 0.45, i)
    s += '<path d="M1640,860 L1660,740 Q1660,660 1700,640 L1700,560 L1760,560 L1760,640 Q1800,660 1800,740 L1820,860 Z" fill="#4a0e14" opacity="0.9"/>'
    s += '<path d="M680,860 L690,800 L740,730 L670,730 Q650,680 715,670 Q780,680 760,730 L690,800 Z" fill="#7a1420" opacity="0.6"/>'
    return svg(s)

# ------------------------------------------------------------------ variants
@art
def malinche():
    s = sky('#050912', '#1a2a3c') + stars(180, 11, 700) + moon(600, 230, 70)
    s += '<path d="M0,900 Q500,850 800,700 Q1050,420 1250,380 Q1330,370 1400,390 Q1650,450 1900,700 Q2150,860 2400,880 L2400,1350 L0,1350 Z" fill="#0e1826"/>'
    s += '<path d="M1250,380 Q1300,420 1400,390 Q1360,470 1300,450 Q1270,500 1220,430 Z" fill="#26364a"/>'
    s += '<path d="M0,1000 Q600,940 1200,980 Q1800,1020 2400,960 L2400,1350 L0,1350 Z" fill="#070c14"/>'
    s += glow(1560, 760, 260, 'warm', 0.95) + '<path d="M1500,800 Q1560,700 1620,800 Z" fill="#ffcf6a"/>'
    s += '<path d="M600,1150 Q900,1000 1200,920 Q1400,860 1540,800" stroke="#1c2836" stroke-width="12" fill="none" stroke-dasharray="30 18"/>'
    for i, (x, y, k) in enumerate([(1180, 930, 0.16), (1060, 975, 0.19), (930, 1030, 0.22)]):
        s += place(horse('walk', rim='#7f9fc3', seed=i + 20, saddle=False, steam=False, eye=False), x, y, k)
        s += place(campesino('walk', '#7f9fc3', sarape=True), x + 150 * k, y + 5, k * 0.95)
    s += tree(250, 1100, 500, 3, '#04070b', 'bare')
    return svg(s)

@art
def cave_gold():
    s = '<rect width="2400" height="1350" fill="#0c0806"/>' + glow(1200, 760, 900, 'warm', 0.9)
    r = random.Random(3)
    for i in range(80):
        x = 1200 + r.uniform(-600, 600); y = 900 + r.uniform(-120, 120) * (1 - abs(x - 1200) / 700)
        s += coin(x, y, r.uniform(26, 40), 0.4, i)
    s += '<ellipse cx="1200" cy="900" rx="600" ry="120" fill="#ffcf5a" opacity="0.25" filter="url(#blur3)"/>'
    for i in range(5):
        x = 800 + i * 200
        s += f'<path d="M{x},960 L{x+20},840 L{x+120},840 L{x+140},960 Z" fill="#5a3a14" stroke="#c9a46a" stroke-width="4"/>'
    s += '<path d="M0,0 L2400,0 L2400,1350 L2000,1350 Q2200,800 1900,400 Q1600,180 1200,170 Q800,180 500,400 Q200,800 400,1350 L0,1350 Z" fill="#070504"/>'
    s += '<path d="M400,1350 Q200,800 500,400 Q800,180 1200,170 Q1600,180 1900,400 Q2200,800 2000,1350" stroke="#3a2210" stroke-width="16" fill="none" opacity="0.8"/>'
    s += '<g transform="translate(700,1180) rotate(-12)"><ellipse rx="200" ry="40" fill="#3a2a16"/><path d="M-60,-10 Q-60,-90 0,-96 Q60,-90 60,-10 Z" fill="#3a2a16"/></g>'
    return svg(s)

@art
def toluca():
    s = sky('#0a1220', '#5a6a80', mid='#2a3a52') + stars(60, 2, 300)
    s += '<path d="M200,900 Q700,700 1000,420 Q1080,360 1160,380 Q1220,350 1300,400 Q1380,360 1460,410 Q1800,700 2300,900 Z" fill="#1c2838"/>'
    s += '<path d="M1000,420 Q1080,360 1160,380 Q1220,350 1300,400 Q1380,360 1460,410 Q1520,470 1420,470 Q1380,520 1300,470 Q1200,540 1140,470 Q1060,500 1000,420 Z" fill="#dfe8f0"/>'
    s += '<rect x="0" y="880" width="2400" height="470" fill="#121a24"/>'
    s += church(1600, 1000, 0.32, '#0a1018', True)
    for i, x in enumerate([200, 600, 900, 1900, 2150]):
        s += adobe_house(x, 1010 + (i % 2) * 20, 220, 130, '#0a1018', False, i % 2 == 0)
    s += cloud_band(820, '#9aaabb', 3, 10, 0.25, 40)
    return svg(s)

@art
def bridge():
    s = sky('#050a12', '#1c2c3a') + moon(1800, 260, 90) + stars(100, 7, 500)
    s += ridge(780, 100, '#0c1620', 3)
    s += water(980, 1350, '#1a2c3a', '#060a10') + reflection(1800, 985, 1350, width=160)
    s += '<path d="M0,760 L2400,760 L2400,830 L0,830 Z" fill="#141c26"/>'
    for i in range(4):
        x = 150 + i * 560
        s += f'<path d="M{x},830 L{x+520},830 L{x+520},1020 Q{x+260},760 {x},1020 Z" fill="#141c26" stroke="#2a3644" stroke-width="3"/>'
    s += '<rect x="0" y="730" width="2400" height="30" fill="#1c2632"/>'
    for i in range(50): s += f'<rect x="{i*48}" y="742" width="44" height="18" fill="none" stroke="#0c121a" stroke-width="2"/>'
    for x in (90, 2330):
        s += f'<path d="M{x},760 Q{x+20},500 {x-10},300" stroke="#03060a" stroke-width="22" fill="none"/>'
        for k in range(7):
            a = -2.8 + k * 0.45
            s += f'<path d="M{x-10},300 Q{x-10+math.cos(a)*120},{300+math.sin(a)*90} {x-10+math.cos(a)*230},{300+math.sin(a)*40+80}" stroke="#03060a" stroke-width="12" fill="none"/>'
    s += place(horse_and_rider('walk', MOONRIM, 3, steam=False), 1100, 735, 0.28)
    return svg(s)

@art
def cashbox():
    s = '<rect width="2400" height="1350" fill="#0e0805"/>' + glow(1300, 300, 900, 'warm', 0.8) + quinque(1300, 40, 1.2)
    s += '<path d="M300,500 L2100,500 L2300,1350 L100,1350 Z" fill="#4a2c16"/><path d="M380,560 L2020,560 L2180,1300 L220,1300 Z" fill="#1c1008"/>'
    for x in (930, 1470): s += f'<path d="M{x},560 L{x+(x-1200)*0.15},1300" stroke="#4a2c16" stroke-width="24"/>'
    r = random.Random(7)
    for i in range(70):
        x = r.uniform(300, 2100); y = r.uniform(620, 1260)
        if r.random() < 0.5:
            s += f'<path d="M{f(x-40)},{f(y)} Q{f(x-30)},{f(y-40)} {f(x+10)},{f(y-36)} Q{f(x+45)},{f(y-20)} {f(x+38)},{f(y+12)} Q{f(x)},{f(y+28)} {f(x-40)},{f(y)} Z" fill="{r.choice(["#5a5450","#6e6862","#48423e"])}"/>'
        else:
            s += f'<path d="M{f(x-34)},{f(y)} L{f(x-10)},{f(y-30)} L{f(x+30)},{f(y-20)} L{f(x+36)},{f(y+14)} L{f(x)},{f(y+24)} Z" fill="#0a0908"/><path d="M{f(x-10)},{f(y-28)} L{f(x+30)},{f(y-20)}" stroke="#4a4a50" stroke-width="2"/>'
    s += coin(1100, 860, 46, 0.5, 3, 0.85) + coin(1500, 1000, 46, 0.5, 4, 0.6)
    return svg(s)

@art
def woman_walk(): return svg(place(woman('walk', MOONRIM), 1150, 1270, 1.0))

@art
def rebozo_dawn():
    s = sky('#3a3a4a', '#d8a080', mid='#8a7080') + glow(1700, 760, 500, 'warm', 0.6)
    s += ridge(760, 80, '#4a4050', 3) + '<rect x="0" y="790" width="2400" height="560" fill="#5a4a42"/>'
    s += road(500, 1900, 1200, 790, '#7a6656', '#5a4a42', 1350, 200)
    r = random.Random(5)
    for i in range(14):
        t = i / 13; x = 1200 + math.sin(i * 1.3) * 60 + (t - 0.5) * 300 * t; y = 820 + t * 520
        k = 0.3 + t * 1.4
        s += f'<ellipse cx="{f(x+ (30 if i%2 else -30)*k)}" cy="{f(y)}" rx="{f(26*k)}" ry="{f(14*k)}" fill="#1a0e08"/><ellipse cx="{f(x+(30 if i%2 else -30)*k)}" cy="{f(y)}" rx="{f(18*k)}" ry="{f(8*k)}" fill="#ff6a1a" opacity="0.35" filter="url(#blur1)"/>'
    # crumpled striped rebozo with knotted fringe and burnt, smouldering edge
    folds = [('M880,1150 Q960,1060 1120,1075 Q1230,1050 1330,1090 Q1420,1120 1450,1180 Q1380,1240 1220,1235 Q1060,1265 930,1230 Q850,1200 880,1150 Z', '#26304a'),
             ('M960,1120 Q1080,1090 1200,1110 Q1300,1100 1380,1140 Q1300,1170 1180,1165 Q1060,1185 960,1160 Z', '#323e5c'),
             ('M920,1190 Q1060,1170 1200,1190 Q1320,1185 1420,1200 Q1330,1225 1200,1222 Q1050,1240 930,1220 Z', '#1c2438')]
    for d, c in folds: s += f'<path d="{d}" fill="{c}"/>'
    for k in range(9):
        y0 = 1085 + k * 17
        s += f'<path d="M{900+k*6},{y0+40} Q{1100},{y0+10-k} {1300-k*4},{y0+24} Q{1380},{y0+30} {1430-k*3},{y0+50}" stroke="{"#8a9ab8" if k%2 else "#0e1220"}" stroke-width="{3 if k%2 else 5}" fill="none" opacity="0.55"/>'
    for k in range(16):
        x = 885 + k * 4; y = 1150 + k * 5
        s += f'<path d="M{x},{y} q{-30-r.uniform(0,25):.0f},{r.uniform(-6,10):.0f} {-50-r.uniform(0,20):.0f},{r.uniform(5,20):.0f}" stroke="#26304a" stroke-width="3.5" fill="none"/>'
    s += '<path d="M1330,1085 Q1440,1110 1462,1180 Q1420,1215 1360,1205 Q1390,1160 1330,1085 Z" fill="#0c0806"/>'
    s += '<path d="M1330,1085 Q1440,1110 1462,1180 Q1420,1215 1360,1205" stroke="#ff6a1a" stroke-width="5" fill="none" opacity="0.8" filter="url(#blur1)"/>'
    s += ''.join(f'<circle cx="{1340+r.uniform(0,120):.0f}" cy="{1095+r.uniform(0,110):.0f}" r="{r.uniform(2,5):.0f}" fill="#ffb040" opacity="0.8"/>' for _ in range(14))
    s += '<g filter="url(#blur3)">' + ''.join(f'<ellipse cx="{1350+i*30}" cy="{1080-i*90}" rx="{60+i*20}" ry="{40+i*10}" fill="#bbb2aa" opacity="{0.3-i*0.04:.2f}"/>' for i in range(6)) + '</g>'
    return svg(s)

@art
def church_dawn():
    s = sky('#2a2a48', '#f0a070', mid='#a06070') + glow(1500, 900, 700, 'warm', 0.7) + stars(30, 4, 250)
    s += ridge(840, 90, '#3a2a3a', 4) + '<rect x="0" y="900" width="2400" height="450" fill="#1a1420"/>'
    s += church(1300, 960, 0.75, '#1a1220', True)
    s += adobe_house(150, 980, 400, 220, '#1a1420', False, True) + adobe_house(1850, 990, 450, 240, '#1a1420', False, False)
    s += road(700, 1700, 1300, 960, '#3a2c30', '#2a2028', 1350, 120)
    s += place(campesino('walk', '#ffc890'), 1180, 1300, 0.36)
    return svg(s)

@art
def planchada():
    s = '<rect width="2400" height="1350" fill="#06100e"/>'
    s += '<path d="M0,0 L900,420 L1500,420 L2400,0 Z" fill="#0c1a18"/><path d="M0,1350 L900,880 L1500,880 L2400,1350 Z" fill="#132622"/>'
    s += '<path d="M0,0 L900,420 L900,880 L0,1350 Z" fill="#0a1614"/><path d="M2400,0 L1500,420 L1500,880 L2400,1350 Z" fill="#0a1614"/>'
    for k in range(5):
        t = k / 5; x0 = 0 + 900 * t ** 0.7
        s += f'<path d="M{f(x0)},{f(1350-470*t**0.7)} L{f(x0)},{f(420*t**0.7)}" stroke="#08100f" stroke-width="{f(40*(1-t)+6)}"/>'
        s += f'<path d="M{f(2400-x0)},{f(1350-470*t**0.7)} L{f(2400-x0)},{f(420*t**0.7)}" stroke="#08100f" stroke-width="{f(40*(1-t)+6)}"/>'
    for k in range(4):
        y = 120 + k * 80; s += glow(1200, y + 80, 160 - k * 25, 'white', 0.35 - k * 0.06)
    s += '<rect x="900" y="420" width="600" height="460" fill="#16302a"/>' + glow(1200, 650, 260, 'white', 0.5)
    s += f'<g opacity="0.85">{ghost_woman(1200, 860, 360, "#dff5ee", 0.85)}</g>'
    s += '<path d="M1180,550 L1220,550 L1225,560 L1175,560 Z" fill="#ffffff" opacity="0.8"/>'
    return svg(s)

# ------------------------------------------------------------------ overlays
@art
def smoke():
    r = random.Random(2); s = '<g filter="url(#blur3)">'
    for i in range(40):
        x = r.uniform(0, 2400); y = r.uniform(300, 1350)
        s += f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{r.uniform(120,320):.0f}" ry="{r.uniform(40,110):.0f}" fill="#c8c0b0" opacity="{r.uniform(0.08,0.25):.2f}"/>'
    s += '</g><g filter="url(#blur2)">'
    for i in range(18):
        x = r.uniform(0, 2400); y = r.uniform(400, 1300)
        s += f'<path d="M{f(x)},{f(y)} q60,-120 0,-240 q-60,-120 20,-240" stroke="#e0d8c8" stroke-width="{r.uniform(10,26):.0f}" fill="none" opacity="{r.uniform(0.08,0.2):.2f}"/>'
    return svg(s + '</g>')

def flame_tongues(x0, x1, ybase, hmin, hmax, n, seed, cols=("#ff4a10", "#ff8a1a", "#ffc040"), op=0.7, yjit=0, lean0=0.0):
    r = random.Random(seed); s = ''
    yb0 = ybase
    for i in range(n):
        ybase = yb0 + r.uniform(-yjit, 0)
        x = r.uniform(x0, x1); h = r.uniform(hmin, hmax); w = h * r.uniform(0.18, 0.3); lean = (r.uniform(-0.3, 0.3) + lean0) * h
        s += (f'<path d="M{f(x-w)},{f(ybase)} C{f(x-w*1.1)},{f(ybase-h*0.45)} {f(x+lean*0.5-w*0.3)},{f(ybase-h*0.7)} {f(x+lean)},{f(ybase-h)} '
              f'C{f(x+lean*0.4+w*0.5)},{f(ybase-h*0.6)} {f(x+w*1.1)},{f(ybase-h*0.4)} {f(x+w)},{f(ybase)} Z" fill="{r.choice(cols)}" opacity="{op}"/>')
    return s

@art
def flames():
    s = glow(1200, 1400, 1100, 'red', 0.7)
    s += f'<g filter="url(#blur2)">{flame_tongues(-100, 2500, 1380, 250, 620, 46, 1, ("#a0200a", "#d83a10"), 0.85)}</g>'
    s += f'<g filter="url(#blur1)">{flame_tongues(-100, 2500, 1370, 160, 420, 60, 2, ("#ff5a14", "#ff8a1a"), 0.75)}</g>'
    s += f'<g filter="url(#blur1)">{flame_tongues(-100, 2500, 1360, 80, 220, 70, 3, ("#ffc040", "#ffe080"), 0.7)}</g>'
    return svg(s)

# ------------------------------------------------------------------ extra plates (variety)
@art
def road_side():
    s = sky('#040810', '#22344a', mid='#0c1626') + stars(160, 12, 650) + moon(520, 260, 85) + cloud_band(300, '#18243a', 6, 7, 0.6, 30)
    s += ridge(850, 160, '#0e1826', 7, step=30) + ridge(930, 70, '#0a121c', 15, step=30)
    s += '<rect x="0" y="960" width="2400" height="390" fill="#0a0f16"/>'
    for i, (x, sz) in enumerate([(150, 220), (520, 150), (980, 120), (1400, 170), (1750, 110), (2150, 210)]):
        s += maguey(x, 1120, sz, 40 + i, '#05080d', rim='#5f7fa3')
    s += posts([60 + i * 300 for i in range(9)], [1160] * 9, [190] * 9, '#05080c')
    s += '<path d="M0,1170 Q1200,1150 2400,1175 L2400,1350 L0,1350 Z" fill="#2a2a2c"/>'
    r = random.Random(3)
    for i in range(90):
        s += f'<ellipse cx="{r.uniform(0,2400):.0f}" cy="{r.uniform(1185,1345):.0f}" rx="{r.uniform(4,16):.0f}" ry="{r.uniform(2,5):.0f}" fill="#141518" opacity="0.8"/>'
    s += grass(1172, 0, 2400, '#06090e', 120, 50, 8)
    return svg(s)

@art
def road_curve():
    s = sky('#03070f', '#1e2e44', mid='#0a1424') + stars(190, 21, 700) + moon(1850, 330, 105) + cloud_band(420, '#16233a', 2, 7, 0.55, 36)
    s += ridge(760, 220, '#0c1622', 21, step=30) + ridge(860, 110, '#091019', 22, step=30)
    s += '<rect x="0" y="880" width="2400" height="470" fill="#080d14"/>'
    s += '<path d="M700,1350 C760,1150 1500,1120 1700,1000 C1820,930 1700,900 1560,880 L1600,880 C1780,905 1900,940 1760,1010 C1560,1140 1250,1180 1700,1350 Z" fill="#26262a"/>'
    s += tree(420, 1180, 1100, 17, '#03050a', 'bare', 0.2)
    s += maguey(1950, 1150, 260, 55, '#04070b', rim='#5f7fa3') + maguey(260, 1330, 300, 56, '#020407') + nopal(2250, 1300, 170, 9, '#020407')
    s += '<rect x="1505" y="900" width="10" height="70" fill="#05070a"/><rect x="1490" y="915" width="40" height="8" fill="#05070a"/>'
    s += grass(1340, 0, 2400, '#04070b', 150, 70, 4)
    return svg(s)

@art
def roadside_cross():
    s = sky('#03070f', '#1a2a3e') + stars(120, 31, 600) + f'<circle cx="1700" cy="250" r="700" fill="url(#moonglow)"/>' + moon(1750, 240, 70)
    s += ridge(820, 120, '#0b1420', 31, step=30) + '<rect x="0" y="860" width="2400" height="490" fill="#090e15"/>'
    s += road(-200, 1500, 1350, 860, '#252528', '#121418', 1350, 300)
    s += f'<rect x="1690" y="640" width="46" height="620" fill="#1a120c"/><rect x="1560" y="760" width="306" height="42" fill="#1a120c"/>'
    s += f'<path d="M1690,640 L1736,640 L1736,1260" stroke="#5f7fa3" stroke-width="3" fill="none" opacity="0.6"/>'
    r = random.Random(5)
    for i in range(16):
        x = 1600 + r.uniform(-90, 260); y = 1250 + r.uniform(-30, 40); rr = r.uniform(22, 34)
        s += f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(rr)}" fill="#e88a14"/><circle cx="{f(x)}" cy="{f(y)}" r="{f(rr*0.55)}" fill="#c86a08"/>'
        s += f'<path d="M{f(x)},{f(y+rr)} l{r.uniform(-10,10):.0f},60" stroke="#2a4a1a" stroke-width="5"/>'
    s += candle(1560, 1290, 70, 22) + candle(1900, 1300, 50, 20)
    s += '<path d="M1520,1310 Q1700,1290 1960,1320 L1960,1350 L1520,1350 Z" fill="#0a0806"/>'
    s += maguey(300, 1300, 340, 61, '#020407', rim='#5f7fa3') + grass(1340, 0, 2400, '#04070b', 160, 70, 6)
    return svg(s)

@art
def red_hills():
    s = sky('#0a0103', '#5a1008', mid='#2a0406') + glow(1200, 900, 1200, 'red', 0.8)
    s += '<path d="M0,900 Q600,820 1200,880 Q1800,940 2400,860 L2400,1350 L0,1350 Z" fill="#160304"/>'
    s += ridge(940, 140, '#0c0203', 41, step=30)
    s += tree(1900, 1150, 900, 41, '#050102', 'bare', -0.15) + tree(300, 1200, 700, 42, '#050102', 'bare', 0.1)
    s += '<path d="M0,1180 Q1200,1120 2400,1200 L2400,1350 L0,1350 Z" fill="#070102"/>'
    s += f'<g filter="url(#blur2)">{flame_tongues(-100, 2500, 960, 60, 220, 60, 9, ("#ff4a10", "#ff8a1a", "#c02a0a"), 0.6)}</g>'
    return svg(s)

@art
def charro_eyes():
    bg = '<rect width="2400" height="1350" fill="#020304"/>' + f'<circle cx="1200" cy="200" r="900" fill="url(#moonglow)" opacity="0.6"/>'
    fig = charro_front_(hand_out=False, bag=False, upper=True, cape=False)
    return svg(bg, place(fig, 1200, 680 + 962 * 6.2, 6.2))

# ------------------------------------------------------------------ runner
if __name__ == "__main__":
    os.makedirs(os.path.join(HERE, 'art'), exist_ok=True)
    names = sys.argv[1:] or list(A)
    for n in names:
        open(os.path.join(HERE, 'art', n + '.svg'), 'w').write(A[n]())
    print("wrote", len(names), "svgs")
