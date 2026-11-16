"""Custom characters for 'El Nahual': Tomás (young farmer), Lupe (his wife), don Fermín (the curandero / nahual),
abuela Chabela, and the nahual beast (a huge black dog with human eyes). Faces reuse the shared head() builder
(base_chars.py) with new skins, hair, hats, rebozos and costume; the beast is hand-drawn."""
import math, random
from base_chars import head, uid, grad_lin, grad_rad

SK_TOMAS = dict(base="#9a6644", light="#bb8158", hi="#d9a074", shadow="#64402a", deep="#331f12")
SK_LUPE = dict(base="#a87252", light="#c98e68", hi="#e6b08a", shadow="#6e4630", deep="#3a2216")
SK_OLD = dict(base="#8c6046", light="#a87a5c", hi="#c49474", shadow="#5a3c2a", deep="#2e1c12")
SK_SICK = dict(base="#7c6656", light="#968070", hi="#b09a88", shadow="#4e3e34", deep="#28201a")
SIL = "#04060a"


def strands(r, pts, n, color, w=(1.5, 3.5), op=(0.4, 0.9), jit=6):
    out = ""
    for (x0, y0, cx, cy, x1, y1) in pts:
        for _ in range(n):
            j = lambda: r.uniform(-jit, jit)
            out += (f'<path d="M{x0+j():.1f},{y0+j():.1f} Q{cx+j()*2:.1f},{cy+j()*2:.1f} {x1+j():.1f},{y1+j():.1f}" '
                    f'stroke="{color}" stroke-width="{r.uniform(*w):.1f}" fill="none" opacity="{r.uniform(*op):.2f}" stroke-linecap="round"/>')
    return out


def wrinkles(color="#2e1c12", op=0.5, heavy=1.0):
    s = ""
    for i, y in enumerate((-80, -70, -60)):
        s += f'<path d="M-42,{y} Q0,{y-8*heavy} 42,{y}" stroke="{color}" stroke-width="{2.4*heavy}" fill="none" opacity="{op*(1-i*0.2):.2f}"/>'
    s += f'<path d="M-26,34 Q-42,60 -36,86 M26,34 Q42,60 36,86" stroke="{color}" stroke-width="{2.8*heavy}" fill="none" opacity="{op}"/>'
    s += f'<path d="M-62,-14 l-13,-7 M-62,-8 l-14,2 M-60,-2 l-12,8 M62,-14 l13,-7 M62,-8 l14,2 M60,-2 l12,8" stroke="{color}" stroke-width="2" opacity="{op}"/>'
    s += f'<path d="M-50,4 Q-40,12 -14,6 M50,4 Q40,12 14,6" stroke="{color}" stroke-width="2" fill="none" opacity="{op*0.7:.2f}"/>'
    return s


def nahual_eyes(col="#ffb43a", op=0.95):
    """Amber glint in the iris: the beast's eyes looking out of a human face."""
    return ''.join(f'<circle cx="{x}" cy="-19" r="26" fill="url(#warmglow)" opacity="0.55"/><circle cx="{x}" cy="-19" r="6" fill="{col}" opacity="{op}"/>' for x in (-31, 31))


# ------------------------------------------------------------------ hair / hats / rebozo
def hair_short(seed=5, color="#0a0807"):
    r = random.Random(seed)
    s = (f'<path d="M-80,-40 C-90,-110 -50,-150 0,-150 C55,-150 92,-112 82,-40 C78,-62 70,-82 56,-94 C30,-84 -10,-96 -40,-90 C-60,-84 -74,-64 -80,-40 Z" fill="{color}"/>')
    s += strands(r, [(-70, -90, -30, -130, 20, -110), (60, -100, 20, -130, -20, -110)], 8, "#3a3230", (1.2, 2.4), (0.3, 0.6), 8)
    s += f'<path d="M-80,-40 L-78,10 L-72,-10 Z M80,-40 L78,10 L72,-10 Z" fill="{color}"/>'
    return s


