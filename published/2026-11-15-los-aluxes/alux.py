"""The alux: knee-high old man of the monte (bearded, wrinkled, palm hat, white cotton clothes, sandals,
amber night eyes). Also the clay (barro) version made by the jmen. Hand-drawn paths in local coords."""
import math, random
from base_chars import uid, grad_lin, grad_rad

SK_ALUX = dict(base="#6e4a32", light="#946646", hi="#b8865e", shadow="#45291a", deep="#22130b")
SK_CLAY = dict(base="#8a5a3a", light="#a8724c", hi="#c99068", shadow="#5a3622", deep="#2e1a10")
BEARD = ("#b8b4ac", "#e8e4dc", "#6e6a64")
CLAY_BEARD = ("#7a4e32", "#a87050", "#4a2c1a")


def beard_strands(seed, col_hi, col_dk, n=60, y0=40, y1=230, w=95):
    r = random.Random(seed); s = ""
    for _ in range(n):
        x = r.uniform(-w, w); y = r.uniform(y0, y0 + 30)
        L = (y1 - y0) * (1 - (abs(x) / w) ** 2 * 0.6) * r.uniform(0.7, 1.0)
        bend = r.uniform(-18, 18)
        s += (f'<path d="M{x:.0f},{y:.0f} C{x+bend:.0f},{y+L*0.4:.0f} {x*0.75-bend:.0f},{y+L*0.75:.0f} {x*0.55+bend*0.5:.0f},{y+L:.0f}" '
              f'stroke="{r.choice((col_hi, col_dk))}" stroke-width="{r.uniform(1.5,3.8):.1f}" fill="none" opacity="{r.uniform(0.45,0.95):.2f}" stroke-linecap="round"/>')
    return s


