"""Custom characters for La Mulata de Córdoba (hand-written SVG paths, local coordinates + transforms)."""
import math, random

_n = [0]
def uid(p="c"):
    _n[0] += 1
    return f"{p}{_n[0]}"

SKIN = dict(base="#7a4a2e", light="#b07650", hi="#d59c6e", shadow="#4a2918", deep="#2b150c")
REB = ["#c8963e", "#d9c7a0", "#6b2a24", "#3a5590"]


def grad_lin(id_, stops, x1=0, y1=0, x2=1, y2=0, units="userSpaceOnUse"):
    u = f' gradientUnits="{units}"' if units else ""
    s = "".join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a}"/>' for o, c, a in stops)
    return f'<linearGradient id="{id_}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"{u}>{s}</linearGradient>'


def grad_rad(id_, stops, cx=0.5, cy=0.5, r=0.5, units=None):
    u = f' gradientUnits="{units}"' if units else ""
    s = "".join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a}"/>' for o, c, a in stops)
    return f'<radialGradient id="{id_}" cx="{cx}" cy="{cy}" r="{r}"{u}>{s}</radialGradient>'


def curls(path_pts, seed=1, r0=9, r1=16, color="#140a06", hi="#5a3a28", density=1.0):
    """Clusters of springy curls along a polyline [(x,y,spread),...]."""
    r = random.Random(seed); out = []; his = []
    for i in range(len(path_pts) - 1):
        (x0, y0, s0), (x1, y1, s1) = path_pts[i], path_pts[i + 1]
        n = int(10 * density * (1 + math.hypot(x1 - x0, y1 - y0) / 60))
        for k in range(n):
            u = r.random(); x = x0 + (x1 - x0) * u; y = y0 + (y1 - y0) * u; sp = s0 + (s1 - s0) * u
            x += r.uniform(-sp, sp); y += r.uniform(-sp * 0.6, sp * 0.6)
            rr = r.uniform(r0, r1)
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rr:.1f}"/>')
            if r.random() < 0.6:
                a0 = r.uniform(0, 6.28)
                his.append(f'<path d="M{x+rr*0.6*math.cos(a0):.1f},{y+rr*0.6*math.sin(a0):.1f} A{rr*0.6:.1f},{rr*0.6:.1f} 0 0 1 {x+rr*0.6*math.cos(a0+2.4):.1f},{y+rr*0.6*math.sin(a0+2.4):.1f}"/>')
    return (f'<g fill="{color}">{"".join(out)}</g>'
            f'<g fill="none" stroke="{hi}" stroke-width="2.2" stroke-linecap="round" opacity="0.85">{"".join(his)}</g>')


