#!/usr/bin/env python3
"""Illustrations for 'El Sombrerón' (San Cristóbal de las Casas, Chiapas) — writes art/*.svg (2400x1350).
Reuses helpers of earlier videos (beso_art.py, chars.py, base_chars.py, qm_art.py, aguacate_art.py, pas_art.py = La Pascualita).
New here: the Sombrerón (tiny charro, enormous hat, silver guitar), Inés (long hair, braided hair, Chiapas blouse),
horses and mules with braided manes, Altos de Chiapas valley, Santo Domingo façade, plate of earth, scissors, braids.
Usage: python3 make_art.py [name ...]   then: node /home/claude/pipeline/render_svg.js art/*.svg"""
import sys, os, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '/home/claude/pipeline'); sys.path.insert(0, HERE)
from art import *
from chars import place, man_full, woman_full, strands, bust_frame, SIL, hair_carmen_front, brigida_bust
from base_chars import head, uid, grad_lin, grad_rad
import beso_art as BA
from beso_art import S, clouds, room_walls, candle_at, flame, table_wood, portrait_bg, MOONRIM
import qm_art as QM
import aguacate_art as AG
import pas_art as PA

A = os.path.join(HERE, "art"); os.makedirs(A, exist_ok=True)
ART = {}
def art(fn):
    ART[fn.__name__] = fn; return fn

WARM = "#ffcf8a"; RED = "#c8141a"; SILVER = "#dfe6ee"
SK_INES = dict(base="#c4926e", light="#dcac88", hi="#eec8a6", shadow="#86583e", deep="#462a1e")
inner = PA.inner


def crop(svgstr, k, cx, cy, extra=""):
    return S(f'<g transform="translate(1200,675) scale({k}) translate({-cx},{-cy})">{inner(svgstr)}</g>', extra)


# ===================================================================== braids
def braid(pts, w=14, col="#0c0806", hi="#4a3428", seed=1, op=1.0):
    """A plait following a polyline pts [(x,y),...]: alternating tilted lobes with a highlight on each."""
    r = random.Random(seed)
    out = ""
    seg = []
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        L_ = math.hypot(x1 - x0, y1 - y0); n = max(1, int(L_ / (w * 0.9)))
        for i in range(n):
            t = i / n; seg.append((x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, math.degrees(math.atan2(y1 - y0, x1 - x0))))
    for i, (x, y, a) in enumerate(seg):
        tilt = 35 if i % 2 else -35
        out += (f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{w*0.62:.1f}" ry="{w*0.36:.1f}" fill="{col}" '
                f'transform="rotate({a+tilt:.1f} {x:.1f} {y:.1f})" opacity="{op}"/>')
        out += (f'<ellipse cx="{x:.1f}" cy="{y-w*0.08:.1f}" rx="{w*0.36:.1f}" ry="{w*0.1:.1f}" fill="{hi}" '
                f'transform="rotate({a+tilt:.1f} {x:.1f} {y:.1f})" opacity="{0.55*op:.2f}"/>')
    if seg:
        x, y, a = seg[-1]
        out += f'<path d="M{x:.1f},{y:.1f} l{r.uniform(-4,4):.1f},{w*1.4:.1f} M{x:.1f},{y:.1f} l{r.uniform(-8,0):.1f},{w*1.2:.1f} M{x:.1f},{y:.1f} l{r.uniform(0,8):.1f},{w*1.2:.1f}" stroke="{col}" stroke-width="{w*0.18:.1f}" opacity="{op}"/>'
    return out


def wavy(x0, y0, x1, y1, amp, n=3, seed=0):
    r = random.Random(seed)
    pts = []
    for i in range(n * 4 + 1):
        t = i / (n * 4)
        pts.append((x0 + (x1 - x0) * t + math.sin(t * n * math.pi * 2 + seed) * amp * (0.4 + t), y0 + (y1 - y0) * t))
    return pts


# ===================================================================== Inés
def ines_hair_back(braided=False, seed=4, wind=0.0):
    r = random.Random(seed)
    s = ('<path d="M-96,-60 C-118,-150 -64,-182 0,-184 C64,-182 118,-150 96,-60 C130,80 170,300 230,640 '
         'L-230,640 C-170,300 -130,80 -96,-60 Z" fill="#0a0605"/>')
    if not braided:
        s += strands(r, [(-90, -40, -150, 200, -200, 620), (90, -40, 150, 200, 200, 620), (-60, 0, -110, 300, -120, 630),
                         (60, 0, 110, 300, 130, 630)], 14, "#2a1a12", (1.5, 3.5), (0.3, 0.7), 10)
    else:
        for i in range(9):
            x = -190 + i * 47
            s += braid(wavy(x * 0.45, -20, x, 640, 8, 2, i), 15, "#090504", "#5a4232", seed=i)
    return s


def ines_front_locks(braided=False, seed=6):
    r = random.Random(seed)
    s = ""
    if not braided:
        for side in (-1, 1):
            s += (f'<path d="M{side*74},-40 C{side*96},60 {side*120},200 {side*170},420 C{side*176},480 {side*150},520 {side*120},540 '
                  f'C{side*120},420 {side*96},250 {side*62},40 Z" fill="#0c0706"/>')
            s += strands(r, [(side * 76, -30, side * 110, 200, side * 150, 520)], 12, "#3a261a", (1.2, 2.6), (0.35, 0.8), 8)
    else:
        for side in (-1, 1):
            for j in range(5):
                x0 = side * (64 + j * 7); x1 = side * (110 + j * 22)
                s += braid(wavy(x0, -30 + j * 6, x1, 520 - j * 18, 6, 2, j + (3 if side > 0 else 0)), 11, "#0a0605", "#6a5040", seed=j)
    return s


def ines_blouse(g, rim):
    """white cotton blouse with embroidered flowers at the square neckline (Chiapas), rebozo on the shoulders"""
    s = (f'<defs>{grad_lin(g+"b", [(0, "#8a8a92", 1), (0.5, "#d8d4cc", 1), (0.85, "#f0ece4", 1), (1, "#c8c4bc", 1)], -340, 0, 340, 0)}'
         f'{grad_lin(g+"s", [(0, SK_INES["deep"], 1), (0.4, SK_INES["shadow"], 1), (0.75, SK_INES["base"], 1), (1, SK_INES["shadow"], 1)], -220, 0, 220, 0)}'
         f'{grad_lin(g+"r", [(0, "#14060a", 1), (0.6, "#3a1222", 1), (1, "#5a1c30", 1)], -300, 200, 300, 600)}</defs>')
    s += f'<path d="M-44,40 C-44,100 -58,150 -150,186 L150,186 C58,150 44,100 44,40 Z" fill="url(#{g}s)"/>'
    s += f'<path d="M-200,240 C-120,226 -60,214 0,214 C60,214 120,226 200,240 L200,260 L-200,260 Z" fill="url(#{g}s)"/>'
    s += f'<path d="M-250,226 C-170,236 -140,250 -130,262 L130,262 C140,250 170,236 250,226 C320,270 350,400 360,660 L-360,660 C-350,400 -320,270 -250,226 Z" fill="url(#{g}b)"/>'
    r = random.Random(3)
    cols = ["#c8142a", "#e8a020", "#2a7a3a", "#d0306a", "#3a5ab0"]
    for i in range(12):  # embroidered flowers along the neckline
        fx_ = -140 + i * 25.5; fy_ = 285 + (i % 2) * 14
        c = cols[i % len(cols)]
        for a in range(6):
            ang = math.radians(a * 60)
            s += f'<ellipse cx="{fx_+math.cos(ang)*7:.1f}" cy="{fy_+math.sin(ang)*7:.1f}" rx="6" ry="3.5" fill="{c}" transform="rotate({a*60} {fx_+math.cos(ang)*7:.1f} {fy_+math.sin(ang)*7:.1f})"/>'
        s += f'<circle cx="{fx_}" cy="{fy_}" r="3" fill="#f8e070"/>'
        s += f'<path d="M{fx_+8},{fy_+10} q8,10 0,22" stroke="#2a6a2a" stroke-width="3" fill="none"/>'
    s += '<path d="M-150,262 L150,262" stroke="#c8142a" stroke-width="5"/>'
    for d in ["M-200,330 Q-210,480 -190,660", "M200,330 Q210,480 190,660", "M-60,320 Q-50,480 -70,660", "M60,320 Q50,480 70,660"]:
        s += f'<path d="{d}" stroke="#6a6a74" stroke-width="10" fill="none" opacity="0.5" filter="url(#blur1)"/>'
    for side in (-1, 1):
        s += f'<path d="M{side*250},226 C{side*330},270 {side*370},420 {side*380},660 L{side*240},660 C{side*250},480 {side*240},330 {side*190},250 Z" fill="url(#{g}r)"/>'
        for i in range(5):
            s += f'<path d="M{side*(205+i*28)},{240+i*8} C{side*(245+i*26)},380 {side*(255+i*24)},520 {side*(245+i*24)},660" stroke="#7a2a44" stroke-width="2.5" fill="none" opacity="0.5"/>'
    if rim:
        s += f'<path d="M-250,226 C-330,270 -370,420 -380,660" stroke="{rim}" stroke-width="5" fill="none" opacity="0.5" filter="url(#blur1)"/>'
    return s


def ines_head(look=0.0, turn=0.0, lids=0.25, smile=0.2, eyes_closed=False, fear=False, rim="#9fc2e8", thin=False):
    s = head(look=look, smile=(-0.6 if fear else smile), lids=(0.0 if fear else lids), rim=rim, turn=turn, eyes_closed=eyes_closed,
             sk=SK_INES, headwrap=False, lips=(("#7a4a48", "#8a5a56") if thin else ("#7a3a36", "#9a4e48")), iris="#1e1008",
             earring=True, brow_w=0.85)
    if fear:
        s += '<ellipse cx="0" cy="74" rx="14" ry="10" fill="#2a0e0a"/>'
    if thin:  # dark rings under the eyes, hollow cheeks, pallor
        for x in (-31, 31):
            s += f'<path d="M{x-22},-2 Q{x},12 {x+22},-2" stroke="#4a2a3a" stroke-width="7" fill="none" opacity="0.55" filter="url(#blur1)"/>'
        for x in (-52, 52):
            s += f'<path d="M{x},20 Q{x*0.9},60 {x*0.7},88" stroke="#5a3a3a" stroke-width="12" fill="none" opacity="0.35" filter="url(#blur2)"/>'
        s += '<ellipse cx="0" cy="-10" rx="80" ry="125" fill="#c8d4e0" opacity="0.18"/>'
    s += hair_carmen_front(seed=3, loose=False, flower=False)
    return s


