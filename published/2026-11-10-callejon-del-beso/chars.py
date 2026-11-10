"""Custom characters for 'El Callejón del Beso': Carmen, Luis, the father, Brígida, the noble suitor.
Front faces reuse the shared head() builder (base_chars.py, from the Mulata example) with new skins, hair and costume;
balcony figures are hand-drawn profile silhouettes with rim light (shadow-theatre look)."""
import math, random
from base_chars import head, uid, grad_lin, grad_rad, hand_open

SK_CARMEN = dict(base="#c99a7c", light="#e3b896", hi="#f4d2b4", shadow="#8a5e48", deep="#4a2c20")
SK_LUIS = dict(base="#a8774f", light="#c99668", hi="#e0b088", shadow="#6c4630", deep="#3a2216")
SK_FATHER = dict(base="#b48a6c", light="#cfa486", hi="#e2bda0", shadow="#6e4c3a", deep="#33211a")
SK_OLD = dict(base="#9c7458", light="#b88e70", hi="#d0a888", shadow="#644432", deep="#30201a")
SK_NOBLE = dict(base="#d4ab92", light="#e8c4ac", hi="#f6dcc8", shadow="#94705c", deep="#4e3428")
SIL = "#04060a"


def strands(r, pts, n, color, w=(1.5, 3.5), op=(0.4, 0.9), jit=6):
    """Hair strand strokes following a list of cubic paths [(x0,y0,cx,cy,x1,y1)]."""
    out = ""
    for (x0, y0, cx, cy, x1, y1) in pts:
        for _ in range(n):
            j = lambda: r.uniform(-jit, jit)
            out += (f'<path d="M{x0+j():.1f},{y0+j():.1f} Q{cx+j()*2:.1f},{cy+j()*2:.1f} {x1+j():.1f},{y1+j():.1f}" '
                    f'stroke="{color}" stroke-width="{r.uniform(*w):.1f}" fill="none" opacity="{r.uniform(*op):.2f}" stroke-linecap="round"/>')
    return out


# ------------------------------------------------------------------ hair
def hair_carmen_back(seed=2):
    r = random.Random(seed)
    s = ('<path d="M-92,-40 C-112,-120 -70,-178 0,-180 C70,-178 112,-120 92,-40 C104,10 120,70 96,118 '
         'C70,150 -70,150 -96,118 C-120,70 -104,10 -92,-40 Z" fill="#0d0806"/>')
    # low chignon behind the neck (visible on both sides)
    s += '<ellipse cx="-70" cy="112" rx="60" ry="44" fill="#120a07"/><ellipse cx="72" cy="112" rx="52" ry="40" fill="#0f0806"/>'
    s += strands(r, [(-110, 100, -70, 70, -30, 120), (110, 100, 70, 70, 30, 120)], 10, "#3a2418", (1.5, 3), (0.3, 0.7))
    return s


def hair_carmen_front(seed=3, loose=True, flower=True, wind=0.0):
    r = random.Random(seed)
    # cap: center part, smooth bands over the temples down behind the ears
    cap = ('M0,-104 C-30,-104 -62,-88 -74,-56 C-80,-30 -82,-6 -78,14 C-92,0 -100,-50 -92,-90 C-82,-140 -40,-168 0,-168 '
           'C40,-168 82,-140 92,-90 C100,-50 92,0 78,14 C82,-6 80,-30 74,-56 C62,-88 30,-104 0,-104 Z')
    s = f'<path d="{cap}" fill="#120a07"/>'
    s += strands(r, [(-2, -104, -40, -110, -76, -40), (-2, -110, -50, -140, -90, -60), (2, -104, 40, -110, 76, -40),
                     (2, -110, 50, -140, 90, -60), (-2, -150, -50, -160, -92, -80), (2, -150, 50, -160, 92, -80)],
                 9, "#4a2e1e", (1.2, 2.6), (0.35, 0.8), 5)
    s += '<path d="M0,-166 L0,-104" stroke="#2a1a12" stroke-width="2" opacity="0.8"/>'
    s += strands(r, [(-30, -160, -50, -150, -70, -120), (30, -160, 50, -150, 70, -120)], 4, "#9a7a62", (1.5, 3), (0.25, 0.5), 3)
    if loose:
        s += strands(r, [(-74, -40, -94 - wind * 40, 40, -84 - wind * 80, 140), (74, -40, 96 + wind * 30, 40, 88 + wind * 60, 150)], 3, "#140b08", (2, 3.5), (0.7, 1), 4)
    if flower:  # white jasmine-like blossoms over the left ear
        for (fx, fy, k) in ((-86, -64, 1.0), (-98, -40, 0.75), (-72, -82, 0.6)):
            for a in range(5):
                ang = math.radians(a * 72 + 10)
                s += f'<ellipse cx="{fx+math.cos(ang)*9*k:.1f}" cy="{fy+math.sin(ang)*9*k:.1f}" rx="{8*k:.1f}" ry="{5*k:.1f}" fill="#efe6d2" transform="rotate({a*72+10} {fx+math.cos(ang)*9*k:.1f} {fy+math.sin(ang)*9*k:.1f})"/>'
            s += f'<circle cx="{fx}" cy="{fy}" r="{4*k:.1f}" fill="#d9a63a"/>'
    return s


