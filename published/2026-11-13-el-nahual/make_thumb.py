import sys, os
sys.path.insert(0, '/home/claude/pipeline'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from art import *
from chars import *
bg = '<rect width="2400" height="1350" fill="#04070e"/>' + moon(1650, 380, 520) + glow(1650, 500, 1200, "moon", 0.9)
face = f'<g transform="translate(1650,700) scale(2.0)">{beast_head(eyes="human", lids=0.25, smile=1.0)}</g>'
txt = thumb_text("OJOS DE", 80, 430, 270) + thumb_text("HOMBRE", 80, 720, 300, fill="#ff2a2a")
eyes = ''.join(f'<circle cx="{1650+x*2.0}" cy="{700-16}" r="130" fill="url(#warmglow)" opacity="0.9"/>' for x in (-116, 104))
face += eyes
open('thumb_a.svg', 'w').write(thumb(bg, face, txt))