def ines_bust(x, y, k=1.0, rim="#9fc2e8", braided=False, **hk):
    g = uid("ib")
    back = f'<g transform="translate({x},{y}) scale({k})">{ines_hair_back(braided)}</g>'
    front = f'<g transform="translate({x},{y}) scale({k})">{ines_front_locks(braided)}</g>'
    return back + bust_frame(ines_blouse(g, rim), ines_head(rim=rim, **hk), x, y, k) + front


# ===================================================================== the Sombrerón (feet at 0,0; ~560 tall incl. hat)
def hat(cx=0, cy=0, k=1.0, rim=MOONRIM, emb=SILVER, tilt=0):
    """charro sombrero seen slightly from below/front: huge brim rolled up at the edges, tall crown, silver embroidery"""
    g = uid("ht")
    s = (f'<defs>{grad_lin(g+"c", [(0, "#020203", 1), (0.55, "#0c0c12", 1), (0.8, "#1c1c26", 1), (1, "#06060a", 1)], -80, 0, 80, 0)}'
         f'{grad_lin(g+"b", [(0, "#050508", 1), (0.5, "#14141c", 1), (1, "#050508", 1)], -260, 0, 260, 0)}</defs>')
    s += f'<g transform="translate({cx},{cy}) scale({k}) rotate({tilt})">'
    # crown
    s += f'<path d="M-78,-10 C-84,-90 -70,-170 -30,-200 C-12,-212 12,-212 30,-200 C70,-170 84,-90 78,-10 Z" fill="url(#{g}c)"/>'
    s += '<path d="M-30,-200 C-10,-180 10,-180 30,-200" stroke="#000" stroke-width="6" fill="none" opacity="0.7"/>'  # pinch
    s += f'<path d="M-78,-10 C-84,-90 -70,-170 -30,-200" stroke="{rim}" stroke-width="4" fill="none" opacity="0.6"/>'
    # band with silver zigzag
    s += '<path d="M-80,-14 C-40,-30 40,-30 80,-14 L80,-44 C40,-58 -40,-58 -80,-44 Z" fill="#08080c"/>'
    zz = "M-78,-30 " + " ".join(f"L{-78+i*13},{-30 + (-10 if i % 2 else 6)}" for i in range(1, 13))
    s += f'<path d="{zz}" stroke="{emb}" stroke-width="3" fill="none" opacity="0.85"/>'
    # brim: wide ellipse, underside darker, edges rolled up
    s += f'<path d="M-270,-40 C-250,10 -150,40 0,40 C150,40 250,10 270,-40 C282,-30 286,-6 270,10 C230,60 120,78 0,78 C-120,78 -230,60 -270,10 C-286,-6 -282,-30 -270,-40 Z" fill="#030305"/>'
    s += f'<path d="M-270,-40 C-250,10 -150,40 0,40 C150,40 250,10 270,-40 C240,-60 130,-70 0,-70 C-130,-70 -240,-60 -270,-40 Z" fill="url(#{g}b)"/>'
    s += f'<path d="M-270,-40 C-250,10 -150,40 0,40 C150,40 250,10 270,-40" stroke="{rim}" stroke-width="3.5" fill="none" opacity="0.55"/>'
    s += f'<path d="M-270,10 C-230,60 -120,78 0,78 C120,78 230,60 270,10" stroke="{rim}" stroke-width="5" fill="none" opacity="0.7"/>'
    # embroidery ring on the brim
    s += f'<ellipse cx="0" cy="-12" rx="200" ry="34" stroke="{emb}" stroke-width="3" fill="none" stroke-dasharray="10 7" opacity="0.7"/>'
    for i in range(18):
        a = i / 18 * math.pi * 2
        s += f'<circle cx="{math.cos(a)*230:.1f}" cy="{-12+math.sin(a)*42:.1f}" r="3.2" fill="{emb}" opacity="0.75"/>'
    s += '</g>'
    return s


def silver_guitar(x, y, ang=-25, k=1.0, glow_strings=True):
    g = uid("sg")
    s = (f'<defs>{grad_lin(g+"m", [(0, "#5a6470", 1), (0.35, "#c8d2dc", 1), (0.55, "#f4f8fc", 1), (0.8, "#8a96a4", 1), (1, "#4a525c", 1)], -90, -60, 90, 60)}</defs>')
    s += f'<g transform="translate({x},{y}) rotate({ang}) scale({k})">'
    s += f'<path d="M-40,-14 L-300,-10 L-300,10 L-40,14 Z" fill="#1a1a20"/>'  # neck
    for i in range(7):
        s += f'<path d="M{-80-i*30},-12 L{-80-i*30},12" stroke="#c8d0d8" stroke-width="2"/>'  # frets
    s += f'<path d="M-300,-20 L-350,-26 L-354,26 L-300,20 Z" fill="#c8d2dc"/>'  # head
    for i in range(3):
        s += f'<circle cx="{-312-i*14}" cy="-30" r="5" fill="#e8eef4"/><circle cx="{-312-i*14}" cy="30" r="5" fill="#e8eef4"/>'
    s += f'<path d="M-50,0 C-50,-60 -10,-80 30,-64 C60,-52 70,-70 110,-84 C170,-100 210,-50 210,0 C210,50 170,100 110,84 C70,70 60,52 30,64 C-10,80 -50,60 -50,0 Z" fill="url(#{g}m)"/>'
    s += f'<path d="M-50,0 C-50,-60 -10,-80 30,-64 C60,-52 70,-70 110,-84 C170,-100 210,-50 210,0" stroke="#ffffff" stroke-width="3" fill="none" opacity="0.6"/>'
    s += '<circle cx="60" cy="0" r="26" fill="#0a0a10"/><circle cx="60" cy="0" r="32" stroke="#6a7480" stroke-width="5" fill="none"/>'
    s += '<rect x="140" y="-30" width="14" height="60" fill="#2a2a30"/>'
    for i in range(6):
        yy = -10 + i * 4
        s += f'<path d="M-350,{yy*0.8:.1f} L148,{yy}" stroke="#ffffff" stroke-width="1.4" opacity="0.9"/>'
    if glow_strings:
        s += '<path d="M-330,0 L148,0" stroke="#cfe8ff" stroke-width="16" opacity="0.25" filter="url(#blur2)"/>'
    s += '</g>'
    return s


def sombreron_fig(rim=MOONRIM, eyes=None, guitar=True, fill="#050508", play=0.0):
    """tiny charro: stocky body ~330 tall, hat ~520 wide. Face hidden in the brim's shadow."""
    s = ""
    # boots with spurs
    for side, x in ((-1, -38), (1, 38)):
        s += f'<path d="M{x-24},-60 L{x+22},-60 L{x+24},-14 C{x+24*side+30*side},-12 {x+40*side},-4 {x+44*side},0 L{x-24*side if side<0 else x-24},0 Z" fill="#0a0a0e"/>'
        s += f'<path d="M{x-22},-8 L{x+42*side if side>0 else x+22},-8" stroke="{SILVER}" stroke-width="3" opacity="0.6"/>'
        sx = x - 30 * side
        s += f'<circle cx="{sx}" cy="-12" r="12" stroke="{SILVER}" stroke-width="3" fill="none"/>'
        for a in range(8):
            ang = a * math.pi / 4
            s += f'<path d="M{sx},{-12} l{math.cos(ang)*14:.1f},{math.sin(ang)*14:.1f}" stroke="{SILVER}" stroke-width="2"/>'
    # trousers with silver botonadura on the outer seams
    s += f'<path d="M-66,-200 L-60,-60 L-16,-60 L-4,-160 L4,-160 L16,-60 L60,-60 L66,-200 Z" fill="{fill}"/>'
    for side in (-1, 1):
        for i in range(7):
            yy = -190 + i * 19
            s += f'<circle cx="{side*(64-i*0.6):.1f}" cy="{yy}" r="5" fill="{SILVER}"/><circle cx="{side*(64-i*0.6)-1.5:.1f}" cy="{yy-1.5}" r="1.8" fill="#fff"/>'
    # short charro jacket
    s += f'<path d="M-92,-300 C-100,-260 -94,-220 -78,-196 L78,-196 C94,-220 100,-260 92,-300 C60,-322 -60,-322 -92,-300 Z" fill="{fill}"/>'
    s += f'<path d="M-30,-310 L0,-250 L30,-310 Z" fill="#e8e4dc"/>'  # shirt
    s += f'<path d="M-24,-300 C-10,-290 10,-290 24,-300 L18,-284 L0,-292 L-18,-284 Z" fill="#a81020"/>'  # moño (bow tie) in red
    for side in (-1, 1):
        for i in range(3):
            s += f'<circle cx="{side*42}" cy="{-280+i*26}" r="6" fill="{SILVER}"/>'
        s += f'<path d="M{side*90},-290 C{side*96},-260 {side*92},-226 {side*78},-200" stroke="{SILVER}" stroke-width="3" fill="none" stroke-dasharray="6 6" opacity="0.7"/>'
    # belt with big buckle
    s += f'<rect x="-74" y="-206" width="148" height="16" fill="#1a1612"/><rect x="-14" y="-210" width="28" height="24" fill="none" stroke="{SILVER}" stroke-width="4"/>'
    # arms + hands
    if guitar:
        s += f'<path d="M-90,-296 C-120,-260 -126,-220 -100,-196 L-70,-206 C-84,-230 -78,-260 -66,-284 Z" fill="{fill}"/>'
        s += f'<path d="M90,-296 C130,-276 150,-250 160,-226 L136,-212 C124,-236 110,-256 72,-270 Z" fill="{fill}"/>'
        s += silver_guitar(-10, -214, -16 + play * 4, 0.62)
        s += '<ellipse cx="-96" cy="-200" rx="14" ry="11" fill="#8a6248"/>'  # strumming hand
        s += '<ellipse cx="150" cy="-224" rx="12" ry="10" fill="#8a6248"/>'
        s += f'<circle cx="-92" cy="-206" r="3" fill="#f0c860"/>'
    else:
        s += f'<path d="M-90,-296 C-118,-250 -120,-200 -110,-160 L-86,-160 C-92,-200 -86,-250 -70,-280 Z" fill="{fill}"/>'
        s += f'<path d="M90,-296 C118,-250 120,-200 110,-160 L86,-160 C92,-200 86,-250 70,-280 Z" fill="{fill}"/>'
        s += '<ellipse cx="-98" cy="-150" rx="14" ry="12" fill="#8a6248"/><ellipse cx="98" cy="-150" rx="14" ry="12" fill="#8a6248"/>'
    # head in shadow under the brim
    s += '<path d="M-40,-318 C-44,-360 -30,-384 0,-386 C30,-384 44,-360 40,-318 C30,-306 -30,-306 -40,-318 Z" fill="#020203"/>'
    s += '<path d="M-26,-322 C-12,-312 12,-312 26,-322" stroke="#3a2a22" stroke-width="3" fill="none" opacity="0.6"/>'  # chin glint
    s += hat(0, -380, 1.0, rim=rim)
    if eyes:
        for ex in (-22, 22):
            s += f'<circle cx="{ex}" cy="-318" r="16" fill="url(#redglow)" opacity="1"/><ellipse cx="{ex}" cy="-318" rx="5" ry="3.2" fill="{eyes}"/>'
    else:
        for ex in (-22, 22):
            s += f'<ellipse cx="{ex}" cy="-318" rx="3" ry="1.6" fill="#8aa0c0" opacity="0.5"/>'

    # rim light on the body edges
    s += f'<path d="M-92,-300 C-100,-260 -94,-220 -78,-196 M-66,-200 L-60,-60" stroke="{rim}" stroke-width="4" fill="none" opacity="0.6"/>'
    return s


