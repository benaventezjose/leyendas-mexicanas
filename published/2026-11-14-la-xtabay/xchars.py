"""Custom characters for 'La Xtabay': the Xtabay (white huipil, ankle-long black hair, big black eyes),
Xkeban (warm, loose hair with white flowers), Utz Colel (pale, tight bun, haughty), Lencho, Candelaria, abuela Nicolasa.
Faces reuse head() from base_chars.py; hair, huipiles and full figures are drawn here."""
import math, random
from base_chars import head, uid, grad_lin, grad_rad
from chars import strands, hair_center, braids, rebozo_head, bust_frame, blouse_body, tomas_bust, lupe_bust, abuela_bust, SK_LUPE, SK_TOMAS

SK_X = dict(base="#b58466", light="#d2a084", hi="#ecc4a8", shadow="#7a523c", deep="#3e2618")      # Xtabay: luminous
SK_XK = dict(base="#a87252", light="#c98e68", hi="#e6b08a", shadow="#6e4630", deep="#3a2216")     # Xkeban warm
SK_UTZ = dict(base="#b49a88", light="#ccb4a2", hi="#e4d0c2", shadow="#7c6658", deep="#40322a")    # Utz Colel pale
SK_DEAD = dict(base="#8a8c94", light="#a4a8b0", hi="#c8ccd4", shadow="#5a5c66", deep="#24262e")   # ghostly
HAIR = "#07060a"; HAIR_HI = "#3a4660"


def flower(x, y, r=14, col="#f6f1e4", c2="#e8c860", n=5, rot=0):
    s = ""
    for i in range(n):
        a = math.radians(rot + i * 360 / n)
        s += f'<ellipse cx="{x+math.cos(a)*r*0.7:.1f}" cy="{y+math.sin(a)*r*0.7:.1f}" rx="{r*0.62:.1f}" ry="{r*0.38:.1f}" fill="{col}" transform="rotate({rot+i*360/n:.0f} {x+math.cos(a)*r*0.7:.1f} {y+math.sin(a)*r*0.7:.1f})"/>'
    return s + f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r*0.28:.1f}" fill="{c2}"/>'


def trumpet(x, y, k=1.0, rot=0, col="#f4f2ea", glow=False):
    """xtabentún morning-glory: white trumpet flower."""
    s = f'<g transform="translate({x},{y}) rotate({rot}) scale({k})">'
    if glow:
        s += '<circle cx="0" cy="-30" r="60" fill="url(#whiteglow)" opacity="0.5"/>'
    s += f'<path d="M-6,30 C-8,0 -26,-30 -40,-50 C-20,-62 20,-62 40,-50 C26,-30 8,0 6,30 Z" fill="{col}"/>'
    s += '<path d="M-40,-50 C-20,-62 20,-62 40,-50 C20,-44 -20,-44 -40,-50 Z" fill="#ffffff"/>'
    s += '<path d="M0,26 L0,-46 M-4,20 L-24,-48 M4,20 L24,-48" stroke="#c8d0c0" stroke-width="2" opacity="0.7"/>'
    s += '<path d="M-6,30 L6,30 L4,44 L-4,44 Z" fill="#3a5a2a"/></g>'
    return s


# ------------------------------------------------------------------ hair
def long_hair_back(seed=2, length=1.0, spread=1.0, col=HAIR, hi=HAIR_HI, wave=1.0):
    """Mass of straight black hair behind a head at origin, falling to y = 640*length."""
    r = random.Random(seed); L = 640 * length; W = 150 * spread
    s = (f'<path d="M0,-150 C-95,-150 -120,-80 -118,0 C-130,{L*0.4:.0f} -{W+30:.0f},{L*0.75:.0f} -{W+20:.0f},{L:.0f} '
         f'C-{W*0.4:.0f},{L+40:.0f} {W*0.4:.0f},{L+40:.0f} {W+20:.0f},{L:.0f} C{W+30:.0f},{L*0.75:.0f} 130,{L*0.4:.0f} 118,0 C120,-80 95,-150 0,-150 Z" fill="{col}"/>')
    for i in range(46):
        x0 = r.uniform(-110, 110); xe = x0 * (W + 20) / 110 + r.uniform(-20, 20)
        w = r.uniform(10, 26) * wave
        s += (f'<path d="M{x0:.0f},{r.uniform(-120,0):.0f} C{x0+w:.0f},{L*0.3:.0f} {xe-w:.0f},{L*0.65:.0f} {xe:.0f},{L+r.uniform(-30,30):.0f}" '
              f'stroke="{hi}" stroke-width="{r.uniform(1.2,3.2):.1f}" fill="none" opacity="{r.uniform(0.15,0.5):.2f}"/>')
    return s