def alux_head(mood="grin", eyes="glow", rim="#9fc2e8", clay=False, hat=True, look=0.0, seed=3):
    """Head centred at (0,0); face ~260 tall. mood: grin | calm | scare. eyes: glow | dark | none(clay closed)."""
    g = uid("ax"); sk = SK_CLAY if clay else SK_ALUX; bd = CLAY_BEARD if clay else BEARD
    r = random.Random(seed)
    s = "<defs>" + grad_lin(g + "f", [(0, sk["shadow"], 1), (0.45, sk["base"], 1), (0.8, sk["light"], 1), (1, sk["base"], 1)], -110, 0, 110, 0)
    s += grad_lin(g + "b", [(0, bd[2], 1), (0.5, bd[0], 1), (1, bd[1], 1)], -100, 0, 100, 0)
    s += grad_rad(g + "e", [(0, "#fff6c0", 1), (0.35, "#ffc23a", 1), (0.7, "#c86a10", 0.8), (1, "#c86a10", 0)])
    s += grad_lin(g + "h", [(0, "#5e4a26", 1), (0.5, "#b0925a", 1), (1, "#d8be84", 1)], -300, 0, 300, 0) + "</defs>"
    # big ears
    for sx in (-1, 1):
        s += (f'<path d="M{sx*96},-20 C{sx*150},-60 {sx*160},10 {sx*130},50 C{sx*118},66 {sx*100},60 {sx*94},40 Z" fill="{sk["base"]}"/>'
              f'<path d="M{sx*104},-8 C{sx*138},-30 {sx*140},14 {sx*120},38" stroke="{sk["deep"]}" stroke-width="5" fill="none" opacity="0.7"/>')
    # face: broad, lumpy, old
    face = ("M-100,-70 C-112,-10 -108,40 -88,80 C-70,112 -36,130 0,132 C36,130 70,112 88,80 C108,40 112,-10 100,-70 "
            "C90,-120 50,-142 0,-142 C-50,-142 -90,-120 -100,-70 Z")
    s += f'<path d="{face}" fill="url(#{g}f)"/>'
    # cheeks / brow lumps shading
    s += f'<ellipse cx="-56" cy="34" rx="30" ry="22" fill="{sk["hi"]}" opacity="0.35" filter="url(#blur2)"/><ellipse cx="60" cy="34" rx="30" ry="22" fill="{sk["hi"]}" opacity="0.45" filter="url(#blur2)"/>'
    s += f'<path d="M-92,-40 C-60,-62 -24,-58 -6,-34 C14,-58 56,-64 94,-40 C70,-46 40,-40 10,-14 L-10,-14 C-36,-40 -66,-46 -92,-40 Z" fill="{sk["shadow"]}" opacity="0.9"/>'
    # wrinkles on forehead
    for i, y in enumerate((-92, -78, -64)):
        s += f'<path d="M{-60+i*6},{y} C-30,{y-10} 30,{y-10} {60-i*6},{y}" stroke="{sk["deep"]}" stroke-width="3" fill="none" opacity="0.55"/>'
    # eye sockets
    lx = look * 8
    for sx in (-1, 1):
        cx = sx * 42 + lx
        s += f'<ellipse cx="{cx:.0f}" cy="-16" rx="26" ry="17" fill="{sk["deep"]}"/>'
        if eyes == "glow":
            big = 1.35 if mood == "scare" else 1.0
            s += f'<circle cx="{cx:.0f}" cy="-16" r="{34*big:.0f}" fill="url(#{g}e)" opacity="0.9"/>'
            s += f'<ellipse cx="{cx:.0f}" cy="-16" rx="{13*big:.0f}" ry="{10*big:.0f}" fill="#ffd25a"/><ellipse cx="{cx:.0f}" cy="-16" rx="3.5" ry="{9*big:.0f}" fill="#1a0800"/>'
            s += f'<circle cx="{cx+4:.0f}" cy="-20" r="2.5" fill="#fff"/>'
        elif eyes == "dark":
            s += f'<ellipse cx="{cx:.0f}" cy="-16" rx="12" ry="9" fill="#0a0604"/><circle cx="{cx+4:.0f}" cy="-19" r="2" fill="#d8d0c0" opacity="0.6"/>'
        else:  # clay: carved slits
            s += f'<path d="M{cx-14:.0f},-16 Q{cx:.0f},-10 {cx+14:.0f},-16" stroke="{sk["deep"]}" stroke-width="5" fill="none"/>'
        # crow's feet
        for k in range(3):
            s += f'<path d="M{cx+sx*24:.0f},{-20+k*7} l{sx*16},{-6+k*8}" stroke="{sk["deep"]}" stroke-width="2.4" opacity="0.6"/>'
        # bags under eyes
        s += f'<path d="M{cx-22:.0f},0 Q{cx:.0f},12 {cx+22:.0f},0" stroke="{sk["deep"]}" stroke-width="3" fill="none" opacity="0.5"/>'
    # bushy white brows
    for sx in (-1, 1):
        for k in range(14):
            x0 = sx * (14 + k * 5.5); y0 = -40 - math.sin(k / 13 * math.pi) * 10
            s += f'<path d="M{x0:.0f},{y0:.0f} l{sx*r.uniform(10,22):.0f},{r.uniform(-14,-2) if mood!="scare" else r.uniform(-4,8):.0f}" stroke="{bd[1]}" stroke-width="{r.uniform(2,4):.1f}" stroke-linecap="round" opacity="0.9"/>'
    # big hooked nose
    s += (f'<path d="M-6,-20 C-14,10 -34,34 -30,52 C-26,66 -8,66 0,60 C8,66 26,66 30,52 C34,34 14,10 6,-20 Z" fill="{sk["light"]}"/>'
          f'<path d="M-30,52 C-26,66 -8,66 0,60" stroke="{sk["deep"]}" stroke-width="4" fill="none"/><path d="M30,52 C26,66 8,66 0,60" stroke="{sk["deep"]}" stroke-width="4" fill="none"/>'
          f'<ellipse cx="6" cy="20" rx="6" ry="16" fill="{sk["hi"]}" opacity="0.6"/>')
    s += f'<path d="M-30,52 C-50,58 -60,80 -56,100 M30,52 C50,58 60,80 56,100" stroke="{sk["deep"]}" stroke-width="4" fill="none" opacity="0.6"/>'
    # beard + moustache
    s += f'<path d="M-96,40 C-100,120 -70,210 -10,250 L10,250 C70,210 100,120 96,40 C80,90 50,110 0,108 C-50,110 -80,90 -96,40 Z" fill="url(#{g}b)"/>'
    s += beard_strands(seed, bd[1], bd[2], 70)
    # mouth
    if mood == "scare":
        s += '<path d="M-42,84 C-30,70 30,70 42,84 C40,130 20,150 0,152 C-20,150 -40,130 -42,84 Z" fill="#1a0404"/>'
        for i in range(7):
            x = -32 + i * 10.6
            s += f'<path d="M{x:.0f},{80+abs(x)*0.1:.0f} l5,14 l5,-14 Z" fill="#e8dcc0"/>'
            s += f'<path d="M{x:.0f},{142-abs(x)*0.3:.0f} l5,-12 l5,12 Z" fill="#d8ccb0"/>'
    elif mood == "grin":
        s += '<path d="M-44,80 C-24,104 24,104 44,80 C30,96 -30,96 -44,80 Z" fill="#1a0604"/>'
        s += '<path d="M-20,88 l6,8 l6,-8 Z M10,89 l6,8 l6,-8 Z" fill="#e0d4b8"/>'
        s += f'<path d="M-44,80 C-52,74 -54,68 -50,62 M44,80 C52,74 54,68 50,62" stroke="{sk["deep"]}" stroke-width="3" fill="none"/>'
    else:
        s += '<path d="M-28,86 C-10,92 10,92 28,86" stroke="#1a0604" stroke-width="5" fill="none"/>'
    # moustache over the mouth
    s += (f'<path d="M0,66 C-20,62 -46,66 -62,92 C-44,84 -24,80 -2,78 Z M0,66 C20,62 46,66 62,92 C44,84 24,80 2,78 Z" fill="{bd[0]}"/>'
          f'<path d="M-6,70 C-24,70 -40,76 -54,88 M6,70 C24,70 40,76 54,88" stroke="{bd[1]}" stroke-width="2" fill="none"/>')
    if clay:  # cracks and finger marks in the clay
        for _ in range(9):
            x, y = r.uniform(-80, 80), r.uniform(-120, 100)
            s += f'<path d="M{x:.0f},{y:.0f} l{r.uniform(-14,14):.0f},{r.uniform(6,18):.0f} l{r.uniform(-10,10):.0f},{r.uniform(6,14):.0f}" stroke="{sk["deep"]}" stroke-width="2" fill="none" opacity="0.7"/>'
    # rim light along the right cheek/beard
    if rim:
        s += f'<path d="M100,-70 C112,-10 108,40 88,80 C80,140 60,200 12,248" stroke="{rim}" stroke-width="6" fill="none" opacity="0.6" filter="url(#blur1)"/>'
    if hat:  # wide palm hat, pulled low
        s += (f'<path d="M-82,-104 C-86,-180 -50,-214 0,-216 C50,-214 86,-180 82,-104 Z" fill="url(#{g}h)"/>'
              f'<path d="M-84,-118 C-30,-106 30,-106 84,-118 L84,-102 C30,-90 -30,-90 -84,-102 Z" fill="{"#5a3622" if clay else "#3a2416"}"/>'
              f'<path d="M-280,-82 C-220,-130 -110,-140 0,-140 C110,-140 220,-130 280,-82 C220,-62 110,-56 0,-58 C-110,-56 -220,-62 -280,-82 Z" fill="url(#{g}h)"/>'
              f'<path d="M-280,-82 C-220,-62 -110,-56 0,-58 C110,-56 220,-62 280,-82 C220,-70 110,-66 0,-68 C-110,-66 -220,-70 -280,-82 Z" fill="#2a1e10" opacity="0.8"/>')
        for i in range(30):
            a = -270 + i * 18.6
            s += f'<path d="M{a:.0f},{-86+abs(a)*0.03:.0f} L{a*0.28:.0f},-136" stroke="#4a3818" stroke-width="1.8" opacity="0.4"/>'
        for i in range(8):
            s += f'<path d="M{-70+i*20},-110 L{-50+i*14},-200" stroke="#4a3818" stroke-width="1.6" opacity="0.35"/>'
        s += '<path d="M-150,-70 l-8,18 M-90,-62 l-4,20 M140,-70 l8,18 M200,-76 l10,16" stroke="#6a5428" stroke-width="2"/>'  # frayed edge
        # brim shadow over the eyes
        s += f'<path d="M-104,-60 C-60,-44 60,-44 104,-60 L100,-30 C60,-20 -60,-20 -100,-30 Z" fill="#000" opacity="0.35" filter="url(#blur2)"/>'
        if rim:
            s += f'<path d="M0,-140 C110,-140 220,-130 280,-82" stroke="{rim}" stroke-width="4" fill="none" opacity="0.7"/>'
    return s


