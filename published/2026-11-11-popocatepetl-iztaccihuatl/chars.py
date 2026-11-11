"""Custom characters for 'Popocatépetl e Iztaccíhuatl': the princess Iztaccíhuatl, the warrior Popocatépetl,
the lord of Tlaxcala and the jealous warrior. Faces reuse the shared head() builder (base_chars.py) with new skins,
hair, feather headdresses and costume. Full figures are hand-drawn shadow-theatre silhouettes with rim light."""
import math, random
from base_chars import head, uid, grad_lin, grad_rad

SK_IZTA = dict(base="#b98a6a", light="#d6aa88", hi="#efcfb0", shadow="#7a5440", deep="#40281c")
SK_IZTA_PALE = dict(base="#b8b0aa", light="#d4ccc6", hi="#eee8e2", shadow="#7c7470", deep="#3e3836")
SK_POPO = dict(base="#8e5e3c", light="#b07a52", hi="#cf9a6c", shadow="#5a3824", deep="#2e1a10")
SK_FATHER = dict(base="#86593c", light="#a67452", hi="#c4906a", shadow="#55382a", deep="#2a1a12")
SK_RIVAL = dict(base="#7c5034", light="#9a6644", hi="#b8805a", shadow="#4c2e1e", deep="#26160c")
SIL = "#04060a"
JADE = ("#1f6b52", "#3fa07a", "#8fe0b8")
QUETZAL = ("#0b3d2c", "#17784e", "#3fbf7a")


def strands(r, pts, n, color, w=(1.5, 3.5), op=(0.4, 0.9), jit=6):
    out = ""
    for (x0, y0, cx, cy, x1, y1) in pts:
        for _ in range(n):
            j = lambda: r.uniform(-jit, jit)
            out += (f'<path d="M{x0+j():.1f},{y0+j():.1f} Q{cx+j()*2:.1f},{cy+j()*2:.1f} {x1+j():.1f},{y1+j():.1f}" '
                    f'stroke="{color}" stroke-width="{r.uniform(*w):.1f}" fill="none" opacity="{r.uniform(*op):.2f}" stroke-linecap="round"/>')
    return out


def feather(x, y, L, ang, w=26, c=QUETZAL, seed=1):
    """Long quetzal-like feather from (x,y), length L, angle in degrees (0 = up)."""
    r = random.Random(seed)
    s = (f'<path d="M0,0 C{-w*0.6:.0f},{-L*0.3:.0f} {-w:.0f},{-L*0.7:.0f} 0,{-L:.0f} C{w:.0f},{-L*0.7:.0f} {w*0.6:.0f},{-L*0.3:.0f} 0,0 Z" fill="{c[1]}"/>'
         f'<path d="M0,0 C{-w*0.3:.0f},{-L*0.3:.0f} {-w*0.5:.0f},{-L*0.7:.0f} 0,{-L:.0f} L0,0 Z" fill="{c[0]}" opacity="0.8"/>'
         f'<path d="M0,0 Q{w*0.1:.0f},{-L*0.5:.0f} 0,{-L*0.98:.0f}" stroke="{c[2]}" stroke-width="2.5" fill="none" opacity="0.8"/>')
    for k in range(int(L / 22)):
        yy = -L * (0.12 + 0.8 * k / max(1, L / 22))
        s += f'<path d="M0,{yy:.0f} l{w*0.7:.0f},{-14:.0f} M0,{yy:.0f} l{-w*0.7:.0f},{-14:.0f}" stroke="{c[0]}" stroke-width="1.6" opacity="0.5"/>'
    return f'<g transform="translate({x},{y}) rotate({ang})">{s}</g>'


def ear_spool(x, y, r=13, c=JADE):
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c[0]}"/><circle cx="{x}" cy="{y}" r="{r*0.62:.1f}" fill="{c[1]}"/>'
            f'<circle cx="{x-r*0.25:.1f}" cy="{y-r*0.25:.1f}" r="{r*0.22:.1f}" fill="{c[2]}"/>')


def wrinkles(color="#33211a", op=0.45, heavy=1.0):
    s = ""
    for i, y in enumerate((-78, -68, -58)):
        s += f'<path d="M-40,{y} Q0,{y-8*heavy} 40,{y}" stroke="{color}" stroke-width="{2.2*heavy}" fill="none" opacity="{op*(1-i*0.2):.2f}"/>'
    s += f'<path d="M-26,34 Q-40,60 -34,84 M26,34 Q40,60 34,84" stroke="{color}" stroke-width="{2.6*heavy}" fill="none" opacity="{op}"/>'
    s += f'<path d="M-62,-14 l-12,-6 M-62,-8 l-13,2 M62,-14 l12,-6 M62,-8 l13,2" stroke="{color}" stroke-width="2" opacity="{op}"/>'
    return s


def tears(op=0.85):
    return (f'<path d="M-34,-6 C-36,16 -32,40 -38,62" stroke="#d8ecff" stroke-width="4" fill="none" opacity="{op}" stroke-linecap="round"/>'
            f'<path d="M30,-6 C30,20 34,44 28,70" stroke="#d8ecff" stroke-width="4" fill="none" opacity="{op}" stroke-linecap="round"/>'
            f'<circle cx="-38" cy="64" r="4.5" fill="#eef7ff" opacity="{op}"/><circle cx="28" cy="72" r="4.5" fill="#eef7ff" opacity="{op}"/>')