# ------------------------------------------------------------------ head (local coords: face ~245 tall, centre 0,0)
def head(look=0.0, smile=0.5, lids=0.2, rim="#9fc2e8", wrap="#8c2a1d", wrap_hi="#c9563c", wrap_dk="#4a120b",
         earring=True, seed=3, turn=0.0, back_curls=True, eyes_closed=False, neck=True):
    """Afro-Mexican woman's head: tied headwrap (pañuelo), escaping curls, calm knowing gaze.
    turn: -1..1 head rotation (positive = face turned toward viewer's right)."""
    g = uid("h"); sk = SKIN
    ml, mr = (1 + 0.06 * turn, 1 - 0.32 * turn) if turn >= 0 else (1 + 0.32 * turn, 1 - 0.06 * turn)
    fx = lambda x: x * (ml if x < 0 else mr)
    sh = turn * 20  # feature shift
    def P(pts):
        return " ".join(f"{fx(x):.1f},{y:.1f}" if isinstance(x, (int, float)) else x for x, y in pts)
    face = (f"M{fx(-72):.1f},-62 C{fx(-78):.1f},-12 {fx(-74):.1f},34 {fx(-58):.1f},64 C{fx(-44):.1f},94 {fx(-21):.1f},114 {sh*0.4:.1f},116 "
            f"C{fx(21)+sh*0.5:.1f},114 {fx(44):.1f},94 {fx(58):.1f},64 C{fx(74):.1f},34 {fx(78):.1f},-12 {fx(72):.1f},-62 "
            f"C{fx(64):.1f},-112 {fx(30):.1f},-130 0,-130 C{fx(-30):.1f},-130 {fx(-64):.1f},-112 {fx(-72):.1f},-62 Z")
    defs = ("<defs>"
            + grad_lin(g + "f", [(0, sk["shadow"], 1), (0.42, sk["base"], 1), (0.78, sk["light"], 1), (1, sk["base"], 1)], -80, 0, 80, 0)
            + grad_rad(g + "c", [(0, sk["hi"], 0.75), (1, sk["hi"], 0)], 0.5, 0.5, 0.5)
            + grad_lin(g + "n", [(0, sk["deep"], 1), (0.5, sk["shadow"], 1), (1, sk["base"], 1)], -45, 0, 45, 0)
            + grad_lin(g + "w", [(0, wrap_dk, 1), (0.45, wrap, 1), (1, wrap_hi, 1)], -110, -100, 110, -200)
            + grad_lin(g + "j", [(0, sk["deep"], 0.9), (1, sk["deep"], 0)], 0, 75, 0, 140)
            + "</defs>")
    s = defs
    if back_curls:
        s += curls([(-84, -60, 10), (-98, 10, 14), (-100, 80, 16), (-90, 130, 14)], seed, 10, 17)
        s += curls([(84, -60, 10), (98, 10, 14), (102, 80, 16), (94, 125, 12)], seed + 1, 10, 17)
    if neck:
        # neck (shorter, wider)
        s += f'<path d="M{fx(-44):.0f},64 C{fx(-44):.0f},100 {fx(-48):.0f},130 {fx(-60):.0f},168 L{fx(62):.0f},168 C{fx(50):.0f},130 {fx(46):.0f},100 {fx(44):.0f},64 Z" fill="url(#{g}n)"/>'
        s += f'<path d="M{fx(-46):.0f},64 L{fx(-46):.0f},168 L{fx(64):.0f},168 L{fx(46):.0f},64 Z" fill="url(#{g}j)"/>'
        s += f'<path d="M{-16+sh:.0f},112 Q{-12+sh:.0f},140 {-20+sh:.0f},166" stroke="{sk["deep"]}" stroke-width="3" fill="none" opacity="0.3"/>'
    # ears
    if turn < 0.4:
        s += f'<path d="M{fx(-72):.0f},-20 C{fx(-88):.0f},-26 {fx(-90):.0f},6 {fx(-78):.0f},22 C{fx(-74):.0f},26 {fx(-70):.0f},20 {fx(-70):.0f},14 Z" fill="{sk["shadow"]}"/>'
    if turn > -0.4:
        s += f'<path d="M{fx(72):.0f},-20 C{fx(88):.0f},-26 {fx(90):.0f},6 {fx(78):.0f},22 C{fx(74):.0f},26 {fx(70):.0f},20 {fx(70):.0f},14 Z" fill="{sk["base"]}"/>'
    s += f'<path d="{face}" fill="url(#{g}f)"/>'
    # modelling
    s += f'<ellipse cx="{fx(40)+sh*0.5:.0f}" cy="10" rx="30" ry="22" fill="url(#{g}c)" opacity="0.8"/>'
    s += f'<ellipse cx="{14+sh*0.5:.0f}" cy="-82" rx="40" ry="22" fill="url(#{g}c)" opacity="0.5"/>'
    s += f'<ellipse cx="{6+sh:.0f}" cy="98" rx="16" ry="9" fill="url(#{g}c)" opacity="0.45"/>'
    s += f'<ellipse cx="{fx(-42):.0f}" cy="16" rx="22" ry="18" fill="{sk["deep"]}" opacity="0.16" filter="url(#blur1)"/>'
    s += (f'<path d="M{fx(-58):.1f},64 C{fx(-44):.1f},94 {fx(-21):.1f},114 {sh*0.4:.1f},116 C{fx(21)+sh*0.5:.1f},114 {fx(44):.1f},94 {fx(58):.1f},64 '
          f'C{fx(46):.1f},98 {fx(22)+sh*0.5:.1f},108 {sh*0.4:.1f},109 C{fx(-22):.1f},108 {fx(-46):.1f},98 {fx(-58):.1f},64 Z" fill="{sk["deep"]}" opacity="0.32"/>')
    # ---- features group (shifted for turn)
    f = ""
    for side in (-1, 1):
        k = (ml if side < 0 else mr)
        ex = side * 31 * k
        e = lambda x, y: f"{ex + (x - side*31) * k + sh:.1f},{y:.1f}"
        # brows
        f += f'<path d="M{e(side*62,-41)} Q{e(side*38,-61)} {e(side*10,-48)} Q{e(side*35,-53)} {e(side*62,-41)} Z" fill="#150906"/>'
        # socket
        f += f'<ellipse cx="{ex+sh:.1f}" cy="-21" rx="{27*k:.1f}" ry="14" fill="{sk["deep"]}" opacity="{0.26 if side<0 else 0.18}" filter="url(#blur1)"/>'
        eye = f"M{e(side*57,-17)} Q{e(side*32,-38)} {e(side*7,-18)} Q{e(side*31,-3)} {e(side*57,-17)} Z"
        cid = uid("ec")
        f += f'<defs><clipPath id="{cid}"><path d="{eye}"/></clipPath></defs>'
        if eyes_closed:
            f += f'<path d="{eye}" fill="{sk["shadow"]}"/>'
            f += f'<path d="M{e(side*57,-16)} Q{e(side*31,-6)} {e(side*7,-17)}" stroke="#0c0503" stroke-width="4" fill="none" stroke-linecap="round"/>'
            continue
        ix = ex + sh + look * 7 * k
        f += f'<path d="{eye}" fill="#cdb79c"/>'
        f += (f'<g clip-path="url(#{cid})"><circle cx="{ix:.1f}" cy="-19" r="11.5" fill="#3d1f0f"/>'
              f'<circle cx="{ix:.1f}" cy="-19" r="8" fill="#1e0e06"/><circle cx="{ix:.1f}" cy="-19" r="4.6" fill="#050201"/>'
              f'<circle cx="{ix+3.8:.1f}" cy="-23.5" r="2.8" fill="#fff8ee"/><circle cx="{ix-3.4:.1f}" cy="-14.5" r="1.3" fill="#f0d8c0" opacity="0.7"/>'
              f'<path d="M{e(side*62,-44)} L{e(side*3,-44)} L{e(side*3,-19)} Q{e(side*32,-38+lids*18)} {e(side*62,-15)} Z" fill="{sk["base"] if side > 0 else sk["shadow"]}"/></g>')
        f += f'<path d="M{e(side*59,-16)} Q{e(side*32,-38+lids*18)} {e(side*6,-19)}" stroke="#0c0503" stroke-width="4.2" fill="none" stroke-linecap="round"/>'
        f += f'<path d="M{e(side*58,-17)} Q{e(side*61,-19)} {e(side*63,-22)}" stroke="#0c0503" stroke-width="2.4" fill="none" stroke-linecap="round" opacity="0.8"/>'
        f += f'<path d="M{e(side*53,-12)} Q{e(side*31,-3)} {e(side*10,-15)}" stroke="{sk["deep"]}" stroke-width="1.6" fill="none" opacity="0.7"/>'
        f += f'<path d="M{e(side*54,-31)} Q{e(side*32,-45+lids*8)} {e(side*9,-31)}" stroke="{sk["deep"]}" stroke-width="2" fill="none" opacity="0.5"/>'
    # nose
    n = lambda x, y: f"{x + sh*1.15:.1f},{y:.1f}"
    f += f'<path d="M{n(-8,-12)} C{n(-10,6)} {n(-14,18)} {n(-18,30)}" stroke="{sk["deep"]}" stroke-width="3" fill="none" opacity="0.35" stroke-linecap="round"/>'
    if turn > 0.2:
        f += f'<path d="M{n(4,-14)} C{n(10,6)} {n(20,22)} {n(24,32)} Q{n(26,42)} {n(14,46)}" stroke="{sk["deep"]}" stroke-width="3" fill="none" opacity="0.55" stroke-linecap="round"/>'
    f += f'<path d="M{n(6,-14)} C{n(10,6)} {n(12,18)} {n(12,26)}" stroke="{sk["hi"]}" stroke-width="4" fill="none" opacity="0.35" stroke-linecap="round"/>'
    f += f'<path d="M{n(-26,34)} Q{n(-30,46)} {n(-16,47)} Q{n(-8,44)} {n(0,48)} Q{n(8,44)} {n(16,47)} Q{n(30,46)} {n(26,34)} Q{n(20,26)} {n(10,30)} Q{n(0,26)} {n(-10,30)} Q{n(-20,26)} {n(-26,34)} Z" fill="{sk["shadow"]}" opacity="0.55"/>'
    f += f'<ellipse cx="{3+sh*1.15:.1f}" cy="34" rx="11" ry="8" fill="{sk["light"]}" opacity="0.8"/><ellipse cx="{6+sh*1.15:.1f}" cy="31" rx="4" ry="2.5" fill="{sk["hi"]}" opacity="0.8"/>'
    f += f'<path d="M{n(-15,44)} Q{n(-10,40)} {n(-5,45)} M{n(15,44)} Q{n(10,40)} {n(5,45)}" stroke="#1d0c06" stroke-width="3.4" fill="none" stroke-linecap="round"/>'
    f += f'<path d="M{n(-24,36)} Q{n(-29,44)} {n(-21,47)} M{n(24,36)} Q{n(29,44)} {n(21,47)}" stroke="{sk["deep"]}" stroke-width="2.2" fill="none" opacity="0.8"/>'
    # mouth
    m = lambda x, y: f"{x*(1-0.15*abs(turn)) + sh:.1f},{y:.1f}"
    cy0 = 68; up = smile * 4
    f += f'<path d="M{m(-27,cy0-up)} Q{m(-15,cy0-12)} {m(-5,cy0-9)} Q{m(0,cy0-7)} {m(5,cy0-9)} Q{m(15,cy0-12)} {m(27,cy0-up)} Q{m(12,cy0+1)} {m(0,cy0+1)} Q{m(-12,cy0+1)} {m(-27,cy0-up)} Z" fill="#5e2622"/>'
    f += f'<path d="M{m(-25,cy0-up+1)} Q{m(-12,cy0+3)} {m(0,cy0+3)} Q{m(12,cy0+3)} {m(25,cy0-up+1)} Q{m(16,cy0+20)} {m(0,cy0+21)} Q{m(-16,cy0+20)} {m(-25,cy0-up+1)} Z" fill="#7d3b34"/>'
    f += f'<ellipse cx="{5+sh:.1f}" cy="{cy0+11}" rx="10" ry="3.5" fill="#c4887a" opacity="0.55"/>'
    f += f'<path d="M{m(-27,cy0-up)} Q{m(-12,cy0+2)} {m(0,cy0+2)} Q{m(12,cy0+2)} {m(27,cy0-up)}" stroke="#220b08" stroke-width="2.4" fill="none" stroke-linecap="round"/>'
    f += f'<path d="M{m(-28,cy0-up-2)} q-4,2 -3,6 M{m(28,cy0-up-2)} q4,2 3,6" stroke="{sk["deep"]}" stroke-width="2" fill="none" opacity="0.55"/>'
    s += f
    # subtle cool rim on the shadow side
    if rim:
        s += f'<path d="M{fx(-73):.0f},-56 C{fx(-78):.0f},-12 {fx(-74):.0f},34 {fx(-60):.0f},62" stroke="{rim}" stroke-width="3" fill="none" opacity="0.45" filter="url(#blur1)"/>'
    # temple curls
    s += curls([(fx(-76), -80, 6), (fx(-82), -36, 7), (fx(-84), 4, 6)], seed + 5, 8, 12)
    s += curls([(fx(76), -80, 6), (fx(82), -40, 6)], seed + 6, 8, 12)
    # ---- headwrap: wide wrapped volume leaning back, twisted knot at top-front
    W = (f"M{fx(-88):.0f},-58 C{fx(-118):.0f},-104 {fx(-116):.0f},-168 -40,-192 C20,-210 {fx(100):.0f},-200 {fx(116):.0f},-150 "
         f"C{fx(124):.0f},-116 {fx(108):.0f},-82 {fx(92):.0f},-56 C{fx(76):.0f},-88 {fx(40):.0f},-106 0,-106 C{fx(-42):.0f},-106 {fx(-72):.0f},-88 {fx(-88):.0f},-58 Z")
    s += f'<path d="{W}" fill="url(#{g}w)"/>'
    s += f'<path d="M{fx(-86):.0f},-58 C{fx(-72):.0f},-88 {fx(-42):.0f},-106 0,-106 C{fx(40):.0f},-106 {fx(74):.0f},-88 {fx(90):.0f},-56 C{fx(78):.0f},-74 {fx(46):.0f},-92 0,-92 C{fx(-46):.0f},-92 {fx(-74):.0f},-78 {fx(-86):.0f},-58 Z" fill="{wrap_dk}" opacity="0.85"/>'
    cid = uid("wc")
    s += f'<defs><clipPath id="{cid}"><path d="{W}"/></clipPath></defs><g clip-path="url(#{cid})">'
    for i in range(7):
        y0 = -96 - i * 16
        d = f"M{fx(-120):.0f},{y0+40} C{fx(-60):.0f},{y0-10} {fx(20):.0f},{y0-30} {fx(130):.0f},{y0-70}"
        s += f'<path d="{d}" stroke="{wrap_dk}" stroke-width="{9 if i%2 else 6}" fill="none" opacity="0.55"/>'
        s += f'<path d="{d}" stroke="{wrap_hi}" stroke-width="3" fill="none" opacity="0.5" transform="translate(0,-9)"/>'
    rr = random.Random(seed)
    for k in range(60):
        x = rr.uniform(-110, 110); y = rr.uniform(-200, -100)
        s += f'<circle cx="{fx(x):.0f}" cy="{y:.0f}" r="{rr.uniform(1.8,3):.1f}" fill="#e8c26a" opacity="0.55"/>'
    s += "</g>"
    # knot: twisted rosette + two fabric tails up and back
    kx = fx(46) + sh * 0.3; ky = -188
    s += (f'<path d="M{kx:.0f},{ky:.0f} C{kx-30:.0f},{ky-40:.0f} {kx-70:.0f},{ky-30:.0f} {kx-64:.0f},{ky-6:.0f} C{kx-50:.0f},{ky+6:.0f} {kx-20:.0f},{ky+4:.0f} {kx:.0f},{ky:.0f} Z" fill="{wrap_hi}"/>'
          f'<path d="M{kx:.0f},{ky:.0f} C{kx+24:.0f},{ky-46:.0f} {kx+66:.0f},{ky-44:.0f} {kx+66:.0f},{ky-14:.0f} C{kx+60:.0f},{ky+4:.0f} {kx+26:.0f},{ky+6:.0f} {kx:.0f},{ky:.0f} Z" fill="{wrap}"/>'
          f'<path d="M{kx-56:.0f},{ky-14:.0f} C{kx-40:.0f},{ky-28:.0f} {kx-20:.0f},{ky-20:.0f} {kx-6:.0f},{ky-4:.0f} M{kx+56:.0f},{ky-24:.0f} C{kx+40:.0f},{ky-34:.0f} {kx+20:.0f},{ky-24:.0f} {kx+6:.0f},{ky-6:.0f}" stroke="{wrap_dk}" stroke-width="4" fill="none" opacity="0.7"/>'
          f'<ellipse cx="{kx:.0f}" cy="{ky+2:.0f}" rx="17" ry="13" fill="{wrap}"/><path d="M{kx-12:.0f},{ky:.0f} Q{kx:.0f},{ky-10:.0f} {kx+12:.0f},{ky:.0f}" stroke="{wrap_hi}" stroke-width="3" fill="none"/>')
    if earring:
        if turn < 0.4:
            s += f'<circle cx="{fx(-80):.0f}" cy="44" r="15" stroke="#9c7a33" stroke-width="3.5" fill="none" opacity="0.9"/>'
        if turn > -0.4:
            s += f'<circle cx="{fx(80):.0f}" cy="44" r="15" stroke="#e5b54e" stroke-width="3.5" fill="none"/><circle cx="{fx(76):.0f}" cy="31" r="3" fill="#f4d27a"/>'
    return s