def hair_luis(seed=5):
    r = random.Random(seed)
    s = ('<path d="M-80,-30 C-96,-90 -70,-158 -10,-166 C50,-172 96,-130 88,-40 C84,-70 70,-96 40,-108 C10,-96 -30,-100 -60,-88 C-70,-70 -76,-50 -80,-30 Z" fill="#0f0a07"/>')
    # tousled locks falling on the forehead
    for i in range(14):
        x0 = r.uniform(-60, 60); y0 = r.uniform(-160, -120)
        s += f'<path d="M{x0:.0f},{y0:.0f} Q{x0+r.uniform(-30,30):.0f},{y0+30:.0f} {x0+r.uniform(-34,24):.0f},{y0+r.uniform(50,72):.0f} L{x0+r.uniform(-6,6)+12:.0f},{y0+10:.0f} Z" fill="#120b08"/>'
    s += strands(r, [(-60, -150, -20, -170, 40, -150), (-40, -130, 0, -150, 60, -120)], 8, "#4a3424", (1.5, 3), (0.3, 0.6), 8)
    s += '<path d="M-80,-30 C-84,-10 -82,10 -78,22 L-72,-10 Z M88,-40 C88,-10 84,10 80,22 L76,-14 Z" fill="#0f0a07"/>'
    return s


def stubble(r, color, n=220, y0=40, y1=112, x=62, op=0.45):
    return "".join(f'<circle cx="{r.uniform(-x, x):.0f}" cy="{r.uniform(y0, y1):.0f}" r="1.3" fill="{color}" opacity="{op}"/>'
                   for _ in range(n) if True)


def hair_father():
    s = ('<path d="M-84,-20 C-98,-80 -80,-148 -20,-160 C40,-168 92,-140 92,-60 C92,-40 90,-24 86,-10 '
         'C80,-50 70,-80 54,-96 C20,-110 -20,-110 -50,-96 C-70,-76 -78,-50 -84,-20 Z" fill="#1a1512"/>')
    s += '<path d="M-50,-96 C-20,-110 20,-110 54,-96 C30,-128 -20,-130 -50,-96 Z" fill="#3a3632" opacity="0.8"/>'  # receding, grey
    # grey temples + long sideburns
    s += '<path d="M-84,-20 C-86,10 -80,40 -70,62 L-62,30 C-66,10 -70,-6 -72,-30 Z" fill="#6e6a64"/>'
    s += '<path d="M86,-10 C86,16 82,40 72,62 L64,30 C68,10 72,-4 74,-26 Z" fill="#6e6a64"/>'
    # heavy mustache
    s += ('<path d="M-46,58 C-30,44 -10,44 0,50 C10,44 30,44 46,58 C56,66 60,80 54,88 C42,72 24,64 0,64 C-24,64 -42,72 -54,88 C-60,80 -56,66 -46,58 Z" fill="#2a2420"/>')
    s += strands(random.Random(9), [(-40, 56, -50, 70, -54, 86), (40, 56, 50, 70, 54, 86)], 6, "#8a847c", (1.2, 2.2), (0.3, 0.6), 4)
    return s


def wrinkles(color="#33211a", op=0.45, heavy=1.0):
    return (f'<g stroke="{color}" fill="none" stroke-linecap="round" opacity="{op}">'
            f'<path d="M-40,-78 Q0,-86 40,-78" stroke-width="{2.4*heavy}"/><path d="M-32,-66 Q0,-72 32,-66" stroke-width="{2*heavy}"/>'
            f'<path d="M-10,-52 L-6,-40 M10,-52 L6,-40" stroke-width="{2.6*heavy}"/>'
            f'<path d="M-30,34 Q-40,56 -34,76 M30,34 Q40,56 34,76" stroke-width="{2.6*heavy}"/>'
            f'<path d="M-62,-14 l-10,-4 M-62,-8 l-10,2 M62,-14 l10,-4 M62,-8 l10,2" stroke-width="{1.8*heavy}"/></g>')


def angry_brows(color="#141010", w=12):
    return (f'<path d="M-66,-48 Q-40,-50 -10,-34" stroke="{color}" stroke-width="{w}" fill="none" stroke-linecap="round"/>'
            f'<path d="M66,-48 Q40,-50 10,-34" stroke="{color}" stroke-width="{w}" fill="none" stroke-linecap="round"/>')


