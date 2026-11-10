import sys, os
sys.path.insert(0, '/home/claude/pipeline'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from art import *
from chars import *
bg = '<rect width="2400" height="1350" fill="#06040a"/>' + glow(1550, 520, 1100, "moon", 0.9) + glow(1550, 1300, 700, "red", 0.5)
face = '<g filter="url(#ghost)">' + carmen_bust(1560, 600, 2.35, lids=0.0, smile=-0.3, rim="#dfeaff", wind=1.0) + '</g>'
eyes = ''.join(f'<circle cx="{1560+x*2.35:.0f}" cy="{600-19*2.35:.0f}" r="26" fill="#f0f8ff"/>' for x in (-31, 31))
blood = '<rect width="2400" height="1350" fill="#7ab0ff" opacity="0.12"/>'
txt = thumb_text("EL ÚLTIMO", 90, 400, 250) + thumb_text("BESO", 90, 720, 360, fill="#ff2a2a")
open('thumb_a.svg', 'w').write(thumb(bg, face, eyes, blood, txt))
