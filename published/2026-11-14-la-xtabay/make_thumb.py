import sys, os
sys.path.insert(0, '/home/claude/pipeline'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from helpers import *
from xchars import *
from make_art import ceiba, monte, yuc_night
s = sky("#000306", "#0c2630") + glow(820, 520, 900, "moon", 0.55)
s += ceiba(300, 1500, 1.25, "#010304", "#9cc8e0", thorns=True)
s += xtabay_bust(820, 520, 2.05, scare=1, smile=0.8, lids=0.05, rim="#d0ecff")
s += '<rect width="2400" height="1350" fill="#000" opacity="0.0"/>'
s += thumb_text("NO LA\nSIGAS", x=1420, y=470, size=380, fill="#ffffff", sw=34)
s += '<rect x="1430" y="900" width="560" height="14" fill="#c8141a"/>'
open("thumb_a.svg", "w").write(thumb(s))
