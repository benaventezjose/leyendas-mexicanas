import sys, os
sys.path.insert(0, '/home/claude/pipeline'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from art import *
from hand import hand, place
from make_art import child_arm
s = '<rect width="2400" height="1350" fill="#030408"/>' + glow(700, 700, 900, "red", 0.45) + glow(700, 500, 600, "moon", 0.3)
s += '<rect x="0" y="0" width="2400" height="150" fill="#c8ccd4"/><rect x="0" y="130" width="2400" height="40" fill="#3a2230"/>'
s += child_arm([(620, 100), (640, 260), (660, 420)], w=90)
s += place(720, 1500, 12, 1.7, hand("claw", rim="#ff8a6a", seed=5, rim_side=-1))
s += thumb_text("NO SAQUES\nEL BRAZO", x=1290, y=420, size=250, fill="#ffffff", sw=28)
s += '<rect x="1300" y="790" width="900" height="16" fill="#c8141a"/>'
open("thumb_a.svg", "w").write(thumb(s))
