"""Reusable drawing parts for 'El Hombre Caimán' (coast of Oaxaca): palms, mangroves, palapa huts, canoes,
the caiman (side view, close head, bride in white dress), the Chontal king, the Huave princess, elders, fishermen."""
import sys, os, math, random
sys.path.insert(0, '/home/claude/pipeline'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from art import *
from base_chars import head, uid, grad_lin, grad_rad, hand_open
from chars import strands, wrinkles, stubble, hair_luis, bust_frame, SK_LUIS, SK_OLD, SIL
from beso_art import S, clouds

MOON = "#a8c8ff"; WARM = "#ffcf8a"; GOLD = "#e8b23a"
SK_KING = dict(base="#9a6a44", light="#b8845a", hi="#d6a078", shadow="#5e3c26", deep="#321e12")
SK_PRIN = dict(base="#b07c58", light="#cc9670", hi="#e4b48c", shadow="#704a32", deep="#3c2618")


# ------------------------------------------------------------------ landscape parts
def palm(x, yb, h=700, lean=0.15, seed=1, color="#03070b", rim=None, fronds=9):
    r = random.Random(seed); k = h / 700
    tx, ty = x + lean * h, yb - h
    s = f'<path d="M{x-16*k},{yb} Q{x+lean*h*0.2},{yb-h*0.55} {tx-8*k},{ty} L{tx+8*k},{ty} Q{x+lean*h*0.2+22*k},{yb-h*0.55} {x+16*k},{yb} Z" fill="{color}"/>'
    for i in range(int(h / 40)):  # trunk rings
        t = i / (h / 40); px = x + (tx - x) * t * t * 0.6 + lean * h * 0.2 * 2 * t * (1 - t); py = yb - h * t
        s += f'<path d="M{px-14*k:.0f},{py:.0f} q{14*k:.0f},6 {28*k:.0f},0" stroke="#000" stroke-width="3" fill="none" opacity="0.5"/>'
    for f in range(fronds):
        a = math.radians(-170 + f * (160 / (fronds - 1)) + r.uniform(-8, 8))
        L = r.uniform(260, 360) * k; droop = r.uniform(80, 160) * k
        ex, ey = tx + math.cos(a) * L, ty + math.sin(a) * L * 0.55 + droop
        mx, my = tx + math.cos(a) * L * 0.5, ty + math.sin(a) * L * 0.5 - 30 * k
        s += f'<path d="M{tx:.0f},{ty:.0f} Q{mx:.0f},{my:.0f} {ex:.0f},{ey:.0f}" stroke="{color}" stroke-width="{7*k:.1f}" fill="none"/>'
        for j in range(1, 13):
            t = j / 13
            px = (1 - t) ** 2 * tx + 2 * (1 - t) * t * mx + t * t * ex; py = (1 - t) ** 2 * ty + 2 * (1 - t) * t * my + t * t * ey
            ll = (1 - t * 0.6) * 90 * k
            for sgn in (-1, 1):
                s += f'<path d="M{px:.0f},{py:.0f} q{sgn*ll*0.3:.0f},{ll*0.5:.0f} {sgn*ll*0.2:.0f},{ll:.0f}" stroke="{color}" stroke-width="{5*k:.1f}" fill="none"/>'
        if rim:
            s += f'<path d="M{tx:.0f},{ty:.0f} Q{mx:.0f},{my:.0f} {ex:.0f},{ey:.0f}" stroke="{rim}" stroke-width="2" fill="none" opacity="0.5"/>'
    return s


def mangrove(x, yb, k=1.0, seed=3, color="#02060a", rim=None):
    r = random.Random(seed); s = ""
    for i in range(9):  # arching prop roots
        dx = r.uniform(-220, 220) * k
        s += f'<path d="M{x+dx*0.2:.0f},{yb-260*k:.0f} Q{x+dx*0.9:.0f},{yb-240*k:.0f} {x+dx:.0f},{yb:.0f}" stroke="{color}" stroke-width="{r.uniform(8,16)*k:.1f}" fill="none"/>'
    s += f'<path d="M{x-20*k},{yb-200*k} L{x-14*k},{yb-420*k} L{x+14*k},{yb-420*k} L{x+20*k},{yb-200*k} Z" fill="{color}"/>'
    for i in range(16):
        cx = x + r.uniform(-300, 300) * k; cy = yb - r.uniform(420, 640) * k
        s += f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{r.uniform(90,180)*k:.0f}" ry="{r.uniform(60,110)*k:.0f}" fill="{color}"/>'
    if rim:
        for i in range(8):
            cx = x + r.uniform(-260, 260) * k; cy = yb - r.uniform(560, 680) * k
            s += f'<path d="M{cx-80*k:.0f},{cy:.0f} q{80*k:.0f},{-50*k:.0f} {160*k:.0f},0" stroke="{rim}" stroke-width="3" fill="none" opacity="0.35"/>'
    return s


def palapa(x, yb, k=1.0, lit=True, color="#05080c", thatch="#0a0c0e", rim=None):
    s = f'<g transform="translate({x},{yb}) scale({k})">'
    s += f'<rect x="-150" y="-200" width="300" height="200" fill="{color}"/>'
    for i in range(15): s += f'<path d="M{-150+i*21},-200 L{-150+i*21},0" stroke="#000" stroke-width="4" opacity="0.5"/>'
    if lit:
        s += '<rect x="-40" y="-150" width="80" height="150" fill="#ffb658"/>' + glow(0, -60, 180, "warm", 0.7)
    else:
        s += '<rect x="-40" y="-150" width="80" height="150" fill="#000"/>'
    s += f'<path d="M-230,-170 L0,-420 L230,-170 Z" fill="{thatch}"/>'
    for i in range(22): s += f'<path d="M{-230+i*21},-170 L{-115+i*10.5},{-300}" stroke="#000" stroke-width="3" opacity="0.4"/>'
    s += '<path d="M-230,-170 q20,14 40,0 q20,14 40,0 q20,14 40,0 q20,14 40,0 q20,14 40,0 q20,14 40,0 q20,14 40,0 q20,14 40,0 q20,14 40,0 q20,14 40,0 q20,14 40,0 q20,14 40,0" stroke="#000" stroke-width="5" fill="none" opacity="0.5"/>'
    if rim: s += f'<path d="M0,-420 L230,-170" stroke="{rim}" stroke-width="5" opacity="0.6"/>'
    return s + '</g>'


def canoe(x, y, k=1.0, color="#06080a", rim=None, flip=False):
    fl = " scale(-1,1)" if flip else ""
    s = f'<g transform="translate({x},{y}) scale({k}){fl}">'
    s += f'<path d="M-330,-30 Q-300,40 -180,46 L200,46 Q310,40 340,-36 L320,-20 Q0,-6 -310,-16 Z" fill="{color}"/>'
    if rim: s += f'<path d="M-330,-30 Q0,-12 340,-36" stroke="{rim}" stroke-width="4" fill="none" opacity="0.7"/>'
    return s + '</g>'


def lagoon_bg(dawn=False, moon_xy=(1700, 300), mr=110, mangroves=True):
    if dawn:
        s = sky("#26324a", "#f0a86a", "#8a6a7a") + glow(1500, 900, 900, "warm", 0.6)
        s += ridge(860, 70, "#2a2a3a", 4, step=50)
        s += water(900, 1350, "#a87a6a", "#2a2a3a") + reflection(1500, 905, 1350, "#ffd0a0", 260, 3)
        mc, rim = "#14141c", "#ffb27a"
    else:
        s = sky("#040912", "#163049", "#0c1d30") + stars(160, 4, 700) + moon(moon_xy[0], moon_xy[1], mr)
        s += clouds(8, 120, 600, 5, "#2a3e58", (0.15, 0.35))
        s += ridge(860, 70, "#0a1624", 4, step=50)
        s += water(900, 1350, "#16303f", "#03070c") + reflection(moon_xy[0], 905, 1350, "#dfe8f2", 220, 3)
        mc, rim = "#02060a", MOON
    if mangroves:
        s += mangrove(220, 930, 0.9, 3, mc, rim) + mangrove(2250, 930, 1.0, 5, mc, rim) + palm(450, 920, 640, -0.2, 2, mc, rim)
        s += palm(2050, 925, 720, 0.18, 6, mc, rim)
    s += reeds(0, 700, 1350, 7, mc, 70, 200) + reeds(1800, 2400, 1350, 8, mc, 70, 220)
    return s


# ------------------------------------------------------------------ caiman
def scales(cx, cy, w, h, seed=1, color="#000", op=0.35, step=26):
    r = random.Random(seed); s = f'<g opacity="{op}">'
    for yy in range(int(cy - h / 2), int(cy + h / 2), step):
        off = (yy // step) % 2 * step / 2
        for xx in range(int(cx - w / 2), int(cx + w / 2), step):
            s += f'<rect x="{xx+off:.0f}" y="{yy}" width="{step-6}" height="{step-8}" rx="6" fill="none" stroke="{color}" stroke-width="2"/>'
    return s + '</g>'


def caiman(x, y, k=1.0, flip=False, body="#2a3a2c", belly="#8a8a6a", rim=MOON, eye=GOLD, mouth=0.0, dress=False, sil=False):
    """Side view, facing right, ~1500 units long at k=1, belly line at y. sil=True -> dark silhouette with rim."""
    g = uid("cm"); fl = " scale(-1,1)" if flip else ""
    if sil: body, belly = "#05080a", "#0a0e10"
    s = f'<g transform="translate({x},{y}) scale({k}){fl}">'
    s += f'<defs>{grad_lin(g+"b", [(0, "#0a120c", 1), (0.5, body, 1), (1, "#0a120c", 1)], 0, -170, 0, 20)}</defs>'
    # tail
    tail = "M-260,-40 C-500,-60 -760,-20 -1000,10 C-860,-6 -560,10 -260,20 Z"
    s += f'<path d="{tail}" fill="url(#{g}b)"/>'
    for i in range(14):
        tx = -300 - i * 50; ty = -48 + i * 4
        s += f'<path d="M{tx-18},{ty+8} L{tx},{ty-22+i} L{tx+18},{ty+8} Z" fill="#0a120c"/>'
    # legs
    for (lx, ph) in ((-180, 1), (260, -1)):
        s += f'<path d="M{lx-40},0 C{lx-60},40 {lx-80*ph},70 {lx-110*ph},86 L{lx-150*ph},96 L{lx-90*ph},100 L{lx-20},60 L{lx+30},0 Z" fill="#0e160f"/>'
        for t in range(4): s += f'<path d="M{lx-110*ph},92 l{-20*ph-t*8*ph},{4+t*3}" stroke="#0e160f" stroke-width="6"/>'
    # body + head
    up = -mouth * 60
    bodyp = ("M-280,-40 C-200,-130 100,-150 330,-110 C420,-96 470,-84 520,-80 C560,-110 600,-118 640,-104 "
             f"C700,-90 800,-70 930,{-50+up*0.4:.0f} C960,{-44+up*0.5:.0f} 970,{-28+up*0.5:.0f} 950,{-20+up*0.3:.0f} L640,-14 "
             "C560,10 420,20 300,24 C100,36 -100,30 -280,20 Z")
    s += f'<path d="{bodyp}" fill="url(#{g}b)"/>'
    # lower jaw
    s += f'<path d="M560,-10 C700,-6 840,{-6-up*0.0:.0f} 940,{-12-up*-0.0:.0f} C930,6 860,20 640,20 C600,18 570,10 560,-10 Z" fill="#162018"/>'
    if mouth > 0:
        s += f'<path d="M600,-24 L940,{-30+up*0.6:.0f} L940,-12 L600,-6 Z" fill="#5a1a14"/>'
    # teeth
    for i in range(11):
        tx = 620 + i * 30
        s += f'<path d="M{tx},-18 l6,16 l6,-16 Z" fill="#e8e0c8"/>'
        if i % 2: s += f'<path d="M{tx+10},-10 l6,-14 l6,14 Z" fill="#d8d0b8"/>'
    # belly
    s += f'<path d="M-260,16 C-60,30 200,34 520,4 C420,26 100,38 -260,26 Z" fill="{belly}" opacity="0.5"/>'
    # osteoderm rows on back
    for i in range(18):
        bx = -240 + i * 42; by = -118 - 18 * math.sin(i / 17 * math.pi)
        s += f'<path d="M{bx-14},{by+12} L{bx},{by-14} L{bx+14},{by+12} Z" fill="#0a120c"/><path d="M{bx-12},{by+40} L{bx},{by+20} L{bx+12},{by+40} Z" fill="#0c140d" opacity="0.8"/>'
    s += f'<g clip-path="none">{scales(150, -60, 760, 120, 3, "#000", 0.25)}</g>'
    # eye on raised bump
    s += '<path d="M600,-110 C620,-140 670,-140 690,-108 Z" fill="#1a241a"/>'
    s += glow(645, -112, 70, "warm", 0.6) if not sil else ""
    s += f'<ellipse cx="645" cy="-112" rx="20" ry="13" fill="{eye}"/><ellipse cx="645" cy="-112" rx="4" ry="12" fill="#050505"/>'
    s += '<circle cx="925" cy="-56" r="7" fill="#050805"/>'
    if rim:
        s += f'<path d="M-280,-40 C-200,-130 100,-150 330,-110 C420,-96 470,-84 520,-80 C560,-110 600,-118 640,-104 C700,-90 800,-70 930,-50" stroke="{rim}" stroke-width="5" fill="none" opacity="0.75"/>'
        s += f'<path d="M-260,-40 C-500,-60 -760,-20 -1000,10" stroke="{rim}" stroke-width="3" fill="none" opacity="0.5"/>'
    if dress:
        # white wedding dress: rounded bodice over the back, ruffled skirt hanging below the belly, lace dots
        s += ('<path d="M-220,-110 C-120,-175 220,-180 380,-112 C400,-60 400,0 390,40 C430,80 450,140 440,190 '
              'C200,220 -40,220 -300,190 C-310,140 -280,80 -250,40 C-250,0 -245,-60 -220,-110 Z" fill="#f4f0e6"/>')
        for i in range(8):
            s += f'<path d="M{-270+i*92},190 Q{-224+i*92},230 {-178+i*92},190" fill="#f8f6f0" stroke="#d8d0c0" stroke-width="3"/>'
        s += '<path d="M-250,40 C-40,70 200,70 390,40" stroke="#e6c46a" stroke-width="10" fill="none"/>'
        for i in range(7): s += f'<path d="M{-200+i*90},60 Q{-190+i*90},130 {-215+i*94},190" stroke="#d6cebe" stroke-width="5" fill="none"/>'
        r_ = random.Random(2)
        for i in range(40): s += f'<circle cx="{r_.uniform(-200,360):.0f}" cy="{r_.uniform(-140,30):.0f}" r="4" fill="#d8d0c0"/>'
        s += '<path d="M-220,-110 C-120,-175 220,-180 380,-112" stroke="#fff" stroke-width="5" fill="none" opacity="0.8"/>'
        # veil: from the flower crown back over the dress, translucent
        s += '<path d="M600,-140 C480,-200 200,-200 0,-160 C-120,-120 -200,-40 -240,60 C-120,0 100,-60 300,-90 C420,-100 520,-110 600,-120 Z" fill="#ffffff" opacity="0.35"/>'
        s += '<path d="M600,-140 C480,-200 200,-200 0,-160 C-120,-120 -200,-40 -240,60" stroke="#ffffff" stroke-width="3" fill="none" opacity="0.6"/>'
        for i, c in enumerate(["#d23a5a", "#f0c040", "#ffffff", "#e0507a", "#f08a30", "#ffffff"]):
            fx_, fy_ = 560 + i * 26, -134 - 6 * math.sin(i)
            s += f'<circle cx="{fx_}" cy="{fy_}" r="16" fill="{c}"/><circle cx="{fx_}" cy="{fy_}" r="5" fill="#f6d040"/>'
        # ribbon tying the snout
        s += '<path d="M820,-70 L836,20 M800,-66 L814,22" stroke="#e8ddc8" stroke-width="12"/><path d="M826,22 q-30,40 -10,70 M826,22 q30,40 10,74" stroke="#e8ddc8" stroke-width="8" fill="none"/>'
    return s + '</g>'


def caiman_head_close(cx, cy, k=1.0, eye=GOLD, rim=MOON, mouth=0.25):
    """Big close profile of the head (facing left), filling the frame."""
    g = uid("ch"); s = f'<g transform="translate({cx},{cy}) scale({k})">'
    s += f'<defs>{grad_lin(g+"h", [(0, "#050a06", 1), (0.45, "#2e4030", 1), (1, "#060a06", 1)], 0, -380, 0, 260)}</defs>'
    op = mouth * 160
    up = f"M1300,-420 C900,-470 500,-420 160,-300 C-200,-250 -560,-210 -900,-150 C-980,-130 -1000,-90 -960,-60 L-520,{-40-op*0.3:.0f} C-100,{-30-op*0.6:.0f} 500,{-20-op:.0f} 1300,-60 Z"
    lo = f"M1300,-40 C600,{20+op*0.3:.0f} 0,{60+op*0.5:.0f} -560,{40+op*0.6:.0f} L-900,{40+op*0.6:.0f} C-920,{80+op*0.6:.0f} -880,{110+op*0.6:.0f} -800,{120+op*0.6:.0f} C-300,{190+op*0.6:.0f} 400,240 1300,300 Z"
    if mouth > 0:
        s += f'<path d="M-900,-60 L1300,-60 L1300,0 L-900,{60+op*0.6:.0f} Z" fill="#3a0c0a"/>'
    s += f'<path d="{lo}" fill="#121c12"/>'
    s += f'<path d="{up}" fill="url(#{g}h)"/>'
    r = random.Random(9)
    for i in range(22):  # teeth top
        tx = -880 + i * 60 + r.uniform(-8, 8); ty = -50 - op * (0.3 + 0.7 * (tx + 900) / 2200) * 0.9
        L = r.uniform(36, 70)
        s += f'<path d="M{tx-12:.0f},{ty:.0f} L{tx:.0f},{ty+L:.0f} L{tx+12:.0f},{ty:.0f} Z" fill="#ece4cc"/>'
    for i in range(20):
        tx = -840 + i * 62 + r.uniform(-8, 8); ty = 40 + op * 0.6 - i * 2
        L = r.uniform(30, 60)
        s += f'<path d="M{tx-11:.0f},{ty:.0f} L{tx:.0f},{ty-L:.0f} L{tx+11:.0f},{ty:.0f} Z" fill="#d8d0b6"/>'
    s += scales(200, -200, 1800, 300, 4, "#000", 0.3, 44)
    for i in range(40):
        px = r.uniform(-850, 1200); py = r.uniform(-330, -120)
        s += f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{r.uniform(4,10):.0f}" fill="#000" opacity="0.35"/>'
    # eye bump
    s += '<path d="M260,-330 C300,-500 560,-520 620,-320 Z" fill="#1c2a1c"/>'
    s += glow(440, -360, 260, "warm", 0.55)
    s += f'<ellipse cx="440" cy="-370" rx="96" ry="62" fill="{eye}"/>'
    s += '<ellipse cx="440" cy="-370" rx="96" ry="62" fill="none" stroke="#3a2a08" stroke-width="10"/>'
    for a in range(24):
        ang = a * 15
        s += f'<path d="M440,-370 L{440+math.cos(math.radians(ang))*90:.0f},{-370+math.sin(math.radians(ang))*58:.0f}" stroke="#a87a1a" stroke-width="3" opacity="0.6"/>'
    s += '<ellipse cx="440" cy="-370" rx="16" ry="58" fill="#030303"/><ellipse cx="410" cy="-392" rx="16" ry="10" fill="#fff" opacity="0.85"/>'
    s += '<path d="M330,-420 C380,-460 500,-460 560,-420" stroke="#0a100a" stroke-width="18" fill="none"/>'
    s += '<ellipse cx="-880" cy="-150" rx="22" ry="14" fill="#020402"/>'
    if rim:
        s += f'<path d="M1300,-420 C900,-470 500,-420 160,-300 C-200,-250 -560,-210 -900,-150" stroke="{rim}" stroke-width="8" fill="none" opacity="0.7"/>'
    return s + '</g>'


def eyes_pair(x, y, k=1.0, op=1.0):
    s = f'<g transform="translate({x},{y}) scale({k})" opacity="{op}">'
    for dx in (-70, 70):
        s += glow(dx, 0, 110, "warm", 0.9) + f'<ellipse cx="{dx}" cy="0" rx="26" ry="15" fill="{GOLD}"/><ellipse cx="{dx}" cy="0" rx="5" ry="14" fill="#060606"/>'
        s += f'<path d="M{dx-40},6 Q{dx},22 {dx+40},6" stroke="#0a1418" stroke-width="10" fill="none"/>'
    s += '<path d="M-240,30 C-100,10 100,10 240,30" stroke="#a8c8e8" stroke-width="3" fill="none" opacity="0.5"/>'
    s += '<path d="M200,40 C320,36 420,40 520,46" stroke="#05080a" stroke-width="14" fill="none"/>'
    return s + '</g>'


# ------------------------------------------------------------------ people (full figures, shadow theatre)
def king_full(x, y, h=900, torch=True, rim=MOON, kneel=False, holding=False, arms_up=False, fill=SIL):
    k = h / 1000; s = f'<g transform="translate({x},{y}) scale({k})">'
    if kneel:
        body = ("M-20,-650 C-66,-650 -86,-610 -80,-566 C-76,-536 -60,-516 -48,-508 C-110,-488 -150,-440 -160,-370 "
                "C-170,-300 -176,-220 -170,-160 C-200,-130 -250,-110 -270,-60 C-280,-30 -270,0 -240,0 L60,0 "
                "C110,0 150,-30 150,-80 C150,-120 120,-140 70,-150 L90,-260 C140,-250 190,-270 210,-310 L180,-330 "
                "C150,-300 110,-300 80,-320 C90,-380 80,-450 30,-500 C46,-512 60,-536 62,-566 C66,-616 30,-650 -20,-650 Z")
    else:
        body = ("M0,-1000 C-50,-1000 -70,-960 -68,-910 C-66,-870 -50,-850 -40,-840 C-110,-820 -150,-780 -160,-700 "
                "L-180,-420 L-150,-420 L-120,-500 L-110,-300 L-90,0 L-20,0 L0,-300 L20,0 L90,0 L110,-300 L120,-500 L150,-420 L180,-420 "
                "L160,-700 C150,-780 110,-820 40,-840 C50,-850 66,-870 68,-910 C70,-960 50,-1000 0,-1000 Z")
    s += f'<path d="{body}" fill="{fill}"/>'
    hx, hy = (-10, -580) if kneel else (0, -930)
    # long hair down the back
    s += f'<path d="M{hx-50},{hy-40} C{hx-90},{hy+40} {hx-80},{hy+140} {hx-60},{hy+200} L{hx-30},{hy+120} Z" fill="{fill}"/>'
    # white cotton manta draped over a shoulder
    if not kneel:
        s += '<path d="M150,-800 C60,-760 -60,-640 -150,-520 L-110,-480 C-20,-600 80,-700 165,-740 Z" fill="#8a98a8" opacity="0.45"/>'
        for i in range(11):
            a = math.radians(200 + i * 14)
            s += f'<circle cx="{math.cos(a)*-60:.0f}" cy="{-830+abs(math.sin(a))*30+i%2*6:.0f}" r="9" fill="#efe8d8"/>'
    else:
        s += '<path d="M130,-470 C60,-440 -40,-380 -140,-300 L-110,-270 C-20,-350 70,-410 145,-430 Z" fill="#8a98a8" opacity="0.45"/>'
    # band with feather
    s += f'<path d="M{hx-66},{hy-30} L{hx+66},{hy-30}" stroke="#b8402a" stroke-width="10" opacity="0.8"/>'
    s += f'<path d="M{hx+30},{hy-34} C{hx+60},{hy-140} {hx+120},{hy-180} {hx+140},{hy-190} C{hx+110},{hy-140} {hx+70},{hy-90} {hx+40},{hy-34} Z" fill="{fill}"/>'
    if torch and not kneel:
        s += '<path d="M150,-440 L230,-860" stroke="#2a1a10" stroke-width="22"/>' + glow(235, -900, 360, "warm", 0.9)
        s += '<path d="M235,-990 Q275,-920 240,-860 Q200,-900 235,-990 Z" fill="#ffb84a"/><path d="M236,-950 Q252,-910 238,-878 Q222,-905 236,-950 Z" fill="#fff0c0"/>'
    if arms_up:
        s += '<path d="M-150,-760 L-300,-1080 L-260,-1100 L-110,-800 Z M150,-760 L300,-1080 L260,-1100 L110,-800 Z" fill="' + fill + '"/>'
    if rim:
        s += f'<path d="{body}" fill="none" stroke="{rim}" stroke-width="5" opacity="0.55" filter="url(#blur1)"/>'
    return s + '</g>'


def princess_full(x, y, h=900, rim=MOON, back=False, fill=SIL, glowc=None):
    k = h / 1000; s = f'<g transform="translate({x},{y}) scale({k})">'
    body = ("M0,-1000 C-48,-1000 -66,-960 -64,-912 C-62,-880 -52,-860 -40,-850 C-100,-830 -130,-790 -136,-720 "
            "L-150,-520 L-120,-520 L-110,-600 L-120,-420 C-180,-260 -230,-120 -260,0 L260,0 C230,-120 180,-260 120,-420 "
            "L110,-600 L120,-520 L150,-520 L136,-720 C130,-790 100,-830 40,-850 C52,-860 62,-880 64,-912 C66,-960 48,-1000 0,-1000 Z")
    if glowc: s += glow(0, -500, 700, glowc, 0.5)
    s += f'<path d="{body}" fill="{fill}"/>'
    # long hair to the waist
    s += f'<path d="M-60,-960 C-110,-860 -120,-700 -110,-560 L-60,-580 C-70,-700 -50,-840 -30,-900 Z" fill="{fill}"/>'
    s += f'<path d="M60,-960 C110,-860 120,-700 110,-560 L60,-580 C70,-700 50,-840 30,-900 Z" fill="{fill}"/>'
    if back:
        s += f'<path d="M-64,-940 C-90,-800 -80,-640 -40,-560 L40,-560 C80,-640 90,-800 64,-940 Z" fill="#050608"/>'
    # huipil hem and skirt pattern catching the light
    s += '<path d="M-150,-520 L150,-520" stroke="#8a2a3a" stroke-width="14" opacity="0.8"/>'
    for i in range(7): s += f'<path d="M{-140+i*46},-510 l12,20 l12,-20" stroke="#c8a040" stroke-width="5" fill="none" opacity="0.7"/>'
    s += '<path d="M-250,-40 C-80,-20 80,-20 250,-40" stroke="#c8c4b8" stroke-width="12" fill="none" opacity="0.6"/>'
    # flowers in hair
    for (fx_, fy_, c) in ((-50, -960, "#e0507a"), (-70, -930, "#f0c040"), (-36, -985, "#ffffff")):
        s += f'<circle cx="{fx_}" cy="{fy_}" r="16" fill="{c}"/>'
    if rim:
        s += f'<path d="{body}" fill="none" stroke="{rim}" stroke-width="5" opacity="0.55" filter="url(#blur1)"/>'
    return s + '</g>'


def fisher_sil(x, y, h=700, kind="pull", fill=SIL, rim=None, facing=1, seed=1):
    k = h / 1000; fl = "" if facing > 0 else " scale(-1,1)"
    s = f'<g transform="translate({x},{y}) scale({k}){fl}">'
    if kind == "pull":  # leaning back pulling a rope / net
        p = ("M60,-930 C20,-930 4,-890 10,-850 C14,-820 30,-806 40,-800 C-20,-780 -60,-730 -80,-650 L-110,-440 L-60,-420 "
             "L-40,-300 L-160,0 L-90,0 L20,-250 L80,0 L150,0 L90,-330 L100,-480 L280,-560 L290,-600 L110,-640 C120,-720 120,-790 80,-806 "
             "C96,-816 110,-840 108,-870 C104,-910 90,-930 60,-930 Z")
    elif kind == "cast":
        p = ("M0,-930 C-40,-930 -56,-890 -52,-850 C-50,-820 -36,-806 -26,-800 C-90,-780 -120,-730 -130,-650 L-280,-760 L-300,-730 L-150,-560 "
             "L-120,-440 L-110,0 L-40,0 L0,-300 L40,0 L110,0 L120,-440 L140,-640 L320,-900 L290,-920 L120,-760 C100,-790 60,-806 30,-806 "
             "C44,-816 56,-840 54,-870 C50,-910 36,-930 0,-930 Z")
    else:  # stand
        p = ("M0,-930 C-40,-930 -56,-890 -52,-850 C-50,-820 -36,-806 -26,-800 C-90,-780 -120,-730 -130,-650 L-150,-420 L-110,-420 "
             "L-100,0 L-30,0 L0,-300 L30,0 L100,0 L110,-420 L150,-420 L130,-650 C120,-730 90,-780 26,-800 "
             "C36,-806 50,-820 52,-850 C56,-890 40,-930 0,-930 Z")
    s += f'<path d="{p}" fill="{fill}"/>'
    s += f'<ellipse cx="{50 if kind=="pull" else 0}" cy="-900" rx="120" ry="22" fill="{fill}"/>'
    if rim: s += f'<path d="{p}" fill="none" stroke="{rim}" stroke-width="5" opacity="0.5" filter="url(#blur1)"/>'
    return s + '</g>'


def net(x0, y0, x1, y1, color="#c8c0a8", op=0.5, n=14):
    s = f'<g stroke="{color}" stroke-width="2.5" opacity="{op}" fill="none">'
    for i in range(n + 1):
        t = i / n
        s += f'<path d="M{x0+(x1-x0)*t:.0f},{y0} Q{x0+(x1-x0)*t+20:.0f},{(y0+y1)/2+40:.0f} {x0+(x1-x0)*t:.0f},{y1}"/>'
        s += f'<path d="M{x0},{y0+(y1-y0)*t:.0f} Q{(x0+x1)/2:.0f},{y0+(y1-y0)*t+50:.0f} {x1},{y0+(y1-y0)*t:.0f}"/>'
    return s + '</g>'


def fish(x, y, k=1.0, rot=0, c="#cfd8e0"):
    return (f'<g transform="translate({x},{y}) rotate({rot}) scale({k})"><path d="M-60,0 C-30,-26 30,-26 50,0 C30,26 -30,26 -60,0 Z" fill="{c}"/>'
            f'<path d="M50,0 L80,-22 L76,0 L80,22 Z" fill="{c}"/><circle cx="-38" cy="-4" r="4" fill="#111"/>'
            f'<path d="M-30,-12 C0,-18 30,-10 44,0" stroke="#fff" stroke-width="3" fill="none" opacity="0.7"/></g>')


# ------------------------------------------------------------------ busts
def shell_necklace(y=170, n=13, w=150, droop=60):
    s = f'<path d="M{-w},{y-30} Q0,{y+droop+20} {w},{y-30}" stroke="#6a5a40" stroke-width="3" fill="none"/>'
    for i in range(n):
        t = i / (n - 1); px = -w + 2 * w * t; py = (y - 30) * (1 - t) ** 2 + 2 * (1 - t) * t * (y + droop + 20) + t * t * (y - 30)
        s += f'<path d="M{px-9:.0f},{py:.0f} Q{px:.0f},{py+26:.0f} {px+9:.0f},{py:.0f} Z" fill="#efe6d4" stroke="#a89878" stroke-width="2"/>'
    s += f'<circle cx="0" cy="{y+droop+30}" r="18" fill="#3a8a6a"/><circle cx="-4" cy="{y+droop+26}" r="6" fill="#8ad0b0" opacity="0.7"/>'
    return s


def hair_long_back(color="#0a0705", seed=1, w=1.0):
    r = random.Random(seed)
    s = (f'<path d="M-92,-60 C-120,-150 -60,-186 0,-186 C60,-186 120,-150 92,-60 C110,40 {130*w},180 {120*w},330 '
         f'L{-120*w},330 C{-130*w},180 -110,40 -92,-60 Z" fill="{color}"/>')
    s += strands(r, [(-100, 0, -130 * w, 160, -110 * w, 320), (100, 0, 130 * w, 160, 110 * w, 320)], 14, "#3a2a1e", (1.5, 3), (0.3, 0.6), 10)
    return s


def king_head(look=0.0, turn=0.0, lids=0.2, smile=0.1, rim=MOON, shock=False):
    s = ""
    s += head(look=look, smile=(-0.5 if shock else smile), lids=(0.0 if shock else lids), rim=rim, turn=turn, sk=SK_KING, headwrap=False,
              earring=False, lips=("#5a2e22", "#6e3a2c"), iris="#1e1008", brow_w=1.3, neck=True)
    # hair cap with center part
    s += ('<path d="M0,-112 C-36,-112 -66,-92 -76,-54 C-80,-30 -82,-6 -80,20 C-96,-10 -100,-60 -92,-100 C-80,-150 -40,-176 0,-176 '
          'C40,-176 80,-150 92,-100 C100,-60 96,-10 80,20 C82,-6 80,-30 76,-54 C66,-92 36,-112 0,-112 Z" fill="#0a0604"/>')
    # woven band with shells and a feather
    s += '<path d="M-92,-96 C-40,-124 40,-124 92,-96 L92,-74 C40,-102 -40,-102 -92,-74 Z" fill="#b8402a"/>'
    for i in range(9):
        s += f'<circle cx="{-72+i*18}" cy="{-98-8*math.sin(i/8*math.pi)}" r="5" fill="#efe6d4"/>'
    s += '<path d="M70,-100 C110,-200 150,-250 190,-280 C170,-220 130,-150 86,-92 Z" fill="#1a3a4a"/><path d="M76,-100 C120,-190 150,-240 186,-276" stroke="#4aa0b0" stroke-width="3" fill="none"/>'
    if shock: s += '<ellipse cx="0" cy="76" rx="14" ry="10" fill="#2a0e0a"/>'
    return s


def king_body(rim=MOON):
    g = uid("kb"); sk = SK_KING
    s = (f'<defs>{grad_lin(g+"m", [(0, "#4a4e56", 1), (0.5, "#c8ccd0", 1), (1, "#e8e8e4", 1)], -360, 0, 360, 0)}'
         f'{grad_lin(g+"s", [(0, sk["deep"], 1), (0.5, sk["shadow"], 1), (1, sk["base"], 1)], -240, 0, 240, 0)}</defs>')
    s += hair_long_back("#080504", 7, 1.1).replace('fill="#080504"', 'fill="#080504" transform="translate(0,-10)"', 1) if False else ""
    s += f'<path d="M-52,40 C-54,110 -62,150 -80,190 L80,190 C62,150 54,110 52,40 Z" fill="url(#{g}s)"/>'
    s += f'<path d="M-260,240 C-180,200 -100,180 0,180 C100,180 180,200 260,240 L320,660 L-320,660 Z" fill="url(#{g}s)"/>'
    # manta knotted on the right shoulder
    s += f'<path d="M-330,300 C-200,230 60,280 210,200 C260,240 300,320 330,660 L-340,660 C-350,500 -350,380 -330,300 Z" fill="url(#{g}m)"/>'
    for d in ["M-200,290 Q-180,480 -220,660", "M-60,300 Q-40,480 -80,660", "M80,260 Q100,460 60,660", "M200,230 Q230,440 210,660"]:
        s += f'<path d="{d}" stroke="#5a5e66" stroke-width="7" fill="none" opacity="0.55"/>'
    s += '<path d="M-330,420 L330,400" stroke="#b8402a" stroke-width="12" opacity="0.8"/>'
    s += '<path d="M-330,440 L330,420" stroke="#e0b040" stroke-width="5" opacity="0.8"/>'
    s += '<ellipse cx="210" cy="210" rx="40" ry="28" fill="#d8dad8"/>'
    s += shell_necklace(170, 13, 150, 60)
    if rim: s += f'<path d="M-260,240 C-320,320 -340,460 -340,660" stroke="{rim}" stroke-width="6" fill="none" opacity="0.5" filter="url(#blur1)"/>'
    return s


def bust_frame2(back, body, headsvg, x, y, k):
    return f'<g transform="translate({x},{y}) scale({k})">{back}<g transform="translate(0,18) scale(0.74,0.86)">{body}</g>{headsvg}</g>'


def king_bust(x, y, k=1.0, rim=MOON, **hk):
    return bust_frame2(hair_long_back("#080504", 7, 1.1), king_body(rim), king_head(rim=rim, **hk), x, y, k)


def princess_head(look=0.0, turn=0.0, lids=0.25, smile=0.3, rim=MOON, reptile=False, wet=False):
    s = ""
    s += head(look=look, smile=smile, lids=(0.0 if reptile else lids), rim=rim, turn=turn, sk=SK_PRIN, headwrap=False,
              earring=True, lips=("#7a3632", "#94483e"), iris=(GOLD if reptile else "#24140a"), brow_w=0.8, neck=True)
    if reptile:
        for dx in (-34, 34):
            ix = dx + look * 8
            s += glow(ix, -19, 46, "warm", 1.0) + f'<circle cx="{ix}" cy="-19" r="12" fill="{GOLD}"/><ellipse cx="{ix}" cy="-19" rx="3.5" ry="11" fill="#050505"/>' 
        # faint scales on temples and cheeks
        for side in (-1, 1):
            for i in range(10):
                s += f'<path d="M{side*(58+i%3*6)},{-50+i*10} q{side*6},4 0,8" stroke="#3a5a3a" stroke-width="2" fill="none" opacity="0.6"/>'
    s += ('<path d="M0,-108 C-34,-108 -64,-90 -76,-56 C-82,-30 -84,0 -84,30 C-98,0 -102,-50 -94,-92 C-84,-142 -42,-170 0,-170 '
          'C42,-170 84,-142 94,-92 C102,-50 98,0 84,30 C84,0 82,-30 76,-56 C64,-90 34,-108 0,-108 Z" fill="#0d0806"/>')
    r = random.Random(11)
    s += strands(r, [(-2, -108, -44, -116, -80, -40), (2, -108, 44, -116, 80, -40)], 8, "#4a2e1e", (1.2, 2.6), (0.35, 0.8), 5)
    s += strands(r, [(-80, -40, -110, 80, -96, 200), (80, -40, 110, 80, 96, 210)], 6, "#140b08", (2, 3.5), (0.7, 1), 6)
    for (fx_, fy_, kk, c) in ((-80, -90, 1.0, "#e0507a"), (-96, -62, 0.8, "#f0c040"), (-60, -118, 0.7, "#ffffff"), (-104, -36, 0.6, "#e0507a")):
        for a in range(6):
            ang = math.radians(a * 60)
            s += f'<ellipse cx="{fx_+math.cos(ang)*11*kk:.1f}" cy="{fy_+math.sin(ang)*11*kk:.1f}" rx="{9*kk:.1f}" ry="{6*kk:.1f}" fill="{c}" transform="rotate({a*60} {fx_+math.cos(ang)*11*kk:.1f} {fy_+math.sin(ang)*11*kk:.1f})"/>'
        s += f'<circle cx="{fx_}" cy="{fy_}" r="{5*kk:.1f}" fill="#f6d040"/>'
    if wet:
        for i in range(6): s += f'<circle cx="{-50+i*20}" cy="{-60+(i%3)*40}" r="3" fill="#dfefff" opacity="0.8"/>'
    return s


def princess_body(rim=MOON):
    g = uid("pb"); sk = SK_PRIN
    s = (f'<defs>{grad_lin(g+"h", [(0, "#3a0e1a", 1), (0.5, "#8a1e34", 1), (1, "#5a1424", 1)], -360, 0, 360, 0)}'
         f'{grad_lin(g+"s", [(0, sk["deep"], 1), (0.5, sk["shadow"], 1), (1, sk["base"], 1)], -60, 0, 60, 0)}</defs>')
    s += f'<path d="M-44,40 C-44,100 -58,150 -110,186 L110,186 C58,150 44,100 44,40 Z" fill="url(#{g}s)"/>'
    # huipil: wide square neck, embroidered yoke with flowers and birds (Isthmus style)
    s += f'<path d="M-250,226 C-170,206 -130,196 -110,186 L110,186 C130,196 170,206 250,226 C320,270 350,400 360,660 L-360,660 C-350,400 -320,270 -250,226 Z" fill="url(#{g}h)"/>'
    s += '<path d="M-110,186 L-120,290 L120,290 L110,186" fill="none" stroke="#e0b040" stroke-width="8"/>'
    r = random.Random(5)
    for i in range(26):
        px = r.uniform(-300, 300); py = r.uniform(300, 640)
        c = r.choice(["#f0c040", "#f4f0e0", "#e0507a", "#4ab0a0"])
        for a in range(5):
            ang = math.radians(a * 72)
            s += f'<circle cx="{px+math.cos(ang)*12:.0f}" cy="{py+math.sin(ang)*12:.0f}" r="8" fill="{c}" opacity="0.85"/>'
        s += f'<circle cx="{px:.0f}" cy="{py:.0f}" r="5" fill="#2a0a10"/>'
    s += shell_necklace(160, 11, 110, 40)
    if rim: s += f'<path d="M-250,226 C-330,270 -350,420 -360,660" stroke="{rim}" stroke-width="5" fill="none" opacity="0.5" filter="url(#blur1)"/>'
    return s


def princess_bust(x, y, k=1.0, rim=MOON, **hk):
    return bust_frame2(hair_long_back("#0b0705", 3, 1.25), princess_body(rim), princess_head(rim=rim, **hk), x, y, k)


def elder_head(smile=-0.1, lids=0.45, rim=WARM, band="#e8e0cc", look=0.0):
    r = random.Random(13)
    s = ('<path d="M-92,-60 C-110,-150 -60,-180 0,-180 C60,-180 110,-150 92,-60 C104,20 110,100 100,170 L-100,170 C-110,100 -104,20 -92,-60 Z" fill="#8a8680"/>')
    s += strands(r, [(-96, -40, -112, 60, -100, 160), (96, -40, 112, 60, 100, 160)], 12, "#c8c4bc", (1.5, 3), (0.4, 0.8), 8)
    s += head(look=look, smile=smile, lids=lids, rim=rim, turn=0.0, sk=SK_OLD, headwrap=False, earring=False,
              lips=("#4a2a22", "#5a3428"), iris="#1a0e08", brow_w=1.4, neck=True)
    s += wrinkles(heavy=1.3)
    s += '<path d="M-60,-14 Q-34,-6 -10,-14 M10,-14 Q34,-6 60,-14" stroke="#30201a" stroke-width="3" fill="none" opacity="0.5"/>'
    s += ('<path d="M0,-104 C-40,-104 -70,-84 -80,-44 C-90,-80 -80,-150 0,-160 C80,-150 90,-80 80,-44 C70,-84 40,-104 0,-104 Z" fill="#a8a49c"/>')
    s += strands(r, [(-4, -150, -50, -150, -80, -60), (4, -150, 50, -150, 80, -60)], 10, "#e0dcd4", (1.2, 2.4), (0.4, 0.8), 5)
    s += f'<path d="M-90,-90 C-40,-116 40,-116 90,-90 L90,-70 C40,-96 -40,-96 -90,-70 Z" fill="{band}"/>'
    return s


def elder_body(rim=WARM, color=("#2a2620", "#7a6e5a", "#a8987a")):
    g = uid("eb")
    s = (f'<defs>{grad_lin(g+"m", [(0, color[0], 1), (0.6, color[1], 1), (1, color[2], 1)], -360, 0, 360, 0)}</defs>')
    s += f'<path d="M-50,40 C-52,110 -60,150 -76,190 L76,190 C60,150 52,110 50,40 Z" fill="{SK_OLD["shadow"]}"/>'
    s += f'<path d="M-280,250 C-180,200 -100,176 -70,170 L0,250 L70,170 C100,176 180,200 280,250 L330,660 L-330,660 Z" fill="url(#{g}m)"/>'
    for d in ["M-200,280 Q-180,480 -210,660", "M200,280 Q180,480 210,660", "M-40,300 Q-30,480 -50,660", "M40,300 Q30,480 50,660"]:
        s += f'<path d="{d}" stroke="#1a160e" stroke-width="7" fill="none" opacity="0.5"/>'
    s += shell_necklace(180, 9, 90, 30)
    if rim: s += f'<path d="M-280,250 C-320,320 -330,460 -330,660" stroke="{rim}" stroke-width="6" fill="none" opacity="0.5" filter="url(#blur1)"/>'
    return s


def elder_bust(x, y, k=1.0, rim=WARM, color=("#2a2620", "#7a6e5a", "#a8987a"), **hk):
    return bust_frame(elder_body(rim, color), elder_head(rim=rim, **hk), x, y, k)


def fisher_head(look=0.0, lids=0.15, smile=0.3, rim=MOON, shock=False, laugh=False):
    r = random.Random(4)
    s = head(look=look, smile=(-0.5 if shock else smile), lids=(0.0 if shock else lids), rim=rim, turn=0.0, sk=SK_LUIS, headwrap=False,
             earring=False, lips=("#6a3a2c", "#7e4a3a"), iris="#24140a", brow_w=1.25, neck=True)
    s += stubble(r, "#2a1810")
    if laugh:
        s += '<path d="M-34,70 Q0,104 34,70 Q0,84 -34,70 Z" fill="#2a0e0a"/><path d="M-28,72 Q0,80 28,72" stroke="#e8e0d0" stroke-width="5" fill="none"/>'
    if shock:
        s += '<ellipse cx="0" cy="78" rx="12" ry="9" fill="#2a0e0a"/>'
        s += '<g fill="#e8eef6" opacity="0.9"><circle cx="-34" cy="-19" r="15"/><circle cx="34" cy="-19" r="15"/></g><circle cx="-34" cy="-19" r="5" fill="#120a06"/><circle cx="34" cy="-19" r="5" fill="#120a06"/>'
    s += hair_luis()
    return s


def fisher_body(rim=MOON):
    g = uid("fb2"); sk = SK_LUIS
    s = (f'<defs>{grad_lin(g+"w", [(0, "#4a4a46", 1), (0.6, "#b8b4a8", 1), (1, "#d4d0c4", 1)], -340, 0, 340, 0)}'
         f'{grad_lin(g+"s", [(0, sk["deep"], 1), (0.5, sk["shadow"], 1), (1, sk["base"], 1)], -60, 0, 60, 0)}</defs>')
    s += f'<path d="M-50,40 C-52,110 -60,150 -70,190 L70,190 C60,150 52,110 50,40 Z" fill="url(#{g}s)"/>'
    s += f'<path d="M-240,230 C-160,190 -90,160 -60,150 L0,300 L60,150 C90,160 160,190 240,230 L280,660 L-280,660 Z" fill="url(#{g}w)"/>'
    s += f'<path d="M-60,150 L0,300 L60,150 Z" fill="url(#{g}s)"/>'
    for d in ["M-180,260 Q-160,460 -190,660", "M180,260 Q160,460 190,660", "M-60,320 Q-50,480 -70,660"]:
        s += f'<path d="{d}" stroke="#4a4840" stroke-width="7" fill="none" opacity="0.5"/>'
    s += '<path d="M-240,230 L-60,150 M240,230 L60,150" stroke="#8a8478" stroke-width="5"/>'
    if rim: s += f'<path d="M-240,230 C-290,320 -300,460 -300,660" stroke="{rim}" stroke-width="5" fill="none" opacity="0.5" filter="url(#blur1)"/>'
    return s


def fisher_bust(x, y, k=1.0, rim=MOON, **hk):
    return bust_frame(fisher_body(rim), fisher_head(rim=rim, **hk), x, y, k)