# ===================================================================== horses / mules
def horse_shape(x, y, h, color="#030405", rim=None, facing=1, mule=False, braids=0, packs=False, seed=1):
    s = h / 400.0
    d = ("M-245,-385 C-150,-372 -40,-368 60,-385 C100,-395 130,-410 150,-440 C185,-500 215,-545 248,-568 L256,-600 L268,-570 "
         "C290,-560 310,-530 330,-490 C345,-460 362,-440 366,-424 C368,-410 352,-402 338,-406 C318,-412 300,-420 286,-432 "
         "C270,-440 255,-440 240,-450 C222,-420 205,-370 186,-320 C180,-290 170,-268 160,-255 "
         "L168,-140 L172,-30 L182,0 L150,0 L152,-30 L146,-140 L132,-240 "
         "L118,-240 L110,-140 L104,-30 L112,0 L84,0 L86,-30 L92,-140 L96,-245 "
         "C40,-250 -60,-250 -140,-262 L-150,-160 L-170,-110 L-160,-30 L-150,0 L-178,0 L-184,-30 L-196,-110 L-186,-170 "
         "L-205,-180 L-238,-118 L-232,-30 L-222,0 L-252,0 L-258,-30 L-264,-120 L-258,-200 C-272,-260 -272,-340 -245,-385 Z")
    tail = "M-245,-378 C-290,-370 -318,-300 -318,-200 C-316,-150 -300,-120 -290,-110 C-296,-170 -290,-250 -262,-320 Z"
    parts = f'<path d="{d}"/><path d="{tail}"/>'
    if mule:
        parts += '<path d="M246,-570 L232,-660 L262,-588 Z"/><path d="M262,-574 L262,-668 L280,-580 Z"/>'
    else:
        parts += '<path d="M150,-440 C185,-500 215,-545 248,-568 C236,-540 214,-500 196,-470 C180,-450 168,-430 160,-420 Z"/>'
    if packs:
        parts += '<path d="M-150,-380 C-160,-470 40,-470 40,-385 Z"/><rect x="-170" y="-400" width="90" height="150" rx="30"/><rect x="-60" y="-400" width="90" height="150" rx="30"/>'
    body = f'<g transform="translate({x},{y}) scale({s*facing},{s})">{parts}</g>'
    out = ""
    if rim:
        out += f'<g fill="{rim}" filter="url(#blur1)" opacity="0.9"><g transform="translate({x+4*facing},{y-3}) scale({s*facing},{s})">{parts}</g></g>'
    out += f'<g fill="{color}">{body}</g>'
    if packs:  # coal lumps on top of the sacks
        r = random.Random(seed)
        for i in range(10):
            px, py = r.uniform(-150, 20), r.uniform(-470, -440)
            out += f'<g transform="translate({x},{y}) scale({s*facing},{s})"><circle cx="{px:.0f}" cy="{py:.0f}" r="{r.uniform(10,18):.0f}" fill="#141418"/><circle cx="{px-3:.0f}" cy="{py-4:.0f}" r="4" fill="#6a7080" opacity="0.6"/></g>'
    if braids:
        r = random.Random(seed)
        for i in range(braids):
            t = (i + 0.5) / braids
            bx = 150 + (248 - 150) * t; by = -440 + (-568 + 440) * t
            L_ = r.uniform(50, 80)
            pts = [(bx, by), (bx - 14, by + L_ * 0.5), (bx - 10, by + L_)]
            out += f'<g transform="translate({x},{y}) scale({s*facing},{s})">{braid(pts, 12, "#060608", rim or "#3a4250", seed=i)}</g>'
        for i in range(4):  # braided tail
            pts = [(-250 - i * 8, -370), (-285 - i * 6, -300), (-300 - i * 4, -200), (-296 - i * 4, -130)]
            out += f'<g transform="translate({x},{y}) scale({s*facing},{s})">{braid(pts, 14, "#060608", rim or "#3a4250", seed=10 + i)}</g>'
    return out


# ===================================================================== backgrounds: Altos de Chiapas
def pines(x0, x1, ybase, seed, col, hmin=60, hmax=160, n=40):
    r = random.Random(seed); s = ""
    for _ in range(n):
        x = r.uniform(x0, x1); h = r.uniform(hmin, hmax); w = h * 0.32
        y = ybase + r.uniform(-10, 10)
        s += f'<path d="M{x:.0f},{y-h:.0f} L{x+w:.0f},{y:.0f} L{x-w:.0f},{y:.0f} Z" fill="{col}"/>'
    return s


def town(ybase, seed, mood="night", n=34, x0=0, x1=2400, k=1.0):
    r = random.Random(seed); s = ""
    wall = {"night": ["#1a1e2c", "#22263a", "#1c1a28"], "dawn": ["#5a4a58", "#6a5462", "#4a4052"], "day": ["#d8c8a8", "#e0b890", "#c8a888"]}[mood]
    roof = {"night": "#2a1612", "dawn": "#6a3022", "day": "#a8482a"}[mood]
    xs = sorted(r.uniform(x0, x1) for _ in range(n))
    for x in xs:
        w = r.uniform(90, 170) * k; h = r.uniform(50, 90) * k; y = ybase + r.uniform(-30, 30) * k
        s += f'<rect x="{x:.0f}" y="{y-h:.0f}" width="{w:.0f}" height="{h:.0f}" fill="{r.choice(wall)}"/>'
        s += f'<path d="M{x-10*k:.0f},{y-h:.0f} L{x+w/2:.0f},{y-h-34*k:.0f} L{x+w+10*k:.0f},{y-h:.0f} Z" fill="{roof}"/>'
        s += f'<path d="M{x-10*k:.0f},{y-h:.0f} L{x+w+10*k:.0f},{y-h:.0f}" stroke="#000" stroke-width="{3*k:.1f}" opacity="0.5"/>'
        if mood != "day" and r.random() < 0.5:
            s += f'<rect x="{x+w*0.4:.0f}" y="{y-h*0.6:.0f}" width="{12*k:.0f}" height="{18*k:.0f}" fill="#ffc865" opacity="{0.9 if mood=="night" else 0.5}"/>'
    return s


def sto_domingo(x, yb, k=1.0, mood="night"):
    """baroque façade of Santo Domingo (San Cristóbal): ochre/pink stone, three bodies, columns, niches, central window"""
    stone = {"night": ("#4a3a40", "#2a2028", "#6a5258"), "day": ("#d8a078", "#b07858", "#f0c098"), "dawn": ("#8a6068", "#5a4048", "#b08088")}[mood]
    s = f'<g transform="translate({x},{yb}) scale({k})">'
    s += f'<path d="M-330,0 L-330,-520 L-260,-520 L-260,-640 L-120,-640 C-100,-720 100,-720 120,-640 L260,-640 L260,-520 L330,-520 L330,0 Z" fill="{stone[0]}"/>'
    s += f'<rect x="-330" y="-520" width="660" height="520" fill="#000" filter="url(#plaster)" opacity="0.4"/>'
    for yy in (-180, -360, -520):
        s += f'<rect x="-340" y="{yy-10}" width="680" height="18" fill="{stone[2]}"/>'
    for col in (-250, -150, 150, 250):
        for yy in (-180, -360):
            s += f'<rect x="{col-14}" y="{yy}" width="28" height="170" fill="{stone[2]}"/>'
            for j in range(6):
                s += f'<path d="M{col-14},{yy+20+j*25} q14,-10 28,0" stroke="{stone[1]}" stroke-width="5" fill="none"/>'  # solomonic twist
        for yy in (-170,):
            pass
    for nx in (-200, 200):
        for ny in (-300, -470):
            s += f'<path d="M{nx-30},{ny+90} L{nx-30},{ny} Q{nx},{ny-40} {nx+30},{ny} L{nx+30},{ny+90} Z" fill="{stone[1]}"/>'
            s += f'<path d="M{nx},{ny+80} C{nx-12},{ny+40} {nx-10},{ny+20} {nx},{ny+10} C{nx+10},{ny+20} {nx+12},{ny+40} {nx},{ny+80} Z" fill="{stone[2]}" opacity="0.6"/>'
    s += f'<path d="M-90,0 L-90,-130 Q0,-210 90,-130 L90,0 Z" fill="{stone[1]}"/><path d="M-70,0 L-70,-125 Q0,-190 70,-125 L70,0 Z" fill="#1a0e08"/>'
    s += f'<circle cx="0" cy="-440" r="54" fill="{stone[1]}"/><circle cx="0" cy="-440" r="40" fill="{"#ffc865" if mood=="night" else "#2a1a14"}" opacity="0.85"/>'
    s += f'<path d="M0,-720 L0,-780 M-20,-760 L20,-760" stroke="{stone[2]}" stroke-width="10"/>'
    for i in range(30):  # carved ornament dots
        r = random.Random(i)
        s += f'<circle cx="{r.uniform(-320,320):.0f}" cy="{r.uniform(-630,-20):.0f}" r="{r.uniform(3,6):.0f}" fill="{stone[2]}" opacity="0.5"/>'
    s += '</g>'
    return s