def glow_eyes(col="#eaf6ff"):
    return ''.join(f'<circle cx="{x}" cy="-19" r="30" fill="url(#whiteglow)"/><ellipse cx="{x}" cy="-19" rx="20" ry="9" fill="{col}"/>' for x in (-31, 31))


# ------------------------------------------------------------------ hair
def hair_izta_back(seed=2, wind=0.0, length=560):
    r = random.Random(seed)
    s = (f'<path d="M-96,-40 C-114,-130 -66,-180 0,-182 C66,-180 114,-130 96,-40 C112,80 {130+wind*60:.0f},{length*0.6:.0f} {120+wind*90:.0f},{length:.0f} '
         f'L{-120+wind*40:.0f},{length:.0f} C{-128+wind*20:.0f},{length*0.6:.0f} -112,80 -96,-40 Z" fill="#07080c"/>')
    s += strands(r, [(-96, -20, -120, 200, -110 + wind * 40, length - 20), (96, -20, 124 + wind * 40, 200, 116 + wind * 90, length - 20),
                     (-70, 60, -90, 260, -80 + wind * 40, length), (70, 60, 92 + wind * 30, 260, 84 + wind * 80, length)],
                 10, "#262a36", (1.4, 3), (0.3, 0.7), 10)
    return s


def hair_izta_front(seed=3, wind=0.0):
    r = random.Random(seed)
    cap = ('M0,-100 C-34,-100 -64,-86 -76,-54 C-82,-24 -84,10 -80,40 C-96,20 -102,-40 -94,-88 C-84,-142 -42,-170 0,-170 '
           'C42,-170 84,-142 94,-88 C102,-40 96,20 80,40 C84,10 82,-24 76,-54 C64,-86 34,-100 0,-100 Z')
    s = f'<path d="{cap}" fill="#08090d"/>'
    s += strands(r, [(-2, -100, -40, -108, -78, -30), (-2, -110, -52, -140, -92, -50), (2, -100, 40, -108, 78, -30),
                     (2, -110, 52, -140, 92, -50)], 9, "#3a4256", (1.1, 2.4), (0.3, 0.7), 5)
    s += '<path d="M0,-168 L0,-100" stroke="#1a1c26" stroke-width="2" opacity="0.8"/>'
    # two long locks falling in front of the shoulders
    for side in (-1, 1):
        sw = wind * (40 if side > 0 else 20)
        s += (f'<path d="M{side*78},-40 C{side*90},60 {side*92+sw:.0f},180 {side*86+sw*1.5:.0f},300 L{side*72+sw:.0f},300 '
              f'C{side*78},180 {side*76},60 {side*70},-30 Z" fill="#07080c"/>')
        s += strands(r, [(side * 76, -30, side * 92, 140, side * 76 + sw * 1.4, 320)], 5, "#30384a", (1, 2), (0.3, 0.6), 4)
    # headband of gold and jade with a small quetzal crest
    s += '<path d="M-92,-92 C-60,-126 60,-126 92,-92 L88,-76 C56,-108 -56,-108 -88,-76 Z" fill="#b8892e"/>'
    for i in range(7):
        x = -66 + i * 22; y = -104 - 6 * math.cos((i - 3) / 3)
        s += f'<circle cx="{x}" cy="{y:.0f}" r="7" fill="{JADE[1]}"/><circle cx="{x-2}" cy="{y-2:.0f}" r="2.4" fill="{JADE[2]}"/>'
    for k, a in enumerate((-28, -14, 0, 14, 28)):
        s += feather(a * 1.2, -116, 150 - abs(a) * 1.6, a * 0.9, 18, QUETZAL, seed + k)
    s += '<circle cx="0" cy="-114" r="13" fill="#d8a83a"/><circle cx="0" cy="-114" r="7" fill="#f4d47a"/>'
    return s


def hair_warrior(seed=5, color="#06070a"):
    r = random.Random(seed)
    s = ('<path d="M-92,-30 C-108,-120 -64,-176 0,-178 C64,-176 108,-120 92,-30 C100,20 104,70 96,110 L74,104 C80,40 80,-30 72,-60 '
         'C40,-92 -40,-92 -72,-60 C-80,-30 -80,40 -74,104 L-96,110 C-104,70 -100,20 -92,-30 Z" fill="' + color + '"/>')
    s += ('<path d="M-74,-60 C-50,-104 50,-104 74,-60 C62,-74 40,-84 20,-80 L14,-66 L4,-82 L-8,-64 L-18,-82 L-30,-66 L-40,-80 C-56,-78 -66,-70 -74,-60 Z" fill="' + color + '"/>')
    s += strands(r, [(-80, -100, -100, 0, -88, 100), (80, -100, 100, 0, 88, 100)], 6, "#2a2e3a", (1.2, 2.4), (0.3, 0.6), 6)
    return s


def headdress_warrior(seed=7, c1=QUETZAL, c2=("#5a0e0a", "#a8231a", "#e8563a"), tall=1.0):
    """Feather crest + band: Tlaxcalan warrior."""
    s = ""
    for k, a in enumerate(range(-50, 51, 10)):
        col = c1 if k % 2 else c2
        s += feather(a * 1.5, -118, (210 - abs(a) * 1.4) * tall, a * 0.85, 22, col, seed + k)
    s += '<path d="M-96,-96 C-60,-130 60,-130 96,-96 L92,-74 C58,-106 -58,-106 -92,-74 Z" fill="#e8e0cc"/>'
    s += '<path d="M-96,-96 C-60,-130 60,-130 96,-96" stroke="#a8231a" stroke-width="6" fill="none"/>'
    for i in range(9):
        x = -72 + i * 18
        s += f'<rect x="{x-4}" y="{-112 + abs(i-4)*2}" width="8" height="8" fill="#1a1a1a" transform="rotate(45 {x} {-108+abs(i-4)*2})"/>'
    return s


