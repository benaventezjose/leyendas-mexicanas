import sys, os
sys.path.insert(0, '/home/claude/pipeline'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from art import *
from make_art import soldier_bust, kid_sil, canopy, place
s = '<rect width="2400" height="1350" fill="#03050c"/>' + glow(700, 500, 900, "moon", 0.55) + glow(700, 1350, 900, "red", 0.35)
s += canopy(500, -40, 800, 230, 7, "#a8c8ff", n=220, fruit=6, leaf=1.5)
s += f'<g filter="url(#ghost)">{soldier_bust(720, 600, 2.3, rim="#e8f4ff", ghost=True, cold=True)}</g>'
s += '<circle cx="646" cy="526" r="20" fill="#ffffff" filter="url(#glow)"/><circle cx="794" cy="526" r="20" fill="#ffffff" filter="url(#glow)"/>'
s += thumb_text("¿JUEGAS\nCONMIGO?", x=1320, y=380, size=245, fill="#ffffff", sw=28)
s += '<rect x="1330" y="700" width="900" height="18" fill="#c8141a"/>'
open("thumb_a.svg", "w").write(thumb(s))