def front_hair(col=HAIR, hi=HAIR_HI, seed=4, length=1.0):
    """Centre-parted hair over the forehead, falling in two curtains past the shoulders in front."""
    r = random.Random(seed); L = 420 * length
    s = (f'<path d="M0,-134 C-50,-134 -84,-104 -86,-50 C-88,20 -96,{L*0.5:.0f} -124,{L*0.92:.0f} L-104,{L:.0f} L-90,{L*0.94:.0f} L-76,{L*0.98:.0f} C-66,{L*0.5:.0f} -72,0 -70,-50 C-60,-96 -24,-114 0,-116 Z" fill="{col}"/>'
         f'<path d="M0,-134 C50,-134 84,-104 86,-50 C88,20 96,{L*0.5:.0f} 124,{L*0.92:.0f} L104,{L:.0f} L90,{L*0.94:.0f} L76,{L*0.98:.0f} C66,{L*0.5:.0f} 72,0 70,-50 C60,-96 24,-114 0,-116 Z" fill="{col}"/>')
    s += strands(r, [(-30, -124, -92, -60, -100, L*0.92), (30, -124, 92, -60, 100, L*0.92)], 12, hi, (1.2, 2.6), (0.25, 0.6), 10)
    return s


def black_eyes(red=False):
    """Eyes become fully black wells with a pinpoint glint (the scare face)."""
    s = ""
    for x in (-31, 31):
        s += f'<path d="M{x-27},-17 Q{x},-42 {x+25},-18 Q{x},0 {x-27},-17 Z" fill="#000"/>'
        s += f'<ellipse cx="{x}" cy="-19" rx="34" ry="22" fill="#000" opacity="0.45" filter="url(#blur1)"/>'
        s += f'<circle cx="{x+2}" cy="-21" r="3.2" fill="{"#ff2a20" if red else "#dfe8f4"}"/>'
    return s


def gaping_mouth():
    return ('<path d="M-30,62 C-30,100 -16,170 0,172 C16,170 30,100 30,62 C16,70 -16,70 -30,62 Z" fill="#050101"/>'
            '<path d="M-30,62 C-16,58 16,58 30,62" stroke="#3a0a08" stroke-width="5" fill="none"/>'
            '<path d="M-22,70 l4,14 l4,-13 M-6,72 l3,14 l3,-14 M8,72 l3,13 l3,-13" fill="#d8d4c8"/>')


