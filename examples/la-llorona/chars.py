"""Custom hand-drawn characters and props for the La Llorona video (SVG fragments, 2400x1350 canvas).
Local drawing coordinates are written for a figure 1000 units tall (top of head y=0, feet y=1000, centre x=0)
and placed with translate/scale."""
import math, random

_n = [0]
def uid(p="c"):
    _n[0] += 1
    return f"{p}{_n[0]}"


def place(frag, x, y_feet, height, flip=False, rot=0):
    s = height / 1000.0
    fx = -s if flip else s
    return f'<g transform="translate({x},{y_feet - height}) rotate({rot}) scale({fx},{s})">{frag}</g>'


def drips(r, pts, color="#cfe0ee", op=0.7, size=1.0):
    out = []
    for (x, y) in pts:
        L = r.uniform(10, 26) * size; w = r.uniform(2.2, 4) * size
        out.append(f'<path d="M{x},{y} q{w},{L*0.7} 0,{L} q{-w},{-L*0.3} 0,{-L} z" fill="{color}" opacity="{op*r.uniform(0.5,1):.2f}"/>')
    return "".join(out)


def hair_strands(r, roots, length=(250, 450), sway=40, width=(2, 7), color="#030406", n=40, curl=1.0, dx_bias=0.0):
    """Long wet strands falling from roots list[(x,y)]."""
    out = []
    for i in range(n):
        x0, y0 = roots[i % len(roots)]
        x0 += r.uniform(-8, 8)
        L = r.uniform(*length)
        b1 = r.uniform(-sway, sway) * curl + dx_bias * 0.5; b2 = r.uniform(-sway, sway) * curl + dx_bias
        x3 = x0 + b2 + r.uniform(-10, 10)
        out.append(f'<path d="M{x0:.0f},{y0:.0f} C{x0+b1*0.4:.0f},{y0+L*0.3:.0f} {x0+b1:.0f},{y0+L*0.6:.0f} {x3:.0f},{y0+L:.0f}" '
                   f'stroke="{color}" stroke-width="{r.uniform(*width):.1f}" fill="none" stroke-linecap="round" opacity="{r.uniform(0.75,1):.2f}"/>')
    return "".join(out)


def _bez(p, t):
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = p
    a, b, c, d = (1-t)**3, 3*(1-t)**2*t, 3*(1-t)*t*t, t**3
    return a*x0+b*x1+c*x2+d*x3, a*y0+b*y1+c*y2+d*y3


def tapered(p, w0, w1=0.6, n=16):
    """Filled tapered stroke along cubic bezier p=[(x,y)*4] — width w0 at start to w1 at the tip."""
    L, R = [], []
    for i in range(n + 1):
        t = i / n
        x, y = _bez(p, t); x2, y2 = _bez(p, min(1, t + 0.01)); x1, y1 = _bez(p, max(0, t - 0.01))
        dx, dy = x2 - x1, y2 - y1; d = math.hypot(dx, dy) or 1
        nx, ny = -dy / d, dx / d
        w = (w0 * (1 - t) + w1 * t) * (1 - 0.15 * math.sin(t * 9)) * min(1.0, 0.25 + t * 6) / 2
        L.append(f"{x+nx*w:.1f},{y+ny*w:.1f}"); R.append(f"{x-nx*w:.1f},{y-ny*w:.1f}")
    return "M" + " L".join(L) + " L" + " L".join(reversed(R)) + " Z"


def hair_clumps(r, roots, length=(250, 450), sway=40, width=(5, 14), clumps=10, per=4, color="#030406",
                dx_bias=0.0, op=(0.85, 1.0), wave=1.0):
    """Wet hair: clumps of tapered strands that converge to points (like soaked hair)."""
    out = []
    for c in range(clumps):
        x0, y0 = roots[c % len(roots)]
        x0 += r.uniform(-10, 10); y0 += r.uniform(-6, 6)
        L = r.uniform(*length)
        b1 = r.uniform(-sway, sway) * wave; b2 = r.uniform(-sway, sway) * wave
        tip = (x0 + dx_bias + r.uniform(-sway, sway) * 0.6, y0 + L)
        p1 = (x0 + b1 * 0.5 + dx_bias * 0.2, y0 + L * 0.33); p2 = (x0 + b2 + dx_bias * 0.7, y0 + L * 0.66)
        wc = r.uniform(*width)
        for k in range(per):
            off = (k - (per - 1) / 2) * wc * 0.55
            p = [(x0 + off, y0), (p1[0] + off * 0.8, p1[1]), (p2[0] + off * 0.45, p2[1]),
                 (tip[0] + off * 0.08 + r.uniform(-4, 4), tip[1] + r.uniform(-L * 0.12, L * 0.05))]
            out.append(f'<path d="{tapered(p, wc * r.uniform(0.5, 0.9), 0.5)}" fill="{color}" opacity="{r.uniform(*op):.2f}"/>')
    return "".join(out)


