"""SVG illustration helpers for the channel's look: moonlit silhouette / shadow-theatre style.
Canvas: 2400x1350 (16:9, 1.25x the 1080p frame so the camera can move).

    import sys; sys.path.insert(0, '/home/claude/pipeline'); from art import *
    open('art/s01_bg.svg','w').write(svg(sky('#0a1322','#22394a'), stars(160, 1), moon(1750, 300, 105),
                                          ridge(820, 120, '#101c2a', 3), water(900, 1350), reflection(1750, 905, 1350)))
    then: node /home/claude/pipeline/render_svg.js art/*.svg

All functions return SVG fragment strings. Colours are CSS strings. Seeds make shapes repeatable.
"""
import math, random

W, H = 2400, 1350

DEFS = '''<defs>
<filter id="blur1" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3"/></filter>
<filter id="blur2" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="10"/></filter>
<filter id="blur3" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="28"/></filter>
<filter id="blur4" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="70"/></filter>
<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="14" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="ghost" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="paper" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="4" result="n"/><feColorMatrix in="n" type="saturate" values="0"/><feComponentTransfer><feFuncA type="table" tableValues="0 0.08"/></feComponentTransfer><feComposite in2="SourceGraphic" operator="in"/></filter>
<radialGradient id="moonglow"><stop offset="0" stop-color="#eaf2ff" stop-opacity="0.55"/><stop offset="0.35" stop-color="#9fb8d6" stop-opacity="0.18"/><stop offset="1" stop-color="#9fb8d6" stop-opacity="0"/></radialGradient>
<radialGradient id="warmglow"><stop offset="0" stop-color="#ffd27a" stop-opacity="0.9"/><stop offset="0.3" stop-color="#ff9a3c" stop-opacity="0.35"/><stop offset="1" stop-color="#ff7a20" stop-opacity="0"/></radialGradient>
<radialGradient id="redglow"><stop offset="0" stop-color="#ff3b2f" stop-opacity="0.95"/><stop offset="0.3" stop-color="#c0141a" stop-opacity="0.4"/><stop offset="1" stop-color="#800000" stop-opacity="0"/></radialGradient>
<radialGradient id="whiteglow"><stop offset="0" stop-color="#ffffff" stop-opacity="0.85"/><stop offset="0.4" stop-color="#cfe3ff" stop-opacity="0.25"/><stop offset="1" stop-color="#cfe3ff" stop-opacity="0"/></radialGradient>
<linearGradient id="fadeDown" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="1"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<mask id="fadeBottom" maskContentUnits="objectBoundingBox"><rect width="1" height="1" fill="url(#fadeDown)"/></mask>
</defs>'''


def svg(*parts, defs="", w=W, h=H):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{DEFS}{defs}{"".join(parts)}</svg>'


def _gid(prefix="g"):
    _gid.n = getattr(_gid, "n", 0) + 1
    return f"{prefix}{_gid.n}"


def sky(top="#0a1322", bottom="#22394a", mid=None, y0=0, y1=H):
    g = _gid("sky"); stops = f'<stop offset="0" stop-color="{top}"/>' + (f'<stop offset="0.55" stop-color="{mid}"/>' if mid else "") + f'<stop offset="1" stop-color="{bottom}"/>'
    return f'<defs><linearGradient id="{g}" x1="0" y1="0" x2="0" y2="1">{stops}</linearGradient></defs><rect x="0" y="{y0}" width="{W}" height="{y1-y0}" fill="url(#{g})"/>'


def stars(n=150, seed=1, ymax=800, color="#dfe8ff"):
    r = random.Random(seed); out = []
    for _ in range(n):
        x, y = r.uniform(0, W), r.uniform(0, ymax) ** 1.0
        s = r.choice([0.8, 1, 1.2, 1.6, 2.2]); o = r.uniform(0.25, 0.9) * (1 - y / ymax * 0.6)
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{s}" fill="{color}" opacity="{o:.2f}"/>')
    return "".join(out)