def sombrero(color="#c8a868", dk="#6e5a30", hi="#e8d49a", band="#5a1410", tilt=0.0, k=1.0, worn=False):
    """Palm sombrero seen slightly from below: wide brim + tall crown. Origin = forehead centre (0,-110)."""
    g = uid("sb")
    s = f'<defs>{grad_lin(g, [(0, dk, 1), (0.55, color, 1), (1, hi, 1)], -260, 0, 260, 0)}</defs>'
    s += f'<g transform="translate(0,26) rotate({tilt}) scale({k})">'
    s += f'<path d="M-62,-150 C-66,-215 -40,-245 0,-247 C40,-245 66,-215 62,-150 Z" fill="url(#{g})"/>'
    s += f'<path d="M-62,-162 C-20,-150 20,-150 62,-162 L62,-146 C20,-134 -20,-134 -62,-146 Z" fill="{band}"/>'
    s += f'<path d="M-250,-118 C-200,-160 -100,-170 0,-170 C100,-170 200,-160 250,-118 C200,-96 100,-90 0,-92 C-100,-90 -200,-96 -250,-118 Z" fill="url(#{g})"/>'
    s += f'<path d="M-250,-118 C-200,-96 -100,-90 0,-92 C100,-90 200,-96 250,-118 C200,-104 100,-100 0,-102 C-100,-100 -200,-104 -250,-118 Z" fill="{dk}" opacity="0.8"/>'
    r = random.Random(7)
    for i in range(26):  # weave texture
        a = -240 + i * 19
        s += f'<path d="M{a},{-120 + abs(a) * 0.06:.0f} L{a*0.25:.0f},-165" stroke="{dk}" stroke-width="1.6" opacity="0.35"/>'
    if worn:
        s += '<path d="M150,-130 l20,-6 l-6,14 Z M-170,-128 l-14,-8 l2,14 Z" fill="#0a0806" opacity="0.7"/>'
    s += '</g>'
    return s


def rebozo_head(color="#24365e", dk="#0e1830", hi="#4a64a0", stripe="#c9b88a", open_=1.0):
    """Rebozo draped over the head and falling on both shoulders (drawn around a head at origin)."""
    g = uid("rb")
    s = f'<defs>{grad_lin(g, [(0, dk, 1), (0.5, color, 1), (1, hi, 1)], -200, 0, 200, 0)}</defs>'
    w = 112 * open_
    s += (f'<path d="M0,-176 C-90,-176 -126,-110 -122,-30 C-118,60 -150,150 -230,230 L-120,260 C-100,170 -{w-10:.0f},80 -{w-14:.0f},0 '
          f'C-{w-6:.0f},-80 -70,-136 0,-138 C70,-136 {w-6:.0f},-80 {w-14:.0f},0 C{w-10:.0f},80 100,170 120,260 L230,230 C150,150 118,60 122,-30 C126,-110 90,-176 0,-176 Z" fill="url(#{g})"/>')
    for i in range(6):
        y = -150 + i * 10
        s += f'<path d="M-118,{y+60} C-100,{y-20} -60,{y-28} 0,{y-30}" stroke="{stripe}" stroke-width="2" fill="none" opacity="0.35"/>'
    s += f'<path d="M-120,-20 C-118,70 -150,150 -228,228" stroke="{hi}" stroke-width="5" fill="none" opacity="0.5"/>'
    return s


def braids(color="#0b0807", hi="#3a302c", seed=3, gray=False):
    if gray: color, hi = "#7c7874", "#c8c4bc"
    s = ""
    for side in (-1, 1):
        for i in range(9):
            y = 60 + i * 30
            s += f'<ellipse cx="{side*(86 + i*4)}" cy="{y}" rx="16" ry="20" fill="{color}" transform="rotate({side*-20} {side*(86+i*4)} {y})"/>'
            s += f'<path d="M{side*(76+i*4)},{y-10} q{side*12},10 {side*22},2" stroke="{hi}" stroke-width="2.5" fill="none" opacity="0.6"/>'
        s += f'<path d="M{side*120},{336} l{side*6},30" stroke="#a8231a" stroke-width="8"/>'
    return s


def hair_center(color="#0b0807", hi="#3a302c", seed=4, gray=False):
    if gray: color, hi = "#7c7874", "#d8d4cc"
    r = random.Random(seed)
    s = (f'<path d="M0,-132 C-60,-134 -86,-96 -84,-40 C-82,0 -86,30 -92,60 L-74,40 C-70,0 -72,-40 -66,-70 C-46,-100 -16,-112 0,-116 '
         f'C16,-112 46,-100 66,-70 C72,-40 70,0 74,40 L92,60 C86,30 82,0 84,-40 C86,-96 60,-134 0,-132 Z" fill="{color}"/>')
    s += strands(r, [(0, -124, -50, -110, -76, -40), (0, -124, 50, -110, 76, -40)], 7, hi, (1.2, 2.2), (0.3, 0.6), 4)
    return s