# ======================================================================== LA LLORONA — full figure
def llorona(pose="stand", seed=3, rim="#bfe0ff", glow=True, face_vis=True, wind=1.0, mist=True, veil_on=True, horns=False, nofx_low=False):
    """Tall woman in a wet white dress, long veil, long black hair, pale face with hollow eyes.
    pose: stand (arms hanging), reach (right arm reaching forward/up), mourn (hands to face), walk (profile-ish lean).
    Returned in local coords (1000 tall) — wrap with place()."""
    r = random.Random(seed)
    g = uid("ll")
    defs = f'''<defs>
<linearGradient id="{g}dress" x1="0" y1="180" x2="0" y2="1000" gradientUnits="userSpaceOnUse">
 <stop offset="0" stop-color="#f3f7fa"/><stop offset="0.45" stop-color="#d4dee6"/><stop offset="0.8" stop-color="#9fb1c0"/><stop offset="1" stop-color="#7d93a6"/></linearGradient>
<linearGradient id="{g}side" x1="-250" y1="0" x2="250" y2="0" gradientUnits="userSpaceOnUse">
 <stop offset="0" stop-color="#1c2a38" stop-opacity="0.55"/><stop offset="0.35" stop-color="#1c2a38" stop-opacity="0.12"/>
 <stop offset="0.7" stop-color="#ffffff" stop-opacity="0"/><stop offset="1" stop-color="#ffffff" stop-opacity="0.25"/></linearGradient>
<radialGradient id="{g}face" cx="0.6" cy="0.35" r="0.75"><stop offset="0" stop-color="#eef2f4"/><stop offset="0.6" stop-color="#c3ccd3"/><stop offset="1" stop-color="#7f8c97"/></radialGradient>
<linearGradient id="{g}veil" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f6fbff" stop-opacity="0.75"/><stop offset="0.6" stop-color="#dfeaf3" stop-opacity="0.4"/><stop offset="1" stop-color="#dfeaf3" stop-opacity="0.05"/></linearGradient>
<linearGradient id="{g}fade" x1="0" y1="0" x2="0" y2="1000" gradientUnits="userSpaceOnUse">
 <stop offset="0" stop-color="#fff"/><stop offset="0.80" stop-color="#fff"/><stop offset="0.97" stop-color="#fff" stop-opacity="0.25"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<mask id="{g}m" maskUnits="userSpaceOnUse" x="-600" y="-100" width="1200" height="1200"><rect x="-600" y="-100" width="1200" height="1200" fill="url(#{g}fade)"/></mask>
<linearGradient id="{g}skin" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8d9aa6"/><stop offset="0.5" stop-color="#d7dee3"/><stop offset="1" stop-color="#eef3f6"/></linearGradient>
</defs>'''
    W = wind
    # ---------- veil (behind everything), flowing to the right with the wind
    vb = []
    for i in range(9):
        x = -175 + i * (380 + 60 * W) / 8
        vb.append(f"{x:.0f},{700 + (30 if i % 2 else -10) + r.uniform(-15, 15):.0f}")
    veil_d = (f'M-40,40 C-120,120 -165,330 -185,560 L{" L".join(vb)} '
              f'C{220+80*W},{560} {170+40*W},380 {90+20*W},170 C70,110 50,60 30,38 Q-5,22 -40,40 Z')
    veil = (f'<path d="{veil_d}" fill="url(#{g}veil)" opacity="0.7" filter="url(#blur2)"/>'
            f'<path d="{veil_d}" fill="url(#{g}veil)" opacity="0.55"/>')
    veil_folds = "".join(
        f'<path d="M{x0},{60+abs(x0)*0.3:.0f} C{x0*1.4+r.uniform(-20,20):.0f},260 {x0*1.6+W*20+r.uniform(-30,30):.0f},460 {x0*2.1+W*40:.0f},{690+r.uniform(-20,20):.0f}" stroke="#ffffff" stroke-opacity="{r.uniform(0.12,0.28):.2f}" stroke-width="{r.uniform(3,7):.1f}" fill="none" filter="url(#blur1)"/>'
        for x0 in (-70, -40, -12, 18, 48, 75))
    # ---------- back hair: long wet clumps falling behind the shoulders
    back_hair = (hair_clumps(r, [(-26, 80), (-30, 110), (-28, 140)], (400, 520), 20, (12, 22), clumps=7, per=3, dx_bias=-40) +
                 hair_clumps(r, [(26, 80), (30, 110), (28, 140)], (360, 470), 20, (12, 22), clumps=7, per=3, dx_bias=40))
    # ---------- dress body (one shape incl. skirt), hem tattered
    hem = []
    xs = list(range(-250, 271, 26))
    for i, x in enumerate(xs):
        y = 990 + (14 if i % 2 else -10) + r.uniform(-12, 12)
        hem.append(f"{x},{y:.0f}")
    hem_path = " L".join(hem)
    dress = (f'<path d="M-24,172 C-48,178 -76,190 -92,212 C-104,250 -92,300 -76,350 C-70,390 -62,420 -66,450 '
             f'C-110,600 -170,800 -250,985 L{hem_path} '
             f'C200,800 128,600 76,452 C70,420 74,390 80,350 C96,300 104,250 92,212 C78,190 48,178 24,172 Z"')
    dress_fill = dress + f' fill="url(#{g}dress)"/>'
    dress_shade = dress + f' fill="url(#{g}side)"/>'
    # folds of wet cloth clinging to the legs
    folds = []
    for k in range(13):
        x0 = -60 + k * 10 + r.uniform(-4, 4)
        x1 = -230 + k * 38 + r.uniform(-10, 10)
        cx = x0 + (x1 - x0) * 0.5 + r.uniform(-25, 25)
        folds.append(f'<path d="M{x0:.0f},{470 + r.uniform(0,60):.0f} Q{cx:.0f},{740:.0f} {x1:.0f},{985:.0f}" stroke="#4c6274" stroke-opacity="{r.uniform(0.25,0.55):.2f}" stroke-width="{r.uniform(3,8):.1f}" fill="none" filter="url(#blur1)"/>')
        if k % 2 == 0:
            folds.append(f'<path d="M{x0+6:.0f},{500:.0f} Q{cx+8:.0f},{750:.0f} {x1+12:.0f},{980:.0f}" stroke="#ffffff" stroke-opacity="{r.uniform(0.25,0.5):.2f}" stroke-width="{r.uniform(1.5,3):.1f}" fill="none"/>')
    # bodice details: neckline, waist seam, gathered cloth at chest
    bodice = ('<path d="M-30,176 Q0,215 30,176" stroke="#5d7385" stroke-width="3" fill="none" opacity="0.7"/>'
              '<path d="M-68,440 Q0,462 74,440" stroke="#56697a" stroke-width="4" fill="none" opacity="0.55"/>'
              '<path d="M-40,250 Q-30,330 -46,420 M-10,230 Q-4,330 -14,430 M22,236 Q30,330 20,430 M48,250 Q40,330 52,420" stroke="#6d8294" stroke-width="2.5" fill="none" opacity="0.45"/>')
    # wet dark patches near hem and stains
    wet = "".join(f'<ellipse cx="{r.uniform(-200,220):.0f}" cy="{r.uniform(800,970):.0f}" rx="{r.uniform(20,60):.0f}" ry="{r.uniform(40,90):.0f}" fill="#3b5163" opacity="{r.uniform(0.15,0.3):.2f}" filter="url(#blur2)"/>' for _ in range(9))
    # ---------- neck + head
    neck = f'<path d="M-17,128 L-21,182 Q0,192 21,182 L17,128 Z" fill="url(#{g}skin)"/>'
    head_tilt = 7 if pose != "walk" else 12
    face = f'''<g transform="rotate({head_tilt} 0 100)">
<ellipse cx="0" cy="98" rx="41" ry="54" fill="url(#{g}face)"/>
<path d="M-38,96 Q-36,140 -14,152 Q0,158 14,152 Q36,140 38,96" fill="#7f8d99" opacity="0.35"/>
<ellipse cx="-16" cy="93" rx="11.5" ry="9" fill="#06080b" filter="url(#blur1)"/>
<ellipse cx="17" cy="93" rx="11.5" ry="9" fill="#06080b" filter="url(#blur1)"/>
<ellipse cx="-16" cy="93" rx="8" ry="6" fill="#000"/><ellipse cx="17" cy="93" rx="8" ry="6" fill="#000"/>
<circle cx="-15" cy="93" r="1.8" fill="#d8ecff" opacity="{0.9 if face_vis else 0}"/><circle cx="18" cy="93" r="1.8" fill="#d8ecff" opacity="{0.9 if face_vis else 0}"/>
<path d="M-16,101 Q-18,125 -14,142 M17,101 Q19,122 16,138" stroke="#1a2026" stroke-width="2.4" fill="none" opacity="0.55"/>
<path d="M0,98 Q3,113 -1,120 Q2,122 5,120" stroke="#6c7883" stroke-width="2" fill="none" opacity="0.7"/>
<path d="M-11,133 Q0,128 11,133 Q0,141 -11,133 Z" fill="#14181d" opacity="0.85"/>
<path d="M-30,80 Q-18,74 -6,80 M6,80 Q18,74 30,80" stroke="#2a3138" stroke-width="2.4" fill="none" opacity="0.6"/>
</g>'''
    # front hair: centre parting, wet strands over face sides and shoulders
    front_hair = (f'<g transform="rotate({head_tilt} 0 100)">'
                  '<path d="M0,42 C-34,40 -52,66 -50,104 C-49,124 -46,140 -42,152 L-34,150 C-36,128 -36,108 -32,88 C-26,64 -14,54 0,54 '
                  'C14,54 26,64 32,88 C36,108 36,128 34,150 L42,152 C46,140 49,124 50,104 C52,66 34,40 0,42 Z" fill="#040507"/>'
                  '<path d="M-4,46 C-22,50 -34,66 -38,90" stroke="#3b4a59" stroke-width="2" fill="none" opacity="0.6"/>'
                  '</g>')
    strands_f = hair_clumps(r, [(-40, 100), (-46, 130), (-42, 160), (-38, 90)], (260, 420), 22, (8, 16), clumps=9, per=3, dx_bias=-8)
    strands_f += hair_clumps(r, [(40, 100), (46, 130), (42, 160), (38, 92)], (220, 360), 22, (8, 16), clumps=8, per=3, dx_bias=10)
    strands_f += hair_clumps(r, [(-30, 70)], (110, 170), 8, (4, 7), clumps=2, per=2, dx_bias=-4)
    strands_hl = hair_strands(r, [(-38, 120), (40, 125)], (180, 320), 20, (1, 1.6), color="#4a5b6b", n=10)
    # front veil layer over the head (thin, translucent lace edge)
    veil_front = (f'<g transform="rotate({head_tilt} 0 100)"><path d="M-62,90 C-60,40 -30,22 0,22 C30,22 60,40 64,92 C70,130 80,170 92,200 '
                  f'L80,206 C66,170 56,130 52,96 C46,52 26,38 0,38 C-26,38 -46,52 -50,96 C-54,130 -64,170 -80,206 L-92,200 C-80,170 -66,130 -62,90 Z" fill="#eef5fb" opacity="0.55"/>'
                  '<path d="M-58,92 C-54,46 -28,30 0,30 C28,30 54,46 58,92" stroke="#ffffff" stroke-width="3" fill="none" opacity="0.5" stroke-dasharray="2 5"/></g>')
    # ---------- arms + hands
    def sleeve(side, wrist, elbow, sh=(90, 214)):
        s = side
        sx, sy = sh[0] * s, sh[1]
        ex, ey = elbow; wx, wy = wrist
        # outer edge, inner edge
        return (f'<path d="M{sx},{sy-4} C{sx+18*s},{sy+40} {ex+16*s},{ey-40} {ex+14*s},{ey} C{ex+12*s},{ey+50} {wx+12*s},{wy-50} {wx+12*s},{wy} '
                f'L{wx-12*s},{wy+4} C{wx-13*s},{wy-50} {ex-14*s},{ey+40} {ex-15*s},{ey} C{ex-18*s},{ey-40} {sx-26*s},{sy+50} {sx-30*s},{sy+20} Z" fill="url(#{g}dress)"/>'
                f'<path d="M{ex-6*s},{ey-30} Q{ex+4*s},{ey} {ex-4*s},{ey+30} M{ex+2*s},{ey+20} Q{ex+8*s},{ey+60} {wx},{wy-40}" stroke="#53687a" stroke-width="3" fill="none" opacity="0.5"/>')

    def hand(cx, cy, ang=0, s=1.0, spread=1.0, curl=0.3):
        """Pale bony hand hanging down from wrist at (cx,cy); ang rotates (deg)."""
        fingers = []
        for i, (dx, L, w) in enumerate([(-11, 58, 6.5), (-3.5, 68, 6.8), (4, 66, 6.6), (11, 54, 6)]):
            dx *= spread
            tipx = dx * 1.25 + curl * 6; tipy = 38 + L
            fingers.append(f'<path d="M{dx-w/2},{36} C{dx-w/2},{36+L*0.5} {tipx-w/2},{tipy-14} {tipx},{tipy} C{tipx+w/2},{tipy-14} {dx+w/2},{36+L*0.5} {dx+w/2},{36} Z"/>')
            fingers.append(f'<path d="M{dx-w/2+1},{36+L*0.35:.0f} q{w/2},2 {w-2},0 M{dx-w/2+1.5},{36+L*0.68:.0f} q{w/2},2 {w-3},0" stroke="#7b8894" stroke-width="1" fill="none"/>')
        thumb = '<path d="M-14,8 C-24,20 -26,36 -22,52 C-20,58 -14,56 -14,50 C-14,38 -10,26 -6,18 Z"/>'
        palm = '<path d="M-14,0 L14,0 C17,14 17,28 15,40 L-15,40 C-17,28 -17,14 -14,0 Z"/>'
        body = palm + thumb + "".join(fingers)
        return (f'<g transform="translate({cx},{cy}) rotate({ang}) scale({s})">'
                f'<g fill="#e6edf2" stroke="#8495a3" stroke-width="1.2">{body}</g>'
                f'<path d="M-6,4 L-8,36 M2,4 L0,36 M9,4 L9,36" stroke="#9aa8b4" stroke-width="1.2" opacity="0.6"/></g>')

    if pose == "reach":
        arms = (sleeve(-1, (-104, 545), (-122, 380)) + hand(-104, 548, 4) +
                f'<path d="M98,200 C150,200 210,190 270,165 C320,145 360,120 395,100 L405,122 C370,145 330,170 285,195 C230,222 170,240 110,250 Z" fill="url(#{g}dress)"/>'
                f'<path d="M150,236 C200,226 260,205 330,150 C330,200 300,260 270,330 C250,300 220,280 150,260 Z" fill="url(#{g}dress)" opacity="0.9"/>'
                f'<path d="M200,240 Q250,270 268,325 M240,222 Q280,250 290,300" stroke="#53687a" stroke-width="3" fill="none" opacity="0.5"/>'
                + drips(r, [(270, 335), (262, 330), (285, 300)], size=1.2)
                + f'<path d="M160,215 Q230,195 300,160" stroke="#53687a" stroke-width="3" fill="none" opacity="0.5"/>' + hand(410, 108, -115, 1.05, 1.2, 0.0))
        strands_f += hair_strands(r, [(60, 160)], (120, 200), 20, (2, 4), n=6, dx_bias=30)
    elif pose == "mourn":
        arms = (f'<path d="M-96,205 C-120,260 -110,330 -70,350 C-50,330 -40,250 -30,170 L-50,160 Z" fill="url(#{g}dress)"/>'
                f'<path d="M96,205 C120,260 110,330 70,350 C50,330 40,250 30,170 L50,160 Z" fill="url(#{g}dress)"/>'
                + hand(-30, 175, 160, 0.9, 1.1, 0.2) + hand(30, 175, 200, 0.9, 1.1, 0.2))
    else:
        arms = (sleeve(-1, (-110, 548), (-124, 380)) + sleeve(1, (114, 540), (126, 375)) +
                hand(-110, 550, 6) + hand(114, 543, -6))
    # ---------- drips + mist
    drip_pts = [(r.uniform(-240, 260), r.uniform(985, 1010)) for _ in range(14)]
    if pose == "stand":
        drip_pts += [(-112 + r.uniform(-8, 8), 650 + r.uniform(0, 10)) for _ in range(3)] + [(112 + r.uniform(-8, 8), 645) for _ in range(3)]
    drops = drips(r, drip_pts, size=1.2)
    # rim light (right side contours)
    rim_d = ('M24,172 C48,178 78,190 92,212 C104,250 96,300 80,350 C74,390 70,420 76,452 C128,600 200,800 270,985 '
             '')
    rim_l = (f'<path d="{rim_d}" stroke="{rim}" stroke-width="10" fill="none" opacity="0.55" filter="url(#blur2)"/>'
             f'<path d="{rim_d}" stroke="#ffffff" stroke-width="3" fill="none" opacity="0.8"/>') if rim else ""
    aura = (f'<ellipse cx="0" cy="480" rx="330" ry="560" fill="#bcd8f0" opacity="0.16" filter="url(#blur4)"/>'
            f'<ellipse cx="0" cy="110" rx="120" ry="130" fill="#e6f2ff" opacity="0.22" filter="url(#blur3)"/>') if glow else ""
    mist_l = (f'<ellipse cx="0" cy="990" rx="380" ry="70" fill="#dbe8f2" opacity="0.5" filter="url(#blur3)"/>'
              f'<ellipse cx="-120" cy="960" rx="200" ry="50" fill="#e8f1f8" opacity="0.35" filter="url(#blur3)"/>'
              f'<ellipse cx="170" cy="975" rx="220" ry="45" fill="#e8f1f8" opacity="0.35" filter="url(#blur3)"/>') if mist else ""
    if not veil_on:
        veil = veil_folds = veil_front = ""
    if nofx_low:   # resvg crashes on filtered elements that end up fully off-canvas (very large placements)
        wet = ""; folds = [f.replace(' filter="url(#blur1)"', '') for f in folds]; drops = ""
    if horns:   # Cihuacoatl: hair tied up in two small horns crossed over the forehead (Sahagun)
        veil_front = (f'<g transform="rotate({head_tilt} 0 100)">'
                      '<path d="M-10,52 C-30,20 -50,-10 -46,-40 C-30,-20 -14,10 4,44 Z" fill="#040507"/>'
                      '<path d="M10,52 C30,20 50,-10 46,-40 C30,-20 14,10 -4,44 Z" fill="#040507"/>'
                      '<path d="M-44,-36 C-34,-14 -20,14 -6,40 M44,-36 C34,-14 20,14 6,40" stroke="#5a6b7c" stroke-width="2" fill="none"/>'
                      '<rect x="-30" y="40" width="60" height="10" rx="4" fill="#c9b06a"/></g>')
    body = (veil + veil_folds + back_hair + dress_fill + dress_shade + "".join(folds) + bodice + wet +
            neck + arms + face + front_hair + strands_f + strands_hl + veil_front + rim_l)
    return defs + aura + f'<g mask="url(#{g}m)">{body}</g>' + drops + mist_l