def valley_svg(mood="night", seed=1, moon_xy=(1750, 260)):
    if mood == "night":
        s = sky("#030712", "#1a2c42", "#0c1828") + stars(200, seed, 650) + moon(moon_xy[0], moon_xy[1], 85)
        cols = ("#0e1a28", "#0a1420", "#071018", "#04080e")
    else:
        s = sky("#2a2c4a", "#e0a080", "#8a6a8a") + glow(1800, 760, 900, "warm", 0.5)
        cols = ("#4a4a64", "#3a3a54", "#2a2a40", "#1a1a2c")
    s += ridge(560, 160, cols[0], 4 + seed, step=30) + ridge(660, 110, cols[1], 7 + seed, step=30)
    s += pines(0, 2400, 700, 3 + seed, cols[1], 30, 70, 90)
    s += clouds(10, 640, 760, 5 + seed, "#b8c8dc" if mood == "night" else "#f0d0c0", (0.12, 0.25), (300, 700), (30, 70))
    s += ridge(820, 50, cols[2], 9 + seed, step=40)
    s += town(900, 11 + seed, "night" if mood == "night" else "dawn", 40, 0, 2400, 0.9)
    s += sto_domingo(900, 900, 0.32, "night" if mood == "night" else "dawn")
    s += town(1010, 12 + seed, "night" if mood == "night" else "dawn", 30, 0, 2400, 1.2)
    s += clouds(14, 960, 1150, 13 + seed, "#b8c8dc" if mood == "night" else "#f0d8c8", (0.1, 0.22), (300, 800), (40, 90))
    s += f'<path d="M0,1100 C400,1060 900,1120 1400,1090 C1800,1070 2100,1110 2400,1090 L2400,1350 L0,1350 Z" fill="{cols[3]}"/>'
    s += pines(0, 700, 1120, 21 + seed, cols[3], 120, 300, 12) + pines(1800, 2400, 1120, 22 + seed, cols[3], 120, 300, 12)
    return s


@art
def valley_night(): return S(valley_svg("night", 1))
@art
def valley_night2(): return S(valley_svg("night", 4, (600, 220)), QM.fog_band(1050, 0.4, 7))
@art
def valley_dawn(): return S(valley_svg("dawn", 2))


@art
def street_sc(): return S(QM.persp_street("night", seed=41), QM.fog_band(1180, 0.3, 42))
@art
def street_sc2(): return S(QM.persp_street("night", seed=43, whispers=False), QM.fog_band(1150, 0.4, 44), '<rect width="2400" height="1350" fill="#02040c" opacity="0.2"/>')
@art
def alley_sc(): return S(AG.callejon("night", niche=True, tree=False, seed=45))


@art
def street_shadow():
    s = QM.persp_street("night", seed=47)
    # hat shadow on the cobbles + little body shadow + guitar neck
    s += '<g opacity="0.82" filter="url(#blur2)"><ellipse cx="1250" cy="1170" rx="330" ry="70" fill="#000"/>'
    s += '<path d="M1210,1180 L1290,1180 L1300,1300 L1200,1300 Z" fill="#000"/><path d="M1260,1230 L1480,1200 L1484,1212 L1264,1244 Z" fill="#000"/></g>'
    return S(s, QM.fog_band(1200, 0.3, 48))


@art
def plaza_sc():
    s = sky("#5a7aa8", "#e8c89a", "#a8b8c8")
    s += ridge(700, 80, "#5a6a7a", 3, step=40) + pines(0, 2400, 760, 4, "#4a5a6a", 40, 80, 50)
    s += town(900, 6, "day", 18, 0, 700, 1.6) + town(900, 7, "day", 18, 1700, 2400, 1.6)
    s += sto_domingo(1200, 1010, 1.05, "day")
    s += '<rect x="0" y="1000" width="2400" height="350" fill="#b8a080"/>'
    s += cobbles(1010, 1350, "#9a8468", 5, wet=False)
    r = random.Random(3)
    for i in range(9):  # churchgoers leaving mass
        x = r.uniform(200, 1100) if i % 2 else r.uniform(1300, 2200)
        k = r.uniform(0.2, 0.27)
        s += place(woman_full(rebozo_head=True, rim="#fff0d0", fill="#2a1c18") if i % 3 else man_full(hat=True, cape=False, rim="#fff0d0", fill="#2a1c18"), x, 1060 + r.uniform(0, 80), k)
    return S(s)


@art
def church_ext():
    s = sky("#040814", "#1a2a40") + stars(80, 9, 400) + moon(500, 200, 70)
    s += town(960, 8, "night", 14, 0, 700, 1.6) + town(960, 9, "night", 14, 1700, 2400, 1.6)
    s += sto_domingo(1200, 1060, 1.1, "night") + glow(1200, 600, 500, "warm", 0.25)
    s += '<rect x="0" y="1050" width="2400" height="300" fill="#141822"/>' + cobbles(1060, 1350)
    return S(s, QM.fog_band(1150, 0.35, 12))


# ----------------------------------------------------- the house of Inés
HOUSE = BA.ART["house_facade"]
@art
def house_window(): return S(inner(HOUSE()), glow(1200, 480, 420, "warm", 0.4), QM.fog_band(1260, 0.35, 15))
@art
def house_window2():
    return S(inner(HOUSE()), '<rect width="2400" height="1350" fill="#020610" opacity="0.35"/>', moon(400, 90, 60),
             glow(1200, 480, 380, "warm", 0.5), QM.fog_band(1180, 0.4, 16), QM.fog_band(1290, 0.5, 17))
@art
def l_window_glow(): return S(glow(1200, 480, 520, "warm", 0.45))
@art
def l_sombreron(): return S(place(sombreron_fig(), 1560, 1290, 0.95))
@art
def l_lamp_glow(): return QM.ART["l_lamp_glow"]()
@art
def l_candle_glow(): return PA.ART["l_candle_glow"]()
@art
def l_fog(): return PA.ART["l_fog"]()


@art
def l_notes():
    r = random.Random(5); s = ""
    for i in range(14):
        x, y = r.uniform(1300, 1900), r.uniform(500, 1050); k = r.uniform(0.7, 1.4)
        s += (f'<g transform="translate({x:.0f},{y:.0f}) scale({k:.2f}) rotate({r.uniform(-20,20):.0f})" opacity="{r.uniform(0.4,0.9):.2f}">'
              f'<ellipse cx="0" cy="0" rx="13" ry="9" fill="#e8f2ff" transform="rotate(-25)"/><path d="M11,-4 L11,-52 Q24,-44 30,-30" stroke="#e8f2ff" stroke-width="4" fill="none"/></g>')
        s += glow(x, y, 40, "white", 0.25)
    return S(s)


@art
def sombreron_full():
    s = QM.persp_street("night", seed=51)
    s += '<rect width="2400" height="1350" fill="#020510" opacity="0.25"/>'
    return S(s, QM.fog_band(1240, 0.4, 52))
@art
def sombreron_full2(): return S(AG.callejon("night", niche=False, tree=False, seed=53), '<rect width="2400" height="1350" fill="#020510" opacity="0.2"/>', QM.fog_band(1240, 0.4, 54))


def sombreron_bust_svg(eyes=None, k=2.5, cx=1200, cy=1560, rim=MOONRIM, bg="#04070e", tilt=0):
    s = f'<rect width="2400" height="1350" fill="{bg}"/>' + glow(1200, 300, 1100, "moon", 0.5)
    s += f'<g transform="translate({cx},{cy}) scale({k}) rotate({tilt})">{sombreron_fig(rim=rim, eyes=eyes, guitar=False)}</g>'
    return s


@art
def sombreron_close(): return S(sombreron_bust_svg(eyes=None), QM.fog_band(1300, 0.3, 61))
@art
def sombreron_eyes():
    return S('<rect width="2400" height="1350" fill="#0a0204"/>' + glow(1200, 500, 1200, "red", 0.35) +
             f'<g transform="translate(1200,2250) scale(5.2)">{sombreron_fig(rim="#ff7050", eyes="#ffd0a0", guitar=False)}</g>')
@art
def sombreron_eyes2():
    return S('<rect width="2400" height="1350" fill="#06020a"/>' + glow(1100, 400, 1100, "red", 0.3) +
             f'<g transform="translate(1100,2420) scale(6.0) rotate(-8)">{sombreron_fig(rim="#ff9070", eyes="#fff0d0", guitar=False)}</g>')
@art
def sombreron_cry():
    s = sombreron_bust_svg(eyes=None, k=2.6, cy=1300, rim="#bcd0ff", bg="#03050c", tilt=6)
    s += '<rect width="2400" height="1350" fill="#0a1a3a" opacity="0.25"/>'
    s += f'<g transform="translate(1600,1050) rotate(30)">{silver_guitar(0, 0, 0, 1.6, False)}</g>'
    for i in range(6):  # snapped strings
        s += f'<path d="M{1500+i*14},{900+i*6} C{1450+i*10},{820} {1520-i*8},{760} {1460+i*20},{700}" stroke="#e8f2ff" stroke-width="2" fill="none" opacity="0.8"/>'
    return S(s, QM.fog_band(1250, 0.35, 62))


@art
def hat_brim():
    s = '<rect width="2400" height="1350" fill="#03060c"/>' + glow(1500, 200, 1200, "moon", 0.55)
    s += hat(1200, 760, 3.6, rim="#cfe0ff")
    s += '<path d="M1040,1040 C1060,1200 1340,1200 1360,1040 Z" fill="#010102"/>'
    return S(s, clouds(10, 1000, 1350, 64, "#b0c4d8", (0.06, 0.16), (300, 700), (40, 100)))