def moon(cx=1750, cy=300, r=100, color="#f2f0e4", halo=4.5, phase=None):
    """Full moon with halo. phase: None (full) or 0..1 shadow offset for a crescent."""
    s = f'<circle cx="{cx}" cy="{cy}" r="{r*halo}" fill="url(#moonglow)"/>'
    s += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}"/>'
    rr = random.Random(int(cx + cy))
    for _ in range(7):
        a, d = rr.uniform(0, 6.28), rr.uniform(0, r * 0.7)
        s += f'<circle cx="{cx+math.cos(a)*d:.0f}" cy="{cy+math.sin(a)*d:.0f}" r="{rr.uniform(r*0.06, r*0.2):.0f}" fill="#c9c6b8" opacity="0.35"/>'
    if phase is not None:
        s += f'<circle cx="{cx + r*2*phase}" cy="{cy - r*0.1}" r="{r*1.02}" fill="#0a1322"/>'
    return s


def ridge(y=820, amp=120, color="#101c2a", seed=3, rough=0.55, step=40, y_bottom=H):
    r = random.Random(seed); pts = []; n = W // step + 2
    vals = [0.0] * n; scale = 1.0; k = n
    while k > 1:
        for i in range(0, n, k):
            vals[i] += r.uniform(-1, 1) * scale
        k //= 2; scale *= rough
    # smooth interpolate
    for i in range(n):
        x = i * step; v = vals[i] if vals[i] else 0
        pts.append(f"{x},{y - amp * (0.5 + 0.5 * math.sin(i * 0.21 + seed)) * 0.6 - amp * v * 0.5:.0f}")
    return f'<polygon points="0,{y_bottom} {" ".join(pts)} {W},{y_bottom}" fill="{color}"/>'


def water(y0=900, y1=H, top="#1b2e3d", bottom="#070c14"):
    g = _gid("wat")
    return f'<defs><linearGradient id="{g}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{top}"/><stop offset="1" stop-color="{bottom}"/></linearGradient></defs><rect x="0" y="{y0}" width="{W}" height="{y1-y0}" fill="url(#{g})"/>'


def reflection(cx=1750, y0=905, y1=H, color="#e8eef5", width=200, seed=5):
    r = random.Random(seed); out = []
    y = y0
    while y < y1:
        wv = width * (0.4 + 0.8 * r.random()) * (1 + (y - y0) / (y1 - y0))
        o = 0.55 * (1 - (y - y0) / (y1 - y0)) ** 1.3 + 0.05
        out.append(f'<rect x="{cx - wv/2 + r.uniform(-30, 30):.0f}" y="{y:.0f}" width="{wv:.0f}" height="{r.uniform(2, 6):.0f}" rx="3" fill="{color}" opacity="{o:.2f}"/>')
        y += r.uniform(6, 16)
    return f'<g filter="url(#blur1)">{"".join(out)}</g>'


def reeds(x0=0, x1=W, y=1000, seed=7, color="#05080d", n=120, hmax=180):
    r = random.Random(seed); out = []
    for _ in range(n):
        x = r.uniform(x0, x1); h = r.uniform(hmax * 0.3, hmax); bend = r.uniform(-40, 40)
        out.append(f'<path d="M{x:.0f},{y} Q{x+bend*0.3:.0f},{y-h*0.6:.0f} {x+bend:.0f},{y-h:.0f}" stroke="{color}" stroke-width="{r.uniform(2,5):.1f}" fill="none" stroke-linecap="round"/>')
        if r.random() < 0.2:
            out.append(f'<ellipse cx="{x+bend:.0f}" cy="{y-h:.0f}" rx="5" ry="18" fill="{color}" transform="rotate({bend*0.4:.0f} {x+bend:.0f} {y-h:.0f})"/>')
    return "".join(out)