# ------------------------------------------------------------------ bodies
def huipil_body(g, sk, rim, cloth=("#8a9098", "#e4e6e2", "#fbfbf6"), emb=("#c8283a", "#2e8a5a", "#e8b030", "#7a3aa0"), glowy=False):
    """Yucatecan huipil: white, square neckline framed by a band of cross-stitch flowers."""
    s = (f'<defs>{grad_lin(g+"d", [(0, cloth[0], 1), (0.5, cloth[1], 1), (0.85, cloth[2], 1), (1, cloth[1], 1)], -360, 0, 360, 0)}'
         f'{grad_lin(g+"s", [(0, sk["deep"], 1), (0.4, sk["shadow"], 1), (0.75, sk["base"], 1), (1, sk["shadow"], 1)], -220, 0, 220, 0)}</defs>')
    s += f'<path d="M-44,40 C-44,100 -58,150 -150,186 L150,186 C58,150 44,100 44,40 Z" fill="url(#{g}s)"/>'
    s += f'<path d="M-300,226 C-220,196 -170,186 -130,182 L-130,300 L130,300 L130,182 C170,186 220,196 300,226 C350,300 370,420 380,660 L-380,660 C-370,420 -350,300 -300,226 Z" fill="url(#{g}d)"/>'
    s += f'<path d="M-130,180 L-130,300 L130,300 L130,180 C60,150 -60,150 -130,180 Z" fill="url(#{g}s)"/>'
    s += f'<path d="M-60,200 Q0,236 60,200" stroke="{sk["deep"]}" stroke-width="4" fill="none" opacity="0.4"/>'
    # embroidered square frame
    r = random.Random(7)
    band = ""
    pts = [(-150 + i * 20, 316) for i in range(16)] + [(-150, 190 + i * 21) for i in range(6)] + [(150, 190 + i * 21) for i in range(6)]
    for i, (x, y) in enumerate(pts):
        band += flower(x, y, 11, emb[i % len(emb)], "#f4d47a", 5, r.uniform(0, 70))
        band += f'<path d="M{x-8},{y+12} q8,6 16,0" stroke="#2e7a4a" stroke-width="3" fill="none"/>'
    s += f'<path d="M-160,180 L-160,330 L160,330 L160,180" stroke="#1a1a1a" stroke-width="4" fill="none" opacity="0.25"/>' + band
    for d in ["M-230,280 Q-250,440 -230,660", "M230,280 Q250,440 230,660", "M-40,360 Q-30,500 -50,660", "M80,360 Q90,500 70,660"]:
        s += f'<path d="{d}" stroke="{cloth[0]}" stroke-width="12" fill="none" opacity="0.4" filter="url(#blur1)"/>'
    if rim:
        s += f'<path d="M-300,226 C-350,300 -370,420 -380,660" stroke="{rim}" stroke-width="7" fill="none" opacity="0.6" filter="url(#blur1)"/>'
        s += f'<path d="M300,226 C350,300 370,420 380,660" stroke="{rim}" stroke-width="4" fill="none" opacity="0.35" filter="url(#blur1)"/>'
    if glowy:
        s += '<ellipse cx="0" cy="420" rx="420" ry="300" fill="url(#whiteglow)" opacity="0.25"/>'
    return s


# ------------------------------------------------------------------ busts
def xtabay_bust(x, y, k=1.0, rim="#a8d0ff", look=0.0, smile=0.45, lids=0.3, scare=0, turn=0.0, comb=False):
    """scare: 0 beautiful, 1 black eyes + cold smile, 2 black eyes + gaping mouth, skin turned ashen."""
    g = uid("xb")
    sk = SK_X if scare == 0 else SK_DEAD
    back = '<ellipse cx="0" cy="40" rx="260" ry="320" fill="url(#moonglow)" opacity="0.35"/>' + long_hair_back(3, 0.98, 1.25)
    hs = head(look=look, smile=(smile if scare < 2 else 0), lids=lids, rim=rim, turn=turn, sk=sk, headwrap=False, earring=False,
              lips=(("#6a1e22", "#8c2a2e") if scare == 0 else ("#2a1418", "#3a1c20")), iris="#0a0505", brow_w=0.9)
    if scare:
        hs += black_eyes(red=scare == 2)
        hs += '<path d="M-60,-60 C-30,-40 30,-40 60,-60" stroke="#000" stroke-width="0" fill="none"/>'
        hs += '<ellipse cx="0" cy="0" rx="90" ry="130" fill="#203040" opacity="0.18"/>'
    if scare == 2:
        hs += gaping_mouth()
    hs += front_hair()
    # white flowers of xtabentún tucked behind the ear
    hs += trumpet(-92, -70, 0.55, -40) + trumpet(-80, -96, 0.45, -70)
    body = huipil_body(g, sk, rim, glowy=True)
    s = bust_frame(body, hs, x, y, k, back=back)
    if comb:
        s += f'<g transform="translate({x+150*k},{y+120*k}) scale({k})">{comb_hand(sk)}</g>'
    return s