@art
def guitar_close():
    s = '<rect width="2400" height="1350" fill="#04070e"/>' + glow(1300, 500, 1000, "moon", 0.45)
    s += f'<path d="M0,1350 L0,900 C400,860 900,1000 1300,1350 Z" fill="#060608"/>'  # sleeve with silver buttons
    for i in range(6):
        s += f'<circle cx="{300+i*130}" cy="{1010+i*42}" r="16" fill="{SILVER}"/>'
    s += silver_guitar(1300, 760, -12, 3.2)
    # little hand with gold ring strumming
    s += '<path d="M1460,860 C1500,820 1580,820 1600,860 C1620,900 1580,960 1520,960 C1470,958 1440,910 1460,860 Z" fill="#8a6248"/>'
    for i in range(3):
        s += f'<path d="M{1500+i*28},880 C{1500+i*28},920 {1495+i*28},950 {1490+i*28},980" stroke="#6a4430" stroke-width="22" stroke-linecap="round"/>'
    s += '<circle cx="1530" cy="905" r="12" stroke="#f0c860" stroke-width="7" fill="none"/>'
    return S(s)


# ----------------------------------------------------- horses
def stable_svg(dark=False):
    s = '<rect width="2400" height="1350" fill="#140e0a"/>'
    for i in range(16):
        s += f'<rect x="{i*150}" y="0" width="140" height="1100" fill="{"#2a1e14" if i%2 else "#24180e"}"/><path d="M{i*150},0 L{i*150},1100" stroke="#0a0604" stroke-width="10"/>'
    s += '<rect width="2400" height="1100" fill="#000" filter="url(#plaster)" opacity="0.35"/>'
    s += '<rect x="0" y="180" width="2400" height="40" fill="#0e0804"/><rect x="0" y="1080" width="2400" height="270" fill="#2a2010"/>'
    r = random.Random(4)
    for i in range(300):
        x = r.uniform(0, 2400); y = r.uniform(1090, 1350)
        s += f'<path d="M{x:.0f},{y:.0f} l{r.uniform(-30,30):.0f},{r.uniform(-8,8):.0f}" stroke="#a88a40" stroke-width="2" opacity="0.6"/>'
    s += '<path d="M1700,300 L1700,1100 M1700,640 L2400,640 M1700,860 L2400,860" stroke="#0e0804" stroke-width="30"/>'
    s += QM.ART["l_lamp_glow"]().split(">", 1)[1].rsplit("</svg>", 1)[0] if False else ""
    s += lamp(452, 520, 120, True) if False else f'<rect x="440" y="420" width="24" height="60" fill="#1a1008"/>' + glow(452, 470, 300, "warm", 0.8) + candle(452, 470, 40, 14)
    s += horse_shape(1150, 1150, 640, "#06050a", rim="#ffb860", facing=1, braids=14, seed=3)
    s += horse_shape(2150, 1120, 520, "#08060a", rim="#ffb860", facing=-1, braids=9, seed=5)
    if dark:
        s += '<rect width="2400" height="1350" fill="#02040c" opacity="0.4"/>'
    return s


@art
def stable(): return S(stable_svg())


@art
def mane_close():
    s = '<rect width="2400" height="1350" fill="#04070e"/>' + glow(1700, 250, 1100, "moon", 0.6)
    crest = lambda t: (-100 + 2000 * t, 1250 - 1150 * math.sin(t * math.pi / 2) ** 0.8)
    top = " ".join(f"L{crest(i/40)[0]:.0f},{crest(i/40)[1]:.0f}" for i in range(41))
    s += f'<path d="M-100,1350 {top} C2000,120 2120,200 2080,330 C1950,700 1600,1050 1400,1350 Z" fill="#0b0a10"/>'
    s += f'<path d="M{crest(0)[0]:.0f},{crest(0)[1]:.0f} {top}" stroke="#a8c4e8" stroke-width="12" fill="none" opacity="0.6" filter="url(#blur1)"/>'
    s += '<path d="M400,1300 C800,950 1200,700 1700,520" stroke="#1c1c28" stroke-width="60" fill="none" opacity="0.6" filter="url(#blur3)"/>'
    s += '<path d="M1880,170 L1930,40 L1960,180 Z" fill="#0b0a10" stroke="#a8c4e8" stroke-width="5"/>'
    s += '<path d="M2080,330 C2200,420 2300,520 2340,620 C2300,680 2200,660 2150,600 C2100,520 2020,460 1990,420 Z" fill="#0b0a10"/>'
    s += '<path d="M2080,330 C2200,420 2300,520 2340,620" stroke="#a8c4e8" stroke-width="6" fill="none" opacity="0.5"/>'
    s += '<ellipse cx="1960" cy="300" rx="40" ry="26" fill="#000"/><circle cx="1972" cy="294" r="9" fill="#e8f0ff"/>'
    for i in range(16):
        t = 0.04 + i * 0.055
        bx, by = crest(t)
        L_ = 260 + (i % 3) * 50
        pts = [(bx, by - 10), (bx + 40, by + L_ * 0.5), (bx + 25, by + L_)]
        s += f'<path d="M{bx:.0f},{by:.0f} L{bx+30:.0f},{by+L_:.0f}" stroke="#000" stroke-width="40" opacity="0.5" filter="url(#blur2)"/>'
        s += braid(pts, 40, "#0a0a10", "#a8c4ee", seed=i)
    return S(s)


@art
def corral_dawn():
    s = sky("#2a3048", "#c89080", "#6a6080") + ridge(700, 120, "#3a3a50", 3, step=40) + pines(0, 2400, 760, 2, "#2a2a40", 40, 90, 60)
    s += clouds(10, 700, 860, 4, "#f0d0c0", (0.15, 0.3), (300, 700), (30, 70))
    s += '<rect x="0" y="880" width="2400" height="470" fill="#2a2228"/>'
    for x in range(0, 2400, 160):  # wooden fence
        s += f'<rect x="{x}" y="860" width="22" height="200" fill="#120c0c"/>'
    s += '<rect x="0" y="900" width="2400" height="16" fill="#120c0c"/><rect x="0" y="980" width="2400" height="16" fill="#120c0c"/>'
    s += horse_shape(700, 1250, 440, "#0a0810", rim="#f0b090", braids=12, seed=7)
    s += horse_shape(1500, 1200, 380, "#0a0810", rim="#f0b090", facing=-1, braids=10, seed=8)
    s += place(man_full(hat=True, cape=False, rim="#f0b090", fill="#0a0810"), 1950, 1260, 0.46)
    return S(s)


@art
def road_mules():
    s = sky("#1a2240", "#c87a5a", "#5a4a6a") + glow(1900, 760, 700, "warm", 0.5)
    s += ridge(640, 140, "#2a2840", 5, step=30) + ridge(760, 90, "#1c1a2c", 8, step=30) + pines(0, 2400, 800, 9, "#141220", 50, 120, 60)
    s += '<path d="M0,1100 C600,1000 1200,960 2400,900 L2400,1350 L0,1350 Z" fill="#0e0c16"/>'
    s += '<path d="M0,1180 C700,1080 1400,1020 2400,960 L2400,1020 C1500,1080 800,1150 0,1260 Z" fill="#3a2e2a"/>'
    return S(s)


@art
def l_mules():
    s = ""
    for i in range(4):
        s += horse_shape(500 + i * 330, 1215 - i * 40, 210 - i * 10, "#08060a", rim="#ffb080", mule=True, packs=True, seed=i)
    s += place(sombreron_fig(rim="#ffb080"), 1720, 1080, 0.42)
    return S(s)


@art
def post_mules():
    s = inner(HOUSE()) + '<rect width="2400" height="1350" fill="#020510" opacity="0.2"/>'
    s += '<rect x="1630" y="900" width="30" height="380" fill="#1a120a"/><rect x="1622" y="900" width="46" height="20" fill="#2a1e12"/>'
    s += '<path d="M1660,960 C1740,1000 1800,990 1860,960" stroke="#5a4a30" stroke-width="5" fill="none"/>'
    for i in range(3):
        s += horse_shape(1950 + i * 170, 1300 + i * 8, 230, "#06050a", rim=MOONRIM, mule=True, packs=True, facing=-1, seed=20 + i)
    return S(s, QM.fog_band(1270, 0.35, 21))


@art
def rider_ridge():
    s = sky("#1a2238", "#b88a8a", "#4a4a64") + glow(1900, 700, 700, "warm", 0.35)
    s += ridge(760, 130, "#2a2a40", 3, step=30) + pines(0, 2400, 800, 4, "#1c1c2c", 40, 90, 50)
    s += '<path d="M0,1000 C500,900 1200,860 2400,880 L2400,1350 L0,1350 Z" fill="#0a0a12"/>'
    s += clouds(12, 1000, 1200, 6, "#e0d0d0", (0.1, 0.22), (300, 700), (40, 80))
    return S(s)


@art
def l_rider():
    s = horse_shape(700, 1000, 300, "#040306", rim="#f0b0a0", facing=1)
    s += place(sombreron_fig(rim="#f0b0a0", guitar=False), 690, 775, 0.42)
    return S(s)


# ----------------------------------------------------- Inés and the women
@art
def ines_portrait(): return S(portrait_bg("candle"), ines_bust(1200, 560, 1.75, rim="#ffb860", look=0.15, lids=0.3, smile=0.35))
@art
def ines_window(): return S(portrait_bg("moon"), ines_bust(1200, 600, 1.8, rim=MOONRIM, look=0.6, turn=0.25, lids=0.35, smile=0.05),
                            '<rect x="0" y="0" width="2400" height="1350" fill="none" stroke="#0a0604" stroke-width="160"/>')
@art
def ines_window2(): return S(portrait_bg("moon"), ines_bust(1200, 620, 1.9, rim=MOONRIM, look=-0.5, turn=-0.2, lids=0.45, smile=0.0),
                             *[f'<rect x="{x}" y="0" width="22" height="1350" fill="#06080c"/>' for x in (300, 520, 1880, 2100)])