# ------------------------------------------------------------------ heads
def izta_head(back=True, look=0.0, turn=0.0, lids=0.3, smile=0.15, eyes_closed=False, shock=False, rim="#9fc2e8", wind=0.0, pale=False, ghost_eyes=False):
    sk = SK_IZTA_PALE if pale else SK_IZTA
    s = hair_izta_back(wind=wind, length=300) if back else ""
    s += head(look=look, smile=(-0.7 if shock else smile), lids=(0.0 if shock else lids), rim=rim, turn=turn, eyes_closed=eyes_closed or ghost_eyes,
              sk=sk, headwrap=False, earring=False, lips=("#6e3a34", "#8a4a42") if not pale else ("#6a5a5e", "#7e6c70"), iris="#1e1008", brow_w=0.75)
    if shock:
        s += '<ellipse cx="0" cy="74" rx="13" ry="11" fill="#2a0e0a"/>'
    s += ear_spool(-80, 18, 12) + ear_spool(80, 18, 12)
    s += hair_izta_front(wind=wind)
    if ghost_eyes:
        s += glow_eyes()
    return s


def popo_head(look=0.0, turn=0.0, lids=0.15, smile=0.1, eyes_closed=False, grief=False, rim="#9fc2e8", paint=True, frost=False):
    s = hair_warrior()
    s += head(look=look, smile=(-0.9 if grief else smile), lids=(0.5 if grief else lids), rim=rim, turn=turn, eyes_closed=eyes_closed,
              sk=SK_POPO, headwrap=False, earring=False, lips=("#5a2e22", "#6e3a2c"), iris="#1a0c06", brow_w=1.45, neck=True)
    if paint:  # two thin red war stripes on the cheekbones
        s += '<path d="M-64,14 L-30,22 M-62,28 L-32,34 M64,14 L30,22 M62,28 L32,34" stroke="#b0281c" stroke-width="5" opacity="0.8" stroke-linecap="round"/>'
    s += '<path d="M-60,40 C-50,90 -26,114 0,116 C26,114 50,90 60,40" stroke="#2e1a10" stroke-width="5" fill="none" opacity="0.35"/>'
    if grief:
        s += '<path d="M-58,-46 Q-36,-58 -10,-40 M58,-46 Q36,-58 10,-40" stroke="#120806" stroke-width="7" fill="none"/>'
        s += '<ellipse cx="0" cy="76" rx="16" ry="12" fill="#1e0a06"/>' + tears()
    s += ear_spool(-82, 16, 15, ("#7a5a1e", "#d0a23a", "#f8e08a")) + ear_spool(82, 16, 15, ("#7a5a1e", "#d0a23a", "#f8e08a"))
    s += headdress_warrior()
    if frost:
        r = random.Random(9)
        s += "".join(f'<circle cx="{r.uniform(-110,110):.0f}" cy="{r.uniform(-200,140):.0f}" r="{r.uniform(1.5,5):.1f}" fill="#eef6ff" opacity="{r.uniform(0.3,0.9):.2f}"/>' for _ in range(160))
        s += '<path d="M-96,-30 C-108,-120 -64,-176 0,-178 C64,-176 108,-120 96,-30" stroke="#eef6ff" stroke-width="10" fill="none" opacity="0.5" filter="url(#blur1)"/>'
    return s


def father_head(rim="#9fc2e8"):
    s = hair_warrior(seed=8, color="#3a3a3e")
    s += head(look=0.0, smile=-0.5, lids=0.5, rim=rim, sk=SK_FATHER, headwrap=False, earring=False, lips=("#4e2a20", "#62362a"), iris="#1a0e08", brow_w=1.3)
    s += wrinkles(heavy=1.1)
    s += '<path d="M-14,96 l28,0 l-4,12 l-20,0 Z" fill="#d0a23a"/>'  # gold lip plug (bezote)
    s += ear_spool(-82, 18, 16, ("#7a5a1e", "#d0a23a", "#f8e08a")) + ear_spool(82, 18, 16, ("#7a5a1e", "#d0a23a", "#f8e08a"))
    # lord's diadem (white and gold) with white heron feathers
    s += '<path d="M-98,-90 C-60,-132 60,-132 98,-90 L96,-70 C60,-108 -60,-108 -96,-70 Z" fill="#d0a23a"/>'
    s += '<path d="M-30,-120 L0,-180 L30,-120 Z" fill="#d0a23a"/><circle cx="0" cy="-134" r="10" fill="' + JADE[1] + '"/>'
    for k, a in enumerate(range(-40, 41, 10)):
        s += feather(a * 1.7, -116, 170 - abs(a), a, 20, ("#9a9a92", "#e8e6dc", "#ffffff"), 20 + k)
    return s


