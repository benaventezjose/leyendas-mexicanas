import sys, os, math
sys.path.insert(0, '/home/claude/pipeline'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from art import *
from caiman_parts import caiman_head_close, GOLD
s = '<rect width="2400" height="1350" fill="#02060a"/>' + glow(1600, 500, 1100, "moon", 0.55) + glow(1854, 615, 420, "warm", 0.7)
s += caiman_head_close(1480, 930, 0.85, mouth=0.35, rim="#cfe2ff")
# bridal veil and flower crown on the head
s += '<path d="M2400,330 C2250,300 2080,330 1990,420 C1940,520 1960,700 2020,860 C2080,700 2200,600 2400,580 Z" fill="#ffffff" opacity="0.3"/>'
for i, c in enumerate(["#e0507a", "#f0c040", "#ffffff", "#e0507a", "#f08a30", "#ffffff", "#e0507a"]):
    x = 1660 + i * 66; y = 470 - 40 * math.sin(i / 6 * math.pi)
    s += f'<circle cx="{x}" cy="{y:.0f}" r="34" fill="{c}"/><circle cx="{x}" cy="{y:.0f}" r="11" fill="#f6d040"/>'
s += '<rect width="2400" height="1350" fill="url(#vig)" opacity="0"/>'
s += thumb_text("SE CASÓ\nCON ELLA", x=90, y=330, size=270, fill="#ffffff", sw=26)
s += '<rect x="100" y="760" width="820" height="18" fill="#c8141a"/>'
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "thumb_a.svg"), "w").write(thumb(s))
