import sys, os
sys.path.insert(0, '/home/claude/pipeline'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from art import *
from make_art import nun_bust, peach_tree, MOONRIM
s = '<rect width="2400" height="1350" fill="#030308"/>' + glow(650, 600, 1100, "moon", 0.6) + glow(1900, 300, 800, "red", 0.35)
s += f'<g opacity="0.55">{peach_tree(1800, 1900, 1.6, rim="#ff8060", seed=5)}</g>'
s += nun_bust(640, 760, 3.0, rim="#e8f2ff", ghost=True, hollow=True, glow_eyes=True, smile=-0.3)
s += thumb_text("¿POR QUÉ\nNO\nVOLVISTE?", x=1260, y=330, size=225, fill="#ffffff", sw=26)
s += '<rect x="1270" y="870" width="820" height="16" fill="#c8141a"/>'
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "thumb_a.svg"), "w").write(thumb(s))