def ember_eyes():
    return ''.join(f'<circle cx="{x}" cy="-19" r="26" fill="url(#redglow)" opacity="0.9"/><circle cx="{x}" cy="-19" r="6" fill="#ff5a3a"/>' for x in (-31, 31))


# ------------------------------------------------------------------ heads
def carmen_head(look=0.0, turn=0.0, lids=0.25, smile=0.25, eyes_closed=False, fear=False, rim="#9fc2e8", wind=0.0):
    s = hair_carmen_back()
    s += head(look=look, smile=(-0.6 if fear else smile), lids=(0.0 if fear else lids), rim=rim, turn=turn, eyes_closed=eyes_closed,
              sk=SK_CARMEN, headwrap=False, lips=("#7a3a36", "#9a4e48"), iris="#2a170c", earring=True, brow_w=0.8)
    if fear:
        s += '<ellipse cx="0" cy="74" rx="14" ry="10" fill="#2a0e0a"/>'
    s += hair_carmen_front(wind=wind)
    return s


def luis_head(look=0.0, turn=0.0, lids=0.15, smile=0.3, rim="#9fc2e8", shock=False):
    r = random.Random(4)
    s = head(look=look, smile=(-0.5 if shock else smile), lids=(0.0 if shock else lids), rim=rim, turn=turn, sk=SK_LUIS, headwrap=False,
             earring=False, lips=("#6a3a2c", "#7e4a3a"), iris="#24140a", brow_w=1.25, neck=True)
    s += stubble(r, "#2a1810")
    s += '<path d="M-70,40 C-60,90 -30,116 0,118 C30,116 60,90 70,40" stroke="#3a2216" stroke-width="5" fill="none" opacity="0.35"/>'
    s += hair_luis()
    return s


def father_head(red=False, rim="#9fc2e8"):
    r = random.Random(7)
    s = head(look=0.0, smile=-0.7, lids=0.45, rim=(None if red else rim), turn=0.0, sk=SK_FATHER, headwrap=False, earring=False,
             lips=("#5a2e26", "#6a3a30"), iris="#1a0e08", brow_w=1.4)
    s += wrinkles(heavy=1.2)
    s += stubble(r, "#3a3028", 120, 90, 116, 50, 0.35)
    s += hair_father()
    s += angry_brows("#141010" if not red else "#0a0606")
    if red:
        s += ember_eyes()
        s += '<path d="M-73,-56 C-78,-12 -74,34 -60,62 M73,-56 C78,-12 74,34 60,62" stroke="#ff3a24" stroke-width="5" fill="none" opacity="0.7" filter="url(#blur1)"/>'
    return s


def brigida_head(fear=False):
    s = ('<path d="M-118,-60 C-130,-150 -70,-210 0,-212 C70,-210 130,-150 118,-60 C124,20 130,120 140,220 L-140,220 C-130,120 -124,20 -118,-60 Z" fill="#1c1a24"/>')
    for i in range(10):
        a = -150 + i * 30
        s += f'<path d="M{a},{-120+abs(a)*0.4:.0f} Q{a*0.9:.0f},40 {a*1.05:.0f},220" stroke="#3c3848" stroke-width="3" fill="none" opacity="0.4"/>'
    s += head(look=0.3, smile=(-0.6 if fear else -0.1), lids=(0.0 if fear else 0.4), rim=None, sk=SK_OLD, headwrap=False, earring=False,
              lips=("#5a3a30", "#6e4a3e"), iris="#2a1a10", brow_w=0.7)
    s += wrinkles(op=0.55, heavy=1.0)
    s += '<path d="M0,-104 C-40,-104 -70,-80 -76,-50 L-70,-56 C-50,-90 -20,-96 0,-96 C20,-96 50,-90 70,-56 L76,-50 C70,-80 40,-104 0,-104 Z" fill="#8a8680"/>'
    # rebozo framing the face
    s += ('<path d="M-118,-60 C-130,-150 -70,-210 0,-212 C70,-210 130,-150 118,-60 C110,-100 70,-140 0,-142 C-70,-140 -110,-100 -118,-60 Z" fill="#2a2634"/>')
    s += ('<path d="M-118,-60 C-112,0 -100,60 -82,110 L-60,110 C-74,60 -80,0 -82,-60 C-90,-100 -108,-90 -118,-60 Z" fill="#24202e"/>'
          '<path d="M118,-60 C112,0 100,60 82,110 L60,110 C74,60 80,0 82,-60 C90,-100 108,-90 118,-60 Z" fill="#24202e"/>')
    return s