def mustache(color="#0a0807", gray=False, big=1.0):
    if gray: color = "#d8d4cc"
    return (f'<path d="M-4,50 C-20,44 -40,46 -{50*big:.0f},{64+6*big:.0f} C-36,62 -18,60 -2,58 Z M4,50 C20,44 40,46 {50*big:.0f},{64+6*big:.0f} C36,62 18,60 2,58 Z" fill="{color}"/>'
            f'<path d="M-40,52 l-6,10 M-28,50 l-4,10 M28,50 l4,10 M40,52 l6,10" stroke="{"#ffffff" if gray else "#2a2420"}" stroke-width="1.5" opacity="0.5"/>')


# ------------------------------------------------------------------ heads
def tomas_head(look=0.0, turn=0.0, lids=0.15, smile=0.2, fear=False, hat=True, rim="#9fc2e8"):
    s = ""
    s += head(look=look, smile=(-0.8 if fear else smile), lids=(0.0 if fear else lids), rim=rim, turn=turn, sk=SK_TOMAS, headwrap=False,
              earring=False, lips=("#5a2e22", "#6e3a2c"), iris="#1a0c06", brow_w=1.4)
    if fear:
        s += '<ellipse cx="0" cy="76" rx="12" ry="10" fill="#1e0a06"/>'
        s += '<path d="M-58,-50 Q-36,-64 -10,-48 M58,-50 Q36,-64 10,-48" stroke="#120806" stroke-width="6" fill="none"/>'
        s += '<path d="M-60,-70 c-4,10 -2,18 2,24 M70,-60 c3,8 2,14 -1,20" stroke="#dbe8f4" stroke-width="3" fill="none" opacity="0.6"/>'
    s += hair_short()
    s += '<path d="M-30,96 Q0,112 30,96" stroke="#1a0e08" stroke-width="10" fill="none" opacity="0.25" filter="url(#blur1)"/>'  # stubble
    if hat:
        s += sombrero(tilt=-3)
    return s


def lupe_head(look=0.0, turn=0.0, lids=0.25, smile=0.35, fear=False, rim="#9fc2e8", rebozo=True):
    s = rebozo_head() if rebozo else ""
    s += hair_center()
    s += head(look=look, smile=(-0.8 if fear else smile), lids=(0.0 if fear else lids), rim=rim, turn=turn, sk=SK_LUPE, headwrap=False,
              earring=True, lips=("#6a2e2a", "#8a4038"), iris="#24120a", brow_w=0.8)
    if fear:
        s += '<ellipse cx="0" cy="76" rx="11" ry="9" fill="#2a0e0a"/>'
    s += hair_center().split('/>')[0] + '/>' if False else ""
    # hair framing over the forehead
    s += ('<path d="M0,-130 C-40,-130 -70,-110 -76,-64 C-60,-96 -30,-108 -4,-108 Z M0,-130 C40,-130 70,-110 76,-64 C60,-96 30,-108 4,-108 Z" fill="#0b0807"/>')
    if rebozo:
        s += ('<path d="M0,-178 C-92,-178 -128,-112 -124,-30 L-108,-30 C-110,-100 -80,-150 0,-152 C80,-150 110,-100 108,-30 L124,-30 C128,-112 92,-178 0,-178 Z" fill="#1a2848"/>')
    return s


def fermin_head(look=0.0, turn=0.0, lids=0.45, smile=0.3, eyes="human", hat=True, rim="#9fc2e8"):
    s = ""
    s += head(look=look, smile=smile, lids=lids, rim=rim, turn=turn, sk=SK_OLD, headwrap=False, earring=False,
              lips=("#4e2a20", "#62362a"), iris="#2a1608", brow_w=1.2)
    s += wrinkles(heavy=1.1)
    s += '<path d="M-80,-40 C-86,-96 -60,-126 -20,-130 L-60,-90 Z M80,-40 C86,-96 60,-126 20,-130 L60,-90 Z" fill="#d8d4cc"/>'
    s += '<path d="M-62,-52 Q-36,-66 -10,-50 M62,-52 Q36,-66 10,-50" stroke="#e8e4dc" stroke-width="7" fill="none"/>'  # white brows
    s += mustache(gray=True, big=1.2)
    if eyes == "nahual":
        s += nahual_eyes()
    if hat:
        s += sombrero(color="#a88a50", dk="#4a3a1c", hi="#d0b878", band="#1a1410", tilt=2, worn=True)
    return s