def alux_full(x, y, h=420, pose="stand", rim="#9fc2e8", eyes="glow", clay=False, mood="grin", facing=1, sling=False, trompo=False):
    """Full figure, feet at (x,y), total height h. pose: stand | sit (legs dangling) | walk."""
    k = h / 1000.0; g = uid("af"); sk = SK_CLAY if clay else SK_ALUX
    cloth = ("#8a8676", "#d8d2c0", "#f2ecdc") if not clay else ("#6a4228", "#9a6a46", "#b8865e")
    s = f'<g transform="translate({x},{y}) scale({k*facing},{k})">'
    s += "<defs>" + grad_lin(g + "c", [(0, cloth[0], 1), (0.55, cloth[1], 1), (1, cloth[2], 1)], -200, 0, 200, 0) + "</defs>"
    leg = sk["shadow"]
    if pose == "sit":
        # legs dangling forward/down from a seat at y=-420
        for sx, sw in ((-1, 6), (1, -8)):
            s += f'<path d="M{sx*50},-330 C{sx*60},-260 {sx*70+sw},-200 {sx*64+sw},-120" stroke="url(#{g}c)" stroke-width="64" fill="none" stroke-linecap="round"/>'
            s += f'<path d="M{sx*64+sw},-130 L{sx*62+sw},-40" stroke="{leg}" stroke-width="40" stroke-linecap="round"/>'
            s += f'<path d="M{sx*62+sw-30},-30 C{sx*62+sw-30},-60 {sx*62+sw+50},-60 {sx*62+sw+56},-26 Z" fill="#3a2414"/>'
        top = -330
    else:
        st = 30 if pose == "walk" else 0
        for sx, sw in ((-1, -st), (1, st)):
            s += f'<path d="M{sx*48},-320 L{sx*52+sw},-120" stroke="url(#{g}c)" stroke-width="78" stroke-linecap="round"/>'
            s += f'<path d="M{sx*52+sw},-130 L{sx*52+sw},-30" stroke="{leg}" stroke-width="44" stroke-linecap="round"/>'
            s += f'<path d="M{sx*52+sw-34},-6 C{sx*52+sw-34},-36 {sx*52+sw+50},-40 {sx*52+sw+60},-6 Z" fill="#3a2414"/>'
            s += f'<path d="M{sx*52+sw-20},-30 l40,-6" stroke="#6a4a2a" stroke-width="5"/>'  # sandal strap
        top = -320
    # torso: loose white cotton shirt with folds
    s += (f'<path d="M-120,{top-260} C-150,{top-200} -150,{top-60} -130,{top+20} L130,{top+20} C150,{top-60} 150,{top-200} 120,{top-260} '
          f'C80,{top-290} -80,{top-290} -120,{top-260} Z" fill="url(#{g}c)"/>')
    for d in (-70, -20, 40, 90):
        s += f'<path d="M{d},{top-250} C{d+10},{top-160} {d-10},{top-80} {d+6},{top+10}" stroke="{cloth[0]}" stroke-width="5" fill="none" opacity="0.5"/>'
    s += f'<path d="M-130,{top+10} L130,{top+10}" stroke="#5a3a20" stroke-width="14"/>'  # sash
    # little bag (sabucán) on a strap
    s += f'<path d="M-90,{top-250} L110,{top-40}" stroke="#6a4a2a" stroke-width="8"/><path d="M80,{top-60} C70,{top+40} 170,{top+40} 160,{top-60} Z" fill="#8a6a3a"/>'
    # arms
    s += f'<path d="M-118,{top-240} C-170,{top-170} -180,{top-90} -150,{top-30}" stroke="url(#{g}c)" stroke-width="52" fill="none" stroke-linecap="round"/>'
    s += f'<circle cx="-150" cy="{top-20}" r="26" fill="{sk["base"]}"/>'
    if sling:  # forked slingshot raised in the right hand
        s += f'<path d="M118,{top-240} C170,{top-300} 190,{top-380} 180,{top-440}" stroke="url(#{g}c)" stroke-width="50" fill="none" stroke-linecap="round"/>'
        s += f'<circle cx="180" cy="{top-450}" r="26" fill="{sk["base"]}"/>'
        s += f'<path d="M180,{top-460} L180,{top-540} M180,{top-540} L150,{top-600} M180,{top-540} L210,{top-600}" stroke="#4a2e18" stroke-width="12" stroke-linecap="round"/>'
        s += f'<path d="M150,{top-600} C150,{top-560} 210,{top-560} 210,{top-600}" stroke="#2a2a2a" stroke-width="4" fill="none"/>'
    else:
        s += f'<path d="M118,{top-240} C170,{top-170} 180,{top-90} 150,{top-30}" stroke="url(#{g}c)" stroke-width="52" fill="none" stroke-linecap="round"/>'
        s += f'<circle cx="150" cy="{top-20}" r="26" fill="{sk["base"]}"/>'
        if trompo:
            s += f'<g transform="translate(160,{top+10})">{trompo_svg(0.5)}</g>'
    s += f'<g transform="translate(0,{top-430}) scale(1.05)">{alux_head(mood, eyes, rim, clay)}</g>'
    if rim:
        s += f'<path d="M120,{top-260} C150,{top-200} 150,{top-60} 130,{top+20}" stroke="{rim}" stroke-width="6" fill="none" opacity="0.55"/>'
    s += '</g>'
    return s