def noble_head():
    r = random.Random(11)
    # powdered wig: rolled side curls + queue
    s = '<path d="M-96,-40 C-110,-130 -60,-178 0,-178 C60,-178 110,-130 96,-40 L96,30 L-96,30 Z" fill="#c9c4b8"/>'
    s += head(look=-0.2, smile=0.6, lids=0.55, rim=None, sk=SK_NOBLE, headwrap=False, earring=False, lips=("#8a5048", "#a0605a"), iris="#3a3428", brow_w=0.8)
    s += wrinkles(op=0.5, heavy=0.9)
    s += '<ellipse cx="-52" cy="20" rx="18" ry="12" fill="#d07a6a" opacity="0.35"/><ellipse cx="52" cy="20" rx="18" ry="12" fill="#d07a6a" opacity="0.35"/>'
    s += '<path d="M0,-104 C-46,-104 -76,-84 -82,-50 C-86,-90 -50,-150 0,-152 C50,-150 86,-90 82,-50 C76,-84 46,-104 0,-104 Z" fill="#dcd7cc"/>'
    for side in (-1, 1):
        for k in range(3):
            cy = -40 + k * 34
            s += f'<ellipse cx="{side*98}" cy="{cy}" rx="28" ry="16" fill="#e6e1d6" stroke="#9a948a" stroke-width="2"/>'
            s += f'<path d="M{side*78},{cy} a20,10 0 0 {1 if side>0 else 0} {side*40},0" stroke="#a8a296" stroke-width="2" fill="none"/>'
    s += strands(r, [(-40, -150, -60, -120, -82, -60), (40, -150, 60, -120, 82, -60)], 10, "#a8a296", (1, 2), (0.4, 0.8), 6)
    return s


# ------------------------------------------------------------------ busts (head centre at x,y; k=1 -> face ~245 tall)
def bust_frame(body, headsvg, x, y, k):
    return f'<g transform="translate({x},{y}) scale({k})"><g transform="translate(0,18) scale(0.74,0.86)">{body}</g>{headsvg}</g>'


def carmen_bust(x, y, k=1.0, rim="#9fc2e8", **hk):
    g = uid("cb"); sk = SK_CARMEN
    s = (f'<defs>{grad_lin(g+"d", [(0, "#0a1420", 1), (0.5, "#1a3448", 1), (0.85, "#2c5068", 1), (1, "#1a3448", 1)], -340, 0, 340, 0)}'
         f'{grad_lin(g+"s", [(0, sk["deep"], 1), (0.4, sk["shadow"], 1), (0.75, sk["base"], 1), (1, sk["shadow"], 1)], -220, 0, 220, 0)}'
         f'{grad_lin(g+"r", [(0, "#0c0a14", 1), (0.6, "#24203a", 1), (1, "#3c3658", 1)], -300, 200, 300, 600)}</defs>')
    # neck and chest
    s += f'<path d="M-44,40 C-44,100 -58,150 -150,186 L150,186 C58,150 44,100 44,40 Z" fill="url(#{g}s)"/>'
    s += f'<path d="M-44,60 C-30,108 30,108 44,60 L44,40 L-44,40 Z" fill="{sk["deep"]}" opacity="0.5" filter="url(#blur1)"/>'
    s += f'<path d="M-200,240 C-120,226 -60,214 0,214 C60,214 120,226 200,240 L200,260 L-200,260 Z" fill="url(#{g}s)"/>'
    # little gold cross
    s += '<path d="M-60,150 Q0,196 60,150" stroke="#c9a24a" stroke-width="2.5" fill="none"/><path d="M0,176 L0,208 M-10,186 L10,186" stroke="#e0bb5a" stroke-width="5" stroke-linecap="round"/>'
    # dress with square lace neckline
    s += f'<path d="M-250,226 C-170,236 -140,250 -130,262 L130,262 C140,250 170,236 250,226 C320,270 350,400 360,660 L-360,660 C-350,400 -320,270 -250,226 Z" fill="url(#{g}d)"/>'
    s += '<path d="M-150,262 L150,262" stroke="#e8e0cc" stroke-width="16"/>'
    for i in range(31):
        px = -150 + i * 10
        s += f'<circle cx="{px}" cy="272" r="5" fill="#e8e0cc" opacity="0.85"/>'
    for d in ["M-200,330 Q-210,480 -190,660", "M200,330 Q210,480 190,660", "M-60,300 Q-50,480 -70,660", "M60,300 Q50,480 70,660"]:
        s += f'<path d="{d}" stroke="#061018" stroke-width="10" fill="none" opacity="0.6" filter="url(#blur1)"/>'
    # rebozo over both shoulders
    for side in (-1, 1):
        s += (f'<path d="M{side*250},226 C{side*330},270 {side*370},420 {side*380},660 L{side*230},660 C{side*240},480 {side*230},330 {side*180},250 Z" fill="url(#{g}r)"/>')
        for i in range(6):
            s += f'<path d="M{side*(200+i*28)},{240+i*8} C{side*(240+i*26)},380 {side*(250+i*24)},520 {side*(240+i*24)},660" stroke="#4a4470" stroke-width="2.5" fill="none" opacity="0.5"/>'
    if rim:
        s += f'<path d="M-250,226 C-330,270 -370,420 -380,660" stroke="{rim}" stroke-width="5" fill="none" opacity="0.5" filter="url(#blur1)"/>'
    return bust_frame(s, carmen_head(rim=rim, **hk), x, y, k)