def rival_head(rim=None):
    s = hair_warrior(seed=11)
    s += head(look=0.35, smile=0.35, lids=0.55, rim=rim, sk=SK_RIVAL, headwrap=False, earring=False, lips=("#4a2418", "#5a2e20"), iris="#120804", brow_w=1.6)
    # black war-paint band across the eyes
    s += '<path d="M-82,-44 C-40,-50 40,-50 82,-44 L80,4 C40,-2 -40,-2 -80,4 Z" fill="#050404" opacity="0.72"/>'
    s += '<path d="M-58,-44 Q-34,-36 -10,-46 M58,-44 Q34,-34 10,-46" stroke="#050404" stroke-width="8" fill="none"/>'
    s += ''.join(f'<ellipse cx="{x}" cy="-19" rx="9" ry="4" fill="#ffb040" opacity="0.85"/>' for x in (-28, 34))
    s += ear_spool(-82, 16, 13, ("#1a1a1a", "#4a4a4a", "#8a8a8a")) + ear_spool(82, 16, 13, ("#1a1a1a", "#4a4a4a", "#8a8a8a"))
    s += headdress_warrior(seed=30, c1=("#2a0a06", "#6a1410", "#b8301e"), c2=("#0a0a0a", "#2a2a2a", "#5a5a5a"), tall=0.8)
    return s


# ------------------------------------------------------------------ busts (head centre at x,y; k=1 -> face ~245 tall)
def bust_frame(body, headsvg, x, y, k):
    return f'<g transform="translate({x},{y}) scale({k})"><g transform="translate(0,18) scale(0.74,0.86)">{body}</g>{headsvg}</g>'


def huipil_body(g, sk, rim, white=("#6e6a66", "#d8d2c6", "#f4efe4")):
    s = (f'<defs>{grad_lin(g+"d", [(0, white[0], 1), (0.5, white[1], 1), (0.85, white[2], 1), (1, white[1], 1)], -340, 0, 340, 0)}'
         f'{grad_lin(g+"s", [(0, sk["deep"], 1), (0.4, sk["shadow"], 1), (0.75, sk["base"], 1), (1, sk["shadow"], 1)], -220, 0, 220, 0)}</defs>')
    s += f'<path d="M-44,40 C-44,100 -58,150 -150,186 L150,186 C58,150 44,100 44,40 Z" fill="url(#{g}s)"/>'
    s += f'<path d="M-44,60 C-30,108 30,108 44,60 L44,40 L-44,40 Z" fill="{sk["deep"]}" opacity="0.5" filter="url(#blur1)"/>'
    s += f'<path d="M-300,226 C-200,190 -150,180 -110,176 Q0,240 110,176 C150,180 200,190 300,226 C350,300 370,420 380,660 L-380,660 C-370,420 -350,300 -300,226 Z" fill="url(#{g}d)"/>'
    # embroidered neckline: red and teal step-fret band
    s += '<path d="M-130,182 Q0,262 130,182 L150,206 Q0,292 -150,206 Z" fill="#8a1a16"/>'
    for i in range(13):
        t = (i - 6) / 6.0; x = t * 132; y = 214 + 50 * (1 - t * t)
        s += f'<path d="M{x-8:.0f},{y:.0f} l8,-8 l8,8 l-8,8 Z" fill="#2e8a7a"/>'
    for d in ["M-230,300 Q-240,480 -220,660", "M230,300 Q240,480 220,660", "M-80,320 Q-70,480 -90,660", "M80,320 Q70,480 90,660"]:
        s += f'<path d="{d}" stroke="#5a5650" stroke-width="10" fill="none" opacity="0.45" filter="url(#blur1)"/>'
    # jade necklace
    for i in range(15):
        t = (i - 7) / 7.0
        s += f'<circle cx="{t*120:.0f}" cy="{196 + 60*(1-t*t):.0f}" r="10" fill="{JADE[1]}"/><circle cx="{t*120-3:.0f}" cy="{193 + 60*(1-t*t):.0f}" r="3" fill="{JADE[2]}"/>'
    if rim:
        s += f'<path d="M-300,226 C-350,300 -370,420 -380,660" stroke="{rim}" stroke-width="6" fill="none" opacity="0.55" filter="url(#blur1)"/>'
    return s


def izta_bust(x, y, k=1.0, rim="#9fc2e8", pale=False, **hk):
    g = uid("ib")
    sk = SK_IZTA_PALE if pale else SK_IZTA
    wind = hk.get("wind", 0.0)
    back = f'<g transform="translate(0,-18) scale(1.35,1.16)">{hair_izta_back(wind=wind, length=560)}</g>'
    return bust_frame(back + huipil_body(g, sk, rim), izta_head(back=False, rim=rim, pale=pale, **hk), x, y, k)


