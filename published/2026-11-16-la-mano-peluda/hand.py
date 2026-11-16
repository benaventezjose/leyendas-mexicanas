"""The Mano Peluda: a huge, black, hairy disembodied hand drawn procedurally (palm + jointed fingers + fur + claws).
Local coords: wrist at (0,0), hand pointing up (-y). Palm ~260 wide, total ~640 tall at k=1."""
import math, random
from base_chars import uid

SKIN = "#0d0907"; SKIN_HI = "#2a201a"; FUR = "#050403"; FUR_HI = "#4a3e34"; NAIL = "#cbb478"; NAIL_DK = "#6e5a2c"

# finger spec: (base_x, base_y, angle_deg, [len1,len2,len3], [w1,w2,w3])
BASES = {"thumb": (-112, -96, -50, [88, 70, 56], [84, 70, 58]),
         "index": (-96, -262, -12, [118, 82, 66], [72, 62, 52]),
         "middle": (-32, -284, -3, [130, 90, 72], [74, 64, 54]),
         "ring": (34, -278, 7, [122, 84, 66], [70, 60, 50]),
         "pinky": (94, -246, 18, [92, 66, 54], [60, 52, 44])}
POSES = {  # bend per joint (deg, positive = curls toward palm side = clockwise when seen from back… we just add to angle)
    "reach": {"thumb": [8, 10, 6], "index": [-6, 12, 12], "middle": [0, 14, 14], "ring": [4, 16, 14], "pinky": [8, 18, 14]},
    "open": {"thumb": [-6, 4, 4], "index": [-10, 4, 4], "middle": [0, 4, 4], "ring": [8, 6, 4], "pinky": [16, 8, 6]},
    "claw": {"thumb": [20, 30, 30], "index": [10, 45, 45], "middle": [6, 50, 45], "ring": [6, 50, 45], "pinky": [8, 50, 40]},
    "grab": {"thumb": [40, 40, 30], "index": [60, 70, 50], "middle": [62, 72, 52], "ring": [64, 72, 50], "pinky": [64, 70, 46]},
    "crawl": {"thumb": [-40, 30, 30], "index": [-60, 70, 40], "middle": [-10, 80, 50], "ring": [40, 70, 40], "pinky": [70, 60, 30]},
    "cup": {"thumb": [24, 16, 10], "index": [0, 24, 22], "middle": [0, 26, 24], "ring": [4, 26, 22], "pinky": [8, 26, 20]},
}


def _finger_pts(name, bends, spread=1.0):
    bx, by, ang, ls, ws = BASES[name]
    pts = [(bx, by)]; a = ang * spread; x, y = bx, by
    for l, b in zip(ls, bends):
        a += b; r = math.radians(a)
        x += math.sin(r) * l; y -= math.cos(r) * l
        pts.append((x, y))
    return pts, ws, a


def palm_path():
    return ("M-84,0 C-100,-50 -130,-100 -142,-170 C-150,-230 -136,-270 -100,-290 C-60,-312 50,-312 104,-278 "
            "C136,-254 146,-210 138,-160 C128,-100 104,-50 86,0 Z")