def tree(x=300, y=1100, size=600, seed=11, color="#03060a", kind="bare", lean=0.0):
    """Recursive silhouette tree. kind: 'bare' (twisted branches), 'willow' (weeping strands), 'ahuehuete' (wide trunk)."""
    r = random.Random(seed); out = []
    def branch(x0, y0, ang, length, width, depth):
        x1 = x0 + math.cos(ang) * length; y1 = y0 - math.sin(ang) * length
        cx = (x0 + x1) / 2 + r.uniform(-length, length) * 0.18; cy = (y0 + y1) / 2 + r.uniform(-length, length) * 0.18
        out.append(f'<path d="M{x0:.0f},{y0:.0f} Q{cx:.0f},{cy:.0f} {x1:.0f},{y1:.0f}" stroke="{color}" stroke-width="{width:.1f}" fill="none" stroke-linecap="round"/>')
        if depth == 0 or length < 12:
            if kind == "willow":
                for _ in range(3):
                    L = r.uniform(size * 0.25, size * 0.6); sx = x1 + r.uniform(-20, 20)
                    out.append(f'<path d="M{x1:.0f},{y1:.0f} Q{sx+r.uniform(-30,30):.0f},{y1+L*0.5:.0f} {sx+r.uniform(-50,50):.0f},{y1+L:.0f}" stroke="{color}" stroke-width="{r.uniform(1.5,3.5):.1f}" fill="none" opacity="{r.uniform(0.6,1):.2f}"/>')
            return
        nb = 2 if r.random() < 0.7 else 3
        for i in range(nb):
            da = r.uniform(0.25, 0.65) * (1 if i % 2 == 0 else -1) + (r.uniform(-0.2, 0.2) if kind == "bare" else 0)
            branch(x1, y1, ang + da, length * r.uniform(0.62, 0.8), max(1.2, width * 0.66), depth - 1)
    base_w = size * (0.09 if kind != "ahuehuete" else 0.16)
    out.append(f'<path d="M{x-base_w*1.4:.0f},{y} Q{x-base_w*0.5:.0f},{y-size*0.15:.0f} {x-base_w*0.4:.0f},{y-size*0.3:.0f} L{x+base_w*0.4:.0f},{y-size*0.3:.0f} Q{x+base_w*0.5:.0f},{y-size*0.15:.0f} {x+base_w*1.5:.0f},{y} Z" fill="{color}"/>')
    branch(x, y - size * 0.25, math.pi / 2 + lean, size * 0.32, base_w * 0.85, 7 if kind != "willow" else 6)
    return "".join(out)


def glow(x, y, r=120, kind="warm", opacity=1.0):
    """Soft light pool: kind = warm | red | white | moon."""
    gid = {"warm": "warmglow", "red": "redglow", "white": "whiteglow", "moon": "moonglow"}[kind]
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="url(#{gid})" opacity="{opacity}"/>'


def candle(x, y, h=60, w=16, wax="#e8dcc0"):
    return (glow(x, y - h - 10, h * 2.4, "warm", 0.9) +
            f'<rect x="{x-w/2}" y="{y-h}" width="{w}" height="{h}" rx="3" fill="{wax}"/>'
            f'<path d="M{x},{y-h-34} Q{x+9},{y-h-12} {x},{y-h-2} Q{x-9},{y-h-12} {x},{y-h-34} Z" fill="#ffdf8a"/>'
            f'<path d="M{x},{y-h-22} Q{x+4},{y-h-10} {x},{y-h-4} Q{x-4},{y-h-10} {x},{y-h-22} Z" fill="#fff6d8"/>')


def lamp(x, y, h=420, color="#05070a", lit=True):
    """Colonial street lamp (farol) on a post, base at (x,y)."""
    s = f'<rect x="{x-7}" y="{y-h}" width="14" height="{h}" fill="{color}"/><rect x="{x-22}" y="{y-14}" width="44" height="14" fill="{color}"/>'
    s += f'<path d="M{x-34},{y-h} L{x+34},{y-h} L{x+24},{y-h-70} L{x-24},{y-h-70} Z" fill="{"#ffd98a" if lit else "#223"}"/>'
    s += f'<path d="M{x-40},{y-h-70} L{x+40},{y-h-70} L{x},{y-h-110} Z" fill="{color}"/><rect x="{x-38}" y="{y-h}" width="76" height="8" fill="{color}"/>'
    if lit: s = glow(x, y - h - 35, 260, "warm", 0.85) + s
    return s


def window(x, y, w=90, h=150, lit=True, arch=True, color="#05070a", light="#ffc865"):
    top = f'A{w/2},{w/2} 0 0 1 {x+w},{y+w/2}' if arch else f'L{x+w},{y}'
    start = f'M{x},{y+w/2}' if arch else f'M{x},{y}'
    s = ""
    if lit: s += glow(x + w / 2, y + h / 2, w * 1.8, "warm", 0.55)
    s += f'<path d="{start} {top} L{x+w},{y+h} L{x},{y+h} Z" fill="{light if lit else "#0d141c"}"/>'
    s += f'<rect x="{x+w/2-2}" y="{y}" width="4" height="{h}" fill="{color}"/><rect x="{x}" y="{y+h*0.55}" width="{w}" height="4" fill="{color}"/>'
    return s