def popo_bust(x, y, k=1.0, rim="#9fc2e8", ribbon=True, **hk):
    g = uid("pb"); sk = SK_POPO
    s = (f'<defs>{grad_lin(g+"s", [(0, sk["deep"], 1), (0.4, sk["shadow"], 1), (0.72, sk["base"], 1), (1, sk["shadow"], 1)], -360, 0, 360, 0)}'
         f'{grad_lin(g+"a", [(0, "#5a564c", 1), (0.6, "#c8c0aa", 1), (1, "#e6dec8", 1)], -300, 0, 300, 0)}'
         f'{grad_rad(g+"sh", [(0, "#d0a23a", 1), (0.55, "#8a1a16", 1), (0.6, "#e8e0cc", 1), (1, "#6a5a3a", 1)], 0.5, 0.5, 0.5)}</defs>')
    # shield behind the left shoulder
    s += f'<circle cx="-300" cy="300" r="230" fill="url(#{g}sh)"/><circle cx="-300" cy="300" r="230" fill="none" stroke="#2a1a0a" stroke-width="10"/>'
    for i in range(12):
        a = math.radians(i * 30 + 15)
        s += f'<circle cx="{-300+math.cos(a)*170:.0f}" cy="{300+math.sin(a)*170:.0f}" r="16" fill="{QUETZAL[1] if i%2 else "#a8231a"}"/>'
    # neck + muscular shoulders
    s += f'<path d="M-56,40 C-58,110 -70,150 -120,180 C-240,200 -330,250 -360,360 L-380,660 L380,660 L360,360 C330,250 240,200 120,180 C70,150 58,110 56,40 Z" fill="url(#{g}s)"/>'
    s += f'<path d="M-120,190 C-60,230 60,230 120,190" stroke="{sk["deep"]}" stroke-width="10" fill="none" opacity="0.5"/>'
    s += f'<path d="M-170,250 C-110,300 -40,300 -10,280 M170,250 C110,300 40,300 10,280" stroke="{sk["deep"]}" stroke-width="8" fill="none" opacity="0.45"/>'
    s += f'<path d="M200,230 C270,250 310,300 330,380" stroke="{sk["hi"]}" stroke-width="8" fill="none" opacity="0.35"/>'
    # quilted cotton armour (ichcahuipilli) from the chest down + cape knot on the right shoulder
    s += f'<path d="M-300,380 C-150,350 150,350 300,380 L320,660 L-320,660 Z" fill="url(#{g}a)"/>'
    for i in range(8):
        s += f'<path d="M{-300+i*86},380 L{-310+i*88},660" stroke="#8a8270" stroke-width="3" opacity="0.6"/>'
    for j in range(4):
        s += f'<path d="M-310,{430+j*60} L310,{430+j*60}" stroke="#8a8270" stroke-width="3" opacity="0.5"/>'
    s += '<path d="M120,200 C200,220 300,300 360,660 L240,660 C230,480 200,330 150,260 Z" fill="#a8231a" opacity="0.92"/>'
    s += '<circle cx="140" cy="210" r="30" fill="#7a1410"/><path d="M120,200 q20,-24 44,0" stroke="#e8563a" stroke-width="5" fill="none"/>'
    # necklace of jade + gold
    for i in range(11):
        t = (i - 5) / 5.0
        s += f'<circle cx="{t*100:.0f}" cy="{200 + 40*(1-t*t):.0f}" r="9" fill="{JADE[1] if i%2 else "#d0a23a"}"/>'
    if ribbon:  # the woven ribbon on the right upper arm
        s += '<path d="M300,330 C320,320 350,330 360,350 L352,372 C340,352 318,344 296,352 Z" fill="#e8e0cc"/>'
        s += '<path d="M330,340 l6,14 M316,342 l4,14 M344,346 l6,12" stroke="#a8231a" stroke-width="4"/>'
    if rim:
        s += f'<path d="M-120,180 C-240,200 -330,250 -360,360 L-380,660" stroke="{rim}" stroke-width="6" fill="none" opacity="0.55" filter="url(#blur1)"/>'
    return bust_frame(s, popo_head(rim=rim, **hk), x, y, k)


def father_bust(x, y, k=1.0, rim="#9fc2e8"):
    g = uid("fb"); sk = SK_FATHER
    s = (f'<defs>{grad_lin(g+"c", [(0, "#3a3630", 1), (0.6, "#bcb4a0", 1), (1, "#e8e2d0", 1)], -380, 0, 380, 0)}</defs>')
    s += f'<path d="M-56,40 C-58,110 -66,150 -76,190 L76,190 C66,150 58,110 56,40 Z" fill="{sk["shadow"]}"/>'
    s += f'<path d="M-90,170 C-220,200 -340,260 -380,660 L380,660 C340,260 220,200 90,170 Q0,230 -90,170 Z" fill="url(#{g}c)"/>'
    # cape border with red and black triangles, knot at the chest
    for side in (-1, 1):
        for i in range(10):
            yy = 220 + i * 44; xx = side * (110 + i * 10)
            s += f'<path d="M{xx},{yy} l{side*30},20 l{-side*30},20 Z" fill="{"#8a1a16" if i%2 else "#1a1a1a"}"/>'
    s += '<circle cx="0" cy="250" r="34" fill="#d0a23a"/><circle cx="0" cy="250" r="18" fill="' + JADE[1] + '"/>'
    # pectoral: big gold disc
    s += '<circle cx="0" cy="380" r="80" fill="#b8892e"/><circle cx="0" cy="380" r="60" fill="none" stroke="#f4d47a" stroke-width="6"/>'
    for i in range(8):
        a = math.radians(i * 45)
        s += f'<path d="M{math.cos(a)*30:.0f},{380+math.sin(a)*30:.0f} L{math.cos(a)*56:.0f},{380+math.sin(a)*56:.0f}" stroke="#f4d47a" stroke-width="6"/>'
    if rim:
        s += f'<path d="M-90,170 C-220,200 -340,260 -380,660" stroke="{rim}" stroke-width="6" fill="none" opacity="0.5" filter="url(#blur1)"/>'
    return bust_frame(s, father_head(rim=rim), x, y, k)


