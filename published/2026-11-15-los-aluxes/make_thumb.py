import sys, os
sys.path.insert(0, '/home/claude/pipeline'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from art import *
from alux import alux_head
from make_art import milpa_row, kahtal, MOONRIM
s = sky("#010407", "#0a2a30") + glow(700, 560, 900, "moon", 0.5)
s += milpa_row(1400, 22, 700, 1000, "#020605", MOONRIM, 7, w=12)
s += '<rect width="2400" height="1350" fill="#000" opacity="0.25"/>'
s += glow(700, 600, 700, "warm", 0.35)
s += f'<g transform="translate(720,700) scale(2.75)">{alux_head("scare", "glow", "#d8f0ff")}</g>'
s += thumb_text("NO LO\nOLVIDES", x=1330, y=420, size=300, fill="#ffffff", sw=30)
s += '<rect x="1340" y="790" width="560" height="14" fill="#c8141a"/>'
open("thumb_a.svg", "w").write(thumb(s))