def herb_bundle(x, y, k=1.0, rot=0, seed=4):
    """Bundle of ruda / hierbabuena tied with red thread; stems end at (0,90)."""
    r = random.Random(seed); s = ""
    for i in range(16):
        a = math.radians(-90 + r.uniform(-30, 30)); L = r.uniform(110, 190)
        x1, y1 = math.cos(a) * L, math.sin(a) * L
        s += f'<path d="M0,40 Q{x1*0.4:.0f},{y1*0.5:.0f} {x1:.0f},{y1:.0f}" stroke="#3d5a2a" stroke-width="3" fill="none"/>'
        for j in range(5):
            t = 0.4 + j * 0.13; lx, ly = x1 * t, y1 * t
            ang = r.uniform(-60, 60); col = r.choice(["#5f8a3a", "#4f7a32", "#7aa04a", "#3e6a2c"])
            s += f'<ellipse cx="{lx:.0f}" cy="{ly:.0f}" rx="{r.uniform(6,11):.0f}" ry="{r.uniform(3,5):.0f}" fill="{col}" transform="rotate({ang:.0f} {lx:.0f} {ly:.0f})"/>'
        if r.random() < 0.35:
            s += f'<circle cx="{x1:.0f}" cy="{y1:.0f}" r="5" fill="#e0c040"/>'
    s += '<path d="M-10,30 L10,30 L8,90 L-8,90 Z" fill="#3a5226"/><path d="M-12,40 L12,46 M-12,50 L12,56" stroke="#b3122e" stroke-width="5"/>'
    return f'<g transform="translate({x},{y}) rotate({rot}) scale({k})">{s}</g>'


def hand_fist(x, y, k=1.0, rot=0, shade=False):
    """Hand closed around a stem, seen from the back; knuckles to +x. centre at (0,0), ~70 wide."""
    sk = SKIN; c = sk["shadow"] if shade else sk["base"]
    s = (f'<path d="M-40,-18 C-30,-34 10,-38 30,-30 C46,-24 50,-8 46,6 C44,22 30,32 10,32 C-10,32 -30,26 -40,14 Z" fill="{c}"/>'
         f'<path d="M30,-30 C40,-20 42,-6 40,4 M34,-14 L46,-12 M32,4 L44,8 M24,20 L36,24" stroke="{sk["deep"]}" stroke-width="2.4" fill="none" opacity="0.7"/>'
         f'<path d="M-30,-26 C-10,-34 14,-34 28,-28" stroke="{sk["hi"]}" stroke-width="4" fill="none" opacity="0.5"/>'
         f'<path d="M-6,30 C4,38 18,36 22,28 C16,24 4,24 -6,30 Z" fill="{sk["light"]}"/>')
    return f'<g transform="translate({x},{y}) rotate({rot}) scale({k})">{s}</g>'


def hand_open(x, y, k=1.0, rot=0, shade=False):
    """Open hand, palm down, fingers extended toward +x; wrist at (0,0). ~160 long."""
    sk = SKIN; c = sk["shadow"] if shade else sk["base"]
    s = (f'<path d="M0,-22 C30,-30 70,-30 92,-24 C112,-20 136,-16 150,-8 C158,-4 156,6 146,6 C130,4 112,2 98,6 '
         f'C120,10 140,14 148,20 C154,26 148,34 138,32 C120,28 104,24 92,26 C110,32 124,38 128,44 C130,52 122,56 114,52 '
         f'C100,46 86,40 76,40 C84,48 90,56 88,62 C84,68 76,66 70,60 C56,48 40,34 24,28 C10,24 0,20 -4,10 Z" fill="{c}"/>'
         f'<path d="M30,-24 C50,-28 80,-28 100,-20" stroke="{sk["hi"]}" stroke-width="5" fill="none" opacity="0.5"/>'
         f'<path d="M98,6 C106,4 116,2 126,4 M92,26 C100,26 110,28 118,30 M76,40 C84,40 92,44 100,48" stroke="{sk["deep"]}" stroke-width="2.5" fill="none" opacity="0.6"/>')
    return f'<g transform="translate({x},{y}) rotate({rot}) scale({k})">{s}</g>'


def fist(x, y, k=1.0, shade=False):
    """Small closed hand seen from the front: four stacked fingers + thumb across the top. Centre (x,y), ~60 units."""
    sk = SKIN; c = sk["shadow"] if shade else sk["base"]; s = ""
    s += f'<path d="M-30,-26 C-10,-34 20,-32 30,-22 L32,24 C20,34 -10,34 -30,26 Z" fill="{c}"/>'
    for i in range(4):
        yy = -18 + i * 13
        s += f'<rect x="-30" y="{yy-6}" width="58" height="13" rx="6.5" fill="{c}" stroke="{sk["deep"]}" stroke-width="1.6" stroke-opacity="0.6"/>'
        s += f'<path d="M-24,{yy-3} q20,-3 44,0" stroke="{sk["hi"]}" stroke-width="2" fill="none" opacity="0.35"/>'
    s += f'<path d="M-34,-24 C-20,-36 10,-36 26,-26 C14,-22 -10,-20 -30,-14 Z" fill="{sk["light"]}"/>'
    return f'<g transform="translate({x},{y}) scale({k})">{s}</g>'


