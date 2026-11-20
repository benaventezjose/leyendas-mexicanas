import sys, os
sys.path.insert(0, '/home/claude/pipeline'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from art import *
from make_art import dog, put, MOONRIM
from base_chars import uid
s = '<rect width="2400" height="1350" fill="#030306"/>' + glow(650, 600, 1000, "red", 0.55) + glow(1900, 300, 700, "moon", 0.3)
s += f'<g transform="translate(560,675) scale(3.1) translate(-480,440)">{dog("black", "stand", growl=True, rim="#ff8060", seed=7)}</g>'
s += f'<g transform="translate(1380,1300) scale(0.55)">{dog("white", "stand", seed=3)}</g>'
s += thumb_text("¿DE QUÉ\nCOLOR\nERA?", x=1220, y=330, size=230, fill="#ffffff", sw=26)
s += '<rect x="1230" y="870" width="760" height="16" fill="#c8141a"/>'
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "thumb_a.svg"), "w").write(thumb(s))