def rival_bust(x, y, k=1.0, rim="#ff5a3a"):
    g = uid("rb"); sk = SK_RIVAL
    s = (f'<defs>{grad_lin(g+"s", [(0, sk["deep"], 1), (0.4, sk["shadow"], 1), (0.75, sk["base"], 1), (1, sk["shadow"], 1)], -360, 0, 360, 0)}'
         f'{grad_lin(g+"j", [(0, "#120a06", 1), (0.5, "#3a2a14", 1), (1, "#6a5228", 1)], -360, 0, 360, 0)}</defs>')
    s += f'<path d="M-56,40 C-58,110 -70,150 -120,180 C-240,200 -330,250 -360,360 L-380,660 L380,660 L360,360 C330,250 240,200 120,180 C70,150 58,110 56,40 Z" fill="url(#{g}s)"/>'
    # jaguar-spotted cape over the shoulders
    s += f'<path d="M-130,184 C-250,206 -340,260 -370,380 L-380,660 L-200,660 C-200,460 -170,320 -60,230 Z" fill="url(#{g}j)"/>'
    s += f'<path d="M130,184 C250,206 340,260 370,380 L380,660 L200,660 C200,460 170,320 60,230 Z" fill="url(#{g}j)"/>'
    r = random.Random(3)
    for _ in range(40):
        side = r.choice((-1, 1)); xx = side * r.uniform(140, 350); yy = r.uniform(240, 640)
        s += f'<ellipse cx="{xx:.0f}" cy="{yy:.0f}" rx="{r.uniform(10,18):.0f}" ry="{r.uniform(8,14):.0f}" fill="none" stroke="#0a0604" stroke-width="5"/><circle cx="{xx:.0f}" cy="{yy:.0f}" r="3" fill="#0a0604"/>'
    s += f'<path d="M-120,190 C-60,230 60,230 120,190" stroke="{sk["deep"]}" stroke-width="10" fill="none" opacity="0.5"/>'
    # obsidian blade handle across the chest
    s += '<path d="M-200,620 L180,260" stroke="#2a1a0a" stroke-width="26" stroke-linecap="round"/>'
    for i in range(7):
        t = 0.45 + i * 0.075; xx = -200 + 380 * t; yy = 620 - 360 * t
        s += f'<path d="M{xx:.0f},{yy:.0f} l18,18 l10,-26 Z" fill="#141418" stroke="#6a6a80" stroke-width="2"/>'
    if rim:
        s += f'<path d="M120,180 C240,200 330,250 360,360 L380,660" stroke="{rim}" stroke-width="7" fill="none" opacity="0.7" filter="url(#blur1)"/>'
    return bust_frame(s, rival_head(rim=rim), x, y, k)


# ------------------------------------------------------------------ silhouettes (shadow theatre), built from joints
def _crest(cx, cy, k=1.0, n=7, spread=60, L=200):
    s = ""
    for i in range(n):
        a = -spread / 2 + spread * i / (n - 1)
        s += f'<g transform="translate({cx},{cy}) rotate({a})"><path d="M0,0 C-16,{-L*0.4*k:.0f} -12,{-L*0.8*k:.0f} 0,{-L*k:.0f} C12,{-L*0.8*k:.0f} 16,{-L*0.4*k:.0f} 0,0 Z"/></g>'
    return s


# Profile figures facing +x, feet at y=0, ~1000 tall. Limbs are thick round-capped strokes -> organic silhouettes.
def limb(pts, w0, w1, color):
    out = ""; n = len(pts) - 1
    for i in range(n):
        w = w0 + (w1 - w0) * i / max(1, n - 1) if n > 1 else w0
        (x0, y0), (x1, y1) = pts[i], pts[i + 1]
        out += f'<path d="M{x0},{y0} L{x1},{y1}" stroke="{color}" stroke-width="{w:.0f}" stroke-linecap="round"/>'
    return out


POSES = {
    #        back leg                          front leg                         back arm                      front arm          dy(torso drop)
    "stand": ([(-12, -470), (-20, -240), (-30, -30), (40, -12)], [(18, -470), (26, -240), (30, -30), (100, -12)],
              [(-10, -760), (-30, -600), (-20, -470)], [(20, -760), (40, -600), (50, -470)], 0),
    "march": ([(-12, -470), (-90, -250), (-160, -40), (-110, -8)], [(18, -470), (100, -260), (110, -30), (180, -10)],
              [(-10, -760), (-70, -610), (-60, -480)], [(20, -760), (90, -620), (130, -520)], 0),
    "run":   ([(-12, -470), (-140, -300), (-260, -220), (-230, -170)], [(18, -470), (170, -330), (150, -60), (220, -40)],
              [(-10, -760), (-110, -680), (-150, -560)], [(20, -760), (130, -700), (200, -800)], 20),
    "kneel": ([(-10, -330), (-70, -30), (-270, -20), (-300, -40)], [(20, -330), (200, -330), (200, -30), (270, -12)],
              [(-10, -620), (40, -480), (110, -420)], [(20, -620), (110, -480), (180, -430)], 140),
    "fight": ([(-12, -470), (-120, -250), (-200, -40), (-150, -8)], [(18, -470), (130, -280), (150, -30), (220, -10)],
              [(-10, -760), (-110, -720), (-170, -640)], [(20, -760), (60, -900), (80, -1040)], 0),
    "carry": ([(-12, -470), (-80, -250), (-140, -40), (-90, -8)], [(18, -470), (90, -260), (100, -30), (170, -10)],
              [(-10, -760), (40, -650), (170, -690)], [(20, -760), (80, -640), (-60, -690)], 0),
    "torch": ([(-10, -330), (-70, -30), (-270, -20), (-300, -40)], [(20, -330), (200, -330), (200, -30), (270, -12)],
              [(-10, -620), (60, -520), (150, -500)], [(20, -620), (120, -560), (160, -700)], 140),
}


