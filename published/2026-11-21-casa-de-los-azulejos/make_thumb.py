import sys, os
sys.path.insert(0, '/home/claude/pipeline'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from art import *
from make_art import diego_bust, ghostify, tiles_rect
s = '<rect width="2400" height="1350" fill="#02040a"/>'
s += f'<g opacity="0.55">{tiles_rect(0, 0, 2400, 1350, 170, ("#1d3f93", "#2c5cc0", "#9aa4b8", "#a08a4a"))}</g>'
s += '<rect width="2400" height="1350" fill="#02040a" opacity="0.45"/>'
s += glow(650, 600, 1000, "moon", 0.7)
s += ghostify(diego_bust(640, 700, 2.6), 1.0)
s += glow(546, 658, 60, "white", 1.0) + glow(703, 658, 60, "white", 1.0) + glow(546, 658, 30, "white", 1.0) + glow(703, 658, 30, "white", 1.0)
s += glow(1080, 1050, 300, "warm", 0.8) + '<rect x="1066" y="1040" width="28" height="110" fill="#f0e6d0"/><path d="M1080,980 Q1098,1012 1080,1040 Q1062,1012 1080,980 Z" fill="#ffe7a0"/>'
s += thumb_text("ALGUIEN\nBAJA", x=1240, y=420, size=280, fill="#ffffff", sw=28)
s += '<rect x="1250" y="780" width="900" height="16" fill="#c8141a"/>'
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "thumb_a.svg"), "w").write(thumb(s))
