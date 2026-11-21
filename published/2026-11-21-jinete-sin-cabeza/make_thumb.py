import sys, os
sys.path.insert(0, '/home/claude/pipeline'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from art import *
from make_art import horse_rider, moon
s = '<rect width="2400" height="1350" fill="#02050c"/>' + glow(1650, 520, 1100, "moon", 0.7)
s += '<circle cx="1650" cy="560" r="520" fill="#e8eef4"/>' + glow(1650, 560, 900, "moon", 0.6)
s += '<rect y="1120" width="2400" height="230" fill="#020306"/>'
s += horse_rider(1500, 1500, 1.25, "walk", rim="#ffffff", col="#010203")
s += thumb_text("SIN\nCABEZA", x=90, y=330, size=300, fill="#ffffff", sw=26)
s += '<rect x="100" y="900" width="760" height="20" fill="#c8141a"/>'
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "thumb_a.svg"), "w").write(thumb(s))