def warrior_sil(pose="stand", shield=True, weapon=True, crest=True, facing=1, rim="#a8c8ff", fill=SIL, seed=1, cape=False, torch=False, head_bow=0):
    bl, fl, ba, fa, dy = POSES[pose]
    s = limb(bl, 74, 44, fill)
    s += f'<path d="M{bl[-2][0]},{bl[-2][1]} L{bl[-1][0]},{bl[-1][1]}" stroke="{fill}" stroke-width="30" stroke-linecap="round"/>'
    s += limb(ba, 46, 34, fill) if pose != "carry" else ""
    t = f'translate(0,{dy})'
    torso = ('M-62,-800 C-70,-720 -64,-600 -52,-470 L56,-470 C62,-560 70,-650 74,-720 C76,-770 52,-806 20,-812 Z')
    body = f'<path d="{torso}"/>'
    if cape:
        body += '<path d="M-60,-800 C-140,-700 -210,-540 -250,-360 C-190,-380 -130,-360 -80,-400 C-70,-540 -60,-680 -40,-790 Z"/>'
    body += '<path d="M-58,-500 L60,-500 L70,-430 L-58,-430 Z"/><path d="M20,-450 L70,-450 L60,-330 L28,-330 Z"/>'  # maxtlatl
    body += f'<path d="M-8,-830 L36,-830 L40,-790 L-4,-790 Z"/>'
    hx, hy = 16 + head_bow * 0.6, -886 + head_bow
    body += f'<ellipse cx="{hx}" cy="{hy}" rx="52" ry="60" transform="rotate({head_bow*0.3} {hx} {hy})"/><path d="M{hx+44},{hy-10} l22,18 l-24,10 Z"/>'
    body += f'<path d="M{hx-52},{hy-20} C{hx-64},{hy+30} {hx-60},{hy+70} {hx-44},{hy+100} L{hx-10},{hy+60} Z"/>'  # hair to the neck
    if crest:
        body += _crest(hx - 6, hy - 46, 1.0, 7, 80, 220)
    if shield and pose not in ("carry", "torch"):
        body += '<circle cx="-70" cy="-640" r="140"/>' + "".join(f'<path d="M{-170+i*50},-520 l-6,80 l16,0 Z"/>' for i in range(5))
    s += f'<g transform="{t}">{body}</g>'
    s += limb(fl, 76, 46, fill)
    s += f'<path d="M{fl[-2][0]},{fl[-2][1]} L{fl[-1][0]},{fl[-1][1]}" stroke="{fill}" stroke-width="30" stroke-linecap="round"/>'
    fa2 = [(x, y + dy) for x, y in fa]
    if weapon and pose not in ("carry", "torch"):
        wx, wy = fa2[-1]
        if pose == "fight":
            s += f'<path d="M{wx},{wy} L{wx+60},{wy-280}" stroke="{fill}" stroke-width="26" stroke-linecap="round"/>'
            for i in range(6):
                px = wx + 12 + i * 9; py = wy - 60 - i * 40
                s += f'<path d="M{px},{py} l30,6 l-12,-26 Z M{px-6},{py-6} l-28,-8 l6,26 Z" fill="{fill}"/>'
        else:
            s += f'<path d="M{wx},{wy+120} L{wx+40},{wy-520}" stroke="{fill}" stroke-width="16" stroke-linecap="round"/><path d="M{wx+30},{wy-510} l12,-110 l18,110 Z" fill="{fill}"/>'
    if torch:
        wx, wy = fa2[-1]
        s += f'<path d="M{wx-10},{wy+60} L{wx+14},{wy-150}" stroke="#1a0e06" stroke-width="20" stroke-linecap="round"/>'
    if pose not in ("carry",):
        s += limb([(x, y + dy) for x, y in fa], 48, 34, fill)
    out = f'<g fill="{fill}">{s}</g>'
    if rim:
        rp = f'M-62,-800 C-70,-720 -64,-600 -52,-470 M{hx-40},{hy-40} C{hx-20},{hy-66} {hx+30},{hy-66} {hx+52},{hy-20}'
        out += f'<path d="{rp}" transform="{t}" stroke="{rim}" stroke-width="8" fill="none" opacity="0.85" filter="url(#blur1)"/>'
        out += f'<path d="{" ".join(("M" if i==0 else "L")+f"{x},{y}" for i,(x,y) in enumerate(bl))}" stroke="{rim}" stroke-width="5" fill="none" opacity="0.35" filter="url(#blur1)" transform="translate(-30,0)"/>'
    if torch:
        wx, wy = fa2[-1]
        out += (f'<circle cx="{wx+16}" cy="{wy-200}" r="260" fill="url(#warmglow)"/>'
                f'<path d="M{wx+16},{wy-320} C{wx+60},{wy-240} {wx+50},{wy-170} {wx+16},{wy-150} C{wx-20},{wy-170} {wx-26},{wy-240} {wx+16},{wy-320} Z" fill="#ffb040"/>'
                f'<path d="M{wx+16},{wy-270} C{wx+36},{wy-220} {wx+30},{wy-180} {wx+16},{wy-160} C{wx},{wy-180} {wx-4},{wy-220} {wx+16},{wy-270} Z" fill="#fff2b0"/>')
    return f'<g transform="scale({facing},1)">{out}</g>'