def head_profile(rim="#ffd27a", wrap="#8c2a1d", wrap_hi="#c9563c", wrap_dk="#4a120b", seed=8, smile=0.4, lit=0.6):
    """Profile head facing +x (right). Centre ~ (0,0), face ~245 tall; neck to y=230. Rim light on the face edge."""
    g = uid("p"); sk = SKIN
    prof = ("M30,-128 C56,-120 70,-86 72,-50 C72,-38 68,-28 64,-22 C70,-10 84,10 96,26 C100,32 96,40 88,42 "
            "C82,44 78,46 76,50 C80,54 86,58 87,63 C85,68 80,70 78,71 C82,74 87,80 85,86 C80,92 72,94 70,96 "
            "C74,102 78,110 74,118 C66,128 50,132 36,134 C30,136 24,140 22,148 L28,236 L-64,236 "
            "C-60,180 -58,120 -62,80 C-72,40 -82,-20 -72,-80 C-62,-120 -10,-136 30,-128 Z")
    s = (f'<defs>{grad_lin(g+"f", [(0, sk["deep"], 1), (0.5, sk["shadow"], 1), (0.85, sk["base"], 1), (1, sk["light"], 1)], -70, 0, 100, 0)}'
         f'{grad_rad(g+"c", [(0, sk["hi"], 0.7), (1, sk["hi"], 0)], 0.5, 0.5, 0.5)}</defs>')
    s += curls([(-70, -40, 12), (-78, 40, 16), (-70, 120, 16), (-50, 180, 14)], seed, 11, 17)
    s += f'<path d="{prof}" fill="url(#{g}f)"/>'
    s += f'<ellipse cx="44" cy="10" rx="26" ry="22" fill="url(#{g}c)" opacity="{lit}"/>'
    s += f'<path d="M-6,40 C10,90 30,118 60,124" stroke="{sk["deep"]}" stroke-width="5" fill="none" opacity="0.4" filter="url(#blur1)"/>'
    # ear + earring
    s += f'<path d="M-14,-18 C-30,-22 -34,10 -22,26 C-14,32 -6,24 -8,12 C-4,0 -4,-14 -14,-18 Z" fill="{sk["shadow"]}"/>'
    s += f'<path d="M-18,-8 C-24,0 -22,12 -16,18" stroke="{sk["deep"]}" stroke-width="2.5" fill="none"/>'
    s += f'<circle cx="-18" cy="44" r="15" stroke="#e5b54e" stroke-width="3.5" fill="none"/>'
    # eye (profile wedge), lashes, brow
    s += f'<path d="M58,-20 Q48,-28 38,-20 Q48,-12 58,-18 Z" fill="#cdb79c"/><path d="M58,-20 Q52,-23 48,-20 Q52,-15 57,-18 Z" fill="#1e0e06"/>'
    s += f'<path d="M60,-21 Q48,-31 36,-21" stroke="#0c0503" stroke-width="3.6" fill="none" stroke-linecap="round"/>'
    s += f'<path d="M60,-21 l6,-4 M58,-24 l5,-6" stroke="#0c0503" stroke-width="2" stroke-linecap="round"/>'
    s += f'<path d="M30,-44 Q50,-52 68,-42" stroke="#150906" stroke-width="6" fill="none" stroke-linecap="round"/>'
    s += f'<path d="M76,50 C66,48 62,44 64,36" stroke="{sk["deep"]}" stroke-width="2.5" fill="none" opacity="0.8"/>'
    s += f'<path d="M84,64 C82,72 80,72 78,71 C82,76 84,80 84,84" fill="#6e2e28" stroke="none"/>'
    s += f'<path d="M78,71 L66,{70-smile*4:.0f}" stroke="#220b08" stroke-width="2.4" stroke-linecap="round"/>'
    # rim light on the profile edge
    if rim:
        s += (f'<path d="M30,-128 C56,-120 70,-86 72,-50 C72,-38 68,-28 64,-22 C70,-10 84,10 96,26 C100,32 96,40 88,42 '
              f'C82,44 78,46 76,50 C80,54 86,58 87,63 C85,68 80,70 78,71 C82,74 87,80 85,86 C80,92 72,94 70,96 '
              f'C74,102 78,110 74,118 C66,128 50,132 36,134 C30,136 24,140 22,148 L28,236" stroke="{rim}" stroke-width="5" fill="none" opacity="0.9" filter="url(#blur1)"/>')
        s += f'<path d="M30,-128 C56,-120 70,-86 72,-50 C72,-38 68,-28 64,-22 C70,-10 84,10 96,26 C100,32 96,40 88,42" stroke="#fff4d6" stroke-width="2" fill="none" opacity="0.8"/>'
    # headwrap covering the skull, knot at the back
    W = ("M70,-70 C76,-120 50,-180 -10,-200 C-70,-214 -130,-180 -140,-120 C-146,-80 -134,-40 -108,-16 "
         "C-96,-30 -84,-52 -70,-60 C-40,-84 10,-92 70,-70 Z")
    s += f'<path d="{W}" fill="{wrap}"/>'
    cid = uid("pw")
    s += f'<defs><clipPath id="{cid}"><path d="{W}"/></clipPath></defs><g clip-path="url(#{cid})">'
    for i in range(7):
        s += f'<path d="M{80-i*6},{-80-i*18} C{30-i*10},{-150-i*8} {-80-i*4},{-170+i*6} {-150},{-50+i*4}" stroke="{wrap_dk}" stroke-width="{8 if i%2 else 5}" fill="none" opacity="0.55"/>'
        s += f'<path d="M{80-i*6},{-88-i*18} C{30-i*10},{-158-i*8} {-80-i*4},{-178+i*6} {-150},{-58+i*4}" stroke="{wrap_hi}" stroke-width="3" fill="none" opacity="0.5"/>'
    s += f'<path d="M-160,-220 L-20,-220 L-60,0 L-160,0 Z" fill="#000" opacity="0.3"/></g>'
    s += (f'<path d="M-118,-160 C-160,-206 -206,-180 -190,-136 C-178,-112 -144,-120 -122,-136 Z" fill="{wrap_hi}"/>'
          f'<path d="M-122,-148 C-172,-134 -188,-96 -160,-80 C-142,-74 -126,-100 -116,-124 Z" fill="{wrap}"/>'
          f'<ellipse cx="-124" cy="-140" rx="20" ry="16" fill="{wrap}"/><path d="M-138,-142 Q-124,-152 -110,-140" stroke="{wrap_hi}" stroke-width="3" fill="none"/>')
    if rim:
        s += f'<path d="M70,-70 C76,-120 50,-180 -10,-200" stroke="{rim}" stroke-width="5" fill="none" opacity="0.7" filter="url(#blur1)"/>'
    return s


def mulata_backview(x, y, h=900, rim="#ffd27a", reach=True, face_left=True, skirt="#26355e", skirt_dk="#111833", skirt_hi="#4a5f96"):
    """Full figure seen from behind, stepping toward a wall/ship, head in profile looking back.
    feet at (x,y); height h."""
    g = uid("bv"); k = h / 1000.0; sk = SKIN
    s = (f'<defs>{grad_lin(g+"sk", [(0, skirt_dk, 1), (0.5, skirt, 1), (0.8, skirt_hi, 1), (1, skirt_dk, 1)], -240, 0, 240, 0)}'
         f'{grad_lin(g+"rb", [(0, "#070c1e", 1), (0.55, "#18244a", 1), (1, "#2e4170", 1)], -170, 0, 170, 0)}</defs>')
    hem = " ".join(f"{-250 + 480*t:.0f},{-6 + 10*math.sin(t*math.pi*7) + 14*math.sin(t*math.pi):.0f}" for t in [i/24 for i in range(25)])
    skirt_d = f"M-66,-585 C-92,-450 -170,-230 -250,-8 L{hem} C168,-230 92,-450 66,-585 Z"
    s += f'<path d="{skirt_d}" fill="url(#{g}sk)"/>'
    for i, (xa, xb) in enumerate([(-50, -170), (-25, -92), (0, -12), (25, 62), (50, 146), (-62, -224), (60, 205)]):
        s += f'<path d="M{xa},-570 C{xa+(xb-xa)*0.25:.0f},-380 {xb*0.88:.0f},-200 {xb},4" stroke="{skirt_dk}" stroke-width="{13 if i%2 else 8}" fill="none" opacity="0.5"/>'
    s += f'<path d="M-248,-12 L{hem}" stroke="#9c1a2a" stroke-width="13" fill="none" opacity="0.9" transform="translate(0,-8)"/>'
    # raised right arm reaching forward (toward the wall, up-right)
    if reach:
        s += f'<path d="M60,-800 C100,-830 150,-850 200,-860 C222,-864 230,-830 210,-824 C170,-812 130,-790 96,-750 Z" fill="#e6dcc8"/>'
        s += f'<path d="M200,-862 C236,-872 270,-884 300,-896 C312,-900 318,-882 306,-876 C276,-864 244,-850 210,-826 Z" fill="{sk["base"]}"/>'
        s += f'<path d="M298,-898 C316,-908 340,-914 356,-910 C364,-906 360,-896 350,-896 C336,-894 322,-888 310,-878 Z" fill="{sk["base"]}"/>'
        if rim:
            s += f'<path d="M60,-800 C100,-830 150,-850 200,-860 C240,-872 280,-888 356,-910" stroke="{rim}" stroke-width="5" fill="none" opacity="0.7" filter="url(#blur1)"/>'
    # rebozo covering the back to the hips, fringe
    hp = head_profile(rim=rim)
    tr = "translate(6,-905) scale(-0.48,0.48)" if face_left else "translate(-6,-905) scale(0.48)"
    s += f'<g transform="{tr}">{hp}</g>'
    reb = "M-30,-842 C-80,-840 -112,-812 -126,-770 C-146,-690 -162,-590 -172,-480 C-130,-460 -50,-420 0,-392 C50,-420 130,-460 172,-480 C162,-590 146,-690 126,-770 C112,-812 80,-840 30,-842 Z"
    cid = uid("rb")
    s += f'<defs><clipPath id="{cid}"><path d="{reb}"/></clipPath></defs><path d="{reb}" fill="url(#{g}rb)"/>'
    s += f'<g clip-path="url(#{cid})">' + "".join(f'<path d="M{-200+i*10},-860 C{-196+i*10.2},-720 {-200+i*10.4},-600 {-206+i*10.8},-460" stroke="{REB[i%4]}" stroke-width="2.5" fill="none" opacity="0.5"/>' for i in range(41))
    s += "".join(f'<path d="M{-110+j*55},-790 C{-104+j*56},-700 {-110+j*58},-580 {-118+j*60},-470" stroke="#03060f" stroke-width="16" fill="none" opacity="0.4" filter="url(#blur1)"/>' for j in range(5)) + "</g>"
    for i in range(41):
        xx = -170 + i * 8.5
        s += f'<path d="M{xx:.0f},{-478 + (1-abs(xx)/172)*84:.0f} l{(i%3)-1},{30+(i%4)*7}" stroke="#1f2d52" stroke-width="3"/>'
    if rim:
        s += f'<path d="{reb}" stroke="{rim}" stroke-width="6" fill="none" opacity="0.55" filter="url(#blur1)"/>'
        s += f'<path d="M66,-585 C92,-450 168,-230 230,-10 M-66,-585 C-92,-450 -170,-230 -250,-8" stroke="{rim}" stroke-width="7" fill="none" opacity="0.5" filter="url(#blur1)"/>'
    return f'<g transform="translate({x},{y}) scale({k})">{s}</g>'