@art
def ines_braids(): return S(portrait_bg("moon"), ines_bust(1200, 560, 1.75, rim=MOONRIM, braided=True, look=0.0, lids=0.35, smile=-0.05))
@art
def ines_braids2(): return S(portrait_bg("candle"), ines_bust(1200, 580, 1.85, rim="#ffb860", braided=True, look=-0.35, turn=-0.15, lids=0.3, smile=-0.2))
@art
def ines_thin(): return S(portrait_bg("ghost"), ines_bust(1200, 560, 1.75, rim="#c8d8ff", braided=True, thin=True, look=0.3, lids=0.5, smile=-0.25))
@art
def ines_fear(): return S(portrait_bg("candle"), ines_bust(1200, 560, 1.75, rim="#ffb860", braided=True, thin=True, fear=True, look=-0.4, turn=-0.2))


@art
def ines_sleep():
    s = '<rect width="2400" height="1350" fill="#060a14"/>' + glow(1500, 300, 1000, "moon", 0.5)
    s += '<path d="M0,800 C600,760 1800,760 2400,800 L2400,1350 L0,1350 Z" fill="#c8ccd8"/>'  # sheet
    s += '<path d="M0,800 C600,760 1800,760 2400,800 L2400,900 C1800,860 600,860 0,900 Z" fill="#9aa0b4"/>'
    s += '<ellipse cx="1150" cy="760" rx="520" ry="160" fill="#e8e8f0"/>'  # pillow
    s += '<ellipse cx="1150" cy="790" rx="500" ry="110" fill="#b8bccc" opacity="0.5"/>'
    s += f'<g transform="translate(1150,680) rotate(-80) scale(1.7)">{ines_hair_back(True)}</g>'
    s += f'<g transform="translate(1150,680) rotate(-80) scale(1.7)">{ines_head(eyes_closed=True, smile=0.4, rim=MOONRIM)}</g>'
    s += '<path d="M0,960 C600,920 1800,940 2400,980 L2400,1350 L0,1350 Z" fill="#7a2a3a"/>'  # blanket
    s += '<path d="M0,960 C600,920 1800,940 2400,980" stroke="#c8d8ff" stroke-width="4" fill="none" opacity="0.5"/>'
    return S(s, '<rect width="2400" height="1350" fill="#0a1830" opacity="0.25"/>')


@art
def braids_pillow():
    s = '<rect width="2400" height="1350" fill="#0a0e18"/>' + glow(1300, 400, 1200, "moon", 0.45)
    s += '<rect x="0" y="0" width="2400" height="1350" fill="#d8dce6" opacity="0.85"/>'
    r = random.Random(2)
    for i in range(30):  # cloth folds
        s += f'<path d="M{r.uniform(0,2400):.0f},{r.uniform(0,1350):.0f} q{r.uniform(-200,200):.0f},{r.uniform(-60,60):.0f} {r.uniform(-400,400):.0f},{r.uniform(-30,30):.0f}" stroke="#a0a6b8" stroke-width="{r.uniform(8,30):.0f}" fill="none" opacity="0.4" filter="url(#blur2)"/>'
    for i in range(26):
        x0 = 200 + i * 75 + r.uniform(-20, 20)
        pts = wavy(x0, -40, x0 + r.uniform(-200, 200), 1400, r.uniform(20, 50), 2, i)
        s += f'<path d="{"M" + " L".join(f"{x:.0f},{y+8:.0f}" for x, y in pts)}" stroke="#6a6e80" stroke-width="30" fill="none" opacity="0.35" filter="url(#blur2)"/>'
        s += braid(pts, 30, "#0a0605", "#7a6050", seed=i)
    return S(s, '<rect width="2400" height="1350" fill="#0a1a3a" opacity="0.28"/>')


@art
def bootprints():
    s = '<rect width="2400" height="1350" fill="#2a1e16"/>'
    for i in range(12):  # floor boards in perspective
        s += f'<path d="M{i*220-200},1350 L{1200+(i*220-1400)*0.3:.0f},300" stroke="#140c08" stroke-width="8"/>'
    s += '<rect width="2400" height="1350" fill="#000" filter="url(#plaster)" opacity="0.35"/>'
    s += '<path d="M800,0 L1600,0 L1500,300 L900,300 Z" fill="#1a3050"/>' + glow(1200, 150, 500, "moon", 0.8)  # window
    s += '<path d="M900,300 L1500,300 L2100,1350 L300,1350 Z" fill="#a8c4e8" opacity="0.18"/>'
    for j, (x, y, a) in enumerate([(1100, 1220, -8), (1260, 1080, 6), (1140, 930, -6), (1270, 800, 5), (1170, 680, -4), (1260, 570, 4), (1200, 470, 0)]):
        k = 1.4 - j * 0.14
        s += (f'<g transform="translate({x},{y}) rotate({a}) scale({k})"><path d="M-22,-40 C-26,-70 22,-70 22,-40 L18,0 C10,8 -10,8 -18,0 Z" fill="#120a04" opacity="0.9"/>'
              f'<rect x="-16" y="16" width="32" height="26" rx="8" fill="#120a04" opacity="0.9"/>'
              f'<circle cx="0" cy="58" r="9" stroke="#120a04" stroke-width="3" fill="none" opacity="0.8"/></g>')
    return S(s)


@art
def mother_portrait(): return PA.ART["mother_portrait"]()
@art
def mother_fear(): return S(portrait_bg("candle"), PA.mother_bust(1200, 560, 1.75, rim="#ffb860", look=-0.3, sad=True))
@art
def mother_dark(): return PA.ART["mother_dark"]()
@art
def abuela(): return BA.ART["brigida_portrait"]()


@art
def room_ines(): return S(BA.carmen_room_svg(False))
@art
def room_ines2(): return S(BA.carmen_room_svg(False), '<rect width="2400" height="1350" fill="#020510" opacity="0.35"/>', glow(1230, 880, 400, "warm", 0.4))
@art
def room_window_open():
    s = BA.carmen_room_svg(False) + '<rect width="2400" height="1350" fill="#020510" opacity="0.3"/>'
    s += '<path d="M1520,320 L1300,260 L1300,1120 L1520,1080 Z" fill="#2a1c12"/>'  # open shutter
    for i in range(4):  # boards nailed, now hanging
        s += f'<rect x="{1540+i*30}" y="{520+i*120}" width="320" height="40" fill="#3a2a1a" transform="rotate({20+i*14} {1540+i*30} {520+i*120})"/>'
    s += clouds(8, 600, 1100, 3, "#b8c8dc", (0.15, 0.3), (200, 400), (40, 90))
    return S(s)


@art
def sombreron_bed():
    s = '<rect width="2400" height="1350" fill="#0a0604"/>' + glow(500, 900, 600, "warm", 0.7)
    s += '<path d="M0,820 C600,780 1800,780 2400,820 L2400,1350 L0,1350 Z" fill="#6a5a4a"/>'
    s += '<ellipse cx="1350" cy="800" rx="520" ry="150" fill="#9a8a72"/>'
    s += f'<g transform="translate(1350,720) rotate(-80) scale(1.6)">{ines_hair_back(True)}</g>'
    s += f'<g transform="translate(1350,720) rotate(-80) scale(1.6)">{ines_head(eyes_closed=True, smile=0.1, rim=WARM, thin=True)}</g>'
    s += '<path d="M0,980 C600,940 1800,960 2400,1000 L2400,1350 L0,1350 Z" fill="#4a1a22"/>'
    s += hat(1350, 520, 2.4, rim="#ffb860", tilt=8)
    s += '<path d="M460,960 L500,860" stroke="#e8d0a0" stroke-width="10"/>' + glow(500, 850, 120, "warm", 1.0) + flame(500, 850, 0.8)
    s += '<path d="M380,1350 C400,1100 440,1000 470,960 L520,970 C520,1060 520,1200 540,1350 Z" fill="#8a5a40"/>'  # arm with matchstick
    return S(s)


@art
def candle_out(): return PA.ART["candle_out"]()
@art
def black(): return S('<rect width="2400" height="1350" fill="#000"/>')
@art
def red_flash(): return PA.ART["red_flash"]()


@art
def table_food():
    s = room_walls("#2a1e18", "#0c0806", "#1a120c") + table_wood(760)
    s += candle_at(500, 760, 160)
    # clay plate with beans, tortillas in a basket, jarro de chocolate
    s += '<ellipse cx="1200" cy="900" rx="330" ry="90" fill="#7a3a1a"/><ellipse cx="1200" cy="890" rx="280" ry="70" fill="#a85a2a"/>'
    s += '<ellipse cx="1200" cy="885" rx="200" ry="48" fill="#3a1a10"/>'
    r = random.Random(3)
    for i in range(60):
        s += f'<ellipse cx="{1200+r.uniform(-180,180):.0f}" cy="{885+r.uniform(-38,38):.0f}" rx="9" ry="6" fill="#4a2214"/>'
    s += '<ellipse cx="1750" cy="860" rx="200" ry="60" fill="#6a4a20"/><ellipse cx="1750" cy="840" rx="170" ry="40" fill="#e8d0a0"/>'
    s += '<path d="M700,920 L700,800 C700,770 860,770 860,800 L860,920 Z" fill="#7a3a1a"/><ellipse cx="780" cy="800" rx="80" ry="20" fill="#3a1a0a"/>'
    s += '<path d="M860,820 C920,820 920,880 860,880" stroke="#7a3a1a" stroke-width="16" fill="none"/>'
    s += '<path d="M1290,860 L1600,700" stroke="#c8c8c8" stroke-width="12" stroke-linecap="round"/>'
    return S(s)