def luis_bust(x, y, k=1.0, rim="#9fc2e8", **hk):
    g = uid("lb"); sk = SK_LUIS
    s = (f'<defs>{grad_lin(g+"j", [(0, "#140d08", 1), (0.6, "#3e2a1a", 1), (1, "#5e4228", 1)], -340, 0, 340, 0)}'
         f'{grad_lin(g+"w", [(0, "#6a6458", 1), (0.6, "#bdb4a0", 1), (1, "#d8cfba", 1)], -160, 0, 160, 0)}'
         f'{grad_lin(g+"s", [(0, sk["deep"], 1), (0.5, sk["shadow"], 1), (1, sk["base"], 1)], -60, 0, 60, 0)}</defs>')
    s += f'<path d="M-50,40 C-52,110 -60,150 -70,190 L70,190 C60,150 52,110 50,40 Z" fill="url(#{g}s)"/>'
    s += f'<path d="M-50,70 C-30,116 30,116 50,70 L50,40 L-50,40 Z" fill="{sk["deep"]}" opacity="0.5" filter="url(#blur1)"/>'
    s += '<path d="M-8,120 Q0,150 8,120" stroke="#3a2216" stroke-width="3" fill="none" opacity="0.5"/>'
    # open-collar shirt
    s += f'<path d="M-230,230 C-160,190 -90,160 -60,150 L0,280 L60,150 C90,160 160,190 230,230 L250,660 L-250,660 Z" fill="url(#{g}w)"/>'
    s += '<path d="M-60,150 L-110,240 L-20,250 Z M60,150 L110,240 L20,250 Z" fill="#cfc6b0"/>'
    s += '<path d="M-60,150 L0,280 L60,150" stroke="#7a7262" stroke-width="4" fill="none"/>'
    # jacket
    for side in (-1, 1):
        s += f'<path d="M{side*130},200 C{side*260},220 {side*340},300 {side*360},660 L{side*120},660 C{side*130},480 {side*110},330 {side*70},230 Z" fill="url(#{g}j)"/>'
        s += f'<path d="M{side*130},210 C{side*110},320 {side*120},480 {side*130},660" stroke="#6e5434" stroke-width="3" fill="none" opacity="0.6"/>'
        for b in range(4):
            s += f'<circle cx="{side*112}" cy="{330+b*70}" r="7" fill="#8a7040"/>'
    s += '<path d="M-200,420 Q-150,440 -110,430 M200,420 Q150,440 110,430" stroke="#0a0604" stroke-width="10" fill="none" opacity="0.5"/>'
    if rim:
        s += f'<path d="M-130,200 C-260,220 -340,300 -360,660" stroke="{rim}" stroke-width="5" fill="none" opacity="0.5" filter="url(#blur1)"/>'
    return bust_frame(s, luis_head(rim=rim, **hk), x, y, k)


def father_bust(x, y, k=1.0, red=False, rim="#9fc2e8"):
    g = uid("fb")
    coat = ("#2a0a08", "#4a1410", "#6a1c16") if red else ("#0e0c10", "#24202a", "#38323e")
    s = (f'<defs>{grad_lin(g+"c", [(0, coat[0], 1), (0.6, coat[1], 1), (1, coat[2], 1)], -380, 0, 380, 0)}</defs>')
    s += f'<path d="M-52,40 C-54,110 -62,150 -72,190 L72,190 C62,150 54,110 52,40 Z" fill="{SK_FATHER["shadow"]}"/>'
    # white cravat
    s += '<path d="M-80,170 C-40,150 40,150 80,170 L60,300 C30,320 -30,320 -60,300 Z" fill="#cfc8b8"/><path d="M-40,200 Q0,230 40,200 M-30,250 Q0,270 30,250" stroke="#8a8474" stroke-width="3" fill="none"/>'
    # coat with gold buttons and embroidery
    s += f'<path d="M-90,170 C-220,200 -340,260 -380,660 L380,660 C340,260 220,200 90,170 L60,300 L30,660 L-30,660 L-60,300 Z" fill="url(#{g}c)"/>'
    for side in (-1, 1):
        s += f'<path d="M{side*90},176 C{side*80},300 {side*70},480 {side*60},660" stroke="#b08a3a" stroke-width="4" fill="none" opacity="0.7"/>'
        for b in range(5):
            s += f'<circle cx="{side*100}" cy="{300+b*70}" r="9" fill="#c9a24a"/>'
    if rim and not red:
        s += f'<path d="M-90,170 C-220,200 -340,260 -380,660" stroke="{rim}" stroke-width="5" fill="none" opacity="0.5" filter="url(#blur1)"/>'
    return bust_frame(s, father_head(red=red, rim=rim), x, y, k)