# ------------------------------------------------------------------ bust
def mulata_bust(x, y, k=1.0, look=0.0, smile=0.5, lids=0.2, rim="#9fc2e8", turn=0.0, herbs=False, eyes_closed=False):
    """Head and shoulders; head centre at (x,y); k=1 -> face ~245px tall. Wide embroidered neckline + rebozo."""
    g = uid("b"); sk = SKIN
    s = (f'<defs>{grad_lin(g+"bl", [(0, "#7d7466", 1), (0.45, "#d8cfbb", 1), (0.8, "#f2e9d6", 1), (1, "#d8cfbb", 1)], -320, 0, 320, 0)}'
         f'{grad_lin(g+"sk", [(0, sk["deep"], 1), (0.4, sk["shadow"], 1), (0.75, sk["base"], 1), (1, sk["shadow"], 1)], -240, 0, 240, 0)}'
         f'{grad_lin(g+"rb", [(0, "#0c1228", 1), (0.6, "#1d2a4e", 1), (1, "#334678", 1)], -330, 200, 200, 600)}'
         f'<clipPath id="{g}rc"><path d="M-370,660 C-370,440 -330,300 -250,236 C-210,206 -170,196 -130,196 C-90,250 -40,320 16,420 C66,520 104,600 120,660 Z"/></clipPath></defs>')
    # skin: neck flaring into shoulders and upper chest
    s += f'<path d="M-46,40 C-46,100 -60,150 -150,180 C-210,196 -250,214 -270,240 L270,240 C250,214 210,196 150,180 C66,150 46,100 46,40 Z" fill="url(#{g}sk)"/>'
    s += f'<path d="M-46,60 C-30,110 30,110 46,60 L46,40 L-46,40 Z" fill="{sk["deep"]}" opacity="0.55" filter="url(#blur1)"/>'
    s += f'<path d="M-60,176 Q-30,196 -6,184 M60,176 Q30,196 6,184" stroke="{sk["deep"]}" stroke-width="3" fill="none" opacity="0.45"/>'
    s += f'<path d="M-150,182 C-90,168 -60,150 -48,120" stroke="{sk["hi"]}" stroke-width="3" fill="none" opacity="0.25"/>'
    # blouse with a wide gathered neckline
    s += (f'<path d="M-240,214 C-160,250 -80,262 0,262 C80,262 160,250 240,214 C300,250 340,360 360,660 L-360,660 C-340,360 -300,250 -240,214 Z" fill="url(#{g}bl)"/>')
    s += f'<path d="M-240,214 C-160,250 -80,262 0,262 C80,262 160,250 240,214" stroke="#ebe2cf" stroke-width="12" fill="none"/>'
    for i in range(21):
        t = i / 20; px = -230 + 460 * t; py = 222 + 44 * math.sin(math.pi * t) ** 0.8
        col = ["#b3122e", "#2f4a9a", "#e2a11b"][i % 3]
        s += f'<circle cx="{px:.0f}" cy="{py+12:.0f}" r="6.5" fill="{col}"/><circle cx="{px-8:.0f}" cy="{py+20:.0f}" r="3" fill="#3a7a3a"/><circle cx="{px+8:.0f}" cy="{py+20:.0f}" r="3" fill="#3a7a3a"/>'
    for i in range(26):
        t = i / 25; px = -226 + 452 * t; py = 236 + 44 * math.sin(math.pi * t) ** 0.8
        s += f'<path d="M{px:.0f},{py+14:.0f} q{(t-0.5)*30:.0f},40 {(t-0.5)*50:.0f},90" stroke="#a49a86" stroke-width="2.5" fill="none" opacity="0.5"/>'
    for d in ["M190,300 Q180,460 210,660", "M120,350 Q128,490 106,660", "M260,280 Q282,360 290,660"]:
        s += f'<path d="{d}" stroke="#a49a86" stroke-width="7" fill="none" opacity="0.45"/>'
    # rebozo over the left shoulder
    s += f'<path d="M-370,660 C-370,440 -330,300 -250,236 C-210,206 -170,196 -130,196 C-90,250 -40,320 16,420 C66,520 104,600 120,660 Z" fill="url(#{g}rb)"/>'
    s += f'<g clip-path="url(#{g}rc)">' + "".join(
        f'<path d="M{-390+i*30},{190+i*16} C{-310+i*30},{320+i*16} {-180+i*30},{480+i*16} {-90+i*30},{680+i*16}" stroke="{REB[i%4]}" stroke-width="{2.5 if i%2 else 4.5}" fill="none" opacity="0.55"/>'
        for i in range(-4, 18))
    for i in range(5):
        s += f'<path d="M{-310+i*70},{320+i*20} C{-250+i*70},{400+i*20} {-210+i*70},{490+i*20} {-190+i*70},660" stroke="#05081a" stroke-width="18" fill="none" opacity="0.35" filter="url(#blur1)"/>'
    s += "</g>"
    s += f'<path d="M-130,196 C-90,250 -40,320 16,420 C66,520 104,600 120,660" stroke="#070b1c" stroke-width="10" fill="none" opacity="0.75"/>'
    s += f'<path d="M-132,200 C-92,254 -42,324 14,424" stroke="#8fa6d8" stroke-width="3" fill="none" opacity="0.45"/>'
    if rim:
        s += f'<path d="M-250,236 C-330,300 -370,440 -370,660" stroke="{rim}" stroke-width="5" fill="none" opacity="0.45" filter="url(#blur1)"/>'
    s += head(look, smile, lids, rim, turn=turn, eyes_closed=eyes_closed, neck=False)
    if herbs:
        s += herb_bundle(190, 560, 1.35, -12)
    return f'<g transform="translate({x},{y}) scale({k})">{s}</g>'