@art
def plate_earth():
    s = '<rect width="2400" height="1350" fill="#0a0806"/>' + glow(800, 400, 1000, "warm", 0.35) + glow(1200, 700, 800, "moon", 0.25)
    s += '<ellipse cx="1200" cy="760" rx="900" ry="380" fill="#5a2a12"/><ellipse cx="1200" cy="740" rx="780" ry="310" fill="#8a4a22"/>'
    s += '<ellipse cx="1200" cy="740" rx="620" ry="240" fill="#1a120c"/>'
    r = random.Random(7)
    for i in range(500):
        x = 1200 + r.gauss(0, 260); y = 740 + r.gauss(0, 90)
        if ((x - 1200) / 600) ** 2 + ((y - 740) / 230) ** 2 > 1: continue
        s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(3,14):.0f}" fill="{r.choice(["#2a1c12","#3a2618","#120c08","#4a3220"])}"/>'
    for i in range(6):  # a worm and some roots
        x = 1000 + i * 70
        s += f'<path d="M{x},{720+i*6} q20,-20 40,0 t40,0" stroke="#5a3a24" stroke-width="4" fill="none"/>'
    s += '<path d="M1120,760 C1160,730 1220,790 1260,750 C1290,722 1320,760 1340,740" stroke="#8a5a5a" stroke-width="12" fill="none" stroke-linecap="round"/>'
    s += '<path d="M1700,700 L2300,260" stroke="#b8b8b8" stroke-width="28" stroke-linecap="round"/><ellipse cx="1660" cy="730" rx="90" ry="50" fill="#b8b8b8" transform="rotate(-35 1660 730)"/>'
    s += '<ellipse cx="1660" cy="730" rx="70" ry="34" fill="#2a1c12" transform="rotate(-35 1660 730)"/>'
    return S(s)


@art
def scissors_cut():
    s = '<rect width="2400" height="1350" fill="#0c0806"/>' + glow(700, 500, 1000, "warm", 0.6)
    # one thick braid hanging diagonally
    pts = [(1200, -40), (1180, 300), (1150, 640), (1130, 1000), (1120, 1400)]
    s += braid(pts, 70, "#0a0605", "#8a6a50", seed=4)
    # open scissors biting the braid
    s += '<g transform="translate(1180,640) rotate(-12)">'
    s += f'<path d="M0,0 L600,-60 L600,-30 Z" fill="#d8d8dc"/><path d="M0,0 L600,90 L600,60 Z" fill="#b8b8c0"/>'
    s += '<path d="M0,0 L600,-60" stroke="#ffffff" stroke-width="4" opacity="0.8"/>'
    s += '<circle cx="0" cy="0" r="16" fill="#8a8a90"/>'
    s += '<path d="M0,0 L-260,-90" stroke="#9a9aa0" stroke-width="30"/><path d="M0,0 L-260,110" stroke="#9a9aa0" stroke-width="30"/>'
    s += '<circle cx="-330" cy="-110" r="70" stroke="#9a9aa0" stroke-width="26" fill="none"/><circle cx="-330" cy="140" r="70" stroke="#9a9aa0" stroke-width="26" fill="none"/>'
    s += '</g>'
    # hand on the handle
    s += '<path d="M640,520 C720,460 860,480 900,560 C930,640 880,760 780,790 C700,810 620,760 600,680 Z" fill="#a87858"/>'
    s += '<path d="M600,680 C560,800 520,1000 480,1350 L700,1350 C720,1100 760,900 780,790" fill="#1a1218"/>'
    return S(s)


@art
def hair_table():
    s = room_walls("#2a1e18", "#0c0806", "#1a120c") + table_wood(700) + candle_at(380, 700, 160)
    r = random.Random(9)
    for i in range(14):
        x0 = r.uniform(600, 1900); y0 = r.uniform(780, 1000); a = r.uniform(-0.5, 0.5)
        pts = [(x0, y0), (x0 + 200 * math.cos(a), y0 + 60 * math.sin(a) + 20), (x0 + 420 * math.cos(a), y0 + 30 * math.sin(a) + 50)]
        s += braid(pts, 22, "#0a0605", "#9a7a60", seed=i)
    s += '<g transform="translate(1600,1150) rotate(15)"><path d="M0,0 L380,-30 L380,-12 Z" fill="#c8c8d0"/><path d="M0,0 L380,40 L380,22 Z" fill="#a8a8b0"/>'
    s += '<circle cx="-110" cy="-40" r="44" stroke="#8a8a90" stroke-width="18" fill="none"/><circle cx="-110" cy="60" r="44" stroke="#8a8a90" stroke-width="18" fill="none"/></g>'
    return S(s)


@art
def church_int(): return QM.ART["church_mass"]()


@art
def altar_hair():
    s = '<rect width="2400" height="1350" fill="#0c0806"/>' + glow(1200, 400, 1100, "warm", 0.5)
    s += '<rect x="700" y="80" width="1000" height="700" fill="#5a4010"/>'
    for i in range(10):
        s += f'<rect x="{730+i*96}" y="100" width="40" height="660" fill="#c8a040" opacity="0.6"/>'
    s += '<path d="M1200,180 L1200,560 M1080,300 L1320,300" stroke="#1a1008" stroke-width="34"/>'
    s += '<rect x="400" y="780" width="1600" height="570" fill="#e8dcc8"/><rect x="400" y="780" width="1600" height="40" fill="#c8a040"/>'
    for x in (520, 760, 1640, 1880):
        s += candle_at(x, 780, 200)
    # rebozo with the cut braids
    s += '<path d="M800,900 C900,860 1500,860 1600,900 L1640,1060 C1500,1100 900,1100 760,1060 Z" fill="#5a1c30"/>'
    for i in range(6):
        y = 930 + i * 20
        s += braid([(880, y), (1200, y - 10 + (i % 2) * 20), (1520, y + 5)], 22, "#0a0605", "#9a7a60", seed=i)
    # priest's hand with hyssop and water drops
    s += '<path d="M1700,500 C1760,460 1840,470 1860,520 L2100,700 L2000,800 L1760,600 C1720,580 1690,540 1700,500 Z" fill="#2a2228"/>'
    s += '<ellipse cx="1690" cy="520" rx="50" ry="40" fill="#a87858"/><path d="M1660,520 L1500,700" stroke="#c8c8c8" stroke-width="14"/><circle cx="1490" cy="712" r="24" fill="#d8d8d8"/>'
    r = random.Random(3)
    for i in range(30):
        x, y = 1490 + r.uniform(-260, 120), 740 + r.uniform(0, 220)
        s += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="4" ry="8" fill="#e8f4ff" opacity="0.85"/>'
    return S(s)


@art
def windowsill():
    s = '<rect width="2400" height="1350" fill="#e8dcc8"/>' + sky("#7a9cc8", "#f0e0c8")
    s += '<rect x="0" y="0" width="380" height="1350" fill="#3a2a20"/><rect x="2020" y="0" width="380" height="1350" fill="#3a2a20"/>'
    s += ridge(700, 100, "#6a7a90", 3, step=30) + town(860, 4, "day", 20, 380, 2020, 1.4)
    s += '<rect x="300" y="900" width="1800" height="450" fill="#8a7060"/><rect x="300" y="900" width="1800" height="40" fill="#a89080"/>'
    s += '<rect width="2400" height="1350" fill="#000" filter="url(#plaster)" opacity="0.2"/>'
    s += '<path d="M800,980 C900,930 1500,930 1600,980 L1640,1120 C1500,1160 900,1160 760,1120 Z" fill="#5a1c30"/>'  # folded rebozo
    for i in range(10):
        s += f'<path d="M{790+i*85},1130 l-10,40 M{800+i*85},1130 l0,44" stroke="#5a1c30" stroke-width="5"/>'
    s += '<path d="M800,980 C900,930 1500,930 1600,980" stroke="#fff0e0" stroke-width="5" fill="none" opacity="0.6"/>'
    return S(s, '<rect width="2400" height="1350" fill="#0a1a3a" opacity="0.15"/>')


@art
def windowsill_braid():
    s = '<rect width="2400" height="1350" fill="#5a1c30"/>'
    r = random.Random(6)
    for i in range(20):
        s += f'<path d="M{r.uniform(0,2400):.0f},0 C{r.uniform(0,2400):.0f},600 {r.uniform(0,2400):.0f},900 {r.uniform(0,2400):.0f},1350" stroke="#3a0c1c" stroke-width="{r.uniform(10,40):.0f}" fill="none" opacity="0.5" filter="url(#blur2)"/>'
    s += glow(1200, 600, 1000, "white", 0.22)
    for i in range(12):  # a coil of plaits gathered at the centre
        a0 = i / 12 * math.pi * 2
        pts = [(1200 + math.cos(a0 + t * 2.2) * (80 + t * 520), 680 + math.sin(a0 + t * 2.2) * (60 + t * 330)) for t in [j / 10 for j in range(11)]]
        s += f'<path d="{"M" + " L".join(f"{x:.0f},{y+12:.0f}" for x, y in pts)}" stroke="#1a0410" stroke-width="44" fill="none" opacity="0.6" filter="url(#blur2)"/>'
        s += braid(pts, 36, "#0a0605", "#a08060", seed=i)
    s += '<circle cx="1200" cy="680" r="70" fill="#050305"/><path d="M1180,640 L1300,560 L1290,620 Z M1180,700 L1310,760 L1260,790 Z" fill="#050305"/>'
    return S(s, '<rect width="2400" height="1350" fill="#0a1a3a" opacity="0.2"/>')


@art
def rose_close():
    s = '<rect width="2400" height="1350" fill="#06040a"/>' + glow(1200, 600, 900, "moon", 0.45)
    s += braid([(-40, 1100), (600, 900), (1100, 760)], 70, "#0a0605", "#9a7a60", seed=3)
    s += '<path d="M1080,740 C1150,700 1200,720 1250,760 C1300,800 1290,860 1240,880" stroke="#050305" stroke-width="22" fill="none"/>'  # black ribbon
    s += '<path d="M1250,760 L1400,660 L1380,720 Z M1250,760 L1420,800 L1370,840 Z" fill="#050305"/>'
    # wet red petal with dew
    g = uid("pt")
    s += f'<defs>{grad_rad(g, [(0, "#e83040", 1), (0.6, "#a8101a", 1), (1, "#4a0008", 1)], 0.45, 0.4, 0.6)}</defs>'
    s += f'<path d="M1290,640 C1300,500 1450,430 1580,470 C1700,510 1720,640 1650,730 C1590,800 1470,820 1380,780 C1420,740 1440,700 1420,680 C1380,700 1320,700 1290,640 Z" fill="url(#{g})"/>'
    s += '<path d="M1320,580 C1420,520 1540,550 1570,640" stroke="#e85060" stroke-width="10" fill="none" opacity="0.7"/>'
    s += '<path d="M1300,560 C1360,640 1420,700 1400,780" stroke="#600008" stroke-width="8" fill="none" opacity="0.7"/>'
    s += '<path d="M1330,560 C1420,520 1560,540 1620,620" stroke="#ff8090" stroke-width="5" fill="none" opacity="0.6"/>'
    s += '<path d="M1600,520 C1660,560 1680,620 1660,700" stroke="#ffb0b8" stroke-width="7" fill="none" opacity="0.5"/>'
    s += '<path d="M1500,700 C1520,708 1528,720 1520,730 C1510,740 1494,732 1500,700 Z" fill="#f0f8ff" opacity="0.8"/>'
    return S(s)