def brigida_bust(x, y, k=1.0, fear=False):
    s = '<path d="M-150,220 C-260,260 -340,360 -360,660 L360,660 C340,360 260,260 150,220 Z" fill="#1e1a28"/>'
    for i in range(12):
        s += f'<path d="M{-300+i*50},300 Q{-290+i*50},480 {-310+i*52},660" stroke="#3a3446" stroke-width="3" fill="none" opacity="0.5"/>'
    s += '<path d="M-150,220 C-260,260 -340,360 -360,660" stroke="#ffb860" stroke-width="5" fill="none" opacity="0.5" filter="url(#blur1)"/>'
    # hands clutching the rebozo + candle
    s += candle_hand(170, 420, 1.0)
    return bust_frame(s, brigida_head(fear=fear), x, y, k)


def candle_hand(x, y, k=1.0):
    s = ('<rect x="-16" y="-170" width="32" height="170" rx="6" fill="#e8dcc0"/><path d="M-16,-170 Q0,-160 16,-170" stroke="#c8b898" stroke-width="3" fill="none"/>'
         '<circle cx="0" cy="-200" r="150" fill="url(#warmglow)" opacity="0.9"/>'
         '<path d="M0,-240 Q14,-208 0,-180 Q-14,-208 0,-240 Z" fill="#fff3c8"/><path d="M0,-226 Q6,-206 0,-190 Q-6,-206 0,-226 Z" fill="#ffffff"/>'
         f'<path d="M-50,-30 C-40,-60 40,-60 50,-30 C60,0 40,30 0,34 C-40,30 -60,0 -50,-30 Z" fill="{SK_OLD["base"]}"/>'
         f'<path d="M-46,-26 C-20,-40 20,-40 46,-26" stroke="{SK_OLD["hi"]}" stroke-width="4" fill="none" opacity="0.6"/>'
         f'<path d="M-30,-10 l60,0 M-30,6 l60,0" stroke="{SK_OLD["deep"]}" stroke-width="2.5" opacity="0.6"/>')
    return f'<g transform="translate({x},{y}) scale({k})">{s}</g>'


def noble_bust(x, y, k=1.0):
    g = uid("nb")
    s = f'<defs>{grad_lin(g+"c", [(0, "#14100a", 1), (0.6, "#3a2c14", 1), (1, "#5a4420", 1)], -380, 0, 380, 0)}</defs>'
    s += f'<path d="M-50,40 C-52,110 -60,150 -70,190 L70,190 C60,150 52,110 50,40 Z" fill="{SK_NOBLE["shadow"]}"/>'
    s += '<path d="M-90,160 C-40,140 40,140 90,160 L70,380 C30,400 -30,400 -70,380 Z" fill="#ece6d8"/>'
    for i in range(6):
        s += f'<path d="M{-70+i*4},{200+i*30} Q0,{230+i*30} {70-i*4},{200+i*30}" stroke="#b0a894" stroke-width="3" fill="none"/>'
    s += f'<path d="M-90,166 C-220,190 -340,260 -380,660 L380,660 C340,260 220,190 90,166 L70,380 L40,660 L-40,660 L-70,380 Z" fill="url(#{g}c)"/>'
    r = random.Random(2)
    for side in (-1, 1):
        for b in range(14):
            yy = 200 + b * 32
            s += f'<path d="M{side*(96+b*2)},{yy} q{side*20},-10 {side*30},6 q{side*-10},14 {side*-30},-6" stroke="#d8b050" stroke-width="2.5" fill="none" opacity="0.8"/>'
    # ring on a hand resting on the cane
    s += f'<path d="M180,520 C200,490 260,490 280,520 C290,560 260,590 230,590 C200,590 170,560 180,520 Z" fill="{SK_NOBLE["base"]}"/><circle cx="214" cy="520" r="10" fill="#3a6a9a" stroke="#e0c060" stroke-width="4"/>'
    s += '<rect x="220" y="580" width="16" height="200" fill="#1a1008"/><circle cx="228" cy="512" r="26" fill="#c9a24a" opacity="0"/>'
    return bust_frame(s, noble_head(), x, y, k)