def abuela_head(rim="#ffcf8a"):
    s = rebozo_head(color="#2a1c1c", dk="#100808", hi="#5a3a34", stripe="#8a6a5a", open_=0.96)
    s += hair_center(gray=True)
    s += head(look=0.3, smile=0.1, lids=0.55, rim=rim, sk=SK_OLD, headwrap=False, earring=True, lips=("#4e2a24", "#5e3a32"), iris="#1e1008", brow_w=0.7)
    s += wrinkles(heavy=1.3)
    s += ('<path d="M0,-180 C-94,-180 -130,-112 -126,-30 L-110,-30 C-112,-100 -82,-152 0,-154 C82,-152 112,-100 110,-30 L126,-30 C130,-112 94,-180 0,-180 Z" fill="#1c1212"/>')
    return s


# ------------------------------------------------------------------ busts (head centre at x,y; k=1 -> face ~245 tall)
def bust_frame(body, headsvg, x, y, k, back=""):
    return f'<g transform="translate({x},{y}) scale({k})">{back}<g transform="translate(0,18) scale(0.74,0.86)">{body}</g>{headsvg}</g>'


def shirt_body(g, sk, rim, cloth=("#5e5a52", "#cfc8b6", "#efe8d6"), sarape=True):
    s = (f'<defs>{grad_lin(g+"d", [(0, cloth[0], 1), (0.5, cloth[1], 1), (0.85, cloth[2], 1), (1, cloth[1], 1)], -360, 0, 360, 0)}'
         f'{grad_lin(g+"s", [(0, sk["deep"], 1), (0.4, sk["shadow"], 1), (0.75, sk["base"], 1), (1, sk["shadow"], 1)], -220, 0, 220, 0)}</defs>')
    s += f'<path d="M-50,40 C-50,100 -60,150 -90,180 L90,180 C60,150 50,100 50,40 Z" fill="url(#{g}s)"/>'
    s += f'<path d="M-90,170 C-220,190 -330,250 -370,380 L-390,660 L390,660 L370,380 C330,250 220,190 90,170 L30,240 L0,200 L-30,240 Z" fill="url(#{g}d)"/>'
    s += f'<path d="M-30,240 L0,200 L30,240 L0,330 Z" fill="{sk["shadow"]}"/>'
    for d in ["M-200,260 Q-220,420 -200,660", "M200,260 Q220,420 200,660", "M-60,330 Q-50,480 -70,660"]:
        s += f'<path d="{d}" stroke="{cloth[0]}" stroke-width="10" fill="none" opacity="0.45" filter="url(#blur1)"/>'
    if sarape:
        s += '<path d="M90,170 C220,190 330,250 370,380 L390,660 L230,660 C210,450 170,300 60,230 Z" fill="#7a1a14"/>'
        for i, c in enumerate(("#e8b030", "#1e4a6a", "#e8e0cc", "#1e4a6a", "#e8b030")):
            s += f'<path d="M{120+i*44},{200+i*16} C{200+i*40},{330+i*10} {240+i*30},{480} {250+i*28},660" stroke="{c}" stroke-width="9" fill="none" opacity="0.85"/>'
    if rim:
        s += f'<path d="M-90,170 C-220,190 -330,250 -370,380 L-390,660" stroke="{rim}" stroke-width="7" fill="none" opacity="0.55" filter="url(#blur1)"/>'
    return s