# ------------------------------------------------------------------ full figure (feet at 0,0; height ~1000 units)
def mulata_full(x, y, h=900, look=0.0, rim="#9fc2e8", props="herbs", pose="stand", skirt="#26355e", skirt_dk="#111833",
                skirt_hi="#4a5f96", flip=False, turn=0.0, shade=0.35):
    """Full figure: headwrap, embroidered blouse, rebozo draped over shoulders and arms, long skirt.
    props: 'herbs' | 'charcoal' | None.  pose: 'stand' | 'step' | 'reach' (right arm up to a wall)."""
    g = uid("m"); k = h / 1000.0; sk = SKIN
    d = (f'<defs>{grad_lin(g+"sk", [(0, skirt_dk, 1), (0.45, skirt, 1), (0.75, skirt_hi, 1), (1, skirt, 1)], -240, 0, 240, 0)}'
         f'{grad_lin(g+"bl", [(0, "#8a8172", 1), (0.6, "#e6dcc8", 1), (1, "#f2ead8", 1)], -80, 0, 80, 0)}'
         f'{grad_lin(g+"rb", [(0, "#0b1129", 1), (0.55, "#1d2a4e", 1), (1, "#394d84", 1)], -170, 0, 170, 0)}'
         f'{grad_lin(g+"sh", [(0, "#000", shade), (0.55, "#000", 0), (1, "#000", 0)], -240, 0, 240, 0)}</defs>')
    s = d
    sw = 50 if pose == "step" else 0
    # skirt with a softly scalloped hem
    hem = " ".join(f"{-232-sw + (464+sw*0.6)*t:.0f},{-6 + 10*math.sin(t*math.pi*7) + 14*math.sin(t*math.pi):.0f}" for t in [i/24 for i in range(25)])
    skirt_d = f"M-66,-585 C-92,-450 -168,-230 -{232+sw},-8 L{hem} C168,-230 92,-450 66,-585 Z"
    s += f'<path d="{skirt_d}" fill="url(#{g}sk)"/>'
    for i, (xa, xb) in enumerate([(-50, -160), (-25, -92), (0, -12), (25, 62), (50, 146), (-62, -214), (60, 205)]):
        s += f'<path d="M{xa},-570 C{xa+(xb-xa)*0.25:.0f},-380 {xb*0.88:.0f},-200 {xb},4" stroke="{skirt_dk}" stroke-width="{13 if i%2 else 8}" fill="none" opacity="0.5"/>'
        s += f'<path d="M{xa+9},-570 C{xa+9+(xb-xa)*0.25:.0f},-380 {xb*0.88+11:.0f},-200 {xb+13},4" stroke="{skirt_hi}" stroke-width="3" fill="none" opacity="0.35"/>'
    s += f'<path d="M-{230+sw},-12 L{hem}" stroke="#9c1a2a" stroke-width="13" fill="none" opacity="0.9" transform="translate(0,-8)"/>'
    s += f'<path d="M-{228+sw},-34 L{hem}" stroke="#e2a11b" stroke-width="4" fill="none" stroke-dasharray="6 10" opacity="0.8" transform="translate(0,-30)"/>'
    s += f'<ellipse cx="-44" cy="10" rx="30" ry="11" fill="{sk["shadow"]}"/><ellipse cx="{48+sw}" cy="12" rx="30" ry="11" fill="{sk["deep"]}"/>'
    # torso (only the front panel shows between the rebozo edges)
    torso = "M-64,-585 C-70,-660 -84,-730 -96,-790 C-70,-814 -40,-826 0,-828 C40,-826 70,-814 96,-790 C84,-730 70,-660 64,-585 C30,-576 -30,-576 -64,-585 Z"
    s += f'<path d="{torso}" fill="url(#{g}bl)"/>'
    s += f'<path d="M-52,-818 C-32,-778 32,-778 52,-818" stroke="#d9cfba" stroke-width="6" fill="none"/>'
    for i in range(9):
        t = i / 8; px = -50 + 100 * t; py = -818 + 32 * math.sin(math.pi * t)
        s += f'<circle cx="{px:.0f}" cy="{py+7:.0f}" r="4" fill="{["#b3122e", "#2f4a9a", "#e2a11b"][i%3]}"/>'
    for i in range(6):
        s += f'<path d="M{-30+i*12},-770 q{(i-2.5)*3},60 {(i-2.5)*5},150" stroke="#a49a86" stroke-width="2" fill="none" opacity="0.5"/>'
    s += f'<path d="M-68,-600 C-30,-588 30,-588 68,-600 L66,-572 C30,-562 -30,-562 -66,-572 Z" fill="#8c2a1d"/>'
    # raised arm (behind the rebozo edge) for 'reach'
    if pose == "reach":
        s += f'<path d="M70,-790 C110,-830 150,-880 186,-930 C196,-944 218,-934 212,-918 C182,-866 140,-806 100,-764 Z" fill="url(#{g}bl)"/>'
        s += f'<path d="M186,-930 C204,-958 222,-982 236,-1004 C242,-1014 256,-1008 252,-996 C240,-970 224,-942 208,-914 Z" fill="{sk["base"]}"/>'
        s += f'<g transform="translate(244,-1008) rotate(-58) scale(0.34)"><path d="M0,-22 C30,-30 70,-30 92,-24 C120,-18 150,-12 156,0 C150,10 120,8 96,10 C80,30 50,40 20,30 C6,26 -4,16 -4,6 Z" fill="{sk["base"]}"/></g>'
        if props == "charcoal":
            s += '<rect x="250" y="-1036" width="26" height="10" rx="4" fill="#111" transform="rotate(-50 262 -1030)"/>'
    # rebozo: over shoulders and arms, hanging to the hips, crossing loosely in front
    reb = ("M-30,-836 C-70,-834 -104,-812 -124,-770 C-150,-700 -164,-600 -170,-500 L-152,-488 C-120,-500 -90,-500 -70,-492 "
           "C-64,-560 -56,-640 -40,-700 C-30,-740 -36,-790 -30,-836 Z")
    reb_r = ("M30,-836 C70,-834 104,-812 124,-770 C150,-700 164,-600 170,-500 L152,-488 C120,-500 90,-500 70,-492 "
             "C64,-560 56,-640 40,-700 C30,-740 36,-790 30,-836 Z")
    if pose == "reach":
        reb_r = ("M30,-836 C70,-834 104,-812 124,-780 C140,-740 150,-690 156,-620 L128,-610 C110,-640 96,-680 80,-720 C60,-760 40,-800 30,-836 Z")
    s += f'<path d="M-30,-836 C-10,-846 10,-846 30,-836 L30,-820 C10,-826 -10,-826 -30,-820 Z" fill="url(#{g}rb)"/>'
    for rp, sd in ((reb, -1), (reb_r, 1)):
        cid = uid("rc")
        s += f'<defs><clipPath id="{cid}"><path d="{rp}"/></clipPath></defs><path d="{rp}" fill="url(#{g}rb)"/>'
        s += f'<g clip-path="url(#{cid})">' + "".join(
            f'<path d="M{sd*(10+i*7)},-850 C{sd*(30+i*7.5)},-740 {sd*(40+i*8)},-620 {sd*(36+i*8.6)},-480" stroke="{REB[i%4]}" stroke-width="2.4" fill="none" opacity="0.55"/>'
            for i in range(20))
        s += "".join(f'<path d="M{sd*(60+j*30)},-800 C{sd*(80+j*30)},-700 {sd*(84+j*28)},-600 {sd*(80+j*30)},-490" stroke="#03060f" stroke-width="10" fill="none" opacity="0.35" filter="url(#blur1)"/>' for j in range(3))
        s += "</g>"
        s += f'<path d="{rp}" stroke="#070b1c" stroke-width="3" fill="none" opacity="0.6"/>'
    if pose != "reach":
        for i in range(18):
            s += f'<path d="M{-168+i*5.4:.0f},{-496+ (i*0.6):.0f} l{(i%3)-1},{30+(i%4)*7}" stroke="#1f2d52" stroke-width="3"/>'
            s += f'<path d="M{72+i*5.4:.0f},{-492 - (i*0.2):.0f} l{(i%3)-1},{30+(i%4)*7}" stroke="#1f2d52" stroke-width="3"/>'
        # right hand peeking out holding the rebozo edge
        s += fist(80, -556, 0.5, shade=True)
    else:
        for i in range(18):
            s += f'<path d="M{-168+i*5.4:.0f},{-496+ (i*0.6):.0f} l{(i%3)-1},{30+(i%4)*7}" stroke="#1f2d52" stroke-width="3"/>'
    # left hand at the chest holding herbs / charcoal
    if props == "herbs":
        s += herb_bundle(-30, -742, 0.7, 8)
    s += fist(-38, -686, 0.62)
    if props == "charcoal" and pose != "reach":
        s += '<rect x="-30" y="-706" width="26" height="10" rx="4" fill="#111" transform="rotate(-30 -18 -700)"/>'
    # global shading on the shadow side
    cid = uid("sil")
    s += f'<defs><clipPath id="{cid}"><path d="{skirt_d}"/><path d="{torso}"/><path d="{reb}"/><path d="{reb_r}"/></clipPath></defs>'
    s += f'<rect x="-300" y="-900" width="600" height="930" fill="url(#{g}sh)" clip-path="url(#{cid})"/>'
    if rim:
        s += f'<path d="{reb}" stroke="{rim}" stroke-width="5" fill="none" opacity="0.45" filter="url(#blur1)"/>'
        s += f'<path d="M-66,-585 C-92,-450 -168,-230 -{232+sw},-8" stroke="{rim}" stroke-width="6" fill="none" opacity="0.5" filter="url(#blur1)"/>'
    # neck + head (face 245 -> ~120 units)
    s += f'<path d="M-20,-860 L-22,-828 L22,-828 L20,-860 Z" fill="{sk["shadow"]}"/>'
    s += f'<g transform="translate(0,-902) scale(0.48)">{head(look, 0.5, 0.2, rim, turn=turn)}</g>'
    fl = " scale(-1,1)" if flip else ""
    return f'<g transform="translate({x},{y}) scale({k}){fl}">{s}</g>'


def mulata_back(x, y, k=1.0, turn=0.5, rim="#ffd27a"):
    """Over-the-shoulder: her back (rebozo) toward us, head turned to look back at the viewer over her
    right shoulder (viewer's right). Head centre at (x,y); k=1 -> face ~245px."""
    g = uid("bk"); sk = SKIN
    back = ("M-470,760 C-460,520 -420,380 -320,300 C-240,240 -140,200 -60,150 L-40,90 L70,90 C90,150 150,190 230,226 "
            "C330,280 400,420 420,760 Z")
    s = (f'<defs>{grad_lin(g+"rb", [(0, "#070c1e", 1), (0.6, "#16223f", 1), (1, "#2a3c68", 1)], -470, 0, 420, 0)}'
         f'<clipPath id="{g}c"><path d="{back}"/></clipPath></defs>')
    # neck (seen from behind/side)
    s += f'<path d="M-46,60 C-50,110 -60,150 -70,190 L90,190 C80,150 70,110 60,60 Z" fill="{sk["shadow"]}"/>'
    s += f'<path d="{back}" fill="url(#{g}rb)"/>'
    s += f'<g clip-path="url(#{g}c)">' + "".join(
        f'<path d="M{-500+i*24},120 C{-470+i*24},320 {-450+i*24},540 {-470+i*24},780" stroke="{REB[i%4]}" stroke-width="{2.5 if i%2 else 4}" fill="none" opacity="0.5"/>'
        for i in range(42))
    for i in range(6):
        s += f'<path d="M{-330+i*120},250 C{-300+i*120},400 {-320+i*120},560 {-340+i*120},780" stroke="#03060f" stroke-width="26" fill="none" opacity="0.4" filter="url(#blur1)"/>'
    s += "</g>"
    if rim:
        s += f'<path d="M230,226 C330,280 400,420 420,760" stroke="{rim}" stroke-width="9" fill="none" opacity="0.8" filter="url(#blur1)"/>'
        s += f'<path d="M-60,150 C-140,200 -240,240 -320,300 C-420,380 -460,520 -470,760" stroke="{rim}" stroke-width="7" fill="none" opacity="0.55" filter="url(#blur1)"/>'
    # curls at the nape spilling over the rebozo
    s += curls([(-80, 80, 14), (-70, 170, 18), (10, 190, 16), (70, 150, 12)], 41, 12, 18)
    s += head(look=-0.7, smile=0.65, lids=0.25, rim=rim, turn=turn, back_curls=True)
    # far shoulder edge rising under the chin (foreground)
    s += f'<path d="M120,200 C200,210 300,250 360,320 C420,400 440,560 440,760 L300,760 C300,600 280,460 220,360 C180,300 140,260 110,240 Z" fill="#0b1228"/>'
    s += "".join(f'<path d="M{130+i*20},{230+i*6} C{200+i*20},{300+i*10} {260+i*18},{420+i*6} {300+i*16},760" stroke="{REB[i%4]}" stroke-width="3" fill="none" opacity="0.45"/>' for i in range(8))
    if rim:
        s += f'<path d="M120,200 C200,210 300,250 360,320 C420,400 440,560 440,760" stroke="{rim}" stroke-width="7" fill="none" opacity="0.85" filter="url(#blur1)"/>'
    return f'<g transform="translate({x},{y}) scale({k})">{s}</g>'