# ----------------------------------------------------- history
@art
def map_chiapas():
    s = '<rect width="2400" height="1350" fill="#d8c8a0"/><rect width="2400" height="1350" fill="#000" filter="url(#paper)" opacity="0.25"/>'
    s += '<rect x="80" y="80" width="2240" height="1190" fill="none" stroke="#5a3a1a" stroke-width="6"/>'
    # simplified coastlines/regions
    s += '<path d="M150,300 C500,250 800,320 1000,420 C1100,470 1180,560 1220,640 L1500,700 C1600,640 1700,560 1820,520 C1900,500 2000,420 2100,330 L2250,300 L2250,1220 L150,1220 Z" fill="#c8b48a"/>'
    s += '<path d="M150,300 C500,250 800,320 1000,420 C1100,470 1180,560 1220,640 L1500,700" stroke="#5a3a1a" stroke-width="5" fill="none"/>'
    s += '<path d="M1100,700 C1150,800 1300,900 1350,1000 C1380,1080 1450,1150 1550,1220" stroke="#8a1a1a" stroke-width="7" fill="none" stroke-dasharray="20 14"/>'  # border
    s += '<path d="M800,900 C950,820 1150,780 1260,820 C1340,860 1300,980 1250,1060 C1150,1140 900,1100 800,1020 Z" fill="#a89060" opacity="0.6"/>'  # Chiapas
    s += '<path d="M1400,960 C1550,900 1800,920 1900,1000 C1950,1080 1850,1180 1700,1200 C1550,1210 1420,1120 1400,960 Z" fill="#98a070" opacity="0.55"/>'  # Guatemala
    s += '<text x="980" y="960" font-family="Cinzel" font-size="64" fill="#3a2010">CHIAPAS</text>'
    s += '<text x="1560" y="1080" font-family="Cinzel" font-size="56" fill="#3a2010">GUATEMALA</text>'
    s += '<text x="560" y="600" font-family="Cinzel" font-size="80" fill="#3a2010" opacity="0.7">MÉXICO</text>'
    s += '<circle cx="1130" cy="900" r="14" fill="#8a1a1a"/><text x="1010" y="870" font-family="IM FELL English" font-size="40" fill="#3a2010">San Cristóbal</text>'
    s += '<path d="M2050,230 L2050,140 M2020,170 L2050,140 L2080,170" stroke="#5a3a1a" stroke-width="6" fill="none"/><text x="2032" y="270" font-family="Cinzel" font-size="40" fill="#5a3a1a">N</text>'
    return S(s)


@art
def chronicle():
    s = '<rect width="2400" height="1350" fill="#d8c8a0"/><rect width="2400" height="1350" fill="#000" filter="url(#paper)" opacity="0.3"/>'
    s += '<rect x="160" y="100" width="2080" height="1150" fill="none" stroke="#5a3a1a" stroke-width="5"/>'
    s += '<text x="1200" y="230" text-anchor="middle" font-family="IM FELL English" font-size="84" fill="#3a2010">El Sombrerón, o el Tzipitío</text>'
    s += '<text x="1200" y="300" text-anchor="middle" font-family="IM FELL English" font-size="44" fill="#5a3a1a" font-style="italic">leyenda de la vieja capital</text>'
    s += '<rect x="600" y="360" width="1200" height="760" fill="#c8b48a" stroke="#5a3a1a" stroke-width="4"/>'
    # engraving: convent arch, girl at the window, tiny man with huge hat and mules
    s += '<path d="M1300,1100 L1300,560 Q1500,420 1700,560 L1700,1100 Z" fill="#8a7050"/><rect x="1440" y="640" width="120" height="170" fill="#3a2a18"/>'
    s += place(woman_full(rim=None, fill="#2a1a10"), 1500, 810, 0.18)
    s += place(sombreron_fig(rim="#c8b48a", fill="#2a1a10"), 1050, 1080, 0.75)
    for i in range(2):
        s += horse_shape(700 + i * 150, 1090, 160, "#2a1a10", mule=True, packs=True, seed=30 + i)
    for i in range(40):
        s += f'<path d="M620,{380+i*18} L1780,{380+i*18}" stroke="#5a3a1a" stroke-width="1" opacity="0.15"/>'
    return S(s)


@art
def stage_1946():
    s = '<rect width="2400" height="1350" fill="#0c0606"/>' + glow(1200, 700, 900, "warm", 0.45)
    s += '<rect x="300" y="900" width="1800" height="450" fill="#3a2414"/><rect x="300" y="900" width="1800" height="20" fill="#6a4424"/>'
    for side in (-1, 1):
        x0 = 1200 + side * 1200
        s += f'<path d="M{x0},0 L{1200+side*560},0 C{1200+side*620},300 {1200+side*700},600 {1200+side*760},1350 L{x0},1350 Z" fill="#6a0c14"/>'
        for i in range(7):
            xx = 1200 + side * (620 + i * 80)
            s += f'<path d="M{xx},0 C{xx+side*20},400 {xx+side*40},800 {xx+side*60},1350" stroke="#3a0408" stroke-width="18" fill="none" opacity="0.7"/>'
    s += '<path d="M0,0 L2400,0 L2400,140 C1800,200 600,200 0,140 Z" fill="#7a1018"/>'
    s += '<path d="M500,1350 L900,900 L1500,900 L1900,1350 Z" fill="#fff0c0" opacity="0.08"/>'
    s += place(sombreron_fig(rim="#ffd8a0"), 1200, 960, 0.85)
    for i in range(14):  # audience heads
        s += f'<ellipse cx="{120+i*170}" cy="1330" rx="70" ry="60" fill="#050303"/>'
    return S(s)


@art
def book_1930():
    s = room_walls("#2a1e18", "#0c0806", "#1a120c") + table_wood(820) + candle_at(420, 820, 200)
    s += '<path d="M700,820 L1200,760 L1700,820 L1700,1060 L1200,1000 L700,1060 Z" fill="#e8dcc0"/>'
    s += '<path d="M1200,760 L1200,1000" stroke="#8a7a5a" stroke-width="6"/>'
    for i in range(10):
        s += f'<path d="M{760},{840+i*20} L{1150},{790+i*20}" stroke="#6a5a40" stroke-width="3" opacity="0.6"/>'
        s += f'<path d="M{1250},{790+i*20} L{1640},{840+i*20}" stroke="#6a5a40" stroke-width="3" opacity="0.6"/>'
    s += f'<g transform="translate(980,980) scale(0.12)">{hat(0,0,1.0,rim="#3a2a1a",emb="#3a2a1a")}</g>'
    return S(s)


@art
def film_1950():
    s = '<rect width="2400" height="1350" fill="#100c08"/>' + glow(1200, 600, 900, "white", 0.35)
    s += '<rect x="500" y="250" width="1400" height="850" fill="#d8d0c0"/>'
    for y in (250, 1050):
        s += f'<rect x="500" y="{y-40 if y==250 else y}" width="1400" height="50" fill="#1a1612"/>'
        for i in range(24):
            s += f'<rect x="{520+i*58}" y="{y-28 if y==250 else y+12}" width="30" height="24" fill="#d8d0c0"/>'
    s += f'<rect x="560" y="280" width="1280" height="740" fill="#3a3a3a"/>'
    s += f'<g transform="translate(1200,980) scale(1.0)" opacity="0.95">{sombreron_fig(rim="#e8e8e8", fill="#0a0a0a")}</g>'
    s += '<rect x="560" y="280" width="1280" height="740" fill="#d8d0c0" opacity="0.15"/>'
    return S(s, '<rect width="2400" height="1350" fill="#000" filter="url(#paper)" opacity="0.2"/>')


@art
def title_bg():
    s = sky("#030610", "#14223a") + stars(160, 21, 900) + moon(1200, 430, 300)
    s += ridge(1000, 80, "#060a12", 5, step=30) + town(1100, 6, "night", 30, 0, 2400, 1.0)
    s += f'<g transform="translate(1200,1300) scale(1.55)">{sombreron_fig(rim="#dfe9f5", fill="#020204")}</g>'
    return S(s, QM.fog_band(1250, 0.45, 22))


@art
def cadejo():
    s = sky("#030610", "#16243a") + stars(120, 8, 600) + moon(1800, 260, 80) + ridge(860, 70, "#0a1018", 3)
    s += '<path d="M0,1100 C700,1040 1500,1060 2400,1080 L2400,1350 L0,1350 Z" fill="#0a0c12"/>'
    s += place(man_full(hat=True, cape=False, walk=0.3, rim=MOONRIM), 700, 1150, 0.5)
    # big black dog silhouette with red eyes
    d = ("M0,0 L10,-120 C0,-160 20,-200 60,-210 L300,-220 C340,-260 380,-300 400,-300 L420,-330 L430,-300 C470,-290 500,-260 510,-230 "
         "L480,-210 L420,-205 C400,-160 380,-120 370,-80 L380,0 L350,0 L340,-90 L300,-120 L120,-120 L80,-60 L90,0 L60,0 L50,-80 L30,-110 Z")
    s += glow(1550, 1000, 600, "moon", 0.55)
    s += f'<g transform="translate(1300,1180) scale(1.1)"><path d="{d}" fill="#020204"/><path d="{d}" stroke="{MOONRIM}" stroke-width="7" fill="none" opacity="0.8"/>'
    s += '<circle cx="455" cy="-262" r="22" fill="url(#redglow)"/><circle cx="455" cy="-262" r="6" fill="#ff5a3a"/>'
    s += '<path d="M10,-120 C-40,-150 -60,-200 -40,-240" stroke="#020204" stroke-width="22" fill="none"/></g>'
    return S(s, QM.fog_band(1200, 0.4, 9))


def write(names):
    for n in names:
        open(os.path.join(A, n + ".svg"), "w").write(ART[n]())


if __name__ == "__main__":
    write(sys.argv[1:] or list(ART))