def blouse_body(g, sk, rim, rebozo=("#24365e", "#0e1830", "#4a64a0")):
    s = (f'<defs>{grad_lin(g+"d", [(0, "#5e5a52", 1), (0.5, "#d8d2c6", 1), (1, "#f4efe4", 1)], -340, 0, 340, 0)}'
         f'{grad_lin(g+"r", [(0, rebozo[1], 1), (0.5, rebozo[0], 1), (1, rebozo[2], 1)], -380, 0, 380, 0)}'
         f'{grad_lin(g+"s", [(0, sk["deep"], 1), (0.4, sk["shadow"], 1), (0.75, sk["base"], 1), (1, sk["shadow"], 1)], -220, 0, 220, 0)}</defs>')
    s += f'<path d="M-44,40 C-44,100 -58,150 -150,186 L150,186 C58,150 44,100 44,40 Z" fill="url(#{g}s)"/>'
    s += f'<path d="M-300,226 C-200,190 -150,180 -110,176 Q0,240 110,176 C150,180 200,190 300,226 C350,300 370,420 380,660 L-380,660 C-370,420 -350,300 -300,226 Z" fill="url(#{g}d)"/>'
    for i in range(14):  # embroidered neckline flowers
        t = (i - 6.5) / 6.5; x = t * 128; y = 196 + 50 * (1 - t * t)
        s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="9" fill="{"#c8283a" if i%2 else "#2e8a5a"}"/><circle cx="{x:.0f}" cy="{y:.0f}" r="3" fill="#f4d47a"/>'
    # rebozo over the shoulders, crossing in front
    s += f'<path d="M-330,230 C-250,200 -170,200 -120,240 C-40,320 60,420 200,660 L-380,660 C-380,420 -370,300 -330,230 Z" fill="url(#{g}r)"/>'
    s += f'<path d="M330,230 C260,200 190,200 150,250 C110,330 80,420 60,660 L380,660 C380,420 370,300 330,230 Z" fill="url(#{g}r)"/>'
    for i in range(10):
        s += f'<path d="M{-300+i*26},{620+i*2} l-4,40" stroke="{rebozo[2]}" stroke-width="3" opacity="0.5"/>'
    for i in range(5):
        s += f'<path d="M{-300+i*30},250 C{-200+i*40},330 {-60+i*50},480 {120+i*30},660" stroke="#c9b88a" stroke-width="2" fill="none" opacity="0.25"/>'
    if rim:
        s += f'<path d="M-330,230 C-370,300 -380,420 -380,660" stroke="{rim}" stroke-width="6" fill="none" opacity="0.55" filter="url(#blur1)"/>'
    return s


def tomas_bust(x, y, k=1.0, rim="#9fc2e8", **hk):
    g = uid("tb")
    return bust_frame(shirt_body(g, SK_TOMAS, rim), tomas_head(rim=rim, **hk), x, y, k)


def lupe_bust(x, y, k=1.0, rim="#9fc2e8", **hk):
    g = uid("lb")
    back = rebozo_head()  # drawn behind body too so the rebozo frames the shoulders
    return bust_frame(blouse_body(g, SK_LUPE, rim), lupe_head(rim=rim, rebozo=False, **hk), x, y, k, back=back + braids())


def fermin_bust(x, y, k=1.0, rim="#9fc2e8", bandage=False, **hk):
    g = uid("fb")
    body = shirt_body(g, SK_OLD, rim, cloth=("#4a463e", "#b8b0a0", "#d8d0bc"), sarape=False)
    body += '<path d="M-90,170 C-220,190 -330,250 -370,380 L-390,660 L-250,660 C-240,450 -200,300 -60,230 Z" fill="#3a2e22" opacity="0.9"/>'  # dark jorongo
    s = bust_frame(body, fermin_head(rim=rim, **hk), x, y, k)
    if bandage:
        s += f'<g transform="translate({x+280*k},{y+300*k}) scale({k})">{bandaged_hand()}</g>'
    return s


def abuela_bust(x, y, k=1.0, rim="#ffcf8a"):
    g = uid("ab")
    back = rebozo_head(color="#2a1c1c", dk="#100808", hi="#5a3a34", stripe="#8a6a5a")
    return bust_frame(blouse_body(g, SK_OLD, rim, rebozo=("#2a1c1c", "#100808", "#5a3a34")), abuela_head(rim=rim), x, y, k, back=back + braids(gray=True))


def bandaged_hand(k=1.0, blood=True):
    """Old man's right hand wrapped in a stained cloth, held up. Origin at the wrist."""
    s = '<path d="M-60,200 C-60,120 -50,40 -40,-10 L40,-10 C50,40 60,120 60,200 Z" fill="#4a463e"/>'  # sleeve
    s += '<path d="M-48,0 C-60,-60 -58,-120 -40,-150 C-20,-176 30,-176 46,-150 C62,-120 60,-60 48,0 Z" fill="#d8d0bc"/>'
    for i in range(6):
        y = -20 - i * 24
        s += f'<path d="M-52,{y} C-20,{y-14} 20,{y-10} 54,{y-22}" stroke="#a89c84" stroke-width="4" fill="none"/>'
    if blood:
        s += '<path d="M-10,-120 C10,-140 34,-128 30,-100 C26,-80 6,-70 -8,-84 C-20,-96 -24,-108 -10,-120 Z" fill="#6a0e0c" opacity="0.85"/>'
        s += '<path d="M14,-82 C18,-60 12,-40 16,-24" stroke="#6a0e0c" stroke-width="6" fill="none" opacity="0.7"/>'
    # fingertips peeking out
    for i, x in enumerate((-30, -10, 10, 30)):
        s += f'<path d="M{x-8},-168 C{x-8},{-196-4*(i%2)} {x+8},{-196-4*(i%2)} {x+8},-168 Z" fill="{SK_OLD["base"]}"/>'
    return f'<g transform="scale({k})">{s}</g>'