# ------------------------------------------------------------------ profile silhouettes (facing +x, head centre 0,0, ~240 tall)
WOMAN_HEAD = ("M-40,130 C-60,110 -96,80 -104,40 C-130,30 -140,-10 -118,-30 C-110,-90 -70,-130 -10,-130 C40,-128 64,-100 70,-60 "
              "C72,-40 76,-30 84,-16 C92,-4 96,4 92,10 C86,14 80,14 80,20 C84,26 84,32 80,36 C84,42 82,50 76,54 C74,70 66,84 48,92 "
              "C34,98 22,100 18,110 L20,140 Z")
MAN_HEAD = ("M-50,140 C-70,110 -96,60 -98,10 C-104,-60 -70,-128 -6,-132 C46,-134 70,-104 76,-64 C78,-46 80,-36 88,-22 "
            "C98,-6 102,4 96,10 C90,14 84,14 84,20 C88,28 88,34 82,38 C86,46 84,54 78,58 C76,78 66,94 46,102 C30,108 20,112 18,124 L22,150 Z")
MAN_HAIR = "M-98,10 C-104,-60 -70,-128 -6,-132 C30,-136 60,-120 70,-90 C40,-110 0,-104 -20,-90 C-50,-60 -60,-20 -70,30 Z"


def profile_figure(kind="woman", lean=0.0, arm=None, rim="#a8c8ff", fill=SIL, rim_op=0.85, ghost=False):
    """Upper body in profile facing +x; head centre (0,0). lean: degrees forward. arm: None | 'reach' | 'hold'."""
    hp = WOMAN_HEAD if kind == "woman" else MAN_HEAD
    s = ""
    # torso + shoulders (behind the neck), reaching down to y=620
    if kind == "woman":
        torso = "M-40,120 C-90,150 -150,200 -160,300 C-170,420 -150,520 -140,620 L150,620 C150,500 120,380 100,280 C90,220 60,170 20,130 Z"
        s += '<ellipse cx="-112" cy="10" rx="42" ry="36"/>'  # chignon
    else:
        torso = "M-50,130 C-110,160 -170,210 -180,320 C-190,430 -170,530 -160,620 L170,620 C170,500 140,380 120,290 C108,226 70,176 22,140 Z"
    s += f'<path d="{torso}" transform="translate(-10,40) scale(0.74,0.9)"/>'
    if arm == "reach":
        s += '<path transform="translate(0,-70) rotate(-6 60 220)" d="M60,220 C150,240 260,250 360,250 C380,250 392,262 388,276 C384,290 370,292 356,290 C250,290 140,300 40,300 Z"/>'
        s += '<path transform="translate(0,-70) rotate(-6 60 220)" d="M356,250 C380,246 410,250 420,262 C426,272 416,280 404,278 C398,286 380,290 366,288 Z"/>'
    elif arm == "hold":
        s += '<path d="M60,220 C150,236 240,246 320,250 L330,290 C240,292 140,300 40,300 Z"/>'
    s += f'<path d="{hp}"/>'
    if kind == "man":
        s += f'<path d="{MAN_HAIR}"/>'
    out = f'<g fill="{fill}">{s}</g>'
    if not ghost and rim:
        rr = random.Random(5 if kind == "woman" else 6)
        hs = "".join(f'<path d="M{rr.uniform(-90,30):.0f},{rr.uniform(-125,-100):.0f} q{rr.uniform(-60,-20):.0f},{rr.uniform(30,60):.0f} {rr.uniform(-90,-50):.0f},{rr.uniform(90,140):.0f}" stroke="#1c2a3e" stroke-width="3" fill="none" opacity="0.45"/>' for _ in range(14))
        out += hs
        out += f'<path d="M60,-30 q-10,-4 -18,2" stroke="#2a3a52" stroke-width="3" fill="none"/>'
    if rim:
        rimp = f'<path d="{hp}" stroke="{rim}" stroke-width="5" fill="none" opacity="{rim_op}" filter="url(#blur1)"/>'
        rimp += f'<path d="M-10,-130 C40,-128 64,-100 70,-60 C72,-40 76,-30 84,-16 C92,-4 96,4 92,10" stroke="#ffffff" stroke-width="2.5" fill="none" opacity="{rim_op*0.7:.2f}"/>'
        out += rimp
    if ghost:
        out = f'<g filter="url(#ghost)" opacity="0.85">{out}</g>'
    return f'<g transform="rotate({lean})">{out}</g>'


def place(frag, x, y, k=1.0, flip=False):
    fl = " scale(-1,1)" if flip else ""
    return f'<g transform="translate({x},{y}) scale({k}){fl}">{frag}</g>'