# ======================================================================== LA LLORONA — close portrait
def llorona_face(scream=False, seed=5, cx=1200, cy=700, s=1.0, rim="#a9d2ff", bg=True, tears=True):
    """Close-up head & shoulders, ~1100px tall at s=1. scream=True: mouth torn open, eyes wider."""
    r = random.Random(seed)
    g = uid("lf")
    defs = f'''<defs>
<radialGradient id="{g}sk" cx="0.58" cy="0.38" r="0.7"><stop offset="0" stop-color="#f1f4f5"/><stop offset="0.45" stop-color="#c9d1d7"/><stop offset="0.8" stop-color="#8794a0"/><stop offset="1" stop-color="#4f5c68"/></radialGradient>
<radialGradient id="{g}eye" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#000"/><stop offset="0.6" stop-color="#05070a"/><stop offset="1" stop-color="#3a4550" stop-opacity="0"/></radialGradient>
<linearGradient id="{g}veil" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f4f9ff" stop-opacity="0.8"/><stop offset="1" stop-color="#cfe0ee" stop-opacity="0.15"/></linearGradient>
<linearGradient id="{g}dr" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e9eff3"/><stop offset="1" stop-color="#6f8394"/></linearGradient>
<radialGradient id="{g}bg" cx="0.5" cy="0.45" r="0.7"><stop offset="0" stop-color="#1a2a3a"/><stop offset="0.6" stop-color="#08101a"/><stop offset="1" stop-color="#020407"/></radialGradient>
</defs>'''
    out = [defs]
    if bg:
        out.append(f'<rect width="2400" height="1350" fill="url(#{g}bg)"/>')
        out.append('<ellipse cx="1200" cy="560" rx="700" ry="520" fill="#9fc4e6" opacity="0.10" filter="url(#blur4)"/>')
    # all in local coords centred at face centre (0,0), face ~ 330 wide, 440 tall
    L = []
    # veil behind head + shoulders
    vd = 'M-300,-150 C-280,-330 -150,-400 0,-400 C150,-400 290,-330 320,-140 C350,100 400,380 520,700 L-520,700 C-400,380 -340,100 -300,-150 Z'
    L.append(f'<path d="{vd}" fill="url(#{g}veil)" opacity="0.55" filter="url(#blur3)"/><path d="{vd}" fill="url(#{g}veil)" opacity="0.35"/>')
    for k in range(7):
        x = -260 + k * 85
        L.append(f'<path d="M{x*0.6:.0f},-330 C{x*0.9:.0f},-100 {x*1.2:.0f},250 {x*1.7:.0f},700" stroke="#ffffff" stroke-width="{r.uniform(6,14):.0f}" opacity="{r.uniform(0.06,0.14):.2f}" fill="none" filter="url(#blur2)"/>')
    # back hair mass
    L.append(hair_clumps(r, [(-170, -150), (-190, -60), (-200, 40), (-180, 120)], (560, 820), 40, (40, 70), clumps=10, per=3, dx_bias=-90))
    L.append(hair_clumps(r, [(170, -150), (190, -60), (200, 40), (180, 120)], (560, 820), 40, (40, 70), clumps=10, per=3, dx_bias=90))
    # shoulders / dress
    L.append(f'<path d="M-520,700 C-470,500 -320,410 -140,380 C-100,370 -90,360 -88,340 L88,340 C90,360 100,370 140,380 C320,410 470,500 520,700 Z" fill="url(#{g}dr)"/>')
    L.append('<path d="M-90,410 Q0,470 90,410" stroke="#566b7c" stroke-width="5" fill="none" opacity="0.7"/>')
    for k in range(9):
        x = -380 + k * 95 + r.uniform(-20, 20)
        L.append(f'<path d="M{x*0.5:.0f},{440+r.uniform(0,30):.0f} Q{x*0.8:.0f},560 {x:.0f},700" stroke="#4d6070" stroke-width="{r.uniform(3,7):.1f}" opacity="0.4" fill="none" filter="url(#blur1)"/>')
    # neck
    L.append(f'<path d="M-92,170 C-96,260 -110,340 -120,400 Q0,450 120,400 C110,340 96,260 92,170 Z" fill="url(#{g}sk)"/>')
    L.append('<path d="M-60,240 Q-40,330 -70,400 M55,250 Q40,330 66,400" stroke="#55626d" stroke-width="5" fill="none" opacity="0.35"/>')
    # face shape (long, gaunt)
    jaw = 260 if not scream else 330
    L.append(f'<path d="M-165,-60 C-170,-200 -95,-270 0,-270 C95,-270 170,-200 165,-60 C162,40 140,140 100,{jaw-50} C70,{jaw-10} 30,{jaw} 0,{jaw} C-30,{jaw} -70,{jaw-10} -100,{jaw-50} C-140,140 -162,40 -165,-60 Z" fill="url(#{g}sk)"/>')
    # cheekbone hollows & temple shadows
    L.append('<path d="M-150,30 C-120,90 -100,140 -96,190 C-120,150 -150,90 -158,40 Z" fill="#3e4954" opacity="0.45" filter="url(#blur2)"/>')
    L.append('<path d="M150,30 C120,90 100,140 96,190 C120,150 150,90 158,40 Z" fill="#3e4954" opacity="0.35" filter="url(#blur2)"/>')
    L.append('<ellipse cx="-95" cy="95" rx="40" ry="60" fill="#47525d" opacity="0.30" filter="url(#blur2)"/><ellipse cx="95" cy="95" rx="40" ry="60" fill="#47525d" opacity="0.25" filter="url(#blur2)"/>')
    # eye sockets: deep hollow
    ew, eh = (62, 44) if not scream else (68, 58)
    for sx in (-1, 1):
        ex = sx * 72
        L.append(f'<ellipse cx="{ex}" cy="-25" rx="{ew+28}" ry="{eh+30}" fill="#2b333b" opacity="0.55" filter="url(#blur2)"/>')
        L.append(f'<ellipse cx="{ex}" cy="-22" rx="{ew}" ry="{eh}" fill="url(#{g}eye)"/>')
        L.append(f'<ellipse cx="{ex}" cy="-20" rx="{ew*0.62:.0f}" ry="{eh*0.6:.0f}" fill="#000"/>')
        # tiny glint deep inside
        L.append(f'<circle cx="{ex+sx*4}" cy="-22" r="{5 if not scream else 6}" fill="#e9f6ff" opacity="0.95"/><circle cx="{ex+sx*4}" cy="-22" r="16" fill="#9fd0ff" opacity="0.35" filter="url(#blur1)"/>')
        # brow ridge
        L.append(f'<path d="M{ex-sx*50},{-72 - (12 if scream else 0)} Q{ex},{-96 - (16 if scream else 0)} {ex+sx*44},{-70}" stroke="#39434c" stroke-width="6" fill="none" opacity="0.35" stroke-linecap="round" filter="url(#blur1)"/>')
        if tears:
            # black water tears running down
            L.append(f'<path d="M{ex-sx*6},{eh-18} C{ex-sx*10},{60} {ex-sx*2},{120} {ex-sx*14},{200} C{ex-sx*16},{230} {ex-sx*10},{250} {ex-sx*8},{250} C{ex-sx*4},{240} {ex-sx*6},{200} {ex+sx*2},{140} C{ex+sx*8},{80} {ex+sx*6},{40} {ex+sx*6},{eh-18} Z" fill="#05070a" opacity="0.8"/>')
            L.append(f'<path d="M{ex+sx*14},{eh-16} C{ex+sx*18},{50} {ex+sx*12},{90} {ex+sx*20},{130}" stroke="#05070a" stroke-width="4" fill="none" opacity="0.6"/>')
    # nose
    L.append('<path d="M-6,-10 C-10,40 -20,80 -28,96 C-14,108 0,104 6,100 C18,106 30,104 34,94 C24,80 14,40 10,-10" fill="#9aa5ae" opacity="0.55"/>')
    L.append('<path d="M-24,98 Q-12,92 -4,100 M8,100 Q18,92 30,96" stroke="#1d2328" stroke-width="5" fill="none" opacity="0.8"/>')
    # mouth
    if scream:
        L.append('<path d="M-62,160 C-60,135 -30,124 0,126 C30,124 60,135 62,160 C66,220 40,290 0,298 C-40,290 -66,220 -62,160 Z" fill="#020203"/>')
        L.append('<path d="M-62,160 C-60,135 -30,124 0,126 C30,124 60,135 62,160" stroke="#6b5a5e" stroke-width="7" fill="none" opacity="0.7"/>')
        L.append('<path d="M-56,190 C-60,240 -40,280 -10,292 M56,190 C60,240 40,280 10,292" stroke="#3a3f45" stroke-width="5" fill="none" opacity="0.6"/>')
    else:
        L.append('<path d="M-46,170 C-24,160 -8,164 0,166 C8,164 24,160 46,170 C26,182 10,186 0,186 C-10,186 -26,182 -46,170 Z" fill="#141a1f"/>')
        L.append('<path d="M-44,170 C-20,176 20,176 44,170" stroke="#020304" stroke-width="5" fill="none"/>')
        L.append('<path d="M-30,190 Q0,204 30,190" stroke="#59646e" stroke-width="4" fill="none" opacity="0.6"/>')
        L.append('<path d="M-38,174 l2,4 M-20,178 l1,5 M18,178 l-1,5 M36,174 l-2,4" stroke="#3a3f45" stroke-width="2" opacity="0.7"/>')
    # cracked skin lines
    for _ in range(7):
        x0, y0 = r.uniform(-140, 140), r.uniform(-200, 220)
        L.append(f'<path d="M{x0:.0f},{y0:.0f} l{r.uniform(-20,20):.0f},{r.uniform(10,30):.0f} l{r.uniform(-15,15):.0f},{r.uniform(10,25):.0f}" stroke="#5d6972" stroke-width="1.6" fill="none" opacity="0.45"/>')
    # front hair: centre parting, curtains over the face sides, wet clumps
    L.append(hair_clumps(r, [(-160, -120), (-165, -40), (-145, -180), (-168, 40), (-160, 80)], (320, 560), 40, (20, 36), clumps=10, per=3, dx_bias=-45))
    L.append(hair_clumps(r, [(160, -120), (165, -40), (145, -180), (168, 40), (160, 80)], (320, 540), 40, (20, 36), clumps=10, per=3, dx_bias=45))
    L.append('<path d="M0,-272 C-90,-274 -160,-220 -178,-120 C-190,-40 -186,40 -182,110 L-150,110 C-150,20 -146,-60 -128,-130 C-100,-210 -50,-246 0,-250 '
             'C50,-246 100,-210 128,-130 C146,-60 150,20 150,110 L182,110 C186,40 190,-40 178,-120 C160,-220 90,-274 0,-272 Z" fill="#030405"/>')
    # wet clumps across the face (left eye half hidden)
    L.append(hair_clumps(r, [(-100, -235), (-80, -245), (-120, -215)], (330, 470), 25, (12, 20), clumps=4, per=2, dx_bias=30))
    L.append(hair_clumps(r, [(110, -230)], (300, 420), 20, (10, 16), clumps=2, per=2, dx_bias=-10))
    L.append(hair_strands(r, [(-150, -150), (150, -150)], (300, 520), 40, (1.2, 2), color="#3e4c5a", n=14))
    # veil over the crown
    L.append('<path d="M-215,-60 C-210,-300 -100,-352 0,-352 C100,-352 210,-300 220,-60" stroke="#eef6fd" stroke-width="34" fill="none" opacity="0.28" filter="url(#blur2)"/>')
    L.append('<path d="M-200,-110 C-190,-290 -95,-336 0,-336 C95,-336 190,-290 202,-110" stroke="#ffffff" stroke-width="5" stroke-dasharray="3 9" fill="none" opacity="0.6"/>')
    # drops on face / hair
    L.append(drips(r, [(r.uniform(-160, 160), r.uniform(-180, 240)) for _ in range(9)], color="#e4f1fb", op=0.6, size=1.6))
    # rim light on right side of face and hair
    if rim:
        L.append(f'<path d="M100,-250 C170,-220 200,-120 196,-20 C192,100 150,200 100,{jaw-40}" stroke="{rim}" stroke-width="22" fill="none" opacity="0.45" filter="url(#blur2)"/>')
        L.append(f'<path d="M150,-210 C190,-150 200,-60 196,20" stroke="#ffffff" stroke-width="4" fill="none" opacity="0.7"/>')
        L.append(f'<path d="M200,40 C210,200 240,380 300,560" stroke="{rim}" stroke-width="5" fill="none" opacity="0.6"/>')
    out.append(f'<g transform="translate({cx},{cy}) scale({s})">{"".join(L)}</g>')
    return "".join(out)