# ------------------------------------------------------------------ the beast
def beast_head(eyes="human", smile=0.0, rim="#8fb4dc", lids=0.35, glow=True, seed=4):
    """Close 3/4 front view of the huge black dog. Local coords: eyes around y=0, muzzle down to y~360, ears up to y~-360.
    eyes='human' draws almond human eyes with lids and white sclera; 'glow' adds amber light."""
    r = random.Random(seed)
    g = uid("bh")
    s = (f'<defs>{grad_rad(g+"f", [(0, "#2a2e36", 1), (0.6, "#101218", 1), (1, "#040508", 1)], 0.5, 0.42, 0.6)}'
         f'{grad_lin(g+"m", [(0, "#06070a", 1), (0.6, "#1a1c22", 1), (1, "#2c2e36", 1)], 0, 120, 0, 380)}</defs>')
    # neck / ruff
    s += '<path d="M-430,520 C-420,300 -330,160 -250,120 L250,120 C330,160 420,300 430,520 Z" fill="#05060a"/>'
    # ears
    for side in (-1, 1):
        s += (f'<path d="M{side*130},-150 C{side*170},-260 {side*210},-340 {side*250},-380 C{side*270},-300 {side*280},-200 {side*250},-90 Z" fill="#07080c"/>'
              f'<path d="M{side*160},-160 C{side*190},-240 {side*220},-300 {side*240},-330 C{side*250},-270 {side*254},-200 {side*236},-120 Z" fill="#3a1a1a" opacity="0.6"/>')
    # skull
    s += (f'<path d="M-250,-80 C-270,-200 -150,-250 0,-252 C150,-250 270,-200 250,-80 C246,10 220,90 170,150 C130,200 100,260 90,330 '
          f'C60,370 -60,370 -90,330 C-100,260 -130,200 -170,150 C-220,90 -246,10 -250,-80 Z" fill="url(#{g}f)"/>')
    # muzzle
    s += (f'<path d="M-110,90 C-120,180 -110,280 -80,340 C-40,372 40,372 80,340 C110,280 120,180 110,90 C70,60 -70,60 -110,90 Z" fill="url(#{g}m)"/>')
    # nose
    s += ('<path d="M-56,300 C-60,270 -30,256 0,256 C30,256 60,270 56,300 C52,330 20,342 0,342 C-20,342 -52,330 -56,300 Z" fill="#020203"/>'
          '<path d="M-36,276 C-20,266 20,266 36,276" stroke="#5a6070" stroke-width="5" fill="none" opacity="0.7"/>'
          '<ellipse cx="-22" cy="308" rx="10" ry="7" fill="#000"/><ellipse cx="22" cy="308" rx="10" ry="7" fill="#000"/>')
    # mouth / lips (smile pulls the corners up and shows teeth)
    up = 40 * smile
    s += f'<path d="M0,342 L0,372 M0,372 C-40,390 -90,{380-up:.0f} -140,{330-up*1.6:.0f} M0,372 C40,390 90,{380-up:.0f} 140,{330-up*1.6:.0f}" stroke="#000" stroke-width="7" fill="none"/>'
    if smile > 0.3:
        for i in range(9):
            t = (i - 4) / 4.0
            x = t * 120; yb = 372 - abs(t) * up * 1.2 + 6
            s += f'<path d="M{x-8:.0f},{yb:.0f} L{x:.0f},{yb+18+(8 if abs(t)>0.7 else 0):.0f} L{x+8:.0f},{yb:.0f} Z" fill="#d8d0c0"/>'
        s += f'<path d="M-130,{336-up*1.4:.0f} C-60,{396:.0f} 60,396 130,{336-up*1.4:.0f}" stroke="#5a0a0a" stroke-width="4" fill="none" opacity="0.8"/>'
    # fur strands
    s += strands(r, [(-240, -100, -270, 50, -200, 160), (240, -100, 270, 50, 200, 160), (-150, -230, -60, -260, 0, -230),
                     (150, -230, 60, -260, 0, -230), (-160, 120, -210, 300, -300, 420), (160, 120, 210, 300, 300, 420)], 14,
                 "#2a2e38", (1.5, 3.2), (0.3, 0.7), 18)
    s += strands(r, [(-100, 100, -110, 220, -84, 320), (100, 100, 110, 220, 84, 320)], 8, "#3a3e48", (1.2, 2.2), (0.3, 0.6), 10)
    # brow ridge, stop
    s += '<path d="M-200,-60 C-150,-110 -70,-100 -30,-50 M200,-60 C150,-110 70,-100 30,-50" stroke="#000" stroke-width="12" fill="none" opacity="0.7"/>'
    s += '<path d="M-30,-40 C-20,40 -40,80 -60,110 M30,-40 C20,40 40,80 60,110" stroke="#000" stroke-width="6" fill="none" opacity="0.5"/>'
    # eyes
    for side in (-1, 1):
        cx = side * 110; cy = -10
        eye = f"M{cx-side*62},{cy+8} Q{cx},{cy-46} {cx+side*58},{cy-4} Q{cx},{cy+30} {cx-side*62},{cy+8} Z"
        cid = uid("be")
        s += f'<defs><clipPath id="{cid}"><path d="{eye}"/></clipPath></defs>'
        if eyes == "human":
            s += f'<path d="{eye}" fill="#d6ccb8"/>'
            s += (f'<g clip-path="url(#{cid})"><circle cx="{cx-side*6}" cy="{cy-6}" r="22" fill="#6a3a12"/><circle cx="{cx-side*6}" cy="{cy-6}" r="15" fill="#2a1406"/>'
                  f'<circle cx="{cx-side*6}" cy="{cy-6}" r="8" fill="#000"/><circle cx="{cx-side*6+7}" cy="{cy-14}" r="5" fill="#fff8ee"/>'
                  f'<path d="M{cx-side*70},{cy-50} L{cx+side*70},{cy-50} L{cx+side*70},{cy-10+lids*0} Q{cx},{cy-46+lids*40} {cx-side*70},{cy+4} Z" fill="#1a1c22"/></g>')
            s += f'<path d="M{cx-side*64},{cy+8} Q{cx},{cy-46+lids*40} {cx+side*60},{cy-4}" stroke="#000" stroke-width="6" fill="none"/>'
            s += f'<path d="M{cx-side*58},{cy+14} Q{cx},{cy+36} {cx+side*54},{cy+2}" stroke="#3a3e48" stroke-width="3" fill="none" opacity="0.7"/>'
            s += f'<path d="M{cx-side*50},{cy-30+lids*20} Q{cx},{cy-60+lids*30} {cx+side*50},{cy-26+lids*16}" stroke="#2a2e38" stroke-width="3" fill="none" opacity="0.7"/>'  # eyelid crease
            if glow:
                s += f'<circle cx="{cx-side*6}" cy="{cy-6}" r="80" fill="url(#warmglow)" opacity="0.35"/>'
        else:
            s += f'<path d="{eye}" fill="#ffb43a"/><ellipse cx="{cx}" cy="{cy-4}" rx="7" ry="20" fill="#000"/>'
    # moonlight rim
    s += f'<path d="M-250,-80 C-270,-200 -150,-250 0,-252" stroke="{rim}" stroke-width="8" fill="none" opacity="0.6" filter="url(#blur1)"/>'
    s += f'<path d="M-130,-150 C-170,-260 -210,-340 -250,-380" stroke="{rim}" stroke-width="6" fill="none" opacity="0.5" filter="url(#blur1)"/>'
    s += f'<path d="M-110,90 C-120,180 -110,280 -80,340" stroke="{rim}" stroke-width="5" fill="none" opacity="0.4" filter="url(#blur1)"/>'
    return s


