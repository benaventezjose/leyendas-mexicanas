import sys, os
sys.path.insert(0, '/home/claude/pipeline'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from art import *
from make_art import bride_bust, glow
s = '<rect width="2400" height="1350" fill="#05070e"/>' + glow(700, 520, 1000, "moon", 0.6) + glow(700, 1350, 800, "red", 0.3)
s += bride_bust(720, 640, 2.9, rim="#e8f4ff", look=0.0, lids=0.0, bouquet=False)
s += ''.join(f'<circle cx="{720+x_*2.9:.0f}" cy="{640-19*2.9:.0f}" r="46" fill="url(#whiteglow)" opacity="0.85"/><circle cx="{720+x_*2.9:.0f}" cy="{640-19*2.9:.0f}" r="8" fill="#fff"/>' for x_ in (-31, 31))
s += thumb_text("NO ES\nMANIQUÍ", x=1330, y=400, size=260, fill="#ffffff", sw=28)
s += '<rect x="1340" y="720" width="880" height="18" fill="#c8141a"/>'
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "thumb_a.svg"), "w").write(thumb(s))