def comb_hand(sk=SK_X):
    """A slender hand drawing a comb of long cactus spines down a lock of hair."""
    s = '<path d="M-10,-200 C-20,-60 -6,120 20,320" stroke="#07060a" stroke-width="70" fill="none" stroke-linecap="round"/>'
    s += '<path d="M10,-200 C0,-60 14,120 40,320" stroke="#3a4660" stroke-width="2" fill="none" opacity="0.6"/>'
    s += f'<path d="M-40,60 C-60,20 -40,-10 0,-20 C40,-28 70,-10 74,20 C76,46 60,70 30,76 C0,80 -30,80 -40,60 Z" fill="{sk["base"]}"/>'
    for i in range(4):
        s += f'<path d="M{-30+i*24},-16 C{-34+i*24},-60 {-20+i*24},-70 {-14+i*24},-20" fill="{sk["light"]}" stroke="{sk["shadow"]}" stroke-width="2"/>'
    for i in range(9):  # spines
        s += f'<path d="M{-50+i*13},-4 L{-70+i*13},-130" stroke="#e8dcc0" stroke-width="3" stroke-linecap="round"/>'
    s += '<rect x="-60" y="-14" width="120" height="18" rx="6" fill="#4a3a26"/>'
    return s


def xkeban_bust(x, y, k=1.0, rim="#ffcf8a", **hk):
    g = uid("xk")
    back = long_hair_back(5, 0.9, 1.0, hi="#5a3a28")
    hs = head(rim=rim, sk=SK_XK, headwrap=False, earring=True, lips=("#7a2e2a", "#9a4038"), iris="#2a1408", brow_w=0.8,
              smile=hk.get("smile", 0.7), lids=hk.get("lids", 0.3), look=hk.get("look", 0.0), turn=hk.get("turn", 0.0))
    hs += front_hair(hi="#5a3a28", length=0.9)
    for i, (fx_, fy) in enumerate(((-86, -96), (-100, -60), (-70, -124), (88, -100))):
        hs += flower(fx_, fy, 16, "#fbf6ea", "#f0b830", 6, i * 20)
    body = huipil_body(g, SK_XK, rim, cloth=("#7a6a58", "#e8dcc4", "#f8f0de"), emb=("#d84a3a", "#e8a030", "#3a8a5a"))
    return bust_frame(body, hs, x, y, k, back=back)


def utz_bust(x, y, k=1.0, rim="#a8c8e8", **hk):
    g = uid("uz")
    sk = hk.pop("sk", SK_UTZ)
    hs = head(rim=rim, sk=sk, headwrap=False, earring=False, lips=("#5a2a2a", "#6a3434"), iris="#140a06", brow_w=1.25,
              smile=hk.get("smile", -0.3), lids=hk.get("lids", 0.55), look=hk.get("look", -0.6), turn=hk.get("turn", -0.15))
    # severe pulled-back hair with a high bun
    hs += ('<path d="M0,-134 C-60,-136 -86,-100 -84,-46 C-80,-70 -60,-104 0,-108 C60,-104 80,-70 84,-46 C86,-100 60,-136 0,-134 Z" fill="#06050a"/>'
           '<ellipse cx="0" cy="-168" rx="56" ry="40" fill="#06050a"/><path d="M-40,-176 Q0,-200 40,-176" stroke="#3a4660" stroke-width="3" fill="none"/>'
           '<path d="M-50,-160 L50,-150" stroke="#c8b070" stroke-width="5"/>')
    hs += '<path d="M-58,-46 L-12,-52 M58,-46 L12,-52" stroke="#120806" stroke-width="5"/>'  # straight, hard brows
    body = huipil_body(g, sk, rim, cloth=("#5a6070", "#c8ccd4", "#eef0f4"), emb=("#2a3a6a", "#4a5a8a", "#8a96b0"))
    body += '<path d="M-300,226 C-220,196 -170,186 -130,182 L-90,140 L-60,120 L60,120 L90,140 L130,182 C170,186 220,196 300,226" fill="#1a2440" opacity="0.0"/>'
    return bust_frame(body, hs, x, y, k)