def beast_body(rim="#8fb4dc", fill="#030407", eyes=True, limp=False, sit=False, head_low=True, seed=2):
    """Side view (facing right) of the huge black dog, shadow-theatre style. Ground at y=0, ~1000 long, ~620 tall."""
    r = random.Random(seed)
    if sit:
        d = ("M-120,0 C-160,-60 -170,-200 -120,-300 C-90,-380 -40,-440 20,-470 C40,-520 60,-560 90,-600 L110,-660 L130,-600 L150,-640 L160,-580 "
             "C200,-560 240,-540 260,-520 L250,-490 C220,-480 190,-470 170,-450 C150,-400 120,-330 110,-240 C100,-150 110,-60 130,0 L80,0 "
             "C70,-60 60,-120 40,-180 C10,-120 0,-60 10,0 Z M-120,0 C-200,10 -260,-10 -280,-40 C-250,-30 -190,-20 -140,-20 Z")
        ex, ey = 200, -540
    else:
        h = 110 if head_low else 0   # head drop
        d = (f"M-430,-420 C-300,-455 -100,-440 60,-452 C150,-460 210,-490 250,-500 C300,-{520-h*0.4:.0f} 340,-{545-h*0.7:.0f} 390,-{560-h:.0f} "
             f"L405,-{640-h:.0f} L440,-{575-h:.0f} L470,-{650-h:.0f} L486,-{570-h:.0f} C520,-{560-h:.0f} 560,-{540-h:.0f} 600,-{515-h:.0f} "
             f"L650,-{495-h:.0f} C660,-{480-h:.0f} 650,-{466-h:.0f} 630,-{462-h:.0f} C590,-{452-h:.0f} 545,-{445-h:.0f} 520,-{440-h:.0f} "
             f"C480,-{425-h:.0f} 430,-{410-h*0.6:.0f} 390,-{390-h*0.3:.0f} C350,-360 335,-320 330,-270 "
             f"C336,-200 340,-120 342,-40 C346,-20 368,-10 380,0 L310,0 C300,-14 296,-30 296,-44 C290,-120 278,-190 262,-240 "
             f"C200,-262 100,-250 -40,-252 C-90,-256 -130,-270 -160,-280 "
             f"C-150,-220 -170,-170 -205,-130 C-225,-100 -232,-60 -226,-30 C-220,-12 -200,-4 -180,0 L-252,0 C-268,-20 -276,-50 -280,-90 "
             f"C-300,-150 -330,-200 -370,-250 C-410,-300 -440,-350 -440,-400 "
             f"C-480,-400 -540,-360 -580,-290 C-610,-230 -620,-170 -600,-130 C-590,-190 -560,-260 -520,-310 C-490,-345 -460,-370 -430,-390 Z")
        # far legs (one step behind, darker)
        far = ("M250,-250 C230,-180 210,-110 200,-40 C196,-20 210,-8 228,0 L170,0 C160,-16 158,-36 162,-60 C172,-140 190,-210 210,-260 Z "
               "M-250,-280 C-260,-210 -290,-150 -320,-110 C-336,-80 -338,-40 -330,-14 L-376,0 C-386,-30 -384,-70 -370,-110 C-350,-170 -320,-230 -300,-290 Z")
        ex, ey = 520, -(530 - h)
    s = ""
    if rim:
        s += f'<path d="{d}" fill="{rim}" filter="url(#blur2)" opacity="0.75"/>'
    if not sit:
        s += f'<path d="{far}" fill="#0c0e14" opacity="{1 if fill != "#000" else 0.9}"/>'
    s += f'<path d="{d}" fill="{fill}"/>'
    # bristling fur on the back
    for i in range(44):
        if sit: break
        x = -420 + i * 15
        y = -430 - (x + 420) / 680 * 40 if x < 260 else -480
        s += f'<path d="M{x},{y+8:.0f} l{r.uniform(-4,12):.0f},{-r.uniform(14,34):.0f}" stroke="{fill}" stroke-width="5" stroke-linecap="round"/>'
    if not sit:  # shaggy ruff under the neck and belly fringe
        for i in range(16):
            x = 330 + i * 8; y = -380 + i * 6
            s += f'<path d="M{x},{y} l{r.uniform(-14,-4):.0f},{r.uniform(14,30):.0f}" stroke="{fill}" stroke-width="5" stroke-linecap="round"/>'
        for i in range(22):
            x = 240 - i * 18; y = -250 - (i > 14) * 15
            s += f'<path d="M{x},{y} l{r.uniform(-6,4):.0f},{r.uniform(10,22):.0f}" stroke="{fill}" stroke-width="5" stroke-linecap="round"/>'
    if eyes:
        s += f'<circle cx="{ex}" cy="{ey}" r="40" fill="url(#warmglow)"/><ellipse cx="{ex}" cy="{ey}" rx="12" ry="6" fill="#ffd27a"/>'
    return s
