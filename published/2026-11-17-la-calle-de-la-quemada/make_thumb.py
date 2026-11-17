import sys, os
sys.path.insert(0, '/home/claude/pipeline'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from art import *
from make_art import veiled_bust, MOONRIM, brazier_svg
import random
s = '<rect width="2400" height="1350" fill="#04050a"/>' + glow(700, 1350, 1100, "red", 0.75) + glow(700, 450, 700, "moon", 0.45)
r = random.Random(3)
for i in range(70):
    x, y = r.uniform(100, 1400), r.uniform(200, 1350)
    s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(3,9):.1f}" fill="#ffa040" opacity="{r.uniform(0.3,0.9):.2f}"/>'
s += veiled_bust(720, 560, 2.15, rim="#ffd0a0", lids=0.05, look=0.0)
s += thumb_text("DETRÁS\nDEL VELO", x=1330, y=360, size=250, fill="#ffffff", sw=28)
s += '<rect x="1340" y="700" width="880" height="18" fill="#c8141a"/>'
open("thumb_a.svg", "w").write(thumb(s))