# ------------------------------------------------------------------ other characters
def male_profile(kind="jailer", rim="#ffd27a", mouth_open=0.0, lit="#e09a5a"):
    """Male head in profile facing +x. kind: 'jailer' (balding, stubble) | 'alcalde' (mustache, goatee). Centre (0,0), ~250 tall."""
    g = uid("mp")
    base, sh, dp = ("#b98a68", "#7a553e", "#3e2a1e") if kind == "jailer" else ("#c79c7c", "#80604a", "#3a2a20")
    prof = ("M10,-130 C50,-126 70,-100 74,-60 C76,-44 82,-36 84,-28 C80,-22 76,-18 78,-10 C90,8 104,30 106,44 "
            "C108,54 98,58 88,56 C84,62 86,66 84,70 C88,74 90,80 86,84 "
            f"C84,{90+mouth_open*14:.0f} 80,{92+mouth_open*14:.0f} 82,{96+mouth_open*14:.0f} C86,{108+mouth_open*14:.0f} 82,{122+mouth_open*14:.0f} 64,{130+mouth_open*12:.0f} "
            "C46,136 30,138 20,150 L26,240 L-80,240 C-76,180 -80,120 -90,80 C-104,20 -110,-40 -96,-80 C-80,-120 -40,-134 10,-130 Z")
    s = f'<defs>{grad_lin(g+"f", [(0, dp, 1), (0.5, sh, 1), (0.85, base, 1), (1, lit, 1)], -90, 0, 110, 0)}</defs>'
    s += f'<path d="{prof}" fill="url(#{g}f)"/>'
    s += f'<path d="M-30,20 C-10,80 20,118 60,{124+mouth_open*10:.0f}" stroke="{dp}" stroke-width="5" fill="none" opacity="0.4" filter="url(#blur1)"/>'
    # ear
    s += f'<path d="M-30,-20 C-48,-26 -52,14 -36,30 C-26,36 -18,26 -20,12 C-16,0 -18,-16 -30,-20 Z" fill="{sh}"/>'
    # eye + heavy brow
    s += f'<path d="M66,-24 Q56,-30 46,-24 Q56,-16 66,-22 Z" fill="#d8c8b0"/><circle cx="{60 if mouth_open < 0.5 else 58}" cy="-23" r="3.6" fill="#140a06"/>'
    s += f'<path d="M70,-26 Q56,-36 42,-26" stroke="#1a0f08" stroke-width="3.5" fill="none"/>'
    brow_y = -44 if mouth_open < 0.5 else -52
    s += f'<path d="M36,{brow_y+4} Q56,{brow_y-6} 80,{brow_y+2}" stroke="{"#cfc6b8" if kind == "jailer" else "#1a1210"}" stroke-width="9" fill="none" stroke-linecap="round"/>'
    s += f'<path d="M40,-12 Q56,-4 70,-12" stroke="{dp}" stroke-width="2" fill="none" opacity="0.6"/>'
    s += f'<path d="M88,56 C80,52 74,46 76,38" stroke="{dp}" stroke-width="3" fill="none" opacity="0.8"/>'
    if mouth_open > 0.1:
        s += f'<path d="M84,72 C76,74 72,{80+mouth_open*10:.0f} 82,{88+mouth_open*14:.0f}" fill="#2a0e0a"/>'
    else:
        s += f'<path d="M86,78 L70,80" stroke="#2a120c" stroke-width="2.6" stroke-linecap="round"/>'
    if kind == "jailer":
        # balding: grey fringe, stubble
        s += f'<path d="M-96,-80 C-110,-40 -104,20 -90,60 C-80,40 -70,0 -60,-30 C-50,-60 -60,-80 -96,-80 Z" fill="#9a948a"/>'
        r = random.Random(5)
        s += "".join(f'<circle cx="{r.uniform(10,100):.0f}" cy="{r.uniform(60,140):.0f}" r="1.6" fill="#6a6058" opacity="0.8"/>' for _ in range(160) if True)
        s += f'<path d="M-2,-132 C40,-128 64,-108 72,-78" stroke="{lit}" stroke-width="3" fill="none" opacity="0.5"/>'
    else:
        s += f'<path d="M-96,-80 C-112,-40 -110,30 -92,80 C-70,60 -60,0 -50,-40 C-40,-80 -20,-110 10,-126 C-40,-132 -80,-116 -96,-80 Z" fill="#1c140f"/>'
        s += f'<path d="M86,64 C70,60 56,66 50,78 C64,72 76,74 92,80 C100,84 106,80 104,74 C100,68 94,64 86,64 Z" fill="#1a1210"/>'
        s += f'<path d="M70,96 C80,100 86,120 80,144 C70,140 62,120 64,100 Z" fill="#1a1210"/>'
    if rim:
        s += f'<path d="{prof.split(" L26,240")[0]}" stroke="{rim}" stroke-width="4" fill="none" opacity="0.85" filter="url(#blur1)"/>'
    return s


def jailer(x, y, h=900, mouth_open=0.0, lantern=True, rim="#ffd27a", facing=1, lantern_up=False):
    """Old jailer, profile facing +x (or -x with facing=-1): loose shirt, leather vest, rope belt, keys, lantern."""
    g = uid("j"); k = h / 1000.0
    s = (f'<defs>{grad_lin(g+"sh", [(0, "#2b241c", 1), (0.6, "#6d6152", 1), (1, "#a39380", 1)], -120, 0, 140, 0)}'
         f'{grad_lin(g+"v", [(0, "#120c08", 1), (1, "#4a3020", 1)], -120, 0, 120, 0)}'
         f'{grad_lin(g+"t", [(0, "#0e0b09", 1), (1, "#3a3028", 1)], -100, 0, 100, 0)}</defs>')
    # legs / trousers (slightly bent, hunched old man)
    s += f'<path d="M-70,-470 C-80,-320 -90,-160 -96,-10 L-40,-6 C-30,-150 -10,-300 0,-420 C14,-300 34,-160 50,-8 L104,-12 C96,-170 82,-330 70,-470 Z" fill="url(#{g}t)"/>'
    s += f'<path d="M-104,-12 C-110,0 -60,8 -36,0 L-38,-14 Z M44,-12 C40,2 100,8 118,-2 L106,-16 Z" fill="#1a120c"/>'
    # torso (hunched forward) with sloped shoulders
    torso = "M-76,-470 C-92,-560 -104,-660 -96,-740 C-90,-790 -40,-818 20,-820 C70,-818 104,-780 108,-720 C112,-640 100,-540 80,-470 Z"
    s += f'<path d="{torso}" fill="url(#{g}sh)"/>'
    s += f'<path d="M-96,-730 C-80,-640 -80,-560 -76,-470 L-20,-470 C-14,-580 -24,-690 -30,-800 C-60,-800 -86,-770 -96,-730 Z" fill="url(#{g}v)"/>'
    s += f'<path d="M50,-814 C66,-700 70,-570 64,-470 L84,-470 C102,-560 112,-650 106,-730 C100,-780 76,-808 50,-814 Z" fill="url(#{g}v)"/>'
    s += f'<path d="M-10,-818 C10,-790 30,-780 50,-800" stroke="#4a3f33" stroke-width="5" fill="none"/>'
    s += f'<path d="M-80,-500 C-20,-486 40,-486 84,-500" stroke="#6a5a3a" stroke-width="12" fill="none"/>'
    # keys ring hanging at the belt
    s += f'<circle cx="-40" cy="-450" r="26" stroke="#8a7a5a" stroke-width="5" fill="none"/>'
    for i, a in enumerate((-30, 0, 30, 60)):
        ax = -40 + 26 * math.sin(math.radians(a)); ay = -450 + 26 * math.cos(math.radians(a))
        s += f'<path d="M{ax:.0f},{ay:.0f} l{-6+i*4},70 m-6,0 l14,0 m-12,-12 l12,0" stroke="#9a8a62" stroke-width="5" fill="none" stroke-linecap="round"/>'
    # arm with lantern held forward
    if lantern:
        ly = -700 if lantern_up else -560
        s += f'<path d="M40,-790 C100,-740 132,{ly+30} 168,{ly-16} L194,{ly+16} C150,{ly+70} 96,-680 40,-690 Z" fill="url(#{g}sh)"/>'
        s += f'<path d="M40,-790 C100,-740 132,{ly+30} 168,{ly-16}" stroke="#1a140e" stroke-width="3" fill="none" opacity="0.5"/>'
        s += f'<ellipse cx="184" cy="{ly}" rx="20" ry="16" fill="#9a6a48"/>'
        s += f'<path d="M184,{ly} L184,{ly+30}" stroke="#1a120c" stroke-width="4"/>'
        lx, lyy = 184, ly + 30
        s += f'<circle cx="{lx}" cy="{lyy+70}" r="200" fill="url(#warmglow)" opacity="0.85"/>'
        s += (f'<path d="M{lx-34},{lyy+20} L{lx+34},{lyy+20} L{lx+28},{lyy+110} L{lx-28},{lyy+110} Z" fill="#ffd98a"/>'
              f'<path d="M{lx-40},{lyy+20} L{lx+40},{lyy+20} L{lx},{lyy-10} Z M{lx-34},{lyy+108} L{lx+34},{lyy+108} L{lx+30},{lyy+124} L{lx-30},{lyy+124} Z" fill="#1a120c"/>'
              f'<path d="M{lx-30},{lyy+20} L{lx-26},{lyy+110} M{lx+30},{lyy+20} L{lx+26},{lyy+110} M{lx},{lyy+20} L{lx},{lyy+110}" stroke="#1a120c" stroke-width="5"/>'
              f'<path d="M{lx},{lyy+40} Q{lx+10},{lyy+70} {lx},{lyy+90} Q{lx-10},{lyy+70} {lx},{lyy+40} Z" fill="#fff6d8"/>')
    s = s.replace('<path d="M-76,-470 C-80,-320', '<path d="M-76,-470 C-80,-320')
    head = f'<g transform="translate(46,-900) scale(0.6)">{male_profile("jailer", rim, mouth_open)}</g>'
    s = s.replace(f'<path d="{torso}"', head + f'<path d="{torso}"', 1)
    fl = "" if facing > 0 else " scale(-1,1)"
    return f'<g transform="translate({x},{y}) scale({k}){fl}">{s}</g>'