def lencho_bust(x, y, k=1.0, rim="#9fc2e8", **hk):
    return tomas_bust(x, y, k, rim=rim, **hk)


def candelaria_bust(x, y, k=1.0, rim="#9fc2e8", **hk):
    return lupe_bust(x, y, k, rim=rim, **hk)


# ------------------------------------------------------------------ full figures
def xtabay_full(x, y, h=900, facing=1, back=False, comb=True, rim="#bfe0ff", op=1.0, hair_len=1.0):
    """Full figure, feet at (x,y). back=True: seen from behind, hair down to the ankles hiding the body."""
    k = h / 900.0; g = uid("xf")
    s = f'<g transform="translate({x},{y}) scale({k*facing},{k})" opacity="{op}">'
    s += f'<defs>{grad_lin(g, [(0, "#9aa4b0", 1), (0.5, "#eef2f4", 1), (1, "#ffffff", 1)], -140, 0, 140, 0)}</defs>'
    s += '<ellipse cx="0" cy="-420" rx="300" ry="560" fill="url(#moonglow)" opacity="0.35"/>'
    # skirt / fustán with lace hem
    s += f'<path d="M-90,-520 C-110,-360 -140,-160 -170,0 L170,0 C140,-160 110,-360 90,-520 Z" fill="url(#{g})"/>'
    s += '<path d="M-170,0 L170,0 L166,-36 L-166,-36 Z" fill="#f8f8f4"/>'
    for i in range(17):
        s += f'<circle cx="{-160+i*20}" cy="-18" r="5" fill="#c8283a" opacity="0.8"/><circle cx="{-150+i*20}" cy="-24" r="4" fill="#2e8a5a" opacity="0.8"/>'
    # torso huipil
    s += f'<path d="M-110,-800 C-140,-700 -130,-600 -110,-500 L110,-500 C130,-600 140,-700 110,-800 C60,-830 -60,-830 -110,-800 Z" fill="url(#{g})"/>'
    # arms
    if comb and not back:
        s += '<path d="M90,-780 C150,-760 170,-860 120,-950" stroke="#e8ecf0" stroke-width="44" fill="none" stroke-linecap="round"/>'
        s += '<ellipse cx="118" cy="-960" rx="20" ry="24" fill="#b58466"/>'
    elif not back:
        s += '<path d="M-110,-780 C-140,-680 -140,-600 -120,-520" stroke="#dfe4e8" stroke-width="40" fill="none" stroke-linecap="round"/>'
    if not back:
        s += '<path d="M-60,-800 L-60,-730 L60,-730 L60,-800" fill="none" stroke="#c8283a" stroke-width="10" stroke-dasharray="10 8"/>'
        s += '<path d="M-24,-830 C-24,-860 24,-860 24,-830 Z" fill="#9a6a50"/>'  # neck
        # face
        s += '<ellipse cx="0" cy="-905" rx="44" ry="58" fill="#b58466"/><ellipse cx="10" cy="-900" rx="30" ry="42" fill="#d2a084" opacity="0.6"/>'
        s += '<ellipse cx="-16" cy="-910" rx="9" ry="6" fill="#050203"/><ellipse cx="16" cy="-910" rx="9" ry="6" fill="#050203"/>'
        s += '<path d="M-12,-872 Q0,-866 12,-872" stroke="#6a1e22" stroke-width="5" fill="none"/>'
    # hair
    hl = 860 * hair_len
    if back:
        s += (f'<path d="M0,-975 C-70,-975 -90,-920 -88,-860 C-110,-600 -140,{-975+hl*0.7:.0f} -150,{-975+hl:.0f} '
              f'C-60,{-975+hl+30:.0f} 60,{-975+hl+30:.0f} 150,{-975+hl:.0f} C140,{-975+hl*0.7:.0f} 110,-600 88,-860 C90,-920 70,-975 0,-975 Z" fill="{HAIR}"/>')
        if comb:
            s += '<path d="M84,-800 C118,-780 128,-760 126,-730" stroke="#e8ecf0" stroke-width="40" fill="none" stroke-linecap="round"/>'
            s += '<path d="M126,-730 C132,-690 110,-660 82,-668" stroke="#a87458" stroke-width="24" fill="none" stroke-linecap="round"/>'
            s += '<path d="M126,-730 C132,-690 110,-660 82,-668" stroke="#d8a888" stroke-width="5" fill="none" opacity="0.6"/>'
            s += '<ellipse cx="78" cy="-668" rx="20" ry="15" fill="#b58466"/>'
            for i in range(7):
                s += f'<path d="M{54+i*5},-668 l-22,34" stroke="#e8dcc0" stroke-width="3"/>'
    else:
        s += ('<path d="M0,-968 C-60,-968 -60,-930 -48,-880 C-60,-700 -110,-400 -120,-140 L-80,-140 C-70,-400 -40,-700 -36,-880 C-30,-930 -10,-950 0,-950 '
              'C10,-950 30,-930 36,-880 C40,-700 70,-400 80,-140 L120,-140 C110,-400 60,-700 48,-880 C60,-930 60,-968 0,-968 Z" fill="' + HAIR + '"/>')
    r = random.Random(9)
    for i in range(40):
        xx = r.uniform(-80, 80)
        s += f'<path d="M{xx*0.6:.0f},-960 C{xx:.0f},-700 {xx*1.4:.0f},-400 {xx*1.7:.0f},{-975+hl-r.uniform(0,40):.0f}" stroke="{HAIR_HI}" stroke-width="{r.uniform(1.5,3):.1f}" fill="none" opacity="{r.uniform(0.15,0.45):.2f}"/>' if back else ""
    # moon rim
    s += f'<path d="M-90,-860 C-110,-600 -140,-300 -170,0" stroke="{rim}" stroke-width="6" fill="none" opacity="0.55" filter="url(#blur1)"/>'
    s += '</g>'
    return s