def hand(pose="reach", k=1.0, rim="#9fc2e8", seed=1, hair=1.0, rim_side=-1, nails=True, wrist_fur=True, spread=1.0):
    r = random.Random(seed); g = uid("mh")
    bends = POSES[pose]; fingers = {n: _finger_pts(n, bends[n], spread) for n in BASES}
    def strokes(col, extra=0, op=1.0, filt=""):
        s = f'<path d="{palm_path()}" fill="{col}" opacity="{op}" {filt}/>'
        if extra:
            s = f'<path d="{palm_path()}" fill="{col}" stroke="{col}" stroke-width="{extra*2}" opacity="{op}" {filt}/>'
        for n, (pts, ws, a) in fingers.items():
            for i in range(3):
                (x0, y0), (x1, y1) = pts[i], pts[i + 1]
                s += f'<path d="M{x0:.1f},{y0:.1f} L{x1:.1f},{y1:.1f}" stroke="{col}" stroke-width="{ws[i]+extra:.1f}" stroke-linecap="round" opacity="{op}" {filt}/>'
        return s
    out = f'<defs><linearGradient id="{g}s" x1="-150" y1="0" x2="150" y2="0" gradientUnits="userSpaceOnUse">' \
          f'<stop offset="0" stop-color="{SKIN_HI if rim_side < 0 else SKIN}"/><stop offset="0.5" stop-color="{SKIN}"/>' \
          f'<stop offset="1" stop-color="{SKIN_HI if rim_side > 0 else SKIN}"/></linearGradient></defs>'
    # rim halo
    if rim:
        out += f'<g transform="translate({rim_side*7},-4)">{strokes(rim, extra=10, op=0.55, filt="filter=" + chr(34) + "url(#blur2)" + chr(34))}</g>'
    # fur fringe sticking out of the silhouette (drawn before body so the roots hide under it)
    fur = ""
    def fringe(x0, y0, x1, y1, w, n, outward=True):
        nonlocal fur
        dx, dy = x1 - x0, y1 - y0; L = math.hypot(dx, dy) or 1; ux, uy = dx / L, dy / L; nx, ny = -uy, ux
        for _ in range(int(n * hair)):
            t = r.random(); side = r.choice((-1, 1))
            px = x0 + dx * t + nx * side * w * 0.42; py = y0 + dy * t + ny * side * w * 0.42
            ang = math.atan2(ny * side, nx * side) + r.uniform(-0.9, 0.9) - 0.5 * math.atan2(uy, ux) * 0
            # hairs lean toward the fingertip
            hx = math.cos(ang) * 0.7 + ux * 0.6; hy = math.sin(ang) * 0.7 + uy * 0.6
            ln = r.uniform(12, 34)
            lit = rim and (side * nx * rim_side > 0.2)
            col = rim if lit and r.random() < 0.55 else FUR
            fur += (f'<path d="M{px:.1f},{py:.1f} q{hx*ln*0.5+r.uniform(-4,4):.1f},{hy*ln*0.5:.1f} {hx*ln:.1f},{hy*ln:.1f}" '
                    f'stroke="{col}" stroke-width="{r.uniform(1.4,3.2):.1f}" fill="none" stroke-linecap="round" opacity="{r.uniform(0.6,0.95):.2f}"/>')
    for n, (pts, ws, a) in fingers.items():
        for i in range(3):
            fringe(*pts[i], *pts[i + 1], ws[i] + 6, 34 if i < 2 else 16)
    # palm outline fur
    edge = [(-92, 0), (-120, -110), (-136, -200), (-100, -280), (0, -300), (96, -272), (130, -190), (110, -80), (94, 0)]
    for (a0, a1) in zip(edge, edge[1:]):
        fringe(*a0, *a1, 30, 40)
    out += fur
    out += strokes(f"url(#{g}s)")
    # knuckle bumps + skin creases
    for n, (pts, ws, a) in fingers.items():
        for i in (1, 2):
            x, y = pts[i]; ang = math.atan2(pts[i + 1][1] - y, pts[i + 1][0] - x) if i < 3 else 0
            nx, ny = -math.sin(ang), math.cos(ang)
            for j in (-1, 0, 1):
                out += (f'<path d="M{x+nx*ws[i]*0.3+math.cos(ang)*j*6:.1f},{y+ny*ws[i]*0.3+math.sin(ang)*j*6:.1f} '
                        f'L{x-nx*ws[i]*0.3+math.cos(ang)*j*6:.1f},{y-ny*ws[i]*0.3+math.sin(ang)*j*6:.1f}" stroke="#2e241c" stroke-width="2" opacity="0.7"/>')
        x, y = pts[1]
        out += f'<ellipse cx="{(pts[0][0]+x)/2:.0f}" cy="{(pts[0][1]+y)/2:.0f}" rx="{ws[0]*0.3:.0f}" ry="{ws[0]*0.22:.0f}" fill="{SKIN_HI}" opacity="0.6" filter="url(#blur1)"/>'
    # tendons on back of hand
    for x in (-70, -20, 34, 84):
        out += f'<path d="M{x*0.5:.0f},-30 Q{x*0.8:.0f},-160 {x:.0f},-260" stroke="{SKIN_HI}" stroke-width="7" fill="none" opacity="0.55" filter="url(#blur1)"/>'
    # dense fur on the back of the hand and first phalanges
    for _ in range(int(520 * hair)):
        x = r.uniform(-120, 120); y = r.uniform(-290, -10)
        if abs(x) > 128 - (y + 290) * 0.08: continue
        ln = r.uniform(10, 26); a = math.radians(r.uniform(-30, 30) - 90 + x * 0.12)
        out += (f'<path d="M{x:.0f},{y:.0f} q{math.cos(a)*ln*0.5+r.uniform(-3,3):.1f},{math.sin(a)*ln*0.5:.1f} {math.cos(a)*ln:.1f},{math.sin(a)*ln:.1f}" '
                f'stroke="{r.choice((FUR, FUR, FUR_HI, "#211a14"))}" stroke-width="{r.uniform(1.2,2.6):.1f}" fill="none" opacity="{r.uniform(0.5,0.9):.2f}" stroke-linecap="round"/>')
    for n, (pts, ws, a) in fingers.items():
        for i in range(2):
            (x0, y0), (x1, y1) = pts[i], pts[i + 1]
            for _ in range(int(40 * hair)):
                t = r.random(); px = x0 + (x1 - x0) * t + r.uniform(-ws[i] * 0.3, ws[i] * 0.3); py = y0 + (y1 - y0) * t + r.uniform(-ws[i] * 0.3, ws[i] * 0.3)
                ux, uy = (x1 - x0), (y1 - y0); L = math.hypot(ux, uy) or 1; ln = r.uniform(8, 20)
                out += f'<path d="M{px:.0f},{py:.0f} l{ux/L*ln+r.uniform(-5,5):.1f},{uy/L*ln+r.uniform(-5,5):.1f}" stroke="{r.choice((FUR, FUR_HI))}" stroke-width="1.6" opacity="0.75"/>'
    # rim line on the lit edge
    if False:
        for n, (pts, ws, a) in fingers.items():
            d = " ".join(f"{'M' if i == 0 else 'L'}{x + rim_side * w * 0.36 * math.cos(math.radians(a)):.1f},{y + rim_side * w * 0.36 * math.sin(math.radians(a)):.1f}"
                         for i, ((x, y), w) in enumerate(zip(pts, ws + [ws[-1]])))
            out += f'<path d="{d}" stroke="{rim}" stroke-width="3" fill="none" opacity="0.75" stroke-linecap="round"/>'
        side = "M-96,-10 C-106,-70 -124,-120 -136,-180 C-142,-226 -128,-262 -100,-280" if rim_side < 0 else "M92,-10 C104,-60 122,-110 130,-170 C134,-212 124,-250 96,-272"
        out += f'<path d="{side}" stroke="{rim}" stroke-width="4" fill="none" opacity="0.7"/>'
    # claws: long, yellow, curved
    if nails:
        for n, (pts, ws, a) in fingers.items():
            (xa, ya), (xb, yb) = pts[2], pts[3]
            ux, uy = xb - xa, yb - ya; L = math.hypot(ux, uy) or 1; ux, uy = ux / L, uy / L; nx, ny = -uy, ux
            w = ws[2] * 0.42; ln = 58 if n != "thumb" else 50
            tip = (xb + ux * ln + nx * 10, yb + uy * ln + ny * 10)
            d = (f"M{xb - ux*18 + nx*w:.1f},{yb - uy*18 + ny*w:.1f} Q{xb + ux*ln*0.6 + nx*w*1.1:.1f},{yb + uy*ln*0.6 + ny*w*1.1:.1f} {tip[0]:.1f},{tip[1]:.1f} "
                 f"Q{xb + ux*ln*0.5 - nx*w*0.6:.1f},{yb + uy*ln*0.5 - ny*w*0.6:.1f} {xb - ux*18 - nx*w:.1f},{yb - uy*18 - ny*w:.1f} Z")
            out += f'<path d="{d}" fill="{NAIL}" stroke="{NAIL_DK}" stroke-width="3"/>'
            out += f'<path d="M{xb + nx*w*0.3:.1f},{yb + ny*w*0.3:.1f} Q{xb + ux*ln*0.5 + nx*w*0.6:.1f},{yb + uy*ln*0.5 + ny*w*0.6:.1f} {tip[0]:.1f},{tip[1]:.1f}" stroke="#f4e8b8" stroke-width="3" fill="none" opacity="0.7"/>'
            for j in range(3):
                t = 0.2 + j * 0.25
                out += f'<path d="M{xb + ux*ln*t + nx*w*0.6:.1f},{yb + uy*ln*t + ny*w*0.6:.1f} l{-nx*w*1.0:.1f},{-ny*w*1.0:.1f}" stroke="{NAIL_DK}" stroke-width="1.5" opacity="0.6"/>'
    # wrist: a ragged ruff of fur fading into darkness (no gore)
    if wrist_fur:
        for _ in range(int(110 * hair)):
            x = r.uniform(-100, 100); ln = r.uniform(20, 60); a = math.radians(90 + r.uniform(-40, 40))
            out += f'<path d="M{x:.0f},{-r.uniform(0,30):.0f} q{math.cos(a)*ln*0.5:.1f},{math.sin(a)*ln*0.5:.1f} {math.cos(a)*ln:.1f},{math.sin(a)*ln:.1f}" stroke="{FUR}" stroke-width="{r.uniform(2,4):.1f}" fill="none" opacity="0.9"/>'
        out += '<ellipse cx="0" cy="10" rx="110" ry="40" fill="#000" opacity="0.7" filter="url(#blur2)"/>'
    return f'<g transform="scale({k})">{out}</g>'


def place(x, y, rot, k, svg_, flip=False):
    return f'<g transform="translate({x},{y}) rotate({rot}) scale({-k if flip else k},{k})">{svg_}</g>'