def alcalde(x, y, h=950, rim="#9fc2e8", facing=1, hat_in_hand=False, lit="#e0a070"):
    """17th-c. alcalde: black doublet, white golilla collar, cape, plumed wide hat, cane. Profile facing +x."""
    g = uid("a"); k = h / 1000.0
    s = (f'<defs>{grad_lin(g+"c", [(0, "#050506", 1), (0.7, "#15151c", 1), (1, "#2a2a36", 1)], -200, 0, 160, 0)}'
         f'{grad_lin(g+"d", [(0, "#0b0b0e", 1), (1, "#30303c", 1)], -100, 0, 100, 0)}</defs>')
    # legs with stockings and shoes
    s += f'<path d="M-50,-440 C-56,-300 -60,-160 -58,-10 L-26,-8 C-22,-160 -14,-300 -6,-420 L6,-420 C14,-300 22,-160 30,-10 L62,-10 C64,-160 60,-300 54,-440 Z" fill="#141419"/>'
    s += f'<path d="M-70,-8 C-74,6 -20,8 -20,-4 Z M22,-8 C20,6 80,8 86,-4 Z" fill="#050506"/><circle cx="-40" cy="-6" r="7" fill="#c9a24a"/><circle cx="50" cy="-6" r="7" fill="#c9a24a"/>'
    # breeches
    s += f'<path d="M-66,-560 C-80,-500 -76,-450 -60,-420 L66,-420 C80,-450 80,-500 66,-560 Z" fill="url(#{g}d)"/>'
    # doublet (jubón) with buttons
    s += f'<path d="M-70,-800 C-90,-720 -84,-620 -70,-540 L72,-540 C88,-620 90,-720 70,-800 C30,-820 -30,-820 -70,-800 Z" fill="url(#{g}d)"/>'
    s += "".join(f'<circle cx="18" cy="{-780+i*28}" r="5" fill="#c9a24a"/>' for i in range(9))
    s += f'<path d="M-70,-560 L72,-560 L66,-530 L-64,-530 Z" fill="#7a1a1a"/>'
    # cape over the back shoulder
    s += f'<path d="M-60,-810 C-140,-760 -170,-600 -180,-380 C-130,-370 -90,-380 -60,-400 C-50,-560 -40,-700 -20,-800 Z" fill="url(#{g}c)"/>'
    # golilla (flat white collar)
    s += f'<path d="M-60,-830 C-20,-850 50,-850 90,-830 L84,-806 C40,-816 -20,-816 -56,-806 Z" fill="#ece6d8"/>'
    # arm with cane (front)
    s += f'<path d="M50,-790 C90,-720 110,-640 120,-560 L96,-556 C84,-630 66,-700 36,-760 Z" fill="url(#{g}d)"/>'
    s += f'<ellipse cx="112" cy="-548" rx="18" ry="14" fill="#c79c7c"/>'
    s += f'<path d="M118,-560 L150,-8" stroke="#2a1a10" stroke-width="10" stroke-linecap="round"/><circle cx="118" cy="-566" r="12" fill="#c9a24a"/>'
    # head
    s = s.replace('<path d="M-70,-800 C-90,-720', f'<g transform="translate(14,-925) scale(0.54)">{male_profile("alcalde", rim, 0.0, lit)}</g><path d="M-70,-800 C-90,-720', 1)
    # hat
    if hat_in_hand:
        s += f'<g transform="translate(-60,-560) rotate(-80)"><ellipse cx="0" cy="0" rx="110" ry="22" fill="#0a0a0d"/><path d="M-50,-4 C-50,-60 50,-60 50,-4 Z" fill="#0a0a0d"/></g>'
    else:
        s += f'<ellipse cx="14" cy="-985" rx="124" ry="21" fill="#0a0a0d"/><path d="M-44,-990 C-48,-1050 70,-1056 70,-990 Z" fill="#0a0a0d"/>'
        s += f'<path d="M-34,-1026 C-74,-1066 -134,-1046 -154,-996 C-114,-1026 -74,-1026 -44,-1006 Z" fill="#e8e0d0" opacity="0.9"/>'
    if rim:
        s += f'<path d="M-60,-810 C-140,-760 -170,-600 -180,-380 M-50,-440 C-56,-300 -60,-160 -58,-10" stroke="{rim}" stroke-width="6" fill="none" opacity="0.55" filter="url(#blur1)"/>'
    fl = "" if facing > 0 else " scale(-1,1)"
    return f'<g transform="translate({x},{y}) scale({k}){fl}">{s}</g>'


def hooded(x, y, h=1100, rim="#c0141a", eyes=False, candle=False, cross=False, seed=1, lean=0.0):
    """Tall hooded figure of the Holy Office: long robe, deep hood with darkness inside, rim light."""
    g = uid("hd"); k = h / 1000.0; r = random.Random(seed)
    s = f'<defs>{grad_lin(g+"r", [(0, "#020203", 1), (0.6, "#0d0b0e", 1), (1, "#1e1a20", 1)], -200, 0, 200, 0)}</defs>'
    robe = (f"M0,-1000 C-60,-996 -96,-950 -104,-880 C-110,-830 -140,-800 -170,-760 C-200,-560 -220,-300 -250,0 "
            f"L250,0 C220,-300 200,-560 170,-760 C140,-800 110,-830 104,-880 C96,-950 60,-996 0,-1000 Z")
    s += f'<path d="{robe}" fill="url(#{g}r)" transform="skewX({lean})"/>'
    s += f'<path d="M-60,-930 C-60,-880 -40,-840 0,-830 C40,-840 60,-880 60,-930 C50,-960 -50,-960 -60,-930 Z" fill="#000"/>'
    for i in range(6):
        xx = r.uniform(-180, 180)
        s += f'<path d="M{xx*0.5:.0f},-760 C{xx*0.7:.0f},-500 {xx*0.9:.0f},-260 {xx:.0f},0" stroke="#000" stroke-width="{r.uniform(6,14):.0f}" fill="none" opacity="0.6"/>'
    if eyes:
        s += '<circle cx="-18" cy="-890" r="5" fill="#ffb08a" opacity="0.8"/><circle cx="18" cy="-890" r="5" fill="#ffb08a" opacity="0.8"/>'
    if cross:
        s += '<path d="M-14,-700 L14,-700 L14,-640 L44,-640 L44,-612 L14,-612 L14,-520 L-14,-520 L-14,-612 L-44,-612 L-44,-640 L-14,-640 Z" fill="#1f5a2a" stroke="#2e7a3a" stroke-width="3"/>'
    if candle:
        s += f'<circle cx="60" cy="-560" r="160" fill="url(#warmglow)" opacity="0.8"/><rect x="52" y="-560" width="16" height="70" fill="#e8dcc0"/><path d="M60,-600 Q70,-578 60,-562 Q50,-578 60,-600 Z" fill="#ffdf8a"/>'
        s += '<path d="M30,-500 C50,-520 80,-520 96,-500 C80,-480 50,-480 30,-500 Z" fill="#1a1416"/>'
    if rim:
        s += f'<path d="{robe}" stroke="{rim}" stroke-width="7" fill="none" opacity="0.7" filter="url(#blur1)" transform="skewX({lean})"/>'
    return f'<g transform="translate({x},{y}) scale({k})">{s}</g>'


def villager(x, y, h=600, kind="woman", color="#07080b", rim=None, seed=1, facing=1, face=None):
    """Simple townsperson silhouette: woman with rebozo over the head, or man with a wide hat / brim hat."""
    k = h / 1000.0; s = ""
    if kind == "woman":
        s += ("M0,-1000 C-50,-1000 -80,-960 -84,-900 C-90,-840 -120,-800 -140,-700 C-170,-500 -200,-250 -220,0 L220,0 "
              "C200,-250 170,-500 140,-700 C120,-800 90,-840 84,-900 C80,-960 50,-1000 0,-1000 Z")
    elif kind == "man":
        s += ("M-40,-930 C-44,-980 44,-980 40,-930 L46,-880 C60,-860 110,-840 120,-780 L130,-480 L100,-470 L96,-420 "
              "L80,0 L20,0 L4,-380 L-4,-380 L-20,0 L-80,0 L-96,-420 L-100,-470 L-130,-480 L-120,-780 C-110,-840 -60,-860 -46,-880 Z")
        s += " M-150,-950 C-100,-966 100,-966 150,-950 C100,-934 -100,-934 -150,-950 Z M-46,-950 C-50,-1040 50,-1040 46,-950 Z"
    else:  # child
        s += "M0,-1000 C-60,-1000 -70,-900 -40,-860 C-90,-840 -110,-700 -120,-500 L-80,-480 L-70,0 L70,0 L80,-480 L120,-500 C110,-700 90,-840 40,-860 C70,-900 60,-1000 0,-1000 Z"
    out = ""
    if rim:
        out += f'<path d="{s}" fill="{rim}" filter="url(#blur2)" opacity="0.8"/>'
    out += f'<path d="{s}" fill="{color}"/>'
    if face and kind == "woman":
        out += (f'<path d="M-6,-930 C30,-934 50,-900 48,-860 C46,-820 30,-790 4,-786 C-14,-800 -20,-880 -6,-930 Z" fill="{face}"/>'
                f'<path d="M48,-860 L60,-848 L46,-842 M44,-822 Q34,-818 30,-822" stroke="#2a150c" stroke-width="4" fill="none"/>'
                f'<path d="M28,-880 q8,-4 14,0" stroke="#1a0c06" stroke-width="5" fill="none"/>'
                f'<path d="M-6,-930 C30,-934 50,-900 48,-860" stroke="#ffcf90" stroke-width="5" fill="none" opacity="0.7"/>')
    fl = "" if facing > 0 else " scale(-1,1)"
    return f'<g transform="translate({x},{y}) scale({k}){fl}">{out}</g>'
