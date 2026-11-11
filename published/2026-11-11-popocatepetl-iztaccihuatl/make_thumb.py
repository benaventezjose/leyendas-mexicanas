import sys, os
sys.path.insert(0, '/home/claude/pipeline'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from art import *
from chars import *
from make_art import popo, plume
bg = sky("#03050c", "#1a2c44") + popo(2050, 1350, 620, 880, rock="#1a2638", dark="#080e16", snow="#cfdbe8", seed=5)
bg += plume(2050, 470, 1.3, "#8a96a4", 0.5, 3, -0.6) + glow(2050, 470, 260, "red", 0.9)
bg += glow(1420, 520, 800, "moon", 0.7)
face = '<g filter="url(#ghost)">' + izta_bust(1420, 500, 2.25, rim="#ffffff", pale=True, ghost_eyes=True, wind=0.8) + '</g>'
tint = '<rect width="2400" height="1350" fill="#7ab0ff" opacity="0.08"/>'
txt = thumb_text("VA A", 90, 430, 300) + thumb_text("DESPERTAR", 90, 760, 300, fill="#ff2a2a")
open('thumb_a.svg', 'w').write(thumb(bg, face, tint, txt))
