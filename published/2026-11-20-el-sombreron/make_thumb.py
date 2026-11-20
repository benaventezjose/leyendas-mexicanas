import sys, os
sys.path.insert(0, '/home/claude/pipeline'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from art import *
from make_art import sombreron_fig, braid, wavy
s = '<rect width="2400" height="1350" fill="#05070e"/>' + glow(700, 420, 1000, "moon", 0.6) + glow(700, 1100, 800, "red", 0.35)
for i in range(7):
    x0 = 80 + i * 40
    s += braid(wavy(x0, -20, x0 + 60, 1400, 25, 2, i), 34, "#0a0605", "#7a6050", seed=i)
s += f'<g transform="translate(640,1560) scale(2.6)">{sombreron_fig(rim="#cfe0ff", eyes="#fff0d0", guitar=False)}</g>'
for ex in (-22, 22):
    s += f'<circle cx="{640+ex*2.6:.0f}" cy="{1560-318*2.6:.0f}" r="45" fill="url(#redglow)" opacity="0.9"/>'
s += thumb_text("NO TE\nASOMES", x=1360, y=400, size=270, fill="#ffffff", sw=28)
s += '<rect x="1370" y="760" width="860" height="18" fill="#c8141a"/>'
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "thumb_a.svg"), "w").write(thumb(s))