def woman_sil(rim="#a8c8ff", fill=SIL, crown=False, hair_wind=0.0, arms="down", facing=1, dress=None):
    d = dress or fill
    s = limb([(10, -760), (30, -610), (40, -500)], 36, 28, fill) if arms == "down" else limb([(10, -760), (60, -640), (40, -560)], 36, 28, fill)
    s += f'<path d="M-70,-560 C-90,-380 -130,-180 -150,-8 L160,-8 C140,-180 100,-380 70,-560 Z" fill="{d}"/>'
    s += f'<path d="M-78,-560 C-90,-640 -80,-740 -50,-790 C-20,-806 40,-806 60,-790 C86,-740 92,-640 82,-560 Z" fill="{d}"/>'
    s += '<path d="M-6,-830 L30,-830 L34,-790 L-2,-790 Z"/>'
    s += '<ellipse cx="14" cy="-882" rx="46" ry="56"/><path d="M54,-892 l18,16 l-20,8 Z"/>'
    s += f'<path d="M-30,-930 C-60,-860 {-70-hair_wind*60:.0f},-720 {-60-hair_wind*140:.0f},-560 L{-30-hair_wind*100:.0f},-560 C-30,-700 -14,-840 10,-930 Z"/>'
    if crown:
        s += _crest(14, -930, 0.55, 5, 60, 180)
    out = f'<g fill="{fill}">{s}</g>'
    if rim:
        out += f'<path d="M-30,-930 C0,-950 50,-940 60,-880 M-78,-560 C-90,-640 -80,-740 -50,-790" stroke="{rim}" stroke-width="6" fill="none" opacity="0.8" filter="url(#blur1)"/>'
    return f'<g transform="scale({facing},1)">{out}</g>'


def lying_woman(dress="#e8eef4", skin="#c9b6a8", hair="#05060a", rim="#ffffff", hands=True):
    """Iztaccíhuatl lying on her back, head at left. Local coords: length ~900, ground y=0."""
    s = f'<path d="M-440,-40 C-470,-30 -470,40 -380,40 L-200,30 Z" fill="{hair}"/>'  # hair spread on the mat
    s += f'<path d="M-500,10 C-470,30 -380,50 -260,40 L-260,26 C-360,30 -440,20 -500,10 Z" fill="{hair}"/>'
    s += f'<ellipse cx="-360" cy="-62" rx="56" ry="44" fill="{skin}"/><path d="M-330,-104 l-10,-22 l-18,22 Z" fill="{skin}"/>'  # face up, nose
    s += f'<path d="M-410,-100 C-380,-120 -330,-118 -306,-96" stroke="{hair}" stroke-width="16" fill="none"/>'
    s += f'<path d="M-300,-80 C-240,-120 -160,-130 -60,-118 C40,-110 160,-90 300,-86 C380,-84 430,-70 450,-40 L450,0 L-300,0 Z" fill="{dress}"/>'
    s += f'<path d="M-240,-112 C-200,-150 -140,-150 -90,-124" fill="{dress}"/><ellipse cx="-180" cy="-120" rx="70" ry="30" fill="{dress}"/>'  # chest
    if hands:
        s += f'<path d="M-200,-150 C-170,-170 -130,-166 -110,-150 L-120,-132 C-150,-146 -180,-148 -196,-134 Z" fill="{skin}"/>'
    for x in (-120, 0, 120, 240):
        s += f'<path d="M{x},-110 C{x+20},-70 {x+10},-30 {x+30},0" stroke="#9aa8b6" stroke-width="5" fill="none" opacity="0.6"/>'
    s += f'<path d="M-300,-80 C-240,-120 -160,-130 -60,-118 C40,-110 160,-90 300,-86 C380,-84 430,-70 450,-40" stroke="{rim}" stroke-width="7" fill="none" opacity="0.7" filter="url(#blur1)"/>'
    return s


def popo_carry(rim="#cfe4ff", fill=SIL, dress="#e8eef4", skin="#c9b6a8"):
    """Warrior walking right, carrying the princess across his arms (her head hangs on the right)."""
    s = warrior_sil("carry", shield=False, weapon=False, rim=rim, fill=fill, cape=True, head_bow=14)
    # her: thighs/legs to the left, torso to the right, head and hair hanging
    w = f'<path d="M-160,-700 C-80,-740 60,-730 180,-700 C230,-690 260,-670 280,-650 L262,-620 C200,-650 100,-660 -20,-650 C-80,-646 -130,-630 -170,-600 Z" fill="{dress}"/>'
    w += f'<path d="M-170,-600 C-200,-570 -220,-520 -230,-460 L-196,-456 C-186,-510 -170,-560 -140,-620 Z" fill="{dress}"/>'  # dress over hanging legs
    w += f'<path d="M-230,-460 l-6,40 l30,4 l6,-40 Z" fill="{skin}"/>'
    w += f'<ellipse cx="300" cy="-620" rx="42" ry="48" fill="{skin}" transform="rotate(30 300 -620)"/>'
    w += f'<path d="M290,-660 C330,-580 340,-480 324,-360 L300,-360 C306,-460 294,-560 276,-620 Z" fill="#05060a"/>'
    w += f'<path d="M326,-640 C360,-560 376,-460 368,-350 L346,-350 C352,-450 340,-540 316,-610 Z" fill="#05060a"/>'
    w += f'<path d="M200,-690 C216,-610 222,-550 228,-480 L210,-478 C204,-546 192,-610 180,-680 Z" fill="{skin}"/>'  # her arm hanging
    w += f'<path d="M-160,-700 C-80,-740 60,-730 180,-700 C230,-690 260,-670 280,-650" stroke="#ffffff" stroke-width="8" fill="none" opacity="0.7" filter="url(#blur1)"/>'
    w += '<path d="M-60,-712 C-40,-680 0,-664 60,-672 M60,-716 C80,-690 120,-680 170,-684" stroke="#9aa8b6" stroke-width="4" fill="none" opacity="0.7"/>'
    arms = limb([(20, -760), (90, -650), (180, -690)], 46, 34, fill) + limb([(-10, -760), (20, -650), (-80, -690)], 46, 34, fill)
    return s + w + arms