# ------------------------------------------------------------------ full-length silhouettes (feet at 0,0; ~1000 tall)
def man_full(hat=True, cape=True, dagger=False, lantern=False, walk=0.0, rim="#a8c8ff", fill=SIL, step_up=False):
    s = ""
    # legs
    if step_up:
        s += '<path d="M-60,-470 C-70,-330 -80,-200 -90,-10 L-40,-6 C-30,-160 -10,-300 0,-420 C30,-330 60,-260 110,-240 L120,-180 L170,-186 L150,-270 C110,-330 80,-400 70,-470 Z"/>'
    else:
        a = walk * 60
        s += f'<path d="M-60,-470 C-70,-330 {-80-a:.0f},-200 {-90-a:.0f},-10 L{-40-a:.0f},-6 C-30,-160 -10,-300 0,-420 C14,-300 {34+a:.0f},-160 {50+a:.0f},-8 L{104+a:.0f},-12 C96,-170 82,-330 70,-470 Z"/>'
    # torso + cape
    s += '<path d="M-80,-470 C-96,-560 -104,-660 -96,-740 C-90,-790 -40,-818 20,-820 C70,-818 104,-780 108,-720 C112,-640 100,-540 84,-470 Z"/>'
    if cape:
        s += '<path d="M-90,-780 C-160,-700 -200,-500 -220,-300 C-180,-280 -130,-300 -90,-330 C-80,-480 -70,-620 -40,-800 Z"/>'
    # head + hat
    s += '<ellipse cx="18" cy="-880" rx="56" ry="66"/><path d="M-10,-830 L50,-830 L46,-800 L-6,-800 Z"/>'
    if hat:
        s += '<path d="M-110,-920 C-60,-940 100,-940 150,-920 C120,-906 -80,-906 -110,-920 Z"/><path d="M-50,-924 C-50,-990 -30,-1010 20,-1012 C70,-1010 88,-990 88,-924 Z"/>'
    if dagger:
        s += '<path d="M90,-760 C150,-720 190,-640 200,-560 L170,-550 C150,-620 120,-680 70,-700 Z"/>'
        s += '<path d="M178,-560 L196,-566 L240,-300 L226,-298 Z" fill="#cfd8e0"/><path d="M160,-560 L214,-576" stroke="#b08a3a" stroke-width="10"/>'
    if lantern:
        s += '<path d="M90,-760 C150,-700 170,-620 176,-560 L150,-556 C140,-610 120,-660 70,-700 Z"/>'
        s += '<circle cx="170" cy="-500" r="180" fill="url(#warmglow)"/><rect x="146" y="-540" width="48" height="76" fill="#ffd98a"/>'
    out = f'<g fill="{fill}">{s}</g>'
    if rim:
        hp = "M-110,-920 C-60,-940 100,-940 150,-920 " if hat else "M-36,-900 C-30,-940 30,-950 64,-910 "
        cp = "M-90,-780 C-160,-700 -200,-500 -220,-300" if cape else "M-96,-740 C-104,-660 -96,-560 -80,-470"
        out += (f'<path d="M-96,-740 C-90,-790 -40,-818 20,-820 {hp}{cp}" stroke="{rim}" stroke-width="6" fill="none" opacity="0.8" filter="url(#blur1)"/>')
    return out


def woman_full(rebozo_head=False, candle=False, rim="#a8c8ff", fill=SIL, old=False):
    s = '<path d="M-200,0 C-180,-200 -130,-420 -90,-560 L90,-560 C130,-420 180,-200 200,0 Z"/>'  # skirt
    s += '<path d="M-90,-560 C-100,-640 -96,-720 -70,-770 C-40,-800 40,-800 70,-770 C96,-720 100,-640 90,-560 Z"/>'
    if old:
        s += '<path d="M-100,-760 C-110,-700 -130,-620 -150,-520 L150,-520 C130,-620 110,-700 100,-760 Z"/>'
    s += '<ellipse cx="0" cy="-850" rx="52" ry="64"/>'
    if rebozo_head:
        s += '<path d="M-70,-880 C-80,-940 -40,-970 0,-972 C40,-970 80,-940 70,-880 C90,-800 120,-700 150,-560 L-150,-560 C-120,-700 -90,-800 -70,-880 Z"/>'
    else:
        s += '<ellipse cx="-40" cy="-810" rx="34" ry="28"/>'
    if candle:
        s += '<path d="M60,-700 C100,-660 120,-640 130,-620 L110,-600 C96,-620 80,-640 50,-660 Z"/>'
        s += '<circle cx="130" cy="-690" r="160" fill="url(#warmglow)"/><rect x="122" y="-660" width="18" height="50" fill="#e8dcc0"/><path d="M131,-700 Q140,-680 131,-664 Q122,-680 131,-700 Z" fill="#fff3c8"/>'
    out = f'<g fill="{fill}">{s}</g>'
    if rim:
        out += (f'<path d="M-52,-860 C-50,-900 -20,-916 10,-914 M-90,-560 C-130,-420 -180,-200 -200,0" stroke="{rim}" stroke-width="6" fill="none" opacity="0.75" filter="url(#blur1)"/>')
    return out