def trompo_svg(k=1.0, worn=False):
    """Wooden spinning top, centre at its widest point; ~200 tall at k=1."""
    g = uid("tp")
    paint = ("#a8282a", "#2a5a9a", "#e8b030") if not worn else ("#6a3a2a", "#3a4a5a", "#8a7040")
    s = f'<defs>{grad_lin(g, [(0, "#4a2a14", 1), (0.5, "#c8945a", 1), (1, "#6a4020", 1)], -80, 0, 80, 0)}</defs>'
    s += f'<g transform="scale({k})">'
    s += f'<path d="M-80,-20 C-80,-80 80,-80 80,-20 C80,30 20,90 0,120 C-20,90 -80,30 -80,-20 Z" fill="url(#{g})"/>'
    for i, c in enumerate(paint):
        y = -40 + i * 26
        w = 80 - i * 14
        s += f'<path d="M{-w},{y} C{-w*0.5},{y+12} {w*0.5},{y+12} {w},{y}" stroke="{c}" stroke-width="9" fill="none" opacity="{0.55 if worn else 0.95}"/>'
    s += '<path d="M0,-70 L0,-110" stroke="#5a3418" stroke-width="16" stroke-linecap="round"/>'
    s += '<path d="M0,118 L0,150" stroke="#9a9a9a" stroke-width="7"/>'
    if worn:
        r = random.Random(4)
        for _ in range(14):
            x = r.uniform(-60, 60); y = r.uniform(-50, 40)
            s += f'<path d="M{x:.0f},{y:.0f} l{r.uniform(6,16):.0f},{r.uniform(-3,3):.0f}" stroke="#d8b88a" stroke-width="3" opacity="0.7"/>'
    s += '</g>'
    return s