def man_walk(x, y, h=640, facing=1, lantern=True, sway=0, color="#04060a", rim="#9fc2e8", hat=True, drunk=False):
    k = h / 640.0
    s = f'<g transform="translate({x},{y}) scale({k*facing},{k}) rotate({-6 if drunk else 0})">'
    s += f'<path d="M-30,-400 C-60,-300 -64,-200 -40,-180 L-60,0 L-30,0 L0,-170 L30,0 L60,0 L40,-190 C60,-260 60,-340 30,-400 Z" fill="{color}"/>'
    s += f'<path d="M-50,-520 C-80,-500 -90,-430 -60,-380 L60,-380 C90,-430 80,-500 50,-520 Z" fill="{color}"/>'
    s += f'<circle cx="0" cy="-560" r="40" fill="{color}"/>'
    if hat:
        s += f'<ellipse cx="0" cy="-582" rx="110" ry="18" fill="{color}"/><path d="M-40,-585 C-40,-640 40,-640 40,-585 Z" fill="{color}"/>'
    s += f'<path d="M50,-500 C90,-440 100,-380 90,-330" stroke="{color}" stroke-width="30" fill="none" stroke-linecap="round"/>'
    s += f'<path d="M-50,-500 C-80,-440 -86,-380 -76,-320" stroke="{color}" stroke-width="30" fill="none" stroke-linecap="round"/>'
    if lantern:
        s += '<path d="M90,-330 L90,-300" stroke="#222" stroke-width="4"/><rect x="74" y="-300" width="32" height="44" rx="4" fill="#ffc870"/>'
        s += '<circle cx="90" cy="-278" r="120" fill="url(#warmglow)" opacity="0.7"/>'
    s += f'<path d="M-50,-520 C-80,-500 -90,-430 -60,-380 M-30,-400 C-60,-300 -64,-200 -40,-180 L-60,0" stroke="{rim}" stroke-width="4" fill="none" opacity="0.5"/>'
    s += f'<path d="M-110,-582 L110,-582" stroke="{rim}" stroke-width="3" opacity="0.5"/>'
    s += '</g>'
    return s