def facade(x, y_base, w=520, h=560, color="#0c1219", seed=1, lit=0.4, balcony=True):
    """Colonial house front: flat roof with cornice, arched windows/doors, optional balcony."""
    r = random.Random(seed)
    s = f'<rect x="{x}" y="{y_base-h}" width="{w}" height="{h}" fill="{color}"/><rect x="{x-12}" y="{y_base-h-18}" width="{w+24}" height="22" fill="{color}"/>'
    cols = max(2, int(w // 170))
    for i in range(cols):
        wx = x + (i + 0.5) * w / cols - 40
        s += window(wx, y_base - h + 70, 80, 140, r.random() < lit)
        if balcony and i % 2 == 0:
            s += f'<rect x="{wx-20}" y="{y_base-h+215}" width="120" height="8" fill="#05070a"/>' + "".join(f'<rect x="{wx-18+k*14}" y="{y_base-h+180}" width="3" height="38" fill="#05070a"/>' for k in range(9))
    s += f'<path d="M{x+w/2-55},{y_base} L{x+w/2-55},{y_base-170} A55,55 0 0 1 {x+w/2+55},{y_base-170} L{x+w/2+55},{y_base} Z" fill="#05070a"/>'
    return s


def church(x, y_base, scale=1.0, color="#080d13", lit_windows=True):
    """Baroque church silhouette: two bell towers + dome + cross, centred at x."""
    k = scale; s = ""
    for side in (-1, 1):
        tx = x + side * 230 * k
        s += f'<rect x="{tx-70*k}" y="{y_base-620*k}" width="{140*k}" height="{620*k}" fill="{color}"/>'
        s += f'<rect x="{tx-55*k}" y="{y_base-760*k}" width="{110*k}" height="{150*k}" fill="{color}"/>'
        s += f'<path d="M{tx-40*k},{y_base-660*k} L{tx-40*k},{y_base-700*k} A40,40 0 0 1 {tx+40*k},{y_base-700*k} L{tx+40*k},{y_base-660*k} Z" fill="{"#d9a85a" if lit_windows else "#111a24"}" opacity="0.8"/>'
        s += f'<path d="M{tx-60*k},{y_base-760*k} Q{tx},{y_base-860*k} {tx+60*k},{y_base-760*k} Z" fill="{color}"/>'
        s += f'<rect x="{tx-4*k}" y="{y_base-930*k}" width="{8*k}" height="{80*k}" fill="{color}"/><rect x="{tx-22*k}" y="{y_base-905*k}" width="{44*k}" height="{8*k}" fill="{color}"/>'
    s += f'<rect x="{x-170*k}" y="{y_base-480*k}" width="{340*k}" height="{480*k}" fill="{color}"/>'
    s += f'<path d="M{x-150*k},{y_base-480*k} Q{x},{y_base-700*k} {x+150*k},{y_base-480*k} Z" fill="{color}"/>'
    s += f'<rect x="{x-5*k}" y="{y_base-790*k}" width="{10*k}" height="{110*k}" fill="{color}"/><rect x="{x-30*k}" y="{y_base-760*k}" width="{60*k}" height="{10*k}" fill="{color}"/>'
    s += f'<path d="M{x-70*k},{y_base} L{x-70*k},{y_base-200*k} A70,70 0 0 1 {x+70*k},{y_base-200*k} L{x+70*k},{y_base} Z" fill="#030507"/>'
    s += f'<circle cx="{x}" cy="{y_base-360*k}" r="{45*k}" fill="{"#e0b066" if lit_windows else "#111a24"}" opacity="0.75"/>'
    return s


def cobbles(y0=1150, y1=H, color="#141b22", seed=9, wet=True):
    r = random.Random(seed); s = f'<rect x="0" y="{y0}" width="{W}" height="{y1-y0}" fill="{color}"/>'
    y = y0; row = 0
    while y < y1:
        hgt = 14 + (y - y0) * 0.06; x = -r.uniform(0, 60)
        while x < W:
            wdt = hgt * r.uniform(1.6, 2.4)
            s += f'<rect x="{x:.0f}" y="{y:.0f}" width="{wdt-4:.0f}" height="{hgt-3:.0f}" rx="{hgt/3:.0f}" fill="#1d2630" opacity="{r.uniform(0.4,0.9):.2f}"/>'
            if wet and r.random() < 0.08:
                s += f'<rect x="{x+4:.0f}" y="{y+2:.0f}" width="{wdt*0.5:.0f}" height="2" fill="#9fb6c9" opacity="0.35"/>'
            x += wdt
        y += hgt; row += 1
    return s


def papel_picado(y=0, color="#b3122e", n=8, seed=2, opacity=0.9):
    """String of papel-picado flags across the top (festive / Día de Muertos)."""
    r = random.Random(seed); s = f'<path d="M0,{y+20} Q{W/2},{y+90} {W},{y+20}" stroke="#222" stroke-width="3" fill="none"/>'
    cols = [color, "#e7a21b", "#5b2a86", "#1f7a5a", "#d9466f"]
    for i in range(n):
        x = (i + 0.5) * W / n; yy = y + 20 + 70 * (1 - ((x - W / 2) / (W / 2)) ** 2) - 5
        c = cols[i % len(cols)]
        s += f'<g opacity="{opacity}"><path d="M{x-90:.0f},{yy:.0f} L{x+90:.0f},{yy:.0f} L{x+90:.0f},{yy+150:.0f} L{x+60:.0f},{yy+170:.0f} L{x+30:.0f},{yy+150:.0f} L{x:.0f},{yy+170:.0f} L{x-30:.0f},{yy+150:.0f} L{x-60:.0f},{yy+170:.0f} L{x-90:.0f},{yy+150:.0f} Z" fill="{c}"/>'
        for _ in range(6):
            cx, cy = x + r.uniform(-60, 60), yy + r.uniform(30, 130)
            s += f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r.uniform(6,14):.0f}" fill="#000" opacity="0.55"/>'
        s += "</g>"
    return s


# ------------------------------------------------------------------ figures (silhouettes)
def figure(x, y, h=600, color="#020305", hat=None, dress="long", pose="stand", rim=None, facing=1, veil=False, hair=False, eyes=None):
    """Parametric human silhouette standing on (x,y), height h.
    hat: None | 'sombrero' | 'brim' (colonial wide hat) | 'cap' (nurse cap) | 'hood'
    dress: 'long' (floor gown) | 'robe' | 'cape' | 'trousers' | 'skirt'
    pose: 'stand' | 'arms_up' | 'reach' (one arm forward) | 'mourn' (hands to face) | 'walk' | 'point'
    rim: optional colour for a back-light rim glow (e.g. '#9fc2e8'); eyes: optional colour of glowing eyes ('#ff2a1a').
    veil/hair: long veil or long flowing hair. facing: 1 right, -1 left.
    """
    u = h / 100.0; f = facing
    hx, hy = x, y - 92 * u
    parts = []
    parts.append(f'<ellipse cx="{hx}" cy="{hy}" rx="{5.2*u}" ry="{6.4*u}"/>')
    parts.append(f'<rect x="{x-2*u}" y="{hy+5*u}" width="{4*u}" height="{4*u}"/>')
    sw = 11 * u if dress != "cape" else 15 * u
    parts.append(f'<path d="M{x-sw},{y-80*u} Q{x},{y-84*u} {x+sw},{y-80*u} L{x+8*u},{y-52*u} L{x-8*u},{y-52*u} Z"/>')
    if dress in ("long", "robe"):
        wid = 22 * u if dress == "long" else 16 * u
        parts.append(f'<path d="M{x-8*u},{y-54*u} Q{x-12*u},{y-25*u} {x-wid},{y} L{x+wid},{y} Q{x+12*u},{y-25*u} {x+8*u},{y-54*u} Z"/>')
    elif dress == "skirt":
        parts.append(f'<path d="M{x-8*u},{y-54*u} Q{x-14*u},{y-35*u} {x-18*u},{y-12*u} L{x+18*u},{y-12*u} Q{x+14*u},{y-35*u} {x+8*u},{y-54*u} Z"/>')
        parts.append(f'<rect x="{x-6*u}" y="{y-14*u}" width="{3.5*u}" height="{14*u}"/><rect x="{x+2.5*u}" y="{y-14*u}" width="{3.5*u}" height="{14*u}"/>')
    elif dress == "cape":
        parts.append(f'<path d="M{x-15*u},{y-80*u} Q{x-24*u},{y-35*u} {x-20*u},{y-8*u} L{x+20*u},{y-8*u} Q{x+24*u},{y-35*u} {x+15*u},{y-80*u} Z"/>')
        parts.append(f'<rect x="{x-7*u}" y="{y-12*u}" width="{4.5*u}" height="{12*u}"/><rect x="{x+2.5*u}" y="{y-12*u}" width="{4.5*u}" height="{12*u}"/>')
    else:  # trousers
        st = 6 * u if pose != "walk" else 12 * u
        parts.append(f'<path d="M{x-8*u},{y-54*u} L{x-2*u-st},{y} L{x-st+3*u},{y} L{x},{y-40*u} L{x+st-3*u},{y} L{x+2*u+st},{y} L{x+8*u},{y-54*u} Z"/>')
    aw = 3.6 * u
    sh_l, sh_r = (x - 10 * u, y - 79 * u), (x + 10 * u, y - 79 * u)
    if pose == "arms_up":
        arms = [(sh_l, (x - 22 * u, y - 100 * u)), (sh_r, (x + 22 * u, y - 100 * u))]
    elif pose == "reach":
        arms = [(sh_l, (x - 12 * u, y - 50 * u)), (sh_r, (x + f * 34 * u, y - 82 * u))]
    elif pose == "point":
        arms = [(sh_l, (x - 12 * u, y - 50 * u)), (sh_r, (x + f * 38 * u, y - 88 * u))]
    elif pose == "mourn":
        arms = [(sh_l, (x - 2 * u, y - 88 * u)), (sh_r, (x + 2 * u, y - 88 * u))]
    elif pose == "walk":
        arms = [(sh_l, (x - f * 12 * u, y - 52 * u)), (sh_r, (x + f * 12 * u, y - 52 * u))]
    else:
        arms = [(sh_l, (x - 13 * u, y - 50 * u)), (sh_r, (x + 13 * u, y - 50 * u))]
    for (a, b) in arms:
        mx, my = (a[0] + b[0]) / 2 + (b[1] - a[1]) * 0.08, (a[1] + b[1]) / 2
        parts.append(f'<path d="M{a[0]},{a[1]} Q{mx},{my} {b[0]},{b[1]}" stroke="{color}" stroke-width="{aw}" stroke-linecap="round" fill="none"/>')
    if hat == "sombrero":
        parts.append(f'<ellipse cx="{hx}" cy="{hy-4*u}" rx="{19*u}" ry="{3.2*u}"/>')
        parts.append(f'<path d="M{hx-7*u},{hy-5*u} Q{hx-6*u},{hy-17*u} {hx},{hy-18*u} Q{hx+6*u},{hy-17*u} {hx+7*u},{hy-5*u} Z"/>')
        parts.append(f'<path d="M{hx-19*u},{hy-4*u} Q{hx-21*u},{hy-8*u} {hx-17*u},{hy-7*u} M{hx+19*u},{hy-4*u} Q{hx+21*u},{hy-8*u} {hx+17*u},{hy-7*u}" stroke="{color}" stroke-width="{1.5*u}" fill="none"/>')
    elif hat == "brim":
        parts.append(f'<ellipse cx="{hx}" cy="{hy-4*u}" rx="{12*u}" ry="{2.4*u}"/><path d="M{hx-6*u},{hy-4*u} L{hx-5*u},{hy-12*u} L{hx+5*u},{hy-12*u} L{hx+6*u},{hy-4*u} Z"/>')
    elif hat == "cap":
        parts.append(f'<path d="M{hx-6*u},{hy-3*u} L{hx-8*u},{hy-10*u} L{hx+8*u},{hy-10*u} L{hx+6*u},{hy-3*u} Z" fill="#e9eef2"/>')
    elif hat == "hood":
        parts.append(f'<path d="M{hx-8*u},{hy+8*u} Q{hx-9*u},{hy-10*u} {hx},{hy-10*u} Q{hx+9*u},{hy-10*u} {hx+8*u},{hy+8*u} Z"/>')
    if veil:
        parts.append(f'<path d="M{hx-6*u},{hy-5*u} Q{hx-16*u},{hy+20*u} {hx-20*u},{y-40*u} L{hx+20*u},{y-40*u} Q{hx+16*u},{hy+20*u} {hx+6*u},{hy-5*u} Q{hx},{hy-9*u} {hx-6*u},{hy-5*u} Z" opacity="0.92"/>')
    if hair:
        parts.append(f'<path d="M{hx-5*u},{hy-3*u} Q{hx-f*12*u},{hy+15*u} {hx-f*9*u},{y-58*u} L{hx-f*2*u},{y-62*u} Q{hx},{hy+10*u} {hx+5*u},{hy-3*u} Z"/>')
    body = "".join(parts)
    s = ""
    if rim:
        s += f'<g fill="{rim}" filter="url(#blur2)" opacity="0.85">{body.replace(f"stroke=\"{color}\"", f"stroke=\"{rim}\"")}</g>'
    s += f'<g fill="{color}">{body}</g>'
    if eyes:
        for dx in (-1.9, 1.9):
            s += f'<circle cx="{hx+dx*u+f*0.8*u}" cy="{hy-0.5*u}" r="{2.6*u}" fill="{eyes}" opacity="0.5" filter="url(#blur1)"/><circle cx="{hx+dx*u+f*0.8*u}" cy="{hy-0.5*u}" r="{0.9*u}" fill="#fff4e0"/>'
    return s


def ghost_woman(x, y, h=700, color="#e9f1f7", opacity=0.85):
    """Translucent woman in a long white dress and veil whose hem dissolves into mist (La Llorona look)."""
    u = h / 100.0; hx, hy = x, y - 92 * u; g = _gid("gw")
    body = (f'<ellipse cx="{hx}" cy="{hy}" rx="{5*u}" ry="{6.2*u}"/>'
            f'<path d="M{hx-6*u},{hy-5*u} Q{hx-20*u},{hy+30*u} {hx-26*u},{y} L{hx+26*u},{y} Q{hx+20*u},{hy+30*u} {hx+6*u},{hy-5*u} Q{hx},{hy-10*u} {hx-6*u},{hy-5*u} Z"/>'
            f'<path d="M{x-10*u},{y-78*u} Q{x-20*u},{y-62*u} {x-16*u},{y-48*u}" stroke="{color}" stroke-width="{3.2*u}" fill="none" stroke-linecap="round"/>'
            f'<path d="M{x+10*u},{y-78*u} Q{x+26*u},{y-70*u} {x+32*u},{y-84*u}" stroke="{color}" stroke-width="{3.2*u}" fill="none" stroke-linecap="round"/>')
    fade = (f'<defs><linearGradient id="{g}" x1="0" y1="{y-100*u}" x2="0" y2="{y}" gradientUnits="userSpaceOnUse">'
            f'<stop offset="0" stop-color="#fff" stop-opacity="1"/><stop offset="0.65" stop-color="#fff" stop-opacity="0.9"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
            f'<mask id="m{g}"><rect x="{x-60*u}" y="{y-110*u}" width="{120*u}" height="{120*u}" fill="url(#{g})"/></mask></defs>')
    return (fade + f'<g mask="url(#m{g})" opacity="{opacity}">'
            f'<g fill="{color}" filter="url(#blur3)" opacity="0.7">{body}</g>'
            f'<g fill="{color}" filter="url(#ghost)" opacity="0.8">{body}</g>'
            f'<ellipse cx="{hx}" cy="{hy+1*u}" rx="{3.6*u}" ry="{4.6*u}" fill="#2a3640" opacity="0.55"/></g>')


# ------------------------------------------------------------------ thumbnails (author at 2400x1350, export --width 1280)
def thumb_text(text, x=110, y=420, size=330, fill="#ffffff", stroke="#000000", sw=30, anchor="start", rotate=0, font="Anton", spacing=2):
    """Huge thumbnail word(s) with a thick outline. Use 2-3 words max. Put \n in text for a second line."""
    lines = text.split("\n"); s = ""
    for i, ln in enumerate(lines):
        yy = y + i * size * 1.02
        s += (f'<text x="{x}" y="{yy}" text-anchor="{anchor}" font-family="{font}" font-size="{size}" letter-spacing="{spacing}" '
              f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" paint-order="stroke" '
              f'transform="rotate({rotate} {x} {yy})">{ln}</text>')
    return f'<g filter="url(#tshadow)">{s}</g>'

THUMB_DEFS = '<defs><filter id="tshadow" x="-10%" y="-20%" width="130%" height="160%"><feDropShadow dx="0" dy="14" stdDeviation="18" flood-color="#000" flood-opacity="0.9"/></filter></defs>'

def thumb(*parts):
    """Thumbnail on the normal 2400x1350 canvas; render with: node render_svg.js thumb.svg --width 1280"""
    return svg(*parts, defs=THUMB_DEFS)
